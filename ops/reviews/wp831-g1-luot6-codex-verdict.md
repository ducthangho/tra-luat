verdict: changes_requested
reviewed_sha: bbdfc019fdabc2bafc2ee5c3861e097e3c0a6b02

F01–F04 **ĐÃ VÁ THẬT** trên miền đã đo. Còn **F05 P2 `reverse-batch-fixture-escapes-installer-stubs`**: chiều bash→rg mới thêm đưa trình cài thật lên trước stub và làm ca Linux đỏ. Không có P0/P1/P3 mới. Không đạt ngưỡng approve khi F05 còn mở.

Reviewer độc lập OpenAI Codex, họ GPT-6 theo chỉ dẫn runtime; `provider: openai_codex`, `execution_surface: codex_service` (API agent có công cụ shell), `transport: machine`. Không đo model variant/effort, session/launcher receipt hoặc assurance live; không suy từ tài khoản vận chuyển. Executor Claude theo assignment. Agent `tl_auditor` chỉ đọc tài liệu/log theo CLAUDE.md §Quy trình sửa code/5, không chạy test hay ghi tệp.

Đã đọc toàn bộ prompt.snapshot được chỉ định, bốn spec, các diff và hai verdict trước; đối chiếu Spec lẫn Standards/Security. Chỉ đọc cay-kho/. Bản sao, mutation, fixture và hiện vật bền đặt trong review-data/. Không gọi GitHub, push, merge/land/deploy; không sửa nhánh executor. Đây là verdict nội dung offline, không thay quyền vận hành hoặc CI exact SHA.

**Neo, băm và phạm vi**

| Phép đo | Kết quả tự đo |
|---|---|
| HEAD / tree | `bbdfc019fdabc2bafc2ee5c3861e097e3c0a6b02` / `41ca2285ab46c0a4956c951dce4122a2be9de591` |
| Base nghiệm thu được giao | `6b641ca2a2b889c9f43eec58bae47a00a80373cd`; là tổ tiên của HEAD |
| origin/master snapshot | `2d33a0cd21b96bf3340b147fb57480ffce3b42a3` |
| SHA-256 SPEC-r1.md | `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888` |
| SHA-256 SPEC-r2.md | `3ab3aac4c68a7bbe87daf5dfee75c649ff46110697b2cd5b00b29586e4c253e7` |
| SHA-256 SPEC-r3.md | `dd8f0fab5e3592975e4cde2f180fe0d052fc66e67fae15194e71970cb02f65e6` |
| SHA-256 SPEC-r4.md | `5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad` |
| Bundle | diff.patch, numstat.txt, diff-tu-luot5.patch đều khớp BYTE Git; delta lượt 5 loại đúng ops/cong_cu_test.py và ops/bash_nen.py đến từ master |
| Master drift | 85 đường dẫn, tất cả ops/land/, giao write set = rỗng; merge-tree trên bản sao rc0, tree `cc549981bec3cf8a9ba97273992d85aa22e8b8bc` |
| Môi trường | Linux x86_64, Python 3.13.16, Bash 5.2.21, Ruff 0.17.1; bytecode tắt; Ruff --no-cache |
| Bản sao | local --no-hardlinks, detached exact SHA; core.abbrev=7, core.autocrlf=false; không mạng/fetch GitHub |

| Đường dẫn lease r4 | Thêm | Xóa |
|---|---:|---:|
| `.claude/dev/launcher_test.py` | 177 | 1 |
| `RELEASE_MANIFEST.json` | 16 | 6 |
| `changelog.d/wp-831.md` | 21 | 0 |
| `docs/GOI_AGENT_DA_NEN.md` | 17 | 3 |
| `ops/cai_cong_cu.sh` | 16 | 1 |
| `ops/cong_cu.yaml` | 10 | 2 |
| `ops/handoff/wp831-g1-claude.md` | 96 | 0 |
| `scripts/tl_selftest.py` | 7 | 5 |

