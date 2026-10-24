verdict: changes_requested
reviewed_sha: d3fba0c8e5411002540078312a9ccd979a984b84
reviewed_tree: 5fda44be7adff3b20a6885379260d2980de6d763
base_sha: 8324567788caab8dc332d45df458ef415fd305be

Có **3 P2 và 1 P3** đang mở. Ba phản chứng miền đầu vào của lượt 1 và mutant dispatcher nguyên văn đã được vá, y04 đã có hai răng độc lập. Tuy nhiên ca CLI mới cấp tín dụng giả khi cây mutant thiếu HEAD, làm rộng bán kính mutant cũ; bảng CLI còn thiếu các ô N1; env ngoài làm đổi hai ca cũ. Không approve mã. N4 GitHub thật tách riêng, **KHÔNG ĐO ĐƯỢC** offline, không dùng làm lý do cho các finding mã dưới đây.

Reviewer độc lập: Codex / OpenAI, họ GPT-6 theo cấu hình phiên; thực thi qua công cụ `exec_command` trong sandbox quản lý, transport machine/local. Không có attestation model/effort từng request hoặc xác nhận riêng đường launcher; không suy identity từ actor GitHub. Lớp `sensitive`. Python 3.13.16, PyYAML 6.0.3; CI ghim Python 3.12, không đồng nhất hai môi trường.

Đã đọc **đủ** prompt snapshot, SPEC r2, VERDICT lượt 1 (205 dòng, đúng ba finding), diff sửa và source action được cung cấp. Không dùng kết luận của lượt 2 bị cắt làm kết quả: các script dùng lại đều đã chạy mới và có log mới ở [evidence](evidence/). `VERDICT.md` được tạo `pending` ngay đầu và cập nhật tăng dần; bản lịch sử trước tổng hợp ở [working-verdict.txt](evidence/working-verdict.txt).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `VERDICT-luot1.md`, SHA `70172ec590dc1eefd414d8aa951a8cb4fc82a86c`. Các lệnh Python dùng env chung ở phần tái lập bên dưới; `$R` là archive head mới.

| Finding / tình trạng | Phép đo nguyên văn lượt 1 | Output thật / phạm vi đóng |
|---|---|---|
| P2 `y04-dot-bien-khong-khoa-du-hai-ngoai-le`: **ĐÃ VÁ THẬT — đã đóng** | `python3 evidence-luot1/probe-y04-tooth.py "$Y" evidence/y04-tooth.json` trên archive riêng | 8 mutant đích y04; `invalid_yaml_in_declared_table []`. Gỡ with: 7/8, **chỉ** `y04_with_che_do_buoc_tai_ve` sống. Nới env mọi bước mảnh: 7/8, **chỉ** `y04_env_vao_buoc_khac` sống. Hai witness được meta-mutation chấp nhận, head từ chối. [Log](evidence/y04-tooth.log), [JSON](evidence/y04-tooth.json). |
| P2 `gom-duong-nhanh-chua-khoa-dispatcher-cli`: **biểu hiện gốc đã đóng; VÁ SINH LỖI MỚI, lớp chưa đóng** | `python3 evidence-luot1/probe-dispatch.py "$R" evidence/dispatch.json` | `rv_dispatch_fast_rc1` giết đúng t52, **1/61**, 61 ca đo được. Lý do đúng là `cli_dn_rong`/`cli_dn_khong_co` rc 1 rỗng; witness head rc 0 KHÔNG ĐO / mutant rc 1. Nhưng hai mutant CLI mới sống khi gỡ lỗi giàn giáo; xem finding cùng slug. [JSON](evidence/dispatch.json). |
| P3 `gom-thieu-doi-chung-ngoai-gia-tri-va-thu-muc`: **ba biểu hiện cũ ĐÃ VÁ THẬT; lớp còn mở P3** | `python3 evidence-luot1/custom-radius.py "$R" evidence/radius-custom.json` + `python3 evidence-luot1/witness-mutants.py "$R" evidence/witness.json` | `rv_endswith`, `rv_ignore_hidden`, `rv_strip_CR` đều giết đúng t52, **1/61**, không skip. Lý do lần lượt `dn_dau`, `dn_tep_an`, `dn_cr`, không phải G-head. Witness mỗi cái head rc 1 → mutant rc 0 KHÔNG ĐO. `rv_contains` cũng chết đúng 1/61. Biểu hiện mới thư mục con ở finding P3 dưới. [Radius](evidence/radius-custom.json), [witness](evidence/witness.json). |

