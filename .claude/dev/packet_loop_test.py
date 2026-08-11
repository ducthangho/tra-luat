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

import os
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
CANONICAL = HERE / "packet_loop.py"
ROOT = HERE.parents[1]

EXECUTOR = "claude"
REVIEWER = "codex"


# --- hạ tầng ------------------------------------------------------------------


def run(script: Path, args, state_dir=None, env_extra=None):
    cmd = [sys.executable, str(script)]
    if state_dir is not None:
        cmd += ["--state-dir", str(state_dir)]
    cmd += [str(x) for x in args]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONIOENCODING", None)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(cmd, capture_output=True, env=env)
    return p.returncode, p.stdout, p.stderr


def _txt(b: bytes) -> str:
    return b.decode("utf-8", "replace").strip()


def _doi(expect: int, rc: int, err: bytes, msg: str) -> None:
    if rc != expect:
        raise AssertionError(f"{msg}: đòi rc={expect}, được rc={rc}; stderr={_txt(err)!r}")


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

    def init(self, sd: Path, packet=55, executor=EXECUTOR, reviewer=REVIEWER, extra=()):
        return run(
            self.script,
            ["init", "--packet", packet, "--mission", 54,
             "--executor", executor, "--reviewer", reviewer, *extra],
            sd,
        )

    def head(self, luot: int) -> str:
        """Head giả nhưng ĐÚNG DẠNG git oid, khác nhau theo lượt."""
        return f"{luot:040x}"

    def den_reviewing(self, sd: Path, packet: int, luot: int):
        """begin-attempt → record-post → transition reviewing (neo head của lượt)."""
        rc, _, e = run(self.script, ["begin-attempt", "--packet", packet, "--provider", EXECUTOR], sd)
        _doi(0, rc, e, f"begin-attempt lượt {luot}")
        cid = str(9_000_000_000 + packet * 1000 + luot * 2)
        rc, _, e = run(self.script,
                       ["record-post", "--packet", packet, "--for", "reviewing", "--comment-id", cid], sd)
        _doi(0, rc, e, f"record-post lượt {luot}")
        rc, _, e = run(self.script,
                       ["transition", "--packet", packet, "--to", "reviewing",
                        "--comment-id", cid, "--head-sha", self.head(luot)], sd)
        _doi(0, rc, e, f"transition reviewing lượt {luot}")
        return cid

    def review(self, sd, packet, ids, verdict="changes_requested", descs=(), luot=1, sha=None):
        args = ["record-review", "--packet", packet, "--provider", REVIEWER, "--verdict", verdict,
                "--reviewed-sha", self.head(luot) if sha is None else sha]
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
                   ["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "5258163128"], sd)
    _doi(5, rc, e, "ID chưa ghi sổ phải bị từ chối")


def case_comment_id_dung_lai_bi_tu_choi(c: Ctx):
    """Cùng một ID dùng cho transition THỨ HAI phải bị từ chối."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    c.den_reviewing(sd, 55, 1)
    cid_run = "7770000001"
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "running", "--comment-id", cid_run], sd)
    _doi(0, rc, e, "record-post running")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "running", "--comment-id", cid_run], sd)
    _doi(0, rc, e, "transition running lần 1")
    # vòng hai: quay lại reviewing (không cần lượt mới) rồi thử tiêu thụ LẠI ID cũ
    rc, _, e = run(c.script,
                   ["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000013"], sd)
    _doi(0, rc, e, "record-post reviewing vòng 2")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "reviewing",
                    "--comment-id", "7770000013", "--head-sha", c.head(1)], sd)
    _doi(0, rc, e, "transition reviewing vòng 2")
    rc, _, e = run(c.script,
                   ["transition", "--packet", 55, "--to", "running", "--comment-id", cid_run], sd)
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
                   ["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000002"], sd)
    _doi(5, rc, e, "ID đăng ký cho transition khác không dùng chéo được")


def case_thieu_comment_id_chan_transition(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script, ["transition", "--packet", 55, "--to", "reviewing"], sd)
    _doi(5, rc, e, "chưa đăng comment thì transition phải bị chặn")


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


# --- §8 quota không tiêu thụ attempt -------------------------------------------


def case_void_attempt_allowlist(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota"], sd)
    _doi(0, rc, e, "quota phải hoàn được lượt")


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


def _repo_gia(tmp: Path, noi_dung: str, ten="demo") -> Path:
    r = tmp / f"repo_{abs(hash(noi_dung)) % 10**8}_{ten}"
    d = r / ".claude" / "skills" / ten
    d.mkdir(parents=True, exist_ok=True)
    (d / "SKILL.md").write_text(noi_dung, encoding="utf-8", newline="\n")
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


def case_doctrine_scan_repo_that_sach(c: Ctx):
    """Adapter THẬT trong kho này phải sạch — nếu không thì tiêu chí là lời hứa."""
    rc, o, e = run(c.script, ["doctrine-scan", "--root", ROOT])
    _doi(0, rc, e, f"adapter thật phải sạch; stderr={_txt(e)}")


# --- (d) stdout an toàn dưới codepage không UTF-8 ------------------------------


def _kich_ban_in(c: Ctx, codepage: str):
    """Chạy MỌI lệnh in tiếng Việt với stdout BỊ CAPTURE và encoding ép về codepage."""
    env = {"PYTHONIOENCODING": codepage}
    sd = c.sd()
    r = _repo_gia(c.tmp, SACH, ten=f"cp{codepage}")

    buoc = [
        (["where"], None),
        (["init", "--packet", 55, "--mission", 54,
          "--executor", EXECUTOR, "--reviewer", REVIEWER], sd),
        (["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd),
        (["next-comment", "--packet", 55], sd),
        (["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000009"], sd),
        (["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000009",
          "--head-sha", "%040x" % 1], sd),
        (["record-review", "--packet", 55, "--provider", REVIEWER, "--verdict", "changes_requested",
          "--reviewed-sha", "%040x" % 1,
          "--finding-id", "loi-co-dau-tieng-viet", "--finding-desc", "mô tả có dấu tiếng Việt"], sd),
        (["status", "--packet", 55], sd),
        (["doctrine-scan", "--root", r], None),
    ]
    for args, state_dir in buoc:
        rc, o, e = run(c.script, args, state_dir, env_extra=env)
        ten = args[0]
        if rc != 0:
            raise AssertionError(
                f"[{codepage}] lệnh {ten!r} phải rc=0 khi stdout bị capture, được rc={rc}; "
                f"stderr={_txt(e)!r}"
            )
        if not o.strip():
            raise AssertionError(f"[{codepage}] lệnh {ten!r} rc=0 nhưng stdout RỖNG")


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


CASES = [
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
    ("guard_khong_co_co_noi", case_guard_khong_co_co_noi),
    ("transition_hop_le_rc0", case_transition_hop_le_rc0),
    ("comment_id_chua_dang_ky_bi_tu_choi", case_comment_id_chua_dang_ky_bi_tu_choi),
    ("comment_id_dung_lai_bi_tu_choi", case_comment_id_dung_lai_bi_tu_choi),
    ("comment_id_sai_transition_bi_tu_choi", case_comment_id_sai_transition_bi_tu_choi),
    ("thieu_comment_id_chan_transition", case_thieu_comment_id_chan_transition),
    ("record_post_id_sai_dang_bi_tu_choi", case_record_post_id_sai_dang_bi_tu_choi),
    ("record_post_trung_id_bi_tu_choi", case_record_post_trung_id_bi_tu_choi),
    ("transition_khong_hop_le_thoat_8", case_transition_khong_hop_le_thoat_8),
    ("void_attempt_allowlist", case_void_attempt_allowlist),
    ("void_attempt_ly_do_tu_che_bi_tu_choi", case_void_attempt_ly_do_tu_che_bi_tu_choi),
    ("void_sau_review_bi_chan", case_void_sau_review_bi_chan),
    ("doctrine_scan_sach_xanh", case_doctrine_scan_sach_xanh),
    ("doctrine_scan_bom_cum_tu_do", case_doctrine_scan_bom_cum_tu_do),
    ("doctrine_scan_repo_that_sach", case_doctrine_scan_repo_that_sach),
    ("stdout_cp1252", case_stdout_cp1252),
    ("stdout_cp1258", case_stdout_cp1258),
    ("cross_review_co_cu_phap_ghi_verdict_len_pr", case_cross_review_co_cu_phap_ghi_verdict_len_pr),
    ("land_packets_khong_tu_trigger", case_land_packets_khong_tu_trigger),
]

# Đột biến nới ngưỡng: mỗi cái BẮT BUỘC giết đúng những ca dưới đây. Ca không
# chết được nghĩa là nó không đo cái nó khai.
MUTANTS = {
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
    "bo_cung_hoa_stdout": (
        "\n    _cung_hoa_stdout()\n",
        "\n    pass  # đột biến: bỏ cứng hoá stdout\n",
        ["stdout_cp1252", "stdout_cp1258"],
    ),
}


def chay_suite(script: Path, tmp: Path, chi_chay=None):
    ket = {}
    for ten, fn in CASES:
        if chi_chay and ten not in chi_chay:
            continue
        d = tmp / ten
        d.mkdir(parents=True, exist_ok=True)
        try:
            fn(Ctx(script, d))
            ket[ten] = None
        except Exception as ex:  # noqa: BLE001 — ca đỏ là dữ liệu, không phải sự cố
            ket[ten] = f"{type(ex).__name__}: {ex}"
    return ket


def main() -> int:
    _ = [s.reconfigure(encoding="utf-8", errors="backslashreplace")
         for s in (sys.stdout, sys.stderr) if hasattr(s, "reconfigure")]
    goc = CANONICAL.read_text(encoding="utf-8")
    that_bai_tong = 0

    with tempfile.TemporaryDirectory(prefix="packet_loop_test_") as td:
        tmp = Path(td)

        # --- 1. nền: mọi ca phải XANH -----------------------------------------
        ket = chay_suite(CANONICAL, tmp / "baseline")
        dat = sum(1 for v in ket.values() if v is None)
        tong = len(ket)
        for ten, loi in ket.items():
            if loi:
                print(f"  ĐỎ  {ten}: {loi}")
        print(f"nền: {dat}/{tong} đạt")
        that_bai_tong += tong - dat

        # --- 2. tự chứng minh không rỗng --------------------------------------
        print("\ntự chứng minh suite KHÔNG RỖNG (nới ngưỡng ⇒ ca tương ứng phải ĐỎ):")
        for ten_mut, (tim, thay, phai_chet) in MUTANTS.items():
            if tim not in goc:
                print(f"  ĐỎ  đột biến {ten_mut}: không tìm thấy mỏ neo {tim!r}")
                that_bai_tong += 1
                continue
            mut_dir = tmp / f"mut_{ten_mut}"
            mut_dir.mkdir(parents=True, exist_ok=True)
            mut = mut_dir / "packet_loop.py"
            mut.write_text(goc.replace(tim, thay, 1), encoding="utf-8", newline="\n")
            ket_mut = chay_suite(mut, mut_dir, chi_chay=set(phai_chet))
            song = [t for t in phai_chet if ket_mut.get(t) is None]
            if song:
                print(f"  ĐỎ  đột biến {ten_mut}: ca {song} VẪN XANH ⇒ ca đó không đo gì")
                that_bai_tong += len(song)
            else:
                print(f"  ok  {ten_mut} → giết {len(phai_chet)}/{len(phai_chet)} ca: {', '.join(phai_chet)}")

    print(f"\nTỔNG: {'ĐẠT' if that_bai_tong == 0 else f'{that_bai_tong} lỗi'}")
    return 0 if that_bai_tong == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
