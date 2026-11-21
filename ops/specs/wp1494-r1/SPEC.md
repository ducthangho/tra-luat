# wp1494 r1 — B2 của kế hoạch nguồn r4: watchdog độ tươi biên nhận full audit (CANH-TUOI-AUDIT-B2)
packet_id: wp1494
revision: 1
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587
mission_issue: 1172
packet_issue: 1494
risk: sensitive
review_class: sensitive
executor: claude
environment: cloud (Linux)
immutable_acceptance_baseline: **B** — KHÔNG ghim trong tệp này; OID do Mission revision cài đặc tả và lease cùng ghi, theo mục "Baseline nghiệm thu"

Trạng thái: **ứng viên đóng băng, revision 1** (lượt soạn thứ 1 của packet này). CHƯA review spec, CHƯA được chủ kho duyệt băm, chưa có lease. Thẩm quyền: Mission #1172 r96 (`ops/specs/wp1172-source-plan-r4/mission-r96.json` trên nhánh `ops/wp1172-plan-r4`, sha256 `2d9a60a5eda9537475d7bb0901e882fef2d97d96a2ad4a4aa0d97c76862e73a9`, cài tại https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-7066078931), mục `packet_graph` vai B2: `admitted_spec_drafting`, ngân sách `per_new_packet` (soạn spec 5, review spec Codex 6); điều kiện tiên quyết của Mission: "đặc tả đóng băng được chủ kho duyệt băm và Mission revision riêng trước mọi lease" — điều kiện ấy chặt hơn quyết định 2 của `ADR-0067` và thắng cho packet này. Quyết định Q6 của chủ kho (Mission r84 `owner_decisions.Q6`): chấp nhận làn B; G7 là best-effort có giám sát chéo. Nguồn: kế hoạch nguồn r4 bản sửa 9 (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`; "§…" không ghi nguồn là tới tệp ấy), §5 B2, §7, §9 G7, §10 Q6; bảng ba trạng thái của r2 gốc §4 (`nguon/KE_HOACH_TOI_UU_MUTATION_TESTING_r2_2026-11-03.md` cùng thư mục, sha256 `f4611b0f0c79f33d56b293f5fcb854eeeae2fcbb6acbdfd59d6134dcbfbdcb8f`). Nơi đặc tả này khác kế hoạch thì đặc tả này thắng cho packet này; mỗi chỗ khác nêu ở "Chỗ lệch có chủ đích". Base lúc soạn: `master` `e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8` (đo 2026-11-21T17:01Z, merge PR #1492 = PR1 đã land); base thi công là B (mục "Baseline nghiệm thu").

**GHIM-B1A — hợp đồng biên nhận do B1a nắm thẩm quyền; khai ở MỘT chỗ này, mọi chỗ khác chỉ viết "GHIM-B1A" hoặc "B1a §n / luật Cn / điều Xn", không lặp băm, không định nghĩa lại luật nào của B1a** (cùng cách B3 r9 `ops/wp1461-r1@a12f6e8` tiêu dùng B1a):
- tệp `ops/specs/wp1460-r1/SPEC.md` revision 7, nhánh `ops/wp1460-r1`, commit `d1b08c219227d4b8925702029cd20d4e0febed54`, sha256 `d53341fb8d549d89f99e4cda0bd6ed380bf9975ce47b95a43ad1adaf5b3963b3` (đầu nhánh `163ece8` chỉ thêm hồ sơ review; Mission r96 `packet_graph` 1460: review spec lượt 7 approve 0 finding);
- **ba hiện vật máy = toàn bộ hợp đồng B2 tiêu dùng** (đo 2026-11-21T17:0xZ trên blob của `origin/ops/wp1460-r1`):
  - `ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json` — sha256 `844b5218b6f6844945f5c4c9440f09015d238fe09a60d64b3787c440787e4f46`;
  - `ops/specs/wp1460-r1/hop_dong/fixture.json` (`bien_nhan_audit.v1.fixture/3`, 120 ca) — sha256 `ce8595739a1ab2f4a86c9c196255e5f91fb19a9f6d3865df6caa2d66f9970e6d`;
  - **khối mã "Lệnh kiểm"** của tệp đặc tả B1a = các dòng GIỮA dòng đầu tiên bằng đúng ```` ```python ```` đứng sau dòng bắt đầu bằng `## Lệnh kiểm` và dòng kế tiếp bằng đúng ```` ``` ````, nối bằng LF, có LF cuối: sha256 `d9c78e708e18a211b7d8c7309638ffd1c73200578cf3128f9f0fc4275430f24e` (254 dòng, 14 992 byte). Hàm `tieu_dung` trong khối ấy là định nghĩa chuẩn tắc của luật C1–C12.
- **Luật tương thích:** bản B1a được chủ kho duyệt và được PR B1a thi công là tương thích ⇔ CẢ BA băm trên bằng nhau từng cái. Băm tệp đặc tả B1a khác mà ba băm bằng ⇒ vẫn tương thích, lease ghi băm tệp mới. Một trong ba băm khác ⇒ B2 DỪNG, cần revision mới; executor không tự chọn giữa hai bản.
- B2 tiêu dùng ĐÚNG hợp đồng ấy: không thêm trường, không tạo biến thể v1, không viết lại schema, không sửa tệp nào dưới `ops/specs/wp1460-r1/`. Hai hằng chỉ có trong văn xuôi B1a §1 — tên artifact `bien-nhan-audit-<run_id>-<run_attempt>` và tên tệp `bien_nhan_audit.json` — được kiểm trên tệp workflow thật tại B (điều kiện 2 của "Baseline nghiệm thu").
- **Đã chạy lúc soạn** (2026-11-21, `jsonschema` 4.26.0, Python 3.13.18): trích khối mã theo đúng luật trên rồi `python3 -I -B <tệp> <thư mục chứa hai tệp hop_dong>` ⇒ `FIXTURE: 480/480 phep kiem dung ky vong · hinh 120 · ngu nghia 118 · tu vung 79 · doi tuong 163 · luat duoc phu 12/12` / `TONG: DAT`, rc 0. Không chạy `--dot-bien` (249/249 là lời khai của B1a và review lượt 7; tác giả B2 không đo lại).

**Ba dòng khai ADR ở đầu tệp.** `tran_kich_thuoc_sensitive` là điều kiện `ADR-0053` đặt ra để trần MẶC ĐỊNH của packet `sensitive` là 6 tệp / 450 dòng thêm (thiếu nó: 3 / 300); nó không xin ngoại lệ. `tran_loi_goi_codex` kích hoạt trần mười lời gọi Codex review mỗi PR của `ADR-0055`; cách nó ghép với trần Mission ở "Quy trình và quyền". `dieu_kien_merge` kích hoạt `ADR-0060` (M10) cho packet này: M1 severity, M3 Windows, M5 push một lần, M6 draft, M9 full audit. Đo 2026-11-21T17:01Z cho CẢ BA OID, kho không shallow (`git rev-parse --is-shallow-repository` = `false`): `git cat-file -e <OID>:<tệp ADR>` rc 0 cho cả ba (`8ab1007…` với `docs/adr/0053-tran-kich-thuoc-sensitive-len-sau-tep.md`, `d2e3052…` với `docs/adr/0055-tran-loi-goi-codex-len-muoi.md`, `36d7c5d…` với `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`); `git cat-file -e <OID>^:<tệp ADR>` rc 128 cho cả ba; `git rev-list --first-parent origin/master` (đầu `e2f28fb`) chứa cả ba OID (đếm khớp nguyên dòng = 3). Tệp này có đúng một dòng khai cho mỗi ADR ấy và không có dòng khai `ADR-0052`.

## Mục tiêu
Sau packet này, một workflow riêng chạy mỗi 6 giờ (và theo `workflow_dispatch`) đọc REST các lượt `schedule` của `.github/workflows/ci-dot-bien-du.yml`, phán biên nhận B1a của chúng bằng luật C1–C12 (GHIM-B1A) với đầu vào ĐỘC LẬP lấy từ REST, xếp kết quả vào MỘT trong bốn trạng thái `fresh` · `due_in_progress` · `stale_or_missing` · `khong_do_duoc` theo khung cron, rồi ghi nhịp tim và (khi cần) cảnh báo lên MỘT Issue theo dõi và ĐỌC LẠI những gì đã ghi. Không đọc được thì không bao giờ là `fresh`. Chỉ báo cáo: không chặn merge, không chặn release.

## Hợp đồng

### 1. Bất biến
- **I1 — Chỉ thêm.** Không sửa `ci-dot-bien-du.yml`, `ci.yml`, `ops/ci_provenance.py`, `.claude/dev/packet_loop.py`, mọi tệp dưới `ops/specs/wp1460-r1/`. Ở `.claude/dev/ci_dang_ky_test.py` chỉ thêm ĐÚNG MỘT mục đăng ký bộ test mới vào `MOI` (mục 9).
- **I2 — Bốn trạng thái, một chiều.** Mọi phép đọc cho ra `dat` · `khong_dat` · `khong_do_duoc`; `khong_do_duoc` không bao giờ thành `dat`, và trạng thái tổng chỉ là `fresh` khi có một lượt `dat` cho khung hiện hành (mục 5).
- **I3 — Không seam đổi quyết định.** Không biến môi trường, tham số dòng lệnh hay input dispatch nào đổi kho, workflow được canh, số Issue, hằng thời gian, hay bỏ bước. Hằng nằm trong mã. Test tiêm đồng hồ, transport và số Issue bằng THAM SỐ HÀM Python, không qua môi trường.
- **I4 — Bí mật.** Token chỉ đọc từ biến `GH_TOKEN` mà bước workflow đặt bằng `github.token`; không lên argv, không vào báo cáo, không in ra; `Authorization` chỉ gửi tới `api.github.com` (không gửi tới host lưu trữ của lời chuyển hướng tải artifact). Không đọc secret nào khác.
- **I5 — Không hồi tố, không dựng mốc.** Lượt trước B1a không có biên nhận ⇒ `khong_dat` (biên nhận vắng); không suy "xanh" từ kết luận REST. Không thay mốc REST bằng giờ hiện tại hay giờ của attempt.
- **I6 — Ghi phải đọc lại.** Mọi lần ghi Issue được đọc lại bằng REST; lệch hoặc lỗi ⇒ job ĐỎ (mã 3, mục 9). Job đỏ KHÔNG có nghĩa chủ kho đã nhận tin (mục 10).
- **I7 — Không viết dấu bỏ-qua-CI** (chuỗi mà GitHub đọc để không chạy workflow, ở mọi biến thể hoa thường và thứ tự từ) vào bất kỳ tệp giao nộp, văn bản Issue/comment do workflow sinh, hay commit message nào của packet. Đặc tả này chỉ nhắc nó bằng lời.