Giữ slug lớp cũ; không đổi tên để xóa lịch sử. Có **4 lớp mở**: lớp CLI cũ (2 biểu hiện mới), lớp biên đầu vào cũ (1 biểu hiện mới), và 2 lớp mới là tín dụng giả/Git HEAD và kế thừa env. Hai răng y04 đã đóng độc lập.

## BẢNG ĐO VÀ TÁI LẬP

Bản sao tạo bằng `mktemp -d` + `git -C cay-kho archive <OID> | tar -xf -`; Git init/fetch **từ mirror cục bộ**, reset mixed tới OID, `core.abbrev=7`, autocrlf false/EOL LF. Không mạng; không sửa `cay-kho/`, không đăng GitHub. `$T=$(cat evidence/tmp-root)`, `$R=$T/head`; `$Y=/tmp/wp892-r2-review.VdXw4s/y04`. Tất cả Python đo có `PYTHONDONTWRITEBYTECODE=1`; signing của máy được tắt **cho tiến trình** bằng:

```sh
GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false
```

Lệnh chính thức chạy **cả base/head trong một lần gọi**, mỗi cặp dùng cùng command/env:

```sh
PYTHONDONTWRITEBYTECODE=1 python3 evidence/reproduce-final.py
```

Driver ghi command, rc, thời lượng, stdout/stderr từng vế vào [reproduction-final](evidence/reproduction-final/). Lượt đầu `evidence/reproduce.py` khởi động quá sớm khi archive head chưa hoàn tất; Ruff head chỉ thấy phần cây. Đã loại kết quả head lượt ấy và đo lại trên cây hoàn chỉnh. Không dùng các log cấp trên `evidence/ci-*`, `registry-*`, `ruff-*` để thay kết quả chính thức dưới đây.

