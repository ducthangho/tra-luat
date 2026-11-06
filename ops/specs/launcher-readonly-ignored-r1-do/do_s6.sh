#!/bin/bash
# chay trong ban sao moi cua kho; in sha256 .git/index sau tung lenh
set -u
K="$1"; cd "$K" || exit 2
h(){ sha256sum .git/index | cut -c1-16; }
echo "truoc            $(h)"
for c in "git status --short" "git log --oneline -3" "git diff --stat HEAD~1 HEAD" "git show --stat HEAD" "git rev-parse HEAD" "git ls-files -s README.md"; do
  $c >/dev/null 2>&1; echo "rc=$? $(h)  $c"
done
f=$(git ls-files | head -1); touch -m "$f"; git status --short >/dev/null; echo "rc=$? $(h)  touch -m $f; git status --short"
git diff --quiet; echo "rc=$? $(h)  git diff --quiet (sau touch)"
