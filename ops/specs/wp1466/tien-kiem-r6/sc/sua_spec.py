import pathlib, re, sys
P = pathlib.Path("/home/user/tra-luat/ops/specs/wp1466.md")
s = P.read_text(encoding="utf-8")
blk = pathlib.Path(sys.argv[1]).read_text(encoding="utf-8")
def thay(cu, moi, n=1):
    global s
    assert s.count(cu) == n, (cu[:80], s.count(cu))
    s = s.replace(cu, moi)
R6 = "/tmp/claude-0/-home-user-tra-luat/1428173d-f5d8-5c81-a6c4-b24675398aaa/scratchpad/r6"
# đầu tệp
thay("# wp1466 r5 — ", "# wp1466 r6 — ")
thay("\nrevision: 5\n", "\nrevision: 6\n")
thay("và sau checkpoint lần hai nêu ở mục 0. Người soạn r1",
     "và sau checkpoint lần hai nêu ở mục 0. Revision 6 soạn cùng ngày, cùng người soạn, trên `origin/master` `4e56f005785db1b04e043bb71fc694a674a8dc9f`, sau review Codex lượt 5 của r5 (commit `05d12f1`, verdict `ops/specs/wp1466/review/r5-l5/VERDICT.md`, sha256 `9ce3dce34b61252d70d418881684fdfe471cb7d147f02bffb08ba60ce59af767`: `changes_requested`; bảng (i) 1 lớp P2, 0 P0, 0 P1, 0 lớp mới, 0 lớp tái mở; hội tụ 2/3); r6 chỉ sửa lớp ấy (mục 0). Người soạn r1")
# mục 0
thay("""3. `tien-kiem-lease-chua-du` (F11.b/c): vắng tệp policy change-impact trên base là ĐIỀU KIỆN BẮT ĐẦU đo được, fail-closed; phần chuẩn hoá và so tiền tố của §5 mà `ai-dang-giu` không làm được đo bằng một khối tiền kiểm có điều kiện dừng, chạy trước khi đăng lease và chạy lại ngay sau khi đăng (mục 1).
""", """3. `tien-kiem-lease-chua-du` (F11.b/c): vắng tệp policy change-impact trên base là ĐIỀU KIỆN BẮT ĐẦU đo được, fail-closed; phần chuẩn hoá và so tiền tố của §5 mà `ai-dang-giu` không làm được đo bằng một khối tiền kiểm có điều kiện dừng, chạy trước khi đăng lease và chạy lại ngay sau khi đăng (mục 1).

**Revision 6, sau review lượt 5.** Lượt 5 cho hội tụ 2/3: U là ba lớp bảng (i) cuối lượt 4; F là phần wp1466 của `kiem-chuoi-khong-doc-cau-truc` và lớp `tieu-chi-dong-xoa-khong-do-hanh-vi`. Không lớp mới, không lớp tái mở. Còn mở đúng một lớp P2, `tien-kiem-lease-chua-du`, với biểu hiện F11.d: bước 3a chỉ chứng minh tập cặp của `refs/remotes/origin/*` với máy chủ, trong khi hàm quét lease mà 3c, 3d, 3e dùng (`_cac_ref_cuc_bo` của `ops/lease_publish.py`) đọc thêm `refs/heads/*` và mọi remote khác. Vì thế một bản ghi thay thế CHƯA CÔNG BỐ dựng được bia mộ hai chiều cho một lease đang giữ tệp trên máy chủ, và cả 3c, 3d, 3e cùng xanh giả. Đây là lần thứ năm lớp này có mặt. Theo §12, một lớp có mặt ở ba lượt trở lên đòi xem lại cách làm; người soạn xét lại như sau. Hình dạng lặp lại qua năm lượt là: mỗi revision xác minh thêm MỘT đầu vào của quyết định cấp lease, rồi bỏ sót đầu vào kế tiếp mà không ai chỉ. Revision 6 vì vậy không vá theo đường vào reviewer đã dựng. Nó liệt kê MỌI đầu vào mà quyết định của khối `tien-kiem` đọc, và dựng nguồn dữ liệu sao cho chỉ còn ảnh chụp máy chủ đã xác minh. Đó là bất biến `I-NGUON` (mục 1, 3d), dùng như nhau cho 3d và 3e. Phần r6 đổi gồm điều kiện bắt đầu 3, khối `tien-kiem`, và các dòng số đo, chưa đo và lịch sử nói về chúng. Bốn tệp của nguyên mẫu không đổi. Khoá văn bản, N8, khối `khoa`, các khối protocol và bảng (ii) cũng không đổi. Chuyển tiếp r4→r5 có tỷ lệ 2/3, không dưới 50%, nên tín hiệu "hai chuyển tiếp liên tiếp dưới 50%" của §12 không kích hoạt lại.
""")
thay("| packet | `wp1466`, revision 5, generation 1.", "| packet | `wp1466`, revision 6, generation 1.")
# 3a
thay("So cặp bao trùm so tập tên của CLAUDE.md và bắt thêm nhánh đã đổi đầu. `base_sha` của lease, gọi là B, là `origin/master` sau bước này.",
     "So cặp bao trùm so tập tên của CLAUDE.md và bắt thêm nhánh đã đổi đầu. Tập cặp của máy chủ ở lần so cuối là ẢNH CHỤP V: nó chỉ đúng tại giờ của lần so ấy, và mọi dữ liệu mà 3b, 3d, 3e dùng để quyết định phải đến từ V (bất biến `I-NGUON`, 3d). `base_sha` của lease, gọi là B, là `origin/master` sau bước này.")
