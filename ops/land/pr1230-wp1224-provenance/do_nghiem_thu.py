"""Do lai A1–A6 cua dac ta ops/specs/cloud-setup-p3c-docs-r2.md §4 tren blob merge 825eb35 (base c5a1c3d de so),
phien ghi so land session_015GtxrZk7fu1wjDZjWqyg2R — tra loi finding P1 r4485646618 tren PR #1251 (luot offline 4 chi review delta).

Moi tieu chi = mot ham vi tu tren noi dung tep; VE DUONG chay tren blob merge (phai True), VE AM chay tren ban dot bien theo
cot "dot bien lam DO" cua dac ta (phai False; MOI menh de A3 la mot dot bien). Dot bien sua CHUOI trong bo nho, khong ghi tep.
Cach goi: python3 do_nghiem_thu.py --kho <goc kho>
"""
import argparse, json, re, subprocess, sys

M, B = "825eb3561a94e05c36045d2c981b4108c523e31c", "c5a1c3d1230b347333d4ca10f7dc514b817f7a9d"
ap = argparse.ArgumentParser(); ap.add_argument("--kho", required=True); a = ap.parse_args()


def blob(rev, path):
    return subprocess.run(["git", "-C", a.kho, "show", f"{rev}:{path}"], check=True, capture_output=True).stdout.decode("utf-8")


gop = lambda s: re.sub(r"\s+", " ", s).strip()  # noqa: E731
ket = []


def ghi(ten, duong, am):
    ok = duong and all(v is False for _, v in am)
    ket.append(ok)
    print(f"{ten}: {'DAT' if ok else 'DO'} — duong={duong}" + "".join(f" | am[{m}]={v}" for m, v in am))


# A1 — DEV_TOOLING_GUIDE
dtg = blob(M, "references/DEV_TOOLING_GUIDE.md")
CUM1 = "hiện hành `references/Code.2.21.2q.gs`"
def a1(t):
    return not any("2.21.2p" in x for x in t.splitlines() if "hiện hành" in x) and t.count(CUM1) == 1
print("# DEV_TOOLING_GUIDE dong 'hiện hành' co .gs: " + repr([x.strip()[:160] for x in dtg.splitlines() if "hiện hành" in x and ".gs" in x]))
ghi("A1", a1(dtg), [("de 2p", a1(dtg.replace(CUM1, "hiện hành `references/Code.2.21.2p.gs`")))])

# A2 — DELTA_v1.19 so voi RELEASE_MANIFEST.json cua base
man = json.loads(blob(B, "RELEASE_MANIFEST.json"))
def duong_dan(m):
    for k in ("files", "entries"):
        if k in m:
            v = m[k]
            return [x["path"] if isinstance(x, dict) else x for x in v] if isinstance(v, list) else list(v)
    raise SystemExit("khong doc duoc danh sach tep trong manifest")
GS_MAN = {re.sub(r"^references/Code\.|\.gs$", "", p) for p in duong_dan(man) if re.fullmatch(r"references/Code\.[^/]+\.gs", p)}
SO = {1: "một", 2: "hai", 3: "ba", 4: "bốn", 5: "năm"}
delta = blob(M, "references/DELTA_v1.19.md")
def a2(t):
    d = [x for x in t.splitlines() if "Gói phát hành chỉ kèm snapshot" in x]
    if len(d) != 1:
        return False
    tap = set(re.findall(r"`(2\.\d+\.\w+)`", d[0]))
    return tap == GS_MAN and f"của {SO.get(len(GS_MAN), '?')} bản mới nhất" in d[0]
dd = [x for x in delta.splitlines() if "Gói phát hành chỉ kèm snapshot" in x]
print(f"# .gs trong RELEASE_MANIFEST.json@base: {sorted(GS_MAN)}; doan DELTA: {dd[0].strip()[:200] if dd else None!r}")
ghi("A2", a2(delta), [("xoa 2.21.2q khoi doan", a2(delta.replace(", `2.21.2q`", ""))),
                      ("chu 'hai'", a2(delta.replace("của ba bản mới nhất", "của hai bản mới nhất")))])

# A3 — khoi trich dan M3 trong GOI_AGENT_DA_NEN.md
M3 = gop("**Đường cũ (05-11-2026).** `CODEX_AUTH_JSON` là cơ chế cấu hình cũ, không dùng cho thiết lập mới. Đường hiện "
         "hành là `agent_creds`: P2b nạp credential lúc mở phiên, P3 ghi ngược khi `Stop`. Code vẫn còn đọc `CODEX_AUTH_JSON` "
         "để tương thích (hook phiên, `.claude/dev/launcher.py`; `.claude/dev/codex_cred.py` còn sinh và gỡ biến); đường ấy "
         "chưa gỡ, việc gỡ là packet riêng `CODEX-AUTH-JSON-GO-CODE`.")
goi = blob(M, "docs/GOI_AGENT_DA_NEN.md")
def doan(t):
    return [p for p in re.split(r"\n\s*\n", t)]
def a3(t):
    ds = doan(t)
    k = [i for i, p in enumerate(ds) if p.lstrip().startswith(">") and gop(re.sub(r"(?m)^\s*> ?", "", p)) == M3]
    if len(k) != 1:
        return False
    i = k[0]
    return i >= 1 and ds[i - 1].strip() == "### Để không phải nhập mã lại mỗi phiên" and ds[i + 1].lstrip().startswith("Container phiên remote là")
