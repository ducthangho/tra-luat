"""Do LAI bang dot bien r1 + r2 + r3 (M3/M4) + r3 luot 2 tren BYTES DA LAND cua #687 (git archive 163fd5d).

Dung: python3 -B do_l5_687.py <thu_muc_lam_viec_moi> <cay_nen_163fd5d> [ten ...]
Moi dot bien: MOT ban sao tam rieng (ops/*.py, ops/*.sh, .github), moi neo khop DUNG 1 lan, tien trinh con moi,
`-B` + PYTHONDONTWRITEBYTECODE=1 (khong va cham .pyc). Ban sao KHONG xoa (de lai, ghi duong dan).

PHAN HANG BA LOP (CLAUDE.md "dot bien bi giet khong phai dot bien bi giet DUNG LY DO"):
  A  mdrv687.py trong tien trinh: CHOT | DO_KHAC | QUA (xem docstring mdrv687.py).
  B  thong diep cua CHOT phai chua MOT chuoi trong danh sach CHO PHEP cua (dot bien, ca dich) — viet TRUOC khi chay,
     tu dac ta/ma nguon (vế nao giu tinh chat bi dot bien pha). CHOT ma lech chuoi => TIN_DUNG_GIA.
  C  CLI that `python -B ops/lease_publish_test.py --chi-ca=<ca>`: rc 1 + dong `  ĐỎ  <ca>:` (hoac rc 0 + `1/1 đạt`).
GIET = A CHOT + B khop + C do. SONG = A QUA + C xanh. TIN_DUNG_GIA = A DO_KHAC, hoac A CHOT ma B lech. LECH_RIG = A/C trai.
Ky vong ('GIET', [...]) / ('SONG',) / ('TIN_DUNG_GIA',) duoc so voi hang => cot `dung_ky_vong`.
"""
import concurrent.futures as cf
import glob
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

W, BASE = os.path.abspath(sys.argv[1]), os.path.abspath(sys.argv[2])
CHI = sys.argv[3:]
HERE = os.path.dirname(os.path.abspath(__file__))
GOC = os.path.join(HERE, "spec-goc")
DRV = os.path.join(HERE, "mdrv687.py")
TEST = "ops/lease_publish_test.py"


def nap(ten, src=None):
    ns = {}
    exec(compile(src if src is not None else open(os.path.join(GOC, ten), encoding="utf-8").read(), ten, "exec"), ns)
    return ns["MUT"]


srcA = open(os.path.join(GOC, "specA.py"), encoding="utf-8").read()
MUT_A = nap("specA.py#chinh", srcA[:srcA.index("\nCMP=")])       # danh sach chinh L1a..L4f (truoc khi tep gan lai MUT)
MUT_SOLO = nap("specA.py#solo", srcA)                             # cuoi tep: MUT = SOLO (go tung khoa chup)


def G(*s):
    return ("GIET", list(s))


SONG, TDG = ("SONG",), ("TIN_DUNG_GIA",)
RO, LMD = G("RÒ trạng thái"), G("lượt mặc định phải dùng argv")
SO = G("sổ phải BẰNG")

# ===== BO SUNG (dang ky ky vong TRUOC khi chay; sau luot chinh 06:42Z..06:43Z) =====
# R15q: R15 cua r2 nhung LY DO BO QUA van neu nhan runs-on that ('ubuntu-latest') => (e) KHONG con bat duoc;
#       ca dich phai do o vế A4 (sổ MẶC ĐỊNH + YAML ở WORKFLOW_DANG đổi sang có Windows).
# V7q: bo kiem THOI LUONG ma KHONG lam hong phan tich trang thai (regex luoi `.*?` thay `\d+\.\d{3}s `). V7 cua r3
#       (`.*` tham) chet o vế 'bỏ qua ngoài sổ' vi doc `BO_QUA` thanh `QUA` — khong phai vi thoi luong.
KV = {
    "moi:R15q-tin-so-ly-do-giu-nhan": {"t193": G("A4 có Windows")},
    "moi:V7q-bo-thoi-luong-giu-trang-thai": {"t194": ("GHI",)},
}
KV_DC = {}
LP = "ops/lease_publish.py"
DS = [
    ("moi:R15q-tin-so-ly-do-giu-nhan", [(TEST,
        'try: ly_do = _ly_do_bo_qua_workflow(ex.tep, ex.ten_job, nen=nen) if dung_cap else ""',
        'try: ly_do = ("chỉ chạy Ubuntu; tin sổ; runs-on \'ubuntu-latest\'") if (dung_cap and so is SO_BO_QUA and '
        '(nen or os.name) == "nt") else (_ly_do_bo_qua_workflow(ex.tep, ex.ten_job, nen=nen) if dung_cap else "")')]),
    ("moi:V7q-bo-thoi-luong-giu-trang-thai", [(TEST,
        r're.fullmatch(r" \d+\.\d{3}s (QUA|DO|BO_QUA)[ \t\r]*", d)',
        r're.fullmatch(r".*?(QUA|DO|BO_QUA)[ \t\r]*", d)')]),
]
ten_ds = [t for t, _ in DS]
assert len(ten_ds) == len(set(ten_ds)), "ten dot bien trung"
assert set(ten_ds) == set(KV), f"KV lech danh sach: thieu={sorted(set(ten_ds) - set(KV))} thua={sorted(set(KV) - set(ten_ds))}"
if CHI:
    DS = [x for x in DS if x[0] in CHI or x[0] == "NEN"]


