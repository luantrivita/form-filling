from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from esf.retrieval import ConceptRetriever
r=ConceptRetriever(ROOT/'registry/concepts/canonical_concepts.v0.2.json',ROOT/'registry/mappings/form_to_concepts.v0.2.json')
res={}
for k in [5,10,20]:
 vals=[]; allcov=[]
 for p in sorted((ROOT/'data/reviewed/regression_cases').glob('*.json')):
  d=json.load(open(p,encoding='utf-8'))
  text='\n'.join(t['text'] for t in d['conversation']['turns'])
  gold={f['concept_id'] for f in d['fact_graph']['facts'] if f['concept_id'] in r.by_id}
  out=r.retrieve(text,'MOH_29_BV_02',k=k,min_top_score=0.0)
  cand=set(out['candidate_concept_ids'])
  vals.append(len(gold & cand)/len(gold) if gold else 1.0); allcov.append(gold<=cand)
 res[str(k)]={'mean_gold_recall':sum(vals)/len(vals),'all_gold_covered_cases':sum(allcov)/len(allcov)}
print(json.dumps(res,indent=2))
