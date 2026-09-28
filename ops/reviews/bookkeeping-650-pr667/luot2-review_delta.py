import hashlib, json, pathlib, subprocess, yaml
from run_checks import ROOT, OUT, ENV

def emit(k,v): print(k+'='+json.dumps(v,ensure_ascii=False))
def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
class UniqueLoader(yaml.SafeLoader): pass
def unique(loader,node,deep=False):
    result={}
    for kn,vn in node.value:
        key=loader.construct_object(kn,deep=deep)
        if key in result: raise ValueError('duplicate key '+str(key))
        result[key]=loader.construct_object(vn,deep=deep)
    return result
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique)
path=ROOT/'ops/land/pr666-wp650-land-evidence.yaml'
land=yaml.load(path.read_bytes(),Loader=UniqueLoader)
lease=yaml.load((ROOT/'ops/leases/c1a1a-exec-2-claude-20260927.yaml').read_bytes(),Loader=UniqueLoader)
emit('yaml_parsed','2/2; unique keys')
try:
    yaml.load('outer:\n  duplicate: 1\n  duplicate: 2\n',Loader=UniqueLoader)
except ValueError as e: emit('duplicate_negative_control',str(e))
else: raise AssertionError('duplicate accepted')
rb=json.loads(pathlib.Path('/tmp/review667-r2-input/github-readback.json').read_text())
r=rb['audit_comment_5864536112']; a=land['authorization_thu_tu_thoi_gian']['noi_dung_readback']
emit('readback_quoted_core_count',len(r['dong_trich']))
emit('readback_quotes_all_present',all(s in a['dong_trich_nguyen_van'] for s in r['dong_trich']))
emit('readback_actor_metadata_match',all(a[k]==r[k] for k in ('user','author_association')))
emit('readback_checkboxes_match',a['so_muc_x_tu_kiem']==r['boxes_checked_in_final_body'])
emit('authorization_sha_match',all(x==land['authorized_head_sha'] for x in [land['merge_api_expected_head_sha'],land['hai_cha'].split()[1],rb['pr666']['merge_api']['expectedHeadSha']]))
emit('literal_body_present','body' in r)
emit('current_packet_status',{k:land['trang_thai_packet'][k] for k in ('merged','landed')})
emit('remaining_conditions',land['trang_thai_packet']['dieu_kien_con_thieu_de_landed'])
emit('unmeasured_provenance',land['khong_do_duoc'][0])
emit('land_disclosed_deviations',[x['id'] for x in land['lech_protocol_khai']])
emit('provider_enum',land['provider'])
emit('provider_taxonomy',land['provider_taxonomy_da_provider'])
emit('lease_expiry',lease['lease_expires_at_utc'])
emit('lease_command',land['bookkeeping'][2]['lenh'])
for dst,src in [('luot1-verdict-day-du.md','VERDICT.md'),('luot1-audit_facts.py','audit_facts.py'),('luot1-reproduce_findings.py','reproduce_findings.py')]:
    p=ROOT/'ops/reviews/bookkeeping-650-pr667'/dst; q=pathlib.Path('/tmp/review667-r1-output')/src
    emit('historical_artifact',{'file':dst,'bytes':len(p.read_bytes()),'sha256':digest(p),'original_sha256':digest(q),'same_bytes':p.read_bytes()==q.read_bytes()})
for p in (path,pathlib.Path('/tmp/review667-r2-input/github-readback.json')): emit('input_hash',{'path':str(p),'sha256':digest(p)})
print('EXACT EXCERPT:')
for n,line in enumerate(path.read_text().splitlines(),1):
    if 27<=n<=39 or 145<=n<=156: print(f'{path.relative_to(ROOT)}:{n}: {line}')
print('PROTOCOL FOUR ANCHORS:')
p=ROOT/'docs/PROTOCOL_DA_PHIEN.md'
for n,line in enumerate(p.read_text().splitlines(),1):
    if 889<=n<=903: print(f'{p.relative_to(ROOT)}:{n}: {line}')
