#!/usr/bin/env python3
"""Phản chứng cho `doc_receipt_thu_hoi.py` (C1a1a, #650; spec r5 §5) và nhóm Git `doc_receipt_thu_hoi_git.py` (C1a1b, #1179).

Fixture dương = receipt thật PR #589 (artifact `10842182657`, `receipt.json` sha256 `ca67dc6a…`), chép tay, KHÔNG đọc artifact.
Mỗi ca âm là MỘT biến đổi của fixture; oracle là CẢ vectơ năm luật (luật cùng đỏ tất yếu thì khai, K1 đỏ kéo K2–K5 theo M1).
Bảng nghĩa vụ A0 = `DB` + `_theo_truong()`: mỗi dòng một ID mệnh đề M1–M6/M8, một đột biến chạy trên BẢN SAO TẠM, và ca
đích. Disposition tính TỪ KẾT QUẢ CHẠY: `witness_killed` khi ca đích ném `TinHieuChotCa` mang ĐÚNG TÊN nó (mã triển khai
không ném được lớp này), fixture dương vẫn xanh, và ngoại lệ trần (nếu có) đúng loại khai ở cột cuối; `equivalent_verified`
khi dòng khai `TD:` kèm lập luận và CẢ bộ ca vẫn xanh trên đột biến; còn lại `unresolved` (chặn merge).
"""
import ast
import hashlib
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import traceback
import zlib

GOC = pathlib.Path(__file__).resolve().parent
MODUN = GOC / "doc_receipt_thu_hoi.py"
S, H, X40, X64 = "601a0f18c83057fa079d204122660f5697fc6389", "af6b54cd5a67f4a2c3ff4cb3f11e32c22b26b6e6", "0123456789abcdef" * 2 + "01234567", "ab" * 32
KHO, WFR = "ducthangho/tra-luat", "ducthangho/tra-luat/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/master"
C3, OID = ("checkout_commit", "bo_kiem_da_chay_commit", "workflow_definition_commit"), "5e811ebbf89c0d439776dd8fbaff694a4dce6650"
FIX = {"S": S, "H": H, "T": "cd365f76377581707d8ee32b9af0f283e088eae7", "tree_S": "8480b690b7b52c7fb25885e46443e26f3c6dd698",
       **dict.fromkeys(C3, S), "oid_bo_kiem_da_chay": OID, "oid_bo_kiem_tai_S": OID,
       "workflow_definition_blob": "277df262ff3f7bc6bc0be839be6419f6db441f5a",
       "workflow_definition_sha256": "e1d1785915a6e3fa4f633f7588c5022d3466d41db69d1b692867404926e49b79",
       "schema_version": 1, "canh_ancestry": 4, "so_object_da_doc": 11, "tong_bytes": 15572, "pull_request": 589,
       "run_id": 36081907282, "run_attempt": 1, "check_run_id": 107905495884, "job_id": 107905495884, "checker_rc": 0,
       "event": "thu_hoi_admission_receipt", "che_do": "chua_kich_hoat", "ket_luan": "TAP_THU_HOI_RONG",
       "repository": KHO, "kho_canonical": "github.com/" + KHO, "nhanh_mac_dinh": "master", "workflow_ref": WFR,
       "thoi_diem_utc": "2026-09-25T01:25:14Z", "descriptor_q13_ghim": None, "policy_T": None, "profile_digest": None,
       "discovery": "KHONG_CHAY: A0 chưa kích hoạt; PROFILE_ADAPTER_DA_DUYET rỗng (quyết định chủ kho)",
       "so_thu_hoi_S": {}, "so_thu_hoi_T": {}, "metadata_T": [], "thu_hoi_moi": [],
       "ngan_sach": {"max_alternate_depth": 4, "max_alternate_stores": 8, "max_object_bytes": 8388608,
                     "max_parent_path_edges": 10000, "max_reader_wall_seconds": 60.0, "max_total_object_bytes": 134217728,
                     "max_tree_or_alias_edges": 128, "max_unique_objects": 50000}}
# Trường -> giá trị sai miền, VIẾT Ở ĐÂY, độc lập với `KIEU` của module (A6). C3 ở ngoài: quan hệ đồng nhất che (A7).
SAI = {**{k: FIX[k].upper() for k in ("S", "H", "T", "oid_bo_kiem_da_chay", "workflow_definition_blob", "oid_bo_kiem_tai_S",
                                      "workflow_definition_sha256")},
       "tree_S": FIX["tree_S"] + "0", "thoi_diem_utc": "2026-09-25 01:25:14Z", "descriptor_q13_ghim": "ab", "policy_T": [],
       "profile_digest": 5, "discovery": None, "so_thu_hoi_S": [], "so_thu_hoi_T": [], "ngan_sach": [], "metadata_T": {},
       "thu_hoi_moi": {}, **dict.fromkeys(("schema_version", "canh_ancestry", "so_object_da_doc", "tong_bytes",
                                           "pull_request", "run_id", "run_attempt", "check_run_id", "job_id"), True),
       "checker_rc": False}
CUNG_DO = {"S": ("K2", "K4"), "H": ("K2", "K4"), "schema_version": ("K1",)}  # K1 chặn schema_version trước K2


class TinHieuChotCa(AssertionError):
    """Chỉ khung ca sinh; mã triển khai không ném được lớp này."""


class LoiDo(RuntimeError):
    """Phép đo tự hỏng: làm suite ĐỎ, không bao giờ được tính là giết đột biến."""


def doi(**kv):
    return lambda d: {**d, **kv}


def ma(d):
    return json.dumps(d, ensure_ascii=False, indent=1).encode()


def kiem_kq(ten, kq, do):
    """Oracle DÙNG CHUNG cho API và CLI (luot2 F17): dict đúng 3 khoá, `ok` bool, `luat` đúng vectơ, `ly_do` list[str];
    K1 đỏ ⇒ mỗi K2–K5 có ĐÚNG lý do "Kx: K1 do" (luot2 F22), không chỉ có tiền tố."""
    muon = {k: "do" if k in do or "K1" in do else "qua" for k in ("K1", "K2", "K3", "K4", "K5")}
    ly = kq.get("ly_do") if type(kq) is dict else None
    if (type(kq) is not dict or set(kq) != {"ok", "luat", "ly_do"} or kq["luat"] != muon or type(kq["ok"]) is not bool
            or kq["ok"] != (not do) or type(ly) is not list or any(type(x) is not str for x in ly) or bool(ly) != bool(do)
            or ("K1" in do and not all(f"{k}: K1 do" in ly for k in ("K2", "K3", "K4", "K5")))):
        raise TinHieuChotCa(f"{ten}: {kq} != {muon}")


def ca(m, ten, dau_vao, do=(), **tham):
    raw = dau_vao if isinstance(dau_vao, bytes) else ma(dau_vao(FIX))
    try:
        kq = m.kiem_json(raw, **{"kho": KHO, "nhanh": "master", "base_hien_hanh": S, "head_hien_hanh": H, **tham})
    except Exception as e:  # M1: không được ném với MỌI bytes. Ghi LOẠI + SỐ DÒNG ném trong module (luot2 F15)
        so, gd, tb = [f.lineno for f in traceback.extract_tb(e.__traceback__) if f.filename == m.__file__], "?", e.__traceback__
        while tb is not None:  # GIAI ĐOẠN = số luật đã ghi trong frame kiem_json lúc ném (luot3 F25: đúng dòng mà sai giai đoạn)
            if tb.tb_frame.f_code.co_filename == m.__file__ and type(tb.tb_frame.f_locals.get("luat")) is dict:
                gd = len(tb.tb_frame.f_locals["luat"])
            tb = tb.tb_next
        raise TinHieuChotCa(f"{ten}: NEM:{type(e).__name__}@{so[-1] if so else '?'}#{gd}") from None
    kiem_kq(ten, kq, do)
    if "K4" in do and "K1" not in do:  # nghĩa lý do K4: ĐÚNG trường lệch, ĐÚNG "stale, chay lai" (luot3 F30 K4-THONG-BAO-STALE)
        r, t = json.loads(raw), {"S": S, "H": H, **{k: tham[v] for k, v in (("S", "base_hien_hanh"), ("H", "head_hien_hanh")) if v in tham}}
        k4 = [re.fullmatch(r"K4\s*:\s*([SH])\s*:?\s*(?:receipt )?stale, ch(?:ay|ạy) l(?:ai|ại)", x.lstrip()) for x in kq["ly_do"] if re.match(r"\s*K4\b", x)]
        if not all(k4) or sorted(x[1] for x in k4) != sorted(k for k in ("S", "H") if r[k] != t[k]):  # luot5 F35, luot6 F39/F40, luot7 F41
            raise TinHieuChotCa(f"{ten}: ly do K4 sai nghia: {kq['ly_do']}")


WFK, WFN = WFR.replace(KHO, "other/repo"), WFR[:-6] + "main"
LIM, _E = 4300, "PYTHONINTMAXSTRDIGITS"  # F23: bytes dựng tay vì json.dumps/int() cũng vướng giới hạn; _ghim() GHIM nó


def _SO(n):
    return ma(FIX).replace(b'"run_id": 36081907282', b'"run_id": ' + b"1" * n)


# F19: danh mục CÓ HỆ THỐNG cho regex giờ — mỗi token × {ít, nhiều, sai lớp} (nhóm số) hoặc {ký tự khác} (hằng).
TOK = [(r"\d{4}", "2026"), ("-", "-"), (r"\d\d", "09"), ("-", "-"), (r"\d\d", "25"), ("T", "T"), (r"\d\d", "01"), (":", ":"),
       (r"\d\d", "25"), (":", ":"), (r"\d\d", "14"), ("Z", "Z")]
KHAC = {"-": "/", "T": " ", ":": "-", "Z": "X"}
GIO = []
for i, (mau, gt) in enumerate(TOK):
    n = len(gt)
    for op, m_moi, g_moi in ([("it", rf"\d{{{n - 1},{n}}}", gt[:-1]), ("nhieu", rf"\d{{{n},{n + 1}}}", gt + "0"), ("lop", "." * n, "a" * n)]
                             if mau.startswith("\\d") else [("khac", f"(?:{mau}|{KHAC[mau]})", KHAC[mau])]):
        GIO.append((f"gio_{i}_{op}", "".join(m_moi if j == i else t for j, (t, _) in enumerate(TOK)),
                    "".join(g_moi if j == i else g for j, (_, g) in enumerate(TOK))))
assert "".join(t for t, _ in TOK) == r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ" and "".join(g for _, g in TOK) == FIX["thoi_diem_utc"]
CA = [("duong_fixture", lambda d: d, ()), ("duong_c_khac_s", doi(**dict.fromkeys(C3, X40)), ()),
      ("duong_oid_tai_s_null", doi(oid_bo_kiem_tai_S=None), ()), ("duong_descriptor_hex64", doi(descriptor_q13_ghim=X64), ()),
      ("duong_policy_dict", doi(policy_T={}), ()), ("duong_profile_str", doi(profile_digest="x"), ()),
      ("bom", b"\xef\xbb\xbf" + ma(FIX), ("K1",)), ("khong_phai_json", b"{", ("K1",)), ("goc_null", b"null", ("K1",)),
      ("goc_list_38_khoa", json.dumps(sorted(FIX)).encode(), ("K1",)),
      ("byte_0x80", ma(FIX).replace(b"KHONG_CHAY", b"KHONG\x80CHAY"), ("K1",)), ("thua_khoa", doi(la=1), ("K1",)),
      ("schema_true", doi(schema_version=True), ("K1",)), ("schema_2", doi(schema_version=2), ("K1",)),
      ("event_v2", doi(event="thu_hoi_admission_receipt_v2"), ("K1",)), ("job_id_null", doi(job_id=None), ("K2",)),
      ("c_ca_nhom_39", doi(**dict.fromkeys(C3, S[:39])), ("K2",)), ("gio_hau_to", doi(thoi_diem_utc="2026-09-25T01:25:14Zx"), ("K2",)),
      ("duong_doi_chung", doi(descriptor_q13_ghim=X64, policy_T={}, profile_digest="x"), ()),  # A1 cho nhóm null (luot2 F16)
      ("int_chuoi", doi(run_id="5"), ("K2",)), ("so_dai_gioi_han", _SO(LIM), ()), ("so_dai_vuot", _SO(LIM + 1), ("K1",) if LIM else ()),
      ("long_sau", b"[" * 100000 + b"]" * 100000, ("K1",)),  # 1000 tầng KHÔNG ném trên 3.12/3.13 (CI gate-registry 36367726882); 1e5 ném trên 3.10–3.13
      ("k3_ca_nhom_kho", doi(repository="other/repo", kho_canonical="github.com/other/repo", workflow_ref=WFK), ("K3",)),
      ("k3_ca_nhom_nhanh", doi(nhanh_mac_dinh="main", workflow_ref=WFN), ("K3",)),
      ("k4_base", lambda d: d, ("K4",), {"base_hien_hanh": X40}), ("k4_head", lambda d: d, ("K4",), {"head_hien_hanh": X40}),
      ("k4_ca_hai", lambda d: d, ("K4",), {"base_hien_hanh": X40, "head_hien_hanh": X40}),  # oracle K4 hai trường, không ghim thứ tự
      ("k5_rc", doi(checker_rc=1), ("K5",)), ("k5_ket_luan", doi(ket_luan="TAP_THU_HOI_KHAC"), ("K5",)),
      ("k5_che_do", doi(che_do="da_kich_hoat"), ("K5",)), ("k5_ket_luan_list", doi(ket_luan=[]), ("K5",)),
      ("k5_ket_luan_dict", doi(ket_luan={}), ("K5",)), ("k5_ket_luan_null", doi(ket_luan=None), ("K5",)),
      ("k5_ket_luan_so", doi(ket_luan=1), ("K5",)), ("hex40_ngoai_af", doi(T="g" * 40), ("K2",)),
      ("hex64_ngoai_af", doi(workflow_definition_sha256="g" * 64), ("K2",)), ("hex64_63", doi(workflow_definition_sha256="a" * 63), ("K2",)),
      ("hex64_65", doi(workflow_definition_sha256="a" * 65), ("K2",)), ("hex_la_so", doi(T=int("1" * 40)), ("K2",)),
      ("hex64_la_so", doi(workflow_definition_sha256=int("1" * 64)), ("K2",)), ("descriptor_la_so", doi(descriptor_q13_ghim=int("1" * 64)), ("K2",)),
      ("int_float", doi(run_id=1.5), ("K2",)), ("gio_unicode_so", doi(thoi_diem_utc="\u0662026-09-25T01:25:14Z"), ()),
      ("duong_kho_khac", doi(repository="other/repo", kho_canonical="github.com/other/repo", workflow_ref=WFK), (), {"kho": "other/repo"}),
      ("duong_nhanh_khac", doi(nhanh_mac_dinh="main", workflow_ref=WFN), (), {"nhanh": "main"}), ("a11_k3_k4", doi(repository="other/repo"), ("K3", "K4"), {"base_hien_hanh": X40})]
# ASCII (ensure_ascii) để bytes UTF-16/32 vẫn là UTF-8 hợp lệ: ca phải tới PARSER, không bị decode chặn trước (M2c)
CA += [(f"utf{n}", json.dumps(FIX).encode(f"utf-{n}"), ("K1",)) for n in ("16-le", "16-be", "32-le", "32-be")]
CA += [(f"thieu_{k}", lambda d, k=k: {x: v for x, v in d.items() if x != k}, ("K1",)) for k in FIX]
CA += [(f"kieu_{k}", doi(**{k: v}), CUNG_DO.get(k, ("K2",))) for k, v in SAI.items()]
CA += [(f"c_le_{k}", doi(**{k: X40}), ("K2",)) for k in C3]
CA += [(ten, doi(thoi_diem_utc=gio), ("K2",)) for ten, _, gio in GIO]
CA += [(f"k3_{n}", doi(**{k: v}), ("K3",)) for n, k, v in (
    ("repository", "repository", "other/repo"), ("kho_canonical", "kho_canonical", "github.com/other/repo"),
    ("wf_kho", "workflow_ref", WFK), ("nhanh", "nhanh_mac_dinh", "main"), ("wf_nhanh", "workflow_ref", WFN),
    ("host", "kho_canonical", "evil.example/" + KHO), ("wf_tags", "workflow_ref", WFR.replace("heads", "tags")),
    ("wf_duong", "workflow_ref", WFR.replace("ops-thu-hoi-admission", "untrusted")))]


CLI_CA = [("xanh", ma(FIX), (), {}), ("k1_bom", b"\xef\xbb\xbf" + ma(FIX), ("K1",), {}), ("k1_so_dai", _SO(LIM + 1), ("K1",), {}),
          ("k2_T", ma({**FIX, "T": "g" * 40}), ("K2",), {}), ("k3_repo", ma({**FIX, "repository": "other/repo"}), ("K3",), {}),
          ("k4_head", ma(FIX), ("K4",), {"--head-hien-hanh": X40}), ("k5_ket_luan", ma({**FIX, "ket_luan": []}), ("K5",), {})]


def _cli(path, raw, tham):
    with tempfile.TemporaryDirectory() as t:
        p = pathlib.Path(t) / "r.json"
        p.write_bytes(raw)
        a = {"--receipt": str(p), "--kho": KHO, "--nhanh-mac-dinh": "master", "--base-hien-hanh": S, "--head-hien-hanh": H, **tham}
        return subprocess.run([sys.executable, "-B", str(path), "kiem-json", *[x for kv in a.items() if kv[1] is not None for x in kv]],
                              capture_output=True, text=True, timeout=60)


