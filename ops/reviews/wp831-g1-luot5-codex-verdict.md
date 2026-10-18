verdict: changes_requested
reviewed_sha: 957ad2ebbc9adc14fee8d4676107249781a1bfb0

**Phán cuối lượt 5/8 (lượt cuối chủ kho yêu cầu): F01/F02 đóng; F04 đã vá biểu hiện môi trường/scalar; F03 P2 tái mở dưới `allexport`.** Không đủ ngưỡng approve vì còn một lớp P2 mở. Không lập P0/P1 hoặc P3 mới. Không tự cấp thêm lượt review, merge, land hay push.

Reviewer độc lập: OpenAI Codex, family GPT-6 theo runtime instructions; `provider: openai_codex`, `execution_surface: codex_service` (công cụ shell trong dịch vụ, không có bằng chứng đi qua lệnh `codex` hoặc Desktop), `transport: machine`. Không đo được model variant/effort, identity/receipt launcher hoặc assurance live. Executor trong assignment: Claude; không tái sử dụng context executor. Đây là kết luận nội dung offline, không thay biên nhận/ủy quyền hay CI exact HEAD.

Đã đọc toàn bộ `prompt.snapshot` được chỉ định và bốn spec, đối chiếu verdict lượt 3/4. Chỉ đọc `cay-kho/`; mọi clone, mutation, fixture, log và kết quả nằm trong `review-data/`. Không gọi GitHub, không sửa branch executor. Python 3.13.16, Bash 5.2.21, Ruff 0.17.1, Linux x86_64; macOS là recipe trên Bash Linux, `py -3` là shim có kiểm đối số, không phải bằng chứng native.

**Neo, băm và phạm vi**

HEAD `957ad2ebbc9adc14fee8d4676107249781a1bfb0`, tree `7aea6154b580feab1990e26074ec9af80bd9d6ae`; base `577d7b95d257f6c376677e1ffb0131d12b74d24e`. Base là tổ tiên của HEAD; merge có đúng parent master này. `diff.patch`, `numstat.txt`, `diff-tu-luot4.patch` đều khớp BYTE Git; delta lượt 4 đã loại đúng `ops/land`. Ba commit mới trên master chỉ đổi `ops/land/pr823-wp802-*`, không đổi runtime/test của packet. [preflight.json](preflight.json), [master-authority.json](master-authority.json).

| Spec | SHA-256 tự đo |
|---|---|
| SPEC-r1.md | `92d179bca46c3523f1ce21e3a65bd06d6074237ffa79b8bf293cba3179659888` |
| SPEC-r2.md | `3ab3aac4c68a7bbe87daf5dfee75c649ff46110697b2cd5b00b29586e4c253e7` |
| SPEC-r3.md | `dd8f0fab5e3592975e4cde2f180fe0d052fc66e67fae15194e71970cb02f65e6` |
| SPEC-r4.md | `5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad` |

| Đường dẫn lease r4 | Dòng thêm | Dòng xóa |
|---|---:|---:|
| `.claude/dev/launcher_test.py` | 157 | 1 |
| `RELEASE_MANIFEST.json` | 16 | 6 |
| `changelog.d/wp-831.md` | 20 | 0 |
| `docs/GOI_AGENT_DA_NEN.md` | 17 | 3 |
| `ops/cai_cong_cu.sh` | 14 | 1 |
| `ops/cong_cu.yaml` | 10 | 2 |
| `ops/handoff/wp831-g1-claude.md` | 86 | 0 |
| `scripts/tl_selftest.py` | 7 | 5 |

Tổng **8 tệp / 327 dòng thêm / 18 dòng xóa**, dưới trần 8/450 và đúng tám đường dẫn spec r4. Lease object `31d9641`/refs lease không có trong bundle cục bộ; không gọi GitHub để suy ra lease hiện còn hiệu lực. Đối chiếu write set dựa trên spec đã băm và assignment, không tuyên bố đã xác minh authority live.

**Đối chiếu lượt trước — giữ ID/slug**

