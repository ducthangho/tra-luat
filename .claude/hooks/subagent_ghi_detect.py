#!/usr/bin/env python3
"""May PHAT HIEN GHI cho subagent tu khai read-only — packet #329 pha 2.

Doc truoc: `ops/specs/agent-may-phat-hien-ghi.md` (dac ta pha 1, land o 6031222).
Tep nay KHONG nhac lai dac ta; day chi la cai dat cua ba quyet dinh da chot o
https://github.com/ducthangho/tra-luat/issues/329#issuecomment-5429476065 :

  D1 = CHI TO CAO. Khong CHAN (hieu luc `SubagentStop` exit 2 CHUA AI DO — xem `A10`
       o duoi, va cho toi khi co phep do thi mot chot dua vao no la mot chot chua biet
       co ton tai khong). Khong HOAN TAC (duong hoan tac bien chinh detector thanh mot
       DUONG GHI MOI — doi mot lo lay mot lo).
  D2 = GIU bo phan tich chuoi cua #324. Hai lop doc lap, va lop 1 cho phan hoi TRUOC
       lenh; lop nay chi thay o `SubagentStop`, tuc SAU tac dung phu.
  D3 = MO RONG HEP: them DUNG mot co `--ignored`. Ly do do duoc: `.tl_state/` bi
       ignore (`.gitignore:22`) va do la noi duong ghi THAT da do duoc rot xuong
       (`tl nlm-reconcile` khong `--apply` van tao `.tl_state/reconcile_plan_*.json`).
       KHONG mo rong sang toan he tep hay mang — hai vung ay VAN MU, va bao cao phai
       goi ten chung.

BA TRANG THAI, khong phai hai: `clean` · `changed` · `unknown`. `unknown` KHONG duoc
doc thanh `clean` — do la `None != False`, va no la ly do duy nhat tep nay dai hon
mot ham `diff`.

ANH CHUP KHONG NAM TRONG WORKTREE DANG DO. Neu nam trong, may tu tao dung thay doi ma
no to cao — dac ta goi thang ra dieu nay.
"""
import hashlib
import json
import os
import pathlib
import subprocess
import sys
import tempfile
import time

# Chi hai agent tu khai read-only. Mo rong tap nay phai co quyet dinh + ca do rieng.
_AGENT = frozenset({"tl-auditor", "tl-rasoat"})

# Tuoi tho anh chup. Con so nay CHUA duoc do bang luot chay dai/chay chong (dac ta §4.5
# noi vay); 24h la tran AN TOAN de don rac, khong phai mot phep do.
_TUOI_TOI_DA_GIAY = 24 * 3600

_MA_CLEAN, _MA_CHANGED, _MA_UNKNOWN = 0, 0, 0   # D1: CHI TO CAO -> khong ma nao chan


def _thu_muc_anh():
    """NGOAI worktree. `TMPDIR` de test tro sang thu muc rieng."""
    d = pathlib.Path(os.environ.get("TL_SUBAGENT_SNAP_DIR")
                     or pathlib.Path(tempfile.gettempdir()) / "tl-subagent-snap")
    d.mkdir(parents=True, exist_ok=True)
    return d


def _git(cwd, *args):
    """Tra (rc, stdout). `--no-optional-locks` la BAT BUOC o CA HAI lan chup:
    `git status` tran co the refresh stat data va GHI `.git/index` ma porcelain khong
    lo — dac ta §2 co phep do A/B cho viec nay. Thieu co ay thi chinh detector ghi."""
    try:
        p = subprocess.run(["git", "--no-optional-locks", "-C", str(cwd), *args],
                           capture_output=True, text=True, timeout=120)
    except (OSError, subprocess.SubprocessError) as e:
        return 128, "loi goi git: %s" % e
    return p.returncode, p.stdout


