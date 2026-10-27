Verdict: approve
Reviewed commit: 7c789142ce2a2599fd034a57faa5a6661001ec5f
Spec sha256: adaf8d2469ac16c46314c3c9ac7667cce90825a053a7b98e12b803c6719040c3; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

Đã hoàn tất review độc lập, offline, **lượt 2 — xác minh merge**, packet #977 / revision 1 / generation 1. Không còn finding P0/P1/P2/P3 trong phạm vi này. Các mục (a), (b), (c) đạt.

Lý do lượt 2: sau approval lượt 1, master tiến; executor tạo hai merge commit `f8d75656f3c997eee9d4ab971d6fa5400ba712e1` rồi head hiện tại. Lượt này xác minh tính toàn vẹn của phần đã duyệt và tác động ngữ nghĩa của master mới, không mở lại review từ đầu. Nguồn lịch sử là `tham-chieu/wp977-g1-codex-luot1-VERDICT.md`, approve `e05ea6a11eb689e1cebb11b417a56930cec8f11e`, không có lớp finding mở để tái kiểm đóng.

Reviewer: Codex, model family `openai`, provider `openai_codex`, execution surface `codex_cli`, transport `machine`; run `48d54b73780c49b58f16b8ffc25f9c0d`. Ba trường provider/surface/transport được đối chiếu `runs/48d54b73/run.json`. Tệp run được đọc không có bằng chứng model ID/effort thực phục vụ; không tự điền telemetry ấy. Sandbox phiên là `workspace-write` theo cấu hình runtime; read-only với `src/` là phạm vi đã tuân thủ và được kiểm bằng snapshot, không khai là cơ chế cấm ghi của hệ điều hành. Executor trong lease là Claude, họ `claude`; review class `sensitive`, assurance target `cross_approved`. Hai trục: Spec và Standards/Security. Không kế thừa context executor.

Đã đọc toàn bộ `runs/48d54b73/prompt.snapshot`. Spec bản chép và phần chung khớp hai băm ở dòng 3; lease khớp packet/revision/generation/spec và phân vai. Lease dành thêm đường dẫn handoff trên nhánh lease; diff packet thực tế chỉ có tệp protocol. Các ref được đo là **snapshot Git cục bộ**, không phải readback remote live. Không gọi mạng/GitHub, không push/merge/land, không sửa packet. Mọi kiểm tra thực thi chạy trên `out/review-copy/` hoặc fixture riêng dưới `out/`; mọi tệp mới đều dưới `out/`.

**Bảng lớp finding**

| slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá |
|---|---|---|---|---|
| — (không có lớp finding mở) | — | — | (a), (b), (c) và 43/43 ca hồi quy đạt | Không yêu cầu vá |

Đếm theo nguyên nhân: **P0=0, P1=0, P2=0, P3=0; 0 biểu hiện lỗi**. Luật phân hạng của chủ kho được áp như sau: không phát hiện mệnh đề sai so với mã, luật mới chưa cưỡng chế, mâu thuẫn protocol hay thiếu mục bắt buộc, nên không có căn cứ P2+. Lượt 1 không có phản chứng/finding mở còn sống. Lượt này không tự dựng đột biến độ phủ mới; các đầu vào âm trong ca có sẵn bị từ chối đúng không phải finding P3. Nếu chỉ có đột biến độ phủ mới trong khi A/B vẫn xử lý đúng thì phải là P3 có tên nợ/owner/hướng xử lý, không nâng thành P2.

**(a) Toàn vẹn merge và write set — ĐẠT**

Trong bảng lệnh: `H=7c789142ce2a2599fd034a57faa5a6661001ec5f`, `B=44884446f71c89e25f9a72ac58e4f597db63c1ba`, `O=09db70350414d767b793a71cb630e643f216a1b1`, `A=e05ea6a11eb689e1cebb11b417a56930cec8f11e`, `P=docs/PROTOCOL_DA_PHIEN.md`. Đối số đầy đủ, cwd, stdout/stderr và rc từng lệnh nằm trong `acceptance.jsonl` và `acceptance.log`.

