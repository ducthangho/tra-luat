verdict: approve
reviewed_sha: 2c70821245f777ede564c79e4e4abade0de53ae6

**Approve nội dung bản vá trên exact SHA nêu trên.** Không còn finding P0/P1/P2 đã phát hiện; finding P2 lượt trước và ba mutant sống lượt trước đều **ĐÃ ĐÓNG** bằng phép đo. M1–M3, N1/N2 đạt; bộ kiểm chính `11/11`, dữ liệu thật `23/23`. Bốn mutant mới sống được khai rõ là giới hạn độ phủ. N3 chưa xanh trọn do dịch vụ ký commit bị chặn trong sandbox; N4 chưa đo được. Verdict này không chứng nhận các điều kiện push/land đã đầy đủ.

## Phạm vi, định danh và toàn vẹn

- Reviewer độc lập Codex/họ OpenAI, executor họ Claude theo assignment; lớp `sensitive`, lượt **2/2 cuối**. Thực thi shell cục bộ qua công cụ của phiên API, transport machine. Bundle không có receipt launcher để xác minh riêng model/effort đã phục vụ; không suy danh tính từ actor GitHub.
- Base `74132ce20cb1f9f74e163717908eca384f672dd0`; head ở dòng thứ hai; tree `fe6fd26e912596edb60ae3dfd8db3e7363dabfd9`.
- `sha256sum SPEC.md` → `3d026415193d3f3b1ceef005cdc99fcc73871b0c7539697f82b4b0198f578079`, đúng băm được cấp.
- `git -C cay-kho diff BASE HEAD` và `--numstat` sinh lại khớp từng byte với `diff.patch`, `numstat.txt`: `47 11 ops/kiem_ho_so_land.py`, `137 3 ops/kiem_ho_so_land_test.py`. **2 tệp, 184 dòng thêm ≤ 200**; `ops/land/` không đổi. [Tiền kiểm](evidence/preflight.json).
- Python `3.13.17`; mọi script đo, fixture, mutant và log của reviewer nằm trong `evidence/`. `TMPDIR` trỏ `evidence/tmp`, tắt ghi bytecode. Selftest toàn kho chạy trong clone riêng `evidence/gate-copy`, ghim `core.abbrev=7`, cùng head/tree. Không sửa checkout `cay-kho/`, không push, không truy cập dịch vụ từ xa.
- Các lệnh `python -B evidence/...` dưới đây chạy từ thư mục chứa verdict; các lệnh `python ops/...` chạy với cwd `cay-kho/`. [Nhật ký cập nhật theo hướng](evidence/progress.md).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lệnh dùng chung: `python -B evidence/probe.py mutations` → rc 0; [output thật](evidence/mutations.out), [kết quả có cấu trúc](evidence/mutations.json). Đã chạy 19 ca con trên bản thật, từng mutant trên bản sao riêng và gọi lại bộ chấm hiện hành.

| Finding / mutant lượt 1 | Đo trên head mới | Kết luận |
|---|---|---|
| P2 `mutant-crash-counted-as-kill` | `khoi_sai_kieu_bo_qua → khoi-chuoi`: `('SAI', 'rc 0, BO_QUA (cần 3, LOI)')`, `CRASH=0`, `_giet_dung=True`; mutant lỗi vô can bị từ chối như các dòng dưới | **ĐÃ ĐÓNG** |
| Phản chứng `RuntimeError: REVIEW_UNRELATED_FAULT` | Thay mutant `bo_da_duyet` bằng biểu thức ném RuntimeError, gọi thật `ca_wp981_dot_bien()`: `RUNTIMEERROR_REJECTED đột biến sống/chết sai lý do: ['runtimeerror (đích b-tt)']`; đích được phân loại `CRASH`, `_giet_dung=False` | **ĐÃ ĐÓNG** |
| `skip-sha-pure-b` | Nay có `bo_sha_kieu_b → b-sha-hong`: `SAI`, `DAT (cần TRUOT, phải nêu ('authorized_head_sha',))`, `CRASH=0`, giết đúng | **ĐÃ ĐÓNG** |
| `only-first-active-block` | `chi_khoi_dau → b-hai-khoi`: `SAI`, `DAT (cần TRUOT, phải nêu ('landed_20261028.quyet_dinh_chu_kho.comment',))`, `CRASH=0` | **ĐÃ ĐÓNG** |
| `relax-a-if-active-b` | `noi_a_khi_co_b → ab-khong-manh`: `SAI`, `DAT (cần TRUOT, phải nêu ('authorization_url',))`, `CRASH=0` | **ĐÃ ĐÓNG** |

