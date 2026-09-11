# VERDICT — cross-review khác nền, LƯỢT 13, PR #468

verdict: approve
reviewed_sha: f77f19895e00835d71644d82f1c54e9b519ccfe6

**Approve cho HỒ SƠ PR #468 (thuần `ops/`): 0 P1, 0 P2, 1 P3.** Bốn finding lượt 12 đều đóng bằng phép đo độc lập. Đây không phải merge authorization, không phải nghiệm thu bốn packet #463–#466, và không xác thực quyền bắt tay trên trạng thái GitHub tương lai.

Reviewer: Codex / OpenAI, phiên API độc lập, shell cục bộ; transport đầu ra: tệp sandbox. `VERDICT.md` được tạo ngay đầu phiên và cập nhật trong quá trình đo. Không mạng, không sửa checkout/nhánh executor, không commit/push lên kho, không đăng GitHub/ghi receipt hoặc state. Selftest có dựng kho giả trong `do-review13/tmp/`; chúng không phải nhánh executor. Đường `ops/...` trong báo cáo tính từ `cay-kho/`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `mirror-thieu-ref-khong-du-do-a9` [P1]: **ĐÃ VÁ THẬT — bằng bundle**. Tự chạy `git for-each-ref --format='%(refname)%09%(objectname)%09%(symref)' refs/remotes/origin`, bỏ symref HEAD rồi so **tập tên và OID** với `tai-lieu/ls-remote-heads.txt`: **303/303, thiếu 0, thừa 0, lệch OID 0**. Bare `kho.git` cũng bằng đúng tập 303 tên+OID ấy. Có đủ năng lực tái đo A9 trên snapshot được giao. Không suy thành đã đo GitHub trực tiếp. Bằng chứng: `do-review13/preflight.json`.

- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **ĐÃ VÁ THẬT về trạng thái — đóng bằng THỜI GIAN**. Chạy CLI sản phẩm thật lúc **20:50:34–20:50:42Z ngày 07-09-2026**, sau hạn **14:30:07Z**: cả `.github/workflows/ci.yml` và `.claude/dev/ci_dang_ky_test.py` in **NGƯỜI_GIỮ 1 = gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906**, rc=11. Registry còn đúng **2 dòng #456, cả hai HẾT_HẠN**; không còn bản #456 CÒN_HẠN gây chồng. `git cat-file --batch-check` trên 303 nhánh đếm blob `8b2103c` trên **11** nhánh, `1f95042` trên **1** nhánh. **Cơ chế bia mộ chưa sửa, ngoài phạm vi PR**: `ops/lease_publish.py` không đổi so 02b0b86, `_kiem_bia_mo` vẫn dùng `any(...)`, blob cũ chưa bia mộ còn tồn tại. Hết hạn không hồi tố hợp thức hóa việc cấp sớm. Bằng chứng: `do-review13/leases.json`, ba stdout và `old456-batch-check.txt`.

- `bien-nhan-luot10-bo-sot-va-tron-dau-vet-phien` [P2]: **ĐÃ VÁ THẬT tại df0800c**. Hai mỏ neo đã sửa: URL vận chuyển lấy từ trailer `Claude-Session` của `17c6901`, có nhãn **TỰ KHAI / không phải danh tính reviewer đã xác thực**; khung giờ thay bằng launch **11:24:25Z**, số đo **11:26:40/11:29:38Z**, final-check **11:47:28.896723Z** lưu trong đúng gói lượt 10. Parse YAML trước/sau chỉ đổi **2 lá prose**: `/github_submitter_identity/phien_van_chuyen` và `/KHONG_do_duoc/2`. Giữ nguyên model reviewer, assurance `review_deferred`, verdict, hash, byte, reviewed_sha, evidence_url, anchor. Không suy thời lượng launcher từ các mốc rời. Bằng chứng: `do-review13/standards.json`.

