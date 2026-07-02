#!/usr/bin/env python3
"""nlm_sources.py — tra-luat v1.13.3
NLM client phía CLI (dùng khi có `nlm` trong môi trường: Cowork / host / container MCP).
Liệt kê nguồn NHANH (bỏ freshness) và lấy DESCRIBE (tóm tắt + từ khóa) của nguồn.

HAI CHẾ ĐỘ truy cập NLM trong skill tra-luat:
- Cowork / host có `nlm`: dùng script này (CLI) — nhanh, bỏ freshness, không treo MCP.
- Claude chat (bash không có `nlm`): KHÔNG dùng script này để gọi NLM; Claude gọi MCP
  (source_list_drive(skip_freshness=True), source_describe) rồi dump JSON cho backfill.

Cú pháp CLI tự dò 2 dạng (0.7.6 trước, cũ sau):
  nlm source list <nb> --drive --skip-freshness --json     # 0.7.6
  nlm list sources <nb> -d -S --json                        # cũ
  nlm source describe <sid> --json   |   nlm describe <sid> --json

CLI:
  nlm_sources.py list <notebook> [--all][--json][--reconcile M][--emit-backfill]
                 [--nlm-bin P][--docker C][--profile P][--cmd "tmpl"][--timeout N]
  nlm_sources.py describe <notebook> --source-ids a,b,c [--json][...]
  nlm_sources.py --selftest
"""
import argparse, json, os, re, shutil, subprocess, sys

UUID = re.compile(r"[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}")
K_ID = ("source_id", "sourceId", "id", "source", "sid", "uuid")
K_TITLE = ("title", "name", "display_name", "displayName", "source_title")
K_TYPE = ("type", "source_type", "sourceType", "kind")
K_DRIVE = ("drive_id", "driveId", "document_id", "documentId", "doc_id", "drive_document_id",
           "externalId", "external_id")
K_STATUS = ("status", "freshness", "state", "sync_status", "syncStatus", "stale", "fresh")
K_SUMMARY = ("summary", "description", "overview", "abstract", "desc")
K_KEYWORDS = ("keywords", "chips", "keyword_chips", "topics", "tags")


def _first(d, keys):
    if not isinstance(d, dict):
        return None
    for k in keys:
        if k in d and d[k] not in (None, ""):
            return d[k]
    low = {str(k).lower(): v for k, v in d.items()}
    for k in keys:
        v = low.get(k.lower())
        if v not in (None, ""):
            return v
    return None


def _find_rows(obj):
    if isinstance(obj, list):
        return obj if all(isinstance(x, dict) for x in obj) else []
    if isinstance(obj, dict):
        for k in ("sources", "items", "data", "results", "rows"):
            v = obj.get(k)
            if isinstance(v, list) and v and isinstance(v[0], dict):
                return v
        for v in obj.values():
            r = _find_rows(v)
            if r:
                return r
    return []


def normalize(raw_text):
    txt = (raw_text or "").strip()
    rows = []
    try:
        rows = _find_rows(json.loads(txt))
    except Exception:
        rows = []
    if not rows:
        for ln in txt.splitlines():
            ln = ln.strip().rstrip(",")
            if ln.startswith("{") and ln.endswith("}"):
                try:
                    rows.append(json.loads(ln))
                except Exception:
                    pass
    out = []
    if rows:
        for r in rows:
            out.append({"source_id": _first(r, K_ID), "title": _first(r, K_TITLE),
                        "type": _first(r, K_TYPE), "drive_id": _first(r, K_DRIVE),
                        "status": _first(r, K_STATUS)})
        return out, "json"
    for ln in txt.splitlines():
        m = UUID.search(ln)
        if not m:
            continue
        out.append({"source_id": m.group(0),
                    "title": (ln[:m.start()] + " " + ln[m.end():]).strip(" \t|") or None,
                    "type": None, "drive_id": None, "status": None})
    return out, ("table" if out else "empty")


def _prefix(nlm_bin=None, docker=None):
    nlm = nlm_bin or "nlm"
    return (["docker", "exec", docker, nlm] if docker else [nlm])


def nlm_available(nlm_bin=None, docker=None):
    if docker:
        return True  # giả định container có nlm; lỗi sẽ lộ khi chạy
    return bool(nlm_bin or shutil.which("nlm"))


