verdict: approve
reviewed_sha: 6f4b88991b14f1a15ceafdf4b4b3b564039449a1
spec_sha256: c34d506626e40a07fbfef41ccd39e138f74a2df3116f1b53cea704aaf6068d43
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

Packet #1117 r2, lease `wp1117-r2-g2-claude`, Codex lượt 4/10, review class `sensitive`.
Đã review hai trục Spec và Standards/Security. Không có finding mới trong phạm vi đã đo; F01/F02/F03 giữ đóng.
Không áp ADR-0060. `approve` là kết luận review mã nguồn; các gate chưa đo được vẫn giữ trạng thái riêng.

Reviewer: `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`, run `e9dab4183a284a51b142651b401617bf`.
Nguồn nhận dạng: `run/e9dab418/run.json`, không suy từ actor GitHub. Model/effort thực sự phục vụ từng request và
session executor không đo độc lập được từ gói hiện vật; không tự tạo receipt, assurance hoặc quyền merge/land.

HEAD/tree: `6f4b88991b14f1a15ceafdf4b4b3b564039449a1` / `1670437d1ce6ff83d6d56df35b60240aa81be922`.
Base: `c7174bfe03b3acd22cfa055b5fce176129d29542`, đã xác nhận là tổ tiên HEAD. Checkout detached, sạch ở đầu/cuối.
Spec r1 kế thừa: SHA-256 `48710a9b41cb744dd5b89df1d9f632fae51d08dcf22a0581088918832663598e`.
`diff.patch` khớp byte với `git diff BASE HEAD -- .claude`.

`git diff --quiet 4a0d45d HEAD -- .claude` trả rc=0. Merge có hai parent `4a0d45d3c689600f749866f7b27e83b9d6039c00`
và `9091cf52cf20ac197c1a356d6a33cac6bab0b318`; chỉ thêm `ops/specs/CHANGELOG-D-NGOAI-GOI-r2.md` (113 dòng).
Tệp ấy khớp byte với parent master. Thay đổi harness: 2 tệp, +326/-85; toàn bộ diff hai chấm với base cố định:
3 tệp, +439/-85, vẫn dưới trần 6 tệp/+450. Không tính tệp đặc tả kế thừa từ master thành thay đổi runtime của #1117.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / slug ổn định | Nguồn | Kết luận và phép kiểm trên exact HEAD |
|---|---|---|
| F01 `runner-stdin-khong-ghim-utf8` | L1 `b6fe8534d7498ebe88a1a222b49fbf36fe97cdf1` | ĐÃ VÁ THẬT trong biểu hiện Linux đã báo, giữ đóng: HEAD 6/6 tổ hợp đường ASCII/có dấu × utf-8/ascii/cp1258; L1 4/6, base 6/6. Mutation codec `OK giet 1/1` đúng ca UTF-8. Windows thật chưa đo độc lập. |
| F02 `dot-bien-map-van-nham-ca-qua-runner` | L1 | ĐÃ VÁ THẬT, giữ đóng: hai mutation map HEAD đều `OK giet 1/1` đúng `r1122_nhat_ky_giu_loai_va_thong_diep_160`; nhóm F01/F02 HEAD `(0,0)`, L1 `(2,0)`. |
| F03 `chot-kieu-record-chua-co-dot-bien-dung-tin-hieu` | L2 `b9f010b3e5ef521d2980f12a5a3d4317e1e78724`, đóng tại L3 | ĐÃ VÁ THẬT, giữ đóng: cùng mutation bỏ guard dict trên L2 `SAI giet 0/1` do AttributeError; HEAD `OK giet 1/1` đúng ca kiểm record. Nhóm 7 mutation `(0,0)`, đủ 8/8 kết quả ca đích; đối chứng AttributeError vô can vẫn `loi`, không được cấp tín dụng. |

