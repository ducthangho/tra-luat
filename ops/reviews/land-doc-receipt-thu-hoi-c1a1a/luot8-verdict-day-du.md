**0 P1 / 0 P2 / 0 P3**

verdict: approve

```yaml
packet: LAND-DOC-RECEIPT-THU-HOI-C1a1a
issue: 650
review_round: 8
reviewed_sha: cb9ecc8606a7d4b237a5b20702c04f096af2d0e6
reviewed_tree: 675b9a75ed5e00071163f3a451ac03131ab3e92a
base: ceb1a3f36912dd4f03fe1741c443cd09e82a44ee
previous_reviewed_sha: 55619d8e9ddc9dd4e7ad3ab9ba6c43d64679a45a
spec_revision: 5
spec_sha256: 978058983e8eddefebfba267dbff2ef5cee95daf9b2d4847121d43b8cff89d77
receipt_sha256: ca67dc6a817b7cf8643616e4762d5f3e95c0ec7a46cf9693f9436b47c00f5960
review_class: sensitive
assurance: advisory_review
provider: openai_codex
execution_surface: codex_cli
transport: machine
executor: Claude (assignment)
review_axes: [spec, standards_security]
```

**F41 đã vá thật.** Hai mutant nguyên cơ chế lượt 7 nay bị oracle K4 bắt; không tìm thấy lỗ mới trong bản vá được giao. `re \s` và `str.lstrip()` có cùng tập khoảng trắng trên cả bốn Python đã chạy. M5g phân biệt được bộ lọc cũ/mới và chết đúng assertion ngữ nghĩa. Ba driver runtime và các gate yêu cầu đạt trong phạm vi đo dưới đây. Không có finding F42 trở đi.

`approve` là kết luận **lượt 8 hẹp**, giữ mức `advisory_review`; không tự tạo `cross_approved`, quyền merge hoặc land, không mở rộng thành audit lại toàn Packet.

## Mỏ neo, authority và phạm vi

Đo đầu/cuối bằng `git rev-parse HEAD 'HEAD^{tree}' origin/master`: khớp khối trên. `git show -s --format='%H %P %T' HEAD` xác nhận parent duy nhất là `55619d8e9ddc9dd4e7ad3ab9ba6c43d64679a45a`; `git rev-list --count 55619d8..HEAD` trả **1**. Spec blob tại `HEAD:ops/specs/LAND-DOC-RECEIPT-THU-HOI-C1a1a.md` và bản trên đĩa cùng băm được cấp. Receipt thật có đúng băm, kích thước **1863 byte**. Nguồn số đo: [facts.json](facts.json), [snapshot-before.json](snapshot-before.json), [snapshot-after.json](snapshot-after.json).

