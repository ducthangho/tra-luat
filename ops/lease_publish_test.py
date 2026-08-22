#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Phản chứng cho `lease_publish.py` — cổng chặn TRƯỚC khi một lease được đăng.

Vì sao cần cổng này: workflow chạy bằng `GITHUB_TOKEN`, nghĩa là **push được thành
đăng được**. Thứ duy nhất đứng giữa một tệp YAML trong kho và một comment mang danh
nghĩa kho là bộ kiểm này. Nó mà xanh dễ dãi thì đường git-thay-API trở thành đường
đăng bừa.

Cùng doctrine với `packet_loop_test.py`: gọi CHÍNH lệnh qua subprocess, không import.
Thứ workflow gõ là lệnh, nên thứ được đo phải là lệnh.

Chạy: python3 ops/lease_publish_test.py
"""

from __future__ import annotations

import re
import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "lease_publish.py"
WORKFLOW_DANG = HERE.parent / ".github" / "workflows" / "ops-publish-lease.yml"

RC_OK, RC_THAM_SO, RC_TU_CAP, RC_DA_DANG, RC_NOI_DUNG, RC_NEO = 0, 2, 4, 9, 8, 6

CA: list = []


class BoQuaNen(Exception):
    def __init__(self, tep=None, ten_job=None):
        self.tep, self.ten_job = tep, ten_job

def ca(fn):
    CA.append(fn)
    return fn


def chay(*doi_so, env=None, cwd=None):
    p = subprocess.run([sys.executable, str(SCRIPT), *[str(x) for x in doi_so]],
                       capture_output=True, text=True, env=env, cwd=cwd)
    return p.returncode, p.stdout, p.stderr


def _doc_do_gia(tep: Path, rc: int, stdout: str, stderr: str, mo_ta: str) -> str:
    if not tep.is_file():
        raise AssertionError(f"KHÔNG ĐO ĐƯỢC {mo_ta}: đồ giả không sinh tệp {tep}; "
                             f"rc={rc}, stdout={stdout!r}, stderr={stderr!r}")
    return tep.read_text(encoding="utf-8")

def mai_sau(gio=4) -> str:
    return (datetime.now(timezone.utc) + timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


def khi_truoc(gio=4) -> str:
    return (datetime.now(timezone.utc) - timedelta(hours=gio)).strftime("%Y-%m-%dT%H:%M:%SZ")


SHA40 = "cf39109c9e5167516c53f2071e5fa7ec5c6afff5"


def lease_mau(**doi) -> dict:
    d = {
        "schema_version": 1,
        "event": "review_lease_granted",
        "packet_issue": 55,
        "packet_id": "wp55",
        "lease_id": "wp55-r2-review-3-codex-20260814",
        "role": "reviewer",
        "provider": "codex",
        "target_pull_request": 92,
        "reviewed_sha_required": SHA40,
        "granted_by": "ducthangho",
        "lease_expires_at_utc": mai_sau(),
        "attempts_used": 2,
        "attempts_limit": 3,
    }
    d.update(doi)
    return d


def viet(tmp: Path, lease: dict, ten="l.yaml") -> Path:
    import yaml
    p = tmp / ten
    p.write_text(yaml.safe_dump(lease, allow_unicode=True, sort_keys=False), encoding="utf-8")
    return p


class San:
    def __enter__(self):
        self.d = Path(tempfile.mkdtemp(prefix="lp_"))
        return self.d

    def __exit__(self, *a):
        import shutil
        shutil.rmtree(self.d, ignore_errors=True)


def bang(dk, msg):
    if not dk:
        raise AssertionError(msg)


def dat_prompt(goc: Path, noi_dung: bytes, duong="ops/prompts/p.md") -> tuple[str, str]:
    """Đặt một tệp prompt trong "kho" giả, trả về (đường dẫn tương đối, sha256)."""
    import hashlib
    f = goc / duong
    f.parent.mkdir(parents=True, exist_ok=True)
    f.write_bytes(noi_dung)
    return duong, hashlib.sha256(noi_dung).hexdigest()


def _nap_cong():
    import importlib.util
    spec = importlib.util.spec_from_file_location("lease_publish_thu", SCRIPT)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


class GhGia:
    """GitHub giả giữ DANH SÁCH comment theo issue, không trả lời theo lượt."""
    def __init__(self, loai=None, comments=None, loi_comment=()):
        self.loai = loai or {}
        self.comments = {int(k): list(v) for k, v in (comments or {}).items()}
        self.loi_comment = set(loi_comment)
        self.calls = []

    def __call__(self, *args):
        import json
        self.calls.append(args)
        endpoint = next((x for x in args if str(x).startswith("repos/")), "")
        so = int(endpoint.split("/issues/", 1)[1].split("/", 1)[0])
        if endpoint.endswith("/comments"):
            if so in self.loi_comment:
                return subprocess.CompletedProcess(args, 1, "", "comments hong")
            return subprocess.CompletedProcess(
                args, 0, json.dumps([self.comments.get(so, [])]), "")
        loai = self.loai.get(so, "issue")
        if loai == "loi":
            return subprocess.CompletedProcess(args, 1, "", "issue hong")
        doan = "pull" if loai == "pr" else "issues"
        return subprocess.CompletedProcess(
            args, 0, json.dumps({"html_url": f"https://github.com/o/r/{doan}/{so}"}), "")

    def dang(self, so: int, body: str):
        ds = self.comments.setdefault(so, [])
        comment = {"id": 9000 + len(ds), "body": body,
                   "user": {"login": "github-actions[bot]"}}
        ds.append(comment)
        self.calls.append(("POST", so, comment["id"]))
        return comment["id"]


ENV_GITHUB = {"GITHUB_REPOSITORY": "o/r"}


def _goi_lop_gh(gh: GhGia, ten: str, *args, env_them=None, bo_qua=()):
    import os
    from unittest import mock
    mod = _nap_cong()
    mod.GOI_GH = gh
    for ten_bo_qua in bo_qua:
        setattr(mod, ten_bo_qua, lambda *a: None)
    moi = dict(os.environ)
    moi.update(env_them or {})
    try:
        with mock.patch.dict(os.environ, moi, clear=True):
            getattr(mod, ten)(*args)
    except mod.Chan as ex:
        return ex, mod
    return None, mod


def _buoc_workflow(ten: str) -> dict:
    import yaml
    tep = WORKFLOW_DANG
    bang(tep.is_file(), f"không thấy {tep}")
    d = yaml.safe_load(tep.read_text(encoding="utf-8"))
    ds = [x for x in d["jobs"]["dang"]["steps"] if x.get("name") == ten]
    bang(len(ds) == 1, f"chờ ĐÚNG một bước {ten!r}, thấy {len(ds)}")
    return ds[0]


def _ly_do_bo_qua_workflow(tep: Path, ten_job: str, nen=None, job=None) -> str:
    import os, yaml
    job = job or yaml.safe_load(tep.read_text(encoding="utf-8"))["jobs"][ten_job]
    raw, nhan = job.get("runs-on"), []
    m = re.fullmatch(r"\$\{\{\s*matrix\.([A-Za-z_][\w-]*)\s*\}\}", raw) if isinstance(raw, str) else None
    nhan = (((job.get("strategy") or {}).get("matrix") or {}).get(m.group(1))
            if m else raw if isinstance(raw, list) else [raw])
    if (nen or os.name) == "nt" and nhan and all(
            isinstance(x, str) and x.lower().startswith("ubuntu-") for x in nhan):
        return (f"{tep.name}:{ten_job} chỉ chạy Ubuntu; runs-on đã đọc được: "
                f"{raw!r}, phân giải thành {nhan!r}")
    return ""


# --- các ca ---------------------------------------------------------------------


@ca
def t01_lease_hop_le_thi_QUA():
    """Cổng phải xanh được, không thì người ta gỡ nó ra."""
    with San() as s:
        rc, o, e = chay("check", viet(s, lease_mau()))
        bang(rc == RC_OK, f"chặn oan lease hợp lệ: rc={rc} {e}")


@ca
def t02_granted_by_la_ten_provider_bi_CHAN():
    """Chốt CỐT LÕI, cùng luật với `packet_loop.py record-lease`.

    Nếu chỗ này lỏng, một agent tự soạn lease cho mình rồi push là có comment
    mang danh nghĩa kho — đúng thứ doctrine 'không tự cấp lease' cấm.
    """
    with San() as s:
        for ten in ("codex", "claude", "Claude", "  CODEX  "):
            rc, _, e = chay("check", viet(s, lease_mau(granted_by=ten), ten="x.yaml"))
            bang(rc == RC_TU_CAP, f"granted_by={ten!r} lọt: rc={rc} {e}")


@ca
def t02b_ten_KHONG_CO_THAM_QUYEN_bi_CHAN():
    """`lease-authority-spoof` — P1 của cross-review lượt 4 (codex, 14-08-2026).

    Bản trước chỉ từ chối ĐÚNG hai chuỗi `claude`/`codex`, nên mọi biến thể lọt sạch.
    Nguyên văn kết luận của reviewer: *"distinguishes spelling, not authority"*.
    Bốn chuỗi dưới đây là ca reviewer đã chạy được và thu `rc=0` trên bản cũ.

    Đắng: prompt do chính phiên soạn cho reviewer LIỆT KÊ `codex-dispatcher` làm hướng
    tấn công số 1, rồi cổng vẫn thua đúng ca đó. Nghĩ ra phép thử mà không chạy thì
    phép thử ấy không tồn tại — ca này tồn tại để lần sau không cần nghĩ lại.
    """
    with San() as s:
        for ten in ("codex-dispatcher", "ai-codex-bot", "cödex", "claude-code",
                    "dispatcher", "ducthangho2"):
            rc, _, e = chay("check", viet(s, lease_mau(granted_by=ten), ten="a.yaml"))
            bang(rc == RC_TU_CAP, f"granted_by={ten!r} LỌT: rc={rc} {e}")
            bang("danh sách người có thẩm quyền" in e,
                 f"{ten!r} bị chặn nhưng KHÔNG phải bởi danh sách cho phép: {e.strip()!r}")


@ca
def t02c_nguoi_CO_tham_quyen_thi_QUA_moi_cach_viet():
    """Chiều DƯƠNG. Một danh sách cho phép chặn được tất cả thì cũng vô dụng."""
    with San() as s:
        for ten in ("ducthangho", "Ducthangho", "  DUCTHANGHO  "):
            rc, _, e = chay("check", viet(s, lease_mau(granted_by=ten), ten="b.yaml"))
            bang(rc == RC_OK, f"chặn oan người có thẩm quyền {ten!r}: rc={rc} {e}")


@ca
def t02d_GITHUB_ACTOR_khong_co_tham_quyen_bi_CHAN():
    """Neo vào danh tính GitHub XÁC THỰC, không phải chữ trong tệp YAML.

    Kẻ soạn lease đặt được `granted_by`, nhưng KHÔNG đặt được `GITHUB_ACTOR` — biến
    đó do GitHub đặt cho runner. Lệch nhau thì tin cái GitHub xác thực.
    """
    import os
    with San() as s:
        p = viet(s, lease_mau())          # granted_by hợp lệ
        moi = dict(os.environ, GITHUB_ACTOR="ke-la-mat")
        q = subprocess.run([sys.executable, str(SCRIPT), "check", str(p)],
                           capture_output=True, text=True, env=moi)
        bang(q.returncode == RC_TU_CAP,
             f"GITHUB_ACTOR lạ mà vẫn đăng được: rc={q.returncode} {q.stderr}")
        bang("GITHUB_ACTOR" in q.stderr, f"chặn nhưng nói sai lỗi: {q.stderr.strip()!r}")
        # chiều dương: actor có thẩm quyền thì qua
        moi["GITHUB_ACTOR"] = "ducthangho"
        q2 = subprocess.run([sys.executable, str(SCRIPT), "check", str(p)],
                            capture_output=True, text=True, env=moi)
        bang(q2.returncode == RC_OK, f"chặn oan actor hợp lệ: rc={q2.returncode} {q2.stderr}")


@ca
def t03_lease_da_het_han_bi_CHAN():
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(lease_expires_at_utc=khi_truoc())))
        bang(rc == RC_NOI_DUNG, f"đăng được lease đã chết: rc={rc} {e}")


@ca
def t04_han_thieu_mui_gio_bi_CHAN():
    """"18:30" không nói múi là hai mốc cách nhau tới 26 giờ — chặn, đừng đoán."""
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(lease_expires_at_utc="2026-12-01T18:30:00")))
        bang(rc == RC_NOI_DUNG, f"nhận hạn không múi giờ: rc={rc} {e}")


@ca
def t05_thieu_truong_bat_buoc_bi_CHAN():
    with San() as s:
        for thieu in ("packet_issue", "lease_id", "granted_by",
                      "lease_expires_at_utc", "reviewed_sha_required"):
            d = lease_mau()
            d.pop(thieu)
            rc, _, e = chay("check", viet(s, d, ten=f"{thieu}.yaml"))
            bang(rc == RC_NOI_DUNG, f"thiếu {thieu!r} mà vẫn qua: rc={rc} {e}")


@ca
def t06_sha_khong_dung_dang_bi_CHAN():
    """SHA ngắn/lệch dạng là mỏ neo giả — reviewer sẽ đọc nhầm head."""
    with San() as s:
        for xau in ("cf39109c", "z" * 40, SHA40 + "0", ""):
            rc, _, e = chay("check", viet(s, lease_mau(reviewed_sha_required=xau), ten="s.yaml"))
            bang(rc == RC_NOI_DUNG, f"sha {xau!r} lọt: rc={rc} {e}")


@ca
def t07_packet_issue_khong_phai_so_bi_CHAN():
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(packet_issue="55; rm -rf /")))
        bang(rc == RC_NOI_DUNG, f"packet_issue rác lọt: rc={rc} {e}")


@ca
def t08_da_dang_roi_thi_BAO_BO_QUA_khong_dang_lai():
    """Idempotent: workflow chạy lại (retry, re-run) KHÔNG được đăng trùng."""
    with San() as s:
        rc, _, e = chay("check", viet(s, lease_mau(posted_comment_id=5288831421)))
        bang(rc == RC_DA_DANG, f"sẽ đăng trùng: rc={rc} {e}")


@ca
def t09_body_in_ra_nguyen_van_YAML_de_doi_chieu():
    """Thân comment phải chứa lại chính khối YAML — người đọc đối chiếu được."""
    with San() as s:
        rc, o, e = chay("body", viet(s, lease_mau()))
        bang(rc == RC_OK, f"dựng thân hỏng: rc={rc} {e}")
        for phai_co in ("wp55-r2-review-3-codex-20260814", SHA40, "```"):
            bang(phai_co in o, f"thân comment thiếu {phai_co!r}")


@ca
def t10_body_TU_CHOI_lease_khong_hop_le():
    """`body` không được dựng thân cho một lease mà `check` đã chặn.

    Hai lệnh hai đường mà chỉ một đường có chốt là chốt đi vòng được.
    """
    with San() as s:
        rc, _, e = chay("body", viet(s, lease_mau(granted_by="codex")))
        bang(rc == RC_TU_CAP, f"`body` bỏ qua chốt: rc={rc} {e}")


@ca
def t11_mark_ghi_comment_id_vao_tep():
    with San() as s:
        p = viet(s, lease_mau())
        rc, _, e = chay("mark", p, "--comment-id", "5288831421")
        bang(rc == RC_OK, f"mark hỏng: rc={rc} {e}")
        rc2, _, _ = chay("check", p)
        bang(rc2 == RC_DA_DANG, f"mark xong mà check vẫn đòi đăng: rc={rc2}")


@ca
def t12_tep_khong_ton_tai_bao_ro():
    rc, _, e = chay("check", "/khong/co/tep/nay.yaml")
    bang(rc == RC_THAM_SO, f"tệp thiếu phải là {RC_THAM_SO}: rc={rc}")


@ca
def t13_yaml_hong_khong_duoc_no_traceback():
    with San() as s:
        p = s / "hong.yaml"
        p.write_text("a: [1, 2\n  b: :::\n", encoding="utf-8")
        rc, _, e = chay("check", p)
        bang(rc == RC_NOI_DUNG, f"YAML hỏng phải là {RC_NOI_DUNG}: rc={rc}")
        bang("Traceback" not in e, "lộ traceback thô ra ngoài")


@ca
def t14_neo_prompt_DUNG_thi_QUA():
    """Chiều DƯƠNG. Chốt chỉ biết chặn mà không biết cho qua thì cũng hỏng."""
    with San() as s:
        duong, sha = dat_prompt(s, b"Ban la phien REVIEWER...\n")
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sha))
        rc, o, e = chay("check", p, "--root", s)
        bang(rc == RC_OK, f"chặn oan lease neo prompt đúng: rc={rc} {e}")
        # Đòi in ra ĐÚNG cái băm vừa xác minh, không chỉ chữ "khớp băm": một dòng
        # xác nhận in được cả khi chốt đã bị gỡ thì nó là trang trí, không phải
        # bằng chứng. Có ca này thì gỡ chốt ⇒ ca này đỏ.
        bang("khớp băm" in o and sha[:12] in o,
             f"không nêu băm đã xác minh (chờ {sha[:12]}): {o!r}")


@ca
def t15_bam_LECH_thi_CHAN():
    """ĐÂY LÀ BUG GỐC, dựng lại nguyên trạng.

    Lease #3 của wp55 khai `46a833cc…` trong khi không văn bản nào băm ra thế.
    Trước bản vá này cổng vẫn xanh, và hỏng im lặng suốt hai ngày.
    """
    with San() as s:
        duong, _ = dat_prompt(s, b"noi dung that\n")
        sai = "46a833ccfefba0b659a16183daf8b4f4893a5ef0eeb4e7fdf3cd315aad550dfc"
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sai))
        rc, _, e = chay("check", p, "--root", s)
        bang(rc == RC_NEO, f"băm lệch mà vẫn đăng được: rc={rc} {e}")
        # Đòi thông điệp nói CẢ HAI con số. Một cổng chỉ hô "lệch" thì người sửa
        # vẫn phải tự đi băm lại — đúng chỗ hai ngày vừa rồi mất thời gian.
        bang(sai in e and "thực tế" in e, f"thông điệp không nêu đủ hai băm: {e!r}")


@ca
def t16_tep_prompt_KHONG_CO_thi_CHAN():
    with San() as s:
        p = viet(s, lease_mau(prompt_path="ops/prompts/khong-co.md",
                              prompt_sha256_required="0" * 64))
        rc, _, e = chay("check", p, "--root", s)
        bang(rc == RC_NEO, f"neo vào tệp không tồn tại mà qua: rc={rc} {e}")


@ca
def t17_neo_NUA_VOI_thi_CHAN_CA_HAI_CHIEU():
    """Băm không địa chỉ = không kiểm được. Địa chỉ không băm = đổi lúc nào không hay.

    Neo THÔNG ĐIỆP, và lý do đáng ghi: bỏ chốt này đi thì `prompt_path` rỗng biến
    thành `PurePosixPath("")` = `.`, tức trỏ vào chính thư mục gốc kho, và bị chặn
    ở `is_file()` với câu "không có tệp". Vẫn RC_NEO, nên ca chỉ đòi mã thoát sẽ
    XANH trong khi chốt đã bị gỡ — mà thông điệp thì chỉ sai chỗ đúng kiểu đã làm
    mất hai ngày: nói tệp thiếu, trong khi lỗi thật là lease không khai địa chỉ.
    """
    with San() as s:
        duong, sha = dat_prompt(s, b"x\n")
        rc, _, e = chay("check", viet(s, lease_mau(prompt_sha256_required=sha), ten="a.yaml"),
                        "--root", s)
        bang(rc == RC_NEO, f"băm không có prompt_path mà qua: rc={rc} {e}")
        bang("thiếu `prompt_path`" in e,
             f"chặn nhưng nói sai lỗi (chờ 'thiếu prompt_path'): {e.strip()!r}")
        rc, _, e = chay("check", viet(s, lease_mau(prompt_path=duong), ten="b.yaml"),
                        "--root", s)
        bang(rc == RC_NEO, f"prompt_path không có băm mà qua: rc={rc} {e}")
        bang("thiếu `prompt_sha256_required`" in e,
             f"chặn nhưng nói sai lỗi (chờ 'thiếu prompt_sha256_required'): {e.strip()!r}")


@ca
def t18_prompt_path_VUOT_RA_NGOAI_kho_thi_CHAN():
    """`prompt_path` là dữ liệu YAML mà thành một lượt đọc đĩa — phải chặn đường ra.

    Ca này neo THÔNG ĐIỆP chứ không chỉ mã thoát, và đó là chủ đích. Có HAI lớp
    chặn (lọc dạng đường dẫn trước khi đụng đĩa, rồi `relative_to` sau `resolve`),
    và đã đo: bỏ lớp nào thì lớp kia vẫn trả đúng RC_NEO. Nếu chỉ đòi mã thoát thì
    đột biến gỡ lớp trên SỐNG SÓT, và bộ test nói dối rằng nó có đo lớp ấy. Neo
    thông điệp thì mỗi lớp có một ca riêng: t18 giữ lớp lọc, t19 giữ `relative_to`.
    """
    with San() as s:
        ngoai = s.parent / f"ngoai_{s.name}.md"
        ngoai.write_bytes(b"tep ngoai kho\n")
        import hashlib
        sha = hashlib.sha256(b"tep ngoai kho\n").hexdigest()
        try:
            for xau in (f"../{ngoai.name}", str(ngoai), "..\\..\\x.md",
                        "ops/../../" + ngoai.name):
                p = viet(s, lease_mau(prompt_path=xau, prompt_sha256_required=sha),
                         ten="v.yaml")
                rc, _, e = chay("check", p, "--root", s)
                bang(rc == RC_NEO, f"prompt_path {xau!r} thoát ra ngoài kho: rc={rc} {e}")
                bang("đường dẫn tương đối" in e,
                     f"{xau!r} bị chặn nhưng KHÔNG phải bởi lớp lọc dạng đường dẫn "
                     f"(thông điệp: {e.strip()!r})")
        finally:
            ngoai.unlink(missing_ok=True)


@ca
def t19_symlink_tro_RA_NGOAI_kho_thi_CHAN():
    """`..` chỉ là một trong hai đường ra. Symlink là đường kia, và nó im hơn."""
    with San() as s:
        ngoai = s.parent / f"sym_{s.name}.md"
        ngoai.write_bytes(b"tep ngoai kho\n")
        import hashlib
        sha = hashlib.sha256(b"tep ngoai kho\n").hexdigest()
        lk = s / "ops" / "prompts" / "p.md"
        lk.parent.mkdir(parents=True, exist_ok=True)
        try:
            lk.symlink_to(ngoai)
        except (OSError, NotImplementedError):
            return   # nền không cho tạo symlink (Windows thiếu quyền) — bỏ qua
        try:
            p = viet(s, lease_mau(prompt_path="ops/prompts/p.md",
                                  prompt_sha256_required=sha))
            rc, _, e = chay("check", p, "--root", s)
            bang(rc == RC_NEO, f"symlink ra ngoài kho vẫn qua: rc={rc} {e}")
            # Symlink là ca DUY NHẤT mà lớp lọc dạng đường dẫn không thấy được:
            # `ops/prompts/p.md` sạch về mặt chuỗi, chỉ `resolve()` mới lộ.
            bang("ngoài kho" in e,
                 f"chặn nhưng không phải bởi `relative_to` sau resolve: {e.strip()!r}")
        finally:
            ngoai.unlink(missing_ok=True)


@ca
def t20_sha256_SAI_DANG_thi_CHAN():
    with San() as s:
        duong, sha = dat_prompt(s, b"x\n")
        for xau in (sha[:32], sha.upper(), sha + "0", "z" * 64):
            p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=xau),
                     ten="d.yaml")
            rc, _, e = chay("check", p, "--root", s)
            bang(rc == RC_NEO, f"sha256 {xau!r} lọt: rc={rc} {e}")
            # Neo THÔNG ĐIỆP: băm sai dạng thì cũng khác băm thật, nên chốt so băm
            # bên dưới vẫn chặn — chỉ đòi mã thoát là ca này không đo gì cả (đã đo:
            # gỡ chốt dạng đi thì suite vẫn xanh). Nói "sai dạng" khác hẳn nói
            # "băm lệch": cái sau đẩy người sửa đi băm lại một tệp không có lỗi.
            bang("64 ký tự hex" in e,
                 f"sha256 {xau!r} bị chặn nhầm chỗ — chờ lỗi SAI DẠNG, được: {e.strip()!r}")


@ca
def t21_bam_theo_BYTE_chu_khong_theo_van_ban():
    """CRLF và LF là hai tệp khác nhau, và phải ra hai băm khác nhau.

    `read_text` chuẩn hoá xuống dòng nên cùng một tệp cho hai kết quả tuỳ nền —
    một cổng như thế xanh ở Linux, đỏ ở Windows, không ai hiểu vì sao.
    """
    with San() as s:
        import hashlib
        lf = b"dong mot\ndong hai\n"
        duong, sha_lf = dat_prompt(s, lf)
        (s / duong).write_bytes(lf.replace(b"\n", b"\r\n"))   # cùng đường dẫn, đổi EOL
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sha_lf))
        rc, _, e = chay("check", p, "--root", s)
        bang(rc == RC_NEO, f"CRLF/LF ra cùng băm — đang đọc văn bản, không đọc byte: rc={rc}")
        # chiều dương: khai đúng băm bản CRLF thì phải qua
        sha_crlf = hashlib.sha256(lf.replace(b"\n", b"\r\n")).hexdigest()
        p2 = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required=sha_crlf),
                  ten="crlf.yaml")
        rc2, _, e2 = chay("check", p2, "--root", s)
        bang(rc2 == RC_OK, f"chặn oan bản CRLF khai đúng băm: rc={rc2} {e2}")


@ca
def t22_body_cung_bi_CHAN_khi_neo_hong():
    """Hai lệnh hai đường mà chỉ một đường có chốt là chốt đi vòng được."""
    with San() as s:
        duong, _ = dat_prompt(s, b"that\n")
        p = viet(s, lease_mau(prompt_path=duong, prompt_sha256_required="0" * 64))
        rc, o, e = chay("body", p, "--root", s)
        bang(rc == RC_NEO, f"`body` bỏ qua chốt neo prompt: rc={rc} {e}")
        bang(not o.strip(), f"`body` vẫn in thân comment cho lease hỏng: {o[:120]!r}")


@ca
def t23_MOI_lease_THAT_trong_kho_phai_QUA():
    """Chốt phải xanh trên chính các tệp lease đang dùng, không chỉ trên đồ giả.

    Quét MỌI lease trong `ops/leases/`, không chỉ định danh một tệp. Bản đầu ca này
    ghi cứng tên lease #3; đến lease #4 thì nó vẫn xanh trong khi lease mới có thể
    hỏng — thêm lease là thêm chỗ mù, mà chỗ mù nằm đúng ở tệp mới nhất, tức tệp
    khả nghi nhất. Ca ghi cứng một tên chỉ canh được quá khứ.

    Bỏ ca này thì bộ test có thể xanh trong khi lease thật vẫn hỏng — đúng khoảng
    cách giữa "code chạy" và "việc chạy".
    """
    import hashlib
    import yaml
    goc = HERE.parent
    thu_muc = HERE / "leases"
    if not thu_muc.is_dir():
        return
    ds = sorted(p for p in thu_muc.iterdir() if p.suffix in (".yaml", ".yml"))
    # KHÔNG cho phép "không có lease nào" âm thầm thành ĐẠT: thư mục rỗng và thư mục
    # toàn lease lành cho cùng một màu xanh, mà ý nghĩa thì ngược nhau.
    bang(ds, f"không thấy lease nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")
    da_kiem = 0
    for p in ds:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        duong, sha = d.get("prompt_path"), d.get("prompt_sha256_required")
        if not duong and not sha:
            continue          # lease không neo prompt — hợp lệ, bỏ qua
        bang(duong and sha, f"{p.name}: neo prompt NỬA VỜI (path={duong!r} sha={sha!r})")
        f = goc / duong
        bang(f.is_file(), f"{p.name}: trỏ vào tệp không có: {duong}")
        thuc = hashlib.sha256(f.read_bytes()).hexdigest()
        bang(thuc == sha, f"{p.name}: LỆCH BĂM — khai {sha}, tệp {duong!r} thực {thuc}")
        da_kiem += 1
    bang(da_kiem, "không lease nào neo prompt — ca này không đo được gì")


@ca
def t24_workflow_KHONG_duoc_nhet_dau_skip_ci_vao_commit():
    """Không workflow nào được ghi dấu skip-ci vào thông điệp commit.

    Đã trả giá hai lần trong CÙNG một ngày (14-08-2026), theo hai đường khác nhau:

    1. Bước ghi ngược của `ops-publish-lease.yml` commit kèm `[skip ci]` để khỏi tự
       kích hoạt lại. Dấu ấy sống trong LỊCH SỬ, nên khi commit ghi ngược thành HEAD
       của một PR thì nó tắt gate của PR đó: PR #100 có **0 check run** mà vẫn hiện
       `mergeable_state: clean`. Cổng không nói dối — nó vắng mặt, và trên giao diện
       hai thứ đó nhìn giống hệt nhau.
    2. Một merge commit TRÍCH DẪN `[skip ci]` để giải thích lỗi số 1 đã tắt gate của
       chính master. GitHub khớp CHUỖI trên toàn thông điệp, không đọc Markdown, nên
       dấu nháy ngược không phải hàng rào — cùng bài học với `doctrine-scan`.

    Ca này canh đường (1): quét mọi workflow, cấm dấu skip-ci đi kèm `git commit`.
    Đường (2) là kỷ luật viết commit, máy không canh được ở đây — ghi trong CLAUDE.md.
    """
    # HERE là `ops/`, nên gốc kho là HERE.parent. Bản đầu viết `HERE.parent.parent`
    # ⇒ trỏ RA NGOÀI gốc kho, thư mục không có, hàm `return` sớm và ca XANH RỖNG —
    # đúng bệnh mà chính nó sinh ra để chặn. Chỉ lộ vì đã đột biến thử; suite vẫn báo
    # 24/24 trong khi ca này không đo gì. "Ca có mặt" khác "ca có đo".
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Chỉ tha khi đây rõ ràng là BẢN SAO rời (bộ đột biến chép mỗi `ops/`).
        # Trong kho thật mà thiếu thư mục workflow thì phải ĐỎ, không được lặng lẽ qua.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh rỗng")
        return
    ds = sorted(p for p in goc.iterdir() if p.suffix in (".yml", ".yaml"))
    bang(ds, f"không thấy workflow nào trong {goc} — ca này sẽ xanh mà không đo gì")
    # Chỉ những dạng GitHub THẬT SỰ hiểu. Đừng nới thêm biến thể tưởng tượng: bảng
    # rộng quá thì ca này bắt oan một chú thích bình thường rồi bị gỡ.
    DAU = ("[skip ci]", "[ci skip]", "[no ci]", "[skip actions]", "[actions skip]")
    for p in ds:
        noi_dung = p.read_text(encoding="utf-8")
        for so, dong in enumerate(noi_dung.splitlines(), 1):
            # Chỉ soi dòng thực sự tạo commit — chú thích GIẢI THÍCH về dấu này là
            # hợp lệ và cần thiết, cấm luôn thì tài liệu không viết được.
            if "git commit" not in dong:
                continue
            for d in DAU:
                bang(d not in dong,
                     f"{p.name}:{so} nhét {d!r} vào thông điệp commit — dấu đó ở lại "
                     f"trong lịch sử và sẽ tắt gate của PR nào có commit này làm HEAD")


_GOI_CONG_LEASE_TRONG_WORKFLOW = re.compile(
    r"(?:^|\s)(?:python3?|py|bash|sh|exec)\s+"
    r"(\S*(?:lease_publish(?:_test)?\.py|chay_lease_publish_test\.sh))")
_RUN_INLINE = re.compile(r"^\s*(?:-\s*)?run\s*:\s*")


def _cat_chu_thich_run_inline(dong: str) -> str:
    """Cắt chú thích chắc chắn của một dòng YAML ``run:`` dạng inline.

    Shell chỉ mở chú thích ở ``#`` không được quote/escape và đứng đầu lệnh hoặc
    sau khoảng trắng. Ta theo dõi nháy đơn, nháy kép và dấu chéo ngược trên đúng
    dòng đó; ``#`` trong ``"a#b"``, ``'a#b'``, ``a\\#b`` hay ngay sau ``}}`` không
    bị cắt.

    Giới hạn có chủ ý: scalar YAML được quote, block scalar (``|``/``>``), quote
    nhiều dòng và heredoc không được phân tích. Các dạng ấy được giữ nguyên để
    t25 có thể báo oan (fail-closed), thay vì cắt khi chưa biết trạng thái quote và
    làm mất một lời gọi thật (fail-open).
    """
    moc = _RUN_INLINE.match(dong)
    if not moc:
        return dong
    lenh = dong[moc.end():]
    if not lenh or lenh[0] in "|'\">":
        return dong

    nhay = None
    thoat = False
    for i, ky_tu in enumerate(lenh):
        if thoat:
            thoat = False
            continue
        if nhay == "'":
            if ky_tu == "'":
                nhay = None
            continue
        if ky_tu == "\\":
            thoat = True
            continue
        if nhay == '"':
            if ky_tu == '"':
                nhay = None
            continue
        if ky_tu in "'\"":
            nhay = ky_tu
            continue
        if ky_tu == "#" and (i == 0 or lenh[i - 1].isspace()):
            return dong[:moc.end() + i].rstrip()
    return dong


def _cac_loi_goi_cong_lease(noi_dung: str) -> list[tuple[int, str]]:
    """Trả ``(số dòng, đối số)`` từ đúng đường quét mà t25 sử dụng."""
    ket_qua = []
    for so, dong in enumerate(noi_dung.splitlines(), 1):
        if dong.lstrip().startswith("#"):
            continue
        dong = _cat_chu_thich_run_inline(dong)
        ket_qua.extend((so, duong)
                       for duong in _GOI_CONG_LEASE_TRONG_WORKFLOW.findall(dong))
    return ket_qua


@ca
def t25_workflow_dang_lease_phai_chay_bo_kiem_NEO_khong_lay_tu_head():
    """Workflow đăng lease KHÔNG được chạy `lease_publish*.py` lấy từ head được đẩy.

    Finding P1 của cross-review trên PR #104 (14-08-2026): bản trước chạy
    `python3 ops/lease_publish.py`, tức bộ kiểm ĐẾN TỪ CHÍNH NHÁNH ĐANG BỊ KIỂM. Một
    push vào `ops/**` vừa thêm tên mình vào `NGUOI_CO_THAM_QUYEN` vừa đổi lease là đủ:
    `checkout` lấy head đó, workflow chạy bộ kiểm đã bị sửa, cả `granted_by` lẫn
    `GITHUB_ACTOR` đều qua. Bộ kiểm nằm cùng nhánh với thứ nó kiểm thì nó không kiểm gì.

    Ca này canh phần MÁY canh được: mọi lời gọi `lease_publish.py`,
    `lease_publish_test.py` hoặc wrapper chạy bộ kiểm trong workflow phải đi qua bản
    neo (`$NEO/…`), không được gọi thẳng `ops/…`.

    KHÔNG canh được ở đây, và phải nói thẳng: với sự kiện `push`, GitHub lấy chính
    tệp workflow từ head, nên ai sửa được bộ kiểm cũng sửa được ca này lẫn mỏ neo.
    Phần ấy chỉ ruleset ngoài kho mới đóng. Ca này chặn TRÔI NGƯỢC do vô ý — bản vá
    bị "dọn cho gọn" về lại `ops/…` — chứ không chặn kẻ cố tình.
    """
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Cùng chốt với t24: chỉ tha khi đây rõ ràng là BẢN SAO rời (bộ đột biến chép
        # mỗi `ops/`). Trong kho thật mà thiếu thư mục workflow thì phải ĐỎ.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh rỗng")
        return
    tep = goc / "ops-publish-lease.yml"
    bang(tep.is_file(), f"không thấy {tep} — ca này sẽ xanh mà không đo gì")
    noi_dung = tep.read_text(encoding="utf-8")
    # Chỉ soi đối số đứng sau một token lệnh thực thi đã biết, không bó theo việc dòng
    # có NHẮC tên tệp. Dòng `sha256sum ops/…` cố ý in băm của head và cố ý không có
    # `$NEO`; coi nó là lời gọi sẽ báo oan. Đây vẫn là phép đo đối số, không phải parser
    # shell: thêm một token lệnh mới phải là quyết định có chủ ý và có phản chứng.
    thay = thay_wrapper = 0
    for so, duong in _cac_loi_goi_cong_lease(noi_dung):
        thay += 1
        if duong.endswith("chay_lease_publish_test.sh"):
            thay_wrapper += 1
        bang("$NEO" in duong or "${NEO}" in duong,
             f"ops-publish-lease.yml:{so} chạy {duong!r} — bộ kiểm này đến TỪ HEAD "
             f"ĐƯỢC ĐẨY, tức từ chính nhánh nó đang kiểm (finding P1, PR #104). "
             f"Phải gọi qua bản neo vào nhánh mặc định: \"$NEO/ops/…\"")
    # Chốt riêng cho wiring bộ kiểm: đừng để việc gỡ hẳn wrapper chỉ rơi vào thông điệp
    # đếm chung, vì ba lời gọi `lease_publish.py` khác vẫn đủ làm ngưỡng cũ xanh.
    bang(thay_wrapper >= 1,
         "không thấy lời gọi thực thi `chay_lease_publish_test.sh` trong workflow — "
         "cổng đăng lease đã gỡ hẳn bộ tự kiểm mà t25 vẫn đang chạy")
    # Bốn lời gọi thật hiện tại là wrapper + check + body + mark. Ngưỡng cũ là 3 và chú
    # thích gọi chúng là (test, check, body), nhưng `test` đã chuyển sang wrapper nên ba
    # lời gọi `lease_publish.py` còn lại tự chúng thoả ngưỡng, làm cổng xanh rỗng.
    bang(thay >= 4,
         f"chỉ thấy {thay} lời gọi cổng/wrapper trong workflow — chờ ít nhất 4 "
         f"(wrapper, check, body, mark); ca này đang không đo cái nó tưởng nó đo")
    # Mỏ neo phải CÓ THẬT, không chỉ là biến `$NEO` trỏ vào hư không.
    bang("git worktree add" in noi_dung and "default_branch" in noi_dung,
         "không thấy bước dựng worktree từ `default_branch` — `$NEO` phải được neo "
         "vào nhánh mặc định, nếu không thì nó chỉ là một tên biến khác cho head")


@ca
def t41_t25_chi_cat_chu_thich_run_inline_khi_chac_chan():
    """Khóa hai ĐỎ giả mà không đổi chúng lấy một XANH giả đắt hơn."""
    an_toan = {
        "chú thích nguyên dòng": "# sh chay_lease_publish_test.sh",
        "echo nhắc tên": 'run: echo "info: chay_lease_publish_test.sh"',
        "name nhắc tên": "name: kiểm tra chay_lease_publish_test.sh tồn tại",
        "chú thích sau lệnh, dạng sh":
            "run: echo ok # sh chay_lease_publish_test.sh",
        "chú thích sau lệnh, dạng bash":
            "run: echo ok # xem bash ops/chay_lease_publish_test.sh",
    }
    for ten, noi_dung in an_toan.items():
        thay = _cac_loi_goi_cong_lease(noi_dung)
        bang(not thay, f"t25 vẫn đếm oan {ten}: {thay}")

    loi_goi_that = {
        "thiếu NEO": "run: bash ops/chay_lease_publish_test.sh",
        "# trong nháy kép":
            'run: echo "a#b"; bash ops/chay_lease_publish_test.sh',
        "# trong nháy đơn":
            "run: echo 'a#b'; bash ops/chay_lease_publish_test.sh",
        "# sau chéo ngược":
            r"run: echo a\#b; bash ops/chay_lease_publish_test.sh",
        "# liền sau biểu thức Actions":
            "run: echo ${{ github.event.issue.number }}#x; "
            "bash ops/chay_lease_publish_test.sh",
    }
    for ten, noi_dung in loi_goi_that.items():
        thay = _cac_loi_goi_cong_lease(noi_dung)
        bang(thay == [(1, "ops/chay_lease_publish_test.sh")],
             f"t25 cắt quá tay ở ca {ten}, làm mất lời gọi thật: {thay}")

    # Với block scalar/heredoc, helper không biết trạng thái xuyên dòng nên KHÔNG cắt.
    # Giữ một ĐỎ giả ở vùng chưa hiểu vẫn rẻ hơn che mất một lời gọi thật.
    dong_heredoc = "  echo ok # bash ops/chay_lease_publish_test.sh"
    bang(_cat_chu_thich_run_inline(dong_heredoc) == dong_heredoc,
         "helper đã lấn sang thân block/heredoc dù không có trạng thái xuyên dòng")


def _doi_thu_muc_reviews():
    """Trả `ops/reviews`, và ĐỎ nếu nó vắng — KHÔNG có nhánh 'vắng thì thôi'.

    Nhánh cũ bỏ qua ca khi thư mục vắng, với lý do 'bản sao không phải kho thật'. Đo ra
    thì đó là một lỗ: xoá RIÊNG `README.md` -> ĐỎ, mà xoá CẢ thư mục -> vẫn 30/30 ĐẠT.
    Tức chốt bắt được đột biến nhỏ và bỏ lọt đột biến lớn hơn chứa nó.

    Cái giá thật nằm ở chỗ khác và đắt hơn: đột biến LUÔN chạy trên bản sao tạm (bài học
    "bom hẹn giờ" — không đột biến tệp thật). Bản sao không có `.git`, nên chính chỗ duy
    nhất ta dùng để đo sức của bộ test lại là chỗ chốt tự tắt. Bộ đo mà tự tắt trong môi
    trường đo thì mọi con số nó trả về đều không neo vào đâu.

    Một bản sao `ops/` hợp lệ vốn phải chứa `reviews/`. Nên đòi thẳng.
    """
    thu_muc = HERE / "reviews"
    bang(thu_muc.is_dir(),
         f"thiếu hẳn {thu_muc}. KHÔNG bỏ qua ca khi thư mục vắng: bản sao `ops/` hợp lệ "
         f"vốn phải chứa nó. Nhánh 'vắng thì thôi' từng làm CẢ t26 lẫn t27 XANH khi đột "
         f"biến xoá trọn thư mục — bắt được cái nhỏ, lọt cái to hơn chứa nó.")
    return thu_muc


def _bang(van: str, tieu_de: str) -> list:
    """Trả các HÀNG DỮ LIỆU của bảng dưới `## <tieu_de>`, mỗi hàng là dict {tên cột: ô}.

    SÁU bậc thu hẹp, mỗi bậc vì một lỗ ĐO ĐƯỢC. Chuỗi này mới là bài học, không phải
    từng bậc riêng lẻ:

    1. `in` cả tệp        -> id sót ở prose vẫn ĐẠT
    2. `in` các DÒNG bảng -> id trong `<!-- -->` trên dòng '|' vẫn ĐẠT
    3. `in` mọi Ô         -> tái dùng id được thoả bởi hàng của verdict KHÁC
    4. theo HÀNG          -> mô tả của hàng nhắc CHÉO verdict khác + id của nó vẫn ĐẠT
    5. theo CỘT CÓ TÊN    -> nhưng lấy cột thành HAI danh sách rồi `zip` thì hàng thiếu ô
       bị lọc lệch nhau ⇒ `zip` ghép ô của HAI hàng khác nhau; và bảng KHÔNG có hàng
       gạch phân cách vẫn được nhận, dù GitHub không render nó thành bảng.
    6. nay: đòi hàng gạch, và trả HÀNG-CÓ-KHOÁ — không bao giờ tách cột rồi ghép lại.

    Bậc 5 là bậc do CHÍNH bản vá bậc 4 sinh ra: tôi ràng "cùng hàng" bằng một cơ chế tự
    nó phá vỡ ranh giới hàng. Vá một lớp bằng cách mở một lớp khác.
    """
    import re
    van = re.sub(r"<!--.*?-->", "", van, flags=re.S)      # comment: người đọc KHÔNG thấy
    ra, lay, rao = [], False, None
    dau_bang, cho_gach = None, False

    def la_gach(dong):
        o = [x.strip() for x in dong.strip().strip("|").split("|")]
        return bool(o) and all(x and set(x) <= set("-: ") for x in o)

    for dong in van.splitlines():
        # Rào mã: PHẢI nhớ ký tự mở và ĐỘ DÀI. Cờ bật/tắt thô bỏ sót rào `~~~` và đóng
        # sớm rào ```` khi gặp dòng ``` bên trong — Markdown thì không đóng.
        m = re.match(r"^\s*(`{3,}|~{3,})", dong)
        if m:
            k, d = m.group(1)[0], len(m.group(1))
            if rao is None:
                rao = (k, d)
            elif k == rao[0] and d >= rao[1] and not dong.strip()[d:].strip():
                rao = None
            continue
        if rao is not None:                                # bảng trong khối mã là ví dụ
            continue
        if dong.startswith("## "):
            lay, dau_bang, cho_gach = (tieu_de in dong), None, False
            continue
        if not lay:
            continue
        if not dong.strip().startswith("|"):
            dau_bang, cho_gach = None, False               # hết bảng
            continue

        o = [x.strip().strip("`").strip() for x in dong.strip().strip("|").split("|")]
        if dau_bang is None:                               # ứng viên hàng tiêu đề
            dau_bang, cho_gach = [x.lower() for x in o], True
            continue
        if cho_gach:
            # Không có hàng gạch thì GitHub KHÔNG render thành bảng. Bộ đọc cũ chỉ BỎ QUA
            # hàng gạch chứ không ĐÒI nó, nên xoá `|---|` đi là người đọc mất bảng mà
            # `t27` vẫn xanh.
            if la_gach(dong):
                cho_gach = False
            else:
                dau_bang, cho_gach = None, False
            continue
        if la_gach(dong):
            continue
        ra.append({ten: o[i] for i, ten in enumerate(dau_bang) if i < len(o)})
    return ra


def _cot_duy_nhat(van: str, tieu_de: str, ten_cot: str) -> str:
    """Kiểm tên cột tồn tại và DUY NHẤT trong bảng; trả về khoá đã chuẩn hoá."""
    hang = _bang(van, tieu_de)
    bang(hang, f"bảng dưới '## …{tieu_de}…' RỖNG, thiếu hàng gạch `|---|`, hoặc không "
               f"có — không kiểm được gì")
    ten = ten_cot.strip().lower()
    dem = sum(1 for k in hang[0] if k == ten)
    bang(dem == 1,
         f"bảng '{tieu_de}': cột {ten_cot!r} xuất hiện {dem} lần — không định danh được "
         f"cột thì mọi phép kiểm theo cột chỉ là đoán")
    return ten


def _ten_tep(o: str) -> set:
    """Rút TÊN TỆP trong một ô, để so BẰNG NHAU thay vì so chuỗi con.

    Vì sao: `foo-verdict.md` là chuỗi con của `old-foo-verdict.md`, nên một hàng mục lục
    của tệp NÀY thoả luôn cho tệp KIA. Hai tên chồng nhau là đủ để một verdict không có
    hàng riêng mà vẫn xanh.
    """
    import re
    return set(re.findall(r"[\w.\-/]+\.(?:md|ya?ml)", o))


@ca
def t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi():
    """Biên nhận giao hàng trong `ops/reviews/` phải khớp băm tệp gốc.

    Vì sao có: verdict của reviewer là tệp NGUYÊN VĂN neo băm, không được sửa — kể cả
    để điền `evidence_url` sau khi đăng. Nên chỗ đăng được ghi ra một tệp biên nhận
    RIÊNG. Nhưng một biên nhận trỏ vào tệp đã đổi thì tệ hơn không có biên nhận: nó
    khai một con băm không còn đúng, mà người đọc lại tin. Ca này buộc hai thứ đi
    cùng nhau — đổi tệp gốc mà quên biên nhận thì ĐỎ.
    """
    import hashlib
    import yaml
    thu_muc = _doi_thu_muc_reviews()
    ds = sorted(thu_muc.glob("*.receipt.yaml"))
    bang(ds, f"không thấy biên nhận nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")
    for p in ds:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        duong = str(d.get("verdict_path") or "").strip()
        sha = str(d.get("verdict_sha256") or "").strip()
        bang(duong and sha,
             f"{p.name}: biên nhận NỬA VỜI (verdict_path={duong!r} sha={sha!r}) — "
             f"băm không địa chỉ thì không kiểm được, địa chỉ không băm thì tệp đổi "
             f"lúc nào cũng không ai biết")
        f = HERE.parent / duong
        bang(f.is_file(), f"{p.name}: trỏ vào tệp không có: {duong}")
        thuc = hashlib.sha256(f.read_bytes()).hexdigest()
        bang(thuc == sha,
             f"{p.name}: LỆCH BĂM — biên nhận khai {sha}, tệp {duong!r} thực {thuc}. "
             f"Tệp verdict là NGUYÊN VĂN của reviewer: hoặc bạn vừa sửa nhầm nó, hoặc "
             f"biên nhận chưa cập nhật. Đừng ghi đè băm cho hết đỏ trước khi biết là ca nào.")
        # Biên nhận mà không nói đăng ở đâu thì nó không phải biên nhận.
        bang(str(d.get("evidence_url") or "").startswith("https://"),
             f"{p.name}: thiếu `evidence_url` dạng https — đây chính là trường mà bản "
             f"gốc để `pending-owner-post`, và là lý do biên nhận này tồn tại")


@ca
def t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc():
    """Mọi verdict/biên nhận phải có trong `ops/reviews/README.md`, và mọi caveat phải nêu tên ở đó.

    Vì sao có (finding của codex trên PR #114, ĐÚNG): tệp verdict là nguyên văn neo băm
    nên chỗ sai không vá được tại nguồn, và đính chính phải sống ở biên nhận. Nhưng
    người mở thẳng `verdict_path` để chạy lại lệnh KHÔNG có gì trỏ họ sang tệp sidecar
    — quét cả kho cũng không có bộ đọc nào đưa `verdict_usage_caveats` ra. Nghĩa là bản
    vá đầu tiên chỉ DỜI vấn đề sang một tệp ít người mở hơn, không giải nó.

    Ca này biến mục lục thành chốt: thêm caveat mà quên nâng lên `README.md` thì ĐỎ.
    Nó KHÔNG khẳng định mục lục đủ để cứu mọi người đọc — giới hạn ấy ghi ngay trong
    README. Nó chỉ bảo đảm một điều kiểm được: cảnh báo không nằm im một chỗ.

    BA LỖ đã bịt (codex tìm trên cây đã merge của PR #114; cả ba tái lập được trên
    master trước khi vá, cả ba đều cho 30/30 ĐẠT):

      L1  không có thư mục `ops/reviews`               -> ĐỎ qua `_doi_thu_muc_reviews`
      L2  bỏ caveat khỏi BẢNG, giữ id trong comment    -> soi Ô của bảng cảnh báo
      L3  thả một `*-verdict.md` mồ côi                -> glob verdict ĐỘC LẬP

    BA LỖ NỮA (codex tìm trên chính bản vá ba lỗ trên; cả ba cũng 30/30 ĐẠT trước khi vá):

      N1  id chỉ còn trong `<!-- … -->` TRÊN một dòng `|`  -> bỏ comment TRƯỚC khi tách Ô
      N2  tên verdict/biên nhận chỉ còn ở prose            -> soi Ô của bảng 'Mục lục'
      N3  biên nhận đúng tên nhưng `verdict_path` trỏ tệp KHÁC -> so khớp đường dẫn

    N1 và N2 đáng ghi hơn cả: bản vá L2 sinh ra để bịt lỗ comment HTML, rồi **tự nó vẫn
    thủng bằng đúng comment HTML** — vì nó chỉ thu hẹp PHẠM VI (dòng bảng) mà không đổi
    THỨ ĐEM SO (văn bản thô). Và tôi áp ý "soi trong bảng" cho caveat mà quên áp cho mục
    lục — cùng một khẳng định, hai vị trí, lần thứ tư trong đợt này.
    """
    import yaml
    thu_muc = _doi_thu_muc_reviews()
    muc_luc = thu_muc / "README.md"
    bang(muc_luc.is_file(),
         f"thiếu {muc_luc} — thư mục verdict không có cửa vào thì cảnh báo trong biên "
         f"nhận không tới được ai")
    van = muc_luc.read_text(encoding="utf-8")
    CB = "Cảnh báo đang có hiệu lực"
    ML = "Mục lục"
    k_cb_v = _cot_duy_nhat(van, CB, "tệp verdict")
    k_cb_id = _cot_duy_nhat(van, CB, "id")
    k_ml_v = _cot_duy_nhat(van, ML, "tệp verdict")
    k_ml_bn = _cot_duy_nhat(van, ML, "biên nhận")
    hang_cb = _bang(van, CB)
    hang_ml = _bang(van, ML)
    bang(hang_ml, f"{muc_luc.name}: bảng 'Mục lục' RỖNG — mục lục rỗng thì mọi phép "
                  f"kiểm dưới đây chỉ là hình thức")

    def co_o_cot(ten, hang, khoa):
        """Tên tệp phải BẰNG một tên trong ô của đúng cột — không phải chuỗi con."""
        return any(ten in _ten_tep(h.get(khoa, "")) for h in hang)

    ds = sorted(thu_muc.glob("*.receipt.yaml"))
    ds_verdict = sorted(thu_muc.glob("*-verdict.md"))
    bang(ds, f"không thấy biên nhận nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")
    bang(ds_verdict, f"không thấy verdict nào trong {thu_muc} — ca này sẽ xanh mà không đo gì")

    # L3 — duyệt VERDICT theo đĩa, KHÔNG suy từ biên nhận. Suy từ biên nhận thì một
    # verdict chưa ai làm biên nhận sẽ vô hình đúng lúc nó cần bị thấy nhất.
    for f in ds_verdict:
        bang(co_o_cot(f.name, hang_ml, k_ml_v),
             f"{muc_luc.name}: verdict {f.name!r} KHÔNG có trong CỘT 'tệp verdict' của "
             f"bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột "
             f"mô tả nào đó thì bảng render ra vẫn thiếu nó.")
        bn = thu_muc / f"{f.stem}.receipt.yaml"
        bang(bn.is_file(),
             f"{f.name}: KHÔNG có biên nhận {bn.name}. Verdict không biên nhận là verdict "
             f"không ai khai đã đăng ở đâu — và `t26` cũng không đụng tới nó.")
        # N3+P1 — đúng TÊN chưa đủ, và đúng BASENAME cũng chưa đủ. So ĐƯỜNG DẪN ĐẦY ĐỦ:
        # một biên nhận trỏ `ops/reviews/archive/x.md` trong khi tệp thật nằm ở
        # `ops/reviews/x.md` có basename y hệt, nên t26 đi băm BẢN LƯU TRỮ còn tệp thật
        # không ca nào đụng tới. Đã đo: thay ruột tệp thật bằng rác mà suite vẫn 30/30.
        d_bn = yaml.safe_load(bn.read_text(encoding="utf-8")) or {}
        tro = PurePosixPath(str(d_bn.get("verdict_path") or "").strip().lstrip("./"))
        mong = PurePosixPath(f.relative_to(HERE.parent).as_posix())
        bang(tro == mong,
             f"{bn.name}: `verdict_path` trỏ {str(tro)!r} chứ không phải {str(mong)!r}. "
             f"So basename thôi thì một bản sao ở thư mục khác lọt qua, và tệp THẬT "
             f"không được băm bởi bất kỳ ca nào.")

    for p in ds:
        d = yaml.safe_load(p.read_text(encoding="utf-8")) or {}
        bang(co_o_cot(p.name, hang_ml, k_ml_bn),
             f"{muc_luc.name}: biên nhận {p.name} KHÔNG có trong CỘT 'biên nhận' của "
             f"bảng 'Mục lục'")
        ten_verdict = Path(str(d.get("verdict_path") or "")).name
        bang(ten_verdict and co_o_cot(ten_verdict, hang_ml, k_ml_v),
             f"{muc_luc.name}: verdict {ten_verdict!r} KHÔNG có trong CỘT 'tệp verdict' "
             f"của bảng 'Mục lục'")

        cac_caveat = d.get("verdict_usage_caveats") or []
        for c in cac_caveat:
            ma = str((c or {}).get("id") or "").strip()
            bang(ma, f"{p.name}: có caveat KHÔNG có `id` — không nêu tên được thì "
                     f"không nâng lên mục lục được, và cũng không ai trích dẫn được")
            # L2+N4+P3 — id phải nằm ở CỘT `id`, trên CÙNG HÀNG với tên verdict ở CỘT
            # `tệp verdict`. Ràng theo hàng thôi vẫn thủng: phần mô tả của một hàng nhắc
            # CHÉO tên verdict khác kèm id của nó thì phép kiểm "cả hai chuỗi có mặt đâu
            # đó trong hàng" nhận nhầm đó là cảnh báo của verdict thứ hai.
            bang(any(ma in {x.strip() for x in h.get(k_cb_id, "").split()}
                     and ten_verdict in _ten_tep(h.get(k_cb_v, ""))
                     for h in hang_cb),
                 f"{muc_luc.name}: caveat {ma!r} của {p.name} KHÔNG nằm ở CỘT 'id' trên "
                 f"cùng hàng với {ten_verdict!r} ở CỘT 'tệp verdict', trong bảng "
                 f"'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác "
                 f"KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.")


@ca
def t31_moi_workflow_cai_pyyaml_phai_GHIM_va_ghim_CUNG_MOT_ban():
    """Mọi bước cài PyYAML trong workflow phải ghim exact, và tất cả cùng một số.

    Vì sao có, hai lớp:

    1. **Spec trần.** Cross-review PR #134 (codex) nêu `unpinned-pyyaml-ci-dependency`:
       `pip install pyyaml` không biên làm CÙNG MỘT SHA có thể xanh hôm nay và đỏ sau
       này mà cây không đổi. Cùng lớp với tiền lệ `pypdf>=4.0` không có trần. Bộ kiểm
       cổng đăng lease chạy ở đường có `contents: write` + `issues: write`, nên một
       dependency trôi ở đó là trôi ngay dưới chân cổng.

    2. **Hai bản sẽ trôi lệch.** Bản vá cho lớp 1 ghi `PyYAML==6.0.3` vào HAI tệp
       workflow. CLAUDE.md đã ghi đúng hình dạng này ở ca quét secrets: *"hai bản sẽ
       trôi lệch, và bên quên cập nhật chính là bên đẩy lọt"*. Nâng bản ở một chỗ mà
       quên chỗ kia thì hai đường chạy hai runtime khác nhau, và chỗ quên là chỗ không
       ai đo. Ca này biến lời hứa "nhớ sửa cả hai" thành chốt.

    Ca này sinh ra từ chính lượt vá lớp 1: nghĩ ra được rủi ro thì phải biến ngay thành
    ca test, đừng để nó nằm trong chú thích — chỗ đó là nơi các ca đi chết.
    """
    import re
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Cùng chốt chống xanh-rỗng với `t24`: chỉ tha khi đây rõ ràng là BẢN SAO rời.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh rỗng")
        return
    ds = sorted(p for p in goc.iterdir() if p.suffix in (".yml", ".yaml"))
    bang(ds, f"không thấy workflow nào trong {goc} — ca này sẽ xanh mà không đo gì")

    # Bắt MỌI dòng cài pyyaml, kể cả viết hoa/thường khác nhau, rồi mới xét nó có ghim
    # không. Bắt theo `pip install` chứ không theo `PyYAML==` — nếu chỉ tìm dạng ĐÚNG
    # thì một dòng SAI (spec trần) không khớp mẫu và ca này im lặng cho qua.
    RE_CAI = re.compile(r"pip\s+install\b[^\n]*?\bpyyaml", re.I)
    RE_GHIM = re.compile(r"\bPyYAML==(\d+(?:\.\d+)*)\b", re.I)

    thay = []
    for p in ds:
        for so, dong in enumerate(p.read_text(encoding="utf-8").splitlines(), 1):
            if not RE_CAI.search(dong):
                continue
            m = RE_GHIM.search(dong)
            bang(m, f"{p.name}:{so} cài PyYAML mà KHÔNG ghim exact: {dong.strip()!r} — "
                    f"spec trần làm cùng một SHA xanh hôm nay, đỏ sau này mà cây không đổi")
            thay.append((p.name, so, m.group(1)))

    # Chốt chống xanh-rỗng: hai tệp ĐANG có bước cài. Bộ này về 0 nghĩa là mẫu khớp
    # hỏng, không phải cây sạch — và khi ấy hai chốt trên không đo gì.
    bang(len(thay) >= 2,
         f"chỉ thấy {len(thay)} bước cài PyYAML (đợi >= 2) — mẫu khớp có thể đã hỏng; "
         f"ca xanh vì không tìm thấy gì thì tệ hơn ca đỏ")

    ban = {v for _, _, v in thay}
    bang(len(ban) == 1,
         f"các workflow ghim PyYAML LỆCH NHAU: "
         f"{', '.join(f'{t}:{s}={v}' for t, s, v in thay)} — hai đường chạy hai runtime "
         f"khác nhau, và chỗ quên nâng bản chính là chỗ không ai đo")


def _than_buoc_chon_lease() -> str:
    """Trích THÂN bước `tìm lease vừa đổi` TỪ CHÍNH tệp workflow.

    Chép lại thân bước vào test là dựng hai bản sẽ trôi lệch, và bên quên cập nhật
    chính là bên đẩy lọt — cùng nếp mà `ops/don_ref_chot_test.sh` đã phải học.
    """
    import yaml
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # Cùng chốt với t24/t25: chỉ tha khi đây rõ ràng là BẢN SAO rời. Trong kho thật
        # mà thiếu thư mục workflow thì phải ĐỎ, kẻo ca xanh rỗng.
        assert not (HERE.parent / ".git").exists(), \
            f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì"
        return ""
    tep = goc / "ops-publish-lease.yml"
    assert tep.is_file(), f"không thấy {tep} — ca này sẽ xanh mà không đo gì"
    d = yaml.safe_load(tep.read_text(encoding="utf-8"))
    buoc = [b for b in d["jobs"]["dang"]["steps"] if b.get("name") == "tìm lease vừa đổi"]
    assert len(buoc) == 1, f"chờ ĐÚNG một bước `tìm lease vừa đổi`, thấy {len(buoc)}"
    b = buoc[0]
    # ĐIỀU KIỆN ĐỂ CA NÀY TỒN TẠI: thân bước không còn `${{ }}`. Còn biểu thức thì nó
    # KHÔNG chạy lại được ngoài Actions, và ta sẽ chỉ đo một bản chép tay.
    assert "${{" not in b["run"], \
        "thân `run` còn nội suy biểu thức Actions — GitHub nội suy trên TOÀN BỘ thân " \
        "trước khi shell thấy nó (một cặp rỗng trong CHÚ THÍCH đã làm hỏng cả " \
        "ops-don-ref.yml, run 31971137920: 0 job), và thân có biểu thức thì không " \
        "chạy lại được ở đây. Khai qua `env:`."
    assert set(b.get("env") or {}) >= {"TRUOC", "NAY", "MAC_DINH"}, \
        f"bước phải khai TRUOC/NAY/MAC_DINH qua `env:`, thấy {list(b.get('env') or {})}"
    return b["run"]


def _kho_thu(tmp: Path):
    """Dựng kho có `origin` THẬT: master mang một lease CŨ, HẾT HẠN, CHƯA TỪNG ĐĂNG.

    `commit.gpgsign=false` KHÔNG phải cho gọn — nó đóng một finding P2 của cross-review
    lượt 2 (codex, head `23588c97`). Trên máy có `commit.gpgsign=true` toàn cục mà signer
    không gọi được, fixture chết bằng `fatal: failed to write commit object` và `t32` ĐỎ vì
    **cấu hình của host**, không vì thứ nó đo. Reviewer đo được cả hai chiều: `rc=1 32/33`
    với signing bật, `rc=0 33/33` khi tắt.

    Một cổng đỏ vì lý do không liên quan tệ ngang một cổng xanh giả: cả hai đều làm người
    đọc đi sai hướng. Phạm vi tắt signing chỉ trong kho fixture tạm — không đụng kho thật,
    không che ca nào về chữ ký.
    """
    def g(cay, *a):
        return subprocess.run(["git", "-c", "user.email=a@b", "-c", "user.name=c",
                               "-c", "commit.gpgsign=false",
                               "-C", str(cay), *a],
                              capture_output=True, text=True, check=True)
    goc = tmp / "origin.git"
    subprocess.run(["git", "init", "-q", "--bare", str(goc)], check=True)
    cay = tmp / "cay"
    subprocess.run(["git", "clone", "-q", str(goc), str(cay)], check=True)
    # DỰNG LẠI ĐÚNG MÁY ĐÃ LÀM t32 ĐỎ, ngay trong fixture — nếu không thì chốt trên chỉ là
    # lời hứa: nó chạy xanh cả khi ai đó gỡ `-c commit.gpgsign=false` ra, trên một máy
    # không bật signing. Đặt ở LOCAL config vì `-c` dòng lệnh thắng config tệp; gỡ `-c` ra
    # là fixture chết ngay, tức ca này ĐO chốt chứ không chỉ mang chốt.
    # BÁM ĐÚNG KHOÁ, và đây là chỗ bản đầu SAI: nó đặt `gpg.program` — khoá của định dạng
    # **openpgp** — trong khi máy dựng fixture khai `gpg.format=ssh`, nên chốt giả bám vào
    # một khoá không ai đọc và mutant "gỡ `-c commit.gpgsign=false`" SỐNG SÓT (đo được:
    # `giet 0/1`). Ép luôn `gpg.format=ssh` để fixture không phụ thuộc cấu hình host, rồi
    # trỏ `gpg.ssh.program` vào một đường dẫn không tồn tại.
    for k, v in (("commit.gpgsign", "true"),
                 ("gpg.format", "ssh"),
                 ("user.signingkey", "khong-phai-khoa-that"),
                 ("gpg.ssh.program", str(tmp / "signer-khong-ton-tai"))):
        subprocess.run(["git", "-C", str(cay), "config", k, v], check=True)
    (cay / "ops" / "leases").mkdir(parents=True)
    # Chính hình dạng đã giết cổng ngày 20-08: hết hạn, KHÔNG `posted_comment_id`.
    (cay / "ops" / "leases" / "cu-het-han.yaml").write_text(
        f"lease_id: cu-het-han\nlease_expires_at_utc: '{khi_truoc(48)}'\n", encoding="utf-8")
    g(cay, "add", "-A")
    g(cay, "commit", "-qm", "nen")
    g(cay, "branch", "-M", "master")
    g(cay, "push", "-q", "origin", "master")
    return cay, g


def _bash_posix() -> str:
    """Trả đường dẫn `bash` POSIX THẬT — KHÔNG phải `bash` của WSL.

    ĐÃ TRẢ GIÁ (master `e03c6d28`, run 32351777642, job `gate (windows-latest)`):
    `subprocess.run(["bash", ...])` trên runner Windows phân giải sang
    `C:\\Windows\\System32\\bash.exe` — cửa vào WSL — và nó trả

        Windows Subsystem for Linux has no installed distributions.

    với `rc=1`. Ca `t32` đọc mã ấy thành "bước chọn lease ĐỎ" và báo một finding KHÔNG CÓ
    THẬT, trong khi thứ hỏng là **trình thông dịch**, không phải thân bước.

    Cùng họ với bài học `taskkill` của kho: một cái TÊN phân giải sang thứ khác trên nền
    khác. Nên ở đây dùng DANH SÁCH CHO PHÉP (Git Bash), và loại thẳng `System32`.

    Nói rõ phạm vi: bước được đo chạy trong job `runs-on: ubuntu-latest`, nên Windows chỉ
    là nơi bộ test tình cờ chạy. Nhưng "tình cờ" mà báo finding giả thì vẫn phải chữa.
    """
    import os
    import shutil
    if os.name != "nt":
        return "bash"
    ung_vien = [
        r"C:\Program Files\Git\bin\bash.exe",
        r"C:\Program Files (x86)\Git\bin\bash.exe",
        r"C:\Program Files\Git\usr\bin\bash.exe",
    ]
    for d in ung_vien:
        if Path(d).is_file():
            return d
    tim = shutil.which("bash")
    # `System32\bash.exe` LÀ WSL. Nhận nó là tự chuốc một finding giả.
    if tim and "system32" not in tim.replace("/", "\\").lower():
        return tim
    return ""


def _chay_than(than: str, cay: Path, truoc: str, nay: str, mac_dinh: str = "master"):
    import os
    mt = dict(os.environ, TRUOC=truoc, NAY=nay, MAC_DINH=mac_dinh)
    vo = _bash_posix()
    # KHÔNG ĐO ĐƯỢC ≠ ĐẠT: thiếu bash POSIX thì ném, để `t32` ĐỎ với đúng lý do — chứ
    # không lặng lẽ trả một kết quả rỗng rồi được đếm là qua.
    if not vo:
        raise AssertionError(
            "KHÔNG ĐO ĐƯỢC: không tìm thấy `bash` POSIX (Git Bash). `bash` trong "
            "System32 là WSL, không dùng được để chạy thân bước.")
    p = subprocess.run([vo, "-c", than], cwd=str(cay), env=mt,
                       capture_output=True, text=True)
    ds = (cay / "ds.txt")
    return p.returncode, (ds.read_text(encoding="utf-8").split() if ds.is_file() else []), p.stderr + p.stdout


ZERO40 = "0" * 40


@ca
def t32_buoc_chon_lease_KHONG_duoc_quet_CA_THU_MUC():
    """Push MỞ NHÁNH MỚI chỉ được xử lý lease mà NHÁNH ẤY thêm — không phải cả thư mục.

    VÌ SAO CÓ CA NÀY, và nó không phải giả thiết: lượt chạy `32342373756`
    (2026-08-20T07:05Z, push nhánh `ops/lease-plat-m4-exec-1`) ĐỎ `rc=8`. Log liệt kê
    BẢY tệp lease KHÔNG nằm trong push đó ⇒ nó đi vào đường dự phòng
    `find ops/leases -type f`. Tệp giết cổng là `don-nhanh-base-review-6-…`: KHÔNG có
    `posted_comment_id`, hạn `2026-08-18T17:45Z`.

    Hệ quả: từ 18-08 tới 20-08, MỌI lease mới không đăng được, và không ai biết — cổng
    không nói dối, nó VẮNG MẶT. Chú thích cũ khai "chốt `posted_comment_id` lo phần
    không đăng trùng": đúng cho lease ĐÃ đăng (rc=9), sai cho lease CHƯA TỪNG đăng.

    Và mọi lease đều đi bằng một nhánh MỚI theo `ops/README.md`, nên đường "dự phòng"
    ấy thật ra là đường CHÍNH — đúng lớp bệnh "nhánh không-thấy-thì-bỏ-qua nằm im tới
    đúng lúc cần".
    """
    than = _than_buoc_chon_lease()
    if not than:
        return
    with tempfile.TemporaryDirectory() as t:
        tmp = Path(t)
        cay, g = _kho_thu(tmp)
        g(cay, "checkout", "-qb", "ops/lease-moi")
        (cay / "ops" / "leases" / "moi.yaml").write_text(
            f"lease_id: moi\nlease_expires_at_utc: '{mai_sau()}'\n", encoding="utf-8")
        g(cay, "add", "-A")
        g(cay, "commit", "-qm", "lease moi")
        head1 = g(cay, "rev-parse", "HEAD").stdout.strip()

        # (1) NHÁNH MỚI: `before` toàn số 0. Chỉ được thấy lease nhánh này thêm.
        rc, ds, ra = _chay_than(than, cay, ZERO40, head1)
        assert rc == 0, f"nhánh mới mà bước chọn lease ĐỎ (rc={rc}): {ra}"
        assert ds == ["ops/leases/moi.yaml"], \
            f"chờ ĐÚNG lease nhánh này thêm, được {ds} — quét cả thư mục thì một lease " \
            f"cũ hết hạn sẽ giết cả lượt đăng (bug #195)"

        # (2) PUSH THƯỜNG trên cùng nhánh: vẫn phải diff `before`..`sha`, không lùi về
        # merge-base — lùi về đó là kéo theo cả lease của commit TRƯỚC, đã đăng rồi.
        (cay / "ops" / "leases" / "moi2.yaml").write_text(
            f"lease_id: moi2\nlease_expires_at_utc: '{mai_sau()}'\n", encoding="utf-8")
        g(cay, "add", "-A")
        g(cay, "commit", "-qm", "lease moi 2")
        head2 = g(cay, "rev-parse", "HEAD").stdout.strip()
        rc, ds, ra = _chay_than(than, cay, head1, head2)
        assert rc == 0, f"push thường mà ĐỎ (rc={rc}): {ra}"
        assert ds == ["ops/leases/moi2.yaml"], f"push thường: chờ moi2.yaml, được {ds}"

        # (3) KHÔNG ĐO ĐƯỢC ≠ KHÔNG CÓ GÌ. Mốc so không phân giải được thì phải ĐỎ, chứ
        # không được trả danh sách rỗng — rỗng đọc y hệt "không có lease nào để đăng".
        rc, ds, ra = _chay_than(than, cay, ZERO40, head2, mac_dinh="nhanh-khong-ton-tai")
        assert rc != 0, f"mốc so không phân giải được mà rc=0, ds={ds}: {ra}"
        assert "KHONG DO DUOC" in ra, f"đỏ mà không nói KHÔNG ĐO ĐƯỢC: {ra!r}"

        # ...và nhánh mặc định RỖNG cũng là không đo được, không phải "quét tất".
        rc, _ds, ra = _chay_than(than, cay, ZERO40, head2, mac_dinh="")
        assert rc != 0, f"MAC_DINH rỗng mà vẫn chạy tiếp: {ra}"


@ca
def t33_workflow_dang_lease_phai_qua_actionlint():
    """`actionlint` phải XANH trên mọi workflow — và THIẾU công cụ là ĐỎ, không phải bỏ qua.

    "YAML parse được" KHÁC "GitHub NHẬN". Đo 16-08-2026: `ops-don-ref.yml` bị GitHub từ
    chối, dấu hiệu là một run mang tên ĐƯỜNG DẪN TỆP, 0 job, `conclusion: failure` — lỗi
    XÁC THỰC ĐỊNH NGHĨA, không phải một job đỏ. SÁU lượt cross-review đều kết luận "YAML
    ok" vì cả sáu chỉ kiểm bằng PyYAML, mà PyYAML không biết luật của GitHub.

    Một cổng tự tắt khi thiếu công cụ là cổng không tồn tại đúng lúc nó cần nhất, nên ca
    này ĐỎ khi không có `actionlint` — trừ khi đây là bản sao rời không có `.git`.
    """
    import shutil
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        assert not (HERE.parent / ".git").exists(), \
            f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì"
        return
    duong = shutil.which("actionlint")
    assert duong, (
        "KHÔNG ĐO ĐƯỢC: thiếu `actionlint`. PyYAML không thay được nó — nó không biết "
        "luật của GitHub. Cài: go install github.com/rhysd/actionlint/cmd/actionlint@latest "
        "(hoặc `brew install actionlint`, hoặc tải bản dựng sẵn từ releases).")
    p = subprocess.run([duong, str(goc / "ops-publish-lease.yml")],
                       capture_output=True, text=True)
    assert p.returncode == 0, f"actionlint ĐỎ (rc={p.returncode}):\n{p.stdout}{p.stderr}"


def _dong_lenh(than: str) -> list:
    """Tách thân `run` thành các LỆNH: nối dòng bị ngắt bằng `\\`, rồi bỏ chú thích.

    NỐI TRƯỚC, LỌC SAU — và thứ tự ấy là một finding của chính bộ test này chứ không phải
    lý thuyết: bản đầu khớp theo TỪNG DÒNG, nên lệnh

        curl -fsSL -o "$DICH/goi" \\
          "https://…/actionlint/releases/download/v${AL_VER}/${GOI}"

    có `curl` ở dòng một và `actionlint` ở dòng hai ⇒ không dòng nào chứa CẢ HAI, và phép
    kiểm kết luận "workflow không cài actionlint" trong khi nó cài. Một phép quét đọc lệnh
    mà không hiểu dấu nối dòng thì nó đang đọc VĂN BẢN, không đọc LỆNH.
    """
    noi, dem = [], ""
    for d in than.splitlines():
        if d.lstrip().startswith("#"):
            continue
        dem = f"{dem} {d.strip()}" if dem else d.strip()
        if dem.endswith("\\"):
            dem = dem[:-1].rstrip()
            continue
        if dem:
            noi.append(dem)
        dem = ""
    if dem:
        noi.append(dem)
    return noi


@ca
def t34_workflow_khong_duoc_goi_THANG_tep_bo_test():
    """Phương án (1): chỉ canh lời gọi thẳng tệp `.py`, không phân tích shell.

    Wrapper đã gộp installer + selftest thành một tiến trình. Vì vậy chốt này KHÔNG còn
    tuyên bố "đã chứng minh job cài công cụ trước khi chạy"; nó chỉ bắt một hồi quy hẹp,
    đọc được: workflow gọi thẳng `lease_publish_test.py` thay vì đi qua wrapper.

    Hai phản chứng vòng 2 vẫn đỏ vì cả hai đều đưa lời gọi thẳng `.py` trở lại job chạy
    test, dù installer nằm ở job khác hay nằm sau nó. `bash -c "python ...py"` cũng đỏ vì
    vẫn chứa chính lời gọi thẳng ấy.

    PHẠM VI ĐO ĐƯỢC: t34 chỉ nhận canonical
    `python|python3|py <đường-dẫn>/lease_publish_test.py` KHÔNG CỜ. Năm dạng đã đo là
    lọt: `python -m ops.lease_publish_test`; `python3 -u ops/lease_publish_test.py`;
    shebang trực tiếp `./ops/lease_publish_test.py`; `uv run ops/lease_publish_test.py`;
    và `python -X utf8 ops/lease_publish_test.py`. Runner khác ngoài ba token canonical
    cũng không thuộc lời hứa. Lời khai được hạ xuống đúng phép đo thay vì nối regex để
    đuổi theo cú pháp shell; quyết định danh sách cho phép đã tách sang packet `#209`.

    Đổi wrapper thành một trong các dạng lọt vẫn có cùng nghĩa với xoá wiring của gate;
    một selftest không thể tự chứng minh nó đã được CI gọi.

    PHẠM VI BẰNG SỐ: `t34` che **3/8 = 37,5%** dạng gọi đã biết (3 canonical nhận được,
    5 dạng đã đo là lọt). Nói bằng số vì "che phần lớn" là lời khai không có phép đo, và
    kho đã trả giá đúng hình dạng ấy nhiều lần.

    NỢ CÓ TÊN `PLAT-X5-required-status-check`: branch protection phải require status của
    job `gate` (và lượt đăng lease tương ứng). Chốt ngoài kho ấy mới trả lời "CI có thật sự
    chạy gate không". `t34` chỉ là lan can chống hồi quy vô ý, không phải security boundary.
    Q7 ĐÃ QUYẾT (21-08-2026, `ducthangho`): KHÔNG BẬT ⇒ nợ này là THƯỜNG TRỰC, ghi ở
    `ops/NO_KY_THUAT.md` §9. `t42` bên dưới canh cho docstring này không trôi rộng ra.
    """
    import yaml
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì")
        return
    goi_thang = []
    for tep in sorted(goc.glob("*.yml")) + sorted(goc.glob("*.yaml")):
        d = yaml.safe_load(tep.read_text(encoding="utf-8")) or {}
        for ten_job, job in (d.get("jobs") or {}).items():
            for i, b in enumerate(job.get("steps") or []):
                than = b.get("run")
                if not isinstance(than, str):
                    continue
                for lenh in _dong_lenh(than):
                    if _CHAY_BO_TEST.search(lenh):
                        goi_thang.append(
                            f"{tep.name}:{ten_job}:bước {i} ({b.get('name') or 'không tên'})")
    bang(not goi_thang,
         f"workflow gọi THẲNG `lease_publish_test.py` thay vì wrapper: {goi_thang}. "
         f"Chuyển cài + chạy về `ops/chay_lease_publish_test.sh`; không mở rộng regex "
         f"để giả vờ chứng minh mọi cú pháp shell.")


def _bam_tep(duong_dan):
    """sha256 của một tệp — để ca test tự cấp `AL_SHA256` cho gói GIẢ nó vừa dựng."""
    import hashlib
    h = hashlib.sha256()
    with open(duong_dan, "rb") as f:
        for khoi in iter(lambda: f.read(65536), b""):
            h.update(khoi)
    return h.hexdigest()


# Chỉ nhận diện canonical `python|python3|py <tệp>.py` KHÔNG CỜ cho hợp đồng hẹp của
# t34. Đây không phải parser shell; năm dạng lọt đã đo được khai ngay trong docstring,
# và không được nối regex ở packet này. Nợ "CI có chạy gate không" thuộc required
# status check được nêu ngay trong t34.
_CHAY_BO_TEST = __import__("re").compile(
    r"""(?<![\w.])(?:python3?|py)\s+["']?\S*lease_publish_test\.py["']?""")


def _goi_actionlint_gia(dich, ver, than):
    """Dựng một gói `.tar.gz` chứa `actionlint` GIẢ. `than=None` ⇒ gói KHÔNG có binary.

    Dùng `tarfile` (thư viện chuẩn) chứ không gọi `tar` ngoài: ca này phải chạy được cả
    trên runner Windows, nơi bộ công cụ nén không giống Linux.
    """
    import io
    import tarfile
    goi = dich / f"actionlint_{ver}_gia.tar.gz"
    with tarfile.open(goi, "w:gz") as t:
        if than is None:
            b = b"day khong phai binary\n"
            ti = tarfile.TarInfo("DOC.txt")
            ti.size, ti.mode = len(b), 0o644
        else:
            b = than.encode("utf-8")
            ti = tarfile.TarInfo("actionlint")
            ti.size, ti.mode = len(b), 0o755
        t.addfile(ti, io.BytesIO(b))
    return goi


def _goi_actionlint_zip_gia(dich, ver):
    """Dựng ZIP chứa binary giả đúng bản, giữ mode executable cho đường `tar` dự phòng."""
    import zipfile
    goi = dich / f"actionlint_{ver}_gia.zip"
    info = zipfile.ZipInfo("actionlint")
    info.create_system = 3
    info.external_attr = 0o100755 << 16
    with zipfile.ZipFile(goi, "w") as z:
        z.writestr(info, f"#!/bin/sh\necho {ver}\n".encode("utf-8"))
    return goi


@ca
def t35_script_cai_actionlint_phai_TU_CHOI_ban_sai():
    """CHẠY THẬT `ops/cai_actionlint.sh` với `actionlint` GIẢ, và đòi nó TỪ CHỐI.

    VÌ SAO VIẾT LẠI (cross-review `#200`, codex, P2-2). Bản trước chỉ kiểm sự ĐỒNG HIỆN
    của vài token trên cùng một dòng `run`. Đo được — dựng lại đúng phản chứng đã ghi thì
    ca CŨ giết nó, nhưng phản chứng ấy chỉ trượt vì nó xoá luôn token `grep` mà phép lọc
    bấu vào; một no-op GIỮ token thì lọt sạch:

        printf '%s\\n' "$AL_VER" | grep -q . || true      -> 35/35 đạt, rc=0

    Dòng ấy KHÔNG hề so bản cài với bản ghim và KHÔNG bao giờ thất bại, mà ca cũ vẫn xanh.
    Đó là lần thứ ba cùng một hình dạng lỗi: *kiểm sự CÓ MẶT của chuỗi rồi tuyên là đã đo
    HÀNH VI*.

    Nên chữa ở TẦNG, không siết mẫu chuỗi lần thứ tư. Hành vi cài + đối chiếu nằm trong
    MỘT script chạy được; ca này CHẠY nó thật với `actionlint` giả và đọc `rc` TRỰC TIẾP
    từ tiến trình. Một script chạy được thì không thể xanh rỗng bằng cách viết lại chữ.

    Có CA DƯƠNG (bản đúng ⇒ nhận). Không có nó thì mọi ca âm đều có thể xanh chỉ vì script
    hỏng toàn tập — "luôn từ chối" cũng qua hết ca âm.
    """
    import os
    import re
    import shutil
    import subprocess
    import tempfile
    import yaml

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(),
         f"không thấy {kich} — hành vi cài `actionlint` phải nằm trong MỘT script chạy "
         f"được thì ca này mới đo được nó; không có script thì không có gì để đo")

    bash = shutil.which("bash")
    # FAIL-CLOSE khi thiếu công cụ, đúng lối `t33`: một cổng tự tắt lúc thiếu công cụ là
    # cổng không tồn tại đúng lúc nó cần nhất. Chữa bằng cách cấp `bash` cho runner.
    bang(bash, "KHÔNG ĐO ĐƯỢC: thiếu `bash` để chạy `ops/cai_actionlint.sh`. Cấp `bash` "
               "cho runner (bước gọi bộ test khai `shell: bash`), đừng bỏ qua ca này.")

    def chay(ver, goi, dich, them=None):
        mt = dict(os.environ)
        mt.update({"AL_VER": ver, "AL_DICH": str(dich), "AL_NEN": "Linux"})
        if goi is not None:
            mt["AL_GOI"] = str(goi)
            # PHẢI cấp băm của chính gói giả này. Không cấp thì script dừng ở cổng băm
            # (rc=9) TRƯỚC khi chạm logic bản-ghim — mọi ca âm bên dưới vẫn "đạt" mà
            # KHÔNG ĐO GÌ, đúng bệnh `t24`. Ca đo cổng băm nằm riêng ở `t37`.
            mt["AL_SHA256"] = _bam_tep(goi)
        mt.pop("GITHUB_PATH", None)     # đừng ghi vào PATH của runner khi đang đo
        if them:
            mt.update(them)
        r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return r.returncode, (r.stdout or "")   # rc lấy TRỰC TIẾP từ tiến trình

    VER = "1.7.7"
    loi = []
    with tempfile.TemporaryDirectory() as tam:
        from pathlib import Path as _P
        tam = _P(tam)

        # ——— CA DƯƠNG: binary khai ĐÚNG bản ghim ⇒ phải NHẬN.
        rc, ra = chay(VER, _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}"),
                      tam / "d-dung")
        if rc != 0:
            loi.append(f"bản ĐÚNG mà script vẫn từ chối (rc={rc}) — ca âm bên dưới sẽ vô "
                       f"nghĩa vì 'luôn từ chối' cũng qua hết:\n{ra.strip()[:400]}")

        # ——— CA DƯƠNG 2: gói có tên KHÔNG CÓ DẤU CHẤM vẫn phải nhận.
        # Phản chứng của cross-review `#203` lượt 2: bản trước dựng tên cục bộ bằng
        # `${TEN_GOI##*.}`, mà khi đường dẫn không có dấu chấm thì phép mở rộng ấy trả lại
        # CẢ ĐƯỜNG DẪN (gồm `/`) ⇒ `cp` chết, rc=5, trên một tar HOÀN TOÀN HỢP LỆ.
        # `AL_GOI` được khai là "đường dẫn tới một gói có sẵn" — nó KHÔNG đòi tên phải có
        # phần mở rộng. Đây cũng là regression do chính lượt vá trước sinh ra.
        _g = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
        _kd = tam / "goikhongduoi"
        _kd.write_bytes(_g.read_bytes())
        rc, ra = chay(VER, _kd, tam / "d-khongduoi")
        if rc != 0:
            loi.append(f"gói tên KHÔNG có dấu chấm mà script từ chối (rc={rc}) — tên tệp "
                       f"không phải hợp đồng, `AL_GOI` chỉ khai là một đường dẫn:"
                       f"\n{ra.strip()[:300]}")

        # ——— CA ÂM: mỗi ca là một kiểu 'đã cài' mà KHÔNG phải 'đã cài ĐÚNG BẢN'.
        AM = [
            ("bản SAI", f"#!/bin/sh\necho 0.0.0"),
            # đúng phản chứng codex lượt 1 (`fd76921`): rc=0, tên đúng, bản bịa
            ("giả kiểu `actionlint fake-0.0.0`", "#!/bin/sh\necho 'actionlint fake-0.0.0'"),
            ("rc=0 mà không in gì", "#!/bin/sh\nexit 0"),
            ("binary không chạy được", "#!/bin/sh\nexit 1"),
            ("gói KHÔNG có binary", None),
        ]
        for k, (ten, than) in enumerate(AM):
            rc, ra = chay(VER, _goi_actionlint_gia(tam, VER, than), tam / f"d-am{k}")
            if rc == 0:
                loi.append(f"`actionlint` giả ({ten}) mà script NHẬN (rc=0) — 'đã cài' "
                           f"không phải 'đã cài ĐÚNG BẢN'; cổng sẽ xanh RỖNG")

        # ——— `AL_VER` không phải X.Y.Z ⇒ từ chối, không âm thầm cài đại một bản nào đó.
        # `1x.2y.3z` … `1.2.3 ` la PHAN CHUNG cua cross-review #203: ban truoc dung glob
        # cua `case` (`[0-9]*.[0-9]*.[0-9]*`), ma trong glob `*` khop CA CHU CAI con `.`
        # la ky tu thuong — nen mot ban ghim khong phai so van qua cong (do duoc: rc=0).
        # Nay la regex day du; moi muc duoi day phai bi tu choi rc=2.
        for ban_xau in ("", "latest", "1.7", "1x.2y.3z", "1.2.3-rc1", "1.2.3/abc",
                        "1.2.3 ", " 1.2.3", "1.2.3.4", "v1.2.3"):
            rc, _ = chay(ban_xau, _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}"),
                         tam / f"d-ver{ban_xau or 'rong'}")
            if rc != 2:
                loi.append(f"`AL_VER={ban_xau!r}` không phải X.Y.Z mà script trả rc={rc} "
                           f"(phải là 2). rc=0 nghĩa là ghim trần — hôm nay xanh, mai đỏ, "
                           f"cây không đổi. rc khác 2 mà khác 0 cũng sai: mã thoát là thứ "
                           f"người gọi dùng để khẳng định LÝ DO từ chối, nêu nhầm mã thì "
                           f"họ khẳng định nhầm chuyện")

        # `mkdir` hỏng từng rơi thẳng qua `set -e` với rc=1 — trùng đúng mã của chính
        # suite khi có ca đỏ. Người gọi vì thế không phân biệt được hạ tầng cài đặt hỏng
        # với cổng nội dung đỏ. Đích là một tệp thường để tái hiện được cả khi chạy root.
        dich_la_tep = tam / "dich-la-tep"
        dich_la_tep.write_text("không phải thư mục\n", encoding="utf-8")
        rc, ra = chay(VER, _goi_actionlint_gia(
            tam, VER, f"#!/bin/sh\necho {VER}"), dich_la_tep)
        if rc != 12 or "khong tao duoc thu muc cai" not in ra:
            loi.append(f"`AL_DICH` là tệp phải trả rc=12 riêng cùng thông điệp phân "
                       f"biệt được, không được trùng rc=1 của suite: rc={rc}, "
                       f"output={ra.strip()[:300]!r}")

    # ——— GIỮ TẦNG: workflow chỉ gọi wrapper; wrapper gọi installer, không cài lại tại chỗ.
    goc = HERE.parent / ".github" / "workflows"
    if goc.is_dir():
        LAY_VE = ("curl", "wget", "choco install", "brew install", "go install")
        GOI_WRAPPER = {
            "bash ops/chay_lease_publish_test.sh",
            'bash "$NEO/ops/chay_lease_publish_test.sh"',
        }
        # PHẠM VI ĐO ĐƯỢC: regex neo `^`; ở nhánh `bash|sh` nó nhận đúng một token
        # lệnh dẫn đầu rồi đòi một token đường dẫn liền mạch (`exec` là nhánh phụ được
        # liệt kê riêng); `\S*` không vượt được khoảng trắng. Bốn dạng đã đo KHÔNG được
        # nhận diện và rơi vào `continue`:
        # `env AL_X=1 bash ops/chay_lease_publish_test.sh`;
        # `bash -c 'bash ops/chay_lease_publish_test.sh'`;
        # `command bash ops/chay_lease_publish_test.sh`; và
        # `bash ${{ github.workspace }}/ops/chay_lease_publish_test.sh` (biểu thức có
        # khoảng trắng). Hai đối chứng bị nhận diện rồi TỪ CHỐI đúng thiết kế là
        # `bash /đường/dẫn/tuyệt/đối/ops/chay_lease_publish_test.sh` và
        # `bash ${{github.workspace}}/ops/chay_lease_publish_test.sh` (không khoảng trắng).
        #
        # NỢ CÓ TÊN `PLAT-X5-nhan-dien-loi-goi-wrapper`: bốn dạng trên vẫn được miễn
        # nghĩa vụ `AL_VER` ở tầng t35. Hậu quả bị chặn ở tầng sau vì
        # `ops/cai_actionlint.sh` vẫn `loi 2` khi thiếu `AL_VER` bất kể cú pháp gọi.
        # Nợ này cùng họ với việc đảo t34 thành danh sách cho phép và thuộc packet #209;
        # không mở regex nhận diện trong lượt vá hẹp này.
        GOI_WRAPPER_THUC_THI = re.compile(
            r"^(?:(?:bash|sh)\s+|exec\s+(?:(?:bash|sh)\s+)?|)"
            r"[\"']?\S*chay_lease_publish_test\.sh[\"']?(?:\s|$)")
        for tep in sorted(goc.glob("*.yml")) + sorted(goc.glob("*.yaml")):
            d = yaml.safe_load(tep.read_text(encoding="utf-8")) or {}
            for job in (d.get("jobs") or {}).values():
                for b in (job.get("steps") or []):
                    than = b.get("run")
                    if not isinstance(than, str):
                        continue
                    ten = f"{tep.name}:{b.get('name') or '(không tên)'}"
                    dong_lenh = _dong_lenh(than)
                    if any("actionlint" in x and any(k in x for k in LAY_VE)
                           for x in dong_lenh):
                        loi.append(f"{ten}: cài `actionlint` TẠI CHỖ. Chép logic ra khỏi "
                                   f"`ops/cai_actionlint.sh` là dựng lại đúng chỗ hỏng — "
                                   f"bản chép sẽ không được ca này chạy thử. Gọi wrapper.")
                    goi_wrapper = [x.strip() for x in dong_lenh
                                   if GOI_WRAPPER_THUC_THI.search(x.strip())]
                    if not goi_wrapper:
                        continue
                    ngoai_danh_sach = [x for x in goi_wrapper if x not in GOI_WRAPPER]
                    if ngoai_danh_sach:
                        loi.append(f"{ten}: có lệnh gọi wrapper ngoài danh sách canonical "
                                   f"{ngoai_danh_sach}. Allowlist này gác nghĩa vụ "
                                   f"`AL_VER`, nên ngoài danh sách phải bị từ chối chứ "
                                   f"không được miễn")
                    ban = str((b.get("env") or {}).get("AL_VER") or "")
                    if not re.fullmatch(r"\d+\.\d+\.\d+", ban):
                        loi.append(f"{ten}: gọi wrapper mà thiếu `AL_VER` "
                                   f"dạng X.Y.Z (được {ban!r})")

    bang(not loi, "cài `actionlint` không cưỡng chế bản ghim:\n  - " + "\n  - ".join(loi))


