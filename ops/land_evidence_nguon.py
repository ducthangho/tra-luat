#!/usr/bin/env python3
"""Cổng NGUỒN cho lời khai trong `ops/land/*-land-evidence.yaml` — packet #773, đặc tả đóng băng
`ops/specs/land-evidence-khai-phai-co-nguon-r1.md` (sha256 063ccaa6…).

VÌ SAO CÓ. Ba lượt Codex connector trên PR ghi sổ #771 bắt cùng MỘT lỗi — lời khai rộng hơn bằng chứng giữ lại (H1) —
mỗi lượt vá tay đúng câu được chỉ; không cổng nào đo lớp lỗi này (`bien_nhan_v2` chỉ đọc `ops/reviews/*.receipt.yaml`).

LUẬT:
  L1  Mỗi LỜI KHAI ĐO — chuỗi YAML (khoá hoặc giá trị, mọi độ sâu) mà sau khi bỏ khoảng trắng đầu bắt đầu bằng token
      `measured` theo sau là khoảng trắng, `—`, `-` hoặc `:` — phải chứa ≥ 1 TOKEN NGUỒN phân giải được tới đường dẫn
      CÓ THẬT, NẰM TRONG gốc kho. Token nguồn = một dải tối đa `[A-Za-z0-9_./{}*-]+` (bỏ dấu `.` cuối câu) kết thúc
      bằng `.json|.txt|.log|.yaml|.yml|.md|.sh|.py|.patch` hoặc bằng `/` (khi ấy phải là thư mục). Thứ tự phân giải:
      `<hồ sơ>-provenance/`, `ops/land/`, gốc kho. Có `*` ⇒ glob, phải khớp ≥ 1 mục đúng LOẠI. Chặt hơn chữ đặc tả (Q3):
      so `measured` không phân biệt hoa thường; token trỏ CHÍNH hồ sơ không tính là nguồn.
  L2  Mapping có khoá `positive` phải có `nguon_positive` (chuỗi/danh sách) cùng cấp; mỗi tệp phải có; mọi token `N/M`
      và `hong N` của `positive` phải có NGUYÊN VĂN (biên chữ số) trong ≥ 1 tệp ấy.
  L3  Có `pre_merge_checks` và provenance có `readback-pr-*.json` mang `merged_at` ⇒ mọi mốc ISO-8601 đầy đủ trong
      một phần tử `pre_merge_checks` phải `<` `merged_at`. Không có readback ⇒ ghi "L3 không áp dụng", không ĐẠT ngầm.
  L4  Ba trạng thái: ĐẠT · ĐỎ · KHÔNG ĐO ĐƯỢC. YAML hỏng, provenance vắng khi có lời khai đo/`positive`, đọc tệp lỗi,
      readback hỏng, KHOÁ YAML TRÙNG (parser giữ giá trị cuối ⇒ lời khai trước biến mất), ngày sai, nhiều `merged_at`
      khác nhau, không thấy hồ sơ nào ⇒ KHÔNG ĐO ĐƯỢC, không bao giờ ĐẠT. Băm L5 và luật đo trên CÙNG một lần đọc.
  L5  `MIEN_TRU_CUTOVER` = {tên: sha256 byte} của MỌI hồ sơ trên `origin/master` lúc bắt đầu (`c73af7b`). Băm khớp ⇒
      bỏ qua có ghi nhận. Băm lệch ⇒ mất miễn trừ, kiểm đủ luật. Bản kỳ vọng CHÉP RIÊNG trong test: thêm tên ⇒ ĐỎ.

ĐIỀU CỔNG NÀY KHÔNG LÀM (đặc tả `ngoai_pham_vi`): L1 chỉ đo "lời khai trỏ tới thứ CÓ THẬT", KHÔNG đo thứ ấy chứng minh câu
văn — một tệp vô can vẫn làm L1 qua. Chỉ L2 đọc NỘI DUNG, và chỉ cho token số. Hồ sơ cũ đi qua miễn trừ, không được kiểm.
Không sửa hồ sơ nào. Chưa nằm trên đường CI tự động — việc của lease g2 (`ci.yml`).

Dùng: python ops/land_evidence_nguon.py [--root GOC] [--tep TEP ...] — thoát 0 ĐẠT · 1 ĐỎ · 2 KHÔNG ĐO ĐƯỢC (không vi phạm).
"""
import argparse
import datetime
import glob
import hashlib
import json
import re
import sys
from pathlib import Path

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

