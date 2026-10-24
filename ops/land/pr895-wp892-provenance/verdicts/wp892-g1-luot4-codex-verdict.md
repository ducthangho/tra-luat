verdict: approve
reviewed_sha: 9bad91e9261a9097b0924718db3333da624e01cf
reviewed_tree: 2f830513aee427ee385e8a07c2c1280e4e8060c9
base_sha: 8324567788caab8dc332d45df458ef415fd305be

# Cross-review wp892 — lượt 4, PR #895, lớp sensitive

**APPROVE mã trên exact SHA trên: không còn P0/P1/P2 đo được.** P2 CLI lượt 3 đã đóng thật. Mutant P3 env vắng gốc đã bị bắt; giữ ba khoản nợ P3 bên dưới với quyết định **chấp nhận**, owner **executor wp892**, có bằng chứng và hướng xử lý riêng. **N4 GitHub thật: KHÔNG ĐO ĐƯỢC offline**, tách khỏi verdict mã; không suy approval này thành CI xanh, quyền merge/land hoặc packet hoàn tất.

Reviewer độc lập: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; execution surface agent API với `exec_command`, transport machine/local, session/run `523d11cc`. Không có attestation model/effort từng request hay xác nhận riêng launcher/CLI; không suy identity từ tài khoản GitHub. Không gọi subagent, không kế thừa context executor, không đăng GitHub. Mục tiêu assurance theo packet là cross-provider; biên nhận/delivery và identity gate không được tự tạo bởi file offline này. Hai trục review: spec và standards/security.

Đã đọc **toàn bộ** `runs/523d11cc/prompt.snapshot`. Áp chỉ thị lượt cuối nâng trần lên 5 trong prompt, spec **r2** SHA256 `aeac5b18566f4b9d3bd5f88d39503d44facd4029913793c32e01a43c3ff5dc9b`; không dùng r1. Spec cung cấp khớp byte với blob tại OID `d90d847f19b8a98b10ba63b8dfdb0672421acb28`, dù không nằm trong checkout mã. HEAD/tree và hai diff khớp; bốn tệp thuộc write set, diff-check rc 0; YAML parse chỉ hai job được phép thay đổi. [Định danh trước](evidence/invariants.json), [sau](evidence/readonly-after.json), [spec từ OID](evidence/spec-from-pinned-oid.md), [YAML](evidence/yaml-scope.json).

Đã tạo `VERDICT.md` pending ngay đầu và cập nhật sau các phép đo; [bản tăng dần trước khi chốt](evidence/working-verdict.txt). Các script dùng lại từ lượt 3 và các probe gốc mà lượt 3 gọi giữ nguyên byte; tìm lại bản gốc cục bộ `rv892c.I0su/evidence-luot2/`, copy ra sandbox, không lấy log cũ làm số đo head. [Hash và đối chiếu script](evidence/final-audits.json).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh: `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/new-hunts.py`. Script **nguyên văn**, cả 5 mục, builder/CA/classifier giữ nguyên. Mỗi mục đủ **61 CA**, chỉ t52 `giet_that`, **60 qua**, không skip/tín dụng giả, lỗi bán kính 0. [Audit gọn gồm lý do nguyên văn + witness](evidence/prior-audit.json), [log](evidence/new-hunts.log), [raw](evidence/new-hunts.json).

