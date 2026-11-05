verdict: request_changes
reviewed_sha: c0c0f4d636894544ecda515fcc1db3b1e2fad237
reviewed_tree: b03bf8458dff4b951d182b56ac1f7404c7f406d9

## DANH TÍNH

Đo đầu lượt (2026-11-04 UTC); mọi lệnh dưới đây exit 0:

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
c0c0f4d636894544ecda515fcc1db3b1e2fad237
b03bf8458dff4b951d182b56ac1f7404c7f406d9
$ git -C cay-kho status --porcelain=v1 --ignored
<rỗng>
$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3,4,5,6}.md
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  r1
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  r2
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  r3
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  r4
25473237f53684706112b5a2f8dfafce143000110a57c8d680f3b44f924e5ed5  r5
b078da106387512cac956d8bc18d702bb50cfcf4bfd37101bb6c7aeb0686d201  r6
```

R6 là bản hiệu lực. Diff base `1f0941e9` → head chỉ thêm r4/r5/r6; không có mã thi hành. Danh tính thực tế: provider `openai_codex`; họ model OpenAI/GPT-6 theo khai báo hệ thống (không đo được exact served model ID); execution surface `codex_service` (Codex qua công cụ, không gọi CLI/Desktop); transport `machine`. Không tự suy danh tính từ tài khoản GitHub. Không có context Executor. Checkout chỉ đọc; phản chứng/bản sao đặt ngoài `cay-kho/`.

Đo CUỐI lượt lúc `2026-11-04T16:29:14.632396+00:00`; hai lệnh exit 0:

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
c0c0f4d636894544ecda515fcc1db3b1e2fad237
b03bf8458dff4b951d182b56ac1f7404c7f406d9
$ git -C cay-kho status --porcelain=v1 --ignored
<rỗng>
```

HEAD, tree và trạng thái (kể cả ignored) không đổi. Không sửa, commit hay checkout trong `cay-kho/`.

## ĐO LẠI KHẲNG ĐỊNH

Các số dưới đây đo trên exact head đã neo; thời điểm đo nguồn: `2026-11-04T16:26:00.837185+00:00`. Đơn vị được ghi ở từng ô. Lệnh đầy đủ và đầu ra ở các script/log ngoài checkout:

- `python -B source_measurements.py > source-measurements.log 2>&1` — exit 0; dữ liệu `review-artifacts/source-measurements.json`.
- `python -B behavior_checks.py > behavior-checks.log 2>&1` — exit 0; dữ liệu `review-artifacts/behavior-results.json`.
- `python -B review_checks.py > review-artifacts-output.log 2>&1` — exit 0; dữ liệu `review-artifacts/results.json`. Mã thoát của bộ đo không có nghĩa tiêu chí đặc tả xanh: các giá trị màu nằm trong JSON, kể cả phản chứng xanh giả.
- `python -B cay-kho/.claude/dev/packet_loop.py doctrine-scan --root cay-kho > doctrine-scan.log 2>&1` — exit 0.

`source_measurements.py` đọc dòng/AST/manifest và chạy các lệnh Git chỉ đọc. `behavior_checks.py` chỉ chạy hàm nguồn với đồ giả trong RAM. `review_checks.py` lấy nguyên AST của `cmd_adr_song`, `_che_khong_render`, `_hang_adr_trong_bang` và các hằng phụ thuộc từ `.claude/dev/packet_loop.py`, chạy trên bản sao `docs/adr` + protocol ở `review-artifacts/adr-fixture/`; phần D1/D3/H1 dịch đúng câu chữ tiêu chí. A13 chạy hàm `_nlm_auth_alive` nguồn và thân Python `_canary_song` nguồn với `nlm_cli`/`tl` giả, thay hàm sleep bằng hàm rỗng. Không dùng module `tl` thật để gọi dịch vụ.

