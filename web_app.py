from flask import Flask, render_template, request, redirect, url_for, flash
import csv, os
from datetime import datetime
import pandas as pd
import numpy as np

BASE=os.path.dirname(os.path.abspath(__file__)); DATA=os.path.join(BASE,'data')
app=Flask(__name__); app.secret_key='campusly-pbl'
FILES={k:os.path.join(DATA,k+'.csv') for k in ['events','students','registrations','feedback']}
HEAD={'events':['event_id','event_name','date','venue','max_participants'],'students':['student_id','name','department','email'],'registrations':['registration_id','student_id','event_id'],'feedback':['student_id','event_id','rating','comment']}
os.makedirs(DATA,exist_ok=True)
for k,p in FILES.items():
    if not os.path.exists(p):
        with open(p,'w',newline='',encoding='utf-8') as f: csv.writer(f).writerow(HEAD[k])
def rd(k):
    try:return pd.read_csv(FILES[k]).fillna('')
    except:return pd.DataFrame(columns=HEAD[k])
def wr(k,d):d.to_csv(FILES[k],index=False)
def stats():
    f=rd('feedback'); r=pd.to_numeric(f.rating,errors='coerce').dropna() if not f.empty else pd.Series(dtype=float)
    return {'events':len(rd('events')),'students':len(rd('students')),'registrations':len(rd('registrations')),'feedback':len(f),'avg':round(float(r.mean()),2) if len(r) else 0}
def nextid():
    d=rd('registrations'); nums=[]
    for x in d.registration_id.astype(str):
        try: nums.append(int(x[1:]))
        except: pass
    return f'R{(max(nums)+1 if nums else 1):03d}'

@app.route('/')
def home():
    e,r=rd('events'),rd('registrations'); rows=[]
    for _,x in e.iterrows():
        n=int((r.event_id.astype(str)==str(x.event_id)).sum()) if not r.empty else 0
        rows.append({'name':x.event_name,'date':x.date,'venue':x.venue,'n':n,'cap':int(float(x.max_participants))})
    return render_template('dashboard.html',page='dashboard',stats=stats(),events=sorted(rows,key=lambda x:x['date'])[:6])

@app.route('/events',methods=['GET','POST'])
def events():
    if request.method=='POST':
        d=rd('events'); x={k:request.form.get(k,'').strip() for k in ['event_id','event_name','date','venue','max_participants']}
        try:
            datetime.strptime(x['date'],'%Y-%m-%d'); cap=int(x['max_participants']); assert cap>0
            if x['event_id'] in d.event_id.astype(str).values: raise ValueError('Event ID already exists.')
            wr('events',pd.concat([d,pd.DataFrame([x])],ignore_index=True)); flash('Event created successfully!','ok')
        except ValueError as ex: flash(str(ex) or 'Use a valid date and capacity.','bad')
        except: flash('Please fill every field correctly.','bad')
        return redirect(url_for('events'))
    e,r=rd('events'),rd('registrations'); rows=[]
    for _,x in e.iterrows():
        n=int((r.event_id.astype(str)==str(x.event_id)).sum()) if not r.empty else 0; rows.append({**x.to_dict(),'n':n})
    return render_template('events.html',page='events',events=rows)

@app.post('/events/delete/<eid>')
def delete_event(eid):
    e,r=rd('events'),rd('registrations')
    if not r.empty and (r.event_id.astype(str)==eid).any(): flash('Cannot delete an event with registrations.','bad')
    else: wr('events',e[e.event_id.astype(str)!=eid]); flash('Event deleted.','ok')
    return redirect(url_for('events'))

@app.route('/students',methods=['GET','POST'])
def students():
    if request.method=='POST':
        d=rd('students'); x={k:request.form.get(k,'').strip() for k in ['student_id','name','department','email']}
        if x['student_id'] in d.student_id.astype(str).values: flash('Student ID already exists.','bad')
        elif '@' not in x['email']: flash('Enter a valid email.','bad')
        else: wr('students',pd.concat([d,pd.DataFrame([x])],ignore_index=True)); flash('Student added successfully!','ok')
        return redirect(url_for('students'))
    return render_template('students.html',page='students',students=rd('students').to_dict('records'))

