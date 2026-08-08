# -*- coding: utf-8 -*-
"""F3-03 — nghiem thu cho `.claude/dev/packet_loop.py`.

Ly do suite nay ton tai: chu kho doi packet phai CHUNG MINH tran vong lap hoat dong,
khong chi khai la co. Mot vong lap tu goi lai chinh no ma khong co tran DA DUOC KIEM la
cach nhanh nhat de dot het ngan sach vao mot loi no khong sua noi.

Moi ca chay CHINH entrypoint qua subprocess voi `--state-dir` rieng trong Temp — khong goi
ham noi bo. Cung doctrine voi `.githooks/eol_policy_test.py::case_real_hook_rename_only_bi_chan`:
goi that thi moi bat duoc loi cua lop CLI/argparse, goi ham noi bo thi khong.

Ma thoat la thu duy nhat dang tin: 0 di tiep · 3 DUNG theo chot · 4 vi pham cross-provider ·
5 con comment chua dang. Moi ca doi DUNG ma thoat, khong doi rc=0 chung chung.
"""
from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

sys.dont_write_bytecode = True

_LOOP = Path(__file__).resolve().parent / "packet_loop.py"

RC_OK, RC_USAGE, RC_STOP, RC_PROVIDER, RC_UNPOSTED = 0, 2, 3, 4, 5


def _chay(state_dir: Path, *argv: str) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, str(_LOOP), "--state-dir", str(state_dir), *argv],
        capture_output=True, text=True, encoding="utf-8", errors="replace")


def _init(state_dir: Path, packet: int = 999, executor: str = "codex",
          reviewer: str = "claude") -> subprocess.CompletedProcess:
    return _chay(state_dir, "init", "--packet", str(packet), "--mission", "48",
                 "--executor", executor, "--reviewer", reviewer)


def _dang_het(state_dir: Path, packet: int = 999) -> None:
    """Dang moi comment dang cho — de ca sau khong bi chan boi RC_UNPOSTED."""
    for _ in range(50):
        r = _chay(state_dir, "mark-posted", "--packet", str(packet),
                  "--url", "https://example.invalid/c")
        if r.returncode != RC_OK:
            return


def _trang_thai(state_dir: Path, packet: int = 999) -> dict:
    r = _chay(state_dir, "status", "--packet", str(packet))
    return json.loads(r.stdout)


# ─────────────────────────── tran 3 luot ───────────────────────────

def case_tran_3_luot_chan_luot_4(sd: Path) -> bool:
    """Ba luot di qua; luot THU TU bi chan bang rc=3 va state ve `blocked`.

    Day la phan chung cua `max_attempts_per_packet: 3` trong envelope #48.
    """
    _init(sd); _dang_het(sd)
    for i in range(3):
        r = _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex")
        if r.returncode != RC_OK:
            print(f"    luot {i+1} le ra phai qua, rc={r.returncode} {r.stderr.strip()[:80]}")
            return False
        _dang_het(sd)
    r = _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex")
    if r.returncode != RC_STOP or "TRAN_LUOT" not in r.stderr:
        print(f"    luot 4 phai DUNG rc=3/TRAN_LUOT, thuc te rc={r.returncode}")
        return False
    return _trang_thai(sd)["state"] == "blocked"


# ─────────────────────── same-failure-limit 2 ───────────────────────

def case_cung_finding_lap_2_lan_thi_blocked(sd: Path) -> bool:
    """CUNG mot finding lap lan 2 ⇒ DUNG ngay, khong doi het 3 luot.

    Day la ca chu kho doi tan mat: bom mot finding lap lai de thay no dung.
    """
    _init(sd); _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    r1 = _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
               "--verdict", "changes_requested", "--finding", "release-verify do vi manifest lech")
    if r1.returncode != RC_OK:
        print(f"    lan 1 le ra phai qua, rc={r1.returncode}")
        return False
    _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    # Dien dat lech khoang trang + hoa thuong — van phai tinh la CUNG mot finding.
    r2 = _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
               "--verdict", "changes_requested",
               "--finding", "  RELEASE-VERIFY  do vi   manifest LECH ")
    if r2.returncode != RC_STOP or "SAME_FAILURE_LIMIT" not in r2.stderr:
        print(f"    lan 2 phai DUNG rc=3/SAME_FAILURE_LIMIT, thuc te rc={r2.returncode}")
        return False
    return _trang_thai(sd)["state"] == "blocked"


