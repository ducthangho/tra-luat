# Cross-review lượt 1 của revision 2 — packet `NO-CAU-LICH-SU-BIEN-NHAN` (Issue ducthangho/tra-luat#960) — reviewer: codex

## Đối tượng
- `reviewed_sha`: `f7659a2f911e4a686d2b312ce046f3625a563b93` (nhánh `agent/wp960-g1-claude`, CHƯA merge), một commit trên base
  `44884446f71c89e25f9a72ac58e4f597db63c1ba` (= `origin/master` lúc cấp lease r2).
- Diff so base: `diff.patch`, `numstat.txt` — đúng hai tệp `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`.
- Đặc tả ĐÓNG BĂNG (nguồn DUY NHẤT của phạm vi): `cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`, sha256 phải là
  `9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca` (tự kiểm). M1–M6, nghiệm thu B1–B8, `ngoai_pham_vi`,
  `hinh_dang_ke_thua`, `chua_do_duoc`. Lease r2: `lease-r2.yaml` (bản chép từ nhánh `ops/wp960-r2-g1-lease`).
- Review class hiệu lực: `sensitive`. Executor: Claude (khác họ với bạn).
- Lịch sử: revision 1 (PR #976, đã merge) có hai lượt codex `changes_requested`; verdict ở `verdict-cu/`. Lượt 2 của r1 còn 7 finding;
  r2 được thiết kế để đóng các LỚP của chúng theo kiến trúc (spec mục "Vấn đề").

## Lời khai của executor (tự kiểm, ĐỪNG tin)
1. `python3 ops/bien_nhan_v2.py --root .` ⇒ rc=0, `TỔNG: ĐẠT`, `câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0`.
2. `python3 ops/bien_nhan_v2_test.py` ⇒ `87/87 ca · 99/99 đột biến thường CÓ RĂNG · 2/2 TỰ KIỂM` (~6 phút).
3. M1: không còn phép đọc mốc hay truy lịch sử tệp; `rg -n '"dung_tai"|def _moc_|def _commit_them_cau|def _co_cau' ops/bien_nhan_v2.py` ⇒ 0.
4. M2: per-receipt `try/except Exception` trong `_kiem_cau_lich_su` ⇒ chua khoá `(tên, "*", "*")`; `kiem` bỏ qua kết luận nợ chết
   cho tệp có khoá ấy; băm + đọc receipt trong `try` riêng ⇒ `KhongDoDuoc`. `KhongDoDuoc` (alias vòng) vẫn được ném lại.
5. M3: `_oid_bat_buoc` — 40 hex · trộn · backtick hai đầu · ngay sau từ `commit` (regex `\bcommit\s*\Z` trên phần trước token).
6. M4: cửa sổ {j-1, j, j+1} phải có `\bprovider\b` và KHÔNG có `[\w./-]+\.[A-Za-z0-9]+:\d+`. Hệ quả có chủ đích: trích dẫn đứng SAU
   khai báo trong cửa sổ cũng loại dòng ấy (`c79` ca `trich-dan-sau` đổi kỳ vọng 1 → 0).
7. M5: nợ sinh lại 61 mục; 3 nợ L-SURFACE cũ thành nợ chết và bị gỡ.
8. Đột biến cũ bị gỡ theo M1: m77, m86, m87, m90, m93 (đích là mốc). `m83`/`m84`/`m76`/`m92` neo lại theo thụt lề mới.

## Nhiệm vụ: ĐO LẠI TỪNG KHẲNG ĐỊNH tại `f7659a2f911e4a686d2b312ce046f3625a563b93`
Danh sách dưới KHÔNG đủ — mỗi lỗi thật bạn tìm ra ngoài danh sách được tính là finding.

(a) **Đúng đặc tả r2.** Đối chiếu từng M1–M6 và B1–B8 với mã + ca test; ca không đo đúng điều B# đòi là finding.
(b) **Ba trạng thái / biên lỗi đo.** Còn đường nào một lỗi ĐO (git, I/O, YAML, JSON, mã hoá, nhánh mặc định) thành rc=0 hoặc rc=1,
    hoặc traceback? Biên M2 có nuốt mất một lỗi LẬP TRÌNH thật (che bug thành rc=2) không — đo bằng phản chứng.
(c) **Ứng viên.** Bộ chọn OID theo ngữ cảnh (M3) và lời tự khai (M4): bỏ sót / bắt nhầm trên dữ liệu thật của kho (mọi
    `ops/reviews/*.receipt.yaml` và verdict có `run_json`). Đo, đừng đoán.
(d) **Nợ.** `NO_CAU_LICH_SU` có khớp đúng vi phạm thật trên base? Ổn định trong CI `pull_request` (merge commit, `fetch-depth: 0`,
    không `origin/HEAD`)?
(e) **Không phá gì.** Suite N/N hai số BẰNG NHAU; mọi đột biến cũ còn răng; `ruff check --select F` delta 0 so base (nếu có ruff);
    `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check base HEAD`.
(f) **Đột biến của bạn.** Trên BẢN SAO: gỡ từng chốt mới (≥ 5 chốt khác m94–m102/m85) và ghi ca nào ĐỎ; chốt không ca nào đỏ = finding.
(g) **Hình dạng kế thừa.** Spec r2 mục `hinh_dang_ke_thua`: ba hình dạng (lỗi đo thành sạch/vi phạm · bộ chọn ứng viên bỏ sót/bắt
    nhầm · nguồn gốc câu cho mốc). Với MỖI finding bạn ghi, gắn nhãn nó thuộc hình dạng nào trong ba hay KHÁC — bắt buộc.

## Ghi VERDICT.md TĂNG DẦN
Tạo `VERDICT.md` ở thư mục này (chứa PROMPT.md, KHÔNG trong `cay-kho/`) NGAY khi bắt đầu (dòng đầu `verdict: dang_lam`), nối thêm
sau MỖI hướng thử. Cuối cùng dòng đầu `verdict: approve` hoặc `verdict: changes_requested`, dòng 2
`reviewed_sha: f7659a2f911e4a686d2b312ce046f3625a563b93`, dòng 3 `Kết quả: <n> P0, <n> P1, <n> P2, <n> P3.`

Cấu trúc:
```
verdict: ...
reviewed_sha: ...
Kết quả: ...

## BẢNG ĐO
| khẳng định | bên giao khai | đo được (lệnh) | khớp? |

## BẢNG SĂN   (>= 6 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT)
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

### <slug-kebab>  [P0|P1|P2|P3]  <tiêu đề>
HÌNH DẠNG: <loi-do | bo-chon-ung-vien | nguon-goc-cau | khac>
TỆP/DÒNG:
VẤN ĐỀ:
ĐÃ THỬ NGHIỆM: <lệnh + kết quả, hoặc KHÔNG ĐO ĐƯỢC + lý do>
ĐỘ TIN: cao/vừa/thấp
```
P1 = hành vi sai đo được (kết quả sai, trạng thái sai, chốt không răng, lệch đặc tả). P2 = khai rộng hơn phép đo / thiếu điều kiện /
ca test không đo đúng điều nó khai. P3 = diễn đạt.
Không có finding thì vẫn phải có BẢNG ĐO đủ và BẢNG SĂN >= 6 hướng có output thật; "approve" không có output là không hợp lệ.
Trong VERDICT.md, nếu tự khai môi trường chạy của mình thì chỉ ghi điều bạn ĐO được; đừng tự đặt tên execution surface.
Gợi ý vá (nếu có) ghi vào `HINT.patch` ở thư mục này, định dạng `patch -p0` từ gốc `cay-kho/`, và PHẢI kiểm `patch --dry-run --fuzz=0`
sạch trên bản sao tại `f7659a2`.

## Ràng buộc
Bạn là reviewer CHỈ ĐỌC + ĐO, độc lập với executor. KHÔNG sửa `cay-kho/` (mọi đột biến làm trên BẢN SAO ở thư mục tạm), KHÔNG push,
KHÔNG gọi mạng. Chỉ CHẠY ca test có sẵn và ĐỘT BIẾN mã/fixture trên bản sao.
Mọi khẳng định phải đo TẠI `f7659a2f911e4a686d2b312ce046f3625a563b93`. Thứ định danh tệp là SHA, không phải tên nhánh.
Cây đầy đủ, KHÔNG shallow, tại `cay-kho/` (HEAD detached đúng `f7659a2…`; mọi nhánh ở `refs/remotes/origin/*`; `core.abbrev=7`).
Mirror trần: `mirror.git`.
Lưu ý môi trường: nếu ca nào báo `Codex home is inside a repository` thì đó là tạo tác của sandbox (`/tmp/.git`), ghi là KHÔNG ĐO
ĐƯỢC chứ đừng ghi thành finding.