- `ghi-nhan-luot11-gan-sai-commit-va-moc-van-chuyen` [P2]: **ĐÃ VÁ THẬT tại df0800c**. Receipt sửa đúng hai mỏ neo header/ghi chú; chỉ **1 lá YAML** `/evidence_url_ghi_chu` đổi. GHI-NHAN đồng bộ hai chỗ: **19 tệp rig thêm ở 17c6901**, **0 tệp rig đổi tại 4c18cb2**; billing sửa tại 4c18cb2. Timestamp hai commit **11:50:33Z → 12:17:11Z**, cách **1598 s**, được gọi đúng là thứ tự commit; đã bỏ lời khẳng định PUSH cách 5 s và ghi thiếu log push. Identity/assurance/băm/neo và byte verdict lịch sử không đổi. Bằng chứng: `do-review13/standards.json`.

## BẢNG ĐO

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact HEAD / tree / sạch | f77f198; sạch | `f77f19895e00835d71644d82f1c54e9b519ccfe6` / `43c215a4481c5067c9887c94937287a4fe0dacb6`; status rỗng | có |
| Môi trường Git | abbrev=7, đủ lịch sử, origin GitHub | 7; shallow=false; origin HTTPS GitHub | có |
| Tập snapshot / remote / bare | 303/303, thiếu 0 | 303/303/303; thiếu/thừa/lệch OID 0/0/0; symref loại trước khi so | có với snapshot |
| Trạng thái GitHub trực tiếp / fetch 20:44Z | clone mirror thật, readback 20:45:09Z | KHÔNG ĐO ĐƯỢC trực tiếp; chỉ xác minh byte snapshot ↔ Git local | giới hạn offline |
| Diff sau 02b0b86 | patch + numstat được giao | 186 tệp, +43923/−7, 4 commit; patch/numstat khớp byte; 0 path ngoài ops | có |
| Full diff so origin/master | thuần ops | 795 tệp, +209820/−0; patch/numstat khớp byte; 0 path ngoài ops | có |
| c073655 → f77f198 | thêm 1 DOC-READBACK | đúng 1 tệp thêm | có |
| Spec/lease/Issue/runtime sau 02b0b86 | chỉ hồ sơ review mới | 0 đường đổi trong các phạm vi này | có |
| Tổng ref scanner trong DOC | 306, gồm local + remote ở máy 14:39Z | sandbox này 303 remote + 1 local = 304 ref; bản kê local-head lúc 14:39Z không được giao | KHÔNG ĐO ĐƯỢC lại 306; khác máy, không phải mâu thuẫn 303/306 |
| Đơn vị scanner | khử trùng `(blob,path)` | 288 cặp trên snapshot; #456 có 2 cặp, không phải 2 ref | có |
| ci.yml sau hạn | giữ 1 = exec-1r4; rc=11 | 1, đúng tên, rc=11; #456 có 0 dòng | có |
| ci_dang_ky_test.py sau hạn | giữ 1; #456 2 dòng hết hạn; rc=11 | 1, đúng tên, 2/2 HẾT_HẠN, rc=11 | có |
| pretooluse_guard_test.py sau hạn | giữ 0; #456 2 dòng hết hạn; rc=0 | 0, 2/2 HẾT_HẠN, rc=0 | có |
| So raw readback phiên 20:45Z | ba tệp stdout đã giao | 3/3 bằng byte với stdout reviewer vừa chạy | có; không xác thực thời điểm lịch sử |
| Blob #456 không bia mộ | 8b2103c trên 11 nhánh | `8b2103c06687546379a17f6deafc97f1fe0173fd`: 11, da_bi_thay_the vắng | có |
| Blob #456 có bia mộ | 1f95042 trên 1 nhánh | `1f9504281c3415f7194e124eb7b2702c34c8efd1`: 1, bia mộ hai chiều đúng | có |
| Tổng nhánh mang #456 | 12, khác 2 dòng CLI | 11+1=12; còn 291 nhánh không có tệp này | có |
| 14:39:17Z so hạn 14:30:07Z | 9 phút 10 giây | 550 s = 9 phút 10 giây | có về phép tính; thời điểm chạy lịch sử là lời khai |
| Đo blob ở 14:42:17Z | mốc riêng với 14:39:17Z | hai mốc cách 180 s, tài liệu tách rõ | có về lời ghi, không tái tạo máy lịch sử |
| wp461 trong DOC | 2 lease còn giữ cùng 4 đường, hạn sang 08-09 | 4 cặp blob/path của 3 lease_id; 2 bản có bia mộ; còn 2 ID giữ cùng tập 4 đường, hết 05:27:42Z/09:52:00Z 08-09 | có trên snapshot; ngoài packet #463 |
| Chuỗi #456 → r1 → r2 → r3 → r4 | 4 cạnh hai chiều | 4/4 cạnh tìm được bản trỏ ngược; không suy mọi bản #456 có bia mộ | có |
| R4 thời hạn/write set/neo | 1440 phút; 2 đường; 3 neo d28c4b1 | 1440; 2; cả 3 bằng d28c4b1062e8505cbdaaf0237fcbe3f9b8ee4705 | có |
| Hash write set r4 | 0f7b869d… | `0f7b869da648e9b21023e461925efd0d45bca58fb308a8fcc82bc55ad9f66ef0`, sort + LF cuối | có |
| Bốn spec/alias/Issue/lease | GATE revision 4, ba nháp revision 1 | 4/4 hash, alias, bản chiếu và blob neo đúng; GATE/LO neo 1a33030, 2A/2B neo b743f17 | có |
| Null và generation | GATE cấp thật, 3 nháp chưa cấp | GATE 0 null; mỗi nháp 5 null; cả 4 generation=1 | có |
| Receipt/verdict lượt 10 | 25294 B | 25294 B; SHA256 5e22088b996a4b6e4f564159703ed311bba2c0cf6b137cb9a0614bc9c7476672 | có |
| Receipt/verdict lượt 11 | 22385 B | 22385 B; SHA256 852ba0df07c83a8fc2f2bd02f6658157156e96944273139e6cc8d2aa227cbffd | có |
| Receipt/verdict lượt 12 | 23631 B | 23631 B; SHA256 b4b2671d5d053785232486460251a519b6efd47cff196e672260f3258228d0bd | có |
| Ba evidence_url | commit đầu tiên chứa verdict; ancestry đúng | 3/3: 17c6901,4c18cb2,df0800c; 3/3 blob bằng byte; 3/3 ancestry | có |
| Bản chiếu receipt 10/11/12 + verdict12 | bản được giao đúng head | 4/4 bằng byte | có |
| Bản vá P2 tại df0800c | hai finding, không đổi identity/assurance/băm | receipt10 đổi 2 lá; receipt11 đổi 1 lá + header; 2 vị trí GHI-NHAN đồng bộ; mọi trường bảo vệ và verdict10/11 giữ nguyên | có |
| Mốc/nguồn vận chuyển 10 và sửa 19 rig | dẫn đúng trailer/commit | trailer Claude-Session có URL đã dẫn; 19/0 tệp ở 17c6901/4c18cb2; chênh timestamp 1598 s | có; PUSH vẫn KHÔNG ĐO ĐƯỢC |
| Verdict12 / README / GHI-NHAN | 2 P1,2 P2; lượt11 đóng2/còn1 | 4 header finding đúng severity; bảng và mô tả khớp verdict lịch sử | có |
| Gói lượt12 | manifest 178/178 | sha256sum -c: 178/178, rc=0, 178 tên duy nhất, toàn tệp thường | có |
| Số tệp gói12 | 177 hiện vật + manifest; DOC giải thích ánh xạ | 179 tệp =177 hiện vật + ARTIFACTS + DOC-MANIFEST; 0 symlink; verdict nằm ngoài | có, các đơn vị khác nhau |
| Attestation lượt12 | run 8d2e0018, thread 01a07bff-4592-7833-92c4-26c4c4b324cc; gpt-6-astra 6/6; rc=0; stdout536028 B | 0 raw run/session/prompt trong gói để đối chứng | KHÔNG ĐO ĐƯỢC độc lập |
| Prompt lượt12 | SHA256 1ab4c26b0eb0320fce75ea33b08a9768e40fd2981d6d5761bad4ab7bd243b49c | không có prompt nguyên bản lượt12 để băm | KHÔNG ĐO ĐƯỢC |
| Runtime lượt12 / làm tròn | 1166.934 s; 1166.9/1167 trong prose | làm tròn đúng; final-check lưu 13:31:12.065339Z; không có runtime gốc | có về làm tròn; thời lượng KHÔNG ĐO ĐƯỢC độc lập |
| Hai lần phóng đầu lượt12 | launcher rc=11, reviewer chưa chạy | không có hai run/preflight log; code MA_KHO=11 và chốt kho phù hợp lời giải thích | KHÔNG ĐO ĐƯỢC số lần/kết quả lịch sử |
| bien_nhan_v2 | ĐẠT, 27 v2? | rc=0;27 v2+11 legacy+42 nợ=80;0 vi phạm;0 không đo được theo phạm vi validator | có về schema/băm/neo |
| lease_publish_test | 121/121 | rc=0;121/121;đã chạy121,bỏ qua0 | có |
| lease r4 check | đăng được | rc=0, ĐĂNG ĐƯỢC; cổng tự khai không đo 2 lớp GitHub | có; không thay A9 |
| doctrine / ADR | sạch | rc=0;7 tệp/0 chép;46 ADR/46 dòng, ngoại lệ trạng thái0016 của cổng | có |
| doc-claims strict | ok | rc=0,ok:true;106 tệp;367 advisory/0 cờ cứng;10 lớp chạy,0 lớp bỏ qua trong tập bật | có; roots không có ops |
| EOL toàn index | ok | rc=0,ok:true;1635 quét/1613 kiểm/22 bỏ qua/0 vi phạm | có |
| Bao phủ EVIDENCE | tự khai suite chưa chạy | thiếu cách trích/giới hạn bộ lọc; phép bổ sung lấy 90 dòng ứng viên từ 6 tệp, không phải 90 khẳng định đã chứng minh | P3 bên dưới |
| GitHub CI/branch protection/billing/Windows/authority | CI run34125520827 head02b0b86 success; head mới chưa đọc | KHÔNG ĐO ĐƯỢC offline; không dùng local pass thay GitHub required check | giới hạn đã giữ |

