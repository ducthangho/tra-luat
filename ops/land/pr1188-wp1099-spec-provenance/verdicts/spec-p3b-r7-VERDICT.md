verdict: request_changes
reviewed_sha: bc1d5e048cc7889e6a759027059c5dd4735a4678
reviewed_tree: d72a43cefaad037904de9d3c4ac15c169cf96ce6

## DANH TÍNH

Đo trước review: HEAD/tree đúng yêu cầu; status (bao gồm ignored) rỗng.

```text
$ git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
bc1d5e048cc7889e6a759027059c5dd4735a4678
d72a43cefaad037904de9d3c4ac15c169cf96ce6
$ git -C cay-kho status --porcelain=v1 --ignored
(output rỗng)
$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3,4,5,6,7}.md
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md
25473237f53684706112b5a2f8dfafce143000110a57c8d680f3b44f924e5ed5  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r5.md
b078da106387512cac956d8bc18d702bb50cfcf4bfd37101bb6c7aeb0686d201  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r6.md
887dc78a1f20d640f1b779b58fea7c963b2931e76e31abbe00ca13960d699061  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r7.md
```

Phạm vi: review ĐẶC TẢ r7; r1–r6 chỉ đối chiếu chuỗi errata. Provider: OpenAI/Codex, phiên API có công cụ shell cục bộ, transport machine; không phải ChatGPT Web human-mediated. Model theo chỉ dẫn runtime: GPT-6; không tự xác minh backend/effort hoặc provenance của launcher. Không có context Executor, không dùng subagent.

Quy tắc đối chiếu: `AGENTS.md`, `CONTEXT.md`, `CLAUDE.md` (Nguồn sự thật, bài học phép đo/đột biến, deploy mục 5), `.claude/skills/soan-spec/SKILL.md` L1–L6, `docs/PROTOCOL_DA_PHIEN.md` (verdict contract, §8/8.2/8.3, §11, §20), kế hoạch đa provider và chỉ thị trong `PROMPT.md`. Không thực hiện các bước bootstrap/LIVE của tài liệu vận hành vì prompt review cấm rõ.

## ĐO LẠI KHẲNG ĐỊNH

Lệnh dưới đây chạy từ SANDBOX. Đơn vị là đường dẫn, dòng mã, ca fixture hoặc giây theo từng hàng. Mốc đo của bảng nguồn: `2026-11-04T16:42:32.371644+00:00`; mốc fixture trong `review_summary.json`. Đầu ra bền: `measure_claims.log`, `measure_claims_results.json`, `review_v.log`, `review_v_results.json`, `review_behavior.log`, `review_behavior_results.json`.

