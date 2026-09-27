verdict: changes_requested
reviewed_sha: 70d1698ad2867d8e6e6721d416e80b1f3ebb9704
nguong_ap: sensitive + chỉ thị chủ kho "đến hết P1, P2, P3"

Có **2 lớp finding / 2 finding P2** còn mở: kiểm kiểu matrix workflow và schema JSON của đường gộp. Không đủ điều kiện approved. Các phép đo bổ sung chưa phát hiện tín dụng giả trong bộ phân hạng hiện có; thay đổi r543 qua phép đo A8.

## ĐỊNH DANH VÀ PHẠM VI

- HEAD/tree: `70d1698ad2867d8e6e6721d416e80b1f3ebb9704` / `a55ad4572a7cb9aebab38ee80513bd5f63797726`.
- Base: `5618f61c6ac2fa14aab52b0f5ce3d065aee8e022`. Spec SHA256 đo khớp `9a2ab4fe746330f87ef86cc9b9a2bef6da8edde6e198a1989d415827c9fb2783`. Lease đọc từ `1efa6cf40c06e9413cd942a2260aed7b12fb8095` trong `kho.git`: revision 2, generation 1, đúng W1–W3, hạn 2026-09-28T15:22Z; lease cho phép base trôi tới 5618f61. Không xác minh người ký qua mạng.
- Reviewer `openai_codex / codex_cli / machine`; header thật ở `stderr.log`: Codex v0.157.1, model `gpt-6-astra`, effort `xhigh`, session `01a0e379-19d4-7b12-a012-4a45c0771073`. Header CLI công bố, không phải telemetry xác minh mọi request. Phiên review độc lập với executor; không gọi subagent.
- Sandbox `workspace-write`, approval `never`. Quy tắc read-only với `cay-kho` được thực hiện bằng cách đặt script, fixture, bản sao và log ngoài checkout; không tuyên bố sandbox khóa ghi vật lý toàn checkout. Python chạy `PYTHONDONTWRITEBYTECODE=1`; Ruff dùng `--no-cache`.
- Môi trường: Python 3.12.3; `python3` mặc định là 3.11.15; actionlint 1.7.7, ShellCheck 0.9.0; Ruff sẵn có 0.15.8. Registry cần Git fixture không ký commit: dùng `GIT_CONFIG_GLOBAL=/tmp/r1-git-measure.config` (commit/tag gpgsign=false, core.abbrev=7). Không sửa cấu hình global hoặc checkout.
- Không mạng GitHub, không CI, không chạy full 233 mutant không mảnh hoặc đủ bốn mảnh. Prompt cho phép chọn lọc; phần chưa đo được ghi riêng, không tính là pass.
- Bằng chứng trong `evidence/`; lệnh tái lập trong `do/`. `do/run_logged.py LABEL COMMAND...` ghi stdout/stderr vào `evidence/LABEL.log`, cùng command/rc/giây thật trong `evidence/LABEL.json`. Khi helper `tk_muc.py` tự trả rc=0, kết luận dựa thêm tuple phân hạng và từng dòng ca đích, không dựa riêng rc.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 1 — không có finding cũ.

## BẢNG LỚP

| Slug lớp | Biểu hiện | Hạng | Nguồn | Hướng đóng lớp |
|---|---|---|---|---|
| workflow-matrix-type-confusion | F01: matrix bool lọt validator và registry | P2 | Lượt 1 / reviewed_sha trên | So kiểu matrix trước so giá trị; thêm phản chứng workflow sai kiểu, chạy cả validator, actionlint và registry thật |
| shard-json-schema | F02: object thay mảng; bool/float phiên bản; kiểu so_manh tùy vị trí tệp | P2 | Lượt 1 / reviewed_sha trên | Kiểm schema của từng tệp, thêm ca r552 và mutant riêng có đầu vào phân biệt; giữ chốt thiếu/trùng/lệch tập tên |

