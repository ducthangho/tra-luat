verdict: changes_requested
reviewed_sha: 3f1cda17aa254e1a10afa12aa387bc782a945c6f
vong: 2/10
so_p1: 0
so_p2: 4
so_p3: 1
so_no_ngoai_write_set: 6

Review offline đã hoàn tất. Reviewer: OpenAI Codex / GPT-6, execution surface: Codex service, transport: machine; độc lập với phiên executor Claude. Không đăng verdict lên GitHub.

reviewed_tree: 98ffde01a2bf14eb5150aa09044323ed20c71121

Đã đọc trọn prompt.snapshot; HEAD đúng; cây sạch; actionlint 1.7.7 và shellcheck 0.9.0 có mặt. SHA256 đặc tả revision 3 đúng `47c3b1fe70da6976cf802436fa8883c2ba48ac8f706b3d9ec103deaeb5f37778`.

Windows/full CI: KHÔNG ĐO ĐƯỢC; không chạy mạng/CI. Các phép đột biến sẽ chạy trên bản sao riêng, không sửa cây đang chạy suite.

## control-bo-sot-chot-va-trang-thai — P2

**CÓ; bản vá vòng 1 chưa đóng cả lớp. Hai thể hiện mới đã đo.** `ops/lease_publish_test.py:7154–7174` khai bốn chốt không có đầu vào phân biệt qua giao diện công khai; `t164` không chứng minh được điều ấy. Ít nhất hai chốt trong `CHOT_BI_HAP_THU_512` có đầu vào phân biệt thật:

1. Chốt bản ghi vừa có `ca` vừa đóng lượt (:6664). Lấy kênh DO_CHOT/rc=1 do `main()` thật chạy control dương t160, giữ bản ghi ca trước, rồi bổ sung `ca` vào bản ghi đóng lượt. Bộ đọc gốc trả `KHONG_DO_DUOC`; chỉ gỡ chốt này trả `GIET`. Chốt “kênh không có ca” không hấp thụ được vì đã có bản ghi ca hợp lệ trước đó. Tuy vậy `t164` trên bản gỡ chốt vẫn **13/13, rc=0**.
2. Vỏ `doc_kenh` bắt ngoại lệ (:6623). Dùng giá trị list `[1,2]` từ fixture t164 làm nhãn trong kênh thật. JSON vẫn parse được; phép membership vào frozenset ném `TypeError`. Bản gốc trả KDD; bỏ bắt `TypeError` thì ngoại lệ thoát qua giao diện công khai. `except JSONDecodeError` không hấp thụ lỗi này. `t164` vẫn **13/13, rc=0**.

Phép đo: `python3 ket-qua/probe.py absorption`, driver **rc=0**; log [absorption.log](absorption.log), các kênh thật và biến thể lưu cùng thư mục. Output thật: `mixed-record original=('KHONG_DO_DUOC',...)`, `guard-removed=('GIET','')`; `outer-wrapper guard-removed ESCAPED TypeError unhashable type: 'list'`.

Hai thể hiện cũng bác số hạng **4 bị hấp thụ** trong BANG_KHAI #10 và lời khai tương ứng trong prompt/commit d5e7e7d. Không lấy 3/7 ca đỏ làm bằng chứng 4/7 còn lại tương đương. Hai chốt khác trong danh sách chưa bị bác ở checkpoint này.

Bổ sung đo răng KDD: `python3 ket-qua/probe.py kdd_teeth`, driver **rc=0**, [kdd-teeth.log](kdd-teeth.log). Gỡ kiểm rc lệch ⇒ `t163` **6/7, rc=1** (có răng). Gỡ riêng kiểm thiếu đóng lượt ⇒ **7/7, rc=0**; `dong.get(...)` trên None ném AttributeError rồi vỏ trả KDD, nên chốt sau hấp thụ. Gỡ riêng kiểm dấu đóng không phải true ⇒ **7/7, rc=0**; dấu số 1 vẫn không được nhận là đóng, rơi xuống “thiếu tên ca”. Cả hai vẫn được `t163` ghi GIET. Vì vậy câu ở :7117–7120 rằng gỡ đúng chốt thì mọi mục KDD lệch **rộng hơn phép đo**. Log lịch sử `do-lai-3-cua-SAU-va.txt` khai gỡ thiếu đóng làm 6/7 nhưng không kèm cặp neo/thay; không tái lập được lời khai đó bằng phép gỡ đúng một kiểm tra hiện tại.

