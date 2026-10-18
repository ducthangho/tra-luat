Reviewed commit: f9d84d70fb46540bbecfae963c9afb4a2b48984d

verdict: approve
P1=0 P2=0 P3=0

**F18 ĐÃ VÁ THẬT. Audit mới trên HEAD: 39 tên / 40 ô, 40/40 chết đúng chốt, không traceback runtime.** Mutant thiếu họ model chết tại assertion “v1 phải suy 3/3”; mutant suy0 vẫn chết tại `record-codex-call` đòi rc3/được0. Không phát hiện finding F19 trở đi trong phạm vi kiểm định đã giao.

Suite đúng cwd KHO **rc0: nền351/351, BỎ QUA1;145 mutant khai báo,144 báo giết và1 bỏ qua Windows; TỔNG: ĐẠT**. Bảng ngoài **40/40 GIET_THAT**,0 tín dụng giả/0 sống. Ruff F và E302/E305 không tăng so base; doctrine-scan/adr-song base và HEAD đều rc0.

## Định danh và phạm vi

- KHO chỉ đọc: `/tmp/claude-0/-home-user-tra-luat/d2609060-62e1-5761-b248-ec0c3bc71a0b/scratchpad/rv17`; detached HEAD đúng OID dòng đầu; tree `4e712f37bf014e18e87df07d0f94d0ba353fb3e7`. [Snapshot đầu](repo-initial.json).
- SPEC wp775 r1: [spec-wp775.md](spec-wp775.md), SHA-256 `4b7530c265dddefbebd06ea209d7c0594210f57b391e0d0d353931171fd2b6d8`. Diff so base `653fef3f52f3130dd6f597c1036430ffb807fef1` đúng hai tệp: runtime +157/−4, test +189/−8, tổng **346 dòng thêm**, diff --check rc0. [Diff toàn packet](packet.diff).
- Kích thước không tăng so lượt16; commit local `fa5be283f63af1eaddbb21141aaf94898e4fe1da` ghi lời khai chủ kho đã duyệt346. Không xác minh độc lập thẩm quyền GitHub; không coi số346 là đạt trần300 nguyên bản bằng phép tính.
- Reviewer: Codex/OpenAI, họ `openai`; bề mặt thực quan sát được là phiên API có công cụ shell/Python cục bộ; transport `machine`. Không tự chứng nhận launcher, model ID/effort phục vụ từng request, receipt hay quyền merge.
- Sandbox thực cho phép ghi thư mục ra và `/tmp`; mọi bản sao, state hỏng do test dựng, log và patch thử nằm ngoài KHO. Python dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`; Ruff dùng `--no-cache` trên bản sao. Không gọi mạng, không sửa mã KHO.
- Môi trường đo: Linux, Python3.13.16, Ruff0.16.8, Git2.43.0. [Phiên bản](tool-versions.json).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lịch sử là [VERDICT lượt16](VERDICT-luot16.md), reviewed SHA `84bdbaccbd85210db3cb829bc487a28c2e1848a4`. Kết quả bên dưới được đo lại trên HEAD lượt17. “ĐÃ VÁ THẬT” giới hạn ở biểu hiện và chốt được giao; không có nghĩa đã phủ mọi JSON hay mọi vế con trong predicate ghép.

| Finding / nguồn | Biểu hiện | Kết luận trên HEAD lượt17 và bằng chứng mới |
| --- | --- | --- |
| F01 | Reader bỏ kiểm sổ/counter | **ĐÃ VÁ THẬT, giữ đóng**: reader15/15 và consistency2/2 bị8; 11 mutant nhóm reader chết tại `status` đúng nhóm. [reader](reader.log), ô1–11. |
| F02 | Fixture âm lẫn nhiều lỗi | **ĐÃ VÁ THẬT, giữ đóng**: baseline M6 xanh; mỗi biến thể bắt đầu từ `t` sạch, có đối chứng `{}`; trạng thái trước từng điểm chết trong trace. Không khai đã cô lập mọi vế con của nhóm dem-goi. |
| F03 | Schema/container/identity/flag/trục | **ĐÃ VÁ THẬT, giữ đóng**: r2 mẫu hỏng8; v1 thật và hai checkpoint hợp lệ chạy được. [r2](r2.log). |
| F04 | Mutant M5-khac định tuyến sai | **ĐÃ VÁ THẬT, giữ đóng**: mutant nhắm nhánh quyết định khác; assertion giữ blocked chạy ngay sau `tach_stable_slice`. Ô36. |
| F05 | Metadata attempt/review sai kiểu | **ĐÃ VÁ THẬT, giữ đóng**: attempts_used bool/float/string, attempt_open sai kiểu, finding_counts=[], same_failure_limit=null, thiếu review.attempt/provider đều8. [r3](r3.log). |
| F06 | Dòng trắng giữa hàm | **ĐÃ VÁ THẬT, giữ đóng**: E302/E305 runtime3/3, test5/5 so base/HEAD; delta0. [quality](quality-summary.json). |
| F07 | Packet identity/projection | **ĐÃ VÁ THẬT, giữ đóng**: packet/state/projection sai bị8; bốn identity Codex hợp lệ call0. [r4](r4.log). |
| F08 | Posts/anchor/findings/checkpoint | **ĐÃ VÁ THẬT, giữ đóng**: r6 có20 cặp status/consumer8/8 +1 findings status8;41 lỗi đều giữ bytes. [r6](r6.log). |
| F09 | Packet sai kiểu cũng sai giá trị | **ĐÃ VÁ THẬT, giữ đóng**: fixture packet55.0 giữ đúng giá trị; mutant bỏ type cho status0 thay8. Ô13. |
| F10 | Hạ schema v2 làm reset counter | **ĐÃ VÁ THẬT, giữ đóng**: reviewing/blocked hạ schema đều status8/action8, giữ used2 và hai calls; v1 thật vẫn di trú. [schema](schema.log), [r2](r2.log). |
| F11 | Spacing/style phát sinh | **ĐÃ VÁ THẬT, giữ đóng**: Ruff F runtime1/1(F841), test2/2(F541); spacing3/3 và5/5; delta0. Bare lint vẫn rc1 vì nợ nền. [quality](quality-summary.json). |
| F12 | Mở rescue thiếu sổ nâng | **ĐÃ VÁ THẬT, giữ đóng**: limit2>used1 nhưng sổ rỗng không mở; sổ thiếu trường cũng8/blocked. Baseline M5 và [connector a](connector.log). |
| F13 | Mutant sổ nâng bị vế trần che | **ĐÃ VÁ THẬT, giữ đóng**: `pl_f12_bo_so_nang` chết đúng biên bản6, used1/limit2, sổ rỗng,8→0. Ô33. |
| F14 | Trục vòng che trục Codex | **ĐÃ VÁ THẬT, giữ đóng**: mutant chỉ vòng chết ở riêng calls2/2, vòng2/50; mutant ưu tiên chết nhãn ở cùng2/2. Ô25–26. |
| F15 | Mutant replay chết ở reader sau khi phá writer | **ĐÃ VÁ THẬT, giữ đóng**: dựng lượt2 thành công, cùng H1/b1=true; chết ngay review replay5→0. Ô20. |
| F16 | Hậu điều kiện M5 kiểm quá muộn | **ĐÃ VÁ THẬT, giữ đóng**: ngay sau `tach_stable_slice` rc0, assertion thấy running/None/None; chưa gọi `revision`. Ô36. |
| F17 | Reader che lời gọi M6 cần đo | **ĐÃ VÁ THẬT, giữ đóng**: mutant phối hợp suy0/gỡ cận dưới chết tại call trên sd2,3→0, trước status. Ô39. |
| F18 | Mutant thiếu họ chết ở guard provider | **ĐÃ VÁ THẬT**: call trên sd2 có họ tường minh rc3; status trên sd vẫn thiếu họ rc0; assertion tuple thấy(0,3,true) thay(3,3,true). Ô40. |
| Connector trước11: provider | Reviewer khác Codex ghi call | **ĐÃ VÁ THẬT, giữ đóng**: sáu cấu hình Claude call4/unchanged; bốn identity Codex hợp lệ call0. [r4](r4.log), ô28 đo ưu tiên mã. |
| Connector trước11: khóa sổ | tran_cu/tran_moi và strip actor | **ĐÃ VÁ THẬT, giữ đóng**: baseline M4 kiểm khóa chuẩn/actor strip; hai lần nâng/mở ở r2 rc0. |
| Connector11/P1-a | Sổ nâng thiếu hình dạng M4 | **ĐÃ VÁ THẬT, giữ đóng**: connector a8/blocked; mutant hình dạng chết đúng biên bản7 với used1/limit2, sổ chỉ truc/tran_moi. Ô34. |
| Connector11/P1-b | Review mới khi hết vòng | **ĐÃ VÁ THẬT, giữ đóng**: connector b review11=3, giữ10/10/blocked; mutant preguard cho approve0 khi trước đó9/9. Ô35. |
| Connector12/P2-a | Ưu tiên trục khi cùng chạm | **ĐÃ VÁ THẬT, giữ đóng**: HEAD ưu tiên Codex; mutant vẫn rc3 nhưng assertion thấy nhãn vong_review. Ô26. |
| Connector12/P2-b | Đoạn URL/neo cuối | **ĐÃ VÁ THẬT, giữ đóng biểu hiện cũ**: baseline M4 từ chối owner# và URL+LF bằng2; mutant regex cũ chết ở owner#. Không khai đã khóa độc lập nhánh LF bằng mutant này. Ô31. |

**Kiểm riêng F18:** vị trí fixture `.claude/dev/packet_loop_test.py:5545`, assertion suy tại `:5550`/`:5551`; fallback runtime tại `.claude/dev/packet_loop.py:642`/`:673`. diff84bdbac→HEAD đúng [HINT-F18.patch](HINT-F18.patch), SHA-256 `cad226ea241199d2641fafaaa3ca0c98efda4361fd1990414dca4e8c4ccbf000`. Đã dry-run bằng `patch -p0 --fuzz=0 --dry-run` rồi áp trên bản sao test84bdbac, rc0/0; bytes kết quả bằng testHEAD. Đổi1 dòng thành1 dòng, **Δ dòng thêm=0**. [Log so patch](f18-patch-check.json). Không áp patch vào KHO. Đo riêng trước audit: [baseline8 ca](f18-first/BASELINE/audit.json), [F18](f18-first/pl_m6_state_cu_mat_ho/audit.json), [F17](f18-first/pl_m6_suy_used_0/audit.json).

## BẢNG LỚP

| Slug lớp / lịch sử từ lượt16 trên84bdbac | Mức cao nhất còn mở | Phép kiểm đóng lớp / giới hạn |
| --- | --- | --- |
| `mutant-wrong-latch` — F04/F13–F18 | Không | Fixture call có họ tường minh, fixture legacy thiếu họ riêng; hậu điều kiện M5 kiểm ngay. Audit mới đủ40 ô đúng chốt, gồm toàn bộ M5/M6. |
| `state-ledger-validation` — F01/F03/F05/F07/F08/F10/F12, connector11-a | Không trong các biểu hiện được giao | Reader/consumer mẫu hỏng8, không traceback; r6 giữ bytes; v1 thật/luồng hợp lệ0. Không tuyên bố schema toàn phần cho mọi metadata. |
| `state-negative-fixture-contamination` — F02/F09 | Không | Đối chứng sạch; từng biến thể từ `t`; packet55.0 cô lập kiểu. Không mở rộng kết luận tới từng predicate con chưa có mutant riêng. |
| `budget-boundary / rescue-axis` — F14, connector11-b/12-a | Không | Riêng vòng, riêng call, cùng chạm, approve tại biên, review mới khi hết vòng và hai checkpoint nối tiếp. |
| `provider / raise-record / URL` — connector trước11,11-a,12-b | Không | Provider/allowlist/khóa chuẩn/hình dạng sổ và URL đo đúng; không chứng thực ai thực sự viết căn cứ. |
| `top-level-function-spacing` — F06/F11 | Không phát sinh delta | Bare Ruff F và preview E302/E305 so cùng base: số lỗi không tăng. Không gọi bare lint rc1 là pass tuyệt đối. |

Tập lớp mở cuối lượt16 `U={mutant-wrong-latch}`; lượt17 xác minh đóng toàn bộ các biểu hiện được giao của lớp này: `|F|/|U|=1/1=100%`. Lớp mới0, lớp tái mở0 trong phạm vi đã đo. Bảy nợ ngoài spec được bảo lưu riêng, không tính là “đã vá” hoặc dùng để nâng tỷ lệ này.

## BẢNG AUDIT 40 Ô

Đã chạy lại **39 tên / 40 ô** trên HEAD: **40/40 đúng chốt**, 0 traceback runtime, 0 ô sống. Tám ca nền `pl_*` đều xanh. [Driver](audit_mutants.py), [summary](mutation-audit-head/summary.json), [phân loại](mutation-audit-head/classified.json).

Mỗi mutant một bản sao và một process `python3.13 -B`; lệnh con đầy đủ, state trước/sau và stack assertion nằm trong trace. Stack reviewer là dữ liệu chẩn đoán, không phải traceback runtime của sản phẩm. `H1=0000000000000000000000000000000000000001`, `H2=0000000000000000000000000000000000000002`, `Ha=000000000000000000000000000000000000000a`; `U=https://github.com/o/r/issues/775#issuecomment-1`, `U0=https://github.com/o/r/issues/775`, `U#=https://github.com/o#x/r/issues/775#issuecomment-1`. “rcA→B” là đòi A/được B.

