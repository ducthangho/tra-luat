# Bằng chứng soạn đặc tả GWS-CRED-DICH-NGOAI-KHO-N r1 (#433, bốn nợ)

Đo trên `master` `8a72d28d7a413047733277545fc8547f32010593` (tree `df0bbe85dc230c595d44c197eae694fe41feecf8`), 2026-11-20.
Đây là PHÉP ĐO lúc soạn, không phải nghiệm thu.

| tệp | nội dung |
|---|---|
| `probe433n.py` | Chạy fragment packet 1 ba biến thể trên bản sao tạm: `goc` (nguyên văn), `log` (in đường `os.replace` nhận ở N8.4-W2/W6), `chuan` (chỉ hai phép so đổi thành so sau `normcase(normpath)`). |
| `do433n.py` | Driver Desktop: khoá `KHOA.txt`, clone sạch `8a72d28`, kiểm tree và sha256 probe, chạy ba biến thể. |
| `desktop-wp433n-out-20261120T012952Z/` | Đầu ra thô từ `DESKTOP-T9R33P2` (Windows 11 10.0.26300, Python 3.12.10). Zip chuyển về có sha256 `d9602167…53c0d`. `log.stderr.txt` gốc 56 dòng (sha256 `e1a0dc01…`) — chỉ chép 40 dòng đầu. |
| `probe-linux.txt` | Cùng probe trên Linux: `goc`, `chuan` đều True. |
| `tai_hien.py` · `tai-hien-linux.txt` | Tái hiện nợ (2) W6 ghi xuyên symlink HOME/tổ tiên HOME (W4 cùng đường thì từ chối), (3) bundle không phải dict ⇒ `AttributeError` ở `bootstrap` và `nlm-auth-pull`, (4) `_trong_kho_git` đọc `PermissionError` thành "không có `.git`". |

Kết luận nợ (1): Desktop `goc` ⇒ False đúng hai lượt `N8.4-W2`/`N8.4-W6`; `chuan` ⇒ True, `CA 18/18`, `DOT BIEN 30/30`. Nguyên nhân ở
TEST: `ntpath.expanduser("~/.x")` giữ dấu `/`, phép so chuỗi của fragment không bao giờ khớp đích mà mã thật ghi.

Chưa đo: lượt EACCES thật cho nợ (4) (container chạy root; lệnh `setpriv` bị từ chối trong phiên soạn).
