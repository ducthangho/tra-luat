verdict: changes_requested
reviewed_sha: 9b329bfab0b38a821992a7105d479ca44bed389b
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: 9b329bfab0b38a821992a7105d479ca44bed389b
reviewed_tree: f107d82b2fd68d432f1298621d729de7ec2dd62e
packet: wp899-r4
review_round: 7
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol (CLI-published)
effort: xhigh (CLI-published)
session_id: 01a172ce-0440-7063-b4e1-20f324906cb9
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**V2 chưa đạt: P0=0, P1=1, P2=0 theo lớp. F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` LẶP, chưa đóng cả lớp.** 32 mutant mới còn sống 50/50 ca và đổi kết quả thuộc miền M4/M12 đã định nghĩa; từng mutant có phản chứng HEAD rc0 → mutant rc3 bởi `TinHieuChotCa` đúng tên. 3 survivor mới được tách riêng là P3/miền cần quyết định hoặc tương đương. Không suy lỗi của mutant thành lỗi sản phẩm hiện tại.

## Authority, preflight và phạm vi

Đối tượng là exact HEAD/tree ở đầu verdict, detached HEAD, parent `35453ff30170998ffea663801299db5876cc8e0c`. Origin `https://github.com/ducthangho/tra-luat.git`; base là ancestor (rc0). SHA-256 spec r4 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` (23860 byte), r3 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`, r2 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707`; đều khớp. Đã đọc toàn bộ r4 và các định nghĩa/mục tiêu/nghiệm thu được dẫn từ r2/r3, chỉ dẫn repository, adapter cross-review và các mục protocol áp dụng.

Write set thực tế đúng ba tệp: `.claude/dev/ci_dang_ky_test.py` +1, `ops/ci_provenance.py` +444, `ops/ci_provenance_test.py` +1289 = **1734 dòng thêm**. Registry chỉ thêm một mục MOI. Delta parent chỉ sửa test (+88/−3); sản phẩm không đổi. `git diff --check <base> HEAD` rc0. `full.patch`, `delta.patch`, `preflight6.json` giữ lệnh/rc và byte diff. `core.abbrev=7` có sẵn; clone shallow.

Áp Q1–Q12 và các quyết định checkpoint được assignment cung cấp: nâng trần/tiếp tục sau lượt 2, tiêu chí phân hạng và D01 sau lượt 5, tiếp tục một lượt sau lượt 6. Không coi 1734>1250 hoặc V5 cũ là finding. Đây là lời gọi **7/8**, còn một lời gọi dành cho connector theo assignment; không reset budget. Authority hiện là bản đóng băng user giao; lease/generation/state/ref fence, số chi thực tế và readback GitHub **KHÔNG ĐO ĐƯỢC offline**.

Gốc tin là nội dung tại SHA checkout, gồm action pin tag. Các phản chứng mới là dữ liệu hợp đồng vô hại; không tự soạn nội dung tấn công nhạy cảm hay tuyên bố chống được tác giả workflow/action có quyền sửa nội dung được tin. Không truy cập REST/LIVE, gọi subagent, push, đăng GitHub, merge, land hay deploy; nỗ lực ký commit của fixture bị sandbox từ chối được ghi ở A9. Mọi artifact được tạo trong `.review/`.

Môi trường: Linux x86_64, Python3.13.17, PyYAML6.0.3, Git2.43.0, Ruff0.15.15, codex-cli0.164.0. `runtime6.json` đọc đúng thread/cwd từ rollout `rollout-2026-10-25T11-24-27-01a172ce-0440-7063-b4e1-20f324906cb9.jsonl`. Model/effort là CLI công bố; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Executor Claude/cloud theo assignment. Sandbox thực tế workspace-write, network=false, approval=never, `.git` read-only; không khai toàn sandbox là read-only. Rollout/launcher receipt chỉ đóng băng được sau khi review kết thúc; A13 chưa hoàn tất, verdict không tự tạo `cross_approved`.

## BẢNG LỚP