| Khẳng định trong r7 | Lệnh/phép đo | Kết quả | Khớp/lệch |
|---|---|---|---|
| `diff.patch` đúng diff base `1f0941e9` → head được giao | `python3 measure_claims.py > measure_claims.log`; so với `git -C cay-kho diff 1f0941e9 HEAD` | Byte nội dung diff trùng; chỉ thêm bốn tệp spec r4–r7 (259/287/309/342 dòng thêm) | Khớp; trần 550 dòng của packet tính năng tương lai không áp vào diff soạn spec này |
| Base `1f0941e9` là merge PR #1186 | `git -C cay-kho show -s --format='%H %s' 1f0941e9` | `1f0941e9bba1d1d517eda4174167b81963c06bd5 Merge pull request #1186 ...` | Khớp |
| OID land ADR-0052/0053 là merge PR #791 | `git -C cay-kho show -s --format='%H %s' 8ab100793df9831505f495543a74044b91c2c9ab` | Đúng OID, `Merge pull request #791 ...` | Khớp |
| 9 mục tiêu → đúng 9 đường dẫn write set; mỗi mục tiêu có nghiệm thu | `python3 measure_claims.py` (tách mục tiêu/write set/cột mục tiêu trong bảng) | `goal_write_map_ok=true`, `acceptance_unmapped_goals=[]` | Khớp L2 về ánh xạ; chất lượng phép đo vẫn có F01 |
| Manifest có 184 tệp và chứa cả adapter, bundle, hai tài liệu doctrine | Cùng script, `json.load(RELEASE_MANIFEST.json)` | `file_count=184`, `len(files)=184`, bốn đường dẫn đều có | Khớp |
| `_run` là điểm chạy subprocess trong adapter; tuple trả về, rc 124/127 | `nl -ba cay-kho/scripts/nlm_cli.py` dòng 110–124 | `_run`, `subprocess.run`, ba trường trả về; timeout=124, FileNotFound=127 | Khớp; chưa có cơ chế nạp lại |
| Ba bộ chuỗi auth tại `nlm_cli.py:143/162/229` | `python3 measure_claims.py`, mục `line_anchors` | Cả ba là `auth,401,login,unauthor,credential` | Khớp |
| Bốn hằng auth phải giữ nguyên; `_AUTH_FIX_FALLBACK` ở dòng 297 | Đọc AST hằng trong `review_behavior.py`; neo dòng bằng `measure_claims.py` | Có đủ bốn hằng; fallback khai báo ở 297, dòng 296 là chú thích | Khớp lời khai hiệu lực r7/E14 |
| Điều cấm nằm ở RASOAT 118–119, QUY_TRINH 49 | Cùng script, đọc từng dòng thật | RASOAT có `CẤM tự` vắt dòng; QUY_TRINH có `**CẤM** tự` trong gạch Sửa xác thực | Khớp |
| `_nlm_auth_alive` ở 308–363; tối đa 3 probe × 30 s, backoff 1,5 + 3 s | `python3 review_behavior.py > review_behavior.log`; AST hàm nguồn + fake `nc._run`, thay sleep bằng hàm rỗng | Ba probe với timeout 30 ở lỗi retry; tổng hạn probe+sleep 94,5 s, nhỏ hơn timeout con 120 s được đặc tả chọn | Khớp (không giả nhận đã đo thời gian mạng thật) |
| A13 sáu ca, gồm chuỗi trộn | Cùng script, chạy hàm nguồn `_nlm_auth_alive` và `_nlm_canary_raw_get` | `None,None,False,False,False,None` | Khớp; không nêu lại quyết định “chỉ lần cuối quyết định” làm finding |
| Canary chuẩn `_canary_song`, `nlm-auto-refresh.sh:93–105`, mã 0/3/2 | Cùng script, lấy nguyên thân Python của shell, chạy bằng Python con với `tl.py` giả trong `fixtures/behavior/` | Sáu ca A13 ra `2,2,3,3,3,2`; stdout/stderr con rỗng; không dịch vụ | Khớp; hằng CANARY tương lai chưa tồn tại nên không khai đã chạy nó |
| `_nlm_preflight_report` gộp lỗi probe thành False ở 1424–1430 | Cùng script, AST hàm nguồn + đồ giả tuổi/rotation/NLM | Mạng, quyền, auth đều `alive=False`; 1425 là `bool(r.get("ok"))`, 1429 là nhánh exception | Khớp E6, đúng lý do r7 bỏ canary bằng status |
| `nlm-auth-load` tải nguồn sẵn có, giữ chống hạ cấp, không cần đường ghi remote mới | Đọc `tl_gws.py:1909–1967`, `:2024`; AST `_nlm_auth_load_downgrade` với tuổi tổng hợp trong RAM | Public download trước, fallback GAS action `download`; giải mã bằng token; ghi jar cục bộ; bản cũ hơn bị từ chối khi không force | Khớp; nhánh không đủ mốc thời gian giữ hành vi cũ, không đo credential thật |
| Chỉ stage sau canary dương; canary đòi thân notebook | Đọc `tl_gws.py:852–895,1970–2023`, `nlm-auto-refresh.sh:76–124`, fragment wp726 | Cổng trước đọc payload/upload, dùng `require_notebook_body=True`; wrapper xử mã stage và hỏi lại canary | Khớp mã; lịch laptop thực tế không quan sát từ sandbox |
| Fragment mẫu wp726=260 dòng, wp727=259 dòng; hợp đồng TEST_ID/run | `wc -l cay-kho/scripts/test_fragments/wp{726_script_nlm_canary,727_tl_gws_refresh}.py`; đọc đầu/cuối tệp | 260/259 dòng; có TEST_ID và `run(tl_module)` | Khớp |
| Bundle sinh bằng `generate_bundled_module_bytes`; CI có bundled-fragment check | Đọc `scripts/tl_core/test_fragments.py:464`, `.github/workflows/ci.yml:293–296`, `.github/checks/bundle_fragment_check.py` | Hàm tồn tại, mỗi source được JSON-encode một dòng; tên bước và lệnh khớp F3 | Khớp sự tồn tại/cách gọi; không chạy cả gate tính năng |
| r213 ở `tl_selftest.py:24829`, thêm ngoại lệ không cần sửa test | `review_behavior.py`: AST nguyên logic ca r213, import surfaces giả bằng các hằng nguồn; đọc hai tài liệu thật và hai fixture D1 | Base=True, fixture thêm câu=True | Khớp trong phạm vi ca r213; không thay thế full selftest |
| ADR status dùng `_ADR_TRANG_THAI` ở 1887; ADR-0060/0062 dòng 3 theo khuôn | `measure_claims.py`, đọc regex và dòng 3 của hai ADR | Regex có `re.M | re.I`; cả hai ADR bắt đầu `- **Trạng thái:** Accepted (...)` | Khớp; D3 r7 cố ý đòi chuỗi Accepted chính xác không hậu tố |
| Ô ADR-0060 ở protocol dòng 1517; số 0062 đã bị chiếm | Cùng script; `git -C cay-kho ls-tree -r --name-only HEAD docs/adr` | Dòng 1517 đúng ô backtick; có `0062-adr-0060-mac-dinh-va-dong-bang-adr-0054.md` | Khớp |
| Số ADR-0063 chưa có; baseline chưa có cơ chế | Cùng script, tìm symbol/đường dẫn | 0 `NAP_LAI/nap_lai` trong adapter; 0 `ADR-0063` trong protocol; 0 tệp `0063-*` | Khớp trạng thái “chưa làm” |
| Điều kiện không chiếm số ADR trên mọi ref | Cùng script, `for-each-ref` rồi `ls-tree` từng ref origin cục bộ | Cả 6 ref snapshot trong clone đều không có `docs/adr/0063-*`; không đo được tính đầy đủ so remote hiện tại | Khớp tập cục bộ; không coi là đã đo điều kiện cấp lease LIVE |
| Khuôn changelog wp1038 là một đoạn, có tiền tố packet | `cat cay-kho/changelog.d/wp-1038.md` | Một đoạn tiếng Anh, tiền tố WP1038 đúng khuôn được viện dẫn | Khớp |
| Năm tệp nền không đổi giữa `90c101b8` và `1f0941e9` | `git -C cay-kho diff --stat 90c101b8 1f0941e9 -- scripts/nlm_cli.py scripts/tl_gws.py scripts/tl_core/nlm_ops.py references/RASOAT_HOSO_LOOP.md references/QUY_TRINH_RA_SOAT_3_TANG.md` | Output rỗng | Khớp E10; từng neo dòng vẫn đã đo riêng |
| Errata thấp hơn được giữ nguyên qua revision | `measure_claims.py`, tách từng mục errata rồi so nguyên văn r2→…→r7 | 15 cặp mục lịch sử đều bằng nhau | Khớp; lời khai cũ đã được E7/E14 thay không bị tính lại là lỗi r7 |
| `_che_khong_render` đủ làm nền đo nội dung render; V đóng lớp lỗi | `python3 review_v.py > review_v.log`, chạy chính các node AST nguồn, fixture ngoài repo | D2/D3 nhận sai hai trạng thái qua code span; code thụt lề và mục thứ bảy lọt; có cả ĐỎ oan | **Lệch — F01** |
| D1/D3/H1 có đúng màu trên các ca tự khai | Cùng script; `review_summary.json` | 18 ca D1 + 13 ca D3 + 6 ca H1 = 37 ca tự khai đều đúng màu; toàn bộ suite 63 fixture | Khớp ca đã khai, chưa đủ đóng lớp; phản chứng mở rộng ở F01 |