Ba phản chứng tự kiểm bộ chấm cũng đã chạy: `nem_khi_doc_trang_thai` có 17 `CRASH`; `chet_luc_nap` có 19 `CRASH`; `sai_kem_crash` có đích `b-tt=SAI` nhưng hai ca khối sai kiểu `CRASH`. Cả ba đều `_giet_dung=False`. Như vậy vế loại crash không chỉ bảo vệ riêng ca đích.

**Lời khai mutant tương đương là đúng trong miền kết quả của hàm hiện tại.** Đổi `kq[dich][0] == "SAI"` thành `kq.get(dich) is not None` vẫn giữ chốt `isinstance(..., tuple)` và “không ca nào CRASH”. `_wp981_ket_qua` chỉ sinh `None`, tuple `SAI` hoặc tuple `CRASH`; sau hai chốt còn lại, tuple của đích chỉ có thể là `SAI`. Đã so **428** tổ hợp/đích gồm toàn bộ 27 tổ hợp ba trạng thái, đích vắng và kết quả thực của baseline/các mutant; `EQUIVALENT_TRUE checks=428`. Bản sao test có thay đổi này chạy trọn `11/11`, rc 0 (`EQUIVALENT_SUITE 11/11`). Không coi mutant tương đương này là lỗ độ phủ; lập luận không mở rộng sang tuple tùy ý ngoài miền của producer.

## Đối chiếu M1–M3 từng gạch

