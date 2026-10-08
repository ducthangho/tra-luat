#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""Cổng chặn cho đường ĐĂNG LEASE BẰNG GIT.

VÌ SAO CÓ TỆP NÀY
Git không tạo được issue/comment/PR — đó là cơ sở dữ liệu riêng của GitHub, không
phải object trong git. Nhưng Actions thì kích hoạt được bằng `push`, và mỗi workflow
tự có `GITHUB_TOKEN`. Nên chuỗi `git push → workflow → API` biến git thành đường vận
chuyển cho thao tác GitHub, và phiên chạy chỉ cần quyền git — thứ MỌI phiên đều có.
Đã đo 13/14-08-2026: phiên `origin: claude_code_mcp_seed` bị chặn 403 ở mọi lời gọi
`api.github.com`, trong khi clone/fetch/push đều chạy.

ĐỔI LẠI, RỦI RO PHẢI NÓI THẲNG: workflow chạy bằng `GITHUB_TOKEN` nghĩa là **push
được thành đăng được**. Thứ duy nhất đứng giữa một tệp YAML trong kho và một comment
mang danh nghĩa kho chính là bộ kiểm trong tệp này. `check` và `body` cùng đi qua
`kiem()` thuần; riêng hai phép đo GitHub chỉ workflow gọi qua `kiem-github`.

MÃ THOÁT
  0  qua
  2  tham số / không đọc được tệp
  4  `granted_by` là tên một PROVIDER — agent tự cấp lease cho mình
  6  mỏ neo prompt hỏng (thiếu `prompt_path`, tệp không có, hoặc băm lệch)
  8  nội dung lease sai (thiếu trường, sai dạng, hết hạn, YAML hỏng)
  9  lease ĐÃ có comment trên Issue — BỎ QUA, không đăng lại
 10  lớp review khai không khớp lớp cổng tính từ write_set
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import shlex
import subprocess
import sys
import unicodedata
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath
from urllib.parse import urlparse

RC_OK = 0
RC_THAM_SO = 2
RC_TU_CAP = 4
RC_NEO = 6
RC_NOI_DUNG = 8
RC_DA_DANG = 9
RC_LOP = 10
RC_DANG_GIU = 11
RC_KHONG_XAC_DINH = 12

_THU_TU_LOP = {"routine": 0, "systemic": 1, "sensitive": 2}

# Danh sách CHO PHÉP cố ý hẹp: chỉ những đường mà Protocol §8 gọi tên đủ để
# phân lớp. Đường không biết không được suy từ đuôi tệp hay tên thư mục; nó rơi
# về `sensitive`. Nhờ vậy thêm một loại artefact mới không âm thầm hạ assurance.
_BANG_LOP = (
    (".github/workflows/", "sensitive"),
    (".github/coordination/", "sensitive"),
    (".claude/dev/packet_loop.py", "sensitive"),
    (".claude/dev/launcher.py", "sensitive"),
    (".claude/dev/gate_lifecycle.py", "sensitive"),
    ("ops/lease_publish.py", "sensitive"),
    ("scripts/tl_gws.py", "sensitive"),
)

def GOI_GH(*doi_so):
    return subprocess.run(["gh", "api", *doi_so], capture_output=True, text=True)


def GOI_GIT(*doi_so, cwd=None):
    # Decode synchronously: Windows reader-thread exceptions otherwise escape
    # the consumer's UnicodeError handler and print an unrelated traceback.
    p = subprocess.run(["git", *doi_so], cwd=cwd, capture_output=True)
    p.stdout = p.stdout.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    p.stderr = p.stderr.decode("utf-8").replace("\r\n", "\n").replace("\r", "\n")
    return p


# Cùng danh sách với `.claude/dev/packet_loop.py`. Hai chỗ cưỡng chế CÙNG một luật
# ("không tự cấp lease") ở hai tầng khác nhau: một tầng cục bộ lúc chạy máy trạng
# thái, một tầng ở cửa đăng. Tầng nào thủng thì tầng kia còn đỡ.
#
# ĐÂY CHỈ LÀ DANH SÁCH CẤM, và một danh sách cấm KHÔNG BAO GIỜ ĐỦ. Giữ lại vì thông
# điệp của nó chỉ đúng tên bệnh ("agent tự ký cho mình"), nhưng thứ thật sự chặn là
# `NGUOI_CO_THAM_QUYEN` bên dưới.
PROVIDER_FAMILIES = {"claude": "claude", "codex": "openai", "google_antigravity": None}
PROVIDERS = tuple(PROVIDER_FAMILIES)
MODEL_FAMILIES = ("claude", "openai", "gemini")
RUNTIME_CAPABILITIES = {
    "claude": {"claude_code": ("machine/local",)},
    # machine/local là cách khai legacy của Codex CLI/Desktop; service chỉ nhận machine.
    "codex": {"codex_cli": ("machine", "machine/local"),
              "codex_desktop": ("machine", "machine/local"),
              "codex_service": ("machine",)},
    "google_antigravity": {"antigravity": ("machine/local",)},
    "human": {"manual_audit": ("human",)},
}


def _kiem_capability_khai(lease, provider, surface_key, transport_key, *, required=False):
    """Check only declared metadata, except AG paths that require a complete tuple."""
    surface = str(lease.get(surface_key) or "").strip()
    transport = str(lease.get(transport_key) or "").strip()
    if required and not (surface and transport):
        raise Chan(RC_NOI_DUNG, f"{provider} cần {surface_key} và {transport_key}")
    if (surface_key in lease and not surface) or (transport_key in lease and not transport):
        raise Chan(RC_NOI_DUNG, f"{provider} khai {surface_key}/{transport_key} rỗng")
    capabilities = RUNTIME_CAPABILITIES[provider]
    if surface and surface not in capabilities:
        raise Chan(RC_NOI_DUNG, f"{provider} không hỗ trợ {surface_key}={surface!r}")
    allowed = (capabilities[surface] if surface else
               {t for options in capabilities.values() for t in options})
    if transport and transport not in allowed:
        raise Chan(RC_NOI_DUNG, f"{provider} không hỗ trợ {transport_key}={transport!r}")


def _kiem_executor_khai_voi_human_reviewer(lease, executor):
    """Human audit requires AG identity; legacy Claude/Codex metadata stays optional."""
    family_key = "executor_model_family"
    surface_key = "executor_execution_surface"
    transport_key = "executor_transport"
    family = str(lease.get(family_key) or "").strip()
    if executor == "google_antigravity":
        if family not in MODEL_FAMILIES:
            raise Chan(RC_NOI_DUNG, "executor google_antigravity khai model_family thiếu hoặc sai")
        _kiem_capability_khai(lease, executor, surface_key, transport_key, required=True)
    elif family_key in lease and family != PROVIDER_FAMILIES.get(executor):
        raise Chan(RC_NOI_DUNG, f"executor_model_family không khớp provider {executor!r}")
    else:
        _kiem_capability_khai(lease, executor, surface_key, transport_key)


def _kiem_provider_identity(lease):
    """Validate declared runtime identity; legacy leases without identity remain valid."""
    # Historical full IDs name the same providers. Normalize only this validation
    # view: the recorded lease (and any serialized evidence) must keep its bytes.
    aliases = {"anthropic_claude": "claude", "openai_codex": "codex"}
    lease = dict(lease)
    for key in ("provider", "executor", "reviewer"):
        if key in lease:
            value = str(lease[key] or "").strip()
            lease[key] = aliases.get(value, value)
    role = str(lease.get("role") or "").strip()
    assurance = str(lease.get("assurance_target") or "").strip()
    # A missing legacy identity differs from an actor field explicitly declared blank.
    for key in ("provider", "executor"):
        if key in lease and not str(lease[key] or "").strip():
            raise Chan(RC_NOI_DUNG, f"{key} khai rỗng")
    provider = str(lease.get("provider") or lease.get("executor") or "").strip()
    if not provider:
        if assurance == "cross_approved" and role != "executor":
            raise Chan(RC_LOP, "lease khai cross_approved nhưng thiếu executor/reviewer identity hoặc model family")
        return
    if provider == "human":
        if role != "reviewer" or assurance not in ("human_audited", "cross_approved_or_human_audited"):
            raise Chan(RC_LOP, "human chỉ có thể là reviewer với human_audited")
        if str(lease.get("model_family") or "").strip():
            raise Chan(RC_NOI_DUNG, "human reviewer không có model_family")
        _kiem_capability_khai(lease, "human", "execution_surface", "transport")
        if lease.get("reviewer") and str(lease["reviewer"]).strip() != "human":
            raise Chan(RC_NOI_DUNG, "reviewer không khớp provider human")
        executor = str(lease.get("executor") or "").strip()
        if executor and executor not in PROVIDERS:
            raise Chan(RC_NOI_DUNG, f"executor không hợp lệ: {executor!r}")
        if not executor and any(key in lease for key in
                                ("executor_model_family", "executor_execution_surface", "executor_transport")):
            raise Chan(RC_NOI_DUNG, "executor metadata không có executor provider")
        if executor:
            _kiem_executor_khai_voi_human_reviewer(lease, executor)
        return
    if provider not in PROVIDERS:
        raise Chan(RC_NOI_DUNG, f"provider không hợp lệ: {provider!r}")
    if provider == "google_antigravity" and role not in ("executor", "reviewer"):
        raise Chan(RC_LOP, "google_antigravity chỉ giữ vai executor hoặc reviewer")
    declared_family = str(lease.get("model_family") or "").strip()
    surface = str(lease.get("execution_surface") or "").strip()
    transport = str(lease.get("transport") or "").strip()
    if provider == "google_antigravity" and not all((declared_family, surface, transport)):
        raise Chan(RC_NOI_DUNG, "google_antigravity cần model_family, execution_surface, transport")
    if declared_family and (declared_family not in MODEL_FAMILIES or
                            (PROVIDER_FAMILIES[provider] and declared_family != PROVIDER_FAMILIES[provider])):
        raise Chan(RC_NOI_DUNG, f"model_family không hợp lệ: {declared_family!r}")
    family = declared_family or PROVIDER_FAMILIES[provider]
    _kiem_capability_khai(lease, provider, "execution_surface", "transport",
                         required=provider == "google_antigravity")

    declared_executor_family = ""
    declared_reviewer_family = ""
    if role == "reviewer":
        executor = str(lease.get("executor") or "").strip()
        reviewer = provider
        declared_executor_family = str(lease.get("executor_model_family") or "").strip()
        if lease.get("reviewer") and str(lease["reviewer"]).strip() != reviewer:
            raise Chan(RC_NOI_DUNG, "reviewer không khớp provider của lease reviewer")
        executor_surface = str(lease.get("executor_execution_surface") or "").strip()
        executor_transport = str(lease.get("executor_transport") or "").strip()
        reviewer_family = family
        executor_family = declared_executor_family or PROVIDER_FAMILIES.get(executor)
        if executor in PROVIDERS:
            _kiem_capability_khai(lease, executor, "executor_execution_surface",
                                 "executor_transport", required=executor == "google_antigravity")
    else:
        if role == "executor" and "executor" in lease and str(lease["executor"]).strip() != provider:
            raise Chan(RC_NOI_DUNG, "executor không khớp provider của lease executor")
        executor = provider
        reviewer = str(lease.get("reviewer") or "").strip()
        executor_family = family
        declared_reviewer_family = str(lease.get("reviewer_model_family") or "").strip()
        reviewer_family = declared_reviewer_family or PROVIDER_FAMILIES.get(reviewer)
        reviewer_surface = str(lease.get("reviewer_execution_surface") or "").strip()
        reviewer_transport = str(lease.get("reviewer_transport") or "").strip()
        if reviewer == "google_antigravity" and not all((reviewer_family,
                                                           reviewer_surface, reviewer_transport)):
            raise Chan(RC_NOI_DUNG, "google_antigravity reviewer cần model_family, execution_surface, transport")
        if reviewer in RUNTIME_CAPABILITIES:
            _kiem_capability_khai(lease, reviewer, "reviewer_execution_surface",
                                 "reviewer_transport", required=reviewer == "google_antigravity")

    if executor and executor not in PROVIDERS:
        raise Chan(RC_NOI_DUNG, f"executor không hợp lệ: {executor!r}")
    if reviewer and reviewer not in PROVIDERS and reviewer != "human":
        raise Chan(RC_NOI_DUNG, f"reviewer không hợp lệ: {reviewer!r}")
    for actor, declared, effective in ((executor, declared_executor_family, executor_family),
                                        (reviewer, declared_reviewer_family, reviewer_family)):
        if actor == "human" and declared:
            raise Chan(RC_NOI_DUNG, "human reviewer không có model_family")
        if declared and (declared not in MODEL_FAMILIES or
                         (PROVIDER_FAMILIES.get(actor) and declared != PROVIDER_FAMILIES[actor])):
            raise Chan(RC_NOI_DUNG, f"model_family không khớp provider {actor!r}: {declared!r}")
        if actor == "google_antigravity" and not effective:
            raise Chan(RC_NOI_DUNG, "google_antigravity cần model_family")
    # An executor grant names a future assurance target, not an achieved review.
    # It may precede reviewer assignment; any explicitly assigned pair still
    # has to satisfy the declared cross-provider constraints below.
    strict_cross = assurance == "cross_approved" and (role != "executor" or bool(reviewer))
    claims_cross = "cross_approved" in assurance
    if assurance == "human_audited" and role != "executor" and reviewer != "human":
        raise Chan(RC_LOP, "human_audited đòi reviewer human")
    if strict_cross and not (executor and reviewer and executor_family and reviewer_family):
        raise Chan(RC_LOP, "lease khai cross_approved nhưng thiếu executor/reviewer identity hoặc model family")
    if strict_cross and (executor not in PROVIDERS or reviewer not in PROVIDERS):
        raise Chan(RC_LOP, "cross_approved đòi hai model provider, không nhận human")
    if claims_cross and reviewer and reviewer != "human" and (executor == reviewer or
                    (executor_family and reviewer_family and executor_family == reviewer_family)):
        raise Chan(RC_LOP, "reviewer cùng provider hoặc model family không đạt cross-review")

# CHỐT THẬT — danh sách CHO PHÉP, không phải danh sách cấm.
#
# Vì sao đổi: cross-review lượt 4 (codex, 14-08-2026) tìm ra `lease-authority-spoof`
# P1 — bản trước chỉ từ chối ĐÚNG hai chuỗi `claude`/`codex`, nên `codex-dispatcher`,
# `ai-codex-bot`, `cödex` đều lọt qua và tự cấp được lease. Nguyên văn kết luận:
# *"distinguishes spelling, not authority"* — phân biệt CÁCH VIẾT, không phân biệt
# THẨM QUYỀN. Lỗ không bị bịt, nó chỉ chuyển chỗ.
#
# Đắng hơn: prompt do chính phiên soạn ra cho reviewer LIỆT KÊ `"codex-dispatcher"`
# làm hướng tấn công số 1, rồi cổng này vẫn thua đúng ca đó. Nghĩ ra được phép thử
# mà không chạy nó thì phép thử ấy không tồn tại.
#
# Danh sách cấm phải đoán trước mọi cách viết của kẻ gian — thua từ trong thiết kế.
# Danh sách cho phép chỉ phải liệt kê những người CÓ thẩm quyền, một tập nhỏ và biết
# trước. Đây là một trong hai đường mà finding đề ra; đường kia là "thôi đừng khai nó
# chặn tự cấp nữa", và chúng ta chọn đường siết chứ không chọn đường hạ lời khai.
#
# NÓI THẲNG GIỚI HẠN, đừng để ai đọc rộng hơn thực tế: danh sách này chứng minh cái
# TÊN được phép cấp lease, KHÔNG chứng minh đúng người đó đã gõ. Thứ thật sự neo là
# (a) sửa danh sách này phải qua một commit có review, và (b) chốt `GITHUB_ACTOR`
# dưới đây — danh tính do GitHub xác thực, không phải chữ trong tệp YAML.
NGUOI_CO_THAM_QUYEN = ("ducthangho",)

BAT_BUOC = (
    "packet_issue",
    "lease_id",
    "granted_by",
    "lease_expires_at_utc",
    "reviewed_sha_required",
)

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")
REPO = re.compile(r"^[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+$")
LEASE_ID = re.compile(r"^[A-Za-z0-9._-]+$")

# Chỉ cấu trúc YAML này tạo tham chiếu có quyền chặn. Văn xuôi không mang ngữ nghĩa
# ấy; lệnh quét ngược chỉ báo nó như gợi ý sau khi parser đã loại comment.
_TRUONG_SCHEMA_LEASE = frozenset({"vung_duoc_phep_cham"})
_KHOA_THAM_CHIEU = "tham_chieu_truong_lease"


class Chan(Exception):
    def __init__(self, ma: int, thong_diep: str):
        super().__init__(thong_diep)
        self.ma = ma
        self.thong_diep = thong_diep


def _repr_an_toan(gia_tri, tran: int = 120) -> str:
    """`repr` cho THÔNG ĐIỆP chẩn đoán — KHÔNG BAO GIỜ ném, luôn có trần (review thi hành wp678 lượt 1).

    `repr()` thô của giá trị YAML hỏng ĐÃ ĐO sai hai cách: `int` vượt `sys.get_int_max_str_digits()` — YAML 1.1 dựng
    được qua `0x…`, `0b…`, `0…` hay lục thập phân mà `safe_load` KHÔNG ném — làm `repr()` ném `ValueError`, nên cửa
    "chỉ ném `Chan`" thành traceback rc=1; bí danh YAML lồng nhau nở theo cấp số nhân (tệp 591 byte ⇒ 2,79 triệu ký
    tự stderr). `reprlib` cắt theo cấu trúc; 3.11/3.12 vẫn ném ở `int` lớn nên phải bọc `try`.
    """
    import reprlib
    r = reprlib.Repr()
    r.maxlevel, r.maxlist, r.maxtuple, r.maxdict, r.maxset, r.maxstring, r.maxother, r.maxlong = 2, 4, 4, 4, 4, 60, 60, 40
    try:
        hien = r.repr(gia_tri)
    except Exception:  # noqa: BLE001 — đường chẩn đoán không được nổ
        hien = f"<{type(gia_tri).__name__} không in được>"
    return hien if len(hien) <= tran else hien[:tran] + "…"


def _nhan_lease_id_sai(gia_tri) -> str:
    """Nhãn chẩn đoán: `sai kiểu` (không phải `str`) khác `sai dạng` (`str` không khớp `LEASE_ID`), kèm repr có trần."""
    return f"{'sai dạng' if isinstance(gia_tri, str) else 'sai kiểu'} {_repr_an_toan(gia_tri)}"


