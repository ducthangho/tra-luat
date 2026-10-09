import datetime, hashlib, json, pathlib, subprocess, sys, yaml
from run_checks import ROOT, OUT, ENV

def git(*args):
    p=subprocess.run(['git',*args],cwd=ROOT,env=ENV,capture_output=True)
    if p.returncode: raise RuntimeError((args,p.returncode,p.stderr.decode()))
    return p.stdout
def sha(b): return hashlib.sha256(b).hexdigest()
def show(k,v): print(k+'='+json.dumps(v,ensure_ascii=False))

class UniqueLoader(yaml.SafeLoader): pass
def unique(loader,node,deep=False):
    out={}
    for kn,vn in node.value:
        key=loader.construct_object(kn,deep=deep)
        if key in out: raise ValueError('duplicate key '+str(key))
        out[key]=loader.construct_object(vn,deep=deep)
    return out
UniqueLoader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG,unique)
landpath='ops/land/pr666-wp650-land-evidence.yaml'
leasepath='ops/leases/c1a1a-exec-2-claude-20260927.yaml'
land=yaml.load((ROOT/landpath).read_bytes(),Loader=UniqueLoader)
lease=yaml.load((ROOT/leasepath).read_bytes(),Loader=UniqueLoader)
rb=json.loads(pathlib.Path('/tmp/review667-r1-input/github-readback.json').read_text())
show('yaml_unique_keys','2/2 mappings, no duplicate keys')
show('readback_sha256',sha(pathlib.Path('/tmp/review667-r1-input/github-readback.json').read_bytes()))
show('land_sha256',sha((ROOT/landpath).read_bytes()))
show('lease_sha256',sha((ROOT/leasepath).read_bytes()))
show('lease_blob',git('rev-parse','HEAD:'+leasepath,'origin/ops/cap-lease-650:'+leasepath).decode().splitlines())
show('land_blob',git('rev-parse','HEAD:'+landpath).decode().strip())
show('lease_generation_revision_spec_hash_match',all(land['input_packet_generations'][0][a]==lease[b] for a,b in [('generation','generation'),('revision','revision'),('spec_sha256','spec_hash')]))
source=lease['spec_source_commit']+':'+lease['spec']
show('spec_source',source)
show('spec_source_blob',git('rev-parse',source).decode().strip())
show('spec_hashes',{'source':sha(git('show',source)),'local':sha((ROOT/lease['spec']).read_bytes()),'lease':lease['spec_hash']})
show('write_set_hash_match',sha(('\n'.join(sorted(lease['write_set']))+'\n').encode())==lease['write_set_hash'])
for rev in [land['authorized_head_sha'],land['merge_commit'],'origin/master','origin/ops/cap-lease-650','cb9ecc8']:
    show('commit',git('show','-s','--format=%H%n%T%n%P%n%cI',rev).decode().splitlines())
show('merge_tree_matches',git('rev-parse',land['merge_commit']+'^{tree}').decode().strip()==land['tree'])
show('merge_parents_match',git('show','-s','--format=%P',land['merge_commit']).decode().strip()==land['hai_cha'])
show('merge_time_matches',datetime.datetime.fromisoformat(git('show','-s','--format=%cI',land['merge_commit']).decode().strip())==datetime.datetime.fromisoformat(land['merged_at']))
show('reviewed_product_diff_vs_cb9ecc8',git('diff','--name-only','cb9ecc8',land['authorized_head_sha'],'--','.claude/dev','ops/specs').decode().splitlines())
show('A14_numstat',git('diff','--numstat',lease['immutable_acceptance_baseline'],land['authorized_head_sha'],'--',*lease['write_set']).decode().splitlines())
show('A14_vs_premerge_master',git('diff','--numstat',land['hai_cha'].split()[0],land['authorized_head_sha'],'--',*lease['write_set']).decode().splitlines())
for check in [land['pre_merge_checks'][1],*land['post_merge_checks']]:
    d=check['workflow_definition']; ref=d['tai_commit']+':'+d['path']
    show('workflow_definition_local',{'ref':ref,'full_commit':git('rev-parse',d['tai_commit']).decode().strip(),'blob':git('rev-parse',ref).decode().strip(),'blob_match':git('rev-parse',ref).decode().strip()==d['blob'],'sha256':sha(git('show',ref)),'sha256_match':sha(git('show',ref))==d['sha256']})
pr=land['pre_merge_checks'][1]
show('PR_job_ids_and_conclusions_match',all(rb['ci_pr_bf63bb1']['run_36379712476']['jobs'][k]==[v,'success'] for k,v in pr['jobs_success'].items()))
post=land['post_merge_checks']
show('master_ci_job_ids_match',post[0]['jobs_success']==rb['ci_master_f8a7829']['run_36387278453']['jobs'])
show('master_launcher_job_ids_match',{k.removeprefix('launcher-'):v for k,v in post[1]['jobs_success'].items()}==rb['ci_master_f8a7829']['run_36387278424']['jobs'])
show('time_delta_seconds',(datetime.datetime.fromisoformat(land['merged_at'])-datetime.datetime.fromisoformat(rb['audit_comment_5864536112']['updated_at'])).total_seconds())
show('readback_audit_keys',sorted(rb['audit_comment_5864536112']))
show('readback_PR_run_keys',sorted(rb['ci_pr_bf63bb1']['run_36379712476']))
show('readback_master_run_keys',{k:sorted(v) for k,v in rb['ci_master_f8a7829'].items()})
show('required_schema_fields_missing',sorted(set('schema_version mission_id generation provider role session_id input_packet_generations authorized_head_sha approver authorization_url land_operator merge_method merge_commit pre_merge_checks post_merge_checks bookkeeping'.split())-land.keys()))
show('land_operator_session',land['session_id'])
show('lease_executor_session',lease['g1_ghi_chu'])
show('local_remote_ref_count',len(git('for-each-ref','--format=%(refname)','refs/remotes/origin').decode().splitlines()))
show('land_nang_tran',land['nang_tran'])
wf=yaml.safe_load(git('show','bf63bb1:.github/workflows/ci.yml'))
for name,job in wf['jobs'].items():
    show('PR_checkout_definition_'+name,[step for step in job.get('steps',[]) if 'actions/checkout@' in step.get('uses','')])
show('PR_workflow_gate_evidence',[{k:step[k] for k in ('name','if','uses') if k in step} for step in wf['jobs']['gate']['steps'] if 'selftest' in step.get('name','') or 'gate-evidence' in step.get('name','')])
show('land_status_quote',land['post_merge_ghi_chu'])
show('unmeasured_quotes',land['khong_do_duoc'])
show('bookkeeping_quote',land['bookkeeping'][1])