### 2. Thời gian và khung
- **Kho, workflow được canh, cron ghim:** `ducthangho/tra-luat`; `.github/workflows/ci-dot-bien-du.yml`; `CRON_GHIM` = `17 19 * * 6` và hàm `khung_cron` của khối mã GHIM-B1A (chép nguyên văn, như `tieu_dung`): mốc thứ Bảy 19:17:00 UTC gần nhất ≤ một thời điểm.
- **T** = thời điểm đánh giá: `datetime.now(timezone.utc)` cắt về giây, đọc MỘT lần ở đầu tiến trình, ghi vào báo cáo; test tiêm T bằng tham số hàm.
- **F** = `khung_cron(T)` (khung hiện hành); **P** = F − 7 ngày (khung trước).
- **Gán khung cho một lượt:** khung của lượt R = `khung_cron(R.created_at)` với `created_at` của REST (D2), KHÔNG từ biên nhận. `created_at` phải khớp trọn `YYYY-MM-DDTHH:MM:SSZ` và là thời điểm có thật; một phần tử của danh sách lượt vi phạm ⇒ danh sách `khong_do_duoc` (mã `khoa_chon_khong_doc_duoc`). Hệ quả đóng băng: chạy lại một attempt KHÔNG đổi `created_at` của lượt nên KHÔNG đổi khung; một lượt `workflow_dispatch` không bao giờ là ứng viên (mục 3, D1), nên dispatch trên SHA cũ không làm mới gì.
- **Ba hằng thời gian (đóng băng):**
  - `TRE_LICH_TOI_DA` = 12 giờ: khung F chưa có lượt nào khi T > F + 12 h ⇒ khung VẮNG. Căn cứ đo (mục "Số đo lúc soạn"): 7/7 lượt `schedule` đã có của `ci-dot-bien-du.yml` được tạo trễ 2 h 11 m … 3 h 41 m sau mốc cron. 12 h là "độ trễ lịch đã khai" của G7.
  - `TUOI_TOI_DA` = 8 ngày: tuổi snapshot = T − khung của lượt `dat` đang dùng; > 8 ngày ⇒ không còn tươi (r2 §4: "cửa 8 ngày là trần tuổi của snapshot gốc, không phải ân hạn thêm sau 36 giờ").
  - Ân hạn 36 h của r2 §4 KHÔNG được mã hoá thành hằng riêng: với cron 7 ngày, điều kiện tuổi ≤ 8 ngày của khung P hết ở F + 24 h, TRƯỚC F + 36 h, nên một hằng 36 h sẽ là mã chết và đột biến của nó là đột biến TƯƠNG ĐƯƠNG (khai ở "Bảng đột biến"). Ân hạn hiệu dụng cho khung đang chạy là 24 h; chặt hơn 36 h, ghi ở "Chỗ lệch có chủ đích" 1.
- **G7 phát biểu đúng phạm vi:** một khung vắng hoặc đỏ được báo `stale_or_missing` trong lượt watchdog đầu tiên chạy sau F + 12 h (vắng) hoặc ngay lượt đầu sau khi lượt đỏ hoàn tất (đỏ), hoặc muộn nhất sau F + 24 h (đang chạy quá lâu); cộng tối đa một chu kỳ watchdog (6 h) và độ trễ lịch của chính watchdog — điều mà GitHub không bảo đảm (mục 10). Best-effort có giám sát chéo theo Q6.

### 3. Đầu vào REST và luật liệt kê
Mọi lời gọi tới `https://api.github.com/repos/ducthangho/tra-luat…`, chỉ GET trừ D11/D12. Mã đường đi D1–D13 (đặt tên D để khỏi lẫn với mã E1–E5 của `ADR-0067`):

| # | Endpoint | Quyền | Dùng cho |
|---|---|---|---|
| D1 | `/actions/workflows/ci-dot-bien-du.yml/runs?event=schedule&per_page=100` | Actions: read | danh sách ứng viên (mọi khung) |
| D2 | `/actions/runs/{id}` | Actions: read | T1, T7 (U6) |
| D3 | `/actions/runs/{id}/jobs?filter=all&per_page=100` | Actions: read | T1 |
| D4 | `/actions/runs/{id}/artifacts?per_page=100` | Actions: read | T1, T2, T5 |
| D5 | `/actions/artifacts/{id}/zip` (lớp R/S) | Actions: read | T2, T5 |
| D6 | `/contents/.github/workflows/ci-dot-bien-du.yml?ref={run.head_sha}` | Contents: read | T3 (`job_ky_vong`) |
| D7 | `/git/commits/{run.head_sha}` | Contents: read | T3 (`tree_h`) |
| D8 | `/git/ref/heads/master` | Contents: read | báo cáo (SHA đầu master) |
| D9 | `/compare/{sha_audit}...{sha_master}` | Contents: read | báo cáo (khoảng cách) |
| D10 | `/issues/{ISSUE_THEO_DOI}` (GET) | Issues: read | nhịp tim trước; đọc lại sau D11 |
| D11 | `/issues/{ISSUE_THEO_DOI}` (PATCH `{"body","state":"open"}`) | Issues: write | ghi nhịp tim |
| D12 | `/issues/{ISSUE_THEO_DOI}/comments` (POST) | Issues: write | cảnh báo |
| D13 | `/issues/comments/{id}` (GET) | Issues: read | đọc lại comment vừa ghi |

**Ba lớp phản hồi** (giữ nguyên định nghĩa lớp J/R/S của B3 r9 mục 5, chép lại đây vì B2 là tệp riêng):
- **J — JSON từ `api.github.com`** (mọi D trừ thân tải của D5): nhận 2xx chỉ khi có header `X-GitHub-Request-Id` và thân là JSON đúng kiểu mong đợi. 2xx không dấu, 3xx, 4xx, 5xx, JSON hỏng, hết giờ ⇒ `khong_do_duoc` kèm mã phân biệt "GitHub trả `<mã>`" với "không có dấu GitHub".
- **R — chuyển hướng của D5:** 302 từ `api.github.com`, có `X-GitHub-Request-Id`, `Location` là URL `https`; tối đa 3 lần. Khác ⇒ `khong_do_duoc`.
- **S — tải từ host lưu trữ:** KHÔNG gửi `Authorization`. Trọn ⇔ mã 200, đọc hết luồng không lỗi, số byte bằng `Content-Length` khi có header ấy, kích thước ≤ `TRAN_GOI` (hằng trong mã). Không trọn ⇒ `khong_do_duoc`. Lớp S trả (byte, sha256), không phán nội dung.
- Mỗi lời gọi có hạn giờ; thử lại có trần cho lỗi mạng/5xx/429 (kết quả = lần thử CUỐI); tổng thời gian tiến trình có trần (hằng), vượt ⇒ các phép đọc chưa xong `khong_do_duoc`.
- **Biên ngoại lệ (đóng băng; cùng chính sách B3 r9 cho `nhap_wd`, quyết định chủ kho [E1+E2] 2026-11-21):** mỗi lời gọi ra ngoài tiến trình — gọi transport HTTP, `json.loads(<byte>.decode("utf-8"))`, mở/đọc ZIP bằng `zipfile`, `yaml.safe_load`, nạp `jsonschema`, và lời gọi `tieu_dung` — nằm trong một khối `try` chỉ chứa ĐÚNG lời gọi ấy và phép gán kết quả; mọi ngoại lệ `e` thoát ra mà `isinstance(e, Exception)` ⇒ phép đọc ấy `khong_do_duoc`, mã `<tên điểm>_nem:<type(e).__module__>.<type(e).__qualname__>`. KHÔNG có danh sách lớp ngoại lệ, không phép so `type(e)`, không nhánh bắt hẹp hơn. `BaseException` không phải `Exception` không bị bắt. Riêng ĐỌC-JSON và ĐỌC-ZIP dùng đúng định nghĩa miền của B3 r9 mục 4.2 (mục thư mục không phải tệp; hai mục cùng tên là hai tệp), chỉ thay danh sách ngoại lệ liệt kê của B3 bằng luật "mọi `Exception`" này.
- **Lưới an toàn của pha đánh giá:** toàn bộ pha đánh giá (mục 4–6, trước mọi lần ghi) chạy trong MỘT khối bắt mọi `Exception`; ngoại lệ thoát ra ⇒ trạng thái tổng `khong_do_duoc`, mã `danh_gia_nem:<module>.<qualname>`, và pha ghi (mục 7) VẪN chạy. Lý do: mục đích của watchdog là báo; một lỗi lập trình không được làm im cảnh báo. Pha ghi KHÔNG nằm trong khối ấy.