| Phép đo | Command từng vế | Output / kết luận |
|---|---|---|
| Exact head/tree/spec/write set | `rev-parse`, `sha256sum SPEC.md`, `git diff --name-only`, `diff --check` | SHA/tree như header; spec `aeac5b18566f4b9d3bd5f88d39503d44facd4029913793c32e01a43c3ff5dc9b`; đúng 4 tệp spec, diff-check rc 0. YAML parse chỉ đổi `gate-cong-cu` và `gate-cong-cu-gop`, top-level khác bằng nhau. [YAML](evidence/yaml-scope.json). Cả hai patch được cấp khớp byte Git diff thật ([hash](evidence/patch-integrity.json)). Lease snapshot có base lúc cấp khác; base so sánh của review lấy đúng prompt hiện hành, không tự sửa lease. |
| Classifier base/head | `python3 ops/ci_duong_nhanh_test.py` | Base rc 1: **CA 103/104 dat · 0 do · 1 hong · DOT BIEN 377/384 bi giet dung ly do**; head rc 1: **CA 103/104 dat · 0 do · 1 hong · DOT BIEN 385/392 bi giet dung ly do**. Cùng t20zo lỗi `socket.bind`: PermissionError Errno 1. Cùng 5 mutant không có tiền đề socket xanh và 2 mutant timeout 120 giây (`ca_du_lieu_bo_t27`, `ca_du_lieu_bo_qua_rc`); không gọi 7 mục đó là survivor; tên/lý do trong [base](evidence/reproduction-final/ci-base.log), [head](evidence/reproduction-final/ci-head.log). Không khai 104/104 hay toàn bộ 392/392 xanh trong sandbox. Retry riêng hai timeout bằng cùng consumer và ngưỡng 120 giây: **2/2 GIET trên mỗi vế** (9–19 giây/mục); không đổi tỷ lệ raw của lượt suite đầy đủ. [Script](evidence/retry-classifier-timeouts.py), [base](evidence/ci-timeouts-base.log), [head](evidence/ci-timeouts-head.log). Tám mutant classifier thêm mới đều bị giết; 7 mục bất thường của lượt đầy đủ trùng nhau giữa base/head. |
| Cong-cu nền head | `python3 evidence-luot1/radius.py "$R" evidence/baseline.json baseline` | **61/61 qua, 0 skip**, không ca đỏ/hỏng. [JSON](evidence/baseline.json). |
| Registry | `python3 .claude/dev/ci_dang_ky_test.py` | Cặp chính thức: **1063/1064 → 1070/1070**, rc **1/0**. Base đỏ ở `p637-A3c-chau-setsid-thoat-nhom-van-bi-bat: LỌT`; cặp retry cùng kết quả. Đoạn xử lý process này nằm ngoài diff, chưa đo nguyên nhân nền; không quy là lỗi mới của packet. Log base lần chuẩn bị đầu từng 1064/1064 (cây base đã hoàn tất), không dùng nó thay lượt cặp thất bại. [Retry hai vế](evidence/registry-retry/results.json). |
| Lease t16 | `python3 ops/lease_publish_test.py --chi-ca=t16` | **9/9** mỗi vế, rc 0/0, đã chạy=9, bỏ qua=0. Gồm chốt t16x nguồn os. |
| Actionlint | `actionlint .github/workflows/ci.yml` | 1.7.7, rc 0/0, stdout/stderr rỗng. Phạm vi YAML đổi; không chứng minh scheduler/runner. |
| Bare Ruff | `ruff check --no-cache --select F --output-format json .` | 0.16.9; **rc 1/1, 8807/8807** finding nền. Counter theo relative path + rule + message: thêm=[], bớt=[], **delta 0**. Không khai lint xanh. [Delta](evidence/ruff-final-delta.json). |
| Doctrine | `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc 0/0; quét 10 tệp, 0 chỗ chép doctrine. |
| Read-only | status gồm ignored/untracked, HEAD/tree, diff/index, hash byte | Status gồm ignored/untracked rỗng; diff/index rỗng; HEAD/tree không đổi; 4 tệp đổi khớp byte blob reviewed_sha. [Mốc trước](evidence/checkout-before.json), [mốc sau](evidence/checkout-after.json). Sandbox thực tế workspace-write; ranh giới reviewer được giữ bằng thao tác trên bản sao. Hai mốc không chứng minh toàn bộ lịch sử giữa chúng. |

N3 tĩnh: **61 CA** giữ nguyên tên/thứ tự; **470/470 DOT_BIEN cũ** giữ nguyên toàn bộ định nghĩa, binding/phụ thuộc/đích, thứ tự tương đối; từng mỏ neo cũ giữ nguyên số lần, **0** thay đổi. Head **483 = 470 + 13**. [Meta base](evidence/meta-base.json), [meta head](evidence/meta-head.json), [so sánh](evidence/n3.json). **N3 bán kính có hồi quy** như finding tín dụng giả; không dùng kết quả tĩnh này để tuyên bố Linux đầy đủ không đổi. Không khai đã chạy toàn bộ 470 mutant cũ.

Năm mục không có tiền đề socket: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Hai timeout cũ đã đo lại riêng và đều GIET; không suy nguyên nhân timeout từ việc retry qua.

## BẢNG ĐỘT BIẾN — 13 MỤC ĐĂNG KÝ

Lệnh thật: `REVIEW_WORKERS=4 python3 evidence-luot1/radius.py "$R" evidence/radius-new.json new`. Driver gọi **`_ban_kinh_moi_dot_bien`**, đo đủ danh sách 61 ca; không giả bộ phân hạng. [Log](evidence/radius-new.log), [JSON](evidence/radius-new.json).

| Mutant | Kết luận cơ chế thật |
|---|---|
| `wp892_bo_nhanh` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_strip` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_lower` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_tien_to` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_vang_la_nhanh` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_bo_dk_rong` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_nhan_tep` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_rc_do` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_hau_to` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_bo_cr` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_lo_tep_an` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_dispatcher_nhanh_rc1` | giết đúng t52; bán kính **1/61**; lỗi 0 |
| `wp892_dong_gia_giet` | giết đúng t52; bán kính **1/61**; lỗi 0 |

