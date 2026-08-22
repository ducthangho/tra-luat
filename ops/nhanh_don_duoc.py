#!/usr/bin/env python3
"""Phan loai nhanh ops/**; chi in lenh xoa, khong tu xoa ref."""
from __future__ import annotations
import argparse
import re
import shlex
import subprocess
import sys
from dataclasses import dataclass
from datetime import datetime, timezone
from pathlib import Path
SHA = re.compile(r"[0-9a-f]{40}")
POSTED = re.compile(rb"posted_comment_id:[ \t]+[0-9]+(?:[ \t]+#[^\r\n]*)?\n")
GIOI_HAN = (
    "GIOI HAN: phan loai chi dung tai thoi diem do; nhanh mac dinh co the bi ep lui sau do.",
    "GIOI HAN: lenh in ra KHONG co phep kiem nao luc chay; phai doc lai ket qua truoc khi dan lenh.",
)
@dataclass(frozen=True)
class KetQua:
    nhom: str
    ly_do: str
def _git(repo: Path, *args: str) -> subprocess.CompletedProcess[str]:
    return subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, text=True,
        encoding="utf-8", errors="replace", check=False,
    )
def _oid(repo: Path, ref: str) -> tuple[str | None, str]:
    p = _git(repo, "rev-parse", "--verify", f"{ref}^{{commit}}")
    oid = p.stdout.strip()
    if p.returncode or not SHA.fullmatch(oid):
        return None, (p.stderr.strip() or "git khong tra ve commit OID")
    return oid, ""
def _mot_dong_posted(old: bytes, new: bytes) -> bool:
    cu, moi = old.splitlines(keepends=True), new.splitlines(keepends=True)
    if len(moi) != len(cu) + 1:
        return False
    return any(POSTED.fullmatch(dong) and moi[:i] + moi[i + 1:] == cu
               for i, dong in enumerate(moi))
def _chi_them_posted(repo: Path, commit: str, base_oid: str) -> tuple[bool, str]:
    p = _git(repo, "show", "-s", "--format=%P", commit)
    cha = p.stdout.split()
    if p.returncode or len(cha) != 1:
        return False, "khong do duoc mot commit thuong co dung mot cha"
    if _git(repo, "merge-base", "--is-ancestor", cha[0], base_oid).returncode != 0:
        return False, "cha cua commit duy nhat khong do duoc la to tien cua nhanh mac dinh"
    p = _git(repo, "diff-tree", "--no-commit-id", "--name-status", "-z", "-r", cha[0], commit)
    muc = p.stdout.split("\0")
    if p.returncode or not muc or muc[-1] != "":
        return False, "git loi khi doc cac tep cua commit duy nhat"
    muc = muc[:-1]
    if not muc or len(muc) % 2:
        return False, "diff commit duy nhat khong co hinh dang do duoc"
    for trang_thai, path in zip(muc[0::2], muc[1::2]):
        if trang_thai != "M" or not path.startswith("ops/leases/") or not path.endswith(".yaml"):
            return False, "commit duy nhat khong chi sua lease YAML"
        cu = subprocess.run(["git", "-C", str(repo), "show", f"{cha[0]}:{path}"],
                            capture_output=True, check=False)
        moi = subprocess.run(["git", "-C", str(repo), "show", f"{commit}:{path}"],
                             capture_output=True, check=False)
        if cu.returncode or moi.returncode:
            return False, f"git loi khi doc noi dung {path}"
        if not _mot_dong_posted(cu.stdout, moi.stdout):
            return False, f"{path} co thay doi khac posted_comment_id"
    return True, "chi con mot commit chi them posted_comment_id"
def phan_loai(repo: Path, ref: str, expected_tip: str,
              base_ref: str, base_oid: str) -> KetQua:
    tip, loi = _oid(repo, ref)
    if tip is None:
        return KetQua("C", f"ref bien mat/khong doc duoc: {loi}")
    if tip != expected_tip:
        return KetQua("C", f"ref doi giua chung: mong {expected_tip}, thay {tip}")
    base_now, loi = _oid(repo, base_ref)
    if base_now is None or base_now != base_oid:
        return KetQua("C", f"nhanh mac dinh doi/khong doc duoc: {loi or base_now}")
    p = _git(repo, "rev-list", "--count", f"{base_oid}..{tip}")
    raw = p.stdout.strip()
    if p.returncode or not raw.isdigit():
        return KetQua("C", f"khong doc duoc so commit rieng: {p.stderr.strip() or raw}")
    so_rieng = int(raw)
    if so_rieng == 0:
        p = _git(repo, "merge-base", "--is-ancestor", tip, base_oid)
        if p.returncode == 0:
            return KetQua("A", "moi commit da nam trong nhanh mac dinh")
        return KetQua("C", "git khong xac nhan duoc quan he to tien du kien")
    if so_rieng == 1:
        p = _git(repo, "rev-list", f"{base_oid}..{tip}")
        commits = p.stdout.split()
        if p.returncode or len(commits) != 1 or not SHA.fullmatch(commits[0]):
            return KetQua("C", "git loi khi doc commit rieng duy nhat")
        la_posted, ly_do = _chi_them_posted(repo, commits[0], base_oid)
        if la_posted:
            return KetQua("B", ly_do)
        return KetQua("C", ly_do)
    return KetQua("C", f"con {so_rieng} commit rieng")
