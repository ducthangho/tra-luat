verdict: changes_requested
reviewed_sha: 7849d1cdbab50b3b4a1a296a3867ce0939732b02
reviewed_tree: 6e40cea57a3595a313d1bf613f1c65820b5dc877
base_sha: 8324567788caab8dc332d45df458ef415fd305be

# Cross-review wp892 — lượt 3, PR #895, lớp sensitive

Còn **1 P2** (lớp CLI của lượt 2 chưa đóng hết) và **1 P3 mới** (mất đối chứng env vắng của cửa tự kiểm). Ba mutant cụ thể của lượt 2 đều được bắt thật; lỗi tín dụng giả đã hết ở các phép đo được yêu cầu. Tuy nhiên các mutant CLI nhanh trả ĐỎ trên bộ mảnh hợp lệ hoặc in lời “giết” trái hợp đồng vẫn sống đủ 61 ca. **Không approve mã.** N4 GitHub thật: **KHÔNG ĐO ĐƯỢC**, tách khỏi kết luận mã.

Reviewer độc lập: Codex/OpenAI, họ GPT-6 theo cấu hình phiên; công cụ `exec_command` qua API, transport machine/local. Không có attestation model/effort từng request hoặc xác nhận riêng bề mặt launcher/CLI; không suy từ tài khoản GitHub. Không gọi thêm reviewer/subagent. Đã đọc trọn `runs/8a8a68a5/prompt.snapshot`; dùng spec r2, không dùng r1 để nghiệm thu. Đã tạo verdict pending ngay đầu và cập nhật tăng dần; [lịch sử](evidence/working-verdict.txt).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Các script dưới đây là **nguyên văn** ở `evidence-luot2/`, chạy mới trên archive head. Không lấy log lượt 2 làm số đo head. [SHA256 script dùng lại](evidence/reused-script-sha256.json).

| Finding lượt 2 | Phân loại lượt 3 | Output thật |
|---|---|---|
| P2 `gom-cli-tep-an-cap-tin-dung-gia` | **ĐÃ VÁ THẬT — đóng trong phạm vi đo** | `probe-false-credit.py`: mutation tương đương SỐNG, 61 qua/0 chết/0 skip trên giàn chuẩn KHÔNG HEAD; đối chứng có HEAD cũng sống. `probe-old-regression.py`: f9_sha_hang, f9_head_hang, bn_ban_kinh_giau_ly_do giữ 1/61, lỗi 0 ở cả base/head. [Equivalent](evidence/false-credit.json), [old](evidence/old-regression.json). |
| P2 `gom-duong-nhanh-chua-khoa-dispatcher-cli` | **ĐÃ VÁ THẬT hai biểu hiện cũ; CHƯA ĐÓNG toàn lớp** | `custom-new.py`: rv_cli_fast_shards_skip và rv_cli_empty_success đều giết đúng t52 1/61; lý do lần lượt CLI có mảnh rc 0/stdout rỗng và cli_dn_trong rc 0. Không phải chết vì cấm G-head. Nhưng CLI dương có vân tay hợp lệ và hậu điều dòng shortcut còn hở, xem P2 dưới. [Số đo](evidence/custom-new.json). |
| P2 `gom-ca-cu-ke-thua-env-duong-nhanh` | **ĐÃ VÁ THẬT — đóng biểu hiện gốc; VÁ SINH LỖI MỚI P3 riêng** | `probe-env.py`: cả vắng/duong_nhanh/day_du/outer-sentinel/rỗng: t52 qua, selfcheck rc 0, env cha giữ nguyên; 7 ô fixture mà probe lưu giống nhau sau chuẩn hoá đường tạm. [Raw](evidence/env.json), [tổng hợp](evidence/env-summary.json). |
| P3 `gom-thieu-doi-chung-ngoai-gia-tri-va-thu-muc` | **ĐÃ VÁ THẬT — đóng** | `rv_ignore_subdirs` bị giết đúng t52 1/61, lý do dn_con rc 0 KHÔNG ĐO; witness head rc 1 G-tep, mutant rc 0. [Số đo](evidence/custom-new.json). |

