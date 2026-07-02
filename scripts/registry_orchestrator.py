#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""registry_orchestrator.py (v1.12.0) — ĐIỀU PHỐI TỰ ĐỘNG sổ cái registry.

Quyết định KHI NÀO chạy `regen2`, `reg_bulk`, `changes_pull`, `manifest_export`
để Claude khỏi phải hỏi/đoán mỗi phiên. Triết lý GIỮ NGUYÊN của skill:
  «kiểm RẺ chạy LUÔN, kiểm ĐẮT chỉ khi nghi vấn» — happy path < vài giây.

Vai trò 4 action (nhắc lại để rõ, không đổi):
  regen2         = dựng lại CẤU TRÚC sheet từ Drive (files.list OR-parents) — GIỮ cột nlm_*.
  changes_pull   = giữ Sheet TƯƠI bằng DELTA rẻ (Drive changes token) — KHÔNG quét toàn bộ.
  reg_bulk       = điền cột CURATE hàng loạt (mặc định nlm_title) trong 1 read+write.
  manifest_export= CHỤP ẢNH Sheet → JSON snapshot + treeHash (fallback offline + L2 cache).
Nói gọn: regen2 lo cấu trúc → reg_bulk điền curate → changes_pull giữ tươi → manifest_export chụp ảnh.

CHẾ ĐỘ:
  boot     — chạy NGAY khi tra-luat load / lần đầu chạm registry trong phiên.
  end      — cuối phiên (chốt sổ).
  --dry    — chỉ IN KẾ HOẠCH, không gọi action ghi.
  --apply  — thực thi phần script tự làm được (changes_pull/regen2/manifest_export).
             reg_bulk cần dump notebook_get (MCP) ⇒ in lệnh backfill_nlm_title.py để Claude chạy tiếp.
  --selftest — kiểm thử hàm quyết định thuần (offline, không mạng).

ĐẦU VÀO phụ:
  --manifest PATH  tra_luat_manifest.json đã tải về (để đếm khoảng trống curate).
  --regen-threshold N (mặc 40)  delta changes_pull > N ⇒ leo thang regen2.
  --bulk-threshold  N (mặc 8)   số dòng thiếu nlm_title ≥ N ⇒ đề xuất reg_bulk.
  --min-version V  (mặc 2.13.7) webapp tối thiểu có reg_bulk.

