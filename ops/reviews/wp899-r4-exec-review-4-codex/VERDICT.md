verdict: changes_requested
reviewed_sha: 75d0f6b5fe01611dda0b8768e50f5826657135e7
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 75d0f6b5fe01611dda0b8768e50f5826657135e7
reviewed_tree: d07a624425fff37d998ff0369345537b263ec3c1
packet: wp899-r4
review_round: 4
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a171ad-5e4e-7f01-bd04-5e65557baf40
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**P0=0, P1=1, P2=0, P3=0, đếm theo lớp. F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` LẶP; chưa đủ V2.** Các biểu hiện đã chỉ ở lượt 3 được vá thật: c46/c47 có răng trên các đột biến cũ. Tuy nhiên, **17 đột biến mới sống toàn bộ 47/47 ca** ở các chốt nguyên văn/miền/vị trí còn lại của M4/M12. Với từng mutant sống, reviewer chạy ca độc lập trên HEAD rc0 rồi trên bản sao mutant rc3, dòng `DO:<đúng tên ca>:` từ `TinHieuChotCa`. Không lấy lỗi setup hoặc chỉ rc khác 0 làm GIET. Không khẳng định sản phẩm hiện có lỗi mà chỉ mutant mới có.

Ví dụ: bỏ `re.escape(x)` trong ghép job, chuẩn hoá hoa thường khi ghép job, hoặc `strip()` tên bước tường minh đều không làm 47 ca đỏ. Ca riêng dùng alias `Build (release)`, REST `J` so với khoá `j`, hoặc tên bước ` Kiem tra ` phân biệt được HEAD và mutant. Ví dụ downstream: thay `run.rstrip("\n")` bằng `run.strip("\n")` vẫn qua suite; workflow có dòng đầu rỗng, còn khối log bỏ dòng ấy, phải không được xác thực. Ca c37 hiện chỉ đòi ghép ở biến thể này, chưa đòi kết quả marker.

**Authority, preflight và môi trường.** Nguồn review là assignment `.review-input/prompt.md` được user giao trực tiếp; spec r4 đã đọc trọn, 23.860 byte, SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`. Các hash r3 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`, r2 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` khớp; đã đọc các mục kế thừa và lịch sử verdict F01–F11. Áp skill `.agents/skills/cross-review/SKILL.md`, đối chiếu protocol §7/§8/§8.1–§8.3/§10.2.1–§10.2.3/§13 và quy tắc phát triển. Catalog không có `environment_status`; không suy khả năng mạng/credential từ việc thiếu công cụ đó.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD đúng SHA/tree đầu verdict; parent `27997a73c6b01e577ed655ea94e73d56adf697da`. Immutable acceptance baseline là `ba222ffd1615f0d74b59985b9612f725211b62f5` (ancestor rc0), điểm xuất phát `fe7522eb104daf93d0a8a5f37f0ee774e62a7846`; parent chỉ là delta lượt 4, không dời baseline. Diff có đúng ba tệp: registry +1, công cụ +444, test +946 = **1391 dòng thêm**. Registry chỉ thêm một mục MOI. `git diff --check <base> HEAD` rc0; `core.abbrev=7` có sẵn, không sửa Git config. `preflight.json`, `full.patch`, `delta.patch`, `setup.stdout.txt` giữ số đo/lệnh/rc. Clone shallow, không đủ mọi object/ref lịch sử.

Giữ Q1–Q12 và `gioi_han_khai`: workflow/script/action tại SHA checkout, gồm action pin tag, là gốc tin. Không coi thay nội dung gốc tin để quyết định output là một đường tấn công ngoài giới hạn ấy. Theo authority mới trong assignment (checkpoint issuecomment-6393643859), chủ kho đã nâng trần và cho tiếp tục tới hết P1/P2; **không coi 1391>1250 hay V5 cũ là finding/stop condition của lượt này**. Lời gọi này là **4/8** theo assignment. Việc đã đẩy nhánh lưu trữ, generation/lease/state GitHub hiện hành, chi thực tế và remote fence **KHÔNG ĐO ĐƯỢC offline**; không suy chúng từ tên archive. Không dùng review này để tự chuyển state, push, merge hoặc land.

Linux x86_64, Python 3.13.17, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15, codex-cli 0.164.0. Runtime metadata của đúng thread ở `/root/.codex/sessions/2026/10/25/rollout-2026-10-25T06-09-10-01a171ad-5e4e-7f01-bd04-5e65557baf40.jsonl` công bố model/effort như trên, originator `codex_exec`; `runtime.json` giữ phần metadata đã đọc. Model phục vụ từng request và receipt launcher/rollout sau khi writer kết thúc **KHÔNG ĐO ĐƯỢC trong lượt đang chạy**. Executor Claude/cloud theo assignment; không suy model Executor từ tài khoản vận chuyển. Sandbox workspace-write, `.git` read-only, network false, approval never; reviewer giữ candidate read-only bằng hành vi và snapshot. Mọi output/cache/temp do phép đo này tạo đều trong `.review/`; không gọi subagent, GitHub, push hoặc LIVE. Không tự soạn payload tấn công nhạy cảm; dữ liệu mới là tên/khoảng trắng/metadata và biến thể hợp đồng thuần offline.

**BẢNG LỚP — cùng F10, bốn nhóm biểu hiện mới, 17 mutant.** Số lớp mới=0. Các chốt mã sản phẩm được nêu dưới đây đang cho kết quả đúng trên baseline; phần cần vá là bằng chứng test/đột biến. Chỉ tăng số mutant mà không đặt fixture phân biệt được chốt chưa đóng lớp.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F10 — LẶP: tên nguyên văn | P1 | `ops/ci_provenance_test.py:568`, `:659`: alias chỉ `Build`, thiếu metachar/khoảng trắng/hoa thường; `:537` thiếu tên bước có khoảng trắng biên. Chốt tại `ops/ci_provenance.py:167`, `:172`. | `job_escape_alias`, `job_alias_strip`, `job_casefold`, `name_explicit_strip`: mỗi mutant SONG_SOT 47/47. `boundary_cases.py <tên>`: HEAD0 → mutant3 đúng ca, 4/4. | **Ở đâu:** c37/c39/c47 + DOT_BIEN vì cần đo nguyên văn cả tên job lẫn tên bước. **Cách:** tham số hoá alias có dấu ngoặc, alias có khoảng trắng giữ nguyên, job khác hoa thường phải không ghép, tên bước giữ khoảng trắng. **Khoá:** bốn mutant trên phải chết đúng ca; các đối chứng downstream phải đòi cả ghép và marker. **Rủi ro:** dùng tên khoá job không hợp lệ để thử regex hoặc strip fixture sẽ làm mất phép đo; dùng alias `name:` hợp lệ như ca reviewer. | ~10–16, test+mutant |
| F10 — LẶP: miền metadata/bước đã chạy | P1 | `ops/ci_provenance_test.py:568`, `:662` chỉ thử `Post `; `:537` thử failure nhưng chưa neutral/cancelled của bước. Chốt tại `ops/ci_provenance.py:196`, `:198`. | `metadata_setup_prefix`, `metadata_complete_prefix`, `ran_neutral_excluded`, `ran_cancelled_excluded`: SONG_SOT 47/47, 4 ca riêng HEAD0 → mutant3 đúng tên. | **Ở đâu:** ca ghép c37/c47, sau helper dựng state. **Cách:** tên bước hợp lệ `Set up job results`/`Complete job results` không phải tên metadata nguyên văn; chỉ bỏ skipped, vẫn giữ kết luận neutral/cancelled trong miền M12 đã định nghĩa. **Khoá:** bốn mutant phải GIET bằng khẳng định ghép/marker mong đợi, không chết do đếm fixture sai. **Rủi ro:** đánh đồng outcome job với conclusion của bước, hoặc tự thêm luật chỉ giữ success ngoài spec. Không khai các trạng thái này đã đo LIVE. | ~10–16, test+mutant |
| F10 — LẶP: miền chế độ và vị trí bước trước | P1 | `ops/ci_provenance_test.py:639`: thiếu khoá prefix có hậu tố rỗng/khác hoa thường, env bước rỗng, shell có khoảng trắng/khác hoa thường; `:610` chưa run nhắc ENV đứng trước nhưng skipped. Chốt `ops/ci_provenance.py:154`, `:214`, `:215`, `:216`. | `env_prefix_empty_suffix`, `env_prefix_casefold`, `mode_step_key_truthy`, `mode_shell_strip`, `mode_shell_casefold`, `mode_prior_requires_ran`: SONG_SOT 47/47; 6/6 ca HEAD0 → mutant3. | **Ở đâu:** c46 và c42/c45 vì đây là miền/định vị của luật chặn đã có. **Cách:** cô lập từng biến thể; prefix đúng `CI_DANG_KY_` vẫn chặn, prefix khác hoa thường không bị tự chuẩn hoá; khoá env bước có mặt dù dict rỗng vẫn ngoài allowlist; shell ngoài ba chuỗi vẫn chặn; Q7 quét run đứng trước, không tự thêm điều kiện bước ấy đã chạy. **Khoá:** sáu mutant trên GIET, kiểm đúng lý do chế độ và ghép passed trước đó. **Rủi ro:** một chốt khác che chốt đang thử; đừng đổi fixture nhiều trục hoặc đánh giá biểu thức `if` ngoài scope. | ~14–22, test+mutant |
| F10 — LẶP: nguyên văn/biên của khối | P1 | `ops/ci_provenance_test.py:537` chỉ đo ghép ở run dòng đầu rỗng; c35/c47 chưa cô lập khoảng trắng đầu header/shell. Chốt tại `ops/ci_provenance.py:271`, `:274`, `:295`. | `run_compare_strip_newlines`, `header_lstrip`, `shell_lstrip`: SONG_SOT 47/47; 3/3 ca HEAD0 → mutant3. Tất cả baseline ghép passed nhưng khối không xác thực/không marker. | **Ở đâu:** c35/c37/c47 + DOT_BIEN vì kiểm cấu trúc sau ghép phải đi tới marker. **Cách:** giữ REST/YAML tên/giờ hợp lệ; lần lượt bỏ dòng đầu rỗng trong khối log, thêm khoảng trắng vào riêng header, thêm khoảng trắng vào riêng token shell. **Khoá:** ba mutant phải GIET đúng ca, baseline không marker và ghép passed. **Rủi ro:** ca chết ở tên/số/giờ sẽ lại che chốt khối; không chuẩn hoá lại dữ liệu. | ~8–14, test+mutant |

