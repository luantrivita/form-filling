from __future__ import annotations
from typing import Any

def retrieve_evidence_turns(turns: list[dict[str,Any]], concept: dict[str,Any], *, top_n:int=2) -> list[dict[str,Any]]:
    """Rank turns lexically for a target concept. Never fabricates spans."""
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    labels=concept.get('labels') or {}
    query=' '.join(filter(None,[concept.get('canonical_name',''),labels.get('vi',''),labels.get('en',''),' '.join(concept.get('aliases') or []),concept.get('description','')]))
    texts=[str(t.get('text','')) for t in turns]
    if not texts or not query.strip(): return []
    vec=TfidfVectorizer(lowercase=True,ngram_range=(1,2),analyzer='word')
    X=vec.fit_transform([query]+texts)
    scores=cosine_similarity(X[0],X[1:]).ravel()
    order=scores.argsort()[::-1][:top_n]
    return [{'turn_id':turns[i]['turn_id'],'speaker':turns[i].get('speaker'),'text':texts[i],'score':float(scores[i])} for i in order]