Các phép đo đã chạy ở trên rc 0; D2 rc 9 trong các fixture âm là màu ĐỎ mong đợi (ngoại lệ ĐỎ oan nêu F01). `review_v.py` chép V2/V3 từ văn xuôi vì r7 không cung cấp hàm cho hai bước ấy; V1, regex và `cmd_adr_song` là hàm/hằng nguồn thật, compile AST để tránh side effect import. D2 chạy trên bản sao toàn bộ ADR + protocol với một dòng/tệp ADR-0063 mới, trong `fixtures/d2-root/`. Mỗi fixture D3 dùng đúng cùng nội dung cho D2.

Không có triển khai tương lai trong PR: A1–A12 của tính năng, F1/F3/J1/G1/K1/K2/L1, full selftest và lint/gate phát hành **not_run**; không coi là pass. G2 tồn tại là gate bất biến, nhưng không dùng việc chưa chạy nó làm bằng chứng xanh. M1, jar/bundle LIVE, log bootstrap lịch sử, lịch 30 phút trên laptop và trạng thái lease/GitHub hiện tại **chưa đo được** theo hạn chế offline. Mọi số lịch sử/ước tính được hiểu theo mốc ghi tại spec; không thay thành lời khai LIVE.

## ĐỐI CHIẾU LƯỢT TRƯỚC VÀ LỚP FINDING

