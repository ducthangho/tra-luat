verdict: request_changes
reviewed_sha: dc693d258e95ee94ea5f5e384aba6d5fef4f3619
reviewed_tree: 7211ec9bf6ac0b932e3d3baee950b52cc0a20ced

Review **ĐẶC TẢ r5**, chưa phải review triển khai. Reviewer: Codex/OpenAI, độc lập với context Claude executor theo PROMPT; thực thi phép đo bằng công cụ shell cục bộ, transport machine. Không có attestation độc lập về tên model/effort phục vụ; không suy danh tính reviewer từ tài khoản GitHub. Không gọi mạng, Drive, NLM, webapp, GitHub hoặc đọc/ghi credential thật. Checkout chỉ đọc; mọi script, log và fixture đặt ngoài `cay-kho/`.

## (i) DANH TÍNH

Lệnh đầu tiên sau khi đọc PROMPT đã tạo `VERDICT.md` với `verdict: pending`; từng finding được ghi ngay khi xác nhận. Danh tính đầu lượt:

```console
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
dc693d258e95ee94ea5f5e384aba6d5fef4f3619
7211ec9bf6ac0b932e3d3baee950b52cc0a20ced
$ git -C cay-kho status --porcelain=v1 --ignored
```

Cả hai lệnh rc 0; status rỗng. Lệnh `sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3,4,5}.md` rc 0:

| revision | SHA-256 đầu lượt, cũng khớp cuối lượt |
|---|---|
| r1 | `15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e` |
| r2 | `c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d` |
| r3 | `e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121` |
| r4 | `d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f` |
| r5 | `25473237f53684706112b5a2f8dfafce143000110a57c8d680f3b44f924e5ed5` |

`diff.patch` bằng từng byte kết quả `git -C cay-kho diff 1f0941e9 HEAD`. Diff này chỉ thêm r4 (259 dòng) và r5 (287 dòng), tổng 546 dòng thêm / 2 tệp; không có mã triển khai. Base review là `1f0941e9` đã ghim trong PROMPT. Ref `origin/master` cục bộ đang ở `8983e1bbf00c91d8def101a97a4d32509ae630cc`; không dùng ref ấy thay base đã ghim, không fetch và không suy trạng thái GitHub/lease hiện tại từ nó.

## (ii) ĐO LẠI KHẲNG ĐỊNH

Phép đo hành vi và fixture: `PYTHONDONTWRITEBYTECODE=1 python3 review_measure.py > review_measure.log` — rc 0. Kết quả máy đọc được: [review_measure.json](review_measure.json); nguồn phép đo: [review_measure.py](review_measure.py). Thời điểm phép đo trong JSON: **2026-11-04T16:11:07.828253+00:00**. Mọi số đếm dưới đây là số đo của lượt này trên exact head nêu trên, trừ số lịch sử đã ghi riêng commit.

Script dùng AST lấy đúng hàm nguồn, chỉ thay dependency bên ngoài bằng đồ giả trong RAM. Fixture tài liệu là bản sao ngoài checkout. Kết quả thử thước không được diễn giải thành feature tương lai đã thi hành.