**Luật liệt kê, thứ tự và duy nhất** (U1–U6 cùng nghĩa với B3 r9 mục 4.0; nêu lại phần B2 dùng):
- **U1 — Trọn rồi mới dùng.** Danh sách TRỌN ⇔ không còn `rel="next"` trong giới hạn trang `TRANG_TOI_DA` = 10 VÀ số phần tử gom được bằng `total_count` của trang CUỐI VÀ U2 đạt. Không trọn ⇒ `khong_do_duoc`; không dùng phần đã thấy (kể cả khi phần ấy có một lượt `dat`).
- **U2 — `id` là khoá duy nhất.** Mọi phần tử có `id` số nguyên dương (`bool` không tính), không hai phần tử cùng `id`; vi phạm ⇒ `khong_do_duoc` (`danh_sach_sai_kieu` / `danh_sach_trung_id`), không khử trùng lặp.
- **U5 — "Đúng một" không thay thế.** 0 ⇒ `khong_dat` hậu tố `_vang`; ≥ 2 ⇒ `khong_dat` hậu tố `_trung`.
- **U6 — Ảnh chụp lượt nhất quán.** Với mỗi lượt được phán: đọc D2 ĐẦU và CUỐI việc phán lượt ấy; `run_attempt`, `status`, `conclusion`, `updated_at` của hai lần đọc phải bằng nhau, lệch ⇒ lượt `khong_do_duoc` (`luot_doi_giua_chung`). Mọi phép con dùng bản đọc ĐẦU.
- **U7 — Thứ tự tại biên với `tieu_dung`.** Bảng đủ mọi danh sách của đặc tả này (đếm DÒNG: 6):

| # | Danh sách | Đi tới | Phụ thuộc thứ tự? | Luật |
|---|---|---|---|---|
| 1 | lượt của D1 | gán khung, gộp khung (mục 5), chọn `sha_audit` | không: gộp khung giao hoán; `sha_audit` lấy lượt `dat` có `id` NHỎ NHẤT | không xếp |
| 2 | `rest.jobs` (D3) | `tieu_dung` | CÓ (đo ở B3 r9 mục 4.0: bảng "bản ghi mới nhất theo tên" giữ bản ghi gặp đầu tiên) | xếp `id` TĂNG trước khi trao; xếp không lọc, không khử trùng |
| 3 | `rest.artifacts` (D4) | `tieu_dung`; T2 (đếm tên); T5 (tra `id`) | không: tra theo `id`, U2 cấm trùng | không xếp |
| 4 | `ngoai.job_ky_vong` (T3) | `tieu_dung` | không, vì T3 từ chối tên trùng và khoá trùng | không xếp |
| 5 | `ngoai.tai_ve` (T5) | `tieu_dung` | không: bảng theo `id` | khoá là `id` viết thập phân |
| 6 | các mảng trong biên nhận | `tieu_dung` | CÓ | NGUYÊN thứ tự tài liệu JSON đã so digest; B2 không xếp lại |

- **Phần tử của D1 phải đúng hình**, không thì danh sách `khong_do_duoc` (`danh_sach_la`): `event == "schedule"`, `path == ".github/workflows/ci-dot-bien-du.yml"`, `head_branch == "master"`, `head_sha` 40 hex thường, `status` chuỗi, `created_at` như mục 2. Không có bộ lọc `created` phía máy chủ: mọi lượt `schedule` đều được liệt kê (đo 2026-11-21: `total_count` = 7), và giới hạn 10 trang × 100 là trần biết trước; vượt ⇒ `khong_do_duoc`.

### 4. Phán một lượt audit R (bảy phép con T1–T7)
Chỉ áp cho lượt có D2 đọc ĐẦU trả `status == "completed"`; lượt có `status` khác ⇒ phán quyết lượt = `dang_chay` (không đọc biên nhận, không phép con nào). Với lượt completed, mỗi phép con có mã cố định; phụ thuộc là đồ thị cố định; phép con không đủ điều kiện ghi `khong_danh_gia` và không tham gia phép VÀ.
- **T1 `doc_rest`** — D2 (đầu), D3 trọn, D4 trọn; trường bắt buộc và kiểu như B3 r9 K1 (run: `id`, `run_attempt`, `status`, `conclusion`, `event`, `head_sha`, `path`, `created_at`, `repository.full_name`, `repository.id`; job: `id`, `name`, `run_attempt`, `status`, `conclusion`; artifact: `id`, `name`, `expired`, khoá `digest`). Thiếu, sai kiểu, không trọn ⇒ `khong_do_duoc`. Đầu ra `rest` = {`run` bản đọc đầu, `jobs` đã xếp theo U7 dòng 2, `artifacts`}.
- **T2 `bien_nhan`** (cần T1) — tên N = `bien-nhan-audit-<run.id>-<run.run_attempt>`; đếm phần tử `name == N` trong D4 (U5: `bien_nhan_vang` / `bien_nhan_trung`; biên nhận của attempt thấp hơn không bao giờ được dùng thay); `expired` khác `false` ⇒ `khong_dat`; tải (D5): không trọn ⇒ `khong_do_duoc`; sha256(gói) ≠ `digest` ⇒ `khong_dat`; gói không mở được, không có đúng MỘT tệp, hoặc tệp không tên `bien_nhan_audit.json` ⇒ `khong_dat`; nội dung không đọc được như JSON UTF-8 ⇒ `khong_dat`.
- **T3 `dau_vao_doc_lap`** (cần T1) — `job_ky_vong` lập từ thân D6 tại `run.head_sha` (base64 giải mã), theo ĐÚNG luật đặt tên của B1a điều X2 như B3 r9 K3 đã chốt (job không `strategy` ⇒ tên là khoá; `strategy.matrix` là object một khoá, giá trị là danh sách khác rỗng số nguyên hoặc chuỗi ⇒ `<khoá> (<giá trị>)`; hình khác ⇒ `khong_dat` mã `hinh_workflow_la`; tên trùng ⇒ `job_ky_vong_trung`; hai tên khác nhau cùng khoá `khoa_tu_ten` ⇒ `job_ky_vong_trung_khoa`); `tree_h` = `tree.sha` của D7. D6/D7 không đọc được hoặc YAML ném ⇒ `khong_do_duoc`. `h` = `run.head_sha`. Đây là chỗ B2 đọc "workflow tại `su_kien.sha`" của B1a §5 bằng giá trị REST thay cho giá trị biên nhận tự khai; hai giá trị chỉ khác khi C3 đã vi phạm (chỗ lệch 2).
- **T4 `hop_dong`** — schema = tệp `ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json` trong CHECKOUT của chính workflow watchdog; sha256 phải bằng băm của GHIM-B1A (hằng trong mã) và `jsonschema.Draft202012Validator` nạp được. Lệch (`hop_dong_lech_ghim`), vắng, thiếu thư viện ⇒ `khong_do_duoc`. Tính một lần mỗi tiến trình.
- **T5 `tai_goi`** (cần T1, T2, T4 và biên nhận đúng hình với `ok == true`) — y hệt B3 r9 K5: ID_TẢI = tập `id` khác nhau mà biên nhận nêu (`job[].dau_job.id`, `manh[].artifact.id`) có trong D4 với `expired == false`; tải mỗi `id` đúng một lần; `tai_ve[<id>]` = `{sha256_goi, tep}`, `tep` = mọi tệp của gói xếp theo tên, mỗi phần tử `{ten, sha256, noi_dung}` (`noi_dung` = ĐỌC-JSON hoặc `null`). Tải không trọn ⇒ `khong_do_duoc`. Biên nhận sai hình hoặc `ok` khác `true` ⇒ ID_TẢI rỗng, T5 `dat`.
- **T6 `luat_C`** (cần T1–T5 `dat`) — gọi `tieu_dung` CHÉP NGUYÊN VĂN từ khối mã GHIM-B1A (cùng ngôn ngữ; nghiệm thu 3 là thước đo) với `V` dựng từ schema của T4, biên nhận của T2, `rest` của T1, `ngoai` = {`h`, `tree_h`, `job_ky_vong` của T3, `tai_ve` của T5}. `vi_pham` rỗng ⇒ `dat`; khác rỗng ⇒ `khong_dat`, mã `luat_C:` + các luật xếp theo số tăng nối bằng `+`. `canh_bao` chứa `C10` ⇒ báo cáo ghi nguyên văn `C10` cùng `dinh_danh_definition` của biên nhận (B1a luật C10: "B2 báo nguyên văn"); KHÔNG đổi phán quyết. Hàm ném ⇒ `khong_do_duoc` (biên ngoại lệ, mục 3).
- **T7 `anh_chup`** — đọc D2 CUỐI; U6. Lệch ⇒ `khong_do_duoc`.
- **Phán quyết lượt** (completed) = phép VÀ trên các phép con ĐÃ đánh giá: có `khong_dat` ⇒ `khong_dat`; không thì có `khong_do_duoc` ⇒ `khong_do_duoc`; không thì `dat`. Lượt `dat` ⇔ T1–T7 đều `dat`. Ghi nhận thêm (không quyết định): `moc_tuoi` do `tieu_dung` trả; với lượt `dat`, nó BẰNG khung REST của lượt (C9 bảo đảm) — bộ test canh bất biến này.

### 5. Gộp khung và trạng thái tổng
**Gộp khung K** (K ∈ {F, P}) trên tập ứng viên = các lượt của D1 có khung REST = K: có lượt `dat` ⇒ `dat`; không thì có lượt `khong_dat` ⇒ `do`; không thì có lượt `khong_do_duoc` ⇒ `khong_do_duoc`; không thì có lượt `dang_chay` ⇒ `dang_chay`; không thì (0 ứng viên) ⇒ `vang`. Kết quả không phụ thuộc thứ tự.

**Trạng thái tổng S** — áp luật đầu tiên khớp, từ trên xuống; mã lý do chính ghi kèm:

| # | Điều kiện | S | mã |
|---|---|---|---|
| S1 | D1 không trọn/không đọc được, hoặc T4 `khong_do_duoc`, hoặc lưới an toàn bắt ngoại lệ | `khong_do_duoc` | mã của phép hỏng |
| S2 | gộp F = `dat` | `fresh` | `khung_xanh` |
| S3 | gộp F = `do` | `stale_or_missing` | `khung_do` |
| S4 | gộp F = `khong_do_duoc` | `khong_do_duoc` | `khung_khong_do_duoc` |
| S5 | gộp F = `vang` và T > F + `TRE_LICH_TOI_DA` | `stale_or_missing` | `khung_vang` |
| S6 | gộp F ∈ {`dang_chay`, `vang`} và T − P > `TUOI_TOI_DA` | `stale_or_missing` | `qua_tuoi_8_ngay` |
| S7 | gộp F ∈ {`dang_chay`, `vang`}, còn lại: xét gộp P — `dat` ⇒ `due_in_progress` (`khung_dang_cho`); `khong_do_duoc` ⇒ `khong_do_duoc` (`khung_truoc_khong_do_duoc`); khác ⇒ `stale_or_missing` (`khung_truoc_khong_xanh`) | | |

