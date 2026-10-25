from pathlib import Path
import json
R=Path(__file__).resolve().parent
header='''verdict: changes_requested
reviewed_sha: 52e9573d0bd401a629a031a9c32df7bfd17c27c1
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 52e9573d0bd401a629a031a9c32df7bfd17c27c1
reviewed_tree: 64e23a976f261ecdc6ab3535f6561536df3dc765
packet: wp899-r4
review_round: 2
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a1715b-6eec-7b43-96a0-0ffa85addf15
execution_surface: codex_cli
transport: machine
model_reviewer_identity: openai_codex/gpt-6.1-sol/01a1715b-6eec-7b43-96a0-0ffa85addf15 (CLI-published)
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**P0=0, P1=1, P2=0, P3=0, đếm theo lớp. F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` LẶP LỚP ở lượt 2 r4 ⇒ DỪNG HẲN theo V5.** F09 và F11 đã vá thật trong phạm vi đo; bốn biểu hiện F10 được chỉ ở lượt 1 cũng đã có răng, nhưng lớp fixture định danh bước còn hai chốt dạng độc lập chưa được kiểm. Hai mutant mới sống qua toàn bộ 44 ca. Không có lỗi sản phẩm mới được chứng minh trên HEAD; finding P1 là thiếu răng M11 trên các chốt M12 đang được sản phẩm giữ đúng. Không đổi slug thành F12 để né V5; không tự mở vòng vá.

**Preflight và authority.** Assignment là `.review-input/prompt.md`; spec r4 đã đọc trọn, 23.860 byte, SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`, khớp. Spec kế thừa r3 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f` và r2 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` cũng khớp; đã đọc các mục được dẫn cùng lịch sử hai verdict r3 và verdict r4 lượt 1. Giữ Q1–Q12, giới hạn nguồn tin và trần được giao; không coi chúng là finding.

Origin `https://github.com/ducthangho/tra-luat.git`, detached HEAD đúng SHA/tree đầu tệp; parent là `ca11a6f1a7eb5286eeb6efc730d99beb33e2dcd1`. Baseline nghiệm thu bất biến `ba222ffd1615f0d74b59985b9612f725211b62f5` là ancestor, rc0. Kho được cấp shallow (`true`); không suy đã có mọi ref/lịch sử. Numstat từ baseline: `.claude/dev/ci_dang_ky_test.py` 1/0, `ops/ci_provenance.py` 444/0, `ops/ci_provenance_test.py` 805/0: **đúng 3 tệp, 1250 dòng thêm, hết dư**. Mục MOI đúng một dòng và regex bằng mục tiền lệ. `git diff --check <base> HEAD` rc0, `core.abbrev=7` đã có. `preflight.json`, `full.patch`, `delta.patch` giữ lệnh/rc và bytes diff.

Đây là lời gọi 2/8 của r4 theo assignment. Generation riêng của r4, freshness lease/state/remote refs, lịch sử chi thực tế, nguồn gốc Git OID r3 không có trong clone và authority GitHub **KHÔNG ĐO ĐƯỢC offline**; không mượn generation 2 của r3. Không gọi mạng, GitHub, LIVE, subagent, commit, push, merge hoặc land.

**Môi trường và phạm vi bằng chứng.** Linux x86_64, Python 3.13.17 `/usr/bin/python`, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15, codex-cli 0.164.0. `preflight.json` trích đúng thread từ `/root/.codex/sessions/2026/10/25/rollout-2026-10-25T04-39-41-01a1715b-6eec-7b43-96a0-0ffa85addf15.jsonl`: originator `codex_exec`, provider OpenAI, turn_context công bố model/effort trên. Model phục vụ từng request KHÔNG ĐO ĐƯỢC. Executor Claude/cloud/họ Claude theo spec, chưa có runtime receipt Executor để tự xác minh. Rollout đang được ghi; A13 cần điều phối lấy size/hash sau khi writer kết thúc cùng stdout thread.started/run.json của đúng lượt. Không tự nhận `cross_approved` hoặc approval/land authority.

Skill `cross-review` được áp dụng. Sandbox thực tế `workspace-write`; candidate được giữ read-only bằng hành vi và snapshot, `.git` read-only. Catalog không có environment_status. Không chạy doctor/chuan-bi/cài dependency trong assignment offline. `codex --version` rc0 kèm cảnh báo không tạo được PATH alias trên filesystem read-only. Mọi hiện vật reviewer tạo nằm trong `.review/`; wrapper `python -B .review/run.py <nhãn> <command...>` đặt `PYTHONDONTWRITEBYTECODE=1`, TMPDIR/TMP/TEMP/cache vào đó, ghi rc con thật và hash/size stdout/stderr. Driver thu thập rc0 không biến các ca con đỏ hoặc lỗi setup thành pass.

**BẢNG LỚP — một lớp còn mở, hai biểu hiện.** Nguồn F10 là verdict r4 lượt 1 trên `ca11a6f1a7eb5286eeb6efc730d99beb33e2dcd1`. Cùng nguyên nhân: fixture ghép do `wf_tu`/`buoc_rest`/`g1` dựng giữ một số chiều dạng luôn hợp lệ, nên bỏ đúng chốt M12 mà suite vẫn xanh. C44 thêm malformed phần tử nhưng vẫn luôn giữ container YAML `steps` là list và không thử number không dương. Đây là tiếp diễn F10 về fixture định danh bước, không phải F09 về xác thực lịch, F02 về nguồn lời gọi hay F08 về reader Git. Một biểu hiện chỉ sửa REST; biểu hiện YAML là thiếu kiểm thử no-throw, không khai thành cuộc tấn công vượt giới hạn nguồn tin tại SHA.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| **F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` — LẶP LỚP** | **P1**, M11 chưa khóa đầy đủ M12 | `ops/ci_provenance_test.py:582`–`:593`, DOT_BIEN `:699`–`:702`; chốt sản phẩm `ops/ci_provenance.py:192` và `:194` | `shape-zero-audit.json`: `_so(s.get("number"), 1)` → `_so(s.get("number"), 0)` vẫn **44/44 rc0**, cả c44 rc0. Ca độc lập `rest_number_zero`: baseline rc0/steps_rest_sai_dang/không marker; mutant **rc3, DO:rest_number_zero:** do TinHieuChotCa, ghép và marker chuyển sai thành passed. `shape-audit.json`: bỏ riêng ` or type(sy) is not list` cũng **44/44 rc0**. Ca `yaml_steps_absent/null/integer`: baseline rc0/not_measured, mutant **rc3/DO đúng ca** vì vi phạm tính chất không ném (TypeError ở công cụ); không tính lỗi vô can như giết. | Ở c44, mở vector REST number=0/âm sau `buoc_rest`; thêm vector YAML thiếu/null/non-list, giữ `w_rest` chuẩn để helper không sửa hoặc ném trước chốt. Khẳng định reason/no marker/no-throw, và đối chứng hợp lệ ghép passed. Thêm từng neo/thay mutant ở bảng DOT_BIEN, đòi đúng c44 ném TinHieuChotCa. Không cần vá sản phẩm hiện đúng. Rủi ro: đổi number làm lệch thứ tự/trùng số rồi chết ở chốt khác; helper dựng lại state; bắt mọi lỗi setup thành tín hiệu chốt. Chỉ biến ngoại lệ thành assertion khi no-throw chính là tính chất ca đích kiểm. | Khoảng **6–10 dòng logic** nếu tham số hóa c44 và thêm hai mutant; chưa áp, chưa cam kết numstat. Hiện hết dư: phải thu gọn trong write set hoặc có authority mới. **V5 không cấp vòng vá tiếp; HINT chỉ phục vụ checkpoint.** |

Phép tái hiện (từ gốc kho, TMPDIR/cache qua wrapper):

```
python -B .review/run.py shape-zero python -B .review/shape_audit.py
python -B .review/run.py shape-containers-final python -B .review/shape_audit.py --containers
CI_PROVENANCE_MA="$PWD/.review/shape-mutants/rest_number_cho_zero.py" PYTHONDONTWRITEBYTECODE=1 python -B .review/shape_audit.py rest_number_zero
```

Hai driver đầu rc0, xem rc từng ca trong JSON; lệnh cuối rc3/DO:rest_number_zero do assertion thật. Bản sao mutant số 0 SHA-256 `233eb700b0765bddeb166332e28a6c429f15e3bd5fe5357eaebff47c4a114fae`; mutant container `ae252dd457210c0e7bdefe049bf7db14af2bed6e53f99001f7e70fa39f538b9c`. Không sửa branch Executor. `c44-trace.json` đo **5/5 nhánh c44 thật sự gọi công cụ và assert**, không có ca return sớm; không báo thêm một P2 “ca có mặt mà không đo”. Hai chiều thiếu được chỉ ra ở trên khác các nhánh đã có răng.

**ĐỐI CHIẾU LƯỢT TRƯỚC / F01–F11.** Giữ stable slug và lịch sử; “giữ đóng” chỉ trong phạm vi đo được, không là bảo đảm mọi input.

| lớp | kết luận | phép đo độc lập trên HEAD |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG | c22 + mutant F01 đúng ca; probes Run thiếu/kiểu sai, steps và check_run_url lạ, bool/newline, collection envelope: không nâng mốc thiếu thành passed. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG | Mỗi bộ r3 lượt 1/2 có sáu ca reviewer rc0 sau khi emitter có stdout suite thật. Hai cơ chế r2 passed → HEAD not_measured; tám collision mỗi bộ đều không marker. Composite và boundary đã dựng lại trên steps REST hợp lệ, ghép passed ở boundary nhưng không xác thực khối; Q8 count/uses chặn composite. c23/c25–c27/c35/c40/c41/c43 và mutant đích có răng. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20/probes jobs/artifacts: thiếu/trùng/total đổi/underreported/short page, mutant từng chốt GIET c20. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | Route run/jobs/artifacts khác và log ID lạ trả404; attempt đọc state; hai mutant run+1 GIET c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG trong phạm vi đo | c01/c19/c22, HTTP403 ở bốn endpoint, thân run list/null/string, lỗi ghi và lưới cuối; mutant summary/projection GIET đúng ca. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24/redirect error và token-header mutants GIET đúng ca, dùng mock offline, không gọi credential/mạng thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG bằng authority | Replay đúng Checkout13+1 và22+1, không bịa SHA cho chuan-bi không checkout. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 Git reader thật trên tree tạm: đúng byte, thiếu path, non-UTF8. Hai mutant Git từ mỗi bộ r3 chỉ chết c34rc3/DO:c34,43 ca khác xanh; không lấy nhãn CHECK_OUTPUT của script làm kết luận. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | **ĐÃ VÁ THẬT** | calendar_cases.py: cả sáu giá trị sai đều rc0/not_measured/no marker. verify_new_cases.py: invalid_calendar baseline rc0; nới offset/dùng REST khi thiếu header bị giết đúng c38 và ca reviewer. calendar-extra.json kiểm năm0000, leap2024/2000, nonleap2026/1900, min/maxyear, phần thập phân 10.000 chữ số, whitespace và cửa sổ đảo; không ném, kết quả theo dạng được phép. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | **VÁ HỜ ở cấp đóng lớp; LẶP LỚP — P1** | Bốn biểu hiện cũ sort/duplicate/first-line/expression-name đều GIET đúng c37 và đúng ca reviewer. C44 bốn mutant mới đều GIET c44. Nhưng hai chốt độc lập khác vẫn không có răng: bảng lớp và hai survivor trên44 ca. |
| F11 `chan-path-chua-co-phan-chung` | **ĐÃ VÁ THẬT** | c42 đo ENV và PATH cho đứng trước/cùng job, khác job, đứng sau. Bỏ riêng PATH GIET c42 và github_path, baseline cả hai rc0. |

U={F09,F10,F11} ở lượt 1; đóng thật F={F09,F11}: **2/3 (66,7%)**. Lớp mới=0; lớp còn mở/lặp=1 với hai biểu hiện. Bốn biểu hiện cũ F10 đã đóng không đủ đóng toàn lớp; tỷ lệ không thay V5.

**Phản chứng cũ, sửa giàn và ranh giới nguồn tin.** Đã chạy lại các script đo lượt 1: preflight/snapshot, prepare/run_old, calendar_cases, new_probes_r4, extra_mutants_r4, verify_new_cases/reviewer_cases_r4, audit_mutants, classifier_negative, registry_check, replay_q1, q1_time_detail; cùng scripts r3 trong old1/old2. Bản sinh verdict và kiểm cuối được tái dẫn xuất cho SHA của lượt này (`write_verdict.py`, `final_check.py`), không chép verdict hoặc assertion SHA cũ làm kết luận mới.

Giữ evidence các lần setup hỏng: lượt run_old đầu chạy trước suite làm emitter thiếu stdout; lượt sau suite, cả12 ca đúng tên đều DAT. Hai r4_compare nguyên bản rc1 vì object `9e5019e...` không có trong clone. Bản current dùng r2-source.py đã giao và thêm steps[] hợp lệ; nguồn cũ là bytes được giao, **không xác thực được OID Git cũ**. Boundary nguyên bản rc3 vì fixture r3 lệch số bước, không dùng làm finding; bản current chỉ giữ workflow cho đúng bước đang kiểm, ghép passed rồi assertion no-marker đạt. Composite current thêm setup REST/YAML nhất quán; hai dạng outer/no-outer còn được kiểm ở new_probes_r4 và c41. Bản thống kê glob cũ đo0 log; đã đổi rglob và đo đủ37. Ba neo giờ cũ HONG_NEO sau đổi _gio; finish_probes.py tái neo vào `a <= h <= z`/header parse mới, cả ba bị giết c38. Không coi HONG_NEO hay lỗi thiếu fixture là survivor.

`old1/probes.json` và `old2/probes.json` mỗi bản85 nhóm; `old2/new-probes.json` sau rglob đo37 log/325 nhóm Run/226 khối hợp lệ, không nested metadata, không CRLF/closing-suffix thật. `new-r4-probes.json` có metadata/mixed-color/collision/composite, skipped xen giữa, missing/bool/duplicate numbers, tên lạ, header thiếu/sai lịch, continue-on-error. Dữ liệu giờ dùng datetime naive UTC đã cắt microsecond=0; cả REST và header cùng dạng Z, không trộn aware với naive. Header có whitespace ngoài grammar bị không nhận nhóm rồi vế(a) hỏng, không ném; không coi đó là ca đo riêng vế(c).

Giữ `gioi_han_khai`: workflow/script/action tại SHA checkout, kể cả action pin tag, là gốc tin. Phản chứng composite cũ là regression theo Q8, không khai tác giả action sửa output là cuộc tấn công ngoài giới hạn đã duyệt. Không tự soạn hay thử nội dung tấn công nhạy cảm.

**A10 replay và giới hạn LIVE.** `replay_q1.py` tự kiểm tên/job/thứ tự/giờ từ raw log bằng oracle riêng, dùng Git thật cho workflow/parents/tree và callback REST chỉ đọc dữ liệu đóng băng. SHA256SUMS37/37 và hash/size37/37 log khớp provenance. Cả37 job labels Ubuntu; 345/345 tên,325/325 cửa sổ cùng vị trí; nhóm Run325=REST đã chạy325, REST ứng YAML345=YAML345, job ghép duy nhất37/37. Tên bằng Run+header97/325. Số cửa sổ duy nhất nếu chỉ tính bước đã chạy là10/325; số6/325 của spec tính cả metadata REST (đã phân biệt ở lượt1), không dùng metric này thay vế(c).

| run / attempt1 | rc replay | Checkout / ghép | provenance SHA-256, trùng byte A10 |
|---|---:|---|---|
| 39342960764 | 0 | 13 passed,1 chuan-bi not_measured; SHA b27fe85c9e9593ddbb059808fe4347fe1bd267be, parents5618020a67709ca6f2c93138905df0aa8d9c2df6 +400589368e09ab2ee0e734b7af08b93478035503, tree857bc47e6bc5f0024e442b400819ac51286dfc55 | `5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0` |
| 40074551995 | 0 | 22 passed,1 chuan-bi not_measured; SHA dc657149941f9db3ab2afc6fb6462ba4827bf18f | `24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b` |

Run đầu không marker MOI; run sau tám gate-nhanh-manh có nhanh_don_duoc_test not_measured/che_do_khong_xac_dinh, gate-nhanh-gop không marker. Không Gate failed. Workflow definition vẫn not_measured. Đây là **frozen replay passed**; LIVE độc lập, HTTP receipts/freshness/retention **KHÔNG ĐO ĐƯỢC** trong review offline, không dùng YAML tại checkout để nâng mốc Workflow definition.

**ĐỐI CHIẾU A1–A27.**

| tiêu chí | trạng thái | bằng chứng và giới hạn |
|---|---|---|
| A1 | passed | c01/help đủ4 cờ, thiếuattempt mutant GIET; sai đối số rc2/summary4. |
| A2 | passed | c02 attempt2 so1 failed/rc12, mutant đúng ca. |
| A3 | passed trong7 ca chỉ định | c03–c09/Linux/Windows fixture/SHA thiếu/khác/push/PR parents, mutant đích GIET; không là native Windows execution. |
| A4 | passed các ca chỉ định | c10–c15, runner0 not_run, skipped, marker sai/khác bước failed, ngoàiMOI chưa đo, MOI import động; mutant đúng ca. |
| A5 | passed | c16 giữ WD chưa đo, REST path chỉ lời khai; mutant path⇒passed GIET. |
| A6 | passed | c17 lỗi ghi giữa chừng: không out nửa vời, có/không bản trước; mutant GIET. |
| A7 | passed | c18/c19; summary NOT_MEASURED1, REST403 rc3 và summary4, mutants đúng ca. |
| A8 | passed định dạng/số đếm; **M11 còn F10** | Suite44/44,99/99,TU_KIEM2,TONG DAT rc0; audit riêng99GIET; false-credit selftest đúng loại. Hai chốt định danh khác vẫn thiếu răng. |
| A9 | **failed command / full acceptance KHÔNG ĐO ĐƯỢC** | --chay rc1, ĐĂNG KÝ25/25, launcher4/4, Ruff contract3/3 rồi fixture Git commit128 do signer loopback socket bị cấm. Normal registry25/25; bỏ mục⇒test sống chưa đăng ký. Chưa chạy trọn nhánh chay; không bypass signer. Evidence Executor giữa hai SHA không thay gate exact HEAD. |
| A10 | frozen replay passed; LIVE KHÔNG ĐO ĐƯỢC | Hai run đúng hash/byte,37 log; không gọi API mới. |
| A11 | passed | 3tệp/1250 dòng thêm, diff-check0, doctrine10tệp/0chép, adr53/53, bare Ruff F0finding. Ruff lint tách khỏi pin/probe contract3/3. |
| A12 | KHÔNG ĐO ĐƯỢC | Offline không hỏi remote/push/connector; không có quyền đẩy. |
| A13 | pending / KHÔNG ĐO ĐƯỢC hoàn chỉnh | Metadata CLI đúng thread đã đọc; final rollout hash,size/run receipt sau khi writer kết thúc thuộc điều phối. |
| A14 | passed | c25 metadata màu, fixture ghép passed; mutant đúng ca. |
| A15 | passed | c26 mixed-color/subset, mutant đúng ca. |
| A16 | passed | c27 toàn khối tối giản và đối chứng; mutant đúng ca. |
| A17 | passed | c28–c31 env step/job/workflow, defaults/shell/VAR, args, đối chứng; mutants đúng ca. |
| A18 | passed | c32 nguồn thiếu/object/path/YAML/SHA chưa đo không marker/không ném; c34 readerGit thật, mutants đúng ca. |
| A19 | passed | c33 cùng chữ khác job/env đúng vị trí, hai mutants đúng ca. |
| A20 | passed | c36 hai vế số nhóm/sốYAML, mỗi vế một mutant. |
| A21 | passed các vế chỉ định; **F10 chưa đóng rộng** | c37 tên lệch/name nguyên văn, bốn biến thể cũ F10 có răng; numeric-bound/container chưa đo. |
| A22 | passed | c38 và calendar probes, ba neo giờ hiện hành, offset/header/calendar mutants GIET đúng c38. |
| A23 | passed các vế chỉ định; **F10 còn phần dạng** | c39 zero/multi-key/expression/reusable/matrix-prefix; mutants GIET; YAML steps thiếu/non-list chưa có ca sẵn. |
| A24 | passed | c40 nested nhóm, ghép passed nhưng không marker; mutant GIET c40. |
| A25 | passed | c41 uses/composite có/không bước sau, count và uses mutants GIET đúng ca. |
| A26 | passed | c42 lặp3đối chứng cho cảENV/PATH; bỏPATH GIET c42. |
| A27 | passed | c43 khối của bước khác/skipped; mutant GIET c43. |

**Sổ lệnh và rc.** Mọi lệnh Python dưới chạy với -B và bytecode tắt qua run.py; mỗi nhãn có `<nhãn>.json`, stdout/stderr nguyên văn/hash/size. “rc0 driver” chỉ xác nhận đã thu dữ liệu.

| nhãn | command con | rc / bằng chứng dương |
|---|---|---|
| suite | python -B ops/ci_provenance_test.py | 0;44/44,99/99,TU_KIEM2,TONG DAT |
| audit | python -B .review/audit_mutants.py | 0;101 mục,99GIET +1TIN_DUNG_GIA chủ ý +1SONG_SOT chủ ý |
| calendar / new-probes | python -B .review/calendar_cases.py / new_probes_r4.py | 0 mỗi driver;6 ca lịch sai bị chặn; shape/boundary variants trong JSON |
| extra-r4-original | python -B .review/extra_mutants_r4.py | 0 driver;baseline44/44,13GIET/2aggregateTIN_DUNG_GIA/3HONG_NEO; xem phân hạng đích bên dưới |
| finish-probes | python -B .review/finish_probes.py | 0;3neo giờ tái dẫn xuất GIET c38,12/12 calendar mới đúng mong đợi |
| reviewer-cases-r4 | python -B .review/verify_new_cases.py | 0 driver;8 baseline rc0,7 mutant rc3 đúng ca reviewer |
| shape-zero | python -B .review/shape_audit.py | 0 driver;mutant44/44 sống;ca độc lập0→3đúng assertion |
| shape-containers-final | python -B .review/shape_audit.py --containers | 0 driver;YAML list guard44/44sống;REST list guardGIET c22;ca no-throw độc lập0→3 |
| c44-trace | python -B .review/trace_c44.py | 0;5/5nhánh gọi thật/khẳng định thật |
| classifier | python -B .review/classifier_negative.py | 0 driver;main rc1,TIN_DUNG_GIA,DOT_BIEN0/1,TONG DO |
| old-cases-rerun | python -B .review/run_old.py | 0 driver;12ca reviewer rc0;missingOID/fixture cũ giữ riêng, không tính pass |
| old1/2-compare-current | python -B .review/old{1,2}/r4_compare_current.py | 0 mỗi driver;2cơ chế r2passed→HEADnot_measured,8collision mỗi bộ |
| old2-boundary/composite-current | python -B .review/old2/{boundary_current,composite_current}.py | 0 mỗi ca;DAT đúng tên |
| old1/2-probes,old2-new-probes-current | python -B .review/old{1,2}/probes.py / old2/new_probes_current.py | 0;85nhóm mỗi bộ,37full logs |
| old1/2-extra | python -B .review/old{1,2}/extra_mutants.py | 0 driver;2mutant mỗi bộ,43ca xanh/c34rc3đúng chốt |
| registry | python -B .review/registry_check.py | 0 driver;25/25,thiếuentrybịbắt,regex nhận suite/từ chối bad;phan_chung Git128 lưu rawstderr |
| a9 | python -B .claude/dev/ci_dang_ky_test.py --chay | 1;fixture signer lỗi trước khi chạy trọn |
| replay-q1,time-detail | python -B .review/replay_q1.py / q1_time_detail.py | 0;hai provenance trùng byte,37log đúng |
| doctrine,adr,ruff | packet_loop.py doctrine-scan/adr-song; ruff check --no-cache --select F hai tệp | 0 mỗi command;positive evidence ở bảng A11 |

**DANH SÁCH MUTANT VÀ HẠNG.** Audit từng mutant ứng viên chạy baseline cùng ca trước, rồi mutant bản sao; chỉ rc3 với DO:<đúng-ca>: do TinHieuChotCa được tính GIET. Neo/thay nguyên văn, command, rc và raw output nằm `mutants/results.json`. Không cộng các alias/tái chạy thành mutant khác nhau.

| mutant ứng viên / tự kiểm | ca đích | rc baseline → mutant | hạng |
|---|---|---|---|
'''
rows=json.loads((R/'mutants/results.json').read_text())
for row in rows:
    header+=f"| `{row['name']}` | `{row['case']}` | {row['baseline']['rc']} → {row.get('mutant',{}).get('rc','?')} | {row['rank']} |\n"