Lệnh: `python3 -B evidence/probe_review.py`, `probe_f03.py`, `probe_hint_negative.py`.
Kết quả đầy đủ: `review-probes.json`, `f03-results.json`, `hint-negative-result.json`.
Ba lớp lịch sử / ba finding lịch sử; không có lớp hoặc biểu hiện đang mở trong phạm vi review. Giải pháp chung và
witness được giữ nguyên từ L3: codec UTF-8, neo mutation đúng reporter, và chốt đúng lỗi `.get` trên record list của fixture.
Không mở catch thành mọi AttributeError. Không thấy cửa giả thụ động thứ tư trong các nhánh và phép đo đã kiểm;
giới hạn `RUNNER-CUNG-TIEN-TRINH` giữ nguyên theo quyết định chủ kho.

## BANG NGHIEM THU

| Tiêu chí | Phép đo / kết quả | Trạng thái |
|---|---|---|
| Exact SHA/spec/diff/trần | `evidence/preflight.json`: SHA/spec khớp; .claude giống L3; +439 tổng, +326 harness | passed |
| N0 r2 | Hai ca phản chứng sẵn có chép nguyên văn vào base c7174bf: cả hai rc=1, HONG TinHieuChotCa, kết quả `giet` sai | passed |
| A1: giả lúc khởi tạo module | Hai ca HEAD qua; các mutation env/argv/ghi sớm trong full mutation đều OK đúng ca | passed trong phạm vi đo |
| A2: chép runner thật | Ca byte identity qua; 6 bản runner méo đều bị chính A2 giết, accounting `(0,0)`; mutation bỏ copy cũng OK | passed |
| A3: đọc/đóng stdin trước nạp, ghi sau chấm | Runner đọc byte UTF-8 :44, dup2 :48, đọc frame :62 trước nạp :72, chấm :77 trước ghi :78. 11 phép contract đúng; đảo thứ tự bị ca hiện có giết | passed |
| A4: giữ chốt #1079 | 38/38 ca tập trung; 7 mutation kênh/lặp ca qua `chay_dot_bien` thật, 7/7 OK và 8/8 ca đích | passed |
| A7: giữ (a)(b)(c) #1122 | Ca lồng cùng tên/định dạng lỗi, loại + 160 ký tự, qua/bỏ qua không mang lỗi cũ đều qua; 3 mutation map/chi tiết OK đúng đích | passed |
| A8/A6 tĩnh | Ruff bare lint rc=1 mỗi vế với cùng 5 F841 cũ; delta chuẩn hóa=0. Doctrine rc=0 (10 tệp/0 chỗ), diff-check rc=0 | passed theo delta/tĩnh |
| A5 full suite cục bộ | HEAD 335/358, base 331/354; cùng 23 tên lỗi, cùng 10 skip, rc=1 mỗi vế | failed; delta lỗi 0 |
| A5 full mutation cục bộ | HEAD 552/584, base 543/575; cùng 32 SAI, 4 không đo, rc=1 | failed; delta SAI 0 |
| A5 credential | Hai vế cùng output tổng đỏ và cùng 5 dòng lỗi; xem log và mutation-results.json | failed; delta lỗi 0 |
| Linux A/B đúng TMPDIR ngoài /tmp | Sandbox chỉ cho ghi workspace và /tmp; không thử ghi ngoài quyền | KHÔNG ĐO ĐƯỢC |
| A5 r2 Windows exact HEAD / CI / hậu land | Gói chỉ có lời khai lượt Windows cũ và run trên HEAD đang chạy, không có job log để kiểm; không gọi mạng lấy thêm | not_measured / not_run |

A3 literal r1 nói LT_KENH chỉ còn trong ca/mutation, nhưng mục 2 chính r1 yêu cầu lọc env; bộ lọc và docstring
`cham_lap_ca` phục vụ yêu cầu ấy. Main đã bỏ phần đọc/ghi kênh và `loai_luot`; probe CLI HEAD không tạo kênh, base có.
Không tính xung đột câu chữ kế thừa đó thành finding mới.

## BANG DO