`probe-fixture-order.py`: direct→CLI và CLI→direct đều rc 1 G-dau, .gitkeep tồn tại/hash không đổi. `probe-order.py`: đảo cả bảng trực tiếp/CLI không đổi 7 ô nghiệp vụ mà probe lưu. Script order hardcode OID lượt 2; đã giữ nguyên byte script, dùng [Git shim cục bộ](evidence/git-head-remap/git) chỉ đổi đối số OID cũ thành reviewed_sha cho archive/fetch. [Log](evidence/order.log), [JSON](evidence/order.json). Khi gọi trực tiếp `_in_tu_kiem_gom` trong cùng tiến trình, biến env bị pop là chủ ý của helper dành cho subprocess; `probe-env.py` xác nhận môi trường cha t52 không đổi. Không coi cột restored=False của phép gọi helper trực tiếp là hồi quy cha.

## FINDINGS

### [P2] `gom-duong-nhanh-chua-khoa-dispatcher-cli` — ô CLI dương cùng lỗi vẫn bằng nhau; lời khai shortcut thiếu chốt

**Vị trí:** `ops/cong_cu_test.py:7295`, `:7302`, `:8480`, `:8506`. Spec N1 yêu cầu `TEP_TEST --gop` dưới mode nhanh với đủ mảnh **hợp lệ** phải gom thật. Bảng mới so rc/dòng đầu của `cli_dn_dung`/`cli_th_dung` và `cli_dn_thieu`/`cli_th_thieu`, nhưng `dung` chứa vân tay giả cố định. Ở cây mutant không Git, hai vế cùng G-head; ở cây Git thật, vân tay vẫn không khớp. Các ô này đòi rc ≥1 và không bao giờ chứng minh CLI nhanh có thể gom thành công. F17 có kho Git/vân tay thật nhưng chỉ chạy env thường. Vì vậy lỗi chỉ ảnh hưởng đường CLI nhanh thành công vẫn lọt.

**Phép đo:**

```sh
PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/new-hunts.py --only rv_cli_fast_valid_rc1
```

Mutation chỉ sửa dispatcher: gọi nguyên `_main_gop()`, sau đó ép rc 1 khi mode chính xác là nhanh và có manh-*.txt. **SỐNG: 61 qua, 0 chết/skip** qua `_ban_kinh_moi_dot_bien([name], (), 1)`. Witness tạo đúng 487 tên, đủ 3 mảnh/header khớp từng script và HEAD: head thường/nhanh **0/0**, mutant thường/nhanh **0/1**; cả bốn lần đều in `GOM MẢNH 3/3`. Mutation không cần hardcode lỗi G-head. [Neo/thay, radius đủ 61 ca, witness](evidence/rv_cli_fast_valid_rc1.json), [log](evidence/new-hunt-valid-rc1.log).

Đối chứng khác: `rv_cli_fast_head_none` chỉ làm mất HEAD riêng dispatcher CLI nhanh có mảnh, cũng **SỐNG 61/61**; witness head 0/0, mutant 0/1 G-head. [Dữ liệu đã sửa witness](evidence/rv_cli_fast_head_none.json).

Một biểu hiện khác cùng lớp: CLI shortcut chỉ đòi rc 0 và substring `KHÔNG ĐO`; không khoá mode hoặc cấm “giết”. `rv_cli_fast_claim_kills` thay riêng shortcut CLI thư mục rỗng/vắng thành rc 0 `GOM: KHÔNG ĐO — bị giết 0 đột biến`, **SỐNG đủ 61 ca**. Head in dòng đúng; mutant thiếu che_do và có “giết”, trái hợp đồng. Ca trực tiếp vẫn chạy thân `_main_gop` đúng nên không bắt dispatcher này. [Dữ liệu](evidence/rv_cli_fast_claim_kills.json), [log witness](evidence/witness-claim-kills-corrected.log).

**Vá ở đâu/vì sao:** tại t52/_in_tu_kiem_gom, vì thiếu đối chứng ở cửa CLI, không có bằng chứng cần sửa runtime head. **Vá thế nào:** tái dùng kho Git tạm F17 với vân tay từ đúng script để chạy cả thường và nhanh; đòi đủ mảnh rc 0 và thiếu mảnh rc 1 đúng chốt. Kiểm đủ KHÔNG ĐO + mode chính xác + không “giết” cho CLI shortcut. **Ca khoá:** các survivor trên phải bị từ chối đúng t52; mutation tương đương vẫn sống và f9/bn cũ vẫn 1/61. **Rủi ro:** tự băm fixture độc lập với `_van_tay` gây t52 giết mutant t53; cấm substring rộng lại tái tạo tín dụng giả G-head. Độ tin cao.

