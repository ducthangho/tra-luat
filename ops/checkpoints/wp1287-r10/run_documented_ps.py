"""Run actual documented PS helper/cleanup in each native shell; no product adapter."""
import sys,json,datetime,hashlib
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
import native_flow as M
kind=sys.argv[1];assert kind in ('ps51','ps7')
BASE=Path(r'C:\tl-win\wp1287-r10-ps-positive-20261110');ROOT=BASE/kind;E=ROOT/'evidence';INSTALL=Path(r'C:\tl-win\wp1287-r9-timeout-20261110\installation')
SHELL=r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe' if kind=='ps51' else r'C:\Program Files\PowerShell\7\pwsh.exe'
M.ROOT=ROOT;M.E=E;M.INSTALL=INSTALL;M.CLI=INSTALL/'node_modules/@playwright/cli/playwright-cli.js';M.NONCE='tl-pw-128710105101' if kind=='ps51' else 'tl-pw-128710100701'
M.BODY=('<!doctype html><html><head><meta charset="utf-8"><title>WP1287 candidate</title></head><body><p>controlled-source-wp1287-candidate '+M.NONCE+'</p></body></html>').encode()
M.ENV.update(TL_PW_NODE=M.NODE,TL_PW_CLI=str(M.CLI),TL_PW_SESSION=M.NONCE,TL_PW_ROOT=str(ROOT),TL_PW_RUN=str(E),NPM_CONFIG_USERCONFIG=str(ROOT/'npm-user-empty.conf'),NPM_CONFIG_GLOBALCONFIG=str(ROOT/'npm-global-empty.conf'),NPM_CONFIG_CACHE=str(ROOT/'npm-cache'))
original=M.command;cache={};alias={'close':'08-close','delete-data':'09-delete-data','verify-closed':'10-verify'}
def cli_record(label):
    records=[]
    for line in (E/'commands.tsv').read_text(encoding='utf-8-sig').splitlines():
        cols=line.split('\t')
        if len(cols)>=5 and cols[1]==label and cols[3].startswith('rc=') and cols[3][3:].lstrip('-').isdigit():
            records.append({'rc':int(cols[3][3:]),'start':cols[0],'end':cols[4]})
    assert len(records)==1,(label,'CLI_RC_NOT_PROVEN');r=records[0]
    seconds=(datetime.datetime.fromisoformat(r['end'].replace('Z','+00:00'))-datetime.datetime.fromisoformat(r['start'].replace('Z','+00:00'))).total_seconds()
    return {'rc':r['rc'],'stdout':(E/(label+'.json')).read_bytes(),'stderr':(E/(label+'.err')).read_bytes(),'timed_out':False,'documented_step':label,'seconds':seconds}
def command(label,args,timeout=90,track=True):
    if args[:2]!=[M.NODE,str(M.CLI)]:return original(label,args,timeout,track)
    if label in alias:
        if not cache:
            # Freeze diagnostic writers before the verbatim cleanup computes file hashes.
            if M.WORKER:
                proc,_,record=M.WORKER
                if proc.poll() is None:proc.terminate();proc.wait(timeout=3)
                record.update(worker_rc=proc.returncode,state='stopped_for_cleanup',end=M.stamp());M.PROBES.append(record);M.WORKER=None
            for scheduled,x,ispost in M.QUEUE:M.PROBES.append({'scheduled_offset_ns':scheduled,'post_open':ispost,'state':'not_run_cleanup_priority'})
            M.QUEUE.clear();M.save(E/'probe-schedule.json',M.PROBES)
            M.observer_tick=lambda post=False:M.observe()
            result=original('documented-cleanup',[SHELL,'-NoProfile','-NonInteractive','-File',str(BASE/'invoke-documented.ps1'),'cleanup','unused'],60,True)
            for name,step in alias.items():
                try:
                    row=cli_record(step)
                    # Total cleanup watchdog60s; each actual command must still finish<=20s.
                    if row['seconds']>20 or result['rc']!=0:row['timed_out']=True;row['rc']=None
                    cache[name]=row
                except BaseException:cache[name]={'rc':None,'stdout':b'','stderr':b'','timed_out':True,'documented_step':step}
            M.save(E/'documented-cleanup-receipt.json',{'operator_shell_rc':result['rc'],'source_sha256':M.sha(BASE/'documented-cleanup.ps1'),'no_commands_replayed':True,'steps':[{k:v for k,v in row.items() if k not in ('stdout','stderr')} for row in cache.values()]})
        return cache[label]
    argfile=E/(label+'-arguments.json');M.save(argfile,args[3:-1])
    outer=original(label,[SHELL,'-NoProfile','-NonInteractive','-File',str(BASE/'invoke-documented.ps1'),label,str(argfile)],timeout,True)
    row=cli_record(label)
    M.ROWS[-1].update(documented_cli_rc=row['rc'],powershell_rc=outer['rc'],documented_step=label);M.save(E/'commands.json',M.ROWS)
    if outer['rc']!=0 and row['rc']==0:row['rc']=None
    return row
M.command=command
grant=json.loads((ROOT/'execution-grant.json').read_text())
for name,digest in grant['helper_sha256'].items():assert M.sha(BASE/name)==digest and M.sha(ROOT/name)==digest
rc=M.flow()
M.save(E/'documented-shell-receipt.json',{'shell':kind,'actual_versions':json.loads((E/'shell-version-open.json').read_text()),'helper_sha256':M.sha(BASE/'documented-helper.ps1'),'cleanup_sha256':M.sha(BASE/'documented-cleanup.ps1'),'source_excerpts_sha256':M.sha(BASE/'source-excerpts.json'),'operator_child_rc':rc,'config_action_timeout_ms':10000,'config_launch_timeout_ms':30000,'scope':'Actual documented helper+whole Cleanup; controlled operator fixture/config/arguments; no claim every Setup/Capture block literal'})
sys.exit(rc)
