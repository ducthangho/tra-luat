verdict: changes_requested
reviewed_sha: 9337779b7d61d3b08947982383081de127e7d632
base_sha: 802fc01b5db866478459dbc4a65d008a38619898
reviewed_tree: 16f44dad14b83a2eeab68a6b0a4aacc5a8b034e5

**CÒN 3 P1 phải sửa trước khi land · 0 P2 · 17 P3.** Ba P2 của lượt 4 đã vá thật. Hai P1 liên quan khối mới và việc đồng bộ bookkeeping; P1 còn lại là lời khai đóng nợ không đúng với hiện vật. Các cổng được giao đều xanh; chúng không xác nhận tính đúng của các lời khai này.

Reviewer: Codex / OpenAI, shell cục bộ qua công cụ của phiên này, vận chuyển bằng tệp trong gói. Executor theo chỉ thị là Claude; không suy model/effort cụ thể từ tên sản phẩm. Chỉ đọc/ghi trong gói, không gọi mạng, không đọc transcript bên ngoài, không tự soạn nội dung tấn công, không commit/push. Nội dung tracked của `cay-kho/` giữ nguyên, `git status --porcelain` rỗng trước/sau.

Nguồn đối chiếu lượt trước là [VERDICT-LUOT4.md](VERDICT-LUOT4.md), đã đọc cả **ĐÃ THỬ VÁ** của ba P2. Không có hiện vật gốc lượt 1–3 của #478 trong gói; không dựng lại verdict của họ từ lời tự khai trong commit.

Quy ước: đường `ops/...`, `docs/...`, `CLAUDE.md` tính từ `cay-kho/`; `LAND` dưới đây là `ops/land/pr468-hoso-4-packet-land-evidence.yaml`. Bản `LAND_EVIDENCE.yaml` ở gốc gói bằng byte blob tại reviewed SHA. Các lệnh `python3 -B do-luot5/...` chạy từ **gốc gói**. Script, stdout/stderr và JSON kết quả ở [do-luot5](do-luot5/). `rc=0` của script audit nghĩa là đã đọc/tính thành công; phải đọc kết quả các lệnh con, không suy mọi đối tượng audit đều pass.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `land-evidence-dem-bon-goi-doi-bo-cuc`: **ĐÃ VÁ THẬT** — LAND:235–247 phân biệt đúng 3 manifest bố cục và 1 băm trần. `python3 -B do-luot5/audit.py manifests`: ba direct `rc=1`, `0/128`, `0/178`, `0/48`; băm trần `rc=1`, stdout **0 B**, lỗi định dạng. Ánh xạ đúng đều pass; băm trực tiếp khớp. Không rơi vào bẫy sửa thành chỉ ba phép kiểm trực tiếp lỗi.
- `land-evidence-so-luot-khong-co-don-vi`: **ĐÃ VÁ THẬT** — LAND:75–91 giữ `so_luot: 15`, định nghĩa số thứ tự cuối; **10** gắn với *verdict hoàn tất có hiện vật*, không được dùng làm tổng invocation/lịch sử. `python3 -B do-luot5/audit.py reviews`: hai kho đều có đúng 10 đường verdict theo mẫu, 6–15; đọc nội dung có verdict/kết luận, không chỉ đếm tên. Lượt 11 là một verdict riêng, có DOC-MANIFEST giải thích đổi số từ 10; không loại như bản trùng. Ghi nhận lượt 5 tự phủ định; không tìm được verdict 1–4 theo inventory ấy. Bản vá **không thay mù 15 bằng 10**. Sự tồn tại các phiên ngoài gói vẫn KHÔNG ĐO ĐƯỢC.
- `land-evidence-dan-adr-sai-pham-vi`: **ĐÃ VÁ THẬT** — LAND:3–14 đổi cả căn cứ lẫn đối tượng của câu dẫn. `python3 -B do-luot5/sources.py` lưu ADR-0034:17–20, Protocol:466–488 và ADR-0045:5–8: nghĩa vụ land evidence nằm ở hai nguồn đầu; nguồn cuối nói về ngoại lệ Codex executor sensitive và lease. Không chỉ đổi số hiệu trong câu cũ.
- `land-evidence-khai-dong-p3-khi-con-sot`: **CHƯA VÁ** — LAND:124 vẫn “vá nốt P3”; README full-gate:57 còn nguyên câu về chạy lại để đối chiếu byte gốc, được verdict 15:80 đưa vào chính P3 ấy. `python3 -B do-luot5/audit.py fullgate` và `python3 -B do-luot5/sources.py` xác nhận. Finding bên dưới phân hạng **P1 cho lời khai đã đóng trong hồ sơ land**, theo tiêu chí lượt này; không nâng lỗi README gốc hay viết lại verdict 15.
- `land-evidence-gioi-han-chua-phu-het-loi-khai`: **VÁ HỜ trên toàn phạm vi finding** — authorization:41–47 và model:94–99 đã được giới hạn thật. Nhưng số invocation full-gate, 71 s, mốc snapshot 23:43:30Z, trạng thái Issue/Mission vẫn thiếu giới hạn tương ứng; phần #477 nay có phản chứng cụ thể và tách thành P1. Nguồn: `sources-audit.json`, `reviews-audit.json`, `checks.json`. Không gọi các API fact chưa kiểm được là sai.

Mười một P3 sau của lượt 4 là **độ phủ bảng giao review**, không phải giá trị sai trong PR. Bảng chín hàng lượt này vẫn bỏ các mệnh đề ấy; vì vậy “CHƯA VÁ” dưới đây chỉ nói về độ phủ. Tôi đã bổ sung vào BẢNG ĐO và giữ finding riêng như người dùng yêu cầu:

- `bang-do-bo-sot-land-evidence-thu-hai`: **CHƯA VÁ về bảng** — `audit.py git`: base có 1, reviewed tree có 2 tệp land-evidence YAML. Không đếm tệp #477 ở nhánh khác thành tệp có trước #468.
- `bang-do-bo-sot-mot-commit-chen`: **CHƯA VÁ về bảng** — `audit.py git`: khoảng `745d888..17f4a1b` đúng 1 commit.
- `bang-do-bo-sot-bon-cap-delta`: **CHƯA VÁ về bảng** — `audit.py fullgate`: 4/4 cặp bằng byte, chỉ trong phạm vi hiện vật đã lưu.
- `bang-do-bo-sot-sau-bo-full-gate`: **CHƯA VÁ về bảng** — cùng lệnh: 6 bộ ở mỗi log, rc lần lượt `0,0,1,0,0,0`.
- `bang-do-bo-sot-out-khong-rong`: **CHƯA VÁ về bảng** — cùng lệnh: 0/12 trường `out` bằng 0; năm bộ không đủ raw để xác thực kích thước lịch sử.
- `bang-do-bo-sot-mot-phan-sau-stdout`: **CHƯA VÁ về bảng** — cùng lệnh: 1 raw doc JSON + 2 tail + 1 norm + 2 bộ không có output.
- `bang-do-bo-sot-lease-truoc-merge`: **CHƯA VÁ về bảng** — cùng lệnh: log trước merge `120/121`, chạy 121, bỏ qua 0; t33 đỏ ở tiền điều kiện thiếu actionlint.
- `bang-do-bo-sot-byte-lease`: **CHƯA VÁ về bảng** — phép chạy mới suite ở reviewed SHA cho stdout 8649 B, stderr 56 B; không đồng nhất với thời lượng lịch sử 71 s.
- `bang-do-bo-sot-chin-manifest-truc-tiep`: **CHƯA VÁ về bảng** — `audit.py manifests`: 9 direct pass, tổng 613 mục; ánh xạ thêm 354 mục, tổng ARTIFACTS 967; băm trần kiểm riêng.
- `bang-do-bo-sot-sau-buoc-if-sai`: **CHƯA VÁ về bảng** — `audit.py ci`: Windows có 6 điều kiện sai trên push/master. Đây là số tĩnh, không phải phép đọc số skipped của API ở hàng 5 bảng giao.
- `bang-do-bo-sot-sau-loi-goi-review-spec`: **CHƯA VÁ về bảng** — `audit.py bookkeeping`: spec r6 trên ref đã nêu có đúng 6 hàng invocation `1,2,3,4a,4b,5`, gồm một hàng chết. Không gọi là sáu verdict hoàn tất.

## BẢNG ĐO

