#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""sapxep.py (v1.10.1) — Sắp xếp file/folder VBQPPL linh hoạt, KHÔNG bắt buộc đủ mọi bước.

Bước khả dụng (chọn bằng --steps, mặc định: rename,move,register):
  convert   binary (.docx/.doc/.pdf/.html) -> Google Doc (giữ binary làm src cạnh GDoc)
  rename    đổi tên theo chuẩn (tự đề xuất từ tên cũ + phân loại; --name để ép tên)
  move      chuyển vào folder chủ đề (tự phân loại theo linhvuc_phapdien.json; --cat để ép)
  register  reg_upsert (cat, linhvuc, src_id, name...)
  share     cấp anyoneView + trả webViewLink THẬT (đã verify từ Drive API)
  manifest  manifest_export MỘT lần cuối (khi xử lý nhiều file)

Ví dụ:
  sapxep.py --file <id>                              # rename+move+register (auto đề xuất, hỏi nếu không chắc)
  sapxep.py --file <id> --steps rename               # CHỈ đổi tên
  sapxep.py --file <id> --steps move --cat 34        # giữ tên, CHỈ move vào 34
  sapxep.py --file <id> --steps convert,rename,move,register --name Luat_90-2025-QH15_sua_doi_8_luat --cat 46
  sapxep.py --folder <folderId>                      # cả folder: in KẾ HOẠCH bảng -> xác nhận -> chạy
  sapxep.py ... --yes                                # bỏ bước hỏi (chỉ khi mọi phân loại đạt ngưỡng)
  sapxep.py ... --dry                                # chỉ in kế hoạch

