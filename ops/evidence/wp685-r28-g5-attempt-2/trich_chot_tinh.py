"""Trich NGUYEN VAN khoi `chot_tinh_r12.py` tu dac ta r28 bang may, doi chieu sha256 khoi da cong bo trong dac ta.
Dung: python3 trich_chot_tinh.py <spec.md> <tep ra>. rc=0 chi khi: spec dung sha256, dung MOT khoi khop, 412 dong, sha khop."""
import hashlib, sys
SPEC_SHA = "8007edf4e00aaefc298bf299bf19be9a71c54e73ff6a1610eb676a806773e156"
KHOI_SHA = "add42b31beeaece6e3cf546d3915a153099bfe7a232995b0e1546bbd4a5735b6"
b = open(sys.argv[1], "rb").read()
assert hashlib.sha256(b).hexdigest() == SPEC_SHA, "spec sai bam"
dong = b.decode("utf-8").split("\n")
khoi, i = [], 0
while i < len(dong):
    if dong[i].strip() == "```python" and i + 1 < len(dong) and dong[i + 1].startswith("# chot_tinh_r12.py"):
        j = i + 1
        while dong[j].strip() != "```":
            j += 1
        khoi.append(dong[i + 1:j]); i = j
    i += 1
assert len(khoi) == 1, f"so khoi = {len(khoi)}"
noi = ("\n".join(khoi[0]) + "\n").encode("utf-8")
h = hashlib.sha256(noi).hexdigest()
print(f"dong={len(khoi[0])} sha256={h} khop={h == KHOI_SHA}")
assert len(khoi[0]) == 412 and h == KHOI_SHA
open(sys.argv[2], "wb").write(noi)
