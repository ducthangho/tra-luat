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

import json
import os
import platform
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


BIEN_BC = "TL_MOI_TRUONG_JSON"
_ANH_SACH = []


def anh_moi_truong_sach(**doi) -> str:
    """Ảnh `doctor --json` HỢP LỆ, dùng chung. `doi` để bẻ đúng một chiều làm ca đỏ."""
    d = {"thieu_bat_buoc": [], "chua_xac_thuc": [], "he_dieu_hanh": platform.system(),
         "ok": True, "ok_kha_dung": True}
    d.update(doi)
    if not doi and _ANH_SACH:
        return _ANH_SACH[0]
    f = Path(tempfile.mkdtemp(prefix="tl-mt-")) / "doctor.json"
    f.write_text(json.dumps(d), encoding="utf-8")
    if not doi:
        _ANH_SACH.append(str(f))
    return str(f)


def run(script: Path, args, state_dir=None, env_extra=None):
    cmd = [sys.executable, str(script)]
    if state_dir is not None:
        cmd += ["--state-dir", str(state_dir)]
    cmd += [str(x) for x in args]
    env = os.environ.copy()
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    env.pop("PYTHONIOENCODING", None)
    # `begin-attempt` nay ĐÒI ảnh môi trường. 33 chỗ gọi nó ở dưới KHÔNG đo chốt ấy, nên
    # tiêm một ảnh SẠCH mặc định thay vì sửa 33 dòng. `env_extra` ghi đè được, để ca nào
    # ĐO chính chốt ấy vẫn nhìn thấy trạng thái thiếu/hỏng.
    env[BIEN_BC] = anh_moi_truong_sach()
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

    def init(self, sd: Path, packet=55, executor=EXECUTOR, reviewer=REVIEWER, extra=(),
             lease=True):
        """init, rồi GHI LUÔN một lease hợp lệ (mặc định).

        `init` chỉ đưa packet tới `awaiting_lease`, nên phần lớn ca ở dưới — vốn đo
        hành vi HẠ NGUỒN của lease — cần một lease thật để đi tiếp. Ca nào đo chính
        cái chốt lease thì truyền `lease=False` để nhìn thấy trạng thái chưa có lease.
        """
        rc, o, e = run(
            self.script,
            ["init", "--packet", packet, "--mission", 54,
             "--executor", executor, "--reviewer", reviewer, *extra],
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


def case_mt_thieu_cong_cu_thi_khong_mo_duoc_luot(c: Ctx):
    """N1 — lượt chết vì thiếu công cụ KHÔNG được tiêu một attempt."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    anh = anh_moi_truong_sach(thieu_bat_buoc=["rg"])
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR],
                   sd, env_extra={BIEN_BC: anh})
    _doi(10, rc, e, "thiếu công cụ bắt buộc mà vẫn mở được lượt")
    assert b"rg" in e, f"thông điệp không nêu công cụ thiếu: {e!r}"
    st = json.loads((sd / "wp55.json").read_text(encoding="utf-8"))
    assert st["attempts_used"] == 0, f"attempt bị TIÊU dù từ chối: {st['attempts_used']}"


def case_mt_sach_thi_van_mo_duoc_luot(c: Ctx):
    """N2 — chiều BẮT OAN. Ca chiều-tha chỉ chết bởi đột biến SIẾT THÊM."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, o, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "ảnh môi trường SẠCH mà vẫn bị chặn")
    assert b"1/3" in o, f"không mở đúng lượt 1: {o!r}"


def case_mt_chup_tren_nen_khac_thi_tu_choi(c: Ctx):
    """N3 — ảnh chụp trên MÁY KHÁC là lời khai về máy khác."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    anh = anh_moi_truong_sach(he_dieu_hanh="Plan9")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR],
                   sd, env_extra={BIEN_BC: anh})
    _doi(10, rc, e, "ảnh chụp nền khác mà vẫn mở được lượt")


def case_mt_anh_hong_la_KHONG_DOC_DUOC_khong_phai_thieu(c: Ctx):
    """N7 — trạng thái THỨ BA có tên riêng; gộp vào `khong` là nói sai chỗ cần sửa."""
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    f = Path(tempfile.mkdtemp(prefix="tl-mt-hong-")) / "doctor.json"
    f.write_text("{ khong phai json", encoding="utf-8")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR],
                   sd, env_extra={BIEN_BC: str(f)})
    _doi(10, rc, e, "ảnh hỏng cú pháp mà vẫn mở được lượt")
    assert "KHÔNG ĐỌC ĐƯỢC".encode() in e, f"gộp nhầm vào THIẾU: {e!r}"
def case_luong_canonical_chay_that(c: Ctx):
    """N10′ — CHẠY khối §7.4a chứ không khớp chuỗi (`doctor --json >` cắt cụt vẫn qua phép
    khớp). Khối là PowerShell dùng `$env:TEMP` nên chỉ đo thật trên Windows; nền khác BỎ QUA
    CÓ IN LÝ DO."""
    ke = ROOT / "ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md"
    if not ke.is_file():                       # chỉ tha bản sao rời (không có `.git`)
        assert not (ROOT / ".git").exists(), f"trong kho thật mà thiếu {ke}"
        return
    i = (s := ke.read_text(encoding="utf-8")).find("```powershell", s.find("#### 7.4a"))
    assert i != -1, "không thấy khối lệnh §7.4a — tài liệu đổi cấu trúc, ca này mù"
    dau = (k := s[i + 13:s.find("```", i + 13)])[:k.find("record-post")].rsplit("python", 1)[0]
    if os.name != "nt":
        print(f"  BO QUA n10 (nen {os.name}): khoi la PowerShell dung $env:TEMP", flush=True)
        return
    _doi(0, *c.init(sd := c.sd())[0:1], b"", "init")
    ps = dau.replace("<issue>", "55").replace("<executor-provider>", EXECUTOR)
    ps = ps.replace("packet_loop.py ", f"packet_loop.py --state-dir {sd} ")
    r = subprocess.run(["pwsh", "-NoProfile", "-Command", ps], cwd=str(ROOT), capture_output=True)
    assert r.returncode == 0, f"khoi canonical KHONG chay duoc: {r.stderr!r}"
def case_void_giu_dung_hanh_vi_master(c: Ctx):
    """N11 — canh việc BỎ M3/M4 đã SẠCH, không sót mảnh nào.

    Hai chiều: (a) HÀNH VI — mọi lý do trong allowlist hoàn được lượt, KHÔNG cờ bằng
    chứng nào; (b) BỀ MẶT — bốn cờ M3/M4 phải biến khỏi parser. Thiếu (b) thì mảnh sót
    vẫn qua (a) khi cờ có mặc định vô hại; thiếu (a) thì gỡ cờ mà để lại `_die` vẫn xanh.
    """
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    for ly_do in ("quota", "rate_limit", "infrastructure", "permission"):
        rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
        _doi(0, rc, e, "begin-attempt")
        rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", ly_do], sd)
        _doi(0, rc, e, f"{ly_do} bị đòi bằng chứng — void-attempt phải giữ đúng hành vi master")
    rc, o, e = run(c.script, ["void-attempt", "--help"], sd)
    _doi(0, rc, e, "void-attempt --help")
    sot = [f for f in ("--bang-chung", "--khong-co-bang-chung", "--ai-cho-phep", "--can-cu")
           if f.encode() in o]
    assert not sot, f"cờ M3/M4 còn sót trong parser: {sot}"


def case_void_attempt_allowlist(c: Ctx):
    sd = c.sd()
    _doi(0, *c.init(sd)[0:1], b"", "init")
    rc, _, e = run(c.script, ["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd)
    _doi(0, rc, e, "begin-attempt")
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota"], sd)
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
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota"], sd)
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
    spec.loader.exec_module(m)
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
        (["next-comment", "--packet", 55], sd),
        (["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000009"], sd),
        (["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000009",
          "--head-sha", "%040x" % 1], sd),
        # `void-attempt` in tiếng Việt lúc THÀNH CÔNG — lệnh generation 4 bỏ sót.
        # Đặt TRƯỚC `record-review`: một lượt đã có review thì không hoàn được nữa
        # (chốt `void_sau_review_bi_chan`), nên đặt sau sẽ đo nhầm đường thất bại.
        (["void-attempt", "--packet", 55, "--reason", "quota"], sd),
        # Mở lại lượt: đồng thời là phép đo chiều bắt-oan của
        # `void-reviewing-accepts-attempt-zero` — void xong phải chạy tiếp được.
        (["begin-attempt", "--packet", 55, "--provider", EXECUTOR], sd),
        (["record-post", "--packet", 55, "--for", "reviewing", "--comment-id", "7770000019"], sd),
        (["transition", "--packet", 55, "--to", "reviewing", "--comment-id", "7770000019",
          "--head-sha", "%040x" % 2], sd),
        (["record-review", "--packet", 55, "--provider", REVIEWER, "--verdict", "changes_requested",
          "--reviewed-sha", "%040x" % 2,
          "--finding-id", "loi-co-dau-tieng-viet", "--finding-desc", "mô tả có dấu tiếng Việt"], sd),
        (["status", "--packet", 55], sd),
        (["doctrine-scan", "--root", r], None),
        (["adr-song", "--root", r_adr], None),
    ]
    da_phu = set()
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
    rc, _, e = run(c.script, ["void-attempt", "--packet", 55, "--reason", "quota"], sd)
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


CASES = [
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
    ("mt_thieu_cong_cu_thi_khong_mo_duoc_luot", case_mt_thieu_cong_cu_thi_khong_mo_duoc_luot),
    ("mt_sach_thi_van_mo_duoc_luot", case_mt_sach_thi_van_mo_duoc_luot),
    ("mt_chup_tren_nen_khac_thi_tu_choi", case_mt_chup_tren_nen_khac_thi_tu_choi),
    ("mt_anh_hong_la_KHONG_DOC_DUOC", case_mt_anh_hong_la_KHONG_DOC_DUOC_khong_phai_thieu),
    ("luong_canonical_chay_that", case_luong_canonical_chay_that),
    ("void_giu_dung_hanh_vi_master", case_void_giu_dung_hanh_vi_master),
    ("void_attempt_allowlist", case_void_attempt_allowlist),
    ("void_xong_van_mo_lai_duoc_luot", case_void_xong_van_mo_lai_duoc_luot),
    ("void_attempt_ly_do_tu_che_bi_tu_choi", case_void_attempt_ly_do_tu_che_bi_tu_choi),
    ("void_sau_review_bi_chan", case_void_sau_review_bi_chan),
    ("doctrine_scan_sach_xanh", case_doctrine_scan_sach_xanh),
    ("doctrine_scan_bom_cum_tu_do", case_doctrine_scan_bom_cum_tu_do),
    ("doctrine_scan_bat_doctrine_THAT_tu_protocol", case_doctrine_scan_bat_doctrine_THAT_tu_protocol),
    ("doctrine_scan_repo_that_sach", case_doctrine_scan_repo_that_sach),
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
    # --- M1/M2 · N11: mỗi luật MỘT đột biến -------------------------------------
    # N2 là ca chiều BẮT OAN nên chỉ chết bởi đột biến SIẾT (ngưỡng tuổi về -1) — và
    # đột biến ấy KHÔNG làm N1 đỏ, vì N1 vốn đòi rc=10. Hai chiều, hai loại đột biến.
    "mt_bo_chot_thieu_cong_cu": (
        '    thieu = d.get("thieu_bat_buoc") or []\n',
        '    thieu = []   # đột biến: bỏ chốt thiếu công cụ\n',
        ["mt_thieu_cong_cu_thi_khong_mo_duoc_luot"],
    ),
    "mt_siet_nguong_tuoi_ve_am_mot": (
        "NGUONG_TUOI_BANG_CHUNG_GIAY = 3600\n",
        "NGUONG_TUOI_BANG_CHUNG_GIAY = -1   # đột biến: siết, ảnh nào cũng 'cũ'\n",
        ["mt_sach_thi_van_mo_duoc_luot"],
    ),
    "mt_bo_so_nen_chup_anh": (
        '    if d.get("he_dieu_hanh") != nen_thuc:\n',
        '    if False:   # đột biến: bỏ so nền\n',
        ["mt_chup_tren_nen_khac_thi_tu_choi"],
    ),
    "mt_gop_khong_doc_duoc_vao_thieu": (
        '        return BC_KHONG_DOC_DUOC, None, f"ảnh môi trường không đọc được ({ex.__class__.__name__}): {duong}"\n',
        '        return BC_KHONG, None, f"hỏng: {ex}"   # đột biến: gộp trạng thái thứ ba\n',
        ["mt_anh_hong_la_KHONG_DOC_DUOC"],
    ),
    "mt_them_lai_doi_bang_chung_o_void": (
        "    if a.reason not in LY_DO_VOID:\n",
        '    if a.reason in ("infrastructure", "permission"):\n'
        '        _die(RC_MOI_TRUONG, "đột biến: đòi lại bằng chứng")\n'
        "    if a.reason not in LY_DO_VOID:\n",
        ["void_giu_dung_hanh_vi_master"],
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
    "adr_tha_khi_thieu_thu_muc": (
        '        if (root / ".git").exists():\n',
        "        if False:                     # đột biến: kho thật cũng bỏ qua êm\n",
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
}


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
            thieu = [t for t, _ in cap if t not in goc]
            if thieu:
                print(f"  ĐỎ  đột biến {ten_mut}: không tìm thấy mỏ neo {thieu!r}")
                that_bai_tong += len(thieu)
                continue
            mut_dir = tmp / f"mut_{ten_mut}"
            mut_dir.mkdir(parents=True, exist_ok=True)
            mut = mut_dir / "packet_loop.py"
            than = goc
            for t, th in cap:
                than = than.replace(t, th, 1)
            mut.write_text(than, encoding="utf-8", newline="\n")
            doi_chung = _doi_chung_khac_ho(phai_chet)
            ket_mut = chay_suite(mut, mut_dir, chi_chay=set(phai_chet) | set(doi_chung))
            song = [t for t in phai_chet if ket_mut.get(t) is None]
            oan = [t for t in doi_chung if ket_mut.get(t) is not None]
            if song:
                print(f"  ĐỎ  đột biến {ten_mut}: ca {song} VẪN XANH ⇒ ca đó không đo gì")
                that_bai_tong += len(song)
            if oan:
                print(f"  ĐỎ  đột biến {ten_mut}: giết cả ĐỐI CHỨNG KHÁC HỌ {oan} ⇒ "
                      f"đột biến không nhắm đúng tầng nó khai")
                that_bai_tong += len(oan)
            if not song and not oan:
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
