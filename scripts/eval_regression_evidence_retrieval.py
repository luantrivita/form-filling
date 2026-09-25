from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from esf.evidence import retrieve_evidence_turns
reg=json.load(open(ROOT/'registry/concepts/canonical_concepts.v0.2.json',encoding='utf-8'))
byid={c['concept_id']:c for c in reg['concepts']}
total=hit1=hit2=0; skipped=[]
for p in sorted((ROOT/'data/reviewed/regression_cases').glob('*.json')):
 d=json.load(open(p,encoding='utf-8')); turns=d['conversation']['turns']
 goldturn={a['fact_id']:set(a['turn_ids']) for a in d['evidence_alignment']['alignments'] if a.get('supported')}
 for f in d['fact_graph']['facts']:
  if f['fact_id'] not in goldturn or f['concept_id'] not in byid: continue
  total+=1; out=retrieve_evidence_turns(turns,byid[f['concept_id']],top_n=2)
  ranks=[x['turn_id'] for x in out]
  if ranks and ranks[0] in goldturn[f['fact_id']]: hit1+=1
  if goldturn[f['fact_id']] & set(ranks): hit2+=1
print(json.dumps({'facts_evaluated':total,'hit_at_1':hit1/total if total else 0,'hit_at_2':hit2/total if total else 0},indent=2))
