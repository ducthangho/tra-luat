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

RC_OK, RC_THAM_SO, RC_TU_CAP, RC_DA_DANG, RC_NOI_DUNG = 0, 2, 4, 9, 8

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
