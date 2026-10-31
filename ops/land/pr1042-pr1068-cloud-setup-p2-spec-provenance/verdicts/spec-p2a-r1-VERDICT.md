verdict: request_changes
reviewed_sha: eb7242561f5dd99071991cbc38528bdb3cb1cf52
reviewed_tree: 726ad3571166cf11709882e3c0e974bfe6acf328

## (i) DANH TÍNH

Đúng cả ba neo: HEAD, tree và SHA-256 của CẢ HAI tệp. Reviewer: `openai_codex`, phiên công cụ có shell trực tiếp; review độc lập đặc tả S-A. Không review phần thi hành PR #1063.

Phép đo đầu tiên sau khi đọc prompt, rc 0:

```sh
git -C cay-kho rev-parse HEAD 'HEAD^{tree}'
```

```text
eb7242561f5dd99071991cbc38528bdb3cb1cf52
726ad3571166cf11709882e3c0e974bfe6acf328
```

```sh
sha256sum SPEC.md cay-kho/ops/specs/cloud-setup-p2a-exec-r1.md
```

```text
1071797a1cf2016a9266a98ccece02ed6edd4e80ca33d3b91b2547f7ca0c13e1  SPEC.md
1071797a1cf2016a9266a98ccece02ed6edd4e80ca33d3b91b2547f7ca0c13e1  cay-kho/ops/specs/cloud-setup-p2a-exec-r1.md
```

Lệnh hash rc 0. Đo lại bằng script ở cuối review vẫn cho đúng hai hash trên.

```sh
git -C cay-kho merge-base 757bde561d09738858506aecf5de2f050a5f0d5e HEAD
git -C cay-kho diff --numstat 757bde561d09738858506aecf5de2f050a5f0d5e eb7242561f5dd99071991cbc38528bdb3cb1cf52
```

```text
757bde561d09738858506aecf5de2f050a5f0d5e
203     0       ops/specs/cloud-setup-p2a-exec-r1.md
```

Hai lệnh đều rc 0. Diff các đường `scripts`, `.claude/hooks`, `references/golden`, `RELEASE_MANIFEST.json` giữa base và HEAD rỗng, rc 0. Vì vậy số đo mã tại HEAD cũng là số đo tại base được giao.

`git -C cay-kho status --porcelain=v1 --untracked-files=all` đầu/cuối không có output, rc 0. Không sửa `cay-kho/`. Cache, log, bản sao và mọi dữ liệu giả đều ở `review_evidence/`. Snapshot hai mốc chỉ chứng minh không có delta quan sát được; không phải bằng chứng giám sát mọi thao tác trung gian. Môi trường thực tế: workspace-write, kho được review được đối xử read-only.

## (ii) ĐO LẠI KHẲNG ĐỊNH CỦA ĐẶC TẢ

Dòng tham chiếu dưới đây là dòng của `SPEC.md`, đồng nhất với tệp đặc tả trong kho. Những mục định nghĩa hành vi MỚI là yêu cầu cho executor, không bị coi là khẳng định rằng tính năng đã tồn tại tại HEAD.

Các lệnh CLI được chạy trong clone local `review_evidence/tree`, checkout đúng SHA, `core.abbrev=7`, `-B`, HOME/TMP riêng và môi trường tối thiểu. Trước các lệnh có `tl`, đã chạy:

```sh
unset TL_MASTER_KEY TL_AGENT_CREDS_FILEID CLAUDE_CODE_OAUTH_TOKEN GEMINI_API_KEY
```

Runner không truyền các biến ấy cho tiến trình đo. Audit hook bổ sung chặn network, mở credential/config ngoài scratch và thực thi các CLI ngoài phạm vi. Không gọi mạng/Drive/NLM/webapp, không tải/chạy `agy`, không mở credential thật. Không tái hiện các thao tác LIVE.

Lệnh/script đo có thể chạy lại:

```sh
python -B review_evidence/measure_claims.py
unset TL_MASTER_KEY TL_AGENT_CREDS_FILEID CLAUDE_CODE_OAUTH_TOKEN GEMINI_API_KEY
python -B review_evidence/run_offline.py probe ../probe.py
```

