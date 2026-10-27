# Handoff wp943 r1 g1 — executor claude

- Packet: `wp943`, Issue #943, revision 1, generation 1. Lease `wp943-r1-g1-claude` (`ops/wp943-r1-g1-lease@ab75b66`),
  hạn `2026-10-28T12:53:00Z`, `heartbeat_required_minutes: 30` (không đổi).
- Đặc tả: `ops/specs/wp943.md` @ `ops/wp943-spec@80ebcfb`, sha256 `22729e93eec0e1c4677a5d6529b81f9f0c46c47f3f605017b7abb337b5e1e270`
  (băm lại bằng `git show … | sha256sum`, khớp).
- Phiên executor: `session_01Mr84zPTvmQhhshvV6Q88vq`. Phiên giao việc: `session_01FLVLxi5gKZgtVvbuTCEqEn`.
- Nhánh code: `agent/wp943-g1-claude`, rẽ từ `3e973a03b151e37cd402e0a723816eeaa8247193`, head `eb5e5bf119358babf831d2aec0ee27c7e5896c1f`.
  Đẩy MỘT lần. PR draft #963.
- Q4: `git log 3e973a0..origin/master -- <write set>` (origin/master `f577ab5`, kho đã unshallow) ⇒ 0 commit. Không áp Q4.

## Preflight và xác thực Codex
1. Lần đầu (00:21Z): `CODEX_AUTH_JSON` vắng; `~/.codex/auth.json` có refresh token đã bị thu hồi
   (`codex exec` thăm dò: `refresh token was revoked`, 401). DỪNG trước khi sửa, báo #943 issuecomment-6430570920.
2. Mở lại theo chỉ thị chủ kho ghi hộ ở #943 issuecomment-6432439309: `codex login --device-auth` trong container.
   Mã thứ nhất hết hạn 15 phút mà chưa ai nhập; mã thứ hai được nhập, tiến trình thoát rc 0 lúc 03:04Z.
   `doctor --kiem-song` ⇒ codex `DUNG_DUOC`, có `TRALUAT-CRED-OK`. URL/mã chỉ gửi qua send_message, không lên GitHub.

## Diff (2 tệp, +12/−5; trần ≤ 2 tệp, ≤ 80 dòng thêm)
Hunk (N4):
- `docs/adr/0056-lease-no-progress-six-hours.md` `@@ -3,8 +3,10 @@` — M1 *Trạng thái*: `CHƯA KÍCH HOẠT VẬN HÀNH …` ⇒
  `ĐÃ KÍCH HOẠT VẬN HÀNH`, mốc = merge của PR thi công wp943 (không ghi SHA/giờ), căn cứ #835 issuecomment-6407154789
  + quét mã của mục *Hiệu lực*, thi hành bằng wp943.
- `docs/adr/0056-lease-no-progress-six-hours.md` `@@ -34,8 +36,13 @@` — M1 *Hiệu lực*: giữ đoạn đo 19-10/25-10; thay câu
  "Controller ngoài … chưa đo được …" bằng đoạn mốc 26-10-2026 + luật áp dụng (chỉ lease cấp SAU mốc khai 360; lease
  cấp trước giữ byte và số, kể cả `wp943-r1-g1-claude` khai 30).
- `docs/PROTOCOL_DA_PHIEN.md` `@@ -1532,7 +1532,7 @@` — M2: dòng §20 `ADR-0056`, cột trạng thái ⇒ "Accepted — đã kích
  hoạt vận hành (merge PR thi công wp943)", cột cổng thêm "không có controller ngoài, phiên điều phối áp tay".
- §4: **giữ nguyên**. Dòng 271 và câu ~283 ("chỉ áp cho lease MỚI cấp sau khi `ADR-0056` kích hoạt vận hành") vẫn
  đúng sau kích hoạt. Phần §4 của #834 (cửa `accept`) không đụng; reviewer lượt 1 đo §4 bằng byte giữa base và head.
- Không đổi: số 360, *Những gì KHÔNG đổi*, *Không hồi tố*, *Vì sao sáu giờ*, ADR khác, dòng §20 khác, lease, code,
  `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json`.

## Tiêu chí hoàn tất
- **N1** `python .claude/dev/packet_loop.py adr-song --root .` rc 0 (`55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1`);
  `doctrine-scan --root .` rc 0 (`10 tệp, 0 chỗ chép doctrine`); `git diff --check` rc 0.
- **N2** trên `eb5e5bf`: `python scripts/tl.py --selftest` ⇒ `== tl selftest 1731/1731 ==`, rc 0.
  `doc-claims-check --strict --json` ở base `3e973a0` và head: cả hai rc 0, `ok: true`, `flags: 0`,
  `advisories: 379`, `files_scanned: 115` ⇒ delta 0.
- **N3** lệnh: `rg -n "CHƯA KÍCH HOẠT VẬN HÀNH|chưa kích hoạt vận hành" docs/adr/0056-* docs/PROTOCOL_DA_PHIEN.md`
  output: rỗng, rc 1.
- **N4** xem danh sách hunk ở trên.
- **N5** check run `ci.yml` trên PR #963: ghi ở comment kết quả trên #943 khi xong.

## Cross-review Codex (lớp sensitive; trần 2 lời gọi; đã dùng 2/2)
| lượt | thư mục | kết quả | ghi chú |
|---|---|---|---|
| 1 | `ops/reviews/wp943-g1-review-1-codex/` | bị cắt, không verdict | container khởi động lại ~03:16Z; `run.json` còn `dang_chay`, `ma_thoat: null`. `VERDICT.partial.md`: 7 hướng săn, cả 7 KHÔNG PHẢI LỖI. Tính 1 lời gọi (đã sinh output). |
| 2 | `ops/reviews/wp943-g1-review-2-codex/` | **approve**, 0 finding P0–P3, `reviewed_sha` `eb5e5bf` | `run.json` `xong`, `ma_thoat: 0`, 1147 s; `model_phuc_vu` = `gpt-6.1-sol` (`DO_DUOC`, 41 response), effort yêu cầu `xhigh`. 6 hướng săn mới (H8–H13). |

Lượt 2 chạy selftest độc lập trong sandbox ⇒ `1729/1731`, rc 1. Hai ca đỏ là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`
và `r268_l2_trichotomy_theo_trang_thai_object`; cả hai dựng kho Git tạm và lệnh commit fixture trả rc 128 vì cấu hình
ký Git của sandbox. Reviewer tái hiện y hệt trên base, nên ghi là giới hạn hạ tầng, không phải finding. Bằng chứng
N/N còn lại là lần chạy của executor trên cùng commit.

Băm prompt: lượt 1 `5b3a09c5…0772`, lượt 2 `217924c1…46c2` (khớp `prompt_sha256` trong `run.json`).

## Lỗi khác lộ ra (Q5 — ghi, KHÔNG vá)
- Hai ca selftest ở trên đỏ trong sandbox Codex có ký commit bắt buộc; ca nên tắt ký trong kho tạm (`-c commit.gpgsign=false`)
  để không phụ thuộc cấu hình ký của máy. Chưa đo trên máy khác; thuộc packet khác.
- `launcher.py run` để lại `run.json` `dang_chay` sau khi container chết (đã biết, adapter cross-review có ghi).

## Trạng thái
Chờ CI trên PR #963 và chủ kho duyệt. Không merge/land/deploy. Không còn lượt Codex: sau approve không đẩy thêm
merge commit.
