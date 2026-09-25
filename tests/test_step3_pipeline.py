import json
from pathlib import Path
from esf.retrieval import ConceptRetriever
from esf.evidence import retrieve_evidence_turns
from esf.projection import DeterministicFormProjector
from esf.validation import validate_projected_form
ROOT=Path(__file__).resolve().parents[1]
REG=ROOT/'registry'

def retriever():
 return ConceptRetriever(REG/'concepts/canonical_concepts.v0.2.json',REG/'mappings/form_to_concepts.v0.2.json')

def projector():
 return DeterministicFormProjector(REG/'forms/moh',REG/'mappings/form_to_concepts.v0.2.json',REG/'concepts/canonical_concepts.v0.2.json')

def test_form_anchors_are_never_pruned():
 r=retriever(); out=r.retrieve('Tôi đau bụng từ sáng','MOH_29_BV_02',k=3)
 assert set(out['anchor_concepts']) <= set(out['candidate_concept_ids'])

def test_evidence_turn_retrieval_hits_obvious_turn():
 reg=json.load(open(REG/'concepts/canonical_concepts.v0.2.json'))
 c=next(x for x in reg['concepts'] if x['concept_id']=='RESP.DYSPNEA')
 turns=[{'turn_id':1,'speaker':'INTAKE_ASSISTANT','text':'Anh đến khám vì vấn đề gì?'},{'turn_id':2,'speaker':'PATIENT','text':'Từ sáng tôi hơi khó thở.'}]
 out=retrieve_evidence_turns(turns,c,top_n=1)
 assert out[0]['turn_id']==2

def test_projection_not_mentioned_is_not_negative():
 facts=[{'fact_id':'f1','concept_id':'ENCOUNTER.CHIEF_COMPLAINT','value':'khó thở','assertion':'POSITIVE','temporality':'CURRENT'}]
 out=projector().project(facts,'MOH_29_BV_02')
 by={x['technical_name']:x for x in out['fields']}
 assert by['LyDoVaoVien']['status']=='SUPPORTED'
 assert by['TienSuBenhBanThan']['status']=='NOT_MENTIONED'
 assert by['TienSuBenhBanThan']['value'] is None
 assert validate_projected_form(out)==[]

def test_same_fact_projects_to_two_forms():
 facts=[{'fact_id':'f1','concept_id':'HISTORY.FAMILY_CONDITION','value':'mẹ tăng huyết áp','assertion':'POSITIVE','temporality':'HISTORICAL'}]
 p=projector(); a=p.project(facts,'MOH_29_BV_02'); b=p.project(facts,'MOH_15_BV_01')
 assert next(x for x in a['fields'] if x['technical_name']=='TienSuBenhGiaDinh')['status']=='SUPPORTED'
 assert next(x for x in b['fields'] if x['technical_name']=='TienSuBenhGiaDinh')['status']=='SUPPORTED'

def test_conflict_is_flagged_not_overwritten():
 facts=[
 {'fact_id':'f1','concept_id':'HISTORY.PAST_CONDITION','value':'hen','assertion':'POSITIVE','temporality':'HISTORICAL'},
 {'fact_id':'f2','concept_id':'HISTORY.PAST_CONDITION','value':'không có hen','assertion':'NEGATIVE','temporality':'CURRENT'},
 ]
 out=projector().project(facts,'MOH_15_BV_01')
 fld=next(x for x in out['fields'] if x['technical_name']=='TienSuBenhBanThan')
 assert fld['status']=='CONFLICT'