## BẢNG ĐỐI CHIẾU SPEC

`Đạt phần đo` chỉ xác nhận các lệnh ghi ở hàng đó; không thay nghiệm thu chưa chạy.

| Mục | Kết luận | Bằng chứng chạy được / giới hạn |
|---|---|---|
| M1 | Đạt phần đo | `contracts.log`: CLI sai k/N rc=2 trước mutant; mọi phân hoạch N=2..8 phủ đủ/rời nhau; trùng tên cả hai bảng bị từ chối. `r549–r551` xanh trong TU_KIEM; mutant bỏ pop env/gỡ chốt/đổi vòng lặp bị giết đúng đích trong `selected-*.log`. Chưa chạy một mảnh đầy đủ đến khi ghi artifact thật. |
| M2 | **Lệch P2 F02** | `boundaries.log`: CLI gộp nhận object và số/bool sai kiểu. Đối chứng hợp lệ và các trường hợp thiếu/trùng/chuyển tên, băm sai, thiếu/thừa JSON được kiểm bởi r552 và mutant tương ứng. |
| M3 | Đạt các chốt đã có; thiếu phủ lỗi F02 | 33 mục mới = 32 mục nhắm r549–r552 + `ghi-so-gop` nhắm r546 đều giết đúng đích. `NHOM_BAT_BUOC=52`, `SAN_NHOM=52`. Chưa có ca phân biệt các schema sai ở F02. |
| M4 | Đạt đường CLI | `contracts.log`: biến đúng làm riêng nhanh_don_duoc nhẹ, hai bộ kia không đổi; 6 chuỗi lạ làm `--chay` rc=2 trước kế hoạch; biến trong env bước ci.yml bị từ chối. Thử env cấp workflow cũng bị chốt băm chặn. |
| M5 | **Lệch P2 F01** | Matrix `[false,true,2,3]` lọt cả validator, actionlint và registry thật (`registry-matrix-bool.log`: 933/933, rc=0). Các lệch được liệt kê ở A5 vẫn bị chặn. |
| M6 | Đạt tại chỗ | Workflow thật đúng hình cấu hình, actionlint 1.7.7 + shellcheck rc=0; kiểm qua registry 933/933. Không xác nhận artifact action/runner bằng CI. |
| M7 | Đạt phép đo yêu cầu | HEAD r543 dưới đột biến 0/400; gốc 0/300; base dưới đột biến 6/300; trả bộ sinh cũ trên HEAD 5/300. 13 mục liên quan r543/vòng rút lại đều giết đúng đích, mục vòng rút lại vẫn nhắm `{r527,r528}`. |
| A1 | Chưa đo trọn | Tự đo kích thước phân hoạch `[3,3,2,2]` và `[59,58,58,58]`, tổng 10/233. Fixture gộp in đủ ba dòng nhưng KHÔNG phải bốn artifact từ bốn lượt mutant thật. Không xác nhận rc/thời gian của bốn lượt executor khai. |
| A2 | Đạt các ca liệt kê; mở rộng gặp F02 | Thiếu/thừa tệp, chuyển/xoá tên, sha test sai, so_manh lệch và JSON hỏng được r552 kiểm; mutant gỡ từng chốt bị giết đúng. Các đầu vào sai kiểu bổ sung vẫn lọt. |
| A3 | Đạt phần đo | CLI sai hình, thiếu RA, không dòng MAU_DAY_DU, độ phủ phân hoạch đều được ca r549–r551 kiểm; mutant gỡ chốt bị giết. `contracts.log` đo CLI thật và phân hoạch độc lập. |
| A4 | **not_run trọn bộ** | Nhẹ 8/8; TU_KIEM 52/52; DOT_BIEN thật `(10,0,0)`; chọn lọc 46/46 đúng đích. Các kết quả này không thay một lượt đủ 233 mutant không mảnh. Executor chưa giao kết quả A4. |
| A5 | Đạt các phản chứng được liệt kê | Registry HEAD 933/933; base 916/916. Tháo chốt job ghim trên bản sao khiến 7 phản chứng lọt, registry đỏ 926/933. Vẫn thiếu phản chứng matrix bool của F01. |
| A6 | Đạt phần đo; thiếu đúng phiên bản Ruff | Registry chung baseline/HEAD đều xanh, +17 phản chứng; BAM_GATE_REGISTRY và ci.yml không đổi. Bare Ruff F base/HEAD 0/0 với 0.15.8; chưa đo 0.15.15. Actionlint rc=0. Không chạy `--chay` trọn mọi bộ khác. |
| A7 | **not_run — sau land** | Không gọi workflow_dispatch; phép quan sát sau land không phải cổng land theo spec. Không xác nhận mục tiêu 22–25 phút. |
| A8 | Đạt phép đo chọn lọc | Các số A8 ở M7 và log r543; 12 mục nhắm r543 cùng 1 mục vòng rút lại đều `(13,0,0)`. Chưa chạy lại chúng trong A4 trọn bộ. |

