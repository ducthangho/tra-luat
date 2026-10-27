Verdict: approve
Reviewed commit: bd5a66ab01823d6775e1673e64c7da42f7e80135
Spec sha256: adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Đã hoàn tất review độc lập, offline, **lượt 3 — xác minh merge**, packet #977 / revision 1 / generation 1. Các mục (a), (b), (c) đạt; không còn finding P0/P1/P2/P3 trong phạm vi được giao.

Lý do lượt 3: sau approval lượt 2 trên `7c78914`, master tiến từ `4488444` lên `c2d84ea` và chạm adapter được doctrine-scan đọc. Lượt này xác minh riêng tác động của đoạn merge ấy và giữ nguyên phần protocol đã duyệt; không mở lại review packet từ đầu. Đã đọc toàn bộ `runs/06393623/prompt.snapshot`, tự kiểm định danh Git, hai băm đặc tả và bản chép lease. Các ref là snapshot Git cục bộ, không phải readback remote live.

Reviewer: Codex, họ model `openai`; provider `openai_codex`, execution surface `codex_cli`, transport `machine`, run `06393623e441468c9346700f2f6f2b9c`. Ba trường provider/surface/transport khớp `runs/06393623/run.json`; snapshot chọn trường ở `runtime-observation.json`. Run đang chạy khi đọc, chưa có trường runtime model/effort/sandbox terminal: **không tự khai model ID/effort đã được máy đo**, không dùng header hay cấu hình để thay telemetry. Sandbox phiên được cấu hình `workspace-write`; read-only với `src/` là ranh giới công việc đã tuân thủ, không phải tuyên bố hệ điều hành cấm mọi ghi. Executor theo assignment/lease là Claude, họ `claude`; review class `sensitive`, assurance target `cross_approved`. Verdict nội dung này không tự hoàn tất receipt thực thi/assurance sau run.

Hai trục review: Spec và Standards/Security. Không kế thừa context executor, không truy cập mạng/GitHub, không push/merge/land. Mọi tệp reviewer tạo nằm dưới `out/`; các phép thử thực thi dùng `out/review-copy/` và fixture riêng dưới `out/`. Lease khớp packet/revision/generation/spec và phân vai; đường dẫn handoff được lease dành riêng không xuất hiện trong diff ứng viên.

**Bảng lớp finding**

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| — (không có lớp finding mở) | — | — | (a), (b), (c) và 177/177 ca chọn lọc đạt | Không yêu cầu vá |

Đếm theo nguyên nhân: **P0=0, P1=0, P2=0, P3=0; 0 biểu hiện lỗi**. Áp luật phân hạng của chủ kho: không thấy hành vi/mệnh đề sai, luật mới chưa được mã cưỡng chế, mâu thuẫn protocol hay thiếu mục bắt buộc để xếp P2+. Không tự dựng đột biến độ phủ mới trong lượt này; đầu vào âm của các ca có sẵn bị từ chối đúng là bằng chứng đạt, không là nợ P3. Nếu một đột biến độ phủ mới vẫn được mã/văn bản xử lý đúng ở A/B thì chỉ là P3 có tên/owner/hướng xử lý, không nâng thành P2.

**ĐỐI CHIẾU LƯỢT TRƯỚC**

`tham-chieu/wp977-g1-codex-luot2-VERDICT.md` approve `7c789142ce2a2599fd034a57faa5a6661001ec5f`, P0–P3 đều 0; lượt 1 approve `e05ea6a11eb689e1cebb11b417a56930cec8f11e`, cũng không có lớp mở. Vì không có finding trước, không có lớp cần gán ĐÃ VÁ THẬT/VÁ HỜ/VÁ SINH LỖI MỚI/CHƯA VÁ; tỷ lệ đóng lớp là N/A. Tính nguyên vẹn của phần đã duyệt được đo lại bằng blob OID và diff, không suy từ lời khai executor.

**(a) Toàn vẹn merge và write set — ĐẠT**

Ký hiệu trong các lệnh dưới đây:

```text
H=bd5a66ab01823d6775e1673e64c7da42f7e80135
B=c2d84ea7c20e835968b630a4fb1b8daa29ac12c7
M=44884446f71c89e25f9a72ac58e4f597db63c1ba
A=e05ea6a11eb689e1cebb11b417a56930cec8f11e
C=7c789142ce2a2599fd034a57faa5a6661001ec5f
O=09db70350414d767b793a71cb630e643f216a1b1
P=docs/PROTOCOL_DA_PHIEN.md
```

`acceptance.jsonl` và `acceptance.log` giữ argv đầy đủ, cwd, rc, stdout/stderr của từng lệnh. Các lệnh Git ở (a)/(b) có cwd `src/`; nghiệm thu và test ở (c) chạy trên copy.

