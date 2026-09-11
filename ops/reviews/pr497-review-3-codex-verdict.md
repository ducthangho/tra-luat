verdict: changes_requested
reviewed_sha: 4e6a2d59386335f966bfb7160e98af02ae30d1ec

Review lượt 3 bằng OpenAI Codex, bề mặt API với công cụ shell trực tiếp trong sandbox; không dùng connector GitHub. Tree tự đo: `115b1835be0a14c63669357a4c8e05a0ad542c4a`. **0 P1 / 6 P2 / 0 P3.** Cả 12 lệnh trong EVIDENCE chạy lại đều đạt. Các finding dưới đây thuộc lời khai và giới hạn bằng chứng; không phát hiện thay đổi runtime trong 16 dòng chú thích được thêm vào `ops/cong_cu.py`.

## ĐỐI CHIẾU LƯỢT 2

- `hai-loi-khai-thieu-nhan-va-sai-co-trang`: **VÁ HỜ** — CHANGELOG:7–22 đã tách object/ref có sẵn khỏi ref máy chủ; cả khối 320/320 và 322/321 đã có THUẬT LẠI. Nhưng `ops/cong_cu.py:223` vẫn khai đã mở #498 mà không có nhãn, trái biên nhận lượt 2:60–63 nói đã gắn. `git diff 1d58500 HEAD -- ops/cong_cu.py` rỗng: chỗ này chưa được vá. Các lời kể lượt Windows đỏ ở CHANGELOG:103–110 và chú thích :218 cũng chưa mang nhãn tại chỗ. Quét ref thật cho 324/324 cục bộ; tệp được thuật lại là máy chủ có 322 dòng, không xác thực GitHub. Không kết luận giá trị Issue/CI sai.
- `attestation-runtime-bi-nang-thanh-phep-do`: **VÁ SINH LỖI MỚI** — ngoại lệ prompt đã bỏ; parse hai YAML và hai hàng mục lục xác nhận `model_yeu_cau=gpt-6-astra`, `model_da_chay=KHONG_DO_DUOC`; CHANGELOG:217–227 đã gắn THUẬT LẠI. Nhưng receipt lượt 2:176–184 vừa gọi lý do lựa chọn cờ của phiên là “ĐO ĐƯỢC”, vừa khai toàn khối runtime ATTESTATION, không ngoại lệ. Receipt lượt 1:135 còn “NỢ ĐÃ ĐO”. Đã gọi riêng `launcher.chot_kho` trên bản chép: cơ chế hiện tại thật sự cho `CHAN 11` với expected-repo, root OID đọc được; phép chạy hiện tại không xác thực cờ đã dùng trong phiên cũ. Xem finding cùng slug và giới hạn của phép khớp tree bên dưới.
- `so-hang-github-khong-co-quy-tac-dem`: **ĐÃ VÁ THẬT** — thực hiện đúng phép cắt từ `## BẢNG ĐO` đến `**Đột biến và phép thử`, đếm dòng bảng chứa nguyên văn `KHÔNG ĐO ĐƯỢC`: **28**. Receipt lượt 1:87–100 và README:274 đều ghi quy tắc, đồng thời nói số này gồm giới hạn ngoài GitHub. Không còn gán 28 cho một tập “phía GitHub” chưa định nghĩa.
- `ke-sai-ly-do-reviewer-khong-chay-ls-remote`: **VÁ HỜ** — CHANGELOG:198–215 đã trích đúng verdict lượt 1:157. Nhưng receipt lượt 1:197 vẫn viết “Reviewer đọc câu sai đó, kết luận…”, README:18 vẫn viết “Reviewer tin câu sai đó…”. Hai nơi ấy kể khác nguồn; README:273 và receipt lượt 2:104 lại khai đã sửa. Đã đối chiếu nguyên văn bằng `nl -ba` và thử sửa cả hai nơi trên bản chép; t27 và validator vẫn rc=0.
- `evidence-dem-thieu-ref-giao-head`: **ĐÃ VÁ THẬT** — đo mirror **324**, ref giao hàng **1**, tập loại riêng ref ấy **323**; quét tiêu đề r362 lần lượt **2/1**. Khối cấu hình EVIDENCE và `do-goi.txt` khớp cả 9 dòng với phép đo cuối lượt. Nói rõ đã loại `pr497-head`, không lọc để ép số. Không tái xác nhận được thao tác dựng gói của lượt 2, chỉ đối chiếu hiện vật kể về lượt đó và đo gói hiện tại.
- `khai-shellcheck-duoc-ci-ghim-khi-khong-co-pin`: **ĐÃ VÁ THẬT** — probe trả actionlint **1.7.7**, shellcheck **0.9.0**, jsonschema **4.26.0**. Parse CI/bản kê: actionlint và jsonschema có pin; shellcheck `ban_ghim=null`, ba công thức apt/brew/choco không nêu phiên bản. CHANGELOG:324–330 và EVIDENCE:53–58 đã phân biệt đúng phiên bản quan sát với phiên bản cưỡng chế.
- `hai-cong-duoc-khai-thanh-moi-cong-trong-kho`: **ĐÃ VÁ THẬT** — CHANGELOG:190–196 thu kết luận về đúng hai cổng. Chạy lại năm mutant Issue/số bước/cha merge/thẩm quyền/số nhánh mù: **5/5 sống** qua `doc-claims-check --strict --json` và `release-verify --strict --json` sau tái sinh manifest. Giữ manifest cũ với mutant Issue thì verify **rc=2**. Đây là giới hạn đã đo của hai cổng, không phải kết luận về mọi cổng.

## BẢNG ĐO

Mọi cổng được chạy trên bản chép đầy đủ trong sandbox, giữ nguyên HEAD và cấu hình `core.abbrev=7`. Bản chép đột biến và bản chép lịch sử riêng biệt. Đặt `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` và cấu hình/cache thử nghiệm trong sandbox; Git dùng global config rỗng tại sandbox, bỏ system config. Không cài gói, không gọi mạng. `ls-remote origin` chỉ được gọi sau khi xác minh origin là đường dẫn mirror trong sandbox.

Các lệnh nền đã chạy, từ gốc bản chép:

```sh
python3 ops/lease_publish_test.py
python3 ops/bien_nhan_v2.py --root .
python3 ops/bien_nhan_v2_test.py
python3 ops/cong_cu.py kiem-tra --json
python3 ops/cong_cu_test.py
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
python3 scripts/tl.py golden-test --json
python3 scripts/tl.py determinism-audit --strict --json
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py workflow-audit --strict --json
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song --root .
```

