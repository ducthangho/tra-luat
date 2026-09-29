<!-- Verdict codex lượt 4/4 (gpt-6-astra, reasoning effort xhigh — header log runtime "reasoning effort: xhigh", session 01a0e5a8-841c-76e0-8d4a-be68da24b4f4), codex_cli tại chỗ, sandbox clone riêng, trên a004a236 (tree cfe98aa), base ceb1a3f3, spec sha256 978058983e8e…. Phạm vi HẸP theo quyết định chủ kho "Vá + Codex lượt 4". Chép NGUYÊN VĂN; không sửa chữ nào. Đường /tmp/review650-r4-output/* là đường trong sandbox reviewer; bản sao script nằm cạnh tệp này. -->
**0 P1 / 2 P2 / 1 P3**

verdict: changes_requested

```yaml
reviewed_sha: a004a23628a13bc1add0ae40b0318063406e3bad
reviewed_tree: cfe98aa3e2755a9cd8c25b9d6be3d1fd3c6a95f2
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
provider: openai_codex
execution_surface: codex_cli
transport: machine
assurance: advisory_review
round: 4/4
```

Các băm khớp đầu–cuối. Đã lưu [verdict đầy đủ](/tmp/review650-r4-output/VERDICT.md) và [manifest bằng chứng](/tmp/review650-r4-output/ARTIFACTS.sha256); **114/114 băm khớp**.

F25–F28 đã vá thật. Bốn phản chứng cũ của F29 đều bị bắt, nhưng cơ chế mới sinh F31/F32. **Dừng vòng model tại 4/4, chuyển human audit của chủ kho.**

## Đối chiếu lượt 3

| Finding | Trạng thái | Bằng chứng tự đo |
|---|---|---|
| F25 | `da_va_that` | Phản chứng đúng dòng nhưng sau K1 đỏ cho `NEM:UnicodeDecodeError@76#1`, nay `unresolved`. Đúng giai đoạn 0 được nhận; sai loại/dòng/giai đoạn, neo trùng và tuple hai phần bị bác. |
| F26 | `da_va_that` | Cả bốn mutant giữ **10/11 ca dương xanh**, gồm `duong_fixture`; chỉ đích `duong_c_khac_s` đỏ. Gác vắng, âm, `None` hoặc trùng đích đều bị bác. |
| F27 | `da_va_that` | M1o3/M1x3 đã có; baseline và gác xanh, mutant thất bại đúng `bom`, disposition `witness_killed`. |
| F28 | `da_va_that` | Mutant ép số hex64 cũ nay suite rc 1, đỏ đúng `hex64_la_so` và `descriptor_la_so`. Nullable và hex64 hợp lệ vẫn xanh. |
| F29 | `va_ho` | Bốn mutant cũ đều suite rc 1, đúng `tinh` đỏ. Tuy nhiên bản vá sinh F31/F32 dưới đây; không đếm thêm F29 thành P2 thứ ba. |

Đã chuyển phép đo ngoại lệ sang bộ ba mới. Script thích ứng và thay đổi phạm vi được lưu trong [adaptations.patch](/tmp/review650-r4-output/adaptations.patch).

## Findings mới

Trong các lệnh dưới, `ROOT` là checkout được giao, `OUT=/tmp/review650-r4-output`.

### F31 — P2 — `tin-dung-gia`

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:445`.

Cơ chế đột biến nhiều chỗ dùng `zip(cu, moi)`, bỏ im phần dư khi hai tuple khác độ dài. Neo bị bỏ không được kiểm hoặc áp nhưng hàng vẫn nhận tín dụng.

**Đã chạy:**

```text
python3 -B "$OUT/new_mechanisms.py" "$ROOT"
rc=0

M1s7 gốc:                 2 neo / 2 thay -> witness_killed
thêm neo vắng, đủ cặp:    3 neo / 3 thay -> unresolved
thêm cùng neo, thiếu cặp: 3 neo / 2 thay -> witness_killed
thừa phần thay:           2 neo / 3 thay -> witness_killed

Suite với duy nhất khai báo M1s7 sai 3/2:
rc=0
155/155 ca · 159/159 đột biến · unresolved 0
```

```text
python3 -B "$OUT/multi_empty.py" "$ROOT"
rc=0
0 neo / 0 thay; source_changed=false -> equivalent_verified
```

Hàng M1s7 hiện hành hợp lệ; lỗi nằm ở việc bộ phân hạng nhận khai báo không được thực hiện đầy đủ.

**Đề xuất:** kiểm hai tuple cùng độ dài, không rỗng và đúng kiểu trước khi áp; lỗi cấu trúc trả `unresolved`. Khoá bằng các ca 3/2, 2/3, 0/0 cùng đối chứng 2/2. Tránh chỉ bật `zip(strict=True)` rồi để ngoại lệ làm crash suite.

### F32 — P2 — `tin-dung-gia`

**Tệp:dòng:** `.claude/dev/doc_receipt_thu_hoi_test.py:229–235`; consumer tại dòng 465.

`ca_tinh` không kiểm mã thoát child. Lỗi sau JSON xanh vẫn pass; lỗi trước JSON lại bị chuyển thành tín hiệu “vi phạm purity” và được tính giết.

**Đã chạy bằng tiến trình con thật:**

```text
python3 -B "$OUT/new_mechanisms.py" "$ROOT"
driver rc=0

baseline:          child rc=0, JSON xanh -> pass
exit sau JSON:     child rc=7, JSON xanh -> pass
ném sau JSON:      child rc=1, JSON xanh -> pass
stderr: RuntimeError: review-child-failure
```

```text
python3 -B "$OUT/purity_failure.py" "$ROOT"
driver rc=0

baseline tinh=pass; mutant duong_fixture=pass
child rc=1, stdout=''
stderr: RuntimeError: review-unrelated-error
disposition: witness_killed
```

Phản chứng sau chỉ làm bản sao ném khi nhận `b"{"`. Nó vi phạm hợp đồng không-ném, nhưng **không chứng minh có tác dụng phụ** để cấp tín dụng cho ca `tinh` không khai ngoại lệ. Đây không phải crash có sẵn trong sản phẩm HEAD.

**Đề xuất:** đòi child hoàn tất rc 0 cùng telemetry hợp lệ; phân biệt lỗi probe/ngoại lệ ngoài dự kiến với bằng chứng tác dụng phụ. Lỗi probe phải làm suite đỏ và disposition `unresolved`. Khoá cả lỗi trước/sau JSON, child bình thường và bốn mutant F29. Chỉ thêm kiểm rc rồi ném cùng `TinHieuChotCa` sẽ giữ lại nhánh tín dụng giả.

## Runtime

**Chưa tìm thấy lỗi runtime thật trên HEAD trong tập đã thử.**

`audit.py runtime`, rc 0:

- **592 lần gọi API**, `errors: []`.
- **16 mẫu API + CLI**: không ngoại lệ API; CLI chỉ rc 0 hoặc 12.
- Số quá dài và JSON sâu gây lỗi parser thật, được HEAD chuyển thành K1 đỏ/CLI 12.
- Suite xác nhận lỗi tham số/tệp vắng trả 2.
- Receipt thật khớp băm, CLI rc 0, `ok:true`, đủ năm luật `qua`.

## Nợ ngoài phạm vi

**F30 — P3 — `no-ngoai-danh-muc` — `K4-THONG-BAO-STALE`**: nợ kế thừa, **không chặn merge**. Không chạy lại hoặc mở rộng chiều này. Chủ kho điều phối xử lý khi mở phạm vi; nên kiểm mã nguyên nhân/nghĩa ổn định thay vì ghim câu chữ.

## Đã chạy

| Lệnh/phạm vi | Rc và kết quả |
|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; băm spec/receipt | 0; khớp đầu–cuối |
| `python3 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **155/155 ca · 159/159 mutant**, equivalent 9, unresolved 0 |
| `python3 -B .claude/dev/ci_dang_ky_test.py` | 0; **22/22 đăng ký, 4/4 launcher, 3/3 Ruff contract, 938/938 phản chứng** |
| Ruff `--no-cache --select F` ba tệp sản phẩm và registry tại base | 0; delta F=0 |
| Ruff F `scripts/tl.py` HEAD/base | Cả hai rc 1, cùng 12 F821; diagnostics bằng nhau, **delta=0** |
| `packet_loop.py doctrine-scan --root .` | 0; 10 tệp, 0 chỗ chép doctrine |
| `packet_loop.py adr-song --root .` | 0; 50 ADR/50 dòng |
| `git diff --numstat origin/master..HEAD` | 0; sản phẩm **+615/−0 trên ba tệp**, dưới trần 650 |
| `git diff --check origin/master..HEAD` | 0 |
| `classifier_stage.py`; `audit.py classifier/attacks/runtime`; `repair_probes.py`; `supplement.py extra/registry` | Mỗi driver 0; rc con và output lưu riêng |
| `new_mechanisms.py`; `multi_empty.py`; `purity_failure.py` | Mỗi driver 0; tái hiện F31/F32 |
| Snapshot đầu–cuối | **2302/2302 tệp không đổi**, HEAD/tree/diff/index không đổi |

Numstat toàn diff là **18 đường, +3043/−0**, gồm ba tệp sản phẩm +615 và 15 đường spec/hiện vật review +2428.

**not_run:** full CI, remote CI, Windows, toàn bộ registry `--chay`; đã chạy consumer cho riêng suite mới. Không tính skipped thành pass. Signer chỉ tắt bằng environment của process, không sửa Git config.

Môi trường: Linux, Python 3.11.15, Ruff 0.16.9, codex-cli 0.157.1. Không xác minh lease/comment live qua mạng hoặc model/effort qua header launcher; giữ `advisory_review`. Không sửa repository, commit, push hoặc gọi mạng.