**TOTAL 13, errors 0.** Mẫu số 61 là danh sách CA; JSON driver giữ kết luận tổng hợp, không dùng mẫu số tự chứng minh mọi ca đều qua ở từng mutant. Nền riêng đã đo đủ 61/61.

Do phát hiện G-head cấp tín dụng giả, đã đo thêm **chỉ ca t52** cho cả 13 trên cây mutant có Git HEAD, không sửa assertion hay điều kiện mode: `python3 evidence/registered-reasons.py "$R" evidence/registered-reasons.json`. **13/13 `giet_that`, 0 lý do G-head**; mỗi cái thất bại ở đối chứng thuộc tính của nó, kể cả hai ô CLI rc 0 dương bị dispatcher rc1 làm hỏng. Đây là đối chứng nguyên nhân, **không** gọi nó là lần đo lại bán kính 61 ca. [Định nghĩa và lý do](evidence/registered-reasons.json).

## BA MUTANT MỚI KHÁC BẢNG ĐĂNG KÝ

Lệnh: `python3 evidence/custom-new.py "$R" evidence/custom-new.json`, rồi cùng script với tham số `head_ready` → `evidence/custom-head-ready.json`. Cả hai dùng `_do_ban_kinh` + `_ket_luan_ban_kinh`, đủ 61 ca. Chế độ thứ hai chỉ Git init/add/commit trong cây mutant **tạm**, không đổi code gom hay ca; dùng để tách nguyên nhân, không thay kết quả giàn chuẩn.

| Mutant / thay đổi | Giàn chuẩn | Đối chứng có HEAD và witness CLI | Kết luận |
|---|---|---|---|
| `rv_cli_fast_shards_skip`: dispatcher rc 0 khi mode nhanh và có `manh-*.txt` | Báo giết đúng t52 1/61, nhưng lý do là hidden fixture G-head | **Sống: 61 qua, 0 giết/skip**, bộ báo errors=1. Witness head rc 1 → mutant rc 0, stdout mutant rỗng. | Lỗ N1/cửa CLI: không khóa `duong_nhanh` + có mảnh qua subprocess. |
| `rv_cli_empty_success`: dispatcher rc 0 khi env bằng chuỗi rỗng | Cùng tín dụng giả G-head | **Sống: 61 qua, 0 giết/skip**, bộ báo errors=1. Witness head rc 1 → mutant rc 0, stdout mutant rỗng. | Lỗ N1/cửa CLI: thiếu ô env rỗng qua subprocess. |
| `rv_ignore_subdirs`: điều kiện rỗng bỏ qua thư mục con, chỉ nhìn `is_file()` | Cùng tín dụng giả G-head | **Sống: 61 qua, 0 giết/skip**, bộ báo errors=1. Witness head rc 1 → mutant rc 0 KHÔNG ĐO. | Nợ kiểm thử P3 cùng lớp biên đầu vào; head hiện từ chối đúng. |

Toàn bộ chuỗi neo/thay, 61 trạng thái và stdout/stderr witness ở [giàn chuẩn](evidence/custom-new.json), [có HEAD](evidence/custom-head-ready.json). Không gọi ba kết quả danh nghĩa 1/61 ban đầu là răng. Các survivor được chứng minh bằng witness khác hành vi; mutation tương đương dưới đây làm đối chứng âm cho giàn.

## FINDINGS

### [P2] `gom-cli-tep-an-cap-tin-dung-gia` — CLI hidden fixture làm rộng bán kính mutant cũ

**Tệp/dòng:** `ops/cong_cu_test.py:7289` (substring assertion), `:8453` (CLI fixture trên cây mutant không Git).

Cây `_dung_cay_dot_bien` chỉ có script và các tệp kèm, không có `.git`. `cli_dn_tep_an` là thư mục không rỗng nên `_main_gop` gọi `_van_tay`; `_gom_manh` trả `[G-head] ... KHÔNG ĐO ĐƯỢC`. Assertion cấm substring `KHÔNG ĐO` coi lỗi setup này là `TinHieuChotCa` của t52. Bất kỳ mutant TEP_TEST không tác động gom cũng có thể nhận tín dụng giả; mutant cũ đích khác nhận thêm t52, khiến gate bán kính đỏ. Đây là hồi quy do commit sửa, không phải socket/signing của sandbox.