**Cây, gói và phép canh ref.** GIT = `git -C cay-kho rev-parse`, `show`, `diff`, `log`, `merge-base --is-ancestor`. REF = `for-each-ref` trên mirror/bộ đệm, `ls-remote --heads origin` trên mirror, rồi so tập tên sau khi bỏ tiền tố; bỏ riêng alias HEAD ở bộ đệm. Quét r dùng biểu thức tiêu đề cấp 1 `^# .*\br362:` / `r363:` trên CHANGELOG của từng ref, không đếm một lần nhắc r trong prose thành một mục phát hành.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact head/tree; clone đầy đủ | `4e6a2d5`; tree trong EVIDENCE | SHA/tree đầy đủ như đầu verdict; shallow=false; HEAD detached; abbrev=7 | Có |
| Ngày và hai việc r362 | 2026-09-10; đóng nợ #490, rút lời khai shellcheck | Commit đầu `25c2d5b` có thời điểm 2026-09-10T03:43:16Z; §1 và §2 có đủ hai việc | Có về Git/nội dung; trạng thái GitHub tách bên dưới |
| VERSION | không nâng, 1.36.68 từ r336 | VERSION=1.36.68; diff VERSION rỗng; `log -S 'v1.36.68 — r336:'` trả `3dcdc6a`; VERSION tại commit ấy cũng 1.36.68 | Có |
| Diff giao hàng | 8 tệp, +1235/−5, 8 commit, `0721811..HEAD` | `diff --numstat`: 8 / 1235 / 5; `rev-list --count`: 8. `diff.patch` và `numstat.txt` khớp byte/nội dung Git | Có |
| Phần đổi từng tệp | CHANGELOG, manifest, chú thích, hồ sơ hai lượt | CHANGELOG +331; manifest +5/−5; cong_cu +16; README +4; verdict/receipt lượt 1 +161/+208; lượt 2 +259/+251 | Có |
| Hành vi cong_cu | chỉ chú thích | `ast.dump(ast.parse(...))` tại `0721811` và HEAD bằng nhau | Có |
| Master đã hợp nhất | `0721811`; master đổi 3 tệp | `merge-base --is-ancestor 0721811 HEAD` rc=0; merge `1e75335` có cha `52b36d1` và `0721811` | Có trong Git |
| Giao write set | 0; ba tệp master | `diff --name-only 28ba133 0721811`: `.github/workflows/ops-thu-hoi-admission.yml`, `ops/lease_publish.py`, `ops/lease_publish_test.py`. Giao với phần PR trước merge rỗng | Có; không có log để tái quan sát thao tác merge cũ |
| Origin | mirror trong sandbox | `config --local --get remote.origin.url` đúng đường dẫn `kho.git` ghi trong do-goi | Có; không phải GitHub |
| Mirror và ref giao hàng | 324 = 323 + 1 | `for-each-ref refs/heads`: 324; `pr497-head`: 1; loại riêng nó: 323 | Có |
| Cấu hình do-goi và khối EVIDENCE | 9 dòng, worktree sạch | Cả 9 giá trị khớp phép đo lại cuối lượt, gồm origin, HEAD, tree, shallow, abbrev, status | Có; không thấy lỗi mô tả hạ tầng mới |
| Bộ đệm hiện tại | phân biệt với máy chủ | 325 remote-tracking refs kể HEAD; 324 sau bỏ HEAD. Mirror/đệm: thiếu 0, thừa 0; `ls-remote` cục bộ cũng 324 | Chỉ chứng minh hai tập cục bộ |
| Tệp được thuật lại là máy chủ | 322 dòng, băm ec6ef20af4eb7f73… | 322 dòng, 25.944 byte; SHA-256 `ec6ef20af4eb7f734fcb0e321c86b93d0efbb34493630e968fcfb138b51b5ec8` | Có về byte |
| Nguồn và giờ chụp tệp đó | GitHub, 2026-09-10T07:55:40Z | **KHÔNG ĐO ĐƯỢC**: chỉ có nội dung tệp, không có nguồn độc lập xác thực nơi chạy/giờ chụp | ATTESTATION đã ghi đúng |
| Tệp 322 so mirror | cần so tập, không chỉ lực lượng | Tệp thiếu so mirror: 0; mirror thừa `pr487-merge`, `pr497-head`: 2. Sau bỏ ref giao hàng còn thừa 1 | Có số học; không xác minh trạng thái xóa nhánh GitHub |
| r360 đã có | nhánh khác, chưa merge | Một ref có tiêu đề r360: `claude/pr491-land-va-findings-wip`; trạng thái PR/phiên **KHÔNG ĐO ĐƯỢC** | Có trong snapshot, không xác nhận GitHub |
| Lịch sử canh lần đầu | máy chủ 320, đệm 320, mù 1 rồi 0; quét 320 | **KHÔNG ĐO ĐƯỢC**: không có snapshot máy chủ/bộ đệm trước fetch tại thời điểm ấy | Đã gắn THUẬT LẠI; không lấy số mới bác snapshot cũ |
| Nhánh từng mù lần đầu | `codex/wp484-g3-windows`, đầu r356 | `git show` ref hiện tại: tiêu đề đầu r356. Có 1 tên được nêu; việc từng mù **KHÔNG ĐO ĐƯỢC** | Một phần |
| Lịch sử canh lần hai | 322/321, mù 2, thừa 1 | **KHÔNG ĐO ĐƯỢC** tập đệm 321 trước fetch. Phép tính 322−321=1, 2−1=1 đúng | Đã gắn THUẬT LẠI |
| Hai nhánh mù được kể | land-492-bookkeeping, wp484-g4-windows | Cả hai ref hiện có; lịch sử mù và fetch **KHÔNG ĐO ĐƯỢC** | Không nâng hiện diện hiện tại thành lịch sử |
| Sau fetch lần hai | mù 0, quét 323 ref phía điều phối | Hiện tại tệp 322 không có tên thiếu trong mirror; thao tác fetch và tập điều phối quá khứ **KHÔNG ĐO ĐƯỢC** | Một phần |
| r362 trên mirror | 2 cả gói; 1 sau loại ref giao hàng | Đúng hai ref: `claude/handoff-tra-luat-repo-2ak5th`, `pr497-head`; loại ref giao hàng còn 1 trên tập 323 | Có |
| r363 | 1, ở land-492-bookkeeping | Đúng 1 ref `claude/land-492-bookkeeping`; tiêu đề đầu r363. Nhánh wp484-g4-windows hiện có đầu r356 | Có trong snapshot |
| Đếm bằng nhau có thể che tập lệch | canh số đếm không đủ | Đối chứng dữ liệu cục bộ: lấy tập 322 tên của tệp, thay wp484-g4-windows bằng pr487-merge. Vẫn 322=322; hiệu tập chỉ đúng 1 thiếu/1 thừa | Có răng; không giả là snapshot GitHub |

