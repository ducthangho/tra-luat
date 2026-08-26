"""Phan chung cho packet #324 pha A1 — danh sach CHO PHEP cua agent read-only.

Chay: python .claude/hooks/pretooluse_guard_test.py
Thoat 0 khi VA CHI KHI moi ca DAT va moi dot bien BI GIET.

Doc truoc khi sua: mot ca xanh vi LY DO KHAC van la ca xanh. Nen moi tinh chat cua guard deu
co mot DOT BIEN rieng o duoi; bo mot dot bien la bo mot chot. Dot bien chay tren BAN SAO trong
thu muc tam (khong bao gio ghi vao tep that — bai hoc "dot bien ghi vao tep THAT roi khoi phuc
trong finally la bom hen gio"), moi ban sao mot TEN RIENG + chay bang `-B`, de tranh va cham
`.pyc` da tung tuoc rang moi mutant (CPython coi .pyc con hop le theo (mtime GIAY, kich thuoc)).
"""
import json
import pathlib
import subprocess
import sys
import tempfile

HERE = pathlib.Path(__file__).resolve().parent
GUARD = HERE / "pretooluse_guard.py"

# 8 hinh dang GHI — dung bang da do 2026-08-26 trong Issue #324, noi ca 8 DI LOT.
GHI = [
    ("sed -i tai cho", "sed -i 's/x/y/' scripts/tl.py"),
    ("chuyen huong >", 'echo "r" > scripts/tl.py'),
    ("chuyen huong >>", 'echo "r" >> scripts/tl.py'),
    ("tee", 'echo "r" | tee scripts/tl.py'),
    ("cp de len", "cp /tmp/x scripts/tl.py"),
    ("mv de len", "mv /tmp/x scripts/tl.py"),
    ("python -c ghi", "python -c \"open('scripts/tl.py','w').write('x')\""),
    ("truncate : >", ": > scripts/tl.py"),
]
# Lenh DOC hop le — CO ong, `;`, `$( )`, `2>/dev/null`. Day la ca chong tai dien #314:
# allowlist kieu tien to se chan oan sach nhung dong nay.
DOC = [
    "git log --oneline -1",
    "git status --porcelain | wc -l",
    "python scripts/tl.py cat-audit --json | head -40",
    'M=$(git rev-parse HEAD); echo "$M"',
    'rg -n "def main" .claude/dev | head -5',
    "git diff --numstat HEAD~1..HEAD -- docs/ 2>/dev/null | sort",
    "cat CLAUDE.md | grep -c python",
]
# Lenh GHI giau BEN TRONG thay the lenh. Vo lenh trong ra la vo hai (`echo THAYTHE`), nen
# chi bat duoc neu guard KIEM DE QUY phan trong. Dot bien m3 song o luot dau chinh vi
# bang GHI o tren khong co hinh dang nay — dot bien tim ra lo hong cua BO TEST, dung viec.
GHI_LONG = [
    ("ghi long trong $()", 'echo "$(cp /tmp/x scripts/tl.py)"'),
    ("ghi long trong backtick", 'echo "`sed -i s/a/b/ scripts/tl.py`"'),
    ("ghi long hai tang", 'echo "$(echo "$(mv /tmp/x scripts/tl.py)")"'),
    # Ba hinh dang duoi do duoc bang PHEP RA DOI NGHICH sau khi suite dau tien da xanh 8/8 —
    # tuc suite xanh KHONG chung minh khong con lo. Xuong dong: `shlex` whitespace_split nuot
    # newline nen hai lenh gop lam mot doan, chi chuong trinh DAU bi kiem.
    ("xuong dong tach lenh", "echo hi\ncp /tmp/x scripts/tl.py"),
    ("xuong dong + sed -i", "git log -1\nsed -i 's/a/b/' scripts/tl.py"),
    ("thay the tien trinh <()", "cat <(cp /tmp/x scripts/tl.py)"),
    # Ca nay chi LOT khi bo CA HAI chot (heredoc + tach xuong dong) — xem m10.
    ("ghi trong than heredoc", "python scripts/tl.py <<'E'\ncp /tmp/x scripts/tl.py\nE"),
]
# 11 ca do CROSS-REVIEW CODEX (PR #328) tim ra — 5 finding P1, ca 11 DA TAI HIEN la ALLOW
# tren ban da day. Chung o day vi bo test truoc do xanh 8/8 ma khong thay cai nao.
GHI_CHE_DO = [
    ("chuyen huong &>", "echo x &> scripts/tl.py"),
    ("chuyen huong &>>", "echo x &>> scripts/tl.py"),
    ("chuyen huong doc-ghi <>", "cat <> scripts/tl.py"),
    ("sort -o", "sort -o scripts/tl.py CLAUDE.md"),
    ("uniq doi so ra", "uniq CLAUDE.md scripts/tl.py"),
    ("diff --output=", "diff --output=scripts/tl.py CLAUDE.md CONTEXT.md"),
    ("ruff format", "ruff format .claude/hooks/pretooluse_guard.py"),
    ("sed lenh w", "sed -n 'w scripts/tl.py' CLAUDE.md"),
    ("git branch tao ref", "git branch readonly-agent-wrote-this"),
    ("git tag tao ref", "git tag readonly-agent-wrote-this"),
    ("awk system co khoang trang", 'awk \'BEGIN { system ("touch scripts/written") }\''),
]
# Ca DUONG di kem — cross-review doi giu lai che do DOC cua dung nhung chuong trinh tren, kẻo
# ban va bien thanh chan oan. Khong co danh sach nay thi "deny 11/11" khong noi len dieu gi.
DOC_CHE_DO = [
    "sort CLAUDE.md | head -3",
    "uniq CLAUDE.md | wc -l",
    "diff CLAUDE.md CONTEXT.md | head -5",
    "ruff check .claude/hooks/pretooluse_guard.py",
    "git branch --list",
    "git tag --list",
    "git branch",
    "git log --oneline -1 2>/dev/null",
]
DOI_CHUNG = [("rm -rf /x", "ask"), ("git push origin master --force", "ask")]
AGENT = ("tl-auditor", "tl-rasoat")