Tối ưu RTT: webapp >= 2.13.2 -> 1 call `organize`/file; cũ hơn -> fallback đa-call tự động.
Mặc định luôn DRY trước khi ghi trừ khi --yes; phân loại dưới ngưỡng 0.8 -> HỎI, không xếp âm thầm.
"""
import argparse, json, re, sys, unicodedata, collections, time
from pathlib import Path
HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gas

def _tax():
    for p in (HERE / "linhvuc_phapdien.json", HERE.parent / "references" / "linhvuc_phapdien.json"):
        if p.exists():
            return json.load(open(p, encoding="utf-8"))
    sys.exit("Thiếu linhvuc_phapdien.json")

def _strip(s):
    s = (s or "").replace("Đ", "D").replace("đ", "d")
    s = "".join(c for c in unicodedata.normalize("NFD", s) if unicodedata.category(c) != "Mn")
    return re.sub(r"[_\-./]", " ", s).lower()

def classify(name, tax):
    """-> (code, confidence, lý do). Quy tắc cứng trước, alias-score sau."""
    s = _strip(name)
    if re.search(r"\b(kl|nq|ct)\s?\d+.{0,12}tw\b|bo chinh tri|ban bi thu|van kien|dai hoi dang", s):
        return "00", 0.9, "văn bản Đảng"
    if re.search(r"sua ?doi.{0,40}\d+ ?luat|sua ?\d+ ?luat|suadoi[ _](\w+[ _]){1,6}(dau ?tu|ppp|dau ?thau|quy ?hoach)", s):
        return "46", 0.85, "luật sửa nhiều luật"
    if re.search(r"^cu[ _]|cong uoc|dieu uoc|ilo ?\d+", s):
        return "23", 0.9, "công ước/điều ước"
    if re.search(r"bao hiem xa hoi|bhxh|bao hiem y te|bhyt", s):
        return "02", 0.85, "bảo hiểm"
    scores = collections.Counter()
    for code, v in tax["chude"].items():
        for kw in v.get("alias", []):
            k = _strip(kw)
            if k and k in s:
                scores[code] += 2 if len(k) > 8 else 1
    if not scores:
        return None, 0.0, "không khớp alias nào"
    top = scores.most_common(2)
    if len(top) > 1 and top[0][1] == top[1][1]:
        return None, 0.4, f"hòa điểm {top[0][0]}/{top[1][0]}"
    return top[0][0], (0.85 if top[0][1] >= 3 else 0.7), f"alias {top[0]}"

def suggest_name(name, mime, code):
    """Đề xuất tên chuẩn từ tên cũ (heuristic nhẹ; tên đã chuẩn -> giữ)."""
    base = re.sub(r"\.(docx?|pdf|html?|txt)$", "", name, flags=re.I)
    if re.match(r"^(Luat|BLDS|BLLD|VBHN|ND|NQ|TT|QD|CT|KL|CU)_", base):
        return base  # đã theo convention
    m = re.search(r"(\d+)[_/](\d{4})[_/](QH\d+|ND-CP|TT-\w+|QD-\w+|UBTVQH\d+|VBHN-\w+)", base)
    if m:
        so = f"{m.group(1)}-{m.group(2)}-{m.group(3)}"
        loai = {"QH": "Luat", "ND": "ND", "TT": "TT", "QD": "QD", "UB": "NQ", "VB": "VBHN"}.get(m.group(3)[:2], "VB")
        rest = re.sub(re.escape(m.group(0)), "", base).strip("_- ")
        rest = re.sub(r"[^\w]+", "_", rest).strip("_")
        return f"{loai}_{so}" + (f"_{rest[:40]}" if rest else "")
    return None  # không đề xuất được -> giữ tên / hỏi

def dedup_check(item, reg_rows):
    """3 tầng: (1) số hiệu trong tên khớp registry; (2) md5 khớp; (3) tên trùng. -> (level, đối_chiếu)"""
    import re as _re
    s = item["name"]
    m = _re.search(r"(\d+)[-_](\d{4}|VBHN)[-_]((?:QH|ND|TT|QD|CT|KL|NQ|VPQH|CP|BYT|BGDDT|BTC)[\w-]*)", s)
    so = f"{m.group(1)}-{m.group(2)}-{m.group(3)}".upper() if m else None
    for r in reg_rows:
        if so and r.get("sohieu","").upper() == so and r.get("drive_id") != item["id"]:
            return "SOHIEU", r
        if item.get("md5") and r.get("md5") and item["md5"] == r["md5"] and r.get("drive_id") != item["id"]:
            return "MD5", r
        if r.get("name") == item["name"] and r.get("drive_id") != item["id"]:
            return "NAME", r
    return None, None

def plan_for(item, tax, args):
    name, mime = item["name"], item.get("mime", "")
    steps = args.steps.split(",")
    p = {"id": item["id"], "name_cu": name, "steps": steps}
    binary = mime and "google-apps" not in mime
    p["convert"] = "convert" in steps and binary
    code, conf, why = (args.cat, 1.0, "ép bằng --cat") if args.cat else classify(name, tax)
    p["cat"], p["conf"], p["ly_do"] = code, conf, why
    p["name_moi"] = args.name or (suggest_name(name, mime, code) if "rename" in steps else None)
    p["ask"] = ("move" in steps and (code is None or conf < 0.8)) and not args.cat
    return p

def execute(p, tax, ver, args):
    """Thi hành 1 plan. ver>= (2,13,2): 1 call organize; cũ: fallback đa-call."""
    folder = tax["chude"].get(p["cat"], {}).get("folder", "")
    kw = {}
    if p["convert"]: kw["convert"] = "true"
    if p["name_moi"] and "rename" in p["steps"]: kw["name"] = p["name_moi"]
    if "move" in p["steps"] and p["cat"]: kw["cat"] = p["cat"]; kw["moveSrc"] = "true"
    if "register" in p["steps"]:
        kw["register"] = "true"; kw["linhvuc"] = p["cat"] or ""
        kw["reg_cat"] = folder or (p["cat"] or "")
    if "share" in p["steps"]: kw["share"] = "true"
    if ver >= (2, 13, 2):
        return gas.post("organize", fileId=p["id"], **kw)
    # ---- fallback đa-call (webapp cũ) ----
    out = {"ok": True, "steps": {}}
    fid, src = p["id"], ""
    if p["convert"]:
        r = gas.post("copy_convert", fileId=fid, name=p["name_moi"] or "")
        if not r.get("ok"): return {"ok": False, "step": "convert", "error": r.get("error")}
        src, fid = fid, r["fileId"]; out["steps"]["convert"] = {"gdocId": fid}
    if p["name_moi"] and "rename" in p["steps"]:
        r = gas.post("rename", fileId=fid, name=p["name_moi"])
        out["steps"]["rename"] = {"ok": r.get("ok"), "to": p["name_moi"]}
        if src:
            gas.post("rename", fileId=src, name=p["name_moi"] + ".src")
    if "move" in p["steps"] and p["cat"]:
        cats = gas.get("categories").get("categories", {})
        folderId = cats.get(p["cat"]) or cats.get(folder)
        if not folderId:
            mk = gas.post("mkdir", name=folder); folderId = mk.get("folderId")
        r = gas.post("move", fileId=fid, folderId=folderId, removeFromParent="true")
        out["steps"]["move"] = {"ok": r.get("ok"), "folderId": folderId}
        if src:
            gas.post("move", fileId=src, folderId=folderId, removeFromParent="true")
    if "register" in p["steps"]:
        r = gas.post("reg_upsert", drive_id=fid, cat=folder or (p["cat"] or ""),
                     linhvuc=p["cat"] or "", src_id=src, name=p["name_moi"] or p["name_cu"])
        out["steps"]["register"] = {"ok": r.get("ok")}
    if "share" in p["steps"]:
        gas.post("share", fileId=fid)
        info = gas.get("info", fileId=fid)
        out["steps"]["share"] = {"url": (info.get("file") or {}).get("webViewLink")}
    out["fileId"] = fid
    return out

def main():
    ap = argparse.ArgumentParser()
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--file", help="fileId cần sắp xếp")
    g.add_argument("--folder", help="folderId: sắp xếp mọi file con (không đệ quy)")
    ap.add_argument("--steps", default="rename,move,register",
                    help="convert,rename,move,register,share,manifest — chọn tổ hợp tùy ý")
    ap.add_argument("--name", help="ép tên mới (bỏ qua đề xuất)")
    ap.add_argument("--cat", help="ép mã chủ đề NN (bỏ qua phân loại)")
    ap.add_argument("--dry", action="store_true", help="chỉ in kế hoạch")
    ap.add_argument("--yes", action="store_true", help="không hỏi (chỉ chạy item đạt ngưỡng)")
    ap.add_argument("--force", action="store_true", help="bỏ qua cảnh báo trùng (dùng khi cố ý cập nhật)")
    args = ap.parse_args()
    tax = _tax()
    # contract 2.21.2i có CHỮ CÁI ('i') → split('.') vỡ int(); tách theo NHÓM SỐ rồi lấy 3 phần đầu → (2,21,2)
    ver = tuple(int(x) for x in re.split(r"[^0-9]+", gas.get("ping").get("version", "0.0.0")) if x)[:3]

    items = []
    if args.file:
        f = gas.get("info", fileId=args.file).get("file", {})
        items = [{"id": args.file, "name": f.get("name", ""), "mime": f.get("mimeType", "")}]
    else:
        for it in gas.get("list", folderId=args.folder).get("items", []):
            if it.get("type") != "folder":
                items.append({"id": it["id"], "name": it["name"], "mime": it.get("mime", "")})

    # CỔNG CHECK TRÙNG (bắt buộc trước mọi bước ghi)
    reg = gas.get("reg_get", refresh="true", name_contains="") if False else None
    # đọc toàn bộ qua manifest-lite: dùng find theo từng item rẻ hơn — nhưng chắc nhất là reg đọc 1 lần:
    allrows = []
    try:
        import urllib  # noqa
        mr = gas.get("manifest_export")
        # manifest_export không trả entries -> đọc registry theo lô bằng reg_get từng sohieu là đắt;
        # dùng action find cho từng item (registry-backed, 1 call/item, có cache server)
    except Exception:
        pass
    plans = []
    for it in items:
        lvl, hit = (None, None)
        try:
            fr = gas.get("find", q=it["name"][:40])
            rows = fr.get("rows") or []
            lvl, hit = dedup_check(it, rows)
        except Exception:
            pass
        p = plan_for(it, tax, args)
        if lvl:
            p["ask"] = True
            p["ly_do"] = f"TRÙNG [{lvl}] với registry: {hit.get('name','')[:40]} ({hit.get('drive_id','')[:10]}…) — cần anh quyết (--force để bỏ qua)" if not args.force else p["ly_do"] + " | trùng nhưng --force"
            if args.force: p["ask"] = False
        plans.append(p)
    print(f"{'tên hiện tại':45} {'tên mới':40} {'cat':4} {'conf':5} ghi chú")
    for p in plans:
        print(f"{p['name_cu'][:44]:45} {(p['name_moi'] or '(giữ)')[:39]:40} "
              f"{p['cat'] or '??':4} {p['conf']:.2f}  {'HỎI! ' if p['ask'] else ''}{p['ly_do']}")
    if args.dry:
        return
    todo = [p for p in plans if not p["ask"]]
    skip = [p for p in plans if p["ask"]]
    if skip:
        print(f"\n⚠ {len(skip)} item dưới ngưỡng -> BỎ QUA, cần người dùng quyết (--cat để ép).")
    if not todo:
        return
    if not args.yes:
        print(f"\nSẽ thi hành {len(todo)} item với steps={args.steps}. Chạy lại kèm --yes để xác nhận.")
        return
    t0 = time.monotonic()
    for p in todo:
        r = execute(p, tax, ver, args)
        ok = r.get("ok")
        print(("✓" if ok else "✗"), p["name_moi"] or p["name_cu"],
              f"({r.get('elapsed_ms') or '-'}ms server / {r.get('_client_ms')}ms)",
              "" if ok else r.get("error"))
    if "manifest" in args.steps:
        m = gas.get("manifest_export")
        print("manifest:", {k: m.get(k) for k in ("treeHash", "count")})
    print(f"Xong {len(todo)} item / {time.monotonic()-t0:.1f}s "
          f"({'organize 1-RTT' if ver >= (2,13,2) else 'fallback đa-call — dán v2.13.2 để nhanh hơn'})")

if __name__ == "__main__":
    main()