**§1, §2: GitHub, số học và công cụ.** CI-TĨNH = parse `.github/workflows/ci.yml` tại `8cee941`, `7693852`, `28ba133`, HEAD. Cả bốn có cùng blob `2e21c0c1f0701e837f7c13fa20a55ab39fd5805c`. Đánh giá điều kiện thiết kế khác việc quan sát job đã chạy.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Ba vế ADR-0034 | merged, hậu-merge gate, bookkeeping | Định nghĩa CONTEXT/ADR phù hợp ba vế | Có về quy tắc |
| Merge #490, hai cha | 8cee941; 00e017a + 01e7f77 | `show -s --format='%H %P' 8cee941`: đúng merge và thứ tự hai cha | Có trong Git |
| r359 có 0 hiện vật CI trong cây | không có hiện vật neo 8cee941 | `git grep -l 8cee941 71e0053 -- .` chỉ trả CHANGELOG. Tìm ở HEAD trả thêm các hồ sơ review, không thấy response CI thô | Có trong phạm vi cây/tìm kiếm; không suy thành CI chưa chạy |
| Job Ubuntu | success, 37 success + 4 skipped + 0 failure = 41 | Tổng số học 41; kết quả/đếm runtime **KHÔNG ĐO ĐƯỢC**, thiếu response Actions | Nhãn thuật lại; chưa xác minh CI |
| Job Windows | success, 35 success + 6 skipped + 0 failure = 41 | Tổng số học 41; runtime **KHÔNG ĐO ĐƯỢC** | Như trên |
| Hai khoảng thời gian job | 18:50:37→19:11:32; 18:50:37→19:44:09 | Hiệu lần lượt 1.255 s = 20m55s; 3.212 s = 53m32s. Các mốc đầu vào **KHÔNG ĐO ĐƯỢC** | Chỉ xác nhận số học |
| Run và attempt | 34391481045, push, master, 8cee941, attempt 1, không rerun | **KHÔNG ĐO ĐƯỢC**: không dữ liệu Actions hoặc mạng | Không chứng nhận run |
| Hai lượt đối chiếu | 7693852 attempt 2; 28ba133 attempt 1 | Commit tồn tại, workflow cùng blob; attempt/kết quả **KHÔNG ĐO ĐƯỢC** | Một phần |
| Ba lượt cùng hình dạng; skip 4/6 | khớp từng bước giữa 3 lượt master | CI-TĨNH cho push/master thành công: Ubuntu skip 11,23,28,39; Windows skip 11,21,22,28,36,39, theo cách đánh số cộng bước Setup job. Quan sát 3 lượt thật **KHÔNG ĐO ĐƯỢC** | Thiết kế phù hợp; không xác minh runtime |
| #11; #22/#23; #38/#39 | PR-only; Linux/không Linux; LAND/WORKER | Đúng điều kiện trong YAML. Workflow khai 40 bước; 41 là số runtime được kể, không phải 41 mục YAML | Có về mã |
| #490 đạt landed, 0 failure | đủ 3 vế | Merge và đoạn bookkeeping đọc được; CI và thẩm quyền **KHÔNG ĐO ĐƯỢC** | Reviewer không tự chứng nhận landed |
| Bookkeeping không có tệp riêng | r359, theo quyết định chủ kho | Có lời ghi ở r359; quyết định/thẩm quyền ngoại bộ **KHÔNG ĐO ĐƯỢC** | Chỉ xác nhận văn bản |
| Nợ treo bao lâu | khoảng vài giờ; rút ~7 giờ; bằng chứng sẵn từ 19:44:09Z | **KHÔNG ĐO ĐƯỢC**: không mốc đọc/đóng nợ. Giờ commit không phải giờ đọc CI | Giới hạn đã nói rõ |
| Lời r361 bị rút | “Nếu chỉ shellcheck hỏng thì không ai biết” | Câu có trong r361; r362 rút rõ. Giữ lịch sử không phải lỗi mới | Có |
| A/B có shellcheck | actionlint DAT, shellcheck DAT; canary DAT, SC1003 rc=1 | PATH thử riêng: đúng cả bốn; tổng DAT, CLI rc=0 | Có |
| A/B thiếu shellcheck | actionlint DAT; shellcheck KHONG_DO_DUOC; canary DO/blocking | Đúng; chi tiết SUY_GIAM, fixture rc=0; tổng DO, CLI rc=2 | Có |
| Một công cụ thiếu vẫn xanh | `--chi shellcheck`: tổng DAT, canary rỗng | Đúng: shellcheck KHONG_DO_DUOC, canary có 0 phần tử, CLI rc=0 | Có |
| Điều kiện chạy canary | chỉ `chi is None` | Full scan có 1 canary; quét riêng thiếu shellcheck có 0 | Có |
| Quyền chặn | canary DO nâng tổng, trừ advisory | Bỏ nhánh nâng tổng: canary DO nhưng tổng DAT/rc=0. Đổi blocking→advisory: cùng kết quả tổng DAT/rc=0 | Đã đo cả cơ chế và ngoại lệ |
| Hai bước cài riêng; G5 #9 | #7 shellcheck, #8 rg; G5 quét đầy đủ | YAML thứ tự khai báo 6/7/8, phù hợp #7/#8/#9 khi cộng Setup job. Installer gọi `kiem-tra --chi`; G5 không `--chi`; rg bắt buộc, shellcheck không | Có về mã |
| Windows đỏ #8 khiến #9 skip | #7 xanh nhưng shellcheck hỏng, #8 đỏ, #9 bỏ qua | Thiết kế cho phép; JSON/trạng thái của lượt thật **KHÔNG ĐO ĐƯỢC** | Chưa đủ nhãn tại chỗ ở §2/chú thích |
| Hai lần chạy bác lời r361 | 2 lần cong_cu.py | A/B hai full scan ở trên đủ cho DAT→DO. Số lần tác giả thật sự chạy trong phiên cũ **KHÔNG ĐO ĐƯỢC** | Có về khả năng tái hiện |
| “tệp này đã ghi ba lần” | 3 lần bài học đọc rỗng thành phủ định | **KHÔNG ĐO ĐƯỢC** con số phân loại: không chỉ ba đoạn hoặc quy tắc nhận một lần. Không đồng nhất với ngưỡng ba lần trong CLAUDE | Chưa có phép đếm tái lập |
| Packet #290 và ba dẫn chiếu | xuất xứ, spec đóng băng; dòng 28/116/164, AGENTS:22–23 | Spec có cảnh báo đóng băng; Git có merge `59fe955` của #291/#290, ancestor HEAD rc=0. Ba dòng protocol chứa đúng nội dung dẫn | Có về nguồn trong kho; landed GitHub không đo được |
| Số mục protocol | 20, không phải §28/116/164 | Đếm `^## [0-9]+`: 20 | Có |
| Ba finding trước lượt 1, P2 ×2 ở phần cuối | 3 P2; 2 đính chính phần nhận việc | Verdict lượt 1 có đối chiếu đủ 3 slug; số review GitHub gốc **KHÔNG ĐO ĐƯỢC** | Có về hồ sơ, không tự xác thực GitHub |
| Trang Issue cũ | 30 là cỡ trang, 0 khớp bị rút | Bản đầu có lời 30/0; response trang **KHÔNG ĐO ĐƯỢC** | Đã sửa cách diễn đạt |
| Issue mới | 128 mở; total_count 101 | **KHÔNG ĐO ĐƯỢC**: không response, truy vấn đầy đủ, thời điểm và phân trang | Nhãn tại CHANGELOG đúng |
| Tỷ lệ quét | ≈23%, 30/128 | 23,4375%; đầu vào GitHub không được xác thực | Số học đúng |
| Bốn Issue liên đới | #249/#295/#269/#297 | 4 ID khác nhau; nội dung/trạng thái và “không trùng” **KHÔNG ĐO ĐƯỢC** từ GitHub | Nhãn cùng nguồn đã có |
| t33 và write set | kiểm actionlint, không kiểm shellcheck; khác cong_cu.py | Đọc thân `t33_workflow_dang_lease_phai_qua_actionlint`: đúng một workflow/actionlint, không đòi shellcheck. Quan hệ mã đo được; liên kết Issue #249 là thuật lại | Đúng phạm vi mã |
| Phiên đang chạy | KHÔNG ĐO ĐƯỢC | Không có nguồn runtime phiên; truy vấn Issue không thay được phép này | Nhãn đúng |
| Nợ đã mở #498 | có Issue nhận nợ | **KHÔNG ĐO ĐƯỢC**: không hiện vật Issue. CHANGELOG:147 có nhãn; cong_cu.py:223 không có | VÁ HỜ |

