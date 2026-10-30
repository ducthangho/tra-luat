# Đặc tả packet `PKG-SECRET-SCAN-DUOI-LA` r1: bộ quét bí mật trước đóng gói không được bỏ qua tệp có đuôi lạ

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

| trường | giá trị |
|---|---|
| packet | `PKG-SECRET-SCAN-DUOI-LA` (mission #748), revision 1, generation 1 |
| review_class | `sensitive` (cổng an ninh trên đường deploy Package) |
| write set | `scripts/pkg_secret_scan.py`, `scripts/test_fragments/pkg_secret_scan_duoi_la.py` (planned) |
| base | `origin/master` lúc cấp lease (đo khi soạn: `5f3855e`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, neo đúng head |
| depends_on | không |

## 1. Vì sao
Phát hiện ngày 29-10-2026: executor của packet `WINDOWS-LOCAL-MAY-CHU-KHO` r1 (`session_015GtxrbUPS7zGdffB8Sfo8Y`) báo lỗi, phiên điều phối xác nhận bằng cách đọc mã trên `5f3855e`.

`scripts/pkg_secret_scan.py`, hàm `_is_scannable` (dòng 36–47), xử lý ba nhóm tệp:
- tệp có đuôi thuộc `TEXT_SUFFIXES` được quét;
- tệp không có đuôi được kiểm NUL ở 8 KB đầu, thêm trần `MAX_BYTES` (2 MB), rồi mới quét;
- tệp có đuôi **khác** (`.log`, `.out`, `.patch`, `.diff`, `.csv`, `.tsv`, `.xml`, `.bak`, `.orig`, …) bị `return False` và **bỏ qua hoàn toàn**.

Bộ quét này dùng chung cho `scripts/deploy-package.sh` (dòng 237) và `scripts/deploy-package.ps1` (dòng 303), nên lỗ có trên cả hai nền. Một khoá nằm trong tệp `.log` trong Package sẽ không bị bắt. Đây là đúng họ lỗi mà CLAUDE.md đã ghi cho tệp không đuôi ("lọc theo PHẦN MỞ RỘNG là mù ĐÚNG CHỖ secrets nằm"), lần này xảy ra ở nhánh đuôi lạ.

Giới hạn của phép đo: chưa có phản chứng chạy được. Lệnh dựng một khoá giả trong tệp `.log` để chạy bộ quét đã bị bộ lọc quyền của phiên điều phối chặn. Phản chứng là việc đầu tiên của executor (§3).

## 2. Thay đổi
1. **`scripts/pkg_secret_scan.py`:**
   - Mọi tệp **không** thuộc `TEXT_SUFFIXES`, có đuôi hay không, đều đi qua **cùng** phép lọc hiện dùng cho tệp không đuôi: trần `MAX_BYTES` cộng kiểm NUL ở 8 KB đầu.
   - Chỉ bỏ qua tệp là nhị phân (có NUL) hoặc vượt trần.
   - Giữ nguyên `PATTERNS`, `TEXT_SUFFIXES`, cơ chế bỏ qua tệp mang bảng mẫu theo tên, mã thoát và định dạng output.
   - Tệp bị bỏ vì vượt trần hay vì là nhị phân phải được **đếm và in** trong output, theo cùng kiểu dòng tổng kết hiện có. Không được im lặng.
2. **`scripts/test_fragments/pkg_secret_scan_duoi_la.py` (mới):** một fragment selftest theo khuôn các fragment hiện có (vd `wp727_tl_gws_refresh.py`), có các ca `r<nnn>_…`:
   - **phản chứng trên base (A1):** chuỗi khớp mẫu đặt trong tệp `.log`, `.patch`, `.csv` ⇒ bản base cho rc=0, bản vá cho rc khác 0. Ca này phải ĐỎ trên base;
   - tệp đuôi lạ chứa NUL trong 8 KB đầu ⇒ không báo hit, và được đếm là bỏ vì nhị phân;
   - tệp đuôi lạ lớn hơn `MAX_BYTES` ⇒ không đọc, được đếm là bỏ vì vượt trần;
   - đối chứng: tệp `.txt` và tệp không đuôi vẫn bắt được như trước;
   - tệp mang bảng mẫu vẫn được bỏ qua theo tên.

   Chuỗi giống mẫu trong test phải được **dựng lúc chạy** (ghép chuỗi), không viết nguyên văn trong mã nguồn. Lý do: không để chính fragment làm bộ quét của kho đỏ.

## 3. Tiêu chí xong
- **Phản chứng ở A1** chạy được, ĐỎ trên base và XANH trên head.
- **Đột biến** khôi phục `return False` cho tệp đuôi lạ phải làm ca A1 ĐỎ. Đột biến bỏ bước đếm tệp bị bỏ qua phải làm ca đếm ĐỎ.
- **`python scripts/tl.py --selftest`** cho N/N. Có thêm ca mới, không ca cũ nào đỏ.
- **Ruff F** trên `scripts/pkg_secret_scan.py` và fragment mới: delta so master = 0.
- **Quét cây thật:** chạy `scripts/pkg_secret_scan.py` trên thư mục gói do `deploy-package.sh` dựng ở chế độ không push. Nếu có không thể dựng gói thì chạy trên một bản sao các tệp được đóng gói. So số hit với base:
  - hit mới là **phát hiện thật**, phải báo chủ kho và **không tự xoá dữ liệu**;
  - delta hit bằng 0 thì ghi rõ là 0.
- **Parity hai nền:** nếu một máy Windows thuộc phạm vi ADR-0057/0058 đang Online, chạy bộ quét trên cùng một thư mục đầu vào ở cả Linux lẫn Windows; số tệp đã quét, số bỏ và số hit phải khớp. Máy offline thì ghi "không đo local".
- **Review chéo** Codex qua `launcher.py run` trên đúng head, tới khi 0 P0–P3.
- **Không** bump VERSION, không sửa CHANGELOG, không sửa `RELEASE_MANIFEST.json`. Lý do: `pkg_secret_scan.py` nằm trong `_RELEASE_EXCLUDE_NAMES_ANYWHERE` (`scripts/tl_core/release.py:413`), fragment selftest cũng là dev-side, nên Package không đổi. Ngoài ra `RELEASE_MANIFEST.json` và `scripts/tl.py` đang bị lease `wp1009-cloud-setup-p1-r4-g4-claude` giữ (quét lúc 2026-10-30T04:2xZ). Nếu gate đòi các tệp ấy thì dừng lại và xin revision.

## 4. Trần
- Kích thước: ≤ 2 tệp / ≤ 220 dòng thêm.
- Lời gọi Codex: 10 theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không đổi `PATTERNS`. Mở rộng mẫu là việc khác.
- Không sửa `deploy-package.sh` hay `deploy-package.ps1`. Hai script dùng chung bộ quét, nên tự hưởng bản vá.
- Không chạy `--push` hay bất kỳ thao tác deploy thật nào.