| Finding / biểu hiện lượt 3 | Phân loại lượt 4 | Output và assertion thật |
|---|---|---|
| P2 `gom-duong-nhanh-chua-khoa-dispatcher-cli`: `rv_cli_fast_valid_rc1` | **ĐÃ VÁ THẬT** | t52 1/61. `cli_git_dn_dung` rc **1** so với thường **0**, cả hai bảng đúng 490 dòng/0 lỗi. Witness head thường/nhanh **0/0**, mutant **0/1**, vẫn in `GOM MẢNH 3/3`. |
| Cùng P2: `rv_cli_fast_head_none` | **ĐÃ VÁ THẬT** | t52 1/61. Cặp Git dương mất HEAD riêng nhanh: head **0/0**, mutant **0/1 G-head**. Assertion so rc/toàn bảng/đối chứng, không cấm substring G-head. |
| Cùng P2: `rv_cli_fast_claim_kills` | **ĐÃ VÁ THẬT** | t52 1/61. `cli_dn_rong`/`cli_dn_khong_co`: mutant rc 0 nhưng dòng `GOM: KHÔNG ĐO — bị giết 0 đột biến` thiếu mode, có “giết”. Head rc 0 dòng đúng. |
| P3 `gom-tu-kiem-mat-doi-chung-env-vang`: `rv_selfcheck_absent_rc1` | **ĐÃ VÁ THẬT mutant gốc; giữ phần chưa phủ là P3 được chấp nhận. VÁ SINH LỖI MỚI P3 cờ nhẹ/định dạng, xem bên dưới.** | t52 1/61, lý do `cửa --tu-kiem-gom dưới env VẮNG (bản nhẹ) hỏng: rc=1` qua `bang`, không qua `dung`. Witness head vắng/nhanh **0/0**, mutant **1/0**. |
| Đối chứng `rv_bypass_changed_text` | **Vẫn khóa thật** | t52 1/61: CLI có mảnh rc 0/thiếu bảng không qua, dù đổi chữ shortcut. |

Các finding đã đóng ở lượt 3 cũng được đo lại bằng probe nguyên văn qua `python3 evidence/recheck.py`: `custom-new.py` bắt cả `rv_cli_fast_shards_skip`, `rv_cli_empty_success`, `rv_ignore_subdirs` đúng t52 1/61; `probe-env.py` cho cả 5 env vắng/nhanh/đầy đủ/sentinel/rỗng: t52 qua, selfcheck rc 0, env cha không đổi. `probe-fixture-order.py` giữ `.gitkeep` và hash ở cả hai thứ tự gọi. `probe-order.py` đảo cả hai bảng vẫn giữ bảy ô nghiệp vụ sau chuẩn hóa duy nhất đường tạm. Script order hardcode SHA lượt 2 nên dùng [Git shim](evidence/git-head-remap/git) **chỉ remap đối số OID** sang reviewed_sha, không sửa byte probe. Cột restored=False khi gọi helper trực tiếp là helper pop env trong tiến trình con theo thiết kế; probe t52 xác nhận cha không đổi. [Recheck](evidence/recheck-results.json), [custom](evidence/custom-new.json), [env](evidence/env.json), [fixture](evidence/fixture-order.json), [order](evidence/order.json), [audit order](evidence/final-audits.json).

## BẢNG LỚP

| Lớp đã quét | Bằng chứng mới / phạm vi | Quyết định |
|---|---|---|
| CLI nhanh thành công, mã thoát, vân tay, toàn bảng và lời khai shortcut | 5 probe lượt 3; 20 mutant đăng ký; cặp Git thật dương/3 lỗi; mutant mất chi tiết mới | P2 đóng; assertion nghiệp vụ thật. |
| Nguồn vân tay ↔ consumer, tín dụng giả | Mutation điều kiện tương đương sống 61/61 trên giàn chuẩn và HEAD-ready; f9/bn cũ giữ 1/61 | Không thấy hồi quy t53 sang t52. |
| Env ngoài ↔ bản nhẹ/nặng ↔ sản phẩm | 156 CLI, 6 giá trị cờ; main thật; mutant chỉ phá bản ĐỦ/env vắng | P3 giới hạn input và P3 cờ kế thừa: chấp nhận có căn cứ. |
| Hợp đồng dòng shortcut ↔ ghim định dạng | Mutation đổi lời đúng hợp đồng vẫn bị light assertion từ chối | P3 ghim quá chặt: chấp nhận, không nhận là kill nghiệp vụ. |
| So sánh mode chính xác | 50 giá trị theo lớp, chỉ chuỗi đúng rc 0 | Không lỗi mới ở head. |
| Artifact/đường dẫn có nội dung ↔ rỗng/vắng | 11 họ integrity, 9 hình dạng filesystem; 8 mảnh/vân tay thật | Hai mode cùng kết luận, không thấy bypass head. |
| Bán kính mới ↔ nền cũ | 20/20 mới đủ CA, 40 cũ A/B seed 892003, 3 f9/bn cũ riêng | Mới đúng 1/61; mẫu cũ delta 0. |
| Workflow/ruleset/runner thật | YAML/registry/actionlint và classifier cục bộ; không mạng | Mã không có finding mới; N4 chưa đo. |