Một lớp P1 lặp; D02 là ghi chú P3 mới cần quyết định miền. Cách vá chung cho F10 là mở rộng phân hoạch oracle và kiểm đầy đủ bằng chứng đầu ra, giữ source/REST/log độc lập; không sửa sản phẩm đang đúng chỉ để làm đẹp tổng mutant.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F10 — miền tên job/bước | P1 | `ops/ci_provenance_test.py:763`, `:866`; alias/tên bước Unicode, hậu tố matrix có dấu chấm chưa khóa. Chốt sản phẩm `ops/ci_provenance.py:164`, `:170`. | Survivor tương ứng ở bảng dưới; `cases7.py`, `proof7-results.json`, `proof-repairs7-results.json`. | Thêm bảng tên Unicode, hậu tố thực tế có dấu chấm, so ghép duy nhất và marker. Khóa bằng từng mutant tương ứng. Giữ tên REST literal; helper tự dựng lại tên theo sản phẩm sẽ che sai lệch. | ~8–15 |
| F10 — miền và quan hệ thời gian | P1 | `ops/ci_provenance_test.py:549`, `:818`, `:866`; c49 chỉ năm2026, c50 chưa khóa toàn bộ quan hệ lịch/cửa sổ. Chốt `ops/ci_provenance.py:176`, `:205`. | Các survivor time trong bảng dưới; đối chứng năm nhuận thế kỷ, năm biên, qua tháng/năm, sai lịch/format. | Thêm các phân hoạch vào bảng giờ hiện có; oracle kiểm timestamp hợp lệ trước quan hệ cửa sổ. Mỗi trục giữ tên/số đếm đúng. Rủi ro: làm hỏng vế a/b trước sẽ tạo răng giả cho vế c. | ~12–22 |
| F10 — nguồn REST, vị trí và chặn chế độ | P1 | `ops/ci_provenance_test.py:608`, `:763`, `:866`; các miền còn sống trong bảng mutant. Chốt `ops/ci_provenance.py:193`, `:196`, `:210`. | Metadata đã loại không cần giờ; Post không phụ thuộc number; nguồn chặn/giá trị env theo từng survivor. | Mở rộng oracle bằng các quan hệ còn thiếu; so cả ghép, danh sách marker và nguyên nhân. Mutant phải chết đúng ca, không nhờ lỗi helper/duplicate number. Rủi ro: thêm ràng buộc REST ngoài spec hoặc trộn dữ liệu metadata với bước chạy. | ~12–22 |
| F10 — nội dung/nguồn bằng chứng và cấu trúc log | P1 | `ops/ci_provenance_test.py:253`, `:846`, `:866`; c49/c50 chủ yếu chiếu trạng thái/lý do, bỏ sót miền nội dung marker/metadata. Chốt `ops/ci_provenance.py:253`, `:288`. | Các survivor dd/log trong bảng dưới; so dòng khớp, command và danh sách marker trên nhiều bước. | Kiểm đầy đủ projection được hợp đồng yêu cầu: dòng bằng chứng nhiều dòng, thứ tự/nội dung log, marker của từng bước và số bước xác thực. Đưa các quan hệ vào bảng/oracle, thêm mutant độc lập. Rủi ro: chỉ đòi Gate chung hoặc fixture tự đồng bộ với mutant sẽ che mất lỗi. | ~18–30 |
| D02 — miền `uses:` nhiều dòng, MỚI | P3 | `ops/ci_provenance.py:173`, `:174`; dùng chung phép lấy dòng đầu cho run/uses. | `name_uses_whole_value`: current và biến thể so toàn giá trị khác nhau; `cases7.py`, `proof7-results.json`; cả50 ca không phân biệt. | Owner đề xuất `ducthangho` chốt miền action reference malformed và việc từ chối/so nguyên văn. Nếu coi mọi chuỗi uses YAML thuộc miền, cần tách quy tắc run dòng đầu/uses toàn giá trị, có cặp REST đúng/sai tên. Rủi ro: tự mở rộng miền runtime chưa được chứng thực. | ~5–10 sau quyết định |

