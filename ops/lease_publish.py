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
mang danh nghĩa kho chính là bộ kiểm trong tệp này. Nó xanh dễ dãi thì đường này
thành đường đăng bừa. Vì thế mọi lệnh ở đây — kể cả `body` — đều đi qua cùng một
hàm kiểm; hai đường mà chỉ một đường có chốt là chốt đi vòng được.

MÃ THOÁT
  0  qua
  2  tham số / không đọc được tệp
  4  `granted_by` là tên một PROVIDER — agent tự cấp lease cho mình
  6  mỏ neo prompt hỏng (thiếu `prompt_path`, tệp không có, hoặc băm lệch)
  8  nội dung lease sai (thiếu trường, sai dạng, hết hạn, YAML hỏng)
  9  lease ĐÃ đăng rồi (có `posted_comment_id`) — workflow phải BỎ QUA, không đăng lại
"""

from __future__ import annotations

import argparse
import hashlib
import re
import sys
from datetime import datetime, timezone
from pathlib import Path, PurePosixPath

RC_OK = 0
RC_THAM_SO = 2
RC_TU_CAP = 4
RC_NEO = 6
RC_NOI_DUNG = 8
RC_DA_DANG = 9

# Cùng danh sách với `.claude/dev/packet_loop.py`. Hai chỗ cưỡng chế CÙNG một luật
# ("không tự cấp lease") ở hai tầng khác nhau: một tầng cục bộ lúc chạy máy trạng
# thái, một tầng ở cửa đăng. Tầng nào thủng thì tầng kia còn đỡ.
PROVIDERS = ("claude", "codex")

BAT_BUOC = (
    "packet_issue",
    "lease_id",
    "granted_by",
    "lease_expires_at_utc",
    "reviewed_sha_required",
)

SHA40 = re.compile(r"^[0-9a-f]{40}$")
SHA256 = re.compile(r"^[0-9a-f]{64}$")


class Chan(Exception):
    def __init__(self, ma: int, thong_diep: str):
        super().__init__(thong_diep)
        self.ma = ma
        self.thong_diep = thong_diep


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


def kiem(lease: dict, tep=None, goc=None) -> tuple:
    """Trả `(lease, băm prompt ĐÃ XÁC MINH)` nếu ĐĂNG ĐƯỢC; ném `Chan` nếu không.

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

    so = lease["packet_issue"]
    # `bool` là con của `int` trong Python: `True` sẽ lọt nếu chỉ kiểm isinstance.
    if isinstance(so, bool) or not isinstance(so, int) or so <= 0:
        raise Chan(RC_NOI_DUNG, f"packet_issue phải là số nguyên dương, được {so!r}")

    sha = str(lease["reviewed_sha_required"]).strip()
    if not SHA40.match(sha):
        # SHA ngắn hoặc lệch dạng là mỏ neo GIẢ: reviewer sẽ đọc một head khác với
        # head mà lease tưởng đang nói tới, và không ai phát hiện ra.
        raise Chan(RC_NOI_DUNG,
                   f"reviewed_sha_required phải là 40 ký tự hex thường, được {sha!r}")

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
    print(f"lease {lease['lease_id']} ĐĂNG ĐƯỢC — issue #{lease['packet_issue']}, "
          f"neo {lease['reviewed_sha_required'][:12]}, hết hạn {lease['lease_expires_at_utc']}"
          + (f", prompt {lease['prompt_path']} khớp băm {neo[:12]}" if neo else ""))
    return RC_OK


def lenh_body(a) -> int:
    # Đi qua ĐÚNG hàm kiểm của `check`. Nếu `body` có đường riêng, ai đó chỉ cần
    # gọi thẳng `body` là vòng qua được toàn bộ chốt.
    lease, _ = kiem(_doc_yaml(a.tep), a.tep, getattr(a, "goc", None))
    sys.stdout.write(dung_than(lease, a.tep))
    return RC_OK


def lenh_mark(a) -> int:
    _doc_yaml(a.tep)          # đọc để chắc tệp còn hợp lệ trước khi ghi thêm
    _ghi_comment_id(a.tep, a.comment_id)
    print(f"đã ghi posted_comment_id={a.comment_id} vào {a.tep}")
    return RC_OK


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

    a = ap.parse_args(argv)
    try:
        return a.fn(a)
    except Chan as e:
        print(f"CHAN [{e.ma}]: {e.thong_diep}", file=sys.stderr)
        return e.ma


if __name__ == "__main__":
    sys.exit(main())
