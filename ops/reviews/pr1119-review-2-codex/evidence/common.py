import hashlib, json, os, pathlib, subprocess
S=pathlib.Path(__file__).resolve().parent
E=S/'evidence'; R=S/'work/head'
BASE='c82047da4d6f9546ce1d68282c37acf9567b74bc'
HEAD='8715ac9f591b27d9b176e9d656437ef4b71b54dc'
os.environ.update(PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0',GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='core.abbrev',GIT_CONFIG_VALUE_0='7')
ITEMS=[(1110,1,'review1110a'),(1110,2,'review1110b'),(1114,1,'review1114a'),(1114,2,'review1114b')]
def digest(b):return hashlib.sha256(b).hexdigest()
def git(*a,root=R):return subprocess.check_output(['git',*a],cwd=root)
def save(name,value): (E/name).write_text(json.dumps(value,ensure_ascii=False,indent=2)+'\n')
def note(s):
    with (S/'VERDICT.md').open('a') as f:f.write('\n'+s+'\n')
def logged(name,cmd,cwd):
    p=subprocess.run(cmd,cwd=cwd,capture_output=True)
    (E/(name+'.stdout')).write_bytes(p.stdout); (E/(name+'.stderr')).write_bytes(p.stderr)
    return dict(cmd=cmd,cwd=str(cwd),rc=p.returncode,stdout=name+'.stdout',stderr=name+'.stderr')
