# Cross-review packet wp923 r2 (pha B) — lớp sensitive, reviewer codex

Bạn là REVIEWER độc lập (họ openai) cho một diff của executor họ claude. Bạn chỉ ĐỌC và ĐO;
không sửa `cay-kho/`, không commit, không push, không gọi mạng. Mọi kết luận phải kèm lệnh + output thật.

## Neo
- Kho: github.com/ducthangho/tra-luat. Bản sao làm việc: `cay-kho/` (checkout detached).
- base_sha = `e139e55883d90fd74a358230be5599c9e223d4b3`
- reviewed_sha = `67bacb3b51ac9eda72297b10b15b798b3ca51959` (kiểm `git -C cay-kho rev-parse HEAD`).
- Đặc tả đóng băng: `SPEC.md` (sha256 `a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1` — tự băm lại).
- Diff: `diff.patch`, `numstat.txt` (cũng tái dựng được bằng `git -C cay-kho diff <base> <reviewed>`).
- Log N2 executor đã chạy: `n2_base.log`, `n2_head.log`.

## Việc của packet (tóm tắt — SPEC.md là nguồn)
Chỉ sửa DÒNG CHÚ THÍCH trong `.claude/dev/ci_dang_ky_test.py` đang khẳng định `timeout-minutes` HIỆN TẠI của job
`.github/workflows/ci.yml` mà đã sai. Câu lịch sử có mốc giữ nguyên; giá trị mới thì nối câu có mốc.

Executor khai:
1. `:759` `(nay 105)` (gate-registry) → `(#705: 105 · #910 pha B, a7da463: 150)`.
2. `:808` câu `WP748 r16: … tran 30 phut` (về `gate-nhanh-manh`/`gate-nhanh-gop`, đúng bộ khoá trong `bam_gate_nhanh`)
   được GIỮ, nối dòng mới `# #910 pha B (PR #917, a7da463): tran job manh 30 -> 150; job gom van 10.`
3. Quét toàn tệp bằng `tokenize` lọc COMMENT có timeout/phút/trần job: 5 dòng (759, 760, 761, 808, 978).
   760 không có số; 761 là câu lịch sử `#705 … job 90 → 105 phút` ⇒ giữ; 978 nói trần 360 của job mảnh
   trong `ci-dot-bien-du.yml` (không phải `ci.yml`) và khớp hằng `"timeout-minutes": 360` ngay dưới ⇒ ngoài phạm vi.
4. N3: `git grep ci_dang_ky_test` ngoài `*.md`: không có chốt băm NGUYÊN BYTE sống; chỉ có import/runpy/copy
   (`ops/ci_provenance.py`, `ops/ci_duong_nhanh_test.py`, `.claude/dev/doc_receipt_thu_hoi_test.py`, ps1) và ảnh chụp
   bằng chứng lịch sử trong `ops/reviews/**`, `ops/land/**`.
5. N1 +2/−1, 0 dòng không phải chú thích; `ast.dump` base == head. N2 `TỔNG: ĐẠT` base và head, output giống hệt.
   N4 `scripts/tl.py --selftest` 1731/1731 trên 67bacb3.

## Việc của bạn — BẢNG SĂN ≥ 5 hướng ĐỘC LẬP, mỗi hướng có LỆNH + OUTPUT THẬT
Gợi ý (tự thêm hướng khác):
- H1 N1: mọi dòng `+`/`-` là chú thích; AST bằng nhau (chạy python thật trên hai blob).
- H2 Đúng sự thật: đối chiếu từng giá trị mới với `ci.yml` ở base (`git -C cay-kho show <base>:.github/workflows/ci.yml`),
  và mốc `a7da463`/PR #917 với `git log` (kho có đủ lịch sử? kiểm `--is-shallow-repository`). Câu 808 nói về job nào —
  xác định bằng mã ngay dưới (`BAM_GATE_NHANH` → `bam_gate_nhanh`), không đoán.
- H3 Độ phủ quét: còn câu chú thích nào khác khẳng định timeout HIỆN TẠI của job `ci.yml` mà executor bỏ sót?
  Tự quét bằng phương pháp KHÁC executor (vd regex số phút, "trần", "phut", "nay", tên job). Lưu ý cả dạng không dấu.
- H4 N3: có chốt nào băm/so nguyên byte tệp này (blob sha, sha256 của tệp, bảng băm tệp test, manifest)? Đừng chỉ grep
  tên tệp — thử grep blob OID của tệp ở base (`git rev-parse <base>:.claude/dev/ci_dang_ky_test.py`) và sha256 của nó.
- H5 N2: chạy `python .claude/dev/ci_dang_ky_test.py` (KHÔNG `--chay`) trong `cay-kho` ở reviewed_sha; so với `n2_base.log`.
  Nếu môi trường thiếu thứ gì thì ghi KHÔNG ĐO ĐƯỢC + lý do, đừng suy.
- H6 Câu chữ: câu mới có đúng thể "câu có mốc", không viết lại sự thật lịch sử, không tạo khẳng định HIỆN TẠI mới sẽ cũ
  lần nữa? Write set ≤ 1 tệp, ≤ 20 dòng thêm.

## Ghi kết quả
Ghi `VERDICT.md` ở thư mục này NGAY TỪ ĐẦU (`verdict: pending`) và cập nhật sau MỖI hướng, để lượt bị ngắt vẫn còn
dữ liệu. Dạng:

```
verdict: approve | changes_requested | blocked
reviewed_sha: 67bacb3b51ac9eda72297b10b15b798b3ca51959

## BẢNG SĂN
HƯỚNG n: <tên>
  giả thuyết : ...
  lệnh       : ...
  output     : ...
  kết luận   : LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC

## FINDINGS
### <slug>  [P0|P1|P2|P3]  <tiêu đề>
TỆP/DÒNG / VẤN ĐỀ / ĐÃ THỬ NGHIỆM / ĐỘ TIN
```

`approve` chỉ khi không còn P0/P1/P2. P3 (tuỳ chọn) không chặn.