Băm spec tự tính đầy đủ:

| packet | SHA256 spec | revision/generation | ô null trong lease |
|---|---|---|---|
| #463 | `4c542f6b931f62687edd6dca0c5f22c0399ad41f4e80b48e29cdfcd519289cd8` | 4/1 | 0 |
| #464 | `66dcb20d7bc044cc3185074b56152f0f7f737ac2d1a49c225c29a29b144b4917` | 1/1 | 5 |
| #465 | `2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759` | 1/1 | 5 |
| #466 | `417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521` | 1/1 | 5 |

Các lệnh cổng tự chạy ở `cay-kho/` và chi phí đo của **lượt này**, không phải runtime Codex lịch sử:

| tên hiện vật | rc | giây | stdout/stderr byte |
|---|---:|---:|---:|
| `lease-publish-test` | 0 | 54.863 | 8649/56 |
| `bien-nhan-v2` | 0 | 1.169 | 163/0 |
| `doc-claims` | 0 | 2.813 | 70854/0 |
| `doctrine-scan` | 0 | 0.429 | 69/0 |
| `adr-song` | 0 | 0.298 | 113/0 |
| `eol` | 0 | 0.54 | 138/0 |
| `lease-check` | 0 | 2.972 | 235/0 |

Lệnh đầy đủ có trong JSON cùng tên: `python3 -B ops/lease_publish_test.py`; `python3 -B ops/bien_nhan_v2.py`; `python3 -B scripts/tl.py doc-claims-check --strict --json`; `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`; `python3 -B .claude/dev/packet_loop.py adr-song --root .`; `python3 -B .githooks/eol_policy.py --all --json`; `python3 -B ops/lease_publish.py check ops/leases/gate-tach-job-cat-chi-phi-exec-1r4-claude-20260906.yaml`. Không chạy `packet_loop_test`, `ci_dang_ky --chay` hoặc toàn bộ runtime suite: phần đổi sau 02b0b86 không sửa mã runtime. Đây là **not_run**, không khai pass.

### evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu  [P3]  Bảng EVIDENCE chưa khai cách trích số và phần bỏ sót

TỆP/DÒNG: `EVIDENCE.md:14–20`; đối chiếu `tai-lieu/PROTOCOL-trich-8-12-13.md`, §8 đoạn “Bảng bằng chứng do executor cung cấp phải TỰ KHAI GIỚI HẠN”.

VẤN ĐỀ: EVIDENCE có giới hạn suite, nhưng không có lệnh/script trích danh sách khẳng định định lượng, tiêu chí lọc và phần lọc bỏ sót. Các số mới **23631 B,178/178,536028 B,1166.934 s** không được đưa vào bảng hoặc phân loại nguồn. PROMPT của lượt này mở phạm vi cho reviewer và reviewer đã tự đo byte/manifest, ghi attestation KHÔNG ĐO ĐƯỢC; vì vậy đây là nợ chất lượng gói mức P3, không phải P1 thiếu ref tái phát hoặc bằng chứng receipt sai.

ĐÃ THỬ VÁ: **Có**, soạn bản bổ sung `do-review13/goi-y-evidence.md` trong scratch: chỉ rõ cách trích sáu tệp hồ sơ vừa đổi, tách số đã băm/đếm lại và số chỉ là lời khai, ghi giới hạn bộ lọc chữ số và quy tắc mục bỏ sót vẫn tính finding. Không sửa receipt/assurance/authority hoặc checkout. Rủi ro của hướng vá: bộ lọc chữ số bỏ số viết bằng chữ và bắt cả SHA/ID; cần phân loại bằng người, không nâng 90 dòng ứng viên thành 90 chứng cứ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review13/claims_inventory.py` **rc=0**, lấy **90** dòng thêm có chữ số trên **6** tệp của diff 02b0b86→f77f198, xác nhận bốn ví dụ trên vắng trong EVIDENCE. Kết quả và giới hạn được lưu ở `claims-inventory.json`; byte/manifest đã kiểm độc lập bằng `standards.py`. Khi executor áp bổ sung, phép kiểm là chạy lại lệnh đã công bố và đối chiếu từng số với loại nguồn, không chỉ tìm sự có mặt của từ “giới hạn”.

ĐỘ TIN: cao về thiếu phương pháp/bao phủ trong gói được giao; không khẳng định những số chưa xác minh là sai.

## STANDARDS — KẾT LUẬN VÀ GIỚI HẠN

Receipt12 neo đúng blob tại `df0800c1b02f156925f22ec14584a754f2aea142`, reviewer SHA là tổ tiên, verdict/hash/bảng README/ghi nhận thống nhất. Hai mỏ neo receipt10 và hai mỏ neo receipt11 mà lượt12 yêu cầu đã được executor sửa đúng, không tăng assurance. Gói lịch sử được bảo toàn; không sửa verdict cũ để xóa finding. `cross_approved` trong receipt12 là **nhãn assurance được khai cho review lịch sử có verdict changes_requested**, không biến reviewer12 thành đã approve head hiện tại. Schema validator không xác thực raw model/session vắng mặt. Thread, prompt hash, runtime, stdout và lời khai “2 lần phóng đầu chặn rc=11” được giữ ở mức **KHÔNG ĐO ĐƯỢC độc lập**, không bị đánh tráo bằng mã thoát cổng local.

DOC-READBACK đã sửa lỗi đơn vị ở f77f198: hai dòng là hai cặp `(blob,path)`, 11+1 là số tên nhánh đo riêng; 303 là nhánh remote, 306 là phạm vi scanner có thêm local tại máy/lúc của tác giả. Không thấy mâu thuẫn số học hoặc lẫn đơn vị còn gây P1/P2. Mốc 14:39/14:42 thuộc phiên vận chuyển khác, 20:45 thuộc bundle này, 20:50 thuộc reviewer; chúng không thay thế nhau. Câu kết luận đóng bằng thời gian được hiểu là không có bản vá bia mộ mới cho việc đóng này: một blob đã có bia mộ từ trước vẫn tồn tại và được bảng ghi rõ. Dòng wp461 là vấn đề khác, đo được còn hai ID giữ bốn path không giao write set #463; không tự mở task sửa nó trong PR hồ sơ.

**Cách chạy offline được công bố:** CLI nguyên bản gọi `git ls-remote`, nên đặt `GIT_ALLOW_PROTOCOL=file` và `GIT_CONFIG_COUNT=1`, với khóa `url.<file://.../rv468g/kho.git>.insteadOf` thay đúng URL `https://github.com/ducthangho/tra-luat.git` chỉ trong môi trường tiến trình. `ls-remote` đọc **mirror Git thật**, sau khi đã tự so tên+OID mirror ↔ snapshot ↔ checkout. Không sửa config trên đĩa, không thay scanner, đồng hồ hoặc output; không kết nối mạng. Lệnh/scenario đầy đủ nằm trong `do-review13/measure.py`. Đây là phép đo trạng thái trên snapshot đủ ref được giao, không phải readback trực tiếp GitHub; A9 phải được executor đo lại tại thời điểm bắt tay trên cây nguồn theo spec.