def ca_cli(ten, path, m):
    for tham in (("--receipt", "/khong/co/tep.json"), ("--base-hien-hanh", S[:39]), ("--head-hien-hanh", H[:39]), ("--kho", ""),
                 ("--nhanh-mac-dinh", ""), ("--base-hien-hanh", ""), ("--head-hien-hanh", ""), ("--base-hien-hanh", S.upper()), ("--kho", None)):
        r = _cli(path, ma(FIX), dict([tham]))
        if r.returncode != 2:  # rc đọc thẳng từ subprocess.run, không qua pipe (A12)
            raise TinHieuChotCa(f"{ten}: {tham} rc={r.returncode} != 2")
    for nhan, raw, do, tham in CLI_CA:  # mỗi luật đỏ một ca: CLI phải giữ NGUYÊN kết quả đỏ, không chỉ nhánh xanh (luot2 F18)
        r = _cli(path, raw, tham)
        if r.returncode != (12 if do else 0) or len(r.stdout.splitlines()) != 1:
            raise TinHieuChotCa(f"{ten}:{nhan}: rc={r.returncode} stdout={r.stdout!r}")
        kq = json.loads(r.stdout)
        kiem_kq(f"{ten}:{nhan}", kq, do)  # kiểu `ok` ở biên JSON của CLI (luot2 F17), rồi mới so giá trị
        if kq != m.kiem_json(raw, kho=KHO, nhanh="master", base_hien_hanh=S, head_hien_hanh=tham.get("--head-hien-hanh", H)):
            raise TinHieuChotCa(f"{ten}:{nhan}: CLI khac kiem_json")


def ca_thu_tu(ten, m):
    """M2(a)(b)(c): chốt BOM TRƯỚC giải mã, giải mã MỘT lần, parser nhận CHÍNH chuỗi đã giải mã (luot1 F9)."""
    for dau, duoi, muon in ((b"", b"", ["slice", "decode", "parse"]), (b"\xef\xbb\xbf", b"", ["slice"]),
                            (b" \t", b"\n", ["slice", "decode", "parse"])):  # whitespace: .strip() tạo str KHÁC (luot2 F21)
        ev, giai = [], []

        class Raw(bytes):
            def __getitem__(self, k):
                ev.append("slice")
                return bytes.__getitem__(self, k)

            def decode(self, *a, **kw):
                ev.append("decode")
                giai.append(bytes.decode(self, *a, **kw))
                return giai[-1]
        goc = m.json.loads
        m.json.loads = lambda v, *a, **kw: (ev.append("parse" if giai and v is giai[-1] else f"parse:{type(v).__name__}"), goc(v, *a, **kw))[1]
        try:
            ca(m, ten, Raw(dau + ma(FIX) + duoi), ("K1",) if dau.startswith(b"\xef") else ())
        finally:
            m.json.loads = goc
        if ev != muon:
            raise TinHieuChotCa(f"{ten}: thu tu {ev} != {muon}")


_CON_TINH = r"""
import importlib.util, json, sys
sp = importlib.util.spec_from_file_location("m_tinh", sys.argv[1])
m = importlib.util.module_from_spec(sp)
sp.loader.exec_module(m)
dang, ev = [False], []
sys.addaudithook(lambda e, a: ev.append(e) if dang[0] and e.split(".")[0] in ("open", "os", "subprocess", "socket", "shutil", "urllib", "http", "ctypes") else None)
anh = lambda: ({k: repr(v) for k, v in vars(sys).items() if k != "modules"}, sorted(sys.modules), {k: repr(v) for k, v in vars(m).items() if k != "__builtins__"})
tham, raws = dict(kho=sys.argv[2], nhanh="master", base_hien_hanh=sys.argv[3], head_hien_hanh=sys.argv[4]), [open(p, "rb").read() for p in sys.argv[5:]]
truoc = anh()
dang[0] = True
kq = [m.kiem_json(r, **tham) for r in raws + raws]
dang[0] = False
print(json.dumps({"ev": ev, "trang_thai": anh() == truoc, "tat_dinh": kq[:len(raws)] == kq[len(raws):]}))
"""


def ca_tinh(ten, m):
    """M1: module thuần (import chỉ trong tập cho phép) và docstring khai đúng giới hạn (không quyền land/provenance)."""
    cay = ast.parse(pathlib.Path(m.__file__).read_text(encoding="utf-8"))
    ten_import = {a.name.split(".")[0] for n in ast.walk(cay) if isinstance(n, (ast.Import, ast.ImportFrom))
                  for a in (n.names if isinstance(n, ast.Import) else [ast.alias(n.module or "")])}
    doc = ast.get_docstring(cay) or ""
    if ten_import - {"argparse", "json", "re", "sys"} or "KHÔNG phải quyền land" not in doc or "KHÔNG chứng minh provenance" not in doc:
        raise TinHieuChotCa(f"{ten}: import {sorted(ten_import)} hoac docstring thieu loi khai gioi han")
    with tempfile.TemporaryDirectory() as t:  # M1 hàm thuần, đo trong TIẾN TRÌNH CON cô lập bằng audit hook (luot3 F29)
        vao = [pathlib.Path(t) / f"r{i}.json" for i in range(2)]
        for p, raw in zip(vao, (ma(FIX), b"{")):
            p.write_bytes(raw)
        r = subprocess.run([sys.executable, "-B", "-c", _CON_TINH, m.__file__, KHO, S, H, *map(str, vao)],
                           capture_output=True, text=True, timeout=60)
    try:
        kq = json.loads(r.stdout.splitlines()[-1])
    except (IndexError, ValueError):
        kq = None
    if (r.returncode != 0 or type(kq) is not dict or set(kq) != {"ev", "trang_thai", "tat_dinh"} or type(kq["ev"]) is not list
            or any(type(e) is not str for e in kq["ev"]) or {type(kq["trang_thai"]), type(kq["tat_dinh"])} != {bool}):  # luot5 F36
        raise LoiDo(f"{ten}: probe tinh thuan hong rc={r.returncode}: {r.stderr[-200:]}")  # KHÔNG phải bằng chứng tác dụng phụ (luot4 F32)
    if kq != {"ev": [], "trang_thai": True, "tat_dinh": True}:
        raise TinHieuChotCa(f"{ten}: kiem_json co tac dung phu: {kq}")


MAU = r'^doc_receipt_thu_hoi tests: ([1-9]\d*)/(\1) ca QUA · ([1-9]\d*)/(\3) dot bien GIET$'


def ca_dang_ky(ten, mau=MAU):
    cdk = _nap(GOC / "ci_dang_ky_test.py", "ci_dang_ky_duoi_test")
    if cdk.MOI.get(".claude/dev/doc_receipt_thu_hoi_test.py") != MAU:
        raise TinHieuChotCa(f"{ten}: MOI khong dang ky dung MAU (M8)")
    for a, b, nhan in (("3/3", "2/2", True), ("3/4", "2/2", False), ("3/3", "1/2", False), ("3/4", "1/2", False),
                       ("0/0", "0/0", False), ("3/3", "0/0", False)):
        if bool(cdk.bang_chung_xanh(f"doc_receipt_thu_hoi tests: {a} ca QUA · {b} dot bien GIET", mau)) != nhan:
            raise TinHieuChotCa(f"{ten}: mau dang ky {a} · {b} phai {'nhan' if nhan else 'bac'}")


def _ghim(f):  # GHIM giới hạn cho helper + MỌI con (env thừa kế; -X thì không), HOÀN NGUYÊN cả có/vắng env (luot5 F34, luot6 F38)
    def boc(*a, **kw):
        cu = sys.get_int_max_str_digits(), os.environ.get(_E)
        sys.set_int_max_str_digits(LIM), os.environ.__setitem__(_E, str(LIM))
        try:
            return f(*a, **kw)
        finally:
            sys.set_int_max_str_digits(cu[0]), os.environ.pop(_E) if cu[1] is None else os.environ.__setitem__(_E, cu[1])
    return boc


ca, ca_cli, ca_tinh = map(_ghim, (ca, ca_cli, ca_tinh))


def chay_ca(m, path, chi=None, bo=()):
    for c in CA:
        if (chi is None and c[0] not in bo) or (chi is not None and c[0] in chi):
            ca(m, c[0], c[1], c[2], **(c[3] if len(c) > 3 else {}))
    for ten, f in (("thu_tu_k1", ca_thu_tu), ("tinh", ca_tinh)):
        if (chi is None and ten not in bo) or (chi is not None and ten in chi):
            f(ten, m)
    if chi is None or "cli" in chi:
        ca_cli("cli", path, m)
    if chi is None or "dang_ky" in chi:
        ca_dang_ky("dang_ky")


# (ID, mệnh đề, tên đột biến, chuỗi cũ, chuỗi mới, ca đích | "TD: lập luận", ngoại lệ trần (loại, DÒNG ném nguyên văn),
#  [ca gác A1 — mặc định "duong_fixture"; None = A1 KHÔNG ÁP DỤNG được, khai rõ | với TD: các ca loại khỏi phép đo])
_Q, _K4, _IN, _DAU = 'if r[k] != v])', '    ghi("K4"', '    print(json.dumps(kq, ', '    luat, ly_do = {}, []'
_CX = 'r["checkout_commit"] == ' + repr(X40)
_TRA = '    return {"ok": all(v == "qua" for v in luat.values()), "luat": luat, "ly_do": ly_do}'
_BAT = ('except UnicodeDecodeError:\n            loi.append("khong phai UTF-8 strict")\n        except json.JSONDecodeError:\n'
        '            loi.append("khong phai JSON")\n        except (ValueError, RecursionError):')