khoi = next((p for p in doan(goi) if gop(re.sub(r"(?m)^\s*> ?", "", p)) == M3), "")
am3 = [(f"xoa '{m}'", a3(goi.replace(khoi, khoi.replace(m, "", 1)))) for m in
       ("không dùng cho thiết lập mới", "Đường hiện\n> hành là `agent_creds`" if "Đường hiện\n> hành" in khoi else "Đường hiện hành là `agent_creds`",
        "Code vẫn còn đọc", "đường ấy\n> chưa gỡ" if "đường ấy\n> chưa gỡ" in khoi else "đường ấy chưa gỡ")]
am3.append(("doi khoi xuong cuoi muc", a3(goi.replace(khoi + "\n\n", "", 1) + "\n\n" + khoi + "\n")))
n_m3 = sum(1 for p in doan(goi) if gop(re.sub(r"(?m)^\s*> ?", "", p)) == M3)
print(f"# A3 khoi tim thay: {bool(khoi)}; so lan khop M3: {n_m3}")
ghi("A3", a3(goi), am3)

# A4 — cau M4 trong CLAUDE.md, trong gach 'Refresh token cua codex XOAY VONG'
M4 = gop("**Từ 05-11-2026 biến này là đường cũ**: `agent_creds` (P2b/P3) thay thế; code đọc biến vẫn còn để tương thích và "
         "chưa gỡ — xem khối đầu mục *Để không phải nhập mã lại mỗi phiên* trong `docs/GOI_AGENT_DA_NEN.md`.")
cl, cl_b = blob(M, "CLAUDE.md"), blob(B, "CLAUDE.md")
def gach(t):
    out, cur = [], None
    for x in t.splitlines():
        if re.match(r"^- ", x) or re.match(r"^#+ ", x) or x.strip() == "":
            if cur is not None:
                out.append(cur)
            cur = x if x.startswith("- ") else None
        elif cur is not None:
            cur += "\n" + x
    if cur is not None:
        out.append(cur)
    return out
def a4(t):
    if gop(t).count(M4) != 1:
        return False
    g = [x for x in gach(t) if M4 in gop(x)]
    return len(g) == 1 and g[0].startswith("- **Refresh token của codex XOAY VÒNG")
ghi("A4", a4(cl), [("bo cau", a4(cl.replace("**Từ 05-11-2026 biến này là đường cũ**", "", 1))),
                   ("xoa ve 'chưa gỡ'", a4(cl.replace("vẫn còn để tương thích và\n  chưa gỡ", "vẫn còn để tương thích", 1))),
                   ("doi sang gach khac", a4(cl.replace("  **Từ 05-11-2026 biến này là đường cũ**", "- **Từ 05-11-2026 biến này là đường cũ**", 1)))])

# A5 — ve am theo doan cho M3/M4. DON VI "doan": doan cach dong trong, TACH THEM tai moi dong bat dau "- " (muc danh sach).
# Ly do: CLAUDE.md §Goi agent da nen la MOT doan cach-dong-trong dai (danh sach khong co dong trong), nen tach chi theo dong trong
# gop moi gach dau dong lai va bat nham "bản đã gỡ" (codex_env_policy.py, khong lien quan CODEX_AUTH_JSON; co y het tren base).
CUM5 = ["đã gỡ", "đã bỏ", "không còn hỗ trợ", "removed"]
def don_vi(t, tach_muc):
    out = []
    for p in re.split(r"\n\s*\n", t):
        out += re.split(r"(?m)^(?=- )", p) if tach_muc else [p]
    return out
def vi_pham(t, tach_muc):
    v = []
    for p in don_vi(t, tach_muc):
        if "CODEX_AUTH_JSON" not in p:
            continue
        for c in CUM5:
            for mm in re.finditer(re.escape(c), p):
                truoc = p[:mm.start()].rstrip().split()[-1:]
                if not (truoc and truoc[0].lower() in ("chưa", "không")):
                    v.append((c, p[max(0, mm.start() - 60):mm.end()].replace("\n", " ")))
    return v
def a5(*ts):
    return not any(vi_pham(t, True) for t in ts)
for ten, t, tb in (("GOI_AGENT_DA_NEN.md", goi, blob(B, "docs/GOI_AGENT_DA_NEN.md")), ("CLAUDE.md", cl, cl_b)):
    print(f"# A5 {ten}: vi pham theo doan-cach-dong-trong: merge {len(vi_pham(t, False))} / base {len(vi_pham(tb, False))}; "
          f"theo doan+muc: merge {len(vi_pham(t, True))} / base {len(vi_pham(tb, True))}" + "".join(f" | {x!r}" for x in vi_pham(t, False)))
ghi("A5", a5(goi, cl), [("them 'code đọc CODEX_AUTH_JSON đã gỡ'", a5(goi.replace(khoi, khoi + " Code đọc CODEX_AUTH_JSON đã gỡ."), cl)),
                        ("them vao gach Refresh token cua CLAUDE.md", a5(goi, cl.replace("**Từ 05-11-2026 biến này là đường cũ**", "**Từ 05-11-2026 biến này là đường cũ; code đọc CODEX_AUTH_JSON đã gỡ**", 1)))])

# A6 — CLAUDE.md dong 673–683 cua base giu nguyen byte (theo noi dung)
doan6 = "\n".join(cl_b.splitlines()[672:683])
print(f"# A6 doan base 673–683: {len(doan6)} ky tu, dong dau {cl_b.splitlines()[672][:80]!r}")
ghi("A6", doan6 in cl and len(doan6) > 0, [("sua doan su co 15-08", doan6 in cl.replace(cl_b.splitlines()[675], cl_b.splitlines()[675] + " X", 1))])

print(f"TONG: {sum(ket)}/{len(ket)} tieu chi DAT (A1–A6)")
sys.exit(0 if all(ket) else 1)
