# -*- coding: utf-8 -*-
"""wp725 — hướng dẫn NLM cũ (`nlm login --check` làm phép xác nhận) không quay lại tài liệu và help.

N1: mọi dòng chứa `login --check` trong COWORK_PROJECT.md / RUNBOOK.md phải khớp ĐÚNG MỘT neo trong danh sách
CHO PHÉP (câu phủ định có chủ đích), và mỗi neo khớp đúng một dòng. N2: help của `nlm-auth-stage` và các cờ của nó
không dạy quy trình cũ; help `--force` nói đúng là KHÔNG qua được cổng canary.
"""

import argparse
from pathlib import Path


TEST_ID = "wp725_huong_dan_nlm"

_CAU_CU = "login --check"

# Danh sách CHO PHÉP: (tệp, chuỗi con neo duy nhất của dòng được phép nhắc `login --check`).
_CHO_PHEP = (
    ("references/RUNBOOK.md", "`nlm login --check` xanh KHÔNG đủ."),
    ("references/RUNBOOK.md", "`nlm login --check` KHÔNG còn là bằng chứng"),
    ("references/RUNBOOK.md", "rc 0 của refresh, `nlm login --check` hay số notebook đều KHÔNG cho phép upload"),
    ("references/COWORK_PROJECT.md", "`nlm login --check` xanh hay rc 0 của refresh KHÔNG đủ để stage"),
)


def _vi_pham_tai_lieu(van_ban_theo_tep):
    """Trả danh sách vi phạm (rỗng = đạt). `van_ban_theo_tep`: {đường dẫn tương đối: văn bản}."""
    loi = []
    dung = {neo: 0 for neo in _CHO_PHEP}
    for tep, van_ban in van_ban_theo_tep.items():
        for so, dong in enumerate(van_ban.splitlines(), 1):
            if _CAU_CU not in dong:
                continue
            khop = [neo for neo in _CHO_PHEP if neo[0] == tep and neo[1] in dong]
            if len(khop) != 1:
                loi.append(f"{tep}:{so}")
            for neo in khop:
                dung[neo] += 1
    loi.extend(f"neo:{neo[0]}:{neo[1][:30]}={n}" for neo, n in dung.items() if n != 1)
    return loi


_KEO_CU = ("- **Drive → Cowork (kéo):** đầu phiên `bootstrap` đã ghi cookie; giữa phiên cần mới hơn thì\n"
           "  `python scripts/tl.py nlm-auth-pull --secrets-file ./tl_secrets.enc` (hoặc bỏ `--secrets-file` để direct-media\n"
           "  kéo bản mới nhất trên Drive). Cowork KHÔNG tự chạy browser được nên KHÔNG tự refresh — refresh thật ở Code.\n")


def _vi_pham_duong_keo(cowork):
    """Bước 3: bản wrapper đẩy ở NLM_CRED_FILEID ⇒ đường kéo mặc định phải là `nlm-auth-load`, không phải
    `nlm-auth-pull` (đọc bundle `secrets`, cũ hơn) — reviewer lượt 1 đo được pull nhận bản CŨ, rc 0."""
    try:
        buoc3 = cowork.split("## Bước 3", 1)[1].split("\n## ", 1)[0]
        keo = buoc3.split("- **Drive → Cowork (kéo):**", 1)[1].split("\n\n", 1)[0].split("\n- **", 1)[0]
    except IndexError:
        return ["thiếu Bước 3 / mục kéo"]
    loi = []
    if "nlm-auth-load" not in keo:
        loi.append("mục kéo không nêu nlm-auth-load")
    elif "nlm-auth-pull" in keo and keo.index("nlm-auth-pull") < keo.index("nlm-auth-load"):
        loi.append("nlm-auth-pull đứng trước nlm-auth-load")
    if "nlm-auth-pull --secrets-file" in keo:
        loi.append("mục kéo còn dạy nlm-auth-pull --secrets-file làm đường mặc định")
    return loi


def _help_nlm_auth_stage(tl_module):
    parser = tl_module.build_parser()
    sub = next(a for a in parser._actions if isinstance(a, argparse._SubParsersAction))
    cmd = sub.choices["nlm-auth-stage"]
    lenh_help = next(c.help for c in sub._choices_actions if c.dest == "nlm-auth-stage")
    co = {s: a.help or "" for a in cmd._actions for s in a.option_strings}
    return lenh_help or "", co


def _vi_pham_help(lenh_help, co):
    loi = []
    tat_ca = [lenh_help, co.get("--refresh", ""), co.get("--force", "")]
    if any(_CAU_CU in h for h in tat_ca):
        loi.append("help nhắc login --check")
    if "sau `nlm login`" in lenh_help:
        loi.append("help lệnh: stage sau nlm login")
    if "canary" not in lenh_help:
        loi.append("help lệnh: thiếu cổng canary")
    force = co.get("--force", "")
    if "bỏ qua cổng verify" in force or "DÙ cookie đang chết" in force:
        loi.append("help --force: hứa bỏ qua cổng")
    if "KHÔNG bỏ qua được cổng canary" not in force:
        loi.append("help --force: thiếu khẳng định cổng vẫn áp")
    if "tái sinh cookie từ browser profile" in co.get("--refresh", ""):
        loi.append("help --refresh: mô tả cơ chế cũ")
    return loi


def run(tl_module):
    goc = Path(tl_module.__file__).resolve().parent.parent
    tai_lieu = {t: (goc / t).read_text(encoding="utf-8")
                for t in ("references/RUNBOOK.md", "references/COWORK_PROJECT.md")}
    if _vi_pham_tai_lieu(tai_lieu):
        return False
    # Phản chứng tại chỗ: một dòng khẳng định kiểu cũ bơm vào phải bị bắt — chứng minh bộ kiểm có răng.
    ban_ban = dict(tai_lieu)
    ban_ban["references/COWORK_PROJECT.md"] += "\nĐịnh kỳ chạy `tl secrets-set --nlm` (tự `nlm login --check` refresh).\n"
    if not _vi_pham_tai_lieu(ban_ban):
        return False
    cowork = tai_lieu["references/COWORK_PROJECT.md"]
    if _vi_pham_duong_keo(cowork):
        return False
    keo_moi = cowork.split("- **Drive → Cowork (kéo):**", 1)[1].split("\n\n", 1)[0]
    if not _vi_pham_duong_keo(cowork.replace("- **Drive → Cowork (kéo):**" + keo_moi + "\n", _KEO_CU, 1)):
        return False            # phản chứng: trả mục kéo về bản cũ (pull bundle) phải bị bắt
    lenh_help, co = _help_nlm_auth_stage(tl_module)
    if _vi_pham_help(lenh_help, co):
        return False
    co_cu = dict(co)
    co_cu["--force"] = "(v1.33.39) bỏ qua cổng verify-LIVE — ép stage DÙ cookie đang chết"
    return bool(_vi_pham_help(lenh_help, co_cu))