| Khẳng định / nguồn | Đo độc lập tại lượt này | Kết luận |
|---|---|---|
| Merge master giữ .claude nguyên byte với L3 | `git diff --quiet 4a0d45d HEAD -- .claude`: rc=0; chỉ thêm changelog spec, khớp parent master | Khớp |
| Gói executor: suite 352/362 → 356/366, cùng 10 HONG; mutation 550/575 → 559/584, cùng 25 SAI, TMPDIR /var/tmp | Hai cặp tập tên đính kèm bằng nhau; điều kiện /var/tmp không tái lập được. A/B offline dưới /tmp có cùng tập 23 HONG và 32 SAI giữa hai vế | Chỉ xác nhận delta cục bộ; không nhận số executor thành phép đo của reviewer |
| Không có kênh trong env/argv | Spy chuyển tiếp subprocess thật: argv 4 mục, stdin 2 dòng, env LT_KENH rỗng, channel_in_argv=false, kênh cha không tồn tại | Khớp trong phép đo |
| F03 không biến lỗi vô can thành kill | `hint-negative-result.json`: `loi`, not_credited=true | Khớp |
| Mỗi record có neo và ca đích | AST toàn bộ 3 bảng: product 446→446, hook 79→79 không đổi; harness 54→63, +12/-3/5 đổi; 63 neo đúng một chỗ, không thiếu ca đích | Khớp với universe trong cây; không chứng minh bao phủ mọi mutation có thể có |
| Windows run 41372451716 thành công trên 4a0d45d; run 41376440756 trên HEAD đang chạy; connector không finding trên HEAD | Không có job/check log gốc trong bundle | Không xác minh độc lập; không coi là gate exact HEAD đạt |

## BANG TEST

| Bộ / lệnh | Kết quả thật | Skip / giới hạn |
|---|---|---|
| `python3 -B evidence/run_ab.py`, suite HEAD | 335/358 qua, tổng 368, rc=1 | 23 lỗi, 10 skip |
| Cùng lệnh, suite BASE | 331/354 qua, tổng 364, rc=1 | Cùng tập lỗi/skip; head_only_failed=[] |
| Cùng lệnh, mutation HEAD | 552/584 đạt, tổng 588, rc=1 | 32 SAI, 4 không đo |
| Cùng lệnh, mutation BASE | 543/575 đạt, tổng 579, rc=1 | Cùng tập SAI/skip; head_only_failed=[] |
| Credential hai vế | nền: 13/18 đạt; TỔNG: ĐỎ (nền chưa xanh — không đo đột biến khi nền đã đỏ); cùng 5 dòng lỗi, rc=1 | Log giữ nguyên; không khai đạt |
| `probe_review.py` | 38/38 ca tập trung, 6/6 transport HEAD, 2/2 phản chứng N0 đỏ đúng; F01/F02 đúng đối chứng | 0 skip ca tập trung; Linux |
| `probe_f03.py` | 7/7 mutation HEAD OK, 8/8 ca đích, neutral qua; L2 nhóm có 1 SAI | Không lấy AttributeError làm kill |
| `probe_contract.py` | 11/11 đúng: 3 frame hợp lệ; 5 frame sai rc=2/no channel; thiếu/trùng ca → loi; EOF 4 alias | Không pyc |
| `probe_copy_and_cli.py` | 6/6 biến thể runner bị A2 giết; CLI HEAD không tạo kênh | Mutation dùng record sẵn có |
| `probe_order.py`, `probe_extra.py` | Đảo thứ tự đọc stdin OK giet 1/1; thiếu module/sai cú pháp rc≠0, không kênh | Không thêm payload giả kênh mới |
| `python3 -B evidence/validate_probes.py` | 29/29 kiểm nội dung bằng chứng đạt, rc=0 | Không chỉ dựa rc của script probe |

A/B dựng cả hai vế exact SHA trong MỘT lệnh, dùng cùng env/TMPDIR/công cụ; mỗi vế chạy suite → mutation → credential.
Python 3.13.18, Ruff 0.16.9. Khoảng đo HEAD: 2026-11-02T02:34:22.315637+00:00 → 2026-11-02T02:46:03.969622+00:00.
Cwd/command/rc/UTC/thời lượng của từng lệnh ở `evidence/{base,head}-{suite,mutations,credentials}.json`; output ở `.log`.
Danh sách tên lỗi/skip đầy đủ ở `suite-comparison.json`, `mutation-results.json`. Cả 12 mutation mới và 5 mutation đổi đều OK.
Bare Ruff được đo riêng; không khai đã kiểm pin/probe contract của workflow.

