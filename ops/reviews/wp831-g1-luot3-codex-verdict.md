verdict: changes_requested
reviewed_sha: 6376cd33474f60c64e7605c8a3774a0c448dc703

**Phán cuối lượt 3/3: F01/F02 ĐÃ VÁ THẬT; F03 P2 `chooser-path-reselects-python` chỉ vá MỘT PHẦN, còn mở ở `--bat-buoc`.** Ngưỡng assignment không cho approve khi còn P0/P1/P2. Không phát hiện lớp finding mới; không có P0/P1 hoặc P3 mới được lập.

Reviewer Codex, họ OpenAI; provider `openai_codex`, execution surface `codex_service` (API agent có shell Linux), transport `machine`. Executor Claude theo assignment. Model variant/effort, session/launcher receipt, assurance và lease live: **KHÔNG ĐO ĐƯỢC**; không suy từ người vận chuyển verdict. Agent `tl_auditor` chỉ đọc log và đối chiếu cơ chế theo CLAUDE.md mục Quy trình sửa code/5, không chạy test hoặc ghi cây. Đây là verdict nội dung, không tự cấp trạng thái Packet hoặc quyền land.

Đã đọc toàn bộ prompt.snapshot, ba spec, hai verdict trước và các diff; kiểm cả Spec và Standards/Security, wrapper/checker/recipe/helper/mutation/caller liên quan. Mọi clone, fixture, mutation, log và output nằm trong `review-data/`. Không gọi GitHub, không push/merge/land, không sửa `cay-kho/`. Không soạn payload tấn công; installer trong fixture là stub, không cài apt/brew/pip thật.

## Neo và phạm vi

| Phép đo | Kết quả tự đo |
|---|---|
| HEAD / tree | `6376cd33474f60c64e7605c8a3774a0c448dc703` / `d2a85f18eb7b8d11219f64c956d788044df82b94` |
| Base `refs/remotes/origin/master` của source | `1e69d2a0d3c708efe0dec86752fc13a0fe039aab` |
| SPEC-r1 SHA-256 | `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888` |
| SPEC-r2 SHA-256 | `3ab3aac4c68a7bbe87daf5dfee75c649ff46110697b2cd5b00b29586e4c253e7` |
| SPEC-r3 SHA-256 | `dd8f0fab5e3592975e4cde2f180fe0d052fc66e67fae15194e71970cb02f65e6` |
| Bundle | `diff.patch`, `numstat.txt`, `diff-tu-luot2.patch` đều khớp BYTE với Git đúng hai đầu mút; [preflight.json](preflight.json) |
| Dựng cây | Clone local `--no-hardlinks --no-checkout`, detached exact SHA, origin đặt về endpoint gốc, không fetch; `core.abbrev=7`, `core.autocrlf=false` ở cả base/head |
| Runtime | Linux x86_64, Python 3.13.16, Bash GNU; Python tắt bytecode, Ruff `--no-cache`; TMPDIR riêng dưới review-data cho từng runner |
| Phạm vi shell r3 | Diff wrapper đúng 3 dòng chú thích + dòng ghim `PY[0]`; không đổi phần khác |
| YAML / selftest | Chỉ 2 leaf recipe Linux/macOS đổi; install prefix trước ` && ` đầu tiên của Linux/macOS/Windows giữ nguyên; r802 parity giữ nguyên. AST selftest chỉ có đúng 2 constant 187→189 sau khi bỏ chú thích |

Đúng 8 đường dẫn lease r3 được giao (7 r2 + wrapper), **258 thêm / 17 xóa**, 258 ≤ 450. Quyền lease live không được suy từ bảng offline này.

| Đường dẫn so base | Thêm | Xóa |
|---|---:|---:|
| `.claude/dev/launcher_test.py` | 120 | 1 |
| `RELEASE_MANIFEST.json` | 16 | 6 |
| `changelog.d/wp-831.md` | 16 | 0 |
| `docs/GOI_AGENT_DA_NEN.md` | 17 | 3 |
| `ops/cai_cong_cu.sh` | 4 | 0 |
| `ops/cong_cu.yaml` | 10 | 2 |
| `ops/handoff/wp831-g1-claude.md` | 68 | 0 |
| `scripts/tl_selftest.py` | 7 | 5 |

## Đối chiếu lượt trước — giữ finding ID/slug

