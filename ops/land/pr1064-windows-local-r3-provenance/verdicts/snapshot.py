"""Snapshot §8.2 cua mot checkout: HEAD/tree, diff/index, tracked/untracked/ignored kem hash bytes.

Dung: python3 snapshot.py <checkout> <out.json>
Hash moi tep trong cay lam viec (tru .git/), nen bat duoc ca ghi roi xoa giua hai moc chi khi
noi dung con khac o moc cuoi — gioi han §8.2 van giu nguyen.
"""
import hashlib
import json
import os
import subprocess
import sys


def git(repo, *a):
    return subprocess.run(["git", "-C", repo, *a], capture_output=True, check=True).stdout


def h(b):
    return hashlib.sha256(b).hexdigest()


def main(repo, out):
    tep = {}
    for goc, dirs, files in os.walk(repo):
        if ".git" in dirs:
            dirs.remove(".git")
        for f in files:
            p = os.path.join(goc, f)
            rel = os.path.relpath(p, repo).replace(os.sep, "/")
            if os.path.islink(p):
                tep[rel] = "symlink:" + os.readlink(p)
            else:
                with open(p, "rb") as fh:
                    tep[rel] = h(fh.read())
    snap = {
        "head": git(repo, "rev-parse", "HEAD").decode().strip(),
        "tree": git(repo, "rev-parse", "HEAD^{tree}").decode().strip(),
        "diff_binary_sha256": h(git(repo, "diff", "--binary")),
        "diff_cached_binary_sha256": h(git(repo, "diff", "--cached", "--binary")),
        "untracked": git(repo, "ls-files", "--others", "--exclude-standard", "-z").decode().split("\0")[:-1],
        "ignored": git(repo, "ls-files", "--others", "--ignored", "--exclude-standard", "-z").decode().split("\0")[:-1],
        "status_porcelain_sha256": h(git(repo, "status", "--porcelain=v1", "--untracked-files=all", "--ignored=matching")),
        "so_tep": len(tep),
        "tep_sha256": dict(sorted(tep.items())),
    }
    snap["tong_sha256"] = h(json.dumps(snap, sort_keys=True).encode())
    with open(out, "w", encoding="utf-8") as fh:
        json.dump(snap, fh, ensure_ascii=False, indent=1, sort_keys=True)
    print(out, snap["head"], snap["tree"], snap["so_tep"], len(snap["untracked"]), len(snap["ignored"]), snap["tong_sha256"])


if __name__ == "__main__":
    main(*sys.argv[1:])