| Điều kiện SPEC | Mã và bằng chứng |
|---|---|
| M1: khóa mức gốc fullmatch `landed_\d{8}` | Dòng 100. `names`: 7/9 chữ số, tiền/hậu tố, LF cuối, `landed_x`, khóa lồng đều `BO_QUA/0`; tên chuẩn được nhận. Chữ số Unicode và `99999999` được nhận đúng regex đã đóng băng, không tự thêm kiểm ngày lịch. |
| M1: khóa không phải `str` | Guard `isinstance(k, str)` trước regex/sort; khóa YAML null/bool/int/float/date trong hồ sơ b hợp lệ đều `DAT/0`, không crash (`names`). |
| M1: a OR b, giữ thứ tự đọc a | Dòng 93–105. `matrix_a`: 50 tổ hợp nguồn a × trạng thái b × URL gốc; thêm 8 ca ưu tiên và 5 ca `trang_thai_packet` sai kiểu. Có `trang_thai_packet` thì không fallback về `landed` gốc, kể cả khóa landed bên trong vắng. Sai kiểu packet vẫn `LOI/3`, dù b hợp lệ. |
| M2: khối có tên khớp phải là ánh xạ | Dòng 101–103. `structure`: null/bool/int/float/str/list/set đều `LOI/3`, **cả khi a đã True**. Không dùng a để bỏ qua khối hỏng. N1(v) làm rõ phải bắt cả scalar chưa thể đọc `.get('landed')`. |
| M2: quyết định phải là ánh xạ | Dòng 64–66. Quyết định vắng/null/bool/int/float/str/list/set đều `TRUOT/1`, nêu `<khối>.quyet_dinh_chu_kho` (`structure`). |
| M2: trạng thái đúng chuỗi `da_duyet`, không ép kiểu | Dòng 68–70. null/bool/int/list/dict/bytes, sai hoa thường, khoảng trắng, rỗng đều `TRUOT/1`, nêu `.trang_thai` (`structure`). |
| M2: comment đúng kiểu, tiền tố, mảnh | Dòng 46–47, 71–72. N1(ii) đo thiếu/sai comment; `urls` so 18 đầu vào × base-a/head-a/head-b = **54** kết quả khớp. Điều kiện URL cũ được giữ nguyên, kể cả những chuỗi luật cũ vốn chấp nhận. |
| M2: **mỗi** khối landed True đều phải hợp lệ | Dòng 109–110. Khối hỏng đứng trước/sau khối đúng đều `TRUOT` đúng tên, có/không a cũng vậy. Ba khối hợp lệ chỉ đếm một hồ sơ; khối inactive có quyết định cũ hỏng không làm hồ sơ trượt (`multi_alias`). |
| M2: SHA mức gốc bắt buộc như cũ | Dòng 54–56 luôn chạy; pure b thiếu/số/list/dict/rỗng/39/41 ký tự/chữ hoa/LF cuối đều `TRUOT/1` (`structure`); mutant bỏ SHA riêng cho b chết đúng `b-sha-hong`. |
| M2: pure b không đòi URL gốc | Dòng 108. URL vắng/KHONG_AP_DUNG/bool/số/list/dict/rỗng đều `DAT/0` nếu comment đúng; **cùng đầu vào** xóa comment đều `TRUOT/1`, kể cả URL gốc vắng (`structure`). |
| M2: không nới a ở bất kỳ đường phối hợp nào | `doi_url_goc=landed is True`, dòng 108, phụ thuộc nguồn a đã chọn. a gốc và a nested với URL sai/vắng đều trượt, bất kể b vắng/True/False/chuỗi/số (`matrix_a`). a True + b True phải qua cả luật gốc lẫn từng khối. |
| M2: landed khác `True` không kích hoạt b | Dòng 104 dùng `is True`; False, `"true"`, `1`, `1.0`, null, list/dict và vắng đều `BO_QUA/0` khi a không landed (`names`). |
| M3: DAT/TRUOT nói nguồn landed | Dòng 107, 111–116; a gốc ghi `landed (mức gốc)`, a nested ghi `trang_thai_packet.landed`, b ghi `<khối>.landed`, hồ sơ hỗn hợp ghi cả hai. Kiểm cả kết quả đạt và trượt qua `matrix_a`, N1 và CLI. |
| M3: docstring và MIEN_TRU | Docstring dòng 8–15 giải thích hai kiểu, comment và ngoại lệ URL chỉ cho pure b. `MIEN_TRU` bằng base, đúng một mục pr672; `TRUOT` ở mục ấy được miễn, `LOI` không được miễn, miễn trừ trỏ tệp vắng vẫn rc 3 (`cli`). |
| Không đổi mã thoát và `--json` | `cli`: text/JSON cùng rc 0/1/3; lỗi cùng trượt → 3; root sai + thiếu PyYAML → 2 trước quét. Schema khóa ngoài và từng dòng không đổi; nội dung `ly_do` đổi đúng M3. Phần tính rc/CLI không có diff. |

[Script tái chạy](evidence/probe.py); dữ liệu đầy đủ: [matrix_a](evidence/matrix_a.json), [names](evidence/names.json), [structure](evidence/structure.json), [urls](evidence/urls.json), [multi_alias](evidence/multi_alias.json), [cli](evidence/cli.json).

## N1: có mặt, có đo, đột biến chết đúng lý do

Lệnh `python -B evidence/probe.py mutations` chạy từng fixture riêng để lấy rc thực, rồi dùng bộ chấm hiện hành trên mỗi bản sao đột biến. Baseline: **19/19 ca con** (17 thường + 2 LOI); không bỏ qua ca. **11/11 mutant ngữ nghĩa giết đúng**, đích `SAI`, không có ca `CRASH` trong mỗi lượt.

| N1 | Ca trong test | Output bản thật | Mutant → output đích |
|---|---|---|---|
| (i) | `b-du` | `DAT/0` | `bo_nhanh_b` → `BO_QUA`, `SAI` |
| (ii) | `b-cmt-manh`, `b-cmt-tien-to`, `b-cmt-so`; thiếu comment ở `b-kad-cmt-vang` | Đều `TRUOT/1`, đúng `.comment` | `bo_kiem_comment` → `b-cmt-manh=DAT`, `SAI` |
| (iii) | `b-tt` | `TRUOT/1`, đúng `.trang_thai` | `bo_da_duyet` → `DAT`, `SAI` |
| (iv) | `b-landed-chuoi`, `b-landed-mot` | Đều `BO_QUA/0` | `ep_kieu_landed_khoi` → `b-landed-chuoi=DAT`, `SAI` |
| (v) | `khoi-chuoi`, `khoi-ds` | Đều `LOI/3` | `khoi_sai_kieu_bo_qua` → `BO_QUA/0`, `SAI`, **không AttributeError** |
| (vi) | `a-khong-manh` | `TRUOT/1`, `authorization_url` | `noi_kieu_a` → `DAT`, `SAI` |
| (vii) | `ten-7so`, `ten-x` | Đều `BO_QUA/0` | `noi_ten_khoi` → `ten-x=DAT`, `SAI` |
| (viii) | `b-kad`, `b-vang-url`, `b-kad-cmt-vang` | `DAT/0`, `DAT/0`, `TRUOT/1` | `doi_url_goc_kieu_b` → `b-kad=TRUOT`, `SAI` |

