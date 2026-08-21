# ĐÍNH CHÍNH — `review_class` của `PLAT-M4` (#194 / PR "#204")

**Loại:** append-only. **KHÔNG tệp spec hay lease nào bị sửa.** Lý do ở §5 — đó là phần
quan trọng nhất của tệp này, đừng bỏ qua nó.

**Quyết định của người giữ kho, 21-08-2026:**
> "Sửa `review_class` thành `sensitive`, ghi rõ lý do."

**`review_class` đúng của `PLAT-M4` là `sensitive`.** Lời khai `systemic` là SAI.

## 1. Sự việc — đo được

| tệp | dòng | giá trị |
|---|---|---|
| `ops/specs/plat-m4-v0.md` | 11 | `review_class` = **`systemic`** — *"chạm `.claude/dev/**`, KHÔNG chạm `.github/workflows/**` và KHÔNG chạm cổng đăng lease"* |
| `ops/leases/plat-m4-exec-2-claude-20260821.yaml` | 21 | `review_class: systemic` |
| `ops/leases/plat-m4-review-2-codex-20260821.yaml` | 19 | `review_class: systemic` |
| `docs/PROTOCOL_DA_PHIEN.md` | 572 | `sensitive` gồm *"workflow/CI authority, **security/credential boundary**, dispatcher/reconciler, review/land authority, **launcher** hoặc gate lifecycle, migration dữ liệu và LIVE adapter"* |

Packet sửa `.claude/dev/launcher.py`, và nội dung bản vá là **xử lý credential trong URL**.
Nó khớp `sensitive` theo **HAI mệnh đề độc lập**: `launcher`, và `security/credential boundary`.

## 2. Lỗi nằm ở HÌNH DẠNG của lời khai, không ở một chữ gõ nhầm

Lý do ghi trong spec phân loại theo **thứ packet KHÔNG đụng** (`.github/workflows/**`, cổng
đăng lease) trong khi danh sách `sensitive` gọi **đích danh** thứ nó CÓ đụng. Đây là
**phân loại theo VỊ TRÍ thay vì theo HẬU QUẢ** — cùng hình dạng với bốn lần kho đã trả giá
cho "đếm sự CÓ MẶT thay vì KHẢ NĂNG" (`which(gh)` · `rest-chung` · `gh auth status` ·
`shutil.which` trong `DUNG_DUOC`). Lần này đối tượng đổi, hình dạng thì không.

Và `docs/PROTOCOL_DA_PHIEN.md:567` nói thẳng: **"Executor không được hạ lớp."** Người khai
`systemic` chính là phiên executor.

## 3. Vì sao KHÔNG ai bắt được — đây mới là nợ thật

§8 giao việc tính `effective_review_class` **fail-closed** cho *dispatcher*. Kho **không có
dispatcher**. Đo được:

| phép đo | kết quả |
|---|---|
| lease khai `effective_review_class` | **0/41** |
| tệp mã chạm trường ấy | **1** — `ops/chatgpt_review/build_bundle.py:165` |
| việc tệp ấy làm | `effective_review_class = review_class or spec_meta["review_class"]` rồi kiểm nó có thuộc ba chuỗi hợp lệ không |

Tức nó **CHÉP LẠI giá trị đã khai**, không suy từ write set. Chốt fail-closed mà §8 quy định
**không tồn tại**. Đây là lý do gốc, và nó **vẫn còn**: ca tiếp theo sẽ lọt y hệt.

## 4. Hệ quả — cả hai đều thật, và cả hai đã xảy ra

1. **`same_provider_approved` không dùng được.** §8:544 và §8:572: *"`same_provider_approved`
   vẫn không thay `cross_approved` cho class `sensitive`"* · *"Phải có Codex `cross_approved`
   hoặc `human_audited`; hết quota mà chưa có human thì pause."* Vì tin vào lời khai
   `systemic`, phiên chính đã soạn `ops/uy-quyen-194-same-provider-20260821.yaml` và trình
   nó với người giữ kho **như một lần hạ mức TRONG thang** — trong khi thực tế nó sẽ là
   **override chính §8**. Uỷ quyền ấy nay **không đủ**, và cũng đã tự vô hiệu theo §9 khi
   head đổi sang `a9e021d`.