| Khẳng định | Lệnh đo | Kết quả | Khớp/lệch |
|---|---|---|---|
| R6 có hiệu lực; PR chỉ thêm đặc tả | `git -C cay-kho diff --stat 1f0941e9 c0c0f4d636894544ecda515fcc1db3b1e2fad237` + đọc r6:1–9 | Chỉ r4/r5/r6, 3 tệp đặc tả mới; không có mã thi hành mới | Khớp |
| Các errata r2–r5 được giữ nguyên trong r6 | `python -B source_measurements.py`, `historical_errata_unchanged` | Từng khối r2/r3/r4/r5 bằng nguyên văn bản lúc nó được giới thiệu | Khớp; các neo lịch sử cũ không bị nhầm làm yêu cầu hiệu lực |
| Mỗi mục tiêu ứng với một đường dẫn của write set; đều có nghiệm thu | cùng lệnh, `goal_mapping`, `goal_coverage` | 9 mục tiêu / 9 đường dẫn; mỗi mục tiêu có ít nhất 1 tiêu chí | Khớp L2 |
| Base là merge PR #1186; OID trần là commit land #791 | `git show -s` trong script và `git -C cay-kho log -1 --format='%H %s' 1f0941e9` | `1f0941e9bba1d1d517eda4174167b81963c06bd5` merge #1186; `8ab100793df9831505f495543a74044b91c2c9ab` merge #791 | Khớp |
| Các tệp nguồn được E3/E10 khai không đổi từ base r1 | `git -C cay-kho diff --numstat 90c101b8 1f0941e9 -- scripts/nlm_cli.py scripts/tl_gws.py scripts/tl_core/nlm_ops.py references/RASOAT_HOSO_LOOP.md references/QUY_TRINH_RA_SOAT_3_TANG.md` | Output rỗng, exit 0; diff từ `1f0941e9` tới head chỉ thêm specs | Khớp |
| `_run` là điểm chạy CLI và giữ tuple/timeout | `python -B behavior_checks.py`, `baseline_run`; AST `nlm_cli.py:110–124` | Lệnh fake nhận nguyên argv/timeout; lọc nhiễu keyring; rc 1 trả tuple, missing → rc 127, timeout → rc 124 | Khớp hành vi hiện có; cơ chế mới chưa được thi hành |
| Ba bộ chuỗi auth/`auth_hint` ở các neo hiện hành | `source_measurements.py`, dòng 143/162/229 + đọc AST `nlm_cli.py` | Cả 3 dòng là `auth = any(...)`, bộ `auth/401/login/unauthor/credential`; `_run_json`, `source_list`, `_auth_fail` trả dict như mô tả | Khớp |
| `_AUTH_FIX_FALLBACK` và selftest r213 có đúng neo mới | cùng lệnh, `line_anchors` | Khai hằng tại `nlm_ops.py:297`; def r213 tại `tl_selftest.py:24829` | Khớp E14/E10 |
| Điều cấm doctrine có đúng Markdown/neo | cùng lệnh; `nl -ba` hai tài liệu | RASOAT:118–119 là `CẤM tự` vắt dòng; QUY_TRINH:49 là `**CẤM** tự` | Khớp E8/E14 |
| `_nlm_auth_alive` và nhánh `_nlm_preflight_report` | cùng lệnh, `line_anchors`; A13 trong `review_checks.py` | Def canary 308, return cuối 363; `nlm_ops.py:1424–1429` dùng `bool(r.get("ok"))`, ngoại lệ gán `False` | Khớp; không dùng `nlm-auth-status` làm canary mới |
| Ba lần probe, 30 giây/lần, backoff tổng 4,5 giây; lần cuối quyết định | AST `tl_gws.py:308–363`; `review_checks.py`, `A13` | `range(3)`, timeout mặc định 30 s, chờ 1,5 s rồi 3 s; sáu ca cho alive `None,None,False,False,False,None` | Khớp; đây là quyết định chủ kho đã chấp nhận, không phải finding |
| `<CANARY>` cùng thân canary chuẩn, mã 0/3/2 | `nlm-auto-refresh.sh:93–105`; A13 chạy thân Python nguồn | `_imp`, `bind`, `_nlm_canary_notebook(None)`, `require_notebook_body=True`; sáu ca lỗi cho mã `2,2,3,3,3,2` | Khớp; timeout 120 s là giới hạn thiết kế, không phải số đo LIVE |
| Stage chỉ lấy payload sau canary dương | `python -B behavior_checks.py`, `stage_canary_gate`; `tl_gws.py:867–894,1978–2009`; shell:107 | True → `canary,read_fake_jar`, rc 0; False/None → chỉ `canary`, rc 4, không lấy payload | Khớp; không đọc jar thật |
| Load đi qua lệnh cũ, giữ chốt chống hạ cấp | cùng lệnh, `downgrade_guard`; đọc `tl_gws.py:1894–1949,2024–2035` | Older=True, equal/fresher=False; `force` mặc định False; load tải bản mã, fallback webapp action `download`, ghi jar cục bộ sau chốt | Khớp phạm vi; unknown age là hành vi nền, không sửa trong packet |
| Không thêm đường ghi registry/credential lên dịch vụ | đọc `CLAUDE.md:7–13`, `muc_tieu` 1 và write set; AST load nói trên | Spec chỉ tái sử dụng `nlm-auth-load`; không thêm endpoint hay ghi trực tiếp Sheets/Drive; marker và jar là local. Quy tắc LockService/RMW của registry giữ tại GAS | Khớp thiết kế; không gọi endpoint thật |
| Các hằng thông báo giữ nguyên; khuôn fragment/bundle có thật | đọc `nlm_cli.py:36–55`; `test_fragments/wp726_script_nlm_canary.py:21,246`; `tl_core/test_fragments.py:464–480` | Bốn hằng tồn tại; `TEST_ID`/`run(tl_module)` đúng; generator ghi mỗi nguồn fragment thành một dòng chuỗi | Khớp mã nền; A12/F3 của implementation tương lai chưa chạy |
| Manifest và kích thước hai fragment mẫu | `python -B source_measurements.py`, `manifest`, `reference_fragment_lines` | 184 mục manifest, cả 4 đường dẫn khai ở write_set:9 có mặt; wp726 = 260 dòng, wp727 = 259 dòng | Khớp, đơn vị tệp/mục/dòng; 495 dòng là ước tính được khai rõ |
| Các dấu hiệu “chưa làm” trên nền | cùng lệnh, `baseline_absence`; `review_checks.py` | ADR-0063 vắng, protocol có 0 lần nhắc, `NAP_LAI/nap_lai` trong adapter = 0; D1/D3/H1 âm trên nền | Khớp; `adr-song` nền rc 0 nhưng D2 tổng thể đỏ do thiếu dòng ADR-0063 |
| E16: A9/A11 cùng đơn vị lời gọi | `review_checks.py`, `A9_A11_model`, đọc r6:116–122,170,172 | Hai lời gọi → từng bộ đệm 1 dòng; tổng 2 dòng/tiến trình, đúng thứ tự nghĩa vụ | Khớp mô hình; không khai đã chạy cơ chế mới chưa có |
| D1 đo riêng mỗi tệp, giữ toàn văn cũ và chấp nhận reflow | `review_checks.py`, `D1` | Mỗi tệp: chèn 1 câu đúng vị trí xanh; không chèn/xoá/chèn đôi/sửa chữ cũ đỏ; chỉ đổi ngắt dòng xanh | Khớp E12/E18; không tái nêu lỗi Markdown cũ đã sửa |
| E17: D2 và D3 cùng xanh trên fixture dương | `review_checks.py`, `ADR.positive` | Source gate rc 0: 62 ADR / 62 dòng bảng; D2 true, D3 true | Khớp |
| Khuôn dòng trạng thái/ô bảng mới khớp nguồn thật | `source_measurements.py`, `line_anchors`; `_ADR_TRANG_THAI` tại 1887–1889 | ADR-0060/0062 dòng 3 đều có `- **Trạng thái:** Accepted (…)`; protocol:1517 ô `ADR-0060` có backtick | Khớp E17 và quét neo r6 |
| D2 bỏ dòng §20; D3 các đột biến câu | `review_checks.py`, `ADR.delete_protocol_row/delete_sentence/600_to_1600/1_to_2_loads/omit_force_prohibition` | Bỏ dòng §20: D2 đỏ, gate rc 9; từng đột biến câu: D3 đỏ; ngắt dòng cùng đoạn: D3 xanh | Khớp các phép âm đã khai |
| D3 trạng thái plain/Proposed/nhân đôi Accepted | cùng lệnh, `ADR.plain_status/proposed_status/duplicate_accepted_status` | Plain: D2 đỏ rc 9 và D3 đỏ; Proposed hay nhân đôi Accepted: D3 đỏ | Khớp các ca này |
| D3 thêm trạng thái mâu thuẫn khác | cùng lệnh, `ADR.second_conflicting_status` | D2 xanh rc 0 và D3 xanh | **Lệch — F01** |
| D3 các quyết định chỉ còn trong comment; nối qua dòng trống | cùng lệnh, `ADR.hidden_decisions/split_across_paragraphs` | Cả D2/D3 xanh; comment che sáu câu khỏi văn bản render (0 lần mỗi câu); câu tách sang đoạn khác vẫn khớp toàn tệp | **Lệch L6b/độ phủ mục tiêu — F02** |
| H1 khuôn changelog/đếm từng cụm | `cat cay-kho/changelog.d/wp-1038.md`; `review_checks.py`, `H1` | Mẫu gốc là văn xuôi bắt đầu `WP1038 (…): `; fixture mới xanh; rỗng/bỏ tiền tố/bỏ từng cụm đều đỏ | Khớp |
| F2 r213 không cần sửa khi thêm ngoại lệ | `review_checks.py`, `F2`, chạy def nguồn với hằng nguồn + tài liệu copy | Base true, thêm câu true, xoá `CẤM` ở QUY_TRINH false | Khớp |
| G2 trên nền | `python -B cay-kho/.claude/dev/packet_loop.py doctrine-scan --root cay-kho` | rc 0: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | Khớp |

