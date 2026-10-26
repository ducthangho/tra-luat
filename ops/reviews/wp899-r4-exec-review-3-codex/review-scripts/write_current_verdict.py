from pathlib import Path
import json,collections,hashlib
R=Path(__file__).resolve().parent
base='ba222ffd1615f0d74b59985b9612f725211b62f5';head='27997a73c6b01e577ed655ea94e73d56adf697da'
audit=json.loads((R/'mutants/results.json').read_text());front=json.loads((R/'frontier/results.json').read_text())+json.loads((R/'frontier2/results.json').read_text());proof=json.loads((R/'frontier-counterexamples.json').read_text())
assert len(audit)==127 and sum(x['rank']=='GIET' for x in audit)==125
assert len(front)==61 and collections.Counter(x['rank'] for x in front)=={'GIET':33,'SONG_SOT':28}
assert len(proof)==52 and all(x['rc']==0 if x['source']=='HEAD' else x['rc']==3 and x['output'].startswith('DO:'+x['case']+':') for x in proof)
proved={x['mutant'] for x in proof};assert len(proved)==25
A=json.loads((R/'snapshot-start.json').read_text());B=json.loads((R/'snapshot-end.json').read_text())
delta=[p for p in set(A['files'])|set(B['files']) if A['files'].get(p)!=B['files'].get(p)];assert not delta and A['git']==B['git']
(R/'snapshot-comparison.json').write_text(json.dumps({'files':len(A['files']),'delta':delta,'git_equal':A['git']==B['git']},indent=2))
text='''verdict: changes_requested
reviewed_sha: 27997a73c6b01e577ed655ea94e73d56adf697da
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 27997a73c6b01e577ed655ea94e73d56adf697da
reviewed_tree: 3749900da8c09704d91674421957a1d6e1567ee1
packet: wp899-r4
review_round: 3
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a17181-66a4-7513-aa98-0f337e5a6438
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**P0=0, P1=1, P2=0, P3=0, đếm theo lớp. F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` LẶP; chưa đủ V2.** Hai biểu hiện lượt 2 đã vá thật, nhưng bộ 45 ca chưa khóa hết kiểu/miền giá trị/vị trí của chuỗi ghép và xác thực bước. Một ví dụ trực tiếp: mutant cho `number` là bool sống **45/45**; ca c44 hiện đặt `True` vào bước có number=3, trùng với number=1 của `Set up job`, nên uniqueness vẫn chặn và che việc mất kiểm kiểu. Đặt True vào chính metadata đầu tiên thì baseline chặn, mutant ghép `passed` và sinh marker `passed`. Đây là cùng cơ chế F10, không đổi thành lớp mới để bỏ lịch sử.

Suite khai **45/45 ca, 125/125 mutant, tự kiểm 2, TONG DAT, rc0** được chạy lại. Audit riêng xác nhận 125 mutant nghiệp vụ GIET đúng ca; hai tự kiểm là TIN_DUNG_GIA và SONG_SOT có chủ ý. Nhưng 61 thử nghiệm bổ sung cho **33 GIET / 28 SONG_SOT** trên cả 45 ca. Với 25 mutant sống, reviewer dựng 26 ca độc lập: **26 baseline rc0 → 26 mutant rc3/DO đúng tên**, chỉ qua TinHieuChotCa. Không lấy tổng suite xanh làm bằng chứng đóng lớp; không dùng mutant để khẳng định sản phẩm hiện có chính lỗi của mutant.

**Authority và preflight.** Assignment `.review-input/prompt.md` được người dùng giao trực tiếp. Đã kiểm và đọc trọn spec r4: 23.860 byte, SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`; r3 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`, r2 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` đều khớp. Đọc các mục được dẫn, lịch sử F01–F11 và nguồn protocol/adapter. Áp skill `cross-review` (.agents/skills/cross-review/SKILL.md).

Giữ Q1–Q12 và `gioi_han_khai`. Theo authority mới trong assignment (checkpoint issuecomment-6393643859), V5 cũ không buộc dừng lượt này; chủ kho đã nâng trần dòng chưa nêu số và cho tiếp tục đến hết P1/P2. Đây là lời gọi 3/8 theo assignment. Không coi 1312>1250 hoặc việc chưa đẩy/chưa chạy heavy gate là finding; không suy rằng trần đã vô hạn.

Origin `https://github.com/ducthangho/tra-luat.git`, detached HEAD đúng SHA/tree trên; parent `52e9573d0bd401a629a031a9c32df7bfd17c27c1`. Baseline nghiệm thu bất biến `ba222ffd1615f0d74b59985b9612f725211b62f5` là ancestor, rc0. Điểm xuất phát `fe7522eb104daf93d0a8a5f37f0ee774e62a7846`; parent chỉ là delta lượt này, không dời baseline. `git diff --numstat <base> HEAD`: **1 + 444 + 867 = 1312 dòng thêm**, đúng ba tệp write set; diff registry đúng một mục MOI. `git diff --check <base> HEAD` rc0; `core.abbrev=7` đã có. `preflight.json`, `full.patch`, `delta.patch` giữ lệnh/rc và bytes. Clone shallow; không khẳng định đủ mọi ref/object lịch sử. Nguồn spec authoritative trong phạm vi review offline là bản/hash được assignment chỉ định, không tự chứng nhận freshness GitHub.

Generation riêng, lease/state/authority GitHub hiện hành, remote fence, việc đã đẩy nhánh lưu trữ, tổng chi thực tế và blob provenance `7f5a02c` **KHÔNG ĐO ĐƯỢC offline**. Không suy generation từ tên archive. Những giới hạn đó không được dùng để chuyển state hoặc chứng nhận land.

**BẢNG LỚP — một lớp mở, nhiều biểu hiện.** Giữ slug F10. Phạm vi quét mở rộng theo yêu cầu lượt này sang ghép tên, kiểu/miền number, chế độ, vị trí bước trước và cấu trúc khối. Cùng cơ chế là fixture mặc định/khẳng định ghép che một chốt khác; các biểu hiện mới dưới đây không reset lịch sử. Bản vá của hai biểu hiện đã chỉ ở lượt 2 là thật, nhưng kết luận đóng CẢ LỚP là chưa thật.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F10 — LẶP, kiểu number không được cô lập | P1 | `ops/ci_provenance_test.py:601` c44 gán True ở bước thứ 3, đụng number 1; không có float. Chốt sản phẩm `ops/ci_provenance.py:193` đang đúng. | `frontier.py`/`frontier2.py`: `rest_number_bool`, `rest_number_float`, `number_type_bool_guard_drop` đều sống 45/45. `frontier_cases.py number_bool_metadata` và `number_float`: HEAD0 → mutant3 đúng ca; bool metadata qua mutant sinh marker passed. | **Ở đâu:** c44 + DOT_BIEN, vì fixture đó phải đo kiểm kiểu thay vì uniqueness. **Cách:** biến đổi state sau helper; bool đặt ở metadata đầu tiên để thứ tự/uniqueness vẫn đúng, float giữ vị trí cũ. **Khóa:** ba mutant trên phải chết đúng ca; giữ đối chứng integer và bool-as-int toàn cục. **Rủi ro:** helper sinh lại steps, hoặc số thay đổi làm chốt tên/thứ tự chết trước; đòi đúng lý do `steps_rest_sai_dang`. Không cần sửa sản phẩm. | ~6–12, test+mutant |
| F10 — biểu hiện mới trong cùng lớp, tên và byte của run | P1 | `ops/ci_provenance_test.py:563` c39 chỉ có đối chứng tên khoá, chưa có `name: Build` được gọi đúng alias; `:537` chỉ đòi ghép khi run có khoảng trắng cuối, chưa đòi marker. Chốt tại `ops/ci_provenance.py:167`, `:197`, `:295`. | `job_alias_exact_drop`, `metadata_post_anywhere`, `run_rstrip_all` sống 45/45; ca `job_alias_exact`, `metadata_post_infix`, `run_trailing_space`: HEAD0 → mutant3. `matrix_empty` cũng phân biệt được `.*`/`.+`. | **Ở đâu:** c37/c39 và ca run nguyên văn hiện có, vì cần kiểm tới kết quả marker sau ghép. **Cách:** thêm alias exact hợp lệ, tên chứa `Post ` ở GIỮA; khối và YAML cùng giữ khoảng trắng cuối. **Khóa:** mutant tương ứng phải chết đúng ca; kiểm ghép passed trước khi so marker. **Rủi ro:** chỉ so `ghep_buoc` sẽ lại bỏ qua do_dau_duong; đừng strip fixture để làm khớp. | ~10–18, test+mutant |
| F10 — biểu hiện mới trong cùng lớp, miền chế độ | P1 | `ops/ci_provenance_test.py:469` c31 chỉ thử một shell lạ và defaults khác rỗng; mặc định không mang các khoá allowlist. `_env_chan`/`chan_buoc` tại `ops/ci_provenance.py:153`, `:214`. | `mode_env_shape_drop`, `mode_env_truthy`, `mode_env_string_only`, `mode_defaults_*_truthy`, `mode_shell_no_pwsh`, `mode_shell_no_sh`, `mode_shell_null_default`, `mode_env_presence_not_value`, bốn `mode_key_*_drop` đều sống. Các ca độc lập tương ứng HEAD0 → mutant3. | **Ở đâu:** c31/c44 và DOT_BIEN, tái dùng fixture đã ghép đúng. **Cách:** tách absent/false/list/expression/dict rỗng, defaults có mặt nhưng rỗng, shell sh/pwsh/explicit null và từng khoá id/if/timeout/continue-on-error. **Khóa:** bỏ một giá trị hợp lệ hoặc cho một dạng bị chặn qua phải làm đúng ca đỏ. **Rủi ro:** một khoá lạ khác che khoá đang đo; mỗi biến thể chỉ đổi một trục, có cả chặn và đối chứng cho phép. Đây là kiểm hợp đồng offline, không khai native pwsh đã chạy. | ~18–30, test+mutant |
| F10 — biểu hiện mới trong cùng lớp, vị trí và cấu trúc | P1 | `ops/ci_provenance_test.py:589` c42 đặt ghi ENV/PATH sát bước đích, sau một uses ở index0; không đo run ở index0 hay một run không sát đích. Chốt `ops/ci_provenance.py:216`, `:271`. | `mode_prior_skip_first`, `mode_prior_only_last`, `log_shell_suffix` sống 45/45. Ca `prior_first_step`, `prior_nonadjacent`, `shell_prefix_space_missing`: HEAD0 → mutant3. `run_type_coerce` sống nhưng ca `nonstr_no_throw` bắt đúng thuộc tính không ném (HEAD0 → mutant3). | **Ở đâu:** c42/c35/c44 + DOT_BIEN. **Cách:** dùng REST/log cố định khớp workflow không có nhóm uses thừa; đặt run nhắc ENV/PATH tại đầu và cách đích một bước; đo token shell thiếu dấu cách; nonstring run có name tĩnh đi tới chốt dạng. **Khóa:** đúng mutant/đúng ca, ghép passed ở các ca downstream; no-throw là chính điều ca dạng kiểm, không đổi mọi ngoại lệ thành kill. **Rủi ro:** giữ LINUX setup group khi bỏ bước uses làm lệch đếm, tạo phản chứng giả; bắt ngoại lệ vô can có thể cấp tín dụng giả. | ~12–22, test+mutant |

Ước tổng khoảng **46–82 dòng**, có thể gọn hơn khi tham số hoá; không là bảo đảm size hoặc quyền mở write set. HINT chỉ cho test/đột biến, chưa áp vào cây thật. Executor tự tái dẫn xuất và đo, không sao chép mù. Không yêu cầu áp y gợi ý; phải đóng lớp chứ không chỉ giết đúng danh sách này.

**ĐỐI CHIẾU F01–F11 / LƯỢT TRƯỚC.** Nguồn gần nhất `.review-input/r4-luot2/VERDICT.md` tại `52e9573…`; trước đó r4 lượt1 `ca11a6f…`, r3 hai lượt được giữ trong input.

| lớp / slug | phân loại | bằng chứng độc lập trên HEAD và giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | ĐÃ VÁ THẬT / giữ đóng trong phạm vi đo | c22, các mutant F01 đúng ca; probes cả hai bộ cũ. Không lấy metadata kich_ban thay marker hoặc ghép. F10 bool-number là thiếu răng test, không nói HEAD đã nhận bool. |
| F02 `nhac-ten-script-thanh-thuc-thi` | ĐÃ VÁ THẬT / giữ đóng trong phạm vi phản chứng | 12 ca reviewer r3 (6 mỗi bộ) rc0; compare hai cơ chế cũ chuyển passed→not_measured, collision, c25/c26/c35/c40/c41/c43 cùng mutant đúng ca. Composite sau sửa riêng đường dẫn scratch và dựng REST đúng r4 rc0; boundary cũ thiếu steps giữ lỗi fixture, bản current rc0. Không dùng đầu ra do tác giả sửa nội dung tại SHA để vượt `gioi_han_khai`. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | ĐÃ VÁ THẬT / giữ đóng | c20/mutant phân trang thiếu/lặp/total đổi và probes cũ jobs/artifacts; không coi total khai bằng số ID là đủ. |
| F04 `rest-gia-khong-neo-run` | ĐÃ VÁ THẬT / giữ đóng | c20/probes route run/attempt/log lạ; đổi jobs/artifacts sang run+1 GIET đúng c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | ĐÃ VÁ THẬT / giữ đóng trong phạm vi đo | c01/c19/c22, bốn endpoint403, sai shape run, lỗi ghi, lưới cuối, các mutant summary/projection đúng ca. Lỗi ngoài hợp đồng vẫn không biến thành rc0. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | ĐÃ VÁ THẬT / giữ đóng | c24/redirect/network/token mocks và hai mutant đúng ca; không gọi mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | ĐÃ VÁ THẬT bằng authority / giữ đóng | Replay đủ37 log: mỗi run một chuan-bi chưa đo checkout, không bịa SHA; số13+1 và22+1 đúng r4. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | ĐÃ VÁ THẬT / giữ đóng | c34 dùng Git object/tree thật, missing path/nonUTF8; hai mutant reader GIET c34 trong catalogue và hai bộ extra cũ. Không xác thực được OID lịch sử không có trong shallow clone. |
| F09 `thoi-diem-khong-hop-le-van-ghep-passed` | ĐÃ VÁ THẬT / giữ đóng trong phạm vi đo | c38, calendar_cases và12 biến thể finish-probes; `_gio` hiện parse lịch, fullmatch, header cắt giây tại caller. Mutant lịch/offset/header/lower/upper bound đúng ca sau tái neo chữ ký mới. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | **VÁ HỜ nếu kết luận đóng cả lớp; các biểu hiện đã chỉ ĐÃ VÁ THẬT** | zero/âm GIET c44; YAML steps absent/null/integer GIET c44; REST list guard GIET c22. Trace mới13/13 nhánh gọi thật. Nhưng bool bị che uniqueness, float, alias và các biên trong bảng lớp còn mutant sống; lớp vẫn mở, **lặp lượt3 r4**, không đổi slug. |
| F11 `chan-path-chua-co-phan-chung` | ĐÃ VÁ THẬT / giữ đóng đúng phạm vi PATH | c42 lặp ENV/PATH ba chiều và chính bước chứa đường dẫn GITHUB_PATH; bỏ riêng PATH GIET c42 và ca github_path. Các vị trí khác chưa khóa được ghi F10, không nói ca PATH hiện có không chạy. |

Không phát hiện lớp sản phẩm mới có phản chứng nằm ngoài nguồn tin đã được chủ kho chấp nhận. Một lớp kiểm thử P1 còn mở. Quyết định mới đã gỡ stop V5 cũ; reviewer không tự khôi phục V5, cũng không tự cấp quyền vòng vá/lease mới.

**Kiểm hai lời khai tương đương.**

- `log_nested_after_only` vẫn SONG_SOT45/45. Phép yếu này chỉ bỏ luật nhóm lồng TRƯỚC shell; ở trạng thái tiền tố, dòng không màu đầu tiên còn phải bắt đầu `shell: `, mà `##[group]` không thể thoả nó. Nó đã làm `ok=False` trước khi luật lồng được xét. Sáu vị trí chèn nhóm của `remaining_survivors.py` cho cùng kết quả ở hai bản; đây là lập luận cấu trúc cho đúng chốt, không là lời khẳng định mọi văn bản đều đã fuzz. Ngược lại `log_nested_before_only` bỏ bảo vệ SAU shell bị c40 GIET.
- `[:i+1]` thay `[:i]` **không tương đương toàn cục**: khác ở chính run i nhắc ENV/PATH. Ca đường dẫn `ops/GITHUB_PATH_test.py` hiện có khóa đúng khác biệt: `A26_tinh_ca_buoc_i` và `mode_prior_include_current` GIET c42. Lời khai “khác biệt đó đã có ca” là đúng; không dùng nó để miễn hai vị trí run trước mới tìm được.

**Replay A10 offline.** `replay_q1.py` dùng callback REST đọc run.json/jobs.json/log đóng băng; parents/tree và workflow lấy bằng Git thật tại SHA checkout, không dùng YAML HEAD hiện tại. Artifact metadata được tái dựng từ provenance đóng băng, không phải REST artifact receipt độc lập mới. Replay được chạy lại bằng cả hai script lịch sử (cùng nội dung); `q1-details.json`, `q1-summary.json` và các output replay giữ phép đo.

| run / attempt1 | rc | checkout / ghép | SHA-256 provenance; so A10 trên parent |
|---|---:|---|---|
| 39342960764 | 0 | 13 passed,1 chuan-bi not_measured; SHA b27fe85c9e9593ddbb059808fe4347fe1bd267be; parents5618020a67709ca6f2c93138905df0aa8d9c2df6 +400589368e09ab2ee0e734b7af08b93478035503; tree857bc47e6bc5f0024e442b400819ac51286dfc55 | `5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0` — **trùng byte, 0 khác biệt** |
| 40074551995 | 0 | 22 passed,1 chuan-bi not_measured; SHA dc657149941f9db3ab2afc6fb6462ba4827bf18f | `24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b` — **trùng byte, 0 khác biệt** |

37/37 log khớp SHA256SUMS và hash/size trong provenance. Đối chiếu Q1 độc lập:37/37 job duy nhất;325 nhóm =325 REST đã chạy;345 REST ứng YAML =345 YAML;345/345 tên;325/325 cửa sổ. Tên bằng Run+header97/325. Cửa sổ duy nhất là10/325 nếu chỉ tính bước đã chạy,6/325 nếu tính mọi REST steps kể cả metadata; không nhầm metric này với điều kiện(c).

Run đầu không marker MOI; run sau8 job gate-nhanh-manh có marker nhanh_don_duoc_test not_measured/che_do_khong_xac_dinh, gate-nhanh-gop không marker. Không Gate failed, labels37/37 Ubuntu. Workflow definition vẫn not_measured. Logic giờ/tên thay trên HEAD không làm đổi hai bộ dữ liệu thật được giao. **Frozen replay passed; LIVE mới/HTTP/freshness/retention KHÔNG ĐO ĐƯỢC**, không tự nâng mốc Workflow definition.

**ĐỐI CHIẾU A1–A27.**

| tiêu chí | trạng thái | bằng chứng / giới hạn |
|---|---|---|
| A1 | passed | c01/help đủ4cờ, mutant đúngca; sai đối số rc2/summary4. |
| A2 | passed | c02 attempt2/1 failed rc12, mutant đúngca. |
| A3 | passed trong7ca | c03–c09 Linux/Windows fixture, SHA thiếu/khác/push/PR parents, mutant đúngca. Không là native Windows execution. |
| A4 | passed các vế chỉ định | c10–c15, runner0 not_run, skipped, sai marker/khác bước failed, ngoàiMOI chưa đo, import MOI động. Răng phạm vi rộng M11 còn F10. |
| A5 | passed | c16/M5 giữ not_measured và loi_khai_rest_path; mutant đúngca. |
| A6 | passed ở lỗi ghi được thử | c17 out vắng/giữ bản cũ, mutant ghi thẳng đúngca. Crash/power loss/writer cạnh tranh không đo. |
| A7 | passed ở phạm vi đo | c18 rc0/NOT_MEASURED1, c19 HTTP403/rc3/summary4 ở4endpoint, sai shape và lỗi ghi/thu; mutant đúngca. |
| A8 | passed định dạng/catalogue; **M11 chưa đủ — F10** |45/45,125/125,TU_KIEM2,TONG DAT rc0; audit127 mục đúnghạng, classifier negative rc1/TIN_DUNG_GIA/TONG DO. Có mutant bổ sung sống45/45. |
| A9 | **full command not_run; targeted partial passed/failed** | Không chạy lại --chay/heavy gate theo authority. kiem errors[]25/25, gỡentry báo25/24+test chưa đăng ký, regex nhận suite/từ chối unequal/zero/red. phan_chung được thử nhưng fixture Git signer rc128/socket denied; giữ failed bên trong, không gọi driverrc0 là A9pass. |
| A10 | frozen replay passed; LIVE mới KHÔNG ĐO ĐƯỢC | Hai provenance trùng byte;35checkout/ghép passed+2chuan-bi chưa đo,37log, bảng trên. |
| A11 | passed phần đo tại chỗ / trần theo authority mới | đúng3tệp/1312dòng; diffcheck0; doctrine10tệp/0chép; adr53/53; bare Ruff F0finding trên2tệp. Không áp lại trần1250 đã được owner nâng. |
| A12 | not_run / KHÔNG ĐO ĐƯỢC | Không ls-remote, push, connector hay nhận quyền đẩy trong review offline. |
| A13 | KHÔNG ĐO ĐƯỢC hoàn chỉnh | Đã đọc metadata đúng thread:CLI model/effort; rollout đang ghi, hash/size cuối và stdout thread.started/launcher run.json sau run thuộc người điều phối. |
| A14 | passed | c25 xác thực/ghép đúng trước negative marker, mutant đúngca; replay metadata màu cũ. |
| A15 | passed | c26 subset/mixed-color, mutant đúngca; counter cũ giữ chặn. |
| A16 | passed các ca chỉ định | c27 toàn khối minimal/nonminimal+đốichứng, mutants đúngca. Các biên run khác còn F10. |
| A17 | passed ba vế chỉ định; miền rộng thiếu răng F10 | c28–c31 envstep/envjob/args/VAR/defaults/shell; các mutant chỉ định đúngca. Miền shell và env/defaults chưa khóa đầy đủ như bảnglớp. |
| A18 | passed trong phạm vi đo | c32 nguồn/shape/SHA thiếu không ném, c34/Git thật, mutants đúngca. |
| A19 | passed | c33 cùng chữ khácjob/env hai chiều, mutants đúngca. |
| A20 | passed | c36 thiếu/thừa nhóm vàREST/YAML, mỗi vế mutant đúngca. |
| A21 | passed vế chỉ định; **F10 chưa đóng cảlớp** | c37 sai tên/name tĩnh/order; các miền tên và primitive number mới chưa khóa. |
| A22 | passed trong phạm vi đo | c38/calendar/probes, parse lịch+header cut, offset/suffix/header missing và bounds, mutants đúngca sau tái neo. |
| A23 | passed ca chỉ định; **F10 miền job vẫn thiếu** | c39 zero/multiple/expression/reusable/key matrix; alias literal valid còn mutant sống. |
| A24 | passed | c40 nested sau shell, mutant đúngca; trước shell redundant đã kiểm cấu trúc. |
| A25 | passed | c41 uses/composite, count/uses mutants đúngca; composite replay current rc0 sau sửa đường dẫn scratch. |
| A26 | passed3đốichứng ENV/PATH; **F10 miền vị trí rộng còn thiếu** | c42 và own-path case; index0/nonadjacent chưa có răng trong suite. |
| A27 | passed | c43 block bằng bước khác/skipped không marker, mutant đúngca. |

**Môi trường, lệnh và bằng chứng.** Linux x86_64, Python3.13.17 `/usr/bin/python`, PyYAML6.0.3, Git2.43.0, Ruff0.15.15, codex-cli0.164.0. Model/effort/session đọc từ `prior2/preflight.json`: originator codex_exec, provider openai, turn_context công bố gpt-6.1-sol/xhigh. Model phục vụ từng request KHÔNG ĐO ĐƯỢC. Executor Claude/cloud/họ Claude theo spec; không có runtime receipt Executor mới để tự xác minh. Không lấy GitHub submitter làm model reviewer. Chưa nhận cross_approved hoặc approval/land authority.

Sandbox thực tế workspace-write, .git read-only theo môi trường; candidate được giữ read-only bằng hành vi/snapshot. Mọi scratch/cache/TMP/bytecode policy nằm dưới .review (bytecode tắt, Ruff --no-cache), theo ngoại lệ output user giao. Catalog không có cloud_environment.environment_status; không cài dependency, không gọi mạng, secrets/LIVE, subagent, git push/commit/merge/land hoặc record-review.

| command (đều Python -B, PYTHONDONTWRITEBYTECODE=1 khi chạy Python) | rc thật / kết quả |
|---|---|
| python -B ops/ci_provenance_test.py |0;45/45,125/125,TU_KIEM2,TONG DAT (`suite.json`) |
| python -B .review/audit_mutants.py |0;125GIET+1TIN_DUNG_GIA+1SONG_SOT tựkiểm (`audit.json`,mutants/results.json) |
| python -B .review/frontier.py / frontier2.py |0 mỗi driver;33GIET,28SONG_SOT tổng;baseline45/45,mỗi mutant45ca,rawoutputs giữ riêng |
| python -B .review/prove_frontier.py / prove_last.py |0;26đốichứng HEAD0→mutant3 đúngTinHieu/tên; `frontier-counterexamples.json` |
| python -B .review/replay_prior_all.py |0driver;rc từngscript trongprior-reruns.json, bao gồm fixture/OID cũ hỏng; không suy pass hàng loạt |
| python -B .review/remaining_prior.py |0driver;12 bước córc riêng, trace c44 cũrc1 do đếm5đãstale; lỗi adapter chữ ký cũ giữ riêng |
| python -B .review/repair_legacy_anchors.py |0;5neo hiện hành GIET đúng c38/c37/c42, không nhận lỗi chữ ký `_gio(v,TS)` là kill |
| python -B .review/prior2/verify_new_cases.py |0;8baseline0 và7mutant3/DO đúngca, lần cuối `reviewer-cases-final.json` |
| python -B .review/close_prior.py |0 lần cuối;trace13/13,c44đo thật,registrynegative sửa sizefixture mới; `close-prior-final.json` |
| python -B .review/prior2/replay_q1.py (cả bộ prior1 tương tự) |0;hai replayrc0/trùngbyte/37log; q1-summary.json |
| python -B .claude/dev/packet_loop.py doctrine-scan --root . |0;10tệp/0chép |
| python -B .claude/dev/packet_loop.py adr-song --root . |0;53/53, ngoại lệ0016 theo canon |
| python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py |0;All checks passed,0finding; barelint scope2tệp |
| loi_ruff_ci() qua registry_check.py |errors[],count3; đây là pin/probe contract riêng, không dùng thay barelint |

Chạy lại các script KIỂM của cả hai lượt r4; script giống byte dùng cùng một kết quả thay vì tạo số đo giả mới (inventory hashes ở `prior-script-inventory.json`). Các renderer lịch sử `write_verdict.py`/`final_check.py` và bootstrap `prepare.py` không được phát lại để chép verdict cũ hoặc làm hỏng bố trí scratch; snapshot/run/emit dùng chức năng tương đương hiện hành. Đây là giới hạn “mọi script”: mọi phép kiểm/phản chứng, không tái tạo báo cáo cũ như bằng chứng mới.

Các lỗi hạ tầng/fixture đã giữ và giải thích: OID9e5019e thiếu rc128 (compare_current đọc r2-source.py được giao, không chứng thực Git OID nguồn); boundary/composite legacy thiếu RESTnumber/count và đường dẫn .review/composite cũ; `trace_c44` đòi5 khi giờ có13; registry negative thay chuỗi43/43 hay44/44 không còn làm đổi suite45/45; neo `_gio(v,TS)` stale làm TypeError. Đã tái dẫn xuất đường dẫn/state/neo ở scratch và đo lại phần liên quan, không sửa candidate. Không cộng các lần lỗi này vào GIET. `number_missing_tu_sinh` có đúng c44rc3 nhưng c22rc4/KeyError: **TIN_DUNG_GIA ở aggregate**; chỉ c44 là kill có thuộc tính no-throw. `job_khoa_bi_bo` hiện không còn IndexError c14 sau executor sửa assertions; targetc39 vẫn GIET.

**DANH SÁCH MUTANT VÀ HẠNG.** Mọi source bản sao, neo/thay, rc/output từngca ở JSON được chỉ. Rank GIET chỉ nhận rc3/DO:<đúng-ca>: từ TinHieuChotCa; không nhận lỗi setup hay ngoại lệ không bắt. Các dòng dưới là mục catalogue/target, không khẳng định mọi source mutation khác nhau (ví dụ A20i/A25ii chung thay đổi, khác target). Không cộng alias hoặc tái chạy thành mutant mới.

| mutant catalogue ứng viên / tự kiểm | ca đích | hạng (baseline→mutant) |
|---|---|---|
'''
for v in audit:
 rc=v['mutant']['rc']; text+=f"| `{v['name']}` | `{v['case']}` | {v['rank']} (0→{rc}) |\n"