## CẶP CLI GIT THẬT VÀ TÍN DỤNG GIẢ

`cli_git_dn_dung` ↔ `cli_git_dung` đã phân biệt được dispatcher chỉ ép đỏ **đường nhanh thành công**. Hai ô thường bị khóa độc lập bởi F16/F17: bộ đủ rc 0, 490 ok/0 đỏ; bộ 3 lỗi rc 1, 487 ok/3 đỏ; bảng **nguyên văn** bằng oracle và mã thoát khớp tổng lỗi. Hai ô nhanh phải bằng **toàn bộ** vector đối chứng, gồm cờ bảng nguyên văn và cờ rc, nên không còn “hai vế cùng G-head” che đường dương.

`probe-false-credit.py`: mutation đổi vế so sánh nhưng giữ ngữ nghĩa **SỐNG đủ 61/61** trên builder chuẩn không HEAD và builder có HEAD; không skip, không chết vì G-head. `probe-old-regression.py`: base/head `f9_sha_hang`, `f9_head_hang` chỉ giết **t53 1/61**; `bn_ban_kinh_giau_ly_do` chỉ giết **t29 1/61**, lỗi 0. Nguồn fixture dùng chính `_van_tay` của script đang đo, nên thay nguồn vân tay không cấp thêm kill t52. [Equivalent](evidence/false-credit.json), [f9/bn](evidence/old-regression.json). Diagnostic `registered-reasons.py` có HEAD-ready và chỉ t52; **không lấy diagnostic một ca làm bán kính 61 ca**. [Diagnostic](evidence/registered-reasons.json).

## P3 CÒN MỞ — QUYẾT ĐỊNH TƯỜNG MINH CHO LỚP SENSITIVE

### [P3] `gom-tu-kiem-mat-doi-chung-env-vang` — phần bản ĐỦ chưa được đối chứng dưới env vắng

**Vị trí:** `ops/cong_cu_test.py:7246`, `:8281`, cửa dispatcher `--tu-kiem-gom`. **Phép đo:** `r4_absent_full_only` chỉ trả rc 1 khi cửa selfcheck nhận env mode vắng **và cờ nhẹ khác 1**. Thân `--gop`/`main` không đổi. Qua `_ban_kinh_moi_dot_bien` thật: **SỐNG 61 qua/0 chết/0 skip**. Witness head đầy đủ-vắng/nhẹ-vắng/đủ-nhanh **0/0/0**, mutant **1/0/0**. Đây là đúng giới hạn executor tự khai, đã đo độc lập. [Neo/thay + đủ trạng thái + witness](evidence/r4_absent_full_only.json).

**Quyết định: CHẤP NHẬN nợ P3**, owner **executor wp892**, tên nợ giữ nguyên ID trên; không chặn merge mã. Lý do: lỗi giả chỉ nằm ở một input của **cửa tự kiểm nội bộ**; đối chứng nhẹ đã bắt mutant gốc, bản đầy đủ vẫn chạy dưới env thù địch, và `--gop` env vắng/nhanh đã có đối chứng trực tiếp lẫn CLI. Chưa có bằng chứng head gom sai hoặc bỏ kiểm sản phẩm. Một mẫu đo tuần tự dưới tải hiện tại: bản ĐỦ rc 0, **14,5852 s**, 102 khóa KQ; NHẸ rc 0, **0,5365 s**, 2 ô lõi + marker. Đây là một mẫu, không phải benchmark thống kê. Nhân đôi toàn bộ fixture ở mỗi mutant mua thêm độ phủ nội bộ với chi phí đo được, không phải blocker N1 hiện tại. [Số đo](evidence/light-cost.json), [script](evidence/light-cost.py).

