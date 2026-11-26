# Review offline MÃ — packet `bo-sinh-bat-bien` r1 g1 (Issue #1539) — lượt 5 (XÁC NHẬN) — reviewer độc lập, theo PROTOCOL §8.3 và ADR-0060

Bạn là reviewer ĐỘC LẬP, chỉ đọc, cho MÃ của work packet `sensitive` `bo-sinh-bat-bien` (kho ducthangho/tra-luat). Đây là lời gọi Codex **5/5**: trần lease là 4, chủ kho nâng thêm đúng một lời gọi chỉ cho lượt XÁC NHẬN này trên đúng SHA, không đổi mã (#1539 issuecomment-7197354187). Gốc của lượt: `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5`.

## Vì sao có lượt này
Lượt 4 (của bạn, `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/lich_su/luot4/VERDICT.md` và `VERDICT.json`) review ĐÚNG ứng viên `97ec968` và kết luận `changes_requested` CHỈ vì hai P3 R4-01, R4-02 (lớp `nghiem-thu-khong-co-lap-chot-dich`) đang chờ chủ kho; không còn P0/P1/P2; R3-01, R3-02, R3-03 `DA_VA_THAT`, lớp `nghiem-thu-thoi-gian-chua-dat` đóng. Sau đó chủ kho đã miễn hai P3 neo đúng SHA này. Lời miễn (trích nguyên văn từ #1539 issuecomment-7197313309, phiên điều phối ghi hộ lựa chọn chủ kho bấm trong hộp câu hỏi: *"Miễn 2 P3, đi tiếp (Recommended)"*):

```
mien_p3: 97ec9686184fdf55dc1736007e6fdcb186122465 nghiem-thu-khong-co-lap-chot-dich
```
Nợ ghi: `BO-SINH-BAT-BIEN-R4-01-danh-tinh-mien-doi-so`, `BO-SINH-BAT-BIEN-R4-02-danh-tinh-128-ascii`.

Bạn KHÔNG truy cập được GitHub; coi trích dẫn trên là đầu vào do điều phối cung cấp, và ghi rõ trong verdict rằng bạn dựa vào nó (không tự kiểm được tác giả comment). Cổng `kiem-merge` K5 sẽ tự đo dòng `mien_p3:` trên GitHub.

Mục tiêu: xác nhận rằng trên ĐÚNG `97ec968` (a) không có gì đổi so với lượt 4, (b) không có finding P0–P2 nào lượt 4 bỏ sót, (c) điều kiện duy nhất còn lại của lượt 4 là lời miễn hai P3 nay đã có — rồi ra kết luận chính thức theo §8. Đây KHÔNG phải lượt tìm P3 mới: không lặp lại việc quét đột biến sâu của lượt 4.

## Quyền
- CHỈ ĐỌC trong `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/repo`. Không sửa, không commit, không push. Không gọi GitHub/mạng.
- Tệp nháp: CHỈ dưới `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/work/`. Đặt `PYTHONDONTWRITEBYTECODE=1` và `TMPDIR=/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/work/tmp`.

## Đầu vào
- `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/repo` ở HEAD `97ec9686184fdf55dc1736007e6fdcb186122465` (tree `9f8123cc4de66c59968a1b8a3c8d8ef05be0b5eb`), base `a89c83acf998008caecba9084a7d295845bf1976`.
- `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/SPEC.md` (sha256 phải là `bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577`), `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/LEASE.yaml`.
- Verdict lượt 1–4 của bạn và các probe: `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/lich_su/`. Bằng chứng executor lượt 4: `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/bang_chung/` (lời khai).
- Thông tin sau lượt 4, do điều phối đo (lời khai, chỉ ghi nhận): Windows local M3 trên DESKTOP-T9R33P2 xanh cho `97ec968` (biên nhận #1539 issuecomment-7196524386: B 40/40·145/145, A 53/53·149/149, `land_evidence_nguon` ĐẠT, `ci_dang_ky_test` 1654/1654, selftest 1788/1789 hai vế cùng ca đỏ `r380_llm_khai_niem_bien_dau_vao`, delta 0). Luật 9 trên `97ec968`: executor đang chạy, chưa có kết quả.

## Việc phải làm
1. Xác nhận `git rev-parse HEAD` = `97ec968…`, tree khớp, cây sạch, `git diff a89c83a HEAD` chỉ chạm hai tệp write set, numstat +274 −9 (trần 320), `git diff --check` rc 0.
2. Chạy lại: `python3 -B ops/land_evidence_nguon_test.py` và `python3 -B ops/gate_output_doi_chieu_test.py` (đòi `CA: N/N`, `DOT BIEN: M/M`, `TONG: DAT`); `python3 -B ops/land_evidence_nguon.py --root .`; `python3 -m ruff check --select F` hai tệp so base. Hai module sản phẩm byte-identical base.
3. Đối chiếu lớp (§8.3): gán nhãn cho hai lớp có ở lượt 4. R4-01, R4-02: miễn neo SHA (ghi trong `prior_class_status` với evidence trỏ lời miễn). Nếu phát hiện finding MỚI mức P0–P2, báo đủ với phép đo; P3 mới ⇒ báo và ghi `chờ miễn chủ kho`.
4. Quét nhanh theo lớp toàn diff một lượt để chắc lượt 4 không bỏ sót P0–P2: ưu tiên những gì có thể làm bộ test ĐỢT A hoặc ĐỢT B xanh giả trên chính sản phẩm (chốt bị đường nhớ đệm che, ca phản chứng tự xanh trên mọi đầu vào, đọc tệp nguồn bằng AST có thể ném ngoại lệ ở môi trường CI/Windows, phụ thuộc phiên bản Unicode giữa Python 3.12 và 3.13).
5. Nhắc lại các mục `not_run` (luật 9 trên SHA này, CI, M9, connector, audit uỷ quyền) — chúng KHÔNG làm verdict thành `changes_requested`; ghi vào `not_run`.

## Mức nghiêm trọng — §8
`sensitive`: approve chỉ khi 0 P0/P1/P2 mở; **mỗi P3 phải đóng** (bạn xác nhận có bằng chứng, hoặc chủ kho miễn neo exact SHA). Mỗi P2+ phải có phép đo. Một P3 đã được chủ kho miễn neo SHA thì ghi trong `prior_class_status` (status + evidence trỏ lời miễn), KHÔNG để nó làm `verdict` thành `changes_requested`.

## Đầu ra
1. `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/work/VERDICT.json`: khoá như lượt 4 (`reviewed_sha`, `reviewed_tree`, `base_sha`, `spec_sha256`, `vong`: 5, `findings`, `class_table`, `prior_class_status`, `verdict`, `m3_windows`, `pham_vi_e`, `luat9`, `not_run`, `limits`). Kiểm `python3 /tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/kiem_verdict_lop.py /tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/work/VERDICT.json --vong 5` (phải `HOP_LE`; lưu stdout vào `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/work/kiem_verdict.txt`).
2. `/tmp/claude-0/-home-user-tra-luat/cb39e949-45ab-5475-a00b-c971889891ff/scratchpad/review1539/l5/work/VERDICT.md`: tóm tắt; dòng cuối `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested`.
3. **Tin nhắn trả lời cuối cùng của bạn** (thứ in ra stdout) phải KẾT THÚC bằng đúng một dòng riêng, không định dạng, không ký tự nào sau nó: `KET_LUAN: approve` hoặc `KET_LUAN: changes_requested` — trùng với dòng cuối của VERDICT.md. Cổng `kiem-merge` K4 đọc dòng cuối của stdout này.