### [P3] `gom-tu-kiem-mat-doi-chung-env-vang` — env thù địch cố định mất đối chứng cửa tự kiểm khi biến ngoài vắng

**Vị trí:** `ops/cong_cu_test.py:7240`. t52 luôn gọi `--tu-kiem-gom` với env ngoài duong_nhanh. `rv_selfcheck_absent_rc1` chỉ cho cửa tự kiểm thoát 1 khi biến mode vắng, không sửa `--gop`. Nó **SỐNG đủ 61 ca**. Witness head vắng/nhanh rc 0/0; mutant rc **1/0**. Cùng mutation trên archive lượt 2, gọi t52 với danh sách CA nguyên vẹn: bị từ chối `tin_dung_gia`, “giàn giáo hỏng … cửa --tu-kiem-gom hỏng rc=1”. Đây là lỗi giàn trước kia phát hiện, không gọi đó là kill nghiệp vụ. [Head](evidence/rv_selfcheck_absent_rc1.json), [đối chiếu trước/sau](evidence/absent-entry-contrast.json).

Mức P3 vì mất đối chứng giao diện nội bộ; chưa chứng minh `--gop` sản phẩm sai dưới env vắng (các ô CLI vắng vẫn có). **Vá:** tại t52 giữ cả env vắng và env thù địch, có thể dùng đối chứng entry nhẹ cho vắng để tránh nhân đôi toàn fixture. **Khoá:** mutant trên phải bị từ chối ở input vắng, wp892_ro_env_ngoai vẫn chết đúng ở input nhanh. **Rủi ro:** chạy hai lần toàn fixture làm tăng mạnh chi phí từng radius; không thay bỏ input thù địch. Nợ đề xuất owner executor wp892, cùng packet; chưa có quyết định chấp nhận nợ của chủ kho.

## TÁI LẬP HAI VẾ

Archive bằng mktemp + `git -C cay-kho archive <OID>`, Git init/fetch **mirror cục bộ** và reset mixed về đúng OID. `core.abbrev=7`, autocrlf false, EOL LF. Tất cả phép đo Python có `PYTHONDONTWRITEBYTECODE=1`; tắt ký commit cho tiến trình bằng GIT_CONFIG_COUNT/KEY_0/VALUE_0 như lệnh trên. Python 3.13.16, PyYAML 6.0.3; CI ghim Python 3.12, không đồng nhất môi trường. Ruff 0.16.9, actionlint 1.7.7.

