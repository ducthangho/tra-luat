"""Do THAT phan con lai cua ma tran N1 (#646, spec LEASE-TRUONG-KHAI-NGHIA-r1 §4 N1, cot phai): cac ca MOI TRUONG/cau hinh doc hai
va dot bien tung chot cua n1.sh, tren rig git tam ngoai kho, dung n1.sh/n5.py cua ho so (khong sua ban goc).
Dung: python -X utf8 -B n1env_1386.py <clone_day_du_lich_su> <B> <H> <n1.sh> <n5.py>
Rig: clone tam; Hg = commit tren B voi blob H cua docs/PROTOCOL_DA_PHIEN.md (dung). Moi ca khai bao rc ky vong theo dac ta:
  rc 0 (khong doi ket qua): diff.ignoreSubmodules=all; .git/info/attributes `* -diff`; .git/info/grafts; nguoi goi dat GIT_DIR,
    GIT_WORK_TREE, GIT_OBJECT_DIRECTORY, GIT_ALTERNATE_OBJECT_DIRECTORIES sai; kho co replace ref cua object khac.
  rc 1: gitlink (ca duoi ignoreSubmodules=all); them dong o §5 duoi `* -diff`; `git replace H_bad Hg` (H_bad them tep ngoai write set),
    ca khi nguoi goi dat GIT_NO_REPLACE_OBJECTS= rong; `git replace` blob xau bang blob dung; H_bad duoi grafts; chen khoi sai vi tri.
  rc 2: core.abbrev=bogus trong config cuc bo.
Dot bien tung chot (ban sao n1.sh): bo GIT_NO_REPLACE_OBJECTS=1 => ca replace commit rc 0; bo `unset` => ca GIT_DIR sai rc 2;
  bo (b) diff-tree => chmod +x va them tep rc 0; bo dong thoi (c)(d)(e) => them dong §5 va chen sai vi tri rc 0;
  bo dong thoi (d)(e) => chen sai vi tri rc 0."""
import json, os, pathlib, shutil, subprocess, sys, tempfile

# r1407: goi bash qua ops/bash_nen.tim_bash() (cong cong_cu_test cam loi goi `bash` TRAN).
import sys as _sys_bn
from pathlib import Path as _Path_bn
_sys_bn.path.insert(0, str(_Path_bn(__file__).resolve().parents[3]))
from bash_nen import tim_bash as _tim_bash  # noqa: E402
_BASH, _BASH_CHAN_DOAN = _tim_bash()
if not _BASH:
    raise SystemExit(f'KHONG DO DUOC: khong co bash dung duoc ({_BASH_CHAN_DOAN})')
SRC, B, H, N1, N5 = sys.argv[1:6]
P = "docs/PROTOCOL_DA_PHIEN.md"
BASE_ENV = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
CENV = dict(BASE_ENV, GIT_AUTHOR_NAME="rig", GIT_AUTHOR_EMAIL="rig@invalid", GIT_COMMITTER_NAME="rig", GIT_COMMITTER_EMAIL="rig@invalid",
            GIT_AUTHOR_DATE="2026-11-18T00:00:00Z", GIT_COMMITTER_DATE="2026-11-18T00:00:00Z")


def git(d, *a, inp=None):
    p = subprocess.run(["git", "-C", str(d), *a], capture_output=True, env=CENV, input=inp)
    if p.returncode:
        raise SystemExit(f"git {a} loi: {p.stderr.decode()[-400:]}")
    return p.stdout.decode().strip()


def chay(script, repo, b, h, env_them=None):
    env = dict(BASE_ENV, **(env_them or {}))
    p = subprocess.run([_BASH, str(script), str(repo), b, h, N5], capture_output=True, text=True, env=env)
    return {"rc": p.returncode, "out": (p.stdout + p.stderr).strip()[-240:]}


