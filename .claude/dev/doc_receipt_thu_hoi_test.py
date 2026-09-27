#!/usr/bin/env python3
"""Phản chứng cho `doc_receipt_thu_hoi.py` (C1a1a, #650; spec r5 §5).

Fixture dương = receipt thật PR #589 (artifact `10842182657`, `receipt.json` sha256 `ca67dc6a…`), chép tay, KHÔNG đọc artifact.
Mỗi ca âm là MỘT biến đổi của fixture; oracle là CẢ vectơ năm luật (luật cùng đỏ tất yếu thì khai, K1 đỏ kéo K2–K5 theo M1).
Bảng nghĩa vụ A0 = `DB` + `_theo_truong()`: mỗi dòng một ID mệnh đề M1–M6/M8, một đột biến chạy trên BẢN SAO TẠM, và ca
đích. Disposition tính TỪ KẾT QUẢ CHẠY: `witness_killed` khi ca đích ném `TinHieuChotCa` mang ĐÚNG TÊN nó (mã triển khai
không ném được lớp này), fixture dương vẫn xanh, và ngoại lệ trần (nếu có) đúng loại khai ở cột cuối; `equivalent_verified`
khi dòng khai `TD:` kèm lập luận và CẢ bộ ca vẫn xanh trên đột biến; còn lại `unresolved` (chặn merge).
"""
import importlib.util
import json
import pathlib
import subprocess
import sys
import tempfile

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


def doi(**kv):
    return lambda d: {**d, **kv}


def ma(d):
    return json.dumps(d, ensure_ascii=False, indent=1).encode()


def ca(m, ten, dau_vao, do=(), **tham):
    raw = dau_vao if isinstance(dau_vao, bytes) else ma(dau_vao(FIX))
    try:
        kq = m.kiem_json(raw, **{"kho": KHO, "nhanh": "master", "base_hien_hanh": S, "head_hien_hanh": H, **tham})
    except Exception as e:  # M1: hàm thuần không được ném với MỌI bytes; LOẠI ngoại lệ được so ở phân hạng
        raise TinHieuChotCa(f"{ten}: NEM:{type(e).__name__}") from None
    muon = {k: "do" if k in do or "K1" in do else "qua" for k in ("K1", "K2", "K3", "K4", "K5")}
    if kq["luat"] != muon or kq["ok"] != (not do) or bool(kq["ly_do"]) != bool(do):
        raise TinHieuChotCa(f"{ten}: {kq} != {muon}")


WFK, WFN = WFR.replace(KHO, "other/repo"), WFR[:-6] + "main"
CA = [("duong_fixture", lambda d: d, ()), ("duong_c_khac_s", doi(**dict.fromkeys(C3, X40)), ()),
      ("duong_oid_tai_s_null", doi(oid_bo_kiem_tai_S=None), ()), ("duong_descriptor_hex64", doi(descriptor_q13_ghim=X64), ()),
      ("duong_policy_dict", doi(policy_T={}), ()), ("duong_profile_str", doi(profile_digest="x"), ()),
      ("bom", b"\xef\xbb\xbf" + ma(FIX), ("K1",)), ("khong_phai_json", b"{", ("K1",)), ("goc_null", b"null", ("K1",)),
      ("goc_list_38_khoa", json.dumps(sorted(FIX)).encode(), ("K1",)),
      ("byte_0x80", ma(FIX).replace(b"KHONG_CHAY", b"KHONG\x80CHAY"), ("K1",)), ("thua_khoa", doi(la=1), ("K1",)),
      ("schema_true", doi(schema_version=True), ("K1",)), ("schema_2", doi(schema_version=2), ("K1",)),
      ("event_v2", doi(event="thu_hoi_admission_receipt_v2"), ("K1",)), ("job_id_null", doi(job_id=None), ("K2",)),
      ("c_ca_nhom_39", doi(**dict.fromkeys(C3, S[:39])), ("K2",)), ("gio_hau_to", doi(thoi_diem_utc="2026-09-25T01:25:14Zx"), ("K2",)),
      ("k3_ca_nhom_kho", doi(repository="other/repo", kho_canonical="github.com/other/repo", workflow_ref=WFK), ("K3",)),
      ("k3_ca_nhom_nhanh", doi(nhanh_mac_dinh="main", workflow_ref=WFN), ("K3",)),
      ("k4_base", lambda d: d, ("K4",), {"base_hien_hanh": X40}), ("k4_head", lambda d: d, ("K4",), {"head_hien_hanh": X40}),
      ("k5_rc", doi(checker_rc=1), ("K5",)), ("k5_ket_luan", doi(ket_luan="TAP_THU_HOI_KHAC"), ("K5",)),
      ("k5_che_do", doi(che_do="da_kich_hoat"), ("K5",)), ("a11_k3_k4", doi(repository="other/repo"), ("K3", "K4"), {"base_hien_hanh": X40})]
