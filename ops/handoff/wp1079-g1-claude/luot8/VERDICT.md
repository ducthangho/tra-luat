verdict: changes_requested
reviewed_sha: af057e982ccc99b1f5eef2ae86dd129ccaa969b5
spec_sha256: 81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3. M-1: CHUA DAT — chua du bang chung A1/A2/M5 va CI A4 de approve HEAD cuoi.

## BANG DONG FINDING — thực hiện trước khi săn mới

Lệnh chung chạy từ `cay-kho/`: `python3 -B ../evidence/common.py closure.py`. Script và output thật: `evidence/closure.py`, `evidence/closure.log`. Tái dựng cùng cơ chế phản chứng trong các verdict cũ; không giả là đã có các script cũ trong bundle.

| slug | lượt | lệnh / phép đo | output thật | trạng thái |
|---|---|---|---|---|
| F01-harness-tin-ten-loai-va-duoi-stdout | 1 | closure.py: F01_equal_qualname_RuntimeError, F01_fake_suffix | `loi ... khac:TinHieuChotCa`; `loi ... khong co ket qua kenh, rc=1`; own signal `giet` | DONG |
| F01-harness-cung-qualname-van-cap-tin-dung | 2 | closure.py: F01_equal_qualname_{RuntimeError,AssertionError} | cả hai `loi ... khac:TinHieuChotCa` | DONG |
| F02-n13-do-bash-ke-thua-init-va-home-cha | 1 | closure.py: F02_outer_init; BASH_ENV/ENV ghi marker trơ, HOME cha tạm | ca qua; `lines=[]`, `home_files=[]` | DONG |
| F03-cc-ca-khoa-chi-tim-chuoi-diem-noi | 1 | closure.py: F03_preserved_comment; đổi do.add, giữ lời gọi trong comment | ca hành vi ném OWN_SIGNAL; mutant nhận sai cả AttributeError/AssertionError | DONG |
| F05-assertion-ca-khac-bi-ghi-thanh-ca-dich | 2 | closure.py: F05_product/harness/credential; target gọi registered other | a `loi(chot cua ca khac)`; b `loi(khac:TinHieuChotCa)`; c tên có `(chot cua ca khac)` | DONG |
| F05-assertion-ca-khac-bi-ghi-thanh-ca-dich | 4 | closure.py: F08_other_*; gọi other chung factory | cả a/b/c từ chối `ValueError __code__`, `calls=[]` | DONG theo quyết định cấm registry chung code |
| F06-ca-dich-vang-bi-xoa-khoi-mau-so | 2 | closure.py: F06_missing/partial/duplicate qua runner thật | cả ba `(1,0)`, `SAI - ca dich khong tim thay/trung` | DONG |
| F07-khoa-neutral-chi-do-chuoi-nguon | 2 | closure.py: F07_preserved_literal; bỏ neutral, giữ literal | OWN_SIGNAL của khóa hành vi, vì a `(0,0)` thay vì `(1,0)` | DONG |
| F08-shared-code-khong-phai-ca-khac | 3 | closure.py: F08_own_* | a/b/c từ chối registry trước chạy, `calls=[]`; không còn chạy rồi gán sai nguồn | DONG theo phạm vi chủ kho sửa đổi |
| F08-shared-code-khong-phai-ca-khac | 5 | closure.py: F08_*_chay_dot_bien, F08_lock harness_direct_CA | ValueError trước chạy, `calls=[]`; khóa ba chế độ CLI PASS | DONG |
| F08-shared-code-khong-phai-ca-khac | 6 | closure.py: F08_{pass,skip,own}_{cham_mot_ca,chay_bo_ca} | mọi tổ hợp ValueError trước thân ca; `calls=[]`; hai khóa lượt 6 PASS | DONG |
| F09-commit-dem-sai-so-dot-bien-moi | 4 | closure.py: F09_history; AST commit 5548919 so cha trực tiếp | `added=4`, `changed=3`, `correction=true`; HANDOFF và c5acb70 đã đính chính | DONG bằng đính chính; commit lịch sử vẫn sai |

