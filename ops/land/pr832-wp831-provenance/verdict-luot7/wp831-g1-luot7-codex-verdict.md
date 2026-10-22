verdict: approve
reviewed_sha: 51ae5c095972611d2c6045bd81786a4fc7e9ca62

F01–F05 **ĐÃ VÁ THẬT** trên miền đã đo. Không còn P0/P1/P2 mở; không có finding P3 mới hoặc P3 mở cần chủ kho quyết. Áp dụng ngưỡng trong prompt lượt 7: không P0/P1/P2 mở. Đây là approval nội dung offline trên exact SHA dòng 2; các giới hạn đo và cổng chưa chạy được ghi rõ dưới đây.

Reviewer độc lập OpenAI Codex, họ GPT-6 theo chỉ dẫn runtime; `provider: openai_codex`, `execution_surface: codex_service` (API agent có shell), `transport: machine`. Không đo model variant/effort, launcher receipt hoặc assurance live. Executor Claude theo assignment. Agent `tl_auditor` chỉ đọc hướng dẫn, mã và log theo `CLAUDE.md` §Quy trình sửa code/5; không chạy test hay sửa tệp.

Đã đọc toàn bộ `prompt.snapshot` được giao, spec r1→r4, diff và verdict lượt 5/6; review cả Spec lẫn Standards/Security. Chỉ đọc `cay-kho/`. Mọi clone, fixture, đột biến và output ở `review-data/`. Không gọi GitHub, push, merge, land hoặc chạy installer thật.

**Neo và phạm vi**

| Phép đối chiếu | Kết quả tự đo |
|---|---|
| HEAD / tree | `51ae5c095972611d2c6045bd81786a4fc7e9ca62` / `a59ccc5a870d2ab6f250e6a3f3ca9aa07d8729fa` |
| Merge-base nghiệm thu | `6b641ca2a2b889c9f43eec58bae47a00a80373cd`, là tổ tiên của HEAD |
| origin/master snapshot | `2d33a0cd21b96bf3340b147fb57480ffce3b42a3`; drift 85 đường dẫn, tất cả `ops/land/`, không giao write set |
| SHA-256 spec r4 | `5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad`; cả bốn spec khớp neo |
| Bundle | `diff.patch` và `diff-tu-luot6.patch` khớp byte Git |
| So lượt 6 | Chỉ `.claude/dev/launcher_test.py` và `ops/handoff/wp831-g1-claude.md`; mã sản phẩm không đổi |
| Bản sao | Clone cục bộ `--no-hardlinks`, detached exact SHA; `core.abbrev=7`, `core.autocrlf=false` |

| Đường dẫn lease r4 | Thêm | Xóa |
|---|---:|---:|
| `.claude/dev/launcher_test.py` | 187 | 1 |
| `RELEASE_MANIFEST.json` | 16 | 6 |
| `changelog.d/wp-831.md` | 21 | 0 |
| `docs/GOI_AGENT_DA_NEN.md` | 17 | 3 |
| `ops/cai_cong_cu.sh` | 16 | 1 |
| `ops/cong_cu.yaml` | 10 | 2 |
| `ops/handoff/wp831-g1-claude.md` | 106 | 0 |
| `scripts/tl_selftest.py` | 7 | 5 |

Đúng **8 tệp / 380 dòng thêm / 18 dòng xóa**, trong trần 8/450 và đúng tám đường dẫn r4. So sánh YAML chỉ đổi hai leaf `rg.cai.linux/macos`; phần installer trước ` && ` đầu tiên giữ nguyên. AST selftest chỉ đổi hai hằng ratchet 187→189; phần còn lại là chú thích. AST ca parity r802 không đổi. Không xác minh lease live; dùng assignment và spec băm làm phạm vi review. [Preflight](preflight.json), [đối chiếu tĩnh](static-checks.json).

**Đối chiếu lượt trước — giữ ID/slug**

