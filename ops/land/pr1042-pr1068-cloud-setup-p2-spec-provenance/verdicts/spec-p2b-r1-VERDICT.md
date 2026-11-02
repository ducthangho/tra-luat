verdict: request_changes
reviewed_sha: 780b7ecc7f64e76f6fa6f64c7bce5a5f530880e3
reviewed_tree: ad751ea6429f162364a5675e54db834fc5aec082

Reviewer: `openai_codex`; provider: OpenAI; execution surface: Codex với shell cục bộ trong sandbox; transport: API. Review đặc tả độc lập, lượt 1/8 theo prompt. Không suy danh tính model từ tài khoản Git. Không dùng context Executor, không sửa cây review hoặc đặc tả đóng băng.

## (i) DANH TÍNH

**Đúng cả HEAD, tree và SHA-256 của HAI tệp.** Lệnh Git này là phép đo đầu tiên trên `cay-kho/`, ngay sau khi tạo `VERDICT.md` với `verdict: pending`:

```console
$ git -C cay-kho rev-parse HEAD HEAD^{tree}
780b7ecc7f64e76f6fa6f64c7bce5a5f530880e3
ad751ea6429f162364a5675e54db834fc5aec082
$ sha256sum SPEC.md cay-kho/ops/specs/cloud-setup-p2b-wire-r1.md
67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81  SPEC.md
67b448acc825fdd29f118c3b9082583773b4ad218a7c83ab4db496daa8f26d81  cay-kho/ops/specs/cloud-setup-p2b-wire-r1.md
```

Cả hai lệnh rc=0. Đo thêm:

```console
$ git -C cay-kho merge-base 01ff65035c8b0833fa521b93239931772c14dffd 780b7ecc7f64e76f6fa6f64c7bce5a5f530880e3
01ff65035c8b0833fa521b93239931772c14dffd
$ git -C cay-kho diff --numstat 01ff65035c8b0833fa521b93239931772c14dffd 780b7ecc7f64e76f6fa6f64c7bce5a5f530880e3
248	0	ops/specs/cloud-setup-p2b-wire-r1.md
$ git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored
$ git -C cay-kho diff --exit-code
$ git -C cay-kho diff --cached --exit-code
```

Các lệnh trên rc=0; ba lệnh cuối stdout/stderr rỗng. `diff.patch` bằng byte với `git diff` theo hai OID được giao: 32739 byte, SHA-256 `b61698e17c2e69ad6fcf6b058d0bf989a3e56a7872ea09bf6dae20129cf8164c`.

Đầu và cuối review cùng HEAD/tree, status kể cả ignored đều sạch. Cuối review, 22 tệp nguồn/tài liệu được chọn đối chiếu trực tiếp với `git show HEAD:<path>` đều bằng byte; hai SHA-256 đặc tả vẫn đúng. Bằng chứng: [repo-summary](measurements/repo-summary.txt), [final-state](measurements/final-state.txt).

Giới hạn read-only: sandbox thực tế là `workspace-write`, không có cơ chế cấm ghi riêng cho `cay-kho/`; reviewer giữ cây chỉ đọc và đặt script, log, bản sao tạm ngoài cây. Snapshot chứng minh không có delta quan sát ở hai mốc, không chứng minh toàn bộ lịch sử không có ghi rồi hoàn nguyên. Không có lệnh sửa/hoàn nguyên cây review trong phiên này.

Không dùng mạng, Drive/NLM/webapp; không tải hoặc chạy nhị phân `agy`; không đọc/ghi credential thật. Các phép đo hành vi dùng AST của hàm nguồn với dependency giả trong RAM, hoặc tiến trình Python vô hại. Trước các phép đo có entrypoint giả/hàm `tl`, đã chạy `unset TL_MASTER_KEY TL_AGENT_CREDS_FILEID CLAUDE_CODE_OAUTH_TOKEN GEMINI_API_KEY`. Không gọi CLI `tl` thật.

## (ii) ĐO LẠI KHẲNG ĐỊNH CỦA ĐẶC TẢ

Dòng dưới đây là dòng của `SPEC.md`, bằng byte với đặc tả trong cây. Lệnh tái lập chính: `python3 -B probe_repo.py`; command/output/rc lưu trong [repo-summary](measurements/repo-summary.txt). Các phép đo riêng có liên kết ở từng hàng.