F04-kenh-ket-qua-gia-truoc-main (lượt 2, nợ #1117): closure.py/F04_debt1117_module_initializer vẫn cho `('giet','review_target')` mà thân target không chạy. Giữ riêng theo chỉ thị, không tính finding chặn. Chưa thấy tệ hơn; sẽ đối chiếu AST receiver/reporter với mốc đã khai nợ.

Phép xác minh bổ sung qua toàn bộ `chay_dot_bien` với neutral child xanh và mutant child thật: `python3 -B ../evidence/common.py closure_full_runner.py` → F01 hai lớp cùng qualname/stdout giả và F05 other đều `(1,0)` SAI; own `(0,0)` OK; F04 initializer vẫn `(0,0)` OK như nợ cũ. Xem `closure-full-runner.log`.

## Định danh, phạm vi và cách chạy

Reviewer: OpenAI Codex, provider `openai_codex`, execution surface `codex_service`, transport `machine`; shell/tool thực sự chạy trong phiên này, độc lập với Executor Claude. Runtime không cung cấp chứng cứ xác minh exact model ID phục vụ từng request; không suy từ lịch sử launcher. Lease/generation theo chỉ thị trực tiếp: `wp1079-r1-g10-claude`, `sensitive`, lượt 8/8. Thông tin g8 trong HANDOFF là lịch sử, không dùng thay chỉ thị g10. Không gọi mạng, không dùng credential thật, không ghi GitHub.

HEAD `af057e982ccc99b1f5eef2ae86dd129ccaa969b5`; tree `25ce0eea23a45e0ba0cf5444466ddb9c66a42342`; base `7eeb1d9a10aea8e1805b66fbf3d68549eb6778da`. `gates.py`: `diff_exact=true`, `numstat_exact=true`; SPEC tự băm khớp `81070fa2c5a00bc0bb63867c7173f310cba9002001b68a26d62726ec904cbf5b`. Diff `.claude/` đúng hai tệp, +834/−118; trần 1000 do chủ kho nâng không là finding.

Mọi lệnh dạng `python3 -B ../evidence/common.py <script.py> [tham số]` dưới đây chạy được từ `cay-kho/`. Wrapper xoá môi trường kế thừa, dùng HOME và TMPDIR riêng ngoài checkout, Git config trơ, `PYTHONDONTWRITEBYTECODE=1`, `PIP_NO_INDEX=1`; không đọc secret. Ba lệnh suite được subprocess chạy đúng `python3 .claude/dev/launcher_test.py`, thêm `--dot-bien` khi cần, và `python3 .claude/dev/codex_cred_test.py`. Output/rc/thời lượng lưu riêng `.out`, `.err`, `.json`.

Không tạo tar hay bản sao toàn kho. Bản base chọn đúng blob của các fixture thực thi: 182 tệp/12.570.626 byte, sau bổ sung gói `scripts/tl_core` 32 tệp/2.751.706 byte để kiểm một skip do fixture thiếu. Mọi mutant chỉ ở thư mục tạm ngoài checkout, được xoá sau phép đo; có đủ >6 GB trống trong khi chạy. Bản base tối thiểu không phải full checkout, nên khai riêng khác biệt fixture; không dùng số tổng của nó để giả là A1 đạt.

`/tmp/.git` tồn tại, chỉ đọc; `/var/tmp` không ghi được trong sandbox. Vì vậy chưa có tiền đề chuẩn A1. Không xoá/bypass hai rào này. Các lỗi storage, môi trường và offline bên dưới không được tính thành hồi quy packet.

## BANG NGHIEM THU

| tiêu chí | lệnh | output | đạt? |
|---|---|---|---|
| M1 — a phân loại đúng, giữ skip | `python3 -B ../evidence/common.py oracles.py`; `python3 -B ../evidence/common.py closure.py` | AttributeError, implementation AssertionError, wrapped AssertionError đều SAI/tín dụng giả; own chốt OK; all-skip `(0,1)`, mixed `(0,0)` | ĐẠT phần đã đo |
| M2 — neutral a/b bản nguyên, cache, đỏ làm cổng đỏ | `python3 -B ../evidence/common.py oracles.py` | a/b neutral lỗi hoặc chốt → `(1,0)` và `neutral do`; hai mutant cùng target chỉ neutral 1 lần, mutant 2 lần; b chạy child thật từ harness_goc | ĐẠT |
| M3 — b đòi tín hiệu đúng target, bỏ stdout/rc làm nguyên nhân | `python3 -B ../evidence/common.py oracles.py`; `python3 -B ../evidence/common.py closure.py` | child stdout giả rồi SystemExit → SAI, thiếu kênh; lớp cùng qualname ở hai họ đều `loi`; own signal `giet`; registered other bị loại | ĐẠT trong giới hạn #1117 đã được chấp nhận |
| M4 — c đúng lớp/đúng tệp/assert thật; wrapped không giả | `python3 -B ../evidence/common.py oracles.py`; `python3 -B ../evidence/common.py extra_checks.py` | t2 neutral `[]`; own assert đúng tên; unrelated/wrapped có suffix loại; tệp khác cùng số dòng assert bị loại. 13/18 native mutant giết đúng, 5 neutral đỏ do môi trường | ĐẠT classifier; 5 native storage mutant KHÔNG ĐO ĐƯỢC |
| M5 — 11 mutant cũ chết bằng chính chốt ca | `python3 -B ../evidence/common.py base_oracle.py` | 10 mutant có neutral xanh, chết OWN_SIGNAL đúng target. `g2_rejected_refresh_khong_phu_thuoc_metadata` neutral OSError `Codex home is inside a repository` | 10 đạt; 1 KHÔNG ĐO ĐƯỢC, không khai 11/11 |
| M6 — N13 cô lập PATH/installer/HOME/init, giữ thứ tự npm | `python3 -B ../evidence/common.py fixture.py`; `python3 -B ../evidence/common.py a2_fixture.py` | base installer 7/init 3; HEAD 0/0; cả hai probe Bash và hook ở HEAD không dùng HOME cha, không BASH_ENV/ENV/BASH_FUNC; HOME cha trống; npm codex → npm claude → chuan-bi → doctor | ĐẠT |
| M7 — khóa a/b/c, gỡ từng chốt phải đỏ đúng ca; không chặn nhầm own/helper | `python3 -B ../evidence/common.py mutations.py`; `python3 -B ../evidence/common.py extra_checks.py`; `python3 -B ../evidence/common.py oracles.py` | 26 mutant của packet, 29 target, **29 OWN_SIGNAL**, wrong=[]; 22 khóa mới xanh trên HEAD. Hai guard mới của lượt cuối đều có phản chứng OWN_SIGNAL. r13 và t70 cùng helper vẫn giết thật | ĐẠT phần đã đo; shared-code bị từ chối theo quyết định chủ kho |
| A1 — N/N, M/M, credential ĐẠT khi /tmp/.git vắng | `python3 -B ../evidence/common.py run_suites.py head launcher`; `python3 -B ../evidence/common.py run_suites.py head mutation`; `python3 -B ../evidence/common.py run_suites.py head credential` | 318/342, 10 skip, 24 lỗi; 512/548, 4 không đo nền, 36 neutral đỏ; credential 13/18, dừng trước mutation | KHÔNG ĐO ĐƯỢC trong tiền đề chuẩn; không là pass |
| A2 — thước mới trên ca base, khóa đỏ trên scorer/fixture cũ | `python3 -B ../evidence/common.py base_oracle.py`; `python3 -B ../evidence/common.py a2_fixture.py`; `python3 -B ../evidence/common.py extra_checks.py` | scorer đầy đủ: 397 OK/446 product, 34 neutral đỏ, 11 SAI, 4 skip; gồm 10 tên SPEC và alias r13/t70 do F05, thiếu tên g2 do storage. Phép type-only 12 mutant đối chứng tách ảnh hưởng F05. Khóa neutral trên runner base OWN_SIGNAL; khóa credential đỏ khi dùng do.add của base; base N13 + hậu điều mới OWN_SIGNAL | Phản chứng đạt phần đo được; bộ **đúng 11 tên SPEC** trên nền chuẩn KHÔNG ĐO ĐƯỢC |
| A3 — A/B installer ngoài npm giả | `python3 -B ../evidence/common.py fixture.py` | base 7, HEAD 0; init 3→0; npm vẫn được đo thật bằng shim | ĐẠT |
| A4 — ruff F delta0, diff-check, doctrine, CI head cuối | `python3 -B ../evidence/common.py gates.py` | Ruff 0.16.8: launcher 5 F841 ở cả hai bản, credential 0/0; delta0. Diff `.claude/` rc0; doctrine rc0, 10 tệp/0 chỗ. Toàn diff rc2: blank EOF của master ở ops/specs/launcher-sandbox-lay-mau-r2.md | Local scope ĐẠT; CI check run trên exact HEAD KHÔNG ĐO ĐƯỢC vì cấm mạng và không có snapshot check-run cuối trong bundle |

## BANG TEST

| bộ | N/M, rc và bằng chứng | bỏ qua |
|---|---|---|
| HEAD launcher | **318/342** ca đã chạy qua; tổng352, lỗi24; rc1; `head-launcher.out/.err/.json` | 10: 1 fixture Windows, 8 venv/pip offline, 1 SID Windows |
| HEAD mutation | **512/548**, rc1; `head-mutation.out/.err/.json`; 36 SAI đều có `neutral do`, không nhận là kill | 4 nền: 3 native Windows, 1 fixture Windows t62 |
| HEAD credential | nền **13/18**, `TỔNG: ĐỎ`, rc1; `head-credential.out/.err/.json`; dừng trước mutation | 0 skip; 5 nền đỏ KHÔNG ĐO ĐƯỢC do /tmp/.git |
| BASE launcher, fixture tối thiểu | **294/319**, tổng330, lỗi25, rc1; `base-launcher.out/.err/.json`; không có lỗi chỉ xuất hiện ở HEAD | 11: cùng10 như HEAD + r349 vì ban đầu chưa chép scripts/tl_core; phép bổ sung kiểm riêng, không sửa lại log thô |
| BASE credential | nền **13/18**, `TỔNG: ĐỎ`, rc1; cùng5 tên ca lỗi ở HEAD (HEAD thêm suffix loại đúng thiết kế) | 0 skip; dừng trước mutation |
| Mutant gỡ chốt packet độc lập | **29/29** target OWN_SIGNAL trên26 mutant; `mutations.log`; toàn22 khóa mới xanh trên HEAD | 0 |
| Credential mutant đo riêng | **13/18** được nhận đúng tên với neutral xanh; `extra-checks.log` | 5 neutral đỏ, không được coi là skip hay kill |
| 11 mutant SPEC trên ca HEAD | **10/11** OWN_SIGNAL với neutral xanh; `base-oracle.log` | 1 không đo được do neutral OSError, không là kill |

Bộ credential: năm ca nền đỏ là t6, t9, t15, t16, t18 ở cả base/HEAD; t15 trả trạng thái khác vì rào storage, bốn ca còn lại ném OSError. Bộ launcher: 24 lỗi HEAD đều có trong base; base có thêm t76 nhạy thời gian. Phép chạy riêng t76/r349 và bộ so sánh chi tiết ghi tại `final-probes.log`.

## BANG DO

Cách tìm lời khai: đối chiếu toàn bộ `git diff BASE HEAD -- .claude`, từng hunk với AST hai tệp, dùng `tokenize` lấy comment và `ast.get_docstring` lấy docstring giao với dòng thêm/sửa, lấy cả câu `assert`/`bang` mới. `python3 -B ../evidence/common.py gates.py` tạo `claims-inventory.json`: **119 mục = 63 assertion + 32 comment + 24 docstring**. Đây là inventory nguồn, không phải tuyên bố mọi nhánh đã được phủ động. Đọc toàn bộ `%B` bằng `git log --format='%H%n%B' BASE..HEAD`; `commits.txt` giữ output nguyên; `commits-inventory.json` chứa **35 commit**, gồm10 commit thay `.claude/` và7 merge. Các message từ master cũng được lưu, nhưng việc land/CI/authority bên ngoài không thể tái xác minh offline.

| khẳng định | diff khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| CA chung code bị từ chối trước thực thi ở các điểm vào đã biết | launcher kiem_registry/ca/cham_mot_ca/chay_bo_ca/chay_dot_bien; message af057e9 | `closure.py`, `extra_checks.py`: pass/skip/own/other đều calls=[]; guard gỡ độc lập → OWN_SIGNAL | KHỚP |
| Không hứa bảo vệ mọi chỗ gọi thẳng fn() | docstring kiem_registry, message af057e9 đã thu hẹp | AST entrypoints và phản chứng hook trong `mutations.py`; hiện registry352/352 code riêng | KHỚP phạm vi đã khai |
| Gỡ guard main tương đương trên các đường thực thi ca | message af057e9; main đi qua hai runner | `closure.py`: default/repeat/mutants đều từ chối registry trước thân; `mutations.py`: guard hook vẫn có răng | KHỚP; không tính mutant tương đương sống là lỗi |
| Chỉ đúng tín hiệu assertion suite mới là kill ở a; AssertionError trần/đổi kiểu không qua | cham_mot_ca/ket_luan_mutant docstrings, các khóa a | `oracles.py`: unrelated/implementation/wrapped đều `(1,0)`; own `(0,0)` | KHỚP |
| Chốt registered other không là chốt target ở a/b/c | chot_tu_ca_khac; reporter; ten_do; message5548919 | `closure.py`: cả ba loại other; factory cùng code bị từ chối; `oracles.py` giữ helper thật | KHỚP trên HEAD; lời khai5368c34 sai trong lịch sử đã được đính chính |
| Neutral đỏ → không đo và hỏng; bản gốc và cache mỗi target | hai cache trong chay_dot_bien và khóa hành vi | `oracles.py`: neutral1/mutant2; lỗi neutral a/b `(1,0)`; `closure.py` bỏ thực thi giữ literal làm khóa đỏ | KHỚP |
| Thiếu/trùng target không rơi mẫu số | F06 nhánh a; message5548919 | `closure.py`: missing/partial/duplicate cùng `(1,0)` | KHỚP |
| Skip nền vẫn giữ all-skip/mixed | ket_luan_mutant, M1/M2 | `oracles.py`: a/b all `(0,1)`; mixed a `(0,0)`; khóa thuần mixed b chung ket_luan_mutant PASS trong mutations.log | KHỚP phần đã đo; không thử native Windows |
| b lấy kênh có nonce thay stdout; ca không giữ LT variables trong env | cham_lap_ca và main pop hai LT keys | `oracles.py`, `closure.py`, `mutations.py`: stdout giả bị loại; sai nonce bị loại; own signal nhận; code pop trước chạy ca | KHỚP với ranh giới đã công bố |
| Kênh không chống mã cấp module của mutant | docstring cham_lap_ca, message5548919/HANDOFF #1117 | `closure.py`: forged initializer vẫn giet; `gates.py`: receiver AST không đổi từ5548919 | KHỚP nợ; không thấy làm tệ hơn; không tính finding |
| c đúng lớp, đúng tệp, dòng assert; bare assert thật vẫn nhận | la_chot_cua_suite/ten_do/chay_suite | `oracles.py`: own bare assert thật được nhận, foreign-file cùng dòng bị loại, implementation/wrapped bị loại | KHỚP |
| Khóa credential phải đo hành vi, comment không thay thực thi | r1079_cc_chay_suite_phai_do_hanh_vi; messageee23c44 | `closure.py` giữ comment và khôi phục do.add sai → OWN_SIGNAL; 7 mutant c trong `mutations.py` đều đúng ca | KHỚP |
| 28 assert được chuyển sang bang tại hai ca g2 | hai hunk r484_g2 | `final_probes.py`: 20→0 và8→0 assert; `base_oracle.py` đo checkpoint mutant bằng own signal | KHỚP về chuyển đổi; recovery còn storage chưa đo được |
| r01/r10 không nhận kill từ FileNotFoundError | helper _r1079_run_json và hai ca | `base_oracle.py`: cả hai neutral qua, mutant OWN_SIGNAL với thông báo thiếu run.json | KHỚP |
| t115 bắt vi phạm hợp đồng không ném ra ngoài bằng chốt của ca | wrapper _doc_mcp_json | `base_oracle.py`: bốn mutant JSON/kểu đều neutral qua và OWN_SIGNAL, chẩn đoán giữ loại gốc | KHỚP |
| t79 lỗi fake Win32 dùng tín hiệu suite | OpenProcess shim đổi lớp | `base_oracle.py`: job_bo_qua_loi_dat_gioi_han OWN_SIGNAL | KHỚP trên fake API; không khai đã chạy Windows |
| r13 dùng helper chung thay ca t70 | hunk r13/t70; message7df242e | `oracles.py`: riêng r13 và t70 đều OK/giet1/1; `a2_fixture.py` type-only base alias OK2/2 còn thước F05 hiện tại loại alias cũ | KHỚP |
| N13 không gọi installer ngoài npm giả, không dùng init/HOME cha | fixture và khóa N13; messaged8f8998/ee23c44 | `fixture.py`: 7→0 installer,3→0 init, cha HOME trống ở HEAD; `mutations.py`: bỏ rg/shim/filter/probe env đều OWN_SIGNAL | KHỚP hiện tại; F02 lượt1 đã đóng |
| Cây harness có đúng bố cục và companion | _dung_cay_harness, messagec73dff3/c5acb70 | `mutations.py`: tất cả khóa N13/c credential nạp đúng và giết đúng; các tệp được tạo dưới .claude/dev, .claude/hooks, ops/bash_nen.py | KHỚP; không có tín dụng FileNotFoundError trong29 target |
| “5 dot bien moi” của5548919 | thông điệp lịch sử | `closure.py`: thêm4 tên/sửa3 hàng; c5acb70 và HANDOFF đính chính rõ | SAI lịch sử nhưng đã đính chính, F09 đóng |
| “đóng theo cấu trúc” củac5acb70, “mọi điểm vào” củae3bcaf0, F05 còn bị loại của5368c34 | thông điệp lịch sử | phản chứng cũ được giữ; các message sau và HANDOFF đính chính; `closure.py` đo lại các lối đã bỏ sót | ĐÃ ĐÍNH CHÍNH; không coi message cũ tự đúng vì HEAD đã sửa |
| Các số test lịch sử5368c34/7df242e/5548919/d929ee2/c73dff3 và hash HINT provenance | các message trong commits.txt | `final_probes.py` inventory từng full SHA; bundle có verdict cũ nhưng không có toàn bộ HINT/run byte để băm lại | KHÔNG ĐO ĐƯỢC đầy đủ số lịch sử/hash provenance; không dùng làm pass hiện tại |
| Các số N/N và M/M của HANDOFF tại af057e9 | 350/350,548/548,TỔNG ĐẠT khi /tmp/.git vắng | ba suite độc lập trong môi trường hiện tại cho318/342,512/548,13/18 | KHÔNG ĐO ĐƯỢC đúng tiền đề; không kết luận lời khai sai do chênh môi trường |
| ruff F delta0, diff-check và doctrine | HANDOFF; một số message cũ | `gates.py`: delta0, scope diff-check rc0, doctrine rc0 | KHỚP HEAD local; không thay bằng chứng CI |
| CI/check-run/land/authority và số đo của25 commit master/merge còn lại | commits.txt giữ nguyên toàn35%B | `final_probes.py` lưu mỗi OID/message và scope; không có mạng hay đầy đủ receipt ngoài bundle | KHÔNG ĐO ĐƯỢC; ngoài code delta packet, không kết luận bằng lời khai |

Đối với credential mutant đo riêng: `extra-checks.log` có14 lần tập đỏ khớp tên, nhưng **chỉ13 có neutral xanh**. Lần thứ14 là t15 đã đỏ từ neutral, nên bị loại khỏi số kill chứng minh được. `main` thật đã dừng ngay khi nền13/18, đúng yêu cầu không chạy mutation khi neutral đỏ; không lấy14/18 làm số đạt.

## BANG SAN

Tất cả lệnh dưới đây dùng wrapper `python3 -B ../evidence/common.py` từ `cay-kho/`; tên script và nhãn output là phần tái lập cụ thể. Không có hướng chỉ nêu ý tưởng mà chưa chạy.

| hướng độc lập | lệnh | output thật | phân loại |
|---|---|---|---|
| 1. Lỗi vô can trực tiếp ở a/b/c | `python3 -B ../evidence/common.py oracles.py` | PRODUCT/HARNESS_attribute `(1,0)` có AttributeError; c t2(AttributeError) | KHÔNG PHẢI LỖI |
| 2. AttributeError qua except đổi thành AssertionError | `python3 -B ../evidence/common.py oracles.py` | PRODUCT/HARNESS_wrapped `(1,0)`, `tin dung gia`; c có suffix AssertionError | KHÔNG PHẢI LỖI |
| 3. AssertionError trần do implementation | `python3 -B ../evidence/common.py oracles.py` | a/b SAI giet0/1; c tên không khớp target | KHÔNG PHẢI LỖI |
| 4. Chốt own thật và helper không đăng ký | `python3 -B ../evidence/common.py oracles.py` | own a/b `(0,0)`; c đúng tên; r13/t70 mỗi ca OK1/1 | KHÔNG PHẢI LỖI; không chặn nhầm đối chứng này |
| 5. Assertion từ registered other code riêng | `python3 -B ../evidence/common.py closure.py` | a chot cua ca khac; b khac:TinHieuChotCa; c suffix chot cua ca khac | KHÔNG PHẢI LỖI |
| 6. Same factory own và gọi thật sang alias | `python3 -B ../evidence/common.py closure.py` | mọi runner ValueError __code__, calls=[] cả own/other/pass/skip | KHÔNG PHẢI LỖI theo chính sách cấm đã được chủ kho duyệt |
| 7. Đường raw CA qua hai hàm vừa vá | `python3 -B ../evidence/common.py closure.py`; `python3 -B ../evidence/common.py extra_checks.py` | HEAD từ chối trước thân; gỡ guard từng hàm → OWN_SIGNAL với calls=['review_target'] | KHÔNG PHẢI LỖI; F08 lượt6 đóng |
| 8. Nhánh hook cần guard chay_dot_bien | `python3 -B ../evidence/common.py mutations.py` | wp1079_registry_bo_kiem_chay_dot_bien → OWN_SIGNAL đúng r1079_registry_nhanh_hook_tu_choi_truoc_chay | KHÔNG PHẢI LỖI |
| 9. Neutral đỏ và neutral cache | `python3 -B ../evidence/common.py oracles.py` | a/b lỗi/chốt neutral `(1,0)`; cached calls neutral,mutant,mutant | KHÔNG PHẢI LỖI |
| 10. Bỏ qua theo nền/all-skip/mixed | `python3 -B ../evidence/common.py oracles.py`; `python3 -B ../evidence/common.py mutations.py` | all-skip a/b `(0,1)`; mixed `(0,0)` | KHÔNG PHẢI LỖI trong phép đo Linux |
| 11. Child giả LOAI_HONG/headline rồi thoát | `python3 -B ../evidence/common.py oracles.py`; `python3 -B ../evidence/common.py closure.py` | SAI; thiếu kết quả kênh rc1 | KHÔNG PHẢI LỖI |
| 12. Lớp khác cùng __name__/__qualname__ | `python3 -B ../evidence/common.py closure.py` | RuntimeError và AssertionError giả đều loi(khac:TinHieuChotCa) | KHÔNG PHẢI LỖI |
| 13. Tệp khác có assert cùng số dòng | `python3 -B ../evidence/common.py oracles.py`; `python3 -B ../evidence/common.py mutations.py` | kiểm foreign-file PASS; mutant bỏ so tệp → OWN_SIGNAL đúng khóa c | KHÔNG PHẢI LỖI |
| 14. Target thiếu/trùng/thiếu một phần | `python3 -B ../evidence/common.py closure.py` | cả ba `(1,0)` với SAI ca dich khong tim thay/trung | KHÔNG PHẢI LỖI |
| 15. Giữ chữ trong comment/literal nhưng gỡ hành vi | `python3 -B ../evidence/common.py closure.py` | F03_preserved_comment và F07_preserved_literal đều OWN_SIGNAL | KHÔNG PHẢI LỖI; khóa mới có răng |
| 16. PATH rg hỏng + installer gián điệp + init + HOME cha | `python3 -B ../evidence/common.py fixture.py` | base7 installer/3init; head0/0, HOME cha trống, ba child env đều sạch | KHÔNG PHẢI LỖI HEAD |
| 17. Gỡ từng guard/khôi phục fixture base | `python3 -B ../evidence/common.py mutations.py`; `… a2_fixture.py` | 29/29 OWN_SIGNAL; base N13 + hậu điều mới OWN_SIGNAL với7 AMBIENT | KHÔNG PHẢI LỖI HEAD |
| 18. Chạy thước thật cũ với unrelated exception | `python3 -B ../evidence/common.py base_oracle.py` | base a/b `(0,0)` OK dù AttributeError; head a/b `(1,0)` SAI | KHÔNG PHẢI LỖI HEAD; phản chứng nguyên nhân F01 đã được vá |
| 19. Giả kênh tại module initializer | `python3 -B ../evidence/common.py closure.py`; `python3 -B ../evidence/common.py gates.py` | vẫn giet; receiver AST unchanged=true | LỖI ĐÃ NHẬN NỢ #1117, không phải finding chặn mới; không thấy tệ hơn |
| 20. Phân biệt hỏng môi trường với hồi quy | `python3 -B ../evidence/common.py final_probes.py` | only_head=[]; t76 và r349 chạy riêng đều PASS ở cả hai bản | KHÔNG PHẢI LỖI packet; tổng suite vẫn đỏ và không đạt A1 |
| 21. Chính xác toàn11 tên cũ trên nền chuẩn | `python3 -B ../evidence/common.py base_oracle.py`; `… a2_fixture.py` | 10 tên đo được; g2 recovery neutral OSError; alias F05 được tách bằng đối chứng type-only | KHÔNG ĐO ĐƯỢC trọn bộ vì /tmp/.git |
| 22. Check run CI trên exact HEAD | inventory commits và bundle; không gọi mạng | không có snapshot check-run cuối; HANDOFF mới khai15 success/8 running tại lúc ghi | KHÔNG ĐO ĐƯỢC, không là CI xanh |

Không tìm thấy finding P0/P1/P2/P3 mới trong phạm vi diff và các phản chứng đã đo. Không mở lại F04, không tính trần dòng, và không đổi bẫy sandbox thành lỗi sản phẩm.

## Quyết định và bảo toàn checkout

`changes_requested` vì chưa đủ chứng cứ nghiệm thu để approve, **không có yêu cầu vá mã mới** trong review này. F01–F09 đã có bảng kiểm đóng riêng; F04 giữ đúng nợ #1117. Để đạt M-1 cần hoàn tất phép đo A1 và phần còn lại M5/A2 trong môi trường `/tmp/.git` vắng, ghi đủ các số bằng nhau/skip thật, và cung cấp check run CI thành công trên đúng `af057e982ccc99b1f5eef2ae86dd129ccaa969b5`. Không yêu cầu nới rào sandbox của phiên này và không tự đọc thiếu bằng chứng thành pass.

`final-probes.log`: base/head t76 chạy riêng đều PASS; base/head r349 đều PASS sau bổ sung đúng package base. Không có lỗi chỉ HEAD. Chênh t76 ở suite nguyên được giữ nguyên trong số thô, không sửa log thành xanh. Đối chứng A2 type-only: 10 mutant SPEC SAI vì lỗi/AssertionError vô can, 1 mutant SPEC neutral đỏ vì storage; alias r13/t70 OK2/2 khi chưa bật F05. Đủ giải thích vì sao phép dùng toàn bộ scorer HEAD trên ca base có thêm lỗi alias, nhưng chưa đủ chứng minh toàn11 tên SPEC trong tiền đề chuẩn.

`python3 -B ../evidence/common.py integrity.py` đối chiếu **10.161 tệp tracked** với snapshot đầu: changed=[], extra_tracked=[], Git status kể cả ignored rỗng; HEAD/tree giữ nguyên; diff packet vẫn khớp bundle. Suite native đã tự sinh một marker ignored `.claude/.packet_state/session-start.ran` (28 byte, thời điểm tạo sau snapshot đầu); đã lưu metadata/hash và dọn duy nhất hiện vật test này cùng thư mục rỗng. Không sửa nội dung tracked. Bằng chứng: `final-integrity.json`, `integrity.log`. Snapshot đầu/cuối chứng minh không còn delta quan sát được; không được đọc thành chưa từng có ghi tạm của test.

`HINT.patch` rỗng (0 byte): không đề xuất bản vá runtime khi chưa phát hiện lỗi mã mới. Các script phản chứng và output giữ trong `evidence/`; bản base phục vụ đo chỉ khoảng15 MB, toàn evidence17 MB, còn6,5 GB trống lúc kết thúc. Không có tar/bản sao toàn kho hoặc tệp tạm lớn còn lại của reviewer. Không sửa nhánh Executor, không push, không gọi mạng và không dùng credential thật.
