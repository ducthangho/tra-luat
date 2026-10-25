from pathlib import Path
import json,collections
R=Path(__file__).resolve().parent
head='''verdict: changes_requested
reviewed_sha: ca11a6f1a7eb5286eeb6efc730d99beb33e2dcd1
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: ca11a6f1a7eb5286eeb6efc730d99beb33e2dcd1
reviewed_tree: 68a0f79e542d383acebf38313be7ea51c697ccfd
packet: wp899-r4
review_round: 1
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a17143-e953-7631-82b9-03a3c45295af
execution_surface: codex_cli
transport: machine
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a17143-e953-7631-82b9-03a3c45295af (CLI-published)
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**Chưa đạt V2: P0=1, P1=1, P2=1, P3=0, đếm theo lớp.** F01–F08 giữ đóng trong phạm vi đo; F02 đã được kiểm bằng phản chứng cũ và cấu trúc REST mới. Có ba lớp mới F09–F11. F09 là lỗi sản phẩm: thời điểm không tồn tại vẫn đủ điều kiện ghép và sinh marker `passed`. F10/F11 là thiếu răng kiểm thử trên các chốt sản phẩm hiện đang đúng. Đây là lượt 1 r4, lời gọi 1/8 theo assignment; nếu một lớp này lặp ở lượt 2 r4 thì áp V5. Không tự ghi approval hay chuyển state.

**Preflight, authority và phạm vi.** Nguồn assignment là `.review-input/prompt.md` và đặc tả r4 `.review-input/wp899-r4.md` **23.860 byte**, SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`, khớp. Đã đọc trọn r4 và các mục r2/r3 được kế thừa, verdict r3 lượt 2 trước lượt 1, mã/diff và counter scripts. R3 hash `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`, r2 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707`, đều khớp. Giữ Q1–Q12, trần ≤3 tệp/≤1250 dòng thêm, giới hạn khai của r4 và sensitive; không coi lựa chọn kiến trúc/giới hạn nguồn tin ấy là finding.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD và tree đúng đầu verdict. Base `ba222ffd1615f0d74b59985b9612f725211b62f5` là tổ tiên (rc0), parent `fe7522eb104daf93d0a8a5f37f0ee774e62a7846`. Immutable acceptance baseline là base; parent chỉ là điểm xuất phát cho delta. Diff toàn bộ và delta ở `full.patch`, `delta.patch`. Numstat rc0: `.claude/dev/ci_dang_ky_test.py` 1/0, `ops/ci_provenance.py` 444/0, `ops/ci_provenance_test.py` 772/0: **1217 dòng, còn 33**. Mục MOI đúng một dòng và regex bằng tiền lệ. `git diff --check <base> HEAD` rc0. `core.abbrev=7` đã có, không sửa config. `preflight-details.json` giữ command/rc/model evidence; `preflight.json` là receipt của wrapper.

Git OID r3 `7f5a02c...` và `9e5019e...` không có trong object database được cấp (rc128); không tự xác nhận lời khai hai blob ở parent được chép từ `7f5a02c`. `startpoint.json` giữ phần KHÔNG ĐO ĐƯỢC này. Đã đọc trực tiếp ba tệp tại parent và delta. Authority/generation/lease freshness phía GitHub, remote refs và sổ chi thực tế KHÔNG ĐO ĐƯỢC offline; assignment không cung cấp số generation riêng cho r4. Không suy generation từ tên thư mục hoặc dùng dữ liệu r3 thay r4.

**Môi trường và tái hiện.** Linux x86_64, Python 3.13.17 `/usr/bin/python`, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15, codex-cli 0.164.0. Metadata đúng thread trong `/root/.codex/sessions/2026/10/25/rollout-2026-10-25T04-13-59-01a17143-e953-7631-82b9-03a3c45295af.jsonl` công bố model/effort trên; model phục vụ từng request KHÔNG ĐO ĐƯỢC. Executor Claude/cloud/model_family=claude theo spec, chưa có runtime receipt Executor trong assignment. Không băm rollout đang được writer ghi để nhận A13 hoàn chỉnh.

Sandbox thực tế workspace-write, `.git` read-only; hành vi read-only của candidate được kiểm bằng snapshot. Skill `cross-review` được áp dụng. Catalog không có `environment_status`; doctor/chuan-bi/cài dependency không chạy trong review offline. `codex --version` rc0 kèm cảnh báo không tạo được PATH alias trên filesystem read-only. Không gọi mạng/GitHub/LIVE/subagent/push. A9 tự gọi signer fixture qua loopback và bị sandbox từ chối; không bypass ký/trust. Mọi tệp reviewer tạo nằm trong `.review/` theo assignment.

Từ gốc workspace, tái hiện bằng `python -B .review/run.py <nhãn> <command...>`. Wrapper đặt `PYTHONDONTWRITEBYTECODE=1`, TMPDIR/TMP/TEMP/cache vào `.review/`; receipt ghi rc con thật, command, thời gian, size/hash stdout/stderr. Rc0 của driver chỉ thu evidence; với phản chứng, xem rc ca trong JSON. Mutation chỉ ghi bản sao ở `.review/`, không sửa candidate. Chỉ `TinHieuChotCa` của đúng ca mới được cấp GIET.

**BẢNG LỚP.** Ba lớp mới, không đổi slug F01–F08. F09 khác F01: lỗi xác thực giá trị thời điểm của phép ghép M12 mới, không phải thiếu trường Run/job legacy. F10 là fixture định danh bước chưa có biến thể độc lập cho `number`/tên; F11 là nhánh chặn PATH chưa được đo. Không gộp chúng vào F02 về nguồn của lời gọi.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| **F09 `thoi-diem-khong-hop-le-van-ghep` — MỚI** | **P0** theo hạng assignment: thiếu căn cứ hợp lệ mà ghép/marker `passed` | `ops/ci_provenance.py:176`, `:203`; c38 ở `ops/ci_provenance_test.py:532` chỉ kiểm dạng một số trường. `_gio` chỉ regex và cắt chuỗi; so thứ tự từ điển không chứng minh thời điểm tồn tại. `started_at=2026-02-30T00:00:00Z` hoặc completed_at tháng13/giờ24/phút99/giây99 vẫn bao được header hợp lệ. | `python -B .review/run.py calendar python -B .review/calendar_cases.py`: driver rc0; **6/6 ca rc3/DO:<đúng-ca>**, tool rc0, `ghep_buoc=passed`, Gate/marker passed cả sáu. Workflow và log giữ cùng hash, chỉ sửa một trường REST; không cần quyền sửa nội dung tại SHA. `calendar-results.json` giữ đầy đủ. Header có ngày/giờ không tồn tại cũng lọt khi REST cùng dạng (`new-r4-probes.json`). `invalid_calendar` trong `reviewer-cases-r4.json` đỏ đúng chốt. | **Ở đâu/cách:** trong `_gio` và vế (c), giữ regex dạng UTC hiện hành, sau đó parse/validate lịch thật; kiểm cả header đã cắt về giây qua cùng validator. Thiếu/sai ⇒ cả job không marker. **Khóa:** mở rộng c38 bằng sáu biến thể độc lập đã đo, header thiếu/sai lịch, offset không hỗ trợ và đối chứng phần thập phân hợp lệ của header; mutant bỏ validation lịch, nới riêng offset, dùng giờ REST khi header thiếu phải chết đúng ca. Hai mutant sau hiện **SONG_SOT43/43**, ca reviewer giết đúng tên. **Rủi ro:** parse nới vô tình nhận offset/phần thập phân REST ngoài spec; datetime không được so với chuỗi; giữ đối chứng cùng giây và lỗi không ném. Chỉ mô tả hướng sửa mã sản phẩm. | **12–15 dòng ròng**, gồm code + mở rộng ca/mutant, tận dụng c38 hiện có; chưa áp. |
| **F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` — MỚI** | **P1**, M11 chưa khóa các phần của M12 | `ops/ci_provenance_test.py:108` (`buoc_rest`), `:525`, `:541`, bảng DOT_BIEN `:609`: các fixture luôn cho số tăng đúng thứ tự, không trùng, tên bước đơn giản. Bỏ sort hoặc kiểm uniqueness không ca nào đỏ; đổi first-line sang lstrip hoặc cho name biểu thức cũng không bị bắt. | `python -B .review/run.py extra-r4 python -B .review/extra_mutants_r4.py`: `sort_bi_bo`, `kiem_number_bi_bo`, `ten_run_lstrip`, `ten_name_khong_kiem_bieu_thuc` đều **43/43 xanh** trên bản sao, baseline43/43. `reviewer-cases-r4.json`: ca `rest_order`, `rest_duplicate`, `first_line`, `expression_name` baseline rc0; mutant tương ứng **rc3/DO đúng ca**, chứng minh thay đổi không tương đương. Không khẳng định sản phẩm hiện sai ở bốn chốt này. | **Ở đâu/cách:** bổ sung state biến thể sau `buoc_rest`, ở c36/c37/c39 hoặc một ca ghép chung: đảo list nhưng giữ number ⇒ vẫn passed; number trùng ⇒ not_measured; first-line rỗng ⇒ tên raw `Run `; name biểu thức ⇒ not_measured. Giữ workflow/log cố định ở mỗi phép đối chứng. **Khóa:** thêm bốn neo/thay trong `extra-r4/classified-results.json`; đòi chết bằng TinHieuChotCa đúng ca, ghép passed trước các ca cần kiểm downstream. **Rủi ro:** helper tự sửa lại state sau mutation làm mất phép đo; dùng header thiếu mà REST helper cũng sinh giờ sai thì ca chết ở chốt khác. | **10–13 dòng ròng** cho ca + mutant, tái dùng g1; chưa áp. |
| **F11 `chan-path-chua-co-phan-chung` — MỚI** | **P2**, lỗ kiểm thử hẹp M4/M11 | `ops/ci_provenance_test.py:565`: c42 chỉ dùng `GITHUB_ENV`; chưa kiểm nửa `GITHUB_PATH` của luật Q7/M4. | Cùng lệnh extra-r4: mutant `env_bo_PATH` chỉ đổi regex thành GITHUB_ENV, **43/43 xanh**. `github_path` trong `reviewer-cases-r4.json`: baseline rc0/CHAN, mutant **rc3/DO:github_path**, ghép passed; marker chuyển sai từ chưa đo thành passed trên mutant. | **Ở đâu/cách:** tham số hóa các đối chứng c42 hiện có qua ENV/PATH; giữ trước/cùng job, khác job, đứng sau. **Khóa:** mutant bỏ riêng PATH phải GIET đúng c42 (không cần sửa sản phẩm hiện đúng). **Rủi ro:** chỉ kiểm marker vắng mà không đòi ghép passed sẽ lại cấp tín dụng do lỗi fixture. | **2–3 dòng ròng** nếu lặp trên cùng ba đối chứng + một mutant; chưa áp. |

Tổng HINT **24–31 dòng ròng**, nằm trong 33 dòng dư theo ước lượng. Executor cần tái dẫn xuất, đo numstat thật và chạy lại gate; đây không phải bảo đảm đã triển khai trong trần hoặc quyền mở write set. Không đính patch mã sản phẩm.

**ĐỐI CHIẾU F01–F08.** Nguồn lịch sử: hai verdict r3 được giao, gần nhất reviewed_sha `7f5a02c9c2ff346484e10c2f5b4e94fcb0468b8b`; parent r4 được assignment chỉ định. Giữ các slug/lịch sử r2 và r3.

| lớp | kết quả trên r4 | bằng chứng/phạm vi |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG trong phạm vi đã đo | c22/các mutant F01 GIET đúng ca; probes thiếu/kiểu lạ của Run, steps, check_run_url giữ chưa đo và không ném ở các dạng đã thử. Không lấy `kich_ban.trang_thai` thay ghép và marker. |
| F02 `nhac-ten-script-thanh-thuc-thi` | **ĐÃ VÁ THẬT trong phạm vi phản chứng được giao** | Sáu ca reviewer r3 l1 và l2 đều rc0; hai cơ chế metadata/mixed-color r2 passed → r4 not_measured; tám collision có/không env/cùng/khác job bị chặn. Composite cũ rc0, boundary cũ rc3 do fixture ghép hỏng; đã dựng lại cả hai với `steps[]` hợp lệ: c40 ghép passed không marker; composite có nhóm cha lệch đếm, không có nhóm cha thì ghép passed nhưng bước uses không sinh marker. A14–A27/chốt nguyên văn và nested có mutant đúng ca. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20/probes total đổi, thiếu/trùng/underreported/short page trên jobs và artifacts; từng mutant tương ứng GIET. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | probes route run6/jobs6/artifacts6/logID lạ trả404; attempt khác đọc state; hai mutant đổi run+1 GIET c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG trong phạm vi đã đo | c01/c19/c22 + mutant summary/projection/lưới cuối GIET; HTTP403 bốn endpoint, run list/null/string, lỗi ghi và ngoại lệ ngoài hợp đồng giữ summary/rc hoặc ngoại lệ thật. Không suy mọi lỗi đều đã thử. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24/mutant direct/sau302 lỗi mạng và redirect token GIET; mock offline, không xác thực đường mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG bằng authority | Đúng13+1 và22+1; full-log replay không bịa SHA cho `chuan-bi` không checkout. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 reader thật trên tree tạm, missing path/non-UTF8; hai mutant F08 GIET đúng c34. Ca reviewer `git_workflow_source` dùng commit b27fe85/Git thật rc0. Chạy lại hai script extra_mutants r3 trên43 ca, đọc chi tiết ở evidence tương ứng. |

Lớp mở gần nhất U={F02}, đóng bằng phản chứng F={F02}: **1/1**, chỉ trong tập kiểm nêu trên. Ba lớp F09–F11 mới được báo riêng, không vào tử số và không đổi tên để xóa lịch sử. Giới hạn nguồn tin r4 bao gồm workflow/script/action tại SHA, kể cả action pin theo tag; không coi việc tác giả sửa chúng để in log giả là finding. Counter composite cũ được chạy lại để kiểm regression, không nhận là một cuộc tấn công nằm ngoài giới hạn nguồn tin mới.

**Chi tiết phản chứng F02 và quét rộng.** `old-cases-results.json` giữ lệnh/rc từng ca của hai lượt. `old1/probes.json`, `old2/probes.json` mỗi bản85 nhóm; `old2/new-probes.json` thêm biên nhóm/màu/composite và đo37 log:325 nhóm Run,226 khối hợp lệ,0 nested metadata,0 CRLF,0 closing suffix,0 dòng màu rỗng. `new-r4-probes.json` thêm số bước trùng/thiếu/bool, list đảo thứ tự, skipped xen giữa, tên reserved/name không chuỗi/name biểu thức ở job khác, run dòng đầu rỗng, continue-on-error, header thiếu, giờ dưới một giây/chung giây/REST offset/phân số; các kết quả được giữ riêng, không gọi tổng probe là tổng acceptance. Continue-on-error không suy rc từ conclusion; marker3/4 vẫn failed.

Composite mới: có nhóm cha + nhóm con ⇒ số nhóm lệch, cả job không marker. Chỉ nhóm con thay nhóm action ⇒ số đếm có thể khớp và ghép passed, nhưng bước uses không marker; bước run thật sau đó thiếu marker ⇒ failed. Nested không phải Run trước/sau shell ⇒ khối không hợp lệ; nested trong OUTPUT sau dấu đóng metadata vẫn cho đối chứng passed. Job gọi lại bị chặn. Hai job matrix có thể ghép cùng một key theo Q1(d), không tự yêu cầu uniqueness xuyên job.

Các lần chạy ban đầu `r4_compare.py` thiếu object9e5019e rc1 được giữ trong `old-cases-original-results.json`; sau đó dùng chính `r2-source.py` được giao, khai rõ không xác thực được Git OID cũ. Fixture direct RestGia phải thêm `steps[]` bằng helper hiện tại; bản có steps cho r2 passed → r4 not_measured (`old1-compare-with-steps.*`, `old2-compare-with-steps.*`). Script thống kê cũ glob ở sai cấp thư mục cho0 log, đã chạy lại với rglob để đo37. Lần đầu reviewer-cases khi một số mutant chưa tạo xong giữ riêng `reviewer-cases-r4-before-dependencies.json`; chỉ dùng lần `reviewer-cases-complete.*` sau khi đủ dependency. Header thiếu được thử lại với REST timestamp hợp lệ cố định để ca đo đúng thiếu header. Không dùng lỗi setup hay fixture sai làm finding/tín dụng giết.

**Căn cứ Q1 — đo lại đủ37 job, so với spec và output công cụ.** `replay_q1.py` tự đọc header thô bằng regex riêng, dựng mapping job/tên từ YAML Git thật, kiểm timestamp bằng datetime độc lập; `q1-details.json` có bảng từng job, ba số đếm, tên/giờ/hash log và trạng thái tool. Không lấy kết quả `ghep_buoc` của sản phẩm làm oracle.

| phép đo | 39342960764 | 40074551995 | tổng/đối chiếu spec |
|---|---:|---:|---|
| job ghép duy nhất | 14/14 | 23/23 | **37/37 khớp** |
| nhóm Run = REST đã chạy | 140=140 | 185=185 | **325=325,37/37 job khớp** |
| REST ứng YAML = YAML | 150=150 | 195=195 | **345=345,37/37 job khớp** |
| tên đúng từng vị trí | 150/150 | 195/195 | **345/345 khớp** |
| header cắt giây trong cửa sổ cùng vị trí | 140/140 | 185/185 | **325/325 khớp** |
| tên REST = Run + header | 35 | 62 | **97/325 khớp** |
| header cắt giây thuộc đúng1 cửa sổ, tính toàn bộ steps REST kể cả metadata | 2 | 4 | **6/325 khớp** |
| tool ghép passed | 13/14 | 22/23 | đúng A10; mỗi run `chuan-bi` thiếu checkout |

Chi tiết phép đo cửa sổ: nếu chỉ tính REST đã chạy sau lọc Set up/Complete/Post thì10/325 (4+6); tính toàn bộ REST steps cho6/325 đúng bảng spec. Không cắt header về giây cho một phép đo khác323/325 unique,2/325 không trong cửa sổ nào; không dùng metric này thay vế(c). `q1-time-details.json`, `q1-window-all-steps.json` giữ các phân biệt ấy. Q1 vẫn là quyết định đã cấp, không có finding về việc chọn thứ tự.

**A10 replay và giới hạn LIVE.** `python -B .review/run.py replay-q1 python -B .review/replay_q1.py` rc0;37/37 full-log hash và size khớp provenance,37/37 SHA256SUMS đúng (`log-hashes.json`). Callback REST chỉ đọc run.json/jobs.json/log được giao, artifact metadata từ provenance đóng băng; workflow và parents/tree gọi Git thật. Main chạy thật với callback ấy; provenance của cả hai run **trùng từng byte** với input:

- 39342960764: SHA-256 `5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0`, rc0; Checkout13 passed SHA `b27fe85c9e9593ddbb059808fe4347fe1bd267be`, parents `5618020a67709ca6f2c93138905df0aa8d9c2df6` + `400589368e09ab2ee0e734b7af08b93478035503`, tree `857bc47e6bc5f0024e442b400819ac51286dfc55`; chuan-bi chưa đo. Không marker đường dẫn thuộc MOI.
- 40074551995: SHA-256 `24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b`, rc0; Checkout22 passed SHA `dc657149941f9db3ab2afc6fb6462ba4827bf18f`, chuan-bi chưa đo. Tám job gate-nhanh-manh có marker nhanh_don_duoc_test chưa đo/che_do_khong_xac_dinh; gate-nhanh-gop không marker. Không Gate failed.

Cả37 job labels Ubuntu; Workflow definition luôn not_measured. Không có HTTP receipt/mạng mới để tự xác thực nguồn LIVE: **LIVE độc lập KHÔNG ĐO ĐƯỢC**, frozen replay passed. Không nâng mốc định nghĩa workflow bằng YAML ở SHA checkout hoặc đọc rc0 thành đủ bốn mốc.

**ĐỐI CHIẾU A1–A27.** Passed của ca chỉ định không thay việc invariant rộng đang có finding.

| tiêu chí | trạng thái | bằng chứng/phạm vi |
|---|---|---|
| A1 | passed | c01/help đủ4 cờ, mutant bỏattempt GIET; sai đối số rc2/summary4. |
| A2 | passed | c02/attempt2 so1 failed/rc12; mutant GIET. |
| A3 | passed trong7 ca | c03–c09/Linux/Windows fixture/SHA thiếu/khác/push/PR parents; mutant đích GIET. Windows fixture không là native Windows execution. |
| A4 | passed5 ca chỉ định; M4/M12 còn F09 | c10–c15 và mutants: runner0 not_run, skipped, marker sai/khác bước failed, ngoàiMOI chưa đo, import động thấy mục mới. |
| A5 | passed | c16/mutant path⇒passed GIET, REST path chỉ lời khai. |
| A6 | passed ở lỗi được thử | c17/lỗi ghi giữa chừng giữ out cũ hoặc vắng, mutant ghi thẳng GIET; crash/power-loss/writer cạnh tranh chưa đo. |
| A7 | passed ở phạm vi đo | c18 rc0/NOT_MEASURED1; c19 bốn endpoint403/rc3/summary4, lỗi JSON shape/lỗi ghi/lưới cuối; mutant GIET. |
| A8 | định dạng/phân hạng passed; M11 chưa đủ — F10/F11 | Suite rc0:43/43,87/87,TU KIEM DAT2,TONG DAT; audit89 mục đúng hạng. Tiêm mutant vô can vào DOT_BIEN ⇒ main rc1/TIN_DUNG_GIA/TONG DO (`classifier-negative.json`); không nhận nó là GIET. |
| A9 | command failed rc1; full acceptance KHÔNG ĐO ĐƯỢC do môi trường | --chay in ĐĂNG KÝ25/25, WINDOWS contract4/4, RUFF contract3/3 rồi signer fixture commit rc128/socket denied. Chưa tới chay_moi. Registry normal errors[]/25/25; gỡ mục trong bộ nhớ ⇒ test sống chưa đăng ký/25/24. Regex nhận suite thật, từ chối unequal/0mutant/TONG DO (`registry-details.json`). Không dùng probe thay --chay. |
| A10 | frozen replay passed; LIVE độc lập KHÔNG ĐO ĐƯỢC | Đủ37 log + REST frozen + Git thật; hai provenance trùng byte, đúng kỳ vọng r4 như trên. |
| A11 | passed | doctrine-scan rc0:10tệp/0chép; adr-song rc0:53/53; Ruff bare lint rc0/0finding trên2tệp mới; đúng3tệp/1217dòng; diff-check rc0. Ruff contract đo riêng errors[]/3, không dùng thay lint. |
| A12 | not_run/KHÔNG ĐO ĐƯỢC remote/future | Không ls-remote/push/connector trong review offline; V2 chưa đạt. |
| A13 | KHÔNG ĐO ĐƯỢC hoàn chỉnh | Đã trích model/effort/session từ rollout đúng run; vận chuyển cần stdout thread.started, launcher run.json, rollout size/hash ổn định sau run và readback1–5. |
| A14 | passed | c25 ghép passed trước khi chốt cấu trúc/nguyên văn chặn; mutant dựng từ màu GIET. Hai cơ chế cũ replay xanh. |
| A15 | passed | c26 ghép passed, không marker cho khối tập con; mutant tập con GIET; collision cũ bị chặn. |
| A16 | passed | c27 âm nonminimal + đối chứng toàn minimal có marker; mutant whole-block/equality GIET. |
| A17 | passed | c28/c29/c30 ba vế envstep/envjob/đối số + đối chứng, mutant từng vế GIET; c31 thêm các guard chế độ. |
| A18 | passed trong phạm vi đo | c32 object/path/YAML/SHA thiếu không ném; c34/Git thật, hai mutant F08; chưa xác thực object lịch sử không được cấp. |
| A19 | passed | c33 hai chiều job đích/job khác env; hai mutant quét mọi ứng viên/đọc job khác GIET đúng c33. |
| A20 | passed | c36 cả(a)(i)/(ii) có khẳng định ghép và không marker; bỏ riêng mỗi đếm GIET đúng c36; count guard chặn fake group cùng giây trong helper. |
| A21 | ca chỉ định passed; phần tên rộng thiếu răng F10 | c37 tên REST lệch + name nguyên văn dương; bỏ kiểm tên GIET. Name biểu thức/first-line rỗng chỉ được khóa trong ca reviewer, mutant còn sống43/43. |
| A22 | **failed ở yêu cầu thời điểm hợp lệ — F09** | c38 chặn một số dạng sai, ngoài cửa sổ, có đối chứng cắt giây; bỏ giới hạn dưới/trên chết đúng c38. Ngày không tồn tại vẫn ghép passed; offset-only và thiếu header chưa có răng trong suite43 ca. |
| A23 | ca(d) chỉ định passed; M11 vẫn F10 | c39 0/≥2key/expression job/reusable và matrix-key dương; mutant key đầu/uses/expr GIET. Number unique/order là phần định danh REST cần thêm ca. |
| A24 | passed | c40 ghép passed, nested sau shell không marker; bỏ luật nested GIET c40; before-shell/OUTPUT được probe riêng. |
| A25 | passed | c41 uses không marker và composite(+followup) fail count; hai mutant chỉ định GIET. Đã bổ sung biến thể composite ghép passed. |
| A26 | ENV ba chiều passed; PATH thiếu răng F11 | c42 đúng vị trí trước/cùng job, khác job, sau; bỏ guard/quét workflow/quét cả job GIET. Mutant chỉ bỏ PATH còn sống43/43. |
| A27 | passed | c43 ghép passed nhưng khối bằng bước khác/skipped, không marker; mutant tìm run khác GIET c43. |

**MUTANT VÀ HẠNG.** `mutants/results.json` lưu87 mục DOT_BIEN +2 tự kiểm, baseline từng target, neo/thay, command/rc/output/hash:87 GIET,1 TIN_DUNG_GIA tự kiểm,1 SONG_SOT comment-only tự kiểm. Đây là số mục catalogue/target, không khẳng định87 source mutation khác nhau (A20i và A25ii dùng cùng phép thay, khác target). `extra-r4/classified-results.json` giữ18 lần thử thêm/kiểm lại:10 GIET đúng ca chọn theo tính chất,7 SONG_SOT43/43,1 TIN_DUNG_GIA; baseline nguyên source43/43 không tính mutant. Bốn phép bỏ(a)/(b)/(d) là replay mutant đã có, không cộng thành mutant phân biệt. Lần đổi job-key còn gây một số lỗi vô can ở ca khác; chỉ cấp GIET theo DO:c39 đã lưu. Lần `number_missing_tu_sinh` chỉ gây KeyError ở c22 nên không tính GIET. Bảy survivor đều GIET bởi ca reviewer bổ sung sau khi baseline xanh, không đổi hạng SONG_SOT của chúng đối với bộ43 ca ứng viên.

| mutant catalogue | ca đích | rc baseline → mutant | hạng |
|---|---|---|---|
'''
rows=json.loads((R/'mutants/results.json').read_text())
for r in rows:
 head+=f"| `{r['name']}` | `{r['case']}` | {r['baseline']['rc']} → {r.get('mutant',{}).get('rc','N/A')} | {r['rank']} |\n"
