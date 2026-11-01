import sys,os,subprocess,importlib.util,time
sys.path.insert(0,sys.argv[1]+'/ops')
spec=importlib.util.spec_from_file_location('m',sys.argv[1]+'/ops/cloud_agent_creds.py');m=importlib.util.module_from_spec(spec);spec.loader.exec_module(m)
import ctypes; ctypes.CDLL(None).prctl(36,1,0,0,0); m._SUBREAPER=False
def con_song(pid):
    try: return os.kill(pid,0) is None and open(f"/proc/{pid}/stat").read().rsplit(")",1)[1].split()[0]!="Z"
    except (ProcessLookupError,FileNotFoundError): return False
bad=0;N=int(sys.argv[2])
for i in range(N):
    p=subprocess.Popen(["sh","-c","sleep 30 & echo $!; sleep 30"],stdout=subprocess.PIPE,start_new_session=True)

    time.sleep(0.3)
    da,ra=m._giet_nhom(p)
    if not ra.split(): print("rong"); continue
    g=int(ra.split()[0])
    het=time.monotonic()+5
    while con_song(g) and time.monotonic()<het: time.sleep(0.02)
    if con_song(g):
        bad+=1; print("SONG", g, open(f"/proc/{g}/stat").read().split(")")[1].split()[0] if os.path.exists(f"/proc/{g}/stat") else "?")
    else:
        pass
    try: os.kill(g,9)
    except OSError: pass
    try: os.waitpid(g,os.WNOHANG)
    except ChildProcessError: pass
print("song_ngay_sau_giet",bad,"/",N)