Phạm vi đã review gồm **Spec** (A9 hiện trạng, bốn hợp đồng/băm/neo và không có delta spec/runtime) và **Standards/Security** (bản vá P2, receipt12, README/GHI-NHAN, DOC-READBACK, toàn vẹn gói, môi trường cổng). Không nghiệm thu A1–A8, billing, Windows hay bốn packet chưa thi công. Năng lực/budget lịch sử và quyền GitHub không được tự cấp từ lượt này. PROMPT chỉ cho đầu ra trên đĩa, nên việc vận chuyển verdict/receipt lên PR thuộc bên điều phối; không có review GitHub chính thức hoặc merge/land nào được thực hiện.

## KIỂM CUỐI VÀ BÀN GIAO

Kiểm cuối **2026-09-07T21:04:16.336801+00:00**: HEAD/tree giữ nguyên, status/diff/index rỗng, **0 commit** sau reviewed_sha. Kết quả ở `do-review13/final-check.json`. Bộ đo bổ sung có một lần dừng do regex của reviewer giả định mỏ neo Issue là URL; đã sửa để đọc đúng dạng `` `path` @ `SHA` `` và chạy lại thành công. Đây là lỗi bộ đo trong scratch, không phải finding của PR.

`ARTIFACTS.sha256` liệt kê **48 tệp thường** gồm VERDICT, script và bằng chứng mới; không symlink, không thành phần đường dẫn tương đối `tmp`. Bản sao bố trí `manifest12-layout/` chỉ phục vụ phép kiểm manifest cũ, không đưa lặp vào manifest bàn giao mới; kết quả từng hash nằm trong `standards.json` và `manifest12.stdout`. Đã kiểm `sha256sum -c ARTIFACTS.sha256` sau khi chốt nội dung.

**Approve chỉ cho HỒ SƠ PR #468 thuần ops tại exact SHA nêu trên; không phải merge authorization và không phải nghiệm thu bốn packet.**

verdict: approve
