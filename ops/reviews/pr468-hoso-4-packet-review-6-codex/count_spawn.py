import contextlib, io, json, os, subprocess, time
from harness import ROOT, OUT, module
os.environ.update({'TMPDIR':str(OUT/'tmp'),'GIT_ALLOW_PROTOCOL':'file','GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'commit.gpgsign','GIT_CONFIG_VALUE_0':'false'})
rows=[]
def measure(label,fn):
    old=subprocess.Popen;count=0
    def popen(*args,**kwargs):
        nonlocal count
        count+=1
        return old(*args,**kwargs)
    subprocess.Popen=popen;t=time.monotonic();out=io.StringIO()
    try:
        with contextlib.redirect_stdout(out):result=fn()
    finally: subprocess.Popen=old
    row={'phase':label,'Popen':count,'seconds':time.monotonic()-t,'result':repr(result)}
    (OUT/(label+'.stdout')).write_text(out.getvalue());rows.append(row)
    (OUT/'spawn-counts.json').write_text(json.dumps(rows,indent=2)+'\n')
    print(json.dumps(row),flush=True)
s=module(ROOT/'.claude/hooks/subagent_ghi_detect_test.py','subagent_count_review')
measure('subagent-base',lambda:[f(None)[0] for f in s.CA])
s.DOT_BIEN=[];s.DOT_BIEN_NHAM_TEST=[];s.DOT_BIEN_SETTINGS=[]
measure('subagent-empty',s.chay)
n=module(ROOT/'ops/nhanh_don_duoc_test.py','nhanh_count_review')
measure('nhanh-base',n.chay_ca)
measure('nhanh-mutants',n.chay_dot_bien)