# ASCII (ensure_ascii) để bytes UTF-16/32 vẫn là UTF-8 hợp lệ: ca phải tới PARSER, không bị decode chặn trước (M2c)
CA += [(f"utf{n}", json.dumps(FIX).encode(f"utf-{n}"), ("K1",)) for n in ("16-le", "16-be", "32-le", "32-be")]
CA += [(f"thieu_{k}", lambda d, k=k: {x: v for x, v in d.items() if x != k}, ("K1",)) for k in FIX]
CA += [(f"kieu_{k}", doi(**{k: v}), CUNG_DO.get(k, ("K2",))) for k, v in SAI.items()]
CA += [(f"c_le_{k}", doi(**{k: X40}), ("K2",)) for k in C3]
CA += [(f"k3_{n}", doi(**{k: v}), ("K3",)) for n, k, v in (
    ("repository", "repository", "other/repo"), ("kho_canonical", "kho_canonical", "github.com/other/repo"),
    ("wf_kho", "workflow_ref", WFK), ("nhanh", "nhanh_mac_dinh", "main"), ("wf_nhanh", "workflow_ref", WFN),
    ("host", "kho_canonical", "evil.example/" + KHO), ("wf_tags", "workflow_ref", WFR.replace("heads", "tags")),
    ("wf_duong", "workflow_ref", WFR.replace("ops-thu-hoi-admission", "untrusted")))]


def ca_cli(ten, path):
    for tham, rc_muon in ((("--receipt", "/khong/co/tep.json"), 2), (("--base-hien-hanh", S[:39]), 2),
                          (("--head-hien-hanh", H[:39]), 2), (("--kho", ""), 2), (("--nhanh-mac-dinh", ""), 2), ((), 0),
                          (("--head-hien-hanh", X40), 12)):
        with tempfile.TemporaryDirectory() as t:
            p = pathlib.Path(t) / "r.json"
            p.write_bytes(ma(FIX))
            a = {"--receipt": str(p), "--kho": KHO, "--nhanh-mac-dinh": "master", "--base-hien-hanh": S, "--head-hien-hanh": H}
            a.update(zip(tham[::2], tham[1::2]))
            r = subprocess.run([sys.executable, "-B", str(path), "kiem-json", *[x for kv in a.items() for x in kv]],
                               capture_output=True, text=True, timeout=60)
        if r.returncode != rc_muon:  # rc đọc thẳng từ subprocess.run, không qua pipe (A12)
            raise TinHieuChotCa(f"{ten}: {tham} rc={r.returncode} != {rc_muon}")
        if rc_muon != 2 and (len(r.stdout.splitlines()) != 1 or json.loads(r.stdout)["ok"] != (rc_muon == 0)):
            raise TinHieuChotCa(f"{ten}: stdout khong phai MOT dong JSON: {r.stdout!r}")


MAU = r'^doc_receipt_thu_hoi tests: ([1-9]\d*)/(\1) ca QUA · ([1-9]\d*)/(\3) dot bien GIET$'


def ca_dang_ky(ten, mau=MAU):
    cdk = _nap(GOC / "ci_dang_ky_test.py", "ci_dang_ky_duoi_test")
    if cdk.MOI.get(".claude/dev/doc_receipt_thu_hoi_test.py") != MAU:
        raise TinHieuChotCa(f"{ten}: MOI khong dang ky dung MAU (M8)")
    for a, b, nhan in (("3/3", "2/2", True), ("3/4", "2/2", False), ("3/3", "1/2", False), ("3/4", "1/2", False),
                       ("0/0", "0/0", False), ("3/3", "0/0", False)):
        if bool(cdk.bang_chung_xanh(f"doc_receipt_thu_hoi tests: {a} ca QUA · {b} dot bien GIET", mau)) != nhan:
            raise TinHieuChotCa(f"{ten}: mau dang ky {a} · {b} phai {'nhan' if nhan else 'bac'}")


