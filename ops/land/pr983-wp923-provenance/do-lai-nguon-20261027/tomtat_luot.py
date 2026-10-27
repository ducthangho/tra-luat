"""Tom tat cac luot review: python3 -I tomtat_luot.py <thu_muc_verdicts> <tien_to> <so_luot>"""
import hashlib, json, os, re, sys
D, T, N = sys.argv[1], sys.argv[2], int(sys.argv[3])
for i in range(1, N + 1):
    b = os.path.join(D, f"{T}-review-{i}-codex-")
    r = json.load(open(b + "run.json"))
    v = open(b + "verdict.md", encoding="utf-8").read()
    ph = hashlib.sha256(open(b + "prompt.md", "rb").read()).hexdigest()
    mp = r.get("model_phuc_vu")
    vd = re.search(r"Verdict:\s*\**\s*([\w_]+)", v)
    rc = re.search(r"Reviewed commit:\s*\W*([0-9a-f]{7,40})", v)
    print(i, r.get("run_id"), str(r.get("head") or r.get("head_sha"))[:7], r.get("trang_thai"), r.get("ma_thoat"),
          r.get("thoi_luong_giay"), "prompt_khop", ph == r.get("prompt_sha256"), r.get("model_phuc_vu_trang_thai"),
          json.dumps(mp, ensure_ascii=False)[:120] if mp else None, vd and vd[1], rc and rc[1][:7])