| Lệnh / phép đo | rc | Bằng chứng dương |
|---|---|---|
| `git -C src rev-parse HEAD HEAD^{tree} refs/remotes/origin/master` | 0 | Head = H; tree = `618822dd1c643b6fc5b97c8cf4335f684d940c18`; ref master = B; kiểm lại cuối lượt vẫn khớp. |
| `git -C src symbolic-ref -q HEAD`; `git -C src rev-parse --is-shallow-repository` | 1 mong đợi / 0 | Detached HEAD; `false` cho shallow; `.git` là thư mục. |
| `git -C src status --porcelain=v1 --untracked-files=all --ignored` | 0 | stdout rỗng cả đầu và cuối lượt. |
| `sha256sum tham-chieu/wp977.md src/ops/specs/may-adr-0054-chung.md` | 0 | Hai băm đúng dòng 3; đã kiểm lại cuối lượt. |
| `git -C src merge-base --is-ancestor "$B" "$H"`; tương tự A→H | 0 / 0 | Base mới và head đã approve đều là tổ tiên của H. |
| `git -C src log -2 --first-parent --format='%H %P' "$H"` | 0 | H có parents `f8d7565…` và B; `f8d7565…` có parents A và `7f19424478616b2c5d0a0c7f26839e1d1c41261b`. |
| `git -C src rev-parse "$H:$P"`; tương tự A | 0 / 0 | Cùng blob OID **`a8f689d11b2eab370de68d6dc197a97f72420e94`**. |
| `git -C src diff --exit-code "$A" "$H" -- "$P"` | 0 | Không có diff; protocol giống từng byte với bản được duyệt lượt 1. |
| `git -C src diff --numstat "$B" "$H"` | 0 | **`19  2  docs/PROTOCOL_DA_PHIEN.md`**; đúng 1 tệp, 19 ≤ 40. |
| `git -C src diff "$B" "$H"`; `git -C src diff --check "$B" "$H"` | 0 / 0 | `candidate.diff`: đúng hai hunk §4 và §12, không lỗi whitespace. |

Đoạn mới vẫn là một đoạn văn xuôi ngay sau `approved_pending`, đủ M1. Câu mission ở §12 bổ sung đúng hai state, đủ M2. Không có thay đổi code hoặc các mục protocol khác.

**(b) Tác động của master mới — không làm sai §4/§12**

`git -C src diff "$O" "$B"` rc=0, lưu **toàn bộ** ở `master.diff`; `--name-status` và `--numstat` rc=0, lưu `master-paths.txt`, `master-numstat.txt`. Tổng cộng **112 đường dẫn**: 97 trong `ops/reviews/` (hiện vật/lịch sử review và README), 3 spec, 12 tệp còn lại. Phân loại đầy đủ ở `master-inventory.json`. Đã đối chiếu các thay đổi mã/spec có thể tác động đến mô tả packet; đây không phải approval lại các packet đã vào master.