**Đo:** `python3 evidence/probe-false-credit.py "$R" evidence/false-credit.json`. Mutation tương đương duy nhất là đổi thứ tự hai vế `==`. Giàn chuẩn báo `ok … giết đúng t52 · 1/61`; lý do duy nhất là `cli_dn_tep_an`/G-head. Cấp HEAD cho đúng cây tạm ấy → **61 qua, 0 giết/skip**; mutation tương đương sống đúng như phải sống. [JSON](evidence/false-credit.json).

Lệnh cặp `python3 evidence/probe-old-regression.py`, qua **`_ban_kinh_moi_dot_bien`** thật:

| Mutant cũ / đối chứng | Base | Head |
|---|---|---|
| `f9_sha_hang` | 1/61, lỗi 0 | 2/61, thêm t52 vì G-head; lỗi 1 |
| `f9_head_hang` | 1/61, lỗi 0 | 1/61, không đổi; lỗi 0 |
| `bn_ban_kinh_giau_ly_do` | 1/61, lỗi 0 | 2/61, thêm t52 vì G-head; lỗi 1 |

Hai ca hồi quy là bằng chứng bán kính cũ đã đổi; `f9_head_hang` tự cung cấp HEAD hằng khác None nên không kích hoạt lỗi thiếu HEAD. [Kết quả hai vế](evidence/old-regression.json). Không suy rằng đã đo toàn bộ 470 mutant.

**Cách vá:** sửa giàn CLI và assertion trong `_in_tu_kiem_gom`/t52. Phân biệt dòng nhánh nhanh `GOM: KHÔNG ĐO` với lỗi `KHÔNG ĐO ĐƯỢC`; bảo đảm fixture có mảnh đo được trong ngữ cảnh Git phù hợp, tái dùng cách dựng của F17 và tránh buộc t52 vào nguồn vân tay thuộc t53. Không chữa bằng cách nới để mọi lỗi setup được xem là đo thành công. **Ca khóa:** mutation tương đương phải sống; ba mutant cũ giữ 1/61; hidden bypass vẫn chết vì rc 0 sai. **Rủi ro vá:** chỉ thêm `.git` có thể lại làm t52 chết khi mutant đích t53 cố tình sửa `_van_tay`; phải đo cả target/non-target và điều kiện giàn giáo. Độ tin cao.

### [P2] `gom-duong-nhanh-chua-khoa-dispatcher-cli` — còn thiếu ô CLI bắt buộc của N1

**Tệp/dòng:** `ops/cong_cu_test.py:8453` và `:8477`.

Bảng `cli_dn_*` mới chỉ có nhanh+rỗng/vắng, day_du/vắng+rỗng, hidden. `dn_dung`/`dn_thieu` vẫn gọi `_main_gop` trực tiếp. `cli_git_*` không đặt env nhanh, nên không thay được ô subprocess nhanh+có mảnh. Bảng cũng không có env **chuỗi rỗng**, lệch hoa/thường và khoảng trắng ở cửa subprocess như N1 yêu cầu.

**Đo:** hai mutant `rv_cli_fast_shards_skip`, `rv_cli_empty_success` trong bảng trên đều sống đủ 61 ca khi sửa riêng điều kiện giàn giáo có HEAD; witness literal `TEP_TEST --gop` đổi rc 1 của head thành rc 0 của mutant. Giàn nguyên bản chỉ báo giết nhờ finding G-head. Mutant dispatcher nguyên văn lượt 1 đã chết đúng, nhưng không đủ đóng toàn lớp.

**Cách vá:** thêm bảng mode × trạng thái thư mục N1 qua subprocess của **TEP_TEST đang mutate**, gồm mảnh hợp lệ/thiếu với mode nhanh và tất cả giá trị âm; dựng vân tay từ đúng cây CLI. **Ca khóa:** đăng ký hai mutant dispatcher mới, mỗi cái chết đúng t52, bán kính 1/61 sau khi loại tín dụng giả; gom thật phải có output/kết luận giống đường thường. **Rủi ro vá:** fixture dùng hash/HEAD của bản chưa mutate có thể bị G-van-tay trước khi đo hành vi, tái tạo chính lỗi tín dụng giả. Độ tin cao.

