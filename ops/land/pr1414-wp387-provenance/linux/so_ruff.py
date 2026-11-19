"""So tap diagnostic ruff (bo so dong/cot) giua hai muc `ruff check` trong mot tep nghiem-thu-bo-sung. Dung: python so_ruff.py <tep>"""
import collections, re, sys
secs = re.split(r"(?m)^(?=## )", open(sys.argv[1], encoding="utf-8").read())
r = [s for s in secs if "ruff check" in s.splitlines()[0]]
assert len(r) == 2, len(r)
ms = [collections.Counter(re.sub(r":\d+:\d+:", ":", l) for l in s.splitlines() if re.match(r"\S+:\d+:\d+: [A-Z]\d+", l)) for s in r]
print(f"base {sum(ms[0].values())} diagnostic, merge {sum(ms[1].values())}; base-merge {dict(ms[0] - ms[1])}; merge-base {dict(ms[1] - ms[0])}")
print("DELTA 0" if ms[0] == ms[1] else "DELTA KHAC 0")