M2 có ví dụ cũ `185/185`, còn A1 yêu cầu N lấy từ bảng thực tế. Base hiện tại có 200, HEAD có 233; review dùng N=233 theo tiêu chí động A1 và claim commit, không đòi hard-code 185.

## BẢNG SĂN

| Hướng | Giả thuyết / lệnh | Output thật | Kết luận |
|---|---|---|---|
| 0 | Kiểm neo: sha256sum, Git OID/tree, numstat, lease | Spec/HEAD/tree đúng; +449/-16 đúng ba W1–W3 | KHÔNG PHẢI LỖI |
| 1 | `python3.12 do/probe_boundaries.py`: tệp gộp sai schema vẫn xanh | bool/float phiên bản, float số mảnh tệp sau, object hai tập tên: CLI rc=0 + GOP MANH 4/4 + 10/10 + 233/233 | **LỖI F02** |
| 2 | Cũng script trên: tập tên thiếu/trùng/băm sai/mảnh bool | CLI rc=1 và `GOP: LOI`; không có dòng GOP MANH | KHÔNG PHẢI LỖI trên các đầu vào này |
| 3 | Matrix bool trên bản sao workflow; registry thật với Git config riêng | validator `[]`; actionlint rc=0; registry 933/933, `TỔNG: ĐẠT`, rc=0. CLI `false/4`, `true/4` đều rc=2 | **LỖI F01** |
| 4 | Matrix/needs/if/continue-on-error/env registry/bước lệch | Phản chứng p661 trong 933/933 đều đỏ đúng. Gỡ so job ghim làm registry 926/933, rc=1 | KHÔNG PHẢI LỖI trên hình sai đã có ca; chốt có răng nhưng chưa phủ kiểu bool |
| 5 | Thêm biến mảnh cấp workflow ci.yml (`sandbox/ci-env`) | Registry rc=1, lỗi băm gate-registry; `loi_env_registry` riêng không bắt nhưng chốt tổng bắt | KHÔNG PHẢI LỖI |
| 6 | `python3.12 do/probe_contracts.py`: đầu vào mảnh lạ/trùng mutant | k/N lạ rc=2; trùng từng bảng ValueError; N=2..8 phủ đúng và rời nhau | KHÔNG PHẢI LỖI |
| 7 | Biến mảnh rò xuống con / bỏ chạy TU_KIEM / làm giả tổng / chọn sai phần bảng | `tk_muc.py ... 0/2 new` và `1/2 new`: `(16,0,0)` mỗi phần; từng mục đỏ đúng ca | KHÔNG PHẢI LỖI ở các đường đã đo |
| 8 | M4 giá trị lạ làm bộ khác nhẹ | CLI 6 chuỗi lạ rc=2; đường đúng giữ cả hai bộ khác nguyên. Hàm ke_hoach trực tiếp tin tham số đã validate; không tìm đường CLI vượt doc_bien_manh | KHÔNG PHẢI LỖI đường CLI |
| 9 | `python3.12 do/probe_false_credit.py`: TypeError/no-op bị tính GIẾT | TypeError → DO_KHAC r551/r552 → TIN DUNG GIA; no-op → child rc=0 → TIN DUNG GIA; tuple `(0,2,0)` | KHÔNG PHẢI LỖI; không cấp tín dụng giả |
| 10 | `do/do_r543.py` HEAD/base và HEAD trả bộ sinh cũ | HEAD mutant 0/400; HEAD gốc 0/300; base mutant 6/300; HEAD revert mutant 5/300 | KHÔNG PHẢI LỖI; bản sửa có tác dụng và phép đo có răng |
| 11 | `tk_muc.py ... r543`, rồi `... ghi-so-gop` | `(13,0,0)` và `(1,0,0)`; tổng chọn lọc 46/46 đúng đích | KHÔNG PHẢI LỖI trên các mục đã chọn |
| 12 | `tk-json-recursion-escape`, Python 3.11 và 3.12, base/HEAD | 3.11: cả hai `(0,1,0)`, đỏ r539+r540; 3.12: cả hai `(1,0,0)`, đỏ đúng r539 | KHÔNG PHẢI LỖI packet; delta=0 |
| 13 | `python3.12 do/try_guards.py`: thử chặn hai finding trên sandbox | W1 sai schema chuyển đỏ, đối chứng và r549–r552 xanh; guard kiểu matrix trong bộ nhớ từ chối bool/float, vẫn nhận workflow gốc | Hướng vá khả thi ở phạm vi thử; chưa xác nhận toàn mutation suite sau vá |
| 14 | Bốn mảnh thật, gộp thật, full không mảnh, runner GitHub | Không chạy trong lượt này | KHÔNG ĐO ĐƯỢC; không suy pass từ fixture |