| Khẳng định (mục/dòng) | Đặc tả khai | Đo được (lệnh) | Khớp? |
|---|---|---|---|
| Dòng 9, kế hoạch thi công | Không có dòng kế hoạch packet trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` | `probe_repo.py`: tìm riêng `1039`, `CLOUD-SETUP-P2B`, `cloud-setup` trên tệp 620 dòng: đều 0 | Có, trong phạm vi định danh packet |
| Dòng 10–11, sensitive | Chạm credential và hook SessionStart | Nguồn `cmd_bootstrap`, `_bootstrap_agent_creds`, hook và write_set đúng các ranh giới đó | Có |
| Dòng 12, base | `01ff6503`, merge PR #1042 | `git show -s --format=... 01ff6503`: full OID đúng, subject merge #1042; merge-base đúng | Có |
| Dòng 14, P2a đã merge | PR #1063, `69dcfee`, 04:28Z 31-10 | `git show -s` cho `69dcfee9274aae12ca27dfecc22a980e560cc3bc`: merge #1063, `2026-10-31T11:28:26+07:00` = 04:28:26Z; `merge-base --is-ancestor ... HEAD` rc=0. [git-times](measurements/git-times.txt) | Có |
| Dòng 15, hồ sơ land | `ops/land/pr1063-*` chưa có | `git ls-tree -r --name-only HEAD ops/land`, lọc đúng prefix: `[]` | Có; không tự suy P2a đã landed |
| Dòng 15–16, lease còn hạn | Lease P2a vẫn còn hạn; không giao write_set vì chỉ giữ `scripts/tl_gws.py` | Không có nguồn lease hiện hành/fresh trong bundle để chứng thực hạn. Đếm write_set P2b: 0 đường dẫn `scripts/tl_gws.py` | Phần không giao tệp khớp; trạng thái lease chưa đo, không gọi mạng |
| Dòng 17–22, trần riêng | 8 tệp / 600 dòng thêm, ADR-0052 ghim OID | Write_set có đúng 8 đường dẫn riêng biệt; đúng 1 dòng `tran_loi_goi_codex: ADR-0052@...`. ADR-0052 định nghĩa trần 8; ADR-0053 định nghĩa 6/450 trước ngoại lệ riêng | Khớp nội dung local; lời duyệt ngoài kho không được tái chứng thực offline |
| Dòng 24–25, OID ADR | Cha thứ nhất chưa có hai ADR; commit land có cả hai | `git ls-tree 8ab1007^1`: 0 tệp ADR-0052/0053; `git ls-tree 8ab1007`: đúng 2 tệp; subject merge #791 | Có đối với phép đo đã khai. Ref mặc định vừa fetch không có trong bundle, không tuyên bố đủ toàn bộ gate hiệu lực ADR |
| Dòng 29–30, bootstrap status | Dòng `[bootstrap] agent_creds: ...` ở 1756 | AST: `cmd_bootstrap` 1645–1762; dòng 1756 là câu print khai báo | Có |
| Dòng 30–31, agent exec | Hàm ở 1260, Gemini chỉ đặt trong môi trường con | AST 1260–1309; nguồn sao môi trường rồi đặt bản sao cho subprocess. [child-env](measurements/child-env.txt): con nhận sentinel giả, môi trường cha giả không đổi, log hàm không chứa sentinel | Có; đã đo với Python con, không đo `agy` thật |
| Dòng 31, fileId | Hằng thật ở 1089 | AST: `AGENT_CREDS_FILEID` ở 1089, chuỗi không rỗng dài 33 ký tự | Có với giá trị được commit; không xác minh tài nguyên mạng |
| Dòng 32–33, hook | 642 dòng, chưa nối bootstrap | `probe_repo.py`: 642 dòng; số lời/chuỗi ` bootstrap`, `cloud_agent_creds.py` đều 0 | Có |
| Dòng 32–33, setup | 105 dòng, chưa nối bootstrap | `probe_repo.py`: 105 dòng; `bootstrap`, `cloud_agent_creds.py` đều 0 | Có |
| Dòng 33–34, chưa cài/chưa đo `agy` ở mọi phiên cloud | Quan sát phiên soạn và lịch sử phiên cloud | Bundle không chứa trạng thái mọi container/phiên; không gọi dịch vụ để xác minh | Chưa đo được ngoại kho; không nâng thành finding |
| Dòng 34–36, bootstrap thoát sớm | Thiếu khoá/tải lỗi rc=2; giải mã lỗi rc=3, chưa có status agent | [contracts-verified](measurements/contracts-verified.txt): chạy đúng AST `cmd_bootstrap`, dependency giả: `missing_key rc=2`, `fetch_failed rc=2`, `decrypt_failed rc=3`; cả ba `agent_lines=0` | Có |
| Dòng 43–50, write_set | 8 đường dẫn; helper/test mới | Sáu đường dẫn đã có; `ops/cloud_agent_creds.py` và `ops/cloud_agent_creds_test.py` chưa tồn tại; không có wildcard | Có. Đây là review spec, sự vắng mã mới không phải finding |
| Dòng 50, 157, manifest | RUNBOOK thuộc manifest nên cần tái sinh | Parse JSON: `references/RUNBOOK.md`, size 86217, SHA-256 `6bb3c7650aee1189aad1b143b42b4cf9f248e8892587accd492e4837d3d6bbfa`, bằng tệp thật | Có |
| Dòng 57–61, Codex secret / HOME / internet | Giới hạn tài liệu/quan sát, việc secret bị gỡ chưa đo | `ops/codex_cloud_setup.sh:43–54` có đúng chú thích HOME chỉ đọc và giải pháp LOCALAPPDATA đã dẫn. Secret/internet của dịch vụ không đo offline | Khớp nguồn local; giới hạn dịch vụ giữ nguyên chưa đo |
| Dòng 65, sổ công cụ CI | `ops/cong_cu.yaml` là sổ CI, chưa có `agy` | Đọc sổ và workflow CI: sổ dùng cho tool probe/install CI; chưa có mục công cụ `agy` | Có đối với kho tại head |
| Dòng 66, installer chính thức | Installer latest, không có cờ ghim; `agy install` sửa shell | Không có installer/nhị phân gốc để kiểm tại bundle, và bị cấm tải/chạy | Chưa tái chứng thực; không tuyên bố đã đo |
| Dòng 68–69, PATH | Codex setup có `ghi_bashrc` thêm local bin | Nguồn dòng 52–55 và 71: export `$HOME/.local/bin:$PATH` | Có. PATH của phiên Claude soạn không có trong bundle |
| Dòng 71, 248, local hook | Hook thoát khi `CLAUDE_CODE_REMOTE` khác true | Nguồn hook 54–60: nhánh kiểm và `exit 0` trước vùng sẽ chèn | Có với shell hook; không tuyên bố toàn bộ bridge không chạy trên local |
| Dòng 75–99, hằng agy | 6 nền, version 1.4.12, URL/băm/chuỗi tĩnh đã đo ở phiên soạn | Parse bảng: đúng 6 khoá, 6 URL ghim đường dẫn 1.4.12, 6 sha512 gồm 128 chữ số hex. Không có bytes manifest/tarball/binary để đo lại version, thành viên, size hay chuỗi tĩnh | Khớp cấu trúc nội bộ; nguồn ngoài kho chưa đo, không dùng mạng |
| Dòng 138, vị trí hook | Header phụ thuộc dòng 237; lời gọi policy dòng 585 | Đúng 237/585 trên cả base/head. **Pip thực ở 501, khối phụ thuộc kết thúc 510**; chỗ nhắc policy đầu tiên là comment dòng 575 | Số khai khớp; khác biệt header/end gây F01 |
| Dòng 143–144, main setup | Gọi sau pip và trước bước bằng chứng dương | `main` mở ở 67; pip requirements dòng 74; marker bước 5 ở 94 | Có, có vùng chèn hợp lệ trong write_set |
| Dòng 148–151, mẫu test | Có sẵn mẫu đòi cả hai tỷ số bằng nhau và lớn hơn 0 | `MOI` của registry có mẫu `doc_receipt_thu_hoi_test.py` với backreference và `[1-9]`; probe: tỷ số đủ khớp, lệch mutant và 0/0 không khớp | Có |
| Dòng 152, RUNBOOK | A0.4d ở 180, A0.4e chưa có | `probe_repo.py`: A0.4d đúng dòng 180, A0.4e 0 lần; mục tiếp theo A0.5 ở 219 | Có |
| Dòng 201, độ dài credential lịch sử | FileId 33, token/khoá đã đo trong P2a | FileId commit đo được 33. Không đọc credential thật để xác minh hai độ dài còn lại | Phần công khai khớp; credential thật không đo theo giới hạn prompt |
| Dòng 216–218, baseline vế âm | H1/E1/R1 và hai năng lực mới chưa có; G3 xanh | Hook/setup/RUNBOOK bằng byte base; helper calls/A0.4e đều 0; capability line cũ chưa có hai tên. G3 base/head: rc=0, 10 tệp, 0 chỗ chép doctrine | Có; [doctrine-base](measurements/doctrine-base.txt), [doctrine-head](measurements/doctrine-head.txt) |
| Dòng 222–224, kích thước | Khoảng 550 dòng là ước tính chưa đo | Các số 150+280+30+60+20+8+2+1 = 551, hợp với “khoảng 550”; chưa có implementation để đo numstat | Đúng cách khai ước tính, không coi là kết quả đã chạy |
| Dòng 224, ba commit cũ | +81/+221, +17/+26, +16/+52 | `git show --numstat` trên đúng ba commit và đúng hai tệp trả lần lượt 81/221, 17/26, 16/52 dòng thêm | Có |
| Dòng 225–226, budget | ADR-0052 trần 8, hết trần chưa approve thì rescue | Đọc ADR-0052: đúng trần và điều kiện checkpoint; bộ đếm lời gọi của phiên soạn không suy từ Git | Khớp luật được trích |
| Dòng 231–235, lịch sử P1/P2a | 8/8, chuỗi finding và vượt trần của phiên trước | Không có authority/readback hiện hành đủ để kiểm toàn bộ lịch sử vận hành trong review offline này | Chưa tái chứng thực; không lấy làm bằng chứng lỗi của spec này |
| Dòng 237–248, các giới hạn đã khai | Enum, auto-update env, CLAUDE_ENV_FILE, secret Codex, thời gian bootstrap, 5 tarball, Windows chưa đo | Không phép đo nào của review này xác nhận các hành vi LIVE đó; nguồn bridge có truyền env nhưng không chứng minh nền tảng đã đặt biến | Giữ nguyên `chua_do_duoc`, **không tính finding** |

**Write_set:** chưa thấy tệp cơ học bắt buộc bị bỏ sót hoặc tệp ghi thừa. Helper/test ở `ops/` và hook/registry ở `.claude/` đều thuộc các thư mục loại khỏi release trong `scripts/tl_core/release.py:394–400`; chỉ RUNBOOK làm thay đổi nội dung gói, nên đã đưa manifest vào write_set là phù hợp. Không có cơ sở đo để kết luận 600 dòng không khả thi trước khi có implementation.

**Hai kết quả đã cân nhắc nhưng không tính finding:**

- A3: chạy Python với script bị xoá thực tế trả rc=2, không làm `subprocess.run` tự ném OSError. Probe cũng xác nhận `stat` riêng trên script bị xoá ném `FileNotFoundError`. Executor có thể thêm preflight trong nhánh chạy để đáp ứng kết quả A3; không có lệnh cấm preflight. Vì vậy đây không phải tiêu chí bất khả thi. Khi test nhánh OSError của chính thao tác spawn, cần đồ giả ném lỗi đó, tránh tự suy từ việc xoá script. [Phép đo](measurements/contracts-verified.txt).
- Xoay khoá ở mục tiêu 10: hàm hiện có cập nhật agent bundle mặc định bằng cách giải mã bản cũ với master hiện tại. AST + RAM giả đo được: master cũ/update rc=0; master mới/update rc=3 và 0 upload; master mới/`--new` rc=0 và tạo ID mới. RUNBOOK mới phải giải thích đường tạo lại và cập nhật ID/nguồn tương ứng, hoặc quy trình di chuyển phù hợp; đặc tả không cấm giải thích các bước/tuỳ chọn đó. Chưa có RUNBOOK mới để kết luận nó hướng dẫn sai. Không chạy thao tác xoay khoá thật. [Phép đo](measurements/contracts-verified.txt).

## (ii) TIÊU CHÍ NGHIỆM THU

Đã đọc **41 hàng tiêu chí**. “Đo được” dưới đây là khả năng thiết kế phép đo/đột biến, **không phải** lời khai implementation đã pass. Helper/test mới chưa có ở head; A–F/H/R/J/K/G1 của sản phẩm tương lai không được báo `passed`. Các đồ giả tải `cai-agy` phải giữ mọi I/O trong sandbox, không tải `agy` thật. Đối với cơ chế vượt guard/tarball độc, chỉ mô tả bằng lời theo prompt.

| Tiêu chí | Đo được không / giới hạn | Đột biến làm đổi màu |
|---|---|---|
| A1 | Có: hai ca vắng/rỗng tách riêng, đo stdout, rc và nhật ký 0 lần | Gọi bootstrap dù không có khoá |
| A2 | Có: đếm đúng 1 status, loại dòng nguồn và giữ chi tiết | Bỏ lọc status nguồn làm thành 2 dòng |
| A3 | Có với fixture/phân loại lỗi tương ứng; xoá script tự nó trả Python rc=2, cần preflight nếu muốn phân loại “không chạy được” | Bỏ status cho 0 dòng; bỏ kiểm tập trạng thái |
| A4 | Đo được thời hạn, status và PID cha; **chưa đo yêu cầu chết cả nhóm**: F02 | Bỏ kill hoặc bỏ timeout làm ca hiện tại đỏ; mutant chỉ giết cha cần ca có con mới đỏ |
| A5 | Có: đo riêng 4 giá trị quy định | Chấp nhận 0 thay vì về mặc định |
| A6 | Có: log argv đầy đủ và interpreter từ script giả | Bỏ no-nlm hoặc thêm require-agent-creds |
| A7 | Có: sentinel giả trong dòng thường/status, kiểm cả hai kênh | Bỏ redaction |
| A8 | Có: bảng rc giả và ca cú pháp tách riêng | Trả rc của bootstrap |
| B1 | Có: tải giả đếm 1, so bytes và mode | Không ghi executable |
| B2 | Có: hai fixture absent/existing, so bytes trước/sau | Bỏ so sha512 |
| B3 | Có đối với bản có sẵn và 0 tải; phép so version chứa chuỗi chưa chứng minh pin: F03 | Luôn tải; cần thêm mutant nới so version khi sửa F03 |
| B4 | Có với version lệch và probe rc=1 | Chỉ kiểm file tồn tại |
| B5 | Có: nền giả ngoài bảng, 0 lần tải | Tự fallback sang nền được hỗ trợ |
| B6 | Có về mặt thiết kế; review này không tạo archive/chuỗi tấn công. Ca phải kiểm không có ghi ra ngoài vùng cho phép và không có agy | Thay xác thực thành giải nén toàn bộ archive; chỉ mô tả cơ chế |
| B7 | Có: lời gọi executable giả được ghi nhật ký | Thêm lời gọi install |
| B8 | Có: so từng cặp bảng **bản thật** với dữ liệu độc lập từ spec; không dùng bảng đã mock | Đổi một chữ số băm |
| B9 | Có: 4 vế giả độc lập của hàm chọn nền | Bỏ nhánh musl |
| C1 | Có: object có khoá khác và fixture chưa có tệp | Ghi đè mất khoá khác |
| C2 | Có: so sha256/bytes với hai loại dữ liệu lỗi | Ghi đè khi parse lỗi |
| C3 | Có: chỉ dùng sentinel giả | Ghi API key môi trường vào settings |
| D1 | Có: chạy hai lần, đếm dòng env và giữ dòng cũ | Nối không khử trùng |
| D2 | Có: fixture cô lập phần env-file hoặc đã chuẩn bị agy/settings; không đọc thành cấm cả các tác dụng phụ hợp lệ B/C | Cố ghi env-file khi biến vắng; đột biến D1 đã khoá nhánh ghi chung |
| H1 | **Sai cận dưới cho mục tiêu 5:** sau header không bằng sau khối phụ thuộc; F01 | Đột biến đã nêu “dời sau doctor” làm đỏ, nhưng đặt ngay sau header vẫn lọt điều kiện thứ tự |
| H2 | Có: trích khối chính tệp, script giả rc=3, shell strict | Bỏ cơ chế giữ rc làm bash thất bại |
| H3 | Có: so tập năng lực với bản base bằng OID | Xoá một tên năng lực cũ |
| E1 | Có: xác định thân main và vị trí sau pip, đếm riêng cai-agy; khi review còn kiểm cận trước bước 5 từ mục tiêu 6 | Dời lời gọi lên trước pip |
| E2 | Có: chạy chính dòng trích dưới shell strict | Bỏ fallback rc |
| F1 | Có: cần rc + mẫu có hai tỷ số bằng nhau và >0; mẫu sẵn có đã được xác minh | Để một mutant sống; xoá dòng đăng ký |
| F2 | Có: kiểm bằng lớp riêng/tên ca, không dựa chuỗi thông báo | Chấp nhận lỗi AttributeError đã bọc, hoặc assertion ca khác |
| F3 | Có: so count với baseline; AST danh sách CA hiện tại có 11 hàm. Nếu thêm đúng hai ca E thì kỳ vọng 13 | Bỏ một ca E khỏi danh sách chạy; E1/E2 đã có mutant |
| R1 | Có đối với sự hiện diện tiêu đề/cụm từ, phạm vi đoạn, độ dài và vế âm base. Nội dung thao tác mục tiêu 10 vẫn phải được reviewer đọc nghĩa | Xoá một trạng thái khỏi bảng |
| R2 | Có: kiểm văn bản, chỉ dùng dữ liệu giả nếu cần; review không đọc credential thật | Chèn dữ liệu giả có hình dạng bị cấm, chỉ mô tả cơ chế |
| J1 | Có trong cây ứng viên có manifest mới; đọc ok/expected/checked. Không chạy CLI tl thật ở review này | Đổi byte RUNBOOK sau sinh manifest |
| G1 | Có bằng selftest từng ca trên Ubuntu cùng config và baseline; **not_run** trong review spec này | Một ca pass base chuyển fail head |
| G2 | Có khi có ref origin/master phù hợp và môi trường không đụng credential thật; ở sandbox ref này vắng, doctor thật **not_run** | Xoá năng lực cũ; H3 cũng đo bằng tập độc lập |
| G3 | **Đã chạy:** base rc=0 và head rc=0, đều quét 10 tệp, 0 chỗ chép doctrine | Thêm nội dung doctrine bị scanner cấm vào adapter; review này không tạo chuỗi vượt guard |
| K1 | Có với implementation, pin/config và delta đúng scope; bare Ruff **not_run** vì chưa có helper/test mới và không sửa sản phẩm | Thêm tên chưa định nghĩa |
| K2 | Có khi có base lease cố định/ref đúng thời điểm. Review offline dùng OID được giao vì thiếu origin/master; không coi diff spec +248 là diff implementation | Vượt trần hoặc thay tệp ngoài write_set |
| L1 | Có với run/job/checkout/workflow provenance của ứng viên; **not_run**, không gọi GitHub. Không suy required từ tên workflow | Một job bắt buộc của đúng run thất bại |
| M1 | LIVE cần owner duyệt riêng; **not_run/chua_do_duoc** đúng như đặc tả, không coi enum hoặc biến env đã được xác nhận | Đầu ra probe thuộc loại lỗi quy định hoặc không có model/rc khác 0; phiên bản còn cần sửa F03 |
| M2 | LIVE sau land do chủ kho chạy; **not_run/chua_do_duoc** đúng như đặc tả | Mất hoặc nhân đôi dòng trạng thái; trạng thái quan sát được phải được ghi thật |

Bằng chứng chạy cục bộ:

| Lệnh | Kết quả thật | Phạm vi |
|---|---|---|
| `python3 -B probe_repo.py` | rc=0 | Đối chiếu Git, nguồn, số dòng, bảng và mẫu registry; [log](measurements/repo-summary.txt) |
| `python3 -B probe_contracts.py` | rc=0 ở lượt `contracts-verified` | AST bootstrap/rotation với RAM giả; script thiếu; các predicate; tiến trình con vô hại; dọn xong cả cha/con. [log](measurements/contracts-verified.txt) |
| `python3 -B probe_child_env.py` | rc=0; child saw synthetic=True, parent unchanged=True, sentinel in log=False | Đúng AST agent-exec với dependency/môi trường giả; [log](measurements/child-env.txt) |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B cay-kho/.claude/dev/packet_loop.py doctrine-scan --root cay-kho` | rc=0; sạch, 10 tệp | Head thực; [log](measurements/doctrine-head.txt) |
| `PYTHONDONTWRITEBYTECODE=1 python3 -B probe_baseline.py` | rc=0; sạch, 10 tệp | 13 tệp nguồn/tài liệu được chép bằng `git show <base>:<path>` vào cây tạm; chỉ đủ phạm vi scanner, không gọi đó là full baseline suite. [log](measurements/doctrine-base.txt) |
| `python3 -B probe_final.py` | rc=0; 22 tệp bằng byte HEAD; status/diff/index sạch | Kiểm cuối, [log](measurements/final-state.txt) |