def _chup(cwd):
    """Tra (anh, ly_do_unknown). anh=None khi khong do duoc."""
    rc, top = _git(cwd, "rev-parse", "--show-toplevel")
    if rc != 0:
        return None, "cwd khong phai worktree git: %s" % str(cwd)
    top = top.strip()
    rc, head = _git(cwd, "rev-parse", "HEAD")
    if rc != 0:
        return None, "khong doc duoc HEAD"
    # D3: `--ignored` la DUY NHAT mo rong. Giu NGUYEN VAN tung ban ghi, khong dem dong.
    rc, st = _git(cwd, "status", "--porcelain=v1", "-uall", "--ignored")
    if rc != 0:
        return None, "git status that bai (rc=%d)" % rc
    idx = pathlib.Path(top) / ".git" / "index"
    van_tay_idx = ""
    if idx.is_file():
        van_tay_idx = hashlib.sha256(idx.read_bytes()).hexdigest()[:16]
    noi_dung, mu = _van_tay_noi_dung(top, st)
    return {
        "top": top,
        "head": head.strip(),
        "status": st,
        "noi_dung": noi_dung,               # path -> van tay NOI DUNG
        "mu_noi_dung": mu,                  # path KHONG noi-dung-hoa duoc
        "index_sha256_16": van_tay_idx,     # A12: byte cua index KHONG duoc doi
        "luc": time.time(),
    }, None


# Tran kich thuoc khi bam noi dung. Tep lon hon thi KHONG bam — va duoc khai la MU chu
# khong lang le bo qua.
_TRAN_BAM_BYTE = 8 * 1024 * 1024


def _duong_tu_porcelain(dong):
    """Tra duong dan tu mot ban ghi porcelain v1. `R  cu -> moi` tra ban MOI."""
    if len(dong) < 4:
        return None
    p = dong[3:]
    if " -> " in p:                       # rename/copy
        p = p.split(" -> ", 1)[1]
    if p.startswith('"') and p.endswith('"'):
        # git trich dan khi ten co ky tu la; giai bang chinh luat cua no
        try:
            p = p[1:-1].encode("latin-1", "backslashreplace").decode("unicode_escape")
        except Exception:
            return None
    return p


def _van_tay_noi_dung(top, st):
    """Bam NOI DUNG tung duong dan trong porcelain. Tra (anh_xa, danh_sach_MU).

    VI SAO CAN — lo P1 `status-on-dinh-che-giau-lan-ghi` (cross-review PR #342, DA TAI HIEN):
    ban truoc chi so TAP DONG porcelain cong bam `.git/index`. Mot tep DA co mat truoc Start
    o cung trang thai (`!! .tl_state/plan.json`) bi GHI DE thi dong porcelain KHONG doi va
    index KHONG doi => may bao `clean` trong khi byte da khac. Do duoc: `TRUOC` -> `SAU-DA-
    BI-DE`, ket qua `clean`. Vung mu nam DUNG o `.tl_state/` — noi D3 vua mo ra, va noi
    duong ghi that da do duoc rot xuong.

    VI SAO BAM DUOC, khong phai vi re: voi `-uall --ignored` git tra TUNG TEP chu khong tra
    thu muc — do tren kho nay: 61 ban ghi, 0 ban ghi ket thuc bang `/`. Nen tap can bam la
    huu han va biet truoc, khong phai "duyet ca cay".

    Duong nao KHONG bam duoc (thu muc, symlink, qua tran, doc khong duoc) thi vao danh sach
    MU va duoc GOI TEN o bao cao — khong lang le bo qua."""
    anh_xa, mu = {}, []
    for dong in st.splitlines():
        if not dong.strip():
            continue
        duong = _duong_tu_porcelain(dong)
        if duong is None:
            mu.append(dong[:80])
            continue
        f = pathlib.Path(top) / duong
        try:
            if f.is_symlink():
                anh_xa[duong] = "symlink:" + os.readlink(f)   # KHONG di theo
                continue
            if f.is_dir():
                mu.append(duong + " (thu muc)")
                continue
            if not f.is_file():
                mu.append(duong + " (khong phai tep thuong)")
                continue
            if f.stat().st_size > _TRAN_BAM_BYTE:
                mu.append(duong + " (qua tran %d byte)" % _TRAN_BAM_BYTE)
                continue
            anh_xa[duong] = hashlib.sha256(f.read_bytes()).hexdigest()[:16]
        except OSError as e:
            mu.append("%s (khong doc duoc: %s)" % (duong, e.__class__.__name__))
    return anh_xa, sorted(mu)