| Finding / slug | Trạng thái cuối | Bằng chứng chạy được |
|---|---|---|
| F01 P2 `chooser-checker-path-fallthrough` | **ĐÃ VÁ THẬT**, Linux/macOS | `probe_regressions.py`: candidate `rg` mode 0644, front tốt; direct recipe rc0, in đúng front ở cả hai nền. Gỡ `-x` riêng mỗi nền làm đúng r831 đỏ bằng TinHieuChotCa tại assertion chọn thư mục, không phải lỗi dựng fixture. |
| F02 P2 `linux-candidate-set-drops-usrbin` | **ĐÃ VÁ THẬT** | `/usr/bin/rg --version` thật rc0/ripgrep 14.1.0. dpkg stub khai `/usr/bin/rg` rồi candidate hỏng khác; head chọn `/usr/bin`, không gọi dpkg, cả seam vắng/rỗng và đảo hai dòng. Recipe exact lượt 1 rc2 ở thứ tự tốt→hỏng, rc0 khi đảo. Mutant bỏ candidate usrbin bị đúng r831 Linux giết. |
| F03 P2 `chooser-path-reselects-python` | **MỘT PHẦN — còn mở** | Wrapper `rg` riêng đạt 12/12, nhưng batch rg→bash rc3/thiếu yaml 12/12. Cùng fixture đảo bash→rg đạt 12/12. Lặp source chain với YAML đầy đủ khớp BYTE HEAD cũng cho 12 lỗi/12 đối chứng qua. |

Bằng chứng: [regressions.json](regressions.json), [python-probes.json](python-probes.json), [source-chain.json](source-chain.json), [mutations.json](mutations.json). Lượt 2→3 chỉ có một lớp mở đầu vào là F03, đóng hoàn toàn 0/1; không đổi slug để xóa lịch sử. Hai lớp F01/F02 đã đóng từ lượt 2 và được đo lại ở đây.

## Bảng săn — lệnh → kết quả thật → ý nghĩa

Lệnh orchestration tính từ gốc rv3; lệnh gate nội bộ có cwd bản sao head/base. Mọi selftest đầy đủ chạy **TUẦN TỰ**: head, base, rồi hai mutant ratchet. `GIT_CONFIG_GLOBAL=review-data/gitconfig-selftest` giữ include config hiện có rồi tắt signing riêng cho fixture, không sửa global/home. Log raw và `*.result.json` ghi command/cwd/rc/thời gian thật.

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| `python review-data/preflight.py` | rc0; 3 spec đúng băm, 3 artifact khớp byte, 8 tệp / 258 dòng thêm | Đúng neo và trần r3 |
| `python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | HEAD có/không auth giả đều rc0; 1/1 qua, 0 bỏ qua, 0 hỏng | N1/N3/N7 stock đạt |
| Tương tự `r831_cai_rg_macos_chon_ban_chay_duoc` | Hai môi trường auth đều rc0, 1/1, 0 bỏ qua | N2/N3/N7 stock đạt trên Bash Linux |
| Tương tự `r802_cai_rg_windows_chon_ban_chay_duoc` | Base/head × hai môi trường auth đều rc0, 1/1, 0 bỏ qua | Fixture Windows trên POSIX không hồi quy; không chứng nhận native Windows |
| Tương tự `r802_bang_cai_rg_khop_cong_cu_yaml` | Base/head × hai môi trường auth đều rc0, 1/1, 0 bỏ qua | Parity Linux/Windows đạt; macOS được đối chiếu riêng bằng parse YAML |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` | Base/head đều rc0, **56/56 đạt**, 0 bỏ qua, tiền kiểm bỏ qua 0; cổng cây thật ĐẠT, lỗi tự kiểm đột biến 0 | Phạm vi caller của wrapper xanh, delta 0. Đây là chế độ gate có sẵn của kho, giao 470 bán kính đột biến sang lane khác |
| `python ops/cong_cu_test.py` mặc định | HEAD đã in 56/56, 0 bỏ qua; sau đó vào 470 mutant, reviewer dừng bằng Ctrl-C (terminal runner rc130; rc riêng của child không thu được) | **interrupted**, không nhận là full suite mặc định rc0 hoặc 470/470 đạt. Nguồn ghi vòng này khoảng 43 phút; không cần cho phép đo caller 56 ca đã chạy trong gate mode ở cả hai vế |
| `GIT_CONFIG_GLOBAL=<tệp cô lập> PYTHONDONTWRITEBYTECODE=1 python scripts/tl.py --selftest` | Base/head đều **rc0, tl 1731/1731**, transport 12/12 | N6 N/N, delta 0, không lỗi signer giả |
| Full selftest mutant r291:189→187 | rc1, **1730/1731**, chỉ `[FAIL] r291_docs_ngoai_goi`; r357 OK | Giết đúng ratchet r291 |
| Full selftest mutant r357:189→187 | rc1, **1730/1731**, chỉ `[FAIL] r357_agents_ngoai_goi`; r291 OK | Giết đúng ratchet r357; không chồng selftest |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (`core.abbrev=7`) | HEAD rc0, **ok=true, expected=checked=189**; base rc2, ok=false, 187/187, extra_files có wp-802 | N5/L3 đạt trên exact head; không sinh lại manifest để làm xanh |
| `python scripts/tl.py doc-claims-check --strict` | Base/head rc0, ok=true | N4 doc-claims đạt |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | Base/head rc0, 10 tệp/0 chỗ | N4 doctrine đạt |
| `python review-data/static_checks.py` | rc0; bash -n và git diff --check rc0; AST/prefix/parity đúng | Không vượt phạm vi sửa được cấp |
| `python -m ruff check --no-cache --select F --output-format json ...` | Base/head cùng 5 chẩn đoán launcher_test, cùng 4392 chẩn đoán tl_selftest, multiset code+message bằng nhau; mỗi lượt rc1 | Bare lint đỏ nền, **delta 0**; không gọi là lint sạch. Ruff pin/probe contract không chạy riêng |
| `python review-data/probe_python.py` | rc0 của probe; 96 records/12 layout đúng assertion | Python ban đầu có yaml, venv thật thiếu yaml; direct bare rc2, pin/absolute rc0, wrapper đơn rc0; batch còn lỗi như finding |
| `python review-data/probe_source_chain.py` | rc0; 24/24 assertion đạt, YAML đầy đủ khớp BYTE HEAD | Source lại rg→bash vẫn hỏng, đảo thứ tự qua; loại nghi can do schema YAML rút gọn |
| `python review-data/audit_mutations.py` | rc0, 16/16 killed, đúng type/frame ca đích | Các chốt yêu cầu vẫn có răng; không dùng mọi exception làm kill |

