"""Reject duplicate/line-less findings and an incorrect delta review identity."""
import json,pathlib,sys
def validate(v,head,tree,base,known):
    errors=[]
    for key,expected in [('reviewed_sha',head),('reviewed_tree',tree),('review_base_sha',base),('discovery_scope','delta_only')]:
        if v.get(key)!=expected:errors.append('identity:'+key)
    if v.get('verdict') not in ['approve','changes_requested','blocked']:errors.append('verdict')
    oldids={x['id'] for x in known['classes']};oldslugs={x['class_slug'] for x in known['classes']}
    seen=set()
    for f in v.get('findings',[]):
        fid=f.get('finding_id',f.get('id'));slug=f.get('class_slug')
        if not fid or not slug:errors.append('missing-id-or-class')
        if fid in oldids or slug in oldslugs:errors.append('duplicate-known-class')
        if fid in seen:errors.append('duplicate-id')
        seen.add(fid)
        if not isinstance(f.get('file'),str) or not f.get('file'):errors.append('missing-file')
        first=f.get('start_line');last=f.get('end_line')
        if type(first) is not int or type(last) is not int or first<1 or last<first:errors.append('invalid-lines')
        if not f.get('evidence') or not f.get('remediation'):errors.append('missing-causal-evidence-or-remediation')
    prior=v.get('previous_finding_status',[])
    ids=[x.get('finding_id',x.get('id')) for x in prior]
    if set(ids)!=oldids or len(ids)!=len(oldids):errors.append('prior-class-status-incomplete-or-duplicate')
    return errors
if __name__=='__main__':
    v=json.loads(pathlib.Path(sys.argv[1]).read_text());known=json.loads(pathlib.Path(sys.argv[2]).read_text());errors=validate(v,*sys.argv[3:6],known)
    print(json.dumps({'ok':not errors,'errors':errors}));sys.exit(bool(errors))