**Hai verdict, hai receipt, bốn hàng README và §3.** Các băm dưới đây do đọc byte thật, không lấy digest trong receipt làm kết quả đo. Với mỗi đường dẫn verdict, đã chạy `git log --all --diff-filter=A --format=%H -- <đường-dẫn>`, đọc blob tại commit neo và kiểm ancestry. Không truy cập URL GitHub.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Verdict lượt 1: byte/dòng | 28.955 / 161 | 28.955 byte / 161 dòng | Có |
| Verdict lượt 1: SHA-256 | a6bf4bea… | `a6bf4bea67c347385960285c5e5d0d28346887da684595b6429f22a6d67aed27` | Có |
| Verdict lượt 2: byte/dòng | 43.791 / 259 | 43.791 byte / 259 dòng | Có |
| Verdict lượt 2: SHA-256 | 206aaf28… | `206aaf2814c5cb249506b6ae607b17a9071ac4d50eeea51b5cb031ca92531b00` | Có |
| Receipt lượt 1: evidence_url | commit đầu 8104480 | Log thêm tệp trả đúng **1** commit `8104480fe756978455abf1baf96adf6f9b399cbb`; blob bằng byte hiện tại; ancestor HEAD rc=0 | Có về Git; URL trực tiếp KHÔNG ĐO ĐƯỢC |
| Receipt lượt 2: evidence_url | commit đầu 4d2a6f6 | Đúng **1** commit `4d2a6f69e67ce5299253bf8905b6b742d516f3fc`; blob bằng byte hiện tại; ancestor HEAD rc=0 | Có về Git; URL trực tiếp KHÔNG ĐO ĐƯỢC |
| Neo chưa ở master | cả hai anchor chưa trên master lúc viết | Với origin/master cục bộ `0721811`: ancestor rc=1 cho cả hai; HEAD rc=0 cho cả hai | Có trong snapshot; không nói master máy chủ hiện tại |
| Commit đầu và commit kế | lượt 1 chỉ verdict; lượt 2 verdict kèm vá; receipt sau | `diff-tree`: 8104480 chỉ 1 tệp verdict; 4d2a6f6 đổi 4 tệp, **không có cong_cu.py**. Cả hai t27 rc=1 tại commit đầu; HEAD t27 rc=0 | Đúng chuỗi nhập hồ sơ; “cả bảy đã vá” không đúng |
| Số P1/P2/P3 lượt 1 | 0/1/1 | Đếm tiêu đề `^### .*\[P1\]`, tương tự P2/P3: 0/1/1; tổng **2** | Có |
| Số P1/P2/P3 lượt 2 | 0/7/0 | 0/7/0; tổng **7**; danh sách bay_finding có 7 slug | Có |
| “Số finding tăng 1→7” | 1 finding lên 7 | **Tổng 2→7**; riêng hạng P2 mới là 1→7 | Không: đổi mẫu đếm mà không gọi tên |
| 5/7 nhắm phần chỉ có sau lượt 1 | năm finding | Theo chính tiêu chí phần bị chấm xuất hiện sau e826730, có **6**: attestation, số hàng, kể lý do, gói, pin shellcheck, và câu suy rộng hai cổng. Câu cuối thêm ở 52b36d1 | Thiếu một; xem finding đếm hồ sơ |
| Ba finding chạm receipt lượt 1/hai hàng README | 3/7 | Đối chiếu TỆP/DÒNG của verdict lượt 2: attestation, số hàng, kể lý do = 3 | Có |
| Cả bảy đã vá trước land | không finding nào bị bác, tất cả đã vá | Đối chiếu ở đầu: 4 đã vá thật, 2 vá hờ, 1 vá sinh lỗi mới. Quyết định nhận/bác và thời điểm land ngoại bộ **KHÔNG ĐO ĐƯỢC** | Lời “cả bảy đã vá” vượt cây hiện tại |
| Số hàng README | 2 mục lục + 2 cảnh báo | Đúng bốn dòng 17,18,273,274; đếm theo tên verdict trong cột đầu, không theo mọi lần nhắc chéo | Có số hàng; còn sai nội dung ở dòng 18 |
| Tree lượt 1 | 67df2efa… gắn e826730 | `rev-parse e826730^{tree}` = `67df2efa7e6f6c7b23bedfb43da647b395800a37`, khớp verdict | Có về định danh |
| Tree lượt 2 | 0430d2bd… gắn 1d58500 | `rev-parse 1d58500^{tree}` = `0430d2bdbc8e6e6c11bbf93c8bb12b1272b1202d`, khớp verdict | Có về định danh |
| Khớp tree xác nhận reviewer đọc đúng cây | “Bằng chứng DƯƠNG rằng reviewer đọc đúng cây” | Phép so xác nhận OID nhất quán. Đối chứng chỉ lấy OID bằng rev-parse, chép vào một dòng, so lại: cũng true ở cả hai SHA, không cần đọc nội dung tệp trong tree | Không đủ tự xác thực hành vi phiên |
| Hàng không đo được lượt 1 | 28, thay cho 17 | Đúng 28 theo quy tắc đã công bố. Tập 21 dòng ví dụ trong verdict lượt 2 đếm ra 21 chỉ số dòng; không dùng nó thay quy tắc 28 | Có |
| Prompt lượt 1 chỉ có trong receipt | `git grep … HEAD` trả chính 1 tệp | Tại 1d58500: **1** tệp. Tại HEAD: **2** tệp, thêm verdict lượt 2; vẫn không có prompt gốc | Không khớp lệnh HEAD hiện tại |
| Prompt lượt 2 | digest f9865a… là ATTESTATION | `git grep` digest đầy đủ chỉ trả receipt lượt 2; không có nguồn prompt độc lập | Nhãn prompt đúng; không xác minh digest nguồn |
| 13 ca thử lượt 1 | 13 | Bảng “Đột biến và phép thử” có 13 hàng dữ liệu, gồm cả thử vá và hai phép đo cho cùng mutant. Đã tái chạy cơ chế chính, 5 mutant prose, đối chứng tập và thử vá trong lượt này | Có về số hàng; không biến 13 hàng thành 13 mutant độc lập |
| 5/5 mutant lời khai sống | 5/5 qua hai cổng | Chạy lại đúng năm thay đổi: cả năm claims/verify rc=0 sau tái sinh manifest | Có, giới hạn đúng hai cổng |
| Danh tính/runtime hai lượt | provider/cross-provider, model yêu cầu; run ID, prompt, timestamps, trạng thái xong/rc=0 | **KHÔNG ĐO ĐƯỢC** độc lập: run.json, prompt, transcript không có trong gói. Hai README giữ requested/served tách biệt đúng | ATTESTATION; không tự xác nhận assurance hoặc danh tính người đăng |
| Thời lượng runtime | 878.149 s và 1242.188 s; README 878/1242 s | Hiệu các timestamp trong receipt: **878.148880** và **1242.187745** s; làm tròn đúng. Mốc thời gian thật **KHÔNG ĐO ĐƯỢC** | Chỉ số học |
| Lần chết và stdout/stderr | lượt 1: 1 lần, 297/396316 byte; lượt 2: 0 lần, 300/539074 byte | **KHÔNG ĐO ĐƯỢC** số lần, byte, hash stdout/stderr, mã thoát và thread_id của phiên cũ: thiếu hiện vật nguồn | Nhãn runtime không chứng thực scalar |
| Lỗi websocket/probe/record treo | 1 lần chết, os error 111, probe rc=0/0 lỗi, dang_chay/null | **KHÔNG ĐO ĐƯỢC** từ kho. CHANGELOG đã gắn THUẬT LẠI/tương quan; receipt lượt 1 còn NỢ ĐÃ ĐO | Còn mâu thuẫn nhãn |
| Lựa chọn neo launcher lượt 2 | expected-root-commit; expected-repo CHAN 11; “Lý do ĐO ĐƯỢC” | Gọi riêng `chot_kho` hiện tại: expected-repo cho CHAN 11, remotes rỗng; root `394e93468fc8d84ec20938e6df8fb7ab72b2cc37`. **KHÔNG ĐO ĐƯỢC** lệnh phiên cũ thật sự dùng | Cơ chế tái hiện được; trường runtime vẫn là ATTESTATION |
| Hai gói cũ và tuân thủ reviewer | lượt 1 origin GitHub/321; lượt 2 mirror324; sạch, 0 commit ngoài head | Đọc được lời khai trong verdict/receipt. **KHÔNG ĐO ĐƯỢC** trạng thái filesystem/quá trình lịch sử độc lập; không lấy gói lượt 3 thay gói cũ | Chỉ đối chiếu nguồn văn bản |
| Ba lối land neo | MERGE/fast-forward giữ, squash phá; đã đo 3/3 ở hồ sơ #490 | Receipt #490 có ba nhánh đo ở `phep_do_BA_LOI_LAND`; hai receipt #497 nói không đo lại. Lượt này kiểm ancestry hiện có, không tái chạy ba lối land | Không nâng lời dẫn hồ sơ cũ thành phép thử mới |