# 3c
thay("Công cụ này chỉ so chuỗi bằng nhau trên `write_set`; phần còn lại của §5 đo ở 3d.",
     "Công cụ này chỉ so chuỗi bằng nhau trên `write_set`; phần còn lại của §5 đo ở 3d. Nó còn đọc `refs/heads/*` và mọi `refs/remotes/<remote>/*` của clone, không chỉ V. Review lượt 5 đo được nó trả `NGƯỜI_GIỮ 0` khi một bản ghi chưa công bố dựng bia mộ cho lease đang giữ tệp. Vì thế 3c ra người giữ thì DỪNG, nhưng 3c ra 0 KHÔNG đủ để cấp lease; bước quyết định là 3d.")
# 3d
thay("Chạy khối `tien-kiem` dưới đây ở gốc clone ấy, đã checkout B: `python <tệp> B` phải in `TIỀN KIỂM: ĐẠT` và rc 0. Khối đo lại 3a và 3b; rồi đo §5 bước 5:",
     "Chạy khối `tien-kiem` dưới đây ở gốc clone ấy: `python <tệp> B` phải in `TIỀN KIỂM: ĐẠT` và rc 0. Khối đo lại 3a. Rồi nó dựng bất biến `I-NGUON`: mọi byte mà quyết định đọc phải đến từ object của V. Cụ thể, B phải giải ra `master` của V hoặc một tổ tiên của nó. Policy, liên kết tượng trưng và lease được đọc trong một kho trần TẠM, mà ref duy nhất là đúng các cặp của V, object mượn của clone qua `alternates`. Mã quét lease nạp từ blob `<B>:ops/lease_publish.py`, không từ cây làm việc. Các đường vào đã liệt kê và đóng theo cách ấy: nhánh cục bộ, remote khác origin, packed-refs, replace ref, tag, ref `origin` thừa so với máy chủ, tên B bị một ref cục bộ che, B là commit chưa công bố, và tệp `.py` hay `.pyc` của cây làm việc (mục 18 ghi ca đỏ của từng đường). Khối đo 3b trên B trong kho tạm ấy; rồi đo §5 bước 5:")
thay("Một mục bị bước 2 từ chối, một lease không đọc được write set, hay ref chưa mới ⇒ DỪNG.",
     "Một mục bị bước 2 từ chối, một lease không đọc được write set, ref chưa mới, hay B không thuộc V ⇒ DỪNG.")
