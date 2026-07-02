#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""backfill_nlm_title.py — tra-luat v1.13.3
Đồng bộ nlm_title (và tùy chọn DESCRIBE) vào registry bằng MỘT call reg_bulk.

Vì sao reg_bulk: N nguồn × reg_upsert = N round-trip (~1.6s/op → vài phút, dễ timeout).
reg_bulk đọc registry 1 LẦN, vá RAM theo nlm_source_id, ghi 1 LẦN ⇒ vài giây.

HAI CHẾ ĐỘ lấy danh sách nguồn NLM:
  • COWORK / host có `nlm`:  --from-nlm <notebook>   (script tự gọi nlm CLI, bỏ freshness)
  • CLAUDE CHAT (MCP):       --nlm-json dump.json     (Claude gọi MCP source_list_drive
                              (skip_freshness=True) + source_describe rồi dump ra JSON)
  • (thay thế)               --manifest tra_luat_manifest.json  (name làm nlm_title)

DESCRIBE (tóm tắt + từ khóa của nguồn):
  --with-describe            kèm describe; ghi sidecar nlm_describe_<nb>.json
  --desc-col COL             ngoài sidecar, vá describe vào cột COL của registry (cột phải
                              tồn tại sẵn trong sheet). Khi đó cols = nlm_title,COL.
  --source-ids a,b / --limit N   giới hạn tập describe (describe là N call/nguồn → tốn).
  Ở chế độ --nlm-json: describe lấy từ chính JSON (field desc/summary/keywords) — không gọi nlm.