def case_finding_khac_nhau_khong_bi_chan(sd: Path) -> bool:
    """Chieu nguoc lai: hai finding KHAC nhau khong duoc kich tran.

    Thieu ca nay thi `same_failure_limit` co the chi la bo dem review tho — dung sai cho,
    va vong lap se chet oan o luot 2 du dang tien trien.
    """
    _init(sd); _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    r1 = _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
               "--verdict", "changes_requested", "--finding", "loi thu nhat")
    _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    r2 = _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
               "--verdict", "changes_requested", "--finding", "loi thu hai hoan toan khac")
    if r1.returncode != RC_OK or r2.returncode != RC_OK:
        print(f"    hai finding khac nhau bi chan oan: rc={r1.returncode}/{r2.returncode}")
        return False
    return _trang_thai(sd)["state"] != "blocked"


# ─────────────────────────── cross-provider ───────────────────────────

def case_executor_trung_reviewer_bi_chan_tu_init(sd: Path) -> bool:
    r = _init(sd, executor="claude", reviewer="claude")
    return r.returncode == RC_PROVIDER and "CROSS_PROVIDER" in r.stderr


def case_review_sai_provider_bi_chan(sd: Path) -> bool:
    """executor `codex` khong duoc tu review viec cua chinh no."""
    _init(sd); _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    r = _chay(sd, "record-review", "--packet", "999", "--provider", "codex",
              "--verdict", "approve")
    return r.returncode == RC_PROVIDER and "CROSS_PROVIDER" in r.stderr


def case_executor_sai_provider_bi_chan(sd: Path) -> bool:
    _init(sd); _dang_het(sd)
    r = _chay(sd, "begin-attempt", "--packet", "999", "--provider", "claude")
    return r.returncode == RC_PROVIDER and "CROSS_PROVIDER" in r.stderr


# ─────────────────────────── dung cung truoc merge ───────────────────────────

def case_guard_chan_moi_hanh_vi_cam(sd: Path) -> bool:
    """Khong hanh vi cam nao lot, va KHONG co co noi nao."""
    for act in ("merge", "deploy", "live", "secrets", "force-push",
                "delete-branch", "delete-worktree", "edit-other-spec"):
        r = _chay(sd, "guard", "--action", act)
        if r.returncode != RC_STOP or "CAM_TRONG_VONG_LAP" not in r.stderr:
            print(f"    `{act}` le ra phai bi chan, rc={r.returncode}")
            return False
    return True


def case_approve_dung_truoc_merge(sd: Path) -> bool:
    """`approve` KHONG dan toi merge — no dan toi `awaiting_merge` va het quyen."""
    _init(sd); _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    r = _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
              "--verdict", "approve")
    if r.returncode != RC_OK:
        return False
    _dang_het(sd)
    return (_trang_thai(sd)["state"] == "awaiting_merge"
            and _chay(sd, "guard", "--action", "merge").returncode == RC_STOP)


# ─────────────────── transition phai co dau vet ben ───────────────────

def case_comment_chua_dang_thi_chan_di_tiep(sd: Path) -> bool:
    """Quen dang comment ⇒ vong lap KHONG di tiep duoc.

    Bien "moi transition ghi comment vao Issue" tu loi hua thanh co che: khong dang thi
    khong advance, nen transition khong the troi im lang roi mat dau trong context phien.
    """
    _init(sd)  # co Y khong goi _dang_het
    r = _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex")
    if r.returncode != RC_UNPOSTED or "CHUA_DANG" not in r.stderr:
        print(f"    phai chan bang rc=5, thuc te rc={r.returncode}")
        return False
    _dang_het(sd)
    return _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex").returncode == RC_OK


def case_blocked_thi_khong_tu_di_tiep(sd: Path) -> bool:
    """Da `blocked` thi moi lenh chuyen trang thai deu dung — khong tu go."""
    _init(sd); _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
          "--verdict", "changes_requested", "--finding", "x")
    _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    _chay(sd, "record-review", "--packet", "999", "--provider", "claude",
          "--verdict", "changes_requested", "--finding", "x")
    _dang_het(sd)
    return (_chay(sd, "begin-attempt", "--packet", "999",
                  "--provider", "codex").returncode == RC_STOP
            and _chay(sd, "status", "--packet", "999").returncode == RC_STOP)