Quét bổ sung `python3 ket-qua/probe.py guard_matrix`, **rc=0**, [guard-matrix.json](guard-matrix.json): gỡ riêng **19 nhánh if** của bộ đọc, chỉ **6** làm t164 đỏ. Đây là độ phủ trên 19 phép gỡ đã lưu, **không** phải tuyên bố 13 nhánh còn lại độc lập hoặc có lỗi. `CHOT_CHUA_CO_CONTROL_512` đã bị xoá khỏi HEAD; prompt mục 2 vẫn bảo nó khai 9 chốt. Bảng 3/4/2 hiện chỉ phản ánh một phần các nhánh, không phải kiểm kê toàn bộ.

**Thêm bốn thể hiện có đầu vào phân biệt** (`python3 ket-qua/probe.py unguarded`, **rc=0**, [unguarded.log](unguarded.log)); tổng thể hiện hành vi thiếu tự kiểm phân biệt đã xác nhận ở lớp này: **6** (hai ban đầu + bốn dưới):

- Bản ghi ca có `dong_luot=False`: gốc KDD; gỡ kiểm dấu true ⇒ GIET. Khác fixture số 1 của M5, không bị kiểm thiếu tên ca che.
- `chi_tiet` kiểu list: gốc KDD; gỡ kiểm kiểu ⇒ GIET.
- Tiền tố caller không khớp tên ca thật trong kênh: gốc KDD; gỡ kiểm prefix ⇒ GIET.
- Đích gồm một ca có mặt và một ca vắng: gốc KDD; gỡ kiểm đích hiện diện ⇒ KHONG_GIET (mất phân biệt lỗi cấu hình với mutant sống).

Các kênh là tổ hợp dữ liệu fixture sẵn có với kênh DO_CHOT thật. Gỡ **riêng** bốn chốt trên, t164 đều 13/13 rc=0 (ma trận). Gỡ **cả bốn**, t161 16/16, t162 12/12, t163 7/7 đều rc=0; t164 **12/13 rc=1** vì lúc này cả kiểm prefix và kiểm đích-vắng cùng bị gỡ. Nghĩa là t164 có canh **cặp** ấy trên fixture hiện tại, nhưng không phân biệt từng chốt; không khai cả bốn cùng qua mọi cổng.

Đề xuất mở rộng tương ứng: giữ đích khớp kênh khi chỉ thử prefix; giữ ca trong kênh khớp prefix khi chỉ thử đích-vắng; thêm fixture trường chi tiết sai kiểu và dấu false trên bản ghi có tên ca. Khoá bằng gỡ riêng từng điều kiện. Rủi ro: một fixture vi phạm hai điều kiện sẽ lại bị chốt thứ hai hấp thụ và cho cảm giác đã canh.

Đề xuất: thêm hai đầu vào phân biệt vào `t164` trong write set, và sửa phân loại chốt theo kết quả gỡ từng chốt. Đòi riêng mỗi mutant làm `t164` đỏ; kênh gốc hợp lệ phải giữ phân hạng. Rủi ro vá: chỉ đổi tên hoặc đòi lý do KDD vẫn không kiểm được hành vi; đầu vào bản ghi hỗn hợp phải có ca hợp lệ đứng trước để tránh bị chốt khác che. Phần >5 dòng cần executor xử lý S2 với chủ kho, không phải lý do giảm finding.

## vat-hoa-tuong-duong-qua-rong — P2

**CÓ; VÁ HỜ ở phạm vi lớp (phần đính chính đúng, nhưng còn câu sai và thiếu hai tự kiểm).** Chú thích bảng M5 tại `ops/lease_publish_test.py:7144–7148` vẫn khẳng định hai phép vật hoá là “một bộ TƯƠNG ĐƯƠNG, không phải hai chốt độc lập”. Nó trái với chính docstring đã sửa ở :6592–6612. Hai đường độc lập vẫn chỉ được khai nợ trong `NO_CHUA_CO_TU_KIEM_512`, chưa có ca khoá.

Phép đo: `python3 ket-qua/probe.py materialization`, **rc=0**, [materialization.log](materialization.log). Cả hai dùng kênh do `main()` thật sinh:

- Kênh DAT thật, t160 **1/1 rc=0**; truyền iterator đích vào bộ đọc: gốc `KHONG_GIET`, chỉ gỡ tuple trong `doc_kenh` ⇒ **GIET** dù không ca nào đỏ.
- Control dương thật, seam `doc` trả KDD lần đầu để thực hiện retry M3: gốc đọc `[GIET,GIET]` và trả GIET; chỉ gỡ tuple ở `_ten_day_du_512` đọc `[GIET,KHONG_DO_DUOC]`, trả KDD với lý do `đích RỖNG`.

