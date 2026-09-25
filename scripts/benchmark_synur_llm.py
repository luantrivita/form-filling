#!/usr/bin/env python3
from __future__ import annotations
import argparse,json,os,sys,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from esf.datasets.synur import iter_jsonl
from esf.inference.openai_compat import OpenAICompatClient
from esf.prompts.synur import build_messages
from esf.evaluation.synur_validation import extract_json_array,validate_predictions
from esf.evaluation.synur_llm_metrics import score_example,aggregate
from esf.evaluation.split_guard import ensure_split_allowed


def lexical_topk_schema(transcript,schema,k):
    # Lightweight no-fit-per-sample lexical scoring. Benchmark reproducibility > sophistication here.
    import re,math
    def toks(s): return set(re.findall(r"[a-z0-9]+",s.lower()))
    q=toks(transcript)
    scored=[]
    for spec in schema:
        d=toks(spec.get('name','')+' '+' '.join(map(str,spec.get('value_enum') or [])))
        inter=len(q&d); denom=math.sqrt(max(1,len(q))*max(1,len(d)))
        scored.append((inter/denom,str(spec['id'])))
    scored.sort(reverse=True)
    ids={cid for _,cid in scored[:k]}
    return [x for x in schema if str(x['id']) in ids]


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--model-config',required=True)
    ap.add_argument('--endpoint',required=True,help='e.g. http://localhost:8000')
    ap.add_argument('--split',choices=['train','dev','test'],default='dev')
    ap.add_argument('--mode',choices=['full_schema','retrieval_top50'],default='full_schema')
    ap.add_argument('--limit',type=int,default=0)
    ap.add_argument('--resume',action='store_true')
    ap.add_argument('--output')
    args=ap.parse_args()
    ensure_split_allowed(args.split)
    cfg=json.load(open(args.model_config,encoding='utf-8'))
    schema=json.load(open(ROOT/'data/external/synur/synur_schema.json',encoding='utf-8'))
    data_path=next((ROOT/'data/external/synur').glob(f'*_{args.split}-*.jsonl'))
    rows=list(iter_jsonl(data_path))
    if args.limit: rows=rows[:args.limit]
    out=Path(args.output or ROOT/f"experiments/llm_baselines/{cfg['id']}_{args.split}_{args.mode}.jsonl")
    out.parent.mkdir(parents=True,exist_ok=True)
    if out.exists() and not args.resume:
        raise FileExistsError(f'{out} already exists; pass --resume or choose --output to avoid mixing runs')
    done=set()
    records=[]
    if args.resume and out.exists():
        for line in out.read_text(encoding='utf-8').splitlines():
            if line.strip():
                r=json.loads(line); done.add(str(r['id'])); records.append(r)
    client=OpenAICompatClient(args.endpoint)
    with out.open('a',encoding='utf-8') as f:
        for idx,row in enumerate(rows,1):
            if row['id'] in done: continue
            candidate=schema if args.mode=='full_schema' else lexical_topk_schema(row['transcript'],schema,50)
            rec={'id':row['id'],'model_id':cfg['id'],'hf_model':cfg['hf_model'],'split':args.split,'mode':args.mode}
            try:
                result=client.chat(model=cfg['hf_model'],messages=build_messages(row['transcript'],candidate),
                                   temperature=cfg['generation']['temperature'],max_tokens=cfg['generation']['max_tokens'])
                rec['latency_seconds']=result.latency_seconds; rec['usage']=result.usage; rec['raw_text']=result.text
                pred=extract_json_array(result.text)
                rec['parse_ok']=True; rec['prediction']=pred
                valid,errors=validate_predictions(pred,candidate)
                rec['schema_valid']=valid; rec['validation_errors']=errors
                rec['score']=score_example(pred,row['observations'])
            except Exception as e:
                rec.update({'parse_ok':False,'schema_valid':False,'error':repr(e)})
            f.write(json.dumps(rec,ensure_ascii=False)+'\n'); f.flush(); records.append(rec)
            print(f"[{idx}/{len(rows)}] {row['id']} parse={rec.get('parse_ok')} valid={rec.get('schema_valid')}")
    summary=aggregate(records)
    summary.update({'model_id':cfg['id'],'hf_model':cfg['hf_model'],'split':args.split,'mode':args.mode,'output_jsonl':str(out)})
    sp=out.with_suffix('.summary.json'); sp.write_text(json.dumps(summary,indent=2),encoding='utf-8')
    print(json.dumps(summary,indent=2))

if __name__=='__main__': main()
