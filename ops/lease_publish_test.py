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

import subprocess
import sys
import tempfile
from datetime import datetime, timedelta, timezone
from pathlib import Path, PurePosixPath

HERE = Path(__file__).resolve().parent
SCRIPT = HERE / "lease_publish.py"

RC_OK, RC_THAM_SO, RC_TU_CAP, RC_DA_DANG, RC_NOI_DUNG, RC_NEO = 0, 2, 4, 9, 8, 6

CA: list = []


def ca(fn):
    CA.append(fn)
    return fn


def chay(*doi_so):
    p = subprocess.run([sys.executable, str(SCRIPT), *[str(x) for x in doi_so]],
                       capture_output=True, text=True)
    return p.returncode, p.stdout, p.stderr


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


@ca
def t25_workflow_dang_lease_phai_chay_bo_kiem_NEO_khong_lay_tu_head():
    """Workflow đăng lease KHÔNG được chạy `lease_publish*.py` lấy từ head được đẩy.

    Finding P1 của cross-review trên PR #104 (14-08-2026): bản trước chạy
    `python3 ops/lease_publish.py`, tức bộ kiểm ĐẾN TỪ CHÍNH NHÁNH ĐANG BỊ KIỂM. Một
    push vào `ops/**` vừa thêm tên mình vào `NGUOI_CO_THAM_QUYEN` vừa đổi lease là đủ:
    `checkout` lấy head đó, workflow chạy bộ kiểm đã bị sửa, cả `granted_by` lẫn
    `GITHUB_ACTOR` đều qua. Bộ kiểm nằm cùng nhánh với thứ nó kiểm thì nó không kiểm gì.

    Ca này canh phần MÁY canh được: mọi lời gọi `lease_publish.py` / `lease_publish_test.py`
    trong workflow phải đi qua bản neo (`$NEO/…`), không được gọi thẳng `ops/…`.

    KHÔNG canh được ở đây, và phải nói thẳng: với sự kiện `push`, GitHub lấy chính
    tệp workflow từ head, nên ai sửa được bộ kiểm cũng sửa được ca này lẫn mỏ neo.
    Phần ấy chỉ ruleset ngoài kho mới đóng. Ca này chặn TRÔI NGƯỢC do vô ý — bản vá
    bị "dọn cho gọn" về lại `ops/…` — chứ không chặn kẻ cố tình.
    """
    import re
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
    # Chỉ soi dòng THỰC SỰ chạy python, không soi chú thích — chú thích giải thích về
    # `ops/lease_publish.py` là hợp lệ và cần thiết (cả khối "vì sao có lớp 4" ở đầu
    # tệp nhắc tên ấy). Cấm luôn thì không viết nổi tài liệu, và một ca bắt oan là
    # một ca sắp bị gỡ.
    goi = re.compile(r"python3?\s+(\S*lease_publish(?:_test)?\.py)")
    thay = 0
    for so, dong in enumerate(noi_dung.splitlines(), 1):
        if dong.lstrip().startswith("#"):
            continue
        for duong in goi.findall(dong):
            thay += 1
            bang("$NEO" in duong or "${NEO}" in duong,
                 f"ops-publish-lease.yml:{so} chạy {duong!r} — bộ kiểm này đến TỪ HEAD "
                 f"ĐƯỢC ĐẨY, tức từ chính nhánh nó đang kiểm (finding P1, PR #104). "
                 f"Phải gọi qua bản neo vào nhánh mặc định: \"$NEO/ops/…\"")
    # Không cho "workflow không gọi bộ kiểm lần nào" âm thầm thành ĐẠT: một tệp đã bị
    # gỡ sạch lời gọi và một tệp gọi đúng cho cùng màu xanh, mà nghĩa thì ngược nhau.
    bang(thay >= 3,
         f"chỉ thấy {thay} lời gọi lease_publish* trong workflow — chờ ít nhất 3 "
         f"(test, check, body); ca này đang không đo cái nó tưởng nó đo")
    # Mỏ neo phải CÓ THẬT, không chỉ là biến `$NEO` trỏ vào hư không.
    bang("git worktree add" in noi_dung and "default_branch" in noi_dung,
         "không thấy bước dựng worktree từ `default_branch` — `$NEO` phải được neo "
         "vào nhánh mặc định, nếu không thì nó chỉ là một tên biến khác cho head")


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
def t34_MOI_workflow_goi_bo_test_deu_phai_duoc_cap_actionlint():
    """Workflow nào ĐỘNG tới bộ test này thì phải gọi `ops/cai_actionlint.sh` — KHÔNG trừ ai.

    VÌ SAO CÓ CA NÀY, và nó không phải giả thiết. `t33` được thêm ở `#195`, mà bộ test này
    được HAI workflow gọi: `ci.yml` (được cấp công cụ) và `ops-publish-lease.yml` (KHÔNG).
    Đo được ở run `32351892214`:

        ĐỎ  t33_workflow_dang_lease_phai_qua_actionlint: KHÔNG ĐO ĐƯỢC: thiếu `actionlint`
        lease_publish: 32/33 đạt
        ##[error]Process completed with exit code 1.

    Hệ quả: cổng đăng lease vẫn chết, chỉ ĐỔI LÝ DO — `rc=8` vì lease cũ hết hạn thành
    `rc=1` vì thiếu công cụ. Người đẩy lease vẫn không đăng được gì.

    VÌ SAO VIẾT LẠI (cross-review `#200`, codex, P2-1). Bản trước cố ĐOÁN dòng nào là
    "người gọi thật" bằng một danh sách `SOI` khớp CHUỖI CON TRÊN CẢ DÒNG. Đo được:

        run: echo preparing; python ops/lease_publish_test.py     -> 35/35 đạt, rc=0

    Cả dòng chứa `echo ` nên bị loại khỏi tập người gọi — trong khi nó GỌI THẬT. Đo tiếp,
    và đây mới là chỗ đau: bỏ HẲN bước cài `actionlint` khỏi `ci.yml` rồi giấu người gọi
    sau `echo ` thì bộ test VẪN `35/35`, tức ca này im lặng đúng lúc regression
    `32351892214` quay lại. Fail-OPEN.

    Nên KHÔNG siết mẫu chuỗi thêm lần nữa — đó là lần thứ tư cùng một hình dạng lỗi. Đổi
    NGHĨA VỤ cho nó không cần đoán: hễ một dòng lệnh có NHẮC tới bộ test thì workflow ấy
    phải gọi `ops/cai_actionlint.sh`. Không phân biệt "gọi thật" với "chỉ soi" nữa — phân
    biệt sai hướng nào cũng ra fail-open, còn nghĩa vụ thừa thì rẻ (thêm một dòng gọi
    script). Chỉ còn MỘT token canonical để khớp, và `t35` mới là chỗ đo HÀNH VI.

    VÀ LẦN VIẾT LẠI ẤY VẪN CHƯA ĐÓNG ĐƯỢC NÓ (cross-review `#203`, codex, P2-1 mở lại).
    Câu "chỉ còn MỘT token canonical để khớp" ở ngay trên là chỗ hỏng: **vẫn là khớp
    chuỗi**, chỉ đổi chỗ khớp — từ "caller" sang "installer". Phản chứng đo được:

        run: echo ops/cai_actionlint.sh      ->  35/35 đạt, rc=0

    Token vẫn còn nguyên trên dòng nên workflow được tính là đã cấp công cụ, trong khi nó
    KHÔNG chạy gì cả. Lần thứ tư cùng một hình dạng, và lần này nằm trong chính packet
    sinh ra để chấm dứt hình dạng đó.

    Nên bỏ hẳn phép khớp chuỗi: đảo thành **DANH SÁCH CHO PHÉP** (`GOI_CANON`). Một bước
    được tính là THỰC THI installer chỉ khi TOÀN BỘ phần lệnh của nó — đã bỏ chú thích và
    dòng trắng — bằng ĐÚNG một mục trong danh sách. Danh sách CẤM phải đoán trước mọi cách
    viết của kẻ gian nên thua từ trong thiết kế; danh sách CHO PHÉP chỉ phải liệt kê một
    tập nhỏ và biết trước. Cần thêm biến thể thì thêm vào `GOI_CANON` — tường minh, đọc
    được, và ai thêm phải nói rõ vì sao.

    ĐỘT BIẾN ĐÃ CHẠY: đổi cả hai workflow sang `run: echo ops/cai_actionlint.sh` ⇒ ca này
    ĐỎ (`35/36`, rc=1). Trước bản vá, chính đột biến ấy cho `35/35` rc=0.
    """
    import yaml
    goc = HERE.parent / ".github" / "workflows"
    if not goc.is_dir():
        # KHÔNG có nhánh "không thấy thì bỏ qua" trong kho thật: chỉ tha cho BẢN SAO rời.
        bang(not (HERE.parent / ".git").exists(),
             f"kho thật mà không thấy {goc} — ca này sẽ xanh mà không đo gì")
        return

    # DANH SÁCH CHO PHÉP, không phải phép khớp chuỗi. Một bước được tính là THỰC THI
    # installer chỉ khi TOÀN BỘ phần lệnh của nó (đã bỏ chú thích, bỏ dòng trắng) bằng
    # ĐÚNG một mục dưới đây. Cần thêm biến thể thì THÊM VÀO ĐÂY — tường minh, đọc được.
    GOI_CANON = (
        ["bash ops/cai_actionlint.sh"],
    )

    def _thuc_thi_installer(than: str) -> bool:
        return [x.strip() for x in _dong_lenh(than) if x.strip()] in [list(x) for x in GOI_CANON]

    nhac_bo_test, thieu_cong_cu = [], []
    for tep in sorted(goc.glob("*.yml")) + sorted(goc.glob("*.yaml")):
        d = yaml.safe_load(tep.read_text(encoding="utf-8")) or {}
        than_chay = [b["run"] for job in (d.get("jobs") or {}).values()
                     for b in (job.get("steps") or []) if isinstance(b.get("run"), str)]
        # BỎ CHÚ THÍCH TRƯỚC (`_dong_lenh`), nếu không một dòng `# ops/cai_actionlint.sh`
        # sẽ được tính là đã cấp công cụ — phép kiểm không phân biệt được LỆNH với CHÚ
        # THÍCH thì nó đang đọc tài liệu, không đọc hành vi.
        dong_lenh = [x for than in than_chay for x in _dong_lenh(than)]
        if not any("lease_publish_test.py" in x for x in dong_lenh):
            continue
        nhac_bo_test.append(tep.name)
        if not any(_thuc_thi_installer(than) for than in than_chay):
            thieu_cong_cu.append(tep.name)

    # KHÔNG cho "không tìm thấy workflow nào" âm thầm thành ĐẠT: một lượt quét hỏng và một
    # kho thật sự không ai gọi bộ test cho cùng màu xanh, mà nghĩa thì ngược nhau.
    bang(nhac_bo_test,
         "không thấy workflow nào nhắc `lease_publish_test.py` — phép quét đang hỏng, "
         "hoặc bộ test này đã mồ côi; cả hai đều phải ĐỎ chứ không phải xanh rỗng")
    bang(not thieu_cong_cu,
         f"workflow {thieu_cong_cu} động tới `lease_publish_test.py` mà KHÔNG có bước nào "
         f"THỰC THI `ops/cai_actionlint.sh`. Một bước được tính chỉ khi phần lệnh của nó "
         f"bằng ĐÚNG một mục trong `GOI_CANON` — `echo ops/cai_actionlint.sh` KHÔNG tính, "
         f"và đó chính là phản chứng đã lọt ở cross-review #203. Bộ test ĐÒI `actionlint` "
         f"(t33 fail-close), nên workflow không cấp thì cổng chết vì thiếu công cụ chứ "
         f"không phải vì lease sai — đúng regression run 32351892214. Cần một biến thể "
         f"lệnh khác thì THÊM vào `GOI_CANON`, đừng nới phép so.")


