from pathlib import Path
import json, sys
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, f1_score, classification_report
ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/'src'))
from esf.datasets.mts_dialog import load_csv
D=ROOT/'data/external/mts_dialog'
train=load_csv(D/'MTS-Dialog-TrainingSet.csv',previsit_only=True)
valid=load_csv(D/'MTS-Dialog-ValidationSet.csv',previsit_only=True)
tests=[
 ('test_chat',load_csv(D/'MTS-Dialog-TestSet-1-MEDIQA-Chat-2023.csv',previsit_only=True)),
 ('test_sum',load_csv(D/'MTS-Dialog-TestSet-2-MEDIQA-Sum-2023.csv',previsit_only=True)),
]
vec=TfidfVectorizer(lowercase=True,ngram_range=(1,2),min_df=2,max_features=40000,sublinear_tf=True)
X=vec.fit_transform([r['dialogue'] for r in train]); y=[r['section_header_norm'] for r in train]
clf=LogisticRegression(max_iter=3000,class_weight='balanced',C=2.0)
clf.fit(X,y)

def ev(name,rows):
    yy=[r['section_header_norm'] for r in rows]
    pred=clf.predict(vec.transform([r['dialogue'] for r in rows]))
    return {'rows':len(rows),'accuracy':accuracy_score(yy,pred),'macro_f1':f1_score(yy,pred,average='macro',zero_division=0),'micro_f1':f1_score(yy,pred,average='micro',zero_division=0),'weighted_f1':f1_score(yy,pred,average='weighted',zero_division=0),'report':classification_report(yy,pred,output_dict=True,zero_division=0)}
out={'baseline':'tfidf_word12_logreg_balanced','train_rows':len(train),'labels':sorted(set(y)),'validation':ev('validation',valid)}
for name,rows in tests: out[name]=ev(name,rows)
p=ROOT/'experiments/public_baselines/mts_section_tfidf_logreg.json'; p.write_text(json.dumps(out,indent=2),encoding='utf-8')
print(json.dumps({k:v for k,v in out.items() if k!='validation' and not k.startswith('test_')},indent=2))
for k in ['validation','test_chat','test_sum']:
 print(k,{m:round(out[k][m],4) for m in ['rows','accuracy','macro_f1','micro_f1','weighted_f1']})
