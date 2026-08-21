#!/usr/bin/env python3
"""Phan chung bang kho bare that, kem bang dot bien tren ban sao tam."""
from __future__ import annotations
import importlib.util
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path
sys.dont_write_bytecode = True
HERE = Path(__file__).resolve().parent
TOOL = HERE / "nhanh_don_duoc.py"
def run(args: list[str], cwd: Path, check: bool = True, env: dict[str, str] | None = None):
    p = subprocess.run(args, cwd=cwd, capture_output=True, text=True, encoding="utf-8",
                       errors="replace", env=env, check=False)
    if check and p.returncode:
        raise AssertionError(f"rc={p.returncode}: {' '.join(args)}\n{p.stdout}\n{p.stderr}")
    return p
def viet(path: Path, text: str) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(text, encoding="utf-8", newline="\n")
def kho_bare(*, mac_dinh: str = "main", a: bool = False, b: bool = False,
             c_mot: bool = False, c_hai: bool = False):
    td = tempfile.TemporaryDirectory()
    root, remote, work = Path(td.name), Path(td.name) / "remote.git", Path(td.name) / "work"
    run(["git", "init", "--bare", str(remote)], root)
    run(["git", "init", "-b", mac_dinh, str(work)], root)
    run(["git", "config", "user.name", "test"], work)
    run(["git", "config", "user.email", "test@example.invalid"], work)
    viet(work / "ops/leases/base.yaml", "lease_id: base\n")
    viet(work / "state.txt", "A\n")
    run(["git", "add", "--", "ops/leases/base.yaml", "state.txt"], work)
    run(["git", "commit", "-m", "A"], work)
    viet(work / "state.txt", "S\n")
    run(["git", "commit", "-am", "S"], work)
    if a:
        run(["git", "branch", "ops/a"], work)
    viet(work / "state.txt", "D\n")
    run(["git", "commit", "-am", "D"], work)
    if b:
        run(["git", "switch", "-c", "ops/b"], work)
        with (work / "ops/leases/base.yaml").open("a", encoding="utf-8", newline="\n") as f:
            f.write("posted_comment_id: 123   # workflow ghi, DUNG sua tay\n")
        run(["git", "commit", "-am", "posted_comment_id"], work)
        run(["git", "switch", mac_dinh], work)
    if c_mot:
        run(["git", "switch", "-c", "ops/c-mot"], work)
        viet(work / "rieng.txt", "khac posted_comment_id\n")
        run(["git", "add", "--", "rieng.txt"], work)
        run(["git", "commit", "-m", "mot commit thuong"], work)
        run(["git", "switch", mac_dinh], work)
    if c_hai:
        run(["git", "switch", "-c", "ops/c-hai"], work)
        for i in (1, 2):
            viet(work / "rieng.txt", f"{i}\n")
            run(["git", "add", "--", "rieng.txt"], work)
            run(["git", "commit", "-m", f"commit rieng {i}"], work)
        run(["git", "switch", mac_dinh], work)
    run(["git", "remote", "add", "origin", str(remote)], work)
    run(["git", "push", "--all", "origin"], work)
    run(["git", "symbolic-ref", "HEAD", f"refs/heads/{mac_dinh}"], remote)
    run(["git", "fetch", "origin"], work)
    return td, remote, work
def tool(work: Path):
    p = run([sys.executable, str(TOOL), "--repo", str(work)], work, check=False)
    if p.returncode:
        raise AssertionError(f"tool rc={p.returncode}\n{p.stdout}\n{p.stderr}")
    nhom = {}
    for line in p.stdout.splitlines():
        if re.match(r"^[ABC]\t", line):
            n, ten, ly_do = line.split("\t", 2)
            nhom[ten] = (n, ly_do)
    dong_lenh = next(x for x in p.stdout.splitlines() if x.startswith("git push "))
    return nhom, shlex.split(dong_lenh)[4:], p.stdout
def nap_tool():
    spec = importlib.util.spec_from_file_location("nhanh_don_duoc", TOOL)
    assert spec and spec.loader
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)
    return mod