2. **Packet vượt trần kích thước.** ADR-0044 cho `sensitive` trần **≤3 tệp / ≤300 dòng thêm**;
   đo tại `825e970` là **2 tệp / +473**. Tình tiết có thật: ADR-0044 land SAU khi packet bắt
   đầu, và nó trích **chính PLAT-M4** (`+351/−25`) làm ví dụ cho ngưỡng — packet đã vượt qua
   chính con số từng làm ví dụ cho nó.

## 5. Vì sao KHÔNG sửa thẳng vào `ops/specs/plat-m4-v0.md`

Người giữ kho nói "sửa"; tệp này thực hiện đúng ý ấy nhưng **không mutate đặc tả đã đóng
băng**, và lý do là một phép đo chứ không phải sự thận trọng chung chung.

`ops/specs/plat-m4-v0.md` có sha256 `63ff22bcc2427850ddd66322ed4a5ac5dcaa03f8d242cc857d12825b601953d1`,
và **bốn lease đang neo băm ấy** qua trường `spec_sha256`. Sửa một byte trong tệp là đổi băm ⇒
bốn lease trỏ vào một con băm mà **không tệp nào ứng với**. Đó chính xác là bệnh đã làm `wp55`
đứng im hai ngày (`prompt_sha256_required: 46a833cc…` không kèm địa chỉ tra được), và cũng
chính là bệnh phiên này đã phải chữa **hai lần trong hôm nay** — một lần ở lease `3r3`, một lần
ở mục 11 của bản thẩm định tri thức. Cổng chưa cưỡng chế `spec_sha256` (đo được: 0 lần xuất
hiện trong `ops/lease_publish.py`) — nhưng "cổng chưa bắt" không phải lý do để làm hỏng.

**Cách đọc đúng từ nay:** `ops/specs/plat-m4-v0.md:11` là **bản ghi LỊCH SỬ** của một lời khai
sai; tệp này là bản có hiệu lực. Ai đọc spec mà không đọc tệp này sẽ tin nhầm — nên nó được
trỏ tới từ `verdict_usage_caveats` (id `packet-bi-phan-class-SAI`) trong
`ops/reviews/plat-m4-review-3-claude-verdict.receipt.yaml`, và từ bảng cảnh báo của
`ops/reviews/README.md`. Đó là ba chỗ; **không** chỗ nào trong số đó là MÁY, và phải nói thẳng
như vậy.

## 6. Đính chính này KHÔNG hồi tố hiệu lực cho hai lượt review đã chạy

Lượt 1 và lượt 2 chạy dưới nhãn `systemic` với reviewer `codex` — tức **cross-provider**, tức
đã thoả yêu cầu của `sensitive` **về nhà cung cấp**, dù nhãn ghi sai. Chúng KHÔNG bị vô hiệu.
Thứ bị vô hiệu là **lượt 3**: reviewer cùng nhà cung cấp, và dưới `sensitive` thì mức ấy không
đủ để land. Verdict lượt 3 vẫn có giá trị làm **dữ liệu tìm lỗi** — nó tìm ra bốn finding thật,
ba đã vá ở `a9e021d`.

## 7. Việc còn phải làm — có tên, không phải lời hứa

- **`PLAT-M4-effective-review-class-khong-co-chot-fail-closed`**: dựng chốt suy `review_class`
  từ write set thay vì đọc lời khai, fail-closed về `sensitive` khi không phân loại được
  (đúng chữ §8:569). Chưa có nhà trong `ops/NO_KY_THUAT.md` — tệp ấy đang nằm trong write set
  của `SLICE-B-C` (#215/PR #216), nên mục nợ vào sổ khi packet ấy land.
- **Trần kích thước**: người giữ kho quyết chấp nhận mức vượt có ghi, hay tách packet. Tách
  sau ba vòng review sẽ làm mất hiệu lực bằng chứng đã có; đây là đánh đổi, không phải một
  đáp án đúng sẵn.
