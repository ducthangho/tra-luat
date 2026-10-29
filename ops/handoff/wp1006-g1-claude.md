# Handoff wp1006 g1 — executor `claude` (phiên cloud), 29-10-2026

- Packet #1006 `T27-GLOB-HOA-THUONG` r1 · lease `ops/leases/wp1006-r1-g1-claude.yaml` @ `50ce01e` (nhánh `ops/wp1006-r1-g1-lease`,
  bản chiếu https://github.com/ducthangho/tra-luat/issues/1006#issuecomment-6489959636) · đặc tả `ops/specs/wp1006.md` @ `440e151`,
  sha256 `6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef`.
- Phiên này VỪA ghi lease VỪA thi công (`recorder_is_executor: true`), theo chỉ thị trực tiếp của chủ kho trong phiên
  `session_015GtxrYjGJtmjF3eT1nCSG9`.
- Nhánh code `claude/magical-clarke-gzvwbp` (nhánh phiên được chỉ định, thay cho `agent/wp1006-g1-claude`), PR draft #1007.
  Head **`65e623b4357906b4a2406d5923ae7e45f3eed965`**.
- Không merge/land/deploy. Không force-push, không xoá ref.

## Lịch sử nhánh
| commit | nội dung |
|---|---|
| `183e28f` | M1–M4: `_liet_ke_theo_duoi`, tách `_kiem_muc_luc`, ca phản chứng, hai biên nhận wp929, README (+ bỏ dòng trống cắt bảng cảnh báo) |
| `b1be853` | merge `origin/master` `0a8f4d7` (#994, chỉ `ops/land/**`) — `thu-hoi` đòi master là tổ tiên của head |
| `65e623b` | vá Codex lượt 1: P2 (biên nhận dẫn run.json có sẵn), P3 (khoá `is_file()` + `.RECEIPT.YAML`) |

## Đính chính tiền đề của ĐẶC TẢ (spec đóng băng, không sửa byte)
SPEC M4 viết *"không có run.json ⇒ runtime là KHÔNG_ĐO_ĐƯỢC"*. **SAI**: `ops/land/pr933-wp929-provenance/verdicts/` (vào kho ở `f46ddf5`,
tổ tiên của base) có run.json/prompt/stderr-header của cả hai lượt wp929. Codex lượt 1 bắt (P2). Biên nhận đã sửa theo thực tế: chỉ
model/effort thực phục vụ là KHÔNG ĐO ĐƯỢC (run.json không có `model_phuc_vu`). Bài học: đúng họ "hỏi chỗ TIỆN TAY" của CLAUDE.md — tôi tìm
hiện vật trong `ops/reviews/` và đọc sự vắng mặt ở đó thành "không có".

## Ngoài lệ thời gian
Sửa `ops/lease_publish_test.py` bắt đầu khoảng 06:43–06:44Z, trước `leased_at_utc` 06:45Z của lease (lease đăng 06:47Z). Commit đầu
(`183e28f`) sau mốc ấy. Ghi lại cho đúng, không che.

## Tiêu chí — đo trên head
- **A1 Linux**: `python3 ops/lease_publish_test.py --chi-ca=t27_` ⇒ `2/2 đạt`. Trước khi thêm hàng README, t27 thật ĐỎ trên Linux đúng thông
  báo của Windows (`verdict 'wp929-g1-codex-luot1-VERDICT.md' KHÔNG có trong CỘT 'tệp verdict'`) — tức Linux đã tái hiện lỗi.
- **A1 Windows**: **KHÔNG ĐO ĐƯỢC.** `workflow_dispatch` (runner_set windows-only) run 40833816523 trên `65e623b`: `gate-ops (windows-latest)`
  ĐỎ ở bước `bien-nhan v2 selftest` (`90/93`), bước `lease-publish selftest` (chứa t27) nằm sau nên không chạy. Lỗi ấy KHÔNG của PR:
  `ops/bien_nhan_v2*.py` giống byte master `0a8f4d7` (blob `83ba1d3`/`86959ff`); ca `c96_git_rc_LA_ma_stderr_RONG_van_la_KHONG_DO_DUOC` dựng `git`
  giả bằng `#!/bin/sh` không phần mở rộng, Windows không chạy được qua PATH ⇒ `git.exe` thật trả rc=1 thay vì 3. Phần test ấy vào master qua
  #995 (wp960 r2) và chưa từng chạy Windows (run gốc 40812761896 trên `dd877da`, trước #995). Comment trên PR: issuecomment-6490910747.
- **A2** đột biến trên bản sao tạm (`PYTHONDONTWRITEBYTECODE=1`), chạy `--chi-ca=t27_phan`, đọc thông báo:

  | đột biến | kết quả | chốt bắt |
  |---|---|---|
  | (a) `_liet_ke_theo_duoi` → `glob("*" + duoi)` | ĐỎ (và t27 thật thành XANH mù) | `bộ liệt kê không thấy đủ cả hai cách viết đuôi` |
  | (b) (a) + vô hiệu chốt tự kiểm bộ liệt kê | ĐỎ | `verdict đuôi -VERDICT.md vắng khỏi mục lục mà _kiem_muc_luc vẫn XANH` |
  | (c2) bỏ `is_file()` | ĐỎ | `bộ liệt kê nhận cả THƯ MỤC mang đuôi verdict` |
  | (c4) `_kiem_muc_luc` dùng `glob("*.receipt.yaml")` | ĐỎ | `biên nhận đuôi .RECEIPT.YAML vắng khỏi mục lục mà _kiem_muc_luc vẫn XANH` |

- **A3** `python3 ops/lease_publish_test.py` ⇒ `268/268 đạt; bỏ qua=0`, rc=0 (container đã cài `shellcheck` 0.9.0 — thiếu nó thì t137/t159
  `KHÔNG ĐO ĐƯỢC`, không liên quan bản vá). `ops/bien_nhan_v2.py --root .` ⇒ `246 ĐẠT v2 · 0 vi phạm · TỔNG: ĐẠT`.
- **A4** ruff F base/head cùng 7 F401 + 2 F541 ⇒ delta 0 · `git diff --check` rc0 · `doctrine-scan` rc0.
- **A5** CI lượt PR (Ubuntu) run 40833813717 trên `65e623b`: `gate-ops (ubuntu-latest)` (gồm lease-publish selftest), `gate`, `gate-cong-cu` 0–7,
  `gate-nhanh-*` xanh; `gate-registry`/`gate-packet-loop` lúc ghi còn chạy. Đọc lại bằng check run trước khi báo đủ điều kiện.

## Cross-review Codex — 2/2 lời gọi (trần lease M-1)
Qua `.claude/dev/launcher.py run --expected-repo github.com/ducthangho/tra-luat --expected-head <H> --require-clean --prompt-file …`,
`codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh --sandbox workspace-write`. Sandbox: clone thường detached + SPEC + diff, không mạng.
Hiện vật nguyên byte ở `ops/handoff/wp1006-g1-claude/` (SHA256SUMS kèm).

| lượt | run_id | head | thời lượng | model_phuc_vu (do_may) | verdict | sha256 verdict |
|---|---|---|---|---|---|---|
| 1 | `ee63cae14a964b1a8686fcfb2005b06a` | `183e28f` | 990.184 s, rc0 | `gpt-6-astra` 24/24 khung, effort `xhigh` | request_changes (1 P2, 1 P3) | `f05e7166…732fcb` |
| 2 | `5f67e45bdfaa40f0ae925cb88b4ad039` | `65e623b` | 865.934 s, rc0 | `gpt-6-astra` 24/24 khung, effort `xhigh` | **approve** (0/0/0/0) | `92d473e8…f3c01c` |

- Lượt 2 tự khai bề mặt `codex_service`; run.json ghi `execution_surface: codex_cli`. Đây là dương tính giả đã biết của L-SURFACE (#960):
  run.json là nguồn. Nếu ghi biên nhận cho hai verdict này sau, phải kèm caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE`.
- Verdict để ở `ops/handoff/` chứ KHÔNG ở `ops/reviews/`: đặt verdict vào `ops/reviews/` mà thiếu biên nhận + hàng mục lục sẽ tái tạo đúng lỗi
  wp929 (t27 đỏ). Thư mục hiện vật này ngoài write set nguyên văn (write set khai một tệp handoff); tiền lệ wp929 để verdict trên nhánh lease.

## Quan sát (ghi, KHÔNG vá — ngoài write set)
1. `ops/bien_nhan_v2_test.py` ĐỎ trên Windows (c96 và hai ca khác, 90/93) — git giả `#!/bin/sh`. Chặn mọi phép đo t27 Windows qua `gate-ops`.
2. `ops/bien_nhan_v2.py:1442,1601` cũng `glob("*.receipt.yaml")` — cùng bệnh phụ thuộc nền với t27 (hiện mọi biên nhận đuôi thường nên chưa lộ).
3. `ops/lease_publish_test.py` còn `goc.glob("*.yml")`/`("*.yaml")` cho workflow (dòng 2303, 2525 trên head `65e623b`) — cùng lớp, chưa lộ.
4. Bảng cảnh báo README trên master có một dòng trống cắt bảng (ba hàng không render). PR này bỏ dòng ấy; không có chốt nào canh việc bảng
   bị cắt (t27 chỉ thấy hàng nằm trong bảng đọc được).

## Việc còn lại
- A1 Windows: cần sửa `bien_nhan_v2_test` trên Windows (packet khác) rồi gọi lại `workflow_dispatch`; hoặc chủ kho chọn cách đo khác.
- Merge/land: chủ kho. `uy_quyen_merge: false`.
