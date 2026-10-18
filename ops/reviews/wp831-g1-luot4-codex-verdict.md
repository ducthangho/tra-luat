verdict: changes_requested
reviewed_sha: c59d479be2132242125d4a8e77356ed676f76d2c

F01/F02 đã vá thật. Bản vá F03 giữ được interpreter qua vòng source, nhưng sinh **F04 P2 `inherited-marker-reuses-scalar-python`**: dấu nhập từ môi trường trùng PID cho phép dùng PY scalar lạ, trái spec r4 mục 2. Không đạt ngưỡng approve khi còn P2 mở. Không phát hiện P0/P1; không mở P3 mới.

Reviewer Codex, họ OpenAI, provider `openai_codex`, execution surface `codex_service` (API agent có shell Linux), transport `machine`. Executor Claude theo assignment. Model variant/effort và session/launcher receipt độc lập: **KHÔNG ĐO ĐƯỢC**; không suy từ tài khoản vận chuyển. Agent `tl_auditor` chỉ đọc/tiêu hoá evidence theo CLAUDE.md §Quy trình sửa code/5, không chạy test hay ghi tệp. Verdict này không tự cấp assurance, transition hay quyền land.

Đã đọc toàn bộ prompt.snapshot, bốn spec, hai verdict và các diff được giao; đối chiếu code, Spec và Standards/Security liên quan. Clone, fixture, mutation, log và output đều dưới `review-data/`. Không gọi GitHub, push, merge/land/deploy hoặc sửa `cay-kho/`. Các installer trong phép đo tập trung là stub; probe môi trường chỉ dùng Python thật, không tạo payload tấn công.

**Neo, băm và phạm vi**

| Phép đo | Kết quả tự đo |
|---|---|
| HEAD / tree | `c59d479be2132242125d4a8e77356ed676f76d2c` / `aa87a7d80705685df0ee092141b4b8a29369f061` |
| Immutable acceptance baseline | `1e69d2a0d3c708efe0dec86752fc13a0fe039aab` |
| origin/master snapshot | `577d7b95d257f6c376677e1ffb0131d12b74d24e`; không dời baseline nghiệm thu |
| SHA-256 SPEC-r1.md | `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888` |
| SHA-256 SPEC-r2.md | `3ab3aac4c68a7bbe87daf5dfee75c649ff46110697b2cd5b00b29586e4c253e7` |
| SHA-256 SPEC-r3.md | `dd8f0fab5e3592975e4cde2f180fe0d052fc66e67fae15194e71970cb02f65e6` |
| SHA-256 SPEC-r4.md | `5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad` |
| Bundle | diff.patch, numstat.txt và diff-tu-luot3.patch đều khớp BYTE Git ở đúng hai đầu mút |
| Dựng cây | Clone local --no-hardlinks --no-checkout, detached exact SHA, origin về endpoint gốc; không fetch/network; core.abbrev=7, core.autocrlf=false |
| Master drift | 3 commit, 40 đường dẫn ops/land/pr823-wp802-*, không giao 8 tệp packet; merge-tree mô phỏng trên bản sao rc0, tree `0c4d4b3ab3b0697185919fe6356a326bc391ffd2`; không thực hiện merge branch |
| Runtime | Linux x86_64, Python 3.13.16, GNU Bash 5.2.21, Ruff 0.17.1; bytecode tắt, Ruff --no-cache; TMPDIR riêng trong review-data |
| Phạm vi sửa | YAML chỉ hai leaf recipe Linux/macOS; install prefix Linux/macOS/Windows giữ nguyên; ca r802 parity nguyên; AST selftest chỉ hai constant 187→189 sau normalize |
| Shell r4 | Chỉ guard dùng lại PY, dòng gán dấu, phần ghim/chú thích được cấp; không sửa phần khác |
| Manifest commit cuối | HEAD chỉ đổi RELEASE_MANIFEST.json, sau commit changelog/handoff |

Đúng **8 đường dẫn lease r4, 293 thêm / 18 xóa**, 293≤450. Lease/receipt/CI live không đo được vì assignment cấm GitHub; không lấy lời khai executor thay evidence.

