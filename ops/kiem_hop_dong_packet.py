#!/usr/bin/env python3
"""Canh HAI HANG SO bi CHEP o nhieu cho giua dac ta va lease.

VI SAO CO TEP NAY. Cung mot hinh dang loi da xuat hien BON lan trong packet #463:
  · r14  tran 300 -> 400: muc `review_class` cua dac ta van ghi 300;
  · r15  vua don xong thi lease `viec_trong_lease` van ghi 300 (ly_do_thu_hoi ghi 400);
  · r17  tran 400 -> 430: hai dong o muc `review_class` van ghi 400 (tu phat hien);
  · r17  VA lease `viec_trong_lease`/`dieu_kien_dung` van ghi 400 (cross-review luot 4
         `R4-F01` bat) — DUNG HAI DONG da phai sua o r14, hong lai lan thu hai.
Kem `R4-F02`: tieu de dac ta ghi `revision 17` con truong `revision` ghi `15`.

`PROTOCOL §12`: cung hinh dang lan thu BA thi sua CACH LAM. Vá con so lan thu nam la
tiep tuc dung cach lam da hong bon lan. Cach lam moi: **hang so nam DUNG MOT CHO, va
may canh dieu do** — con nguoi khong doc ra duoc mot con so VANG MAT o dung cho.

Ba chot, moi chot mot ma thoat rieng de biet cai nao do:
  2  revision lech giua tieu de dac ta / truong `revision` cua dac ta / `revision` lease
  3  dac ta neu tran KHONG DUNG MOT lan
  4  lease NEU LAI mot hang so ba chu so trong khoi nghia vu (phai TRO toi A8, khong chep)
  5  `spec_hash` cua lease khong khop sha256 cua dac ta
  6  khong doc duoc tep / thieu truong  (KHONG DO DUOC — fail-close, khong phai DAT)
"""
import argparse, hashlib, pathlib, re, sys

# CHOT 3 do dung mot thu: mot MUC nghia vu vien den tieu chi `A<n>` cua dac ta thi KHONG
# duoc chep NGUONG cua tieu chi ay vao — no phai TRO toi dac ta da ghim bang `spec_hash`.
# Phan biet NGUONG voi THAM CHIEU: so hieu Issue, `run_id`, so PR, nam deu la tham chieu
# va nam trong nhung muc KHONG vien tieu chi nao, nen khong bi bat.
#
# KHE CON LAI, KHAI THANG — day van la mot danh sach CAM tren tu vung neo (`A<n>`), nen
# mot muc dien dat nghia vu A8 ma khong viet chu "A8" se LOT. No chi thu hep khe chu
# khong dong. Phan DONG duoc theo cau truc la chot 2 (dac ta neu tran DUNG MOT lan):
# co dung mot nguon thi khong con ban sao nao de troi.
KHOI_NGHIA_VU = ("viec_trong_lease", "dieu_kien_dung")
# `R6-F04`: bo rieng `dieu_kien_dung` khoi tap tren van cho bo test 10/10 — moi PHAN TU cua
# tap nay cung la mot cua. Ky vong NEO DOC LAP; chot 5 doi hai ben bang nhau.
KHOI_NGHIA_VU_KY_VONG = ("viec_trong_lease", "dieu_kien_dung")
NEO_TIEU_CHI = re.compile(r"\b(A[1-9]|M[1-9]|additions|dòng thêm)\b")
# Nguong: so >= 3 chu so, hoac thap phan kieu Viet (`36,00`, `0,60`).
# Bien phai chan GIUA MOT SO PHIEN BAN (`0.15.15`) chu KHONG chan dau cham CAU
# (`... ≤ 400.`). Ban dau dung `(?![\w.])` nen `400.` khong khop va ca t4 DO —
# phan chung bat duoc, va phep dot bien "noi danh sach cho phep" khi ay bao DAT
# GIA vi ca nen von da hong. Hai ca canh nhau moi lo ra.
NGUONG = re.compile(r"(?<![\w.])(\d{3,}|\d+,\d+)(?!\.?\d)(?!\w)")
# DANH SACH CHO PHEP cho THAM CHIEU (khong phai danh sach cam cho nguong): mot con so di
# sau mot trong nhung dau hieu nay la MOT DINH DANH, khong phai mot nguong — so hieu Issue,
# `run_id`, so PR, ngay thang. Moi so con lai trong mot muc vien tieu chi la nguong bi chep.
THAM_CHIEU = re.compile(
    r"(?:#|comment\s+|run\s+|PR\s*#?\s*|issue\s*#?\s*|\d{2}-\d{2}-"
    r"|[A-Za-z]{2,}-)(\d{3,})", re.I)   # `[A-Za-z]{2,}-` cho `ADR-0044`, `PLAT-...`