Các ca bổ sung `b-ab`, `b-sha-hong`, `b-hai-khoi`, `ab-khong-manh` cũng đã đo độc lập. Tổ hợp URL gốc vắng + comment vắng chưa nằm trong bảng WP981 của repository; reviewer đã đo nó trong `structure`, kết quả `TRUOT/1` đúng khóa. Bốn mutant bắt buộc của SPEC đều chết bằng sai khác hành vi; ba mutant mới đóng lỗ lượt trước được ghi tại mục đối chiếu.

## Bốn đột biến KHÁC do reviewer tự viết

Lệnh: `python -B evidence/probe.py own` → rc 0 của script đo; [output](evidence/own.out), [neo/thay, stdout và phản chứng](evidence/own.json). Bốn mutant mới khác các mutant lượt 1 và `DOT_BIEN_WP981`; chạy trên bản sao nằm ngoài checkout.

Đo bằng **10 ca kiểm hành vi** hiện có (9 cũ + `ca_wp981_kieu_b`); chỉ bỏ `ca_wp981_dot_bien` vì nó tự tạo mutant và kiểm số lần khớp mẫu nguồn, không phải phép đo hành vi của candidate. Baseline cũng đạt `10/10`. Không gọi kết quả này là chạy trọn suite `11/11` trên mutant.

| Mutant riêng | Thay đổi | Bộ kiểm hành vi hiện có | Phản chứng reviewer: bản thật → mutant |
|---|---|---|---|
| `ignore-nonmapping-decision` | Quyết định không phải dict trả danh sách lỗi rỗng | **SỐNG: 10/10, rc 0** | b active, quyết định `[]`: `TRUOT/1 → DAT/0` |
| `ignore-bad-block-when-a` | Khi a True, loại khối không phải dict khỏi danh sách nhận diện | **SỐNG: 10/10, rc 0** | a hợp lệ + khối tên đúng là chuỗi: `LOI/3 → DAT/0` |
| `prefix-match-block-name` | Nhận tên khối bằng `match` thay `fullmatch` | **SỐNG: 10/10, rc 0** | `landed_20261027suffix`: `BO_QUA/0 → DAT/0` |
| `accept-true-approval` | Chấp nhận thêm `trang_thai is True` | **SỐNG: 10/10, rc 0** | b active, trạng thái bool True: `TRUOT/1 → DAT/0` |

Đây là **giới hạn độ phủ còn lại**, không phải bốn lỗi của mã sản phẩm trên head thật: từng phản chứng chạy trên head đều cho kết quả đúng SPEC. Các ca N1 bắt buộc và mutant riêng cho chúng đã đạt. Có thể dùng các fixture trong `own.json` để tăng độ phủ về sau; không gán hành vi mutant cho bản vá được review.

## Bảng SĂN — các hướng độc lập

Các lệnh đều đã chạy; output dưới đây trích log thật, không lấy việc đếm dòng/băm SPEC/chạy nguyên suite làm hướng săn. Mỗi script trả rc 0 vì các khẳng định của phép đo đều đạt.