Ước tổng **42–68 dòng**, chỉ là HINT chưa áp vào cây thật. Executor tự tái dẫn xuất, đo numstat/gate và chịu trách nhiệm commit. Có thể tham số hoá gọn hơn; không yêu cầu sao chép nguyên script reviewer hay áp đúng cách gợi ý. Không cần sửa sản phẩm đang đúng để làm test xanh.

**ĐỐI CHIẾU F01–F11.** Nguồn gần nhất r4 lượt3 tại parent `27997a73c6b01e577ed655ea94e73d56adf697da`; các verdict r4 lượt1/2 và r3 giữ trong input. Giữ slug/lịch sử, không reset bằng revision hay biểu hiện mới.

| lớp | kết quả | phép đo độc lập và giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG trong phạm vi đo | c22 và audit các mutant định danh GIET đúng ca; probes cũ Run/job/steps/check-run sai kiểu vẫn chưa đo. Không dùng `kich_ban.trang_thai` thay marker/ghép. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG các phản chứng sản phẩm được giao | Chạy lại 12 ca r3 của mỗi bộ prior: đúng 12/12 rc0 sau khi emitter có stdout suite thật. Hai cơ chế r2 metadata/mixed-color, collision, composite/boundary được chạy lại trên fixture REST r4 hợp lệ. Các ca c25–c27/c35/c40/c41/c43 và mutant đích đạt. F10 còn lỗ kiểm thử khác, không đổi chúng thành F02 mới. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20 và probes total đổi/thiếu/trùng/short page; từng mutant đúng ca. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | Probes route run/job/artifact khác trả404, attempt lọc state; F04 jobs/artifacts run+1 GIET c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG phạm vi đo | c01/c19/c22 và mutant summary/chiếu dữ liệu/lưới cuối GIET; HTTP403, thân sai dạng, lỗi ghi/ngoại lệ giữ mã thực/dòng đếm. Không tuyên bố mọi lỗi đã thử. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24 và mutant redirect/mất bắt lỗi/mang token GIET đúng ca; mock offline, không đo đường mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG bằng authority | A10 replay 13+1 và22+1; mỗi run một chuan-bi chưa đo, không gán SHA bằng REST. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 reader Git thật trên tree tạm; mutant bỏ SHA/luôn vắng GIET c34; ca git_workflow_source dùng object b27fe85 thật rc0. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | GIỮ ĐÓNG, không thấy regression sau đổi nơi cắt giây | Calendar probes và c38, mutant bỏ lịch/nhận offset/header thiếu lấy REST GIET đúng ca; các chốt thời điểm trong frontier/operator được đo lại. Không nhận timestamp sai thành passed trong các ca đã thử. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | **ĐÃ VÁ THẬT các biểu hiện lượt3 / CHƯA ĐÓNG CẢ LỚP** | 59 mutant cũ GIET, một neo hết hiệu lực và một tương đương đã xác minh; 17 mutant bổ sung không tương đương vẫn SONG_SOT47/47, từng cái có ca0→3. Bốn nhóm biểu hiện cũ về number/tên/chế độ/vị trí đã có răng c46/c47, nhưng miền chốt nguyên văn/chế độ kế tiếp vẫn hở như bảng lớp. |
| F11 `chan-path-chua-co-phan-chung` | GIỮ ĐÓNG | c42 lặp ENV/PATH trước/khác job/sau; mutant chỉ bỏ PATH GIET đúng c42. |

U={F10}, F={}: **0/1 lớp đóng toàn bộ (0%)** so lượt3; 0 lớp mới, 1 lớp còn mở/lặp. Các biểu hiện cũ đóng thật không đủ để ghi cả F10 đã đóng. Quyết định tiếp tục sau checkpoint của chủ kho vẫn được giữ; reviewer không tự áp lại V5 cũ.

**Phân hạng đột biến và lời khai executor.** Suite chính rc0, `CA: 47/47 dat`, `DOT BIEN: 155/155 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (2 dot bien)`, `TONG: DAT`; audit riêng 155 GIET đúng ca, 1 tự kiểm TIN_DUNG_GIA và1 tự kiểm SONG_SOT đúng thiết kế. `mutants/results.json` có neo/thay, baseline, ca đích, command/rc, output và hash từng mục. Các bản sao không ghi vào candidate.

61 phép frontier lượt3 được replay, tái neo phép đọc header giờ sau khi nó chuyển về tach_buoc: **59 GIET / 1 HONG_NEO / 1 SONG_SOT tương đương**. `raw-frontier-anchors.json` phân biệt script nguyên bản với phép tái neo: hai neo raw cũ mất là `log_group_close_exact` và `header_time_other_group`; phép sau đã được tái dẫn xuất và GIET, không tính mất neo là survivor. `log_group_close_exact` không tạo mutant vì HEAD đã là phép so nguyên văn ấy; chiều ngược lại `L3_endgroup_startswith` GIET c47. Đếm độc lập **753/753** dòng đóng trên37 log nguyên văn. `log_nested_after_only` tương đương: trước shell, mọi dòng không màu không có prefix shell làm ok=false dù bỏ riêng chốt nhóm lồng; sau shell cả hai biểu thức đều chặn; nhánh màu không đổi. Thử sáu vị trí cho output bằng nhau6/6 (`equivalence.json`), kèm lập luận theo nhánh, không gọi đây là lỗ test.

20 mutant reviewer bổ sung: **3 GIET / 17 SONG_SOT / 0 TIN_DUNG_GIA / 0 HONG_NEO**. Ba cái đã bị suite bắt là `name_explicit_casefold`, `metadata_post_suffix`, `number_contiguous`; không báo chúng là lỗ. Có18 ca độc lập0→3 (17 survivor và đối chứng number_contiguous), đủ36 lượt trong `new-counterexamples.json`. `new_frontier.py` và `boundary_cases.py` là script tái hiện; lệnh với bản sao dùng `CI_PROVENANCE_MA=.review/new-frontier/<tên>.py python -B .review/boundary_cases.py <tên>`. Chỉ `TinHieuChotCa` được bắt riêng để in DO/rc3; lỗi vô can ra HONG/rc4.

Đã tái chạy đột biến toán tử của executor trên130 bản biên dịch được, đổi đường dẫn và temp về scratch, giữ cơ chế sinh token. Bảng dưới giữ riêng từng hạng và mọi lỗi ca khác; **GIET+NEM không đồng nghĩa toàn bộ lỗi của mutant đều được cấp GIET**. Chỉ ca đã chết bằng TinHieuChotCa đúng tên được tính; ngoại lệ ngoài đó là tín dụng giả nếu dùng làm kill. c23/c39/c38/c44 kiểm chính thuộc tính không ném trên miền dữ liệu của ca nên biến ngoại lệ ở đúng miền thành TinHieuChotCa là phép đo hợp lệ; không lấy nó làm bộ bắt mọi lỗi ở mọi ca. Đây là phép đo độ phủ test, không phải chứng minh mọi mutant lỗi là lỗi sản phẩm HEAD.