@ca
def t36_giai_nen_phai_chiu_duoc_duong_dan_mang_DAU_HAI_CHAM():
    """`cai_actionlint.sh` phải giải nén được khi ĐƯỜNG DẪN GÓI mang dấu hai chấm.

    ĐÂY LÀ CA SINH RA TỪ MỘT LƯỢT WINDOWS ĐỎ THẬT, không phải từ suy đoán. Lượt
    `workflow_dispatch` `32368383473` (job `96423003418`, head `d0acd79f`) làm chân
    `gate (windows-latest)` ĐỎ ở bước `lease-publish selftest`:

        tar (child): Cannot connect to C: resolve failed
        cai_actionlint: giai nen tar that bai

    GNU tar đọc đối số của `-f` theo dạng `HOST:PATH` khi có dấu hai chấm đứng TRƯỚC dấu
    gạch chéo đầu tiên. Trên Windows đường dẫn mang ký tự ổ đĩa (`C:...`) nên tar không mở
    tệp — nó đi PHÂN GIẢI TÊN MÁY `C`. Hệ quả: trên Windows script LUÔN trả rc=5, tức
    installer không bao giờ cài được.

    VÌ SAO CA NÀY ĐO ĐƯỢC TRÊN CẢ HAI NỀN, không phải "bỏ qua trên POSIX":

      • Windows: đường dẫn tuyệt đối TỰ NÓ mang ký tự ổ đĩa ⇒ chạy bản thường là đã đo
        đúng ca đó, không cần dựng gì thêm.
      • POSIX: dựng một đường dẫn TƯƠNG ĐỐI mà đoạn đầu chứa dấu hai chấm (`C:sub/goi...`).
        Cùng LUẬT của tar, nên nó tái lập đúng lỗi Windows — đã đo: bản chưa vá trả rc=5
        kèm y nguyên câu `Cannot connect to C:`.

    Không nền nào rơi vào nhánh "không thấy thì bỏ qua" — đó là bệnh `t24` mà kho đã ghi sổ.

    ĐỘT BIẾN ĐÃ CHẠY (đưa dòng giải nén về dạng cũ `tar -xzf "$TEN_GOI" -C "$AL_DICH"`):
    bản vá rc=0, bản đột biến **rc=5** kèm đúng câu lỗi trên ⇒ ca này CÓ RĂNG.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = shutil.which("bash")
    bang(bash, "KHÔNG ĐO ĐƯỢC: thiếu `bash` để chạy `ops/cai_actionlint.sh`")

    VER = "1.7.7"
    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        if os.name == "nt":
            # Windows: KHÔNG dựng được thư mục tên `C:sub` (dấu hai chấm là ký tự cấm),
            # nhưng cũng KHÔNG cần — đường dẫn tuyệt đối ở đây đã mang sẵn ký tự ổ đĩa.
            goi = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
            cwd = None
            mo_ta = f"đường dẫn tuyệt đối Windows (mang ký tự ổ đĩa): {goi}"
        else:
            thu_muc = tam / "C:sub"
            thu_muc.mkdir(parents=True, exist_ok=True)
            goi = _goi_actionlint_gia(thu_muc, VER, f"#!/bin/sh\necho {VER}")
            goi = _P("C:sub") / goi.name        # TƯƠNG ĐỐI: dấu hai chấm TRƯỚC gạch chéo
            cwd = tam
            mo_ta = f"đường dẫn tương đối có dấu hai chấm ở đoạn đầu: {goi}"

        dich = tam / "dich"
        mt = dict(os.environ)
        goi_that = (tam / "C:sub" / goi.name) if cwd else goi
        mt.update({"AL_VER": VER, "AL_DICH": str(dich),
                   "AL_NEN": "Windows" if os.name == "nt" else "Linux",
                   "AL_GOI": str(goi), "AL_SHA256": _bam_tep(goi_that)})
        mt.pop("GITHUB_PATH", None)
        r = subprocess.run([bash, str(kich)], env=mt, cwd=(str(cwd) if cwd else None),
                           timeout=180, stdout=subprocess.PIPE,
                           stderr=subprocess.STDOUT, text=True)
        rc, ra = r.returncode, (r.stdout or "")   # rc TRỰC TIẾP từ tiến trình

    bang(rc == 0,
         f"gói ở {mo_ta} mà script KHÔNG giải nén được (rc={rc}). Đây đúng lỗi đã làm "
         f"`gate (windows-latest)` đỏ ở lượt 32368383473 — tar hiểu `C:` là TÊN MÁY, "
         f"không phải ổ đĩa:\n{ra.strip()[:400]}")


@ca
def t37_goi_tai_ve_phai_qua_DOI_CHIEU_BAM_truoc_khi_chay():
    """Gói `actionlint` phải khớp băm ghim TRƯỚC khi được giải nén và CHẠY.

    VÌ SAO (cross-review `#203`, codex, P2-3). Trước đó thứ duy nhất "xác minh" gói tải từ
    mạng là `actionlint --version` — tức **binary TỰ KHAI**. Một binary bị thay thế chỉ cần
    tự in `1.7.7` là qua. Mà nó chạy trong job có `contents: write` + `issues: write`:

        rg -n 'sha256|checksum|shasum|cosign' ops/cai_actionlint.sh   ->  rc=1 (KHÔNG CÓ)

    BỐN TRẠNG THÁI, mã thoát RIÊNG để người gọi khẳng định được LÝ DO:

        không có băm để đối chiếu   -> rc=8, và DỪNG TRƯỚC KHI TẢI
        thiếu cả sha256sum lẫn shasum -> rc=8 (fail-close, không bỏ qua)
        băm không khớp              -> rc=9
        băm khớp                    -> rc=0

    CA DƯƠNG là bắt buộc: một cổng "luôn từ chối" cũng qua hết ca âm.

    VÌ SAO CA NÀY PHẢI ĐỨNG RIÊNG. `t35`/`t36` **tự cấp** `AL_SHA256` cho gói giả chúng
    dựng — bắt buộc, nếu không chúng dừng ở cổng băm và mọi ca âm của chúng "đạt" mà không
    đo gì. Nghĩa là hai ca ấy **cố ý đi vòng qua** cổng băm, nên cổng ấy phải có ca đo
    riêng — chỗ này.

    GIỚI HẠN, khai thẳng: băm ghim được tính TỪ CHÍNH bản tải về lúc ghim, không phải từ một
    trust root độc lập. Nó chặn DRIFT và THAY THẾ VỀ SAU — đúng mức bảo đảm của
    `pip install X==1.2.3`, KHÔNG hơn.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = shutil.which("bash")
    bang(bash, "KHÔNG ĐO ĐƯỢC: thiếu `bash`")

    VER = "1.7.7"
    loi = []

    def chay(dich, **them):
        mt = dict(os.environ)
        mt.update({"AL_VER": VER, "AL_DICH": str(dich), "AL_NEN": "Linux"})
        mt.pop("AL_SHA256", None)
        mt.update({k: str(v) for k, v in them.items()})
        mt.pop("GITHUB_PATH", None)
        r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        return r.returncode, (r.stdout or "")

    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        goi = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
        bam = _bam_tep(goi)

        # ——— CA DƯƠNG: băm khớp ⇒ NHẬN.
        rc, ra = chay(tam / "d-dung", AL_GOI=goi, AL_SHA256=bam)
        if rc != 0:
            loi.append(f"băm KHỚP mà script vẫn từ chối (rc={rc}) — mọi ca âm dưới đây "
                       f"sẽ vô nghĩa vì 'luôn từ chối' cũng qua hết:\n{ra.strip()[:300]}")

        # ——— băm SAI ⇒ rc=9.
        rc, _ = chay(tam / "d-sai", AL_GOI=goi, AL_SHA256="0" * 64)
        if rc != 9:
            loi.append(f"băm KHÔNG khớp mà script trả rc={rc} (phải 9) — gói lạ vẫn được "
                       f"giải nén và CHẠY")

        # ——— gói lạ, KHÔNG kèm băm ⇒ mốc so là băm CHÍNH THỨC ⇒ rc=9.
        rc, _ = chay(tam / "d-khongbam", AL_GOI=goi)
        if rc != 9:
            loi.append(f"gói lạ không kèm `AL_SHA256` mà script trả rc={rc} (phải 9). "
                       f"Bản cài offline cũng phải là đúng artefact chính thức.")

        # ——— bản KHÔNG có băm ghim ⇒ rc=8, và phải DỪNG TRƯỚC KHI TẢI.
        rc, ra = chay(tam / "d-chuaghim", AL_VER="9.9.9")
        if rc != 8:
            loi.append(f"`AL_VER=9.9.9` chưa ghim băm mà script trả rc={rc} (phải 8)")
        if "tai ve that bai" in ra:
            loi.append("script ĐÃ TẢI rồi mới phát hiện không có băm — phải dừng TRƯỚC: "
                       "tải một thứ không đối chiếu được rất dễ thành 'thôi cài đại'")

    bang(not loi, "cổng đối chiếu băm không cưỡng chế:\n  - " + "\n  - ".join(loi))