| ID / lớp | Trạng thái trên HEAD | Phản chứng đã chạy |
|---|---|---|
| F01 P2 `chooser-checker-path-fallthrough` | **ĐÃ VÁ THẬT** | Ca r831 L/M chọn đúng front khi candidate 0644; mutation X bỏ `-x` làm đúng assertion chọn thư mục đỏ 2/2. Control HEAD xanh. |
| F02 P2 `linux-candidate-set-drops-usrbin` | **ĐÃ VÁ THẬT** | `CONG_CU_GOC` vắng/rỗng đều chọn `/usr/bin`, dpkg stub không được gọi. Bỏ candidate `/usr/bin` làm r831 Linux đỏ đúng rc2; installer vẫn là stub. |
| F03 P2 `chooser-path-reselects-python` | **ĐÃ VÁ THẬT**, giữ đóng allexport | 72/72 batch DAT với venv thật thiếu yaml, 3 tên interpreter, copy/symlink, hai thứ tự, normal/cờ/env allexport; A/B/C/G bị giết đúng rc3/rc2. Wrapper đơn và batch stock cũng qua. |
| F04 P2 `inherited-marker-reuses-scalar-python` | **ĐÃ VÁ THẬT** | Hai ca stock L/M đi cả cài đơn và batch qua exec trùng PID + PY scalar: rc0/DAT; installer quan sát đúng 1/2 lần và chỉ ABSENT. D chết vì rò dấu; E sống sót, không nhận thành kill scalar. |
| F05 P2 `reverse-batch-fixture-escapes-installer-stubs` | **ĐÃ VÁ THẬT** | Bash hệ thống `/usr/bin/bash`, đủ 8 tổ hợp L/M × hai thứ tự × hai cách allexport: rc0/DAT, entrypoint/path/count stub dương. H bỏ symlink chết tại `fixture ro` 2/2 trước wrapper batch. Phép dò helper lượt 6 chỉ chạy bước đầu và dừng, chứng minh đường hệ thống cũ. |

Lệnh tái lập từ gốc rv7: `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_review.py safety`, `... matrix`, `... mutations`; `python review-data/probe_yaml.py`; `python review-data/probe_routes.py` (đều dùng tiền tố bytecode trên). Các probe đọc sản phẩm từ clone đã neo, không vá cây nguồn. [Mutation A–H](mutations.json), [mutation YAML](yaml-mutations.json), [Q1 ngoài seam](q1-system.json).

**Bảng săn — lệnh → kết quả thật → ý nghĩa**

