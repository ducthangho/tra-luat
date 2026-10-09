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

KV = {
    # ---- spec1 (r3, viet cho f721fb4): 14 cua r1 + R15-R23 + U1-U3 + M3a-d + N1-N7 + P/Q/T
    "s1:M1-bo-kiem-so": {"t193": G("M3 t", "(a) ", "(b) ")},
    "s1:M2-bo-include": {"t193": G("(c/d) include thêm windows")},
    "s1:M3-prefix": {"t193": G("(c/d) ubuntu-not-a-runner")},
    "s1:M4a-so-tan-cong": {"t193": SO}, "s1:M4b-so-t01": {"t193": SO},
    "s1:M3a-bo-t196": {"t193": SO}, "s1:M3b-them-t199": {"t193": SO}, "s1:M3c-them-t201": {"t193": SO},
    "s1:M3d-t200-sai-job": {"t193": SO},
    "s1:M8-bo-exclude": {"t193": G("(c/d) exclude")},
    "s1:M11-include-thieu-khoa": {"t193": G("(c/d) include sinh tổ hợp thiếu os")},
    "s1:R15-main-tin-so": {"t193": G("(c/d) ", "A4 ")},
    "s1:R20-absolute": {"t193": G("A5 alias ..")},
    "s1:P1-chi-tep": {"t193": G("(b) ")}, "s1:P2-chi-job": {"t193": G("(b) ")},
    "s1:Q-no-thi-mien": {"t193": G("(c/d) job vắng")},
    "s1:T1-strategy-kieu": {"t193": G("(c/d) strategy sai kiểu")},
    "s1:T2-matrix-kieu": {"t193": G("(c/d) matrix là biểu thức")},
    "s1:N5-include-kieu": {"t193": G("(c/d) literal + include là chuỗi")},
    "s1:U1-literal-som": {"t193": G("(c/d) fixed_exclude")},
    "s1:U2-list-som": {"t193": G("(c/d) list_exclude")},
    "s1:U3-truc-kieu": {"t193": G("(c/d) bad_other_axis")},
    "s1:M5-bo-goi-verifier": {"t194": G("nối: hai con cùng 0/0"), "t160": G("t125 phải xác minh CẢ HAI vế")},
    "s1:R17-bo-kiem-rc": {"t194": G("vế ĐỎ 'rc 7 mà không ca ĐỎ'")},
    "s1:R18-t125-bo-rc": {"t194": G("nối: hai con đủ ca, rc=7"), "t160": G("t125 phải xác minh CẢ HAI vế")},
    "s1:R16-bo-doichieu-BOQUA": {"t194": G("vế ĐỎ 'dòng BỎ QUA mà ra là QUA'")},
    "s1:N3-bo-doichieu-DO": {"t194": G("vế ĐỎ 'ĐỎ thiếu dòng ĐỎ'")},
    "s1:M6-chi-dem-marker": {"t194": G("vế ĐỎ 'trùng tên, đủ số ca'")},
    "s1:M7-bo-tk-vs-dem": {"t194": G("vế ĐỎ 'tổng kết lệch marker'")},
    "s1:M9-bo-BOQUA-trong-so": {"t194": G("vế ĐỎ 'bỏ qua ngoài sổ'")},
    "s1:M10-bo-dung-mot-tk": {"t194": G("vế ĐỎ 'hai dòng tổng kết'")},
    "s1:N1-bo-ca-trung": {"t194": G("vế ĐỎ 'CA kỳ vọng trùng'")},
    "s1:N2-bo-ra-hop-le": {"t194": G("vế ĐỎ 'trạng thái lạ'")},
    "s1:N7-regex-khong-CR": {"t194": G("vế QUA 'CRLF")},
    "s1:N4-t125-bo-chan": {"t160": G("classifier chỉ nhận cặp ĐÃ xác minh"), "t194": G("nối: hai con cùng 0/0")},
    "s1:N6-ten-tu-transcript": {"t194": G("nối: hai con cùng 0/0")},
    "s1:R21-nen-ghi-osname": {"t203": RO, "t193": TDG},     # o t193: NotImplementedError(WindowsPath) — r2/r3: KHONG tinh
    "s1:R22-chon-ghi-CA": {"t203": RO, "t193": SONG},        # o t193 song (r3) — ca dich la t203
    "s1:R23-so-ghi-so-that": {"t203": RO, "t193": G("(e) ")},
    # ---- spec2 (r3)
    "s2:R15p-tin-so-MAC-DINH": {"t193": G("A4 có Windows")},
    "s2:R20p-symlink-only": {"t193": G("A5 alias symlink")},
    "s2:V2-tk-khong-neo": {"t194": G("vế QUA 'dòng chẩn đoán GIỮA dòng")},
    "s2:V4-su-kien-khong-neo": {"t194": G("vế QUA 'dòng chẩn đoán GIỮA dòng")},
    "s2:V5-ra-khong-neo": {"t194": G("vế QUA 'dòng chẩn đoán GIỮA dòng")},
    "s2:V6-do-khong-neo": {"t194": G("vế QUA 'dòng chẩn đoán GIỮA dòng")},
    "s2:V7-bo-kiem-thoi-luong": {"t194": ("GHI",)},          # khong co ky vong truoc: B3 "thoi luong hop le"
    "s2:V8-rc-chi-ca-do": {"t194": G("vế ĐỎ 'rc 0 mà có ca ĐỎ'")},
    "s2:L4a-seam-ghi-environ": {"t203": RO}, "s2:L4b-seam-ghi-global-allow": {"t203": RO},
    "s2:L4c-seam-chdir": {"t203": RO}, "s2:L4d-seam-ghi-WORKFLOW_DANG": {"t203": G("RÒ trạng thái", "lượt mặc định")},
    "s2:L4e-seam-sua-NHAN-tren-sys.path": {"t203": RO},
    "s2:L4f-so-ghi-gia-tri-trong-sổ(in-place-doi-tuple)": {"t203": RO},
    "s2:L4g-chon-chen-vao-CA-roi-xoa-giu-doi-tuong": {"t203": SONG},   # tuong duong (r3)
    "s2:L4h-seam-doi-stdout": {"t203": SONG},                          # tuong duong (r3)
    # ---- spec5/6 (r3)
    "s5:R24-seam-ghi-argv": {"t203": RO}, "s5:R25-nen-dinh": {"t203": LMD},
    "s5:R26-chon-dinh": {"t203": LMD}, "s5:R27-so-dinh": {"t203": LMD},
    "s6:R25L-nen-dinh-LAST-wins": {"t203": LMD}, "s6:R25F-nen-dinh-FIRST-wins": {"t203": LMD},
    # ---- specA (r3 luot 2, viet cho 9d7a523)
    "sA:L1a-ind-1tang-chua-dky": {"t193": SO, "t70": SONG}, "sA:L1b-ind-3tang-chua-dky": {"t193": SO, "t70": SONG},
    "sA:L1c-ind-1tang-da-dky": {"t193": SO, "t70": SONG}, "sA:L1d-ind-3tang-da-dky": {"t193": SO, "t70": SONG},
    "sA:L1e-GO-chot-uv+1tang": {"t193": SONG, "t70": SONG}, "sA:L1f-GO-chot-uv+3tang": {"t193": SONG, "t70": SONG},
    "sA:L1g-GO-vedonvi-uv": {"t193": SONG},
    "sA:L1h-vedonvi-tang3": {"t193": G("ứng viên phải tính cả ca gọi helper BỌC")},
    "sA:L1i-def-long-chua-dky": {"t193": SONG, "t70": SONG},           # P4 L-A da chap nhan (human audit)
    **{f"sA:L2-{v}": {"t194": G("vế QUA 'dòng chẩn đoán GIỮA dòng")} for v in ("V2", "V4", "V5", "V6")},
    **{f"sA:L2-GO-vey+{v}": {"t194": SONG} for v in ("V2", "V4", "V5", "V6")},
    "sA:L3a-R25L": {"t203": LMD}, "sA:L3a-GO-luot5+R25L": {"t203": SONG}, "sA:L3b-R25F": {"t203": LMD},
    **{f"sA:{n}": {"t203": RO} for n in ("L3c-environ", "L3d-environ-xoa", "L3e-cwd", "L3f-syspath-insert",
                                         "L3g-syspath-xoa", "L3h-global-rebind-allow", "L3i-global-moi-ten",
                                         "L3j-global-xoa-ten", "R21", "R22", "R23", "R24", "L4f")},
    **{f"sA:{n}": {"t203": TDG} for n in ("L3c-GO-anh+environ", "L3e-GO-anh+cwd", "L3f-GO-anh+syspath",
                                          "L3h-GO-anh+global")},      # dot bien go cua reviewer tu hong (KeyError)
    **{f"sA:{n}": {"t203": SONG} for n in ("L3k-global-inplace-dict", "L3l-global-inplace-set",
                                           "L3m-global-inplace-list",   # P4 L-B da chap nhan (human audit)
                                           "L3n-sys.modules", "L3o-umask")},   # ngoai pham vi spec C1
    "sA:R26": {"t203": LMD}, "sA:R27": {"t203": LMD},
    # ---- SOLO (r3 luot 2): go RIENG mot khoa chup => dot bien cua khoa ay song; go khoa KHAC (doi chung) => van giet
    **{f"sSOLO:SOLO-GO-{k}+{n}": {"t203": SONG} for k, n in (("os.environ", "environ"), ("cwd", "cwd"),
                                                              ("sys.path", "syspath"), ("globals", "global"))},
    **{f"sSOLO:SOLO-GO-{o}+{n}(doi-chung)": {"t203": RO} for o, n in (("cwd", "environ"), ("sys.path", "cwd"),
                                                                       ("globals", "syspath"), ("os.environ", "global"))},
    # ---- moi (phien va nay)
    "moi:M4c-so-ten-la": {"t193": SO},
    "moi:L-677": {"t195": G("M2 tập (i)"), "t196": G("M3a: PR + có dấu + còn hạn"), "t197": G("M3b: Issue + có dấu"),
                  "t178": G("`lease_id` là `None`"), "t198": SONG},
    # tu kiem bo phan hang: ca ba PHAI ra TIN_DUNG_GIA o dung lop
    "moi:DC1-TypeError-truoc-chot": {"t193": TDG},        # lop A: DO_KHAC
    "moi:DC2-bang-helper-chung": {"t194": TDG},           # lop B: bang() that tu helper chung, thong diep lech
    "moi:DC3-except-doi-thanh-chot": {"t203": TDG},       # lop B: `except` cua t203 doi RuntimeError thanh chot()
}
KV_DC = {"moi:DC2-bang-helper-chung": {"t194": ["vế ĐỎ", "vế QUA", "nối:"]},
         "moi:DC3-except-doi-thanh-chot": {"t203": ["RÒ trạng thái"]}}   # chuoi cua mot ca giet THAT, de lop B so

