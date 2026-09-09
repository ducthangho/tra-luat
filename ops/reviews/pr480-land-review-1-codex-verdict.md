verdict: changes_requested
reviewed_sha: afddf7efe21e784fd22ed6b5aed399bc9d04a67d
base_sha: 585c7d510e026b4ea5a2b395c69581f24c1d8fa0
luot: 1
so_lan_luot_nay_bi_chet_va_phong_lai: 0

Review lượt thứ 1; 0 lần chết/phóng lại được quan sát trong lượt này. Reviewer Codex/OpenAI, thực thi công cụ cục bộ qua API; không xác nhận model/effort lịch sử từ tên tài khoản GitHub. Reviewed tree: `32254b3b440be32af51bd8ad0326b626e03e6b02`.

**CHẶN MERGE: 1 finding P1, 4 finding P2, 3 finding P3.** P1 nằm ngay phần khẳng định cơ chế/số cuối “đứng vững”: cặp tổng không chứa bằng chứng chuyển trạng thái từng bước. Không kết luận số 6 bước skipped sai; kết luận hồ sơ khai chắc chắn hơn nguồn cho phép.

Đã ghi verdict sớm khi xác định P1, sau đó bổ sung bản hoàn chỉnh này. Chỉ đọc hiện vật trong gói; ghi dưới `do-review/`, `cay/` và `VERDICT.md`. Không mạng, không CI, không chạy bộ test dài, không sửa `cay-kho/`, không thay timeout.

Các số hiệu PR/ADR, SHA, phiên bản, dòng nguồn và giá trị schema là **định danh**, không phải đại lượng đo. Mỗi số đếm/phép so dưới đây nêu đơn vị. `ok: true` của wrapper chỉ xác nhận mệnh đề hẹp được mô tả trong JSON, không chứng minh cả land evidence đúng.

## BẢNG ĐO

Bảng thủ công có 106 hàng đối chiếu, tách sự kiện API khỏi nội dung Git và số học. Mỗi hàng thuộc đúng một ô. “Khớp” ở hàng nội dung tệp không xác thực sự kiện mà tệp thuật lại. Bảng không chỉ liệt kê lỗi.