header+='''
99/99 mutant nghiệp vụ GIET đúng ca; hai tự kiểm lần lượt TIN_DUNG_GIA và SONG_SOT chủ ý. Chi tiết18 mutant reviewer lượt1 dưới đây dùng ca đích theo tính chất ở suite hiện hành. Với các mutant có lỗi ở ca KHÁC, ghi riêng phân hạng tổng hợp; không lấy lỗi khác ca làm bằng chứng giết.

| mutant reviewer lượt1 | ca đích hiện hành | hạng đích / ghi chú |
|---|---|---|
'''
targets={'sort_bi_bo':'c37','kiem_number_bi_bo':'c37','sap_xep_theo_ten':'c37','gio_nhan_offset':'c38','gio_thieu_header_lay_rest':'c38','gio_bo_can_duoi':'c38','gio_bo_can_tren':'c38','a_bo_dem_nhom':'c36','a_bo_dem_yaml':'c36','b_bo_ten':'c37','d_lay_dau':'c39','env_quet_ca_job':'c42','env_bo_PATH':'c42','number_missing_tu_sinh':'c44','job_ten_name_bi_bo':'c39','job_khoa_bi_bo':'c39','ten_run_lstrip':'c37','ten_name_khong_kiem_bieu_thuc':'c37'}
adapt={r['name']:r for r in json.loads((R/'adapted-time-mutants.json').read_text())}
original={r['name']:r for r in json.loads((R/'extra-r4/results.json').read_text())}
for name,prefix in targets.items():
    row=adapt.get(name,original.get(name))
    if 'cases' in row and isinstance(row['cases'],list):
        case=next(c for c in row['cases'] if c['case'].split('_')[0]==prefix)
    else:
        data=json.loads((R/f'extra-r4/{name}.stdout.txt').read_text())
        case=next(c for c in data if c['case'].split('_')[0]==prefix)
    assert case['rc']==3 and case['output'].startswith('DO:'+case['case']+':')
    note='GIET, rc0→3/DO đúng ca'
    if name in ('number_missing_tu_sinh','job_khoa_bi_bo'):
        note+='; aggregate TIN_DUNG_GIA vì '+('c22rc4/KeyError number' if name=='number_missing_tu_sinh' else 'c14rc4/IndexError')
    if name in adapt:note+='; tái neo giờ hiện hành'
    header+=f"| `{name}` | `{case['case']}` | {note} |\n"