Lượt probe ban đầu `measurements/contracts.txt` rc=1 do race khi đọc `/proc` sau khi tiến trình vừa biến mất trong **mã probe reviewer**. Đã sửa bộ quan sát để coi `ProcessLookupError` là chết và chạy lại; kết quả dùng cho finding là `contracts-verified` rc=0. Đây không phải lỗi của kho hay một selftest sản phẩm bị đỏ.

## (iii) KẾT LUẬN

**`request_changes`: 3 finding còn mở — 1 P1, 2 P2; 0 P0, 0 P3.** Danh tính đúng. Các khẳng định local về repo đã đo ở trên chủ yếu khớp; lỗi còn mở nằm ở thiết kế nghiệm thu/vị trí và phép xác nhận phiên bản ghim. Không tìm thấy finding P0 trong phạm vi đã review; các phép LIVE vẫn chưa đo đúng như giới hạn đã khai.

Đặc tả revision 1 đã đóng băng và merge: không sửa trong review này. Các gợi ý dưới đây chỉ để chủ kho cân nhắc revision 2, không phải uỷ quyền thay đổi repo.

| Slug lớp | Finding/biểu hiện | Mức cao nhất còn mở | Nguồn | Cách đóng lớp |
|---|---|---|---|---|
| `h1-neo-header-thay-ket-thuc-phu-thuoc` | F01, cận dưới H1 sai | P1 | Lượt này, reviewed_sha ở đầu tệp | Đo cả vị trí sau khối thật và mutant chèn trước khi cài phụ thuộc |
| `a4-chi-do-pid-cha` | F02, kiểm dừng nhóm chỉ nhìn cha | P2 | Lượt này, cùng SHA | Ca có tiến trình con cùng nhóm; mutant chỉ kill cha phải chết đúng ca |
| `agy-ghim-bang-chuoi-con` | F03, chứa version chưa phải bằng version | P2 | Lượt này, cùng SHA | So token phiên bản ghim; đối chứng phiên bản khác có tiền tố chung |