def _khoi_yaml(van, ten):
    """Cat mot khoi YAML muc cao nhat theo ten, khong can parser: tu `ten:` toi khoa ke."""
    m = re.search(rf"(?m)^{re.escape(ten)}:\s*$", van)
    if m is None:
        return None
    con_lai = van[m.end():]
    ke = re.search(r"(?m)^[A-Za-z_][A-Za-z0-9_]*:", con_lai)
    return con_lai[:ke.start()] if ke else con_lai


def kiem(spec: pathlib.Path, lease: pathlib.Path, nghiem_ngat: bool = False):
    """Tra (danh sach loi, danh sach chot BO QUA vi khong ap dung).

    `nghiem_ngat` bien moi chot BO QUA thanh CHAN [7] — dung cho packet buoc phai khai
    du hop dong. Mac dinh KHONG nghiem ngat, vi mot chot khong ap dung ma bao do la
    bao dong gia, va bao dong gia lam nguoi ta thoi doc cong.
    """
    loi, bo_qua = [], []
    try:
        sv = spec.read_text(encoding="utf-8")
        lv = lease.read_text(encoding="utf-8")
    except OSError as e:
        return [(6, f"khong doc duoc: {e}")], []

    # ── chot 1: revision o BA cho phai bang nhau ────────────────────────────────
    tieu_de = re.search(r"^#.*\(revision\s+(\d+)\)", sv, re.M)
    truong = re.search(r"^-\s*`revision`:\s*\*\*(\d+)\*\*", sv, re.M)
    l_rev = re.search(r"(?m)^revision:\s*(\d+)\s*$", lv)
    # KHONG AP DUNG khac VI PHAM. Do 12-09-2026 tren 59 cap lease/spec that cua kho:
    # ban dau chot nay tra CHAN cho 58 cap, va con so ay la MOT LOI CUA BO CANH chu khong
    # phai no cua kho — cac dac ta khac khong dung dinh dang `(revision N)` o tieu de va
    # khong co truong `- \`revision\`: **N**`. Suyt bao mot nen bia. Nen: khong co CA HAI
    # dau hieu => dac ta hinh dang khac, bo qua chot nay; co DUNG MOT => nghi ngo, CHAN.
    if not tieu_de and not truong:
        bo_qua.append("revision (dac ta khong khai revision o tieu de lan o truong)")
    elif not (tieu_de and truong and l_rev):
        loi.append((6, f"khai revision KHONG DAY DU: tieu de={bool(tieu_de)} "
                       f"truong={bool(truong)} lease={bool(l_rev)}"))
    else:
        bo = {"tieu de dac ta": tieu_de.group(1), "truong `revision` dac ta": truong.group(1),
              "`revision` lease": l_rev.group(1)}
        if len(set(bo.values())) != 1:
            loi.append((2, "revision LECH: " + " · ".join(f"{k}={v}" for k, v in bo.items())))

    # ── chot 2: dac ta neu tran DUNG MOT lan ────────────────────────────────────
    tran = re.findall(r"`additions`\s*≤\s*\*\*(\d+)\*\*", sv)
    if len(tran) == 0:
        bo_qua.append("tran A8 (dac ta khong neu tran dong nao)")
    elif len(tran) > 1:
        loi.append((3, f"dac ta neu tran {len(tran)} lan (phai dung 1): {tran}"))

    # ── chot 3: lease KHONG duoc chep hang so vao khoi nghia vu ─────────────────
    for ten in KHOI_NGHIA_VU:
        khoi = _khoi_yaml(lv, ten)
        if khoi is None:
            # Lease hinh dang khac (ten truong khac) — KHONG AP DUNG, khong phai vi pham.
            bo_qua.append(f"khoi `{ten}` (lease khong co truong nay)"); continue
        # Cat theo TUNG MUC danh sach YAML: mot muc vien tieu chi ma mang nguong => CHAN.
        for muc in re.split(r"(?m)^\s*-\s", khoi):
            if not NEO_TIEU_CHI.search(muc):
                continue
            # `R6-F03` — tru THAM CHIEU theo VI TRI, khong theo GIA TRI. Ban truoc lam
            # `set(NGUONG) - set(THAM_CHIEU)` nen mot muc ghi `Issue #400 ... ≤ 400` duoc THA:
            # tham chieu `#400` hop thuc hoa luon con so 400 dung sau `≤`. Nay xet tung LAN
            # XUAT HIEN theo span. (Ten `la_tham_chieu` cung tranh trung `bo_qua` cua ham —
            # va cham ten ay tung lam `--nghiem-ngat` bao mot `run_id` la "chot bi bo qua".)
            nhip_tc = {m.span(1) for m in THAM_CHIEU.finditer(muc)}
            so = sorted({m.group(1) for m in NGUONG.finditer(muc)
                         if m.span(1) not in nhip_tc})
            if so:
                nhan = NEO_TIEU_CHI.search(muc).group(1)
                loi.append((4, f"lease `{ten}` muc vien `{nhan}` CHEP nguong {so} — phai TRO "
                               f"toi dac ta da ghim bang `spec_hash`, khong chep so"))

    # ── chot 5: tap khoi nghia vu khop ky vong neo doc lap (`R6-F04`) ───────────
    if tuple(KHOI_NGHIA_VU) != tuple(KHOI_NGHIA_VU_KY_VONG):
        loi.append((4, f"KHOI_NGHIA_VU {tuple(KHOI_NGHIA_VU)} lech ky vong "
                       f"{tuple(KHOI_NGHIA_VU_KY_VONG)}"))

    # ── chot 4: spec_hash tro dung byte dac ta ──────────────────────────────────
    h = re.search(r"(?m)^spec_hash:\s*([0-9a-f]{64})\s*$", lv)
    if h is None:
        loi.append((6, "lease thieu `spec_hash` 64 ky tu"))
    else:
        that = hashlib.sha256(spec.read_bytes()).hexdigest()
        if h.group(1) != that:
            loi.append((5, f"spec_hash lease {h.group(1)[:12]}… != sha256 dac ta {that[:12]}…"))
    if nghiem_ngat:
        loi += [(7, f"NGHIEM NGAT: chot bi bo qua — {b}") for b in bo_qua]
        bo_qua = []
    return loi, bo_qua


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--spec", required=True, type=pathlib.Path)
    ap.add_argument("--lease", required=True, type=pathlib.Path)
    ap.add_argument("--nghiem-ngat", action="store_true",
                    help="chot KHONG AP DUNG cung thanh CHAN [7]")
    a = ap.parse_args(argv)
    loi, bo_qua = kiem(a.spec, a.lease, a.nghiem_ngat)
    for b in bo_qua:
        print(f"BO QUA: {b}")
    for ma, mo in loi:
        print(f"CHAN [{ma}]: {mo}")
    if not loi:
        print(f"DAT: {a.spec.name} + {a.lease.name} — "
              f"{len(bo_qua)} chot bo qua, phan con lai khop")
        # `R6-F08` — khai GIOI HAN ngay tren duong DAT, vi day la cho nguoi doc ket luan.
        print("GIOI HAN: chot 2 dem DUNG MOT mau Markdown; mot nghia vu tran viet khac cach "
              "(vd \"Cot additions khong duoc vuot 400 dong.\") KHONG duoc dem. Day la kiem "
              "DINH DANG, KHONG phai bang chung 'dac ta chi co mot nghia vu tran'.")
        return 0
    return max(ma for ma, _ in loi)


if __name__ == "__main__":
    sys.exit(main())