| khẳng định (dòng) | hồ sơ khai | tôi đo được | ô | khớp? |
|---|---|---|---|---|
| 1 | Land cho PR #477, chuẩn hoá gói và t33 | Commit merge 585c7d5 ghi đúng chủ đề; script và báo cáo t33 có trong cây | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 3 | Land evidence thứ ba, sau plat-x8 và #468 | Lịch sử thêm tệp: 0a0c1a4 → 7ae7619 → be47638 theo mốc Git. 3/3 tệp có commit thêm; không phải 3 tệp trong checkout này (checkout có 2 tệp) | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 4 (ô bảng ADR) | PROTOCOL §20 ghi ADR-0045 có 0 cổng | Dòng 1147 ghi đúng 0 cổng cho ADR về đảo vai | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 4–5 (suy rộng) | Lấy ô ADR-0045 làm căn cứ không bộ kiểm nào cưỡng chế land evidence; chỉ cross-review bắt được | ADR-0045 nói ngoại lệ đảo vai; ADR-0034:17–20 mới quy định land evidence. Ô 0 cổng của một ADR không chứng minh mệnh đề về mọi bộ kiểm | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 7 | schema_version mang giá trị phiên bản 1 | yaml.safe_load đọc được số hiệu schema 1; chưa có kiểm schema land được viện dẫn | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 8 | mission_id là pr-477 | Đo được giá trị định danh; không có Packet/Mission gốc PR #477 để xác minh ánh xạ | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 9,13 | generation 1 và danh sách input_packet_generations gồm generation 1 | 1 giá trị đầu vào trong YAML; generation thực của Packet không có nguồn gốc kèm theo | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 10–12 | provider/recorded_by claude, role land_operator | Lời khai danh tính/vai trò phiên; metadata commit không xác thực runtime của phiên | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 15,20 (object) | Head 75fe4c43c47c9e2a0495f7de46942c9e26320a92 | 1/1 OID head khớp cha thứ hai của merge 585c7d5; git.json ok: true | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 16–20 (API) | notebyme88 APPROVED, khác tác giả ducthangho; URL review 5136229055; mốc 2026-09-08T00:54:34Z; đúng head | Không mạng, thiếu JSON review/PR; so hai chuỗi khác nhau không chứng minh độc lập người duyệt | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 20 (review) | Lượt review thứ 6 đọc đúng head 75fe4c4 | Không tìm thấy verdict gốc PR #477; chỉ có lời thuật lại | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 21 (số commit sau duyệt) | Đẩy thêm 4 commit sau khi được duyệt tại 14dab5e | git rev-list 14dab5e..75fe4c4 có 5 commit, danh sách 5/5 OID đọc được. Thiếu mốc approval/push/dismiss nên không suy 5 commit đều được đẩy sau duyệt hoặc bác số 4 theo thời gian | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 21–22 (API/phiên) | Review cũ DISMISSED vì push; lỗi vận hành lần thứ 3 trong phiên | Không có timeline phê duyệt hoặc log thao tác phiên | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 24–25 | merge_method merge; merge_commit 585c7d510e026b4ea5a2b395c69581f24c1d8fa0 | Git object có 2/2 cha 802fc01 và 75fe4c4; chứng minh topology merge, không phải đối số API đã gọi | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 26 | merged_at 2026-09-08T01:22:39Z | API KHÔNG ĐO ĐƯỢC. Git committer time là 2026-09-08T01:22:38Z UTC, khác trường merged_at nên không chấm lệch 1 giây | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 27–31 | land_operator và merged_by.login là ducthangho, đọc qua pull_request_read(get) | Thiếu JSON PR #477; đây đã được ghi rõ là attestation | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 29,113 (phạm vi hiện vật) | Không kèm JSON thô PR/run/job làm nguồn cho các mốc đang xét | Không có đường dẫn/hash nguồn được viện dẫn cho các lần đọc này; tra hiện vật liên quan chỉ thấy lời thuật lại. Không khẳng định toàn kho không có JSON của những run khác | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 33–38 | Phiên Claude merge bằng PAT, chủ kho không tự bấm; chỉ thị nguyên văn cho phép merge/land; không có URL bền | Nguồn duy nhất được khai là chính land evidence; không có vết phiên/JSON để đối chứng | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 35–36,108–111 | merged_by không phân biệt người với phiên; không có trường GitHub phân biệt | Không có payload/nhật ký để quy người thao tác. Phần khẳng định toàn bộ khả năng API không xác minh từ sandbox; không suy người thật từ tên tài khoản | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 40–41 | PR #468 bị classifier từ chối; chủ kho tự bấm; PR #477 gọi được; điều phối không tìm đường vòng ở cả 2 lần | Không có log classifier, thao tác hay transport. Land #468 mới cũng chỉ thừa nhận không biết UI hay API | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 44–48 | 6 lượt review; reviewer codex, executor claude, model gpt-6-astra, effort xhigh | Không có verdict gốc hoặc runner metadata PR #477; không lấy tên model trong commit làm phép đo model thực | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 49 (map) | P1 mở ở lượt 1→6: 1,1,1,0,0,0 finding P1 | Không đếm trực tiếp được lượt nào của PR #477. Tóm tắt executor nêu các số tương thích; không thay verdict gốc | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 50–52 (nguồn) | Đã đếm heading P1 trên verdict từng lượt; phân biệt heading đóng/mới ở lượt 3 và lượt 4 | 154/154 blob verdict được tra; chỉ 3 blob nhắc #477, đều là verdict PR #478. Nguồn đếm trực tiếp được tuyên không có trong gói; chưa đánh nhãn nguồn thứ cấp | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 53–59 | Lượt cuối thứ 6: approve, 0 finding P1, 0 finding P2, 2 finding P3, reviewed_sha 75fe4c4 | Commit b789e73 thuật lại đúng số, không có verdict gốc để xác nhận; KHÔNG coi số heading tìm được là 0 finding | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 60–62 | khop_head_da_merge true; không có nợ head chưa review | Git xác nhận head đã merge; vế reviewed_sha dựa duy nhất lời khai. Kết luận đóng nợ review mạnh hơn bằng chứng có thể đối chiếu | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 62 (đối chứng #468) | PR #468 còn nợ head chưa review | Verdict cuối #468 neo 745d888; merge 802fc01 có cha 17f4a1b; nguồn land468 giữ nợ. 2/2 OID khác nhau đúng như nguồn | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 64–68 (đếm mục) | SÁU lần bản vá tự sinh lỗi mới | Đọc thủ công có 6/6 mục: PATH, rm, mktemp, chốt muộn, t27, receipt. rm có 2 hậu quả nhưng là 1 mục/bản vá; không đếm thành 7 lần | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 64–68 (lịch sử) | Cả 6 mục là sự kiện đã xảy ra do bản vá | Các commit chứa 6/6 mô tả tương ứng, có diff hỗ trợ các thay đổi mã/receipt; thiếu runner/hiện vật A/B để tái xác minh đủ 6 sự kiện. Chốt muộn chỉ nằm trong lời thú nhận ở commit 37d66a6 | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 64 (mã) | Bản vá prepend PATH cho phép che lệnh hệ thống | Diff 3d2ac9b thêm PATH trước vòng gọi công cụ theo tên; a6a5222 gỡ nó. 2/2 trạng thái mã đối chiếu được | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 65 (mã) | Bản vá rm -rf đi qua thành phần symlink và phá archive offline | a6a5222 thêm xoá AL_DICH trước installer; 4d4137f thay bằng chốt symlink + mktemp. Cấu trúc thứ tự mã khớp; không chạy xoá dữ liệu | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 65–66 (mã) | mktemp tạo lần cài mới khi dựng lại cùng gói | 4d4137f thêm mktemp; 37d66a6 thêm chốt đầu vào đã dùng. Đối chiếu 2/2 trạng thái mã | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 66 (số học) | Manifest 2142→2154→2166 | 2/2 hiệu số đều 12 tệp. Đây chỉ là số học có điều kiện; không xác minh số hạng lịch sử | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 66 (lịch sử) | Manifest có 2142, 2154, 2166 mục; chốt muộn làm OK=1520/2136 mục | Không có các gói và manifest lịch sử; commit 37d66a6 chỉ thuật lại. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): không chạy dựng gói/test dài để sinh số mới | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 67–68 (cấu trúc) | Vá thêm verdict thiếu mục lục/receipt, rồi thêm receipt thiếu anchor | 260f7c6 thêm 2 tệp receipt và 2 hàng mục lục; 5a4dd85 thêm anchor. Khớp diễn biến nội dung Git, không tự chứng minh màu gate lịch sử | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 67–68 (kết quả gate) | t27 ĐỎ rồi cổng receipt v2 ĐỎ | Không có output runner tương ứng trong tệp dẫn nguồn; không chạy các bộ test ngoài danh sách ngắn | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 71–72 | Trước merge bộ lease 121/121 ca đạt; chạy 121 ca, bỏ qua 0 ca; actionlint đúng pin; rc=0 | Log t33 đính kèm neo b416830/f77f198, không phải 75fe4c4. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): không chạy lại bộ test lease; chạy mới cũng không xác thực phiên lịch sử | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 73–74,91–92 (lịch sử) | shellcheck trước/sau merge rc=0 | Không có capture lịch sử; rc=0 được chép không phải bằng chứng dương | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 73–74,91–92 (tái đo mã) | Script vừa land sạch shellcheck | shellcheck -f json trả danh sách rỗng, 0 chẩn đoán; wrapper ok: true. Blob script giống nhau ở 75fe4c4/585c7d5/afddf7e | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 75 | Tên phép kiểm CI trên exact head 75fe4c4 | Dòng 80 tự rút tính exact-head nhưng nhãn chính còn khẳng định nó; checkout không khai ref head. Không được dùng nhãn này chứng nhận exact-head CI | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 76 | Run 34171856469 pull_request success; Ubuntu 44 bước, 0 bước hỏng, 3 bước skipped | Không JSON run/job, không mạng; ID run chỉ là định danh, không phải bằng chứng nội dung | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 78 (run thực) | Lượt PR chỉ có 1 job Ubuntu | Không có response; matrix tĩnh chỉ hỗ trợ nếu PR không có nhãn windows | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 78–80 (giới hạn) | PR xanh không chứng minh Windows hoặc CI exact head; checkout merge tổng hợp | YAML matrix phụ thuộc event/ref/nhãn windows; actions/checkout không khai ref. Đo cấu hình chỉ đủ kết luận thiếu chứng cứ exact head/Windows, không xác thực checkout thực | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 84 (Git) | Head 75fe4c4 đã vào merge/master | Cha thứ hai của 585c7d5 chính là 75fe4c4; nhánh không có commit ngoài 585c7d5, git.json ok: true | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 84 (ref lịch sử) | origin/master lúc đo = 585c7d5 | Snapshot nay master=da481f9 và không có refs/remotes/origin/master do thiết kế gói. Không có ảnh ref tại lần land; không chấm lệch từ ref mới | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 85–86 | Nhánh không còn commit ngoài master, 0 commit | git rev-list --count 585c7d5..75fe4c4 = 0 commit; quan hệ cha xác nhận kết quả dương, ok: true | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 87–88 | Bộ lease sau merge 121/121 ca, chạy 121 ca, bỏ qua 0 ca; rc=0 | KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): bộ test lease không thuộc lệnh ngắn được phép; thiếu log neo 585c7d5 | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 89–90 (phân nhóm) | Tổng 81 biên nhận, 11 legacy, 42 nợ, 28 còn lại | Đếm 81/81 tệp; 11/11 băm allowlist khớp; 42/42 băm nợ khớp; còn 28/28 tệp khai schema v2. Có 29 tệp khai v2 nếu đếm cả nợ, nên không nhầm raw schema count với nhóm đạt | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 90 (validator) | 28 ĐẠT v2, 0 vi phạm, TỔNG ĐẠT | Kiểm tĩnh phân nhóm không chứng minh validate đầy đủ. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): không chạy cổng receipt ngoài danh sách lệnh ngắn; thiếu capture lần land | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 90 (số học) | 28 + 11 + 42 = 81 biên nhận | Tái tính đúng 81 biên nhận; so-hoc.json ok: true, độc lập với kết luận validator | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 93–94 | Dựng từ master thành công; 307 ref ở 3 nguồn, 0 ref lệch; manifest 3010/3010 mục | Không có gói lịch sử. Gói hiện tại là mốc 312 ref; không thay số 307 ref hoặc số 3010 mục bằng số mới. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): không chạy builder có mạng/ghi Git | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 95–101 (run API) | Run push 34176439015 neo 585c7d5, cả Ubuntu/Windows success | Thiếu JSON run/job/head/attempt; không xác nhận trạng thái GitHub từ Git commit | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 98 | Ubuntu 44 bước, 0 bước hỏng, 4 bước skipped | Không có response job; 40 bước YAML không phải mẫu số 44 bước API | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 99 (mốc) | Ubuntu bắt đầu 01:22:44Z, kết thúc 01:49:30Z | Hai mốc API không có hiện vật để xác thực | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 99 (phép trừ) | Thời lượng 26 phút 46 giây | Hai mốc được khai cách nhau 1606 giây = 26 phút 46 giây; đúng có điều kiện | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 100–101 | Windows 44 bước, 0 bước hỏng, 6 bước skipped; Complete job success | Không có response; không lấy 6 if sai làm 6 skipped thực tế | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 101 (mốc) | Windows bắt đầu 01:22:45Z, kết thúc 02:11:00Z | Hai mốc API không có hiện vật để xác thực | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 101,103 (phép trừ) | Thời lượng 48 phút 15 giây | Tái tính từ mốc khai ra 2895 giây = 48 phút 15 giây | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 103 | timeout-minutes 60 phút | YAML gate khai 60 phút; ci-tinh.json ok: true. Không thay workflow | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 103,105–106 | Dưới trần; còn khoảng 11 phút 45 giây; sát trần | 3600 giây − 2895 giây = 705 giây, tức 11 phút 45 giây; “sát” là đánh giá, chưa có ngưỡng riêng; không suy thời lượng thực từ phép trừ | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 104–105 | Packet GATE/Issue #463 nhằm cắt wall-clock bằng tách job, không nâng trần | Spec GATE-TACH-JOB-CAT-CHI-PHI và bản Issue trong cây ghi mục tiêu tách job; đây là nội dung đặc tả, không chứng minh Issue trên GitHub hiện thời | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 106 | Success lần này không chứng minh vấn đề chi phí đã hết | Một kết quả job không nghiệm thu mục tiêu cắt chi phí; không thấy lời nghiệm thu packet trong phép đo được dẫn | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 112–113 | Các số CI và merge là attestation của điều phối | Đúng loại nguồn được tệp tự khai; điều này không làm các câu “ĐÚNG/ĐỨNG VỮNG” phía dưới thành đã đo | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 114–115 (nguồn được dẫn) | Đã tự khai mọi phép đo Linux+Bash trong DO-T33-VA-GOI-REVIEW-20260907.md | Bản tài liệu tại reviewed SHA không có đoạn tự khai Linux+Bash/macOS/Windows native; đoạn ấy chỉ được thêm ở b789e73. Đang dẫn bản chưa chứa nội dung đã tuyên | ĐO ĐƯỢC + LỆCH | Không |
| 114–115 (thực thi) | Không đo macOS/Windows native, mọi phép đo trên Linux+Bash | Không có runner identity của toàn bộ phép đo lịch sử; sandbox lượt này cũng không cung cấp hai nền ấy | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 118–122 (lịch sử văn bản) | Khối cũ tên giai_mau_thuan_4_vs_6_skipped, chốt đọc giữa chừng, đã bị rút | Git show ee0bdd8 và diff afddf7e chứa việc đổi khối; tên khoá và mệnh đề cũ đối chiếu được | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 120–121 (verdict #478) | P1 land-evidence-chot-nguyen-nhan-chua-quan-sat ở lượt 5 đã được chấm | Verdict PR #478 lượt 5 trong refs/heads/master có đúng heading P1 ấy; lượt 6 xác nhận đóng với nhãn attestation | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 119–120 (phiên) | Đã dặn phiên khác lan truyền và phiên ấy đã làm | Có văn bản đính chính ở cả hai nhánh; không có log giao/nhận để chứng minh hành động giữa các phiên | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 125–127 (văn bản) | Land #468 từng ghi mau_thuan_chua_giai: 43 bước/4 skipped, merge 802fc01, run 34169756563 | Các blob lịch sử của land #468 có lời khai đó. Đo được văn bản từng viết, không đo được response đã sinh số | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 126–127 (API) | Lần đọc cũ thực tế trả 43 bước/4 skipped cho Windows run 34169756563 | Thiếu response lần đọc cũ và job ID/attempt | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 127–128 (phân tích tĩnh) | 6 bước if sai với push/master/windows | YAML có 40 bước khai báo, 10 if; 6/6 điều kiện false trên Windows, 4/4 trên Linux. File workflow cùng blob tại 802fc01,585c7d5,afddf7e | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 127 (nguồn review) | Chính cross-review #478 lượt 2 đã làm phép phân tích ấy | Verdict gốc lượt 2 không có trong phạm vi hiện vật tìm được; tóm tắt lượt sau là nguồn thứ cấp | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 130–131 (số API) | Đọc lại job cũ completed: 44 bước, 6 bước skipped, 0 bước null | Không JSON response/job ID/attempt; số 6 không bị chấm sai vì không đo được | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 130–131 (mức bằng chứng) | Số ĐÚNG là 6, phần này ĐỨNG VỮNG | Khẳng định chắc chắn trong khi nguồn chỉ là attestation. Bản #468 được viện dẫn giữ rõ giới hạn ấy; tệp #477 đã bỏ nó ngay ở kết luận | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 132–134 (nguồn API) | Đo trước/sau cùng job run 34176439015: 43 bước/1 skipped → 44 bước/6 skipped | Không có 2 response, job ID hoặc attempt để đối chứng “cùng job”, trạng thái và số liệu | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 133–134 (số học) | Biến động tổng của cặp khai | Nếu nhận số khai: tăng 1 bước tổng, tăng 5 bước skipped; 2/2 hiệu số tái tính được | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 135–136 | Cặp số chứng minh bước chưa chạy có null, đếm giữa chừng thấp hơn thực tế | Không có trường null hoặc đối chiếu từng bước trong cặp tổng; phản chứng tổng cho cùng số bước/skipped nhưng số null khác nhau, ok: true. Cơ chế chưa được phép đo này chứng minh | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 138–139 | Chưa xác định nguyên nhân lần đọc 43 bước/4 skipped; chứng minh tồn tại không chứng minh gây ra | Phân biệt logic đúng; dữ liệu còn thiếu nên không có cơ sở chọn nguyên nhân cụ thể | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 139 (hai lý do) | Cả 2 lý do đều đo được | Chỉ phép số học tái tính được; lý do về mẫu API 1 skipped vẫn là lời khai | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 140–143 | Phản ví dụ đọc Ubuntu 44 bước/4 skipped rồi ghi nhầm 43 bước; lấy số tranh cãi làm chuẩn là không hợp lệ | (44 bước − 1 bước, 4 skipped + 0 skipped) = (43 bước, 4 skipped), ok: true; chỉ phản ví dụ logic, không khẳng định có lỗi ghi chép thực | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 141–145 (Ubuntu API) | Ubuntu completed thực có 44 bước/4 skipped | Không có response; việc khớp số học không xác thực hai số hạng | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 144 (mức bằng chứng) | Mẫu giữa chừng ĐO ĐƯỢC ở đây là 1 skipped | Gói không kèm mẫu ấy; phải ghi “điều phối khai 1 bước skipped” | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 145–147 | Mẫu 1 skipped không neo riêng số 4; đọc nhầm cũng chưa được chứng minh; không có lời giải duy nhất | Không thể chọn giả thuyết từ các tổng hiện có; phản ví dụ số học giữ nhiều khả năng | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 148 | Thời điểm gọi API không được ghi ở đâu; không phép đo nào phân định được | Sandbox chỉ biết không được cung cấp hiện vật; không thể xác nhận sự vắng mặt ở mọi nơi hoặc mọi phép đo | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 150–152 | Chỉ dùng số cuối khi completed; in_progress phải ghi chưa đo được; kiểm thêm 0 bước null | Đây là đề xuất quy tắc đọc evidence, không phải cổng đã triển khai. Hợp lý nếu kiểm null là bổ sung; null=0 tự nó không đủ chứng minh job completed/response đầy đủ | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 153–154 | Không thể loại giả thuyết bằng chính số khai đang nghi ngờ | Phản ví dụ ghi nhầm đáp ứng cặp tổng, nên phép loại trong hồ sơ cũ thiếu tiền đề độc lập | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 156–159 (văn bản) | #468 đổi 3 tên khoá, có nguyen_nhan_that_su CHƯA XÁC ĐỊNH và 4 giả thuyết | Blob land468 tại c87b067 có 3/3 tên khoá mới, 4/4 giả thuyết (a)–(d) và mệnh đề chưa xác định | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 156 (phiên) | Phiên session_01C52eS8AgeiwTrDifXGDGYP thực hiện sửa | Không xác minh session identity từ Git và lời khai | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 156–158 (phạm vi đóng) | ĐÃ XONG, không còn việc cho ai; #478 lượt 6 xác nhận ĐÃ VÁ THẬT | Khớp nếu giới hạn ở P1 đính chính nguyên nhân: verdict #478 lượt 6 xác nhận đúng finding. Không đồng nghĩa hết mọi nợ; verdict ấy còn 23 finding P3 | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 158–159 (Git) | PR #478 đã merge tại c87b0679a837055ee4cc33ac48c9adb8d7ad8784 | Git object có 2/2 cha 585c7d5 + ff3431f, tiêu đề merge PR #478; xác minh sự hợp nhất trong Git, không xác minh API hiện thời | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 163,165–166 (nội dung) | 2 P3 nêu đúng slug t33-khong-chay-van-con-o-mo-dau và gioi-han-dung-goi-chua-tu-khai | Commit b789e73 có cả 2/2 slug và sửa 2/2 nội dung; bản ở 75fe4c4/585c7d5 còn lỗi mở đầu và thiếu mục giới hạn | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 163 (số P3/PR API) | Đó là 2 P3 của verdict lượt 6 và sang PR #479 theo chỉ thị chủ kho | Không verdict gốc hoặc JSON PR #479/chỉ thị; đối chiếu commit chỉ xác nhận nội dung bản sửa, không xác thực số hiệu PR hoặc toàn bộ verdict | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 164 | Mỗi commit đẩy thêm sẽ huỷ approval đã có | ADR-0034 quy định head đổi làm authorization stale. Cấu hình GitHub thực có tự dismiss hay không thì thiếu nguồn; tách nghĩa quy trình khỏi API | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 168 (nguồn PR) | Các giới hạn đã được tự khai ở PR #479 | Nội dung có ở commit b789e73. Gắn commit ấy với PR #479 trên GitHub không đo được | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 169 (mã) | Chỉ actionlint ghim; shellcheck/git/python3 tin PATH đầu vào | Script:122–161 kiểm AL_VER và binary cài riêng; :167–177 dùng type -P/--version, không so bản ghim cho 3 công cụ. Đọc đủ 3/3 nhánh công cụ | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 170 (thực nghiệm lịch sử) | Đặt bản giả đầu PATH vẫn rc=0, ghi version: 9.9.9 | Không có capture A/B; mã hỗ trợ khả năng tin bản giả nhưng không chứng minh lần chạy được kể | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 170–172 (mã) | Vẫn rm -rf kho.git/cay-kho; chốt symlink không xét R | 2/2 lệnh xoá hiện hữu tại :77,:86; chỉ kiểm thành phần con :76,:85,:134,:136; không có chốt R | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 171–172 (sentinel) | R symlink làm cả 2 sentinel bị xoá | Lời khai trong b789e73; không chạy builder/xoá dữ liệu. KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho): chỉ đọc mã và phép Python ngắn | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 174–175 (mã) | Lỗ any trong _kiem_bia_mo vẫn nguyên, ngoài phạm vi PR | lease_publish.py:605 dùng not any; diff base→head chỉ 1 tệp land YAML; mã runtime không đổi | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 175–176 (trạng thái) | Spec ở revision 6; 6/6 lời gọi đã hết; chặn kế là checkpoint | Đúng tại 2aee80a (6/6 hàng lời gọi), nhưng snapshot 0123ace đã có revision 8, 7/7 hàng lời gọi, ghi checkpoint mới. Không neo mốc nên không thể dùng lịch sử đó như trạng thái chặn hiện tại | KHAI RỘNG HƠN PHÉP ĐO | Không |
| 175–176 (authority API) | Trần review và quyết định checkpoint thực tế của chủ kho | Đo được nội dung spec, không xác minh comment/authority trên GitHub; không dùng spec mới tự cấp quyền tiếp tục cho ai | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| 178–179 (cấu trúc A9) | 4 lease GATE cấp trước hạn #456, 4 spec_hash khác nhau, generation giữ 1 | 4/4 tệp lease có mốc leased_at trước mốc hạn được khai 2026-09-07T14:30:07Z; 4/4 hash khác nhau, 4/4 generation mang giá trị 1. Đo nội dung YAML, không xác minh lần cấp trên server | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 178–179 (doctrine) | Thay revision/hash mà giữ generation lệch ADR-0034 | ADR-0034:7–8 đòi đổi contract thì revision và generation mới; 4 revision trong chuỗi đều generation 1; khớp nhận định về hồ sơ | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| 179 (trạng thái nợ) | A9 vẫn chờ quyết định chủ kho | Không API/comment hiện tại; không suy còn chờ hay đã xử lý chỉ từ lease đã hết hạn | KHÔNG ĐO ĐƯỢC | Chưa kết luận |
| Gói, ngoài diff | BANG-KHANG-DINH.tsv có 85 khẳng định định lượng | Chạy lại script khớp 85/85 dòng token trên 45 dòng nguồn; không phải 85 mệnh đề độc lập. Có 8 hit SHA chỉ gồm chữ số, đồng thời bị bắt ID; 4 hit “478 lượt” nhầm số hiệu PR | KHAI RỘNG HƠN PHÉP ĐO | Không |
| Gói, ngoài diff | 312 refs/heads được dựng có chủ ý | 312/312 tên+OID khớp cả 3 TSV và cây Git; không suy khớp server hiện thời; git.json ok: true | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |
| Gói, ngoài diff | Reviewed SHA/base và cây sạch | 1/1 tệp đổi, 179 dòng thêm, 0 dòng xoá; HEAD đúng full OID, detached, status 0 byte; git.json ok: true | ĐO ĐƯỢC + KHỚP | Có, trong phạm vi ghi ở cột đo |

Nguồn đo chính: [git.json](do-review/git.json), [ci-tinh.json](do-review/ci-tinh.json), [so-hoc.json](do-review/so-hoc.json), [receipt-static.json](do-review/receipt-static.json), [a9.json](do-review/a9.json), [spec.json](do-review/spec.json), [tim-verdict477.json](do-review/tim-verdict477.json). Lệnh tái đo ngắn: `python3 -B do-review/audit.py`; đầu ra gốc của các cổng nằm cạnh script.

## KẾT LUẬN RIÊNG CHO CÁC CHỖ MỀM

- **P1 theo lượt PR #477:** chưa đếm trực tiếp được cả 6 lượt, gồm lượt 1–3. Chỉ có thuật lại của executor. Các verdict tìm được và đếm thật là **PR #478**: lượt 4 có 0 heading P1 mở, 3 heading P2, 13 heading P3; lượt 5 có 3 heading P1, 0 heading P2, 17 heading P3; lượt 6 có 0 heading P1, 0 heading P2, 23 heading P3. Không dùng map ấy cho PR #477. [Bảng đếm](do-review/dem-verdict478.json).
- **Hai P3 cuối PR #477:** khớp 2/2 slug và 2/2 nội dung sửa trong commit b789e73; số P3 trong verdict gốc và ánh xạ sang PR #479 vẫn KHÔNG ĐO ĐƯỢC. Bản script vừa land còn lời mở đầu sai về t33 và chưa tự khai hợp đồng đầu vào; đúng là bản sửa nằm ở commit khác.
- **Chuỗi sáu lần:** đúng **6 mục được kể**; rm có 2 hậu quả nhưng cùng 1 bản vá. Không có bằng chứng đủ để đổi thành 7 sự kiện. Cũng không được gọi đây là 6/6 lần đã tái hiện: gói lịch sử thiếu, nhất là chốt muộn và các manifest cũ. Hiệu số 12 tệp đúng không chứng minh các số hạng 2142/2154/2166 mục đúng.
- **Giới hạn builder:** xác nhận trực tiếp từ mã: actionlint kiểm bản ghim và gọi binary riêng; 3 công cụ shellcheck/git/python3 tin PATH, chỉ kiểm chạy được/chuỗi version. Vẫn có 2 lệnh rm -rf và chốt bỏ qua R/cha. Chưa chạy lại tình huống giả công cụ/sentinel; không tuyên đã tái hiện lịch sử.
- **Mốc thời gian, run ID, merged_at, authorization_url:** sự kiện API đều KHÔNG ĐO ĐƯỢC do không mạng và thiếu response. Mốc Git đo được chỉ là metadata Git; không thay merged_at. Phép trừ thời lượng khớp có điều kiện. Đặc biệt chênh 1 giây giữa Git commit time và merged_at không phải finding về API.

## KHẲNG ĐỊNH BẢNG BỎ SÓT

Có 37 nhóm mệnh đề/trường bị bỏ hoặc bị rút còn token không giữ nghĩa. Các nhóm có thể chứa nhiều trường; không gọi số nhóm này là tổng số mệnh đề độc lập. Finding có hậu quả P1/P2 dùng chung slug ở dưới, không đếm lặp để tăng mức.

| dòng | khẳng định | vì sao bộ lọc trượt | hệ quả |
|---|---|---|---|
| 3 | Thứ ba trong chuỗi land evidence | Số thứ tự viết bằng chữ | P3: phân biệt lịch sử liên nhánh với số tệp checkout |
| 4–5 | Ô ADR-0045 chứng minh không bộ kiểm nào cưỡng chế land evidence | Mệnh đề suy luận, số 0 đứng trước “cổng” ngoài từ vựng | P2: dẫn sai nguồn; finding land-evidence-dan-nham-adr |
| 7–13 | Phiên bản schema, generation, input generations, mission/provider/role/recorded_by | Scalar YAML có giá trị bên phải tên trường; enum/định danh không có đơn vị sau số | P3: bỏ cả metadata về phạm vi và vai trò |
| 16–20 | Approver độc lập, APPROVED, đúng head và mốc duyệt | Chỉ bắt SHA/ID, không bắt quan hệ actor/trạng thái/thời gian | P3: bỏ authority cần đối chứng API |
| 21–22 | 4 commit sau duyệt và lỗi lặp lần thứ ba | Số viết bằng chữ; trạng thái dismiss không có số | P3: khoảng SHA có 5 commit; số 4 commit sau duyệt cần timeline API |
| 27–41 | Ai merge, bằng PAT hay UI, chỉ thị nguyên văn, không có URL bền | Định danh/quan hệ/thao tác không chứa số đo | P3: bỏ nguồn authority và giới hạn danh tính |
| 40–41 | Classifier từ chối trước kia và điều phối không tìm đường vòng ở cả hai lần | Mệnh đề phủ định và toàn xưng; số viết bằng chữ | P3: không có log đối chứng |
| 44–48 | Số lượt, provider, model và effort | Giá trị YAML vô đơn vị; enum | P3: số lượt và danh tính chỉ là lời khai |
| 49 | Map P1 theo từng lượt | Tên trường mang đơn vị, số nằm trong map; không có cụm số-đơn-vị | P2: không thể đếm lại từ verdict gốc |
| 50–52 | Phương pháp đếm heading và loại heading đã đóng | Mệnh đề về phương pháp; token 0 P1 không mang quy tắc đếm | P2: nguồn thứ cấp bị trình bày như đếm trực tiếp |
| 53–59 | Lượt cuối approve, 0 P1, 0 P2, 2 P3 và số lượt thứ 6 | Tên trường là đơn vị đứng trước giá trị | P2: mất toàn bộ kết quả cấu trúc, chỉ giữ SHA |
| 60–62 | Head khớp và không còn nợ review | Boolean true không phải ok:true; kết luận phủ định không số | P2: lời đóng nợ vượt khả năng đối chứng |
| 64–68 | Chuỗi 6 lần bản vá sinh lỗi | SÁU viết bằng chữ; dấu chấm giữa không tạo quan hệ nhân quả trong bảng | P3: phải đếm mục và phân biệt sự kiện tái đo |
| 65 | rm gây cả mất dữ liệu ngoài gói và phá offline | 2 hậu quả nằm trong cùng một mệnh đề không số | P3: tránh đếm 2 hậu quả thành 2 lần vá |
| 66 | Ba số hạng manifest 2142→2154→2166 | Chuỗi mũi tên không có đơn vị | P3: tổng/hiệu đúng không chứng minh từng số hạng |
| 67–68 | Hai lần vá metadata làm t27 rồi receipt v2 đỏ | Mệnh đề nhân quả; chữ số là tên test/version, không cụm số-đơn-vị | P3: thiếu gate output lịch sử |
| 72,88 | Đã chạy 121 ca, bỏ qua 0 ca | Gán key=value không có đơn vị sau giá trị; N/N khác vẫn được bắt | P3: tỷ lệ đạt không thay số thực chạy/bỏ qua |
| 75,80 | Tên CI exact-head tự mâu thuẫn phần giới hạn | Bảng chỉ giữ SHA | P3: khung vẫn mạnh hơn thân |
| 78–80 | Một job PR; không chứng minh Windows; checkout merge tổng hợp | Số viết bằng chữ và quan hệ phủ định | P3: sai phạm vi nếu chỉ đọc PR xanh |
| 84–86 | Ancestry đúng và nhánh thừa 0 commit | Số 0 trần, tên câu ở dòng khác | P3: quan hệ Git không có trong bảng token |
| 90 | 42 nợ đóng băng; tổng 81 biên nhận | Không có đơn vị phù hợp sau giá trị | P3: bỏ số hạng và tổng phân nhóm |
| 97,101 | Cả hai nền xanh; Complete job success | Trạng thái/quan hệ không số đo | P3: không thể xác nhận bằng số bước |
| 103–106 | Trần 60 phút; tách job, không nâng trần; success không đóng nợ | Giá trị gắn tên trường phía trước, cùng mệnh đề định tính | P3: mất ràng buộc vận hành |
| 108–115 | Người với phiên, nguồn thô thiếu, chưa đo native, tài liệu đã tự khai | Không số; token 20260907 chỉ là phần tên tệp | P2: tài liệu được dẫn chưa chứa đoạn tự khai |
| 118–122 | Tên khoá và kết luận cũ bị rút sau P1 | Mệnh đề trạng thái/lịch sử không mang đơn vị | P3: số hiệu PR bị hiểu nhầm thành 478 lượt |
| 128 | 6 điều kiện if sai trên push/master/windows | Số 6 không đứng ngay trước “bước” trong cùng dòng | P3: không thể lấy số tĩnh làm số skipped API |
| 130–131 | Số đúng và đứng vững | Độ chắc chắn của mệnh đề không được lưu cùng token số | P1: attestation bị nâng thành kết luận đã xác minh |
| 132,135–136 | Cơ chế đã đo; null trước chạy làm đếm thấp | Tên khoá và mệnh đề nhân quả không số | P1: cặp tổng không chứng minh trạng thái từng bước |
| 138–139 | Chưa xác định nguyên nhân; cả hai lý do đo được | Mệnh đề về mức bằng chứng, số viết chữ | P1 chung: lý do API vẫn chưa đối chứng |
| 140 | Phản ví dụ (44,4)+(−1,0)=(43,4) | Tuple có dấu phẩy và toán tử, không đơn vị | P3: cần phân biệt phép số học với sự kiện API |
| 146–148 | Chưa chứng minh giả thuyết nào; thời điểm API không ghi ở đâu | Phủ định/toàn xưng không số | P1 chung: hạ phạm vi về hiện vật trong gói |
| 150–154 | completed và 0 null; bài học loại giả thuyết | Predicate trạng thái và số trần; số thứ tự viết chữ | P3: không lẫn đề xuất chốt với cổng đã triển khai |
| 156–159 | Đã xong; 3 tên khoá mới, 4 giả thuyết; đã vá thật; đã merge | Phần kết luận và số viết chữ không được trích; SHA vẫn có | P3: chỉ đóng finding đính chính, không đóng mọi nợ |
| 163–166 | Hai P3 sang PR #479; mỗi commit huỷ approval; hai slug | Số chữ, tên PR ngắn và slug không khớp regex | P3: thiếu đối chiếu với bản sửa thật |
| 168–172 | Chỉ actionlint ghim, PATH được tin, xoá hai thư mục, chốt bỏ qua R, sentinel mất | Định tính/tên biến/phiên bản 9.9.9 không phải đơn vị dự đoán | P3: bảng bỏ lời khai mã kiểm được trực tiếp |
| 174–176 | any còn nguyên; spec revision 6; chặn kế là checkpoint | 6/6 được bắt nhưng revision đứng trước số và trạng thái bị bỏ | P2: hồ sơ spec đã sang revision 8, có checkpoint mới |
| 178–179 | 4 lease A9, các hash khác, generation 1, lệch ADR, còn chờ | Số chữ, giá trị YAML ngược chiều, quan hệ không số | P3: mất cả cấu trúc và trạng thái nợ |

### land-evidence-tong-khong-chung-minh-co-che  [P1]  Cặp tổng không chứng minh cơ chế, số API chưa đủ nguồn để gọi đứng vững

TỆP/DÒNG: ops/land/pr477-dung-goi-review-land-evidence.yaml:130–148.

VẤN ĐỀ: Ngay trong khối vừa rút P1, hồ sơ lại nâng attestation lên “Số ĐÚNG”, “ĐỨNG VỮNG”, đặt khoá `co_che_da_do_duoc` và kết cặp tổng chứng minh null→skipped. Gói không có response/job ID/attempt hoặc trạng thái từng bước. Nếu chấp nhận hai tổng, phép đo chỉ cho tăng 1 bước tổng và tăng 5 bước skipped; không định danh được bước null hoặc conclusion của bước mới. Phân tích tĩnh cho 6 if false không xác thực 6 skipped trong API. Câu “hai lý do, cả hai đo được” và “mẫu ... ĐO ĐƯỢC” vẫn nâng lời khai tương tự. Câu “không được ghi ở đâu” cũng vượt phạm vi gói.

Phản chứng trong `phan-chung-tong.json` dựng hai mảng cùng 43 bước/1 bước skipped nhưng lần lượt có 5 bước null và 0 bước null; cả hai cùng khớp tổng đầu vào. Đây là kiểm tính suy ra từ dữ liệu tổng, **không** khẳng định GitHub thực sự chuyển success thành skipped. Nếu muốn loại một mô hình bằng luật trạng thái GitHub thì cần nguồn độc lập cho luật ấy và snapshot đúng danh tính từng bước. Số khai cuối có thể đúng; finding nhắm mức bằng chứng chứ không tuyên số 6 sai.

Vá tại khối này: giữ số khai và nguyên nhân chưa xác định, đổi tên khoá cơ chế, nêu rõ attestation, giới hạn lời phủ định vào gói. Muốn nâng lại cần lưu hai response theo cùng job ID/run attempt, trạng thái job, mốc lấy mẫu, danh sách bước và băm. Rủi ro bản vá: không được biến thiếu nguồn thành khẳng định CI thất bại hoặc phủ nhận số cuối.

ĐÃ THỬ VÁ: có — xuất nội dung tệp đầy đủ, giữ cây review nguyên vẹn; executor tự tái dẫn xuất.

GÓI VÁ: [cay/ops/land/pr477-dung-goi-review-land-evidence.yaml](cay/ops/land/pr477-dung-goi-review-land-evidence.yaml). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review/audit.py`: `phan-chung-tong.json` và `ci-tinh.json` đều `ok: true`; Windows 6/6 điều kiện false, Linux 4/4 điều kiện false. `python3 -B do-review/build_hint.py`: 11/11 điều kiện đạt, `ok: true`. API KHÔNG ĐO ĐƯỢC; không mạng/không response.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### land-evidence-dem-review-khong-co-verdict  [P2]  Nguồn đếm review chưa có verdict gốc nhưng hồ sơ dùng để đóng nợ

TỆP/DÒNG: ops/land/pr477-dung-goi-review-land-evidence.yaml:44–62.

VẤN ĐỀ: Không tìm thấy verdict gốc của cả sáu lượt PR #477, kể cả lượt 1–3 được yêu cầu kiểm riêng. Tra 154/154 blob Markdown mang tên verdict trong object reachable của gói, chỉ 3 blob nhắc #477; đó là verdict PR #478 lượt 4–6. Không được lấy chúng lấp bản PR #477. Báo cáo DO-T33 và commit 37d66a6/75fe4c4/b789e73 là lời tóm tắt của executor. Chúng không cho phép tái đếm heading P1 đang mở; cũng không độc lập chứng nhận verdict lượt cuối, model/effort hoặc reviewed_sha. Vì vậy câu nguồn “đếm trên verdict từng lượt” thiếu giới hạn nguồn, và “KHÔNG có nợ” chưa có đủ vế đối chứng.

Vá: ghi map và lượt cuối là attestation, liệt kê nguồn thứ cấp; hoặc đính kèm verdict gốc từng lượt cùng neo OID/hash và quy tắc bỏ heading ĐÃ ĐÓNG. Gói vá chọn hạ mức nguồn, giữ số được khai. Ca kiểm: không có verdict phải ra chưa đo được, không ra 0 finding. Rủi ro: đổi sang `null` hoặc xoá số có thể làm mất lịch sử; gói giữ số nhưng không nâng thành đã xác minh.

ĐÃ THỬ VÁ: có — xuất nội dung tệp đầy đủ, giữ cây review nguyên vẹn; executor tự tái dẫn xuất.

GÓI VÁ: [cay/ops/land/pr477-dung-goi-review-land-evidence.yaml](cay/ops/land/pr477-dung-goi-review-land-evidence.yaml). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review/audit.py`: tra 154/154 blob verdict, kết quả trong `tim-verdict477.json`; `git.json` xác nhận head là cha merge, `ok: true`. `build_hint.py`: 11/11 điều kiện đạt. Không đo được heading PR #477; không dùng rc=0 tìm kiếm làm bằng chứng approve.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### land-evidence-dan-nham-adr  [P2]  Ô không cổng của ADR đảo vai không phải bằng chứng cho land evidence

TỆP/DÒNG: ops/land/pr477-dung-goi-review-land-evidence.yaml:4–5.

VẤN ĐỀ: Ô ADR-0045 có 0 cổng là đúng, nhưng ADR ấy quy định ngoại lệ đảo vai Codex Executor. Nghĩa vụ land evidence nằm ở ADR-0034:17–20; chính §20 còn ghi ADR-0034 “có nhắc” trong lease_publish.py và packet_loop.py. Từ ô của ADR khác không thể kết luận không bộ kiểm nào cưỡng chế tệp này. Ngược lại, chữ “có nhắc” cũng không chứng minh nội dung land được kiểm. Đây là sai nguồn cho lời khẳng định về cơ chế duy nhất chặn merge, đã bỏ lọt trong bảng token.

Vá: dẫn đúng ADR-0034 và mẫu Protocol:466–488; không suy số cổng nội dung từ thống kê lượt nhắc ADR. Ca kiểm: mở văn bản ADR đối chiếu nghĩa vụ, không chỉ kiểm mã ADR tồn tại. Rủi ro: đổi sang ADR-0034 nhưng vẫn chép “0 cổng” sẽ sinh lời khai sai mới.

ĐÃ THỬ VÁ: có — xuất nội dung tệp đầy đủ, giữ cây review nguyên vẹn; executor tự tái dẫn xuất.

GÓI VÁ: [cay/ops/land/pr477-dung-goi-review-land-evidence.yaml](cay/ops/land/pr477-dung-goi-review-land-evidence.yaml). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đọc `docs/adr/0034-*.md`, `docs/adr/0045-*.md` và `docs/PROTOCOL_DA_PHIEN.md:1147`: 2/2 ADR có nội dung đối chiếu trên cây. `adr-song`: 46/46 mục ADR khớp, chỉ chứng minh đăng ký; `build_hint.py`: 11/11 điều kiện đạt.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### land-evidence-bookkeeping-chua-neo-moc  [P2]  Trạng thái chờ checkpoint giữ nguyên từ revision cũ

TỆP/DÒNG: ops/land/pr477-dung-goi-review-land-evidence.yaml:174–176.

VẤN ĐỀ: Số revision 6 và trần dùng hết 6/6 lời gọi đúng với snapshot 2aee80a. Nhưng bản review này không neo mốc cho câu “ở revision 6 ... bước chặn kế”. Nhánh đặc tả tại 0123ace đã có revision 8, 7/7 hàng lời gọi được đếm và ghi checkpoint thứ hai với chỉ thị tiếp tục tới hết P1. Revision 7 đã ghi checkpoint từ mốc Git 2026-09-08T03:18:48Z; revision 8 có mốc 2026-09-09T08:23:03Z, trước mốc reviewed commit 2026-09-09T08:28:09Z. Một bookkeeping không ghi mốc có thể yêu cầu lại checkpoint đã được sổ ghi nhận.

Vá: giữ trạng thái revision 6 dưới nhãn lịch sử và exact commit; thêm con trỏ snapshot revision 8, tách nội dung sổ khỏi xác thực thẩm quyền GitHub. Không tự cấp quyền hay reset bộ đếm. Ca kiểm: số revision, hàng review, trạng thái checkpoint và mốc OID phải cùng nguồn. Rủi ro: lấy tip nhánh mới làm trạng thái lúc merge cũ; bản gợi ý ghi rõ hai mốc riêng.

ĐÃ THỬ VÁ: có — xuất nội dung tệp đầy đủ, giữ cây review nguyên vẹn; executor tự tái dẫn xuất.

GÓI VÁ: [cay/ops/land/pr477-dung-goi-review-land-evidence.yaml](cay/ops/land/pr477-dung-goi-review-land-evidence.yaml). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review/audit.py`: `spec.json`, `spec-r6.md`, `spec-r8.md`; 6/6 hàng lịch sử ở revision 6, 7/7 hàng ở revision 8. Git OID/mốc có trong gói; authority comment 5578460203 KHÔNG ĐO ĐƯỢC. `build_hint.py`: 11/11 điều kiện đạt.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### land-evidence-nguon-native-o-ban-khac  [P2]  Tài liệu được dẫn chưa có đoạn tự khai nền thực thi

TỆP/DÒNG: ops/land/pr477-dung-goi-review-land-evidence.yaml:114–115.

VẤN ĐỀ: Dòng 115 nói đã tự khai mọi phép đo Linux+Bash trong DO-T33-VA-GOI-REVIEW-20260907.md. Bản tại reviewed SHA không có đoạn ấy. Đoạn “Mọi số ... Linux + Bash ... Chưa có ... macOS hay Windows native” được thêm ở commit b789e73, ngoài cây đang review. Bản gói vá cho PR #479 đúng là nguồn có nội dung, nhưng con trỏ không neo commit khiến reviewer mở bản ở #477 rồi không thể đối chiếu.

Vá: dẫn exact commit b789e73274e7766ac36ff894445b82f051a47f6b và mục “Nền đã đo, và nền chưa đo”; ghi lời khai nền thực thi chưa có runner metadata. Ca kiểm: đọc đúng blob đích phải chứa nội dung được dẫn. Rủi ro: bổ sung đoạn vào tài liệu tracked sẽ vượt diff của PR này và có thể trùng PR #479; chỉ sửa con trỏ trong land evidence.

ĐÃ THỬ VÁ: có — xuất nội dung tệp đầy đủ, giữ cây review nguyên vẹn; executor tự tái dẫn xuất.

GÓI VÁ: [cay/ops/land/pr477-dung-goi-review-land-evidence.yaml](cay/ops/land/pr477-dung-goi-review-land-evidence.yaml). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đối chiếu `git show afddf7e:ops/reviews/DO-T33-VA-GOI-REVIEW-20260907.md` với cùng path ở b789e73: 2/2 blob đọc được, chỉ bản b789e73 chứa đoạn tự khai. Hiện vật đầy đủ: `ghi-chu-tai-b789e73.md`. Kiểm gói vá ghi nguồn đúng commit, `ok: true`. Không xác minh platform lịch sử qua lời tự khai.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### land-evidence-nhan-ci-exact-head  [P3]  Nhãn CI vẫn khẳng định exact head dù phần thân đã rút

TỆP/DÒNG: ops/land/pr477-dung-goi-review-land-evidence.yaml:75–80.

VẤN ĐỀ: Tên phép kiểm ghi “CI trên exact head 75fe4c4” trong khi ngay dòng 80 nói đây không phải bằng chứng CI exact head. Đổi tên thành “CI được báo cho PR có head ...” để bảng tóm tắt không tái tạo kết luận mà thân đã rút. Ca kiểm: đọc riêng tên kiểm phải giữ đúng phạm vi; rủi ro là vô tình đổi luôn số run được khai.

ĐÃ THỬ VÁ: có — xuất nội dung tệp đầy đủ, giữ cây review nguyên vẹn; executor tự tái dẫn xuất.

GÓI VÁ: [cay/ops/land/pr477-dung-goi-review-land-evidence.yaml](cay/ops/land/pr477-dung-goi-review-land-evidence.yaml). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: Đối chiếu 2/2 vị trí tên và cảnh báo trong YAML; đọc workflow checkout không khai ref. Gợi ý đã có trong tệp đầy đủ; API KHÔNG ĐO ĐƯỢC.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### bang-khang-dinh-bo-lop-gia-tri-co-cau-truc  [P3]  Bộ lọc bỏ map, scalar và predicate có đơn vị nằm ở tên trường

TỆP/DÒNG: trich_khang_dinh.py:18–40; LAND:44–60,175–179.

VẤN ĐỀ: Lỗ không chỉ là thiếu đơn vị trong danh sách: `p1: 0`, `p3: 2`, map theo lượt, `generation: 1`, `khop_head_da_merge: true`, `đã chạy=121` và tuple toán học đều có nghĩa nhưng không có “số rồi đơn vị”. Boolean true cũng khác pattern `ok: true`. Thêm từ “cổng” hoặc “nợ” không bắt được cả lớp này. Bảng bỏ sót ở trên là inventory bổ sung, có cả trường hợp khớp và chưa đo được.

Vá phương pháp: đọc cây YAML và giữ key path/giá trị/dòng; kèm duyệt thủ công prose, phủ định, quan hệ nhân quả và mức chắc chắn. Ca kiểm mẫu cần chứa scalar, map, enum, số chữ, tuple; không dùng số token bắt được làm độ phủ. Rủi ro: parser cấu trúc vẫn không hiểu quan hệ trong prose nên không được tự khai đủ.

ĐÃ THỬ VÁ: không sửa công cụ đầu vào — đã bổ sung inventory thủ công và chỉ rõ cách cải tiến phương pháp.

GÓI VÁ: KHÔNG; phương pháp và inventory bổ sung nằm trong verdict này.

ĐÃ THỬ NGHIỆM: Chạy lại `python3 trich_khang_dinh.py cay-kho/ops/land/pr477-dung-goi-review-land-evidence.yaml`: 85/85 dòng khớp TSV, `trich.json` ok: true. Những key path nêu trên không có token tương ứng; bảng bỏ sót là đối chiếu thủ công.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

### bang-khang-dinh-token-khong-phai-menh-de  [P3]  Bảng token nhân đôi định danh và bỏ độ chắc chắn của chính số đã bắt

TỆP/DÒNG: trich_khang_dinh.py:23–40; BANG-KHANG-DINH.tsv.

VẤN ĐỀ: 85 dòng là 85 hit trên 45 dòng nguồn, không phải 85 khẳng định độc lập. 8 chuỗi chữ số bị bắt đồng thời như SHA và ID; trong đó có ngày ở tên tệp. 4 hit “478 lượt” nhầm số hiệu PR thành số lượt. Chiều ngược lại, token “6 skipped” có mặt nhưng câu “số ĐÚNG/ĐỨNG VỮNG” và quan hệ “chứng minh cơ chế” bị mất. Một số đã vào bảng không có nghĩa mọi khẳng định về số đó được kiểm.

Vá phương pháp: gọi đầu ra là token ứng viên, giữ câu/key path và ngữ cảnh; tách định danh với đại lượng, khử trùng lớp ID/SHA, kiểm quan hệ/nguồn/mức chắc chắn thủ công. Ca kiểm: PR #478 lượt 2 không được thành 478 lượt; cùng số khai có thể mang nhãn attestation hoặc đã chứng minh. Rủi ro: regex dài hơn vẫn không thay inventory ngữ nghĩa.

ĐÃ THỬ VÁ: không sửa công cụ đầu vào — đã bổ sung inventory thủ công và chỉ rõ cách cải tiến phương pháp.

GÓI VÁ: KHÔNG; phương pháp và inventory bổ sung nằm trong verdict này.

ĐÃ THỬ NGHIỆM: `trich.json`: 85/85 dòng tái tạo, 45 dòng nguồn, 8 hit SHA dạng số, 4 hit nhầm số hiệu PR, `ok: true`. Không sửa script đầu vào; inventory bổ sung ở VERDICT và claims.json.

ĐỘ TIN: cao về nội dung/logic đã đo; không nâng độ tin của sự kiện API chưa có hiện vật.

## KIỂM TRA VÀ GIỚI HẠN CUỐI

- `shellcheck -f json ops/dung_goi_review.sh`: 0 chẩn đoán, `ok: true` trong wrapper; không chỉ dựa rc=0.
- `python3 -B scripts/tl.py doc-claims-check --strict`: `ok: true`, stdout 70854 byte. Không chứng minh mọi câu land evidence đúng.
- `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .`: 7/7 tệp mục tiêu được quét, 0 chỗ chép doctrine. `adr-song --root .`: 46/46 mục ADR khớp, có miễn thiếu trạng thái cho định danh ADR-0016.
- `python3 -B do-review/build_hint.py`: kiểm nội dung YAML, giữ SHA và phạm vi đính chính. Kết quả cuối trong [hint-check.json](do-review/hint-check.json); nhãn gợi ý tại [cay/README.md](cay/README.md). Đây là kiểm ngắn nội dung gợi ý, chưa phải cổng trên cây executor.
- Bộ test lease 121 ca, cổng receipt đầy đủ, builder, native Windows/macOS và CI: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**; chỉ chạy các lệnh ngắn đã cho phép. Phân nhóm receipt và so băm không thay validate schema/authority.
- Các số ref/manifest lịch sử không được thay bằng số gói mới. Snapshot có 312/312 ref khớp tên+OID; trạng thái server không đo được. Không dùng URL origin thật để gọi mạng.

Trạng thái cây cuối và băm hiện vật nằm trong [final-check.json](do-review/final-check.json). `git -C cay-kho status --porcelain` phải có 0 byte; HEAD giữ nguyên reviewed SHA.
