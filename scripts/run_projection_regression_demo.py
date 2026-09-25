from pathlib import Path
import json, sys
ROOT=Path(__file__).resolve().parents[1]; sys.path.insert(0,str(ROOT/'src'))
from esf.projection import DeterministicFormProjector
from esf.validation import validate_projected_form
p=DeterministicFormProjector(ROOT/'registry/forms/moh',ROOT/'registry/mappings/form_to_concepts.v0.2.json',ROOT/'registry/concepts/canonical_concepts.v0.2.json')
outdir=ROOT/'experiments/step3_projection_demo'; outdir.mkdir(parents=True,exist_ok=True)
summary=[]
for src in sorted((ROOT/'data/reviewed/regression_cases').glob('*.json')):
 d=json.load(open(src,encoding='utf-8')); facts=d['fact_graph']['facts']; case=src.stem
 rec={'case':case,'forms':{}}
 for fid in ['MOH_29_BV_02','MOH_15_BV_01']:
  obj=p.project(facts,fid); errs=validate_projected_form(obj)
  (outdir/f'{case}__{fid}.json').write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8')
  rec['forms'][fid]={'validation_errors':errs,'supported_fields':sum(x['status']=='SUPPORTED' for x in obj['fields']),'conflict_fields':sum(x['status']=='CONFLICT' for x in obj['fields'])}
 summary.append(rec)
(outdir/'summary.json').write_text(json.dumps(summary,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps({'cases':len(summary),'outputs':len(summary)*2,'validation_errors':sum(len(v['validation_errors']) for r in summary for v in r['forms'].values())},indent=2))
