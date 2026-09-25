from __future__ import annotations
import json
from pathlib import Path
from typing import Any

class ConceptRetriever:
    """Lightweight lexical retriever for the internal canonical registry.

    V1 safety policy: target-form anchor concepts are always included. Dynamic
    retrieval only prunes additional concepts. Low-confidence queries may fall
    back to the full canonical registry.
    """
    def __init__(self, concept_registry: str | Path, mapping_registry: str | Path):
        from sklearn.feature_extraction.text import TfidfVectorizer
        from sklearn.preprocessing import normalize
        self._normalize = normalize
        reg=json.load(open(concept_registry,encoding='utf-8'))
        self.concepts=reg['concepts'] if isinstance(reg,dict) else reg
        self.by_id={c['concept_id']:c for c in self.concepts}
        self.mappings=json.load(open(mapping_registry,encoding='utf-8'))['mappings']
        self.ids=[c['concept_id'] for c in self.concepts]
        self.docs=[self._doc(c) for c in self.concepts]
        self.word=TfidfVectorizer(lowercase=True,ngram_range=(1,2),sublinear_tf=True)
        self.char=TfidfVectorizer(lowercase=True,analyzer='char_wb',ngram_range=(3,5),sublinear_tf=True)
        from scipy.sparse import hstack
        self._hstack=hstack
        self.word.fit(self.docs); self.char.fit(self.docs)
        self.D=normalize(hstack([self.word.transform(self.docs),self.char.transform(self.docs)]))

    @staticmethod
    def _doc(c: dict[str,Any]) -> str:
        labels=c.get('labels') or {}
        aliases=' '.join(c.get('aliases') or [])
        vals=' '.join(map(str,c.get('allowed_values') or []))
        return ' '.join(filter(None,[c.get('canonical_name',''),labels.get('vi',''),labels.get('en',''),aliases,c.get('description',''),vals]))

    def form_anchor_ids(self, form_id: str) -> set[str]:
        out=set()
        for m in self.mappings:
            if m['form_id']==form_id: out.update(m.get('concept_refs') or [])
        return out

    def retrieve(self, conversation_text: str, form_id: str, *, k: int=20,
                 min_top_score: float=0.03, full_schema_fallback: bool=True) -> dict[str,Any]:
        import numpy as np
        q=self._normalize(self._hstack([self.word.transform([conversation_text]),self.char.transform([conversation_text])]))
        scores=(q@self.D.T).toarray()[0]
        order=np.argsort(-scores)
        ranked=[{'concept_id':self.ids[i],'score':float(scores[i])} for i in order[:k]]
        anchors=self.form_anchor_ids(form_id)
        top_score=ranked[0]['score'] if ranked else 0.0
        fallback=bool(full_schema_fallback and top_score < min_top_score)
        if fallback:
            candidates=list(self.ids)
        else:
            candidates=list(dict.fromkeys(list(anchors)+[r['concept_id'] for r in ranked]))
        return {
            'form_id':form_id,'k':k,'top_score':top_score,
            'fallback_full_schema':fallback,
            'anchor_concepts':sorted(anchors),
            'ranked_dynamic':ranked,
            'candidate_concept_ids':candidates,
        }
