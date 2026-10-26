#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng CHẠY ĐƯỢC cho từng chốt của `packet_loop.py`.

Hai nguyên tắc, cả hai đều đã phải trả giá mới có:

1. Suite gọi CHÍNH entrypoint qua `subprocess` với `--state-dir` riêng trong Temp,
   KHÔNG import và KHÔNG gọi hàm nội bộ. Cùng doctrine với
   `.githooks/eol_policy_test.py::case_real_hook_rename_only_bi_chan`: gọi hàm
   nội bộ chứng minh hàm chạy, không chứng minh LỆNH chạy — mà thứ người dùng gõ
   là lệnh.

2. Suite tự chứng minh KHÔNG RỖNG. "26/26 đạt" chẳng nói lên gì nếu không có ca
   nào đỏ được. Mỗi chốt số có một ĐỘT BIẾN nới ngưỡng, và ca tương ứng BẮT BUỘC
   phải chết theo. Ca không chết được là ca không đo gì.

Chạy: `python .claude/dev/packet_loop_test.py`
"""

from __future__ import annotations

import hashlib
import importlib.util
import json
import os
import platform
import re
import subprocess
import sys
import tempfile
import time
import unicodedata
from pathlib import Path

from launcher import ky_ban_ghi_luot

HERE = Path(__file__).resolve().parent
CANONICAL = HERE / "packet_loop.py"
ROOT = HERE.parents[1]

# --- CÔ LẬP GIT KHỎI CẤU HÌNH NGOÀI (cross-review codex, PR #343, cùng lớp với P1-a của
# PR #342) --------------------------------------------------------------------------
#
# TRIỆU CHỨNG: fixture nào `git commit` mà không ghim `commit.gpgsign=false` sẽ ăn cấu hình
# TOÀN CỤC của máy chạy. Container này ĐANG có đúng nền ấy — đo được:
#     git config --global --list | grep -E 'gpgsign|signingkey'
#       commit.gpgsign=true · user.signingkey=… · gpg.format=ssh
# Tái hiện được cú chết bằng một global config dựng sẵn có `signingkey` trỏ tệp KHÔNG tồn
# tại: `error: cannot run ssh-keygen` → `fatal: failed to write commit object`, rc=128.
# Reviewer đo `271/273` trên một nền bật ký; ở đây nền bật ký vẫn `rc=0` vì máy có sẵn
# `gpg.ssh.program`. Hai nền, hai kết quả — tức con số phụ thuộc MÁY, đúng thứ hermeticity
# sinh ra để giết.
#
# VÌ SAO KHÔNG GHIM TỪNG KHOÁ: bản của PR #342 liệt `commit.gpgsign` `tag.gpgsign`
# `core.autocrlf` `core.eol` `gc.auto` — đó là DANH SÁCH CẤM, và kho này đã trả giá cho
# hình dạng ấy (`lease-authority-spoof`: "danh sách cấm không bao giờ đủ"). `core.hooksPath`,
# `include.path`, `core.fsmonitor`, `merge.*`, `diff.*`… đều có thể phá fixture, và không ai
# liệt hết được. ĐẢO thành: KHÔNG đọc nguồn cấu hình ngoài NÀO — `GIT_CONFIG_GLOBAL` và
# `GIT_CONFIG_SYSTEM` trỏ `os.devnull` (git ≥ 2.32; đo tại chỗ: 2.43.0). Cấu hình
# REPO-LOCAL (`.git/config`, ví dụ `core.abbrev=7` mà CLAUDE.md đòi) KHÔNG bị đụng.
#
# Danh tính commit phải cấp bằng biến vì global đã tắt — fixture nào quên `git config
# user.email` sẽ không còn mượn được của máy chạy.
#
# ĐẶT NGAY KHI NẠP MODULE, TRƯỚC mọi lần spawn: `run()` và các fixture đều `os.environ.copy()`
# hoặc kế thừa thẳng, nên một chỗ này phủ CẢ tiến trình con lẫn `git` gọi trực tiếp.
_GIT_BIEN_CO_LAP = {
    "GIT_CONFIG_GLOBAL": os.devnull,
    "GIT_CONFIG_SYSTEM": os.devnull,
    "GIT_AUTHOR_NAME": "tl-test",
    "GIT_AUTHOR_EMAIL": "tl-test@invalid",
    "GIT_COMMITTER_NAME": "tl-test",
    "GIT_COMMITTER_EMAIL": "tl-test@invalid",
}


# NGUỒN THỨ BA, và bản lượt 3 của chính tệp này KHÔNG BIẾT tới nó — cross-review codex
# lượt 2 trên PR #342 bắt trên packet anh em, tái hiện tại đây:
#   env COUNT=1 KEY_0=commit.gpgsign VALUE_0=true + GIT_CONFIG_GLOBAL=/dev/null
#     -> commit rc=128 "gpg failed to sign the data" · `config --get commit.gpgsign` = true
#   gỡ đúng ba biến ấy ra -> rc=0
# Tức cấu hình PHẠM VI LỆNH (`GIT_CONFIG_COUNT` + `GIT_CONFIG_KEY_<n>`/`VALUE_<n>`) có độ
# ưu tiên CAO HƠN cả repo-local, và `GIT_CONFIG_GLOBAL` không đụng tới nó. Câu "đã cắt
# nguồn ngoài" của lượt 3 vì thế SAI — nó cắt HAI TRONG BA.
#
# KHÔNG hiển nhiên và KHÔNG hiếm: container này ĐANG đặt `GIT_CONFIG_COUNT=3` (url rewrite
# + `credential.interactive=false`), nên kênh ấy sống trong MỌI lệnh git bộ test gọi. Hiện
# vô hại, nhưng "vô hại hôm nay" không phải "không tồn tại".
#
# VÌ SAO ĐÂY KHÔNG PHẢI DANH SÁCH CẤM: git đọc cấu hình từ một tập ĐÓNG gồm ba NGUỒN
# (system · global · phạm vi lệnh) — ta chặn cả ba. Tập KHOÁ thù địch mới là thứ vô hạn,
# và đó là chỗ danh sách cấm thua.
def _la_cau_hinh_pham_vi_lenh(k: str) -> bool:
    if k == "GIT_CONFIG_COUNT":
        return True
    for tien_to in ("GIT_CONFIG_KEY_", "GIT_CONFIG_VALUE_"):
        # Xoá MỌI cặp đánh số, không chỉ những cặp dưới `COUNT` hiện tại: bỏ sót một cặp
        # rồi để `COUNT` mới trỏ tới nó còn tệ hơn không xoá gì.
        if k.startswith(tien_to) and k[len(tien_to):].isdigit():
            return True
    return False


def _ep_git_co_lap(env):
    """Ép một môi trường về trạng thái KHÔNG đọc cấu hình git ngoài. Nhận `env` làm ĐỐI SỐ
    để ca `fixture_git_KHONG_an_config_toan_cuc` gọi được với một nền THÙ ĐỊCH dựng sẵn —
    một hàm chỉ sửa `os.environ` thì không có cách nào cho nó ca biết trước đáp án."""
    for k in [k for k in env if _la_cau_hinh_pham_vi_lenh(k)]:
        del env[k]
    env.update(_GIT_BIEN_CO_LAP)
    return env


_ep_git_co_lap(os.environ)

EXECUTOR = "claude"
REVIEWER = "codex"
BIEN_BC = "TL_MOI_TRUONG_JSON"
VOID_DUYET = ["--khong-co-bang-chung", "--ai-cho-phep", "ducthangho",
              "--can-cu", "ca test có người duyệt"]
_ANH_SACH = []


# --- hạ tầng ------------------------------------------------------------------

class BoQua(Exception):
    pass


def anh_doctor(**doi) -> str:
    d = {"thieu_bat_buoc": [], "chua_xac_thuc": [],
         "he_dieu_hanh": platform.system()}
    d.update(doi)
    if not doi and _ANH_SACH:
        return _ANH_SACH[0]
    f = Path(tempfile.mkdtemp(prefix="tl-doctor-")) / "doctor.json"
    f.write_text(json.dumps(d), encoding="utf-8")
    if not doi:
        _ANH_SACH.append(str(f))
    return str(f)


def anh_doctor_ky(sd, **doi) -> str:
    f = Path(anh_doctor(**doi)); d = json.loads(f.read_text(encoding="utf-8"))
    st = json.loads((sd / "wp55.json").read_text(encoding="utf-8")); neo = st["attempt_anchor"]
    d.update(nonce=neo["nonce"], attempt=neo["attempt"])
    d["chu_ky"] = ky_ban_ghi_luot(d, st["hmac_key"])
    f.write_text(json.dumps(d), encoding="utf-8")
    return str(f)


def run(script: Path, args, state_dir=None, env_extra=None):
    cmd = [sys.executable, str(script)]
    if state_dir is not None:
        cmd += ["--state-dir", str(state_dir)]
    cmd += [str(x) for x in args]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONIOENCODING", None)
    env[BIEN_BC] = anh_doctor()
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(cmd, capture_output=True, env=env)
    if args and str(args[0]) == "kiem-gate":
        _kg_kiem_ket_qua(p.returncode, p.stdout, p.stderr, cmd)
    return p.returncode, p.stdout, p.stderr


def run_json_that(c, sd, reason="infrastructure", xong=False, loi_probe=False,
                  truoc_spawn=True) -> Path:
    launcher = c.script.with_name("launcher.py")
    if not launcher.is_file():
        launcher.write_text((HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
    rr = c.tmp / f"runs{c._n}-{reason}-{int(xong)}-{time.time_ns()}"
    cmd = [sys.executable, str(launcher), "run", "--workspace", str(ROOT),
           "--run-root", str(rr), "--attempt-state", str(sd / "wp55.json"),
           "--void-reason", reason, "--"]
    if loi_probe:
        cmd += [str(c.tmp / f"khong-ton-tai-{time.time_ns()}")]
    else:
        cmd += [sys.executable, "-c", "pass" if xong else "import sys; sys.exit(23)"]
    if truoc_spawn and not loi_probe and not xong:
        # Fail only the actual child launch; the existing --version probe runs.
        # The real launcher writes/signs the pre-spawn record. Never forge a
        # post-spawn verdict merely to reach the consumer's nonce checks.
        driver = c.tmp / f"fail-popen-{time.time_ns()}.py"
        driver.write_text(
            "import runpy,sys,subprocess\n"
            "real = subprocess.Popen\n"
            "def fail(argv, *a, **kw):\n"
            "    if list(argv)[-2:] == ['-c', 'import sys; sys.exit(23)']:\n"
            "        raise PermissionError(13, 'INERT pre-spawn denial')\n"
            "    return real(argv, *a, **kw)\n"
            "subprocess.Popen = fail\n"
            "sys.argv = sys.argv[1:]\n"
            "runpy.run_path(sys.argv[0], run_name='__main__')\n", encoding="utf-8")
        cmd.insert(1, str(driver))
    p = subprocess.run(cmd, capture_output=True,
                       env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    f = next(rr.iterdir()) / "run.json"
    if loi_probe or xong:
        return f

    d = json.loads(f.read_text(encoding="utf-8"))
    if truoc_spawn:
        assert p.returncode != 0 and d.get("trang_thai") == "hong"
        assert d.get("void_reason") == reason and not d.get("pid")
        assert d.get("probe", {}).get("spawn", {}).get("trang_thai") == "DAT"
        return f
    if p.returncode != 23 or d.get("ma_thoat") != 23:
        raise AssertionError(f"child sau-spawn không thất bại đúng cách: rc={p.returncode}, sổ={d}")
    if d.get("probe", {}).get("spawn", {}).get("trang_thai") != "DAT":
        raise AssertionError(f"child chưa qua probe spawn: {d.get('probe')}")
    # An unknown post-spawn failure has no machine-void certificate.
    assert "void_reason" not in d and d.get("failure_class") == "unknown"
    return f


def _txt(b: bytes) -> str:
    return b.decode("utf-8", "replace").strip()


def _doi(expect: int, rc: int, err: bytes, msg: str) -> None:
    if rc != expect:
        raise AssertionError(f"{msg}: đòi rc={expect}, được rc={rc}; stderr={_txt(err)!r}")


# Head hợp lệ dùng cho các ca ĐO SỔ COMMENT. Nó KHÔNG phải chi tiết trang trí:
# `transition --to reviewing` chặn thiếu `--head-sha` TRƯỚC khi gọi
# `_tieu_thu_comment_id` (xem `packet_loop.py`), nên một ca quên head sẽ nhận
# đúng `RC_TRACE` vì lý do KHÁC và xanh mà không đo gì.
HEAD_HOP_LE = "0" * 39 + "1"


def _doi_ly_do(expect: int, rc: int, err: bytes, phai_chua: str, msg: str) -> None:
    """Đòi CẢ mã thoát LẪN lý do — neo mã trần là chốt rỗng.

    VÌ SAO CÓ (cross-review lượt 4 `R4-05`, đo được): ba ca sổ comment gọi
    `transition --to reviewing --comment-id …` mà KHÔNG cấp `--head-sha`. Lệnh
    trả `RC_TRACE` ngay ở chốt head, TRƯỚC khi sổ comment được đụng tới; ba ca
    chỉ so mã nên cả ba xanh. Đột biến thay `_tieu_thu_comment_id(...)` bằng
    `{}` — tức GỠ HẲN cổng sổ comment — mà cả ba VẪN xanh. Chúng mang tên sổ
    comment nhưng đang đo chốt head-sha.
    """
    if rc != expect:
        raise AssertionError(f"{msg}: đòi rc={expect}, được rc={rc}; stderr={_txt(err)!r}")
    # #856 (run 39729983506, Windows): stderr của CLI con ra `\r\n`, lý do nhiều dòng viết `\n` ⇒ 3 ca `kg_*` đỏ oan.
    t = _txt(err).replace("\r\n", "\n")
    if phai_chua not in t:
        raise AssertionError(
            f"{msg}: rc đúng nhưng LÝ DO sai — đòi chứa {phai_chua!r}, stderr={t!r}. "
            f"Mã thoát trùng nhau không chứng minh chốt nào đã chạy.")


class Ctx:
    def __init__(self, script: Path, tmp: Path):
        self.script = script
        self.tmp = tmp
        self._n = 0

    def sd(self) -> Path:
        self._n += 1
        d = self.tmp / f"sd{self._n}"
        d.mkdir(parents=True, exist_ok=True)
        return d

    def init(self, sd: Path, packet=55, executor=EXECUTOR, reviewer=REVIEWER, extra=(),
             lease=True):
        """init, rồi GHI LUÔN một lease hợp lệ (mặc định).

        `init` chỉ đưa packet tới `awaiting_lease`, nên phần lớn ca ở dưới — vốn đo
        hành vi HẠ NGUỒN của lease — cần một lease thật để đi tiếp. Ca nào đo chính
        cái chốt lease thì truyền `lease=False` để nhìn thấy trạng thái chưa có lease.
        """
        rc, o, e = run(
            self.script,
            ["init", "--packet", packet, "--mission", 54, "--executor", executor, "--reviewer",
             reviewer, "--review-rounds-limit", 50, "--codex-review-calls-limit", 50, *extra],
            sd,
        )
        if rc != 0 or not lease:
            return rc, o, e
        return self.cap_lease(sd, packet)

    def cap_lease(self, sd: Path, packet=55, granted_by="ducthangho", expires=None,
                  evidence=None, extra=(), lease_id=None):
        """Ghi một lease HỢP LỆ (mặc định) — hoặc lệch đúng một chiều để làm ca đỏ.

        `granted_by` mặc định là `"ducthangho"` — tên DUY NHẤT trong
        `NGUOI_CO_THAM_QUYEN` (finding `lease-authority-spoof`: chốt là danh sách
        CHO PHÉP, không còn là danh sách cấm PROVIDERS).
        """
        from datetime import datetime, timedelta, timezone

        if expires is None:
            expires = (datetime.now(timezone.utc) + timedelta(hours=4)).strftime(
                "%Y-%m-%dT%H:%M:%SZ")
        if evidence is None:
            evidence = f"https://github.com/o/r/issues/{packet}#issuecomment-5281636040"
        if lease_id is None:
            lease_id = f"wp{packet}-r2-review-2-codex-test"
        return run(
            self.script,
            ["record-lease", "--packet", packet,
             "--lease-id", lease_id,
             "--granted-by", granted_by, "--evidence", evidence,
             "--expires-utc", expires, *extra],
            sd,
        )

    def head(self, luot: int) -> str:
        """Head giả nhưng ĐÚNG DẠNG git oid, khác nhau theo lượt."""
        return f"{luot:040x}"

    def den_reviewing(self, sd: Path, packet: int, luot: int, head=None):
        """begin-attempt → record-post → transition reviewing (neo head của lượt)."""
        rc, _, e = run(self.script, ["begin-attempt", "--packet", packet, "--provider", EXECUTOR], sd)
        _doi(0, rc, e, f"begin-attempt lượt {luot}")
        cid = str(9_000_000_000 + packet * 1000 + luot * 2)
        rc, _, e = run(self.script,
                       ["record-post", "--packet", packet, "--for", "reviewing", "--comment-id", cid], sd)
        _doi(0, rc, e, f"record-post lượt {luot}")
        rc, _, e = run(self.script,
                       ["transition", "--packet", packet, "--to", "reviewing",
                        "--comment-id", cid, "--head-sha", head or self.head(luot)], sd)
        _doi(0, rc, e, f"transition reviewing lượt {luot}")
        return cid

    def review(self, sd, packet, ids, verdict="changes_requested", descs=(), luot=1, sha=None, goi=None):
        if goi is None:  # #775 M3: review codex neo một lời gọi đã ghi trên head của lượt
            run(self.script, ["record-codex-call", "--packet", packet, "--head", self.head(luot), "--run-id", goi := f"g{luot}"], sd)
        args = ["record-review", "--packet", packet, "--provider", REVIEWER, "--verdict", verdict,
                "--reviewed-sha", self.head(luot) if sha is None else sha, "--codex-call", goi]
        for i in ids:
            args += ["--finding-id", i]
        for d in descs:
            args += ["--finding-desc", d]
        return run(self.script, args, sd)

    def state(self, sd, packet) -> str:
        rc, o, e = run(self.script, ["status", "--packet", packet], sd)
        _doi(0, rc, e, "status")
        import json
        return json.loads(o.decode("utf-8"))["state"]

    def counts(self, sd, packet) -> dict:
        rc, o, e = run(self.script, ["status", "--packet", packet], sd)
        _doi(0, rc, e, "status")
        import json
        return json.loads(o.decode("utf-8"))["finding_counts"]


# --- (a) cross-provider --------------------------------------------------------


def case_init_cross_provider_ok(c: Ctx):
    sd = c.sd()
    rc, _, e = c.init(sd)
    _doi(0, rc, e, "init khác provider phải chạy")


def case_init_cung_provider_thoat_4(c: Ctx):
    sd = c.sd()
    rc, _, e = c.init(sd, executor="claude", reviewer="claude")
    _doi(4, rc, e, "executor trùng reviewer phải bị chặn TỪ init")


def case_review_sai_provider_thoat_4(c: Ctx):
    """Review đúng packet nhưng sai nền ⇒ thoát 4."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = run(
        c.script,
        ["record-review", "--packet", 55, "--provider", EXECUTOR,
         "--verdict", "changes_requested", "--finding-id", "sai-nen-review",
         "--reviewed-sha", c.head(1)],
        sd,
    )
    _doi(4, rc, e, "executor tự review chính mình phải bị chặn")


# --- trần attempt --------------------------------------------------------------


def case_cap_lan_4_thoat_3(c: Ctx):
    """Trần 3 lượt: lượt thứ 4 thoát mã 3 và state về blocked."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    for n in (1, 2, 3):
        c.den_reviewing(sd, 55, n)
        # ID khác nhau mỗi lượt để KHÔNG kích same-failure — ca này chỉ đo trần lượt.
        rc, _, e = c.review(sd, 55, [f"loi-khac-nhau-{n}"], luot=n)
        _doi(0, rc, e, f"review lượt {n}")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(3, rc, e, "lượt thứ 4 phải thoát 3")
    if c.state(sd, 55) != "blocked":
        raise AssertionError(f"state phải là blocked, đang là {c.state(sd, 55)!r}")


def case_begin_attempt_lap_khong_tieu_them_tran(c: Ctx):
    """Lượt ĐANG MỞ thì gọi lại begin-attempt không mở lượt mới, không tiêu trần.

    Thiếu chốt này, gõ begin-attempt bốn lần liên tiếp đủ đưa một packet mặc định
    về blocked dù chưa lượt nào chạy xong.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt lần 1")
    for lan in (2, 3, 4):
        rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
        if rc == 0:
            raise AssertionError(f"begin-attempt lần {lan} khi lượt đang mở phải bị từ chối")
    if c.state(sd, 55) == "blocked":
        raise AssertionError("gọi lặp begin-attempt KHÔNG được làm cạn trần")
    rc, o, e = run(c.script, ["status", "--packet", 55], sd)
    _doi(0, rc, e, "status")
    import json
    if json.loads(o.decode("utf-8"))["attempts_used"] != 1:
        raise AssertionError("attempts_used phải giữ 1 sau các lần gọi lặp")


def case_init_khong_ghi_de_state_da_blocked(c: Ctx):
    """Không có đường nào hồi sinh một packet đã cạn trần bằng cách init lại."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["loi-lap-lai"])
    _doi(0, rc, e, "review lượt 1")
    c.den_reviewing(sd, 55, 2)
    rc, _, e = c.review(sd, 55, ["loi-lap-lai"], luot=2)
    _doi(3, rc, e, "same-failure phải chặn")
    # init lại: phải bị từ chối, và state cũ KHÔNG được đổi
    rc, _, e = c.init(sd)
    if rc == 0:
        raise AssertionError("init đè lên state đã tồn tại phải bị từ chối")
    if c.state(sd, 55) != "blocked":
        raise AssertionError("state blocked không được bị init xoá")


def case_init_khong_co_co_ghi_de(c: Ctx):
    rc, o, e = run(c.script, ["init", "--help"])
    _doi(0, rc, e, "init --help")
    txt = _txt(o).lower()
    for co in ("--force-new", "--force", "--overwrite", "--reset", "--clobber"):
        if co in txt:
            raise AssertionError(f"init KHÔNG được có cờ ghi đè, nhưng thấy {co!r}")


# --- bằng chứng review neo EXACT SHA ------------------------------------------


def case_review_phai_neo_head_da_dua_ra_review(c: Ctx):
    """--reviewed-sha khác head đã đưa ra review ⇒ từ chối, KHÔNG cho accepted."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, [], verdict="approve", sha="b" * 40)
    _doi(5, rc, e, "approve trên SHA khác head đưa ra review phải bị từ chối")
    if c.state(sd, 55) == "accepted":
        raise AssertionError("KHÔNG được accepted khi bản duyệt không neo đúng head")


def case_review_thieu_hoac_sai_dang_sha(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = run(c.script,
                   ["record-review", "--packet", 55, "--provider", REVIEWER,
                    "--verdict", "approve"], sd)
    _doi(5, rc, e, "thiếu --reviewed-sha phải bị từ chối")
    for xau in ("1bca750", "Z" * 40, "A" * 40, ""):
        rc, _, e = c.review(sd, 55, [], verdict="approve", sha=xau)
        if rc == 0:
            raise AssertionError(f"--reviewed-sha sai dạng {xau!r} phải bị từ chối")


def case_transition_reviewing_phai_khai_head(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000011"], sd)
    _doi(0, rc, e, "record-post")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000011"], sd)
    _doi(5, rc, e, "vào reviewing mà không khai --head-sha phải bị từ chối")


def case_approve_neo_dung_head_thi_chay(c: Ctx):
    """Chiều dương: đúng head thì approve chạy và ghi lại accepted_sha."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, [], verdict="approve")
    _doi(0, rc, e, "approve đúng head")
    rc, o, e = run(c.script, ["status", "--packet", 55], sd)
    _doi(0, rc, e, "status")
    import json
    st = json.loads(o.decode("utf-8"))
    if st["state"] != "accepted" or st["accepted_sha"] != c.head(1):
        raise AssertionError(f"accepted phải neo đúng SHA, đang là {st['accepted_sha']!r}")


def case_head_moi_lam_ban_duyet_cu_het_hieu_luc(c: Ctx):
    """Mở lượt mới (có commit mới) ⇒ head cũ không còn dùng để duyệt được."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["can-sua-them"])
    _doi(0, rc, e, "changes_requested lượt 1")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt lượt 2")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000012"], sd)
    _doi(0, rc, e, "record-post")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", "7770000012", "--head-sha", c.head(2)], sd)
    _doi(0, rc, e, "transition reviewing lượt 2")
    rc, _, e = c.review(sd, 55, [], verdict="approve", sha=c.head(1))
    _doi(5, rc, e, "duyệt bằng head CŨ sau khi có commit mới phải bị từ chối")


# --- (a..d) same-failure theo ID ----------------------------------------------


def case_same_failure_cung_id_qua_2_review(c: Ctx):
    """(a) cùng ID qua hai review ⇒ DỪNG ở lần thứ hai."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["url-alias"])
    _doi(0, rc, e, "lần 1 cùng ID chưa được chặn")
    c.den_reviewing(sd, 55, 2)
    rc, _, e = c.review(sd, 55, ["url-alias"], luot=2)
    _doi(3, rc, e, "lần 2 cùng ID phải chặn")
    if c.state(sd, 55) != "blocked":
        raise AssertionError("same-failure phải đưa state về blocked")


def case_same_failure_hai_id_khac_khong_kich(c: Ctx):
    """(b) hai ID khác nhau KHÔNG kích trần."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["url-alias"])
    _doi(0, rc, e, "ID thứ nhất")
    c.den_reviewing(sd, 55, 2)
    rc, _, e = c.review(sd, 55, ["van-tay-lach"], luot=2)
    _doi(0, rc, e, "ID khác không được kích trần")
    if c.state(sd, 55) == "blocked":
        raise AssertionError("hai ID khác nhau không được làm blocked")


def case_same_failure_lap_trong_mot_review_tinh_mot(c: Ctx):
    """(c) cùng ID lặp TRONG MỘT review ⇒ tính MỘT lần, không chặn oan lượt đầu."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["lap-trong-mot-luot", "lap-trong-mot-luot", "lap-trong-mot-luot"])
    _doi(0, rc, e, "lặp trong CÙNG một review không được chặn oan")
    dem = c.counts(sd, 55)
    if dem.get("lap-trong-mot-luot") != 1:
        raise AssertionError(f"phải đếm đúng 1, đang là {dem!r}")


def case_same_failure_hai_mo_ta_cung_id_la_mot(c: Ctx):
    """(d) hai mô tả khác nhau cùng một ID ⇒ vẫn là MỘT finding."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(
        sd, 55,
        ["mot-id-hai-mo-ta", "mot-id-hai-mo-ta"],
        descs=["mô tả thứ nhất", "mô tả thứ hai hoàn toàn khác"],
    )
    _doi(0, rc, e, "hai mô tả cùng ID")
    dem = c.counts(sd, 55)
    if dem.get("mot-id-hai-mo-ta") != 1:
        raise AssertionError(f"mô tả không được tham gia phép đếm, đang là {dem!r}")


def case_thieu_finding_id_thoat_khac_0(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, [])
    _doi(2, rc, e, "changes_requested thiếu --finding-id phải thoát khác 0")


def case_slug_sai_dang_thoat_khac_0(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    for xau in ("URL_Alias", "url alias", "-dau-gach", "hai--gach", "Hoa", "dấu-tiếng-việt", ""):
        rc, _, e = c.review(sd, 55, [xau])
        if rc == 0:
            raise AssertionError(f"slug sai dạng {xau!r} phải bị từ chối, nhưng rc=0")


# --- guard ---------------------------------------------------------------------


def case_guard_moi_hanh_vi_thoat_7(c: Ctx):
    sd = c.sd()
    for act in ("merge", "deploy", "live", "secrets", "force-push",
                "delete-branch", "delete-worktree", "edit-other-spec"):
        rc, _, e = run(c.script, ["guard", "--action", act], sd)
        _doi(7, rc, e, f"guard {act}")


def case_guard_khong_co_co_noi(c: Ctx):
    rc, o, e = run(c.script, ["guard", "--help"])
    _doi(0, rc, e, "guard --help")
    txt = _txt(o).lower()
    for co in ("--force", "--allow", "--override", "--yes", "--bypass", "--no-guard", "--i-know"):
        if co in txt:
            raise AssertionError(f"guard KHÔNG được có cờ nới, nhưng thấy {co!r}")


# --- #338: mốc đột biến phải khớp ĐÚNG MỘT CHỖ -------------------------------------
#
# VÌ SAO CÓ: bảng `MUTANTS` áp bằng `str.replace(moc, thay, 1)` — phép CHUỖI CON, không
# neo dòng. Nên một dòng thụt SÂU HƠN chứa trọn mốc thụt NÔNG hơn:
#     "            except ValueError:\n"   CHỨA   "        except ValueError:\n"
# Nếu dòng sâu ấy nằm TRƯỚC mục tiêu trong tệp, `replace(..., 1)` sửa NHẦM nó và đột biến
# thành vô hiệu — ca đích vẫn XANH, và runner báo "ca đó không đo gì", tức đổ lỗi cho CA
# trong khi lỗi nằm ở MỐC.
#
# ĐÃ XẢY RA THẬT trong chính packet này: thêm một `except ValueError:` 12 dấu cách vào
# `cmd_doi_chieu_uy_quyen` làm `bien_nhan_bo_nhanh_valueerror` mất răng. Đo được: mốc khớp
# 1 chỗ trên `origin/master`, 2 chỗ sau khi thêm dòng ấy. Nền master `TỔNG: ĐẠT`, nhánh
# `TỔNG: 1 lỗi` — delta THẬT, dù `git diff | grep bien_nhan` = 0. Suy "diff không chạm tên
# ấy nên không phải của mình" là SAI: tương tác đi qua CHUỖI CON, không qua tên.
#
# Chốt này nói đúng chỗ đau ngay lần đầu, thay vì để người sau truy như tôi vừa truy.
#
# LƯỢT 3 — cross-review codex bắt đúng hai lỗ của bản lượt 2, và cả hai đều thuộc lớp
# "phép kiểm tự bảo vệ mình bằng chính thứ cần được bảo vệ":
#
#  (1) BẢNG NGOẠI LỆ LÀ CỬA. Bản trước khai `MOC_MO_HO_CO_SAN = {"adr_…": 2}` để tha một
#      mốc khớp 2 chỗ. Nhưng bảng ngoại lệ chính là thứ mà mọi mốc mơ hồ SAU này sẽ được
#      thêm vào — đúng hình dạng "danh sách CẤM/THA không bao giờ đủ" mà kho đã trả giá.
#      Đường ra: làm MỐC ĐỦ HẸP (kéo thêm một dòng ngữ cảnh vào mốc `adr_tha_khi_thieu_thu_muc`,
#      đo còn 1 chỗ) rồi BỎ HẲN bảng, đòi `== 1` vô điều kiện. Cửa chết theo KIẾN TRÚC.
#
#  (2) PHÉP KIỂM XANH-THEO-CẤU-TẠO KHÔNG THỂ TỰ CHỨNG MINH CÓ RĂNG. Đo được: nới vị từ
#      thành `if n == n:` thì KHÔNG ca nào chết — vì trên dữ liệu THẬT mọi mốc đều khớp,
#      nên nhánh "báo xấu" chưa từng chạy. Một vị từ không bao giờ sai thì đột biến làm nó
#      luôn đúng chẳng đổi gì. Đường ra là tách VỊ TỪ khỏi DỮ LIỆU: `_moc_khop_sai(...)`
#      nhận bảng làm ĐỐI SỐ, rồi cho nó một ca BIẾT TRƯỚC ĐÁP ÁN (một mốc dựng sẵn khớp 2
#      chỗ PHẢI bị tố; một mốc khớp 1 chỗ PHẢI được tha). Nay đột biến `if True:` giết
#      `moc_kiem_TU_NO_co_rang` — tức phép kiểm có răng ĐO ĐƯỢC, không phải suy ra.
def _moc_khop_sai(bang, nham_test, goc, goc_test) -> list[str]:
    """Trả danh sách mốc KHÔNG khớp đúng một chỗ. Bảng là ĐỐI SỐ nên gọi được với dữ liệu
    dựng sẵn — đó là cách duy nhất cho vị từ này một ca biết trước đáp án."""
    xau = []
    for ten, bo in bang.items():
        than = goc_test if ten in nham_test else goc
        for t, _ in _cap_thay_the(bo[0], bo[1]):
            n = than.count(t)
            if n == 1:
                continue
            xau.append(f"{ten}: mốc khớp {n} chỗ (đòi 1) — {t[:50]!r}")
    return xau


def case_moc_dot_bien_phai_khop_DUNG_MOT_CHO(c: Ctx):
    xau = _moc_khop_sai(MUTANTS, MUTANTS_NHAM_TEST,
                        c.script.read_text(encoding="utf-8"),
                        Path(__file__).read_text(encoding="utf-8"))
    if xau:
        raise AssertionError(
            "mốc đột biến KHÔNG khớp đúng một chỗ ⇒ `replace(...,1)` có thể sửa NHẦM chỗ và "
            "đột biến mất răng trong im lặng: " + "; ".join(xau))


def case_moc_kiem_TU_NO_co_rang(c: Ctx):
    """Ca BIẾT TRƯỚC ĐÁP ÁN cho `_moc_khop_sai` — hai chiều, vì một vị từ luôn-tố cũng vô
    dụng y như một vị từ luôn-tha."""
    goc = "alpha\nbeta\nalpha\n"
    hai_cho = {"mut_khop_2": ("alpha\n", "GAMMA\n", ["ca_nao_do"])}
    mot_cho = {"mut_khop_1": ("beta\n", "GAMMA\n", ["ca_nao_do"])}
    khong_cho = {"mut_khop_0": ("delta\n", "GAMMA\n", ["ca_nao_do"])}

    ra = _moc_khop_sai(hai_cho, frozenset(), goc, "")
    if len(ra) != 1 or "khớp 2 chỗ" not in ra[0]:
        raise AssertionError(f"mốc khớp 2 chỗ PHẢI bị tố, nhận: {ra!r}")

    ra = _moc_khop_sai(khong_cho, frozenset(), goc, "")
    if len(ra) != 1 or "khớp 0 chỗ" not in ra[0]:
        raise AssertionError(f"mốc khớp 0 chỗ (mỏ neo chết) PHẢI bị tố, nhận: {ra!r}")

    ra = _moc_khop_sai(mot_cho, frozenset(), goc, "")
    if ra:
        raise AssertionError(f"mốc khớp ĐÚNG 1 chỗ phải được tha, nhưng bị tố: {ra!r}")

    # Chiều thứ ba: bảng `nham_test` phải đổi NGUỒN đọc, chứ không chỉ là trang trí.
    ra = _moc_khop_sai(mot_cho, frozenset({"mut_khop_1"}), goc, "")
    if len(ra) != 1 or "khớp 0 chỗ" not in ra[0]:
        raise AssertionError(f"MUTANTS_NHAM_TEST phải chuyển sang thân test, nhận: {ra!r}")


_CAU_HINH_THU_DICH = (
    "[user]\n\tname = Ke Thu\n\temail = kethu@example.invalid\n"
    "\tsigningkey = /khong/co/khoa/nao.pub\n"
    "[gpg]\n\tformat = ssh\n[commit]\n\tgpgsign = true\n[core]\n\tautocrlf = true\n"
)


def _thu_commit(goc: Path, env) -> tuple[int, str]:
    """Dựng một kho tí hon rồi commit — trả `(rc, stderr)` của riêng bước commit."""
    goc.mkdir(parents=True, exist_ok=True)
    for a in (["init", "--quiet", "-b", "main"], ["add", "a.txt"]):
        if a[0] == "add":
            (goc / "a.txt").write_text("1\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(goc), *a], capture_output=True, env=env)
    p = subprocess.run(["git", "-C", str(goc), "commit", "-qm", "goc"],
                       capture_output=True, env=env)
    return p.returncode, _txt(p.stderr)


def case_fixture_git_KHONG_an_config_toan_cuc(c: Ctx):
    """Ca BIẾT TRƯỚC ĐÁP ÁN cho `_ep_git_co_lap`, hai chiều.

    Không có chiều ĐỐI CHỨNG thì ca này xanh cả khi hàm cô lập là một `pass` — vì nền
    của máy đang chạy có thể vốn đã lành. Chiều đối chứng chứng minh nền thù địch THẬT SỰ
    giết được commit; chỉ khi ấy chiều còn lại mới nói lên điều gì."""
    thu = c.tmp / f"gitcfg-thu-{time.time_ns()}"
    thu.write_text(_CAU_HINH_THU_DICH, encoding="utf-8")

    # (1) ĐỐI CHỨNG: gỡ đúng các biến cô lập ra ⇒ nền thù địch phải giết được commit.
    ban = os.environ.copy()
    for k in _GIT_BIEN_CO_LAP:
        ban.pop(k, None)
    ban["GIT_CONFIG_GLOBAL"] = str(thu)
    ban["GIT_CONFIG_SYSTEM"] = os.devnull
    rc, e = _thu_commit(c.tmp / f"kho-thu-doi-chung-{time.time_ns()}", ban)
    if rc == 0:
        raise BoQua("KHÔNG ĐO ĐƯỢC: nền thù địch dựng sẵn vẫn commit được (máy này có "
                    "ssh-keygen + khoá?) ⇒ chiều đối chứng vô nghĩa, không kết luận gì")

    # (2) CHIỀU THẬT: cùng nền thù địch, nhưng đi qua hàm cô lập ⇒ commit phải SỐNG.
    sach = _ep_git_co_lap(dict(ban))
    rc, e = _thu_commit(c.tmp / f"kho-thu-co-lap-{time.time_ns()}", sach)
    if rc != 0:
        raise AssertionError(f"_ep_git_co_lap KHÔNG chặn được cấu hình toàn cục: rc={rc} {e[:200]!r}")

    # (3) Cô lập phải là KHÔNG ĐỌC NGUỒN NGOÀI, không phải "ghim vài khoá đã nghĩ tới":
    # một khoá ngoài danh sách của PR #342 (`core.hooksPath`) cũng phải biến mất.
    thu2 = c.tmp / f"gitcfg-thu2-{time.time_ns()}"
    thu2.write_text("[core]\n\thooksPath = /khong/co/hooks\n", encoding="utf-8")
    moi = _ep_git_co_lap(dict(os.environ, GIT_CONFIG_GLOBAL=str(thu2)))
    goc = c.tmp / f"kho-thu-hooks-{time.time_ns()}"
    goc.mkdir(parents=True, exist_ok=True)
    subprocess.run(["git", "-C", str(goc), "init", "--quiet", "-b", "main"],
                   capture_output=True, env=moi)
    ra = subprocess.run(["git", "-C", str(goc), "config", "--get", "core.hooksPath"],
                        capture_output=True, text=True, env=moi)
    if ra.stdout.strip():
        raise AssertionError(f"khoá NGOÀI danh sách #342 vẫn lọt: core.hooksPath="
                             f"{ra.stdout.strip()!r} ⇒ đang ghim khoá chứ chưa cắt nguồn")

    # (4) NGUỒN THỨ BA — cấu hình PHẠM VI LỆNH. Bản lượt 3 KHÔNG chặn nó, và nó thắng cả
    # repo-local. Hai chiều, vì chiều đối chứng là thứ chứng minh nền thù địch có thật.
    thu_lenh = {"GIT_CONFIG_COUNT": "1", "GIT_CONFIG_KEY_0": "commit.gpgsign",
                "GIT_CONFIG_VALUE_0": "true"}
    ban3 = dict(os.environ, **thu_lenh)
    for k in ("GIT_CONFIG_GLOBAL", "GIT_CONFIG_SYSTEM"):
        ban3[k] = os.devnull                      # hai nguồn KIA đã bị chặn sẵn…
    rc, e = _thu_commit(c.tmp / f"kho-thu-lenh-doi-chung-{time.time_ns()}", ban3)
    if rc == 0:
        raise BoQua("KHÔNG ĐO ĐƯỢC: nền `GIT_CONFIG_COUNT` vẫn commit được (máy này thiếu "
                    "gpg?) ⇒ chiều đối chứng vô nghĩa, không kết luận gì")

    sach3 = _ep_git_co_lap(dict(os.environ, **thu_lenh))
    rc, e = _thu_commit(c.tmp / f"kho-thu-lenh-co-lap-{time.time_ns()}", sach3)
    if rc != 0:
        raise AssertionError(f"cấu hình PHẠM VI LỆNH vẫn lọt qua `_ep_git_co_lap`: "
                             f"rc={rc} {e[:200]!r}")


# --- #338: hạ lời khai của guard + sổ khai báo ĐẾM ĐƯỢC -------------------------


def case_guard_KHONG_khai_minh_kiem_tham_quyen(c: Ctx):
    """Bản trước nói "Đây là cổng của người có quyền" — một phép kiểm KHÔNG TỒN TẠI.
    Cổng chặn một NHÃN VAI; phiên chạy bằng credential của chủ kho (đo: `get_me` ->
    ducthangho), nên nó không phân biệt được uỷ quyền thật với tự cấp.

    Ca này KHÔNG đo văn phong. Nó đo hai thứ cụ thể: (1) câu khẳng định cũ đã biến mất,
    (2) cơ chế CÒN THIẾU được gọi tên. Thiếu (2) thì hạ lời khai chỉ là xoá chữ."""
    sd = c.sd()
    rc, _, e = run(c.script, ["guard", "--action", "merge"], sd)
    _doi(7, rc, e, "guard merge")
    txt = _txt(e)
    if "cổng của người có quyền" in txt:
        raise AssertionError("guard vẫn khẳng định một phép kiểm thẩm quyền không tồn tại")
    for phai_co in ("LỜI NHẮC", "KHÔNG PHẢI PHÉP KIỂM THẨM QUYỀN", "TÁCH DANH TÍNH", "338"):
        if phai_co not in txt:
            raise AssertionError(f"thông điệp guard thiếu {phai_co!r}: {txt[:300]!r}")


def case_ghi_uy_quyen_doi_danh_sach_CHO_PHEP(c: Ctx):
    """Danh sách CẤM thua từ trong thiết kế — kho đã trả giá đúng một lần
    (`lease-authority-spoof` P1: `codex-dispatcher`/`ai-codex-bot`/`cödex` đều lọt).
    Ca này dùng LẠI đúng ba tên tấn công ấy."""
    sd = c.sd()
    sha = "a" * 40
    for xau in ("codex-dispatcher", "ai-codex-bot", "cödex", "claude", "codex", ""):
        rc, _, e = run(c.script, ["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", xau,
                                  "--bang-chung", "https://x", "--head-sha", sha], sd)
        if rc == 0:
            raise AssertionError(f"--nguoi-cap {xau!r} phải bị chặn, nhưng rc=0")
    rc, o, e = run(c.script, ["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", "ducthangho",
                              "--bang-chung", "https://x", "--head-sha", sha], sd)
    _doi(0, rc, e, "ghi-uy-quyen người cấp hợp lệ")
    if "LỜI KHAI" not in _txt(o):
        raise AssertionError("bản ghi phải tự khai nó là LỜI KHAI, không phải bằng chứng")


def case_ghi_uy_quyen_doi_sha40_that(c: Ctx):
    """Neo vào ĐÚNG head. Neo sai chỗ thì con số đối chiếu vô nghĩa."""
    sd = c.sd()
    for xau in ("deadbeef", "", "z" * 40, "a" * 39, "a" * 41):
        rc, _, _ = run(c.script, ["ghi-uy-quyen", "--action", "merge",
                                  "--nguoi-cap", "ducthangho", "--bang-chung", "https://x",
                                  "--head-sha", xau], sd)
        if rc == 0:
            raise AssertionError(f"--head-sha {xau!r} phải bị từ chối, nhưng rc=0")


def case_khai_uy_quyen_KHONG_mo_khoa_guard(c: Ctx):
    """Chốt trung tâm của #338: ghi khai báo KHÔNG được biến `rc=7` thành `rc=0`.
    Nếu nó mở khoá được thì nó là D1 — và D1 đã bị bác, vì phiên tự gõ được lệnh ấy."""
    sd = c.sd()
    sha = "b" * 40
    rc, _, e = run(c.script, ["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", "ducthangho",
                              "--bang-chung", "https://x", "--head-sha", sha], sd)
    _doi(0, rc, e, "ghi-uy-quyen")
    rc, _, e = run(c.script, ["guard", "--action", "merge"], sd)
    _doi(7, rc, e, "guard SAU khi đã khai — vẫn phải 7")


def case_doi_chieu_dem_duoc_merge_co_khai_va_khong(c: Ctx):
    """Biến KHÔNG ĐO ĐƯỢC thành SỐ. Dựng một kho tạm có merge thật rồi đếm hai chiều."""
    sd = c.sd()
    goc = c.tmp / f"kho-338-{time.time_ns()}"
    goc.mkdir(parents=True)
    g = lambda *a: subprocess.run(["git", "-C", str(goc), *a], capture_output=True)
    g("init", "--quiet", "-b", "main")
    g("config", "user.email", "t@t"); g("config", "user.name", "t")
    (goc / "a.txt").write_text("1\n", encoding="utf-8")
    g("add", "a.txt"); g("commit", "-qm", "goc")
    g("checkout", "-q", "-b", "nhanh")
    (goc / "b.txt").write_text("2\n", encoding="utf-8")
    g("add", "b.txt"); g("commit", "-qm", "viec")
    head_nhanh = subprocess.run(["git", "-C", str(goc), "rev-parse", "HEAD"],
                                capture_output=True, text=True).stdout.strip()
    g("checkout", "-q", "main")
    g("merge", "--no-ff", "-q", "nhanh", "-m", "Merge nhanh")
    # chua khai gi -> 1 merge, 0 co khai
    goc_sha = subprocess.run(["git", "-C", str(goc), "rev-list", "--max-parents=0", "HEAD"],
                             capture_output=True, text=True).stdout.split()[0]
    # SO RONG khac SO VANG, va do dung la phan biet packet nay vua dung: so vang =>
    # KHONG DO DUOC (rc=8, co ca rieng `doi_chieu_THIEU_SO_la_KHONG_DO_DUOC`); so rong =>
    # that su "0 khai bao". Tao so rong de do dung chieu thu hai.
    (sd / "uy_quyen_merge.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (sd / "uy_quyen_merge.jsonl").write_text("", encoding="utf-8")
    rc, o, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(goc), "--nhanh", "main",
                              "--since", goc_sha], sd)
    _doi(0, rc, e, "doi-chieu lan 1 (so RONG)")
    t = _txt(o)
    if "CÓ khai báo    : 0" not in t or "KHÔNG khai báo : 1" not in t:
        raise AssertionError(f"trước khi khai phải là 0/1, được: {t!r}")
    # khai dung head DA MERGE (cha thu hai) -> 1 co khai
    rc, _, e = run(c.script, ["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", "ducthangho",
                              "--bang-chung", "https://x", "--head-sha", head_nhanh], sd)
    _doi(0, rc, e, "ghi-uy-quyen head nhánh")
    rc, o, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(goc), "--nhanh", "main",
                              "--since", goc_sha], sd)
    _doi(0, rc, e, "doi-chieu lan 2")
    t = _txt(o)
    if "CÓ khai báo    : 1" not in t or "KHÔNG khai báo : 0" not in t:
        raise AssertionError(f"sau khi khai phải là 1/0, được: {t!r}")
    if "không nghĩa là đã được duyệt" not in t:
        raise AssertionError("đối chiếu phải tự khai nó đo TẦN SUẤT, không đo THẨM QUYỀN")


def case_doi_chieu_neo_dung_HEAD_da_merge_khong_phai_commit_merge(c: Ctx):
    """CHỈ cha thứ hai (HEAD đã merge) mới được tính. Khai vào SHA của chính commit
    merge KHÔNG được tính, và khai vào một SHA vô can cũng KHÔNG. Không có chốt này thì
    đếm gì cũng ra 'có khai'.

    Docstring này từng nói NGƯỢC hành vi (`"SHA của chính commit merge cũng được tính"`)
    — đúng cái lỗi mà chính finding `doi-chieu-nhan-sai-schema-va-sai-neo` tố cáo ở mã,
    chỉ là ở lời khai. Lúc KHAI thì commit merge CHƯA TỒN TẠI, nên neo vào nó là neo vào
    thứ chưa có."""
    sd = c.sd()
    goc = c.tmp / f"kho-338b-{time.time_ns()}"
    goc.mkdir(parents=True)
    g = lambda *a: subprocess.run(["git", "-C", str(goc), *a], capture_output=True)
    g("init", "--quiet", "-b", "main")
    g("config", "user.email", "t@t"); g("config", "user.name", "t")
    (goc / "a.txt").write_text("1\n", encoding="utf-8")
    g("add", "a.txt"); g("commit", "-qm", "goc")
    g("checkout", "-q", "-b", "nhanh")
    (goc / "b.txt").write_text("2\n", encoding="utf-8")
    g("add", "b.txt"); g("commit", "-qm", "viec")
    g("checkout", "-q", "main")
    g("merge", "--no-ff", "-q", "nhanh", "-m", "Merge nhanh")
    (sd / "uy_quyen_merge.jsonl").parent.mkdir(parents=True, exist_ok=True)
    (sd / "uy_quyen_merge.jsonl").write_text("", encoding="utf-8")
    rc, _, e = run(c.script, ["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", "ducthangho",
                              "--bang-chung", "https://x", "--head-sha", "c" * 40], sd)
    _doi(0, rc, e, "ghi-uy-quyen sha vô can")
    goc_sha = subprocess.run(["git", "-C", str(goc), "rev-list", "--max-parents=0", "HEAD"],
                             capture_output=True, text=True).stdout.split()[0]
    rc, o, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(goc), "--nhanh", "main",
                              "--since", goc_sha], sd)
    _doi(0, rc, e, "doi-chieu")
    if "KHÔNG khai báo : 1" not in _txt(o):
        raise AssertionError("khai vào SHA vô can KHÔNG được tính là có khai")
    # Chieu thu hai, do duoc chu khong chi tuyen bo: khai vao chinh COMMIT MERGE cung
    # KHONG duoc tinh. Ban truoc chu thich noi vay ma MA nhan ca hai, va ca test mang ten
    # "khong phai commit merge" chua bao gio dung mot ban ghi nhu the.
    merge_sha = subprocess.run(["git", "-C", str(goc), "rev-parse", "main"],
                               capture_output=True, text=True).stdout.strip()
    rc, _, e = run(c.script, ["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", "ducthangho",
                              "--bang-chung", "https://x", "--head-sha", merge_sha], sd)
    _doi(0, rc, e, "ghi-uy-quyen vao COMMIT MERGE")
    rc, o, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(goc), "--nhanh", "main",
                              "--since", goc_sha], sd)
    _doi(0, rc, e, "doi-chieu sau khi khai vao commit merge")
    if "KHÔNG khai báo : 1" not in _txt(o):
        raise AssertionError("khai vào chính COMMIT MERGE KHÔNG được tính — lúc khai nó "
                             "chưa tồn tại")


def case_doi_chieu_chi_dem_FIRST_PARENT(c: Ctx):
    """P2 `doi-chieu-dem-ca-merge-ben-nhanh` (cross-review PR #343, DA TAI HIEN).

    Thieu `--first-parent`, lenh dem ca merge nam BEN TRONG nhanh phu nhu mot merge "tren
    master". Do tren kho that, dung cua so cua Issue #338: `--merges` -> 10,
    `--merges --first-parent` -> 9. Con so `9` executor khai o luot 1 do bang mot lenh
    KHAC voi lenh da giao.

    Fixture dung dung hinh dang ay: nhanh phu MERGE master vao no truoc, roi moi merge
    nhanh phu vao master."""
    sd = c.sd()
    goc = c.tmp / f"kho-fp-{time.time_ns()}"
    goc.mkdir(parents=True)
    def g(*a):
        return subprocess.run(["git", "-C", str(goc), *a], capture_output=True, text=True)
    g("init", "--quiet", "-b", "main")
    for k, v in (("user.email", "t@t"), ("user.name", "t"), ("commit.gpgsign", "false")):
        g("config", k, v)
    (goc / "a.txt").write_text("1\n", encoding="utf-8")
    g("add", "a.txt"); g("commit", "-qm", "goc")
    goc_sha = g("rev-parse", "HEAD").stdout.strip()
    g("checkout", "-q", "-b", "phu")
    (goc / "b.txt").write_text("2\n", encoding="utf-8")
    g("add", "b.txt"); g("commit", "-qm", "viec phu")
    g("checkout", "-q", "main")
    (goc / "c.txt").write_text("3\n", encoding="utf-8")
    g("add", "c.txt"); g("commit", "-qm", "viec main")
    g("checkout", "-q", "phu")
    g("merge", "--no-ff", "-q", "main", "-m", "Merge main VAO nhanh phu")   # merge BEN TRONG
    g("checkout", "-q", "main")
    g("merge", "--no-ff", "-q", "phu", "-m", "Merge phu vao main")          # merge first-parent
    so = c.tmp / f"so-fp-{time.time_ns()}.jsonl"
    so.write_text("", encoding="utf-8")
    rc, o, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(goc), "--nhanh", "main",
                              "--since", goc_sha, "--so", str(so)], sd)
    _doi(0, rc, e, "doi-chieu first-parent")
    t = _txt(o)
    if "merge trên main: 1" not in t:
        raise AssertionError(f"phai dem DUNG 1 merge first-parent, duoc: {t!r}")
    if "(first-parent)" not in t:
        raise AssertionError("phai in ro cua so la first-parent")
    # doi chung: khong first-parent thi git thay HAI merge — chung minh fixture co that
    tho = g("rev-list", "--count", "--merges", goc_sha + "..main").stdout.strip()
    fp = g("rev-list", "--count", "--merges", "--first-parent", goc_sha + "..main").stdout.strip()
    if (tho, fp) != ("2", "1"):
        raise AssertionError(f"fixture khong dung hinh dang: tho={tho} fp={fp} (can 2/1)")


def case_doi_chieu_THIEU_SO_la_KHONG_DO_DUOC(c: Ctx):
    """P2 `so-khai-cuc-bo-bien-mat-thanh-khong-khai`. So mac dinh nam trong thu muc bi
    `.gitignore` loai, nen mot clone moi khong phan biet duoc "khong co khai bao" voi "so
    khong duoc chuyen sang". Tra 0 la doc cai IM LANG thanh mot phep do."""
    sd = c.sd()
    rc, _, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(ROOT), "--nhanh", "HEAD",
                              "--since", "HEAD~1",
                              "--so", str(c.tmp / f"khong-ton-tai-{time.time_ns()}.jsonl")], sd)
    if rc == 0:
        raise AssertionError("thieu so PHAI la KHONG DO DUOC, khong duoc tra 0 va rc=0")
    if "KHONG DO DUOC" not in _txt(e):
        raise AssertionError(f"phai noi ro KHONG DO DUOC, stderr={_txt(e)[:200]!r}")


def case_doi_chieu_TU_CHOI_ban_ghi_sai_luoc_do(c: Ctx):
    """P2 `doi-chieu-nhan-sai-schema-va-sai-neo`. Ban truoc chi doi co truong `head_sha`,
    nen mot ban ghi cua action KHAC hoac mot dong JSON viet tay cung duoc tinh."""
    sd = c.sd()
    sha_that = subprocess.run(["git", "-C", str(ROOT), "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    so = c.tmp / f"so-xau-{time.time_ns()}.jsonl"
    xau = [
        {"head_sha": sha_that},                                              # thieu het
        {"event": "linh_tinh", "action": "merge", "nguoi_cap": "ducthangho",
         "bang_chung": "x", "head_sha": sha_that},                           # sai event
        {"event": "uy_quyen_merge_KHAI_BAO", "action": "deploy", "nguoi_cap": "ducthangho",
         "bang_chung": "x", "head_sha": sha_that},                           # sai action
        {"event": "uy_quyen_merge_KHAI_BAO", "action": "merge", "nguoi_cap": "codex-dispatcher",
         "bang_chung": "x", "head_sha": sha_that},                           # nguoi cap gia mao
        {"event": "uy_quyen_merge_KHAI_BAO", "action": "merge", "nguoi_cap": "ducthangho",
         "bang_chung": "x", "head_sha": "deadbeef"},                         # sha khong hop le
    ]
    so.write_text("\n".join(json.dumps(x) for x in xau) + "\n", encoding="utf-8")
    rc, o, e = run(c.script, ["doi-chieu-uy-quyen", "--root", str(ROOT), "--nhanh", "HEAD",
                              "--since", "HEAD~1", "--so", str(so)], sd)
    _doi(0, rc, e, "doi-chieu so xau")
    t = _txt(o)
    if "BO QUA 5 ban ghi" not in t:
        raise AssertionError(f"phai BO QUA ca 5 ban ghi sai luoc do, duoc: {t[:300]!r}")
    if "CÓ khai báo    : 0" not in t:
        raise AssertionError("khong ban ghi sai nao duoc tinh la co khai")


# --- (b) dấu vết comment -------------------------------------------------------


def case_transition_hop_le_rc0(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    if c.state(sd, 55) != "reviewing":
        raise AssertionError("transition hợp lệ phải đổi được state")


def case_comment_id_chua_dang_ky_bi_tu_choi(c: Ctx):
    """ID bịa — chưa từng ghi sổ — phải bị từ chối."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", "5258163128", "--head-sha", HEAD_HOP_LE], sd)
    _doi_ly_do(5, rc, e, "chưa có trong sổ", "ID chưa ghi sổ phải bị từ chối")


def case_comment_id_dung_lai_bi_tu_choi(c: Ctx):
    """Cùng một ID dùng cho transition THỨ HAI phải bị từ chối.

    Dựng lại sau finding `review-transition-bypasses-record-review`: bản trước quay
    về `running` bằng `transition`, cửa đó nay ĐÃ ĐÓNG. Đường hợp lệ duy nhất ra
    khỏi `reviewing` là một VERDICT — nên vòng hai đi qua `record-review
    --verdict changes_requested`, rồi `begin-attempt` mở lượt mới. Ca vẫn đo đúng
    thứ nó khai: một `comment-id` đã tiêu thụ không dùng lại được.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    cid_rev1 = c.den_reviewing(sd, 55, 1)
    # Ra khỏi `reviewing` bằng VERDICT, không bằng `transition`.
    rc, _, e = c.review(sd, 55, ["mot-loi"], luot=1)
    _doi(0, rc, e, "record-review changes_requested đưa về running")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt lượt 2")
    # Vào `reviewing` vòng 2 bằng ĐÚNG id đã tiêu thụ ở vòng 1. State lúc này là
    # `running` nên BẢNG CHUYỂN cho phép — thứ phải chặn là SỔ COMMENT. Đo như vậy
    # mới cô lập được chốt "mỗi ID dùng đúng MỘT lần". Nếu dùng một id mới rồi mới
    # thử lại id cũ thì lệnh chết vì `reviewing → reviewing` không hợp lệ, và ca hoá
    # ra đang đo bảng chuyển chứ không đo sổ comment.
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing", "--comment-id", cid_rev1,
                    "--head-sha", c.head(2)], sd)
    _doi(5, rc, e, "ID đã tiêu thụ không được dùng lại")


def case_comment_id_sai_transition_bi_tu_choi(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "accepted", "--comment-id", "7770000002"], sd)
    _doi(0, rc, e, "record-post accepted")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", "7770000002", "--head-sha", HEAD_HOP_LE], sd)
    _doi_ly_do(5, rc, e, "accepted", "ID đăng ký cho transition khác không dùng chéo được")


def case_thieu_comment_id_chan_transition(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing", "--head-sha", HEAD_HOP_LE], sd)
    _doi_ly_do(5, rc, e, "thiếu --comment-id", "chưa đăng comment thì transition phải bị chặn")


def case_record_post_id_sai_dang_bi_tu_choi(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    for xau in ("abc", "123", "https://github.com/x/y/issues/55#issuecomment-1", "-1", ""):
        rc, _, e = run(c.script,
                       ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", xau], sd)
        if rc == 0:
            raise AssertionError(f"id sai dạng {xau!r} phải bị từ chối, nhưng rc=0")


def case_record_post_trung_id_bi_tu_choi(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000003"], sd)
    _doi(0, rc, e, "record-post lần 1")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "running", "--comment-id", "7770000003"], sd)
    _doi(5, rc, e, "ghi trùng một ID phải bị từ chối")


def case_transition_khong_hop_le_thoat_8(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "accepted", "--comment-id", "7770000004"], sd)
    _doi(0, rc, e, "record-post")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "accepted", "--comment-id", "7770000004"], sd)
    _doi(8, rc, e, "leased → accepted phải bị từ chối")


def case_accepted_chi_dat_duoc_qua_record_review(c: Ctx):
    """`accepted` phải có ĐÚNG MỘT cửa vào: record-review --verdict approve.

    Lỗ đã đo: khi `accepted` còn là đích hợp lệ của `transition`, một lệnh
    `transition --to accepted` kèm comment-id hợp lệ đi thẳng vào `accepted` với
    `reviews: []` và `accepted_sha: null` — mỏ neo SHA bị vô hiệu hoàn toàn.

    Ca này thử từ MỌI state mà CLI với tới được, chứ không chỉ chỗ đã hở, để lần
    sau có ai mở lại một cửa khác thì vẫn bị bắt.
    """
    import json
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")

    def thu_accepted(nhan, cid):
        rc, _, e = run(c.script,
                       ["record-post", "--packet", 55, "--for", "accepted", "--comment-id", cid], sd)
        _doi(0, rc, e, f"record-post accepted ({nhan})")
        rc, _, e = run(c.script,
                       ["transition", "--packet", 55, "--to", "accepted", "--comment-id", cid], sd)
        if rc == 0:
            raise AssertionError(f"[{nhan}] transition --to accepted phải bị từ chối")
        if c.state(sd, 55) == "accepted":
            raise AssertionError(f"[{nhan}] state KHÔNG được thành accepted")

    thu_accepted("từ leased", "8880000101")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    thu_accepted("từ running", "8880000102")
    cid = str(9_000_000_000 + 55 * 1000 + 2)
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", cid], sd)
    _doi(0, rc, e, "record-post reviewing")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", cid, "--head-sha", c.head(1)], sd)
    _doi(0, rc, e, "transition reviewing")
    thu_accepted("từ reviewing", "8880000103")

    # và bất biến: nếu có accepted thì PHẢI có review + accepted_sha
    rc, o, e = run(c.script, ["status", "--packet", 55], sd)
    _doi(0, rc, e, "status")
    st = json.loads(o.decode("utf-8"))
    if st["state"] == "accepted" and (not st["reviews"] or not st["accepted_sha"]):
        raise AssertionError("accepted mà không có review/accepted_sha là vô nghĩa")


def case_vao_reviewing_phai_co_luot_dang_mo(c: Ctx):
    """Sau changes_requested, quay lại `reviewing` phải mở lượt mới trước.

    Lỗ đã đo: không có chốt này thì hai review dồn vào CÙNG một attempt, nên lặp
    một finding đủ khoá cứng packet trong khi mới tiêu 1/3 lượt — trần same-failure
    bắn đúng lúc trần attempt còn nguyên.
    """
    import json
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["loi-can-sua"])
    _doi(0, rc, e, "changes_requested lượt 1")
    rc, o, e = run(c.script, ["status", "--packet", 55], sd)
    _doi(0, rc, e, "status")
    if json.loads(o.decode("utf-8"))["attempt_open"]:
        raise AssertionError("sau review, lượt phải đóng")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "8882000001"], sd)
    _doi(0, rc, e, "record-post")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", "8882000001", "--head-sha", c.head(2)], sd)
    if rc == 0:
        raise AssertionError("vào reviewing khi không có lượt mở phải bị từ chối")
    # chiều DƯƠNG: mở lượt rồi thì vào được
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt lượt 2")
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "8882000002"], sd)
    _doi(0, rc, e, "record-post 2")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", "8882000002", "--head-sha", c.head(2)], sd)
    _doi(0, rc, e, "mở lượt rồi thì phải vào được reviewing")


def case_doctrine_scan_bat_qua_ngat_dong(c: Ctx):
    """Doctrine bị XUỐNG DÒNG kiểu Markdown thường vẫn phải bị bắt.

    Đã ĐO trước khi sửa: 3/3 cụm thử lọt sạch vì bộ so chạy theo DÒNG VẬT LÝ.
    Ngắt dòng là thứ người viết làm vô thức, nên chốt nào thua nó thì thua
    thường xuyên chứ không phải hiếm.
    """
    nl = "\n"
    bien_the = [
        ("ngắt trước accepted",
         "proposed → ready → leased → running → reviewing" + nl + "→ accepted → integrated → landed"),
        ("ngắt giữa cụm merged", "merged: PR đã vào" + nl + "nhánh đích của PR"),
        ("ngắt giữa ô vai trò",
         "Sửa đúng effective write set" + nl + "trên branch của generation"),
        ("ngắt + nháy ngược", "`merged`: PR đã vào" + nl + "`nhánh` đích của PR"),
        ("ngắt qua dòng trống", "merged: PR đã vào" + nl + nl + "nhánh đích của PR"),
        ("ngắt ba mảnh",
         "proposed → ready → leased →" + nl + "running → reviewing →" + nl + "accepted → integrated → landed"),
    ]
    lot = []
    for i, (ten, txt) in enumerate(bien_the):
        r = _repo_gia(c.tmp, "# Adapter" + nl + nl + txt + nl, ten=f"ngat{i}")
        rc, _, _ = run(c.script, ["doctrine-scan", "--root", r])
        if rc != 6:
            lot.append(f"{ten} (rc={rc})")
    if lot:
        raise AssertionError(f"{len(lot)}/{len(bien_the)} biến thể ngắt dòng LỌT: {', '.join(lot)}")


# --- §8 quota không tiêu thụ attempt -------------------------------------------


def _mo_luot(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    _doi(0, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)[0:1],
         b"", "begin-attempt")
    return sd


def _void_may(c, sd, f, reason="infrastructure"):
    return run(c.script, ["void-attempt", "--packet", 55, "--reason", reason,
                          "--bang-chung", f], sd)


def case_void_khong_bang_chung_phai_ghi_so(c: Ctx):
    sd = _mo_luot(c)
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota"], sd)
    _doi(10, rc, e, "quota trần không được hoàn ngoài hai cửa")
    _doi(0, *run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota", *VOID_DUYET], sd)[0:1],
         b"", "cửa có người duyệt")
    st = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    assert any(x.get("event") == "void_khong_co_bang_chung" for x in st["history"])


def case_void_cung_run_hai_lan_bi_chan(c: Ctx):
    sd = _mo_luot(c); f = run_json_that(c, sd)
    lan_dau = _void_may(c, sd, f)
    # Ca âm này không đo đường chấp nhận: nếu một bản khác siết từ chối mọi run,
    # P6 phải đỏ còn P2 vẫn xanh. Bản chuẩn và đột biến bỏ-đốt đều đi tiếp ở đây.
    if lan_dau[0] != 0:
        _doi(10, lan_dau[0], lan_dau[2], "lần đầu bị từ chối")
        return
    rc, _, e = _void_may(c, sd, f)
    _doi(10, rc, e, "phát lại"); assert "đã dùng".encode() in e


def case_void_lat_phan_quyet_bi_hmac_chan(c: Ctx):
    for kieu in ("run", "doctor"):
        sd = _mo_luot(c); f = run_json_that(c, sd, xong=True) if kieu == "run" else Path(anh_doctor_ky(sd, thieu_bat_buoc=["rg"]))
        d = json.loads(f.read_text(encoding="utf-8")); d["trang_thai" if kieu == "run" else "he_dieu_hanh"] = "hong"
        f.write_text(json.dumps(d), encoding="utf-8")
        rc, _, e = _void_may(c, sd, f)
        _doi(10, rc, e, f"sửa {kieu}"); assert "bị sửa".encode() in e


def case_void_run_cheo_luot_bi_chan(c: Ctx):
    sd = _mo_luot(c); f = run_json_that(c, sd)
    _doi(0, *run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota",
                            *VOID_DUYET], sd)[0:1], b"", "đóng lượt 1 có ghi sổ")
    _doi(0, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)[0:1],
         b"", "mở lượt 2")
    rc, _, e = _void_may(c, sd, f)
    _doi(10, rc, e, "chéo lượt")


def case_void_run_cu_khong_neo_co_thong_diep_rieng(c: Ctx):
    sd = _mo_luot(c); cu = c.tmp / "run-cu.json"; cu.write_text('{"trang_thai":"hong"}', encoding="utf-8")
    for f in (cu, anh_doctor()):
        rc, _, e = _void_may(c, sd, f); _doi(10, rc, e, "bằng chứng cũ")
        assert _txt(e) == "bằng chứng máy không có neo lượt — dùng `--khong-co-bang-chung` (có ghi sổ)"


def case_void_run_that_dung_luot_duoc_tha(c: Ctx):
    sd = _mo_luot(c); f = run_json_that(c, sd)
    _doi(0, *_void_may(c, sd, f)[0:1], b"", "run thật đúng lượt")


def case_void_hai_ly_do_khong_dung_chung_run(c: Ctx):
    sd = _mo_luot(c); f = run_json_that(c, sd, reason="permission")
    _doi(10, *_void_may(c, sd, f, "infrastructure")[0:1], b"", "một run chứng minh hai lý do")
    _doi(0, *_void_may(c, sd, f, "permission")[0:1], b"", "permission có run riêng")


def case_void_phan_biet_loi_probe_va_sau_spawn(c: Ctx):
    sd = _mo_luot(c)
    probe = json.loads(run_json_that(c, sd, loi_probe=True).read_text(encoding="utf-8"))
    sau_path = run_json_that(c, sd, truoc_spawn=False)
    sau = json.loads(sau_path.read_text(encoding="utf-8"))
    assert probe.get("giai_doan") == "probe" and sau.get("giai_doan") is None
    assert probe["probe"]["spawn"]["trang_thai"] == "DO"
    assert sau["probe"]["spawn"]["trang_thai"] == "DAT"
    assert not {"nonce", "chu_ky"} & probe.keys()
    assert {"nonce", "chu_ky"} <= sau.keys()
    assert "void_reason" not in sau
    before = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))["attempts_used"]
    _doi(10, *_void_may(c, sd, sau_path)[0:1], b"", "unknown post-spawn cannot refund")
    assert json.loads((sd / "wp55.json").read_text(encoding="utf-8"))["attempts_used"] == before
    assert probe["ma_thoat"] != sau["ma_thoat"]


def _anh_doctor_luot_truoc(c: Ctx, cham=False):
    sd = _mo_luot(c); f = anh_doctor_ky(sd, thieu_bat_buoc=["rg"])
    _doi(0, *_void_may(c, sd, f)[0:1], b"", "ảnh chụp trong lượt 1")
    _doi(0, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)[0:1],
         b"", "mở lượt 2")
    if cham: Path(f).touch()
    return sd, f


def case_void_cung_anh_doctor_hai_luot_bi_chan(c: Ctx):
    sd, f = _anh_doctor_luot_truoc(c)
    rc, _, e = _void_may(c, sd, f)
    _doi(10, rc, e, "phát lại ảnh lượt 1"); assert "neo thuộc lượt khác".encode() in e


def case_void_touch_anh_doctor_cu_van_bi_chan(c: Ctx):
    sd, f = _anh_doctor_luot_truoc(c, cham=True)
    rc, _, e = _void_may(c, sd, f)
    _doi(10, rc, e, "touch ảnh cũ"); assert "neo thuộc lượt khác".encode() in e


def case_chup_anh_doctor_ky_noi_bo(c: Ctx):
    sd = _mo_luot(c); f = c.tmp / "doctor-signed.json"
    _doi(0, *run(c.script, ["chup-anh-doctor", "--packet", 55, "--out", f], sd)[0:1], b"", "chụp")
    d = json.loads(f.read_text(encoding="utf-8")); st = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    assert d["nonce"] == st["attempt_anchor"]["nonce"]
    assert d["chu_ky"] == ky_ban_ghi_luot(d, st["hmac_key"])


def case_anh_doctor_nen_chung_tuoi_chi_begin(c: Ctx):
    for kieu in ("nen", "tuoi"):
        f = anh_doctor(he_dieu_hanh="Plan9") if kieu == "nen" else anh_doctor(ok=True)
        if kieu == "tuoi": os.utime(f, (time.time() - 7200,) * 2)
        sd = c.sd(); _doi(0, *c.init(sd)[0:1], b"", "init")
        _doi(10, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR,
                                "--bang-chung-moi-truong", f], sd)[0:1], b"", f"begin {kieu}")
        sd = _mo_luot(c)
        f = anh_doctor_ky(sd, he_dieu_hanh="Plan9" if kieu == "nen" else platform.system(),
                          thieu_bat_buoc=["codex"])
        if kieu == "tuoi": os.utime(f, (time.time() - 7200,) * 2)
        _doi(10 if kieu == "nen" else 0, *_void_may(c, sd, f)[0:1], b"", f"void {kieu}")


def case_ma_in_thang_gioi_han_cung_principal(c: Ctx):
    s = (HERE / "launcher.py").read_text(encoding="utf-8")
    assert "chống VÔ Ý" in s and "chống PHÁT LẠI" in s and "cùng principal" in s


def case_void_attempt_allowlist(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota", *VOID_DUYET], sd)
    _doi(0, rc, e, "quota phải hoàn được lượt")


def case_void_xong_van_mo_lai_duoc_luot(c: Ctx):
    """Chiều BẮT OAN: hoàn lượt vì quota không được khoá cứng packet.

    Nếu `void-attempt` trả trần mà quên đóng lượt đang mở thì begin-attempt sau
    đó bị từ chối vĩnh viễn — một lỗi hạ tầng tạm thời hoá thành ngõ cụt.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt lần 1")
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota", *VOID_DUYET], sd)
    _doi(0, rc, e, "void vì quota")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "sau khi hoàn lượt phải mở lại được lượt")
    rc, o, e = run(c.script, ["status", "--packet", 55], sd)
    _doi(0, rc, e, "status")
    import json
    if json.loads(o.decode("utf-8"))["attempts_used"] != 1:
        raise AssertionError("hoàn rồi mở lại phải cho attempts_used = 1")


def case_void_attempt_ly_do_tu_che_bi_tu_choi(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    for ly_do in ("toi-ban", "content", "khong-thich", "vi-sao-cung-duoc"):
        rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", ly_do], sd)
        if rc == 0:
            raise AssertionError(f"lý do tự chế {ly_do!r} phải bị từ chối")


def case_void_sau_review_bi_chan(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["mot-loi-nao-do"])
    _doi(0, rc, e, "review")
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota"], sd)
    if rc == 0:
        raise AssertionError("lượt ĐÃ review không được hoàn")


# --- (c) doctrine-scan hai chiều ----------------------------------------------


SACH = "# Adapter demo\n\n**Đọc trước:** `docs/PROTOCOL_DA_PHIEN.md` §13.\n\nDưới đây chỉ có cú pháp của nền.\n"

CUM_TU_THU = [
    "max_attempts_per_packet: 3",
    "proposed → ready → leased → running → reviewing → accepted → integrated → landed",
    "Land Operator",
    "LAND OPERATOR",
    "landed: kết quả đã vào canonical",
    "paused | blocked | cancelled | stale",
    "Dispatcher/reconciler",
    "45 phút/run",
]


# Nguồn đối chiếu TRUNG TÍNH cho cây giả: đủ dài để qua `_PROTO_TU_TOI_THIEU`, và cố ý
# KHÔNG chứa câu chữ nào của protocol thật lẫn của các adapter mẫu — nên nó không tự sinh
# phát hiện. Dùng protocol THẬT làm mặc định là sai: nó nặng, và nó buộc các ca đối chứng
# vốn "khác họ" phải phụ thuộc vào đường đọc protocol, làm 36 phép kiểm đột biến đỏ (đo được).
_PROTO_TRUNG_TINH = ("man xanh luc bao phu trien doi thoai nguyen so bay muoi hai "
                     "cau chuyen ve mot chiec thuyen go tren song vang " * 20)


def _repo_gia(tmp: Path, noi_dung: str, ten="demo", protocol: str | None = None) -> Path:
    """Cây giả cho `doctrine-scan`, NAY luôn có nguồn đối chiếu dưới `--root`.

    Bản trước chỉ dựng `.claude/skills/<ten>/SKILL.md`, nên mọi ca dùng nó đo theo protocol
    của kho THẬT qua fallback `parents[2]`; `--root` chỉ góp phần adapter. Đo được: gỡ
    fallback thì `doctrine_scan_chep_tron_5_1_bi_chan` và `..._chep_doan_ngan_...` ĐỎ ngay
    — hai ca ấy chưa từng đo cây mà chúng khai là đang đo.

    `protocol=None` ⇒ ghi nguồn TRUNG TÍNH (ca không nói gì về chép). Ca nào đo hành vi chép
    thì truyền protocol THẬT vào, tường minh, để người đọc thấy nguồn so sánh là gì.
    """
    r = tmp / f"repo_{abs(hash(noi_dung)) % 10**8}_{ten}"
    d = r / ".claude" / "skills" / ten
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(noi_dung, encoding="utf-8", newline="\n")
    (r / "docs").mkdir(parents=True, exist_ok=True)
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(
        protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding="utf-8", newline="\n")
    return r


def case_doctrine_scan_sach_xanh(c: Ctx):
    r = _repo_gia(c.tmp, SACH)
    rc, o, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(0, rc, e, "adapter sạch phải XANH")


def case_doctrine_scan_bom_cum_tu_do(c: Ctx):
    for i, cum in enumerate(CUM_TU_THU):
        r = _repo_gia(c.tmp, SACH + f"\nGhi chú: {cum}\n", ten=f"bom{i}")
        rc, o, e = run(c.script, ["doctrine-scan", "--root", r])
        if rc != 6:
            raise AssertionError(f"bơm {cum!r} phải ĐỎ (rc=6), được rc={rc}")


def case_doctrine_scan_bat_doctrine_THAT_tu_protocol(c: Ctx):
    """Chép DÒNG THẬT từ docs/PROTOCOL_DA_PHIEN.md vào adapter ⇒ phải ĐỎ hết.

    Đây là ca đắt nhất của bộ này. Bơm cụm từ do chính mình soạn chỉ chứng minh
    danh sách khớp với chính nó; lấy dòng từ NGUỒN mới chứng minh nó phủ được
    doctrine thật. Lần chạy đầu ca này bắt 4/9 — 5 dòng lọt CHỈ vì dấu nháy
    ngược của Markdown (`merged`: … không khớp "merged: …"), đúng loại lỗ đã làm
    ba lượt review trước trượt.

    Ca này đọc protocol LÚC CHẠY, nên khi doctrine đổi câu chữ mà danh sách cấm
    không theo, nó sẽ đỏ thay vì im lặng mục ruỗng.
    """
    proto = ROOT / "docs" / "PROTOCOL_DA_PHIEN.md"
    if not proto.is_file():
        raise AssertionError(f"thiếu {proto}")
    neo = (
        "| Dispatcher", "| Executor", "| Reviewer", "| Land Operator",
        "| Người có thẩm quyền", "proposed →", "- `merged`", "- `integrated`",
        "- `landed`", "- `complete`", "Mặc định: 3 attempt/packet",
    )
    dong = [
        (i, l.strip())
        for i, l in enumerate(proto.read_text(encoding="utf-8").splitlines(), 1)
        if l.strip().startswith(neo) and len(l.strip()) >= 40
    ]
    if len(dong) < 8:
        raise AssertionError(f"chỉ tìm được {len(dong)} dòng doctrine — mỏ neo có thể đã trôi")
    lot = []
    for n, (ln, s) in enumerate(dong):
        r = _repo_gia(c.tmp, f"# Adapter\n\nĐọc trước: docs/PROTOCOL_DA_PHIEN.md.\n\n{s}\n",
                      ten=f"that{n}")
        rc, _, _ = run(c.script, ["doctrine-scan", "--root", r])
        if rc != 6:
            lot.append(f"protocol:{ln} rc={rc} :: {s[:80]}")
    if lot:
        raise AssertionError(
            f"{len(lot)}/{len(dong)} dòng doctrine THẬT lọt lưới:\n  " + "\n  ".join(lot)
        )


def case_doctrine_scan_repo_that_sach(c: Ctx):
    """Adapter THẬT trong kho này phải sạch — nếu không thì tiêu chí là lời hứa."""
    rc, o, e = run(c.script, ["doctrine-scan", "--root", ROOT])
    _doi(0, rc, e, f"adapter thật phải sạch; stderr={_txt(e)}")


def case_doctrine_scan_chep_tron_5_1_bi_chan(c: Ctx):
    """A1 — Chép trọn §5.1 của protocol vào adapter ⇒ phải ĐỎ (rc=6)."""
    proto = ROOT / "docs" / "PROTOCOL_DA_PHIEN.md"
    raw = proto.read_text(encoding="utf-8")
    m = re.search(r"(## 5\.1 .*?)(?=\n## |\Z)", raw, re.DOTALL)
    if not m:
        raise AssertionError("không tìm thấy §5.1 trong protocol")
    sec_5_1 = m.group(1)
    r = _repo_gia(c.tmp, f"# Adapter\n\n{sec_5_1}\n", ten="sec_5_1", protocol=raw)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "chép trọn §5.1 phải ĐỎ (rc=6)")


def case_doctrine_scan_chep_doan_ngan_5_1_bi_chan(c: Ctx):
    """A1 — Chép đoạn ngắn 29 từ từ §5.1 (không dính 28 cụm cấm) ⇒ phải ĐỎ (rc=6)."""
    proto = ROOT / "docs" / "PROTOCOL_DA_PHIEN.md"
    raw = proto.read_text(encoding="utf-8")
    m = re.search(r"## 5\.1\s+.*?\n(.*?)(?=\n## |\Z)", raw, re.DOTALL)
    if not m:
        raise AssertionError("không tìm thấy §5.1 trong protocol")
    lines = [
        line.strip()
        for line in m.group(1).splitlines()
        if line.strip() and not line.strip().startswith(("#", "```", "-"))
    ]
    words = " ".join(lines).split()
    doan = " ".join(words[:29])
    r = _repo_gia(c.tmp, f"# Adapter\n\n{doan}\n", ten="sec_5_1_ngan", protocol=raw)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "chép đoạn ngắn 29 từ của §5.1 phải ĐỎ (rc=6)")


def case_doctrine_scan_chep_12_bi_chan(c: Ctx):
    """A1 — Chép đoạn văn xuôi thuần §12 (không dính 28 cụm cấm) ⇒ phải ĐỎ (rc=6).

    Khác bản trước: bản trước chép trọn §12 (vốn chứa cả cụm cấm cũ như 'người có
    thẩm quyền'), nên khi tắt n-gram (`bo_kiem_chep_protocol`), ca này vẫn XANH.
    Đoạn này lấy 30 từ văn xuôi thuần ở §12 không dính bất kỳ cụm nào trong 28 cụm cấm
    cũ, chứng minh cơ chế so sánh n-gram mới thật sự đo được hành vi chép.
    """
    proto = ROOT / "docs" / "PROTOCOL_DA_PHIEN.md"
    raw = proto.read_text(encoding="utf-8")
    m = re.search(r"(## 12\.\s+.*?)(?=\n## 13|\Z)", raw, re.DOTALL)
    if not m:
        raise AssertionError("không tìm thấy §12 trong protocol")
    sec_12 = m.group(1)
    words = [w for w in sec_12.split() if not w.startswith("#")]
    doan = " ".join(words[45:75])
    r = _repo_gia(c.tmp, f"# Adapter\n\n{doan}\n", ten="sec_12_ngan", protocol=raw)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "chép đoạn ngắn §12 không dính cụm cấm phải ĐỎ (rc=6)")


def case_doctrine_scan_fail_close_thieu_protocol(c: Ctx):
    """Fail-close: thiếu docs/PROTOCOL_DA_PHIEN.md dưới --root ⇒ phải ĐỎ (rc=2)."""
    r = c.tmp / "repo_thieu_proto"
    d = r / ".claude" / "skills" / "demo"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(SACH, encoding="utf-8", newline="\n")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(2, rc, e, "thiếu PROTOCOL_DA_PHIEN.md phải ĐỎ (rc=2)")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {_txt(e)!r}")


def case_doctrine_scan_fail_close_khong_phai_utf8(c: Ctx):
    """Fail-close: PROTOCOL_DA_PHIEN.md lỗi UTF-8 ⇒ phải ĐỎ (rc=2)."""
    r = c.tmp / "repo_proto_khong_utf8"
    d = r / ".claude" / "skills" / "demo"
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(SACH, encoding="utf-8", newline="\n")
    (r / "docs").mkdir(parents=True, exist_ok=True)
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_bytes(b"\x80\x81\xff\xfe")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(2, rc, e, "PROTOCOL_DA_PHIEN.md lỗi UTF-8 phải ĐỎ (rc=2)")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {_txt(e)!r}")


def case_doctrine_scan_fail_close_protocol_ngan(c: Ctx):
    """Fail-close: PROTOCOL_DA_PHIEN.md quá ngắn (< 200 từ) ⇒ phải ĐỎ (rc=2)."""
    proto_ngan = "tu " * 50
    r = _repo_gia(c.tmp, SACH, ten="proto_ngan", protocol=proto_ngan)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(2, rc, e, "PROTOCOL_DA_PHIEN.md quá ngắn (< 200 từ) phải ĐỎ (rc=2)")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {_txt(e)!r}")


def case_doctrine_scan_fail_close_chi_co_fence(c: Ctx):
    """Fail-close: PROTOCOL_DA_PHIEN.md chỉ có code fence (bỏ fence rỗng/<200 từ) ⇒ phải ĐỎ (rc=2)."""
    proto_fence = "```markdown\n" + ("noi dung trong fence " * 100) + "\n```\n"
    r = _repo_gia(c.tmp, SACH, ten="proto_fence", protocol=proto_fence)
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(2, rc, e, "PROTOCOL_DA_PHIEN.md chỉ có fence phải ĐỎ (rc=2)")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {_txt(e)!r}")



def case_doctrine_scan_adr_0048_khong_phai_chep_protocol(c: Ctx):
    """A1 — Đoạn trần ADR-0048 không thuộc PROTOCOL_DA_PHIEN.md ⇒ phải XANH (rc=0)."""
    adr_48 = ROOT / "docs" / "adr" / "0048-tran-vong-review-len-muoi.md"
    raw = adr_48.read_text(encoding="utf-8")
    doan_adr = "\n".join(
        l for l in raw.splitlines() if not l.startswith(">") and "PROTOCOL" not in l
    )[:400]
    r = _repo_gia(c.tmp, f"# Adapter\n\n{doan_adr}\n", ten="adr_48")
    rc, o, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(0, rc, e, "đoạn trần ADR-0048 không phải chép protocol nên phải XANH (rc=0)")


def case_doctrine_scan_con_tro_thuan_tuy_xanh(c: Ctx):
    """A4 — Con trỏ thuần tuý nhắc §3.2, §8, assurance_target, reviewed_sha ⇒ phải XANH (rc=0)."""
    nd = (
        "# Adapter chuẩn\n\n"
        "Đọc trước: `docs/PROTOCOL_DA_PHIEN.md` §3.2 và §8.\n"
        "Quy định về assurance_target và reviewed_sha xem tại protocol.\n"
        "Mọi hành vi tuân thủ stop condition tại §12.\n"
    )
    r = _repo_gia(c.tmp, nd, ten="con_tro")
    rc, o, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(0, rc, e, "con trỏ thuần tuý phải XANH (rc=0)")


# --- (d) stdout an toàn dưới codepage không UTF-8 ------------------------------


def _han_tuong_lai(gio: int = 4) -> str:
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


# Lệnh con KHÔNG có đường thành công in stdout — khai TƯỜNG MINH kèm lý do.
LENH_KHONG_CO_STDOUT = {
    "guard": "luôn thoát 7 và chỉ in stderr — không có đường thành công để đo",
}


def _lenh_con_tu_parser(script: Path) -> list:
    """Danh sách lệnh con lấy từ CHÍNH `build_parser()`, không liệt kê tay.

    Finding `ac14-codepage-void-attempt-uncovered` (cross-review lượt 6): ma trận
    codepage của generation 4 liệt kê tay và bỏ sót `void-attempt`, dù lệnh đó in
    stdout tiếng Việt lúc thành công. Liệt kê tay thì thêm một lệnh con mới là mất
    phủ mà KHÔNG AI BIẾT — bộ test im lặng đúng chỗ đáng ra nó phải kêu.
    """
    import importlib.util
    spec = importlib.util.spec_from_file_location("pl_parser", script)
    m = importlib.util.module_from_spec(spec)
    sys.path.insert(0, str(script.parent))
    try:
        spec.loader.exec_module(m)
    finally:
        sys.path.pop(0)
    p = m.build_parser()
    for a in p._actions:
        ch = getattr(a, "choices", None)
        if ch and hasattr(next(iter(ch.values())), "parse_args"):
            return sorted(ch)
    raise AssertionError("không tìm được subparser trong build_parser()")


def _kich_ban_in(c: Ctx, codepage: str):
    """Chạy MỌI lệnh in tiếng Việt với stdout BỊ CAPTURE và encoding ép về codepage."""
    env = {"PYTHONIOENCODING": codepage}
    sd = c.sd()
    r = _repo_gia(c.tmp, SACH, ten=f"cp{codepage}")
    # `adr-song` in tiếng Việt lúc THÀNH CÔNG (`sạch — N ADR trên đĩa…`), nên nó
    # thuộc kịch bản này. Chốt PHỦ ở cuối hàm đã bắt đúng chỗ này khi lệnh vừa
    # được thêm — ma trận lấy danh sách từ `build_parser()` chứ không kê tay.
    r_adr = _repo_adr_gia(c.tmp, [("0001", True)], ["0001"], f"cp{codepage}")
    # `bien-nhan` in tiếng Việt lúc THÀNH CÔNG ("N biên nhận `role: reviewer` trên …"),
    # nên nó THUỘC kịch bản này. Cần một kho giả CÓ biên nhận reviewer, vì đường thất bại
    # chỉ in stderr — đo đường ấy là đo nhầm chỗ.
    r_bn = c.tmp / f"cp{codepage}-bien-nhan"
    (r_bn / ".git").mkdir(parents=True, exist_ok=True)
    (r_bn / "ops" / "reviews").mkdir(parents=True, exist_ok=True)
    (r_bn / "ops" / "reviews" / "a-verdict.receipt.yaml").write_text(
        _BN_REVIEWER, encoding="utf-8")
    # `_BN_REVIEWER` trỏ `verdict_path: ops/reviews/v.md` — thiếu tệp ấy thì biên nhận thành
    # MỒ CÔI và lệnh trả rc=11, tức kịch bản codepage sẽ đo nhầm ĐƯỜNG THẤT BẠI (chỉ in stderr)
    # thay vì đường thành công. Chốt PHỦ ở cuối hàm bắt đúng chuyện này khi phép mồ côi vừa thêm.
    (r_bn / "ops" / "reviews" / "v.md").write_text("verdict\n", encoding="utf-8")
    # #770: `kiem-gate` in "gate XANH trên …" lúc THÀNH CÔNG — chốt PHỦ dưới đã bắt nó.
    cr = c.tmp / f"cp{codepage}-check-runs.json"
    cr.write_text(json.dumps({"total_count": 1, "check_runs": [_kg_run(1, name="cổng-đủ")]}), encoding="utf-8")

    buoc = [
        (["where"], None),
        (["init", "--packet", 55, "--mission", 54,
          "--executor", EXECUTOR, "--reviewer", REVIEWER], sd),
        # `record-lease` cũng in tiếng Việt nên nó THUỘC kịch bản này, không phải
        # chỉ là bước dọn đường: bỏ nó ra là mất luôn phép đo codepage cho một lệnh.
        (["record-lease", "--packet", 55, "--lease-id", "wp55-cp-test",
          "--granted-by", "ducthangho",
          "--evidence", "https://github.com/o/r/issues/55#issuecomment-1",
          "--expires-utc", _han_tuong_lai()], sd),
        (["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd),
        (["chup-anh-doctor", "--packet", 55, "--out", c.tmp / f"doctor-{codepage}.json"], sd),
        (["next-comment", "--packet", 55], sd),
        (["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000009"], sd),
        (["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000009",
          "--head-sha", "%040x" % 1], sd),
        # `void-attempt` in tiếng Việt lúc THÀNH CÔNG — lệnh generation 4 bỏ sót.
        # Đặt TRƯỚC `record-review`: một lượt đã có review thì không hoàn được nữa
        # (chốt `void_sau_review_bi_chan`), nên đặt sau sẽ đo nhầm đường thất bại.
        (["void-attempt", "--packet", 55, "--reason", "quota", *VOID_DUYET], sd),
        # Mở lại lượt: đồng thời là phép đo chiều bắt-oan của
        # `void-reviewing-accepts-attempt-zero` — void xong phải chạy tiếp được.
        (["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd),
        (["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000019"], sd),
        (["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000019",
          "--head-sha", "%040x" % 2], sd),
        (["record-codex-call", "--packet", 55, "--head", "%040x" % 2, "--run-id", "cp-1"], sd),
        (["record-review", "--packet", 55, "--provider", REVIEWER, "--verdict", "changes_requested",
          "--reviewed-sha", "%040x" % 2, "--codex-call", "cp-1",
          "--finding-id", "loi-co-dau-tieng-viet", "--finding-desc", "mô tả có dấu tiếng Việt"], sd),
        (["status", "--packet", 55], sd),
        (["doctrine-scan", "--root", r], None),
        (["adr-song", "--root", r_adr], None),
        (["bien-nhan", "--root", r_bn, "--packet", "249"], None),
        (["kiem-gate", "--head", _KG_HEAD, "--check-runs", cr, "--bat-buoc", "cổng-đủ",
          "--check-suite", _KG_SUITE], None),
        # #338: cả hai lệnh in tiếng Việt CÓ DẤU lúc thành công. `ghi-uy-quyen` in "đã ghi
        # KHAI BÁO…", `doi-chieu-uy-quyen` in "CÓ khai báo"/"KHÔNG khai báo". Console máy
        # Việt là cp1258, nên thiếu phủ ở đây là để nguyên đúng cái bẫy mà chốt này sinh ra
        # để chặn — và chính chốt ấy đã bắt tôi ở lượt đầu (270/272).
        (["ghi-uy-quyen", "--action", "merge", "--nguoi-cap", "ducthangho",
          "--bang-chung", "https://x", "--head-sha", "%040x" % 3], sd),
        # `--root ROOT`: kho THAT, vi lenh nay doc lich su git that su. `_repo_gia` chi
        # co `.git` GIA nen `git log` se hong va ca se do vi ly do sai. Lenh chi DOC.
        (["doi-chieu-uy-quyen", "--root", str(ROOT), "--nhanh", "HEAD",
          "--since", "%040x" % 0 if False else "HEAD~1",
          "--so", str(sd / "uy_quyen_merge.jsonl")], sd),
    ]
    rc, _, e, _, o = _r834(c, env=env)  # #812 lease ref → review có biên nhận, rồi #834 `accept`: đều in tiếng Việt; rc khác 0 ⇒ ĐỎ
    if rc or not o.strip():
        raise AssertionError(f"[{codepage}] chuỗi r812 lease → review → accept phải rc=0 và có stdout, được rc={rc}; stderr={_txt(e)!r}")
    sd_r = _reviewing(c, "--codex-review-calls-limit", 1)  # #775: rescue cần state đã chạm trần, dựng ngoài kịch bản
    _pl(c, sd_r, _goi("r1", _H1), _goi("r2", _H1, 3))
    buoc += [([b[1], "--packet", 55, *b[2:]], sd_r) for b in (_nang(0, tran=2), _rescue(0, "nang_tran"))]
    da_phu = {"accept"}
    for args, state_dir in buoc:
        rc, o, e = run(c.script, args, state_dir, env_extra=env)
        ten = args[0]
        da_phu.add(ten)
        if rc != 0:
            raise AssertionError(
                f"[{codepage}] lệnh {ten!r} phải rc=0 khi stdout bị capture, được rc={rc}; "
                f"stderr={_txt(e)!r}"
            )
        if not o.strip():
            raise AssertionError(f"[{codepage}] lệnh {ten!r} rc=0 nhưng stdout RỖNG")

    # CHỐT PHỦ: mọi lệnh con của parser phải nằm trong kịch bản, hoặc được khai
    # tường minh là không có stdout. Không có chốt này thì thêm lệnh con mới là mất
    # phủ trong im lặng — đúng cách `void-attempt` lọt qua generation 4.
    tat_ca = _lenh_con_tu_parser(c.script)
    thieu = [x for x in tat_ca if x not in da_phu and x not in LENH_KHONG_CO_STDOUT]
    if thieu:
        raise AssertionError(
            f"[{codepage}] ma trận codepage THIẾU PHỦ lệnh con {thieu} — thêm vào kịch "
            f"bản, hoặc khai trong LENH_KHONG_CO_STDOUT kèm lý do")
    thua = [x for x in LENH_KHONG_CO_STDOUT if x not in tat_ca]
    if thua:
        raise AssertionError(
            f"LENH_KHONG_CO_STDOUT khai {thua} nhưng parser không có lệnh ấy — "
            f"danh sách miễn trừ đã trôi khỏi thực tế")


def case_stdout_cp1252(c: Ctx):
    _kich_ban_in(c, "cp1252")


def case_stdout_cp1258(c: Ctx):
    _kich_ban_in(c, "cp1258")


# --- (e) cross-review có cú pháp ghi verdict lên PR ----------------------------


def case_cross_review_co_cu_phap_ghi_verdict_len_pr(c: Ctx):
    f = ROOT / ".claude" / "skills" / "cross-review" / "SKILL.md"
    if not f.is_file():
        raise AssertionError(f"thiếu adapter {f}")
    txt = f.read_text(encoding="utf-8")
    if "gh pr " not in txt:
        raise AssertionError(
            "cross-review phải có cú pháp TƯỜNG MINH ghi verdict lên PR "
            "(vòng review 3 đo được adapter nhận đối số PR mà không có đường ghi nào)"
        )


def case_land_packets_khong_tu_trigger(c: Ctx):
    f = ROOT / ".claude" / "skills" / "land-packets" / "SKILL.md"
    if not f.is_file():
        raise AssertionError(f"thiếu adapter {f}")
    if "disable-model-invocation: true" not in f.read_text(encoding="utf-8"):
        raise AssertionError("land-packets phải khai disable-model-invocation: true")


# --- (f) lease: init KHÔNG được tự cấp -----------------------------------------
#
# Do review cross-provider (codex, 14-08-2026) tìm ra, mức CHẶN: `init` ghi thẳng
# state `leased` mà không đòi bất kỳ uỷ quyền nào, nên executor gõ
# `init --packet 999999 ...` là có ngay một "lease" hợp lệ rồi `begin-attempt`
# sang `running`. Đó là đường vòng qua chính doctrine "không tự cấp lease", mà
# acceptance #55 r2 lại đòi chặn TỪ `init`.
#
# Chốt gồm ba lớp, mỗi lớp một ca đỏ riêng:
#   1. `init` chỉ đưa packet tới `awaiting_lease` — chưa mở được lượt.
#   2. `record-lease` từ chối người cấp mang tên một PROVIDER (agent tự cấp cho mình).
#   3. Hạn lease được cưỡng chế CẢ lúc ghi LẪN lúc mở lượt. Lớp 3 sinh ra từ một ca
#      thật: một lượt review đã chạy 7 GIỜ SAU khi lease hết hạn mà không gì chặn.


def case_init_KHONG_duoc_tu_cap_lease(c: Ctx):
    """Ca tái hiện đúng finding của reviewer."""
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    tt = c.state(sd, 55)
    if tt != "awaiting_lease":
        raise AssertionError(f"init tự cấp lease: state={tt!r}, phải là 'awaiting_lease'")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(8, rc, e, "mở được lượt khi CHƯA có lease")


def case_tu_cap_lease_bang_ten_provider_bi_chan(c: Ctx):
    """Chặn ĐÚNG bởi chốt PROVIDERS (thông điệp gọi tên bệnh), không phải tình cờ
    bị chốt allow-list phía sau vớt lại — cùng input, hai chốt độc lập, phải kiểm
    được TỪNG chốt riêng (xem `case_lease_authority_ten_gia_mao_bi_chan` cho chốt
    allow-list)."""
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    rc, _, e = c.cap_lease(sd, 55, granted_by=EXECUTOR)
    _doi(7, rc, e, "agent tự cấp lease cho chính mình mà không bị chặn")
    if "tên một provider" not in _txt(e):
        raise AssertionError(
            f"rc=7 nhưng KHÔNG phải do chốt PROVIDERS (thông điệp phải nêu 'tên một "
            f"provider'), có thể chốt allow-list phía sau đã vớt oan: {_txt(e)!r}")


def case_lease_authority_ten_gia_mao_bi_chan(c: Ctx):
    """`lease-authority-spoof` P1 — cross-review lượt 4 (codex, 14-08-2026).

    Danh sách CẤM cũ chỉ từ chối đúng hai chuỗi `claude`/`codex`, nên bốn tên dưới
    đây — nguyên văn ca reviewer tái lập được, cộng thêm dạng tổ hợp dấu — đều
    `rc=0` trên bản trước. Nguyên văn kết luận: *"distinguishes spelling, not
    authority"*. Cả `cödex` dựng sẵn (NFC, `U+00F6`) lẫn dạng tổ hợp
    (`o` + `U+0308`, NFD) đều phải bị chặn — cùng một cái tên, hai cách mã hoá.
    """
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    ten_gia_mao = [
        "codex-dispatcher",
        "ai-codex-bot",
        "cödex",     # cödex dựng sẵn (NFC)
        "cödex",    # o + combining diaeresis (NFD) — cùng cái tên, khác mã hoá
    ]
    for ten in ten_gia_mao:
        rc, _, e = c.cap_lease(sd, 55, granted_by=ten)
        _doi(7, rc, e, f"granted_by={ten!r} LỌT qua chốt thẩm quyền")


def case_lease_authority_nguoi_co_tham_quyen_thi_qua(c: Ctx):
    """Chiều DƯƠNG: danh sách cho phép chặn được kẻ gian mà không chặn oan."""
    for ten in ("ducthangho", "Ducthangho", "  DUCTHANGHO  "):
        sd = c.sd()
        rc, _, e = c.init(sd, lease=False)
        _doi(0, rc, e, "init")
        rc, _, e = c.cap_lease(sd, 55, granted_by=ten)
        _doi(0, rc, e, f"chặn oan người có thẩm quyền {ten!r}")


def case_lease_da_het_han_khong_ghi_duoc(c: Ctx):
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    rc, _, e = c.cap_lease(sd, 55, expires="2020-01-01T00:00:00Z")
    _doi(8, rc, e, "ghi được một lease đã hết hạn")


def case_lease_hop_le_thi_mo_duoc_luot(c: Ctx):
    """Chốt phải XANH được, không thì người ta gỡ nó ra."""
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    rc, _, e = c.cap_lease(sd, 55)
    _doi(0, rc, e, "lease hợp lệ mà bị chặn")
    tt = c.state(sd, 55)
    if tt != "leased":
        raise AssertionError(f"lease hợp lệ nhưng state={tt!r}")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "lease hợp lệ mà không mở được lượt")


def case_begin_attempt_sau_khi_lease_HET_HAN_bi_chan(c: Ctx):
    """Lease hết hạn giữa chừng thì lượt sau KHÔNG được mở."""
    import time
    from datetime import datetime, timedelta, timezone

    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    han = (datetime.now(timezone.utc) + timedelta(seconds=2)).strftime("%Y-%m-%dT%H:%M:%SZ")
    rc, _, e = c.cap_lease(sd, 55, expires=han)
    _doi(0, rc, e, "lease còn 2 giây mà bị từ chối ngay lúc ghi")
    time.sleep(3)
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(8, rc, e, "mở được lượt bằng một lease ĐÃ HẾT HẠN")


def _script_tu_git(tmp: Path, sha: str, ten: str) -> Path:
    """Vật chất hoá `packet_loop.py` ở một SHA lịch sử thành TỆP THẬT.

    Chạy được bằng `run()` giống hệt CANONICAL, không mô phỏng state bằng tay —
    fixture phải đi qua ĐÚNG entrypoint cũ để chứng minh bug là ở HÀNH VI, không
    phải ở một JSON tự bịa ra giống bug.

    Đòi lịch sử KHÔNG shallow (cùng điều kiện mà `work-packet/SKILL.md` đòi trước
    khi tin bất kỳ phép so lịch sử nào): thiếu commit thì báo lỗi rõ, không im lặng
    bỏ qua ca.
    """
    p = subprocess.run(["git", "show", f"{sha}:.claude/dev/packet_loop.py"],
                        cwd=ROOT, capture_output=True)
    if p.returncode != 0:
        raise AssertionError(
            f"không đọc được packet_loop.py tại {sha} — lịch sử git thiếu commit này "
            f"(clone shallow?): {_txt(p.stderr)!r}")
    f = tmp / ten
    f.write_bytes(p.stdout)
    return f


def case_g9_lease_khoa_thua_bi_chan(c: Ctx):
    """`lease-schema-allows-extra-keys` P2 — cross-review lượt 9.

    `_kiem_luoc_do_lease` kiểm THIẾU khoá nhưng không kiểm THỪA. Nên một state có đủ
    bốn khoá cộng `unexpected: true` vẫn mở được lượt (`rc=0`) — lặp lại ĐÚNG tiêu chí
    mà AC 21 đặt ra để bắt bệnh cũ: `begin-attempt` nhận một state mà `record-lease`
    KHÔNG BAO GIỜ sinh ra được, vì nó chỉ dựng đúng bốn khoá ấy.

    Ca đi qua ĐƯỜNG HỢP LỆ trước rồi mới nhét khoá lạ vào state — để đo đúng chốt lược
    đồ, không đo nhầm chốt thẩm quyền hay chốt hạn.
    """
    import json as _json
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    rc, _, e = c.cap_lease(sd, 55)
    _doi(0, rc, e, "lease hợp lệ mà bị chặn")
    p_state = Path(sd) / "wp55.json"
    tt = _json.loads(p_state.read_text(encoding="utf-8"))
    tt["lease"]["unexpected"] = True
    p_state.write_text(_json.dumps(tt), encoding="utf-8")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(8, rc, e, "begin-attempt nhận lease có khoá THỪA mà không chặn")


def case_legacy_state_khong_co_lease_bi_chan(c: Ctx):
    """`legacy-lease-bypass` P1 — cross-review lượt 4 (codex, 14-08-2026).

    State do ĐÚNG entrypoint TRƯỚC (`22d2cc9`) sinh ra có `state: leased` mà
    KHÔNG có trường `lease` — bản đó ghi thẳng `leased` trong `init`, chưa có khái
    niệm ghi hộ lease riêng. Bản MỚI trước khi vá nhận state đó thẳng vào
    `running` (`begin-attempt` fail-open khi thiếu `lease`) mà chưa từng đi qua
    `record-lease` — mâu thuẫn trực tiếp với bất biến "leased chỉ tới được qua
    record-lease" (xem `CHUYEN_HOP_LE`).
    """
    sd = c.sd()
    legacy = _script_tu_git(c.tmp, "22d2cc9", "packet_loop_22d2cc9.py")
    rc, _, e = run(legacy, ["init", "--packet", 55, "--mission", 54,
                            "--executor", EXECUTOR, "--reviewer", REVIEWER], sd)
    _doi(0, rc, e, "init (entrypoint cũ 22d2cc9)")
    tt = c.state(sd, 55)
    if tt != "leased":
        raise AssertionError(f"fixture không đúng dạng bug gốc: state={tt!r}, phải là 'leased'")
    p_state = Path(sd) / "wp55.json"
    du_lieu = json.loads(p_state.read_text(encoding="utf-8"))
    du_lieu["hmac_key"] = "0" * 64  # cô lập ca này: chỉ thiếu lease, không thiếu khoá mới
    p_state.write_text(json.dumps(du_lieu), encoding="utf-8")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(8, rc, e, "begin-attempt (bản MỚI) nhận state cũ KHÔNG có 'lease' mà không chặn")


# --- (g) doctrine-scan phải bắt cả dạng RENDER RA đúng cụm cấm ------------------


def case_doctrine_scan_bat_zero_width_bi_chan(c: Ctx):
    """`doctrine-rendering-bypass` P1 — cross-review lượt 4 (codex, 14-08-2026).

    `mer<ZWSP>ged: PR đã vào nhánh đích` RENDER RA đúng cụm doctrine bị cấm (ký
    tự zero-width không hiển thị), nhưng bản chuẩn hoá trước chỉ xử lý trang trí
    Markdown + khoảng trắng, không xử lý ký tự định dạng Unicode (`Cf`) — nên nó
    lọt (`rc=0`) trên bản cũ.
    """
    r = _repo_gia(c.tmp, SACH + "\nGhi chú: mer​ged: PR đã vào nhánh đích\n",
                  ten="render-zwsp")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "zero-width-space LỌT doctrine-scan dù render ra đúng cụm cấm")


def case_doctrine_scan_bat_html_entity_bi_chan(c: Ctx):
    """`doctrine-rendering-bypass` P1 — cùng finding, dạng HTML entity.

    `merged&#58; ...` RENDER RA `merged: ...` trong Markdown/HTML, nhưng bản
    chuẩn hoá trước không giải entity — nên nó lọt (`rc=0`) trên bản cũ.
    """
    r = _repo_gia(c.tmp, SACH + "\nGhi chú: merged&#58; PR đã vào nhánh đích\n",
                  ten="render-entity")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "HTML entity LỌT doctrine-scan dù render ra đúng cụm cấm")


def case_doctrine_scan_khong_giai_entity_lap(c: Ctx):
    """An toàn: giải entity MỘT LẦN, không lặp tới điểm bất động.

    `&amp;#58;` hiển thị NGUYÊN VĂN `&#58;` trong Markdown/HTML — KHÔNG phải dấu
    hai chấm. Giải LẶP sẽ biến nó thành `:` và sinh DƯƠNG TÍNH GIẢ trên cụm
    `merged: ...`. `rc=0` Ở ĐÂY LÀ ĐÚNG — đây không phải chỗ để bắt lỗi.
    """
    r = _repo_gia(c.tmp, SACH + "\nGhi chú: merged&amp;#58; PR đã vào nhánh đích\n",
                  ten="entity-kep")
    rc, o, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(0, rc, e, "giải entity LẶP sinh dương tính giả trên merged&amp;#58;")


# --- (h) AC 18 · DANH SÁCH ĐÓNG các lớp lách -----------------------------------
#
# VÌ SAO LÀ DANH SÁCH, KHÔNG PHẢI VÀI CA LẺ: `doctrine-scan` đã thua NĂM vòng
# liên tiếp, mỗi vòng đúng một hình dạng ký tự mới, và mỗi lần vá xong lại lộ
# hình dạng kế tiếp. Bảng dưới đây là DANH SÁCH ĐÓNG đã đo trên bản CHƯA VÁ:
# 40 ca, 18 LỌT. Mỗi lớp một ca, mỗi lớp một đột biến giết đúng ca đó (xem
# MUTANTS) — đó là điều kiện để tin rằng ca đang đo đúng lớp nó khai.

def _ca_doctrine(noi_dung: str, ten: str, doi: int = 6):
    """Dựng một ca doctrine-scan: bơm `noi_dung` vào adapter, đòi đúng `doi`."""
    def f(c: Ctx):
        r = _repo_gia(c.tmp, SACH + "\n" + noi_dung + "\n", ten=ten)
        rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
        _doi(doi, rc, e, f"lớp {ten!r}")
    return f


# Chiều LỌT — mỗi dòng RENDER RA đúng một cụm doctrine bị cấm.
LOP_LACH = [
    # A · NFKC vs NFC — NFC theo ĐỊNH NGHĨA không gộp ký tự tương thích.
    ("nfkc_hai_cham_toan_rong", "Ghi chú: merged： PR đã vào nhánh đích"),
    ("nfkc_chu_toan_rong", "Ghi chú: ｍｅｒｇｅｄ： PR đã vào nhánh đích"),
    ("nfkc_chu_so_tron", "Ghi chú: ③ attempt/packet"),
    ("nfkc_chu_so_mu", "Ghi chú: ³ attempt/packet"),
    ("nfkc_ligature_ff", "Ghi chú: sửa đúng eﬀective write set trên branch của generation"),
    ("nfkc_solidus_toan_rong", "Ghi chú: dispatcher／reconciler"),
    ("nfkc_gach_duoi_toan_rong", "Ghi chú: same＿failure＿limit"),
    ("nfkc_vach_dung_toan_rong", "Ghi chú: paused ｜ blocked ｜ cancelled ｜ stale"),
    # phân cách: NBSP, en-dash, hyphen phải quy về cùng mối với khoảng trắng / `_`.
    # NBSP được PHỦ HAI LỚP — NFKC đã gộp `U+00A0` về khoảng trắng, và phép gộp
    # phân cách cũng gộp nó. Nên KHÔNG đột biến đơn lẻ nào giết được ca này, và
    # nó cố ý không nằm trong danh sách phải-chết của mutant nào: nói thẳng chỗ
    # phủ chồng còn hơn gán bừa cho một lớp rồi tưởng đã đo được lớp ấy.
    # U+00A0 viết bằng ESCAPE chứ không phải ký tự trần. Ký tự trần trông hệt khoảng
    # trắng thường trong mọi trình soạn thảo, nên một lần sửa dòng bên cạnh là gõ đè
    # mất mà không ai thấy — ca sẽ lặng lẽ thôi đo lớp nó khai. Escape thì hỏng ồn ào.
    #
    # Tên lớp đổi `phu_hai_lop` → `phu_ba_lop` vì lời khai cũ SAI. Dựng đột biến đúng
    # hai vế mà lời khai nêu (NFKC + `_PHAN_CACH`) thì ca VẪN XANH, và đường thứ ba
    # lộ ra: `str.split()` không đối số tách theo khoảng trắng UNICODE, nên dòng cuối
    # `_chuan_hoa` cũng nuốt U+00A0. Đây đúng là thứ ngoại lệ `PHU_NHIEU_LOP` che
    # mất — nó GHI NHẬN lời khai "hai đường phủ" mà không bao giờ KIỂM, nên lời khai
    # sai sống sót. Đòi có đột biến thì lời khai sai chết ngay lượt đầu.
    ("nbsp_phu_ba_lop", "Ghi chú: local\u00a0controller"),
    ("phan_cach_en_dash", "Ghi chú: same–failure–limit"),
    ("phan_cach_hyphen", "Ghi chú: same-failure-limit"),
    # B · ký tự định dạng `Cf` — không hiển thị nhưng cắt được chuỗi khớp.
    ("cf_zwnj", "Ghi chú: mer‌ged: PR đã vào nhánh đích"),
    ("cf_zwj", "Ghi chú: mer‍ged: PR đã vào nhánh đích"),
    ("cf_word_joiner", "Ghi chú: mer⁠ged: PR đã vào nhánh đích"),
    ("cf_soft_hyphen", "Ghi chú: mer­ged: PR đã vào nhánh đích"),
    ("cf_bom", "Ghi chú: mer﻿ged: PR đã vào nhánh đích"),
    # C · HTML entity — bốn cách viết, cùng một dấu hai chấm.
    ("entity_thap_luc", "Ghi chú: merged&#x3A; PR đã vào nhánh đích"),
    ("entity_co_ten", "Ghi chú: merged&colon; PR đã vào nhánh đích"),
    ("entity_thieu_cham_phay", "Ghi chú: merged&#58 PR đã vào nhánh đích"),
    # D · đồng tự Cyrillic / Hy Lạp — NFKC KHÔNG gộp những chữ này.
    ("dong_tu_cyrillic_e", "Ghi chú: mеrged: PR đã vào nhánh đích"),
    ("dong_tu_cyrillic_o", "Ghi chú: lоcal controller"),
    ("dong_tu_hy_lap_o", "Ghi chú: lοcal controller"),
    ("dong_tu_cyrillic_a", "Ghi chú: pаused | blocked | cancelled | stale"),
    # E · nháy cong xen giữa từ.
    ("nhay_cong_xen_giua", "Ghi chú: mer’ged: PR đã vào nhánh đích"),
    # F · biến thể mũi tên.
    ("mui_ten_dai", "Ghi chú: proposed ⟶ ready ⟶ leased ⟶ running ⟶ reviewing "
                    "⟶ accepted ⟶ integrated ⟶ landed"),
    # G · cấu trúc Markdown / HTML — thứ RENDER RA cụm cấm.
    ("tag_html_xen_giua", "Ghi chú: mer<b>ged</b>: PR đã vào nhánh đích"),
    ("comment_html_xen_giua", "Ghi chú: mer<!-- x -->ged: PR đã vào nhánh đích"),
    ("link_markdown", "Ghi chú: [merged](#a): PR đã vào nhánh đích"),
    ("backslash_escape", "Ghi chú: merged\\: PR đã vào nhánh đích"),
    # --- I · tag/link mà regex của generation 4 xử lý SAI (cross-review lượt 6) ---
    # Bản trước cấm ký tự `>` theo VỊ TRÍ (`[^<>]*`), nên một `>` nằm hợp lệ trong
    # giá trị thuộc tính làm regex không khớp và tag không bị gỡ.
    ("tag_thuoc_tinh_nhay_kep", 'Ghi chú: mer<span title=">">ged:</span> PR đã vào nhánh đích'),
    ("tag_thuoc_tinh_nhay_don", "Ghi chú: mer<span title='>'>ged:</span> PR đã vào nhánh đích"),
    ("tag_thuoc_tinh_dau_nho_hon", 'Ghi chú: mer<span title="<">ged:</span> PR đã vào nhánh đích'),
    # Tag/comment TRẢI NHIỀU DÒNG: `_chuan_hoa` chạy theo từng dòng nên không thấy.
    ("tag_ngat_qua_dong", 'Ghi chú: mer<span\n  class="x">ged: PR đã vào nhánh đích'),
    ("comment_html_ngat_qua_dong", 'Ghi chú: mer<!--\n  ghi chú\n-->ged: PR đã vào nhánh đích'),
    ("link_ngoac_long", "Ghi chú: [merged](#a(b)): PR đã vào nhánh đích"),
    # --- J · cụm ĐỨNG MỘT MÌNH — AC 2 đòi bơm MỘT cụm là phải ĐỎ ------------------
    # Đây là chiều FAIL-OPEN mà bản vá bắt-oan của generation 4 tự mở ra.
    ("cum_don_heading", "## Người có thẩm quyền"),
    ("cum_don_dong_tran", "Người có thẩm quyền"),
    ("cum_don_gach_dau_dong", "- Người có thẩm quyền"),
    ("cum_don_in_dam", "**Người có thẩm quyền**"),
    ("cum_don_dinh_nghia", "Người có thẩm quyền: người cấp lease"),
    # --- K · cụm đứng một mình bị NGẮT DÒNG. Lượt 7 đo được: chỉ cần gõ Enter giữa
    # cụm là qua cổng, vì miễn trừ AC 19 của generation 5 tha MỌI hình dạng ngắt
    # dòng chứ không riêng văn xuôi. Danh sách đóng đo được 18 hình dạng lọt, trong
    # đó reviewer nêu 4; ba ca trích dẫn thì lọt vì lý do KHÁC — xem `cum_don_trich_dan`.
    ("cum_don_heading_ngat_dong", "## Người có\nthẩm quyền"),
    ("cum_don_gach_dau_dong_ngat_dong", "- Người có\n  thẩm quyền"),
    ("cum_don_danh_sach_so_ngat_dong", "1. Người có\n   thẩm quyền"),
    ("cum_don_dong_tran_ngat_dong", "Người có\nthẩm quyền"),
    # Hai ca fence CỐ TÌNH có chữ ở cả hai phía cụm. Nếu để cụm đứng trần trong
    # fence thì chốt VĂN XUÔI đã bắt rồi, và đột biến gỡ chốt KHỐI MÃ sẽ không giết
    # được ca — ca mất độ phân giải, đúng bệnh `ac18-mutation-not-per-class`. Có chữ
    # hai phía thì chỉ còn chốt khối mã đứng giữa, nên nó đo đúng thứ nó khai.
    ("cum_don_code_fence",
     "```\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n```"),
    ("cum_don_code_fence_ngoac_song",
     "~~~\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n~~~"),
    ("cum_don_o_bang_html_ngat_dong",
     "<table><tr><td>Người có\nthẩm quyền</td></tr></table>"),
    # Hàng rào LỒNG MỘT CẤP. Chốt khối mã bản đầu chỉ khớp `^\s{0,3}` nên không nhận
    # ra chúng, và miễn trừ văn xuôi tha luôn cả khối mã. Ca bullet còn dựng ra một
    # hàng rào MA: dòng đóng `  ``` ` thụt 2 dấu cách thì khớp, nên nó MỞ thay vì
    # ĐÓNG. Ba ca đều cố tình có chữ hai phía cụm để chỉ còn chốt khối mã đứng giữa.
    ("cum_don_fence_trong_bullet",
     "- ```\n  Bảng vai trò: người có\n  thẩm quyền là người cấp lease.\n  ```"),
    ("cum_don_fence_trong_trich_dan",
     "> ```\n> Bảng vai trò: người có\n> thẩm quyền là người cấp lease.\n> ```"),
    # LỚP `cum_don_fence_thut_bon_dau_cach` ĐÃ BỎ ở generation 9.
    #
    # Nó sinh ra ở g8 khi `_RE_HANG_RAO` còn khớp `^\\s*`, tức thụt 4 dấu cách vẫn được
    # đọc là hàng rào. Generation 9 trả lại mức thụt CommonMark (`^ {0,3}`) vì lập luận
    # "fail-closed" của g8 đã bị bác, nên thụt 4 dấu cách KHÔNG còn là hàng rào và lớp
    # này thôi đo hàng rào — nó chỉ còn vô tình đỏ nhờ chốt phép đo.
    #
    # RESIDUAL KHAI THẲNG: CommonMark coi khối thụt 4 dấu cách là KHỐI MÃ THỤT LỀ, và
    # packet này KHÔNG cài phép dò ấy. Nên một cụm cấm đặt trong khối mã thụt lề, kèm
    # dấu hiệu phép đo, vẫn được tha. Không cài vì rủi ro BẮT OAN cao: dòng nối tiếp của
    # một mục danh sách thường thụt 4 dấu cách trở lên và là văn xuôi thật. Đánh đổi này
    # để chủ kho/reviewer phán, không tự quyết.
    # Ô bảng HTML CÓ CHỮ HAI PHÍA — cross-review lượt 8. Khác `cum_don_o_bang_html_
    # ngat_dong` ở chỗ ca kia không có chữ bọc nên chốt văn xuôi đã bắt; ca này có,
    # nên chỉ còn chốt BẢNG HTML đứng giữa. Ô bảng là chép bảng, không bao giờ là
    # câu kể lại kết quả đo, nên không được hưởng miễn trừ AC 19.
    ("cum_don_o_bang_html_co_chu_hai_phia",
     "<table><tr><td>Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.</td></tr></table>"),
    ("cum_don_o_bang_html_khong_dong_the",
     "<table><tr><td>Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0."),
    ("cum_don_chi_co_chu_truoc", "Vai trò: người có\nthẩm quyền"),
    ("cum_don_chi_co_chu_sau", "Người có\nthẩm quyền là vai trò."),
    # --- W · wrapper TUỲ Ý (cross-review lượt 9) --------------------------------
    # Chốt g6–g8 chỉ đòi "có ký tự chữ hai phía", nên hai ký tự vô nghĩa là qua cổng.
    # Executor đã HAI LẦN khai đây là "giới hạn đã khai vì cần hiểu NGHĨA"; reviewer bác
    # đúng: không buộc phải tha MỌI wrapper, ca thật neo được vào dấu hiệu phép đo.
    ("cum_don_wrapper_mot_chu_cai", "x người có\nthẩm quyền y"),
    ("cum_don_wrapper_chu_so", "1 người có\nthẩm quyền 2"),
    ("cum_don_wrapper_trong_tag", "<b>x</b> người có\nthẩm quyền <b>y</b>"),
    # Câu văn xuôi thật, có chữ hai phía, nhưng KHÔNG kể lại phép đo nào — nên không
    # nằm trong bề rộng AC 19 tha. Trước là ca bắt-oan `oan_term_ngat_dong`.
    ("cum_don_van_xuoi_khong_ke_phep_do",
     "Quyết định này thuộc về người có\nthẩm quyền, không thuộc phiên này."),
    # --- F · rào đóng SAI LUẬT (cross-review lượt 9) ----------------------------
    ("cum_don_rao_dong_ngan_hon",
     "````\n```\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n````"),
    ("cum_don_rao_dong_co_duoi",
     "```\n``` not-a-close\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n```"),
    ("cum_don_rao_song_dong_ngan_hon",
     "~~~~\n~~~\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.\n~~~~"),
    # --- H · bảng HTML LỒNG (cross-review lượt 9) ------------------------------
    ("cum_don_bang_html_long",
     "<table>\n<tr><td><table></table></td></tr>\n"
     "<tr><td>Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.</td></tr>\n</table>"),
    ("cum_don_bang_html_long_ba_cap",
     "<table>\n<tr><td><table><tr><td><table></table></td></tr></table></td></tr>\n"
     "<tr><td>Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.</td></tr>\n</table>"),
    # Ba ca dưới lọt vì `_chuan_hoa` GIỮ dấu `>`, nên chuỗi phẳng ra
    # `> người có > thẩm quyền` và cụm cấm không khớp một lần nào — scanner KHÔNG
    # THẤY, chứ không phải miễn trừ tha nhầm. Dấu `-` tình cờ bị `_PHAN_CACH` nuốt,
    # `>` `#` `1.` thì không: lỗ tồn tại nhờ đúng sự không nhất quán ấy. Reviewer
    # lượt 7 không nêu họ này; danh sách đóng tìm ra.
    ("cum_don_trich_dan_ngat_dong", "> Người có\n> thẩm quyền"),
    ("cum_don_trich_dan_long_hai_cap", ">> Người có\n>> thẩm quyền"),
    ("cum_don_heading_long_trich_dan", "> ## Người có\n> thẩm quyền"),
    # Trước là ca bắt-oan `oan_term_giua_cau` của generation 4. Chuyển sang đây:
    # AC 2 đòi bơm một cụm trong danh sách là phải ĐỎ, và một adapter viết câu này
    # đang CHÉP nội dung bảng vai trò §2 chứ không TRỎ về protocol. AC 19 chỉ đòi
    # tha câu văn xuôi KỂ LẠI KẾT QUẢ ĐO bị ngắt dòng, không tha mọi câu văn xuôi.
    ("cum_don_cau_van_xuoi_mot_dong",
     "Chỉ người có thẩm quyền mới cấp được lease; phiên worker thì không."),
    # --- MƯỜI HAI CA ĐỔI MA TRẬN ở revision 4 — BẮT-OAN sang LỌT ------------------
    #
    # Cả mười hai TRƯỚC nằm ở `LOP_BAT_OAN`, được miễn trừ AC 19 tha vì cụm cấm bị
    # ngắt qua dòng trong văn xuôi kể lại một phép đo. Revision 4 bỏ hẳn miễn trừ,
    # nên chúng ĐỎ. Đây KHÔNG phải hồi quy — đây là hợp đồng mới, khai thẳng:
    # cụm trong danh sách cấm không được xuất hiện ở BẤT KỲ hình dạng nào, và
    # adapter cần kể lại phép đo có chứa cụm ấy thì VIẾT LẠI CÂU.
    #
    # Spec revision 4 đoán HAI ca sẽ đổi. Đo trọn suite: MƯỜI HAI. Phân hoạch sạch —
    # 12 ca đỏ đúng bằng 12 ca CÓ chứa cụm cấm, 23 ca không chứa vẫn xanh; không ca
    # nào đỏ vì lý do khác. Chênh lệch là do spec mới mô phỏng chứ chưa chạy trọn.
    #
    # Mỗi ca ở đây có một ca CÙNG TÊN GỐC bên `LOP_BAT_OAN` giữ Y HỆT hình dạng
    # (bảng chưa đóng thẻ, rào bốn backtick, dòng thụt lề, mã inline, comment,
    # bullet, danh sách số, trích dẫn) nhưng viết `tên thuộc / danh sách cho phép`.
    # Cặp ấy là thứ chứng minh cổng phân biệt NỘI DUNG chứ không phân biệt HÌNH DẠNG.
    ("cum_don_claude_md_master_tha_cu",
     'biệt THẨM QUYỀN. Danh sách cấm phải đoán trước mọi cách viết của kẻ gian\n  (dấu nối, tiền tố, hậu tố, đồng tự Unicode, tổ hợp dấu) nên thua từ trong\n  thiết kế. Đo ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`, người có\n  thẩm quyền vẫn `rc=0`. Kèm chốt: đột biến nới danh sách phải làm ca đích ĐỎ.'),
    ("cum_don_term_ngat_dong_tha_cu",
     'Đo lại trên bản v1.36.68 thì quyết định vẫn thuộc về người có\nthẩm quyền, và cổng trả rc=0 như cũ.'),
    ("cum_don_van_xuoi_ngat_dong_trong_bullet_tha_cu",
     '- Kết quả đo cho thấy người có\n  thẩm quyền vẫn qua cổng bình thường.'),
    ("cum_don_van_xuoi_ngat_dong_trong_danh_sach_so_tha_cu",
     '1. Bản đo ghi rằng người có\n   thẩm quyền vẫn qua cổng bình thường.'),
    ("cum_don_van_xuoi_ngat_dong_trong_trich_dan_tha_cu",
     '> Bản đo ghi rằng người có\n> thẩm quyền không bị chặn ở bước này.'),
    ("cum_don_van_xuoi_sau_bang_html_tha_cu",
     '<table><tr><td>x</td></tr></table>\n\nĐo được ở `v1.36.68`: ba tên tấn công `rc=0` → `rc=4`, người có\nthẩm quyền vẫn `rc=0`.'),
    ("cum_don_rao_dong_dung_luat_tha_cu",
     '````\nvo hai\n````\n\nĐo được ở v1.36.68: cổng trả rc=0 cho người có\nthẩm quyền như cũ.'),
    ("cum_don_dong_thut_le_khong_phai_rao_tha_cu",
     '    ``` đây chỉ là một dòng code thụt lề\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'),
    ("cum_don_the_bang_trong_khoi_ma_tha_cu",
     '```html\n<table>\n```\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'),
    ("cum_don_the_bang_trong_ma_inline_tha_cu",
     'Ví dụ ký hiệu `<table>` trong tài liệu. Đo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'),
    ("cum_don_the_bang_trong_comment_tha_cu",
     '<!-- <table> -->\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'),
    ("cum_don_van_xuoi_sau_bang_html_chua_dong_tha_cu",
     '<table><tr><td>thời gian</td></tr>\n\nĐo được: ba tên tấn công rc=4, người có\nthẩm quyền vẫn rc=0.'),
]

# Chiều BẮT OAN — AC 19. Mỗi lớp chuẩn hoá thêm ở trên có ít nhất một ca ở đây.
# Chuẩn hoá mạnh hơn mà bắt oan văn bản bình thường là KHÔNG ĐẠT, y như để lọt.
#
# `oan_claude_md_master` là ca THẬT đang làm gate đỏ trên cây ĐÃ MERGE: `CLAUDE.md`
# của master ngắt dòng giữa `người có` / `thẩm quyền` trong một câu KỂ LẠI kết quả
# đo. Câu ấy không chép bảng vai trò §2 — nó tường thuật một phép đo.
LOP_BAT_OAN = [
    ("oan_claude_md_master",
     'biệt DANH SÁCH CHO PHÉP. Danh sách cấm phải đoán trước mọi cách viết của kẻ gian\n  (dấu nối, tiền tố, hậu tố, đồng tự Unicode, tổ hợp dấu) nên thua từ trong\n  thiết kế. Đo ở `v1.36.68` (PR #104): ba tên tấn công `rc=0` → `rc=4`, tên thuộc\n  danh sách cho phép vẫn `rc=0`. Kèm chốt: đột biến nới danh sách phải làm ca đích ĐỎ.'),
    # `oan_term_giua_cau` ĐÃ CHUYỂN sang LOP_LACH (`cum_don_cau_van_xuoi_mot_dong`)
    # — xem lý do ở đó. Giữ lại một ca cùng chỗ nhưng ĐÚNG bề rộng của AC 19:
    # Ca này TRƯỚC ở ma trận BẮT-OAN. Generation 9 chuyển sang ma trận LỌT — xem
    # `cum_don_van_xuoi_khong_ke_phep_do` trong `LOP_LACH`. Thay bằng một ca CÙNG hình
    # dạng (ngắt dòng, văn xuôi, có chữ hai phía) nhưng CÓ kể lại một phép đo, tức đúng
    # bề rộng mà AC 19 tha.
    ("oan_term_ngat_dong",
     'Đo lại trên bản v1.36.68 thì quyết định vẫn thuộc về tên thuộc\ndanh sách cho phép, và cổng trả rc=0 như cũ.'),
    ("oan_entity_long", "Ghi chú: merged&amp;#58; PR đã vào nhánh đích"),
    ("oan_van_ban_nga", "Пример текста на русском языке: локальный контроллер работает."),
    ("oan_van_ban_hy_lap", "Παράδειγμα κειμένου στα ελληνικά για δοκιμή."),
    ("oan_tu_gach_noi", "Quy trình cross-review chạy end-to-end với cấu hình read-only."),
    ("oan_shell_lt_gt", "Chạy: `python tl.py --json` rồi so `a < b > c` trong shell."),
    ("oan_tag_html_vo_hai", "Xem <b>tài liệu</b> và <i>ghi chú</i> ở docs/."),
    ("oan_link_binh_thuong",
     "Đọc [protocol](docs/PROTOCOL_DA_PHIEN.md) và [changelog](CHANGELOG.md)."),
    ("oan_escape_markdown", "Ký tự \\* và \\_ phải escape khi viết Markdown."),
    # Ca này TRƯỚC khai là lớp `Cf` nhưng KHÔNG chứa ký tự Cf nào — nó không đo lớp
    # nó khai (cross-review lượt 6). Nay có ZWSP thật giữa câu tiếng Việt vô hại.
    ("oan_tieng_viet_du_dau",
     "Điều 5 quy định: người sử dụng​ lao động phải trả lương đúng hạn."),
    ("oan_dau_cau_toan_rong", "Trích nguồn CJK：文書の内容はここにあります。"),
    ("oan_bang_khac", "| cột | giá trị |\n|---|---|\n| thời gian | 5 phút |"),
    # --- ca bắt-oan cho các chốt generation 4 thêm mà chưa có ca (AC 19) ---------
    ("oan_nhay_cong_van_xuoi",
     "Tác giả viết “đúng” và ‘chưa đúng’ để phân biệt hai mức."),
    ("oan_mui_ten_van_xuoi",
     "Luồng xử lý: đọc ⟶ kiểm ⟶ ghi, không liên quan state machine."),
    ("oan_comment_html_vo_hai",
     "Đoạn này <!-- ghi chú của người soạn --> vẫn là văn bản bình thường."),
    ("oan_to_hop_dau_tieng_viet",
     "Chuỗi tổ hợp: cà phê, tiếng Việt, nhân viên — không có cụm cấm nào."),
    # --- ca bắt-oan cho các chốt MỚI của generation 5 ----------------------------
    ("oan_tag_thuoc_tinh_vo_hai",
     'Xem <a href="https://x/y?a=1&b=2" title="Ghi chú">tài liệu</a> ở docs/.'),
    ("oan_tag_ngat_dong_vo_hai",
     'Thẻ nhiều dòng vô hại: <a\n  href="/x">tài liệu</a> — không có cụm cấm.'),
    ("oan_link_ngoac_long_vo_hai",
     "Đọc [ghi chú](docs/a(b).md) và [khác](docs/c.md) — đều vô hại."),
    ("oan_shell_chuyen_huong",
     "Chạy `a < b.txt > c.txt` rồi so `x <= y` — không phải tag HTML."),
    # --- ca bắt-oan cho họ K của generation 6 ------------------------------------
    # Bản vá lượt 7 thu miễn trừ về "văn xuôi BỌC HAI PHÍA và không nằm trong khối
    # mã". Bốn ca dưới là chiều ngược của đúng chốt ấy: cùng bị ngắt dòng, cùng nằm
    # trong bullet/danh sách/trích dẫn, nhưng CÓ chữ ở cả hai phía ⇒ vẫn phải tha.
    # Thu miễn trừ quá tay thì chính bốn ca này đỏ lên.
    ("oan_van_xuoi_ngat_dong_trong_bullet",
     '- Kết quả đo cho thấy tên thuộc\n  danh sách cho phép vẫn qua cổng bình thường.'),
    ("oan_van_xuoi_ngat_dong_trong_danh_sach_so",
     '1. Bản đo ghi rằng tên thuộc\n   danh sách cho phép vẫn qua cổng bình thường.'),
    ("oan_van_xuoi_ngat_dong_trong_trich_dan",
     '> Bản đo ghi rằng tên thuộc\n> danh sách cho phép không bị chặn ở bước này.'),
    # Khối mã bị LOẠI khỏi miễn trừ. Chốt ấy không được biến mọi khối mã thành vi
    # phạm: khối mã KHÔNG chứa cụm cấm vẫn phải xanh.
    ("oan_code_fence_vo_hai",
     "```\nchay: python tl.py --json\nket qua: rc=0\n```"),
    # Nới chốt hàng rào để nhận rào lồng cấp thì phải KHÔNG được biến mọi dấu đầu
    # dòng thành hàng rào. Ca này có bullet, trích dẫn, đường kẻ ngang `---` và một
    # dòng chú thích shell mở đầu bằng `#` NGAY TRONG khối mã — `_go_dau_dong_tho`
    # cố ý không gỡ `#` chính vì dòng ấy.
    # Chốt bảng HTML không được biến MỌI bảng thành vi phạm: bảng không chứa cụm cấm
    # vẫn phải xanh.
    ("oan_bang_html_vo_hai",
     "<table><tr><td>thời gian</td><td>5 phút</td></tr></table>"),
    # Và không được lan RA NGOÀI thẻ đóng: câu văn xuôi kể kết quả đo đứng SAU bảng
    # vẫn phải được tha theo AC 19.
    ("oan_van_xuoi_sau_bang_html",
     '<table><tr><td>x</td></tr></table>\n\nĐo được ở `v1.36.68`: ba tên tấn công `rc=0` → `rc=4`, tên thuộc\ndanh sách cho phép vẫn `rc=0`.'),
    # Rào đóng ĐÚNG LUẬT vẫn phải đóng được — siết luật rào không được biến mọi khối
    # mã bình thường thành khối không bao giờ đóng.
    ("oan_rao_dong_dung_luat",
     '````\nvo hai\n````\n\nĐo được ở v1.36.68: cổng trả rc=0 cho tên thuộc\ndanh sách cho phép như cũ.'),
    # Bảng lồng HỢP LỆ, không chứa cụm cấm — đếm lồng nhau không được bắt oan nó.
    ("oan_bang_html_long_vo_hai",
     "<table><tr><td><table><tr><td>5 phút</td></tr></table></td></tr></table>"),
    # --- CHỐNG ĐẦU ĐỘC ĐUÔI TỆP (finding P1 thứ tư, lượt 9) ---------------------
    # g8 nới `_RE_HANG_RAO` về `^\s*` rồi biện minh "fail-closed". Reviewer bác: AC 19
    # nói bắt oan văn bản bình thường là KHÔNG ĐẠT, ngang với để lọt. Ba ca dưới đo
    # đúng chiều ấy — một cấu trúc VÔ HẠI đứng trước không được tước miễn trừ của câu
    # AC 19 hợp lệ đứng sau.
    ("oan_dong_thut_le_khong_phai_rao",
     '    ``` đây chỉ là một dòng code thụt lề\n\nĐo được: ba tên tấn công rc=4, tên thuộc\ndanh sách cho phép vẫn rc=0.'),
    ("oan_the_bang_trong_khoi_ma",
     '```html\n<table>\n```\n\nĐo được: ba tên tấn công rc=4, tên thuộc\ndanh sách cho phép vẫn rc=0.'),
    # CÙNG MỘT ĐOẠN, cố ý không có dòng trống: nếu tách đoạn thì luật "dòng trống kết
    # thúc khối HTML" đã cứu ca này rồi, và đột biến gỡ phép loại mã inline sẽ không
    # giết được nó — ca mất độ phân giải.
    ("oan_the_bang_trong_ma_inline",
     'Ví dụ ký hiệu `<table>` trong tài liệu. Đo được: ba tên tấn công rc=4, tên thuộc\ndanh sách cho phép vẫn rc=0.'),
    ("oan_the_bang_trong_comment",
     '<!-- <table> -->\n\nĐo được: ba tên tấn công rc=4, tên thuộc\ndanh sách cho phép vẫn rc=0.'),
    # Bảng THẬT chưa đóng thẻ. Luật CommonMark "khối HTML kết thúc ở DÒNG TRỐNG đầu
    # tiên" là thứ duy nhất giữ câu AC 19 phía sau khỏi bị nuốt; g8 cho nuốt tới hết tệp.
    ("oan_van_xuoi_sau_bang_html_chua_dong",
     '<table><tr><td>thời gian</td></tr>\n\nĐo được: ba tên tấn công rc=4, tên thuộc\ndanh sách cho phép vẫn rc=0.'),
    ("oan_fence_long_cap_vo_hai",
     "- ```sh\n  # chay thu\n  python tl.py --json\n  ```\n\n---\n\n"
     "> ```\n> ket qua: rc=0\n> ```\n"),
]

# --- ÁNH XẠ LỚP → CA BẮT-OAN — AC 19 đòi "ít nhất một ca bắt-oan cho MỖI lớp" ----
#
# Finding `ac19-false-positive-matrix-incomplete` (cross-review lượt 6): generation 4
# khai 40 lớp lách nhưng chỉ có 14 ca bắt-oan, và KHÔNG có bảng nào nối hai bên. Không
# có ánh xạ thì "mỗi lớp một ca" là lời hứa, không phải điều kiểm được — thêm một lớp
# mà quên ca bắt-oan sẽ đi lọt trong im lặng.
#
# Bảng này biến lời hứa thành CHỐT: `main()` đối chiếu mọi lớp trong `LOP_LACH` với
# bảng, và suite ĐỎ nếu có lớp không được ánh xạ. Một lớp có thể dùng chung ca với lớp
# cùng họ — nói rõ như vậy còn hơn nhân bản ca cho đủ số.
ANH_XA_LOP_BAT_OAN = {
    # Mười hai lớp mới của revision 4: mỗi lớp trỏ về ca bắt-oan CÙNG HÌNH DẠNG,
    # khác đúng một chỗ — nội dung không còn cụm cấm. Cặp cùng hình dạng là thứ
    # chứng minh cổng phân biệt NỘI DUNG chứ không phân biệt cấu trúc Markdown.
    "cum_don_claude_md_master_tha_cu": "oan_claude_md_master",
    "cum_don_term_ngat_dong_tha_cu": "oan_term_ngat_dong",
    "cum_don_van_xuoi_ngat_dong_trong_bullet_tha_cu": "oan_van_xuoi_ngat_dong_trong_bullet",
    "cum_don_van_xuoi_ngat_dong_trong_danh_sach_so_tha_cu": "oan_van_xuoi_ngat_dong_trong_danh_sach_so",
    "cum_don_van_xuoi_ngat_dong_trong_trich_dan_tha_cu": "oan_van_xuoi_ngat_dong_trong_trich_dan",
    "cum_don_van_xuoi_sau_bang_html_tha_cu": "oan_van_xuoi_sau_bang_html",
    "cum_don_rao_dong_dung_luat_tha_cu": "oan_rao_dong_dung_luat",
    "cum_don_dong_thut_le_khong_phai_rao_tha_cu": "oan_dong_thut_le_khong_phai_rao",
    "cum_don_the_bang_trong_khoi_ma_tha_cu": "oan_the_bang_trong_khoi_ma",
    "cum_don_the_bang_trong_ma_inline_tha_cu": "oan_the_bang_trong_ma_inline",
    "cum_don_the_bang_trong_comment_tha_cu": "oan_the_bang_trong_comment",
    "cum_don_van_xuoi_sau_bang_html_chua_dong_tha_cu": "oan_van_xuoi_sau_bang_html_chua_dong",
    "nfkc_hai_cham_toan_rong": "oan_dau_cau_toan_rong",
    "nfkc_chu_toan_rong": "oan_dau_cau_toan_rong",
    "nfkc_chu_so_tron": "oan_dau_cau_toan_rong",
    "nfkc_chu_so_mu": "oan_dau_cau_toan_rong",
    "nfkc_ligature_ff": "oan_tieng_viet_du_dau",
    "nfkc_solidus_toan_rong": "oan_dau_cau_toan_rong",
    "nfkc_gach_duoi_toan_rong": "oan_tu_gach_noi",
    "nfkc_vach_dung_toan_rong": "oan_bang_khac",
    "nbsp_phu_ba_lop": "oan_tieng_viet_du_dau",
    "phan_cach_en_dash": "oan_tu_gach_noi",
    "phan_cach_hyphen": "oan_tu_gach_noi",
    "cf_zwnj": "oan_tieng_viet_du_dau",
    "cf_zwj": "oan_tieng_viet_du_dau",
    "cf_word_joiner": "oan_tieng_viet_du_dau",
    "cf_soft_hyphen": "oan_tieng_viet_du_dau",
    "cf_bom": "oan_tieng_viet_du_dau",
    "entity_thap_luc": "oan_entity_long",
    "entity_co_ten": "oan_entity_long",
    "entity_thieu_cham_phay": "oan_entity_long",
    "dong_tu_cyrillic_e": "oan_van_ban_nga",
    "dong_tu_cyrillic_o": "oan_van_ban_nga",
    "dong_tu_hy_lap_o": "oan_van_ban_hy_lap",
    "dong_tu_cyrillic_a": "oan_van_ban_nga",
    "nhay_cong_xen_giua": "oan_nhay_cong_van_xuoi",
    "mui_ten_dai": "oan_mui_ten_van_xuoi",
    "tag_html_xen_giua": "oan_tag_html_vo_hai",
    "comment_html_xen_giua": "oan_comment_html_vo_hai",
    "link_markdown": "oan_link_binh_thuong",
    "backslash_escape": "oan_escape_markdown",
    "tag_thuoc_tinh_nhay_kep": "oan_tag_thuoc_tinh_vo_hai",
    "tag_thuoc_tinh_nhay_don": "oan_tag_thuoc_tinh_vo_hai",
    "tag_thuoc_tinh_dau_nho_hon": "oan_shell_chuyen_huong",
    "tag_ngat_qua_dong": "oan_tag_ngat_dong_vo_hai",
    "comment_html_ngat_qua_dong": "oan_comment_html_vo_hai",
    "link_ngoac_long": "oan_link_ngoac_long_vo_hai",
    "cum_don_heading": "oan_term_ngat_dong",
    "cum_don_dong_tran": "oan_term_ngat_dong",
    "cum_don_gach_dau_dong": "oan_term_ngat_dong",
    "cum_don_in_dam": "oan_term_ngat_dong",
    "cum_don_dinh_nghia": "oan_term_ngat_dong",
    "cum_don_cau_van_xuoi_mot_dong": "oan_claude_md_master",
    # Họ K — ca bắt-oan phải là hình dạng ĐỐI XỨNG: cùng bị ngắt dòng, nhưng LÀ văn
    # xuôi kể lại kết quả đo. Nếu bản vá thu miễn trừ quá tay thì chính những ca này
    # đỏ lên, nên chúng đo được hướng ngược của cùng một chốt.
    "cum_don_heading_ngat_dong": "oan_claude_md_master",
    "cum_don_gach_dau_dong_ngat_dong": "oan_van_xuoi_ngat_dong_trong_bullet",
    "cum_don_danh_sach_so_ngat_dong": "oan_van_xuoi_ngat_dong_trong_danh_sach_so",
    "cum_don_dong_tran_ngat_dong": "oan_term_ngat_dong",
    "cum_don_code_fence": "oan_code_fence_vo_hai",
    "cum_don_code_fence_ngoac_song": "oan_code_fence_vo_hai",
    "cum_don_o_bang_html_ngat_dong": "oan_tag_ngat_dong_vo_hai",
    "cum_don_fence_trong_bullet": "oan_fence_long_cap_vo_hai",
    "cum_don_fence_trong_trich_dan": "oan_fence_long_cap_vo_hai",
    "cum_don_o_bang_html_co_chu_hai_phia": "oan_bang_html_vo_hai",
    "cum_don_o_bang_html_khong_dong_the": "oan_van_xuoi_sau_bang_html",
    # Họ W/F/H của lượt 9. Ca bắt-oan phải ĐỐI XỨNG: cùng hình dạng, nhưng CÓ kể lại
    # một phép đo (họ W), hoặc rào/bảng hợp lệ (họ F/H).
    "cum_don_wrapper_mot_chu_cai": "oan_term_ngat_dong",
    "cum_don_wrapper_chu_so": "oan_term_ngat_dong",
    "cum_don_wrapper_trong_tag": "oan_claude_md_master",
    "cum_don_van_xuoi_khong_ke_phep_do": "oan_term_ngat_dong",
    "cum_don_rao_dong_ngan_hon": "oan_rao_dong_dung_luat",
    "cum_don_rao_dong_co_duoi": "oan_rao_dong_dung_luat",
    "cum_don_rao_song_dong_ngan_hon": "oan_rao_dong_dung_luat",
    "cum_don_bang_html_long": "oan_bang_html_long_vo_hai",
    "cum_don_bang_html_long_ba_cap": "oan_bang_html_long_vo_hai",
    "cum_don_chi_co_chu_truoc": "oan_claude_md_master",
    "cum_don_chi_co_chu_sau": "oan_term_ngat_dong",
    "cum_don_trich_dan_ngat_dong": "oan_van_xuoi_ngat_dong_trong_trich_dan",
    "cum_don_trich_dan_long_hai_cap": "oan_van_xuoi_ngat_dong_trong_trich_dan",
    "cum_don_heading_long_trich_dan": "oan_van_xuoi_ngat_dong_trong_trich_dan",
}


def case_g5_reviewing_khong_ra_bang_transition(c: Ctx):
    """`review-transition-bypasses-record-review` P1 — cross-review lượt 6.

    Bản trước cho `reviewing → running` bằng `transition`, nên ba lệnh transition là
    quay lại review mà KHÔNG gọi `record-review`: lặp review↔fix vô hạn trong cùng
    một attempt, `reviews` rỗng, `finding_counts` rỗng, không chạm trần nào.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "running", "--comment-id", "7788000001"], sd)
    _doi(0, rc, e, "record-post running")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "running", "--comment-id", "7788000001"], sd)
    _doi(8, rc, e, "ra khỏi 'reviewing' bằng transition — đường vòng qua record-review")
    if c.state(sd, 55) != "reviewing":
        raise AssertionError("transition bị chặn nhưng state vẫn đổi")


def case_g5_verdict_van_dua_duoc_ve_running(c: Ctx):
    """Chiều BẮT OAN của ca trên: đóng cửa `transition` KHÔNG được khoá cứng packet.

    Đường hợp lệ ra khỏi `reviewing` là VERDICT. Thiếu ca này thì "siết cho chặt"
    biến `reviewing` thành ngõ cụt và không ai phân biệt được chốt đúng với chốt hỏng.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = c.review(sd, 55, ["mot-loi"], luot=1)
    _doi(0, rc, e, "changes_requested phải đưa về running")
    if c.state(sd, 55) != "running":
        raise AssertionError(f"sau changes_requested state phải là 'running', được {c.state(sd, 55)!r}")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "mở được lượt mới sau verdict")


def case_g5_void_o_reviewing_khong_ket_thuc_bang_approve(c: Ctx):
    """`void-reviewing-accepts-attempt-zero` P1 — cross-review lượt 6.

    Chuỗi đo được trên `e6e4b73`: `void-attempt` rc=0 để lại `state=reviewing` với
    `attempts_used=0`; `begin-attempt` rc=8 nên packet KẸT; rồi `record-review
    --verdict approve` rc=0 đưa sang `accepted` với `reviews[0].attempt=0` — bản
    duyệt của một lượt KHÔNG TỒN TẠI.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota", *VOID_DUYET], sd)
    _doi(0, rc, e, "void-attempt vì quota")
    tt = c.state(sd, 55)
    if tt == "reviewing":
        raise AssertionError("void để state KẸT ở 'reviewing' — begin-attempt sẽ rc=8")
    rc, _, e = run(c.script,
                   ["record-review", "--packet", 55, "--provider", REVIEWER,
                    "--verdict", "approve", "--reviewed-sha", c.head(1)], sd)
    if rc == 0:
        raise AssertionError("approve được với attempts_used=0 — bản duyệt của lượt KHÔNG TỒN TẠI")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "sau void phải mở lại được lượt — không được kẹt cứng")


def case_g5_record_review_doi_LUOT_DANG_MO(c: Ctx):
    """Cô lập chốt LỚP HAI của `void-reviewing-accepts-attempt-zero`.

    Sau khi `void-attempt` đã được sửa để rời `reviewing`, trạng thái
    `state=reviewing` + `attempt_open=False` KHÔNG còn tới được qua public CLI —
    nên ca đi qua CLI chỉ đo được chốt thứ nhất, và chốt thứ hai trông như thừa.
    Nó không thừa: nó là hàng phòng thủ cho state CŨ hoặc BỊ SỬA TAY, đúng loại
    state mà `legacy_state_khong_co_lease_bi_chan` đã phải chặn một lần rồi.

    Nên ca này dựng thẳng state ấy — cùng cách `_state_voi_lease` đang làm — để mỗi
    chốt có ca riêng và mỗi đột biến giết đúng ca của nó.
    """
    import json as _json
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    p = sd / "wp55.json"
    st = _json.loads(p.read_text(encoding="utf-8"))
    st["attempt_open"] = False          # lượt đã đóng nhưng state kẹt ở reviewing
    p.write_text(_json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    rc, _, e = run(c.script,
                   ["record-review", "--packet", 55, "--provider", REVIEWER,
                    "--verdict", "approve", "--reviewed-sha", c.head(1)], sd)
    _doi(8, rc, e, "ghi được review khi KHÔNG có lượt nào đang mở")


def case_g5_record_review_doi_SO_LUOT_LON_HON_0(c: Ctx):
    """Cô lập chốt `attempts_used > 0`, tách khỏi chốt `attempt_open`."""
    import json as _json
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    p = sd / "wp55.json"
    st = _json.loads(p.read_text(encoding="utf-8"))
    st["attempts_used"] = 0             # lượt vẫn "mở" nhưng số lượt là 0
    p.write_text(_json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    rc, _, e = run(c.script,
                   ["record-review", "--packet", 55, "--provider", REVIEWER,
                    "--verdict", "approve", "--reviewed-sha", c.head(1)], sd)
    _doi(8, rc, e, "ghi được review cho lượt số 0")


def case_ac19_bang_vai_tro_THAT_van_bi_bat(c: Ctx):
    """Chiều DƯƠNG của hạng NGÔN NGỮ THƯỜNG: chép ĐÚNG dòng bảng vai trò vẫn ĐỎ.

    Không có ca này thì `CUM_NGON_NGU_THUONG` chỉ là một đường tha, và người đọc
    không phân biệt được "đã sửa chiều bắt oan" với "đã gỡ chốt".

    Ô bảng CỐ Ý không chứa mục cấm nào khác — nếu để nguyên ô nội dung thật
    (`start/pause/…`) thì ca vẫn đỏ nhờ mục KHÁC, và đột biến gỡ cụm khỏi danh
    sách sẽ không giết được nó: ca sẽ xanh vì lý do khác với lý do nó khai.
    """
    dong = "| Người có thẩm quyền | vai trò cấp lease |"
    r = _repo_gia(c.tmp, SACH + "\n" + dong + "\n", ten="oan_bang_vai_tro_that")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "chép ĐÚNG dòng bảng vai trò §2 mà KHÔNG bị bắt")


def case_ac19_term_kem_muc_khac_cung_nhom_bi_bat(c: Ctx):
    """Cụm hạng ngôn ngữ thường + một mục KHÁC cùng nhóm trong cùng đoạn ⇒ ĐỎ.

    Đây là điều kiện (2) của `_co_ngu_canh_doctrine`: đoạn đang DỰNG LẠI bảng vai
    trò chứ không dùng cụm từ trong câu.
    """
    r = _repo_gia(
        c.tmp,
        SACH + "\nVai trò: người có thẩm quyền, local controller, land operator.\n",
        ten="oan_term_kem_muc_khac")
    rc, _, e = run(c.script, ["doctrine-scan", "--root", r])
    _doi(6, rc, e, "term + mục khác cùng nhóm trong một đoạn mà KHÔNG bị bắt")


# --- (i) AC 21 · lược đồ lease qua MỘT hàm kiểm chung ---------------------------

def _state_voi_lease(c: Ctx, lease):
    """Dựng state `leased` mang đúng hình dạng `lease` cần đo, rồi mở lượt.

    Sửa THẲNG tệp state là cố ý: đây là mô phỏng một state CŨ hoặc BỊ SỬA TAY —
    đúng thứ `begin-attempt` phải fail-closed trước, và đúng thứ `record-lease`
    không bao giờ sinh ra được.
    """
    import json as _json
    sd = c.sd()
    rc, _, e = c.init(sd, lease=False)
    _doi(0, rc, e, "init")
    p = sd / "wp55.json"
    st = _json.loads(p.read_text(encoding="utf-8"))
    st["state"] = "leased"
    st["lease"] = lease
    p.write_text(_json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\n",
                 encoding="utf-8")
    return run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)


def _han_sau(**kw) -> str:
    from datetime import datetime, timedelta, timezone
    return (datetime.now(timezone.utc) + timedelta(**kw)).strftime("%Y-%m-%dT%H:%M:%SZ")


def _lease_du(**ghi_de) -> dict:
    d = {"lease_id": "wp55-test", "granted_by": "ducthangho",
         "evidence": "https://github.com/o/r/issues/55#issuecomment-5281636040",
         "expires_utc": _han_sau(hours=4)}
    d.update(ghi_de)
    return d


def _doi_chan(c: Ctx, lease, ten: str):
    """Đòi MÃ THOÁT CÓ KIỂM SOÁT và KHÔNG traceback."""
    rc, _, e = _state_voi_lease(c, lease)
    err = _txt(e)
    if rc == 0:
        raise AssertionError(f"{ten}: hình dạng lease sai mà LỌT (rc=0)")
    if rc == 1 or "Traceback" in err:
        raise AssertionError(f"{ten}: vỡ bằng TRACEBACK THÔ (rc={rc}) thay vì mã thoát "
                             f"có kiểm soát; stderr={err[:200]!r}")


def case_ac21_lease_chi_co_expires(c: Ctx):
    """P1-B nguyên văn: `begin-attempt` nhận state `record-lease` không sinh ra được."""
    _doi_chan(c, {"expires_utc": _han_sau(hours=4)}, "chỉ có expires_utc")


def case_ac21_lease_thieu_tung_khoa(c: Ctx):
    for k in ("lease_id", "granted_by", "evidence", "expires_utc"):
        d = _lease_du()
        d.pop(k)
        _doi_chan(c, d, f"thiếu {k}")


def case_ac21_lease_sai_kieu_khong_traceback(c: Ctx):
    for v in ("stolen", 12345, [1, 2], True, 3.5):
        _doi_chan(c, v, f"lease kiểu {type(v).__name__}")


def case_ac21_khoa_sai_kieu_khong_traceback(c: Ctx):
    for k, v in (("lease_id", ["x"]), ("granted_by", 7), ("evidence", {}),
                 ("expires_utc", 99), ("expires_utc", None)):
        _doi_chan(c, _lease_du(**{k: v}), f"{k}={v!r}")


def case_ac21_khoa_rong(c: Ctx):
    for k in ("lease_id", "granted_by", "evidence", "expires_utc"):
        _doi_chan(c, _lease_du(**{k: "   "}), f"{k} rỗng")


def case_ac21_expires_sai_dang(c: Ctx):
    for v in ("not-a-date", "2099-01-01T00:00:00", "2099-13-45T99:99:99"):
        _doi_chan(c, _lease_du(expires_utc=v), f"expires_utc={v!r}")


def case_ac21_expires_ngoai_cua_so(c: Ctx):
    """Năm 9999 và trước 1970 — hai đầu của cửa sổ hạn.

    Một lease sống tới năm 9999 làm chốt hạn thành trang trí; bản trước nhận nó.
    """
    _doi_chan(c, _lease_du(expires_utc="9999-01-01T00:00:00Z"), "năm 9999")
    _doi_chan(c, _lease_du(expires_utc="1960-01-01T00:00:00Z"), "trước 1970")
    _doi_chan(c, _lease_du(expires_utc=_han_sau(days=400)), "xa hơn 366 ngày")


def case_ac21_lease_tu_cap_trong_state(c: Ctx):
    """Lease TỰ CẤP còn nguyên trong state vẫn là lease tự cấp lúc mở lượt.

    `record-lease` chặn `granted_by: "claude"` bằng rc=7, nhưng bản trước
    `begin-attempt` KHÔNG kiểm lại thẩm quyền — nên state đó mở được lượt (rc=0).
    """
    _doi_chan(c, _lease_du(granted_by="claude"), "granted_by là provider")
    _doi_chan(c, _lease_du(granted_by="codex-dispatcher"), "granted_by ngoài allowlist")


def case_ac21_lease_hop_le_KHONG_bi_chan(c: Ctx):
    """Chiều BẮT OAN của AC 21: state HỢP LỆ không được bị chặn.

    Thiếu ca này thì "siết cho chặt" biến packet thành kẹt cứng, và không ai
    phân biệt được chốt đúng với chốt hỏng.
    """
    for ten, d in (("hạn +4h", _lease_du()),
                   ("hạn +300 ngày", _lease_du(expires_utc=_han_sau(days=300))),
                   ("granted_by có hoa/khoảng trắng", _lease_du(granted_by="  DUCTHANGHO  "))):
        rc, _, e = _state_voi_lease(c, d)
        _doi(0, rc, e, f"chặn OAN một lease hợp lệ ({ten})")


def case_ac21_hai_cua_CUNG_luoc_do(c: Ctx):
    """Hai cửa, MỘT lược đồ: thứ `record-lease` từ chối thì `begin-attempt` cũng từ chối.

    Đây là phát biểu trực tiếp của AC 21. Ca này so HÀNH VI của hai lệnh trên
    cùng một tập hình dạng, thay vì tin rằng chúng dùng chung hàm.
    """
    xau = [_lease_du(granted_by="claude"),
           _lease_du(granted_by="codex-dispatcher"),
           _lease_du(lease_id="  "),
           _lease_du(evidence="  "),
           _lease_du(expires_utc="9999-01-01T00:00:00Z"),
           _lease_du(expires_utc="2099-01-01T00:00:00")]
    for d in xau:
        sd = c.sd()
        rc, _, e = c.init(sd, lease=False)
        _doi(0, rc, e, "init")
        rc_ghi, _, _ = c.cap_lease(sd, 55, granted_by=d["granted_by"],
                                   expires=d["expires_utc"], evidence=d["evidence"],
                                   lease_id=d["lease_id"])
        rc_mo, _, _ = _state_voi_lease(c, d)
        if (rc_ghi == 0) != (rc_mo == 0):
            raise AssertionError(
                f"record-lease và begin-attempt LỆCH NHAU trên {d!r}: "
                f"record-lease rc={rc_ghi}, begin-attempt rc={rc_mo}")


# --- (d) adr-song: bảng §20 phải PHỦ HẾT docs/adr/ ----------------------------
#
# Cổng này thay một dòng PHẠM VI đã chết (`ADR-0017 đến ADR-0035`) bằng một bảng
# mà máy đòi đầy đủ. Mỗi luật của nó có ĐÚNG một ca ở đây và ĐÚNG một đột biến ở
# `MUTANTS` — luật không có đột biến riêng là luật sẽ âm thầm hở lại, đúng bài
# học "mỗi cửa phải có ĐỘT BIẾN RIÊNG".

_ADR_THAN = "# ADR-{n} — ca thử\n\n- **Trạng thái:** Accepted (2026-08-22)\n\nThân.\n"
_ADR_THAN_KHONG_TRANG_THAI = "# ADR-{n} — ca thử\n\nKhông có dòng trạng thái.\n"


def _repo_adr_gia(tmp: Path, so_adr, hang_bang, ten,
                  co_git=True, co_muc20=True, co_thu_muc=True, them_van_xuoi=""):
    """Dựng một kho giả tối thiểu: `docs/adr/*.md` + `docs/PROTOCOL_DA_PHIEN.md` §20.

    `so_adr` là danh sách `(số, có_dòng_trạng_thái)`. `hang_bang` là danh sách số
    sẽ được viết thành DÒNG BẢNG trong §20 — tách khỏi `so_adr` cốt để dựng được
    cả hai chiều lệch (thiếu dòng / dòng trỏ hư).
    """
    r = tmp / f"repo_adr_{ten}"
    (r / "docs").mkdir(parents=True, exist_ok=True)
    if co_git:
        (r / ".git").mkdir(exist_ok=True)
    if co_thu_muc:
        d = r / "docs" / "adr"
        d.mkdir(parents=True, exist_ok=True)
        for so, co_tt in so_adr:
            mau = _ADR_THAN if co_tt else _ADR_THAN_KHONG_TRANG_THAI
            (d / f"{so}-ca-thu.md").write_text(mau.format(n=so), encoding="utf-8", newline="\n")
    than = "# Protocol giả\n\n## 19. Mục trước\n\nNội dung.\n"
    if co_muc20:
        than += "\n## 20. Quy tắc đang hiệu lực — bảng định tuyến ADR\n\n"
        than += them_van_xuoi
        than += "| ADR | luật | trạng thái | cổng đã ĐO |\n|---|---|---|---|\n"
        for so in hang_bang:
            than += f"| `ADR-{so}` | luật {so} | Accepted | 0 cổng |\n"
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(than, encoding="utf-8", newline="\n")
    return r


def case_adr_song_sach_xanh(c: Ctx):
    r = _repo_adr_gia(c.tmp, [("0001", True), ("0002", True)], ["0001", "0002"], "sach")
    rc, o, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "bảng phủ đủ phải XANH")
    # BẰNG CHỨNG DƯƠNG, không chỉ rc: hai số phải BẰNG NHAU và phải là 2.
    s = _txt(o)
    if "2 ADR trên đĩa, 2 dòng" not in s:
        raise AssertionError(f"thiếu bằng chứng dương hai số bằng nhau: {s!r}")


def case_adr_song_thieu_dong_thi_do(c: Ctx):
    r = _repo_adr_gia(c.tmp, [("0001", True), ("0002", True)], ["0001"], "thieu")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "ADR có tệp mà không có dòng trong §20 phải ĐỎ")


def case_adr_song_con_tro_chet_thi_do(c: Ctx):
    """Chính căn bệnh cổng này sinh ra để chữa: bảng trỏ một ADR không tồn tại."""
    r = _repo_adr_gia(c.tmp, [("0001", True)], ["0001", "0099"], "contro")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "§20 trỏ ADR không có tệp phải ĐỎ")


def case_adr_song_trung_dong_thi_do(c: Ctx):
    r = _repo_adr_gia(c.tmp, [("0001", True)], ["0001", "0001"], "trung")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "một ADR có hai dòng phải ĐỎ")


def case_adr_song_thieu_trang_thai_thi_do(c: Ctx):
    """Trạng thái thứ ba (`không đo được`) phải làm cổng ĐỎ, không làm nó xanh."""
    r = _repo_adr_gia(c.tmp, [("0007", False)], ["0007"], "khongtt")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "ADR thiếu dòng `Trạng thái` phải ĐỎ")


def case_adr_song_ngoai_le_0016_van_xanh(c: Ctx):
    """Nợ CÓ TÊN `ADR-0016-THIEU-DONG-TRANG-THAI` — tha ĐÚNG một số, liệt kê tường minh.

    Ca này và ca trên đo CÙNG một luật ở hai phía: `0016` được tha, `0007` thì
    không. Không có ca này thì không phân biệt được "tha đúng một số" với "tha tất".
    """
    r = _repo_adr_gia(c.tmp, [("0016", False)], ["0016"], "ngoaile")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "ngoại lệ đã liệt kê phải XANH")


def case_adr_song_van_xuoi_khong_tinh_la_dong(c: Ctx):
    """Nhắc `ADR-0002` trong VĂN XUÔI không được tính là đã có dòng trong bảng.

    `t43` của `lease_publish_test.py` đã trả giá đúng chỗ này theo chiều ngược
    lại (một câu văn xuôi bị nhận nhầm làm marker). Ở đây chiều nguy hiểm là
    chiều kia: nhận nhầm thì cổng báo PHỦ ĐỦ trong khi bảng còn thiếu.
    """
    r = _repo_adr_gia(c.tmp, [("0001", True), ("0002", True)], ["0001"], "vanxuoi",
                      them_van_xuoi="Xem thêm `ADR-0002` | và các quyết định liên quan.\n\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "nhắc ADR trong văn xuôi KHÔNG phải một dòng bảng")


def case_adr_song_thieu_muc20_thi_do(c: Ctx):
    r = _repo_adr_gia(c.tmp, [("0001", True)], [], "khongmuc20", co_muc20=False)
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "protocol không có §20 thì cổng không có gì để đo — phải ĐỎ")


def case_adr_song_kho_that_thieu_thu_muc_thi_do(c: Ctx):
    """Nhánh "không thấy thì bỏ qua" chỉ được tha khi cây là bản sao rời.

    Bài học `t24`: một ca `return` sớm vì đường dẫn sai vẫn được đếm là ĐẠT.
    """
    r = _repo_adr_gia(c.tmp, [], [], "khongthumuc", co_thu_muc=False)
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "kho git mà thiếu docs/adr/ phải ĐỎ, không được bỏ qua êm")


def case_adr_song_ban_sao_roi_duoc_tha(c: Ctx):
    r = _repo_adr_gia(c.tmp, [], [], "bansaoroi", co_thu_muc=False, co_git=False)
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "bản sao rời (không .git) được tha")


def case_adr_song_KHO_THAT_xanh(c: Ctx):
    """Chạy trên KHO THẬT, không phải kho giả.

    Kho giả chứng minh cổng khớp với chính nó. Chỉ lượt chạy trên `docs/adr/`
    thật mới chứng minh bảng §20 đang phủ đủ HÔM NAY — và nó sẽ đỏ vào đúng ngày
    ai đó thêm một ADR mà quên bảng, tức đúng lúc cần.
    """
    if not (ROOT / "docs" / "adr").is_dir():
        raise AssertionError(f"thiếu {ROOT / 'docs' / 'adr'} — không đo được")
    rc, o, e = run(c.script, ["adr-song", "--root", ROOT])
    _doi(0, rc, e, "kho thật phải XANH")
    s = _txt(o)
    n = len(list((ROOT / "docs" / "adr").glob("*.md")))
    if f"{n} ADR trên đĩa, {n} dòng" not in s:
        raise AssertionError(f"đòi hai số bằng nhau = {n}; được: {s!r}")


def case_wp320_invalid_inputs(c: Ctx):
    bad = c.tmp / "bad.json"
    bad.write_text("{", encoding="utf-8")
    missing = c.tmp / "missing.json"
    missing.write_text('{"he_dieu_hanh": "Windows"}', encoding="utf-8")
    missing_file_path = c.tmp / "nonexistent.json"
    if missing_file_path.exists():
        raise AssertionError("WP320 diagnostic: Missing file fixture already exists")

    inputs = [
        ("absent flag/environment", [], {BIEN_BC: ""},
         ["không có ảnh môi trường", "''"]),
        ("missing file", ["--bang-chung-moi-truong", str(missing_file_path)], None,
         ["không có ảnh môi trường", "nonexistent.json"]),
        ("malformed JSON", ["--bang-chung-moi-truong", str(bad)], None,
         ["không đọc được", "JSONDecodeError"]),
        ("missing required fields", ["--bang-chung-moi-truong", str(missing)], None,
         ["thiếu trường của `doctor --json`"]),
    ]

    msgs = set()
    for name, args, env_extra, expected_substrs in inputs:
        sd = c.sd()
        _doi(0, *c.init(sd)[0:1], b"", "init")
        rc, o, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR] + args, sd, env_extra=env_extra)

        err_msg = _txt(e)
        msgs.add(err_msg)

        if rc != 10:
            raise AssertionError(f"WP320 diagnostic {name}: expected rc=10, got {rc}. err: {err_msg!r}")

        for substr in expected_substrs:
            if substr not in err_msg:
                raise AssertionError(f"WP320 diagnostic {name}: expected {substr!r} in {err_msg!r}")

        st = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
        if st["attempts_used"] != 0 or st["attempt_open"]:
            raise AssertionError(f"WP320 diagnostic {name}: state not isolated (attempts={st['attempts_used']}, open={st['attempt_open']})")

    if len(msgs) != 4:
        raise AssertionError(f"WP320 diagnostic: Expected 4 distinct messages, got {len(msgs)}: {msgs!r}")

def case_wp320_valid_evidence(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, o, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "WP320 clean valid evidence")
    st = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    if st["attempts_used"] != 1 or not st["attempt_open"]:
        raise AssertionError("WP320 diagnostic: Clean input phải increment lượt")


CASES = [
    ("wp320_invalid_inputs", case_wp320_invalid_inputs),
    ("wp320_valid_evidence", case_wp320_valid_evidence),
    ("init_KHONG_duoc_tu_cap_lease", case_init_KHONG_duoc_tu_cap_lease),
    ("tu_cap_lease_bang_ten_provider_bi_chan", case_tu_cap_lease_bang_ten_provider_bi_chan),
    ("lease_da_het_han_khong_ghi_duoc", case_lease_da_het_han_khong_ghi_duoc),
    ("lease_hop_le_thi_mo_duoc_luot", case_lease_hop_le_thi_mo_duoc_luot),
    ("begin_attempt_sau_khi_lease_HET_HAN_bi_chan", case_begin_attempt_sau_khi_lease_HET_HAN_bi_chan),
    ("init_cross_provider_ok", case_init_cross_provider_ok),
    ("init_cung_provider_thoat_4", case_init_cung_provider_thoat_4),
    ("review_sai_provider_thoat_4", case_review_sai_provider_thoat_4),
    ("cap_lan_4_thoat_3", case_cap_lan_4_thoat_3),
    ("begin_attempt_lap_khong_tieu_them_tran", case_begin_attempt_lap_khong_tieu_them_tran),
    ("init_khong_ghi_de_state_da_blocked", case_init_khong_ghi_de_state_da_blocked),
    ("init_khong_co_co_ghi_de", case_init_khong_co_co_ghi_de),
    ("review_phai_neo_head_da_dua_ra_review", case_review_phai_neo_head_da_dua_ra_review),
    ("review_thieu_hoac_sai_dang_sha", case_review_thieu_hoac_sai_dang_sha),
    ("transition_reviewing_phai_khai_head", case_transition_reviewing_phai_khai_head),
    ("approve_neo_dung_head_thi_chay", case_approve_neo_dung_head_thi_chay),
    ("head_moi_lam_ban_duyet_cu_het_hieu_luc", case_head_moi_lam_ban_duyet_cu_het_hieu_luc),
    ("same_failure_cung_id_qua_2_review", case_same_failure_cung_id_qua_2_review),
    ("same_failure_hai_id_khac_khong_kich", case_same_failure_hai_id_khac_khong_kich),
    ("same_failure_lap_trong_mot_review_tinh_mot", case_same_failure_lap_trong_mot_review_tinh_mot),
    ("same_failure_hai_mo_ta_cung_id_la_mot", case_same_failure_hai_mo_ta_cung_id_la_mot),
    ("thieu_finding_id_thoat_khac_0", case_thieu_finding_id_thoat_khac_0),
    ("slug_sai_dang_thoat_khac_0", case_slug_sai_dang_thoat_khac_0),
    ("guard_moi_hanh_vi_thoat_7", case_guard_moi_hanh_vi_thoat_7),
    # --- #338: ha loi khai + so khai bao DEM DUOC ---
    ("moc_dot_bien_phai_khop_DUNG_MOT_CHO", case_moc_dot_bien_phai_khop_DUNG_MOT_CHO),
    ("moc_kiem_TU_NO_co_rang", case_moc_kiem_TU_NO_co_rang),
    ("fixture_git_KHONG_an_config_toan_cuc", case_fixture_git_KHONG_an_config_toan_cuc),
    ("guard_KHONG_khai_minh_kiem_tham_quyen", case_guard_KHONG_khai_minh_kiem_tham_quyen),
    ("ghi_uy_quyen_doi_danh_sach_CHO_PHEP", case_ghi_uy_quyen_doi_danh_sach_CHO_PHEP),
    ("ghi_uy_quyen_doi_sha40_that", case_ghi_uy_quyen_doi_sha40_that),
    ("khai_uy_quyen_KHONG_mo_khoa_guard", case_khai_uy_quyen_KHONG_mo_khoa_guard),
    ("doi_chieu_dem_duoc_merge_co_khai_va_khong",
     case_doi_chieu_dem_duoc_merge_co_khai_va_khong),
    ("doi_chieu_neo_dung_HEAD_da_merge",
     case_doi_chieu_neo_dung_HEAD_da_merge_khong_phai_commit_merge),
    ("doi_chieu_chi_dem_FIRST_PARENT", case_doi_chieu_chi_dem_FIRST_PARENT),
    ("doi_chieu_THIEU_SO_la_KHONG_DO_DUOC", case_doi_chieu_THIEU_SO_la_KHONG_DO_DUOC),
    ("doi_chieu_TU_CHOI_ban_ghi_sai_luoc_do", case_doi_chieu_TU_CHOI_ban_ghi_sai_luoc_do),
    ("guard_khong_co_co_noi", case_guard_khong_co_co_noi),
    ("transition_hop_le_rc0", case_transition_hop_le_rc0),
    ("comment_id_chua_dang_ky_bi_tu_choi", case_comment_id_chua_dang_ky_bi_tu_choi),
    ("comment_id_dung_lai_bi_tu_choi", case_comment_id_dung_lai_bi_tu_choi),
    ("comment_id_sai_transition_bi_tu_choi", case_comment_id_sai_transition_bi_tu_choi),
    ("thieu_comment_id_chan_transition", case_thieu_comment_id_chan_transition),
    ("record_post_id_sai_dang_bi_tu_choi", case_record_post_id_sai_dang_bi_tu_choi),
    ("record_post_trung_id_bi_tu_choi", case_record_post_trung_id_bi_tu_choi),
    ("transition_khong_hop_le_thoat_8", case_transition_khong_hop_le_thoat_8),
    ("accepted_chi_dat_duoc_qua_record_review", case_accepted_chi_dat_duoc_qua_record_review),
    ("vao_reviewing_phai_co_luot_dang_mo", case_vao_reviewing_phai_co_luot_dang_mo),
    ("doctrine_scan_bat_qua_ngat_dong", case_doctrine_scan_bat_qua_ngat_dong),
    ("void_khong_bang_chung_phai_ghi_so", case_void_khong_bang_chung_phai_ghi_so),
    ("void_cung_run_hai_lan_bi_chan", case_void_cung_run_hai_lan_bi_chan),
    ("void_lat_phan_quyet_bi_hmac_chan", case_void_lat_phan_quyet_bi_hmac_chan),
    ("void_run_cheo_luot_bi_chan", case_void_run_cheo_luot_bi_chan),
    ("void_run_cu_khong_neo_co_thong_diep_rieng", case_void_run_cu_khong_neo_co_thong_diep_rieng),
    ("void_run_that_dung_luot_duoc_tha", case_void_run_that_dung_luot_duoc_tha),
    ("void_hai_ly_do_khong_dung_chung_run", case_void_hai_ly_do_khong_dung_chung_run),
    ("void_phan_biet_loi_probe_va_sau_spawn", case_void_phan_biet_loi_probe_va_sau_spawn),
    ("void_cung_anh_doctor_hai_luot_bi_chan", case_void_cung_anh_doctor_hai_luot_bi_chan),
    ("void_touch_anh_doctor_cu_van_bi_chan", case_void_touch_anh_doctor_cu_van_bi_chan),
    ("chup_anh_doctor_ky_noi_bo", case_chup_anh_doctor_ky_noi_bo),
    ("anh_doctor_nen_chung_tuoi_chi_begin", case_anh_doctor_nen_chung_tuoi_chi_begin),
    ("ma_in_thang_gioi_han_cung_principal", case_ma_in_thang_gioi_han_cung_principal),
    ("void_attempt_allowlist", case_void_attempt_allowlist),
    ("void_xong_van_mo_lai_duoc_luot", case_void_xong_van_mo_lai_duoc_luot),
    ("void_attempt_ly_do_tu_che_bi_tu_choi", case_void_attempt_ly_do_tu_che_bi_tu_choi),
    ("void_sau_review_bi_chan", case_void_sau_review_bi_chan),
    ("doctrine_scan_sach_xanh", case_doctrine_scan_sach_xanh),
    ("doctrine_scan_bom_cum_tu_do", case_doctrine_scan_bom_cum_tu_do),
    ("doctrine_scan_bat_doctrine_THAT_tu_protocol", case_doctrine_scan_bat_doctrine_THAT_tu_protocol),
    ("doctrine_scan_repo_that_sach", case_doctrine_scan_repo_that_sach),
    ("doctrine_scan_chep_tron_5_1_bi_chan", case_doctrine_scan_chep_tron_5_1_bi_chan),
    ("doctrine_scan_chep_doan_ngan_5_1_bi_chan", case_doctrine_scan_chep_doan_ngan_5_1_bi_chan),
    ("doctrine_scan_chep_12_bi_chan", case_doctrine_scan_chep_12_bi_chan),
    ("doctrine_scan_fail_close_thieu_protocol", case_doctrine_scan_fail_close_thieu_protocol),
    ("doctrine_scan_fail_close_khong_phai_utf8", case_doctrine_scan_fail_close_khong_phai_utf8),
    ("doctrine_scan_fail_close_protocol_ngan", case_doctrine_scan_fail_close_protocol_ngan),
    ("doctrine_scan_fail_close_chi_co_fence", case_doctrine_scan_fail_close_chi_co_fence),
    ("doctrine_scan_adr_0048_khong_phai_chep_protocol", case_doctrine_scan_adr_0048_khong_phai_chep_protocol),
    ("doctrine_scan_con_tro_thuan_tuy_xanh", case_doctrine_scan_con_tro_thuan_tuy_xanh),
    ("stdout_cp1252", case_stdout_cp1252),
    ("stdout_cp1258", case_stdout_cp1258),
    ("cross_review_co_cu_phap_ghi_verdict_len_pr", case_cross_review_co_cu_phap_ghi_verdict_len_pr),
    ("land_packets_khong_tu_trigger", case_land_packets_khong_tu_trigger),
    ("lease_authority_ten_gia_mao_bi_chan", case_lease_authority_ten_gia_mao_bi_chan),
    ("lease_authority_nguoi_co_tham_quyen_thi_qua", case_lease_authority_nguoi_co_tham_quyen_thi_qua),
    ("g9_lease_khoa_thua_bi_chan", case_g9_lease_khoa_thua_bi_chan),
    ("legacy_state_khong_co_lease_bi_chan", case_legacy_state_khong_co_lease_bi_chan),
    ("doctrine_scan_bat_zero_width_bi_chan", case_doctrine_scan_bat_zero_width_bi_chan),
    ("doctrine_scan_bat_html_entity_bi_chan", case_doctrine_scan_bat_html_entity_bi_chan),
    ("doctrine_scan_khong_giai_entity_lap", case_doctrine_scan_khong_giai_entity_lap),
    ("g5_reviewing_khong_ra_bang_transition", case_g5_reviewing_khong_ra_bang_transition),
    ("g5_verdict_van_dua_duoc_ve_running", case_g5_verdict_van_dua_duoc_ve_running),
    ("g5_void_o_reviewing_khong_ket_thuc_bang_approve", case_g5_void_o_reviewing_khong_ket_thuc_bang_approve),
    ("g5_record_review_doi_LUOT_DANG_MO", case_g5_record_review_doi_LUOT_DANG_MO),
    ("g5_record_review_doi_SO_LUOT_LON_HON_0", case_g5_record_review_doi_SO_LUOT_LON_HON_0),
    ("ac19_bang_vai_tro_THAT_van_bi_bat", case_ac19_bang_vai_tro_THAT_van_bi_bat),
    ("ac19_term_kem_muc_khac_cung_nhom_bi_bat", case_ac19_term_kem_muc_khac_cung_nhom_bi_bat),
    ("ac21_lease_chi_co_expires", case_ac21_lease_chi_co_expires),
    ("ac21_lease_thieu_tung_khoa", case_ac21_lease_thieu_tung_khoa),
    ("ac21_lease_sai_kieu_khong_traceback", case_ac21_lease_sai_kieu_khong_traceback),
    ("ac21_khoa_sai_kieu_khong_traceback", case_ac21_khoa_sai_kieu_khong_traceback),
    ("ac21_khoa_rong", case_ac21_khoa_rong),
    ("ac21_expires_sai_dang", case_ac21_expires_sai_dang),
    ("ac21_expires_ngoai_cua_so", case_ac21_expires_ngoai_cua_so),
    ("ac21_lease_tu_cap_trong_state", case_ac21_lease_tu_cap_trong_state),
    ("ac21_lease_hop_le_KHONG_bi_chan", case_ac21_lease_hop_le_KHONG_bi_chan),
    ("ac21_hai_cua_CUNG_luoc_do", case_ac21_hai_cua_CUNG_luoc_do),
]

# --- (d2) adr-song: DẠNG TÊN TỆP và tệp TRÙNG SỐ -------------------------------
#
# Cả bốn ca dưới đây sinh từ MỘT finding cross-review (codex, P2 trên PR #233, head
# `cbd14439bb`): bản đầu gom tệp bằng `{f.name[:4]: f for f in glob("*.md")}`, nên
# hai tệp cùng bốn chữ số đầu thì cái sau ĐÈ cái trước. Phản chứng đã chạy trước
# khi vá: 2 tệp trên đĩa, cổng in "1 ADR trên đĩa, 1 dòng trong §20", `rc=0`.
#
# Bài học ghi ở đây vì nó rộng hơn một bản vá: **hai số bằng nhau chỉ là bằng chứng
# khi chúng đến từ HAI phép đếm ĐỘC LẬP.** Ở bản đầu cả hai số đều rút từ cùng cái
# map đã bị nuốt, nên chúng bằng nhau bất kể bao nhiêu tệp biến mất — một "bằng
# chứng dương" tự chứng minh chính nó.


def _repo_adr_ten(tmp: Path, ten_tep, hang_bang, ten, co_git=True, thu_muc_con=None):
    """Như `_repo_adr_gia` nhưng nhận TÊN TỆP nguyên văn, để dựng được tên lệch dạng."""
    r = tmp / f"repo_adrten_{ten}"
    d = r / "docs" / "adr"
    d.mkdir(parents=True, exist_ok=True)
    if co_git:
        (r / ".git").mkdir(exist_ok=True)
    for n in ten_tep:
        (d / n).write_text(f"# ADR — {n}\n\n- **Trạng thái:** Accepted (2026-08-22)\n",
                           encoding="utf-8", newline="\n")
    if thu_muc_con:
        (d / thu_muc_con).mkdir(exist_ok=True)
    than = "# Protocol giả\n\n## 19. Mục trước\n\nNội dung.\n"
    than += "\n## 20. Quy tắc đang hiệu lực — bảng định tuyến ADR\n\n"
    than += "| ADR | luật | trạng thái | cổng đã ĐO |\n|---|---|---|---|\n"
    for so in hang_bang:
        than += f"| `ADR-{so}` | luật {so} | Accepted | 0 cổng |\n"
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(than, encoding="utf-8", newline="\n")
    return r


def case_adr_song_hai_tep_cung_so_thi_do(c: Ctx):
    """FINDING CODEX P2, PR #233 — hai tệp cùng số bị gom thành một, cổng báo sạch.

    Ca này là phản chứng ĐÃ CHẠY TRƯỚC KHI VÁ, không phải viết sau cho đẹp: bản
    cũ trả `rc=0` và in "1 ADR trên đĩa" trong khi đĩa có 2 tệp.
    """
    r = _repo_adr_ten(c.tmp, ["0001-goc.md", "0001-ban-sao-len-lut.md"], ["0001"], "trungso")
    rc, o, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "hai tệp cùng số ADR phải ĐỎ")
    if "2 tệp cùng số" not in _txt(e):
        raise AssertionError(f"thông điệp phải nói ra CẢ HAI tệp; được: {_txt(e)!r}")


def case_adr_song_ten_tep_la_thi_do(c: Ctx):
    """Tên lệch dạng là trạng thái THỨ BA (`không đo được`), không phải `bỏ qua`.

    Bản cũ lọc `f.name[:4].isdigit()`, nên `045-thieu-mot-so.md` — một ADR đặt tên
    sai — biến mất KHÔNG DẤU VẾT và cổng vẫn xanh. Cùng họ với bộ quét secrets lọc
    theo phần mở rộng rồi mù với `.env`.
    """
    r = _repo_adr_ten(c.tmp, ["0001-ok.md", "045-thieu-mot-so.md"], ["0001"], "tenla")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "tên tệp lệch dạng phải ĐỎ, không được bỏ qua êm")


def case_adr_song_thu_muc_con_thi_do(c: Ctx):
    """Một thư mục con trong `docs/adr/` có thể GIẤU ADR — không phân loại được thì ĐỎ."""
    r = _repo_adr_ten(c.tmp, ["0001-ok.md"], ["0001"], "thumuccon", thu_muc_con="kho-luu")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "thư mục con không phân loại được phải ĐỎ")


def case_adr_song_readme_duoc_tha(c: Ctx):
    """Chiều BẮT OAN: `README.md` cố ý không phải ADR, và nó nằm trong danh sách CHO PHÉP.

    Không có ca này thì không phân biệt được "bó dạng tên" với "cấm mọi tệp không
    phải ADR" — và cổng báo động giả là cổng sẽ bị tắt.
    """
    r = _repo_adr_ten(c.tmp, ["0001-ok.md", "README.md"], ["0001"], "readme")
    rc, o, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "README.md trong danh sách cho phép phải XANH")
    if "1 ADR trên đĩa" not in _txt(o):
        raise AssertionError(f"README không được tính là ADR; được: {_txt(o)!r}")

# --- (d3) adr-song: vùng KHÔNG RENDER và BIÊN của dạng tên tệp -----------------
#
# Sinh từ lượt cross-review THỨ HAI (codex, hai P2 trên PR #233, head `d17019628f`).
# Cả hai đã tái hiện TRƯỚC khi vá: ba ca vùng-không-render đều trả `rc=0` trong khi
# bảng RENDER ra không có dòng nào.

_ADR_OK = "# ADR-0001 — ca thử\n\n- **Trạng thái:** Accepted (2026-08-22)\n"
_H20 = "## 20. Quy tắc đang hiệu lực — bảng định tuyến ADR\n\n"
_HDR = "| ADR | luật | trạng thái | cổng đã ĐO |\n|---|---|---|---|\n"
_ROW = "| `ADR-0001` | luật | Accepted | 0 cổng |\n"


def _repo_adr_tho(tmp: Path, ten, than_adr, than_proto, co_git=True):
    """Dựng kho giả với THÂN TỆP nguyên văn — để đặt metadata vào vùng không render."""
    r = tmp / f"repo_adrtho_{ten}"
    d = r / "docs" / "adr"
    d.mkdir(parents=True, exist_ok=True)
    if co_git:
        (r / ".git").mkdir(exist_ok=True)
    (d / "0001-ca-thu.md").write_text(than_adr, encoding="utf-8", newline="\n")
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(
        "# Protocol giả\n\n## 19. Mục trước\n\n" + than_proto, encoding="utf-8", newline="\n")
    return r


def case_adr_song_dong_bang_trong_khoi_ma_khong_tinh(c: Ctx):
    """Dòng bảng chỉ nằm giữa ``` ``` ⇒ bảng RENDER ra không có nó ⇒ phải ĐỎ."""
    r = _repo_adr_tho(c.tmp, "fence", _ADR_OK, _H20 + _HDR + "```\n" + _ROW + "```\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "dòng bảng trong khối mã KHÔNG phải metadata sống")


def case_adr_song_dong_bang_trong_comment_html_khong_tinh(c: Ctx):
    r = _repo_adr_tho(c.tmp, "cmt", _ADR_OK, _H20 + _HDR + "<!--\n" + _ROW + "-->\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "dòng bảng trong comment HTML KHÔNG phải metadata sống")


def case_adr_song_trang_thai_trong_khoi_ma_khong_tinh(c: Ctx):
    """Chiều thứ hai: `Trạng thái` của chính tệp ADR nằm trong khối mã."""
    r = _repo_adr_tho(c.tmp, "adrfence",
                      "# ADR-0001 — ca thử\n\nVí dụ:\n\n```\n- **Trạng thái:** Accepted\n```\n",
                      _H20 + _HDR + _ROW)
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "`Trạng thái` trong khối mã KHÔNG phải trường thật")


def case_adr_song_rao_khong_dong_thi_do(c: Ctx):
    """Rào hỏng phải FAIL-CLOSE: nó nuốt mọi metadata phía sau."""
    r = _repo_adr_tho(c.tmp, "raohong", _ADR_OK, _H20 + _HDR + _ROW + "```\nchưa đóng\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "rào khối mã không đóng phải ĐỎ, không được che im lặng")


def case_adr_song_comment_khong_dong_thi_do(c: Ctx):
    r = _repo_adr_tho(c.tmp, "cmthong", _ADR_OK, _H20 + _HDR + _ROW + "<!-- chưa đóng\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "comment HTML không đóng phải ĐỎ")


def case_adr_song_khoi_ma_HOP_LE_van_xanh(c: Ctx):
    """Chiều BẮT OAN — và ca này KHÔNG thừa: §20 thật CÓ một khối mã.

    Nếu che vùng không-render mà làm hỏng ca này thì bản vá đã giết chính §20 nó
    sinh ra để canh.
    """
    r = _repo_adr_tho(c.tmp, "fenceok", _ADR_OK,
                      _H20 + "```\npython3 .claude/dev/packet_loop.py adr-song --root .\n```\n\n"
                      + _HDR + _ROW)
    rc, o, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "khối mã hợp lệ không chứa metadata thì phải XANH")


def case_adr_song_bien_dau_noi_cua_ten_tep(c: Ctx):
    """Biên của `_ADR_TEN_TEP`, và văn bản phải khai ĐÚNG cái mã làm.

    Codex (P2 lượt 2): dạng quảng cáo `^\\d{4}-[0-9a-z-]+\\.md$` nhận
    `0046--draft.md` và `0046-draft-.md`, mã thì từ chối. Đã chọn GIỮ mã chặt và
    sửa văn bản; ca này khoá cả BA biên để lần sau đổi bên nào cũng phải đổi có ý thức.
    """
    for ten_tep, doi in (("0046--draft.md", 9), ("0046-draft-.md", 9), ("0046-a--b.md", 0)):
        r = c.tmp / f"repo_bien_{ten_tep.replace('.', '_')}"
        d = r / "docs" / "adr"
        d.mkdir(parents=True, exist_ok=True)
        (r / ".git").mkdir(exist_ok=True)
        (d / "0001-ca-thu.md").write_text(_ADR_OK, encoding="utf-8", newline="\n")
        (d / ten_tep).write_text("# ADR-0046 — x\n\n- **Trạng thái:** Accepted\n",
                                 encoding="utf-8", newline="\n")
        (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(
            "# Protocol giả\n\n## 19. T\n\n" + _H20 + _HDR + _ROW
            + "| `ADR-0046` | luật | Accepted | 0 cổng |\n", encoding="utf-8", newline="\n")
        rc, _, e = run(c.script, ["adr-song", "--root", r])
        if rc != doi:
            raise AssertionError(f"{ten_tep}: đòi rc={doi}, được {rc}; {_txt(e)[:200]}")


def case_adr_song_thong_diep_loi_IN_RA_chinh_regex(c: Ctx):
    """Văn bản mô tả dạng tên phải SINH TỪ mã, không chép tay.

    Đây là chốt chống trôi cho đúng finding trên: nếu ai đổi `_ADR_TEN_TEP` mà
    quên sửa mọi chỗ mô tả nó, ít nhất thông điệp lỗi vẫn nói đúng sự thật.
    """
    r = _repo_adr_tho(c.tmp, "indregex", _ADR_OK, _H20 + _HDR + _ROW)
    (r / "docs" / "adr" / "045-lech.md").write_text("# x\n", encoding="utf-8", newline="\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "tên lệch dạng phải ĐỎ")
    s = _txt(e)
    if "[0-9a-z]" not in s or "d{4}" not in s:
        raise AssertionError(f"thông điệp phải IN RA chính regex; được: {s[:300]!r}")

# --- (d3) adr-song: rào MỞ và rào ĐÓNG không cùng luật ------------------------
#
# FINDING cross-review lượt 3 (codex, P2 trên head `ef19e3b075`). Bản trước khớp
# rào bằng TIỀN TỐ cho cả hai chiều, nên `"```not-a-close"` bị tính là rào ĐÓNG.
# Codex dựng chuỗi xen kẽ — mở · `"```not-a-close"` · dòng bảng GIẢ · hai rào nữa
# — và `adr-song` trả `rc=0` trong khi Markdown RENDER giữ dòng giả trong khối mã.
# Đã tái hiện TRƯỚC khi vá.
#
# Bốn ca dưới đây đo BỐN vế khác nhau, và hai trong bốn kéo cổng theo hai hướng
# NGƯỢC nhau — đó là lý do không gộp được thành một regex:
#   · đóng phải có đuôi khoảng trắng  ⇒ cổng CHẶT hơn
#   · backtick mở có backtick trong info thì không mở ⇒ cổng RỘNG hơn

_RAO_B = "`" * 3
_RAO_T = "~" * 3
_HANG_ADR = "| `ADR-0001` | luật | Accepted | 0 cổng |\n"
_BANG_DAU = "| ADR | luật | trạng thái | cổng đã ĐO |\n|---|---|---|---|\n"


def _repo_adr_than20(tmp: Path, than_20: str, ten: str):
    """Kho giả một ADR, và §20 với THÂN do ca tự soạn (để dựng rào)."""
    r = tmp / f"repo_than20_{ten}"
    d = r / "docs" / "adr"
    d.mkdir(parents=True, exist_ok=True)
    (r / ".git").mkdir(exist_ok=True)
    (d / "0001-ok.md").write_text(
        "# ADR-0001 — ca thử\n\n- **Trạng thái:** Accepted (2026-08-22)\n",
        encoding="utf-8", newline="\n")
    # TIÊU ĐỀ + DÒNG PHÂN CÁCH là bắt buộc: từ bản vá "dòng bảng phải THUỘC một
    # bảng", một dòng `|…|` trần KHÔNG được tính nữa. Fixture cũ viết khi dòng trần
    # còn được đếm, và hai ca đã ĐỎ đúng lúc bản vá vào — đó là bộ test làm việc,
    # không phải hồi quy.
    # Mỗi ca tự đặt TIÊU ĐỀ + DÒNG PHÂN CÁCH đúng chỗ. Từ bản vá "dòng bảng phải
    # THUỘC một bảng", một dòng `|…|` trần không được tính — nên VỊ TRÍ của tiêu đề
    # so với cấu trúc đang thử LÀ một phần của phép đo, không phải khung nền.
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(
        "# Protocol giả\n\n## 19. Mục trước\n\n"
        "## 20. Quy tắc đang hiệu lực — bảng định tuyến ADR\n\n" + than_20,
        encoding="utf-8", newline="\n")
    return r


def case_adr_song_rao_xen_ke_hang_gia_trong_khoi_ma(c: Ctx):
    """CA CỦA CODEX, nguyên trạng: rào xen kẽ đẩy dòng bảng giả ra ngoài vùng che."""
    than = (f"{_BANG_DAU}{_RAO_B}\n{_RAO_B}not-a-close\n{_HANG_ADR}{_RAO_B}\n{_RAO_B}\n")
    r = _repo_adr_than20(c.tmp, than, "xenke")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "dòng bảng nằm TRONG khối mã không được tính là phủ")


def case_adr_song_rao_dong_hop_le_van_che_dung(c: Ctx):
    """Chiều BẮT OAN: rào đóng ĐÚNG luật (chỉ khoảng trắng sau) vẫn phải đóng.

    Không có ca này thì "siết rào đóng" có thể siết thành KHÔNG BAO GIỜ đóng, và
    mọi §20 có khối mã sẽ đỏ oan — kể cả §20 thật, vốn CÓ một khối mã.
    """
    # rào chứa RÁC (không phải dòng bảng), đóng ĐÚNG luật; bảng thật nằm SAU nó.
    # Rào không đóng được ⇒ bảng bị che ⇒ ĐỎ. Đóng được ⇒ XANH.
    than = f"{_RAO_B}\nrác trong khối mã\n{_RAO_B}   \n{_BANG_DAU}{_HANG_ADR}"
    r = _repo_adr_than20(c.tmp, than, "donghople")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "rào đóng hợp lệ phải đóng; dòng bảng sau nó là dòng THẬT")


def case_adr_song_backtick_mo_co_backtick_trong_info(c: Ctx):
    """CommonMark: rào backtick mà info string chứa backtick thì KHÔNG mở khối nào.

    Nên dòng bảng phía sau là dòng THẬT — che nó đi là bắt oan.
    """
    # ```js`x KHÔNG mở khối mã ⇒ bảng ngay sau nó không bị che ⇒ XANH.
    than = f"{_RAO_B}js`x\n{_BANG_DAU}{_HANG_ADR}"
    r = _repo_adr_than20(c.tmp, than, "infobacktick")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "```js`x không mở khối mã ⇒ dòng bảng sau nó là THẬT")


def case_adr_song_nga_mo_info_co_backtick_van_che(c: Ctx):
    """Ngược lại: rào NGÃ thì info string tuỳ ý — `~~~ a`b` LÀ một rào mở hợp lệ.

    Cặp với ca trên: cùng một ký tự backtick trong info, hai loại rào, hai kết quả.
    Đo được cả hai mới chứng minh luật bó đúng theo LOẠI RÀO chứ không theo ký tự.
    """
    than = f"{_BANG_DAU}{_RAO_T} a`b\n{_HANG_ADR}{_RAO_T}\n"
    r = _repo_adr_than20(c.tmp, than, "ngainfo")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "~~~ a`b LÀ rào mở ⇒ dòng bảng trong nó phải bị che")

# --- (d4) dòng bảng chỉ được tính khi THUỘC MỘT BẢNG --------------------------
#
# Đây là ca đắt nhất của bộ này, và nó BÁC một lập luận tôi đã viết ra.
#
# Sau finding lượt 4 (`<pre>`), tôi lập luận với người giữ kho rằng có thể GIỮ
# NGUYÊN và chỉ khai giới hạn, vì chốt chính (N tệp = N dòng) vẫn bắt được rủi ro
# THẬT — "quên một dòng" — bất kể vùng không render. Rồi ĐO: dựng repo có 2 ADR,
# §20 chỉ có 1 dòng thật, và một dòng GIẢ cho đúng cái ADR đang thiếu đặt trong
# từng cấu trúc. SÁU/sáu dạng cho `rc=0`. Dòng giả LẤP CHỖ dòng bị quên.
#
# Lập luận sai, và cách nó sai đáng ghi: tôi suy ra "chỉ kẻ CỐ Ý mới khai thác
# được" từ hình dạng của lỗ, chứ không ĐO xem chốt chính có còn đứng không. Một
# mô hình đe doạ chưa đo là một lời khai, không phải một phép đo.
#
# Dạng đắt nhất KHÔNG có HTML nào: một dòng `|…|` đứng sau đoạn văn. GFM đòi
# header + dòng phân cách mới thành bảng, nên nó KHÔNG render thành hàng — mà bản
# trước vẫn đếm. Vậy lỗ chưa bao giờ là "HTML"; nó là chưa hỏi dòng ấy có thuộc
# một BẢNG không.
#
# Chữa Ở TẦNG: định vị bảng (tiêu đề + dòng phân cách) rồi chỉ đọc dòng `|` LIỀN
# MẠCH sau đó. Đóng cả MƯỜI dạng cùng lúc — bốn lỗ cross-review tìm ra và ba lỗ
# tôi tự khai — mà không thêm một bộ phân tích Markdown nào.

_HANG_GIA = "| `ADR-0002` | giả | Accepted | 0 cổng |\n"
_RAO3 = "`" * 3

# Mười dạng vùng-không-render, mỗi dạng đặt dòng GIẢ cho đúng ADR đang thiếu.
# Tên phải nói ra HÌNH DẠNG, để khi một ca đỏ thì biết ngay dạng nào hở.
LOP_VUNG_KHONG_RENDER = [
    ("pre",            f"<pre>\n{_HANG_GIA}</pre>\n"),
    ("div",            f"<div>\n{_HANG_GIA}</div>\n"),
    ("script",         f"<script>\n{_HANG_GIA}</script>\n"),
    ("textarea",       f"<textarea>\n{_HANG_GIA}</textarea>\n"),
    ("the_p",          f"<p>\n{_HANG_GIA}</p>\n"),
    ("dong_tran_sau_doan_van", f"Xem ví dụ:\n{_HANG_GIA}"),
    ("rao_backtick",   f"{_RAO3}\n{_HANG_GIA}{_RAO3}\n"),
    ("comment_html",   f"<!--\n{_HANG_GIA}-->\n"),
    ("khoi_ma_thut_le", "    " + _HANG_GIA),
    ("rao_trong_block_quote", f"> {_RAO3}\n> {_HANG_GIA}> {_RAO3}\n"),
]


def _repo_quen_dong(tmp: Path, chen: str, so_hang: int, ten: str):
    """2 ADR trên đĩa; §20 chỉ có `so_hang` dòng THẬT, cộng `chen` phía sau."""
    r = tmp / f"repo_quen_{ten}"
    d = r / "docs" / "adr"
    d.mkdir(parents=True, exist_ok=True)
    (r / ".git").mkdir(exist_ok=True)
    for n in ("0001", "0002"):
        (d / f"{n}-ok.md").write_text(
            f"# ADR-{n} — ca thử\n\n- **Trạng thái:** Accepted (2026-08-22)\n",
            encoding="utf-8", newline="\n")
    than = "| ADR | luật | trạng thái | cổng đã ĐO |\n|---|---|---|---|\n"
    for n in ["0001", "0002"][:so_hang]:
        than += f"| `ADR-{n}` | luật {n} | Accepted | 0 cổng |\n"
    (r / "docs" / "PROTOCOL_DA_PHIEN.md").write_text(
        "# Protocol giả\n\n## 19. Mục trước\n\n"
        "## 20. Quy tắc đang hiệu lực — bảng định tuyến ADR\n\n" + than + "\n" + chen,
        encoding="utf-8", newline="\n")
    return r


def _ca_quen_dong(chen: str, ten: str):
    def ca(c: Ctx):
        r = _repo_quen_dong(c.tmp, chen, 1, ten)
        rc, _, e = run(c.script, ["adr-song", "--root", r])
        _doi(9, rc, e, f"dòng giả trong `{ten}` LẤP CHỖ dòng bị quên — phải ĐỎ")
    return ca


def case_adr_song_trang_thai_rao_xen_ke_khong_tinh(c: Ctx):
    """Luật rào đóng vẫn là lớp DUY NHẤT ở phía TỆP ADR — đo tại đó.

    Bên §20 thì tầng "dòng bảng phải thuộc một bảng" đã bao trùm luật rào, nên
    một đột biến rào không còn giết được ca bên ấy. Nhưng tệp ADR KHÔNG có bảng
    nào để neo vào: dòng `Trạng thái` chỉ được che bởi `_che_khong_render`. Nếu
    nhận nhầm rào đóng thì dòng `Trạng thái` trong khối mã lại được tính là thật.
    """
    r = _repo_adr_ten(c.tmp, [], ["0001"], "ttraoxenke")
    (r / "docs" / "adr").mkdir(parents=True, exist_ok=True)
    (r / "docs" / "adr" / "0001-ok.md").write_text(
        "# ADR-0001 — ca thử\n\n"
        + _RAO_B + "\n" + _RAO_B + "not-a-close\n"
        + "- **Trạng thái:** Accepted (2026-08-22)\n"
        + _RAO_B + "\n" + _RAO_B + "\n",
        encoding="utf-8", newline="\n")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(9, rc, e, "dòng `Trạng thái` nằm trong khối mã không được tính là thật")


def case_adr_song_du_dong_that_van_xanh(c: Ctx):
    """Chiều BẮT OAN của cả lớp trên: bảng đủ dòng thì XANH."""
    r = _repo_quen_dong(c.tmp, "", 2, "duhang")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "bảng đủ dòng thật phải XANH")


def case_adr_song_pre_vo_hai_khong_bat_oan(c: Ctx):
    """Bảng đủ dòng, và §20 có một `<pre>` KHÔNG chứa dòng ADR nào — phải XANH.

    Không có ca này thì "chỉ đọc dòng trong bảng" có thể siết thành "từ chối mọi
    §20 có HTML", và §20 thật sẽ đỏ oan.
    """
    r = _repo_quen_dong(c.tmp, "<pre>\nvi du\n</pre>\n", 2, "prevohai")
    rc, _, e = run(c.script, ["adr-song", "--root", r])
    _doi(0, rc, e, "<pre> không chứa dòng ADR không được làm cổng đỏ")

# --- (d) adr-song ---
CASES += [
    ("adr_song_sach_xanh", case_adr_song_sach_xanh),
    ("adr_song_thieu_dong_thi_do", case_adr_song_thieu_dong_thi_do),
    ("adr_song_con_tro_chet_thi_do", case_adr_song_con_tro_chet_thi_do),
    ("adr_song_trung_dong_thi_do", case_adr_song_trung_dong_thi_do),
    ("adr_song_thieu_trang_thai_thi_do", case_adr_song_thieu_trang_thai_thi_do),
    ("adr_song_ngoai_le_0016_van_xanh", case_adr_song_ngoai_le_0016_van_xanh),
    ("adr_song_van_xuoi_khong_tinh_la_dong", case_adr_song_van_xuoi_khong_tinh_la_dong),
    ("adr_song_thieu_muc20_thi_do", case_adr_song_thieu_muc20_thi_do),
    ("adr_song_kho_that_thieu_thu_muc_thi_do", case_adr_song_kho_that_thieu_thu_muc_thi_do),
    ("adr_song_ban_sao_roi_duoc_tha", case_adr_song_ban_sao_roi_duoc_tha),
    ("adr_song_KHO_THAT_xanh", case_adr_song_KHO_THAT_xanh),
    ("adr_song_hai_tep_cung_so_thi_do", case_adr_song_hai_tep_cung_so_thi_do),
    ("adr_song_ten_tep_la_thi_do", case_adr_song_ten_tep_la_thi_do),
    ("adr_song_thu_muc_con_thi_do", case_adr_song_thu_muc_con_thi_do),
    ("adr_song_readme_duoc_tha", case_adr_song_readme_duoc_tha),
    ("adr_song_dong_bang_trong_khoi_ma_khong_tinh", case_adr_song_dong_bang_trong_khoi_ma_khong_tinh),
    ("adr_song_dong_bang_trong_comment_html_khong_tinh", case_adr_song_dong_bang_trong_comment_html_khong_tinh),
    ("adr_song_trang_thai_trong_khoi_ma_khong_tinh", case_adr_song_trang_thai_trong_khoi_ma_khong_tinh),
    ("adr_song_rao_khong_dong_thi_do", case_adr_song_rao_khong_dong_thi_do),
    ("adr_song_comment_khong_dong_thi_do", case_adr_song_comment_khong_dong_thi_do),
    ("adr_song_khoi_ma_HOP_LE_van_xanh", case_adr_song_khoi_ma_HOP_LE_van_xanh),
    ("adr_song_bien_dau_noi_cua_ten_tep", case_adr_song_bien_dau_noi_cua_ten_tep),
    ("adr_song_thong_diep_loi_IN_RA_chinh_regex", case_adr_song_thong_diep_loi_IN_RA_chinh_regex),
    ("adr_song_rao_xen_ke_hang_gia_trong_khoi_ma", case_adr_song_rao_xen_ke_hang_gia_trong_khoi_ma),
    ("adr_song_rao_dong_hop_le_van_che_dung", case_adr_song_rao_dong_hop_le_van_che_dung),
    ("adr_song_backtick_mo_co_backtick_trong_info", case_adr_song_backtick_mo_co_backtick_trong_info),
    ("adr_song_nga_mo_info_co_backtick_van_che", case_adr_song_nga_mo_info_co_backtick_van_che),
    ("adr_song_trang_thai_rao_xen_ke_khong_tinh", case_adr_song_trang_thai_rao_xen_ke_khong_tinh),
    ("adr_song_du_dong_that_van_xanh", case_adr_song_du_dong_that_van_xanh),
    ("adr_song_pre_vo_hai_khong_bat_oan", case_adr_song_pre_vo_hai_khong_bat_oan),
]
# Mười dạng vùng-không-render, mỗi dạng MỘT ca có tên riêng — để một đột biến chỉ
# giết đúng dạng nó làm hở, không gộp thành một chỗ chết chung.
CASES += [(f"adr_song_quen_dong_{ten}", _ca_quen_dong(chen, ten))
          for ten, chen in LOP_VUNG_KHONG_RENDER]
CASES += [
]

# AC 18 — mỗi lớp trong danh sách đóng thành MỘT ca có tên riêng, để đột biến
# tương ứng giết được ĐÚNG ca đó. Gộp cả bảng vào một ca sẽ làm mọi đột biến
# giết cùng một chỗ, và khi ấy phép tự chứng minh không rỗng mất hết độ phân giải.
CASES += [(f"ac18_{ten}", _ca_doctrine(nd, f"ac18_{ten}", 6)) for ten, nd in LOP_LACH]
# AC 19 — chiều BẮT OAN, cùng cách tổ chức.
CASES += [(f"ac19_{ten}", _ca_doctrine(nd, f"ac19_{ten}", 0)) for ten, nd in LOP_BAT_OAN]

# Đột biến nới ngưỡng: mỗi cái BẮT BUỘC giết đúng những ca dưới đây. Ca không
# chết được nghĩa là nó không đo cái nó khai.
MUTANTS = {
    "wp320_overwrite_diagnostic": (
        "    if d is not None and (not isinstance(d, dict) or not {\"thieu_bat_buoc\", \"chua_xac_thuc\", \"he_dieu_hanh\"} <= d.keys()):\n",
        "    if not isinstance(d, dict) or not {\"thieu_bat_buoc\", \"chua_xac_thuc\", \"he_dieu_hanh\"} <= d.keys():\n",
        ["wp320_invalid_inputs"],
    ),
    # --- dòng bảng phải THUỘC một bảng: đột biến dựng lại bản cũ -----------------
    #
    # Bản cũ đếm mọi dòng khớp `^| \`ADR-NNNN\` |` ở cột 0, bất kể nó có nằm trong
    # bảng hay không. Đột biến này khôi phục ĐÚNG cơ chế ấy, nên nó phải giết SẠCH
    # mười ca `quen_dong_*` — mỗi ca một hình dạng vùng-không-render.
    "adr_dem_moi_dong_giong_hang_bang": (
        "    trong_bang: list[str] = _hang_adr_trong_bang(than)\n",
        "    trong_bang: list[str] = _ADR_O_DAU_CU.findall(than)   # đột biến: bản cũ\n",
        # ĐO ĐƯỢC, không kê tay: chạy đột biến rồi lấy đúng những ca trả rc=0.
        # SÁU, không phải mười — bốn dạng còn lại (`rao_backtick`, `comment_html`,
        # `khoi_ma_thut_le`, `rao_trong_block_quote`) được bảo vệ bởi lớp KHÁC
        # (che vùng không render, và neo `^|` ở cột 0), nên gỡ tầng bảng không
        # làm chúng hở. Khai đúng sáu là khai đúng TẦNG NÀO che DẠNG NÀO.
        ["adr_song_quen_dong_pre", "adr_song_quen_dong_div",
         "adr_song_quen_dong_script", "adr_song_quen_dong_textarea",
         "adr_song_quen_dong_the_p",
         "adr_song_quen_dong_dong_tran_sau_doan_van"],
    ),
    # Chiều BẮT OAN: siết dòng phân cách thành "không bao giờ khớp" ⇒ không tìm
    # thấy bảng nào ⇒ bảng THẬT chết. Đo rằng phép định vị bảng đang thực sự
    # định vị, chứ không phải tình cờ đúng.
    "adr_bang_khong_bao_gio_khop": (
        '_ADR_BANG_PHAN_CACH = re.compile(r"^\\|[\\s:|-]+\\|\\s*$")\n',
        '_ADR_BANG_PHAN_CACH = re.compile(r"^KHONG_BAO_GIO_KHOP$")  # đột biến\n',
        ["adr_song_du_dong_that_van_xanh", "adr_song_pre_vo_hai_khong_bat_oan"],
    ),
    # --- rào MỞ / rào ĐÓNG: hai luật, hai đột biến ------------------------------
    #
    # (1) DỰNG LẠI ĐÚNG BUG lượt 3: khớp rào đóng bằng TIỀN TỐ. Không phải "gỡ một
    # chốt" mà là khôi phục nguyên văn cơ chế cũ — ai vô tình viết lại như cũ thì ca
    # của codex ĐỎ ngay.
    "adr_dong_rao_khop_tien_to": (
        "            mc = _RAO_DONG.match(d)\n",
        "            mc = _RAO_MO.match(d)   # đột biến: khớp tiền tố như bản cũ\n",
        # Ca bên §20 nay được tầng bảng bao trùm nên không chết nữa; luật rào
        # chỉ còn là lớp DUY NHẤT ở phía tệp ADR, nên đo tại đó.
        ["adr_song_trang_thai_rao_xen_ke_khong_tinh"],
    ),
    # (2) Chiều NGƯỢC: bỏ luật "backtick trong info thì không mở". Ca đích là ca
    # BẮT OAN, nên đột biến này chứng minh luật ấy đang nới cổng đúng chỗ.
    "adr_bo_luat_backtick_trong_info": (
        '            if m and not (m.group(1)[0] == "`" and "`" in m.group(2)):\n',
        "            if m:                   # đột biến: bỏ luật info string\n",
        ["adr_song_backtick_mo_co_backtick_trong_info"],
    ),
    # --- adr-song: đột biến cho lượt cross-review THỨ HAI ------------------------
    #
    # (1) BỎ che vùng không-render — dựng lại nguyên văn bệnh codex bắt được.
    #
    # Danh sách phải-chết ĐO LẠI sau khi có tầng bảng (`_hang_adr_trong_bang`): HAI,
    # không phải bốn. Hai ca "dòng bảng nằm trong vùng không render" nay được HAI
    # đường cùng phủ — che vùng, và luật "dòng phải nằm trong khối `|` liền mạch
    # ngay sau bảng" — nên gỡ MỘT đường thì ca vẫn xanh. Đó KHÔNG phải ca yếu: đúng
    # hình dạng mà `_cap_thay_the` mô tả, và lượt 7 đã cấm khai ngoại lệ cho nó. Hai
    # ca ấy chuyển sang đột biến PHỐI HỢP ngay dưới.
    #
    # Hai ca rào/comment KHÔNG ĐÓNG thì ở lại đây, vì che vùng là đường DUY NHẤT
    # phủ chúng — tầng bảng không biết gì về một cái rào hỏng.
    "adr_bo_che_vung_khong_render": (
        '    raw, van_de = _che_khong_render(proto.read_text(encoding="utf-8"))\n',
        '    raw, van_de = proto.read_text(encoding="utf-8"), []   # đột biến\n',
        ["adr_song_rao_khong_dong_thi_do", "adr_song_comment_khong_dong_thi_do"],
    ),
    # (1b) PHỐI HỢP — gỡ ĐÚNG hai đường cùng phủ, không gỡ thêm gì. Danh sách 12 ca
    # là ĐO ĐƯỢC (chạy đột biến rồi lấy đúng những ca đổi màu), không kê tay.
    "adr_bo_ca_hai_duong_phu_vung_khong_render": (
        ('    raw, van_de = _che_khong_render(proto.read_text(encoding="utf-8"))\n',
         "    trong_bang: list[str] = _hang_adr_trong_bang(than)\n"),
        ('    raw, van_de = proto.read_text(encoding="utf-8"), []   # đột biến\n',
         "    trong_bang: list[str] = _ADR_O_DAU_CU.findall(than)   # đột biến\n"),
        ["adr_song_dong_bang_trong_khoi_ma_khong_tinh",
         "adr_song_dong_bang_trong_comment_html_khong_tinh",
         "adr_song_rao_khong_dong_thi_do", "adr_song_comment_khong_dong_thi_do",
         "adr_song_quen_dong_pre", "adr_song_quen_dong_div",
         "adr_song_quen_dong_script", "adr_song_quen_dong_textarea",
         "adr_song_quen_dong_the_p", "adr_song_quen_dong_dong_tran_sau_doan_van",
         "adr_song_quen_dong_rao_backtick", "adr_song_quen_dong_comment_html"],
    ),
    # (2) Chỉ bỏ che ở phía TỆP ADR — tách khỏi (1) để biết đúng phía nào hở.
    "adr_bo_che_o_phia_tep_adr": (
        '        than_adr, vd = _che_khong_render(f.read_text(encoding="utf-8"))\n',
        '        than_adr, vd = f.read_text(encoding="utf-8"), []   # đột biến\n',
        ["adr_song_trang_thai_trong_khoi_ma_khong_tinh"],
    ),
    # (3) Rào hỏng thành "che êm tới hết tệp" thay vì ĐỎ — fail-open kinh điển.
    "adr_rao_hong_khong_do": (
        '        van_de.append(f"rào khối mã mở ở dòng {rao_dong} không được đóng")\n',
        '        pass                              # đột biến: rào hỏng không ĐỎ\n',
        ["adr_song_rao_khong_dong_thi_do"],
    ),
    # (4) Nới dạng tên tệp về đúng bản QUẢNG CÁO — ca biên phải ĐỎ.
    "adr_noi_ten_tep_ve_ban_quang_cao": (
        '_ADR_TEN_TEP = re.compile(r"^(\\d{4})-[0-9a-z]([0-9a-z-]*[0-9a-z])?\\.md$")',
        '_ADR_TEN_TEP = re.compile(r"^(\\d{4})-[0-9a-z-]+\\.md$")   # đột biến',
        ["adr_song_bien_dau_noi_cua_ten_tep"],
    ),
    # (5) Thông điệp lỗi quay về chuỗi CHÉP TAY — chốt chống trôi mất răng.
    "adr_thong_diep_chep_tay": (
        'f"{thu_muc}/{x}: không khớp {_ADR_TEN_TEP.pattern} và không thuộc "',
        'f"{thu_muc}/{x}: sai dạng tên và không thuộc "',
        ["adr_song_thong_diep_loi_IN_RA_chinh_regex"],
    ),
    # --- adr-song: ba đột biến của finding cross-review PR #233 ------------------
    #
    # (1) DỰNG LẠI ĐÚNG BUG. Không phải "gỡ một chốt" mà là khôi phục nguyên văn cơ
    # chế cũ — gom tệp vào dict theo bốn chữ số đầu. Đây là dạng đột biến mạnh nhất:
    # nếu ai đó vô tình viết lại như cũ, ca đích ĐỎ ngay.
    "adr_gom_map_de_bi_nuot": (
        "    for f in sorted(thu_muc.iterdir()):\n",
        "    for f in {x.name[:4]: x for x in sorted(thu_muc.glob('*.md'))}.values():\n",
        ["adr_song_hai_tep_cung_so_thi_do", "adr_song_thu_muc_con_thi_do"],
    ),
    # (2) Tha tên lệch dạng trong im lặng — đúng bệnh `f.name[:4].isdigit()` cũ.
    "adr_tha_ten_tep_la": (
        "    if la:\n",
        "    if False:                         # đột biến: bỏ qua tên lệch dạng\n",
        ["adr_song_ten_tep_la_thi_do", "adr_song_thu_muc_con_thi_do"],
    ),
    # (3) Chiều BẮT OAN: rỗng danh sách cho phép thì `README.md` bị bắt oan. Chứng
    # minh ca `readme_duoc_tha` đo danh sách CHO PHÉP chứ không đo thứ khác.
    "adr_rong_allowlist_ten_tep": (
        '_ADR_TEP_KHONG_PHAI_ADR = frozenset({"README.md"})\n',
        "_ADR_TEP_KHONG_PHAI_ADR = frozenset()   # đột biến: bắt oan\n",
        ["adr_song_readme_duoc_tha"],
    ),
    # --- adr-song: MỖI luật một đột biến riêng ---------------------------------
    #
    # ĐỐI CHỨNG KHÁC HỌ, nói cho đúng cơ chế: `_la_ho_doctrine` chỉ nhận tiền tố
    # `ac18_`/`ac19_`/`doctrine_`, nên tên `adr_song_*` rơi vào vế "không ca nào
    # thuộc họ doctrine" và đối chứng lấy là `DOI_CHUNG_DOCTRINE`. Đó ĐÚNG là điều
    # cần khẳng định ở đây — sửa `adr-song` không được đụng `doctrine-scan` — nên
    # phân loại này dùng được nguyên trạng; chỉ đừng đọc nó thành "adr thuộc họ máy
    # trạng thái".
    #
    # Sáu luật, sáu đột biến. Gộp lại thì mọi đột biến giết cùng một chỗ và phép
    # tự-chứng-minh-không-rỗng mất hết độ phân giải — đúng lý do `ac18` phải tách
    # từng lớp thành ca riêng.
    "adr_bo_kiem_thieu_dong": (
        "    for s in sorted(set(theo_so) - co):\n",
        "    for s in []:                      # đột biến: thôi đòi phủ đủ\n",
        ["adr_song_thieu_dong_thi_do", "adr_song_van_xuoi_khong_tinh_la_dong"],
    ),
    "adr_bo_kiem_con_tro_chet": (
        "    for s in sorted(co - set(theo_so)):\n",
        "    for s in []:                      # đột biến: thôi bắt con trỏ chết\n",
        ["adr_song_con_tro_chet_thi_do"],
    ),
    "adr_bo_kiem_trung_dong": (
        "    trung = sorted({s for s in trong_bang if trong_bang.count(s) > 1})\n",
        "    trung = []                        # đột biến: thôi bắt dòng trùng\n",
        ["adr_song_trung_dong_thi_do"],
    ),
    # Hình dạng đã trả giá ở `v1.36.68`: NỚI DANH SÁCH CHO PHÉP để chứa chính thứ
    # đang tấn công. Không có đột biến này thì không biết ca đích đang đo danh
    # sách hay đo thứ khác.
    "adr_noi_ngoai_le_cho_moi_ADR": (
        '_ADR_THA_THIEU_TRANG_THAI = frozenset({"0016"})\n',
        '_ADR_THA_THIEU_TRANG_THAI = frozenset({"0016", "0007"})  # đột biến: nới\n',
        ["adr_song_thieu_trang_thai_thi_do"],
    ),
    # Nhánh "không thấy thì bỏ qua" biến thành tha vô điều kiện — bệnh `t24`.
    # MỐC HAI DÒNG, không phải một: `if (root / ".git").exists():` khớp ĐÚNG HAI chỗ
    # (`cmd_adr_song` và `cmd_bien_nhan` dùng cùng một idiom "chỉ tha khi cây rời"), nên
    # mốc một dòng buộc phải khai ngoại lệ `count == 2` — và ngoại lệ ấy là CỬA cho mọi
    # mốc mơ hồ khác lọt qua. Kéo thêm đầu dòng `_die(RC_ADR, ` vào mốc là đủ phân biệt
    # (đo: 1 chỗ) ⇒ bảng ngoại lệ BỎ HẲN, phép kiểm đòi `== 1` vô điều kiện.
    "adr_tha_khi_thieu_thu_muc": (
        '        if (root / ".git").exists():\n            _die(RC_ADR, ',
        "        if False:                     # đột biến: kho thật cũng bỏ qua êm\n"
        "            _die(RC_ADR, ",
        ["adr_song_kho_that_thieu_thu_muc_thi_do"],
    ),
    # Nới phép nhận dòng bảng thành khớp cả VĂN XUÔI: cổng sẽ báo phủ đủ trong khi
    # bảng còn thiếu — chiều nguy hiểm hơn của cùng lỗi mà `t43` đã trả giá.
    #
    # MỎ NEO ĐỔI sau khi có tầng bảng: `_ADR_HANG` không còn tồn tại, nên đột biến
    # cũ mất mỏ neo và bộ test báo thẳng ra. Giữ một đột biến của mã đã chết là giữ
    # một phép đo không chạy, nên nó được RETARGET chứ không vá cho qua. Dạng tương
    # đương ở kiến trúc mới là gỡ HẲN phép định vị bảng rồi nhận mọi lần nhắc
    # `ADR-xxxx` ở bất kỳ đâu — đúng cách một người sẽ "sửa" khi cổng đỏ ở chỗ phiền.
    # Nó khác `adr_dem_moi_dong_giong_hang_bang` ở chỗ bỏ CẢ neo `^|`, nên hai đột
    # biến tách được "THUỘC VỀ một bảng" khỏi "TRÔNG GIỐNG một dòng bảng".
    #
    # Danh sách 9 ca là ĐO ĐƯỢC. Ba ca chiều BẮT OAN (`du_dong_that_van_xanh`,
    # `pre_vo_hai_khong_bat_oan`, `khoi_ma_HOP_LE_van_xanh`) đã kiểm là VẪN XANH —
    # đột biến này NỚI cổng, nên nó không được phép làm ca chiều tha đỏ.
    "adr_hang_nhan_ca_van_xuoi": (
        "    trong_bang: list[str] = _hang_adr_trong_bang(than)\n",
        '    trong_bang: list[str] = re.findall(r"`ADR-(\d{4})`", than)   # đột biến\n',
        ["adr_song_van_xuoi_khong_tinh_la_dong",
         "adr_song_quen_dong_pre", "adr_song_quen_dong_div",
         "adr_song_quen_dong_script", "adr_song_quen_dong_textarea",
         "adr_song_quen_dong_the_p", "adr_song_quen_dong_dong_tran_sau_doan_van",
         "adr_song_quen_dong_khoi_ma_thut_le",
         "adr_song_quen_dong_rao_trong_block_quote"],
    ),
    # Cùng họ với đột biến trên, nhưng RỘNG HƠN — đây là hình dạng generation 4:
    # tha cụm ấy VÔ ĐIỀU KIỆN, không cần ngắt dòng. Nói cách khác: "cứ cho hẳn cụm
    # này vào danh sách miễn". Đó là cách sửa mà người ta thật sự hay chọn khi gate
    # đỏ ở một chỗ phiền, nên nó đáng có đột biến riêng chứ không gộp vào cái trên.
    #
    # Nó phủ SÁU lớp mà đột biến ngắt-dòng KHÔNG với tới — `cum_don_heading`,
    # `dong_tran`, `gach_dau_dong`, `in_dam`, `dinh_nghia`, `cau_van_xuoi_mot_dong`
    # — vì cả sáu đặt cụm cấm GỌN TRONG MỘT DÒNG, mà miễn trừ ngắt dòng theo định
    # nghĩa không tha những ca ấy. Hai đột biến vì thế đo hai bề rộng khác nhau của
    # cùng một sai lầm, và bỏ cái nào cũng để lại một khoảng mù.
    #
    # Danh sách phải-chết ĐO ĐƯỢC: 43 ca, đúng bằng số ca của `LOP_LACH` có chứa cụm.
    "tha_vo_dieu_kien_nhu_generation_4": (
        "                tu = phang.find(kim)\n",
        ('                if cum in ("người có thẩm quyền",):\n'
         '                    tu = -1               # đột biến: tha VÔ ĐIỀU KIỆN\n'
         '                else:\n'
         '                    tu = phang.find(kim)\n'),
        [
         'ac18_cum_don_heading', 'ac18_cum_don_dong_tran',
         'ac18_cum_don_gach_dau_dong', 'ac18_cum_don_in_dam',
         'ac18_cum_don_dinh_nghia', 'ac18_cum_don_heading_ngat_dong',
         'ac18_cum_don_gach_dau_dong_ngat_dong', 'ac18_cum_don_danh_sach_so_ngat_dong',
         'ac18_cum_don_dong_tran_ngat_dong', 'ac18_cum_don_code_fence',
         'ac18_cum_don_code_fence_ngoac_song', 'ac18_cum_don_o_bang_html_ngat_dong',
         'ac18_cum_don_fence_trong_bullet', 'ac18_cum_don_fence_trong_trich_dan',
         'ac18_cum_don_o_bang_html_co_chu_hai_phia', 'ac18_cum_don_o_bang_html_khong_dong_the',
         'ac18_cum_don_chi_co_chu_truoc', 'ac18_cum_don_chi_co_chu_sau',
         'ac18_cum_don_wrapper_mot_chu_cai', 'ac18_cum_don_wrapper_chu_so',
         'ac18_cum_don_wrapper_trong_tag', 'ac18_cum_don_van_xuoi_khong_ke_phep_do',
         'ac18_cum_don_rao_dong_ngan_hon', 'ac18_cum_don_rao_dong_co_duoi',
         'ac18_cum_don_rao_song_dong_ngan_hon', 'ac18_cum_don_bang_html_long',
         'ac18_cum_don_bang_html_long_ba_cap', 'ac18_cum_don_trich_dan_ngat_dong',
         'ac18_cum_don_trich_dan_long_hai_cap', 'ac18_cum_don_heading_long_trich_dan',
         'ac18_cum_don_cau_van_xuoi_mot_dong', 'ac18_cum_don_claude_md_master_tha_cu',
         'ac18_cum_don_term_ngat_dong_tha_cu', 'ac18_cum_don_van_xuoi_ngat_dong_trong_bullet_tha_cu',
         'ac18_cum_don_van_xuoi_ngat_dong_trong_danh_sach_so_tha_cu', 'ac18_cum_don_van_xuoi_ngat_dong_trong_trich_dan_tha_cu',
         'ac18_cum_don_van_xuoi_sau_bang_html_tha_cu', 'ac18_cum_don_rao_dong_dung_luat_tha_cu',
         'ac18_cum_don_dong_thut_le_khong_phai_rao_tha_cu', 'ac18_cum_don_the_bang_trong_khoi_ma_tha_cu',
         'ac18_cum_don_the_bang_trong_ma_inline_tha_cu', 'ac18_cum_don_the_bang_trong_comment_tha_cu',
         'ac18_cum_don_van_xuoi_sau_bang_html_chua_dong_tha_cu',
        ],
    ),
    # --- ĐỘT BIẾN THAY CHO MƯỜI HAI ĐỘT BIẾN ĐÃ XOÁ ở revision 4 -------------------
    #
    # Mười hai đột biến cũ nhắm vào máy dò cấu trúc phục vụ MIỄN TRỪ (`_dong_khoi_ma`,
    # `_dong_bang_html`, `_DAU_HIEU_PHEP_DO`, `_RE_HANG_RAO`…). Revision 4 xoá hẳn máy
    # ấy, nên cả mười hai mất mỏ neo — giữ lại là giữ đột biến của mã không còn tồn tại.
    #
    # Thay bằng MỘT đột biến duy nhất, và nó mạnh hơn cả mười hai cộng lại: dựng LẠI
    # đúng cơ chế miễn trừ (tha khi cụm cấm chỉ xuất hiện qua ngắt dòng). Nếu ai đó mở
    # lại miễn trừ dưới bất kỳ hình thức nào, ca ở đây ĐỎ ngay.
    #
    # Danh sách phải-chết dưới đây ĐO ĐƯỢC, không kê tay: chạy scanner đã đột biến trên
    # từng ca của `LOP_LACH` rồi lấy đúng những ca trả rc=0. Ba mươi bảy ca — mười hai
    # ca vừa đổi ma trận, cộng hai mươi lăm ca ngắt dòng đã có từ trước. Con số lớn là
    # ĐÚNG chứ không phải đột biến nhắm sai tầng: miễn trừ vốn tha theo HÌNH DẠNG ngắt
    # dòng, nên mở lại nó thì mọi hình dạng ngắt dòng cùng lọt một lượt.
    "mo_lai_mien_tru_ngat_dong": (
        "                tu = phang.find(kim)\n",
        ("                if any(kim in _chuan_hoa(_d) for _s, _d in _dong_sau_khi_go(raw)):\n"
         "                    tu = phang.find(kim)      # đột biến: mở lại miễn trừ\n"
         "                else:\n"
         "                    tu = -1\n"),
        [
         'ac18_cum_don_heading_ngat_dong', 'ac18_cum_don_gach_dau_dong_ngat_dong',
         'ac18_cum_don_danh_sach_so_ngat_dong', 'ac18_cum_don_dong_tran_ngat_dong',
         'ac18_cum_don_code_fence', 'ac18_cum_don_code_fence_ngoac_song',
         'ac18_cum_don_o_bang_html_ngat_dong', 'ac18_cum_don_fence_trong_bullet',
         'ac18_cum_don_fence_trong_trich_dan', 'ac18_cum_don_o_bang_html_co_chu_hai_phia',
         'ac18_cum_don_o_bang_html_khong_dong_the', 'ac18_cum_don_chi_co_chu_truoc',
         'ac18_cum_don_chi_co_chu_sau', 'ac18_cum_don_wrapper_mot_chu_cai',
         'ac18_cum_don_wrapper_chu_so', 'ac18_cum_don_wrapper_trong_tag',
         'ac18_cum_don_van_xuoi_khong_ke_phep_do', 'ac18_cum_don_rao_dong_ngan_hon',
         'ac18_cum_don_rao_dong_co_duoi', 'ac18_cum_don_rao_song_dong_ngan_hon',
         'ac18_cum_don_bang_html_long', 'ac18_cum_don_bang_html_long_ba_cap',
         'ac18_cum_don_trich_dan_ngat_dong', 'ac18_cum_don_trich_dan_long_hai_cap',
         'ac18_cum_don_heading_long_trich_dan', 'ac18_cum_don_claude_md_master_tha_cu',
         'ac18_cum_don_term_ngat_dong_tha_cu', 'ac18_cum_don_van_xuoi_ngat_dong_trong_bullet_tha_cu',
         'ac18_cum_don_van_xuoi_ngat_dong_trong_danh_sach_so_tha_cu', 'ac18_cum_don_van_xuoi_ngat_dong_trong_trich_dan_tha_cu',
         'ac18_cum_don_van_xuoi_sau_bang_html_tha_cu', 'ac18_cum_don_rao_dong_dung_luat_tha_cu',
         'ac18_cum_don_dong_thut_le_khong_phai_rao_tha_cu', 'ac18_cum_don_the_bang_trong_khoi_ma_tha_cu',
         'ac18_cum_don_the_bang_trong_ma_inline_tha_cu', 'ac18_cum_don_the_bang_trong_comment_tha_cu',
         'ac18_cum_don_van_xuoi_sau_bang_html_chua_dong_tha_cu',
        ],
    ),
    "tran_attempt_3_thanh_99": (
        "MAC_DINH_TRAN_ATTEMPT = 3",
        "MAC_DINH_TRAN_ATTEMPT = 99",
        ["cap_lan_4_thoat_3"],
    ),
    "same_failure_2_thanh_99": (
        "MAC_DINH_TRAN_SAME_FAILURE = 2",
        "MAC_DINH_TRAN_SAME_FAILURE = 99",
        ["same_failure_cung_id_qua_2_review"],
    ),
    "bien_nhan_bo_gom_full_va_viet_tat": (
        "    khoa_theo_bien_nhan = _khoa_neo_cac_sha(that, root)\n",
        ('    khoa_theo_bien_nhan = []\n'
         '    for d in that:\n'
         '        s = str(d.get("reviewed_sha") or "").strip().lower()\n'
         '        khoa_theo_bien_nhan.append(s if _la_dang_commit(s) '
        'else "__khong_neo_duoc__")\n'),
        ["bien_nhan_cung_sha_full_va_viet_tat_dem_MOT"],
    ),
    "bien_nhan_khong_doc_object_format_thi_giu_hanh_vi_cu": (
        "        if p.returncode != 0:\n            return (40, 64)\n",
        ('        if p.returncode != 0:\n'
         '            _die(RC_BIEN_NHAN, "đột biến: hỏi object format lỗi thành chặn")\n'),
        ["bien_nhan_ban_sao_roi_co_du_lieu_van_dem_duoc"],
    ),
    "bien_nhan_khong_leo_len_kho_cha": (
        "            cung_goc = Path(dong_dau).resolve() == root.resolve()\n",
        "            cung_goc = True  # đột biến: bỏ phép so toplevel\n",
        ["bien_nhan_ban_sao_roi_duoi_sha256_cha_dem_MOT"],
    ),
    "bien_nhan_root_xuong_dong_tach_tu_trai": (
        '        ket_qua = p.stdout.removesuffix("\\n").rsplit("\\n", 1)\n',
        "        ket_qua = p.stdout.splitlines()\n", ["bien_nhan_sha256_root_xuong_dong_dem_MOT"]),
    "bien_nhan_root_xuong_dong_tha_vo_dieu_kien": (
        "        goc.mkdir()\n", '        raise BoQua("đột biến: tha vô điều kiện")\n',
        ["bien_nhan_sha256_root_xuong_dong_dem_MOT"]),
    "bien_nhan_shim_tha_vo_dieu_kien": (
        "        p = subprocess.run([str(git)], capture_output=True, check=True)\n",
        '        raise BoQua("đột biến: tha vô điều kiện")\n',
        ["bien_nhan_git_gia_duong_dan_nul_giu_fallback"]),
    # Hai chiều của CÙNG một vị từ, vì bản lượt 2 không có chiều nào: nới thành luôn-tha
    # (`if True:`) và siết thành luôn-tố (`if False:`). Cả hai PHẢI giết
    # `moc_kiem_TU_NO_co_rang`; nếu chỉ một chiều giết được thì ca ấy mới đo được nửa vị từ.
    # Cô lập git thành no-op ⇒ fixture ăn lại cấu hình toàn cục của máy chạy.
    "git_co_lap_tha_vo_dieu_kien": (
        "    env.update(_GIT_BIEN_CO_LAP)\n",
        "    pass  # đột biến: không cô lập gì\n",
        ["fixture_git_KHONG_an_config_toan_cuc"]),
    # Lùi về hình dạng GHIM KHOÁ của PR #342: vẫn ĐỌC config toàn cục, chỉ đè đúng khoá đã
    # nghĩ tới. Chiều (2) của ca vẫn xanh — đúng như vậy — nên chỉ chiều (3) giết nó, tức
    # chiều (3) đo được RIÊNG cái khác biệt "cắt nguồn" vs "ghim khoá".
    # Bỏ đúng bước xoá kênh PHẠM VI LỆNH — tức lùi về chính bản lượt 3, bản "cắt hai
    # trong ba nguồn". Nếu ca không chết thì chiều (4) chưa đo gì.
    "git_co_lap_bo_sot_pham_vi_lenh": (
        "    for k in [k for k in env if _la_cau_hinh_pham_vi_lenh(k)]:\n        del env[k]\n",
        "    pass  # đột biến: bỏ sót kênh cấu hình phạm vi lệnh\n",
        ["fixture_git_KHONG_an_config_toan_cuc"]),
    "git_co_lap_lui_ve_ghim_khoa": (
        '    "GIT_CONFIG_GLOBAL": os.devnull,\n    "GIT_CONFIG_SYSTEM": os.devnull,\n',
        '    "GIT_CONFIG_COUNT": "1",  # đột biến: ghim khoá thay vì cắt nguồn\n'
        '    "GIT_CONFIG_KEY_0": "commit.gpgsign",\n    "GIT_CONFIG_VALUE_0": "false",\n',
        ["fixture_git_KHONG_an_config_toan_cuc"]),
    "moc_kiem_noi_vo_dieu_kien": (
        "            if n == 1:\n",
        "            if True:   # đột biến: luôn tha, phép kiểm thành vô nghĩa\n",
        ["moc_kiem_TU_NO_co_rang"]),
    "moc_kiem_to_vo_dieu_kien": (
        "            if n == 1:\n",
        "            if False:  # đột biến: luôn tố, kể cả mốc khớp đúng 1 chỗ\n",
        ["moc_kiem_TU_NO_co_rang"]),
    "phan_loai_lai_dot_bien_test_bang_suy_luan": (
        "    dot_bien_test = ten_mut in MUTANTS_NHAM_TEST\n",
        "    dot_bien_test = all(t in goc_test for t, _ in cap)  # đột biến: suy từ văn bản\n",
        ["phan_loai_dot_bien_san_pham_neo_trung_test_van_DO"]),
    "bo_qua_html_guard_trong_trich_xuat": (
        "            if html_end:\n",
        "            if False:\n",
        ["trich_xuat_74a_chong_nhieu"]),
    "bien_nhan_bo_nhanh_valueerror": (
        "        except ValueError:\n", "        except RuntimeError:\n",
        ["bien_nhan_git_gia_duong_dan_nul_giu_fallback"]),
    "bien_nhan_valueerror_tai_indexing_phai_noi": (
        "        dong_dau = ket_qua[0]\n", '        raise ValueError("injected-indexing")\n',
        ["bien_nhan_git_gia_duong_dan_nul_giu_fallback"]),
    "bien_nhan_sha256_khong_nhan_40_la_oid_day_du": (
        '    return {"sha1": (40,), "sha256": (64,)}.get(ket_qua[1].strip(), (40, 64))\n',
        '    return (40, 64)  # đột biến: không phân biệt object format\n',
        ["bien_nhan_sha256_full64_va_tien_to40_dem_MOT"],
    ),
    "bien_nhan_gom_moi_oid_day_du": (
        "            khoa_theo_sha[sha] = ung_vien_day_du[0]\n",
        '            khoa_theo_sha[sha] = "__gom_moi_oid__"  # đột biến\n',
        ["bien_nhan_sha256_hai_oid_khac_nhau_dem_HAI"],
    ),
    "bien_nhan_tra_lai_safe_loader_doi_kieu": (
        '            d = yaml.load(f.read_text(encoding="utf-8"), Loader=yaml.BaseLoader)\n',
        '            d = yaml.safe_load(f.read_text(encoding="utf-8"))  # đột biến\n',
        ["bien_nhan_sha_so_co_0_dau_van_dem_RIENG"],
    ),
    "bien_nhan_bo_chan_tien_to_mo_ho": (
        "        if len(ung_vien_day_du) > 1:\n",
        "        if False:  # đột biến: tự chọn OID đầu tiên\n",
        ["bien_nhan_viet_tat_khop_hai_oid_la_KHONG_DO_DUOC"],
    ),
    "bo_cung_hoa_stdout": (
        "\n    _cung_hoa_stdout()\n",
        "\n    pass  # đột biến: bỏ cứng hoá stdout\n",
        ["stdout_cp1252", "stdout_cp1258"],
    ),
    # --- lease: dựng lại ĐÚNG bug gốc mà review cross-provider tìm ra.
    "init_tu_cap_lease_nhu_bug_goc": (
        '"state": "awaiting_lease",',
        '"state": "leased",',
        ["init_KHONG_duoc_tu_cap_lease"],
    ),
    "bo_chan_tu_cap_bang_ten_provider": (
        "    if nguoi_cap.lower() in PROVIDERS:",
        "    if False:",
        ["tu_cap_lease_bang_ten_provider_bi_chan"],
    ),
    # AC 21 đổi hình dạng chốt hạn: TRƯỚC có HAI phép kiểm rời nhau (một trong
    # `record-lease`, một trong `begin-attempt`) nên cần hai đột biến không phủ
    # nhau. Giờ chỉ còn MỘT phép kiểm trong hàm chung — đó chính là điều AC 21
    # đòi — nên một đột biến giết CẢ HAI ca là kết quả ĐÚNG, không phải mất độ
    # phân giải: hai ca vẫn đi qua hai đường gọi khác nhau (ghi lease / mở lượt).
    "bo_kiem_khoa_thua_trong_luoc_do_lease": (
        "    thua = [k for k in lease if k not in KHOA_LEASE]",
        "    thua = []",
        ["g9_lease_khoa_thua_bi_chan"],
    ),
    "bo_kiem_han_trong_ham_chung": (
        "    if han <= bay_gio:",
        "    if False:",
        ["lease_da_het_han_khong_ghi_duoc",
         "begin_attempt_sau_khi_lease_HET_HAN_bi_chan"],
    ),
    "bo_gioi_han_cua_so_han": (
        "    if (han - bay_gio).days > GIOI_HAN_HAN_NGAY:",
        "    if False:",
        ["ac21_expires_ngoai_cua_so"],
    ),
    # --- `lease-authority-spoof` P1 (cross-review lượt 4, codex, 14-08-2026) -----
    # Nới danh sách CHO PHÉP để chứa cả bốn tên tấn công: nếu ca đích VẪN xanh sau
    # khi danh sách nới ra, nghĩa là ca không thật sự đo danh sách cho phép — nó
    # đo thứ gì khác.
    "noi_danh_sach_cho_phep_chua_ten_gia_mao": (
        'NGUOI_CO_THAM_QUYEN = ("ducthangho",)',
        'NGUOI_CO_THAM_QUYEN = ("ducthangho", "codex-dispatcher", "ai-codex-bot", '
        '"cödex", "cödex")',
        ["lease_authority_ten_gia_mao_bi_chan"],
    ),
    # --- `partial-lease-authority-bypass` P1 (verdict lượt 5, PR #92) -----------
    # ĐỘT BIẾN SPEC ĐÒI: "tách hai chốt ra khỏi hàm chung ⇒ ca đích phải ĐỎ".
    # Thay lời gọi hàm chung bằng ĐÚNG phép tự kiểm rời rạc của bản trước — đòi
    # `lease` truthy VÀ có `expires_utc`, rồi kiểm hạn — không kiểm trọn lược đồ,
    # không kiểm kiểu, không kiểm lại thẩm quyền. Ca hạn VẪN xanh dưới đột biến
    # này, nên nó đo đúng cái nó khai: sự CHUNG NHAU của phép kiểm lược đồ.
    "tach_begin_attempt_khoi_ham_chung": (
        '    _kiem_luoc_do_lease(st.get("lease"), RC_STATE)',
        '    _l = st.get("lease")\n'
        '    if not _l or not _l.get("expires_utc"):\n'
        '        _die(RC_STATE, "đột biến: chốt riêng, không dùng hàm chung")\n'
        '    if _doc_han_utc(_l["expires_utc"]) <= datetime.now(timezone.utc):\n'
        '        _die(RC_STATE, "đột biến: lease hết hạn")',
        ["ac21_lease_chi_co_expires", "ac21_lease_thieu_tung_khoa",
         "ac21_lease_sai_kieu_khong_traceback", "ac21_khoa_sai_kieu_khong_traceback",
         "ac21_khoa_rong", "ac21_lease_tu_cap_trong_state", "ac21_hai_cua_CUNG_luoc_do"],
    ),
    "tra_ve_fail_open_thieu_lease": (
        '    _kiem_luoc_do_lease(st.get("lease"), RC_STATE)',
        '    _l = st.get("lease")\n'
        '    if _l and _l.get("expires_utc"):\n'
        '        _kiem_luoc_do_lease(_l, RC_STATE)',
        ["legacy_state_khong_co_lease_bi_chan"],
    ),
    # --- AC 18 · MỘT ĐỘT BIẾN CHO MỖI LỚP CHUẨN HOÁ -----------------------------
    # Gỡ RIÊNG từng lớp để chứng minh mỗi lớp thật sự cần thiết, và để ca của lớp
    # ấy chết ĐÚNG khi lớp ấy biến mất. Đây là phép tự chứng minh không rỗng ở độ
    # phân giải TỪNG LỚP — thứ mà năm vòng vá theo hình dạng trước đây không có.
    #
    # Đột biến spec đòi cho P1-A: "hạ NFKC về NFC ⇒ ca đích phải ĐỎ".
    "ha_NFKC_ve_NFC": (
        'unicodedata.normalize("NFKC", text)',
        'unicodedata.normalize("NFC", text)',
        ["ac18_nfkc_hai_cham_toan_rong", "ac18_nfkc_chu_toan_rong",
         "ac18_nfkc_chu_so_tron", "ac18_nfkc_chu_so_mu",
         "ac18_nfkc_solidus_toan_rong", "ac18_nfkc_gach_duoi_toan_rong",
         "ac18_nfkc_vach_dung_toan_rong"],
    ),
    "bo_loc_ky_tu_dinh_dang_Cf": (
        '    text = "".join(ch for ch in text if unicodedata.category(ch) != "Cf")\n',
        "",
        ["doctrine_scan_bat_zero_width_bi_chan", "ac18_cf_zwnj", "ac18_cf_zwj",
         "ac18_cf_word_joiner", "ac18_cf_soft_hyphen", "ac18_cf_bom"],
    ),
    "bo_giai_html_entity": (
        "    text = html.unescape(text)\n",
        "",
        ["doctrine_scan_bat_html_entity_bi_chan", "ac18_entity_thap_luc",
         "ac18_entity_co_ten", "ac18_entity_thieu_cham_phay"],
    ),
    "bo_gap_dong_tu": (
        ".translate(_DONG_TU)",
        "",
        ["ac18_dong_tu_cyrillic_e", "ac18_dong_tu_cyrillic_o",
         "ac18_dong_tu_hy_lap_o", "ac18_dong_tu_cyrillic_a"],
    ),
    "bo_gap_mui_ten": (
        ".translate(_MUI_TEN)",
        "",
        ["ac18_mui_ten_dai"],
    ),
    "bo_bo_trang_tri_va_nhay": (
        ".translate(_BO_HAN)",
        "",
        ["ac18_nhay_cong_xen_giua"],
    ),
    "bo_gop_phan_cach": (
        ".translate(_PHAN_CACH)",
        "",
        ["ac18_phan_cach_en_dash", "ac18_phan_cach_hyphen"],
    ),
    # Gỡ tag/comment nay nằm TRỌN ở `_dong_sau_khi_go` — tầng duy nhất thấy được
    # cấu trúc trải nhiều dòng. Đột biến vì thế bỏ từng regex khỏi vòng lặp ở đó.
    "bo_go_tag_html": (
        "    for rx in (_RE_COMMENT_HTML, _RE_TAG_HTML):",
        "    for rx in (_RE_COMMENT_HTML,):",
        ["ac18_tag_html_xen_giua", "ac18_tag_thuoc_tinh_nhay_kep",
         "ac18_tag_thuoc_tinh_nhay_don", "ac18_tag_thuoc_tinh_dau_nho_hon",
         "ac18_tag_ngat_qua_dong"],
    ),
    "bo_go_comment_html": (
        "    for rx in (_RE_COMMENT_HTML, _RE_TAG_HTML):",
        "    for rx in (_RE_TAG_HTML,):",
        ["ac18_comment_html_xen_giua", "ac18_comment_html_ngat_qua_dong"],
    ),
    # Trả regex tag về dạng CẤM KÝ TỰ theo vị trí của generation 4 ⇒ mọi lớp
    # thuộc-tính-có-nháy phải ĐỎ lại, còn tag thường vẫn xanh.
    "tra_regex_tag_ve_cam_ky_tu": (
        'r"""(?:\\s+(?:"[^"]*"|\'[^\']*\'|[^>"\'])*)?"""  # thuộc tính: nháy kép | nháy đơn | ký tự thường',
        'r"""(?:\\s[^<>]*)?"""',
        ["ac18_tag_thuoc_tinh_nhay_kep", "ac18_tag_thuoc_tinh_nhay_don",
         "ac18_tag_thuoc_tinh_dau_nho_hon"],
    ),
    "bo_ngoac_long_trong_link": (
        r'_RE_LINK_MD = re.compile(r"!?\[([^\]\n]*)\]\((?:[^()\n]|\([^()\n]*\))*\)")',
        r'_RE_LINK_MD = re.compile(r"!?\[([^\]\n]*)\]\([^()\n]*\)")',
        ["ac18_link_ngoac_long"],
    ),
    "bo_rut_text_link_markdown": (
        '    text = _RE_LINK_MD.sub(r"\\1", text)\n',
        "",
        ["ac18_link_markdown"],
    ),
    "bo_go_backslash_escape": (
        '    text = _RE_ESCAPE.sub(r"\\1", text)\n',
        "",
        ["ac18_backslash_escape"],
    ),
    # --- AC 19 · chiều BẮT OAN --------------------------------------------------
    # Bỏ điều kiện ngữ cảnh của hạng NGÔN NGỮ THƯỜNG ⇒ văn xuôi kể lại kết quả đo
    # bị tính là chép doctrine trở lại. Không có đột biến này thì không ai biết
    # ba ca bắt-oan kia đang đo chốt hay chỉ đang xanh sẵn.
    # Nới miễn trừ trở lại bề rộng SAI của generation 4 (tha mọi thứ không nằm gọn
    # trong một dòng CÓ `|`) ⇒ mọi lớp "đứng một mình" phải ĐỎ lại.
    # PHỐI HỢP hai vế, và lý do phải phối hợp là bài học của lượt 7. Bản đơn chỉ gỡ
    # chốt "nằm gọn trong một dòng"; sau bản vá lượt 7 thì chốt VĂN XUÔI BỌC HAI PHÍA
    # cũng bắt được đúng những ca ấy, nên gỡ một vế thôi thì ca vẫn XANH và đột biến
    # mất răng — đã đo: 5/6 ca đích sống sót. Muốn nới miễn trừ về ĐÚNG bề rộng sai
    # của generation 4 thì phải gỡ CẢ HAI vế.
    # Chốt khối mã của lượt 7, đứng RIÊNG để có độ phân giải.
    # Hai chốt của việc dò hàng rào lồng cấp, RỜI NHAU để có độ phân giải: một cái
    # gỡ dấu khối trước khi dò, một cái nới mức thụt lề.
    # Ô bảng HTML KHÔNG có chữ bọc thì HAI chốt cùng phủ — bảng HTML lẫn văn xuôi
    # bọc hai phía — nên phải gỡ cả hai mới thấy ca đo gì. Đúng cơ chế phối hợp đã
    # dựng cho P2 lượt 7, nay dùng lại cho một lớp khác.
    # Generation 9 TRẢ LẠI mức thụt CommonMark, nên đột biến đổi chiều: nay nó NỚI
    # mức thụt về `^\\s*` — đúng cái g8 làm — và ca đích là ca BẮT OAN, không phải ca
    # lọt. Nới ra thì một dòng code thụt 4 dấu cách thành hàng rào ma và đầu độc đuôi tệp.
    # --- ba chốt MỚI của generation 9, mỗi cái một đột biến RIÊNG ---------------
    # Chốt gỡ dấu đầu dòng ở tầng phẳng hoá — thiếu nó thì `>` phá khớp hoàn toàn.
    "bo_go_dau_dong_khi_phang_hoa": (
        "        n = _go_dau_dong(_chuan_hoa(dong))",
        "        n = _chuan_hoa(dong)",
        ["ac18_cum_don_trich_dan_ngat_dong", "ac18_cum_don_trich_dan_long_hai_cap",
         "ac18_cum_don_heading_long_trich_dan"],
    ),
    # HAI ĐỘT BIẾN PHỐI HỢP thay cho ngoại lệ `PHU_NHIEU_LOP` đã bỏ (xem
    # `_cap_thay_the`). Mỗi cái gỡ ĐÚNG hai đường cùng phủ một lớp, không hơn.
    # BA vế, không phải hai. Khai ban đầu là "hai đường phủ" (NFKC + `_PHAN_CACH`);
    # dựng đột biến hai vế thì ca VẪN XANH, và đường thứ ba lộ ra: `str.split()`
    # không đối số tách theo khoảng trắng UNICODE, nên `" ".join(text.split())` ở
    # dòng cuối `_chuan_hoa` cũng nuốt U+00A0. Đo được: `'a\\xa0b'.split()` →
    # `['a', 'b']`. Đây chính là giá trị của việc ĐÒI có đột biến thay vì cho khai
    # ngoại lệ — lời khai "hai đường" sai, và chỉ đột biến mới phát hiện ra.
    "ha_NFKC_va_bo_moi_duong_gop_nbsp": (
        ('unicodedata.normalize("NFKC", text)',
         ".translate(_PHAN_CACH)",
         'return " ".join(text.split())'),
        ('unicodedata.normalize("NFC", text)',
         "",
         'return " ".join(re.split(r"[ \\t\\n\\r\\f\\v]+", text)).strip()'),
        ["ac18_nbsp_phu_ba_lop"],
    ),
    "ha_NFKC_va_bo_casefold": (
        ('unicodedata.normalize("NFKC", text)', "text.casefold().translate(_DONG_TU)"),
        ('unicodedata.normalize("NFC", text)', "text.translate(_DONG_TU)"),
        ["ac18_nfkc_ligature_ff"],
    ),
    "void_bo_ghi_so_nguoi_duyet": (
        '        st["history"].append({"event": "void_khong_co_bang_chung", "reason": a.reason,\n'
        '                              "ai_cho_phep": a.ai_cho_phep, "can_cu": a.can_cu})',
        '        pass  # đột biến: cửa thoát không ghi sổ',
        ["void_khong_bang_chung_phai_ghi_so"],
    ),
    "void_bo_dot_nonce": (
        '    anchor["consumed"] = True', '    anchor["consumed"] = False  # đột biến',
        ["void_cung_run_hai_lan_bi_chan"],
    ),
    "void_bo_kiem_hmac": (
        '        if not hmac.compare_digest(d["chu_ky"], mong):', '        if False:',
        ["void_lat_phan_quyet_bi_hmac_chan"],
    ),
    "void_bo_khop_nonce": (
        '        if d["nonce"] != anchor["nonce"]:', '        if False:',
        ["void_run_cheo_luot_bi_chan", "void_cung_anh_doctor_hai_luot_bi_chan",
         "void_touch_anh_doctor_cu_van_bi_chan"],
    ),
    "void_gop_thong_diep_run_cu": (
        '"bằng chứng máy không có neo lượt — dùng "', '"ảnh môi trường thiếu trường của `doctor --json` — "',
        ["void_run_cu_khong_neo_co_thong_diep_rieng"],
    ),
    "void_siet_tu_choi_moi_run": (
        '        if d.get("trang_thai") not in ("qua_han", "hong"):', '        if True:',
        ["void_run_that_dung_luot_duoc_tha"],
    ),
    "void_bo_phan_biet_ly_do": (
        '        if d.get("void_reason") != ly_do:', '        if False:',
        ["void_hai_ly_do_khong_dung_chung_run"],
    ),
    "doctor_bo_ky_anh": (
        '    d["chu_ky"] = ky_ban_ghi_luot(d, st["hmac_key"])',
        '    d.pop("chu_ky", None)  # đột biến: ảnh writer không ký',
        ["chup_anh_doctor_ky_noi_bo"],
    ),
    "begin_bo_kiem_nen_tuoi_dung_chung": (
        '    anh = _kiem_anh_moi_truong(getattr(a, "bang_chung_moi_truong", None)\n'
        '                               or os.environ.get(BIEN_BANG_CHUNG), can_sach=True)',
        '    anh = _doc_anh_moi_truong(getattr(a, "bang_chung_moi_truong", None)\n'
        '                              or os.environ.get(BIEN_BANG_CHUNG))[0]  # đột biến',
        ["anh_doctor_nen_chung_tuoi_chi_begin"],
    ),
    "void_khoi_phuc_kiem_tuoi": (
        '    d = _kiem_anh_moi_truong(duong, can_sach=False, d=d, kiem_tuoi=False)',
        '    d = _kiem_anh_moi_truong(duong, can_sach=False, d=d, kiem_tuoi=True)',
        ["anh_doctor_nen_chung_tuoi_chi_begin"],
    ),
    # Hai chốt của `void-reviewing-accepts-attempt-zero`, hai đột biến RỜI NHAU.
    "bo_void_roi_reviewing": (
        '    if st["state"] == "reviewing":\n        st["state"] = "running"',
        '    if False:\n        st["state"] = "running"',
        ["g5_void_o_reviewing_khong_ket_thuc_bang_approve"],
    ),
    "bo_record_review_doi_luot_mo": (
        '    if not st["attempt_open"]:',
        "    if False:",
        ["g5_record_review_doi_LUOT_DANG_MO"],
    ),
    "bo_record_review_doi_so_luot_duong": (
        '    if st["attempts_used"] <= 0:\n        _die(RC_STATE,\n             f"attempts_used',
        '    if False:\n        _die(RC_STATE,\n             f"attempts_used',
        ["g5_record_review_doi_SO_LUOT_LON_HON_0"],
    ),
    "mo_lai_cua_reviewing_sang_running": (
        '    "reviewing": (),',
        '    "reviewing": ("running",),',
        ["g5_reviewing_khong_ra_bang_transition"],
    ),
    # Chiều ngược: gỡ HẲN cụm khỏi danh sách cấm thì ca DƯƠNG phải chết — chứng
    # minh sửa chiều bắt oan KHÔNG phải là gỡ chốt.
    #
    # Chỉ ca ô-bảng nằm trong danh sách phải-chết. `ac19_term_kem_muc_khac_...`
    # theo định nghĩa phải chứa một mục KHÁC cùng nhóm, nên nó vẫn đỏ khi cụm bị
    # gỡ — nó đo điều kiện (2) của ngữ cảnh, không đo sự có mặt của cụm.
    "go_han_cum_khoi_danh_sach": (
        '        "người có thẩm quyền",\n',
        "",
        ["ac19_bang_vai_tro_THAT_van_bi_bat"],
    ),
    "luong_canonical_chay_that_dao_os_name": (
        '    assert os.name == "nt", "phải chạy trên Windows"\n',
        '    assert os.name != "nt", "phải chạy trên Windows"  # đột biến\n',
        ["luong_canonical_chay_that"],
    ),
    "74a_splitlines_sai": ('    p = re.split(r\'(\\r\\n|\\r|\\n)\', noi_dung); lines = [p[i]+p[i+1] for i in range(0,len(p)-1,2)]+([p[-1]] if p[-1] else [])', '    lines = noi_dung.splitlines(keepends=True)', ["trich_xuat_74a_chong_nhieu"]),
    "74a_raw_closing_cung_ten": ('            if mh:\n                end_re = re.compile(r"-->" if mh.group(1) else r"(?i)</(?:pre|script|style|textarea)>")', '            if mh:\n                end_re = re.compile(r"-->" if mh.group(1) else f"(?i)</{mh.group(2)}>")', ["trich_xuat_74a_chong_nhieu"]),
    "bo_kiem_chep_protocol": (
        "        if True:",
        "        if False:  # bo_kiem_chep_protocol",
        ["doctrine_scan_chep_tron_5_1_bi_chan",
         "doctrine_scan_chep_doan_ngan_5_1_bi_chan",
         "doctrine_scan_chep_12_bi_chan"],
    ),
    "nang_nguong_chep_protocol_len_50": (
        "            threshold = 15 if is_claude_md else 10",
        "            threshold = 50  # nang_nguong_chep_protocol_len_50",
        ["doctrine_scan_chep_doan_ngan_5_1_bi_chan"],
    ),
}

# Phân loại là KHAI BÁO: tên chỉ có mặt ở đây mới được sửa test harness.
# Mỏ neo của mọi mục vẫn phải sống trong đúng tệp được khai.
MUTANTS_NHAM_TEST = frozenset({
    "bien_nhan_root_xuong_dong_tha_vo_dieu_kien",
    "bien_nhan_shim_tha_vo_dieu_kien",
    "git_co_lap_bo_sot_pham_vi_lenh",
    "git_co_lap_lui_ve_ghim_khoa",
    "git_co_lap_tha_vo_dieu_kien",
    "moc_kiem_noi_vo_dieu_kien",
    "moc_kiem_to_vo_dieu_kien",
    "phan_loai_lai_dot_bien_test_bang_suy_luan",
    "luong_canonical_chay_that_dao_os_name",
    "bo_qua_html_guard_trong_trich_xuat", "74a_splitlines_sai", "74a_raw_closing_cung_ten",
})


# Ca được PHỦ BỞI NHIỀU LỚP nên không đột biến ĐƠN LẺ nào giết được. Khai tường
# minh kèm lý do ĐO ĐƯỢC — nói thẳng chỗ phủ chồng còn hơn gán bừa cho một lớp rồi
# tưởng đã đo được lớp ấy, và còn hơn để ca nằm ngoài mọi danh sách như generation 4.
# `PHU_NHIEU_LOP` ĐÃ BỎ. Nó từng miễn chốt AC 18 cho `ac18_nbsp_phu_ba_lop` và
# `ac18_nfkc_ligature_ff` với lý do "hai đường cùng phủ nên đột biến đơn không giết
# được". Cross-review lượt 7 bác: lý do ấy đúng, nhưng nó giải thích vì sao đột biến
# ĐƠN không đủ, chứ không miễn được yêu cầu phải CÓ đột biến. Thay bằng hai đột biến
# PHỐI HỢP gỡ đúng hai đường phủ của từng lớp — xem `_cap_thay_the`. Giờ KHÔNG lớp
# nào trong `LOP_LACH` được miễn, và chốt dưới không còn cửa ngoại lệ để lách.


# Đối chứng KHÁC HỌ: ca thuộc tầng mà một đột biến ở tầng kia KHÔNG được đụng tới.
# Chọn ca "xương sống" của mỗi họ — nếu đột biến làm hỏng cả những ca này thì nó
# không nhắm đúng tầng nó khai, dù ca đích vẫn chết đúng.
DOI_CHUNG_DOCTRINE = ("doctrine_scan_sach_xanh", "ac18_nfkc_hai_cham_toan_rong",
                      "ac19_oan_claude_md_master")
DOI_CHUNG_MAY_TRANG_THAI = ("lease_hop_le_thi_mo_duoc_luot", "transition_hop_le_rc0",
                            "cap_lan_4_thoat_3")


def _cap_thay_the(tim, thay):
    """Chuẩn hoá một đột biến về DANH SÁCH cặp `(tìm, thay)`.

    Vì sao cần đột biến PHỐI HỢP — cross-review lượt 7 bắt đúng chỗ này. AC 18 đòi
    *mỗi lớp* có một đột biến giết đúng ca của nó. Nhưng có lớp được HAI đường
    trong `_chuan_hoa` cùng phủ:

      `ac18_nbsp_phu_ba_lop`  — NFKC gộp U+00A0, và `_PHAN_CACH` cũng gộp nó;
      `ac18_nfkc_ligature_ff`  — NFKC gấp `ﬀ`, và `casefold()` ĐỘC LẬP cũng gấp.

    Gỡ một đường thì đường kia vẫn bắt, nên đột biến đơn không giết được ca —
    generation 5 xử lý bằng cách KHAI NGOẠI LỆ (`PHU_NHIEU_LOP`) và coi lớp có mặt
    trong danh sách ngoại lệ là đạt. Reviewer bác đúng: lý do phủ chồng giải thích
    vì sao đột biến ĐƠN không giết được, nhưng không thay thế được yêu cầu phải CÓ
    đột biến. Khai ngoại lệ là hạ chuẩn so với câu chữ spec.

    Đường ra không phải ngoại lệ mà là đột biến MẠNH VỪA ĐỦ: gỡ ĐÚNG hai đường phủ
    của lớp ấy, không gỡ thêm gì. Ca đích chết, và đối chứng khác họ vẫn sống —
    tức đột biến vẫn nhắm đúng tầng. `PHU_NHIEU_LOP` do đó bị BỎ HẲN, không còn
    lớp nào trong `LOP_LACH` được miễn.
    """
    if isinstance(tim, str):
        return [(tim, thay)]
    if len(tim) != len(thay):
        raise AssertionError(f"đột biến phối hợp lệch số vế: {len(tim)} ≠ {len(thay)}")
    return list(zip(tim, thay))


def _phan_loai_dot_bien(ten_mut, cap, goc, goc_test):
    """Chọn nguồn bằng khai báo, rồi canh mỏ neo trong chính nguồn ấy."""
    dot_bien_test = ten_mut in MUTANTS_NHAM_TEST
    than = goc_test if dot_bien_test else goc
    thieu = [t for t, _ in cap if t not in than]
    return than, dot_bien_test, thieu


def _la_ho_doctrine(ten: str) -> bool:
    return ten.startswith(("ac18_", "ac19_", "doctrine_"))


def _doi_chung_khac_ho(phai_chet) -> tuple:
    """Đột biến ở họ nào thì đối chứng lấy từ họ KIA."""
    if all(_la_ho_doctrine(t) for t in phai_chet):
        return DOI_CHUNG_MAY_TRANG_THAI
    if not any(_la_ho_doctrine(t) for t in phai_chet):
        return DOI_CHUNG_DOCTRINE
    # Đột biến bắc qua hai họ: không có "họ kia" để đối chứng — nói thẳng thay vì
    # chọn bừa một tập rồi coi như đã đo.
    return ()


# --- #298 B3 — cổng `bien-nhan` ------------------------------------------------------
#
# VÌ SAO CÓ: kho ĐÃ có bộ đếm bền (`ops/reviews/*.receipt.yaml`, trong git nên sống sót
# container) và ĐÃ có hai cổng `t26`/`t27` gác nó. Nhưng `t27` duyệt `glob("*-verdict.md")`
# — nó gác thứ ĐÃ ghi ra đĩa, mù hoàn toàn với verdict chưa ai viết. Packet #249 chạy BỐN
# vòng cross-review, để lại 0 biên nhận, suite vẫn 98/98 xanh. Chuỗi `doctor-github-mcp`
# mất năm lượt y hệt trước đó.

def _kho_gia(c: Ctx, ten: str, bien_nhan=()) -> Path:
    """Dựng một "kho" giả có `.git` và `ops/reviews/` chứa các biên nhận cho trước."""
    goc = c.tmp / ten
    (goc / ".git").mkdir(parents=True, exist_ok=True)
    tm = goc / "ops" / "reviews"
    tm.mkdir(parents=True, exist_ok=True)
    for ten_tep, noi_dung in bien_nhan:
        (tm / ten_tep).write_text(noi_dung, encoding="utf-8")
    return goc


def _kho_gia_co_verdict(c: Ctx, ten: str, bien_nhan=()) -> Path:
    """Như `_kho_gia` nhưng tạo luôn `ops/reviews/v.md` để biên nhận không thành mồ côi."""
    goc = _kho_gia(c, ten, bien_nhan)
    (goc / "ops" / "reviews" / "v.md").write_text("verdict\n", encoding="utf-8")
    return goc


_BN_REVIEWER = """schema_version: 1
kind: review_delivery_receipt
packet_id: '249'
role: reviewer
provider: codex
verdict: approve
reviewed_sha: efcf5757403bd989c0ebbd388fa7a7180171b49f
verdict_path: ops/reviews/v.md
"""

# Hình dạng THẬT, không phải bịa: `plat-m4-human-audit-ducthangho-verdict.receipt.yaml` và
# `slice-b-c-human-audit-...` trong kho đều mang `role: auditor`. Một packet có audit của
# người mà KHÔNG có vòng review nào là trạng thái tồn tại được — và đếm TỆP sẽ gọi nó là
# "đã review".
_BN_AUDITOR = """schema_version: 1
kind: review_delivery_receipt
packet_id: '249'
role: auditor
provider: ducthangho
verdict: approve
reviewed_sha: efcf5757403bd989c0ebbd388fa7a7180171b49f
"""


def case_bien_nhan_0_thi_DO(c: Ctx):
    goc = _kho_gia(c, "bn0")
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "packet 0 biên nhận reviewer phải ĐỎ")


def case_bien_nhan_co_reviewer_thi_QUA(c: Ctx):
    goc = _kho_gia_co_verdict(c, "bn1", [("a-verdict.receipt.yaml", _BN_REVIEWER)])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "có biên nhận reviewer thì phải QUA")


def case_bien_nhan_chi_dem_VAI_khong_dem_TEP(c: Ctx):
    """Trục phân biệt: `role`, KHÔNG phải số tệp trong thư mục.

    Bỏ mệnh đề `role == "reviewer"` thì ca này XANH oan — đó là phép thử cho chính nó.
    """
    goc = _kho_gia(c, "bn_audit", [("h-verdict.receipt.yaml", _BN_AUDITOR)])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "chỉ có biên nhận `role: auditor` mà vẫn QUA ⇒ cổng đang đếm TỆP")


def case_bien_nhan_yaml_hong_la_KHONG_DO_DUOC(c: Ctx):
    """YAML hỏng phải ĐỎ kèm `KHÔNG ĐO ĐƯỢC` — KHÔNG được lặng lẽ thành "0 biên nhận".

    Ba trạng thái, không phải hai: hai câu ấy đòi hai hành động ngược nhau (ghi biên nhận ·
    sửa môi trường) mà con số thì giống hệt.
    """
    goc = _kho_gia(c, "bn_hong", [("x-verdict.receipt.yaml", "[: khong phai yaml\n")])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "YAML hỏng phải ĐỎ")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {_txt(e)!r}")


def case_bien_nhan_kho_that_thieu_thu_muc_la_DO(c: Ctx):
    goc = c.tmp / "bn_thieu"
    (goc / ".git").mkdir(parents=True, exist_ok=True)
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc)])
    _doi(11, rc, e, "kho thật mà thiếu ops/reviews phải ĐỎ")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {_txt(e)!r}")


def case_bien_nhan_ban_sao_roi_thi_bo_qua(c: Ctx):
    """Bản sao rời (không `.git`) được tha — nhưng CHỈ bản sao rời. Bài học `t24`."""
    goc = c.tmp / "bn_roi"
    goc.mkdir(parents=True, exist_ok=True)
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc)])
    _doi(0, rc, e, "bản sao rời không có .git thì bỏ qua")


CASES += [
    ("bien_nhan_0_thi_DO", case_bien_nhan_0_thi_DO),
    ("bien_nhan_co_reviewer_thi_QUA", case_bien_nhan_co_reviewer_thi_QUA),
    ("bien_nhan_chi_dem_VAI_khong_dem_TEP", case_bien_nhan_chi_dem_VAI_khong_dem_TEP),
    ("bien_nhan_yaml_hong_la_KHONG_DO_DUOC", case_bien_nhan_yaml_hong_la_KHONG_DO_DUOC),
    ("bien_nhan_kho_that_thieu_thu_muc_la_DO", case_bien_nhan_kho_that_thieu_thu_muc_la_DO),
    ("bien_nhan_ban_sao_roi_thi_bo_qua", case_bien_nhan_ban_sao_roi_thi_bo_qua),
]


# --- #298 lượt 1 cross-review: ba finding, bốn ca khoá lại -----------------------------
#
# Hai đột biến SỐNG SÓT qua cả 6 ca đầu (`s2-sau-ca-khong-khoa-truc-khop`, P2): đổi so BẰNG
# thành chuỗi con, và bỏ `packet_slug`. Mã vốn ĐÚNG cả hai — nhưng không ca nào ĐO, nên
# "đúng" là may chứ không phải được khoá. Cộng `s2-dem-tep-tu-nhan-reviewer` (P2): hai biên
# nhận trùng vòng, trỏ verdict không tồn tại, vẫn qua cổng.

_BN_SLUG = """schema_version: 1
kind: review_delivery_receipt
packet_slug: T33-DOI-SHELLCHECK
role: reviewer
provider: codex
verdict: approve
reviewed_sha: efcf5757403bd989c0ebbd388fa7a7180171b49f
verdict_path: ops/reviews/v.md
"""


def _bn_that(sha: str, duong: str = "ops/reviews/v.md") -> str:
    """Biên nhận HỢP LỆ: có `verdict_path` trỏ tệp thật (ca tự tạo tệp ấy)."""
    return (f"schema_version: 1\nkind: review_delivery_receipt\npacket_id: '249'\n"
            f"role: reviewer\nprovider: codex\nverdict: approve\n"
            f"reviewed_sha: {sha}\nverdict_path: {duong}\n")


def _dat_object_format(goc: Path, dinh_dang: str) -> None:
    p = subprocess.run(["git", "-C", str(goc), "init", "--quiet",
                        f"--object-format={dinh_dang}"], capture_output=True)
    if p.returncode != 0:
        raise AssertionError(f"KHÔNG ĐO ĐƯỢC: git init {dinh_dang} rc={p.returncode}: "
                             f"{_txt(p.stderr)!r}")


# Ba hình dạng fixture SHA mà #305 bắt buộc phủ: có chữ · toàn số không 0 đầu ·
# toàn số có 0 đầu. Hai hằng cuối cố ý KHÔNG đặt nháy khi đi qua `_bn_that`.
_SHA_CO_CHU = "8b627e843a3be87f2ceac97f2f147bbadcaa3cdc"
_SHA_SO_KHONG_0_A = "1234567012345670123456701234567012345670"
_SHA_SO_KHONG_0_B = "2234567022345670223456702234567022345670"
_SHA_SO_CO_0_DAU_A = "0123456"
_SHA_SO_CO_0_DAU_B = "0765432"


def case_bien_nhan_packet_24_khong_an_bien_nhan_249(c: Ctx):
    """So BẰNG, không phải chuỗi con. `24` là chuỗi con của `249`.

    Đột biến `M1_KHOP_SUBSTRING` sống sót qua 6 ca đầu; ca này giết nó.
    """
    goc = _kho_gia_co_verdict(c, "bn24", [("a-verdict.receipt.yaml", _bn_that("%040x" % 1))])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "24"])
    _doi(11, rc, e, "packet '24' ăn biên nhận của '249' ⇒ đang khớp CHUỖI CON")


def case_bien_nhan_khop_duoc_bang_packet_slug(c: Ctx):
    """`packet_slug` phải khớp được — lease khai vậy, và đột biến bỏ nó từng sống sót."""
    goc = _kho_gia_co_verdict(c, "bnslug", [("a-verdict.receipt.yaml", _BN_SLUG)])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc),
                              "--packet", "T33-DOI-SHELLCHECK"])
    _doi(0, rc, e, "biên nhận chỉ mang `packet_slug` phải khớp được bằng slug")


def case_bien_nhan_mo_coi_khong_duoc_dem(c: Ctx):
    """`verdict_path` trỏ tệp KHÔNG CÓ ⇒ không chứng minh ai review, chỉ chứng minh ai ghi YAML."""
    goc = _kho_gia(c, "bnmocoi", [("a-verdict.receipt.yaml",
                                   _bn_that("%040x" % 1, "ops/reviews/KHONG-CO.md"))])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "biên nhận mồ côi vẫn được đếm ⇒ cổng đo TỆP chứ không đo VÒNG")


def case_bien_nhan_verdict_path_TUYET_DOI_khong_duoc_dem(c: Ctx):
    """`verdict_path` tuyệt đối trỏ RA NGOÀI kho ⇒ không được tính.

    `pathlib` định nghĩa `a / "/x"` == `Path("/x")` — vế trái bị VỨT. Nên bộ lọc mồ côi
    bản đầu (`(root / verdict_path).is_file()`) hoá ra hỏi về chính tệp ngoài kho, thấy nó
    có thật, rồi tính biên nhận là một vòng hợp lệ. Cross-review lượt 2 của #298 tái hiện
    được: `rc=0` ở nơi phải `rc=11`.
    """
    ngoai = c.tmp / "ngoai-kho-tuyet-doi.md"
    ngoai.write_text("khong phai verdict\n", encoding="utf-8")
    goc = _kho_gia(c, "bnabs", [("a-verdict.receipt.yaml",
                                 _bn_that("%040x" % 3, str(ngoai.resolve())))])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "đường dẫn TUYỆT ĐỐI ra ngoài kho vẫn được đếm ⇒ bộ lọc đo "
                    "'có tệp nào đó tồn tại', không đo 'verdict nằm trong kho này'")


def case_bien_nhan_verdict_path_SYMLINK_ra_ngoai_khong_duoc_dem(c: Ctx):
    """Symlink trong `ops/reviews/` trỏ ra ngoài kho ⇒ không được tính.

    Đường thứ hai của cùng lỗ: `is_file()` ĐI THEO liên kết, nên đích ngoài kho vẫn đạt.
    Chốt phải `resolve()` rồi đòi ĐÍCH CUỐI nằm trong `ops/reviews`.
    """
    ngoai = c.tmp / "ngoai-kho-symlink.md"
    ngoai.write_text("khong phai verdict\n", encoding="utf-8")
    goc = _kho_gia(c, "bnsym", [("a-verdict.receipt.yaml",
                                 _bn_that("%040x" % 4, "ops/reviews/link.md"))])
    try:
        (goc / "ops" / "reviews" / "link.md").symlink_to(ngoai.resolve())
    except (OSError, NotImplementedError) as ex:
        # KHÔNG ĐO ĐƯỢC ⇒ ĐỎ, không lặng lẽ ĐẠT. Windows chỉ cho tạo symlink khi bật
        # Developer Mode hoặc chạy quyền cao. Một ca tự tha khi thiếu năng lực là ca
        # "có MẶT mà không ĐO" — đúng bệnh `t24`, và cùng nếp với `t33` (thiếu
        # `actionlint` ⇒ ĐỎ chứ không bỏ qua).
        raise AssertionError(
            f"KHÔNG ĐO ĐƯỢC: nền không tạo được symlink ({type(ex).__name__}: {ex}). "
            f"Ca này gác đường symlink nên không đo được thì phải ĐỎ.") from ex
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "symlink trỏ ra ngoài kho vẫn được đếm ⇒ chốt chưa đi hết liên kết")


def case_bien_nhan_thieu_sha_nhieu_ban_van_dem_MOT(c: Ctx):
    """Nhiều biên nhận cùng THIẾU `reviewed_sha` góp nhiều nhất MỘT vòng.

    Bản đầu rơi về khoá `f"__khong_sha__{tên tệp}"`, tức lại đếm theo TỆP — đúng khuyết tật
    lượt 1 đã nêu, chỉ dời sang nhánh không ai nghĩ tới. Một biên nhận không neo commit thì
    không nói được nó là vòng NÀO.
    """
    khong_sha = ("schema_version: 1\nkind: review_delivery_receipt\npacket_id: '249'\n"
                 "role: reviewer\nprovider: codex\nverdict: approve\n"
                 "verdict_path: ops/reviews/v.md\n")
    goc = _kho_gia_co_verdict(c, "bnnosha", [("a-verdict.receipt.yaml", khong_sha),
                                             ("b-verdict.receipt.yaml", khong_sha)])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "2"])
    _doi(11, rc, e, "hai biên nhận cùng THIẾU sha được đếm thành 2 ⇒ lấp trần bằng chép tệp")
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "chặn oan: thiếu sha vẫn phải tính là MỘT vòng hợp lệ")


def case_bien_nhan_sha_RAC_khong_duoc_lam_khoa_vong(c: Ctx):
    """`reviewed_sha` CÓ mặt nhưng là RÁC ⇒ không được làm khoá vòng.

    Dạng THỨ BA của cùng một bệnh, cross-review lượt 3 của #298 tìm ra. Hai dạng trước
    đếm theo TỆP; dạng này đếm theo GIÁ TRỊ TỰ KHAI — ba chuỗi rác khác nhau thành ba
    "vòng", `rc=0` ở nơi phải `rc=11`. Chốt đóng HÌNH DẠNG, không đóng thêm một dạng:
    chỉ chuỗi trông như commit mới được làm khoá; mọi thứ khác dồn về CÙNG một xô.
    """
    def bn(sha):
        return ("schema_version: 1\nkind: review_delivery_receipt\npacket_id: '249'\n"
                "role: reviewer\nprovider: codex\nverdict: approve\n"
                f"reviewed_sha: {sha}\nverdict_path: ops/reviews/v.md\n")
    goc = _kho_gia_co_verdict(c, "bnracsha", [("a-verdict.receipt.yaml", bn("rac-1")),
                                              ("b-verdict.receipt.yaml", bn("rac-2")),
                                              ("c-verdict.receipt.yaml", bn("khong-phai-sha"))])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "3"])
    _doi(11, rc, e, "ba chuỗi RÁC khác nhau thành 3 vòng ⇒ cổng đếm GIÁ TRỊ TỰ KHAI")
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "chặn oan: sha rác vẫn phải tính là MỘT vòng hợp lệ")


def case_bien_nhan_cung_sha_full_va_viet_tat_dem_MOT(c: Ctx):
    """N1: full OID + viết tắt của chính nó là MỘT khoá neo, không phải hai."""
    goc = _kho_gia_co_verdict(c, "bnfulltat", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU)),
        ("b-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU[:7])),
    ])
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "2"])
    _doi(11, rc, e, "full SHA + viết tắt của nó được đếm thành HAI")
    if "1 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm MỘT: {_txt(o)!r}")


def case_bien_nhan_sha256_full64_va_tien_to40_dem_MOT(c: Ctx):
    """SHA-256: 40 ký tự chỉ là tiền tố, không phải một OID SHA-1 thứ hai."""
    sha = _SHA_CO_CHU + "fedcba987654321001234567"
    goc = _kho_gia_co_verdict(c, "bnsha256tat", [
        ("a-verdict.receipt.yaml", _bn_that(sha)),
        ("b-verdict.receipt.yaml", _bn_that(sha[:40])),
    ])
    _dat_object_format(goc, "sha256")
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "SHA-256 full-64 + tiền tố-40 của nó bị chặn oan")
    if "1 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm MỘT: {_txt(o)!r}")


def case_bien_nhan_sha256_root_xuong_dong_dem_MOT(c: Ctx):
    sha = _SHA_CO_CHU + "f" * 24
    goc = c.tmp / "bnsha256\nroot"
    try:
        goc.mkdir()
    except OSError as ex:
        raise BoQua(f"nền từ chối tên thư mục có xuống dòng: {ex}") from ex
    goc = _kho_gia_co_verdict(c, "bnsha256\nroot", [
        ("a-verdict.receipt.yaml", _bn_that(sha)),
        ("b-verdict.receipt.yaml", _bn_that(sha[:40]))])
    _dat_object_format(goc, "sha256")
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "root có xuống dòng làm mất object format")
    if "1 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm MỘT: {_txt(o)!r}")


def case_bien_nhan_git_gia_duong_dan_nul_giu_fallback(c: Ctx):
    git = c.tmp / "git"
    git.write_text("#!/usr/bin/env python3\nimport sys\nsys.stdout.buffer.write(b'/tmp/a\\x00b\\nsha256\\n')\n", encoding="utf-8")
    git.chmod(0o755)
    try:
        p = subprocess.run([str(git)], capture_output=True, check=True)
    except OSError as ex:
        raise BoQua(f"nền từ chối thi hành git giả: {ex}") from ex
    if b"\x00" not in p.stdout:
        raise AssertionError("git giả được gọi nhưng không trả fixture NUL")
    goc = _kho_gia_co_verdict(c, "bnnul", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU)),
        ("b-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU[:7]))])
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"],
                   env_extra={"PATH": str(c.tmp) + os.pathsep + os.environ["PATH"]})
    _doi(0, rc, e, "ValueError từ top-level không hợp lệ thoát traceback")
    if "1 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm MỘT: {_txt(o)!r}")


def case_bien_nhan_sha256_hai_oid_khac_nhau_dem_HAI(c: Ctx):
    """Chiều bắt-oan: hai OID SHA-256 khác nhau không được gom sạch."""
    goc = _kho_gia_co_verdict(c, "bnsha256hai", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU + "a" * 24)),
        ("b-verdict.receipt.yaml", _bn_that("9" * 64)),
    ])
    _dat_object_format(goc, "sha256")
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "2"])
    _doi(0, rc, e, "hai OID SHA-256 khác nhau bị gom thành một")
    if "2 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm HAI: {_txt(o)!r}")


def case_bien_nhan_ban_sao_roi_co_du_lieu_van_dem_duoc(c: Ctx):
    """Không hỏi được object format thì giữ phép phân loại cũ, không chặn."""
    goc = _kho_gia_co_verdict(c, "bnroidudulieu", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU)),
        ("b-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU[:7])),
    ])
    (goc / ".git").rmdir()
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "bản sao rời có dữ liệu bị chặn vì không hỏi được format")
    if "1 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm MỘT: {_txt(o)!r}")


def case_bien_nhan_ban_sao_roi_duoi_sha256_cha_dem_MOT(c: Ctx):
    goc = _kho_gia_co_verdict(c, "bnroichasha256", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU)),
        ("b-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU[:7])),
    ])
    (goc / ".git").rmdir()
    _dat_object_format(goc.parent, "sha256")
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "bản sao rời dưới kho cha SHA-256 bị chặn oan")
    if "1 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm MỘT: {_txt(o)!r}")


def case_bien_nhan_sha_so_co_0_dau_van_dem_RIENG(c: Ctx):
    """N3: YAML không nháy không được đổi hai SHA toàn số có 0 đầu thành một xô."""
    goc = _kho_gia_co_verdict(c, "bnso0dau", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_SO_CO_0_DAU_A)),
        ("b-verdict.receipt.yaml", _bn_that(_SHA_SO_CO_0_DAU_B)),
    ])
    rc, o, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "2"])
    _doi(0, rc, e, "hai SHA toàn số có 0 đầu bị YAML đổi kiểu rồi gom một xô")
    if "2 biên nhận PHÂN BIỆT ĐƯỢC" not in _txt(o):
        raise AssertionError(f"không có bằng chứng dương đếm HAI: {_txt(o)!r}")


def case_bien_nhan_viet_tat_khop_hai_oid_la_KHONG_DO_DUOC(c: Ctx):
    """Dạng 6: một viết tắt khớp hai full OID ⇒ không được tự chọn một phía."""
    sha_b = _SHA_CO_CHU[:7] + "f" * 33
    goc = _kho_gia_co_verdict(c, "bnmoho", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU)),
        ("b-verdict.receipt.yaml", _bn_that(sha_b)),
        ("c-verdict.receipt.yaml", _bn_that(_SHA_CO_CHU[:7])),
    ])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(11, rc, e, "viết tắt khớp hai OID mà cổng vẫn tự gom")
    if "KHÔNG ĐO ĐƯỢC" not in _txt(e):
        raise AssertionError(f"đỏ mà không khai trạng thái thứ ba: {_txt(e)!r}")


def case_bien_nhan_sha_that_van_dem_RIENG(c: Ctx):
    """Chặn oan phía kia: hai `reviewed_sha` HỢP LỆ và khác nhau vẫn phải là HAI vòng.

    Thiếu ca này thì chốt F4 có thể gom sạch mọi thứ về một xô mà không ai biết —
    cổng sẽ "an toàn" bằng cách không đếm được gì.
    """
    goc = _kho_gia_co_verdict(c, "bnshathat", [
        ("a-verdict.receipt.yaml", _bn_that(_SHA_SO_KHONG_0_A)),
        ("b-verdict.receipt.yaml", _bn_that(_SHA_SO_KHONG_0_B)),
    ])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "2"])
    _doi(0, rc, e, "hai sha HỢP LỆ khác nhau bị gom thành một ⇒ cổng thành mù")


def case_bien_nhan_nguong_0_hoac_am_bi_CHAN(c: Ctx):
    """`--toi-thieu 0` / âm ⇒ CHẶN. Cổng tắt được bằng chính cờ của nó thì không phải cổng."""
    goc = _kho_gia(c, "bnnguong")
    for n in ("0", "-1"):
        rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                                  "--toi-thieu", n])
        _doi(2, rc, e, f"--toi-thieu {n} được chấp nhận ⇒ cổng TỰ TẮT được")


def case_bien_nhan_hai_ban_trung_vong_dem_MOT(c: Ctx):
    """Hai biên nhận cùng `reviewed_sha` là MỘT vòng ghi hai lần.

    Đếm là 2 thì `--toi-thieu 2` lấp được bằng cách CHÉP TỆP — cổng đo số tệp, không đo số vòng.
    """
    sha = "%040x" % 7
    goc = _kho_gia_co_verdict(c, "bntrung", [("a-verdict.receipt.yaml", _bn_that(sha)),
                                         ("b-verdict.receipt.yaml", _bn_that(sha))])
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249",
                              "--toi-thieu", "2"])
    _doi(11, rc, e, "hai biên nhận TRÙNG vòng được đếm thành 2 ⇒ lấp được trần bằng chép tệp")
    rc, _, e = run(c.script, ["bien-nhan", "--root", str(goc), "--packet", "249"])
    _doi(0, rc, e, "chặn oan: trùng vòng vẫn phải tính là MỘT vòng hợp lệ")


CASES += [
    ("bien_nhan_packet_24_khong_an_bien_nhan_249", case_bien_nhan_packet_24_khong_an_bien_nhan_249),
    ("bien_nhan_khop_duoc_bang_packet_slug", case_bien_nhan_khop_duoc_bang_packet_slug),
    ("bien_nhan_mo_coi_khong_duoc_dem", case_bien_nhan_mo_coi_khong_duoc_dem),
    ("bien_nhan_hai_ban_trung_vong_dem_MOT", case_bien_nhan_hai_ban_trung_vong_dem_MOT),
    ("bien_nhan_verdict_path_TUYET_DOI_khong_duoc_dem",
     case_bien_nhan_verdict_path_TUYET_DOI_khong_duoc_dem),
    ("bien_nhan_verdict_path_SYMLINK_ra_ngoai_khong_duoc_dem",
     case_bien_nhan_verdict_path_SYMLINK_ra_ngoai_khong_duoc_dem),
    ("bien_nhan_thieu_sha_nhieu_ban_van_dem_MOT",
     case_bien_nhan_thieu_sha_nhieu_ban_van_dem_MOT),
    ("bien_nhan_nguong_0_hoac_am_bi_CHAN",
     case_bien_nhan_nguong_0_hoac_am_bi_CHAN),
    ("bien_nhan_sha_RAC_khong_duoc_lam_khoa_vong",
     case_bien_nhan_sha_RAC_khong_duoc_lam_khoa_vong),
    ("bien_nhan_cung_sha_full_va_viet_tat_dem_MOT",
     case_bien_nhan_cung_sha_full_va_viet_tat_dem_MOT),
    ("bien_nhan_sha256_full64_va_tien_to40_dem_MOT",
     case_bien_nhan_sha256_full64_va_tien_to40_dem_MOT),
    ("bien_nhan_sha256_root_xuong_dong_dem_MOT", case_bien_nhan_sha256_root_xuong_dong_dem_MOT),
    ("bien_nhan_git_gia_duong_dan_nul_giu_fallback", case_bien_nhan_git_gia_duong_dan_nul_giu_fallback),
    ("bien_nhan_sha256_hai_oid_khac_nhau_dem_HAI",
     case_bien_nhan_sha256_hai_oid_khac_nhau_dem_HAI),
    ("bien_nhan_ban_sao_roi_co_du_lieu_van_dem_duoc",
     case_bien_nhan_ban_sao_roi_co_du_lieu_van_dem_duoc),
    ("bien_nhan_ban_sao_roi_duoi_sha256_cha_dem_MOT",
     case_bien_nhan_ban_sao_roi_duoi_sha256_cha_dem_MOT),
    ("bien_nhan_sha_so_co_0_dau_van_dem_RIENG",
     case_bien_nhan_sha_so_co_0_dau_van_dem_RIENG),
    ("bien_nhan_viet_tat_khop_hai_oid_la_KHONG_DO_DUOC",
     case_bien_nhan_viet_tat_khop_hai_oid_la_KHONG_DO_DUOC),
    ("bien_nhan_sha_that_van_dem_RIENG",
     case_bien_nhan_sha_that_van_dem_RIENG),
]


def case_phan_loai_dot_bien_san_pham_neo_trung_test_van_DO(c: Ctx):
    """Neo sản phẩm chết phải lộ, dù nguyên văn neo vẫn nằm trong bảng MUTANTS."""
    ten = "tran_attempt_3_thanh_99"
    cap = _cap_thay_the(*MUTANTS[ten][:2])
    goc = c.script.read_text(encoding="utf-8")
    goc_test = Path(__file__).read_text(encoding="utf-8")
    for neo, _ in cap:
        if neo not in goc_test:
            raise AssertionError("fixture phải có neo trùng trong tệp test")
        goc = goc.replace(neo, "", 1)
    _, dot_bien_test, thieu = _phan_loai_dot_bien(ten, cap, goc, goc_test)
    if dot_bien_test or not thieu:
        raise AssertionError("không tìm thấy mỏ neo: neo sản phẩm chết đã bị nuốt")


def case_dot_bien_test_khai_bao_chay_va_giet_dung_ca(c: Ctx):
    """Mutant test-harness khai báo vẫn được nạp và giết đúng ca đích của nó."""
    ten = "bien_nhan_root_xuong_dong_tha_vo_dieu_kien"
    tim, thay, phai_chet = MUTANTS[ten]
    cap = _cap_thay_the(tim, thay)
    goc = c.script.read_text(encoding="utf-8")
    goc_test = Path(__file__).read_text(encoding="utf-8")
    than, dot_bien_test, thieu = _phan_loai_dot_bien(ten, cap, goc, goc_test)
    if not dot_bien_test or thieu:
        raise AssertionError(f"khai báo mutant test-harness không dùng được: {thieu!r}")
    for neo, thay_the in cap:
        than = than.replace(neo, thay_the, 1)
    mut_dir = c.tmp / "test_harness_mutant"
    mut_dir.mkdir(parents=True, exist_ok=True)
    script = mut_dir / "packet_loop.py"
    script.write_text(goc, encoding="utf-8", newline="\n")
    (mut_dir / "launcher.py").write_text(
        (HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
    test_mut = mut_dir / "packet_loop_test.py"
    test_mut.write_text(than, encoding="utf-8", newline="\n")
    spec = importlib.util.spec_from_file_location("packet_loop_test_khoa_neo", test_mut)
    suite = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(suite)
    ket = suite.chay_suite(script, mut_dir / "run", chi_chay=set(phai_chet))
    if set(ket) != set(phai_chet) or any(ket[t] is None for t in phai_chet):
        raise AssertionError(f"mutant test-harness không giết đúng ca đích: {ket!r}")


def case_dot_bien_test_neo_chet_van_DO(c: Ctx):
    """Khai nhắm test chỉ đổi tệp tra neo; nó không được làm chốt biến mất."""
    ten = "bien_nhan_root_xuong_dong_tha_vo_dieu_kien"
    cap = _cap_thay_the(*MUTANTS[ten][:2])
    goc = c.script.read_text(encoding="utf-8")
    goc_test = Path(__file__).read_text(encoding="utf-8")
    for neo, _ in cap:
        goc_test = goc_test.replace(neo, "", 1)
    _, dot_bien_test, thieu = _phan_loai_dot_bien(ten, cap, goc, goc_test)
    if not dot_bien_test or not thieu:
        raise AssertionError("không tìm thấy mỏ neo: neo test-harness chết đã bị nuốt")


def _ps_statements(script: str):
    stmts, cur, state, start, i, n, tb = [], [], "N", 0, 0, len(script), True
    while i < n:
        c, os = script[i], state
        if state == "N":
            if tb and script.startswith("<#", i): state = "B"; cur.extend([" ", " "]); i += 1
            elif tb and c == "#": state = "L"; cur.append(" ")
            elif script.startswith("@'\n", i) or script.startswith("@'\r\n", i): state = "H1"; cur.extend(["@", "'"]); i += 1
            elif script.startswith('@"\n', i) or script.startswith('@"\r\n', i): state = "H2"; cur.extend(["@", '"']); i += 1
            elif c == "'": state = "S1"; cur.append(c)
            elif c == '"': state = "S2"; cur.append(c)
            elif c == "`": state = "E"; tb = False
            elif c in ";\n":
                txt = "".join(cur).strip(" \t\r\n")
                if txt: stmts.append((start, i, txt))
                cur, start = [], i + 1; tb = True
            elif c in " \t\r": cur.append(c); tb = True
            else: cur.append(c); tb = c in ")]}"
        elif state == "L":
            if c == "\n": state = "N"; continue
            else: cur.append(" ")
        elif state == "B":
            if script.startswith("#>", i): state = "N"; cur.extend([" ", " "]); i += 1
            else: cur.append(" " if c != "\n" else "\n")
        elif state == "S1":
            cur.append(c)
            if c == "'":
                if i+1 < n and script[i+1] == "'": cur.append("'"); i += 1
                else: state = "N"
        elif state == "S2":
            cur.append(c)
            if c == '"':
                if i+1 < n and script[i+1] == '"': cur.append('"'); i += 1
                else: state = "N"
            elif c == "`": state = "E2"
        elif state == "E":
            state = "N"
            if c == "\n": cur.append(" ")
            elif c == "\r" and i+1 < n and script[i+1] == "\n": cur.append(" "); i += 1
            else: cur.extend(["`", c])
        elif state == "E2": state = "S2"; cur.append(c)
        elif state == "H1":
            if c == "\n" and script.startswith("'@", i+1): state = "N"; cur.extend(["\n", "'", "@"]); i += 2
            else: cur.append(" " if c != "\n" else "\n")
        elif state == "H2":
            if c == "\n" and script.startswith('"@', i+1): state = "N"; cur.extend(["\n", '"', "@"]); i += 2
            else: cur.append(" " if c != "\n" else "\n")
        if state == "N" and os in ("B", "S1", "S2", "H1", "H2"): tb = True
        i += 1
    if state in ("B", "S1", "S2", "H1", "H2", "E", "E2"):
        raise AssertionError("unfinished")
    txt = "".join(cur).strip(" \t\r\n")
    if txt: stmts.append((start, n, txt))
    return stmts


def _trich_xuat_powershell_74a(noi_dung: str) -> str:
    import re
    p = re.split(r'(\r\n|\r|\n)', noi_dung); lines = [p[i]+p[i+1] for i in range(0,len(p)-1,2)]+([p[-1]] if p[-1] else [])
    f_char, f_len, in_sec, n_head, blocks, cur, html_end = None, 0, False, 0, [], None, None
    for line in lines:
        if not f_char:
            if html_end:
                if html_end.search(line): html_end = None
                continue
            mh = re.match(r"(?i)^ {0,3}(?:(<!--)|<(pre|script|style|textarea)(?:[ \t\v\f\r\n>]|$))", line)
            if mh:
                end_re = re.compile(r"-->" if mh.group(1) else r"(?i)</(?:pre|script|style|textarea)>")
                if not end_re.search(line): html_end = end_re
                continue
        m = re.match(r"^ {0,3}(`{3,}|~{3,})(.*)$", line)
        if not f_char:
            if line.rstrip("\r\n") == "#### 7.4a Thứ tự state trước khi gọi reviewer":
                n_head, in_sec = n_head + 1, True
                continue
            if in_sec and re.match(r"^ {0,3}#{1,6}(?:[ \t\r\n]|$)", line): in_sec = False
            if m:
                f_char, f_len = m.group(1)[0], len(m.group(1))
                if in_sec and m.group(2).rstrip("\r\n").strip(" \t") == "powershell": cur = []
        else:
            if m and m.group(1)[0] == f_char and len(m.group(1)) >= f_len and not m.group(2).rstrip("\r\n").strip(" \t"):
                if cur is not None: blocks.append("".join(cur)); cur = None
                f_char, f_len = None, 0
            elif cur is not None: cur.append(line)
    errs = []
    if n_head != 1: errs.append("không tìm thấy duy nhất một mục #### 7.4a đúng chuẩn")
    if f_char: errs.append("unclosed fence")
    if not blocks: errs.append("không tìm thấy khối powershell sau 7.4a")
    elif len(blocks) > 1: errs.append("duplicate powershell fence")
    if errs: raise AssertionError(" | ".join(errs))
    return blocks[0].strip(" \t\r\n")


def _loc_lenh_truoc_record_post(doan_code: str) -> str:
    import re
    py_script = r"python \.claude/dev/packet_loop\.py"
    ws = r"[ \t]+"
    opt = r"[ \t]*"
    patterns = [
        r"\$Begin" + opt + r"=" + opt + py_script + ws + r"begin-attempt" + ws + r"--packet" + ws + r"<issue>" + ws + r"--provider" + ws + r"<executor-provider>",
        r"if" + opt + r"\(\$LASTEXITCODE" + ws + r"-ne" + ws + r"0\)" + opt + r"\{" + opt + r"exit" + ws + r"\$LASTEXITCODE" + opt + r"\}",
        r"if" + opt + r"\(\$Begin" + ws + r"-notmatch" + ws + r"'nonce=\(\[0-9a-f\]\{32\}\)'\)" + opt + r"\{" + opt + r"throw" + ws + r"'begin-attempt không in nonce hợp lệ'" + opt + r"\}",
        r"\$AttemptNonce" + opt + r"=" + opt + r"\$Matches\[1\]",
        py_script + ws + r"chup-anh-doctor" + ws + r"--packet" + ws + r"<issue>" + ws + r"--out" + ws + r"<doctor-signed.json>",
        py_script + ws + r"record-post" + ws + r"--packet" + ws + r"<issue>" + ws + r"--for" + ws + r"reviewing" + ws + r"--comment-id" + ws + r"<recorded-github-comment-id>"
    ]
    stmts = _ps_statements(doan_code)
    if len(stmts) < 6:
        raise AssertionError("thiếu lệnh")
    for idx, pat in enumerate(patterns):
        if not re.fullmatch(pat, stmts[idx][2]):
            raise AssertionError(f"lệnh {idx+1} sai template: {stmts[idx][2]}")
    return doan_code[:stmts[5][0]].strip(" \t\r\n")


def _kiem_residual_placeholder(lenh: str):
    import re
    for _, _, code in _ps_statements(lenh):
        if re.search(r"<[^>]+>", code):
            raise AssertionError(f"residual placeholder trong lệnh: {code}")


def case_luong_canonical_chay_that(c: Ctx):
    assert os.name == "nt", "phải chạy trên Windows"

    ke_hoach_md = ROOT / "ops" / "KE_HOACH_THI_CONG_CLAUDE_CODEX.md"
    if not ke_hoach_md.is_file():
        if (ROOT / ".git").exists():
            raise AssertionError("thiếu kế hoạch thi công trong repo thật")
        return

    doan_code = _trich_xuat_powershell_74a(ke_hoach_md.read_text(encoding="utf-8"))

    lenh_da_loc = _loc_lenh_truoc_record_post(doan_code)

    if not lenh_da_loc or "nonce" not in lenh_da_loc:
        raise AssertionError("tiền tố chạy lệnh rỗng hoặc thiếu logic nonce")

    sd = c.sd()
    rc, _, e = c.init(sd)
    _doi(0, rc, e, "init")

    lenh_da_loc = lenh_da_loc.replace("<issue>", "55")
    lenh_da_loc = lenh_da_loc.replace("<executor-provider>", EXECUTOR)
    sd_ps = "'" + str(sd).replace("'", "''") + "'"
    doctor_ps = "'" + str(sd / "doctor-signed.json").replace("'", "''") + "'"
    lenh_da_loc = lenh_da_loc.replace("packet_loop.py ", f"packet_loop.py --state-dir {sd_ps} ")
    lenh_da_loc = lenh_da_loc.replace("<doctor-signed.json>", doctor_ps)

    _kiem_residual_placeholder(lenh_da_loc)

    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env[BIEN_BC] = anh_doctor()

    try:
        p = subprocess.run(["pwsh", "-NoProfile", "-Command", lenh_da_loc], cwd=str(ROOT), capture_output=True, env=env)
    except OSError:
        raise AssertionError("thiếu pwsh trên Windows")

    _doi(0, p.returncode, p.stderr, f"luồng canonical chạy thất bại (stdout={_txt(p.stdout)!r})")

    import json as _json
    try:
        doc_data = _json.loads((sd / "doctor-signed.json").read_text(encoding="utf-8"))
    except Exception as ex:
        raise AssertionError(f"không đọc được doctor-signed.json: {ex}")
    st = _json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    neo = st["attempt_anchor"]
    if doc_data.get("nonce") != neo["nonce"]:
        raise AssertionError("nonce không khớp")
    if doc_data.get("attempt") != neo["attempt"]:
        raise AssertionError("attempt không khớp")
    if doc_data.get("chu_ky") != ky_ban_ghi_luot(doc_data, st["hmac_key"]):
        raise AssertionError("chữ ký không khớp")


def case_trich_xuat_74a_chong_nhieu(c: Ctx):
    def loi(func, match):
        try:
            func()
        except AssertionError as e:
            if match not in str(e):
                raise AssertionError(f"có lỗi nhưng không khớp {match!r}: {e}")
            return
        raise AssertionError(f"lọt {match}")

    t_chuan = "#### 7.4a Thứ tự state trước khi gọi reviewer\n"
    loi(lambda: _trich_xuat_powershell_74a("#### 7.4a\n```powershell\n```\n"), "đúng chuẩn")
    assert _trich_xuat_powershell_74a("\t```powershell\n" + t_chuan + "```powershell\n# ok\n```\n") == "# ok"
    loi(lambda: _trich_xuat_powershell_74a("#### 7.4a — SAI\n```powershell\n```\n"), "đúng chuẩn")
    loi(lambda: _trich_xuat_powershell_74a("### 7.4a Thứ tự state trước khi gọi reviewer\n```powershell\n```\n"), "đúng chuẩn")
    loi(lambda: _trich_xuat_powershell_74a("##### 7.4a Thứ tự state trước khi gọi reviewer\n```powershell\n```\n"), "đúng chuẩn")

    assert _trich_xuat_powershell_74a(t_chuan + "```powershell\n# #### comment\n```\n#### 8.0\n") == "# #### comment"
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "\n#### 8.0\n```powershell\n```\n"), "không tìm thấy khối powershell")
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "```powershell\n```\n```powershell\n```\n"), "duplicate powershell fence")
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "```powershell\n"), "unclosed fence")

    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "```\n#### 8.0\n```powershell\n```\n"), "không tìm thấy khối")
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "```\n#### 8.0\n"), "unclosed fence")
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "````\n```powershell\n```\n````\n"), "không tìm thấy khối")
    assert _trich_xuat_powershell_74a(t_chuan + "~~~powershell\n#### 8.0\n~~~\n") == "#### 8.0"

    loi(lambda: _trich_xuat_powershell_74a("````\n" + t_chuan + "````\n"), "không tìm thấy duy nhất một mục")
    loi(lambda: _trich_xuat_powershell_74a("````\n" + t_chuan), "không tìm thấy duy nhất một mục")
    loi(lambda: _trich_xuat_powershell_74a("   ````\n" + t_chuan + "```powershell\n```\n   ````\n"), "không tìm thấy duy nhất một mục")
    loi(lambda: _trich_xuat_powershell_74a("   ````\n" + t_chuan + "```powershell\n```\n"), "không tìm thấy duy nhất một mục #### 7.4a đúng chuẩn | unclosed fence")
    loi(lambda: _trich_xuat_powershell_74a("````\n````\xa0\n" + t_chuan + "```powershell\n```\n````\n"), "không tìm thấy duy nhất một mục")

    _kiem_residual_placeholder("cmd # <harmless>")
    loi(lambda: _kiem_residual_placeholder("cmd '<harmless>'"), "residual placeholder")
    loi(lambda: _kiem_residual_placeholder('cmd "<harmless>"'), "residual placeholder")
    loi(lambda: _kiem_residual_placeholder('cmd "a`"b # " <harmless>'), "residual placeholder")
    loi(lambda: _kiem_residual_placeholder('cmd "a""b # " <harmless>'), "residual placeholder")
    loi(lambda: _kiem_residual_placeholder("cmd 'a''b # ' <harmless>"), "residual placeholder")
    _kiem_residual_placeholder("# comment <harmless>\n\n")
    _kiem_residual_placeholder("<# <residual> #>")
    _kiem_residual_placeholder("@'\n<residual>\n'@")
    _kiem_residual_placeholder('@"\n<residual>\n"@')

    cmd_b = "$Begin = python .claude/dev/packet_loop.py begin-attempt --packet <issue> --provider <executor-provider>"
    cmd_e = "if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }"
    cmd_c = "if ($Begin -notmatch 'nonce=([0-9a-f]{32})') { throw 'begin-attempt không in nonce hợp lệ' }"
    cmd_a = "$AttemptNonce = $Matches[1]"
    cmd_d = "python .claude/dev/packet_loop.py chup-anh-doctor --packet <issue> --out <doctor-signed.json>"
    cmd_r = "python .claude/dev/packet_loop.py record-post --packet <issue> --for reviewing --comment-id <recorded-github-comment-id>"

    valid_code = f"{cmd_b}\n{cmd_e}\n{cmd_c}\n{cmd_a}\n{cmd_d} # doctor\n# c\n{cmd_r}"
    assert _loc_lenh_truoc_record_post(valid_code) == f"{cmd_b}\n{cmd_e}\n{cmd_c}\n{cmd_a}\n{cmd_d} # doctor\n# c"

    for f, t in [("<executor-provider>", "<executor-provider> # tail"), ("chup-anh-doctor --packet", "chup-anh-doctor <# note #> --packet"), ("}", "}# harmless"), ("}", "}<# harmless #>"), (")", ")<# harmless #>"), ("hợp lệ' }", "hợp lệ'<# harmless #> }")]:
        vc = valid_code.replace(f, t, 1)
        assert _loc_lenh_truoc_record_post(vc) == vc[:vc.rfind(cmd_r)].strip()
    assert _ps_statements("'x'# comment")[-1][2] == "'x'"
    vc = f"# start\n{valid_code}"
    assert _loc_lenh_truoc_record_post(vc) == vc[:vc.rfind(cmd_r)].strip()

    loi(lambda: _loc_lenh_truoc_record_post(valid_code.replace("<executor-provider>", "<executor-provider>#tail|Mark")), "lệnh 1 sai template")
    loi(lambda: _loc_lenh_truoc_record_post(valid_code.replace("chup-anh-doctor --packet", "chup-anh-doctor<# note #>--packet")), "lệnh 5 sai template")

    loi(lambda: _loc_lenh_truoc_record_post(f"{cmd_b}\n{cmd_r}"), "thiếu lệnh")
    loi(lambda: _loc_lenh_truoc_record_post(f"{cmd_b}\n{cmd_e}\n{cmd_c}\n{cmd_a}\n{cmd_d}\nexit 0\n{cmd_r}"), "lệnh 6 sai template")
    loi(lambda: _loc_lenh_truoc_record_post(f"{cmd_d}\n{cmd_b}\n{cmd_r}"), "thiếu lệnh")
    loi(lambda: _loc_lenh_truoc_record_post(f"{cmd_b}\n{cmd_e}\n{cmd_c}\n{cmd_a}\n{cmd_d} ; exit 0\n{cmd_r}"), "lệnh 6 sai template")
    loi(lambda: _loc_lenh_truoc_record_post(f"{cmd_b}\n{cmd_e}\n{cmd_c}\n{cmd_a}\npython .claude/dev/packet_loop.py chup-anh-doctor --packet <issue> --out <doctor-signed.json>|Get-Date\n{cmd_r}"), "lệnh 5 sai template")
    loi(lambda: _trich_xuat_powershell_74a("#### 7.4a Thứ tự state trước khi gọi reviewer\n```powershell\xa0\n```\n"), "không tìm thấy khối powershell")

    for tg, sp, cl in [("<!--", "", "-->"), ("<pre", "\f", "</pre>"), ("<SCRIPT", "\v", "</SCRIPT>"), ("<TeXtArEa", "", "</textarea>")]: loi(lambda t=tg, s=sp, c=cl: _trich_xuat_powershell_74a(f"{t}{s}\n{t_chuan}```powershell\nc\n```\n{c}\n"), "không tìm thấy duy nhất")
    loi(lambda: _trich_xuat_powershell_74a(f"<!--\n{t_chuan}```powershell\nc\n```\n"), "không tìm thấy duy nhất")
    for s in "\v\f\x1c\x1d\x1e\x85\u2028\u2029":
        loi(lambda s=s: _trich_xuat_powershell_74a(f"<!--\n-->{s}{t_chuan}```powershell\nc\n```\n"), "không tìm thấy")
    for o, c in ((o, c) for o in ["pre", "script", "style", "textarea"] for c in ["pre", "script", "style", "textarea"]):
        assert _trich_xuat_powershell_74a(f"<{o}>\n{t_chuan}```powershell\nc\n```\n</{c}>\n{t_chuan}```powershell\n# ok\n```\n") == "# ok"
    assert _trich_xuat_powershell_74a(f"<!--\n{t_chuan}```powershell\nc\n```\n-->\n{t_chuan}```powershell\n# ok\n```\n") == "# ok"

    # R8 Assertions
    loi(lambda: _loc_lenh_truoc_record_post(f"\xa0{valid_code}"), "lệnh 1 sai template")
    loi(lambda: _loc_lenh_truoc_record_post(f"{valid_code}\u2003"), "lệnh 6 sai template")
    loi(lambda: _loc_lenh_truoc_record_post(valid_code.replace("python .claude/dev/packet_loop.py", "python x|.claude/dev/packet_loop.py")), "lệnh 1 sai template")
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + " #### 8.0\n```powershell\n```\n"), "không tìm thấy khối")
    loi(lambda: _trich_xuat_powershell_74a(t_chuan + "   #### 8.0\n```powershell\n```\n"), "không tìm thấy khối")
    assert _trich_xuat_powershell_74a(t_chuan + "    #### 8.0\n```powershell\n# INSIDE\n```\n") == "# INSIDE"
    loi(lambda: _loc_lenh_truoc_record_post(valid_code + "\n<#"), "unfinished")
    loi(lambda: _loc_lenh_truoc_record_post(valid_code + "\n@'\n"), "unfinished")
    assert _loc_lenh_truoc_record_post(valid_code + "\n# eof") == f"{cmd_b}\n{cmd_e}\n{cmd_c}\n{cmd_a}\n{cmd_d} # doctor\n# c"


def case_windows_only_skip_khoa(c: Ctx):
    goc_sys = platform.system
    platform.system = lambda: "Linux"
    try:
        ket = chay_suite(c.script, c.tmp, chi_chay={"luong_canonical_chay_that"})
        if not isinstance(ket.get("luong_canonical_chay_that"), BoQua):
            raise AssertionError("chay_suite không ngắt WINDOWS_ONLY thành BoQua")
    finally:
        platform.system = goc_sys


CASES += [
    ("luong_canonical_chay_that", case_luong_canonical_chay_that),
    ("trich_xuat_74a_chong_nhieu", case_trich_xuat_74a_chong_nhieu),
    ("windows_only_skip_khoa", case_windows_only_skip_khoa),
    ("phan_loai_dot_bien_san_pham_neo_trung_test_van_DO",
     case_phan_loai_dot_bien_san_pham_neo_trung_test_van_DO),
    ("dot_bien_test_khai_bao_chay_va_giet_dung_ca",
     case_dot_bien_test_khai_bao_chay_va_giet_dung_ca),
    ("dot_bien_test_neo_chet_van_DO", case_dot_bien_test_neo_chet_van_DO),
]

WINDOWS_ONLY = {"luong_canonical_chay_that"}


def case_ag_identity_and_cross_family(c: Ctx):
    sd = c.sd()
    ag = ("--executor-model-family", "gemini", "--executor-execution-surface",
          "antigravity", "--executor-transport", "machine/local")
    rc, _, e = c.init(sd, executor="google_antigravity", reviewer="claude", extra=ag)
    _doi(0, rc, e, "AG identity init")
    state = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    if state["executor_identity"]["model_family"] != "gemini":
        raise AssertionError("AG model family not preserved")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "google_antigravity"], sd)
    _doi(2, rc, e, "AG runtime missing family")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "google_antigravity",
                             "--model-family", "claude", "--execution-surface", "antigravity",
                             "--transport", "machine/local"], sd)
    _doi(4, rc, e, "AG runtime wrong family")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "google_antigravity",
                             "--model-family", "gemini", "--execution-surface", "antigravity",
                             "--transport", "machine/local"], sd)
    _doi(0, rc, e, "AG runtime correct identity")
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "claude",
                             "--verdict", "approve", "--reviewed-sha", c.head(1)], sd)
    _doi(8, rc, e, "AG invalid review state")
    cid = "9000055002"
    rc, _, e = run(c.script, ["record-post", "--packet", 55, "--for", "reviewing",
                             "--comment-id", cid], sd)
    _doi(0, rc, e, "AG review post")
    rc, _, e = run(c.script, ["transition", "--packet", 55, "--to", "reviewing",
                             "--comment-id", cid, "--head-sha", c.head(1)], sd)
    _doi(0, rc, e, "AG reviewing transition")
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "claude",
                             "--verdict", "approve", "--reviewed-sha", "b" * 40], sd)
    _doi(5, rc, e, "AG stale reviewed SHA")
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "claude",
                             "--verdict", "approve", "--reviewed-sha", c.head(1)], sd)
    _doi(0, rc, e, "AG exact SHA review")
    sd2 = c.sd()
    rc, _, e = c.init(sd2, executor="google_antigravity", reviewer="claude",
                      extra=("--executor-model-family", "claude", *ag[2:]), lease=False)
    _doi(4, rc, e, "same family cross-review")
    sd3 = c.sd()
    rc, _, e = c.init(sd3, executor="google_antigravity", reviewer="claude", lease=False)
    _doi(2, rc, e, "AG missing identity")
    sd4 = c.sd()
    rc, _, e = c.init(sd4, executor="unknown", reviewer="claude", lease=False)
    _doi(2, rc, e, "unknown provider")
    for surface, transport in (("codex_cli", "machine/local"),
                               ("antigravity", "human_mediated"),
                               (" ", "machine/local")):
        invalid_sd = c.sd()
        rc, _, e = c.init(invalid_sd, executor="google_antigravity", reviewer="claude",
                          extra=("--executor-model-family", "gemini",
                                 "--executor-execution-surface", surface,
                                 "--executor-transport", transport), lease=False)
        _doi(2, rc, e, "AG unsupported executor surface/transport")
    sd5 = c.sd()
    rc, _, e = c.init(sd5, executor="codex", reviewer="google_antigravity",
                      extra=("--reviewer-model-family", "gemini", "--reviewer-execution-surface",
                             "antigravity", "--reviewer-transport", "machine/local"))
    _doi(0, rc, e, "AG reviewer identity init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "codex"], sd5)
    _doi(0, rc, e, "AG reviewer executor begin")
    cid = "9000055004"
    rc, _, e = run(c.script, ["record-post", "--packet", 55, "--for", "reviewing",
                             "--comment-id", cid], sd5)
    _doi(0, rc, e, "AG reviewer post")
    rc, _, e = run(c.script, ["transition", "--packet", 55, "--to", "reviewing",
                             "--comment-id", cid, "--head-sha", c.head(1)], sd5)
    _doi(0, rc, e, "AG reviewer transition")
    for family, surface, expected_rc in (("openai", "antigravity", 4),
                                         ("gemini", "codex_cli", 2)):
        rc, _, e = run(c.script, ["record-review", "--packet", 55,
                                 "--provider", "google_antigravity", "--model-family", family,
                                 "--execution-surface", surface, "--transport", "machine/local",
                                 "--verdict", "approve", "--reviewed-sha", c.head(1)], sd5)
        _doi(expected_rc, rc, e, "AG reviewer runtime identity mismatch")
        st = json.loads((sd5 / "wp55.json").read_text(encoding="utf-8"))
        if st["state"] != "reviewing" or st["reviews"]:
            raise AssertionError("failed AG review changed state or added verdict")
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "google_antigravity",
                             "--model-family", "gemini", "--execution-surface", "antigravity",
                             "--transport", "machine/local", "--verdict", "approve",
                             "--reviewed-sha", c.head(1)], sd5)
    _doi(0, rc, e, "AG reviewer exact SHA")
    for family, surface, transport in ((" ", "antigravity", "machine/local"),
                                       ("gemini", "codex_cli", "machine/local"),
                                       ("gemini", "antigravity", "human_mediated")):
        invalid_sd = c.sd()
        rc, _, e = c.init(invalid_sd, executor="codex", reviewer="google_antigravity",
                          extra=("--reviewer-model-family", family,
                                 "--reviewer-execution-surface", surface,
                                 "--reviewer-transport", transport), lease=False)
        _doi(2, rc, e, "AG unsupported reviewer identity")


CASES.append(("ag_identity_and_cross_family", case_ag_identity_and_cross_family))


def case_codex_runtime_surface_transport(c: Ctx):
    sd = c.sd()
    rc, _, e = c.init(sd, executor="codex", reviewer="claude",
                      extra=("--executor-execution-surface", "codex_desktop",
                             "--executor-transport", "machine/local"))
    _doi(0, rc, e, "Codex Desktop identity init")
    state = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    if state["executor_identity"]["execution_surface"] != "codex_desktop":
        raise AssertionError("Codex Desktop surface was replaced")
    for surface, transport, expected_rc in (("codex_cli", "machine/local", 4),
                                            ("codex_desktop", "service", 2)):
        rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "codex",
                                 "--execution-surface", surface, "--transport", transport], sd)
        _doi(expected_rc, rc, e, "Codex executor runtime mismatch")
        if c.state(sd, 55) != "leased":
            raise AssertionError("mismatched Codex runtime opened attempt")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "codex",
                             "--execution-surface", "codex_desktop", "--transport", "machine/local"], sd)
    _doi(0, rc, e, "Codex Desktop runtime match")

    sd2 = c.sd()
    rc, _, e = c.init(sd2, executor="claude", reviewer="codex",
                      extra=("--reviewer-execution-surface", "codex_desktop",
                             "--reviewer-transport", "machine/local"))
    _doi(0, rc, e, "Codex reviewer identity init")
    c.den_reviewing(sd2, 55, 1)
    for surface, transport, expected_rc in (("codex_cli", "machine/local", 4),
                                            ("codex_desktop", "service", 2)):
        rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex",
                                 "--execution-surface", surface, "--transport", transport,
                                 "--verdict", "approve", "--reviewed-sha", c.head(1)], sd2)
        _doi(expected_rc, rc, e, "Codex reviewer runtime mismatch")
        st = json.loads((sd2 / "wp55.json").read_text(encoding="utf-8"))
        if st["state"] != "reviewing" or st["reviews"]:
            raise AssertionError("mismatched Codex reviewer recorded verdict")
    run(c.script, ["record-codex-call", "--packet", 55, "--head", c.head(1), "--run-id", "g1"], sd2)
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex", "--codex-call", "g1",
                             "--execution-surface", "codex_desktop", "--transport", "machine/local",
                             "--verdict", "approve", "--reviewed-sha", c.head(1)], sd2)
    _doi(0, rc, e, "Codex Desktop reviewer match")

    legacy = c.sd()
    rc, _, e = c.init(legacy, executor="codex", reviewer="claude")
    _doi(0, rc, e, "legacy Codex init")
    state = json.loads((legacy / "wp55.json").read_text(encoding="utf-8"))
    if state["executor_identity"]["execution_surface"] is not None:
        raise AssertionError("legacy unknown Codex surface was fabricated")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "codex"], legacy)
    _doi(0, rc, e, "legacy unknown Codex runtime")

    service = c.sd()
    rc, _, e = c.init(service, executor="codex", reviewer="claude",
                      extra=("--executor-execution-surface", "codex_service",
                             "--executor-transport", "machine"))
    _doi(0, rc, e, "Codex service identity init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "codex",
                             "--execution-surface", "codex_service", "--transport", "machine"], service)
    _doi(0, rc, e, "Codex service runtime match")

    claude = c.sd()
    rc, _, e = c.init(claude, executor="claude", reviewer="codex",
                      extra=("--executor-execution-surface", "claude_code",
                             "--executor-transport", "machine/local"))
    _doi(0, rc, e, "Claude declared identity init")
    for surface, transport in (("codex_desktop", "machine/local"),
                               ("claude_code", "service")):
        rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "claude",
                                 "--execution-surface", surface, "--transport", transport], claude)
        _doi(2, rc, e, "Claude invalid runtime tuple")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", "claude",
                             "--execution-surface", "claude_code", "--transport", "machine/local"], claude)
    _doi(0, rc, e, "Claude declared runtime match")

    for provider, reviewer, surface, transport in (
            ("codex", "claude", "antigravity", "machine/local"),
            ("codex", "claude", "codex_service", "machine/local"),
            ("claude", "codex", "codex_desktop", "machine/local")):
        invalid = c.sd()
        rc, _, e = c.init(invalid, executor=provider, reviewer=reviewer,
                          extra=("--executor-execution-surface", surface,
                                 "--executor-transport", transport), lease=False)
        _doi(2, rc, e, "provider cannot declare foreign/invalid runtime tuple")


CASES.append(("codex_runtime_surface_transport", case_codex_runtime_surface_transport))


# --- #770 `kiem-gate` (spec `ops/specs/wp770.md` r1, M1–M5) --------------------------
#
# Mỗi ca ĐỎ đòi CẢ mã 12 LẪN lý do (`_doi_ly_do`) — mã trần trùng nhau không chứng minh
# chốt nào đã chạy. Mỗi chốt có đột biến riêng ở `MUTANTS.update` cuối khối.
_KG_HEAD = "ab" * 20
# #788: suite neo mặc định = 1 CÓ CHỦ Ý — `True == 1` trong Python, nên chốt bool của
# `check_suite.id` hỏng là ca `kg_n2_suite_id_bool` XANH chứ không chỉ đổi lý do.
_KG_SUITE, _KG_SUITE_KHAC = 1, 9


def _kg_run(i, name="gate", conclusion="success", status="completed", head=_KG_HEAD, suite=_KG_SUITE):
    return {"id": i, "name": name, "head_sha": head, "status": status, "conclusion": conclusion,
            "check_suite": {"id": suite}}


def _kg_dem(du_lieu):
    """#788 N5: `total_count` nay BẮT BUỘC. Trang nào chưa khai thì điền ĐÚNG số id phân biệt
    trên mọi trang (bản sao, không sửa hằng). Ca đo chính chốt ấy truyền `dem=False`."""
    du_lieu = json.loads(json.dumps(du_lieu))
    trang = [t for t in (du_lieu if isinstance(du_lieu, list) else [du_lieu])
             if isinstance(t, dict) and isinstance(t.get("check_runs"), list)]
    so = len({json.dumps(r.get("id")) for t in trang for r in t["check_runs"] if isinstance(r, dict)})
    for t in trang:
        t.setdefault("total_count", so)
    return du_lieu


# #822 M6: CLI sập (traceback, hoặc rc ngoài bộ `RC_*` của chính lệnh — Python sập trả 1) KHÔNG phải tín
# hiệu ca đích. `_doi` bọc traceback thành `AssertionError` nên bộ chạy từng cấp tín dụng cho đột biến sập
# (đo lượt 1 wp822: F02 `ValueError→TypeError`). Lớp RIÊNG, mã sản phẩm không ném được; `chay_suite` dò
# nó trên CẢ CHUỖI ngoại lệ, nên một `except … raise AssertionError` đổi kiểu cũng không rửa được (bài học
# `TinHieuChotCa`, CLAUDE.md).
class CliSapDo(Exception):
    pass


class _TinDungGia(str):
    """Ca ĐỎ vì CLI sập (#822 M6) — vẫn là chuỗi lỗi với mọi chỗ đọc `ket`, nhưng không phải GIẾT."""


def _co_sap_do(ex) -> bool:
    thay, cho = set(), [ex]   # CẢ `__cause__` LẪN `__context__`: `raise … from None` vẫn giữ context
    while cho:
        ex = cho.pop()
        if ex is None or id(ex) in thay:
            continue
        if isinstance(ex, CliSapDo):
            return True
        thay.add(id(ex))
        cho += [ex.__cause__, ex.__context__]
        if isinstance(ex, getattr(sys.modules["builtins"], "BaseExceptionGroup", ())):
            cho += list(ex.exceptions)
    return False


def _phan_loai_giet(v) -> str:
    return ("SONG" if v is None else "BO_QUA" if isinstance(v, BoQua)
            else "TIN_DUNG_GIA" if isinstance(v, _TinDungGia) else "GIET")


_KG_RC_HOP_LE = frozenset((0, 2, 12))


_KG_BANNER = b"Traceback (most recent call last)"


def _co_banner(b: bytes) -> bool:
    """Thô HOẶC sau ≤3 lớp giải escape (JSON/repr lồng nhau). MỘT hàm cho cả đầu vào lẫn đầu ra (review 3)."""
    for _ in range(4):   # thô + 3 lớp
        if _KG_BANNER in b:
            return True
        b = b.decode("unicode_escape", "ignore").encode("latin-1", "ignore")
    return False


def _kg_kiem_ket_qua(rc, o, e, cmd=()):
    """#822 M6 (review 1–2): KHÔNG đoán vỏ trình bày (đầu dòng, JSON, repr, tiền tố log — mỗi lượt một vỏ mới).
    Đảo lại: ĐẦU VÀO bị cấm mang banner, nên banner ở BẤT KỲ đâu trên stdout/stderr chỉ có thể do CLI tự in."""
    tep = cmd[cmd.index("--check-runs") + 1] if "--check-runs" in cmd else None
    vao = [str(x).encode("utf-8", "surrogatepass") for x in cmd]
    if tep and Path(tep).is_file():
        vao.append(Path(tep).read_bytes())   # `_co_banner` tự giải escape JSON (`\\u0054…`) — không cần json.loads
    if any(_co_banner(b) for b in vao):
        raise AssertionError("fixture kiem-gate KHÔNG được mang banner traceback — lỗi viết test, không phải tín hiệu")
    sap = any(_co_banner(out) for out in (o, e))
    if sap or rc not in _KG_RC_HOP_LE:
        raise CliSapDo(f"kiem-gate SẬP: rc={rc}; stdout={_txt(o)[-300:]!r}; stderr={_txt(e)[-300:]!r}")


def _kg(c: Ctx, du_lieu, *bat_buoc, head=_KG_HEAD, tho=None, suite=_KG_SUITE, dem=True):
    f = c.tmp / f"cr{time.time_ns()}.json"
    if isinstance(tho, bytes):
        f.write_bytes(tho)
    elif du_lieu is not None or tho is not None:
        f.write_text(tho if tho is not None else json.dumps(_kg_dem(du_lieu) if dem else du_lieu),
                     encoding="utf-8")
    args = ["kiem-gate", "--check-runs", f] + (["--head", head] if head is not None else [])
    args += ["--check-suite", suite] if suite is not None else []
    for t in bat_buoc:
        args += ["--bat-buoc", t]
    return run(c.script, args)


def _kg_ca(du_lieu, bat_buoc=("gate",), expect=12, chua="", head=_KG_HEAD, tho=None, suite=_KG_SUITE,
           dem=True, dong_xanh=None):
    def ca(c: Ctx):
        rc, o, e = _kg(c, du_lieu, *bat_buoc, head=head, tho=tho, suite=suite, dem=dem)
        if expect == 0:
            _doi(0, rc, e, "gate phải XANH")
            if f"(suite {suite})" not in _txt(o):   # N6: dòng xanh nêu suite đã neo
                raise AssertionError(f"dòng xanh thiếu suite {suite}: {_txt(o)!r}")
            for t in dict.fromkeys(bat_buoc):
                if _txt(o).count(f"{t} id=") != 1:
                    raise AssertionError(f"dòng xanh phải liệt kê {t!r} đúng MỘT lần: {_txt(o)!r}")
            if dong_xanh is not None and _txt(o) != dong_xanh:   # #822 r5: NGUYÊN VĂN (head, id lớn nhất, thứ tự `--bat-buoc`)
                raise AssertionError(f"dòng xanh đòi {dong_xanh!r}, được {_txt(o)!r}")
        else:
            _doi_ly_do(expect, rc, e, chua, "kiem-gate")
    ca.kw = dict(du_lieu=du_lieu, bat_buoc=bat_buoc, expect=expect, chua=chua, head=head, tho=tho, suite=suite, dem=dem,
                 dong_xanh=dong_xanh)   # #856 T6: bản sửa dựng từ đúng fixture của ca
    return ca


_KG_1 = {"total_count": 1, "check_runs": [_kg_run(1)]}
_KG_KDD = "KHÔNG ĐO ĐƯỢC"
_KG_TRANG = "không phải object có `check_runs` là list"   # #822 M3: lý do của ĐÚNG cửa chặn
_KG_CA = {
    # M1 — đối số
    "kg_m1_thieu_head": _kg_ca(_KG_1, head=None, expect=2, chua="--head"),
    "kg_m1_head_7_ky_tu": _kg_ca({"check_runs": [_kg_run(1, head="abababa")]},
                                 head="abababa", expect=2, chua="SHA 40"),
    "kg_m1_khong_bat_buoc": _kg_ca(_KG_1, bat_buoc=(), expect=2, chua="--bat-buoc"),
    "kg_m1_bat_buoc_rong": _kg_ca({"check_runs": [_kg_run(1, name="")]}, bat_buoc=("",), expect=2, chua="không được rỗng"),
    "kg_m1_trung_ten_mot_dong": _kg_ca(_KG_1, bat_buoc=("gate", "gate"), expect=0),
    # M2 — đọc đầu vào: mọi chỗ hỏng là KHÔNG ĐO ĐƯỢC + 12
    "kg_m2_tep_vang": _kg_ca(None, chua="như JSON (FileNotFoundError"),
    "kg_m2_json_hong": _kg_ca(None, tho="{", chua="như JSON (JSONDecodeError"),
    "kg_m2_khong_co_check_runs": _kg_ca({"total_count": 1, "x": 1}, chua=_KG_TRANG),
    "kg_m2_check_runs_khong_phai_list": _kg_ca({"total_count": 1, "check_runs": {"gate": _kg_run(1)}}, chua=_KG_TRANG),
    # Chỉ conclusion vắng: giữ số id đúng; run hỏng không bắt buộc để gỡ kiểm không KeyError.
    "kg_m2_thieu_conclusion": _kg_ca(
        {"total_count": 2, "check_runs": [_kg_run(1), {k: v for k, v in _kg_run(2, name="khac").items() if k != "conclusion"}]},
        chua="trường ['conclusion']"),
    "kg_m2_id_bool": _kg_ca({"check_runs": [_kg_run(True)]}, chua="trường ['id']"),
    "kg_m2_id_chuoi": _kg_ca({"check_runs": [_kg_run("5")]}, chua="trường ['id']"),
    "kg_m2_thieu_trang": _kg_ca({"total_count": 3, "check_runs": [_kg_run(1)]}, chua="thiếu trang"),
    "kg_m2_object_mot_trang": _kg_ca({"total_count": 1, "check_runs": [_kg_run(1)]}, expect=0),
    "kg_m2_list_nhieu_trang": _kg_ca(
        [{"total_count": 2, "check_runs": [_kg_run(1, conclusion="cancelled")]},
         {"total_count": 2, "check_runs": [_kg_run(2)]}], expect=0),
    # M3 — luật xanh
    "kg_m3_vang": _kg_ca({"check_runs": [_kg_run(1, name="khac")]}, chua="VẮNG"),
    "kg_m3_huy_moi_nhat": _kg_ca(
        {"check_runs": [_kg_run(1), _kg_run(2, conclusion="cancelled")]}, chua="'cancelled'"),
    "kg_m3_chay_lai_xanh": _kg_ca(
        {"check_runs": [_kg_run(1, conclusion="cancelled"), _kg_run(2)]}, expect=0),
    "kg_m3_in_progress": _kg_ca({"check_runs": [_kg_run(1, conclusion=None, status="in_progress")]},
                                chua="'in_progress'"),
    "kg_m3_head_khac": _kg_ca({"check_runs": [_kg_run(1, head="cd" * 20)]}, chua="cd" * 20),
    "kg_m3_ten_tuyet_doi": _kg_ca(
        {"check_runs": [_kg_run(1, name="gate (ubuntu-latest) extra"), _kg_run(2, name="gate")]},
        bat_buoc=("gate (ubuntu-latest)",), chua="VẮNG"),
    "kg_m3_ngoai_bo_qua": _kg_ca(
        {"check_runs": [_kg_run(1), _kg_run(2, name="khac", conclusion="cancelled")]}, expect=0),
    # Trùng `id` lớn nhất: MỌI bản ghi của id ấy phải xanh — không tự chọn bản thuận lợi.
    "kg_m3_trung_id_moi_ban_phai_xanh": _kg_ca(
        {"check_runs": [_kg_run(2), _kg_run(2, conclusion="cancelled")]}, chua="'cancelled'"),
}
# F01 — không để parser xoá bằng chứng mâu thuẫn hoặc nhận hằng ngoài JSON.
for _k, _v in {"id": 2, "name": "khac", "head_sha": "cd" * 20, "status": "in_progress",
               "conclusion": "cancelled", "check_suite": {"id": _KG_SUITE_KHAC}}.items():
    _raw = "{" + json.dumps(_k) + ":" + json.dumps(_v) + "," + json.dumps(_kg_run(1))[1:]
    for _slurp in (False, True):
        _page = '{"total_count":1,"check_runs":[' + _raw + "]}"
        _KG_CA[f"kg_m2_khoa_trung_{_k}_{_slurp}"] = _kg_ca(
            None, tho="[" + _page + "]" if _slurp else _page, chua="khoá trùng")
for _k, _v in {"check_runs": [_kg_run(2, conclusion="cancelled")], "total_count": 2}.items():
    _page = "{" + json.dumps(_k) + ":" + json.dumps(_v) + ',"total_count":1,"check_runs":' + json.dumps([_kg_run(1)]) + "}"
    _KG_CA[f"kg_m2_khoa_trung_{_k}"] = _kg_ca(None, tho=_page, chua="khoá trùng")
for _token in ("NaN", "Infinity", "-Infinity"):
    for _nested in (False, True):
        _value = '{"x":' + _token + "}" if _nested else _token
        _raw = json.dumps(_KG_1)[:-1] + ',"extra":' + _value + "}"
        _KG_CA[f"kg_m2_hang_ngoai_json_{_token}_{_nested}"] = _kg_ca(None, tho=_raw, chua="không thuộc JSON chuẩn")
# F02 — một điều kiện sai, hai điều kiện kia đúng; bắt riêng luật status.
_KG_CA["kg_m3_in_progress_success"] = _kg_ca(
    {"check_runs": [_kg_run(1, status="in_progress")]}, chua="status='in_progress'")

# M3-ket-luan — mỗi giá trị một ca: luật là danh sách CHO PHÉP `success`.
_KG_KET_LUAN = ("skipped", "neutral", "failure", "timed_out", "action_required", "stale", None)
for _kl in _KG_KET_LUAN:
    _KG_CA[f"kg_m3_ket_luan_{_kl}"] = _kg_ca({"check_runs": [_kg_run(1, conclusion=_kl)]},
                                            chua=f"conclusion={_kl!r}")


# --- #788 (spec `ops/specs/wp788.md` r1, N1–N7) ------------------------------------------
_KG_ARG = "--check-suite phải là"
_KG_CA["kg_n1_thieu_check_suite"] = _kg_ca(_KG_1, suite=None, expect=2, chua="--check-suite")
for _ten, _gt in {"abc": "abc", "am": "-1", "0": "0", "012": "012", "cong": "+5", "cach": " 1",
                  "unicode": "1\u0661"}.items():
    _KG_CA[f"kg_n1_check_suite_{_ten}"] = _kg_ca(   # #856 M3: neo JSON ở int(đối số) khi parse được
        {"check_runs": [_kg_run(1, suite=int(_gt))]} if _ten != "abc" else _KG_1, suite=_gt, expect=2, chua=_KG_ARG)
_KG_CS = "`check_suite` không phải object"
_VANG_T = object()
_kg_cs = lambda cs: {k: v for k, v in _kg_run(1).items() if k != "check_suite"} | (
    {} if cs is _VANG_T else {"check_suite": cs})
for _ten, _cs in {"thieu": _VANG_T, "null": None, "list": [1], "thieu_id": {},
                  "id_bool": {"id": True}, "id_chuoi": {"id": "105"}}.items():
    _KG_CA[f"kg_n2_suite_{_ten}"] = _kg_ca({"check_runs": [_kg_cs(_cs)]}, chua=_KG_CS,
                                         suite="105" if _ten == "id_chuoi" else _KG_SUITE)
_KG_CA["kg_n2_run_khong_bat_buoc_thieu_suite"] = _kg_ca(
    {"check_runs": [_kg_run(1), {**_kg_cs(_VANG_T), "id": 2, "name": "khac"}]}, chua=_KG_CS)
_KG_N3_PRODUCER = {"check_runs": [_kg_run(1, conclusion="failure"), _kg_run(2, suite=_KG_SUITE_KHAC)]}
_KG_N3_CU_HON = {"check_runs": [_kg_run(1, conclusion="failure", suite=_KG_SUITE_KHAC),
                                _kg_run(2, conclusion="cancelled"), _kg_run(3)]}
_KG_CA.update({
    "kg_n3_producer": _kg_ca(_KG_N3_PRODUCER, chua="conclusion='failure'"),
    "kg_n3_vang": _kg_ca({"check_runs": [_kg_run(1, suite=_KG_SUITE_KHAC)]}, chua="VẮNG"),
    "kg_n3_chay_lai": _kg_ca({"check_runs": [_kg_run(1, conclusion="cancelled"), _kg_run(2)]}, expect=0),
    # Suite khác có run id NHỎ HƠN: phân biệt "lọc theo suite đã neo" với "lọc theo suite của run đầu".
    "kg_n3_chay_lai_suite_khac_cu_hon": _kg_ca(_KG_N3_CU_HON, expect=0),
    # N5 — `total_count` phải có, là số nguyên ≥ 0, cùng mọi trang, BẰNG ĐÚNG số id.
    "kg_n5_thieu": _kg_ca({"check_runs": [_kg_run(1)]}, dem=False, chua="thiếu `total_count`"),
    "kg_n5_thieu_o_trang_sau": _kg_ca([{"total_count": 2, "check_runs": [_kg_run(1, conclusion="cancelled")]},
                                       {"check_runs": [_kg_run(2)]}], dem=False, chua="trang 1 thiếu `total_count`"),
    "kg_n5_khong_voi_mot_run": _kg_ca({"total_count": 0, "check_runs": [_kg_run(1)]}, chua="THỪA id"),
    "kg_n5_khai_3_co_2": _kg_ca({"total_count": 3, "check_runs": [_kg_run(1, conclusion="cancelled"),
                                                                  _kg_run(2)]}, chua="thiếu trang"),
    "kg_n5_khai_1_co_2": _kg_ca({"total_count": 1, "check_runs": [_kg_run(1, conclusion="cancelled"),
                                                                  _kg_run(2)]}, chua="THỪA id"),
    "kg_n5_lech_trang": _kg_ca([{"total_count": 2, "check_runs": [_kg_run(1, conclusion="cancelled")]},
                                {"total_count": 3, "check_runs": [_kg_run(2)]}], chua="khác nhau"),
})
for _ten, _tc in {"am": -1, "bool": True, "thuc": 1.0, "chuoi": "1", "null": None}.items():
    _KG_CA[f"kg_n5_{_ten}"] = _kg_ca({"total_count": _tc, "check_runs": [_kg_run(1)]}, chua="≥ 0")

# F01 (cross-review lượt 1, H3): cùng `id` mà khác danh tính ⇒ KHÔNG ĐO ĐƯỢC, kể cả khi mọi
# phép đếm đều đúng; bản trùng NHẤT QUÁN vẫn được (trang lặp hợp lệ).
_KG_DT = "mang hai danh tính"
_KG_CA.update({
    "kg_f01_cung_id_khac_suite": _kg_ca(
        {"total_count": 1, "check_runs": [_kg_run(1), _kg_run(1, suite=_KG_SUITE_KHAC, conclusion="failure")]},
        dem=False, chua=_KG_DT),
    "kg_f01_cung_id_khac_ten": _kg_ca(
        {"total_count": 1, "check_runs": [_kg_run(1), _kg_run(1, name="khac", conclusion="failure")]},
        dem=False, chua=_KG_DT),
    "kg_f01_cung_id_hai_ten_bat_buoc": _kg_ca(
        {"total_count": 1, "check_runs": [_kg_run(1), _kg_run(1, name="gate2")]},
        bat_buoc=("gate", "gate2"), dem=False, chua=_KG_DT),
    "kg_f01_cung_id_khac_suite_hai_trang": _kg_ca(
        [{"total_count": 1, "check_runs": [_kg_run(1)]},
         {"total_count": 1, "check_runs": [_kg_run(1, suite=_KG_SUITE_KHAC, conclusion="failure")]}],
        dem=False, chua=_KG_DT),
    "kg_f01_cung_id_nhat_quan_hai_trang": _kg_ca(
        [{"total_count": 1, "check_runs": [_kg_run(1)]}, {"total_count": 1, "check_runs": [_kg_run(1)]}],
        dem=False, expect=0),
})

# F04 lượt 4 (chủ kho chốt 18-10): tên bắt buộc chứa ký tự ngắt dòng ⇒ RC_ARG; tab và chuỗi
# hai ký tự `\` + `n` không phải ngắt dòng nên vẫn được.
for _ten, _kt in {"lf": "\n", "cr": "\r", "crlf": "\r\n", "vt": "\x0b", "ff": "\x0c", "fs": "\x1c",
                  "nel": "\x85", "ls": "\u2028", "ps": "\u2029"}.items():
    _KG_CA[f"kg_f04_xuong_dong_{_ten}"] = _kg_ca({"check_runs": [_kg_run(1, name=f"ga{_kt}te")]}, bat_buoc=(f"ga{_kt}te",),
                                                 expect=2, chua="xuống dòng")
_KG_CA["kg_f04_xuong_dong_cuoi"] = _kg_ca({"check_runs": [_kg_run(1, name="gate\n")]}, bat_buoc=("gate\n",), expect=2,
                                          chua="xuống dòng")
for _ten, _t in {"tab": "ga\tte", "cheo_n": "ga\\nte"}.items():
    _KG_CA[f"kg_f04_ten_hop_le_{_ten}"] = _kg_ca({"check_runs": [_kg_run(1, name=_t)]}, bat_buoc=(_t,), expect=0)


def case_kg_f02_suite_vuot_tran_int(c: Ctx):
    """F02: đúng dạng N1 mà dài hơn trần chữ số của `int()` ⇒ VẮNG rc=12, KHÔNG traceback."""
    rc, _, e = _kg(c, _KG_1, "gate", suite="1" * 4301)
    _doi_ly_do(12, rc, e, "VẮNG", "kiem-gate --check-suite 4301 chữ số")
    if "Traceback" in _txt(e):
        raise AssertionError(f"không được traceback: {_txt(e)[-300:]!r}")


def case_kg_n4_canh_bao(c: Ctx):
    """N4: đúng MỘT dòng mỗi tên bắt buộc có run ở suite khác; 0 dòng cho tên không bắt buộc;
    mã thoát do luật xanh quyết, cảnh báo không đổi nó. Kiểm NGAY sau từng lệnh."""
    dem = lambda e: [d for d in _txt(e).splitlines() if d.startswith("CẢNH BÁO:")]
    rc, _, e = _kg(c, _KG_N3_PRODUCER, "gate")
    _doi(12, rc, e, "producer khác: gate đỏ vì suite neo đỏ")
    if dem(e) != ["CẢNH BÁO: 'gate' có 1 run ở suite khác (2) — bỏ qua"]:
        raise AssertionError(f"đòi đúng MỘT dòng cảnh báo cho 'gate': {dem(e)!r}")
    rc, _, e = _kg(c, {"check_runs": [_kg_run(1), _kg_run(2, name="khac", suite=_KG_SUITE_KHAC)]}, "gate")
    _doi(0, rc, e, "tên KHÔNG bắt buộc ở suite khác")
    if dem(e):
        raise AssertionError(f"tên không bắt buộc không được cảnh báo: {dem(e)!r}")
    rc, _, e = _kg(c, _KG_N3_CU_HON, "gate")
    _doi(0, rc, e, "cảnh báo không đổi mã thoát")
    if dem(e) != ["CẢNH BÁO: 'gate' có 1 run ở suite khác (1) — bỏ qua"]:
        raise AssertionError(f"ca xanh vẫn phải cảnh báo: {dem(e)!r}")
    rc, _, e = _kg(c, [{"total_count": 2, "check_runs": [_kg_run(1), _kg_run(2, suite=_KG_SUITE_KHAC)]},
                       {"total_count": 2, "check_runs": [_kg_run(2, suite=_KG_SUITE_KHAC)]}], "gate")
    if rc != 0 or dem(e) != ["CẢNH BÁO: 'gate' có 1 run ở suite khác (2) — bỏ qua"]:   # F05
        raise AssertionError(f"bản lặp là MỘT run: rc={rc} {dem(e)!r}")
    t = "reviewer's gate"   # F04: tên in nguyên văn trong nháy đơn, không theo repr
    rc, _, e = _kg(c, {"check_runs": [_kg_run(1, name=t), _kg_run(2, name=t, suite=_KG_SUITE_KHAC)]}, t)
    if rc != 0 or dem(e) != [f"CẢNH BÁO: '{t}' có 1 run ở suite khác (2) — bỏ qua"]:
        raise AssertionError(f"tên nguyên văn: rc={rc} {dem(e)!r}")
    # #822 r2: ≥2 id phân biệt + bản lặp + HAI tên bắt buộc cùng một ca (đếm, liệt kê đủ id, đủ tên).
    rc, _, e = _kg(c, {"check_runs": [_kg_run(1), _kg_run(2, name="gate2"), _kg_run(3, suite=9), _kg_run(4, suite=9),
                                      _kg_run(4, suite=9), _kg_run(5, name="gate2", suite=9)]}, "gate", "gate2")
    if rc != 0 or dem(e) != ["CẢNH BÁO: 'gate' có 2 run ở suite khác (3, 4) — bỏ qua",
                             "CẢNH BÁO: 'gate2' có 1 run ở suite khác (5) — bỏ qua"]:
        raise AssertionError(f"cảnh báo phải đủ tên và id phân biệt: rc={rc} {dem(e)!r}")


def case_kg_n6_help(c: Ctx):
    rc, o, e = run(c.script, ["kiem-gate", "--help"])
    t = _txt(o).replace("\n", " ")
    for can in ("--check-suite", "check_suite_id", "actions/runs/", "filter=all"):
        if rc != 0 or can not in t:
            raise AssertionError(f"--help của kiem-gate thiếu {can!r}: {t!r}")


# N7: cắt từ JSON check-runs THẬT của `bb8c0c4` (`gh api --paginate --slurp "repos/ducthangho/
# tra-luat/commits/bb8c0c4…/check-runs?filter=all&per_page=100"`, đo 17-10-2026: 1 trang,
# `total_count` 32 — spec đo 30 lúc 16-10, hai lượt `thu-hoi` đến sau). Mọi run `completed`,
# cùng `app` 15368; chỉ bỏ trường lệnh không đọc. Cột: id · check_suite.id · conclusion · name.
_KG_THAT_HEAD = "bb8c0c41d37ea5d7eddef254ea9079518e114890"
_KG_THAT = """\
116911923097 105371237228 success thu-hoi
116911938097 105371250078 success chuan-bi
116911939487 105371249716 skipped launcher
116912042882 105371250078 success gate-packet-loop (ubuntu-latest)
116912042979 105371250078 cancelled gate-ops (ubuntu-latest)
116912042994 105371250078 cancelled gate-cong-cu (ubuntu-latest, 4)
116912043019 105371250078 cancelled gate-cong-cu (ubuntu-latest, 0)
116912043029 105371250078 cancelled gate-cong-cu (ubuntu-latest, 1)
116912043048 105371250078 cancelled gate-cong-cu (ubuntu-latest, 7)
116912043074 105371250078 cancelled gate-cong-cu (ubuntu-latest, 3)
116912043090 105371250078 cancelled gate-cong-cu (ubuntu-latest, 2)
116912043092 105371250078 success gate-registry (ubuntu-latest)
116912043094 105371250078 success gate (ubuntu-latest)
116912043162 105371250078 cancelled gate-cong-cu (ubuntu-latest, 6)
116912043211 105371250078 cancelled gate-cong-cu (ubuntu-latest, 5)
116915400395 105371250078 cancelled gate-cong-cu-gop
116968288225 105371250078 success chuan-bi
116968376214 105371250078 success gate (ubuntu-latest)
116968376237 105371250078 success gate-registry (ubuntu-latest)
116968376242 105371250078 success gate-cong-cu (ubuntu-latest, 0)
116968376281 105371250078 success gate-cong-cu (ubuntu-latest, 5)
116968376298 105371250078 success gate-packet-loop (ubuntu-latest)
116968376337 105371250078 success gate-cong-cu (ubuntu-latest, 6)
116968376346 105371250078 success gate-cong-cu (ubuntu-latest, 7)
116968376359 105371250078 success gate-cong-cu (ubuntu-latest, 2)
116968376391 105371250078 success gate-ops (ubuntu-latest)
116968376441 105371250078 success gate-cong-cu (ubuntu-latest, 4)
116968376482 105371250078 success gate-cong-cu (ubuntu-latest, 3)
116968377756 105371250078 success gate-cong-cu (ubuntu-latest, 1)
116979365158 105371250078 success gate-cong-cu-gop (ubuntu-latest)
116980148107 105428551057 success thu-hoi
117001304665 105446307702 success thu-hoi
"""
_KG_THAT_JSON = {"total_count": 32, "check_runs": [
    {"id": int(i), "name": ten, "head_sha": _KG_THAT_HEAD, "status": "completed", "conclusion": kl,
     "app": {"id": 15368, "slug": "github-actions"}, "check_suite": {"id": int(cs)}}
    for i, cs, kl, ten in (d.split(" ", 3) for d in _KG_THAT.splitlines())]}
_KG_CI14 = ("chuan-bi", "gate (ubuntu-latest)", "gate-registry (ubuntu-latest)", "gate-ops (ubuntu-latest)",
            "gate-packet-loop (ubuntu-latest)", "gate-cong-cu-gop (ubuntu-latest)",
            *(f"gate-cong-cu (ubuntu-latest, {k})" for k in range(8)))
_KG_CA["kg_n7_that_suite_ci"] = _kg_ca(_KG_THAT_JSON, bat_buoc=_KG_CI14, expect=0, head=_KG_THAT_HEAD,
                                       suite="105371250078", dem=False)
_KG_CA["kg_n7_that_suite_thu_hoi"] = _kg_ca(_KG_THAT_JSON, bat_buoc=_KG_CI14, head=_KG_THAT_HEAD,
                                            suite="105371237228", dem=False, chua="VẮNG")


def case_kg_m4_rc_gate_12(c: Ctx):
    rc, _, e = _kg(c, {"check_runs": [_kg_run(1, conclusion="cancelled")]}, "gate")
    _doi(12, rc, e, "gate đỏ phải trả ĐÚNG 12")
    nguon = c.script.read_text(encoding="utf-8")
    if "\nRC_GATE = 12\n" not in nguon or not re.search(r"^\s+12\s+`kiem-gate`", nguon, re.M):
        raise AssertionError("thiếu `RC_GATE = 12` hoặc dòng 12 trong bảng mã thoát docstring")
    rc, o, e = run(c.script, ["kiem-gate", "--help"])
    if rc != 0 or "12 gate không xanh" not in _txt(o).replace("\n", " "):
        raise AssertionError(f"--help của kiem-gate thiếu mã 12: {_txt(o)!r}")


CASES += list(_KG_CA.items()) + [("kg_m4_rc_gate_12", case_kg_m4_rc_gate_12),
                                 ("kg_n4_canh_bao", case_kg_n4_canh_bao), ("kg_n6_help", case_kg_n6_help),
                                 ("kg_f02_suite_vuot_tran_int", case_kg_f02_suite_vuot_tran_int)]

_KG_CAM = [f"kg_m3_ket_luan_{k}" for k in _KG_KET_LUAN if k != "failure"]
MUTANTS.update({
    "kg_bo_status_rieng": ('r["status"] == "completed" and r["conclusion"] == "success"',
                           'r["conclusion"] == "success"', ["kg_m3_in_progress_success"]),
    "kg_bo_conclusion_rieng": ('r["status"] == "completed" and r["conclusion"] == "success"',
                               'r["status"] == "completed"', [f"kg_m3_ket_luan_{k}" for k in _KG_KET_LUAN]),
    "kg_bo_hook_khoa_trung": ("object_pairs_hook=_cam_khoa_trung, ", "",
                              [k for k in _KG_CA if k.startswith("kg_m2_khoa_trung_")]),
    "kg_bo_hook_hang_ngoai_json": (", parse_constant=_cam_hang_ngoai_json", "",
                                   [k for k in _KG_CA if k.startswith("kg_m2_hang_ngoai_json_")]),
    "kg_bo_sha_re": ("    if not SHA_RE.fullmatch(a.head):\n", "    if False:\n",
                     ["kg_m1_head_7_ky_tu"]),
    "kg_bo_kiem_ten_rong": ("    if any(not t.strip() or t.splitlines() != [t] for t in ten_bb):\n", "    if False:\n",
                            ["kg_m1_bat_buoc_rong"] + [k for k in _KG_CA if k.startswith("kg_f04_xuong_dong_")]),
    "kg_f04_bo_kiem_xuong_dong": (" or t.splitlines() != [t] for t in ten_bb", " for t in ten_bb",
                                  [k for k in _KG_CA if k.startswith("kg_f04_xuong_dong_")]),
    "kg_bo_qua_phan_tu_thieu_truong": ("            if sai:\n                hong(",
                                       "            if sai:\n                continue\n                hong(",
                                       ["kg_m2_thieu_conclusion"]),
    "kg_bool_la_int": ("type(r.get(k, _VANG)) not in kieu]", "not isinstance(r.get(k, _VANG), kieu)]",
                       ["kg_m2_id_bool"]),
    "kg_bo_kiem_thieu_trang": ("    if so_id != tong_khai:\n", "    if False:\n",
                               ["kg_m2_thieu_trang", "kg_n5_khai_3_co_2", "kg_n5_khai_1_co_2", "kg_n5_khong_voi_mot_run"]),
    "kg_bo_kiem_vang": ('do.append(f"{ten!r}: VẮNG', 'xanh.append(f"{ten!r}: VẮNG',
                        ["kg_m3_vang", "kg_m3_ten_tuyet_doi"]),
    "kg_chon_success_bat_ky": ('id_max = max(r["id"] for r in cung)',
                               'id_max = max((r["id"] for r in cung if r["conclusion"] == "success"), default=-1)',
                               ["kg_m3_huy_moi_nhat"]),
    "kg_chon_luot_cu_nhat": ('id_max = max(r["id"]', 'id_max = min(r["id"]',
                             ["kg_m3_chay_lai_xanh", "kg_m2_list_nhieu_trang", "kg_n3_chay_lai",
                              "kg_n3_chay_lai_suite_khac_cu_hon"]),
    "kg_trung_id_chon_mot": ('for r in (r for r in cung if r["id"] == id_max):',
                             'for r in [next(r for r in cung if r["id"] == id_max)]:',
                             ["kg_m3_trung_id_moi_ban_phai_xanh"]),
    "kg_danh_sach_cam": ('hop_le = (r["status"] == "completed" and r["conclusion"] == "success"',
                         'hop_le = (r["status"] == "completed" and r["conclusion"] not in ("cancelled", "failure")', _KG_CAM),
    "kg_bo_so_head": ('"success"\n                      and r["head_sha"] == a.head)', '"success")',
                      ["kg_m3_head_khac"]),
    "kg_khop_tien_to": ('if r["name"] == ten]', 'if r["name"].startswith(ten)]',
                        ["kg_m3_ten_tuyet_doi"]),
    "kg_xet_moi_check": ('cung = [r for r in runs if r["name"] == ten]', "cung = list(runs)",
                         ["kg_m3_ngoai_bo_qua"]),
    "kg_rc_gate_thanh_0": ("\nRC_GATE = 12\n", "\nRC_GATE = 0\n", ["kg_m4_rc_gate_12"]),
    # --- #788: mỗi ô "Phép đo làm ĐỎ" một đột biến; ca đích chết vì đổi MÀU, không vì traceback.
    "kg_n1_bo_kiem_dang": ('    if not re.fullmatch(r"[1-9][0-9]*", a.check_suite):\n', "    if False:\n",
                           [f"kg_n1_check_suite_{t}" for t in ("am", "0", "012", "cong", "cach", "unicode")]),   # abc: không neo được (#856)
    "kg_n1_cho_so_0_dau": ('r"[1-9][0-9]*"', 'r"[0-9]+"', ["kg_n1_check_suite_0", "kg_n1_check_suite_012"]),
    "kg_n1_chu_so_unicode": ('r"[1-9][0-9]*"', 'r"[1-9]\\d*"', ["kg_n1_check_suite_unicode"]),
    # "chỉ kiểm run bắt buộc": gỡ chốt ở đầu đọc, dời nó vào lệnh cho đúng tên bắt buộc. Chốt
    # danh tính F01 cũng đọc `check_suite` mọi run nên phải nới theo — thiếu vế ấy là traceback.
    "kg_n2_chi_kiem_bat_buoc": (
        ('            if not isinstance(cs, dict) or type(cs.get("id", _VANG)) is not int:\n',
         'dt = (r["name"], r["check_suite"]["id"], r["head_sha"])',
         "    runs = _doc_check_runs(a.check_runs)\n"),
        ("            if False:\n", 'dt = (r["name"], (r.get("check_suite") or {}).get("id"), r["head_sha"])',
         "    runs = _doc_check_runs(a.check_runs)\n    if any(not isinstance(r.get('check_suite'), dict) or "
         "type(r['check_suite'].get('id')) is not int for r in runs if r['name'] in ten_bb):\n"
         "        _die(RC_GATE, 'KHÔNG ĐO ĐƯỢC: `check_suite` không phải object')\n"),
        ["kg_n2_run_khong_bat_buoc_thieu_suite"]),
    "kg_n2_bool_la_int": ('type(cs.get("id", _VANG)) is not int', 'not isinstance(cs.get("id", _VANG), int)',
                          ["kg_n2_suite_id_bool"]),
    "kg_n3_bo_loc_suite": ('        cung = [r for r in cung if r["check_suite"]["id"] == suite]', "        pass",
                           ["kg_n3_producer", "kg_n3_vang", "kg_n7_that_suite_thu_hoi"]),
    "kg_n3_suite_cua_run_dau": ('r["check_suite"]["id"] == suite]',
                                'r["check_suite"]["id"] == min(cung, key=lambda x: x["id"])["check_suite"]["id"]]',
                                ["kg_n3_chay_lai_suite_khac_cu_hon"]),
    "kg_n4_bo_canh_bao": ("        if khac:\n", "        if False:\n", ["kg_n4_canh_bao"]),
    "kg_n4_canh_bao_moi_ten": ("    for ten_cb in ten_bb:\n", "    for ten_cb in dict.fromkeys(r['name'] for r in runs):\n",
                               ["kg_n4_canh_bao"]),
    "kg_n5_quay_ve_nho_hon": ("    if so_id != tong_khai:\n", "    if so_id < tong_khai:\n",
                              ["kg_n5_khai_1_co_2", "kg_n5_khong_voi_mot_run"]),
    "kg_n5_bo_doi_co_mat": ('tc = tr.get("total_count", _VANG)', 'tc = tr.get("total_count", len(tr["check_runs"]))',
                            ["kg_n5_thieu"]),
    "kg_n5_trang_sau_thua_huong": ('tc = tr.get("total_count", _VANG)', 'tc = tr.get("total_count", khai[0] if khai else _VANG)',
                                   ["kg_n5_thieu_o_trang_sau"]),
    "kg_n5_bo_so_giua_trang": ("    if any(t != tong_khai for t in khai):\n", "    if False:\n", ["kg_n5_lech_trang"]),
    "kg_n5_bool_la_int": ("type(tc) is not int or", "not isinstance(tc, int) or", ["kg_n5_bool"]),
    "kg_n6_xoa_help": ('help="id suite của CHÍNH lượt workflow', 'help=argparse.SUPPRESS or "', ["kg_n6_help"]),
    # F01: mỗi trường danh tính một đột biến — gỡ cả kiểm, hoặc gỡ riêng từng trường.
    "kg_f01_bo_kiem_danh_tinh": ("        if danh_tinh.setdefault(r[\"id\"], dt) != dt:\n", "        if False:\n",
                                 [k for k in _KG_CA if k.startswith("kg_f01_cung_id_khac") or k.endswith("hai_ten_bat_buoc")]),
    "kg_f01_bo_suite_khoi_danh_tinh": ('dt = (r["name"], r["check_suite"]["id"], r["head_sha"])', 'dt = (r["name"], r["head_sha"])',
                                       ["kg_f01_cung_id_khac_suite", "kg_f01_cung_id_khac_suite_hai_trang"]),
    "kg_f01_bo_ten_khoi_danh_tinh": ('dt = (r["name"], r["check_suite"]["id"], r["head_sha"])', 'dt = (r["check_suite"]["id"], r["head_sha"])',
                                     ["kg_f01_cung_id_khac_ten", "kg_f01_cung_id_hai_ten_bat_buoc"]),
    # F02: ca nền khoá traceback; đột biến gỡ đường bắt trần chết bằng traceback nên bị loại (F03).
    "kg_f02_du_phong_khop_nham": ("        suite = a.check_suite   #", "        suite = 1   #", ["kg_f02_suite_vuot_tran_int"]),
    "kg_n4_dem_ban_ghi": (('sorted({r["id"] for r in runs if', ' != suite})'), ('sorted([r["id"] for r in runs if', ' != suite])'),
                          ["kg_n4_canh_bao"]),
    "kg_n4_ten_theo_repr": ("CẢNH BÁO: '{ten_cb}'", "CẢNH BÁO: {ten_cb!r}", ["kg_n4_canh_bao"]),
    "kg_n6_dong_xanh_khong_suite": ('(suite {suite}): ', ": ", ["kg_m2_object_mot_trang", "kg_n7_that_suite_ci"]),
})

# --- #822 `KG-RANG-TEST` (spec `ops/specs/wp822.md` r1, M1–M6) -----------------------------------------
# Quét theo LỚP: mỗi điều kiện của `_doc_check_runs` + `cmd_kiem_gate` một đột biến KHÔNG SẬP, mỗi đột biến
# một ca đích đòi rc + lý do của ĐÚNG cửa chặn. Chốt chỉ "gỡ ra là sập" thì đột biến là dạng NUỐT/BỎ QUA
# (đường thoái lui im lặng) — dạng gỡ thẳng chỉ cho tín dụng giả (M6). Fixture run không bắt buộc: dưới
# đột biến CLI không chạm khoá hỏng nên ra XANH GIẢ, không traceback (M3).
_kg_khac = lambda **doi: {k: v for k, v in {**_kg_run(2, name="khac"), **doi}.items() if v is not _VANG_T}
_KG_RUN1_SAU = lambda *khac, tc=None: {"check_runs": [_kg_run(1), *khac], **({} if tc is None else {"total_count": tc})}
_KG_TRUONG = "thiếu/sai kiểu trường"
_KG_CA.update({
    # K01: mỗi lớp ngoại lệ một ca, lý do nêu ĐÚNG lớp ấy.
    "kg_k01_utf8_hong": _kg_ca(None, tho=json.dumps(_KG_1).encode()[:-1] + b',"x":"\xff"}', chua="như JSON (UnicodeDecodeError"),
    "kg_k01_de_quy": _kg_ca(None, tho="[" * 100000, chua="như JSON (RecursionError"),
    "kg_k04_list_rong": _kg_ca(None, tho="[]", chua="list trang RỖNG"),
    "kg_k05_trang_khong_phai_object": _kg_ca([[1], {"total_count": 1, "check_runs": [_kg_run(1)]}], chua="trang 0 " + _KG_TRANG),
    "kg_k08_phan_tu_khong_phai_object": _kg_ca(_KG_RUN1_SAU(5, tc=1), chua="check_runs[1] không phải object"),
    "kg_k09_id_chuoi_khong_bat_buoc": _kg_ca(_KG_RUN1_SAU(_kg_khac(id="x")), chua=f"{_KG_TRUONG} ['id']"),
    "kg_d3_name_sai_kieu": _kg_ca(_KG_RUN1_SAU(_kg_khac(name=5)), chua=f"{_KG_TRUONG} ['name']"),
    "kg_d4_head_sha_sai_kieu": _kg_ca(_KG_RUN1_SAU(_kg_khac(head_sha=5)), chua=f"{_KG_TRUONG} ['head_sha']"),
    "kg_d5_status_sai_kieu": _kg_ca(_KG_RUN1_SAU(_kg_khac(status=5)), chua=f"{_KG_TRUONG} ['status']"),
    "kg_d5_thieu_status_khong_bat_buoc": _kg_ca(_KG_RUN1_SAU(_kg_khac(status=_VANG_T)), chua=f"{_KG_TRUONG} ['status']"),
    "kg_d6_conclusion_sai_kieu": _kg_ca(_KG_RUN1_SAU(_kg_khac(conclusion=5)), chua=f"{_KG_TRUONG} ['conclusion']"),
    "kg_m2_thieu_conclusion_khong_bat_buoc": _kg_ca(_KG_RUN1_SAU(_kg_khac(conclusion=_VANG_T)),
                                                    chua=f"{_KG_TRUONG} ['conclusion']"),
    "kg_k37_conclusion_null_khong_bat_buoc": _kg_ca(_KG_RUN1_SAU(_kg_khac(conclusion=None, status="queued")), expect=0),
    "kg_k15_bo_qua_run_thieu_suite": _kg_ca(_KG_RUN1_SAU(_kg_khac(check_suite=_VANG_T), tc=2), dem=False, chua=_KG_CS),
    "kg_d1_cung_id_khac_head": _kg_ca(_KG_RUN1_SAU(_kg_run(1, head="cd" * 20), _kg_run(2), tc=2), dem=False, chua=_KG_DT),
    "kg_d2_mot_ten_do_mot_ten_xanh": _kg_ca(_KG_RUN1_SAU(_kg_run(2, name="gate2", conclusion="cancelled")),
                                            bat_buoc=("gate", "gate2"), chua="1/2 tên bắt buộc đỏ"),
    "kg_k21_head_hoa": _kg_ca({"check_runs": [_kg_run(1, head="AB" * 20)]}, head="AB" * 20, expect=2, chua="SHA 40"),
    "kg_k24_ten_chi_khoang_trang": _kg_ca({"check_runs": [_kg_run(1, name=" ")]}, bat_buoc=(" ",), expect=2,
                                          chua="không được rỗng"),
    "kg_k24_ten_chi_tab": _kg_ca({"check_runs": [_kg_run(1, name="\t")]},
                                 bat_buoc=("\t",), expect=2, chua="không được rỗng"),
    "kg_k24_ten_chi_nbsp": _kg_ca({"check_runs": [_kg_run(1, name="\u00a0")]},
                                  bat_buoc=("\u00a0",), expect=2, chua="không được rỗng"),
    "kg_k31_status_do_truoc": _kg_ca({"check_runs": [_kg_run(2, status="in_progress"), _kg_run(2)]},
                                     chua="status='in_progress'"),
    "kg_k31_conclusion_do_truoc": _kg_ca({"check_runs": [_kg_run(2, conclusion="cancelled"), _kg_run(2)]},
                                         chua="conclusion='cancelled'"),
    "kg_k40_hai_ban_do_mot_ten": _kg_ca({"check_runs": [_kg_run(2, conclusion="cancelled"), _kg_run(2, conclusion="failure")]},
                                        chua="1/1 tên bắt buộc đỏ"),
})
for _ten, _head in (("phi_hex", "g" * 40), ("39", "a" * 39), ("41", "a" * 41)):
    _KG_CA[f"kg_r2_sha_{_ten}"] = _kg_ca({"check_runs": [_kg_run(1, head=_head)]}, head=_head, expect=2, chua="SHA 40")
for _ten, _cu, _moi, _rc in (("moi_do", "success", "cancelled", 12), ("moi_xanh", "cancelled", "success", 0)):
    _KG_CA[f"kg_r2_id_so_{_ten}"] = _kg_ca({"check_runs": [_kg_run(9, conclusion=_cu), _kg_run(10, conclusion=_moi)]},
                                           expect=_rc, chua="conclusion='cancelled'")
for _truong, _gt in (("id", "x"), ("name", 5), ("head_sha", 5), ("status", 5), ("conclusion", 5),
                     ("status", _VANG_T), ("conclusion", _VANG_T)):
    _KG_CA[f"kg_r2_trang_sau_{_truong}_{'vang' if _gt is _VANG_T else 'kieu'}"] = _kg_ca(
        [{"total_count": 2, "check_runs": [_kg_run(1)]}, {"total_count": 2, "check_runs": [_kg_khac(**{_truong: _gt})]}],
        chua=f"trang 1 check_runs[0] {_KG_TRUONG} ['{_truong}']")
for _ten, _trang, _tc, _ly in (
        ("suite_chuoi", [_kg_khac(check_suite={"id": "5"})], 2, _KG_CS), ("tc_thuc", [_kg_run(2)], 2.0, "≥ 0"),
        ("tc_bool", [], True, "≥ 0"), ("page_shape", {}, 1, "trang 1 " + _KG_TRANG),
        ("run_shape", [5], 1, "trang 1 check_runs[0] không phải object")):
    _KG_CA[f"kg_r2_trang_sau_{_ten}"] = _kg_ca(
        [{"total_count": int(_tc), "check_runs": [_kg_run(1)]}, {"total_count": _tc, "check_runs": _trang}], chua=_ly)
_KG_CA["kg_r2_ba_trang_lech_cuoi"] = _kg_ca(
    [{"total_count": 3, "check_runs": [_kg_run(1, conclusion="cancelled")]},
     {"total_count": 3, "check_runs": [_kg_run(2, conclusion="cancelled")]}, {"total_count": 4, "check_runs": [_kg_run(3)]}],
    chua="khác nhau")
# Review 3: mỗi biến thể một fixture chỉ sai đúng chốt; dữ liệu + mutant dùng chung bảng.
_KG_R3 = (
    ('K07', 'later_page_negative_count', 'negative', 'if type(tc) is not int or tc < 0:', 'if type(tc) is not int or (tc < 0 and i == 0):', [{'total_count': 1, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'total_count': -1, 'check_runs': []}], {'dem': False, 'chua': 'trang 1: `total_count` không phải số nguyên ≥ 0'}),
    ('K15', 'later_page_suite_bool', 'bool', 'type(cs.get("id", _VANG)) is not int:', '(not isinstance(cs.get("id", _VANG), int) if i else type(cs.get("id", _VANG)) is not int):', [{'total_count': 2, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'total_count': 2, 'check_runs': [{'id': 2, 'name': 'khac', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': True}}]}], {'dem': False, 'chua': 'trang 1 check_runs[0] `check_suite` không phải object'}),
    ('K14', 'later_page_run_bool', 'bool', 'if type(r.get(k, _VANG)) not in kieu]', 'if (not isinstance(r.get(k, _VANG), kieu) if i else type(r.get(k, _VANG)) not in kieu)]', [{'total_count': 2, 'check_runs': [{'id': 2, 'name': 'gate', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'total_count': 2, 'check_runs': [{'id': True, 'name': 'khac', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}], {'dem': False, 'chua': "trang 1 check_runs[0] thiếu/sai kiểu trường ['id']"}),
    ('K02', 'nested_suite_duplicates_ignored', 'suite_id', 'object_pairs_hook=_cam_khoa_trung, ', 'object_pairs_hook=lambda pairs: dict(pairs) if all(k == "id" for k, _ in pairs) else _cam_khoa_trung(pairs), ', None, {'dem': False, 'tho': '{"total_count": 1, "check_runs": [{"id": 1, "name": "gate", "head_sha": "abababababababababababababababababababab", "status": "completed", "conclusion": "success", "check_suite": {"id": 9, "id": 1}}]}', 'chua': 'khoá trùng'}),
    ('K02', 'extra_key_duplicates_ignored', 'root', 'object_pairs_hook=_cam_khoa_trung, ', 'object_pairs_hook=lambda pairs: _cam_khoa_trung([(k,v) for k,v in pairs if k in {"check_runs", "total_count", "id", "name", "head_sha", "status", "conclusion", "check_suite"}]) | dict(pairs), ', None, {'dem': False, 'tho': '{"total_count": 1, "check_runs": [{"id": 1, "name": "gate", "head_sha": "abababababababababababababababababababab", "status": "completed", "conclusion": "success", "check_suite": {"id": 1}}],"extra":1,"extra":2}', 'chua': 'khoá trùng'}),
    ('K02', 'extra_key_duplicates_ignored', 'nested', 'object_pairs_hook=_cam_khoa_trung, ', 'object_pairs_hook=lambda pairs: _cam_khoa_trung([(k,v) for k,v in pairs if k in {"check_runs", "total_count", "id", "name", "head_sha", "status", "conclusion", "check_suite"}]) | dict(pairs), ', None, {'dem': False, 'tho': '{"total_count": 1, "check_runs": [{"id": 1, "name": "gate", "head_sha": "abababababababababababababababababababab", "status": "completed", "conclusion": "success", "check_suite": {"id": 1}}],"extra":{"x":1,"x":2}}', 'chua': 'khoá trùng'}),
    ('K02', 'extra_key_duplicates_ignored', 'array', 'object_pairs_hook=_cam_khoa_trung, ', 'object_pairs_hook=lambda pairs: _cam_khoa_trung([(k,v) for k,v in pairs if k in {"check_runs", "total_count", "id", "name", "head_sha", "status", "conclusion", "check_suite"}]) | dict(pairs), ', None, {'dem': False, 'tho': '{"total_count": 1, "check_runs": [{"id": 1, "name": "gate", "head_sha": "abababababababababababababababababababab", "status": "completed", "conclusion": "success", "check_suite": {"id": 1}}],"extra":[{"x":1,"x":2}]}', 'chua': 'khoá trùng'}),
    ('K34', 'head_prefix', 'prefix', 'and r["head_sha"] == a.head)', 'and r["head_sha"].startswith(a.head))', {'total_count': 1, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'abababababababababababababababababababab1', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'head_sha='}),
    ('K34', 'head_suffix', 'head_suffix', 'and r["head_sha"] == a.head)', 'and r["head_sha"].endswith(a.head))', {'total_count': 1, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': '1abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'head_sha='}),
    ('K34', 'head_casefold', 'head_casefold', 'and r["head_sha"] == a.head)', 'and r["head_sha"].lower() == a.head.lower())', {'total_count': 1, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'ABABABABABABABABABABABABABABABABABABABAB', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'head_sha='}),
    ('K34', 'head_first7', 'head_first7', 'and r["head_sha"] == a.head)', 'and r["head_sha"][:7] == a.head[:7])', {'total_count': 1, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'abababaccccccccccccccccccccccccccccccccc', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'head_sha='}),
    ('K27', 'name_suffix', 'name_suffix', 'if r["name"] == ten]', 'if r["name"].endswith(ten)]', {'total_count': 1, 'check_runs': [{'id': 1, 'name': 'extra gate', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'VẮNG'}),
    ('K27', 'name_casefold', 'name_casefold', 'if r["name"] == ten]', 'if r["name"].lower() == ten.lower()]', {'total_count': 1, 'check_runs': [{'id': 1, 'name': 'GATE', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'VẮNG'}),
    ('K27', 'name_strip_run', 'name_strip_run', 'if r["name"] == ten]', 'if r["name"].strip() == ten]', {'total_count': 1, 'check_runs': [{'id': 1, 'name': ' gate ', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'chua': 'VẮNG'}),
    ('K27', 'name_strip_arg', 'spaces', 'if r["name"] == ten]', 'if r["name"] == ten.strip()]', {'total_count': 1, 'check_runs': [{'id': 1, 'name': ' gate ', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'success', 'check_suite': {'id': 1}}]}, {'dem': False, 'expect': 0, 'bat_buoc': (' gate ',)}),
    ('K39', 'red_first_name_only', 'two_red', '        for dong in do:\n', '        for dong in do[:1]:\n', {'total_count': 2, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'failure', 'check_suite': {'id': 1}}, {'id': 2, 'name': 'gate2', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'cancelled', 'check_suite': {'id': 1}}]}, {'dem': False, 'bat_buoc': ('gate', 'gate2'), 'chua': "'gate2' id=2: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 2/2 tên bắt buộc đỏ"}),
    ('K40', 'red_count_constant', 'two_red', '{len(do)}/{len(ten_bb)} tên bắt buộc đỏ', '{1}/{len(ten_bb)} tên bắt buộc đỏ', {'total_count': 2, 'check_runs': [{'id': 1, 'name': 'gate', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'failure', 'check_suite': {'id': 1}}, {'id': 2, 'name': 'gate2', 'head_sha': 'abababababababababababababababababababab', 'status': 'completed', 'conclusion': 'cancelled', 'check_suite': {'id': 1}}]}, {'dem': False, 'bat_buoc': ('gate', 'gate2'), 'chua': "'gate2' id=2: status='completed' conclusion='cancelled' head_sha='abababababababababababababababababababab'\ngate KHÔNG xanh trên abababababababababababababababababababab: 2/2 tên bắt buộc đỏ"}),
)
for _k, _m, _nhan, _tim, _thay, _du_lieu, _opts in _KG_R3:
    _ca = f"kg_r3_{_m}_{_nhan}"
    MUTANTS.setdefault("kg_r3_" + _m, (_tim, _thay, []))[2].append(_ca)
    _KG_CA[_ca] = _kg_ca(_du_lieu, **_opts)
# Review 4 (`so-khop-tuyet-doi-chua-du`, đóng theo LỚP): MỌI phép `==` trên chuỗi của hai hàm, mỗi chỗ chạy CẢ HỌ biến thể
# gần đúng (hoa/thường · tiền tố · hậu tố · đệm trắng · fullwidth · NFD) — đột biến nới phép so kiểu nào cũng gặp ít nhất một.
_kg_gan = lambda v: {k: x for k, x in {
    "hoa": v.upper(), "tien_to": "x" + v, "hau_to": v + "x", "doi_dau": "c" + v[1:], "doi_cuoi": v[:-1] + "c", "dem": f" {v} ",
    "nfd": unicodedata.normalize("NFD", v),
    "rong": "".join(chr(ord(k) + 0xFEE0) if "!" <= k <= "~" else k for k in v)}.items() if x != v}
_KG_T = "gat\u00e9"
_KG_GAN = {   # chỗ so → (giá trị đúng, p ↦ đối số `_kg_ca` sai ĐÚNG giá trị ấy)
    "status": ("completed", lambda p: dict(du_lieu={"check_runs": [_kg_run(1, status=p)]}, chua=f"status={p!r}")),
    "conclusion": ("success", lambda p: dict(du_lieu={"check_runs": [_kg_run(1, conclusion=p)]}, chua=f"conclusion={p!r}")),
    "head": (_KG_HEAD, lambda p: dict(du_lieu={"check_runs": [_kg_run(1, head=p)]}, chua=f"head_sha={p!r}")),
    "ten": (_KG_T, lambda p: dict(du_lieu={"check_runs": [_kg_run(1, name=p)]}, bat_buoc=(_KG_T,), chua="VẮNG")),
    "dt_ten": (_KG_T, lambda p: dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, name=_KG_T), _kg_run(1, name=p),
               _kg_run(2, name=_KG_T)]}, bat_buoc=(_KG_T,), dem=False, chua=_KG_DT)),
    "dt_head": (_KG_HEAD, lambda p: dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1), _kg_run(1, head=p), _kg_run(2)]},
                dem=False, chua=_KG_DT)),
}


def _kg_ho_gan(cho):
    def ca(c: Ctx):
        for nhan, p in _kg_gan(_KG_GAN[cho][0]).items():
            try:
                _kg_ca(**_KG_GAN[cho][1](p))(c)
            except AssertionError as ex:
                raise AssertionError(f"{cho}/{nhan} ({p!r}): {ex}") from None
    return ca


def case_kg_r4_gan_canh_bao(c: Ctx):
    for nhan, p in _kg_gan(_KG_T).items():   # tên GẦN ĐÚNG ở suite khác không phải tên bắt buộc ⇒ KHÔNG cảnh báo
        rc, _, e = _kg(c, {"check_runs": [_kg_run(1, name=_KG_T), _kg_run(2, name=p, suite=_KG_SUITE_KHAC)]}, _KG_T)
        if rc != 0 or "CẢNH BÁO" in _txt(e):
            raise AssertionError(f"canh_bao/{nhan} ({p!r}): rc={rc} {_txt(e)!r}")


def case_kg_r4_ba_ten(c: Ctx):
    """Ba tên đỏ: đủ BA dòng ĐỎ + `3/3`; ba tên có run ở suite khác (gate: ba id): đủ BA dòng cảnh báo, đủ id giữa."""
    ten = ("gate", "gate2", "gate3")
    rc, _, e = _kg(c, {"check_runs": [_kg_run(i + 1, name=t, conclusion="cancelled") for i, t in enumerate(ten)]}, *ten)
    thieu = [t for t in ten if f"ĐỎ  '{t}' id=" not in _txt(e)] + ["3/3"] * ("3/3 tên bắt buộc đỏ" not in _txt(e))
    if rc != 12 or thieu:
        raise AssertionError(f"ba tên đỏ: rc={rc} thiếu {thieu}: {_txt(e)!r}")
    rc, _, e = _kg(c, {"check_runs": [_kg_run(i + 1, name=t) for i, t in enumerate(ten)] + [_kg_run(i, name=t, suite=9)
                   for i, t in ((10, "gate"), (9, "gate"), (16, "gate"), (7, "gate2"), (8, "gate3"))]}, *ten)   # id: số ≠ chữ ≠ thứ tự set
    dong = [d for d in _txt(e).splitlines() if d.startswith("CẢNH BÁO:")]
    if rc != 0 or dong != ["CẢNH BÁO: 'gate' có 3 run ở suite khác (9, 10, 16) — bỏ qua", "CẢNH BÁO: 'gate2' có 1 run ở suite khác (7) — bỏ qua",
                           "CẢNH BÁO: 'gate3' có 1 run ở suite khác (8) — bỏ qua"]:
        raise AssertionError(f"ba tên cảnh báo: rc={rc} {dong!r}")


def case_kg_r4_tha_ten(c: Ctx):
    """Chiều THA: tên KHÔNG chuẩn (đệm trắng/hoa/NFD/fullwidth) mà run và `--bat-buoc` trùng NGUYÊN VĂN ⇒ khớp + cảnh báo
    đúng. Chuẩn hoá MỘT phía (chỉ run, hoặc chỉ đối số) làm vỡ phép bằng ở đây."""
    for nhan, t in _kg_gan(_KG_T).items():
        if nhan in ("tien_to", "hau_to", "doi_dau", "doi_cuoi"):
            continue
        rc, o, e = _kg(c, {"check_runs": [_kg_run(1, name=t), _kg_run(2, name=t, suite=_KG_SUITE_KHAC)]}, t)
        if rc != 0 or _txt(o).count(f"{t} id=1") != 1 or f"CẢNH BÁO: '{t}' có 1 run ở suite khác (2)" not in _txt(e):
            raise AssertionError(f"tha/{nhan} ({t!r}): rc={rc} {_txt(o)!r} {_txt(e)!r}")


CASES += [(f"kg_r4_gan_{k}", _kg_ho_gan(k)) for k in _KG_GAN] + [("kg_r4_tha_ten", case_kg_r4_tha_ten),
                                                                  ("kg_r4_gan_canh_bao", case_kg_r4_gan_canh_bao),
                                                                  ("kg_r4_ba_ten", case_kg_r4_ba_ten)]
# Review 5 (đóng theo LỚP): mỗi lớp một BỘ SINH fixture — tích các chiều (kiểu JSON × trường × vị trí × trang; vị trí
# trong danh sách; cặp id × thứ tự × chiều màu; dạng đối số) — và đột biến sinh bằng vòng ở dưới.
_KG_KIEU = (("null", None), ("bool", True), ("int", 7), ("float", 1.5), ("str", "x"), ("list", [1]), ("dict", {"a": 1}))
_KG_CHO_PHEP = {"id": ("int",), "name": ("str",), "head_sha": ("str",), "status": ("str",), "conclusion": ("str", "null"),
                "suite": ("int",)}


def _kg_dat_vi_tri(hong, tot, vi_tri):   # chèn `hong` vào đầu / giữa / cuối danh sách `tot`
    return {"dau": [hong, *tot], "giua": [*tot[:1], hong, *tot[1:]], "cuoi": [*tot, hong]}[vi_tri]


def _kg_sinh(ten, sinh):
    def ca(c: Ctx):
        for nhan, kw in sinh():
            try:
                _kg_ca(**kw)(c)
            except AssertionError as ex:
                raise AssertionError(f"{ten}/{nhan}: {ex}") from None
    return ca


def _kg_sinh_kieu(truong):   # mọi kiểu JSON sai × đầu/giữa/cuối × một trang / trang sau, trên run KHÔNG bắt buộc
    for k, v in _KG_KIEU:
        if k in _KG_CHO_PHEP[truong]:
            continue
        hong = _kg_khac(check_suite={"id": v}) if truong == "suite" else _kg_khac(**{truong: v})
        for vt in ("dau", "giua", "cuoi"):
            ds = _kg_dat_vi_tri(hong, [_kg_run(1), _kg_run(3, name="khac")], vt)
            ly = _KG_CS if truong == "suite" else f"{_KG_TRUONG} ['{truong}']"
            yield f"{k}_{vt}", dict(du_lieu={"total_count": 3, "check_runs": ds}, dem=False, chua=ly)
        yield f"{k}_trang_sau", dict(du_lieu=[{"total_count": 3, "check_runs": [_kg_run(1), _kg_run(3, name="khac")]},
                                              {"total_count": 3, "check_runs": [hong]}], dem=False, chua=ly)


def _kg_sinh_trang():   # trang hỏng (không object · thiếu `check_runs` · `check_runs` sai kiểu) ở đầu/giữa/cuối
    hong = [(f"trang_{k}", v) for k, v in _KG_KIEU if k != "dict"] + [("thieu_check_runs", {"total_count": 2})] + [
        (f"check_runs_{k}", {"total_count": 2, "check_runs": v}) for k, v in (*_KG_KIEU[:5], ("rong", ""), ("dict", {}))]
    for nhan, tr in hong:
        for vt in ("dau", "giua", "cuoi"):
            ds = _kg_dat_vi_tri(tr, [{"total_count": 2, "check_runs": [_kg_run(1)]},
                                     {"total_count": 2, "check_runs": [_kg_run(3, name="khac")]}], vt)
            yield f"{nhan}_{vt}", dict(du_lieu=ds, dem=False, chua=_KG_TRANG)


def _kg_sinh_vi_tri():   # K24 mọi tên · K16–K18 mọi bản ghi · K29 mọi tập con tên vắng (kể cả 0 run, chỉ suite khác)
    for xau in ("", " ", "a\nb"):
        for vt in range(5):   # NĂM tên: lát cắt `[:2] + [-2:]` không phủ được vị trí giữa
            ten = ["gate", "gate2", "gate3", "gate4"]
            bb = (*ten[:vt], xau, *ten[vt:])   # #856 M3: run cho MỌI tên, kể cả tên hỏng — VẮNG không chặn hộ
            yield f"ten_{vt}_{xau!r}", dict(du_lieu={"check_runs": [_kg_run(i + 1, name=t) for i, t in enumerate(bb)]},
                                           bat_buoc=bb, expect=2, chua="--bat-buoc")
    tot = [_kg_run(9)] + [_kg_run(i, name="khac") for i in (1, 2, 3, 4)]
    for a, b in ((0, 5), (1, 2), (2, 3), (3, 4), (0, 1), (4, 5), (1, 4)):
        ds = [*tot]
        ds.insert(b - 1 if b > a else b, _kg_run(ds[a]["id"], name="khac", head="cd" * 20))
        yield f"danh_tinh_{a}_{b}", dict(du_lieu={"total_count": 5, "check_runs": ds}, dem=False, chua=_KG_DT)
    ten = ("gate", "gate2", "gate3")
    for vang in [(t,) for t in ten] + [(ten[0], ten[2]), ten[1:], ten]:
        co = [t for t in ten if t not in vang]
        for kieu, ds in (("rong", [_kg_run(i + 1, name=t) for i, t in enumerate(co)]),
                         ("suite_khac", [_kg_run(i + 1, name=t, suite=t in vang and _KG_SUITE_KHAC or _KG_SUITE)
                                         for i, t in enumerate(ten)])):
            yield f"vang_{'_'.join(vang)}_{kieu}", dict(du_lieu={"check_runs": ds}, bat_buoc=ten,
                                                         chua=f"{len(vang)}/3 tên bắt buộc đỏ")


def _kg_sinh_id():   # cặp id × hai thứ tự × hai chiều màu; đáp án neo vào id LỚN hơn theo SỐ
    for lo, hi in ((9, 10), (-5, 2), (2 ** 53, 2 ** 53 + 1), (1, 2)):
        for dao in (False, True):
            for hi_xanh in (True, False):
                ds = [_kg_run(lo, conclusion="cancelled" if hi_xanh else "success"),
                      _kg_run(hi, conclusion="success" if hi_xanh else "cancelled")]
                yield f"{lo}_{hi}_{dao}_{hi_xanh}", dict(du_lieu={"check_runs": ds[::-1] if dao else ds},
                                                          expect=0 if hi_xanh else 12, chua="conclusion='cancelled'",
                                                          dong_xanh=f"gate XANH trên {_KG_HEAD} (suite 1): gate id={hi}")
    yield "thu_tu_bat_buoc", dict(du_lieu={"check_runs": [_kg_run(1), _kg_run(2, name="gate2")]}, bat_buoc=("gate2", "gate"),
                                  expect=0, dong_xanh=f"gate XANH trên {_KG_HEAD} (suite 1): gate2 id=2 · gate id=1")


_KG_HEAD_SO = "0123456789abcdef" * 2 + "01234567"


def _kg_sinh_doi_so():   # dạng SAI ở chính `--head` / `--check-suite`; mọi thứ khác (run trùng nguyên văn) hợp lệ
    rong = lambda x, i: x[:i] + chr(ord(x[i]) + 0xFEE0) + x[i + 1:]
    for nhan, h in (("dem_trai", " " + _KG_HEAD_SO), ("dem_phai", _KG_HEAD_SO + " "), ("rong_so", rong(_KG_HEAD_SO, 0)),
                    ("rong_chu", rong(_KG_HEAD_SO, 10)), ("tab", _KG_HEAD_SO + "\t")):
        yield f"head_{nhan}", dict(du_lieu={"check_runs": [_kg_run(1, head=h)]}, head=h, expect=2, chua="SHA 40")
    for nhan, cs in (("dem_trai", " 1"), ("dem_phai", "1 "), ("rong", "１"), ("tab", "1\t"), ("arap", "١")):
        yield f"suite_{nhan}", dict(du_lieu=_KG_1, suite=cs, expect=2, chua=_KG_ARG)


def _kg_sinh_trung_id():   # ≥3 bản cùng id lớn nhất, MỘT bản đỏ (riêng status / riêng conclusion) ở mọi vị trí
    for truong, gt in (("status", "in_progress"), ("conclusion", "cancelled")):
        for vt in range(3):
            ds = [_kg_run(2, **({truong: gt} if i == vt else {})) for i in range(3)]
            yield f"{truong}_{vt}", dict(du_lieu={"check_runs": ds}, chua=f"{truong}={gt!r}")   # cung[0] là một bản cùng id


_KG_R5_CA = {**{f"kg_r5_kieu_{t}": (lambda t=t: _kg_sinh_kieu(t)) for t in _KG_CHO_PHEP},
             "kg_r5_trang": _kg_sinh_trang, "kg_r5_vi_tri": _kg_sinh_vi_tri, "kg_r5_id": _kg_sinh_id,
             "kg_r5_doi_so": _kg_sinh_doi_so, "kg_r5_trung_id": _kg_sinh_trung_id}
CASES += [(k, _kg_sinh(k, v)) for k, v in _KG_R5_CA.items()]
_KG_CA_822 = [k for k in _KG_CA if k not in dict(CASES)]
CASES += [(k, _KG_CA[k]) for k in _KG_CA_822]

_KG_EXC = "    except (OSError, UnicodeDecodeError, ValueError, RecursionError) as ex:\n"
MUTANTS.update({
    **{f"kg_k01_nuot_{t}": (_KG_EXC, f"    except {t}:\n        d = []\n" + _KG_EXC, [ca]) for t, ca in (
        ("OSError", "kg_m2_tep_vang"), ("UnicodeDecodeError", "kg_k01_utf8_hong"),
        ("ValueError", "kg_m2_json_hong"), ("RecursionError", "kg_k01_de_quy"))},
    "kg_k04_list_rong_im_lang": ("    if not trang:\n        hong(", "    if not trang:\n        return []\n        hong(",
                                 ["kg_k04_list_rong"]),
    "kg_k05_bo_qua_trang_hong": ('            hong(f"trang {i} không phải object có', '            continue\n            hong(f"trang {i} không phải object có',
                                 ["kg_k05_trang_khong_phai_object"]),
    "kg_k05_bo_kiem_check_runs_list": (' or not isinstance(tr.get("check_runs"), list)', "", ["kg_m2_check_runs_khong_phai_list"]),
    "kg_k07_bo_kiem_kieu_tc": ("        if type(tc) is not int or tc < 0:\n", "        if tc < 0:\n", ["kg_n5_thuc"]),
    "kg_k07_bo_kiem_am": (" or tc < 0:", ":", ["kg_n5_am"]),
    "kg_k08_bo_qua_phan_tu": ('                hong(f"trang {i} check_runs[{j}] không phải object")',
                              '                continue\n                hong(f"trang {i} check_runs[{j}] không phải object")',
                              ["kg_k08_phan_tu_khong_phai_object"]),
    "kg_k09_bo_kieu_id": ('(("id", (int,)), ', "(", ["kg_k09_id_chuoi_khong_bat_buoc"]),
    # D1–D6: NGUYÊN VĂN bảng D của đặc tả.
    "kg_d1_bo_head_khoi_danh_tinh": ('dt = (r["name"], r["check_suite"]["id"], r["head_sha"])',
                                     'dt = (r["name"], r["check_suite"]["id"])', ["kg_d1_cung_id_khac_head"]),
    "kg_d2_mot_ten_xanh_che_do": ("    if do:\n        for dong in do:", "    if do and not xanh:\n        for dong in do:",
                                  ["kg_d2_mot_ten_do_mot_ten_xanh"]),
    "kg_d3_bo_kieu_name": ('("name", (str,)), ', "", ["kg_d3_name_sai_kieu"]),
    "kg_d4_bo_kieu_head_sha": ('("head_sha", (str,)),\n', "\n", ["kg_d4_head_sha_sai_kieu"]),
    "kg_d5_bo_kieu_status": ('("status", (str,)), ', "", ["kg_d5_status_sai_kieu", "kg_d5_thieu_status_khong_bat_buoc"]),
    "kg_d6_bo_kieu_conclusion": (', ("conclusion", (str, type(None)))', "",
                                 ["kg_d6_conclusion_sai_kieu", "kg_m2_thieu_conclusion_khong_bat_buoc"]),
    "kg_k15_bo_kieu_id_suite": ('            if not isinstance(cs, dict) or type(cs.get("id", _VANG)) is not int:\n',
                                "            if not isinstance(cs, dict):\n", ["kg_n2_suite_id_chuoi"]),
    "kg_k15_bo_qua_run_suite_hong": ("                hong(f\"trang {i} check_runs[{j}] `check_suite`",
                                     "                continue\n                hong(f\"trang {i} check_runs[{j}] `check_suite`",
                                     ["kg_k15_bo_qua_run_thieu_suite"]),
    "kg_k20_dem_ban_ghi": ('so_id = len({r["id"] for r in runs})', "so_id = len(runs)", ["kg_f01_cung_id_nhat_quan_hai_trang"]),
    "kg_k21_nhan_hex_hoa": ('SHA_RE = re.compile(r"^[0-9a-f]{40}\\Z")', 'SHA_RE = re.compile(r"^[0-9a-fA-F]{40}\\Z")',
                            ["kg_k21_head_hoa"]),
    "kg_k22_match_tien_to": ('re.fullmatch(r"[1-9][0-9]*", a.check_suite)', 're.match(r"[1-9][0-9]*", a.check_suite)',
                             ["kg_n1_check_suite_unicode"]),
    "kg_k24_bo_strip": ("if any(not t.strip() or", "if any(not t or", ["kg_k24_ten_chi_khoang_trang"]),
    "kg_k24_chi_strip_space": ('not t.strip() or t.splitlines()', 'not t.strip(" ") or t.splitlines()',
                                ["kg_k24_ten_chi_tab", "kg_k24_ten_chi_nbsp"]),
    "kg_k31_chon_ban_cuoi": ('for r in (r for r in cung if r["id"] == id_max):',
                              'for r in [r for r in cung if r["id"] == id_max][-1:]:',
                              ["kg_k31_status_do_truoc", "kg_k31_conclusion_do_truoc"]),
    "kg_k25_bo_khu_trung": ("ten_bb = list(dict.fromkeys(a.bat_buoc))", "ten_bb = list(a.bat_buoc)", ["kg_m1_trung_ten_mot_dong"]),
    "kg_k26_canh_bao_ca_suite_neo": (' and r["check_suite"]["id"] != suite})', "})", ["kg_n4_canh_bao"]),
    "kg_k26_canh_bao_ra_stdout": ('— bỏ qua", file=sys.stderr)', '— bỏ qua")', ["kg_n4_canh_bao"]),
    "kg_k36_chi_ten_dau": ('" · ".join(xanh))', '" · ".join(xanh[:1]))', ["kg_n7_that_suite_ci"]),
    "kg_k37_vang_la_null": ("type(r.get(k, _VANG)) not in kieu]", "type(r.get(k)) not in kieu]",
                            ["kg_m2_thieu_conclusion_khong_bat_buoc"]),
    "kg_k38_list_la_mot_trang": ("trang = d if isinstance(d, list) else [d]", "trang = [d]", ["kg_m2_list_nhieu_trang"]),
    "kg_k38_object_bi_bo": ("trang = d if isinstance(d, list) else [d]", "trang = d if isinstance(d, list) else []",
                            ["kg_m2_object_mot_trang"]),
    "kg_k39_khong_in_dong_do": ('            print(f"  ĐỎ  {dong}", file=sys.stderr)', "            pass", ["kg_m3_huy_moi_nhat"]),
    "kg_k40_bo_break": ("                break\n        else:\n            xanh.append", "        else:\n            xanh.append",
                        ["kg_k40_hai_ban_do_mot_ten"]),
})

MUTANTS.update({
    **{f"kg_r2_sha_{n}": ('SHA_RE = re.compile(r"^[0-9a-f]{40}\\Z")', f'SHA_RE = re.compile(r"^{r}\\Z")', [f"kg_r2_sha_{n}"])
       for n, r in (("phi_hex", "[0-9a-z]{40}"), ("39", "[0-9a-f]{39,40}"), ("41", "[0-9a-f]{40,41}"))},
    "kg_r2_id_theo_chuoi": ('id_max = max(r["id"] for r in cung)', 'id_max = max((r["id"] for r in cung), key=str)',
                            ["kg_r2_id_so_moi_do", "kg_r2_id_so_moi_xanh"]),
    "kg_r2_canh_bao_dem_1": ("{len(khac)} run ở suite khác", "{1} run ở suite khác", ["kg_n4_canh_bao"]),
    "kg_r2_canh_bao_id_dau": ("', '.join(map(str, khac))", "', '.join(map(str, khac[:1]))", ["kg_n4_canh_bao"]),
    "kg_r2_canh_bao_ten_dau": ("    for ten_cb in ten_bb:\n", "    for ten_cb in ten_bb[:1]:\n", ["kg_n4_canh_bao"]),
    "kg_r2_schema_trang_dau": ("            if sai:\n", "            if sai and i == 0:\n",
                               [n for n in _KG_CA if n.startswith("kg_r2_trang_sau_") and n.endswith(("_vang", "_kieu"))]),
    "kg_r2_suite_trang_dau": ('            if not isinstance(cs, dict) or type(cs.get("id", _VANG)) is not int:\n',
                              '            if i == 0 and (not isinstance(cs, dict) or type(cs.get("id", _VANG)) is not int):\n',
                              ["kg_r2_trang_sau_suite_chuoi"]),
    "kg_r2_tc_trang_dau": ("        if type(tc) is not int or tc < 0:\n", "        if i == 0 and (type(tc) is not int or tc < 0):\n",
                           ["kg_r2_trang_sau_tc_thuc", "kg_r2_trang_sau_tc_bool"]),
    "kg_r2_bo_trang_sau_hong": ('            hong(f"trang {i} không phải object có',
                                '            if i > 0:\n                continue\n            hong(f"trang {i} không phải object có',
                                ["kg_r2_trang_sau_page_shape"]),
    "kg_r2_bo_run_trang_sau": ('                hong(f"trang {i} check_runs[{j}] không phải object")',
                               '                if i > 0:\n                    continue\n                hong(f"trang {i} check_runs[{j}] không phải object")',
                               ["kg_r2_trang_sau_run_shape"]),
    "kg_r2_so_hai_trang_dau": ("    if any(t != tong_khai for t in khai):\n", "    if any(t != tong_khai for t in khai[:2]):\n",
                               ["kg_r2_ba_trang_lech_cuoi"]),
})

# Review 4: mỗi chỗ so × mỗi cách NỚI phép `==` một đột biến, sinh bằng vòng (lớp, không danh sách tay).
_KG_NOI = {"hoa": "{}.casefold()", "strip": "{}.strip()", "nfkc": 'unicodedata.normalize("NFKC", {})',
           "nfc": 'unicodedata.normalize("NFC", {})', "bo_dau": "{}[1:]", "bo_cuoi": "{}[:-1]"}
_KG_R4 = {}
for _cho, _x, _y, _sau in (("status", 'r["status"]', '"completed"', ""), ("conclusion", 'r["conclusion"]', '"success"', ""),
                           ("head", 'r["head_sha"]', "a.head", ""), ("ten", 'r["name"]', "ten", "]"),
                           ("canh_bao", 'r["name"]', "ten_cb", "")):
    for _n, _f in [*_KG_NOI.items()][:4 if _cho in ("ten", "canh_bao") else 3] + [("tien_to", None), ("hau_to", None)]:
        _thay = (f"{_x}.startswith({_y})" if _n == "tien_to" else f"{_x}.endswith({_y})" if _n == "hau_to"
                 else f"{_f.format(_x)} == {_f.format(_y)}").replace("unicodedata", '__import__("unicodedata")')
        _KG_R4.setdefault(_cho, []).append(f"kg_r4_{_cho}_{_n}")
        MUTANTS[f"kg_r4_{_cho}_{_n}"] = (f"{_x} == {_y}{_sau}", _thay + _sau,
                                         ["kg_r4_gan_canh_bao" if _cho == "canh_bao" else f"kg_r4_gan_{_cho}"])
        if _cho in ("ten", "canh_bao") and _f:   # chuẩn hoá MỘT phía: chỉ run, hoặc chỉ đối số
            for _phia, _a, _b in (("run", _f.format(_x), _y), ("doi_so", _x, _f.format(_y))):
                _KG_R4[_cho].append(f"kg_r4_{_cho}_{_n}_{_phia}")
                MUTANTS[f"kg_r4_{_cho}_{_n}_{_phia}"] = (f"{_x} == {_y}{_sau}", f"{_a} == {_b}{_sau}".replace(
                    "unicodedata", '__import__("unicodedata")'), ["kg_r4_tha_ten"])
_KG_DT_DONG = 'dt = (r["name"], r["check_suite"]["id"], r["head_sha"])'
for _cho, _x in (("dt_ten", 'r["name"]'), ("dt_head", 'r["head_sha"]')):
    for _n, _f in [*_KG_NOI.items()][:4 if _cho == "dt_ten" else 3] + [*_KG_NOI.items()][4:]:
        _KG_R4.setdefault(_cho, []).append(f"kg_r4_{_cho}_{_n}")
        MUTANTS[f"kg_r4_{_cho}_{_n}"] = (_KG_DT_DONG, _KG_DT_DONG.replace(_x, _f.format(_x).replace(
            "unicodedata", '__import__("unicodedata")'), 1), [f"kg_r4_gan_{_cho}"])
MUTANTS.update({
    "kg_r4_do_chi_cuoi": ("        for dong in do:\n", "        for dong in do[-1:]:\n", ["kg_r4_ba_ten"]),
    "kg_r4_do_hai_dau": ("        for dong in do:\n", "        for dong in do[:1] + do[-1:]:\n", ["kg_r4_ba_ten"]),
    "kg_r4_canh_bao_id_hai_dau": ("', '.join(map(str, khac))", "', '.join(map(str, khac[:1] + khac[-1:]))", ["kg_r4_ba_ten"]),
    "kg_r4_canh_bao_ten_hai_dau": ("for ten_cb in ten_bb:", "for ten_cb in ten_bb[:1] + ten_bb[-1:]:", ["kg_r4_ba_ten"]),
})

# Review 5: đột biến sinh bằng vòng, mỗi lớp một họ.
_KG_R5 = {}


def _kg_r5(lop, ten, tim, thay, ca):
    _KG_R5.setdefault(lop, []).append(f"kg_r5_{ten}")
    MUTANTS[f"kg_r5_{ten}"] = (tim, thay, [ca])


for _t, (_tim, _goc) in {"id": ('("id", (int,))', "(int, {})"), "name": ('("name", (str,))', "(str, {})"),
                         "head_sha": ('("head_sha", (str,))', "(str, {})"), "status": ('("status", (str,))', "(str, {})"),
                         "conclusion": ('("conclusion", (str, type(None)))', "(str, type(None), {})"),   # `{}` = kiểu được nới
                         "suite": ('type(cs.get("id", _VANG)) is not int', None)}.items():
    for _k, _ in _KG_KIEU:
        if _k in _KG_CHO_PHEP[_t] or (_t == "id" and _k in ("list", "dict")):   # id list/dict: không băm được ⇒ sập (M6)
            continue
        _py = "type(None)" if _k == "null" else _k
        _thay = (f'type(cs.get("id", _VANG)) not in (int, {_py})' if _goc is None
                 else _tim.replace(_goc.split(", {}")[0] + (",)" if _goc.count(",") == 1 else ")"), _goc.format(_py)))
        assert _thay != _tim, _t   # đột biến PHẢI đổi mã — bản đầu không đổi gì mà vẫn được khai
        _kg_r5(_t, f"kieu_{_t}_{_k}", _tim, _thay, f"kg_r5_kieu_{_t}")
_KG_VONG_TRANG = "    for i, tr in enumerate(trang):\n"
for _dk, _dkn in (("i", "sau"), ("not i", "dau")):
    for _ten, _bo in (("khong_object", "not isinstance(tr, dict)"),
                      ("thieu_check_runs", 'isinstance(tr, dict) and "check_runs" not in tr')):
        _kg_r5("trang", f"trang_bo_{_ten}_{_dkn}", _KG_VONG_TRANG, f"{_KG_VONG_TRANG}        if {_dk} and {_bo}:\n            continue\n",
               "kg_r5_trang")
for _k in ("str", "dict"):
    _kg_r5("trang", f"check_runs_nhan_{_k}", 'not isinstance(tr.get("check_runs"), list)',
           f'not isinstance(tr.get("check_runs"), (list, {_k}))', "kg_r5_trang")
_KG_CAT = {"dau": "{}[:1]", "cuoi": "{}[-1:]", "hai_dau": "{0}[:1] + {0}[-1:]", "bo_dau": "{}[1:]", "bo_cuoi": "{}[:-1]",
           "xen_ke": "{}[::2]", "hai_dau_2": "{0}[:2] + {0}[-2:]", "dau_2": "{}[:2]"}
for _n, _f in _KG_CAT.items():
    _kg_r5("vi_tri_ten", f"ten_bb_{_n}", "t.splitlines() != [t] for t in ten_bb)",
           f"t.splitlines() != [t] for t in {_f.format('ten_bb')})", "kg_r5_vi_tri")
    _kg_r5("vi_tri_dt", f"danh_tinh_{_n}", "    for r in runs:\n        dt =", f"    for r in {_f.format('runs')}:\n        dt =",
           "kg_r5_vi_tri")
_KG_VANG = '            do.append(f"{ten!r}: VẮNG — không check-run nào mang đúng tên này trong suite {suite}")\n'
for _n, _g in (("dau", "ten == ten_bb[0]"), ("cuoi", "ten == ten_bb[-1]"), ("co_run", "runs"), ("mot_ten", "len(ten_bb) == 1")):
    _kg_r5("vi_tri_vang", f"vang_chi_{_n}", _KG_VANG, f"            if {_g}:\n    " + _KG_VANG.lstrip(" ").rjust(len(_KG_VANG) + 4),
           "kg_r5_vi_tri")
for _n, _thay in (("abs", 'max((r["id"] for r in cung), key=abs)'), ("float", 'max((r["id"] for r in cung), key=float)'),
                  ("am", 'max((r["id"] for r in cung), key=lambda x: -x)'), ("cuoi", 'cung[-1]["id"]'), ("dau", 'cung[0]["id"]')):
    _kg_r5("id", f"id_max_{_n}", 'id_max = max(r["id"] for r in cung)', f"id_max = {_thay}", "kg_r5_id")
for _n, _f in (("strip", "{}.strip()"), ("lstrip", "{}.lstrip()"), ("rstrip", "{}.rstrip()"),
               ("nfkc", '__import__("unicodedata").normalize("NFKC", {})')):
    _kg_r5("head_arg", f"head_arg_{_n}", "SHA_RE.fullmatch(a.head)", f"SHA_RE.fullmatch({_f.format('a.head')})", "kg_r5_doi_so")
    _kg_r5("suite_arg", f"suite_arg_{_n}", 're.fullmatch(r"[1-9][0-9]*", a.check_suite)',
           f're.fullmatch(r"[1-9][0-9]*", {_f.format("a.check_suite")})', "kg_r5_doi_so")
_kg_r5("head_arg", "head_lop_d", 'SHA_RE = re.compile(r"^[0-9a-f]{40}\\Z")', 'SHA_RE = re.compile(r"^[\\da-f]{40}\\Z")',
       "kg_r5_doi_so")
for _tr, _goc in (("status", 'r["status"] == "completed"'), ("conclusion", 'r["conclusion"] == "success"')):
    for _n, _g in (("tru_dau", "r is cung[0]"), ("chi_dau", "r is not cung[0]"), ("tru_cuoi", "r is cung[-1]"),
                   ("chi_cuoi", "r is not cung[-1]")):
        _kg_r5(_tr, f"trung_id_{_tr}_{_n}", _goc, f"({_g} or {_goc})", "kg_r5_trung_id")

# Đầu ra THÀNH CÔNG nguyên văn (review 5 xếp "quan sát"; đóng luôn để dòng xanh/cảnh báo không trôi).
_KG_CB = 'khac = sorted({r["id"] for r in runs if r["name"] == ten_cb and r["check_suite"]["id"] != suite})'
for _lop, _ten, _tim, _thay, _ca in (
        ("xanh", "xanh_id_dau", 'xanh.append(f"{ten} id={id_max}")', """xanh.append(f"{ten} id={cung[0]['id']}")""", "kg_r5_id"),
        ("xanh", "xanh_id_cuoi", 'xanh.append(f"{ten} id={id_max}")', """xanh.append(f"{ten} id={cung[-1]['id']}")""", "kg_r5_id"),
        ("xanh", "xanh_bo_head", 'print(f"gate XANH trên {a.head} (suite {suite}): "', 'print(f"gate XANH (suite {suite}): "', "kg_r5_id"),
        ("xanh", "xanh_sap_xep", '" · ".join(xanh))', '" · ".join(sorted(xanh)))', "kg_r5_id"),
        ("canh_bao_thu_tu", "canh_bao_sap_chu", _KG_CB, _KG_CB[:-1] + ", key=str)", "kg_r4_ba_ten"),
        ("canh_bao_thu_tu", "canh_bao_khong_sap", _KG_CB, "khac = list(" + _KG_CB[len("khac = sorted("):], "kg_r4_ba_ten")):
    _kg_r5(_lop, _ten, _tim, _thay, _ca)

# --- #856 `KG-RANG-TEST-2` (spec `ops/specs/wp856.md` r1, T1–T6, M1–M4) -----------------------------------------
# Tập toán tử CỐ ĐỊNH: mỗi ô vị trí × toán tử của `tap_toan_tu` ⇒ một đột biến SINH BẰNG VÒNG (giết không sập, M6)
# hoặc `tuong_duong`/`khong_ap_dung` kèm lập luận. `_KG_MA_TRAN` ghi TỪNG ô để đối chiếu A4. Ca đích theo
# (họ, vị trí): một đột biến chỉ chạy vài fixture, nên số ô không làm job `gate-packet-loop` phình theo.
def _kg_kiem(c: Ctx, du_lieu=None, bat_buoc=("gate",), expect=12, chua="", head=_KG_HEAD, tho=None, suite=_KG_SUITE,
             dong_xanh=None, canh_bao=None, dem=False):
    """MỘT lần gọi CLI: rc + lý do (đỏ) hoặc dòng xanh (xanh), cộng cảnh báo NGUYÊN VĂN khi khai `canh_bao`."""
    rc, o, e = _kg(c, du_lieu, *bat_buoc, head=head, tho=tho, suite=suite, dem=dem)
    if expect != 0:
        _doi_ly_do(expect, rc, e, chua, "kiem-gate")
    else:
        _doi(0, rc, e, "gate phải XANH")
        if not re.fullmatch(re.escape(f"gate XANH trên {head} (suite {suite}): ")   # tên NGUYÊN VĂN, đúng thứ tự `--bat-buoc`
                            + re.escape(" · ").join(re.escape(t) + r" id=-?[0-9]+" for t in dict.fromkeys(bat_buoc)), _txt(o)):
            raise AssertionError(f"dòng xanh thiếu suite hoặc tên: {_txt(o)!r}")
        if dong_xanh is not None and _txt(o) != dong_xanh:
            raise AssertionError(f"dòng xanh đòi {dong_xanh!r}, được {_txt(o)!r}")
    if canh_bao is not None and [d for d in _txt(e).splitlines() if d.startswith("CẢNH BÁO:")] != list(canh_bao):
        raise AssertionError(f"cảnh báo đòi {list(canh_bao)!r}, được {_txt(e)!r}")


def _kg_ho(ten, muc):
    """Ca đích của MỘT họ: dừng ở lần ĐỎ SẠCH đầu tiên. CLI sập ở một mục không che mục sau (mục sau có thể giết
    sạch); chỉ khi không mục nào đỏ sạch mới ném lại cú sập ⇒ `_TinDungGia`, không phải GIẾT (M6)."""
    def ca(c: Ctx):
        sap = loi = None
        for nhan, kw, _sua in muc():
            try:
                _kg_kiem(c, **kw)
            except AssertionError as ex:
                loi = f"{ten}/{nhan}: {ex}"
            except CliSapDo as ex:
                sap = sap or ex
            if loi:
                break
        if loi:   # NGOÀI khối except: lỗi sạch không mang cú sập nào trong `__context__`
            raise AssertionError(loi)
        if sap:
            raise sap
    ca.muc = muc   # #856 T6: duyệt bản sửa của MỌI họ đã đăng vào CASES, không qua một danh sách chép tay
    return ca


_KG_GOC = CANONICAL.read_text(encoding="utf-8")
_KG_T_K = {}   # hàng mới của `_KG_KIEM_KE`: "<họ T>-<hàng K của #822>" → đột biến
_KG_MA_TRAN = {}   # (họ, vị trí, toán tử) → tên đột biến | ("tuong_duong" | "khong_ap_dung", lập luận)


def _kg_ap(goc, tim, thay):
    for t, th in _cap_thay_the(tim, thay):
        goc = goc.replace(t, th, 1)
    return goc


_KG_DA_CO = {hashlib.sha256(_kg_ap(_KG_GOC, *v[:2]).encode()).hexdigest(): k
             for k, v in MUTANTS.items() if k.startswith("kg_")}


def _kg_o(ho, vi_tri, toan_tu, k, ten, tim, thay, ca):
    """Đăng ký MỘT ô bằng một đột biến. Đột biến PHẢI đổi mã (bài học #822: bộ sinh từng khai 22 đột biến không đổi
    gì); trùng NGUỒN sau đột biến với một đột biến đã có ⇒ ô trỏ về tên cũ, không chạy hai lần cùng một mã."""
    moi = _kg_ap(_KG_GOC, tim, thay)
    assert all(t != th for t, th in _cap_thay_the(tim, thay)) and moi != _KG_GOC, f"{ten}: đột biến không đổi mã"
    bam = hashlib.sha256(moi.encode()).hexdigest()
    if bam not in _KG_DA_CO:
        MUTANTS[ten] = (tim, thay, [ca])
        _KG_DA_CO[bam] = ten
        _KG_T_K.setdefault(f"{ho}-{k}", []).append(ten)
    _KG_MA_TRAN[(ho, vi_tri, toan_tu)] = _KG_DA_CO[bam]


def _kg_khong(ho, vi_tri, toan_tu, loai, ly_do):
    _KG_MA_TRAN[(ho, vi_tri, toan_tu)] = (loai, ly_do)


_KG_A_SAI = "            sai = [k for k, kieu in _TRUONG_CHECK_RUN if type(r.get(k, _VANG)) not in kieu]\n"
_KG_A_CS = '            cs = r.get("check_suite", _VANG)\n'
_KG_A_RUN = "            if not isinstance(r, dict):\n"
_KG_A_TRANG = '        if not isinstance(tr, dict) or not isinstance(tr.get("check_runs"), list):\n'
_KG_A_TC = '        tc = tr.get("total_count", _VANG)\n'
_KG_A_SUITE = '            if not isinstance(cs, dict) or type(cs.get("id", _VANG)) is not int:\n'

# --- T1: kiểu JSON × hiện diện. Vị trí → (kiểu cho phép, có thể VẮNG, hàng K).
_KG_T1_VI_TRI = {"id": (("int",), True, "K09"), "name": (("str",), True, "K10"), "head_sha": (("str",), True, "K11"),
                 "status": (("str",), True, "K12"), "conclusion": (("str", "null"), True, "K13"),
                 "check_suite": (("dict",), True, "K15"), "check_suite.id": (("int",), True, "K15"),
                 "phan_tu": (("dict",), False, "K08"), "trang": (("dict",), False, "K05"),
                 "check_runs": (("list",), True, "K05"), "total_count": (("int",), True, "K07")}
_KG_T1_KIEU = (*_KG_KIEU, ("vang", _VANG_T))
_KG_T1_PY = {"null": "type(None)", "bool": "bool", "int": "int", "float": "float", "str": "str", "list": "list",
             "dict": "dict"}


def _kg_t1_cac_kieu(vi_tri):
    cho, vang, _ = _KG_T1_VI_TRI[vi_tri]
    return [(k, v) for k, v in _KG_T1_KIEU if k not in cho and (k != "vang" or vang)]


def _kg_t1_run(vi_tri, gt):   # run KHÔNG bắt buộc id 15, sai ĐÚNG vị trí
    if vi_tri == "phan_tu":
        return gt
    if vi_tri == "check_suite.id":
        return _kg_khac(id=15, check_suite={} if gt is _VANG_T else {"id": gt})
    return _kg_khac(**{"id": 15, vi_tri: gt})


def _kg_t1_ly_do(vi_tri, kieu, tien_to):
    if vi_tri in ("trang", "check_runs"):
        return f"{tien_to} {_KG_TRANG}"
    if vi_tri == "total_count":
        return f"{tien_to} thiếu `total_count`" if kieu == "vang" else f"{tien_to}: `total_count` không phải số nguyên ≥ 0"
    if vi_tri == "phan_tu":
        return f"{tien_to} không phải object"
    return f"{tien_to} {_KG_CS}" if vi_tri.startswith("check_suite") else f"{tien_to} {_KG_TRUONG} ['{vi_tri}']"


def _kg_t1_muc(vi_tri, kieu, gt, ep=None):
    """Run-level: đầu/giữa/cuối × (một trang · trang GIỮA của ba trang), luôn có run hợp lệ trước HOẶC sau trong trang
    và cả hai phía qua trang. Trang-level: đầu/giữa/cuối giữa năm trang hợp lệ, cộng trang duy nhất.
    `ep` (#856 lượt 2): giá trị sai là ẢNH ÉP KIỂU của đúng giá trị ở chỗ ấy trong bản sửa — nhận-sau-ép ra XANH, bỏ-qua ra
    thiếu id, nên mọi hiện thực "ép được thì nhận/bỏ" đều đổi hành vi."""
    g = (lambda dung: ep(dung)) if ep else (lambda dung: gt)
    if vi_tri not in ("trang", "check_runs", "total_count"):
        tot = _kg_khac(id=15)
        hong = _kg_t1_run(vi_tri, g({"id": 15, "check_suite.id": 1, "check_suite": {"id": 1}, "phan_tu": tot}.get(vi_tri)))
        for vt, j in (("dau", 0), ("giua", 2), ("cuoi", 4)):
            ds = [_kg_run(11), *(_kg_run(i, name="khac") for i in (12, 13, 14))]
            lam = lambda x: {"total_count": 5, "check_runs": ds[:j] + [x] + ds[j:]}
            yield f"mot_trang_{vt}", dict(du_lieu=lam(hong), chua=_kg_t1_ly_do(vi_tri, kieu, f"trang 0 check_runs[{j}]")), \
                dict(du_lieu=lam(tot), expect=0)
        for vt, j in (("dau", 0), ("giua", 1), ("cuoi", 2)):
            giua = [_kg_run(11), _kg_run(23, name="khac")]
            lam = lambda x: [{"total_count": 7, "check_runs": [_kg_run(21, name="khac"), _kg_run(22, name="khac")]},
                             {"total_count": 7, "check_runs": giua[:j] + [x] + giua[j:]},
                             {"total_count": 7, "check_runs": [_kg_run(24, name="khac"), _kg_run(25, name="khac")]}]
            yield f"ba_trang_{vt}", dict(du_lieu=lam(hong), chua=_kg_t1_ly_do(vi_tri, kieu, f"trang 1 check_runs[{j}]")), \
                dict(du_lieu=lam(tot), expect=0)
        return
    tc = 6 if vi_tri == "total_count" else 5
    tot = [{"total_count": tc, "check_runs": [_kg_run(i, name="gate" if i == 33 else "khac")]} for i in (31, 32, 33, 34, 35)]
    run_trang = [_kg_run(36, name="khac")] if vi_tri == "total_count" else []
    lam = {"trang": lambda g, n: g,
           "check_runs": lambda g, n: {"total_count": n, **({} if g is _VANG_T else {"check_runs": g})},
           "total_count": lambda g, n: {**({} if g is _VANG_T else {"total_count": g}), "check_runs": run_trang}}[vi_tri]
    sua = {"trang": lambda n: {"total_count": n, "check_runs": []}, "check_runs": lambda n: {"total_count": n, "check_runs": []},
           "total_count": lambda n: {"total_count": n, "check_runs": run_trang}}[vi_tri]
    gn = {"trang": lambda n: g(sua(n)), "check_runs": lambda n: g([]), "total_count": lambda n: g(n)}[vi_tri]
    for vt, p in (("dau", 0), ("giua", 2), ("cuoi", 5)):
        yield f"nam_trang_{vt}", dict(du_lieu=tot[:p] + [lam(gn(tc), tc)] + tot[p:], chua=_kg_t1_ly_do(vi_tri, kieu, f"trang {p}")), \
            dict(du_lieu=tot[:p] + [sua(tc)] + tot[p:], expect=0)
    # Trang DUY NHẤT: bản sửa mang run `gate` ngay trong chính phần tử đích (không còn trang nào khác giữ nó).
    mot = {"trang": lambda: {"total_count": 1, "check_runs": [_kg_run(11)]},
           "check_runs": lambda: {"total_count": 1, "check_runs": [_kg_run(11)]},
           "total_count": lambda: {"total_count": 1, "check_runs": [_kg_run(11)]}}[vi_tri]()
    g1 = {"trang": lambda: g(mot), "check_runs": lambda: g([_kg_run(11)]), "total_count": lambda: g(1)}[vi_tri]()
    hong1 = {"trang": g1, "check_runs": {"total_count": 1, **({} if g1 is _VANG_T else {"check_runs": g1})},
             "total_count": {**({} if g1 is _VANG_T else {"total_count": g1}), "check_runs": [_kg_run(11)]}}[vi_tri]
    yield "trang_duy_nhat", dict(du_lieu=[hong1], chua=_kg_t1_ly_do(vi_tri, kieu, "trang 0")), dict(du_lieu=[mot], expect=0)


_kg_cap = lambda d: [[k, v] for k, v in d.items()]
# Miền ÉP ĐƯỢC (#856 lượt 2): (vị trí, kiểu) → [(nhãn, ép giá trị đúng thành kiểu sai, vị từ, phép ép ngược)].
_KG_T1_EP_LOAI = {"nguyen": (float, "type({x}) is float and {x}.is_integer()", "int({x})"),
                  "chuoi_so": (str, "type({x}) is str and {x}.isdecimal()", "int({x})"),
                  "cap": (_kg_cap, "type({x}) is list and all(type(p) is list and len(p) == 2 for p in {x})", "dict({x})"),
                  "json": (json.dumps, 'type({x}) is str and {x}[:1] in ("[", "{{")', "json.loads({x})")}
_KG_T1_EP = {("id", "float"): "nguyen", ("id", "str"): "chuoi_so", ("check_suite.id", "float"): "nguyen",
             ("check_suite.id", "str"): "chuoi_so", ("total_count", "float"): "nguyen", ("total_count", "str"): "chuoi_so",
             ("phan_tu", "list"): "cap", ("phan_tu", "str"): "json", ("check_suite", "list"): "cap", ("check_suite", "str"): "json",
             ("trang", "list"): "cap", ("trang", "str"): "json", ("check_runs", "str"): "json"}
_KG_T1_CA = {}
for _vt in _KG_T1_VI_TRI:
    for _k, _gt in _kg_t1_cac_kieu(_vt):
        _ca = f"kg_t1_{_vt.replace('.', '_')}_{_k}"
        _ep = _KG_T1_EP.get((_vt, _k))
        _KG_T1_CA[_ca] = (lambda vt=_vt, k=_k, gt=_gt, ep=_ep: (*_kg_t1_muc(vt, k, gt), *(
            (f"ep_{ep}_{n}", kw, sua) for n, kw, sua in (_kg_t1_muc(vt, k, gt, _KG_T1_EP_LOAI[ep][0]) if ep else ()))))
        _p = (lambda x, k=_k: f"{x} is _VANG" if k == "vang" else f"type({x}) is {_KG_T1_PY[k]}")
        _hang = "K06" if (_vt, _k) == ("total_count", "vang") else _KG_T1_VI_TRI[_vt][2]
        if _vt in ("id", "name", "head_sha", "status", "conclusion"):
            _x = f'r.get("{_vt}", _VANG)'
            _tot = {"id": "10 ** 6", "name": '"khac"', "head_sha": '"x"', "status": '"completed"', "conclusion": "None"}[_vt]
            _nhan = (_KG_A_SAI, f"            if {_p(_x)}:\n                r = {{**r, \"{_vt}\": {_tot}}}\n" + _KG_A_SAI)
            _bo = (_KG_A_SAI, f"            if {_p(_x)}:\n                continue\n" + _KG_A_SAI)
        elif _vt == "check_suite":
            _nhan = (_KG_A_CS, _KG_A_CS + f'            if {_p("cs")}:\n                cs = {{"id": 9}}\n'
                                         '                r = {**r, "check_suite": cs}\n')
            _bo = (_KG_A_CS, _KG_A_CS + f'            if {_p("cs")}:\n                continue\n')
        elif _vt == "check_suite.id":
            _x = 'cs.get("id", _VANG)'
            _nhan = (_KG_A_CS, _KG_A_CS + f'            if isinstance(cs, dict) and {_p(_x)}:\n                cs = {{**cs, "id": 9}}\n'
                                         '                r = {**r, "check_suite": cs}\n')
            _bo = (_KG_A_CS, _KG_A_CS + f"            if isinstance(cs, dict) and {_p(_x)}:\n                continue\n")
        elif _vt == "phan_tu":
            _nhan = (_KG_A_RUN, f'            if {_p("r")}:\n                r = {{"id": 10 ** 6, "name": "khac", "head_sha": "x", '
                                '"status": "completed", "conclusion": None, "check_suite": {"id": 9}}\n' + _KG_A_RUN)
            _bo = (_KG_A_RUN, f'            if {_p("r")}:\n                continue\n' + _KG_A_RUN)
        elif _vt == "trang":
            _nhan = (_KG_A_TRANG, f'        if {_p("tr")}:\n            tr = {{"total_count": next((t["total_count"] for t in trang '
                                  'if type(t) is dict and type(t.get("total_count")) is int), 0), "check_runs": []}\n' + _KG_A_TRANG)
            _bo = (_KG_A_TRANG, f'        if {_p("tr")}:\n            continue\n' + _KG_A_TRANG)
        elif _vt == "check_runs":
            _x = 'tr.get("check_runs", _VANG)'
            _nhan = (_KG_A_TRANG, f'        if isinstance(tr, dict) and {_p(_x)}:\n            tr = {{**tr, "check_runs": []}}\n' + _KG_A_TRANG)
            _bo = (_KG_A_TRANG, f"        if isinstance(tr, dict) and {_p(_x)}:\n            continue\n" + _KG_A_TRANG)
        else:   # total_count: nhận = ép về số id THẬT trên mọi trang (mạnh nhất có thể); bỏ qua = bỏ cả trang
            _nhan = (_KG_A_TC, _KG_A_TC + f'        if {_p("tc")}:\n            tc = len({{json.dumps(x.get("id")) for t in trang '
                     'if isinstance(t, dict) and isinstance(t.get("check_runs"), list) for x in t["check_runs"] if isinstance(x, dict)})\n')
            _bo = (_KG_A_TC, _KG_A_TC + f'        if {_p("tc")}:\n            continue\n')
        for _tt, (_tim, _thay) in (("nhan", _nhan), ("bo_qua", _bo)):
            _kg_o("T1", f"{_vt}:{_k}", _tt, _hang, f"{_ca}_{_tt}", _tim, _thay, _ca)
        if _ep:   # hiện thực "ép được thì nhận / bỏ cái ép được" — mỗi miền một cặp đột biến riêng
            _, _vd, _ct = _KG_T1_EP_LOAI[_ep]
            _x, _vao, _gan = {"id": ('r.get("id", _VANG)', "truoc_sai", 'r = {{**r, "id": {c}}}'),
                              "check_suite.id": ('(cs.get("id", _VANG) if isinstance(cs, dict) else _VANG)', "sau_cs",
                                                 'cs = {{**cs, "id": {c}}}\n                r = {{**r, "check_suite": cs}}'),
                              "check_suite": ("cs", "sau_cs", 'cs = {c}\n                r = {{**r, "check_suite": cs}}'),
                              "phan_tu": ("r", "truoc_run", "r = {c}"), "trang": ("tr", "truoc_trang", "tr = {c}"),
                              "check_runs": ('(tr.get("check_runs", _VANG) if isinstance(tr, dict) else _VANG)', "truoc_trang",
                                             'tr = {{**tr, "check_runs": {c}}}'),
                              "total_count": ("tc", "sau_tc", "tc = {c}")}[_vt]
            _le = "        " if _vao in ("truoc_trang", "sau_tc") else "            "
            _neo = {"truoc_sai": _KG_A_SAI, "sau_cs": _KG_A_CS, "truoc_run": _KG_A_RUN, "truoc_trang": _KG_A_TRANG, "sau_tc": _KG_A_TC}[_vao]
            for _tt in ("nhan", "bo_qua"):
                _than = (f"{_le}if {_vd.format(x=_x)}:\n{_le}    "
                         + ("continue" if _tt == "bo_qua" else _gan.format(c=_ct.format(x=_x)).replace("\n                ", "\n" + _le + "    "))
                         + "\n")
                _kg_o("T1", f"{_vt}:{_k}:ep_{_ep}", _tt, _hang, f"{_ca}_ep_{_ep}_{_tt}", _neo,
                      (_neo + _than) if _vao.startswith("sau") else (_than + _neo), _ca)

# --- T2: nới phép so chuỗi. Toán tử → (mã nguồn, hàm Python CÙNG nghĩa để tự tính fixture nào giết ô nào).
_KG_NFC = '__import__("unicodedata").normalize("NFC", {})'
_KG_T2_F = {"casefold": ("{}.casefold()", str.casefold), "strip": ("{}.strip()", str.strip),
            "lstrip": ("{}.lstrip()", str.lstrip), "rstrip": ("{}.rstrip()", str.rstrip),
            "nfc": (_KG_NFC, lambda s: unicodedata.normalize("NFC", s)),
            "nfkc": (_KG_NFC.replace("NFC", "NFKC"), lambda s: unicodedata.normalize("NFKC", s)),
            "bo_dau": ("{}[1:]", lambda s: s[1:]), "bo_cuoi": ("{}[:-1]", lambda s: s[:-1]),
            "bo_giua": ("(lambda s: s[:len(s) // 2] + s[len(s) // 2 + 1:])({})", lambda s: s[:len(s) // 2] + s[len(s) // 2 + 1:]),
            "sap_xep": ('"".join(sorted({}))', lambda s: "".join(sorted(s)))}
_KG_T2_PHIA = {"hai_phia": (lambda f, x, y: f.format(x) + " == " + f.format(y), lambda g, x, y: g(x) == g(y)),
               "trai": (lambda f, x, y: f.format(x) + " == " + y, lambda g, x, y: g(x) == y),
               "phai": (lambda f, x, y: x + " == " + f.format(y), lambda g, x, y: x == g(y))}
_KG_T2_HUONG = {"startswith_xy": ("{x}.startswith({y})", lambda x, y: x.startswith(y)),
                "startswith_yx": ("{y}.startswith({x})", lambda x, y: y.startswith(x)),
                "endswith_xy": ("{x}.endswith({y})", lambda x, y: x.endswith(y)),
                "endswith_yx": ("{y}.endswith({x})", lambda x, y: y.endswith(x))}
# Giá trị KHÔNG chuẩn ở MỌI toán tử (hoa · đệm hai đầu · NFD · fullwidth · không sắp xếp): chiều THA của mọi phép
# chuẩn hoá MỘT phía — run và đối số trùng nguyên văn mà một phía bị chuẩn hoá thì phép bằng vỡ.
_KG_T2_KHONG_CHUAN = " \uff27ae\u0301tE "


def _kg_bien_the(v):
    """Họ gần đúng: mỗi biến thể THẬT SỰ khác `v` (bài học #822: đổi ký tự đầu `completed` bằng `c` trùng gốc)."""
    ds = {"hoa": v.upper(), "dem": f" {v} ", "dem_trai": " " + v, "dem_phai": v + " ", "nfd": unicodedata.normalize("NFD", v),
          "rong": "".join(chr(ord(k) + 0xFEE0) if "!" <= k <= "~" else k for k in v), "tien_to": "x" + v, "hau_to": v + "x",
          "cat_dau": v[1:], "cat_cuoi": v[:-1], "dao": v[::-1], "chen_giua": v[:(len(v) + 1) // 2] + "x" + v[(len(v) + 1) // 2:],
          "doi_cho_0": v[1:2] + v[:1] + v[2:],
          **{f"anh_{f}": g(v) for f, (_, g) in _KG_T2_F.items()}}   # ẢNH f(v): hiện thực `x == y or x == f(y)` cần nó
    for i in range(len(v)):   # #856 lượt 2: MỌI chỉ số — "bỏ một ký tự giữa" không chỉ là chỉ số trung tâm
        k = v[i]
        ds[f"doi_{i}"] = v[:i] + ("x" if k != "x" else "y") + v[i + 1:]
        ds[f"bo_{i}"] = v[:i] + v[i + 1:]
        ds[f"lap_{i}"] = v[:i] + k + v[i:]
    ra = {n: p for n, p in ds.items() if p != v}
    assert all(p != v for p in ra.values())
    return ra


def _kg_t2_so(x, y):   # chỗ so trực tiếp `x == y`: x phía run, y phía hằng/đối số
    return {"mau": f"{x} == {y}", "x": x, "y": y}


_KG_T2_VI_TRI = {   # vị trí → (hàng K, đích nghiêm, giá trị tha, dựng fixture nghiêm p, dựng fixture tha v)
    "status": ("K32", ("completed",), ("completed",),
               lambda p, t: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, status=p)]}, chua=f"status={p!r}"),
               lambda v: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, status=v)]}, expect=0)),
    "conclusion": ("K33", ("success",), ("success",),
                   lambda p, t: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, conclusion=p)]}, chua=f"conclusion={p!r}"),
                   lambda v: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, conclusion=v)]}, expect=0)),
    # Đích ĐÃ SẮP XẾP (head hợp lệ, tên) để hiện thực `sorted(x) == y` có tiền ảnh; tên KHÔNG CHUẨN làm đích để ảnh f(đích) ≠ đích.
    "head": ("K34", (_KG_HEAD, "".join(sorted(_KG_HEAD))), (_KG_HEAD,),
             lambda p, t: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, head=p)]}, head=t, chua=f"head_sha={p!r}"),
             lambda v: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, head=v)]}, head=v, expect=0)),
    "ten": ("K27", (_KG_T, "".join(sorted(_KG_T)), _KG_T2_KHONG_CHUAN), (_KG_T, _KG_T2_KHONG_CHUAN),
            lambda p, t: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, name=p)]}, bat_buoc=(t,), chua="VẮNG"),
            lambda v: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, name=v)]}, bat_buoc=(v,), expect=0)),
    "canh_bao": ("K26", (_KG_T, "".join(sorted(_KG_T)), _KG_T2_KHONG_CHUAN), (_KG_T, _KG_T2_KHONG_CHUAN),
                 lambda p, t: dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, name=t), _kg_run(2, name=p, suite=9)]},
                                   bat_buoc=(t,), expect=0, canh_bao=()),
                 lambda v: dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, name=v), _kg_run(2, name=v, suite=9)]},
                                bat_buoc=(v,), expect=0, canh_bao=(f"CẢNH BÁO: '{v}' có 1 run ở suite khác (2) — bỏ qua",))),
}
_KG_T2_SO = {"status": _kg_t2_so('r["status"]', '"completed"'), "conclusion": _kg_t2_so('r["conclusion"]', '"success"'),
             "head": _kg_t2_so('r["head_sha"]', "a.head"), "ten": {**_kg_t2_so('r["name"]', "ten"), "duoi": "]"},
             "canh_bao": _kg_t2_so('r["name"]', "ten_cb")}


def _kg_dt_loi(a, b, k):   # lý do NGUYÊN VĂN của chốt danh tính: hai tuple, vế `k` khác nhau
    ta, tb = ["gate", _KG_SUITE, _KG_HEAD], ["gate", _KG_SUITE, _KG_HEAD]
    ta[k], tb[k] = a, b
    return f"id 1 mang hai danh tính {tuple(ta)!r} và {tuple(tb)!r}"


for _vt, _k in (("dt_ten", 0), ("dt_head", 2)):
    _f = "name" if _k == 0 else "head"
    # Đích nghiêm gồm `_KG_HEAD` cho head (biên `a`/`b` của #822 lượt 6) lẫn tên có dấu; cặp xung đột theo HAI thứ tự.
    _KG_T2_VI_TRI[_vt] = ("K16" if _k == 0 else "K18", (_KG_T, _KG_T2_KHONG_CHUAN, *((_KG_HEAD,) if _k == 2 else ())),
                          (_KG_T2_KHONG_CHUAN,),
                          (lambda a, b, f=_f, k=_k: dict(du_lieu={"total_count": 2, "check_runs": [
                              _kg_run(1, **{f: a}), _kg_run(1, **{f: b}), _kg_run(2)]}, chua=_kg_dt_loi(a, b, k))),
                          (lambda v, f=_f: dict(du_lieu={"total_count": 2, "check_runs": [
                              _kg_run(1, **{f: v}), _kg_run(1, **{f: v}), _kg_run(2)]}, expect=0)))
_KG_T2_VI_TRI["dedup"] = ("K25", (_KG_T, _KG_T2_KHONG_CHUAN), (), lambda a, b: dict(
    du_lieu={"total_count": 2, "check_runs": [_kg_run(1, name=a), _kg_run(2, name=b, conclusion="cancelled")]},
    bat_buoc=(a, b), chua="1/2 tên bắt buộc đỏ"), None)


def _kg_t2_sua(vi_tri, x, y):
    """Bản sửa (T6) của mục nghiêm (x, y) theo đúng thứ tự `nghiem` nhận: chỉ giá trị gần đúng đổi về giá trị đúng."""
    if vi_tri == "canh_bao":
        return None   # mục nghiêm của cảnh báo vốn XANH (đòi 0 dòng), không phải fixture từ chối
    if vi_tri == "dedup":
        return dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, name=x), _kg_run(2, name=y)]}, bat_buoc=(x, y), expect=0)
    return _KG_T2_VI_TRI[vi_tri][4](x if vi_tri in ("dt_ten", "dt_head") else y)


def _kg_t2_khop(vi_tri, toan_tu, phia, hoac=False):
    """Hàm Python cùng nghĩa với ĐỘT BIẾN của ô: (x, y) ⇒ đột biến coi hai giá trị là KHỚP. Ở `dt_*` x là bản ghi
    LƯU TRƯỚC, y là bản ghi tới sau; ở `dedup` x là tên SAU, y là tên TRƯỚC. `hoac`: hiện thực GIỮ phép bằng nguyên văn
    rồi nới thêm (`x == y or ...`) — không thể bị giết bằng chiều THA, chỉ bằng chiều NGHIÊM."""
    if toan_tu in _KG_T2_HUONG:
        k = _KG_T2_HUONG[toan_tu][1]
    else:
        g = _KG_T2_F[toan_tu][1] if toan_tu in _KG_T2_F else (lambda s, i=int(toan_tu[3:]): s[:i] + s[i + 1:])
        k = lambda x, y: _KG_T2_PHIA[phia][1](g, x, y)
    return (lambda x, y: x == y or k(x, y)) if hoac else k


def _kg_t2_muc_giet(vi_tri, toan_tu, phia, hoac=False):
    """Các mục giết ô này, TÍNH bằng hàm cùng nghĩa: nghiêm (p ≠ t mà đột biến coi là khớp) + tha (v = v mà đột biến
    coi là lệch). Rỗng ⇒ ô phải được khai `tuong_duong` (assert ở bộ sinh)."""
    _, dich, tha, nghiem, dung_tha = _KG_T2_VI_TRI[vi_tri]
    khop, ra = _kg_t2_khop(vi_tri, toan_tu, phia, hoac), []
    for t in dich:
        for nhan, p in _kg_bien_the(t).items():
            cap = ((p, t), (t, p)) if vi_tri in ("dt_ten", "dt_head", "dedup") else ((p, t),)
            for x, y in cap:
                if khop(x, y):
                    a, b = (x, y) if vi_tri in ("dt_ten", "dt_head") else (y, x) if vi_tri == "dedup" else (p, t)
                    ra.append((f"nghiem_{nhan}_{x == p}", (nghiem(a, b), _kg_t2_sua(vi_tri, a, b))))
    ra += [(f"tha_{i}", (dung_tha(v), None)) for i, v in enumerate(tha) if not khop(v, v)]
    return ra


def _kg_t2_ma(vi_tri, toan_tu, phia):   # (tìm, thay) của ô
    if vi_tri in ("dt_ten", "dt_head"):
        k = 0 if vi_tri == "dt_ten" else 2
        x = 'r["name"]' if k == 0 else 'r["head_sha"]'
        dong, so = _KG_DT_DONG, '        if danh_tinh.setdefault(r["id"], dt) != dt:\n'
        doi = lambda e, f: "(" + ", ".join(f.format(f"{e}[{i}]") if i == k else f"{e}[{i}]" for i in range(3)) + ")"
        if toan_tu in _KG_T2_HUONG:
            m = _KG_T2_HUONG[toan_tu][0].format(x=f"o[{k}]", y=f"dt[{k}]")
            return so, (f"        if not (lambda o: {m} and o[:{k}] + o[{k + 1}:] == dt[:{k}] + dt[{k + 1}:])"
                        '(danh_tinh.setdefault(r["id"], dt)):\n')
        f = _KG_T2_F[toan_tu][0]
        if phia == "hai_phia":
            return dong, dong.replace(x, f.format(x), 1)
        if phia == "trai":
            return so, f'        if (lambda o: {doi("o", f)})(danh_tinh.setdefault(r["id"], dt)) != dt:\n'
        return so, f'        if danh_tinh.setdefault(r["id"], dt) != {doi("dt", f)}:\n'
    if vi_tri == "dedup":
        tim = "ten_bb = list(dict.fromkeys(a.bat_buoc))"
        if toan_tu in _KG_T2_HUONG or phia != "hai_phia":   # MỘT phía: so cặp (tên sau t, tên trước u)
            m = (_KG_T2_HUONG[toan_tu][0].format(x="t", y="u") if toan_tu in _KG_T2_HUONG
                 else _KG_T2_PHIA[phia][0](_KG_T2_F[toan_tu][0], "t", "u"))
            return tim, f"ten_bb = [t for i, t in enumerate(a.bat_buoc) if not any({m} for u in a.bat_buoc[:i])]"
        return tim, "ten_bb = list({" + _KG_T2_F[toan_tu][0].format("t") + ": t for t in a.bat_buoc}.values())"
    so = _KG_T2_SO[vi_tri]
    duoi = so.get("duoi", "")
    if toan_tu in _KG_T2_HUONG:
        return so["mau"] + duoi, _KG_T2_HUONG[toan_tu][0].format(x=so["x"], y=so["y"]) + duoi
    return so["mau"] + duoi, _KG_T2_PHIA[phia][0](_KG_T2_F[toan_tu][0], so["x"], so["y"]) + duoi


def _kg_t2_ma_hoac(vi_tri, toan_tu, phia):   # (tìm, thay) của hiện thực `x == y or <một phía>` (ô trai/phai)
    f = _KG_T2_F[toan_tu][0]
    if vi_tri in ("dt_ten", "dt_head"):
        k = 0 if vi_tri == "dt_ten" else 2
        doi = lambda e: "(" + ", ".join(f.format(f"{e}[{i}]") if i == k else f"{e}[{i}]" for i in range(3)) + ")"
        nho = f"{doi('o')} != dt" if phia == "trai" else f"o != {doi('dt')}"
        return ('        if danh_tinh.setdefault(r["id"], dt) != dt:\n',
                f'        if (lambda o: o != dt and {nho})(danh_tinh.setdefault(r["id"], dt)):\n')
    if vi_tri == "dedup":
        m = _KG_T2_PHIA[phia][0](f, "t", "u")
        return ("ten_bb = list(dict.fromkeys(a.bat_buoc))",
                f"ten_bb = [t for i, t in enumerate(a.bat_buoc) if not any(t == u or {m} for u in a.bat_buoc[:i])]")
    so = _KG_T2_SO[vi_tri]
    duoi = so.get("duoi", "")
    return so["mau"] + duoi, f'({so["mau"]} or {_KG_T2_PHIA[phia][0](f, so["x"], so["y"])})' + duoi


# Ô T2 ĐÃ BIẾT tương đương — bộ sinh ĐÒI tập ô không giết được (tính bằng hàm cùng nghĩa) BẰNG ĐÚNG tập này.
_KG_T2_BAT_BIEN = ("casefold", "strip", "lstrip", "rstrip", "nfc", "nfkc")
_KG_T2_TUONG_DUONG = {
    **{(v, f, "phai"): f"vế phải là {'hằng ' + repr(h) if h else '`a.head`, đã qua `SHA_RE` ([0-9a-f]{40})'}, bất biến "
       f"dưới {f} — `kg_t_bo_de` đo" for v, h in (("status", "completed"), ("conclusion", "success"), ("head", ""))
       for f in _KG_T2_BAT_BIEN},
    **{(v, "nfc", p): "không chuỗi p ≠ vế phải nào có NFC(p) bằng nó: vế phải chỉ gồm ký tự ASCII [0-9a-f] hoặc chữ của "
       "`completed`/`success`, và không code point ngoài tập ấy có NFD nằm trọn trong tập — `kg_t_bo_de` đo cả 0x110000"
       for v in ("status", "conclusion", "head") for p in ("hai_phia", "trai")},
}
# Ô mà RIÊNG hiện thực `x == y or <một phía>` tương đương (bộ sinh đòi BẰNG ĐÚNG tập tính ra; `kg_t_bo_de` đo bổ đề).
_KG_T2_TUONG_DUONG_HOAC = {(v, "sap_xep", "trai"): f"hằng {h!r} CHƯA được sắp xếp nên không x nào có sorted(x) bằng nó: vế "
                           "`or` không bao giờ đúng, còn lại đúng phép bằng gốc" for v, h in (("status", "completed"), ("conclusion", "success"))}
_KG_T2_CA = {}
for _vt in _KG_T2_VI_TRI:
    for _tt in (*_KG_T2_F, *_KG_T2_HUONG):
        for _ph in ((None,) if _tt in _KG_T2_HUONG else _KG_T2_PHIA):
            _o = (_vt, _tt, _ph or "huong")
            _giet = _kg_t2_muc_giet(_vt, _tt, _ph)
            if not _giet:
                assert _o in _KG_T2_TUONG_DUONG, f"T2 {_o}: không fixture nào giết mà chưa khai tương đương"
                _kg_khong("T2", _vt, f"{_tt}:{_ph or 'huong'}", "tuong_duong", _KG_T2_TUONG_DUONG[_o])
                if _ph in ("trai", "phai"):   # `x == y or <tương đương của x == y>` vẫn là x == y
                    assert not _kg_t2_muc_giet(_vt, _tt, _ph, hoac=True), _o
                    _kg_khong("T2", _vt, f"{_tt}:{_ph}:hoac", "tuong_duong", _KG_T2_TUONG_DUONG[_o])
                continue
            assert _o not in _KG_T2_TUONG_DUONG, f"T2 {_o}: khai tương đương mà fixture {_giet[0][0]} giết được"
            _ca = f"kg_t2_{_vt}_{_tt}"
            _KG_T2_CA.setdefault(_ca, {}).update(dict(_giet[:1] + _giet[-1:]))   # đủ để giết ô; họ đầy đủ ở ca `_ho`
            _kg_o("T2", _vt, f"{_tt}:{_ph or 'huong'}", _KG_T2_VI_TRI[_vt][0], f"{_ca}_{_ph or 'huong'}",
                  *_kg_t2_ma(_vt, _tt, _ph), _ca)
            if _ph in ("trai", "phai"):   # hiện thực thứ hai của CÙNG ô: giữ phép bằng nguyên văn rồi nới một phía
                _giet = _kg_t2_muc_giet(_vt, _tt, _ph, hoac=True)
                if not _giet:
                    assert _o in _KG_T2_TUONG_DUONG_HOAC, f"T2 {_o}: hiện thực `hoặc` không fixture nào giết mà chưa khai tương đương"
                    _kg_khong("T2", _vt, f"{_tt}:{_ph}:hoac", "tuong_duong", _KG_T2_TUONG_DUONG_HOAC[_o])
                    continue
                assert _o not in _KG_T2_TUONG_DUONG_HOAC, f"T2 {_o}: khai tương đương mà `hoặc` giết được"
                _KG_T2_CA[_ca].update(dict(_giet[:1]))
                _kg_o("T2", _vt, f"{_tt}:{_ph}:hoac", _KG_T2_VI_TRI[_vt][0], f"{_ca}_{_ph}_hoac", *_kg_t2_ma_hoac(_vt, _tt, _ph), _ca)
_KG_T2_CA = {k: (lambda d=d: [(n, kw, sua) for n, (kw, sua) in d.items()]) for k, d in _KG_T2_CA.items()}


def _kg_t2_ho(vi_tri):   # HỌ ĐẦY ĐỦ của một vị trí (mọi biến thể × mọi đích × hai thứ tự + tha), giết cả đột biến ngoài bảng
    _, dich, tha, nghiem, dung_tha = _KG_T2_VI_TRI[vi_tri]
    for t in dich:
        for nhan, p in _kg_bien_the(t).items():
            if vi_tri in ("dt_ten", "dt_head", "dedup"):
                yield f"{nhan}_truoc", nghiem(p, t), _kg_t2_sua(vi_tri, p, t)
                yield f"{nhan}_sau", nghiem(t, p), _kg_t2_sua(vi_tri, t, p)
            else:
                yield nhan, nghiem(p, t), _kg_t2_sua(vi_tri, p, t)
    for i, v in enumerate(tha):
        yield f"tha_{i}", dung_tha(v), None


_KG_T2_CA.update({f"kg_t2_{v}_ho": (lambda v=v: _kg_t2_ho(v)) for v in _KG_T2_VI_TRI})


def _kg_t2_phu_loi(vi_tri, bien_the=None) -> list:
    """Ô nào của vị trí KHÔNG có mục giết trong HỌ ĐẦY ĐỦ, tính bằng hàm cùng nghĩa: toán tử của bảng + "bỏ ký tự ở chỉ số i"
    cho MỌI chỉ số giữa của mọi đích, × phía × (thuần | `hoặc`). Thiếu mà không nằm trong tập tương đương đã khai ⇒ lỗi.
    `bien_the` là ĐỐI SỐ để ca tự kiểm cho nó một họ biết trước là thiếu."""
    _, dich, tha, _, _ = _KG_T2_VI_TRI[vi_tri]
    bt = bien_the or _kg_bien_the
    cap = [(p, t) for t in dich for p in bt(t).values()]
    cap += [(t, p) for p, t in cap] if vi_tri in ("dt_ten", "dt_head", "dedup") else []
    cap += [(v, v) for v in tha]
    toan_tu = [*_KG_T2_F, *_KG_T2_HUONG, *sorted({f"bo_{i}" for t in dich for i in range(1, len(t) - 1)})]
    loi = []
    for tt in toan_tu:
        for ph in ((None,) if tt in _KG_T2_HUONG else ("hai_phia", "trai", "phai")):
            for hoac in ((False, True) if ph in ("trai", "phai") else (False,)):
                khop = _kg_t2_khop(vi_tri, tt, ph, hoac)
                if any((x != y and khop(x, y)) or (x == y and not khop(x, y)) for x, y in cap):
                    continue
                if (vi_tri, tt, ph or "huong") not in (_KG_T2_TUONG_DUONG_HOAC if hoac else {}) | _KG_T2_TUONG_DUONG:
                    loi.append(f"{vi_tri}/{tt}/{ph}/{'hoac' if hoac else 'thuan'}")
    return loi


def case_kg_t2_phu(c: Ctx):
    loi = [x for v in _KG_T2_VI_TRI for x in _kg_t2_phu_loi(v)]
    # Biết trước đáp án: họ chỉ đổi ký tự ở chỉ số TRUNG TÂM thì "bỏ ký tự ở chỉ số 1" của `completed` PHẢI bị tố.
    gia = _kg_t2_phu_loi("status", lambda v: {"giua": v[:len(v) // 2] + "x" + v[len(v) // 2 + 1:]})
    # Họ RỖNG, chỉ còn chiều tha: một phía THUẦN bị tha giết, hiện thực `hoặc` (giữ phép bằng) thì không ⇒ phải tố riêng nó.
    gia2 = _kg_t2_phu_loi("ten", lambda v: {})
    if loi or "status/bo_1/hai_phia/thuan" not in gia or "ten/casefold/trai/hoac" not in gia2 or "ten/casefold/trai/thuan" in gia2:
        raise AssertionError(f"T2 thiếu mục giết: {loi[:8]} ({len(loi)}) · tự kiểm tố {len(gia)} / {gia2[:4]}")


CASES.append(("kg_t2_phu", case_kg_t2_phu))

# --- T3: so số nguyên lỏng. Cặp phân biệt: 2^53 / 2^53+1 (float), âm/dương (abs), 9/10 (thứ tự chữ ≠ số), 12/13 (tiền tố).
_KG_T3_OP = {"float": ("float({})", "float"), "abs": ("abs({})", "abs"), "str": ("str({})", "str"),
             "tien_to": ("str({})[:1]", "lambda x: str(x)[:1]")}
_KG_T3_CAP = ((2 ** 53, 2 ** 53 + 1), (-5, 5), (9, 10), (12, 13), (1, 12), (-12, -1))   # 1/12, -12/-1: tiền tố THẬT
_KG_CB_DONG = lambda ids: f"CẢNH BÁO: 'gate' có {len(ids)} run ở suite khác ({', '.join(map(str, ids))}) — bỏ qua"


def _kg_t3_muc(vi_tri):
    xanh = lambda i: f"gate XANH trên {_KG_HEAD} (suite 1): gate id={i}"
    for lo, hi in _KG_T3_CAP:
        for a, b in ((lo, hi), (hi, lo)):
            n = f"{a}_{b}"
            if vi_tri == "dt_suite":
                yield n, dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, suite=a), _kg_run(1, suite=b), _kg_run(2)]},
                              chua=f"id 1 mang hai danh tính {('gate', a, _KG_HEAD)!r} và {('gate', b, _KG_HEAD)!r}"), \
                    dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, suite=a), _kg_run(1, suite=a), _kg_run(2)]}, expect=0)
            elif vi_tri == "suite_neo" and a > 0:
                yield n, dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, suite=a, conclusion="failure"),
                                                                        _kg_run(2, suite=b)]}, suite=a, chua="conclusion='failure'"), \
                    dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, suite=a), _kg_run(2, suite=b)]}, suite=a, expect=0)
            elif vi_tri == "suite_canh_bao" and a > 0:
                yield n, dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1, suite=a), _kg_run(2, suite=b)]}, suite=a,
                              expect=0, canh_bao=(_KG_CB_DONG([2]),)), None
            elif vi_tri == "id_danh_tinh":
                yield n, dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(a), _kg_run(b, name="gate2")]},
                              bat_buoc=("gate", "gate2"), expect=0), None
            elif vi_tri == "id_dem":
                yield n, dict(du_lieu={"total_count": 3, "check_runs": [_kg_run(a, name="khac"), _kg_run(b, name="khac"),
                                                                        _kg_run(10 ** 6)]}, expect=0), None
            elif vi_tri in ("id_max", "id_loc_max"):   # bản id NHỎ hơn (theo SỐ) đỏ, bản lớn xanh
                nho, lon = sorted((a, b))
                ds = [_kg_run(nho, conclusion="cancelled"), _kg_run(lon)]
                yield n, dict(du_lieu={"total_count": 2, "check_runs": ds if a == nho else ds[::-1]}, expect=0,
                              dong_xanh=xanh(lon)), None
            elif vi_tri == "id_canh_bao":
                yield n, dict(du_lieu={"total_count": 3, "check_runs": [_kg_run(10 ** 6), _kg_run(a, suite=9), _kg_run(b, suite=9)]},
                              expect=0, canh_bao=(_KG_CB_DONG(sorted((a, b))),)), None
    if vi_tri == "suite_neo":   # miền: `check_suite.id` trong JSON là MỌI int (CLI chỉ đòi `--check-suite` dương)
        for sid in (0, -1, -(2 ** 53 + 1), 2 ** 53 + 1, 10 ** 40 + 1):
            yield f"mien_{sid}", dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(1), _kg_run(2, name="khac", suite=sid)]},
                                      expect=0), None


_KG_T3_VI_TRI = {   # vị trí → (hàng K, tìm, mẫu thay theo toán tử)
    "dt_suite": ("K17", _KG_DT_DONG, lambda f, k: _KG_DT_DONG.replace('r["check_suite"]["id"]', f.format('r["check_suite"]["id"]'))),
    "suite_neo": ("K28", 'r["check_suite"]["id"] == suite]',
                  lambda f, k: f.format('r["check_suite"]["id"]') + " == (" + f.format("suite") + " if isinstance(suite, int) else suite)]"),
    "suite_canh_bao": ("K26", 'r["check_suite"]["id"] != suite})',
                       lambda f, k: f.format('r["check_suite"]["id"]') + " != (" + f.format("suite") + " if isinstance(suite, int) else suite)})"),
    "id_danh_tinh": ("K16", ('danh_tinh.setdefault(r["id"], dt)', "danh_tinh[r['id']]"),
                     lambda f, k: ("danh_tinh.setdefault(" + f.format('r["id"]') + ", dt)", "danh_tinh[" + f.format("r['id']") + "]")),
    "id_dem": ("K20", 'so_id = len({r["id"] for r in runs})', lambda f, k: "so_id = len({" + f.format('r["id"]') + " for r in runs})"),
    "id_max": ("K30", 'id_max = max(r["id"] for r in cung)', lambda f, k: f'id_max = max((r["id"] for r in cung), key={k})'),
    "id_canh_bao": ("K26", _KG_CB, lambda f, k: "khac = sorted({" + f.format('r["id"]') + ': r["id"] for r in runs if r["name"] == ten_cb '
                    'and r["check_suite"]["id"] != suite}.values(), key=' + k + ")"),
    "id_loc_max": ("K31", 'if r["id"] == id_max)', lambda f, k: "if " + f.format('r["id"]') + " == " + f.format("id_max") + ")"),
}
_KG_T3_TUONG_DUONG = {
    "suite_neo": "`str` là đơn ánh trên int nên str(a) == str(b) ⇔ a == b; `suite` là CHUỖI chỉ ở F02 (> trần chữ số `int()`), "
                 "mà `json` không đọc nổi int dài thế nên không run nào mang chuỗi ấy",
    "suite_canh_bao": "như `suite_neo`: đơn ánh, cùng tập run bị bỏ, cùng dòng cảnh báo",
    "id_danh_tinh": "đơn ánh ⇒ cùng tập khoá; lý do in `r['id']` gốc và `danh_tinh[str(id)]` trả CÙNG tuple đã lưu",
    "id_dem": "đơn ánh ⇒ `len` của tập không đổi; lý do in `so_id`, cùng số",
    "id_loc_max": "đơn ánh ⇒ cùng tập bản ghi mang id lớn nhất",
}
_KG_T3_CA = {f"kg_t3_{v}": (lambda v=v: _kg_t3_muc(v)) for v in _KG_T3_VI_TRI}
for _vt, (_hang, _tim, _thay) in _KG_T3_VI_TRI.items():
    for _tt, (_f, _key) in _KG_T3_OP.items():
        if _tt == "str" and _vt in _KG_T3_TUONG_DUONG:
            _kg_khong("T3", _vt, _tt, "tuong_duong", _KG_T3_TUONG_DUONG[_vt])
            continue
        _kg_o("T3", _vt, _tt, _hang, f"kg_t3_{_vt}_{_tt}", _tim, _thay(_f, _key), f"kg_t3_{_vt}")
# Tiền tố ĐẦY ĐỦ (`str(x).startswith(str(y))`, hai hướng) — `str(x)[:1]` chỉ là một chiếu của nó (#856 lượt 1). x là bản
# ghi/run/id ĐANG xét, y là thứ nó được so với (bản đã lưu, suite neo, id lớn nhất, id đứng trước).
_KG_DT_SO = '        if danh_tinh.setdefault(r["id"], dt) != dt:\n'
_KG_GOP_TT = "(lambda u: [i for n, i in enumerate(u) if not any({m} for j in u[:n])])"
_KG_T3_TIEN_TO = {   # vị trí → (tìm, mẫu thay với {m}, (x, y) của hướng xy)
    "dt_suite": (_KG_DT_SO, '        if not (lambda o: {m} and o[0] == dt[0] and o[2] == dt[2])(danh_tinh.setdefault(r["id"], dt)):\n',
                 ("o[1]", "dt[1]")),
    "suite_neo": ('r["check_suite"]["id"] == suite]', "{m}]", ('r["check_suite"]["id"]', "suite")),
    "suite_canh_bao": ('r["check_suite"]["id"] != suite})', "not {m}})", ('r["check_suite"]["id"]', "suite")),
    "id_danh_tinh": ((_KG_DT_SO, "danh_tinh[r['id']]"),
                     ('        _k = next((k for k in danh_tinh if {m}), r["id"])\n        if danh_tinh.setdefault(_k, dt) != dt:\n',
                      "danh_tinh[_k]"), ('r["id"]', "k")),
    "id_dem": ('so_id = len({r["id"] for r in runs})', "so_id = len(" + _KG_GOP_TT + '(list(dict.fromkeys(r["id"] for r in runs))))',
               ("i", "j")),
    "id_canh_bao": (_KG_CB, "khac = " + _KG_GOP_TT + "(" + _KG_CB[len("khac = "):] + ")", ("i", "j")),
    "id_loc_max": ('if r["id"] == id_max)', "if {m})", ('r["id"]', "id_max")),
}
for _vt, (_tim, _thay, (_x, _y)) in _KG_T3_TIEN_TO.items():
    for _h, (_a, _b) in (("xy", (_x, _y)), ("yx", (_y, _x))):
        _m = f"str({_a}).startswith(str({_b}))"
        _th = tuple(t.replace("{m}", _m) for t in _thay) if isinstance(_thay, tuple) else _thay.replace("{m}", _m)
        _kg_o("T3", _vt, f"bat_dau_{_h}", _KG_T3_VI_TRI[_vt][0], f"kg_t3_{_vt}_bat_dau_{_h}", _tim, _th, f"kg_t3_{_vt}")
for _h, (_x, _y) in (("xy", ("x", "y")), ("yx", ("y", "x"))):   # #856 lượt 2: `max` nhận bộ so bất kỳ qua `cmp_to_key`
    _kg_o("T3", "id_max", f"bat_dau_{_h}", "K30", f"kg_t3_id_max_bat_dau_{_h}", 'id_max = max(r["id"] for r in cung)',
          'id_max = max((r["id"] for r in cung), key=__import__("functools").cmp_to_key('
          f'lambda x, y: 0 if str({_x}).startswith(str({_y})) else (x > y) - (x < y)))', "kg_t3_id_max")

# --- T5: dạng đối số. Run trùng NGUYÊN VĂN đối số sai, nên chỉ chốt đối số quyết định màu.
_KG_T5_HEAD = _KG_HEAD_SO
_kg_thay_kt = lambda s, i, k: s[:i] + k + s[i + 1:]


def _kg_t5_muc(vi_tri):
    if vi_tri == "head":
        h = _KG_T5_HEAD
        bt = {"dem_trai": " " + h, "dem_phai": h + " ", "tab_trai": "\t" + h, "tab_phai": h + "\t",
              **{f"rong_{i}": _kg_thay_kt(h, i, chr(ord(h[i]) + 0xFEE0)) for i in (0, 20, 39)},
              **{f"arap_{i}": _kg_thay_kt(h, i, "\u0661") for i in (0, 20, 39)},
              **{f"hoa_{i}": _kg_thay_kt(h, i, "A") for i in (10, 20, 39)},
              "g_giua": _kg_thay_kt(h, 20, "g"), "cach_giua": _kg_thay_kt(h, 20, " ")}
        for n, x in bt.items():
            assert x != h
            yield n, dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, head=x)]}, head=x, expect=2, chua="SHA 40"), \
                dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, head=h)]}, head=h, expect=0)
    elif vi_tri == "suite":
        bt = {"dem_trai": " 111", "dem_phai": "111 ", "tab_trai": "\t111", "tab_phai": "111\t",
              **{f"{n}_{i}": _kg_thay_kt("111", i, k) for n, k in (("rong", "\uff11"), ("arap", "\u0661"), ("cach", " "),
                                                                   ("hoa", "A")) for i in range(3)}}
        for n, x in bt.items():   # neo JSON ở 111 = int(...) của mọi biến thể parse được; còn lại đột biến ra VẮNG rc 12 ≠ 2
            yield n, dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, suite=111)]}, suite=x, expect=2, chua=_KG_ARG), \
                dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, suite=111)]}, suite="111", expect=0)
    else:
        for n, x in (("lf_cuoi", "gate\n"), ("lf_dau", "\ngate"), ("lf_giua", "ga\nte"), ("ls_giua", "ga\u2028te"),
                     ("cr_cuoi", "gate\r"), ("cach", " "), ("rong", "")):
            yield n, dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, name=x)]}, bat_buoc=(x,), expect=2, chua="--bat-buoc"), \
                dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, name="gate")]}, bat_buoc=("gate",), expect=0)
        # Chiều THA: tên KHÔNG chuẩn hợp lệ, run trùng nguyên văn ⇒ chuẩn hoá đối số rồi dùng tiếp làm vỡ phép khớp.
        v = _KG_T2_KHONG_CHUAN
        yield "tha_khong_chuan", dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1, name=v)]}, bat_buoc=(v,), expect=0), None


_KG_T5_CA = {f"kg_t5_{v}": (lambda v=v: _kg_t5_muc(v)) for v in ("head", "suite", "bat_buoc")}
_KG_T5_CHUAN = {"strip": "{}.strip()", "lstrip": "{}.lstrip()", "rstrip": "{}.rstrip()", "nfkc": _KG_NFC.replace("NFC", "NFKC")}
_KG_HAI_DAU = '{0}[:1] + "0" * max(len({0}) - 2, 0) + {0}[1:][-1:]'
_KG_BB = "    if any(not t.strip() or t.splitlines() != [t] for t in ten_bb):\n"
for _tt, _f in _KG_T5_CHUAN.items():
    _kg_o("T5", "head", f"chuan_hoa_{_tt}:dong_chay", "K21", f"kg_t5_head_{_tt}_dong_chay", "    if not SHA_RE.fullmatch(a.head):\n",
          f"    a.head = {_f.format('a.head')}\n    if not SHA_RE.fullmatch(a.head):\n", "kg_t5_head")
    _kg_o("T5", "suite", f"chuan_hoa_{_tt}:dong_chay", "K22", f"kg_t5_suite_{_tt}_dong_chay",
          '    if not re.fullmatch(r"[1-9][0-9]*", a.check_suite):\n',
          f'    a.check_suite = {_f.format("a.check_suite")}\n    if not re.fullmatch(r"[1-9][0-9]*", a.check_suite):\n', "kg_t5_suite")
    _kg_o("T5", "bat_buoc", f"chuan_hoa_{_tt}:dong_chay", "K24", f"kg_t5_bat_buoc_{_tt}_dong_chay",
          "ten_bb = list(dict.fromkeys(a.bat_buoc))", f"ten_bb = list(dict.fromkeys({_f.format('t')} for t in a.bat_buoc))",
          "kg_t5_bat_buoc")
    _kg_o("T5", "head", f"chuan_hoa_{_tt}:chi_kiem", "K21", f"kg_t5_head_{_tt}", "SHA_RE.fullmatch(a.head)",
          f"SHA_RE.fullmatch({_f.format('a.head')})", "kg_t5_head")
    _kg_o("T5", "suite", f"chuan_hoa_{_tt}:chi_kiem", "K22", f"kg_t5_suite_{_tt}", 're.fullmatch(r"[1-9][0-9]*", a.check_suite)',
          f're.fullmatch(r"[1-9][0-9]*", {_f.format("a.check_suite")})', "kg_t5_suite")
    if _tt == "nfkc":
        _kg_khong("T5", "bat_buoc", "chuan_hoa_nfkc:chi_kiem", "tuong_duong",
                  "NFKC giữ nguyên mọi ký tự ngắt dòng, đưa khoảng trắng về khoảng trắng, không đưa ký tự khác về khoảng trắng/"
                  "ngắt dòng/rỗng (`kg_t_bo_de` đo cả 0x110000); không cặp ghép nào tạo/xoá ký tự trắng hay ngắt dòng, nên "
                  "`not u.strip() or u.splitlines() != [u]` cùng giá trị trên t và NFKC(t), và ở hiện thực CHỈ-KIỂM này chỉ giá "
                  "trị bool ấy được dùng (hiện thực DÒNG CHẢY là ô `chuan_hoa_nfkc:dong_chay`, có đột biến riêng)")
        continue
    _kg_o("T5", "bat_buoc", f"chuan_hoa_{_tt}:chi_kiem", "K24", f"kg_t5_bat_buoc_{_tt}", _KG_BB,
          "    if any(not {0}.strip() or {0}.splitlines() != [{0}] for t in ten_bb):\n".format(_f.format("t")), "kg_t5_bat_buoc")
_kg_o("T5", "head", "hai_dau", "K21", "kg_t5_head_hai_dau", "SHA_RE.fullmatch(a.head)",
      f"SHA_RE.fullmatch({_KG_HAI_DAU.format('a.head')})", "kg_t5_head")
_kg_o("T5", "suite", "hai_dau", "K22", "kg_t5_suite_hai_dau", 're.fullmatch(r"[1-9][0-9]*", a.check_suite)',
      f're.fullmatch(r"[1-9][0-9]*", {_KG_HAI_DAU.format("a.check_suite")})', "kg_t5_suite")
_kg_o("T5", "bat_buoc", "hai_dau", "K24", "kg_t5_bat_buoc_hai_dau", _KG_BB,
      "    if any((lambda u: not u.strip() or u.splitlines() != [u])(t[:1] + t[-1:]) for t in ten_bb):\n", "kg_t5_bat_buoc")
_KG_CHEO = chr(92)   # dựng dấu chéo ngược SAU khi phân tích cú pháp (bài học tầng vận chuyển, CLAUDE.md)
for _tt, _re in (("lop_d", f"[{_KG_CHEO}da-f]{{40}}"), ("lop_hoa", "[0-9a-fA-F]{40}")):
    _kg_o("T5", "head", _tt, "K21", f"kg_t5_head_{_tt}", "    if not SHA_RE.fullmatch(a.head):\n",
          f'    if not re.fullmatch(r"{_re}", a.head):\n', "kg_t5_head")
for _tt, _re in (("lop_d_dau", f"{_KG_CHEO}d[0-9]*"), ("lop_d_sau", f"[1-9]{_KG_CHEO}d*"), ("lop_hoa_dau", "[1-9A-Z][0-9]*"),
                 ("lop_hoa_sau", "[1-9][0-9A-Z]*")):
    _kg_o("T5", "suite", _tt, "K22", f"kg_t5_suite_{_tt}", 'r"[1-9][0-9]*"', f'r"{_re}"', "kg_t5_suite")
for _tt in ("lop_d", "lop_hoa"):
    _kg_khong("T5", "bat_buoc", _tt, "khong_ap_dung", "`--bat-buoc` không kiểm bằng regex, không có lớp ký tự để nới")

# --- T4: lượng từ / vị trí. NĂM phần tử để mọi lát cắt phân biệt được; điều kiện chặn đặt vi phạm ở đầu/giữa/cuối.
_KG_CAT_T4 = {"dau": "{}[:1]", "cuoi": "{}[-1:]", "bo_dau": "{}[1:]", "bo_cuoi": "{}[:-1]", "xen_ke": "{}[::2]",
              "hai_dau": "{0}[:1] + {0}[-1:]", "hai_dau_2": "{0}[:2] + {0}[-2:]"}
_KG_TEN5 = ("gate", "gate2", "gate3", "gate4", "gate5")
_KG_XANH5 = f"gate XANH trên {_KG_HEAD} (suite 1): " + " · ".join(f"{t} id={i + 1}" for i, t in enumerate(_KG_TEN5))


def _kg_t4_trang(chot):
    """Năm trang, trang k mang run id 40+k (`gate` ở trang 1). Vi phạm `chot` đặt ở trang 0 / 2 / 4."""
    def trang(n, vi_pham=None, p=None, sua=False):
        ra = []
        for k in range(5):
            tr = {"total_count": n, "check_runs": [_kg_run(40 + k, name="gate" if k == 1 else "khac")]}
            if k == p:
                tr = vi_pham(tr, sua)
            ra.append(tr)
        return ra
    if chot is None:   # lát cắt: năm trang hợp lệ
        yield "nam_trang", dict(du_lieu=trang(5), expect=0, dong_xanh=f"gate XANH trên {_KG_HEAD} (suite 1): gate id=41"), None
        return
    them = lambda tr, run: {**tr, "check_runs": tr["check_runs"] + [run]}
    bang = {   # chốt → (total_count, dựng vi phạm/bản sửa, lý do theo p)
        "trang": (4, lambda tr, s: {"total_count": 4, "check_runs": []} if s else None, lambda p: f"trang {p} {_KG_TRANG}"),
        "tc_vang": (5, lambda tr, s: tr if s else {"check_runs": tr["check_runs"]}, lambda p: f"trang {p} thiếu `total_count`"),
        "tc_kieu": (5, lambda tr, s: tr if s else {**tr, "total_count": "5"}, lambda p: f"trang {p}: `total_count`"),
        "tc_am": (5, lambda tr, s: tr if s else {**tr, "total_count": -1}, lambda p: f"trang {p}: `total_count`"),
        "run": (6, lambda tr, s: them(tr, _kg_khac(id=99) if s else 5), lambda p: f"trang {p} check_runs[1] không phải object"),
        "schema": (6, lambda tr, s: them(tr, _kg_khac(id=99, status="completed" if s else 5)),
                   lambda p: f"trang {p} check_runs[1] {_KG_TRUONG} ['status']"),
        "suite": (6, lambda tr, s: them(tr, _kg_khac(id=99, check_suite={"id": 1 if s else "5"})),
                  lambda p: f"trang {p} check_runs[1] {_KG_CS}")}
    n, vp, ly = bang[chot]
    for p in (0, 2, 4):
        yield f"trang_{p}", dict(du_lieu=trang(n, vp, p), chua=ly(p)), dict(du_lieu=trang(n, vp, p, True), expect=0)


def _kg_t4_run(chot):
    """MỘT trang năm run (`gate` id 51). Vi phạm `chot` ở run 0 / 2 / 4."""
    tot = [_kg_run(51), *(_kg_run(i, name="khac") for i in (52, 53, 54, 55))]
    if chot is None:
        yield "nam_run", dict(du_lieu={"total_count": 5, "check_runs": tot}, expect=0,
                              dong_xanh=f"gate XANH trên {_KG_HEAD} (suite 1): gate id=51"), None
        return
    hong, sua, ly = {"run": (5, _kg_khac(id=99), "không phải object"),
                     "schema": (_kg_khac(id=99, status=5), _kg_khac(id=99), f"{_KG_TRUONG} ['status']"),
                     "suite": (_kg_khac(id=99, check_suite={"id": "5"}), _kg_khac(id=99), _KG_CS)}[chot]
    for j in (0, 2, 4):
        lam = lambda x: {"total_count": 6, "check_runs": [*tot[:j], x, *tot[j:]]}
        yield f"run_{j}", dict(du_lieu=lam(hong), chua=f"trang 0 check_runs[{j}] {ly}"), dict(du_lieu=lam(sua), expect=0)


def _kg_t4_doi_so():   # cùng bộ dựng với `kg_r5_vi_tri` (ten_*): run cho MỌI tên, kể cả tên hỏng (#822 lượt 6)
    for nhan, kw in _kg_sinh_vi_tri():
        if nhan.startswith("ten_"):
            kw = {**kw, "dem": True}   # bộ sinh cũ để `total_count` cho `_kg_dem` điền
            yield nhan, kw, _kg_sua_ten(kw, kw["bat_buoc"][int(nhan.split("_")[1])], "gate9")


def _kg_t4_mau(loai):
    runs = lambda bo=None, do=None: [_kg_run(i + 1, name=t, conclusion="cancelled" if i == do else "success")
                                     for i, t in enumerate(_KG_TEN5) if i != bo]
    yield "xanh", dict(du_lieu={"total_count": 5, "check_runs": runs()}, bat_buoc=_KG_TEN5, expect=0, dong_xanh=_KG_XANH5), None
    for k in (0, 2, 4):
        if loai in (None, "vang"):
            yield f"vang_{k}", dict(du_lieu={"total_count": 4, "check_runs": runs(bo=k)}, bat_buoc=_KG_TEN5,
                                    chua=f"'{_KG_TEN5[k]}': VẮNG"), dict(du_lieu={"total_count": 5, "check_runs": runs()},
                                                                        bat_buoc=_KG_TEN5, expect=0)
        if loai == "do" and k == 0:   # NĂM tên đỏ: mọi dòng `ĐỎ` phải có, đúng thứ tự (lát cắt vòng in)
            do = [f"ĐỎ  '{t}' id={i + 1}: status='completed' conclusion='cancelled' head_sha='{_KG_HEAD}'"
                  for i, t in enumerate(_KG_TEN5)]
            yield "do_ca_nam", dict(du_lieu={"total_count": 5, "check_runs": [_kg_run(i + 1, name=t, conclusion="cancelled")
                                                                              for i, t in enumerate(_KG_TEN5)]},
                                    bat_buoc=_KG_TEN5, chua="\n  ".join(do) + "\n"), \
                dict(du_lieu={"total_count": 5, "check_runs": runs()}, bat_buoc=_KG_TEN5, expect=0)
        if loai in (None, "do"):
            yield f"do_{k}", dict(du_lieu={"total_count": 5, "check_runs": runs(do=k)}, bat_buoc=_KG_TEN5,
                                  chua=f"'{_KG_TEN5[k]}' id={k + 1}: status='completed' conclusion='cancelled'"), \
                dict(du_lieu={"total_count": 5, "check_runs": runs()}, bat_buoc=_KG_TEN5, expect=0)


def _kg_t4_canh_bao():
    ds = [_kg_run(i + 1, name=t) for i, t in enumerate(_KG_TEN5)] + [_kg_run(i + 11, name=t, suite=9) for i, t in enumerate(_KG_TEN5)]
    yield "nam_ten", dict(du_lieu={"total_count": 10, "check_runs": ds}, bat_buoc=_KG_TEN5, expect=0, canh_bao=tuple(
        f"CẢNH BÁO: '{t}' có 1 run ở suite khác ({i + 11}) — bỏ qua" for i, t in enumerate(_KG_TEN5))), None
    # MỘT tên, NĂM run ở suite khác: lát cắt trên `runs` của cảnh báo và trên danh sách id in ra đều phân biệt được.
    # Run suite khác đứng ĐẦU (mục trên để chúng cuối): cắt đầu lẫn cắt cuối `runs` đều rơi đúng một id cần in.
    yield "nam_id", dict(du_lieu={"total_count": 6, "check_runs": [_kg_run(20 + i, suite=9) for i in range(1, 6)] + [_kg_run(1)]},
                         expect=0, canh_bao=(_KG_CB_DONG(list(range(21, 26))),)), None


def _kg_t4_truong():   # NĂM trường kiểu của run, mỗi mục sai ĐÚNG một trường (lát cắt bảng `_TRUONG_CHECK_RUN`)
    for f, gt in (("id", "x"), ("name", 5), ("head_sha", 5), ("status", 5), ("conclusion", 5)):
        yield f, dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(11), _kg_khac(**{"id": 15, f: gt})]},
                      chua=f"trang 0 check_runs[1] {_KG_TRUONG} ['{f}']"), \
            dict(du_lieu={"total_count": 2, "check_runs": [_kg_run(11), _kg_khac(id=15)]}, expect=0)


def _kg_t4_max():   # NĂM bản ghi CÙNG tên, id khác nhau; bản id lớn nhất (xanh) đặt ở từng vị trí, các bản khác huỷ
    for p in range(5):
        ids = [1, 2, 3, 4]
        ids.insert(p, 5)
        yield f"max_{p}", dict(du_lieu={"total_count": 5, "check_runs": [_kg_run(i, conclusion="success" if i == 5 else "cancelled")
                                                                         for i in ids]},
                               expect=0, dong_xanh=f"gate XANH trên {_KG_HEAD} (suite 1): gate id=5"), None


def _kg_t4_dt():   # cặp xung đột (bản lưu a, bản lệch chèn ở b) như `_kg_sinh_vi_tri`; bản sửa = bản lặp NHẤT QUÁN
    tot = [_kg_run(9)] + [_kg_run(i, name="khac") for i in (1, 2, 3, 4)]
    for a, b in ((0, 5), (1, 2), (2, 3), (3, 4), (0, 1), (4, 5), (1, 4)):
        lam = lambda x: tot[:b - 1 if b > a else b] + [x] + tot[b - 1 if b > a else b:]
        yield f"danh_tinh_{a}_{b}", dict(du_lieu={"total_count": 5, "check_runs": lam(_kg_run(tot[a]["id"], name="khac", head="cd" * 20))},
                                         chua=_KG_DT), dict(du_lieu={"total_count": 5, "check_runs": lam(dict(tot[a]))}, expect=0)


def _kg_t4_id_max():
    for truong, gt in (("status", "in_progress"), ("conclusion", "cancelled")):
        for vt in range(5):
            yield f"{truong}_{vt}", dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(7, **({truong: gt} if i == vt else {}))
                                                                                    for i in range(5)]},
                                         chua=f"{truong}={gt!r}"), \
                dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(7) for _ in range(5)]}, expect=0)


def _kg_t4_khai():
    for p in range(5):
        ds = [{"total_count": 6 if k == p else 5, "check_runs": [_kg_run(60 + k, name="gate" if k == 0 else "khac")]}
              for k in range(5)]
        sua = [{**tr, "total_count": 5} for tr in ds]
        yield f"lech_{p}", dict(du_lieu=ds, chua="khác nhau"), dict(du_lieu=sua, expect=0)


_KG_T4_CA = {"kg_t4_trang_cat": lambda: _kg_t4_trang(None), "kg_t4_run_cat": lambda: _kg_t4_run(None),
             **{f"kg_t4_trang_{c}": (lambda c=c: _kg_t4_trang(c)) for c in ("trang", "tc_vang", "tc_kieu", "tc_am", "run", "schema", "suite")},
             **{f"kg_t4_run_{c}": (lambda c=c: _kg_t4_run(c)) for c in ("run", "schema", "suite")},
             "kg_t4_doi_so": _kg_t4_doi_so, "kg_t4_mau": lambda: _kg_t4_mau(None), "kg_t4_mau_vang": lambda: _kg_t4_mau("vang"),
             "kg_t4_mau_do": lambda: _kg_t4_mau("do"), "kg_t4_canh_bao": _kg_t4_canh_bao, "kg_t4_dt": _kg_t4_dt,
             "kg_t4_id_max": _kg_t4_id_max, "kg_t4_khai": _kg_t4_khai, "kg_t4_truong": _kg_t4_truong, "kg_t4_max": _kg_t4_max}
_KG_NHOM_MAX = '[x for x in cung if x["id"] == id_max]'
_KG_T4_VONG = {   # vòng → (hàng K, tìm, dạng thay chứa {S} cho tập đã cắt, ca đích lát cắt)
    "trang": ("K05", "    for i, tr in enumerate(trang):\n", "    for i, tr in enumerate({S}):\n", "trang", "kg_t4_trang_cat"),
    "run": ("K08", '        for j, r in enumerate(tr["check_runs"]):\n', "        for j, r in enumerate({S}):\n", 'tr["check_runs"]',
            "kg_t4_run_cat"),
    "ten_doi_so": ("K24", "t.splitlines() != [t] for t in ten_bb)", "t.splitlines() != [t] for t in {S})", "ten_bb", "kg_t4_doi_so"),
    "ten_mau": ("K35", "    for ten in ten_bb:\n", "    for ten in {S}:\n", "ten_bb", "kg_t4_mau"),
    "ten_canh_bao": ("K26", "    for ten_cb in ten_bb:\n", "    for ten_cb in {S}:\n", "ten_bb", "kg_t4_canh_bao"),
    "danh_tinh": ("K16", "    for r in runs:\n        dt =", "    for r in {S}:\n        dt =", "runs", "kg_t4_dt"),
    "id_max": ("K31", 'for r in (r for r in cung if r["id"] == id_max):', "for r in {S}:", _KG_NHOM_MAX, "kg_t4_id_max"),
    "khai": ("K19", "any(t != tong_khai for t in khai)", "any(t != tong_khai for t in {S})", "khai", "kg_t4_khai"),
    # #856 lượt 1: MỌI vòng lặp/comprehension của hai hàm (AST đếm 16, `kg_t_ma_tran` đối chiếu) + 3 phép duyệt NGẦM.
    "truong": ("K09", "for k, kieu in _TRUONG_CHECK_RUN if", "for k, kieu in {S} if", "_TRUONG_CHECK_RUN", "kg_t4_truong"),
    "id_dem": ("K20", 'so_id = len({r["id"] for r in runs})', 'so_id = len({r["id"] for r in {S}})', "runs", "kg_t4_run_cat"),
    "canh_bao_runs": ("K26", 'khac = sorted({r["id"] for r in runs if', 'khac = sorted({r["id"] for r in {S} if', "runs", "kg_t4_canh_bao"),
    "cung_ten": ("K27", 'cung = [r for r in runs if r["name"] == ten]', 'cung = [r for r in {S} if r["name"] == ten]', "runs", "kg_t4_mau"),
    "cung_suite": ("K28", 'cung = [r for r in cung if r["check_suite"]["id"] == suite]',
                   'cung = [r for r in {S} if r["check_suite"]["id"] == suite]', "cung", "kg_t4_id_max"),
    "max_cung": ("K30", 'id_max = max(r["id"] for r in cung)', 'id_max = max(r["id"] for r in {S})', "cung", "kg_t4_max"),
    "id_max_cung": ("K31", 'for r in (r for r in cung if r["id"] == id_max):', 'for r in (r for r in {S} if r["id"] == id_max):', "cung",
                    "kg_t4_id_max"),
    "dong_do": ("K39", "        for dong in do:\n", "        for dong in {S}:\n", "do", "kg_t4_mau_do"),
    "bat_buoc_khu": ("K25", "ten_bb = list(dict.fromkeys(a.bat_buoc))", "ten_bb = list(dict.fromkeys({S}))", "a.bat_buoc", "kg_t4_mau"),
    "xanh_join": ("K36", '" · ".join(xanh))', '" · ".join({S}))', "xanh", "kg_t4_mau"),
    "khac_join": ("K26", "', '.join(map(str, khac))", "', '.join(map(str, {S}))", "khac", "kg_t4_canh_bao"),
}
_KG_T4_NGAM = ("bat_buoc_khu", "xanh_join", "khac_join")   # duyệt tập qua hàm dựng sẵn, không có nút vòng lặp trong AST
for _vg, (_hang, _tim, _thay, _tap, _ca) in _KG_T4_VONG.items():
    for _tt, _cat in _KG_CAT_T4.items():
        if (_vg, _tt) == ("khai", "bo_dau"):
            _kg_khong("T4", _vg, f"cat_{_tt}", "tuong_duong", "`tong_khai` CHÍNH LÀ `khai[0]`, nên `t != tong_khai` luôn False ở phần "
                      "tử đầu: bỏ nó không đổi `any(...)`, và mọi dòng sau dùng `khai` nguyên vẹn")
            continue
        _kg_o("T4", _vg, f"cat_{_tt}", _hang, f"kg_t4_{_vg}_cat_{_tt}", _tim, _thay.replace("{S}", _cat.format(_tap)), _ca)
    _kg_khong("T4", _vg, "chi_khi_khac_rong", "tuong_duong",
              "thân vòng (hoặc biểu thức trong comprehension / hàm duyệt) chỉ chạy khi tập đang duyệt có phần tử, nên điều kiện "
              "\"tập khác rỗng\" luôn True ở mọi lần nó được xét; tập rỗng thì cả bản gốc lẫn đột biến đều không duyệt gì")
# Điều kiện chặn: phép kiểm trong vòng chỉ chạy ở phần tử ĐẦU / CUỐI / HAI ĐẦU. Hai dạng hiện thực, chọn dạng KHÔNG SẬP:
# "cho qua" (bỏ phép kiểm, phần tử đi tiếp) hoặc "bỏ qua" (bỏ cả phần tử) khi cho qua chắc chắn chạm khoá hỏng.
_KG_G = {"dau": "{0} == 0", "cuoi": "{0} == {1} - 1", "hai_dau": "({0} == 0 or {0} == {1} - 1)"}
_KG_T4_CHOT = {   # (vòng, chốt) → (hàng K, tìm, hàm G ↦ thay, ca đích)
    ("trang", "trang"): ("K05", _KG_A_TRANG, lambda g: f"        if not ({g}) and (not isinstance(tr, dict) or "
                         'not isinstance(tr.get("check_runs"), list)):\n            continue\n' + _KG_A_TRANG),
    ("trang", "tc_vang"): ("K06", "        if tc is _VANG:\n", lambda g: f"        if tc is _VANG and ({g}):\n"),
    ("trang", "tc_kieu"): ("K07", "        if type(tc) is not int or tc < 0:\n",
                           lambda g: f"        if (type(tc) is not int and ({g})) or (type(tc) is int and tc < 0):\n"),
    ("trang", "tc_am"): ("K07", "        if type(tc) is not int or tc < 0:\n", lambda g: f"        if type(tc) is not int or (tc < 0 and ({g})):\n"),
    ("trang", "run"): ("K08", _KG_A_RUN, lambda g: f"            if not ({g}) and not isinstance(r, dict):\n                continue\n" + _KG_A_RUN),
    ("trang", "schema"): ("K12", "            if sai:\n", lambda g: f"            if sai and ({g}):\n"),
    ("trang", "suite"): ("K15", _KG_A_SUITE, lambda g: _KG_A_SUITE.replace("if ", "if (", 1).replace(":\n", f") and ({g}):\n")),
}
for (_vg, _ch), (_hang, _tim, _thay) in list(_KG_T4_CHOT.items()):
    for _tt, _g in _KG_G.items():
        _kg_o("T4", "trang", f"chi_{_tt}:{_ch}", _hang, f"kg_t4_trang_{_ch}_chi_{_tt}", _tim, _thay(_g.format("i", "len(trang)")),
              f"kg_t4_trang_{_ch}")
        if _ch in ("run", "schema", "suite"):
            _kg_o("T4", "run", f"chi_{_tt}:{_ch}", _hang, f"kg_t4_run_{_ch}_chi_{_tt}", _tim,
                  _thay(_g.format("j", 'len(tr["check_runs"])')), f"kg_t4_run_{_ch}")
for _tt, _g in _KG_G.items():
    _kg_o("T4", "ten_doi_so", f"chi_{_tt}", "K24", f"kg_t4_ten_doi_so_chi_{_tt}", _KG_BB,
          f"    if any((not t.strip() or t.splitlines() != [t]) and ({_g.format('k', 'len(ten_bb)')}) for k, t in enumerate(ten_bb)):\n",
          "kg_t4_doi_so")
    _gt = _g.format("ten_bb.index(ten)", "len(ten_bb)")
    _kg_o("T4", "ten_mau", f"chi_{_tt}:vang", "K29", f"kg_t4_ten_mau_vang_chi_{_tt}", "        if not cung:\n",
          f"        if not cung and not ({_gt}):\n            continue\n        if not cung:\n", "kg_t4_mau_vang")
    _kg_o("T4", "ten_mau", f"chi_{_tt}:do", "K35", f"kg_t4_ten_mau_do_chi_{_tt}", "            if not hop_le:\n",
          f"            if not hop_le and ({_gt}):\n", "kg_t4_mau_do")
    _kg_o("T4", "ten_canh_bao", f"chi_{_tt}", "K26", f"kg_t4_ten_canh_bao_chi_{_tt}", "        if khac:\n",
          f"        if khac and ({_g.format('ten_bb.index(ten_cb)', 'len(ten_bb)')}):\n", "kg_t4_canh_bao")
    _kg_o("T4", "danh_tinh", f"chi_{_tt}", "K16", f"kg_t4_danh_tinh_chi_{_tt}", '        if danh_tinh.setdefault(r["id"], dt) != dt:\n',
          f'        if danh_tinh.setdefault(r["id"], dt) != dt and ({_g.format("[id(x) for x in runs].index(id(r))", "len(runs)")}):\n', "kg_t4_dt")
    _kg_o("T4", "id_max", f"chi_{_tt}", "K31", f"kg_t4_id_max_chi_{_tt}", "            if not hop_le:\n",
          "            if not hop_le and (" + _g.format(f"[id(x) for x in {_KG_NHOM_MAX}].index(id(r))", f"len({_KG_NHOM_MAX})") + "):\n",
          "kg_t4_id_max")
    _kg_o("T4", "khai", f"chi_{_tt}", "K19", f"kg_t4_khai_chi_{_tt}", "any(t != tong_khai for t in khai)",
          f"any(t != tong_khai and ({_g.format('k', 'len(khai)')}) for k, t in enumerate(khai))", "kg_t4_khai")


# --- T6: fixture ĐƠN CHỐT. Mỗi fixture từ chối được SINH có bản sửa khác nó ĐÚNG ở chốt đích, và bản sửa phải ra rc 0;
# bản sửa còn đỏ ⇒ fixture đang bị một chốt KHÁC chặn hộ (lớp `fixture-vi-pham-nhieu-chot`, #822 lượt 5–6).
def _kg_sua_ten(kw, cu, moi):
    """Bản sửa của fixture ĐỐI SỐ: thay giá trị sai bằng giá trị đúng ở MỌI chỗ nó xuất hiện nguyên văn (đối số và run trùng
    nguyên văn), không đụng gì khác."""
    doi = lambda x: moi if x == cu else x
    du = json.loads(json.dumps(kw["du_lieu"]))
    for tr in du if isinstance(du, list) else [du]:
        for r in tr.get("check_runs", []):
            r["name"] = doi(r["name"])
    return {**kw, "du_lieu": du, "bat_buoc": tuple(doi(t) for t in kw["bat_buoc"]), "expect": 0, "chua": ""}




def _kg_t6_cu():
    """18 ca đối số cũ của #822 (12 tên + 6 suite) — đọc fixture TỪ CHÍNH ca (`_kg_ca(...).kw`), không chép lại."""
    for ten, ca in _KG_CA.items():
        kw = getattr(ca, "kw", None)
        if kw is None or kw["expect"] != 2:
            continue
        if ten.startswith("kg_n1_check_suite_") and ten != "kg_n1_check_suite_abc":
            yield ten, {**kw, "suite": "1", "du_lieu": {"check_runs": [_kg_run(1)]}, "expect": 0, "chua": ""}
        elif ten in ("kg_m1_bat_buoc_rong", "kg_k24_ten_chi_khoang_trang") or ten.startswith("kg_f04_xuong_dong_"):
            yield ten, _kg_sua_ten(kw, kw["bat_buoc"][0], "gate")


def _kg_t6_loi(c: Ctx, muc) -> list:
    """Mục mà BẢN SỬA không ra rc 0. Danh sách là ĐỐI SỐ để ca tự kiểm cho nó một mục biết trước đáp án."""
    loi = []
    for nhan, sua in muc:
        try:
            _kg_kiem(c, **{**sua, "expect": 0, "chua": ""})
        except (AssertionError, CliSapDo) as ex:
            loi.append(f"{nhan}: {type(ex).__name__}: {str(ex)[:200]}")
    return loi


def case_kg_t6_ban_sua(c: Ctx):
    """T6 trên MỌI họ `_kg_ho` đã đăng vào CASES (đếm độc lập trên bảng bộ sinh, nên bỏ một họ khỏi phép duyệt là ĐỎ), cộng 18
    ca đối số cũ. Bản sửa trùng nhau giữa ca theo toán tử và ca họ đầy đủ chỉ chạy MỘT lần."""
    ho = [(k, f.muc) for k, f in CASES if getattr(f, "muc", None)]
    so_ho = sum(map(len, (_KG_T1_CA, _KG_T2_CA, _KG_T3_CA, _KG_T4_CA, _KG_T5_CA)))   # bảng bộ sinh, ĐỘC LẬP với phép duyệt CASES
    muc, thieu, da = [], [], set()
    for ten, sinh in ho:
        for nhan, kw, sua in sinh():
            if kw.get("expect", 12) == 0:
                continue
            if not sua:
                thieu.append(f"{ten}/{nhan}")
                continue
            khoa = json.dumps(sua, sort_keys=True, ensure_ascii=False)
            if khoa not in da:
                da.add(khoa)
                muc.append((f"{ten}/{nhan}", sua))
    cu = list(_kg_t6_cu())
    if thieu or len(cu) != 18 or len(ho) != so_ho:
        raise AssertionError(f"T6: thiếu bản sửa {thieu[:5]} ({len(thieu)}) · ca cũ {len(cu)}/18 · họ duyệt {len(ho)}/{so_ho}")
    muc += cu
    loi = _kg_t6_loi(c, muc)
    if loi:
        raise AssertionError(f"{len(loi)} bản sửa không ra rc 0 (chốt khác chặn hộ): " + "; ".join(loi[:5]))


def case_kg_t6_co_rang(c: Ctx):
    """Biết trước đáp án: bản sửa còn thiếu run của `gate2` PHẢI bị tố; bản sửa sạch PHẢI được tha."""
    ban = lambda bb: dict(du_lieu={"total_count": 1, "check_runs": [_kg_run(1)]}, bat_buoc=bb)
    ra = _kg_t6_loi(c, [("hai_chot", ban(("gate", "gate2"))), ("sach", ban(("gate",)))])
    if len(ra) != 1 or not ra[0].startswith("hai_chot:"):
        raise AssertionError(f"tự kiểm T6 đòi tố đúng `hai_chot`, được {ra!r}")


# --- Bổ đề cho các dòng `tuong_duong` của T2/T5: ĐO, không khẳng định suông.
def case_kg_t_bo_de(c: Ctx):
    chu = set("0123456789abcdef") | set("completed") | set("success")
    for h in ("completed", "success"):
        if "".join(sorted(h)) == h:
            raise AssertionError(f"{h!r} đã sắp xếp — ô `sap_xep:trai:hoac` không còn tương đương")
    for h in ("completed", "success", _KG_HEAD, _KG_T5_HEAD):
        for f in _KG_T2_BAT_BIEN:
            if _KG_T2_F[f][1](h) != h:
                raise AssertionError(f"{f}({h!r}) đổi giá trị — ô `phai` không còn tương đương")
    sai = [hex(k) for k in range(0x110000) if not 0xD800 <= k < 0xE000 and chr(k) not in chu
           and all(x in chu for x in unicodedata.normalize("NFD", chr(k)))]
    ngat = {chr(k) for k in range(0x110000) if not 0xD800 <= k < 0xE000 and ("a" + chr(k) + "b").splitlines() != ["a" + chr(k) + "b"]}
    for k in range(0x110000):
        if 0xD800 <= k < 0xE000:
            continue
        x, n = chr(k), unicodedata.normalize("NFKC", chr(k))
        if (x in ngat) != any(y in ngat for y in n) or x.isspace() != n.isspace() or not n:
            sai.append(f"NFKC {hex(k)}")
    if sai:
        raise AssertionError(f"bổ đề tương đương sai ở {sai[:10]}")


def _kg_ma_tran_loi(ma_tran, mutants, kiem_ke) -> list:
    """Mỗi ô trỏ một đột biến CÓ trong MUTANTS và CÓ trong bảng kiểm kê, hoặc khai `tuong_duong`/`khong_ap_dung` có lập luận."""
    co = {m for v in kiem_ke.values() if v[:1] != ("tuong_duong",) for m in v}
    loi = []
    for o, v in ma_tran.items():
        if isinstance(v, str):
            loi += [f"{o}: {v} ngoài MUTANTS/bảng kiểm kê"] if v not in mutants or v not in co else []
        elif len(v) != 2 or v[0] not in ("tuong_duong", "khong_ap_dung") or not str(v[1]).strip():
            loi.append(f"{o}: khai không hợp lệ {v!r}")
    return loi


def case_kg_t_ma_tran(c: Ctx):
    so = {h: sum(1 for o in _KG_MA_TRAN if o[0] == h) for h in ("T1", "T2", "T3", "T4", "T5")}
    doi = {"T1": 2 * sum(len(_kg_t1_cac_kieu(v)) for v in _KG_T1_VI_TRI) + 2 * len(_KG_T1_EP),
           "T2": len(_KG_T2_VI_TRI) * (len(_KG_T2_F) * 5 + len(_KG_T2_HUONG)),
           "T3": len(_KG_T3_VI_TRI) * (len(_KG_T3_OP) + 2),
           "T4": len(_KG_T4_VONG) * (len(_KG_CAT_T4) + 1) + len(_KG_G) * (len(_KG_T4_CHOT) + 3 + 1 + 2 + 1 + 1 + 1 + 1),
           "T5": 3 * (len(_KG_T5_CHUAN) * 2 + 1) + 2 + 4 + 2}
    loi = _kg_ma_tran_loi(_KG_MA_TRAN, MUTANTS, _KG_KIEM_KE) + [f"{h}: {so[h]} ô, đòi {doi[h]}" for h in so if so[h] != doi[h]]
    import ast   # T4 "mọi vòng lặp": số nút vòng lặp/comprehension THẬT của hai hàm = số vị trí T4 tường minh
    ham = [n for n in ast.parse(c.script.read_text(encoding="utf-8")).body
           if isinstance(n, ast.FunctionDef) and n.name in ("_doc_check_runs", "cmd_kiem_gate")]
    vong = sum(isinstance(x, (ast.For, ast.comprehension)) for h in ham for x in ast.walk(h))
    if len(ham) != 2 or vong != len(_KG_T4_VONG) - len(_KG_T4_NGAM):
        loi.append(f"T4: AST đếm {vong} vòng lặp, bảng khai {len(_KG_T4_VONG) - len(_KG_T4_NGAM)}")
    gia = _kg_ma_tran_loi({("T0", "x", "y"): "kg_khong_ton_tai", ("T0", "x", "z"): ("tuong_duong", " ")}, MUTANTS, _KG_KIEM_KE)
    if loi or len(gia) != 2:
        raise AssertionError(f"ma trận tập toán tử: {loi[:5]} · tự kiểm tố {len(gia)}/2")


def case_kg_t_ho_sap(c: Ctx):
    """M6 cho `_kg_ho`: chỉ-sập ⇒ TIN_DUNG_GIA; sập rồi đỏ SẠCH ⇒ GIẾT. Đo qua `chay_suite` + `_phan_loai_giet` trên bản sao
    sản phẩm có cú sập THẬT ở F02 (`ValueError→TypeError`, cùng cú sập ca tự kiểm M6 của #822 dùng)."""
    goc, tim = c.script.read_text(encoding="utf-8"), "    except ValueError:   # F02:"
    if goc.count(tim) != 1:
        raise AssertionError("mỏ neo F02 phải khớp đúng một chỗ")
    d = c.tmp / "sap"
    d.mkdir()
    (d / "packet_loop.py").write_text(goc.replace(tim, "    except TypeError:   # F02:"), encoding="utf-8", newline="\n")
    (d / "launcher.py").write_text((HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
    sap = ("sap", dict(du_lieu=_KG_1, suite="1" * 4301, chua="VẮNG"), None)
    do = ("do", dict(du_lieu=_KG_1, chua="ly do khong ton tai"), None)
    global CASES
    cu = CASES
    try:
        for ten, muc, doi in (("chi_sap", [sap], "TIN_DUNG_GIA"), ("sap_roi_do", [sap, do], "GIET")):
            CASES = [(ten, _kg_ho(ten, lambda m=muc: m))]
            v = chay_suite(d / "packet_loop.py", c.tmp / ten)[ten]
            if _phan_loai_giet(v) != doi:
                raise AssertionError(f"{ten}: đòi {doi}, được {_phan_loai_giet(v)} ({v!r})")
    finally:
        CASES = cu


CASES += [(k, _kg_ho(k, v)) for d in (_KG_T1_CA, _KG_T2_CA, _KG_T3_CA, _KG_T4_CA, _KG_T5_CA) for k, v in d.items()]


def case_kg_t_crlf_ly_do(c: Ctx):
    """#856 (run 39729983506, Windows): `_doi_ly_do` khớp lý do nhiều dòng dù stderr ra `\r\n`; lý do sai vẫn ĐỎ."""
    _doi_ly_do(2, 2, "A\r\nB\r\n".encode(), "A\nB", "crlf")
    try:
        _doi_ly_do(2, 2, "A\r\nC\r\n".encode(), "A\nB", "crlf")
    except AssertionError:
        return
    raise AssertionError("lý do sai mà vẫn qua")


CASES += [("kg_t6_ban_sua", case_kg_t6_ban_sua), ("kg_t6_co_rang", case_kg_t6_co_rang), ("kg_t_bo_de", case_kg_t_bo_de),
          ("kg_t_ma_tran", case_kg_t_ma_tran),
          ("kg_t_ho_sap", case_kg_t_ho_sap), ("kg_t_crlf_ly_do", case_kg_t_crlf_ly_do)]


# M1 — bảng kiểm kê: mỗi thành phần ⇒ đột biến (không sập, M6) HOẶC `("tuong_duong", "<lập luận hành vi>")`.
# K38–K41 executor thêm khi kiểm kê lại trên base `f712205`; K41 là argparse (ngoài lớp) nhưng M5(a) đòi mọi
# đột biến `kg_` có dòng.
_KG_KIEM_KE = {
    "K01": tuple(f"kg_k01_nuot_{t}" for t in ("OSError", "UnicodeDecodeError", "ValueError", "RecursionError")),
    "K02": ("kg_bo_hook_khoa_trung", "kg_r3_nested_suite_duplicates_ignored", "kg_r3_extra_key_duplicates_ignored"),
    "K03": ("kg_bo_hook_hang_ngoai_json",),
    "K04": ("kg_k04_list_rong_im_lang",),
    "K05": ("kg_k05_bo_qua_trang_hong", "kg_k05_bo_kiem_check_runs_list", "kg_r2_bo_trang_sau_hong", *_KG_R5["trang"]),
    "K06": ("kg_n5_bo_doi_co_mat", "kg_n5_trang_sau_thua_huong"),
    "K07": ("kg_k07_bo_kiem_kieu_tc", "kg_k07_bo_kiem_am", "kg_n5_bool_la_int", "kg_r2_tc_trang_dau", "kg_r3_later_page_negative_count"),
    "K08": ("kg_k08_bo_qua_phan_tu", "kg_r2_bo_run_trang_sau"),
    "K09": ("kg_k09_bo_kieu_id", "kg_bool_la_int", "kg_bo_qua_phan_tu_thieu_truong", "kg_r2_schema_trang_dau", *(m for m in _KG_R5["id"] if "kieu" in m)),
    "K10": ("kg_d3_bo_kieu_name", "kg_r2_schema_trang_dau", *_KG_R5["name"]),
    "K11": ("kg_d4_bo_kieu_head_sha", "kg_r2_schema_trang_dau", *_KG_R5["head_sha"]),
    "K12": ("kg_d5_bo_kieu_status", "kg_r2_schema_trang_dau", *(m for m in _KG_R5["status"] if "kieu" in m)),
    "K13": ("kg_d6_bo_kieu_conclusion", "kg_r2_schema_trang_dau", *(m for m in _KG_R5["conclusion"] if "kieu" in m)),
    "K14": ("kg_bool_la_int", "kg_n2_bool_la_int", "kg_n5_bool_la_int", "kg_r3_later_page_run_bool"),
    "K15": ("kg_n2_chi_kiem_bat_buoc", "kg_n2_bool_la_int", "kg_k15_bo_kieu_id_suite", "kg_k15_bo_qua_run_suite_hong", "kg_r2_suite_trang_dau", "kg_r3_later_page_suite_bool", *_KG_R5["suite"]),
    "K16": ("kg_f01_bo_ten_khoi_danh_tinh", "kg_f01_bo_kiem_danh_tinh", *_KG_R4["dt_ten"], *_KG_R5["vi_tri_dt"]),
    "K17": ("kg_f01_bo_suite_khoi_danh_tinh",),
    "K18": ("kg_d1_bo_head_khoi_danh_tinh", *_KG_R4["dt_head"]),
    "K19": ("kg_n5_bo_so_giua_trang", "kg_r2_so_hai_trang_dau"),
    "K20": ("kg_bo_kiem_thieu_trang", "kg_n5_quay_ve_nho_hon", "kg_k20_dem_ban_ghi"),
    "K21": ("kg_bo_sha_re", "kg_k21_nhan_hex_hoa", "kg_r2_sha_phi_hex", "kg_r2_sha_39", "kg_r2_sha_41", *_KG_R5["head_arg"]),
    "K22": ("kg_n1_bo_kiem_dang", "kg_n1_cho_so_0_dau", "kg_n1_chu_so_unicode", "kg_k22_match_tien_to", *_KG_R5["suite_arg"]),
    "K23": ("kg_f02_du_phong_khop_nham",),
    "K24": ("kg_bo_kiem_ten_rong", "kg_f04_bo_kiem_xuong_dong", "kg_k24_bo_strip", "kg_k24_chi_strip_space", *_KG_R5["vi_tri_ten"]),
    "K25": ("kg_k25_bo_khu_trung",),
    "K26": ("kg_n4_bo_canh_bao", "kg_n4_canh_bao_moi_ten", "kg_n4_dem_ban_ghi", "kg_n4_ten_theo_repr",
            "kg_k26_canh_bao_ca_suite_neo", "kg_k26_canh_bao_ra_stdout", "kg_r2_canh_bao_dem_1", "kg_r2_canh_bao_id_dau", "kg_r2_canh_bao_ten_dau", *_KG_R4["canh_bao"], "kg_r4_canh_bao_id_hai_dau", "kg_r4_canh_bao_ten_hai_dau", *_KG_R5["canh_bao_thu_tu"]),
    "K27": ("kg_khop_tien_to", "kg_xet_moi_check", "kg_r3_name_suffix", "kg_r3_name_casefold", "kg_r3_name_strip_run", "kg_r3_name_strip_arg", *_KG_R4["ten"]),
    "K28": ("kg_n3_bo_loc_suite", "kg_n3_suite_cua_run_dau"),
    "K29": ("kg_bo_kiem_vang", *_KG_R5["vi_tri_vang"]),
    "K30": ("kg_chon_success_bat_ky", "kg_chon_luot_cu_nhat", "kg_r2_id_theo_chuoi", *(m for m in _KG_R5["id"] if "id_max" in m)),
    "K31": ("kg_trung_id_chon_mot", "kg_k31_chon_ban_cuoi", *(m for m in _KG_R5["status"] + _KG_R5["conclusion"] if "trung_id" in m)),
    "K32": ("kg_bo_status_rieng", *_KG_R4["status"]),
    "K33": ("kg_bo_conclusion_rieng", "kg_danh_sach_cam", *_KG_R4["conclusion"]),
    "K34": ("kg_bo_so_head", "kg_r3_head_prefix", "kg_r3_head_suffix", "kg_r3_head_casefold", "kg_r3_head_first7", *_KG_R4["head"]),
    "K35": ("kg_d2_mot_ten_xanh_che_do", "kg_rc_gate_thanh_0"),
    "K36": ("kg_n6_dong_xanh_khong_suite", "kg_k36_chi_ten_dau", *_KG_R5["xanh"]),
    "K37": ("kg_k37_vang_la_null", "kg_r2_schema_trang_dau"),
    "K38": ("kg_k38_list_la_mot_trang", "kg_k38_object_bi_bo"),   # list ⇒ nhiều trang, object ⇒ một trang
    "K39": ("kg_k39_khong_in_dong_do", "kg_r3_red_first_name_only", "kg_r4_do_chi_cuoi", "kg_r4_do_hai_dau"),   # mỗi tên đỏ một dòng `ĐỎ` trên stderr nêu status/conclusion/head
    "K40": ("kg_k40_bo_break", "kg_r3_red_count_constant"),   # nhiều bản ghi đỏ cùng id lớn nhất vẫn là MỘT tên đỏ
    "K41": ("kg_n6_xoa_help",),   # `--help` nêu cách lấy check-suite (argparse)
    **{k: tuple(v) for k, v in _KG_T_K.items()},   # #856: "<họ T>-<hàng K>" ⇒ đột biến sinh bằng vòng của tập toán tử
}


def case_kg_m5_kiem_ke(c: Ctx):
    """M5: (a) mọi đột biến `kg_` có dòng · (b) mọi tên trong bảng có thật · (c) đủ K01…K37 · dòng
    `tuong_duong` phải kèm lập luận."""
    dung, loi = set(), []
    for k, v in _KG_KIEM_KE.items():
        if v[:1] == ("tuong_duong",):
            loi += [f"{k}: tuong_duong thiếu lập luận"] if len(v) != 2 or not str(v[1]).strip() else []
        elif not v:
            loi.append(f"{k}: dòng rỗng")
        dung |= set() if v[:1] == ("tuong_duong",) else set(v)
    loi += [f"(a) đột biến ngoài bảng: {sorted({m for m in MUTANTS if m.startswith('kg_')} - dung)}"] * bool(
        {m for m in MUTANTS if m.startswith("kg_")} - dung)
    loi += [f"(b) tên không có trong MUTANTS: {sorted(dung - set(MUTANTS))}"] * bool(dung - set(MUTANTS))
    thieu = [f"K{i:02d}" for i in range(1, 38) if f"K{i:02d}" not in _KG_KIEM_KE]
    loi += [f"(c) thiếu dòng {thieu}"] * bool(thieu)
    if loi:
        raise AssertionError("; ".join(loi))


def case_kg_m6_tin_dung_giet(c: Ctx):
    """M6: đột biến SẬP ở F02 (`ValueError→TypeError`) là TÍN DỤNG GIẢ; đột biến dự phòng `suite = 1`
    (xanh giả, không sập) là GIẾT; nền là SỐNG. Đo qua đúng `chay_suite` + `_phan_loai_giet` mà bộ chạy dùng."""
    goc, ca = c.script.read_text(encoding="utf-8"), "kg_f02_suite_vuot_tran_int"
    help_tim = 'help="id suite của CHÍNH lượt workflow'
    help_thay = 'help=1 or "id suite của CHÍNH lượt workflow'
    for ten, (tim, thay), doi, dich in (
            ("nen", ("", ""), "SONG", ca),
            ("sap", ("    except ValueError:   # F02:", "    except TypeError:   # F02:"), "TIN_DUNG_GIA", ca),
            ("du_phong", MUTANTS["kg_f02_du_phong_khop_nham"][:2], "GIET", ca),
            ("stdout", ("        suite = a.check_suite   #",
                        "        import traceback; traceback.print_exc(file=sys.stdout); return RC_GATE   #"), "TIN_DUNG_GIA", ca),
            ("repr", ("        suite = a.check_suite   #",
                      "        import traceback; print(repr(traceback.format_exc())); return RC_GATE   #"), "TIN_DUNG_GIA", ca),
            ("rc8", ("        suite = a.check_suite   #", "        return RC_STATE   #"), "TIN_DUNG_GIA", ca),
            # Traceback THẬT (ValueError của `int()` ở F02) trong mọi vỏ, trên cả hai kênh, rc 12 hợp lệ.
            *((f"boc_{nhan}_{kenh}", ("        suite = a.check_suite   #",
                                      f"        import traceback; print({bt}, file=sys.{kenh}); return RC_GATE   #"),
               "TIN_DUNG_GIA", ca) for kenh in ("stdout", "stderr") for nhan, bt in (
                ("json", 'json.dumps({"traceback": traceback.format_exc()})'),
                ("long", 'json.dumps({"e": {"tb": traceback.format_exc()}})'),
                ("hai_lop", 'json.dumps(json.dumps({"e": traceback.format_exc()}))'),
                ("list", "repr([traceback.format_exc()])"), ("log", '"ERROR: " + traceback.format_exc()'),
                ("khong_frame", "traceback.format_exc().splitlines()[0]"),
                ("escape_u", 'json.dumps(traceback.format_exc()).replace("T", "\\\\u0054")'),
                ("escape_u_2_lop", 'json.dumps(json.dumps(traceback.format_exc()).replace("T", "\\\\u0054"))'))),
            ("help", (help_tim, help_thay), "TIN_DUNG_GIA", "kg_n6_help"),
            ("help12", (help_tim, help_thay), "TIN_DUNG_GIA", "kg_m4_rc_gate_12")):
        d = c.tmp / ten
        d.mkdir()
        if tim and goc.count(tim) != 1:
            raise AssertionError(f"mỏ neo {tim!r} phải khớp đúng một chỗ")
        (d / "packet_loop.py").write_text(goc.replace(tim, thay, 1) if tim else goc, encoding="utf-8", newline="\n")
        (d / "launcher.py").write_text((HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
        v = chay_suite(d / "packet_loop.py", d / "run", chi_chay={dich})[dich]
        if _phan_loai_giet(v) != doi:
            raise AssertionError(f"{ten}: đòi {doi}, được {_phan_loai_giet(v)} ({v!r})")

    # Mọi nhánh except phải giữ tín hiệu crash, kể cả BoQua.
    global CASES
    cu = CASES
    nhom = getattr(sys.modules["builtins"], "ExceptionGroup", None)
    try:
        for mode in ("cause", "context", "none", "skip_cause", "skip_context", "cause_ngoai", "skip_cause_ngoai", "group")[:8 if nhom else 7]:
            def boc(ctx, mode=mode):
                loi = None
                try:
                    case_kg_f02_suite_vuot_tran_int(ctx)
                except CliSapDo as ex:
                    loi = ex
                    if mode not in ("group", "cause_ngoai", "skip_cause_ngoai"):
                        if mode == "skip_cause":
                            raise BoQua("bọc crash") from ex
                        if mode == "skip_context":
                            raise BoQua("bọc crash")
                        if mode == "cause":
                            raise AssertionError("bọc crash") from ex
                        if mode == "none":
                            raise AssertionError("bọc crash") from None
                        raise AssertionError("bọc crash")
                # NGOÀI khối except: `__context__` rỗng, chỉ `__cause__` (hoặc thành viên nhóm) còn giữ tín hiệu.
                if mode == "group":
                    raise nhom("bọc crash", [loi])
                raise (BoQua if mode == "skip_cause_ngoai" else AssertionError)("bọc crash") from loi
            CASES = [("kg_m6_boc_cli", boc)]
            v = chay_suite(c.tmp / "sap" / "packet_loop.py", c.tmp / mode)["kg_m6_boc_cli"]
            if _phan_loai_giet(v) != "TIN_DUNG_GIA":
                raise AssertionError(f"{mode}: crash bị rửa thành {_phan_loai_giet(v)}")
    finally:
        CASES = cu

    # Chiều bắt OAN: fixture mang banner (thô, trong đối số, hoặc qua escape JSON) bị từ chối như lỗi viết
    # test — KHÔNG thành `CliSapDo`, nên không thể biến một ca đúng thành tín dụng giả.
    ten = "Traceback (most recent call last):"
    for du_lieu, tho, bb in (({"check_runs": [_kg_run(1, name=ten)]}, None, ten),
                             (_KG_1, None, ten),
                             (None, json.dumps(_KG_1).replace('"gate"', '"\\u0054raceback (most recent call last)"'), "gate")):
        ket = "không bị từ chối"
        try:
            _kg(c, du_lieu, bb, tho=tho)
        except CliSapDo:   # ném NGOÀI khối except: `CliSapDo` trong `__context__` sẽ biến ca này thành tín dụng giả
            ket = "bị đọc thành CLI sập"
        except AssertionError as ex:
            ket = None if "KHÔNG được mang banner" in str(ex) else f"lỗi khác: {ex}"
        if ket:
            raise AssertionError(f"fixture mang banner {bb!r}: {ket}")


CASES += [("kg_m5_kiem_ke", case_kg_m5_kiem_ke), ("kg_m6_tin_dung_giet", case_kg_m6_tin_dung_giet)]
# A4 + A12: đột biến NHẮM TEST — gỡ từng vế của hai ca tự kiểm thì ca ấy phải ĐỎ.
MUTANTS.update({
    # Đổi TÊN khoá (giữ mọi đột biến trong bảng) ⇒ (a)(b) vẫn đúng, chỉ (c) có thể đỏ.
    "t822_bang_mat_K14": ('    "K14": ("kg_bool' + '_la_int",', '    "K14_ban_sao": ("kg_bool_la_int",', ["kg_m5_kiem_ke"]),
    # Mốc ghép bằng `+` để chuỗi liền chỉ có ở ĐÚNG chỗ bị đột biến (`moc_dot_bien_phai_khop_DUNG_MOT_CHO`).
    "t822_bang_ten_khong_ton_tai": ('    "K25": ("kg_k25_bo' + '_khu_trung",),', '    "K25": ("kg_k25_bo_khu_trung", "kg_khong_ton_tai"),',
                                    ["kg_m5_kiem_ke"]),
    "t822_mutant_kg_ngoai_bang": ('CASES += [("kg_m5_kiem' + '_ke", case_kg_m5_kiem_ke),',
                                  'MUTANTS["kg_ngoai_bang"] = ("x", "y", ["kg_m5_kiem_ke"])\nCASES += [("kg_m5_kiem' + '_ke", case_kg_m5_kiem_ke),',
                                  ["kg_m5_kiem_ke"]),
    # M6: mỗi chốt của bộ phân loại một đột biến riêng — gỡ chốt nào thì ca tự kiểm M6 phải ĐỎ.
    **{f"t822_m6_{ten}": (tim, thay, ["kg_m6_tin_dung_giet"]) for ten, tim, thay in (
        ("run_khong_kiem", "        _kg_kiem_ket_qua(p.returncode, p.stdout," + " p.stderr, cmd)\n", "        pass\n"),
        ("chi_doc_stderr", "sap = any(_co_banner(out) for out in (o, " + "e))", "sap = any(_co_banner(out) for out in (e,))"),
        ("dau_vao_khong_kiem", "    if any(_co_banner(b) for b in " + "vao):\n", "    if False:\n"),
        ("bo_giai_escape", "    for _ in range(4):   # thô" + " + 3 lớp\n", "    for _ in range(1):\n"),
        ("bo_duyet_cause", "        cho += [ex.__cause__, ex." + "__context__]\n", "        cho += [ex.__context__]\n"),
        ('bo_doi_so', '    vao = [str(x).encode("utf-8", "surrogatepass") for x in cmd]\n', '    vao = []\n'),
        ("rc_moi_so", "_KG_RC_HOP_LE = frozenset((0, 2, " + "12))", "_KG_RC_HOP_LE = frozenset(range(256))"),
        ("boqua_rua_sap", 'ket[ten] = (_TinDungGia(f"{type(ex).__name__}: {ex}") if _co_sap' + "_do(ex) else",
         'ket[ten] = (_TinDungGia(f"{type(ex).__name__}: {ex}") if False else'),
        ("bo_duyet_group", "            cho += list(ex." + "exceptions)\n", "            pass\n"))},
    "t822_moi_ca_do_la_giet": ('else "TIN_DUNG_GIA" if isinstance(v, _TinDung' + 'Gia)', 'else "TIN_DUNG_GIA" if False', ["kg_m6_tin_dung_giet"]),
})
MUTANTS_NHAM_TEST = MUTANTS_NHAM_TEST | {k for k in MUTANTS if k.startswith("t822_")}
# #856: gỡ từng phép tự kiểm mới thì ca tự kiểm của nó PHẢI đỏ. Mốc ghép bằng `+` (khớp ĐÚNG một chỗ).
MUTANTS.update({
    "t856_t6_khong_chay_ban_sua": ('            _kg_kiem(c, **{**sua, "expect": 0, ' + '"chua": ""})\n', "            pass\n", ["kg_t6_co_rang"]),
    "t856_t2_chi_so_trung_tam": ("    for i in range(len(v)):   # #856 lượt 2: MỌI " + "chỉ số",
                                 "    for i in sorted({0, 1, len(v) // 2, len(v) - 1}):   # #856 lượt 2: MỌI chỉ số", ["kg_t2_phu"]),
    "t856_t2_phu_khong_tinh_hoac": ("for hoac in ((False, True) if ph in (" + '"trai", "phai") else (False,)):',
                                    "for hoac in (False,):", ["kg_t2_phu"]),
    "t856_t6_bo_mot_ho": ('    ho = [(k, f.muc) for k, f in CASES if getattr(f, "muc", ' + 'None)]\n',
                          '    ho = [(k, f.muc) for k, f in CASES if getattr(f, "muc", None)][1:]\n', ["kg_t6_ban_sua"]),
    "t856_ma_tran_khong_kiem_ten": ("if v not in mutants or v not in " + "co else []", "if False else []", ["kg_t_ma_tran"]),
    "t856_ho_nuot_sap": ("        if sap:\n            raise " + "sap\n", "        if False:\n            raise sap\n", ["kg_t_ho_sap"]),
    "t856_ho_sap_thanh_giet": ("                sap = sap " + "or ex\n", "                loi = f\"{ten}: {ex}\"\n", ["kg_t_ho_sap"]),
    "t856_ly_do_bo_crlf": ('    t = _txt(err).replace("\\r\\n", ' + '"\\n")\n', "    t = _txt(err)\n", ["kg_t_crlf_ly_do"]),
})
MUTANTS_NHAM_TEST = MUTANTS_NHAM_TEST | {k for k in MUTANTS if k.startswith("t856_")}

# --- #775 Review Rescue. `verdict ≠ approve VÀ (vòng ≥ trần HOẶC codex ≥ trần)`: mỗi vế một ca sai ĐÚNG MỘT vế.
_URL, _H1, _H2 = "https://github.com/o/r/issues/775#issuecomment-1", f"{1:040x}", f"{2:040x}"
_RESCUE = {"state": "blocked", "ly_do": "rescue_required"}
_st = lambda sd: json.loads((sd / "wp55.json").read_text(encoding="utf-8"))


def _pl(c, sd, *buoc):  # mỗi bước `(rc đòi, lệnh, đối số…)`; `--packet 55` tự chèn
    for rc_doi, lenh, *doi in buoc:
        rc, _, e = run(c.script, [lenh, "--packet", 55, *doi], sd)
        _doi(rc_doi, rc, e, f"{lenh} {doi}")


def _kiem(sd, msg, **muon):
    co = {k: _st(sd).get(k) for k in muon}
    if co != muon: raise AssertionError(f"{msg}: đòi {muon}, được {co}")


_goi = lambda run_id, head, rc=0: (rc, "record-codex-call", "--head", head, "--run-id", run_id)
_rescue = lambda rc, qd: (rc, "record-rescue", "--quyet-dinh", qd, "--can-cu", _URL)
_nang = lambda rc, ai="ducthangho", tran=3, can_cu=_URL: (rc, "nang-tran", "--truc", "codex_review_calls", "--tran-moi", tran, "--ai-nang", ai, "--can-cu", can_cu)
_rv = lambda rc, verdict, goi, sha=_H1: (rc, "record-review", "--provider", REVIEWER, "--verdict", verdict, "--reviewed-sha", sha, *(["--codex-call", goi] if goi else []), *(["--finding-id", f"loi-{goi}"] if verdict != "approve" else []))


def _reviewing(c, *extra, vao=True):
    sd = c.sd(); _doi(0, c.init(sd, extra=extra)[0], b"", "init")
    if vao: c.den_reviewing(sd, 55, 1)
    return sd


def case_pl_m1_tran_so_duong(c: Ctx):
    for co in ("--review-rounds-limit", "--codex-review-calls-limit"):
        for xau in ("0", "-1", "abc"):
            _doi(2, c.init(c.sd(), extra=(co, xau), lease=False)[0], b"", f"init {co} {xau}")
    sd = c.sd()
    _pl(c, sd, (0, "init", "--mission", 54, "--executor", EXECUTOR, "--reviewer", REVIEWER))
    _kiem(sd, "state v2 mặc định", schema_version=2, review_rounds_used=0, review_rounds_limit=10,
          codex_review_calls_used=0, codex_review_calls_limit=2, codex_calls=[], nang_tran=[])


def case_pl_m2_loi_goi(c: Ctx):
    sd = _reviewing(c, "--codex-review-calls-limit", 2, vao=False)
    _pl(c, sd, _goi("g0", _H1, 8))
    c.den_reviewing(sd, 55, 1)
    _pl(c, sd, _goi("g1", _H2, 5), _goi("g1", _H1), _goi("g1", _H1, 2), _goi("a b", _H1, 2), _goi("g2", _H1), _goi("g3", _H1, 3))
    _kiem(sd, "chặn TRƯỚC khi ghi", truc="codex_review_calls", codex_review_calls_used=2, **_RESCUE)
    (sd / "wp55.json").write_text(json.dumps({**_st(sd), "reviewer": "claude", "reviewer_identity": None}))
    _pl(c, sd, _goi("g9", _H1, 4))  # reviewer khác codex ⇒ RC_PROVIDER, không phải RC_STATE/RC_TRAN


def case_pl_m3_neo_loi_goi(c: Ctx):
    sd = _reviewing(c)
    _pl(c, sd, _goi("b1", _H1), _rv(5, "approve", None), _rv(0, "changes_requested", "b1"))
    c.den_reviewing(sd, 55, 2, head=_H1)  # cùng head ⇒ chỉ vế `da_dung` sai
    _pl(c, sd, _rv(5, "approve", "b1"))
    _kiem(sd, "review bị từ chối không tăng vòng", review_rounds_used=1)
    sd = _reviewing(c)
    _pl(c, sd, _goi("a1", _H1), _goi("b1", _H1), _rv(0, "changes_requested", "b1"))
    c.den_reviewing(sd, 55, 2)  # `a1` chưa dùng ⇒ chỉ vế head sai
    _pl(c, sd, _rv(5, "approve", "a1", _H2))


def _hai_nhanh(c, sd, luot, truc):  # state chạm trần ⇒ changes_requested: rescue · approve: accepted
    sd2, g, h = c.sd(), f"g{luot}", c.head(luot)
    __import__("shutil").copytree(sd, sd2, dirs_exist_ok=True)
    _pl(c, sd, _goi(g, h), _rv(3, "changes_requested", g, h))
    _kiem(sd, "chạm trần + changes_requested", truc=truc, **_RESCUE)
    _pl(c, sd2, _goi(g, h), _rv(0, "approve", g, h)); _kiem(sd2, "approve không bao giờ kích rescue", state="accepted")


def case_pl_m3_vong(c: Ctx):
    sd = _reviewing(c, "--review-rounds-limit", 10, "--attempts-limit", 10, vao=False)
    for n in range(1, 10):
        c.den_reviewing(sd, 55, n)
        _doi(0, c.review(sd, 55, [f"loi-{n}"], luot=n)[0], b"", f"vòng {n} < trần")
    c.den_reviewing(sd, 55, 10)
    sd3 = c.sd(); __import__("shutil").copytree(sd, sd3, dirs_exist_ok=True); (sd3 / "wp55.json").write_text(json.dumps({**_st(sd3), "review_rounds_limit": 9})); _pl(c, sd3, _goi("g10", c.head(10)), _rv(3, "approve", "g10", c.head(10)))  # review MỚI khi đã chạm trần vòng ⇒ rescue, kể cả approve
    _hai_nhanh(c, sd, 10, "vong_review")


def case_pl_m3_codex(c: Ctx):
    for tran_vong in (50, 2):  # riêng trục codex, rồi hai trục cùng chạm để khóa thứ tự
        sd = _reviewing(c, "--codex-review-calls-limit", 2, "--review-rounds-limit", tran_vong)
        _doi(0, c.review(sd, 55, ["loi-1"])[0], b"", "lời gọi 1")
        c.den_reviewing(sd, 55, 2); _hai_nhanh(c, sd, 2, "codex_review_calls")


def case_pl_m4_nang_tran(c: Ctx):
    sd = _reviewing(c, "--codex-review-calls-limit", 2)
    _pl(c, sd, *[_nang(7, ai=t) for t in ("codex-dispatcher", "ducthangho-bot", "cödex", "codex", "")],
        _nang(2, tran=2), *[_nang(2, can_cu=u) for u in (_URL.split("#")[0], "https://github.com/o#x/r/issues/775#issuecomment-1", _URL + "\n")], _nang(0, ai=" ducthangho "))
    _kiem(sd, "nâng trần hợp lệ", codex_review_calls_limit=3)
    if [(n["tran_cu"], n["tran_moi"]) for n in _st(sd)["nang_tran"]] != [(2, 3)]: raise AssertionError("khối nang_tran phải mang khoá chuẩn tran_cu/tran_moi (ADR-0043/0048)")


def case_pl_m5_rescue(c: Ctx):
    sf = _reviewing(c, vao=False)
    for n, rc in ((1, 0), (2, 3)):
        c.den_reviewing(sf, 55, n)
        _doi(rc, c.review(sf, 55, ["lap-lai"], luot=n)[0], b"", f"same-failure lượt {n}")
    _pl(c, sf, _rescue(8, "dung"))  # blocked vì same-failure ⇒ không phải cửa rescue
    sd = _reviewing(c, "--codex-review-calls-limit", 1)
    _pl(c, sd, _goi("g1", _H1), _goi("g2", _H1, 3), (8, "transition", "--to", "running"), _rescue(8, "nang_tran"))
    for qd in ("tach_stable_slice", "revision", "dung"):
        _pl(c, sd, _rescue(0, qd)); _kiem(sd, f"{qd} GIỮ blocked", truc="codex_review_calls", **_RESCUE)
    for hong in ({"nang_tran": [dict(truc="codex_review_calls", tran_cu=0, tran_moi=1, ai_nang="ducthangho", can_cu=_URL)]}, {"codex_review_calls_limit": 2}, {"codex_review_calls_limit": 2, "nang_tran": [{"truc": "codex_review_calls", "tran_moi": 2}]}): (sd / "wp55.json").write_text(json.dumps({**_st(sd), "nang_tran": [], **hong})); _pl(c, sd, _rescue(8, "nang_tran"))  # F12: sửa tay MỘT trường (sổ nâng / trần) không mở lại
    _pl(c, sd, _nang(0, tran=3), _rescue(0, "nang_tran")); _kiem(sd, "nang_tran mở lại running", state="running", ly_do=None, truc=None)
    if sum(h["event"] == "record_rescue" for h in _st(sd)["history"]) != 8: raise AssertionError("record-rescue phải LUÔN ghi biên bản")


def case_pl_m6_state_v1(c: Ctx):
    sd = _reviewing(c); st = {k: v for k, v in _st(sd).items() if not k.startswith(("review_r", "reviewer_i", "codex_", "nang"))}
    (sd / "wp55.json").write_text(json.dumps({**st, "schema_version": 1, "reviews": [{"provider": REVIEWER, "attempt": n} for n in (1, 2, 3)]}))
    sd2 = c.sd(); (sd2 / "wp55.json").write_text(json.dumps({**_st(sd), "reviewer_identity": {"model_family": "openai"}})); _pl(c, sd2, _goi("g1", _H1, 3))  # M6: call dùng họ tường minh; sd giữ thiếu họ để đo suy
    _kiem(sd2, "lần ghi sau lưu v2 giữ cờ", schema_version=2, dem_tu_suy=True, codex_review_calls_used=3)
    rc, o, e = run(c.script, ["status", "--packet", 55], sd)
    _doi(0, rc, e, "status trên state v1 hợp lệ")
    t = json.loads(o.decode("utf-8"))
    if "SUY RA" not in _txt(e) or (t["codex_review_calls_used"], t["review_rounds_used"], t["dem_tu_suy"]) != (3, 3, True):
        raise AssertionError(f"v1 phải suy 3/3 kèm cảnh báo: {_txt(e)!r}")
    g = {"run_id": "g1", "head": _H1, "da_dung": False}  # mỗi ca: state SẠCH `t` lệch ĐÚNG MỘT bất biến; {} là đối chứng
    for hong in ({}, *({k: ...} for k in ("packet", "state", "attempt_open", "reviewing_head_sha", "mission", "executor", "posts", "hmac_key")), {"schema_version": 1}, {"schema_version": 3}, {"schema_version": 2.0}, {"schema_version": True}, {"schema_version": 1.0},
                 *({k: v} for k, v in (("attempts_used", True), ("attempts_used", 0.5), ("attempts_used", "one"),
                                      ("attempt_open", "false"), ("attempt_open", []), ("same_failure_limit", None), ("finding_counts", []), ("packet", None), ("packet", []), ("packet", True), ("packet", 55.0), ("packet", 56), ("state", []), ("state", "other"), ("reviewing_head_sha", []), ("reviewing_head_sha", t["reviewing_head_sha"] + "\n"), ("posts", None), ("posts", []), ("posts", "x"), ("executor_identity", []), ("executor_identity", False), ("executor_identity", "claude"))),
                 *({"posts": {"123456789": p}} for p in ({}, [], False, "x", {"for": "reviewing"})), {"attempt_anchor": {k: v for k, v in t["attempt_anchor"].items() if k != "nonce"}}, {"finding_counts": {"probe-finding": 1}}, {"reviews": [dict(r, finding_ids=["probe-finding"]) for r in t["reviews"]]}, {"history": [{"event": "blocked_rescue_required", "truc": "codex_review_calls"}]},
                 *({"state": s, "ly_do": "rescue_required", "truc": "codex_review_calls", "history": [{"event": "blocked_rescue_required", "truc": "codex_review_calls"}]} for s in ("running", "reviewing", "accepted")),
                 {"codex_review_calls_limit": True}, {"codex_calls": {}}, {"dem_tu_suy": "false"}, {"codex_calls": [dict(g, da_dung=1)]},
                 {"codex_calls": [g, g]}, {"codex_calls": [dict(g, run_id=f"g{i}") for i in range(4)]}, {"codex_review_calls_used": 2},
                 {"codex_calls": [g]}, {"review_rounds_used": 2}, {"reviews": {}, "review_rounds_used": 0}, {"history": None}, {"history": [None]},
                 {"reviews": [{}], "review_rounds_used": 1}, {"reviews": [{"provider": REVIEWER}], "review_rounds_used": 1}, {"reviewer_identity": {"model_family": None}}, {"reviewer_identity": []},
                 {"reviewer_identity": False}, {"state": "blocked", "ly_do": "rescue_required", "truc": "vong_review",
                                             "history": [{"event": "blocked_rescue_required", "truc": "codex_review_calls"}]},
                 {"state": "blocked", "ly_do": "rescue_required", "truc": "unknown", "history": [{"event": "blocked_rescue_required", "truc": "unknown"}]}):
        (sd / "wp55.json").write_text(json.dumps({k: v for k, v in {**t, **hong}.items() if v is not ...}))
        _pl(c, sd, (8 if hong else 0, "status"))


CASES += [(n[5:], f) for n, f in list(globals().items()) if n.startswith("case_pl_m")]
_PL_VONG = "in reversed(TRUC_TRAN.items()):  #"
_PL_CHAN = ('    if st["codex_review_calls_used"] >= st["codex_review_calls_limit"]:\n',
            '        _vao_rescue(state_dir, st, "codex_review_calls", "lời gọi codex bị CHẶN TRƯỚC")\n',
            '    st["codex_review_calls_used"] += 1\n')
MUTANTS.update({f"pl_f01_bo_{ten}": (f'("{ten}", ', f'("{ten}", True or ', ["pl_m6_state_v1"])
                for ten in ("schema", "bo-dem", "so", "loi-goi", "dem-goi", "dem-vong", "truc", "posts", "anchor", "findings", "checkpoint")})
MUTANTS.update({
    "pl_f10_bo_phan_biet_v1": (' and not st.keys() & {"review_rounds_used", "review_rounds_limit", "codex_review_calls_used", "codex_review_calls_limit", "codex_calls", "nang_tran", "dem_tu_suy"}', "", ["pl_m6_state_v1"]),
    "pl_f07_bo_kieu_packet": ('type(st["packet"]) is int and ', "", ["pl_m6_state_v1"]),
    "pl_m1_bo_kiem_so_duong": ("a.codex_review_calls_limit) <= 0:", "a.codex_review_calls_limit) < 0:", ["pl_m1_tran_so_duong"]),
    "pl_m2_kiem_sau_khi_ghi": ("".join(_PL_CHAN), _PL_CHAN[2] + _PL_CHAN[0].replace(">=", ">") + _PL_CHAN[1], ["pl_m2_loi_goi"]),
    "pl_m2_lon_hon_bang": (_PL_CHAN[0], _PL_CHAN[0].replace(">=", ">"), ["pl_m2_loi_goi"]),
    "pl_m2_bo_so_head": ('    if a.head != st["reviewing_head_sha"]:\n', "    if False:\n", ["pl_m2_loi_goi"]),
    "pl_m2_bo_kiem_trung": (' or any(g["run_id"]', ' or False and any(g["run_id"]', ["pl_m2_loi_goi"]),
    "pl_m3_codex_call_tuy_chon": ("    if _la_codex(st):\n", "    if _la_codex(st) and a.codex_call:\n", ["pl_m3_neo_loi_goi"]),
    "pl_m3_bo_co_da_dung": ('        if goi["da_dung"]:\n', "        if False:\n", ["pl_m3_neo_loi_goi"]),
    "pl_m3_bo_so_head_loi_goi": ('        if goi["head"] != a.reviewed_sha:\n', "        if False:\n", ["pl_m3_neo_loi_goi"]),
    "pl_m3_kich_ca_khi_approve": ('    if a.verdict != "approve":', "    if True:", ["pl_m3_vong", "pl_m3_codex"]),
    "pl_m3_bo_truc_vong": (_PL_VONG, _PL_VONG.replace("in r", "in [*r").replace("())", "())][:1]"), ["pl_m3_vong"]),
    "pl_m3_chi_xet_truc_vong": (_PL_VONG, _PL_VONG.replace("in r", "in [*r").replace("())", "())][1:]"), ["pl_m3_codex"]),
    "pl_c12_thu_tu_truc": (_PL_VONG, _PL_VONG.replace("reversed(TRUC_TRAN.items())", "TRUC_TRAN.items()"), ["pl_m3_codex"]),
    "pl_m4_danh_sach_cam": ('ai_nang or "").strip() not in NGUOI', 'ai_nang or "").strip() in ("claude", "codex", "") or 0 in NGUOI', ["pl_m4_nang_tran"]),
    "pl_m2_bo_kiem_reviewer_codex": ("    if not _la_codex(st):  # connector P2", "    if False:  # connector P2", ["pl_m2_loi_goi"]),
    "pl_m4_tran_moi_bang": ("if a.tran_moi <= st[t]", "if a.tran_moi < st[t]", ["pl_m4_nang_tran"]),
    "pl_m4_can_cu_long": ("#issuecomment-[0-9]+\\Z", "(#issuecomment-[0-9]+)?\\Z", ["pl_m4_nang_tran"]),
    "pl_c12_can_cu_doan": ("[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+/(issues|pull)/[0-9]+#issuecomment-[0-9]+\\Z", "[^/]+/[^/]+/(issues|pull)/[0-9]+#issuecomment-[0-9]+$", ["pl_m4_nang_tran"]),
    "pl_m5_mo_khong_can_nang": (" and st[t] > st[u] and any(", " and st[t] >= 0 and any(", ["pl_m5_rescue"]),
    "pl_f12_bo_so_nang": (' and any(type(n) is dict and n.get("truc") == st["truc"] and n.get("tran_moi") == st[t] and type(n.get("tran_cu")) is int and n["tran_cu"] < st[t] and n.get("ai_nang") in NGUOI_CO_THAM_QUYEN and bool(CAN_CU_RE.match(str(n.get("can_cu")))) for n in st["nang_tran"])', "", ["pl_m5_rescue"]),
    "pl_c11_bo_hinh_nang": (' and type(n.get("tran_cu")) is int and n["tran_cu"] < st[t] and n.get("ai_nang") in NGUOI_CO_THAM_QUYEN and bool(CAN_CU_RE.match(str(n.get("can_cu"))))', "", ["pl_m5_rescue"]),
    "pl_c11_bo_chan_vuot_vong": ('    if st["review_rounds_used"] >= st["review_rounds_limit"]:  #', "    if False:  #", ["pl_m3_vong"]),
    "pl_m5_quyet_dinh_khac_mo": ('mo = (nang := a.quyet_dinh == "nang_tran") and', 'mo = not (nang := a.quyet_dinh == "nang_tran") or', ["pl_m5_rescue"]),
    "pl_m5_bo_kiem_ly_do": (' or st.get("ly_do") != "rescue_required":', ":", ["pl_m5_rescue"]),
    "pl_m5_them_blocked_running": ('    "blocked": (),\n', '    "blocked": ("running",),\n', ["pl_m5_rescue"]),
    "pl_m6_suy_used_0": (("codex_review_calls_used=can_duoi,", " >= can_duoi + sum("), ("codex_review_calls_used=0,", " >= 0 + sum("), ["pl_m6_state_v1"]),  # phối hợp: gỡ cận dưới reader để đo đúng fail-open lời gọi M6
    "pl_m6_state_cu_mat_ho": ('.get("model_family", "openai")', '.get("model_family")', ["pl_m6_state_v1"]),
})


# --- #812 MAY-ADR-0054-a r2: mỗi ca dựng baseline DƯƠNG đầy đủ (kho git + origin bare, lease đã đẩy, validator canon + nguồn của nó
# trên origin/master, biên nhận H THẬT: verdict blob trong git, băm đúng) rồi đổi ĐÚNG một yếu tố. Mẫu kho dựng MỘT lần mỗi biến thể.
_R812_MAU: dict = {}
_g = lambda cwd, *a: subprocess.run(["git", *a], cwd=cwd, capture_output=True, text=True, check=True).stdout.strip()  # noqa: E731
_R812_LEASE = {"schema_version": 2, "event": "executor_lease_granted", "packet_issue": 55, "packet_id": "wp55", "mission_issue": 54, "revision": 1,
               "generation": 1, "lease_id": "wp55-r1-g1-claude", "role": "executor", "provider": "claude", "executor": "claude", "model": "claude-opus-5-5",
               "model_family": "claude", "execution_surface": "claude_code", "transport": "machine/local", "environment": "cloud", "reviewer": "codex",
               "reviewer_model_family": "openai", "reviewer_execution_surface": "codex_cli", "reviewer_transport": "machine", "access": "read-write",
               "assurance_target": "cross_approved", "review_class": "sensitive", "effective_review_class": "sensitive", "spec_path": "ops/specs/wp55.md",
               "prompt_path": "ops/specs/wp55-prompt.md", "write_set": ["x/a.py"], "branch": "agent/wp55-g1-claude", "granted_by": "ducthangho",
               "leased_at_utc": "2026-10-18T07:58:00Z", "granted_on_instruction": "https://github.com/o/r/issues/55#issuecomment-5281636040",
               "heartbeat_at": "2026-10-18T07:58:00Z"}


def _kho812(c: Ctx, bien: str = "") -> Path:
    """Biến thể: khong_kich_hoat · spec_lech · cuc_bo · h_hong · giu_khac · nong · hai_dong · thieu_nguon · rc_falsy · oid_khong_chua ·
    oid_khong_dua_vao · oid_ngoai_fp (ba phép đo land-OID, mỗi biến thể làm hỏng đúng MỘT phép)."""
    if bien not in _R812_MAU:
        goc, R = Path(tempfile.mkdtemp(prefix="r812-")), HERE.parent.parent
        w = goc / "w"
        _g(goc, "init", "-q", "--bare", "o.git"), _g(goc, "init", "-q", "-b", "master", "w"), _g(w, "remote", "add", "origin", "../o.git")

        def ghi(nd, msg):
            for p, b in nd.items():
                (w / p).parent.mkdir(parents=True, exist_ok=True), (w / p).write_bytes(b if isinstance(b, bytes) else b.encode())
            return [_g(w, "add", "-A"), _g(w, "commit", "-qm", msg), _g(w, "rev-parse", "HEAD")][-1]
        pr = (R / "docs/PROTOCOL_DA_PHIEN.md").read_text(encoding="utf-8")
        B0 = ghi({**{p: (R / p).read_bytes() for p in ("ops/lease_publish.py", "ops/bien_nhan_v2.py", ".claude/dev/launcher.py", "AGENTS.md")},
                  **({"AGENTS.md": "# rong\n"} if bien == "thieu_nguon" else {})}, "base")  # `thieu_nguon`: validator đọc được tệp nhưng nguồn luật hỏng
        adr = {"docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md": "x\n"}
        if bien == "oid_ngoai_fp":  # commit đưa ADR vào nằm ở nhánh phụ, master chỉ thấy qua merge --no-ff ⇒ ngoài chuỗi first-parent
            L = [_g(w, "checkout", "-qb", "phu"), ghi(adr, "adr54 phu"), _g(w, "checkout", "-q", "master"), _g(w, "merge", "-q", "--no-ff", "-m", "m", "phu")][1]
        else:
            L = ghi(adr, "adr54")
            L = {"oid_khong_dua_vao": ghi({"docs/z.md": "z\n"}, "noop"), "oid_khong_chua": B0}.get(bien, L)
        spec = f"# spec\nluat_push_va_dung_va: ADR-0054@{L}\n" * (2 if bien == "hai_dong" else 1)
        V = ghi({"ops/specs/wp55.md": spec, "ops/specs/wp55-prompt.md": "prompt\n", "ops/reviews/v.md": "Verdict: approve\n", "docs/PROTOCOL_DA_PHIEN.md": pr.replace("chưa kích hoạt", "đã kích hoạt"),
                 **({} if bien == "khong_kich_hoat" else {"docs/adr/0099-kich-hoat-adr-0054.md": "kích hoạt `ADR-0054`\n"})}, "act")
        sh, han = __import__("hashlib").sha256(spec.encode()).hexdigest(), time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime(time.time() + 6 * 3600))
        lease = {**_R812_LEASE, "spec_hash": sh, "prompt_sha256_required": __import__("hashlib").sha256(b"prompt\n").hexdigest(), "base_sha": L, "reviewed_sha_required": L, "lease_until": han,
                 "lease_expires_at_utc": han, **({"required_checks": False} if bien == "rc_falsy" else {})}
        if bien == "h_hong":  # validator canon từ chối (thiếu lớp review hiệu lực) — mọi phép kiểm khác của packet_loop vẫn qua
            del lease["effective_review_class"]
        _g(w, "push", "-q", "origin", "master"), _g(w, "checkout", "-qb", "ops/wp55-spec")
        ghi({"ops/leases/l.yaml": json.dumps(lease), **({"ops/specs/wp55.md": spec + "lech\n"} if bien == "spec_lech" else {}),
             **({"ops/leases/k.yaml": json.dumps({**lease, "lease_id": "wp55-r1-g1-khac"})} if bien == "giu_khac" else {})}, "lease")
        # `cuc_bo`: lease CHỈ ở ref cục bộ — ref theo dõi remote GIẢ (update-ref), máy chủ không có nhánh.
        _g(w, *(("update-ref", "refs/remotes/origin/ops/wp55-spec", "HEAD") if bien == "cuc_bo" else ("push", "-q", "origin", "ops/wp55-spec")))
        _g(w, "checkout", "-q", "-b", "agent/wp55-g1-claude", "master"), ghi({"x/a.py": "a = 1\n"}, "code")
        _g(w, "push", "-q", "origin", "agent/wp55-g1-claude"), _g(w, "checkout", "-q", "master"), _g(w, "branch", "-q", "-D", "ops/wp55-spec", "agent/wp55-g1-claude")
        if bien == "nong":
            (w / ".git" / "shallow").write_text(_g(w, "rev-parse", "master~2") + "\n")
        _R812_MAU[bien] = (goc, V)
    __import__("shutil").copytree(_R812_MAU[bien][0], c.tmp / f"kho{bien}", symlinks=True)
    return c.tmp / f"kho{bien}" / "w"


def _bn812(w: Path, h: str, sh: str, lop=(), bn=None) -> dict:
    v = _R812_MAU[next(k for k, (g, _) in _R812_MAU.items() if w.parent.name == f"kho{k}")][1]
    bn = {k: x.format(V=v) if isinstance(x, str) else x for k, x in (bn or {}).items()}
    return {"schema_version": 2, "receipt_id": "r1", "packet_issue": 55, "generation": 1, "lease_id": "wp55-r1-g1-claude", "role": "reviewer", "reviewed_sha": h,
            "spec_hash": sh, "verdict": "approve", "assurance": "cross_approved", "executor_provider": "claude", "verdict_path": "ops/reviews/v.md",
            "verdict_sha256": __import__("hashlib").sha256(b"Verdict: approve\n").hexdigest(), "evidence_url": f"https://github.com/o/r/blob/{v}/ops/reviews/v.md",
            "github_submitter_identity": None, "anchor": {"loai": "canonical_ancestry", "cuong_do": "x"}, "bang_lop": [{"slug": s, "hang": g} for s, g in lop],
            "model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": "s1"}, **(bn or {})}


def _r812(c: Ctx, den: str, bien="", comment=True, bn=None, lop=(), verdict="approve", ids=(), env=None, truoc_lease=None, rv=()):
    """Baseline dương tới `den` (lease · review); mỗi tham số đổi ĐÚNG một yếu tố. Trả (rc, sd, err, bytes state NGAY TRƯỚC bước cuối)."""
    w, sd, f = _kho812(c, bien), c.sd(), c.tmp
    buoc = lambda *l: (lambda truoc: (*run(c.script, [l[0], "--packet", 55, *l[1:], "--root", w], sd, env)[::2], truoc))((sd / "wp55.json").read_bytes())  # noqa: E731
    _doi(0, *c.init(sd, lease=False)[::2], "init")
    (f / "cm.json").write_text(json.dumps([{"user": {"login": "github-actions[bot]"}, "body": "```yaml\nlease_id: wp55-r1-g1-claude\n```",
                                            "issue_url": "https://api.github.com/repos/o/r/issues/55"}][:int(comment)]))
    (truoc_lease or (lambda w: None))(w)
    rc, e, truoc = buoc("record-lease", "--lease-ref", "origin/ops/wp55-spec", "--lease-path", "ops/leases/l.yaml", "--lease-comments", f / "cm.json")
    if den == "lease" or rc:
        return rc, sd, e, truoc
    c.den_reviewing(sd, 55, 1, head=(h := _g(w, "rev-parse", "refs/remotes/origin/agent/wp55-g1-claude")))
    (f / "bn.yaml").write_text(__import__("yaml").safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], lop, bn)))
    _doi(0, *run(c.script, ["record-codex-call", "--packet", 55, "--head", h, "--run-id", "g1"], sd)[::2], "codex-call")
    rc, e, truoc = buoc("record-review", "--provider", "codex", "--verdict", verdict, "--reviewed-sha", h, "--codex-call", "g1", "--bien-nhan", f / "bn.yaml",
                        *(x for i in ids for x in ("--finding-id", i)), *rv)
    return rc, sd, e, truoc


def _r812_ca(den, rc_doi, muon=None, **doi):
    """rc đúng; ca dương kiểm `muon`, ca âm đòi state giữ nguyên TỪNG BYTE so với ảnh ngay trước bước bị từ chối (I4)."""
    def ca(c):
        rc, sd, e, truoc = _r812(c, den, **doi)
        _doi(rc_doi, rc, e, f"r812 {den} {sorted(doi)}")
        if muon:
            _kiem(sd, f"r812 {den} {sorted(doi)}", **muon)
        elif (sd / "wp55.json").read_bytes() != truoc:
            raise AssertionError(f"I4: state đổi sau khi {den} từ chối")
    return ca


def _r812_ca_posix(ca):
    """Đo hành vi trên MỌI nền, nhưng trên Windows khai BỎ QUA sau khi đo: `Path.resolve()` của Windows tự hiểu `\\`
    nên đột biến `r812_bo_dau_cheo_nguoc` TƯƠNG ĐƯƠNG ở đó (run 39729983506 · 5618020: VẪN XANH) — chỉ POSIX phân biệt được."""
    def bao(c):
        ca(c)
        if os.name == "nt":
            raise BoQua("đột biến bỏ thay dấu chéo ngược tương đương trên Windows") from OSError("Path Windows nhận cả hai dấu chéo")
    return bao


def case_r812_duong_cu_luon_false(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd, lease=False)[::2], "init")
    _kiem(sd, "init chưa có lease", state="awaiting_lease")
    _doi(0, *c.cap_lease(sd)[::2], "Ctx.cap_lease")
    if _st(sd)["luat_adr0054"] is not False or _st(sd)["state"] != "leased":
        raise AssertionError("đường cũ phải đưa về leased với luat_adr0054: false")
    _doi(8, *c.cap_lease(sd)[::2], "gọi lại đường cũ")


def case_r812_true_khong_quay_ve_duong_cu(c: Ctx):
    rc, sd, e, _ = _r812(c, "lease")
    _doi(0, rc, e, "lease đường mới")
    truoc = (sd / "wp55.json").read_bytes()
    _doi(8, *c.cap_lease(sd)[::2], "đường cũ khi chế độ đã true")
    if (sd / "wp55.json").read_bytes() != truoc:
        raise AssertionError("I4: state đổi")


def case_r812_cua_khep_luot_van_chay(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd, extra=("--attempts-limit", 1))[::2], "init trần 1")
    c.den_reviewing(sd, 55, 1)
    _doi(8, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)[::2], "chạm trần, lượt đang mở")
    _doi(0, *c.review(sd, 55, ["x"])[::2], "cửa KHÉP lượt đang mở vẫn chạy")
    truoc = (sd / "wp55.json").read_bytes()  # I4: đầu vào hỏng (ảnh doctor không có) ở trần ⇒ từ chối, state nguyên byte
    _doi(10, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR, "--bang-chung-moi-truong", c.tmp / "khong-co.json"], sd)[::2], "đầu vào hỏng ở trần")
    if (sd / "wp55.json").read_bytes() != truoc:
        raise AssertionError("I4: begin-attempt ghi state trước khi kiểm đầu vào")
    _doi(3, *run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)[::2], "mở lượt mới ở trần")


def case_r812_executor_antigravity_hop_le(c: Ctx):
    """I8: họ executor theo `model_family` lease khai (gemini), không theo họ mặc định của tên provider."""
    w = _kho812(c)
    spec = importlib.util.spec_from_file_location("pl812_ag", c.script)
    sys.path.insert(0, str(c.script.parent))
    spec.loader.exec_module(m := importlib.util.module_from_spec(spec))
    nc = m._ngu_canh_lease({**_R812_LEASE, "provider": "google_antigravity", "model_family": "gemini", "execution_surface": "antigravity",
                            "spec_hash": "s" * 64}, "origin/x", "0" * 40, "l.yaml", "o/r")
    h = _g(w, "rev-parse", "refs/remotes/origin/agent/wp55-g1-claude")
    (c.tmp / "ag.yaml").write_text(__import__("yaml").safe_dump(_bn812(w, h, "s" * 64, bn={
        "executor_provider": "google_antigravity", "model_executor_identity": {"model_family": "gemini", "model_evidence": "do_may", "model_evidence_ref": "r"}})))
    try:  # `_die` là SystemExit — không để nó thoát khỏi bộ chạy
        kq = m._du_dieu_kien_approve({"packet": 55, "ngu_canh_lease": nc}, __import__("argparse").Namespace(
            bien_nhan=c.tmp / "ag.yaml", root=w, verdict="approve", reviewed_sha=h, finding_id=None))
    except SystemExit as ex:
        raise AssertionError(f"antigravity/gemini hợp lệ phải đạt, được rc={ex.code}") from None
    if kq["p3"] != []:
        raise AssertionError(f"antigravity/gemini hợp lệ phải đạt: {kq}")


def _r812_doi_lease(w, doi, them=None):
    """Đổi lease (và thêm lease khác) trên nhánh ops của fixture rồi đẩy — mỗi ca đổi ĐÚNG một yếu tố."""
    import yaml
    _g(w, "checkout", "-qb", "ops/wp55-spec", "refs/remotes/origin/ops/wp55-spec")
    lease = {**yaml.safe_load((w / "ops/leases/l.yaml").read_bytes()), **doi}
    (w / "ops/leases/l.yaml").write_text(yaml.safe_dump(lease))
    for ten, nd in (them(lease) if them else {}).items():
        (w / "ops/leases" / ten).write_text(yaml.safe_dump(nd))
    _g(w, "add", "-A"), _g(w, "commit", "-qm", "doi lease"), _g(w, "push", "-q", "origin", "ops/wp55-spec"), _g(w, "checkout", "-q", "master")
    _g(w, "branch", "-q", "-D", "ops/wp55-spec")


def _r812_tran_vong(c: Ctx, verdict: str, rc_doi: int, muon=None):
    """State ADR-0054 ở TRẦN VÒNG (sổ nhất quán: một review cũ), rồi chạy cửa khép lượt đang mở."""
    rc, sd, e, raw = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    st = json.loads(raw)
    st.update(review_rounds_limit=1, review_rounds_used=1, codex_review_calls_used=2, reviews=[{
        "attempt": 1, "provider": "codex", "verdict": "changes_requested", "reviewed_sha": st["reviewing_head_sha"], "finding_ids": [], "finding_descs": []}])
    (sd / "wp55.json").write_text(json.dumps(st))
    truoc = (sd / "wp55.json").read_bytes()
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex", "--verdict", verdict, "--reviewed-sha", st["reviewing_head_sha"],
                              "--codex-call", "g1", "--bien-nhan", c.tmp / "bn.yaml", "--root", c.tmp / "kho/w"], sd)
    _doi(rc_doi, rc, e, f"cửa khép ADR-0054 ở trần vòng ({verdict})")
    if muon:
        _kiem(sd, "đã ghi kết quả", **muon)
    elif (sd / "wp55.json").read_bytes() != truoc:
        raise AssertionError("I4: đầu vào hỏng ở trần vòng mà state đổi")


def case_r812_don_thu_muc_tam(c: Ctx):
    (t := c.tmp / "tmpd").mkdir()
    rc, sd, e, _ = _r812(c, "review", env={"TMPDIR": str(t)})
    _doi(0, rc, e, "chuỗi lease → review")
    if list(t.glob("pl812-canon-*")):
        raise AssertionError(f"thư mục canon tạm không được dọn: {list(t.iterdir())}")


def case_r812_ngu_canh_long_sai_hinh(c: Ctx):
    rc, sd, e, _ = _r812(c, "lease")
    _doi(0, rc, e, "lease đường mới")
    st = _st(sd)
    st["ngu_canh_lease"]["reviewer"] = {}
    (sd / "wp55.json").write_text(json.dumps(st))
    _doi(8, *run(c.script, ["status", "--packet", 55], sd)[::2], "ngữ cảnh lồng sai hình dạng ⇒ state hỏng, không traceback")


def case_r812_executor_ag_qua_cli(c: Ctx):
    """I8 qua CLI đầy đủ, băm thật: executor Antigravity khai họ `gemini` rồi `openai` (biên nhận khai họ canon `gpt`) ⇒ approved_pending."""
    import yaml
    for ho, ho_bn in (("gemini", "gemini"), ("openai", "gpt")):
        (d := c.tmp / ho).mkdir()
        w, sd = _kho812(cc := Ctx(c.script, d)), cc.sd()
        _r812_doi_lease(w, {"provider": "google_antigravity", "executor": "google_antigravity", "model_family": ho, "execution_surface": "antigravity",
                            "reviewer": "claude", "reviewer_model_family": "claude", "reviewer_execution_surface": "claude_code", "reviewer_transport": "machine/local"})
        _doi(0, *cc.init(sd, executor="google_antigravity", reviewer="claude", lease=False, extra=(
            "--executor-model-family", ho, "--executor-execution-surface", "antigravity", "--executor-transport", "machine/local"))[::2], "init AG")
        (d / "cm.json").write_text(json.dumps([{"user": {"login": "github-actions[bot]"}, "body": "lease_id: wp55-r1-g1-claude",
                                                "issue_url": "https://api.github.com/repos/o/r/issues/55"}]))
        h = _g(w, "rev-parse", "refs/remotes/origin/agent/wp55-g1-claude")
        for args in (["record-lease", "--lease-ref", "origin/ops/wp55-spec", "--lease-path", "ops/leases/l.yaml", "--lease-comments", d / "cm.json", "--root", w],
                     ["begin-attempt", "--provider", "google_antigravity", "--model-family", ho, "--execution-surface", "antigravity", "--transport", "machine/local"],
                     ["record-post", "--for", "reviewing", "--comment-id", "9000055002"],
                     ["transition", "--to", "reviewing", "--comment-id", "9000055002", "--head-sha", h]):
            _doi(0, *run(c.script, [args[0], "--packet", 55, *args[1:]], sd)[::2], f"AG/{ho} {args[0]}")
        (d / "bn.yaml").write_text(yaml.safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], bn={
            "executor_provider": "google_antigravity", "model_executor_identity": {"model_family": ho_bn, "model_evidence": "do_may", "model_evidence_ref": "r"},
            "model_reviewer_identity": {"provider": "anthropic_claude", "surface": "claude_code", "transport": "machine/local", "session_run_id": "s"}})))
        _doi(0, *run(c.script, ["record-review", "--packet", 55, "--provider", "claude", "--verdict", "approve", "--reviewed-sha", h,
                                "--bien-nhan", d / "bn.yaml", "--root", w], sd)[::2], f"AG/{ho} H hợp lệ")
        _kiem(sd, f"AG/{ho}", state="approved_pending")


def case_r812_canon_vang_phu_thuoc(c: Ctx):
    rc, sd, e, truoc = _r812(c, "lease", truoc_lease=lambda w: [_g(w, "rm", "-q", "AGENTS.md"), _g(w, "commit", "-qm", "rm"), _g(w, "push", "-q", "origin", "master")])
    _doi(8, rc, e, "validator canon vắng phụ thuộc trên origin/master")
    if (sd / "wp55.json").read_bytes() != truoc:
        raise AssertionError("I4: state đổi")


def case_r812_r4_yaml_deep(c: Ctx):
    def mutate(w):
        import yaml
        _g(w, "checkout", "-qb", "ops/wp55-spec", "refs/remotes/origin/ops/wp55-spec")
        p = w / "ops/leases/l.yaml"
        l = yaml.safe_load(p.read_bytes())
        p.write_text(yaml.safe_dump(l) + "extra: " + "[" * 700 + "0" + "]" * 700 + "\n")
        _g(w, "add", "-A"), _g(w, "commit", "-qm", "nested ordinary metadata"), _g(w, "push", "-q", "origin", "ops/wp55-spec")
        _g(w, "checkout", "-q", "master"), _g(w, "branch", "-q", "-D", "ops/wp55-spec")
    _r812_ca("lease", 2, truoc_lease=mutate)(c)


def case_r812_r4_symlink_scope(c: Ctx):
    def mutate(w, conflict):
        (w / "x").mkdir()
        (w / "x/a.py").write_text("a = 1\n")
        (w / "alias").symlink_to("x", target_is_directory=True)
        assert (w / "alias/a.py").resolve() == (w / "x/a.py").resolve()
        # Windows (run 39729983506): Git for Windows mặc định `core.symlinks=false` nên `add` chép `alias/` thành thư mục
        # thường — cây không còn symlink, `alias/a.py` là tệp KHÁC, rc 0 là đúng với cây ấy. Bật cờ cho kho fixture, rồi ĐO.
        _g(w, "config", "core.symlinks", "true")
        _g(w, "add", "-A"), _g(w, "commit", "-qm", "alias inside fixture"), _g(w, "push", "-q", "origin", "master")
        if not _g(w, "ls-tree", "HEAD", "alias").startswith("120000 "):
            raise BoQua("nền không ghi được symlink vào cây Git") from OSError(_g(w, "ls-tree", "HEAD", "alias"))
        _r812_doi_lease(w, {}, (lambda l: {"other.yaml": {**l, "lease_id": "other-lease", "write_set": ["alias/a.py"]}}) if conflict else None)
    for conflict in (False, True):
        (d := c.tmp / str(conflict)).mkdir()
        _r812_ca("lease", 7 if conflict else 0, None if conflict else {"state": "leased"},
                 truoc_lease=lambda w: mutate(w, conflict))(Ctx(c.script, d))


def case_r812_r4_context_executor_surface(c: Ctx):
    rc, sd, e, before = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    st = json.loads(before)
    st["ngu_canh_lease"]["executor"]["execution_surface"] = []
    (sd / "wp55.json").write_text(json.dumps(st))
    raw = (sd / "wp55.json").read_bytes()
    _doi(8, *run(c.script, ["status", "--packet", 55], sd)[::2], "context sai kiểu")
    if raw != (sd / "wp55.json").read_bytes():
        raise AssertionError("I4: state đổi")



def _r812_r5_canon_hong_sau_lease(c: Ctx):
    rc, sd, e, before = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    (sd / "wp55.json").write_bytes(before)
    w = c.tmp / "kho/w"
    (w / "AGENTS.md").write_text("# nguồn hỏng\n")
    _g(w, "add", "AGENTS.md"), _g(w, "commit", "-qm", "source invalid after valid lease")
    _g(w, "push", "-q", "origin", "master"), _g(w, "fetch", "-q", "origin")
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex", "--verdict", "approve",
        "--reviewed-sha", json.loads(before)["reviewing_head_sha"], "--codex-call", "g1", "--bien-nhan", c.tmp / "bn.yaml", "--root", w], sd)
    _doi(11, rc, e, "review không được dùng nguồn canon hỏng")
    if (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: state đổi")

_R812_KHAC = lambda **x: lambda w: _r812_doi_lease(w, {}, lambda l: {"other.yaml": {**l, "lease_id": "other-lease", **x}})  # noqa: E731
_R812_XOA_DAC_TA = lambda w: [(w / p).unlink() for p in ("ops/specs/wp55.md", "ops/specs/wp55-prompt.md")]  # noqa: E731 — vắng ở worktree, có tại lease OID
CASES += [(n[5:], f) for n, f in list(globals().items()) if n.startswith("case_r812_")] + [
    ("r812_duong_moi_du_dieu_kien", _r812_ca("review", 0, {"state": "approved_pending", "luat_adr0054": True})),
    ("r812_dac_ta_chi_tai_lease_oid", _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True}, truoc_lease=_R812_XOA_DAC_TA)),
    ("r812_khong_kich_hoat_la_false", _r812_ca("review", 0, {"state": "accepted", "luat_adr0054": False}, bien="khong_kich_hoat")),
    ("r812_nong_la_false", _r812_ca("lease", 0, {"luat_adr0054": False}, bien="nong")),
    ("r812_hai_dong_khai_la_false", _r812_ca("lease", 0, {"luat_adr0054": False}, bien="hai_dong")),
    ("r812_lease_chi_o_ref_cuc_bo", _r812_ca("lease", 7, bien="cuc_bo")),
    ("r812_dac_ta_lech_bam", _r812_ca("lease", 2, bien="spec_lech")),
    ("r812_lease_chua_comment_workflow", _r812_ca("lease", 7, comment=False)),
    ("r812_lease_h_hong", _r812_ca("lease", 7, bien="h_hong")),
    ("r812_nguoi_giu_khac", _r812_ca("lease", 7, bien="giu_khac")),
    ("r812_required_checks_falsy", _r812_ca("lease", 2, bien="rc_falsy")),
    ("r812_canon_thieu_nguon", _r812_r5_canon_hong_sau_lease),
    ("r812_approve_kem_lop_p1", _r812_ca("review", 11, lop=(("a-b", "P1"),))),
    ("r812_hang_px", _r812_ca("review", 11, lop=(("a-b", "PX"),))),
    ("r812_slug_xuong_dong", _r812_ca("review", 11, lop=(("a-b\n", "P3"),))),
    ("r812_verdict_blob_khong_co", _r812_ca("review", 11, bn={"verdict_sha256": "b" * 64})),
    ("r812_bien_nhan_lech_surface", _r812_ca("review", 11, bn={"model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_desktop", "transport": "machine", "session_run_id": "s1"}})),
    ("r812_bien_nhan_lech_transport", _r812_ca("review", 11, bn={"model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_cli", "session_run_id": "s1"}})),
    ("r812_bien_nhan_lech_generation", _r812_ca("review", 11, bn={"generation": 2})),
    ("r812_bien_nhan_lech_packet", _r812_ca("review", 11, bn={"packet_issue": 56})),
    ("r812_bien_nhan_lech_spec_hash", _r812_ca("review", 11, bn={"spec_hash": "c" * 64})),
    ("r812_verdict_changes_requested", _r812_ca("review", 11, bn={"verdict": "changes_requested"})),
    ("r812_verdict_blocked", _r812_ca("review", 11, bn={"verdict": "blocked"})),
    ("r812_slug_ngoai_bang_lop", _r812_ca("review", 11, bn={"verdict": "changes_requested"}, lop=(("a-b", "P2"),), verdict="changes_requested", ids=("a-b", "tu-dat"))),
    ("r812_oid_khong_chua_adr", _r812_ca("lease", 0, {"luat_adr0054": False}, bien="oid_khong_chua")),
    ("r812_oid_khong_dua_adr_vao", _r812_ca("lease", 0, {"luat_adr0054": False}, bien="oid_khong_dua_vao")),
    ("r812_oid_ngoai_first_parent", _r812_ca("lease", 0, {"luat_adr0054": False}, bien="oid_ngoai_fp")),
    ("r812_bia_mo_hai_chieu_tai_lease_oid", _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True}, truoc_lease=lambda w: _r812_doi_lease(
        w, {"thay_the_cho": ["old-lease"]}, lambda l: {"old.yaml": {**l, "lease_id": "old-lease", "thay_the_cho": [], "da_bi_thay_the": l["lease_id"]}}))),
    ("r812_nguoi_giu_prefix_giao_nhau", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {}, lambda l: {"other.yaml": {**l, "lease_id": "other-lease", "write_set": ["x/"]}}))),
    ("r812_nguoi_giu_effective_giao_nhau", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {}, lambda l: {"other.yaml": {**l, "lease_id": "other-lease", "write_set": ["y/b.py"], "effective_write_set": ["y/b.py", "x/a.py"]}}))),
    ("r812_nguoi_giu_planned_hop_le", _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True}, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["planned:x/a.py"]}))),
    ("r812_model_family_falsy", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"model_family": False}))),
    ("r812_lease_role_sai", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"role": "reviewer"}))),
    ("r812_lease_generation_khong_duong", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"generation": 0}))),
    ("r812_lease_assurance_ngoai_mien", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"assurance_target": "advisory_review"}))),
    ("r812_prompt_path_thu_muc", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"prompt_path": "."}))),
    ("r812_provider_bi_danh_canon", _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True}, truoc_lease=lambda w: _r812_doi_lease(
        w, {"provider": "anthropic_claude", "executor": "anthropic_claude"}))),
    ("r812_executor_provider_lech_lease", _r812_ca("review", 11, bn={"executor_provider": "google_antigravity", "model_executor_identity": {
        "model_family": "claude", "model_evidence": "do_may", "model_evidence_ref": "r"}})),
    ("r812_executor_surface_lech_lease", _r812_ca("review", 11, bn={"model_executor_identity": {"surface": "antigravity"}})),
    ("r812_schema_h_bat_buoc", _r812_ca("review", 11, bn={"github_submitter_identity": False})),
    ("r812_verdict_path_khong_ton_tai", _r812_ca("review", 11, bn={"verdict_path": "ops/reviews/khong.md", "evidence_url": "https://github.com/o/r/blob/{V}/ops/reviews/khong.md"})),
    ("r812_tran_vong_cua_khep_ghi_ket_qua", lambda c: _r812_tran_vong(c, "approve", 0, {"state": "approved_pending", "review_rounds_used": 2, "attempt_open": False})),
    ("r812_tran_vong_dau_vao_hong_khong_ghi", lambda c: _r812_tran_vong(c, "blocked", 11)),
    ("r812_nguoi_giu_hoa_thuong", _r812_ca("lease", 7, truoc_lease=_R812_KHAC(write_set=["X/"]))),
    ("r812_nguoi_giu_dau_cheo_nguoc", _r812_ca_posix(_r812_ca("lease", 7, truoc_lease=_R812_KHAC(write_set=["x\\a.py"])))),
    ("r812_nguoi_giu_unicode_nfd", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["café/a.py"]}, lambda l: {
        "other.yaml": {**l, "lease_id": "other-lease", "write_set": ["cafe\u0301/"]}}))),
    ("r812_nguoi_giu_cham_gach", _r812_ca("lease", 7, truoc_lease=_R812_KHAC(write_set=["./x/a.py"]))),
    ("r812_effective_mo_rong_hop_le", _r812_ca("lease", 0, {"state": "leased"}, truoc_lease=lambda w: _r812_doi_lease(w, {"effective_write_set": ["x/a.py", "y/b.py"]}))),
    ("r812_lease_branch_rong", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"branch": ""}))),
    ("r812_bien_nhan_provider_sai_kieu", _r812_ca("review", 11, bn={"model_reviewer_identity": {"provider": [], "surface": "codex_cli", "transport": "machine", "session_run_id": "s1"}})),
    ("r812_bien_nhan_family_sai_kieu", _r812_ca("review", 11, bn={"model_reviewer_identity": {"provider": "openai_codex", "surface": "codex_cli", "transport": "machine",
                                                                                              "session_run_id": "s1", "model_family": []}})),
    ("r812_bien_nhan_lech_sha", _r812_ca("review", 11, bn={"reviewed_sha": "{V}"})),
    ("r812_bien_nhan_lech_lease_id", _r812_ca("review", 11, bn={"lease_id": "lease-khac"})),
    ("r812_executor_transport_lech_lease", _r812_ca("review", 11, bn={"model_executor_identity": {"transport": "human"}})),
    ("r812_verdict_am_dung_bang_lop", _r812_ca("review", 0, {"state": "running"}, bn={"verdict": "changes_requested"}, lop=(("a-b", "P2"),),
                                               verdict="changes_requested", ids=("a-b",))),
]
CASES += [
    ("r812_r4_own_union_conflict", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(
        w, {"effective_write_set": ["y/b.py"]}, lambda l: {"other.yaml": {**l, "lease_id": "other-lease", "write_set": ["x/"], "effective_write_set": ["x/"]}}))),
    ("r812_r4_own_dot", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["./x/a.py"]}))),
    ("r812_r4_own_parent", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"effective_write_set": ["x/../y/b.py"]}))),
    ("r812_r4_own_glob", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["x/*.py"]}))),
    ("r812_r4_empty_declared", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": [], "effective_write_set": ["x/a.py"]}))),
    ("r812_r4_top_family", _r812_ca("review", 11, bn={"model_family": []})),
    ("r812_r4_executor_identity", _r812_ca("review", 11, bn={"model_executor_identity": False})),
    ("r812_r4_duplicate_slug", _r812_ca("review", 11, lop=(("a-b", "P3"), ("a-b", "P3")))),
]
MUTANTS.update({
    "r812_bo_so_ls_remote": ('    if xa[0] or gan[0] or xa[1].split() != [oid.encode(), f"refs/heads/{m[1]}".encode()]:\n', "    if gan[0]:\n", ["r812_lease_chi_o_ref_cuc_bo"]),
    "r812_ghi_state_roi_moi_tu_choi": ("        _die(RC_ARG, f\"đặc tả {l['spec_path']}", "        _save(state_dir, {**st, \"state\": \"leased\"}) or _die(RC_ARG, f\"đặc tả {l['spec_path']}", ["r812_dac_ta_lech_bam"]),
    "r812_bo_bam_dac_ta": ('hashlib.sha256(spec).hexdigest() != l["spec_hash"]:', "False:", ["r812_dac_ta_lech_bam"]),
    "r812_bo_comment_workflow": ("    if not any(isinstance(c, dict) and", "    if False and any(isinstance(c, dict) and", ["r812_lease_chua_comment_workflow"]),
    "r812_bo_h_check": ("        if p.returncode:  # I2(H)", "        if False:  # I2(H)", ["r812_lease_h_hong"]),
    "r812_h_check_tren_worktree": ('"--root", str(td / "snap")]', '"--root", str(root)]', ["r812_dac_ta_chi_tai_lease_oid"]),
    "r812_bo_nguoi_giu": (("        if p.returncode != RC_DANG_GIU_LEASE or", "        if giao_nhau:\n            _die(RC_GUARD, f\"I2(Đ): lease khác"), ("        if False and", "        if False:\n            _die(RC_GUARD, f\"I2(Đ): lease khác"), ["r812_nguoi_giu_khac"]),  # phối hợp: hai lớp cùng chặn
    "r812_bo_shallow": ('_git_do(root, "rev-parse", "--is-shallow-repository") == (0, b"false\\n")', "True", ["r812_nong_la_false"]),
    "r812_nhan_nhieu_dong_khai": ("    if len(khai) != 1:", "    if not khai:", ["r812_hai_dong_khai_la_false"]),
    "r812_bo_kich_hoat": ('            and ls[0] == 0 and all(rc == 0 for rc, _ in adr) and len(kich) == 1\n', "", ["r812_khong_kich_hoat_la_false"]),
    "r812_rc_falsy_thanh_rong": ('rc = l.get("required_checks", [])', 'rc = l.get("required_checks") or []', ["r812_required_checks_falsy"]),
    "r812_canon_suy_giam": ("if bnv.PROVIDER_NGUON_HONG is not None or ", "if False or ", ["r812_canon_thieu_nguon"]),
    "r812_bo_neo_git": ("+ neo[0] + neo[1] +", "+", ["r812_verdict_blob_khong_co"]),
    "r812_duong_cu_ghi_true": ('st["luat_adr0054"] = False  # I9', 'st["luat_adr0054"] = None  # I9', ["r812_duong_cu_luon_false"]),
    "r812_bn_chi_cho_approve": ('if st.get("luat_adr0054") is True else None', 'if st.get("luat_adr0054") is True and a.verdict == "approve" else None', ["r812_slug_ngoai_bang_lop"]),
    "r812_approve_cu_cho_adr0054": ('if st.get("luat_adr0054") is True else None', "if False else None", ["r812_approve_kem_lop_p1", "r812_duong_moi_du_dieu_kien"]),
    "r812_bo_chan_p0_p2": ('("con-P0-P2", lop_ok and (', '("con-P0-P2", True or (', ["r812_approve_kem_lop_p1"]),
    "r812_mien_hang_mo": ("\n                                           and x.get(\"hang\") in HANG_LOP for x in lop)", " for x in lop)", ["r812_hang_px"]),
    "r812_slug_match_thay_fullmatch": ('SLUG_RE.fullmatch(x["slug"])', 'SLUG_RE.match(x["slug"])', ["r812_slug_xuong_dong"]),
    "r812_bo_surface": ('("surface", nc[', '("surface", True or nc[', ["r812_bien_nhan_lech_surface"]),
    "r812_bo_transport": ('("transport", nc[', '("transport", True or nc[', ["r812_bien_nhan_lech_transport"]),
    "r812_bo_generation": ('("generation", type(', '("generation", True or type(', ["r812_bien_nhan_lech_generation"]),
    "r812_bo_packet": ('("packet", type(', '("packet", True or type(', ["r812_bien_nhan_lech_packet"]),
    "r812_bo_spec_hash": ('("spec_hash", d.get("spec_hash")', '("spec_hash", True or d.get("spec_hash")', ["r812_bien_nhan_lech_spec_hash"]),
    "r812_verdict_tu_nguoi_goi": ('("verdict", d.get("verdict") == a.verdict)', '("verdict", True)', ["r812_verdict_changes_requested", "r812_verdict_blocked"]),
    "r812_bo_slug_trong_bang": ('("slug-ngoai-bang", lop_ok and', '("slug-ngoai-bang", True or', ["r812_slug_ngoai_bang_lop"]),
    "r812_siet_lop_khong_rong": ("lop_ok = type(lop) is list and all(", "lop_ok = type(lop) is list and bool(lop) and all(", ["r812_duong_moi_du_dieu_kien"]),
    "r812_tran_chan_cua_khep": ('if cua == "begin-attempt" and st["attempts_used"]', 'if cua in ("begin-attempt", "record-review") and st["attempts_used"]', ["r812_cua_khep_luot_van_chay"]),
    "r812_xet_dung_truoc_dau_vao": ('    anh = _kiem_anh_moi_truong(getattr(a, "bang_chung_moi_truong"', '    _xet_dung(state_dir, st, "begin-attempt")\n    anh = _kiem_anh_moi_truong(getattr(a, "bang_chung_moi_truong"', ["r812_cua_khep_luot_van_chay"]),
    "r812_bo_do_chua_adr": ('            and _git_do(root, "cat-file", "-e", f"{oid}:{ADR0054_TEP}")[0] == 0\n', "", ["r812_oid_khong_chua_adr"]),
    "r812_bo_do_dua_vao": ('            and _git_do(root, "cat-file", "-e", f"{oid}^1:{ADR0054_TEP}")[0] != 0\n', "", ["r812_oid_khong_dua_adr_vao"]),
    "r812_bo_do_first_parent": ("            and chuoi[0] == 0 and oid.encode() in chuoi[1].split()\n", "", ["r812_oid_ngoai_first_parent"]),
    "r812_snapshot_khong_git": ('_git_do(root, "worktree", "add", "-q", "--detach", str(td / "snap"), oid)[0]', '(td / "snap").mkdir() or _git_do(root, "archive", oid)[0] and False', ["r812_bia_mo_hai_chieu_tai_lease_oid"]),
    "r812_giao_chi_bang_nhau": ("    return a == b or a.startswith(b + \"/\") or b.startswith(a + \"/\")", "    return a == b", ["r812_nguoi_giu_prefix_giao_nhau"]),
    "r812_bo_effective_nguoi_khac": ('for k in ("write_set", "effective_write_set")', 'for k in ("write_set",)', ["r812_nguoi_giu_effective_giao_nhau"]),
    "r812_bo_quet_giao": ("        if giao_nhau:\n            _die(RC_GUARD, f\"I2(Đ): lease khác", "        if False:\n            _die(RC_GUARD, f\"I2(Đ): lease khác", ["r812_nguoi_giu_prefix_giao_nhau", "r812_nguoi_giu_effective_giao_nhau"]),
    "r812_planned_khong_go": ('"ai-dang-giu", duong.removeprefix("planned:")', '"ai-dang-giu", duong', ["r812_nguoi_giu_planned_hop_le"]),
    "r812_bo_kieu_identity_lease": (' or any(k in l and (type(l[k]) is not str or not l[k].strip()) for k in ten_id)', "", ["r812_model_family_falsy"]),
    "r812_bo_role_lease": (' or l.get("role") != "executor"', "", ["r812_lease_role_sai"]),
    "r812_bo_generation_duong": ((' or l["generation"] < 1', ' and nc["generation"] > 0'), ("", ""), ["r812_lease_generation_khong_duong"]),  # phối hợp: chốt lease + lược đồ state
    "r812_bo_mien_assurance": ('        if l["assurance_target"] not in bnv_lease.ASSURANCE_CAN_DOC_LAP:\n', "        if False:\n", ["r812_lease_assurance_ngoai_mien"]),
    "r812_bo_bi_danh": ('    p = dict(launcher._PROVIDER_BI_DANH).get(p, p)\n    return next(', "    return p or next(", ["r812_provider_bi_danh_canon"]),
    "r812_bo_provider_executor": ('("provider-executor", p_chuan(', '("provider-executor", True or p_chuan(', ["r812_executor_provider_lech_lease"]),
    "r812_bo_surface_executor": ('("executor-surface-transport", all(', '("executor-surface-transport", True or all(', ["r812_executor_surface_lech_lease"]),
    "r812_bo_thieu": ("list(bnv._thieu(d) if d else [])", "list([])", ["r812_schema_h_bat_buoc"]),
    "r812_tran_vong_chan_cua_khep": (' and a is None and st.get("luat_adr0054") is not True:', " and a is None:", ["r812_tran_vong_cua_khep_ghi_ket_qua"]),
    "r812_dung_truoc_H": ("    bn = _du_dieu_kien_approve(st, a) if", '    _xet_dung(state_dir, st, "record-review", a)\n    bn = _du_dieu_kien_approve(st, a) if', ["r812_tran_vong_dau_vao_hong_khong_ghi"]),
    "r812_khong_don_tam": ("        shutil.rmtree(td, ignore_errors=True)", "        pass", ["r812_don_thu_muc_tam"]),
    "r812_nc_chi_tap_khoa": ('_nc_hop_le(st["ngu_canh_lease"])', 'set(st["ngu_canh_lease"]) == set(KHOA_NGU_CANH)', ["r812_ngu_canh_long_sai_hinh"]),
    "r812_bo_casefold": (').casefold()\n    parts', ')\n    parts', ["r812_nguoi_giu_hoa_thuong"]),
    "r812_bo_dau_cheo_nguoc": (('.strip().replace("\\\\", "/")).casefold()', 'q = p.removeprefix("planned:").strip().replace("\\\\", "/")\n',
                                     '.replace("\\\\", "/").split("/"), [], 0'),
                                    (".strip()).casefold()", 'q = p.removeprefix("planned:").strip()\n', '.split("/"), [], 0'), ["r812_nguoi_giu_dau_cheo_nguoc"]),
    "r812_bo_nfc": ('    q = unicodedata.normalize("NFC", p.removeprefix', '    q = (lambda _f, x: x)("NFC", p.removeprefix', ["r812_nguoi_giu_unicode_nfd"]),
    "r812_bo_cham_gach": ('    if "." in q.split("/"):', '    if False:', ["r812_r4_own_dot"]),
    "r812_ai_dang_giu_ca_effective": ('        for duong in l["write_set"]:  # I2(Đ)', "        for duong in ws:  # I2(Đ)", ["r812_effective_mo_rong_hop_le"]),
    "r812_branch_rong_lot": ((' or any(t is str and not l[k].strip() for k, t in kieu.items())', "    if not _nc_hop_le(json.loads(json.dumps(nc))):"), ("", "    if False:"),
                             ["r812_lease_branch_rong"]),  # phối hợp: chốt kiểu lease + lược đồ state trước `_save`
    "r812_bo_kieu_danh_tinh_bn": ("        if kieu_sai:  # có mặt", "        if False:  # có mặt", ["r812_bien_nhan_family_sai_kieu"]),
    "r812_bo_so_sha_bn": ('("reviewed_sha", d.get("reviewed_sha") == a.reviewed_sha)', '("reviewed_sha", True)', ["r812_bien_nhan_lech_sha"]),
    "r812_bo_so_lease_id_bn": ('("lease_id", d.get("lease_id") == nc["lease_id"])', '("lease_id", True)', ["r812_bien_nhan_lech_lease_id"]),
    "r812_bo_transport_executor": ('(("surface", "execution_surface"), ("transport", "transport"))', '(("surface", "execution_surface"),)', ["r812_executor_transport_lech_lease"]),
    "r812_ho_theo_ten_provider": ("    ho = lambda vai: HO_CANON[nc[vai][\"model_family\"]]", "    ho = lambda vai: bnv.HO_MODEL_MAC_DINH.get(bnv._chuan_hoa_provider(nc[vai][\"provider\"]), \"\")",
                                  ["r812_executor_ag_qua_cli", "r812_executor_antigravity_hop_le"]),
    "r812_bo_chan_awaiting": ('    if st["state"] != "awaiting_lease":\n        _die(RC_STATE,\n             f"chỉ ghi', '    if False:\n        _die(RC_STATE,\n             f"chỉ ghi', ["r812_true_khong_quay_ve_duong_cu", "r812_duong_cu_luon_false"]),
})

MUTANTS.update({
    "r812_r4_bo_chan_yaml_sau": ('except (yaml.YAMLError, RecursionError):', 'except yaml.YAMLError:', ["r812_r4_yaml_deep"]),
    "r812_r4_bo_resolve": ('return {ten, _chuan_duong(dich.as_posix())}', 'return {ten}', ["r812_r4_symlink_scope"]),
    "r812_r4_own_chi_effective": ('for x in giu(l)))', 'for x in ws))', ["r812_r4_own_union_conflict"]),
    "r812_r4_bo_glob": ('    if any(c in q for c in "*?[]"):', '    if False:', ["r812_r4_own_glob"]),
    "r812_r4_bo_parent": (' or ".." in parts', '', ["r812_r4_own_parent"]),
    "r812_r4_cho_declared_rong": (' or not l["write_set"]', '', ["r812_r4_empty_declared"]),
    "r812_r4_bo_schema_bn": ('        if kieu_sai:  # có mặt', '        if False:  # có mặt', ["r812_r4_top_family", "r812_r4_executor_identity"]),
    "r812_r4_bo_schema_surface": (('                    and (nc[v]["execution_surface"] is None or type(nc[v]["execution_surface"]) is str',
                                    '                    and (nc[v]["transport"] is None or type(nc[v]["transport"]) is str'),
                                   ('                    and (True or type(nc[v]["execution_surface"]) is str',
                                    '                    and (True or type(nc[v]["transport"]) is str'), ["r812_r4_context_executor_surface"]),
    "r812_r4_bo_unique_slug": ('and len({x["slug"] for x in lop}) == len(lop)', '', ["r812_r4_duplicate_slug"]),
    "r812_r4_init_tu_cap": ('"state": "awaiting_lease",', '"state": "leased",', ["r812_duong_cu_luon_false"]),
    "r812_r4_bo_dep_vang": (('            if rc != 0 or not b:', '        if bnv_lease.PROVIDER_NGUON_HONG is not None:'),
                                 ('            if False:', '        if False:'), ["r812_canon_vang_phu_thuoc"]),
    "r812_r4_bo_neo_path": ('+ neo[0] + neo[1] +', '+', ["r812_verdict_path_khong_ton_tai"]),
    "r812_r4_chan_am_hop_le": ('("slug-ngoai-bang", lop_ok and set(a.finding_id or []) <= {x["slug"] for x in lop})',
                               '("slug-ngoai-bang", lop_ok and not a.finding_id)', ["r812_verdict_am_dung_bang_lop"]),
})
MUTANTS["r812_bo_h_check"][2].append("r812_prompt_path_thu_muc")




def _r812_r5_source_module(w, content):
    (w / "ops/bien_nhan_v2.py").write_text(content)
    _g(w, "add", "ops/bien_nhan_v2.py"), _g(w, "commit", "-qm", "invalid canon module")
    _g(w, "push", "-q", "origin", "master")

# #812 lượt 5: nguồn suy giảm ở lease, mọi nguồn tham chiếu, chuẩn hoá tuple và lỗi argv.
CASES += [
    ("r812_r5_lease_canon_hong", _r812_ca("lease", 8, bien="thieu_nguon")),
    ("r812_r5_source_api_missing", _r812_ca("lease", 8, truoc_lease=lambda w: _r812_r5_source_module(w, "# missing API\n"))),
    ("r812_r5_source_syntax", _r812_ca("lease", 8, truoc_lease=lambda w: _r812_r5_source_module(w, "ordinary invalid syntax\n"))),
    ("r812_r5_instruction_long", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {
        "granted_on_instruction": "https://github.com/o/r/issues/" + "5" * 4400 + "#issuecomment-1"}))),
    ("r812_r5_spec_path_zero", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"spec_path": "ops/specs/wp55\x00.md"}))),
]
for k in ("executor_model_evidence_ref", "executor_telemetry_path", "executor_nguoi_audit", "executor_audit_actor"):
    CASES.append(("r812_r5_nested_" + k, _r812_ca("review", 11, bn={"model_executor_identity": {
        "model_family": "claude", "model_evidence": "do_may", "model_evidence_ref": "r", k: []}})))
for k, val in (("che_do", []), ("KHONG_do_duoc", []), ("phien_doc_lap", "false")):
    CASES.append(("r812_r5_reviewer_" + k, _r812_ca("review", 11, bn={"model_reviewer_identity": {
        "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": "s1", k: val}})))
CASES.append(("r812_r5_session_list", _r812_ca("review", 11, bn={"model_reviewer_identity": {
    "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": [], "phien_doc_lap": True, "KHONG_do_duoc": "ordinary explanation"}})))
for k, val in (("provider", " openai_codex "), ("surface", " codex_cli "), ("transport", " machine ")):
    CASES.append(("r812_r5_padded_" + k, _r812_ca("review", 0, {"state": "approved_pending"}, bn={"model_reviewer_identity": {
        "provider": "openai_codex", "surface": "codex_cli", "transport": "machine", "session_run_id": "s1", k: val}})))
CASES += [
    ("r812_r5_alias_surface", _r812_ca("review", 0, {"state": "approved_pending"}, bn={"model_executor_identity": {"surface": "claude_code_cli", "transport": "machine/local"}})),
    ("r812_r5_prefixed_reference_valid", _r812_ca("review", 0, {"state": "approved_pending"}, bn={"model_executor_identity": {
        "model_family": "claude", "model_evidence": "do_may", "executor_model_evidence_ref": "r"}})),
]
MUTANTS.update({
    "r812_r5_no_loader_guard": ('    except Exception as ex:  # loader canon:', '    except OSError as ex:  # loader canon:', ["r812_r5_source_syntax"]),
    "r812_r5_no_api_guard": ('if ten == "bien_nhan_v2" and any(not hasattr(m, k) for k in api):', 'if False:', ["r812_r5_source_api_missing"]),
    "r812_r5_lease_degraded": ('        if bnv_lease.PROVIDER_NGUON_HONG is not None:', '        if False:', ["r812_r5_lease_canon_hong"]),
    "r812_r5_unbounded_int": ('mr[2].lstrip("0") != str(st["packet"])', 'int(mr[2]) != st["packet"]', ["r812_r5_instruction_long"]),
    "r812_r5_argv_valueerror": ('except (OSError, subprocess.SubprocessError, ValueError):', 'except (OSError, subprocess.SubprocessError):', ["r812_r5_spec_path_zero"]),
    "r812_r5_ignore_bad_attestations": ('        if kieu_sai:  # có mặt', '        if False:  # có mặt',
        ["r812_r5_nested_executor_model_evidence_ref", "r812_r5_reviewer_che_do", "r812_r5_reviewer_phien_doc_lap", "r812_r5_reviewer_KHONG_do_duoc", "r812_r5_session_list"]),
    "r812_r5_raw_provider": ('bnv._chuan_hoa_provider(bnv._chuoi(x) or "")', 'bnv._chuan_hoa_provider(x or "")', ["r812_r5_padded_provider"]),
    "r812_r5_raw_surface": ('bm_chuan(mri.get("surface")) ==', 'mri.get("surface") ==', ["r812_r5_padded_surface"]),
    "r812_r5_raw_transport": ('bnv._chuoi(mri.get("transport")) ==', 'mri.get("transport") ==', ["r812_r5_padded_transport"]),
})

CASES += [
    ("r812_r5_review_role", _r812_ca("review", 11, bn={"role": "executor"})),
    ("r812_r5_review_assurance", _r812_ca("review", 11, bn={"assurance": "same_provider_approved"})),
]
MUTANTS.update({
    "r812_r5_drop_role": ('("role", d.get("role") == "reviewer")', '("role", True)', ["r812_r5_review_role"]),
    "r812_r5_drop_assurance": ('("assurance", d.get("assurance") == nc["assurance_target"])', '("assurance", True)', ["r812_r5_review_assurance"]),
})

# #812 lượt 6: API canon dùng được, lỗi argv/serialization giữ byte, và mỗi thành phần authority/identity có phản chứng riêng.
def _r812_r6_api_lease(w, key):
    p = w / "ops/bien_nhan_v2.py"
    p.write_text(p.read_text() + "\n" + key + " = None\n")
    _g(w, "add", "ops/bien_nhan_v2.py"), _g(w, "commit", "-qm", "invalid canonical API type")
    _g(w, "push", "-q", "origin", "master")


def _r812_r6_comment(c, field):
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline lease H/Đ/R")
    (sd / "wp55.json").write_bytes(before)
    p = c.tmp / "cm.json"
    cm = json.loads(p.read_text())
    if field == "author":
        cm[0]["user"]["login"] = "ordinary-reviewer"
    elif field == "issue":
        cm[0]["issue_url"] = "https://api.github.com/repos/o/r/issues/56"
    else:
        cm[0]["body"] = "lease_id: different-lease"
    p.write_text(json.dumps(cm))
    rc, _, e = run(c.script, ["record-lease", "--packet", 55, "--lease-ref", "origin/ops/wp55-spec", "--lease-path", "ops/leases/l.yaml",
                            "--lease-comments", p, "--root", c.tmp / "kho/w"], sd)
    _doi(7, rc, e, "I2(R) chỉ lệch " + field)
    if (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: state đổi")


def _r812_r6_activation(c, variant):
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline đã kích hoạt")
    _kiem(sd, "baseline bật", luat_adr0054=True)
    (sd / "wp55.json").write_bytes(before)
    w = c.tmp / "kho/w"
    p = w / "docs/PROTOCOL_DA_PHIEN.md"
    row = next(x for x in p.read_text().splitlines() if re.match(r"^\|\s*`ADR-0054`\s*\|", x))
    replacement = {"pending": row + " chưa kích hoạt", "missing": "", "duplicate": row + "\n" + row}[variant]
    p.write_text(p.read_text().replace(row, replacement, 1))
    _g(w, "add", "docs/PROTOCOL_DA_PHIEN.md"), _g(w, "commit", "-qm", "protocol activation condition")
    _g(w, "push", "-q", "origin", "master")
    rc, _, e = run(c.script, ["record-lease", "--packet", 55, "--lease-ref", "origin/ops/wp55-spec", "--lease-path", "ops/leases/l.yaml",
                            "--lease-comments", c.tmp / "cm.json", "--root", w], sd)
    _doi(0, rc, e, "lease hợp lệ khi chế độ chưa đủ điều kiện")
    _kiem(sd, "kích hoạt protocol thiếu " + variant, luat_adr0054=False)


def _r812_r6_family(c, role):
    import yaml
    w, sd = _kho812(c), c.sd()
    ex, rv = ("google_antigravity", "claude") if role == "executor" else ("claude", "google_antigravity")
    doi = {"provider": ex, "executor": ex, "reviewer": rv}
    if role == "executor":
        doi.update(model_family="gemini", execution_surface="antigravity", reviewer_model_family="claude",
                   reviewer_execution_surface="claude_code", reviewer_transport="machine/local")
    else:
        doi.update(reviewer_model_family="gemini", reviewer_execution_surface="antigravity", reviewer_transport="machine/local")
    _r812_doi_lease(w, doi)
    _doi(0, *c.init(sd, executor=ex, reviewer=rv, lease=False, extra=(f"--{role}-model-family", "gemini",
        f"--{role}-execution-surface", "antigravity", f"--{role}-transport", "machine/local"))[::2], "init AG " + role)
    (c.tmp / "cm.json").write_text(json.dumps([{"user": {"login": "github-actions[bot]"}, "body": "lease_id: wp55-r1-g1-claude",
                                               "issue_url": "https://api.github.com/repos/o/r/issues/55"}]))
    h = _g(w, "rev-parse", "refs/remotes/origin/agent/wp55-g1-claude")
    args = ["--model-family", "gemini", "--execution-surface", "antigravity", "--transport", "machine/local"]
    for cmd in (["record-lease", "--lease-ref", "origin/ops/wp55-spec", "--lease-path", "ops/leases/l.yaml", "--lease-comments", c.tmp / "cm.json", "--root", w],
                ["begin-attempt", "--provider", ex, *(args if role == "executor" else [])],
                ["record-post", "--for", "reviewing", "--comment-id", "9000055002"],
                ["transition", "--to", "reviewing", "--comment-id", "9000055002", "--head-sha", h]):
        _doi(0, *run(c.script, [cmd[0], "--packet", 55, *cmd[1:]], sd)[::2], "AG baseline " + cmd[0])
    sub = {"model_family": "gemini", "model_evidence": "do_may", "model_evidence_ref": "r"}
    bn = _bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], bn={"executor_provider": ex,
        "model_reviewer_identity": {"provider": "anthropic_claude" if role == "executor" else "google_antigravity",
            "surface": "claude_code" if role == "executor" else "antigravity", "transport": "machine/local", "session_run_id": "s1"}})
    bn.setdefault("model_" + role + "_identity", {}).update(sub)
    p, before = c.tmp / "bn.yaml", (sd / "wp55.json").read_bytes()
    cmd = ["record-review", "--packet", 55, "--provider", rv, *(args if role == "reviewer" else []), "--verdict", "approve",
           "--reviewed-sha", h, "--bien-nhan", p, "--root", w]
    p.write_text(yaml.safe_dump(bn))
    _doi(0, *run(c.script, cmd, sd)[::2], "baseline H thật, họ khớp lease")
    (sd / "wp55.json").write_bytes(before)
    bn["model_" + role + "_identity"]["model_family"] = "gpt"  # vẫn khác họ Claude, H canon vẫn hợp lệ
    p.write_text(yaml.safe_dump(bn))
    rc, _, e = run(c.script, cmd, sd)
    _doi(11, rc, e, "I8 họ " + role + " lệch lease")
    if (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: state đổi")


def _r812_r6_bad_receipt_path(c, native=False):
    import yaml
    rc, sd, e, before = _r812(c, "review")
    _doi(0, rc, e, "baseline H thật")
    (sd / "wp55.json").write_bytes(before)
    p = c.tmp / "bn.yaml"
    if native:
        if os.name == "nt":
            raise BoQua("tên tệp byte native (surrogateescape) chỉ có trên POSIX") from OSError("không áp dụng trên Windows")
        q = c.tmp / ("receipt-" + chr(0xdc80) + ".yaml")
        q.write_bytes(p.read_bytes())
        p = q
    else:
        bn = yaml.safe_load(p.read_bytes())
        bn["verdict_path"] += "\x00"
        bn["evidence_url"] += "\x00"
        p.write_text(yaml.safe_dump(bn))
    rc, _, e = run(c.script, ["record-review", "--packet", 55, "--provider", "codex", "--verdict", "approve",
        "--reviewed-sha", json.loads(before)["reviewing_head_sha"], "--codex-call", "g1", "--bien-nhan", p, "--root", c.tmp / "kho/w"], sd)
    _doi(8 if native else 11, rc, e, "đường dẫn biên nhận không mã hoá/không gọi git được")
    if (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: đầu vào làm hỏng state")


for key in ("ASSURANCE_CAN_DOC_LAP", "HO_MODEL_CHO_PHEP", "_thieu", "_neo_git", "_nguon_tra_model", "_giai_ho_model_reviewer", "_giai_ho_model_executor", "_chuoi", "_chuan_hoa_provider"):
    CASES.append(("r812_r6_api_" + key, _r812_ca("lease", 8, truoc_lease=lambda w, k=key: _r812_r6_api_lease(w, k))))
for field in ("author", "issue", "lease_id"):
    CASES.append(("r812_r6_workflow_" + field, lambda c, k=field: _r812_r6_comment(c, k)))
for variant in ("pending", "missing", "duplicate"):
    CASES.append(("r812_r6_activation_" + variant, lambda c, k=variant: _r812_r6_activation(c, k)))
for role in ("executor", "reviewer"):
    CASES.append(("r812_r6_family_" + role, lambda c, k=role: _r812_r6_family(c, k)))
CASES += [
    ("r812_r6_write_set_nul", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["x/a.py\x00"]}))),
    ("r812_r6_write_set_long", _r812_ca("lease", 7, truoc_lease=lambda w: _r812_doi_lease(w, {"write_set": ["x/" + "a" * 140000]}))),
    ("r812_r6_receipt_nul", _r812_r6_bad_receipt_path),
    ("r812_r6_receipt_native", lambda c: _r812_r6_bad_receipt_path(c, native=True)),
]
MUTANTS.update({
    "r812_r6_no_api_types": ('        if (any(type(getattr(m, k))', '        if False and (any(type(getattr(m, k))', ["r812_r6_api_" + k for k in ("ASSURANCE_CAN_DOC_LAP", "HO_MODEL_CHO_PHEP", "_thieu", "_neo_git", "_nguon_tra_model", "_giai_ho_model_reviewer", "_giai_ho_model_executor", "_chuoi", "_chuan_hoa_provider")]),
    "r812_r6_unhandled_argv_valueerror": ('except (OSError, subprocess.SubprocessError, ValueError) as ex:', 'except (OSError, subprocess.SubprocessError) as ex:', ["r812_r6_write_set_nul"]),
    "r812_r6_unhandled_argv_oserror": ('except (OSError, subprocess.SubprocessError, ValueError) as ex:', 'except (subprocess.SubprocessError, ValueError) as ex:', ["r812_r6_write_set_long"]),
    "r812_r6_unhandled_receipt_path": ('        except Exception as ex:  # H hỏng/không đo được', '        except OSError as ex:  # H hỏng/không đo được', ["r812_r6_receipt_nul"]),
    "r812_r6_family_executor": ('("ho-executor", bool(ho_exec) and ho_exec == ho("executor"))', '("ho-executor", True)', ["r812_r6_family_executor"]),
    "r812_r6_family_reviewer": ('("ho-reviewer", bool(ho_rev) and ho_rev == ho("reviewer"))', '("ho-reviewer", True)', ["r812_r6_family_reviewer"]),
    "r812_r6_activation_protocol": ('and pr[0] == 0 and len(dong20) == 1 and "chưa kích hoạt" not in dong20[0].casefold()', 'and True', ["r812_r6_activation_" + k for k in ("pending", "missing", "duplicate")]),
    "r812_r6_workflow_author": ('c["user"].get("login") == BOT_LEASE', 'True', ["r812_r6_workflow_author"]),
    "r812_r6_workflow_issue": ('str(c.get("issue_url", "")).endswith(f"/{mr[1]}/issues/{st[\'packet\']}")', 'True', ["r812_r6_workflow_issue"]),
    "r812_r6_workflow_lease_id": ('re.search(rf"^lease_id: {re.escape(lid)}$", str(c.get("body", "")), re.M)', 'True', ["r812_r6_workflow_lease_id"]),
})
MUTANTS["r812_r6_encode_after_truncate"] = (
    ('    try:\n        raw = (json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\\n").encode("utf-8")\n    except (ValueError, TypeError, UnicodeError) as ex:\n        _die(RC_STATE, f"state không mã hoá được: {type(ex).__name__}")\n    p.write_bytes(raw)'),
    '    p.write_text(json.dumps(st, ensure_ascii=False, indent=2, sort_keys=True) + "\\n", encoding="utf-8", newline="\\n")', ["r812_r6_receipt_native"])


# #812 lượt 7: phân biệt cờ có mặt/rỗng; URL issue đầy đủ; identity lease chuẩn hoá; chốt M1 độc lập.
def _r812_r7_cmd(c, sd, w, *extra):
    return run(c.script, ["record-lease", "--packet", 55, "--lease-ref", "origin/ops/wp55-spec",
        "--lease-path", "ops/leases/l.yaml", "--lease-comments", c.tmp / "cm.json", "--root", w, *extra], sd)


def _r812_r7_mixed(c, key, old_empty=False):
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline lease H/Đ/R")
    (sd / "wp55.json").write_bytes(before)
    w = c.tmp / "kho/w"
    if old_empty:
        rc, _, e = _r812_r7_cmd(c, sd, w, key, "")
    elif key == "complete":
        rc, _, e = _r812_r7_cmd(c, sd, w, "--lease-id", "old", "--granted-by", "ducthangho",
            "--evidence", "ordinary authority", "--expires-utc", _han_tuong_lai(1))
    else:
        rc, _, e = run(c.script, ["record-lease", "--packet", 55, "--lease-id", "old", "--granted-by", "ducthangho",
            "--evidence", "ordinary authority", "--expires-utc", _han_tuong_lai(1), key, ""], sd)
    _doi(2, rc, e, "hai đường phải loại trừ khi cờ CÓ MẶT, kể cả rỗng")
    if (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: state đổi khi cờ hai đường trộn nhau")


def _r812_r7_comment_url(c, url, rc_doi):
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline lease H/Đ/R")
    (sd / "wp55.json").write_bytes(before)
    p = c.tmp / "cm.json"
    cm = json.loads(p.read_bytes()); cm[0]["issue_url"] = url
    p.write_text(json.dumps(cm))
    rc, _, e = _r812_r7_cmd(c, sd, c.tmp / "kho/w")
    _doi(rc_doi, rc, e, "I2(R) URL phải neo đúng GitHub repo và issue")
    if rc_doi and (sd / "wp55.json").read_bytes() != before:
        raise AssertionError("I4: state đổi khi URL comment sai")


def _r812_r7_init_identity(c, role):
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline lease H/Đ/R")
    st = json.loads(before)
    st[role + "_identity"]["execution_surface"] = "codex_desktop" if role == "reviewer" else "claude_code"
    raw = json.dumps(st).encode(); (sd / "wp55.json").write_bytes(raw)
    rc, _, e = _r812_r7_cmd(c, sd, c.tmp / "kho/w")
    _doi(4, rc, e, "lease không đổi identity đã init")
    if (sd / "wp55.json").read_bytes() != raw:
        raise AssertionError("I4: lease identity khác init làm state đổi")


def _r812_r7_activation_name(c):
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline kích hoạt ADR-0054")
    (sd / "wp55.json").write_bytes(before)
    w = c.tmp / "kho/w"
    p = w / "docs/adr/0099-kich-hoat-adr-0054.md"
    p.write_text(p.read_text().replace("ADR-0054", "ADR-0053"))
    _g(w, "add", p.relative_to(w).as_posix()), _g(w, "commit", "-qm", "different activation target")
    _g(w, "push", "-q", "origin", "master")
    rc, _, e = _r812_r7_cmd(c, sd, w)
    _doi(0, rc, e, "lease hợp lệ, kích hoạt ADR khác")
    _kiem(sd, "chế độ phải false khi tệp kích hoạt ADR khác", luat_adr0054=False)


def _r812_r7_init_ag_family(c, role):
    w, sd = _kho812(c), c.sd()
    ex, rv = ("google_antigravity", "claude") if role == "executor" else ("claude", "google_antigravity")
    doi = {"provider": ex, "executor": ex, "reviewer": rv}
    if role == "executor":
        doi.update(model_family="gemini", execution_surface="antigravity", reviewer_model_family="claude",
                   reviewer_execution_surface="claude_code", reviewer_transport="machine/local")
    else:
        doi.update(reviewer_model_family="gemini", reviewer_execution_surface="antigravity", reviewer_transport="machine/local")
    _r812_doi_lease(w, doi)
    _doi(0, *c.init(sd, executor=ex, reviewer=rv, lease=False, extra=(f"--{role}-model-family", "gemini",
        f"--{role}-execution-surface", "antigravity", f"--{role}-transport", "machine/local"))[::2], "init AG")
    (c.tmp / "cm.json").write_text(json.dumps([{"user": {"login": "github-actions[bot]"},
        "body": "lease_id: wp55-r1-g1-claude", "issue_url": "https://api.github.com/repos/o/r/issues/55"}]))
    before = (sd / "wp55.json").read_bytes()
    _doi(0, *_r812_r7_cmd(c, sd, w)[::2], "baseline lease khớp init AG")
    st = json.loads(before); st[role + "_identity"]["model_family"] = "openai"
    raw = json.dumps(st).encode(); (sd / "wp55.json").write_bytes(raw)
    _doi(4, *_r812_r7_cmd(c, sd, w)[::2], "lease chỉ lệch họ model đã init " + role)
    if (sd / "wp55.json").read_bytes() != raw:
        raise AssertionError("I4: state đổi khi lease lệch identity init")


for role in ("executor", "reviewer"):
    CASES.append(("r812_r7_lease_init_ag_" + role, lambda c, r=role: _r812_r7_init_ag_family(c, r)))

for key in ("--lease-id", "--granted-by", "--evidence", "--expires-utc"):
    CASES.append(("r812_r7_new_plus_empty_" + key[2:].replace("-", "_"), lambda c, k=key: _r812_r7_mixed(c, k, True)))
for key in ("--lease-ref", "--lease-path", "--lease-comments"):
    CASES.append(("r812_r7_old_plus_empty_" + key[2:].replace("-", "_"), lambda c, k=key: _r812_r7_mixed(c, k)))
CASES.append(("r812_r7_paths_exclusive", lambda c: _r812_r7_mixed(c, "complete")))
for name, url in (("wrong_host", "https://example.org/repos/o/r/issues/55"), ("not_url", "ordinary/o/r/issues/55"),
                  ("extra_prefix", "https://api.github.com/repos/different/o/r/issues/55")):
    CASES.append(("r812_r7_comment_" + name, lambda c, u=url: _r812_r7_comment_url(c, u, 7)))
CASES.append(("r812_r7_comment_web", lambda c: _r812_r7_comment_url(c, "https://github.com/o/r/issues/55", 0)))
for role, key, value in (("executor", "provider", " claude "), ("reviewer", "reviewer", " codex "),
                          ("executor_alias", "provider", " anthropic_claude "), ("reviewer_alias", "reviewer", " openai_codex ")):
    CASES.append(("r812_r7_padded_lease_" + role, _r812_ca("lease", 0, {"state": "leased", "luat_adr0054": True},
        truoc_lease=lambda w, k=key, v=value: _r812_doi_lease(w, {k: v}))))
CASES += [
    ("r812_r7_lease_packet", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w, {"packet_issue": 56}))),
    ("r812_r7_instruction_packet", _r812_ca("lease", 2, truoc_lease=lambda w: _r812_doi_lease(w,
        {"granted_on_instruction": "https://github.com/o/r/issues/56#issuecomment-1"}))),
    ("r812_r7_lease_init_reviewer", lambda c: _r812_r7_init_identity(c, "reviewer")),
    ("r812_r7_activation_adr_name", _r812_r7_activation_name),
]
MUTANTS.update({
    "r812_r7_ignore_empty_flags": (("moi_co = any(x is not None for x in moi)", "cu_co = any(x is not None for x in cu)"),
        ("moi_co = any(moi)", "cu_co = any(cu)"), [n for n, _ in CASES if n.startswith(("r812_r7_new_plus_empty_", "r812_r7_old_plus_empty_"))]),
    "r812_r7_paths_mixed": ("if moi_co == cu_co or not all(moi if moi_co else cu):", "if not all(moi if moi_co else cu):", ["r812_r7_paths_exclusive"]),
    "r812_r7_comment_suffix": ('c.get("issue_url") in (f"https://api.github.com/repos/{mr[1]}/issues/{st[\'packet\']}", f"https://github.com/{mr[1]}/issues/{st[\'packet\']}")',
        'str(c.get("issue_url", "")).endswith(f"/{mr[1]}/issues/{st[\'packet\']}")', ["r812_r7_comment_" + k for k in ("wrong_host", "not_url", "extra_prefix")]),
    "r812_r7_lease_raw_provider": ("    p = p.strip()  # I8: bản chiếu identity lease", "    # I8: không strip provider", ["r812_r7_padded_lease_" + k for k in ("executor", "reviewer", "executor_alias", "reviewer_alias")]),
    "r812_r7_lease_packet": (' or l["packet_issue"] != st["packet"]', '', ["r812_r7_lease_packet"]),
    "r812_r7_instruction_packet": (' or mr[2].lstrip("0") != str(st["packet"])', '', ["r812_r7_instruction_packet"]),
    "r812_r7_lease_init_identity": ('if any(v is not None and nc[vai][k] != v for k, v in (st.get(f"{vai}_identity") or {}).items()):', 'if False:', ["r812_r7_lease_init_reviewer", "r812_r7_lease_init_ag_executor", "r812_r7_lease_init_ag_reviewer"]),
    "r812_r7_activation_adr_name": ('"kích hoạt `ADR-0054`" in nfc(b)', '"kích hoạt `ADR-005" in nfc(b)', ["r812_r7_activation_adr_name"]),
    "r812_r7_reject_web_comment": ('f"https://github.com/{mr[1]}/issues/{st[\'packet\']}"', '"web-form-rejected"', ["r812_r7_comment_web"]),
})
MUTANTS["r812_r6_workflow_issue"] = (MUTANTS["r812_r7_comment_suffix"][0], "True", ["r812_r6_workflow_issue"])


# wp929: ADR kích hoạt `ADR-0054` nhận theo CỤM khai trên mọi `docs/adr/NNNN-*.md` (trừ chính ADR-0054), đúng MỘT tệp — không theo số.
_R929_KICH = "docs/adr/0099-kich-hoat-adr-0054.md"
_R929_ADR54 = "docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md"


def _r929_symlink(w):
    """Symlink ghi THẲNG vào index (120000): đích là cụm khai, nên `git show` in ra đúng cụm ấy dù không có tệp ADR nào khai."""
    o = subprocess.run(["git", "hash-object", "-w", "--stdin"], cwd=w, input="kích hoạt `ADR-0054`".encode(), capture_output=True, check=True)
    _g(w, "update-index", "--add", "--cacheinfo", f"120000,{o.stdout.decode().strip()},docs/adr/0732-lien-ket.md")


def _r929_adr(c, doi, muon, nen=True, index=None, sau=None):
    """Baseline lease (đã kích hoạt) rồi đổi `docs/adr/` trên master theo `doi` (None ⇒ xoá; bytes ghi nguyên) và ghi lại lease qua
    đường thật. `index(w)` sửa index sau `add` (mục không có trên đĩa); `sau(w)` chạy sau push. `nen=False` khi ca đòi True: phép
    đo nền khi ấy không phân biệt được gì, mà lại che mất chỗ chết của đột biến đích."""
    rc, sd, e, before = _r812(c, "lease")
    _doi(0, rc, e, "baseline kích hoạt ADR-0054")
    if nen:
        _kiem(sd, "baseline bật", luat_adr0054=True)
    (sd / "wp55.json").write_bytes(before)
    w = c.tmp / "kho/w"
    for p, nd in doi.items():
        (w / p).parent.mkdir(parents=True, exist_ok=True)
        (w / p).unlink() if nd is None else (w / p).write_bytes(nd if isinstance(nd, bytes) else nd.encode("utf-8"))
    _g(w, "add", "-A", "docs/adr"), (index or (lambda w: None))(w), _g(w, "commit", "-qm", "wp929 adr"), _g(w, "push", "-q", "origin", "master")
    (sau or (lambda w: None))(w)
    rc, _, e = _r812_r7_cmd(c, sd, w)
    _doi(0, rc, e, "lease hợp lệ dù chế độ đổi")
    _kiem(sd, f"wp929 {sorted(doi)}", luat_adr0054=muon)


CASES += [
    # (a) số bất kỳ, tên bất kỳ — không neo 0055 hay 0099
    ("r929_kich_hoat_so_bat_ky", lambda c: _r929_adr(c, {_R929_KICH: None, "docs/adr/0731-bat-ky.md": "Tệp này kích hoạt `ADR-0054`.\n"}, True, nen=False)),
    # (b) giống ADR-0055 thật: có "kích hoạt" và "ADR-0054" nhưng không đúng cụm
    ("r929_hai_chuoi_roi_khong_tinh", lambda c: _r929_adr(c, {_R929_KICH: None, "docs/adr/0055-tran-loi-goi-codex-len-muoi.md":
                                                               "ADR-0054 chưa kích hoạt; trần Codex không phụ thuộc `ADR-0054`.\n"}, False)),
    # (c) hai tệp cùng khai ⇒ mơ hồ ⇒ False
    ("r929_hai_tep_kich_hoat", lambda c: _r929_adr(c, {"docs/adr/0100-kich-hoat-lai.md": "kích hoạt `ADR-0054`\n"}, False)),
    # (d) chỉ chính ADR-0054 nêu cụm (mục Hiệu lực của nó) ⇒ không tự kích hoạt
    ("r929_chi_adr0054_tu_neu_cum", lambda c: _r929_adr(c, {_R929_KICH: None, _R929_ADR54: "x\nđo bằng cụm kích hoạt `ADR-0054`\n"}, False)),
    # review #1: thư mục đuôi `.md` / symlink — cụm chỉ nằm trong TÊN con hoặc ĐÍCH liên kết, không phải nội dung tệp
    ("r929_thu_muc_ten_md", lambda c: _r929_adr(c, {_R929_KICH: None, "docs/adr/0731-thu-muc.md/kích hoạt `ADR-0054`": "ghi chú\n"}, False)),
    ("r929_symlink_khong_tinh", lambda c: _r929_adr(c, {_R929_KICH: None}, False, index=_r929_symlink)),
    # biên tên tệp: đúng bốn chữ số, đuôi `.md`
    ("r929_ba_chu_so_khong_tinh", lambda c: _r929_adr(c, {_R929_KICH: None, "docs/adr/099-kich-hoat.md": "kích hoạt `ADR-0054`\n"}, False)),
    ("r929_duoi_khac_md_khong_tinh", lambda c: _r929_adr(c, {_R929_KICH: None, "docs/adr/0099-kich-hoat.txt": "kích hoạt `ADR-0054`\n"}, False)),
    # NFD trong blob phải được chuẩn hoá trước khi so cụm
    ("r929_nfd_van_tinh", lambda c: _r929_adr(c, {_R929_KICH: __import__("unicodedata").normalize("NFD", "kích hoạt `ADR-0054`\n").encode()}, True, nen=False)),
    # `git show` một ứng viên lỗi (blob mất khỏi kho) ⇒ False dù tệp kích hoạt khác vẫn hợp lệ
    ("r929_show_loi_la_false", lambda c: _r929_adr(c, {"docs/adr/0100-ghi-chu.md": "ghi chú wp929\n"}, False, sau=lambda w: (
        w / ".git/objects" / (o := _g(w, "rev-parse", "master:docs/adr/0100-ghi-chu.md"))[:2] / o[2:]).unlink())),
]
MUTANTS.update({
    "r929_bo_loai_tru_adr0054": (' and t != ADR0054_TEP]', ']', ["r929_chi_adr0054_tu_neu_cum"]),
    "r929_mot_tro_len": ('and len(kich) == 1', 'and len(kich) >= 1', ["r929_hai_tep_kich_hoat"]),
    "r929_hai_chuoi_roi": ('"kích hoạt `ADR-0054`" in nfc(b)', '"kích hoạt" in nfc(b) and "ADR-0054" in nfc(b)', ["r929_hai_chuoi_roi_khong_tinh"]),
    "r929_duong_dan_co_dinh_0055": ('re.fullmatch(r"docs/adr/[0-9]{4}-[^/]+\\.md", t)', 't == "docs/adr/0055-kich-hoat-adr-0054.md"', ["r929_kich_hoat_so_bat_ky"]),
    "r929_bo_kiem_loai_doi_tuong": ('k.split(" ")[:2] in (["100644", "blob"], ["100755", "blob"]) and ', '', ["r929_thu_muc_ten_md", "r929_symlink_khong_tinh"]),
    "r929_nhan_symlink": ('(["100644", "blob"], ["100755", "blob"])', '(["100644", "blob"], ["100755", "blob"], ["120000", "blob"])', ["r929_symlink_khong_tinh"]),
    "r929_so_chu_so_tuy_y": ('r"docs/adr/[0-9]{4}-', 'r"docs/adr/[0-9]+-', ["r929_ba_chu_so_khong_tinh"]),
    "r929_bo_duoi_md": ('[^/]+\\.md", t)', '[^/]+", t)', ["r929_duoi_khac_md_khong_tinh"]),
    "r929_bo_nfc": ('in nfc(b)]', 'in b.decode("utf-8", "replace")]', ["r929_nfd_van_tinh"]),
    "r929_bo_rc_show": (' and all(rc == 0 for rc, _ in adr)', '', ["r929_show_loi_la_false"]),
})
# `_ten_provider` chuẩn hoá dùng chung: gỡ một trong hai phép strip của receipt là mutant tương đương.
MUTANTS["r812_r5_raw_provider"] = ((MUTANTS["r812_r5_raw_provider"][0], "    p = p.strip()  # I8: bản chiếu identity lease"),
    (MUTANTS["r812_r5_raw_provider"][1], "    # bỏ strip dùng chung"), ["r812_r5_padded_provider"])


# #812 connector (review tự kích hoạt khi PR ready, trên f4ab8b6): ba lớp P2.
def _r812_r8_symlink(dich, ws_khac, cay="khac", ten=None):
    """Symlink (mặc định `alias -> dich`) CHỈ có trên MỘT cây (ref lease này · ref `ops/khac` của lease kia), checkout người gọi
    không có; lease khác còn hiệu lực giữ `ws_khac` ở `ops/khac`. Symlink ghi THẲNG vào index (120000) — không cần quyền tạo
    symlink của hệ tệp, và tạo được cả hai tên chỉ khác hoa/thường trên hệ tệp không phân biệt."""
    def doi(w):
        goc = _g(w, "rev-parse", "refs/remotes/origin/ops/wp55-spec")  # hai nhánh rẽ từ CÙNG gốc — symlink chỉ ở đúng một cây
        lease = json.loads(_g(w, "show", f"{goc}:ops/leases/l.yaml"))
        for nhanh in ("ops/wp55-spec", "ops/khac"):
            _g(w, "checkout", "-qb", nhanh, goc)
            if nhanh == "ops/khac":
                (w / "ops/leases/k.yaml").write_text(json.dumps({**lease, "lease_id": "wp55-r1-g1-khac", "write_set": ws_khac}))
                _g(w, "add", "ops/leases")
            if nhanh.endswith(cay):
                for t, d in (ten or {"alias": dich}).items():
                    blob = subprocess.run(["git", "hash-object", "-w", "--stdin"], input=d, cwd=w, text=True, capture_output=True, check=True).stdout.strip()
                    _g(w, "update-index", "--add", "--cacheinfo", f"120000,{blob},{t}")
            _g(w, "commit", "-qm", "r8", "--allow-empty"), _g(w, "push", "-q", "origin", nhanh), _g(w, "checkout", "-qf", "master")
            _g(w, "branch", "-q", "-D", nhanh)
    return doi

LOP_R8 = (("lop-tai-dien", "P1"), ("lop-moi", "P2"))
BN_AM = {"verdict": "changes_requested"}
CASES += [
    ("r812_r8_symlink_chi_trong_ref", _r812_ca("lease", 7, truoc_lease=_r812_r8_symlink("x", ["alias/a.py"]))),
    ("r812_r8_symlink_chi_trong_snapshot", _r812_ca("lease", 7, truoc_lease=_r812_r8_symlink("x", ["alias/a.py"], cay="spec"))),
    ("r812_r8_symlink_doi_chung", _r812_ca("lease", 0, {"state": "leased"}, truoc_lease=_r812_r8_symlink("x", ["alias/b.py"]))),
    ("r812_r8_symlink_hoa_thuong", _r812_ca("lease", 7, truoc_lease=_r812_r8_symlink("x", ["ALIAS/a.py"]))),
    ("r812_r8_symlink_unicode", _r812_ca("lease", 7, truoc_lease=_r812_r8_symlink("x", ["CAFE\u0301/a.py"], ten={"caf\u00e9": "x"}))),
    ("r812_r8_symlink_hoa_thuong_doi_chung", _r812_ca("lease", 0, {"state": "leased"}, truoc_lease=_r812_r8_symlink("x", ["ALIAS/b.py"]))),
    ("r812_r8_symlink_mo_ho", _r812_ca("lease", 7, truoc_lease=_r812_r8_symlink("x", ["Alias/a.py"], ten={"ALIAS": "y", "alias": "x"}))),
    ("r812_r8_am_bo_lop_tai_dien", _r812_ca("review", 11, bn=BN_AM, lop=LOP_R8, verdict="changes_requested", ids=("lop-moi",))),
    ("r812_r8_am_du_lop", _r812_ca("review", 0, {"state": "running", "finding_counts": {"lop-tai-dien": 1, "lop-moi": 1}}, bn=BN_AM,
                                   lop=LOP_R8, verdict="changes_requested", ids=("lop-tai-dien", "lop-moi"))),
    ("r812_r8_approve_no_p3", _r812_ca("review", 0, {"state": "approved_pending"}, lop=(("no-p3", "P3"),))),
    ("r812_r8_runtime_trai_lease", _r812_ca("review", 4, rv=("--execution-surface", "codex_desktop", "--transport", "machine/local"))),
    ("r812_r8_runtime_khop_lease", _r812_ca("review", 0, {"state": "approved_pending"}, rv=("--execution-surface", "codex_cli", "--transport", "machine"))),
]
MUTANTS.update({
    "r812_r8_symlink_theo_checkout": ("_bieu_dien_duong(x, root) | {_dich_trong_cay(root, r, x) for r in revs}", "_bieu_dien_duong(x, root)",
                                      ["r812_r8_symlink_chi_trong_ref"]),
    "r812_r8_bo_cay_ref_kia": ("revs = (oid, m[\"ref\"])", "revs = (oid,)", ["r812_r8_symlink_chi_trong_ref"]),
    "r812_r8_bo_snapshot_lease": ("revs = (oid, m[\"ref\"])", "revs = (m[\"ref\"],)", ["r812_r8_symlink_chi_trong_snapshot"]),
    "r812_r8_cay_theo_byte": ('        khoa = lambda s: unicodedata.normalize("NFC", s).casefold()  # noqa: E731', '        khoa = lambda s: s  # noqa: E731',
                              ["r812_r8_symlink_hoa_thuong", "r812_r8_symlink_unicode"]),
    "r812_r8_cay_bo_nfc": ('lambda s: unicodedata.normalize("NFC", s).casefold()  # noqa', 'lambda s: s.casefold()  # noqa', ["r812_r8_symlink_unicode"]),
    "r812_r8_cay_bo_mo_ho": ("        if len(khop) > 1:", "        if False:", ["r812_r8_symlink_mo_ho"]),
    "r812_r8_bo_du_lop_am": ('("thieu-lop-am", lop_ok and (', '("thieu-lop-am", True or (', ["r812_r8_am_bo_lop_tai_dien"]),
    "r812_r8_du_lop_ca_approve": ('a.verdict == "approve" or {x["slug"]', 'False or {x["slug"]', ["r812_r8_approve_no_p3"]),
    "r812_r8_runtime_bo_lease": ('    if isinstance(lease, dict) and any(', '    if False and any(', ["r812_r8_runtime_trai_lease"]),
})


# --- #834 MAY-ADR-0054-a2 `accept`: baseline DƯƠNG = approved_pending thật (`_r812`) + 5 job bắt buộc xanh trên attempt mới nhất của run
# mới nhất + connector sạch neo head; mỗi ca đổi ĐÚNG một yếu tố qua `doi(x, w, h)`, đòi rc + lý do; ca âm đòi state nguyên byte (I4).
_CN834, _API834 = "chatgpt-codex-connector[bot]", "https://api.github.com/repos/o/r/"
_J834 = [f"{j} (ubuntu-latest)" for j in ("gate", "gate-cong-cu-gop", "gate-ops", "gate-packet-loop", "gate-registry")]


def _r834(c: Ctx, doi=None, lop=(), p3_cn=False, env=None, vo=False):
    rc, sd, e, _ = _r812(c, "review", lop=lop, env=env)
    _doi(0, rc, e, "r834 nền approved_pending")
    w, f, h = c.tmp / "kho" / "w", c.tmp, _st(sd)["pending_sha"]
    qd = lambda nguon, khoa: {"nguon": nguon, "khoa": khoa, "ten_no": "no-x", "owner": "ducthangho", "huong": "#814", "ly_do": "nit"}  # noqa: E731
    x = {"runs": [{"id": 100, "path": ".github/workflows/ci.yml", "head_sha": h, "repository": {"full_name": "o/r"}, "run_attempt": 1,
                   "status": "completed", "conclusion": "success", "check_suite_id": 500}],
         "jobs": [{"id": 200 + i, "run_id": 100, "run_attempt": 1, "name": j, "head_sha": h, "status": "completed", "conclusion": "success",
                   "check_run_url": f"{_API834}check-runs/{300 + i}"} for i, j in enumerate(_J834)],
         "cr": [{"id": 300 + i, "name": j, "head_sha": h, "status": "completed", "conclusion": "success", "check_suite": {"id": 500},
                 "app": {"slug": "github-actions"}, "url": f"{_API834}check-runs/{300 + i}"} for i, j in enumerate(_J834)],
         "reviews": [], "review_comments": [], "qd": [qd("offline", s) for s, g in lop if g == "P3"], "bnc": None, "qdf": qd, "sd": sd, "jobs2": None,
         "issue_comments": [{"id": 20, "user": {"login": _CN834}, "body": f"Codex Review: Didn't find any major issues.\n\n**Reviewed commit:** `{h[:10]}`\n\n<details>x</details>", "issue_url": f"{_API834}issues/55"}]}
    if p3_cn:
        x["review_comments"] = [{"id": 11, "user": {"login": _CN834}, "body": "![P3 Badge] nit", "commit_id": h, "pull_request_url": f"{_API834}pulls/55"}]
        x["bnc"], x["qd"] = {"bang_lop": [{"slug": "c-d", "hang": "P3", "connector_refs": [["review_comments", 11]]}]}, [*x["qd"], qd("connector", "c-d")]
    (doi or (lambda *_: None))(x, w, h)
    trang = lambda k, v: {"total_count": len({i["id"] for i in v}), k: v}  # noqa: E731
    ghi = lambda ten, d: ((f / ten).write_text(d if isinstance(d, str) else json.dumps(d)), f / ten)[1]  # noqa: E731
    cn = "{" if x.get("hong") else {"repo": "o/r", "pr": 55, "head_sha": h, **{k: trang("items", x[k]) for k in ("reviews", "review_comments", "issue_comments")}, **x.get("env", {})}
    args = ["accept", "--packet", 55, "--root", w, "--pr", 55, "--workflow-runs", ghi("wr.json", trang("workflow_runs", x["runs"])),
            "--workflow-jobs", ghi("wj.json", trang("jobs", x["jobs"])), *(("--workflow-jobs", ghi("wj2.json", trang("jobs", x["jobs2"]))) if x["jobs2"] else ()), "--check-runs", ghi("cr.json", trang("check_runs", x["cr"])), "--connector", ghi("cn.json", cn),
            *(("--quyet-dinh-p3", ghi("qd.json", x["qd"])) if x["qd"] else ()),
            *(("--bien-nhan-connector", ghi("bnc.yaml", __import__("yaml").safe_dump(_bn812(w, h, _st(sd)["ngu_canh_lease"]["spec_hash"], bn=x["bnc"])))) if x["bnc"] else ())]
    truoc = (sd / "wp55.json").read_bytes()
    if vo:
        (f / "vo.py").write_text(_VO834)
    rc, o, e = run(f / "vo.py", [c.script, *args], sd, env) if vo else run(c.script, args, sd, env)
    return rc, sd, e, truoc, o


def _r834_ca(rc_doi, doi=None, phai="", **kw):
    def ca(c):
        rc, sd, e, truoc, _ = _r834(c, doi, **kw)
        _doi(rc_doi, rc, e, "r834 accept")
        if phai not in _txt(e):
            raise AssertionError(f"r834: rc đúng mà lý do khác — đòi {phai!r}, stderr={_txt(e)!r}")
        if rc_doi == 0:
            _kiem(sd, "r834 accepted", state="accepted", accepted_sha=_st(sd)["pending_sha"])
        elif (sd / "wp55.json").read_bytes() != truoc:
            raise AssertionError("I4: state đổi sau khi accept từ chối")
    return ca


def _r834_day_nhanh(x, w, h):
    _g(w, "checkout", "-q", "-b", "t834", "refs/remotes/origin/agent/wp55-g1-claude"), (w / "x/b.py").write_text("b = 2\n")
    _g(w, "add", "-A"), _g(w, "commit", "-qm", "sau approve"), _g(w, "push", "-q", "origin", "HEAD:agent/wp55-g1-claude")


_S834 = lambda k, i=0, **v: lambda x, w, h: x[k][i].update(v)  # noqa: E731
_R834_RV = lambda trang_thai, than="": lambda x, w, h: x["reviews"].append({"id": 30, "user": {"login": _CN834}, "state": trang_thai, "commit_id": h,  # noqa: E731
                                                                            "body": than, "pull_request_url": f"{_API834}pulls/55"})
CASES += [
    ("r834_sach_accepted", _r834_ca(0)),
    ("r834_p3_du_quyet_dinh", _r834_ca(0, lop=(("a-b", "P3"),), p3_cn=True)),
    ("r834_dau_nhanh_lech", _r834_ca(5, _r834_day_nhanh, "≠ pending_sha")),
    ("r834_check_vang", _r834_ca(12, lambda x, w, h: x["jobs"].pop(2), "VẮNG")),
    ("r834_check_app_khac", _r834_ca(12, _S834("cr", 1, app={"slug": "evil-app"}), "không từ app")),
    ("r834_check_workflow_khac", _r834_ca(12, _S834("runs", 0, path=".github/workflows/khac.yml"), "VẮNG")),
    ("r834_rerun_dang_chay", _r834_ca(12, _S834("runs", 0, run_attempt=2, status="in_progress", conclusion=None), "chưa xanh")),
    ("r834_check_kho_khac", _r834_ca(12, _S834("cr", 0, url="https://api.github.com/repos/x/r/check-runs/300"), "kho khác")),
    ("r834_pr_khac_cung_head", _r834_ca(12, _S834("issue_comments", 0, issue_url=f"{_API834}issues/56"), "không thuộc")),
    ("r834_review_pending", _r834_ca(12, lambda x, w, h: (x["issue_comments"].clear(), _R834_RV("PENDING")(x, w, h)), "chưa xong")),
    ("r834_review_changes_p1", _r834_ca(12, _R834_RV("CHANGES_REQUESTED", "![P1 Badge] bug"), "còn ['P1']")),
    ("r834_issue_comment_p1", _r834_ca(12, lambda x, w, h: x["issue_comments"].append(
        {**x["issue_comments"][0], "id": 21, "body": f"![P1 Badge] bug\nReviewed commit: `{h[:10]}`"}), "còn ['P1']")),
    ("r834_cung_id_hai_noi_dung", _r834_ca(12, lambda x, w, h: x["review_comments"].insert(0, {**x["review_comments"][0], "body": "![P1 Badge] bug"}),
                                           "hai nội dung", p3_cn=True)),
    ("r834_run_cung_id_khac_path", _r834_ca(12, lambda x, w, h: x["runs"].insert(0, {**x["runs"][0], "path": ".github/workflows/khac.yml"}), "hai nội dung")),
    ("r834_p3_offline_thieu_qd", _r834_ca(2, lambda x, w, h: x["qd"].clear(), "P3 còn mở", lop=(("a-b", "P3"),))),
    ("r834_p3_connector_thieu_qd", _r834_ca(2, lambda x, w, h: x["qd"].clear(), "P3 còn mở", p3_cn=True)),
    ("r834_p3_connector_khong_slug", _r834_ca(11, lambda x, w, h: x.update(bnc=None, qd=[x["qdf"]("connector", "review_comments:11")]),
                                              "--bien-nhan-connector", p3_cn=True)),
    ("r834_bang_chung_duong_rong", _r834_ca(12, lambda x, w, h: x["issue_comments"].clear(), "chưa xong")),
    ("r834_dau_vao_hong_state_nguyen", _r834_ca(12, lambda x, w, h: x.update(hong=True), "KHÔNG ĐO ĐƯỢC")),
]
_M834_EP = "    for k in EP_CONNECTOR:\n        for x, n in cua[k]:"
MUTANTS.update({
    "r834_bo_ket_luan_issue_comment": ('    if not (any(n == "hien" for _, n in cua["issue_comments"])', "    if not (False", ["r834_sach_accepted"]),
    "r834_bo_ref_connector_h": ('    lop = [x for x in lop if "connector_refs" in x]', "    lop = []", ["r834_p3_du_quyet_dinh"]),
    "r834_bo_dau_nhanh_remote": ("    if xa[0] or xa[1].split() != [h.encode(), f\"refs/heads/{nc['branch']}\".encode()]:", "    if xa[0]:", ["r834_dau_nhanh_lech"]),
    "r834_job_vang_bo_qua": ("            if not jj:\n", "            if not jj:\n                continue\n            if False:\n", ["r834_check_vang"]),
    "r834_bo_app": ("get(\"slug\") != APP_CHECK:", "get(\"slug\") != APP_CHECK and False:", ["r834_check_app_khac"]),
    "r834_bo_path_workflow": ('r.get("path") == wf and ', "", ["r834_check_workflow_khac"]),
    "r834_bo_attempt_moi_nhat": (('        if (run.get("status"), run.get("conclusion")) != ("completed", "success"):',
                                  '(j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)'),
                                 ("        if False:", '(j.get("run_id"), j.get("head_sha"), j.get("name")) == (run["id"], h, ten_j)'),
                                 ["r834_rerun_dang_chay"]),  # phối hợp: run mới nhất chưa xanh VÀ job phải thuộc attempt mới nhất — hai lớp cùng chặn
    "r834_bo_kho_check_run": ("            if r.get(\"url\") != f\"{API_GH}{nc['repo']}/check-runs/{r['id']}\":", "            if False:", ["r834_check_kho_khac"]),
    "r834_bo_neo_pr_phan_tu": ("if not all(x.get(url) == dung and", "if not all(", ["r834_pr_khac_cung_head"]),
    "r834_pending_la_xong": (' and x.get("state") in ("APPROVED", "COMMENTED", "CHANGES_REQUESTED")', "", ["r834_review_pending"]),
    "r834_bo_finding_review": (_M834_EP, '    for k in ("review_comments", "issue_comments"):\n        for x, n in cua[k]:', ["r834_review_changes_p1"]),
    "r834_bo_finding_issue_comment": (_M834_EP, '    for k in ("reviews", "review_comments"):\n        for x, n in cua[k]:', ["r834_issue_comment_p1"]),
    "r834_bo_nhat_quan_id": ('        if json.dumps(moi.setdefault(x["id"], x), sort_keys=True) != json.dumps(x, sort_keys=True):', '        if moi.update({x["id"]: x}):',
                             ["r834_cung_id_hai_noi_dung", "r834_run_cung_id_khac_path"]),
    "r834_bo_p3_offline": ('{("offline", s) for s in p3_off} | ', "", ["r834_p3_offline_thieu_qd"]),
    "r834_bo_p3_connector": (' | {("connector", s) for s in slug_cn}', "", ["r834_p3_connector_thieu_qd"]),
    "r834_khoa_id_so": ("slug_cn = _slug_connector(st, a, h, p3_cn) if p3_cn else []", 'slug_cn = [f"{k}:{i}" for k, i in p3_cn]', ["r834_p3_connector_khong_slug"]),
    "r834_bo_bang_chung_duong": ('    if not (any(n == "hien" for _, n in cua["issue_comments"])', '    if False and (any(n == "hien" for _, n in cua["issue_comments"])', ["r834_bang_chung_duong_rong"]),
    "r834_ghi_truoc_khi_doc": ("    p3_cn, moc = _doc_connector(", '    _save(state_dir, {**st, "state": "accepted"})\n    p3_cn, moc = _doc_connector(', ["r834_dau_vao_hong_state_nguyen"]),
})


# #834 lượt 2 — mỗi chốt Codex lượt 1 chỉ ra (gồm 8 đột biến sống của reviewer) có ca đổi đúng một yếu tố + đột biến riêng.
def _r834_run_cu_xanh(x, w, h):  # run 90 cũ, đủ job/check-run xanh ở suite 490; run 100 mới nhất ĐỎ
    x["runs"][0]["conclusion"] = "failure"
    x["runs"].append({**x["runs"][0], "id": 90, "check_suite_id": 490, "conclusion": "success"})
    x["jobs"] += [{**j, "id": j["id"] + 400, "run_id": 90, "check_run_url": f"{_API834}check-runs/{j['id'] + 500}"} for j in x["jobs"]]
    x["cr"] += [{**r, "id": r["id"] + 400, "check_suite": {"id": 490}, "url": f"{_API834}check-runs/{r['id'] + 400}"} for r in x["cr"]]


def _r834_state(**doi):
    def f(x, w, h):
        st = _st(x["sd"])
        for k, v in doi.items():
            st[k] = {**st[k], **v}
        (x["sd"] / "wp55.json").write_text(json.dumps(st))
    return f


_IC834 = lambda than, i=21: lambda x, w, h: x["issue_comments"].append({**x["issue_comments"][0], "id": i, "body": than.format(h=h)})  # noqa: E731
CASES += [
    ("r834_check_noi_do", _r834_ca(12, _S834("cr", 0, conclusion="failure"), "KHÔNG xanh")),
    ("r834_check_noi_do_bi_che", _r834_ca(12, lambda x, w, h: (x["cr"][0].update(conclusion="failure"), x["cr"].append(
        {**x["cr"][0], "id": 999, "conclusion": "success", "app": {"slug": "evil-app"}, "url": "https://api.github.com/repos/x/r/check-runs/999"})), "mới hơn")),
    ("r834_check_cung_id_khac_app", _r834_ca(12, lambda x, w, h: x["cr"].insert(0, {**x["cr"][0], "app": {"slug": "evil-app"}}), "hai nội dung")),
    ("r834_attempt_moi_job_cu", _r834_ca(12, _S834("runs", 0, run_attempt=2), "VẮNG")),
    ("r834_run_moi_nhat_do", _r834_ca(12, _r834_run_cu_xanh, "chưa xanh")),
    ("r834_job_url_kho_khac", _r834_ca(12, _S834("jobs", 0, check_run_url="https://api.github.com/repos/x/r/check-runs/300"), "không trỏ check-run")),
    ("r834_job_tro_check_khong_co", _r834_ca(12, _S834("jobs", 0, check_run_url=f"{_API834}check-runs/399"), "không trỏ check-run")),
    ("r834_hai_tep_jobs", _r834_ca(0, lambda x, w, h: (x["runs"].append({**x["runs"][0], "id": 101, "path": ".github/workflows/khac.yml", "check_suite_id": 501}),
                                                        x.update(jobs2=[{**x["jobs"][0], "id": 250, "run_id": 101, "name": "khac"}])))),
    ("r834_badge_ngoai_mien_review", _r834_ca(12, _R834_RV("COMMENTED", "![Q1 Badge] x"), "ngoài miền")),
    ("r834_review_changes_khong_hang", _r834_ca(12, _R834_RV("CHANGES_REQUESTED", "cần sửa"), "ngoài miền")),
    ("r834_review_comment_thieu_commit", _r834_ca(12, lambda x, w, h: x["review_comments"].append(
        {"id": 12, "user": {"login": _CN834}, "body": "![P1 Badge] bug", "pull_request_url": f"{_API834}pulls/55"}), "thiếu/sai/mơ hồ")),
    ("r834_reviewed_commit_sai_dang", _r834_ca(12, lambda x, w, h: x["issue_comments"][0].update(body=f"Reviewed commit: `{h[:10]}-invalid`"), "thiếu/sai/mơ hồ")),
    ("r834_reviewed_commit_mau_thuan", _r834_ca(12, lambda x, w, h: x["issue_comments"][0].update(
        body=f"Reviewed commit: `{h[:10]}`\nReviewed commit: `{'0' * 10}`"), "thiếu/sai/mơ hồ")),
    ("r834_issue_comment_head_cu_khong_chan", _r834_ca(0, _IC834("![P1 Badge] bug\nReviewed commit: `" + "0" * 10 + "`"))),
    ("r834_envelope_head_khac", _r834_ca(12, lambda x, w, h: x.update(env={"head_sha": "0" * 40}), "không neo đúng")),
    ("r834_trang_thieu", _r834_ca(12, lambda x, w, h: x["issue_comments"].append({**x["issue_comments"][0], "id": 22, "body": "x"})
                                  or x.update(env={"issue_comments": {"total_count": 2, "items": x["issue_comments"][:1]}}), "total_count")),
    ("r834_refs_thua", _r834_ca(11, lambda x, w, h: x["bnc"]["bang_lop"][0]["connector_refs"].append(["review_comments", 12]), "phủ ĐÚNG", p3_cn=True)),
    ("r834_state_required_checks_rong", _r834_ca(8, _r834_state(ngu_canh_lease={"required_checks": []}), "state hỏng")),
    ("r834_state_p3_sai_kieu", _r834_ca(8, _r834_state(bien_nhan_approve={"p3": ""}), "state hỏng")),
]
MUTANTS.update({
    "r834_bo_kiem_gate": ("        cmd_kiem_gate(argparse.Namespace(head=h, check_suite=str(suite), bat_buoc=ten_bb, check_runs=a.check_runs), state_dir)", "        pass",
                          ["r834_check_noi_do"]),
    "r834_bo_check_moi_nhat": ('            if r["id"] != max(x["id"] for x in cr.values() if x["name"] == ten_j and x["check_suite"]["id"] == suite):', "            if False:",
                               ["r834_check_noi_do_bi_che"]),
    "r834_check_run_khong_nhat_quan": ('    cr = {r["id"]: r for r in _trang_du(_doc_json(a.check_runs, RC_GATE)[0], "check_runs", "check_runs")}',
                                       '    cr = {r["id"]: r for r in _doc_check_runs(a.check_runs)}', ["r834_check_cung_id_khac_app"]),
    "r834_bo_khop_attempt_job": ('(j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)',
                                 '(j.get("run_id"), j.get("head_sha"), j.get("name")) == (run["id"], h, ten_j)', ["r834_attempt_moi_job_cu"]),
    "r834_run_cu_nhat": ("run = max(ung, key=lambda r: r[\"id\"])", "run = min(ung, key=lambda r: r[\"id\"])", ["r834_run_moi_nhat_do"]),
    "r834_bo_kho_url_job": ("re.escape(API_GH + nc['repo'])", "'https://api\\\\.github\\\\.com/repos/[^/]+/[^/]+'", ["r834_job_url_kho_khac"]),
    "r834_noi_check_theo_ten": ("            r = next((x for i, x in cr.items() if str(i) == m[1]), None) if m else None", '            r = next((x for x in cr.values() if x["name"] == ten_j), None)',
                                ["r834_job_tro_check_khong_co", "r834_job_url_qua_dai"]),
    "r834_jobs_total_toan_cuc": ('    jobs = _trang_du({"total_count": len({j["id"] for j in moi_tep}), "jobs": moi_tep}, "jobs", "workflow_jobs (gộp các tệp)")',
                                 '    jobs = _trang_du([_doc_json(f, RC_GATE)[0] for f in a.workflow_jobs], "jobs", "workflow_jobs")', ["r834_hai_tep_jobs"]),
    "r834_badge_chi_P": ('BADGE_RE = re.compile(r"!\\[([^\\]]*?)\\s*Badge\\]", re.I)', 'BADGE_RE = re.compile(r"!\\[(P[^\\]\\s]*) Badge\\]")', ["r834_badge_ngoai_mien_review"]),
    "r834_changes_khong_hang_lot": (' or x.get("state") == "CHANGES_REQUESTED"):', "):", ["r834_review_changes_khong_hang"]),
    "r834_commit_thieu_la_cu": ('"hien" if c == head else "cu" if type(c) is str and SHA_RE.fullmatch(c) else "hong"', '"hien" if c == head else "cu"', ["r834_review_comment_thieu_commit"]),
    "r834_reviewed_commit_tim_dau": ('    khai = [re.fullmatch(r"(`?)([0-9a-f]{7,40})\\1", t.strip()) for t in re.findall(r"Reviewed commit:(?:\\*\\*)?([^\\n]*)", x["body"])]',
                                     '    khai = [re.search(r"`?([0-9a-f]{7,40})", t) for t in re.findall(r"Reviewed commit:(?:\\*\\*)?([^\\n]*)", x["body"])][:1]', ["r834_reviewed_commit_sai_dang", "r834_reviewed_commit_mau_thuan"]),
    "r834_head_cu_van_chan": ("            if n is None and hang:", "            if n != \"hien\" and hang:", ["r834_issue_comment_head_cu_khong_chan"]),
    "r834_bo_envelope": ('    if not isinstance(d, dict) or (d.get("repo"), d.get("pr"), d.get("head_sha")) != (repo, pr, head):', "    if not isinstance(d, dict):",
                         ["r834_envelope_head_khac"]),
    "r834_bo_total_count": (' or {t["total_count"] for t in cac} != {len({x["id"] for x in ds})}', "", ["r834_trang_thieu"]),
    "r834_bo_phu_dung_refs": (" or sorted(refs) != sorted(p3):", ":", ["r834_refs_thua"]),
    "r834_bo_luoc_do_state": ('    if not {tuple(x) for x in CHECK_BAT_BUOC} <= {tuple(x) for x in nc["required_checks"]} or type(p3_off) is not list \\',
                              "    if False \\", ["r834_state_required_checks_rong", "r834_state_p3_sai_kieu"]),
})


# #834 lượt 3 — Codex lượt 2: F1 neo head (trường trọn, tiền tố mơ hồ) · F2 độ phủ (I5 gọi `_xet_dung` sau đầu vào, repo/head run,
# head job, quyết định P3 trùng, generation H connector) · F3 lược đồ job. `_VO834` bọc CLI, thay `_xet_dung` bằng cọc đo lời gọi.
_VO834 = ("import sys, importlib.util as u\nfrom pathlib import Path\nkb = sys.argv.pop(next(i for i, x in enumerate(sys.argv) if x.endswith('packet_loop.py')))\n"
          "sys.path.insert(0, str(Path(kb).parent)); s = u.spec_from_file_location('pl', kb); m = u.module_from_spec(s); s.loader.exec_module(m)\n"
          "def coc(sd, st, cua, *a, **k):\n    if cua == 'accept':\n        print('COC_XET_DUNG', file=sys.stderr); sys.exit(3)\n"
          "m._xet_dung = coc\nsys.exit(m.main(sys.argv[1:]))\n")
CASES += [
    ("r834_reviewed_commit_span_thua", _r834_ca(12, lambda x, w, h: x["issue_comments"][0].update(body=f"Reviewed commit: `{h[:10]} invalid`"), "thiếu/sai/mơ hồ")),
    ("r834_tien_to_mo_ho", _r834_ca(12, lambda x, w, h: _R834_RV("CHANGES_REQUESTED", "![P1 Badge] bug")(x, w, h) or x["reviews"][-1].update(
        commit_id=h[:10] + ("f" * 30 if h[10:] != "f" * 30 else "e" * 30)), "thiếu/sai/mơ hồ")),
    ("r834_xet_dung_duoc_goi", _r834_ca(3, None, "COC_XET_DUNG", vo=True)),
    ("r834_xet_dung_sau_dau_vao", _r834_ca(12, lambda x, w, h: x.update(hong=True), "KHÔNG ĐO ĐƯỢC", vo=True)),
    ("r834_run_kho_khac", _r834_ca(12, _S834("runs", 0, repository={"full_name": "x/r"}), "VẮNG")),
    ("r834_run_head_khac", _r834_ca(12, _S834("runs", 0, head_sha="0" * 40), "VẮNG")),
    ("r834_job_head_khac", _r834_ca(12, _S834("jobs", 1, head_sha="0" * 40), "VẮNG")),
    ("r834_qd_trung", _r834_ca(2, lambda x, w, h: x["qd"].append(dict(x["qd"][0])), "P3 còn mở", lop=(("a-b", "P3"),))),
    ("r834_bnc_lech_generation", _r834_ca(11, lambda x, w, h: x["bnc"].update(generation=2), "generation", p3_cn=True)),
    ("r834_job_attempt_bool", _r834_ca(12, _S834("jobs", 0, run_attempt=True), "int thật")),
    ("r834_job_run_id_float", _r834_ca(12, _S834("jobs", 0, run_id=100.0), "int thật")),
    ("r834_job_url_qua_dai", _r834_ca(12, _S834("jobs", 0, check_run_url=f"{_API834}check-runs/" + "3" * 5000), "không trỏ check-run")),
]
MUTANTS["r812_bo_generation"][2].append("r834_bnc_lech_generation")
MUTANTS.update({
    "r834_bo_dau_hang_tron": ('    khai = [re.fullmatch(r"(`?)([0-9a-f]{7,40})\\1", t.strip())', '    khai = [re.match(r"`?()([0-9a-f]{7,40})", t.strip())', ["r834_reviewed_commit_span_thua"]),
    "r834_bo_tien_to_mo_ho": (" or any(head.startswith(t[2]) and any(b != head and b.startswith(t[2]) for b in biet) for t in khai):", ":", ["r834_tien_to_mo_ho"]),
    "r834_bo_goi_xet_dung": ('    _xet_dung(state_dir, st, "accept")\n', "", ["r834_xet_dung_duoc_goi"]),
    "r834_xet_dung_truoc_dau_vao": (('    _xet_dung(state_dir, st, "accept")\n', '    sha_ci = _kiem_ci(a, nc, h, state_dir)\n'),  # gỡ lời gọi gốc TRƯỚC, rồi chèn
                                    ("", '    _xet_dung(state_dir, st, "accept")\n    sha_ci = _kiem_ci(a, nc, h, state_dir)\n'), ["r834_xet_dung_sau_dau_vao"]),
    "r834_bo_kho_run": (' and isinstance(r.get("repository"), dict) and r["repository"].get("full_name") == nc["repo"]]', "]", ["r834_run_kho_khac"]),
    "r834_bo_head_run": ('r.get("path") == wf and r.get("head_sha") == h and ', 'r.get("path") == wf and ', ["r834_run_head_khac"]),
    "r834_bo_head_job": ('(j.get("run_id"), j.get("run_attempt"), j.get("head_sha"), j.get("name")) == (run["id"], run["run_attempt"], h, ten_j)',
                         '(j.get("run_id"), j.get("run_attempt"), j.get("name")) == (run["id"], run["run_attempt"], ten_j)', ["r834_job_head_khac"]),
    "r834_qd_theo_tap": ('or sorted((q["nguon"], q["khoa"]) for q in qd) != sorted(con_mo)):', 'or {(q["nguon"], q["khoa"]) for q in qd} != con_mo):', ["r834_qd_trung"]),
    "r834_bo_kieu_job": ('    if not all(type(j.get("run_id")) is int and type(j.get("run_attempt")) is int and j["run_attempt"] > 0\n', "    if False and all(True\n",
                         ["r834_job_attempt_bool", "r834_job_run_id_float"]),
})


def chay_suite(script: Path, tmp: Path, chi_chay=None):
    ket = {}
    for ten, fn in CASES:
        if chi_chay and ten not in chi_chay:
            continue
        if ten in WINDOWS_ONLY and platform.system() != "Windows":
            ket[ten] = BoQua("chỉ đo lệnh pwsh trên Windows")
            continue
        d = tmp / ten
        d.mkdir(parents=True, exist_ok=True)
        try:
            fn(Ctx(script, d))
            ket[ten] = None
        except BoQua as ex:
            ket[ten] = (_TinDungGia(f"{type(ex).__name__}: {ex}") if _co_sap_do(ex) else
                        ex if isinstance(ex.__cause__, OSError) else f"BỎ QUA không có OSError đo được: {ex}")
        except Exception as ex:  # noqa: BLE001 — ca đỏ là dữ liệu, không phải sự cố
            ket[ten] = (_TinDungGia if _co_sap_do(ex) else str)(f"{type(ex).__name__}: {ex}")
    return ket



def main() -> int:
    _ = [s.reconfigure(encoding="utf-8", errors="backslashreplace")
         for s in (sys.stdout, sys.stderr) if hasattr(s, "reconfigure")]
    goc = CANONICAL.read_text(encoding="utf-8")
    goc_test = Path(__file__).read_text(encoding="utf-8")
    that_bai_tong = 0

    with tempfile.TemporaryDirectory(prefix="packet_loop_test_") as td:
        tmp = Path(td)

        # --- 1. nền: mọi ca phải XANH -----------------------------------------
        ket = chay_suite(CANONICAL, tmp / "baseline")
        bo_qua = {ten: ex for ten, ex in ket.items() if isinstance(ex, BoQua)}
        dat = sum(1 for v in ket.values() if v is None)
        tong = len(ket) - len(bo_qua)
        for ten, loi in ket.items():
            if isinstance(loi, BoQua):
                print(f"  BỎ QUA  {ten}: {loi}")
            elif loi:
                print(f"  ĐỎ  {ten}: {loi}")
        print(f"nền: {dat}/{tong} đạt · BỎ QUA: {len(bo_qua)}")
        that_bai_tong += tong - dat

        # --- 2. AC 19: MỖI lớp lách phải có một ca bắt-oan ---------------------
        # Không có chốt này thì "mỗi lớp một ca" chỉ là lời hứa: thêm một lớp mà
        # quên ca bắt-oan sẽ đi lọt trong im lặng (finding
        # `ac19-false-positive-matrix-incomplete`).
        print("\nAC 19 — ánh xạ lớp lách → ca bắt-oan:")
        ten_ca_oan = {f"ac19_{t}" for t, _ in LOP_BAT_OAN}
        thieu_anh_xa = [t for t, _ in LOP_LACH if t not in ANH_XA_LOP_BAT_OAN]
        tro_hong = {k: v for k, v in ANH_XA_LOP_BAT_OAN.items()
                    if f"ac19_{v}" not in ten_ca_oan}
        thua_anh_xa = [k for k in ANH_XA_LOP_BAT_OAN
                       if k not in {t for t, _ in LOP_LACH}]
        if thieu_anh_xa:
            print(f"  ĐỎ  {len(thieu_anh_xa)} lớp KHÔNG có ca bắt-oan: {thieu_anh_xa}")
            that_bai_tong += len(thieu_anh_xa)
        if tro_hong:
            print(f"  ĐỎ  ánh xạ trỏ vào ca KHÔNG TỒN TẠI: {tro_hong}")
            that_bai_tong += len(tro_hong)
        if thua_anh_xa:
            print(f"  ĐỎ  ánh xạ khai lớp không còn trong LOP_LACH: {thua_anh_xa}")
            that_bai_tong += len(thua_anh_xa)
        if not (thieu_anh_xa or tro_hong or thua_anh_xa):
            print(f"  ok  {len(LOP_LACH)}/{len(LOP_LACH)} lớp lách đều có ca bắt-oan "
                  f"({len(set(ANH_XA_LOP_BAT_OAN.values()))} ca riêng biệt)")

        # --- 3. tự chứng minh không rỗng, ĐO CẢ HAI VẾ ------------------------
        #
        # Finding `ac18-mutation-not-per-class`: generation 4 chỉ chạy tập `phai_chet`
        # do chính đột biến tự khai, nên nó chứng minh "ca đích chết" mà KHÔNG chứng
        # minh "và ĐÚNG ca đó" — một đột biến giết sạch mọi thứ cũng qua trót lọt.
        #
        # ĐÃ THỬ VÀ BỎ cách hiển nhiên — chạy TOÀN BỘ suite dưới mỗi đột biến rồi đòi
        # không ca nào ngoài `phai_chet` chết. Đo ra thì nó SAI DẠNG: đột biến
        # `init_tu_cap_lease_nhu_bug_goc` giết 42 ca, vì gần như mọi ca đều gọi
        # `c.init()` làm bước dựng nền. Đó là phụ thuộc FIXTURE, không phải "đo chung
        # một chốt" — phạt nó chỉ ép người viết làm YẾU chính những đột biến tốt nhất.
        #
        # Thứ vừa đo được vừa đúng ý AC 18 là ĐỐI CHỨNG KHÁC HỌ: một đột biến ở tầng
        # doctrine KHÔNG được đụng tới máy trạng thái, và ngược lại. Đụng nghĩa là nó
        # không nhắm đúng tầng nó khai.
        print("\ntự chứng minh suite KHÔNG RỖNG (ca đích ĐỎ · đối chứng khác họ XANH):")
        for ten_mut, (tim, thay, phai_chet) in MUTANTS.items():
            cap = _cap_thay_the(tim, thay)
            than, dot_bien_test, thieu = _phan_loai_dot_bien(
                ten_mut, cap, goc, goc_test)
            if thieu:
                print(f"  ĐỎ  đột biến {ten_mut}: không tìm thấy mỏ neo {thieu!r}")
                that_bai_tong += len(thieu)
                continue
            mut_dir = tmp / f"mut_{ten_mut}"
            mut_dir.mkdir(parents=True, exist_ok=True)
            mut = mut_dir / "packet_loop.py"
            for t, th in cap:
                than = than.replace(t, th, 1)
            mut.write_text(goc if dot_bien_test else than, encoding="utf-8", newline="\n")
            (mut_dir / "launcher.py").write_text(
                (HERE / "launcher.py").read_text(encoding="utf-8"), encoding="utf-8")
            suite = sys.modules[__name__]
            if dot_bien_test:
                test_mut = mut_dir / "packet_loop_test.py"
                test_mut.write_text(than, encoding="utf-8", newline="\n")
                spec = importlib.util.spec_from_file_location(f"packet_loop_test_{ten_mut}", test_mut)
                suite = importlib.util.module_from_spec(spec)
                spec.loader.exec_module(suite)
            doi_chung = suite._doi_chung_khac_ho(phai_chet)
            ket_mut = suite.chay_suite(mut, mut_dir,
                                       chi_chay=set(phai_chet) | set(doi_chung))
            bo_qua_mut = [t for t in phai_chet
                           if isinstance(ket_mut.get(t), suite.BoQua)]
            song = [t for t in phai_chet if ket_mut.get(t) is None]
            oan = [t for t in doi_chung if ket_mut.get(t) is not None]
            gia = [t for t in phai_chet if suite._phan_loai_giet(ket_mut.get(t)) == "TIN_DUNG_GIA"]
            if song:
                print(f"  ĐỎ  đột biến {ten_mut}: ca {song} VẪN XANH ⇒ ca đó không đo gì")
                that_bai_tong += len(song)
            if gia:   # #822 M6
                print(f"  ĐỎ  đột biến {ten_mut}: ca {gia} chỉ chết vì CLI SẬP ⇒ TÍN DỤNG GIẢ, không phải giết")
                that_bai_tong += len(gia)
            if oan:
                print(f"  ĐỎ  đột biến {ten_mut}: giết cả ĐỐI CHỨNG KHÁC HỌ {oan} ⇒ "
                      f"đột biến không nhắm đúng tầng nó khai")
                that_bai_tong += len(oan)
            if bo_qua_mut:
                print(f"  BỎ QUA  đột biến {ten_mut}: ca {bo_qua_mut} không được tính là đã giết")
            if not song and not oan and not bo_qua_mut and not gia:
                print(f"  ok  {ten_mut} → giết {len(phai_chet)} ca đích · "
                      f"{len(doi_chung)} đối chứng khác họ còn sống")

        # --- 4. MỖI LỚP LÁCH phải có đột biến của nó -------------------------
        #
        # AC 18 nói về LỚP LÁCH: *"Mỗi lớp trong danh sách phải có một ca phản chứng
        # và một đột biến giết đúng ca đó."* Generation 4 để `nbsp_phu_ba_lop` ngoài
        # mọi danh sách phải-chết mà không ai thấy — chốt này làm chuyện đó không im
        # lặng được nữa.
        #
        # PHẠM VI CÓ CHỦ Ý, nói rõ để không ai tưởng là bỏ sót: chốt chỉ áp cho các ca
        # sinh từ `LOP_LACH` (`ac18_*`). ĐÃ THỬ áp cho MỌI ca và nó sai dạng — 65 ca
        # bị báo, gần hết là ca CHIỀU THA (`ac19_oan_*`, `*_hop_le_*`, `*_sach_xanh`)
        # vốn khẳng định `rc=0`. Một đột biến GỠ chốt không thể giết ca chiều tha; thứ
        # giết được nó là đột biến SIẾT THÊM, một loại khác hẳn. Ép mỗi ca chiều tha
        # có một đột biến sẽ đẻ ra hàng chục đột biến giả chỉ để lấp bảng — làm suite
        # dài ra mà không đo thêm gì. Giá trị của ca chiều tha được chứng minh theo
        # đường khác: chúng ĐỎ ngay khi một chốt siết quá tay, và `bo_mien_tru_ngat_dong`
        # là ví dụ đang chạy.
        print("\nAC 18 — mỗi LỚP LÁCH phải có đột biến của nó:")
        co_dot_bien = {t for _, (_, _, ds) in MUTANTS.items() for t in ds}
        ten_ca_lop = [f"ac18_{t}" for t, _ in LOP_LACH]
        # KHÔNG còn cửa ngoại lệ: mọi lớp trong `LOP_LACH` phải có một đột biến giết
        # được ca của nó. Lớp bị nhiều đường cùng phủ thì dùng đột biến PHỐI HỢP, chứ
        # không được khai miễn (bài học lượt 7 — xem `_cap_thay_the`).
        mo_coi = [t for t in ten_ca_lop if t not in co_dot_bien]
        if mo_coi:
            print(f"  ĐỎ  {len(mo_coi)} lớp KHÔNG đột biến nào giết: {mo_coi}")
            that_bai_tong += len(mo_coi)
        else:
            phoi_hop = sum(1 for _t, (tim, _th, _d) in MUTANTS.items()
                           if not isinstance(tim, str))
            print(f"  ok  {len(ten_ca_lop)} lớp lách đều có đột biến giết · "
                  f"{phoi_hop} đột biến PHỐI HỢP · 0 ngoại lệ")

    # --- 5. SUITE PHẢI TỰ KHAI SỐ CỦA MÌNH ---------------------------------
    #
    # Cross-review lượt 9, finding `packet-suite-mutation-count-mismatch`: hồ sơ
    # executor khai `39 đột biến`, `len(MUTANTS)` thật là `38`. Con số lệch một thì
    # nhỏ, nhưng chỗ hở nó phơi ra thì không: **suite KHÔNG assert con số nó khai**.
    # Một bộ test dựng lên để chống lời khai sai lại không chặn được lời khai sai của
    # chính người viết nó — và con số ấy đã đi vào cả commit message lẫn tệp lease.
    #
    # Chữa bằng cách bắt suite IN RA con số đếm bằng máy, ở dòng cuối, cùng chỗ với
    # các số khác. Ai chép số vào hồ sơ thì chép từ đây, không gõ tay.
    print(f"\nSỐ LIỆU (đếm bằng máy — chép vào hồ sơ TỪ ĐÂY, đừng gõ tay):")
    print(f"  ca               : {len(CASES)}")
    print(f"  đột biến         : {len(MUTANTS)}")
    print(f"  lớp lách         : {len(LOP_LACH)}")
    print(f"  ca bắt-oan       : {len(LOP_BAT_OAN)}")
    print(f"  ngoại lệ AC 18   : 0")

    print(f"\nTỔNG: {'ĐẠT' if that_bai_tong == 0 else f'{that_bai_tong} lỗi'}")
    return 0 if that_bai_tong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
