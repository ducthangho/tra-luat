# Cross-review lượt 2 — packet #858 (wp858), lớp `sensitive`

Bạn là REVIEWER độc lập (họ openai). KHÔNG sửa mã trong `kho/`, KHÔNG push, KHÔNG gọi GitHub. Mọi đột biến/phản chứng
chạy trên BẢN SAO TẠM dưới `out/`.

## Định danh — tự kiểm
- Cây review `kho/`, HEAD phải là `97544b576392540ce316b2d61e5cc0de3a4a88eb`. Nền: `git merge-base HEAD origin/master`
  (= `637f78029f5a5fe56d35199dd0f75c50274f2c0f`).
- Spec `git show origin/ops/wp858-spec:ops/specs/wp858.md`, sha256 phải là
  `5a61e959281f852592b2a5420b4618718d2364db8fa6320934d2651bbb7d4c54`.
- Phụ lục chủ kho cho `python` (giữ nguyên từ lượt 1): phương án (a), ca python chỉ khẳng định rc 0 và không in thư
  mục bản hỏng; nợ có tên `python-probe-khong-theo-PATH`; không sửa `ops/cong_cu.py`.
- Verdict lượt 1 của bạn (cùng họ reviewer): `VERDICT-luot1.md` cạnh tệp này, neo `bfbd273`. Lượt này phải đối chiếu
  từng finding lượt 1 với head mới.

## Thay đổi kể từ lượt 1 (`git log --oneline bfbd273..HEAD`, `git diff bfbd273 HEAD`)
1. F858-01: `chon_thu_muc_chay_duoc` trả 1 TƯỜNG MINH khi `cygpath -u`, `cygpath -w` hoặc phép ghi `$GITHUB_PATH` hỏng.
   Ca âm qua INSTALLER THẬT: `$GITHUB_PATH` là thư mục (mọi nền) và stub `cygpath -w` thoát 37 (Windows).
2. F858-03: nhánh tên trần đã DAT in dòng cuối `:giu-nguyen-PATH:` (không phải thư mục). N4 thêm biến thể trình cài in
   thư mục đầu (có `bash` tốt + `rg` hỏng) ở dòng cuối stdout.
3. F858-02: fixture Windows dùng ổ `V:` mà CHỈ stub `cygpath -u` ánh xạ được. Bỏ hẳn bộ lọc trước `-f/-x/.exe`; lập luận
   tương đương: hàm chỉ tới vòng ứng viên khi tên trần CHƯA DAT, và thêm một thư mục KHÔNG chứa `<ten>` vào đầu PATH thì
   phép tra tên không đổi, nên checker đã từ chối đúng thư mục ấy. HÃY BÁC lập luận này nếu tìm được phản chứng (ví dụ
   checker có nhiều probe, PATHEXT, tệp không thực thi, symlink…).
4. L2 (`t86`), gốc ĐÃ ĐO: `codex-linux-sandbox` gắn tmpfs chỉ đọc lên `<gốc ghi được>/.git`, để lại thư mục rỗng
   `/tmp/.git` trên hệ tệp máy chủ khi một phiên Codex đang sống (`/proc/<pid>/mountinfo`: `/tmp/.git ro … tmpfs`;
   thư mục biến mất khi phiên kết thúc). `_KhoCodex` từ chối home có tổ tiên mang `.git` ⇒ `t86` (và 10 ca `r484_*`,
   packet khác — Q8, không vá) đỏ. Vá: `t86` chọn gốc tạm đầu tiên không có `.git` ở chính nó hay tổ tiên
   (`gettempdir()`, `/var/tmp`, `/dev/shm`), không có ⇒ đỏ `KHONG DO DUOC`. Ca `r858_goc_tam_tranh_to_tien_co_git` +
   đột biến harness `wp858_goc_tam_bo_kiem_to_tien`.
   LƯU Ý cho phép đo của bạn: CHÍNH sandbox của bạn có `/tmp/.git` và `<thư mục làm việc>/.git` là mount chỉ đọc, nên
   trong sandbox `t86`/`r484_*` có thể đỏ hoặc báo `KHONG DO DUOC` vì môi trường. Kiểm `mountinfo` của bạn trước khi
   kết luận, và đo delta nền/head trong CÙNG điều kiện.
5. Đột biến `wp858_sh_bo_kiem_ten_tran` nay chỉ nhắm ca Linux + ca hình dạng (bỏ N4): khi không còn lọc trước, bỏ kiểm
   tên trần thì ứng viên đầu `/usr/bin` luôn DAT nhờ tên trần nên N4 vẫn xanh; hại thật là ghi `$GITHUB_PATH`.

## Số đo của executor trên `97544b5` (khi `/tmp/.git` VẮNG) — giả thuyết để bác
`launcher_test` nền 234/234 (có/không auth giả) · head 242/242 (có/không auth giả) · `--dot-bien` head 291/291
(4 không đo được trên Linux) · `tl.py --selftest` 1731/1731 · `release-verify --strict` ok 190/190 ·
`CONG_CU_TEST_BAN_KINH=manh ops/cong_cu_test.py` 61 ca, lỗi đột biến 0.

## Việc của bạn
1. Với MỖI finding lượt 1 (F858-01/02/03): chạy lại đúng phép tái hiện của bạn (các script `out/` lượt 1 KHÔNG có ở đây —
   dựng lại tối thiểu) trên head mới ⇒ ĐÓNG / CHƯA ĐÓNG kèm lệnh + kết quả.
2. Đột biến bản vá mới (dòng canh, ba `|| return 1`, ánh xạ `V:`) trên bản sao tạm; báo đột biến sống.
3. Kiểm lập luận tương đương ở mục 3 và quyết định ở mục 5.
4. Kiểm bản vá L2 (mục 4) có che lỗi thật không: `t86` có còn đo được credential thật khi mọi gốc tạm sạch? Bộ chọn có
   thể chọn một gốc mà `_KhoCodex` vẫn từ chối vì lý do khác (quyền, sticky bit) không?
5. Các đường mới mà bản vá mở: dòng canh có thể trùng một thư mục thật không; `printf` vào `$GITHUB_PATH` khi biến chứa
   khoảng trắng; Windows khi `cygpath` vắng hẳn. Hướng cần soạn nội dung nhạy cảm thì MÔ TẢ BẰNG LỜI.

## Đầu ra — BẮT BUỘC: `out/VERDICT.md`
Dòng đầu `verdict: approve` hoặc `verdict: changes_requested`; `reviewed_head: 97544b576392540ce316b2d61e5cc0de3a4a88eb`;
bảng đối chiếu finding lượt 1 (ĐÓNG/CHƯA ĐÓNG + phép đo); bảng finding mới (id, P0–P3, tệp:dòng, lệnh → kết quả thật,
đề xuất); bảng "lệnh → kết quả thật"; mục "không đo được". Không tính lời khai là đúng nếu chưa chạy phép đo cho nó.