Không tự soạn thử thoát thư mục/đường dẫn. Các artifact fixture chỉ dùng kiểm parser, không có giá trị chứng minh 233 mutant đã chạy.

## BẢNG ĐO

| # / khẳng định | Executor khai | Reviewer đo | Khớp? |
|---|---|---|---|
| 1 / A1 | Bốn lượt rc=0, 3/59, 3/58, 2/58, 2/58; gộp 10/233; ~1780s/mảnh | Phân hoạch đúng các kích thước; fixture gộp đúng format. Không chạy bốn lượt thật | Chỉ khớp phân hoạch/format; rc/thời gian/đủ 233 chưa xác minh |
| 2 / A8 | HEAD mutant 0/400, gốc 0/300; base mutant 8/300 | 0/400, 0/300; base 6/300; trả bộ sinh cũ trên HEAD 5/300 | Khớp tính chất; 6 so 8 là dao động phép lấy mẫu, không gọi là số khai sai |
| 3 / registry | 933/933, TỔNG: ĐẠT | Sau cô lập cấu hình Git: HEAD 933/933 rc=0 (7.175s), base 916/916 rc=0 (6.950s). Nguyên môi trường rc=1 vì commit.gpgsign=true | Khớp khi Git fixture không ký; điều kiện sandbox được khai rõ |
| 4 / actionlint | 1.7.7 rc=0, có shellcheck | Đúng 1.7.7 + ShellCheck 0.9.0, rc=0, không chẩn đoán | Có |
| 5 / Ruff | 0 finding cả hai vế với 0.15.15 | Có sẵn 0.15.8: `--no-cache --select F` W1,W2 đều `All checks passed!` base/HEAD, rc=0 | Delta=0 ở phiên bản đo; chưa xác minh 0.15.15 |
| 6 / diff | +449/-16, 3 tệp | W1 +317/-7; W2 +66/-9; W3 +66/-0 | Có |
| 7 / 46 mục chọn | 33 mới + 13 liên quan r543 đều giết đúng | `(16,0,0)+(16,0,0)+(1,0,0)+(13,0,0)`, từng tên/đích có log | Có, 46/46; không có tín dụng giả hoặc không đo được |
| 8 / recursion | Python3.11 giết lây r540 cả hai; 3.12 đúng cả hai | Đúng như bảng săn hướng 12 | Có, delta=0 |
| 9 / thời gian TU_KIEM | 52 ca ~16–17s so 48 ca ~11s, thừa nhận chưa đo hai vế cùng lệnh | Cùng lệnh, tuần tự xen kẽ sau khi các tác vụ đo khác đã xong: HEAD 21.842/22.310/22.778s; base 20.681/20.154/19.703s. Median 22.31/20.154s, tăng 2.156s (10.7%). Tất cả rc=0, 52/52 và 48/48 | Không tái hiện số tuyệt đối ước lượng; đã đo hai vế đồng điều kiện trong sandbox |
| 10 / A4 | Chưa có kết quả lúc giao | Không chạy trọn; không nhận được kết quả executor bổ sung | Chưa xác minh |
| Commit / bảng và ca | 200→233 mutant, 48→52 ca/sàn; +33 mutant | Tự import base/HEAD: đúng 200/233, 48/52; set tên mới đúng 33 | Có |

