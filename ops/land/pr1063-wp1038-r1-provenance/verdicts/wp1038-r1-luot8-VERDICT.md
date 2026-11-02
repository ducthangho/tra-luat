verdict: approve
reviewed_sha: f4360ddc7b0b23983816a349066d0fac049a5532

Kết luận chốt: **approve — không còn finding P0–P3 trong phạm vi packet trên SHA được review.** F01–F09 đã được đối chiếu bằng các phép đo bên dưới. Không sửa mã nguồn trong cay-kho/.

review_class: sensitive. Provider: openai_codex; model_family: openai; model theo developer: GPT-6, không có attestation độc lập model/effort/session. execution_surface: codex_service (API/tool runner); transport: machine. Session reference: prompt snapshot run86030e16. Đây là phiên reviewer đọc nguồn và chạy phép đo, không phải phiên executor; không tự cấp assurance/land hoặc đăng ra dịch vụ ngoài.

reviewed_tree: acf1a4e9fa29f781dc9ae2f8a1eecd2a6cc5e496. Base: 8cdb15a786304bab084b43c8b30c127ae87e2594. SPEC sha256: 1071797a1cf2016a9266a98ccece02ed6edd4e80ca33d3b91b2547f7ca0c13e1. diff_tu_luot1.patch không được cấp; đã lưu delta git từ f599ee2 tại evidence/diff-from-round1.patch. Đã đọc cả diff.patch và diff_tu_luot7.patch.

Môi trường Linux, full gate Python3.13.17; parser/r1000 thêm Python3.11.17/3.12.3/3.14.5; Ruff đúng pin0.15.15 từ /usr/local/bin/ruff. Các lệnh tl bỏ bốn biến được yêu cầu và TL_WEBAPP/TL_TOKEN trước khi gọi; phép đo sản phẩm thay tải bằng fixture trong RAM. Không đọc credential thật, không gọi Drive/NLM/LIVE. Lượt selftest đầu dùng cấu hình ký commit của môi trường và bị chặn IPC tới dịch vụ ký localhost; lượt chuẩn hoá tắt ký riêng bằng command-scope env, không sửa cấu hình cây nguồn. Xem bằng chứng G1 bên dưới.

## BẢNG SĂN

HƯỚNG 1: Neo và kích thước
  giả thuyết : cây hoặc đặc tả lệch neo, hoặc vượt trần chủ kho đã duyệt.
  lệnh       : git -C cay-kho rev-parse HEAD; sha256sum SPEC.md; git -C cay-kho diff --numstat 8cdb15a f599ee2; git -C cay-kho diff --numstat 8cdb15a HEAD; git -C cay-kho config core.abbrev
  output     : HEAD=f4360ddc7b0b23983816a349066d0fac049a5532; SPEC=1071797a1cf2016a9266a98ccece02ed6edd4e80ca33d3b91b2547f7ca0c13e1; f599ee2:13 tệp/364 dòng thêm; HEAD:13 tệp/524 dòng thêm; core.abbrev=7; status --short rỗng trước test.
  kết luận   : KHÔNG PHẢI LỖI (trần hiện hành 13/550 theo chỉ thị lượt 8; SPEC đóng băng ghi trần cũ).

HƯỚNG 2: Parser/dispatch và vá F01/F09
  giả thuyết : viết tắt hoặc cờ global tại cấp cha vẫn làm parser nhận leaf khác guard; REMAINDER nuốt cờ con.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python evidence/parser_probe.py
  output     : Python3.13.17: 42/42 phép đo đạt; root, hygiene và rasoat đều allow_abbrev=False. Bảy argv qua main thật rc2/load_creds0; --prof=scan ở hygiene và rasoat đều rc2. Full spelling profile/config, dạng dấu =, deterministic và json ở các cha hợp lệ. Cờ sau -- nằm nguyên trong lenh.
  kết luận   : KHÔNG PHẢI LỖI với các nhánh đã đo. Quét toàn bộ tiền tố cờ dài ở mọi cha: 136/136 rc2, raw evidence/parents-global-prefixes.json. Ma trận42 phép đo đạt trên cả Python3.11.17/3.12.3/3.13.17/3.14.5. Raw evidence/parser-313.log. Hai giả định ban đầu của harness về --json đã sửa theo parser thật (cờ được inject), không tính là lỗi sản phẩm.