## BANG SAN

| Hướng kiểm | Lệnh / output thật | Kết luận |
|---|---|---|
| Codec/path có dấu | probe_review.py: HEAD 6/6, L1 4/6; mutation codec bị đúng ca giết | Không tái mở F01 |
| Record list và lỗi vô can | probe_f03.py + probe_hint_negative.py: đúng TinHieuChotCa cho guard deletion, lỗi vô can là loi | Không tái mở F03 |
| Frame/stdin còn dữ liệu | probe_contract.py: 5 frame sai không kênh; text/buffer/original/fd0 đều EOF | Không thấy lỗi trong các frame đo |
| Thiếu/trùng ca hoặc nạp lỗi | probe_contract.py + probe_extra.py: không chọn đại; nạp lỗi không ghi kênh | Không thấy lỗi |
| Đảo thời điểm đọc stdin | probe_order.py: đúng ca phản chứng giet 1/1 | Test canh được thứ tự |
| Runner cây lồng lấy bản méo | probe_copy_and_cli.py: cả 6 biến thể bị chính A2 giết | Ca byte identity có tác dụng trong biến thể đo |
| Bỏ sót record ngoài prefix wp1117 | inventory.py: cả 3 bảng, không thiếu ca/neo; full mutation kiểm toàn universe | Không thấy lỗi kiểm kê |
| Merge gây hồi quy ngoài nhóm tập trung | run_ab.py + suite_summary.py + summarize.py: không tên lỗi mới, không tên SAI mới | Delta=0 trong điều kiện offline dưới /tmp |

## Giới hạn, bảo toàn và bàn giao

Lượt A/B đầu đã dừng bằng SIGINT (rc=130) khi phát hiện fixture `_r345_venv` gọi pip install; log dở dang giữ ở
`evidence/ab-interrupted/`, không dùng làm evidence nghiệm thu. Lượt A/B dùng kết luận đặt `PIP_NO_INDEX=1`,
`PIP_DISABLE_PIP_VERSION_CHECK=1`, `PIP_CONFIG_FILE=/dev/null` cho cả hai vế; các ca thiếu gói cục bộ ghi skip.
Không thay fixture hoặc làm xanh các ca ngoài phạm vi. Các phép đo trên bản sao dùng -B/dont_write_bytecode,
Ruff no-cache. Script kế thừa từ evidence L3, provenance và bốn thay đổi phục vụ lượt này ở `script-provenance.json`.
Không tái sử dụng context executor; chỉ tái dùng các hiện vật đo đã được giao từ lượt review trước.

`/tmp/.git` hiện hữu; không xóa/che nó hoặc sửa phép kiểm tổ tiên. A/B đúng TMPDIR ngoài /tmp, Windows thật exact HEAD,
CI PR/check-run và hậu land vẫn KHÔNG ĐO ĐƯỢC từ môi trường/gói hiện tại. Không dùng số pass giả định thay log thiếu.
Giới hạn RUNNER-CUNG-TIEN-TRINH bao gồm can thiệp có chủ ý trong cùng tiến trình và ghi đè tệp trên đĩa, giữ đúng spec.

Snapshot đầu/cuối bao phủ 10,815 tệp ngoài .git, gồm tracked/untracked/ignored: delta byte rỗng,
HEAD/tree/index/status bằng nhau (`snapshot-comparison.json`). Đây là bằng chứng tại hai mốc, không chứng minh toàn bộ
lịch sử chưa từng ghi rồi hoàn nguyên. Sandbox thực tế workspace-write; checkout được đối xử read-only theo vai review.
Không sửa `cay-kho/`, không push hoặc dùng credential thật. `HINT.patch` rỗng vì không có finding cần đề nghị vá.
Không tạo quyền merge/land hoặc đổi gate thiếu bằng chứng thành passed.
