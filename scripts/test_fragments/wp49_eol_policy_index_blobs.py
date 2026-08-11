# -*- coding: utf-8 -*-
"""F2-A (ADR-0018) — regression EOL canonical chạy TRONG canonical selftest.

PHÂN CÔNG CÓ CHỦ ĐÍCH giữa hai suite, không phải trùng lặp lười:

- Fragment NÀY chạy trong `tl --selftest` ở CẢ cây dev lẫn gói đã giải nén. Writer canonical,
  `.gitattributes` và các bảng extension runtime đều có trong cả hai topology; `.editorconfig`
  là config dev-side nên CỐ Ý bị release loại. Fragment phân biệt topology bằng chính source
  fragment/bundled adapter, vì vậy bundle không biến thành ca rỗng chỉ vì thiếu config dev-side.
- Nó KHÔNG import `.githooks/eol_policy.py` — `.githooks/` bị `_RELEASE_EXCLUDE_DIRS` loại khỏi
  gói. `.githooks/eol_policy_test.py` dựng bundle thật, giải nén và chạy chính case `wp49` từ
  generated adapter để khoá đường package này.
- `.githooks/eol_policy_test.py` giữ phần hành vi validator ở tầng git (rename/copy, tên Unicode,
  binary, tệp mới). Nó cần một kho git thật nên không package-safe; CI gọi nó CHẶN trên cả
  ubuntu lẫn windows.

Vì sao cần ca trong canonical selftest: `.gitattributes` một mình KHÔNG chặn được artifact phái
sinh. Tệp phái sinh được GHI RA trước, git chỉ nhìn thấy nó sau. Nếu writer nhả CRLF thì mỗi lần
tái sinh golden/manifest lại đẻ một đợt renormalize, và F2 sẽ tự mở lại chính lớp hỏng nó vừa đóng.
"""
from __future__ import annotations

import re
import tempfile
from pathlib import Path

TEST_ID = "wp49_eol_policy_index_blobs"

# Sàn chống RỖNG. Không phải bản sao của danh sách: nếu một nguồn hợp đồng bị đổi tên hay import
# hỏng, tập suy ra co lại và phép `⊆` sẽ ĐÚNG một cách vô nghĩa. Sàn này biến "vô tình rỗng" thành
# ĐỎ. Đo 07-08-2026: hợp nhất ba nguồn cho 12 họ.
_SAN_TOI_THIEU = 10


def _root(tl_module):
    """Gốc kho/gói: `tl.py` luôn nằm ở `<root>/scripts/`, đúng ở cả cây dev lẫn bản giải nén."""
    return Path(tl_module.__file__).resolve().parent.parent


def _topology(tl_module):
    """Nhận diện tường minh dev/bundle; trạng thái lai hoặc thiếu adapter phải fail closed."""
    root = _root(tl_module)
    source = root / "scripts" / "test_fragments" / "wp49_eol_policy_index_blobs.py"
    bundled = root / "scripts" / "tl_test_fragments_bundled.py"
    editorconfig = root / ".editorconfig"
    if source.is_file() and bundled.is_file() and editorconfig.is_file():
        return "dev"
    if not source.exists() and bundled.is_file() and not editorconfig.exists():
        return "bundle"
    return None


def _writer_canonical(tl_module):
    """Writer phải nhả LF dù đầu vào là CRLF, CR đơn lẻ hay trộn lẫn.

    `newline="\\n"` một mình KHÔNG đủ: nó tắt phép dịch `\\n`→`\\r\\n` lúc ghi nhưng không đụng
    `\\r` đã nằm sẵn trong chuỗi. Đọc một tệp CRLF rồi ghi lại qua writer "đã ghim LF" vẫn ra CRLF.
    """
    write = getattr(tl_module, "_write_text_atomic", None)
    if not callable(write):
        return False
    mau = [
        "a\r\nb\r\n",          # CRLF toàn phần
        "a\r\nb\nc\r\n",       # trộn
        "a\rb\r",              # CR đơn lẻ (Mac cổ / stdout lạ)
        "a\nb\n",              # vốn đã LF: phải giữ nguyên, không nhân đôi
    ]
    with tempfile.TemporaryDirectory(prefix="wp49_writer_") as tmp:
        for i, text in enumerate(mau):
            # Ghi vào thư mục con CHƯA tồn tại: khoá luôn hợp đồng mkdir của writer.
            dest = Path(tmp) / ("sub%d" % i) / "out.txt"
            write(dest, text)
            raw = dest.read_bytes()
            if b"\r" in raw:
                return False
            if raw.decode("utf-8") != text.replace("\r\n", "\n").replace("\r", "\n"):
                return False
    return True