def dung_ban_sao(ten, sua):
    d = tempfile.mkdtemp(prefix=re.sub(r"[^A-Za-z0-9]+", "_", ten)[:40] + "-", dir=W)
    os.makedirs(d + "/ops")
    for f in glob.glob(BASE + "/ops/*.py") + glob.glob(BASE + "/ops/*.sh"):
        shutil.copy(f, d + "/ops/")
    shutil.copytree(BASE + "/.github", d + "/.github")
    loi = []
    for tep, old, new in sua:
        p = os.path.join(d, tep)
        s = open(p, encoding="utf-8").read()
        c = s.count(old)
        if c != 1:
            loi.append(f"NEO khop {c} lan trong {tep}: {old[:70]!r}")
            continue
        open(p, "w", encoding="utf-8", newline="").write(s.replace(old, new))
    return d, loi


ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE="1", PYTHONUTF8="1")


def chay_cap(ten, d, ca):
    p = subprocess.run([sys.executable, "-B", DRV, d, ca], capture_output=True, text=True, cwd=d, timeout=900, env=ENV)
    try:
        a = json.loads(p.stdout.strip().splitlines()[-1])
    except Exception:  # noqa: BLE001
        a = [{"ca": ca, "A": "DRIVER_ERR", "msg": (p.stdout + p.stderr)[-400:]}]
    q = subprocess.run([sys.executable, "-B", "ops/lease_publish_test.py", "--chi-ca=" + ca], capture_output=True,
                       text=True, cwd=d, timeout=900, env=ENV)
    tk = re.findall(r"(?m)^lease_publish: .*$", q.stdout)
    return a, {"rc": q.returncode, "tong_ket": tk[-1] if tk else None,
               "do": [ln[:300] for ln in q.stdout.splitlines() if ln.startswith("  ĐỎ  ")]}


def phan_hang(ten, ca, a, c):
    kv = KV.get(ten, {}).get(ca, ("GHI",)) if ten != "NEN" else SONG
    r = a[0] if len(a) == 1 else {"A": "NHIEU_CA", "msg": json.dumps(a, ensure_ascii=False)[:300]}
    c_do = c["rc"] == 1 and any(x.startswith(f"  ĐỎ  {r.get('ca', ca)}") for x in c["do"])
    c_xanh = c["rc"] == 0 and c["tong_ket"] == "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    cho_phep = kv[1] if kv[0] == "GIET" else KV_DC.get(ten, {}).get(ca, [])
    b = r.get("A") == "CHOT" and any(s in r.get("msg", "") for s in cho_phep)
    if r.get("A") == "QUA":
        hang = "SONG" if c_xanh else "LECH_RIG"
    elif r.get("A") == "CHOT":
        hang = ("GIET" if b else "TIN_DUNG_GIA") if c_do else "LECH_RIG"
    elif r.get("A") == "DO_KHAC":
        hang = "TIN_DUNG_GIA" if c_do else "LECH_RIG"
    else:
        hang = r.get("A", "?")
    return {"ten": ten, "ca": ca, "ky_vong": kv[0], "hang": hang,
            "dung_ky_vong": (kv[0] == "GHI") or (hang == kv[0]), "A": r.get("A"), "cls": r.get("cls"),
            "last": r.get("last"), "inca": r.get("inca"), "B_khop": b, "cho_phep": cho_phep,
            "C": c, "msg": r.get("msg", "")}


def mot(ten, sua):
    d, loi = dung_ban_sao(ten, sua)
    if loi:
        return [{"ten": ten, "ca": "-", "hang": "NEO_LOI", "dung_ky_vong": False, "loi": loi, "ban_sao": d}]
    ra = []
    cac_ca = sorted(KV[ten]) if ten != "NEN" else ["t70", "t160", "t178", "t193", "t194", "t195", "t196", "t197",
                                                   "t198", "t203"]
    for ca in cac_ca:
        a, c = chay_cap(ten, d, ca)
        x = phan_hang(ten, ca, a, c)
        x["ban_sao"] = d
        ra.append(x)
    return ra


def main():
    os.makedirs(W, exist_ok=True)
    tu = {"runner_sha256": hashlib.sha256(open(__file__, "rb").read()).hexdigest(),
          "driver_sha256": hashlib.sha256(open(DRV, "rb").read()).hexdigest(),
          "test_sha256_nen": hashlib.sha256(open(BASE + "/" + TEST, "rb").read()).hexdigest(),
          "lease_publish_sha256_nen": hashlib.sha256(open(BASE + "/" + LP, "rb").read()).hexdigest(),
          "python": sys.version.split()[0], "so_dot_bien": len(DS)}
    print("# " + json.dumps(tu, ensure_ascii=False), flush=True)
    kq = []
    viec = [("NEN", [])] + DS
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for ra in ex.map(lambda x: mot(*x), viec):
            for x in ra:
                kq.append(x)
                print(f"{x['ten'][:52]:52s} {x['ca']:5s} kv={x.get('ky_vong', '-'):12s} {x['hang']:12s} "
                      f"{'OK ' if x['dung_ky_vong'] else 'LECH'} | {(x.get('msg') or '; '.join(x.get('loi', [])))[:150]}",
                      flush=True)
    json.dump({"tu": tu, "kq": kq}, open(os.path.join(W, "ket-qua.json"), "w", encoding="utf-8"), ensure_ascii=False,
              indent=1)
    dot = [x for x in kq if x["ten"] != "NEN"]
    dem = {}
    for x in dot:
        dem[x["hang"]] = dem.get(x["hang"], 0) + 1
    lech = [x for x in kq if not x["dung_ky_vong"]]
    print(f"TONG: {len(dot)} cap (dot bien, ca dich) tren {len(DS)} dot bien | {dem} | lech ky vong: {len(lech)} | "
          f"nen: {[(x['ca'], x['hang']) for x in kq if x['ten'] == 'NEN']}", flush=True)


if __name__ == "__main__":
    main()