Biên ghi terminal bị ngắt: [head-cong-cu-interrupted.result.json](logs/head-cong-cu-interrupted.result.json); rc130 do reviewer quan sát từ công cụ terminal, không có returncode riêng của child trong raw log.

Log chính: [selftest-summary.json](selftest-summary.json), [ratchet-summary.json](ratchet-summary.json), [remaining-summary.json](remaining-summary.json), [logs/head-selftest.log](logs/head-selftest.log), [logs/base-selftest.log](logs/base-selftest.log), [static-checks.json](static-checks.json). Hai lỗi giàn đo khi soạn probe (đường dpkg chưa kết thúc `/bin/rg`, và đếm chuỗi DAT thay vì parse hai JSON) đã sửa trước khi nhận kết quả; log lỗi giữ riêng, không đếm thành finding/kill sản phẩm.

## Bảng đột biến

L = `r831_cai_rg_linux_chon_ban_chay_duoc`; M = `r831_cai_rg_macos_chon_ban_chay_duoc`; W = `r802_cai_rg_windows_chon_ban_chay_duoc`. Mỗi neo thay phải khớp đúng một lần. Chỉ cấp tín dụng khi **type(exception) chính xác TinHieuChotCa**, traceback có function ca đích và `bang`; toàn bộ frame/message trong mutations.json.

| Chốt / mutant | Ca | Kết quả thật |
|---|---|---|
| Bỏ dòng ghim PY[0] — một bản mutant, chạy một lần mỗi ca | L, M | 2 giết thật tại chiều venv F03; wrapper rc2/GITHUB_PATH rỗng. Không thêm vào DOT_BIEN_HOOK |
| Bỏ `-x` riêng Linux/macOS | L, M | 2 giết thật tại chiều candidate 0644 bị chọn nhầm |
| Bỏ candidate usrbin Linux / brew macOS | L, M | 2 giết thật; không còn tìm được rg tốt khi front hỏng |
| Đổi selector kiem-tra thành chỉ `rg --version`, riêng hai nền | L, M | 2 giết thật ở chiều rc0-rỗng/rác; ghi path sai rồi checker cuối từ chối |
| Bỏ điều kiện rg tên trần trước ghi GITHUB_PATH, riêng hai nền | L, M | 2 giết thật; bare rg đã DAT mà vẫn persist path |
| 5 `wp831_yaml_*` nguyên văn bảng HEAD | Theo khai báo L/M | 5 giết thật; các neo đều khớp một lần |
| `wp802_yaml_chon_ung_vien_chi_theo_ma_thoat` neo dài | W | 1 giết thật; không mất mutation Windows sau khi thêm checker POSIX |
| Ratchet r291 189→187, riêng một bản sao | r291 | Full harness FAIL đúng r291, 1730/1731 |
| Ratchet r357 189→187, riêng một bản sao | r357 | Full harness FAIL đúng r357, 1730/1731 |