def T1():
    td, _, work = kho_bare(a=True)
    try:
        nhom, lenh, _ = tool(work)
        assert nhom["ops/a"][0] == "A" and "ops/a" in lenh
    finally:
        td.cleanup()
def T2():
    td, _, work = kho_bare(c_hai=True)
    try:
        nhom, _, _ = tool(work)
        assert nhom["ops/c-hai"][0] == "C"
    finally:
        td.cleanup()
def T3():
    td, _, work = kho_bare(b=True, c_mot=True)
    try:
        nhom, lenh, _ = tool(work)
        assert nhom["ops/b"][0] == "B" and "ops/b" in lenh
        assert nhom["ops/c-mot"][0] == "C" and "ops/c-mot" not in lenh
    finally:
        td.cleanup()
def T4():
    td, _, work = kho_bare(a=True)
    try:
        ref = "refs/remotes/origin/ops/a"
        tip = run(["git", "rev-parse", ref], work).stdout.strip()
        base_ref = "refs/remotes/origin/main"
        base = run(["git", "rev-parse", base_ref], work).stdout.strip()
        run(["git", "update-ref", "-d", ref], work)
        kq = nap_tool().phan_loai(work, ref, tip, base_ref, base)
        assert kq.nhom == "C" and ("bien mat" in kq.ly_do or "khong doc" in kq.ly_do)
    finally:
        td.cleanup()
def T5():
    td, remote, _ = kho_bare(c_hai=True)
    try:
        reader = Path(td.name) / "shallow"
        run(["git", "clone", "--depth", "1", "--no-single-branch", remote.as_uri(), str(reader)], Path(td.name))
        nhom, lenh, _ = tool(reader)
        assert nhom and all(v[0] == "C" and "kho nong" in v[1] for v in nhom.values()) and not lenh
    finally:
        td.cleanup()
def T6():
    td, _, work = kho_bare(mac_dinh="ops/main", a=True)
    try:
        nhom, lenh, _ = tool(work)
        assert nhom["ops/main"][0] == "A" and "ops/main" not in lenh
    finally:
        td.cleanup()
def T7():
    td, _, work = kho_bare()
    try:
        _, _, out = tool(work)
        assert "nhanh mac dinh co the bi ep lui" in out
        assert "KHONG co phep kiem nao luc chay" in out
    finally:
        td.cleanup()
def T8():
    td, remote, work = kho_bare(a=True)
    try:
        assert run(["git", "rev-parse", "--is-bare-repository"], remote).stdout.strip() == "true"
        ref = "refs/remotes/origin/ops/a"
        tip = run(["git", "rev-parse", ref], work).stdout.strip()
        base_ref = "refs/remotes/origin/main"
        base = run(["git", "rev-parse", base_ref], work).stdout.strip()
        assert run(["git", "rev-list", "--count", f"{base}..{tip}"], work).stdout.strip() == "0"
        assert run(["git", "merge-base", "--is-ancestor", tip, base], work, check=False).returncode == 0
        remote.rename(Path(td.name) / "remote.offline")
        nhom, lenh, _ = tool(work)
        assert nhom["ops/a"][0] == "C" and "fetch loi:" in nhom["ops/a"][1]
        assert "ops/a" not in lenh
    finally:
        td.cleanup()