**Khớp nguồn** = đọc được giá trị trong hiện vật, không xác thực lần chạy lịch sử. **Đo mới** = reviewer thực chạy trong lượt này. **KHÔNG ĐO ĐƯỢC** không phải pass/fail. `BS` là định lượng ngoài bảng chín hàng của điều phối, có finding về độ phủ bên dưới; nhóm cùng map/phép đếm dùng chung một finding, không nhân theo từng số hạng. SHA, số hiệu PR/ADR và version chỉ làm định danh thì không được nhân thành finding số lượng.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Head/base/tree và bản tệp giao | SHA ở đầu prompt | Đúng full SHA/tree ở đầu verdict; tệp gốc bằng byte Git blob | Có |
| Phạm vi PR so base | Hồ sơ land + hiện vật review | 112 tệp, +12969/−0; LAND 292 dòng, 111 path còn lại thuộc `ops/reviews/`; 0 thay đổi mã vận hành | Có |
| Hai commit kể từ lượt 4 | `83e4786`, `9337779` | Đúng chuỗi cha, chỉ sửa LAND; +110/−14 so `5a4dd85` | Có |
| Năng lực gói hiện tại | 309 heads, 62 tags, không nông, abbrev 7 | Đúng; `kho.git` còn có 327 pull refs | Có về snapshot; server KHÔNG ĐO ĐƯỢC |
| **BS:** snapshot mà đoạn đếm verdict viện dẫn, LAND:85 | 307 nhánh + 62 tag, 08-09 | Verdict lượt 4 ghi phép đo 307/62; gói lượt này là 309/62 | Khớp nguồn lượt 4; không coi 307 là số hiện tại |
| Căn cứ mở đầu | ADR-0034:17–20 + Protocol:466–488 | Hai nguồn có đúng nghĩa vụ/mẫu; ADR-0045 nói ngoại lệ khác | Có |
| **BS:** số thành phần land, LAND:5 | Sáu thứ | Approver, authorization, operator, merge commit, post-merge gate, bookkeeping | Có |
| **BS:** thứ tự tệp, LAND:16 | Land evidence thứ hai, sau plat-x8 | Base có 1 YAML loại này; reviewed tree có 2; lịch sử tạo plat-x8 trước | Có trong phạm vi loại tệp/lịch sử đó |
| Schema/role | v1, generation 1, input `[1]`, land_operator | YAML parse được, trường/mẫu đúng | Khớp cấu trúc; không xác thực identity/land attempt |
| Approval | 2 APPROVED; 22:54:28Z và 23:15:00Z; actor và commit_id | Thiếu JSON API gốc | **KHÔNG ĐO ĐƯỢC** |
| Dismiss/blocked/classifier | 2 DISMISSED; khoảng 5 phút; nguyên nhân; classifier từ chối | Thiếu timeline/response/log gốc | **KHÔNG ĐO ĐƯỢC** |
| “Mỗi commit đẩy sau approval đều huỷ approval” | Quy luật ở LAND:40 | Không có cấu hình/timeline để kiểm mọi lần push | **KHÔNG ĐO ĐƯỢC**; đã có nhãn attestation cấp mục |
| Người merge và merged_at | notebyme88; 23:21:22Z | Git author notebyme88, committer GitHub, commit time 23:21:21Z UTC | `merged_by`/API time **KHÔNG ĐO ĐƯỢC**; 1 giây khác loại timestamp không chứng minh sai |
| Đơn vị lượt review | 15 là chỉ số cuối; 10 verdict có hiện vật; 1–4 thiếu, 5 không hoàn tất | Hai inventory object paths: 10 verdict 6–15; nguồn lượt 5 tự phủ định | Có trong phạm vi hiện vật; tổng lịch sử KHÔNG ĐO ĐƯỢC |
| Model/effort | Attestation codex gpt-6-astra xhigh | run.json 14/15 chỉ có 3 khoá trong `lenh`; receipt giữ giới hạn | **KHÔNG ĐO ĐƯỢC** model thực được phục vụ |
| **BS:** P1 từng lượt | `{7:4,8:2,9:1,10:1,11:1,12:2,13:0,14:0,15:0}` | Đếm heading `[P1]` đúng cả 9 số hạng | Có |
| **BS:** phạm vi verdict và manifest 14/15 | 6–13 trên base; 14/15 thêm cùng PR; 59/59 và 45/45 | `cat-file -e` đúng phân chia; `sha256sum -c` đúng hai tỷ số, rc=0 | Có |
| **BS:** lượt cuối | 15; `745d888…`; approve; 0 P1/0 P2/1 P3 | Nội dung và heading verdict 15 đúng | Có |
| **BS:** số commit giữa head review/merge | Một commit `17f4a1b` | `git log 745d888..17f4a1b` đúng 1 dòng | Có |
| Diff riêng `17f4a1b` | 2 tệp +23/−8, toàn ops/reviews, 0 mã vận hành | Manifest +1/−1; README +22/−7 | Có |
| “vá nốt P3” | Đã đóng P3 duy nhất của lượt 15 | Còn câu README:57 mà verdict 15:80 gộp vào P3 đó | **Không — P1** về lời khai đóng |
| Head merge chưa có cross-review | Lượt cuối neo cha `745d888` | Không verdict #468 hiện có neo `17f4a1b` | Khớp hồ sơ; review ngoài gói KHÔNG ĐO ĐƯỢC |
| Full-gate MỘT lần | Một lần theo chỉ thị; nền b416830, sau f77f198 | Một bộ hiện vật; neo là commit có thật | **KHÔNG ĐO ĐƯỢC** tổng invocation và provenance launcher lịch sử |
| **BS:** bốn cặp DELTA | 0 | 4/4 bằng byte: tail 206/96 B, norm 8827 B, JSON 70861 B mỗi vế | Có, đúng phạm vi bốn cặp |
| **BS:** sáu bộ, cặp rc | cidk 0/0, ploop 0/0, lease 1/1, doctrine 0/0, adr 0/0, doc 0/0 | Hai `.rc`, mỗi tệp 6 record, đúng map | Khớp log; exit code lịch sử KHÔNG ĐO ĐƯỢC độc lập |
| **BS:** không out=0 B | Không bộ nào | 0/12 trường out bằng 0; mỗi vế `[2934,8752,8971,69,113,70861]` B | Khớp log; thiếu raw 5/6 bộ |
| **BS:** độ phủ stdout | 1/6 tự đếm lại được | Doc raw đủ; 2 tail, 1 norm, 2 không output | Có về nguyên liệu |
| **BS:** lease trước merge | 120/121; t33 chạy và đỏ | Cả hai norm ghi 120/121, chạy 121, bỏ qua 0; thiếu actionlint | Khớp log; không phải skipped |
| CI push #468 khi completed | Windows 44 bước, 6 skipped, 0 null; Ubuntu 44/4 | Không có raw jobs response; workflow có 40 bước khai tĩnh | **KHÔNG ĐO ĐƯỢC API**, không lấy 40 bác 44 |
| CI PR #468 | 1 Ubuntu job, 44 bước, 0 hỏng | Không có response/checkout log của run | **KHÔNG ĐO ĐƯỢC** |
| **BS:** phân tích tĩnh | Windows 6 bước có if sai | Base ci.yml: 40 bước, 10 if; Windows 6 false, Linux 4 false trên push/master | Có về tĩnh; không xác thực run API |
| Cặp trước/sau run #477 | 43 bước/1 skipped → 44/6 | Có cùng lời khai trong land #477 trên ref khác; không có raw response | **KHÔNG ĐO ĐƯỢC**; hai văn bản cùng kể không thành hai phép đo độc lập |
| Hai client, job/time/completion ở khối mới | MCP và JSON-RPC cùng kết quả; các mốc kết thúc | Không có phản hồi gốc/client logs | **KHÔNG ĐO ĐƯỢC** |
| Cửa sổ 4 skipped | 00:04:53Z → 00:11:17Z = 6,4 phút, duy nhất | Trừ hai mốc **được khai**: 384 s = 6,4 phút; sáu mốc chỉ có trong prose | Số học đúng; mốc thật/cửa sổ hiển thị API **KHÔNG ĐO ĐƯỢC** |
| Loại Ubuntu bằng 43 vs 44 | Chỉ đọc giữa chừng khớp cả hai số | Phép loại giả định ghi đúng 43 từ cùng response; không có nguồn giữ giả định ấy | **Không — P1**, cùng finding nguyên nhân |
| Đã xác định nguyên nhân/null cũ | Điều phối đo giữa chừng; “trong ca này” null khác 0 | Chính LAND:179–183 nói không ghi thời điểm gọi, không quan sát run cũ lúc in_progress | **Không đủ để khai đã chốt — P1** |
| Rút exact-head CI | PR run không chứng minh test `17f4a1b` | Workflow checkout không ghim ref về SHA đó; thiếu checkout log riêng | Giới hạn hợp lý; run thật KHÔNG ĐO ĐƯỢC |
| Tool discovery | 44 tools, ít nhất 2 client, probe 4 tools | CLAUDE.md:580–584 nêu endpoint riêng/hai client | Khớp tài liệu; con số lần probe **KHÔNG ĐO ĐƯỢC** |
| Merge topology | master tại merge =802fc01, cha b416830 + 17f4a1b; ancestor đúng; nhánh thừa 0 | Dùng exact base: ancestor rc=0, count stdout 0 rc=0; hai parent khớp | Có; `master` gói hiện tại đã là 585c7d5 |
| Cổng lease lượt này | Kỳ vọng 121/121, chạy 121, bỏ qua 0 | Trên reviewed SHA: rc=0, đúng cả ba, 66,316 s | Có ở phép chạy mới; 71 s lịch sử KHÔNG ĐO ĐƯỢC |
| **BS:** byte stdout lease | 8649 B | Đo mới 8649 B stdout; 56 B stderr riêng | Có |
| actionlint | 1.7.7 | Binary trong cong-cu.txt, gọi đường tuyệt đối; lint workflow rc=0 | Có về bản/lệnh mới; cách cài lịch sử chỉ là nguồn khai |
| Cổng receipt lượt này | 0 vi phạm | rc=0; 30 ĐẠT v2; 11/11 legacy; 42 nợ; tổng 83; 0 vi phạm; TỔNG ĐẠT | Có; schema không chứng minh identity |
| Doc-claims | rc=0, ok:true; lịch sử 70861, kho đủ tag 70854 | Đo mới 70854 B; log cũ 70861 B; JSON khác đúng 1 lá `/advisories/74/reason` | Có về byte/nội dung |
| Giải thích delta doc | SHA1835b46 trên tag archive/dlbrut-ke-hoach-dau; reason ngắn 7 | Tag trỏ đúng commit; object không là tổ tiên head; hai reason khác đúng 7 ký tự | Có về object/reason; lịch sử thiếu đúng 23 tag và thao tác fetch **KHÔNG ĐO ĐƯỢC độc lập** |
| Đối chiếu nền↔sandbox lượt 5 | Điều phối khai byte bằng 70854/70854 | Một vế mới do reviewer chạy 70854; không có hai raw log riêng của phép đối chiếu điều phối | **KHÔNG ĐO ĐƯỢC** cả cặp; không suy môi trường tương đương |
| **BS:** tổng/chín manifest và ánh xạ | 13, 0 hỏng; 9 direct; 128/128, 178/178, 48/48; băm prompt khớp | Base: 12 ARTIFACTS +1 băm trần; 9 direct rc0=613 mục; mapped rc0=354; tổng 967; băm e60c376a… khớp | Có; không gọi băm trần là manifest chuẩn |
| 3 bố cục +1 định dạng | 4 direct không dùng được, hai nguyên nhân | Ba record sets 0/N; một bare stdout rỗng, rc1; đầy đủ stderr đã lưu | Có, P2 đã vá thật |
| `_kiem_bia_mo` còn any | Chưa sửa mã | `ops/lease_publish.py:606` giữ `not any(...)`; diff không sửa runtime | Có; không tạo thử nghiệm tấn công mới |
| Spec thu hồi | r6; tip 2aee80a; 22:53:12Z; chưa Packet Issue/chờ checkpoint | Blob trên đúng ref khớp revision/tip/commit time và lời trạng thái | Khớp hồ sơ; API state/approval KHÔNG ĐO ĐƯỢC |
| **BS:** số lời gọi spec | 6/6, đã hết | Sáu hàng 1/2/3/4a/4b/5, một hàng chết vẫn đếm | Khớp nội dung; runtime/authority lịch sử KHÔNG ĐO ĐƯỢC |
| Mốc snapshot cũ | 23:43:30Z | Gói này ghi 2026-09-08T02:56:05Z; không có chứng từ snapshot cũ tương ứng | **KHÔNG ĐO ĐƯỢC** mốc cũ; không dùng giờ mới để bác |
| Bốn lease GATE | 03:37:33/07:50:35/09:44:51/10:17:12Z, trước 14:30:07Z | Đọc từng YAML trên 309 head refs: đúng 4/4; tiền nhiệm #456 đúng hạn | Có trong snapshot |
| Revision/hash/generation | r1/2/3/4, 4 hash khác, generation đều1 | Đúng từng số hạng và 4 distinct hash; ADR-0034 có điều khoản generation mới | Có; quyết định xử lý ngoài gói KHÔNG ĐO ĐƯỢC |
| P1 #456 đóng bằng thời gian | Readback sau hạn; không vá code | DOC-READBACK ghi 14:39:17Z sau 14:30:07Z; mã giữ điều kiện hạn, runtime không đổi | Khớp hồ sơ; không tái xác thực readback server |
| Issue #463–466 và Mission467 | Cả 5 open | Không có JSON API thời điểm tương ứng | **KHÔNG ĐO ĐƯỢC** trạng thái |
| PR477 chưa merge | LAND:292 “đang… chưa merge” | LAND:164 đã gọi merge585c7d5; Git object hai parent, commit time01:22:38Z, nằm trên master trước commit 933 lúc02:27:22Z | **Không — P1** về hồ sơ/snapshot; API state không đo |