S1 xét TRƯỚC mọi luật khác nên một danh sách không trọn không bao giờ cho `fresh`, kể cả khi phần đã thấy có lượt `dat`. Biên: "T > F + 12 h" và "T − P > 8 ngày" là so CHẶT; T bằng đúng biên còn trong hạn. S6 đứng trước S7 nên lượt đang chạy quá F + 24 h không được tính là đang chờ.

Lần chạy đầu sau khi B1a land: khung P là lượt trước B1a (không có biên nhận) ⇒ trong ân hạn của khung đầu tiên có biên nhận, S7 cho `stale_or_missing` (`khung_truoc_khong_xanh`). Đây là cảnh báo ĐÚNG theo luật (chưa có bằng chứng tuần trước), không phải lỗi; runbook nêu.

### 6. Báo cáo
Một đối tượng JSON (in ra stdout một dòng, `ensure_ascii=True`, `sort_keys=True`) và bản đọc người ở `$GITHUB_STEP_SUMMARY` (biến do runner cấp; vắng ⇒ bỏ, không lỗi). Trường: `schema` = `b2_bao_cao.v1`; `T`; `F`; `P`; `trang_thai`; `ma_ly_do`; mỗi khung: phán quyết gộp và danh sách lượt (`id`, `run_attempt`, `head_sha`, phán quyết, mã từng phép con, `canh_bao`, `dinh_danh_definition` khi có `C10`); `sha_audit` = `head_sha` của lượt `dat` có `id` nhỏ nhất ở khung quyết định trạng thái (F khi `fresh`, P khi `due_in_progress`; `null` khác); `sha_master` (D8, hoặc `khong_do_duoc`); `so_sanh` = {`status`, `ahead_by`, `behind_by`} của D9 khi cả hai SHA có, hoặc `khong_do_duoc` / `khong_ap_dung`; `nhip_tim_truoc` (mục 7); `kenh_giao_tin` (mục 10). D8/D9 lỗi KHÔNG đổi `trang_thai` (chúng là thông tin, không phải bằng chứng audit).
- **Câu về master (đóng băng, r2 §4):** dòng tóm tắt người đọc in ĐÚNG MỘT trong ba câu: `master hiện tại = SHA đã audit <sha>` (chỉ khi `sha_master` và `sha_audit` có và BẰNG nhau); `master hiện tại KHÁC SHA đã audit: master <sha_master>, audit <sha_audit>, master đi trước <ahead_by> commit` (khi khác; `ahead_by` thay bằng `khong_do_duoc` khi D9 lỗi); `chưa có SHA đã audit hợp lệ hoặc không đọc được master` (còn lại). Không văn bản nào do watchdog sinh nói master hiện tại "đã đủ", "đã audit" hay "xanh" khi hai SHA khác nhau.

### 7. Issue theo dõi và nhịp tim
- **Số Issue:** hằng `ISSUE_THEO_DOI` trong mã = số của MỘT Issue do phiên điều phối tạo TRƯỚC khi cấp lease (thân tuỳ ý; lượt đầu ghi đè), ghi trong Mission revision cài đặc tả và trong lease; hai nơi lệch ⇒ không thi công. Workflow KHÔNG tạo Issue, không tìm Issue theo tiêu đề hay nhãn. Hằng không phải số nguyên dương ⇒ mã 2, không gọi mạng.
- **Thân Issue (đóng băng) = đúng hai dòng, nối bằng một LF, không LF cuối:** dòng 1 `B2 watchdog do tuoi full audit (wp1494). Than Issue do workflow ghi de moi luot; dung sua tay.`; dòng 2 `B2_NHIP_TIM: ` + JSON của nhịp tim, `json.dumps(x, ensure_ascii=True, sort_keys=True, separators=(",", ":"))`. Toàn thân là ASCII (tránh lớp chuẩn hoá chuỗi khi đọc lại).
- **Nhịp tim `b2_nhip_tim.v1`** — tập khoá ĐÓNG: `schema` (= `b2_nhip_tim.v1`), `luc` (= T, `YYYY-MM-DDTHH:MM:SSZ`), `run_id`, `run_attempt` (của lượt watchdog, từ context `github.run_id`/`github.run_attempt` truyền qua `env`), `trang_thai`, `ma_ly_do`, `khung` (= F), `sha_audit`, `sha_master` (chuỗi 40 hex hoặc `null`).
- **Luật đọc nhịp tim (đóng băng; dành cho lượt watchdog kế tiếp VÀ cho packet nối nhịp tim vào B3, chỗ lệch 8 của B3 r9):** đọc thân bằng D10; tách theo `\n`; đếm dòng bắt đầu bằng ĐÚNG `B2_NHIP_TIM: ` — 0 ⇒ `vang`; ≥ 2 ⇒ `khong_doc_duoc` (`nhip_tim_trung`); 1 ⇒ phần sau tiền tố đọc bằng ĐỌC-JSON; phải là object đúng tập khoá đóng, `schema` đúng, `luc` đúng dạng và có thật; sai ⇒ `khong_doc_duoc`. `luc` > T ⇒ `khong_doc_duoc` (`nhip_tim_tuong_lai`). T − `luc` > 24 h ⇒ `cu`; còn lại ⇒ `moi`. D10 lỗi ⇒ `khong_doc_duoc`. Không có phép chọn "mới nhất" nào: Issue có đúng một chỗ chứa nhịp tim.
- **Trình tự pha ghi (mỗi lượt, cả khi S là `khong_do_duoc`):** (1) D10 đọc nhịp tim TRƯỚC (làm trước pha đánh giá; kết quả là `nhip_tim_truoc`); (2) D11 PATCH thân mới + `state: "open"`; (3) D10 đọc lại: `body` BẰNG từng ký tự thân vừa gửi VÀ `state == "open"`, không thì lỗi ghi; (4) nếu luật comment dưới đây đòi: D12 POST comment, rồi D13 đọc lại theo `id` trả về: `body` bằng từng ký tự, không thì lỗi ghi. Lỗi ghi ở bất kỳ bước nào ⇒ mã thoát 3 (mục 9), sau khi đã thử các bước còn lại.
- **Luật comment (đóng băng):** POST một comment ⇔ ÍT NHẤT MỘT trong: (a) S ∈ {`stale_or_missing`, `khong_do_duoc`} và bộ (`trang_thai`, `khung`, `ma_ly_do`) khác bộ tương ứng của nhịp tim TRƯỚC (nhịp tim trước không phải `moi`/`cu` hợp lệ ⇒ coi là khác); (b) S ∈ {`fresh`, `due_in_progress`} và nhịp tim trước hợp lệ có `trang_thai` ∈ {`stale_or_missing`, `khong_do_duoc`} (báo hồi phục); (c) `nhip_tim_truoc` ∈ {`cu`, `vang`, `khong_doc_duoc`} (lượt watchdog trước vắng hoặc dấu hỏng). Thân comment: dòng đầu `B2 watchdog: <trang_thai> (<ma_ly_do>)`, rồi dòng tóm tắt master của mục 6, `nhip_tim_truoc`, URL lượt watchdog; ASCII hoặc UTF-8 đều được, không chứa dấu bỏ-qua-CI. Comment lặp cùng bộ không được gửi lại (chống spam); job vẫn đỏ mỗi lượt khi S là trạng thái cảnh báo (mục 9).

### 8. Workflow (hình đóng băng; chốt bằng ca trong bộ test của packet)
Tệp `.github/workflows/canh-tuoi-audit.yml`, đúng các khoá sau, không khoá nào khác ở mức workflow và mức job:
- `name`; `on`: `schedule` đúng một mục `cron: "41 */6 * * *"` + `workflow_dispatch` TRẦN (không `inputs`); không trigger nào khác.
- `permissions` mức workflow ĐÚNG `{actions: read, contents: read, issues: write}`; không `permissions` mức job.
- `concurrency`: `group: canh-tuoi-audit`, `cancel-in-progress: false`.
- Đúng một job `canh-tuoi`: `runs-on: ubuntu-latest`, `timeout-minutes: 20`, không `if`, không `continue-on-error`, không `strategy`. Bước theo thứ tự: (1) `actions/checkout@v4` với `persist-credentials: false`; (2) `actions/setup-python@v5` `python-version: "3.12"`; (3) `python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0`; (4) `python ops/canh_tuoi_audit.py` với `env:` ĐÚNG ba biến `GH_TOKEN: ${{ github.token }}`, `B2_RUN_ID: ${{ github.run_id }}`, `B2_RUN_ATTEMPT: ${{ github.run_attempt }}`. Không thân `run` nào chứa biểu thức Actions, kể cả trong chú thích.
- Hai biến `B2_RUN_*` là context để ghi nhịp tim, không phải seam quyết định (I3): sai dạng ⇒ mã 2.
- **Cổng:** `actionlint` trên tệp này rc 0 với `shellcheck` CÓ MẶT (ghi phiên bản; vắng ⇒ phép đo không tính), delta finding so B = 0.

### 9. Mã thoát
0 — pha ghi đạt và S ∈ {`fresh`, `due_in_progress`} · 1 — pha ghi đạt và S ∈ {`stale_or_missing`, `khong_do_duoc`} · 2 — cấu hình/context sai (`ISSUE_THEO_DOI`, `B2_RUN_*`, `GH_TOKEN` rỗng), không gọi mạng, không ghi · 3 — một bước ghi/đọc lại của mục 7 lỗi (bất kể S). Chỉ mã 0 làm job xanh.