Authority nhận trực tiếp từ chủ kho trong assignment ngày 28-09-2026, dẫn [#650 comment 5862692098](https://github.com/ducthangho/tra-luat/issues/650#issuecomment-5862692098), lựa chọn “(a) lượt 8 hẹp xác nhận F41”. Không gọi mạng để đọc lại comment, lease, generation hoặc CI. Generation/lease live: **không đo độc lập**; không tự suy quyền thi công từ dữ liệu lịch sử. Căn cứ thực hiện lượt advisory offline là chỉ thị trực tiếp hiện hành. Trần sản phẩm **≤650** và write set nhận theo assignment; không dùng trần 400 lịch sử trong spec để bác chỉ thị mới.

Checkout detached, `core.abbrev=7`; origin là mirror local được cấp `/home/user/tra-luat`. Tên kho đích `ducthangho/tra-luat` theo assignment; không dùng URL mirror làm bằng chứng endpoint GitHub. Base được đo là ref local đã ghim, không khai là đã fetch master mới nhất. Sandbox thực tế `workspace-write`; reviewer giữ checkout read-only bằng thao tác, ghi output/cache/mutant ngoài cây. Không dùng reviewer Claude hoặc subagent.

Phạm vi: F41, cơ chế `git diff 55619d8..cb9ecc8 -- .claude/dev`, ba driver runtime và các gate chỉ định. Diff sản phẩm chỉ đổi `.claude/dev/doc_receipt_thu_hoi_test.py:93`, `:94`, `:386`; runtime module và registry không đổi ở commit vá. [Diff](patch.stdout), [danh sách đường đổi](patch-paths.stdout).

## Đối chiếu lượt 7

Nguồn: `ops/reviews/land-doc-receipt-thu-hoi-c1a1a/luot7-VERDICT.md` và `luot7-verdict-day-du.md` trên `55619d8e…` — **0 P1 / 0 P2 / 1 P3**, F41 thuộc lớp `oracle-k4-bo-sot-ly-do` kế thừa F40. Không mở lại F38/F39 đã đóng ở lượt 7.

| Finding | Trạng thái | Bằng chứng tự chạy trên HEAD |
|---|---|---|
| **F41 — P3 — `oracle-k4-bo-sot-ly-do`** | **da_va_that** | Đúng `patch_mechanisms.py ROOT k4` của lượt 7, chỉ đổi mỏ neo bộ lọc cũ sang mới: hai mutant `space_prefix` và `tab_prefix` nay đều **suite rc 1**, **152/156 ca**, **162/171 mutant**, `unresolved 9`. `k4_base`, `k4_ca_hai`, `a11_k3_k4`, `kieu_S` đỏ đúng `ly do K4 sai nghia`; fixture dương và ca không có S lệch vẫn qua. Lời stale hợp lệ thụt đầu space/tab/NBSP qua đối chứng executor; mở rộng 29 ký tự trắng và tổ hợp cũng qua. Không thấy biểu hiện mới cùng cơ chế trong phạm vi đo. |

Đã đối chiếu **19/19** script đầu vào khi chép ra OUT; **4/4** script có tên `luot7-*` tương ứng trong kho khớp byte. Riêng `executor_thut_dau.py` chép nguyên từ `luot7-executor-thut_dau.py`. [input-identity.json](input-identity.json) lưu băm nguồn. Script runtime và `audit.py` giữ nguyên; chỉ gọi nhánh được giao.

Phép đo F41 không đổi payload hoặc assertion. Thay duy nhất dòng neo trong bản sao `patch_mechanisms.py` để nó tìm được `if re.match(r"\s*K4\b", x)` trên HEAD. [Diff thích nghi mỏ neo](patch-mechanisms-anchor.diff). Không chạy assert cũ để rồi tính lỗi setup thành finding.

Lệnh thực tế (cwd là checkout được giao; `ROOT` là đường tuyệt đối trong [facts.json](facts.json), `OUT=/tmp/review650-r8-output`):

```text
python3.12 -B "$OUT/patch_mechanisms.py" "$ROOT" k4
```

Driver **rc 0**; rc hai suite mutant lồng là **1**, giữ riêng trong [k4-mechanisms.stdout](k4-mechanisms.stdout). Ví dụ output:

```text
HONG k4_base: ly do K4 sai nghia: ['K4: S stale, chay lai', '\tK4:S fresh, khong can chay lai']
nghia vu: witness_killed 162 · equivalent_verified 0 · unresolved 9
doc_receipt_thu_hoi tests: 152/156 ca QUA · 162/171 dot bien GIET
```

`unresolved 9` là hậu quả chạy cả suite trên module cố ý phát lý do sai: các mutant tương đương không còn vượt được toàn bộ ca. Bằng chứng đích đóng F41 là lỗi ngữ nghĩa K4 cụ thể, không chỉ tổng suite đỏ. Bản sao mutant giữ tại [k4_space_prefix](k4_space_prefix/) và [k4_tab_prefix](k4_tab_prefix/), logs [space](k4_space_prefix.log), [tab](k4_tab_prefix.log).

## Kiểm chính bản vá

### Tập khoảng trắng và nhãn luật

Đã chạy độc lập trên **Python 3.10.20 / 3.11.15 / 3.12.3 / 3.13.12**:

```text
python3.<v> -B "$OUT/whitespace_k4.py" "$ROOT"
```

Mỗi lệnh **rc 0**. Script duyệt **1.114.112** mã từ U+0000 tới U+10FFFF, gồm cả vùng surrogate, so hai predicate `re.fullmatch(r"\s", c)` và `c.lstrip() == ""`; đồng thời so nhận nhãn thật `re.match(r"\s*K4\b", c + "K4:S fresh")` với nhận nhãn sau `lstrip()`.

| Python | Unicode database | `re \s` | `lstrip()` | Lệch tập / lệch nhận nhãn |
|---|---|---:|---:|---:|
| 3.10.20 | 13.0.0 | 29 | 29 | 0 / 0 |
| 3.11.15 | 14.0.0 | 29 | 29 | 0 / 0 |
| 3.12.3 | 15.0.0 | 29 | 29 | 0 / 0 |
| 3.13.12 | 15.1.0 | 29 | 29 | 0 / 0 |

Tập đo được giống nhau ở bốn runtime: U+0009–000D, U+001C–001F, U+0020, U+0085, U+00A0, U+1680, U+2000–200A, U+2028–2029, U+202F, U+205F, U+3000. Không nhầm tập này với một danh sách “Unicode whitespace” khác từ bên ngoài. Code HEAD dùng regex `str` không cờ ASCII; lời lý do đã được `kiem_kq` chặn kiểu khác `str`.

Sau phép so tập, script gọi **oracle thật của HEAD** qua module proxy chỉ biến đổi `ly_do` sau lời gọi runtime. **873 tiền tố** = rỗng + 29 ký tự trắng đơn + mọi 841 cặp có thứ tự + hai chuỗi chứa đủ 29 ký tự xuôi/ngược. Mỗi tiền tố đo bốn chế độ × bảy ca (`duong_fixture`, `k4_base`, `k4_head`, `k4_ca_hai`, `a11_k3_k4`, `kieu_S`, `kieu_H`), tổng **24.444 lời gọi mỗi Python**, không lệch kỳ vọng:

- Lý do K4 stale hợp lệ được thêm tiền tố: qua tất cả.
- Giữ lý do stale đúng và thêm lý do K4 fresh có tiền tố khi K4 đỏ: mọi ca đích đỏ đúng assertion K4; fixture dương qua.
- Thêm `K40:S fresh`: không bị vơ vào K4; bảy ca vẫn qua.
- Thêm `K3: workflow co K4 trong ten`: không bị vơ vào K4; bảy ca vẫn qua.

Như vậy không tìm được ký tự được bộ lọc nhận nhưng `lstrip()` giữ lại, hoặc ký tự bị bộ lọc bỏ nhưng `lstrip()` loại. Vì cả hai phép chỉ tiêu thụ tiền tố gồm các ký tự của cùng tập, kết quả phù hợp cả phép so từng ký tự lẫn ma trận tiền tố thực. Đây là kết luận trên bốn runtime đo được, không cam kết cho mọi implementation Python tương lai.

Logs: [3.10](unicode-3.10.stdout), [3.11](unicode-3.11.stdout), [3.12](unicode-3.12.stdout), [3.13](unicode-3.13.stdout). Script kiểm đích có assertion, không chỉ in kết quả.

Đối chứng executor được chạy lại nguyên byte:

```text
python3.12 -B "$OUT/executor_thut_dau.py" "$ROOT"
```

**rc 0**, cả space/tab/NBSP × sáu ca đều `pass`, [output](executor-thut-dau.stdout). Phép `patch_mechanisms.py k4` cũng giữ 16 biến thể tiếng Việt hợp lệ và các đối chứng `fresh`, hậu tố ngược nghĩa, lý do trùng, K40/K3 của lượt 7; không mất răng ở những đối chứng ấy. Không mở miền diễn đạt ngôn ngữ tự nhiên ngoài phạm vi này.

### M5g có phân biệt và chết đúng lý do

Đã chạy:

```text
python3.12 -B "$OUT/m5g_discrimination.py" "$ROOT"
```

**rc 0**. Dùng **nguyên hàng M5g của HEAD**, payload trong module sau giải mã là tab thật trước `K4:S fresh`. Trên bản sao test ngoài checkout chỉ đổi điều kiện nhận nhãn, giữ phần `x.lstrip()` và mọi phần còn lại của HEAD để cô lập hiệu ứng bộ lọc:

| Bộ lọc | Baseline / fixture dương của mutant | `k4_base` của mutant | Disposition M5g |
|---|---|---|---|
| HEAD: `re.match(r"\s*K4\b", x)` | pass / pass | `TinHieuChotCa: k4_base: ly do K4 sai nghia: ['\tK4:S fresh', 'K4: S stale, chay lai']` | `witness_killed`, `giet` |
| Lượt 7: `re.match(r"K4\b", x)` | pass / pass | pass | `unresolved`, `song` |
| Lượt 6: `x.startswith("K4: ")` | pass / pass | pass | `unresolved`, `song` |

Cả hai bản sao phục hồi bộ lọc cũ còn chạy **toàn suite**, mỗi bản **rc 1** với đúng phần M5g sống:

```text
HONG M5g k4_mau_thuan: song
nghia vu: witness_killed 161 · equivalent_verified 9 · unresolved 1
doc_receipt_thu_hoi tests: 156/156 ca QUA · 161/162 dot bien GIET
```

Phân biệt rõ: **M5g sống** làm **suite kiểm đột biến đỏ**. Không gọi đó là mutant đã chết. Trên HEAD, sáu cấu hình suite đều `162/162`, `unresolved 0`; lỗi mục tiêu M5g được đo riêng ở bảng trên, không suy từ tổng.

`patch_mechanisms.py k4` còn xác nhận ba ca không được cấp tín dụng giết: payload vô hại → `unresolved/song`; payload làm fixture dương đỏ → `unresolved/tin dung gia/qua tay`; `ValueError` vô can → `unresolved/nem sai dang: None`. M5g không chết nhờ setup/import/ngoại lệ sai.

Bằng chứng: [m5g-discrimination.stdout](m5g-discrimination.stdout), [suite bộ lọc lượt 7](m5g_r7_filter.log), [suite bộ lọc lượt 6](m5g_r6_filter.log), [driver lượt 7](k4-mechanisms.stdout).

## Runtime

Chỉ chạy lại ba driver được giao, **giữ nguyên bytes**, trên module HEAD thật, mỗi driver bằng cả bốn Python:

```text
python3.<v> -B "$OUT/runtime_isolated.py" "$ROOT"
python3.<v> -B "$OUT/runtime_depth.py" "$ROOT"
python3.<v> -B "$OUT/focused_controls.py" "$ROOT" receipt
```

**12/12 lệnh rc 0.** Mỗi Python có **592 ca API**, `errors=[]`; **16 mẫu API+CLI**; **6 độ sâu nhóm C: 900/990/1000/1200/2000/5000**. Không ngoại lệ API, timeout hoặc crash. JSON CLI bằng kết quả API; rc là **0 khi ok**, **12 khi bác**. Các ca độ sâu đều bị bác rc 12, không ngoại lệ thoát ngoài. Khác biệt parser giữa phiên bản được giữ trong logs, không ép mọi bản phải bác ở cùng luật.

Receipt thật bằng fixture, API `ok:true`, đủ năm luật `qua`, `ly_do:[]`; CLI **rc 0**, JSON bằng API cả bốn Python. Rc **2** cho tham số sai/tệp không tồn tại được suite đo; không nói ba driver runtime này tự phủ rc 2.

Các runtime khởi động ở `int_max_str_digits=4300`, [version-3.10.stdout](version-3.10.stdout) đến [version-3.13.stdout](version-3.13.stdout). Suite env 0/`-X 640` là kiểm harness ghim cấu hình, không phải bằng chứng production runtime trên hai cấu hình đó.

[Runtime summary](runtime-summary.json) được [verify_results.py](verify_results.py) đối chiếu JSON, rc và stderr; không chỉ đếm dòng hay tin rc driver. Logs đầy đủ mang tên `runtime_isolated-*.stdout`, `runtime_depth-*.stdout`, `focused_controls-*.stdout`.

## Nợ ngoài phạm vi

**Không phát sinh nợ ngoài phạm vi mới (`no-ngoai-danh-muc`).** Không săn các chiều khác, không tạo P3 từ giả thuyết chưa đo. Không soạn hoặc chạy nội dung dựng đường dẫn thoát cây. Các giới hạn authority/CI/OS dưới đây là giới hạn evidence, không phải finding sản phẩm mới.

## Đã chạy

Cwd: ROOT như trên. [run_logged.py](run_logged.py) ghi exact argv/rc/thời gian/stdout/stderr vào `*.json`, `*.stdout`, `*.stderr`; nó luôn bổ sung:

```text
PYTHONDONTWRITEBYTECODE=1
GIT_CONFIG_COUNT=1
GIT_CONFIG_KEY_0=commit.gpgsign
GIT_CONFIG_VALUE_0=false
```

Driver logger trả 0 sau khi lưu log; **rc con trong JSON** và rc lệnh lồng trong stdout mới là kết quả kiểm. [commands.json](commands.json) liệt kê **38** lệnh kiểm/driver đã hoàn tất trước bước tổng hợp; cả 38 rc 0, không timeout. Bước tổng hợp riêng [verification.json](verification.json) cũng rc 0, marker `ALL_REQUESTED_RESULTS_VERIFIED`. Rc âm mong đợi của mutant/bare lint được giữ riêng, không làm tròn thành pass.

| Lệnh/phạm vi đã chạy | Rc thật và bằng chứng | Trạng thái |
|---|---|---|
| `git rev-parse HEAD 'HEAD^{tree}' origin/master`; parent/count commit; băm spec/receipt | 0; khớp băm, đúng một commit vá; `facts.json` | passed |
| `git diff 55619d8..cb9ecc8 -- .claude/dev`; `git diff --name-only 55619d8..cb9ecc8` | 0; sản phẩm chỉ đổi test; ngoài sản phẩm là hiện vật review lượt 7 | measured |
| `python3.10 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; **156/156 ca · 162/162 mutant · equivalent 9 · unresolved 0** | passed |
| Cùng suite bằng `python3.11`, `python3.12`, `python3.13` | Mỗi lệnh 0; cùng số dương trên | passed |
| `env PYTHONINTMAXSTRDIGITS=0 python3.12 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; cùng số dương trên | passed |
| `python3.12 -X int_max_str_digits=640 -B .claude/dev/doc_receipt_thu_hoi_test.py` | 0; cùng số dương trên | passed |
| `patch_mechanisms.py ROOT k4` qua Python 3.12 | Driver 0; hai suite mutant rc 1 tại oracle K4; M5g đích chết đúng; đối chứng tín dụng không được tính nhầm | passed phản chứng F41 |
| `executor_thut_dau.py ROOT` qua Python 3.12 | 0; **18/18** kết quả hợp lệ pass | passed |
| `whitespace_k4.py ROOT` × Python 3.10–3.13 | Mỗi lệnh 0; 1.114.112 mã/runtime, 29/29 khoảng trắng, 0 lệch; 24.444 lời gọi oracle/runtime, 0 sai | passed |
| `m5g_discrimination.py ROOT` qua Python 3.12 | Driver 0; M5g chết trên HEAD, sống với cả hai bộ lọc cũ; suite bộ lọc cũ mỗi bản rc 1 với 161/162 | passed phản chứng |
| Ba driver runtime × bốn Python | **12/12 rc 0**; số dương và parity JSON ở mục Runtime | passed trong tập thử |
| `python3 -B .claude/dev/ci_dang_ky_test.py` với env tắt signer trên | 0; **22/22 đăng ký**, **4/4 launcher contract**, **3/3 Ruff contract**, **938/938 phản chứng đỏ đúng**, `TỔNG: ĐẠT` | passed |
| `python3 -m ruff check --no-cache --select F` ba tệp sản phẩm | 0; `All checks passed!`; Ruff **0.16.9** | passed bare lint sản phẩm |
| `python3 -B "$OUT/ruff_delta.py"` | Driver 0; `scripts/tl.py` HEAD/base đều lint **rc 1**, cùng **12 F821** nguyên diagnostic, **delta 0**; registry 0/0; hai tệp mới HEAD 0 lỗi | **failed bare lint tl.py; passed tiêu chí delta** |
| `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0; **10 tệp**, **0** chỗ chép doctrine | passed |
| `python3 -B .claude/dev/packet_loop.py adr-song --root .` | 0; **50 ADR / 50 dòng**, khớp 1–1; ngoại lệ trạng thái `0016` được output khai | passed |
| `git diff --numstat origin/master..HEAD` | 0; toàn diff **60 đường, +5415/−0**; sản phẩm đúng ba đường **+1 +114 +535 = +650/−0**, đúng trần | measured; passed trần sản phẩm |
| `git diff --check origin/master..HEAD` | 0; không diagnostic | passed |
| `python3 -B "$OUT/verify_results.py"` | 0; đối chiếu suite/runtime/oracle/log rc, `ALL_REQUESTED_RESULTS_VERIFIED` | passed |
| `python3 -B "$OUT/snapshot.py" before`, `... after`; so hai JSON bằng Python | Mỗi lệnh 0; **2344/2344 tệp bằng size/hash**, các kết quả Git bằng nhau; [snapshot-comparison.json](snapshot-comparison.json) | passed |

`ruff_delta.py` dùng bytes từ `git show origin/master:<path>` / `HEAD:<path>` và `ruff check --no-cache --select F --output-format json --stdin-filename <path> -` trong cùng cwd/config. Hai `git show` cho tệp sản phẩm mới ở base trả **128 — absent_at_base**, không phải lint pass. Ruff pin/probe **contract** trong registry là phép riêng với bare lint; không dùng `3/3 contract` để khai bản Ruff local là đúng pin CI.

**not_run:** mạng/GitHub; đọc lại live PR/comment/lease/generation/CI provenance; CI remote/full CI/Windows; registry toàn bộ `--chay`; legacy full selftest/release gate; audit lại toàn bảng A0 hoặc các lớp trước F41; `patch_mechanisms.py ghim`, `f41_controls.py` (script hướng vá lịch sử, có neo oracle trước F41; phép đo F41 đã chạy bằng `patch_mechanisms.py k4`); các entrypoint khác của script đầu vào ngoài danh sách trên; runtime thêm ngoài ba driver được giao; production runtime env 0/`-X 640`; merge/land/deploy/LIVE. CI “đã xanh toàn bộ trên cb9ecc8” giữ là dữ kiện chủ kho cung cấp, không khai đã kiểm lại từ sandbox.

**skipped:** không dùng kết quả skipped nào làm pass. **failed:** bare lint `tl.py` rc 1 là nợ nền cùng diagnostic/delta 0 như bảng; các suite trên bản sao sai cố ý rc 1 là bằng chứng âm mong đợi, không phải thất bại suite HEAD. Các phần không đo độc lập không được ghi passed.

## Lịch sử lớp và giới hạn evidence

| Slug | Nguồn và diễn biến | Kết luận lượt 8 |
|---|---|---|
| `oracle-k4-bo-sot-ly-do` | F40 → F41; lượt 7 trên `55619d8e…`: 1 P3 mở. Lượt 8 trên `cb9ecc86…`: phản chứng space/tab bị bắt, normalization Unicode nhất quán, đối chứng dương/nhãn khác qua, M5g đủ răng | **da_va_that** trong scope; **0 lớp / 0 biểu hiện mở** |

Chuyển tiếp này: U = 1 lớp, F = 1 lớp, tỷ lệ xác minh đóng **1/1**; không reset lịch sử hoặc tự cấp lượt review tiếp. Không tuyên bố đã audit lại mọi lớp lịch sử.

Snapshot phủ checkout được giao, gồm tracked/untracked/ignored ngoài `.git`; `.codex/` ignored có sẵn, bytes không đổi. Không phủ repo nguồn Executor. Snapshot bằng nhau chỉ chứng minh không có delta quan sát ở hai mốc, không chứng minh mọi lịch sử thao tác. Registry test tự tạo lịch sử Git trong repo tạm theo lệnh test được giao; không commit/push checkout.

Provider/surface/transport theo assignment và skill [cross-review](/tmp/claude-0/-home-user-tra-luat/0682048d-075d-5414-b3ff-642b89411167/scratchpad/rv8/.agents/skills/cross-review/SKILL.md). System nhận dạng họ GPT-6; không có header launcher của chính run để đo độc lập exact model/effort/session ID, không lấy identity từ actor GitHub hoặc từ header lượt 7. Giữ **advisory_review** như được giao. Báo cáo và manifest là hiện vật local, chưa đăng PR.

Manifest băm báo cáo, script, log và bản sao mutant: [ARTIFACTS.sha256](ARTIFACTS.sha256).