**Manifest và 12 cổng trong EVIDENCE.** Manifest được tự kiểm từng đường dẫn, size và SHA-256, rồi đối chiếu strict verifier; không chỉ so số `file_count` với chính nó.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Kiểm kê gói | 180→180; thêm/bớt 0 | 180 mục ở master và HEAD; hai tập đường dẫn bằng nhau; tự băm đủ 180 tệp, 0 sai size/hash | Có |
| Byte và hash manifest hiện tại | 8.138.680; 41e1c7b0… | Cộng byte thật = **8.138.680**; strict hash current/expected/full-tree đều `41e1c7b02c620a4e52b579b35b69e4c176e0a83c1ab2e3dd374bcedaf0ea22c6` | Có |
| Một tệp đổi trong kiểm kê | chỉ CHANGELOG; ops=0 | Giao 8 tệp PR với 180 mục chỉ CHANGELOG; manifest có 0 mục ops và không tự liệt kê nó. So từng entry: chỉ CHANGELOG đổi | Có |
| CHANGELOG trong manifest | size/hash mới | 844.358 byte; SHA-256 `3e77b38e8480d8ab0908a1da062e6117bf2ceff20e15e384f8569721ecb2b962`; byte gói tăng **28.462** từ master 8.110.218 | Có |
| lease_publish trên cây đã merge | 146/146, chạy146, bỏ0 | **rc=0**, 146/146; đã chạy146, bỏ qua0 | Có |
| lease_publish trước merge | 121/121 | Checkout `52b36d1` trên bản chép lịch sử, chạy cả suite: **rc=0**, 121/121; chạy121, bỏ0 | Có; không trộn hai cây |
| Validator ở CHANGELOG:271 | 49 ĐẠT v2, 0 vi phạm, 0 không đo, tổng102 | Trên HEAD: **50 ĐẠT v2**, 11/11 legacy, 42 nợ, 0 vi phạm, 0 không đo, **tổng103**, rc=0 | Không; số cũ còn nguyên |
| Validator trong EVIDENCE:41 | 50/11/42/0/0/tổng103 | Đúng cả sáu số; 50+11+42=103; TỔNG ĐẠT | Có |
| Nguồn số validator cũ | chưa neo SHA tại bảng “trong cây này” | Checkout `4d2a6f6`: validator rc=0, **49**, 11/11 legacy, 42 nợ, tổng **102** | Đo được số đúng ở cây trước receipt lượt 2 |
| Suite biên nhận | 48/48; 63/63 mutant có răng; 2/2 tự kiểm | **rc=0**, đúng cả ba cặp; suite còn báo 45/63 mutant khai đối chứng | Có |
| cong_cu kiem-tra | rc=0, DAT; canary DAT | **rc=0**, tổng DAT, actionlint_shellcheck DAT, SC1003 rc=1 | Có |
| Suite công cụ | ca23, mutant18, lỗi0 | **rc=0**, 23/18/0 | Có |
| Ba phiên bản môi trường | 1.7.7 / 0.9.0 / 4.26.0 | Probe thật khớp; PyYAML ở đây 6.0.1, CI cài 6.0.3 | Có ba bản được khai; không nhận môi trường hoàn toàn bằng CI |
| Pin của CI | chỉ 2/3 | ci.yml:93 jsonschema==4.26.0; :97 AL_VER1.7.7; :101 shellcheck không phiên bản; cong_cu.yaml shellcheck null | Có |
| Lỗi G5 phiên reviewer cũ | lỗi mutant1/tổngDO do thiếu jsonschema, không mã khác | AST cong_cu không đổi; tệp suite/bản kê không đổi so head lượt 1. Nền hiện tại có jsonschema và suite đạt. Runtime nền cũ **KHÔNG ĐO ĐƯỢC** độc lập | Không gọi khác môi trường là hồi quy |
| Release verify | ok=true; expected=checked=180; extra=[] | **rc=0**, ok=true, 180/180, failed/extra/errors đều rỗng | Có |
| Golden | ok=true | **rc=0**, 20 ca, 0 ca sai | Có |
| Determinism | ok=true | **rc=0**, 15 kiểm tra đạt | Có |
| Doc claims | rc=0, ok=true | **rc=0**, 106 tệp, flags=[], **367 advisory** | Có; không đồng nghĩa 0 cảnh báo hay đã kiểm nghĩa mọi lời khai |
| Workflow audit | rc=0 | **rc=0**, ok=true; 26 cards, 11 groups; errors/warnings rỗng | Có |
| Doctrine scan | rc=0 | **rc=0**, 7 tệp, 0 chỗ chép doctrine | Có |
| ADR sống | rc=0 | **rc=0**, 46 ADR/46 hàng §20; ngoại lệ trạng thái 0016 được khai | Có |
| Cổng đã chạy so CI | EVIDENCE12, ci.yml31 bước cổng | EVIDENCE đúng 12 lệnh, đã chạy đủ. YAML 40 = 8 setup + 31 cổng + 1 upload; setup là bước khai báo 1–7 và 9, upload là 29. Khối r362 chỉ liệt kê 10 lệnh | Có; không khai đã chạy đủ CI |
| CI exact head chưa chạy theo yêu cầu | cố ý không đốt CI | **KHÔNG ĐO ĐƯỢC** trạng thái/quyết định GitHub từ đây | Không xem là cổng đỏ, không yêu cầu chạy CI mới |

**Đột biến: cả hai chiều.** Mỗi ca bỏ/sửa hiện vật được phục hồi byte gốc trước ca tiếp theo. Đã gọi riêng các chốt sau, trên bản chép:

```sh
python3 -c "import sys; sys.path.insert(0,'ops'); import lease_publish_test as t; t.t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()"
python3 -c "import sys; sys.path.insert(0,'ops'); import lease_publish_test as t; t.t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()"
python3 -c "import sys; sys.path.insert(0,'ops'); import cong_cu_test as t; t.t13_actionlint_bien_mat_giua_probe_va_canary()"
```

