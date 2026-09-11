verdict: changes_requested
reviewed_spec_sha256: 43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9
model_tu_khai: OpenAI Codex, qua API/công cụ trong sandbox; cấu hình phiên tự mô tả GPT-6. Tôi không có chứng thực độc lập model/version backend, session identity hay toàn bộ transport; không suy chúng từ tài khoản GitHub.

Review ĐẶC TẢ trước Issue/lease, không phải review mã triển khai. Cần revision trước khi cấp lease; không có approval để thi công theo bản hiện tại. Quy tắc `blocked` của §3.2 áp khi executor đang thi công mà gặp spec thiếu; ở lượt soạn trước Issue này, verdict yêu cầu sửa spec.

Base đã đọc: `b416830ef2a509d60203d55552ce17950afcf67c`; tree `266a2aba97d925dac3ab7473dda55adb0fe23b8e`. Không sửa/commit/push `cay-kho`; không dùng mạng. Mọi kho giả nằm trong `scratch/tmp/` dưới cwd. Chỉ hai tệp kết quả ở cwd là bản này và `HINT.patch`; script/log phụ ở `scratch/`.

`HINT.patch` là gợi ý VÁ CHỮ, không phải mã cổng. Nhãn: **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Đã thử áp bằng `patch -p0` lên bản sao SPEC trong sandbox; việc mở write set/dependency trong hint là đề xuất cho revision, không cấp quyền ghi repository.

## Bảng đo lại

Đo chính lúc **2026-09-07T13:52:30.658239Z**; đọc số liệu lịch sử tại snapshot cố định, đồng thời phân loại hạn ở `13:41Z` và giờ đo. `origin` trỏ bare `kho.git` BÊN TRONG cwd. Bare và cache cùng một bundle không phải hai nguồn có thẩm quyền độc lập về GitHub/độ tươi.

Các lệnh rút gọn trong bảng:

- **D1:** `PYTHONDONTWRITEBYTECODE=1 python3 scratch/measure.py` — quét `git -C cay-kho for-each-ref`, `ls-tree -r`, `cat-file -p`; khử theo `(blob,path)`, parse YAML; output `scratch/measure.json`.
- **D2:** `PYTHONDONTWRITEBYTECODE=1 python3 scratch/more_measure.py` — chạy CLI trên bốn đường, thêm hai lượt launcher, diff các mốc; output `scratch/more_measure.json` và `.log`.
- **D3:** `TMPDIR="$PWD/scratch/tmp" PYTHONDONTWRITEBYTECODE=1 python3 scratch/adversarial.py` — Git bare + working copies thật, MÔ PHỎNG vị từ mới; `scratch/adversarial-results.json`, `.log`, `git-trace.json`.
- **D4:** `TMPDIR="$PWD/scratch/tmp" PYTHONDONTWRITEBYTECODE=1 python3 scratch/loop_routes.py` — state sinh bằng entrypoint thật, thay helper trong bộ nhớ; `scratch/loop-routes.log`.