| ID / lớp / nguồn | Phân loại lượt 5 | Phản chứng chạy độc lập |
|---|---|---|
| F01 P2 `chooser-checker-path-fallthrough`, lượt 1–4 | **ĐÃ VÁ THẬT** | `probe_regressions.py`: candidate mode 0644, front khác chạy tốt; Linux/macOS rc0 và in đúng front. Bỏ `-x` riêng từng nền làm đúng r831 đỏ vì chọn sai thư mục. |
| F02 P2 `linux-candidate-set-drops-usrbin`, lượt 1–4 | **ĐÃ VÁ THẬT** | `/usr/bin/rg` thật tốt; seam vắng/rỗng, dpkg khai tốt→hỏng và đảo: HEAD luôn chọn `/usr/bin`, không gọi dpkg. Recipe lượt 1 hỏng đúng thứ tự tốt→hỏng. Bỏ candidate usrbin giết đúng r831 Linux. |
| F03 P2 `chooser-path-reselects-python`, lượt 2–4 | **MỘT PHẦN — TÁI MỞ** | Shell chuẩn: wrapper đơn 12/12, full-YAML source 24/24, batch front riêng 24/24 đều DAT. Nhưng `bash -a` hoặc môi trường `SHELLOPTS=allexport`: batch rg→bash rc3/thiếu yaml 12/12 cho mỗi cách bật, trong khi normal/đảo thứ tự/lượt 4 cùng fixture đều đạt. |
| F04 P2 `inherited-marker-reuses-scalar-python`, lượt 4 | **ĐÃ VÁ THẬT biểu hiện đã báo; bản vá tái mở F03** | 576/576 ma trận exec qua 12 bố cục đạt; installer chỉ thấy ABSENT. Cùng marker trùng PID + PY scalar: lượt 4 rc3, HEAD rc0. Mutation D vẫn đỏ vì rò dấu, không vì scalar được dùng lại: chốt kiểu E còn chặn scalar. |

Không dùng số ca xanh để xóa lịch sử lớp. Tập mở cuối lượt 4 là F04, nay đóng biểu hiện đó (1/1), nhưng F03 là lớp tái mở phải báo riêng; tỷ lệ đóng 100% của tập cũ không chứng minh hội tụ.

**Bảng săn — lệnh → kết quả thật → ý nghĩa**

Lệnh gate chạy trong bản sao tương ứng `review-data/head` và `base`; launcher có/không `CODEX_AUTH_JSON` giả, không dùng credential thật. `PYTHONDONTWRITEBYTECODE=1`, `core.abbrev=7`. Full selftest TUẦN TỰ head → base → mutant r291 → mutant r357; `GIT_CONFIG_GLOBAL` riêng include config thường rồi tắt ký commit/tag. Mỗi command/cwd/rc/elapsed có `.result.json` và raw log.