def _ghi_nguyen_tu(dich, du_lieu):
    """`mkstemp` (ten ngau nhien + O_EXCL) roi `os.replace`. Ten tam DOAN DUOC + `open(w)`
    la duong de len tep khac qua symlink — bai hoc da tra gia trong kho nay."""
    fd, tam = tempfile.mkstemp(dir=str(dich.parent), prefix=".tam-")
    try:
        with os.fdopen(fd, "w", encoding="utf-8") as f:
            json.dump(du_lieu, f, ensure_ascii=True)
            f.flush()
            os.fsync(f.fileno())
        os.replace(tam, dich)
    except BaseException:
        try:
            os.unlink(tam)
        except OSError:
            pass
        raise


def _don_rac(thu_muc, tru=None):
    """Tuoi tho huu han + chong dung lai. Loi don rac KHONG duoc lam hong phep do."""
    nay = time.time()
    for p in thu_muc.glob("*.json"):
        if tru and p.name == tru:
            continue
        try:
            if nay - p.stat().st_mtime > _TUOI_TOI_DA_GIAY:
                p.unlink()
        except OSError:
            pass


def _bao(ket_qua, ly_do, chi_tiet=None):
    """In BA trang thai ra stderr cho nguoi dieu phoi doc. D1 = chi to cao."""
    d = {"detector": "subagent-ghi", "ket_qua": ket_qua, "ly_do": ly_do}
    if chi_tiet:
        d["chi_tiet"] = chi_tiet
    print(json.dumps(d, ensure_ascii=True), file=sys.stderr)


def _so(truoc, sau):
    """Tra danh sach dong DELTA. Giu NGUYEN VAN ban ghi, khong rut ve so dem."""
    a = [x for x in truoc.splitlines() if x.strip()]
    b = [x for x in sau.splitlines() if x.strip()]
    ta, tb = set(a), set(b)
    return sorted(tb - ta), sorted(ta - tb)


