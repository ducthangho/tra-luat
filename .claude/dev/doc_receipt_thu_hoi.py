#!/usr/bin/env python3
"""doc_receipt_thu_hoi.py — C1a1a (#650): kiểm `receipt.json` của workflow `thu-hoi` THUẦN JSON, không git, không mạng.

Đặc tả `ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` revision 5 (sha256 `978058983e8e…`). `ok: true` KHÔNG phải quyền land
và KHÔNG chứng minh provenance: nó chỉ nói receipt đúng hình dạng, kiểu, danh tính kho, độ tươi và kết luận so với THAM SỐ.
Provenance cần C1a1b (đồ thị git: S ≤ C ≤ master, S ≤ H, tree) + C1a2 (join API) + C1b (nối vào `land-packets`).
Hợp đồng caller (spec §8): `--base/--head-hien-hanh` lấy từ readback PR hiện hành, KHÔNG từ receipt; ở đây không kiểm được.
ADR-0066 (packet THU-HOI-ADMISSION-MERGE-BASE-B r13 mục tiêu 7): nhận receipt v1 (38 khoá) VÀ v2 (41 khoá: thêm
`quan_he_S_H`, `merge_bases`, `vung_tai_S`), mỗi phiên bản một tập khoá đóng riêng, chọn theo `schema_version`.
"""
import argparse
import json
import re
import sys

BOM = b"\xef\xbb\xbf"
EVENT, CHE_DO = "thu_hoi_admission_receipt", "chua_kich_hoat"
KET_LUAN = ("TAP_THU_HOI_RONG",)  # tuple: `in` so bằng ==, list/dict trong JSON không ném TypeError (luot1 F1)
WF = "/.github/workflows/ops-thu-hoi-admission.yml@refs/heads/"
C = ("checkout_commit", "bo_kiem_da_chay_commit", "workflow_definition_commit")
_VANG = object()  # `json.loads("null")` trả None, nên None không dùng làm dấu "chưa parse" được


def _khop(mau):
    return lambda v: type(v) is str and re.fullmatch(mau, v) is not None


_H40, _H64 = _khop("[0-9a-f]{40}"), _khop("[0-9a-f]{64}")
_GIO = r"\d{4}-\d\d-\d\dT\d\d:\d\d:\d\dZ"  # đúng regex spec M3 (`\d`), luot1 F11
KIEU = {k: _H40 for k in ("S", "H", "T", "tree_S", "oid_bo_kiem_da_chay", "workflow_definition_blob") + C}
KIEU.update({k: lambda v: type(v) is int for k in (  # `type is int` loại luôn bool
    "schema_version", "canh_ancestry", "so_object_da_doc", "tong_bytes", "pull_request", "run_id", "run_attempt",
    "check_run_id", "job_id", "checker_rc")})
KIEU.update({k: lambda v: type(v) is dict for k in ("so_thu_hoi_S", "so_thu_hoi_T", "ngan_sach")})
KIEU.update({k: lambda v: type(v) is list for k in ("metadata_T", "thu_hoi_moi")})
KIEU.update({
    "oid_bo_kiem_tai_S": lambda v: v is None or _H40(v), "workflow_definition_sha256": _H64,
    "thoi_diem_utc": _khop(_GIO),
    "descriptor_q13_ghim": lambda v: v is None or _H64(v), "policy_T": lambda v: v is None or type(v) is dict,
    "profile_digest": lambda v: v is None or type(v) is str, "discovery": lambda v: type(v) is str})
# ADR-0066: v2 phát `canh_ancestry = null` ở chế độ `merge_base`; v1 vẫn đòi số nguyên (luật null riêng ở K2).
KIEU["canh_ancestry"] = lambda v: v is None or type(v) is int
# 7 khoá còn lại kiểm theo GIÁ TRỊ: event (K1) · 4 danh tính (K3) · che_do, ket_luan (K5).
KHOA = frozenset(KIEU) | {"event", "repository", "kho_canonical", "nhanh_mac_dinh", "workflow_ref", "che_do", "ket_luan"}
assert len(KHOA) == 38
QUAN_HE = ("to_tien", "merge_base")
_MODE, _LOAI = ("100644", "100755", "120000", "160000", "040000"), ("blob", "tree", "commit")


def _muc_vung(x):
    return type(x) is list and len(x) == 3 and x[0] in _MODE and x[1] in _LOAI and _H40(x[2])


KIEU2 = {  # ba khoá CHỈ có ở v2; quan hệ giữa chúng kiểm ở K2 sau khi kiểu đã đúng
    "quan_he_S_H": lambda v: type(v) is str and v in QUAN_HE,
    "merge_bases": lambda v: type(v) is list and len(v) > 0 and all(_H40(x) for x in v) and v == sorted(v) and len(set(v)) == len(v),
    "vung_tai_S": lambda v: v is None or (type(v) is dict and all(type(k) is str and _muc_vung(x) for k, x in v.items())),
}
# KIEU2: hết
KHOA_V2 = KHOA | frozenset(KIEU2)
assert len(KHOA_V2) == 41