Các lệnh dưới chạy trong `review-data/head` và `review-data/base`. Mỗi invocation dùng `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR/TMP/TEMP` riêng tại `review-data/tmp/<nhãn>` và `GIT_CONFIG_GLOBAL` trỏ tuyệt đối đến [cấu hình cô lập](gitconfig-selftest), tắt ký commit/tag; `GIT_CONFIG_NOSYSTEM=1`. Auth vắng/giả đặt riêng; biến credential phiên không được dùng làm fixture. Selftest **tuần tự HEAD → base**, mỗi vế TMPDIR riêng. Command/cwd/rc/thời lượng trong `logs/*.result.json`.

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| `python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | HEAD absent/fake đều rc0, mỗi lần 1/1, 0 skip/hỏng | N1/N3/N7/N8 và guard F05 đo thật |
| Tương tự `r831_cai_rg_macos_chon_ban_chay_duoc` | HEAD absent/fake đều rc0, 1/1, 0 skip/hỏng | Recipe macOS qua fixture POSIX Linux |
| Tương tự `r802_cai_rg_windows_chon_ban_chay_duoc` | HEAD/base × absent/fake: 4/4 invocation rc0, mỗi lần 1/1 | Không hồi quy fixture Windows POSIX |
| Tương tự `r802_bang_cai_rg_khop_cong_cu_yaml` | HEAD/base × absent/fake: 4/4 rc0, mỗi lần 1/1 | Parity giữ; không sửa ca để cho qua |
| Harness HEAD + wrapper/YAML base | Hai r831 đỏ `TinHieuChotCa`, rc2 do chọn front hỏng | Delta hành vi có răng; base không đăng ký r831, không giả đếm ca vắng là xanh |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` | HEAD/base đều rc0, **61/61**, 0 skip/tiền kiểm skip; tự kiểm đột biến 0 lỗi, cổng cây thật ĐẠT | Delta 0 ca đỏ; **470 mutant giao job mảnh, không đo 470/470 ở đây** |
| `python scripts/tl.py --selftest` | HEAD/base rc0, **1731/1731** và transport 12/12 | N6 đạt, delta 0; ký Git đã cô lập |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | HEAD rc0, **ok=true, expected=checked=189**, failed/extras rỗng; base rc2, ok=false 187/187, extra `changelog.d/wp-802.md` | N5/L3 đã vá trên exact HEAD; không sinh lại manifest |
| `python scripts/tl.py doc-claims-check --strict` | HEAD/base rc0, ok=true | Tài liệu qua checker |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | HEAD/base rc0, 10 tệp/0 chỗ | N4 qua scan |
| `python -m ruff check --no-cache --select F ...` | HEAD/base cùng rc1; launcher 5, selftest 4392, tl.py 12; multiset lỗi bằng nhau | Bare lint còn lỗi nền; delta 0 |
| `bash -n ops/cai_cong_cu.sh`; `git diff --check BASE HEAD` | rc0 | Shell và whitespace hợp lệ |
| `python .claude/dev/launcher_test.py --dot-bien` | HEAD rc0, **277/277**, 4 không đo được; base rc0, **272/272**, 4 không đo được | Năm mutant wp831 và neo Windows đều qua; headline không chứng nhận mọi kill thật |
| `probe_review.py safety` / `matrix` | 8/8 / 72/72 rc0, DAT; mọi entry installer quan sát được thuộc stub | Đối chứng F03/F05, có path và số lần gọi |
| `probe_routes.py` | 16/16 phép dò bước đầu hoàn tất; lượt 6 sau bash trỏ sudo/apt ra `/usr/bin`, HEAD giữ fixture | Không chạy bước cài thứ hai ở đường có thể thoát |

[CLI chính thức](cli-summary.json), [kết quả tổng hợp](results-summary.json), [gate](gate-summary.json), [cong-cu và lượt strace ban đầu](required-summary.json), [stock mutations](stock-mutation-summary.json). Tám lượt `strace` ban đầu bị sandbox từ chối `PTRACE_TRACEME` trước khi Python chạy: **không có tín dụng test**, không phải tám ca sản phẩm đỏ. Mười hai CLI trong `cli-summary.json` là các lượt stock chạy lại thành công, không instrument test hay product.

**F05 — bằng chứng dương và săn đường thoát khác**

Probe safety giữ helper HEAD, wrapper và hai recipe nguyên văn; chỉ thêm lệnh ghi `$0`, argv, `command -v sudo/apt-get/brew` và marker vào entrypoint của ba stub. Không dùng rc0 đơn độc làm bằng chứng. Mỗi batch có cả báo cáo từng công cụ và tổng cuối DAT.

| Nền, mỗi tổ hợp thứ tự/allexport | Số lần vào executable giả | Đường đo được |
|---|---|---|
| Linux, 4 tổ hợp | sudo **2**, apt-get **2** | Tất cả `$0` và ba command-v đều `<fixture>/bin/...`; sudo gọi apt-get theo absolute path |
| macOS recipe, 4 tổ hợp | brew install **2**, brew --prefix **1** | Cả 3 vào `<fixture>/bin/brew`; prefix trả thư mục ứng viên trong fixture |

Tổng **28 entrypoint events** cho 8 batch; mọi marker `ABSENT`. [fixture-safety.json](fixture-safety.json) giữ argv, path, counts và trạng thái. Ma trận mở rộng có **72/72** và **252 events**: Linux/macOS × python/python3/py(-3) × venv copy/symlink × normal/-a/SHELLOPTS × hai thứ tự. Đường có dấu cách; từng candidate được kiểm thật là không import được yaml. [shell-matrix.json](shell-matrix.json). Đây là quan sát tại stub cộng đối chiếu recipe/đường phân giải; syscall trace không đo được do sandbox.