### 10. Giới hạn giao tin, nói thẳng
- GitHub không bảo đảm lượt `schedule` chạy đúng giờ hay chạy: lượt có thể trễ hàng giờ (đo được tới 3 h 41 m ở `ci-dot-bien-du.yml`) hoặc bị bỏ khi tải cao; với kho công khai, GitHub tự tắt lịch sau một thời gian kho không hoạt động (tài liệu GitHub; CHƯA ĐO ở kho này, chưa đo kho công khai hay riêng). Watchdog cũng chịu đúng rủi ro ấy, nên nó không phải SLA: phần bù là (a) lượt watchdog kế tiếp đọc nhịp tim trước (luật comment (c)); (b) phiên điều phối kiểm nhịp tim bằng TAY ở đầu mỗi phiên theo runbook (mục "Runbook điều phối"); (c) packet sau nối nhịp tim vào B3.
- Job đỏ và comment trên Issue KHÔNG chứng minh chủ kho đã nhận tin: định tuyến thông báo phụ thuộc người theo dõi Issue và cài đặt thông báo của họ. **Điều kiện bật B2** (theo §5 B2): chủ kho subscribe Issue theo dõi và xác nhận đã nhận MỘT comment thật của watchdog. Ở packet này hằng `KENH_GIAO_TIN_XAC_NHAN` = `None` ⇒ báo cáo ghi `kenh_giao_tin: chua_do`; điền URL xác nhận là việc của một PR sau, ngoài packet này.
- Mọi ai có quyền ghi kho đều sửa được workflow, thân Issue hay chạy dispatch từ một nhánh có mã khác, nên nhịp tim là giám sát chéo chống tay trượt và lịch rơi, không phải bằng chứng chống người có quyền ghi. Rủi ro tồn dư, Q6.

### Chỗ lệch có chủ đích so với kế hoạch r4 / r2
1. Ân hạn hiệu dụng của khung đang chạy là 24 h (từ trần tuổi 8 ngày của r2), không 36 h; 36 h không có hằng riêng (mục 2). Chặt hơn.
2. `job_ky_vong` và `tree_h` đọc tại `run.head_sha` của REST thay cho `su_kien.sha` của biên nhận (B1a §5); chỉ khác khi C3 đã vi phạm.
3. Lượt `workflow_dispatch` của `ci-dot-bien-du.yml` không bao giờ làm tươi: tuổi neo vào khung `schedule` (r2 "tuổi tính từ slot"); dispatch bù cho một khung bị lịch bỏ KHÔNG xoá cảnh báo của khung ấy. Chặt hơn.
4. Khung vắng được báo sau 12 h (đo độ trễ lịch), không đợi hết ân hạn (r2: "không chờ đến 8 ngày mới báo").
5. Issue theo dõi có số cố định do điều phối tạo trước, không "mở" tự động; "cập nhật" = ghi đè thân + comment theo luật. Không có đường tạo Issue tự động nên không có đua tạo trùng.
6. Nhịp tim nằm ở THÂN Issue (một chỗ, không cần chọn "mới nhất", không phình theo thời gian); cảnh báo đi bằng comment (thông báo cho người subscribe; sửa thân không thông báo). B3 r9 mục 4.4 dựng chỗ cắm bằng danh sách comment (E7 của B3); packet nối nhịp tim vào B3 phải đọc theo luật mục 7 này, không theo comment.
7. Quyền workflow là `actions: read`, `contents: read`, `issues: write`: `contents: read` cần cho checkout mã watchdog, D6–D9; không quyền nào khác.
8. "Runbook dev-side" nằm trong đặc tả này (mục "Runbook điều phối"), không thêm tệp `docs/` vào PR giao nộp.

## Nghiệm thu
Mọi ca chạy offline trên transport giả GIỮ TRẠNG THÁI (ghi nhật ký từng lời gọi: phương thức, URL, header `Authorization` có/không, thân gửi), đồng hồ tiêm, số Issue tiêm. Mỗi luật có ca HAI CHIỀU (một ca đổi màu khi luật bị gỡ, một ca giữ màu khi đầu vào hợp lệ). Ca đạt đòi ĐÚNG `trang_thai` và `ma_ly_do`, không chỉ mã thoát.
1. **Ba trạng thái từng phép con T1–T7 và từng lớp J/R/S:** mỗi phép con một ca cho mỗi trạng thái nó có (`dat`, `khong_dat`, `khong_do_duoc`; T1, T4, T5, T7 không có `khong_dat`; T6 có cả ba vì `tieu_dung` ném ⇒ `khong_do_duoc`). Lớp J: 403 có dấu, 403 không dấu, 404, 5xx hết lượt thử, hết giờ, JSON hỏng, 200 không dấu, 2 trang đủ, vượt 10 trang, `total_count` lệch, trùng `id`, `id` kiểu `bool`. Lớp R/S: 302 → ZIP nhị phân thật được nhận; `Location` không `https`; quá 3 chuyển hướng; thân ngắn hơn `Content-Length`; vượt `TRAN_GOI`; yêu cầu tới host lưu trữ KHÔNG mang `Authorization` (đọc nhật ký transport).
2. **Biên ngoại lệ:** với mỗi điểm của mục 3 (transport, ĐỌC-JSON, ĐỌC-ZIP, YAML, nạp schema, `tieu_dung`) một ca ném một lớp `Exception` KHÔNG thuộc thư viện chuẩn quen dùng (lớp tự định nghĩa trong test) ⇒ đúng mã `<điểm>_nem:<module>.<qualname>`, trạng thái `khong_do_duoc`, không bao giờ `fresh`. Một ca ném `KeyboardInterrupt` từ transport ⇒ không bị bắt (tiến trình kết thúc khác 0). Lưới an toàn: một lỗi lập trình tiêm vào pha đánh giá ⇒ S `khong_do_duoc`, `danh_gia_nem:…`, pha ghi VẪN chạy (D11 có trong nhật ký), mã 1.
3. **Bằng nhau trên fixture CHUNG của GHIM-B1A:** đọc `ops/specs/wp1460-r1/hop_dong/fixture.json` và schema tại chỗ (test tự kiểm sha256 cả hai bằng băm ghim; lệch ⇒ ca ĐỎ, không bỏ qua); với MỖI ca trong `ca[]`, dựng tài liệu đúng `huong_dan` của fixture; kết quả kiểm hình của B2 bằng `hinh_hop_le`; với ca không thuộc nền `dau_job`, `tieu_dung` của B2 trả đúng `vi_pham` (bằng `["C1"]` khi `hinh_hop_le` là `false`; so như tập), `canh_bao`, `moc_tuoi` khi ca khai. Dòng dương bắt buộc: `HOP_DONG_B1A: hinh 120/120 · ngu nghia 118/118 · ghim 3/3`, trong đó `ghim 3/3` là sha256 của schema, fixture và khối mã trích từ tệp đặc tả B1a khi tệp ấy có trong cây (vắng tệp đặc tả B1a ⇒ dòng ghi `ghim 2/2 · khoi_ma khong_co_trong_cay` và ca vẫn ĐỎ nếu đang ở kho thật có `.git` mà hai tệp `hop_dong/` vắng).
4. **Trạng thái tổng S1–S7, mỗi dòng ít nhất một ca, cộng biên:** S2 (khung F `dat`); S3 (F có lượt completed `khong_dat`, kể cả khi một lượt khác của F còn `dang_chay`); S4; S5 tại T = F + 12 h (⇒ còn trong hạn, đi tiếp S7) và T = F + 12 h + 1 s (⇒ `khung_vang`); S6 tại T = P + 8 ngày (⇒ S7) và + 1 s (⇒ `qua_tuoi_8_ngay`) với F `dang_chay`; S7 ba nhánh (P `dat`, P `khong_do_duoc`, P `vang`/`do`); S1 với D1 không trọn MÀ phần đã thấy có lượt `dat` cho F (⇒ `khong_do_duoc`, không `fresh`); T = F đúng mốc (F là khung hiện hành). Mỗi ca có nhiều lượt chạy ở HAI thứ tự API và một lần với hai lượt ở HAI TRANG, đòi cùng S, cùng mã, cùng `sha_audit`.
5. **Chạy lại không làm mới:** (a) lượt `schedule` của khung P chạy lại attempt 2 hôm nay (`created_at` giữ ở P + 3 h, `run_attempt` 2, biên nhận attempt 2 hợp lệ), T = F + 13 h, F vắng ⇒ `stale_or_missing` `khung_vang`, không `fresh`; (b) lượt `workflow_dispatch` xanh trên SHA cũ tạo lúc T ⇒ không phải ứng viên (D1 lọc `event=schedule`; nếu transport giả vẫn trả nó trong D1 ⇒ `danh_sach_la`, `khong_do_duoc`); (c) biên nhận của attempt thấp hơn không được dùng khi attempt cao nhất thiếu biên nhận (⇒ `bien_nhan_vang`, lượt `khong_dat`); (d) bất biến: mọi lượt `dat` có `moc_tuoi` = khung REST.
6. **Đầu vào độc lập:** biên nhận tự khai `su_kien.sha`, `job_ky_vong`-tương-ứng và `tree` khác REST ⇒ `khong_dat` (C3/C4/C5) — B2 không lấy đầu vào `ngoai` từ biên nhận; D6 trả workflow có thêm một job ⇒ `luat_C:C4…` dù biên nhận tự nhất quán; D7 tree khác ⇒ `luat_C:C5`.
7. **Báo cáo và câu master:** `sha_master` = `sha_audit` ⇒ đúng câu thứ nhất; khác ⇒ câu thứ hai với `ahead_by` của D9; D9 lỗi ⇒ câu thứ hai với `khong_do_duoc`, S KHÔNG đổi; D8 lỗi ⇒ câu thứ ba, S không đổi. Âm: khi hai SHA khác, mọi văn bản sinh ra (báo cáo, thân, comment) không chứa câu thứ nhất. `C10` của biên nhận `not_measured` có mặt nguyên văn trong báo cáo và S vẫn `fresh`.
8. **Nhịp tim và Issue:** thân đúng hai dòng ASCII đóng băng; đọc nhịp tim: 0 dòng ⇒ `vang`; 2 dòng ⇒ `nhip_tim_trung`; JSON hỏng; thừa/thiếu khoá; `luc` tương lai; đúng 24 h ⇒ `moi`, 24 h + 1 s ⇒ `cu`. Luật comment (a)/(b)/(c) mỗi vế hai chiều: lặp cùng bộ ⇒ 0 POST; đổi `ma_ly_do` ⇒ 1 POST; hồi phục ⇒ 1 POST; `fresh` liên tiếp với nhịp tim `moi` ⇒ 0 POST. Đọc lại: thân trả về khác một ký tự ⇒ mã 3; `state` khác `open` ⇒ mã 3; D11 403 ⇒ mã 3 và vẫn thử D12 khi luật đòi; comment đọc lại khác ⇒ mã 3; mọi lỗi ghi khi S `fresh` vẫn mã 3 (job đỏ). Đọc nhật ký transport: mỗi lượt đúng 1 PATCH và 0 hoặc 1 POST.
9. **Mã thoát và cấu hình (mục 9):** bốn mã, mỗi mã một ca; `ISSUE_THEO_DOI` `None`/0/âm, `B2_RUN_ID` không phải số, `GH_TOKEN` rỗng ⇒ mã 2 với 0 lời gọi transport. I3: đặt `GITHUB_API_URL`, `GITHUB_REPOSITORY`, `GH_REPO`, `B2_ISSUE` khác đi ⇒ URL trong nhật ký không đổi.
10. **Hình workflow (mục 8), danh sách cho phép:** ca âm cho từng điểm: thêm trigger; `workflow_dispatch` có `inputs`; cron khác; thêm/bớt/đổi một quyền; `permissions` mức job; bỏ `concurrency` hay `cancel-in-progress: true`; `continue-on-error`; `if` ở job; thêm bước; đổi thứ tự bước; bỏ `persist-credentials: false`; thêm biến `env`; biểu thức Actions trong thân `run` (kể cả trong chú thích); đổi phiên bản ghim. Ca dương: tệp thật tại H đạt. Kèm ca I7: tệp workflow, script, test và mọi văn bản sinh ra không chứa dấu bỏ-qua-CI ở mọi biến thể GitHub công nhận (test dựng mẫu từ các mảnh chữ, không viết nguyên văn).
11. **Đột biến riêng cho từng chốt** (bảng dưới): chạy trên BẢN SAO tạm, tên tệp riêng mỗi đột biến, `-B` + `sys.dont_write_bytecode`; phân hạng bằng LỚP NGOẠI LỆ RIÊNG `TinHieuChotCa` (lớp con của `AssertionError` do bộ test định nghĩa, mang TÊN CA) — đột biến chỉ GIẾT khi ca đích ném đúng lớp ấy với đúng tên ca; chết vì lỗi khác hoặc vì ca khác ⇒ TÍN DỤNG GIẢ, kể cả khi ngoại lệ đi qua một `except` đổi kiểu. Kèm bốn ca tự kiểm bộ phân hạng (giết thật; `AttributeError` qua `except` đổi kiểu ⇒ tín dụng giả; assertion của ca khác ⇒ tín dụng giả; sống ⇒ sống). Ca đích CÔ LẬP: trên mã không đột biến, chỉ chốt đang thử quyết định điều ca ấy đòi. Báo `giet that n/n · tin dung gia 0 · song 0`; đòi n/n.
12. **Cổng kho:** `python ops/canh_tuoi_audit_test.py` in đúng bốn dòng cuối `CA: <n>/<n> dat` · `DOT BIEN: <m>/<m> bi giet dung ly do` · `TU KIEM PHAN HANG: DAT (<k> dot bien)` · `TONG: DAT` (khớp mẫu đăng ký ở mục 9 Write set); `python .claude/dev/ci_dang_ky_test.py` đạt (bộ mới có trong sổ; sổ không có mục thừa); `actionlint` theo mục 8; Ruff `--select F` DELTA = 0 so B trên mọi `.py` đổi hoặc thêm; `python .claude/dev/packet_loop.py doctrine-scan --root .` và `adr-song --root .` rc 0; `git diff --numstat B <H>` đo trước MỖI lần đẩy và MỖI lần xin review (mục "Kích thước"); tập tệp đổi so B ⊆ write set; diff của `ci_dang_ky_test.py` so B chỉ là đúng một mục `MOI`.
13. **CI và M9 (`ADR-0060` M9):** diff chạm `.claude/dev/**`, `ops/**/*.py`, `.github/workflows/**` ⇒ một lượt `ci-dot-bien-du.yml` `success` trên đúng H (K7) là điều kiện merge; CI PR Ubuntu xanh trên H; PR ghi delta thời gian của `gate-registry` do bộ test mới.
14. **Sau merge (M8, không chặn merge; trạng thái `chua_do` cho tới khi đo thật):** (a) lượt `schedule` đầu tiên của `canh-tuoi-audit.yml` trên `master` có `conclusion` đúng theo S của nó, thân Issue đọc lại khớp luật đọc nhịp tim mục 7 (đọc bằng REST, không bằng công cụ đọc có chuẩn hoá HTML); (b) lượt watchdog đầu tiên SAU lượt `schedule` đầu tiên của `ci-dot-bien-du.yml` có biên nhận B1a cho trạng thái khớp phán quyết tay của điều phối trên cùng đầu vào; (c) chủ kho xác nhận đã nhận một comment của watchdog (điều kiện bật, mục 10). Điều phối đo và ghi ở hồ sơ land.