| Phần thay đổi / neo mã trên H | Đối chiếu và kết luận |
|---|---|
| `.claude/dev/packet_loop.py` | `git diff --exit-code O B -- .claude/dev/packet_loop.py` rc=0: không đổi. `packet_loop_test.py`, `ops/lease_publish.py`, `.claude/dev/launcher.py`, `AGENTS.md` cũng không đổi, mỗi phép rc=0. |
| `docs/PROTOCOL_DA_PHIEN.md` | `git diff --exit-code O B -- docs/PROTOCOL_DA_PHIEN.md` rc=0: master không chạm protocol. Không có hunk mới làm mâu thuẫn §4 hoặc câu mission §12:1158. |
| `ops/bien_nhan_v2.py:962`, `:1212`, `:1335` | Master bổ sung L-REVIEW/L-ANCESTRY/L-SURFACE và kiểm nợ câu lịch sử vào đường quét toàn bộ `kiem`/CLI. Trong các hàm/lớp có sẵn, chỉ `kiem` và `main` đổi; không xóa hàm cũ. |
| API biên nhận dùng tại `.claude/dev/packet_loop.py:2437`, `:2682` | Packet loop nạp validator canon, gọi `_thieu`, `_neo_git` và các hàm chuẩn hóa/giải họ model; **không gọi `kiem` hoặc `main`**. AST cả phần mã trước khối câu lịch sử giữ nguyên, gồm các hàm ấy và các hằng/khởi tạo liên quan. `_thieu` ở `ops/bien_nhan_v2.py:695`, `_neo_git` ở `:824` không đổi. Không suy rằng toàn bộ validator không đổi: chỉ hợp đồng được luồng packet sử dụng được giữ nguyên. |
| Bảng lớp/slug, `.claude/dev/packet_loop.py:2727`, `:2748`, `:2966` | Kiểm slug duy nhất/miền hạng, tập finding IDs bằng bảng lớp, refs không rỗng/đúng dạng/không lặp vẫn ở packet loop. `check_refs` dùng cặp workflow/job; `connector_refs` phủ đúng tập P0–P2. Master không đổi các chốt đó. 43 ca `r813_*` chạy với validator và protocol mới xác nhận cả đường dương lẫn các đầu vào âm. |
| `.claude/dev/ci_dang_ky_test.py:759`, `:809` | Chỉ bổ sung/sửa chú thích lịch sử timeout job. So AST toàn tệp O/B bằng nhau; không đổi định nghĩa gate, check hoặc timeout thực thi. |
| `scripts/tl.py:104`, `:1600`, `:1771`; `scripts/tl_core/profile_env.py:637`, `ops_misc.py:440`, `:631`, `profile_mgmt.py:478` | #972 đổi nơi backup config, chặn backup vào cây skill, xử lý ngoại lệ và ghi backup qua tệp tạm/replace; re-export helper/lớp ngoại lệ trong `tl.py`. Test `r972_*`, VERSION/SKILL/CHANGELOG/manifest đi cùng thay đổi ấy. Không thêm state packet, cửa tiêu thụ `checkpoint_day` hoặc thay hợp đồng biên nhận mô tả ở §4. |
| `ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md`; hai spec land r2 mới của #988 | Đây là đặc tả công việc tiếp theo về câu lịch sử và hồ sơ assurance land; không phải thay đổi đang thi hành của state machine. Không kích hoạt ADR-0054 và không sửa quy tắc mission complete. |
| `ops/reviews/` và `ops/bien_nhan_v2_test.py` | Bổ sung evidence/caveat các lượt #960 cùng test cho ba luật câu lịch sử. Không được dùng các finding lịch sử #960 làm finding kế thừa của #977; không có thay đổi vào API bảng lớp/slug/refs dùng tại cửa mở lại. |

Phép so độc lập: `PYTHONDONTWRITEBYTECODE=1 python out/check_merge_semantics.py` **rc=0**. `merge-semantics.json` ghi 23 hàm/lớp cũ giữ nguyên AST, 2 hàm đổi (`kiem`, `main`), 16 hàm/lớp mới, 0 hàm bị xóa; bảy hàm API biên nhận được packet loop gọi đều thuộc nhóm giữ nguyên. So AST `ci_dang_ky_test.py` và phần mã validator trước khối câu lịch sử đều đạt.

Vì `cmd_mo_lai`, `cmd_chu_kho_duyet`, `_xet_dung` và các chốt biên nhận mà chúng dùng giữ nguyên, các mệnh đề đã duyệt ở lượt 1 vẫn đúng trên H: hai nguyên nhân mở lại; connector từ quyền `ci-do` chưa có `begin_attempt`; checkpoint `cho_phep_va`; quyền `cho_phep_day` riêng chưa có cửa tiêu thụ; xét dừng và trạng thái chưa hoàn tất. §12 là nghĩa vụ mission, không tuyên bố tồn tại một lệnh máy mới để complete mission.

**(c) Nghiệm thu trên head mới — ĐẠT**

Bản sao `out/review-copy/` là clone thường, ghim H/tree nói trên và ref `origin/master` = B. Môi trường: Linux, Python **3.13.17**, Git **2.43.0**, ripgrep **15.2.0**, PyYAML **6.0.3**. Dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; `TMPDIR`/`TEMP`/`TMP` nằm dưới `out/tmp/`, `core.abbrev=7` chỉ cấu hình trong bản sao. Fixture dùng remote file cục bộ.