def _lease_id_hop_le(gia_tri) -> str:
    """wp678 Q1/Q2 — cửa DUY NHẤT biến `lease_id` thô thành DANH TÍNH.

    Hợp lệ khi và chỉ khi giá trị là `str` NGAY SAU `yaml.safe_load` VÀ khớp `LEASE_ID`; mọi thứ
    khác ⇒ `Chan(RC_NOI_DUNG)`. KHÔNG `str()` lên giá trị thô: YAML 1.1 ép `yes`/`on` thành `True`,
    `0x1F`/`017`/`1_000` thành `int`, `1.50` thành `float`, `2026-09-29` thành `date`, nên ép về chuỗi
    là gộp nhiều cách viết khác nhau vào CÙNG một danh tính (`yes` và `on` cùng thành ``True``) —
    và danh tính ấy là thứ cổng đăng dùng để chống đăng trùng (bảng đo §1 đặc tả wp678). `int` cũng
    bị từ chối (Q1). Cách viết YAML khác nhau mà CHO RA cùng một chuỗi (`'yes'`, `!!str yes`) là
    cùng danh tính một cách CỐ Ý: danh tính là giá trị sau `safe_load`, không phải cú pháp.
    """
    if not isinstance(gia_tri, str) or not LEASE_ID.fullmatch(gia_tri):
        raise Chan(RC_NOI_DUNG,
                   f"lease_id phải là CHUỖI YAML chỉ chứa ASCII chữ/số/`.`/`_`/`-` (không ép kiểu); "
                   f"được {type(gia_tri).__name__} {_repr_an_toan(gia_tri)}")
    return gia_tri


def _lease_id_quet(gia_tri) -> str | None:
    """Bản KHÔNG ném của `_lease_id_hop_le` cho các đường QUÉT lease KHÁC (D5–D8, Q3).

    Sai kiểu ⇒ ``None``: KHÔNG khớp bất kỳ tên nào, và người gọi phải tự quyết fail-close (D7 in
    `KHÔNG_XÁC_ĐỊNH`). Cùng một luật với `_lease_id_hop_le` — gọi thẳng nó, không chép điều kiện.
    """
    try:
        return _lease_id_hop_le(gia_tri)
    except Chan:
        return None


def _khop_tien_to(duong: str, tien_to: str) -> bool:
    """Khớp một tệp chính xác hoặc một prefix thư mục có dấu `/` cuối."""
    return duong.startswith(tien_to) if tien_to.endswith("/") else duong == tien_to


def _tinh_lop_tu_write_set(write_set) -> str:
    """Tính lớp cao nhất; thiếu/rỗng/không đọc được đều fail-closed."""
    if not isinstance(write_set, list) or not write_set:
        return "sensitive"
    ket_qua = "routine"
    for muc in write_set:
        if not isinstance(muc, str) or not muc.strip():
            return "sensitive"
        duong = muc.strip()
        if duong.startswith("planned:"):
            duong = duong[len("planned:"):]
        # Chuẩn hoá traversal trước khi tra bảng; dạng không repo-relative vẫn
        # fail-closed, còn `planned:` hợp lệ dùng cùng một đường phân loại.
        if duong.startswith(("/", "./")) or "\\" in duong:
            return "sensitive"
        duong = posixpath.normpath(duong)
        if duong == ".." or duong.startswith("../"):
            return "sensitive"
        lop = next((gia_tri for tien_to, gia_tri in _BANG_LOP
                    if _khop_tien_to(duong, tien_to)), "sensitive")
        if _THU_TU_LOP[lop] > _THU_TU_LOP[ket_qua]:
            ket_qua = lop
    return ket_qua


def _kiem_lop_review(lease: dict) -> None:
    """Cưỡng chế lớp cho schema v2; dữ liệu cũ chỉ nhận cảnh báo có chủ ý."""
    raw_schema = lease.get("schema_version", 1)
    if isinstance(raw_schema, bool) or not isinstance(raw_schema, (int, str)):
        raise Chan(RC_LOP, f"schema_version hỏng: {raw_schema!r}")
    try:
        schema_version = int(raw_schema)
    except (TypeError, ValueError):
        raise Chan(RC_LOP, f"schema_version hỏng: {raw_schema!r}") from None
    if schema_version < 2:
        moc = str(lease.get("leased_at_utc") or "").strip()
        if moc:
            try:
                luc = datetime.fromisoformat(moc.replace("Z", "+00:00"))
                if luc.tzinfo and luc.astimezone(timezone.utc) > datetime(
                        2026, 8, 21, tzinfo=timezone.utc):
                    print("CẢNH BÁO: lease sau 2026-08-21 vẫn dùng schema_version < 2; "
                          "chốt lớp review chưa áp dụng", file=sys.stderr)
            except ValueError:
                pass  # Timestamp chưa có chốt riêng; mục D mới sở hữu việc đó.
        return

    role = str(lease.get("role") or "").strip().lower()
    khai = str(lease.get("review_class") or "").strip().lower()
    hieu_luc = str(lease.get("effective_review_class") or "").strip().lower()
    if role == "reviewer":
        can = "sensitive"
    elif role == "executor":
        tinh = _tinh_lop_tu_write_set(lease.get("write_set"))
        can = max((khai if khai in _THU_TU_LOP else "sensitive", tinh),
                  key=_THU_TU_LOP.get)
    else:
        can = "sensitive"
    if hieu_luc != can:
        raise Chan(RC_LOP,
                   f"effective_review_class={hieu_luc or '<thiếu>'!r} không bằng lớp "
                   f"cổng tính được {can!r} cho role={role or '<thiếu>'!r}")


def _doc_yaml(duong_dan: str) -> dict:
    p = Path(duong_dan)
    if not p.is_file():
        raise Chan(RC_THAM_SO, f"không thấy tệp lease: {duong_dan}")
    try:
        import yaml
    except ImportError:  # pragma: no cover - môi trường thiếu pyyaml
        raise Chan(RC_THAM_SO, "thiếu PyYAML — `pip install pyyaml`") from None
    try:
        d = yaml.safe_load(p.read_text(encoding="utf-8"))
    except Exception as e:  # YAMLError và cả lỗi decode
        # KHÔNG để traceback thô rơi ra ngoài: workflow đọc stderr, và một cái
        # traceback dài che mất dòng nói lý do thật.
        raise Chan(RC_NOI_DUNG, f"YAML hỏng, không đọc được: {str(e).splitlines()[0][:200]}") from None
    if not isinstance(d, dict):
        raise Chan(RC_NOI_DUNG, f"lease phải là một ánh xạ YAML, đọc ra {type(d).__name__}")
    return d


def _doc_han(chuoi) -> datetime:
    s = str(chuoi or "").strip()
    if not s:
        raise Chan(RC_NOI_DUNG, "lease_expires_at_utc rỗng")
    try:
        d = datetime.fromisoformat(s.replace("Z", "+00:00"))
    except ValueError:
        raise Chan(RC_NOI_DUNG,
                   f"lease_expires_at_utc không đọc được: {s!r} "
                   f"(cần ISO8601, ví dụ 2026-08-14T07:00:00Z)") from None
    if d.tzinfo is None:
        # "hết hạn 18:30" mà không nói múi là hai mốc cách nhau tới 26 giờ. Một
        # lease lệch 26 giờ thì cái hạn chỉ còn là trang trí.
        raise Chan(RC_NOI_DUNG, f"lease_expires_at_utc phải kèm múi giờ (thêm 'Z'): {s!r}")
    return d.astimezone(timezone.utc)


def _cac_con_tro_treo(lease: dict) -> list[str]:
    """Tham chiếu khai máy-đọc-được nhưng thiếu định nghĩa top-level."""
    tham_chieu = lease.get(_KHOA_THAM_CHIEU, [])
    if not isinstance(tham_chieu, list) or any(
            not isinstance(x, str) or not x for x in tham_chieu):
        raise Chan(RC_NOI_DUNG, f"{_KHOA_THAM_CHIEU} phải là danh sách tên trường")
    la = set(tham_chieu)
    khong_biet = la - _TRUONG_SCHEMA_LEASE
    if khong_biet:
        raise Chan(RC_NOI_DUNG, "tham chiếu trường lease không thuộc schema: " +
                   ", ".join(sorted(khong_biet)))
    return sorted(la - lease.keys())


def _kiem_con_tro_treo(lease: dict) -> None:
    treo = _cac_con_tro_treo(lease)
    if treo:
        raise Chan(RC_NOI_DUNG,
                   "con trỏ treo: tham chiếu khai trong cấu trúc nhưng thiếu định nghĩa: " +
                   ", ".join(treo))


def _cac_nhac_mo_ho(lease: dict) -> list[str]:
    """Tên trường trong scalar YAML; chỉ advisory, không tham gia cổng đăng."""
    def scalar(x):
        if isinstance(x, dict):
            for k, v in x.items():
                if k != _KHOA_THAM_CHIEU:
                    yield from scalar(v)
        elif isinstance(x, list):
            for v in x:
                yield from scalar(v)
        elif isinstance(x, str):
            yield x

    van = "\n".join(scalar(lease))
    van = "".join(c for c in unicodedata.normalize("NFD", van).casefold()
                  if unicodedata.category(c) != "Mn").replace("đ", "d")
    return sorted(ten for ten in _TRUONG_SCHEMA_LEASE if ten not in lease and
                  re.search(rf"(?<![a-z0-9_]){re.escape(ten)}(?![a-z0-9_])", van))


def _git(goc: Path, *doi_so) -> str:
    try:
        p = GOI_GIT(*doi_so, cwd=goc)
    except OSError as e:
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: không gọi được git: {e}") from None
    if p.returncode != 0:
        ly = (p.stderr or p.stdout or "không có chẩn đoán").strip().splitlines()[0][:200]
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: git {' '.join(doi_so)} rc={p.returncode}: {ly}")
    return p.stdout


def _ten_nhanh_may_chu(goc: Path) -> set[str]:
    out = _git(goc, "ls-remote", "--heads", "origin")
    ket_qua = set()
    for dong in out.splitlines():
        cot = dong.split()
        if len(cot) != 2 or not cot[1].startswith("refs/heads/"):
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: ls-remote có dòng hỏng: {dong!r}")
        ket_qua.add(cot[1][len("refs/heads/"):])
    return ket_qua


def _cac_ref_cuc_bo(goc: Path) -> tuple[set[str], list[str]]:
    out = _git(goc, "for-each-ref", "--format=%(refname)", "refs/heads", "refs/remotes")
    ten_nhanh, refs = set(), []
    for ref in out.splitlines():
        ref = ref.strip()
        if not ref or ref.endswith("/HEAD"):
            continue
        refs.append(ref)
        if ref.startswith("refs/heads/"):
            ten_nhanh.add(ref[len("refs/heads/"):])
        elif ref.startswith("refs/remotes/origin/"):
            ten_nhanh.add(ref[len("refs/remotes/origin/"):])
    return ten_nhanh, refs


def _doc_cau_hinh_git(goc: Path) -> dict[str, list[str]]:
    """Đọc config cùng giá trị mà không nhập nhằng khoảng trắng hay dòng mới."""
    out, ket_qua = _git(goc, "config", "--includes", "--null", "--list"), {}
    for muc in out.split("\0"):
        if not muc:
            continue
        khoa, co_ngan, gia_tri = muc.partition("\n")
        if not co_ngan or not khoa:
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: git config trả mục hỏng: {muc!r}")
        ket_qua.setdefault(khoa, []).append(gia_tri)
    return ket_qua


def _ref_ton_tai(goc: Path, ref: str) -> bool:
    """Hỏi Git về tồn tại; không dùng tập ref thuộc phạm vi quét lease."""
    try:
        # check-ref-format không hỗ trợ option terminator: cả `--` lẫn
        # `--end-of-options` đều rc=129, kể cả với ref hợp lệ. Chặn
        # dấu `-` từ Python để Git không thể hiểu ref thành option.
        if ref.startswith("-"):
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: ref có hình dạng không an toàn "
                       f"(bắt đầu bằng '-'): {ref}")
        hinh_dang = GOI_GIT("check-ref-format", ref, cwd=goc)
        if hinh_dang.returncode != 0:
            ly = (hinh_dang.stderr or hinh_dang.stdout or "refname không hợp lệ").strip()
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: git check-ref-format {ref} "
                       f"rc={hinh_dang.returncode}: {ly.splitlines()[0][:200]}")
        p = GOI_GIT("show-ref", "--verify", "--quiet", "--", ref, cwd=goc)
    except OSError as e:
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: không gọi được git: {e}") from None
    if p.returncode == 0:
        return True
    if p.returncode == 1:
        return False
    ly = (p.stderr or p.stdout or "không có chẩn đoán").strip().splitlines()[0][:200]
    raise Chan(RC_KHONG_XAC_DINH,
               f"KHÔNG_XÁC_ĐỊNH: git show-ref --verify {ref} rc={p.returncode}: {ly}")


def _nhanh_cuc_bo_tut_sau(goc: Path, refs: list[str]) -> list[tuple[str, str, int, int, str]]:
    """Phân loại nhánh theo upstream thật; chỉ trả các quan hệ phải chặn."""
    out = _git(goc, "for-each-ref", "--format=%(refname)%09%(upstream)", "refs/heads")
    upstream = {}
    for dong in out.splitlines():
        cot = dong.split("\t")
        if len(cot) != 2 or not cot[0].startswith("refs/heads/"):
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: upstream có dòng hỏng: {dong!r}")
        upstream[cot[0]] = cot[1]
    tap_ref, tut_sau, cau_hinh = set(refs), [], _doc_cau_hinh_git(goc)
    for ref in sorted(x for x in tap_ref if x.startswith("refs/heads/")):
        ten = ref.removeprefix("refs/heads/")
        doi_ung = upstream.get(ref, "")
        ds_remote = cau_hinh.get(f"branch.{ten}.remote")
        ds_merge = cau_hinh.get(f"branch.{ten}.merge")
        remote = ds_remote[-1] if ds_remote else None
        merge = ds_merge[-1] if ds_merge else None
        co_cau_hinh = ds_remote is not None or ds_merge is not None
        if co_cau_hinh and not doi_ung:
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: {ten} có config upstream nhưng không giải được: "
                       f"branch.{ten}.remote={remote!r}, branch.{ten}.merge={merge!r}")
        if not doi_ung:
            ung_vien = "refs/remotes/origin/" + ten
            if ung_vien in tap_ref:
                doi_ung = ung_vien
        if doi_ung and not _ref_ton_tai(goc, doi_ung):
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: {ten} khai upstream không có ref: {doi_ung}")
        if not doi_ung:
            continue
        out = _git(goc, "rev-list", "--left-right", "--count", f"{ref}...{doi_ung}")
        try:
            trai, phai = (int(x) for x in out.split())
        except ValueError:
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: rev-list trả kết quả hỏng cho {ten}: {out!r}") from None
        if trai == 0 and phai > 0:
            trang_thai = "TỤT_SAU"
        elif trai > 0 and phai > 0:
            trang_thai = "PHÂN_KỲ"
        elif trai == 0 and phai == 0:
            trang_thai = "BẰNG"
        elif trai > 0 and phai == 0:
            trang_thai = "ĐI_TRƯỚC"
        else:
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: quan hệ ref không hợp lệ cho {ten}: {trai}/{phai}")
        if trang_thai in {"TỤT_SAU", "PHÂN_KỲ"}:
            tut_sau.append((ten, doi_ung, trai, phai, trang_thai))
    return tut_sau


def _thong_tin_nhanh_bi_chan(muc) -> tuple[str, str, int, int, str]:
    """Chuẩn hoá bản ghi; dạng chuỗi chỉ giữ tương thích cho phản chứng legacy."""
    if isinstance(muc, str):
        return muc, "refs/remotes/origin/" + muc, 0, 1, "TỤT_SAU"
    return muc


def _cac_worktree(goc: Path) -> list[dict]:
    out = _git(goc, "worktree", "list", "--porcelain", "-z")
    ds = [dict(x.partition(" ")[::2] for x in khoi.split("\0") if x) for khoi in out.rstrip("\0").split("\0\0") if khoi]
    for muc in ds:
        p = Path(muc["worktree"])
        if not p.exists() or "bare" in muc: continue
        gd = Path(_git(p, "rev-parse", "--git-dir").strip())
        muc["_gitdir"] = gd if gd.is_absolute() else p / gd
        if "branch" not in muc:
            for ten in ("rebase-merge/head-name", "rebase-apply/head-name", "BISECT_START"):
                q = muc["_gitdir"] / ten
                if q.is_file():
                    ref = q.read_text(encoding="utf-8").strip()
                    muc["branch"] = ref if ref.startswith("refs/") else "refs/heads/" + ref
                    break
    return ds
def _trang_thai_worktree(muc: dict) -> list[str]:
    p, trang = Path(muc["worktree"]), []
    if "prunable" in muc: return ["PRUNABLE"]
    if not p.exists(): return ["ĐƯỜNG_DẪN_KHÔNG_TỒN_TẠI"]
    if "bare" in muc: return ["BARE"]
    try:
        meta = {x.name for x in muc["_gitdir"].iterdir()}
    except OSError:
        return ["METADATA_KHÔNG_ĐỌC_ĐƯỢC"]
    trang = [nhan for nhan, ten in (("MERGE", "MERGE_HEAD"), ("REBASE", "rebase-merge"),
             ("REBASE", "rebase-apply"), ("CHERRY-PICK", "CHERRY_PICK_HEAD"),
             ("BISECT", "BISECT_START")) if ten in meta]
    if _git(p, "status", "--porcelain").strip(): trang.append("BẨN")
    return sorted(set(trang))
def _lenh_chua_nhanh_tut_sau(goc: Path, tut_sau: list[str]) -> str:
    worktrees, lenh, chi_tiet, an_toan = _cac_worktree(goc), [], [], True
    for muc in tut_sau:
        ten, doi_ung, _, _, _ = _thong_tin_nhanh_bi_chan(muc)
        ref = "refs/heads/" + ten
        giu = [wt for wt in worktrees if wt.get("branch") == ref]
        if not giu:
            lenh.append(f"git branch -f {shlex.quote(ten)} {shlex.quote(doi_ung)}")
            chi_tiet.append(f"{ten}: KHÔNG_BỊ_WORKTREE_NÀO_GIỮ")
        else:
            lenh.append(f"git -C {shlex.quote(giu[0]['worktree'])} merge --ff-only {shlex.quote(doi_ung)}")
            trang = [(wt, _trang_thai_worktree(wt)) for wt in giu]
            mo_ta = "; ".join(f"{wt['worktree']} [{'+'.join(tt or ['SẠCH', 'RẢNH'])}]" for wt, tt in trang)
            chi_tiet.append(f"{ten}: GIỮ_BỞI_{len(giu)}_WORKTREE; {mo_ta}")
            if len(giu) != 1 or trang[0][1]: an_toan = False
    if not an_toan:
        return ("KHÔNG_PHÁT_LỆNH_CHỮA. " + " | ".join(chi_tiet) + ". Người dùng tự "
                "commit/stash, hoàn tất hoặc huỷ thao tác dở, dọn entry stale, detach bớt worktree, rồi chạy lại cổng.")
    return "chữa: " + "; ".join(lenh)