| Lệnh / phép đo | rc | Bằng chứng dương |
|---|---|---|
| `git rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | HEAD=H, tree=`36ec684c2040432b01f5196a8015236592ddd789`, ref master=B; đầu/cuối khớp. |
| `git symbolic-ref -q HEAD`; `git rev-parse --is-shallow-repository` | 1 mong đợi / 0 | Detached HEAD; shallow=`false`; `.git` là thư mục thật. |
| `git status --porcelain=v1 --untracked-files=all --ignored` | 0 | stdout rỗng đầu/cuối. |
| `sha256sum tham-chieu/wp977.md src/ops/specs/may-adr-0054-chung.md` (đường dẫn tuyệt đối trong log) | 0 | Hai băm đúng dòng 3, kiểm lại cuối lượt. |
| `git merge-base --is-ancestor B H`; tương tự A→H, C→H | 0 / 0 / 0 | Base mới và cả hai head đã approve đều là tổ tiên H. |
| `git show -s --format='%H %P' H` | 0 | H có đúng hai parents C và B. |
| `git rev-parse H:P A:P C:P` | 0 | Cả ba cùng blob **`a8f689d11b2eab370de68d6dc197a97f72420e94`**. |
| `git diff --exit-code A H -- P`; tương tự C→H | 0 / 0 | Không diff; protocol giống từng byte với cả hai bản đã duyệt. |
| `git diff --numstat B H` | 0 | **`19  2  docs/PROTOCOL_DA_PHIEN.md`**, đúng 1 tệp, 19 ≤ 40. |
| `git diff B H`; `git diff --check B H` | 0 / 0 | `candidate.diff`: chỉ thêm đoạn văn xuôi §4 sau `approved_pending`, sửa câu §12; không lỗi whitespace. |

Đủ M1/M2 của đặc tả. Không sửa code hoặc mục protocol khác trong diff packet.

**(b) Tác động của `4488444..c2d84ea` — không làm sai §4/§12**

Đã đọc toàn bộ `git diff M B` (rc=0), lưu `master.diff`; `--name-status` và `--numstat` đều rc=0, lưu `master-paths.txt` và `master-numstat.txt`. Có **8 đường dẫn, 74 dòng thêm/18 dòng xóa**. Các neo dòng sau thuộc reviewed head H.

| Phần thay đổi | Đánh giá tác động đến packet #977 |
|---|---|
| `.claude/skills/cross-review/SKILL.md:139`; `.agents/skills/cross-review/SKILL.md:65` | Đổi nguồn đọc model/effort/sandbox từ header stderr sang các trường `run.json`, chỉ nhận đo được khi trạng thái `DO_DUOC`; header còn là lời khai phụ, cờ CLI là cấu hình yêu cầu. Đây là chỉ dẫn đo evidence của lượt, không thêm state/cửa/authority, không thay điều kiện `mo-lai`, `chu-kho-duyet`, quyền đẩy hoặc mission complete. |
| `.claude/dev/launcher.py:1825`, `:2129`, `:2287` | Đối chiếu trực tiếp `_BoLocStderr.ghi_so`, `_LayMauSandbox.ghi_so` và nhánh đặt `RUST_LOG`: tên trường và cách kết luận trong adapter có sẵn trong mã. Launcher không đổi trong merge này. §8.1:790 vẫn phân biệt cấu hình với runtime evidence và giới hạn của header; adapter không mâu thuẫn yêu cầu ấy. Không tái đo lời thuật lịch sử về CLI bên ngoài. |
| `.claude/dev/packet_loop.py:1625` | Scanner đọc **cả** `.claude/skills/**/*.md` và `.agents/skills/**/*.md`, cộng CLAUDE.md. Vì vậy đã chạy lại trên H, không suy pass từ lượt cũ: quét 10 tệp, 0 chỗ chép doctrine. Các ca scanner kiểm cả chiều chặn và không bắt oan. |
| `.claude/dev/packet_loop.py:2949`, `:2997`, `:3042` | `cmd_mo_lai`, `cmd_chu_kho_duyet`, `_xet_dung` giữ nguyên. `git diff --exit-code M B -- <path>` rc=0 riêng cho toàn bộ `packet_loop.py`, `packet_loop_test.py`, `launcher.py`, `ops/bien_nhan_v2.py`, `ops/lease_publish.py`, protocol và AGENTS. Các API biên nhận/lease mà luồng dùng cũng không đổi. |
| `ops/land/pr945-wp899-land-evidence.yaml:273` và 3 tệp provenance đi cùng | Bổ sung hồ sơ quyết định #899, vẫn giữ `landed: false` và caveat assurance. Không phải checkpoint của #977; không sửa máy trạng thái hoặc tạo ngoại lệ cho câu mission §12. Đây là lịch sử packet khác, không nhập finding của nó vào #977. |
| `scripts/tl_selftest.py:21231`; `RELEASE_MANIFEST.json` | Fixture backup config #972 bổ sung cô lập `USERPROFILE`/`HOMEDRIVE`/`HOMEPATH`, đặt USERPROFILE vào cây tạm để `Path.home()` đúng trên Windows; manifest cập nhật byte/hash tương ứng. Không đổi runtime packet hoặc logic scanner/nghiệm thu protocol. |

Các mệnh đề mới ở protocol:248–263 vẫn neo vào mã không đổi: hai nguyên nhân mở lại; connector từ quyền `ci-do` cùng generation/SHA nguồn, chưa có `begin_attempt`; checkpoint `cho_phep_va`; quyền `cho_phep_day` riêng chưa có cửa tiêu thụ; bộ đếm và xét dừng. Câu §12:1158 giữ nghĩa vụ không complete khi còn packet chưa xong, không tuyên bố thêm lệnh máy complete mission. 43 ca `r813_*` trên H xác nhận lại đường dương và đầu vào âm của các cửa này.

**(c) Nghiệm thu trên head mới — ĐẠT**

Bản sao vật lý đầy đủ `out/review-copy/` ghim H/tree/ref như (a), không dùng hardlink. Môi trường: Linux, Python **3.13.17**, Git **2.43.0**, ripgrep **15.2.0**. Dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; `TMPDIR`/`TMP`/`TEMP` dưới `out/tmp/`. Chỉ cấu hình `core.abbrev=7` trong copy; harness tự cô lập cấu hình Git khi tạo fixture. Các fetch/ls-remote của ca checkpoint dùng remote file cục bộ.

Ba biểu thức được truyền nguyên văn cho `rg -n`:

```text
cho_chu_kho
approved_pending.*cho_chu_kho|cho_chu_kho.*approved_pending
chu-kho-duyet
```

| Lệnh / phép đo | rc | Bằng chứng dương / kết quả |
|---|---|---|
| `rg -n <biểu thức 1> docs/PROTOCOL_DA_PHIEN.md` trên copy | 0 | Dòng **253, 256, 1158**; hai dòng thuộc §4. |
| `rg -n <biểu thức 2> docs/PROTOCOL_DA_PHIEN.md` trên copy | 0 | Khớp đúng câu §12, dòng **1158**. |
| `rg -n <biểu thức 3> docs/PROTOCOL_DA_PHIEN.md` trên copy | 0 | Dòng **256, 259, 261**. |
| `git show O:P`, rồi đưa bytes vào từng `rg -n` ở trên | 0 cho show; **1/1/1** đúng kỳ vọng | Ba stdout rỗng; bytes lưu `old-base-protocol.md`. |
| `git show B:P`, rồi đưa bytes vào từng `rg -n` ở trên | 0 cho show; **1/1/1** đúng kỳ vọng | Ba stdout rỗng; bytes lưu `new-base-protocol.md`. Mỗi rc riêng, không bị pipeline che lỗi. |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` trên copy | **0** | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| `python .claude/dev/packet_loop.py adr-song --root .` trên copy | **0** | `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1`; scanner ghi ngoại lệ trạng thái có sẵn `0016`. |
| `PYTHONDONTWRITEBYTECODE=1 python out/run_selected.py` | **0** | **177/177 đạt, failed=0, skipped=0**. `selected-tests.log`, `selected-results.json`, `selected-receipt.json`. |
| `PYTHONDONTWRITEBYTECODE=1 python out/audit.py finish` | **0** | **8.163 mục (7.522 tệp + 641 thư mục), 0 delta** so snapshot đầu, gồm `.git`. HEAD/tree/ref/spec hashes giữ nguyên; `source-integrity.json`, `src-before.json`, `src-after.json`. |