Nguồn đối chiếu lượt liền trước: r7 §errata_r7 dẫn run `ca2338b5`, r6 head `c0c0f4d6`, 2 P2 tại D3. Không có toàn văn verdict/receipt lượt đó trong bundle được giao; không gọi GitHub để suy thêm nội dung. Bảng sau chỉ nhận diện hai biểu hiện r7 chép trong E21, và tự đo lại chúng:

| Finding trước | Nhãn đối chiếu | Bằng chứng tự đo trên r7 |
|---|---|---|
| F01 r6: Accepted + dòng Proposed vẫn qua D3 | **VÁ HỜ ở lớp**; biểu hiện thô đã đóng | `D3/extra_proposed.md`: D3=False, D2=0. Nhưng `status_between_inline_comment_examples.md`: Proposed vẫn render thành dòng trạng thái, D3=True, D2=0. Cơ chế đếm trên masking sai vẫn hở. |
| F02 r6: sáu câu chỉ nằm trong comment / sai mục / nối đoạn vẫn qua D3 | **VÁ HỜ ở lớp**; các fixture cũ đã đóng | `decisions_comment`, `wrong_section`, `split_paragraph`: D3=False. Nhưng `six_in_indented_code`, `wrong_section_after_setext`: D3=True, D2=0; chuẩn vị trí/loại khối vẫn chưa được đo đủ. |

Lớp duy nhất của lượt này: `thuoc-do-chuoi-khong-khop-markdown-nguon`, nối slug E17 r6 (nguồn từ review r5) và E19/E21 r7; finding hiện tại **F01, P2**. Các nhóm biểu hiện dùng cùng nguyên nhân: xem phép che/regex/collapse là cấu trúc Markdown, rồi bỏ qua những khối không khớp mẫu đang đếm. Một finding không có nghĩa chỉ có một fixture; bảng chi tiết ở dưới. Không đổi slug để reset lịch sử lớp. Hai quyết định chủ kho đã chấp nhận (canary xét lần cuối và race hai tiến trình) không tính finding.