Helper lượt 6 lấy nguyên byte từ Git được chạy trong [probe_routes.py](probe_routes.py) với bước wrapper thay bằng **chỉ source công thức đầu**, đo đường phân giải rồi dừng trước công thức thứ hai. Sau bước bash của lượt 6, sudo/apt-get là `/usr/bin/sudo`, `/usr/bin/apt-get`; trên HEAD chúng luôn ở bin fixture. Không khai đã chạy full batch lượt 6 hoặc installer thật. [escape-routes.json](escape-routes.json).

Đã rà các đường cùng lớp:

- Hai recipe thực sự được đưa vào batch fixture là **rg và bash**, theo N8. Recipe rg chỉ prepend candidate/front trong fixture; recipe bash trả `bin/bash` nhờ symlink và guard trước wrapper. Cả hai thứ tự đã đo. H mất symlink bị chặn trước bước có thể cài thật.
- Các recipe git/python/shellcheck cũng có `dirname command-v` và có thể prepend thư mục hệ thống. Chúng không nằm trong bảng tối thiểu của ca r831. Không mở batch mọi công cụ hoặc đưa các recipe ấy vào fixture thiếu stub; nếu mở rộng ca sau này phải cách ly cả executable lẫn mọi installer trước khi chạy. Giữ nợ ngoài phạm vi mà spec/handoff đã khai.
- Brew thật trên macOS có thể cùng thư mục với Bash cài qua Homebrew. Symlink hiện ép tên trần bash vào bin fixture trước lượt nào prepend PATH; brew stub và prefix fixture đã được đo dương. **Không có macOS native trong phiên này**, không suy phép đo Linux thành native.
- Bare Python sau rg có thể trỏ venv thiếu yaml; cơ chế ghim/reuse vẫn giữ interpreter đầu, gồm đối số `py -3`. Không dùng thay đổi layout Bash để xoá chiều F03. Hai ca stock exec vẫn đo F04.
- Nhánh bootstrap của wrapper batch có ensurepip/pip khi Python đầu thiếu yaml. Các ca stock r831 trước hết đòi cài đơn DAT, nên bố cục thiếu yaml dừng trước batch. Probe reviewer dùng Python đầu đã import yaml được; bản script lưu còn có chốt dừng trước batch nếu thiếu yaml. Không thử bootstrap bằng installer thật. Helper trực tiếp không được coi là sandbox cho mọi môi trường tùy ý.

**Bảng đột biến — kiểm tín dụng**

Mỗi mutant có cây riêng dưới `review-data/mutants/`, dùng ca đích nguyên văn. CONTROL L/M cùng rig xanh 2/2. Giết thật đòi đúng `TinHieuChotCa`, frame ca/helper/bang và sai lệch đúng tính chất đột biến; không cấp tín dụng cho skip, setup error hoặc lỗi trùng control.

| Mutant | Thực đo Linux/macOS | Phân hạng |
|---|---|---|
| A bỏ dùng lại PY | 2/2 batch rc3, chỉ rg DAT, lỗi import yaml | **Giết thật sản phẩm** |
| B bỏ gán dấu cha | 2/2 batch rc3 | **Giết thật sản phẩm** |
| C bỏ ghim PY[0] | 2/2 cài đơn rc2, GITHUB_PATH rỗng | **Giết thật sản phẩm** |
| D bỏ loại marker export đầu tệp | 2/2 assertion thấy PID trong installer | **Giết thật rò dấu**; E vẫn chặn scalar, không suy thêm |
| E bỏ kiểm PY là mảng | 2/2 ca hoàn tất xanh | **Sống sót**; không tính thành kill. Marker môi trường đã bị loại trước guard; giữ phán phòng thủ của lượt 5/6 |
| G bỏ declare +x sau gán | 2/2 allexport rg→bash rc3, chỉ rg DAT | **Giết thật sản phẩm** |
| H bỏ symlink bash | 2/2 `fixture ro`, command-v là `/usr/bin/bash`; wrapper batch chưa được gọi | **Giết thật guard fixture**, không gộp thành kill sản phẩm |
| YAML X/CANDIDATE/CHECKER/GITHUB, từng nền | 8/8 đúng assertion; control xanh | **Giết thật sản phẩm** |
| HEAD harness + BASEPRODUCT | 2/2 lỗi đúng chọn bản hỏng | **So sánh nền**, không cộng thành hai mutant |

