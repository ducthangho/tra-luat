verdict: changes_requested
reviewed_sha: 4511b1eb6168904da117791cea178aa0c80e0e47
base_sha: f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7
Reviewed commit: 4511b1eb6168904da117791cea178aa0c80e0e47
reviewed_tree: fa6c7ab806e485d41a5c3be73d34e73ef85ee5d3
packet: wp899-r4-g5
review_class: sensitive
role: reviewer
provider: openai_codex
model_family: openai
model: gpt-6.1-sol
effort: xhigh
model_evidence: CLI-published
execution_surface: codex_cli
transport: machine
session_id: 01a17b0c-b9b3-7dd2-a7c3-00d6491b58a4
independent_from_executor_session: true
github_submitter_identity: null
review_axes: [spec, standards_security]
assurance: review_deferred

**P0=0, P1=0, P2=1 mới; hai lớp P3 kế thừa.** F13 làm reader Git ném trên commit hợp lệ có message không phải UTF-8. Bộ mặc định xanh nhưng không kiểm đường này bằng Git thật: các ca Checkout tiêm `GIT.get`, c34 kiểm `git_blob`. F13 là lỗi sản phẩm trên đầu vào hợp lệ, không phải yêu cầu thêm mutant ngoài tập đóng.

## Phạm vi và preflight

Đọc toàn bộ prompt, CONTEXT, protocol, CLAUDE, kế hoạch đa provider và skill cross-review. Review đúng diff `f9f4a8d6da2d351fbcf5203256aba4e1bbf027b7..4511b1eb6168904da117791cea178aa0c80e0e47`: `.claude/dev/ci_dang_ky_test.py` +1, `ops/ci_provenance.py` +444, `ops/ci_provenance_test.py` +1600; tổng **3 tệp, +2045/-0**. Dòng MOI mới đúng một mục, cùng mẫu với land_evidence_nguon_test. `git diff --check` rc0. Detached HEAD, origin `https://github.com/ducthangho/tra-luat.git`.

Spec r4 được giao và blob `f28cde363d8a011b2fc6e2265caaee224391f24d:ops/specs/wp899-r4.md` cùng SHA-256 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45`. Đã đọc trọn r2/r3 tại OID ấy; băm lần lượt `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` và `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`, khớp chuỗi dẫn. [Nguồn/băm](spec-provenance.json).

Lease g5 tại `237e71ac850ddbe56e11d5a28f4a7036f7cf4264:ops/leases/wp899-r4-g5-claude.yaml` ghi ba tệp và quyết định nâng trần lên **2050** (#899 issuecomment-6400403263), nên 2045 không vượt trần đã ghi. Đây là hồ sơ lịch sử, đã rút hạn; authority của lượt read-only sau merge là prompt hiện hành #955, không phải quyền writer của lease. Base lease `ba222ffd1615f0d74b59985b9612f725211b62f5` được phân biệt với base diff PR ở trên. Freshness GitHub, tổng budget đã tiêu và receipt owner LIVE **KHÔNG ĐO ĐƯỢC**.

## BẢNG LỚP

Ba lớp mở, bốn biểu hiện: F13 có hai (commit ISO-8859-1 và blob không UTF-8), D02 một, F10/D05 một. Một lớp mới P2, hai lớp kế thừa P3. Ngưỡng V2: còn P2 thì không approve.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT |
|---|---|---|---|---|
| F13 `git-commit-body-encoding-lam-hong-metadata` | **P2 mới** | `ops/ci_provenance.py:138` đọc toàn commit với `text=True`; lỗi decode nổi qua `:425` | `python -B .review/git_commit_encoding.py`: Git thật xác nhận hai commit cùng tree/parents; UTF-8 child rc0, ISO-8859-1 child **rc1/UnicodeDecodeError**, không sinh provenance. Ca đích riêng rc0/`CA: 1/1 dat` đối chứng và rc3/`DO:r955_git_commit_message_encoding:` phản chứng. Blob không UTF-8 cũng ném thay vì None. | **Ở đâu:** git_cuc_bo và test seam Git thật, vì reader này tạo metadata Checkout M3. **Cách:** thu bytes, chỉ giải mã/đọc các trường tree/parent cần dùng; tách body và metadata không liên quan. Đừng chỉ nuốt UnicodeDecodeError thành None: object hợp lệ vẫn đo được tree/parents. **Khoá:** commit UTF-8 và ISO-8859-1 cùng tree/parents, blob không UTF-8, missing object; mutant đưa reader về giải mã toàn stdout bằng text=True phải chết đúng ca. **Rủi ro:** fallback decode thay ký tự có thể che metadata lỗi; giữ kiểm OID và phân biệt object không đọc được. |
| D02 `uses-nhieu-dong` | P3 kế thừa | `ops/ci_provenance.py:174` | `D02_uses_multiline` trong supplemental-results.json: tên implicit lấy dòng đầu của uses nhiều dòng | Giữ nợ theo quyết định chủ kho được ghi trong prompt lượt 11, owner ducthangho. Nếu mở successor, dùng fixture runner thật phân biệt toàn giá trị uses với dòng đầu. Rủi ro: đổi nhầm luật tên run; không vá trong lượt review. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop`, biểu hiện D05 `try-boundary-chua-duoc-catalogue-khoa` | P3 kế thừa | `ops/ci_provenance.py:158`, `ops/ci_provenance_test.py:1044` | [D05-results.json](D05-results.json): HEAD để sentinel sau parse nổi lên; mutant mở rộng try nuốt sentinel nhưng **vẫn qua c52, rc0** | Đề xuất giữ nợ test, owner ducthangho, xử lý successor. Thêm fault injection sau parse và mutant mở rộng try; chốt phải đòi sentinel nổi lên. Rủi ro: mock không được khôi phục làm nhiễm ca khác. HEAD chỉ bọc một lời gọi safe_load, không có lỗi sản phẩm ở ranh giới này. |

