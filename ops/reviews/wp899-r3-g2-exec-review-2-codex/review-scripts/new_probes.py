import importlib.util, sys, json, hashlib, re, subprocess
from pathlib import Path
import yaml
sys.dont_write_bytecode = True
R = Path(__file__).resolve().parent
root = R.parent
s = importlib.util.spec_from_file_location('new_tests', root/'ops/ci_provenance_test.py')
t = importlib.util.module_from_spec(s); s.loader.exec_module(t)
m = t.nap()
results = {}
x = 'python ' + t.DUONG_GIA
base = t.buoc(x, 'THU: 4/4 dat')
def p(name, rows, wf=None):
    lg=t.log_voi(rows)
    rc,out,prov,_=t.chay([(t.job(1),lg)], wf=wf or t.wf_tu(x))
    results[name]={'rc':rc, 'stdout':out, 'gate':t.gate(prov), 'blocks':m.tach_buoc(lg.splitlines()),'log':lg,'workflow':wf or t.wf_tu(x)}
    return results[name]

p('control', base)
p('CRLF', [r+'\r' for r in base])
p('empty_color_line', t.khoi([x,''], 'THU: 4/4 dat'))
p('whitespace_color_line', t.khoi([x,'  '], 'THU: 4/4 dat'), t.wf_tu(x+'\n  '))
p('blank_in_color_block', [base[0],base[1],t.T+' ',*base[2:]])
p('env_before_shell', [*base[:2],t.T+' env:',*base[2:]])
p('env_after_shell', [*base[:3],t.T+' env:',t.T+'   A: 1',*base[3:]])
p('nested_before_shell', [*base[:2],t.T+' ##[group]details',*base[2:]])
p('nested_after_shell_no_outer_close', [*base[:3],t.T+' ##[group]details',*base[3:]])
p('nested_after_shell_with_outer_close', [*base[:3],t.T+' ##[group]details',*base[3:], t.T+' ##[endgroup]'])
p('endgroup_suffix', [r.replace('##[endgroup]','##[endgroup]suffix') for r in base])
p('no_endgroup', [r for r in base if '##[endgroup]' not in r])
p('no_reset_ANSI', [r.replace('\x1b[0m','') for r in base])
p('late_color_before_real_close', [*base[:3],t.T+' ##[group]details',base[3],t.T+' \x1b[36;1mecho hidden\x1b[0m',base[4],base[3]],t.wf_tu(x+'\necho hidden',x))

# Unresolved uses-step origin: no top-level run in the actual job. The same
# run text exists only in a disabled job (or a skipped sibling step).
for where in ('other_job_after','other_job_before','same_job_skipped'):
    wf={'jobs':{'actual':{'runs-on':'ubuntu-latest','steps':[{'uses':'./.review/composite'}]}}}
    decoy={'run':x+'\n','if':False}
    if where=='same_job_skipped': wf['jobs']['actual']['steps'].append(decoy)
    else:
        other={'disabled':{'runs-on':'ubuntu-latest','if':False,'steps':[decoy]}}
        wf['jobs']=(other|wf['jobs']) if where=='other_job_before' else (wf['jobs']|other)
    rows=[t.T+' ##[group]Run ./.review/composite',t.T+' ##[endgroup]',*base]
    p('composite_'+where,rows,yaml.safe_dump(wf))
    wf2=yaml.safe_load(yaml.safe_dump(wf))
    if where=='same_job_skipped': wf2['jobs']['actual']['steps'].pop()
    else: del wf2['jobs']['disabled']
    p('composite_no_collision_'+where,rows,yaml.safe_dump(wf2))
    # The actual substep's env and shell are log metadata, invisible to the
    # top-level candidate mode guards.
    p('composite_hidden_mode_'+where,[*rows[:4], t.T+' shell: python -B .review/emit.py {0}',t.T+' env:',t.T+'   CI_DANG_KY_X: 1',*rows[5:]],yaml.safe_dump(wf))

# Long, exact header is supported; truncation never matches.
longx='python '+ ('a'*5000) + '.py'
p('long_header_exact',t.buoc(longx,'THU: 4/4 dat'),t.wf_tu(longx))
p('long_header_truncated',[t.T+' ##[group]Run '+longx[:100],*t.buoc(longx,'THU: 4/4 dat')[1:]],t.wf_tu(longx))

tot={'files':0,'groups_Run':0,'valid':0,'nested_in_metadata':0,'color_blank':0,'CRLF_files':0,'close_with_suffix':0,'env_before_shell':0}
for f in sorted((root/'.review-input/log-that').glob('*.log')):
    b=f.read_bytes(); lines=b.decode('utf8','replace').splitlines(); tot['files']+=1; tot['CRLF_files']+=b'\r\n' in b
    for i,line in enumerate(lines):
        z=m.than(line)
        if z.startswith('##[endgroup]') and z!='##[endgroup]':tot['close_with_suffix']+=1
        if '\x1b[36;1m' in line and not z.strip():tot['color_blank']+=1
        if not z.startswith('##[group]Run '):continue
        tot['groups_Run']+=1
        block=[]
        for v in lines[i+1:]:
            q=m.than(v)
            if q.startswith('##[endgroup]'):break
            block.append(q)
        tot['nested_in_metadata']+=any(v.startswith('##[group]') for v in block)
        env_at=next((j for j,v in enumerate(block) if v=='env:'),None)
        shell_at=next((j for j,v in enumerate(block) if v.startswith('shell: ')),None)
        tot['env_before_shell']+=env_at is not None and shell_at is not None and env_at<shell_at
    tot['valid']+=sum(b['hop_le'] for b in m.tach_buoc(lines))
results['real_log_extra_stats']=tot
(R/'new-probes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
for name,r in results.items():
    if 'gate' in r:print(name,r['rc'],r['gate']['trang_thai'],r['gate']['kich_ban']['buoc_xac_thuc'])
    else:print(name,r)