| Lệnh / phép đo | Kết quả thật | Ý nghĩa |
|---|---|---|
| `python review-data/preflight.py` | rc0; 4 băm spec, 3 artifact byte-equal, 8/327 | Neo và trần r4 đạt |
| `python .claude/dev/launcher_test.py --lap-ca r831_cai_rg_linux_chon_ban_chay_duoc --lan 1` | HEAD absent/fake: mỗi lượt rc0, 1/1, 0 skip/đỏ | Ca stock đạt trong shell chuẩn |
| Tương tự `r831_cai_rg_macos_chon_ban_chay_duoc` | HEAD absent/fake: mỗi lượt rc0, 1/1, 0 skip/đỏ | Recipe macOS đạt trên Bash Linux |
| Tương tự `r802_cai_rg_windows_chon_ban_chay_duoc` | HEAD/base × absent/fake: đều rc0, 1/1 | Fixture Windows POSIX không hồi quy |
| Tương tự `r802_bang_cai_rg_khop_cong_cu_yaml` | HEAD/base × absent/fake: đều rc0, 1/1 | Parity không đổi; AST ca này byte-equivalent |
| Chạy hai r831 của HEAD với code/YAML base qua harness ngoài | Cả hai đỏ bằng TinHieuChotCa tại assertion chọn bản tốt | Base chưa đăng ký hai ca mới; không giả gọi đó là ca base đã xanh |
| `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` | HEAD/base rc0, 56/56, 0 bỏ qua, 0 tiền kiểm bỏ qua, cổng cây thật ĐẠT, 0 lỗi tự kiểm đột biến | Delta caller 0. 470 mutant được giao lane mảnh, không được đo 470/470 ở đây |
| `GIT_CONFIG_GLOBAL=<isolated> python scripts/tl.py --selftest` | HEAD/base rc0, tl 1731/1731, transport 12/12 | N6 đạt, delta 0, không signer lỗi |
| Đặt r291 189→187, full selftest riêng | rc1, 1730/1731, chỉ FAIL r291_docs_ngoai_goi | Ratchet r291 có răng |
| Đặt r357 189→187, full selftest riêng | rc1, 1730/1731, chỉ FAIL r357_agents_ngoai_goi | Ratchet r357 có răng |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | HEAD rc0, ok=true, expected=checked=189; base rc2, ok=false, 187/187, extra wp-802 | N5/L3 đạt trên exact HEAD, không tái sinh manifest trong review |
| `python scripts/tl.py doc-claims-check --strict` | HEAD/base rc0, ok=true | N4 đạt trong scope checker |
| `python .claude/dev/packet_loop.py doctrine-scan --root .` | HEAD/base rc0, 10 tệp/0 chỗ | Doctrine scan đạt |
| `python review-data/static_checks.py` | rc0; bash -n/diff --check rc0; chỉ hai lá YAML rg thay đổi; AST selftest chỉ hai hằng 187→189 | Phạm vi hẹp giữ đúng spec |
| `python -m ruff check --no-cache --select F ...` | Base/head rc1: launcher_test 5→5, tl_selftest 4392→4392, tl.py 12→12; multiset code/message bằng nhau | Bare lint đỏ nền, delta 0; không gọi lint sạch |
| `loi_ruff_ci()` qua runpy trên đúng checkout | HEAD/base rc0, RUFF_CONTRACT 3 [] | Contract pin/probe riêng biệt với lint |
| `python review-data/probe_regressions.py` | rc0; F01/F02 và đối chứng lượt 1 đúng assertion | Giữ các lớp đã đóng |
| `python review-data/probe_python.py` | rc0, 96 record: wrapper 12/12 rc0, bare 12/12 rc2, pin/absolute 24/24 rc0 | Giữ đủ interpreter/venv/path-space của lượt 3 |
| `python review-data/probe_full_yaml.py` | rc0, 24/24 source-chain, mỗi lượt DAT; YAML khớp BYTE HEAD | Đo vòng source trên YAML đầy đủ, không cài mọi công cụ |
| `python review-data/probe_split_front.py` | rc0, 48 assertion: HEAD 24 batch DAT; r3 rg→bash rc3 12/12, đảo 12/12 DAT | Tách nợ bash prepend front khỏi F03 |
| `python review-data/probe_new_process.py` | rc0, 4/4 controls; dấu không truyền vào process mới; Python chọn theo PATH process đó | Lifetime độc lập trong shell chuẩn |
| `python review-data/marker_matrix.py` | rc0, 576/576; mọi installer marker ABSENT | F04 input matrix đạt |
| Hai `external-matrix-E/F.py` | mỗi script rc0, 96/96; installer marker ABSENT | E/F tương đương HEAD trên miền input môi trường đã đo |
| `python review-data/reachability.py` | rc0, 58 record; E khác HEAD chỉ ở source với trạng thái scalar+dấu do cùng shell dựng; F không khác; allexport làm HEAD/E/F đều hỏng cùng chiều | Không nhận surviving mutant là test thiếu răng mà chưa phân miền input |
| `python review-data/allexport_layouts.py` | rc0 của giàn đo; 144 record: 24 lỗi HEAD rc3 kỳ vọng, 120 controls rc0/DAT | F03 P2 tái mở; rc0 của probe KHÔNG phải sản phẩm xanh |
| Phép so marker trùng PID + scalar trên HEAD/lượt 4 (`f04-comparison.json`) | 8/8 assertion; HEAD rc0, lượt 4 rc3 khi có marker | Khóa phản chứng F04 cũ thực sự |