**Vá ở đâu/thế nào:** giữ input thù địch của t52, bổ sung đối chứng env vắng của phần ĐỦ theo một gate riêng ít tần suất hoặc rút phần kiểm cửa chung để hai biến thể cùng đi qua; không cần sửa consumer gom. **Ca khóa:** `r4_absent_full_only` phải bị từ chối ở input vắng; `wp892_ro_env_ngoai` vẫn chết đúng, 60 ca khác qua. **Nguy cơ vá:** nhân đôi chi phí mọi radius, mất input thù địch nếu thay thế thay vì bổ sung, hoặc tính tín dụng giả nếu cửa chết trước assertion nghiệp vụ.

### [P3] `gom-co-nhe-ke-thua-lam-do-main` — cờ ngoài làm đầy đủ thành nhẹ

**Vị trí:** `ops/cong_cu_test.py:7246` (env của lời gọi ĐỦ), `:8281`. **Phép đo:** t52 trực tiếp dưới cờ ngoài `CONG_CU_TEST_TU_KIEM_GOM_NHE=1` trả `tin_dung_gia`, `KeyError: 'dung'`. Lệnh **sản phẩm không đối số thật** với cấu hình mảnh hợp lệ `CONG_CU_TEST_MANH=0/8`, đường ra tạm và cờ ấy: rc **1**, **60/61**, lỗi duy nhất t52, `[M-nen]`, **không artifact**. [Raw](evidence/main-light.json), [script](evidence/main-light.py).

Cờ **có thể đổi hành vi main theo hướng đỏ** vì main chạy ca t52; không tuyên bố “không ảnh hưởng sản phẩm”. Với `--gop`, 13 trạng thái artifact × 2 mode × 6 giá trị cờ (vắng/rỗng/0/1/true/2) = **156 lời gọi**, toàn bộ rc/stdout/stderr bằng nhau. Main cấu hình sai giữ rc 2 ở cả sáu; fixture dây nối main bằng nhau cả sáu. AST chỉ thấy cờ ở t52, khai báo module, `_in_tu_kiem_gom`, không có nhánh bypass ở `_main_gop`/main. [Matrix](evidence/independent-runtime.json), [AST](evidence/final-audits.json).

**Quyết định: CHẤP NHẬN nợ P3**, owner **executor wp892**: đây là biến nội bộ phải bị caller chủ động đưa ra ngoài; workflow không đặt nó, t52 chỉ truyền vào env tiến trình con và probe xác nhận cha không bị đổi. Hậu quả đo được fail-closed, không tạo xanh giả, không ghi shard sai; không đủ mức chặn merge.

**Vá ở đâu/thế nào:** t52 lọc cờ nhẹ khỏi env của lời gọi ĐỦ, chỉ đặt `1` ở lời gọi NHẸ; giữ phần consumer nguyên. **Ca khóa:** chạy t52 dưới vắng/0/1/giá trị lạ của cờ ngoài phải như nhau, mutant bỏ cô lập phải bị bắt; kiểm env cha giữ nguyên. **Nguy cơ vá:** lọc nhầm cờ ở cả hai lời gọi làm mất đối chứng nhẹ hoặc tăng thời gian, và sửa môi trường cha sẽ gây rò thứ tự fixture.

### [P3] `gom-ban-nhe-ghim-dinh-dang-ngoai-hop-dong` — lời đúng hợp đồng bị coi là lỗi