_TRA1 = '        return {"ok": False, "luat": luat, "ly_do": ly_do}'
DB = [
    ("M1a", "ok = mọi luật qua", "ok_any", 'all(v == "qua"', 'any(v == "qua"', "k4_base", None),
    ("M1b", "K1 đỏ ⇒ K2–K5 ghi do", "bo_k1_do_lan", '            ghi(k, ["K1 do"])', '            pass', "bom", None),
    ("M1c", "mọi luật được chạy", "dung_som", _K4, '    if luat["K3"] == "do":\n        return {"ok": False, "luat": luat, "ly_do": ly_do}\n' + _K4, "a11_k3_k4", None),
    ("M1d", "luật đỏ có ly_do", "bo_ly_do", 'ly_do.extend(f"{k}: {x}" for x in loi)', 'ly_do.extend([])', "k5_rc", None),
    ("M1e", "CLI rc 0 khi ok", "rc_ok_3", 'return 0 if', 'return 3 if', "cli", None),
    ("M1f", "CLI rc 12 khi có luật đỏ", "rc_do_1", 'else 12', 'else 1', "cli", None),
    ("M1g", "CLI rc 2 khi OSError", "oserror_rc1", '        return 2', '        return 1', "cli", None),
    ("M1h", "CLI --kho rỗng ⇒ 2", "rong_bo_kho", 'all((a.kho, ', 'all((', "cli", None),
    ("M1i", "CLI --nhanh-mac-dinh rỗng ⇒ 2", "rong_bo_nhanh", 'a.nhanh_mac_dinh, a.base', 'a.base', "cli", None),
    ("M1j", "CLI --base rỗng ⇒ 2", "rong_bo_base", ', a.base_hien_hanh, a.head_hien_hanh))', ', a.head_hien_hanh))',
     "TD: base rỗng không phải hex40 nên chốt hex bên dưới vẫn trả 2", None),
    ("M1k", "CLI --head rỗng ⇒ 2", "rong_bo_head", 'a.base_hien_hanh, a.head_hien_hanh))', 'a.base_hien_hanh))',
     "TD: head rỗng không phải hex40 nên chốt hex bên dưới vẫn trả 2", None),
    ("M1l", "CLI --base hex40 ⇒ 2", "hex_bo_base", '(_H40(a.base_hien_hanh) and ', '(', "cli", None),
    ("M1m", "CLI --head hex40 ⇒ 2", "hex_bo_head", ' and _H40(a.head_hien_hanh))', ')', "cli", None),
    ("M1n", "CLI in MỘT dòng JSON", "in_nhieu_dong", 'sort_keys=True)', 'sort_keys=True, indent=1)', "cli", None),
    # A2 dự kiến TD ở mức VERDICT (parser str tự bác U+FEFF); oracle thứ tự M2(a) "kiểm TRƯỚC giải mã" (luot1 F9)
    # phân biệt được nó, nên disposition CHẶT hơn A2: witness_killed. Verdict BOM vẫn đo bằng đột biến ghép M2a'.
    ("M2a", "BOM đỏ ở cấp VERDICT (A2)", "bo_chot_bom", 'if raw[:3] == BOM:', 'if False:',
     "TD: json.loads(str) tự bác U+FEFF đầu chuỗi; đo trên MỌI ca TRỪ oracle thứ tự (chủ kho: hai ID hai cấp, F24)", None, ("thu_tu_k1",)),
    ("M2a2", "BOM kiểm TRƯỚC giải mã (cấp THỨ TỰ, M2(a))", "bo_chot_bom_thu_tu", 'if raw[:3] == BOM:', 'if False:', "thu_tu_k1", None),
    ("M2a'", "BOM đỏ (đột biến ghép)", "bom_ghep", 'if raw[:3] == BOM:\n        loi.append("BOM UTF-8")\n    else:\n'
     '        try:\n            chuoi = raw.decode("utf-8", "strict")', 'if False:\n        pass\n    else:\n        try:\n'
     '            chuoi = raw.decode("utf-8", "strict").lstrip("\\ufeff")', "bom", None),
    ("M2b", "UTF-8 strict", "decode_replace", '"utf-8", "strict"', '"utf-8", "replace"', "byte_0x80", None),
    # except (ValueError, RecursionError) của F23 CHE hai chốt dưới (UnicodeDecodeError, JSONDecodeError ⊂ ValueError) ⇒ bỏ
    # riêng từng chốt là TD; răng đo bằng đột biến gỡ CẢ NHÓM chốt (spec §5.0: chốt che nhau thì đo nhóm chốt).
    ("M2b'", "UnicodeDecodeError ⇒ đỏ (chốt riêng)", "bo_try_decode", 'except UnicodeDecodeError:', 'except ZeroDivisionError:',
     "TD: except (ValueError, RecursionError) bắt trùm UnicodeDecodeError ⇒ vẫn K1 đỏ", None),
    ("M2b3", "UnicodeDecodeError ⇒ đỏ (cả nhóm chốt)", "bo_try_decode_nhom", _BAT, _BAT.replace("except UnicodeDecodeError:", "except ZeroDivisionError:")
     .replace("except (ValueError, RecursionError):", "except RecursionError:"), "byte_0x80", ("UnicodeDecodeError", 'chuoi = raw.decode("utf-8", "strict")', 0)),
    ("M2c", "json.loads nhận str", "loads_bytes", 'json.loads(chuoi)', 'json.loads(raw)', "utf16-le", None),
    ("M2c'", "JSONDecodeError ⇒ đỏ (chốt riêng)", "bo_try_json", 'except json.JSONDecodeError:', 'except ZeroDivisionError:',
     "TD: except (ValueError, RecursionError) bắt trùm JSONDecodeError ⇒ vẫn K1 đỏ", None),
    ("M2c3", "JSONDecodeError ⇒ đỏ (cả nhóm chốt)", "bo_try_json_nhom", _BAT, _BAT.replace("except json.JSONDecodeError:", "except ZeroDivisionError:")
     .replace("except (ValueError, RecursionError):", "except RecursionError:"), "khong_phai_json", ("JSONDecodeError", "r = json.loads(chuoi)", 0)),
    ("M2d", "gốc phải object", "bo_kiem_dict", 'type(r) is not dict:', 'False:', "goc_list_38_khoa", ("TypeError", 'elif not (type(r["schema_version"]) is int and r["schema_version"] == 1):', 0)),
    ("M2e", "tập khoá khít: thừa ⇒ đỏ", "khoa_superset", 'if set(r) != KHOA:', 'if not KHOA <= set(r):', "thua_khoa", None),
    ("M2e'", "tập khoá khít: thiếu ⇒ đỏ", "khoa_subset", 'if set(r) != KHOA:', 'if not set(r) <= KHOA:', "thieu_tree_S", ("KeyError", 'loi = [f"{k} sai kieu" for k in sorted(KIEU) if not KIEU[k](r[k])]', 1)),
    ("M2f", "schema_version int không bool", "schema_bo_kieu", 'type(r["schema_version"]) is int and ', '', "schema_true", None),
    ("M2f'", "schema_version == 1", "schema_bo_gia_tri", 'r["schema_version"] == 1)', 'True)', "schema_2", None),
    ("M2g", "event hằng", "bo_event", 'r["event"] != EVENT', 'False', "event_v2", None),
    ("M3a", "hex40 chỉ chữ thường", "hex_hoa", '_khop("[0-9a-f]{40}")', '_khop("[0-9a-fA-F]{40}")', "kieu_T", None),
    ("M3b", "khớp TRỌN chuỗi", "fullmatch_match", 're.fullmatch(mau, v)', 're.match(mau, v)', "kieu_tree_S", None),
    ("M3c", "int không nhận bool", "int_isinstance", 'lambda v: type(v) is int', 'lambda v: isinstance(v, int)', "kieu_job_id", None),
    ("M3d", "job_id không null", "job_id_null", '# 7 khoá', 'KIEU["job_id"] = lambda v: v is None or type(v) is int\n# 7 khoá', "job_id_null", None),
    ("M3e", "hex64 chỉ chữ thường", "hex64_hoa", '_khop("[0-9a-f]{64}")', '_khop("[0-9a-fA-F]{64}")', "kieu_workflow_definition_sha256", None),
    ("M3f6", "thoi_diem_utc theo \\d của spec (F11)", "gio_chi_ascii", r'r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ"',
     'r"[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z"', "gio_unicode_so", None),
    ("M3o", "hex40 chỉ chữ a–f", "hex40_a_z", '_khop("[0-9a-f]{40}")', '_khop("[0-9a-z]{40}")', "hex40_ngoai_af", None),
    ("M3p", "hex64 chỉ chữ a–f", "hex64_a_z", '_khop("[0-9a-f]{64}")', '_khop("[0-9a-z]{64}")', "hex64_ngoai_af", None),
    ("M3q", "hex64 không quá 64", "hex64_65", '{64}")', '{64,65}")', "hex64_65", None),
    ("M3r", "hex64 không thiếu", "hex64_63", '{64}")', '{63,64}")', "hex64_63", None),
    ("M3s", "hex40 không thiếu", "hex40_39", '{40}")', '{39,40}")', "c_ca_nhom_39", None),
    ("M3t", "hex40 không quá 40", "hex40_41", '{40}")', '{40,41}")', "kieu_tree_S", None),
    ("M3u", "hex phải là str (không ép số)", "hex_ep_str", 'type(v) is str and re.fullmatch(mau, v)', 're.fullmatch(mau, str(v))', "hex_la_so", None),
    ("M3v", "int không nhận float", "int_nhan_float", 'lambda v: type(v) is int for k', 'lambda v: type(v) in (int, float) for k', "int_float", None),
    ("M3w", "descriptor nhận null", "descriptor_cam_null", 'v is None or _H64(v)', '_H64(v)', "duong_fixture", None, "duong_doi_chung"),
    ("M3x", "policy_T nhận null", "policy_cam_null", 'v is None or type(v) is dict', 'type(v) is dict', "duong_fixture", None, "duong_doi_chung"),
    ("M3y", "profile_digest nhận null", "profile_cam_null", 'v is None or type(v) is str', 'type(v) is str', "duong_fixture", None, "duong_doi_chung"),
    ("M3g", "oid_bo_kiem_tai_S nhận null", "oid_null_cam", 'lambda v: v is None or _H40(v)', '_H40', "duong_oid_tai_s_null", None),
    ("M3h", "descriptor nhận hex64", "descriptor_chi_null", 'v is None or _H64(v)', 'v is None', "duong_descriptor_hex64", None),
    ("M3i", "policy_T nhận dict", "policy_chi_null", 'v is None or type(v) is dict', 'v is None', "duong_policy_dict", None),
    ("M3j", "profile_digest nhận str", "profile_chi_null", 'v is None or type(v) is str', 'v is None', "duong_profile_str", None),
    ("M3k", "C0 thuộc ràng buộc đồng nhất", "c_bo_0", 'r[C[0]] == r[C[1]] and ', '', "c_le_checkout_commit", None),
    ("M3l", "C2 thuộc ràng buộc đồng nhất", "c_bo_2", ' and r[C[1]] == r[C[2]]', '', "c_le_workflow_definition_commit", None),
    ("M3m", "C1 thuộc ràng buộc đồng nhất", "c_bo_1", 'r[C[0]] == r[C[1]] and r[C[1]] == r[C[2]]', 'r[C[0]] == r[C[2]]', "c_le_bo_kiem_da_chay_commit", None),
    ("M3n", "kiểu hex của CẢ NHÓM C", "c_bo_kieu_ca_nhom", '# 7 khoá', 'KIEU.update(dict.fromkeys(C, lambda v: True))\n# 7 khoá', "c_ca_nhom_39", None),
    ("M4a", "kho lấy từ THAM SỐ", "kho_tu_receipt", '    ghi("K3", [', '    kho = r["repository"]\n    ghi("K3", [', "k3_ca_nhom_kho", None),
    ("M4b", "nhánh lấy từ THAM SỐ", "nhanh_tu_receipt", '    ghi("K3", [', '    nhanh = r["nhanh_mac_dinh"]\n    ghi("K3", [', "k3_ca_nhom_nhanh", None),
    ("M4c", "so repository", "bo_repository", '("repository", kho), ', '', "k3_repository", None),
    ("M4d", "so kho_canonical", "bo_kho_canonical", '("kho_canonical", "github.com/" + kho),', '', "k3_kho_canonical", None),
    ("M4e", "so nhanh_mac_dinh", "bo_nhanh", '("nhanh_mac_dinh", nhanh), ', '', "k3_nhanh", None),
    ("M4f", "so workflow_ref", "bo_workflow_ref", ', ("workflow_ref", kho + WF + nhanh)', '', "k3_wf_kho", None),
    ("M4g", "hằng tiền tố github.com/", "host_hau_to", _Q, 'if r[k] != v and not (k == "kho_canonical" and r[k].endswith("/" + kho))])', "k3_host", None),
    ("M4h", "hằng đường workflow", "wf_duong_tu_do", _Q, 'if r[k] != v and not (k == "workflow_ref" and r[k].startswith(kho + "/") '
     'and r[k].endswith("@refs/heads/" + nhanh))])', "k3_wf_duong", None),
    ("M4i", "hằng loại ref @refs/heads/", "wf_nhan_tags", _Q, 'if r[k] not in (v, v.replace("@refs/heads/", "@refs/tags/"))])', "k3_wf_tags", None),
    ("M5a", "S == base", "bo_base", '("S", base_hien_hanh), ("H", head_hien_hanh)', '("H", head_hien_hanh),', "k4_base", None),
    ("M5b", "H == head", "bo_head", '("S", base_hien_hanh), ("H", head_hien_hanh)', '("S", base_hien_hanh),', "k4_head", None),
    ("M5c", "base lấy từ THAM SỐ", "base_tu_receipt", _K4, '    base_hien_hanh = r["S"]\n' + _K4, "k4_base", None),
    ("M5e", "lý do K4 nói stale (F30)", "k4_noi_fresh", 'stale, chay lai', 'fresh, khong can chay lai', "k4_base", None),
    ("M5f", "lý do K4 nêu ĐÚNG trường (F30)", "k4_sai_truong", '[f"{k} stale', '[f"S stale', "k4_head", None),
    ("M5g", "MỌI lý do nhãn K4 được kiểm, kể cả thụt đầu (F40/F41)", "k4_mau_thuan", _K4, '    ly_do += ["\\tK4:S fresh"] * (r["S"] != base_hien_hanh)\n' + _K4, "k4_base", None),
    ("M5d", "head lấy từ THAM SỐ", "head_tu_receipt", _K4, '    head_hien_hanh = r["H"]\n' + _K4, "k4_head", None),
    ("M6a", "checker_rc == 0", "bo_rc", 'r["checker_rc"] == 0)', 'True)', "k5_rc", None),
    ("M6b", "ket_luan thuộc tập đóng", "bo_ket_luan", 'r["ket_luan"] in KET_LUAN', 'True', "k5_ket_luan", None),
    ("M6c", "che_do hằng", "bo_che_do", 'r["che_do"] == CHE_DO', 'True', "k5_che_do", None),
    ("M6d", "ket_luan sai kiểu JSON ⇒ K5 do, không ném (F1)", "ket_luan_bam", 'KET_LUAN = ("TAP_THU_HOI_RONG",)',
     'KET_LUAN = frozenset({"TAP_THU_HOI_RONG"})', "k5_ket_luan_list", ("TypeError", 'ghi("K5", [f"{k} la" for k, dat in (("checker_rc", r["checker_rc"] == 0), ("ket_luan", r["ket_luan"] in KET_LUAN),', 4)),
    # --- danh mục hình dạng kết quả (M1): {ok, luat, ly_do, tập khoá} × {nhánh K1 đỏ, K2–K5 đỏ, xanh}; nhánh xanh chỉ kích
    # hoạt trên duong_c_khac_s để fixture THẬT vẫn gác A1 (luot3 F26: không miễn A1)
    ("M1o", "ok là bool — nhánh đỏ", "ok_do_int", _TRA, _TRA.replace('"ok": all(v == "qua" for v in luat.values())', '"ok": all(v == "qua" for v in luat.values()) or 0'), "k5_rc", None),
    ("M1o2", "ok là bool — nhánh xanh", "ok_xanh_int", _TRA, _TRA.replace('"ok": all(v == "qua" for v in luat.values())', '"ok": (1 if ' + _CX + ' else all(v == "qua" for v in luat.values()))'), "duong_c_khac_s", None),
    ("M1u", "luat là dict — nhánh đỏ K2–K5", "luat_do_list", _TRA, _TRA.replace('"luat": luat,', '"luat": luat if "do" not in luat.values() else list(luat.items()),'), "k5_rc", None),
    ("M1u2", "luat là dict — nhánh xanh", "luat_xanh_list", _TRA, _TRA.replace('"luat": luat,', '"luat": list(luat.items()) if ' + _CX + ' else luat,'), "duong_c_khac_s", None),
    ("M1o3", "ok là bool — nhánh K1 đỏ (F27)", "ok_k1_int", _TRA1, _TRA1.replace('"ok": False', '"ok": 0'), "bom", None),
    ("M1x3", "đúng 3 khoá — nhánh K1 đỏ (F27)", "khoa_thua_k1", _TRA1, _TRA1.replace('"ly_do": ly_do}', '"ly_do": ly_do, "x": 1}'), "bom", None),
    ("M1v", "luat là dict — nhánh K1 đỏ", "luat_k1_list", _TRA1, _TRA1.replace('"luat": luat', '"luat": list(luat.items())'), "bom", None),
    ("M1w", "ly_do là list — nhánh K1 đỏ", "ly_do_k1_tuple", _TRA1, _TRA1.replace('"ly_do": ly_do', '"ly_do": tuple(ly_do)'), "bom", None),
    ("M1w2", "ly_do là list — nhánh đỏ K2–K5", "ly_do_do_tuple", _TRA, _TRA.replace('"ly_do": ly_do}', '"ly_do": ly_do if not ly_do else tuple(ly_do)}'), "k5_rc", None),
    ("M1w3", "ly_do là list — nhánh xanh", "ly_do_xanh_tuple", _TRA, _TRA.replace('"ly_do": ly_do}', '"ly_do": tuple(ly_do) if ' + _CX + ' else ly_do}'), "duong_c_khac_s", None),
    ("M1x", "đúng 3 khoá — nhánh đỏ", "khoa_thua_do", _TRA, _TRA.replace('"ly_do": ly_do}', '"ly_do": ly_do, **({"x": 1} if ly_do else {})}'), "k5_rc", None),
    ("M1x2", "đúng 3 khoá — nhánh xanh", "khoa_thua_xanh", _TRA, _TRA.replace('"ly_do": ly_do}', '"ly_do": ly_do, **({"x": 1} if ' + _CX + ' else {})}'), "duong_c_khac_s", None),
    ("M1q2", "K1 đỏ ⇒ lý do ĐÚNG 'K1 do' (F22)", "k1_ly_do_sai_nghia", '            ghi(k, ["K1 do"])', '            ghi(k, ["K1 qua"])', "bom", None),
    ("M1y", "CLI giữ kiểu bool của ok (F17)", "cli_ok_int", _IN, '    kq["ok"] = int(kq["ok"])\n' + _IN, "cli", None),
    ("M2i", "parser nhận CHÍNH str đã decode (F21)", "strip_sau_decode", 'chuoi = raw.decode("utf-8", "strict")', 'chuoi = raw.decode("utf-8", "strict").strip()', "thu_tu_k1", None),
    ("M2j", "số nguyên quá dài ⇒ K1 đỏ, không ném (F23)", "bo_bat_value", 'except (ValueError, RecursionError):', 'except ZeroDivisionError:',
     "so_dai_vuot", ("ValueError", "r = json.loads(chuoi)", 0)),
    ("M2k", "lồng quá sâu ⇒ K1 đỏ, không ném", "bo_bat_recursion", 'except (ValueError, RecursionError):', 'except ValueError:',
     "long_sau", ("RecursionError", "r = json.loads(chuoi)", 0)),
    ("M3v2", "int không nhận chuỗi", "int_nhan_str", 'lambda v: type(v) is int for k', 'lambda v: type(v) in (int, str) for k', "int_chuoi", None),
    ("M1p", "ly_do là list[str] (F10)", "ly_do_so", '        ly_do.extend(f"{k}: {x}" for x in loi)',
     '        ly_do.extend(f"{k}: {x}" for x in loi)\n        ly_do[:] = [0 for _ in ly_do]', "k5_rc", None),
    ("M1q", "K1 đỏ ⇒ K2–K5 có lý do", "k1_lan_khong_ly_do", '            ghi(k, ["K1 do"])', '            luat[k] = "do"', "bom", None),
    ("M1r", "CLI in ĐÚNG dict của kiem_json (F8)", "cli_mat_dict", 'json.dumps(kq, ', 'json.dumps({"ok": kq["ok"]}, ', "cli", None),
    ("M1s", "module thuần: chỉ import argparse/json/re/sys", "them_subprocess", 'import argparse\n', 'import argparse\nimport subprocess\n', "tinh", None),
    ("M1t", "docstring khai ok không phải quyền land", "bo_loi_khai", 'KHÔNG phải quyền land', 'là quyền land', "tinh", None),
    ("M2h", "BOM trước decode, decode một lần (F9)", "decode_truoc_bom", '    loi, r = [], _VANG',
     '    try:\n        raw.decode("utf-8", "strict")\n    except UnicodeDecodeError:\n        pass\n    loi, r = [], _VANG', "thu_tu_k1", None),
    ("M4j", "caller đổi kho cùng nhóm ⇒ qua (F12)", "kho_ghim", '    ghi("K3", [', '    kho = "ducthangho/tra-luat"\n    ghi("K3", [', "duong_kho_khac", None),
    ("M4k", "caller đổi nhánh cùng nhóm ⇒ qua (F13)", "nhanh_ghim", '    ghi("K3", [', '    nhanh = "master"\n    ghi("K3", [', "duong_nhanh_khac", None),
    ("M1s2", "không mở tiến trình con (F20)", "tien_trinh", _DAU, _DAU + '\n    __import__("subprocess").run([sys.executable, "-c", "pass"])', "tinh", None),
    ("M1s3", "không đổi trạng thái sys (F20)", "trang_thai_sys", _DAU, _DAU + '\n    sys._dem_c1a1a = getattr(sys, "_dem_c1a1a", 0) + 1', "tinh", None),
    ("M1s4", "không mở tệp (F20)", "mo_tep", _DAU, _DAU + '\n    open(__file__, "rb").close()', "tinh", None),
    ("M1s5", "không đổi biến toàn cục module (F20)", "bien_toan_cuc", _DAU, _DAU + '\n    globals()["_goi_cuoi"] = raw', "tinh", None),
    ("M3u2", "hex64 phải là str (F28)", "hex64_ep_str", 'def _khop(mau):\n', 'def _khop(mau):\n    if mau == "[0-9a-f]{64}":\n'
     '        return lambda v: re.fullmatch(mau, str(v)) is not None\n', "hex64_la_so", None),
    ("M1s6", "không sửa sys.path (F29)", "sys_path", _DAU, _DAU + '\n    sys.path.append("c1a1a-probe")', "tinh", None),
    ("M1s7", "không sửa list toàn cục tại chỗ (F29)", "list_toan_cuc", ("_VANG = object()", _DAU),
     ("_NHAT_KY = []\n_VANG = object()", _DAU + "\n    _NHAT_KY.append(len(raw))"), "tinh", None),
    ("M1s8", "không mở tệp qua io.open (F29)", "io_open", _DAU, _DAU + '\n    __import__("io").open(__import__("os").devnull, "w").close()', "tinh", None),
    ("M1s9", "không posix_spawn/spawnv (F29)", "posix_spawn", _DAU, _DAU + '\n    __import__("os").posix_spawn(sys.executable, [sys.executable, "-c", "pass"], {}) if hasattr(__import__("os"), "posix_spawn") else __import__("os").spawnv(__import__("os").P_WAIT, sys.executable, [sys.executable, "-c", "pass"])', "tinh", None),
    ("M8a", "regex đăng ký buộc cặp ca", "mau_bo_1", r'(\1)', r'(\d+)', "dang_ky", None),
    ("M8b", "regex đăng ký buộc cặp đột biến", "mau_bo_3", r'(\3)', r'(\d+)', "dang_ky", None),
]
DB += [(f"M3z.{ten[4:]}", f"regex giờ: token {ten[4:]}", ten, 'r"' + "".join(t for t, _ in TOK) + '"', f'r"{rx}"', ten, None) for ten, rx, _ in GIO]
DB += [(f"M1z.K{n}", f"CLI giữ nguyên kết quả K{n} đỏ (F18)", f"cli_nuot_k{n}", _IN, f'    if kq["luat"]["K{n}"] == "do":\n'
        f'        kq = {{"ok": True, "luat": dict.fromkeys(kq["luat"], "qua"), "ly_do": []}}\n' + _IN, "cli", None) for n in range(1, 6)]


def _theo_truong():
    """A6: bỏ áp predicate cho TỪNG trường ⇒ ca riêng của trường ấy đỏ; trường bị chốt khác che thì khai TD."""
    td = {"schema_version": "TD: K1 kiểm int-không-bool và ==1 trước K2 (spec A6: K1 chặn, không tính làm bằng chứng K2)",
          **dict.fromkeys(C3, "TD: hai chốt kiểu C còn lại + quan hệ đồng nhất suy ra kiểu trường thứ ba (A7)")}
    return [(f"M3.{k}", f"áp kiểu cho {k}", f"bo_kieu_{k}", "# 7 khoá", f"KIEU[{k!r}] = lambda v: True\n# 7 khoá",
             td.get(k, f"kieu_{k}"), None) for k in list(SAI) + list(C3)]


def _nap(path, ten):
    truoc, sys.dont_write_bytecode = sys.dont_write_bytecode, True  # chống va chạm .pyc giữa các bản đột biến
    try:
        sp = importlib.util.spec_from_file_location(ten, path)
        m = importlib.util.module_from_spec(sp)
        sp.loader.exec_module(m)
        return m
    finally:
        sys.dont_write_bytecode = truoc


DUONG = {c[0] for c in CA if not c[2]}