**Hai thể hiện hành vi, một chú thích còn khai sai.** Không khai các lỗi trên xảy ra với caller mặc định nguyên trạng: đây là phép gỡ riêng chốt để kiểm độc lập và kiểm độ phủ M5. Các cổng t161/t162/t163 xanh không thay thế hai tự kiểm còn thiếu. Prompt nói “cả sáu lớp đã được vá” rộng hơn việc chỉ đính chính và ghi nợ.

Đề xuất: sửa cả chú thích bảng M5, thêm tự kiểm riêng cho đọc trực tiếp iterator và retry tiêu thụ iterator trong cùng tệp. Gỡ riêng từng tuple phải làm ca tương ứng đỏ. Rủi ro: tạo iterator mới ở mỗi retry sẽ che lỗi cần đo; giữ kênh thật và dữ liệu đích được tạo một lần. Đã khai nợ không đồng nghĩa finding P2 vòng trước đã đóng.

## m5-van-cham-chet-bang-chuoi — P2

**CÓ tín dụng giả cùng lớp F6 ở tầng M5; VÁ SINH LỖI MỚI.** Giữ slug vòng trước để theo dõi lớp, nhưng nguyên nhân hiện tại **không còn là đọc chuỗi**: `t163` (:7294–7308) chấp nhận KDD cho bốn mục `DO`, nên không xác minh được t162 chết bằng `TinHieuChotCa` hay ngoại lệ vô can. Chú thích :7294–7295 vẫn nói ngoại lệ vô can không được tín dụng, trái hành vi.

**Bốn thể hiện:** đổi nhánh except; đóng rc=0; không ghi đóng lượt; dấu đóng lượt bằng số 1. Cả bốn kỳ vọng KDD.

Phép đo: `python3 ket-qua/probe.py m5_falsecredit`, driver **rc=0**, [m5-falsecredit.log](m5-falsecredit.log). Đột biến chỉ đổi kiểu ngoại lệ tại chốt cuối t162 khi control lệch sang KDD: ném `Exception` thay `TinHieuChotCa`; không đổi điều kiện, bảng kết quả, tên ca, hay trạng thái khung. Chạy t163 thật:

```
bốn mục KDD: GIET
tự kiểm bộ chấm 512: đạt 7/7
lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
rc=0
```

Đo riêng lượt con t162 của mục đổi-except: **rc=1**, kênh thật [m5-unrelated-real.jsonl](m5-unrelated-real.jsonl) ghi **nhan=DO_KHAC**, chi tiết `Exception: control LỆCH phân hạng`, đóng rc=1. JSON hàng control vẫn được phát trước khi ném, nên `dung_ctrl` không chứng minh loại ngoại lệ. Phản chứng vòng trước ném Exception vô điều kiện nay làm 5/7, nhưng đó chỉ chứng minh hai mục còn lại phát hiện; không chứng minh bốn mục KDD đã đóng lớp.

Đề xuất: tách oracle đáng tin của lượt t162 khỏi nguồn đang bị đột biến, hoặc thử các chốt bộ đọc trực tiếp trên kênh từ lượt thật để tín hiệu của chính ca tự kiểm không bị mutant phá. Không chỉ siết KDD theo chuỗi lý do. Khoá bằng phản chứng trên: mọi mục `DO` phải từ chối ngoại lệ vô can; cả sáu mục đúng vẫn phải qua; A2 giữ nguyên. Rủi ro: ép mọi mục về GIET mà giữ oracle hiện tại sẽ làm đỏ bốn mutant hợp lệ (đã biết); cần sửa ranh giới đo, không đổi nhãn kỳ vọng để làm xanh.

## moc-nen-review-khong-dong-bo — NỢ

**CÓ. Hai thể hiện định lượng/nguồn đo, ngoài write set.** Prompt khai master 2175 commit; gương thật có **2178**. `cay/refs/remotes/origin/master` vẫn trỏ `dc02c9b` (2175), nhưng cùng ref trong `kho-guong.git/` trỏ `d706abd` (2178). HEAD reviewed đã merge d706abd qua 1fc6d24.

BANG_KHAI #1 ghi “numstat so dc02c9b: 1 tệp”. Diff **toàn cây** so base ấy thực tế có **3 tệp**, với số hạng `1/1 .claude/dev/chon_reviewer.py`, `49/4 .claude/dev/chon_reviewer_test.py`, `995/61 ops/lease_publish_test.py`. Diff so **master trong gương d706abd** chỉ có đúng `ops/lease_publish_test.py`: hai tệp kia đến từ merge master, không phải sửa lén của packet. Vì thế **không kết luận vi phạm write set**, và A7 vẫn đúng +995 theo đường lease chỉ định.

