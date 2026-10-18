"""Quet MOI ref refs/remotes/origin/* cua kho quet: moi blob duoi ops/leases/ (theo cap (blob, duong dan), khu trung)
mang lease_id = lease-publish-windows-do-r3-g3-claude => han `lease_expires_at_utc`. Doc YAML bang yaml.safe_load.
Tra loi: o moc 2026-10-02T01:12:00Z, CON ban nao cua g3 tren ref nao CON_HAN (han > moc) khong.
Dung: python3 -B quet_han_g3.py <kho_quet>
"""
import subprocess
import sys
from datetime import datetime, timezone

import yaml

K = sys.argv[1]
LID = "lease-publish-windows-do-r3-g3-claude"
MOC = datetime(2026, 10, 2, 1, 12, 0, tzinfo=timezone.utc)


def git(*a):
    return subprocess.run(["git", "-C", K, *a], capture_output=True, check=True).stdout


refs = git("for-each-ref", "--format=%(refname)", "refs/remotes/origin").decode().split()
cap = {}
for r in refs:
    out = git("ls-tree", "-r", "-z", r, "--", "ops/leases")
    for muc in out.split(b"\0"):
        if not muc:
            continue
        meta, duong = muc.split(b"\t", 1)
        _mode, loai, oid = meta.split()
        if loai == b"blob":
            cap.setdefault((oid.decode(), duong.decode()), []).append(r)
ban, hong = {}, []
for (oid, duong), rs in cap.items():
    b = git("cat-file", "blob", oid)
    if LID.encode() not in b:
        continue
    try:
        d = yaml.safe_load(b.decode("utf-8"))
    except Exception as e:  # noqa: BLE001
        hong.append((oid, duong, type(e).__name__))
        continue
    if not isinstance(d, dict) or str(d.get("lease_id")) != LID:
        continue
    s = str(d.get("lease_expires_at_utc"))
    han = datetime.fromisoformat(s.replace("Z", "+00:00"))
    ban[(oid, duong)] = (s, han, sorted(x.removeprefix("refs/remotes/origin/") for x in rs))
print(f"ref quet: {len(refs)} · cap (blob, duong) duoi ops/leases: {len(cap)} · ban mang lease_id {LID}: {len(ban)}"
      f" · YAML hong: {len(hong)}")
for (oid, duong), (s, han, rs) in sorted(ban.items(), key=lambda x: x[1][1]):
    print(f"  blob {oid[:7]} {duong} han {s} => tai moc 2026-10-02T01:12:00Z: "
          f"{'HET_HAN' if han <= MOC else 'CON_HAN'} · {len(rs)} ref: {', '.join(rs[:6])}{' ...' if len(rs) > 6 else ''}")
con = [k for k, v in ban.items() if v[1] > MOC]
print(f"KET LUAN: ban g3 con han SAU moc tren ref quet duoc: {len(con)}; han muon nhat: "
      f"{max((v[0] for v in ban.values()), default='-')}")
sys.exit(1 if con or hong or not ban else 0)