**Vị trí:** `ops/cong_cu_test.py:7261`, assertion nhẹ bắt chuỗi `=duong_nhanh, 0 mảnh`. **Phép đo:** `r4_valid_shortcut_wording` chỉ đổi lời shortcut thành `GOM: KHÔNG ĐO — hồ sơ; CONG_CU_TEST_GOP_CHE_DO=duong_nhanh; 490 đột biến không chạy…`, vẫn đúng một dòng, rc 0, có KHÔNG ĐO/mode, không chữ “giết”. Witness head/mutant đều đạt đủ hậu điều N1, mode thường vẫn rc 1. Nhưng bộ thật báo t52 `giet_that`, **1/61**, vì thiếu đúng dấu phẩy/nhóm “0 mảnh” ở assertion NHẸ; 60 ca khác qua. Đây là **kill giả theo ngữ nghĩa hợp đồng**, dù classifier nhận đúng kiểu exception `bang`; không dùng nó làm bằng chứng bộ có răng. [Neo/thay + radius + witness contract_ok](evidence/r4_valid_shortcut_wording.json).

**Quyết định: CHẤP NHẬN nợ P3**, owner **executor wp892**: ghim quá chặt chỉ cản một lần đổi lời hợp lệ trong tương lai; head hiện tại thỏa hợp đồng và cả 20 mutant đăng ký đều làm sai thuộc tính nghiệp vụ thật. Không có false green sản phẩm hoặc radius cũ đổi trong mẫu đo.

**Vá ở đâu/thế nào:** assertion hai ô NHẸ nên đòi rc/số lần vân tay và dấu hợp đồng KHÔNG ĐO + mode đúng + không “giết”, cùng G-rong cho ô vắng; tránh neo dấu câu không thuộc hợp đồng. **Ca khóa:** mutant lời hợp lệ trên phải sống; `rv_cli_fast_claim_kills`, `wp892_dong_gia_giet`, bỏ nhánh, rc sai và env vắng phải vẫn bị đúng t52 bắt. **Nguy cơ vá:** nới quá mức bỏ mất kiểm mode/giết/rc/vân tay hoặc tái tạo tín dụng giả bằng cấm substring G-head rộng.

## 20 MUTANT ĐĂNG KÝ — BÁN KÍNH VÀ LÝ DO

Lệnh nguyên văn lượt 3: `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/radius.py new`.

Từng mục gọi **`_ban_kinh_moi_dot_bien([name], (), 1)` thật**, CA/builder/classifier không thay; wrapper chỉ ghi lại raw cases khi classifier thật được gọi. **20/20**, mỗi mục 61 trạng thái: **t52 giet_that + 60 qua**, không skip/tin_dung_gia; lỗi 0. Đã đọc lý do từng mục: lỗi rc/dòng/mode/fixture đúng input mà mutant làm sai, không chết vì cấm G-head hoặc rig thiếu HEAD. Các mục chết sớm ở đối chứng NHẸ vẫn đo đúng hai input lõi (nhanh+rỗng, vắng+rỗng). [Raw](evidence/radius-new.json), [audit gồm lý do nguyên văn](evidence/radius-audit.json), [log](evidence/radius-new.log).