ROOT = Path(__file__).resolve().parents[1]
THU_MUC = "ops/land"
DUOI = "-land-evidence.yaml"

# L5 — đo 2026-10-16 trên `c73af7b`: mọi `ops/land/*-land-evidence.yaml`, sha256 trên byte blob. KHÔNG thêm tên mới.
MIEN_TRU_CUTOVER = {
    "plat-x8-land-evidence.yaml": "fe780adb6e9d897fa50011e0f91a0f1a995c72367280b6c9ab89a40485e6adaf",
    "pr468-hoso-4-packet-land-evidence.yaml": "6633416d86d4bcda1ac5cb9af30aa74a6c355ac6a2095901d91483d83ae19f40",
    "pr477-dung-goi-review-land-evidence.yaml": "3877dc4f2c611377cd80ce5cbe72645f26c6f10dec706a000d7e7da8e7f30bd5",
    "pr478-land-evidence.yaml": "c400cbdbbab9b92f3df2686dc94473cffcd5af9bc1d35953920cad69706d4657",
    "pr480-land-evidence.yaml": "e6d331048396712532f94d214fed0c9225e7fd733e5c5d7178eedace84d2450c",
    "pr487-land-evidence.yaml": "4b8fe2b5f713c20d2eefcb8ae8286ab8891c086a6cb3daf2206f09cc8d3560b8",
    "pr489-land-evidence.yaml": "ff4dad3ae70466c3bbe9ad6644f4d3989558d7839bf7902828caf42d58df99fb",
    "pr491-r358-ghi-so-land-evidence.yaml": "6a53de6f28322454ac084d8817799b9c5f54468aa4b47cf8820350dd805300dd",
    "pr493-land-evidence.yaml": "ea25588d524aba2b6b68f47887b18581adff4734345a2be46760703e9f5af391",
    "pr554-wp541-land-evidence.yaml": "07ea6c44b6245778c5dc34020352e75e8017835ff4c44e215715f4f80dea179c",
    "pr594-wp578-land-evidence.yaml": "858ce838bcaa705d370fa6767e2de36f7533098737d292cbf171e702c8184229",
    "pr621-skill-bai-hoc-land-evidence.yaml": "cb72c1daf84cebf02883f11cd43c7201eaedb3d454a51a90b8bd7359caaeaaa7",
    "pr666-wp650-land-evidence.yaml": "dea62efed34d55689752cfaea6ef2a5cc0b1af71e424be540c6bac82260173db",
    "pr672-wp574-land-evidence.yaml": "543ea45f2859144685ab5b35ad369dab9ccb103a39256a638ea1726c25dbb3ee",
    "pr679-wp678-land-evidence.yaml": "f409cacf8c5e3a6930072041ee8102db4327cb2558cdebd3263356057ef1b3be",
    "pr680-wp676-land-evidence.yaml": "964742fef636a70587b2247c094ac4f38aea540a01abdce8b6319c8f74b447bf",
    "pr684-wp677-land-evidence.yaml": "5b302984cefa5b245397d1facb77a06b9bfcac3cce38295d3f721abc32e7e220",
    "pr689-wp677-land-evidence.yaml": "f9bac5cbaeb8ac5bdf9f2d9b1375917e1d57c687ad6ed943c014a52996664559",
    "pr696-wp668-land-evidence.yaml": "aae2c2dc4ab1641400d8841ad40f11dac854131b80acdf407e52c9539b0afcb0",
    "pr701-wp687-land-evidence.yaml": "3e4004eefc05230aa3228bb88877eae7541d387a560b480c9b54f7aea2132a62",
    "pr703-wp674-land-evidence.yaml": "7266f6256651fe09d60382519d1d4c378c895ab15924e66fa055012d76f2cc18",
    "pr707-wp705-land-evidence.yaml": "d2425c2e4bf0ea930f9d1752ee20ee18a53a0e37315216af46986679141b99e8",
    "pr714-wp710-land-evidence.yaml": "906da0d8fb58ac01a25115dbafa6f4b98c57917c0931b23be0e41f38374f390a",
    "pr718-wp678-land-evidence.yaml": "1e181abab1432fade105b5ef3427d263ccb5f52217bc53c0251770f1a1ddb180",
    "pr721-wp698-land-evidence.yaml": "37bb04390e3cd65d6f489a8e390d8398eca9f1b6e7f565501f44af11a67641c6",
    "pr732-wp685-land-evidence.yaml": "41e806fe12064159e8f407ae81cc6eac1cb04c4bffd7dae6bb1b59c4d915e16a",
    "pr759-no-p3-ho-so-land-evidence.yaml": "574f6c3f13b4a36254fe0894539a66dc407c660ca4949ac80270bc9e442b7aa2",
    "pr765-wp743-land-evidence.yaml": "a468d5fea4dac206024e35567287006eb8b6befe9f1b96ad07f810e64c61c970",
}

