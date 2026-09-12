# -*- coding: utf-8 -*-
"""Catalog dot bien cho 4 lop ban va #512. Moi mutant: cay RIENG ngoai kho, ten tep RIENG, -B (khong .pyc).

Doi bang chung DUONG: ca DICH phai xuat hien trong dong `  DO  <ten ca>:` VA rc != 0.
Mutant chet vi ly do KHAC (ca khac do, hay ImportError) = TIN DUNG GIA -> bao DO cho catalog.
"""
import os, re, shutil, subprocess, sys, tempfile, time
from pathlib import Path

GOC = Path(sys.argv[1]).resolve()
GOC_TEST = GOC / "ops" / "lease_publish_test.py"
NGUON = GOC_TEST.read_text(encoding="utf-8")

MUTANT = [
    ("giet-chi-PID-khong-giet-cay", "t154",
     '''    buoc = []
    killpg, getpgid = getattr(os, "killpg", None), getattr(os, "getpgid", None)''',
     '''    p.kill(); p.wait(timeout=cho_giay); return "DOT BIEN: chi giet PID"
    buoc = []
    killpg, getpgid = getattr(os, "killpg", None), getattr(os, "getpgid", None)'''),
    ("bo-start_new_session", "t154",
     '''        them["start_new_session"] = True''',
     '''        pass  # DOT BIEN: khong tach nhom'''),
    ("bo-chot-selector-khong-khop", "t155",
     '''        if not tien_to or not cac_ca:''',
     '''        if False:  # DOT BIEN'''),
    ("AB_HAN_GIAY-ghi-tay-420", "t156",
     '''AB_HAN_GIAY = _han_ngoai_toi_thieu(AL_HAN_GIAY, SC_HAN_TONG_GIAY, CD_HAN_TONG_GIAY,
                                   AB_SUITE_DO_DUOC_GIAY, AB_DU_PHONG_GIAY)      # 950''',
     '''AB_HAN_GIAY = 420  # DOT BIEN'''),
    ("tee-chi-in-o-cuoi", "t157",
     '''                for d in dong:
                    with khoa:
                        print(f"{tien_to} {d.decode('utf-8', 'replace').rstrip(chr(13))}", flush=True)''',
     '''                for d in dong:
                    if xong:  # DOT BIEN: chi in khi con da xong
                        with khoa:
                            print(f"{tien_to} {d.decode('utf-8', 'replace').rstrip(chr(13))}", flush=True)'''),
    ("tee-bo-tien-to", "t157",
     '''                        print(f"{tien_to} {d.decode('utf-8', 'replace').rstrip(chr(13))}", flush=True)''',
     '''                        print(f"{d.decode('utf-8', 'replace').rstrip(chr(13))}", flush=True)'''),
    ("ngan-sach-cap-lai-han-toi-thieu", "t156",
     '''        con_lai = het - time.monotonic()
        if con_lai <= 0:
            raise HetNganSachDay(i, len(ket), ngan_sach_giay)
        ket.append(chay(lenh, capture_output=True, text=True, timeout=con_lai))''',
     '''        con_lai = het - time.monotonic()
        ket.append(chay(lenh, capture_output=True, text=True, timeout=max(1.0, con_lai)))'''),
    # ── BON MUTANT REVIEWER TIM RA SONG SOT TREN 8ffd062 (M09-M13) — phai CHET tren ban HINT
    ("M09-tee-bo-flush-CA-HAI-print", "t157",
     'print(f"{tien_to} {d.decode(\'utf-8\', \'replace\').rstrip(chr(13))}", flush=True)',
     'print(f"{tien_to} {d.decode(\'utf-8\', \'replace\').rstrip(chr(13))}")'),
    ("M10-ngan-sach-chi-cap-lai-khi-CAN", "t156",
     """        con_lai = het - time.monotonic()
        if con_lai <= 0:
            raise HetNganSachDay(i, len(ket), ngan_sach_giay)
        ket.append(chay(lenh, capture_output=True, text=True, timeout=con_lai))""",
     """        con_lai = het - time.monotonic()
        if con_lai <= 0:
            con_lai = 1.0
        ket.append(chay(lenh, capture_output=True, text=True, timeout=con_lai))"""),
    ("M11-nhanh-can-tra-ket-do-dang", "t156",
     """        if con_lai <= 0:
            raise HetNganSachDay(i, len(ket), ngan_sach_giay)""",
     """        if con_lai <= 0:
            return ket"""),
    ("M13-killpg-khong-chot-truong-nhom", "t154",
     "        if nhom_con is not None and nhom_con == p.pid and nhom_con != nhom_minh:",
     "        if nhom_con is not None:"),
    # ── VONG 6: thiet ke moi — moi lech la CHUA RO NGUYEN NHAN va phai CHAN o CONSUMER
    ("M15-classifier-tra-KHOP-khi-lech", "t160",
     "    return (LECH_CHUA_RO,",
     "    return (LECH_KHOP,"),
    ("M16-consumer-bo-classifier-gan-KHOP", "t160",
     "    ket_luan, thong_diep = _phan_loai_lech_ab(khong_actor, co_actor)",
     "    ket_luan, thong_diep = LECH_KHOP, 'DOT BIEN: bo classifier'"),
    ("M17-consumer-nhan-ca-trang-thai-CHUA-RO", "t160",
     "    bang(ket_luan == LECH_KHOP, thong_diep)",
     "    bang(ket_luan in (LECH_KHOP, LECH_CHUA_RO), thong_diep)"),
    ("M14-moi-truong-con-khong-TAT-DEM", "t158",
     '''    return dict(nen, PYTHONUNBUFFERED="1")''',
     '''    return dict(nen)'''),
    ("T137_TRAN-bo-chan-doan", "t156",
     '''T137_TRAN_GIAY = AL_HAN_GIAY + SC_HAN_TONG_GIAY + CD_HAN_TONG_GIAY       # 480''',
     '''T137_TRAN_GIAY = AL_HAN_GIAY + SC_HAN_TONG_GIAY  # DOT BIEN'''),
]

