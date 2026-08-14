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
from pathlib import Path

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