def _mac_dinh(repo: Path, remote: str) -> tuple[str | None, str | None, str]:
    p = _git(repo, "ls-remote", "--symref", remote, "HEAD")
    if p.returncode:
        return None, None, p.stderr.strip() or "ls-remote HEAD loi"
    ten = oid = None
    for line in p.stdout.splitlines():
        if line.startswith("ref: refs/heads/") and line.endswith("\tHEAD"):
            ten = line.removeprefix("ref: refs/heads/").removesuffix("\tHEAD")
        elif line.endswith("\tHEAD") and SHA.fullmatch(line.split("\t", 1)[0]):
            oid = line.split("\t", 1)[0]
    return ten, oid, "" if ten and oid else "remote HEAD khong day du"
def _refs(repo: Path, remote: str, prefix: str) -> list[tuple[str, str, str]]:
    goc = f"refs/remotes/{remote}/{prefix}"
    p = _git(repo, "for-each-ref", "--format=%(refname)%09%(objectname)%09%(symref)", goc)
    if p.returncode:
        raise RuntimeError(p.stderr.strip() or "for-each-ref loi")
    ket_qua = []
    for line in p.stdout.splitlines():
        ref, oid, symref = line.split("\t", 2)
        if not symref and SHA.fullmatch(oid):
            ket_qua.append((ref.removeprefix(f"refs/remotes/{remote}/"), ref, oid))
    return sorted(ket_qua)
def main(argv: list[str] | None = None) -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8")
        sys.stderr.reconfigure(encoding="utf-8")
    ap = argparse.ArgumentParser(description="Phan loai nhanh ops/** thanh A/B/C, khong xoa ref")
    ap.add_argument("--repo", default=".")
    ap.add_argument("--remote", default="origin")
    ap.add_argument("--prefix", default="ops/")
    a = ap.parse_args(argv)
    repo = Path(a.repo).resolve()
    if _git(repo, "rev-parse", "--git-dir").returncode:
        print("LOI: --repo khong phai kho git", file=sys.stderr)
        return 2
    bat_dau = datetime.now(timezone.utc).isoformat(timespec="seconds")
    fetch = _git(repo, "fetch", "--prune", "--no-tags", a.remote)
    try:
        refs = _refs(repo, a.remote, a.prefix)
    except RuntimeError as exc:
        print(f"LOI: {exc}", file=sys.stderr)
        return 2
    mac_dinh, remote_oid, loi_head = _mac_dinh(repo, a.remote)
    base_ref = f"refs/remotes/{a.remote}/{mac_dinh}" if mac_dinh else ""
    base_oid, loi_base = _oid(repo, base_ref) if base_ref else (None, loi_head)
    shallow = _git(repo, "rev-parse", "--is-shallow-repository").stdout.strip() == "true"
    loi_chung = ""
    if fetch.returncode:
        loi_chung = f"fetch loi: {fetch.stderr.strip()}"
    elif shallow:
        loi_chung = "kho nong; lich su khong du de phan loai an toan"
    elif loi_head or base_oid != remote_oid:
        loi_chung = f"nhanh mac dinh khong do duoc/on dinh: {loi_head or loi_base or base_oid}"
    da_phan: list[tuple[str, KetQua]] = []
    for ten, ref, oid in refs:
        kq = KetQua("C", loi_chung) if loi_chung else phan_loai(repo, ref, oid, base_ref, base_oid or "")
        da_phan.append((ten, kq))
    ket_thuc = datetime.now(timezone.utc).isoformat(timespec="seconds")
    print(f"REMOTE: {a.remote} | PHAM VI: {a.prefix}** | MAC DINH: "
          f"{mac_dinh or 'KHONG DO DUOC'} @ {remote_oid or base_oid or 'KHONG DO DUOC'}")
    print(f"KHOANG DO: {bat_dau} .. {ket_thuc} | CHE DO: chi doc remote; khong push, khong xoa")
    for nhom in "ABC":
        ds = [(ten, kq) for ten, kq in da_phan if kq.nhom == nhom]
        print(f"NHOM {nhom} ({len(ds)})")
        for ten, kq in ds:
            print(f"{nhom}\t{ten}\t{kq.ly_do}")
    an_toan = [ten for ten, kq in da_phan
               if kq.nhom in {"A", "B"} and ten != mac_dinh]
    print("LENH IN RA (KHONG TU CHAY):")
    print("git push " + shlex.quote(a.remote) + " --delete" +
          (" " + " ".join(map(shlex.quote, an_toan)) if an_toan else ""))
    for dong in GIOI_HAN:
        print(dong)
    return 0
if __name__ == "__main__":
    raise SystemExit(main())