def _quet_lease_toan_kho(goc: Path, *, doi_chieu_ref=True,
                         chan_nhanh_tut_sau=False) -> list[dict]:
    """Đọc mỗi cặp (blob, đường dẫn) lease đúng một lần trên mọi ref cục bộ."""
    ten_cuc_bo, refs = _cac_ref_cuc_bo(goc)
    if chan_nhanh_tut_sau:
        bi_chan = _nhanh_cuc_bo_tut_sau(goc, refs)
        if bi_chan:
            tut_sau = [m for m in bi_chan if _thong_tin_nhanh_bi_chan(m)[-1] == "TỤT_SAU"]
            phan_ky = [m for m in bi_chan if _thong_tin_nhanh_bi_chan(m)[-1] == "PHÂN_KỲ"]
            chi_tiet = []
            if tut_sau:
                mo_ta = ", ".join(f"{ten} -> {doi_ung} ({trai}/{phai})"
                                   for ten, doi_ung, trai, phai, _ in
                                   map(_thong_tin_nhanh_bi_chan, tut_sau))
                chi_tiet.append("NHÁNH_CỤC_BỘ_TỤT_SAU: " + mo_ta +
                                ". ai-dang-giu quét refs/heads/*; " +
                                _lenh_chua_nhanh_tut_sau(goc, tut_sau))
            if phan_ky:
                mo_ta = ", ".join(f"{ten} -> {doi_ung} ({trai}/{phai})"
                                   for ten, doi_ung, trai, phai, _ in
                                   map(_thong_tin_nhanh_bi_chan, phan_ky))
                chi_tiet.append("NHÁNH_CỤC_BỘ_PHÂN_KỲ: " + mo_ta +
                                ". KHÔNG_PHÁT_LỆNH_CHỮA; người dùng tự quyết cách hợp nhất hoặc giữ commit.")
            raise Chan(RC_KHONG_XAC_DINH,
                       " | ".join(chi_tiet))
    if doi_chieu_ref:
        thieu = _ten_nhanh_may_chu(goc) - ten_cuc_bo
        if thieu:
            raise Chan(RC_KHONG_XAC_DINH,
                       "KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy chủ: " + ", ".join(sorted(thieu)))
    da_doc, ket_qua = set(), []
    try:
        import yaml
    except ImportError:
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: thiếu PyYAML") from None
    for ref in refs:
        out = _git(goc, "ls-tree", "-r", ref, "--", "ops/leases")
        for dong in out.splitlines():
            try:
                meta, duong = dong.split("\t", 1)
                _, loai, blob = meta.split()
            except ValueError:
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: ls-tree có dòng hỏng: {dong!r}") from None
            if loai != "blob" or not duong.endswith((".yaml", ".yml")):
                continue
            khoa = (blob, duong)
            if khoa in da_doc:
                continue
            da_doc.add(khoa)
            try:
                noi_dung = _git(goc, "cat-file", "-p", blob)
                lease = yaml.safe_load(noi_dung)
            except Exception as e:
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: YAML hỏng tại {ref}:{duong}: {e}") from None
            if not isinstance(lease, dict):
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: lease không phải ánh xạ tại {ref}:{duong}")
            ket_qua.append({"lease": lease, "blob": blob, "path": duong, "ref": ref})
    return ket_qua


def _lease_cham_duong(lease: dict, duong: str) -> bool:
    write_set = lease.get("write_set")
    return isinstance(write_set, list) and any(
        isinstance(x, str) and x.strip().removeprefix("planned:") == duong
        for x in write_set)


def _phan_loai_lease(lease: dict, bay_gio=None) -> str:
    try:
        han = _doc_han(lease.get("lease_expires_at_utc"))
    except Chan as e:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {e.thong_diep}") from None
    bay_gio = bay_gio or datetime.now(timezone.utc)
    return "HẾT_HẠN" if han <= bay_gio else "CÒN_HẠN"


def _danh_sach_thay_the_cho(gia_tri) -> list[str] | None:
    """Chuẩn hoá schema cũ chuỗi và schema mới danh sách; ``None`` là sai kiểu."""
    if gia_tri in (None, ""):
        return []
    if isinstance(gia_tri, str):
        ten = gia_tri.strip()
        return [ten] if ten else []
    if isinstance(gia_tri, list):
        if any(not isinstance(x, str) or not x.strip() for x in gia_tri):
            return None
        return [x.strip() for x in gia_tri]
    return None


def _bia_mo_doi_xung(lease: dict, cac_lease: list[dict]) -> bool | None:
    """Trả ``None`` nếu không có bia mộ, còn lại xác nhận CŨ→MỚI và MỚI→CŨ.

    Chỉ lập chỉ mục phẳng và so tên lease bằng nhau tuyệt đối. Không lần theo bia mộ
    kế tiếp, nên một vòng A→B→A luôn kết thúc sau đúng một lượt quét.
    """
    raw_moi = lease.get("da_bi_thay_the")
    if raw_moi in (None, ""):
        return None
    if not isinstance(raw_moi, str) or not raw_moi.strip():
        return False
    lease_moi = raw_moi.strip()
    # wp678 D5 (Q3): `lease_id` sai kiểu KHÔNG ép sang chuỗi để so — nó không khớp tên nào.
    lease_cu = _lease_id_quet(lease.get("lease_id"))
    if lease_cu is None:
        return False
    for muc in cac_lease:
        ban_moi = muc["lease"]
        if _lease_id_quet(ban_moi.get("lease_id")) != lease_moi:
            continue
        thay_the_cho = _danh_sach_thay_the_cho(ban_moi.get("thay_the_cho"))
        if thay_the_cho is not None and lease_cu in thay_the_cho:
            return True
    return False


def _kiem_bia_mo(lease: dict, tep, goc=None) -> None:
    """Lease mới chỉ được thay mọi X sau khi từng X trỏ ngược đúng lease mới."""
    # wp678 D6: chốt RIÊNG cho lease đang kiểm — không dựa vào việc `kiem()` đã chạy D1 trước.
    lease_moi = _lease_id_hop_le(lease.get("lease_id"))
    thay_the_cho = _danh_sach_thay_the_cho(lease.get("thay_the_cho"))
    if thay_the_cho is None:
        raise Chan(RC_NOI_DUNG,
                   "thay_the_cho phải là một tên lease hoặc danh sách các tên lease hợp lệ")
    if not thay_the_cho:
        return
    root = _goc_kho(Path(tep), goc)
    cac_lease = _quet_lease_toan_kho(root, doi_chieu_ref=False)
    # Lease cũ được QUÉT mang `lease_id` sai kiểu thì không khớp tên nào (Q3) ⇒ bia mộ trỏ tới nó không thoả.
    chua_danh_dau = [ten for ten in thay_the_cho if not any(
        _lease_id_quet(muc["lease"].get("lease_id")) == ten
        and isinstance(muc["lease"].get("da_bi_thay_the"), str)
        and muc["lease"]["da_bi_thay_the"].strip() == lease_moi
        for muc in cac_lease)]
    if chua_danh_dau:
        raise Chan(RC_NOI_DUNG,
                   f"lease mới thay_the_cho={thay_the_cho!r}, nhưng lease cũ "
                   f"{chua_danh_dau!r} chưa "
                   f"mang dòng `da_bi_thay_the: {lease_moi}`; hãy thêm dòng ấy vào "
                   f"từng lease còn thiếu trước khi đăng lease mới "
                   f"(cổng không tự sửa hồ sơ cũ)")


def _doc_gh(mo_ta: str, *doi_so):
    """Gọi `gh api` và trả JSON; mọi trạng thái không đo được đều CHẶN."""
    try:
        p = GOI_GH(*doi_so)
    except OSError as e:
        raise Chan(RC_NOI_DUNG, f"KHÔNG ĐO ĐƯỢC {mo_ta}: không gọi được `gh api`: {e}") from None
    if p.returncode != 0:
        ly = (p.stderr or p.stdout or "không có chẩn đoán").strip().splitlines()[0][:200]
        raise Chan(RC_NOI_DUNG,
                   f"KHÔNG ĐO ĐƯỢC {mo_ta}: `gh api` rc={p.returncode}: {ly}")
    try:
        return json.loads(p.stdout)
    except (TypeError, json.JSONDecodeError):
        raise Chan(RC_NOI_DUNG, f"KHÔNG ĐO ĐƯỢC {mo_ta}: `gh api` không trả JSON hợp lệ") from None


def _repo_github() -> str:
    repo = (os.environ.get("GITHUB_REPOSITORY") or "").strip()
    if not REPO.fullmatch(repo):
        raise Chan(RC_NOI_DUNG, f"KHÔNG ĐO ĐƯỢC repository từ GITHUB_REPOSITORY={repo!r}")
    return repo


def _kiem_loai_so_hieu(repo: str, so: int) -> None:
    try:
        d = _doc_gh("loại số hiệu", f"repos/{repo}/issues/{so}")
    except Chan as e:
        raise Chan(e.ma, f"{e.thong_diep}; số hiệu trỏ vào PR là một nguyên nhân có thể — "
                   "đây là phỏng đoán, không phải phép đo") from None
    if not isinstance(d, dict) or not isinstance(d.get("html_url"), str):
        raise Chan(RC_NOI_DUNG,
                   "KHÔNG ĐO ĐƯỢC loại số hiệu: phản hồi thiếu `html_url`")
    path = urlparse(d["html_url"]).path.rstrip("/")
    if path.endswith(f"/pull/{so}"):
        raise Chan(RC_NOI_DUNG,
                   f"packet_issue #{so} là Pull Request — workflow cố ý không có "
                   "`pull-requests: write`; quy ước bắt buộc trỏ tới Issue")
    if not path.endswith(f"/issues/{so}"):
        raise Chan(RC_NOI_DUNG,
                   f"KHÔNG ĐO ĐƯỢC loại số hiệu từ html_url={d['html_url']!r}")


def _kiem_comment_da_co(repo: str, lease: dict) -> None:
    # wp678 D3: chốt RIÊNG, TRƯỚC `_doc_gh` — `str(True)` từng cho ``**Lease `True`**`` khớp dấu của
    # một lease KHÁC (`yes` ↔ `on`) ⇒ rc=9, lease mới không bao giờ được đăng.
    so, lease_id = lease["packet_issue"], _lease_id_hop_le(lease.get("lease_id"))
    cac_trang = _doc_gh("comment hiện có", "--paginate", "--slurp",
                        f"repos/{repo}/issues/{so}/comments")
    if not isinstance(cac_trang, list):
        raise Chan(RC_NOI_DUNG,
                   "KHÔNG ĐO ĐƯỢC comment hiện có: phản hồi không phải danh sách")
    if not cac_trang:
        raise Chan(RC_NOI_DUNG, "KHÔNG ĐO ĐƯỢC comment hiện có: `--slurp` không trả trang nào")
    if all(isinstance(x, dict) for x in cac_trang):
        comments = cac_trang
    elif all(isinstance(x, list) for x in cac_trang):
        comments = [x for trang in cac_trang for x in trang]
    else:
        raise Chan(RC_NOI_DUNG,
                   "KHÔNG ĐO ĐƯỢC comment hiện có: cấu trúc phân trang lẫn kiểu")
    dau = f"**Lease `{lease_id}`**"
    for comment in comments:
        if not isinstance(comment, dict) or not isinstance(comment.get("body"), str):
            raise Chan(RC_NOI_DUNG, "KHÔNG ĐO ĐƯỢC comment hiện có: phần tử thiếu `body`")
        user = comment.get("user")
        if not isinstance(user, dict) or not isinstance(user.get("login"), str):
            raise Chan(RC_NOI_DUNG, "KHÔNG ĐO ĐƯỢC comment hiện có: phần tử thiếu `user.login`")
        if user["login"] == "github-actions[bot]" and comment["body"].startswith(dau):
            raise Chan(RC_DA_DANG,
                       f"lease {lease_id!r} đã có comment {comment.get('id', '<không id>')} "
                       f"trên issue #{so} — bỏ qua")


def _goc_kho(tep: Path, goc) -> Path:
    """Thư mục mà `prompt_path` được tính từ đó.

    `prompt_path` viết theo gốc KHO (`ops/prompts/…`) chứ không theo thư mục chứa
    lease, vì người đọc lease cần dán đúng đường dẫn ấy vào `sha256sum` ở gốc kho.
    Nên phải tìm được gốc: đi ngược từ tệp lease lên tới thư mục có `.git`.
    `.git` có thể là THƯ MỤC (clone thường) hoặc TỆP (worktree/submodule) — dùng
    `.exists()` chứ không `.is_dir()`, nếu không thì mọi lượt chạy trong worktree
    sẽ rơi về CWD và tính sai đường dẫn.
    """
    if goc:
        return Path(goc).resolve()
    p = tep.resolve().parent
    for d in (p, *p.parents):
        if (d / ".git").exists():
            return d
    # Không thấy `.git` (tệp lease nằm ngoài kho, hoặc cây đã bị tháo): rơi về CWD
    # — workflow luôn chạy ở gốc kho nên đây là mặc định đúng cho đường thật.
    return Path.cwd().resolve()


def _kiem_neo_prompt(lease: dict, tep: Path, goc) -> str:
    """Prompt mà lease neo phải TỒN TẠI và ĐÚNG BĂM.

    Vì sao có chốt này — đã trả giá: lease #3 của wp55 ghi
    `prompt_sha256_required: 46a833cc…` mà KHÔNG nói băm cái gì, và không văn bản
    nào ứng với con băm đó. Cổng `--expected-prompt-sha256` phía reviewer vì thế
    không ai qua được, mà nó hỏng IM LẶNG: lease hợp lệ, hạn còn, chỉ thiếu đúng
    cái vật nó trỏ tới. wp55 đứng im hai ngày.

    Một con băm không kèm địa chỉ thì không kiểm được — nó chỉ là niềm tin viết
    dưới dạng hex. Nên hai trường đi THÀNH ĐÔI: có cái này phải có cái kia.
    """
    sha_khai = str(lease.get("prompt_sha256_required") or "").strip()
    duong = str(lease.get("prompt_path") or "").strip()
    if not sha_khai and not duong:
        return ""   # lease không neo prompt — không phải việc của chốt này

    # Nửa vời là dạng nguy hiểm nhất, và cả HAI chiều đều nguy hiểm: băm không địa
    # chỉ thì không kiểm được (đúng ca đã trả giá), còn địa chỉ không băm thì tệp
    # đổi lúc nào cũng không ai biết. Bỏ một trong hai là gỡ chốt.
    if not duong:
        raise Chan(RC_NEO,
                   "có `prompt_sha256_required` mà thiếu `prompt_path` — một con băm "
                   "không kèm địa chỉ thì không ai kiểm được nó nói về cái gì "
                   "(đúng lỗi đã chặn wp55 hai ngày)")
    if not sha_khai:
        raise Chan(RC_NEO,
                   "có `prompt_path` mà thiếu `prompt_sha256_required` — trỏ vào một "
                   "tệp không neo băm thì tệp đổi lúc nào cũng không ai biết")
    # ĐO RỒI MỚI VIẾT CÂU NÀY: chốt dạng này KHÔNG bắt thêm ca nào mà chốt so băm
    # bên dưới không bắt — băm sai dạng thì cũng khác băm thật, nên vẫn chặn. Giữ
    # lại VÌ THÔNG ĐIỆP: "phải là 64 ký tự hex" chỉ thẳng lỗi gõ, còn "băm LỆCH"
    # đẩy người sửa đi băm lại một tệp vốn không có lỗi. Cả sự cố hai ngày vừa rồi
    # là chuyện cổng chặn đúng mà nói sai chỗ. Phản chứng vì thế neo THÔNG ĐIỆP,
    # không chỉ neo mã thoát — bỏ chốt này là t20 đỏ.
    if not SHA256.match(sha_khai):
        raise Chan(RC_NEO,
                   f"prompt_sha256_required phải là 64 ký tự hex thường, được {sha_khai!r}")

    # `prompt_path` là dữ liệu trong tệp YAML mà lại thành một lượt ĐỌC ĐĨA. Chặn
    # đường vượt ra ngoài kho TRƯỚC khi chạm hệ tệp: tuyệt đối, `..`, và cả dấu `\`
    # (trên Linux `\` là ký tự tên tệp hợp lệ nên `PurePosixPath` KHÔNG coi nó là
    # dấu phân cách — một `..\..\x` sẽ lọt qua vòng kiểm `parts` nếu không bắt riêng).
    # Lớp này CHỒNG với `relative_to` bên dưới, và đã đo: bỏ nó đi thì mọi ca vẫn
    # bị chặn, chỉ khác thông điệp. Giữ vì hai lẽ — chặn trước khi đụng đĩa, và nói
    # đúng tên lỗi. Đừng tưởng nó là lớp phòng thủ độc lập: lớp THẬT là `relative_to`.
    pp = PurePosixPath(duong)
    if pp.is_absolute() or "\\" in duong or any(x == ".." for x in pp.parts):
        raise Chan(RC_NEO,
                   f"prompt_path phải là đường dẫn tương đối trong kho, được {duong!r}")

    root = _goc_kho(tep, goc)
    f = (root / pp).resolve()
    try:
        # Sau `resolve()` nên symlink trỏ ra ngoài cũng bị bắt ở đây, không chỉ `..`.
        f.relative_to(root)
    except ValueError:
        raise Chan(RC_NEO,
                   f"prompt_path trỏ ra ngoài kho: {duong!r} → {f}") from None
    if not f.is_file():
        raise Chan(RC_NEO,
                   f"prompt_path {duong!r} không có tệp (tìm ở {f}) — lease neo một "
                   f"vật không tồn tại thì reviewer không bao giờ qua được cổng")

    # Đọc BYTE, không đọc văn bản: `read_text` sẽ chuẩn hoá xuống dòng trên Windows
    # nên cùng một tệp cho hai băm khác nhau tuỳ nền — đúng loại lệch mà chốt này
    # sinh ra để bắt.
    thuc = hashlib.sha256(f.read_bytes()).hexdigest()
    if thuc != sha_khai:
        raise Chan(RC_NEO,
                   f"băm prompt LỆCH: lease khai {sha_khai}, tệp {duong!r} thực tế là "
                   f"{thuc} ({f.stat().st_size} byte)")
    return thuc