def main() -> int:
    try:
        data = json.load(sys.stdin)
    except Exception:
        return 0                                  # khong doc duoc payload -> im lang
    su_kien = str(data.get("hook_event_name") or "")
    agent = str(data.get("agent_type") or "")
    if agent not in _AGENT:
        return 0                                  # ngoai tap da chot -> khong ap luat
    aid = str(data.get("agent_id") or "")
    cwd = str(data.get("cwd") or "")
    thu_muc = _thu_muc_anh()

    # `agent_id` la KHOA NOI BAT BUOC. Khong noi bang session_id, thoi gian, cwd hay thu
    # tu su kien — dac ta §2 cam tung duong mot.
    if not aid or "/" in aid or "\\" in aid or aid in (".", ".."):
        _bao("unknown", "agent_id thieu hoac khong dung lam ten tep duoc: %r" % aid)
        return _MA_UNKNOWN
    dich = thu_muc / ("%s.json" % aid)

    if su_kien == "SubagentStart":
        _don_rac(thu_muc)
        if dich.exists():
            # Trung khoa => KHONG duoc de lan sau doc nham anh cu.
            _bao("unknown", "da co anh chup cho agent_id nay (trung khoa)", {"agent_id": aid})
            return _MA_UNKNOWN
        anh, ly = _chup(cwd)
        if anh is None:
            _ghi_nguyen_tu(dich, {"hong": ly, "agent_type": agent, "cwd": cwd})
            _bao("unknown", "chup baseline that bai: %s" % ly)
            return _MA_UNKNOWN
        anh["agent_type"] = agent
        anh["cwd"] = cwd
        _ghi_nguyen_tu(dich, anh)
        return 0

    if su_kien != "SubagentStop":
        return 0

    if not dich.exists():
        _bao("unknown", "thieu anh chup cho agent_id nay", {"agent_id": aid})
        return _MA_UNKNOWN
    try:
        truoc = json.loads(dich.read_text(encoding="utf-8"))
    except Exception as e:
        _bao("unknown", "anh chup hong, khong doc duoc: %s" % e)
        return _MA_UNKNOWN
    if truoc.get("hong"):
        _bao("unknown", "baseline da hong tu luc Start: %s" % truoc["hong"])
        _don_rac(thu_muc); dich.unlink(missing_ok=True)
        return _MA_UNKNOWN
    if truoc.get("agent_type") != agent or truoc.get("cwd") != cwd:
        _bao("unknown", "sieu du lieu lech giua Start va Stop",
             {"agent_type": [truoc.get("agent_type"), agent], "cwd": [truoc.get("cwd"), cwd]})
        return _MA_UNKNOWN

    sau, ly = _chup(cwd)
    if sau is None:
        _bao("unknown", "chup luc Stop that bai: %s" % ly)
        return _MA_UNKNOWN
    if sau["top"] != truoc["top"]:
        _bao("unknown", "git top-level doi", {"top": [truoc["top"], sau["top"]]})
        return _MA_UNKNOWN
    if sau["head"] != truoc["head"]:
        _bao("unknown", "HEAD doi giua Start va Stop",
             {"head": [truoc["head"], sau["head"]]})
        return _MA_UNKNOWN

    them, mat = _so(truoc["status"], sau["status"])
    idx_doi = (truoc.get("index_sha256_16") != sau.get("index_sha256_16"))
    nd_t, nd_s = truoc.get("noi_dung") or {}, sau.get("noi_dung") or {}
    doi_noi_dung = sorted(k for k in set(nd_t) & set(nd_s) if nd_t[k] != nd_s[k])
    mu_nd = sorted(set(truoc.get("mu_noi_dung") or []) | set(sau.get("mu_noi_dung") or []))
    # KHONG xoa bang chung TRUOC khi ket qua da duoc tao chac chan (dac ta §4.2).
    if them or mat or idx_doi or doi_noi_dung:
        _bao("changed", "phat hien thay doi trong cay quan sat duoc", {
            "them": them, "mat": mat,
            "noi_dung_doi": doi_noi_dung,       # P1 `status-on-dinh-che-giau-lan-ghi`
            "index_byte_doi": idx_doi,          # A12
            "agent_type": agent, "cwd": cwd,
            "MU": ["ghi ngoai git top-level", "tac dung phu MANG",
                   "ghi roi hoan tac trong cung mot luot"],
        })
        dich.unlink(missing_ok=True)
        return _MA_CHANGED
    if mu_nd:
        # FAIL-CLOSE: co duong quan sat duoc ma KHONG noi-dung-hoa duoc thi khong duoc noi
        # `clean` — day dung la `None != False`. Goi TEN tung duong, dung dem.
        _bao("unknown", "co duong khong noi-dung-hoa duoc nen khong khang dinh duoc `clean`",
             {"khong_bam_duoc": mu_nd,
              "MU": ["ghi ngoai git top-level", "tac dung phu MANG",
                     "ghi roi hoan tac trong cung mot luot"]})
        dich.unlink(missing_ok=True)
        return _MA_UNKNOWN
    _bao("clean", "khong thay doi nao trong cay quan sat duoc", {
        "so_duong_da_bam_noi_dung": len(nd_s),
        "MU": ["ghi ngoai git top-level", "tac dung phu MANG",
               "ghi roi hoan tac trong cung mot luot"]})
    dich.unlink(missing_ok=True)
    return _MA_CLEAN


if __name__ == "__main__":
    sys.exit(main())
