**Tiêu đề:** `GATE-TACH-JOB-CAT-CHI-PHI — tách job để cắt wall-clock, KHÔNG nâng trần`

> **CHƯA ĐỦ ĐIỀU KIỆN BẮT TAY.** Đặc tả đã đóng băng; hai điều kiện chưa thoả, ghi ở mục cuối.
> Packet này **đi ĐẦU** — ba packet còn lại đo trên bố cục đã tách.

## Vấn đề

`gate` trên `windows-latest` đang tiến sát trần `timeout-minutes: 60`. Trần đã được nâng **hai
lần, ba mức** (`25` khởi tạo `9e4f361` → `45` `6d88a2c` → `60` `7657bfd`). `PROTOCOL §12` coi việc
nâng lần nữa là **điều kiện DỪNG**, nên **đặc tả này không đề xuất nâng trần** và packet nào đề xuất
thì bị bác.

## Trần 60 KHÔNG còn là rủi ro suy diễn — nó ĐÃ BỊ CHẠM (run `workflow_dispatch` trên nhánh `claude/tra-luat-process-review-o4d7kb`, không phải master — sửa theo lượt 8)

Run `34048229370`, head `4cd80c5`, `gate (windows-latest)`: **60,17 phút**, `conclusion: cancelled`,
cắt giữa bước `test registry`, **26 / 44** mục còn `skipped`. Job ubuntu cùng run `success` `26,42 p`.

(Hình dạng này dễ đọc nhầm: **run** `cancelled` mà **một job** `success` là ngữ nghĩa tổng hợp bình
thường của GitHub, **không** phải hai tầng mâu thuẫn.)

## Nền — đo ba lần, và nó TRÔI NHANH HƠN tốc độ viết đặc tả

| | 18:10Z 06-09 | 00:45Z 07-09 | **02:49Z 07-09** |
|---|---:|---:|---:|
| `n` job Windows `success` | 2 | 9 | **11** |
| max (phút) | 42,28 | 49,62 | **50,48** |
| **biên độ** | — | 9,42 | **10,28** |
| **biên còn lại dưới trần 60** | 17,72 | 10,38 | **9,52** |

Không con số nào sai lúc viết; chúng **hết hạn**, và hết hạn theo **chiều xấu đi**. Đó là `L5` phát
biểu bằng dữ liệu. **Phiên thi công phải ĐO LẠI**, đừng trích bảng này.

