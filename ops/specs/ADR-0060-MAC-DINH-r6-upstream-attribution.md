# #1124 r6 — quy thuộc thay đổi upstream khi tiếp tục H8

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

Revision kế nhiệm: 6; generation: 1. Đường dẫn dự kiến:
`ops/specs/ADR-0060-MAC-DINH-r6-upstream-attribution.md`.
Trạng thái: DRAFT — chưa duyệt hash, chưa công bố, chưa dùng cấp lease hoặc nghiệm thu.

## Phạm vi và lý do

Kế thừa r4 `ops/specs/ADR-0060-MAC-DINH-r4-reviewer-route.md`, SHA-256
`fd64b142defef4edf047b408847312d8c32847523909948ce9de7e3030789154`,
và r3 mà r4 tham chiếu, SHA-256
`f7e8826d11545ce77b4630e4682464f74c6f1a277bc0e98a93ff5fbd459323e0`.

Chỉ điều chỉnh baseline/quy thuộc A12 khi tích hợp các thay đổi upstream độc lập.
Giữ objective, năm tệp W1–W5, tổng dòng thêm tối đa 450, các tiêu chí khác,
reviewer routing và human audit. Không sửa ADR-0060, checker, workflow hoặc policy.
R5 về lựa chọn máy là đề xuất riêng chưa merge, không được kế thừa hoặc coi đã có hiệu lực.

Nền lease r4 là `B0 = 6c9079c2e6ef51bc2be27f1588958937e11cc261`.
H8 nguồn kế thừa là `ca876c62cb2a4b4d043662ddecda31c8069af40c`, tree
`1eb234252f5283ac67d78991903602288373a135`, parent
`7eaea1f3d9dd4b72c3ca4c20158cc109a5a97054`.
Tại lúc lập nháp, master S0 là `75feff232a5182aa2436e08228c5d864d866f0ec`;
B0..S0 gồm năm commit, chỉ thêm hai spec #564 ngoài W1–W5. S0 không là tổ tiên H8
(merge-base --is-ancestor rc1), nên chưa được chạy heavy gate theo §10.2.1.
Rebase rồi tự dùng S0 thay B0 cho A12 là sai thẩm quyền; bản này cần chủ kho duyệt hash.

## Baseline và A12 kế nhiệm

1. B0 bất biến, giữ trong lease và bằng chứng lịch sử. Công bố toàn bộ path/numstat B0..H,
   cùng diff B0..S và nguồn PR/merge của từng thay đổi upstream; không xóa hoặc đổi nhãn lỗi cũ.
2. S là exact commit canonical master dùng làm nền khi cấp lease kế nhiệm, phải chứa artifact
   spec đã duyệt và là hậu duệ B0. Ghi S/tree(S), refs snapshot và nguồn remote trước tích hợp.
   Mỗi path B0..S phải ở ngoài W1–W5 và thuộc thay đổi canonical đã merge độc lập.
   Nếu một path W1–W5 đã đổi upstream, ngoại lệ này không áp dụng; dừng để có quyết định mới.
3. Tạo ứng viên H từ S, chỉ thay đúng W1–W5. `git merge-base --is-ancestor S H` phải rc0;
   admission bằng mã canonical S phải có receipt dương trước heavy gate.
   Mọi path ngoài W1–W5, bao gồm spec kế nhiệm, phải giữ nguyên blob và mode từ S sang H.
4. A12 cho revision này đo `git diff --numstat S..H`: đúng năm path W1–W5 của r3,
   tổng dòng thêm không quá 450. Vẫn xuất đầy đủ B0..H và B0..S để đối chiếu quy thuộc;
   không tính upstream là công executor. Path thứ sáu do executor viết, vượt trần hoặc
   sai blob/mode upstream đều đỏ.
5. Nếu master đổi sau khi chốt S, kiểm tra drift trước admission/review/heavy/push/merge.
   Khi cần tích hợp S mới thì tạo H mới, ghi checkpoint, review và chạy lại gate theo exact
   identity; không tự tái dùng bằng chứng H8, H4 hoặc H trước đó. Không tự tăng ngân sách push.

## Windows và các gate còn lại

Quyết định trực tiếp của chủ kho ngày 03-11-2026 cho miễn Windows trong lượt này được ghi tại
https://github.com/ducthangho/tra-luat/issues/1124#issuecomment-6596280445 .
Chỉ áp dụng bằng cơ chế miễn sẵn có: comment chủ kho/readback chứa dòng độc lập
`windows: <final-exact-H> mien`, nêu lý do tốn tài nguyên và kế hoạch full test Chủ nhật.
Ghi phân loại `required`, kết quả `owner_waived`; không đổi thành `not_required` hoặc `passed`.
H đổi phải ghi lại miễn đúng H mới theo thẩm quyền đã cấp; không giả chữ ký hoặc comment.
Không chạy thêm test Windows trong lượt này. Bản này không kích hoạt lựa chọn máy của r5.

A7, A8, A9 và A11 cùng các gate ngoài Windows vẫn giữ nguyên. Quyết định hoãn full test
Windows không tự miễn Linux/full local suite, selftest, CI hoặc full_mutant_audit.
Thiếu hoặc not_run phải ghi đúng trạng thái và chặn merge nếu chưa có quyết định riêng hợp lệ.
Không miễn lỗi setup, mandatory skips hoặc findings P0–P3.

## Công bố, lease và hoàn tất

Chỉ sau independent review và chủ kho duyệt SHA-256 chính artifact này mới công bố qua làn
spec riêng. Giữ artifact ngoài diff code W1–W5. Spec PR cần CI và human audit exact HEAD
trước merge theo quy trình hiện hành; kiểm readback blob/hash và commit land sau đó.
Fencing lease r4 trước cấp lease revision 6/generation 1; xác minh holder hiện hành cho năm
path và validator, không ghi đè lease phiên khác. Lease ghi B0, S, source H8, spec_hash,
branch ownership, scope waiver và authority receipt thực tế.

Review P0/P1/P2/P3 phải bằng 0 trên H kế nhiệm, không dùng verdict H8 thay thế.
Điều kiện merge còn lại phải có bằng chứng hoặc miễn trừ đúng phạm vi; human audit code
và cho phép exact HEAD vẫn tách khỏi duyệt spec. Quyền merge có điều kiện của chủ kho
không phải bằng chứng gate đã đạt. Sau merge, xác minh canonical, gate hậu merge và ghi sổ
theo M8; không khai landed khi chỉ mới merged. Không cấp quyền LIVE/deploy, credentials,
security/access hoặc mua quota.