Phép đo: `python3 ket-qua/count_claims.py`, **rc=0**, [counts.json](counts.json); `git -C cay rev-parse refs/remotes/origin/master`, `git -C kho-guong.git rev-parse refs/remotes/origin/master`, `git -C kho-guong.git diff --name-status refs/remotes/origin/master 3f1cda1`, tất cả **rc=0**. Tổng ref vẫn đúng **412 = 8 heads + 365 remotes + 39 tags**, gương không shallow.

Đề xuất điều phối: khai riêng lease-base và PR-base, neo cả hai bằng SHA; dựng ref của cây và gương từ cùng snapshot hoặc nói rõ độ trễ. Ghi “1 đường thuộc packet” khi đang lọc path, không dùng phép lọc để chứng minh diff toàn cây chỉ một tệp. Kiểm khoá: đối chiếu SHA từng ref được prompt sử dụng và diff không lọc. Rủi ro: cập nhật base S2 sang master mà không giữ mốc lease sẽ đổi đại lượng nghiệm thu. Reviewer không sửa ref/lease.

## m3-bo-sot-loi-chuan-bi — P2

**CÓ; hai điểm phát sinh lỗi đã đo.** `_chay_mot_mutant_512` tại :6983–7008 chỉ chuyển OSError của `subprocess.run` thành KDD và retry. Lỗi tạo/copy cây ở `_cay_mut_512` (trước try/finally), hoặc lỗi sinh dấu phiên ở `sinh_dau_phien` (ngoài try bắt OSError), vẫn thoát khỏi giao diện thay vì trả một trong ba trạng thái. M3 mất lần thử thứ hai khi môi trường chuẩn bị gặp lỗi tạm thời.

Phép đo: `python3 ket-qua/probe.py transport`, **rc=0**, [transport.log](transport.log). Cùng control dương có sẵn, fault injection OSError ở từng seam:

```
spawn OSError ('KHONG_DO_DUOC', 'lỗi vận chuyển OSError: reviewer transport') attempts=2
_cay_mut_512 ESCAPED OSError reviewer setup attempts=1
sinh_dau_phien ESCAPED OSError reviewer setup attempts=1
```

Đây là phép tiêm lỗi xác định, **không khai sandbox đã thật hết đĩa/hỏng RNG**. Cùng driver xác nhận sửa vòng trước cho byte stdout không UTF-8 **ĐÃ VÁ THẬT**: control chạy qua main thật, trả GIET; không còn UnicodeDecodeError.

Đề xuất: trong chính runner test, đưa các bước chuẩn bị cần I/O vào phạm vi bắt lỗi của từng attempt, trả KDD có lý do và retry đúng một lần; bảo đảm dọn cây đã tạo dở. Khoá bằng OSError ở tạo cây, ghi nguồn và sinh dấu phiên; lần đầu lỗi rồi lần hai thành công phải giữ phép đo. Rủi ro: bắt quá rộng có thể che lỗi lập trình hoặc nhận nguồn đột biến chưa ghi xong; mỗi attempt phải có cây/kênh mới và không cấp GIET khi chưa chạy.

## phan-ra-dong-them-khong-phai-so-do-chinh-xac — NỢ

**CÓ; bốn số hạng lịch sử đo khác, ngoài write set; đã được prompt thừa nhận.** `python3 ket-qua/count_claims.py`, **rc=0**, phân loại từng dòng thêm từ diff -U0: trống, chú thích bắt đầu #, docstring theo AST, còn lại mã/dữ liệu. Danh sách dòng lưu trong `added-lines-*.json`.

| Mốc | Chú thích | Trống | Docstring khai → đo | Mã/dữ liệu khai → đo | Tổng đo |
|---|---:|---:|---:|---:|---:|
| 540b6f1 | 137 | 67 | ~87 → 89 | ~470 → 471 | 764 |
| a1c7d7f | 148 | 67 | ~90 → 89 | ~497 → 498 | 802 |
| reviewed HEAD | 204 | 82 | 118 | 591 | 995 |

Không biến các ước lượng có `~` thành lời khai chính xác; chênh nhỏ không bác kết luận kích cỡ mã vượt trần cũ 300. Nhưng không được lấy quan hệ 148+67+90+497=802 để chứng minh riêng 90 và 497. Nguồn: hai commit, handoff TRANG_THAI, lease exec-1r2; không sửa hiện vật lịch sử trong PR.

