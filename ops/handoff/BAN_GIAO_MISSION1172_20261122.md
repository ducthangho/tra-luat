# Bàn giao Mission #1172 — phiên điều phối Claude Code → Codex (22-11-2026, ~02:50Z)

Phiên giao: `https://claude.ai/code/session_015Gtxrb3cuZ7Nm935R8yA5W` (Claude Code, vai **điều phối**; không phải executor, không phải
reviewer của packet nào). Tệp này là **dữ liệu bàn giao**, KHÔNG phải lease và KHÔNG giao việc (protocol §7). Quyền làm việc vẫn chỉ đến từ
Packet Issue + lease còn hiệu lực + quyết định chủ kho ghi trên #1172.

Nguồn quy tắc: `docs/PROTOCOL_DA_PHIEN.md` (đọc §3.2, §4, §7, §8, §8.1–§8.3, §10.2.2, §10.2.4, §12, §20). Kế hoạch:
`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md` trên nhánh này (cài ở Mission r83). Mission revision mới nhất: **r96**
(`ops/specs/wp1172-source-plan-r4/mission-r96.json`, comment #1172 `7066078931`).

## 0. ĐỌC TRƯỚC — quyết định chủ kho phải có trước khi Codex làm tiếp

1. **Đổi nền điều phối/executor sang Codex là quyết định của chủ kho, chưa được ghi.** Suốt Mission #1172, Codex (`gpt-6-astra`,
   `model_reasoning_effort=xhigh`, qua `.claude/dev/launcher.py run`) là **reviewer độc lập**; Claude Opus là executor/tác giả spec. Nếu
   Codex nay vừa soạn/thi công vừa review thì mất tính độc lập (§8, `independent_from_executor_session`). Cần một Mission revision ghi:
   ai là executor, ai là reviewer (vd. đổi chiều: Codex thi công, Claude Opus review), và lease mới cho từng packet đổi provider.
   Lease hiện hành đều ghi `provider: claude`.
2. Mọi Mission revision / spec mới cần **chủ kho duyệt băm** trước khi cài/cấp lease (revision chỉ-ghi-sổ được miễn).
3. Chủ kho tự bấm merge; chủ kho tự audit exact-H (`human_exact_head_audit.v1`) **trước lần đẩy đầu tiên của H**; điều phối không ký,
   không tự approve. Nhãn audit uỷ quyền là `owner_delegated_audit`, không bao giờ `human_audited`.