Tập được yêu cầu: **10 kill sản phẩm + 2 kill guard fixture, 2 survivor E, 0 tín dụng giả**, cộng 8 kill YAML độc lập. Không có mutant F trong HEAD; F đã gỡ ở lượt trước. Không thêm A–H vào DOT_BIEN_HOOK hoặc sàn Windows. [mutations.json](mutations.json), [yaml-mutations.json](yaml-mutations.json).

Stock `--dot-bien` vẫn chấp nhận ngoại lệ chung ở nhánh DOT_BIEN. Bốn kill OSError credential mỗi vế được tách khỏi tín dụng: control cùng ca trên head/base đã đỏ trước mutant vì `.git` tổ tiên trong sandbox. Các kill AssertionError trần khác của stock chưa được chứng nhận type/frame ở lượt này. Không đồng nhất 277/277 với 277 kill hành vi đúng; tập A–H/YAML ở trên mới có control dương và phân hạng riêng. [credit-controls.json](credit-controls.json) và các log `*-stock-dot-bien.log` lưu bằng chứng.

**Finding mới, giới hạn và toàn vẹn**

Không có finding P0–P3 mới. F05 tại `.claude/dev/launcher_test.py:8293`, `:8305`, `:8312`, `:8390`, `:8402` đã đóng bằng đổi fixture, guard và đếm lời gọi; không tái gán lỗi test ấy thành lỗi F03 sản phẩm.

**Không chạy full default launcher**: `_r345_venv` tại `.claude/dev/launcher_test.py:6557`–`:6565` tạo venv có pip rồi gọi pip install `pypdf==3.17.4` thật. Dừng đường này theo lệnh cấm installer của prompt; không khai full launcher N/N hoặc delta full ở lượt 7. `--dot-bien` đi nhánh riêng, bảng ca và đường gọi đã được rà trước khi chạy, không chạm helper pip này. Không gỡ `.git`, sửa credential guard hoặc thay suite để lấy số xanh.

Không đo Windows Git Bash/MSYS/py.exe native, macOS native, CI `ci.yml`/`launcher-windows.yml` trên exact HEAD chưa push, lease/receipt/assurance live hoặc 470 mutant cong-cu giao mảnh. Recipe macOS và fixture Windows chạy trên Linux không thay bằng chứng native. Các nợ recipe công cụ khác, sàn Windows và fixture full-suite của nền giữ như spec/handoff; không mở rộng packet hoặc tự cấp quyền vận hành.

Nguồn `cay-kho/`: **4395/4395 file/link, kể cả .git, giữ nguyên hash/mode/đích symlink**; HEAD/tree khớp, status sạch. Hai clone head/base sạch với tracked/untracked; mọi thử nghiệm ở bản sao. Snapshot chứng minh không có delta giữa hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên; source read-only là kỷ luật phiên, không phải mount read-only. [integrity.json](integrity.json), [source-before.json](source-before.json), [source-after.json](source-after.json).

Verdict được ghi tăng dần; [VERDICT-progress.md](VERDICT-progress.md) bảo toàn các mốc trước tổng hợp. Băm hiện vật/log cuối ở [artifact-manifest.json](artifact-manifest.json).

**Quyết định: approve** nội dung trên exact SHA dòng 2, với F01–F05 đóng và không P0/P1/P2 mở. Approval này neo kết quả review offline; việc xác nhận cổng native/CI và quyền push/merge/land thuộc quy trình của chủ kho.