## FINDINGS

### F01 — P2 — Thủ tục V vẫn có XANH giả và ĐỎ oan do không giữ cấu trúc Markdown

**Lớp:** `thuoc-do-chuoi-khong-khop-markdown-nguon`.

**Tệp:dòng:** `ops/specs/cloud-setup-p3b-nlm-401-r7.md:156–161` (V), `:181` (D1), `:183` (D3), `:184` (H1), `:327–329` (lời khai đóng cả lớp). Yêu cầu bị hụt ở `:132–147,150–151`: ngoại lệ đúng vị trí, ADR có sáu gạch quyết định riêng, changelog là đoạn văn.

**Mô tả và tác động.** V1 dùng đúng hàm nguồn được chỉ định nhưng hàm ấy chỉ xử lý fence ở cột 0–3 rồi tìm comment HTML trên chuỗi; nó không hiểu inline code hoặc code thụt lề. V3 xoá thông tin thụt lề, còn D3(b) chỉ *lọc lấy* các khối bắt đầu `- ` thay vì kiểm toàn bộ các item trong mục. Do vậy D3 có thể cho qua một ADR với hai trạng thái thật, một quyết định thứ bảy, hoặc sáu câu chỉ là ví dụ code. D1/H1 cũng có thể cho qua khối code thay cho chỉ dẫn/changelog thật. L3/L6 yêu cầu thước đo đổi màu theo nghĩa nội dung; các phản chứng này cho thấy chưa đạt. D2 rc 0 không cứu được: đã chạy chính cổng ấy trên cùng fixture và nó cũng xanh.

**Tái hiện.** Từ SANDBOX:

```sh
python3 review_v.py > review_v.log
python3 review_behavior.py > review_behavior.log
python3 measure_claims.py > measure_claims.log
```

Chi tiết từng nội dung đầu vào được giữ tại các đường dẫn sau; kết quả đầy đủ ở `review_v_results.json`. Đối chứng chuẩn `fixtures/D3/correct.md` thoả mục tiêu ADR và cho D3=True, D2 rc 0; `fixtures/H1/correct.md` là đoạn tiếng Anh mô tả đúng hành vi, cho H1=True.

