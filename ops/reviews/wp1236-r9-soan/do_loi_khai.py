"""Ban tham chieu L8 (dac ta wp1236 r9) — do tren moi ops/land/*-land-evidence.yaml. KHONG phai ma thi cong."""
import sys, re, json, hashlib, datetime, collections
from pathlib import Path
sys.path.insert(0, str(Path(__file__).resolve().parent))
from thamchieu import kiem_tep, yaml
PHI = {"gateoutputnguon", "gateoutputnguonvagioihan", "mocgateoutputrcdisposition"}
TOKS = {"passed", "measured", "not_measured", "failed", "skipped", "not_run", "owner_waived"}
RE_TOK = re.compile(r"\s*([a-z_]+)(?=$|[\s—\-:(,.;])")
RE_DG = re.compile(r"(?<![A-Za-z0-9_./-])([A-Za-z0-9_./-]*danh-gia-gate-output-[0-9]+\.txt)")
RE_URL = re.compile(r"https://github\.com/ducthangho/tra-luat/\S*?#issuecomment-(\d+)")
RE_MIEN = re.compile(r"mien_gate_output: ([0-9a-f]{40}) os=([a-z0-9,.-]+) ly_do=(\S.*?) han=(\d{4}-\d{2}-\d{2})")
def chuan(k): return "".join(c for c in k.casefold() if c.isalnum())
def loi_khai(x, duong="$"):
    if isinstance(x, dict):
        for k, v in x.items():
            if "gateoutput" in chuan(str(k)) and chuan(str(k)) not in PHI: yield f"{duong}.{k}", v
            yield from loi_khai(v, f"{duong}.{k}")
    elif isinstance(x, list):
        for i, v in enumerate(x): yield from loi_khai(v, f"{duong}[{i}]")
def kiem_mien(v, thu_muc):
    urls = RE_URL.findall(v)
    if len(urls) != 1: return ["url"]
    rb = [p for p in thu_muc.glob(f"readback-*issuecomment-{urls[0]}.json") if p.is_file() and not p.is_symlink()] if thu_muc.is_dir() else []
    if len(rb) != 1: return ["readback"]
    d = json.loads(rb[0].read_text(encoding="utf-8"))
    if d.get("user", {}).get("login") != "ducthangho" or d.get("author_association") != "OWNER": return ["tac_gia"]
    dong = [m for l in str(d.get("body", "")).splitlines() if (m := RE_MIEN.fullmatch(l.strip()))]
    if len(dong) != 1: return ["dong_mien"]
    m = dong[0]
    try: datetime.date.fromisoformat(m[4])
    except ValueError: return ["han"]
    if "ubuntu-latest" not in m[2].split(",") or m[1] not in v: return ["os_sha"]
    return []
sys.path.insert(0, str(Path.cwd() / "ops"))
import land_evidence_nguon as LEN
root = Path(sys.argv[1]); tk = collections.Counter(); ly_tk = collections.Counter(); out = []
for hs in sorted((root / "ops/land").glob("*-land-evidence.yaml")):
    b = hs.read_bytes()
    if LEN.MIEN_TRU_CUTOVER.get(hs.name) == hashlib.sha256(b).hexdigest():
        tk["MIEN_CUTOVER"] += 1; out.append(f"MIEN_CUTOVER {hs.name}"); continue
    doc = yaml.safe_load(b.decode("utf-8"))
    thu_muc = root / "ops/land" / (hs.name[:-len("-land-evidence.yaml")] + "-provenance")
    vp, n, co_duong = [], 0, False
    for duong, v in loi_khai(doc):
        n += 1
        m = RE_TOK.match(v.casefold()) if isinstance(v, str) else None
        tok = m[1] if m and m[1] in TOKS else None
        if tok is None: vp.append((duong, "dinh_dang_loi_khai")); continue
        if tok in ("not_measured", "skipped", "not_run"): continue
        if tok == "owner_waived":
            l = kiem_mien(v, thu_muc)
            if l: vp.append((duong, "waiver_khong_co_can_cu:" + l[0]))
            else: co_duong = True
            continue
        tep = RE_DG.findall(v)
        if tok in ("passed", "measured") and not tep: vp.append((duong, "duong_khong_tep_danh_gia")); continue
        for t in tep:
            p = thu_muc / t
            if ".." in Path(t).parts or t.startswith("/") or not p.is_file() or p.is_symlink(): vp.append((duong, "tep_danh_gia_khong_hop_le")); continue
            tt, _ = kiem_tep(p, thu_muc); can = "passed" if tok in ("passed", "measured") else "failed"
            if tt != can: vp.append((duong, f"danh_gia_khong_{can}:{tt}"))
        if tok in ("passed", "measured"): co_duong = True
    tp = doc.get("trang_thai_packet") if isinstance(doc, dict) else None
    if isinstance(tp, dict) and tp.get("landed") is True and not co_duong and not vp:
        vp.append(("$", "landed_khong_loi_khai_gate_output_duong"))
    kq = "DO" if vp else ("DAT" if n else "KHONG_LOI_KHAI")
    tk[kq] += 1
    for _, l in vp: ly_tk[l.split(":")[0]] += 1
    out.append(f"{kq} {hs.name} " + "; ".join(f"{d}:{l}" for d, l in vp))
print("\n".join(out)); print(dict(tk)); print(dict(ly_tk))