HƯỚNG 3: Từng ca r1000 nguyên bản
  giả thuyết : ca mới không chạy hoặc đỏ trong môi trường hermetic.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python evidence/run_r1000.py
  output     : {"passed":15,"total":15,"python":"3.13.17"}; mỗi case ok=true, gồm fail_close, không ghi đĩa và cả hai vế lazy load.
  kết luận   : KHÔNG PHẢI LỖI ở các fixture này; độ nhạy được đo tiếp bằng đột biến. Cả bốn Python3.11–3.14 đều 15/15, raw evidence/r1000-{311,312,314}.log. Raw evidence/r1000-head.log.

HƯỚNG 4: Gate registry/golden/determinism/workflow/manifest và lint delta
  giả thuyết : metadata, snapshot hoặc manifest sai; lint tăng lỗi so base.
  lệnh       : python evidence/run_gates.py (các argv đầy đủ trong evidence/*.result.json); python evidence/static_checks.py
  output     : registry rc0/10 test OK; golden ok=true/rc0; determinism ok=true/rc0; workflow ok=true/registry.issues=[]/199 leaf/201 node/rc0; release ok=true/195 expected_file_count=195 checked_file_count/rc0. Ruff0.15.15: base4541=head4541 (F4016,F8214533,F8112), delta0. Diff thực và diff.patch cùng sha256 d2836f792afce2f4a1411e0fee49e9259bfe9d76972dcef27e3c644490fedb0d; merge-base exact base đúng neo.
  kết luận   : KHÔNG PHẢI LỖI ở các gate này. H5 suite đúng pin đã hoàn tất rc0/44/44 ca nền/43/43 mutant bị giết; lượt khởi động dùng PATH Ruff0.16.9 không dùng làm bằng chứng đạt.

HƯỚNG 5: Đột biến trên bản sao
  giả thuyết : ca xanh nhưng không đo chốt, đặc biệt nhánh Gemini rỗng, lỗi rc126, tệp tạm tự xoá và F09.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python evidence/mutations.py
  output     : 17/17 mutant có ca đích ok=false/rc1. Gồm env cha, đặt cả hai khoá, bỏ kiểm thiếu Gemini, bỏ kiểm Gemini rỗng, bool schema, rc cố định, in secret chỉ ở OSError126, bỏ lenh length, shell=True, bỏ which, đảo fileId, cache blob, tempfile xoá, ciphertext cwd, root abbreviation, parent abbreviation, bỏ lazy. A7 đỏ qua TypeError khi con không tạo output; A6 đỏ qua IndexError; C2 đỏ qua RuntimeError LOAD_CREDS_1000. 14 mutant còn lại trả False.
  kết luận   : KHÔNG PHẢI LỖI về độ nhạy các chốt đã đo; không sửa cây nguồn. Raw evidence/mutations.json và mutant-*.log.

HƯỚNG 6: Fail-close và entrypoint/stdio thật
  giả thuyết : kiểu schema/credential khác fixture hoặc cờ sau -- gây chạy sai con, đổi môi trường hoặc in credential.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python evidence/product_probe.py
  output     : 32/32 phép đo đạt. 9 nhánh lỗi A3 rc4/con0; schema bool/float/2/string/null/list/dict rc4/con0, int1 rc7/con1; mỗi khoá None/rỗng/whitespace/bool/int/list/dict rc4/con0; không yêu cầu khoá sai kiểu vẫn rc7 đúng; fileId rỗng rc4/tải0, fallback và khoá đọc yếu rc7. OSError mang cả hai sentinel: rc126/credential_in_output=false. Con thật rc0/7 giữ stdout và hậu tố stderr chứa NUL/byte FF. main nhận toàn bộ --json/--deterministic/--profile/--config/--gemini sau -- như dữ liệu con, chỉ đặt Claude; TL_DETERMINISTIC không đổi.
  kết luận   : KHÔNG PHẢI LỖI ở ma trận này. Raw evidence/product-probe.log, product-probe.json; entrypoint dùng main/parser/handler nguyên bản và tải giả trong RAM.

HƯỚNG 7: Guard và fixture lịch sử F03–F08
  giả thuyết : bản vá không chặn fixture đã báo hoặc chặn oan Unicode/lệnh đọc LONG.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python evidence/guard_probe.py
  output     : t50 ok=true32/32; t51 ok=true30/30; t52 ok=true30/30, cả tl-auditor và tl-rasoat. Fixture bao gồm tên mở rộng shell, nối dòng, escape, extglob, # giữa giá trị, Unicode và profile ở cha LONG. Full suite đúng pin rc0, TONG: CA 44/44 dat · DOT BIEN 43/43 bi giet, TONG: DAT. Có bằng chứng dương cho cả nền và đột biến, không có ca nền đỏ hoặc mutant sống.
  kết luận   : KHÔNG PHẢI LỖI ở các fixture có sẵn; không coi số này là duyệt hết mọi cú pháp Bash. Raw evidence/guard-probe.log.

HƯỚNG 8: Nghi vấn literal và nối dòng trong nháy đơn
  giả thuyết : bộ tiền xử lý bỏ dữ liệu literal có thể dẫn guard tới tên lệnh tl khác có quyền ghi.
  lệnh       : python evidence/guard_probe.py; python evidence/literal_shell_probe.py
  output     : phép đo inert với --profile literal nối dòng: guard đọc luat còn argv Bash giữ backslash+newline, leaf vẫn profile-list. Nối dòng trong literal tên profile-list: guard allow nhưng parser thật rc2 vì tên gốc không phải lệnh. Literal $(status) trong query locate bị deny oan; literal $(git status) vẫn allow. Không có mở rộng shell thật trong nháy đơn.
  kết luận   : KHÔNG PHẢI LỖI mở quyền trong các phép đo này. Helper chưa hiểu nháy đơn, có chặn oan bảo thủ với dữ liệu query; chưa có bằng chứng bypass guard→tl. Đối chiếu base: cùng cả bốn decision và AST _boc_thay_the không đổi; chặn oan dữ liệu query sau leaf là NGOÀI PHẠM VI packet tên lệnh/credential, được ghi để không biến nghi vấn này thành lỗ mới. Không xếp P0–P3 cho suy đoán. Raw evidence/literal-shell.log; chỉ dùng lệnh đọc vô hại.

HƯỚNG 9: Môi trường chạy G1
  giả thuyết : hai ca đỏ ngoài packet là hồi quy do code.
  lệnh       : python cay-kho/scripts/tl.py --selftest (lượt đầu); đo lại head/base với GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false, PYTHONDONTWRITEBYTECODE=1 python -B scripts/tl.py --selftest
  output     : lượt đầu rc1/1772/1774; đỏ r226_nguong_l2_troi_theo_abbrev_va_ci_ghim và r268_l2_trichotomy_theo_trang_thai_object. Mini-repo độc lập tái hiện git commit rc128 do chương trình ký gọi MCP localhost rồi socket bị sandbox chặn; HEAD chưa tạo được. Đo lại với ký commit tắt riêng cho phép đo: head rc0/1774/1774, base rc0/1759/1759; r226 và r268 đều [OK] ở cả hai. Không đổi cấu hình kho nguồn. Raw evidence/selftest-head-safe.log và selftest-base-safe.log.
  kết luận   : KHÔNG PHẢI LỖI sản phẩm: hai ca đỏ ban đầu do môi trường ký commit; G1 trên môi trường đo đã chuẩn hoá đạt N/N, delta đỏ mới=0.

## BẢNG ĐO

| khẳng định | commit khai | đo được | khớp? |
|---|---|---|---|
| G1 selftest HEAD/base | 1774/1774 và 1759/1759 | rc0/1774/1774; rc0/1759/1759, 0 ca đỏ mới | Có với tiền điều kiện ký commit đã nêu |
| K2 kích thước hiện hành | ≤13 tệp/550 dòng thêm | 13/524 | Có |

| H1 workflow | rc0/issues=[] | rc0/ok=true/issues=[]/199 leaf | Có |
| H3 registry | rc0 | rc0/10 test OK | Có |
| H4 golden + determinism | rc0/ok=true | cả hai rc0/ok=true | Có |
| J1 release | ok=true/expected=checked | ok=true/195=195 | Có |
| K1 Ruff F delta | 0 | 4541→4541, delta0, pin0.15.15 | Có |
| H5 guard table + suite | rc0/đạt hết | table rc0/106 writer/93 DOC; suite rc0/44/44 ca/43/43 mutant bị giết | Có |
| H2 parser snapshot | match, chỉ thêm lệnh mới | ca r77a [OK]; diff JSON chỉ /agent-creds-exec | Có |
| r1000 trên 3.11–3.14 | tất cả đạt | mỗi bản15/15 | Có |
| Parser F09/REMAINDER | từ chối alias ở cha, giữ cờ con | mỗi Python42/42; quét thêm136/136 prefix rc2 trên3.13 | Có |
| Đột biến r1000 | làm ca đích đỏ |17/17 killed, có case.ok=false thực | Có |


## ĐỐI CHIẾU TỪNG TIÊU CHÍ A1–K2

Các `r1000_*` được trích nguyên khối, dựng đúng các tên r973 rồi chạy. Đồ giả tải giữ danh sách fileId/lời gọi; A1/A2/A4/A7 dùng con Python thật. Tất cả 15 ca đạt trên từng Python 3.11.17, 3.12.3, 3.13.17 và 3.14.5. H/G/J/K dùng gate riêng; không quy chúng thành ca r1000.

| Tiêu chí | Mã và ca thực sự đo | Kết quả và độ nhạy |
|---|---|---|
| A1 | `tl_gws.py:1293–1300`; selftest `_c1000_a1`/`r1000_exec_dat_bien_chi_cho_con`, đo trước restore env | Con thấy đúng hai băm; cha vẫn vắng hai biến. Mutant `a1_parent_env` làm ca False. |
| A2 | `_c1000_a2`/`r1000_exec_chi_dat_khoa_duoc_yeu_cau`, chạy cả hai chiều một cờ | Dict tên→băm chỉ có khoá yêu cầu; mutant `a2_both_keys` False. Product probe còn kiểm khoá không yêu cầu sai kiểu không cản con. |
| A3 | `_HONG1000`, `_nhanh1000`, `_c1000_a3`/`r1000_exec_fail_close`; handler1276–1298 | Chín nhánh lỗi riêng, mỗi nhánh rc4/con0; có thiếu và rỗng cho cả hai khoá, schema2 và bool. Mutant bỏ kiểm thiếu Gemini, chỉ bỏ Gemini rỗng, bỏ strict schema đều False. Ma trận kiểu dữ liệu bổ sung cũng fail-close. |
| A4 | `_c1000_a4`/`r1000_exec_tra_nguyen_rc_con`; handler1310 | Con thật 0 và7 trả đúng; mutant `a4_zero_rc` False. Entrypoint/stdin/stdout/stderr thật cũng rc0/7. |
| A5 | `_c1000_a5`/`r1000_exec_khong_in_gia_tri`; `_safe_exc`302 | Thành công và 11 nhánh lỗi: 12 output được so từng sentinel riêng. Mutant chỉ in Gemini ở OSError126 làm False. OSError chứa cả hai sentinel bị rút còn tên lớp, không rò giá trị. |
| A6 | `_c1000_a6`/`r1000_exec_doi_so_sai`; guard cú pháp1267 | Năm argv sai rc2, tổng tải0; return nằm trước resolve/chạy con. Mutant bỏ kiểm lenh length làm ca đỏ bằng IndexError. Ca đếm tải trực tiếp; không khai có spy đếm con trong chính A6. |
| A7 | `_c1000_a7`/`r1000_exec_khong_shell`; argv list ở1310 | Con nhận nguyên văn 5 đối số shell-looking có sẵn trong ca. Mutant shell=True đỏ vì con không tạo kết quả (TypeError khi đọc None). |
| A8 | `_c1000_a8`/`r1000_exec_resolve_which`; handler1302–1306 | which hỏi đúng hai tên, argv chạy chứa đường resolve; tên vắng rc127/con0. Mutant dùng tên thô False. Không dùng giả lập này để khai đã đo Windows thật. |
| A9 | `_c1000_a9`/`r1000_exec_env_thang_hang`; fileId1272 | Tải ENV1000 dù hằng HANG1000; đảo ưu tiên làm False. Product probe thêm fallback hằng và rỗng cả hai. |
| A10 | `_c1000_a10`/`r1000_exec_tai_moi_lan`; tải1279 | Ghép danh sách lời gọi hai lượt đúng `[AC1000,AC1000]`; mutant cache blob làm False. Mỗi lần wrapper thay hàm tải nhưng state cache sản phẩm giả vẫn sống qua hai lượt. |
| A11 | `_c1000_a11`/`r1000_exec_khong_ghi_dia` | Bọc builtins.open/io.open/os.open và 4 API tempfile; tổng ghi0; con giả nhận đúng env; quét sentinel HOME/cwd/temp sau lệnh. Mutant tempfile tự xoá và ciphertext cwd đều False, bắt được cả tệp không còn tồn tại cuối lượt. |
| B1 | hằng `tl_gws.py:1089`; `r1000_agent_creds_fileid_that` | So nguyên chuỗi fileId đóng băng, ca True; diff base cho hằng rỗng→fileId được cấp. Không gọi Drive/LIVE để xác minh lại file thật. |
| C1 | `cli.py:153–157`; `r1000_parser_agent_creds_exec_help` | Parser thật --help rc0, chứa cả hai cờ; parser mới tồn tại đúng một lần trong diff. Ma trận riêng đo REMAINDER, cờ sau -- và mọi cấp cha. |
| C2 | `_CREDS_LAZY_CMDS`1316/main1336; `_c1000_c2`/`r1000_exec_khong_goi_load_creds` | (a) main thật, spy load_creds0/rc4/thông báo agent-creds-exec; (b) bản sao scripts/cwd/HOME riêng, tất cả candidate config vắng rồi CLI rc4. Bỏ lazy làm ca đỏ bằng RuntimeError LOAD_CREDS_1000. |
| H1 | metadata `command_registry.py:1951`; workflow-audit strict | rc0/ok=true, registry.issues=[],199 leaf/201 node/100% coverage, metadata lệnh mới read_only=False, scope local, builtin gate hiện diện. |
| H2 | `r77a_parser_surface_matches_snapshot` tại selftest6656; snapshot parser | [OK] trong full selftest, TL_WRITE_PARSER_SURFACE vắng. So JSON base/head chỉ thêm `/agent-creds-exec`, không đổi entry cũ. |
| H3 | `command_registry_test.py`, ratchet199 leaf/201 node | rc0/10 test OK; thay đổi trong tệp chỉ số đếm và mô tả tương ứng. |
| H4 | golden-test và determinism-audit strict | rc0/20/20 golden case ok, rc0/15/15 determinism check ok. Hai golden chỉ thêm lệnh mới và điều chỉnh số đếm, được so diff JSON có cấu trúc. |
| H5 | guard `_TL_LENH_GHI`, allowlist DOC, tokenizer, t50/t51/t52, suite đầy đủ | Table đúng pin rc0/106 writer/93 DOC; t50 32/32, t51 30/30, t52 30/30. Suite đầy đủ đúng pin rc0/44/44 ca/43/43 mutant bị giết (guard-suite-pinned.log); không dùng lượt sai pin làm chứng cứ pass. |
| G1 | full selftest trên exact head và exact base, core.abbrev7 | Head rc0/1774/1774; base rc0/1759/1759; đối chiếu multiset nhãn ca: thêm đúng15 r1000, bỏ0, fail0 (g1-comparison.json). Một nhãn hiển thị trùng lịch sử có ở cả hai phía, không dùng set để đếm N/N.  Lượt mặc định1772/1774 là lỗi môi trường ký commit; cả hai ca đỏ đều OK khi tắt ký trong phép đo. Windows giao phiên riêng theo chỉ thị. |
| J1 | release-verify strict trên manifest nguyên bản | rc0/ok=true, expected_file_count=195=checked_file_count; package_hash_current=package_hash_expected và package_hash_match=true. |
| K1 | Ruff0.15.15 `check --no-cache --select F --output-format json` trên 8 tệp Python thay đổi | Base4541=head4541, cùng F4016/F8214533/F8112; so multiset (tệp,code,message), thêm0/xoá0; delta0. Các cây lint nằm ngoài source. Không gọi nền rc1 thành lint tuyệt đối sạch. |
| K2 | numstat exact base→head và exact base→f599ee2 | Head13 tệp/524 thêm/58 xoá; f599ee2 13/364/43. Đạt trần13/550 theo quyết định chủ kho trong prompt; không dùng trần450 cũ của SPEC để báo sai. |


## ĐỐI CHIẾU LƯỢT TRƯỚC

| finding | trạng thái đo lại | lệnh + output thật |
|---|---|---|
| F01 root abbreviation | Đã vá trên nhánh đã báo | parser_probe.py trên Python3.11–3.14: bốn argv qua main rc2/load0; r1000_tl_tu_choi_co_goc_viet_tat ok=true. mutations.py f01_root_abbrev làm ca False. |
| F02 schema true | Đã vá | product_probe.py: bool/float/schema khác1 rc4/con0; int1 rc7/con1. mutations.py f02_schema_bool làm fail_close False. |
| F03 tên qua shell expansion | Đã chặn fixture cũ | guard_probe.py t51 ok=true30/30, gồm hai agent; t50 32/32. Chỉ chạy fixture có sẵn, không tạo chuỗi vượt guard mới. |
| F04 nối dòng Bash | Đã chặn fixture cũ, literal chỉ đo riêng | guard_probe.py t52 ok=true30/30. literal_shell_probe.py: tên lệnh chứa literal newline được guard chuẩn hoá nhưng parser thật rc2; chưa thấy chuyển sang writer. |
| F05 Unicode global | Đã vá fixture cũ | guard_probe.py t52 ok=true30/30: config Quốc hội và profile luật đều allow ở cả hai agent. |
| F06 extglob chia token | Đã chặn fixture cũ | guard_probe.py t52 ok=true30/30 với ba fixture extglob hiện có; không tạo expression mới. |
| F07 midword hash | Đã chặn fixture cũ | guard_probe.py t52 ok=true30/30, fixture --profile a#b agent-creds-exec bị deny cả hai agent; source lex.commenters rỗng đúng quyết định chủ kho. |
| F08 LONG giá trị cờ | Đã vá full spelling | guard_probe.py t52 30/30: hygiene --profile plan scan allow, hygiene --profile scan plan deny. parser_probe.py full profile/config và dạng = chọn đúng lá. |
| F09 viết tắt ở cha LONG | Đã vá bằng parser từ chối | parser_probe.py: root/hygiene/rasoat đều allow_abbrev=False; --prof/--pro/--conf/--det và --prof=scan/--conf=scan đều rc2 ở các cha; main thật với hygiene --prof scan plan q và --prof=scan đều rc2/load0. Full spelling/--deterministic/--json được nhận. mutations.py f09_parent_abbrev làm ca đích False. |


Đối chứng độ nhạy guard đã chạy xong bằng `PATH=/usr/local/bin:$PATH PYTHONDONTWRITEBYTECODE=1 python -B .claude/hooks/pretooluse_guard_test.py` (bỏ bốn biến credential trước lệnh). Raw `evidence/guard-suite-pinned.log`, trích riêng `evidence/previous-findings-mutation-proof.json`:

- F03: `GIET m37_cho_dau_dola_vao_vung_ten_lenh_tl lam DO: t51_ten_lenh_tl_qua_mo_rong_shell_bi_chan`
- F04: `GIET m40_noi_dong_bang_dau_cach     lam DO: t52_ten_lenh_tl_phai_KHOP_danh_sach_DOC`
- F05: `GIET m41_vung_ten_chi_ASCII         lam DO: t52_ten_lenh_tl_phai_KHOP_danh_sach_DOC`
- F06: `GIET m39_bo_chot_danh_sach_lenh_DOC lam DO: t52_ten_lenh_tl_phai_KHOP_danh_sach_DOC`
- F07: `GIET m42_shlex_cat_comment_giua_tu  lam DO: t52_ten_lenh_tl_phai_KHOP_danh_sach_DOC`
- F08: `GIET m43_bo_gia_tri_co_global_sau_ten_cha lam DO: t52_ten_lenh_tl_phai_KHOP_danh_sach_DOC`
- `GIET m38_bo_chot_THAYTHE_o_vung_ten_lenh_tl lam DO: t51_ten_lenh_tl_qua_mo_rong_shell_bi_chan`
- `GIET m44_noi_dong_ca_khi_cheo_nguoc_bi_escape lam DO: t52_ten_lenh_tl_phai_KHOP_danh_sach_DOC`

## PHÁT HIỆN VÀ GIỚI HẠN

Không có finding P0–P3 còn mở trong ranh giới packet. Các fixture lịch sử đã báo đều được chặn hoặc parser từ chối theo quyết định chủ kho. Không suy từ chúng rằng đã vét cạn toàn bộ ngữ pháp Bash; không dựng chuỗi vượt guard mới ngoài phân công.

NGOÀI PHẠM VI: `_boc_thay_the` vẫn có thể chặn oan literal trong dữ liệu truy vấn sau leaf. Đã đo với Bash/parser thật và đối chiếu base cùng hành vi, AST helper không đổi; không phải bằng chứng mở đường tới lệnh credential. Nối dòng trong nháy đơn chưa được helper hiểu đúng, nhưng các trường hợp đã đo chỉ giữ leaf đọc hoặc bị parser từ chối tên không hợp lệ.

Windows thật/PATHEXT/.CMD/mã thoát Windows: KHÔNG ĐO ĐƯỢC trong Linux này, do phiên điều phối đo riêng theo prompt; không tính finding. L1 CI và M1 LIVE ngoài phạm vi, không khai đã đạt. Không gọi mạng ngoài, Drive/NLM hoặc sử dụng credential thật; các thử nghiệm hành vi credential dùng fixture. Lượt đầu git fixture cố dùng dịch vụ ký localhost và bị sandbox chặn; đã loại phụ thuộc đó trong lượt G1 chốt bằng commit.gpgsign=false riêng cho tiến trình đo.

Kiểm cuối: HEAD/tree/SPEC đúng neo; git status --porcelain rỗng; cả13 tệp thuộc diff byte-match blob HEAD (evidence/final-source-check.json). G1 head/base đã hoàn tất; full guard đã hoàn tất với bằng chứng dương. Verdict chỉ lưu cục bộ, không tự cấp quyền merge/land hoặc assurance từ nhận dạng model chưa được attestation.