Lệnh cổng đã chạy với `TMPDIR` trỏ vào `do-luot5/tmp`, `PYTHONDONTWRITEBYTECODE=1`, `GIT_ALLOW_PROTOCOL=file`, và thêm thư mục tuyệt đối chứa actionlint trong `cong-cu.txt` vào đầu PATH. Không fetch/cài công cụ. Các lệnh thực là `python3 -B ops/lease_publish_test.py`, `python3 -B ops/bien_nhan_v2.py`, `python3 scripts/tl.py doc-claims-check --strict`, cwd=`cay-kho/`; lệnh actionlint trực tiếp là `<đường tuyệt đối từ cong-cu.txt> .github/workflows/ops-publish-lease.yml`. [checks.json](do-luot5/checks.json) lưu từng argv, rc, byte và thời lượng; stdout/stderr riêng còn nguyên. Phép lease mới đo **reviewed SHA**, không tự nhận đã chạy lại base hay khôi phục stdout lịch sử.

### land-evidence-chot-nguyen-nhan-chua-quan-sat  [P1]  Chốt “điều phối đo giữa chừng” từ giả thuyết chưa loại được đối thủ

TỆP/DÒNG: LAND:149–189, trọng tâm 159–177 và 189; tiêu đề commit `9337779`; đối chứng `CLAUDE.md:251–264`.

VẤN ĐỀ: khối mới chưa chứng minh nguyên nhân của lần ghi **43/4**, nhưng đặt dưới `mau_thuan_da_giai`, `nguyen_nhan`, `gia_thuyet_da_loai`, viết “Chỉ giả thuyết đọc-giữa-chừng…” và kết bài “trong ca này [null] khác 0”. Tiêu đề commit khẳng định thẳng điều phối đo giữa chừng. Đó là lời khai đã xác định một việc xảy ra, vượt quá bằng chứng mà chính thân bài thừa nhận có.

