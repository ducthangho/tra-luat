# NGUYEN MAU do kich thuoc — KHONG phai ma giao nop. Mat do dong theo kieu packet_loop.py.
import hashlib, json, re, sys
from pathlib import Path
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")
HANG_LOP = ("P0", "P1", "P2", "P3")
RC_OK, RC_ARG, RC_BIEN_NHAN = 0, 2, 11
VERDICT_SCHEMA_TEP = ".github/coordination/schemas/review_verdict.v2.schema.json"
VERDICT_RAO = re.compile(r"(?m)^```json review_verdict\.v2\n(.*?)^```[ \t]*$", re.S)
NHAN_DA_VA = "ĐÃ VÁ THẬT"


class VerdictHong(ValueError):
    pass


def _cam_khoa_trung(cap):
    d = {}
    for k, v in cap:
        if k in d:
            raise ValueError(f"khoá trùng {k!r}")
        d[k] = v
    return d


def _khoi_verdict(van_ban: str) -> dict:
    """ĐÚNG MỘT khối rào `json review_verdict.v2` trong đầu ra của lượt review; JSON nghiêm (khoá trùng, hằng ngoài JSON ⇒ từ chối)."""
    khoi = VERDICT_RAO.findall(van_ban)
    if len(khoi) != 1:
        raise VerdictHong(f"cần ĐÚNG MỘT khối `json review_verdict.v2`, thấy {len(khoi)}")
    try:
        return json.JSONDecoder(parse_constant=lambda c: (_ for _ in ()).throw(ValueError(c)), object_pairs_hook=_cam_khoa_trung).decode(khoi[0])
    except (ValueError, RecursionError) as ex:
        raise VerdictHong(f"khối verdict không phải JSON nghiêm: {type(ex).__name__}") from None


def _kiem_verdict_lop(d, root: Path, *, doi_tuong: str, reviewed_sha: str, sha256=None, packet_id=None, generation=None) -> dict:
    """ADR-0068 — §8.3 cho MỌI lượt review: lược đồ v2 (nguồn duy nhất là tệp schema) + các ràng buộc chéo mà JSON Schema không nói được."""
    try:
        import jsonschema
        luoc_do = json.loads((root / VERDICT_SCHEMA_TEP).read_text(encoding="utf-8"))
        sai = sorted(jsonschema.Draft202012Validator(luoc_do).iter_errors(d), key=lambda e: list(e.absolute_path))
    except Exception as ex:  # noqa: BLE001 — thiếu gói/tệp/schema hỏng đều là KHÔNG ĐO ĐƯỢC, không phải đạt
        raise VerdictHong(f"KHÔNG ĐO ĐƯỢC: lược đồ verdict v2: {type(ex).__name__}") from None
    if sai:
        raise VerdictHong(f"sai lược đồ v2 tại {['/'.join(map(str, e.absolute_path)) or '<gốc>' for e in sai[:5]]}")
    fs, lop, dc = d["findings"], d["bang_lop"], d["doi_chieu_luot_truoc"]
    theo_slug = {x["slug"]: x for x in lop}
    thu_tu = HANG_LOP.index
    loi = [ten for ten, dung in (
        ("doi_tuong", d["doi_tuong"] == doi_tuong and d["doi_tuong_sha256"] == sha256), ("reviewed_sha", d["reviewed_sha"] == reviewed_sha),
        ("packet", packet_id is None or d["packet_id"] == packet_id), ("generation", generation is None or d["generation"] == generation),
        ("lop-trung", len(theo_slug) == len(lop)),
        ("finding-trung", len({f["finding_id"] for f in fs}) == len(fs)),
        ("finding-ngoai-bang", all(f["class_slug"] in theo_slug and f["finding_id"] in theo_slug[f["class_slug"]]["finding_ids"] for f in fs)),
        ("lop-khong-finding", all(any(f["class_slug"] == s for f in fs) for s in theo_slug)),
        ("hang-lop", all(x["hang"] == min((f["severity"] for f in fs if f["class_slug"] == s), key=thu_tu, default=None) for s, x in theo_slug.items())),
        ("approve-con-P0-P2", d["verdict"] != "approve" or not any(x["hang"] in HANG_LOP[:3] for x in lop)),
        ("am-khong-finding", d["verdict"] != "changes_requested" or bool(fs)),
        ("doi-chieu-trung", len({x["finding_id"] for x in dc}) == len(dc)),
        ("doi-chieu-chua-dong", all(x["nhan"] == NHAN_DA_VA or x["class_slug"] in theo_slug for x in dc)),
        ("hoi-tu", d["luot"] == 1 or (set(d["hoi_tu"]["F"]) <= set(d["hoi_tu"]["U"]) == {x["class_slug"] for x in dc}
                                      and set(d["hoi_tu"]["F"]) == {s for s in d["hoi_tu"]["U"] if all(x["nhan"] == NHAN_DA_VA for x in dc if x["class_slug"] == s) and s not in theo_slug})),
    ) if not dung]
    if loi:
        raise VerdictHong(f"verdict không đạt §8.3: {loi}")
    return {"lop": lop, "p3": sorted(x["slug"] for x in lop if x["hang"] == "P3"), "luot": d["luot"]}


def cmd_kiem_verdict(a) -> int:
    """Không state. Buộc run.json ↔ stdout như K4, rồi kiểm khối verdict; in MỘT dòng bằng chứng dương."""
    try:
        r = json.loads(Path(a.run_json).read_text(encoding="utf-8"))
        out = Path(a.stdout).read_bytes()
        if not (isinstance(r, dict) and r.get("trang_thai") == "xong" and type(r.get("ma_thoat")) is int and r["ma_thoat"] == 0
                and r.get("head") == a.reviewed_sha and r.get("stdout_sha256") == hashlib.sha256(out).hexdigest()):
            raise VerdictHong("run.json không buộc được với stdout/head (trang_thai, ma_thoat, head, stdout_sha256)")
        kq = _kiem_verdict_lop(_khoi_verdict(out.decode("utf-8")), Path(a.root), doi_tuong=a.doi_tuong, reviewed_sha=a.reviewed_sha, sha256=a.sha256)
    except (OSError, ValueError) as ex:
        print(f"CHAN [{RC_BIEN_NHAN}]: {ex}", file=sys.stderr)
        return RC_BIEN_NHAN
    print(f"VERDICT_HOP_LE stdout_sha256={r['stdout_sha256']} doi_tuong={a.doi_tuong} luot={kq['luot']} lop={len(kq['lop'])} p3={','.join(kq['p3']) or '-'}")
    return RC_OK