Bằng chứng: [required-summary.json](required-summary.json), [selftest-summary.json](selftest-summary.json), [ratchet-summary.json](ratchet-summary.json), [static-checks.json](static-checks.json), [ruff-tl-summary.json](ruff-tl-summary.json), [ruff-contract.json](ruff-contract.json), [base-new-case-comparison.json](base-new-case-comparison.json).

**Ma trận dấu và 12 bố cục lượt 3**

Mỗi layout: Linux/macOS × python/python3/py(-3) × venv copy/symlink; repo/interpreter/prefix/GITHUB_PATH có dấu cách. Interpreter ban đầu import yaml được; venv thật không có yaml. Ma trận exec là 4 trạng thái dấu (vắng/rỗng/khác PID/trùng PID) × 2 trạng thái PY scalar (không/có, trỏ venv) × 2 thuộc tính dấu đầu vào (export/không) × 3 lời gọi (đơn, rg→bash, bash→rg) = 48/layout, tổng 576. PID trùng được tạo trước exec nên giữ đúng PID. Dấu không export biến mất qua exec, giữ chiều đó làm đối chứng biên tiến trình; không giả gọi nó là biến môi trường đã nhập. Dấu vắng nhưng đánh dấu export không có giá trị cũng không đi qua exec. PY scalar có mặt được export thật.

| Nền | Python đầu | Venv | Ma trận exec | Shell chuẩn: đơn / source full / batch front riêng | allexport rg→bash (hai cách bật) | Controls normal/đảo thứ tự/lượt 4 |
|---|---|---|---|---|---|---|
| linux | `python` | copy | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| linux | `python` | symlink | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| linux | `python3` | copy | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| linux | `python3` | symlink | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| linux | `py -3` | copy | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| linux | `py -3` | symlink | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| macos | `python` | copy | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| macos | `python` | symlink | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| macos | `python3` | copy | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| macos | `python3` | symlink | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| macos | `py -3` | copy | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |
| macos | `py -3` | symlink | 48/48 DAT, ABSENT | DAT / 2 DAT / 2 DAT | rc3/thiếu yaml cả hai | tất cả rc0/DAT |

Giữ nguyên fixture gốc lượt 3 đặt rg hỏng cùng thư mục bash: cả 12 layout vẫn có batch rg→bash rc2/rg DO ở phép tổng CUỐI, dù hai lượt cài riêng DAT; đảo thứ tự rc0. Đây là nợ recipe bash đã khai ngoài scope, không dùng nó làm bằng chứng F03 mới. Các matrix đạt ở trên tách rg hỏng sang front riêng; recipe rg/bash vẫn lấy nguyên từ HEAD. Wrapper đơn/full-source dùng YAML đầy đủ khớp byte; batch thật dùng bảng tối thiểu hai mục như N8. Chưa chạy batch cài mọi công cụ của YAML đầy đủ.

[marker-matrix.json](marker-matrix.json), [python-probes.json](python-probes.json), [full-yaml-source-chain.json](full-yaml-source-chain.json), [split-front-controls.json](split-front-controls.json), [allexport-layouts.json](allexport-layouts.json), [f04-comparison.json](f04-comparison.json).

**Bảng đột biến**

A–F: một bản sao riêng mỗi mutant, chạy một lần mỗi ca r831 Linux/macOS. “Giết thật” đòi đúng type TinHieuChotCa và frame ca đích/bang; skip, exception khác hoặc lỗi dựng fixture không có tín dụng.