Ba lớp, ba biểu hiện. Không có verdict trước được cung cấp trong context của lượt review đặc tả này để tuyên bố finding cũ đã đóng; lịch sử P2a được giữ như thông tin kế thừa, không reset hoặc xét lại budget của nó.

### h1-neo-header-thay-ket-thuc-phu-thuoc  [P1]  H1 cho qua khối gọi bootstrap trước khi phụ thuộc được cài

MỤC/DÒNG: `muc_tieu` 5, SPEC dòng 137–141; H1 dòng 192.

VẤN ĐỀ: Mục tiêu yêu cầu đặt khối mới **sau khối phụ thuộc Python**, vì bootstrap cần các gói đó. H1 chỉ đo sau **dòng tiêu đề** của khối. Giữa header và pip thật là hàng trăm dòng; một khối đặt ngay sau header vẫn đạt điều kiện thứ tự của H1, trước lúc cài dependencies. Trên môi trường mới, bootstrap có thể hỏng ở import và helper vẫn rc=0; hook đã đi qua mà credential chưa nạp. Mutant “dời sau doctor” đã nêu trong đặc tả không phân biệt được lỗi đặt quá sớm này. Đây là thước nghiệm thu sai vị trí cho một yêu cầu chính của packet, không phải sai số số dòng đã khai.

