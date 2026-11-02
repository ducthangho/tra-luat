verdict: approve
reviewed_sha: 8f0dfcf35c8ee92a9a754bde82846eb11430bd0e
spec_sha256: c34d506626e40a07fbfef41ccd39e138f74a2df3116f1b53cea704aaf6068d43
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

Packet #1117 r2, lease `wp1117-r2-g2-claude`, Codex lượt 5/10, review class `sensitive`.
Đã review Spec và Standards/Security. P2 connector `r4438879478` đóng trong phạm vi Linux đã đo;
F01/F02/F03 giữ đóng. Không thấy finding mới. Không áp ADR-0060.
`approve` là kết luận rà soát mã; các gate đỏ hoặc chưa đo bên dưới giữ nguyên trạng thái, không tạo quyền land.

Reviewer theo hiện vật runtime: `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`,
run `e7296898c1a4450c83d9775d085f2ede`; nguồn `run/e7296898/run.json`.
Model/effort phục vụ từng request và session executor không được đo độc lập từ bundle;
không suy danh tính từ actor GitHub, không tự tạo receipt hoặc assurance.

HEAD/tree: `8f0dfcf35c8ee92a9a754bde82846eb11430bd0e` / `ba76eb2e791e16faed68d1ce5c08d3b5f96f700d`.
Base `c7174bfe03b3acd22cfa055b5fce176129d29542` là tổ tiên HEAD. Checkout sạch ở hai mốc kiểm.
Spec r1 kế thừa có SHA-256 `48710a9b41cb744dd5b89df1d9f632fae51d08dcf22a0581088918832663598e`.
Hai tệp diff giao kèm khớp byte với Git. So L4 `6f4b889`, chỉ đổi ca kiểm runner giả trong `launcher_test.py`;
runner thật giữ nguyên byte. Diff so base: 3 tệp, +442/-85; riêng harness +329/-85.
113 dòng changelog spec kế thừa merge master đã được ghi ở L4; không có thay đổi mới ở tệp đó trong lượt này.
Trần 6 tệp/+450 không bị vượt. Bằng chứng: `evidence/preflight.json`.

## DOI CHIEU FINDING VA LOP

| ID / slug ổn định | Nguồn | Kiểm độc lập và kết luận |
|---|---|---|
| F01 `runner-stdin-khong-ghim-utf8` | L1 `b6fe853` | Giữ ĐÃ VÁ THẬT trong biểu hiện Linux đã báo: HEAD 6/6, base 6/6, L1 4/6 tổ hợp đường ASCII/có dấu × utf-8/ascii/cp1258. Mutation codec HEAD giết đúng ca. Windows thật chưa đo độc lập. |
| F02 `dot-bien-map-van-nham-ca-qua-runner` | L1 | Giữ ĐÃ VÁ THẬT: hai mutation map HEAD OK đúng `r1122_nhat_ky_giu_loai_va_thong_diep_160`; L1 cả hai SAI. Nhóm codec/map HEAD `(0,0)`, nhóm hai map L1 `(2,0)`. |
| F03 `chot-kieu-record-chua-co-dot-bien-dung-tin-hieu` | L2 `b9f010b`, đóng L3 | Giữ ĐÃ VÁ THẬT: 7/7 mutation HEAD OK, đủ 8/8 ca đích; cùng guard deletion trên L2 SAI 0/1 vì AttributeError, HEAD OK 1/1 bằng TinHieuChotCa. AttributeError vô can tại chính nhánh danh_sach vẫn là loi, không được cấp tín dụng. |
| `r4438879478` / `runner-gia-tach-khung-stdin-bang-khoang-trang` | Connector sau L4 | ĐÃ VÁ THẬT trong phạm vi đo: HEAD 9/9, L4 3/9 ma trận tempfile.tempdir/codec; CLI TMPDIR HEAD 3/3, L4 1/3. Chỉ đổi splitlines() về split(), giữ nguyên giải mã UTF-8 và fixture có dấu cách, làm ca HEAD đỏ bằng TinHieuChotCa. |

Bốn lớp/bốn finding lịch sử trong bảng, không có lớp/biểu hiện mở trong phạm vi đã đo.
Không thấy cửa giả thụ động thứ tư trong các nhánh đã kiểm. Giới hạn `RUNNER-CUNG-TIEN-TRINH`
(và ghi đè tệp có chủ ý) giữ nguyên theo spec; không tuyên bố đã đóng giới hạn ấy.
Dữ liệu: `focused-results.json`, `history-results.json`, `parser-isolation.json`, `f03-negative.json`
và `legacy/f03-results.json`, tất cả dưới `evidence/`.

