import json, subprocess, sys, tempfile, threading
from pathlib import Path
from datetime import datetime, timedelta, timezone
PL = Path(sys.argv[1]).resolve(); N = int(sys.argv[2]); ITER = int(sys.argv[3]); PKT = 9100
def han(): return (datetime.now(timezone.utc)+timedelta(hours=4)).strftime("%Y-%m-%dT%H:%M:%SZ")
quan_sat = {}
for it in range(ITER):
    with tempfile.TemporaryDirectory() as td:
        sd = Path(td)/"st"; sd.mkdir()
        subprocess.run([sys.executable,str(PL),"--state-dir",str(sd),"init","--packet",str(PKT),
            "--mission","54","--executor","claude","--reviewer","codex"],capture_output=True,check=True)
        subprocess.run([sys.executable,str(PL),"--state-dir",str(sd),"record-lease","--packet",str(PKT),
            "--lease-id","x","--granted-by","ducthangho","--evidence","e","--expires-utc",han()],
            capture_output=True,check=True)
        rao = threading.Barrier(N); ket=[None]*N
        def go(i):
            rao.wait()
            ket[i]=subprocess.run([sys.executable,str(PL),"--state-dir",str(sd),"begin-attempt",
                "--packet",str(PKT),"--provider","claude"],capture_output=True).returncode
        ts=[threading.Thread(target=go,args=(i,)) for i in range(N)]
        [t.start() for t in ts]; [t.join() for t in ts]
        thang=sum(1 for rc in ket if rc==0)
        used=json.loads((sd/f"wp{PKT}.json").read_text(encoding="utf-8"))["attempts_used"]
        quan_sat[(thang,used)] = quan_sat.get((thang,used),0)+1
for (t,u),c in sorted(quan_sat.items()):
    co = "  ← LỖ" if (t>1 or t!=u) else ""
    print(f"   {c:3d} lần · thắng={t} attempts_used={u}{co}")