**Replay A10 — đúng frozen data tại52e9573, không thay LIVE.** Callback REST chỉ trả bytes trong input; Git thật đọc workflow/parents/tree tại SHA checkout. SHA256SUMS37/37 khớp, hash/size full-log37/37 khớp provenance. Oracle độc lập đo37 job ghép duy nhất,345/345 tên,325/325 cửa sổ đúng vị trí; nhóm Run325=REST đã chạy325, REST ứng YAML345=YAML345. `replay-byte-comparison.json`: **43/43 file đầu ra bằng byte**, gồm hai provenance, run/jobs và37 trích log; không có khác biệt cần giải thích so frozen provenance52e9573. Dời cắt giây không đổi giá trị; endgroup exact khớp mọi dòng thật; bỏ cap200 không đổi trích trong dữ liệu này.

| run / attempt1 | rc | Checkout và ghép | SHA-256 provenance, trùng byte |
|---|---:|---|---|
| 39342960764 | 0 | 13 passed,1 chuan-bi not_measured; SHA b27fe85c9e9593ddbb059808fe4347fe1bd267be; parents5618020a67709ca6f2c93138905df0aa8d9c2df6 +400589368e09ab2ee0e734b7af08b93478035503; tree857bc47e6bc5f0024e442b400819ac51286dfc55 | `5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0` |
| 40074551995 | 0 | 22 passed,1 chuan-bi not_measured; SHA dc657149941f9db3ab2afc6fb6462ba4827bf18f | `24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b` |

Run đầu không có mục marker cho đường dẫn trong MOI (vẫn có9 mục ngoài MOI chưa đo). Run sau tám gate-nhanh-manh có nhanh_don_duoc_test not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker MOI. Mọi job labels Ubuntu; Gate không failed, Workflow definition vẫn not_measured. HTTP/freshness/retention/LIVE độc lập **KHÔNG ĐO ĐƯỢC**, không nâng Workflow definition nhờ YAML tại checkout. Chỉ số tên=Run+header97/325; số cửa sổ duy nhất tính trên bước đã chạy10/325, số6/325 của spec tính cả metadata REST, như đã phân biệt ở lượt trước; không dùng chỉ số ấy thay ghép theo vị trí.

**ĐỐI CHIẾU A1–A27.** `passed` dưới đây chỉ cho phép đo nêu rõ, không biến full gate chưa chạy thành passed.

| tiêu chí | trạng thái | bằng chứng và giới hạn |
|---|---|---|
| A1 | passed | c01/help đủ4cờ, thiếu attempt mutant GIET; sai đối số rc2 + summary4. |
| A2 | passed | c02 attempt2/1 failed rc12; mutant đúng ca. |
| A3 | passed trong7ca chỉ định | c03–c09 Linux/Windows fixture, SHA thiếu/khác/push/PR parents; mutant GIET. Không khai native Windows đã chạy. |
| A4 | passed các vế chỉ định | c10–c15 runner0/skipped/marker sai/khác bước/ngoài MOI/import động; mutant đúng ca. |
| A5 | passed | c16 Workflow definition chưa đo, path chỉ lời khai; mutant GIET. |
| A6 | passed | c17 lỗi ghi giữa chừng, có/không bản trước; mutant đúng ca. |
| A7 | passed | c18/c19 summary1, HTTP403 rc3/summary4, lỗi ghi/ngoại lệ; mutant đúng ca. |
| A8 | passed số/định dạng/phân hạng; **M11 còn F10** | Suite47/47,155/155,TU_KIEM2,TONG DAT; audit riêng xác nhận. Các chốt nguyên văn/miền vẫn thiếu răng. |
| A9 | phần đăng ký passed; full command **not_run** | Registry25/25; bỏ entry⇒25/24 và test sống chưa đăng ký; regex bằng tiền lệ, nhận stdout suite thật/từ chối3mẫu xấu; Ruff contract3/3. Không chạy --chay/heavy gate do chỉ thị hoãn của chủ kho. Thử phan_chung nhánh registry gặp git commit rc128 vì signer loopback socket bị sandbox cấm; KHÔNG coi driver0 là full acceptance. |
| A10 | frozen replay passed; LIVE KHÔNG ĐO ĐƯỢC | Hai run đúng hash,43file bằng byte,37log; không gọi API mới. |
| A11 | passed phạm vi được đo/authority mới | Đúng3tệp/1391dòng, diff-check0; doctrine10tệp/0chép, adr53/53; bare Ruff F0finding tách pin/probe3/3. Trần cũ1250 đã được chủ kho nâng theo assignment. |
| A12 | KHÔNG ĐO ĐƯỢC | Không mạng/remote fence/push/connector; không dùng lời khai thay ls-remote. |
| A13 | pending, chưa đo đầy đủ | Đã đo metadata CLI đúng thread; rollout size/hash ổn định và launcher receipt sau khi writer kết thúc thuộc bước điều phối hậu-run. Không nhận A13 hoàn chỉnh trong lượt đang ghi. |
| A14 | passed | c25 metadata màu; mutant đúng ca. |
| A15 | passed | c26 khối subset/mixed-color; mutant đúng ca. |
| A16 | passed các vế chỉ định; **F10 mở rộng** | c27 toàn khối tối giản/đối chứng, mutant GIET; biên run/header/shell mới vẫn hở test. |
| A17 | passed các vế chỉ định; **F10 còn miền chế độ** | c28–c31/c46, env/defaults/shell/VAR/args và đối chứng; các mutant mới sống nêu ở bảng lớp. |
| A18 | passed | c32 nguồn thiếu/object/path/YAML/SHA không marker/không ném; c34 Git thật và mutant. |
| A19 | passed | c33 trùng chữ khác job, đọc đúng chế độ; hai mutant đúng ca. |
| A20 | passed | c36 số nhóm/sốYAML/thiếu/thừa, mỗi chốt mutant; number_contiguous đã bị c36 bắt, không là lỗ mới. |
| A21 | passed ca chỉ định; **F10 còn nguyên văn/miền** | c37 tên lệch/name thẳng, c44/c45/c47, mutant có sẵn GIET; tên biên/metadata/outcome mới chưa có răng. |
| A22 | passed | c38/calendar/time probes; frontier và operator ở chốt giờ được đo lại; không thấy regression. |
| A23 | passed ca chỉ định; **F10 còn alias nguyên văn** | c39/c44/c47 zero/multi/expression/reusable/matrix và domain guard; alias escape/strip/casefold vẫn sống. |
| A24 | passed | c40 nested nhóm, ghép passed không marker; mutant GIET c40. Biến thể tương đương không tính survivor có lỗi. |
| A25 | passed | c41 uses/composite có/không bước theo, cơ chế count/uses; mutant đúng ca. |
| A26 | passed các vế chỉ định; **F10 còn bước trước skipped** | c42 ENV/PATH trước/khác job/sau/chính bước i; c47 đầu/cách bước; mutant bỏ riêng PATH GIET, mutant tự thêm điều kiện đã chạy vẫn sống. |
| A27 | passed | c43 khối khác bước/skipped không marker, mutant đúng ca. |

**Lệnh/rc và hiện vật.** Từ root: `PYTHONDONTWRITEBYTECODE=1 python -B .review/run.py <nhãn> <command...>`. Wrapper ghi command, rc con thật, thời gian, stdout/stderr raw + size/hash; đặt TMPDIR/TMP/TEMP/cache vào scratch. `suite.json`/`audit.json`/`frontier*.json`/`new-frontier.json`/`operators.json`/`replay.json` là receipt, không đồng nhất rc driver với assertion bên trong. Không chạy full selftest/release/CI do authority hoãn; các gate đó **not_run**, không phải skipped hay passed.

Đã chạy lại các bộ phép đo lượt1–3, cùng script r3 nằm trong chúng: calendar/new probes, classifier negative, registry, replay_Q1/time detail, old probes/compare/extra, shape, ca reviewer/trace, frontier và phản chứng. `prior-script-inventory.json` ghi60script root với hash/vai; script sinh cây/neo/verdict/snapshot cũ được tái dẫn xuất cho SHA hiện hành, không chạy mù assertion Reviewed commit cũ để xuất verdict mới. Các producer trùng byte được dùng chung phép audit; không cộng alias/tái chạy thành bằng chứng mutant khác nhau. Bảng lệnh phụ bên dưới giữ cả rc thất bại của script lịch sử; chỉ dùng lần fixture hợp lệ để kết luận.