Đề xuất ngoài packet: công bố bảng exact kèm thuật toán, SHA và danh sách dòng; giữ ước lượng nếu chỉ cần quy mô. Khoá bằng tái chạy script trên hai SHA, kiểm các số hạng riêng. Rủi ro: chuỗi dữ liệu catalogue phải nằm trong mã/dữ liệu, không được tính hết chuỗi là docstring.

## neo-blob-cua-mau-so-493-sai — NỢ

**CÓ; một thể hiện lịch sử, đã được prompt thừa nhận.** Đặc tả revision 3 neo mẫu 493 vào `13a2af8c…` của 36f68c7. `git -C kho-guong.git rev-parse 36f68c7:ops/lease_publish_test.py` **rc=0** trả `5acd563297fea3b8e37dedcd750acd8794d68bec`; `git ... cat-file -t 13a2af8c` **rc=128**, `Not a valid object name`.

`python3 ket-qua/spec_counts.py`, **rc=0**, [spec-counts.json](spec-counts.json), xác nhận trên blob thật: **493 = 454 tĩnh + 39 động/khác**; 8 tiền tố tĩnh va chạm trên 4 ca; t96 có 4; 21 tiền tố động dạng đã khai trên 7 ca; hợp hai nhóm 10 ca, 29 lời gọi. Số đúng không chứng minh mỏ neo đúng. Với 21 tiền tố động, đây là hình dạng AST, không khẳng định mọi giá trị runtime đều va chạm.

Đề xuất điều phối: đính chính OID ở hồ sơ được phép, không sửa đặc tả đóng băng trong PR. Khoá bằng `rev:path` trước phép đếm AST. Rủi ro: lấy một tệp có cùng tổng 493 để thay nguồn mà không đối chiếu blob sẽ tái tạo lỗi provenance. Blob mang tiền tố cũ có tồn tại ngoài gương hay không: **KHÔNG ĐO ĐƯỢC**.

## dem-cau-truc-sai-don-vi — P3

**CÓ; lớp văn định lượng vòng trước chưa đóng cả loạt. Ba thể hiện (bốn vị trí văn).**

1. `ops/lease_publish_test.py:7078` nói chạy 10 control cho sáu mục là **60 lượt con**, lọc riêng chỉ cần **6**. Đó là số descriptor, không phải số tiến trình khi M3 retry. `python3 ket-qua/probe.py control_attempt_counts`, **rc=0**, [control-attempt-counts.json](control-attempt-counts.json), chạy thật từng control trên sáu bản đột biến và đếm lời gọi subprocess: tập đóng băng 10 control cần **109** lượt con, lọc riêng cần **10** (`2+1+2+2+2+1`). Tập đủ 12 hiện tại cần **128**. Chỉ đếm lớp tiến trình chạy control, không cộng cháu của chúng hoặc sáu tiến trình t162 của tầng trên.
2. Hai chú thích A2 tại :7123 và :7245 vẫn mô tả tập được chạy là catalogue + **10 control**, trong khi nhánh thực chạy cả hai bảng, tức **12**. Gate t163 gốc rc=0 và `du_hang` buộc `len(_muc_control_512())`; phép đếm AST/module cho 10+2=12. Bản vá 3f1cda1 sửa câu mẫu số mặc định nhưng còn hai câu cùng đại lượng ở đây. Mẫu số đóng băng riêng 10 vẫn đúng, không cần sửa chốt.
3. `_mo_kenh` :6568–6569 sửa đúng “18 biểu thức / 5 tự gọi” rồi khai **13 chỗ còn lại gọi mã sản phẩm hoặc fixture**. Trong 13 có biểu thức dùng để copy Python executable (:2315), tạo shebang (:2317), dẫn xuất đường dẫn để viết fixture (:2402); chúng không phải lời gọi sinh tiến trình. `python3 ket-qua/count_claims.py`, **rc=0**, lưu đủ 18 vị trí AST trong [counts.json](counts.json); đọc các câu lệnh tại ba vị trí trên xác nhận vai trò. Không phủ nhận ba biểu thức góp phần dựng fixture; điều sai là gọi cả 13 là vị trí gọi mã.

Đề xuất: dùng đúng đơn vị descriptor/attempt/tiến trình và mô tả A2 theo cả hai bảng; với sys.executable, chỉ nói 13 biểu thức còn lại không tự gọi suite. Khoá bằng đếm lượt subprocess qua retry và đối chiếu tập control thực; không đổi retry/mẫu số để khớp văn. Rủi ro: thay 60 bằng 109 hay 10 bằng 12 rồi tiếp tục ghi cứng sẽ lại trôi; ưu tiên dẫn xuất/mô tả hành vi.

