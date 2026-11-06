import copy, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile
from pathlib import Path

BASE=Path(__file__).resolve().parent.parent
WORK, REPO=BASE/'work', BASE/'repo'
os.environ.update(TMPDIR=str(WORK/'tmp'),PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_GLOBAL='/dev/null')
tempfile.tempdir=str(WORK/'tmp')

def load(name,path):
    s=importlib.util.spec_from_file_location(name,path)
    m=importlib.util.module_from_spec(s)
    s.loader.exec_module(m)
    return m

t=load('review_tests',REPO/'ops/gate_output_doi_chieu_test.py')
m=t.nap()
old_dir=WORK/'before-module'
old_dir.mkdir(exist_ok=True)
for f in ['gate_output_doi_chieu.py','ci_provenance.py']:
    (old_dir/f).write_bytes(subprocess.check_output(['git','show','be1aeee:ops/'+f],cwd=REPO))
old=load('before_gate',old_dir/'gate_output_doi_chieu.py')
text,p=t.f_ok()
out={'head':subprocess.check_output(['git','rev-parse','HEAD'],cwd=REPO).decode().strip(),'law_hash':m.bam(m.LUAT_v1)}
out['baseline']={'before':old.kiem(text,p,t.goc()),'after':m.kiem(text,p,t.goc())}

# Every numeric capture in each counted rule, independently, with linked repetitions preserved.
counts=[]
for muc in m.LUAT_v1['MUC']:
    for b in muc['buoc']:
        for kind,pattern in b['dau_hieu']:
            if kind!='DONG' or not re.compile(pattern).groups:
                continue
            matches=[]
            for line in text.splitlines():
                bm=m.RE_BUOC.fullmatch(line)
                if bm and bm[1] in b['ten'] and not bm[2] and (hit:=re.fullmatch(pattern,bm[3])):
                    matches.append((line,bm[3],hit))
            assert matches,pattern
            line,body,hit=matches[0]
            for group in range(1,len(hit.groups())+1):
                # All equal numeric runs in these per-rule samples are the same capture or backreference.
                value=hit[group]
                changed=re.sub(r'(?<!\w)'+re.escape(value)+r'(?!\d)','0',body)
                assert re.fullmatch(pattern,changed), (pattern,changed)
                variant=text.replace(line,line[:-len(body)]+changed,1)
                before=old.kiem(variant,p,t.goc())
                after=m.kiem(variant,p,t.goc())
                counts.append({'step':b['ten'][0],'pattern':pattern,'group':group,'input':changed,'before':before,'after':after})
                assert before[0]=='passed' and after[0]=='not_measured'
out['counts']=counts

R='        run: python .claude/dev/packet_loop_test.py\n'
CMD='python .claude/dev/packet_loop_test.py'
PIPE=CMD+' | cat'
# Benign shell-mode probes only: actual shell execution substitutes `false` for the test command.
cases=[
 ('original_late',None,PIPE+'\nset -o pipefail'),
 ('before',None,'set -euo pipefail\n'+PIPE),
 ('disabled',None,'set -o pipefail\nset +o pipefail\n'+PIPE),
 ('errexit_disabled',None,'set -o pipefail\nset +e\n'+PIPE),
 ('errexit_long_disabled',None,'set +o errexit\n'+CMD+'\ntrue'),
 ('set_wrong_arity',None,'set -x pipefail\n'+PIPE),
 ('compound_set',None,'set -o pipefail; '+PIPE),
 ('explicit_bash','bash',PIPE),
 ('explicit_sh','sh',PIPE),
 ('explicit_pwsh','pwsh','set -o pipefail\n'+PIPE),
 ('conditional_false',None,'if false; then\n  set -o pipefail\nfi\n'+PIPE),
 ('uncalled_function',None,'configure() {\n  set -o pipefail\n}\n'+PIPE),
 ('subshell_enable',None,'(\n  set -o pipefail\n)\n'+PIPE),
 ('command_substitution',None,'unused=$(\n  set -o pipefail\n)\n'+PIPE),
 ('continued_argument',None,'printf %s \\\nset -o pipefail\n'+PIPE),
 ('brace_disable','bash','{ set +o pipefail; }\n'+PIPE),
 ('builtin_disable','bash','builtin set +o pipefail\n'+PIPE),
 ('command_disable','bash','command set +o pipefail\n'+PIPE),
 ('quoted_option_disable','bash',"set '+o' 'pipefail'\n"+PIPE),
 ('continued_disable','bash','set +o \\\npipefail\n'+PIPE),
 ('compound_errexit',None,'true; set +e\n'+CMD+'\ntrue'),
 ('builtin_errexit',None,'builtin set +e\n'+CMD+'\ntrue'),
 ('quoted_errexit',None,"set '+e'\n"+CMD+'\ntrue'),
 ('function_pipe_conditional',None,'configure() {\n  set -o pipefail\n}\nif false; then\n  configure\nfi\n'+PIPE),
 ('subshell_pipe','bash','(\n  builtin set +o pipefail\n  '+PIPE+'\n)'),
 ('function_pipe','bash','run_test() {\n  builtin set +o pipefail\n  '+PIPE+'\n}\nrun_test'),
]
shell_rows=[]
for name,shell,run in cases:
    sh='' if shell is None else f'        shell: {shell}\n'
    yaml_block=sh+'        run: |\n'+''.join('          '+x+'\n' for x in run.splitlines())
    assert t.ci_goc().count(R)==1
    q=t.bien_the_yaml(p,lambda s:s.replace(R,yaml_block))
    before,after=old.kiem(text,q,t.goc()),m.kiem(text,q,t.goc())
    row={'name':name,'shell':shell,'run':run,'before':before,'after':after,'mode_result':m.che_do_shell(run,shell)}
    if shell!='pwsh':
        executable='sh' if shell=='sh' else 'bash'
        args=[executable,'--noprofile','--norc','-e'] if executable=='bash' else ['sh','-e']
        if shell=='bash': args+=['-o','pipefail']
        proc=subprocess.run(args+['-c',run.replace(CMD,'false')],capture_output=True)
        row['actual_shell_rc']=proc.returncode
        row['stdout']=proc.stdout.decode()
        row['stderr']=proc.stderr.decode()
    shell_rows.append(row)
out['shell']=shell_rows

# Check literal/non-count evidence remains permitted and KHONG remains exactly zero.
out['noncount_controls']={}
for name,variant in [('shard_zero',text),('counterexample_zero',text.replace('135/153 đột biến thường khai đối chứng','0/153 đột biến thường khai đối chứng')),
                     ('khong_one',text.replace('KHONG 0','KHONG 1')),('khong_doublezero',text.replace('KHONG 0','KHONG 00'))]:
    out['noncount_controls'][name]=m.kiem(variant,p,t.goc())

(WORK/'probes.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
print('BASELINE',out['baseline'])
print('COUNT_GROUPS',len(counts),'ALL_ZERO_REJECTED',all(x['after'][0]=='not_measured' for x in counts))
for row in shell_rows:
    print('SHELL',row['name'],'before='+row['before'][0],'after='+row['after'][0],'actual_rc='+str(row.get('actual_shell_rc')),row['mode_result'])
print('NONCOUNT',out['noncount_controls'])
print('LAW_HASH',out['law_hash'])
