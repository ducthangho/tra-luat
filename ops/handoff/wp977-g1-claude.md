# Handoff — wp977-r1-g1-claude (`MAY-ADR-0054-b2`), packet #977 r1 g1

Trạng thái (27-10 ~17:35Z): **đã đẩy `agent/wp977-g1-claude` một lần tại head `4c73081474b1e2ab0800cc13992c8f86688532ed`**
sau Codex lượt 5 approve; PR draft mở, đang chờ CI (ci.yml + thu-hoi) và connector Codex. Merge/land do chủ kho.

- Đặc tả `ops/specs/wp977.md` @ `ea34f2d` sha256 `adaf8d24…40c3`; phần chung `ops/specs/may-adr-0054-chung.md` sha256 `4e3d1e1b…bf0`
  (băm lại khớp). Lease `wp977-r1-g1-claude` (hạn 2026-10-29T09:30Z).
- Nhánh rẽ từ `e139e55`. Commit nội dung duy nhất `8770ab3`; sau đó năm merge `origin/master` (không rebase) vì master tiến:
  `09db703` → `7f19424` → `4488444` → `c2d84ea` → `b3decc5` → `ef34d88`.
- Diff so `origin/master` `ef34d88`: `docs/PROTOCOL_DA_PHIEN.md` 19+/2− — đúng 1 đường dẫn, ≤ 40 dòng thêm. Blob tệp
  `a8f689d11b2eab370de68d6dc197a97f72420e94` không đổi qua mọi merge.

## Việc đã làm