Kết quả đầy đủ: [static_claims.json](review_evidence/static_claims.json), [probe.stdout](review_evidence/probe.stdout). `probe.py` chỉ thêm parser/metadata/guard vào bộ nhớ của bản sao, không cài đặt tính năng hay sửa tệp nguồn.

| khẳng định (mục/dòng) | đặc tả khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| D12, base đo gần đóng băng | `5e458f47`, merge #1044 | `git -C cay-kho show --stat --oneline 5e458f47`: merge #1044, chỉ hai tệp hồ sơ land | Có; đây là mốc đo lịch sử, không thay base review |
| D15–16, tiền lệ P1 | Merge `09e05945` chạm 13 tệp | `git -C cay-kho diff --numstat 09e05945^1 09e05945`: 13 tệp, 716 thêm/60 xoá | Có; không lấy 716 làm dự toán P2a |
| D19–22, land ADR | ADR-0052/0053 cùng land tại `8ab10079…` | `git -C cay-kho log --first-parent --format='%H %s' --diff-filter=A -- 'docs/adr/0052*' 'docs/adr/0053*'`: `8ab100793df9831505f495543a74044b91c2c9ab` | Có |
| D26–27, bundle ba khoá | `codex_auth`, `claude_oauth_token`, `antigravity_api_key`, dòng 1090 | AST `scripts/tl_gws.py` trong `measure_claims.py`: tuple đúng ba tên ở dòng 1090 | Có |
| D27–29, bootstrap | Chỉ ghi auth Codex; hai khoá còn lại chỉ báo tên | `nl -ba cay-kho/scripts/tl_gws.py`, 1217–1252: ghi ở 1245; chỉ liệt kê tên ở 1249–1251 | Có, trong nhánh agent-creds; spec cũng nêu bootstrap đầy đủ còn ghi config/gws |
| D28–29, hằng fileId | `AGENT_CREDS_FILEID` rỗng tại 1089 | AST nguồn: `AGENT_CREDS_FILEID = ""`, dòng 1089 | Có |
| D34–46, số tệp write_set | 13 tệp | `measure_claims.py`: `write_set_count=13`; fragment `wp-1038.md` là tệp mới dự kiến | Có về số lượng; hạn chế nội dung tệp test bị mâu thuẫn — F1 |
| D48–49, tệp cơ học P1 | P1 r4 chứng minh registry/golden/guard phải đi theo lệnh mới | `nl -ba cay-kho/ops/specs/cloud-setup-p1-bundle-r4.md`, 6–16, 55–67: đúng các lỗi/đường tương ứng | Có về nội dung tham chiếu; không truy vấn lại CI ngoài mạng |
| D50–51, ratchet | 198 lệnh lá/200 node | `workflow_audit` và `probe`: 198 leaf, 200 node; `command_registry_test.py` đạt 10/10 | Có |
| D50–51, guard test | Dòng 637–640 ghim `= 105` | `nl -ba cay-kho/.claude/hooks/pretooluse_guard_test.py`: đúng docstring 637 và biểu thức 640 | Có |
| D51, manifest | 193 tệp trên `757bde56` và `5e458f47` | `git show <OID>:RELEASE_MANIFEST.json`, parse JSON trong `measure_claims.py`: 193 trên cả hai và HEAD | Có |
| D52–56, lease #1030 | 11/13 rảnh, hai tệp bị giữ; r6 còn hạn; dự kiến 193→194, 1758→1759 | Kho được giao không có ref lease r6/receipt tương ứng; không fetch, không gọi `ai-dang-giu` qua mạng | Không tái đo được lịch sử này; spec đã yêu cầu đo lại lúc cấp lease (D203); không kết luận là đo sai |
| D80, thứ tự fileId P1 | Env > hằng | `nl -ba cay-kho/scripts/tl_gws.py`, 1220: `os.environ.get(...) or AGENT_CREDS_FILEID` | Có |
| D81, helper tải/giải mã sẵn có | `_public_curl_bytes`, giải mã RAM, đường đọc không kiểm mạnh khoá | Đọc nguồn 400–414, 647–648, 1217–1227; `gws_cred_store.decrypt` dòng 42–57 chỉ xử lý bytes/crypto RAM | Có; không thực sự tải hay giải mã credential |
| D86–87, bài học Windows | CLAUDE.md ghi `which`/PATHEXT/`codex.CMD` | `sed -n '728,735p' cay-kho/CLAUDE.md`: đúng bài học này | Có về dẫn chiếu kho; chưa đo Windows thật |
| D93/C2, lazy creds | `main` gọi load_creds trước handler nếu lệnh không lazy | `nl -ba cay-kho/scripts/tl.py`, 1315, 1335–1336: tập có `agent-creds-set`, chưa có lệnh mới; đúng nhánh gọi | Có; đây là lý do phải sửa tập lazy |
| D94–95/H1, registry | Theo khuôn set, `read_only=False`, thiếu gate có thể đỏ | `probe.py`: thêm parser không meta → `UNREGISTERED_PARSER_CMD:agent-creds-exec`; meta drive bỏ gate → `WRITE_CMD_NO_GATE:agent-creds-exec` | Có; cùng khuôn drive thực sự cần gate |
| D97–98, delta parser | 198→199 leaf, 200→201 node | `probe.py`: sau thêm đúng một parser/meta, 199 leaf/201 node | Có |
| D99/H2, tái sinh parser snapshot | `TL_WRITE_PARSER_SURFACE=1 … --selftest` | Đọc `tl_selftest.py:6600–6659`: biến đó điều khiển ghi snapshot; ca tên đúng `r77a_parser_surface_matches_snapshot` | Có về cơ chế; không ghi snapshot kho gốc |
| D101–103/H4, ghi golden | `golden-test --write` tái sinh hai golden liên quan | Đọc `workflow.py:1509–1510,1691–1806`: case và chế độ write đúng; baseline `golden-test --json` rc 0, 20/20 | Có về lệnh/cơ chế; diff sau thêm lệnh thực tế phải do executor đo |
| D104/H5, guard cần tên mới | Lệnh mới phải thuộc `_TL_LENH_GHI` | `probe.py`: lệnh Bash thông thường với tên mới trước thêm trả `None`; sau thêm tên trả lý do deny | Có; không dựng chuỗi vượt guard |
| D106–107, deny list có liệt kê set không | Nếu có thì phải thêm ca lệnh mới | AST/`nl -ba` test: t50 dòng 877 LIỆT KÊ `agent-creds-set --new` | Có; điều kiện đúng và làm lộ F1 |
| D106, guard 105→106 | Dự kiến 106 writer sau thêm lệnh | `probe.py`: 105→106; `--kiem-bang` thật trên head: 98 top + 7 long = 105, rc 0 | Có |
| D111, cần tái sinh manifest | Các tệp runtime/golden thay đổi nằm trong manifest | `probe.py` membership: 8 đường write_set có trong manifest; guard, test registry, fragment và manifest tự nó không nằm trong danh sách | Có; không cần thêm đường ghi ngoài 13 tệp đã liệt kê cho việc này |
| D117–118, prefix test | Số literal r lớn nhất 999, r1000 còn trống | AST `measure_claims.py`: max literal 999 là fixture giả `r999_ten_ma_khong_ton_tai`; không có literal ca `r1000_*` | Có; số 999 không phải bằng chứng tồn tại một ca runtime thật mang prefix ấy |
| C1/D134, vế âm | Base chưa có parser mới | Runner `missing_command`: rc 2, invalid choice; base→head không đổi mã nguồn | Có |
| C2/D135, config candidates | cwd, gốc skill, scripts, HOME, `/tmp/tra_luat_config.json` | `profile_env.py:60–73`; probe khử trùng còn 6 path khi cwd=gốc skill, tất cả `exists=false` | Có; khoảng dòng trích 58–69 bao phủ các dòng tạo candidates chính |
| G1/D141, số nền lịch sử | 1758/1758 trên `09e05945`, run 41017062295; base đo lại khi cấp lease | Không có log/run receipt đủ để xác nhận lượt lịch sử này; không chạy full selftest lần này | `not_measured`; spec khai rõ cần đo lại nền, không quy là số sai |
| J1/D142, output verifier | `ok=true`, `expected == checked` | Runner `release_verify`: rc 0, `ok=true`, `expected_file_count=checked_file_count=193`; không có key `expected`/`checked` | Lệch tên trường/alias chưa định nghĩa — F2 |
| K2/D144, kích thước packet | Trần 13 tệp/450 dòng so merge-base | Trần là lựa chọn đã khai, không phải số thực đo; diff đặc tả hiện tại chỉ 1 tệp/203 thêm. Không có `origin/master` trong bundle | Đo packet thi hành tương lai: `not_run`, không đánh đồng với diff đặc tả |
| L1/D145, ma trận CI | Ubuntu PR; Windows dispatch windows-only, theo YAML khi lệch P1 | Parse `.github/workflows/ci.yml`: Windows chọn đúng OS; cong-cu Windows chỉ shard 0; không có job gộp cong-cu Windows; nhanh có 8 shard mỗi OS | Có; P1 r4 có tên lịch sử `thu-hoi` không có trong YAML hiện tại, áp điều khoản đọc lại/theo ci.yml |
| D153–156, dự toán khoảng 300 dòng | ƯỚC TÍNH, CHƯA ĐO | Spec tự gắn nhãn dự toán; chỉ số thực sẽ đo K2 | Không coi ước tính là khẳng định đã đo |
| D162–163, secrets-set không xoay master key | Giải mã/mã hoá bundle cùng một khoá | AST `_secrets_set_body`: giải mã bundle bằng `master` (1013), mã hoá lại bundle bằng `master` (1053) | Có; không thực thi lệnh ghi secret |
| D166–170, set chỉ in id | Tạo mới in fileId, chưa tự lưu hằng | Đọc `tl_gws.py:1182–1214`: upload nhận id; print ở 1211/1213; không gán lại hằng hoặc lưu env | Có về hành vi mã; không gọi upload |
| D160–187, kết quả LIVE/laptop/session | Các thao tác, kích thước, băm rút gọn, HTTP 200 và bootstrap thành công | Nguồn ngoại vi/laptop không có trong bundle để tái đo; user cấm LIVE và credential thật | `not_measured`; không nhận các lời khai ấy làm phép đo độc lập |
| D197 so D91–92/133/185 | FileId còn ở mục `chua_do_duoc` | `nl -ba SPEC.md`: ID đã được ghi đầy đủ ở mục tiêu/B1 và bước LIVE 5 có kết quả | Mâu thuẫn trạng thái nội bộ — F3 |