D02: chuỗi action reference chứa newline không có phép đo runner thật trong bundle; spec nói `Run <giá trị uses:>` nhưng không chốt việc nhận hay từ chối action reference malformed. Phép đo cụ thể cho `uses: './a\n./b'`, REST `Run ./a`: HEAD ghép được; biến thể so toàn giá trị không ghép được. **Đề xuất:** chủ kho chốt fail-closed cho giá trị này hoặc khẳng định so toàn giá trị; không tự biến nó thành bằng chứng tấn công ngoài gốc tin. Giữ D02 mở/P3, không tuyên bố đã xác minh GHA chạy được dữ liệu này. Nếu owner xác nhận miền gồm mọi chuỗi này, chuyển thành lỗi conformance của M12 và kiểm lại severity theo kết quả đã lưu.

## ĐỐI CHIẾU F01–F11

| lớp | kết quả trên HEAD | bằng chứng độc lập / giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG trong tập đo | c22, probes thiếu/kiểu, catalogue đúng ca; không suy Gate thiếu metadata từ ghép passed. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG các phản chứng được giao | Replay probes/r2-compare/reviewer cases r3 và boundary/composite trên fixture r4; c23/c25–27/c35/c40–43. Composite cuối dùng stdout suite thật. Giữ giới hạn gốc tin. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20 + mutant thiếu/lặp/total đổi ở jobs/artifacts. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | URL sai run/attempt/log trả404; mutant run+1 chết đúng c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG phạm vi đo | c01/c18/c19/c22; HTTP/shape/I/O/lưới cuối, output và rc lưu riêng. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24, mock redirect/network/header; endpoint thật không đo. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG bằng authority | Replay đúng13+1 và22+1; không dùng REST head lấp SHA chuan-bi. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 dùng Git/tree thật, thiếu path/nonUTF8; reader mutant và probe lịch sử. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | GIỮ ĐÓNG sản phẩm trong tập đo | c38/calendar, leap/century/min–max year/offset/fullmatch/header thiếu. Thiếu răng miền mở rộng thuộc F10. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | Các biểu hiện P1 lượt6 ĐÃ VÁ THẬT; CHƯA ĐÓNG CẢ LỚP | 25 mutant P1 lượt6 bị bắt đúng ca hiện tại; frontier6+extras có67 GIET,1 tương đương. 32 survivor P1 mới còn50/50 xanh. |
| F11 `chan-path-chua-co-phan-chung` | GIỮ ĐÓNG | c42 ENV/PATH trước/khác job/sau, mutant bỏ riêng PATH; miền nguồn/vị trí mới giữ slug F10. |
| D01 | GIỮ ĐÓNG theo quyết định chủ kho | c46/c49 phân biệt env null/vắng ở workflow và job; mutant gộp hai trạng thái bị giết. |

Lớp mở P0–P2 lượt6={F10}; **0/1 lớp cũ đóng toàn bộ**, không có lớp P0–P2 mới. Các biểu hiện mới không được đổi slug để xóa lịch sử lặp.

## A1–A27