Tìm bằng `rg -n 'skills/' .claude/dev/packet_loop_test.py` dẫn tới fixture `_repo_gia`; tìm thêm `SKILL.md` và đường dẫn ghép `"skills"` để không bỏ sót ca đọc adapter thật. Tập chọn lọc dùng chính `chay_suite` của H: **17 doctrine_scan + 78 ac18 + 37 ac19 + 1 cross_review + 1 land_packets + 43 r813 = 177**. Có ca đọc adapter thật, chép doctrine/protocol thật, kiểm đầu vào hỏng, không bắt oan, và các cửa mở lại/checkpoint. `selected-scope.json`/`selected-cases.json` ghi danh sách; `selected-calls.jsonl` ghi argv/rc/stdout/stderr các lần harness gọi CLI. Không sửa mã sản phẩm để làm test đạt.

**Giới hạn đo:** full `packet_loop_test.py` và mutation matrix **not_run bởi reviewer**, theo ngoại lệ rõ trong prompt lượt 3. Con số executor 981/981 trên `7c78914` và việc chạy lại trên H là thông tin giao việc, chưa được reviewer xác minh bằng log full suite. Không nhận tập 177 ca này là full suite/CI hay bằng chứng đủ điều kiện merge. Ruff pin/probe và bare lint đều **not_run** (ngoài nghiệm thu merge văn bản được giao); không khai Ruff passed. Snapshot chỉ chứng minh không có delta nội dung/mode quan sát được tại hai mốc, không chứng minh toàn bộ lịch sử thao tác. Receipt terminal của run phải được bên vận chuyển kiểm sau khi writer kết thúc.

Verdict chỉ neo commit **`bd5a66ab01823d6775e1673e64c7da42f7e80135`**, không cấp quyền push, merge hay land; packet này không kích hoạt ADR-0054. Mọi thay đổi code, các mục protocol khác và #814/#815/#816 nằm ngoài phạm vi xếp hạng của lượt này.
