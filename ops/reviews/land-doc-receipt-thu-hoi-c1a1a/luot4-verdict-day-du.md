<!-- Verdict codex lượt 4/4 (gpt-6-astra, reasoning effort xhigh — header log runtime "reasoning effort: xhigh", session 01a0e5a8-841c-76e0-8d4a-be68da24b4f4), codex_cli tại chỗ, sandbox clone riêng, trên a004a236 (tree cfe98aa), base ceb1a3f3, spec sha256 978058983e8e…. Phạm vi HẸP theo quyết định chủ kho "Vá + Codex lượt 4". Chép NGUYÊN VĂN; không sửa chữ nào. Đường /tmp/review650-r4-output/* là đường trong sandbox reviewer; bản sao script nằm cạnh tệp này. -->
**0 P1 / 2 P2 / 1 P3**

verdict: changes_requested

```yaml
reviewed_sha: a004a23628a13bc1add0ae40b0318063406e3bad
reviewed_tree: cfe98aa3e2755a9cd8c25b9d6be3d1fd3c6a95f2
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
receipt_sha256: ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
revision: 5
lease: c1a1a-exec-2-claude-20260927
round: 4/4
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
executor: Claude
```

Các OID/băm trên được đo, khớp đầu–cuối. Áp dụng phạm vi hẹp và lượt cuối theo dữ kiện chủ kho tại Issue #650 comment 5861700702, trường `review_budget_ghi_chu`. Không xác minh comment/lease live qua mạng. Phiên này không có reviewer Claude và không tự tạo `cross_approved`.

**F25–F28 đã vá thật. Bốn phản chứng cũ của F29 đều bị bắt, nhưng bản vá F29 sinh hai lỗi trong chính cơ chế mới: đột biến nhiều chỗ và xử lý tiến trình purity.** Suite HEAD xanh không đóng được hai lỗi này. F29 là hàng đối chiếu tổng hợp, không đếm thêm một P2 ngoài F31/F32. Đây là lỗi của harness; chưa tìm thấy lỗi runtime của bộ kiểm JSON trên HEAD trong tập đầu vào đã thử.

Còn P2 sau lượt **4/4 tuyệt đối cuối**: chuyển toàn bộ bằng chứng sang **human audit của chủ kho**, không mở lượt model tiếp theo. Verdict này không cấp quyền merge/land.

## Phạm vi và hiện vật

Trong các lệnh dưới, `ROOT` là checkout được giao; `OUT=/tmp/review650-r4-output`; `D=.claude/dev`. Mọi lệnh chạy tại `ROOT`, dùng Python `-B`, `PYTHONDONTWRITEBYTECODE=1`; cache và hiện vật ở ngoài checkout. [Script điều khiển](run.py) giữ nguyên command, rc con, stdout và stderr trong từng `*.receipt.json`, `*.stdout`, `*.stderr`.

Ba script đầu vào ở `/tmp/review650-r4-input/` khớp nguyên byte với bản `luot3-*.py` trong kho. Bản lượt 4 chỉ chuyển wrong-type/wrong-line sang bộ ba ngoại lệ, chuyển tệp marker sang scratch lượt 4, bỏ phép hex64 partial-match không thuộc F25–F29 và bỏ chạy lại nợ F30. [Diff thích ứng](adaptations.patch) ghi đầy đủ; `classifier_stage.py` giữ nguyên. Không chạy lại cuộc săn toàn danh mục của lượt 3.

## Đối chiếu lượt 3

Nguồn: `luot3-VERDICT.md`, `luot3-verdict-day-du.md`; SHA lượt 3 `fb8ccff8bcf88aad011016afff3936c2fb4877c7`.

| Finding | Trạng thái | Bằng chứng tự đo trên HEAD |
|---|---|---|
| F25 | `da_va_that` | `classifier_stage.py`: baseline và ca gác pass; ngoại lệ chẩn đoán tại dòng 76 sau K1 đỏ thành `NEM:UnicodeDecodeError@76#1`, bị phân `unresolved`. Neo đúng loại/dòng/giai đoạn 0 thật vẫn `witness_killed`; sai loại, dòng, giai đoạn, neo trùng và tuple hai phần đều bị bác. |
| F26 | `da_va_that` | M1o2/M1u2/M1w3/M1x2: mỗi mutant giữ **10/11 ca dương xanh**, gồm `duong_fixture`; chỉ `duong_c_khac_s` đỏ và được tính giết. Gác `None`, tên vắng, `bom`, hoặc trùng đích đều `unresolved`. M3w/x/y vẫn giữ đối chứng nullable xanh. |
| F27 | `da_va_that` | M1o3 và M1x3 tồn tại; baseline `bom` và gác dương pass; mutant làm đúng `bom` thất bại vì `ok:0` hoặc thừa khoá; cả hai `witness_killed`. Hai ô thiếu của ma trận lượt 3 đã được bổ sung. |
| F28 | `da_va_that` | Phản chứng hex64 ép số cũ nay suite **rc 1**, đỏ đúng `hex64_la_so` và `descriptor_la_so`. M3u2 bị ca đích giết; descriptor null và hex64 hợp lệ vẫn xanh. |
| F29 | `va_ho` — phản chứng cũ đóng, bản vá sinh lỗi mới | `pure_sys_list`, `pure_module_list`, `pure_io_file`, `pure_posix_spawn` đều suite **rc 1**, đúng ca `tinh` đỏ. Hai ca list đo `trang_thai:false`; tệp đo `open`; process đo `os.posix_spawn`. M1s6–M1s9 đều baseline/gác pass, target đỏ. Tuy nhiên cơ chế vừa thêm còn **F31/F32** bên dưới. |

Lệnh: `python3 -B "$OUT/classifier_stage.py" "$ROOT"`; `python3 -B "$OUT/audit.py" "$ROOT" classifier`; `python3 -B "$OUT/audit.py" "$ROOT" attacks`; `python3 -B "$OUT/supplement.py" "$ROOT" extra`; `python3 -B "$OUT/repair_probes.py" "$ROOT"`. Mỗi driver rc 0; rc các suite đột biến được ghi riêng. Log: `stage.stdout`, `classifier.stdout`, `attacks.stdout`, `extra.stdout`, `repair-probes.stdout`.

Probe cũ quan sát trạng thái trong process cha nay cho delta 0 vì purity chạy ở process con. Không dùng delta 0 đó làm bằng chứng “không có tác dụng phụ”; kết luận dựa trên telemetry và failure của child.

## Findings mới

### F31 — P2 — `tin-dung-gia`: tuple đột biến bị cắt im vẫn được cấp tín dụng

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:445`, hàm `chay_dot_bien`; cơ chế nhiều chỗ mới thêm cho M1s7/F29.

`zip(cu, moi)` dừng theo tuple ngắn hơn. Một neo khai thêm nhưng không có phần thay tương ứng không được kiểm duy nhất, cũng không được áp; phần thay dư cũng bị bỏ. Hai tuple rỗng bỏ toàn bộ phép đột biến nhưng vẫn có thể nhận `equivalent_verified`.

**Đã chạy:**

```text
python3 -B "$OUT/new_mechanisms.py" "$ROOT"        # rc 0
M1s7 gốc:                2 neo / 2 thay -> witness_killed
thêm neo vắng, đủ cặp:   3 neo / 3 thay -> unresolved (0 lần)
thêm cùng neo, thiếu cặp:3 neo / 2 thay -> witness_killed
thừa phần thay:          2 neo / 3 thay -> witness_killed
suite với duy nhất khai báo M1s7 sai 3/2:
  rc=0
  witness_killed 159 · equivalent_verified 9 · unresolved 0
  155/155 ca QUA · 159/159 dot bien GIET

python3 -B "$OUT/multi_empty.py" "$ROOT"           # rc 0
0 neo / 0 thay; source_changed=false -> equivalent_verified
```

Phản chứng 3/2 dùng đúng source HEAD, đúng hàng M1s7 hiện hành, chỉ nối một neo chắc chắn vắng vào tuple `cu`; không sửa mã sản phẩm. Output đầy đủ: [new-mechanisms.stdout](new-mechanisms.stdout), [multi-empty.stdout](multi-empty.stdout). Hàng M1s7 hiện hành 2/2 hợp lệ; finding là bộ phân hạng mới nhận khai báo không được thi hành đầy đủ, không phải cáo buộc hàng hiện hành đã sai.

**Đề xuất:** kiểm hình dạng cặp đột biến tại `chay_dot_bien` trước khi áp: hai tuple phải cùng kiểu, cùng độ dài, không rỗng; lỗi cấu trúc trả `unresolved`. Giữ kiểm neo duy nhất cho từng cặp. Khoá bằng ba control 3/2, 2/3, 0/0 và đối chứng M1s7 2/2. Không chỉ bật `zip(strict=True)` rồi để ngoại lệ thoát ngoài khối xử lý: cách đó dễ đổi tín dụng sai thành crash suite. Không cần thay cơ chế đột biến đơn chuỗi.

### F32 — P2 — `tin-dung-gia`: lỗi tiến trình purity bị coi là pass hoặc bằng chứng giết

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:229`, `:232`, `:235`; consumer `chay_dot_bien` tại `:465`.

`ca_tinh` không kiểm `r.returncode`. Nếu child đã in JSON xanh, lỗi sau đó vẫn pass. Nếu child ném trước khi có JSON, traceback được chuyển thành `TinHieuChotCa("tinh: ... co tac dung phu")`; classifier nhận `witness_killed` dù chưa có telemetry chứng minh vi phạm purity và hàng không khai ngoại lệ được phép. Hai biểu hiện cùng nằm ở việc mất trạng thái hoàn tất/lỗi của tiến trình con mới.

**Đã chạy, bằng tiến trình con thật:**

```text
python3 -B "$OUT/new_mechanisms.py" "$ROOT"        # driver rc 0
baseline:           child rc=0, JSON xanh -> ca_tinh pass
sau JSON: exit(7):  child rc=7, JSON xanh -> ca_tinh pass
sau JSON: ném lỗi:  child rc=1, JSON xanh -> ca_tinh pass
  stderr: RuntimeError: review-child-failure

python3 -B "$OUT/purity_failure.py" "$ROOT"        # driver rc 0
baseline tinh=pass; mutant duong_fixture=pass
child rc=1, stdout='', stderr=RuntimeError: review-unrelated-error
target: TinHieuChotCa: tinh: kiem_json co tac dung phu: {'loi': ...}
disposition: witness_killed
```

Phép đầu chỉ thêm hậu tố lỗi vào `_CON_TINH` trong bộ test được nạp ở scratch; module sản phẩm vẫn đúng HEAD. Phép sau thêm trên bản sao module một ngoại lệ khi nhận `b"{"`; đây là phản chứng phân hạng, không phải lỗi runtime có sẵn trên HEAD. Ngoại lệ ấy vi phạm hợp đồng không-ném, nhưng **không chứng minh tính thuần sai** để cấp tín dụng cho ca `tinh` không khai ngoại lệ. Không giả lập `CompletedProcess`. [Script](purity_failure.py), [log](purity-failure.stdout).

**Đề xuất:** tại biên `ca_tinh`, đòi child hoàn tất rc 0 cùng telemetry hợp lệ trước khi xét kết quả. Phân biệt lỗi probe/ngoại lệ ngoài dự kiến với telemetry chứng minh tác dụng phụ; loại đầu phải làm suite đỏ và disposition `unresolved`, không được dùng chung tín hiệu “giết đúng purity”. Khoá cả lỗi trước JSON, lỗi sau JSON, child bình thường và bốn mutant F29 thật. Chỉ thêm `returncode != 0` rồi ném cùng `TinHieuChotCa` sẽ đóng nhánh pass nhưng giữ nhánh tín dụng giả.

## Runtime

**Không tìm thấy lỗi runtime thật trên HEAD trong các phép đã chạy.**

`python3 -B "$OUT/audit.py" "$ROOT" runtime` rc 0:

- **592 lần gọi API**: 38 trường × 14 giá trị bất thường, cộng 60 mức sâu của nhóm C; `errors: []`.
- **16 mẫu API + CLI**: bytes lỗi/rỗng/BOM, scalar, dữ liệu thừa, surrogate, số lớn, lồng sâu; không ngoại lệ API, CLI chỉ rc 0 hoặc 12.
- Parser thật ném `ValueError` ở số 4301/4500 chữ số và `RecursionError` với mảng/object 1000 tầng; HEAD trả K1 đỏ/CLI 12.
- Suite CLI đo lỗi đối số/tệp vắng trả rc 2. Receipt thật đã kiểm băm trả `ok:true`, đủ năm luật `qua`, CLI rc 0.

F32 là lỗi consumer của probe mới trong test, không được nhập vào danh sách crash sản phẩm HEAD. Tập thử hữu hạn, không chứng minh mọi đầu vào đều an toàn tài nguyên.

## Nợ ngoài phạm vi

**F30 — P3 — `no-ngoai-danh-muc` — `K4-THONG-BAO-STALE`: kế thừa, không chặn merge.** Chủ kho đã ghi nợ; lượt này không săn hoặc chạy lại chiều nghĩa của thông báo stale. HEAD hiện vẫn có thông báo đúng. Owner: chủ kho điều phối successor; hướng xử lý khi mở lại phạm vi: oracle mã nguyên nhân/nghĩa ổn định, tránh ghim toàn văn câu chữ. Không phát sinh nợ ngoài phạm vi mới.

## Đã chạy

Mọi rc trong bảng được đọc từ tiến trình thật; driver 0 không thay rc của phép thử con.

| Lệnh/phạm vi | Rc và bằng chứng dương | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; SHA256 spec/receipt đầu–cuối | 0; khớp toàn bộ định danh ở đầu verdict | passed |
| `python3 -B "$D/doc_receipt_thu_hoi_test.py"` | 0; **155/155 ca, 159/159 mutant**, equivalent 9, unresolved 0 | suite passed; audit cơ chế còn F31/F32 |
| `python3 -B "$D/ci_dang_ky_test.py"` | 0; **22/22 đăng ký, 4/4 launcher contract, 3/3 Ruff contract, 938/938 phản chứng** | passed |
| `python3 -m ruff check --no-cache --select F` trên ba tệp sản phẩm | 0; `All checks passed!` | passed |
| Ruff F trên bytes registry tại base, qua `--stdin-filename` | 0; `All checks passed!`; delta F sản phẩm = 0 | passed |
| `python3 -B "$OUT/supplement.py" "$ROOT" ruff` | driver 0; lint `scripts/tl.py` HEAD/base đều **rc 1**, cùng 12 F821, diagnostics bằng nhau | bare lint failed ở nền; delta passed |
| `python3 -B "$D/packet_loop.py" doctrine-scan --root .` | 0; **10 tệp, 0 chỗ chép doctrine** | passed |
| `python3 -B "$D/packet_loop.py" adr-song --root .` | 0; **50 ADR/50 dòng**, tha thiếu trạng thái ADR-0016 theo cấu hình có sẵn | passed |
| `git diff --numstat origin/master..HEAD` | 0; sản phẩm **3 tệp, +615/−0 = 1+114+500**, dưới ngoại lệ ≤650 | passed trong phạm vi sản phẩm |
| `git diff --check origin/master..HEAD` | 0; không lỗi whitespace | passed |
| `classifier_stage.py`; `audit.py classifier`; `repair_probes.py` | từng driver 0; đối chiếu F25–F28 và bốn mutant F29 như bảng trên | đã đo |
| `audit.py attacks`; `supplement.py extra` | từng driver 0; **5 suite mutant cũ đều rc 1**, đúng target đỏ | phản chứng bị bắt |
| `new_mechanisms.py`; `multi_empty.py`; `purity_failure.py` | từng driver 0; tín dụng sai/child lỗi được tái hiện như F31/F32 | audit failed |
| `audit.py runtime`; CLI receipt thật | driver 0; 592 API không lỗi; 16 CLI rc 0/12; receipt thật rc 0 | passed trong tập thử |
| `python3 -B "$OUT/supplement.py" "$ROOT" registry` | driver 0; consumer nhận suite thật rc 0, bác sáu dòng lệch/zero rc 1, bắt xoá đăng ký | passed |
| Snapshot đầu–cuối | **2302/2302 tệp cùng bytes/hash**, HEAD/tree/status/diff/index không đổi | passed |

Numstat đầy đủ có **18 đường, +3043/−0**: ba đường sản phẩm +615; 15 đường spec/hiện vật review +2428. Không tuyên bố toàn diff chỉ có ba đường. Giữ nguyên dữ kiện chủ kho về trần sản phẩm; không mở audit metadata ngoài phạm vi lượt cuối.

`not_run`: full CI, remote CI, Windows, toàn bộ registry `--chay`. Đã chạy consumer `chay_moi` cho **riêng suite mới**. `skipped`: không dùng check skipped làm bằng chứng pass. Signer tắt bằng `GIT_CONFIG_COUNT=1`, `GIT_CONFIG_KEY_0=commit.gpgsign`, `GIT_CONFIG_VALUE_0=false` trong environment của process kiểm tra, không sửa Git config checkout.

Môi trường đo: Linux x86_64, Python **3.11.15**, Ruff **0.16.9**, codex-cli **0.157.1**. Probe phiên bản Codex rc 0 nhưng cảnh báo không tạo được PATH alias vì filesystem read-only; không bypass hoặc đổi quyền. Ruff lint version và Ruff pin/probe contract là hai phép riêng, không tuyên bố đã chạy lint bằng pin CI. Checkout detached, `core.abbrev=7`; `origin` là mirror local `/home/user/tra-luat`, không truy cập mạng.

Snapshot gồm tracked/untracked/ignored; `.codex/` ignored đã có ở đầu và không đổi. Sandbox thực tế `workspace-write`; checkout được giữ read-only bằng thao tác của reviewer, không tuyên bố sandbox khoá ghi toàn checkout. Snapshot chỉ chứng minh không có delta giữa hai mốc, không chứng minh lịch sử mọi thao tác. Không đo checkout nguồn của Executor. Không có header launcher của chính run để độc lập xác nhận model-version/effort; giữ `advisory_review` theo assignment.

## Lịch sử lớp và điểm dừng

| Slug | Finding và mức còn mở | Kết luận trong phạm vi lượt 4 |
|---|---|---|
| `tin-dung-gia` | F25/F26 đóng; **F31/F32 P2** mới trong cơ chế bản vá | Một lớp, hai finding mới; không được tuyên bố lớp đã đóng. Cần kiểm cấu trúc mutation và completion/error của purity child. |
| `dot-bien-tuong-duong-hoac-thieu` | F27/F28 đóng; bốn biểu hiện cũ F29 đã bị bắt | Không suy thành bảo đảm mọi chiều ngoài phạm vi; F29 ghi `va_ho` vì bản vá sinh F31/F32. |
| `no-ngoai-danh-muc` | **F30 P3** kế thừa | Nợ không chặn merge theo chỉ thị chủ kho. |

Lượt **4/4 kết thúc tại đây**. Hai P2 cần chủ kho human audit quyết định; không chuyển sang vòng Executor–model review thứ năm. Không sửa repository, commit, push, mạng, merge, land hoặc LIVE.