# 3e
thay("tức lease ấy còn hiệu lực và không lease nào KHÁC giao write set. DỪNG ⇒ thu hồi lease vừa đăng theo luật thu hồi hiện hành (bia mộ), không thi công. Bước này đóng khe giữa lúc đo ở 3d và lúc đăng.",
     "tức lease ấy còn hiệu lực và không lease nào KHÁC giao write set. Trước đó phải làm mới ref theo 3a, vì lease vừa đăng nằm trên một nhánh máy chủ mới. Bước này dùng đúng bất biến `I-NGUON` của 3d, không nới, không thêm. DỪNG ⇒ thu hồi lease vừa đăng theo luật thu hồi hiện hành (bia mộ), không thi công. Bước này THU HẸP khe giữa lúc đo ở 3d và lúc đăng; nó KHÔNG đóng khe ấy. Một lease khác được đăng lên máy chủ sau lần so cuối của 3e thì không bước nào ở đây thấy, vì kho không có phép so-và-đặt nguyên tử cho lease phía máy chủ.")
# đoạn sau 3f
thay("Răng của khối 3d đo trên kho giả (mục 18): 19 kịch bản đúng kỳ vọng; ở 7 kịch bản `ai-dang-giu` trả `NGƯỜI_GIỮ 0` mà khối vẫn DỪNG đúng lý do. Trên `5a152c1` lúc 03:24:05Z khối DỪNG đúng một lý do: lease `wp1462-r8-g2-claude` còn giữ hai tệp `.py` (S4), đúng là chưa được cấp lease.",
     "Răng của khối 3d đo trên kho giả (mục 18): 33 kịch bản đúng kỳ vọng, gồm 19 kịch bản của r5 và 14 của r6 cho `I-NGUON`; ở 7 kịch bản của r5 `ai-dang-giu` trả `NGƯỜI_GIỮ 0` mà khối vẫn DỪNG đúng lý do. Hai phản chứng của review lượt 5 chạy lại trên khối r6 đều ra DỪNG ở cả 3d và 3e. Trên `4e56f00` lúc 04:09:55Z khối r6 DỪNG đúng một lý do: lease `wp1462-r8-g2-claude` còn giữ hai tệp `.py` (S16), đúng là chưa được cấp lease.")
# đoạn giới thiệu khối
thay("Khối `tien-kiem` (64 dòng không trống). Nó KHÔNG thuộc PR giao nộp; người cấp lease chép nó ra một tệp tạm và chạy ở gốc một clone đã checkout B: `python <tệp> <B> [--sau-dang <lease_id>]`. Nó chỉ đọc. Nó gọi `git` và bốn hàm quét lease của `ops/lease_publish.py` trong cây làm việc ấy (`_quet_lease_toan_kho` với `chan_nhanh_tut_sau=True`, `_phan_loai_lease`, `_bia_mo_doi_xung`, `_lease_id_quet`); thiếu hàm, hàm ném lỗi hay `git` trả rc khác 0 đều là KHÔNG ĐO ĐƯỢC và in DỪNG.",
     "Khối `tien-kiem` (82 dòng không trống). Nó KHÔNG thuộc PR giao nộp; người cấp lease chép nó ra một tệp tạm và chạy ở gốc một clone không shallow có remote `origin`: `python <tệp> <B> [--sau-dang <lease_id>]`. Nó không cần checkout B, và không đọc cây làm việc. Nó không ghi gì vào clone; nó chỉ tạo rồi xoá một kho trần tạm trong thư mục tạm của hệ thống. Nó gọi `git` và bốn hàm quét lease của `ops/lease_publish.py` nạp từ blob của B (`_quet_lease_toan_kho` với `chan_nhanh_tut_sau=True`, chạy trên kho tạm; `_phan_loai_lease`; `_bia_mo_doi_xung`; `_lease_id_quet`). Thiếu hàm, hàm ném lỗi hay `git` trả rc khác 0 đều là KHÔNG ĐO ĐƯỢC và in DỪNG. Quét lease trên kho tạm cũng gọi `git ls-remote origin` lần nữa; lần ấy chỉ bắt được nhánh máy chủ MỚI so với V, không bắt nhánh đã đổi đầu.")