| Mutant | Kết quả thật | Assertion/fixture gây chết |
|---|---|---|
| `wp892_bo_nhanh` | t52, 1/61; lỗi 0 | NHẸ `dn_rong`: rc 1/G-rong, gọi vân tay 1 thay shortcut. |
| `wp892_strip` | t52, 1/61; lỗi 0 | `dn_cach`, `dn_cr` rc 0 sai. |
| `wp892_lower` | t52, 1/61; lỗi 0 | `dn_hoa` rc 0 sai. |
| `wp892_tien_to` | t52, 1/61; lỗi 0 | `dn_cach`, `dn_tien_to`, `dn_cr` rc 0 sai. |
| `wp892_vang_la_nhanh` | t52, 1/61; lỗi 0 | NHẸ `dn_vang`: shortcut rc 0, thiếu G-rong. |
| `wp892_bo_dk_rong` | t52, 1/61; lỗi 0 | `dn_dung`, `dn_thieu` bị shortcut thay gom. |
| `wp892_nhan_tep` | t52, 1/61; lỗi 0 | `dn_tep` rc 0 sai. |
| `wp892_rc_do` | t52, 1/61; lỗi 0 | `dn_rong`, `dn_khong_co` rc 1 thay 0. |
| `wp892_hau_to` | t52, 1/61; lỗi 0 | `dn_dau` rc 0 sai. |
| `wp892_bo_cr` | t52, 1/61; lỗi 0 | `dn_cr` rc 0 sai. |
| `wp892_lo_tep_an` | t52, 1/61; lỗi 0 | `dn_tep_an` rc 0 sai. |
| `wp892_dispatcher_nhanh_rc1` | t52, 1/61; lỗi 0 | CLI rỗng/vắng rc 1 và stdout rỗng; cặp Git dương sai. |
| `wp892_dispatcher_nhanh_bo_gom` | t52, 1/61; lỗi 0 | CLI rỗng/vắng/bộ Git rc 0 nhưng thiếu toàn bộ stdout. |
| `wp892_dispatcher_rong_xanh` | t52, 1/61; lỗi 0 | `cli_dn_trong` rc 0/stdout rỗng. |
| `wp892_bo_qua_thu_muc_con` | t52, 1/61; lỗi 0 | `dn_con` rc 0 sai. |
| `wp892_ro_env_ngoai` | t52, 1/61; lỗi 0 | `cli_tt_rong`, `cli_tt_ten_cua` bị shortcut do env ngoài. |
| `wp892_dispatcher_nhanh_thanh_cong_do` | t52, 1/61; lỗi 0 | `cli_git_dn_dung` rc 1 so với rc 0 thường; bảng vẫn đúng. |
| `wp892_dispatcher_noi_giet` | t52, 1/61; lỗi 0 | CLI rỗng/vắng thiếu mode, có chữ “giết”. |
| `wp892_tu_kiem_vang_rc1` | t52, 1/61; lỗi 0 | Cửa tự kiểm env vắng NHẸ rc 1; assertion `bang` của t52. |
| `wp892_dong_gia_giet` | t52, 1/61; lỗi 0 | NHẸ `dn_rong` sai dấu shortcut: GOM MẢNH, có “giết”, thiếu KHÔNG ĐO. |

## N3 — 470 TÊN CŨ VÀ MẪU RUNTIME CŨ

`python3 evidence/radius.py static`: **61 tên/thứ tự CA giữ nguyên, 470/470 định nghĩa mutant cũ giữ nguyên**, gồm binding/phụ thuộc/đích và thứ tự tương đối; số lần xuất hiện từng mỏ neo cũ thay đổi **0**. Head **490 = 470 + 20**. [Raw](evidence/n3.json).

`PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/radius.py sample`: **một invocation, hai vế**, cùng `_ban_kinh_moi_dot_bien`, đầy đủ CA, không loại ca nền. `random.Random(892003).sample` chọn **40** trong **403** mutant cũ có đích khác t52; seed/danh sách ghi trước đo, đúng script lượt 3. Base **40/40, lỗi 0**; head **40/40, lỗi 0**; **delta phân hạng 0**. Phủ mẫu ngẫu nhiên **40/470 = 8,51%**, không khai đo hết 470. [Danh sách/seed](evidence/sample-names.json), [base](evidence/sample-base.json), [head](evidence/sample-head.json), [delta](evidence/sample-delta.json), [log](evidence/sample.log). Ba f9/bn đo riêng giữ nguyên radius như trên; N126 cổng chuẩn còn tự kiểm ba mutant thật tuần tự/song song. Số 490 “giao mảnh” là kích thước bảng, **không phải lời khai đã chạy toàn bộ 490 radius** trong lệnh gate.

## TÁI LẬP HAI VẾ

Bản sao từ `mktemp -d` + `git -C cay-kho archive <OID>`, Git init/fetch **mirror cục bộ**, reset mixed về đúng OID; `core.abbrev=7`, autocrlf false/EOL LF, commit.gpgsign false. `PYTHONDONTWRITEBYTECODE=1` ở các phép Python đo repo. Python **3.13.16**, PyYAML 6.0.3; CI ghim **3.12**, chưa đo parity interpreter. Ruff 0.16.9, actionlint 1.7.7 ([môi trường](evidence/environment.json)); không có ShellCheck trong sandbox, không khai đã chạy luật ShellCheck.