Lần dùng `/usr/bin/time` ban đầu rc=127 vì công cụ vắng, không phải đã chạy test. Đã thay bằng monotonic clock; các số ở bảng lấy từ lượt thực chạy. Các ước lượng thời gian giữa môi trường/lượt có tải khác nhau không đủ để kết luận executor báo sai; không dùng chúng thay A7.

## FINDINGS

### workflow-matrix-type-confusion [P2] Chốt workflow nhận matrix bool như số nguyên

**TỆP/DÒNG:** `.claude/dev/ci_dang_ky_test.py:867` (so job) và `:874` (matrix kỳ vọng).

**VẤN ĐỀ:** So dict/list bằng `==` khiến `[False, True, 2, 3]` bằng `[0, 1, 2, 3]`. Vì vậy workflow sai matrix M5 vẫn được validator chấp nhận. actionlint coi matrix bool là YAML/workflow hợp lệ và không cứu được chốt này. Registry thật trên bản sao chỉ đổi matrix W3 vẫn rc=0, 933/933 và TỔNG: ĐẠT. Hai giá trị `false/4`, `true/4` bị bộ chạy mảnh từ chối rc=2: thay đổi lỗi có thể qua chốt PR rồi làm lượt tuần hỏng. Không khẳng định toàn workflow sẽ xanh khi mảnh thất bại.

**ĐÃ THỬ VÁ:** Thử guard miền kiểu của matrix trong bộ nhớ, trước validator hiện có: phải là list gồm các `type(x) is int`, rồi so đúng `[0,1,2,3]`. Workflow thật vẫn được nhận, matrix bool/float/thiếu phần tử bị từ chối. Đây là thử hẹp; executor cần tự tích hợp guard và ca p* rồi đo registry đầy đủ. Có thể dùng so cấu trúc có xét kiểu cho toàn job, nhưng phải giữ các đối chứng hợp lệ.

**ĐÃ THỬ NGHIỆM:**

```sh
python3.12 do/probe_boundaries.py
GIT_CONFIG_GLOBAL=/tmp/r1-git-measure.config python3.12 sandbox/workflow-bool/.claude/dev/ci_dang_ky_test.py
python3.12 do/probe_contracts.py
python3.12 do/try_guards.py
```

Output: `WF matrix-bool validator=[] actionlint_rc=0`; registry `PHẢN CHỨNG: 933/933 đỏ đúng`, `TỔNG: ĐẠT`, rc=0; CLI giá trị bool rc=2. Khi tháo hẳn chốt job ghim, registry đỏ 926/933, chứng minh các phản chứng hiện có chạy thật nhưng thiếu trường hợp này.