def kiem(lease: dict, tep=None, goc=None, bo_qua_han: bool = False) -> tuple:
    """Kiểm thuần và trả `(lease, băm prompt)`; ném `Chan` nếu không hợp lệ.

    Trả kèm cái băm chứ không trả mỗi lease, để dòng "prompt … khớp băm" mà `check`
    in ra là BẰNG CHỨNG chứ không phải lời khen. Bản trước in dòng đó chỉ vì lease
    có trường `prompt_path` — nghĩa là gỡ hẳn chốt kiểm băm đi thì nó vẫn in y
    nguyên. Một dòng xác nhận không đi kèm việc kiểm là thứ tệ hơn im lặng.
    """
    # ĐÁNH ĐỔI ĐÃ KHAI (packet #396): hai chốt idempotent chạy ĐƯỢC OFFLINE — một
    # trong tệp, một XUYÊN NHÁNH — đã bị gỡ cùng đường ghi ngược sinh ra chúng.
    # Chống lặp nay chỉ còn `_kiem_comment_da_co`: ONLINE, một lớp, và FAIL-CLOSE.
    # An toàn hơn về tính đúng, YẾU hơn về tính sẵn sàng — mất mạng là không đăng
    # được lease. Đừng mô tả nó như thay thế tương đương; nó không phải.
    #
    # VÀ MẤT MỘT THỨ NỮA, tách riêng vì nó KHÁC hẳn "mất mạng thì chờ" (cross-review
    # codex 29-08-2026): dấu "đã đăng" nay là HIỆN VẬT SỬA ĐƯỢC, sống trong CSDL Issue
    # chứ không trong git.
    #
    # Khai bằng VỊ TỪ, và CHỈ vị từ. Bản trước liệt kê thêm bốn "hệ quả" cho dễ đọc, và
    # BỐN lượt cross-review liên tiếp mỗi lượt bắt được đúng một mục trong danh sách ấy
    # rộng hơn vị từ. Danh sách chính là bề mặt sinh lỗi, nên nó bị bỏ chứ không vá tiếp:
    #
    #   Dấu của lease `L` tồn tại KHI VÀ CHỈ KHI Issue hiện có ÍT NHẤT MỘT comment mà
    #   `user.login == "github-actions[bot]"` VÀ body BẮT ĐẦU đúng bằng `**Lease `L`**`.
    #
    # Điều đáng lo suy thẳng từ đó: thao tác quản trị Issue nào làm biến mất comment khớp
    # CUỐI CÙNG thì làm mất dấu; mất dấu thì CHỐT NÀY không còn chặn — các chốt khác của
    # `kiem_github` vẫn áp dụng, nên đừng đọc thành "sẽ đăng trùng".
    # `posted_comment_id` nằm trong git thì không mất theo thao tác quản trị Issue. Đây
    # là hồi quy về ĐỘ BỀN, không phải tính sẵn sàng. `t126` ghim vị từ bằng ba ca âm.
    thieu = [k for k in BAT_BUOC if lease.get(k) in (None, "")]
    if thieu:
        raise Chan(RC_NOI_DUNG, f"thiếu trường bắt buộc: {', '.join(thieu)}")
    _kiem_provider_identity(lease)

    nguoi_cap = str(lease["granted_by"]).strip()
    # CHỐT CỐT LÕI. Một agent tự ký cho chính mình thì thứ ghi ra không phải lease,
    # chỉ là lời tự khai đội lốt uỷ quyền. So khớp bỏ hoa thường và cắt khoảng
    # trắng vì "  CODEX  " và "codex" là cùng một lời tự khai.
    if nguoi_cap.lower() in PROVIDERS:
        raise Chan(RC_TU_CAP,
                   f"granted_by={nguoi_cap!r} là tên một provider — agent KHÔNG tự cấp "
                   f"lease cho mình được (doctrine 'không tự cấp lease')")

    # CHỐT THẬT: phải NẰM TRONG danh sách cho phép, không chỉ "không nằm trong danh
    # sách cấm". Đây là chỗ `codex-dispatcher` / `ai-codex-bot` / `cödex` từng lọt.
    if nguoi_cap.lower() not in NGUOI_CO_THAM_QUYEN:
        raise Chan(RC_TU_CAP,
                   f"granted_by={nguoi_cap!r} KHÔNG nằm trong danh sách người có thẩm "
                   f"quyền {list(NGUOI_CO_THAM_QUYEN)} — danh sách CẤM không bao giờ đủ "
                   f"(cross-review 14-08-2026, finding lease-authority-spoof), nên cổng "
                   f"này đòi tên phải ĐƯỢC PHÉP chứ không chỉ 'không bị cấm'. Thêm người "
                   f"cấp mới = sửa NGUOI_CO_THAM_QUYEN qua một commit có review.")

    # Lớp neo vào danh tính GitHub XÁC THỰC, không phải chữ trong tệp YAML. `GITHUB_ACTOR`
    # do GitHub đặt cho runner; kẻ soạn tệp lease không đặt được nó. Chỉ áp khi biến có
    # mặt (tức đang chạy trong Actions) — chạy tay ở máy thì lớp này vắng, và nói thẳng
    # như vậy còn hơn giả vờ có.
    actor = (os.environ.get("GITHUB_ACTOR") or "").strip()
    if actor and actor.lower() not in NGUOI_CO_THAM_QUYEN:
        raise Chan(RC_TU_CAP,
                   f"GITHUB_ACTOR={actor!r} không có thẩm quyền cấp lease — người ĐẨY "
                   f"commit mới là thứ GitHub xác thực được, `granted_by` chỉ là chữ "
                   f"trong tệp. Lệch nhau thì tin cái GitHub xác thực.")

    so = lease["packet_issue"]
    # `bool` là con của `int` trong Python: `True` sẽ lọt nếu chỉ kiểm isinstance.
    if isinstance(so, bool) or not isinstance(so, int) or so <= 0:
        raise Chan(RC_NOI_DUNG, f"packet_issue phải là số nguyên dương, được {so!r}")

    _lease_id_hop_le(lease["lease_id"])   # wp678 D1: chuỗi thật, KHÔNG `str()` trước khi so (Q1)

    if tep is not None:
        _kiem_con_tro_treo(lease)
        _kiem_bia_mo(lease, tep, goc)

    sha = str(lease["reviewed_sha_required"]).strip()
    if not SHA40.match(sha):
        # SHA ngắn hoặc lệch dạng là mỏ neo GIẢ: reviewer sẽ đọc một head khác với
        # head mà lease tưởng đang nói tới, và không ai phát hiện ra.
        raise Chan(RC_NOI_DUNG,
                   f"reviewed_sha_required phải là 40 ký tự hex thường, được {sha!r}")

    _kiem_lop_review(lease)

    neo = ""
    if tep is None:
        # KHÔNG KIỂM ĐƯỢC ≠ ĐẠT. Không có đường dẫn tệp lease thì không tính được
        # gốc kho, nên chốt neo prompt không chạy — im lặng cho qua ở đây là dựng
        # lại đúng cái lỗ vừa bịt, chỉ khác cửa vào.
        if lease.get("prompt_sha256_required") or lease.get("prompt_path"):
            raise Chan(RC_NEO,
                       "lease có neo prompt nhưng `kiem()` được gọi không kèm đường dẫn "
                       "tệp — không kiểm được thì không cho qua")
    else:
        neo = _kiem_neo_prompt(lease, Path(tep), goc)

    han = _doc_han(lease["lease_expires_at_utc"])
    # `bo_qua_han` bỏ ĐÚNG MỘT chốt — chốt HẠN, và chỉ nó (vẫn ĐỌC hạn để hạn hỏng dạng còn
    # bị chặn). Người gọi DUY NHẤT: nhánh đã-có-dấu của `kiem_github`, nơi một lease đã đăng
    # rồi mới hết hạn phải được `rc=9` (idempotent, `t174`) chứ không `rc=8`.
    if not bo_qua_han and han <= datetime.now(timezone.utc):
        raise Chan(RC_NOI_DUNG,
                   f"lease đã hết hạn lúc {han.isoformat()} — đăng một lease chết thì "
                   f"người nhận tưởng có quyền mà không có")
    return lease, neo


def _tien_kiem_mien_dang(lease) -> None:
    """Tiền kiểm miền cho `kiem_github` (M2) — và PHẠM VI THẬT của nó, đã ĐO.

    Lời khai đầu tiên viết ở đây là *"thiếu trường sẽ thành `KeyError` TRẦN thoát ra khỏi
    cổng"*. **Phép đo BÁC câu ấy**, và nó bị bác bởi chính đột biến gỡ hàm này ra:

        đột biến bỏ tiền kiểm  ·  thiếu `lease_id`      -> rc=8  (KHÔNG đổi)
        đột biến bỏ tiền kiểm  ·  thiếu `packet_issue`  -> rc=8  (KHÔNG đổi)
        đột biến bỏ tiền kiểm  ·  `packet_issue` SAI KIỂU -> rc=9  (ĐỔI, và đổi NGUY HIỂM) — TRƯỚC bản vá P1

    Lý do hai ca đầu không đổi: `_do_dau_da_dang` vốn NUỐT mọi ngoại lệ không phải
    `RC_DA_DANG`, nên `KeyError` chết ngay tại đó rồi `kiem()` dựng lại `rc=8` như cũ.
    Tức hai ca ấy là **BỘ TƯƠNG ĐƯƠNG** — chúng không đo hàm này, chúng đo cái nuốt.

    Thứ hàm này thật sự đóng là ca THỨ BA: `packet_issue: "579"` (chuỗi) vẫn dựng được URL
    `issues/579/comments` hợp lệ, nên dò thấy dấu và trả `rc=9` — tức một lease SAI KIỂU
    được cấp đường "đã đăng, bỏ qua" và **né sạch mọi chốt của `kiem()`**. Đó là một lỗ
    thật, và nó là lý do duy nhất đã đo được để hàm này tồn tại — CHO TỚI bản vá P1 (#589).
    ĐO LẠI 25-09 sau bản vá P1 (nhánh đã-có-dấu nay chạy `kiem()`): gỡ tiền kiểm thì
    `packet_issue` sai kiểu (chuỗi, `bool`) cho `rc=8` ở CẢ bản đúng lẫn bản gỡ, `kiem()` chạy
    1 lần ở cả hai — mã thoát KHÔNG còn đổi. Răng CÒN LẠI của hàm là số lời gọi GitHub của
    phép dò: 0 (bản đúng) so 1 (bản gỡ). `t178` chốt đúng đại lượng ấy.

    wp678 (D2, Q1/Q2) — tách bằng chứng LỊCH SỬ khỏi hành vi SAU D3. Trước wp678 dòng chốt
    `lease_id` ở đây nhận `str|int` (lệch D1) và là chốt DUY NHẤT giữ `lease_id` sai kiểu khỏi
    mạng; mọi số "0 so 1 lời gọi" của trục `lease_id` ở trên là phép đo thời ấy. Nay nó đọc qua
    `_lease_id_hop_le` (cùng luật D1, `int` cũng bị chặn), và `_kiem_comment_da_co` (D3) có chốt
    RIÊNG trước `_doc_gh`. Hệ quả ĐO 08-10-2026 trên ứng viên: gỡ riêng dòng ấy (đột biến `L`)
    vẫn 0 lời gọi ở trục `lease_id` của `t178`, `t195`–`t197` (D3 đỡ) — ca đích của `L` là
    `t205`, đo hàm này TRỰC TIẾP. (Trục `packet_issue` của hàm này KHÔNG được đo lại ở wp678.)

    `bool` bị loại tường minh vì `isinstance(True, int)` là `True` trong Python: một
    `packet_issue: true` lọt phép kiểm kiểu ngây thơ rồi thành `issues/True` trên URL.
    CA `bool` NAY ĐÃ ĐO — `t178` giữ nó bằng SỐ LỜI GỌI GitHub (`0`), không bằng mã thoát
    (mã thoát là `8` ở cả bản đúng lẫn bản gỡ chốt). Câu "KHÔNG ĐO" ở đây là lời khai của
    bản trước, đã hết hiệu lực từ `M11`; cross-review lượt 2 bắt nó còn sót
    (`post-fix-boolean-evidence-claims-drift`). Giới hạn CÒN đúng: mới đo qua adapter giả,
    chưa đo trên một endpoint HTTP thật.

    HÀM NÀY KHÔNG PHÁN, NÓ CHỈ LÀM PHÉP DÒ CÂM. `Chan` nó ném được `_do_dau_da_dang` bắt
    lại và nuốt; hệ quả là dữ liệu thiếu miền làm phép dò NHƯỜNG quyền phán cho chuỗi
    `kiem()` cũ, đúng thứ tự cũ, đúng mã thoát cũ (M3).

    BẢN TRƯỚC ĐẶT HÀM NÀY NGOÀI `try` VÀ ĐÓ LÀ MỘT HỒI QUY THẬT, do cross-review codex
    lượt 1 bắt (`unposted-error-precedence-changes`). Khi ấy `Chan(8)` ở đây thoát ra khỏi
    cả `kiem_github`, cướp quyền phán của `kiem()`. Phản chứng chạy được: một lease CHƯA
    ĐĂNG vừa tự cấp (`kiem()` trả `rc=4`) vừa có `packet_issue` sai kiểu —

        nền `origin/master`   -> rc=4   (`kiem()` bắt authority trước)
        bản cũ của packet này -> rc=8   (tiền kiểm bắn trước, ĐỔI thứ tự lỗi)
        bản này               -> rc=4   (nhường lại, khớp nền)

    Docstring cũ khai "không đổi mã thoát (M3)" và câu ấy ĐÚNG khi lease chỉ mắc MỘT lỗi,
    SAI khi mắc hai. `t177` chỉ dựng từng lỗi riêng nên không bắt được. `t180` khoá ca hai
    lỗi đồng thời.
    """
    # wp678 D2: cùng luật với D1 (bản trước nhận `str|int`, lệch D1); `int` cũng bị chặn TRƯỚC mạng.
    _lease_id_hop_le(lease.get("lease_id"))
    so = lease.get("packet_issue")
    if isinstance(so, bool) or not isinstance(so, int):
        raise Chan(RC_NOI_DUNG, "tiền kiểm: thiếu `packet_issue` hoặc sai kiểu (đòi số nguyên)")


def _do_dau_da_dang(lease: dict) -> None:
    """M1 — dò dấu "đã đăng" TRƯỚC, không chạm `kiem()`.

    CÓ dấu ⇒ ném `Chan(RC_DA_DANG)` ngay. KHÔNG có dấu, hoặc KHÔNG ĐO ĐƯỢC vì bất cứ lý do
    nào khác, ⇒ trả về lặng lẽ để `kiem_github` chạy TRỌN chuỗi cũ — chính chuỗi ấy sẽ dựng
    lại đúng lỗi đó, đúng thứ tự, đúng mã thoát của `origin/master` (M3).

    Vì sao nuốt mọi ngoại lệ KHÁC ở đây mà không phải là fail-open: hàm này KHÔNG phải một
    cổng, nó là một phép DÒ. Nó chỉ có quyền nói "đã đăng rồi, bỏ qua"; nó không có quyền
    nói "đạt". Mọi phán quyết từ chối vẫn do chuỗi cũ đưa ra, nguyên vẹn.

    `_tien_kiem_mien_dang` nằm TRONG `try` là có chủ đích, và bản trước để nó ngoài — xem
    docstring hàm ấy. Nuốt `Chan` của tiền kiểm KHÔNG làm mất răng của nó: răng của tiền
    kiểm là chặn phép dò CHẠM MẠNG rồi trả `rc=9` cho một lease hỏng miền, và răng ấy đo
    bằng SỐ LỜI GỌI GitHub (`t178`), không đo bằng mã thoát.
    """
    # CHỐT HÌNH DẠNG đứng NGOÀI `try` — có chủ đích, và khác hẳn chốt MIỀN bên dưới.
    #
    # Cross-review lượt 2 bắt (`unposted-error-precedence-changes`, lần thứ hai cùng slug):
    # bản vá lượt 1 đưa CẢ `_tien_kiem_mien_dang` vào trong `try`, nên `Chan` nó ném cho một
    # `lease` KHÔNG PHẢI ánh xạ cũng bị nuốt — rồi `kiem()` gọi `.get()` trên thứ không có
    # phương thức ấy và một `AttributeError` TRẦN thoát ra khỏi cổng. Đo được năm hình dạng:
    # `None` · `[]` · `True` · `55` · `"55"`.
    #
    # KHAI CHO ĐÚNG, ĐỪNG PHÓNG ĐẠI: nền `origin/master` CŨNG vỡ y hệt ở đây, nên đây KHÔNG
    # phải hồi quy mới — nó là việc đánh mất một chốt mà chính lượt 1 vừa thêm vào. Và phạm vi
    # đã đo được là API `kiem_github`; đường CLI có `_doc_yaml` giữ chốt ánh xạ và đo ra `rc=8`.
    #
    # Vì sao HAI chốt chứ không một:
    #   HÌNH DẠNG (không phải dict) -> không ai phán được gì về nó, kể cả `kiem()`. Fail-close
    #                                  NGAY, ngoài `try`.
    #   MIỀN (dict thiếu/sai trường) -> `kiem()` phán được, và phán ĐÚNG THỨ TỰ hơn. Nhường
    #                                  lại: nuốt trong `try`.
    # Gộp hai thứ ấy làm một là lý do lượt 1 sai theo chiều này và lượt 0 sai theo chiều kia.
    if not isinstance(lease, dict):
        raise Chan(RC_NOI_DUNG, "tiền kiểm: lease không phải ánh xạ")
    try:
        _tien_kiem_mien_dang(lease)
        _kiem_comment_da_co(_repo_github(), lease)
    except Chan as c:
        if c.ma == RC_DA_DANG:
            raise
        return
    except Exception:  # noqa: BLE001 — xem docstring: dò, không phán
        return