head+='''
| mutant reviewer | ca đích đã đọc output | rc baseline → mutant | hạng trên43 ca ứng viên |
|---|---|---|---|
'''
for r in json.loads((R/'extra-r4/classified-results.json').read_text()):
 if r['name']=='baseline':continue
 t=r['target'];head+=f"| `{r['name']}` | `{t['case']}` | 0 → {t['rc']} | {r['rank']} |\n"
head+='''
Ca reviewer bổ sung nằm ở `reviewer_cases_r4.py`, command/rc từng baseline/mutant trong `reviewer-cases-r4.json`. Bảy ca `rest_order`, `rest_duplicate`, `first_line`, `expression_name`, `time_format`, `time_missing_header`, `github_path`: baseline rc0 và mutant rc3/DO đúng tên. Ca `invalid_calendar` đỏ ngay trên candidate. `calendar-results.json` đo riêng sáu giá trị sai để một assertion đỏ đầu tiên không che các biến thể còn lại.

**Giới hạn và bàn giao.** Native Windows/pwsh, runner thật sinh biên composite/nested ra sao, API/redirect thật, full runtime/release gates, required CI trên candidate: not_run/KHÔNG ĐO ĐƯỢC. Chưa có dữ liệu đủ cho A9/A12/A13 và LIVE độc lập A10; không ghi chúng là passed. Các hướng cần nội dung tấn công nhạy cảm path/symlink/credential không được tự soạn hoặc thử; ngoài miền phản chứng đã chạy chỉ mô tả giới hạn. Không yêu cầu gỡ guard để tăng tỷ lệ đo.

**Snapshot cuối.** `snapshot-start.json`, `snapshot-end.json`, `snapshot-comparison.json` băm size/nội dung **5632 tệp** ngoài `.git/` và output `.review/`, gồm ignored/untracked, `.codex/` và toàn `.review-input/`: **0 delta**, HEAD/tree giữ nguyên, tracked/cached diff rỗng; Git rc0. Ignored đầu/cuối chỉ `.codex/`, `.review-input/`, `.review/`. Metadata `.git/` không được băm toàn bộ; kiểm HEAD/tree/index/diff/status. Hai snapshot chứng minh không có delta quan sát tại hai mốc; không chứng minh chưa từng ghi rồi hoàn nguyên trong toàn lịch sử. Không có repo nguồn bên ngoài nào được cấp để snapshot.

Verdict changes_requested chỉ neo exact SHA đầu tệp. Giữ F09–F11 cho lượt kế tiếp; áp V5 nếu lặp ở lượt2 r4. Bên điều phối thu receipt runtime sau khi writer kết thúc và vận chuyển theo authority của mình; reviewer không đăng GitHub, đẩy, merge, land, LIVE hoặc tự mở lượt review mới.
'''
(R/'VERDICT.md').write_text(head,encoding='utf-8')
print('wrote',len(head.encode()),'bytes',len(head.splitlines()),'lines')