| tiêu chí | kết quả và phạm vi |
|---|---|
| A1 | passed c01: help đủ cờ, sai đối số rc2 và dòng đếm; mutant đúng ca. |
| A2 | passed c02: lệch attempt Run failed/rc12, đối chứng đúng. |
| A3 | passed c03–09 và mutant SHA/Linux/Windows/PR; fixture Windows không là native Windows execution. |
| A4 | passed c10–15: runner0, skipped, regex đúng bước, import MOI, failure; miền bổ sung thiếu răng ở F10. |
| A5 | passed c16: Workflow definition luôn not_measured; path chỉ là lời khai REST. |
| A6 | passed c17: ghi nguyên tử, fault injection và mutant. |
| A7 | passed c18/c19: rc0/NOT_MEASURED1 và HTTP403/rc3; đúng target mutant, không lấy tổng suite thay receipt. |
| A8 | Suite50/50,255/255,2 tự kiểm,TONG DAT; M11/độ phủ **chưa đạt** do F10. |
| A9 | Đăng ký25/25, bỏ mục MOI→25/24+unregistered, regex và pin/probe đã đo. Full `--chay` **not_run** theo authority; fixture signer bị sandbox từ chối là not_measured. |
| A10 | Replay offline hai provenance byte-identical; LIVE/freshness **KHÔNG ĐO ĐƯỢC**. |
| A11 | passed diff/check/write set,Ruff2 tệp,doctrine10/0,ADR53/53; trần nâng theo assignment, báo1734. |
| A12 | not_run/not_measured: không đẩy, không mạng đo remote fence; bước đẩy phải đo riêng. |
| A13 | Chưa hoàn tất: đúng thread/model/effort/cwd đã đọc; stdout thread.started, hash rollout sau kết thúc và launcher receipt do bên vận chuyển hoàn tất sau run. |
| A14 | passed c25: env metadata mang màu không xác thực; mutant đúng ca. |
| A15 | passed c26: tập con khối không xác thực; mutant subset. |
| A16 | passed c27 và đối chứng; miền log/marker thiếu răng ở F10. |
| A17 | passed c28–31/c46/c48–50: env ba mức, đối số,prefix,defaults,shell; D01 riêng. |
| A18 | passed c32/c34: thiếu workflow/object/path/YAML/SHA không marker, không ném trong tập đo. |
| A19 | passed c33/c49: đúng job giữa nhiều job, không lấy chế độ từ job khác. |
| A20 | passed c36 count log/REST/YAML và mutant từng vế; c49 không sinh vế a, không tự coi là đã lấy mẫu. |
| A21 | passed c37/c48–50 và mutant tên; miền tên còn thiếu răng thuộc F10. |
| A22 | passed c38/calendar/mutant và c49; miền cửa sổ/lịch bổ sung còn thiếu răng thuộc F10. |
| A23 | passed c39/c47–50 duy nhất/prefix/expression; alias/suffix bổ sung ở F10. |
| A24 | passed c40/c35 nested; không ép giết biến đổi tương đương. |
| A25 | passed c41 uses/composite/count; chưa đo composite thật trên runner. |
| A26 | passed c42/c47–50 ENV/PATH trước/khác job/sau/skipped; miền bổ sung ở F10. |
| A27 | passed c43 khối khác bước, mutant đúng ca. |

## Phép đo, scope và phân hạng

Từ gốc checkout: `PYTHONDONTWRITEBYTECODE=1 python -B .review/run.py <nhãn> <command...>`. Wrapper đặt TMPDIR/TMP/TEMP/cache trong `.review/`, lưu command, rc con thật, stdout/stderr, byte và SHA-256. Mutation source là bản sao tạm, `python -B`, `CI_PROVENANCE_MA=<bản sao>`. Chỉ tín hiệu `TinHieuChotCa` của đúng ca được nhận; ngoại lệ/setup/anchor không phải giết.

| command / phép đo | rc và bằng chứng dương |
|---|---|
| `python -B ops/ci_provenance_test.py` | 0: `CA: 50/50 dat`, `DOT BIEN: 255/255 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (2 dot bien)`, `TONG: DAT`; suite.json. |
| `python -B .review/audit_mutants.py` | 0: catalogue255 GIET đúng target; tự kiểm1 TIN_DUNG_GIA và1 SONG_SOT có chủ ý; mutants/results.json giữ neo/thay/baseline/command/rc/output/hash. |
| Ruff bare: `python -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` | 0, All checks passed; riêng với contract. Bare lint scripts/tl.py not_run. |
| Ruff contract `loi_ruff_ci()` | 0, RUFF_CONTRACT3 []; checks.stdout.txt. |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0:10 tệp,0 chỗ chép doctrine. |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | 0:53 ADR/53 dòng; exemption lịch sử0016 được giữ nguyên. |
| Frontier/historical/operator/normalization/proof drivers | rc, case scope và lỗi con trong từng JSON và MUTANTS.md; không coi rc0 driver là mọi lệnh con pass. |
| A9 full registry, release/heavy gates, CI mới, connector, remote/LIVE | not_run theo assignment/môi trường; không chuyển thành passed. |