| Con số khai (SPEC/EVIDENCE) | Con số đo | Lệnh/nguồn phép đo | Khớp/lệch |
|---|---|---|---|
| SHA256 SPEC 64 hex | `43844cb2ea2653f502320a6f35a6e3ae7fd182770f02b62d4d73b9aa8dbea6f9`, bản trong cay-kho cùng băm | `sha256sum SPEC.md cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md` | Khớp |
| base b416830…; core.abbrev 7 | đúng full SHA trên; `7` | `git -C cay-kho rev-parse HEAD`; `git -C cay-kho config core.abbrev` | Khớp |
| 303 ref = 302 remote + 1 local master | 303 = 302 + 1 | D1; `for-each-ref refs/heads` | Khớp. Detached HEAD KHÔNG làm mất ref local master; mirror này có master, không có chênh do local branch |
| 288 cặp blob/path; 273 path; 273 ID | 288 / 273 / 273 | D1 | Khớp |
| 7/273 ID có >1 blob | 7/273; số blob từng ID: 2,2,4,4,5,3,2 | D1 `multiblob` | Khớp; nhiều blob tự nó chưa chứng minh ai sửa/vì sao |
| 8 ID CÒN_HẠN | 8 cả tại 13:41 và 13:52:30 | D1 `now`, `spec_1341` | Khớp |
| 4 ID chưa bia mộ trên ít nhất một ref | 4: gate r4, mutant exec-1, wp461 g2, wp461 r2 | D1 | Khớp |
| gate r4 1 ref; g2 1 ref | 1 (#468); 1 (`ops/lease-wp461-g2`) | `ls-tree <từng ref> -- ops/leases/<ID>.yaml` | Khớp |
| r2 blob 26f07b4… trên 4 ref; fdfde3a… trên 1 ref | 4 + 1 ref; đúng cả hai SHA40 mẫu YAML; tổng chỉ **2 cặp**, 1 path | D1 `special` | Ref khớp. Số dòng A1 không khớp |
| mutant 8b2103c không bia mộ 11 ref; 1f95042 có bia mộ 1 ref | 11 + 1 | D1 | Khớp |
| mutant hết hạn `2026-09-07T14:30:07Z` | đúng trường YAML; còn hạn lúc đo | D1 | Mốc khớp. “Trước khi packet có lease” là dự đoán, không đo được |
| launcher NGƯỜI_GIỮ 2, rc=11, 4,1 s | đúng 2, rc=11; 3,596 / 3,285 / 3,359 s, trung vị 3,359 s | D2, ba output mỗi cái 2217 byte | Hành vi khớp; thời gian khác môi trường/tải, không phải benchmark bản vá |
| 3 đường còn lại, cả 4 đường wp461 đều 2 holder | CHANGELOG 3,528 s; kế hoạch provider 3,491 s; bien_nhan_v2_test 3,319 s; cả ba 2 holder rc=11, mỗi output 941 byte | D2 | Khớp |
| `check` g2 đăng được rc=0 | rc=0, `ĐĂNG ĐƯỢC`; cảnh báo không chạy hai lớp GitHub | `git -C cay-kho show origin/ops/lease-wp461-g2:ops/leases/wp461-be-mat-thu-hai-cua-codex-exec-1g2-claude-20260907.yaml > scratch/g2.yaml`; `python3 cay-kho/ops/lease_publish.py check scratch/g2.yaml --root cay-kho` | Khớp; không phải chứng nhận độc quyền |
| tên ls-remote/cache, comm hai chiều 0/0 | 302 bare heads; thiếu/thừa 0/0, SHA lệch 0 | D1 `local_bare_comparison` | Chỉ khớp NỘI BỘ mirror. Không đo lại được hai nguồn trên GitHub |
| `agent/wp461*` rỗng (hai lần 09:49,13:4x) | 0 head khớp trong bare snapshot | `git -C cay-kho ls-remote --heads origin 'refs/heads/agent/wp461*'` | Khớp snapshot; không tái hiện hai thời điểm nguồn, không chứng minh không có việc chưa push |
| #468 có 28 commit riêng | **31**, master-only 0 | `git -C cay-kho rev-list --left-right --count origin/master...origin/claude/soan-spec-3-viec-treo-20260906` ⇒ `0 31` | Lệch. Ba commit mới nhất 4c18cb2 (12:17:11), 06f6ce3 (12:19:56), 02b0b86 (13:06:21) đều trước giờ soạn; số 28 trong g2 đã cũ |
| 5 cặp bia mộ “đã có trên master”: 3 gate + 1 wp461 + 1 mutant | **7 tệp** mang trường trên master; **0 gate, 0 mutant**. #468 có 11 tệp mang trường, trong đó 3 gate + 1 mutant | D1 `master_tombs`; `scratch/other-counts.json` (parse từng YAML ở hai ref) | Lệch cả tập lẫn ref. 7 tệp mang trường không tự đồng nghĩa 7 cặp hợp lệ |
| commit b416830 một gpgsig; committer web-flow | 1 PGP signature; raw author ducthangho, raw committer `GitHub <noreply@github.com>` | `git -C cay-kho cat-file -p b416830` | Số gpgsig khớp; login web-flow là dữ liệu API, chưa xác minh |
| commit 6635379 “không chữ ký” | **1 SSH signature** | `git -C cay-kho cat-file -p 6635379` | **Lệch, P1 bằng chứng thẩm quyền** |
| `author.login=claude` cho 6635379; author.login chủ kho b416830 | raw author `Claude <noreply@anthropic.com>` / `ducthangho`; Git không có trường login API | cùng lệnh cat-file | Không đo được login GitHub; không đánh đồng raw author với account được xác thực |
| `%G?` b416830 = E | E khi dùng keyring rỗng sandbox | `GNUPGHOME="$PWD/scratch/gnupg" git -C cay-kho show -s --format='%H %G?' b416830` | Khớp trong điều kiện keyring rỗng; không xác minh chữ ký |
| 5 run 372–376, actor ducthangho 5/5, “5/5 do agent push” | Không có API facts Actions trong Git | Không gọi mạng/MCP | **Chưa đo**; actor ngay cả đúng cũng không chứng minh tác nhân người/agent |
| HTTP 403, 249 byte khi lấy khóa web-flow | Không đo lại | Không gọi curl vì cấm mạng | **Chưa đo**, không dùng làm bằng chứng hiện trạng môi trường này |
| comment 5569885143/Issue 461 và PR 474 làm căn cứ | ID/URL có trong spec; chưa có readback `user.login`, body, object ID | Không gọi API | **Chưa đo thẩm quyền/nội dung**; URL được chép không phải bằng chứng |
| _kiem_bia_mo 595–617; any ở 606–610 | đúng các dòng; AST ghi 595–617 | D1; `sed -n '595,617p' cay-kho/ops/lease_publish.py` | Khớp |
| kiem không gọi _lease_cham_duong; 0 lần | 0 call trong AST hàm kiem, dòng 787–890 | D1 | Khớp |
| lớp comment mutable 797–811; actor 833–839 | đúng vùng giải thích/chốt, phụ thuộc code base | `sed -n '787,845p' cay-kho/ops/lease_publish.py` | Khớp vùng dẫn; không chứng minh actor thật |
| quét ls-tree -r; workflow lọc 2 mẫu yaml/yml | đúng; `ops/thu-hoi/` không kích hoạt hiện tại | đọc _quet và `.github/workflows/ops-publish-lease.yml` | Khớp; hệ quả admission bị bỏ sót |
| bốn lệnh Q5 “mọi lệnh đi qua” helper | begin-attempt 1 call; record-post/review/transition **0/0/0**; record-lease 1 | D1 AST; D4 hành vi | Lệch phạm vi chốt |
| sổ hôm nay 0 tệp, sau di trú 1 | 0 tại origin/master; 1 là kế hoạch | D1 `registry_files` | Hiện trạng khớp; chưa triển khai 1 |
| 1 ls-tree + N cat-file, thêm 0 mạng | là dự toán, chưa có mã mới; các kiểm authority/history/default không được dự toán đủ | đọc Q2/Q4/A8 | Không có phép đo implementation; không chứng nhận chi phí |
| 5 tệp write set | đúng 5 đường exact trong spec cũ | đếm khối write_set | Khớp cú pháp; thiếu admission wiring |
| sensitive ≤3 tệp, ≤300 dòng thêm | đúng ADR-0044 | đọc `docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md` | Khớp luật; vượt một ngưỡng đã cần xử lý |
| +450±100; thành phần 120+220+40+60+20 | cộng =460; A=360/3 tệp; B=100/2 tệp | `sum([120,220,40,60,20])` | 460 trong khoảng 350–550, không phải sai cộng; nhưng A vẫn vượt 300 và phạm vi bị thiếu |
| LEASE-HOI-TOAN-KHO “PR #250: 2 tệp/+313” | #250 = **2 tệp SPEC/+409**; mã land #275 = **2 tệp/+368** | `git -C cay-kho diff --numstat 2854380^1 2854380`; cùng lệnh `7883aad^1 7883aad` | Lệch packet/mốc/số |
| PLAT-X8 2 tệp/+265→+313 | hai mốc 08bb4ecd..67a7fbe0 =82+183=265; ..86a55663 =93+220=313; xóa1 cả hai | `git -C cay-kho diff --numstat 08bb4ecd 67a7fbe0`; tương tự 86a55663 | Khớp mốc trung gian; cuối #248 =89+239=**328**, xóa1 (647cfea^1..647cfea) |
| test lease 121 hàm t; nền120/121, t33 đỏ | 121 AST defs; **120/121**, executed121, skip0, rc1, output **9027 B** | `TMPDIR="$PWD/scratch/tmp" PYTHONDONTWRITEBYTECODE=1 python3 cay-kho/ops/lease_publish_test.py > scratch/lease-suite.log 2>&1` | Khớp. Không cài actionlint, không chạy wrapper tải mạng |
| packet-loop 4733 dòng; nền278/278 TỔNG ĐẠT | 4733 dòng; **278/278**, skip0, **81 mutants**, tổng ĐẠT, rc0, output **8752 B** | lệnh tương tự với `.claude/dev/packet_loop_test.py`, log `scratch/loop-suite.log` | Khớp; 81 là số bổ sung tự đếm, không phải số tác giả khai |
| doc-claims-check strict rc0 | rc0, `ok:true`, 106 tệp, flags0, advisory367 | trong cay-kho: `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --strict --json` | Khớp rc/positive evidence; không quét SPEC mặc định |
| doctrine-scan 7 tệp,0 chỗ,rc0 | đúng 7/0/0; thêm SPEC bằng --path ⇒8/0/0 | trong cay-kho: `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; D2 thêm `--path` | Khớp; scan chuỗi không chứng minh toàn bộ spec tuân luật |
| A1 ≥4 dòng r2; blob mutation để lọt26f07b4 | **2** cặp r2; cả hai blob đã có trong known-list nên mutant vẫn thu hồi đủ2 | D3 `a1-cardinality-mutant` | Lệch đơn vị; mutant nêu không tất yếu đổi màu |
| A2 3 ref ⇒3 dòng | cùng blob ở ba ref ⇒**1 dòng/cặp** | D3 `q1-control-a2` | Lệch đơn vị |
| A8 sửa một record ⇒1 dòng git log | **7 dòng**, 5 không rỗng, chỉ1 dòng là path; merge bỏ record ⇒**0 dòng** | D3 hai ca a8 | Lệch; cổng còn bị bỏ qua |
| A6 2×,3 lần; A3 5 ca; A7 7 ca; A9 5 ca; A10 4 ca | là ngưỡng/số nhánh fixture **được liệt kê**, không phải ca đã chạy | đọc từng A; D3 chỉ đo một số phản chứng | Không giả làm số nghiệm thu implementation |
| A1–A12, M1–M8, Q1–Q9; revision1, schema1, SHA40/64, rc0/4/8/11/12; RC_STATE | đúng 12/8/9 mục gốc; version/mã/độ dài là hằng hợp đồng; RC_STATE=8 trong packet_loop | đọc SPEC + constants/parser | Định nghĩa, không phải lời khai thực nghiệm về mã mới |
| hình dạng2 (wp461,#456);2 lời khai hội tụ;1 bất đồng cổng | hai nhóm blob hiện có; hai commit sửa lời khai `3c4c587`, `ddb3200` có thật; bất đồng check/holder tái hiện bằng0/11 | D1,D2; `git show -s --format=%s 3c4c587 ddb3200` | Đủ tái hiện hai hình dạng đầu ở Git. Con số **1** lịch sử check0/ai12 và “hai ngày” chưa có biên nhận API độc lập; không thay0/11 thành0/12 |
| “timeout hỏng3 lần”; thời gian/source13:2x–13:4x,09:49; ID Issue/PR/run/session | Không đo được tần suất workflow/causal history từ snapshot Git này | không đọc transcript, không mạng | Định danh/mốc lời khai, không suy là đã xác thực; các hash/commit có thể kiểm bằng Git đã kiểm riêng phía trên |

## Findings

### authority-signature-evidence-false · P1 · Q2, EVIDENCE

**TÁI HIỆN:** `git -C cay-kho cat-file -p 6635379` in `gpgsig -----BEGIN SSH SIGNATURE-----`; D1/D2 xác nhận đang ở đúng b416830. `b416830` có PGP signature, không cùng loại. Git chỉ ghi raw author/committer, không có `author.login`.

**Vì sao:** “agent không chữ ký” là con số/hiện trạng sai ở chính bảng chống đỡ lập luận thẩm quyền, theo thang P1 của yêu cầu. Có chữ ký, chữ ký hợp lệ, account ký, và người/agent thao tác là bốn kết luận khác nhau. Chữ ký SSH này không bác giới hạn PAT, nhưng bảng đo hiện tại không được giữ nguyên.

**GỢI Ý VÁ:** thay hàng 6635379 bằng “author/committer Claude; có một chữ ký SSH; chưa xác minh người ký”. Tách raw Git khỏi API login/Actions chưa readback. Không nói comment tự gõ bằng cùng account là mạnh hơn về human identity. Hint sửa Q2/Q8. Ca khóa: raw commit fixture có SSH/PGP/không signature và không suy login từ author. Rủi ro: siết chữ ký web-flow sẽ chặn tác nhân hợp lệ; hint không thêm chốt chữ ký đó.

### default-ref-is-untrusted-cache · P1 · Q1, Q4, A2/A6/A7

**TÁI HIỆN:** D3 `q1-symref-authority`: bare HEAD=`refs/heads/master`; sau `git symbolic-ref refs/remotes/origin/HEAD refs/remotes/origin/ops/fake`, so toàn bộ `(tên,SHA)` vẫn equal; holder `[X]→[]`, `check_Y=0`. Ca `q1-fallback-revived`: bare đổi default thành main có event X; xóa symref local, vẫn giữ master cũ ⇒ resolver chọn master, holder `[X]`.

**Vì sao:** `ls-remote --heads` không xác thực symref HEAD. Hai luật “chỉ nhánh mặc định” và “tin origin/HEAD local, vắng dùng master” cho kết quả trái nhau. Đây là cả nhận record không thẩm quyền lẫn đếm lại lease đã bị thu hồi; không cần SHA cache nào sai.

**GỢI Ý VÁ:** “Đọc default từ nguồn canonical đã xác minh; cache phải khớp; vắng/khác/không xác minh được ⇒12, không fallback tên master.” Dùng một `ls-remote --symref` gồm HEAD và heads nếu giữ số lời gọi mạng; ghim nguồn repo. Hint Q1/Q4/A2/A6. Ca khóa: hai ca trên và default không phải master, symref dangling. Rủi ro: clone thiếu metadata bị chặn thật, cần bootstrap rõ; không tha để giữ availability.

### standalone-revocation-has-no-admission-gate · P1 · Q2.2–3, M4, ngoài phạm vi workflow

**TÁI HIỆN:** D3 `q2-no-admission`: commit record X tự khai owner, `can_cu` tới object không có, đưa vào default ⇒ holder `[]`, `check_Y=0`, số lần online trước hiệu lực **0**. Workflow hiện chỉ push `ops/**` và `ops/leases/**.yaml/.yml`; không nhận delta chỉ `ops/thu-hoi/`. `kiem-github` hiện có đường rc9 bỏ lease đã đăng.

**Vì sao:** reader quyết hiệu lực ngay khi thấy record, còn kiểm online phụ thuộc một lease mới về sau. Thu hồi không cấp lại có thể không chạy kiểm online bao giờ. Merge được không đồng nghĩa record được chính owner cấp lệnh; YAML `thu_hoi_boi` không xác thực account tác giả. Ca dùng Git hợp lệ và các điều kiện cổng đã viết; không giả định đã vượt branch protection GitHub thật (chưa đo được). Nếu định tin default như biên đã kiểm authority, spec phải định nghĩa/cưỡng chế biên ấy trước hiệu lực.

**GỢI Ý VÁ:** thêm entrypoint admission cho mọi delta thu hồi, dùng mã canonical và exact candidate/base; wiring bắt buộc vào workflow và kiểm required-check/khả năng bypass trước kích hoạt M5. Bao phủ standalone, cập nhật record và rc9 của lease. Hint Q2/M4/M9/write_set/A9/A11/Q10; workflow thành tệp thứ6, hoặc slice predecessor rõ. Ca khóa: fake API trace bằng0 phải đỏ; record giả không bao giờ có hiệu lực trước admission. Rủi ro: cần thêm scope/điều kiện ngoài kho; không gọi đó là nợ thông báo comment.

### evidence-mention-is-not-an-authorization · P1 · Q2, lược đồ can_cu, A9, Q8

**TÁI HIỆN:** D3 `q2-substring-not-command`: object owner, body `Do not revoke X; keep X active.` ⇒ online rc0. `q2-unrelated-prefix`: body `Revoke X-extra` ⇒rc0 với X. Cả hai đúng luật “account allowlist + thân chứa lease_id”. Chưa có body/user của comment5569885143 để đo M5 thật.

**Vì sao:** đọc được tác giả object không đồng nghĩa object chứa lệnh cho event ấy. Spec cũng không neo URL vào đúng repository/Issue/object ID, không ràng buộc `cap_lai_cho` và không định nghĩa comment bị sửa sau thu hồi. Q8 đề xuất “comment + PR” trong khi schema chỉ có một URL; bản chiếu qua workflow thường do bot đăng, phải readback account thật chứ không đoán owner.

**GỢI Ý VÁ:** một object URL cùng repo; block lệnh có schema, event/ID/Issue/đích và nội dung record khớp chính xác, không substring. Readback byte/ID trước admission, lưu hash/receipt; sau khi đã tiếp nhận, sửa/xoá API object không hồi sinh lease. Q8 chưa có object đạt thì chưa ghi M5. Hint Q2/Q8/A9/schema. Ca khóa: phủ định, tên chỉ là tiền tố, sai repo/Issue, sai đích, body sửa, duplicate block. Rủi ro: căn cứ cũ có thể không hợp schema; cần lệnh mới, không tự nhận lời kể tương đương.

### write-set-exclusion-is-incomplete · P1 · Q3, A5, ngoai_pham_vi

**TÁI HIỆN:** D3 `q3-no-replacement-scope`: đã có Y/Z giữ p, W không khai thay thế ⇒`check_W=0` như A5 yêu cầu. `q3-prefix-overlap`: W giữ `docs/`, Y thay X xin `docs/a.md` ⇒0. `q3-casefold-overlap`: W giữ `README.md`, Y xin `readme.md` ⇒0. Hai ca sau dùng đúng `_lease_cham_duong` thật mà spec đề xuất dùng chung; hàm này chỉ so chuỗi bằng nhau.

**Vì sao:** §5 yêu cầu giao canonical exact/prefix, case-fold và effective-write-set exclusion toàn kho. Giới hạn `thay_the_cho` không phải hàng rào ngăn một lease khác xin cùng p; A5 còn khóa regression vào hướng cho qua. Không có phạm vi hẹp nào đủ chống “hai lease cùng đường” nếu chỉ đổi trường thay thế là tắt chốt. Giao đường không chỉ là mỗi chuỗi write_set có bằng chuỗi khác hay không.

**GỢI Ý VÁ:** áp phép đo giao cho mọi lease, dùng biểu diễn/chuẩn hoá §5; không suy write_set không đọc được thành rỗng. Đổi ca không-thay-thế từ0 thành11; thêm prefix/case-fold/malformed cùng đối chứng không giao. Hint Q3/M3/A5. Các hướng thoát cây/đồng tự/chuỗi thoát chỉ mô tả bằng lời để điều phối dựng. Rủi ro: thêm chốt sẽ chặn các hồ sơ legacy malformed; phải khai12 và lộ hồ sơ, không im lặng bỏ.

### snapshot-check-does-not-fence-writers · P1 · Q3, Q5.1–3, slice A, §3.2/§4/ADR-0028

**TÁI HIỆN:** D3 `q3-concurrent-replacements`: X đã thu hồi, cap_lai_cho trống; hai clone có ứng viên Y/Z cùng p. Hai phép `check` trước publish trả **0/0**; push hai branch hợp lệ rồi fetch ⇒ holder **[Y,Z]**. Đây là phản chứng cho lời hứa chung của `check`, KHÔNG là lời khai đã tái hiện hai job workflow sau-push cùng qua trên GitHub. Thêm vào đó, Q5 tự khai packet-loop không fetch và land chưa có consumer; D4 cho thấy chốt nội bộ cũng không phủ mọi route.

**Vì sao:** quan sát snapshot không phải acquire nguyên tử, không dừng process/binary cũ và không fence heartbeat/push/handoff/land. Câu “không tồn tại cửa sổ hai lease ĐĂNG ĐƯỢC” và “A gỡ cửa sổ hai writer” vượt write set (L2). Nhánh `agent/wp461*` rỗng chỉ đo refs khớp mẫu, không đo uncommitted/unpushed work. Nợ land chưa làm không thể gọi “chốt có răng thật”.

**GỢI Ý VÁ:** định nghĩa rc0 là kết quả snapshot; trước start phải có lease trên server, readback holder và cấp/start được tuần tự hóa bởi authority bền. Dừng/retention worker cũ, generation mới theo §4/ADR-0028; tự động takeover cần dependency fencing thật. Slice A chưa đủ bật M5/start wp461. Hint Q3/Q5/Q7/Q11/A5. Ca khóa: hai candidate đồng thời, cache/binary cũ, old process tiếp tục, snapshot đã cũ không cấp quyền start. Rủi ro: muốn giữ bảo đảm máy tuyệt đối phải mở packet/dependency ngoài năm tệp, không thể chữa bằng một dòng kiểm `check`.

### reads-are-not-pinned-to-one-snapshot · P1 · Q3/Q4, A6

**TÁI HIỆN:** D3 `q4-snapshot-move`: so hai nguồn equal; dùng `git update-ref` đổi `refs/remotes/origin/master` sau phép so về commit trước thu hồi (object đã có); lookup theo refname thấy registry `[]`, trong scan vẫn có X. Đây là thay cache trong lúc đo, không phải lỗi SHA ở thời điểm so ban đầu. Ca đối chứng `q4-stale-sha-control` với SHA đã cũ ngay từ đầu bị chặn rc12.

**Vì sao:** spec ghim “đúng một ref”, chưa ghim object SHA cho toàn lượt. `ls-tree`/lookup tiếp theo có thể dùng một cây khác cây vừa chứng minh tươi, hoặc mix holder/sổ qua hai mốc. So SHA một lần rồi đọc tên trôi không sửa được TOCTOU bên trong lệnh.

**GỢI Ý VÁ:** capture map ref→SHA40/canonical SHA và thời gian một lần; mọi đọc trong lượt dùng OID, lỗi object12; log receipt ghi snapshot. Hint Q4/A6. Ca khóa: mutate ref sau so, thiếu blob sau so, tên ref không đổi nhưng SHA đổi. Rủi ro: snapshot vẫn chỉ đúng ở thời điểm quan sát, không giải quyết acquisition/race ngoài lệnh (finding trước).

### legacy-fallback-conflicts-with-ledger · P1 · Q3/Q6, A3/A4

**TÁI HIỆN:** D3:

- `q6-legacy-old-copy`: canonical có X→Y hai chiều nhưng ref cũ còn blob X trước bia mộ ⇒ holder `[X,Y]`, checkY=**11**, trong khi A3(d) hứa0.
- `q6-fallback-overrides-reservation`: sổ X chỉ cấp cho Z, canonical đồng thời có X→Y ⇒ checkY=**0**, A3(c) đòi8. Vế OR cho vượt hạn chế sổ.
- `q6-republish-legacy-dead`: Y chết qua bia mộ canonical Y→Z, không có sổY ⇒ checkY=**0**, holder chỉZ. Chiều ngược chỉ kiểm sổ nên đăng lại lease đã chết.

Bảng Q6 còn ghi nhầm 3 gate+mutant ở master; phép đo thực là0/0 tại master, có trên #468.

**Vì sao:** “giữ nguyên phân loại theo blob”, “chỉ một thay đổi với lịch sử”, “sổ đặt đích” và các rc nghiệm thu không đồng thời đúng. Bia mộ “mới không nhận, lịch sử nhận” cũng thiếu cutoff/định danh lịch sử, nên executor phải tự quyết một record tạo ngày mai là lịch sử chưa.

**GỢI Ý VÁ:** sổ có precedence tuyệt đối, không fallback khi record tồn tại mà từ chối. Cặp lịch sử hợp lệ phải neo canonical/cutoff/blobs, kiểm hai chiều, áp toàn ID nhất quán giữa hai cổng; chiều ngược dùng cùng trạng thái chết. Hoặc giữ theo blob nhưng phải hạ lời hứa A3(d) và di trú trước. Hint chọn phương án đầu ở Q3/Q6/A3/A4, khai tác động thay đổi compatibility. Ca khóa: ba ca trên, chuỗi/vòng và bia mộ sau cutoff. Rủi ro: lease gate ở feature không còn được coi là thẩm quyền canonical; phải đo lại holder thay vì giấu khác biệt.

### append-only-check-misses-candidate-and-merges · P1 · M1/M6, A8

**TÁI HIỆN:** D3 `a8-normal-modification`: một commit M cho record, chính lệnh A8 in **7 dòng**, không1. `a8-merge-erases-registry`: giữ branch từ trước event, trên branch đó `git merge -s ours master`, push fast-forward kết quả vào default. Commit thu hồi vẫn là ancestor; cây mới mất X.yaml; **`git log --diff-filter=MD --name-only origin/master -- ops/thu-hoi/` có0 byte/0 dòng**, holderX sống lại. Full vector lệnh/OID/rc ở `scratch/git-trace.json`.

**Vì sao:** append-only là bất biến nêu bằng chữ, không có cổng runtime/admission được định nghĩa. `git log` có path simplification và mặc định không hiển thị diff merge theo nghĩa cần đo. Chỉ quét origin/master trong PR còn bỏ hoàn toàn sửa/xoá trên candidate chưa merge. Vì vậy ca có thể hiện diện mà không đo mutation của ứng viên; chuỗi trên vi phạm bất biến mong muốn nhưng đi qua phép nghiệm thu đã chỉ định.

**GỢI Ý VÁ:** cổng nhận candidate T so map đường→blob với canonical S đã xác minh; mọi record cũ phải nguyên vẹn; thêm phải valid; thiếu object/base/history12. Chạy trước MỌI cập nhật default, kể cả FF merge có S ở cha thứ hai. A8 dùng tập path/blob và rc; không đếm metadata log, không skip vì chỉ không thấy thư mục .git. Hint Q2/M1/A8. Ca khóa: M/D/rename, tree result merge, candidate chưa land, shallow/missing object, thêm mới hợp lệ. Rủi ro: phải phân biệt sửa draft trước tiếp nhận đầu tiên với sửa record đã canonical; kiểm mọi ancestor không phân biệt sẽ chặn oan draft.

### packet-loop-guard-is-partial-and-boolean · P1 · Q5.1/M7/A10

**TÁI HIỆN:** D4 tạo state bằng init/record-lease/begin-attempt thật; thay `_kiem_luoc_do_lease` trong bộ nhớ thành luôn RC_STATE; sau đó record-post=**0**, transition=**0**, record-review=**0**, state cuối **accepted**. Ba hàm đó không gọi helper. D3 `q5-existence-boolean`: default commit tồn tại, chỉ blob record thiếu trong object store kho giả; `git show` rc=**128**. Cách cài hỏi tồn tại bằng boolean rc (được Q5 mô tả nhưng không cấm) trả guard0, coi “không đọc được” như “không có”. Đây là mô phỏng lỗ spec, không gán lỗi mới cho mã chưa viết.

**Vì sao:** A10 chỉ thử begin-attempt nên không bắt được ba đường đã bypass helper. Q5 không chỉ định root (helper chỉ nhận lease và rc; state-dir có thể ngoài repo), không định nghĩa persist stale trước exception, idempotency/history, và chỉ fail-close rõ cho default vắng. Một record hỏng/không đọc được cần chặn, không phải absent. M7 thêm câu hỏi vào helper hiện tại chưa đủ hứa bốn entrypoint.

**GỢI Ý VÁ:** guard chung explicit root/state/snapshot ở cả record-lease và bốn route nêu; validate đầy đủ như reader, ba trạng thái. Revoked ⇒ lưu stale+event neoSHA/blob rồi RC_STATE, unknown⇒RC_STATE+KHÔNG ĐO ĐƯỢC không giả event, không tiêu lượt/comment. Hint Q5/M7/A10. Ca khóa: từng entrypoint ở state hợp lệ, failed read, YAML/schema error, root≠cwd, repeated calls và failure to save. Rủi ro: nhiều fixture nền trơ chưa có Git phải cập nhật hợp đồng, không thêm skip làm suite xanh.

### acceptance-confuses-refs-blobs-and-mutations · P1 · A1/A2/A7/A11/A12

**TÁI HIỆN:** D3 `a1-cardinality-mutant`: đúng r2 ở mirror chỉ **2** cặp; A1 yêu cầu≥4 dòng một-dòng/mỗi-cặp không thể xanh với reader đúng. Cả 26f07b4 và fdfde3a đã ở `blob_da_biet_luc_ghi`; mutant dùng danh sách blob vẫn thu hồi **2/2**, không để26f07b4 giữ như lời spec. `q1-control-a2`: cùng blob trên3 ref, sau event đúng1 dòng/cặp, A2 đòi3.

**Vì sao:** mẫu phải tách cặp/ref và có một blob CHƯA biết mới giết được mutant theo blob. “Hoặc0 nếu g2 đã land” còn trái bài học lease không tự chết khi land. Sau hết hạn, bỏ loader không nhất thiết đổi holder2; cần assertion nhãn và fixture clock cố định. A7 `raise→continue` có thể cho11 khi X vẫn giữ, không tất yếu0. A11 delta0 không đồng nghĩa N/N khi nền t33 đang đỏ; A12 chỉ byte/tổng không khóa sự vắng mặt của ca.

**GỢI Ý VÁ:** synthetic fixed clock với ít nhất3 blob, known-list thiếu1; assert exact set ID/cặp và map ref riêng; thêm mutant mất nhãn/mất dòng; smoke kho thật không thay ca. Land≠hết hạn. Report tập ca đã chạy/skip/failed, registered/executed và positive evidence theo A11/A12; không quy tất cả mutant về rc0. Hint thay A1/A2/A7/A11/A12. Rủi ro: ép số động của kho thật làm hard threshold sẽ tiếp tục trôi; đừng “sửa code in trùng” chỉ để đạt4/3 dòng.

### revocation-schema-and-error-contract-incomplete · P2 · M1, Q3/Q4, A7

**TÁI HIỆN:** đọc block schema/A7 bằng `sed -n '280,348p' SPEC.md`; chỉ có ví dụ YAML và7 ca. Q3 vị từ không nêu schema/authority; Q4 gọi safe_load và liệt kê ít lỗi; packet-loop chỉ hỏi file có tồn tại. Đọc mã nền `_doc_yaml` và `_quet_lease_toan_kho`: safe_load không tự kiểm schema/domain/type hay từ chối duplicate key.

**Vì sao:** chưa đóng type/missing/duplicate-key, version/event, trường cap_lai_cho sai kiểu/null/self, format của các SHA advisory, mode/path của Git entry, clock lỗi, và precedence khi nhiều lỗi. ISO có Z có thể được YAML parse thành datetime nếu không quote. Executor phải tự thiết kế cách coi malformed record là8/12, bỏ qua hay thu hồi. Không có code mới để tôi đo đầy đủ parser tương lai; đây là finding thiếu hợp đồng, không khai đã khai thác tất cả dạng.

**GỢI Ý VÁ:** mô tả parser/type/domain/allowed keys/error precedence đầy đủ, không bool-as-int/truthiness; validate một lần, dùng chung qua consumers. Root mapping, duplicate key cấm, regular blob/path exact, chỉ absent khi đọc thành công tree; entry sai phải chặn. Hint phần M1/A7/Q4. Ca khóa: mỗi ràng buộc một lỗi duy nhất và đối chứng; các payload lớp bị cấm chỉ giao điều phối bằng lời. Rủi ro: schema strict có thể chặn dữ liệu mẫu cũ; phải sửa mẫu trước M5, không nới parser ngầm.

### size-estimate-and-slice-anchor-are-stale · P2 · write_set/kích thước/Q7, §0/Q1/Q6

**TÁI HIỆN:** D2 `diff --numstat 2854380^1 2854380` ⇒239+170=**409** (hai spec), không +313 mã. #275 ⇒149+219=**368**. PLAT-X8 final #248 ⇒89+239=**328**, không mốc trung gian313. Ước tác giả A=120+220+20=**360**, B=40+60=100. #468=31 private commits, không28; master tombs sai tập như bảng đo.

**Vì sao:** 460 xấp xỉ450 không phải lỗi số học. Lỗi là dùng mốc sai/giữa kỳ chống đỡ estimate, đếm A1–A9 dù còn A10–A12, không tính wiring/snapshot/admission và tưởng tách3tệp làm A dưới trần. A không tự đủ cho thu hồi vận hành khi admission/fencing chưa có; sửa1test ở220dòng cho nhiều nhóm negative/mutants là dự toán thấp, chưa có diff để khẳng định một con số chắc khác.

**GỢI Ý VÁ:** sửa số/mốc; ước lại từng module, case group/mutant/wiring; ghi ngoại lệ riêng cho A nếu vẫn>300. Tách capability đọc/kiểm (không M5), guard, admission wiring, activation theo dependency đã land; mỗi slice acceptance riêng. Hint write_set/Q7, Q1/Q6. Ca khóa: numstat trước review, map mục tiêu→write set và readiness deployment. Rủi ro: tăng scope không còn hợp lease/spec cũ; phải revision trước xin lease.

### ready-and-rollout-decisions-are-not-closed · P2 · chua_do_duoc6, Q7–Q9, §3.2/§5/L2

**TÁI HIỆN:** workflow hiện dùng checkout@v4 depth0, bước neo fetch default; bundle không có mã action/runner receipt để chứng minh remote refs thực được nạp đủ. Spec6 chính nó dự kiến executor phải sửa workflow ngoài write set rồi revision. `git cat-file -p b416830` ghi miễn trừ bốn trường phái sinh **chỉ wp461 r2 generation1**; không phải miễn chung cho packet này. Q7–Q9 không chốt admission, closure/generation/retention hay pre-start fence.

**Vì sao:** spec đang đóng băng trước lease nên không đòi đã có số Issue hôm nay, nhưng phải đóng đủ hợp đồng trước thi công để executor không tự mở scope. “Cổng cưỡng chế trường phái sinh ngoài phạm vi” không đồng nghĩa nghĩa vụ điền/neo những trường của chính packet được miễn. Predecessor slice phải được nhận trên integration theo §5/ADR0044, không chỉ mọc trên PR đang mở.

**GỢI Ý VÁ:** mở scope workflow trong revision hoặc làm dependency admission đo xong trước activation; thêm Q10/Q11/Q12 cho cơ chế thu hồi có thẩm quyền, dừng worker/cấp lại tuần tự, ready facts/closure/base/checks. Những yêu cầu bắt buộc theo luật không trình như lựa chọn “có tuân hay không”. Hint mục ready cuối + chua_do_duoc6. Ca khóa: wiring trên đúng event/ref/candidate, thiếu default/cache/required-check dừng, no inherited exemption. Rủi ro: chưa có bằng chứng ngoài kho thì activation vẫn blocked; ghi rõ thay vì “đã gỡ cửa sổ” bằng dự định.

## Phản chứng đã thử

Tất cả dưới đây là **Git thực + mô phỏng luật mới**, không phải chạy implementation thu hồi (chưa có). `scratch/adversarial.py` import parser/scan/matcher/bia mộ nền thật; thêm hàm registry/check theo câu chữ spec. JSON trace giữ từng lệnh Git/rc/output/OID. Một diễn giải permissive mà spec chưa cấm đủ chứng minh cần đóng hợp đồng, nhưng không được suy mọi implementation tương lai đều sẽ hỏng giống nhau.

| Câu | Đã thử và kết quả | Loại kết quả |
|---|---|---|
| Q1 | Sổ feature bình thường không thu hồi X; merge vào default thu hồi được mọi bản sao cùng blob. **Không dựng được phản chứng** với default chính xác, snapshot ổn định và record hợp lệ. Đổi symref local hoặc thiếu symref khi default main thì phá được. | control tốt; (b)/(c)/(d) ở resolver |
| Q2 | Standalone record được tính trước online; owner object phủ định vẫn qua substring; ID dài chứa ID ngắn vẫn qua. Không giả credential/PAT, không thử GitHub thật. | (c), unknown admission trở thành hiệu lực |
| Q3 | A5 không-thay-thế buộc cho qua; prefix/case-fold lọt matcher cũ; hai ứng viên kiểm trước publish cùng0, cuối hai holder. | (a); không khẳng định race đã lọt workflow GitHub sau-push |
| Q4 | Static name/SHA mismatch bị12 — **không dựng được** bypass cho chính phép so đầy đủ tại một thời điểm. Ref trôi giữa so và lookup gây mix snapshot; record canonical đúng ID thì áp toàn ID loại đủ mọi blob. | (b)/(d) ở đọc tên trôi; control fail-close hoạt động |
| Q5 | Entry points cũ bypass helper đã bị chặn; missing blob với default tồn tại làm boolean-existence cho qua. Cache/binary cũ được spec thừa nhận; chưa thử cancellation/land thực vì ngoài môi trường. | (d), guard không phủ quyền sau begin |
| Q6 | Bia mộ canonical vẫn để bản cũ giữ; OR vượt cap_lai_cho; lease chết bằng bia mộ vẫn check0. Merge mất sổ qua A8 khôi phục holder X. | (a)/(b), precedence sai |

Chuỗi A8 không tuân BẤT BIẾN append-only mong muốn; nó tuân các thao tác Git hợp lệ và **qua cổng A8 được spec chỉ ra**. Chính khoảng cách giữa câu tuyên bố và phép cưỡng chế là phản chứng, không phải lập luận rằng xóa vẫn là append-only.

Không dựng các payload đường thoát cây, đồng tự Unicode hoặc chuỗi thoát. Chỉ đề nghị điều phối dựng các lớp này trong ca schema/path/normalization. Không đọc transcript để suy danh tính/tác nhân.

### Nhất quán với luật và kích thước

| Nguồn | Kết luận |
|---|---|
| Protocol §3.2; ADR0025 | Có thể đóng băng draft trước Issue như user yêu cầu; trước ready phải có neo/hash/closure/phái sinh bởi authority. Miễn trừ wp461r2g1 không lan truyền. Đổi scope/acceptance sau review phải revision; không để executor tự thêm workflow. |
| §4; ADR0028 | Ledger loại holder không tự tăng/fence generation, không tự cancel process, giữ lastSHA/journal/retention. Land không làm lease tự chết. Cần chặn activation khi chưa có điều kiện dừng worker/readback. |
| §5 | Exclusion toàn repo và canonical exact/prefix, không chỉ exact string hay chỉ lease thay thế; nối tiếp phải dựa predecessor đã integrated, không PR chưa merge. |
| §12 | Không mở PR/slice để né finding cắt ngang authority. A cũ phụ thuộc admission/fencing nên chưa là slice tự đủ cho “thu hồi/cấp lại vận hành”. Dữ liệu hình dạng có giữ, nhưng phải tách số có phép đo khỏi lời kể lịch sử. |
| §8 | Vai review độc lập/read-only phù hợp; patch chỉ chữ spec, không patch runtime authority. Số đo/hash/rc/byte dương có trong review này. Không chứng thực model identity bằng tài khoản đăng. |
| ADR0044 | 3tệp không đủ nếu>300 dòng; A cũ 360. +450±100 không đo được như diff, mốc #250 sai. Có thể xin ngoại lệ có scope hoặc tách với dependency/acceptance riêng, không cắt tests. |
| CLAUDE — allowlist | Chốt provider trước/allowlist sau và mutant nới ai-codex-bot đúng ý; phải có control đủ schema và admission thật, không chỉ field tự khai. |
| CLAUDE — có MẶT≠có ĐO | A8 quét default thay candidate, A10 thiếu ba route, A1 known-blob mutant còn sống là các ví dụ đúng bệnh. |
| CLAUDE — ba trạng thái | Q4/A7 định hướng đúng nhưng Q5 boolean-existence/default fallback và lược đồ/error contract còn hở. Unknown không thành absent/empty. |
| CLAUDE — đo thứ đã đến | A9 mới chỉ hỏi login/substr; chưa neo command/ID/hash thân readback vào event và chưa xử object mutation. Q8 chưa có raw fact. |
| Doctrine/con trỏ | Scan mặc định7tệp không quét SPEC; thêm SPEC thành8 vẫn0 hit. Có quote luật §4 trong Q5 và nhắc lại ngưỡng/stop rule; chưa thấy bản sao đầy đủ bảng/state doctrine bị cấm. Không kết luận “tuân toàn bộ doctrine” từ regex xanh. Hint đổi Q5/ngưỡng sang con trỏ và nghĩa vụ cụ thể để giảm drift. |

### Q7–Q9 và các câu còn thiếu

- **Q7 hợp lệ là quyết định packaging/ngoại lệ**, nhưng hai lựa chọn cũ chưa đủ: slice A vẫn quá dòng và chưa có admission/fencing. Không có lựa chọn được luật cho phép là “3 tệp nên khỏi xét dòng” hoặc “land phần an ninh còn thiếu rồi mới sửa”.
- **Q8 cần quyết định object nào**, sau đó API facts quyết object có đạt không. Không thể bỏ readback vì owner đã chọn URL. Không được dùng chữ “chủ kho gõ trực tiếp” để hứa human-only trong cùng tài khoản/PAT. Cần chốt một event có intent rõ và đúng scope/đích.
- **Q9 là chính sách lịch sử có thể chốt nhận**; không tìm thấy luật bắt buộc cấm thu hồi lease hết hạn. Hết hạn không đảo ngược event hoặc cho tái sử dụng ID. Không gọi lựa chọn sản phẩm này là đáp án bắt buộc từ protocol; khuyến nghị nhận vì tránh race soạn/merge.
- **Thiếu câu chọn đường admission bắt buộc (Q10)**: ai/consumer nào xác minh record, trên exact candidate/base nào, standalone/rc9/direct-push được chặn ở đâu. Thiếu facts thì không kích hoạt.
- **Thiếu câu phạm vi fencing/deployment (Q11)**: dependency máy đầy đủ hay quy trình dừng/readback/cấp lại tuần tự có giới hạn công khai. Generation/retention/không tự cherry-pick là nghĩa vụ sẵn có, không xin phép tuân lại.
- **Thiếu ready facts và rollout (Q12)**: Issue/closure/hash/bên điều phối, base đã nhận predecessor, đủ cache từ workflow và required admission. Chọn implement gate cưỡng chế sau không miễn yêu cầu điều phối hiện tại.

## Tiêu chí A1–A12

Đây là audit thiết kế ca, không tự khai suite mới đã có hoặc đã xanh. “Có phép đỏ” khác “mọi đột biến đã được viết/chạy”.

| Tiêu chí | Có đơn vị? | Có phép làm đỏ thật? | Đột biến đúng ca/thiếu gì? |
|---|---|---|---|
| A1 | Có nhưng lẫn ref với cặp: r2 là2 dòng, không≥4 | Loader bỏ có thể bắt bằng nhãn/holder khi chưa hết hạn; đòi4 sẽ đỏ cả bản đúng | Known-blob mutant **sống 2/2** trên mẫu thật; cần blob thứ3 chưa biết và clock cố định. g2 land không cho0 tự nhiên |
| A2 | Ref3 không có nghĩa3 cặp; một blob⇒1 dòng | Vế sổ trên feature đủ để giết any-ref nếu default đúng | Any-ref đúng mục tiêu; đếm3 dòng sai. Thêm default symref/main-fallback |
| A3 | 5 rc riêng, rõ | (a,b,c,e) dựng được với prerequisite xanh; (d) có old-copy thì phải11 theo luật cũ, trái mong0 | any/cap mutants hợp lý nhưng thiếu **sổ hạn chế + bia mộ cho qua**; precedence/cutoff/history chưa đóng |
| A4 | rc8 + thông điệp | Có, khi chỉ có guard chiều ngược là nguyên nhân | Bỏ guard có thể0 nếu các chốt khác xanh; thiếu Y chết do bia mộ, không chỉ ledger |
| A5 | rc11,ID,path | Có cho exact p/W và fixture X đã được thu hồi đúng | Bỏ loop giết ca chính; nhưng ca không-thay-thế buộc giữ lỗ. Không đo prefix/canonical/effective set hoặc race |
| A6 | SHA/ref/rc12; ratio thời gian | Có với remote-tracking b stale; đã đo control12 | Mutant so tên đúng tầng khi nhánh local/tụt-sau khác không chặn trước; phải nêu ref chính xác. Không giết ref trôi sau so; benchmark mới chưa đo |
| A7 | 7 rc/chẩn đoán | Có nếu mỗi fixture hợp lệ mọi chốt khác | Allowlist nới ai-codex-bot đúng ý; `raise→continue` không luôn0, có thể11. Thiếu parser/missing-object/type/error-order/consumer matrix |
| A8 | “dòng” không chuẩn: metadata cũng bị đếm | Sửa trên default có thể đỏ; sửa chỉ candidate **không thể làm scan default đỏ**; merge ours thật cho0 | Chưa nêu mutant của cổng admission. Ca theo lệnh này có điểm mù rõ và phép M không ra1; thay bằng candidate map-diff trước land |
| A9 | rc5nhánh, account/body | Có bằng fake API giữ trạng thái nếu fixture mới đi tới API | Bỏ account giết(b); không đo ý nghĩa lệnh/endpoint/repo/ID/đích, sự vắng wiring standalone/rc9, object mutable. Cần counter gọi API dương |
| A10 | rc/state/history4nhánh | Có cho begin-attempt, đọc state làm mutant bỏ stale đỏ | Chỉ begin không giết mutant “guard chỉ trong helper” — ba route vẫn0→accepted đã đo. Thiếu record-lease, lỗi blob/YAML và lặp event/root |
| A11 | N/N,delta,rc | Có, nhưng N/N không bằng delta0 trên nền120/121 | Không có mutant riêng được chỉ ra; phải so tập ca/skip trong một lượt cũ/mới cùng tool env. Không dùng doc/doctrine rc0 làm chứng mọi AC chạy |
| A12 | byte,N/N | Output rỗng phát hiện được | Chưa khóa runner in banner/tổng giả hoặc bỏ ca; cần registered/executed/skip và mutant không gọi suite. Chỉ rc≠0 hay byte>0 không đủ |

**Có tiêu chí không thể đỏ?** Không chứng minh được một A nào là hằng-xanh dưới MỌI implementation. Có các điểm **không thể đỏ với đột biến/đối tượng được viện ra**: A8 nhìn default nên mutation candidate không được đo; A1 dùng đúng danh sách hai blob mẫu nên mutation theo known blobs vẫn xanh; A10 không chạm ba route nên bỏ guard ở chúng không đổi ca. Ngược lại, ngưỡng dòng A1/A2 là lỗi **không thể xanh cho implementation đúng đơn vị**, không nên gọi nhầm thành hằng-xanh. Đây chính là điều phải sửa trước khi viết tests.

## chua_do_duoc

1. GitHub API/Actions facts, account tác giả object, branch protection/required checks, hiệu lực PR/Issue và raw body comment5569885143: **không đo** vì cấm mạng. Bare snapshot không chứng minh những facts ấy. Không đọc transcript.
2. Human/agent phía sau PAT, identity/model backend và chữ ký thật: **không chứng thực**. Chỉ đọc raw signature; `%G?=E` trên keyring rỗng không chứng minh signer hợp lệ hay sai.
3. Implementation mới chưa tồn tại. Tất cả exploit luật mới là mô phỏng có nhãn; không có số N/N của A1–A12 mới, chưa đo performance ratio/diff mới/chi phí mạng mới. Không xây runtime thay tác giả.
4. Chưa chạy workflow GitHub thật, checkout@v4 runner thật, Windows/casefold hệ thống thật, heartbeat/push/handoff/land fencing hay cancellation thật. Casefold/prefix là phản chứng comparator dưới hợp đồng §5, không phải phép thử Windows.
5. Nền lease chưa N/N do thiếu actionlint. Không chạy installer mạng và không gọi skip là pass. Packet-loop full suite đã xong gồm mutants; summary/bằng chứng byte ghi trên.
6. Không dựng payload bị cấm (đường thoát cây/đồng tự/chuỗi thoát). Chưa xác minh mọi type/parser corner tương lai; mô tả yêu cầu/ca cho điều phối thay vì tự tạo chuỗi tấn công.
7. Không chứng minh mọi tác giả record giả có thể vượt protection production; finding admission/default nói về những kiểm soát spec đã định nghĩa và ca Git hợp lệ trong sandbox. Nếu production có biên tin cậy bổ sung, phải đưa facts/hợp đồng ấy vào spec để đóng finding.
8. Hai check trước publish cùng0 không chứng minh workflow sau-push có race tương tự. Nó bác bảo đảm chung/độc quyền nguyên tử của `check`; publish/start discipline và fence là câu hỏi riêng đã yêu cầu đóng.
9. Chưa xác minh tần suất “timeout hỏng3 lần”, lịch sử hai ngày/Actions5run, và ca lịch sử bất đồng rc0/12. Không coi con số được nhắc trong Git là measurement độc lập của event ngoài Git.
10. Patch chỉ đã áp lên bản sao SPEC. Phạm vi sáu tệp/dependency/ngoại lệ và object cấp lệnh trong hint phải được chủ kho/điều phối chốt trước lease. Không có thay đổi nào được thực thi trong repository.

Kiểm tra artefact cuối lúc 2026-09-07T14:20:35.475133+00:00: 14 finding (11 P1, 3 P2); 19 kết quả D3 đủ đúng tập ca, D4 độc lập. `patch --dry-run -p0` và áp thật trên bản sao đều rc=0; `cmp` với bản sửa dự kiến rc=0. Băm HINT.patch: `1aeb9621efd07c74db90fd761a6e699b27ddb54ce703623a2936d253b4cd8eb2`; SPEC sau áp trên bản sao: `aaf2493334181121f98fed733b4689af719cea51b9ab9beb21391490bc944fb8`. SPEC gốc giữ nguyên băm đã review; `git diff --quiet` rc=0, status cay-kho vẫn chỉ có spec untracked ban đầu.