| Đường dẫn | Thêm | Xóa |
|---|---:|---:|
| `.claude/dev/launcher_test.py` | 140 | 1 |
| `RELEASE_MANIFEST.json` | 16 | 6 |
| `changelog.d/wp-831.md` | 18 | 0 |
| `docs/GOI_AGENT_DA_NEN.md` | 17 | 3 |
| `ops/cai_cong_cu.sh` | 11 | 1 |
| `ops/cong_cu.yaml` | 10 | 2 |
| `ops/handoff/wp831-g1-claude.md` | 74 | 0 |
| `scripts/tl_selftest.py` | 7 | 5 |

Bằng chứng: [preflight.json](preflight.json), [master-drift.json](master-drift.json), [static-checks.json](static-checks.json).

**Đối chiếu lượt trước — giữ ID/slug**

| ID / slug / nguồn | Phân loại lượt 4 | Phép đo độc lập |
|---|---|---|
| F01 P2 `chooser-checker-path-fallthrough`, lượt 1–3 | **ĐÃ VÁ THẬT** | Ứng viên mode 0644, front rg tốt khác: direct Linux/macOS rc0 và in đúng front; bỏ -x làm đúng r831 đỏ bằng TinHieuChotCa tại assertion hành vi |
| F02 P2 `linux-candidate-set-drops-usrbin`, lượt 1–3 | **ĐÃ VÁ THẬT** | /usr/bin/rg thật tốt; seam vắng/rỗng, dpkg stub khai tốt→hỏng hoặc đảo: HEAD vẫn chọn /usr/bin, không gọi dpkg; recipe r1 chỉ hỏng thứ tự tốt→hỏng. Bỏ candidate usrbin giết đúng r831 Linux |
| F03 P2 `chooser-path-reselects-python`, lượt 2 @75bcd43, lượt 3 @6376cd3 | **VÁ SINH LỖI MỚI → F04**; cơ chế reselect do PATH của lượt trước đã được vá | Wrapper đơn đủ 12 layout rc0. Vòng source full-YAML 24/24 hai công cụ DAT. Batch với front riêng: HEAD 24/24 tổng DAT; r3 rg→bash thiếu yaml/rc3 12/12. Nhưng guard mới tin dấu môi trường/PY scalar: F04 bên dưới |

Không đổi slug F03 để xoá lịch sử. Giữ lớp F03 và liên kết regression do bản vá sang lớp mới F04; không nhận tổng suite xanh là đóng mọi trường hợp. Hai lớp F01/F02 tiếp tục đóng, một regression P2 mới còn mở.

**Bảng săn — lệnh → kết quả thật → ý nghĩa**

