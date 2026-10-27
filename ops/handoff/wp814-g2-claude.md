# Handoff — wp814-r3-g2-claude (`MAY-ADR-0054-c`), packet #814 r3 g2

Phiên executor `session_015Gtxragp1zudiMBsihnHH9` (Claude, cloud). Lease `ops/leases/wp814-r3-g2-claude.yaml` (nhánh này).
Đặc tả `ops/specs/wp814-r3.md` @ `07a6eec`, sha256 `39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73`;
phần chung `ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.

- Base lease `09db703`. Head ứng viên **`5a5c5c1f687f74b73301fe161e332ae6b4c0f779`** (merge `origin/master` `4488444`).
- Diff so `4488444`: `.claude/dev/packet_loop.py` +85/−6, `.claude/dev/packet_loop_test.py` +125/−6 ⇒ 2 đường dẫn, **210 dòng thêm** (≤ 450).
- `doctrine-scan` rc=0, `adr-song` rc=0, `git diff --check` sạch; ruff F: 1 (packet_loop) / 2 (test) = bằng master (delta 0).
- 37 ca `r814_*`, 28 đột biến `r814_*` (+ ca mới được thêm vào đích của `r812_bo_generation`, `r813_quyen_ci_qua_luot_moi`).
- Suite đầy đủ `packet_loop_test.py` trong clone thường ghim `5a5c5c1`: **1018/1018** (1019 ca, BỎ QUA 1 Windows-only), 1371 đột biến, `TỔNG: ĐẠT`.

## Cơ chế đã chọn (đặc tả con chỉ cho bất biến)

1. **Bảng nối (M1, I11)** — trường tuỳ chọn `bang_noi: [{tu: [slug], den: slug, ly_do}]` của biên nhận H. MỘT hàm `_kiem_noi`, gọi từ
   `_du_dieu_kien_approve` (dòng `bang-noi`), nên mọi cửa đọc H nhận một luật: lược đồ; mỗi slug nguồn/đích một lần; lý do khác rỗng;
   xét MỌI hàng; đích là lớp **P3** của chính `bang_lop` H (cả hàng `tu: []` = khai lớp mới); nguồn chỉ nhận ở `record-review`
   (`a.lop_truoc` = bảng lớp review liền trước, `_lop_truoc`) và phải là lớp P3 vòng trước đã rời vòng này.
2. **Vòng vá P3 (M2)** — mỗi review ADR-0054 lưu `lop`, `bang_noi`, `vong_p3`. Verdict liền sau một verdict toàn-P3, không `mo_lai`
   xen giữa, là vòng vá; slug P3 mới không có ở vòng trước và không qua bảng nối ⇒ từ chối; số lớp P3 so sau khi áp bảng nối lên cả hai
   vòng; `_xet_dung` (sau khi ghi sổ) ⇒ `blocked` khi vòng > 2 hoặc không giảm. Slug P3 không vào `finding_counts` ở `record-review` lẫn
   `mo-lai`. State trước #814 (review không có `lop`) lấy bảng lớp verdict đang chờ từ `bien_nhan_approve`.
3. **Cửa `vua-p3` (M3)** — approved_pending → running; tập chọn khác rỗng, ⊆ `bien_nhan_approve.p3`; ghi `mo_lai_tu = (p3, generation,
   pending_sha)` thay quyền cũ (I6); `_xet_dung(..., "vua-p3")` (thêm vào `CUA_DI_TIEP`). Không đổi parser/hợp đồng `mo-lai`, `accept`,
   `chu-kho-duyet`; `_load` nhận thêm nguyên nhân `p3` cho `mo_lai_tu`.
4. **M4** — `r814_check_refs_tron_null` (đột biến `r814_refs_bo_do_dai`); `r814_ci_void_connector` (đột biến `r814_void_khoi_phuc_quyen_ci`
   và đích thêm của `r813_quyen_ci_qua_luot_moi`). Chốt chặn ca (b): "chưa có `begin_attempt` sau `mo_lai` cuối" trong `cmd_mo_lai`,
   mã thoát **rc=8** đúng như #813 đo.

## Bảng cửa đọc biên nhận H (chủ kho A, A' — #814 issuecomment-6443725220, -6444784442)

Liệt kê bằng grep `_du_dieu_kien_approve(` và mọi chỗ đọc `bang_lop`/`bang_noi`/`bien_nhan_approve`:

| cửa | đọc gì | luật bảng nối | ca (đích-không-có · nhiều hàng · khác) |
|---|---|---|---|
| `record-review` | `bang_lop`, `bang_noi` | `_kiem_noi` với `truoc` | `r814_rr_dich_khong_co` · `r814_rr_nhieu_hang` · `r814_noi_*` |
| `mo-lai ci-do` | `bang_lop`+`check_refs`, `bang_noi` | `_kiem_noi`, không `truoc` | `r814_ci_dich_khong_co` · `r814_ci_nhieu_hang` · `r814_mo_lai_ci_noi_lai`, `r814_mo_lai_noi_hong` |
| `mo-lai connector` | `bang_lop`+`connector_refs`, `bang_noi` | như trên | `r814_cn_dich_khong_co` · — (bảng lớp chỉ P0–P2 ⇒ không có hàng hợp lệ) · `r814_mo_lai_cn_noi_lai` |
| `accept` (`_slug_connector`) | `bang_lop`+`connector_refs`, `bang_noi` | như trên | `r814_accept_dich_khong_co` · `r814_accept_nhieu_hang` · `r814_accept_noi_lai` |
| `chu-kho-duyet` | checkpoint `ops/checkpoints/*.yaml`, không đọc H | — | — |
| `vua-p3` | `bien_nhan_approve.p3` (đã qua `record-review`), không đọc tệp H | — | `r814_vua_p3_*` |

Đột biến: `r814_bo_kiem_noi_chung` bỏ lời gọi chung (giết ca mọi cửa). Một lời gọi duy nhất nên **không có** đột biến bỏ-riêng-từng-cửa —
đó là chủ đích của A'. `r814_noi_chi_hang_dau` ("chỉ hàng đầu"), `r814_noi_dich_thieu_lot`, `r814_noi_nguon_hang`, `r814_noi_dich_hang`,
`r814_noi_chuoi_lot`, `r814_noi_moi_hang`, `r814_noi_nguon_lap_lot`, `r814_noi_bo_ly_do`, `r814_noi_bo_nguon`.

## Cross-review Codex (`gpt-6-astra`, xhigh, `launcher.py run`) — 4/8 lời gọi

| lượt | head | run | thời lượng | verdict | lớp |
|---|---|---|---|---|---|
| 1 | `335e746` | `250b3011` | 1653 s rc0 | request_changes | 6 P2, 1 P3 |
| 2 | `4adbf92` | `73047543` | 1160 s rc0 | request_changes | 2 P2 (`finding-lineage-counter-reset` lặp ⇒ dừng hỏi, chủ kho chọn A), 1 P3 |
| 3 | `24f6a73` | `f67768cc` | 1147 s rc0 | request_changes | 1 P2 (`receipt-map-validation-skipped` lặp ⇒ dừng hỏi, chủ kho chọn A'), 2 P3 |
| 4 | `5a5c5c1` | `94a3a54b` | 1388 s rc0 | **approve** | 0 P0–P2, 2 P3 |

Hiện vật: `ops/reviews/wp814-g2-codex-luot{1..4}/{PROMPT.md,VERDICT.md,run.json}`.

## Nợ P3 còn mở

1. **`legacy-p3-failure-counts-retained`** — owner **#816** (packet kích hoạt), theo quyết định chủ kho A. State ADR-0054 do code trước
   #814 tạo (approve có lớp P3 + `--finding-id`) đã cộng lớp P3 vào `finding_counts`; sau nâng cấp, lần P2 đầu của cùng slug chạm trần.
   Không có state thật: ADR-0054 chưa kích hoạt (`git grep 'kích hoạt \`ADR-0054\`' origin/master -- docs/adr/` chỉ ra chính tệp 0054,
   bị `_che_do_0054` loại). Hướng: trước khi kích hoạt, rà dữ liệu thật; không viết migration ở #814.
2. **`r814-mutation-evidence-incomplete` · `duplicate-destination`** — owner executor #814 (chủ kho định tuyến). Đột biến chỉ bỏ
   `and len(set(den)) == len(den)` trong `_kiem_noi` sống; mã sản phẩm từ chối đúng (Codex lượt 4 A/B). Hướng: thêm ca hai hàng cùng
   đích + đột biến gỡ đúng kiểm ấy. Không mở thêm vòng vá để giữ head đã duyệt.

## Lỗi khác lộ ra (ngoài packet)

- `mo-lai ci-do` cho lớp hạng P3 có `check_refs` (chỉ connector đòi P0–P2): nay P3 không vào bộ đếm (M2) — hợp đồng nhận không đổi.
- Quyền `mo_lai_tu` p3 chưa có cửa tiêu thụ; tiêu thụ ở cửa đẩy là việc #816.
- Phiên này hai lần tự giết shell bằng `pkill -f <mẫu>` khi mẫu cũng có trong chính dòng lệnh — dùng PID + `readlink /proc/<pid>/cwd`.

## Nghiệm thu và đẩy

- Suite đầy đủ trên `5a5c5c1` (clone thường, `.git` là thư mục): nền `1018/1018 đạt · BỎ QUA: 1` (`luong_canonical_chay_that`, chỉ
  Windows), AC19 78/78, đột biến 1371, `ngoại lệ AC 18: 0`, `TỔNG: ĐẠT`, rc=0. Codex lượt 4 approve chính SHA này.
- Đẩy `agent/wp814-g2-claude` **một lần** tại `5a5c5c1` (ls-remote xác nhận). PR draft #998, đã subscribe.
- Còn lại theo M-1/M-2: CI `ci.yml` (gate-packet-loop, thu-hoi) xanh trên head, connector Codex xong trên head, trả lời mọi thread.