def kiem_github(lease: dict, tep=None, goc=None) -> tuple:
    """Kiểm một lease TRƯỚC khi đăng, gồm hai lớp GitHub mà `kiem()` không chạm.

    THỨ TỰ LÀ NỘI DUNG, không phải chi tiết cài đặt. Bản trước gọi `kiem()` NGAY DÒNG ĐẦU,
    mà `kiem()` ném `rc=8` khi lease hết hạn (`:885`) — nằm TRƯỚC chốt `rc=9` của
    `_kiem_comment_da_co`. Hệ quả đo được 20-09-2026: một lease **đã đăng rồi mới hết hạn**
    không bao giờ tới được đường `rc=9`; nó chết ở `rc=8`, và bước `đăng` của
    `ops-publish-lease.yml` — vốn CÓ SẴN nhánh `rc=9` đúng — không bao giờ được gọi cho hình
    dạng ấy. Hai lượt `35519177197` (#568) và `35519243379` (#566) đỏ vì đúng chuyện này,
    cả hai đỏ SAU KHI lease mới đã đăng xong.

    GIÁ PHẢI TRẢ, khai thẳng chứ không làm nhẹ (M4) — và bản trước khai SAI hậu quả: với lease
    ĐÃ ĐĂNG, đường này từng trả `rc=9` mà KHÔNG chạy `kiem()`, và câu cũ ở đây nói "một tệp
    lease đã đăng rồi bị SỬA về sau sẽ KHÔNG bị bắt" như một đánh đổi chấp nhận được. Connector
    codex (#589, 24-09) nối nó với `ai-dang-giu` và chỉ ra hậu quả thật: tệp đã sửa được tính là
    người giữ mà chưa qua cổng thẩm quyền — P1. Nay nhánh đã-có-dấu chạy `kiem()` trên tệp HIỆN
    TẠI, trừ đúng chốt hạn; tự cấp (`rc=4`), neo prompt (`rc=6`), trường thiếu/sai dạng
    (`rc=8`) đều bị chặn TRƯỚC `rc=9`. `t190` đo từng vế.
    GIÁ CÒN LẠI, KHÔNG ĐÓNG ở đây: một người CÓ thẩm quyền sửa một lease đã đăng (gia hạn,
    nới `write_set`) thì tệp qua `kiem()` và vẫn `rc=9` — bản CHIẾU đã đăng không phản ánh nội
    dung mới. Đó là thao tác của người có quyền, không phải lỗ thẩm quyền; nhưng bản chiếu cũ
    đi là thật, và chưa có chốt nào so tệp với bản chiếu. Đường ấy CŨNG bỏ `_kiem_loai_so_hieu` — chốt nằm NGOÀI `kiem()`, nên
    câu trên chưa phủ nó (cross-review lượt 7): `packet_issue` trỏ vào một Pull Request mà đã
    có dấu bot thì trả `rc=9` thay vì `rc=8` (`RC_NOI_DUNG`). Reviewer lượt 7 đếm lời gọi thật: có dấu
    ⇒ `kiem` 0 lần, lời gọi loại số hiệu 0 lần, bất kể số hiệu là issue hay PR — số ấy là TRƯỚC
    bản vá P1. Đo lại 25-09 trên lease sạch của bộ #579 (lượt 15): có dấu ⇒ `kiem` 1 lần (kèm
    `bo_qua_han`), loại số hiệu 0 lần; không dấu ⇒ 1 và 1. Nửa về `_kiem_loai_so_hieu` VẪN đúng. Không tạo được
    comment nào: `rc=9` là "đã đăng, bỏ qua", không phải "đạt". Đánh đổi có chủ đích: bản
    chiếu đã công bố mới là thứ người khác đọc, và không ai được lợi khi một lượt CI đỏ vì
    một lease đã đăng đúng.

    Giá thứ hai, nhỏ hơn và cũng phải khai: đường KHÔNG-CÓ-DẤU gọi `_kiem_comment_da_co` HAI
    lần KHI chuỗi cũ đi tới cửa cuối (một lần dò, một lần ở cửa cuối); MỘT lần khi `kiem()`
    hay chốt loại số hiệu chặn trước. Đếm lời gọi thật (24-09, bộ ca #579): lease sạch ⇒ 2,
    endpoint `comments` hỏng mãi ⇒ 2; hết hạn ⇒ 1 (`rc=8`), tự cấp ⇒ 1 (`rc=4`), neo prompt
    không kiểm được ⇒ 1 (`rc=6`), thiếu trường ⇒ 1 (`rc=8`), số hiệu là PR ⇒ 1 (`rc=8`, số
    của cross-review lượt 7). Bản trước khai "HAI lần" cho mọi đường không-dấu — rộng hơn
    phép đo (cross-review lượt 11 song song). Đổi một lời gọi API lấy việc giữ M3 đúng từng
    mã thoát. KHÔNG ĐO: chi phí ấy chưa được đo trên một issue nhiều trang comment.
    """
    try:
        _do_dau_da_dang(lease)
    except Chan as c:
        if c.ma != RC_DA_DANG:
            raise
        # ĐÃ CÓ DẤU — nhưng dấu chỉ nói "lease MANG TÊN NÀY đã đăng", KHÔNG nói "tệp HIỆN TẠI
        # là tệp đã đăng". Cross-review connector codex trên #589 (24-09, P1, đo lại): bản
        # trước tôn trọng dấu NGAY, nên một lease đã đăng bị SỬA thành tự cấp (`rc=4`) hay
        # neo prompt không kiểm được (`rc=6`) vẫn ra `rc=9` — workflow coi là bỏ qua thành
        # công, và `ai-dang-giu` tính tệp đã sửa là người giữ. Trên master `kiem()` chạy
        # trước nên không có lỗ này: đây là HỒI QUY của chính packet.
        # Nên: tệp HIỆN TẠI phải qua MỌI chốt của `kiem()` TRỪ chốt hạn — miễn trừ HẸP đúng
        # một điều kiện, vì hết hạn sau khi đăng là lý do packet này tồn tại (`t174`).
        kiem(lease, tep, goc, bo_qua_han=True)
        raise
    lease, neo = kiem(lease, tep, goc)
    repo = _repo_github()
    _kiem_loai_so_hieu(repo, lease["packet_issue"])
    _kiem_comment_da_co(repo, lease)
    return lease, neo


def dung_than(lease: dict, duong_dan: str) -> str:
    """Thân comment: nói rõ đây là bản CHIẾU, nguồn sự thật nằm trong kho."""
    import yaml
    lease_id = _lease_id_hop_le(lease.get("lease_id"))   # wp678 D4: chốt riêng, dấu đăng là CHUỖI thật
    khoi = yaml.safe_dump(lease, allow_unicode=True, sort_keys=False).rstrip()
    return (
        f"**Lease `{lease_id}`** — đăng tự động từ `{duong_dan}`.\n\n"
        f"Nguồn sự thật là tệp trong kho, comment này chỉ là **bản chiếu**. Sửa lease "
        f"thì sửa tệp rồi push; đừng sửa tay comment này.\n\n"
        f"```yaml\n{khoi}\n```\n"
    )


# =====================================================================================
# A0 — SỔ THU HỒI LEASE trên trunk (packet wp488; spec `ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md`
# revision 9, sha256 465538364b1a…; ADR-0047). CHƯA KÍCH HOẠT: `SO_THU_HOI_KICH_HOAT = False`.
#
# Verdict SẢN PHẨM của `check`/`ai-dang-giu` ở A0 vẫn là LUẬT CŨ (bia mộ hai chiều); luật mới
# (áp sổ theo `lease_id`, precedence, chiều ngược) chỉ chạy trong hàm DỰ BÁO có nhãn `DU_BAO:`
# và KHÔNG đổi rc. Điều duy nhất A0 cưỡng chế thật: sổ `ops/thu-hoi/` KHÔNG RỖNG khi cờ False
# ⇒ 12 ở mọi consumer vận hành — một bản ghi lọt vào trước khi cổng tiếp nhận có mã canonical là
# thứ spec §write_set "Bootstrap" cấm grandfather.
#
# Ba lớp của ADR-0047 nằm ở đây: (1) danh tính ghim `KHO_CANONICAL`, discovery bằng URL tường
# minh; (2) nền thực thi = hồ sơ adapter so với mỏ neo `PROFILE_ADAPTER_DA_DUYET` — RỖNG ở A0 vì
# nền production là QUYẾT ĐỊNH CHỦ KHO, không phải thứ mã tự đo rồi tự duyệt; (3) toàn vẹn object:
# reader `KhoObject` băm lại từng object, lấy cạnh từ bytes đã băm, store cô lập, ngân sách có đơn vị.
# =====================================================================================
KHO_CANONICAL = "github.com/ducthangho/tra-luat"
SO_THU_HOI_KICH_HOAT = False
THU_MUC_SO = "ops/thu-hoi"
PATH_NGOAI_LE_RETIRED = "ops/thu-hoi/_ngoai-le-closure.retired.yaml"
PATH_POLICY_CLOSURE = ".github/coordination/change-impact.v1.json"
PATH_BO_KIEM = "ops/lease_publish.py"
# Mỏ neo profile ĐÃ DUYỆT. Rỗng có chủ đích ở A0: mọi lời gọi discovery production ⇒ 12 cho tới khi
# chủ kho duyệt một manifest (ADR-0047 lớp 2). Test tiêm neo qua tham số `da_duyet=` của API nội bộ;
# KHÔNG có cờ CLI hay biến môi trường nào đổi được tập này (A2: "không có cờ production đổi authority").
PROFILE_ADAPTER_DA_DUYET: frozenset = frozenset()
# Danh sách lịch sử bia mộ — A1 ghim từ receipt A0 (Q6). Rỗng ở A0.
BIA_MO_LICH_SU: tuple = ()
# Descriptor ngoại lệ closure Q13 (S6): sha256 thân comment `5575587924` trên PR #475, A1 readback rồi ghim —
# KHÔNG bịa. Chừng nào còn `None`, mọi marker MỚI ở T đều 12 (A0 không tạo marker; policy có mà không marker
# cũng 12 — không grandfather).
DESCRIPTOR_Q13_SHA256 = None
# Ngân sách reader — ĐỀ XUẤT của reviewer lượt 6 (spec Q4.5), CHƯA đo trên roots production.
# Đơn vị: objects = số `(actual_type, OID)` phân biệt; bytes = bytes thô sau giải nén; edges = số cạnh
# trên MỘT đường (parent: mỗi đường parent; tree/alias: một lần resolve tại một occurrence); seconds =
# deadline monotonic. Biên INCLUSIVE: n ≤ bound đi tiếp, n > bound ⇒ 12.
NGAN_SACH_MAC_DINH = {
    "max_unique_objects": 50000,
    "max_object_bytes": 8388608,
    "max_total_object_bytes": 134217728,
    "max_parent_path_edges": 10000,
    "max_tree_or_alias_edges": 128,
    "max_alternate_stores": 8,
    "max_alternate_depth": 4,
    "max_reader_wall_seconds": 60.0,
}
_RE_ISO_Z = re.compile(r"^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}Z$")
_KHOA_THU_HOI_BAT_BUOC = ("schema_version", "event", "lease_id", "packet_issue", "thu_hoi_boi",
                         "thu_hoi_luc_utc", "ly_do", "can_cu")
_KHOA_THU_HOI_TUY_CHON = ("cap_lai_cho", "blob_da_biet_luc_ghi")
_KHOA_RETIRED = ("schema_version", "event", "descriptor_sha256", "first_policy_sha256",
                 "base_sha_before_add", "retired_at_utc")


def _doc_iso_z(luc: str):
    """`YYYY-MM-DDTHH:MM:SSZ` → datetime UTC, hoặc ``None`` khi lịch không có thật (F06: regex không biết tháng 2)."""
    try:
        return datetime.fromisoformat(luc.replace("Z", "+00:00"))
    except ValueError:
        return None


def _nap_yaml_khong_trung_khoa(noi_dung: bytes):
    """YAML an toàn, KHOÁ TRÙNG ⇒ 12 — PyYAML mặc định lặng lẽ lấy giá trị sau."""
    import yaml
    trung = []

    class _Loader(yaml.SafeLoader):
        pass

    def _mapping(loader, node, deep=False):
        da_thay = set()
        for k_node, _ in node.value:
            k = loader.construct_object(k_node, deep=deep)
            if k in da_thay:
                trung.append(k)
            da_thay.add(k)
        return yaml.SafeLoader.construct_mapping(loader, node, deep)

    _Loader.add_constructor(yaml.resolver.BaseResolver.DEFAULT_MAPPING_TAG, _mapping)
    try:
        d = yaml.load(noi_dung.decode("utf-8"), Loader=_Loader)
    except Exception as e:  # YAMLError / UnicodeDecodeError — nguồn hỏng là 12, không phải 8
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: YAML sổ thu hồi hỏng: {str(e).splitlines()[0][:160]}") from None
    if trung:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: YAML sổ thu hồi có khoá trùng: {trung[0]!r}")
    return d


def phan_tuyen_so(duong: str):
    """Định tuyến một đường dẫn trong namespace sổ: ``thu_hoi`` · ``metadata`` · ``None`` (ngoài sổ).

    ĐÚNG MỘT path reserved đi schema metadata (S7); mọi tên khác — kể cả tên GẦN reserved
    (`.yml`, thiếu `_`) — vẫn là bản ghi thu hồi và phải qua M1. Thư mục con/ tệp không `.yaml`
    trong sổ là ``thu_hoi`` để M1 từ chối (12), không được lặng lẽ bỏ qua.
    """
    if duong == PATH_NGOAI_LE_RETIRED:
        return "metadata"
    if duong.startswith(THU_MUC_SO + "/"):
        return "thu_hoi"
    return None


def kiem_ban_ghi_thu_hoi(duong: str, mode: str, loai: str, noi_dung: bytes, bay_gio=None) -> dict:
    """M1 — hợp đồng parser bản ghi ``lease_revoked`` (r3), thứ tự lỗi: nguồn/object (12) →
    cấu trúc/ID (12) → thẩm quyền (4) → trường còn lại (8). Không truthiness cho bool."""
    bay_gio = bay_gio or datetime.now(timezone.utc)
    ten = duong[len(THU_MUC_SO) + 1:]
    if "/" in ten or loai != "blob" or mode != "100644" or not ten.endswith(".yaml"):
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: {duong}: sổ chỉ nhận regular blob 100644 `<lease_id>.yaml` "
                   f"ngay trong {THU_MUC_SO}/ (được mode={mode} type={loai})")
    d = _nap_yaml_khong_trung_khoa(noi_dung)
    if not isinstance(d, dict):
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: root không phải mapping")
    lease_id = d.get("lease_id")
    if not isinstance(lease_id, str) or not LEASE_ID.fullmatch(lease_id) or lease_id != ten[:-5]:
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: {duong}: lease_id {lease_id!r} phải khớp LEASE_ID và bằng tên tệp")
    nguoi = d.get("thu_hoi_boi")
    nguoi_s = str(nguoi).strip().lower() if isinstance(nguoi, str) else ""
    if nguoi_s in PROVIDERS:
        raise Chan(RC_TU_CAP, f"{duong}: thu_hoi_boi={nguoi!r} là tên provider — agent không tự thu hồi")
    if nguoi_s not in NGUOI_CO_THAM_QUYEN:
        raise Chan(RC_TU_CAP, f"{duong}: thu_hoi_boi={nguoi!r} không nằm trong {list(NGUOI_CO_THAM_QUYEN)}")
    khoa = set(d)
    thua = khoa - set(_KHOA_THU_HOI_BAT_BUOC) - set(_KHOA_THU_HOI_TUY_CHON)
    thieu = [k for k in _KHOA_THU_HOI_BAT_BUOC if k not in khoa]
    if thua or thieu:
        # `key=repr`: khoá YAML lẫn kiểu (int `1` + str) làm `sorted` ném TypeError thành traceback rc=1 thay vì 8
        # (Codex review 457affd, P2) — bản ghi không tin cậy không được quyền chọn mã thoát.
        raise Chan(RC_NOI_DUNG, f"{duong}: khoá thừa {sorted(thua, key=repr)} / thiếu {thieu}")
    sv = d["schema_version"]
    if type(sv) is not int or sv != 1:   # `1.0`/`True` đều bị loại — so KIỂU, không so bằng (F06)
        raise Chan(RC_NOI_DUNG, f"{duong}: schema_version phải là integer 1, được {sv!r}")
    if d["event"] != "lease_revoked":
        raise Chan(RC_NOI_DUNG, f"{duong}: event phải là 'lease_revoked', được {d['event']!r}")
    so = d["packet_issue"]
    if isinstance(so, bool) or not isinstance(so, int) or so <= 0:
        raise Chan(RC_NOI_DUNG, f"{duong}: packet_issue phải là integer dương, được {so!r}")
    luc = d["thu_hoi_luc_utc"]
    if not isinstance(luc, str) or not _RE_ISO_Z.match(luc):
        raise Chan(RC_NOI_DUNG, f"{duong}: thu_hoi_luc_utc phải là CHUỖI ISO8601 'Z', được {luc!r}")
    if _doc_iso_z(luc) is None:   # regex qua nhưng lịch sai (30-02) — mã hợp đồng, không traceback (F06)
        raise Chan(RC_NOI_DUNG, f"{duong}: thu_hoi_luc_utc không phải thời điểm có thật: {luc!r}")
    if _doc_iso_z(luc) > bay_gio:
        raise Chan(RC_NOI_DUNG, f"{duong}: thu_hoi_luc_utc ở tương lai so clock snapshot")
    if not isinstance(d["ly_do"], str) or not d["ly_do"].strip():
        raise Chan(RC_NOI_DUNG, f"{duong}: ly_do phải là chuỗi không rỗng")
    can_cu = d["can_cu"]
    m = re.fullmatch(r"https://" + re.escape(KHO_CANONICAL) + r"/issues/(\d+)#issuecomment-(\d+)", can_cu) \
        if isinstance(can_cu, str) else None
    if not m or int(m.group(1)) != so:
        raise Chan(RC_NOI_DUNG, f"{duong}: can_cu phải là MỘT URL Issue comment của {KHO_CANONICAL} "
                                f"trên issue #{so}, được {can_cu!r}")
    dich = d.get("cap_lai_cho")
    if dich in (None, ""):
        d["cap_lai_cho"] = None
    elif not isinstance(dich, str) or not LEASE_ID.fullmatch(dich) or dich == lease_id:
        raise Chan(RC_NOI_DUNG, f"{duong}: cap_lai_cho phải là LEASE_ID hợp lệ khác {lease_id!r}, được {dich!r}")
    blobs = d.get("blob_da_biet_luc_ghi")
    if blobs is not None and (not isinstance(blobs, list)
                              or any(not isinstance(b, str) or not SHA40.match(b) for b in blobs)):
        raise Chan(RC_NOI_DUNG, f"{duong}: blob_da_biet_luc_ghi phải là danh sách SHA40")
    return d


def kiem_metadata_retired(duong: str, mode: str, loai: str, noi_dung: bytes, bay_gio=None) -> dict:
    """Q13/S7 — metadata `closure_exception_retired`: ĐÚNG sáu khoá, regular 100644; MỌI lỗi ⇒ 12."""
    bay_gio = bay_gio or datetime.now(timezone.utc)
    if loai != "blob" or mode != "100644":
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: metadata phải là regular blob 100644")
    d = _nap_yaml_khong_trung_khoa(noi_dung)
    if not isinstance(d, dict) or set(d) != set(_KHOA_RETIRED):
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: phải là mapping có đúng khoá {list(_KHOA_RETIRED)}")
    sv = d["schema_version"]
    if type(sv) is not int or sv != 1 or d["event"] != "closure_exception_retired":
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: schema_version/event sai")
    for k in ("descriptor_sha256", "first_policy_sha256"):
        if not isinstance(d[k], str) or not SHA256.match(d[k]):
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: {k} phải là sha256 hex")
    if not isinstance(d["base_sha_before_add"], str) or not SHA40.match(d["base_sha_before_add"]):
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: base_sha_before_add phải là SHA40")
    luc = d["retired_at_utc"]
    if not isinstance(luc, str) or not _RE_ISO_Z.match(luc) or _doc_iso_z(luc) is None \
            or _doc_iso_z(luc) > bay_gio:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: retired_at_utc phải là ISO8601 'Z' có thật, không ở tương lai")
    return d


