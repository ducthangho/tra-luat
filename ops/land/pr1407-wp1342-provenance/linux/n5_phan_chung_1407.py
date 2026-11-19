"""Phan chung N5 (dac ta r4 §5): dot bien MO chot claim Windows trong `_1174_platform` phai DO tai assertion dich cua
`wp1174_windows_claim_rejected`; ban sach phai DAT. Dot bien ghi ra BAN SAO TAM, khong sua cay that.
Dung: python -I -B n5_phan_chung_1407.py <thu muc .claude/dev cua cay da checkout>
GIET <=> sach DAT VA dot bien do bang AssertionError VA khung cuoi cua traceback trong packet_loop_test.py nam o DUNG dong
assertion dich (dong chua `_call1174(m._1174_platform, "Windows", "ext4", 0xEF53) is False`) VA doi chung wp1174_witness_valid
DAT tren ban dot bien. Moi ket cuc khac: KHONG GIET (rc 1)."""
import json, os, subprocess, sys, tempfile
from pathlib import Path

TIM = 'return os_name == "Linux" and (fs_name, magic) in (("ext4", 0xEF53), ("xfs", 0x58465342))'
THAY = 'return os_name in ("Linux", "Windows") and (fs_name, magic) in (("ext4", 0xEF53), ("xfs", 0x58465342))'
DICH, DOI_CHUNG = "wp1174_windows_claim_rejected", "wp1174_witness_valid"
DONG_DICH = 'assert _call1174(m._1174_platform, "Windows", "ext4", 0xEF53) is False'
VO = r'''
import json, sys, tempfile, traceback, warnings
from pathlib import Path
warnings.simplefilter("ignore")
dev, script, ten = sys.argv[1:4]
sys.path.insert(0, dev)
import packet_loop_test as t
with tempfile.TemporaryDirectory() as td:
    try:
        dict(t.CASES)[ten](t.Ctx(Path(script), Path(td)))
        kq = ["DAT", None, None, None]
    except t.BoQua as ex:
        kq = ["KHONG_DO", "BoQua", str(ex), None]
    except AssertionError as ex:
        fr = [f for f in traceback.extract_tb(ex.__traceback__) if f.filename.endswith("packet_loop_test.py")]
        kq = ["DO", "AssertionError", (fr[-1].lineno if fr else None), (fr[-1].line if fr else None)]
    except BaseException as ex:
        kq = ["KHONG_DO", type(ex).__name__, str(ex)[:300], None]
print("KQ_N5 " + json.dumps(kq, ensure_ascii=True))
'''


def chay(dev, script, ten):
    p = subprocess.run([sys.executable, "-B", "-c", VO, str(dev), str(script), ten], capture_output=True, text=True,
                       timeout=180, encoding="utf-8", errors="backslashreplace", env=dict(os.environ, PYTHONUTF8="1"))
    d = [x for x in p.stdout.splitlines() if x.startswith("KQ_N5 ")]
    return json.loads(d[-1][6:]) if d else ["KHONG_DO", f"rc={p.returncode}", p.stderr[-300:], None]


def main():
    sys.stdout.reconfigure(encoding="utf-8", errors="backslashreplace")
    dev = Path(sys.argv[1]).resolve()
    goc = (dev / "packet_loop.py").read_text(encoding="utf-8")
    test = (dev / "packet_loop_test.py").read_text(encoding="utf-8").splitlines()
    print("tim khop", goc.count(TIM), "cho; dong dich khop", sum(DONG_DICH in x for x in test), "dong")
    if goc.count(TIM) != 1 or sum(DONG_DICH in x for x in test) != 1:
        print("KHONG DO: neo khong khop dung mot cho"); return 1
    dong_dich = next(i + 1 for i, x in enumerate(test) if DONG_DICH in x)
    with tempfile.TemporaryDirectory(prefix="n5_phan_chung_") as td:
        ban = Path(td) / "packet_loop_n5_mo_windows.py"
        ban.write_text(goc.replace(TIM, THAY, 1), encoding="utf-8", newline="\n")
        compile(ban.read_text(encoding="utf-8"), str(ban), "exec")
        sach, do, dc = chay(dev, dev / "packet_loop.py", DICH), chay(dev, ban, DICH), chay(dev, ban, DOI_CHUNG)
    print("ban sach   ", DICH, sach)
    print("dot bien   ", DICH, do, f"(dong assertion dich = {dong_dich})")
    print("doi chung  ", DOI_CHUNG, "tren ban dot bien", dc)
    giet = sach[0] == "DAT" and do[0] == "DO" and do[1] == "AssertionError" and do[2] == dong_dich and dc[0] == "DAT"
    print("KET QUA:", "GIET dung assertion dich" if giet else "KHONG GIET")
    return 0 if giet else 1


if __name__ == "__main__":
    sys.exit(main())