RE_KHAI_DO = re.compile(r"\s*measured(?:\s|—|-|:)", re.IGNORECASE)
_KT = r"A-Za-z0-9_./{}*-"
RE_DAI = re.compile(rf"(?<![{_KT}])[{_KT}]+")
RE_DUOI_NGUON = re.compile(r"\.(?:json|txt|log|yaml|yml|md|sh|py|patch)$")
RE_SO_POS = re.compile(r"(?<!\d)\d+/\d+(?!\d)|(?<![A-Za-z0-9_])hong \d+(?!\d)")
RE_MOC = re.compile(r"\d{4}-\d{2}-\d{2}T\d{2}:\d{2}(?::\d{2}(?:\.\d+)?)?Z")


class KhongDoDuoc(Exception):
    """Đầu vào không đo được (L4). Không bao giờ quy thành ĐẠT."""


def token_nguon(chuoi):
    """Mọi token nguồn (Q3) trong một chuỗi, theo thứ tự xuất hiện."""
    ung = (m.group(0).rstrip(".") for m in RE_DAI.finditer(chuoi))
    return [t for t in ung if t and (t.endswith("/") or RE_DUOI_NGUON.search(t))]


def _trong_goc(p, goc):
    try:
        p.resolve().relative_to(goc.resolve())
        return True
    except (ValueError, OSError):
        return False


def phan_giai(token, goc, prov):
    """Đường dẫn CÓ THẬT (trong gốc) cho token, hoặc None. Thứ tự: provenance, ops/land, gốc."""
    for nen in (prov, goc / THU_MUC, goc):
        if "*" in token:
            khop = [Path(x) for x in sorted(glob.glob(glob.escape(str(nen)) + "/" + token))]
            khop = [x for x in khop if _trong_goc(x, goc) and (x.is_dir() if token.endswith("/") else x.is_file())]
            if khop:
                return khop[0]
            continue
        p = nen / token
        if (p.is_dir() if token.endswith("/") else p.is_file()) and _trong_goc(p, goc):
            return p
    return None