def _bam_tep(duong_dan):
    """sha256 của một tệp — để ca test tự cấp `AL_SHA256` cho gói GIẢ nó vừa dựng."""
    import hashlib
    h = hashlib.sha256()
    with open(duong_dan, "rb") as f:
        for khoi in iter(lambda: f.read(65536), b""):
            h.update(khoi)
    return h.hexdigest()


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

    # ——— GIỮ TẦNG: workflow chỉ được GỌI script, không được cài lại tại chỗ.
    goc = HERE.parent / ".github" / "workflows"
    if goc.is_dir():
        LAY_VE = ("curl", "wget", "choco install", "brew install", "go install")
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
                                   f"bản chép sẽ không được ca này chạy thử. Gọi script.")
                    if "ops/cai_actionlint.sh" not in than:
                        continue
                    ban = str((b.get("env") or {}).get("AL_VER") or "")
                    if not re.fullmatch(r"\d+\.\d+\.\d+", ban):
                        loi.append(f"{ten}: gọi `ops/cai_actionlint.sh` mà thiếu `AL_VER` "
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


def main() -> int:
    qua, hong = 0, []
    for fn in CA:
        try:
            fn()
            qua += 1
        except AssertionError as ex:
            hong.append((fn.__name__, str(ex)))
        except Exception as ex:  # noqa: BLE001
            hong.append((fn.__name__, f"{type(ex).__name__}: {ex}"))
    for ten, ly in hong:
        print(f"  ĐỎ  {ten}: {ly}")
    print(f"\nlease_publish: {qua}/{len(CA)} đạt")
    return 1 if hong else 0


if __name__ == "__main__":
    sys.exit(main())
