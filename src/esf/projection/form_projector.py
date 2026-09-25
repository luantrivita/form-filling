from __future__ import annotations
import json
from pathlib import Path
from typing import Any

ACTIVE_ASSERTIONS={'POSITIVE','NEGATIVE','UNCERTAIN'}

def _render_fact(f:dict[str,Any], concept:dict[str,Any]|None=None) -> str:
    value=f.get('value')
    if isinstance(value,list): text=', '.join(map(str,value))
    elif isinstance(value,dict): text=json.dumps(value,ensure_ascii=False,sort_keys=True)
    elif value is None: text=''
    else: text=str(value)
    label=((concept or {}).get('labels') or {}).get('vi') or (concept or {}).get('canonical_name') or f.get('concept_id','')
    a=f.get('assertion','POSITIVE'); t=f.get('temporality','UNKNOWN')
    if a=='NEGATIVE': text=f"Không ghi nhận {label}" if not text or text.lower() in {'false','none','no'} else f"Không: {text}"
    elif a=='UNCERTAIN': text=f"Chưa chắc: {text or label}"
    if t=='RESOLVED': text=f"Đã hết: {text or label}"
    elif t=='HISTORICAL' and text: text=f"Tiền sử: {text}"
    return text.strip()

class DeterministicFormProjector:
    def __init__(self, forms_dir:str|Path, mapping_registry:str|Path, concept_registry:str|Path):
        self.forms={}
        for p in Path(forms_dir).glob('*.json'):
            f=json.load(open(p,encoding='utf-8')); self.forms[f['form_id']]=f
        self.mappings=json.load(open(mapping_registry,encoding='utf-8'))['mappings']
        reg=json.load(open(concept_registry,encoding='utf-8')); concepts=reg['concepts'] if isinstance(reg,dict) else reg
        self.concepts={c['concept_id']:c for c in concepts}

    def project(self, facts:list[dict[str,Any]], form_id:str) -> dict[str,Any]:
        if form_id not in self.forms: raise KeyError(form_id)
        fields=[]
        by_concept={}
        for f in facts: by_concept.setdefault(f['concept_id'],[]).append(f)
        for m in self.mappings:
            if m['form_id']!=form_id: continue
            relevant=[]
            for cid in m.get('concept_refs',[]): relevant.extend(by_concept.get(cid,[]))
            conflict=False
            bycid={}
            for f in relevant: bycid.setdefault(f['concept_id'],set()).add((str(f.get('value')),f.get('assertion'),f.get('temporality')))
            if any(len(v)>1 for v in bycid.values()): conflict=True
            rendered=[_render_fact(f,self.concepts.get(f['concept_id'])) for f in relevant]
            rendered=[x for x in rendered if x]
            status='CONFLICT' if conflict else ('SUPPORTED' if rendered else 'NOT_MENTIONED')
            fields.append({
                'field_id':m['field_id'],'technical_name':m['technical_name'],
                'status':status,'value':' ; '.join(rendered) if rendered else None,
                'source_fact_ids':[f.get('fact_id') for f in relevant],
                'projection_type':m.get('projection_type'),
                'renderer_status':'DRAFT_RESEARCH_RENDERER',
            })
        return {'form_id':form_id,'fields':fields}