| Mutant | L/M thực đo | Phân hạng và nghĩa |
|---|---|---|
| A bỏ dùng lại PY | 2/2 TinHieuChotCa, batch rc3, chỉ rg DAT | **Giết thật hành vi**: reselection sau đổi PATH |
| B bỏ gán dấu cha | 2/2 TinHieuChotCa, batch rc3 | **Giết thật hành vi**: lifetime batch mất |
| C bỏ ghim PY[0] | 2/2 TinHieuChotCa, wrapper đơn rc2/GITHUB_PATH rỗng | **Giết thật hành vi**: Python candidate thay bản đầu |
| D bỏ loại dấu export đầu tệp | 2/2 TinHieuChotCa: installer đơn thấy PID | **Giết thật hành vi rò dấu**; không nói scalar được dùng lại vì E vẫn còn |
| E bỏ kiểm PY là mảng | 2/2 ca sống sót; thêm 96/96 input môi trường đạt | **Sống sót**, không tín dụng giả. Source với scalar+dấu không export do cùng shell dựng: E rc3, HEAD rc0 (cả hai nền) |
| F bỏ unset trước gán dấu cha | 2/2 ca sống sót; thêm 96/96 input môi trường đạt | **Sống sót**, không tín dụng giả; đầu tệp đã loại export, không có phép gán dấu xen giữa; dưới allexport thì có/không F đều tái export |
| YAML: bỏ -x / candidate / chuẩn checker / điều kiện GITHUB_PATH, từng nền | 8/8 giết thật hành vi | F01/F02/N1–N3 có phản chứng |
| Năm wp831_yaml_* + neo wp802 Windows kéo dài | 6/6 giết thật hành vi | Neo đúng một lần; parity Windows giữ |
| r291:189→187, bản sao riêng | full rc1/1730 trên 1731, chỉ đúng r291 FAIL | **Giết thật ratchet**, không giả nhận là TinHieuChotCa |
| r357:189→187, bản sao riêng | full rc1/1730 trên 1731, chỉ đúng r357 FAIL | **Giết thật ratchet** |

Chọn lọc: **22 kill hành vi bằng TinHieuChotCa (8 A–D + 14 YAML), 4 lần sống sót E/F, 0 tín dụng giả trong tập này**, cộng 2 kill ratchet. Không thêm A–F vào DOT_BIEN_HOOK/sàn Windows. [mutations-af.json](mutations-af.json), [mutations.json](mutations.json), [ratchet-summary.json](ratchet-summary.json).

**Phán lời khai E/F.** Với invocation mới chỉ mang biến môi trường vô hướng, không nạp thêm shell code: marker nhập có export và bị loại trước guard; shell cha tự tạo PY mảng; không có đường dữ liệu bình thường nào tạo lại marker trước vòng batch. 96 input mỗi mutant cho kết quả tương đương HEAD. E có giá trị phòng thủ khi source trong shell đã có trạng thái bất thường; phản chứng ấy đã chạy nhưng cần tự tạo nội bộ scalar+dấu, không phải input exec. F là lớp dư trên luồng hiện tại; có thể gỡ để giảm tuyên bố dư thừa, không phải yêu cầu sửa để đạt approval. Không bắt buộc gỡ E vì nó diễn đạt invariant PY là mảng. Không tính hai survivor thành “2 kill”, cũng không thêm test soi chính dòng code để lấy điểm mutation. BASH_ENV/trap/function tùy ý có thể viết lại trạng thái shell, không được viện làm phản chứng môi trường thuần.

Lời khai rộng “mọi đầu vào bên ngoài đã chặn” không đủ: `allexport` đi vào bằng cờ Bash hoặc SHELLOPTS ngoài tiến trình, không cần BASH_ENV, source tùy ý hay sửa code. HEAD/E/F cùng hỏng; E/F không vá được lớp này. Cần sửa invariant tạo dấu ở F03, không chỉ đổi số đếm mutation.

**Launcher đầy đủ, delta và giới hạn sandbox**

HEAD/base chạy đồng thời trên hai clone --no-hardlinks riêng; trong mỗi clone, absent → fake → --dot-bien chạy tuần tự, mỗi invocation có TMPDIR/log riêng. Toàn bộ full selftest và hai ratchet đã kết thúc trước khi chạy launcher.