### [P2] `gom-ca-cu-ke-thua-env-duong-nhanh` — môi trường ngoài đổi kết quả các ca cũ

**Tệp/dòng:** `ops/cong_cu_test.py:8446` (F13 kế thừa env), `:8416` (chỉ dọn env sau các ca trực tiếp cũ).

`finally` hoàn nguyên biến cha đúng, nhưng F13 kế thừa lại giá trị ngoài đã hoàn nguyên. Với env ngoài `duong_nhanh`, `cli_tt_rong` và `cli_tt_ten_cua` chạy nhánh nhanh, rc 0 KHÔNG ĐO thay vì lỗi rc 1. t52 nền đổi từ qua thành đỏ. Không phải quên phục hồi biến; đây là ca không cô lập đầu vào môi trường.

**Đo:** `python3 evidence/probe-env.py "$R" evidence/env-corrected.json`: vắng/day_du/outer-sentinel/chuỗi rỗng → t52 `qua`; `duong_nhanh` → `giet_that`, đúng hai ô trên. Env cha trước/sau bằng nhau cả 5 lần. [JSON](evidence/env-corrected.json). `probe-order.py` đảo hai bảng fixture vẫn tái hiện hai ô sai; không phụ thuộc thứ tự. [JSON](evidence/order.json).

**Cách vá:** chuẩn hóa môi trường **từng fixture**, xóa biến mode cho các ca thường kể cả F13/F17 và đường trực tiếp; chỉ ca nhanh được truyền giá trị qua `env` của tiến trình con. Giữ try/finally nếu cần gán môi trường trong tiến trình. **Ca khóa:** chạy cùng ca/bộ với biến ngoài vắng, duong_nhanh, rỗng, giá trị lạ; output nghiệp vụ như nhau, env cha không đổi. **Rủi ro vá:** xóa biến chung quá rộng có thể làm các ô `dn_*` không còn thực sự đo env; cần cả đối chứng dương nhanh+rỗng lẫn âm thường+rỗng. Độ tin cao.

### [P3] `gom-thieu-doi-chung-ngoai-gia-tri-va-thu-muc` — thư mục con bị xem như không có đầu vào chưa bị khóa

**Tệp/dòng:** `ops/cong_cu_test.py:8422` (bảng fixture miền thư mục).

Ba biểu hiện cũ đã sửa thật. Biểu hiện mới cùng lớp: thư mục chỉ có một thư mục con rỗng. Head trả rc 1 `[G-tep]`; mutant `rv_ignore_subdirs` bỏ qua entry không phải tệp và rc 0 KHÔNG ĐO. Sau khi tách lỗi G-head, mutant sống qua 61 ca. Đây là thiếu đối chứng của ca khóa; chưa tìm thấy head sản phẩm xử lý sai trường hợp ấy. [Hai lần radius và witness](evidence/custom-head-ready.json).

**Cách vá:** thêm fixture child-only vào bảng trực tiếp và CLI với env nhanh; đòi đi vào gom thường, rc 1 đúng chốt. **Ca khóa:** mutation bỏ qua subdirectory phải chết đúng t52, không nhờ G-head. **Rủi ro vá:** nhầm hợp đồng thư mục rỗng với “không có tệp mảnh hợp lệ” có thể vô tình nới để bỏ qua artifact lạ; giữ fail closed cho mọi entry. Độ tin cao, không phải lý do chính của changes_requested.

## BẢNG SĂN ĐỘC LẬP MỚI