| Hướng / giả thuyết | LỆNH | OUTPUT THẬT | Kết luận |
|---|---|---|---|
| B dùng để nới luật a hoặc đổi ưu tiên nguồn | `python -B evidence/probe.py matrix_a` | `ALL_ASSERTIONS_PASSED matrix_a records=63`; URL gốc sai vẫn `TRUOT/1`; `nested-precedence-{'landed': 'true'} BO_QUA rc=0`; thêm b → `DAT/0`; packet sai kiểu → `LOI/3` | **KHÔNG PHẢI LỖI** — [log](evidence/matrix_a.out) |
| Tên khối nhận nhầm, khóa không str làm crash, truthy thay True | `python -B evidence/probe.py names` | `ALL_ASSERTIONS_PASSED names records=24`; hậu tố/LF cuối → `BO_QUA/0`, khóa không str → `DAT/0`; `strict-boolean-1 BO_QUA rc=0` | **KHÔNG PHẢI LỖI** — [log](evidence/names.out) |
| Sai kiểu cấu trúc bị bỏ qua hoặc SHA/URL gốc lấn thẩm quyền khối | `python -B evidence/probe.py structure` | `ALL_ASSERTIONS_PASSED structure records=54`; khối sai kiểu với a True → `LOI/3`; quyết định/trạng thái sai → `TRUOT/1`; pure b URL gốc `{}` + thiếu comment → `TRUOT/1` | **KHÔNG PHẢI LỖI** — [log](evidence/structure.out) |
| Tách helper làm lệch điều kiện URL so với base | `python -B evidence/probe.py urls` | `ALL_ASSERTIONS_PASSED urls records=54`; 18 giá trị × ba đường base-a/head-a/head-b cùng kết quả | **KHÔNG PHẢI LỖI** — [log](evidence/urls.out) |
| Bỏ khối active thứ hai, đếm trùng hoặc dùng quyết định inactive | `python -B evidence/probe.py multi_alias` | `multi-bad-landed_20261028-a=True TRUOT rc=1`; `three-active DAT rc=0`, JSON `n_landed=1`; b inactive mang quyết định hỏng vẫn `DAT/0` | **KHÔNG PHẢI LỖI** — [log](evidence/multi_alias.out) |
| Alias/đệ quy YAML và thứ tự serialization làm thay kết quả | `python -B evidence/probe.py multi_alias` | `alias-valid DAT rc=0`; `alias-invalid TRUOT rc=1`; `alias-recursive TRUOT rc=1`; `JSON_IDENTICAL_ALL_6_PERMUTATIONS` | **KHÔNG PHẢI LỖI** — [log](evidence/multi_alias.out) |
| Đổi rc, JSON hoặc dùng MIEN_TRU để che LOI | `python -B evidence/probe.py cli` | `mixed json_rc=text_rc=3 schema=unchanged`; `missing-yaml rootbad=True json=True rc=2`; `exempt MIEN_TRU rc=0`; `exempt LOI rc=3`; `missing-exempt rc=3` | **KHÔNG PHẢI LỖI** — [log](evidence/cli.out) |
| Bộ chấm tiếp tục cấp tín dụng giả cho crash vô can | `python -B evidence/probe.py mutations` | `RUNTIMEERROR_REJECTED`; `sai_kem_crash ... CRASH=2 giet_dung=False`; 11 mutant ngữ nghĩa `CRASH=0 giet_dung=True` | **KHÔNG PHẢI LỖI** trên head mới — [log](evidence/mutations.out) |

## N2: đo nền và sáu hồ sơ thật

```text
python ../evidence/base-tool.py --root .
TỔNG: 17/17 hồ sơ landed True đạt · 0 miễn trừ · rc=0

python ops/kiem_ho_so_land.py --root .
TỔNG: 23/23 hồ sơ landed True đạt · 0 miễn trừ · rc=0
```

`base-tool.py` lấy bằng `git -C cay-kho show 74132ce20cb1f9f74e163717908eca384f672dd0:ops/kiem_ho_so_land.py`. Đo cùng tập dữ liệu thật; `ops/land/` không có diff nên đúng tập ở base.

| Hồ sơ | Base | Head |
|---|---|---|
| pr870-claude-md-bai-hoc-c | BO_QUA | DAT |
| pr889-claude-md-bai-hoc-c | BO_QUA | DAT |
| pr896-claude-md-bai-hoc-c-tro-nguon | BO_QUA | DAT |
| pr924-wp923 | BO_QUA | DAT |
| pr950-wp834 | BO_QUA | DAT |
| pr963-wp943 | BO_QUA | DAT |

