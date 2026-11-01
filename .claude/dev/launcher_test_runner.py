#!/usr/bin/env python3
"""Runner tin cậy cho nhánh harness (b) của `chay_dot_bien` (#1117, spec `ops/specs/wp1117.md`).

Cách gọi: `python launcher_test_runner.py <tệp launcher_test.py> <tên ca>`. Stdin mang đúng hai dòng:
đường tệp kênh kết quả, rồi nonce.

VÌ SAO TỆP NÀY TÁCH RIÊNG. `chay_dot_bien` đột biến một BẢN SAO của `launcher_test.py`. Trước #1117, bản sao
ấy tự chạy ca và tự ghi kết quả, còn đường kênh và nonce được truyền qua env. Mã cấp module chạy TRƯỚC `main`,
nên đọc được env và ghi được một kết quả "giết" mà ca đích không hề chạy (Codex lượt 2 của #1079, F04).
Đó là lần thứ ba nhánh (b) bị phá theo cùng một hình dạng: bộ báo cáo tin một tín hiệu mà chính mã bị
đột biến tạo ra được. Nên lần này đổi kiến trúc: nonce và việc ghi kênh nằm ở tệp này, và
`DOT_BIEN_HARNESS` không bao giờ đột biến tệp này.

HỢP ĐỒNG — thứ tự là chốt, đừng đảo:
  (i)  đọc đường kênh và nonce từ stdin, rồi thay fd 0 bằng /dev/null, TRƯỚC khi nạp tệp test. Env và argv
       không mang dữ liệu kênh nào;
  (ii) nạp tệp test bằng `importlib` dưới tên khác `__main__`, không ghi bytecode;
  (iii) tra ĐÚNG MỘT ca có `__name__` bằng tên ca trong `CA`;
  (iv) chạy ca qua `cham_mot_ca` của CHÍNH module. Bộ chấm là đối tượng bị đo, nên tệp này không phân hạng
       thay nó;
  (v)  chỉ ghi kênh SAU khi `cham_mot_ca` đã trả về. Nạp lỗi hoặc `SystemExit` trước đó thì kết thúc mà
       KHÔNG ghi gì, và bên gọi đọc sự vắng mặt ấy thành `loi`.

GIỚI HẠN CÓ TÊN `RUNNER-CUNG-TIEN-TRINH` (chủ kho chấp nhận, không đóng được): mã đột biến chạy CHUNG tiến
trình với tệp này. Nó vẫn có thể CỐ Ý dò khung ngăn xếp, monkeypatch `json`/`os`/`builtins` hay chính runner,
đọc bộ nhớ tiến trình, hoặc ghi đè các tệp trên đĩa (kể cả bản runner trong cây của nó, mà các lượt chấm sau
trong cùng cây sẽ dùng). Chặn triệt để là không thể, vì tín hiệu `TinHieuChotCa` cũng sinh ra từ chính mã bị
đột biến. Tệp này chỉ chặn việc giả THỤ ĐỘNG: đọc dữ liệu kênh từ env/argv/stdin, hoặc ghi kênh trước khi ca chạy.
Bảng `DOT_BIEN_HARNESS` do kho tự viết, không phải đối thủ.
"""
import importlib.util
import json
import os
import sys

LOAI_HOP_LE = ("qua", "bo_qua", "giet", "loi")


def _doc_kenh_roi_bit_stdin():
    """(i): đọc hết stdin, rồi để fd 0 trỏ /dev/null. Mã cấp module đọc `sys.stdin` hay `os.read(0)` chỉ
    thấy EOF."""
    dong = sys.stdin.read().splitlines()
    rong = os.open(os.devnull, os.O_RDONLY)
    os.dup2(rong, 0)
    os.close(rong)
    sys.stdin = open(0, encoding="utf-8", closefd=False)
    if len(dong) != 2 or not all(dong):
        return None, None
    return dong[0], dong[1]


def main(argv) -> int:
    if len(argv) != 2:
        print("dung: launcher_test_runner.py <tep launcher_test.py> <ten ca>  (stdin: duong kenh, nonce)",
              file=sys.stderr)
        return 2
    tep, ten = argv
    kenh, nonce = _doc_kenh_roi_bit_stdin()
    if kenh is None:
        print("stdin phai co dung 2 dong: duong kenh, nonce", file=sys.stderr)
        return 2
    sys.dont_write_bytecode = True
    sys.argv = [tep]
    sys.path.insert(0, os.path.dirname(os.path.abspath(tep)))
    spec = importlib.util.spec_from_file_location("launcher_test_dot_bien", tep)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[spec.name] = mod
    spec.loader.exec_module(mod)   # (ii) SystemExit/lỗi ở đây ⇒ KHÔNG có kênh
    chon = [f for f in getattr(mod, "CA", []) if getattr(f, "__name__", None) == ten]
    if len(chon) != 1:
        loai, chi_tiet = "loi", f"{ten}(khop {len(chon)} ca)"
    else:
        loai, chi_tiet = mod.cham_mot_ca(chon[0])   # (iv)
    with open(kenh, "w", encoding="utf-8") as f:     # (v) chỉ sau khi ca đã chạy
        json.dump({"nonce": nonce, "ten": ten, "loai": loai, "chi_tiet": chi_tiet}, f)
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