def chay_dot_bien(nguon, dong):
    _id, _md, ten, cu, moi, dich, nem, *phu = dong
    if dich == "dang_ky":  # đột biến M8 đặt lên regex đăng ký, không lên module
        if MAU.count(cu) != 1:
            return "unresolved", "chuoi cu khong duy nhat trong MAU"
        try:
            ca_dang_ky("dang_ky", MAU.replace(cu, moi))
            return "unresolved", "song"
        except TinHieuChotCa as e:
            return ("witness_killed", "giet") if str(e).startswith("dang_ky: mau dang ky") else ("unresolved", f"tin dung gia: {e}")
    cap = list(zip(cu, moi)) if type(cu) is tuple and type(moi) is tuple and len(cu) == len(moi) else [(cu, moi)]
    if not cap or any(type(c) is not str or type(n) is not str for c, n in cap):  # 3/2, 2/3, 0/0, sai kiểu (luot4 F31)
        return "unresolved", "dot bien khai sai dang"
    ban = nguon
    for c, n in cap:  # tuple = đột biến nhiều chỗ, mỗi neo phải duy nhất
        if ban.count(c) != 1:
            return "unresolved", f"chuoi cu xuat hien {ban.count(c)} lan"
        ban = ban.replace(c, n)
    gac = phu[0] if phu else "duong_fixture"
    with tempfile.TemporaryDirectory() as t:
        p = pathlib.Path(t) / f"dot_bien_{ten}.py"  # tên riêng từng đột biến, bản sao tạm
        p.write_text(ban, encoding="utf-8")
        try:
            m = _nap(p, f"db_{ten}")
            if dich.startswith("TD:"):
                chay_ca(m, p, bo=gac if phu else ())
                return "equivalent_verified", "ca bo ca van xanh"
            if gac not in DUONG or gac == dich:  # ca gác phải CÓ THẬT, DƯƠNG, khác đích (luot3 F26)
                return "unresolved", f"ca gac A1 khong hop le: {gac}"
            chay_ca(m, p, {gac})  # A1: đột biến làm ca gác dương đỏ là quá tay (luot2 F16: không miễn theo tên ca đích)
            chay_ca(m, p, {dich})
            return "unresolved", "song"
        except TinHieuChotCa as e:
            s = str(e)
            if "NEM:" not in s:
                ok = s.startswith(dich + ":")
            else:  # ngoại lệ trần: đúng LOẠI và ném tại ĐÚNG dòng neo, dòng ấy phải DUY NHẤT trong bản đột biến (luot2 F15)
                if type(nem) is not tuple or len(nem) != 3:  # hàng khai sai dạng ⇒ không cấp tín dụng, không crash
                    return "unresolved", f"nem sai dang: {nem!r}"
                loai, dong_neo, gd = nem  # + GIAI ĐOẠN: số luật đã ghi khi dòng neo chạy (luot3 F25)
                so = [i for i, dong_ma in enumerate(ban.splitlines(), 1) if dong_ma.strip() == dong_neo]
                ok = len(so) == 1 and s == f"{dich}: NEM:{loai}@{so[0]}#{gd}"
            return ("witness_killed", "giet") if ok else ("unresolved", f"tin dung gia/qua tay: {s[:100]}")
        except Exception as e:
            return "unresolved", f"tin dung gia: {type(e).__name__}"


# ===================== Nhóm Git — C1a1b (#1179), spec `ops/specs/wp1179-c1a1b-r9.md` §4 =====================
# Đồ thị dựng bằng plumbing TRÊN `MOC` thật trong `clone --shared` tạm; oracle `tap_doc` tự đi đồ thị bằng `git cat-file`
# (không gọi module, không rev-list/merge-base/ls-tree); mỗi ca "chỉ G…" chạy guard A23 TRƯỚC khi tiêm.
MODUN_GIT, MOC, BK, WF = GOC / "doc_receipt_thu_hoi_git.py", S, "ops/lease_publish.py", ".github/workflows/ops-thu-hoi-admission.yml"
_EG = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
GOC_KHO = os.environ.get("DRTH_GOC_KHO") or subprocess.run(["git", "-C", str(GOC), "rev-parse", "--show-toplevel"], capture_output=True,
                                                         text=True, env=_EG).stdout.strip()
NHE = bool(os.environ.get("DRTH_E2E_NHE")) and bool(os.environ.get("DRTH_KHONG_E2E"))  # chỉ child e2e: mỗi bảng đột biến 1 dòng
G_, TT, NHAN, Z20 = tuple(f"G{i}" for i in range(10)), {"q": "qua", "d": "do", "k": "khong_do_duoc", "c": "khong_chay"}, ("100644", "100755", "120000"), bytes(20)
OID_WF, SHA_WF = FIX["workflow_definition_blob"], FIX["workflow_definition_sha256"]


def _g(k, *a, inp=None):
    r = subprocess.run(["git", "--no-replace-objects", "-C", str(k), *a], input=inp, capture_output=True, env=_EG, timeout=120)
    if r.returncode:
        raise LoiDo(f"git {' '.join(a[:2])} rc={r.returncode}: {r.stderr[-200:]!r}")
    return r.stdout


def _rev(k, x):
    return _g(k, "rev-parse", x).decode().strip()


def _obj(k, kieu, b):
    return _g(k, "hash-object", "-w", "--literally", "-t", kieu, "--stdin", inp=b).decode().strip()


_RAW = {}


def _raw(k, o):
    """(type, body) | (None, b"") — đọc trên kho tạm cho oracle/builder; KHÔNG đi qua module đang kiểm. Một tiến trình
    `cat-file --batch` giữ lâu cho mỗi kho (phép đi cả lịch sử của guard), đóng ở cuối mỗi ca (`chay_g`)."""
    p = _RAW.get(str(k)) or _RAW.setdefault(str(k), subprocess.Popen(
        ["git", "--no-replace-objects", "-C", str(k), "cat-file", "--batch"], stdin=subprocess.PIPE, stdout=subprocess.PIPE, env=_EG))
    p.stdin.write(o.encode() + b"\n")
    p.stdin.flush()
    c = p.stdout.readline().split()
    return (c[1].decode(), p.stdout.read(int(c[2]) + 1)[:-1]) if len(c) == 3 else (None, b"")


def _es(k, t):
    kieu, b, ket, i = *_raw(k, t), [], 0
    try:
        while kieu == "tree" and i < len(b):
            j = b.index(b"\0", i)
            m, n = b[i:j].decode().split(" ", 1)
            ket, i = ket + [(m, n, b[j + 1:j + 21].hex())], j + 21
        return ket if kieu == "tree" else None
    except ValueError:  # tree hỏng: oracle dừng đúng chỗ module dừng
        return None


def _ma_tree(es):
    return b"".join(f"{m} {n}".encode() + b"\0" + bytes.fromhex(o) for m, n, o in sorted(es, key=lambda e: e[1] + "/" * (e[0] == "40000")))


def _dat(k, t, duong, e):
    """Đặt entry `e` = (mode, OID) hoặc xoá (None) ở `duong` trong tree `t`; trả tree mới."""
    dau, _, duoi = duong.partition("/")
    es = {n: (m, o) for m, n, o in ((_es(k, t) or []) if t else [])}
    if duoi:
        e = ("40000", _dat(k, es.get(dau, ("", None))[1], duoi, e))
    es.pop(dau, None) if e is None else es.__setitem__(dau, e)
    return _obj(k, "tree", _ma_tree([(m, n, o) for n, (m, o) in es.items()]))


def _cm(k, tree, *cha, msg="c1a1b", hong=None):
    b = (f"tree {tree}\n" + "".join(f"parent {c}\n" for c in cha) + "author T <t@t> 1700000000 +0000\ncommitter T <t@t> 1700000000 +0000\n\n"
         + msg + "\n").encode()
    return _obj(k, "commit", hong(b) if hong else b)


def _blob(k, s):
    return _obj(k, "blob", s)


def gac_cay(F):
    """A9: tree(S), tree(H), tree(C) đôi một khác nhau — chạy trước mọi ca G (gọi trong `dung`)."""
    if len({F["tA"], F["tH"], F["tB"]}) != 3:
        raise LoiDo("A9: fixture dung chung tree giua S, H, C")


def dung(t, alias=False, msg_h="H1", hong=None, ten="k"):
    """§4: MOC → A → B → D first-parent, D = merge(B, E), H1 = con A, X = con MOC; S=A, C=B, H=H1, master=D. `hong`: dict
    vị trí → hàm: 'tA'/'tB' (k, tree) → tree cho commit A/B; 'A'/'B'/'H1' bytes commit → bytes."""
    k, h = pathlib.Path(t) / ten, hong or {}
    _g(GOC_KHO, "clone", "-q", "--shared", "--no-checkout", GOC_KHO, str(k))
    tm = _rev(k, MOC + "^{tree}")
    tA = _dat(k, tm, "ops/c1a1b_a.txt", ("100644", _blob(k, b"c1a1b A\n")))
    tB = _dat(k, tA, ".github/workflows/c1a1b_b.yml", ("100644", _blob(k, b"c1a1b B wf\n")))
    tB = tB if alias else _dat(k, tB, "ops/c1a1b_b.txt", ("100644", _blob(k, b"c1a1b B\n")))
    tH = _dat(k, tA, "c1a1b_h.txt", ("100644", _blob(k, b"c1a1b H\n")))
    tAc, tB = h["tA"](k, tA) if "tA" in h else tA, h["tB"](k, tB) if "tB" in h else tB
    A = _cm(k, tAc, MOC, msg="A", hong=h.get("A"))
    B, H1 = _cm(k, tB, A, msg="B", hong=h.get("B")), _cm(k, tH, A, msg=msg_h, hong=h.get("H1"))
    E = _cm(k, _dat(k, tA, "c1a1b_e.txt", ("100644", _blob(k, b"c1a1b E\n"))), A, msg="E")
    D, X = _cm(k, tB, B, E, msg="D"), _cm(k, _dat(k, tm, "c1a1b_x.txt", ("100644", _blob(k, b"c1a1b X\n"))), MOC, msg="X")
    _g(k, "update-ref", "refs/remotes/origin/master", D)
    F = {"k": k, "A": A, "B": B, "D": D, "E": E, "H1": H1, "X": X, "P": _rev(k, MOC + "^1"), "tA": tAc, "tB": tB, "tH": tH,
         "R": {**FIX, "S": A, "H": H1, **dict.fromkeys(C3, B), "T": tH, "tree_S": tAc},
         "tham": {"kho": KHO, "nhanh": "master", "base_hien_hanh": A, "head_hien_hanh": H1, "master": D, "goc_kho": str(k)}}
    gac_cay(F)
    return F


def thay(duong, ham):  # hàm cho `hong['tA'/'tB']`: thay entry ở `duong` bằng ham(k, OID entry tốt)
    return lambda k, t: _dat(k, t, duong, ham(k, _rev(k, f"{t}:{duong}")))


def V(**kv):
    return {g: TT[kv.get(g, "q")] for g in G_}


def chay(m, F, R=None, raw=None, **kw):
    th = {**F["tham"], **{x: kw.pop(x) for x in list(kw) if x in F["tham"]}}
    return m.kiem_git(raw if raw is not None else ma({**F["R"], **(R or {})}), **th, **kw)


def can(ten, kq, mong, chi=None):
    v = kq["git"]["luat"]
    if (v if chi is None else {g: v[g] for g in chi}) != (mong if chi is None else {g: mong[g] for g in chi}):
        raise TinHieuChotCa(f"{ten}: {v} != {mong}")


def tap_doc(F, R=None, master=None):
    """A23 oracle ĐỘC LẬP: doc(G) = các (kiểu mong đợi, OID) luật G cần đọc theo cột "đọc" §2.3, trên đồ thị thật."""
    k, R = F["k"], {**F["R"], **(R or {})}

    def hdr(c):
        kieu, b = _raw(k, c)
        dong = b.partition(b"\n\n")[0].decode("utf-8", "replace").splitlines() if kieu == "commit" else []
        return ([x[5:] for x in dong if x.startswith("tree ")] or [None])[-1], [x[7:] for x in dong if x.startswith("parent ")]

    def g1(x):
        o = []
        while x != MOC:
            o.append(("commit", x))
            x = (hdr(x)[1] or [MOC])[0]
        return o

    def tt(duoi, tren):
        o, ngan = [], [tren] * (duoi != tren)
        while ngan:
            x = ngan.pop()
            if ("commit", x) not in o:
                o.append(("commit", x))
                ch = hdr(x)[1]
                if duoi in ch:
                    break
                ngan += ch
        return o

    def dg(c, duong, blob=None):
        t, phan = hdr(c)[0], duong.split("/")
        o = [("commit", c)] + [("tree", t)] * (t is not None)
        for i, p in enumerate(phan * (t is not None)):  # commit không có tree (hỏng/sai kiểu): module dừng ở commit
            e = {n: (md, x) for md, n, x in (_es(k, t) or [])}.get(p)
            if e is None or (i < len(phan) - 1 and e[0] != "40000"):
                break
            if i == len(phan) - 1:
                return o + [("blob", e[1])] * (blob is not None and e[0] in NHAN and e[1] == blob)
            t = e[1]
            o.append(("tree", t))
        return o
    S_, H_, C_ = R["S"], R["H"], R["checkout_commit"]
    return {"G1": g1(master or F["tham"]["master"]), "G2": tt(S_, C_), "G3": tt(S_, H_), "G4": [("commit", H_)], "G5": [("commit", S_)],
            "G6": dg(S_, BK), "G7": dg(C_, BK, R["oid_bo_kiem_da_chay"]), "G8": dg(C_, WF, R["workflow_definition_blob"]), "G9": []}


def _co(k, o):
    return not subprocess.run(["git", "-C", str(k), "cat-file", "-e", o], env=_EG, capture_output=True).returncode


def _loose(F, o):
    return F["k"] / ".git" / "objects" / o[:2] / o[2:]


def gac_luu(F, o):
    """A23(e) guard VỊ TRÍ LƯU: object loose trong clone tạm và KHÔNG có trong kho gốc (alternate), nếu không xoá vô nghĩa."""
    if not _loose(F, o).is_file() or _co(GOC_KHO, o):
        raise LoiDo(f"guard vi tri luu: {o} khong phai object loose rieng cua clone tam")


def _mo_ghi(F, o):
    """Sau guard: gỡ read-only của loose object (git ghi chỉ-đọc; Windows từ chối unlink/ghi — A16, WinError 5)."""
    gac_luu(F, o)
    _loose(F, o).chmod(0o644)  # Windows chỉ đọc bit S_IWRITE (0o200) của mode
    return _loose(F, o)


def xoa(F, o):
    _mo_ghi(F, o).unlink()
    if _co(F["k"], o):
        raise LoiDo(f"xoa {o} xong cat-file -e van thay")


def ghi_de(F, o, kieu):
    """`E_bam_lech`: bytes ĐÚNG kiểu, cấu trúc hợp lệ, nhưng không băm ra tên — chỉ chốt băm lại bắt được."""
    p = _mo_ghi(F, o)
    b = {"tree": _ma_tree([("100644", "c1a1b_gia", "ab" * 20)]), "commit": f"tree {F['tA']}\n\nc1a1b gia\n".encode()}.get(kieu, b"gia")
    p.write_bytes(zlib.compress(f"{kieu} {len(b)}\0".encode() + b))


class Ra:
    """Bọc stdout của reader: 'lech' = dòng đầu đúng dạng mà OID khác (thân giữ nguyên); 'hong' = thay CẢ phản hồi bằng một
    dòng sai dạng (luồng vẫn đồng bộ, nên chỉ reader bị kết thúc mới làm luật sau đổi màu)."""

    def __init__(s, f, oid, kieu, cb=None, k=7):
        s.f, s.oid, s.kieu, s.cb, s.k, s.buf, s.eof = f, oid.encode(), kieu, cb, k, b"", False

    def readline(s):
        if s.eof:
            return b""
        d = s.f.readline()
        if s.oid and d.startswith(s.oid):
            s.oid, c = None, d.split()
            if s.kieu in ("cut", "lf", "eof_lf"):  # F5: header đúng, phần SAU header bị cắt / LF thay / EOF trước LF
                than = s.f.read(int(c[2]) + 1)[:-1]
                s.buf, s.eof = {"cut": than[:s.k], "lf": than + b"X", "eof_lf": than}[s.kieu], s.kieu != "lf"  # 'lf': luồng chạy tiếp
                return d
            if s.kieu == "han":  # lật đồng hồ seam đúng lúc đọc object này (deadline GIỮA luật)
                s.cb()
                return d
            if s.kieu == "lech":
                return b" ".join([X40.encode(), *c[1:]]) + b"\n"
            s.f.read(int(c[2]) + 1)
            return b"c1a1b sai dang\n"
        return d

    def read(s, n):
        if s.buf or s.eof:
            s.buf, b = s.buf[n:], s.buf[:n]
            return b
        return s.f.read(n)


def ra(oid, kieu, cb=None, k=7, **seam):
    return {"_seam": {"ra": lambda f: Ra(f, oid, kieu, cb, k), **seam}}


def giet_sau(g0):
    def h(g, d):
        if g == g0:
            d.p.kill()
            d.p.wait()
    return {"_seam": {"sau_luat": h}}


def gac(ten, F, kieu, oid, dich, R=None, master=None):
    """A23 guard sự kiện CỤC BỘ: {G : (kiểu, OID) ∈ doc(G)} phải bằng tập KHAI, chạy TRƯỚC khi tiêm."""
    tinh = {g for g, o in tap_doc(F, R, master).items() if (kieu, oid) in o}
    if not tinh or tinh != set(dich):
        raise LoiDo(f"{ten}: guard A23 tap doc {sorted(tinh)} != khai {sorted(dich)}")
    return tinh


def gac_chung(ten, F, g, x, dich, R=None):
    """A23 guard sự kiện CHUNG phát lần đầu ở object `x` của luật `g`: memo = doc(G1..G(g-1)) + phần doc(g) trước `x`; luật
    đích = g và mọi luật sau còn cần object ngoài memo (bảng phạm vi §2.3). Phải bằng tập KHAI."""
    d, i = tap_doc(F, R), int(g[1:])
    memo = {o for j in range(1, i) for o in d[f"G{j}"]} | set(d[g][:d[g].index(x)] if x in d[g] else [None])
    tinh = {g} | {h for h in G_[i + 1:9] if not set(d[h]) <= memo}
    if x not in d[g] or tinh != set(dich):
        raise LoiDo(f"{ten}: guard su kien chung {sorted(tinh)} != khai {sorted(dich)}")
    return memo - {None}


def gac_walk(ten, F, gioi, dich, R=None):
    """A23 guard trần commit MỖI phép đi: đúng các luật đi đồ thị có số commit cần đọc vượt `gioi` mới là đích."""
    d = tap_doc(F, R)
    if {g for g in ("G1", "G2", "G3") if len(d[g]) > gioi} != set(dich):
        raise LoiDo(f"{ten}: guard tran phep di")


def su_kien(ten, m, F, kieu, oid, tiem, dich, R=None, **kw):
    """A12/A20/A23: luật đích = {G : (kiểu, OID) ∈ doc(G)}; guard so với tập KHAI trước khi tiêm; luật khác giữ màu."""
    tinh = gac(ten, F, kieu, oid, dich, R, kw.get("master"))
    v0, them = chay(m, F, R, **kw)["git"]["luat"], tiem() or {}
    kq = chay(m, F, R, **kw, **them)
    can(ten, kq, {g: "khong_do_duoc" if g in tinh else v0[g] for g in G_})
    if any(v0[g] == "khong_do_duoc" for g in tinh):
        raise TinHieuChotCa(f"{ten}: luat dich da khong_do_duoc truoc khi tiem: {v0}")
    return kq


