"""Do THAT mot phan ma tran phan chung N1 cua #646 (spec LEASE-TRUONG-KHAI-NGHIA-r1 §4 N1) bang n1.sh/n5.py cua ho so, rig git tam ngoai kho.
Dung: python -X utf8 -B n1rig_1386.py <clone_day_du_lich_su> <B> <H> <n1.sh> <n5.py>
Rig: clone tam; moi bien the la MOT commit tren B (base lease d1ca71a) dung tu blob H cua docs/PROTOCOL_DA_PHIEN.md.
Ky vong: doi chung H that => rc 0; bien the dung noi dung (commit moi = B + blob H) => rc 0.
  rc 1: H = B; chmod +x; them tep thu hai; them dong o §5; sua mot dong khac (ngoai vung); CRLF toan tep; H la tree.
  rc 2: duong kho khong ton tai; OID khong co trong kho.
KHONG chay lai o day (ghi thang): cac ca moi truong gia (GIT_DIR/GIT_OBJECT_DIRECTORY sai, grafts, replace refs, gitlink,
  diff.ignoreSubmodules=all, * -diff, core.abbrev=bogus) va dot bien tung chot cua n1.sh."""
import json, os, pathlib, subprocess, sys, tempfile
SRC, B, H, N1, N5 = sys.argv[1:6]
P = "docs/PROTOCOL_DA_PHIEN.md"
ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
ENV.update(GIT_AUTHOR_NAME="rig", GIT_AUTHOR_EMAIL="rig@invalid", GIT_COMMITTER_NAME="rig", GIT_COMMITTER_EMAIL="rig@invalid",
           GIT_AUTHOR_DATE="2026-11-18T00:00:00Z", GIT_COMMITTER_DATE="2026-11-18T00:00:00Z")


def git(d, *a, inp=None):
    p = subprocess.run(["git", "-C", str(d), *a], capture_output=True, env=ENV, input=inp)
    if p.returncode:
        raise SystemExit(f"git {a} loi: {p.stderr.decode()[-400:]}")
    return p.stdout


def chay(repo, b, h):
    p = subprocess.run(["bash", N1, str(repo), b, h, N5], capture_output=True, text=True, env={k: v for k, v in os.environ.items()})
    return {"rc": p.returncode, "out": (p.stdout + p.stderr).strip()[-300:]}


bao = {"B": B, "H": H, "ca": {}}
with tempfile.TemporaryDirectory() as tmp:
    d = pathlib.Path(tmp) / "rig"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", SRC, str(d)], check=True, env=ENV)
    blobH = git(d, "show", f"{H}:{P}")
    tree_B = git(d, "rev-parse", f"{B}^{{tree}}").decode().strip()

    def commit_tu(sua):   # sua(index_dir) chinh sua tren worktree tam; tra commit moi tren B
        w = pathlib.Path(tmp) / f"w{len(bao['ca'])}"
        git(d, "worktree", "add", "-q", "--detach", str(w), B)
        sua(w)
        git(w, "add", "-A")
        if getattr(sua, "tho", False):   # ghi blob THO (--no-filters): .gitattributes cua kho chuan hoa CRLF khi `git add`
            oid = git(w, "hash-object", "-w", "--no-filters", P).decode().strip()
            git(w, "update-index", "--cacheinfo", f"100644,{oid},{P}")
        git(w, "-c", "core.autocrlf=false", "commit", "-q", "--no-verify", "-m", "rig")
        oid = git(w, "rev-parse", "HEAD").decode().strip()
        git(d, "worktree", "remove", "--force", str(w))
        return oid

    def ghi(w, data, mode=None):
        f = w / P
        f.write_bytes(data)
        if mode:
            os.chmod(f, mode)

    kv = {}
    kv["doi_chung_H_that"] = (str(d), B, H, 0)
    kv["doi_chung_commit_moi_B_cong_blob_H"] = (str(d), B, commit_tu(lambda w: ghi(w, blobH)), 0)
    kv["H_bang_B"] = (str(d), B, B, 1)
    kv["chmod_x"] = (str(d), B, commit_tu(lambda w: ghi(w, blobH, 0o755)), 1)
    kv["them_tep_thu_hai"] = (str(d), B, commit_tu(lambda w: (ghi(w, blobH), (w / "docs/them.md").write_bytes(b"x\n"))), 1)
    s5 = blobH.index(b"\n## 5. ")
    them5 = blobH[:s5 + 1] + blobH[s5 + 1:].replace(b"\n", b"\nDong them o muc 5.\n", 1)
    kv["them_dong_o_muc_5"] = (str(d), B, commit_tu(lambda w: ghi(w, them5)), 1)
    s1 = blobH.index(b"\n## 1")
    sua1 = blobH[:s1 + 4] + blobH[s1 + 4:].replace(b"\n", b" (sua)\n", 1)
    kv["sua_mot_dong_khac"] = (str(d), B, commit_tu(lambda w: ghi(w, sua1)), 1)
    def crlf(w):
        ghi(w, blobH.replace(b"\n", b"\r\n"))
    crlf.tho = True
    kv["crlf_toan_tep"] = (str(d), B, commit_tu(crlf), 1)
    kv["H_la_tree"] = (str(d), B, tree_B, 1)
    kv["kho_khong_ton_tai"] = (str(pathlib.Path(tmp) / "khong-co"), B, H, 2)
    kv["oid_khong_co"] = (str(d), B, "0123456789abcdef0123456789abcdef01234567", 2)
    for ten, (repo, b, h, ky) in kv.items():
        r = chay(repo, b, h)
        r.update(ky_vong=ky, dung=(r["rc"] == ky), b=b, h=h)
        bao["ca"][ten] = r
bao["so_ca"], bao["so_dung"] = len(bao["ca"]), sum(v["dung"] for v in bao["ca"].values())
bao["TONG"] = "DAT" if bao["so_ca"] == bao["so_dung"] else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if bao["TONG"] == "DAT" else 1)
