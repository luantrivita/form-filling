from __future__ import annotations
from typing import Any
ALLOWED={'SUPPORTED','NOT_MENTIONED','AMBIGUOUS','CONFLICT','INSUFFICIENT_EVIDENCE','NOT_APPLICABLE'}

def validate_projected_form(obj:dict[str,Any]) -> list[str]:
    errors=[]
    if not obj.get('form_id'): errors.append('missing form_id')
    seen=set()
    for f in obj.get('fields',[]):
        fid=f.get('field_id')
        if fid in seen: errors.append(f'duplicate field_id:{fid}')
        seen.add(fid)
        if f.get('status') not in ALLOWED: errors.append(f'invalid status:{f.get("status")}')
        if f.get('status')=='NOT_MENTIONED' and f.get('value') not in (None,''):
            errors.append(f'NOT_MENTIONED has value:{fid}')
        if f.get('status')=='SUPPORTED' and not f.get('source_fact_ids'):
            errors.append(f'SUPPORTED without provenance:{fid}')
    return errors