Lệnh cặp đầu `PYTHONDONTWRITEBYTECODE=1 python3 evidence/reproduce.py` giữ từng rc/stdout/stderr; base scanner timeout 120 s, head rc 0. Lệnh cặp retry `PYTHONDONTWRITEBYTECODE=1 python3 evidence/quiet-final.py` chạy **cùng command/env hai vế trong một invocation**, hai vế tuần tự, sau các nhóm radius lớn/hồi quy và song song nhóm săn cuối một worker; không đổi code hoặc timeout. Retry base 314.18 s, head 348.73 s, đều rc 0. Bản snapshot giữa chừng trong reproduction có ghi **complete=false**, chỉ dùng khởi động batch độc lập; file results cuối là đủ 14 phép thật, không dùng snapshot làm pass evidence. [Driver/stages](evidence/run-stages.py), [initial results](evidence/reproduction/results.json), [retry results](evidence/reproduction/cong-cu-quiet-results.json).

| Phép đo | Base | Head |
|---|---|---|
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` — retry cặp | rc **0**, **61/61**, bỏ qua/tiền kiểm 0; **470 giao mảnh**, lỗi đột biến 0, cây thật ĐẠT | rc **0**, **61/61**, bỏ qua/tiền kiểm 0; **490 giao mảnh**, lỗi đột biến 0, cây thật ĐẠT |
| `python3 ops/ci_duong_nhanh_test.py` | rc **1**; CA: 103/104 dat · 0 do · 1 hong<br>DOT BIEN: 379/384 bi giet dung ly do<br>TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that) | rc **1**; CA: 103/104 dat · 0 do · 1 hong<br>DOT BIEN: 387/392 bi giet dung ly do<br>TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that) |
| `python3 .claude/dev/ci_dang_ky_test.py` | rc **0**, **1064/1064 đỏ đúng**, TỔNG ĐẠT | rc **0**, **1070/1070 đỏ đúng**, TỔNG ĐẠT |
| `python3 ops/lease_publish_test.py --chi-ca=t16` | rc **0**, **9/9**, chạy 9/bỏ qua 0, gồm t16x nguồn os | như base |
| `actionlint .github/workflows/ci.yml` | rc **0**, stdout/stderr rỗng | rc **0**, stdout/stderr rỗng |
| `ruff check --no-cache --select F --output-format json .` | rc **1**, **8807** finding nền | rc **1**, **8807**, Counter relative-path/rule/message **added=[], removed=[]**, delta **0** |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc **0**, **10 tệp, 0 vi phạm** | như base |

[Log cổng base](evidence/reproduction/cong-cu-quiet-base.log), [head](evidence/reproduction/cong-cu-quiet-head.log), [toàn bộ logs](evidence/reproduction/), [tổng hợp initial](evidence/reproduction-summary.json), [Ruff delta](evidence/ruff-delta.json).

**Classifier không xanh:** cả hai cùng t20zo `socket.bind PermissionError [Errno 1]`. Đúng năm mục thiếu tiền đề ở cả base/head: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Tám mục mới bị giết đúng. Không có timeout trong lượt classifier này; không gọi năm mục đó là survivor nghiệp vụ và không khai 104/104 hay 392/392. Script retry timeout cũ cũng đã được chạy lại nguyên văn, hai tên `ca_du_lieu_bo_t27`, `ca_du_lieu_bo_qua_rc` GIET cả hai vế; điều đó không sửa tỷ lệ raw trên. [Classifier base](evidence/reproduction/ci-base.log), [head](evidence/reproduction/ci-head.log), [hai witness cũ](evidence/ci-timeouts-retry.json).

## SĂN ĐỘC LẬP MỚI THEO LỚP

Lệnh `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/independent-runtime.py` và `python3 evidence/independent-mutants.py`. Mỗi mutant mới qua classifier/builder thật, đủ **61 CA**; không suy từ tên assertion. [Script runtime](evidence/independent-runtime.py), [raw runtime](evidence/independent-runtime.json), [script mutant](evidence/independent-mutants.py), [raw mutant](evidence/independent-mutants.json).

| Hướng độc lập / khái quát lớp | Quét và output | Kết luận |
|---|---|---|
| Cờ nhẹ rò từ helper sang runtime | 13 artifact × 2 mode × 6 giá trị cờ = 156 CLI; main cấu hình sai và dây nối 6 giá trị; main mảnh thật cờ 1 | `--gop` delta 0; main lỗi đỏ vì t52, P3 được chấp nhận. |
| Tách bản nhẹ khỏi bản đầy đủ có che hỏng cửa nội bộ? | `r4_absent_full_only` SỐNG 61/61; witness chỉ đủ/env vắng 0→1, nhẹ và env thù địch giữ 0 | P3 giới hạn đã tự khai, xác nhận độc lập/chấp nhận. |
| Oracle dòng shortcut có khóa hợp đồng hay cả dấu câu? | `r4_valid_shortcut_wording` chết t52 1/61 dù witness thỏa hợp đồng cả hai | P3 false positive theo ngữ nghĩa, chấp nhận; không cấp tín dụng nghiệp vụ. |
| Consumer nhanh có bỏ integrity hoặc chi tiết lỗi riêng dispatcher? | 11 họ artifact dưới 2 mode; `r4_cli_fast_trust_header` và `r4_cli_fast_drop_detail` chết đúng t52 1/61 | Head parity; chốt còn răng, không thấy blocker. |
| Chuỗi mode có bị chuẩn hóa rộng? | 50 giá trị: xóa/đổi hoa từng ký tự, tiền/hậu tố, whitespace/control/Unicode hai đầu, đồng tự | Chỉ đúng `duong_nhanh` rc 0 trên rỗng; còn lại rc 1. |
| Rỗng có bỏ qua mọi dạng entry không phải shard? | 9 kiểu: file, hidden, child dir, FIFO, symlink con gãy, root link tới rỗng/file/vắng/có mảnh | 6 kiểu sai rc 1; root link giải theo đích (rỗng/vắng shortcut, có mảnh gom đủ), không phát hiện lỗi theo hợp đồng thư mục. |

Artifact 8 mảnh/490 tên được dựng bằng writer thật với các bản ghi tự kiểm để thử consumer, **không phải 490 phép đo mutation đã chạy**. Trường hợp có nội dung ở 11 họ cho kết quả rc/stdout/stderr y hệt thường/nhanh, gồm hợp lệ rc 0, thiếu rc 1 G-tap, stale hash/head rc 1 G-van-tay, đích sống rc 1, tệp/thư mục lạ, header hỏng, duplicate, tên lạ, sai phân hoạch. Không tuyên bố phủ mọi filesystem hoặc mọi chuỗi Unicode.

## N4 VÀ GIỚI HẠN

**N4 lượt thật GitHub: KHÔNG ĐO ĐƯỢC offline.** Không có jobs API/log trên exact reviewed_sha để xác nhận 8 shard day_du/gom xanh, PR hồ sơ với shard skipped/gom xanh/KHÔNG ĐO hoặc phút runner, và chưa so từng conclusion PR head/master thật. Scheduler Actions, ruleset đang hoạt động, output thiếu→env rỗng, download-artifact và branch head GitHub hiện tại không được fixture local xác thực. Các điều kiện merge N4/CI thật còn thuộc approver/operator, không biến thành pass từ approval mã.

Mọi đột biến/thử nghiệm trên archive/scratch ngoài checkout `cay-kho/`. Kiểm sau cùng HEAD/tree, status kể cả untracked/ignored, diff/index và byte bốn tệp đều giữ nguyên; hai checkpoint không chứng minh mọi thao tác trung gian. Không mạng, không GitHub write, không sửa branch executor, không merge/land/deploy. [Readonly sau](evidence/readonly-after.json).
