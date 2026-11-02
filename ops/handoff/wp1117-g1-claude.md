# Handoff #1117 HARNESS-KET-QUA-NGOAI-MA-DOT-BIEN — lease wp1117-r2-g2-claude (r2)

Trạng thái lúc 04:55Z 02-11-2026: head cuối `8f0dfcf`. Lượt bỏ draft trên `6f4b889` có connector báo P2 `r4438879478`; đã vá, trả lời và resolve thread.
Trên `8f0dfcf`:
- Codex offline lượt 5/10: approve 0/0/0/0;
- connector: sạch;
- `launcher-windows.yml`: 41388160869 success;
- `ci.yml` `windows-only`: 41388158239 — CHỜ.
Phiên này không tự merge.

- Nhánh `agent/wp1117-g1-claude`, head `4a0d45d3c689600f749866f7b27e83b9d6039c00`, base `c7174bf` (master sau #1122).
- Diff: 2 tệp, +326/−85 (trần 450 của ADR-0053). Spec r2 `ops/specs/wp1117-r2.md` (sha256 `c34d5066…`).
- Lệch spec đã duyệt từ r1 vẫn áp dụng (xem mục r1 bên dưới): runner chạy từ cây harness do `_dung_cay_harness` chép.

## Codex r2 — 5/10 lời gọi (trần ADR-0055)
| lượt | head | verdict (P0/P1/P2/P3) | finding |
|---|---|---|---|
| 1 | `b6fe853` | changes_requested 0/2/0/0 | F01 `runner-stdin-khong-ghim-utf8`: runner đọc stdin theo codec của tiến trình con, nên đường kênh có dấu bị hỏng khi dùng ascii/cp1258. F02 `dot-bien-map-van-nham-ca-qua-runner`: 2 đột biến #1079 nhắm ca đã chuyển sang runner, mà ca đó không đọc map |
| 2 | `b9f010b` | changes_requested 0/0/1/0 | F03 `chot-kieu-record-chua-co-dot-bien-dung-tin-hieu` |
| 3 | `4a0d45d` | approve 0/0/0/0 | — |
| 4 | `6f4b889` | approve 0/0/0/0 | merge master `9091cf5`; `.claude/` trùng byte với `4a0d45d` |
| 5 | `8f0dfcf` | **approve 0/0/0/0** | head cuối, sau bản vá P2 connector `r4438879478` (runner giả tách stdin bằng `.split()`) |

Hiện vật nằm ở `wp1117-g1-claude/r2-luot{1,2,3,4,5}/`, mỗi thư mục có `SHA256SUMS`. `HINT.patch` của lượt 3 rỗng.

hint_provenance:
- `b9f010b`: F01 do executor tự vá (runner đọc `sys.stdin.buffer` rồi giải mã UTF-8). Ca kiểm lấy từ HINT lượt 1, có sửa
  để chạy runner của cây LỒNG, vì chỉ như vậy đột biến chép runner mới chạm tới. Thêm đột biến codec. F02 áp NGUYÊN HINT
  lượt 1.
- `4a0d45d`: áp NGUYÊN HINT lượt 2 (F03).

## Bằng chứng r2
- Linux A/B, hai vế dựng trong một lệnh, TMPDIR là `/var/tmp`, so tập theo tên:
  - `b9f010b`: suite hỏng 10 = 10; đột biến base 550/575, head 558/583; tập SAI trùng nhau (delta 0).
  - `4a0d45d`: suite có 10 ca HỎNG ở cả hai vế, cùng tên (352/362 vs 356/366); đột biến 550/575 vs 559/584, tập SAI cùng tên ⇒ delta 0.
- Windows `workflow_dispatch`:
  - `b6fe853`: 466/468, 2 SAI = F02 (run 41368402146);
  - `b9f010b`: **469/469** (run 41370605227, job `windows-latest`);
  - `4a0d45d`: success (run 41372451716).
  - `ci.yml` `windows-only` trên `6f4b889`: run 41376440756 = **success**. 16 job, mỗi job nhãn `windows-latest` và có `runner_id` khác 0. Các dòng BỎ QUA là bỏ qua theo nền, ở những bộ mà #1117 không sửa: `gate-ops` 52, `gate-registry` 20, `gate` 9, `gate-packet-loop` 9, `gate-cong-cu` 2; gate lifecycle 16/28 với 12 bỏ qua. Các bộ đều in `TỔNG: ĐẠT`; registry in `DOT BIEN: 53/53`. Bộ `launcher_test` chạy trên Windows bằng `launcher-windows.yml` với cây `.claude/` trùng byte (`4a0d45d`).
- CI trên PR #1142, head `6f4b889`: 38 success, 2 skipped, 0 failure.
- Connector Codex: `Reviewed commit: 6f4b88991b`, sạch (comment 6567483567).
- Ruff F: 5 = nền.

## Lịch sử r1 (tạm dừng 01-11)
Trạng thái lúc 16:26Z 01-11-2026: **TẠM DỪNG, CHƯA land, CHƯA có PR, CHƯA gọi Codex (0/10).** Chủ kho chọn
"Tạm dừng #1117, làm #1122 trước", vì #1122 cũng sửa `.claude/dev/launcher_test.py`. Lease đã rút hạn về
16:46Z (`thu_hoi_bang_rut_han`).

- Nhánh thi công: `agent/wp1117-g1-claude`, head `git rev-parse origin/agent/wp1117-g1-claude`, base `c82047d`.
  2 tệp: `.claude/dev/launcher_test.py` (+168/−35) và `.claude/dev/launcher_test_runner.py` (mới, 80 dòng).
- **N0 đạt** (16:18Z, base `c82047d` cộng hai ca mục 5): cả hai ca cùng ĐỎ với `('giet', 'review_target')`.
- Trên head: hai ca mục 5, ca A2 và 6 ca kênh cũ của #1079 đều xanh khi chạy `--lap-ca`. ruff F (ĐO LẠI 17:2xZ sau khi cài ruff; số "1/1" ghi trước đó là SAI — ruff chưa cài, lệnh đếm dòng `No module named ruff`) `launcher_test.py` base 5 / head 5, runner 0 — delta 0,
  `doctrine-scan` rc=0, `git diff --check` rc=0, `codex_cred_test` TỔNG: ĐẠT.
- **A5 CHƯA ĐO XONG:** suite đầy đủ và `--dot-bien` đang chạy khi tạm dừng. Phải đo lại sau khi rebase.
- **Lệch spec đã được chủ kho duyệt** ("Duyệt, ghi vào handoff"). `cham_lap_ca` chạy runner nằm TRONG
  `thu_muc`, do `_dung_cay_harness` THẬT chép vào, thay cho runner cạnh `__file__`. Lý do: chỉ cách này mới đột
  biến được các chốt bên trong runner qua `DOT_BIEN_HARNESS`. Bản sao bị đột biến sửa bước chép, nên cây lồng
  nhận runner méo. Không làm vậy thì mục 7 của spec không có răng.
- Việc còn lại: rebase lên master sau #1122, xin lease g2, đo A5, gọi Codex, mở PR draft.
