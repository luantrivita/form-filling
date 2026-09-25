from pathlib import Path
import json, sys, numpy as np
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import normalize
from scipy.sparse import hstack
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from esf.datasets.synur import iter_jsonl

schema=json.load((ROOT/'data/external/synur/synur_schema.json').open(encoding='utf-8'))
ids=[str(x['id']) for x in schema]
docs=[]
for x in schema:
    vals=' '.join(map(str,x.get('value_enum',[]) or []))
    docs.append(f"{x.get('name','')} {x.get('name','')} {vals}")

word=TfidfVectorizer(lowercase=True,ngram_range=(1,2),min_df=1,sublinear_tf=True)
char=TfidfVectorizer(lowercase=True,analyzer='char_wb',ngram_range=(3,5),min_df=1,sublinear_tf=True)
word.fit(docs); char.fit(docs)
D=normalize(hstack([word.transform(docs),char.transform(docs)]))

def eval_split(path):
    rows=list(iter_jsonl(path))
    qs=[r['transcript'] for r in rows]
    Q=normalize(hstack([word.transform(qs),char.transform(qs)]))
    scores=(Q@D.T).toarray()
    ks=[5,10,20,30,50]
    recall={k:[] for k in ks}; allcov={k:[] for k in ks}; first_rr=[]; gold_rr=[]
    for i,r in enumerate(rows):
        gold={str(o['id']) for o in r['observations']}
        order=np.argsort(-scores[i])
        ranked=[ids[j] for j in order]
        ranks={cid:rank+1 for rank,cid in enumerate(ranked)}
        for k in ks:
            top=set(ranked[:k]); hit=len(top & gold)
            recall[k].append(hit/len(gold) if gold else 1.0)
            allcov[k].append(1.0 if gold <= top else 0.0)
        relevant_ranks=[ranks[g] for g in gold if g in ranks]
        first_rr.append(1/min(relevant_ranks) if relevant_ranks else 0.0)
        gold_rr.extend([1/rank for rank in relevant_ranks])
    return {
      'rows':len(rows),
      'mean_gold_concepts':sum(len(r['observations']) for r in rows)/len(rows),
      'recall_at_k':{str(k):float(np.mean(v)) for k,v in recall.items()},
      'all_gold_covered_at_k':{str(k):float(np.mean(v)) for k,v in allcov.items()},
      'mrr_first_relevant':float(np.mean(first_rr)),
      'mean_gold_reciprocal_rank':float(np.mean(gold_rr)) if gold_rr else 0.0,
    }

out={'baseline':'hybrid_tfidf_word12_char35','index_fields':['concept_name','value_enum']}
for split in ['dev','test']:
    p=next((ROOT/'data/external/synur').glob(f'*_{split}-*.jsonl'))
    out[split]=eval_split(p)
path=ROOT/'experiments/public_baselines/synur_retrieval_tfidf.json'
path.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps(out,indent=2))