Các phép âm trong bảng D2/D3 được đo đúng tiêu chí được khai: bỏ dòng bảng chỉ phải làm D2 đỏ; sửa câu chỉ phải làm D3 đỏ; plain status làm cả hai đỏ. Không suy `cmd_adr_song` kiểm trạng thái Accepted hay sáu quyết định: mã nguồn chỉ kiểm có một trạng thái đọc được.

**Trạng thái đo:** các probe offline ở trên `passed` theo mục đích tái hiện, trong đó F01/F02 chứng minh tiêu chí xanh giả. Full selftest, ruff, bundle-fragment CI, release-verify và CI PR cho implementation tương lai là `not_run`; không gắn nhãn passed. M1 LIVE sau land, độ tươi bundle LIVE, lịch WP710 thực trên laptop, phiên cloud thật và Windows/Cowork là `chưa đo được` trong review offline này. Lịch 30 phút/log bootstrap là bối cảnh runtime đã khai nguồn và phần chưa đo; không được dùng để chứng minh jar LIVE sống. Không có network, Drive/NLM/GAS/GitHub call, đọc/ghi credential thật hay lệnh `tl` gọi dịch vụ. Quyết định “chỉ lần cuối quyết định” và ngoại lệ race hai tiến trình được giữ nguyên theo chỉ thị review.

