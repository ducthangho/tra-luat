#!/usr/bin/env python3
"""Quét BÍ MẬT trong cây gói sắp deploy — NGUỒN SỰ THẬT DUY NHẤT cho cả hai đường deploy.

Vì sao tách thành tệp riêng (v1.35.81): `deploy-package.sh` và `deploy-package.ps1` đều phải quét
trước khi đẩy. Nhét inline vào mỗi script = HAI bảng mẫu bí mật, và chúng SẼ trôi lệch nhau — thêm
mẫu ở bản sh mà quên bản ps1 thì đường Windows đẩy lọt secret mà không ai biết. Mẫu bí mật là thứ
tuyệt đối không được có hai bản.

Dùng: python pkg_secret_scan.py <thư-mục-gói-đã-giải-nén>
rc 0 = sạch · rc 1 = BẮT ĐƯỢC bí mật (in <đường-dẫn>:<dòng>: <tên-mẫu>) · rc 2 = sai cách gọi
"""
import pathlib
import re
import sys

# Mẫu bí mật THẬT, cố ý KHÔNG bắt placeholder/ví dụ (vd "YOUR_TOKEN_HERE", "AKfycb<...>") — chặn oan
# thì người ta sẽ tắt bộ quét, tệ hơn là không quét.
PATTERNS = [
    ("google_oauth_client_secret", re.compile(r"GOCSPX-[A-Za-z0-9_\-]{20,}")),
    ("google_api_key",             re.compile(r"AIza[0-9A-Za-z_\-]{35}")),
    ("gas_exec_token",             re.compile(r"AKfycb[0-9A-Za-z_\-]{50,}")),
    ("private_key_block",          re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
    ("bearer_jwt",                 re.compile(r"eyJ[A-Za-z0-9_\-]{10,}\.eyJ[A-Za-z0-9_\-]{10,}\.")),
    ("google_oauth_refresh",       re.compile(r"1//0[A-Za-z0-9_\-]{30,}")),
]

TEXT_SUFFIXES = {".py", ".md", ".json", ".gs", ".txt", ".yaml", ".yml", ".sh", ".ps1", ".cmd",
                 ".js", ".html", ".cfg", ".ini", ".toml", ".env", ".netrc", ".conf", ".properties"}

# Tệp KHÔNG có phần mở rộng cũng phải quét — `.env` `.netrc` `credentials` `Makefile` `LICENSE`:
# pathlib cho `Path('.env').suffix == ''` nên lọc theo suffix ĐƠN THUẦN sẽ MÙ đúng chỗ secrets hay nằm.
# Đã sập bẫy này: bơm GOCSPX-… vào `.env` mà bộ quét trả rc=0. Bù lại phải tự tránh tệp nhị phân:
MAX_BYTES = 2 * 1024 * 1024   # secrets không nằm trong tệp khổng lồ; tránh đọc cả gói nhị phân


def _is_scannable(f: pathlib.Path) -> bool:
    if f.suffix.lower() in TEXT_SUFFIXES:
        return True
    # wp1030 (bơm GOCSPX-… vào a.log/b.patch/c.csv: bản cũ chỉ báo d.txt) — fix: đuôi LẠ đi cùng nhánh với
    # tệp không đuôi. Mặc định là QUÉT; chỉ bỏ theo thuộc tính ĐO được (quá trần, có NUL ⇒ nhị phân), không
    # bỏ theo tên đuôi — danh sách đuôi không bao giờ đủ, lần trước mù `.env`, lần này mù `.log` `.patch`.
    try:
        if f.stat().st_size > MAX_BYTES:
            return False
        with f.open("rb") as fh:
            return b"\x00" not in fh.read(8192)   # có NUL ⇒ coi là nhị phân
    except OSError:
        return False

# Tệp mang CHÍNH bảng mẫu này thì đương nhiên chứa chuỗi giống mẫu — bỏ qua theo TÊN, không theo
# đường dẫn tuyệt đối (gói giải nén ra thư mục tạm khác nhau mỗi lần).
SELF_SKIP = {"pkg_secret_scan.py"}


def scan(root: pathlib.Path):
    hits = []
    for f in sorted(root.rglob("*")):
        if not f.is_file() or not _is_scannable(f):
            continue
        if f.name in SELF_SKIP:
            continue
        try:
            s = f.read_text(encoding="utf-8", errors="ignore")
        except OSError:
            continue
        for name, rx in PATTERNS:
            for m in rx.finditer(s):
                line = s[:m.start()].count("\n") + 1
                hits.append(f"{f.relative_to(root)}:{line}: {name}")
    return hits


def main(argv):
    if len(argv) != 2:
        print(f"dùng: {argv[0]} <thư-mục-gói>", file=sys.stderr)
        return 2
    root = pathlib.Path(argv[1])
    if not root.is_dir():
        print(f"không phải thư mục: {root}", file=sys.stderr)
        return 2
    hits = scan(root)
    for h in hits[:40]:
        print(h)
    if len(hits) > 40:
        print(f"... và {len(hits) - 40} phát hiện nữa")
    return 1 if hits else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