def _kich(F, tap):
    return sum(len(_raw(F["k"], o[1])[1]) for o in set(tap))


def gac_tong(F):
    """A23(e) guard KÍCH THƯỚC (A13 tổng byte): mỗi luật G6–G8 cần ít byte hơn trần = tổng byte G1–G5."""
    d = tap_doc(F)
    tran = _kich(F, [o for g in G_[1:6] for o in d[g]])
    if max(_kich(F, d[g]) for g in ("G6", "G7", "G8")) >= tran:
        raise LoiDo("guard kich thuoc: mot luat G6-G8 can >= tran tong byte")
    return tran


def gac_memo(F, sau):
    """A23(e) guard ĐIỂM TIÊM: mọi object của doc(G4) ∪ doc(G5) đã nằm trong memo khi tiêm sau luật `sau`."""
    d = tap_doc(F)
    if not set(d["G4"] + d["G5"]) <= {o for g in G_[1:int(sau[1:]) + 1] for o in d[g]}:
        raise LoiDo(f"guard diem tiem: doc(G4)+doc(G5) chua nam trong memo sau {sau}")


def cli(m, F, raw, **th):
    with tempfile.TemporaryDirectory() as t:
        p = pathlib.Path(t) / "r.json"
        p.write_bytes(raw)
        a = {"--receipt": str(p), "--kho": KHO, "--nhanh-mac-dinh": "master", "--base-hien-hanh": F["tham"]["base_hien_hanh"],
             "--head-hien-hanh": F["tham"]["head_hien_hanh"], "--master": F["tham"]["master"], "--goc-kho": str(F["k"]), **th}
        return subprocess.run([sys.executable, "-B", m.__file__, "kiem-git", *[f"{x}={v}" for x, v in a.items()]], capture_output=True, timeout=120)


CG = {}


def cg(ten):
    def dk(f):
        CG[ten] = f
        return f
    return dk


def mj():  # C1a1a nạp RIÊNG cho oracle A3, không đi qua module Git đang kiểm
    return _nap(MODUN, "c1a1a_doi_chung")


@cg("g_duong")
def _g_duong(m, t, ten):
    F = dung(t)
    kq = chay(m, F)
    can(ten, kq, V())
    if kq["ok"] is not True or m.ma_thoat(kq) != 0:
        raise TinHieuChotCa(f"{ten}: ok={kq['ok']!r}")


@cg("g_fixture")
def _g_fixture(m, t, ten):
    gac_cay(dung(t))
    try:
        gac_cay({"tA": "a", "tH": "a", "tB": "b"})
    except LoiDo:
        return
    raise TinHieuChotCa(f"{ten}: guard A9 nhan fixture hai tree trung")


@cg("g_json_nguyen_ven")
def _g_json(m, t, ten):
    F = dung(t)
    for nhan, R, raw, th in (("duong", None, None, {}), ("k4", None, None, {"base_hien_hanh": X40}), ("k2", {"job_id": None}, None, {}),
                             ("k1", None, b"{}", {})):
        b = raw if raw is not None else ma({**F["R"], **(R or {})})
        p = {**F["tham"], **th}
        if chay(m, F, raw=b, **th)["json"] != mj().kiem_json(b, kho=KHO, nhanh="master", base_hien_hanh=p["base_hien_hanh"],
                                                            head_hien_hanh=p["head_hien_hanh"]):
            raise TinHieuChotCa(f"{ten}:{nhan}: json khong nguyen ven")


def _to_hop(F):  # A4/A5: (a) dương (b) một G do (c) chỉ khong_do_duoc (d) JSON đỏ + mọi G qua (e) G0 do
    return [("a", ma(F["R"]), {}), ("b", ma({**F["R"], "T": F["tA"]}), {}), ("c", ma({**F["R"], "H": X40}), {"head_hien_hanh": X40}),
            ("d", ma(F["R"]), {"base_hien_hanh": X40}), ("e", b" " * (8388608 + 1), {})]


@cg("g_abi")
def _g_abi(m, t, ten):
    F = dung(t)
    for nhan, raw, th in _to_hop(F):
        kq = chay(m, F, raw=raw, **th)
        g, lu = kq.get("git"), (kq.get("git") or {}).get("luat") or {}
        if (set(kq) != {"ok", "json", "git", "do_dac"} or set(g) != {"luat", "ly_do"} or set(kq["do_dac"]) != {"so_object", "tong_bytes"}
                or any(type(v) is not int for v in kq["do_dac"].values()) or tuple(lu) != G_ or not set(lu.values()) <= set(TT.values())
                or type(kq["ok"]) is not bool or kq["ok"] is not (nhan == "a") or type(g["ly_do"]) is not list
                or not all(any(x.startswith(f"{q}: ") and lu[q] != "qua" for q in G_) for x in g["ly_do"])):
            raise TinHieuChotCa(f"{ten}:{nhan}: ABI sai {kq}")
        c = cli(m, F, raw, **{f"--{x.replace('_', '-')}": v for x, v in th.items()})
        if c.stdout != (json.dumps(kq, ensure_ascii=True, sort_keys=True) + "\n").encode("ascii"):
            raise TinHieuChotCa(f"{ten}:{nhan}: byte stdout khac kiem_git: {c.stdout[:120]!r}")


@cg("g_ma_thoat")
def _g_ma_thoat(m, t, ten):
    F = dung(t)
    for nhan in ("a+b", "-x"):  # ref có thật: chỉ chốt mẫu tên mới trả 2
        _g(F["k"], "update-ref", f"refs/remotes/origin/{nhan}", F["D"])
    rong = pathlib.Path(t) / "rong"
    rong.mkdir()
    ds = [(n, raw, {f"--{x.replace('_', '-')}": v for x, v in th.items()}, rc) for (n, raw, th), rc in zip(_to_hop(F), (0, 12, 13, 12, 12))]
    ds += [("do_va_kdd", ma({**F["R"], "H": X40, "tree_S": F["tH"]}), {"--head-hien-hanh": X40}, 12),
           ("json_do", ma({**F["R"], "checker_rc": 1}), {}, 12)]
    ds += [(f"tham_{x}={v}", ma(F["R"]), {x: v}, 2) for x, v in (
        ("--kho", ""), ("--nhanh-mac-dinh", "a+b"), ("--nhanh-mac-dinh", "-x"), ("--base-hien-hanh", F["A"].upper()),
        ("--head-hien-hanh", F["H1"][:39]), ("--master", F["D"] + "0"), ("--goc-kho", str(rong / "khong")), ("--receipt", str(rong / "x.json")),
        ("--master", F["X"]), ("--nhanh-mac-dinh", "khong-co"))]  # hai dòng cuối: N6 lệch, ref vắng ở lần đọc đầu
    for nhan, raw, th, rc in ds:
        c = cli(m, F, raw, **th)
        kq = json.loads(c.stdout) if rc != 2 and c.stdout else None
        if c.returncode != rc or (rc == 2) != (c.stdout == b"") or (kq is not None and kq["ok"] is not (rc == 0)):
            raise TinHieuChotCa(f"{ten}:{nhan}: rc={c.returncode} != {rc}, stdout={c.stdout[:80]!r}")
        if kq is not None and m.ma_thoat(kq) != rc:
            raise TinHieuChotCa(f"{ten}:{nhan}: ma_thoat lech rc")


@cg("g_khong_chay")
def _g_khong_chay(m, t, ten):
    F = dung(t)
    c9 = {g: "c" for g in G_[1:]}
    for nhan, raw, mong, th in (("k1", b"{}", V(**c9), {}), ("k2", ma({**F["R"], "job_id": None}), V(**c9), {}),
                                ("g0", b" " * 8388609, V(G0="d", **c9), {}), ("k4", ma(F["R"]), V(), {"base_hien_hanh": X40})):
        kq = chay(m, F, raw=raw, **th)
        can(f"{ten}:{nhan}", kq, mong)
        if kq["ok"] or (kq["json"] is None) != (nhan == "g0"):
            raise TinHieuChotCa(f"{ten}:{nhan}: ok/json sai")


@cg("g_g1")
def _g_g1(m, t, ten):
    F = dung(t)
    for c, tt in (("B", "q"), (MOC, "q"), ("P", "d"), ("E", "d"), ("X", "d")):
        can(f"{ten}:C={c[:8]}", chay(m, F, dict.fromkeys(C3, F.get(c, c))), V(G1=tt), ("G1",))
    Q2 = _cm(F["k"], F["tA"], _cm(F["k"], F["tA"], F["P"], msg="Q1"), msg="Q2")
    _g(F["k"], "update-ref", "refs/remotes/origin/master", Q2)
    can(f"{ten}:i", chay(m, F, master=Q2), V(G1="d"))


@cg("g_g1_ii")
def _g_g1_ii(m, t, ten):
    F = dung(t)
    Q1 = _cm(F["k"], F["tA"], F["P"], msg="Q1")
    Q2 = _cm(F["k"], F["tA"], Q1, msg="Q2")
    _g(F["k"], "update-ref", "refs/remotes/origin/master", Q2)
    su_kien(ten, m, F, "commit", Q1, lambda: xoa(F, Q1), {"G1"}, master=Q2)


@cg("g_g2g3")
def _g_g2g3(m, t, ten):
    F = dung(t)
    HB = _cm(F["k"], F["tB"], F["B"], msg="HB")
    for nhan, R, th, mong in (("S=B,C=A", {"S": F["B"], **dict.fromkeys(C3, F["A"]), "tree_S": F["tB"]}, {"base_hien_hanh": F["B"]}, "d"),
                              ("H=X", {"H": F["X"], "T": _rev(F["k"], F["X"] + "^{tree}")}, {"head_hien_hanh": F["X"]}, "d"),
                              ("S=C=B", {"S": F["B"], "H": HB, "T": F["tB"], "tree_S": F["tB"]},
                               {"base_hien_hanh": F["B"], "head_hien_hanh": HB}, "q")):
        g = {"S=B,C=A": ("G2",), "H=X": ("G3",), "S=C=B": ("G2", "G3")}[nhan]
        can(f"{ten}:{nhan}", chay(m, F, R, **th), V(**dict.fromkeys(g, mong)), g)


@cg("g_g4g5")
def _g_g4g5(m, t, ten):
    F = dung(t)
    for nhan, R, mong in (("T=tree(S)", {"T": F["tA"]}, V(G4="d")), ("tree_S=tree(H)", {"tree_S": F["tH"]}, V(G5="d")),
                          ("T=rong", {"T": "4b825dc642cb6eb9a060e54bf8d69288fbee4904"}, V(G4="d"))):
        can(f"{ten}:{nhan}", chay(m, F, R), mong)


def _bang(m, t, ten, vt, g, hang):
    """A10/A11: mỗi hàng (nhãn, hàm tree hoặc None, R thêm, trạng thái mong) dựng một fixture riêng; mọi luật khác qua."""
    for i, (nhan, ham, R, tt) in enumerate(hang):
        F = dung(t, hong={vt: ham} if ham else None, ten=f"k{i}")
        if tt == "k":  # F4: object vắng chỉ thuộc tập đọc của đúng luật đang đo
            gac(f"{ten}:{nhan}", F, "blob", X40, {g}, R)
        can(f"{ten}:{nhan}", chay(m, F, R), V(**{g: tt}))


@cg("g_g6")
def _g_g6(m, t, ten):
    bl = lambda k, t_: _dat(k, t_, "ops", ("100644", _blob(k, b"c1a1b ops blob\n")))
    _bang(m, t, ten, "tA", "G6", [
        ("co_null", None, {"oid_bo_kiem_tai_S": None}, "d"), ("co_dung", None, {}, "q"), ("co_khac", None, {"oid_bo_kiem_tai_S": X40}, "d"),
        ("vang_null", lambda k, t_: _dat(k, t_, BK, None), {"oid_bo_kiem_tai_S": None}, "q"),
        ("vang_hex", lambda k, t_: _dat(k, t_, BK, None), {}, "d"),
        ("gitlink", lambda k, t_: _dat(k, t_, BK, ("160000", X40)), {"oid_bo_kiem_tai_S": X40}, "q"),
        ("blob_null", bl, {"oid_bo_kiem_tai_S": None}, "d"), ("blob_hex", bl, {}, "d")])


def _hang78(duong, khoa, sha):
    """Các dòng bảng G7/G8 §2.4 cho `duong` trong tree(C); `khoa` là trường OID của receipt."""
    dat = lambda e: (lambda k, t_: _dat(k, t_, duong, e(k) if callable(e) else e))
    sym = lambda k: ("120000", _blob(k, b"lease_publish_dich.py"))
    o, so = OID if duong == BK else OID_WF, hashlib.sha1(b"blob 21\0lease_publish_dich.py").hexdigest()
    h = [("100755", dat(("100755", o)), {}, "q"),
         ("120000", dat(sym), {khoa: so, **({"workflow_definition_sha256": hashlib.sha256(b"lease_publish_dich.py").hexdigest()} if sha else {})}, "q"),
         ("oid_khac", None, {khoa: X40}, "d"), ("160000", dat(("160000", o)), {}, "d"), ("40000", dat(("40000", o)), {}, "d"),
         ("vang", dat(None), {}, "d"), ("to_tien_blob", lambda k, t_: _dat(k, t_, duong.split("/")[0], ("100644", _blob(k, b"x\n"))), {}, "d"),
         ("blob_vang", dat(("100644", X40)), {khoa: X40}, "k"), ("f6_lech_vang", dat(("100644", X40)), {}, "d")]
    return h + ([("sha_lech", None, {"workflow_definition_sha256": "ab" * 32}, "d")] if sha else [])


def _g78(m, t, ten, g, duong, khoa, sha):
    hang = _hang78(duong, khoa, sha)
    _bang(m, t, ten, "tB", g, hang)
    F = dung(t, hong={"tB": next(h[1] for h in hang if h[0] == "f6_lech_vang")}, ten="kf6")
    if cli(m, F, ma(F["R"])).returncode != 12:  # F6: OID lệch × blob vắng ⇒ do, rc 12 (không 13)
        raise TinHieuChotCa(f"{ten}:f6_rc")


@cg("g_g7")
def _g_g7(m, t, ten):
    _g78(m, t, ten, "G7", BK, "oid_bo_kiem_da_chay", False)


@cg("g_g8")
def _g_g8(m, t, ten):
    _g78(m, t, ten, "G8", WF, "workflow_definition_blob", True)


def _opsB(F):
    return _rev(F["k"], F["tB"] + ":ops")


@cg("g_r_a")
def _g_r_a(m, t, ten):
    F = dung(t)
    if m.ma_thoat(su_kien(ten, m, F, "commit", F["H1"], lambda: xoa(F, F["H1"]), {"G3", "G4"})) != 13:
        raise TinHieuChotCa(f"{ten}: rc != 13")


@cg("g_r_b")
def _g_r_b(m, t, ten):
    F = dung(t)
    su_kien(ten, m, F, "tree", _opsB(F), lambda: ghi_de(F, _opsB(F), "tree"), {"G7"})


@cg("g_r_c")
def _g_r_c(m, t, ten):
    F = dung(t)
    _g(F["k"], "update-ref", f"refs/replace/{F['B']}", F["X"])
    can(ten, chay(m, F), V())


@cg("g_r_d")
def _g_r_d(m, t, ten):
    F, cu = dung(t), os.environ.get("GIT_OBJECT_DIRECTORY")
    os.environ["GIT_OBJECT_DIRECTORY"] = t
    try:
        kq = chay(m, F)
    finally:
        os.environ.pop("GIT_OBJECT_DIRECTORY") if cu is None else os.environ.__setitem__("GIT_OBJECT_DIRECTORY", cu)
    can(ten, kq, V())


for _ten, _sau, _mong in (("g_r_e", "G0", V(**dict.fromkeys(G_[1:9], "k"))), ("g_r_f", "G5", V(G6="k", G7="k", G8="k")),
                          ("g_r_f2", "G3", V(G6="k", G7="k", G8="k"))):
    def _f(m, t, ten, sau=_sau, mong=_mong):
        F = dung(t)
        if sau == "G3":
            gac_memo(F, sau)
        if sau != "G0":  # reader chết được PHÁT HIỆN ở lần đọc chưa memo đầu tiên: tree(S) của G6
            gac_chung(ten, F, "G6", ("tree", F["tA"]), {g for g in G_ if mong[g] == "khong_do_duoc"})
        can(ten, chay(m, F, **giet_sau(sau)), mong)
    cg(_ten)(_f)


def _shim(t):
    """PATH có shim ĐỨNG GIỮA (giống `cmd\\git.exe` của Windows): kill shim thì git con vẫn sống, giữ ống. Trên Windows dùng
    chính shim của Git for Windows trên PATH (đo A16 07-11); POSIX dựng `sh` KHÔNG `exec`."""
    if os.name == "nt":
        return os.environ["PATH"]
    d = pathlib.Path(t) / "shim"
    d.mkdir()
    (d / "git").write_text(f'#!/bin/sh\n"{subprocess.run(["git", "--exec-path"], capture_output=True, text=True).stdout.strip()}/git" "$@"\n')
    (d / "git").chmod(0o755)
    return f"{d}{os.pathsep}{os.environ['PATH']}"


@cg("g_r_shim")  # reader chết THẬT và Timer deadline gỡ ĐÚNG tiến trình giữ ống, kể cả khi PATH có shim
def _g_r_shim(m, t, ten):
    F, cu = dung(t), os.environ["PATH"]
    gac_chung(ten, F, "G6", ("tree", F["tA"]), {"G6", "G7", "G8"})
    con = []

    def han(g, d):  # deadline 0.3 s đồng hồ thật: đợi Timer nổ rồi đo ỐNG GHI — còn người đọc nghĩa là chỉ giết trung gian
        if g == "G1":
            d.hen.join(10)
            try:
                d.p.wait(3)
            except subprocess.TimeoutExpired:
                pass
            try:
                os.write(d.p.stdin.fileno(), b"\n")
                con.append("ong ghi con nguoi doc")
            except (OSError, ValueError):
                pass
    os.environ["PATH"] = _shim(t)
    try:
        kq = chay(m, F, **giet_sau("G5"))
        kq2 = chay(m, F, ngan_sach={"deadline_giay": 0.3}, _seam={"sau_luat": han})
    finally:
        os.environ["PATH"] = cu
    can(ten, kq, V(G6="k", G7="k", G8="k"))
    can(ten, kq2, V(**dict.fromkeys(G_[2:], "k")))
    if con:
        raise TinHieuChotCa(f"{ten}: Timer deadline khong go tien trinh giu ong: {con}")