@ca
def t38_bam_phai_dung_khi_DUONG_DAN_co_dau_cheo_nguoc():
    r"""Cổng băm phải cho kết quả ĐÚNG khi đường dẫn gói chứa dấu chéo ngược.

    CA NÀY SINH TỪ MỘT LƯỢT WINDOWS ĐỎ THẬT — và đỏ vì CHÍNH BẢN VÁ băm vừa thêm, không
    phải vì gói sai. Lượt `32371632630`, job `96433323614`, bước `cài actionlint`:

        cai_actionlint: bam goi KHONG KHOP:
          mong '7f12f1801bca3d480d67aaf7774f4c2a6359a3ca8eebe382c95c10c9704aa731'
          thuc '\7f12f1801bca3d480d67aaf7774f4c2a6359a3ca8eebe382c95c10c9704aa731'
                ^ đúng MỘT ký tự: một dấu chéo ngược ở đầu

    Băm khớp từng ký tự còn lại. Thứ sai là **định dạng đầu ra của `sha256sum`**: GNU
    coreutils THOÁT cả dòng khi TÊN TỆP chứa dấu chéo ngược (hoặc xuống dòng) — nó thêm
    `\` vào đầu dòng rồi escape tên. Đường dẫn runner Windows là `D:\a\_temp/...` nên
    dính đúng luật ấy, và `cut -d" " -f1` lấy về băm CÓ THÊM một ký tự.

    Cùng họ với những bài học escaping đã ghi trong `CLAUDE.md`: **một lớp mà ta không coi
    là lớp**. Ở đây lớp ấy là định dạng đầu ra của chính công cụ đo.

    Chữa: đọc từ **stdin** (`sha256sum < tệp`) — đầu ra không còn tên tệp thì không còn gì
    để thoát. Không phải "gỡ dấu chéo ở đầu": đó lại là vá theo HÌNH DẠNG, mà tên tệp có
    xuống dòng còn làm đầu ra méo kiểu khác.

    ĐO ĐƯỢC TRÊN LINUX, không cần Windows: dấu chéo ngược là ký tự HỢP LỆ trong tên tệp
    POSIX, nên `sha256sum 'co\cheo.bin'` in ra `\<băm>` y hệt. Ca này dựng đúng tình
    huống đó.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = shutil.which("bash")
    bang(bash, "KHÔNG ĐO ĐƯỢC: thiếu `bash`")

    VER = "1.7.7"
    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        goc = _goi_actionlint_gia(tam, VER, f"#!/bin/sh\necho {VER}")
        if os.name == "nt":
            # KHÔNG bỏ qua trên Windows. Dấu chéo ngược là DẤU PHÂN CÁCH ở đó, nên MỌI
            # đường dẫn tuyệt đối đã mang sẵn nó (`D:\\a\\_temp\\...`) — tức chạy bản
            # thường ở đây LÀ đo đúng ca cần đo, không cần dựng tên tệp dị.
            #
            # Bản đầu của ca này viết `bang(True, ""); return` cho Windows. SAI, và sai
            # đúng kiểu kho đã ghi sổ: harness này KHÔNG có cơ chế bỏ qua — một ca
            # `return` sớm vẫn được đếm là ĐẠT. Nghĩa là trên chính nền sinh ra lỗi, ca
            # canh nó lại không đo gì mà vẫn xanh. Đúng bệnh `t24`.
            goi = goc
        else:
            # POSIX: dấu chéo ngược là ký tự HỢP LỆ trong TÊN tệp, nên dựng thẳng một tên
            # có nó — cùng luật thoát của coreutils, tái lập đúng lỗi Windows.
            goi = tam / "co\\cheo.tar.gz"
            goi.write_bytes(goc.read_bytes())

        mt = dict(os.environ)
        mt.update({"AL_VER": VER, "AL_DICH": str(tam / "dich"), "AL_NEN": "Linux",
                   "AL_GOI": str(goi), "AL_SHA256": _bam_tep(goi)})
        mt.pop("GITHUB_PATH", None)
        r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                           stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
        rc, ra = r.returncode, (r.stdout or "")

    bang(rc == 0,
         f"[nền={os.name}] gói ĐÚNG ở đường dẫn có dấu chéo ngược mà cổng băm từ chối "
         f"(rc={rc}). `sha256sum`"
         f" thoát cả dòng khi tên tệp chứa `\\` — đọc từ stdin thì đầu ra không có tên tệp. "
         f"Đây đúng lỗi đã làm `gate (windows-latest)` đỏ ở lượt 32371632630:\n"
         f"{ra.strip()[:400]}")


@ca
def t39_loai_archive_phai_do_NOI_DUNG_khong_doan_tu_ten():
    """ZIP hợp lệ phải chạy được khi tên không đuôi hoặc dùng `.ZIP` viết hoa.

    Finding vòng 3 đo cả hai ca đều rc=5 vì script cũ dùng `*.zip`, rồi mặc định mọi tên
    còn lại là tar.gz. Hợp đồng `AL_GOI` chỉ nói "đường dẫn tới một gói"; tên tệp không
    phải trường loại. Ca này dùng CÙNG byte ZIP dưới hai tên để buộc phân loại theo magic
    bytes. Có ca dương thật: binary sau giải nén phải chạy và khai đúng bản.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    kich = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(kich.is_file(), f"không thấy {kich}")
    bash = shutil.which("bash")
    bang(bash, "KHÔNG ĐO ĐƯỢC: thiếu `bash`")

    VER = "1.7.7"
    loi = []
    with tempfile.TemporaryDirectory() as tam:
        tam = _P(tam)
        goc = _goi_actionlint_zip_gia(tam, VER)
        for k, ten in enumerate(("goi-khong-duoi", "goi.ZIP")):
            goi = tam / ten
            goi.write_bytes(goc.read_bytes())
            mt = dict(os.environ)
            mt.update({"AL_VER": VER, "AL_DICH": str(tam / f"dich-{k}"),
                       "AL_NEN": "Linux", "AL_GOI": str(goi),
                       "AL_SHA256": _bam_tep(goi)})
            mt.pop("GITHUB_PATH", None)
            r = subprocess.run([bash, str(kich)], env=mt, timeout=180,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            rc, ra = r.returncode, (r.stdout or "")  # rc TRỰC TIẾP từ tiến trình
            if rc != 0:
                loi.append(f"ZIP tên {ten!r} bị từ chối rc={rc}: {ra.strip()[:300]}")
    bang(not loi, "loại archive vẫn bị suy từ suffix:\n  - " + "\n  - ".join(loi))


@ca
def t40_wrapper_phai_CAI_truoc_CHAY_va_giu_rc_cua_bo_test():
    """Chạy wrapper thật trong cây tạm và đo trạng thái, không mô phỏng kịch bản.

    Cây tạm chứa chính wrapper + installer, một gói actionlint có executable chạy thật,
    và một selftest nhỏ tự tìm/call binary trên PATH rồi ghi marker. Ba hậu điều có răng:

    * gói đúng: test thấy binary đúng bản và marker xuất hiện;
    * installer sai bản: rc=7 và marker KHÔNG xuất hiện — test không chạy trước/cạnh lỗi;
    * test chủ động rc=23: wrapper trả đúng 23 — không pipeline nuốt mã thoát.

    POSIX dùng shell stub trạng thái; Windows đóng gói lại chính `actionlint.exe` PE mà
    wrapper ngoài vừa cài — không bắt Windows chạy một shell script không đuôi rồi gọi đó
    là binary Windows. Cả hai nền đều đòi executable được tìm thấy nằm TRONG `AL_DICH`,
    nên xoá installer hoặc quên cập nhật PATH vẫn chết kể cả mồi tình cờ cùng phiên bản.

    PATH mồi được ghép BÊN TRONG Bash bằng `:`, không dùng `os.pathsep` của Python host
    cho một giá trị mà Bash sẽ tiêu thụ. Mỗi nhánh trên đều chạy đủ ba hậu điều; không có
    nhánh return/skip được harness đếm thành đạt.
    """
    import os
    import shutil
    import subprocess
    import tempfile
    from pathlib import Path as _P

    bash = shutil.which("bash")
    bang(bash, "KHÔNG ĐO ĐƯỢC: thiếu `bash`")
    wrapper = HERE.parent / "ops" / "chay_lease_publish_test.sh"
    installer = HERE.parent / "ops" / "cai_actionlint.sh"
    bang(wrapper.is_file(), f"không thấy {wrapper}")
    bang(installer.is_file(), f"không thấy {installer}")

    VER = "1.7.7"
    with tempfile.TemporaryDirectory() as tam:
        goc = _P(tam)
        ops = goc / "ops"
        ops.mkdir()
        shutil.copy2(wrapper, ops / wrapper.name)
        shutil.copy2(installer, ops / installer.name)
        (ops / "lease_publish_test.py").write_text(
            """import os, pathlib, shutil, subprocess, sys

def sai(ly_do):
    print(f"T40_STUB_SAI: {ly_do}", file=sys.stderr)
    raise SystemExit(32)

duong = shutil.which("actionlint")
if not duong:
    sai("shutil.which khong tim thay actionlint")
dich = pathlib.Path(os.environ["AL_DICH"]).resolve()
binary = pathlib.Path(duong).resolve()
try:
    binary.relative_to(dich)
except ValueError:
    sai(f"PATH tro ra ngoai AL_DICH: {binary} (dich {dich})")
p = subprocess.run([duong, "--version"], capture_output=True, text=True)
lines = p.stdout.strip().splitlines()
if p.returncode != 0 or not lines or lines[0] != os.environ["AL_VER"]:
    sai(f"version rc={p.returncode}, stdout={p.stdout!r}, stderr={p.stderr!r}")
pathlib.Path(os.environ["WRAPPER_MARKER"]).write_text("da-chay", encoding="utf-8")
print("WRAPPER_SELFTEST_OK")
raise SystemExit(int(os.environ.get("WRAPPER_TEST_RC", "0")))
""", encoding="utf-8")

        # Đồ mồi mô phỏng TRẠNG THÁI "PATH đã có actionlint ở nơi khác", không trả lời
        # theo lượt. Stub còn đòi đường tìm được thuộc AL_DICH, nên mồi cùng phiên bản
        # cũng không thể diễn kịch để làm ca xanh.
        path_ban_dau = goc / "path-ban-dau"
        path_ban_dau.mkdir()
        if os.name == "nt":
            # Nhánh Windows đo executable Windows THẬT. Wrapper ngoài phải vừa cài nó
            # để t33 chạy được; thiếu/không đúng bản là ĐỎ, không return sớm.
            actionlint_ngoai = shutil.which("actionlint")
            bang(actionlint_ngoai and actionlint_ngoai.lower().endswith(".exe"),
                 "[Windows] KHÔNG ĐO ĐƯỢC: PATH không có `actionlint.exe` thật")
            do_ban = subprocess.run([actionlint_ngoai, "--version"],
                                    capture_output=True, text=True)
            dong = (do_ban.stdout or "").strip().splitlines()
            bang(do_ban.returncode == 0 and dong and dong[0] == VER,
                 f"[Windows] actionlint ngoài không đúng {VER}: rc={do_ban.returncode}, "
                 f"stdout={do_ban.stdout!r}, stderr={do_ban.stderr!r}")

            # Gói dương chứa đúng loại file của archive chính thức: `actionlint.exe`.
            # Copy PE thật thay vì đổi đuôi một shell script rồi giả định Windows chạy nó.
            import zipfile
            goi_dung = goc / "actionlint-windows-dung.zip"
            with zipfile.ZipFile(goi_dung, "w", zipfile.ZIP_DEFLATED) as z:
                z.write(actionlint_ngoai, "actionlint.exe")
            shutil.copy2(actionlint_ngoai, path_ban_dau / "actionlint.exe")
            nen = "Windows"
        else:
            moi = path_ban_dau / "actionlint"
            moi.write_text("#!/bin/sh\necho 0.0.0\n", encoding="utf-8")
            moi.chmod(0o755)
            thu_muc_dung = goc / "goi-dung"
            thu_muc_dung.mkdir()
            goi_dung = _goi_actionlint_gia(
                thu_muc_dung, VER, f"#!/bin/sh\necho {VER}")
            nen = "Linux"

        mt_goc = dict(os.environ, AL_VER=VER, AL_NEN=nen)
        mt_goc.pop("GITHUB_PATH", None)

        # `subprocess` đầu tiên cần PATH native để tìm Git Bash; chỉ sau khi đã ở TRONG
        # Bash mới ghép mồi bằng dấu `:`. `exec` giữ rc wrapper làm rc trực tiếp của r.
        lenh_wrapper = r"""set -euo pipefail
moi="$1"
wrapper="$2"
bash_that="$3"
if command -v cygpath >/dev/null 2>&1; then
  moi="$(cygpath -u "$moi")"
  wrapper="$(cygpath -u "$wrapper")"
  bash_that="$(cygpath -u "$bash_that")"
fi
export PATH="$moi:$PATH"
exec "$bash_that" "$wrapper"
"""

        def chay(goi, dich, marker, rc_test=None, ver=VER):
            mt = dict(mt_goc, AL_GOI=str(goi), AL_DICH=str(dich),
                      AL_SHA256=_bam_tep(goi), WRAPPER_MARKER=str(marker), AL_VER=ver)
            if rc_test is not None:
                mt["WRAPPER_TEST_RC"] = str(rc_test)
            r = subprocess.run(
                [bash, "-c", lenh_wrapper, "t40", str(path_ban_dau),
                 str(ops / wrapper.name), bash],
                cwd=goc, env=mt, timeout=180, stdout=subprocess.PIPE,
                stderr=subprocess.STDOUT, text=True)
            return r.returncode, (r.stdout or "")

        marker_dung = goc / "marker-dung"
        rc, ra = chay(goi_dung, goc / "dich-dung", marker_dung)
        bang(rc == 0 and marker_dung.is_file()
             and marker_dung.read_text(encoding="utf-8") == "da-chay"
             and "WRAPPER_SELFTEST_OK" in ra,
             f"wrapper không cài rồi chạy test thật: rc={rc}, marker={marker_dung.exists()}:\n"
             f"{ra.strip()[:400]}")

        if os.name == "nt":
            # Cùng PE khai 1.7.7 nhưng hợp đồng đòi 0.0.0: trạng thái sai, không phải
            # mock trả lời theo số lượt. Installer phải tự đo mismatch và trả 7.
            goi_sai, ver_sai = goi_dung, "0.0.0"
        else:
            thu_muc_sai = goc / "goi-sai"
            thu_muc_sai.mkdir()
            goi_sai = _goi_actionlint_gia(
                thu_muc_sai, VER, "#!/bin/sh\necho 0.0.0")
            ver_sai = VER
        marker_sai = goc / "marker-sai"
        rc, ra = chay(goi_sai, goc / "dich-sai", marker_sai, ver=ver_sai)
        bang(rc == 7 and not marker_sai.exists(),
             f"installer sai phải dừng TRƯỚC selftest: rc={rc}, "
             f"marker={marker_sai.exists()}:\n{ra.strip()[:400]}")

        marker_rc = goc / "marker-rc"
        rc, ra = chay(goi_dung, goc / "dich-rc", marker_rc, rc_test=23)
        bang(rc == 23 and marker_rc.exists(),
             f"wrapper nuốt rc selftest: chờ 23, được {rc}, marker={marker_rc.exists()}:\n"
             f"{ra.strip()[:400]}")
# `t42` ĐÃ BỊ GỠ ở lượt vá thứ hai — có chủ đích, không phải quên. Nó khẳng định "docstring
# của `t34` có chứa chuỗi X", tức MỘT LỜI KHAI VỀ MỘT LỜI KHAI. Ba lượt liên tiếp cho cùng một
# hình dạng lỗi: cross-review 1 tìm được đột biến nới regex mà nó không bắt; bản vá cho nó lại
# đẻ ra hai docstring TỰ MÂU THUẪN với chính mã vừa viết cộng một con số chết ngay trong commit
# sinh ra nó; cross-review 2 lại tìm được đột biến siết regex mà nó vẫn không bắt.
#
# `CLAUDE.md` nói thẳng về đúng tình huống này: "cùng một hình dạng lặp ba lần trở lên thì câu
# hỏi đúng là CÓ NÊN LÀM VIỆC NÀY KHÔNG, không phải VÁ THẾ NÀO". Người giữ kho quyết bỏ.
#
# NỢ CÒN LẠI, khai thẳng chứ không giả vờ đã xong: mục tiêu gốc — canh cho lời khai phạm vi
# của `t34` không trôi — VẪN CHƯA CÓ CỔNG NÀO. Xem `ops/NO_KY_THUAT.md` §11.
#
# `t42` bên dưới được GIỮ vì nó khác loại: nó đo QUAN HỆ GIỮA HAI TỆP, tức một SỰ KIỆN, không
# phải một câu chữ ai đó gõ vào docstring.


# Marker `NỢ CÓ TÊN` trong workflow, và tiêu đề mục trong sổ nợ. Cố ý HAI mẫu riêng và cả hai
# đều bó vào ĐÚNG hình dạng đang dùng: marker chỉ nhận khi đứng trong một dòng CHÚ THÍCH, mục
# chỉ nhận khi là TIÊU ĐỀ `## <số>.`. Không bó thì một câu văn xuôi có chữ "NỢ CÓ TÊN" — như
# chính các câu giải thích trong hai tệp ấy — sẽ bị đếm nhầm, và cổng lại thành cổng nói dối.
# Marker phải đứng NGAY SAU dấu chú thích — `^\s*#\s*NỢ CÓ TÊN`, không cho chữ tuỳ ý chen
# vào giữa. Bản trước dùng `^\s*#.*NỢ CÓ TÊN` nên một CÂU VĂN XUÔI có nhắc cụm ấy cũng bị nhận
# làm marker; cross-review 2 đo được: chèn một dòng giải thích vào `ci.yml` là `t43` ĐỎ oan.
# Một cổng báo động giả là cổng sẽ bị tắt, rồi cả ca chết theo.
_MARKER_NO = __import__("re").compile(r"^\s*#\s*NỢ CÓ TÊN\s*:?\s*`([^`]+)`")
_MUC_SO_NO = __import__("re").compile(r"^##\s*\d+\.\s*`([^`]+)`")
# BACKLINK: mục sổ nợ TỰ KHAI nó là nhà của một marker trong mã. Chỉ mục có dòng này mới bị
# đòi hai chiều — §1–§8 không có backlink nên không báo động giả, đúng lý do đã hạ `t43` xuống
# một chiều ở lượt trước; nay giữ được cả hai chiều mà KHÔNG ép đối xứng lên toàn sổ.
_BACKLINK_NO = __import__("re").compile(r"^\*\*marker:\*\*\s*`([^`]+)`\s+trong\s+`([^`]+)`")


@ca
def t42_marker_NO_CO_TEN_va_muc_so_no_phai_khop_HAI_CHIEU():
    """Nợ được ĐẶT TÊN trong mã phải có nhà trong sổ, và mục đã khai backlink phải còn marker.

    VÌ SAO CÓ CA NÀY — cross-review lượt 1 (codex, P2): tiêu chí `2 = 2` mà packet tự đặt ra
    chỉ là một ẢNH CHỤP. Thêm marker thứ ba vào `ci.yml` mà không thêm mục ⇒ mọi cổng vẫn
    xanh. Một nợ mới sinh ra là một nợ KHÔNG AI ĐỌC.

    BA LỖ CỦA BẢN ĐẦU, cross-review lượt 2 đo được, nay đã vá — ghi cả ba vì mỗi cái là một
    kiểu thua khác nhau:

    1. **Một chiều làm mất tín hiệu khi marker BỊ GỠ.** Gỡ `PLAT-X5-required-status-check`
       khỏi `ci.yml` mà giữ nguyên §9 ⇒ `marker − sổ = ∅`, suite `43/43`, KHÔNG AI BẮT. Chiều
       nghịch không thể ép lên toàn sổ (§1–§8 là nợ thật, không có marker), nên lời giải là
       **backlink**: mục nào TỰ KHAI mình là nhà của một marker thì mới bị đòi hai chiều.
    2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
       dòng giải thích cũng thành marker. Nay neo ngay sau `#`.
    3. **`set` xoá dấu vết trùng.** Tên ca hứa "ĐÚNG MỘT mục" nhưng `set` biến hai tiêu đề
       cùng ID thành một ⇒ chỉ kiểm được "ít nhất một". Nay đếm bằng `Counter`.

    PHẠM VI, khai thẳng: ca này chỉ đo `.github/workflows/ci.yml` ↔ `ops/NO_KY_THUAT.md`. Nợ
    đặt tên ở tệp khác KHÔNG được canh. Đây là tập đã ĐO, không phải lời hứa về mọi nơi.

    ĐỘT BIẾN LÀM CA NÀY ĐỎ: thêm marker không có nhà · GỠ một marker mà mục vẫn khai backlink
    · thêm mục thứ hai trùng ID. VÀ MỘT CA ÂM PHẢI XANH: chèn câu văn xuôi có cụm `NỢ CÓ TÊN`.
    """
    import collections
    goc = HERE.parent
    wf = goc / ".github" / "workflows" / "ci.yml"
    so = goc / "ops" / "NO_KY_THUAT.md"
    if not wf.is_file() or not so.is_file():
        bang(not (goc / ".git").exists(),
             f"kho thật mà thiếu {wf} hoặc {so} — ca này sẽ xanh mà không đo gì")
        return
    trong_ma = {m.group(1) for d in wf.read_text(encoding="utf-8").splitlines()
                if (m := _MARKER_NO.match(d))}
    dong_so = so.read_text(encoding="utf-8").splitlines()
    dem_muc = collections.Counter(m.group(1) for d in dong_so if (m := _MUC_SO_NO.match(d)))
    backlink = {m.group(1): m.group(2) for d in dong_so if (m := _BACKLINK_NO.match(d))}

    trung = sorted(k for k, n in dem_muc.items() if n > 1)
    bang(not trung,
         f"sổ nợ có mục TRÙNG ID: {trung}. Hai mục cùng tên là hai bản ghi cùng tranh làm nhà "
         f"của một khoản nợ — người đọc không biết bản nào có hiệu lực.")

    thieu_nha = sorted(trong_ma - set(dem_muc))
    bang(not thieu_nha,
         f"nợ ĐƯỢC ĐẶT TÊN trong `ci.yml` mà KHÔNG có mục trong `ops/NO_KY_THUAT.md`: "
         f"{thieu_nha}. Nợ có tên mà không có nhà là nợ KHÔNG AI ĐỌC — thêm mục, đừng gỡ marker.")

    mat_marker = sorted(k for k in backlink if k not in trong_ma)
    bang(not mat_marker,
         f"mục sổ nợ KHAI backlink tới marker mà marker ấy KHÔNG CÒN trong `ci.yml`: "
         f"{mat_marker}. Hoặc nợ đã trả mà mục chưa đóng, hoặc marker bị gỡ nhầm. Đừng làm ca "
         f"này im bằng cách xoá dòng backlink — đó là xoá đúng thứ đang canh.")


@ca
def t43_PR_phai_CHAN_va_neu_pull_requests():
    ex, _ = _goi_lop_gh(GhGia({55: "pr"}), "kiem_github", lease_mau(),
                        env_them=ENV_GITHUB, bo_qua=("_kiem_comment_da_co",))
    bang(ex and ex.ma == RC_NOI_DUNG and "pull-requests" in ex.thong_diep,
         f"PR không bị chặn đúng lý do: {ex}")


@ca
def t44_loi_do_loai_phai_CHAN_khong_dang():
    gh = GhGia({55: "loi"})
    ex, _ = _goi_lop_gh(gh, "kiem_github", lease_mau(), env_them=ENV_GITHUB,
                        bo_qua=("_kiem_comment_da_co",))
    bang(ex and ex.ma == RC_NOI_DUNG and "KHÔNG ĐO ĐƯỢC" in ex.thong_diep
         and "nguyên nhân có thể" in ex.thong_diep
         and "phỏng đoán, không phải phép đo" in ex.thong_diep,
         f"fail-open hoặc khai quá phép đo: {ex}")


@ca
def t45_ISSUE_phai_QUA_lop_do_loai():
    ex, _ = _goi_lop_gh(GhGia(), "kiem_github", lease_mau(), env_them=ENV_GITHUB)
    bang(ex is None, f"chặn oan Issue: {ex}")


@ca
def t46_comment_da_co_thi_BO_QUA_xuyen_nhanh():
    lease, gh = lease_mau(lease_id="lease-lap"), GhGia()
    ex, mod = _goi_lop_gh(gh, "kiem_github", lease, env_them=ENV_GITHUB,
                          bo_qua=("_kiem_loai_so_hieu",))
    bang(ex is None, f"lượt đầu không đăng được: {ex}")
    gh.dang(55, mod.dung_than(lease, "ops/leases/l.yaml"))
    ex, _ = _goi_lop_gh(gh, "kiem_github", lease, env_them=ENV_GITHUB,
                        bo_qua=("_kiem_loai_so_hieu",))
    posts = [x for x in gh.calls if x[0] == "POST"]
    bang(ex and ex.ma == RC_DA_DANG and len(posts) == 1 and len(gh.comments[55]) == 1,
         f"lượt hai không thấy comment lượt một: posts={posts}, {ex}")


@ca
def t47_dau_lease_KHAC_khong_duoc_chan():
    comments = {55: [{"id": 1, "body": "**Lease `lease-10`**",
                      "user": {"login": "github-actions[bot]"}}]}
    ex, _ = _goi_lop_gh(GhGia(comments=comments), "_kiem_comment_da_co", "o/r",
                        lease_mau(lease_id="lease-1"), env_them=ENV_GITHUB)
    bang(ex is None, f"khớp substring lỏng đã chặn lease khác: {ex}")


@ca
def t48_loi_doc_comment_phai_CHAN_khong_dang():
    gh = GhGia(loi_comment={55})
    ex, _ = _goi_lop_gh(gh, "_kiem_comment_da_co", "o/r", lease_mau(),
                        env_them=ENV_GITHUB)
    bang(ex and ex.ma == RC_NOI_DUNG and "KHÔNG ĐO ĐƯỢC" in ex.thong_diep
         and not any(x[0] == "POST" for x in gh.calls), f"fail-open: {ex}")


@ca
def t49_env_va_lease_khong_duoc_chon_moi_noi():
    import os, shutil
    with San() as s:
        nhat_ky = s / "calls"
        gh = s / ("api" if os.name == "nt" else "gh")
        if os.name == "nt":
            shutil.copy2(sys.executable, s / "gh.exe")
        gh.write_text(
            ("" if os.name == "nt" else f"#!{Path(sys.executable).resolve()}\n") +
            "import json,os,pathlib,sys\n"
            "p=pathlib.Path(os.environ['GH_GIA_LOG']); "
            "p.write_text((p.read_text() if p.exists() else '')+' '.join(sys.argv[1:])+'\\n')\n"
            "ep=next(x for x in sys.argv if x.startswith('repos/'))\n"
            "print('[[]]' if ep.endswith('/comments') else "
            "json.dumps({'html_url':'https://github.com/o/r/issues/55'}))\n",
            encoding="utf-8")
        if os.name != "nt":
            gh.chmod(0o755)
        p = viet(s, lease_mau(gh_path="/khong/duoc/chay", api_path="/cung-khong"))
        base = dict(os.environ, PATH=str(s) + os.pathsep + os.environ.get("PATH", ""),
                    GITHUB_REPOSITORY="o/r", GITHUB_ACTOR="ducthangho",
                    GH_GIA_LOG=str(nhat_ky))
        for ten in ("GH_PATH", "GITHUB_CLI_PATH", "API_PATH", "CUSTOM_API", "TOOL_PATH"):
            base.pop(ten, None)
        rc1, o1, e1 = chay("kiem-github", p, env=base, cwd=s)
        goi1 = _doc_do_gia(nhat_ky, rc1, o1, e1, "nhật ký `gh` giả").splitlines()
        nhat_ky.unlink()
        day = dict(base, GH_PATH="/khong/duoc/chay", GITHUB_CLI_PATH="/sai",
                   API_PATH="/sai", CUSTOM_API="https://sai.invalid", TOOL_PATH="/sai")
        rc2, o2, e2 = chay("kiem-github", p, env=day, cwd=s)
        goi2 = _doc_do_gia(nhat_ky, rc2, o2, e2, "nhật ký `gh` giả").splitlines()
        bang(rc1 == rc2 == RC_OK and goi1 == goi2 and bool(goi1),
             f"biến/lease đổi mối nối: rc={rc1}/{rc2}, calls={goi1}/{goi2}, err={e1}{e2}")


@ca
def t50_ngoai_Actions_phai_KHAI_hai_lop_vang():
    with San() as s:
        import os
        moi = dict(os.environ)
        moi.pop("GITHUB_ACTIONS", None)
        rc, o, e = chay("check", viet(s, lease_mau()), env=moi)
        bang(rc == RC_OK and "KHÔNG CHẠY" in o and "ISSUE/PR" in o
             and "comment" in o and "kiem-github" in o,
             f"không khai lớp vắng: rc={rc}, out={o!r}, err={e!r}")


def _chay_buoc_dang(check_hong="", post_hong="", kiem_github_hong="",
                    check_rc9="", kiem_github_rc9="", guard_hong="") -> dict:
    import json
    import os
    if guard_hong == "check":
        check_hong = "giua"
    if guard_hong == "kiem-github":
        kiem_github_hong = "giua"
    if _ly_do_bo_qua_workflow(WORKFLOW_DANG, "dang"):
        raise BoQuaNen(WORKFLOW_DANG, "dang")
    than = _buoc_workflow("đăng")["run"]
    with tempfile.TemporaryDirectory() as t:
        goc, neo = Path(t), Path(t) / "neo"
        (goc / "ops" / "leases").mkdir(parents=True)
        (neo / "ops").mkdir(parents=True)
        (neo / "ops" / "lease_publish.py").write_text(
            """import pathlib,sys,yaml
p=pathlib.Path(sys.argv[2]); d=yaml.safe_load(p.read_text(encoding='utf-8')); cmd=sys.argv[1]
with pathlib.Path(os.environ['LENH_GIA_LOG']).open('a',encoding='utf-8') as f: print(*sys.argv[1:],file=f)
if cmd=='kiem-github': raise SystemExit(9 if d['lease_id']==os.environ.get('KIEM_GITHUB_RC9') else 8 if d['lease_id']==os.environ.get('KIEM_GITHUB_HONG') else 0)
if cmd=='check': raise SystemExit(9 if d['lease_id']==os.environ.get('CHECK_RC9') else 8 if d['lease_id']==os.environ.get('CHECK_HONG') else 0)
if cmd=='body' and d['lease_id']=='giua' and os.environ.get('GUARD_HONG')=='body': raise SystemExit(8)
if cmd=='body' and d['lease_id']=='giua' and os.environ.get('GUARD_HONG')=='payload': sys.stdout.buffer.write(bytes([255])); raise SystemExit(0)
if cmd=='body': print(f\"**Lease `{d['lease_id']}`**\")
if cmd=='mark' and d['lease_id']=='giua' and os.environ.get('GUARD_HONG')=='mark': raise SystemExit(8)
if cmd=='mark':
 p.write_text(p.read_text(encoding='utf-8')+'posted_comment_id: '+sys.argv[4]+'\\n',encoding='utf-8')
 if os.environ.get('GUARD_HONG')=='github_env':
  e=pathlib.Path(os.environ['GITHUB_ENV'])
  if d['lease_id']=='giua': e.unlink(missing_ok=True); e.mkdir()
  elif d['lease_id']=='cuoi': e.rmdir(); e.write_text('DA_DOI=1\\n')
""".replace("import pathlib", "import os,pathlib"), encoding="utf-8")
        (neo / "ops" / "gh_gia.py").write_text(
            """import json,os,pathlib,re,sys
a=sys.argv[1:]; p=pathlib.Path(os.environ['GH_GIA_STATE']); d=json.loads(p.read_text())
raw=pathlib.Path(a[a.index('--input')+1]).read_text(); body='**Lease `giua`**' if os.environ.get('GUARD_HONG')=='payload' and not raw else json.loads(raw)['body']
m=re.search(r'\\*\\*Lease `([^`]+)`\\*\\*',body); lease='giua' if os.environ.get('GUARD_HONG')=='body' and m is None else m.group(1)
ge=pathlib.Path(os.environ['GITHUB_ENV']); snap=ge.read_text() if ge.is_file() else ''
d['snapshots'].append([lease,snap]); p.write_text(json.dumps(d))
if lease==os.environ.get('POST_HONG'): print('POST hong',file=sys.stderr); raise SystemExit(42)
ds=d['comments']; ds.append({'id':9000+len(ds),'body':body,'lease':lease}); p.write_text(json.dumps(d))
if lease=='giua' and os.environ.get('GUARD_HONG')=='post_rc': print(ds[-1]['id']); raise SystemExit(1)
print('khong-phai-so' if lease=='giua' and os.environ.get('GUARD_HONG')=='case_id' else ds[-1]['id'])
""", encoding="utf-8")
        for ten in ("dau", "giua", "cuoi"):
            lease = lease_mau(lease_id=ten)
            if guard_hong == "packet_issue" and ten == "giua":
                lease.pop("packet_issue")
            viet(goc / "ops" / "leases", lease, ten=f"{ten}.yaml")
        (goc / "ds.txt").write_text(
            "".join(f"ops/leases/{x}.yaml\n" for x in ("dau", "giua", "cuoi")),
            encoding="utf-8")
        state, ghe, log = goc / "state.json", goc / "github_env", goc / "argv.log"
        state.write_text('{"comments":[],"snapshots":[]}', encoding="utf-8")
        py = Path(sys.executable).resolve().as_posix()
        than = than.replace("python3 ", f"'{py}' ").replace(
            "gh api ", f"'{py}' \"$NEO/ops/gh_gia.py\" api ").replace(
            'if [ "$BI_CHAN" != "0" ]; then exit 1; fi',
            'echo "BI_CHAN=$BI_CHAN"\nif [ "$BI_CHAN" != "0" ]; then exit 1; fi')
        mt = dict(os.environ, NEO=str(neo), REPO="o/r", GITHUB_ENV=str(ghe),
                  GH_GIA_STATE=str(state), CHECK_HONG=check_hong, POST_HONG=post_hong,
                  KIEM_GITHUB_HONG=kiem_github_hong, CHECK_RC9=check_rc9,
                  KIEM_GITHUB_RC9=kiem_github_rc9, GUARD_HONG=guard_hong,
                  LENH_GIA_LOG=str(log))
        p = subprocess.run([_bash_posix(), "-c", than], cwd=goc, env=mt,
                           capture_output=True, text=True)
        d = json.loads(state.read_text(encoding="utf-8"))
        return {"rc": p.returncode, "bodies": "\n".join(x["body"] for x in d["comments"]),
                "posts": [x["lease"] for x in d["comments"]],
                "marks": {x: "posted_comment_id:" in
                          (goc / "ops" / "leases" / f"{x}.yaml").read_text(encoding="utf-8")
                          for x in ("dau", "giua", "cuoi")},
                "snapshots": dict(d["snapshots"]),
                "env": _doc_do_gia(ghe, p.returncode, p.stdout, p.stderr, "GITHUB_ENV giả"),
                "calls": [x.split()[:2] for x in _doc_do_gia(
                    log, p.returncode, p.stdout, p.stderr, "nhật ký argv giả").splitlines()],
                "out": p.stdout + p.stderr}


@ca
def t51_lease_giua_bi_chan_van_xu_ly_het_nhung_luot_DO():
    kq = _chay_buoc_dang(check_hong="giua")
    bang(kq["rc"] != 0 and "`dau`" in kq["bodies"] and "`cuoi`" in kq["bodies"]
         and "`giua`" not in kq["bodies"] and "DA_DOI=1" in kq["env"],
         f"không cô lập lỗi check: {kq}")


@ca
def t52_buoc_ghi_nguoc_phai_chay_sau_buoc_dang_DO():
    kq = _chay_buoc_dang(post_hong="giua")
    dieu_kien = str(_buoc_workflow("ghi ngược comment id").get("if") or "")
    bang(kq["rc"] != 0 and "`dau`" in kq["bodies"] and "`cuoi`" in kq["bodies"]
         and "`giua`" not in kq["bodies"] and "DA_DOI=1" in kq["env"]
         and "DA_DOI=1" in kq["snapshots"].get("giua", "")
         and "always()" in dieu_kien and "env.DA_DOI == '1'" in dieu_kien,
         f"POST giữa không được cô lập/ghi ngay DA_DOI: if={dieu_kien!r}, {kq}")


@ca
def t53_check_trong_Actions_khong_gh_van_QUA():
    import os
    with San() as s:
        rong = s / "bin-rong"
        rong.mkdir()
        mt = dict(os.environ, GITHUB_ACTIONS="true", GITHUB_REPOSITORY="o/r",
                  GITHUB_ACTOR="ducthangho", PATH=str(rong))
        rc, o, e = chay("check", viet(s, lease_mau()), env=mt)
        bang(rc == RC_OK and "KHÔNG CHẠY" in o,
             f"check gọi mạng trong Actions không gh: rc={rc}, out={o!r}, err={e!r}")


@ca
def t54_comment_nguoi_ngoai_khong_duoc_bit_lease():
    comments = {55: [{"id": 1, "body": "**Lease `lease-that`**",
                      "user": {"login": "nguoi-la"}}]}
    ex, _ = _goi_lop_gh(GhGia(comments=comments), "_kiem_comment_da_co", "o/r",
                        lease_mau(lease_id="lease-that"), env_them=ENV_GITHUB)
    bang(ex is None, f"comment người ngoài bị tính là đã đăng: {ex}")


@ca
def t55a_thieu_user_login_phai_CHAN():
    thieu = {55: [{"id": 1, "body": "không liên quan"}]}
    ex, _ = _goi_lop_gh(GhGia(comments=thieu), "_kiem_comment_da_co", "o/r",
                        lease_mau(), env_them=ENV_GITHUB)
    bang(ex and ex.ma == RC_NOI_DUNG, f"thiếu user.login không bị chặn: {ex}")


@ca
def t55b_dau_khong_o_dau_than_thi_khong_tinh():
    muon = {55: [{"id": 2, "body": "nhắc lại: **Lease `lease-that`**",
                  "user": {"login": "github-actions[bot]"}}]}
    ex, _ = _goi_lop_gh(GhGia(comments=muon), "_kiem_comment_da_co", "o/r",
                        lease_mau(lease_id="lease-that"), env_them=ENV_GITHUB)
    bang(ex is None, f"dấu không ở đầu thân bị tính là đã đăng: {ex}")


@ca
def t56_lease_id_ky_tu_dac_biet_phai_CHAN():
    with San() as s:
        for lease_id in ("x`y", "x*y"):
            rc, _, e = chay("check", viet(s, lease_mau(lease_id=lease_id), "id.yaml"))
            bang(rc == RC_NOI_DUNG and "lease_id" in e,
                 f"lease_id {lease_id!r} lọt: rc={rc}, err={e!r}")


@ca
def t57_slurp_khong_trang_CHAN_mot_trang_rong_QUA():
    def tra(noi_dung):
        return lambda *a: subprocess.CompletedProcess(a, 0, noi_dung, "")
    ex1, _ = _goi_lop_gh(tra("[]"), "_kiem_comment_da_co", "o/r", lease_mau(),
                         env_them=ENV_GITHUB)
    ex2, _ = _goi_lop_gh(tra("[[]]"), "_kiem_comment_da_co", "o/r", lease_mau(),
                         env_them=ENV_GITHUB)
    bang(ex1 and ex1.ma == RC_NOI_DUNG and ex2 is None,
         f"[] và [[]] bị nhập một trạng thái: []={ex1}, [[]]={ex2}")


@ca
def t58_check_body_thuan_va_check_khai_lop_chua_chay():
    import contextlib
    import io
    import os
    from types import SimpleNamespace
    from unittest import mock
    with San() as s:
        p, mod, gh = viet(s, lease_mau()), _nap_cong(), GhGia()
        mod.GOI_GH = gh
        a = SimpleNamespace(tep=str(p), goc=None)
        with mock.patch.dict(os.environ, {"GITHUB_REPOSITORY": "o/r",
                                         "GITHUB_ACTOR": "ducthangho"}, clear=True):
            ra_check, ra_body = io.StringIO(), io.StringIO()
            with contextlib.redirect_stdout(ra_check):
                rc1 = mod.lenh_check(a)
            with contextlib.redirect_stdout(ra_body):
                rc2 = mod.lenh_body(a)
        bang(rc1 == rc2 == RC_OK and not gh.calls and "KHÔNG CHẠY" in ra_check.getvalue()
             and "kiem-github" in ra_check.getvalue() and "**Lease" in ra_body.getvalue(),
             f"check/body chạm GOI_GH hoặc khai thiếu: calls={gh.calls}, check={ra_check.getvalue()!r}")


@ca
def t59_moi_lease_goi_kiem_github_truoc_check():
    kq = _chay_buoc_dang()
    for ten in ("dau", "giua", "cuoi"):
        tep = f"ops/leases/{ten}.yaml"
        kiem, check = ["kiem-github", tep], ["check", tep]
        bang(kq["calls"].count(kiem) == kq["calls"].count(check) == 1
             and kq["calls"].index(kiem) < kq["calls"].index(check),
             f"thiếu/sai thứ tự kiem-github cho {tep}: {kq['calls']}")


@ca
def t60_kiem_github_hong_khong_POST_va_lam_buoc_DO():
    kq = _chay_buoc_dang(kiem_github_hong="giua")
    bang(kq["rc"] != 0 and "`dau`" in kq["bodies"] and "`cuoi`" in kq["bodies"]
         and "`giua`" not in kq["bodies"], f"kiem-github hỏng bị nuốt: {kq}")


@ca
def t62_kiem_github_rc9_bo_qua_lease_va_buoc_XANH():
    kq = _chay_buoc_dang(kiem_github_rc9="giua")
    bang(kq["rc"] == 0 and kq["bodies"].count("`dau`") == 1
         and kq["bodies"].count("`cuoi`") == 1 and "`giua`" not in kq["bodies"],
         f"kiem-github rc=9 xử lý sai: {kq}")


@ca
def t63_check_rc9_bo_qua_lease_va_buoc_XANH():
    kq = _chay_buoc_dang(check_rc9="giua")
    bang(kq["rc"] == 0 and kq["bodies"].count("`dau`") == 1
         and kq["bodies"].count("`cuoi`") == 1 and "`giua`" not in kq["bodies"],
         f"check rc=9 xử lý sai: {kq}")


VE_TRUOC_POST = ("khong_POST", "khong_quan_sat_ghi_nguoc_sau_guard")
VE_SAU_POST = ("co_POST", "khong_the_quan_sat_vang_POST")
SO_GUARD_DANG = {
    r'''bao_chan "hai lớp GitHub chặn (rc=$rc)"''': ("kiem-github", VE_TRUOC_POST),
    r'''bao_chan "cổng chặn (rc=$rc)"''': ("check", VE_TRUOC_POST),
    r'''bao_chan "không đọc được packet_issue (rc=$rc)"''': ("packet_issue", VE_TRUOC_POST),
    r'''bao_chan "không dựng được thân comment (rc=$rc)"''': ("body", VE_TRUOC_POST),
    r'''bao_chan "không dựng được payload (rc=$rc)"''': ("payload", VE_TRUOC_POST),
    r'''bao_chan "đăng comment hỏng (rc=$rc)"''': ("post_rc", VE_SAU_POST),
    r'''bao_chan "gh không trả về comment id: $ID"''': ("case_id", VE_SAU_POST),
    r'''bao_chan "không ghi được comment id (rc=$rc)"''': ("mark", VE_SAU_POST),
    r'''bao_chan "không ghi được GITHUB_ENV (rc=$rc)"''': ("github_env", VE_SAU_POST),
}


def _guard_dan_xuat(than=None) -> set[str]:
    than = _buoc_workflow("đăng")["run"] if than is None else than
    bao = re.findall(r"(?<![\w])bao_chan(?![\w(])", than)
    goi = [x.rstrip() for x in re.findall(r"(?m)(?<![\w])bao_chan[ \t]+[^;\n]+", than)]
    tap = set(goi)
    bang(bao and len(bao) == len(goi) == len(tap), f"không phân tích kín bao_chan: {goi}")
    return tap


def _ve_dan_xuat(than=None) -> dict:
    than = _buoc_workflow("đăng")["run"] if than is None else than
    post = next(x for x in than.splitlines() if x.strip().startswith("ID=$(gh api "))
    return {x: VE_TRUOC_POST if than.index(x) < than.index(post) else VE_SAU_POST
            for x in SO_GUARD_DANG}


@ca
def t64_guard_dan_xuat_tu_YAML_khop_so_dang_ky():
    dan_xuat, dang_ky = _guard_dan_xuat(), set(SO_GUARD_DANG)
    bang(dan_xuat == dang_ky, f"guard YAML != sổ: {dan_xuat ^ dang_ky}")


@ca
def t65_bo_trich_rong_hoac_hong_phai_DO():
    for than in ("", "set +e\nfalse\nset -e\n"):
        try:
            _guard_dan_xuat(than)
        except AssertionError:
            continue
        bang(False, f"bộ trích fail-open với {than!r}")
    try:
        _ve_dan_xuat(_buoc_workflow("đăng")["run"].replace("ID=$(gh api ", "ID=$( gh api ", 1))
    except (StopIteration, ValueError):
        pass
    else:
        bang(False, "bộ dẫn xuất vế fail-open khi không tìm được POST")


@ca
def t66_moi_guard_co_phan_chung_va_ve_theo_vi_tri():
    than, ve = _buoc_workflow("đăng")["run"], _ve_dan_xuat()
    mark = next(x for x, (loi, _) in SO_GUARD_DANG.items() if loi == "mark")
    for guard, (loi, _) in SO_GUARD_DANG.items():
        kq = _chay_buoc_dang(guard_hong=loi)
        co_post, da_mark = ve[guard] == VE_SAU_POST, than.index(guard) > than.index(mark)
        bang(kq["rc"] == 1 and kq["posts"].count("dau") == kq["posts"].count("cuoi") == 1
             and kq["posts"].count("giua") == int(co_post) and kq["marks"]["giua"] == da_mark
             and "BI_CHAN=1" in kq["out"], f"guard {loi}, vế {ve[guard]} sai: {kq}")


@ca
def t67_ve_khang_dinh_phai_khop_vi_tri_dan_xuat_tu_YAML():
    dan_xuat = _ve_dan_xuat()
    bang(all(dan_xuat[x] == ve for x, (_, ve) in SO_GUARD_DANG.items()),
         f"vế đăng ký lệch vị trí YAML: "
         f"{[(loi, dan_xuat[x], ve) for x, (loi, ve) in SO_GUARD_DANG.items() if dan_xuat[x] != ve]}")


@ca
def t68_post_rc_hong_khong_duoc_mark():
    kq = _chay_buoc_dang(guard_hong="post_rc")
    bang(kq["rc"] == 1 and kq["posts"].count("giua") == 1
         and not kq["marks"]["giua"], f"POST rc=1 bị mark: {kq}")


def _dong_tong_ket(qua: int, da_chay: int, bo_qua: int) -> str:
    return f"\nlease_publish: {qua}/{da_chay} đạt; đã chạy={da_chay}, bỏ qua={bo_qua}"
@ca
def t69_W1_W2_thieu_dau_ra_do_gia_phai_bao_du_ba_manh():
    with San() as s:
        loi = ""
        try: _doc_do_gia(s / "khong-sinh", 37, "OUT", "ERR", "đầu ra thử")
        except AssertionError as ex: loi = str(ex)
        bang(all(x in loi for x in
                 ("KHÔNG ĐO ĐƯỢC", "rc=37", "stdout='OUT'", "stderr='ERR'")),
             f"lỗi thiếu tệp không giữ đủ phép đo: {loi!r}")


@ca
def t70_W6_matrix_co_Windows_phai_chay_lai_tam_ca():
    job = {"runs-on": "${{ matrix.os }}", "strategy": {"matrix": {
        "os": ["ubuntu-latest", "windows-latest"]}}}
    ly_do = _ly_do_bo_qua_workflow(WORKFLOW_DANG, "dang", nen="nt", job=job)
    doc_than = [fn.__name__ for fn in CA if "_chay_buoc_dang" in fn.__code__.co_names]
    bang(not ly_do and len(doc_than) == 8,
         f"matrix có Windows vẫn bỏ qua hoặc không dẫn xuất đủ tám ca: {ly_do!r}, {doc_than}")


def _chay_main_meta(fn, nen=None):
    import contextlib, io, os
    from unittest import mock
    cu, out = CA[:], io.StringIO()
    CA[:] = [fn]
    try:
        with contextlib.redirect_stdout(out), (mock.patch.object(os, "name", nen)
                                                if nen else contextlib.nullcontext()):
            rc = main()
    finally: CA[:] = cu
    return rc, out.getvalue()


@ca
def t71_W7_workflow_khong_ubuntu_only_cam_bo_qua():
    with San() as s:
        tep = s / "w.yml"
        tep.write_text("jobs:\n  j:\n    runs-on: windows-latest\n", encoding="utf-8")
        def sai(): raise BoQuaNen(tep, "j")
        rc, out = _chay_main_meta(sai, "nt")
        bang(rc == 1 and "ĐỎ" in out, f"main tin lời bỏ qua không dẫn xuất được: {out}")


@ca
def t72_W8_bo_qua_phai_in_runs_on_va_tong_ket():
    with San() as s:
        nhan = "ubuntu-" + next(tempfile._get_candidate_names())
        tep = s / "w.yml"
        tep.write_text(f"jobs:\n  j:\n    runs-on: {nhan}\n", encoding="utf-8")
        def bo(): raise BoQuaNen(tep, "j")
        rc, out = _chay_main_meta(bo, "nt")
        bang(rc == 0 and nhan in out and "bỏ qua=1" in out,
             f"main không in lý do tự dẫn xuất/tổng kết: rc={rc}, {out!r}")


def main() -> int:
    qua, hong, bo_qua = 0, [], []
    for fn in CA:
        try:
            fn()
            qua += 1
        except BoQuaNen as ex:
            try: ly_do = _ly_do_bo_qua_workflow(ex.tep, ex.ten_job)
            except Exception: ly_do = ""
            if ly_do:
                bo_qua.append((fn.__name__, ly_do))
            else:
                hong.append((fn.__name__, "bỏ qua không dẫn xuất được từ runs-on"))
        except AssertionError as ex:
            hong.append((fn.__name__, str(ex)))
        except Exception as ex:  # noqa: BLE001
            hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))
    for ten, ly in bo_qua:
        print(f"  BỎ QUA {ten}: {ly}")
    for ten, ly in hong:
        print(f"  ĐỎ  {ten}: {ly}")
    print(_dong_tong_ket(qua, len(CA) - len(bo_qua), len(bo_qua)))
    return 1 if hong else 0


if __name__ == "__main__":
    sys.exit(main())