## FINDINGS

### F01 — P2 — D3 đếm riêng dòng Accepted nên vẫn xanh khi ADR có trạng thái mâu thuẫn

- **Vị trí:** `ops/specs/cloud-setup-p3b-nlm-401-r6.md:176` (D3); liên quan mục tiêu 6, dòng 135–147, và E17 dòng 304.
- **Mô tả:** D3 đếm các dòng bằng đúng `- **Trạng thái:** Accepted`, không đếm tổng số dòng trạng thái. Giữ dòng Accepted và thêm một dòng trạng thái Proposed vẫn thoả mọi vế dương. `cmd_adr_song` nguồn chỉ đòi tìm thấy một dòng trạng thái đọc được, không kiểm tính duy nhất hay đồng thuận. Vì vậy D2 và D3 đều xanh trên ADR tự mâu thuẫn, trong khi cột đột biến khai “thêm dòng trạng thái thứ hai ⇒ D3 ĐỎ”. E17 đã sửa giao của hai phép đo trên fixture dương, nhưng chưa làm đúng phép âm mới này (L3/L6c).
- **Tái hiện đã chạy:** `python -B review_checks.py > review-artifacts-output.log 2>&1` (exit 0), kết quả `review-artifacts/results.json`, mục `ADR.second_conflicting_status`: `D2.pass=true`, `gate_rc=0`, `D3=true`. Cùng bộ đo: `positive` cả hai xanh; `plain_status` cả hai đỏ (gate rc 9); `duplicate_accepted_status` D3 đỏ. Hàm `cmd_adr_song` được lấy nguyên AST từ checkout, chạy trên bản sao `docs` ngoài checkout; D3 được dịch trực tiếp theo câu chữ đặc tả.
- **Đề xuất sửa:** D3 liệt kê TẤT CẢ dòng trạng thái theo khuôn nguồn (sau khi che vùng không render), đòi tổng số đúng 1 và dòng duy nhất bằng đúng dòng Accepted yêu cầu. Thêm đột biến giữ Accepted rồi thêm Proposed, ngoài ca nhân đôi Accepted. Chạy lại D2 và D3 trên cùng fixture.