| Biểu hiện / fixture tái hiện ngoài repo | Kết quả đã đo | Vì sao sai |
|---|---|---|
| `fixtures/D3/status_between_inline_comment_examples.md` | V1 không báo vấn đề; D3(a/b/c)=True; D2 rc 0, 62 ADR/62 dòng | Giữa Accepted và mục Quyết định có đoạn ví dụ inline-code mở comment, một dòng `- **Trạng thái:** Proposed` thật, rồi đoạn ví dụ inline-code đóng comment. Markdown không có HTML comment ở đây; V1 che nhầm nên không thấy trạng thái thứ hai. |
| `fixtures/D3/extra_asterisk_item.md`, `extra_plus_item.md`, `extra_numbered_item.md`, `extra_nested_asterisk.md` | D3=True; từng fixture D2 rc 0 | Thêm item `*`, `+`, `1.` hoặc `  *` sau sáu câu. V2 tách item nhưng D3 bỏ qua khi lọc `- `. Sáu câu cũ còn nguyên không chứng minh “không thêm mục”. |
| `fixtures/D3/six_in_indented_code.md` | D3=True; D2 rc 0 | Sáu dòng `    - <câu>` tách bằng dòng trống tạo một code block Markdown, không phải sáu mục quyết định. `_che_khong_render` không che, V3 xoá bốn dấu cách rồi biến chúng thành sáu khối `- ...`. |
| `fixtures/D3/wrong_section_after_setext.md` | D3=True; D2 rc 0 | Ngay sau `## Quyết định` là `Mục khác` + gạch Setext rồi mới có sáu câu: mục Quyết định rỗng, sáu câu thuộc H2 khác. Điểm cắt “# / ## kế tiếp” và V không xử lý heading Setext. |
| `fixtures/D1/rasoat_indented_target_block.md` | D1(a)=True, D1(b)=True | Chỉ chèn câu và đổi whitespace để khối §4b thành code thụt bốn dấu cách. Toàn bộ chữ được giữ nhưng khối doctrine render đã đổi loại; hai vế D1 đều không thấy. `quytrinh_indented_target_block.md` cũng cho True/True với thụt lề làm khối nằm lồng vào phần trước. |
| `fixtures/H1/indented_code.md` | H1=True | Thụt cả đoạn changelog bốn dấu cách: nội dung là code block, không còn là đoạn văn mục tiêu 8. V3 vẫn đưa về đúng prefix/token. |
| `fixtures/D3/valid_comment_with_fence.md`, `fixtures/H1/valid_closed_comment_fence.md` | D3/H1=False; ở ADR D2 rc 9 | Thêm comment HTML đã đóng với dòng ba backtick bên trong. Markdown hợp lệ, phần render đúng như đối chứng, nhưng hàm che fence trước comment báo cả “rào không đóng” và “comment không đóng”. |
| `fixtures/D3/valid_inline_comment_syntax.md`, `fixtures/H1/valid_inline_comment_syntax.md` | D3/H1=False; ở ADR D2 rc 9 | Thêm lời giải thích với ký hiệu mở comment trong inline code. H1 vẫn là một đoạn tiếng Anh đúng mục tiêu. Không có comment HTML thật, nhưng V1 báo comment không đóng. |

Phần làm trạng thái Proposed lọt trong fixture đầu, giữa các dòng trống:

```markdown
Cú pháp mở: `<!--`.

- **Trạng thái:** Proposed

Cú pháp đóng: `-->`.
```

Không cần payload tấn công đường dẫn hoặc credential để tái hiện. Ngoài các ca trong bảng, đã thử bảo toàn chữ cũ, nối/ngắt đoạn, dấu mục thay thế, danh sách lồng, Setext, ATX thụt lề/closing hashes, bảng, token có hậu tố, comment và fence. Tất cả fixture và kết quả còn trong SANDBOX. Các khuôn bị D3 cố ý giới hạn (ví dụ viết cả sáu mục bằng `*` thay `-`, hoặc viết heading chính có closing hashes) được ghi nhận là ĐỎ theo khuôn r7, không tự tính thành finding mới. Bảng trong mục Quyết định không mặc nhiên là sai; ca ấy chỉ là kiểm biên, không dùng làm bằng chứng finding.

**Đề xuất sửa — vá ở đâu và thế nào.** Ra revision mới, sửa V cùng D1/D3/H1 và mục errata tại chính spec; hướng rẻ nhất là chốt một khuôn đầu vào hẹp đủ cho các tài liệu này rồi kiểm *toàn bộ* cấu trúc khuôn, từ chối rõ cấu trúc ngoài khuôn trước khi collapse. Đừng gọi `_che_khong_render` là bằng chứng đầy đủ của Markdown render. D3 phải kiểm tất cả item, kể cả marker khác/cấp lồng, và ranh giới heading; D1 phải giữ loại/vị trí khối, H1 phải đòi đoạn văn. Với inline code/comment/fence, cần một phép tách theo đúng ngữ cảnh hoặc khuôn không cho phép mơ hồ ấy; chỉ đổi thứ tự che comment/fence sẽ mở chiều lỗi ngược lại. Hướng rộng hơn là dùng parser Markdown có kiểu node và phạm vi nguồn, nhưng nếu cần dependency/tệp mới ngoài write set thì phải khai lại trong revision, không giao Executor tự mở phạm vi. Không mặc nhiên sửa `packet_loop.py` vì ngoài write set hiện tại.

