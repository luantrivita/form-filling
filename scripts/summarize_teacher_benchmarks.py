#!/usr/bin/env python3
from pathlib import Path
import json,argparse

def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--dir',default='experiments/llm_baselines'); args=ap.parse_args()
    rows=[]
    for p in sorted(Path(args.dir).glob('*.summary.json')):
        x=json.load(open(p,encoding='utf-8')); x['_file']=str(p); rows.append(x)
    keys=['model_id','split','mode','micro_concept_f1','macro_concept_f1','typed_value_accuracy_on_matched','exact_observation_match_rate','unsupported_fill_rate','schema_valid_rate','latency_p50_seconds','latency_p95_seconds']
    print('\t'.join(keys))
    for r in rows: print('\t'.join(str(r.get(k,'')) for k in keys))
if __name__=='__main__': main()
