"""Operator evidence decisions; no browser/product integration."""
import json

def same_identity(a,b):
    return bool(a and b and all(a.get(k) is not None and a[k]==b.get(k) for k in ('pid','birth','image')))

def module_state(snapshot_ok,first_ok,first_error,next_error,entries,identity_valid,main_present):
    if not snapshot_ok:return 'unavailable'
    if not first_ok:return 'empty_snapshot' if first_error==18 else 'unavailable'
    if not identity_valid or not main_present or len({x['base'] for x in entries})!=len(entries):return 'inconsistent'
    return 'complete_walk' if next_error==18 else 'partial'

def presence(state,names,wanted):
    if wanted.lower() in [n.lower() for n in names]:return 'LISTED'
    return 'NOT_LISTED_IN_COMPLETE_WALK' if state=='complete_walk' else 'UNKNOWN'

def bridge(before,after,observed_path):
    return 'disk_file_verified' if before and before==after and before.get('path')==observed_path else 'UNKNOWN'

def readiness(startup,tab_url,expected_url,statuses,body,expected):
    if startup!='acknowledged':return 'not_run'
    if tab_url is None or body is None:return 'unknown'
    return 'fixture_verified' if tab_url==expected_url and statuses==[302,200] and body==expected else 'failed'

def cleanup(nonce,rows,remaining,ownership_unknown=False):
    expected=[(0,{'session':nonce,'status':'closed'}),(0,{'session':nonce,'deleted':True}),(1,{'isError':True,'error':f"The browser '{nonce}' is not open, please run open first"})]
    if len(rows)!=3 or remaining or ownership_unknown:return 'failed'
    for row,(rc,value) in zip(rows,expected):
        if row.get('rc')!=rc or row.get('stderr')!=b'':return 'failed'
        try:actual=json.loads(row.get('stdout',b''))
        except (ValueError,TypeError):return 'failed'
        if 'deleted' in value and type(actual.get('deleted')) is bool:value['deleted']=actual['deleted']
        if actual!=value:return 'failed'
    return 'verified'

def terminal(fullflow,clean,operator_rc,shell_rc=None):
    return {'success':fullflow=='passed' and clean=='verified' and operator_rc==0,'release_lock':clean=='verified','operator_child_rc':operator_rc,'transport_shell_rc':shell_rc}