**Ca khoá và đột biến.** Giữ toàn bộ 37 ca tự khai làm hồi quy, thêm các fixture trong bảng thành ca riêng. Đột biến bỏ kiểm loại block, chỉ đếm marker `-`, bỏ nhận Setext, hoặc che comment trên inline-code phải bị ca tương ứng giết đúng tên/lý do; đối chứng ngắt dòng mềm vẫn XANH. Chạy D2 và D3 trên cùng ADR dương/âm, ghi riêng màu của từng cổng, không dùng tổng số pass làm bằng chứng đóng lớp.

**Rủi ro bản vá.** Siết khuôn có thể làm ĐỎ các đoạn xuống dòng hay Markdown hiện hữu đang hợp lệ, và sửa mask ở nguồn có thể đổi nghĩa D2 cho toàn kho. Cần công bố phạm vi cú pháp chấp nhận, giữ đối chứng cả hai tài liệu base, giữ khuôn dòng trạng thái mà D2 đọc, và không mở thêm đường ghi/credential hay reset lịch sử lớp.

## TỔNG

| Mức | Số finding |
|---|---:|
| P0 | 0 |
| P1 | 0 |
| P2 | 1 |
| P3 | 0 |

**1 finding / 1 lớp nguyên nhân còn mở; verdict `request_changes`.** Các ca r7 tự khai đã qua phép tái đo, nhưng các phản chứng thêm vẫn làm tài liệu sai XANH và tài liệu đúng ĐỎ. Chưa đủ điều kiện approve theo yêu cầu 0 finding của prompt.

Không truy cập mạng/Drive/NLM/webapp/GitHub; không đọc/ghi credential thật; không chạy `tl` lên dịch vụ. Chỉ dùng đọc file/Git cục bộ, AST hàm nguồn với đồ giả RAM, và Python con trong cây fixture. Không ghi vào `cay-kho/`.

### Danh tính cuối lượt

Đo cuối: 2026-11-04T16:48:11.184258+00:00

```text
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
bc1d5e048cc7889e6a759027059c5dd4735a4678
d72a43cefaad037904de9d3c4ac15c169cf96ce6
rc=0

$ git -C cay-kho status --porcelain=v1 --ignored
(output rỗng)
rc=0

$ git -C cay-kho diff --exit-code
(output rỗng)
rc=0

$ git -C cay-kho diff --cached --exit-code
(output rỗng)
rc=0

$ sha256sum cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r{1,2,3,4,5,6,7}.md
15fe242a65c8df1ff393cdc15784642013e904bacb9b754b0d72a64237dac11e  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r1.md
c6e53a00c7370ce0d75d9bcd954f8b7e69aa7383a0f5e6427a29e5e0d0e3ed8d  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r2.md
e2246e90aaf35b6b006b40a258e694a99c796a1ff1a8ac21aebb408121efa121  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r3.md
d28d00b5dbf6aac631f2aaac4282eb50ad1e59490d03acff095a64e45535430f  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r4.md
25473237f53684706112b5a2f8dfafce143000110a57c8d680f3b44f924e5ed5  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r5.md
b078da106387512cac956d8bc18d702bb50cfcf4bfd37101bb6c7aeb0686d201  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r6.md
887dc78a1f20d640f1b779b58fea7c963b2931e76e31abbe00ca13960d699061  cay-kho/ops/specs/cloud-setup-p3b-nlm-401-r7.md
```

HEAD/tree, tracked, untracked và ignored đều khớp đầu lượt; index/worktree không có diff, bảy băm spec không đổi. Snapshot chứng minh không có delta quan sát được ở hai mốc; không phải cơ chế cưỡng chế mount read-only hay bằng chứng về mọi thời điểm trung gian. Sandbox workspace-write cho phép ghi workspace, còn checkout được giữ chỉ đọc theo chỉ thị review.