def chay_ca(m, path, chi=None):
    for c in CA:
        if chi is None or c[0] in chi:
            ca(m, c[0], c[1], c[2], **(c[3] if len(c) > 3 else {}))
    if chi is None or "cli" in chi:
        ca_cli("cli", path)
    if chi is None or "dang_ky" in chi:
        ca_dang_ky("dang_ky")


# (ID, mệnh đề, tên đột biến, chuỗi cũ, chuỗi mới, ca đích | "TD: lập luận tương đương", ngoại lệ trần được phép)
_Q, _K4 = 'if r[k] != v])', '    ghi("K4"'
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
    ("M2a", "BOM đỏ (chốt riêng)", "bo_chot_bom", 'if raw[:3] == BOM:', 'if False:',
     "TD: json.loads(str) tự bác U+FEFF đầu chuỗi (JSONDecodeError: Unexpected UTF-8 BOM)", None),
    ("M2a'", "BOM đỏ (đột biến ghép)", "bom_ghep", 'if raw[:3] == BOM:\n        loi.append("BOM UTF-8")\n    else:\n'
     '        try:\n            chuoi = raw.decode("utf-8", "strict")', 'if False:\n        pass\n    else:\n        try:\n'
     '            chuoi = raw.decode("utf-8", "strict").lstrip("\\ufeff")', "bom", None),
    ("M2b", "UTF-8 strict", "decode_replace", '"utf-8", "strict"', '"utf-8", "replace"', "byte_0x80", None),
    ("M2b'", "UnicodeDecodeError ⇒ đỏ", "bo_try_decode", 'except UnicodeDecodeError:', 'except ZeroDivisionError:', "byte_0x80", "UnicodeDecodeError"),
    ("M2c", "json.loads nhận str", "loads_bytes", 'json.loads(chuoi)', 'json.loads(raw)', "utf16-le", None),
    ("M2c'", "JSONDecodeError ⇒ đỏ", "bo_try_json", 'except json.JSONDecodeError:', 'except ZeroDivisionError:', "khong_phai_json", "JSONDecodeError"),
    ("M2d", "gốc phải object", "bo_kiem_dict", 'type(r) is not dict:', 'False:', "goc_list_38_khoa", "TypeError"),
    ("M2e", "tập khoá khít: thừa ⇒ đỏ", "khoa_superset", 'if set(r) != KHOA:', 'if not KHOA <= set(r):', "thua_khoa", None),
    ("M2e'", "tập khoá khít: thiếu ⇒ đỏ", "khoa_subset", 'if set(r) != KHOA:', 'if not set(r) <= KHOA:', "thieu_tree_S", "KeyError"),
    ("M2f", "schema_version int không bool", "schema_bo_kieu", 'type(r["schema_version"]) is int and ', '', "schema_true", None),
    ("M2f'", "schema_version == 1", "schema_bo_gia_tri", 'r["schema_version"] == 1)', 'True)', "schema_2", None),
    ("M2g", "event hằng", "bo_event", 'r["event"] != EVENT', 'False', "event_v2", None),
    ("M3a", "hex40 chỉ chữ thường", "hex_hoa", '_khop("[0-9a-f]{40}")', '_khop("[0-9a-fA-F]{40}")', "kieu_T", None),
    ("M3b", "khớp TRỌN chuỗi", "fullmatch_match", 're.fullmatch(mau, v)', 're.match(mau, v)', "kieu_tree_S", None),
    ("M3c", "int không nhận bool", "int_isinstance", 'lambda v: type(v) is int', 'lambda v: isinstance(v, int)', "kieu_job_id", None),
    ("M3d", "job_id không null", "job_id_null", '# 7 khoá', 'KIEU["job_id"] = lambda v: v is None or type(v) is int\n# 7 khoá', "job_id_null", None),
    ("M3e", "hex64 chỉ chữ thường", "hex64_hoa", '_khop("[0-9a-f]{64}")', '_khop("[0-9a-fA-F]{64}")', "kieu_workflow_definition_sha256", None),
    ("M3f", "thoi_diem_utc có chữ T", "gio_bo_T", '[0-9]{2}T[0-9]', '[0-9]{2}.[0-9]', "kieu_thoi_diem_utc", None),
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
    ("M5d", "head lấy từ THAM SỐ", "head_tu_receipt", _K4, '    head_hien_hanh = r["H"]\n' + _K4, "k4_head", None),
    ("M6a", "checker_rc == 0", "bo_rc", 'r["checker_rc"] == 0)', 'True)', "k5_rc", None),
    ("M6b", "ket_luan thuộc tập đóng", "bo_ket_luan", 'r["ket_luan"] in KET_LUAN', 'True', "k5_ket_luan", None),
    ("M6c", "che_do hằng", "bo_che_do", 'r["che_do"] == CHE_DO', 'True', "k5_che_do", None),
    ("M8a", "regex đăng ký buộc cặp ca", "mau_bo_1", r'(\1)', r'(\d+)', "dang_ky", None),
    ("M8b", "regex đăng ký buộc cặp đột biến", "mau_bo_3", r'(\3)', r'(\d+)', "dang_ky", None),
]


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