| Hướng / giả thuyết | Lệnh đã chạy | Output thật | Kết luận |
|---|---|---|---|
| Tín dụng mutation phụ thuộc Git HEAD của cây tạm, kể cả mutation tương đương | `python3 evidence/probe-false-credit.py "$R" evidence/false-credit.json` + `python3 evidence/probe-old-regression.py` | Tương đương bị giết t52 ở giàn chuẩn, sống 61/61 khi có HEAD; mutant cũ mở rộng bán kính | **LỖI P2**. |
| Env đặt ngoài có thể đổi các ca thường dù cha được phục hồi | `python3 evidence/probe-env.py "$R" evidence/env-corrected.json` | Chỉ giá trị ngoài duong_nhanh làm hai ca CLI cũ rc 0; t52 đỏ; 5/5 lần cha không đổi | **LỖI P2**. |
| Dispatcher chỉ bỏ gom khi có artifact hoặc nhận env rỗng có thoát được bảng mới | `python3 evidence/custom-new.py "$R" evidence/custom-head-ready.json head_ready` | Hai mutant CLI sống đủ 61 ca, witness head 1 → mutant 0 | **LỖI P2** của ca khóa N1, không suy runtime head đã có bypass. |
| Shared hidden fixture bị tiêu thụ hoặc đổi nội dung theo thứ tự | `python3 evidence/probe-fixture-order.py "$R" evidence/fixture-order.json`; `python3 evidence/probe-order.py cay-kho evidence/order.json` | Direct→CLI, CLI→direct đều rc 1 G-dau, .gitkeep tồn tại/hash không đổi; đảo cả hai bảng cũng vậy | **KHÔNG PHẢI LỖI** về thứ tự. |
| Nhánh nhanh có thể bỏ chốt nội dung/vân tay khi có artifact | `python3 evidence/probe-integrity.py "$R" evidence/integrity.json` | Đủ 8: 0/0, 486 dòng; thiếu: 1/1 G-tap; đích sống: 1/1; stale HEAD: 1/1 G-van-tay; hidden thêm: 1/1 G-dau. Mode vắng/nhanh có rc/stdout/stderr giống hệt từng fixture | **KHÔNG PHẢI LỖI** ở head. Fixture consumer, không phải 483 mutation chạy thật. |
| Thư mục không có regular file nhưng có child có bị bỏ gom | Cùng `custom-new.py`, mutant rv_ignore_subdirs | Head 1 G-tep, mutant 0; đối chứng có HEAD 61 qua | **LỖI P3** của ca khóa. |

## ACTIONS (b)/(d) VÀ N4 — MỨC CHỨNG CỨ

Đọc đủ [download-artifact-v4.ts](download-artifact-v4.ts), SHA256 `1c67eb1bb4f77a462522341189f433422c4d35a6999d0dea2a1846e6edfedd80`, 207 dòng. Nhánh pattern (136–150) gọi listArtifacts rồi dùng `new Minimatch(inputs.pattern)` và filter; **không có zero-match throw** ở nhánh này. Throw thiếu named artifact (81) và không có IDs khớp (122) thuộc nhánh khác. `downloadArtifact` chỉ ở `artifacts.map` (172–182), nên mảng rỗng không tải gì; vòng await rỗng và cuối hàm in `Total of 0 artifact(s) downloaded`, set output và báo xong (200–202). Không có mkdir trong tệp; đường mã zero-download không yêu cầu tạo `manh`.

**Xác nhận lời khai (b)/(d) ở mức source được cung cấp.** Đây là mã nguồn gắn nhãn nhánh/tag trôi `v4`, không xác thực lại remote ref, không có immutable action SHA hoặc run receipt. Không chạy action/dependency thật; không lấy thiếu mkdir trong tệp làm phép đo toàn bộ side effect của dependency. [Kiểm nguồn](evidence/actions-source.json).

**N4 PR hồ sơ: KHÔNG ĐO ĐƯỢC.** Chưa có jobs API/log từ lượt thật để đo shard skipped, required gom success, dòng KHÔNG ĐO và phút runner. Actions (a) scheduler với needs skipped và (c) biểu thức output thiếu→env rỗng cũng **KHÔNG ĐO ĐƯỢC** offline. Parser/YAML hay fixture Python không thay thế chúng.

Lời khai executor: PR mã `day_du` trên **70172ec** đã xanh **24/24** (8 mảnh + gom). Không kiểm được offline, và SHA ấy khác reviewed_sha. Không dùng lời khai đó để cấp tín dụng CI cho head mới. N4 và so conclusion PR/master thật vẫn mở riêng; không có thao tác merge/land/deploy hoặc đăng GitHub trong lượt này.