## bang-khai-bo-sot-dai-luong — NỢ

**CÓ; 67 thể hiện** được liệt kê theo đại lượng/nguồn/mốc tại [BO_SOT_SO.md](BO_SOT_SO.md), kể cả số đúng và số chưa đo được. Bảng24 hàng vòng2 vẫn bỏ các số hạng M1, các phân rã dòng thêm, thời lượng lịch sử riêng, phép đo chiều ngược A2 và các số hạng của mẫu493. Ví dụ 59 phép chuyển tín hiệu không có mục trong BANG_KHAI; script AST xác nhận đúng59 nhưng bỏ sót vẫn là finding theo chỉ thị.

Phép đo: `python3 ket-qua/count_claims.py`, `python3 ket-qua/spec_counts.py`, các mode probe đã dẫn, đều driver **rc=0**; nguồn dữ liệu và log lưu ở ket-qua. Số chỉ có lời khai mà thiếu raw evidence được đánh **KHÔNG ĐO ĐƯỢC**, không lấy kết quả của lượt khác ghép vào. Bốn số vừa sai vừa bị bỏ sót được liên kết giữa hai lớp, không nhân đôi số lớp.

Đề xuất ngoài write set: dùng sổ đại lượng có ID, nguồn/SHA, đơn vị, phép đo và trạng thái ba giá trị; kiểm cả số hạng, số0 và số viết bằng chữ. Không chỉ sửa regex đơn vị trong trich_so.py. Khoá bằng đối chiếu67 mục đã tìm được với nguồn; tiếp tục tự khai giới hạn của sổ mới. Rủi ro: biến67 thành tuyên bố “đã đầy đủ” sẽ tái tạo chính lỗi bảng này.

## thoi-luong-khac-giua-cac-luot-do — NỢ

**CÓ chênh số theo lượt/máy; bảy đại lượng, không phải bằng chứng hồi quy mới.** Giữ quyết định chủ kho chấp nhận chi phí. `python3 ket-qua/measure_cost.py`, **rc=0**: hai clone offline từ cùng gương, cùng cấu hình core.abbrev=7 và công cụ, base dc02c9b rồi head lịch sử a1c7d7f liên tiếp. Chỉ bắt đầu sau loạt đo bảy chốt kết thúc; mỗi vế đòi đủ ba dòng N/N, bỏ qua0, không dòng đỏ, rc=0.

| Đại lượng | Khai | Đo lại |
|---|---:|---:|
| Suite nền |104.4s|107.580778s|
| Suite a1c7d7f |319.4s|320.159992s|
| Delta suite |214.9s|212.579214s|
| Hệ số |3.06|2.975996|
| t125 nền |53.0s|53.732s|
| t125 a1c7d7f |160.4s|160.740s|
| Delta t125 |107.4s|107.008s|

Hai vế đều đủ CHA/A/B, lần lượt **155/155** và **158/158**, bỏ qua0, **rc=0**. [cost/results.json](cost/results.json) lưu giá trị thô; không lấy tổng thời gian ca thay wall time tiến trình. **Giới hạn:** tài nguyên không cô lập hoàn toàn; probe `first_oracle` chạy đồng thời trong một phần vế sau. Đây là thời gian quan sát trong rig, không phải benchmark đủ để quy thay đổi cho mã.

Một lời khai thời gian khác bị trôi trong prompt: wrapper “~3,5 phút”. Riêng tổng thời gian159ca cấp cha của wrapper hiện tại là **318.913s** (>5,3 phút), chưa cộng overhead, nên không khớpước lượng210s. Đây không phải phát hiện hồi quy mới: chi phí khoảng319s đã được chủ kho chấp nhận.

Đề xuất ngoài packet: giữ số thời gian kèm mốc/lượt và điều kiện đo; không sửa code để làm khớp số một lượt lịch sử. Khoá bằng cùng driver hai vế và bằng chứng dương đầy đủ. Rủi ro: so thời gian từ hai nguồn/lượt khác nhau hoặc làm tròn trước phép trừ sẽ tạo delta không có nguồn thô; không dùng các chênh nhỏ để đảo quyết định đã chốt.

## script-chi-phi-chap-nhan-suite-do — NỢ

**CÓ; một lớp ở script handoff ngoài write set.** `ops/handoff/530/do-delta-chi-phi-hai-ve.sh` lưu rc của suite nhưng không đưa nó vào `ma`; phép kiểm dương chỉ đòi có dòng dạng N/M, không đòi hai số bằng nhau. Suite đỏ vẫn làm script chi phí trả0. Bản vá “thiếu dòng tổng kết thì đỏ” chỉ đóng trường hợp không có dòng.