### F13: bằng chứng và bán kính

[Script tái hiện](git_commit_encoding.py), [ca chốt](encoding_criterion.py), [raw kết quả](git-commit-encoding-results.json), [quét non-commit](git-noncommit-encoding-results.json). Dùng lại byte không UTF-8 có sẵn ở c34; mọi Git object mới ở thư mục tạm dưới `.review/`. Không sửa checkout, không cần thay workflow/script/action tại SHA để làm phát sinh lỗi: chỉ encoding message của commit là đủ.

Git `cat-file -t` xác nhận object là commit; `git show --no-patch --format=%T%n%P` đọc đúng cùng tree/parents; `git log --encoding=UTF-8` chuyển message ISO-8859-1 thành UTF-8 được. Công cụ lại decode toàn stdout của cat-file bằng UTF-8 trước khi tách header. Qua main thật với REST giả giữ trạng thái và reader Git thật, bản UTF-8 sinh provenance/rc0; bản ISO-8859-1 chỉ in `NOT_MEASURED: 4`/`PROVENANCE: khong_sinh` rồi ném/rc1. Lỗi hẹp M3, không có bằng chứng pass giả hay lộ credential.

Đã quét các đường cùng lớp: `git_blob` bắt lỗi UTF-8 và trả None (c34); log decode với replace; JSON lỗi decode thuộc ValueError được ánh xạ LoiRest. Chưa thấy biểu hiện khác ngoài reader Git metadata. Không đề nghị patch sản phẩm trong vai Reviewer.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Báo cáo lượt 11 là lời khai để định hướng. `git diff --exit-code 1f731c7bfc99c8fca3cba74d4cd8bbf6a14db986 HEAD -- ops/ci_provenance.py ops/ci_provenance_test.py` rc0 xác nhận hai nguồn giữ nguyên; kết luận ở đây dựa trên phép đo mới.

| lớp cũ | kết quả lượt này | bằng chứng tự đo |
|---|---|---|
| F01 thiếu định danh | Không tái hiện biểu hiện cũ | c22; thiếu/sai Run, job, artifact không được nâng thành pass của mốc tương ứng. |
| F02 định danh kịch bản/bước | Không tái hiện biểu hiện cũ | c23–43 của suite; 18 mutant riêng phủ ghép tên/số/giờ/job, composite, nhóm lồng, đúng khối YAML và chặn đúng job. |
| F03 phân trang; F04 REST stateful | Không tái hiện biểu hiện cũ | c20 và mutant bộ mặc định: trang thiếu/lặp/total đổi, URL đúng run/attempt. |
| F05 dòng đếm; F06 redirect | Không tái hiện biểu hiện cũ | c01/c18/c19/c24; mutant riêng mất dòng đếm, sai mã REST và Request mang token bị giết đúng ca. F13 vẫn giữ dòng đếm trước khi ném, nên không phải tái mở F05. |
| F07 A10 checkout skipped | LIVE KHÔNG ĐO ĐƯỢC | Không suy A10 từ fixture; c05/c11 giữ thiếu SHA/skipped. |
| F08 reader workflow Git | Không tái hiện biểu hiện cũ | c34 của suite; kiểm reader blob UTF-8, sai path, không UTF-8. F13 thuộc reader metadata riêng, đã tái hiện lỗi mới. |
| F09 thời gian; F11 môi trường | Không tái hiện biểu hiện cũ | c38/c42 cùng mutant riêng bỏ kiểm giờ/GITHUB_ENV; suite kiểm GITHUB_PATH. |
| F10; D02/D05 | Giữ nợ, không gọi là đã vá | D02 và D05 đo như bảng lớp. Không chạy lại toàn tập đóng 1009 mã trong lượt này; không nhận con số cũ làm kết quả mới. |
| F12 parse YAML; D03/D04 | Giữ bản vá trong phạm vi đã đo | c51/c52; tiêm OverflowError, LookupError, TypeError, RuntimeError, OSError tại safe_load đều về None; AST try chỉ có một assignment. Mutant trở về tuple cũ chết đúng c52. |