Phép loại Ubuntu không đứng: nó chỉ bác mô hình **đọc Ubuntu completed và ghi nguyên xi cùng một response**. Chưa có nguồn chứng minh `43` được ghi đúng, hoặc hai số được lấy từ cùng một lần đọc. Khả năng đọc Ubuntu `44/4` rồi ghi nhầm số bước thành 43 vẫn tạo cặp `43/4`; đây là phản ví dụ logic, **không phải lời khai chuyện ấy đã xảy ra**. Không được chọn số 43 đang tranh cãi làm chuẩn chắc chắn để loại mọi sai sót ghi chép.

Ngay cả nếu chấp nhận toàn bộ attestation của lần đọc mới, cặp trước/sau run **khác** chỉ chứng minh cơ chế có thể xảy ra ở run đó. Sáu mốc ở run468 tạo 384 giây theo phép tính, chưa chứng minh thời điểm điều phối đọc, và còn giả định thời điểm step kết thúc đồng nhất với lúc API hiển thị conclusion. `con_lai_khong_do_duoc` chỉ hạ mức “đã chứng kiến”, nhưng vẫn nói “đủ căn cứ để ĐÓNG”; nó không sửa được khung đã chốt nguyên nhân và câu null-cũ. Đính chính số completed về6 theo attestation và tìm ra nguyên nhân vì sao trước đó ghi 4 là **hai kết luận khác nhau**.

ĐÃ THỬ VÁ: **không sửa PR** — nên giữ số completed mới với nhãn attestation, đổi trạng thái điều tra nguyên nhân thành chưa xác định, đặt “đọc giữa chừng” là giả thuyết tương thích; giữ “đọc nhầm/ghi nhầm/trộn lần đọc” chưa bị loại. Đồng bộ tên trường, câu mở, câu kết và lời đính chính tiêu đề commit trong hồ sơ bền; không cần sửa lịch sử commit cũ. Bỏ lời khẳng định null của lần cũ nếu không có response ấy. Ca kiểm bản vá: đọc riêng tiêu đề, nhãn và bài học vẫn không thấy nguyên nhân chưa quan sát được trình bày như đã xác lập. Rủi ro: đổi từ “đã giải” sang “giả thuyết” ở thân rồi vẫn giữ khung; hoặc biến không đo được thành kết luận API6 sai.

ĐÃ THỬ NGHIỆM:

- `python3 -B do-luot5/logic.py` rc=0: phản ví dụ số học `(44,4)+(-1,0)=(43,4)`, `matches_claimed_43_4=true`. Không mô phỏng hay tự tạo response GitHub.
- `python3 -B do-luot5/audit.py ci arithmetic` rc=0: tĩnh Windows 6/Linux 4 false; hai mốc được khai chênh **384 s =6,4 phút**. JSON ghi rõ nguồn là prose, không API replay.
- `python3 -B do-luot5/sources.py` rc=0: lưu các câu đối nghịch. Lệnh con `git grep` các run ID/mốc ngoài LAND ở HEAD trả rc=1, stdout rỗng. Quét `git log --all -G ...` tìm thêm hai commit `be47638`/`ee0bdd8` của land #477: đọc blob thấy cùng lời attestation43/1→44/6, không có raw response. Lệnh quét đầy đủ và output lưu trong `sources-audit.json`/`ci-source-history.txt`.
- **KHÔNG ĐO ĐƯỢC** các giá trị API, sáu timestamp thật, số null lúc đọc cũ, thời điểm gọi cũ và việc điều phối thực sự đọc giữa chừng: không mạng, không response/log gốc tương ứng trong nguồn tìm được. Không kết luận cơ chế được đề xuất là bất khả hoặc chắc chắn sai; lỗi P1 là khai đã xác lập nguyên nhân khi chưa đủ căn cứ.

ĐỘ TIN: **cao** về lỗi suy luận, phạm vi lời khai và mâu thuẫn thân/khung; nguyên nhân lịch sử thật chưa biết.

### land-evidence-pr477-chua-merge-trai-nguon-moi  [P1]  Bookkeeping vẫn khai PR477 chưa merge dù khối mới dùng chính merge đó

TỆP/DÒNG: LAND:292; đối chứng 164–165; Git commit `585c7d510e026b4ea5a2b395c69581f24c1d8fa0`.

VẤN ĐỀ: câu hiện hành “PR #477… đang chạy vòng vá/cross-review riêng, chưa merge” không gắn nhãn trạng thái cũ hay mốc hết hiệu lực. Khối mới ngay trong cùng tệp đã gọi `585c7d5` là merge commit PR477 và dùng run sau merge làm căn cứ. Git snapshot có commit hai parent, tiêu đề Merge pull request #477, timestamp **01:22:38Z**, nằm ở master; bản vá933 được commit **02:27:22Z**, sau đó **1 giờ4 phút44 giây**. Đây là lời trạng thái đã cũ được giữ như hiện hành trong hồ sơ đang cập nhật, có phản chứng trong gói; không chỉ thiếu API để kiểm.

ĐÃ THỬ VÁ: **không sửa PR** — sửa dòng bookkeeping thành trạng thái đúng **theo Git snapshot**, neo merge SHA; nếu cần giữ câu cũ, ghi rõ nó thuộc snapshot trước merge và đã hết hiệu lực. Không suy đã merged thành CI đạt/landed/Mission complete. Ca kiểm: đối chiếu toàn tệp với `585c7d5`, không còn đồng thời “merge của #477 đã đo” và “#477 chưa merge” ở cùng mức hiện hành. Rủi ro: xoá nợ review/CI đi kèm chỉ vì thấy Git merge.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py git` rc=0. `git -C cay-kho show -s --format='%H %P %cI %s' 585c7d5 9337779` trả hai mốc nêu trên; parent của 585 là `802fc01…` và `75fe4c4…`. `git -C cay-kho merge-base --is-ancestor 585c7d5 master` rc=0, `git -C cay-kho rev-parse master` đúng 585c7d5. Nguồn trong `git-audit.json`. Trạng thái PR477/CI trên **GitHub API hiện tại: KHÔNG ĐO ĐƯỢC**, vì không mạng; finding dựa Git object và sự tự mâu thuẫn trong văn bản.

