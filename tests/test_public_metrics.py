from esf.evaluation.public_metrics import precision_recall_f1, exact_observation_match, macro_concept_f1

def test_set_metrics():
    m=precision_recall_f1({'1','2'},{'2','3'})
    assert m['precision']==0.5 and m['recall']==0.5 and m['f1']==0.5

def test_exact_match_order_independent():
    a=[{'id':'1','value_type':'SINGLE_SELECT','value':'Yes'},{'id':'2','value_type':'NUMERIC','value':3}]
    b=list(reversed(a))
    assert exact_observation_match(a,b)

def test_macro_oracle_is_one():
    gold=[[{'id':'1'}],[{'id':'2'}]]
    assert macro_concept_f1(gold,gold)==1.0