# =====================================================================================
# CONTROL cho CHINH bo do nay (F6). Bai hoc #355/#359 cua kho: "dot bien bi giet KHONG
# phai dot bien bi giet DUNG LY DO" — va mot thuoc do dung de chong bi lua thi cung bi
# lua duoc. Nen bo do phai chay bon ca ma ta BIET TRUOC dap an, TRUOC khi ai duoc tin
# mot con so no in ra. Moi control la mot DOT BIEN THAT, di qua DUNG duong ma catalog
# dung — khong phai mot phep thu regex tren chuoi bia.
#
# Chay: python3 dotbien512.py <goc-kho> --tu-kiem
# =====================================================================================
NEO_T160 = (
    '    from unittest import mock\n'
    '    a = (0, "2", "2", frozenset(), frozenset())'
)

CONTROL = [
    # (ten, dich, cu, moi, ket_qua_MONG_DOI)
    #
    # Ba ca AM: ca dich chet vi mot ngoai le VO CAN, khong vi chot cua no. Ca thu nhat la
    # the hien reviewer vong 6 khai; ca thu hai la the hien THU HAI, do lai 12-09-2026 va
    # vong 6 KHONG khai — cung mot lo goc (tien to bat buoc), hai duong vao.
    ("CTRL-ngoai-le-Exception-TRAN", "t160", NEO_T160,
     '    from unittest import mock\n'
     '    raise Exception("CONTROL vo can, khong lien quan A/B")\n'
     '    a = (0, "2", "2", frozenset(), frozenset())',
     "TIN DUNG GIA"),
    ("CTRL-ngoai-le-Error-TRAN", "t160", NEO_T160,
     '    from unittest import mock\n'
     '    class Error(Exception): pass\n'
     '    raise Error("CONTROL vo can, ten lop dung bang Error")\n'
     '    a = (0, "2", "2", frozenset(), frozenset())',
     "TIN DUNG GIA"),
    ("CTRL-ngoai-le-RuntimeError", "t160", NEO_T160,
     '    from unittest import mock\n'
     '    raise RuntimeError("CONTROL vo can, co tien to")\n'
     '    a = (0, "2", "2", frozenset(), frozenset())',
     "TIN DUNG GIA"),
    # Ca DUONG. Thieu no thi ban va "cho moi thu la TIN DUNG GIA" cung qua duoc ba ca tren,
    # tuc bo do se KHONG BAO GIO cap tin dung cho ai — mot chot luon DO cung la chot hong.
    ("CTRL-chet-DUNG-chot-ca-dich", "t160",
     "    return (LECH_CHUA_RO,", "    return (LECH_KHOP,",
     "GIET THAT"),
]


def cay_moi(uniq):
    """Cay TOI THIEU ngoai kho: ops/<phu thuoc> + .github/workflows."""
    d = Path(tempfile.mkdtemp(prefix=f"mut512-{uniq}-"))
    (d / "ops").mkdir()
    for t in ("lease_publish.py", "cai_actionlint.sh", "chay_lease_publish_test.sh"):
        if (GOC / "ops" / t).exists():
            shutil.copy2(GOC / "ops" / t, d / "ops" / t)
    shutil.copytree(GOC / ".github", d / ".github")
    # t154 (sau HINT) NAP `.claude/dev/launcher.py` va doc nguyen van fixture t63/t66 tu
    # `launcher_test.py` — thieu chung thi mutant chet vi FileNotFound, tuc TIN DUNG GIA.
    (d / ".claude" / "dev").mkdir(parents=True)
    for t in ("launcher.py", "launcher_test.py"):
        shutil.copy2(GOC / ".claude" / "dev" / t, d / ".claude" / "dev" / t)
    return d

TU_KIEM = "--tu-kiem" in sys.argv[1:]
DANH_SACH = [c[:4] for c in CONTROL] if TU_KIEM else MUTANT

