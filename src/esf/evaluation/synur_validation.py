from __future__ import annotations
import json
import re
from typing import Any


def extract_json_array(text: str) -> list[dict[str, Any]]:
    s=text.strip()
    # Remove common thinking blocks / fenced wrappers without relying on model-specific parsers.
    s=re.sub(r"<think>.*?</think>", "", s, flags=re.S|re.I).strip()
    if s.startswith("```"):
        s=re.sub(r"^```(?:json)?\s*", "", s, flags=re.I)
        s=re.sub(r"\s*```$", "", s)
    try:
        obj=json.loads(s)
    except json.JSONDecodeError:
        start=s.find("[")
        if start < 0: raise
        decoder=json.JSONDecoder()
        obj, _=decoder.raw_decode(s[start:])
    if not isinstance(obj,list):
        raise ValueError("model output must be a JSON array")
    if not all(isinstance(x,dict) for x in obj):
        raise ValueError("every observation must be an object")
    return obj


def validate_predictions(pred: list[dict[str,Any]], schema: list[dict[str,Any]]) -> tuple[bool,list[str]]:
    by_id={str(x["id"]):x for x in schema}
    errors=[]
    seen=set()
    for i,o in enumerate(pred):
        cid=str(o.get("id"))
        if cid in seen: errors.append(f"duplicate id {cid}")
        seen.add(cid)
        if cid not in by_id:
            errors.append(f"unknown id {cid}"); continue
        spec=by_id[cid]
        if o.get("name") != spec.get("name"):
            errors.append(f"{cid}: name mismatch")
        if o.get("value_type") != spec.get("value_type"):
            errors.append(f"{cid}: value_type mismatch")
        vt=spec.get("value_type"); value=o.get("value"); enum=spec.get("value_enum")
        if vt=="NUMERIC" and (not isinstance(value,(int,float)) or isinstance(value,bool)):
            errors.append(f"{cid}: expected numeric")
        if vt=="MULTI_SELECT":
            if not isinstance(value,list): errors.append(f"{cid}: expected list")
            elif enum and any(v not in enum for v in value): errors.append(f"{cid}: value outside enum")
        if vt=="SINGLE_SELECT" and enum and value not in enum:
            errors.append(f"{cid}: value outside enum")
        if vt=="STRING" and not isinstance(value,str):
            errors.append(f"{cid}: expected string")
    return (not errors),errors