@cg("g_r_g")
def _g_r_g(m, t, ten):
    F = dung(t)
    su_kien(ten, m, F, "tree", _opsB(F), lambda: ra(_opsB(F), "lech"), {"G7"})


@cg("g_r_h")
def _g_r_h(m, t, ten):
    F = dung(t)
    gac_chung(ten, F, "G7", ("tree", _opsB(F)), {"G7", "G8"})
    can(ten, chay(m, F, **ra(_opsB(F), "hong")), V(G7="k", G8="k"))


# F3: sự kiện chung PHÁT HIỆN ở H1 (G3); G5 phải giữ `qua` nhờ memo A từ G1 — khoá hậu quả SAU điểm phát hiện thật
_SAU_H1 = V(G3="k", G4="k", G6="k", G7="k", G8="k")


@cg("g_r_h3")
def _g_r_h3(m, t, ten):
    F = dung(t)
    gac_chung(ten, F, "G3", ("commit", F["H1"]), {g for g in G_ if _SAU_H1[g] == "khong_do_duoc"})
    can(ten, chay(m, F, **ra(F["H1"], "hong")), _SAU_H1)


def _than(ten, m, F, g, x, dich, k, **kw):
    """F5: reader chết vì thân/LF ⇒ vector theo bảng phạm vi; do_dac = memo tại điểm phát hiện + đúng `k` byte thân đã trả."""
    memo = gac_chung(ten, F, g, x, dich)
    kq = chay(m, F, **kw)
    can(ten, kq, V(**dict.fromkeys(dich, "k")))
    if kq["do_dac"] != {"so_object": len(memo) + 1, "tong_bytes": _kich(F, memo) + k}:
        raise TinHieuChotCa(f"{ten}: do_dac {kq['do_dac']} != {len(memo) + 1} object / {_kich(F, memo) + k} B")


@cg("g_r_cut")  # thân cụt rồi EOF: ở ops(B), và ĐANG XẢ H1 quá max_object (đọc dở trên nhánh xả)
def _g_r_cut(m, t, ten):
    F = dung(t, ten="a")
    _than(f"{ten}:ops", m, F, "G7", ("tree", _opsB(F)), {"G7", "G8"}, 7, **ra(_opsB(F), "cut"))
    G = _to(pathlib.Path(t) / "b")
    _than(f"{ten}:xa", m, G, "G3", ("commit", G["H1"]), {"G3", "G4", "G6", "G7", "G8"}, 7, ngan_sach={"max_object_bytes": gac_obj(G)},
          **ra(G["H1"], "cut"))


@cg("g_r_lf")  # thân đủ, byte phân cách khác LF / EOF trước LF
def _g_r_lf(m, t, ten):
    for kieu in ("lf", "eof_lf"):
        F = dung(t, ten=kieu)
        n = len(_raw(F["k"], _opsB(F))[1])
        _than(f"{ten}:{kieu}", m, F, "G7", ("tree", _opsB(F)), {"G7", "G8"}, n, **ra(_opsB(F), kieu))


@cg("g_ns_tong3")
def _g_ns_tong3(m, t, ten):
    F = dung(t)
    gac_chung(ten, F, "G3", ("commit", F["H1"]), {g for g in G_ if _SAU_H1[g] == "khong_do_duoc"})
    d = tap_doc(F)
    can(ten, chay(m, F, ngan_sach={"max_tong_bytes": _kich(F, d["G1"] + d["G2"])}), _SAU_H1)


@cg("g_ns_commit")
def _g_ns_commit(m, t, ten):
    F = dung(t)
    gac_walk(ten, F, 2, {"G1"})
    can(ten, chay(m, F, ngan_sach={"max_commit_moi_phep_di": 2}), V(G1="k"))


@cg("g_ns_g2")  # ô G2 × E_ngan_sach (F3): S = MOC nên G2, G3 phải đi tới MOC
def _g_ns_g2(m, t, ten):
    F = dung(t)
    R = {"S": MOC, "tree_S": _rev(F["k"], MOC + "^{tree}")}
    gac_walk(ten, F, 1, {"G1", "G2", "G3"}, R)
    can(ten, chay(m, F, R, base_hien_hanh=MOC, ngan_sach={"max_commit_moi_phep_di": 1}), V(G1="k", G2="k", G3="k"))


@cg("g_ns_walk")
def _g_ns_walk(m, t, ten):
    F = dung(t)
    h = F["A"]
    for i in range(4):
        h = _cm(F["k"], F["tA"], h, msg=f"Hc{i}")
    gac_walk(ten, F, 3, {"G3"}, {"H": h})
    can(ten, chay(m, F, {"H": h, "T": F["tA"]}, head_hien_hanh=h, ngan_sach={"max_commit_moi_phep_di": 3}), V(G3="k"))


def _to(t):
    return dung(t, msg_h="H1 " + "x" * 300000)


@cg("g_ns_obj")
def _g_ns_obj(m, t, ten):
    F = _to(t)
    can(ten, chay(m, F, ngan_sach={"max_object_bytes": gac_obj(F)}), V(G3="k", G4="k"))


def gac_obj(F):
    """A23(e) guard KÍCH THƯỚC (A13 max_object_bytes): trần = cỡ H1 − 1 phải lớn hơn mọi object khác luật sẽ đọc."""
    n = len(_raw(F["k"], F["H1"])[1])
    if max(len(_raw(F["k"], o[1])[1]) for ds in tap_doc(F).values() for o in ds if o[1] != F["H1"]) >= n - 1:
        raise LoiDo("guard kich thuoc max_object_bytes")
    return n - 1


@cg("g_ns_tong")
def _g_ns_tong(m, t, ten):
    F = _to(t)
    can(ten, chay(m, F, ngan_sach={"max_tong_bytes": gac_tong(F)}), V(G6="k", G7="k", G8="k"))


@cg("g_ns_han")
def _g_ns_han(m, t, ten):
    F, gio = dung(t), [0.0]
    gac_memo(F, "G3")

    def h(g, d):
        if g == "G3":
            gio[0] = 1e9
    can(ten, chay(m, F, _seam={"dong_ho": lambda: gio[0], "sau_luat": h}), V(**dict.fromkeys(G_[4:], "k")))


def _han(g0=None):  # đồng hồ seam: lật quá hạn sau luật `g0` (hook), hoặc qua hàm `lat` trả về
    gio = [0.0]

    def lat():
        gio[0] = 1e9
    return {"dong_ho": lambda: gio[0], "sau_luat": lambda g, d: g == g0 and lat()}, lat


@cg("g_ns_han0")  # F1(a): hết hạn trước một luật KHÔNG đọc object (G2 khi S = C) ⇒ vẫn khong_do_duoc
def _g_ns_han0(m, t, ten):
    F = dung(t)
    HB = _cm(F["k"], F["tB"], F["B"], msg="HB")
    R = {"S": F["B"], "H": HB, "T": F["tB"], "tree_S": F["tB"]}
    if tap_doc(F, R)["G2"]:
        raise LoiDo(f"{ten}: guard: G2 phai la nhanh khong doc object")
    sm, _ = _han("G1")
    can(ten, chay(m, F, R, base_hien_hanh=F["B"], head_hien_hanh=HB, _seam=sm), V(**dict.fromkeys(G_[2:], "k")))


@cg("g_ns_han_g8")  # F1(b): hết hạn GIỮA luật — trong lần đọc blob cuối của G8 — kết quả vừa tính không được ghi
def _g_ns_han_g8(m, t, ten):
    F = dung(t)
    sm, lat = _han()
    can(ten, chay(m, F, _seam={**sm, **ra(OID_WF, "han", lat)["_seam"]}), V(G8="k", G9="k"))


@cg("g_ns_han_g9")  # F1(c): hết hạn trong G9 (trước lần đọc ref cuối)
def _g_ns_han_g9(m, t, ten):
    F = dung(t)
    sm, lat = _han()
    can(ten, chay(m, F, _seam={**sm, "truoc_g9": lat}), V(G9="k"))


@cg("g_ns_dem")  # F2: byte/object đã đọc khỏi ống được đếm ở MỌI đường, khớp oracle; memo/sổ lỗi không đếm lại
def _g_ns_dem(m, t, ten):
    for nhan, F, kw, tiem in (
            ("kieu_sai", dung(t, hong={"tB": lambda k, t_: _dat(k, t_, "ops", ("40000", _blob(k, b"c1a1b la blob\n")))}, ten="a"), {}, None),
            ("lech_la", dung(t, ten="b"), ra(OID, "lech"), None), ("bam_lech", dung(t, ten="c"), {}, "opsB"),
            ("max_object", _to(pathlib.Path(t) / "d"), {}, None)):
        if tiem:
            ghi_de(F, _oid(F, tiem), "tree")
        if nhan == "max_object":
            kw = {"ngan_sach": {"max_object_bytes": gac_obj(F)}}
        u = {o for ds in tap_doc(F).values() for o in ds}
        dd = chay(m, F, **kw)["do_dac"]
        if dd != {"so_object": len(u), "tong_bytes": _kich(F, u)}:
            raise TinHieuChotCa(f"{ten}:{nhan}: do_dac {dd} != {len(u)} object / {_kich(F, u)} B")


@cg("g_ns_memo")
def _g_ns_memo(m, t, ten):
    F = dung(t)
    u = {o for g, ds in tap_doc(F).items() for o in ds}
    dd = chay(m, F)["do_dac"]
    if dd != {"so_object": len(u), "tong_bytes": _kich(F, u)}:
        raise TinHieuChotCa(f"{ten}: do_dac {dd} != {len(u)} object / {_kich(F, u)} B")


@cg("g_ns_g0")
def _g_ns_g0(m, t, ten):
    F = dung(t)
    b = ma(F["R"])
    can(ten, chay(m, F, raw=b + b" " * (8388608 - len(b))), V())
    if (m.TRAN_RECEIPT, m.NGAN_SACH, m.MOC) != (8388608, {"max_commit_moi_phep_di": 50000, "max_object_bytes": 8388608,
                                                         "max_tong_bytes": 134217728, "deadline_giay": 60.0}, MOC):
        raise TinHieuChotCa(f"{ten}: hang mac dinh lech bang §2.6")


@cg("g_troi")
def _g_troi(m, t, ten):
    F = dung(t)
    for nhan, lenh in (("doi", ("update-ref", "refs/remotes/origin/master", F["X"])), ("xoa", ("update-ref", "-d", "refs/remotes/origin/master"))):
        _g(F["k"], "update-ref", "refs/remotes/origin/master", F["D"])
        kq = chay(m, F, _seam={"truoc_g9": lambda lenh=lenh: _g(F["k"], *lenh)})
        can(f"{ten}:{nhan}", kq, V(G9="k"))
        if m.ma_thoat(kq) != 13:
            raise TinHieuChotCa(f"{ten}:{nhan}: rc != 13")


# A20: ô (luật × sự kiện cục bộ) phủ bằng ca sinh: mỗi object một tập đích khai tay, guard A23 so với oracle.
_OBJ = {"D": ("commit", "G1"), "B": ("commit", "G1 G2 G7 G8"), "H1": ("commit", "G3 G4"), "A": ("commit", "G1 G5 G6"),
        "opsA": ("tree", "G6"), "opsB": ("tree", "G7"), "wfB": ("tree", "G8")}


def _oid(F, ten):
    return F.get(ten) or _rev(F["k"], {"opsA": F["tA"] + ":ops", "opsB": F["tB"] + ":ops", "wfB": F["tB"] + ":.github/workflows"}[ten])


for _o, (_kieu, _dich) in _OBJ.items():
    for _ev, _tiem in (("vang", lambda F, o, k: xoa(F, o)), ("bam", lambda F, o, k: ghi_de(F, o, k)), ("lech", lambda F, o, k: ra(o, "lech"))):
        def _f(m, t, ten, o=_o, kieu=_kieu, dich=_dich, tiem=_tiem):
            F = dung(t)
            oid = _oid(F, o)
            su_kien(ten, m, F, kieu, oid, lambda: tiem(F, oid, kieu), set(dich.split()))
        cg(f"g_o_{_ev}_{_o}")(_f)


@cg("g_k_entry")  # E_kieu_sai: entry `ops` của tree(B) mode 40000 mà object là blob ⇒ chỉ G7
def _g_k_entry(m, t, ten):
    F = dung(t, hong={"tB": lambda k, t_: _dat(k, t_, "ops", ("40000", _blob(k, b"c1a1b la blob\n")))})
    gac(ten, F, "tree", _rev(F["k"], F["tB"] + ":ops"), {"G7"})
    can(ten, chay(m, F), V(G7="k"))


@cg("g_k_moc")  # E_kieu_sai trên OID lấy từ receipt / cạnh parent
def _g_k_moc(m, t, ten):
    F = dung(t)
    bl = _blob(F["k"], b"c1a1b parent la blob\n")
    H2, M2 = _cm(F["k"], F["tH"], bl, msg="H2"), _cm(F["k"], F["tB"], bl, msg="M2")
    for nhan, R, th, mong, x in (("C=tree", dict.fromkeys(C3, F["tB"]), {}, V(G1="d", G2="k", G7="k", G8="k"), F["tB"]),
                                 ("H=tree", {"H": F["tH"]}, {"head_hien_hanh": F["tH"]}, V(G3="k", G4="k"), F["tH"]),
                                 ("S=tree", {"S": F["tA"]}, {"base_hien_hanh": F["tA"]}, V(G2="d", G3="d", G5="k", G6="k"), F["tA"]),
                                 ("cha_H=blob", {"H": H2}, {"head_hien_hanh": H2}, V(G3="k"), bl)):
        gac(f"{ten}:{nhan}", F, "commit", x, {g for g in G_ if mong[g] == "khong_do_duoc"}, R)
        can(f"{ten}:{nhan}", chay(m, F, R, **th), mong)
    _g(F["k"], "update-ref", "refs/remotes/origin/master", M2)
    gac(f"{ten}:cha_master=blob", F, "commit", bl, {"G1"}, master=M2)
    can(f"{ten}:cha_master=blob", chay(m, F, master=M2), V(G1="k"))


# A20b: tập chốt parser — mỗi chốt một đuôi entry thêm vào tree hợp lệ, ở ba vị trí (S `ops`, C `ops`, C workflows).
_DUOI = {"t1a": b"100644 c1a1b_cut", "t1b": b"100644 zz\0\x01\x02\x03\x04\x05", "t2": b"100644zz\0" + Z20, "t3": b"100600 zz\0" + Z20,
         "t4": b"100644 \xff\0" + Z20, "t5": b"100644 \0" + Z20, "t6": b"100644 .\0" + Z20, "t7": b"100644 ..\0" + Z20,
         "t8": b"100644 lease_publish.py/x\0" + Z20, "t9": b"40000 .git\0" + Z20, "t10": None, "ctl": b"100644 zz_c1a1b\0" + Z20}
_VT = {"S": ("tA", "ops", "G6"), "C": ("tB", "ops", "G7"), "W": ("tB", ".github/workflows", "G8")}


def _hong_tree(chot):
    def f(k, o):
        b = _raw(k, o)[1]
        return ("40000", _obj(k, "tree", b + (_DUOI[chot] if _DUOI[chot] is not None else b[:b.index(b"\0") + 21])))
    return f


for _chot in _DUOI:
    for _v, (_cay, _duong, _gd) in _VT.items():
        def _f(m, t, ten, chot=_chot, cay=_cay, duong=_duong, gd=_gd):
            F = dung(t, hong={cay: thay(duong, _hong_tree(chot))})
            bad = _rev(F["k"], F[cay] + ":" + duong)
            if chot != "ctl" and {g for g, o in tap_doc(F).items() if ("tree", bad) in o} != {gd}:
                raise LoiDo(f"{ten}: guard A23 tap doc")
            can(ten, chay(m, F), V(**({} if chot == "ctl" else {gd: "k"})))
        cg(f"g_p_{_chot}_{_v}")(_f)


_C1, _C2 = (lambda b: b.replace(b"tree ", b"xree ", 1)), (lambda b: b.replace(b"\nparent ", b"\nparent zz\nparent ", 1))
for _c, _vt, _ham, _dich in (("c1", "H1", _C1, "G3 G4"), ("c2", "H1", _C2, "G3 G4"), ("c1A", "A", _C1, "G1 G5 G6"), ("c1B", "B", _C1, "G1 G2 G7 G8")):
    def _f(m, t, ten, vt=_vt, h=_ham, dich=_dich):
        F = dung(t, hong={vt: h})
        gac(ten, F, "commit", F[vt], dich.split())
        can(ten, chay(m, F), V(**dict.fromkeys(dich.split(), "k")))
    cg(f"g_p_{_c}")(_f)


@cg("g_p_alias")
def _g_p_alias(m, t, ten):
    h = thay("ops", _hong_tree("t8"))
    F = dung(t, alias=True, hong={"tA": h, "tB": h})
    if _oid(F, "opsA") != _oid(F, "opsB"):
        raise LoiDo(f"{ten}: guard alias: ops(A) != ops(B)")
    gac(ten, F, "tree", _oid(F, "opsA"), {"G6", "G7"})
    can(ten, chay(m, F), V(G6="k", G7="k"))