Tổng tập launcher chọn lọc **16 giết thật / 0 survival / 0 tín dụng giả**; thêm **2 full ratchet kill đúng ca**. Không nhận đây là `launcher_test.py --dot-bien` toàn kho hoặc 470 mutation của cong_cu_test. Các bản sao sạch được giữ nguyên; mutation chỉ nằm trong scratch riêng.

## F03 [P2] — chooser-path-reselects-python — còn mở

**Vị trí:** `ops/cai_cong_cu.sh:22` (dòng mới ghim), khối chọn tại :14, vòng source :58, đọc recipe :63, prepend PATH :79; hai recipe tại `ops/cong_cu.yaml:93` và :94. Đây là biểu hiện tiếp theo cùng cơ chế F03 từ lượt 2, không lập F04 hoặc coi recipe bash cũ là một lỗi mới của packet.

**Cơ chế:** dòng ghim giữ đúng interpreter trong một lượt chạy `rg`, gồm selector và checker cuối. Nhưng `--bat-buoc` source lại chính script cho mỗi công cụ. Sau rg, parent đã prepend thư mục venv vào PATH. Lượt source cho bash chạy lại khối chọn và ghi đè PY bằng Python của venv; dòng :22 ghim chính bản vừa chọn sai đó. Nó không có PyYAML nên `cong_cu.py cai-lenh bash` không import được, rc3 trước khi cài/kiểm bash. Bootstrap PyYAML chỉ chạy ở nhánh TEN=--bat-buoc ban đầu, không cứu lần source TEN=bash. Vì vậy identity không được giữ suốt invocation batch như rủi ro lượt 2 đã yêu cầu đo.

**Phản chứng tự chạy:** `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_python.py`. Mỗi nền Linux/macOS có ba lựa chọn ban đầu `python`, `python3` và shim `py -3`, mỗi lựa chọn thử venv copy và symlink (12 layout). PATH ban đầu cô lập để thực sự đi nhánh được ghi, interpreter ban đầu import yaml rc0; venv thật không pip/không yaml import rc1; front rg exit1, candidate rg khai phiên bản hợp lệ. Repository, interpreter path, prefix và GITHUB_PATH đều có dấu cách. Direct PY tên trần rc2; chỉ pin PY[0] hoặc dùng absolute PY thì rc0/in đúng candidate. Wrapper thật `rg` riêng rc0/DAT/GITHUB_PATH=candidate 12/12.

Với cùng wrapper/checker/recipe/probe thật, YAML batch rút còn hai mục **rg→bash**: 12/12 rc3, stdout đã có rg DAT, stderr `ModuleNotFoundError: No module named 'yaml'` rồi thông báo không có công thức bash. Đảo **bash→rg**: 12/12 rc0, tổng DAT. YAML gốc cũng đặt rg ngay trước bash. Phép bổ sung `probe_source_chain.py` dùng YAML đầy đủ **byte-identical HEAD**, source hai công cụ như thân vòng batch: thêm 12 lỗi rg→bash và 12 đối chứng đảo thứ tự qua, stdout JSON được parse và xác nhận đúng cả hai công cụ DAT. Chưa gọi toàn bộ batch với mọi installer trong YAML; điều đã đo là nhánh batch thật với hai mục hợp lệ và source chain nguyên bản trên YAML đầy đủ.

Đây là lỗi tính sẵn sàng khi có nhiều Python hợp lệ trong máy, không cần payload hoặc sự kiểm soát từ actor ít quyền hơn. Lỗi đã có gốc trong caller trước packet; bản r3 đóng selector/đơn công cụ nhưng chưa đóng đường batch thuộc cùng rủi ro được giao đo. Không gán nó thành hồi quy mới không có bằng chứng.

**Hướng vá:** giữ interpreter do invocation chọn qua toàn bộ vòng cài và mọi lần source, thay vì chọn lại từ PATH đã đổi ở mỗi công cụ; giữ các phần tử đối số còn lại của PY và quoting. Thiết kế trạng thái/lifetime rõ để invocation độc lập vẫn tự chọn đúng Python. Nếu cần thêm thay đổi ngoài dòng ghim/chú thích được r3 cấp, phải để điều phối quyết revision/phạm vi, không vá ngầm. Đây là mô tả hướng, không phải patch runtime cho sensitive path.