Các lỗi giàn đã giữ riêng: emitter chạy trước stdout suite thật khiến ca shell rc3 và composite rc1; sau stdout thật, 12ca mỗi prior và composite current rc0. Boundary nguyên bản rc3 do thiếu ghép REST r4, bản current ghép passed rồi no-marker rc0. Một số compare nguyên bản thiếu object9e5019e rc1; bản current dùng r2-source.py đã giao và state steps hợp lệ, **không xác thực được OID Git lịch sử ấy**. Neo cũ thời gian/tên/PATH mất được ghi HONG_NEO rồi tái neo; không dùng lỗi neo làm kill/survivor. Registry regex lần setup đầu dùng summary tổng hợp chỉ để kiểm regex, đã chạy lại với stdout suite THẬT; không dùng summary tổng hợp làm test evidence. Lần thích nghi script giờ đầu còn đối số TS trong CHUỖI THAY, tạo TypeError giả; đã loại khỏi acceptance, tái dẫn xuất đúng chữ ký một đối số rồi chạy lại cả ba mutant (mỗi cái chỉ GIET c38, không lỗi ca khác) và15lượt ca reviewer:8baseline0/7mutant3 đúng tên. close-legacy lần đầu rc1 bắt chính lỗi giàn ấy, không phải finding sản phẩm; legacy-final-assertions.json xác minh kết quả cuối. Mọi lần đầu/incomplete giữ riêng; kết luận dựa phép đo cuối có đủ dependency. `TinHieuChotCa` trong một driver không tự làm lỗi setup thành bằng chứng đúng tính chất.