CA = [(f"T{i}", globals()[f"T{i}"]) for i in range(1, 9)]
DOT_BIEN = [
    ("dao-chieu-to-tien", ("T1",), 'p = _git(repo, "merge-base", "--is-ancestor", tip, base_oid)', 'p = _git(repo, "merge-base", "--is-ancestor", base_oid, tip)'),
    ("bo-kiem-commit-rieng", ("T2",), 'return KetQua("C", f"con {so_rieng} commit rieng")', 'return KetQua("A", "dot bien bo kiem commit rieng")'),
    ("noi-B-thanh-mot-commit", ("T3",), "if la_posted:", "if True:"),
    ("loi-thanh-khong-commit-rieng", ("T4",), 'return KetQua("C", f"ref bien mat/khong doc duoc: {loi}")', 'return KetQua("A", "dot bien coi loi la khong co commit rieng")'),
    ("in-ca-C", ("T3", "T5", "T8"), 'kq.nhom in {"A", "B"} and ten != mac_dinh', 'kq.nhom in {"A", "B", "C"} and ten != mac_dinh'),
    ("bo-loai-mac-dinh", ("T6",), 'kq.nhom in {"A", "B"} and ten != mac_dinh', 'kq.nhom in {"A", "B"}'),
    ("xoa-khai-gioi-han", ("T7",), '"GIOI HAN: lenh in ra KHONG co phep kiem nao luc chay; phai doc lai ket qua truoc khi dan lenh."', '"GIOI HAN: da bi dot bien xoa."'),
    ("bo-chan-fetch-loi", ("T8",), "if fetch.returncode:", "if False:"),
    ("go-nhanh-kho-nong", ("T5",), '    elif shallow:\n        loi_chung = "kho nong; lich su khong du de phan loai an toan"\n', ""),
    ("dao-khop-base-remote", ("T1", "T3", "T6"), "base_oid != remote_oid", "base_oid == remote_oid"),
]
def chay_ca():
    do = []
    for ten, fn in CA:
        try:
            fn()
            print(f"CASE {ten}: DAT")
        except Exception as exc:
            do.append(ten)
            print(f"CASE {ten}: DO — {exc}")
    return do
def chay_dot_bien() -> int:
    dat = 0
    with tempfile.TemporaryDirectory() as d:
        root, src = Path(d), Path(d) / "source"
        run(["git", "init", "-q", str(src)], root)
        run(["git", "config", "user.name", "mutation"], src)
        run(["git", "config", "user.email", "mutation@example.invalid"], src)
        shutil.copy2(TOOL, src / TOOL.name)
        shutil.copy2(Path(__file__), src / Path(__file__).name)
        run(["git", "add", "--", TOOL.name, Path(__file__).name], src)
        run(["git", "commit", "-qm", "source"], src)
        for ten, dich, neo, thay in DOT_BIEN:
            ban_sao = root / ten
            ban_sao.mkdir()
            # Moi mutant bat dau bang dung duong `git archive ... | tar -x`.
            archive = subprocess.Popen(["git", "-C", str(src), "archive", "HEAD"], stdout=subprocess.PIPE)
            assert archive.stdout is not None
            tar = subprocess.run(["tar", "-x", "-C", str(ban_sao)], stdin=archive.stdout, check=False)
            archive.stdout.close()
            if archive.wait() or tar.returncode:
                raise AssertionError("git archive | tar -x that bai")
            tep = ban_sao / TOOL.name
            text = tep.read_text(encoding="utf-8")
            if text.count(neo) != 1:
                raise AssertionError(f"neo mutant {ten} khong duy nhat")
            tep.write_text(text.replace(neo, thay), encoding="utf-8", newline="\n")
            env = dict(os.environ, NHANH_DON_DUOC_KHONG_DOT_BIEN="1", PYTHONDONTWRITEBYTECODE="1")
            p = run([sys.executable, Path(__file__).name], ban_sao, check=False, env=env)
            ca_do = re.findall(r"^CASE (T\d+): DO", p.stdout, re.M)
            ok = p.returncode != 0 and ca_do == list(dich)
            dat += int(ok)
            so_ca = len(dich)
            print(f"MUTANT {ten} | {','.join(dich)} | {f'{so_ca}/{so_ca}' if ok else f'0/{so_ca}'}")
            if not ok:
                print(f"CA DO THUC TE: {','.join(ca_do) or '(rong)'} | rc={p.returncode}")
                print(p.stdout)
                print(p.stderr)
    return dat
def main() -> int:
    do = chay_ca()
    tong = len(CA)
    if do:
        print(f"{tong - len(do)}/{tong}")
        return 1
    if os.environ.get("NHANH_DON_DUOC_KHONG_DOT_BIEN"):
        print(f"{tong}/{tong}")
        return 0
    mutant_dat = chay_dot_bien()
    print(f"{tong}/{tong}")
    return 0 if mutant_dat == len(DOT_BIEN) else 1
if __name__ == "__main__":
    raise SystemExit(main())