M3 r2 chủ ý cho phép lưu SHA khi parents/tree chưa đo được nếu object thiếu; đã đối chiếu phép thử git={} với điều khoản đó, không báo nhầm thành P0. Tương tự, không suy rc lệnh từ conclusion của bước; r2 đã khai giới hạn continue-on-error.

## Phép đo độc lập

Runtime Linux, Python 3.13.17, PyYAML 6.0.3, Git 2.43.0, Ruff 0.15.15, Codex CLI 0.164.0; sandbox workspace-write, approval never, mạng bị tắt. Bytecode tắt bằng `-B` và `PYTHONDONTWRITEBYTECODE=1`; TMPDIR trong `.review/tmp`.

| command / phạm vi | rc thật | trạng thái và bằng chứng |
|---|---|---|
| `python -B ops/ci_provenance_test.py` | 0 | **passed**: 52/52 ca, 292/292 mutant giết đúng lý do, tự kiểm 2 mutant DAT, TONG DAT; 1849.7s. [stdout](baseline.stdout.txt), [receipt](baseline.json). |
| `python -B ops/ci_provenance_test.py --mot-ca <tên>`: 20 ca trong supplemental-results.json | 0 từng ca | **passed**, đối chứng riêng cho ghép bước, metadata, lỗi REST, nguyên tử, phân trang, redirect, parser. |
| `python -B .review/mutants.py` | 0 | **passed phép đo**: 18/18 mutant rc3 đúng TinHieuChotCa/đúng ca, không tín dụng giả. [Receipt và source hashes](mutant-results.json). |
| `python -B .review/git_commit_encoding.py` | 0 observer | **failed tính chất F13**: child ISO-8859-1 rc1, ca chốt rc3; UTF-8 child/ca chốt rc0. Observer rc0 chỉ xác nhận đã thu xong phép đo. |
| `python -B -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` | 0 | **passed bare lint**, All checks passed. |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | **passed**, 10 tệp, 0 chỗ chép doctrine. |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | 0 | **passed**, 55 ADR/55 dòng, 1–1. |
| `python -B .claude/dev/ci_dang_ky_test.py` | **1** | Lệnh **failed** vì fixture ký commit cần local signing service, socket operation not permitted. Trước lỗi có 27/27 đăng ký, launcher 4/4, Ruff CI contract 3/3. Toàn gate **not_measured**, không tính đạt. [stderr](registry.stderr.txt), [nguyên nhân Git thật](supplemental-results.json). |
| Kiểm riêng `kiem(root, registry)` và regex MOI | 0 | **passed phạm vi hẹp**: 27/27, gỡ mục đích ra 27/26 + lỗi đích danh; mẫu dương True, 7 đối chứng thiếu/sai/0 đều False. [Kết quả](registry-targeted.json). |
| `ci_dang_ky_test.py --chay` (A9 đầy đủ); full release/legacy gate | — | **not_run**: preflight fixture registry chưa đủ năng lực ký commit. Không tắt signing, đổi quyền/trust hay gọi mạng để làm xanh. |
| A10 LIVE / required CI exact SHA / native Windows | — | **not_measured / KHÔNG ĐO ĐƯỢC** trong lượt offline này. Không nhận skipped/missing thành pass. |

A1–A8 và A14–A27 có ca/đột biến offline tương ứng trong suite. A11 lint/doctrine/ADR/write set/trần đã đo. A9 đầy đủ chưa đo được. A10 LIVE chưa đo. A12 lịch sử đẩy/connector và A13 receipt sau terminal thuộc phần chưa xác minh, không được coi là hoàn tất.

### Danh sách mutant và hạng

Danh sách **đủ 292 tên/ca/hạng GIET** của bộ mặc định: [MUTANT_CATALOGUE.md](MUTANT_CATALOGUE.md). Bảng dưới là 18 mục được chạy thêm và giữ raw stdout/stderr đầy đủ; “hạng” là mức hậu quả nếu chốt bị tháo, không phải finding trên HEAD. Không cộng thành 310 mutant duy nhất.