**Ca khóa:** thêm chiều batch rg→bash trên venv thiếu yaml cho hai nền, đòi rc0 và cả hai DAT; mutation buộc chọn lại PY sau prepend phải làm đúng ca đỏ. Giữ chiều wrapper riêng, Python3-only, py giữ `-3`, path có khoảng trắng, symlink; chạy lại caller regression. Đảo thứ tự là đối chứng, không là cách vá vì không giữ bất biến cho batch tổng quát.

**Rủi ro hướng vá:** trạng thái PY rò giữa invocation, mất `-3`, quoting/space/symlink và đường MSYS của Git Bash; cần canh cùng danh tính ở selector, checker cuối và lần source kế tiếp. GITHUB_PATH persist cả thư mục vẫn có thể đổi công cụ khác ở bước shell sau; phép pin trong một tiến trình không chứng minh cách ly PATH ở tiến trình khác.

## Rủi ro đã đo / chưa đo

| Trục | Trạng thái và giới hạn |
|---|---|
| `py -3` | Shim POSIX yêu cầu `-3`, ghi argv và exec Python thật; mọi lần gọi wrapper đơn giữ đối số, đúng assertion. **Native Windows py.exe KHÔNG ĐO ĐƯỢC** |
| Quoting/space | 12 layout chạy thật với đường repository/prefix/interpreter/GITHUB_PATH có dấu cách; wrapper đơn đạt, batch thất bại đúng cơ chế reselect, không lỗi tách đối số |
| Symlink interpreter | Initial python/python3 qua symlink tới interpreter thật; venv thử cả symlinks=False và True. Wrapper đơn vẫn đạt |
| `--bat-buoc` / source lại | **ĐO ĐƯỢC: còn lỗi P2 F03**; 12/12 layout có đối chứng và full-YAML source chain bổ sung |
| Windows Git Bash `command -v python` trả MSYS path | **KHÔNG ĐO ĐƯỢC** native; fixture Windows trên Linux không thay chứng cứ này |
| macOS/BSD native | **KHÔNG ĐO ĐƯỢC**; recipe macOS được thực thi trên Bash/Linux với brew stub |
| CI `ci.yml`, `launcher-windows.yml` exact head | Executor khai xanh; **KHÔNG ĐO ĐƯỢC** do assignment cấm GitHub. Không gọi đó là gate tự xác minh |
| Full launcher có/không auth, full `--dot-bien` | **not_run** trong review này; đã đo 4 ca yêu cầu, auth absent/fake, cùng 16 mutant chỉ định |
| Full 470 mutation cong_cu_test | **interrupted/not_completed**; không chạy trọn ở base. Caller gate 56/56 và tự kiểm/cổng thực đã chạy ở cả hai cây |
| Security | Không thấy bằng chứng biên đặc quyền mới. Seam CONG_CU_GOC có tác dụng thật khi đặt; actor điều khiển môi trường có thể đổi candidate và persist thư mục khi bare rg hỏng. Chỉ mô tả hướng, không tạo payload; không tự nâng thành finding độc lập thiếu trust boundary |

## Toàn vẹn và quyết định

Nguồn `cay-kho/`: **4355/4355 file/link kể cả .git không đổi hash/mode/đích symlink**; HEAD/tree/base đúng neo; status gồm tracked/untracked/ignored, diff và index sạch. Bản sao head/base/ratchet sạch sau khi hoàn nguyên mutant: `True`. [integrity.json](integrity.json), [source-before.json](source-before.json), [source-after.json](source-after.json). Sandbox thực tế workspace-write; read-only với source là kỷ luật và đối chiếu hai mốc, không tự nhận sandbox cưỡng chế hoặc chứng minh không từng ghi rồi hoàn nguyên. Cloud environment_status không có trong tool catalog; không suy readiness credential/network.

VERDICT đã được ghi tăng dần; bản tiến độ trước khi chốt ở [VERDICT-progress.md](VERDICT-progress.md). [artifact-manifest.json](artifact-manifest.json) neo hash hiện vật sau khi writer hoàn tất.

**Quyết định cuối: changes_requested trên exact SHA ở dòng 2.** F03 P2 chưa đóng toàn bộ, nên không đạt ngưỡng approve dù các gate đã đo xanh và F01/F02 đã đóng. Lượt 3/3 đã dùng hết theo assignment; bằng chứng này cần về checkpoint/điều phối theo ngân sách hiện hành, không tự cấp thêm lời gọi, merge hoặc land.