ĐỘ TIN: **cao** trong snapshot và nội dung hồ sơ.

### land-evidence-khai-dong-p3-khi-con-sot  [P1]  Khai đã vá nốt P3 dù phần việc được verdict 15 nêu vẫn còn nguyên

TỆP/DÒNG: LAND:124; `ops/reviews/full-gate-pr468-20260907/README.md:57`; `ops/reviews/pr468-hoso-4-packet-review-15-codex-verdict.md:80`.

VẤN ĐỀ: bản vá17f4a1b sửa thật bảng phân loại/phương pháp. Tuy nhiên verdict 15 nêu đích danh câu “muốn đối chiếu byte gốc phải chạy lại”, giải thích chạy mới sinh log mới, và **gộp toàn bộ vào P3 cũ**. Câu đó vẫn nguyên byte ở README hiện hành; cả hai commit lượt này không sửa nó hoặc hạ lời đóng trong LAND. Vì vậy “vá nốt P3 duy nhất còn lại” khai sai về **mức hoàn tất công việc đã xảy ra**.

Đây là P3 về README ở verdict 15/lượt 4, nhưng đối tượng P1 ở lượt này là **lời đóng nợ không đúng trong land record**, đúng quy tắc phân hạng người dùng giao. Không tuyên bố lỗi raw-log gốc tự trở thành lỗ hổng P1, không nâng hạng chỉ vì nó lặp lại.

ĐÃ THỬ VÁ: **không sửa PR** — cách ít thay đổi nhất là ghi “vá phần bảng/phương pháp; còn câu về raw-log phải làm rõ”. Hoặc sửa câu hiện hành, cập nhật manifest của gói theo nội dung mới rồi đo, và chỉ khai đóng ở commit thực sự hoàn tất. Giữ nguyên verdict lịch sử. Ca kiểm: đối chiếu mọi mỏ neo mà verdict 15 gộp vào P3 với trạng thái trong LAND. Rủi ro: cập nhật README làm hỏng manifest, hoặc chạy lại rồi gọi log mới là byte lịch sử đã mất.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate` rc=0 ghi `leftover_prose` tại dòng 57 và `verdict15_prose` tại dòng 80. `python3 -B do-luot5/sources.py` rc=0 lưu diff17f4a1b: đổi bảng và thêm phương pháp, không đổi câu còn sót. `git -C cay-kho diff 745d888 17f4a1b -- ops/reviews/full-gate-pr468-20260907/README.md` rc=0 xác nhận cùng diff. Hai commit 83e4786/9337779 chỉ sửa LAND. Không cần phục hồi hay đoán raw stdout để chứng minh lời “vá nốt” chưa đúng.

ĐỘ TIN: **cao**.

### land-evidence-gioi-han-chua-phu-het-loi-khai  [P3]  Giới hạn đã thêm chưa phủ hết các sự kiện chỉ có lời tự khai

TỆP/DÒNG: LAND:130,209,216–227,269–273,290; phần đã sửa thật ở41–47,94–99.

VẤN ĐỀ: authorization và model/effort nay giới hạn đúng. Nhưng “full-gate chạy MỘT lần”,71 s, snapshot23:43:30Z, lịch sử thiếu đúng 23 tag và Issue/Mission open chưa được bao bởi giới hạn toàn tệp hoặc giới hạn riêng phù hợp. Có log/nội dung khớp một phần không xác thực lần chạy, hành động fetch hay API state lịch sử. Không có bằng chứng để gọi những sự kiện này sai; giữ P3 về provenance. Phần #477 có phản chứng đã tách P1, không đếm lại ở đây.

ĐÃ THỬ VÁ: **không sửa PR** — thêm giới hạn nguồn cho các nhóm còn lại, giữ riêng số reviewer tái tính được. Ca kiểm: inventory mọi khẳng định hiện hành có nguồn, mốc chụp và mức attestation tương ứng. Rủi ro: một nhãn chung mơ hồ làm cả số đã đo thành “không đo được”, hoặc coi attestation là xác nhận độc lập.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate reviews bookkeeping` và `python3 -B do-luot5/sources.py` rc=0. Chỉ có một bộ full-gate, không launcher gốc; doc JSON chênh một reason7 byte; ref spec đúngr6 nhưng câu trạng thái vẫn là nguồn tự khai. Lần lease mới66,316 s không chứng minh/bác71 s lịch sử. **KHÔNG ĐO ĐƯỢC** tổng invocation,71 s lịch sử, snapshot23:43:30Z, số tag thật từng thiếu và API Issue/Mission: thiếu nguồn thô tương ứng, không mạng.

ĐỘ TIN: **cao** về phạm vi thiếu nguồn; không kết luận sự kiện không xảy ra.

Các finding về độ phủ dưới đây ghi nhận **số đúng hoặc giới hạn đã đối chiếu**, không phải thêm lỗi P1/P2 cho PR. Bản vá ở đây là bổ sung bảng của verdict, không sửa các giá trị đúng trong hồ sơ.

### bang-do-bo-sot-land-evidence-thu-hai  [P3]  Bảng bỏ thứ tự tệp land evidence

TỆP/DÒNG: LAND:16–17.

VẤN ĐỀ: “thứ HAI” không nằm trong bảng chín hàng. Đếm đúng loại YAML trên base/head khớp; không suy kho chỉ có hai tài liệu nói về land.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Giữ loại tệp và mốc Git khi thêm hàng; ca kiểm đếm lại base/head. Rủi ro là biến thứ tự tạo trong lịch sử thành tổng trên mọi ref hiện tại.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py git` — rc=0; land_files tại base có 1 path, reviewed tree có 2 path, plat-x8 có trước. File land477 trên ref khác là ghi nhận sau đó, không bác thứ tự tạo file468.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-mot-commit-chen  [P3]  Bảng kiểm numstat nhưng bỏ số commit trong khoảng

TỆP/DÒNG: LAND:123–124.

VẤN ĐỀ: Có đúng MỘT commit giữa head review và head merge; đo diff riêng tip không tự chứng minh điều ấy.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Bổ sung membership và cardinality của khoảng. Ca kiểm không chỉ đọc tip; tránh suy một diff thành một commit.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py git` — rc=0; between.stdout chỉ một dòng 17f4a1b85b8d5146c5e6dddbdc40f11111a659f7; git log --format=%H 745d888..17f4a1b rc=0.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-bon-cap-delta  [P3]  Bảng bỏ bốn cặp byte làm căn cứ DELTA