def case_loi_quota_khong_tieu_thu_attempt(sd: Path) -> bool:
    """§8: quota/rate-limit KHONG an vao tran 3 luot noi dung.

    Thieu chot nay thi hai lan provider nghen la du dot sach tran trong khi executor
    chua sai lan nao — tran bao ve nham thu no phai bao ve.
    """
    _init(sd); _dang_het(sd)
    for _ in range(3):
        _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
        r = _chay(sd, "void-attempt", "--packet", "999", "--reason", "quota")
        if r.returncode != RC_OK:
            print(f"    void-attempt le ra phai qua, rc={r.returncode}")
            return False
        _dang_het(sd)
    if _trang_thai(sd)["attempts_used"] != 0:
        return False
    # Luot noi dung that van con nguyen quyen di tiep.
    return _chay(sd, "begin-attempt", "--packet", "999",
                 "--provider", "codex").returncode == RC_OK


def case_ly_do_void_ngoai_allowlist_bi_chan(sd: Path) -> bool:
    """Khong cho tra luot bang ly do tu che — allowlist la co Y."""
    _init(sd); _dang_het(sd)
    _chay(sd, "begin-attempt", "--packet", "999", "--provider", "codex"); _dang_het(sd)
    r = _chay(sd, "void-attempt", "--packet", "999", "--reason", "toi-thay-khong-dang-tinh")
    return r.returncode == RC_USAGE and "LY_DO_LA" in r.stderr


def case_state_dir_mac_dinh_bi_gitignore_phu(sd: Path) -> bool:
    """State MAC DINH khong duoc lam ban `git status`.

    Ban dau mac dinh la `.claude/dev/.state` — chay mot lenh la `git status` co ngay mot muc
    `??`. Trong kho nay cay ban keo theo ca gate, va state la runtime artifact chu khong phai
    ma nguon. Chua bang cach tai dung ten `.tl_state` MA `.gitignore` DA phu san (dong 22,
    doctrine v1.34.2), thay vi sua `.gitignore` — path do nam ngoai write-set cua packet.

    Ca nay hoi CHINH CLI xem mac dinh cua no o dau (khong doan), roi doi chieu voi `.gitignore`
    THAT cua kho. Doi ten thu muc, hoac go dong ignore, deu lam ca do.
    """
    r = subprocess.run([sys.executable, str(_LOOP), "where"],
                       capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode != RC_OK:
        print(f"    `where` phai tra 0, thuc te rc={r.returncode}")
        return False
    # `where` in JSON ensure_ascii ⇒ thuan ASCII ⇒ khong dinh cp1258 cua pipe tren may nay.
    duong = Path(json.loads(r.stdout)["state_dir"])
    goc = Path(__file__).resolve().parent.parent.parent
    mau = {d.strip().rstrip("/") for d in (goc / ".gitignore").read_text(
        encoding="utf-8").splitlines() if d.strip() and not d.strip().startswith("#")}
    phu = mau & set(duong.parts)
    if not phu:
        print(f"    thu muc state mac dinh {duong.parent} KHONG duoc .gitignore phu")
        return False
    return True


CASES = [
    case_tran_3_luot_chan_luot_4,
    case_state_dir_mac_dinh_bi_gitignore_phu,
    case_loi_quota_khong_tieu_thu_attempt,
    case_ly_do_void_ngoai_allowlist_bi_chan,
    case_cung_finding_lap_2_lan_thi_blocked,
    case_finding_khac_nhau_khong_bi_chan,
    case_executor_trung_reviewer_bi_chan_tu_init,
    case_review_sai_provider_bi_chan,
    case_executor_sai_provider_bi_chan,
    case_guard_chan_moi_hanh_vi_cam,
    case_approve_dung_truoc_merge,
    case_comment_chua_dang_thi_chan_di_tiep,
    case_blocked_thi_khong_tu_di_tiep,
]


def main() -> int:
    if hasattr(sys.stdout, "reconfigure"):
        sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    dat = 0
    hong = []
    for case in CASES:
        with tempfile.TemporaryDirectory(prefix="packet_loop_") as tmp:
            try:
                ok = bool(case(Path(tmp)))
            except Exception as exc:                     # noqa: BLE001 — bao loi, khong nuot
                ok = False
                print("  ! %s: %r" % (case.__name__, exc))
        print("%s %s" % ("PASS" if ok else "FAIL", case.__name__))
        if ok:
            dat += 1
        else:
            hong.append(case.__name__)
    print("\n%d/%d dat" % (dat, len(CASES)))
    if hong:
        print("HONG: %s" % ", ".join(hong))
    return 0 if not hong else 1


if __name__ == "__main__":
    sys.exit(main())