ĐÃ ĐO: `python3 -B probe_contracts.py`, rc=0, [contracts-verified](measurements/contracts-verified.txt):

```text
dependency header=237; pip=501; block end=510; H1 upper bound=575
hypothetical block immediately after header: H1 ordering condition=True; after dependency block=False
```

Các vị trí đến từ chính hook tại reviewed_sha; hook bằng byte base. Không sửa hook hoặc thực thi bootstrap thật. Phép đo là đối chiếu predicate của H1, chưa phải chạy mutant của implementation tương lai.

ĐỘ TIN: cao.

GỢI Ý CHO REVISION 2: Sửa H1 để neo sau ranh giới kết thúc khối phụ thuộc thật; hoặc chạy đoạn trích với dependency/helper giả và ghi thứ tự các bước. Thêm ca cài mới, mutant gọi nap trước khi hoàn tất phụ thuộc phải đỏ vì đúng quan hệ thứ tự. Chốt cả nhánh dependencies đã có và chưa có; tránh neo vào một số dòng cố định dễ trôi. Chỉ thay tiêu chí/vị trí, không mở rộng write_set.

### a4-chi-do-pid-cha  [P2]  A4 chưa chứng minh yêu cầu dừng và kiểm lại cả nhóm tiến trình

MỤC/DÒNG: `muc_tieu` 1, SPEC dòng 108–109, 116; A4 dòng 173; thiết kế fixture dòng 161–166.