def build_list_cmds(nb, drive=True, profile=None, nlm_bin=None, docker=None):
    """Trả về danh sách lệnh ứng viên (0.7.6 trước, cũ sau)."""
    pre = _prefix(nlm_bin, docker)
    prof = (["--profile", profile] if profile else [])
    new = pre + ["source", "list", nb] + (["--drive"] if drive else []) + ["--skip-freshness", "--json"] + prof
    old = pre + ["list", "sources", nb] + (["-d"] if drive else []) + ["-S", "--json"] + prof
    return [new, old]


def build_describe_cmds(sid, profile=None, nlm_bin=None, docker=None):
    pre = _prefix(nlm_bin, docker)
    prof = (["--profile", profile] if profile else [])
    return [pre + ["source", "describe", sid, "--json"] + prof,
            pre + ["describe", sid, "--json"] + prof]


def _run(cmd, timeout):
    p = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def fetch_sources(nb, drive=True, profile=None, nlm_bin=None, docker=None, timeout=180, cmd=None):
    if not nlm_available(nlm_bin, docker):
        raise FileNotFoundError(
            "Không có `nlm` trong môi trường này. Ở Cowork/host/container MCP mới chạy được "
            "(hoặc --nlm-bin/--docker). Trong Claude chat: dùng MCP source_list_drive rồi "
            "--nlm-json cho backfill.")
    cands = [cmd.split()] if cmd else build_list_cmds(nb, drive, profile, nlm_bin, docker)
    last = ""
    for c in cands:
        try:
            rc, out, err = _run(c, timeout)
        except Exception as e:
            last = str(e); continue
        if rc == 0:
            rows, mode = normalize(out)
            if rows:
                return rows, mode, " ".join(c)
            last = "rc=0 nhưng parse rỗng"
        else:
            last = err.strip()[:200]
    raise RuntimeError(f"nlm list thất bại (đã thử {len(cands)} dạng lệnh). Lỗi cuối: {last}")


def fetch_describe(sid, profile=None, nlm_bin=None, docker=None, timeout=120, cmd=None):
    cands = [cmd.replace("{sid}", sid).split()] if cmd else build_describe_cmds(sid, profile, nlm_bin, docker)
    last = ""
    for c in cands:
        try:
            rc, out, err = _run(c, timeout)
        except Exception as e:
            last = str(e); continue
        if rc == 0 and out.strip():
            d = {}
            try:
                d = json.loads(out)
            except Exception:
                d = {"summary": out.strip()}
            obj = d[0] if isinstance(d, list) and d else d
            return {"source_id": sid, "summary": _first(obj, K_SUMMARY) or (out.strip() if not isinstance(d, (dict, list)) else None),
                    "keywords": _first(obj, K_KEYWORDS)}
        last = (err or "rỗng").strip()[:200]
    raise RuntimeError(f"nlm describe thất bại cho {sid}: {last}")


def reconcile(sources, manifest_path):
    m = json.load(open(manifest_path, encoding="utf-8"))
    reg = {}
    for r in _find_rows(m):
        nid = _first(r, ("nlm_source_id", "nlmSourceId", "source_id"))
        if nid:
            reg[nid] = _first(r, ("name", "title", "sohieu", "so_hieu"))
    nlm_ids = {s["source_id"] for s in sources if s.get("source_id")}
    reg_ids = set(reg)
    return {"nlm_count": len(nlm_ids), "registry_linked": len(reg_ids),
            "only_in_nlm": sorted(nlm_ids - reg_ids),
            "only_in_registry": sorted(reg_ids - nlm_ids)}