| Lượt | rc thật | Headline raw |
|---|---:|---|
| `base-launcher-full` | 1 | 220/232 ca DA CHAY QUA (tong 234, bo qua 2, hong 12) - KHONG DU: 2 ca BO QUA, chua do gi |
| `base-launcher-full-fake` | 1 | 220/232 ca DA CHAY QUA (tong 234, bo qua 2, hong 12) - KHONG DU: 2 ca BO QUA, chua do gi |
| `base-dot-bien-full` | 0 | DOT BIEN: 272/272 dat  (4 khong do duoc tren nen nay) |
| `head-launcher-full` | 1 | 222/234 ca DA CHAY QUA (tong 236, bo qua 2, hong 12) - KHONG DU: 2 ca BO QUA, chua do gi |
| `head-launcher-full-fake` | 1 | 222/234 ca DA CHAY QUA (tong 236, bo qua 2, hong 12) - KHONG DU: 2 ca BO QUA, chua do gi |
| `head-dot-bien-full` | 0 | DOT BIEN: 277/277 dat  (4 khong do duoc tren nen nay) |

Auth absent: head/base có 12/12 ca đỏ, 2/2 ca bỏ qua; tập đỏ và bỏ qua trùng theo tên, 0 ca đỏ mới.

Auth fake: head/base có 12/12 ca đỏ, 2/2 ca bỏ qua; tập đỏ và bỏ qua trùng theo tên, 0 ca đỏ mới.


Không nhận headline --dot-bien là bằng chứng tất cả kill thật: đã quan sát đúng 4 dòng stock nhận kill bằng OSError ở ca credential có control vốn đã đỏ vì Codex home nằm trong repository ancestor của sandbox. Không cấp tín dụng 4 kill này thành TinHieuChotCa. Tập mutation chọn lọc bên trên mới có kiểm type/frame riêng. Full launcher còn fail/skip nên KHÔNG là N/N; không đổi guard credential, xóa .git, sửa fixture hay đi ra ngoài review-data để làm xanh. `full-delta.json` giữ tên từng ca và hai chế độ auth. Bản vá F03 mới vẫn bị bỏ sót bởi suite stock vì suite không bật allexport.

[full-launcher-summary.json](full-launcher-summary.json), [full-delta.json](full-delta.json), [stock-mutation-delta.json](stock-mutation-delta.json).

**Finding đang mở — biểu hiện mới cùng lớp F03 [P2] `chooser-path-reselects-python`**

Vị trí: `ops/cai_cong_cu.sh:19`, `:20`, `:62`, `:63`, vòng source `:67`. Regression so lượt 4 `c59d479be2132242125d4a8e77356ed676f76d2c` trên cùng fixture; không lập slug mới để xóa lịch sử F03.

Khi Bash bật allexport (`bash -a`, hoặc SHELLOPTS=allexport trong môi trường của lời gọi mới), phép gán dấu ở dòng 63 tự mang export DÙ vừa unset ở dòng 62. Phép đo riêng Bash ghi đúng `declare -x CAI_CONG_CU_PY_CUA=...` sau chuỗi unset/gán. Lượt source cho rg thấy dấu export, dòng 19 xóa nó; lúc này PATH vẫn ban đầu nên rg cài thành công. Nhưng sau rg, PATH chứa Python của venv không có PyYAML. Lượt source tiếp theo cho bash không còn dấu nên chọn/ghim lại Python venv, import yaml hỏng và wrapper thoát 3. Đây đúng lớp mất danh tính interpreter trong một batch của F03; không phải nợ recipe bash prepend lại rg hỏng (đã tách front).

Phản chứng chạy được: `PYTHONDONTWRITEBYTECODE=1 python review-data/allexport_layouts.py`. Script dựng venv thật thiếu PyYAML, initial Python có yaml, rg hỏng đầu PATH, candidate tốt, installer apt/brew là stub không cài mạng; chạy đường --bat-buoc thật với hai recipe nguyên của HEAD. Đủ 12 layout và cả hai thứ tự. **HEAD rg→bash dưới mỗi cách bật allexport: 12/12 rc3/ModuleNotFoundError yaml; normal, đảo thứ tự và wrapper lượt 4 cùng fixture: tất cả rc0/DAT.** Tổng 144 phép đo: 24 lỗi sản phẩm kỳ vọng và 120 controls qua; probe rc0 chỉ nghĩa assertion đo đúng. `reachability.json` còn chứng minh HEAD/E/F cùng lỗi, cài đơn vẫn rc0.