Lệnh cặp: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/reproduce.py`. Driver chạy cùng command/env trên base/head trong một invocation, giữ rc/stdout/stderr riêng. Sau lỗi timeout, `PYTHONDONTWRITEBYTECODE=1 python3 evidence/retry-cong-cu.py` đợi các lượt nặng kết thúc rồi chạy cùng command cong-cu trên cả hai vế tuần tự; không tăng timeout, không sửa code. [Toàn bộ log](evidence/reproduction/).

| Phép đo | Output thật |
|---|---|
| `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py` | **base** rc 0: cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0<br>SỐ LIỆU: ca=61 · đột biến=470 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT; **head** rc 0: cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0<br>SỐ LIỆU: ca=61 · đột biến=487 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT |
| `python3 ops/ci_duong_nhanh_test.py` base | rc 1; CA: 103/104 dat · 0 do · 1 hong<br>DOT BIEN: 377/384 bi giet dung ly do<br>TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that) |
| `python3 ops/ci_duong_nhanh_test.py` head | rc 1; CA: 103/104 dat · 0 do · 1 hong<br>DOT BIEN: 385/392 bi giet dung ly do<br>TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that) |
| `python3 .claude/dev/ci_dang_ky_test.py` | rc 0/0; 1064/1064 → **1070/1070**, TỔNG: ĐẠT. |
| `python3 ops/lease_publish_test.py --chi-ca=t16` | rc 0/0; **9/9**, đã chạy 9, bỏ qua 0 mỗi vế; có t16x nguồn os. |
| `actionlint .github/workflows/ci.yml` | rc 0/0; stdout/stderr rỗng. ShellCheck không cài (command not found), không khai đã chạy luật shell. |
| `ruff check --no-cache --select F --output-format json .` | rc 1/1; **8807/8807** finding nền; Counter relative path/rule/message: added=[], removed=[], **delta 0**. Không khai lint xanh. |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc 0/0; **10 tệp, 0 vi phạm**. |

Lượt cong-cu đầu CA **61/61, 0 skip** cả hai vế, rồi cùng TimeoutExpired 120 giây ở quét cây thật `bash_nen.py quet`; không dùng số CA đó để khai toàn cổng xanh. Lượt retry nhẹ tải **rc 0/0**, cổng cây thật ĐẠT, lỗi đột biến 0; không thay timeout hoặc code. CI classifier có cùng lỗi nền t20zo socket.bind PermissionError Errno 1 ở hai vế; các mục thiếu tiền đề môi trường hoặc timeout được ghi nguyên văn trong log, **không coi là survivor nghiệp vụ** và không khai 104/104 · 392/392 xanh. Ruff delta ở [JSON](evidence/ruff-delta.json); [tổng hợp reproduction](evidence/reproduction-summary.json). Retry nguyên script `python3 evidence-luot2/retry-classifier-timeouts.py`: hai timeout `ca_du_lieu_bo_t27`/`ca_du_lieu_bo_qua_rc` đều **GIET trên mỗi vế**, 9,52–20,44 giây/mục, vẫn hạn 120 giây; không đổi tỷ lệ raw. [Log base](evidence/ci-timeouts-base.log), [head](evidence/ci-timeouts-head.log), [cặp](evidence/ci-timeouts-retry.json). Năm mục thiếu tiền đề socket: symlink_treo_khong_theo_bi_danh, la_bo_chot_tep_thuong, la_cho_phep_fifo, la_cho_phep_socket, la_khong_theo_symlink.

## N3 — ĐỊNH DANH VÀ MẪU RUNTIME CŨ

Head/tree/spec khớp; SPEC r2 SHA256 `aeac5b18566f4b9d3bd5f88d39503d44facd4029913793c32e01a43c3ff5dc9b`. SPEC cung cấp ở sandbox, không nằm trong checkout mã. Hai patch khớp byte Git diff thật; diff-check rc 0. Đúng bốn tệp write set. YAML parse: chỉ gate-cong-cu/gate-cong-cu-gop đổi, job khác và top-level khác bằng nhau. [Định danh](evidence/invariants.json), [YAML](evidence/yaml-scope.json).

`python3 evidence/radius.py static`: **61 tên/thứ tự CA giữ nguyên; 470/470 định nghĩa mutant cũ giữ nguyên**, gồm binding/phụ thuộc/đích và thứ tự tương đối; từng anchor cũ giữ cùng số lần, thay đổi **0**. Head **487 = 470 + 17**. [Dữ liệu](evidence/n3.json).

Lệnh mẫu cặp: `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/radius.py sample`. Chọn từ 403 mutant cũ có đích khác t52, `random.Random(892003).sample(..., 40)`; danh sách và seed được ghi trước khi đo. Dùng `_ban_kinh_moi_dot_bien` thật, đủ CA, không bỏ ca nền, hai vế trong một invocation.

Output: base **40 mục, 0 lỗi**; head **40 mục, 0 lỗi**; delta phân hạng **0**. Mẫu ngẫu nhiên phủ **40/470 = 8,51%**; cộng mutant cũ đo đích riêng phủ **43/470** tên khác nhau. **Không khai đã chạy toàn bộ 470.** [Danh sách](evidence/sample-names.json), [base](evidence/sample-base.json), [head](evidence/sample-head.json), [delta](evidence/sample-delta.json), [log](evidence/sample.log).

Ngoài 43 tên có raw phân hạng riêng, lệnh cổng chuẩn còn tự kiểm ba tên thật `t1_rc_gop`, `bn_khong_tran_tep`, `bn_khong_git_bo_kiem_oid` đủ CA theo cả đường tuần tự và song song; N126 ĐẠT ở cả hai vế. Tính cả chúng là **46/470** tên cũ được đo bán kính; mẫu ngẫu nhiên vẫn chỉ 40/470. [Phân rã phủ](evidence/coverage.json).

Ba mutant hồi quy lượt 2 được chạy nguyên script `python3 evidence-luot2/probe-old-regression.py`, dùng `_ban_kinh_moi_dot_bien` trên cả hai vế:

| Mutant | Base (dòng kết luận, lỗi) | Head (dòng kết luận, lỗi) |
|---|---|---|
| `f9_sha_hang` | [["  ok  f9_sha_hang → giết đúng 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON' · bán kính 1/61"], 0] | [["  ok  f9_sha_hang → giết đúng 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON' · bán kính 1/61"], 0] |
| `f9_head_hang` | [["  ok  f9_head_hang → giết đúng 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON' · bán kính 1/61"], 0] | [["  ok  f9_head_hang → giết đúng 't53_che_do_doc_FAIL_CLOSED_moi_cau_hinh_la_co_THE_RIENG_va_van_tay_bam_NGUON' · bán kính 1/61"], 0] |
| `bn_ban_kinh_giau_ly_do` | [["  ok  bn_ban_kinh_giau_ly_do → giết đúng 't29_ban_kinh_qua_RONG_phai_neu_LY_DO_tung_ca_oan' · bán kính 1/61"], 0] | [["  ok  bn_ban_kinh_giau_ly_do → giết đúng 't29_ban_kinh_qua_RONG_phai_neu_LY_DO_tung_ca_oan' · bán kính 1/61"], 0] |

## 17 MUTANT ĐĂNG KÝ — BÁN KÍNH VÀ LÝ DO

Lệnh: `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false python3 evidence/radius.py new`. Mỗi mục qua **`_ban_kinh_moi_dot_bien([name], (), 1)`**, không sửa CA, builder hay classifier. Wrapper chỉ lưu raw cases khi classifier thật chạy. Không thay bộ ca bằng t52 để tính bán kính. [Raw](evidence/radius-new.json), [audit](evidence/radius-audit.json), [log](evidence/radius-new.log).

| Mutant | Đo thật | Kết luận | Assertion/fixture gây chết |
|---|---|---|---|
| `wp892_bo_nhanh` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_rong, dn_khong_co` |
| `wp892_strip` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_cach, dn_cr` |
| `wp892_lower` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_hoa` |
| `wp892_tien_to` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_cach, dn_tien_to, dn_cr` |
| `wp892_vang_la_nhanh` | 61/61 ca; lỗi 0 | t52, 1/61 | `cli_tt_rong, cli_tt_ten_cua` |
| `wp892_bo_dk_rong` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_dung, dn_thieu` |
| `wp892_nhan_tep` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_tep` |
| `wp892_rc_do` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_rong, dn_khong_co` |
| `wp892_hau_to` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_dau` |
| `wp892_bo_cr` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_cr` |
| `wp892_lo_tep_an` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_tep_an` |
| `wp892_dispatcher_nhanh_rc1` | 61/61 ca; lỗi 0 | t52, 1/61 | `cli_dn_rong, cli_dn_khong_co, cli_dn_dung, cli_dn_thieu` |
| `wp892_dispatcher_nhanh_bo_gom` | 61/61 ca; lỗi 0 | t52, 1/61 | `cli_dn_rong, cli_dn_khong_co, cli_dn_tep_an, cli_dn_con, cli_dn_dung, cli_dn_thieu` |
| `wp892_dispatcher_rong_xanh` | 61/61 ca; lỗi 0 | t52, 1/61 | `cli_dn_trong` |
| `wp892_bo_qua_thu_muc_con` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_con` |
| `wp892_ro_env_ngoai` | 61/61 ca; lỗi 0 | t52, 1/61 | `cli_tt_rong, cli_tt_ten_cua` |
| `wp892_dong_gia_giet` | 61/61 ca; lỗi 0 | t52, 1/61 | `dn_rong, dn_khong_co` |

