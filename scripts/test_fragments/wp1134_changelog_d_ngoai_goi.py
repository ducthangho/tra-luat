# -*- coding: utf-8 -*-
"""wp1134 — thư mục `changelog.d` KHÔNG vào gói phát hành; tên tệp chứa chuỗi ấy thì vẫn vào.

Gọi hàm sản xuất `_release_should_include` (module thật `tl_core.release`, lấy qua `tl_module._tl_release` vì `tl` chỉ phơi
stub). Hàm ấy kết thúc bằng `path.is_file()`, nên mọi ca dựng TỆP THẬT trong thư mục tạm rồi hỏi:
  (a) `changelog.d/wp-1.md`                ⇒ KHÔNG vào gói;
  (b) `docs-like/changelog.d/x.md`         ⇒ KHÔNG vào gói (luật theo TỪNG thành phần đường dẫn, kể cả thư mục lồng);
  (c) `references/changelog.d.md`          ⇒ VÀO gói (tên tệp, không phải thư mục);
  (d) `references/x.md` (đối chứng)        ⇒ VÀO gói.
Không có nhánh bỏ qua: `scripts/tl_core/release.py` là required release file, có mặt cả trong gói đã giải nén. Mọi lỗi dựng
fixture hoặc gọi hàm ⇒ FAIL có thông báo, không bao giờ trả True.
"""

from pathlib import Path
import sys
import tempfile


TEST_ID = "wp1134_changelog_d_ngoai_goi"

_CA = {
    "a": ("changelog.d/wp-1.md", False),
    "b": ("docs-like/changelog.d/x.md", False),
    "c": ("references/changelog.d.md", True),
    "d": ("references/x.md", True),
}


def _bao(msg):
    print("[%s] FAIL %s" % (TEST_ID, msg), file=sys.stderr)


def run(tl_module):
    try:
        rel_mod = tl_module._tl_release
        with tempfile.TemporaryDirectory() as td:
            goc = Path(td) / "kho"
            for rel, _ in _CA.values():
                p = goc / rel
                p.parent.mkdir(parents=True, exist_ok=True)
                p.write_text("x\n", encoding="utf-8", newline="\n")
            vang = sorted(rel for rel, _ in _CA.values() if not (goc / rel).is_file())
            if vang:
                _bao("tiền điều kiện: không dựng được tệp fixture %s" % vang)
                return False
            thuc = {ca: rel_mod._release_should_include(goc / rel, goc) for ca, (rel, _) in _CA.items()}
    except Exception as exc:                            # fixture/hàm hỏng ⇒ ĐỎ có chẩn đoán
        _bao("không dựng/đo được fixture: %s: %s" % (type(exc).__name__, exc))
        return False
    lech = sorted(ca for ca, (_, mong) in _CA.items() if thuc[ca] is not mong)
    if lech:
        _bao("ca lệch %s; thực %s" % (lech, {ca: thuc[ca] for ca in lech}))
        return False
    return True
