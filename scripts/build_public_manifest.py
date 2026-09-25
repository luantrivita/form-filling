from pathlib import Path
import hashlib, json, csv
ROOT=Path(__file__).resolve().parents[1]

def sha256(p):
    h=hashlib.sha256()
    with p.open('rb') as f:
        for b in iter(lambda:f.read(1024*1024),b''): h.update(b)
    return h.hexdigest()

items=[]
for p in sorted((ROOT/'data/external').rglob('*')):
    if not p.is_file(): continue
    rec={'path':str(p.relative_to(ROOT)),'bytes':p.stat().st_size,'sha256':sha256(p)}
    if p.suffix=='.jsonl':
        rec['rows']=sum(1 for line in p.open(encoding='utf-8') if line.strip())
    elif p.suffix=='.csv':
        with p.open(encoding='utf-8-sig',newline='') as f: rec['rows']=sum(1 for _ in csv.DictReader(f))
    elif p.name=='synur_schema.json':
        rec['concepts']=len(json.load(p.open(encoding='utf-8')))
    items.append(rec)
out={'manifest_version':'0.1','sources':['microsoft/SYNUR','abachaa/MTS-Dialog'],'files':items}
path=ROOT/'data/external/PUBLIC_DATASET_MANIFEST.json'
path.write_text(json.dumps(out,indent=2,ensure_ascii=False),encoding='utf-8')
print(path)