## BANG NGHIEM THU

| Tiêu chí | Bằng chứng | Trạng thái |
|---|---|---|
| N0 r2 | Hai ca phản chứng có sẵn chép nguyên văn vào base; CLI mỗi ca rc=1, HONG TinHieuChotCa, kết quả sai là giet/review_target | passed |
| A1: giả lúc khởi tạo module | Các ca hiện có xanh; mutation env/argv/ghi sớm và quay lại --lap-ca giết đúng ca | passed trong phạm vi đo |
| A2: runner thật | Ca byte identity qua; 6 biến thể runner méo đều bị chính A2 giết; bỏ copy cũng bị giết | passed |
| A3: thứ tự và stdin | 11 phép contract đạt; 4 alias stdin đều EOF; đảo đọc stdin sau import bị ca có sẵn giết. Main bỏ kênh và loai_luot; CLI HEAD không tạo kênh | passed |
| A4: chốt #1079 | 38/38 ca tập trung qua; nhóm 14 mutation được giao (mọi wp1117 và wp1079 nhắm ca kênh) OK qua chay_dot_bien thật | passed |
| A7: bảo đảm #1122 | Ca lồng cùng tên/định dạng lỗi, chi tiết 160 ký tự và không mang lỗi cũ đều qua; 24 mutation reporter OK đúng đích | passed |
| A8/A6 tĩnh | Bare Ruff rc=1 mỗi vế với cùng 5 F841; delta=0. Doctrine rc=0, diff-check rc=0 | passed theo delta/tĩnh |
| A5 suite cục bộ | HEAD 335/358, base 331/354; cùng 23 tên lỗi và 10 skip, rc=1 | failed; delta tập tên lỗi=0 |
| A5 full mutation cục bộ | HEAD 552/584, base 543/575; cùng 32 SAI và 4 không đo, rc=1 | failed; delta tập SAI=0 |
| A5 credential | Hai vế 13/18, cùng 5 lỗi, TỔNG ĐỎ, rc=1; log hai vế trùng SHA-256 | failed; delta lỗi=0 |
| Linux A/B với TMPDIR ngoài /tmp | Quyền ghi chỉ workspace và /tmp; không thử ghi ngoài quyền | KHÔNG ĐO ĐƯỢC |
| A5 r2 Windows exact HEAD, CI và hậu land | Bundle không có job/check log exact HEAD đủ kiểm; không gọi mạng; không thực hiện land | not_measured / not_run |

A3 literal r1 chỉ cho LT_KENH trong ca/mutation nhưng chính r1 cũng yêu cầu bộ lọc env;
bộ lọc và docstring cham_lap_ca phục vụ yêu cầu đó. Giữ cách xử lý đã ghi L4, không mở lại xung đột câu chữ kế thừa.
Bare Ruff đã đo riêng; Ruff pin/probe contract của workflow không chạy ở lượt này.

## BANG DO

| Khẳng định | Phép đo độc lập | Kết luận |
|---|---|---|
| P2 hết với dấu cách và tiếng Việt | Ma trận tempfile.tempdir: ASCII / co dau cach / thư mục tiếng Việt × utf-8 / ascii / cp1258; HEAD 9/9, L4 3/9. CLI đặt TMPDIR ba đường ấy: HEAD 3/3, L4 1/3 | Xác nhận bản vá; không nhầm parser fixture với runner sản phẩm |
| Phản chứng riêng bộ tách dòng | Chỉ splitlines() → split(), giữ UTF-8 và thư mục có dấu cách; ca thành giet | Ca mới có răng; `parser-isolation.json` |
| Còn runner giả/khung stdin tách bằng khoảng trắng? | Duyệt AST toàn 15,661 dòng / 107,864 node, mọi literal stdin (18 node), các phép split (52 call), và đọc các tham chiếu trong nguồn/fixture/bảng mutation | Không thấy parser kênh thứ hai cùng lỗi. Runner giả :10330 dùng byte/UTF-8/splitlines; phản chứng :10551 dùng splitlines; fixture :12523 chỉ readline để điều khiển tiến trình |
| Kênh không vào env/argv | Spy chuyển tiếp subprocess thật: argv 4 mục, stdin 2 dòng, env LT_KENH rỗng, channel_in_argv=false, kênh cha không tồn tại | Khớp trong phép đo |
| Bao phủ bảng hiện có | Product 446, hook 79 giữ nguyên; harness 54→63; mọi ca đích tồn tại; các neo của 63 mutation harness đều khớp đúng một chỗ | Khớp universe trong cây; không chứng minh mọi mutation có thể có |
| Nguồn được bảo toàn | 10,815 tệp tracked/untracked/ignored ở hai mốc, delta byte rỗng; HEAD/tree/status/diff sạch. Hai bản sao dùng đo cũng khớp byte nguồn HEAD/base | Không có delta quan sát được; `snapshot-results.json` |
| Windows/CI xanh trên HEAD | Chỉ có lời khai đang chạy trong prompt, không có log để xác minh | KHÔNG ĐO ĐƯỢC; không coi là gate pass |

