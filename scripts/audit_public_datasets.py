from pathlib import Path
import json, sys

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from esf.datasets.synur import iter_jsonl, observation_type_counts
from esf.datasets.mts_dialog import load_csv, section_counts

report={}
syn=ROOT/'data/external/synur'
for split in ['train','dev','test']:
    matches=list(syn.glob(f'*{split}*.jsonl'))
    if matches:
        rows=list(iter_jsonl(matches[0]))
        report[f'synur_{split}']={'file':matches[0].name,'rows':len(rows),'observation_type_counts':observation_type_counts(rows)}

mts=ROOT/'data/external/mts_dialog'
for p in sorted(mts.glob('*.csv')):
    rows_all=load_csv(p,previsit_only=False)
    rows_pre=load_csv(p,previsit_only=True)
    report[f'mts_{p.stem}']={'rows_total':len(rows_all),'rows_previsit':len(rows_pre),'previsit_section_counts':section_counts(rows_pre)}

out=ROOT/'docs/reports/PUBLIC_DATASET_AUDIT.json'
out.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
