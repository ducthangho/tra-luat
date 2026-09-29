# Cross-review PR #468 — LƯỢT 15, `ducthangho/tra-luat`

Reviewer khác nền (executor Claude; bạn Codex).
`reviewed_sha` = `745d888` · lượt 14 review `922956a`.
Diff `922956a..745d888`: **2 tệp** (`numstat.txt`, `diff-sau-luot14.patch`) — thuần văn bản +
manifest lập lại.

Lượt 14 (`VERDICT-luot14.md`): **`approve` — 0 P1 · 0 P2 · 2 P3**. Lượt này chỉ để đóng hai P3.

## NHIỆM VỤ 1 — ĐỐI CHIẾU LƯỢT 14

| slug | mức | lượt 14 nói gì |
|---|---|---|
| `full-gate-t33-nham-that-bai-voi-khong-chay` | P3 | README viết "t33 không chạy" trong khi log ghi `ĐỎ t33` và `đã chạy=121, bỏ qua=0` |
| `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu` | P3 | phân loại nguồn mạnh hơn hiện vật; chỉ 1/6 stdout tự đếm lại được |

**Executor tự khai đã vá, KIỂM LẠI:**

- README nay có mục **ĐÍNH CHÍNH** nói `t33` ĐÃ CHẠY và ĐỎ ở tiền điều kiện; thứ chưa chạy là
  thao tác **lint workflow** bên trong hàm. Bản đính chính ấy có ĐÚNG với log không? Đối chiếu
  `nen.lease.norm.out` và `sau.lease.norm.out`.
- README nay có bảng phân loại: `doc-claims` 70861 B **tự đếm lại được**; `cidk` 2934 B (hiện vật
  tail 206 B), `ploop` 8752 B (96 B), `lease` 8971 B (bản chuẩn hoá 8827 B), `doctrine-scan`/
  `adr-song` **không giao hiện vật**, 12 `rc` và các số giây là log tổng hợp — đều KHÔNG tự đếm
  lại được. Tức **1/6**. Tự đo lại con số 1/6 ấy.
- DELTA=0 nay thu về **bốn cặp tệp thực sự lưu**. Còn chỗ nào nói rộng hơn không?

## NHIỆM VỤ 2 — bản vá có sinh lỗi mới không?

- `ARTIFACTS.sha256` được lập lại (1 dòng đổi). Manifest có còn `rc=0` và phủ đủ tệp không?
  Có tệp nào rơi ra ngoài không?
- Sửa văn bản có vô tình làm sai một lời khai đang ĐÚNG không?
- Mục ĐÍNH CHÍNH có tự mâu thuẫn với phần còn lại của README không?

## NHIỆM VỤ 3 — phần chưa ai đóng

Nêu thẳng nếu còn: manifest các gói review ghi **bố cục sandbox** chứ không phải bố cục kho, ánh
xạ ở `DOC-MANIFEST.md` — kiểm theo ánh xạ thì **mọi** manifest trong `ops/reviews/**` có `rc=0`
không? Nêu `N/N` từng gói.

## Phạm vi cứng

- CHỈ ĐỌC/GHI TRONG SANDBOX. `cay-kho/` detached `745d888`, sạch, 306 `refs/heads` (do
  `update-ref` tạo CÓ CHỦ Ý). `status --porcelain` phải RỖNG khi xong.
- Không cấp lease, không đăng Issue/PR, không merge, không sửa kho thật.
- Không nâng `timeout-minutes` (`PROTOCOL §12`).
- KHÔNG chạy bộ test dài, KHÔNG gọi CI. Được: `git` chỉ đọc, `yaml.safe_load`, `ai-dang-giu`,
  `lease_publish.py check`, `doc-claims-check`, `doctrine-scan`, `adr-song`, `sha256sum`, và
  gọi TRỰC TIẾP hàm `t33` nếu cần. Không đóng được bằng phép ngắn ⇒ ghi
  `KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)`.
- **Ghi kết luận ra `VERDICT.md` NGAY khi có.**

## GÓI VÁ GỢI Ý — bắt buộc cho mọi P1/P2
Nhãn: *"chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit"*.

## Định dạng `VERDICT.md`
```
verdict: approve | changes_requested | blocked
reviewed_sha: 745d888...
base_da_review_truoc: 922956a7048fd23eea1c9f88aeb986e076f10e24
so_lan_luot_nay_bi_chet_va_phong_lai: <số>

## ĐỐI CHIẾU LƯỢT TRƯỚC
- <slug lượt 14>: ĐÃ VÁ THẬT | VÁ HỜ | VÁ SINH LỖI MỚI | CHƯA VÁ — <bằng chứng bạn tự đo>

## BẢNG ĐO
| khẳng định | hồ sơ khai | tôi đo được | khớp? |

### <slug>  [P1|P2|P3]  <tiêu đề>
TỆP/DÒNG: · VẤN ĐỀ: · ĐÃ THỬ VÁ: · GÓI VÁ: · ĐÃ THỬ NGHIỆM: · ĐỘ TIN:
```
**Giữ NGUYÊN slug.** `approve` là kết quả hợp lệ — mục tiêu là **hết P1**.