# khối mã
m = re.search(r"\n~~~ tien-kiem\n(.*?)\n~~~\n", s, re.S)
s = s[:m.start(1)] + blk.rstrip("\n") + s[m.end(1):]
# mục 3
thay("PR #1477 có đổi `.claude/skills/work-packet/SKILL.md`, một tệp mà `doctrine-scan` quét; S10 đo lại cổng trên `5a152c1`.",
     "PR #1477 có đổi `.claude/skills/work-packet/SKILL.md`, một tệp mà `doctrine-scan` quét; S10 đo lại cổng trên `5a152c1`. r6, 04:03:12Z: `master` ở `4e56f00` (merge PR #1482); `git diff --name-only 5a152c1 4e56f00` cho 5 tệp (`.claude/dev/launcher_test.py`, `ops/cai_cong_cu.sh`, một lease, một đặc tả, một verdict), 0 tệp thuộc tập đo ở trên, nên các số S2–S15 giữ nguyên. S16 là phép đo lại của r6.")
s15 = re.search(r"\n\| S15 \|[^\n]*\n", s)
s16 = ("| S16 | đo lại của r6 (`4e56f00`, clone sạch `--reference` từ máy chủ) | 04:06:27Z: so tập tên `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`), 392 và 392, thiếu 0, thừa 0; kho không shallow. "
       "04:06:59Z: 66 tệp ADR trên `master`; 0 trong 392 ref có `docs/adr/0068-*` hay số lớn hơn. "
       "`ai-dang-giu` (04:06Z–04:07Z): `packet_loop.py` 1 · `packet_loop_test.py` 1, cùng là `wp1462-r8-g2-claude`, rc 11; protocol 0 · tệp ADR 0, rc 0. "
       "04:07:39Z, bằng các hàm quét của `ops/lease_publish.py` trên clone ấy: 550 bản ghi lease; 17 còn hạn; 12 trong số đó có bia mộ hai chiều; 5 còn hiệu lực (`wp1236-a-r10-g1-claude-20261121`, `wp1448-r4-g5-claude`, `wp1462-r8-g2-claude`, `wp1475-r1-g1-claude`, `wp433-r9-g5-claude`). "
       "Khối `tien-kiem` r6 (04:09:55Z–04:10:01Z): 392 nhánh máy chủ = 392 ref kho tạm, 550 bản ghi, 5 còn hiệu lực, liên kết tượng trưng 0, policy 0, `TIỀN KIỂM: DỪNG` với đúng một lý do là `wp1462-r8-g2-claude`, rc 1. "
       "Kho chính `/home/user/tra-luat` không dùng cho phép đo này: nhánh `master` cục bộ của nó tụt sau 29 commit, nên `ai-dang-giu` ở đó ra `CHAN [12]` |\n")
s = s[:s15.end()] + s16 + s[s15.end():]
# mục 9
thay("Mỗi tiêu chí ghi phép đo làm nó ĐỎ. \"H\" là commit ứng viên; \"nền\" là base của lease.",
     "Mỗi tiêu chí ghi phép đo làm nó ĐỎ. \"H\" là commit ứng viên; \"nền\" là base của lease. Tiền kiểm 3a–3f của mục 1 là điều kiện CẤP LEASE, không phải tiêu chí nghiệm thu của H; răng của nó đo trên kho giả (mục 18), và lượt ĐẠT của nó chỉ đo được lúc cấp lease.")
# D12
thay("review lượt 4: thu hẹp lời khai chưa chuyển được nghĩa vụ; S4 và mục 18: 19 kịch bản kho giả đúng kỳ vọng |",
     "review lượt 4: thu hẹp lời khai chưa chuyển được nghĩa vụ; review lượt 5: dữ liệu quyết định đến từ ref chưa xác minh, nên r6 dựng bất biến `I-NGUON` (kho trần tạm chỉ chứa V, mã quét nạp từ blob của B, B thuộc V); S16 và mục 18: 33 kịch bản kho giả đúng kỳ vọng, 3 đột biến mỗi cái đỏ đúng ca của nó |")
# mục 17
thay("Revision 5 không có câu hỏi mới.", "Revision 5 và revision 6 không có câu hỏi mới.")
P.write_text(s, encoding="utf-8")
print("ok")