Lệnh orchestration từ gốc rv4; lệnh gate chạy trong bản sao head/base. Các result.json ghi argv, cwd, rc và elapsed thật. Full selftest TUẦN TỰ: head, base, rồi mutant r291 và r357; GIT_CONFIG_GLOBAL riêng include cấu hình hiện có rồi tắt ký commit/tag và ghim core.abbrev 7, không sửa global/home.

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| `python review-data/preflight.py` | rc0; bốn spec đúng băm, ba artifact khớp byte, 8 tệp/293 dòng thêm | Đúng candidate/baseline/trần r4 |
| `python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | HEAD absent/fake auth: mỗi lượt rc0, 1/1, 0 bỏ qua/hỏng | N1/N3/N7/N8 trong ca stock đạt |
| Tương tự `r831_cai_rg_macos_chon_ban_chay_duoc` | HEAD absent/fake: mỗi lượt rc0, 1/1, 0 bỏ qua/hỏng | Recipe macOS chạy trên Bash Linux |
| Tương tự `r802_cai_rg_windows_chon_ban_chay_duoc` | Base/head × absent/fake: mỗi lượt rc0, 1/1, 0 bỏ qua/hỏng | Windows fixture POSIX không hồi quy; không chứng nhận native |
| Tương tự `r802_bang_cai_rg_khop_cong_cu_yaml` | Base/head × absent/fake: mỗi lượt rc0, 1/1, 0 bỏ qua/hỏng | Install parity giữ nguyên |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` | Base/head rc0, 56/56, bỏ qua 0, tiền kiểm bỏ qua 0, cổng cây thật ĐẠT, lỗi tự kiểm đột biến 0 | Caller delta 0; 470 mutant được giao lane khác, không đo 470/470 trong lượt này |
| `GIT_CONFIG_GLOBAL=<isolated> python scripts/tl.py --selftest` | Base/head rc0, tl 1731/1731, transport 12/12 | N6 N/N; delta 0, không lỗi signer |
| Full selftest r291:189→187 | rc1, 1730/1731, chỉ FAIL r291_docs_ngoai_goi | Đúng ratchet r291 có răng |
| Full selftest r357:189→187 | rc1, 1730/1731, chỉ FAIL r357_agents_ngoai_goi | Đúng ratchet r357 có răng |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, abbrev7 | HEAD rc0, ok=true, expected=checked=189; base rc2, ok=false, 187/187, extra wp-802 | N5/L3 đạt trên exact HEAD; không sinh lại manifest để làm xanh |
| `python scripts/tl.py doc-claims-check --strict` | Base/head rc0, ok=true | N4 đạt |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | Base/head rc0, 10 tệp/0 chỗ | Doctrine gate đạt trong scope scanner |
| `python review-data/static_checks.py` | rc0; bash -n, diff --check rc0; AST/YAML/prefix/parity đúng | Không nới write set |
| `python -m ruff check --no-cache --select F ...` | Base/head đều rc1: launcher_test 5→5; tl_selftest 4392→4392; tl.py 12→12; multiset code/message bằng nhau | Bare lint đỏ nền, delta 0. Ruff pin/probe contract not_run, không gọi lint sạch |
| `python review-data/probe_regressions.py` | rc0; F01/F02 direct và đối chứng r1 đạt assertion | Giữ hai finding đã đóng |
| `python review-data/probe_python.py` | rc0; 96 records/12 layout: wrapper đơn 12/12 rc0; direct bare 12/12 rc2, pin/absolute 24/24 rc0; batch rg→bash rc2/rg DO cuối 12/12, đảo rc0 12/12 | Giữ nguyên fixture lượt 3, không che lỗi bash prepend lại front; hai lượt đơn của rg→bash đều DAT |
| `python review-data/probe_full_yaml.py` | rc0, 24/24 source-chain rc0 và cả hai công cụ DAT; YAML byte-identical HEAD sha256 `44e2e99398d732ee98a917ee564a26b9326aaa94fd75d394310c9412c39ba057` | Dùng trạng thái PY/dấu đúng như cha trước vòng source; không phải toàn bộ batch mọi installer |
| `python review-data/probe_split_front.py` | rc0, 48/48 assertion: HEAD 24/24 batch rc0/DAT; r3 rg→bash 12/12 rc3 thiếu yaml, đảo 12/12 rc0 | Tách lỗi công thức bash đã có khỏi F03 Python; giữ 12 trục layout |
| `python review-data/probe_marker.py` | rc0 của script phản chứng, 16 records: dấu vắng/rỗng/khác PID rc0; trùng PID+PY venv thiếu yaml rc3; trùng PID không PY rc1; trùng PID+PY tốt rc0 | F04: set-u chỉ chặn thiếu biến, không chặn scalar lạ |
| `python review-data/probe_scope.py` | rc0, 10 records: cùng scalar/PID base+r3 rc0, HEAD rc3; marker nhập môi trường được truyền tới installer con; sạch thì ABSENT | Chứng minh regression và export attribute, không nói marker bất kỳ luôn làm hỏng |
| `python review-data/probe_new_process.py` | rc0 của script, 4/4 control (2 child rc0, 2 child rc3 kỳ vọng): tiến trình mới không nhận dấu nội bộ ở env sạch; chọn Python theo PATH mới | Invocation độc lập chọn lại được trong env sạch; không xoá phản chứng env giả ở F04 |
| `python review-data/audit_mutations.py` rồi `more_mutations.py` | rc0 từng script, 24/24 đúng TinHieuChotCa và frame ca đích; 23 hành vi + 1 cấu trúc | Ba shell mutant chạy một lần mỗi ca, không thêm DOT_BIEN_HOOK |

Bằng chứng: [required-summary.json](required-summary.json), [selftest-summary.json](selftest-summary.json), [ratchet-summary.json](ratchet-summary.json), [python-probes.json](python-probes.json), [split-front-controls.json](split-front-controls.json), [full-yaml-source-chain.json](full-yaml-source-chain.json), [marker-probes.json](marker-probes.json), [marker-scope.json](marker-scope.json), [new-process.json](new-process.json).

**Ma trận đúng 12 bố cục lượt 3**

