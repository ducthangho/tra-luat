from pathlib import Path
import os, subprocess, hashlib, json

ROOT = Path(__file__).resolve().parent
REPO = ROOT / 'cay-kho'
EVID = ROOT / 'evidence'
EVID.mkdir(exist_ok=True)
BASE = 'f4b513da5802d439aedbe58ae4a5cd38ff47d6ab'
HEAD = 'a8f74709578f3c68833d366ed80b66fc10fbf0a3'
CASES = [('1110',1,'review1110a'),('1110',2,'review1110b'),('1114',1,'review1114a'),('1114',2,'review1114b')]
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1', GIT_CONFIG_GLOBAL=str(ROOT/'audit.gitconfig'))
def sha(b): return hashlib.sha256(b).hexdigest()
def run(args, cwd=REPO, timeout=180):
    p = subprocess.run(args,cwd=cwd,env=ENV,stdout=subprocess.PIPE,stderr=subprocess.PIPE,timeout=timeout)
    return p
def git(*args, cwd=REPO):
    p=run(['git',*args],cwd)
    if p.returncode: raise RuntimeError(p.stderr.decode())
    return p.stdout
def save(name,obj):
    (EVID/name).write_text(json.dumps(obj,ensure_ascii=False,indent=2)+'\n')
def append(text):
    with (ROOT/'VERDICT.md').open('a') as f: f.write('\n'+text+'\n')