def _writer_van_nguyen_tu(tl_module):
    """Chuẩn hoá không được làm mất ngữ nghĩa nguyên tử: ghi đè xong không để lại tmp lảng vảng."""
    write = tl_module._write_text_atomic
    with tempfile.TemporaryDirectory(prefix="wp49_atomic_") as tmp:
        dest = Path(tmp) / "out.txt"
        write(dest, "cu\r\n")
        write(dest, "moi\r\n")
        if dest.read_bytes() != b"moi\n":
            return False
        # `mkstemp` cùng thư mục + `os.replace` ⇒ sau khi xong chỉ còn ĐÚNG tệp đích.
        return sorted(p.name for p in Path(tmp).iterdir()) == ["out.txt"]


def _ho_binary_suy_ra(tl_module):
    """SUY RA họ binary từ bảng extension ingest/loader của kho, KHÔNG chép tay.

    Một danh sách chép tay có khuyết điểm đi thẳng vào cả policy lẫn test, rồi hai bên gật đầu
    với nhau — đúng cái bẫy đã để lọt `.xls/.odt/.tif/.tiff` ở vòng trước. Neo vào hợp đồng thật:

      PROFILE_INGEST_ALLOWED_EXTS  tl.py                     allowlist của `profile-ingest`
      INGEST_LOCAL_EXTS            tl_core/ingest_contract   allowlist của `ingest-local`
      OCR_SOURCE_EXTS              tl_core/ingest_contract   nguồn đi đường OCR (ảnh + PDF)
      _MIME_BY_EXT                 tl.py                     để loại `text/*` khỏi hợp nhất

    Mở thêm một đuôi ở bất kỳ allowlist nào mà quên khai `-text` ⇒ ca này ĐỎ.
    """
    from tl_core.ingest_contract import INGEST_LOCAL_EXTS, OCR_SOURCE_EXTS
    nguon = [set(tl_module.PROFILE_INGEST_ALLOWED_EXTS), set(INGEST_LOCAL_EXTS), set(OCR_SOURCE_EXTS)]
    if not all(nguon):                      # nguồn rỗng ⇒ phép ⊆ sẽ đúng vô nghĩa
        return None
    mime = getattr(tl_module, "_MIME_BY_EXT", None)
    if not mime:
        return None
    hop = set().union(*nguon)
    return {e for e in hop if not str(mime.get(e, "")).startswith("text/")}


def _policy_khai_du(tl_module):
    """`.gitattributes` phải khai ĐỦ policy ADR-0018 và ĐỦ mọi họ binary suy ra được."""
    path = _root(tl_module) / ".gitattributes"
    if not path.is_file():
        return False
    noi_dung = path.read_text(encoding="utf-8")
    dong = [d.strip() for d in noi_dung.splitlines()]
    dong = [d for d in dong if d and not d.startswith("#")]
    can = [
        "* text=auto eol=lf",
        "*.cmd text eol=crlf",
        "*.bat text eol=crlf",
        "references/golden/** -text",
    ]
    if any(c not in dong for c in can):
        return False
    # `* -text` cũ phải BIẾN MẤT: còn nó thì policy mới vô hiệu ngay từ dòng đầu.
    if "* -text" in dong:
        return False

    suy_ra = _ho_binary_suy_ra(tl_module)
    if not suy_ra or len(suy_ra) < _SAN_TOI_THIEU:
        return False
    khai = {m.group(1) for m in re.finditer(r"(?m)^\*(\.[A-Za-z0-9]+) -text\s*$", noi_dung)}
    return suy_ra <= khai


def _editorconfig_dong_bo(tl_module):
    """Ở topology dev, `.editorconfig` phải phủ những họ mà `.gitattributes` khai `-text`.

    Hai tệp cưỡng chế cùng một policy ở hai tầng khác nhau (git vs editor). Chúng SẼ trôi lệch,
    và bên quên cập nhật chính là bên để editor ghi lại CRLF vào một tệp đáng ra bất khả xâm phạm.
    Gói release không ship config editor; `_topology()` xác nhận sự vắng mặt đó là cấu trúc bundle
    thật, không phải một tệp dev vô tình mất rồi bị bỏ qua.
    """
    root = _root(tl_module)
    ec = root / ".editorconfig"
    if not ec.is_file():
        return False
    suy_ra = _ho_binary_suy_ra(tl_module)
    if not suy_ra or len(suy_ra) < _SAN_TOI_THIEU:
        return False
    phu = set()
    for m in re.finditer(r"(?m)^\[\*\.\{([^}]*)\}\]\s*$", ec.read_text(encoding="utf-8")):
        phu |= {"." + x.strip() for x in m.group(1).split(",") if x.strip()}
    return suy_ra <= phu


def run(tl_module):
    topology = _topology(tl_module)
    return bool(
        topology
        and _writer_canonical(tl_module)
        and _writer_van_nguyen_tu(tl_module)
        and _policy_khai_du(tl_module)
        and (topology == "bundle" or _editorconfig_dong_bo(tl_module))
    )