def _git_windows(path=None, system_root=None, program_files=None, cwd=None,
                 cong_cu_git=None, chan_doan=None, phan_cach=None) -> str | None:
    """Windows: giải executable `git` theo danh sách ứng viên có thứ tự (Q4.1 / M1).
    Thứ tự:
      1. CONG_CU_GIT — biến môi trường tường minh (chỉ nhận git.exe, nếu có).
      2. Thư mục cài Git phân giải từ %ProgramFiles% (và registry nếu đọc được).
      3. git.exe trên PATH thật — đường CHÓT (chỉ chấp nhận git.exe, không qua PATHEXT).
    Ở MỌI BƯỚC: chỉ chấp nhận git.exe, loại ứng viên nằm trong cwd, loại ứng viên nằm dưới %SystemRoot%.
    Khi bước 2 (%ProgramFiles%) không phân giải, chẩn đoán ghi KHÔNG_ĐO_ĐƯỢC chứ không
    im lặng rơi xuống bước 3 (N3b).
    Không thấy gì thì trả None để _git_exe_toi_thieu ném Chan(RC_KHONG_XAC_DINH).
    """
    env = os.environ
    sr = env.get("SystemRoot", "") if system_root is None else str(system_root)
    sr_norm = os.path.normcase(os.path.abspath(sr)).rstrip("\\/") if sr else None

    cw = os.getcwd() if cwd is None else str(cwd)
    cw_norm = os.path.normcase(os.path.abspath(cw)).rstrip("\\/") if cw else None

    def duoi_system_root(u):
        if not sr_norm:
            return False
        q = os.path.normcase(os.path.abspath(str(u)))
        return q == sr_norm or q.startswith(sr_norm + os.sep) or q.startswith(sr_norm + "/")

    def trong_cwd(u):
        if not cw_norm:
            return False
        q = os.path.normcase(os.path.abspath(str(u)))
        return q == cw_norm or q.startswith(cw_norm + os.sep) or q.startswith(cw_norm + "/")

    def hop_le(u):
        if not u:
            return False
        p = Path(u)
        if not p.is_file():
            return False
        try:
            r = p.resolve()
        except Exception:
            r = p
        if duoi_system_root(p) or duoi_system_root(r):
            return False
        if trong_cwd(p) or trong_cwd(r):
            return False
        return True

    # 1. CONG_CU_GIT
    chi_dinh = env.get("CONG_CU_GIT") if cong_cu_git is None else cong_cu_git
    if chi_dinh and Path(chi_dinh).name.lower() == "git.exe" and hop_le(chi_dinh):
        return str(Path(chi_dinh).resolve())

    # 2. %ProgramFiles%
    pf = env.get("ProgramFiles", r"C:\Program Files") if program_files is None else program_files
    ung_vien_pf = [
        Path(pf) / "Git" / "cmd" / "git.exe",
        Path(pf) / "Git" / "bin" / "git.exe",
        Path(pf) / "Git" / "mingw64" / "bin" / "git.exe",
    ]
    if program_files is None and "ProgramFiles(x86)" in env:
        pf86 = env["ProgramFiles(x86)"]
        ung_vien_pf += [
            Path(pf86) / "Git" / "cmd" / "git.exe",
            Path(pf86) / "Git" / "bin" / "git.exe",
        ]
    for u in ung_vien_pf:
        if hop_le(u):
            return str(Path(u).resolve())

    # Bước 2 không phân giải: chẩn đoán ghi KHÔNG_ĐO_ĐƯỢC chứ không im lặng rơi xuống bước 3 (N3b)
    thong_bao_pf = "KHÔNG_ĐO_ĐƯỢC: không thấy git hợp lệ dưới %ProgramFiles%, rơi xuống PATH"
    if chan_doan is not None:
        chan_doan.append(thong_bao_pf)
    else:
        sys.stderr.write(thong_bao_pf + "\n")

    # 3. git.exe trên PATH thật — đường CHÓT
    # Tường minh kiểm tra git.exe, không qua shutil.which / PATHEXT để loại trừ hoàn toàn .bat/.cmd/.py
    path_val = env.get("PATH", "") if path is None else path
    sep = os.pathsep if phan_cach is None else phan_cach
    for d_raw in path_val.split(sep):
        d = d_raw.strip().strip('"')
        if not d or trong_cwd(d) or duoi_system_root(d):
            continue
        cand = Path(d) / "git.exe"
        if hop_le(cand):
            return str(cand.resolve())
    return None


def _git_exe_toi_thieu(*, nen: str | None = None, **tiem) -> str:
    """Executable `git` giải MỘT lần bằng đường tuyệt đối trong PATH tối thiểu (Q4.1 / M1)."""
    import shutil
    nen_thuc = nen
    if nen_thuc is None:
        t = sys.platform
        nen_thuc = "windows" if (t.startswith("win") or t in ("mingw", "msys", "cygwin")) else "posix"
    if nen_thuc == "windows":
        duong = _git_windows(**tiem)
        if not duong:
            raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: không thấy `git` hợp lệ cho Windows")
        return duong
    path_posix = tiem.get("path", "/usr/bin:/bin")
    duong = shutil.which("git", path=path_posix)
    if not duong:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: không thấy `git` trong PATH tối thiểu {path_posix}")
    return str(Path(duong).resolve())


def _env_rong(git_exe: str, git_dir, home: str, **them) -> dict:
    """Env con dựng TỪ RỖNG — không kế thừa `os.environ` (ADR-0047 lớp 2). `git_dir=None` ⇒ không đặt GIT_DIR
    (preflight nguồn giải kho bằng `-C`, F09)."""
    mt = {
        "PATH": str(Path(git_exe).parent),
        "HOME": home,
        **({"GIT_DIR": git_dir} if git_dir is not None else {}),
        "GIT_CONFIG_NOSYSTEM": "1",
        "GIT_CONFIG_GLOBAL": os.devnull,
        "GIT_TEMPLATE_DIR": "",
        "GIT_NO_REPLACE_OBJECTS": "1",
        "GIT_TERMINAL_PROMPT": "0",
        "LC_ALL": "C",
    }
    mt.update(them)
    return mt


def tempfile_home() -> str:
    """HOME rỗng cho các lời gọi git cô lập — thư mục tạm không config, sống tới hết tiến trình."""
    import tempfile
    global _HOME_RONG
    if _HOME_RONG is None:
        _HOME_RONG = tempfile.mkdtemp(prefix="home_rong_")
    return _HOME_RONG


_HOME_RONG = None


def _repo_tam_co_lap(git_exe: str, thu_muc: Path) -> str:
    """Repo tạm KHÔNG ref, KHÔNG config nguồn, KHÔNG template — làm `GIT_DIR` cho mọi lời gọi adapter."""
    git_dir = thu_muc / "tam.git"
    p = subprocess.run([git_exe, "init", "-q", "--bare", "--template=", str(git_dir)],
                       capture_output=True, text=True,
                       env=_env_rong(git_exe, str(git_dir), str(thu_muc)))
    if p.returncode != 0:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: không dựng được repo tạm: {p.stderr[:160]}")
    return str(git_dir)


def hoso_adapter_do(git_exe: str | None = None) -> dict:
    """Hồ sơ nền thực thi đo được từ deployment hiện tại (KHÔNG bí mật). Chỉ là INPUT để so với mỏ neo;
    đo rồi tự đưa vào `PROFILE_ADAPTER_DA_DUYET` là tự khai — bị cấm (ADR-0047 lớp 2)."""
    git_exe = git_exe or _git_exe_toi_thieu()
    p = subprocess.run([git_exe, "--version"], capture_output=True, text=True,
                       env={"PATH": str(Path(git_exe).parent), "LC_ALL": "C"})
    return {
        "schema_version": 1,
        "git_path": git_exe,
        "git_sha256": hashlib.sha256(Path(git_exe).read_bytes()).hexdigest(),
        "git_version": p.stdout.strip() if p.returncode == 0 else "",
        "credential_helper": "",   # không dùng
        "http_sslCAInfo": None,
        "http_sslCAPath": None,
        "proxy": None,
        "endpoint": "https://" + KHO_CANONICAL,
    }


_HOSO_KHOA = ("schema_version", "git_path", "git_sha256", "git_version", "credential_helper",
              "http_sslCAInfo", "http_sslCAPath", "proxy", "endpoint")


def kiem_mien_ho_so(hoso) -> None:
    """Schema HỮU HẠN của hồ sơ adapter (F08): đúng tập khoá, đúng kiểu/miền từng giá trị. Đứng TRƯỚC phép so
    digest — mỏ neo chỉ được so trên một hồ sơ đã nằm trong miền, nên khoá lạ hay giá trị ngoài miền ⇒ 12 kể cả
    khi ai đó băm đúng dict ấy đưa vào mỏ neo."""
    if not isinstance(hoso, dict) or tuple(sorted(hoso)) != tuple(sorted(_HOSO_KHOA)):
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: hồ sơ adapter phải có đúng khoá {list(_HOSO_KHOA)}")
    if type(hoso["schema_version"]) is not int or hoso["schema_version"] != 1:
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: hồ sơ adapter schema_version phải là integer 1")
    gp = hoso["git_path"]
    if not isinstance(gp, str) or not Path(gp).is_absolute():
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: hồ sơ adapter git_path phải là đường tuyệt đối")
    if not isinstance(hoso["git_sha256"], str) or not SHA256.match(hoso["git_sha256"]):
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: hồ sơ adapter git_sha256 phải là sha256 hex")
    if not isinstance(hoso["git_version"], str) or not hoso["git_version"].startswith("git version "):
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: hồ sơ adapter git_version phải là đầu ra `git --version`")
    if hoso["credential_helper"] != "":
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: adapter không dùng credential helper — phải là chuỗi rỗng")
    for k in ("http_sslCAInfo", "http_sslCAPath", "proxy"):
        v = hoso[k]
        if v is not None and (not isinstance(v, str) or not v.strip()):
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: hồ sơ adapter {k} phải là None hoặc chuỗi không rỗng")
    ep = hoso["endpoint"]
    if not isinstance(ep, str) or not re.fullmatch(r"(https|file)://[^\s]+", ep):
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: hồ sơ adapter endpoint phải là URL https:// (file:// chỉ cho fixture)")


def bam_ho_so(hoso: dict) -> str:
    """Digest = sha256(JSON UTF-8, sort_keys, separators `,`/`:`) — MỘT phép so duy nhất với mỏ neo."""
    return hashlib.sha256(json.dumps(hoso, sort_keys=True, separators=(",", ":"),
                                     ensure_ascii=False).encode("utf-8")).hexdigest()


def kham_pha_nguon(endpoint: str | None = None, *, hoso: dict | None = None, da_duyet=None,
                   giao_thuc_cho_phep=("https",), thu_muc_tam: Path | None = None) -> tuple:
    """Q4.1/Q4.3 — MỘT lời gọi discovery qua adapter: `ls-remote --symref <endpoint> HEAD refs/heads/*`.

    Trả ``(nhanh_mac_dinh, {tên: SHA40}, digest)``. `endpoint`/`hoso`/`da_duyet` là API NỘI BỘ cho fixture;
    CLI production KHÔNG có cờ nào tới được ba tham số này. Hồ sơ đo được phải có digest NẰM TRONG mỏ neo
    đã duyệt, nếu không ⇒ 12 — với `PROFILE_ADAPTER_DA_DUYET` rỗng của A0 thì production luôn 12, đúng
    thiết kế: nền được tin là quyết định chủ kho, không phải thứ mã tự công nhận.
    """
    import tempfile
    git_exe = _git_exe_toi_thieu()
    hoso = hoso if hoso is not None else hoso_adapter_do(git_exe)
    kiem_mien_ho_so(hoso)                       # F08: miền TRƯỚC, digest SAU
    if hoso.get("git_path") != git_exe:
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: hồ sơ adapter không khớp executable git đã giải")
    digest = bam_ho_so(hoso)
    neo = PROFILE_ADAPTER_DA_DUYET if da_duyet is None else frozenset(da_duyet)
    if digest not in neo:
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: profile adapter {digest[:12]}… CHƯA được duyệt "
                   f"(mỏ neo có {len(neo)} digest) — nền thực thi production là quyết định chủ kho (ADR-0047)")
    endpoint = endpoint or hoso.get("endpoint") or ("https://" + KHO_CANONICAL)
    with tempfile.TemporaryDirectory(prefix="adapter_") as td:
        git_dir = _repo_tam_co_lap(git_exe, Path(td))
        mt = _env_rong(git_exe, git_dir, td, GIT_ALLOW_PROTOCOL=":".join(giao_thuc_cho_phep))
        lenh = [git_exe, "-c", "protocol.allow=never"]
        for gt in giao_thuc_cho_phep:
            lenh += ["-c", f"protocol.{gt}.allow=always"]
        for khoa, gia_tri in (("http.sslCAInfo", hoso.get("http_sslCAInfo")),
                              ("http.sslCAPath", hoso.get("http_sslCAPath")),
                              ("http.proxy", hoso.get("proxy"))):
            if gia_tri:
                lenh += ["-c", f"{khoa}={gia_tri}"]
        lenh += ["ls-remote", "--symref", endpoint, "HEAD", "refs/heads/*"]
        p = subprocess.run(lenh, capture_output=True, text=True, env=mt)
    if p.returncode != 0:
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: discovery rc={p.returncode}: {(p.stderr or '').strip()[:160]}")
    mac_dinh, quang_ba = None, {}
    for dong in p.stdout.splitlines():
        if dong.startswith("ref: "):
            ref, _, dich = dong[5:].partition("\t")
            if dich == "HEAD" and ref.startswith("refs/heads/"):
                if mac_dinh is not None:
                    raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: advertisement có nhiều symref HEAD")
                mac_dinh = ref[len("refs/heads/"):]
            continue
        cot = dong.split("\t")
        if len(cot) == 2 and cot[1].startswith("refs/heads/") and SHA40.match(cot[0]):
            quang_ba[cot[1][len("refs/heads/"):]] = cot[0]
    if not mac_dinh or mac_dinh not in quang_ba:
        raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: máy chủ không quảng bá symref HEAD hợp lệ — không fallback")
    return mac_dinh, quang_ba, digest


def so_map_cuc_bo(goc: Path, quang_ba: dict) -> dict:
    """Q4.2/Q4.4 — map remote-tracking chụp cục bộ phải có MỌI tên máy chủ với CÙNG SHA40; local heads không bù."""
    out = _git(goc, "for-each-ref", "--format=%(refname) %(objectname)", "refs/remotes/origin")
    cuc_bo = {}
    for dong in out.splitlines():
        ref, _, sha = dong.partition(" ")
        if ref.endswith("/HEAD"):
            continue
        cuc_bo[ref[len("refs/remotes/origin/"):]] = sha
    lech = [(ten, sha, cuc_bo.get(ten)) for ten, sha in quang_ba.items() if cuc_bo.get(ten) != sha]
    if lech:
        ten, sha, cb = lech[0]
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: map cục bộ lệch máy chủ ở {len(lech)} tên; ví dụ {ten}: "
                   f"máy chủ {sha[:12]} vs cục bộ {(cb or '<thiếu>')[:12]}")
    return cuc_bo