`coverage7-results.json` tái sinh seed899:250 kịch bản,189 ghép passed,61 hỏng;487 marker (74 passed,75 failed,338 chặn). Mức lấy mẫu nhỏ nhất10. Có27 job alias=key,20 tên REST dùng hậu tố trên alias, nhưng0 dãy number có gap, thời gian chỉ năm2026. Bảng thieu của c49 khóa các mục thực sự sinh; không có `ghep:a_*` trong bộ sinh (c36 kiểm riêng).

Tên script/JSON có hậu tố6 là tên producer kế thừa; các kết quả được dẫn dưới đây được lượt7 sinh lại trong `.review/`, không nhận kết quả cũ làm phép đo mới.

Replay lịch sử: `legacy6-results.json`, `legacy-cli-repaired6.json`, `legacy-after-suite6-results.json`, `remaining5-results.json`, `historical-targets6/results.json`, `normalization6-results.json`, `reanchored6-results.json`, `operators6/results.json`, `signature6-results.json`. Các producer trùng neo/thay được nối nguồn, không cộng thành mẫu độc lập. Historical mutant đã có target chạy lại exact target+baseline; frontier6 dùng target lịch sử hoặc c50 cho biểu hiện lượt6. Frontier mới chạy cho tới tín hiệu đúng; **mọi survivor mới chạy đủ50 ca**, có baseline50 ca xanh. Không tuyên bố quét mọi ngoại lệ ở mọi ca của các mutant đã có tín hiệu giết.

Raw lỗi driver được giữ: thiếu đối số reviewer_cases, thiếu thư mục extra-r4, composite cần stdout suite hiện tại; đã chạy lại đúng điều kiện. Ba neo lịch sử stale có tái neo riêng. Writer snapshot/prepare/render verdict lịch sử và tệp source mutant là hiện vật, không phải ca nghiệm thu; không chạy writer để ghi đè verdict hiện hành. Bản source r2 đi qua nguồn đóng băng do assignment cấp nếu OID thiếu trong shallow clone; không tự xác thực OID thiếu. Hai lần chạy frontier ban đầu bị ngắt rc130 để chuyển sang exact-target/stop-after-valid-kill; interrupted7.json ghi rõ, không nhận lần dở dang là pass.

**TIN_DUNG_GIA:** mutant min(number) trên mảng rỗng vẫn làm c22 rc4 `ValueError`, không được tính giết; chính mutant đó c50 rc3 đúng tên, head cả hai rc0 (extras7-results.json). Catalogue tự kiểm tín dụng giả giữ riêng. Các ngoại lệ toán tử ngoài ca đích ở operator-errors6-results.json không được cộng giết; GIET+NEM giữ cả hai loại bằng chứng. Lỗi signer ở fixture registry là thiếu capability, không phải pass A9 full và không là hồi quy sản phẩm.

## Replay A10 offline

`replay.json`, `prior2/q1-summary.json`, `prior2/q1-details.json`, `a10checks6-results.json`:37/37 log khớp SHA256SUMS và hash/size provenance đóng băng. Hai workflow không có env null ở workflow/job. Hai provenance mới giống từng byte với A10 trên52e9573: **0 khác biệt cần giải thích**.

| run / attempt | Run | Checkout / ghép | Gate và marker MOI | SHA-256 provenance |
|---|---|---|---|---|
|39342960764 /1|passed|13 passed b27fe85… +1 chuan-bi not_measured; ghép13/14|14 Gate not_measured,0 failed;0 marker MOI|`5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0`|
|40074551995 /1|passed|22 passed dc65714… +1 chuan-bi not_measured; ghép22/23|23 Gate not_measured,0 failed;8 gate-nhanh-manh nhanh_don_duoc not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker|`24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b`|

Labels đều ubuntu-latest; Workflow definition vẫn not_measured. Replay không đo REST/LIVE hiện tại, hạn giữ log, Windows/pwsh thật, PR synthetic merge thật, composite thật hoặc action đổi môi trường; không dùng replay thay freshness/receipt cuối cùng.

## Mutant mới còn sống