bao = {"B": B, "H": H, "ca": {}, "dot_bien": {}}
with tempfile.TemporaryDirectory() as tmp:
    T = pathlib.Path(tmp)
    d = T / "rig"
    subprocess.run(["git", "clone", "-q", "--no-hardlinks", "--no-checkout", SRC, str(d)], check=True, env=CENV)
    blobH = subprocess.run(["git", "-C", str(d), "show", f"{H}:{P}"], capture_output=True, check=True, env=CENV).stdout
    blobB = subprocess.run(["git", "-C", str(d), "show", f"{B}:{P}"], capture_output=True, check=True, env=CENV).stdout
    n = [0]

    def commit(du_lieu, them=None, gitlink=None):
        n[0] += 1
        w = T / f"w{n[0]}"
        git(d, "worktree", "add", "-q", "--detach", str(w), B)
        oid = git(w, "hash-object", "-w", "--no-filters", "--stdin", inp=du_lieu)
        git(w, "update-index", "--cacheinfo", f"100644,{oid},{P}")
        for ten, noi in (them or {}).items():
            o2 = git(w, "hash-object", "-w", "--no-filters", "--stdin", inp=noi)
            git(w, "update-index", "--add", "--cacheinfo", f"100644,{o2},{ten}")
        if gitlink:
            git(w, "update-index", "--add", "--cacheinfo", f"160000,{gitlink},docs/sub")
        tree = git(w, "write-tree")
        c = git(w, "commit-tree", tree, "-p", B, "-m", "rig")
        git(d, "worktree", "remove", "--force", str(w))
        return c

    Hg = commit(blobH)
    s5 = blobH.index(b"\n## 5. ")
    them5 = blobH[:s5 + 1] + blobH[s5 + 1:].replace(b"\n", b"\nDong them o muc 5.\n", 1)
    H_them5 = commit(them5)
    H_tep = commit(blobH, them={"docs/them.md": b"x\n"})
    H_gitlink = commit(blobH, gitlink=B)
    # chen khoi DUNG noi dung nhung SAI vi tri (truoc "## 5."), base con lai giu nguyen => them/xoa van 14 0
    y = blobB.index(b"\n## 5. ")
    # khoi chen = phan blob H khac base (dung cach n5 --ky-vong dung): tim doan chen bang so khop tien to/hau to
    i = 0
    while i < len(blobB) and blobB[i] == blobH[i]:
        i += 1
    j = 0
    while j < len(blobB) - i and blobB[-1 - j] == blobH[-1 - j]:
        j += 1
    khoi = blobH[i:len(blobH) - j]
    sai = blobB[:y + 1] + khoi + blobB[y + 1:]
    H_sai = commit(sai)
    bao["khoi_chen_byte"] = len(khoi)

    def ca(ten, ky, repo, b, h, env_them=None, script=N1):
        r = chay(script, repo, b, h, env_them)
        r.update(ky_vong=ky, dung=(r["rc"] == ky))
        bao["ca"][ten] = r
        return r

    def voi_config(k, v, fn):
        git(d, "config", k, v)
        try:
            fn()
        finally:
            git(d, "config", "--unset", k)

    def voi_tep(rel, noi, fn):
        f = d / ".git" / rel
        f.parent.mkdir(parents=True, exist_ok=True)
        f.write_bytes(noi)
        try:
            fn()
        finally:
            f.unlink()

    ca("doi_chung_Hg", 0, d, B, Hg)
    voi_config("diff.ignoreSubmodules", "all", lambda: (ca("ignoreSubmodules_all_Hg", 0, d, B, Hg),
                                                         ca("gitlink_duoi_ignoreSubmodules_all", 1, d, B, H_gitlink)))
    ca("gitlink", 1, d, B, H_gitlink)
    voi_tep("info/attributes", b"* -diff\n", lambda: (ca("attr_khong_diff_Hg", 0, d, B, Hg),
                                                      ca("them_dong_5_duoi_attr_khong_diff", 1, d, B, H_them5)))
    # grafts: ghep cha gia cho Hg va H_tep (cha = Hg/khac); diff-tree tren cay nen ket qua khong doi
    voi_tep("info/grafts", f"{Hg} {H_tep}\n{H_tep} {Hg}\n".encode(), lambda: (ca("grafts_Hg", 0, d, B, Hg),
                                                                               ca("H_bad_duoi_grafts", 1, d, B, H_tep)))
    for bien, gt in (("GIT_DIR", str(T / "khong-co.git")), ("GIT_WORK_TREE", str(T / "khong-co-wt")),
                     ("GIT_OBJECT_DIRECTORY", str(T / "khong-co-obj")), ("GIT_ALTERNATE_OBJECT_DIRECTORIES", str(T / "khong-co-alt"))):
        ca(f"nguoi_goi_dat_{bien}_sai", 0, d, B, Hg, {bien: gt})
    # replace ref cua object khac (khong lien quan B/Hg): thay H_them5 bang H_tep
    git(d, "replace", H_them5, H_tep)
    ca("replace_ref_object_khac_Hg", 0, d, B, Hg)
    git(d, "replace", "-d", H_them5)
    # replace commit xau bang commit dung
    git(d, "replace", H_tep, Hg)
    ca("replace_H_bad_bang_Hg", 1, d, B, H_tep)
    ca("replace_H_bad_GIT_NO_REPLACE_OBJECTS_rong", 1, d, B, H_tep, {"GIT_NO_REPLACE_OBJECTS": ""})
    git(d, "replace", "-d", H_tep)
    # replace blob xau bang blob dung
    ob_xau = git(d, "rev-parse", f"{H_them5}:{P}")
    ob_dung = git(d, "rev-parse", f"{Hg}:{P}")
    git(d, "replace", ob_xau, ob_dung)
    ca("replace_blob_xau_bang_blob_dung", 1, d, B, H_them5)
    git(d, "replace", "-d", ob_xau)
    ca("chen_khoi_sai_vi_tri", 1, d, B, H_sai)
    voi_config("core.abbrev", "bogus", lambda: ca("core_abbrev_bogus", 2, d, B, Hg))

    # Dot bien tung chot tren ban sao n1.sh
    goc = pathlib.Path(N1).read_text(encoding="utf-8")

    def dot(ten, cap, dich):
        s = goc
        for tim, thay in cap:
            if s.count(tim) != 1:
                bao["dot_bien"][ten] = {"ket_qua": f"KHONG_DO: mau khop {s.count(tim)} lan: {tim[:60]}"}
                return
            s = s.replace(tim, thay)
        f = T / f"n1_{ten}.sh"
        f.write_text(s, encoding="utf-8")
        kq = {}
        for ca_ten, (b, h, env_them, ky_dot) in dich.items():
            r = chay(f, d, b, h, env_them)
            r.update(ky_vong_duoi_dot_bien=ky_dot, doi_ket_qua=(r["rc"] == ky_dot))
            kq[ca_ten] = r
        bao["dot_bien"][ten] = {"ca": kq, "ket_qua": "GIET" if all(v["doi_ket_qua"] for v in kq.values()) else "SONG"}

    # commit chmod +x (mode 100755)
    n[0] += 1
    w = T / f"w{n[0]}"
    git(d, "worktree", "add", "-q", "--detach", str(w), B)
    o = git(w, "hash-object", "-w", "--no-filters", "--stdin", inp=blobH)
    git(w, "update-index", "--cacheinfo", f"100755,{o},{P}")
    H_chmod = git(w, "commit-tree", git(w, "write-tree"), "-p", B, "-m", "rig")
    git(d, "worktree", "remove", "--force", str(w))
    bao["ca"]["chmod_x_ban_sach"] = dict(chay(N1, d, B, H_chmod), ky_vong=1)
    bao["ca"]["chmod_x_ban_sach"]["dung"] = bao["ca"]["chmod_x_ban_sach"]["rc"] == 1
    bao["ca"]["them_tep_ban_sach"] = dict(chay(N1, d, B, H_tep), ky_vong=1)
    bao["ca"]["them_tep_ban_sach"]["dung"] = bao["ca"]["them_tep_ban_sach"]["rc"] == 1

    git(d, "replace", H_tep, Hg)
    dot("bo_GIT_NO_REPLACE_OBJECTS", [("export GIT_NO_REPLACE_OBJECTS=1 ", "export ")], {"replace_H_bad_bang_Hg": (B, H_tep, None, 0)})
    git(d, "replace", "-d", H_tep)
    UNSET = ("unset GIT_DIR GIT_WORK_TREE GIT_OBJECT_DIRECTORY GIT_ALTERNATE_OBJECT_DIRECTORIES GIT_INDEX_FILE GIT_COMMON_DIR \\\n"
             "      GIT_NAMESPACE GIT_REPLACE_REF_BASE GIT_GRAFT_FILE GIT_SHALLOW_FILE GIT_CONFIG GIT_CONFIG_PARAMETERS GIT_CONFIG_COUNT\n")
    dot("bo_unset", [(UNSET, "")], {"nguoi_goi_dat_GIT_DIR_sai": (B, Hg, {"GIT_DIR": str(T / "khong-co.git")}, 2)})
    CB = ('[ "$raw" = "$(printf \':100644 100644 %s %s M\\t%s\' "$oB" "$oH" "$P")" ] \\\n'
          '  || do_ "diff-tree khac dung mot dong M 100644->100644 cho $P: $(printf \'%s\' "$raw" | head -2 | tr \'\\t\\n\' \' |\')"\n')
    CC = '[ "$dem" = "14 0" ] || do_ "dong them/xoa = $dem, can 14 0"\n'
    CD = '[ "$oH" = "$kv" ] || do_ "blob H $oH khac blob ky vong $kv"\n'
    CE = 'python3 -I "$N5" "$T/h.md" >/dev/null || do_ "N5 do tren blob H"\n'
    dot("bo_b_diff_tree", [(CB, "")], {"chmod_x": (B, H_chmod, None, 0), "them_tep": (B, H_tep, None, 0)})
    dot("bo_c_d_e", [(CC, ""), (CD, ""), (CE, "")], {"them_dong_5": (B, H_them5, None, 0), "chen_khoi_sai_vi_tri": (B, H_sai, None, 0)})
    dot("bo_d_e", [(CD, ""), (CE, "")], {"chen_khoi_sai_vi_tri": (B, H_sai, None, 0)})

bao["so_ca"], bao["so_ca_dung"] = len(bao["ca"]), sum(bool(v.get("dung")) for v in bao["ca"].values())
bao["so_dot_bien"], bao["so_dot_bien_giet"] = len(bao["dot_bien"]), sum(v.get("ket_qua") == "GIET" for v in bao["dot_bien"].values())
ok = bao["so_ca"] == bao["so_ca_dung"] and bao["so_dot_bien"] == bao["so_dot_bien_giet"]
bao["TONG"] = "DAT" if ok else "KHONG_DAT"
print(json.dumps(bao, ensure_ascii=False, indent=1))
sys.exit(0 if ok else 1)
