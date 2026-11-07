import ast, collections, json, re, sys
from pathlib import Path
W=Path(__file__).resolve().parent
sys.path.insert(0,str(W/'soan'))
import gram, sinh_r8 as s, dot_bien_r8 as d
from probes_r8 import AM,DUONG
old=list(AM.values())+list(DUONG.values())
CMD='python .claude/dev/packet_loop_test.py';PIPE=CMD+' | cat'
for f in ('rv-a1-8/work/probes.py','rv-a1-9/work/extra_shell_probes.py'):
    path=W/'soan/g1'/f
    cs=next(eval(compile(ast.Expression(n.value),str(path),'eval'),{'CMD':CMD,'PIPE':PIPE})
        for n in ast.walk(ast.parse(path.read_text())) if isinstance(n,ast.Assign) and getattr(n.targets[0],'id',None)=='cases')
    old += [(c[2]+'\n',c[1]) if 'a1-8' in f else (c[1]+'\n',c[2]) for c in cs]
new=[(run,sh) for b in s.kho() for sh in s.SHELL for run in (b,b+'\n')]
out={'KT_count':len(s.KT),'unique_bodies':len(s.kho()),'generated_inputs':len(new),'old_inputs':len(old), 'branch_mutants':[]}
# Same character widening as m-S15, but limited to each DANG branch.
# These only classify the existing supplied corpus; no new shell payload is executed.
for program,suffix in [('bash','sh'),('pwsh -NoProfile -File','ps1')]:
    for c in ";&|!(){}$`'\"\\<>#*?[]~+,@%^":
        wide=r'[A-Za-z0-9_.][A-Za-z0-9_./'+re.escape(c)+r'-]*'
        parts=[rf'python {gram.P}\.py',rf'bash {gram.P}\.sh',rf'pwsh -NoProfile -File {gram.P}\.ps1']
        parts[1 if suffix=='sh' else 2]=rf'{program} {wide}\.{suffix}'
        f=d.dung(DANG='(?:'+'|'.join(parts)+')')
        out['branch_mutants'].append({'branch':suffix,'char_code':ord(c),
            'old_diffs':sum(f(r,sh)!=gram.cp(r,sh) for r,sh in old),
            'generated_diffs':sum(f(r,sh)!=gram.cp(r,sh) for r,sh in new)})
def endpoints_only(run,shell):
    if isinstance(run,str):
        parts=run.removesuffix('\n').split(' | ')
        if len(parts)>2 and gram.RE_DON.fullmatch(parts[0]) and gram.RE_DON.fullmatch(parts[-1]):
            return None if shell=='bash' else 'ong_khong_bash_tuong_minh'
    return gram.cp(run,shell)
safe='python ops/a.py | true | python ops/b.py'
out['endpoints_only']={'old_diffs':sum(endpoints_only(r,sh)!=gram.cp(r,sh) for r,sh in old),
 'generated_diffs':sum(endpoints_only(r,sh)!=gram.cp(r,sh) for r,sh in new),
 'harmless_witness':{'reference':gram.cp(safe,'bash'),'mutant':endpoints_only(safe,'bash')}}
out['branch_survivors']=sum(x['old_diffs']==x['generated_diffs']==0 for x in out['branch_mutants'])
out['accepted_pipeline_lengths']=dict(collections.Counter(len(r.removesuffix('\n').split(' | ')) for r,sh in new if gram.cp(r,sh) is None))
print(json.dumps(out,ensure_ascii=False,indent=2))
(W/'corpus.json').write_text(json.dumps(out,ensure_ascii=False,indent=2))
