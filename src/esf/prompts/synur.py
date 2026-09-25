from __future__ import annotations
import json
from typing import Any

SYSTEM = """You are a clinical information extraction system. Extract only observations explicitly supported by the transcript. Return strict JSON only. Do not add diagnosis, interpretation, or unsupported values."""


def _compact_schema(schema: list[dict[str, Any]]) -> list[dict[str, Any]]:
    out=[]
    for x in schema:
        y={"id":str(x["id"]),"name":x["name"],"value_type":x["value_type"]}
        if x.get("value_enum") is not None:
            y["value_enum"]=x["value_enum"]
        out.append(y)
    return out


def build_messages(transcript: str, schema: list[dict[str, Any]]) -> list[dict[str,str]]:
    schema_json=json.dumps(_compact_schema(schema),ensure_ascii=False,separators=(",",":"))
    user=f"""TASK: Extract SYNUR observations from the clinical transcript using only the supplied schema.

OUTPUT FORMAT:
Return a JSON array only. Each item must have exactly:
{{"id":"<schema id>","value_type":"<schema value_type>","name":"<schema name>","value":<value>}}

RULES:
- Include an observation only when supported by the transcript.
- Never infer a value merely because it is clinically plausible.
- Use only IDs from the candidate schema.
- SINGLE_SELECT: value must be one allowed enum when an enum is supplied.
- MULTI_SELECT: value must be a JSON list and every item must be from the allowed enum when supplied.
- NUMERIC: value must be a JSON number, not a string.
- STRING: value must be concise and evidence-grounded.
- If no observation is supported, return [].
- Do not output markdown, explanations, or reasoning.

CANDIDATE SCHEMA:
{schema_json}

TRANSCRIPT:
{transcript}
"""
    return [{"role":"system","content":SYSTEM},{"role":"user","content":user}]