def duyet(nut, duong="$"):
    """(đường dẫn YAML, nút) cho MỌI nút — dict, list, lá; khoá cũng được trả như một lá `<khoa>`. Kiểu khác mà SafeLoader
    dựng được (`!!set` ⇒ set, `!!omap`/`!!pairs` ⇒ tuple, `!!binary` ⇒ bytes) ⇒ KhongDoDuoc: L2/L3 chỉ hiểu dict, nên
    đi xuống chúng cho L1 vẫn để hai luật kia mù — từ chối là đóng cả ba luật một chỗ (review lượt 2 F05)."""
    if isinstance(nut, (set, frozenset, tuple, bytes, bytearray)):
        raise KhongDoDuoc(f"{duong}: kiểu YAML {type(nut).__name__} ngoài mô hình dict/list/vô hướng")
    yield duong, nut
    con = nut.items() if isinstance(nut, dict) else enumerate(nut) if isinstance(nut, list) else ()
    for k, v in con:
        d = f"{duong}.{k}" if isinstance(nut, dict) else f"{duong}[{k}]"
        if isinstance(nut, dict):
            yield d + "<khoa>", k
        yield from duyet(v, d)


def _thoi_diem(x):
    if isinstance(x, datetime.datetime):
        return x if x.tzinfo else x.replace(tzinfo=datetime.timezone.utc)
    try:
        return datetime.datetime.fromisoformat(x.replace("Z", "+00:00"))
    except ValueError as e:   # regex chỉ kiểm HÌNH (2026-99-16 lọt) — ngày sai là đầu vào không đo được, không phải ĐỎ
        raise KhongDoDuoc(f"mốc {x!r} sai: {e}")


def merged_at(prov, goc_ten):
    """merged_at của PR mà hồ sơ ghi sổ. Hồ sơ tên `pr<N>-…` ⇒ CHỈ `readback-pr-<N>.json` (thư mục còn chứa readback PR lân
    cận và `-commits`, đo 16-10-2026). Tên khác ⇒ mọi `readback-pr-<số>.json` có `merged_at` khác null phải cùng một giá
    trị. None nếu không có readback áp dụng; KhongDoDuoc nếu hỏng, `merged_at` sai dạng, hoặc mâu thuẫn."""
    so = re.match(r"pr(\d+)-", goc_ten)
    tep = [] if not prov.is_dir() else [prov / f"readback-pr-{so.group(1)}.json"] if so else sorted(
        t for t in prov.glob("readback-pr-*.json") if re.fullmatch(r"readback-pr-\d+\.json", t.name))
    gia_tri = set()
    for t in tep:
        try:
            d = json.loads(t.read_text(encoding="utf-8")) if t.exists() else {}
        except (OSError, ValueError) as e:
            raise KhongDoDuoc(f"{t.name}: {type(e).__name__}: {e}")
        if (v := d.get("merged_at") if isinstance(d, dict) else None) is None and (not so or not t.exists()):
            continue
        if not isinstance(v, str) or not RE_MOC.fullmatch(v):
            raise KhongDoDuoc(f"{t.name}: không có merged_at ISO-8601 (được {v!r})")
        gia_tri.add(_thoi_diem(v))
    if len(gia_tri) > 1:
        raise KhongDoDuoc(f"readback-pr-*.json cho {len(gia_tri)} merged_at khác nhau")
    return gia_tri.pop() if gia_tri else None


def nap_yaml(yaml, byte):
    """`safe_load` có chốt, MỘT lần parse. Ở tầng NÚT, trước khi dựng, từ chối thứ làm dữ liệu dựng ra khác văn bản đọc được:
    khoá merge `<<` (làm phẳng đi vòng kiểm trùng — review lượt 3) và anchor/alias (nút dùng lại: vòng, nổ kích thước).
    Không hồ sơ nào trên master dùng chúng (đo 16-10-2026). Còn lại, khoá TRÙNG trong một mapping ⇒ lỗi (kể cả `null`)."""
    class Nap(yaml.SafeLoader):
        pass

    def map_khong_trung(nap, nut, deep=False):
        da = set()
        for k, _ in nut.value:
            khoa = nap.construct_object(k, deep=True)
            try:
                if khoa in da:
                    raise yaml.constructor.ConstructorError(None, None, f"khoá trùng {khoa!r}", k.start_mark)
                da.add(khoa)
            except TypeError:
                pass
        return yaml.SafeLoader.construct_mapping(nap, nut, deep)
    Nap.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, map_khong_trung)
    nap = Nap(byte)
    try:
        goc = nap.get_single_node()
        da, ngan = set(), [goc] if goc is not None else []
        while ngan:
            n = ngan.pop()
            if id(n) in da:
                raise yaml.YAMLError("anchor/alias (nút dùng lại) ngoài mô hình")
            da.add(id(n))
            if isinstance(n, yaml.MappingNode) and any(k.tag == "tag:yaml.org,2002:merge" for k, _ in n.value):
                raise yaml.YAMLError("khoá merge `<<` ngoài mô hình")
            ngan += [x for kv in n.value for x in kv] if isinstance(n, yaml.MappingNode) else \
                n.value if isinstance(n, yaml.SequenceNode) else []
        return nap.construct_document(goc) if goc is not None else None
    finally:
        nap.dispose()