- **M1** — §4, ngay sau đoạn `approved_pending`: một đoạn văn xuôi mô tả `mo-lai` (`ci-do` ⇒ `running`; `connector` ⇒ `cho_chu_kho`;
  `connector` từ `running` khi quyền mở lại hiện hành là `ci-do` cùng generation, chưa có `begin_attempt` sau `mo_lai` cuối, xét
  trên SHA đã mở lại), quyền `mo_lai_tu` và bộ đếm same-failure; `cho_chu_kho` không có cạnh `transition`, chỉ rời bằng
  `chu-kho-duyet` (`cho_phep_va`, checkpoint trên `origin/master` sau fetch + `ls-remote`); `cho_phep_day` chỉ ghi `checkpoint_day`,
  state giữ nguyên, chưa có cửa tiêu thụ (#816); dùng một lần theo cặp (hiện vật, phạm vi); `mo-lai`/`chu-kho-duyet`/`begin-attempt`
  qua `_xet_dung`. Packet chưa áp `ADR-0054` không có các state/cửa này.
- **M2** — §12: câu chặn mission complete thêm `approved_pending` và `cho_chu_kho`.

## Đối chiếu đặc tả với code hiện hành (master, `packet_loop.py` không đổi từ `e139e55` tới `ef34d88`)

Từng mệnh đề neo vào `cmd_mo_lai`, `cmd_chu_kho_duyet`, `_xet_dung`, `CUA_DI_TIEP`, `CHUYEN_HOP_LE`. Đã rà mọi cửa ghi `state`:
từ `cho_chu_kho` chỉ `chu-kho-duyet` ghi state (về `running`, hoặc `blocked` qua `_xet_dung`); `record-codex-call` đòi `reviewing`;
`transition` không có cạnh. `checkpoint_day` không có chỗ đọc ngoài bất biến `_load`. Không mệnh đề nào bị bỏ; không cần hỏi chủ kho.
Codex lượt 1 đối chiếu độc lập từng mệnh đề (file:dòng) và rà mọi cửa ghi state: khớp hết.

## Nghiệm thu

- `rg 'cho_chu_kho'`: 3 dòng sau (2 trong §4, 1 ở §12), 0 trước (`origin/master`). `rg 'approved_pending.*cho_chu_kho|…'`: khớp câu §12
  sau, 0 trước. `rg 'chu-kho-duyet'`: 3 dòng sau, 0 trước.
- `doctrine-scan --root .` rc=0, `adr-song --root .` rc=0 trên mọi head ứng viên.
- `packet_loop_test.py` trong clone thường (`.git` là thư mục) ghim đúng commit: `nền: 981/981 đạt · BỎ QUA: 1`, `TỔNG: ĐẠT`
  (982 ca, 1343 đột biến, 78 lớp lách) trên `e05ea6a`, `f8d7565`, `7c78914`. Ca bỏ qua: `luong_canonical_chay_that` (chỉ đo pwsh Windows).
- **Head đẩy `4c73081`: KHÔNG chạy suite cục bộ** — chủ kho duyệt trong phiên (27-10 ~17:05Z) lấy N/N từ job `packet_loop_test`
  của `ci.yml` trên đúng head đẩy, vì master tiến 5 lần trong ~3 giờ, nhanh hơn một vòng suite ~60 phút. Hai lượt suite trên
  `bd5a66a` và `c3124e5` bị dừng giữa chừng (head bị thay trước khi xong) — không tính là bằng chứng.
- Một lượt suite trên `e05ea6a` đầu tiên trả `rc=124`: lỗi của executor (`timeout 1500` < thời lượng suite), output bị đệm nên
  không có dòng nào — không đo được gì, đã chạy lại không đặt trần ngắn.

## Cross-review Codex (`gpt-6-astra`, xhigh, qua `launcher.py run`) — 5/8 lời gọi (ADR-0052)

| lượt | head | thời lượng | verdict | lớp |
|---|---|---|---|---|
| 1 | `e05ea6a` (merge `09db703`) | 768 s rc0 | **approve** | 0 P0–P3; đối chiếu từng mệnh đề + mọi cửa ghi state |
| 2 | `7c78914` (merge `7f19424`, `4488444`) | 600 s rc0 | **approve** | 0 P0–P3; xác minh merge, 43/43 ca hồi quy |
| 3 | `bd5a66a` (merge `c2d84ea`, chạm adapter cross-review) | 504 s rc0 | **approve** | 0 P0–P3; 177/177 ca chọn lọc |
| 4 | `c3124e5` (merge `b3decc5`) | 453 s rc0 | **approve** | 0 P0–P3 |
| 5 | `4c73081` (merge `ef34d88`) | 406 s rc0 | **approve** | 0 P0–P3; 100/100 ca chọn lọc + 11/11, 11/11 ca `ops/` |

Luật phân hạng của chủ kho (đột biến độ phủ mới mà A/B đúng ⇒ P3) có trong prompt từ lượt 1. Không slug nào lặp (same_failure_limit 2
không chạm). Ngoài ra có HAI lời gọi `codex exec "Reply with exactly: PONG"` chỉ để đo xác thực, không phải review: 09:34Z (rc=1,
refresh token bị thu hồi ⇒ dừng, báo #977 issuecomment-6438401959) và 12:06Z sau khi chủ kho cấp lại `CODEX_AUTH_JSON` (rc=0).

Hiện vật: `ops/reviews/wp977-g1-codex-luot{1..5}/{PROMPT.md,VERDICT.md,run.json}` trên nhánh lease.

## Lỗi khác lộ ra (ngoài packet)

- **Đua với master**: bước 9 của brief (merge master trước lượt Codex cuối, rồi suite N/N cục bộ trên đúng head đẩy) không hội tụ
  khi master merge nhanh hơn ~60 phút/lần. Đề xuất cho các packet sau: cho phép lấy N/N từ CI trên head đẩy, hoặc chọn cửa sổ
  master yên.
- `/tmp/.git` RỖNG do sandbox Codex để lại xuất hiện sau lượt 2 (15:05Z), trong lúc suite trên `7c78914` đang chạy; suite vẫn đạt
  981/981. Đã `rmdir` (chỉ thư mục rỗng của chính lượt mình). Lượt 1, 3, 4 không để lại.
