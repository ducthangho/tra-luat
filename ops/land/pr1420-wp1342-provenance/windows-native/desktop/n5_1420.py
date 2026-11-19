import json
o = r"F:\tl-win\session_015GtxrZk6gmfQKo7g4BfMBS\wp1342r5-out-20261119T120908Z"
def L(f):
    d = {}
    for l in open(o + "\\" + f, encoding="utf-8"):
        if l.startswith("{"):
            j = json.loads(l)
            if "rc" in j and "id" in j:
                d[j["id"]] = j["rc"]
    return d
B, H = L("BASE.stdout.txt"), L("HEAD.stdout.txt")
print("B", len(B), "H", len(H))
print("B rc!=0", [k for k, v in B.items() if v])
print("H rc!=0", [k for k, v in H.items() if v])
print("base khong co o head", [k for k in B if k not in H])
print("moi", sorted(set(H) - set(B)))
for n in ("wp1342_native_job_breakaway_tuong_minh", "wp1342_native_job_breakaway_ngam", "wp1342_native_job_long", "wp1342_pure_spawn_fx_mo_rong"):
    print("==", n)
    for l in open(o + "\\HEAD-" + n + ".txt", encoding="utf-8"):
        print("   ", l.rstrip()[:500])
