#!/usr/bin/env python3
"""dung.py ROUND SHA [PREV_VERDICT_PATH] — dung sandbox review #674 luot ROUND tai exact SHA. In duong dan + sha prompt."""
import hashlib, os, shutil, subprocess, sys
from pathlib import Path
sys.dont_write_bytecode = True
S = Path("/tmp/claude-0/-home-user-tra-luat/7ccc7ea3-39e6-5592-a374-909e124275e1/scratchpad")
REPO = Path("/home/user/tra-luat")
ROUND, SHA = sys.argv[1], sys.argv[2]
PREV = Path(sys.argv[3]) if len(sys.argv) > 3 else None
SPEC_OID, SPEC_PATH = "410529252da143bf5cb83be327065e35ac28c4f0", "ops/specs/CI-DUONG-NHANH-HO-SO-r2.md"
R = S / f"rv{ROUND}"
if R.exists():
    raise SystemExit(f"{R} da ton tai")
def sh(*a, cwd=None, check=True):
    r = subprocess.run(a, cwd=cwd, capture_output=True)
    if check and r.returncode:
        raise SystemExit(f"{a}: rc={r.returncode} {r.stderr.decode()[:400]}")
    return r.stdout.decode().strip()
R.mkdir(parents=True)
for d in ("goi", "out", "tmp"):
    (R / d).mkdir()
sh("git", "clone", "--quiet", "--bare", "--no-local", str(REPO), str(R / "kho.git"))
sh("git", "fetch", "--quiet", str(REPO), "+refs/remotes/origin/*:refs/heads/*", cwd=R / "kho.git")
sh("git", "clone", "--quiet", str(R / "kho.git"), str(R / "cay"))
sh("git", "fetch", "--quiet", "origin", "+refs/heads/*:refs/remotes/origin/*", cwd=R / "cay")
sh("git", "remote", "set-url", "origin", "https://github.com/ducthangho/tra-luat.git", cwd=R / "cay")
sh("git", "config", "core.abbrev", "7", cwd=R / "cay")
sh("git", "config", "core.autocrlf", "false", cwd=R / "cay")
sh("git", "checkout", "--quiet", "--detach", SHA, cwd=R / "cay")
assert sh("git", "rev-parse", "HEAD", cwd=R / "cay") == SHA
assert sh("git", "rev-parse", "--is-shallow-repository", cwd=R / "cay") == "false"
spec = subprocess.run(["git", "show", f"{SPEC_OID}:{SPEC_PATH}"], cwd=REPO, capture_output=True, check=True).stdout
(R / "goi" / "SPEC-r2.md").write_bytes(spec)
spec_sha = hashlib.sha256(spec).hexdigest()
assert spec_sha == "b6e719c999d5990f987628963c248b1ac53d377dfa5b668ac06adce76981da57", spec_sha
for t in ("do_lai_so.py", "DO_LAI.md", "kiem_ke.py"):
    shutil.copyfile(S / "rvtools" / t, R / "goi" / t)
prev = ("Day la luot 1, chua co luot truoc." if PREV is None else
        f"Luot truoc: `{R}/goi/LUOT-TRUOC-VERDICT.md` (verdict cua chinh ban o luot truoc, nguyen van). Bat buoc co muc `DOI CHIEU LUOT TRUOC`. "
        "D1 VA D2 DA DUOC CHU KHO DUYET (erratum dac ta r2, Issue #674 comment 5887720007, https://github.com/ducthangho/tra-luat/issues/674#issuecomment-5887720007): "
        "D1 = `git diff --check` chay voi `core.whitespace=-blank-at-eol,-blank-at-eof,-space-before-tab` (van bat conflict marker); "
        "D2 = lease con han chay `check`, lease het han chay `kiem(bo_qua_han=True)`. Do la HANH VI DUOC DUYET: KHONG ghi finding ve chinh sach; "
        "VAN tim loi TRONG cach hien thuc (bo_qua_han co bo them chot nao khac khong; ba loai khoang trang co bi tat rong hon ba loai do khong). "
        "Luu y S3: cac lop `chot-yaml-chi-do-su-hien-dien`, `bang-do-thieu-neo-va-thieu-kiem-ke` da xuat hien 3 lan; luot nay executor da vá theo HUONG TONG QUAT "
        "(y11 quet moi job, y12 dong bang moi `if:` cap buoc, kiem_ke.py dem tu cau truc). Hay tim CUA VAO CON LAI, va neu gap thi neu CA LOP tong quat chu khong chi cua ban vua thay. "
        "LUOT 5: y13 nay KHOA TOAN BO ci.yml NGOAI THAN `run:` (cap workflow, cap job gom runs-on/needs/strategy/include/exclude/timeout/env/outputs, "
        "cap buoc gom tap khoa/uses/with/env/shell/working-directory/timeout/id/if/continue-on-error va THU TU buoc). BIEN GIOI DA KHAI: than `run:` cua buoc CO SAN "
        "(khong do packet nay them) nam NGOAI pham vi packet va NGOAI y13 (do cong khac va review canh); than `run:` cua buoc do packet them thi khoa nguyen van (y08/y09). "
        "Khang dinh ve than `run:` co san hay ghi la NGOAI-PHAM-VI, khong tinh vao P. Phan hoach ca cho bang kiem ke do ham `phan_hoach_ca` (t96 canh).")
if PREV is not None:
    shutil.copyfile(PREV, R / "goi" / "LUOT-TRUOC-VERDICT.md")
p = (S / "rvtools" / "PROMPT.tmpl.md").read_text(encoding="utf-8")
for k, v in {"ROUND": ROUND, "R": str(R), "SHA": SHA, "SPEC_SHA": spec_sha, "PREV_DOAN": prev}.items():
    p = p.replace("{{" + k + "}}", v)
(R / "PROMPT.md").write_text(p, encoding="utf-8")
print(R)
print("prompt sha256", hashlib.sha256(p.encode("utf-8")).hexdigest())