def chay_dot_bien(nguon, dong):
    _id, _md, ten, cu, moi, dich, nem = dong
    if dich == "dang_ky":  # đột biến M8 đặt lên regex đăng ký, không lên module
        if MAU.count(cu) != 1:
            return "unresolved", "chuoi cu khong duy nhat trong MAU"
        try:
            ca_dang_ky("dang_ky", MAU.replace(cu, moi))
            return "unresolved", "song"
        except TinHieuChotCa as e:
            return ("witness_killed", "giet") if str(e).startswith("dang_ky: mau dang ky") else ("unresolved", f"tin dung gia: {e}")
    if nguon.count(cu) != 1:
        return "unresolved", f"chuoi cu xuat hien {nguon.count(cu)} lan"
    with tempfile.TemporaryDirectory() as t:
        p = pathlib.Path(t) / f"dot_bien_{ten}.py"  # tên riêng từng đột biến, bản sao tạm
        p.write_text(nguon.replace(cu, moi), encoding="utf-8")
        try:
            m = _nap(p, f"db_{ten}")
            if dich.startswith("TD:"):
                chay_ca(m, p)
                return "equivalent_verified", "ca bo ca van xanh"
            if dich != "duong_fixture":
                chay_ca(m, p, {"duong_fixture"})  # A1: đột biến làm fixture dương đỏ là quá tay
            chay_ca(m, p, {dich})
            return "unresolved", "song"
        except TinHieuChotCa as e:
            s = str(e)
            ok = s.startswith(dich + ":") and ("NEM:" not in s or s.endswith(f"NEM:{nem}"))
            return ("witness_killed", "giet") if ok else ("unresolved", f"tin dung gia/qua tay: {s[:100]}")
        except Exception as e:
            return "unresolved", f"tin dung gia: {type(e).__name__}"


def main():
    m, hong_ca, hong_db = _nap(MODUN, "doc_receipt_thu_hoi"), [], []
    for c in CA + [("cli",), ("dang_ky",)]:
        try:
            chay_ca(m, MODUN, {c[0]})
        except TinHieuChotCa as e:
            hong_ca.append(str(e))
    nguon, dem, bang = MODUN.read_text(encoding="utf-8"), dict.fromkeys(("witness_killed", "equivalent_verified", "unresolved"), 0), DB + _theo_truong()
    for dong in bang:
        disp, ghi_chu = chay_dot_bien(nguon, dong)
        dem[disp] += 1
        if disp == "unresolved":
            hong_db.append(f"{dong[0]} {dong[2]}: {ghi_chu}")
    for h in hong_ca + hong_db:
        print("HONG", h)
    n_ca, n_db = len(CA) + 2, len(bang) - dem["equivalent_verified"]
    print("nghia vu: " + " · ".join(f"{k} {v}" for k, v in dem.items()))
    print(f"doc_receipt_thu_hoi tests: {n_ca - len(hong_ca)}/{n_ca} ca QUA · {dem['witness_killed']}/{n_db} dot bien GIET")
    return 1 if hong_ca or hong_db else 0


if __name__ == "__main__":
    sys.exit(main())
