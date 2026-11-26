#!/bin/bash
# Đo lại trạng thái lease thật cho r7, trên clone sạch `--reference` (r7/kho); không đụng ref nào của kho chính.
cd "$(dirname "$0")/../kho" || exit 1
date -u +%FT%TZ
git fetch -q origin '+refs/heads/*:refs/remotes/origin/*' --prune
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort > ../do/mc_ten
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin | grep -v '^HEAD$' | sort > ../do/cb_ten
echo "may_chu $(wc -l < ../do/mc_ten) cuc_bo $(wc -l < ../do/cb_ten) thieu $(comm -23 ../do/mc_ten ../do/cb_ten | wc -l) thua $(comm -13 ../do/mc_ten ../do/cb_ten | wc -l) shallow $(git rev-parse --is-shallow-repository) master $(git rev-parse origin/master)"
date -u +%FT%TZ
echo "adr_tren_master $(git ls-tree --name-only origin/master docs/adr/ | grep -cE '^docs/adr/[0-9]{4}-')"
n=0; for r in $(git for-each-ref --format='%(refname)' refs/remotes/origin); do
  git ls-tree --name-only "$r" docs/adr/ 2>/dev/null | grep -qE '^docs/adr/(0068|0069|00[7-9][0-9]|0[1-9][0-9]{2}|[1-9][0-9]{3})-' && n=$((n+1)); done
echo "ref_co_adr_0068_tro_len $n"
date -u +%FT%TZ
git checkout -q --detach origin/master
for p in .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py docs/PROTOCOL_DA_PHIEN.md docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md; do
  out=$(/usr/bin/python3 ops/lease_publish.py ai-dang-giu "$p" --root . 2>&1); rc=$?
  echo "$p rc=$rc :: $(echo "$out" | tail -1)"
done
date -u +%FT%TZ
/usr/bin/python3 -I - <<'EOF'
import datetime, pathlib, sys, types
lp = types.ModuleType("lp"); exec(compile(open("ops/lease_publish.py", encoding="utf-8").read(), "lp", "exec"), lp.__dict__)
cac = lp._quet_lease_toan_kho(pathlib.Path("."))
now = datetime.datetime.now(datetime.timezone.utc)
con = [m for m in cac if lp._phan_loai_lease(m["lease"], now) == "CÒN_HẠN"]
song = [m for m in con if lp._bia_mo_doi_xung(m["lease"], cac) is not True]
print(now.strftime("%FT%TZ"), "ban_ghi", len(cac), "con_han", len(con), "bia_mo", len(con) - len(song), "song", sorted({m["lease"].get("lease_id") for m in song}))
EOF
date -u +%FT%TZ
/usr/bin/python3 -I ../sc/tien_kiem.py origin/master; echo "rc=$?"
date -u +%FT%TZ
/usr/local/bin/python -I ../sc/tien_kiem.py origin/master; echo "rc_usr_local_python=$?"
date -u +%FT%TZ