VẤN ĐỀ: Yêu cầu là giết **cả nhóm tiến trình** rồi kiểm lại. A4 chỉ tạo `tl.py` giả ngủ và kiểm PID của chính nó. Một implementation thay thao tác giết nhóm bằng giết cha vẫn thoả những quan sát quy định trong ca hiện tại. Nếu bootstrap sinh tiến trình con, helper có thể báo “đã dừng” trong khi con vẫn chạy; lớp lỗi này có điều kiện, không xuất hiện ở fixture chỉ có một tiến trình. Đột biến “bỏ giết” bắt việc không dừng cha, chưa bắt việc để sót con.

ĐÃ ĐO: `python3 -B probe_contracts.py`, rc=0, [contracts-verified](measurements/contracts-verified.txt): reviewer tạo một tiến trình Python mới với session/group riêng, cho nó sinh một Python con chỉ ngủ; chỉ giết và wait cha:

```text
parent dead=True; descendant alive=True
cleanup: parent dead=True; descendant dead=True
```

Mã probe xem zombie là chết theo CLAUDE.md. Cả hai tiến trình đều do reviewer tạo và đã dọn; không gọi CLI thật. Đây là phản chứng cho tính đủ của phép quan sát PID cha, không phải lời khai đã chạy helper chưa tồn tại.