**ĐỘ TIN:** Cao. Cần thêm phản chứng độc lập về **kiểu** matrix, không chỉ số phần tử/N. Không có patch workflow đính kèm.

### shard-json-schema [P2] Gộp chấp nhận sai kiểu schema rồi phát bằng chứng đủ

**TỆP/DÒNG:** `ops/nhanh_don_duoc_test.py:5421` (phiên bản), `:5423` (số mảnh), `:5434` (hai tập tên).

**VẤN ĐỀ:** `_loi_gop` chỉ kiểm kiểu số mảnh của tệp đầu; những tệp sau so bằng giá trị. Phiên bản cũng chỉ so giá trị. Hai trường `giet`/`tk_giet` được duyệt như iterable mà không đòi mảng chuỗi. Vì vậy:

- `phien_ban=true` hoặc `1.0` được nhận như phiên bản nguyên 1.
- `so_manh=4.0` ở tệp sau được nhận, nhưng ở tệp đầu bị từ chối: kết quả phụ thuộc thứ tự tên tệp.
- Thay hai mảng bằng object `{tên_mutant: false}` trong cả bốn tệp vẫn được tính qua các key của object.

Từng phản chứng đều rc=0 và phát ba dòng đủ `GOP MANH 4/4`, `MUTANT ... 10/10`, `TU DOT BIEN ... 233/233`. Đây là lỗ xác thực định dạng bằng chứng M1/M2; r552 chưa phân biệt các kiểu này. Không khẳng định đã làm mất tên mutant, hoặc rằng hash tệp nguồn có khả năng xác thực lịch sử chạy của fixture tự dựng. Đảo thứ tự mảng vẫn bảo toàn tập tên; không tách nó thành finding.

**ĐÃ THỬ VÁ:** Trên bản sao W1, kiểm từng tệp: phiên bản/số mảnh là int thực (không bool/float), hai tập tên là list chứa str. Tất cả fixture sai kiểu kể trên chuyển đỏ; đối chứng hợp lệ vẫn xanh; bốn ca r549–r552 vẫn ĐẠT. Chốt thiếu/trùng tên/băm sai vẫn đỏ. Chưa chạy trọn DOT_BIEN_TU_KIEM trên bản vá thử. Executor cần thêm ca và mutant riêng có đầu vào phân biệt, tránh tạo chốt trùng khiến mutant cũ sống mà không được đo lại.

**ĐÃ THỬ NGHIỆM:** `python3.12 do/probe_boundaries.py` và `python3.12 do/try_guards.py`; chi tiết `evidence/boundaries.log` / `evidence/try-guards.log`. Tệp fixture ở `sandbox/probes/`, bản thử guard W1 ở `sandbox/gop-type-guard/`.

**ĐỘ TIN:** Cao. Phạm vi tác động là schema và tính nhất quán của gate gộp, không phải lỗi thuật toán phân hoạch đã được đo.

**Nhãn chung cho hướng vá:** chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit. Script/bản sao là dữ liệu thử của reviewer, không mang quyền ghi branch hoặc quyền approval/land.

## GIỚI HẠN VÀ KIỂM READ-ONLY

- A1 bốn mảnh, A4 trọn bộ, A7 trên GitHub và Ruff đúng 0.15.15 chưa được xác minh trong lượt này. Không có positive evidence thì không ghi pass.
- Snapshot hash mọi tệp ngoài `.git`: 2251 trước / 2251 sau, 0 tệp đổi/thêm/xoá; HEAD/tree giữ nguyên; status tracked/untracked/ignored rỗng. `git diff` và diff index cuối rỗng. Bằng chứng `evidence/checkout-before.json`, `checkout-after.json`, `checkout-verification.json`. Phép so hai mốc chỉ chứng minh không có delta quan sát được, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.
- Verdict neo exact reviewed_sha; thay HEAD thì cần review lại. Không approve, merge, push hoặc đăng thông điệp ra bên ngoài.