class KhoObject:
    """Q4.5 — API object-store đã xác minh: `GIT_DIR` tạm cô lập + `GIT_OBJECT_DIRECTORY` của kho nguồn
    (giải bằng API Git, không ghép literal), `cat-file --batch` với no-replace, băm lại từng object,
    cạnh lấy từ bytes đã băm, memo `(expected_type, OID)`, ngân sách có đơn vị + deadline monotonic.

    `sau_cat_file` là SEAM cho ca âm của điều phối (bytes lệch OID sau framing, trước băm); `bay_gio` là
    clock tiêm cho ca deadline. Cả hai là API nội bộ, không có đường CLI.
    """

    def __init__(self, goc_kho: Path, *, ngan_sach: dict | None = None, sau_cat_file=None,
                 bay_gio=None, deadline: float | None = None):
        import tempfile
        import time
        self.ngan_sach = dict(NGAN_SACH_MAC_DINH, **(ngan_sach or {}))
        self._sau_cat_file = sau_cat_file
        self._clock = bay_gio or time.monotonic
        self.deadline = deadline if deadline is not None else self._clock() + self.ngan_sach["max_reader_wall_seconds"]
        self.git_exe = _git_exe_toi_thieu()
        goc_kho = Path(goc_kho).resolve()
        # F09: preflight NGUỒN cũng đi bằng git tuyệt đối + env từ rỗng (không GIT_DIR/GIT_*/HOME của caller),
        # cùng biên cô lập với reader — giải bare/working/linked worktree bằng chính API Git qua `-C`.
        if self._git_nguon(goc_kho, "rev-parse", "--is-shallow-repository").strip() == "true":
            raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: kho nguồn shallow — object thiếu là hợp lệ, không đọc được đồ thị")
        obj = self._git_nguon(goc_kho, "rev-parse", "--git-path", "objects").strip()
        self.object_dir = str((goc_kho / obj).resolve()) if not Path(obj).is_absolute() else str(Path(obj).resolve())
        if not Path(self.object_dir).is_dir():
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: object directory không tồn tại: {self.object_dir}")
        self.alternates = self._kiem_alternates(self.object_dir)
        self._td = tempfile.TemporaryDirectory(prefix="khoobj_")
        self.git_dir = _repo_tam_co_lap(self.git_exe, Path(self._td.name))
        self.env = _env_rong(self.git_exe, self.git_dir, self._td.name,
                             GIT_OBJECT_DIRECTORY=self.object_dir,
                             GIT_ALTERNATE_OBJECT_DIRECTORIES=os.pathsep.join(self.alternates))
        self.memo: dict = {}
        self.so_object = 0
        self.tong_bytes = 0

    def _git_nguon(self, goc: Path, *doi_so) -> str:
        p = subprocess.run([self.git_exe, "-C", str(goc), *doi_so], capture_output=True, text=True,
                           env=_env_rong(self.git_exe, None, tempfile_home()))
        if p.returncode != 0:
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: git {' '.join(doi_so)} rc={p.returncode}: "
                                          f"{(p.stderr or '').strip().splitlines()[:1]}")
        return p.stdout

    def _kiem_alternates(self, goc_store: str) -> list[str]:
        """Preflight alternate: DAG store, đếm store phân biệt ngoài primary và depth theo đường dài nhất."""
        stores, tham = [], {}
        def di(store: str, sau: int, duong: tuple):
            if sau > self.ngan_sach["max_alternate_depth"]:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: alternate depth {sau} > {self.ngan_sach['max_alternate_depth']}")
            tep = Path(store) / "info" / "alternates"
            if not tep.is_file():
                return
            for dong in tep.read_text(encoding="utf-8", errors="replace").splitlines():
                dong = dong.strip()
                if not dong or dong.startswith("#"):
                    continue
                st = str((Path(store) / dong).resolve()) if not Path(dong).is_absolute() else str(Path(dong).resolve())
                if st in duong:
                    raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: alternate có vòng")
                if not Path(st).is_dir():
                    raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: alternate không đọc được: {st}")
                if st not in stores:
                    stores.append(st)
                    if len(stores) > self.ngan_sach["max_alternate_stores"]:
                        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: > {self.ngan_sach['max_alternate_stores']} alternate store")
                tham[st] = max(tham.get(st, 0), sau + 1)
                di(st, sau + 1, duong + (st,))
        di(goc_store, 0, (goc_store,))
        return stores

    def _con_thoi_gian(self, o_dau: str) -> float:
        con = self.deadline - self._clock()
        if con <= 0:
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: hết deadline reader tại {o_dau}")
        return con

    def doc(self, oid: str, loai_mong_doi: str) -> bytes:
        """Đọc MỘT object: framing → kiểm size (object VÀ tổng) trước khi nhận body → băm bằng OID → so type.
        Deadline áp ở MỌI cửa: cache-hit, trước spawn, sau khi child hoàn tất, trước khi trả (F04). Child bị
        kill/reap trong `finally` ở mọi đường thoát; rc≠0 của cat-file ⇒ 12 (F05)."""
        import threading
        if not SHA40.match(oid or ""):
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: OID không hợp lệ {oid!r}")
        khoa = (loai_mong_doi, oid)
        self._con_thoi_gian(f"memo {oid[:12]}")
        if khoa in self.memo:
            return self.memo[khoa]
        if any(k[1] == oid and k[0] != loai_mong_doi for k in self.memo):
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: OID {oid[:12]} bị yêu cầu hai type khác nhau")
        if self.so_object + 1 > self.ngan_sach["max_unique_objects"]:
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: > {self.ngan_sach['max_unique_objects']} object phân biệt")
        con = self._con_thoi_gian(f"trước spawn cat-file {oid[:12]}")
        # session riêng để kill được CẢ NHÓM (một helper con giữ pipe sẽ làm close() treo tới khi nó tự thoát);
        # `start_new_session` là API POSIX — nền không có thì bỏ qua, chỉ còn kill tiến trình trực tiếp.
        p = subprocess.Popen([self.git_exe, "--no-replace-objects", "cat-file", "--batch"],
                             stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=self.env,
                             start_new_session=hasattr(os, "killpg"))
        ket_qua: dict = {}
        tong_truoc = self.tong_bytes

        def _doc_thuc():
            try:
                p.stdin.write((oid + "\n").encode("ascii")); p.stdin.close()
                dau = p.stdout.readline().decode("ascii", "replace").rstrip("\n")
                ket_qua["dau"] = dau
                cot = dau.split()
                if len(cot) == 3 and cot[2].isdigit():
                    kich = int(cot[2])
                    if kich > self.ngan_sach["max_object_bytes"]:
                        ket_qua["qua_lon"] = kich
                        return
                    if tong_truoc + kich > self.ngan_sach["max_total_object_bytes"]:
                        ket_qua["qua_tong"] = kich      # F05: kiểm TỔNG từ header, trước khi cấp phát body
                        return
                    ket_qua["than"] = p.stdout.read(kich + 1)
            except Exception as e:  # noqa: BLE001
                ket_qua["loi"] = repr(e)

        t = threading.Thread(target=_doc_thuc, daemon=True)
        try:
            t.start(); t.join(timeout=con)
            if t.is_alive():
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: hết deadline reader khi đọc {oid[:12]} (đã kill cat-file)")
            if "qua_lon" in ket_qua:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: object {oid[:12]} {ket_qua['qua_lon']} B > max_object_bytes")
            if "qua_tong" in ket_qua:
                raise Chan(RC_KHONG_XAC_DINH, "KHÔNG_XÁC_ĐỊNH: vượt max_total_object_bytes")
            if "loi" in ket_qua:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: cat-file lỗi I/O: {ket_qua['loi'][:120]}")
            con2 = self._con_thoi_gian(f"chờ cat-file {oid[:12]} kết thúc")
            try:
                rc = p.wait(timeout=con2)
            except subprocess.TimeoutExpired:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: hết deadline reader chờ cat-file {oid[:12]} kết thúc") from None
            if rc != 0:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: cat-file rc={rc} cho {oid[:12]} — không dùng bytes của tiến trình lỗi")
            cot = (ket_qua.get("dau") or "").split()
            if len(cot) != 3 or cot[0] != oid or not cot[2].isdigit():
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: object {oid[:12]} `{ket_qua.get('dau', '')}` — `missing` là 12, không phải 'vắng'")
            loai_that, kich = cot[1], int(cot[2])
            than = ket_qua.get("than", b"")
            if len(than) != kich + 1:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: object {oid[:12]} framing ngắn ({len(than)}/{kich + 1})")
            than = than[:kich]
            if self._sau_cat_file is not None:   # SEAM ca âm (điều phối dựng), trước băm
                loai_that, kich, than = self._sau_cat_file(oid, loai_that, kich, than)
            bam = hashlib.sha1(f"{loai_that} {len(than)}\0".encode("ascii") + than).hexdigest()
            if bam != oid:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: bytes của {oid[:12]} băm ra {bam[:12]} — cache không tin cậy")
            if loai_that != loai_mong_doi:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {oid[:12]} là {loai_that}, mong đợi {loai_mong_doi}")
            self._con_thoi_gian(f"trước khi trả {oid[:12]}")
            self.so_object += 1
            self.tong_bytes += kich
            self.memo[khoa] = than
            return than
        finally:
            if p.poll() is None:
                try:
                    getattr(os, "killpg")(p.pid, 9)
                except Exception:  # noqa: BLE001 — không có killpg / nhóm đã chết: kill trực tiếp
                    p.kill()
                p.wait()
            if not t.is_alive():   # thread còn kẹt trong read() thì close() sẽ treo — nó là daemon, để nó chết cùng tiến trình
                for luong in (p.stdin, p.stdout, p.stderr):
                    try:
                        luong.close()
                    except Exception:  # noqa: BLE001
                        pass

    def commit(self, oid: str) -> tuple:
        """Trả ``(tree, [parents])`` từ header của bytes đã băm."""
        than = self.doc(oid, "commit")
        dau, _, _ = than.partition(b"\n\n")
        tree, cha = None, []
        for dong in dau.decode("utf-8", "replace").splitlines():
            if dong.startswith("tree "):
                tree = dong[5:].strip()
            elif dong.startswith("parent "):
                cha.append(dong[7:].strip())
        if not tree or not SHA40.match(tree) or any(not SHA40.match(c) for c in cha):
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: commit {oid[:12]} header hỏng")
        return tree, cha

    def tree(self, oid: str) -> list:
        """Entry ``(mode, tên, OID, type)`` parse từ bytes nhị phân đã băm — không `ls-tree`."""
        than = self.doc(oid, "tree")
        ket, i, da_thay = [], 0, set()
        while i < len(than):
            j = than.find(b"\0", i)
            if j < 0 or j + 21 > len(than):
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: tree {oid[:12]} entry cụt")
            mode_b, sep, ten_b = than[i:j].partition(b" ")
            mode = mode_b.decode("ascii", "replace")
            # F03: băm đúng chỉ chứng minh BYTES; cấu trúc entry phải hợp lệ mới được suy "vắng" từ nó.
            if not sep or mode not in ("100644", "100755", "120000", "160000", "40000"):
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: tree {oid[:12]} entry mode không hợp lệ {mode!r}")
            try:
                ten = ten_b.decode("utf-8")
            except UnicodeDecodeError:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: tree {oid[:12]} tên entry không phải UTF-8") from None
            if not ten or ten in (".", "..") or "/" in ten or ".git" == ten or ten in da_thay:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: tree {oid[:12]} tên entry không hợp lệ/trùng {ten!r}")
            da_thay.add(ten)
            sha = than[j + 1:j + 21].hex()
            loai = "tree" if mode == "40000" else "commit" if mode == "160000" else "blob"
            ket.append((mode.zfill(6) if loai == "tree" else mode, ten, sha, loai))
            i = j + 21
        return ket

    def to_tien(self, S: str, H: str) -> int:
        """S là tổ tiên của H? Tự đi đồ thị parent từ H (bytes đã băm), visited-set, biên parent inclusive.
        Trả số cạnh của đường witness; không thấy ⇒ 12."""
        gioi_han = self.ngan_sach["max_parent_path_edges"]
        if S == H:
            self.commit(H)
            return 0
        ngan, tham = [(H, 0)], set()
        while ngan:
            oid, sau = ngan.pop()
            if oid in tham:
                continue
            tham.add(oid)
            _, cha = self.commit(oid)
            for c in cha:
                # Biên INCLUSIVE, kiểm TRƯỚC khi nhận witness: đường đúng `bound` cạnh là hợp lệ,
                # `bound + 1` ⇒ 12 kể cả khi cạnh ấy dẫn thẳng tới S (S8: bound−1/bound/bound+1).
                if sau + 1 > gioi_han:
                    raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: đường parent > {gioi_han} cạnh")
                if c == S:
                    self.commit(S)
                    return sau + 1
                ngan.append((c, sau + 1))
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: S {S[:12]} không phải tổ tiên của H {H[:12]}")

    def tim(self, tree_oid: str, duong: str):
        """Resolve MỘT đường trong cây theo entry đã băm; trả ``(mode, OID, type)`` hoặc ``None`` nếu tree cha
        đã xác minh không có entry. Đếm `max_tree_or_alias_edges` cho lần resolve này."""
        buoc, oid, loai, mode = 0, tree_oid, "tree", "040000"
        for phan in duong.split("/"):
            if loai != "tree":
                # Tổ tiên là blob/symlink/gitlink: cấu trúc KHÔNG xác minh được, không phải "vắng" — trả None
                # ở đây từng biến H thay `ops` bằng một blob thành `TAP_THU_HOI_RONG` rc=0 (Codex review 457affd, P1).
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: tổ tiên của {duong} không phải thư mục (mode {mode} {loai}) — không suy vắng")
            buoc += 1
            if buoc > self.ngan_sach["max_tree_or_alias_edges"]:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: resolve {duong} > {self.ngan_sach['max_tree_or_alias_edges']} cạnh")
            muc = next((e for e in self.tree(oid) if e[1] == phan), None)
            if muc is None:
                return None
            mode, _, oid, loai = muc
        return mode, oid, loai

    def namespace(self, tree_oid: str, thu_muc: str) -> dict:
        """Map ``path → (mode, type, OID)`` của MỌI entry ngay dưới `thu_muc` (kể cả thư mục con/symlink,
        để validator từ chối chứ không bỏ qua). Tree cha vắng entry ⇒ map rỗng, đã được chứng minh."""
        muc = self.tim(tree_oid, thu_muc)
        if muc is None:
            return {}
        mode, oid, loai = muc
        if loai != "tree":
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {thu_muc} không phải thư mục (mode {mode})")
        return {f"{thu_muc}/{ten}": (m, l, o) for m, ten, o, l in self.tree(oid)}

    def dong(self):
        self._td.cleanup()


def _ls_tree_z(goc: Path, ref: str, thu_muc: str, de_quy: bool = True) -> list[tuple]:
    """`ls-tree -r -z` — tên đi NUL-delimited, KHÔNG qua lớp quote của Git (F02: tên Unicode thường như
    `thu hồi.yaml` bị quote thành `"thu h\\341\\273\\223i.yaml"` và dispatcher không thấy tiền tố).
    Đi qua `GOI_GIT` (cùng cửa với luật cũ, để đồ giả trạng thái của bộ test thay được); tên không phải
    UTF-8 làm lớp text của cửa ấy ném ⇒ 12, không traceback. `de_quy=False` liệt kê ĐÚNG entry `thu_muc`
    (không `-r`) — dùng để hỏi kiểu của một tổ tiên."""
    try:
        if de_quy:
            p = GOI_GIT("ls-tree", "-r", "-z", ref, "--", thu_muc, cwd=goc)
        else:
            p = GOI_GIT("ls-tree", "-z", ref, "--", thu_muc, cwd=goc)
    except OSError as e:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: không gọi được git: {e}") from None
    except UnicodeDecodeError:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: ls-tree -z {ref} có tên không phải UTF-8") from None
    if p.returncode != 0:
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: git ls-tree -z {ref} rc={p.returncode}: "
                                      f"{(p.stderr or '').strip()[:160]}")
    ket = []
    for muc in (p.stdout or "").split("\0"):
        if not muc:
            continue
        meta, sep, duong = muc.partition("\t")
        cot = meta.split()
        if not sep or len(cot) != 3:
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: ls-tree -z có mục hỏng: {muc[:80]!r}")
        ket.append((cot[0], cot[1], cot[2], duong))
    return ket


def _quet_so_thu_hoi_moi_ref(goc: Path, refs: list[str]) -> list[dict]:
    """Chế độ CHƯA KÍCH HOẠT: mọi entry trong `ops/thu-hoi/` trên BẤT KỲ ref nào đều được liệt kê;
    consumer vận hành gọi hàm này và ĐỎ (12) khi có bản ghi thu hồi. Lọc theo path trong mã, không tin
    bộ lọc của `ls-tree`. Chính namespace `ops/thu-hoi` mà không phải thư mục (blob/gitlink) ⇒ 12, không
    suy thành "sổ vắng" (F02)."""
    ket = []
    # `ten_ref` chứ không phải `ref`: mutant A1 của t94 neo chuỗi lặp-theo-ref của `_quet_lease_toan_kho` phải giữ DUY NHẤT.
    for ten_ref in refs:
        _kiem_to_tien_la_tree(goc, ten_ref, THU_MUC_SO)
        for mode, loai, oid, duong in _ls_tree_z(goc, ten_ref, THU_MUC_SO):
            if duong == THU_MUC_SO:
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: {THU_MUC_SO} tại {ten_ref} không phải thư mục (mode {mode} {loai})")
            tuyen = phan_tuyen_so(duong)
            if tuyen is None:
                continue
            ket.append({"ref": ten_ref, "path": duong, "mode": mode, "type": loai, "oid": oid, "tuyen": tuyen})
    return ket


def _kiem_to_tien_la_tree(goc: Path, ref: str, thu_muc: str) -> None:
    """Mọi tổ tiên của `thu_muc` trên `ref` phải là TREE. `ls-tree -r ref -- ops/thu-hoi` trả RỖNG khi `ops` là
    blob/symlink/gitlink — trông y hệt "sổ vắng" và consumer từng đi tiếp rc=0 (Codex review 457affd, P1, cùng
    lớp F02 "namespace không phải thư mục ⇒ 12")."""
    phan = thu_muc.split("/")
    for i in range(1, len(phan)):
        tien_to = "/".join(phan[:i])
        for mode, loai, _oid, duong in _ls_tree_z(goc, ref, tien_to, de_quy=False):
            if duong == tien_to and loai != "tree":
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: {tien_to} tại {ref} không phải thư mục (mode {mode} {loai}) — "
                           f"không suy {thu_muc} vắng")


def _doc_blob_text_12(goc: Path, ref: str, duong: str):
    """Đọc blob `ref:duong` qua `GOI_GIT` (text). Vắng/rc≠0 ⇒ ``None``; không giải mã được ⇒ 12 (F10 lượt 2)."""
    try:
        p = GOI_GIT("cat-file", "blob", f"{ref}:{duong}", cwd=goc)
    except UnicodeDecodeError:   # nguồn không phải UTF-8 là 12, không traceback
        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong} tại {ref} không phải UTF-8") from None
    if p is None or p.returncode != 0:
        return None
    return (p.stdout or "").encode("utf-8")


def _kiem_so_rong_khi_chua_kich_hoat(goc: Path, refs: list[str]) -> None:
    if SO_THU_HOI_KICH_HOAT:
        return
    for muc in _quet_so_thu_hoi_moi_ref(goc, refs):
        if muc["tuyen"] == "thu_hoi":
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: SO_THU_HOI_KICH_HOAT=False mà sổ có bản ghi {muc['path']} tại "
                       f"{muc['ref']} — bản ghi lọt trước kích hoạt: dừng, phục hồi có audit, không grandfather")
        if muc["tuyen"] == "metadata":
            # Marker PHẢI qua đúng schema sáu khoá TRƯỚC khi hỏi policy — Q13 "mọi lỗi metadata ⇒ 12". Trước đây
            # consumer chỉ hỏi policy nên marker RÁC + policy `{}` đi qua rc=0 (Codex review 457affd, P2).
            kiem_metadata_retired(muc["path"], muc["mode"], muc["type"],
                                  _doc_blob_text_12(goc, muc["ref"], muc["path"]) or b"")
            noi_dung_p = _doc_blob_text_12(goc, muc["ref"], PATH_POLICY_CLOSURE)   # policy không UTF-8 ⇒ 12 (F10 lượt 2)
            if noi_dung_p is None or _doc_policy_json(noi_dung_p) is None:
                raise Chan(RC_KHONG_XAC_DINH,
                           f"KHÔNG_XÁC_ĐỊNH: {muc['path']} có mặt tại {muc['ref']} mà policy {PATH_POLICY_CLOSURE} "
                           f"vắng hoặc không phải JSON object (Q13)")


def _doc_policy_json(noi_dung: bytes):
    """Policy closure phải là JSON OBJECT (F01); mọi thứ khác ⇒ ``None``."""
    try:
        d = json.loads(noi_dung.decode("utf-8"))
    except (ValueError, UnicodeDecodeError):
        return None
    return d if isinstance(d, dict) else None


def _du_bao_check(lease: dict, goc: Path, nhanh_mac_dinh: str) -> list[str]:
    """M3 dự báo — luật mới (precedence Q3) trên ref canonical CỤC BỘ; KHÔNG đổi rc, chỉ in `DU_BAO:`."""
    # wp678 D8: chốt RIÊNG — `lenh_check` đã qua D1, nhưng hàm này không dựa vào đó (A7).
    lease_id = _lease_id_hop_le(lease.get("lease_id"))
    dong = [f"DU_BAO: chế độ CHƯA KÍCH HOẠT (SO_THU_HOI_KICH_HOAT={SO_THU_HOI_KICH_HOAT}); verdict sản phẩm = luật cũ"]
    ref = f"refs/remotes/origin/{nhanh_mac_dinh}"
    so = {m["path"]: m for m in _quet_so_thu_hoi_moi_ref(goc, [ref])} if _ref_ton_tai(goc, ref) else None
    if so is None:
        dong.append(f"DU_BAO: ref canonical {ref} KHÔNG có trong cache — dự báo KHÔNG ĐO ĐƯỢC")
        return dong
    dong.append(f"DU_BAO: sổ tại {ref}: {len(so)} entry (discovery qua adapter KHÔNG chạy — profile chưa duyệt)")
    thay_the = _danh_sach_thay_the_cho(lease.get("thay_the_cho")) or []
    for x in thay_the:
        muc = so.get(f"{THU_MUC_SO}/{x}.yaml")
        if muc:
            try:
                d = kiem_ban_ghi_thu_hoi(muc["path"], muc["mode"], muc["type"],
                                         GOI_GIT("cat-file", "-p", muc["oid"], cwd=goc).stdout.encode("utf-8"))
                dich = d["cap_lai_cho"]
                rc = 0 if dich in (None, lease_id) else 8
                dong.append(f"DU_BAO: sổ có {x}: cap_lai_cho={dich!r} ⇒ rc dự báo {rc}")
            except Chan as e:
                dong.append(f"DU_BAO: sổ có {x} nhưng bản ghi hỏng ⇒ rc dự báo {e.ma}: {e.thong_diep[:100]}")
        elif any(x == cu and lease_id == moi for cu, moi, *_ in BIA_MO_LICH_SU):
            dong.append(f"DU_BAO: {x} có trong BIA_MO_LICH_SU ⇒ rc dự báo 0")
        else:
            dong.append(f"DU_BAO: {x} không có trong sổ lẫn BIA_MO_LICH_SU ⇒ rc dự báo 8 (luật cũ: bia mộ hai chiều)")
    if f"{THU_MUC_SO}/{lease_id}.yaml" in so:
        dong.append("DU_BAO: chiều ngược — lease đang kiểm CÓ trong sổ ⇒ rc dự báo 8")
    return dong


