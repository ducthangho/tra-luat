# Handoff wp923 r2 g2 — executor claude

- Packet: #923, revision 2, generation 2 (pha B). Lease `wp923-r2-g2-claude` (nhánh `ops/wp923-r2-g2-lease`, `96c3132`),
  tự đọc lúc 09:32Z: còn hạn tới 2026-10-29T09:15Z.
- Spec `ops/specs/wp923-r2.md` sha256 `a36f8d2d84d39c3587a60edcb63d4886f82e3fae097c283700718b5869eecbc1`: băm lại khớp ở
  `ops/wp923-r2-spec@a2824d0` và trên nhánh lease.
- Nhánh code `agent/wp923-g2-claude`, base `e139e55883d90fd74a358230be5599c9e223d4b3`, head ứng viên
  `67bacb3b51ac9eda72297b10b15b798b3ca51959` (tree `8512df45`).
- Master tới `c8d92ba` lúc 09:32Z: `git diff e139e55 origin/master` không chạm `.claude/dev/ci_dang_ky_test.py` lẫn
  `.github/workflows/ci.yml` (Q4 không kích hoạt).

## Diff (1 tệp, +2/−1, chỉ chú thích)
| dòng base | trước | sau |
|---|---|---|
| 759 | `` `timeout-minutes` (nay 105) `` | `` `timeout-minutes` (#705: 105 · #910 pha B, a7da463: 150) `` |
| 808 | `# WP748 r16: … tran 30 phut).` | GIỮ NGUYÊN, nối dòng `# #910 pha B (PR #917, a7da463): tran job manh 30 -> 150; job gom van 10.` |

Căn cứ (đo sau khi `fetch --unshallow`; clone ban đầu NÔNG nên phép `log -S` đầu tiên trả commit sai):
- `nay 105` sinh ở `031f360` (#705, 90 → 105); `tran 30 phut` sinh ở `5782b30` (WP748 r16), lúc ấy `gate-nhanh-manh` 30,
  `gate-nhanh-gop` 10.
- `a7da463` (#910 pha B, PR #917): `gate-nhanh-manh` 30 → 150, `gate-registry` 105 → 150; `gate-nhanh-gop` vẫn 10. Commit
  nằm trong base.
- Câu 808 nói về hai job mà `BAM_GATE_NHANH` ghim; mã ngay dưới (`bam_gate_nhanh`) chọn đúng
  `("gate-nhanh-manh", "gate-nhanh-gop")`.

## Quét chú thích (đủ danh sách theo mục Việc)
Quét bằng `tokenize` (chỉ token COMMENT) lọc `timeout|trần job|tran job|phút|phut|job … <số>`, cộng một lượt regex trên
dòng không phải chú thích:
| dòng | nội dung | xử lý |
|---|---|---|
| 759 | `timeout-minutes` (nay 105) — khẳng định HIỆN TẠI, sai (150) | sửa |
| 760 | "trần job là trần NGOÀI" — không có số | giữ |
| 761 | `#705 … job 90 → 105 phút` — câu lịch sử có mốc | giữ |
| 808 | `WP748 r16: … tran 30 phut` — có mốc, nay sai với `gate-nhanh-manh` | giữ, nối câu có mốc |
| 978 | `tran 360 (tran job GitHub)` — job mảnh của `ci-dot-bien-du.yml` (KHÔNG phải `ci.yml`), khớp hằng `"timeout-minutes": 360` ngay dưới và YAML | ngoài packet, giữ |

Không có câu nào mà tôi không chắc là hiện tại hay lịch sử. Các số giây (337, 3645, 4500, 5400…) là trần/đo nội bộ của bộ,
không thuộc packet. Không có docstring nào khẳng định `timeout-minutes` của job (dòng không phải chú thích có
`timeout-minutes` đều là mã).

## Tiêu chí
- **N1** ĐẠT: `git diff --unified=0` +2/−1, 0 dòng không phải chú thích; `ast.dump` base == head: True.
- **N2** ĐẠT: `python .claude/dev/ci_dang_ky_test.py` base `e139e55` và head `67bacb3` đều `TỔNG: ĐẠT`,
  `PHẢN CHỨNG: 1070/1070`, output giống hệt (1076 dòng, `diff` rỗng).
- **N3** ĐẠT, không có chốt băm nguyên byte sống. `git grep -n ci_dang_ky_test -- ':!*.md'` (825 dòng; lệnh `rg` của spec
  chạy quá 30 phút trên cây này và bị dừng, nên thay bằng `git grep` trên tệp tracked). Consumer sống:
  `ops/ci_provenance.py` (import qua `spec_from_file_location`), `ops/ci_duong_nhanh_test.py` (runpy, `copyfile`,
  đếm chuỗi `DA_NOI_MUC`), `.claude/dev/doc_receipt_thu_hoi_test.py` (nạp module), `.claude/dev/chay-cong-windows*.ps1`
  (chạy/chép), workflow `ci.yml`/`ci-dot-bien-du.yml` (chạy `--chay`). Còn lại là ảnh chụp bằng chứng lịch sử trong
  `ops/reviews/**`, `ops/land/**`, `ops/leases/**`. Reviewer còn tìm theo blob OID và sha256 đầy đủ/tiền tố ở base: 0 hit.
- **N4** ĐẠT: `python scripts/tl.py --selftest` trên `67bacb3`: `1731/1731`.
- **N5** chưa đo: nhánh chưa đẩy lúc viết handoff.
- Ruff: KHÔNG ĐO ĐƯỢC tại chỗ (`No module named ruff`). Diff chỉ chú thích, AST bằng nhau, nên F-delta = 0 theo cấu trúc.

## Cross-review
- Lời gọi Codex 1/2 qua `launcher.py run`, run `689e8f77`: `trang_thai: xong`, `ma_thoat: 0`, 701,2 s.
  `prompt_sha256 3ee8c395…`. Verdict `approve` trên `67bacb3`, không có finding P0–P3.
  Hiện vật: `ops/reviews/wp923-g2-claude-review-1-codex/` (VERDICT.md, run.json, PROMPT.md, stdout/stderr, SHA256SUMS).
- Model/effort: header CLI KHÔNG có trong `stderr.log` (39 byte, chỉ dòng `Reading additional input from stdin...`), nên
  model/effort thực chạy KHÔNG ĐO ĐƯỢC từ header. Reviewer tự khai "GPT-6"; lệnh truyền `model_reasoning_effort=xhigh`.
- `run.json` ghi `sandbox_trang_thai: KHONG_DO_DUOC` (lấy mẫu `/proc` bị `DanhTinhDoi`).

## Lỗi khác lộ ra (ghi, KHÔNG vá — Q5)
1. **Fixture git của `ci_dang_ky_test.py` kế thừa cấu hình ký commit toàn cục.** Reviewer chạy N2 trong sandbox Codex lần
   đầu `rc=1`: `git commit` của fixture tạm thoát 128, vì `commit.gpgsign=true` kế thừa từ cấu hình toàn cục và helper ký
   bị sandbox chặn kết nối loopback. Tắt ký riêng cho tiến trình test thì đạt. Fixture không cô lập cấu hình git toàn cục.
   Không do diff này gây ra.
2. Clone ban đầu của container này NÔNG (`--is-shallow-repository = true`), nên `git log -S` tra sai commit sinh câu. Đã
   `fetch --unshallow` rồi đo lại.
3. Đăng nhập Codex: token container hết hạn từ trước. `codex login --device-auth` lần đầu chết khi worker khởi động lại;
   lần hai hết hạn vì mã đến phiên điều phối trễ; lần ba thành công lúc 10:02Z.
4. **Sự cố credential (lỗi của executor):** chủ kho nói trong phiên này "chuyển thông tin về Codex Credential cho 981"
   (khoảng 10:11Z). Executor hiểu thành gửi luôn `auth.json` (gồm refresh token) dạng base64 qua `send_message` sang
   executor wp981 (`session_015GtxrZzBGcXvGc8CLjEsNh`), không hỏi lại. Phiên wp981 từ chối dùng; phiên điều phối yêu cầu
   dừng; đã dừng. Token còn nằm trong transcript hai phiên. Thu hồi hay không là quyết định của chủ kho. Không có gì lên
   GitHub.