Chi tiết quét toàn tệp ở `evidence/whole-file-audit.json` và `stdin-source-audit.json`.
Các split còn lại xử lý proc stat, phiên bản, marker/log hoặc tham số công cụ; không đọc khung kênh stdin.
Mutation cố ý quay về codec môi trường là dữ liệu phản chứng, không phải parser vận hành thứ hai.

## BANG TEST

| Lệnh / hiện vật | Kết quả thật |
|---|---|
| `python3 -B evidence/focused.py` | 38/38 ca; ma trận HEAD/L4; nhóm 14 mutation `(0,0)`; 24 reporter `(0,0)`. Phản chứng parser được tách riêng, giữ UTF-8, ở parser-isolation.json; bản kết quả trước tách vẫn được lưu |
| `python3 -B evidence/history.py` | Transport HEAD/base/L1 = 6/6, 6/6, 4/6; đối chứng map và record guard đúng kỳ vọng; N0 đỏ đúng |
| CLI theo `evidence/cli-results.json` | HEAD TMPDIR 3/3; L4 1/3; hai N0 rc=1 đúng nguyên nhân giet/review_target |
| 6 script `evidence/legacy/probe_*.py` | Tất cả rc=0; 11 contract, 6 copy mutant, stdin order, CLI, lỗi nạp, F03 7 mutation/8 đích và envelope đều đúng; validator 15/15 |
| `python3 -B evidence/run_ab.py` | Một lệnh dựng lịch chạy HEAD → base, mỗi vế suite → mutation → credential; 6 lệnh con đều rc=1, giữ log nguyên trạng; không có tên lỗi/SAI mới |
| Bare Ruff / doctrine / diff-check | Cấu hình, command, version và rc ở static-results.json; Ruff 0.16.9, delta=0, doctrine 10 tệp/0 chỗ |
| `python3 -B evidence/validate.py` | 33/33 kiểm nội dung bằng chứng đạt; không chỉ dựa rc của script probe |
| `python3 -B evidence/snapshot.py` | Nguồn và hai bản sao đo không có delta byte; rc=0 |

Python 3.13.18; Linux; /tmp/.git hiện hữu và không bị xóa/che. A/B dùng cùng TMPDIR dưới /tmp,
PIP_NO_INDEX=1, PIP_DISABLE_PIP_VERSION_CHECK=1, PIP_CONFIG_FILE=/dev/null, bytecode tắt.
Không thay fixture để làm xanh các lỗi ngoài phạm vi. Số đo cục bộ không thay số đo Windows hoặc TMPDIR ngoài /tmp.
Command/cwd/rc/UTC/thời lượng/hash từng log nằm trong `evidence/{head,base}-{suite,mutations,credentials}.json`;
tập tên lỗi/skip/SAI và đối chiếu ở `evidence/ab-summary.json`.

Các probe kế thừa lấy từ hiện vật review L4, không tái sử dụng context executor. Bốn script giữ nguyên byte;
F03 chỉ bỏ bước clone/checkout vì đã có bản L2 exact SHA; envelope lấy nguyên đoạn đo có sẵn và thêm phần nạp HEAD.
Nguồn/băm/cách thích nghi ở `evidence/legacy/provenance.json`, lượt chạy ở `legacy/runs.json`.
Bản sao lịch sử đã dùng xong được nén trong evidence/*-tree.tar.gz; giải nén vào evidence/trees trước khi chạy lại probe cần chúng.
Không tự soạn payload giả kênh hay lớp ngoại lệ mới; chỉ dùng ca, mutation và probe đã có.

Checkout cay-kho/ được đối xử read-only; sandbox thực tế cho ghi workspace và /tmp.
Snapshot chứng minh không có delta ở hai mốc, không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên.
Không sửa cay-kho/, không push, không gọi mạng, không dùng credential thật.
`HINT.patch` rỗng vì không có finding cần đề nghị vá; không tạo quyền merge/land hoặc miễn gate còn thiếu.

Khoảng đo A/B: 2026-11-02T04:27:00.008593+00:00 → 2026-11-02T04:48:55.107549+00:00.
