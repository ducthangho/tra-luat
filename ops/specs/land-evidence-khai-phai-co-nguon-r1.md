# Đặc tả packet LAND-EVIDENCE-KHAI-PHAI-CO-NGUON — r1

Đặc tả đóng băng. Sửa tệp này là đổi băm; muốn đổi thì soạn `land-evidence-khai-phai-co-nguon-r2.md`, không sửa đè.
Soạn bởi phiên Claude Code `session_017khPoiSXW9Yvefabg6MWaH` ngày 16-10-2026 theo yêu cầu chủ kho ("soạn spec và mẫu
comment cấp lease cho #773"). Các lựa chọn Q1–Q6 là KHUYẾN NGHỊ của phiên soạn; chủ kho chấp nhận chúng bằng chính comment
cấp lease neo băm tệp này.

## packet_id · packet_issue

- `packet_id`: `land-evidence-khai-phai-co-nguon`
- `packet_issue`: [#773](https://github.com/ducthangho/tra-luat/issues/773)
- `revision`: 1

## nguon_cap_viec

Chủ kho chọn "Mở packet làm validator" (16-10-2026) sau khi cùng một hình dạng lỗi — **H1: lời khai rộng hơn bằng chứng
giữ lại** — lặp ba lượt Codex connector trên PR ghi sổ #771 (hồ sơ `ops/land/pr765-wp743-land-evidence.yaml`):

| Lượt | Review | Lời khai | Bằng chứng thật |
|---|---|---|---|
| 1 | 5543182528 | `mergeable_state clean` dán `measured` | readback lưu ghi `unknown`; readback trước merge không lưu |
| 2 | 5543336170 | `positive: 'ubuntu 195/195 hong 0…'` | tệp nguồn chỉ có metadata cấp run, không có dòng tổng kết |
| 2 | 5543336170 | review connector nằm trong `pre_merge_checks` | mốc của nó SAU `merged_at` 28 giây |
| 3 | 5543383024 | "cả 14 job success" | `readback-run-*.json` không chứa job nào |

Không cổng nào kiểm điều này: `ops/bien_nhan_v2.py` chỉ kiểm `ops/reviews/*.receipt.yaml`; `ops/ci_duong_nhanh.py
kiem-re` chỉ kiểm hình thức diff.

## base

`origin/master` = `e0273d31aba78b014aa89297f32ff86f9daf0277` (đo 2026-10-16T05:38Z, 551/551 nhánh, `ls-remote` = `for-each-ref`).
Lease neo `start_from_sha` vào SHA master đo lại lúc cấp.

## review_class

`sensitive` — bộ kiểm bằng chứng land, thuộc "review/land authority" (PROTOCOL §8), cùng lớp #741. Reviewer: Codex CLI
(khác họ executor), chạy qua `launcher.py run`. Assurance để land: `human_audited`.

## quyet_dinh (khuyến nghị, chủ kho chấp nhận bằng comment cấp lease)

- **Q1 — hai đợt lease.** `.github/workflows/ci.yml` đang bị lease `wp748-r12-g12-claude-windows-20261016` (packet #748)
  giữ tới 2026-10-16T15:05:12Z (`ai-dang-giu` rc=11, đo 05:38Z). Nên:
  - **g1** (lease này): `ops/land_evidence_nguon.py` + `ops/land_evidence_nguon_test.py`. Không đụng workflow.
  - **g2** (lease riêng, cấp sau): MỘT bước trong `ci.yml` gọi bộ test, CHỈ cấp khi `ai-dang-giu .github/workflows/ci.yml`
    ra `NGƯỜI_GIỮ 0`. Packet KHÔNG được coi là xong khi g2 chưa land — guard không nằm trên đường tự động thì chỉ là
    tài liệu (bài học r225).
- **Q2 — miễn trừ tệp cũ bằng danh sách ĐÓNG BĂNG theo băm.** Ở base có **27** tệp `ops/land/*-land-evidence.yaml`, 18 tệp
  dùng nhãn `measured` dạng văn xuôi (tới 92 lần/tệp), 0 tệp có `nguon_positive`. Bộ kiểm giữ `MIEN_TRU_CUTOVER` =
  {tên tệp: sha256 byte} của MỌI tệp `*-land-evidence.yaml` có trên `origin/master` lúc executor bắt đầu (đo và ghi vào
  handoff). Tệp trong danh sách mà băm KHỚP ⇒ bỏ qua có ghi nhận. Băm LỆCH ⇒ mất miễn trừ, phải ĐẠT đủ luật. Tệp không
  trong danh sách ⇒ phải ĐẠT. Thêm tên mới vào danh sách mà không khớp ảnh chụp cutover ⇒ test ĐỎ (cùng hình bánh cóc
  `NO_DA_DO` của `bien_nhan_v2`). Nếu PR #771 land trước lúc bắt đầu, `pr765-wp743-land-evidence.yaml` thuộc danh sách.
- **Q3 — luật đo trên VĂN XUÔI phải xác định được.** Một "lời khai đo" là mọi chuỗi YAML (ở bất kỳ độ sâu) mà sau khi
  bỏ khoảng trắng đầu bắt đầu bằng token `measured` theo sau là khoảng trắng, `—`, `-` hoặc `:`. "Token nguồn" là chuỗi
  khớp `[A-Za-z0-9_./{}*-]+\.(json|txt|log|yaml|yml|md|sh|py|patch)` hoặc kết thúc bằng `/`. Token phân giải theo thứ tự:
  thư mục `<tên hồ sơ bỏ "-land-evidence.yaml">-provenance/`, `ops/land/`, gốc kho. Glob (`*`) phải khớp ≥1 tệp.
- **Q4 — trần kích thước.** ADR-0044: ≤ 3 tệp, ≤ 300 dòng thêm. Bộ kiểm + test có phản chứng và đột biến ước tính vượt
  300. Xin ngoại lệ **≤ 600 dòng thêm cho g1** ngay trong comment cấp lease. Vượt 600 ⇒ DỪNG, hỏi chủ kho.
- **Q5 — không sửa hồ sơ cũ.** Packet này KHÔNG chạm tệp `ops/land/**` nào; mọi hồ sơ cũ đi qua miễn trừ Q2.
- **Q6 — CLI.** `python ops/land_evidence_nguon.py [--root GOC] [--tep TEP ...]`; mã thoát `0` ĐẠT, `1` ĐỎ, `2` KHÔNG ĐO
  ĐƯỢC. Dòng cuối bắt buộc dạng `land_evidence_nguon: <n> ĐẠT · <m>/<k> miễn trừ (băm khớp) · <v> vi phạm · <u> KHÔNG ĐO
  ĐƯỢC · tổng <t>` rồi `TỔNG: ĐẠT|ĐỎ|KHÔNG ĐO ĐƯỢC`.

## write_set (g1)

1. `ops/land_evidence_nguon.py`
2. `ops/land_evidence_nguon_test.py`

Đo 2026-10-16T05:38Z: `ai-dang-giu` cho cả hai ra `NGƯỜI_GIỮ 0`, rc=0. Phải đo lại trước khi cấp.
g2 (ngoài lease này): `.github/workflows/ci.yml`.

## muc_tieu

| # | Luật | Đỏ khi |
|---|---|---|
| L1 | Mỗi lời khai đo (Q3) chứa ≥ 1 token nguồn phân giải được tới đường dẫn CÓ THẬT. | Không có token nào, hoặc mọi token đều không phân giải được. |
| L2 | Mọi mapping có khoá `positive` phải có `nguon_positive` (chuỗi hoặc danh sách) cùng cấp; mỗi tệp tồn tại; mọi token `\d+/\d+` và `hong \d+` trong `positive` phải xuất hiện NGUYÊN VĂN trong ≥ 1 tệp `nguon_positive`. | Thiếu `nguon_positive`, tệp vắng, hoặc một token không có trong tệp nào. |
| L3 | Nếu hồ sơ có `pre_merge_checks` và thư mục provenance có `readback-pr-*.json` mang `merged_at`: mọi mốc ISO-8601 đầy đủ (`YYYY-MM-DDTHH:MM(:SS)?Z`) xuất hiện trong một phần tử `pre_merge_checks` phải `<` `merged_at`. | Một mốc `>=` `merged_at`. |
| L4 | Ba trạng thái. YAML hỏng, thư mục provenance cần mà vắng, đọc tệp lỗi ⇒ KHÔNG ĐO ĐƯỢC (rc=2), không bao giờ ĐẠT. | Lỗi đo bị đếm thành ĐẠT. |
| L5 | Miễn trừ theo Q2. | Tệp miễn trừ băm lệch mà vẫn được bỏ qua; tên mới thêm vào danh sách mà test không ĐỎ. |

## nghiem_thu

| Mục | Tiêu chí | Phép đo làm ĐỎ |
|---|---|---|
| chung | `python ops/land_evidence_nguon.py --root .` trên cây g1: `TỔNG: ĐẠT`, rc=0, `<m>/<k>` với m = k = số tệp miễn trừ. | rc≠0, hoặc m≠k. |
| L1 | Ca dựng lại lượt 1 của #771 (`mergeable_state clean` dán `measured`, không token nguồn) ⇒ ĐỎ đúng luật L1. | Ca ra ĐẠT. |
| L2 | Ca dựng lại lượt 2 (`positive` trỏ readback chỉ có metadata) ⇒ ĐỎ L2; thêm `nguon_positive` chứa đúng chuỗi ⇒ ĐẠT; đổi một số trong tệp nguồn ⇒ ĐỎ. | Bất kỳ chiều nào sai. |
| L3 | Ca dựng lại lượt 2 (mốc 02:58:54Z trong `pre_merge_checks`, `merged_at` 02:58:26Z) ⇒ ĐỎ L3; chuyển sang `post_merge_checks` ⇒ ĐẠT. | Bất kỳ chiều nào sai. |
| L4 | YAML hỏng ⇒ rc=2; provenance vắng khi có lời khai đo ⇒ rc=2. | rc=0. |
| L5 | Sửa một byte tệp miễn trừ ⇒ tệp đó bị kiểm đủ luật; thêm tên lạ vào `MIEN_TRU_CUTOVER` ⇒ test ĐỎ. | Bỏ qua im lặng. |
| đột biến | Mỗi luật L1–L5 có ≥ 1 đột biến (trên BẢN SAO TẠM) làm đúng ca đích ĐỎ, chết bằng chốt chứ không bằng traceback (bài học `TinHieuChotCa`). | Đột biến sống, hoặc chết vì lỗi vô can. |
| thực địa | Chạy trên hồ sơ thật của #771 ở `c6e2401`, `1a4c417`, `d60b9e6` (ngoài miễn trừ): ghi vào handoff danh sách ĐỎ từng head. Ở `c6e2401` phải ĐỎ ít nhất các dòng của lượt 1. | Không đo (ghi `KHÔNG ĐO ĐƯỢC` kèm lý do nếu không fetch được). |
| chung | ruff F delta 0 trên hai tệp; `git diff --check` sạch. | Tăng F, hoặc diff bẩn. |
| review | Codex CLI read-only (checkout NGOÀI vùng ghi được của sandbox — bài học #771), exact SHA, P1=0 P2=0. | P1/P2 mở. |

## ngoai_pham_vi

- Sửa bất kỳ hồ sơ `ops/land/**` nào (Q5).
- Nối CI (g2, Q1).
- Kiểm `ops/reviews/*.receipt.yaml` — đã có `bien_nhan_v2`.
- Kiểm NGỮ NGHĨA của lời khai (tệp nguồn có thật sự chứng minh câu văn hay không). L1 chỉ đo "có trỏ tới thứ có thật";
  L2 mới đo nội dung, và chỉ cho token số. Khai thẳng giới hạn này trong docstring.

## Trần kích thước

g1: 2 tệp, ≤ 600 dòng thêm theo Q4 (ngoại lệ ADR-0044 xin trong comment cấp lease). Khi báo cáo ghi đúng dạng
"2 tệp / N dòng thêm; trần ngoại lệ 600".

## chua_do_duoc

- Chưa có prototype; số dòng ước tính.
- L3 chỉ dùng được khi provenance có readback PR; hồ sơ không có thì L3 ghi "không áp dụng", không ĐẠT ngầm.
- Việc PR #771 land trước hay sau lúc bắt đầu chỉ đổi thành phần `MIEN_TRU_CUTOVER`, không đổi luật.