TỆP/DÒNG: LAND:132.

VẤN ĐỀ: DELTA0 đúng trên bốn cặp đã lưu, chưa có trong bảng giao; không mở rộng thành sáu stdout gốc.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Bổ sung từng cặp và loại raw/tail/norm. Ca kiểm so byte trên đúng bốn cặp; rủi ro là bỏ chuẩn hoá khỏi tên nguồn rồi gọi là byte thô.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate` — rc=0; pairs có 4 equal=true; byte mỗi vế 206,96,8827,70861.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-sau-bo-full-gate  [P3]  Bảng bỏ map sáu cặp mã thoát lịch sử

TỆP/DÒNG: LAND:132–133.

VẤN ĐỀ: Số 6 và map rc là lời khai định lượng khác kết quả lease/doc mới. Hai log tổng hợp ghi đúng map.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Bổ sung sáu số hạng với nhãn đọc log. Ca kiểm giữ lease1/1; tránh lấy rc0 của script đọc log làm rc0 của sáu suite.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate` — rc=0; nen.rc và sau.rc mỗi tệp6 record: cidk0, ploop0, lease1, doctrine-scan0, adr-song0, doc-claims-check0. Exit code lịch sử KHÔNG ĐO ĐƯỢC độc lập: thiếu launcher/raw provenance.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-out-khong-rong  [P3]  Bảng bỏ số stdout rỗng được khai trong full-gate

TỆP/DÒNG: LAND:134.

VẤN ĐỀ: “Không bộ nào out=0 B” có nghĩa0/12 trường out bằng 0. Năm bộ chỉ có số kích thước trong log tổng hợp.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm count 0/12 và nguồn trường log. Ca kiểm đếm cả hai vế; rủi ro là thấy tail dương rồi suy toàn stdout gốc được bảo toàn.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate` — rc=0; mỗi vế [2934,8752,8971,69,113,70861]B, tất cả dương. Kích thước raw lịch sử 5/6 bộ KHÔNG ĐO ĐƯỢC độc lập vì không có stdout đầy đủ.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-mot-phan-sau-stdout  [P3]  Bảng bỏ độ phủ một trên sáu stdout nguyên vẹn

TỆP/DÒNG: LAND:138.

VẤN ĐỀ: 1/6 là giới hạn quan trọng của bằng chứng full-gate, không có trong bảng giao. Inventory cho đúng cách phân rã ấy.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm cả tử/mẫu và loại hiện vật. Ca kiểm dựa inventory, không chỉ câu README; tránh gọi norm hoặc tail là stdout nguyên vẹn.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate` — rc=0; một doc JSON raw 70861 B, hai tail206/96 B, lease norm8827 B khác out khai 8971 B, doctrine/adr không output. Sáu bộ =1 raw + 2 tail + 1 norm + 2 vắng.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-lease-truoc-merge  [P3]  Bảng bỏ 120/121 trước merge khi yêu cầu121/121 mới

TỆP/DÒNG: LAND:136–138,211–212.

VẤN ĐỀ: 120/121 trước merge là lời khai riêng, không thể thay bằng kết quả xanh mới. t33 đã chạy và đỏ tiền điều kiện; thao tác lint bên trong chưa chạy.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm hàng trước merge với passed/failed/skipped tách riêng. Ca kiểm giữ121 đã chạy và 0 bỏ qua; rủi ro sửa số cũ thành xanh của hôm nay.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py fullgate` — rc=0; hai norm bằng byte, cuối log120/121 đạt; đã chạy 121, bỏ qua 0; t33 báo thiếu actionlint. Đây là đọc log gốc, không chạy lại suite quá khứ.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-byte-lease  [P3]  Bảng bỏ 8649 byte stdout lease

TỆP/DÒNG: LAND:209.

VẤN ĐỀ: Bảng giao nêu 121/121, không nêu 8649 B. Lần chạy mới đúng 8649 B trên reviewed SHA; không tự xác thực 71 s hoặc byte của lần chạy lịch sử.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm byte vào bảng, ghi exact SHA và tách stderr. Ca kiểm wc -c trên stdout đã lưu; rủi ro cộng stderr để tạo mismatch giả.

ĐÃ THỬ NGHIỆM: `cd cay-kho && python3 -B ops/lease_publish_test.py` — Với môi trường công cụ/TMPDIR đã mô tả: rc=0; 121/121, chạy 121, bỏ qua 0; stdout 8649 B, stderr 56 B; 66,316 s. do-luot5/lease.json và lease.stdout/lease.stderr lưu số thật; không chạy lại chỉ để đếm byte.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-chin-manifest-truc-tiep  [P3]  Bảng bỏ tổng 13, 9 direct và ba tỷ số ánh xạ

TỆP/DÒNG: LAND:230–233.

VẤN ĐỀ: Bảng lượt 5 đã nêu 3 bố cục + 1 băm trần nhưng bỏ tổng 13, 9 direct và 128/178/48; đây vẫn là phần phải đo.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm phân rã, giữ băm trần ngoài mẫu số 967 record. Ca kiểm dùng sha256sum -c đúng layout; rủi ro đổi hash để làm layout sai xanh hoặc nhân bản layout thành gói mới.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py manifests` — rc=0; base có 12 ARTIFACTS + 1 bare; 9 direct rc=0 = 613 mục; mapped 11/12/13 rc=0 lần lượt 128/128, 178/178, 48/48; tổng 967 ARTIFACTS khớp; bare hash e60c376ab385ccc9b3cc8d2cdd87620b2110c8a68e607c879a6100c6b3f9958c khớp.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-sau-buoc-if-sai  [P3]  Bảng bỏ phép đếm tĩnh sáu điều kiện sai

TỆP/DÒNG: LAND:151–157.