| nhãn | command con | rc / bằng chứng dương |
|---|---|---|
| suite | `python -B ops/ci_provenance_test.py` | 0; xem `suite.stdout.txt` và bảng phân hạng/JSON chi tiết |
| audit | `python -B .review/audit_mutants.py` | 0; xem `audit.stdout.txt` và bảng phân hạng/JSON chi tiết |
| frontier | `python -B .review/frontier.py` | 0; xem `frontier.stdout.txt` và bảng phân hạng/JSON chi tiết |
| frontier2 | `python -B .review/frontier2.py` | 0; xem `frontier2.stdout.txt` và bảng phân hạng/JSON chi tiết |
| new-frontier | `python -B .review/new_frontier.py` | 0; xem `new-frontier.stdout.txt` và bảng phân hạng/JSON chi tiết |
| prove-new-final | `python -B .review/prove_new.py` | 0; xem `prove-new-final.stdout.txt` và bảng phân hạng/JSON chi tiết |
| operators | `python -B .review/operators.py` | 0; xem `operators.stdout.txt` và bảng phân hạng/JSON chi tiết |
| replay | `python -B .review/prior2/replay_q1.py` | 0; xem `replay.stdout.txt` và bảng phân hạng/JSON chi tiết |
| equivalence | `python -B .review/verify_equivalence.py` | 0; xem `equivalence.stdout.txt` và bảng phân hạng/JSON chi tiết |
| legacy-final | `python -B .review/finish_legacy_current.py` | 0; xem `legacy-final.stdout.txt` và bảng phân hạng/JSON chi tiết |
| remaining-current | `python -B .review/run_remaining_current.py` | 0; xem `remaining-current.stdout.txt` và bảng phân hạng/JSON chi tiết |
| finish-probes-correct | `python -B .review/prior2/finish_probes.py` | 0; xem `finish-probes-correct.stdout.txt` và bảng phân hạng/JSON chi tiết |
| legacy-reviewer-final | `python -B .review/prior2/verify_new_cases.py` | 0; xem `legacy-reviewer-final.stdout.txt` và bảng phân hạng/JSON chi tiết |
| doctrine | `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; xem `doctrine.stdout.txt` và bảng phân hạng/JSON chi tiết |
| adr | `python -B .claude/dev/packet_loop.py adr-song --root .` | 0; xem `adr.stdout.txt` và bảng phân hạng/JSON chi tiết |
| ruff | `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` | 0; xem `ruff.stdout.txt` và bảng phân hạng/JSON chi tiết |

Driver remaining-current rc0 chỉ có nghĩa đã thu đủ rc từng lệnh; các lỗi con không bị che bằng nhãn passed. `remaining-current-results.json`, `legacy-final-results.json`, `legacy-reanchored.json`, `prior-reruns.json` giữ cả nguyên nhân và lệnh con.

**DANH SÁCH MUTANT KÈM HẠNG.** Dữ liệu raw trong JSON là nguồn đầy đủ cho neo/thay, đúng ca, rc và lỗi vô can. Bảng sau không cấp GIET cho các ca rc4.

| mutant ứng viên / tự kiểm | ca đích | baseline rc → mutant rc | hạng |
|---|---|---|---|
| `A1_xoa_co_attempt` | c01_cli_du_co | 0 → 3 | GIET |
| `A2_bo_so_attempt` | c02_attempt_lech | 0 → 3 | GIET |
| `A3d_lay_sha_dau_tien` | c06_checkout_hai_sha | 0 → 3 | GIET |
| `A3c_thieu_la_do_duoc` | c05_checkout_khong_sha | 0 → 3 | GIET |
| `A3e_lay_head_sha_rest` | c07_checkout_push_lech | 0 → 3 | GIET |
| `A3b_chi_nhan_linux` | c04_checkout_windows | 0 → 3 | GIET |
| `A3g_pr_nhan_moi_sha` | c09_checkout_pr_lech | 0 → 3 | GIET |
| `A3_sha_khong_nguyen_dong` | c05_checkout_khong_sha | 0 → 3 | GIET |
| `A4d_regex_ca_log_job` | c13_marker_buoc_khac | 0 → 3 | GIET |
| `A4b_skipped_la_passed` | c11_job_skipped | 0 → 3 | GIET |
| `A4a_runner_0_la_passed` | c10_runner_id_0 | 0 → 3 | GIET |
| `A4c_khong_khop_la_not_measured` | c12_marker_khong_khop | 0 → 3 | GIET |
| `A4_chep_cung_MOI` | c15_moi_mot_nguon | 0 → 3 | GIET |
| `A4_job_failure_bo_qua` | c14_ngoai_moi | 0 → 3 | GIET |
| `A5_passed_khi_co_path` | c16_workflow_def_luon_not_measured | 0 → 3 | GIET |
| `A6_ghi_thang_vao_out` | c17_ghi_nguyen_tu | 0 → 3 | GIET |
| `A7_bo_dong_dem` | c18_dem_not_measured | 0 → 3 | GIET |
| `A7_gop_rest_vao_12` | c19_rest_loi | 0 → 3 | GIET |
| `M1_chi_doc_trang_dau` | c20_du_trang | 0 → 3 | GIET |
| `F03_dung_khi_du_total` | c20_du_trang | 0 → 3 | GIET |
| `F03_tap_luon_du` | c20_du_trang | 0 → 3 | GIET |
| `F03_trung_id_van_them` | c20_du_trang | 0 → 3 | GIET |
| `F04_jobs_run_khac` | c20_du_trang | 0 → 3 | GIET |
| `F04_artifacts_run_khac` | c20_du_trang | 0 → 3 | GIET |
| `F01_run_thieu_van_passed` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_gate_thieu_van_passed` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_checkout_head_thieu` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F02_search_thay_match` | c23_chi_loi_goi_that | 0 → 3 | GIET |
| `A14_kich_ban_tu_dong_mau` | c25_f02_env_mang_mau | 0 → 3 | GIET |
| `A15_khoi_la_tap_con` | c26_f02_dong_khong_mau | 0 → 3 | GIET |
| `A16_bo_luat_toan_khoi` | c27_f02_yaml_khong_toi_gian | 0 → 3 | GIET |
| `A16_bo_khop_nguyen_van` | c25_f02_env_mang_mau | 0 → 3 | GIET |
| `A17i_cho_env_buoc` | c28_che_do_env_buoc | 0 → 3 | GIET |
| `A17ii_bo_env_job` | c29_che_do_env_job | 0 → 3 | GIET |
| `A17iii_cho_doi_so` | c30_che_do_doi_so | 0 → 3 | GIET |
| `che_do_bo_tien_to_VAR` | c31_che_do_duong_khac | 0 → 3 | GIET |
| `che_do_bo_env_workflow` | c31_che_do_duong_khac | 0 → 3 | GIET |
| `che_do_bo_defaults_workflow` | c31_che_do_duong_khac | 0 → 3 | GIET |
| `che_do_bo_defaults_job` | c31_che_do_duong_khac | 0 → 3 | GIET |
| `che_do_moi_shell` | c31_che_do_duong_khac | 0 → 3 | GIET |
| `A26_bo_GITHUB_ENV` | c42_github_env_cung_job | 0 → 3 | GIET |
| `F11_bo_GITHUB_PATH` | c42_github_env_cung_job | 0 → 3 | GIET |
| `A26_tinh_ca_buoc_i` | c42_github_env_cung_job | 0 → 3 | GIET |
| `A26_GITHUB_ENV_toan_workflow` | c42_github_env_cung_job | 0 → 3 | GIET |
| `F08_git_bo_sha` | c34_git_blob_that | 0 → 3 | GIET |
| `F08_git_luon_vang` | c34_git_blob_that | 0 → 3 | GIET |
| `F02_bo_doi_dong` | c35_f02_khoi_khong_tron_ven | 0 → 3 | GIET |
| `F02_bo_doi_shell` | c35_f02_khoi_khong_tron_ven | 0 → 3 | GIET |
| `F02_cho_mau_sau` | c35_f02_khoi_khong_tron_ven | 0 → 3 | GIET |
| `F02_bo_het_tien_to` | c35_f02_khoi_khong_tron_ven | 0 → 3 | GIET |
| `F02_bo_doi_header` | c35_f02_khoi_khong_tron_ven | 0 → 3 | GIET |
| `A18_head_sha_thay_sha_checkout` | c32_workflow_khong_doc_duoc | 0 → 3 | GIET |
| `A18_yaml_hong_nem` | c32_workflow_khong_doc_duoc | 0 → 3 | GIET |
| `A19_moi_ung_vien_trung_chu` | c33_trung_chu_khac_job | 0 → 3 | GIET |
| `A19_chan_doc_job_khac` | c33_trung_chu_khac_job | 0 → 3 | GIET |
| `A20i_zip_bo_dem_nhom` | c36_ghep_lech_so | 0 → 3 | GIET |
| `A20ii_zip_bo_dem_yaml` | c36_ghep_lech_so | 0 → 3 | GIET |
| `A21_bo_kiem_ten` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `ten_none_bang_none` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `ten_chi_buoc_chay` | c45_buoc_skipped_giua | 0 → 3 | GIET |
| `ten_name_khong_chuoi` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `ten_name_rong_bo_qua` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `ten_v_khong_chuoi` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `ten_rstrip` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `loc_post_khong_cach` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `chay_chi_success` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `dem_chi_khi_thua_nhom` | c36_ghep_lech_so | 0 → 3 | GIET |
| `dem_chi_khi_thieu_rest` | c36_ghep_lech_so | 0 → 3 | GIET |
| `gio_theo_thu_tu_tho` | c45_buoc_skipped_giua | 0 → 3 | GIET |
| `vi_tri_theo_thu_tu_tho` | c45_buoc_skipped_giua | 0 → 3 | GIET |
| `wf_none_khai_passed` | c32_workflow_khong_doc_duoc | 0 → 3 | GIET |
| `gio_match_thay_fullmatch` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `job_hau_to_bat_ky` | c39_ghep_job | 0 → 3 | GIET |
| `job_hau_to_khong_ngoac` | c39_ghep_job | 0 → 3 | GIET |
| `job_cho_x_rong` | c39_ghep_job | 0 → 3 | GIET |
| `gio_bo_kiem_str` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `gio_bo_bat_ValueError` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `job_chi_name_khi_co_name` | c39_ghep_job | 0 → 3 | GIET |
| `L3_number_bool` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_number_float` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_alias_name_bo` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_ma_tran_khac_rong` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_ma_tran_dotall` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_post_o_giua` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_run_rstrip_het` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_run_ep_chuoi` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_bo_dedupe` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_endgroup_startswith` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_shell_khong_cach` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_truoc_bo_buoc_dau` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_truoc_chi_lien_ke` | c47_bien_ghep | 0 → 3 | GIET |
| `L3_env_bo_dang` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_env_truthy` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_env_chi_chuoi` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_env_wf_co_mat` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_defaults_wf_truthy` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_defaults_job_truthy` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_shell_bo_pwsh` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_shell_bo_sh` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_shell_null_mac_dinh` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_khoa_bo_id` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_khoa_bo_if` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_khoa_bo_timeout` | c46_mien_che_do | 0 → 3 | GIET |
| `L3_khoa_bo_coe` | c46_mien_che_do | 0 → 3 | GIET |
| `O_job_none_and` | c39_ghep_job | 0 → 3 | GIET |
| `O_var_mot_dong_all` | c46_mien_che_do | 0 → 3 | GIET |
| `O_goi_or` | c23_chi_loi_goi_that | 0 → 3 | GIET |
| `O_goi_any` | c23_chi_loi_goi_that | 0 → 3 | GIET |
| `job_bo_x_str` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `so_number_0` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `so_number_am` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `sy_khong_list` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `dd_run_khong_chuoi` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `A22_bo_kiem_gio` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `A22_khong_cat_giay` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `F09_bo_kiem_lich` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `F09_nhan_offset` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `F09_header_thieu_dung_rest` | c38_ghep_lech_gio | 0 → 3 | GIET |
| `F10_bo_sort` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `F10_bo_number_trung` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `F10_ten_lstrip` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `F10_name_bieu_thuc` | c37_ghep_lech_ten | 0 → 3 | GIET |
| `dang_bo_number` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `dang_buoc_rest_khong_dict` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `dang_buoc_yaml_khong_dict` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `dang_job_khong_dict` | c44_ghep_sai_dang | 0 → 3 | GIET |
| `A23_lay_khoa_dau` | c39_ghep_job | 0 → 3 | GIET |
| `A23_nhan_job_goi_lai` | c39_ghep_job | 0 → 3 | GIET |
| `A23_nhan_bieu_thuc` | c39_ghep_job | 0 → 3 | GIET |
| `A24_bo_luat_nhom_long` | c40_nhom_long | 0 → 3 | GIET |
| `A25i_uses_sinh_marker` | c41_buoc_uses | 0 → 3 | GIET |
| `A25ii_zip_bo_dem_nhom` | c41_buoc_uses | 0 → 3 | GIET |
| `A27_khoi_bang_buoc_khac` | c43_khoi_khac_buoc | 0 → 3 | GIET |
| `F01_steps_chi_la_list` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F05_chieu_khong_an_toan` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F05_luoi_cuoi` | c19_rest_loi | 0 → 3 | GIET |
| `F02_khong_noi_dong` | c23_chi_loi_goi_that | 0 → 3 | GIET |
| `F02_cho_moi_co` | c23_chi_loi_goi_that | 0 → 3 | GIET |
| `F01_bool_la_int` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_chuoi_rong` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_conclusion_bat_ky` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_labels_rong` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_check_run_bat_ky` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_head_sha_bat_ky` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_head_sha_nhan_newline` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_check_run_nhan_newline` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_artifact_khong_kiem` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F01_phong_bi_khong_kiem` | c22_thieu_dinh_danh_khong_passed | 0 → 3 | GIET |
| `F03_bo_kiem_total_doi` | c20_du_trang | 0 → 3 | GIET |
| `F05_than_run_sai_dang` | c19_rest_loi | 0 → 3 | GIET |
| `F05_loi_ghi_mat_dong_dem` | c19_rest_loi | 0 → 3 | GIET |
| `F05_sai_doi_so_mat_dong_dem` | c01_cli_du_co | 0 → 3 | GIET |
| `F05_rest_mat_dong_dem` | c19_rest_loi | 0 → 3 | GIET |
| `F06_redirect_lot_loi` | c24_goi_that_loi_va_chuyen_huong | 0 → 3 | GIET |
| `F06_redirect_mang_token` | c24_goi_that_loi_va_chuyen_huong | 0 → 3 | GIET |
| `vo_can_AttributeError_qua_except_doi_kieu` | c03_checkout_linux | 0 → 4 | TIN_DUNG_GIA (tự kiểm có chủ ý) |
| `chi_them_chu_thich` | c20_du_trang | 0 → 0 | SONG_SOT (tự kiểm có chủ ý) |