4. Không Windows CI. K6 = dòng chủ kho `windows: <H> mien` hoặc đo trên máy Desktop của chủ kho (DESKTOP-T9R33P2, `F:\tl-verify-<pkt>\`).
5. Không bao giờ viết nguyên văn dấu bỏ-qua-CI trong commit message. `core.abbrev 7` khi chạy gate.
6. Không đọc/in giá trị bí mật; `TL_MASTER_KEY` không đi qua phiên cloud; không xoá tài liệu khoá cũ, `NEW-MASTER-KEY.txt`, `rekey-backup`.

## 1. Bảng trạng thái packet (thứ tự kế hoạch r4 §7: PR1 → B1 → B2 → PR2 → B4 → PR3 → B3 → PR4…)

| Packet | Issue | Nhánh điều phối (đầu) | Trạng thái | Việc kế tiếp |
|---|---|---|---|---|
| PR1 `wp1448` | #1448 | `ops/wp1448-r1` @ `ec72955` | **merged** `e2f28fb3` (PR #1492). Hồ sơ `landed: true` ở **PR nháp #1497** (nhánh `ccr-a1ff05af-u99yr7`) | Chủ kho merge #1497; sau đó đăng M8 mới trên #1448 trỏ hồ sơ, thay M8 cũ `7065823063` |
| B1a `wp1460` | #1460 | `ops/wp1460-r1` @ `163ece8` | spec r7 đóng băng (`d53341fb…`), admitted có điều kiện (r91) | Chờ lease `wp1236-a-r12-g1-claude-20261121` nhả `.claude/dev/ci_dang_ky_test.py` (hạn **2026-11-23T13:45Z**) + slot writer → cấp lease, thi công |
| B2 `wp1494` | #1494 | `ops/wp1494-r1` @ `8c68b39` (+ commit hồ sơ review của bàn giao) | spec r4 `SPEC.md` sha256 `22d6a09277509c5462c955278da03696c6931ea8aa9fbcfe349df73c9e451740`; **review 5 APPROVE, 0 phát hiện** | Chủ kho duyệt băm spec r4 → Mission revision cài spec → lease (sau khi wp1236 nhả `ci_dang_ky_test.py`) |
| PR2 `wp1463` | #1463 | `ops/wp1463-r1` @ `05a073f` | spec **r5** sha256 `3ac18bc62a6bc7ecbf372d1ec3d60dbca183495a83e59e41c0a5400a05bf2d5d`; tác giả **5/5 (hết)**; review 4/6 xong, **review 5 ĐANG CHẠY** lúc bàn giao (run `d9764a9f`) | Đọc verdict lượt 5 (xem §3). Approve ⇒ chủ kho duyệt băm. Còn phát hiện ⇒ cần chủ kho cấp thêm lượt soạn (E2) |
| B4 `wp1462` | #1462 | `ops/wp1462-r1` @ `371e9ed` (+ bàn giao) | spec r9 `e14926d5…`; lease `wp1462-r9-g3-claude` (hạn 2026-11-26T08:00Z); thi công attempt **4/4** = `724993bf23f16070f272ccd81b4fe16c111ce2eb` (+1556/−3, tree `75bd0a3b`); source review **5/5** dùng hết (owner +1 hai lần) — lượt cuối 3c **ĐANG CHẠY** (run `a0f70f4b`) | Xem §2 |
| B3 `wp1461` | #1461 | `ops/wp1461-r1` @ `1a8bbc3` | spec r9 đóng băng (`9066a4c6…`), **chưa admitted** | Chờ thứ tự kế hoạch |
| PR3, PR4… | — | — | chưa mở | — |

Lease chặn đang sống (đo `ai-dang-giu` 02:40Z): `wp1236-a-r12-g1-claude-20261121` (Mission #1236) giữ `.claude/dev/ci_dang_ky_test.py` tới
2026-11-23T13:45Z (chặn B1a, B2, PR2 thi công); `wp1475-r1-g1-claude` giữ `ops/ci_provenance.py`, `ops/ci_provenance_test.py` tới
2026-11-23T01:57:05Z.

Nợ đã ghi (M8 PR1): PR1b thiết kế lại G5 thời gian; `thu_thap` Windows mutant WinError 32; `lease_publish check` không bắt `spec_ref` OID ngắn.

## 2. B4 (`wp1462`) — chi tiết vì nó gần land nhất

- **Commit thi công KHÔNG nằm trên nhánh remote nào** (chưa được đẩy vì quy ước audit exact-H trước lần đẩy đầu). Bản giữ nguyên SHA:
  `ops/specs/wp1462-r1/handoff/attempt4-724993b.bundle` trên nhánh `ops/wp1462-r1`. Khôi phục:
  `git fetch origin master && git bundle verify <bundle> && git fetch <bundle> refs/heads/agent/wp1462-r9-g3-opus:refs/heads/agent/wp1462-r9-g3-opus`
  ⇒ đầu nhánh phải đúng `724993bf23f16070f272ccd81b4fe16c111ce2eb` (tiền đề: `48d372e1…` trên master).
- Handoff executor: `handoff/HANDOFF-attempt{1..4}.yaml` (attempt 4 sha256 `946895b6…`, comment #1462 `7067119801`).
- Source review: 1 (1 P1 + 4 P2) và 2 (P1 VÁ HỜ + 2 P2 + P3) trong `handoff/source-reviews/`. Lượt 3 bị chặn HAI lần do lỗi phía điều phối
  (chuỗi danh tính cũ; origin của clone reviewer là mirror cục bộ) — hồ sơ `codex-source-review-3-blocked*.json`; chủ kho +1 hai lần
  (ghi hộ `7071993377`, `7072684185`) ⇒ trần 5. Lượt 3c (prompt `PROMPT-wp1462-source-review-3c.md`) là lượt cuối.
- **Nếu 3c approve:** (1) lease mới với `spec_ref` OID40 `refs/heads/ops/wp1462-r1@f5b0ff18671abd2d69038fad8cc368dcecac0ce8` (lease g3 ghi OID
  ngắn `f5b0ff1` ⇒ `kiem-merge` K1 sẽ ĐỎ — đúng sự cố của PR1); (2) chủ kho audit exact-H (packet `wp1462`, revision 9, generation đúng lease,
  `review_axes [spec, standards_security]`, `audit_source` = URL comment) **trước** khi đẩy H; (3) đẩy H lên `agent/wp1462-r9-g3-opus`,
  mở PR nháp; merge master vào nếu cần (H đổi ⇒ audit lại); (4) CI PR, K7 (`ci-dot-bien-du.yml` success trên đúng H), connector, K6;
  (5) `python .claude/dev/packet_loop.py kiem-merge …` rc 0; (6) chủ kho merge; (7) M8 + rút hạn lease + hồ sơ land như PR #1497;
  (8) báo SHA merge B4 cho phiên ADR-0068 `session_015GtxrcdabvDuhzgezMEE89`.
- **Nếu 3c còn phát hiện:** ngân sách executor 4/4 và source review 5/5 đều hết ⇒ Review Rescue Checkpoint (§12): dừng, hỏi chủ kho (E2).

## 3. Các lượt đang chạy trong container của phiên giao

Ba lượt Codex chạy NỀN trong container cloud của phiên Claude Code. Kết quả chỉ ở scratchpad của container ấy cho tới khi được commit:

| Lượt | run_id | Đầu ra (trong container) |
|---|---|---|
| B4 source review 3c | `a0f70f4b` | `scratchpad/rv1462/codex-source-review-3.json` |
| PR2 spec review 5 | `d9764a9f` | `scratchpad/rvspec/wp1463-spec-review-5.json` |
| (đã xong) B2 spec review 5 | `4f9faea5` | đã commit: `ops/specs/wp1494-r1/reviews/wp1494-spec-review-5.json` |

Phiên giao sẽ commit hai kết quả còn lại vào `ops/specs/wp1462-r1/handoff/source-reviews/` và `ops/specs/wp1463-r1/reviews/` khi chúng
xong, nếu container còn sống. **Codex: trước khi chạy lại, `git fetch` hai nhánh ấy và tìm tệp — chạy lại khi tệp đã có là tiêu một lời gọi
Codex vô ích và vượt trần.** Không thấy tệp ⇒ hỏi chủ kho trước khi chạy lại (mỗi lời gọi có output đều tính vào trần ADR-0052/0055).
Lượt `9337722b` (B2) là lần khởi chạy nhầm băm spec bị cắt, bị dừng sau vài giây, **không sinh output** ⇒ không tính trần; giữ `run-9337722b.json` làm vết.

## 4. Ngân sách đã dùng (đếm tới lúc bàn giao)

- PR2 `wp1463`: lượt soạn spec 5/5 (hết); review spec 5/6 (lượt 5 đang chạy).
- B2 `wp1494`: lượt soạn spec 4/5; review spec 5/6 (lượt 5 approve).
- B4 `wp1462`: executor 4/4; source review 5/5; trần Codex/PR 10 (dòng `tran_loi_goi_codex: ADR-0055@d2e3052d…` trong spec).
- PR1 `wp1448`: đóng.
Đếm lời gọi Codex TRƯỚC mỗi lời gọi; vượt trần ⇒ dừng, xin `nang_tran` trước (bài học CLAUDE.md "TRẦN LỜI GỌI CODEX").

## 5. Cách chạy review như phiên giao đã làm

- Spec review: `ops/handoff/spec_review.sh` (bản chép script phiên giao). Cách gọi:
  `spec_review.sh PKT BRANCH HEAD SPECSHA ROUND [NOTE_FILE]`. Script clone, đặt `origin` về GitHub thật (§8.1), fetch ĐỦ ref
  (`+refs/heads/*`), `git branch -f master origin/master`, rồi chạy `launcher.py run … -- codex exec -m gpt-6-astra -c model_reasoning_effort=xhigh`.
  Đường dẫn scratchpad trong script là của container cũ — sửa biến `S` trước khi dùng.
- Kiểm verdict: `ops/handoff/kiem_verdict_lop.py <verdict.json> --vong N` (dạng §8.3). Báo `thiếu prior_findings_check` khi lượt
  trước có 0 phát hiện là cảnh báo hình thức, không phải lỗi verdict.
- Prompt reviewer: bảo reviewer CHẠY các ca đã commit và đột biến bản vá, **mô tả** đầu vào thù địch bằng lời — đừng để reviewer tự soạn
  payload tấn công (bộ lọc an ninh của nền sẽ cắt lượt).
- Lease probe trong sandbox reviewer có thể ra rc 12 (không fetch được). Điều phối chạy `ai-dang-giu` trên clone đủ ref rồi đính output vào prompt.

## 6. Mốc tham chiếu nhanh

- master: `e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8` (merge PR1).
- Mission revisions r89–r96: `ops/specs/wp1172-source-plan-r4/mission-r89.json` … `mission-r96.json` (comment #1172 tương ứng ghi trong từng tệp).
- Quyết định chủ kho: comment "Quyết định chủ kho — ghi hộ" trên #1172 (nguyên văn câu trả lời + ngữ cảnh + readback).
- Ủy quyền tự quyết: mục `uy_quyen_quyet_dinh.v1` trên Packet Issue; chỉ hỏi chủ kho các mã ADR-0067 E1–E5 (gắn mã).
- Sao lưu Drive ở mỗi mốc (script cũ `backup_drive.sh` trong scratchpad, không chép theo vì chứa đường dẫn container).