**Hệ quả cho `nghiem_thu` (sửa theo lượt 7–8):** biên độ `10,28` phút là **khoảng biến thiên của một mẫu tiện tay
gộp khác tải (39/40 bước) lẫn khác nhánh (5 master + 6 nhánh)** — không phải nhiễu runner thuần, không phải phương
sai. Nó là lý do ĐỌC kết quả A1 thận trọng, **không** phải giấy phép nới: **A1 giữ `≤ 25,00`**, A1 ĐỎ thì báo chủ kho
như KẾT QUẢ ĐO (đặc tả revision 2–3, `chua_do_duoc` #3; nợ có tên `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`).

## Hệ số nền KHÔNG phải một con số — và điều này đổi hướng ba packet kia

`tỉ lệ = giây Windows / giây ubuntu`, **cùng bước, cùng head**, cả hai nền `success`. Nguồn ghi theo
GIÂY nên mỗi tỉ lệ là một **DẢI**, không phải một điểm.

| bước | n cặp | thấp nhất | cao nhất | trung vị |
|---|---:|---:|---:|---:|
| `test registry` | 11 | 1,07× | 1,71× | **1,20×** |
| `tl selftest` | 11 | 1,41× | 2,26× | **1,83×** |
| `packet-loop selftest` | 11 | 1,88× | 2,89× | **2,35×** |
| `G5 kiem ban ke` | 11 | 1,91× | 3,09× | **2,39×** |
| `lease-publish selftest` | 11 | 2,42× | 3,84× | **2,94×** |
| `bien-nhan v2 selftest` | 10 | 7,07× | 9,74× | **7,56×** |
| **job trọn `gate`** | 11 | 1,52× | 2,36× | **1,73×** |

**Đính chính sau lượt 7 (finding P1 `thieu-hien-vat-quyet-dinh-h-va-chi-phi`):** bảng trên chép từ đặc tả GATE
ĐÃ ĐÓNG BĂNG (lease đã cấp), tính từ `buoc_master.tsv` **không có trong kho**. Tái tính từ nguồn TRONG KHO
(`ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/buoc.tsv`, cùng 11 run, cùng bộ lọc) cho **4/7
trung vị lệch**: `test registry` **1,21×** (khai 1,20) · `packet-loop selftest` **2,37×** (2,35) · `G5` **2,40×**
(2,39) · `bien-nhan v2 selftest` **7,79×** (7,56 — ngoài cả dải làm tròn đã khai `7,48–7,65`); `n`/min/max
khớp. Và **11 run ấy KHÔNG đều là master**: 5 `master/push` + 6 run nhánh khác (`pull_request`/`workflow_dispatch`),
1 head 39 bước + 10 head 40 bước — tức biên độ `10,28` gộp cả khác tải lẫn khác nhánh (finding P2
`bien-do-khac-head-khong-phai-nhieu-runner`). Bảng trong đặc tả **revision 1** vì vậy là **lời khai lịch sử**; con số
dùng được là con số tính lại được từ `buoc.tsv` — và **revision 2** (07-09-2026, chỉ thị chủ kho) đã đưa đúng bảng ấy vào
đặc tả, **revision 3** sửa nốt A2 và các câu sót (xem footer). Bảng dưới đây giữ nguyên số revision 1 để đối chiếu lịch sử;
bảng hiện hành ở đặc tả r3.

Nội suy *"Windows đắt gấp ~3"* mà hai packet `MUTANT-WINDOWS-*` dựa vào là **sai theo cả hai chiều**:
quá CAO cho job trọn (`1,73×`), quá THẤP hơn hai lần cho một selftest python nặng (`7,79×` theo r2–r3; r1 ghi `7,56×`).
Dải toàn bộ `1,07×` – `9,74×`. **Một hệ số duy nhất không dùng được** — phải nói rõ đang nhân cho
**bước nào**.

Cảnh báo tự khai, để không ai đọc rộng hơn phép đo: không bước nào trong bảng là một **vòng đột
biến** — thứ hai packet kia thật sự cần nhân. Đây là **proxy gần nhất đo được**, không phải phép đo
thay; nợ `CHUA-CO-PHAN-RA-THOI-GIAN-THEO-BO-TREN-WINDOWS` **vẫn mở**.

## Hướng

Tách `gate` thành nhiều job chạy song song để cắt **wall-clock của job dài nhất**, giữ nguyên điều
kiện chạy và trần. Đặc tả nói thẳng cái giá: **phút tính tiền TĂNG** (Windows nhân hệ số ×2 theo chú
thích `ci.yml:19-23`), trong khi wall-clock giảm. Nếu `max` **không** giảm dù đã tách, đó là **KẾT
QUẢ ĐO**, không phải thất bại — và phải ghi như vậy.

## Ràng buộc

- **KHÔNG nâng `timeout-minutes`** (`PROTOCOL §12`).
- Mọi job mới mang **cùng** `if` mức job, cùng biểu thức ma trận `fromJSON(...)`, cùng `timeout-minutes`;
  mọi bước dời đi giữ nguyên `if` của nó.
- **Đừng viết cú pháp biểu thức Actions trong comment của `run`** — một cặp `${{ }}` rỗng trong một
  dòng chú thích làm GitHub **từ chối cả tệp** (đã trả giá: run `31971137920`, 0 job).
- Consumer của `ci.yml` nằm **ngoài** `ci.yml` — đổi tên job làm hỏng required status check.

## HAI ĐIỀU KIỆN CHƯA THOẢ

**(1) Chưa có `cross_approved`.** Lượt 5 chết năm lần vì hạ tầng (chữ ký `Connection refused (os
error 111)` trên đường tái kết nối của `codex`; chẩn đoán "proxy không cho `WebSocket upgrades`" ở bản
đầu là **SAI** — đính chính 03:55Z 07-09-2026, nguyên nhân thật **CHƯA BIẾT**). **Lượt 6** (Codex
`gpt-6-astra`, 07-09-2026, phóng có giám sát, chạy trọn 1851 s) trên `reviewed_sha` `2adb681`:
`changes_requested`, **7 P1 / 4 P2**, P3 cũ đóng; P1 cũ `span-rong-nuot-ti-le-vo-can` xếp **VÁ HỜ về
nghĩa vụ xác nhận** (1213 ca / 0 đỏ giả / 0 bỏ sót, nhưng hồ sơ thiếu hiện vật để tái tính). Verdict:
`ops/reviews/pr468-hoso-4-packet-review-6-codex-verdict.md`. Biên bản lượt 5:
`ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md`.

**(2) Write set — đo trên CẢ HAI đường dẫn của lease, 05:52Z 07-09-2026** (bản đầu của mục này chỉ đo
`ci.yml` rồi kết luận "không bị chặn" — finding P1 `issue-kiem-lease-sai-write-set` lượt 6):

```
ai-dang-giu .github/workflows/ci.yml          ⇒ NGƯỜI_GIỮ 1: gate-tach-job-cat-chi-phi-exec-1-claude-20260906
ai-dang-giu .claude/dev/ci_dang_ky_test.py    ⇒ NGƯỜI_GIỮ 2: gate-tach-…  +  mutant-khong-chay-tren-windows-…
```

Bản lease #456 **trên `master`** chưa có bia mộ (bia mộ chỉ nằm trên nhánh của PR này), nên packet
**BỊ CHẶN** cho tới khi PR #468 merge hoặc lease #456 hết hạn tự nhiên lúc `14:30:07Z 07-09-2026`.
Nói cho đúng mức theo lượt 7 (finding P1 `bia-mo-mot-ref-khong-thu-hoi-moi-ban`): "merge là hết chặn" chỉ
đúng khi **mọi ref** còn giữ blob cũ được cập nhật/dọn — `ai-dang-giu` đếm mọi `(blob, path)` trên mọi ref.
Trên máy chủ lúc 07:4xZ 07-09-2026 (`git ls-remote --heads`) **không** có nhánh `claude/gate-tach-job-cat-chi-phi`;
ref ấy trong snapshot của reviewer là nhánh cục bộ của phiên executor (bằng `d28c4b1`) lọt vào mirror qua chuỗi
clone. Executor sẽ chỉ đẩy nhánh packet sau khi rebase lên cây có bia mộ, và **đo lại `ai-dang-giu` sau fetch đủ
ref trước khi bắt tay** — không suy từ merge.
Phép canh hai nguồn ref chạy trước: máy chủ 299 ⊆ cục bộ 300 (`comm -23` rỗng) ⇒ không mù.

---

**Đặc tả đóng băng (revision 2):** `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md` @ `d85365463259615537c4fb96acd2408d917d9bd2` (commit ĐẦU TIÊN chứa bản có băm dưới đây; revision 1 @ `b743f17`, băm `8cca700c…`)
**`spec_sha256`:** `37800aa6b33afb8caf3296440bd0ac49dbd6b4300fe59f832e11ae629cc1ffb2` (**revision 3**, 07-09-2026 — chỉ thị https://github.com/ducthangho/tra-luat/issues/463#issuecomment-5568696936; revision 2 = `bda86f128c220b868e9c103c919d213d8aba5ed1753962b0898ea1ce1852812c`; revision 1 = `8cca700cba9c2312d05bf64eee3d4a5bda5317cb45e244ed22161b4ddcc83c62`)
**`base_sha`:** `1b3caa1` lúc soạn; **ba mỏ neo trong lease đo lại lúc cấp = `d28c4b1`** (head `master`
03:37:33Z 07-09-2026) · **đi TRƯỚC** `LO-319` · `2A` · `2B`
**Lease ĐÃ CẤP (revision 3):** `ops/leases/gate-tach-job-cat-chi-phi-exec-1r3-claude-20260906.yaml` (0 ô null; cấp 2026-09-07T09:44:51Z, hạn 2026-09-08T09:44:51Z, `thay_the_cho` exec-1r2,
uỷ quyền neo https://github.com/ducthangho/tra-luat/issues/463#issuecomment-5568696936); chuỗi `#456 → exec-1 → exec-1r2 → exec-1r3`, mỗi mắt mang bia mộ `da_bi_thay_the` hai chiều.
**Nền A1/A5 tái lập được TRONG KHO:** `ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/`
(13 run · 26 job · 1140 bước, `job.tsv` + `buoc.tsv` + `tinh.py`, đo 03:54Z 07-09-2026) — thay cho
`buoc_master.tsv` mà đặc tả nhắc nhưng không có trong kho (finding P1 `thieu-hien-vat-quyet-dinh-h-va-chi-phi`).
