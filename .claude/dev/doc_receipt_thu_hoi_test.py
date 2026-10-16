#!/usr/bin/env python3
"""Phản chứng cho `doc_receipt_thu_hoi.py` (C1a1a, #650; spec r5 §5).

Fixture dương = receipt thật PR #589 (artifact `10842182657`, `receipt.json` sha256 `ca67dc6a…`), chép tay, KHÔNG đọc artifact.
Mỗi ca âm là MỘT biến đổi của fixture; oracle là CẢ vectơ năm luật (luật cùng đỏ tất yếu thì khai, K1 đỏ kéo K2–K5 theo M1).
Bảng nghĩa vụ A0 = `DB` + `_theo_truong()`: mỗi dòng một ID mệnh đề M1–M6/M8, một đột biến chạy trên BẢN SAO TẠM, và ca
đích. Disposition tính TỪ KẾT QUẢ CHẠY: `witness_killed` khi ca đích ném `TinHieuChotCa` mang ĐÚNG TÊN nó (mã triển khai
không ném được lớp này), fixture dương vẫn xanh, và ngoại lệ trần (nếu có) đúng loại khai ở cột cuối; `equivalent_verified`
khi dòng khai `TD:` kèm lập luận và CẢ bộ ca vẫn xanh trên đột biến; còn lại `unresolved` (chặn merge).
"""
import ast
import importlib.util
import json
import os
import pathlib
import re
import subprocess
import sys
import tempfile
import traceback

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
    ("M1s9", "không posix_spawn (F29)", "posix_spawn", _DAU, _DAU + '\n    __import__("os").posix_spawn(sys.executable, [sys.executable, "-c", "pass"], {})', "tinh", None),
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


def main():
    m, hong_ca, hong_db = _nap(MODUN, "doc_receipt_thu_hoi"), [], []
    for c in CA + [("cli",), ("dang_ky",), ("thu_tu_k1",), ("tinh",)]:
        try:
            chay_ca(m, MODUN, {c[0]})
        except (TinHieuChotCa, LoiDo) as e:
            hong_ca.append(str(e))
    nguon, dem, bang = MODUN.read_text(encoding="utf-8"), dict.fromkeys(("witness_killed", "equivalent_verified", "unresolved"), 0), DB + _theo_truong()
    for dong in bang:
        disp, ghi_chu = chay_dot_bien(nguon, dong)
        dem[disp] += 1
        if disp == "unresolved":
            hong_db.append(f"{dong[0]} {dong[2]}: {ghi_chu}")
    for h in hong_ca + hong_db:
        print("HONG", h)
    n_ca, n_db = len(CA) + 4, len(bang) - dem["equivalent_verified"]
    print("nghia vu: " + " · ".join(f"{k} {v}" for k, v in dem.items()))
    print(f"doc_receipt_thu_hoi tests: {n_ca - len(hong_ca)}/{n_ca} ca QUA · {dem['witness_killed']}/{n_db} dot bien GIET")
    return 1 if hong_ca or hong_db else 0


if __name__ == "__main__":
    sys.exit(main())