Giết đúng nghĩa là chỉ t52 `giet_that`, 60 ca khác `qua`, không skip/tin_dung_gia. Lý do nguyên văn nằm trong audit/raw. Với mutant dispatcher, lý do có thể trích G-head ở **vế đối chứng**; assertion chết vì rc/stdout sai của mutant, không phải vì substring G-head bị cấm. Script `registered-reasons.py` nguyên văn lượt 2 cũng đã chạy lại trên head cho đối chứng HEAD-ready, nhưng phép bán kính chuẩn và lý do trong bảng lấy từ đủ 61 CA ở giàn chuẩn, tránh suy rộng từ diagnostic chỉ một ca.

## SĂN ĐỘC LẬP MỚI

Các neo/thay đầy đủ, 61 trạng thái và witness rc/argv/env/stdout ở [new-hunts-final](evidence/new-hunts-final.json); lệnh `python3 evidence/new-hunts.py` đo cả năm mục. Bốn mục đầu được khởi chạy trước khi thêm mutant rc1 đơn giản; mục rc1 đo riêng bằng --only. Không chọn mẫu sau khi biết kết quả.

| Hướng / giả thuyết | Lệnh / output thật | Kết luận |
|---|---|---|
| Cặp CLI cùng lỗi có giấu việc nhanh không gom thành công? | `new-hunts.py --only rv_cli_fast_valid_rc1`: SỐNG 61/61; head rc 0/0, mutant 0/1, stdout GOM MẢNH 3/3. `rv_cli_fast_head_none` cũng sống. | **LỖI P2**, cùng lớp CLI. |
| Env đầu vào bị cố định có giấu cửa selfcheck hỏng riêng env vắng? | `rv_selfcheck_absent_rc1`: SỐNG 61/61; witness vắng 0→1, nhanh 0→0; `absent-entry-contrast.py` cho thấy t52 lượt 2 từ chối đúng lỗi giàn entry này. | **LỖI P3** phủ input nội bộ, không quy lỗi runtime --gop. |
| CLI shortcut có kiểm cấm lời “giết” và mode? | `rv_cli_fast_claim_kills`: SỐNG 61/61, rc 0 KHÔNG ĐO — bị giết 0 đột biến, thiếu mode. | **LỖI P2**, cùng lớp CLI. |
| Đổi chữ shortcut để né neo âm mới nhưng giữ rc 0 có lọt? | `rv_bypass_changed_text`: giết đúng t52 **1/61**, lỗi 0; cli_dn_dung/cli_dn_thieu rc 0 bị chặn dù không còn `=duong_nhanh, 0 mảnh`. | **KHÔNG PHẢI LỖI** riêng neo âm: rc bắt độc lập. |
| Head có bỏ chốt khi nhanh+CÓ artifact? | `probe-integrity.py` nguyên văn: đủ 8 mảnh rc 0/0, 490 dòng; thiếu rc 1/1 G-tap; đích sống rc 1/1; stale HEAD rc 1/1 G-van-tay; hidden thêm rc 1/1 G-dau; mọi cặp stdout/stderr giống hệt. | **KHÔNG PHẢI LỖI** runtime ở các fixture consumer. Không gọi đó là 487 mutation chạy thật. |