| khẳng định / ca | PR khai hoặc đối chứng | đo được | khớp? |
|---|---|---|---|
| t27 và t26, hồ sơ nguyên vẹn | xanh | cả hai rc=0 | Có |
| Bỏ receipt lượt 1 / lượt 2 | thiếu mảnh hồ sơ | t27 rc=1 / 1; chỉ đúng receipt của từng lượt bị thiếu | Có răng, 2/2 |
| Bỏ hàng mục lục lượt 1 / lượt 2 | thiếu mảnh mục lục | t27 rc=1 / 1; báo thiếu đúng verdict trong cột mục lục | Có răng, 2/2 |
| Bỏ hàng cảnh báo lượt 1 / lượt 2 | cảnh báo phải được nâng | t27 rc=1 / 1; báo đúng caveat thiếu khỏi hàng/cột tương ứng | Có răng, 2/2 |
| Bỏ chính verdict lượt 1 / lượt 2 | kiểm chiều ngược của quan hệ | **t27 rc=0 / 0**, nhưng **t26 rc=1 / 1**, “trỏ vào tệp không có” | t27 riêng không bảo đảm tệp đích tồn tại; cặp t26+t27 bắt được |
| Đổi một chữ số verdict_sha256 của mỗi receipt | neo băm phải chết | bien_nhan_v2 rc=1 / 1; 1 vi phạm mỗi ca | Có răng |
| verdict_bytes cộng 1 ở mỗi receipt | 28955→28956; 43791→43792 | validator vẫn rc=0 / 0 | Không kiểm scalar này; số gốc tự đếm đúng |
| so_p2 cộng 1 ở mỗi receipt | 1→2; 7→8 | validator vẫn rc=0 / 0 | Không kiểm scalar này; số gốc đã tự đếm đúng |
| Chặn vòng canary | `if chi is None`→`if False` | t13 rc=0→1, đúng `TinHieuChotCa`, thông báo “canary mất executable bị nuốt” | Có răng, không lấy crash vô can làm tín dụng |
| Cùng mutant, full scan thiếu shellcheck | đo hậu quả | DO/rc=2→DAT/rc=0, canary=[] | Mất chặn thật |
| Bỏ nâng tổng / đổi advisory | phân biệt đo với quyền chặn | canary vẫn DO; tổng DAT/rc=0 trong từng ca | Khớp cơ chế/ngoại lệ |
| Issue 128→129, manifest cũ | toàn vẹn byte | release-verify rc=2, ok=false | Có răng với byte |
| Issue 128→129, manifest tái sinh | nghĩa số liệu | claims rc=0, build rc=0, verify rc=0 | Sống |
| 37 success→36, giữ 4 skipped và tổng41 | mâu thuẫn cộng | claims/build/verify rc=0/0/0 | Sống |
| Cha thứ nhất đổi thành cha thứ hai | SHA có thật nhưng quan hệ sai | claims/build/verify rc=0/0/0 | Sống |
| Xuất xứ #290→chủ | sai thẩm quyền | claims/build/verify rc=0/0/0 | Sống |
| Mù 1→0 trong lời lịch sử | số lời khai sai | claims/build/verify rc=0/0/0 | Sống |
| Thử sửa các finding của lượt này | nhãn, câu kể, snapshot, số đếm | Trên bản chép: claims, validator, t27, build, verify đều rc=0; sau chỉnh lại cách gọi 1→7, claims/build/verify vẫn rc=0 | Khả thi về các cổng đã chạy; xanh không tự chứng minh prose đúng |

Năm ca prose dùng lần lượt `python3 scripts/tl.py doc-claims-check --strict --json`, `python3 scripts/tl.py release-manifest --out RELEASE_MANIFEST.json --json`, `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`. Không đề nghị mở rộng validator hay xây cổng hiểu nghĩa trong PR hồ sơ này. Nhãn “t27 đòi đủ” chỉ đúng với receipt/hàng mục lục/hàng cảnh báo khi verdict hiện diện; nếu muốn nói cả chiều tồn tại verdict phải nêu thêm t26. Không gọi ca sống ở t27 là cả suite bỏ lọt.

### hai-loi-khai-thieu-nhan-va-sai-co-trang  [P2]  Biên nhận khai đã gắn nhãn #498 nhưng chú thích mã chưa được sửa

TỆP/DÒNG: `cay-kho/ops/cong_cu.py:218`, `:223`; `cay-kho/CHANGELOG.md:103–110`; `cay-kho/ops/reviews/pr497-review-2-codex-verdict.receipt.yaml:60–63`; đối chiếu `EVIDENCE.md:75–77`.

VẤN ĐỀ: Bản vá đã sửa ranh giới object/ref có sẵn với ref máy chủ, và nhãn hai khối số ref lịch sử đúng. Tuy nhiên, lời “gắn nhãn cho #498 trong ops/cong_cu.py” của receipt lượt 2 không khớp cây: chú thích vẫn nói “nợ đã mở thành Issue #498, liên đới #249” như sự thật tại chỗ. Đoạn chú thích về lượt CI rg đỏ/G5 skip và đoạn Windows đỏ trong §2 cũng không có nhãn nguồn tại chỗ. Nhãn ở CHANGELOG:147 không phủ một tệp mã riêng. Vì vậy lời EVIDENCE rằng các số mới “đã mang nhãn … tại chỗ” chỉ đúng với đoạn Issue trong CHANGELOG, chưa đúng toàn bộ bề mặt nó yêu cầu kiểm. Đây vẫn là phần chưa vá của slug đã bị chấm hai lượt, không phải đòi xác minh GitHub offline.

ĐÃ THỬ VÁ: có — trên bản chép thêm THUẬT LẠI và việc thiếu response Issue/log CI ngay ở chú thích và đoạn §2. Giữ số/ID được kể; không biến chúng thành số mới hoặc kết luận Issue không tồn tại. Hướng khóa lỗi là đối chiếu từng vị trí trong danh sách đã tuyên bố vá; không cần đổi runtime hoặc viết cổng ngữ nghĩa mới. Rủi ro cần tránh: một nhãn ở đoạn khác lại bị dùng để che câu tại chỗ.

ĐÃ THỬ NGHIỆM: `git -C cay-kho diff 1d58500 HEAD -- ops/cong_cu.py` → rc=0, stdout rỗng; `git -C cay-kho show --format= --name-only 4d2a6f6` không có tệp mã này. `nl -ba` tại các dòng nêu trên xác nhận câu trần còn nguyên. Bản thử sửa qua doc-claims, bien_nhan_v2, t27 và release-verify sau tái sinh manifest, tất cả rc=0. Giá trị/trạng thái #498 và lượt Windows thật: **KHÔNG ĐO ĐƯỢC**, không mạng/không response.

ĐỘ TIN: cao.

### attestation-runtime-bi-nang-thanh-phep-do  [P2]  Ngoại lệ phép đo tái xuất hiện ngay trong khối runtime của receipt lượt 2

TỆP/DÒNG: `cay-kho/ops/reviews/pr497-review-2-codex-verdict.receipt.yaml:13–15`, `:176–184`; receipt lượt 1:132–139; liên hệ CHANGELOG:182–184 và hai hàng README:273–274 về giới hạn phép khớp tree.