| # | Mutant / trace HEAD | Ca đích | Bước chết: lệnh + đối số; đòi→được | Chốt runtime đột biến nhắm tới | Đúng chốt? |
| --- | --- | --- | --- | --- | --- |
| 1 | [pl_f01_bo_schema](mutation-audit-head/pl_f01_bo_schema/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/schema: packet bắt buộc, đúng kiểu/giá trị; thiếu packet. | Đúng |
| 2 | [pl_f01_bo_bo-dem](mutation-audit-head/pl_f01_bo_bo-dem/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/bo-dem: attempts_used=true bị từ chối. | Đúng |
| 3 | [pl_f01_bo_so](mutation-audit-head/pl_f01_bo_so/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/so: thiếu attempt_open. | Đúng |
| 4 | [pl_f01_bo_loi-goi](mutation-audit-head/pl_f01_bo_loi-goi/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/loi-goi: da_dung=1 khác bool. | Đúng |
| 5 | [pl_f01_bo_dem-goi](mutation-audit-head/pl_f01_bo_dem-goi/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/dem-goi: hai run_id g1 trùng (đồng thời vượt cận dưới unused trong cùng predicate). | Đúng nhóm; không khai cô lập hai vế |
| 6 | [pl_f01_bo_dem-vong](mutation-audit-head/pl_f01_bo_dem-vong/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/dem-vong: used2 khác len(reviews)=3. | Đúng |
| 7 | [pl_f01_bo_truc](mutation-audit-head/pl_f01_bo_truc/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/truc: running nhưng ly_do=rescue_required. | Đúng |
| 8 | [pl_f01_bo_posts](mutation-audit-head/pl_f01_bo_posts/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/posts: posts=null. | Đúng |
| 9 | [pl_f01_bo_anchor](mutation-audit-head/pl_f01_bo_anchor/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/anchor: thiếu hmac_key, anchor còn đủ. | Đúng |
| 10 | [pl_f01_bo_findings](mutation-audit-head/pl_f01_bo_findings/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/findings: finding_counts có probe-finding1 nhưng reviews không có finding. | Đúng |
| 11 | [pl_f01_bo_checkpoint](mutation-audit-head/pl_f01_bo_checkpoint/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/checkpoint: history pending nhưng projection chưa rescue. | Đúng |
| 12 | [pl_f10_bo_phan_biet_v1](mutation-audit-head/pl_f10_bo_phan_biet_v1/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/M6: schema1 trên state vẫn có các khóa v2. | Đúng |
| 13 | [pl_f07_bo_kieu_packet](mutation-audit-head/pl_f07_bo_kieu_packet/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc8→0 | Reader/schema: packet55.0 chỉ lệch kiểu. | Đúng |
| 14 | [pl_m1_bo_kiem_so_duong](mutation-audit-head/pl_m1_bo_kiem_so_duong/audit.json) | `pl_m1_tran_so_duong` | `init --packet 55 --mission 54 --executor claude --reviewer codex --review-rounds-limit 50 --codex-review-calls-limit 50 --review-rounds-limit 0`; rc2→0 | M1 init: min hai trần phải >0. | Đúng |
| 15 | [pl_m2_kiem_sau_khi_ghi](mutation-audit-head/pl_m2_kiem_sau_khi_ghi/audit.json) | `pl_m2_loi_goi` | `record-codex-call --packet 55 --head H1 --run-id g3`; rc3; assert `chặn TRƯỚC khi ghi`: `{"truc": "codex_review_calls", "codex_review_calls_used": 3, "state": "blocked", "ly_do": "rescue_required"}` | M2 chặn TRƯỚC ghi, used phải giữ2. | Đúng: assertion used3 ngay sau call g3 |
| 16 | [pl_m2_lon_hon_bang](mutation-audit-head/pl_m2_lon_hon_bang/audit.json) | `pl_m2_loi_goi` | `record-codex-call --packet 55 --head H1 --run-id g3`; rc3→0 | M2 biên used>=limit (2/2). | Đúng |
| 17 | [pl_m2_bo_so_head](mutation-audit-head/pl_m2_bo_so_head/audit.json) | `pl_m2_loi_goi` | `record-codex-call --packet 55 --head H2 --run-id g1`; rc5→0 | M2 head lời gọi bằng reviewing_head H1. | Đúng |
| 18 | [pl_m2_bo_kiem_trung](mutation-audit-head/pl_m2_bo_kiem_trung/audit.json) | `pl_m2_loi_goi` | `record-codex-call --packet 55 --head H1 --run-id g1`; rc2→0 | M2 run_id chưa tồn tại. | Đúng |
| 19 | [pl_m3_codex_call_tuy_chon](mutation-audit-head/pl_m3_codex_call_tuy_chon/audit.json) | `pl_m3_neo_loi_goi` | `record-review --packet 55 --provider codex --verdict approve --reviewed-sha H1`; rc5→0 | M3 --codex-call bắt buộc với Codex. | Đúng |
| 20 | [pl_m3_bo_co_da_dung](mutation-audit-head/pl_m3_bo_co_da_dung/audit.json) | `pl_m3_neo_loi_goi` | `record-review --packet 55 --provider codex --verdict approve --reviewed-sha H1 --codex-call b1`; rc5→0 | M3 guard chống dùng lại b1=true, cùng head H1. | Đúng; F15 đóng |
| 21 | [pl_m3_bo_so_head_loi_goi](mutation-audit-head/pl_m3_bo_so_head_loi_goi/audit.json) | `pl_m3_neo_loi_goi` | `record-review --packet 55 --provider codex --verdict approve --reviewed-sha H2 --codex-call a1`; rc5→0 | M3 head call a1(H1) bằng reviewed H2; a1 còn false. | Đúng |
| 22 | [pl_m3_kich_ca_khi_approve](mutation-audit-head/pl_m3_kich_ca_khi_approve/audit.json) | `pl_m3_vong` | `record-review --packet 55 --provider codex --verdict approve --reviewed-sha Ha --codex-call g10`; rc0→3 | M3 approve không kích rescue khi vừa chạm trục tương ứng. | Đúng: riêng vòng10/10, calls10/50 |
| 23 | [pl_m3_kich_ca_khi_approve](mutation-audit-head/pl_m3_kich_ca_khi_approve/audit.json) | `pl_m3_codex` | `record-review --packet 55 --provider codex --verdict approve --reviewed-sha H2 --codex-call g2`; rc0→3 | M3 approve không kích rescue khi vừa chạm trục tương ứng. | Đúng: riêng calls2/2, vòng2/50 |
| 24 | [pl_m3_bo_truc_vong](mutation-audit-head/pl_m3_bo_truc_vong/audit.json) | `pl_m3_vong` | `record-review --packet 55 --provider codex --verdict changes_requested --reviewed-sha Ha --codex-call g10 --finding-id loi-g10`; rc3→0 | M3 kích rescue riêng vòng10/10, calls10/50. | Đúng |
| 25 | [pl_m3_chi_xet_truc_vong](mutation-audit-head/pl_m3_chi_xet_truc_vong/audit.json) | `pl_m3_codex` | `record-review --packet 55 --provider codex --verdict changes_requested --reviewed-sha H2 --codex-call g2 --finding-id loi-g2`; rc3→0 | M3 kích rescue riêng calls2/2, vòng2/50. | Đúng; F14 giữ đóng |
| 26 | [pl_c12_thu_tu_truc](mutation-audit-head/pl_c12_thu_tu_truc/audit.json) | `pl_m3_codex` | `record-review --packet 55 --provider codex --verdict changes_requested --reviewed-sha H2 --codex-call g2 --finding-id loi-g2`; rc3; assert `chạm trần + changes_requested`: `{"truc": "vong_review", "state": "blocked", "ly_do": "rescue_required"}` | M3 hai trục2/2: Codex ưu tiên. | Đúng: assertion truc=vong_review thay Codex |
| 27 | [pl_m4_danh_sach_cam](mutation-audit-head/pl_m4_danh_sach_cam/audit.json) | `pl_m4_nang_tran` | `nang-tran --packet 55 --truc codex_review_calls --tran-moi 3 --ai-nang codex-dispatcher --can-cu 'U'`; rc7→0 | M4 người nâng phải ở allowlist. | Đúng |
| 28 | [pl_m2_bo_kiem_reviewer_codex](mutation-audit-head/pl_m2_bo_kiem_reviewer_codex/audit.json) | `pl_m2_loi_goi` | `record-codex-call --packet 55 --head H1 --run-id g9`; rc4→8 | M2 guard reviewer trả RC_PROVIDER trước kiểm state. | Đúng mã/ưu tiên của cùng lệnh; không chứng minh nhận call0 |
| 29 | [pl_m4_tran_moi_bang](mutation-audit-head/pl_m4_tran_moi_bang/audit.json) | `pl_m4_nang_tran` | `nang-tran --packet 55 --truc codex_review_calls --tran-moi 2 --ai-nang ducthangho --can-cu 'U'`; rc2→0 | M4 trần mới tăng nghiêm: 2=2 bị từ chối. | Đúng |
| 30 | [pl_m4_can_cu_long](mutation-audit-head/pl_m4_can_cu_long/audit.json) | `pl_m4_nang_tran` | `nang-tran --packet 55 --truc codex_review_calls --tran-moi 3 --ai-nang ducthangho --can-cu U0`; rc2→0 | M4 căn cứ bắt buộc fragment issuecomment. | Đúng |
| 31 | [pl_c12_can_cu_doan](mutation-audit-head/pl_c12_can_cu_doan/audit.json) | `pl_m4_nang_tran` | `nang-tran --packet 55 --truc codex_review_calls --tran-moi 3 --ai-nang ducthangho --can-cu 'U#'`; rc2→0 | M4 regex giới hạn đoạn owner/repo và neo cuối. | Đúng nhánh owner#; chưa khóa độc lập nhánh LF bằng mutant này |
| 32 | [pl_m5_mo_khong_can_nang](mutation-audit-head/pl_m5_mo_khong_can_nang/audit.json) | `pl_m5_rescue` | `record-rescue --packet 55 --quyet-dinh nang_tran --can-cu 'U'`; rc8→0 | M5 trần>used; sổ hợp hình dạng, used1/limit1. | Đúng: biên bản5 |
| 33 | [pl_f12_bo_so_nang](mutation-audit-head/pl_f12_bo_so_nang/audit.json) | `pl_m5_rescue` | `record-rescue --packet 55 --quyet-dinh nang_tran --can-cu 'U'`; rc8→0 | M5 phải có sổ nâng; used1/limit2 nhưng sổ rỗng. | Đúng: biên bản6; F13 giữ đóng |
| 34 | [pl_c11_bo_hinh_nang](mutation-audit-head/pl_c11_bo_hinh_nang/audit.json) | `pl_m5_rescue` | `record-rescue --packet 55 --quyet-dinh nang_tran --can-cu 'U'`; rc8→0 | M5 sổ nâng đủ hình dạng; used1/limit2, sổ chỉ truc/tran_moi. | Đúng: biên bản7 |
| 35 | [pl_c11_bo_chan_vuot_vong](mutation-audit-head/pl_c11_bo_chan_vuot_vong/audit.json) | `pl_m3_vong` | `record-review --packet 55 --provider codex --verdict approve --reviewed-sha Ha --codex-call g10`; rc3→0 | M3 preguard vòng đã9/9, không nhận review mới kể cả approve. | Đúng |
| 36 | [pl_m5_quyet_dinh_khac_mo](mutation-audit-head/pl_m5_quyet_dinh_khac_mo/audit.json) | `pl_m5_rescue` | `record-rescue --packet 55 --quyet-dinh tach_stable_slice --can-cu 'U'`; rc0; assert `tach_stable_slice GIỮ blocked`: `{"truc": null, "state": "running", "ly_do": null}` | M5 hậu điều kiện quyết định khác phải giữ blocked ngay sau tach_stable_slice. | Đúng; F16 đóng tại assertion ngay sau tach_stable_slice |
| 37 | [pl_m5_bo_kiem_ly_do](mutation-audit-head/pl_m5_bo_kiem_ly_do/audit.json) | `pl_m5_rescue` | `record-rescue --packet 55 --quyet-dinh dung --can-cu 'U'`; rc8→0 | M5 blocked vì same-failure không được record-rescue. | Đúng: chỉ vế reason sai |
| 38 | [pl_m5_them_blocked_running](mutation-audit-head/pl_m5_them_blocked_running/audit.json) | `pl_m5_rescue` | `transition --packet 55 --to running`; rc8→5 | M5 bảng cấm blocked→running phải trả RC_STATE trước comment gate. | Đúng mã lỗi của cùng transition; không chứng minh bypass0 |
| 39 | [pl_m6_suy_used_0](mutation-audit-head/pl_m6_suy_used_0/audit.json) | `pl_m6_state_v1` | `record-codex-call --packet 55 --head H1 --run-id g1`; rc3→0 | M6 lời gọi kế tiếp trên v1 đã có3 review phải bị RC_TRAN, không fail-open. | Đúng; F17 đóng: fail-open lời gọi rc3→0, chưa status |
| 40 | [pl_m6_state_cu_mat_ho](mutation-audit-head/pl_m6_state_cu_mat_ho/audit.json) | `pl_m6_state_v1` | `status --packet 55`; rc0; assertion **“v1 phải suy 3/3”**: tuple **(0,3,true)** thay (3,3,true). Call trước đó trên sd2 rc3. | M6 legacy thiếu identity phải suy Codex/openai và used3. | **Đúng; F18 đóng**: chết ở kết quả suy, không ở guard provider. |

Hai ô ưu tiên mã cần đọc đúng phạm vi: ô28 xác nhận provider guard trả4 trước state guard8; ô38 xác nhận bảng transition trả8 trước comment gate5. Chúng phát hiện thiếu guard ở **chính lệnh được nhắm**, không chứng minh mutant bypass thành công rc0. Ô40 nhắm bộ đếm suy của reader; nay chết tại assertion kết quả suy, đáp ứng khác biệt mà F18 yêu cầu.

## Finding F19 trở đi

Không phát hiện finding mới P1/P2/P3 trong phạm vi diff và các phép đo đã chạy. Không có HINT mới cần tạo. HINT-F18 là hiện vật lịch sử đã được kiểm khớp HEAD và kiểm lại hiệu ứng.

## Đối chiếu SPEC M1–M7 và săn finding còn lại

Đã đọc toàn diff hai tệp và đường `_load`→guard lệnh→ghi state, quan hệ review/counter/call chưa dùng, journal checkpoint và các cửa thoát blocked. Không viết script dữ liệu thử mới; script mới duy nhất dùng tạo/audit đột biến. Ý tưởng dữ liệu chưa có driver chỉ mô tả bằng lời bên dưới.

| Mục | Kết luận trên HEAD |
| --- | --- |
| M1 | Init schema2/counter0/trần10/2/sổ rỗng; hai cờ0/−1/abc bị2. Mutant nới kiểm số dương chết tại init trần0. |
| M2 | Chỉ reviewing/đúng head/run_id đúng dạng/chưa trùng; call vượt trần bị3 trước tăng used/sổ. Caller reviewer khác Codex bị4 trước state. |
| M3 | Review Codex bắt buộc call đúng head/chưa dùng; ghi thành công tăng vòng và đánh dấu call. Hai trục độc lập/cùng chạm đều đo; approve khi vừa chạm không rescue; review mới khi vòng đã hết bị3. |
| M4 | Actor strip rồi allowlist, trần tăng nghiêm, URL issuecomment, khóa chuẩn tran_cu/tran_moi; docstring nêu “LỜI KHAI, KHÔNG PHẢI BẰNG CHỨNG”. |
| M5 | Sai lý do bị8; thiếu nâng vẫn ghi biên bản nhưng giữ blocked; ba quyết định khác giữ blocked ngay sau từng lệnh. Chỉ nâng hợp lệ rồi rescue mới mở running trong các đường đã đo. |
| M6 | V1 thật sinh bởi base cho Codex/Claude đọc/di trú được, cảnh báo/cờ suy còn, lần ghi thành2. Hạ schema trên state có khóa v2 bị8. Hai mutant M6 đều chết đúng chốt. |
| M7 | 8 ca nền pl_* xanh;39 tên/40 ô đều AssertionError đúng chốt,0 traceback runtime. Full suite351/351, skip1;145 mutant khai báo:144 báo giết,1 skip; ĐẠT. Bank ngoài40/40 GIET_THAT. |

Giữ luật same-failure cũ: runtime xét same-failure trước rescue; ca đo từng trục dùng finding khác nhau để không bị chốt này che. Không đổi cách tính attempts và không mở lại bảy mục nợ chỉ thị loại khỏi spec r1.

## HƯỚNG THỬ

| Hướng / giả thuyết | Phép đo | Kết quả / giới hạn |
| --- | --- | --- |
| F18 có thật đúng HINT? | Dry-run/apply trên test84bdbac rồi so bytes | rc0/0, bằng HEAD, Δ dòng thêm0. |
| Thiếu họ M6 còn chết ở provider? | `pl_m6_state_cu_mat_ho` | Call3; status0; tuple0/3/true gây assertion suy — F18 đóng. |
| Vá F18 có mở lại suy0? | `pl_m6_suy_used_0` | Call3→0 trước status — F17 giữ đóng. |
| Fixture M6 đổi làm mutant reader chết sai nơi? | Toàn bộ15 mutant nhắm M6 | 13 reader/schema chết tại status đúng nhóm,2 M6 đúng chốt; baseline xanh. |
| Assertion M5 che trần/sổ/hình dạng? | Ba mutant riêng của M5 | Biên bản5/6/7 vẫn đo riêng đúng trần/sổ/hình dạng. |
| Quyết định rescue khác bị kiểm quá muộn? | `pl_m5_quyet_dinh_khac_mo` | Chết ngay assertion sau tach_stable_slice, trước revision — F16 giữ đóng. |
| Trục vòng che Codex hoặc sai ưu tiên? | M3_vong/M3_codex và mutant | Riêng vòng10/10, riêng calls2/2, cùng2/2 đều đúng. |
| Replay call bị reader che? | Replay b1 trên H1 | Setup lượt2 qua, review5→0 với b1=true. |
| State hỏng gây traceback/reset ngân sách? | reader/consistency/r2/r3/r4/r6/schema | Mẫu hỏng được giao bị8, không traceback; schema giữ used2/two calls; r6 giữ bytes. |
| Guard mới chặn nhầm luồng hợp lệ? | Hai checkpoint, void, v1 thật, identity hợp lệ | Hai lần mở0 rồi approve0; review sau void0; v1 Codex/Claude approve0;4 identity call0. |
| Có cửa khác ra khỏi blocked? | Driver bypass | Transition/begin/init8; void0 vẫn blocked; các quyết định khác0/blocked; nâng rồi mở0. |
| Sổ nâng thiếu hình dạng/review vượt vòng có lọt? | connector a/b và mutant | Rescue8/blocked; review11=3, giữ10/10. |
| Actor/URL có lỏng? | M4 âm/dương và mutant | Actor giả7; thiếu fragment/owner#/LF bị2; actor strip hợp lệ0. Mutant đoạn chỉ khóa riêng owner#. |
| Bản vá phá nền hoặc mutant ngoài pl_*? | Suite đầy đủ, đúng cwd KHO | rc0;351/351, skip1;144 mutant báo giết,1 skip Windows; đối chứng khác họ còn sống; ĐẠT. |
| Nâng nhiều lần/xen trục, tran_cu âm nhưng đủ khóa | **Ý tưởng bằng lời, chưa thêm dữ liệu chạy** | Cần kiểm tính nhất quán journal và sổ nâng; không coi là pass hoặc finding đã chứng minh. |
| JSON lồng sâu/khóa trùng, finding_ids sai kiểu nhưng count vẫn khớp | **Ý tưởng bằng lời, chưa thêm dữ liệu chạy** | Chưa đo; không khẳng định reader phủ mọi JSON. |

## Đã đo

Lệnh driver đều dùng `PYTHONDONTWRITEBYTECODE=1 python3.13 -B`; `DEV=KHO/.claude/dev` là đường tuyệt đối. r2/r4 nhận thêm `--repo KHO`; schema/conn nhận DEV ở đối số vị trí. [Lệnh, cwd, giờ và rc thật của chín process](driver-summary.json). Process rc0 chỉ xác nhận driver chạy xong; kết luận lấy từ mã con và state đọc lại. R4 có đối chứng runtime lịch sử trong cùng log; không gộp mã của bản lịch sử thành kết quả HEAD.

| Phép đo | Kết quả thật | Bằng chứng |
| --- | --- | --- |
| Exact HEAD/tree/SPEC/HINT | Khớp; detached; snapshot đầu sạch; hai tệp khớp blob HEAD | [snapshot](repo-initial.json), [SPEC](spec-wp775.md), [patch](HINT-F18.patch) |
| F18 patch | Dry/apply0/0, bytes bằng HEAD, Δ dòng thêm0 | [check](f18-patch-check.json) |
| F18/F17 và nền pl_* | 8/8 nền xanh; hai mutant đúng chốt, không traceback runtime | [summary](f18-first/summary.json) |
| Audit toàn bộ HEAD | 39 tên/40 ô;40 đúng chốt,0 sai;0 ô sống;0 traceback runtime | [summary](mutation-audit-head/summary.json), [phân loại](mutation-audit-head/classified.json) |
| review_probes reader | Process0;15/15 rc8 | [reader.log](reader.log) |
| review_probes consistency | Process0;2/2 rc8 | [consistency.log](consistency.log) |
| review_probes bypass | Process0;8×5,0×6; checkpoint giữ tới nâng hợp lệ | [bypass.log](bypass.log) |
| probes_r2 --repo KHO | Process0;54 mã con:0×23,3×6,8×25; luồng hợp lệ và v1 thật giữ đúng | [r2.log](r2.log) |
| probes_r3 | Process0;64 mã con:0×26,5×6,8×31,4×1 | [r3.log](r3.log) |
| probes_r4 --repo KHO | Process0;4 identity Codex call0,6 Claude call4/unchanged trên HEAD; mẫu metadata/projection sai8 | [r4.log](r4.log) |
| probes_r6 | Process0;41 lỗi8 giữ bytes;0 traceback | [r6.log](r6.log) |
| schema_probe DEV | Process0;hai lần status/action8/8, giữ used2 và hai calls | [schema.log](schema.log) |
| conn_probe DEV | Process0; a rescue8/blocked; b review11=3/blocked10/10; c không dựng được hai calls khác head | [connector.log](connector.log) |
| Full suite đúng cwd KHO | **rc0;351/351, skip1;145 mutant:144 báo giết,1 skip; TỔNG: ĐẠT** | [suite.log](suite.log), [command/rc](suite-run.json) |
| Bảng đột biến ngoài | Process0;GIET_THAT40,TIN_DUNG_GIA0,SONG0 | [bank-head.log](bank-head.log), [command/rc](bank-run.json) |
| Ruff bare F base/HEAD | rc1/1;runtime F8411/1,test F5412/2;delta0 | [quality](quality-summary.json), [base](ruff-F-base.json), [HEAD](ruff-F-head.json) |
| Ruff preview E302/E305 base/HEAD | rc1/1;runtime3/3,test5/5;delta0 | [base](ruff-spacing-base.json), [HEAD](ruff-spacing-head.json) |
| doctrine-scan base/HEAD | rc0/0;10 tệp,0 vi phạm | [base](doctrine-scan-base.log), [HEAD](doctrine-scan-head.log) |
| adr-song base/HEAD | rc0/0;50 ADR/50 dòng §20, khớp1–1; ngoại lệ trạng thái0016 giữ như nền | [base](adr-song-base.log), [HEAD](adr-song-head.log) |
| Snapshot cuối | HEAD/tree và hai hash giữ nguyên; detached;tracked/untracked/ignored sạch;diff worktree/index/check0;bytes bằng HEAD blob | [snapshot](repo-final.json) |

Giới hạn schema quan sát được: một số metadata không bắt buộc ở `status` (như review.verdict/reviewed_sha/finding_descs); head=None có thể status0 nhưng review5. Không gán các trường này thành bypass ngân sách chưa đo được. SyntaxWarning escape ở test3683 có ở nền, không phải traceback runtime.

Ruff được chạy trên bản sao bằng `ruff check --isolated --no-cache --select F --output-format json` cho hai tệp, và phép riêng thêm `--preview --select E302,E305`. Base/HEAD đều có sẵn3 lỗi F và8 lỗi spacing, delta0; không thay lint rc1 thành pass tuyệt đối. [Lệnh/rc/diagnostics](quality-summary.json). Các scan dùng hai runtime từ bản sao base/HEAD trên cùng root KHO chỉ đọc; toàn diff chỉ đổi hai tệp dev Python nên nguồn doctrine/ADR không đổi. Chưa kiểm Ruff pin/probe contract của workflow.

## KHÔNG ĐO ĐƯỢC

- Windows/pwsh: ca `luong_canonical_chay_that` và mutant tương ứng bỏ qua; không tính skip là pass.
- Launcher sinh output/token thật, binary CLI/model/effort/receipt, GitHub authority/comment, CI exact HEAD và quyền merge không được đo trong lượt cục bộ này; không gọi mạng.
- Không đo toàn bộ không gian JSON, lỗi filesystem, concurrency hay người dùng khác. Ý tưởng dữ liệu mới chỉ mô tả bằng lời; không tính là pass.
- Ruff pin/probe contract của workflow chưa đo; bare lint và delta được báo riêng.
- Snapshot đầu/cuối chứng minh không có delta quan sát được giữa hai mốc, không chứng minh toàn bộ lịch sử không từng ghi/hoàn nguyên. Không mở rộng review sang corpus, pháp luật, LIVE, publish hay deploy.

Bảy nợ ngoài spec r1 theo chỉ thị, **không tính lại và không tuyên bố đã đóng**: bằng chứng launcher; receipt trước khi đếm vòng; trần vòng theo ngày đóng băng spec; fallback/human_audited; kế thừa ngân sách giữa generation; đổi chéo cờ `da_dung` giữa hai lời gọi; lời gọi Codex cuối thất bại không tự vào rescue.

`VERDICT.md` đã được tạo trước phép đo đầu và cập nhật sau các phép đo. [Bản ghi tiến độ trước biên tập](VERDICT.measurements.txt) giữ các kết quả tích lũy; trace/log liên kết ở trên là hiện vật lượt17. Verdict này là kết luận review cục bộ trên exact HEAD, không thay CI/receipt/authority của bước merge.