Mỗi dòng P1:50/50 ca repository xanh; `python -B .review/cases7.py <ID>` với CI_PROVENANCE_MA trỏ HEAD rc0, trỏ bản sao mutant rc3 `DO:<ID>:`. Neo/thay, source và đầy đủ command/output trong frontier7*/results.json và proof*.json. Các mutant chỉ là dữ liệu; executor tự tái dẫn xuất và đo trên cây thật.

| mutant | hạng | bằng chứng / quyết định |
|---|---|---|
|job_alias_unicode_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|name_explicit_unicode_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|name_uses_whole_value|P3 / D02|uses nhiều dòng; xem quyết định đề xuất D02 bên dưới|
|time_same_year|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_same_month|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_century_leap_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_year_9999_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_year_0001_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_clock_only_compare|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_whitespace_strip|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|time_invalid_century_accept|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|rest_metadata_time_required|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|rest_filter_post_number_order|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|mode_env_present_values_only|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|mode_env_empty_key_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|mode_env_unicode_key_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|mode_prior_skip_uses|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|mode_prior_strip_empty_run|P3 / tương đương|các giá trị falsy safe YAML không chứa GITHUB_ENV/PATH; không ép giết|
|dd_first_match_lines_only|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_last_match_lines_only|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_blank_output_lines_remove|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_no_output_final_newline|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_dedup_output_lines|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_sort_match_lines|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_wrong_lenh_first_call|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|dd_step_dedup_paths|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_output_ignore_indented_blank|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_empty_metadata_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_second_shell_reject|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_output_drop_group_lines|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_require_output_nonempty|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_require_metadata_no_ansi|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_color_run_not_contains_shell|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|
|log_header_full_timestamp_required|P3 / tương đương ở đầu ra công khai|header không có timestamp hợp lệ đều hỏng vế c trước khi sinh marker|
|job_suffix_no_dot_pure|P1 / F10|HEAD0 → mutant3 đúng TinHieuChotCa; bổ sung phân hoạch/khẳng định tương ứng trong BẢNG LỚP.|

Các survivor tương đương kế thừa: `env_only_keys_str`, `log_nested_after_only`/`nested_only_after_shell` (cùng biến đổi ngữ nghĩa) có quyết định đề xuất owner `ducthangho`: giữ nguyên sản phẩm, không ép giết mutant tương đương. `env-equivalence6-results.json` kiểm16 loại khoá safe YAML kèm lập luận miền; `equivalence.json` kiểm6 vị trí nhóm lồng,753/753 endgroup trên37 log và lập luận cấu trúc. `equivalence-new7-results.json` kiểm15 giá trị run trước và8 dạng header, kèm lập luận. `mode_prior_strip_empty_run` và `log_header_full_timestamp_required` tương đương ở miền/đầu ra công khai như bảng trên; không tự nhận mọi trường nội bộ bằng nhau. D02 giữ nợ miền có tên, owner và hướng xử lý; chưa là quyết định runtime của owner.

[**MUTANTS.md**](MUTANTS.md) liệt kê TỪNG mutant của catalogue, historical/frontier, toán tử, normalization và đột biến tự thêm, kèm kết quả thật, scope/target và hạng finding. `inventory7.json` giữ dữ liệu bảng. GIET là kết quả phép đo, không là một finding P1 còn mở. Không cộng các lần đo trùng hoặc ba neo hỏng thành đột biến được giết.

## Read-only và bàn giao

`snapshot-start.json`, `snapshot-end7.json`, `snapshot-comparison7.json` băm tracked, untracked và ignored ngoài `.review/`, kiểm HEAD/tree/diff/index. Không có delta quan sát được; git status sạch. Chỉ chứng minh hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên trong toàn lịch sử. Repo nguồn ngoài checkout không thuộc phạm vi quan sát. Các writer test đã kết thúc trước manifest evidence cuối; manifest giữ path/size/hash, không tự chứng nhận receipt/transport sau khi phiên kết thúc. Verdict không cấp quyền ghi branch, approve/land hay mở thêm lượt Codex.