def kiem_json(raw, *, kho, nhanh, base_hien_hanh, head_hien_hanh):
    luat, ly_do = {}, []

    def ghi(k, loi):
        luat[k] = "do" if loi else "qua"
        ly_do.extend(f"{k}: {x}" for x in loi)

    loi, r = [], _VANG
    if raw[:3] == BOM:
        loi.append("BOM UTF-8")
    else:
        try:
            chuoi = raw.decode("utf-8", "strict")
            # nhận `str`, KHÔNG nhận bytes: overload bytes tự nhận UTF-16/32
            r = json.loads(chuoi)
        except UnicodeDecodeError:
            loi.append("khong phai UTF-8 strict")
        except json.JSONDecodeError:
            loi.append("khong phai JSON")
        except (ValueError, RecursionError):  # số nguyên vượt int_max_str_digits / lồng quá sâu: fail-close (chủ kho, luot2 F23)
            loi.append("parser tu choi: so nguyen qua dai hoac long qua sau")
        if r is not _VANG and type(r) is not dict:
            loi.append("goc khong phai object")
        elif r is not _VANG:
            phien = r.get("schema_version") if type(r.get("schema_version")) is int else None
            khoa = KHOA_V2 if phien == 2 else KHOA
            if set(r) != khoa:
                loi.append(f"tap khoa lech: thieu {sorted(khoa - set(r))} thua {sorted(set(r) - khoa)}")
            elif not (type(r["schema_version"]) is int and r["schema_version"] in (1, 2)):
                loi.append("schema_version khac 1 va 2")
            elif r["event"] != EVENT:
                loi.append("event la")
    ghi("K1", loi)
    if loi:
        for k in ("K2", "K3", "K4", "K5"):
            ghi(k, ["K1 do"])
        return {"ok": False, "luat": luat, "ly_do": ly_do}

    loi = [f"{k} sai kieu" for k in sorted(KIEU) if not KIEU[k](r[k])]
    if not (r[C[0]] == r[C[1]] and r[C[1]] == r[C[2]]):
        loi.append("ba truong C khong bang nhau")
    if r["schema_version"] == 1 and r["canh_ancestry"] is None:
        loi.append("canh_ancestry null o v1")
    if r["schema_version"] == 2:
        loi2 = [f"{k} sai kieu" for k in sorted(KIEU2) if not KIEU2[k](r[k])]
        loi += loi2
        qh, mb, canh, vung = r["quan_he_S_H"], r["merge_bases"], r["canh_ancestry"], r["vung_tai_S"]
        if not loi2 and qh == "to_tien":
            loi += ["to_tien: merge_bases phai [S]"] * (mb != [r["S"]])
            loi += ["to_tien: canh_ancestry phai so"] * (canh is None)
            loi += ["to_tien: canh_ancestry am"] * (type(canh) is int and canh < 0)
            loi += ["to_tien: vung_tai_S phai null"] * (vung is not None)
        if not loi2 and qh == "merge_base":
            loi += ["merge_base: canh_ancestry phai null"] * (canh is not None)
            loi += ["merge_base: S nam trong merge_bases"] * (r["S"] in mb)
            loi += ["merge_base: vung_tai_S phai dict"] * (vung is None)
    ghi("K2", loi)
    ghi("K3", [f"{k} lech" for k, v in (("repository", kho), ("kho_canonical", "github.com/" + kho),
                                         ("nhanh_mac_dinh", nhanh), ("workflow_ref", kho + WF + nhanh)) if r[k] != v])
    ghi("K4", [f"{k} stale, chay lai" for k, v in (("S", base_hien_hanh), ("H", head_hien_hanh)) if v != r[k]])
    ghi("K5", [f"{k} la" for k, dat in (("checker_rc", r["checker_rc"] == 0), ("ket_luan", r["ket_luan"] in KET_LUAN),
                                        ("che_do", r["che_do"] == CHE_DO)) if not dat])
    return {"ok": all(v == "qua" for v in luat.values()), "luat": luat, "ly_do": ly_do}


def main(argv=None):
    p = argparse.ArgumentParser(prog="doc_receipt_thu_hoi.py")
    k = p.add_subparsers(dest="lenh", required=True).add_parser("kiem-json")
    for ten in ("--receipt", "--kho", "--nhanh-mac-dinh", "--base-hien-hanh", "--head-hien-hanh"):
        k.add_argument(ten, required=True)
    a = p.parse_args(argv)
    if not all((a.kho, a.nhanh_mac_dinh, a.base_hien_hanh, a.head_hien_hanh)):
        p.error("tham so rong")
    if not (_H40(a.base_hien_hanh) and _H40(a.head_hien_hanh)):
        p.error("--base/--head-hien-hanh phai la hex thuong 40 ky tu")
    try:
        with open(a.receipt, "rb") as f:
            raw = f.read()
    except OSError as e:
        print(f"khong doc duoc receipt: {e}", file=sys.stderr)
        return 2
    kq = kiem_json(raw, kho=a.kho, nhanh=a.nhanh_mac_dinh, base_hien_hanh=a.base_hien_hanh, head_hien_hanh=a.head_hien_hanh)
    print(json.dumps(kq, ensure_ascii=True, sort_keys=True))
    return 0 if kq["ok"] else 12


if __name__ == "__main__":
    sys.exit(main())