Đường repository, interpreter, prefix và GITHUB_PATH có dấu cách; initial interpreter import yaml thành công, venv thật không yaml. `py` là shim yêu cầu và ghi nhận `-3`; không suy py.exe native. “Batch gốc” giữ rg hỏng và bash cùng thư mục như probe lượt 3; “front riêng” chỉ tách rg hỏng khỏi thư mục bash để loại nợ prepend của bash.

| Nền | Python ban đầu | Venv | Wrapper đơn/full YAML | Batch gốc rg→bash / bash→rg | Full-YAML source, hai thứ tự | Batch front riêng, hai thứ tự |
|---|---|---|---|---|---|---|
| linux | `python` | copy | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| linux | `python` | symlink | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| linux | `python3` | copy | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| linux | `python3` | symlink | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| linux | `py -3` | copy | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| linux | `py -3` | symlink | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| macos | `python` | copy | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| macos | `python` | symlink | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| macos | `python3` | copy | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| macos | `python3` | symlink | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| macos | `py -3` | copy | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |
| macos | `py -3` | symlink | rc0/DAT | rc2/rg DO cuối ; rc0/DAT | rc0, cả hai DAT | rc0/tổng DAT |

Batch thật dùng hai mục rg/bash lấy nguyên cấu trúc từ HEAD; full YAML khớp byte dùng ở wrapper đơn và source-chain. Chưa chạy batch cài mọi công cụ với YAML đầy đủ. Nợ công thức bash đã khai trong spec/handoff, không được vá lén hoặc tính là F03 tái diễn thiếu yaml; chi tiết phản chứng nằm trong finding notes.

**Bảng đột biến**

L=`r831_cai_rg_linux_chon_ban_chay_duoc`, M=`r831_cai_rg_macos_chon_ban_chay_duoc`, W=`r802_cai_rg_windows_chon_ban_chay_duoc`. Tín dụng chỉ khi type(exception) chính xác TinHieuChotCa, có frame ca đích và bang. Mỗi neo khớp đúng một lần; mutation chỉ trong bản sao/scratch. Ratchet dùng FAIL của full harness, không giả nhận là TinHieuChotCa.

| Mutant/chốt | Ca | Kết quả thật |
|---|---|---|
| Bỏ dòng ghim PY[0] | L,M | 2 kill hành vi, rc2/GITHUB_PATH rỗng ở chiều interpreter đơn |
| Bỏ phép dùng lại PY | L,M | 2 kill hành vi, batch rc3, thiếu yaml; TinHieuChotCa |
| Bỏ dòng gán dấu cha | L,M | 2 kill hành vi, batch rc3, thiếu yaml; TinHieuChotCa |
| Bỏ -x riêng hai nền | L,M | 2 kill hành vi, chọn sai candidate 0644 |
| Bỏ usrbin/brew candidate | L,M | 2 kill hành vi, không tìm được rg tốt |
| Checker → chỉ rg --version | L,M | 2 kill hành vi, chọn nhầm rc0-rỗng/rác |
| Ghi GITHUB_PATH vô điều kiện | L,M | 2 kill hành vi khi bare rg đã tốt |
| Năm wp831_yaml_* nguyên bảng HEAD | Theo L/M | 5 kill hành vi |
| wp802_yaml_chon_ung_vien_chi_theo_ma_thoat neo dài | W | 1 kill hành vi; neo Windows vẫn duy nhất |
| Bỏ ghi GITHUB_PATH | L,M | 2 kill hành vi, thiếu path cần persist |
| Bỏ fallback command-v | L,M | M: 1 kill hành vi. L: 1 kill cấu trúc ở _wp802_rg_yaml:8182; không nhận là kill hành vi |
| r291 189→187, bản sao riêng | r291 | rc1, 1730/1731, chỉ đúng r291 FAIL |
| r357 189→187, bản sao riêng | r357 | rc1, 1730/1731, chỉ đúng r357 FAIL |

Tổng chọn lọc **24/24 TinHieuChotCa (23 hành vi, 1 cấu trúc)** + **2/2 ratchet full kill đúng ca**. Không thêm ba shell mutant vào DOT_BIEN_HOOK. [mutations.json](mutations.json), [ratchet-summary.json](ratchet-summary.json).

**Launcher đầy đủ và giới hạn sandbox**

