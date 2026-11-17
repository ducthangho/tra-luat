# wp1350 r1 — trục attempts cho nang-tran (NANG-TRAN-ATTEMPTS)
packet_id: wp1350
revision: 1

Trạng thái: đặc tả đóng băng cho Packet #1350, Mission #1172 revision 58 (https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6933449731). Quyết định chủ kho: https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6933449308 .

## Vấn đề (đo được)

State target WP1308 g5 trên Desktop là `leased` rev3, attempts 1/1 đã cạn. Ở master `e4cce23`, `cmd_nang_tran` chỉ nhận các trục trong `TRUC_TRAN`, hiện gồm `vong_review` và `codex_review_calls`. Không đường canonical nào nâng được `attempts_limit` sau `init`, dù whitelist ghi của WP1174 cho `nang-tran` có liệt kê trường đó. Vì vậy canary target không đi tiếp được.

## Hợp đồng

1. `nang-tran --truc attempts --tran-moi N --ai-nang <người> --can-cu <URL>` nâng `attempts_limit` từ giá trị hiện tại lên N > hiện tại. Lệnh dùng đúng các chốt của hai trục cũ: `--ai-nang` phải thuộc `NGUOI_CO_THAM_QUYEN`, `--can-cu` khớp `CAN_CU_RE`, và nối một bản ghi `nang_tran` với `truc`, `tran_cu`, `tran_moi`, `ai_nang`, `can_cu`.
2. Cả hai đường đều phải chạy:
   - legacy v1/v2 (`cmd_nang_tran`);
   - WP1174 scoped/target qua `_1174_ordinary`: postimage chính xác bằng whitelist hiện có của `nang-tran`; đơn điệu (`attempts_limit` không giảm, `state_revision` +1); `high_water`/witness như mọi lệnh thường; resolve, I2, TargetProof giữ nguyên.
3. **Không đổi ngữ nghĩa có sẵn:**
   - Chặn `begin-attempt` khi `attempts_used >= attempts_limit` giữ nguyên.
   - Logic `blocked`/`rescue_required` và thứ tự xét trục ở `_xet_dung` (hiện chỉ cho review/codex) giữ nguyên: chạm trần attempts **không** chuyển sang `rescue_required`.
   - `record-rescue` giữ nguyên.
   - Kiểm `bo-dem` và `truc` trong `_load` không được nới.
   - Nếu cần tách bảng trục cho `nang-tran` khỏi `TRUC_TRAN` để giữ các ngữ nghĩa trên, làm như vậy.
4. Trần cứng của policy hiện có (vd. `attempts_limit <= 18` trong kiểm limits) phải được tôn trọng trên đường WP1174. Vượt trần thì từ chối, không ghi gì.
5. Không thêm cờ nới, không đổi `NGUOI_CO_THAM_QUYEN`, không đổi gate K0–K7, không chạm VERSION, manifest, workflow hay release.

## Write set

- `.claude/dev/packet_loop.py`
- `.claude/dev/packet_loop_test.py`

Cần path thứ ba thì dừng, không mở rộng.

## Kiểm chứng bắt buộc

- **Ca mới** (ID chốt trước): `wp1350_nang_tran_attempts_legacy`, `wp1350_nang_tran_attempts_scoped`, `wp1350_nang_tran_attempts_rejections`.
  - Hai ca dương: nâng được, bản ghi đúng, `begin-attempt` sau đó được phép, counters đúng.
  - Ca âm: người không có quyền, căn cứ sai, N ≤ trần hiện tại, vượt trần policy, `--expected-revision` cũ. Mỗi ca âm phải rc khác 0 và không ghi state/witness.
- **Ca giữ nguyên, phải vẫn đạt:**
  - mọi `wp1315_*` (đặc biệt `wp1315_pending_exhausted_budget`);
  - `wp1174_lifecycle_*`, `wp1174_adopt_*`;
  - các ca rescue/nang-tran hiện có (author liệt kê ID cụ thể trong handoff).
- **Đột biến:** ít nhất ba mutant đăng ký trong `MUTANTS`, mỗi cái có ca đích riêng:
  - bỏ kiểm `NGUOI_CO_THAM_QUYEN` cho trục attempts;
  - bỏ kiểm N > trần hiện tại;
  - bỏ trần policy.
  Mỗi mutant phải làm ca đích đỏ vì assertion của chính ca đó.
- Ruff F delta so với master = 0. `tl.py --selftest` N/N trước push.

## Quy trình và quyền

Lease `wp1350-r1-g1-claude`: executor Claude (`claude-fable-5-2`), reviewer Codex (`gpt-6-astra`). Spec review và source review do Codex làm; audit H là `owner_delegated_audit` theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916538696 (packet source; không phải audit canary). Chỉ push sau khi review approve định dạng K4 trên đúng H. Sau đó draft PR, CI PR Ubuntu, connector, full M9, `kiem-merge` K0–K7. Merge do chủ kho bấm. Windows CI miễn theo https://github.com/ducthangho/tra-luat/issues/1172#issuecomment-6916597687; Windows native: diff chạm `.claude/dev/` nên K6 cần lượt Windows tập trung hoặc dòng miễn có bằng chứng.

Không target G5, LIVE hay installation. Canary WP1308 chỉ chạy lại bằng packet riêng sau khi gói này land.