VẤN ĐỀ: Số 6 API ở bảng giao không bao gồm phép phân tích tĩnh độc lập. Base có 40 bước YAML; không so 40 với 44 API như cùng đơn vị.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm truth table và phân biệt số khai tĩnh với step do runner sinh. Ca kiểm từng if; rủi ro dùng static 6 để tuyên bố đã đo runtime 6 hoặc biết nguyên nhân lần ghi 4.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py ci` — rc=0; 40 steps, 10 if; push/master/Windows 6 false: PR EOL-base, don-nhanh, cgroup Linux, tl PR, ci-phamvi selftest, release-verify WORKER. Linux 4 false. API skipped KHÔNG ĐO ĐƯỢC vì không response/mạng.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-sau-loi-goi-review-spec  [P3]  Bảng bỏ 6/6 invocation của spec thu hồi

TỆP/DÒNG: LAND:269–270.

VẤN ĐỀ: Bộ đếm spec là invocation, khác số thứ tự cuối 5 và số verdict hoàn tất. Bảng giao lượt 5 bỏ cả mục này.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm count 6 và danh sách các hàng, giữ giới hạn authority. Ca kiểm không loại 4a hoặc đếm 5 số thứ tự thành 5 invocation; tránh gọi sáu hàng là sáu review hoàn tất.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py bookkeeping` — rc=0; spec-r6.md trích từ tip 2aee80a, §0 có 6 hàng 1, 2, 3, 4a, 4b, 5; hàng 4a chết vẫn tính, trần 6 hết. Runtime invocation/approval tăng trần KHÔNG ĐO ĐƯỢC độc lập: không log/response gốc.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-sau-thanh-phan-land  [P3]  Bảng bỏ sáu thành phần của nghĩa vụ land evidence

TỆP/DÒNG: LAND:3–6.

VẤN ĐỀ: Câu mới “đúng sáu thứ” là số lượng ngoài hàng viện dẫn nguồn. Sáu thành phần có thật trong ADR, không chỉ số hiệu văn bản đổi.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm sáu thành phần vào bảng. Ca kiểm nội dung nguồn lẫn đối tượng áp dụng; rủi ro coi đủ sáu tên trường là sáu nghĩa vụ thực tế đều đã được xác minh.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/sources.py` — rc=0; đoạn ADR-0034:17–20 liệt kê Approver, authorization, operator, merge commit, post-merge gate, bookkeeping; Protocol:466–488 có trường tương ứng.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-snapshot-dem-review  [P3]  Bảng bỏ 307 nhánh và 62 tag của snapshot dẫn cho bộ đếm

TỆP/DÒNG: LAND:85.

VẤN ĐỀ: 307/62 là bộ số hiện hành trong câu mô tả phép đếm cũ; bảng giao chỉ đưa 10 verdict. Verdict lượt 4 ghi 307/62, còn gói lượt 5 đã 309/62. Chưa có căn cứ coi chênh snapshot là khai sai sự kiện lịch sử.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm mốc/số của cả hai snapshot, không thay 307 bằng 309 trong ghi nhận cũ. Ca kiểm scope thời gian; rủi ro biến một số snapshot thành bất biến của kho.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py git` — rc=0; for-each-ref trực tiếp 309 heads, 62 tags; VERDICT-LUOT4.md hàng năng lực snapshot ghi 307/62. Tập ref máy chủ/lịch sử 307 ở thời điểm tác giả đo KHÔNG ĐO ĐƯỢC độc lập tại đây.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-map-p1-theo-luot  [P3]  Bảng bỏ cả map P1 theo từng verdict

TỆP/DÒNG: LAND:100–106.

VẤN ĐỀ: Bảng lượt 5 bỏ map 9 số hạng. Tất cả đều khớp heading finding; số 0 không tự thành approve hay approval cho head khác.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm map và cách đếm heading. Ca kiểm không đếm các lần nhắc P1 ở phần đối chiếu; rủi ro trộn P1 đã đóng được nhắc trong prose với finding hiện hành.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py reviews` — rc=0; P1 lượt 7→15 lần lượt 4, 2, 1, 1, 1, 2, 0, 0, 0. Lượt 11 có blob/nội dung riêng và DOC-MANIFEST giải thích đánh số lại; không gộp vào 10.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-verdict-va-manifest-14-15  [P3]  Bảng bỏ phạm vi tám verdict trên base và hai gói thêm

TỆP/DÒNG: LAND:108–110.

VẤN ĐỀ: Bảng giao chỉ nói 10 verdict, không nói 8 trên base, 2 thêm cùng PR và 59/59, 45/45. Tổng 10 đúng không tự xác nhận provenance/integrity hai gói mới.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm hiện diện tại exact base/head và hai tỷ số. Ca kiểm blob ancestry lẫn checksum; rủi ro suy hash pass thành xác nhận identity model hoặc GitHub giữ URL vĩnh viễn.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py reviews manifests` — rc=0; cat-file -e base:path: lượt 6–13 rc=0, 14/15 rc=128; ở head đủ 10. sha256sum -c từng gói 14/15 rc=0, 59 OK và 45 OK.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

### bang-do-bo-sot-ket-qua-luot-cuoi  [P3]  Bảng bỏ số finding của verdict cuối

TỆP/DÒNG: LAND:115–121.

VẤN ĐỀ: Ngoài chỉ số 15 đã ở hàng 1, luot_cuoi còn khai 0 P1/0 P2/1 P3 và approve trên 745d888; bảng bỏ các số này.

ĐÃ THỬ VÁ: có — bổ sung BẢNG ĐO của verdict này. Thêm kết quả và reviewed SHA cạnh nhau. Ca kiểm không mang approve của cha sang con; rủi ro dùng 0 P1 của lượt 15 để tuyên bố head merge đã review hoặc P3 đã sửa hết.

ĐÃ THỬ NGHIỆM: `python3 -B do-luot5/audit.py reviews` — rc=0; verdict 15 neo 745d8889d0d6468785f26003876ba823c8b2db99, verdict approve; heading P1=0, P2=0, P3=1. Không có verdict 15 trên 17f4a1b.

ĐỘ TIN: cao về phép đếm/nội dung hiện vật; giới hạn lịch sử đã nêu riêng.