def hoi(guard, cmd, agent=None):
    d = {"tool_name": "Bash", "tool_input": {"command": cmd}}
    if agent:
        d["agent_type"] = agent
    p = subprocess.run([sys.executable, "-B", str(guard)], input=json.dumps(d),
                       capture_output=True, text=True)
    out = (p.stdout or "").strip()
    if not out:
        return "allow", ""
    o = json.loads(out)["hookSpecificOutput"]
    return o["permissionDecision"], o["permissionDecisionReason"]


def t1_agent_bi_chan_moi_hinh_dang_ghi(g):
    xau = [t for t, c in GHI if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"8 hinh dang ghi -> deny {8 - len(xau)}/8" + (f"; LOT: {xau}" if xau else ""))


def t2_ca_hai_agent_deu_bi_chan(g):
    xau = [(a, t) for a in AGENT for t, c in GHI if hoi(g, c, a)[0] != "deny"]
    return (not xau, f"2 agent x 8 ca -> deny {16 - len(xau)}/16" + (f"; LOT: {xau}" if xau else ""))


def t3_khong_chan_oan_lenh_doc(g):
    xau = [c for c in DOC if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"lenh doc hop le -> allow {len(DOC) - len(xau)}/{len(DOC)}"
                     + (f"; CHAN OAN: {xau}" if xau else ""))