### F02 — P2 — D3 đếm câu trong vùng không render và nối xuyên đoạn, nên không đo được phần Quyết định thật

- **Vị trí:** `ops/specs/cloud-setup-p3b-nlm-401-r6.md:176`; lời khai áp dụng L6b ở dòng 189–193; yêu cầu mục Quyết định ở dòng 140–147.
- **Mô tả:** Sau khi kiểm dòng Accepted, D3 chỉ gộp khoảng trắng TOÀN tệp rồi đếm sáu câu. Nó không che comment/khối mã, không giới hạn vào mục Quyết định, không giữ biên đoạn. Trong fixture, giữ Accepted và mục Cưỡng chế, nhưng đặt sáu câu Quyết định trong một comment Markdown hợp lệ: không câu nào còn render ra mà D2 và D3 vẫn cùng xanh. `adr-song` chỉ kiểm đăng ký/trạng thái, không kiểm quyết định; vì vậy nó không bù được chỗ mù này. L6b yêu cầu nối trong TỪNG đoạn, không nối qua dòng trống; chú thích “toàn tệp (L6b)” ở r6 khai ngược quy tắc nguồn. Đây là độ phủ của phép đo D3, độc lập với lỗi đếm trạng thái F01.
- **Tái hiện đã chạy:** `python -B review_checks.py` (exit 0), `ADR.hidden_decisions`: D2 `gate_rc=0`, `pass=true`; D3 `true`. `_che_khong_render` NGUỒN che đúng vùng ấy; đếm lại sáu câu trên văn bản đã che ⇒ `[0,0,0,0,0,0]`. Fixture dương bình thường ⇒ `[1,1,1,1,1,1]`. Các bản sao chỉ là tài liệu cục bộ; không có đường dịch vụ.
- **Đề xuất sửa:** D3 dùng văn bản render theo cùng khuôn nguồn, giới hạn vào mục Quyết định và sáu gạch đầu dòng, gộp khoảng trắng trong từng đoạn rồi so nguyên câu. Thêm phép âm khi câu chỉ còn trong comment/khối mã hoặc bị tách thành các đoạn khác nhau; giữ đối chứng ngắt dòng trong cùng đoạn xanh. D1 có phép so toàn tệp để bảo toàn văn bản cũ là một phép riêng; không viện nó để bỏ biên đoạn của phép khớp câu D3.

## TỔNG

| Mức | Số finding |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |
| P3 | 0 |

`request_changes`: F01 và F02 còn mở ở tiêu chí D3 của r6. E16–E18 đã sửa đúng các biểu hiện được giao trước đó; không nêu lại quyết định canary hay race đã được chấp nhận. Checkout cuối lượt giữ nguyên exact HEAD/tree và sạch cả ignored như đầu lượt.