| mutant | hạng nếu chốt bị tháo | ca đích | kết quả |
|---|---|---|---|
| `A7_bo_dong_dem` | P1 | `c18_dem_not_measured` | GIET, rc3 đúng TinHieuChotCa |
| `A7_gop_rest_vao_12` | P1 | `c19_rest_loi` | GIET, rc3 đúng TinHieuChotCa |
| `A26_bo_GITHUB_ENV` | P0 | `c42_github_env_cung_job` | GIET, rc3 đúng TinHieuChotCa |
| `A26_GITHUB_ENV_toan_workflow` | P1 | `c42_github_env_cung_job` | GIET, rc3 đúng TinHieuChotCa |
| `L10_bat_lai_tuple_luot9` | P2 | `c52_tap_dong` | GIET, rc3 đúng TinHieuChotCa |
| `A19_moi_ung_vien_trung_chu` | P1 | `c33_trung_chu_khac_job` | GIET, rc3 đúng TinHieuChotCa |
| `A19_chan_doc_job_khac` | P0 | `c33_trung_chu_khac_job` | GIET, rc3 đúng TinHieuChotCa |
| `A20i_zip_bo_dem_nhom` | P0 | `c36_ghep_lech_so` | GIET, rc3 đúng TinHieuChotCa |
| `A20ii_zip_bo_dem_yaml` | P0 | `c36_ghep_lech_so` | GIET, rc3 đúng TinHieuChotCa |
| `A21_bo_kiem_ten` | P0 | `c37_ghep_lech_ten` | GIET, rc3 đúng TinHieuChotCa |
| `A22_bo_kiem_gio` | P0 | `c38_ghep_lech_gio` | GIET, rc3 đúng TinHieuChotCa |
| `A22_khong_cat_giay` | P1 | `c38_ghep_lech_gio` | GIET, rc3 đúng TinHieuChotCa |
| `A23_lay_khoa_dau` | P0 | `c39_ghep_job` | GIET, rc3 đúng TinHieuChotCa |
| `A24_bo_luat_nhom_long` | P0 | `c40_nhom_long` | GIET, rc3 đúng TinHieuChotCa |
| `A25i_uses_sinh_marker` | P1 | `c41_buoc_uses` | GIET, rc3 đúng TinHieuChotCa |
| `A25ii_zip_bo_dem_nhom` | P0 | `c41_buoc_uses` | GIET, rc3 đúng TinHieuChotCa |
| `A27_khoi_bang_buoc_khac` | P0 | `c43_khoi_khac_buoc` | GIET, rc3 đúng TinHieuChotCa |
| `F06_redirect_mang_token` | P0 | `c24_goi_that_loi_va_chuyen_huong` | GIET, rc3 đúng TinHieuChotCa |

Hai tự kiểm phân hạng: AttributeError qua except đổi sang AssertionError → TIN_DUNG_GIA; chỉ thêm comment → SONG_SOT, đều đúng mong đợi. Kiểm riêng rc0, rc4, rc3 sai ca, rc3 đúng ca lần lượt cho SONG_SOT, TIN_DUNG_GIA, TIN_DUNG_GIA, GIET. D05 ngoài tập đóng sống c52 đã được ghi **P3**, không tính là GIET. Ca F13 là phản chứng lỗi HEAD, không được cộng vào số mutant bị giết.

## Giới hạn, identity và read-only

[identity.json](identity.json) trích đúng session_meta.id/cwd/CLI version/model_provider và turn_context.model/effort của rollout phiên này: `gpt-6.1-sol`, `xhigh`. Đây là **model do CLI công bố**; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Executor Claude theo assignment/lease; chưa có phép đo runtime độc lập của Executor trong lượt này. Raw rollout còn được ghi; hash/size cuối, terminal/launcher rc và delivery receipt phải được consumer thu sau khi process kết thúc. Không tự tạo cross_approved hoặc authority land từ verdict này.

Snapshot đầu/cuối đối chiếu SHA/tree, tracked/index diff, untracked/ignored status và bytes/hash **6026 tệp** ngoài `.review/` và `.codex/`: không có delta quan sát được. `.codex/` chỉ đọc metadata identity cần thiết, không snapshot nội dung secret/config; `.git/` được kiểm qua Git facts, không snapshot mọi byte nội bộ. Repo nguồn ngoài checkout không thuộc quan sát. Hai mốc sạch không chứng minh chưa từng ghi rồi hoàn nguyên.

Mọi source mutant/phản chứng và đầu ra do reviewer tạo nằm trong `.review/`, ngoại lệ scratch user đã cho phép. Không sửa ba tệp sản phẩm, branch hay index; `git status --short` cuối rỗng. Không gọi subagent, đăng GitHub, push, merge, land hoặc deploy. Không dùng lời khai A10 hay kết luận lượt 11 thay phép đo độc lập.