@app.route('/registrations',methods=['GET','POST'])
def registrations():
    s,e,r=rd('students'),rd('events'),rd('registrations')
    if request.method=='POST':
        sid,eid=request.form['student_id'],request.form['event_id']
        if sid not in s.student_id.astype(str).values: flash('Student ID not found.','bad')
        elif eid not in e.event_id.astype(str).values: flash('Event ID not found.','bad')
        elif not r.empty and ((r.student_id.astype(str)==sid)&(r.event_id.astype(str)==eid)).any(): flash('Duplicate registration is not allowed.','bad')
        else:
            cap=int(float(e.loc[e.event_id.astype(str)==eid,'max_participants'].iloc[0])); n=int((r.event_id.astype(str)==eid).sum())
            if n>=cap: flash('This event is already full.','bad')
            else: wr('registrations',pd.concat([r,pd.DataFrame([{'registration_id':nextid(),'student_id':sid,'event_id':eid}])],ignore_index=True)); flash('Registration created!','ok')
        return redirect(url_for('registrations'))
    rows=[]
    for _,x in r.iterrows():
        sn=s.loc[s.student_id.astype(str)==str(x.student_id),'name']; en=e.loc[e.event_id.astype(str)==str(x.event_id),'event_name']
        rows.append({'id':x.registration_id,'student':sn.iloc[0] if len(sn) else 'Unknown','event':en.iloc[0] if len(en) else 'Unknown','sid':x.student_id,'eid':x.event_id})
    return render_template('registrations.html',page='registrations',registrations=rows,students=s.to_dict('records'),events=e.to_dict('records'))

@app.post('/registrations/cancel/<rid>')
def cancel(rid):
    d=rd('registrations'); wr('registrations',d[d.registration_id.astype(str)!=rid]); flash('Registration cancelled.','ok'); return redirect(url_for('registrations'))

@app.route('/feedback',methods=['GET','POST'])
def feedback():
    s,e,r,f=rd('students'),rd('events'),rd('registrations'),rd('feedback')
    if request.method=='POST':
        sid,eid=request.form['student_id'],request.form['event_id']; rating=int(request.form['rating']); comment=request.form.get('comment','').strip()
        registered=not r.empty and ((r.student_id.astype(str)==sid)&(r.event_id.astype(str)==eid)).any()
        duplicate=not f.empty and ((f.student_id.astype(str)==sid)&(f.event_id.astype(str)==eid)).any()
        if sid not in s.student_id.astype(str).values: flash('Student ID not found.','bad')
        elif eid not in e.event_id.astype(str).values: flash('Event ID not found.','bad')
        elif not registered: flash('Only registered students can submit feedback.','bad')
        elif duplicate: flash('Feedback already submitted for this event.','bad')
        elif not 1<=rating<=5: flash('Rating must be 1–5.','bad')
        else: wr('feedback',pd.concat([f,pd.DataFrame([{'student_id':sid,'event_id':eid,'rating':rating,'comment':comment}])],ignore_index=True)); flash('Feedback submitted!','ok')
        return redirect(url_for('feedback'))
    rows=[]
    for _,x in f.iterrows():
        sn=s.loc[s.student_id.astype(str)==str(x.student_id),'name']; en=e.loc[e.event_id.astype(str)==str(x.event_id),'event_name']
        rows.append({'student':sn.iloc[0] if len(sn) else 'Unknown','event':en.iloc[0] if len(en) else 'Unknown','rating':int(x.rating),'comment':x.comment})
    return render_template('feedback.html',page='feedback',feedback=rows,students=s.to_dict('records'),events=e.to_dict('records'))

@app.route('/analytics')
def analytics():
    e,r,f=rd('events'),rd('registrations'),rd('feedback'); names=[]; ratings=[]; parts=[]
    for _,x in e.iterrows():
        eid=str(x.event_id); names.append(str(x.event_name)); rr=pd.to_numeric(f.loc[f.event_id.astype(str)==eid,'rating'],errors='coerce').dropna() if not f.empty else pd.Series(dtype=float); ratings.append(round(float(rr.mean()),2) if len(rr) else 0); parts.append(int((r.event_id.astype(str)==eid).sum()) if not r.empty else 0)
    vals=pd.to_numeric(f.rating,errors='coerce').dropna().tolist() if not f.empty else []; overall=round(float(np.mean(vals)),2) if vals else 0
    return render_template('analytics.html',page='analytics',names=names,ratings=ratings,parts=parts,vals=vals,overall=overall,stats=stats())

if __name__=='__main__': app.run(debug=True)