def t4_phien_chinh_y_het_ban_master(g):
    """Doi chieu SONG SONG voi ban tren origin/master. Khong lay duoc ban ay => DO, khong bo qua."""
    try:
        cu = subprocess.run(["git", "show", "origin/master:.claude/hooks/pretooluse_guard.py"],
                            cwd=HERE, capture_output=True, text=True, check=True).stdout
    except Exception as e:
        return (False, f"KHONG DO DUOC ban master de doi chieu ({type(e).__name__}) -> fail-close")
    if not cu.strip():
        return (False, "ban master rong -> fail-close")
    with tempfile.TemporaryDirectory() as d:
        nen = pathlib.Path(d) / "guard_master.py"
        nen.write_text(cu, encoding="utf-8")
        moi_lenh = [c for _, c in GHI] + DOC + [c for c, _ in DOI_CHUNG]
        lech = [c for c in moi_lenh if hoi(g, c)[0] != hoi(nen, c)[0]]
    return (not lech, f"phien chinh: {len(moi_lenh) - len(lech)}/{len(moi_lenh)} khop master"
                      + (f"; LECH: {lech}" if lech else ""))


def t5_doi_chung_van_ask(g):
    xau = [c for c, mong in DOI_CHUNG if hoi(g, c)[0] != mong]
    return (not xau, f"doi chung -> ask {len(DOI_CHUNG) - len(xau)}/{len(DOI_CHUNG)}"
                     + (f"; SAI: {xau}" if xau else ""))


def t6_agent_la_khong_bi_ap_luat(g):
    """`Explore` khong nam trong _AGENT_CHI_DOC => phai xu nhu phien chinh, khong chan."""
    xau = [c for _, c in GHI if hoi(g, c, "Explore")[0] == "deny"]
    return (not xau, f"agent ngoai danh sach: khong ap luat ({len(xau)} ca bi chan oan)")