| Lượt | rc thật | Tổng kết raw |
|---|---:|---|
| `head-launcher-full` | 1 | 214/226 ca DA CHAY QUA (tong 236, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi |
| `head-launcher-full-fake` | 1 | 214/226 ca DA CHAY QUA (tong 236, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi |
| `base-launcher-full` | 1 | 212/224 ca DA CHAY QUA (tong 234, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi |
| `base-launcher-full-fake` | 1 | 212/224 ca DA CHAY QUA (tong 234, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi |
| `head-dot-bien-full` | 0 | DOT BIEN: 277/277 dat  (4 khong do duoc tren nen nay) |
| `base-dot-bien-full` | 0 | DOT BIEN: 272/272 dat  (4 khong do duoc tren nen nay) |

Cả absent/fake auth: tập 12 ca hỏng và 10 ca bỏ qua trên head/base giống nhau THEO TÊN, không có ca hỏng mới; head tăng đúng 2 ca qua. [full-delta.json](full-delta.json). Raw --dot-bien được ghi riêng; stock DOT_BIEN còn nhận exception ngoài TinHieuChotCa. Cụ thể head có bốn dòng kill nhận OSError ở các ca credential có control vốn đã đỏ trong sandbox. Không cấp tín dụng “277 kill thật bằng TinHieuChotCa” từ tổng kết raw; tập 24 mutant chọn lọc phía trên mới có audit loại/frame riêng. Không coi raw mutation N/N là full launcher xanh. So theo tên: 276 record chung giữ nguyên status; HEAD thêm đúng 5 wp831_yaml_* đều OK. [stock-mutation-delta.json](stock-mutation-delta.json).

Các fixture credential gặp `.git` trên ancestor `/tmp` và rv4, nên _KhoCodex từ chối với “Codex home is inside a repository”. Các ca phụ thuộc venv/pip bị bỏ qua phải giữ nhãn không đo được. Không đổi guard/security path, không chuyển scratch ra ngoài review-data, không bỏ `.git` để làm xanh. Probe namespace `unshare --user --map-root-user --mount true` rc1, uid_map Operation not permitted; không có capability để dựng runtime mount biệt lập. [sandbox-capabilities.json](sandbox-capabilities.json). Full suite rc1 hoặc skip không là N/N. Lời khai executor full launcher 234/234 không được tái lập trong môi trường này; 277/277 chỉ được xác nhận ở mức headline/rc của runner stock.

Hai lần soạn probe ban đầu có log riêng: phép batch gốc dừng ở rg DO cuối (đã giữ và đo đủ 12 layout), rồi chốt đọc log argv py bị vỡ vì đối số -c có xuống dòng. Đã sửa bộ ghi chỉ ghi đối số đầu tiên (-3) và chạy lại đủ 96 record; không tính lỗi giàn đo ấy thành finding hoặc mutation kill.

**Finding mới**

F04 [P2] `inherited-marker-reuses-scalar-python` — `ops/cai_cong_cu.sh:18`, `:60`.

Điều kiện ở dòng 18 chỉ so sánh giá trị của dấu với PID. Nó không xác minh dấu là biến nội bộ chưa export, cũng không xác minh PY là mảng do lượt cha tạo. Bash nhận biến môi trường PY dưới dạng scalar; scalar vẫn có phần tử số 0, nên `set -u` không chặn trường hợp này. HEAD dùng Python từ scalar ấy khi dấu trùng PID. Phép thử chỉ dùng interpreter thật của venv thiếu PyYAML; không có chương trình hay payload tấn công.

Ở cùng fixture, wrapper bash trên base và r3 tự chọn Python ban đầu và rc0; HEAD rc3/thiếu yaml. HEAD cũng rc0 khi bỏ dấu, giữ nguyên PY scalar. Dấu trùng PID nhưng không có PY cho rc1/unbound variable, chỉ chứng minh nhánh thiếu biến bị chặn. Nhận xét “fail-close” trong chú thích không chứng minh trường hợp có scalar an toàn.

Ngoài ra, phép gán ở dòng 60 không xoá thuộc tính export của biến đã được nhập từ môi trường. Installer con nhìn thấy PID cha khi biến dấu đầu vào mang giá trị bất kỳ. Nếu đầu vào không chứa dấu, installer con thấy ABSENT. Cả hai chiều chạy thật cho Linux và recipe macOS trên Bash Linux.

Đây là vi phạm trực tiếp spec r4 mục 2: một lần gọi độc lập vẫn tự chọn Python, dấu phải không export và không tin biến môi trường kế thừa. Đủ P2 vì thay đổi interpreter/bootstrap và có thể làm lời gọi hợp lệ thất bại; chưa chứng minh mở thêm biên đặc quyền. Không gán P1 hoặc tuyên bố khai thác.

Hướng sửa bằng lời: phân biệt rõ một lần gọi mới với lượt source nội bộ; chỉ dùng lại trạng thái đã được tạo trong đúng shell, có kiểu và thuộc tính phù hợp. Một dấu được nhập từ môi trường phải bị bỏ qua, kể cả trùng PID và đi kèm PY scalar. Khi tạo dấu cho vòng lặp, phải chủ động loại bỏ thuộc tính export có sẵn. Giữ nguyên mảng PY/đối số `-3`, đường dẫn có dấu cách và ghim interpreter. Không cung cấp patch runtime cho sensitive path.

Ca khóa: dùng interpreter venv thật thiếu yaml làm PY scalar trong môi trường, thử dấu vắng/rỗng/khác PID/trùng PID, có và không có PY; so với Python hợp lệ trên PATH. Lượt gọi mới phải tự chọn Python đó. Quan sát riêng trong installer con rằng không có dấu; thử cả biến dấu ban đầu được export. Giữ đủ 12 layout, hai thứ tự batch và ba đột biến shell hiện có. Rủi ro hướng sửa là xóa trạng thái của lượt cha ở lần source, vô tình chọn lại interpreter từ PATH đã thay đổi, mất `-3`, hoặc xử lý sai đường MSYS; native Git Bash còn chưa đo.

Quan sát thêm về nợ đã có: đúng fixture lượt 3 đặt rg hỏng và bash trong cùng thư mục initial tools. Lượt 4 giữ Python thành công, cả hai lượt đơn DAT, nhưng recipe bash đưa initial tools trở lại đầu PATH; tổng cuối rg DO/rc2 ở 12/12 layout. Đây thuộc công thức bash `dirname command-v`, vốn đã được spec/handoff kê là ngoài phạm vi, không phải một lớp F03 mới và không được vá lén trong packet. Tách rg hỏng sang thư mục front riêng cho đối chứng: HEAD 24/24 batch đạt, r3 rg→bash vẫn thiếu yaml 12/12. YAML đầy đủ byte-identical được dùng cho wrapper đơn và 24 source-chain với trạng thái cha; batch thật dùng hai mục nguyên từ HEAD. Chưa chạy batch cài mọi công cụ trong YAML đầy đủ.


**Toàn vẹn, phần chưa đo và quyết định**

Nguồn cay-kho **4355/4355 file/link kể cả .git không đổi hash/mode/đích symlink**; HEAD/tree đúng neo, status tracked/untracked/ignored, diff và index sạch. Bản sao head/base/ratchet sạch sau hoàn nguyên. Stock selftest/hook từng tạo fixture/state ignored trong các bản sao; các tệp ấy được bảo toàn hash và chuyển ra [gate-generated-artifacts.json](gate-generated-artifacts.json) trước phép kiểm sạch cuối, không che việc gate từng ghi scratch checkout. [integrity.json](integrity.json), [source-before.json](source-before.json), [source-after.json](source-after.json). Sandbox workspace-write; read-only với source là kỷ luật và phép so hai mốc, không chứng minh không từng ghi rồi hoàn nguyên.

**KHÔNG ĐO ĐƯỢC:** Windows Git Bash/py.exe/MSYS native, macOS native, CI ci.yml/launcher-windows.yml exact HEAD, lease/receipt/assurance live, model variant/effort. Recipe macOS và Windows fixture trên Bash Linux không thay chứng cứ native. Tool environment_status không có trong catalog; không suy readiness mạng/credential. Full 470 mutation cong_cu_test và Ruff pin/probe contract not_run. Không có P3 mới cần chủ kho quyết; nợ bash recipe và sandbox được ghi rõ ở trên.

VERDICT đã ghi tăng dần; snapshot trước khi biên tập bản cuối ở [VERDICT-progress.md](VERDICT-progress.md). Hash hiện vật sau khi writer kết thúc nằm trong [artifact-manifest.json](artifact-manifest.json).

**Quyết định: changes_requested** trên exact SHA ở dòng 2, vì F04 P2 chưa đóng. Cần sửa điều kiện tin trạng thái shell/môi trường và khóa bằng các ca marker/scalar kể trên, rồi review lại đúng SHA theo ngân sách r4; không tự cấp merge/land hoặc một lượt gọi tiếp theo.