def _du_bao_ai_dang_giu(goc: Path, refs: list[str], cac_lease: list[dict], nhanh_mac_dinh: str) -> list[str]:
    """M2 dự báo: MAP_REF theo cặp (blob, path) và áp sổ canonical cục bộ theo lease_id — không đổi rc."""
    dong = [f"DU_BAO: chế độ CHƯA KÍCH HOẠT (SO_THU_HOI_KICH_HOAT={SO_THU_HOI_KICH_HOAT}); verdict sản phẩm = luật cũ"]
    ref = f"refs/remotes/origin/{nhanh_mac_dinh}"
    so_ids = set()
    if _ref_ton_tai(goc, ref):
        so_ids = {Path(m["path"]).name[:-5] for m in _quet_so_thu_hoi_moi_ref(goc, [ref]) if m["tuyen"] == "thu_hoi"}
        dong.append(f"DU_BAO: sổ tại {ref}: {len(so_ids)} bản ghi (discovery qua adapter KHÔNG chạy — profile chưa duyệt)")
    else:
        dong.append(f"DU_BAO: ref canonical {ref} KHÔNG có trong cache — dự báo KHÔNG ĐO ĐƯỢC")
    map_ref: dict = {}
    for r in refs:
        for mode, loai, oid, duong in _ls_tree_z(goc, r, "ops/leases"):
            if loai == "blob":
                map_ref.setdefault((oid, duong), []).append(r)
    for muc in cac_lease:
        # wp678 D8 (Q3): lease sai kiểu KHÔNG được ép sang chuỗi để tra sổ thu hồi (`1_000` từng tra ra `1000`).
        lid = _lease_id_quet(muc["lease"].get("lease_id"))
        if lid is None:
            dong.append(f"DU_BAO: KHÔNG_XÁC_ĐỊNH lease_id {_nhan_lease_id_sai(muc['lease'].get('lease_id'))} "
                        f"tại {muc['ref']}:{muc['path']} — không tra sổ")
            continue
        nhan = " · ĐÃ_THU_HỒI" if lid in so_ids else ""
        dong.append(f"DU_BAO: {lid}{nhan}\tMAP_REF {len(map_ref.get((muc['blob'], muc['path']), []))} ref")
    dong.append(f"DU_BAO: MÙ 0 · {len(refs)} ref")
    return dong


def lenh_kiem_thu_hoi_github(a) -> int:
    """M4 — cổng tiếp nhận: ancestry S→H, T = tree(H), map append-only, validator toàn namespace T,
    receipt S/H/T. Chế độ chưa kích hoạt: tập revocation phải RỖNG ở cả S lẫn T."""
    S, H = str(a.canonical_base).strip(), str(a.H).strip()
    if not SHA40.match(S) or not SHA40.match(H):
        raise Chan(RC_THAM_SO, "S và H phải là SHA40 hex thường")
    if not a.nhanh_mac_dinh or "/" in a.nhanh_mac_dinh:
        raise Chan(RC_THAM_SO, "--nhanh-mac-dinh bắt buộc, là TÊN nhánh do workflow truyền")
    goc = Path(a.goc or ".").resolve()
    kho = KhoObject(goc)
    try:
        canh = kho.to_tien(S, H)
        tree_S, _ = kho.commit(S)
        tree_T, _ = kho.commit(H)
        map_S = kho.namespace(tree_S, THU_MUC_SO)
        map_T = kho.namespace(tree_T, THU_MUC_SO)
        # Append-only TRƯỚC validator T (Q13/S7): entry ở S phải nguyên vẹn ở T.
        for duong, bo in map_S.items():
            if map_T.get(duong) != bo:
                raise Chan(RC_NOI_DUNG, f"append-only: {duong} tại S {bo} nhưng tại T {map_T.get(duong)}")
        # Q13 (F01): policy ở T phải là regular blob JSON OBJECT — đọc qua reader đã băm; có mặt thôi chưa đủ.
        policy_T = None
        muc_policy = kho.tim(tree_T, PATH_POLICY_CLOSURE)
        if muc_policy is not None:
            mode_p, oid_p, loai_p = muc_policy
            if loai_p != "blob" or mode_p != "100644":
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: policy {PATH_POLICY_CLOSURE} ở T không phải regular blob 100644")
            bytes_p = kho.doc(oid_p, "blob")
            if _doc_policy_json(bytes_p) is None:
                raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: policy {PATH_POLICY_CLOSURE} ở T không phải JSON object")
            policy_T = (oid_p, hashlib.sha256(bytes_p).hexdigest())
        thu_hoi_S = [p for p in map_S if phan_tuyen_so(p) == "thu_hoi"]
        thu_hoi_T, metadata_T = [], []
        for duong, (mode, loai, oid) in sorted(map_T.items()):
            tuyen = phan_tuyen_so(duong)
            if tuyen == "metadata":
                d_meta = kiem_metadata_retired(duong, mode, loai, kho.doc(oid, "blob") if loai == "blob" else b"")
                if policy_T is None:
                    raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong} có mà policy {PATH_POLICY_CLOSURE} vắng/hỏng ở T (Q13)")
                if duong not in map_S:
                    # Marker MỚI ⇒ transition Q13: descriptor đã ghim · hash policy ĐẦU TIÊN = policy T ·
                    # base_sha_before_add == S · S chưa có policy. Marker cũ (đã ở S) chỉ cần append-only ở trên.
                    if DESCRIPTOR_Q13_SHA256 is None:
                        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong} là marker MỚI mà descriptor Q13 chưa được ghim (A1) — A0 không tạo marker")
                    if d_meta["descriptor_sha256"] != DESCRIPTOR_Q13_SHA256:
                        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: descriptor_sha256 không khớp nguồn đã ghim")
                    if d_meta["first_policy_sha256"] != policy_T[1]:
                        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: first_policy_sha256 không bằng sha256 policy tại T")
                    if d_meta["base_sha_before_add"] != S:
                        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: base_sha_before_add phải bằng S {S[:12]}")
                    if kho.tim(tree_S, PATH_POLICY_CLOSURE) is not None:
                        raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: {duong}: S đã có policy mà marker mới xuất hiện — không grandfather")
                metadata_T.append(duong)
            else:
                kiem_ban_ghi_thu_hoi(duong, mode, loai, kho.doc(oid, "blob") if loai == "blob" else b"")
                thu_hoi_T.append(duong)
        if policy_T is not None and not metadata_T:
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: T có policy {PATH_POLICY_CLOSURE} mà thiếu marker {PATH_NGOAI_LE_RETIRED} (Q13) — không grandfather")
        if not SO_THU_HOI_KICH_HOAT and (thu_hoi_S or thu_hoi_T):
            raise Chan(RC_KHONG_XAC_DINH,
                       f"KHÔNG_XÁC_ĐỊNH: chế độ CHƯA KÍCH HOẠT đòi tập revocation RỖNG — S có {len(thu_hoi_S)}, T có {len(thu_hoi_T)}")
        bo_kiem = kho.tim(tree_S, PATH_BO_KIEM)
        receipt = {
            "schema_version": 1, "event": "thu_hoi_admission_receipt", "che_do": "chua_kich_hoat",
            "kho_canonical": KHO_CANONICAL, "nhanh_mac_dinh": a.nhanh_mac_dinh,
            "S": S, "H": H, "T": tree_T, "tree_S": tree_S, "canh_ancestry": canh,
            "so_thu_hoi_S": {p: list(v) for p, v in map_S.items()},
            "so_thu_hoi_T": {p: list(v) for p, v in map_T.items()},
            "metadata_T": metadata_T, "thu_hoi_moi": [p for p in thu_hoi_T if p not in map_S],
            "oid_bo_kiem_tai_S": bo_kiem[1] if bo_kiem else None,
            "policy_T": {"oid": policy_T[0], "sha256": policy_T[1]} if policy_T else None,
            "descriptor_q13_ghim": DESCRIPTOR_Q13_SHA256,
            "profile_digest": None,
            "discovery": "KHONG_CHAY: A0 chưa kích hoạt; PROFILE_ADAPTER_DA_DUYET rỗng (quyết định chủ kho)",
            "ngan_sach": kho.ngan_sach, "so_object_da_doc": kho.so_object, "tong_bytes": kho.tong_bytes,
            "ket_luan": "TAP_THU_HOI_RONG", "thoi_diem_utc": datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ"),
        }
    finally:
        kho.dong()
    van = json.dumps(receipt, ensure_ascii=False, sort_keys=True, indent=1)
    if getattr(a, "receipt", None):
        Path(a.receipt).write_text(van + "\n", encoding="utf-8")
    print(f"THU_HOI_ADMISSION {receipt['ket_luan']}: S={S[:12]} H={H[:12]} T={tree_T[:12]} "
          f"ancestry={canh} cạnh; sổ S={len(map_S)} T={len(map_T)} entry; object đã băm={kho.so_object}")
    return RC_OK


def lenh_check(a) -> int:
    lease, neo = kiem(_doc_yaml(a.tep), a.tep, getattr(a, "goc", None))
    # A0 (spec r9 M3): verdict `check` = LUẬT CŨ, bộ kiểm THUẦN (t53: chạy được trong Actions không git/gh).
    # Chỉ khi `--du-bao` mới chạm git: chốt "sổ không rỗng khi cờ False ⇒ 12" + in `DU_BAO:`; rc không đổi.
    if getattr(a, "du_bao", False):
        goc_check = _goc_kho(Path(a.tep), getattr(a, "goc", None))
        if not (goc_check / ".git").exists():
            raise Chan(RC_KHONG_XAC_DINH, f"KHÔNG_XÁC_ĐỊNH: --du-bao cần một kho git tại {goc_check}")
        _, refs = _cac_ref_cuc_bo(goc_check)
        _kiem_so_rong_khi_chua_kich_hoat(goc_check, refs)
        for dong in _du_bao_check(lease, goc_check, getattr(a, "nhanh_mac_dinh", None) or "master"):
            print(dong)
    print("LỆNH check KHÔNG CHẠY hai lớp GitHub: đo ISSUE/PR và dò comment; dùng `kiem-github`")
    print(f"lease {lease['lease_id']} ĐĂNG ĐƯỢC — issue #{lease['packet_issue']}, "
          f"neo {lease['reviewed_sha_required'][:12]}, hết hạn {lease['lease_expires_at_utc']}"
          + (f", prompt {lease['prompt_path']} khớp băm {neo[:12]}" if neo else ""))
    return RC_OK


def lenh_body(a) -> int:
    # Đi qua ĐÚNG bộ kiểm THUẦN của `check`; hai lớp GitHub do workflow gọi riêng.
    lease, _ = kiem(_doc_yaml(a.tep), a.tep, getattr(a, "goc", None))
    sys.stdout.write(dung_than(lease, a.tep))
    return RC_OK


def lenh_kiem_github(a) -> int:
    lease, _ = kiem_github(_doc_yaml(a.tep), a.tep, getattr(a, "goc", None))
    print(f"hai lớp GitHub ĐÃ QUA cho lease {lease['lease_id']} trên issue #{lease['packet_issue']}")
    return RC_OK


def lenh_ai_dang_giu(a) -> int:
    root = Path(a.goc or ".").resolve()
    print("PHẠM_VI: quét refs/heads/*; nhánh cục bộ tụt sau origin/<cùng tên> sẽ bị CHẶN")
    cac_lease = _quet_lease_toan_kho(root, chan_nhanh_tut_sau=True)
    # A0 (spec r9 M2): chế độ CHƯA KÍCH HOẠT — sổ thu hồi phải RỖNG trên mọi ref cục bộ (12 nếu không),
    # và luật mới CHỈ in ở `--du-bao`; verdict sản phẩm bên dưới vẫn là luật cũ (bia mộ hai chiều).
    _, refs_a0 = _cac_ref_cuc_bo(root)
    _kiem_so_rong_khi_chua_kich_hoat(root, refs_a0)
    if getattr(a, "du_bao", False):
        for dong in _du_bao_ai_dang_giu(root, refs_a0, cac_lease, getattr(a, "nhanh_mac_dinh", None) or "master"):
            print(dong)
    nguoi_giu = {}
    sai_kieu = 0
    for muc in cac_lease:
        lease = muc["lease"]
        if not _lease_cham_duong(lease, a.duong_dan):
            continue
        # wp678 D7 (Q3): `lease_id` không phải chuỗi hợp lệ thì KHÔNG ép thành khoá người giữ (`yes` và
        # `on` từng gộp về ``True``). In `KHÔNG_XÁC_ĐỊNH` cho TỪNG lease lỗi (kèm ref:path) rồi mới thoát
        # khác 0 — fail-close, không dừng ở lease lỗi đầu tiên để người đọc thấy đủ cả tập.
        lease_id = _lease_id_quet(lease.get("lease_id"))
        if lease_id is None:
            sai_kieu += 1
            print(f"KHÔNG_XÁC_ĐỊNH\tlease_id {_nhan_lease_id_sai(lease.get('lease_id'))}\t{muc['ref']}:{muc['path']}")
            continue
        trang_thai = _phan_loai_lease(lease)
        bia_mo = (_bia_mo_doi_xung(lease, cac_lease)
                  if trang_thai == "CÒN_HẠN" else None)
        if bia_mo is False:
            raise Chan(
                RC_KHONG_XAC_DINH,
                f"KHÔNG_XÁC_ĐỊNH: bia mộ một chiều {lease_id!r} -> "
                f"{lease.get('da_bi_thay_the')!r} tại {muc['ref']}:{muc['path']}; "
                "không tìm thấy lease thay thế trỏ ngược bằng thay_the_cho")
        da_chet = bia_mo is True
        nhan = " · ĐÃ_BỊ_THAY_THẾ" if da_chet else ""
        print(f"{trang_thai}{nhan}\t{lease_id}\t{muc['ref']}:{muc['path']}")
        if trang_thai == "CÒN_HẠN" and not da_chet:
            nguoi_giu[lease_id] = None
    if sai_kieu:
        raise Chan(RC_KHONG_XAC_DINH,
                   f"KHÔNG_XÁC_ĐỊNH: {sai_kieu} lease chạm {a.duong_dan} mang lease_id không hợp lệ (sai kiểu hoặc sai dạng) — "
                   "không kết luận được ai đang giữ (wp678 Q3)")
    print(f"NGƯỜI_GIỮ {len(nguoi_giu)}: " + (", ".join(sorted(nguoi_giu)) or "không có"))
    return RC_DANG_GIU if nguoi_giu else RC_OK


def _lease_id_hien_thi(lease: dict) -> str:
    """wp678 D9 — CHỈ để in: chuỗi hợp lệ in nguyên, còn lại in dạng thô có nhãn, KHÔNG `str()` thành danh tính."""
    lid = _lease_id_quet(lease.get("lease_id"))
    return lid if lid is not None else f"<lease_id không hợp lệ: {_repr_an_toan(lease.get('lease_id'))}>"


def lenh_con_tro_treo(a) -> int:
    """Quét ngược read-only; hồ sơ đã đăng không bao giờ bị sửa tại đây."""
    root = Path(a.goc or ".").resolve()
    tim_thay = goi_y = 0
    for muc in _quet_lease_toan_kho(root):
        lease = muc["lease"]
        if (_phan_loai_lease(lease) != "CÒN_HẠN"
                or bool(lease.get("da_bi_thay_the"))):
            continue
        for ten in _cac_con_tro_treo(lease):
            tim_thay += 1
            lease_id = _lease_id_hien_thi(lease)
            print(f"CON_TRỎ_TREO\t{lease_id}\t{ten}\t{muc['ref']}:{muc['path']}")
        for ten in _cac_nhac_mo_ho(lease):
            goi_y += 1
            lease_id = _lease_id_hien_thi(lease)
            print(f"CON_TRỎ_GỢI_Ý\t{lease_id}\t{ten}\t{muc['ref']}:{muc['path']}")
    print(f"CON_TRỎ_TREO {tim_thay}; chỉ báo cáo, không sửa lease đã đăng")
    print(f"CON_TRỎ_GỢI_Ý {goi_y}; văn xuôi chỉ là advisory")
    return RC_OK


def _them_co_du_bao(q) -> None:
    q.add_argument("--du-bao", dest="du_bao", action="store_true",
                   help="in dự báo luật mới (sổ thu hồi) dưới nhãn DU_BAO:; KHÔNG đổi mã thoát")
    q.add_argument("--nhanh-mac-dinh", dest="nhanh_mac_dinh", default=None,
                   help="tên nhánh mặc định cho dự báo (mặc định: master)")


def main(argv=None) -> int:
    for luong in (sys.stdout, sys.stderr):
        try:
            luong.reconfigure(encoding="utf-8", errors="replace")
        except (AttributeError, ValueError, OSError):
            pass
    ap = argparse.ArgumentParser(prog="lease_publish.py", description=__doc__.split("\n")[0])
    sub = ap.add_subparsers(dest="lenh", required=True)
    for ten, fn, mo_ta in (
        ("check", lenh_check, "kiểm lease có đăng được không"),
        ("body", lenh_body, "in thân comment ra stdout"),
        ("kiem-github", lenh_kiem_github, "đo loại số hiệu và comment đã đăng"),
    ):
        q = sub.add_parser(ten, help=mo_ta)
        q.add_argument("tep")
        # Mặc định gốc kho tự tìm bằng `.git`; cờ này để bộ phản chứng dựng được
        # một "kho" giả trong thư mục tạm mà không phải `git init`.
        q.add_argument("--root", dest="goc", default=None,
                       help="gốc kho để tính `prompt_path` (mặc định: tìm .git đi lên)")
        if ten == "check":
            _them_co_du_bao(q)
        q.set_defaults(fn=fn)
    q = sub.add_parser("ai-dang-giu", help="quét toàn kho xem ai đang giữ một đường dẫn")
    q.add_argument("duong_dan")
    q.add_argument("--root", dest="goc", default=".")
    _them_co_du_bao(q)
    q.set_defaults(fn=lenh_ai_dang_giu)
    q = sub.add_parser("kiem-thu-hoi-github",
                       help="M4 cổng tiếp nhận sổ thu hồi: ancestry S→H, map append-only, validator toàn namespace")
    q.add_argument("H", help="SHA40 head của PR (đã fetch vào object-store của kho)")
    q.add_argument("--canonical-base", dest="canonical_base", required=True, help="SHA40 base S (mã canonical đang chạy)")
    q.add_argument("--nhanh-mac-dinh", dest="nhanh_mac_dinh", required=True, help="tên nhánh mặc định (ghi vào receipt)")
    q.add_argument("--root", dest="goc", default=".")
    q.add_argument("--receipt", default=None, help="đường ghi receipt JSON (S/H/T + kết luận)")
    q.set_defaults(fn=lenh_kiem_thu_hoi_github)
    q = sub.add_parser("con-tro-treo",
                       help="liệt kê read-only lease còn hiệu lực có con trỏ treo")
    q.add_argument("--root", dest="goc", default=".")
    q.set_defaults(fn=lenh_con_tro_treo)

    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except Chan as e:
        print(f"CHAN [{e.ma}]: {e.thong_diep}", file=sys.stderr)
        return e.ma


if __name__ == "__main__":
    sys.exit(main())