Log đầy đủ: [base](evidence/base-real.json), [head](evidence/head-real.json), [base JSON](evidence/base-json.json), [head JSON](evidence/head-json.json).

## N3/N4 — trạng thái đo thật

| Cổng / lệnh | Output và rc | Trạng thái |
|---|---|---|
| `python -B ops/kiem_ho_so_land_test.py` | `11/11`, rc 0 | **passed** — [log](evidence/tests.json) |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`, rc 0 | **passed** — [log](evidence/doctrine.json) |
| `git diff --check BASE HEAD` | stdout/stderr rỗng, rc 0 | **passed** — [log](evidence/diff-check.json) |
| `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) | `ĐĂNG KÝ: 28/28`, `TRẠNG THÁI: chan=28 cach_ly=0`, `LAUNCHER WINDOWS: 4/4 hợp đồng`, `RUFF CI: 3/3 hợp đồng`; sau đó git commit kho tạm rc 128, Python rc 1 | **failed trong môi trường hiện tại**, chưa có `TỔNG: ĐẠT` — [log](evidence/registry.json) |
| `python scripts/tl.py --selftest` trên clone cùng head/tree | `== tl selftest 1729/1731 ==`, rc 1, 204.615 giây | **failed trong môi trường hiện tại** — [log](evidence/selftest.json) |
| N4 check run `ci.yml` trên exact head | Không có receipt check run trong gói; assignment cấm mạng | **not_measured / KHÔNG ĐO ĐƯỢC**, không coi là pass |

`python -B evidence/diagnose_registry.py` lấy được stderr gốc: dịch vụ ký commit cục bộ báo `socket: operation not permitted`, `fatal: failed to write commit object` ([bằng chứng](evidence/registry-diagnosis.json)). Không tắt ký hoặc đổi quyền để làm cổng xanh. Thiếu bằng chứng N3/N4 không được dùng để khai đủ điều kiện push/land.

Hai ca selftest đỏ là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`. Lệnh `python -B evidence/diagnose_selftest.py` trích đúng thân hai hàm bằng AST, chạy riêng với module thật và quan sát các lệnh git, không thay kết quả subprocess:

```text
RESULTS {'_c226_nguong_l2_troi_theo_abbrev_va_ci_ghim': False,
         '_c268_l2_trichotomy_theo_trang_thai_object': False}
COMMIT_RCS [128, 128, 128]
COMMIT_ERRORS ['fatal: failed to write commit object',
               'fatal: failed to write commit object',
               'fatal: failed to write commit object']
SIGNING_SOCKET_DENIED True
BASE_HEAD_IDENTICAL {'scripts/tl.py': True, 'scripts/tl_selftest.py': True,
                    '.claude/dev/ci_dang_ky_test.py': True, '.github/workflows/ci.yml': True}
```

[Bằng chứng gốc từng lệnh commit](evidence/selftest-diagnosis.json). Các ca này và registry thất bại cùng cơ chế ký commit cục bộ, không phải sai khác do hai tệp của packet. Không chạy lại trọn selftest trên base, không khai N3 đạt hoặc delta toàn suite đã đo trên hai commit. Không có network/check-run receipt để xác minh N4; bên điều phối vẫn cần bằng chứng N3/N4 hợp lệ theo SPEC trước bước tương ứng.

## Finding và bàn giao cuối lượt

**Không có finding P0/P1/P2 mới hoặc còn mở trong phạm vi diff.** Finding `mutant-crash-counted-as-kill [P2]` đã đóng; ba mutant sống lượt 1 đã có ca khóa và chết đúng lý do. Bốn mutant sống mới là các khuyến nghị tăng độ phủ, không nâng thành lỗi sản phẩm hoặc điều kiện N1 không đạt. Không đính HINT.patch và không sửa mã executor.

Đã kiểm lại `git -C cay-kho rev-parse HEAD`, `HEAD^{tree}`, diff working/index, danh sách untracked/ignored và bytes hai tệp so với blob HEAD: SHA/tree giữ nguyên, tất cả diff/danh sách rỗng, hai tệp khớp HEAD. [Tính toàn vẹn cuối](evidence/integrity-final.json). Checkout gốc không cần hoàn nguyên.