def kiem_ho_so(tep, byte, goc, yaml):
    """(vi_pham, ghi_chu) trên `byte` — CHÍNH bản đã băm cho L5, không đọc tệp lần hai. Ném KhongDoDuoc cho L4."""
    try:
        du_lieu = nap_yaml(yaml, byte)
    except (yaml.YAMLError, ValueError, TypeError, OverflowError, RecursionError) as e:   # ngày sai không nháy: ValueError
        raise KhongDoDuoc(f"parse YAML: {type(e).__name__}: {str(e).splitlines()[0] if str(e) else ''}")
    goc_ten = tep.name[: -len(DUOI)] if tep.name.endswith(DUOI) else tep.stem
    prov = tep.parent / f"{goc_ten}-provenance"
    nut = list(duyet(du_lieu))   # độ sâu: loader ném RecursionError (~500 tầng) TRƯỚC bộ duyệt — đo 16-10-2026
    khai = [(d, v) for d, v in nut if isinstance(v, str) and RE_KHAI_DO.match(v)]
    maps = [(d, v) for d, v in nut if isinstance(v, dict)]
    co_pos = any("positive" in m for _, m in maps)
    if (khai or co_pos) and not prov.is_dir():
        raise KhongDoDuoc(f"thiếu thư mục provenance {prov.name}/ trong khi có {len(khai)} lời khai đo"
                          f"{' và khoá positive' if co_pos else ''}")
    vp, ghi = [], []
    for d, v in khai:   # L1
        tk = token_nguon(v)
        thay = [p for p in (phan_giai(t, goc, prov) for t in tk) if p and p.resolve() != tep.resolve()]   # tự trỏ ≠ nguồn
        if not thay:
            vp.append(f"L1 {d}: lời khai đo không có token nguồn phân giải được"
                      f" (token: {', '.join(tk) if tk else 'không có'}) — {v.strip()[:90]!r}")
    for d, m in maps:   # L2
        if "positive" not in m:
            continue
        ng = m.get("nguon_positive")
        ds = [ng] if isinstance(ng, str) else ng if isinstance(ng, list) else None
        if not ds or not all(isinstance(x, str) and x for x in ds):
            vp.append(f"L2 {d}: có positive mà thiếu nguon_positive (chuỗi/danh sách)")
            continue
        tep_ng = [(x, phan_giai(x, goc, prov)) for x in ds]
        vp += [f"L2 {d}: nguon_positive {x!r} không có tệp" for x, p in tep_ng if p is None or not p.is_file()]
        if any(p is None or not p.is_file() for _, p in tep_ng):
            continue
        try:
            noi_dung = [p.read_bytes().decode("utf-8", "replace") for _, p in tep_ng]
        except OSError as e:
            raise KhongDoDuoc(f"đọc nguon_positive: {e}")
        for so in RE_SO_POS.findall(str(m["positive"])):
            mau = re.compile(r"(?<![A-Za-z0-9_])" + re.escape(so) + r"(?!\d)" if so.startswith("hong")
                             else r"(?<![\d/])" + re.escape(so) + r"(?![\d/])")
            if not any(mau.search(nd) for nd in noi_dung):
                vp.append(f"L2 {d}: positive khai {so!r} mà không tệp nguon_positive nào chứa nguyên văn")
    pmc = du_lieu.get("pre_merge_checks") if isinstance(du_lieu, dict) else None
    if pmc is not None:   # L3
        moc_merge = merged_at(prov, goc_ten)
        if moc_merge is None:
            ghi.append("L3 không áp dụng: provenance không có readback PR mang merged_at")
        else:
            phan_tu = pmc if isinstance(pmc, list) else [{k: v} for k, v in pmc.items()] if isinstance(pmc, dict) else [pmc]
            for i, pt in enumerate(phan_tu):
                for d, v in duyet(pt, f"$.pre_merge_checks[{i}]"):
                    moc = [v] if isinstance(v, datetime.datetime) else RE_MOC.findall(v) if isinstance(v, str) else []
                    for x in moc:
                        if _thoi_diem(x) >= moc_merge:
                            vp.append(f"L3 {d}: mốc {x} không trước merged_at {moc_merge:%Y-%m-%dT%H:%M:%SZ}")
    return vp, ghi