LP = "ops/lease_publish.py"
MOI = [
    ("moi:M4c-so-ten-la", [(TEST, '"t200_M1_nguon_lease_publish_tuy_chon_that_su_duoc_dung")}',
                            '"t200_M1_nguon_lease_publish_tuy_chon_that_su_duoc_dung", "t999_ten_la_khong_ton_tai")}')]),
    ("moi:L-677", [(LP, '    if not isinstance(lease.get("lease_id"), (str, int)) or isinstance(lease.get("lease_id"), bool):\n'
                        '        raise Chan(RC_NOI_DUNG, "tiền kiểm: thiếu `lease_id` hoặc sai kiểu")\n', '')]),
    ("moi:DC1-TypeError-truoc-chot", [(TEST, "    uv = set(_ca_ung_vien_gian_tiep(CA))\n",
                                       "    uv = set(_ca_ung_vien_gian_tiep(CA)) | 1\n")]),
    ("moi:DC2-bang-helper-chung", [(TEST, '    """Transcript ĐÚNG DẠNG của `main()`; `ca_kq` = [(tên, QUA|DO|BO_QUA)], `tong_ket` ghi đè dòng cuối."""\n',
                                    '    """Transcript ĐÚNG DẠNG của `main()`; `ca_kq` = [(tên, QUA|DO|BO_QUA)], `tong_ket` ghi đè dòng cuối."""\n'
                                    '    bang(False, "DC2 helper chung")\n')]),
    ("moi:DC3-except-doi-thanh-chot", [(TEST, '    qua, hong, bo_qua = 0, [], []\n    so = SO_BO_QUA if so is None else so\n',
                                        '    qua, hong, bo_qua = 0, [], []\n    if nen is not None:\n'
                                        '        raise RuntimeError("DC3 loi vo can")\n    so = SO_BO_QUA if so is None else so\n')]),
]

DS = []
for tien, ten_tep, mut in (("s1", "spec1.py", None), ("s2", "spec2.py", None), ("s5", "spec5.py", None),
                           ("s6", "spec6.py", None), ("sA", None, MUT_A), ("sSOLO", None, MUT_SOLO)):
    for ten, _dich, reps in (mut if mut is not None else nap(ten_tep)):
        DS.append((f"{tien}:{ten}", [(TEST, o, n) for o, n in reps]))
DS += MOI
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