| frontier lượt3 / bổ sung lượt4 | ca GIET đầu tiên, nếu có | hạng trên47ca / lỗi ngoài chốt |
|---|---|---|
| `job_rest_type` | c22_thieu_dinh_danh_khong_passed | GIET |
| `job_match_search` | c39_ghep_job | GIET |
| `job_matrix_nonempty` | c47_bien_ghep | GIET |
| `job_dotall_add` | c47_bien_ghep | GIET |
| `job_alias_exact_drop` | c47_bien_ghep | GIET |
| `name_use_last_line` | c26_f02_dong_khong_mau | GIET |
| `name_rest_strip` | c37_ghep_lech_ten | GIET |
| `time_drop_type` | c38_ghep_lech_gio | GIET |
| `time_year0_drop` | c38_ghep_lech_gio | GIET |
| `time_calendar_date_only` | c38_ghep_lech_gio | GIET |
| `time_low_strict` | c12_marker_khong_khop | GIET |
| `time_hi_strict` | c12_marker_khong_khop | GIET |
| `time_or_bounds` | c38_ghep_lech_gio | GIET |
| `time_low_only` | c38_ghep_lech_gio | GIET |
| `time_hi_only` | c38_ghep_lech_gio | GIET |
| `rest_number_float` | c47_bien_ghep | GIET |
| `rest_number_bool` | c47_bien_ghep | GIET |
| `rest_steps_list_drop` | c22_thieu_dinh_danh_khong_passed | GIET |
| `rest_steps_all_any` | c44_ghep_sai_dang | GIET |
| `yaml_steps_all_any` | c44_ghep_sai_dang | GIET |
| `number_sort_desc` | c12_marker_khong_khop | GIET |
| `metadata_keep_setup` | c12_marker_khong_khop | GIET |
| `metadata_keep_complete` | c12_marker_khong_khop | GIET |
| `metadata_post_anywhere` | c47_bien_ghep | GIET |
| `mode_env_shape_drop` | c46_mien_che_do | GIET |
| `mode_env_prefix_exact` | c29_che_do_env_job | GIET |
| `mode_shell_no_pwsh` | c46_mien_che_do | GIET |
| `mode_shell_no_sh` | c46_mien_che_do | GIET |
| `mode_shell_null_default` | c46_mien_che_do | GIET |
| `mode_env_presence_not_value` | c46_mien_che_do | GIET |
| `mode_env_job_presence` | c29_che_do_env_job | GIET |
| `mode_key_id_drop` | c46_mien_che_do | GIET |
| `mode_key_if_drop` | c46_mien_che_do | GIET |
| `mode_key_timeout_drop` | c46_mien_che_do | GIET |
| `mode_key_coe_drop` | c46_mien_che_do | GIET |
| `mode_prior_skip_first` | c47_bien_ghep | GIET |
| `mode_prior_only_first` | c42_github_env_cung_job | GIET |
| `mode_prior_only_last` | c47_bien_ghep | GIET |
| `mode_prior_include_current` | c42_github_env_cung_job | GIET |
| `run_rstrip_all` | c47_bien_ghep | GIET |
| `run_type_coerce` | c47_bien_ghep | GIET |
| `dd_group_reverse` | c12_marker_khong_khop | GIET |
| `dd_map_reverse` | c12_marker_khong_khop | GIET |
| `dd_output_dedupe` | c47_bien_ghep | GIET |
| `log_group_close_exact` | — | HONG_NEO |
| `log_shell_suffix` | c47_bien_ghep | GIET |
| `log_nested_before_only` | c40_nhom_long | GIET |
| `log_nested_after_only` | — | TƯƠNG ĐƯƠNG; SONG_SOT47/47 |
| `log_prefix_drop_ok` | c35_f02_khoi_khong_tron_ven | GIET |
| `log_close_ignore_prefix` | c35_f02_khoi_khong_tron_ven | GIET |
| `mode_defaults_wf_truthy` | c46_mien_che_do | GIET |
| `mode_defaults_job_truthy` | c46_mien_che_do | GIET |
| `mode_env_truthy` | c46_mien_che_do | GIET |
| `mode_env_string_only` | c46_mien_che_do | GIET |
| `number_type_bool_guard_drop` | c47_bien_ghep | GIET |
| `number_min_strict` | c12_marker_khong_khop | GIET |
| `header_time_other_group` | c12_marker_khong_khop | GIET |
| `header_window_other_step` | c38_ghep_lech_gio | GIET |
| `time_current_end_other_step` | c12_marker_khong_khop | GIET |
| `name_only_first_rest` | c37_ghep_lech_ten | GIET |
| `name_only_last_rest` | c45_buoc_skipped_giua | GIET |
| `job_escape_alias` | — | SONG_SOT47/47 (F10) |
| `job_alias_strip` | — | SONG_SOT47/47 (F10) |
| `job_casefold` | — | SONG_SOT47/47 (F10) |
| `name_explicit_strip` | — | SONG_SOT47/47 (F10) |
| `name_explicit_casefold` | c37_ghep_lech_ten | GIET |
| `metadata_setup_prefix` | — | SONG_SOT47/47 (F10) |
| `metadata_complete_prefix` | — | SONG_SOT47/47 (F10) |
| `metadata_post_suffix` | c12_marker_khong_khop | GIET |
| `ran_neutral_excluded` | — | SONG_SOT47/47 (F10) |
| `ran_cancelled_excluded` | — | SONG_SOT47/47 (F10) |
| `env_prefix_empty_suffix` | — | SONG_SOT47/47 (F10) |
| `env_prefix_casefold` | — | SONG_SOT47/47 (F10) |
| `mode_step_key_truthy` | — | SONG_SOT47/47 (F10) |
| `mode_shell_strip` | — | SONG_SOT47/47 (F10) |
| `mode_shell_casefold` | — | SONG_SOT47/47 (F10) |
| `mode_prior_requires_ran` | — | SONG_SOT47/47 (F10) |
| `run_compare_strip_newlines` | — | SONG_SOT47/47 (F10) |
| `header_lstrip` | — | SONG_SOT47/47 (F10) |
| `shell_lstrip` | — | SONG_SOT47/47 (F10) |
| `number_contiguous` | c36_ghep_lech_so | GIET |

**Mutant legacy bổ sung (raw, có neo cũ):** rank aggregate được giữ, phép tái neo tách riêng ở legacy-reanchored.json/adapted-time-mutants.json. Baseline không phải mutant.

| tên legacy | hạng raw / ca đã GIET |
|---|---|
| `sort_bi_bo` | GIET; c37_ghep_lech_ten |
| `kiem_number_bi_bo` | GIET; c37_ghep_lech_ten |
| `sap_xep_theo_ten` | GIET; c13_marker_buoc_khac, c23_chi_loi_goi_that, c31_che_do_duong_khac, c37_ghep_lech_ten, c42_github_env_cung_job, c44_ghep_sai_dang, c46_mien_che_do, c47_bien_ghep |
| `gio_nhan_offset` | GIET; c38_ghep_lech_gio |
| `gio_thieu_header_lay_rest` | HONG_NEO;  |
| `gio_bo_can_duoi` | HONG_NEO;  |
| `gio_bo_can_tren` | HONG_NEO;  |
| `a_bo_dem_nhom` | GIET; c36_ghep_lech_so, c41_buoc_uses |
| `a_bo_dem_yaml` | GIET; c36_ghep_lech_so |
| `b_bo_ten` | HONG_NEO;  |
| `d_lay_dau` | GIET; c39_ghep_job |
| `env_quet_ca_job` | GIET; c42_github_env_cung_job |
| `env_bo_PATH` | HONG_NEO;  |
| `number_missing_tu_sinh` | TIN_DUNG_GIA; c44_ghep_sai_dang |
| `job_ten_name_bi_bo` | GIET; c39_ghep_job, c47_bien_ghep |
| `job_khoa_bi_bo` | GIET; c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c23_chi_loi_goi_that, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c31_che_do_duong_khac, c33_trung_chu_khac_job, c36_ghep_lech_so, c37_ghep_lech_ten, c38_ghep_lech_gio, c39_ghep_job, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c44_ghep_sai_dang, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven |
| `ten_run_lstrip` | GIET; c37_ghep_lech_ten |
| `ten_name_khong_kiem_bieu_thuc` | GIET; c37_ghep_lech_ten |

`number_missing_tu_sinh` có GIET hợp lệ ở c44 nhưng còn rc4/KeyError tại c22, giữ TIN_DUNG_GIA cho các lỗi vô can đó. Không dùng aggregate TIN_DUNG_GIA làm kết luận sản phẩm có lỗi. Ba shape-mutant `rest_number_cho_zero`, `yaml_steps_bo_list_guard`, `rest_steps_bo_list_guard` đều bị bắt trên HEAD; bảng JSON shape giữ mọi ca và lỗi ngoài chốt. Hai alias F08 `git_ignore_sha`/`git_always_unavailable` cùng phép thay với catalog đã GIET đúng c34, không cộng bốn lần chạy lại thành bốn lỗ khác nhau.


**Toán tử tự động — 130 mục.** {'GIET': 108, 'GIET+NEM': 22}. GIET+NEM: kill hợp lệ và lỗi vô can được giữ RIÊNG; không phát hiện mutant chỉ TIN_DUNG_GIA hoặc SONG. Các mutant có NEM không là lỗ sản phẩm HEAD chỉ bởi mutant phá một bất biến gây ngoại lệ.