**Hiệu chỉnh fixture reviewer:** witness lượt đầu trong `new-hunts.log` lẫn tên review tự tiêm vào artifact và bị G-ban-ghi. Đã loại witness đó, bỏ tên review khỏi tập artifact và đo lại **chỉ witness** (`--witness-only`), giữ nguyên radius đã đo. Các JSON cá nhân/new-hunts-final chứa bản sửa đúng; không lấy witness cũ ở aggregate new-hunts.json làm bằng chứng. [Log sửa HEAD](evidence/witness-head-none-corrected.log), [sửa text](evidence/witness-text-corrected.log).

## N4 VÀ GIỚI HẠN

**N4 GitHub thật: KHÔNG ĐO ĐƯỢC offline.** Chưa có jobs API/log trên reviewed_sha để đo 8 shard day_du chạy và gom xanh, hoặc PR hồ sơ với shard skipped/gom xanh/KHÔNG ĐO/phút runner; chưa so từng conclusion PR head/master thật. Không dùng lời khai CI của executor hoặc CI d3fba0c cho head này. Scheduler Actions, output thiếu→env rỗng và side effect download-artifact không được fixture Python xác thực.

Toàn bộ thử nghiệm trên archive/scratch ngoài checkout. Không mạng, không đăng GitHub, không sửa branch executor, không merge/land/deploy. Status có untracked/ignored, diff/index, HEAD/tree và byte bốn tệp reviewed được kiểm lại sau cùng ở [readonly-after](evidence/readonly-after.json); hai mốc không chứng minh mọi thao tác trung gian. Không tự cấp cross_approved/CI success cho các phần không đo được.
