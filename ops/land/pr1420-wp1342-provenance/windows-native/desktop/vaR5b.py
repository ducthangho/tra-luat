import hashlib
W = r"F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS"
s = open(W + r"\dot_bien_r5.py", encoding="utf-8", newline="").read()
a1 = 'with tempfile.TemporaryDirectory() as td:\n'
b1 = 'with tempfile.TemporaryDirectory(ignore_cleanup_errors=True) as td:\n'
a2 = 'print("KQ_R5 " + json.dumps(kq, ensure_ascii=True))\n'
b2 = '    print("KQ_R5 " + json.dumps(kq, ensure_ascii=True), flush=True)  # r5b: in TRUOC khi don thu muc tam (WinError 32 lan 1)\n'
a3 = 'tempfile.TemporaryDirectory(prefix="dot_bien_r5_")'
b3 = 'tempfile.TemporaryDirectory(prefix="dot_bien_r5_", ignore_cleanup_errors=True)'
for a, b in ((a1, b1), (a2, b2), (a3, b3)):
    assert s.count(a) == 1, a
    s = s.replace(a, b)
open(W + r"\dot_bien_r5b.py", "w", encoding="utf-8", newline="").write(s)
print("r5b", hashlib.sha256(s.encode("utf-8")).hexdigest())