def main(argv=None):
    ap = argparse.ArgumentParser(description="Cổng nguồn cho lời khai trong ops/land/*-land-evidence.yaml (#773).")
    ap.add_argument("--root", default=str(ROOT))
    ap.add_argument("--tep", nargs="+", default=None, help="chỉ kiểm các tệp này (tương đối với --root hoặc tuyệt đối)")
    a = ap.parse_args(argv)
    goc = Path(a.root).resolve()   # MỘT hệ quy chiếu: `--root .` + `--tep /tuyệt/đối` từng ném ValueError (review lượt 4 F06)
    try:
        import yaml
    except ImportError as e:
        print(f"KHÔNG ĐO ĐƯỢC: thiếu PyYAML ({e})\nTỔNG: KHÔNG ĐO ĐƯỢC")
        return 2
    teps = [goc / t for t in a.tep] if a.tep else sorted((goc / THU_MUC).glob("*" + DUOI))
    n = m = k = v = u = 0
    for tep in teps:
        nhan = tep.resolve().relative_to(goc).as_posix() if _trong_goc(tep, goc) else str(tep)
        try:
            byte = tep.read_bytes()
        except OSError as e:
            u += 1
            print(f"KHÔNG ĐO ĐƯỢC {nhan}: {type(e).__name__}: {e}")
            continue
        if (bam := MIEN_TRU_CUTOVER.get(tep.name)) is not None:
            k += 1
            if hashlib.sha256(byte).hexdigest() == bam:
                m += 1
                print(f"MIỄN TRỪ {nhan} (băm khớp ảnh chụp cutover)")
                continue
            print(f"MẤT MIỄN TRỪ {nhan}: băm lệch ảnh chụp cutover — kiểm đủ luật")
        try:
            vp, ghi = kiem_ho_so(tep, byte, goc, yaml)
        except KhongDoDuoc as e:
            u += 1
            print(f"KHÔNG ĐO ĐƯỢC {nhan}: {e}")
            continue
        for g in ghi:
            print(f"  ghi chú {nhan}: {g}")
        v, n = v + len(vp), n + (not vp)
        print(f"ĐỎ {nhan}: {len(vp)} vi phạm" + "".join(f"\n  {x}" for x in vp) if vp else f"ĐẠT {nhan}")
    if not teps:
        u += 1
        print(f"KHÔNG ĐO ĐƯỢC: không thấy hồ sơ *{DUOI} nào dưới {goc / THU_MUC}")
    print(f"land_evidence_nguon: {n} ĐẠT · {m}/{k} miễn trừ (băm khớp) · {v} vi phạm · {u} KHÔNG ĐO ĐƯỢC · tổng {len(teps)}")
    rc = 1 if v else 2 if u else 0
    print("TỔNG: " + ("ĐẠT", "ĐỎ", "KHÔNG ĐO ĐƯỢC")[rc])
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