## (ii) TIÊU CHÍ NGHIỆM THU

Đánh giá dưới đây là **khả năng đo và phản chứng của hợp đồng**, không tuyên bố các ca tính năng mới đã chạy/đạt. HEAD đang review chỉ thêm đặc tả; tính năng chưa có tại HEAD này. `not_run` không phải pass. Với đột biến chưa chạy, bảng ghi đó là phân tích thiết kế test.

| tiêu chí | đo được không / cách quan sát | đột biến làm đổi màu; trạng thái đo |
|---|---|---|
| A1 | Có: gọi handler in-process trong env cô lập, đo băm hai giá trị tại con và so môi trường tiến trình tl trước/sau | Đổi sang gán env tiến trình tl: vế sau lệnh đỏ. Phân tích, chưa chạy ca mới |
| A2 | Có: hai lần, mỗi lần một cờ, ban đầu không có cả hai biến | Luôn đặt cả hai: kiểm biến không yêu cầu đỏ. Phân tích |
| A3 | Có: từng nhánh lỗi có bộ đếm con riêng, đòi rc 4 và đếm 0 | Cho nhánh thiếu/rỗng khoá chạy con: bộ đếm đỏ. “Năm” là năm nhóm, nhóm thiếu/rỗng phải đo cả hai mẫu. Phân tích |
| A4 | Có: hai con thoát 0 và 7, so rc wrapper | Wrapper luôn trả 0: trường hợp 7 đỏ. Phân tích |
| A5 | Có trong phạm vi output do wrapper tạo: stdout/stderr thu riêng từng nhánh, mỗi sentinel kiểm riêng; con mẫu chỉ in băm | Chèn in giá trị ở nhánh lỗi: kiểm sentinel đỏ. Cần thử từng nhánh đã liệt kê, không chỉ tổng suite. Phân tích |
| A6 | Có: từng lỗi đối số kiểm rc 2 và downloader giữ trạng thái đếm 0 | Bỏ kiểm thiếu lệnh: lỗi rc hoặc số lần tải đổi màu. Phân tích |
| A7 | Có: con nhận đối số có ký tự đặc biệt nguyên văn, so argv thực tế | Cho shell diễn giải: argv/kết quả con khác. Không dựng payload vượt guard trong review; chưa đo Windows thật |
| A8 | Có: which giả đếm, trường hợp không resolve kiểm rc 127/con 0 | Bỏ which: đếm 0, đỏ. Phân tích; đây chưa chứng minh shim Windows thật chạy được |
| A9 | Có: downloader giả ghi id nhận được, env và hằng cố tình khác nhau | Đảo ưu tiên: id nhận khác kỳ vọng. Phân tích |
| A10 | Có: hai gọi hợp lệ dùng chung downloader giữ trạng thái | Dùng cache: lần tải thứ hai mất, số đếm 1 thay 2. Phân tích |
| A11 | Có trong phạm vi API ghi đã liệt kê: bọc đếm trong khoảng gọi handler, làm fixture trước; con giả, HOME/cwd/TMP riêng; quét sentinel sau | Ghi tệp tạm rồi xoá vẫn làm bộ đếm tăng; ghi bản mã vào cwd cũng tăng. Không đánh đồng quét cuối lượt với bằng chứng không từng ghi. Phân tích, không tạo tệp credential thật |
| B1 | Có: đọc hằng trong nguồn/AST và so ID chính xác; base rỗng là đối chứng âm | Để hằng rỗng: đỏ. Đã đo vế âm tại HEAD/base; không xác nhận nội dung bundle thật |
| C1 | Có: rc/help của parser mới; base chưa có lệnh | Xoá add_parser: CLI rc 2, mất flags. Đã chạy vế âm trên HEAD: rc 2 |
| C2 | Có: (a) mock load_creds đúng namespace tl, đếm 0/rc 4; (b) kiểm không tồn tại TẤT CẢ config candidates trước CLI thật | Bỏ khỏi lazy: mock bị gọi, đỏ bất kể cấu hình máy. Đã đo nguồn main và candidates (đều vắng); chưa có lệnh để chạy hai vế feature. Máy có config cố định thì theo spec phải đỏ, không được skip |
| H1 | Có: parse registry issues và rc workflow audit | Parser mới thiếu metadata: đã đo `UNREGISTERED_PARSER_CMD:agent-creds-exec`; meta drive bỏ gate cũng đỏ. Baseline audit rc 0/issues rỗng |
| H2 | Có: snapshot theo command, kiểm r77a không đặt biến ghi và xem diff JSON | Thêm parser rồi dùng snapshot cũ: key mới thiếu, đỏ. Đã đọc cơ chế r77a và snapshot base; chưa chạy mutation feature |
| H3 | Có: unit test ratchet số parser | Thêm một parser/meta nhưng giữ ratchet 198/200: assertions số đếm đỏ. Baseline unit suite 10/10; probe đo 199/201 sau thêm |
| H4 | Có: golden verification và determinism audit | Khôi phục một trong HAI golden ĐÃ ĐỔI về base: diff kiểm kê đỏ. Baseline golden rc 0/20 ca; determinism/full mutation feature `not_run` |
| H5 | Có, nhưng phạm vi chỉnh test mâu thuẫn F1 | Gỡ tên mới khỏi set guard: probe lệnh thông thường chuyển deny sang allow. Đã đo hai phía trong bộ nhớ; `--kiem-bang` baseline rc 0/105 writer. Full guard-test và ca feature `not_run` |
| G1 | Có theo DELTA từng test ID trên cùng nền/base, mọi ca mới bắt buộc đạt; ghim core.abbrev=7 | Một ca mới đỏ hoặc ca xanh trên base chuyển đỏ trên head: đỏ. Full selftest Ubuntu/Windows `not_run`; không xác nhận 1758/1758 lịch sử |
| J1 | Có sau khi làm rõ tên trường đếm — F2 | Đã đổi 1 ký tự SHA của `.gitattributes` trong bản manifest giả: rc 0→2, ok true→false, báo hash mismatch. Count thực 193/193; không có key viết tắt trong tiêu chí |
| K1 | Có: cùng phiên bản Ruff, rules F và đúng tập tệp Python; so delta baseline | Thêm tên chưa định nghĩa: số lỗi tăng. Bare Ruff trên write_set `not_run`; lần kiểm help của guard không được gọi là lint đã pass |
| K2 | Có khi có ref base/merge-base cần thiết: tổng số hàng numstat và tổng cột added; đếm cả tệp mới đã được Git ghi nhận | Vượt 13 tệp hoặc 450 thêm: đỏ. Packet thi hành chưa được review ở đây; bản giao thiếu origin/master, không fetch. Không gắn nhãn pass cho K2 feature |
| L1 | Có qua run/job API, exact SHA và ma trận YAML tại lúc nghiệm thu; có ngoại lệ cụ thể đã dẫn P1 | Context bắt buộc failed/skipped/vắng ngoài ngoại lệ: đỏ. Chỉ đã đo cấu trúc YAML offline; chưa đo CI thực tế và không dispatch |
| M1 | Có theo phép đo LIVE sau land: con so băm kỳ vọng, đối chứng môi trường đã xoá biến cho băm rỗng | Không chèn biến: vế (i) thành băm rỗng như (ii). `not_run` theo lệnh cấm LIVE/credential của user; đây là giới hạn đã khai, không phải finding |