bang = []
for i, (ten, dich, cu, moi) in enumerate(DANH_SACH, 1):
    if NGUON.count(cu) != 1:
        bang.append((ten, dich, "CHAN", f"mau khop {NGUON.count(cu)} lan, phai 1"))
        continue
    uniq = f"{i}-{int(time.time()*1000)%1000000}"
    d = cay_moi(uniq)
    tep = d / "ops" / "lease_publish_test.py"
    tep.write_text(NGUON.replace(cu, moi, 1), encoding="utf-8")
    mt = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    mt["PYTHONDONTWRITEBYTECODE"] = "1"
    r = subprocess.run([sys.executable, "-B", str(tep), f"--chi-ca={dich}"],
                       capture_output=True, text=True, env=mt, timeout=600)
    ra = r.stdout + r.stderr
    dong_do = [x for x in ra.splitlines() if x.startswith("  ĐỎ  ")]
    ten_do = [x.split(":")[0].replace("ĐỎ", "").strip() for x in dong_do]
    dung_ca = any(x.startswith(dich) for x in ten_do)
    # TIN DUNG GIA: mutant chet vi mot NGOAI LE VO CAN, khong vi chot cua ca dich. main() in ngoai le
    # khong mong doi thanh `<Kieu>Error: ...` / `<Kieu>Exception: ...` sau ten ca.
    chi_tiet_do = dong_do[0].split(":", 1)[1].strip() if dong_do else ""
    # F6 (cross-review vong 6; do lai 12-09-2026 ra THEM mot the hien vong 6 KHONG khai).
    # Ban cu doi IT NHAT MOT ky tu truoc `Error|Exception`, nen ca hai dang TRAN deu LOT va
    # mot ngoai le VO CAN duoc cap `GIET THAT`. Do thuc nghiem, khong doc code:
    #   "Exception: CONTROL unrelated to A/B" -> KHONG khop (lot)  <- the hien reviewer khai
    #   "Error: bare"                         -> KHONG khop (lot)  <- the hien THU HAI
    #   "RuntimeError: seam" / "ValueError: x" -> khop (loai dung)
    # Chuyen tien to thanh TUY CHON dong ca hai duong. Huong sai con lai la FAIL-CLOSE: mot
    # thong diep chot THAT vo tinh bat dau bang `<Tu>Error:` bi xep TIN DUNG GIA, tuc lam
    # catalog DO chu khong cap tin dung khong. `CONTROL` ngay tren la phan chung cho ca hai chieu.
    vo_can = re.match(r"^(?:[A-Za-z_][A-Za-z0-9_.]*)?(?:Error|Exception)\s*:", chi_tiet_do) is not None
    if r.returncode != 0 and dung_ca and len(ten_do) == 1 and not vo_can:
        bang.append((ten, dich, "GIET THAT", f"rc={r.returncode}, chot ca dich: {chi_tiet_do[:60]}"))
    elif r.returncode != 0 and dung_ca and vo_can:
        bang.append((ten, dich, "TIN DUNG GIA", f"chet vi ngoai le VO CAN: {chi_tiet_do[:80]}"))
    elif r.returncode != 0:
        bang.append((ten, dich, "TIN DUNG GIA", f"rc={r.returncode} nhung ĐỎ={ten_do} — khong phai ca dich"))
    else:
        bang.append((ten, dich, "SONG SOT", f"rc=0; out={ra[-200:]!r}"))
    shutil.rmtree(d, ignore_errors=True)

print(f"{'dot bien':38} {'dich':6} {'ket':14} chi tiet")
for a, b, c, e in bang:
    print(f"{a:38} {b:6} {c:14} {e}")

if TU_KIEM:
    # Tu kiem: khong dem "giet", DOI TUNG ca ra DUNG cai da biet truoc. Mot bo do khai
    # 4/4 ma phan hang sai mot ca thi con so 4 ay vo nghia.
    lech = [(a, mong, c) for (a, b, c, e), mong in zip(bang, [x[4] for x in CONTROL]) if c != mong]
    print()
    for (a, b, c, e), mong in zip(bang, [x[4] for x in CONTROL]):
        print(f"  {'DAT ' if c == mong else 'LECH'}  {a:34} mong_doi={mong:14} thuc_te={c}")
    print(f"\nTU KIEM: {len(bang) - len(lech)}/{len(bang)} ca dung phan hang"
          + ("" if not lech else f" — LECH: {lech}"))
    sys.exit(0 if not lech else 1)

giet = sum(1 for x in bang if x[2] == "GIET THAT")
print(f"\nTONG: giet that {giet}/{len(bang)} — tin dung gia {sum(1 for x in bang if x[2]=='TIN DUNG GIA')}, "
      f"song sot {sum(1 for x in bang if x[2]=='SONG SOT')}, chan {sum(1 for x in bang if x[2]=='CHAN')}")
sys.exit(0 if giet == len(bang) else 1)