Phép đo: trích **nguyên khối if** từ script đã lưu, dùng log đỏ có sẵn `A1-t162-control-luot-DAU-8-tren-10.log` (control8/10, suite0/1) làm đầu vào và rc suite=1. Lệnh tái lập:

```
D="$PWD/ket-qua/history" ten=A1-t162-control-luot-DAU-8-tren-10 bash ket-qua/cost-gate-extracted.sh
```

Output thật `captured_suite_rc=1 final_ma=0`, **rc=0**, [cost-gate-probe.log](cost-gate-probe.log). Đây là kiểm khối quyết định thật đã trích; không khai đã chạy nguyên script hardcode /home/user/tra-luat trong sandbox. Script đo lại của reviewer đòi rc=0, ba dòng đúng N/N và không có dòng đỏ nên số đo mới không dựa vào chốt yếu này.

Đề xuất cho chủ hồ sơ: sửa script ở packet khác để tích luỹ rc sai và kiểm ba dòng N/N/skip/đỏ. Khoá bằng chính log đỏ trên, log rỗng và log xanh thật. Rủi ro: lấy rc sau pipeline hoặc chỉ kiểm dòng tổng kết cuối cùng sẽ lại bỏ mất một vế A/B.

## Cổng và phạm vi đã đo

Điều kiện chung: từ gốc rig, `PATH="$PWD/cong-cu:$PATH"`, `PYTHONDONTWRITEBYTECODE=1`; actionlint1.7.7, shellcheck0.9.0 thật. Các lệnh sau chạy trong `cay/`:

| Lệnh | Bằng chứng dương | rc |
|---|---|---:|
| `python3 ops/lease_publish_test.py --chi-ca=t161` | mẫu16, GIET16, KHONG_GIET0,KDD0 | 0 |
| `python3 ops/lease_publish_test.py --chi-ca=t162` |12/12đúng phân hạng |0|
| `python3 ops/lease_publish_test.py --chi-ca=t163` |7/7;6DO+1XANH |0|
| `TAR_OPTIONS=--no-same-owner AL_VER=1.7.7 AL_GOI=../cong-cu/actionlint-1.7.7-goi.gz bash ops/chay_lease_publish_test.sh` |CHA/A/B159/159, bỏ qua0; đúng3dòng;0dòng đỏ |0|
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` |7tệp,0chỗ chép |0|
| `python3 .claude/dev/packet_loop.py adr-song --root .` |48ADR/48dòng; ngoại lệ thiếu trạng thái0016 có khai |0|
| `git diff --numstat dc02c9beed42bd2ea44a80a2e34e1bbe3acfc6c5 -- ops/lease_publish_test.py` |995/61, dư5so trần1000 |0|

Log: `gate-t161.log`, `gate-t162.log`, `gate-t163.log`, `gate-wrapper.log`, `gate-wrapper.rc`, `gate-doctrine.log`, `gate-adr.log`. `count_claims.py` kiểm máy đủ ba dòng N/N và0dòng đỏ (kể cả prefixA/B), không chỉ rc.

**A1/A4/A5/A6/A7 đạt trên các phép chạy được chỉ định. A2 có răng:** `probe.py a2_reverse` đưa phụ thuộc nội dung chi tiết vào bộ đọc ⇒ XANH_SAI, rc con[1,1], t1636/7rc1. **A3/M5 chưa đủ:** false credit và các chốt thiếu tự kiểm ở trên vẫn mở. **A8 kiểm rc lệch có răng**, gỡ so rc làm6/7rc1. Không đọc việc tất cả cổng danh nghĩa xanh thành approve.

M6: **không tìm thấy** bộ chấm mới dùng hình dạng chuỗi để phân biệt chốt và ngoại lệ. Các phép dùng chuỗi trong t125/các ca cũ để kiểm stdout vẫn thuộc ngữ nghĩa cũ. Finding M5 hiện tại là mất thông tin nguyên nhân trong kỳ vọng KDD, không phải một regex còn sót.

`python3 ket-qua/probe.py declared` rc0 xác nhận sáu mụcDO đều làm đúng control đã khai lệch. Năm mục dùng cùng control dươngt160; bốn cùng phép chiếu GIET→KDD, mộtGIET→KHONG_GIET; mục DO_KHAC dùng controlException và KDD→KHONG_GIET. Chúng có tác dụng trên control ấy; vector kết quả giống nhau không chứng minh các chốt tương đương toàn giao diện. MụcA2 là phép bất biến trên cả catalogue/control, không phải mục gỡ chốt.

Hai phần trong CHOT_BI_HAP_THU chưa bị phản chứng bác là “thiếu tên ca” và “kênh không có ca”. Với hợp đồng JSON/tuple đích hiện tại, nhánh kiểm tên phải chuỗi từ chối None; kênh rỗng bị đích-rỗng hoặc đích-vắng từ chối. Không yêu cầu phát minh một control độc lập cho hai nhánh dư thừa ấy; cần phân nhóm đúng theo hành vi.

## Đối chiếu lượt trước và hồi quy

| Lớp vòng1 | Trạng thái trên HEAD này | Bằng chứng độc lập |
|---|---|---|
| vat-hoa-tuong-duong-qua-rong | VÁ HỜ ở cấp lớp | Hai phản chứng còn đúng, câu tương đương còn sót, hai tự kiểm chỉ ghi nợ |
| stdout-giai-ma-lam-mat-phep-do | ĐÃ VÁ THẬT cho lỗi giải mã | Byte stdout255, control thật vẫn GIET; OSError lúc spawn có2attempts. Lỗi chuẩn bị mới ghi lớpM3riêng |
| m5-van-cham-chet-bang-chuoi | VÁ SINH LỖI MỚI | Bỏ đọc chuỗi; bốn kỳ vọngKDD vẫn nhận Exception, t1637/7rc0 |
| control-bo-sot-chot-va-trang-thai | VÁ HỜ ở cấp lớp | Hai control mới có răng (11/12rc1 khi phá), nhưng t164 không đóng các chốt độc lập đã nêu |
| mo-ta-thua-ke-kenh-sai-duong-chay | ĐÃ VÁ THẬT trong write set | Haiattempts cùng3ca+4đóng; t01,t01,t155, không157ca |
| dem-cau-truc-sai-don-vi | VÁ HỜ ở cấp lớp | 18/5,4vùng và16/8/2đúng; còn60/6,10controlA2,13biểu thức bị gọi nhầm đơn vị |
| BốnNỢngoài write set | Đã đo lại, giữ ngoài packet | Phân rã/OID, bảng bỏ sót, thời lượng đều có mục và giới hạn riêng |

Lượt vòng2 bị giết: hai câu7079/7176 đã sửa đúng, nhưng không đóng cả lớp văn trôi. Không coi checkpoint của lượt ấy là một review hoàn tất.

**155ca cũ giữ nguyên điều kiện:** AST từng ca base→HEAD chỉ khác đúng59lời gọi bang→chot trên9ca; sau chuẩn hoá riêng tên hàm, `old_case_AST_changes=[]`. Không chỉ so tổng hoặc số ca. Các phép gỡ chốt và bản sao nằm ngoài cay; không sửa spec, lease, workflow, ops/reviews, mã sản phẩm hay branch executor. Không chạy mạng/CI/push.

Bảng đối chiếu đủ24hàng: [DOI_CHIEU_BANG_KHAI.md](DOI_CHIEU_BANG_KHAI.md). Danh sách67đại lượng bỏ sót: [BO_SOT_SO.md](BO_SOT_SO.md). Những số chỉ ở raw PR/comment không được cấp, stderr lịch sử chưa có bytes, Windows và fullCI: **KHÔNG ĐO ĐƯỢC**; không gọi đó là pass hoặc không có vấn đề.

Trên `doc_kenh` **nguyên trạng**, chưa tìm được GIET giả hoặc KHONG_GIET sai trên tập đầu vào đã chạy. Những ví dụ decoder cấp GIET ở trên đều ghi rõ chốt bị gỡ; tín dụng giả còn mở đã xác nhận thuộc oracle `t163`, và mất retry còn mở thuộc runner chuẩn bị. Không mở rộng kết luận sang khả năng chống mã cùng interpreter sửa trạng thái khung (đặc tả đã loại khỏi mô hình tin cậy).

HEAD cuối lượt vẫn `3f1cda17aa254e1a10afa12aa387bc782a945c6f`, tree `98ffde01a2bf14eb5150aa09044323ed20c71121`; `git -C cay status --porcelain` rỗng. Verdict **changes_requested** vì **4 lớp P2 + 1 lớp P3** trong write set; **0 P1** đã xác nhận. **6 lớp NỢ** được tách ngoài phạm vi, không yêu cầu PR này sửa các đường khác. Phần vá cần hơn5dòng phải xử lý S2 với chủ kho; reviewer không tự nới trần hoặc giảm finding.
