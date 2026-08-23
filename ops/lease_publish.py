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
  9  lease ĐÃ đăng rồi (trong tệp hoặc comment Issue) — BỎ QUA, không đăng lại
 10  lớp review khai không khớp lớp cổng tính từ write_set
"""

from __future__ import annotations

import argparse
import hashlib
import json
import os
import posixpath
import re
import subprocess
import sys
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
    return subprocess.run(["git", *doi_so], cwd=cwd, capture_output=True, text=True)


# Cùng danh sách với `.claude/dev/packet_loop.py`. Hai chỗ cưỡng chế CÙNG một luật
# ("không tự cấp lease") ở hai tầng khác nhau: một tầng cục bộ lúc chạy máy trạng
# thái, một tầng ở cửa đăng. Tầng nào thủng thì tầng kia còn đỡ.
#
# ĐÂY CHỈ LÀ DANH SÁCH CẤM, và một danh sách cấm KHÔNG BAO GIỜ ĐỦ. Giữ lại vì thông
# điệp của nó chỉ đúng tên bệnh ("agent tự ký cho mình"), nhưng thứ thật sự chặn là
# `NGUOI_CO_THAM_QUYEN` bên dưới.
PROVIDERS = ("claude", "codex")

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


class Chan(Exception):
    def __init__(self, ma: int, thong_diep: str):
        super().__init__(thong_diep)
        self.ma = ma
        self.thong_diep = thong_diep


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


def _quet_lease_toan_kho(goc: Path, *, doi_chieu_ref=True) -> list[dict]:
    """Đọc mỗi cặp (blob, đường dẫn) lease đúng một lần trên mọi ref cục bộ."""
    ten_cuc_bo, refs = _cac_ref_cuc_bo(goc)
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
                lease = yaml.safe_load(_git(goc, "cat-file", "-p", blob))
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
    so, lease_id = lease["packet_issue"], str(lease["lease_id"])
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


def _kiem_dau_toan_kho(lease: dict, tep=None, goc=None) -> None:
    if not tep:
        return
    root = _goc_kho(Path(tep), goc)
    if not (root / ".git").exists():
        return
    try:
        Path(tep).resolve().relative_to(root)
    except ValueError:
        return  # fixture/bản sao rời, không phải tệp lease trong kho đang quét
    try:
        p = GOI_GIT("rev-parse", "--git-dir", cwd=root)
    except OSError:
        return
    if p.returncode != 0:
        return
    lease_id = str(lease.get("lease_id") or "")
    for muc in _quet_lease_toan_kho(root, doi_chieu_ref=False):
        ban = muc["lease"]
        if str(ban.get("lease_id") or "") == lease_id and ban.get("posted_comment_id"):
            raise Chan(RC_DA_DANG,
                       f"lease {lease_id!r} đã đăng (comment {ban['posted_comment_id']}) "
                       f"trên {muc['ref']}:{muc['path']} — bỏ qua")


def kiem(lease: dict, tep=None, goc=None) -> tuple:
    """Kiểm thuần và trả `(lease, băm prompt)`; ném `Chan` nếu không hợp lệ.

    Trả kèm cái băm chứ không trả mỗi lease, để dòng "prompt … khớp băm" mà `check`
    in ra là BẰNG CHỨNG chứ không phải lời khen. Bản trước in dòng đó chỉ vì lease
    có trường `prompt_path` — nghĩa là gỡ hẳn chốt kiểm băm đi thì nó vẫn in y
    nguyên. Một dòng xác nhận không đi kèm việc kiểm là thứ tệ hơn im lặng.
    """
    # Idempotent trước tiên: workflow bị chạy lại (retry, re-run tay, push lại
    # cùng commit) KHÔNG được đăng trùng một lease.
    if lease.get("posted_comment_id"):
        raise Chan(RC_DA_DANG,
                   f"lease {lease.get('lease_id')!r} đã đăng "
                   f"(comment {lease['posted_comment_id']}) — bỏ qua")
    _kiem_dau_toan_kho(lease, tep, goc)
    thieu = [k for k in BAT_BUOC if lease.get(k) in (None, "")]
    if thieu:
        raise Chan(RC_NOI_DUNG, f"thiếu trường bắt buộc: {', '.join(thieu)}")

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

    lease_id = str(lease["lease_id"])
    if not LEASE_ID.fullmatch(lease_id):
        raise Chan(RC_NOI_DUNG, f"lease_id chỉ được chứa ASCII chữ/số/`.`/`_`/`-`; được {lease_id!r}")

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
    if han <= datetime.now(timezone.utc):
        raise Chan(RC_NOI_DUNG,
                   f"lease đã hết hạn lúc {han.isoformat()} — đăng một lease chết thì "
                   f"người nhận tưởng có quyền mà không có")
    return lease, neo


def kiem_github(lease: dict, tep=None, goc=None) -> tuple:
    lease, neo = kiem(lease, tep, goc)
    repo = _repo_github()
    _kiem_loai_so_hieu(repo, lease["packet_issue"])
    _kiem_comment_da_co(repo, lease)
    return lease, neo


def dung_than(lease: dict, duong_dan: str) -> str:
    """Thân comment: nói rõ đây là bản CHIẾU, nguồn sự thật nằm trong kho."""
    import yaml
    khoi = yaml.safe_dump(lease, allow_unicode=True, sort_keys=False).rstrip()
    return (
        f"**Lease `{lease['lease_id']}`** — đăng tự động từ `{duong_dan}`.\n\n"
        f"Nguồn sự thật là tệp trong kho, comment này chỉ là **bản chiếu**. Sửa lease "
        f"thì sửa tệp rồi push; đừng sửa tay comment này.\n\n"
        f"```yaml\n{khoi}\n```\n"
    )


def _ghi_comment_id(duong_dan: str, comment_id: int) -> None:
    """Nối một dòng vào cuối tệp — KHÔNG dump lại YAML.

    `yaml.safe_dump` sẽ sắp xếp lại khoá và **xoá sạch chú thích**, mà chú thích
    trong lease chính là chỗ ghi vì sao từng trường có giá trị đó. Nối một dòng
    giữ nguyên tệp người viết.
    """
    p = Path(duong_dan)
    noi_dung = p.read_text(encoding="utf-8")
    if not noi_dung.endswith("\n"):
        noi_dung += "\n"
    noi_dung += f"posted_comment_id: {int(comment_id)}   # workflow ghi, ĐỪNG sửa tay\n"
    p.write_text(noi_dung, encoding="utf-8")


def lenh_check(a) -> int:
    lease, neo = kiem(_doc_yaml(a.tep), a.tep, getattr(a, "goc", None))
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


def lenh_mark(a) -> int:
    _doc_yaml(a.tep)          # đọc để chắc tệp còn hợp lệ trước khi ghi thêm
    _ghi_comment_id(a.tep, a.comment_id)
    print(f"đã ghi posted_comment_id={a.comment_id} vào {a.tep}")
    return RC_OK


def lenh_ai_dang_giu(a) -> int:
    root = Path(a.goc or ".").resolve()
    cac_lease = _quet_lease_toan_kho(root)
    nguoi_giu = []
    for muc in cac_lease:
        lease = muc["lease"]
        if not _lease_cham_duong(lease, a.duong_dan):
            continue
        trang_thai = _phan_loai_lease(lease)
        da_chet = bool(lease.get("da_bi_thay_the")) and trang_thai == "CÒN_HẠN"
        lease_id = str(lease.get("lease_id") or "<thiếu lease_id>")
        nhan = " · ĐÃ_BỊ_THAY_THẾ" if da_chet else ""
        print(f"{trang_thai}{nhan}\t{lease_id}\t{muc['ref']}:{muc['path']}")
        if trang_thai == "CÒN_HẠN" and not da_chet:
            nguoi_giu.append(lease_id)
    print(f"NGƯỜI_GIỮ {len(nguoi_giu)}: " + (", ".join(sorted(nguoi_giu)) or "không có"))
    return RC_DANG_GIU if nguoi_giu else RC_OK


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
        q.set_defaults(fn=fn)
    q = sub.add_parser("mark", help="ghi posted_comment_id vào tệp sau khi đăng xong")
    q.add_argument("tep")
    q.add_argument("--comment-id", type=int, required=True)
    q.set_defaults(fn=lenh_mark)
    q = sub.add_parser("ai-dang-giu", help="quét toàn kho xem ai đang giữ một đường dẫn")
    q.add_argument("duong_dan")
    q.add_argument("--root", dest="goc", default=".")
    q.set_defaults(fn=lenh_ai_dang_giu)

    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except Chan as e:
        print(f"CHAN [{e.ma}]: {e.thong_diep}", file=sys.stderr)
        return e.ma


if __name__ == "__main__":
    sys.exit(main())