@cg("g_tap_doc")  # A23(a): oracle khớp bảng §4 theo OID; oracle không gọi module, không rev-list/merge-base/ls-tree
def _g_tap_doc(m, t, ten):
    F = dung(t)
    o = {x: _oid(F, x) for x in ("opsA", "opsB", "wfB")}
    gh = _rev(F["k"], F["tB"] + ":.github")
    c, tr = (lambda *x: [("commit", F[y]) for y in x]), (lambda *x: [("tree", y) for y in x])
    mong = {"G1": c("D", "B", "A"), "G2": c("B"), "G3": c("H1"), "G4": c("H1"), "G5": c("A"), "G6": c("A") + tr(F["tA"], o["opsA"]),
            "G7": c("B") + tr(F["tB"], o["opsB"]) + [("blob", OID)], "G8": c("B") + tr(F["tB"], gh, o["wfB"]) + [("blob", OID_WF)], "G9": []}
    if {g: set(v) for g, v in tap_doc(F).items()} != {g: set(v) for g, v in mong.items()} or len({o["opsA"], o["opsB"], o["wfB"]}) != 3:
        raise TinHieuChotCa(f"{ten}: tap doc lech bang §4")
    nguon = ast.get_source_segment(pathlib.Path(__file__).read_text(encoding="utf-8"),
                                   next(n for n in ast.walk(ast.parse(pathlib.Path(__file__).read_text(encoding="utf-8")))
                                        if isinstance(n, ast.FunctionDef) and n.name == "tap_doc"))
    if any(x in nguon for x in ("kiem_git", "Doc(", "rev-list", "merge-base", "ls-tree", "MODUN_GIT")):
        raise TinHieuChotCa(f"{ten}: oracle tap doc dung module hoac engine do thi cua git")


@cg("g_alias")  # A23(d) + ca alias §4: ops(A) = ops(B) cùng OID (loose trong clone) ⇒ G6 và G7; G4, G8 qua
def _g_alias(m, t, ten):
    for nhan, tiem in (("xoa", xoa), ("bam", lambda F, o: ghi_de(F, o, "tree"))):
        F = dung(t, alias=True, ten=nhan)
        o = _oid(F, "opsA")
        if o != _oid(F, "opsB"):
            raise LoiDo(f"{ten}: guard alias: ops(A) != ops(B)")
        kq = su_kien(f"{ten}:{nhan}", m, F, "tree", o, lambda: tiem(F, o), {"G6", "G7"})
        can(f"{ten}:{nhan}", kq, V(G6="k", G7="k"))


def _phai_loi_do(ten, f):
    try:
        f()
    except LoiDo:
        return
    raise TinHieuChotCa(f"{ten}: guard khong chan")


@cg("g_guard")  # A23(c, e): mỗi guard tiền đề có ca âm riêng; guard sai ⇒ lỗi setup, không bỏ qua
def _g_guard(m, t, ten):
    F = dung(t, alias=True, ten="a")
    _phai_loi_do(f"{ten}:tap_doc", lambda: su_kien(ten, m, F, "tree", _oid(F, "opsB"), lambda: xoa(F, _oid(F, "opsB")), {"G7"}))
    G = dung(t, ten="b")
    _phai_loi_do(f"{ten}:vi_tri_luu", lambda: gac_luu(G, _rev(G["k"], MOC + ":ops")))  # alias kiểu r7: `ops` mượn từ MOC
    _phai_loi_do(f"{ten}:kich_thuoc", lambda: gac_tong(G))  # không phóng to H1
    _phai_loi_do(f"{ten}:diem_tiem", lambda: gac_memo(G, "G0"))  # tiêm trước G1
    _phai_loi_do(f"{ten}:max_object", lambda: gac_obj(G))  # không phóng to H1
    _phai_loi_do(f"{ten}:su_kien_chung", lambda: gac_chung(ten, G, "G7", ("tree", _oid(G, "opsB")), {"G7"}))  # G8 còn đọc
    _phai_loi_do(f"{ten}:tran_phep_di", lambda: gac_walk(ten, G, 2, {"G1", "G3"}))


# A20 (F3): MỘT ô cho mỗi (luật × sự kiện E mà luật ấy gặp được), mỗi ô một ca đích; mỗi ô một đột biến riêng (`DBG`).
_EV7 = ("E_vang", "E_bam_lech", "E_kieu_sai", "E_hong", "E_ngan_sach", "E_framing_lech", "E_reader_chet")
_VAT = dict(zip(G_[1:9], ("D", "B", "H1", "H1", "A", "opsA", "opsB", "wfB")))
O_GIT = {(g, e): c for g, o in _VAT.items() for e, c in (
    ("E_vang", f"g_o_vang_{o}"), ("E_bam_lech", f"g_o_bam_{o}"), ("E_framing_lech", f"g_o_lech_{o}"), ("E_reader_chet", "g_r_e"),
    ("E_kieu_sai", "g_k_entry" if g == "G7" else "g_k_moc"),
    ("E_hong", {"G1": "g_p_c1A", "G2": "g_p_c1B", "G3": "g_p_c1", "G4": "g_p_c1", "G5": "g_p_c1A", "G6": "g_p_t8_S", "G7": "g_p_t8_C",
                "G8": "g_p_t8_W"}[g]),
    ("E_ngan_sach", {"G1": "g_ns_commit", "G2": "g_ns_g2", "G3": "g_ns_walk", "G4": "g_ns_obj", "G5": "g_ns_han"}.get(g, "g_ns_tong")))}
O_GIT.update({("G9", "E_ngan_sach"): "g_ns_han", ("G9", "E_troi_ref"): "g_troi"})


@cg("g_o_bang")
def _g_o_bang(m, t, ten):
    du = {(g, e) for g in G_[1:9] for e in _EV7} | {("G9", "E_ngan_sach"), ("G9", "E_troi_ref")}
    if set(O_GIT) != du or not set(O_GIT.values()) <= set(CG):
        raise TinHieuChotCa(f"{ten}: bang o luat x su kien thieu {sorted(du - set(O_GIT))} hoac tro ca khong co")


def dong_nhom(ten, ca, db, ev):  # dòng nhóm KHÔNG được khớp regex sổ đăng ký (A18)
    return f"nhom {ten}: {ca[0]}/{ca[1]} ca QUA · {db[0]}/{db[1]} dot bien GIET · equivalent_verified {ev}"


def dong_tong(nj, mj_, ng, mg):
    """A18: dòng tổng chỉ khi CẢ HAI nhóm đã chạy, N_git ≥ 1 và M_git ≥ 1; mỗi đối số là (đạt, tổng) hoặc None."""
    if ng is None or mg is None or ng[1] < 1 or mg[1] < 1:
        return None
    return f"doc_receipt_thu_hoi tests: {nj[0] + ng[0]}/{nj[1] + ng[1]} ca QUA · {mj_[0] + mg[0]}/{mj_[1] + mg[1]} dot bien GIET"


@cg("g_dong_tong")
def _g_dong_tong(m, t, ten):
    for nhan, a, dat in (("du", ((3, 3), (2, 2), (1, 1), (1, 1)), True), ("ca_git_0", ((3, 3), (2, 2), (0, 0), (1, 1)), False),
                         ("db_git_0", ((3, 3), (2, 2), (1, 1), (0, 0)), False), ("git_vang", ((3, 3), (2, 2), None, None), False),
                         ("ca_hong", ((3, 3), (2, 2), (0, 1), (1, 1)), False)):
        d = dong_tong(*a)
        if bool(d and re.fullmatch(MAU, d)) != dat or re.fullmatch(MAU, dong_nhom("git", (3, 3), (2, 2), 0)) or (NHE and not os.environ.get("DRTH_KHONG_E2E")):
            raise TinHieuChotCa(f"{ten}:{nhan}: {d!r}")


if not os.environ.get("DRTH_KHONG_E2E"):
    @cg("g_dong_tong_e2e")
    def _g_e2e(m, t, ten):
        T = pathlib.Path(t)
        for p in (pathlib.Path(__file__), MODUN, MODUN_GIT, GOC / "ci_dang_ky_test.py"):
            (T / p.name).write_bytes(p.read_bytes())
        mau = _nap(T / "ci_dang_ky_test.py", "e2e_ci_dang_ky").MOI[".claude/dev/doc_receipt_thu_hoi_test.py"]
        e = {**os.environ, "DRTH_GOC_KHO": GOC_KHO, "DRTH_KHONG_E2E": "1", "DRTH_E2E_NHE": "1"}  # child NHẸ: A16 Windows hết 3600 s
        con = lambda: subprocess.run([sys.executable, "-B", str(T / pathlib.Path(__file__).name)], cwd=T, capture_output=True, text=True,
                                     timeout=3600, env=e)
        if e.get("DRTH_E2E_NHE") != "1":  # đo TRƯỚC khi chạy: child đầy đủ trên Windows quá hạn, thành lỗi vô can
            raise TinHieuChotCa(f"{ten}: child e2e khong chay ban nhe")
        r = con()  # (0) child DƯƠNG trước trên đúng setup
        ds = r.stdout.splitlines()
        if r.returncode or not any(x.startswith("nhom json: ") for x in ds) or not any(x.startswith("nhom git: ") for x in ds) \
                or not any(re.fullmatch(mau, x) and x.endswith(" · 2/2 dot bien GIET") for x in ds):
            raise LoiDo(f"{ten}: child duong hong rc={r.returncode}: {r.stdout[-300:]} {r.stderr[-300:]}")
        for nhan, noi, dau in (("import", 'raise ImportError("c1a1b-e2e")\n', "ImportError: c1a1b-e2e"), ("cu_phap", "def (:\n", "SyntaxError"),
                               ("vang", None, "FileNotFoundError")):
            (T / MODUN_GIT.name).unlink(missing_ok=True)
            if noi is not None:
                (T / MODUN_GIT.name).write_text(noi, encoding="utf-8")
            r = con()
            if not r.returncode or any(re.fullmatch(mau, x) for x in r.stdout.splitlines()) or dau not in r.stderr or MODUN_GIT.name not in r.stderr:
                raise TinHieuChotCa(f"{ten}:{nhan}: rc={r.returncode} stdout={r.stdout[-200:]!r} stderr={r.stderr[-200:]!r}")


def chay_g(m, chi=None):
    for ten, f in CG.items():
        if chi is None or ten in chi:
            with tempfile.TemporaryDirectory(prefix="c1a1b_", ignore_cleanup_errors=True) as t:
                try:
                    f(m, t, ten)
                finally:
                    for p in _RAW.values():
                        p.kill()
                        p.wait()
                        p.stdin.close()
                        p.stdout.close()
                    _RAW.clear()


# Bảng nghĩa vụ nhóm Git: (ID, mệnh đề, tên đột biến, chuỗi cũ, chuỗi mới — tuple = nhiều chỗ, ca đích | "TD: lập luận", ca gác).
# Ca gác mặc định `g_duong`; None khi đột biến tất yếu đổi fixture dương (khai rõ, không ngầm miễn).
_KDD, _TRY, _HAN = 'ghi(g, "khong_do_duoc", str(e))', "                try:  # F1:", "                    d.kiem_han()\n                    dat, ly = f()\n                    d.kiem_han()\n"
_TT = r'''            if j < 0 or j + 21 > len(b):
                raise SuKien(f"E_hong: t1 {oid}")'''
