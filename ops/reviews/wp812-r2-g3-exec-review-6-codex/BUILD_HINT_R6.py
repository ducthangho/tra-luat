from pathlib import Path
import shutil,subprocess
src=Path('/tmp/wp812-r6-suite');dst=Path('/tmp/wp812-r6-hint')
if not dst.exists():shutil.copytree(src,dst,symlinks=True)
p=dst/'.claude/dev/packet_loop.py';s=(src/'.claude/dev/packet_loop.py').read_text()
def change(a,b):
 global s
 assert s.count(a)==1,(a[:100],s.count(a));s=s.replace(a,b,1)
change('''    p.write_text(
        json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\\n",
        encoding="utf-8",
        newline="\\n",
    )''','''    # Mọi lỗi serialization/encoding là lỗi đầu vào: đo TRƯỚC khi mở/truncate state.
    try:
        raw = (json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\\n").encode("utf-8")
    except (ValueError, TypeError, UnicodeError) as ex:
        _die(RC_STATE, f"state không mã hoá được: {type(ex).__name__}")
    p.write_bytes(raw)''')
change('''    return m


def _ten_provider''','''    if ten == "bien_nhan_v2":
        tap = ("ASSURANCE_CAN_DOC_LAP", "HO_MODEL_CHO_PHEP")
        if (any(type(getattr(m, k)) not in (set, frozenset) or not getattr(m, k)
                or not all(type(x) is str and x for x in getattr(m, k)) for k in tap)
                or any(not callable(getattr(m, k)) for k in api[3:])):
            _die(RC_STATE, f"KHÔNG ĐO ĐƯỢC: validator canon {ten} giao diện sai kiểu")
    return m


def _chay_canon(*args, **kwargs):
    try:
        return subprocess.run(*args, **kwargs)
    except (OSError, subprocess.SubprocessError, ValueError) as ex:
        _die(RC_GUARD, f"KHÔNG ĐO ĐƯỢC: chạy validator canon: {type(ex).__name__}")


def _ten_provider''')
change('p = subprocess.run([*(lp := [sys.executable, str(td / "ops" / "lease_publish.py")]),','p = _chay_canon([*(lp := [sys.executable, str(td / "ops" / "lease_publish.py")]),')
change('p = subprocess.run([*lp, "ai-dang-giu",','p = _chay_canon([*lp, "ai-dang-giu",')
change('''        neo = bnv._neo_git(Path(a.root), Path(a.bien_nhan).name, d) if d else (["không phải ánh xạ"], [])
        loi = list(bnv._thieu(d) if d else []) + neo[0] + neo[1] +''','''        try:
            neo = bnv._neo_git(Path(a.root), Path(a.bien_nhan).name, d) if d else (["không phải ánh xạ"], [])
            thieu = list(bnv._thieu(d) if d else [])
        except Exception as ex:  # H hỏng/không đo được vẫn phải giữ state và mã thoát có kiểm soát.
            _die(RC_BIEN_NHAN, f"KHÔNG ĐO ĐƯỢC: kiểm biên nhận canon: {type(ex).__name__}")
        loi = thieu + neo[0] + neo[1] +''')
p.write_text(s)
t=dst/'.claude/dev/packet_loop_test.py';s0=(src/'.claude/dev/packet_loop_test.py').read_text();extra=Path('HINT_CASES_R6.txt').read_text();t.write_text(s0.replace('\ndef chay_suite(script:',extra+'\ndef chay_suite(script:',1))
paths=['.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py']
patch=b''
for name in paths:
 r=subprocess.run(['git','diff','--no-index','--',str(src/name),str(dst/name)],capture_output=True)
 assert r.returncode in (0,1)
 patch+=r.stdout.replace(b'a'+str(src).encode()+b'/',b'a/').replace(b'b'+str(dst).encode()+b'/',b'b/')
Path('HINT.patch').write_bytes(patch)
r=subprocess.run(['git','-C',str(src),'apply','--check',str(Path('HINT.patch').resolve())],capture_output=True)
Path('HINT_APPLY_CHECK.log').write_bytes(r.stdout+r.stderr);Path('HINT_APPLY_CHECK.exit').write_text(str(r.returncode)+'\n');assert r.returncode==0,r.stderr
print('hint built; git apply --check rc=0')