MÔI TRƯỜNG: TL_WEBAPP, TL_TOKEN (đọc từ tra_luat_config.json — ngoại lệ DUY NHẤT dùng MCP).
KHÔNG dùng Google Drive MCP cho thao tác registry.
"""
import os, sys, json, argparse

# ───────────────────────── LÕI QUYẾT ĐỊNH THUẦN (test offline) ─────────────────────────

def _ver_ge(v, ref):
    """So phiên bản kiểu '2.13.7' >= '2.13.7'. Chuỗi rỗng/None ⇒ False."""
    def parts(s):
        out = []
        for tok in str(s or "").split("."):
            num = "".join(ch for ch in tok if ch.isdigit())
            out.append(int(num) if num else 0)
        return out
    a, b = parts(v), parts(ref)
    n = max(len(a), len(b))
    a += [0] * (n - len(a)); b += [0] * (n - len(b))
    return a >= b


def decide(version, changes_state, delta_count, curate_gap, *,
           min_version="2.13.7", regen_threshold=40, bulk_threshold=8,
           tukhoa_gap=None, tukhoa_threshold=8, phase="boot", end_regen=False):
    """Trả {plan:[action...], has_reg_bulk:bool, reasons:[...]}.

    changes_state ∈ {'ok','no_baseline','unsupported','error'}.
    delta_count   = số file đổi mà changes_pull đã vá (None nếu không rõ).
    curate_gap    = số dòng có nlm_source_id nhưng THIẾU nlm_title (None nếu chưa biết).
    tukhoa_gap    = số doc GDoc on-NLM thiếu `tukhoa`, ĐÃ loại orphan (None nếu chưa biết). (v1.15.0)
    phase='end' + end_regen: cuối phiên chỉ regen2 khi phiên ĐỤNG cấu trúc Drive; nếu không ⇒ chỉ export.
    """
    plan, reasons = [], []
    has_reg_bulk = _ver_ge(version, min_version)

    # 1) ĐỘ TƯƠI CẤU TRÚC ── ưu tiên rẻ (changes_pull); chỉ leo thang regen2 khi cần.
    if phase == "end":
        # CHỐT SỔ: nguồn chân lý từ Drive. KHÔNG chèn changes_init (đó là việc của BOOT).
        if end_regen:
            plan.append("regen2")
            reasons.append("Cuối phiên + có thay đổi cấu trúc Drive (--touched-drive) ⇒ regen2 đối soát nguồn chân lý.")
        else:
            reasons.append("Cuối phiên, KHÔNG đụng cấu trúc Drive ⇒ bỏ regen2 (~25s no-op), chỉ manifest_export.")
    elif changes_state in ("no_baseline", "unsupported", "error"):
        plan += ["regen2", "changes_init"]
        reasons.append("Chưa có baseline changes (token trống/không hỗ trợ) ⇒ regen2 1 lần dựng nền + changes_init.")
    elif changes_state == "ok":
        if delta_count is not None and delta_count > regen_threshold:
            plan.append("regen2")
            reasons.append(f"changes_pull báo delta lớn ({delta_count} > {regen_threshold}) ⇒ regen2 dựng lại cho chắc.")
        else:
            d = "?" if delta_count is None else delta_count
            reasons.append(f"changes_pull đã vá Sheet tươi (delta {d}) ⇒ KHỎI regen2.")

    # 2) KHOẢNG TRỐNG CURATE nlm_title ── chỉ reg_bulk khi đủ NHIỀU dòng cùng cột.
    if curate_gap is None:
        reasons.append("Chưa biết gap nlm_title (thiếu --manifest) ⇒ nếu vừa nạp lô lớn: cân nhắc backfill_nlm_title --manifest.")
    elif curate_gap >= bulk_threshold:
        if has_reg_bulk:
            plan.append("reg_bulk")
            reasons.append(f"{curate_gap} dòng thiếu nlm_title (≥ {bulk_threshold}) ⇒ reg_bulk backfill 1 lần (KHÔNG lặp reg_upsert).")
        else:
            reasons.append(f"{curate_gap} dòng thiếu nlm_title nhưng webapp < {min_version} ⇒ nâng cấp webapp mới có reg_bulk.")
    else:
        reasons.append(f"Chỉ {curate_gap} dòng thiếu nlm_title (< {bulk_threshold}) ⇒ KHỎI reg_bulk; lẻ thì map_set/reg_upsert.")

    # 2b) KHOẢNG TRỐNG TUKHOA ── móc chủ đề (v1.13.4); backfill khi đủ nhiều doc thiếu. (v1.15.0)
    if tukhoa_gap is None:
        reasons.append("Chưa biết gap tukhoa (thiếu --manifest) ⇒ bỏ qua kiểm tukhoa.")
    elif tukhoa_gap >= tukhoa_threshold:
        plan.append("backfill_keywords_live")
        reasons.append(f"{tukhoa_gap} doc on-NLM thiếu tukhoa (≥ {tukhoa_threshold}) ⇒ backfill_keywords_live (bóc heading server-side, KHÔNG AI).")
    elif tukhoa_gap:
        reasons.append(f"Chỉ {tukhoa_gap} doc thiếu tukhoa (< {tukhoa_threshold}) ⇒ KHỎI backfill (thường là orphan removed_from_drive).")

    # 3) CHỤP ẢNH ── sau bất kỳ ghi nào (regen2/reg_bulk/backfill) HOẶC luôn ở cuối phiên.
    if phase == "end" or any(p in plan for p in ("regen2", "reg_bulk", "backfill_keywords_live")):
        plan.append("manifest_export")

    return {"plan": plan, "has_reg_bulk": has_reg_bulk, "reasons": reasons}


# ───────────────────────── I/O: gom tín hiệu + (tùy chọn) thực thi ─────────────────────────

def _parse_changes(res):
    """Đọc kết quả changes_pull một cách phòng thủ (shape webapp có thể khác)."""
    if not isinstance(res, dict):
        return "error", None
    if res.get("error"):
        msg = str(res.get("error")).lower()
        if any(k in msg for k in ("token", "init", "baseline", "chưa")):
            return "no_baseline", None
        return "error", None
    if res.get("ok") is False:
        return "error", None
    if res.get("needs_init") or res.get("no_token"):
        return "no_baseline", None
    # đếm delta từ nhiều khả năng tên trường
    delta = res.get("delta") if isinstance(res.get("delta"), dict) else None
    if delta is not None:
        cnt = sum(len(delta.get(k, []) or []) if isinstance(delta.get(k), list) else int(delta.get(k) or 0)
                  for k in ("added", "renamed", "moved", "removed", "changed"))
        return "ok", cnt
    for k in ("changed", "count", "patched", "applied"):
        if isinstance(res.get(k), int):
            return "ok", res.get(k)
    return "ok", None


def _curate_gap_from_manifest(path):
    """Đếm dòng có nlm_source_id nhưng THIẾU nlm_title từ manifest đã tải về."""
    try:
        m = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"[orch] không đọc được manifest {path}: {e}", file=sys.stderr)
        return None
    ents = m.get("entries", m) if isinstance(m, dict) else m
    gap = 0
    for e in ents or []:
        if not isinstance(e, dict):
            continue
        if e.get("nlm_source_id") and not (e.get("nlm_title") or "").strip():
            gap += 1
    return gap


_GDOC_MIME = "application/vnd.google-apps.document"


def _tukhoa_gap_from_manifest(path):
    """Đếm doc GDoc on-NLM thiếu `tukhoa`, ĐÃ loại orphan removed_from_drive (v1.15.0).

    Chỉ GDoc mới export-text để bóc heading; orphan đã rời Drive không backfill được
    (đó là việc DỌN, không phải backfill) ⇒ không tính vào gap để khỏi kích hoạt nhầm.
    """
    try:
        m = json.load(open(path, encoding="utf-8"))
    except Exception as e:
        print(f"[orch] không đọc được manifest {path}: {e}", file=sys.stderr)
        return None
    ents = m.get("entries", m) if isinstance(m, dict) else m
    gap = 0
    for e in ents or []:
        if not isinstance(e, dict):
            continue
        if (e.get("nlm_source_id")
                and (e.get("mime") or "") == _GDOC_MIME
                and (e.get("nlm_status") or "") != "removed_from_drive"
                and not (e.get("tukhoa") or "").strip()):
            gap += 1
    return gap


def run(args):
    sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
    import gas  # client webapp (get/post) — KHÔNG dùng Drive MCP

    ping = gas.get("ping")
    version = str(ping.get("version", ""))
    print(f"[orch] webapp version = {version}")

    changes_state, delta_count = "error", None
    if args.phase == "boot":
        # changes_pull rẻ: vá Sheet tươi (mặc định applySheet=true).
        try:
            res = gas.post("changes_pull")
            changes_state, delta_count = _parse_changes(res)
            print(f"[orch] changes_pull → state={changes_state} delta={delta_count}")
        except Exception as e:
            print(f"[orch] changes_pull lỗi: {e} → coi như error", file=sys.stderr)
    else:  # end: chốt sổ — decide() nhánh 'end' tự lo; KHÔNG changes_pull, KHÔNG changes_init.
        print(f"[orch] phase=end → regen2 {'CÓ' if args.touched_drive else 'BỎ (không đụng Drive)'}; rồi manifest_export")

    curate_gap = _curate_gap_from_manifest(args.manifest) if args.manifest else None
    tukhoa_gap = _tukhoa_gap_from_manifest(args.manifest) if args.manifest else None

    d = decide(version, changes_state, delta_count, curate_gap,
               min_version=args.min_version, regen_threshold=args.regen_threshold,
               bulk_threshold=args.bulk_threshold, tukhoa_gap=tukhoa_gap,
               tukhoa_threshold=args.tukhoa_threshold,
               phase=args.phase, end_regen=args.touched_drive)

    print("\n=== KẾ HOẠCH ĐIỀU PHỐI (" + args.phase + ") ===")
    print("plan:", " → ".join(d["plan"]) or "(không cần làm gì)")
    for r in d["reasons"]:
        print("  •", r)

    if args.dry or not args.apply:
        if "reg_bulk" in d["plan"]:
            print("\n[orch] backfill nlm_title (an toàn, KHÔNG cần dump NLM) → chạy:")
            print(f"       python scripts/backfill_nlm_title.py --manifest {args.manifest or 'tra_luat_manifest.json'} --export")
        if "backfill_keywords_live" in d["plan"]:
            print("\n[orch] backfill tukhoa (bóc heading server-side, lặp tới con_lai=0) → chạy:")
            print(f"       python scripts/backfill_keywords_live.py --manifest {args.manifest or 'tra_luat_manifest.json'} --budget 200 --batch 40")
        if {"regen2", "manifest_export"} <= set(d["plan"]):
            print("\n[orch] (gộp regen2+export 1 lệnh: python scripts/manifest_build.py)")
        print("\n[orch] (chế độ DRY — không gọi action ghi; thêm --apply để thực thi)")
        return d

    # --apply: thực thi phần script tự làm được; backfill để Claude/script riêng chạy.
    for act in d["plan"]:
        if act == "reg_bulk":
            print(f"[orch] BỎ QUA reg_bulk ở đây — chạy: python scripts/backfill_nlm_title.py "
                  f"--manifest {args.manifest or 'tra_luat_manifest.json'} --export")
            continue
        if act == "backfill_keywords_live":
            print(f"[orch] BỎ QUA backfill_keywords_live ở đây — chạy: python scripts/backfill_keywords_live.py "
                  f"--manifest {args.manifest or 'tra_luat_manifest.json'} --budget 200 --batch 40")
            continue
        if act in ("regen2",):
            print(f"[orch] → {act} confirm=yes ...")
            print("       ", json.dumps(gas.post(act, confirm="yes"), ensure_ascii=False)[:200])
        else:
            print(f"[orch] → {act} ...")
            print("       ", json.dumps(gas.post(act), ensure_ascii=False)[:200])
    return d


# ───────────────────────── SELF-TEST (offline) ─────────────────────────

def selftest():
    cases = []
    def chk(name, got, want):
        ok = got == want
        cases.append((name, ok, got, want))

    # 1) chưa baseline ⇒ regen2 + changes_init + manifest_export, có reg_bulk theo version
    d = decide("2.13.7", "no_baseline", None, 0)
    chk("no_baseline_plan", d["plan"], ["regen2", "changes_init", "manifest_export"])

    # 2) ok + delta nhỏ + gap nhỏ ⇒ plan rỗng
    d = decide("2.13.7", "ok", 3, 0)
    chk("clean_noop", d["plan"], [])

    # 3) ok + delta lớn ⇒ regen2 + manifest_export
    d = decide("2.13.7", "ok", 100, 0, regen_threshold=40)
    chk("big_delta_regen2", d["plan"], ["regen2", "manifest_export"])

    # 4) gap lớn + có reg_bulk ⇒ reg_bulk + manifest_export
    d = decide("2.13.7", "ok", 0, 50, bulk_threshold=8)
    chk("gap_reg_bulk", d["plan"], ["reg_bulk", "manifest_export"])

    # 5) gap lớn nhưng webapp cũ ⇒ KHÔNG reg_bulk (chỉ cảnh báo nâng cấp)
    d = decide("2.13.6", "ok", 0, 50)
    chk("gap_old_webapp_no_bulk", "reg_bulk" in d["plan"], False)
    chk("gap_old_webapp_flag", d["has_reg_bulk"], False)

    # 6) gap chưa biết ⇒ không tự reg_bulk
    d = decide("2.13.7", "ok", 2, None)
    chk("gap_unknown_no_bulk", "reg_bulk" in d["plan"], False)

    # 7) gộp: chưa baseline + gap lớn ⇒ regen2, changes_init, reg_bulk, manifest_export (1 lần)
    d = decide("2.13.7", "no_baseline", None, 30)
    chk("combo_plan", d["plan"], ["regen2", "changes_init", "reg_bulk", "manifest_export"])
    chk("combo_single_export", d["plan"].count("manifest_export"), 1)

    # 8) version compare
    chk("ver_ge_eq", _ver_ge("2.13.7", "2.13.7"), True)
    chk("ver_ge_lt", _ver_ge("2.13.6", "2.13.7"), False)
    chk("ver_ge_gt", _ver_ge("2.14.0", "2.13.7"), True)
    chk("ver_ge_empty", _ver_ge("", "2.13.7"), False)

    # 9) gap đúng ngưỡng (= threshold) ⇒ reg_bulk
    d = decide("2.13.7", "ok", 0, 8, bulk_threshold=8)
    chk("gap_at_threshold", "reg_bulk" in d["plan"], True)

    # 10) END không đụng Drive ⇒ CHỈ manifest_export (KHÔNG regen2, KHÔNG changes_init) — (v1.15.0)
    d = decide("2.19.0", "ok", 0, 0, phase="end", end_regen=False)
    chk("end_export_only", d["plan"], ["manifest_export"])
    chk("end_no_changes_init", "changes_init" not in d["plan"], True)

    # 11) END có đụng Drive ⇒ regen2 + manifest_export (KHÔNG changes_init)
    d = decide("2.19.0", "ok", 0, 0, phase="end", end_regen=True)
    chk("end_touched_regen", d["plan"], ["regen2", "manifest_export"])
    chk("end_touched_no_init", "changes_init" not in d["plan"], True)

    # 12) tukhoa gap lớn ⇒ backfill_keywords_live + manifest_export — (v1.15.0)
    d = decide("2.19.0", "ok", 0, 0, tukhoa_gap=20, tukhoa_threshold=8)
    chk("tukhoa_backfill", d["plan"], ["backfill_keywords_live", "manifest_export"])

    # 13) tukhoa gap nhỏ (orphan) ⇒ KHÔNG backfill
    d = decide("2.19.0", "ok", 0, 0, tukhoa_gap=1, tukhoa_threshold=8)
    chk("tukhoa_small_noop", "backfill_keywords_live" in d["plan"], False)

    # 14) END + tukhoa gap lớn ⇒ backfill_keywords_live + manifest_export (1 export)
    d = decide("2.19.0", "ok", 0, 0, tukhoa_gap=20, phase="end", end_regen=False)
    chk("end_tukhoa", d["plan"], ["backfill_keywords_live", "manifest_export"])
    chk("end_single_export", d["plan"].count("manifest_export"), 1)

    npass = sum(1 for _, ok, *_ in cases if ok)
    for name, ok, got, want in cases:
        if not ok:
            print(f"  FAIL {name}: got={got} want={want}")
    print(f"selftest: {npass}/{len(cases)} pass")
    return 0 if npass == len(cases) else 1


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("phase", nargs="?", default="boot", choices=["boot", "end"])
    ap.add_argument("--manifest")
    ap.add_argument("--regen-threshold", type=int, default=40)
    ap.add_argument("--bulk-threshold", type=int, default=8)
    ap.add_argument("--tukhoa-threshold", type=int, default=8,
                    help="số doc on-NLM thiếu tukhoa ≥ N ⇒ đề xuất backfill_keywords_live (v1.15.0)")
    ap.add_argument("--touched-drive", action="store_true",
                    help="phase=end: phiên CÓ thay đổi cấu trúc Drive (move/rename/ingest/add) ⇒ regen2; mặc định bỏ regen2 (v1.15.0)")
    ap.add_argument("--min-version", default="2.13.7")
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--apply", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(selftest())
    run(a)


if __name__ == "__main__":
    main()