DBG = [
    ("A3a", "json = kiem_json C1a1a nguyên vẹn", "json_hang", "    j = C1A1A.kiem_json(raw, kho=kho, nhanh=nhanh, base_hien_hanh=base_hien_hanh, head_hien_hanh=head_hien_hanh)",
     '    j = {"ok": True, "luat": dict.fromkeys(("K1", "K2", "K3", "K4", "K5"), "qua"), "ly_do": []}', "g_json_nguyen_ven"),
    ("A3b", "không thêm khoá vào json", "json_them_khoa", '"json": j,', '"json": {**j, "x": 1},', "g_json_nguyen_ven"),
    ("A4a", "ok đòi mọi G qua", "ok_chi_json", 'ok = j["ok"] is True and all(v == "qua" for v in luat.values())', 'ok = j["ok"] is True', "g_abi"),
    ("A4b", "ok đòi JSON qua", "ok_bo_json", 'ok = j["ok"] is True and all(', 'ok = all(', "g_abi"),
    ("A4c", "stdout sort_keys", "bo_sort_keys", "ensure_ascii=True, sort_keys=True)", "ensure_ascii=True)", "g_abi"),
    ("A4d", "do_dac đúng hai khoá", "them_giay", '"tong_bytes": d.tong_bytes}', '"tong_bytes": d.tong_bytes, "giay": 0}', "g_abi"),
    ("A4e", "trạng thái thuộc tập đóng", "trang_thai_loi", _KDD, 'ghi(g, "loi", str(e))', "g_abi"),
    ("A5a", "12 xét trước 13", "thu_tu_12_13", '    if kq["json"] is None or kq["json"]["ok"] is not True or "do" in tt:',
     '    if "khong_do_duoc" in tt:\n        return 13\n    if kq["json"] is None or kq["json"]["ok"] is not True or "do" in tt:', "g_ma_thoat"),
    ("A5b", "N6 ban đầu ⇒ rc 2", "bo_n6", "    if doc_ref(a.goc_kho, nh) != a.master:", "    if False:", "g_ma_thoat"),
    ("A5c", "nhánh khớp mẫu", "bo_mau_nhanh", 'not re.fullmatch(r"[A-Za-z0-9._-]+", nh) or ', "", "g_ma_thoat"),
    ("A5d", "nhánh không bắt đầu bằng -", "bo_dau_gach", ' or nh.startswith("-"):', ":", "g_ma_thoat"),
    ("A6a", "K2 đỏ ⇒ G khong_chay", "g_khi_k2", ' and j["luat"]["K2"] != "do":', ":", "g_khong_chay"),
    ("A6b", "K4 đỏ không chặn G", "bo_g_khi_k4", ' and j["luat"]["K2"] != "do":', ' and j["luat"]["K2"] != "do" and j["luat"]["K4"] != "do":', "g_khong_chay"),
    ("A6c", "G0 qua sau JSON đỏ", "g0_khong_chay", '    if j["luat"]["K1"] != "do"', '    luat["G0"] = "qua" if j["ok"] else "khong_chay"\n    if j["luat"]["K1"] != "do"',
     "g_khong_chay"),
    ("A7a", "G1 đi first-parent", "moi_parent", "            x = cha[0]", "            x = cha[-1]", "g_g1", None),
    ("A7b", "G1 dừng ở biên MOC", "bo_bien_moc", ("            if x == MOC:", 'return False, "het chuoi'), ('            if x == "0" * 40:', 'return gap, "het chuoi'),
     "g_g1"),
    ("A7c", "biên MOC gồm cả MOC", "loai_tru_moc", "            gap = gap or x == c", "            gap = gap or (x == c and x != MOC)", "g_g1"),
    ("A7d", "hết chuỗi không gặp MOC ⇒ do", "het_chuoi_kdd", '                return False, "het chuoi first-parent ma khong gap MOC"',
     '                raise SuKien("E_vang: het chuoi")', "g_g1"),
    ("A7e", "object vắng không phải hết chuỗi", "vang_la_het", "            cha = s.commit(x)[1]",
     "            try:\n                cha = s.commit(x)[1]\n            except SuKien:\n                cha = []", "g_g1_ii"),
    ("A8a", "G2 = S ≤ C, đúng chiều", "dao_toan_hang", '("G2", lambda: d.to_tien(S, C))', '("G2", lambda: d.to_tien(C, S))', "g_g2g3", None),
    ("A8b", "G3 so S với H", "g3_so_c", '("G3", lambda: d.to_tien(S, H))', '("G3", lambda: d.to_tien(S, C))', "g_g2g3"),
    ("A9a", "G4 so T với tree(H)", "g4_tree_s", 'lambda: (d.commit(H)[0] == r["T"]', 'lambda: (d.commit(S)[0] == r["T"]', "g_g4g5", None),
    ("A9b", "G5 so tree_S với tree(S)", "g5_tree_h", 'lambda: (d.commit(S)[0] == r["tree_S"]', 'lambda: (d.commit(H)[0] == r["tree_S"]', "g_g4g5", None),
    ("A10a", "G6 không đọc object entry", "g6_doc_entry", '            return False, f"to tien mode {e[1]} khong phai tree"\n        return',
     '            return False, f"to tien mode {e[1]} khong phai tree"\n        if e[0] == "co":\n            s.doc(e[2], "blob")\n        return', "g_g6"),
    ("A10b", "tổ tiên không phải tree ⇒ do", "khong_tree_la_vang", '            return False, f"to tien mode {e[1]} khong phai tree"',
     '            return oid_s is None, ""', "g_g6"),
    ("A10c", "có entry thì null ⇒ do", "nhan_null", 'else (oid_s == e[2], ', 'else (oid_s in (None, e[2]), ', "g_g6"),
    ("A11a", "G7 riêng predicate G6", "g7_la_g6", '("G7", lambda: d.g7(C, r["oid_bo_kiem_da_chay"]))', '("G7", lambda: d.g6(C, r["oid_bo_kiem_da_chay"]))', "g_g7"),
    ("A11b", "G7 nhận 120000", "bac_120000", 'NHAN = ("100644", "100755", "120000")', 'NHAN = ("100644", "100755")', "g_g7"),
    ("A11c", "G7 không theo symlink", "theo_symlink", "        e = s.tim(s.commit(C)[0], duong)  #",
     '        e = s.tim(s.commit(C)[0], duong)\n        if e[0] == "co" and e[1] == "120000":\n'
     '            e = s.tim(s.commit(C)[0], duong.rsplit("/", 1)[0] + "/" + s.doc(e[2], "blob").decode())  #', "g_g7"),
    ("A11d", "G7 đọc blob", "bo_doc_blob", '        b = s.doc(oid, "blob")', '        b = s.doc(oid, "blob") if sha else b""', "g_g7"),
    ("A11e", "G8 so sha256", "bo_sha", "hashlib.sha256(b).hexdigest() == sha", "True", "g_g8"),
    ("A11f", "so OID trước khi đọc blob (F6)", "doc_blob_truoc", "        if e[2] != oid:\n", '        s.doc(e[2], "blob")\n        if e[2] != oid:\n', "g_g7"),
    ("A12a", "băm lại mọi object", "bo_bam", r'        if hashlib.sha1(f"{loai} {n}\0".encode("ascii") + than).hexdigest() != oid:', "        if False:", "g_r_b"),
    ("A12b", "không theo refs/replace", "bo_replace", ('_git_exe(), "--no-replace-objects", "-C", str(s.goc), "cat-file"', 'GIT_NO_REPLACE_OBJECTS="1", '),
     ('_git_exe(), "-C", str(s.goc), "cat-file"', ""), "g_r_c"),
    ("A12l", "reader là git THẬT, không qua shim PATH", "git_qua_path", "    return _GIT[0]", '    return "git"', "g_r_shim"),
    ("A12m", "Timer deadline giết tiến trình giữ ống", "timer_rong", "threading.Timer(s.ns[\"deadline_giay\"], s.p.kill)",
     "threading.Timer(s.ns[\"deadline_giay\"], lambda: None)", "g_r_shim"),
    ("A12c", "lọc GIT_* thừa kế", "bo_loc_git", '    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}', "    e = dict(os.environ)", "g_r_d"),
    ("A12d", "reader chết không khởi động lại", "khoi_dong_lai", "        s.chet = True  #", '        s._mo()\n        raise SuKien("E_reader_chet: mo lai")  #', "g_r_e"),
    ("A12e", "reader chết là sự kiện CHUNG", "chet_cuc_bo", '            s._chet(f"dong dau sai dang {dau[:60]!r}")', '            raise SuKien("E_reader_chet: cuc bo")', "g_r_h"),
    ("A12f", "kết quả đã hoàn tất bất biến", "ghi_de_hoan_tat", '        dd = {"so_object"',
     '        if d.chet:\n            luat.update(dict.fromkeys(LUAT[1:9], "khong_do_duoc"))\n        dd = {"so_object"', "g_r_f"),
    ("A12g", "memo giữ được SAU khi phát hiện reader chết", "xoa_memo", "        s.chet = True  #", "        s.memo.clear()\n        s.chet = True  #", "g_r_h3"),
    ("A12h", "reader chết không chặn memo (khác deadline)", "deadline_cho_reader", "        if k in s.memo:\n",
     '        if s.chet:\n            raise SuKien("E_reader_chet: x")\n        if k in s.memo:\n', "g_r_h3"),
    ("A12j", "tổng byte không chặn memo", "tong_chan_memo", "        if k in s.memo:\n",
     '        if s.het_tong:\n            raise SuKien("E_ngan_sach: tong byte")\n        if k in s.memo:\n', "g_ns_tong3"),
    ("A12i", "framing lệch là cục bộ", "lech_la_chet", '        if m[1] != oid.encode():\n            raise SuKien(f"E_framing_lech',
     '        if m[1] != oid.encode():\n            s._chet("x")\n            raise SuKien(f"E_framing_lech', "g_r_g"),
    ("A13a", "bộ đếm commit riêng từng phép đi", "gop_dem", '        if dem > s.ns["max_commit_moi_phep_di"]:',
     '        s.tong_dem = getattr(s, "tong_dem", 0) + 1\n        if s.tong_dem > s.ns["max_commit_moi_phep_di"]:', "g_ns_walk"),
    ("A13b", "chốt max_object_bytes", "bo_max_obj", 'if n > s.ns["max_object_bytes"]', "if False", "g_ns_obj"),
    ("A13c", "tổng byte là tài nguyên chung", "tong_cuc_bo", _TRY, "                d.tong_bytes, d.het_tong = 0, False\n" + _TRY, "g_ns_tong"),
    ("A13d", "deadline đầu luật", "bo_han_dau", _HAN, "                    dat, ly = f()\n                    d.kiem_han()\n",
     "TD: kiem_han CUỐI luật bắt mọi hạn đã qua trước khi ghi kết quả; đầu luật chỉ là dừng sớm (đo nhóm ở A13d3)"),
    ("A13d2", "deadline cuối luật, sau lần đọc cuối", "bo_han_cuoi", _HAN, "                    d.kiem_han()\n                    dat, ly = f()\n", "g_ns_han_g8"),
    ("A13d3", "deadline đầu+cuối luật cả nhóm", "bo_han_ca_nhom", _HAN, "                    dat, ly = f()\n", "g_ns_han0"),
    ("A13d4", "deadline trong doc() là dừng sớm", "bo_han_doc", "        s.kiem_han()  #", "        pass  #",
     "TD: kiem_han cuối luật quyết định kết quả; lần kiểm trong doc() chỉ cắt phép đi dài, không đổi vector"),
    ("A13h", "đếm byte ở MỌI đường (F2)", "dem_chi_thanh_cong", ("            if dem:\n                s.tong_bytes += len(c)\n", "        return than\n\n    def commit"),
     ("", "        s.tong_bytes += n\n        return than\n\n    def commit"), "g_ns_dem"),
    ("A13i", "đếm cả thân bị xả (F2)", "dem_bo_xa", "            if dem:\n", "            if dem and giu:\n", "g_ns_dem"),
    ("A13j", "đếm byte đọc dở trước EOF (F5)", "dem_sau_lay_du", ("            if dem:\n                s.tong_bytes += len(c)\n", '        return b"".join(ket)'),
     ("", '        s.tong_bytes += n if dem else 0\n        return b"".join(ket)'), "g_r_cut"),
    ("A12k", "byte sau thân phải là LF (F5)", "bo_so_lf", 'if s._lay(1, dem=False) != b"\\n":', 'if s._lay(1, dem=False) != b"\\n" and False:', "g_r_lf"),
    ("A13e", "memo đếm mỗi object một lần", "bo_memo", "        s.memo[k] = than\n", "", "g_ns_memo"),
    ("A13f", "G0 nhận đúng 8.388.608 byte", "g0_ge", "    if len(raw) > TRAN_RECEIPT:", "    if len(raw) >= TRAN_RECEIPT:", "g_ns_g0"),
    ("A14a", "trôi ref ⇒ 13, không 2", "g9_rc2", '    tt = set(kq["git"]["luat"].values())',
     '    if any(x.startswith("G9: ") for x in kq["git"]["ly_do"]):\n        return 2\n    tt = set(kq["git"]["luat"].values())', "g_troi"),
    ("A14b", "G9 đọc lại ref", "bo_doc_lai", "            v = doc_ref(goc_kho, nhanh, timeout=", "            v = master or doc_ref(goc_kho, nhanh, timeout=", "g_troi"),
    ("A20a", "sự kiện cục bộ không lan", "lan_su_kien", '                    ghi(g, "qua" if dat else "do", ly)',
     '                    ghi(g, "khong_do_duoc" if "khong_do_duoc" in luat.values() else "qua" if dat else "do", ly)', "g_o_vang_opsB"),
    ("A20b.t1", "chốt t1", "bo_t1", _TT, '            if False:\n                raise SuKien("")', "g_p_t1b_C"),
    ("A20b.t2", "chốt t2", "bo_t2", "            if not sep:", "            if False:",
     "TD: t2 bị t3/t5 che — không dấu cách thì cả phần trước NUL là mode (ngoài tập ⇒ t3) hoặc mode đúng mà tên rỗng (⇒ t5)"),
    ("A20b.t235", "chốt t2+t3+t5 cả nhóm", "bo_t2_t3_t5", ("            if not sep:", "            if mode not in MODE:", '("t5", not ten)'),
     ("            if False:", "            if False:", '("t5", False)'), "g_p_t2_C"),
    ("A20b.t3", "chốt t3", "bo_t3", "            if mode not in MODE:", "            if False:", "g_p_t3_C"),
    ("A20b.t4", "chốt t4", "bo_t4", 'ten = ten_b.decode("utf-8")', 'ten = ten_b.decode("utf-8", "replace")', "g_p_t4_C"),
    ("A20b.c1", "chốt c1", "bo_c1", "        if not tree or not _H40.fullmatch(tree):", "        if False:", "g_p_c1"),
    ("A20b.c2", "chốt c2", "bo_c2", "        if any(not _H40.fullmatch(c) for c in cha):", "        if False:", "g_p_c2"),
    ("A23a", "sự kiện không lưu thành rỗng", "memo_rong", "                s.loi[k] = str(e)", '                s.memo[k] = b""', "g_alias"),
    ("A23b", "luật sau nhận lại sự kiện", "chi_luat_dau", "            raise SuKien(s.loi[k])", '            return b""', "g_alias"),
]
DBG += [(f"A20b.{c}", f"chốt {c}", f"bo_{c}", f'("{c}", {v})', f'("{c}", False)', f"g_p_{c}_C")
        for c, v in (("t5", "not ten"), ("t6", 'ten == "."'), ("t7", 'ten == ".."'), ("t8", '"/" in ten'), ("t9", 'ten == ".git"'), ("t10", "ten in ket"))]
DBG += [(f"A20.{g}.{e}", f"ô {g} × {e} ⇒ khong_do_duoc", f"do_{g}_{e}", _KDD,
         f'ghi(g, "do" if g == "{g}" and str(e).startswith("{e}") else "khong_do_duoc", str(e))', c) for (g, e), c in O_GIT.items()]
# Đột biến HẠ TẦNG (r3 F7): đặt trong CHÍNH suite, chạy trên bản sao suite cạnh bản chép nguyên byte của hai module + sổ.
_NAP = '    mg = _nap(MODUN_GIT, "doc_receipt_thu_hoi_git")'
DBH = [
    ("H1", "caller không nuốt lỗi nạp nhóm Git", "nuot_import", (_NAP, "    ng, mgd, hong_g = nhom_git(mg)", "    d = dong_tong(nj, mj_, ng, mgd)"),
     ("    try:\n    " + _NAP + "\n    except Exception:\n        mg = None", "    ng, mgd, hong_g = nhom_git(mg) if mg else (None, None, [])",
      '    d = dong_tong(nj, mj_, ng, mgd) if mg else f"doc_receipt_thu_hoi tests: {nj[0]}/{nj[1]} ca QUA · {mj_[0]}/{mj_[1]} dot bien GIET"'),
     "g_dong_tong_e2e"),
    ("H14", "child e2e chạy bản nhẹ (A16 Windows)", "bo_co_nhe", ', "DRTH_E2E_NHE": "1"}', "}", "g_dong_tong_e2e"),
    ("H15", "cờ nhẹ không làm CHA nhẹ đi", "co_lot_sang_cha", 'NHE = bool(os.environ.get("DRTH_E2E_NHE")) and bool(os.environ.get("DRTH_KHONG_E2E"))', "NHE = True", "g_dong_tong"),
    ("H2", "dòng tổng đòi N_git ≥ 1", "bo_n_git", " or ng[1] < 1 or mg[1] < 1:", " or mg[1] < 1:", "g_dong_tong"),
    ("H3", "dòng tổng đòi M_git ≥ 1", "bo_m_git", " or ng[1] < 1 or mg[1] < 1:", " or ng[1] < 1:", "g_dong_tong"),
    ("H4", "A9 assert ba tree khác nhau", "bo_assert_cay", '    if len({F["tA"], F["tH"], F["tB"]}) != 3:', "    if False:", "g_fixture"),
    ("H5", "guard A23 tập đọc", "bo_guard", "    if not tinh or tinh != set(dich):", "    if False:", "g_guard"),
    ("H6", "guard vị trí lưu", "bo_gac_luu", "    if not _loose(F, o).is_file() or _co(GOC_KHO, o):", "    if False:", "g_guard"),
    ("H7", "oracle không dùng module/engine git", "oracle_goi_module", '    k, R = F["k"], {**F["R"], **(R or {})}\n\n    def hdr',
     '    k, R = F["k"], {**F["R"], **(R or {})}\n    assert MODUN_GIT\n\n    def hdr', "g_tap_doc"),
    ("H8", "guard kích thước", "bo_gac_tong", '    if max(_kich(F, d[g]) for g in ("G6", "G7", "G8")) >= tran:', "    if False:", "g_guard"),
    ("H10", "bảng ô phủ đủ luật × E", "bo_mot_o", 'O_GIT.update({("G9", "E_ngan_sach"): "g_ns_han", ("G9", "E_troi_ref"): "g_troi"})',
     'O_GIT.update({("G9", "E_ngan_sach"): "g_ns_han"})', "g_o_bang"),
    ("H11", "guard max_object_bytes", "bo_gac_obj", '    if max(len(_raw(F["k"], o[1])[1]) for ds in tap_doc(F).values()', '    if False and max(len(_raw(F["k"], o[1])[1]) for ds in tap_doc(F).values()', "g_guard"),
    ("H12", "guard sự kiện chung", "bo_gac_chung", "    if x not in d[g] or tinh != set(dich):", "    if False:", "g_guard"),
    ("H13", "guard trần phép đi", "bo_gac_walk", '    if {g for g in ("G1", "G2", "G3") if len(d[g]) > gioi} != set(dich):', "    if False:", "g_guard"),
    ("H9", "guard điểm tiêm", "bo_gac_memo", "    if not set(d[\"G4\"] + d[\"G5\"]) <=", "    if False and set(d[\"G4\"] + d[\"G5\"]) <=", "g_guard"),
]


def _ap(nguon, cu, moi):
    cap = list(zip(cu, moi)) if type(cu) is tuple and type(moi) is tuple and len(cu) == len(moi) else [(cu, moi)]
    for c, n in cap:
        if type(c) is not str or type(n) is not str or nguon.count(c) != 1:
            return None
        nguon = nguon.replace(c, n)
    return nguon


def chay_db_git(nguon, dong, suite=False):
    """Disposition TỪ KẾT QUẢ CHẠY như nhóm JSON: `witness_killed` khi ca đích ném `TinHieuChotCa` mang ĐÚNG tên nó."""
    _id, _md, ten, cu, moi, dich, *phu = dong
    gac, ban = (phu[0] if phu else "g_duong"), _ap(nguon, cu, moi)
    if suite:  # bảng đột biến nằm NGAY trong suite: chỉ áp lên phần nguồn ngoài bảng, neo vẫn phải duy nhất
        a, b = nguon.index("# Bảng nghĩa vụ nhóm Git"), nguon.index("\ndef _ap(")
        ban = _ap(nguon[:a] + "\0BANG\0" + nguon[b:], cu, moi)
        ban = ban and ban.replace("\0BANG\0", nguon[a:b])
    if ban is None:
        return "unresolved", "chuoi cu khong duy nhat / khai sai dang"
    with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as t:
        T = pathlib.Path(t)
        for p in (MODUN, MODUN_GIT, GOC / "ci_dang_ky_test.py") if suite else (MODUN,):
            (T / p.name).write_bytes(p.read_bytes())
        p = T / (pathlib.Path(__file__).name if suite else f"dbg_{ten}.py")
        p.write_text(ban, encoding="utf-8")
        try:
            if suite:  # đột biến hạ tầng: nạp BẢN SAO suite, chạy ca của chính bản sao
                ms = _nap(p, f"dbs_{ten}")
                ms.GOC_KHO, run, mm = GOC_KHO, ms.chay_g, _nap(T / MODUN_GIT.name, f"dbs_g_{ten}")
            else:
                run, mm = chay_g, _nap(p, f"dbg_{ten}")
            if dich.startswith("TD:"):
                run(mm, set(CG) - {"g_dong_tong_e2e"})
                return "equivalent_verified", "ca bo ca van xanh"
            if gac:
                run(mm, {gac})
            run(mm, {dich})
            return "unresolved", "song"
        except AssertionError as e:  # lớp `TinHieuChotCa` của bản sao suite là lớp khác: so theo tên lớp
            ok = type(e).__name__ == "TinHieuChotCa" and str(e).startswith(dich + ":")
            return ("witness_killed", "giet") if ok else ("unresolved", f"tin dung gia/qua tay: {str(e)[:150]}")
        except Exception as e:
            return "unresolved", f"tin dung gia: {type(e).__name__}: {str(e)[:150]}"


def nhom_git(mg):
    hc, hd, dem = [], [], dict.fromkeys(("witness_killed", "equivalent_verified", "unresolved"), 0)
    if not _co(GOC_KHO, MOC + "^{commit}"):  # CI có fetch-depth 0; không có nhánh "bỏ qua"
        return (0, 1), (0, 1), [f"KHÔNG ĐO ĐƯỢC: thiếu MOC trong {GOC_KHO!r}"]
    for ten in CG:
        try:
            chay_g(mg, {ten})
        except (TinHieuChotCa, LoiDo) as e:
            hc.append(str(e))
    bang, nguon = ([(d, False) for d in DBG] + [(d, True) for d in DBH if d[5] in CG])[:1 if NHE else None], MODUN_GIT.read_text(encoding="utf-8")
    for dong, suite in bang:
        disp, gc = chay_db_git(pathlib.Path(__file__).read_text(encoding="utf-8") if suite else nguon, dong, suite)
        dem[disp] += 1
        if disp == "unresolved":
            hd.append(f"{dong[0]} {dong[2]}: {gc}")
    ng, mgd = (len(CG) - len(hc), len(CG)), (dem["witness_killed"], len(bang) - dem["equivalent_verified"])
    print(dong_nhom("git", ng, mgd, dem["equivalent_verified"]))
    return ng, mgd, hc + hd


def main():
    mg = _nap(MODUN_GIT, "doc_receipt_thu_hoi_git")  # nạp TRƯỚC mọi nhóm: lỗi nạp ⇒ traceback, KHÔNG có dòng tổng (A18)
    m, hong_ca, hong_db = _nap(MODUN, "doc_receipt_thu_hoi"), [], []
    for c in CA + [("cli",), ("dang_ky",), ("thu_tu_k1",), ("tinh",)]:
        try:
            chay_ca(m, MODUN, {c[0]})
        except (TinHieuChotCa, LoiDo) as e:
            hong_ca.append(str(e))
    nguon, dem, bang = MODUN.read_text(encoding="utf-8"), dict.fromkeys(("witness_killed", "equivalent_verified", "unresolved"), 0), (DB + _theo_truong())[:1 if NHE else None]
    for dong in bang:
        disp, ghi_chu = chay_dot_bien(nguon, dong)
        dem[disp] += 1
        if disp == "unresolved":
            hong_db.append(f"{dong[0]} {dong[2]}: {ghi_chu}")
    n_ca, n_db = len(CA) + 4, len(bang) - dem["equivalent_verified"]
    nj, mj_ = (n_ca - len(hong_ca), n_ca), (dem["witness_killed"], n_db)
    print("nghia vu json: " + " · ".join(f"{k} {v}" for k, v in dem.items()))
    print(dong_nhom("json", nj, mj_, dem["equivalent_verified"]))
    ng, mgd, hong_g = nhom_git(mg)
    for h in hong_ca + hong_db + hong_g:
        print("HONG", h)
    d = dong_tong(nj, mj_, ng, mgd)
    if d:
        print(d)
    return 1 if hong_ca or hong_db or hong_g or d is None else 0


if __name__ == "__main__":
    sys.exit(main())