| Khẳng định | Lệnh đo / nguồn phép đo | Kết quả | Khớp/lệch |
|---|---|---|---|
| 9 mục tiêu, mỗi mục chiếu đúng một đường dẫn write_set | `review_measure.py`, `history_and_diff.write_set_goals`; đối chiếu r5:48–56 và 83–148 | Đúng 9 đường dẫn riêng, không wildcard; A*→1, F1→2/3, F3→3, D1→4/5, D2/D3→6/7, H1→8, J1→9; mọi mục tiêu có tiêu chí | Khớp L1/L2/L3 về ánh xạ |
| `nlm_cli.py:143` nhận diện auth | `nl -ba cay-kho/scripts/nlm_cli.py`; JSON `current_line_anchors` đọc riêng dòng 143 | `auth = any(...)` với `auth`, `401`, `login`, `unauthor`, `credential` | Khớp |
| `nlm_cli.py:162` nhận diện auth | Cùng phép, đọc riêng dòng 162 | Cùng bộ năm chuỗi trong `_run_json` | Khớp |
| `nlm_cli.py:229` nhận diện auth | Cùng phép, đọc riêng dòng 229 | Cùng bộ năm chuỗi trong `_auth_fail` | Khớp |
| `_run`, tuple kết quả, rc 124/127; `TL_NLM_BIN` | AST `_run` thật với subprocess giả; `nlm_cli.py:88–124` | `_run` ở 110; bình thường trả tuple; timeout→124, thiếu binary→127; `nlm_exe` xét `TL_NLM_BIN` ở 91–93 | Khớp |
| Điều cấm RASOAT ở 118–119 | `nl -ba cay-kho/references/RASOAT_HOSO_LOOP.md`; JSON đọc từng dòng 118,119 | Dòng 118 bắt đầu phần `CẤM tự`, 119 tiếp `nlm-auth-load` và ngoặc về jar cũ/cũng chết | Khớp E14 |
| Gạch “Sửa xác thực” QUY_TRINH ở 49 | `nl -ba cay-kho/references/QUY_TRINH_RA_SOAT_3_TANG.md`; JSON dòng 49 | Có `**CẤM** tự`, không phải chuỗi thô `CẤM tự` | Khớp E8/E14 |
| `_AUTH_FIX_FALLBACK` ở `nlm_ops.py:297` | `nl -ba cay-kho/scripts/tl_core/nlm_ops.py`; JSON dòng 297 | Đúng dòng khai báo; 296 là chú thích | Khớp E14 |
| `_c213_auth_carve_out_khong_pha_thu_tu` ở 24829 | `nl -ba cay-kho/scripts/tl_selftest.py`; JSON dòng 24829 | Đúng dòng `def`; đăng ký tên ca ở 24852 | Khớp E10/E14 |
| `_nlm_auth_alive` ở 308–363 | `nl -ba cay-kho/scripts/tl_gws.py`; đọc riêng neo 308,363 và thân hàm | 308 là `def`, 363 là `return None` cuối; vòng lặp tối đa 3 lần, timeout mặc định 30 giây, backoff 1,5 + 3 giây = 4,5 giây | Khớp |
| Canary sáu ca A13, quyết định theo lần cuối | JSON `A13_source_only`; AST cả `_nlm_auth_alive` và `_nlm_canary_raw_get` thật, CLI/sleep giả | `None,None,False,False,False,None`; ánh xạ mã 2,2,3,3,3,2 đúng; quyền 403 dừng sau 1 probe, các chuỗi auth/mạng thử tối đa 3 | Khớp; không nêu lại quyết định đã chấp nhận |
| Thân canary hiện có ở `nlm-auto-refresh.sh:93–105` | `nl -ba cay-kho/scripts/nlm-auto-refresh.sh`; JSON đọc TỪNG dòng 93–105 | Import `tl`, `_imp`, `bind`, `require_notebook_body=True`, ngoại lệ→None, mã 0/3/2 đúng; `env-reimport.sh:105`, `nlm-auth-import.sh:78` cũng gọi probe này | Khớp |
| `_nlm_preflight_report` gộp lỗi probe thành False ở 1424–1430 | `nl -ba cay-kho/scripts/tl_core/nlm_ops.py`; JSON đọc từng dòng 1424–1430 | `notebook_get`, `bool(ok)` và nhánh except gán False đúng; không còn được dùng làm canary trong r5 | Khớp E6; không coi trạng thái này là canary ba trạng thái |
| Chốt hạ cấp có sẵn, lệnh nạp và credential path | AST `_nlm_auth_load_downgrade` thật + bundle/local giả; đọc `tl_gws.py:1894–1967,2024–2035` | Có mốc thời gian: bundle cũ→chặn, bằng/mới→không chặn; `cmd_nlm_auth_load` gọi loader với force mặc định False. Loader tải `nlm_cred.enc` public, fallback GAS `download`, rồi ghi jar local; không chạy loader thật | Khớp phạm vi lời khai giữ chốt |
| D1 so toàn tệp, mỗi tệp riêng | JSON `D1_RASOAT`, `D1_QUY_TRINH` | Mỗi tệp: chèn câu đúng bằng dấu cách/xuống dòng và đổi thụt lề XANH; không chèn, chèn hai lần, bỏ ngoặc/`**`, sửa chữ cũ ở phần khác ĐỎ | Đột biến E12 khớp |
| D3 khớp đủ sáu câu thay vì token | JSON `D3` | Đúng sáu câu và ngắt dòng giữa câu XANH; xoá riêng từng câu, `600→1600`, `1 lần→2 lần`, bỏ mệnh đề không `--force` ĐỎ | Đột biến E11 khớp; status còn F02 |
| D2 và D3 cùng đo một ADR hợp lệ | JSON `D2_D3_status_format`; hàm nguồn `cmd_adr_song` trên bản sao docs | Dòng trạng thái thô: D3 XANH, D2 rc 9. Dòng Markdown theo kho: D3 ĐỎ, D2 rc 0 | **Lệch — F02** |
| D2 xoá dòng §20 phải ĐỎ | Cùng fixture trên, trạng thái Markdown hợp lệ; xoá riêng dòng ADR-0063 | rc 9, đúng lỗi có tệp mà thiếu dòng §20 | Khớp |
| H1 có tiền tố và bốn cụm; khuôn changelog | JSON `H1`; `cat cay-kho/changelog.d/wp-1038.md` | Khuôn WP1038 là đoạn tiếng Anh đúng tiền tố; fixture WP1099 đúng/ngắt dòng XANH; rỗng, thiếu tiền tố, thiếu riêng từng cụm ĐỎ | Khớp E15 |
| A11 ≤1 dòng stderr/tiến trình khi A9 gọi hai lần | JSON `A9_A11_contract_model`; đối chiếu r5:116–117,166,168 | Mô hình nghĩa vụ đòi 2 dòng trong cùng tiến trình; điều kiện ≤1 ĐỎ | **Lệch — F01** |
| F2 xanh nguyên trạng và không bị câu ngoại lệ phá | JSON `F2_source_only`; chạy đúng hàm nguồn r213 với namespace hằng thật, dependency import giả | Base XANH; thêm câu ngoại lệ XANH; xoá `CẤM` trong QUY_TRINH ĐỎ. Không sửa `tl_selftest.py` | Khớp |
| Manifest 184 tệp, chứa bốn tệp cần tái sinh | JSON `manifest_schema`, `manifest_four_paths` | `file_count=len(files)=184`; cả bốn path có mặt và SHA-256 hiện tại khớp manifest | Khớp E10 |
| Khuôn fragment, generator và một dòng chuỗi/fragment | Đọc `scripts/tl_core/test_fragments.py:287–325,451–481` và `tl_selftest.py:31666–31678` | Hợp đồng `TEST_ID`/`run(tl_module)` đúng; generator có tên `generate_bundled_module_bytes`; mỗi fragment thành một tuple source trên một dòng; selftest đăng ký mỗi fragment thành một case ngoài, các phép con không tự tăng N | Khớp; F1 phải đếm case đăng ký của loader |
| Khuôn đối chiếu 260/259 dòng | `wc -l cay-kho/scripts/test_fragments/wp{726_script_nlm_canary,727_tl_gws_refresh}.py` | Lần lượt 260 và 259 dòng, đúng source hiện tại | Khớp |
| CI có `bundled-fragment check (topology gói)` và pin abbrev | `rg -n 'bundled-fragment|core.abbrev' cay-kho/.github/workflows/ci.yml`; đọc 293–295 | Có bước và đúng lệnh check `--json`; job Ubuntu ghim `core.abbrev=7` | Khớp; chưa chạy CI |
| G2 xanh sẵn trên nền | `cd cay-kho` rồi `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py --state-dir ../review-state doctrine-scan --root .` | rc 0; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` | Khớp |
| Cổng ADR nền xanh | Cùng môi trường, `... packet_loop.py --state-dir ../review-state adr-song --root .` | rc 0; 61 ADR / 61 dòng §20, khớp 1–1 | Khớp |
| Chưa có feature mới, ADR-0063 và changelog WP1099 | Đọc source/đường dẫn, đếm AST/chuỗi và fixture base trong script | Base không có cơ chế `nap_lai`; không ADR-0063, không `wp-1099.md`; câu ngoại lệ vắng ở cả hai tài liệu. Màu “chưa làm” phù hợp | Khớp |
| Source của các neo không đổi từ base r1 | `git -C cay-kho diff --stat 90c101b8 HEAD -- scripts/nlm_cli.py references/RASOAT_HOSO_LOOP.md references/QUY_TRINH_RA_SOAT_3_TANG.md scripts/tl_gws.py scripts/tl_core/nlm_ops.py` | rc 0, output rỗng; không suy tính đúng của neo chỉ từ diff rỗng, đã đọc riêng các neo ở trên | Khớp E3/E10/E14 |
| Chuỗi errata không bị viết lại | JSON `historical_errata_preserved`; so phần E1–E5/E6/E7–E10 với đúng revision nguồn | Cả `errata_r2`, `errata_r3`, `errata_r4` giữ nguyên. `git show` trên c7174bfe: selftest def 24827, manifest 198; trên 1f0941e9: def 24829, manifest 184; trên 90c101b8: manifest 197 | Khớp chuỗi sửa; neo lịch sử không bị dùng làm neo hiện hành |
| OID land ADR-0052/0053 | `git show --no-patch --format='%H%n%P%n%s' 8ab100793df9831505f495543a74044b91c2c9ab`; `git cat-file -e` tại OID và `^1` | Đúng merge PR #791; cả hai ADR có tại OID (rc 0), vắng ở first parent (rc 128) | Khớp |

### Trần bảo đảm, Standards/Security và phần chưa đo

Ba nơi `van_de` (41–42), mục tiêu 1 (88–105) và mục tiêu 6 (135,141) đều cùng phân biệt **1 lần nạp/tiến trình là bảo đảm**, **600 giây giữa tiến trình là best effort**; `chua_do_duoc` 222–223 ghi cùng ngoại lệ cạnh tranh. Không yêu cầu đổi quyết định giữ canary theo lần cuối hoặc ngoại lệ hai tiến trình.

Đối chiếu `CLAUDE.md` “Nguồn sự thật”, protocol §8/§11/§20 và soan-spec L1–L6: write_set không thêm writer registry/credential từ xa hoặc endpoint webapp; đường nạp yêu cầu tái dùng CLI có sẵn, không force, không lấy `tl_secrets.enc`, không tự chạy lại argv ghi; mã canary khác 3/timeout/lỗi không được nạp; đầu ra con phải bị giữ kín. Source GAS target `references/Code.2.21.2p.gs` có `LockService.getScriptLock()`; packet không sửa nó. Không phát hiện yêu cầu thêm đường ghi thứ ba. Đây là kết luận về hợp đồng spec/source, chưa xác nhận triển khai an toàn.

M1, chất lượng/tính tươi credential LIVE, scheduler laptop đang chạy thật mỗi 30 phút, log bootstrap, liveness cloud, quyền owner/lease và facts GitHub là **chưa đo được** trong review offline này. Spec đã ghi rõ các giới hạn LIVE chính; không dùng phép đo đồ giả thay M1. Ước lượng ~495 dòng/9 tệp là ước lượng có ghi thời điểm, không phải numstat triển khai. Full selftest, bare Ruff, bundled-fragment execution, release-verify, CI và Windows **not_run**: r5 chưa triển khai feature, và lượt này không gọi runtime thật lên dịch vụ. `git diff --check 1f0941e9 HEAD` đã chạy, rc 0.

## (iii) FINDINGS

### F01— P2 — `nghiem-thu-khac-don-vi-dem-log`

- Neo: `ops/specs/cloud-setup-p3b-nlm-401-r5.md:168` (A11), đối chiếu mục tiêu 1 dòng 116–117 và A9 dòng 166.
- Mô tả: A11 đòi stderr của TIẾN TRÌNH có tối đa một dòng `nlm_nap_lai:` trong mọi ca A, nhưng ca đầu A9 bắt buộc hai lần `_run` trong cùng tiến trình. Lần đầu nạp xong jar vẫn chết phải báo `BUNDLE CŨNG CHẾT`; lần hai đi vào bước Giới hạn và phải báo `BỎ QUA — đã nạp …`. Theo mục tiêu 1, mỗi lần ấy in đúng một dòng; tổng bắt buộc là hai. Không thể đồng thời đạt cả ba nghĩa vụ nếu A11 đo toàn ca/tiến trình như văn bản đang viết.
- Phép đo: `PYTHONDONTWRITEBYTECODE=1 python3 review_measure.py` (rc 0), mục `A9_A11_contract_model` trong `review_measure.json`: `invocations_in_one_process=2`, `diagnostic_lines_required_by_goal_1=2`, `A11_at_most_one_line_per_process=false`. Đây là mô hình nghĩa vụ của đặc tả, không khai đã chạy một bản triển khai tương lai.
- Đề xuất: thống nhất đơn vị thành mỗi LỜI GỌI `_run` (≤1 dòng/lời gọi, đúng 1 khi đi qua Giới hạn); A9 đo riêng hai khoảng stderr hoặc đòi hai dòng theo thứ tự. Giữ nguyên các yêu cầu chống rò đầu ra của con.

### F02— P2 — `thuoc-do-chuoi-khong-khop-markdown-nguon`

- Neo: `ops/specs/cloud-setup-p3b-nlm-401-r5.md:172` (D3), đối chiếu mục tiêu 6 dòng 133 và D2 dòng 171.
- Mô tả: D3 đòi đúng một dòng nguyên văn `Trạng thái: Accepted`. Cổng `adr-song` thật chỉ nhận dạng dòng có dấu đầu mục và chữ đậm (regex `_ADR_TRANG_THAI` ở `.claude/dev/packet_loop.py:1887`), ví dụ `- **Trạng thái:** Accepted`. Gộp khoảng trắng không bỏ dấu `-`/`**`. Một ADR với một dòng trạng thái theo D3 làm D2 ĐỎ; đổi sang khuôn đang dùng trong kho để D2 XANH lại làm D3 ĐỎ. Muốn qua cả hai theo lời hiện tại phải thêm hai bản trạng thái, thay vì một dòng hợp lệ thống nhất. Đây là biểu hiện còn sót của lớp r4 E8: thước khớp chuỗi bỏ qua Markdown của nguồn.
- Phép đo: `PYTHONDONTWRITEBYTECODE=1 python3 review_measure.py` (rc 0), `D2_D3_status_format` trong `review_measure.json`. Chạy hàm NGUỒN `cmd_adr_song` và các helper thật (AST, không import launcher), trên bản sao docs ngoài checkout: nền thật rc 0; ADR có đủ sáu câu và trạng thái nguyên văn ⇒ D3=true, gate rc 9 với lỗi “không có dòng Trạng thái đọc được”; cùng nội dung chỉ đổi dòng trạng thái thành `- **Trạng thái:** Accepted` ⇒ D3=false, gate rc 0. Đối chứng xoá dòng đăng ký ADR-0063 ⇒ gate rc 9 đúng lý do thiếu §20.
- Đề xuất: quy định một dòng trạng thái Markdown thật mà `_ADR_TRANG_THAI` nhận, sửa D3 để khớp toàn dòng đó (hoặc parse cùng cấu trúc rồi so giá trị Accepted); chạy chung D2+D3 trên cùng fixture dương và thêm đột biến bỏ/sửa trạng thái. Không cần mở rộng write set để sửa cổng.

### Đối chiếu finding trước và lớp nguyên nhân

| Nguồn r4 được r5 dẫn lại | Phép kiểm đóng biểu hiện | Kết luận lượt này |
|---|---|---|
| F01 P2 → E11/E12: thước D1/D3 mù với sửa hậu tố | D1 trên hai tệp thật, D3 trên từng câu, mutant/control ở JSON | Các đột biến đã khai được vá; chưa đóng toàn lớp thước đo chuỗi vì còn F02 về Markdown trạng thái |
| F02 P3 → E14: neo dòng sai | Đọc riêng mọi neo hiện hành | Đã vá các biểu hiện được giao |
| F03 P2 → E13: lời hứa trần mạnh hơn mô hình | Đối chiếu ba nơi + `chua_do_duoc` | Đã vá lời khai; giữ quyết định ngoại lệ cạnh tranh của chủ kho |
| F04 P3 → E15: mục tiêu 8 thiếu nghiệm thu | H1 dương/âm, từng cụm riêng và reflow | Đã vá biểu hiện được giao |

Hai lớp đang mở: `nghiem-thu-khac-don-vi-dem-log` (F01) và `thuoc-do-chuoi-khong-khop-markdown-nguon` (F02). Mỗi lớp có một biểu hiện trong báo cáo, mức cao nhất P2. F02 nối lớp Markdown của E8/r3: phép đo đúng phải dùng cấu trúc nguyên văn mà gate thật nhận. Cách đóng và đối chứng riêng đã nêu ở từng finding; không coi sửa những biểu hiện đã biết là bằng chứng không còn biểu hiện khác.

## (iv) TỔNG

| Mức | Số finding mở |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 2 |
| P3 | 0 |

Tổng **2 finding / 2 lớp**, nên `request_changes`. Cần thống nhất đơn vị stderr của A9/A11 và sửa thước trạng thái D3 để cùng fixture dương đạt cả D2 lẫn D3. Không cần sửa code hoặc đổi write_set để chữa hai lỗi đặc tả này.

### Danh tính cuối lượt

Đo **2026-11-04T16:15:40.083179+00:00**, [final_identity.json](final_identity.json):

```console
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
dc693d258e95ee94ea5f5e384aba6d5fef4f3619
7211ec9bf6ac0b932e3d3baee950b52cc0a20ced
$ git -C cay-kho status --porcelain=v1 --ignored
$ git -C cay-kho diff --raw
$ git -C cay-kho diff --cached --raw
```

Tất cả rc 0; ba lệnh cuối output rỗng. Băm năm spec cuối lượt bằng đầu lượt. HEAD/tree/index/checkout không có delta quan sát được giữa hai mốc. Sandbox cho phép ghi workspace về kỹ thuật; read-only đối với checkout được giữ bằng phạm vi thao tác, không tự nhận có rào filesystem riêng cho `cay-kho/`. Snapshot không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên; trong lượt này không thực hiện thao tác ghi/commit/checkout trong cây được review.