| Lệnh / phép đo | rc | Bằng chứng dương / kết quả |
|---|---|---|
| `rg -n 'cho_chu_kho' docs/PROTOCOL_DA_PHIEN.md` tại copy | 0 | Khớp dòng **253, 256, 1158**; có §4. |
| `rg -n 'approved_pending.*cho_chu_kho\|cho_chu_kho.*approved_pending' docs/PROTOCOL_DA_PHIEN.md` tại copy (dấu `\|` chỉ để hiển thị trong bảng Markdown; đối số thực là `|`) | 0 | Khớp đúng câu §12, dòng **1158**. |
| `rg -n 'chu-kho-duyet' docs/PROTOCOL_DA_PHIEN.md` tại copy | 0 | Khớp dòng **256, 259, 261**. |
| `git show "$O:$P"`, rồi đưa bytes vào từng `rg -n` với ba biểu thức trên | 0 cho show; **1/1/1** cho rg, đúng kỳ vọng | Cả ba stdout rỗng; bytes lưu `old-base-protocol.md`. |
| `git show "$B:$P"`, rồi đưa bytes vào từng `rg -n` với ba biểu thức trên | 0 cho show; **1/1/1** cho rg, đúng kỳ vọng | Cả ba stdout rỗng; bytes lưu `new-base-protocol.md`. Các rc được ghi riêng, không bị pipeline che lỗi. |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` tại copy | **0** | `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. |
| `python .claude/dev/packet_loop.py adr-song --root .` tại copy | **0** | `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1`; scanner nêu ngoại lệ trạng thái sẵn có `0016`. |
| `PYTHONDONTWRITEBYTECODE=1 python out/run_selected.py` | **0** | **43/43 ca `r813_*` đạt, skipped=0**; `selected-tests.log`, `selected-results.json`, `selected-receipt.json`. |
| `git diff --exit-code f8d7565 "$H" -- .claude docs` | 0 | Hai cây `.claude/`, `docs/` giống nhau giữa lần merge đầu và H, như hồ sơ giao việc khai. |
| `PYTHONDONTWRITEBYTECODE=1 python out/audit.py finish` | **0** | **7.486 mục tệp trước/sau, 0 delta**, gồm nội dung `.git`; HEAD/tree/ref và hai băm spec giữ nguyên. `source-integrity.json`, `src-before.json`, `src-after.json`. |

43 ca được gọi từ chính harness của bản sao H. Fixture `_kho812` tại `packet_loop_test.py:7677` đọc protocol thật, chép validator thật vào kho Git riêng; các bước mở lại/checkpoint dùng CLI thật và remote file. Có các ca cho slug ngoài biên nhận, refs lặp/tập con/hạng P3, CI không đỏ/check sai app/run mới, connector sau CI và sau lượt mới, checkpoint sai packet/generation/spec/head/người quyết/phạm vi, quyền đẩy dùng lại và chạm trần. Ca âm kiểm rc/lý do và state nguyên byte theo harness. Đây là tập chọn lọc, không phải full suite hoặc mutation matrix.

**Giới hạn đo:** full `python .claude/dev/packet_loop_test.py` và mutation matrix **not_run bởi reviewer**, theo ngoại lệ rõ trong prompt lượt 2. Con số executor 981/981 trên `f8d7565` và việc chạy lại trên H là thông tin giao việc, chưa được reviewer tái xác minh bằng log full suite. Không tuyên bố full suite/CI trên H đã xanh hoặc đủ điều kiện merge. Snapshot chỉ chứng minh không có delta quan sát được tại hai mốc, không chứng minh toàn bộ lịch sử thao tác. Không có phép kiểm bắt buộc (a)/(b)/(c) nào bị bỏ qua.

Verdict chỉ neo commit **`7c789142ce2a2599fd034a57faa5a6661001ec5f`**, không cấp quyền push, merge hay land; packet này không kích hoạt ADR-0054.