def t8_ghi_giau_qua_tach_lenh_va_thay_the(g):
    xau = [t for t, c in GHI_LONG if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"ghi giau ($() · backtick · xuong dong · <()) -> deny {len(GHI_LONG) - len(xau)}/{len(GHI_LONG)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t9_che_do_ghi_cua_chuong_trinh_cho_phep(g):
    xau = [t for t, c in GHI_CHE_DO if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"che do GHI (11 ca cross-review) -> deny "
                     f"{len(GHI_CHE_DO) - len(xau)}/{len(GHI_CHE_DO)}"
                     + (f"; LOT: {xau}" if xau else ""))


def t10_che_do_doc_cua_cung_chuong_trinh_khong_bi_chan(g):
    xau = [c for c in DOC_CHE_DO if hoi(g, c, "tl-auditor")[0] != "allow"]
    return (not xau, f"che do DOC -> allow {len(DOC_CHE_DO) - len(xau)}/{len(DOC_CHE_DO)}"
                     + (f"; CHAN OAN: {xau}" if xau else ""))


def t7_nhom_mutate_tra_luat_bi_chan(g):
    ca = ["python scripts/tl.py corpus-audit --apply",
          "python scripts/tl.py reg-delete 123",
          "python scripts/tl.py golden-test --write"]
    xau = [c for c in ca if hoi(g, c, "tl-auditor")[0] != "deny"]
    return (not xau, f"nhom mutate tra-luat -> deny {len(ca) - len(xau)}/{len(ca)}")


CA = [t1_agent_bi_chan_moi_hinh_dang_ghi, t2_ca_hai_agent_deu_bi_chan,
      t3_khong_chan_oan_lenh_doc, t4_phien_chinh_y_het_ban_master,
      t5_doi_chung_van_ask, t6_agent_la_khong_bi_ap_luat,
      t7_nhom_mutate_tra_luat_bi_chan, t8_ghi_giau_qua_tach_lenh_va_thay_the,
      t9_che_do_ghi_cua_chuong_trinh_cho_phep,
      t10_che_do_doc_cua_cung_chuong_trinh_khong_bi_chan]

# --- DOT BIEN: moi cai go DUNG MOT tinh chat, va phai lam it nhat mot ca DO ---
DOT_BIEN = [
    ("m1_cho_sed_awk_vao_danh_sach", '"git", "python", "python3", "py", "find",',
     '"sed", "awk", "git", "python", "python3", "py", "find",'),
    ("m2_bo_chot_chuyen_huong", 'if ">" in t:', 'if False:'),
    ("m3_bo_de_quy_thay_the", "ly = _kiem_lenh_agent(t, sau + 1)", "ly = None"),
    ("m4_bo_kiem_python", '"python": _kiem_python, ', ""),
    ("m5_cho_tee_vao_danh_sach", '"rg", "grep",', '"tee", "cp", "mv", "rg", "grep",'),
    ("m6_rong_danh_sach_agent", '_AGENT_CHI_DOC = frozenset({"tl-auditor", "tl-rasoat"})',
     "_AGENT_CHI_DOC = frozenset()"),
    ("m7_bo_chot_tl_mutate", "if _TL_CAM.search(cmd):", "if False:"),
    ("m8_bo_tach_xuong_dong", 'if "\\n" in cmd:', "if False:"),
    ("m9_bo_thay_the_tien_trinh", 'if cmd[i:i + 2] in ("$(", "<("):', 'if cmd[i:i + 2] == "$(":'),
    # GHEP hai chot: rieng le thi cai nay che cai kia nen dot bien don le SONG — khong phai vi
    # test yeu ma vi hai lop doc lap cung chan mot ca. Doctrine: "phai dot bien ghep ca bon".
    ("m12_bo_kiem_sort", '"sort": _kiem_sort,', ""),
    ("m13_bo_kiem_uniq", '"uniq": _kiem_uniq,', ""),
    ("m14_bo_chot_vi_tri_git_ref",
     'if [a for a in con if not a.startswith("-")] and not any(', "if False and any("),
    ("m10_ghep_bo_heredoc_va_tach_dong",
     ('if "<<" in cmd:', 'if "\\n" in cmd:'), ("if False:", "if False:")),
]


def chay():
    goc = GUARD.read_text(encoding="utf-8")
    print("CA:")
    do = 0
    for f in CA:
        ok, mo_ta = f(GUARD)
        do += not ok
        print(f"  {'DAT ' if ok else 'DO  '} {f.__name__:38} {mo_ta}")

    print("DOT BIEN (moi cai PHAI lam it nhat mot ca DO):")
    song = []
    with tempfile.TemporaryDirectory() as d:
        for ten, cu, moi in DOT_BIEN:
            cap = list(zip(cu, moi)) if isinstance(cu, tuple) else [(cu, moi)]
            if any(c not in goc for c, _ in cap):
                print(f"  DO   {ten:30} MOC KHONG CON TRONG MA -> dot bien chua tung chay")
                song.append(ten)
                continue
            ma = goc
            for c, m in cap:
                ma = ma.replace(c, m, 1)
            tep = pathlib.Path(d) / f"guard_{ten}.py"      # TEN RIENG tung dot bien
            tep.write_text(ma, encoding="utf-8")
            giet = [f.__name__ for f in CA if not f(tep)[0]]
            if giet:
                print(f"  GIET {ten:30} lam DO: {', '.join(giet)}")
            else:
                print(f"  SONG {ten:30} KHONG ca nao do -> chot nay KHONG CO RANG")
                song.append(ten)

    tap_giet = len(DOT_BIEN) - len(song)
    print(f"TONG: CA {len(CA) - do}/{len(CA)} dat · DOT BIEN {tap_giet}/{len(DOT_BIEN)} bi giet")
    # Vi ngu phai doi SO DUONG hai ve, khong duoc thoa man boi so rong (bai hoc "so rong thoa
    # `not DO`" cua #319): so ca da chay phai BANG so ca dang ky VA > 0.
    dat = (len(CA) > 0 and do == 0 and len(DOT_BIEN) > 0 and not song)
    print("TONG:", "DAT" if dat else "DO")
    return 0 if dat else 1


if __name__ == "__main__":
    sys.exit(chay())