text+='''
61 thử nghiệm frontier dưới đây có **28 survivor được báo đầy đủ**; không đổi nhãn sống trên suite thành GIET chỉ vì reviewer thêm ca ngoài suite. Cột cuối phân biệt được bằng phản chứng độc lập (và thuộc F10 trừ giới hạn nêu), hoặc thiếu tiêu chí để coi survivor là finding. `new_vs_executor` trong JSON cho biết phép thay chưa có trong hai inventory tự đột biến; các alias cũ được khai rõ.

| mutant bổ sung | hạng trên45ca | kết quả phản chứng / phạm vi |
|---|---|---|
'''
notes={
 'log_nested_after_only':'SONG_SOT nhưng chốt trước-shell dư theo cấu trúc;6/6so sánh bằng nhau;không finding',
 'dd_output_dedupe':'SONG_SOT;2mục thay1mục khi cùng path gọi2lần, trạng thái không đổi;A1–A27 không quy định dedup cardinality,không yêu cầu vá',
 'log_group_close_exact':'SONG_SOT;chỉ khác khi endgroup có hậu tố chưa có trong37log;không tự coi dạng đó là log chuẩn cần hỗ trợ',
 'job_dotall_add':'SONG_SOT;HEAD0→mutant3 ở tên suffix nhiều dòng;đã đo nhưng miền đó chưa được chứng thực bằnglogthật,không dùng riêng nó làm finding',
}
for v in front:
 name=v['name']
 if v['rank']=='GIET':detail='TinHieuChotCa đúng '+v['killed'][0]+(' (còn target khác trongJSON)' if len(v['killed'])>1 else '')
 else:detail=notes.get(name,'HEAD0→mutant3 đúng ca reviewer;F10')
 fresh='mới' if v['new_vs_executor'] else 'tái kiểm phép thay executor'
 text+=f"| `{name}` ({fresh}) | {v['rank']} | {detail} |\n"
