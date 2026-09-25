import json,sys
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from esf.evaluation.synur_validation import extract_json_array,validate_predictions
from esf.evaluation.synur_llm_metrics import score_example,aggregate
from esf.prompts.synur import build_messages


def schema(): return json.load(open(ROOT/'data/external/synur/synur_schema.json',encoding='utf-8'))

def test_json_extraction_and_validation():
    s=schema(); spec=s[0]
    text='```json\n'+json.dumps([{"id":str(spec['id']),"value_type":spec['value_type'],"name":spec['name'],"value":spec.get('value_enum',["x"])[0]}])+'\n```'
    p=extract_json_array(text); ok,err=validate_predictions(p,s)
    assert ok,err

def test_metric_exact():
    g=[{"id":"1","value_type":"STRING","name":"Heart sounds","value":"Normal"}]
    s=score_example(g,g)
    assert s['concept_f1']==1 and s['exact_observation_match']

def test_metric_unsupported():
    g=[{"id":"1","value_type":"STRING","name":"Heart sounds","value":"Normal"}]
    p=g+[{"id":"2","value_type":"STRING","name":"Other","value":"x"}]
    s=score_example(p,g)
    assert s['concept_fp']==1 and s['unsupported_fill_count']==1

def test_prompt_has_schema_and_transcript():
    s=schema()[:2]; m=build_messages('hello transcript',s)
    assert 'hello transcript' in m[-1]['content'] and str(s[0]['id']) in m[-1]['content']

def test_model_configs_exist():
    for name in ['qwen3_30b_a3b_instruct_2507.json','medgemma_27b_text_it.json','baichuan_m2_32b.json']:
        cfg=json.load(open(ROOT/'configs/models'/name,encoding='utf-8'))
        assert cfg['role']=='teacher_candidate' and cfg['hf_model']