| mutant toán tử (vị trí/neo/thay) | ca GIET đầu tiên | hạng / số ca ném không được cấp kill |
|---|---|---|
| `L154c13:'is not'->'is'` | c12_marker_khong_khop | GIET; 0 |
| `L154c25:'and'->'or'` | c12_marker_khong_khop | GIET; 0 |
| `L154c38:'is not'->'is'` | c29_che_do_env_job | GIET; 0 |
| `L154c50:'or'->'and'` | c29_che_do_env_job | GIET; 0 |
| `L154c53:'any'->'all'` | c29_che_do_env_job | GIET; 0 |
| `L162c26:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L162c34:'and'->'or'` | c32_workflow_khong_doc_duoc | GIET; 0 |
| `L162c59:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L166c58:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L166c65:'and'->'or'` | c22_thieu_dinh_danh_khong_passed | GIET; 0 |
| `L166c77:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L166c85:'and'->'or'` | c22_thieu_dinh_danh_khong_passed | GIET; 0 |
| `L166c89:'any'->'all'` | c12_marker_khong_khop | GIET; 0 |
| `L167c16:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L167c23:'and'->'or'` | c33_trung_chu_khac_job | GIET; 0 |
| `L167c29:'and'->'or'` | c33_trung_chu_khac_job | GIET; 0 |
| `L167c39:'not in'->'in'` | c12_marker_khong_khop | GIET; 0 |
| `L167c48:'and'->'or'` | c33_trung_chu_khac_job | GIET; 0 |
| `L168c16:'0'->'1'` | c23_chi_loi_goi_that | GIET+NEM; 31 |
| `L168c32:'=='->'!='` | c12_marker_khong_khop | GIET+NEM; 2 |
| `L168c35:'1'->'2'` | c12_marker_khong_khop | GIET; 0 |
| `L168c35:'1'->'0'` | c12_marker_khong_khop | GIET+NEM; 2 |
| `L171c14:'in'->'not in'` | c23_chi_loi_goi_that | GIET+NEM; 31 |
| `L172c46:'and'->'or'` | c37_ghep_lech_ten | GIET; 0 |
| `L172c56:'not in'->'in'` | c31_che_do_duong_khac | GIET; 0 |
| `L174c34:'0'->'1'` | c23_chi_loi_goi_that | GIET+NEM; 31 |
| `L178c45:'19'->'20'` | c12_marker_khong_khop | GIET; 0 |
| `L178c45:'19'->'18'` | c38_ghep_lech_gio | GIET; 0 |
| `L178c82:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L178c89:'and'->'or'` | c38_ghep_lech_gio | GIET; 0 |
| `L187c10:'is'->'is not'` | c12_marker_khong_khop | GIET+NEM; 7 |
| `L191c9:'is'->'is not'` | c12_marker_khong_khop | GIET+NEM; 2 |
| `L191c17:'or'->'and'` | c39_ghep_job | GIET+NEM; 2 |
| `L191c27:'in'->'not in'` | c12_marker_khong_khop | GIET; 0 |
| `L191c44:'or'->'and'` | c39_ghep_job | GIET; 0 |
| `L191c56:'is not'->'is'` | c12_marker_khong_khop | GIET; 0 |
| `L191c68:'or'->'and'` | c44_ghep_sai_dang | GIET; 0 |
| `L191c71:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L191c75:'all'->'any'` | c44_ghep_sai_dang | GIET; 0 |
| `L191c87:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L193c7:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L193c21:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L193c29:'and'->'or'` | c22_thieu_dinh_danh_khong_passed | GIET; 0 |
| `L193c33:'all'->'any'` | c44_ghep_sai_dang | GIET; 0 |
| `L193c45:'is'->'is not'` | c12_marker_khong_khop | GIET; 0 |
| `L193c53:'and'->'or'` | c44_ghep_sai_dang | GIET+NEM; 1 |
| `L193c78:'1'->'2'` | c12_marker_khong_khop | GIET; 0 |
| `L193c78:'1'->'0'` | c44_ghep_sai_dang | GIET; 0 |
| `L194c12:'and'->'or'` | c22_thieu_dinh_danh_khong_passed | GIET; 0 |
| `L194c47:'=='->'!='` | c12_marker_khong_khop | GIET; 0 |
| `L196c77:'not in'->'in'` | c12_marker_khong_khop | GIET; 0 |
| `L197c11:'and'->'or'` | c12_marker_khong_khop | GIET; 0 |
| `L197c15:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L198c64:'!='->'=='` | c12_marker_khong_khop | GIET; 0 |
| `L199c17:'!='->'=='` | c12_marker_khong_khop | GIET; 0 |
| `L201c16:'!='->'=='` | c12_marker_khong_khop | GIET; 0 |
| `L203c7:'any'->'all'` | c37_ghep_lech_ten | GIET; 0 |
| `L203c11:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L203c37:'or'->'and'` | c37_ghep_lech_ten | GIET; 0 |
| `L203c54:'!='->'=='` | c12_marker_khong_khop | GIET; 0 |
| `L205c7:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L205c11:'all'->'any'` | c38_ghep_lech_gio | GIET; 0 |
| `L205c53:'and'->'or'` | c38_ghep_lech_gio | GIET; 0 |
| `L206c15:'and'->'or'` | c38_ghep_lech_gio | GIET; 0 |
| `L206c41:'and'->'or'` | c38_ghep_lech_gio | GIET; 0 |
| `L206c47:'<='->'<'` | c12_marker_khong_khop | GIET; 0 |
| `L206c52:'<='->'<'` | c12_marker_khong_khop | GIET; 0 |
| `L214c27:'in'->'not in'` | c12_marker_khong_khop | GIET; 0 |
| `L214c33:'or'->'and'` | c31_che_do_duong_khac | GIET; 0 |
| `L214c61:'or'->'and'` | c31_che_do_duong_khac | GIET; 0 |
| `L214c75:'in'->'not in'` | c12_marker_khong_khop | GIET; 0 |
| `L214c80:'or'->'and'` | c29_che_do_env_job | GIET; 0 |
| `L214c107:'or'->'and'` | c28_che_do_env_buoc | GIET; 0 |
| `L215c16:'or'->'and'` | c28_che_do_env_buoc | GIET; 0 |
| `L215c42:'not in'->'in'` | c12_marker_khong_khop | GIET; 0 |
| `L216c16:'or'->'and'` | c31_che_do_duong_khac | GIET; 0 |
| `L216c19:'any'->'all'` | c42_github_env_cung_job | GIET; 0 |
| `L262c91:'True'->'False'` | c12_marker_khong_khop | GIET; 0 |
| `L262c103:'True'->'False'` | c12_marker_khong_khop | GIET; 0 |
| `L262c120:'True'->'False'` | c12_marker_khong_khop | GIET; 0 |
| `L263c35:'19'->'20'` | c12_marker_khong_khop | GIET; 0 |
| `L263c35:'19'->'18'` | c12_marker_khong_khop | GIET; 0 |
| `L264c18:'and'->'or'` | c23_chi_loi_goi_that | GIET+NEM; 35 |
| `L264c34:'1'->'2'` | c12_marker_khong_khop | GIET+NEM; 2 |
| `L264c34:'1'->'0'` | c12_marker_khong_khop | GIET; 0 |
| `L265c31:'in'->'not in'` | c12_marker_khong_khop | GIET; 0 |
| `L266c17:'=='->'!='` | c12_marker_khong_khop | GIET; 0 |
| `L267c26:'False'->'True'` | c12_marker_khong_khop | GIET; 0 |
| `L268c21:'and'->'or'` | c12_marker_khong_khop | GIET; 0 |
| `L271c48:'and'->'or'` | c25_f02_env_mang_mau | GIET; 0 |
| `L271c52:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L271c60:'and'->'or'` | c25_f02_env_mang_mau | GIET; 0 |
| `L271c64:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L271c94:'and'->'or'` | c25_f02_env_mang_mau | GIET; 0 |
| `L272c20:'not'->''` | c47_bien_ghep | GIET; 0 |
| `L272c37:'or'->'and'` | c12_marker_khong_khop | GIET; 0 |
| `L272c66:'False'->'True'` | c12_marker_khong_khop | GIET; 0 |
| `L274c18:'1'->'2'` | c12_marker_khong_khop | GIET; 0 |
| `L274c18:'1'->'0'` | c12_marker_khong_khop | GIET; 0 |
| `L275c27:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L275c39:'and'->'or'` | c25_f02_env_mang_mau | GIET; 0 |
| `L275c51:'and'->'or'` | c25_f02_env_mang_mau | GIET; 0 |
| `L275c55:'not'->''` | c12_marker_khong_khop | GIET; 0 |
| `L275c72:'and'->'or'` | c25_f02_env_mang_mau | GIET; 0 |
| `L275c89:'1'->'2'` | c27_f02_yaml_khong_toi_gian | GIET; 0 |
| `L275c89:'1'->'0'` | c12_marker_khong_khop | GIET; 0 |
| `L275c92:'=='->'!='` | c12_marker_khong_khop | GIET; 0 |
| `L291c17:'0'->'1'` | c25_f02_env_mang_mau | GIET; 0 |
| `L292c36:'or'->'and'` | c12_marker_khong_khop | GIET+NEM; 11 |
| `L294c37:'not in'->'in'` | c12_marker_khong_khop | GIET; 0 |
| `L295c11:'not'->''` | c23_chi_loi_goi_that | GIET+NEM; 32 |
| `L295c26:'is'->'is not'` | c12_marker_khong_khop | GIET+NEM; 1 |
| `L295c33:'and'->'or'` | c25_f02_env_mang_mau | GIET+NEM; 1 |
| `L295c49:'and'->'or'` | c23_chi_loi_goi_that | GIET+NEM; 32 |
| `L295c70:'=='->'!='` | c12_marker_khong_khop | GIET; 0 |
| `L297c14:'1'->'2'` | c27_f02_yaml_khong_toi_gian | GIET; 0 |
| `L297c14:'1'->'0'` | c27_f02_yaml_khong_toi_gian | GIET; 0 |
| `L299c35:'or'->'and'` | c28_che_do_env_buoc | GIET; 0 |
| `L299c38:'any'->'all'` | c46_mien_che_do | GIET; 0 |
| `L299c44:'and'->'or'` | c12_marker_khong_khop | GIET+NEM; 3 |
| `L299c50:'1'->'2'` | c12_marker_khong_khop | GIET; 0 |
| `L299c50:'1'->'0'` | c12_marker_khong_khop | GIET; 0 |
| `L300c38:'2'->'3'` | c44_ghep_sai_dang | GIET+NEM; 20 |
| `L300c38:'2'->'1'` | c12_marker_khong_khop | GIET; 0 |
| `L300c62:'and'->'or'` | c23_chi_loi_goi_that | GIET+NEM; 4 |
| `L300c66:'all'->'any'` | c23_chi_loi_goi_that | GIET+NEM; 1 |
| `L302c21:'not in'->'in'` | c12_marker_khong_khop | GIET+NEM; 3 |
| `L302c32:'or'->'and'` | c28_che_do_env_buoc | GIET+NEM; 3 |
| `L303c102:'not in'->'in'` | c28_che_do_env_buoc | GIET; 0 |
| `L307c98:'0'->'1'` | c12_marker_khong_khop | GIET; 0 |

