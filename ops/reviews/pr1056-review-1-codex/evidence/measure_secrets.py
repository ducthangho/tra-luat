from pathlib import Path
import importlib.util, re, subprocess, sys

root=Path(__file__).resolve().parent.parent/'cay-kho'
def load(name,path):
    spec=importlib.util.spec_from_file_location(name,root/path)
    mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod
guard=load('secret_guard','scripts/hooks/secret_guard.py')
pkg=load('pkg_secret_scan','scripts/pkg_secret_scan.py')
paths=subprocess.check_output(['git','-C',str(root),'diff','--name-only','6db9341','1aae17b'],text=True).splitlines()
patterns=guard._PATTERNS+pkg.PATTERNS
# Extra search only classifies data; never prints match values.
patterns += [('fine_grained_github', re.compile(r'github_pat_[A-Za-z0-9_]{30,}')),
             ('literal_credential_value', re.compile(r'(?i)[\"\x27]?(?:access_token|refresh_token|api_key|client_secret|password)[\"\x27]?\s*[:=]\s*[\"\x27][A-Za-z0-9_./+\-=]{16,}[\"\x27]'))]
credential_path=re.compile(r'(?i)(?:\.aws[/\\]credentials|\.codex[/\\]auth\.json|\.config[/\\](?:gcloud|gws)[/\\][^\s\"\x27]*|[/\\](?:credentials|creds|auth|cookies)\.json|\.ssh[/\\]id_[a-z0-9]+)')
hits=[]; pathhits=[]; scanned=0; skipped=[]
for path in paths:
    f=root/path
    b=f.read_bytes()
    # README existed before PR; scan only new rows for this audit's added material.
    if path=='ops/reviews/README.md':
        delta=subprocess.check_output(['git','-C',str(root),'diff','6db9341','1aae17b','--',path],text=True)
        s='\n'.join(l[1:] for l in delta.splitlines() if l.startswith('+') and not l.startswith('+++'))
    else:
        try:s=b.decode('utf-8')
        except UnicodeDecodeError:skipped.append(path);continue
    scanned+=1
    for name,rx in patterns:
        for m in rx.finditer(s):hits.append((path,s[:m.start()].count('\n')+1,name))
    for m in credential_path.finditer(s):pathhits.append((path,s[:m.start()].count('\n')+1,'credential_path'))
print('SCANNED_CHANGED_FILES',scanned,'SKIPPED_NON_UTF8',skipped,'patterns',len(patterns))
print('SECRET_PATTERN_HITS',len(hits));print(*hits,sep='\n')
print('CREDENTIAL_PATH_HITS',len(pathhits));print(*pathhits,sep='\n')
for n in (1,2):
    p=root/f'ops/reviews/pr1050-review-{n}-codex'
    data=[f for f in p.rglob('*') if f.is_file()]
    print('ROUND',n,'files',len(data),'pkg_scannable',sum(pkg._is_scannable(f) for f in data),'max_file_bytes',max(f.stat().st_size for f in data),'pkg_hits',pkg.scan(p))