Đúng **8 tệp / 360 dòng thêm / 18 dòng xóa**, dưới trần 8/450, đúng tám đường dẫn r4. YAML chỉ hai leaf rg Linux/macOS; install prefix Linux/macOS/Windows giữ nguyên. AST selftest chỉ hai hằng 187→189 và chú thích slot. Không xác minh lease/authority live; dùng assignment và spec băm làm phạm vi review. [preflight.json](preflight.json), [static-checks.json](static-checks.json), [master-drift.json](master-drift.json).

**Đối chiếu lượt trước — giữ ID/slug**

| ID / lớp | Lượt 6 | Phản chứng chạy được |
|---|---|---|
| F01 P2 `chooser-checker-path-fallthrough` | **ĐÃ VÁ THẬT** | probe_regressions.py: candidate 0644, front khác tốt; L/M in đúng front. Bỏ -x riêng từng nền làm đúng r831 đỏ ở assertion chọn thư mục, trên rig control xanh. |
| F02 P2 `linux-candidate-set-drops-usrbin` | **ĐÃ VÁ THẬT** | /usr/bin/rg thật tốt, seam vắng/rỗng, dpkg tốt→hỏng/đảo: HEAD luôn chọn /usr/bin, không gọi dpkg; recipe lượt 1 hỏng đúng chiều. Mutation bỏ ứng viên usrbin chết đúng assertion. |
| F03 P2 `chooser-path-reselects-python` | **ĐÃ VÁ THẬT**, đóng lớp allexport lượt 5 | 12 bố cục × cờ/môi trường × hai thứ tự: 48/48 rc0, rg/bash DAT, installer ABSENT; thêm normal và tùy chọn khác, HEAD 216/216. Lượt 5 cùng fixture tái hiện 24 lỗi rc3/thiếu yaml và 48 controls qua. A/B/C/G đều giết thật. |
| F04 P2 `inherited-marker-reuses-scalar-python` | **ĐÃ VÁ THẬT**, giữ đóng | Ma trận exec 576/576 DAT/ABSENT; matched PID + scalar qua exec: HEAD rc0, lượt 4 rc3 ở cài đơn cả hai nền. Thêm 8 allexport/scalar/batch controls đều DAT/ABSENT. D bị giết vì rò dấu, E còn chặn scalar nên không nhận D là chứng minh scalar được dùng lại. |

Lệnh phản chứng: `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_regressions.py`, `shell_matrix.py`, `marker_matrix.py`, `extra_comparisons.py` (ba tên sau cùng tiền tố review-data/). [regressions.json](regressions.json), [shell-matrix.json](shell-matrix.json), [marker-matrix.json](marker-matrix.json), [extra-comparisons.json](extra-comparisons.json).

**Bảng săn — lệnh → kết quả thật → ý nghĩa**