**TÍN DỤNG GIẢ / GIET+NEM chi tiết.** Các ca sau có rc ngoài0/3, giữ dưới nhãn lỗi vô can, không được tính là GIET:

- `L168c16:'0'->'1'`: c02_attempt_lech, c03_checkout_linux, c04_checkout_windows, c06_checkout_hai_sha, c08_checkout_pr_parents, c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c16_workflow_def_luon_not_measured, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c30_che_do_doi_so, c31_che_do_duong_khac, c33_trung_chu_khac_job, c36_ghep_lech_so, c37_ghep_lech_ten, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven.
- `L168c32:'=='->'!='`: c22_thieu_dinh_danh_khong_passed, c47_bien_ghep.
- `L168c35:'1'->'0'`: c22_thieu_dinh_danh_khong_passed, c47_bien_ghep.
- `L171c14:'in'->'not in'`: c02_attempt_lech, c03_checkout_linux, c04_checkout_windows, c06_checkout_hai_sha, c08_checkout_pr_parents, c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c16_workflow_def_luon_not_measured, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c30_che_do_doi_so, c31_che_do_duong_khac, c33_trung_chu_khac_job, c37_ghep_lech_ten, c39_ghep_job, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven.
- `L174c34:'0'->'1'`: c02_attempt_lech, c03_checkout_linux, c04_checkout_windows, c06_checkout_hai_sha, c08_checkout_pr_parents, c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c16_workflow_def_luon_not_measured, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c30_che_do_doi_so, c31_che_do_duong_khac, c33_trung_chu_khac_job, c37_ghep_lech_ten, c39_ghep_job, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven.
- `L187c10:'is'->'is not'`: c05_checkout_khong_sha, c06_checkout_hai_sha, c07_checkout_push_lech, c08_checkout_pr_parents, c09_checkout_pr_lech, c19_rest_loi, c22_thieu_dinh_danh_khong_passed.
- `L191c9:'is'->'is not'`: c22_thieu_dinh_danh_khong_passed, c47_bien_ghep.
- `L191c17:'or'->'and'`: c22_thieu_dinh_danh_khong_passed, c47_bien_ghep.
- `L193c53:'and'->'or'`: c22_thieu_dinh_danh_khong_passed.
- `L264c18:'and'->'or'`: c02_attempt_lech, c03_checkout_linux, c04_checkout_windows, c05_checkout_khong_sha, c06_checkout_hai_sha, c07_checkout_push_lech, c08_checkout_pr_parents, c09_checkout_pr_lech, c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c16_workflow_def_luon_not_measured, c18_dem_not_measured, c19_rest_loi, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c30_che_do_doi_so, c31_che_do_duong_khac, c33_trung_chu_khac_job, c36_ghep_lech_so, c37_ghep_lech_ten, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven.
- `L264c34:'1'->'2'`: c06_checkout_hai_sha, c47_bien_ghep.
- `L292c36:'or'->'and'`: c05_checkout_khong_sha, c06_checkout_hai_sha, c07_checkout_push_lech, c08_checkout_pr_parents, c09_checkout_pr_lech, c19_rest_loi, c22_thieu_dinh_danh_khong_passed, c36_ghep_lech_so, c37_ghep_lech_ten, c41_buoc_uses, c47_bien_ghep.
- `L295c11:'not'->''`: c02_attempt_lech, c03_checkout_linux, c04_checkout_windows, c06_checkout_hai_sha, c08_checkout_pr_parents, c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c16_workflow_def_luon_not_measured, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c30_che_do_doi_so, c31_che_do_duong_khac, c33_trung_chu_khac_job, c37_ghep_lech_ten, c38_ghep_lech_gio, c39_ghep_job, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven.
- `L295c26:'is'->'is not'`: c41_buoc_uses.
- `L295c33:'and'->'or'`: c41_buoc_uses.
- `L295c49:'and'->'or'`: c02_attempt_lech, c03_checkout_linux, c04_checkout_windows, c06_checkout_hai_sha, c08_checkout_pr_parents, c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c16_workflow_def_luon_not_measured, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c25_f02_env_mang_mau, c26_f02_dong_khong_mau, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c30_che_do_doi_so, c31_che_do_duong_khac, c33_trung_chu_khac_job, c37_ghep_lech_ten, c38_ghep_lech_gio, c39_ghep_job, c40_nhom_long, c41_buoc_uses, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep, c43_khoi_khac_buoc, c35_f02_khoi_khong_tron_ven.
- `L299c44:'and'->'or'`: c30_che_do_doi_so, c42_github_env_cung_job, c47_bien_ghep.
- `L300c38:'2'->'3'`: c12_marker_khong_khop, c13_marker_buoc_khac, c14_ngoai_moi, c15_moi_mot_nguon, c18_dem_not_measured, c20_du_trang, c22_thieu_dinh_danh_khong_passed, c23_chi_loi_goi_that, c27_f02_yaml_khong_toi_gian, c28_che_do_env_buoc, c29_che_do_env_job, c31_che_do_duong_khac, c33_trung_chu_khac_job, c37_ghep_lech_ten, c38_ghep_lech_gio, c39_ghep_job, c42_github_env_cung_job, c45_buoc_skipped_giua, c46_mien_che_do, c47_bien_ghep.
- `L300c62:'and'->'or'`: c27_f02_yaml_khong_toi_gian, c30_che_do_doi_so, c42_github_env_cung_job, c47_bien_ghep.
- `L300c66:'all'->'any'`: c27_f02_yaml_khong_toi_gian.
- `L302c21:'not in'->'in'`: c13_marker_buoc_khac, c14_ngoai_moi, c27_f02_yaml_khong_toi_gian.
- `L302c32:'or'->'and'`: c13_marker_buoc_khac, c14_ngoai_moi, c27_f02_yaml_khong_toi_gian.

**Read-only và bàn giao.** Snapshot đầu/cuối, so hash nội dung tracked/untracked/ignored ngoài `.review/`, head/tree/diff/index và `git status --short` được ghi ở `snapshot-comparison.json`/`final-check.json`. Chỉ chứng minh không có delta quan sát được giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Repo nguồn ngoài checkout được cấp không nằm trong phạm vi quan sát. `evidence-manifest.json` được sinh sau khi mọi writer test dừng, băm/readback hiện vật ổn định; nó không thay biên nhận runtime/transport sau phiên. Không có approve/merge/land/LIVE authority từ verdict này.