## Bảng đột biến (mỗi dòng MỘT đột biến; ca đích nêu tên trong bảng đột biến của bộ test)
| # | Đột biến | Ca đích (nghiệm thu) |
|---|---|---|
| 1 | gán khung theo `moc_tuoi`/`su_kien` của biên nhận thay cho `created_at` REST | 5 (a) |
| 2 | nhận lượt `workflow_dispatch` làm ứng viên | 5 (b) |
| 3 | dùng biên nhận attempt thấp hơn khi attempt cao nhất vắng | 5 (c) |
| 4 | bỏ S1 cho danh sách không trọn (dùng phần đã thấy) | 4 (S1) |
| 5 | đảo thứ tự S2/S3 (lượt đỏ của F thắng lượt `dat`) | 4 (S2 có lượt đỏ kèm) |
| 6 | gộp khung: `khong_do_duoc` thắng `do` | 4 (S3 kèm lượt `khong_do_duoc`) |
| 7 | `TRE_LICH_TOI_DA` so `>=` thay `>` | 4 (S5 biên) |
| 8 | bỏ S5 | 4 (S5 +1 s) |
| 9 | `TUOI_TOI_DA` so `>=` thay `>` | 4 (S6 biên) |
| 10 | bỏ S6 | 4 (S6 +1 s) |
| 11 | S7: P `khong_do_duoc` ⇒ `due_in_progress` | 4 (S7 nhánh 2) |
| 12 | S7: P `vang` ⇒ `due_in_progress` | 4 (S7 nhánh 3) |
| 13 | không xếp `rest.jobs` theo `id` | 4 (hai thứ tự, bản ghi trùng tên-attempt) |
| 14 | `sha_audit` lấy lượt `dat` gặp đầu tiên thay vì `id` nhỏ nhất | 4 (hai trang) |
| 15 | U2: khử trùng `id` rồi đi tiếp | 1 (trùng `id`) |
| 16 | U1: bỏ so `total_count` | 1 (`total_count` lệch) |
| 17 | U6: bỏ đọc D2 cuối | 1 (T7) |
| 18 | `ngoai.h`/`tree_h`/`job_ky_vong` lấy từ biên nhận | 6 |
| 19 | T3: bỏ từ chối khoá trùng | 1 (T3 `job_ky_vong_trung_khoa`) |
| 20 | T4: bỏ so băm schema | 1 (T4 `hop_dong_lech_ghim`) |
| 21 | T2: bỏ so digest gói | 1 (T2 digest) |
| 22 | gửi `Authorization` tới host lưu trữ | 1 (lớp S) |
| 23 | lớp J: nhận 2xx không dấu GitHub | 1 (200 không dấu) |
| 24 | biên ngoại lệ: chỉ bắt `ValueError` ở ĐỌC-JSON | 2 |
| 25 | biên ngoại lệ: bắt `BaseException` ở transport | 2 (`KeyboardInterrupt`) |
| 26 | gỡ lưới an toàn pha đánh giá | 2 (lưới an toàn) |
| 27 | `C10` đổi phán quyết thành `khong_dat` | 7 (`not_measured` vẫn `fresh`) |
| 28 | câu master thứ nhất khi hai SHA khác | 7 |
| 29 | D9 lỗi đổi S | 7 |
| 30 | nhịp tim: bỏ từ chối `luc` tương lai | 8 |
| 31 | nhịp tim: `cu` so `>=` 24 h | 8 (biên 24 h) |
| 32 | nhịp tim: hai dòng ⇒ lấy dòng đầu | 8 |
| 33 | luật comment: bỏ vế chống lặp (a) | 8 (lặp cùng bộ ⇒ 0 POST) |
| 34 | luật comment: bỏ vế hồi phục (b) | 8 (hồi phục) |
| 35 | luật comment: bỏ vế (c) | 8 (nhịp tim `cu`) |
| 36 | bỏ đọc lại thân Issue | 8 (thân khác một ký tự ⇒ 3) |
| 37 | bỏ kiểm `state == "open"` | 8 |
| 38 | bỏ đọc lại comment | 8 |
| 39 | lỗi ghi khi S `fresh` trả 0 | 8 |
| 40 | `GH_TOKEN` rỗng vẫn gọi mạng | 9 |
| 41 | đọc số Issue từ biến môi trường | 9 (I3) |
| 42 | mỗi điểm của danh sách cho phép mục 8 (×N, N = số điểm ca âm của nghiệm thu 10, đếm ĐIỂM) | 10 |