Các giới hạn agy thực, Claude thật, Windows Ctrl-C, kích thước thi hành và nền/lease cần đo lại ở D198–203 được giữ đúng là chưa đo; không tính thành finding. Riêng D197 tự mâu thuẫn với trạng thái đã ghi ngay trong đặc tả, nên tách F3.

Bằng chứng cổng đã chạy (mọi đường dưới đây tương đối sandbox):

| lệnh qua runner | rc thật | kết quả | log |
|---|---:|---|---|
| `registry_test scripts/tl_core/command_registry_test.py` | 0 | 10/10 | `review_evidence/registry_test.stderr` |
| `workflow_audit scripts/tl.py workflow-audit --strict --json` | 0 | ok true, issues rỗng, 198/200 | `review_evidence/workflow_audit.stdout` |
| `golden scripts/tl.py golden-test --json` | 0 | ok true, 20/20 | `review_evidence/golden.stdout` |
| `release_verify scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | ok true, 193/193 | `review_evidence/release_verify.stdout` |
| `release_mutated scripts/tl.py release-verify ../manifest_mutated.json --strict --json` | 2 | **failed có chủ đích**, hash mismatch | `review_evidence/release_mutated.stdout` |
| `probe ../probe.py` | 0 | phép đo parser/metadata/guard trong bộ nhớ hoàn tất | `review_evidence/probe.stdout` |
| `missing_command scripts/tl.py agent-creds-exec --help` | 2 | **đối chứng âm**, parser chưa tồn tại | `review_evidence/missing_command.stderr` |
| `guard_table .claude/hooks/pretooluse_guard.py --kiem-bang` | 4 | lần đầu PATH tối thiểu bỏ sót Ruff; lỗi môi trường runner | `review_evidence/guard_table.stderr` |
| `guard_table_with_ruff .claude/hooks/pretooluse_guard.py --kiem-bang` | 0 | sửa PATH runner để thấy Ruff có sẵn, 105 writer; 26/26 chương trình có help; còn cờ advisory không đo được | `review_evidence/guard_table_with_ruff.stdout` |

Mỗi dòng chạy theo mẫu `python -B review_evidence/run_offline.py <các đối số trong cột lệnh>`, sau `unset` nêu trên. Runner lưu command/cwd, stdout, stderr, rc riêng. Không cài tải công cụ để làm xanh. Không ghi nhận một lần lint Ruff hay Windows test nào chưa thực sự chạy.

## (iii) KẾT LUẬN

`request_changes`: danh tính hợp lệ, còn **3 finding thuộc 3 lớp: 1 P1, 0 P2, 2 P3**. Không phát hiện P0 trong phạm vi review đã đo. Ngưỡng của prompt là không còn P0–P3 mới approve; không chuyển các finding thành nợ để approve.

Đặc tả đóng băng giữ nguyên. Các gợi ý dưới đây chỉ là dữ liệu để chủ kho quyết có ra revision 2; không phải quyền cho executor tự mở rộng write_set hoặc sửa spec hiện tại.

### guard-test-write-set-mau-thuan [P1] F1 — Write set cấm phần chỉnh test mà mục tiêu 10 bắt buộc

MỤC/DÒNG: `write_set` D43; `muc_tieu` D106–107; H5 D140. Nguồn kiểm: `.claude/hooks/pretooluse_guard_test.py:868–883`, đặc biệt D877.

VẤN ĐỀ: D43 chỉ cho sửa số đếm ghim `= 105`. D106–107 lại bắt buộc thêm ca `agent-creds-exec` cạnh `agent-creds-set --new` nếu test liệt kê lệnh. Điều kiện này ĐÚNG tại HEAD: ca t50 có danh sách lệnh viết tường minh. Chỉ sửa số 105 thì thiếu yêu cầu mục tiêu 10; thêm phần tử test thì vượt giới hạn “chỉ sửa số đếm” của write_set. Không có điều khoản xác định mục tiêu 10 thay thế hạn chế D43. Đây là mâu thuẫn phạm vi thi hành, không phải thiếu tên tệp.

ĐÃ ĐO:

```sh
nl -ba cay-kho/.claude/hooks/pretooluse_guard_test.py | sed -n '868,883p'
python -B review_evidence/measure_claims.py
```

```text
877: for lenh, mong in (("agent-creds-set --new", "deny"), ("secrets-set --gws", "deny"),
878:                    ("secrets-keygen", "allow")):
guard_explicit_list.agent_creds_set_listed = true
```

Hai lệnh rc 0. Probe độc lập cũng đo được tên lệnh mới cần thêm vào guard để chuyển allow→deny; không phải ca test thừa không liên quan mục tiêu.

ĐỘ TIN: cao.

Gợi ý cho revision do chủ kho quyết:

- Vá ở đâu: chỉ thị phạm vi test guard ở D43, đối chiếu D106–107.
- Vá thế nào: cho phép tường minh thêm fixture deny của lệnh mới và cập nhật số liệu mô tả phát sinh; giữ nguyên logic guard/logic test ngoài phần ấy.
- Ca khoá: trên bản sao, liệt kê diff t50 và kiểm mọi hunk cần cho mục tiêu 10 đều thuộc phạm vi mới; ca deny phải đỏ khi gỡ tên khỏi guard.
- Tác động cần canh: tránh mở quyền chỉnh tuỳ ý các test bảo vệ khác; tổng file/dòng vẫn chịu K2. Không sửa tệp review hiện tại.

### j1-ten-truong-dem-khong-khop [P3] F2 — J1 dùng hai tên đếm không có trong JSON trả về

MỤC/DÒNG: J1 D142; nguồn `scripts/tl_core/release.py:935–936`.

VẤN ĐỀ: J1 viết `expected == checked` nhưng chưa định nghĩa hai alias đó. JSON thực trả `expected_file_count` và `checked_file_count`. Có thể suy ra ý định bằng cách đọc output, nên xếp P3; điều kiện nghiệm thu nên ghi đúng tên trường để phép đọc máy không phải tự chọn cách ánh xạ. Vế `ok=true` và mutation hash của J1 vẫn có tác dụng; không kết luận toàn bộ verifier là cổng xanh giả.

ĐÃ ĐO:

```sh
unset TL_MASTER_KEY TL_AGENT_CREDS_FILEID CLAUDE_CODE_OAUTH_TOKEN GEMINI_API_KEY
python -B review_evidence/run_offline.py release_verify scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
```

```text
rc=0
ok=true
expected_file_count=193
checked_file_count=193
"expected" in output = false
"checked" in output = false
```

Nguồn trả đúng hai trường có hậu tố `_file_count`; log đầy đủ ở `review_evidence/release_verify.stdout`. Manifest giả đổi một ký tự hash cho rc 2/ok false, chứng minh phần verify nội dung có đổi màu.

ĐỘ TIN: cao về schema thực đo; lỗi chỉ ở cách ghi tên/alias của tiêu chí.

Gợi ý cho revision do chủ kho quyết:

- Vá ở đâu: biểu thức đếm J1.
- Vá thế nào: dùng `expected_file_count == checked_file_count`, hoặc định nghĩa alias tường minh ngay đó.
- Ca khoá: assertion hai key thực tồn tại trước khi so; verifier baseline phải báo 193/193, bản manifest giả sai hash phải fail.
- Tác động cần canh: giữ đòi hỏi rc 0 và `ok=true`, không thay chúng bằng phép so số đếm đơn lẻ.

### chua-do-duoc-fileid-da-co [P3] F3 — Trạng thái fileId chưa đo được không được cập nhật sau LIVE 5

MỤC/DÒNG: `chua_do_duoc` D195–197, đối chiếu trạng thái đóng băng D3–5, mục tiêu D91–92, B1 D133, kết quả LIVE D185–187.

VẤN ĐỀ: fileId vẫn được liệt kê dưới `chua_do_duoc` với chú thích “có sau bước LIVE 5”, trong khi chính đặc tả ghi LIVE 5 đã hoàn tất và điền cùng ID đầy đủ vào mục tiêu/B1/kết quả. Đây là lỗi trạng thái nội bộ sau đóng băng. Không phải finding về tính đúng của credential/bundle bên ngoài, và không đòi reviewer gọi LIVE để xác nhận.

ĐÃ ĐO:

```sh
nl -ba SPEC.md | sed -n '91,92p;133p;185,187p;195,199p'
```

```text
D91–92: mục tiêu đã cho ID chính xác 1I0-p-FKSy3255OUNv7xkhRACy3k1zqWQ
D133: B1 bắt buộc đúng cùng ID
D185: LIVE 5 đã trả ID đó, rev=1, 4725 B
D195–197: vẫn đặt fileId vào mục chua_do_duoc
```

Lệnh rc 0. Các dòng cùng nằm trong hai tệp có SHA-256 đã xác minh ở phần (i).

ĐỘ TIN: cao về lệch trạng thái văn bản; không tuyên bố đã đo lại fileId/bundle trên Drive.

Gợi ý cho revision do chủ kho quyết:

- Vá ở đâu: item fileId trong `chua_do_duoc`.
- Vá thế nào: ghi đã đo ở LIVE 5 hoặc chuyển sang kết quả đã đo, giữ nguyên provenance và ID của B1.
- Ca khoá: đối chiếu danh sách chưa đo với phần LIVE hoàn tất và mục tiêu/B1, không cần mở credential.
- Tác động cần canh: giữ nguyên các giới hạn thực agy, Claude, Windows Ctrl-C, nền và lease cần đo lại; cập nhật trạng thái fileId không được biến chúng thành pass.

Nhật ký đã ghi sớm và cập nhật qua sáu nhóm phép đo được lưu tại [VERDICT.progress.md](review_evidence/VERDICT.progress.md). Bản này là verdict cuối thay cho trạng thái pending. Mọi đề xuất sửa chỉ được ghi lại.