header+='''
`number_missing_tu_sinh`: đúng như cần tự kiểm, c44 GIET bởi TinHieuChotCa no-throw; c22 ném KeyError nên aggregate của script cũ là TIN_DUNG_GIA. Hai kết luận có phạm vi khác nhau, không gọi c22 là giết đúng chốt. `job_khoa_bi_bo` tương tự có c39 GIET thật và một lỗi vô can c14. Baseline control luôn44/44; nhãn SONG_SOT của baseline không là mutant.

| mutant bổ sung lượt2 | ca đích/phạm vi | hạng |
|---|---|---|
| `rest_number_cho_zero` | toàn44 ca đều0; reviewer rest_number_zero baseline0→3/DO đúng tên | **SONG_SOT trên suite ứng viên**, F10; GIET khi thêm ca reviewer |
| `yaml_steps_bo_list_guard` | toàn44 ca đều0; reviewer YAML absent/null/integer baseline0→3/DO đúng tên | **SONG_SOT trên suite ứng viên**, F10; GIET khi thêm ca reviewer no-throw |
| `rest_steps_bo_list_guard` | c22 baseline0→3/DO:c22;43ca khác0 | GIET c22; chốt đã có răng, không là finding |
| `git_ignore_sha`, `git_always_unavailable` (mỗi bộ r3) | c34baseline0→3/DO:c34;43ca khác0 | GIET, alias hai mutant F08, không cộng thêm vào99 |

**Giới hạn và bàn giao.** A9 full không đo trọn vì môi trường signer; LIVE độc lập A10, A12/A13, CI/required-check status exact HEAD, Windows/pwsh native, API/redirect thật, runner composite thật và transport/identity receipt cuối KHÔNG ĐO ĐƯỢC. Full runtime/release gates not_run; không có reviewer check nào được tự coi skipped là passed. Không biến các thiếu quan sát ấy thành pass hoặc finding sản phẩm ngoài bằng chứng. Không đề nghị gỡ guard để đo.

Kết luận nội dung changes_requested vì một lớp P1 F10 lặp ở lượt2r4. **V5: DỪNG HẲN packet, không tiếp tục vòng vá hiện hành; bàn giao người điều phối/chủ kho.** HINT không phải quyền thực hiện. Reviewer không đăng GitHub, cấp lease, gọi record-review, nâng trần, approve/merge/land/deploy hoặc gọi LIVE.
'''
(R/'VERDICT.md').write_text(header,encoding='utf-8')
print('Wrote verdict',len(header.encode()),'bytes')