**Đột biến TƯƠNG ĐƯƠNG đã khai (không tính vào mẫu số, không được đòi giết):** (i) một hằng 36 h đứng sau S6 — không tồn tại trong mã theo mục 2; nếu executor thêm nó, mọi đột biến của nó là tương đương vì S6 chặn trước (chứng minh: với cron 7 ngày, P + 8 ngày = F + 24 h < F + 36 h); (ii) đổi thứ tự duyệt các lượt trong gộp khung (gộp giao hoán). Executor khai thêm đột biến tương đương khác thì phải kèm chứng minh như trên trong PR, và reviewer kiểm.

## Write set
Nhánh điều phối `ops/wp1494-r1` (không thuộc PR giao nộp): `ops/specs/wp1494-r1/SPEC.md`; `ops/leases/wp1494-r<revision được cài>-g<n>-claude-<YYYYMMDD>.yaml` (do ĐIỀU PHỐI cấp).

PR giao nộp (nhánh thi công riêng), đúng BỐN tệp:
1. `.github/workflows/canh-tuoi-audit.yml` (MỚI) — mục 8.
2. `ops/canh_tuoi_audit.py` (MỚI) — mục 2–7, 9; chép nguyên văn `tieu_dung`, `khoa_tu_ten`, `doc_moc`, `khung_cron` từ khối mã GHIM-B1A (kèm chú thích trỏ GHIM-B1A); không import gì từ `ops/specs/`.
3. `ops/canh_tuoi_audit_test.py` (MỚI) — nghiệm thu 1–11; bốn dòng cuối như nghiệm thu 12.
4. `.claude/dev/ci_dang_ky_test.py` — CHỈ thêm vào `MOI` đúng mục `"ops/canh_tuoi_audit_test.py": r"(?ms)\A(?!.*^(?:TONG|TU KIEM PHAN HANG): DO\b).*^CA: ([1-9]\d*)/(\1) dat\nDOT BIEN: ([1-9]\d*)/\3 bi giet dung ly do\nTU KIEM PHAN HANG: DAT \(\d+ dot bien\)\nTONG: DAT\n?\Z",` (cùng mẫu đang dùng cho `ops/ci_provenance_test.py`, đo tại `e2f28fb` dòng 58).

Không tệp thứ năm. Không thuộc write set: `.github/workflows/ci-dot-bien-du.yml`, `.github/workflows/ci.yml`, `ops/ci_provenance.py`, `ops/specs/wp1460-r1/**`, `.claude/dev/packet_loop.py`, `CLAUDE.md`, `docs/**`, `scripts/**`, `RELEASE_MANIFEST.json`, `VERSION`. `ops/` không vào gói phát hành nên không đụng manifest hay trần 200 tệp. Cần sửa một tệp ngoài danh sách ⇒ DỪNG, báo điều phối.

## Ngoài phạm vi
Chặn merge hay release dựa trên S; nối nhịp tim vào B3 (packet sau, đọc theo luật mục 7); điền `KENH_GIAO_TIN_XAC_NHAN`; tạo Issue theo dõi (việc của điều phối trước lease); B1a, B1b (A+3, chẩn đoán, kiểm kê mục), B3, B4, PR2; A4 và `ops-do-workflow-definition.yml`; mọi thay đổi `ci-dot-bien-du.yml` (trigger, cron, concurrency); sửa `doctor`; công tắc A+1; làn C; LIVE; Windows CI.

## Baseline nghiệm thu
- **B không nằm trong tệp này** vì nó chỉ tồn tại sau khi B1a land. Mission revision cài đặc tả và lease của B2 cùng ghi MỘT OID B (40 hex); hai nơi lệch ⇒ không thi công.
- **Điều kiện của B, executor và reviewer tự đo trước khi dùng (sai một điều ⇒ DỪNG):** (1) B trên chuỗi first-parent của `origin/master` vừa fetch, kho không shallow; (2) B là commit merge PR giao nộp của B1a hoặc một commit first-parent sau nó: tại B có hai tệp `ops/specs/wp1460-r1/hop_dong/` với sha256 bằng GHIM-B1A; `.github/workflows/ci-dot-bien-du.yml` tại B có job `bien-nhan-audit` với bước tải lên mang `name: bien-nhan-audit-${{ github.run_id }}-${{ github.run_attempt }}` và tải đúng tệp `bien_nhan_audit.json`; luật T3 áp lên tệp ấy cho danh sách tên không trùng tên, không trùng khoá; (3) tại B, `.claude/dev/ci_dang_ky_test.py` chưa có mục `ops/canh_tuoi_audit_test.py` và không tồn tại `.github/workflows/canh-tuoi-audit.yml`, `ops/canh_tuoi_audit.py`.
- Mọi phép đo của packet tính từ B: numstat, tập tệp đổi, Ruff delta, actionlint delta, mọi vế "base" của A/B. Cập nhật nhánh thi công lên master mới hơn KHÔNG dời B; dời B cần Mission revision mới.

## Kích thước
- Trần là trần MẶC ĐỊNH của lớp `sensitive` theo `ADR-0053`: **≤ 6 tệp và ≤ 450 dòng thêm** theo `git diff --numstat B <H>`. Lease cấp theo trần ấy. Đặc tả này không xin, không ước lượng và không cấp ngoại lệ (Mission r86 luật kích thước; Mission r96 `size_rule`).
- **Số đo của phạm vi tương đương gần nhất (không phải ước lượng của packet này; soan-spec §3):** tại `e2f28fb`, `ops/ci_provenance.py` 653 dòng và `ops/ci_provenance_test.py` 2 330 dòng (một bộ đọc REST/artifact cùng họ có bộ đột biến); `.github/workflows/ops-do-workflow-definition.yml` 49 dòng. PR giao nộp có 4 tệp, trong trần tệp; với số đo ấy, khả năng vượt trần dòng là thật, nên điểm dừng dưới đây là bước dự kiến của quy trình, không phải sự cố.
- **Đo và dừng.** Trước MỖI lần đẩy H và MỖI lần xin review, audit hay CI, executor đo `git diff --numstat B <H>` (số tệp, dòng thêm, từng tệp) trên H đã commit và ghi biên nhận kích thước (SHA, tree của H; SHA của B; numstat từng tệp) ở NGOÀI H: handoff (protocol §7) và một comment trên Issue #1494. Vượt trần đang ghi ở lease ⇒ KHÔNG đẩy, KHÔNG xin review/audit/CI; không cắt ca, đột biến hay luật để lọt trần, không tách PR; nộp biên nhận kèm danh sách việc còn thiếu (theo `ADR-0044`: dừng TRƯỚC review).
- Khi ấy điều phối xin chủ kho [E2] một khối `nang_tran` đúng `ADR-0053` (`ai_nang`, `can_cu` có numstat ĐÃ ĐO và hai SHA, `tran_cu`, `tran_moi`); chủ kho duyệt; khối vào một revision đặc tả (chỉ đổi dòng `revision`, đoạn Trạng thái, mục này, bảng Thay đổi), vào Mission revision, và chép nguyên vào lease. Revision ấy tính vào bộ đếm lượt soạn spec của Mission (`spec_author_calls` 5; r1 là lượt 1). Executor chỉ đẩy/xin review sau khi lease mang khối ấy. Sau đó cùng luật với `tran_moi`.
- Không cổng máy nào canh trần này; executor, người cấp lease và reviewer đo bằng tay.

## Quy trình và quyền
- **Điều kiện cấp lease:** (1) chủ kho duyệt băm đặc tả này (điều kiện của Mission r96 vai B2); (2) bản B1a được duyệt và tương thích theo GHIM-B1A, và PR giao nộp B1a ĐÃ LAND (B2 cần hai tệp `hop_dong/` và job `bien-nhan-audit` tại B; thứ tự §7 kế hoạch: B1 → B2); (3) lease `wp1236-a-r12-g1-claude-20261121` (giữ `.claude/dev/ci_dang_ky_test.py` tới `2026-11-23T13:45Z`, theo Mission r96) đã hết hạn hoặc thu hồi hai chiều, VÀ lease B1a trên cùng tệp đã nhả (B1a, B2, PR2 dùng chung tệp ấy nên xếp NỐI TIẾP); không lease sống nào chồng write set — `ai-dang-giu` trên MỌI ref sau khi so TẬP TÊN ref cục bộ với `ls-remote` (không so số đếm); (4) Issue theo dõi đã được điều phối tạo, số của nó ghi ở Mission revision và lease (mục 7); (5) Mission revision riêng cài đặc tả, ghi OID B và số Issue; (6) số writer executor đang chạy < 2 (Mission r96 `r96_constraints`).
- **Vai:** executor Claude Code (model do điều phối chọn theo chính sách Mission). Reviewer Codex service, mức suy luận cao nhất, phiên độc lập, chỉ đọc; reviewer CHẠY ca và đột biến có sẵn trong cây và có bản sao kho đủ để đo lại mọi con số (protocol §8); hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời cho điều phối.
- **Trần (Mission r96 `per_new_packet`):** soạn spec 5 (r1 là lượt 1) · review spec Codex 6 (chưa dùng) · executor attempts 3 · review mã Codex 3 · CI PR Ubuntu 3 · `full_m9_runs` 1 (K7, nghiệm thu 13) · connector 2 · CI rerun 1 · Windows CI 0 · Windows local: Mission chỉ cấp cho B3. Số đã dùng là thông báo của điều phối, không phải số tác giả tự đo.
- **Trần lời gọi Codex trên PR giao nộp:** dòng khai `ADR-0055` đặt trần PACKET mười lời gọi mỗi PR, đếm CHUNG review mã qua service VÀ connector, kể cả lời gọi bị cắt sau khi đã sinh output. Trần Mission hẹp hơn và là trần dùng được: review mã 3 + connector 2 = 5 ≤ 10; trần chạm trước thắng. Mọi lượt sau lượt đầu theo điều kiện của `ADR-0052`. **Review ĐẶC TẢ là bộ đếm khác** (Mission `codex_spec_review_calls`), không tính vào mười lời gọi này và không được đặt lại khi đặc tả đổi revision. Trước MỖI lời gọi Codex: đếm số đã dùng, đọc trần trong lease và dòng khai.
- **Windows (`ADR-0060` M3):** diff chạm `.claude/dev/**` và `.github/workflows/**` ⇒ phân loại `required`. Mission không cấp lượt Windows local cho B2. Vế này chỉ đạt khi có MỘT trong hai: một dòng của chủ kho `windows: <H> mien` neo đúng H cuối (như PR1; một câu trong đặc tả không phải miễn trừ), hoặc một lượt Windows local được chủ kho cấp [E2]. Đặc tả không tự miễn.
- **`ADR-0060` khác:** M1 (0 P0–P2 mở; P3 đóng có bằng chứng hoặc chủ kho miễn neo SHA); M5 đẩy một lần chính sau review offline approve và gate trước push đạt trên đúng SHA; M6 PR mở draft, cấm nói "sẵn sàng merge" khi chưa đủ điều kiện; M8 sổ sách.
- **Trong lúc thi công và test:** KHÔNG ghi Issue thật, KHÔNG dispatch workflow, KHÔNG đổi biến/secret/bảo vệ nhánh, KHÔNG LIVE. Mọi lời gọi GitHub trong test đi qua transport giả.
- Audit exact-H và merge theo `ADR-0060`/`ADR-0067` cho packet không chạm E4/E5 (mục `pham_vi_e`), cộng điều kiện chặt hơn của Mission nếu Mission revision cài đặc tả ghi thêm.
- **Hoàn tác:** revert PR giao nộp; Issue theo dõi giữ làm lịch sử (đóng tay nếu cần).