text+='''
Ba survivor không lập finding ở bảng trên vẫn là survivor: không gọi chúng “đã giết”. `job_dotall_add` có ca phân biệt nhưng không dựa riêng vào ca nhiều dòng để đòi thêm nghĩa vụ ngoài miền đã cấp. Cũng không dùng metadata riêng lẻ hay giả định log runtime chưa đo làm bằng chứng dương. Hai bool mutant là biến thể cùng thuộc tính; không cộng thành hai lớp. Các guard shape giản lược khác đã bị kiểm bởi đúng ca như bảng GIET, không thêm test để soi gương implementation.

Đột biến lịch sử18mục cũng đã phát lại: bản raw có5HONG_NEO do đổi code,12GIET,1TIN_DUNG_GIA,1SONG_SOT baseline (19dòng kể cả baseline). Sau tái neo các mục giờ/tên/PATH: sort,uniqueness,sorttheoname,offset,bounds,đếm nhóm,đếmYAML,checktên,jobduynhất,quétcảjob,PATH,jobname/key,firstline,nameexpression đều GIET đúngca. `number_missing_tu_sinh` giữ aggregateTIN_DUNG_GIA như trên. Hai bộ readerGit chỉ chết c34 đúngchốt. Không gộp các alias này với61 thử nghiệm thành tổng mutation độc lập.

**Snapshot và giới hạn bàn giao.** Snapshot đầu/cuối băm size/SHA-256 **6763 tệp** ngoài .git/ và .review/, gồm tracked/untracked/ignored, .review-input và .codex: **0 delta**; Git HEAD/tree/status/index/diff bằng nhau, status không ignored rỗng. Danh sách ignored giữ .codex/, .review-input/, .review/. Metadata .git không được băm toàn bộ; kiểm bằng Git views. Hai snapshot chỉ chứng minh không delta quan sát giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Không có repo nguồn khác được cấp để đo. `snapshot-comparison.json`, `evidence-manifest.json` giữ bằng chứng; rollout đang chạy không được hash để giả biên nhận cuối.

Full A9/required CI/heavy gate, LIVE độc lập, remote fence/push/connector, native Windows/pwsh, composite runner thật, HTTP redirect thật, model phục vụ từng request, final rollout/launcher receipt **KHÔNG ĐO ĐƯỢC hoặc not_run như đã phân loại**. Không đổi skipped/not_run thành passed. Phần transport/assurance/land vẫn do người điều phối/Approver đối chiếu receipt sau run.

Verdict **changes_requested vì F10 P1 còn mở**. Authority mới cho phép chủ kho tiếp tục vòng vá trong phạm vi được giao; verdict này không phải lease hay quyền đẩy/merge/land. Reviewer không ghi branch Executor, không publish GitHub, không tự approve hoặc deploy.
'''
(R/'VERDICT.md').write_text(text)
print('VERDICT written',len(text.encode()),'bytes',len(text.splitlines()),'lines')