Đây là input ngoài tiến trình hợp lệ, không cần tin hoặc thực thi dữ liệu tấn công, không cần sửa nguồn/biến nội bộ từ một đoạn shell tùy ý. Chặn bootstrap/batch hợp lệ và vi phạm yêu cầu r4 giữ PY của lượt cha, đủ P2; không có bằng chứng vượt đặc quyền để gán P1.

Hướng sửa BẰNG LỜI: đảm bảo dấu do chính lượt cha tạo có thuộc tính không export ngay cả khi tùy chọn shell tự export đang bật; giữ phân biệt marker nội bộ với môi trường kế thừa, không nới lại rào F04. Giữ PY mảng/đối số -3, ghim absolute và quoting. Thêm chiều allexport cờ/môi trường vào hai ca r831 cùng đối chứng đảo thứ tự; phép sửa phải giữ toàn bộ marker matrix. Không cung cấp patch runtime cho sensitive path, không sửa cay-kho/.

Để đóng: cả 12 layout rg→bash dưới hai cách bật allexport phải rc0, cả rg/bash DAT, installer không nhận dấu; F04 scalar/PID phải tiếp tục được loại. Có thể chọn từ chối rõ tùy chọn không hỗ trợ nếu spec được chủ kho đổi, nhưng không tự đổi acceptance để biến rc3 hiện tại thành pass. Không tự mở thêm review call sau lượt cuối chủ kho yêu cầu.

[allexport-summary.json](allexport-summary.json), [allexport-layouts.json](allexport-layouts.json), [allexport-declaration.json](allexport-declaration.json), [reachability.json](reachability.json). Bản D giữ nguyên mọi thứ trừ phép loại dấu export: dưới allexport 2/2 batch DAT nhưng installer thấy PID; xác nhận quan hệ nhân quả, đồng thời chứng minh không thể bỏ rào F04 làm cách vá. [allexport-D-causal-control.json](allexport-D-causal-control.json).

**Toàn vẹn và phần chưa đo**

Nguồn cay-kho: **4395/4395 file/link kể cả .git không đổi hash/mode/đích symlink**; exact HEAD/tree khớp, status gồm ignored/untracked và diff/index sạch. Bản sao head/base/ratchet sạch sau các phép thử và hoàn nguyên mutant. Tệp ignored do gate tạo đã được bảo toàn hash và chuyển ra `gate-generated-artifacts/` trước kiểm sạch cuối. Snapshot chỉ chứng minh hai mốc không có delta, không chứng minh chưa từng ghi rồi hoàn nguyên. Sandbox là workspace-write; read-only với source là kỷ luật kiểm chứng, không phải mount read-only. [integrity.json](integrity.json), [source-before.json](source-before.json), [source-after.json](source-after.json), [gate-generated-artifacts.json](gate-generated-artifacts.json).

KHÔNG ĐO ĐƯỢC: Windows Git Bash/MSYS/py.exe native, macOS native; CI ci.yml/launcher-windows.yml exact HEAD chưa push; lease/receipt/assurance live, model variant/effort. Không có environment_status trong tool catalog; không suy readiness credential/mạng. 470 mutant cong_cu không chạy ở chế độ manh; chỉ xác nhận gate 56/56 và tự kiểm runner. Recipe macOS và fixture Windows POSIX không thay native evidence. Không có P3 mới để chủ kho quyết; nợ bash recipe và sandbox được ghi rõ ở trên, không vá ngoài scope.

VERDICT được ghi tăng dần trong quá trình đo; bản trước khi tổng hợp ở [VERDICT-progress.md](VERDICT-progress.md). Băm các hiện vật và log được ghi sau khi writer/gate kết thúc ở [artifact-manifest.json](artifact-manifest.json).

**Quyết định: changes_requested**, vì F03 P2 còn mở trên exact SHA dòng 2; F01/F02 đóng, F04 đã vá biểu hiện scalar/PID nhưng sinh regression F03 dưới allexport. Đây là verdict nội dung offline, không ủy quyền push/merge/land hay thay check run/receipt.