## luat_dung
- Điểm dừng của protocol và ADR, dẫn bằng tên, không chép, không hạ ngưỡng: `docs/PROTOCOL_DA_PHIEN.md` §12 (stop conditions và budget); `ADR-0044` (ứng viên vượt trần ⇒ dừng trước review); `ADR-0060` M1 (điều kiện dừng theo P3), M3 (Windows), M5 (số lần push); trần lời gọi của `ADR-0055`/`ADR-0052`; mục "Baseline nghiệm thu" và luật tương thích GHIM-B1A (một băm lệch ⇒ dừng).
- **[E2]** chạm trần kích thước (mang: numstat đã đo, hai SHA, phần việc còn thiếu); chạm trần lời gọi Codex, CI, attempts hay `full_m9_runs` (mang: mức đã dùng, còn thiếu bao nhiêu, để làm gì); Windows `required` mà không có lượt hay dòng miễn (mang: H, lý do `required`).
- **[E1]** một hình dạng lỗi lặp lại sau khi đã đổi thiết kế (mang: gốc rễ, phương án đã thử, đề xuất).
- **[E3]** bằng chứng cho thấy một quyết định chủ kho đã ghi (Q6, quyết định [E1+E2] 2026-11-21 về chính sách ngoại lệ) gây hại đo được cho B2.
- Không có ngân sách mềm nào dưới các trần trên.

## pham_vi_e
- **E4: không chạm.** Packet không đẩy Package, không deploy GAS, không `--apply`, không xoá ref/tag, không đọc hay ghi secret (token là `github.token` tự cấp của lượt chạy), không đổi ruleset. Ghi Issue/comment là thao tác trong kho, hoàn tác được (sửa/xoá), và chỉ xảy ra sau merge do workflow tự chạy.
- **E5: không chạm.** Không sửa danh sách E, `NGUOI_CO_THAM_QUYEN`, cổng cấp lease hay cổng merge; B2 chỉ báo cáo, không quyết định merge/release.
- Không đảo quyết định nào của chủ kho (Q6 được thực hiện; chính sách ngoại lệ [E1+E2] 2026-11-21 được áp nguyên).

## hinh_dang_ke_thua
`khong_ap_dung` theo nghĩa L4 (B2 không phải packet khắc phục). Kế thừa CHỦ ĐỘNG các lớp đã tốn nhiều lượt ở B1a/B3 (đếm theo biên nhận đặc tả của chúng): `b1-consumer-contract-mismatch` và `a4-provenance-contract-incomplete` của B3 (lượt 5–8; đổi sang luật "mọi `Exception`" ở biên — áp ngay ở mục 3); `consumer-records-not-bound-to-producers` và `consumer-freshness-anchor-unverified` của B1a (đầu vào `ngoai` độc lập — mục 4 T3; mốc tuổi REST — mục 2); thứ tự tại biên `tieu_dung` (B3 SPEC-17, U7 — mục 3); danh sách cấm ⇒ danh sách cho phép (mục 8, nghiệm thu 10).

## Runbook điều phối (dev-side; kiểm bằng TAY ở đầu mỗi phiên điều phối Mission #1172 sau khi B2 land)
1. Đọc thân Issue theo dõi bằng REST (`GET /repos/ducthangho/tra-luat/issues/<ISSUE_THEO_DOI>`; đừng dùng công cụ đọc có chuẩn hoá HTML để so byte). Áp luật đọc nhịp tim mục 7 với T = giờ hiện tại.
2. `cu`, `vang` hay `khong_doc_duoc` ⇒ liệt kê lượt `canh-tuoi-audit.yml` gần nhất (REST), ghi vào bản tin hằng ngày; nếu lịch không chạy quá 24 h, dispatch tay một lượt (cùng mã, cùng hằng) và ghi lại lý do.
3. `trang_thai` ∈ {`stale_or_missing`, `khong_do_duoc`} ⇒ đọc báo cáo của lượt ấy; ghi vào bản tin; quy trình audit đỏ là của B3 (`docs/QUY_TRINH_PHAT_HANH_B3.md` khi có).
4. Lần chạy đầu sau khi B1a land có thể báo `khung_truoc_khong_xanh` (mục 5) — đúng luật, không phải lỗi.
5. Comment đầu tiên của watchdog là lần thử giao tin thật: hỏi chủ kho xác nhận đã nhận (điều kiện bật, mục 10) và ghi URL xác nhận vào hồ sơ land.

## Số đo lúc soạn (2026-11-21, `master` `e2f28fb`)
- Blob tại `e2f28fb`: `.github/workflows/ci-dot-bien-du.yml` `613da84955ac6759b192812361ef3bc667860a1d` (145 dòng; ba job, chưa có job `bien-nhan-audit`: B1a chưa land, `git cat-file -e e2f28fb:ops/specs/wp1460-r1/hop_dong/fixture.json` rc 128); `ops/ci_provenance.py` `086f416921c3df1b2e81d95f509e04c6a9d573ae` (653 dòng; B2 không dùng, không sửa); `.claude/dev/ci_dang_ky_test.py` `7b120b5fcce03c46b5dc22448251b4e65dcc198c` (2 992 dòng; `kiem()` đòi mọi `*_test.py` có trong `MOI` hoặc `DA_NOI`).
- REST (MCP `list_workflow_runs`, `ci-dot-bien-du.yml`, `event=schedule`, đọc 2026-11-21 ~17:0xZ): `total_count` 7, cả 7 `success`, `head_branch` `master`, `run_attempt` 1. Độ trễ `created_at` − mốc cron (thứ Bảy 19:17Z): 10-03 2 h 51 m; 10-10 3 h 16 m; 10-17 2 h 11 m; 10-24 2 h 20 m; 10-31 3 h 12 m; 11-07 3 h 28 m; 11-14 3 h 41 m. Không khung nào vắng trong 7 tuần ấy. Thời lượng `updated_at` − `created_at`: 18 … 35 phút.
- GHIM-B1A: ba băm và lệnh kiểm như đoạn GHIM-B1A ở đầu tệp.
- ADR: ba phép đo cho ba OID như đoạn "Ba dòng khai ADR".

## chua_do_duoc
- Lease `wp1236-a-r12-g1-claude-20261121` và hạn `2026-11-23T13:45Z`: lấy từ Mission r96 và chỉ thị điều phối; lượt soạn KHÔNG chạy `ai-dang-giu` trên mọi ref.
- Hành vi thật của GitHub: header `X-GitHub-Request-Id` và lời chuyển hướng 302 của D5 với `github.token`; `body` trả về của PATCH/GET Issue có giữ nguyên từng ký tự không (thân được chọn ASCII để giảm rủi ro); GitHub có tắt lịch của kho này khi không hoạt động không; độ trễ lịch của chính watchdog; định tuyến thông báo comment tới chủ kho. Tất cả đo ở nghiệm thu 14 sau merge.
- `actionlint`/`shellcheck` nền tại B; Ruff nền tại B (B chưa tồn tại).
- Biên nhận B1a thật (chưa có lượt nào: B1a chưa land); `tieu_dung` của B2 chỉ đo được trên fixture tới khi có.
- Tác giả không chạy `--dot-bien` của khối mã GHIM-B1A.

## Sổ quyết định uỷ quyền của người soạn (L7; Mission đã duyệt hướng, không mã E)
1. Chỉ lượt `schedule` làm tươi (chỗ lệch 3). 2. `TRE_LICH_TOI_DA` = 12 h từ số đo 7 lượt (chỗ lệch 4). 3. Ân hạn hiệu dụng 24 h, không hằng 36 h (chỗ lệch 1). 4. Issue số cố định do điều phối tạo; nhịp tim ở thân, cảnh báo ở comment (chỗ lệch 5, 6). 5. `contents: read` thêm vào quyền (chỗ lệch 7). 6. Luật "mọi `Exception`" ở biên và lưới an toàn pha đánh giá (mục 3), theo hướng quyết định chủ kho [E1+E2] cho B3. 7. Runbook trong đặc tả (chỗ lệch 8). 8. Dòng khai `ADR-0060` (theo tiền lệ PR1 cùng Mission).

## Thay đổi
r1: bản đầu.