ĐỘ TIN: cao.

GỢI Ý CHO REVISION 2: Bổ sung fixture sinh con trong cùng nhóm, log cả PID cha/con, bắt cả hai chết sau timeout trong hạn; giữ ca chỉ có cha làm đối chứng. Thêm mutant chỉ kill cha và buộc ca nhóm đỏ đúng `TinHieuChotCa`/tên ca. Cần `finally` dọn nhóm giả khi chính test thất bại và giữ quy ước zombie, để test không để lại tiến trình hoặc cấp tín dụng giả do cleanup.

### agy-ghim-bang-chuoi-con  [P2]  Phép xác nhận bản đã cài không bảo đảm đúng bản ghim

MỤC/DÒNG: mục *Hằng ghim*, SPEC dòng 75–93; `muc_tieu` 2 dòng 121–123; B3/B4 dòng 180–181; M1(iii) dòng 209.

VẤN ĐỀ: Mục tiêu là bản ghim `1.4.12` với URL/băm cố định, nhưng được phép giữ executable có sẵn chỉ vì output `--version` **chứa** văn bản của bản ghim. So chuỗi con không có ranh giới token nhận cả một phiên bản khác có phần đầu trùng rồi tiếp tục bằng chữ số. Nhánh đó không tải lại nên cũng không đi qua bước xác minh sha512. M1(iii) dùng cùng điều kiện chứa chuỗi, vì vậy chưa khắc phục được việc giữ nhầm bản. B4 chỉ có một bản lệch không cùng tiền tố, nên chưa khoá lớp lỗi này. Cơ chế mô tả bằng lời; không đưa chuỗi vượt guard vào hướng dẫn thi hành.

ĐÃ ĐO: Đối chiếu trực tiếp câu điều kiện ở dòng 122 và M1(iii), cùng predicate tương ứng trong `probe_contracts.py` ([contracts-verified](measurements/contracts-verified.txt), rc=0). Phép đo cục bộ chỉ dùng văn bản version tổng hợp; không tải, tạo hay chạy executable `agy`. Nhận định dựa trên ngữ nghĩa phép `contains`, không phụ thuộc một bản phát hành khác thực tế đã tồn tại hay chưa.

ĐỘ TIN: cao đối với lỗi so tiền tố; tác động có điều kiện khi executable có sẵn mang phiên bản cùng tiền tố.

GỢI Ý CHO REVISION 2: Quy định cách lấy token phiên bản từ output probe và so chính xác với `AGY_VER`, gồm quy tắc hậu tố build hợp lệ nếu cần. Dùng cùng chuẩn cho nhánh tái sử dụng và M1(iii). Thêm đối chứng đúng bản phải 0 tải, và khác bản nhưng chung tiền tố phải tải lại; tránh regex quá chặt làm từ chối format version hợp lệ của đúng bản ghim. Giá trị enum `modelProvider` và hành vi auto-update vẫn là các giới hạn đã khai, không bị tính thành finding này.