VẤN ĐỀ: Receipt mới nhấn mạnh toàn bộ `model_reviewer_identity` là ATTESTATION, “KHÔNG TRỪ TRƯỜNG NÀO”, rồi trường `neo_danh_tinh_kho` gọi lý do phiên dùng expected-root-commit thay expected-repo là “ĐO ĐƯỢC”. Cấu hình/nhánh chặn có thể đo lại hôm nay; việc phiên cũ đã truyền cờ nào, gặp lỗi nào, vì sao đổi cờ vẫn chỉ được thuật lại từ run.json ngoài kho. Không tách hai đối tượng đó thì câu này tự tạo lại ngoại lệ vừa bị chấm. Receipt lượt 1 cũng còn “Đây là NỢ ĐÃ ĐO” bên trong khối runtime, trong khi CHANGELOG đã hạ cùng chuyện xuống THUẬT LẠI. Ngoài ra, việc OID trong verdict khớp Git xác nhận định danh nhất quán; không tự xác thực hành vi “reviewer đọc đúng cây” như các bản tóm tắt diễn đạt. Không có kết luận reviewer đã đọc sai cây, dùng sai model hay không chạy test.

ĐÃ THỬ VÁ: có — trên bản chép đổi lý do chọn cờ và nợ launcher thành thuật lại; giữ kết quả cơ chế tại chỗ như một phép đo riêng nếu cần. Giới hạn câu khớp tree về đối chiếu định danh trong hai receipt, README và CHANGELOG. Không yêu cầu nhập runtime riêng tư hoặc phóng reviewer mới. Hướng kiểm lại: mỗi trường có nhãn đo được phải trỏ phép đo đúng đối tượng; tránh dùng rc của thử nghiệm mới để chứng thực phiên cũ.

ĐÃ THỬ NGHIỆM: gọi riêng `launcher.chot_kho(str(Path.cwd()), 'ducthangho/tra-luat', None)` trên bản chép, bắt exception để đọc kết quả: `CHAN 11`, `(khong co remote)`; đọc root OID được `394e93468fc8d84ec20938e6df8fb7ab72b2cc37`. Đây là phép đo chức năng hiện tại, không chạy launcher/provider hay xác thực command line lịch sử. Hai đối chứng chỉ lấy OID bằng `git rev-parse <sha>^{tree}`, chép một dòng rồi so lại đều khớp, không đọc nội dung tệp trong tree. Sửa nhãn/giới hạn trên bản chép qua validator, t27, doc-claims và release-verify rc=0. Runtime cũ: **KHÔNG ĐO ĐƯỢC** do thiếu run.json/transcript/prompt.

ĐỘ TIN: cao đối với mâu thuẫn nhãn; không suy ra scalar runtime nào thực tế sai.

### ke-sai-ly-do-reviewer-khong-chay-ls-remote  [P2]  Hai nơi vẫn kể ngược nguyên nhân dù hồ sơ mới khai đã sửa cả bốn

TỆP/DÒNG: `cay-kho/ops/reviews/README.md:18`, `:273`; receipt lượt 1:196–201; receipt lượt 2:99–104. Nguồn: verdict lượt 1:157.

VẤN ĐỀ: Verdict gốc nói đã đo cấu hình thực tế trả URL GitHub, vì vậy không chạy ls-remote trong sandbox không mạng. README:18 vẫn nói reviewer “tin câu sai đó”; receipt lượt 1:197 vẫn gắn kết luận không chạy với việc “đọc câu sai đó”. CHANGELOG và hàng mới của README lại kể đúng, receipt lượt 2 còn khai đã trích thẳng dòng 157 “ở cả bốn nơi”. Người mở hàng cảnh báo được t27 cưỡng chế vẫn nhận lời kể cũ, trái ngay hàng tổng kết ở cùng tệp. Không phải lỗi nằm trong verdict gốc cần sửa băm.

ĐÃ THỬ VÁ: có — thay đúng hai câu trên bản chép bằng “Theo verdict dòng 157, reviewer đo cấu hình thật trả URL GitHub, nên…”. Giữ nguyên cảnh báo 321/321 chỉ là hai tập cục bộ. Kiểm lại bằng đối chiếu cả bốn nơi với nguồn, không chỉ tìm thấy trích dẫn ở CHANGELOG. Tránh thêm suy đoán mới về trạng thái tâm trí hoặc động cơ reviewer.

ĐÃ THỬ NGHIỆM: `nl -ba cay-kho/ops/reviews/pr497-review-1-codex-verdict.md` tại dòng 157, đối chiếu `nl -ba` receipt lượt 1:197 và README:18 → hai câu chưa sửa. `t27` trên cây nguyên vẹn rc=0 dù câu sai còn đó; bỏ hàng cảnh báo thì rc=1. Đây là chốt có mặt của hàng, không kiểm nghĩa. Bản thử sửa qua t27 và bien_nhan_v2 rc=0; doc-claims/release-verify rc=0.

ĐỘ TIN: cao.

### bang-cong-r362-con-neo-so-truoc-bien-nhan-luot-hai  [P2]  Bảng đo cho “cây này” còn 49/102 trong khi HEAD đã là 50/103

TỆP/DÒNG: `cay-kho/CHANGELOG.md:267–271`; đối chiếu `EVIDENCE.md:36–41` và receipt lượt 2 được thêm tại HEAD.

VẤN ĐỀ: Sau phần ghi sổ cả hai lượt, bảng “Đo tại chỗ sau khi vá … tất cả trong cây này” vẫn khai 49 ĐẠT v2/tổng102. Validator trên exact HEAD trả 50/tổng103. Cả hai lần đều rc=0, nên chỉ nhìn cổng xanh sẽ bỏ qua sai số của lời khai. Số 49/102 đúng ở `4d2a6f6`, trước khi receipt lượt 2 vào kho; bảng không neo số ấy về commit cũ. EVIDENCE lần này đúng, CHANGELOG chưa được cập nhật cùng nó.

ĐÃ THỬ VÁ: có — trên bản chép đổi bảng hiện tại thành 50/tổng103 và tái sinh manifest. Cách khác là giữ 49/102 nhưng ghi rõ exact SHA cũ và thêm kết quả HEAD; không nên trộn số của hai cây dưới một tiêu đề “cây này”. Phép kiểm khóa là chạy validator sau khi nhập xong hồ sơ, lấy các scalar từ output cuối. Rủi ro: nhập thêm receipt hoặc đổi prose lại làm số/hash trôi nếu đo trước bước cuối.

ĐÃ THỬ NGHIỆM: `python3 ops/bien_nhan_v2.py --root .` trên bản chép HEAD → rc=0, `50 ĐẠT v2 · 11/11 ... · 42 NỢ ... · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 103`. Checkout `4d2a6f6` ở bản chép lịch sử, cùng lệnh → rc=0, 49/tổng102. Bản thử sửa bảng qua doc-claims và release-verify sau tái sinh manifest, rc=0/0.

ĐỘ TIN: cao.

### phep-grep-prompt-khong-ghim-snapshot-sau-khi-nhap-verdict  [P2]  Lệnh ghi HEAD còn khai một tệp dù verdict mới đã tạo bản chép thứ hai

TỆP/DÒNG: receipt lượt 1:140–145; receipt lượt 2:72–74; `cay-kho/CHANGELOG.md:236`; README:273. Đầu vào mới: verdict lượt 2:179 và :199 có digest được chép lại.