MÔI TRƯỜNG: TL_WEBAPP, TL_TOKEN. Webapp >= 2.13.7 (reg_bulk). KHÔNG dùng Drive MCP.
"""
import os, sys, json, argparse
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gas
import nlm_sources as nlm


def _desc_text(summary, keywords):
    s = (summary or "").strip()
    if keywords:
        kw = ", ".join(keywords) if isinstance(keywords, list) else str(keywords)
        s = (s + " | Từ khóa: " + kw).strip(" |")
    return s[:1500]


def collect_sources(a):
    """Trả về (rows, source_describe_from_json) với rows=[{source_id,title,desc,keywords}]."""
    if a.from_nlm:
        if not nlm.nlm_available(a.nlm_bin, a.docker):
            sys.exit("[--from-nlm] Không có `nlm` ở đây. Dùng ở Cowork/host/container MCP "
                     "(hoặc --nlm-bin/--docker); trong Claude chat hãy dùng --nlm-json (MCP).")
        rows, mode, used = nlm.fetch_sources(a.from_nlm, drive=(not a.all_sources),
                                             profile=a.profile, nlm_bin=a.nlm_bin,
                                             docker=a.docker, timeout=a.timeout, cmd=a.cmd_list)
        print(f"[from-nlm] {len(rows)} nguồn (lệnh: {used})")
        return [{"source_id": r["source_id"], "title": r.get("title"),
                 "desc": None, "keywords": None} for r in rows if r.get("source_id")]
    if a.nlm_json:
        data = json.load(open(a.nlm_json, encoding="utf-8"))
        src = data.get("sources", data) if isinstance(data, dict) else data
        out = []
        for s in src:
            sid = s.get("id") or s.get("source_id")
            if sid:
                out.append({"source_id": sid, "title": s.get("title") or s.get("name"),
                            "desc": s.get("desc") or s.get("summary"),
                            "keywords": s.get("keywords")})
        return out
    if a.manifest:
        m = json.load(open(a.manifest, encoding="utf-8"))
        ents = m.get("entries", m) if isinstance(m, dict) else m
        out = []
        for e in ents:
            sid = e.get("nlm_source_id")
            if sid:
                out.append({"source_id": sid, "title": e.get("nlm_title") or e.get("name") or "",
                            "desc": None, "keywords": None})
        return out
    sys.exit("Cần một trong: --from-nlm | --nlm-json | --manifest")


def add_describe(a, rows):
    """Bổ sung describe cho rows (in-place). Nguồn describe: nlm CLI (--from-nlm) hoặc JSON sẵn."""
    targets = rows
    if a.source_ids:
        want = {x.strip() for x in a.source_ids.split(",") if x.strip()}
        targets = [r for r in rows if r["source_id"] in want]
    if a.limit:
        targets = targets[:a.limit]
    if a.from_nlm:  # gọi nlm describe từng nguồn
        for i, r in enumerate(targets, 1):
            try:
                d = nlm.fetch_describe(r["source_id"], profile=a.profile, nlm_bin=a.nlm_bin,
                                       docker=a.docker, timeout=a.timeout, cmd=a.cmd_describe)
                r["desc"], r["keywords"] = d.get("summary"), d.get("keywords")
            except Exception as e:
                r["_desc_err"] = str(e)[:160]
            if i % 25 == 0:
                print(f"  describe {i}/{len(targets)}…")
    # ở chế độ --nlm-json: desc đã có sẵn trong rows; không gọi nlm
    return targets


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--from-nlm", help="notebook_id — lấy nguồn qua nlm CLI (Cowork/host)")
    ap.add_argument("--nlm-json", help="dump MCP/JSON [{id,title,desc?,keywords?}] (Claude chat)")
    ap.add_argument("--manifest", help="tra_luat_manifest.json (thay thế)")
    ap.add_argument("--all-sources", action="store_true", help="--from-nlm: mọi nguồn (bỏ --drive)")
    ap.add_argument("--with-describe", action="store_true")
    ap.add_argument("--desc-col", help="cột registry để vá describe (phải tồn tại sẵn)")
    ap.add_argument("--source-ids", help="giới hạn describe theo id (phân tách dấu phẩy)")
    ap.add_argument("--limit", type=int, default=0, help="giới hạn số nguồn describe")
    ap.add_argument("--cols", default="nlm_title")
    ap.add_argument("--nlm-bin"); ap.add_argument("--docker"); ap.add_argument("--profile")
    ap.add_argument("--cmd-list"); ap.add_argument("--cmd-describe"); ap.add_argument("--timeout", type=int, default=180)
    ap.add_argument("--dry", action="store_true")
    ap.add_argument("--export", action="store_true", help="manifest_export sau backfill")
    a = ap.parse_args()

    rows = collect_sources(a)
    cols = a.cols
    if a.with_describe:
        described = add_describe(a, rows)
        # sidecar
        side = f"nlm_describe_{(a.from_nlm or 'dump')[:8]}.json"
        json.dump([{ "source_id": r["source_id"], "title": r.get("title"),
                     "summary": r.get("desc"), "keywords": r.get("keywords"),
                     "error": r.get("_desc_err")} for r in described],
                  open(side, "w", encoding="utf-8"), ensure_ascii=False, indent=1)
        print(f"[describe] {len(described)} nguồn → sidecar {side}")
        if a.desc_col:
            if a.desc_col not in cols.split(","):
                cols = cols + "," + a.desc_col
            print(f"[describe] sẽ vá vào cột '{a.desc_col}' (cột phải có sẵn trong registry)")

    # build items cho reg_bulk
    items = []
    for r in rows:
        it = {"nlm_source_id": r["source_id"]}
        if r.get("title"):
            it["nlm_title"] = r["title"]
        if a.with_describe and a.desc_col and (r.get("desc") or r.get("keywords")):
            it[a.desc_col] = _desc_text(r.get("desc"), r.get("keywords"))
        if len(it) > 1:
            items.append(it)
    print(f"items: {len(items)} (cols={cols})")
    if a.dry:
        print(json.dumps(items[:5], ensure_ascii=False, indent=1)); return

    ping = gas.get("ping")
    if str(ping.get("version", "")) < "2.13.7":
        sys.exit(f"webapp version={ping.get('version')} < 2.13.7 — chưa có reg_bulk.")
    r = gas.post("reg_bulk", items=json.dumps(items, ensure_ascii=False), cols=cols)
    print("reg_bulk:", json.dumps({k: r.get(k) for k in ["ok", "total", "patched", "missed"]}, ensure_ascii=False))
    if r.get("miss"):
        print(f"  mồ côi [{r.get('missed')}] ví dụ:", ", ".join(r["miss"][:10]))
    if a.export:
        print("manifest_export:", json.dumps(gas.get("manifest_export"), ensure_ascii=False)[:160])


if __name__ == "__main__":
    main()
