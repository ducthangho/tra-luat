#!/usr/bin/env python3
"""Kiểm lease THÊM/SỬA trong một PR ở MỌI đường — packet #1445 r1 (đặc tả `ops/specs/lease-pr-r1.md`).

VÌ SAO CÓ. Bộ kiểm lease nghiêm (`lease_publish.kiem` / `lease_publish.py check`) chỉ chạy ở hai chỗ:
`ci_duong_nhanh.py kiem-re` (PR chỉ đổi `ops/{land,leases,reviews,specs}/**`) và `ops-publish-lease.yml` (nhánh `ops/**`).
Lease đi kèm một PR đường thường vì thế vào master mà không ai kiểm. Đo trên `6774181` (Issue #1445): 48/209 lease không qua
kiểm nghiêm. PR đầu tiên sửa riêng một lease như vậy mới đỏ (PR #1442 phải làm lại thành #1443).

CÁCH LÀM. Tệp này KHÔNG có luật riêng. Nó chỉ import hai hàm của `ci_duong_nhanh.py` để cùng một định nghĩa được dùng ở mọi đường:
  · `doc_diff(env)`: tập tệp đổi của PR, cùng định nghĩa với bộ phân loại `chuan-bi`. `None` = KHÔNG ĐO ĐƯỢC.
  · `kiem_lease(doi)`: lease còn hạn chạy `lease_publish.py check`; lease hết hạn chạy `kiem(bo_qua_han=True)`. Tệp đã xoá bỏ qua.
`ci.yml` và `ci_duong_nhanh.py` cố ý KHÔNG bị sửa: lease `wp1448-r2-g1-claude` giữ chúng tới 2026-11-23T08:00Z.

LUẬT THOÁT:
  · sự kiện khác `pull_request` ⇒ rc 0, không gọi git (cổng là PR; push/dispatch không có gì để chặn);
  · `doc_diff` = None ⇒ rc 1 (fail-close: không biết PR đổi gì thì không được nói "không có lease hỏng");
  · có lỗi lease ⇒ rc 1; còn lại rc 0.

GIỚI HẠN (đặc tả §2): check mới chưa chặn merge cho tới khi chủ kho thêm context `kiem-lease-pr` vào ruleset. Chốt `GITHUB_ACTOR`
của `check` áp cho lease còn hạn, y như đường nhanh.

Dùng: python ops/kiem_lease_pr.py   (đọc CI_DUONG_NHANH_SU_KIEN / _GOC / _DAU / _MERGE từ môi trường)
"""
from __future__ import annotations

import os
import subprocess
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import ci_duong_nhanh as cdn  # noqa: E402  (đường import phải có trước)

TIEN_TO = "KIEM_LEASE_PR: "


def la_lease(duong: str) -> bool:
    return duong.startswith("ops/leases/") and duong.endswith((".yaml", ".yml"))


def chay(env=os.environ, chay_lenh=subprocess.run, kho=cdn.ROOT, ra=None, bay_gio=None) -> int:
    ra = ra if ra is not None else sys.stdout
    su_kien = env.get(cdn.BIEN_SU_KIEN) or ""
    if su_kien != "pull_request":
        print(f"{TIEN_TO}su_kien={su_kien!r} khong phai pull_request - cong la PR, bo qua (rc 0)", file=ra)
        return 0
    doi = cdn.doc_diff(env, chay_lenh, kho)
    if doi is None:
        print(f"{TIEN_TO}KHONG DO DUOC tap tep doi cua PR (SHA vang/hong, git loi, nhieu merge-base hoac dau ra cut) - DO", file=ra)
        return 1
    lease = sorted(x for x in doi if la_lease(x))
    for x in lease:
        print(f"{TIEN_TO}lease doi: {x!r}" + ("" if (Path(kho) / x).is_file() else " (da xoa - bo qua)"), file=ra)
    loi = cdn.kiem_lease(doi, kho, chay_lenh, bay_gio, ra)
    for x in loi:
        print(f"{TIEN_TO}LOI - {x}", file=ra)
    print(f"{TIEN_TO}{'DO' if loi else 'DAT'} ({len(lease)} lease doi trong {len(doi)} tep doi, {len(loi)} loi)", file=ra)
    return 1 if loi else 0


if __name__ == "__main__":
    cdn._ep_utf8()
    raise SystemExit(chay())