VẤN ĐỀ: Đính chính dùng phép `git grep … HEAD` để khẳng định chỉ chính receipt lượt 1 chứa digest. Kết quả đó đúng trên head được lượt 2 review, nhưng không đúng trên HEAD đang giao: verdict lượt 2 vừa nhập đã chép cùng digest. Nay grep trả hai tệp. Điều này không tạo được hai nguồn prompt độc lập và không bác bài học prompt là ATTESTATION; nó bác con số/lệnh không ghim snapshot đang được dùng để minh họa bài học. Cần phân biệt “một giá trị digest” với “một tệp chứa giá trị ấy”.

ĐÃ THỬ VÁ: có — trên bản chép đổi phép đo lịch sử sang `1d58500`, nêu HEAD có hai tệp nhưng đều là bản chép; cập nhật mô tả ở receipt, CHANGELOG, mục lục. Giữ nguyên verdict đã neo băm. Kiểm khóa bằng chạy cùng truy vấn ở cả hai SHA; rủi ro cần tránh là biến hai bản chép thành hai chứng cứ prompt.

ĐÃ THỬ NGHIỆM: đã chạy truy vấn dưới với cả `1d58500` và `HEAD`, rc=0 cả hai. Bản cũ trả riêng `ops/reviews/pr497-review-1-codex-verdict.receipt.yaml`; HEAD trả thêm `ops/reviews/pr497-review-2-codex-verdict.md`. Bản sửa nhãn snapshot qua validator, t27, doc-claims/release-verify rc=0.

```sh
git -C cay-kho grep -l fd117770fa4c651aad6194d4dfb9adfc51b60ba78a3a9ea4928823799c480c85 1d58500 -- .
git -C cay-kho grep -l fd117770fa4c651aad6194d4dfb9adfc51b60ba78a3a9ea4928823799c480c85 HEAD -- .
```

ĐỘ TIN: cao về số tệp và khác biệt snapshot; không kết luận có thêm nguồn runtime độc lập.

### dem-finding-doi-mau-va-bo-sot-phan-moi  [P2]  Tổng finding bị gọi thành 1→7 và phần mới bị đếm thiếu một

TỆP/DÒNG: `cay-kho/CHANGELOG.md:253–256`; README:273; receipt lượt 2:142–153. Nguồn: hai verdict và lịch sử CHANGELOG tại `e826730`/`52b36d1`.

VẤN ĐỀ: Câu “Số finding tăng 1→7” bỏ P3 của lượt 1: số tiêu đề thực là 0/1/1 → 0/7/0, tức tổng **2→7**. Chỉ số P2 mới tăng 1→7. Cùng đoạn còn nói 5/7 nhắm phần chỉ tồn tại sau lượt 1; ngoài năm được receipt liệt kê, câu “Không cổng nào trong kho…” của slug thứ bảy cũng chỉ được thêm ở `52b36d1`, sau head lượt 1 `e826730`. Theo chính cách phân loại phần bị chấm được viết sau lượt 1, phải tính thêm trường hợp này thành **6/7**. Không dùng số finding đơn thuần để kết luận chất lượng tăng hay giảm.

ĐÃ THỬ VÁ: có — trên bản chép gọi đúng “finding hạng P2 tăng 1→7”, và ghi 6/7 kèm trường hợp thứ sáu trong receipt/mục lục/CHANGELOG. Cũng có thể bỏ tỷ lệ phân loại nếu không cần; nếu giữ thì liệt kê tập và tiêu chí. Kiểm khóa bằng đếm tiêu đề theo từng hạng, rồi kiểm thời điểm xuất hiện đoạn bị chấm. Rủi ro: số P2, tổng finding, số hàng và số bề mặt mới bị dùng thay nhau.

ĐÃ THỬ NGHIỆM: Python `re.findall` với mẫu tiêu đề từng hạng cho lần lượt **0/1/1** và **0/7/0**. `git -C cay-kho log --format='%h %s' -S 'Không cổng nào' -- CHANGELOG.md` trả commit thêm `52b36d1` và commit sửa `4d2a6f6`; đọc CHANGELOG tại `e826730` không có câu ấy, tại `52b36d1` có. Bản sửa cách gọi số và tập sáu trường hợp qua doc-claims, tái sinh manifest, release-verify, rc=0/0/0.

ĐỘ TIN: cao về tổng 2→7 và thời điểm đoạn văn xuất hiện; tiêu chí phân loại sáu trường hợp được nêu rõ để đối chiếu.

## GIỚI HẠN

- Không truy cập mạng. Không đo trực tiếp trạng thái PR/Issue/review, Actions run/job/attempt, quyền người duyệt, landed hay CI trên exact HEAD. URL trong receipt được kiểm phần Git object/path/ancestry, không kiểm khả năng truy cập GitHub. Sự chưa đo được không tự là finding, không là cổng đỏ và không phải yêu cầu đốt CI mới.
- Tệp `ls-remote-may-chu.txt` xác minh được byte/số học; xuất xứ và timestamp vẫn là ATTESTATION. Không có bộ đệm trước fetch hoặc snapshot gói hai lượt cũ. Chỉ gói lượt 3 được đo trực tiếp; không dựng tập theo lời kể rồi nhận đó là snapshot thật.
- Không có run.json, prompt hay stdout/stderr của hai reviewer cũ. Các hồ sơ runtime khác trong cây không chứng thực hai phiên này. Khớp digest/tree hoặc tính hiệu timestamp chỉ xác nhận đúng đối tượng của phép so/tính, không tự xác nhận danh tính/hành vi phiên.
- Đã chạy đủ 12 lệnh EVIDENCE trên Linux, suite lease trước merge, các ca riêng và đột biến được ghi ở bảng. Không chạy toàn bộ 31 bước cổng CI, không chạy Windows, không tái thực hiện ba lối land của hồ sơ #490. Các kiểm tra static CI không được gọi là run GitHub.
- Không tự soạn nội dung tấn công. Chỉ dùng suite/fixture có sẵn và tự đổi số, chữ mô tả, chính sách, điều kiện canary, sự có mặt của hiện vật và các tên ref đã có. Hướng cần nội dung thoát, đồng tự hoặc đường dẫn vượt cây không được bổ sung.
- Các sửa thử chỉ ở bản chép trong sandbox; không áp lên PR, không sửa verdict đã neo băm trong cây thật. Cổng xanh sau sửa prose chỉ xác nhận các chốt đã chạy vẫn đạt. Không đề nghị sửa băm cho qua cổng hoặc tự nâng assurance.
- Phép đo cuối: khối cấu hình EVIDENCE = `do-goi.txt` = cấu hình thực, cả **9 dòng**. Mirror **324**, gồm **323+1**; raw **322** dòng/băm khớp. Không phát hiện lệch cấu hình gói mới. Thiếu nhãn tại chú thích và lời “đã gắn nhãn” được ghi trong finding đầu, không đánh tráo thành lỗi số ref của gói này.
- Sản phẩm mới duy nhất giữ lại là `VERDICT.md`; đã dọn các bản chép, script và log tạm do lượt này tạo. Kiểm cuối `git -C cay-kho status --porcelain`: **rc=0, stdout rỗng**. HEAD vẫn **4e6a2d59386335f966bfb7160e98af02ae30d1ec**. Không sửa `cay-kho/` hoặc `kho.git`.