def selftest():
    ok = 0; tot = 0
    # parse list
    for raw, mode_exp, n in [
        ('[{"id":"11111111-1111-1111-1111-111111111111","title":"QD_399","document_id":"1tLv"}]', "json", 1),
        ('{"sources":[{"sourceId":"22222222-2222-2222-2222-222222222222","name":"HD_05"}]}', "json", 1),
        ('55555555-5555-5555-5555-555555555555   NĐ 30/2020', "table", 1),
        ("", "empty", 0)]:
        tot += 1; rows, mode = normalize(raw)
        good = mode == mode_exp and len(rows) == n
        print(f"  parse {mode_exp:6}: {'OK' if good else 'FAIL'}"); ok += good
    # command-form: 0.7.6 đứng trước
    tot += 1
    cmds = build_list_cmds("NB", drive=True, docker="c1")
    c0 = " ".join(cmds[0])
    good = ("docker exec c1 nlm source list NB --drive --skip-freshness --json" == c0
            and "list sources NB -d -S --json" in " ".join(cmds[1]))
    print(f"  cmd-form list (0.7.6 first, docker): {'OK' if good else 'FAIL'}"); ok += good
    tot += 1
    dc = " ".join(build_describe_cmds("SID")[0])
    good = dc == "nlm source describe SID --json"
    print(f"  cmd-form describe: {'OK' if good else 'FAIL'}"); ok += good
    # describe parse
    tot += 1
    d = {}
    try:
        # mô phỏng JSON describe qua normalize-helpers
        obj = json.loads('{"summary":"Tóm tắt X","keywords":["a","b"]}')
        d = {"summary": _first(obj, K_SUMMARY), "keywords": _first(obj, K_KEYWORDS)}
    except Exception:
        pass
    good = d.get("summary") == "Tóm tắt X" and d.get("keywords") == ["a", "b"]
    print(f"  describe parse: {'OK' if good else 'FAIL'}"); ok += good
    # reconcile
    tot += 1
    import tempfile
    tf = tempfile.NamedTemporaryFile("w", suffix=".json", delete=False, encoding="utf-8")
    json.dump({"rows": [{"nlm_source_id": "11111111-1111-1111-1111-111111111111"},
                        {"nlm_source_id": "99999999-9999-9999-9999-999999999999"}]}, tf); tf.close()
    rec = reconcile([{"source_id": "11111111-1111-1111-1111-111111111111"},
                     {"source_id": "abababab-abab-abab-abab-abababababab"}], tf.name)
    good = rec["only_in_nlm"] == ["abababab-abab-abab-abab-abababababab"] and \
        rec["only_in_registry"] == ["99999999-9999-9999-9999-999999999999"]
    print(f"  reconcile: {'OK' if good else 'FAIL'}"); ok += good
    print(f"selftest: {ok}/{tot} pass")
    return ok == tot


def _emit_backfill(rows):
    return [{"id": r["source_id"], "title": r.get("title")} for r in rows if r.get("source_id")]


def main():
    ap = argparse.ArgumentParser(description="NLM CLI client (list/describe) cho tra-luat.")
    sub = ap.add_subparsers(dest="cmd_name")
    common = dict()
    for name in ("list", "describe"):
        sp = sub.add_parser(name)
        sp.add_argument("notebook")
        sp.add_argument("--nlm-bin"); sp.add_argument("--docker"); sp.add_argument("--profile")
        sp.add_argument("--cmd"); sp.add_argument("--timeout", type=int, default=180)
        sp.add_argument("--json", action="store_true")
        if name == "list":
            sp.add_argument("--all", action="store_true")
            sp.add_argument("--reconcile"); sp.add_argument("--emit-backfill", action="store_true")
        else:
            sp.add_argument("--source-ids", required=True, help="danh sách id, phân tách bằng dấu phẩy")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        sys.exit(0 if selftest() else 1)
    if a.cmd_name == "list":
        rows, mode, used = fetch_sources(a.notebook, drive=(not a.all), profile=a.profile,
                                         nlm_bin=a.nlm_bin, docker=a.docker, timeout=a.timeout, cmd=a.cmd)
        if a.reconcile:
            print(json.dumps(reconcile(rows, a.reconcile), ensure_ascii=False, indent=2)); return
        if a.emit_backfill:
            print(json.dumps(_emit_backfill(rows), ensure_ascii=False)); return
        if a.json:
            print(json.dumps(rows, ensure_ascii=False, indent=2)); return
        print(f"# {len(rows)} nguồn (parse={mode}; lệnh: {used})")
        for s in rows:
            print(f"  {s['source_id']}  {s.get('title') or ''}")
    elif a.cmd_name == "describe":
        ids = [x.strip() for x in a.source_ids.split(",") if x.strip()]
        out = []
        for sid in ids:
            try:
                out.append(fetch_describe(sid, profile=a.profile, nlm_bin=a.nlm_bin,
                                          docker=a.docker, timeout=a.timeout, cmd=a.cmd))
            except Exception as e:
                out.append({"source_id": sid, "error": str(e)})
        print(json.dumps(out, ensure_ascii=False, indent=2))
    else:
        ap.print_help()


if __name__ == "__main__":
    main()