Các gate chạy trong review-data/head hoặc base với `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR/TMP/TEMP` riêng dưới review-data/tmp, `GIT_CONFIG_GLOBAL=review-data/gitconfig-selftest` (đường tuyệt đối), tắt ký commit/tag, core.abbrev=7. Auth absent/fake được đặt riêng; không dùng credential thật làm fixture. Command/cwd/rc/elapsed đầy đủ trong logs/*.result.json, stdout/stderr trong *.log. Selftest tuần tự HEAD → base → mutant r291 → mutant r357; không có hai selftest đồng thời.

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1 | HEAD absent/fake đều rc1, 0/1, 0 skip/1 hỏng tại bash→rg, sudoers | **F05**, control stock đỏ; không dùng làm kill mutant |
| Tương tự r831_cai_rg_macos_chon_ban_chay_duoc | HEAD absent/fake đều rc0, 1/1, 0 skip/hỏng | Recipe macOS qua fixture Bash Linux |
| Tương tự r802_cai_rg_windows_chon_ban_chay_duoc | HEAD/base × absent/fake đều rc0, 1/1 | Fixture Windows POSIX không hồi quy |
| Tương tự r802_bang_cai_rg_khop_cong_cu_yaml | HEAD/base × absent/fake đều rc0, 1/1; AST ca không đổi | Parity giữ |
| Cả 4 CLI trên HEAD, Bash trong thư mục fixture riêng | 8/8 invocation rc0, mỗi ca 1/1, 0 skip/hỏng | Đối chứng dương cho mutation; KHÔNG ghi đè stock fail |
| Head harness với wrapper+YAML base | Hai r831 đỏ TinHieuChotCa, wrapper rc2 ở chọn bản tốt | Base không có đăng ký r831; không giả gọi đó là ca base xanh |
| Test r5 trên cùng product HEAD | L/M đều qua | Tách hồi quy test mới F05 khỏi sản phẩm đã vá F03 |
| CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py | HEAD/base rc0, 61/61, 0 bỏ qua/tiền kiểm bỏ qua; cổng cây thật ĐẠT; lỗi tự kiểm đột biến=0 | Delta caller=0; 470 mutant giao job mảnh, KHÔNG đo 470/470 ở đây |
| python scripts/tl.py --selftest | HEAD/base rc0, 1731/1731, transport 12/12 | N6 đạt, delta0; ký Git cô lập |
| r291 189→187, full selftest riêng | rc1, 1730/1731, chỉ FAIL r291_docs_ngoai_goi | Ratchet có răng |
| r357 189→187, full selftest riêng | rc1, 1730/1731, chỉ FAIL r357_agents_ngoai_goi | Ratchet có răng |
| python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json | HEAD rc0, ok=true, expected=checked=189; base rc2, ok=false 187/187, extra wp-802 | N5/L3 đạt trên exact HEAD; không tái sinh manifest |
| python scripts/tl.py doc-claims-check --strict | HEAD/base rc0, ok=true | N4 đạt trong scope checker |
| python .claude/dev/packet_loop.py doctrine-scan --root . | HEAD/base rc0, 10 tệp/0 chỗ | Doctrine scan qua |
| python -m ruff check --no-cache --select F ... | Base/head cùng rc1; launcher 5→5, selftest 4392→4392, tl.py 12→12; multiset bằng | Bare lint đỏ nền, delta0 |
| loi_ruff_ci() qua runpy đúng .claude/dev/ci_dang_ky_test.py | HEAD/base rc0, RUFF_CONTRACT 3 [] | Pin/probe contract qua, riêng bare lint |
| bash -n ops/cai_cong_cu.sh; git diff --check BASE HEAD | rc0 cả hai | Shell và whitespace hợp lệ |

[required-summary.json](required-summary.json), [sealed-cases-summary.json](sealed-cases-summary.json), [base-new-case-comparison.json](base-new-case-comparison.json), [prior-case-comparison.json](prior-case-comparison.json), [selftest-summary.json](selftest-summary.json), [ratchet-summary.json](ratchet-summary.json), [ruff-tl-summary.json](ruff-tl-summary.json), [ruff-contract.json](ruff-contract.json).

**Ma trận shell và dấu**

12 bố cục = Linux/macOS × python/python3/py(-3) × venv copy/symlink. Repo/interpreter/prefix/GITHUB_PATH có dấu cách; initial Python import yaml được, candidate là venv thật không yaml; shim py xác minh mọi đối số đầu là -3. Tách rg hỏng khỏi thư mục Bash để đo F03. Tất cả recipe lấy nguyên từ YAML HEAD; batch dùng đúng hai mục như N8.

| Miền đo | Kết quả thật |
|---|---|
| Bash chuẩn / bash -a / SHELLOPTS=allexport, mỗi thứ tự | Mỗi mode 24/24 HEAD DAT/ABSENT; riêng allexport 48/48 |
| --posix / --posix -a / SHELLOPTS=allexport:posix / POSIXLY_CORRECT + -a / BASHOPTS=inherit_errexit + -a / localvar_inherit + -a | Mỗi mode 24/24 HEAD DAT/ABSENT; tổng 144/144 |
| Lượt 5 cùng fixture, normal/allexport × hai thứ tự | 24 lỗi rc3/thiếu yaml allexport rg→bash, 48 controls rc0; không tính lỗi kỳ vọng thành sản phẩm xanh |
| Dấu vắng/rỗng/khác PID/trùng PID × PY scalar không/có × dấu export/không × đơn/rg→bash/bash→rg × 12 layout | 576/576 rc0, mọi object DAT, installer có quan sát và chỉ ABSENT |
| Gán rồi declare +x, so với declare +x X=... một bước | 8 phép declaration: cách tách luôn declare -- / con ABSENT; một bước vẫn -x/con thấy PID dưới allexport, kể cả POSIX |
| set -k / -ak, môi trường tổng hợp | HEAD batch rc2; base script với YAML HEAD cũng rc2. Cài bash riêng head/base cùng rc0 nhưng export PATH cũ in danh sách export dưới -k. Không gán lỗi này cho marker mới hoặc mở finding packet từ nó |

Dấu không export biến mất qua exec; chiều đó là đối chứng biên tiến trình. PY scalar có mặt được export thật, PID trùng tạo trước exec. [shell-matrix-summary.json](shell-matrix-summary.json), [marker-matrix-summary.json](marker-matrix-summary.json), [declaration-probe.json](declaration-probe.json), [keyword-baseline.json](keyword-baseline.json), [keyword-probe.json](keyword-probe.json).

Wrapper đơn 12/12, direct bare Python 12/12 rc2 nhưng pin/absolute 24/24 rc0; full-YAML source-chain khớp BYTE HEAD 24/24, từng lượt DAT. Giữ fixture cũ rg hỏng cùng Bash: rg→bash 12/12 rc2/rg DO ở tổng cuối, hai lượt đơn DAT; đảo 12/12 qua. Đó là nợ recipe bash đã khai; F05 riêng là ca đảo mới khiến installer thoát fixture. [python-probes.json](python-probes.json), [full-yaml-source-chain.json](full-yaml-source-chain.json), [new-process.json](new-process.json).

**Bảng đột biến**

Mỗi mutant là bản sao riêng; mỗi ca đích chạy một lần trong rig kiểm soát Bash, sau khi phát hiện control stock đỏ. Positive control nguyên HEAD cùng rig: 8/8 CLI qua. Giết thật đòi TinHieuChotCa + frame ca/bang + đúng tính chất mutant; chỉ type/frame là chưa đủ.

| Mutant | L/M thực đo | Phân hạng cuối |
|---|---|---|
| A bỏ dùng lại PY | 2/2 batch rc3/thiếu yaml | **Giết thật** |
| B bỏ gán dấu cha | 2/2 batch rc3 | **Giết thật** |
| C bỏ ghim PY[0] | 2/2 wrapper đơn rc2, GITHUB_PATH rỗng | **Giết thật** |
| D bỏ loại dấu export đầu tệp | 2/2 installer thấy PID ở cài đơn | **Giết thật rò dấu**; E còn chặn scalar |
| E bỏ kiểm PY là mảng | 2/2 ca sống sót | **Sống sót**, không tín dụng giả. Source scalar+dấu nội bộ cùng shell: HEAD0/E3 hai nền, không phải input môi trường |
| G bỏ declare +x sau gán | 2/2 allexport rg→bash rc3/thiếu yaml | **Giết thật** |
| YAML: bỏ -x / candidate / checker chuẩn / điều kiện GITHUB_PATH, từng nền | 8/8 assertion đúng hành vi | **Giết thật** |
| Năm wp831_yaml_* + neo wp802 Windows kéo dài | 6/6 assertion đúng hành vi | **Giết thật** |
| Hai ratchet r291/r357, từng bản riêng | Chỉ đúng ca tương ứng FAIL | **Giết thật ratchet**, không nhận là TinHieuChotCa |

Tập AG chốt: **10 kill thật, 2 survivor, 0 kill bằng setup/skip**. Tập YAML riêng 14 kill thật; ratchet 2 kill thật. Không thêm AG vào DOT_BIEN_HOOK/sàn Windows. F đã gỡ khỏi HEAD theo phán lượt 5; không bịa mutant F ở lượt này. E giữ làm bất biến mảng; survivor không chứng minh thiếu test trên miền exec vì marker kế thừa đã bị loại trước guard.

Lượt dò ban đầu chưa cách ly Bash có 9 record rồi dừng: 7 kill đúng, **D Linux và E Linux là 2 tín dụng giả** do cùng sudoers như control HEAD. Trường result=killed trong JSON thô của lượt dò chỉ phản ánh type/frame; phân hạng cuối ở mutation-credit-audit.json. Không cộng hai lượt đo hoặc nhận E là kill. [mutations-ag.json](mutations-ag.json), [mutations-ag-unsealed.json](mutations-ag-unsealed.json), [mutation-credit-audit.json](mutation-credit-audit.json), [mutations.json](mutations.json).

**Launcher đầy đủ — kết quả stock và delta**

Hai clone riêng chạy cùng runner/env; trong mỗi clone absent → fake → --dot-bien tuần tự, mỗi invocation TMPDIR riêng. Đã đặt TMPDIR dưới review-data như prompt yêu cầu. Tự đo vẫn có `.git` tổ tiên ở rv6 và /tmp do sandbox mount; không xóa/đổi `.git`. Do đó credential fixture không thể đạt bằng đổi TMPDIR trong write root này. [tmpdir-ancestry.json](tmpdir-ancestry.json), [sandbox-mounts.json](sandbox-mounts.json).

| Lượt | rc | Headline nguyên log |
|---|---:|---|
| base-dot-bien-full | 0 | DOT BIEN: 272/272 dat  (4 khong do duoc tren nen nay) |
| base-launcher-full | 1 | 212/224 ca DA CHAY QUA (tong 234, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi |
| base-launcher-full-fake | 1 | 212/224 ca DA CHAY QUA (tong 234, bo qua 10, hong 12) - KHONG DU: 10 ca BO QUA, chua do gi |
| head-dot-bien-full | 0 | DOT BIEN: 277/277 dat  (4 khong do duoc tren nen nay) |
| head-launcher-full | 1 | 213/226 ca DA CHAY QUA (tong 236, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi |
| head-launcher-full-fake | 1 | 213/226 ca DA CHAY QUA (tong 236, bo qua 10, hong 13) - KHONG DU: 10 ca BO QUA, chua do gi |

Auth absent: base 12 đỏ, HEAD 13 đỏ; ca đỏ mới = `r831_cai_rg_linux_chon_ban_chay_duoc`; tập bỏ qua bằng nhau = True.

Auth fake: base 12 đỏ, HEAD 13 đỏ; ca đỏ mới = `r831_cai_rg_linux_chon_ban_chay_duoc`; tập bỏ qua bằng nhau = True.

12 lỗi credential chung do .git tổ tiên; 10 skip chung được liệt kê theo tên trong full-delta.json (2 ca Windows và 8 fixture venv/pip chưa dựng được; chưa xác định mạng là nguyên nhân duy nhất). HEAD thêm F05. Không gọi suite này N/N. Không nhận headline --dot-bien là mọi kill thật: stock-credit-audit.json tách 4 OSError tín dụng giả mỗi vế (control đã đỏ) và 6 receipt exception khác chưa chứng nhận kill hành vi; tập mutation chọn lọc phía trên mới có baseline dương và kiểm tính chất từng kill. [full-launcher-summary.json](full-launcher-summary.json), [full-delta.json](full-delta.json), [stock-credit-audit.json](stock-credit-audit.json).

**Finding mới F05 [P2] `reverse-batch-fixture-escapes-installer-stubs` — CHƯA VÁ**

Vị trí: `.claude/dev/launcher_test.py:8371`–`8383` (chiều đảo mới thêm), helper `:8292`–`:8303`. Khi Bash đầu PATH nằm ở `/usr/bin`, helper chỉ đặt sudo/apt-get stub trong `bin` ở trước PATH; không cung cấp Bash trong fixture. Lượt bash chạy trước dùng recipe nguyên `dirname "$(command -v bash)"`, nên wrapper prepend `/usr/bin`. Lượt rg tiếp theo phân giải sudo/apt-get thành `/usr/bin/sudo` và `/usr/bin/apt-get` thay vì stub; log tại đây chứng minh sudo thật đã chạy rồi báo lỗi, chưa chứng minh apt-get đã được thực thi. Trên môi trường này, ca Linux nguyên HEAD đỏ rc1 ở cả auth absent/fake, chỉ bash DAT và sudoers báo lỗi. Trên máy có sudo không cần mật khẩu, đường này có thể chạy trình cài thật; đây là suy luận từ đường executable đã đo, không khai đã cài thật.

Phản chứng không chạy trình cài thật: `PYTHONDONTWRITEBYTECODE=1 python review-data/probe_fixture_escape.py`. Script dựng fixture nguyên HEAD, chỉ thực thi lượt bash rồi đo `command -v sudo/apt-get`: unsealed trả `/usr/bin/sudo` và `/usr/bin/apt-get`; thêm Bash riêng trong vùng fixture giữ đúng hai stub. `fixture-escape.json` lưu command/rc/stdout. Raw CLI tại `logs/head-r831_cai_rg_linux_chon_ban_chay_duoc.log` và bản fake đều 0/1, không skip. Test lượt 5 chạy trên cùng product HEAD vẫn qua cả L/M (`prior-case-comparison.json`), nên đây là hồi quy của ca mới. Không quy lỗi này vào F03 đã vá hoặc chỉ gạt sang nợ recipe bash cũ.

Hướng vá BẰNG LỜI: chỉnh helper test để Bash được tìm thấy trong thư mục fixture riêng, bảo đảm recipe nguyên của bash prepend một thư mục vẫn giữ các installer stub ở trước đường hệ thống. Giữ recipe sản phẩm và ma trận allexport/hai thứ tự. Trước bước rg, đòi bằng chứng dương về đường executable và số lần installer stub được gọi; `set(thay) <= {"ABSENT"}` riêng lẻ không chứng minh đủ hai lượt cài đều được quan sát. Ca khoá: Bash hệ thống ở `/usr/bin`, cả hai thứ tự và hai cách bật allexport phải qua, mọi sudo/apt/brew được gọi đều là stub. Đột biến bỏ cách ly phải bị guard phát hiện TRƯỚC khi gọi host installer. Rủi ro bản vá: bố cục Bash mới có thể che mất chiều Python/rg hoặc đường có dấu cách; tiếp tục giữ initial Python có yaml, venv thật không yaml và test tên trần hỏng/candidate tốt.


**Toàn vẹn và giới hạn**

Nguồn cay-kho: 4395/4395 file/link kể cả .git không đổi hash/mode/đích symlink; HEAD/tree khớp, status kể cả ignored/untracked và diff/index sạch. Các bản sao head/base/ratchet sạch sau hoàn nguyên mutant. Hiện vật ignored do gate tạo được chuyển ra gate-generated-artifacts trước kiểm sạch cuối. Snapshot chứng minh hai mốc không có delta, không chứng minh chưa từng ghi rồi hoàn nguyên. Sandbox workspace-write; source read-only là kỷ luật kiểm chứng. [integrity.json](integrity.json), [source-before.json](source-before.json), [source-after.json](source-after.json), [gate-generated-artifacts.json](gate-generated-artifacts.json).

KHÔNG ĐO ĐƯỢC: macOS native, Windows Git Bash/MSYS/py.exe native; CI ci.yml/launcher-windows.yml exact HEAD, check run, lease/assurance/receipt live (không gọi GitHub theo assignment); model variant/effort; 470 mutant caller ở job mảnh. Recipe macOS và fixture Windows trên Linux không thay native evidence. Catalog không có environment_status nên không suy readiness credential/mạng từ skill cloud-environment-runtime. Chưa chạy batch cài mọi công cụ trên YAML đầy đủ; full-YAML source-chain chỉ đo hai công cụ.

VERDICT được ghi tăng dần; diễn tiến trước tổng hợp ở VERDICT-progress.md. Log khởi dựng/fixture lỗi không được tính pass hoặc kill; extra-comparisons-initial.log giữ ca so bản cũ batch đã chạm bootstrap pip và thất bại, sau đó phép so chuẩn chỉ dùng cài đơn để tránh cài gói thật. Không dùng lỗi bootstrap ấy đóng finding. artifact-manifest.json băm hiện vật sau khi writer/gate kết thúc.

**Quyết định: changes_requested**, vì F05 P2 còn mở trên exact SHA dòng 2. F01/F02 giữ đóng, F03 đóng lớp allexport, F04 giữ đóng. Không tự yêu cầu/thực hiện push, merge/land hoặc thêm review call.
