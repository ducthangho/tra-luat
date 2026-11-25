Review độc lập wp1236 đợt C — r12/g1, lượt 3/4: **approve**, không có finding P0–P3 mở. **Windows M3 vẫn required và chưa chạy native; verdict này không chứng nhận đủ điều kiện merge.**

Reviewed SHA: `dbe650d2a3c3fb6da9573ea485adc65934efdc78`  
Tree: `b0a8b1bd4360ac33e5e0b076d820393e65d6f5bb`  
Base: `f602325574c62184caf16309631f5f680ca5cee2`  
Spec SHA-256: `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`.

Reviewer `openai_codex / codex_cli / machine`, run `bc835451258244288428e3fb73f13a00`, độc lập Executor. Model/effort phục vụ `KHONG_DO_DUOC`; effort yêu cầu high. Linux, Python 3.13.18 và phép bổ sung 3.12.3, Git 2.43.0. Review offline, không GitHub/mạng, không sửa checkout. Sandbox cho workspace-write; tính chỉ đọc được giữ bằng thao tác và snapshot.

| Lớp cũ | Đối chiếu lượt 3 | Mức còn mở |
|---|---|---|
| C01 `archive-loc-mat-du-lieu-kiem` | `DA_VA_THAT` về mã: namespace đầy đủ, danh mục hai chiều, byte tệp và đích symlink | — |
| C02 `hop-dong-dau-ra-duong-dan-tu-do` | `DA_VA_THAT`, không hồi quy theo miền E3 | — |

Hội tụ lượt 2→3: **1/1** lớp còn mở được đóng. C02 đã đóng ở lượt 2 nên không vào mẫu số. Không có lớp mở lặp lần ba, lớp tái mở hoặc P3 chờ miễn.

**C01 — bằng chứng đóng lớp.** [Probe lượt 2](case_directory.json) trên sản phẩm nguyên trạng nay trả rc 8 ở cả Linux thường và mô phỏng không phân biệt hoa/thường, với đúng lỗi tên trùng NFC+casefold; không còn nhận readback của `a` cho đường `A`. Bản chép probe chỉ đổi assertion theo kết quả mong đợi mới và reviewed_sha. [Probe lượt1](behavior.json) vẫn chặn YAML symlink cạnh YAML thường bằng `kiem_tep:not_measured:symlink`.

Ba luật trong `_d2b_kiem` được xét riêng:

- `ls-tree -r -t` liệt kê cả thư mục và tiền tố; một phép NFC+casefold dùng chung cho mọi loại mục, chạy trước extract. Đã đo file/file, dir/dir, dir/file và NFC/NFD file/dir. Hai thư mục anh em khác khóa dưới tiền tố dùng chung vẫn cho đúng rc 12 khi không có readback và rc 0 khi có.
- `os.walk` mặc định không theo symlink. So danh mục tên/loại hai chiều bắt mục thừa, thiếu, đổi tên file/dir, đổi dạng Unicode, đổi file thành thư mục và gitlink. [Phép đo độc lập](independent.json) chạy cả `passed` và `owner_waived`; mọi sai lệch rc 8 một dòng, đối chứng rc 0. Ca thư mục symlink vẫn tới K2 rc 12, không bị walk theo link rồi lệch danh mục.
- Băm blob kiểm byte tệp và đích symlink. EOL/byte đổi và đích symlink viết lại đều bị rc 8 đúng thông điệp nội dung. [Tarfile thực tế](symlink_targets_isolated.log) trên3.13.18 đổi `./x.txt` thành `x.txt` và một số dạng tương đương khác. Lượt đo ban đầu lỗi setup Git commit rc 128 được giữ riêng, không coi là pass; lượt cô lập cấu hình Git rc 0.

[Ma trận](matrix.log) tái lập 22 biến thể×12 đột biến, bản gốc0 lệch. Ba đột biến `chi_chieu_git`, `bo_dich_symlink`, `trung_khoa_chi_cung_loai` đều có đúng ca đích bắt. [Đo bổ sung độc lập](sensitivity.json) có12 kết quả: bản gốc rc 8, từng đột biến rc 0, ở cả hai nhánh. Biến thể gồm thừa thư mục thay vì thừa tệp, đảo hướng c/C dir/file và đổi đích symlink ở nhánh miễn. Luật1 đòi ít nhất một ca đích và đối chứng; không cần thêm ca bắt buộc chỉ vì một biến thể bắt được một mutant.

Symlink tuyệt đối/thoát cây chỉ phân tích bằng lời: `data_filter` của runtime kiểm absolute link và realpath ngoài đích bung, ném lỗi để D2b trả rc 8. Đã chạy phản chứng sẵn có `a112_symlink`, `a116_yaml_la_trong_thu_muc`; không dựng payload thoát cây mới, không gọi đó là phép đo native D2b thoát cây. TOCTOU vẫn gồm nhiều lần đọc: private temporary directory và thực thi đồng bộ không có writer không tin cậy trong phạm vi đã giao; không chứng nhận chống tiến trình cùng UID can thiệp sau khi hash. Các giới hạn này và M3 không được viết thành pass.

**C02.** LF ở cả hai nhánh vẫn rc 12 `duong_dan_sai`. Kiểm toàn bộ Unicode, trừ `/` là dấu phân cách, ở cả 4 vị trí regex: mỗi vị trí chỉ nhận đúng93 ký tự E3. Ca ngoại lệ chứa LF vẫn ra một dòng rc 8. Mã lớp này không đổi trong lượt 3.

**Ba chỗ lệch đặc tả — chấp nhận có căn cứ.**

1. Luật9 trên khối D2b cộng A/B: khối khớp byte (chỉ bỏ2 LF phân cách), ghép lại đúng sản phẩm. Bộ nối gọi nguyên `chay_suite`, không đổi phân hạng. Ba dòng ngoài khối có bằng chứng: xóa import `tarfile` bị ca C1 giết; mC1 xóa lời gọi bị giết; parent `--help` rc 0 có D2b. Full A/B đã audit và phần tự chạy ở dưới.
2. Fixture rút gọn và đổi head: bản gốc/adapted giữ `T-v3-pass=passed`, `T-fail=failed`; C4 chỉ đỏ `kiem_tep:failed:-`, không neo sai. C3 kiểm độc lập run/attempt/head. C1 vẫn lấy dữ liệu qua `git archive O`, worktree ở master không có provenance. C5(c) bản sao `ops/khac` vẫn đúng `duong_dan_sai`. [mC11 đúng fixture lk5](mc11.log) cho rc 0/ĐẠT như đặc tả; probe_more cũ trỏ nhầm tệp vắng, không dùng rc 8 ấy làm bằng chứng C5(b).
3. Hợp đồng đầu ra riêng của harness tích hợp: giữ nguyên consumer/phân hạng cũ; ca tự kiểm không nhận CLI sập hoặc lỗi dựng fixture làm tín dụng giết. 49 đột biến khai báo đều giết đúng đích, đối chứng sống.

Quyết định E3 ASCII và việc báo lỗi đường dẫn trước đo OID được chấp nhận như lượt 2. Không sửa hay nâng nợ `Path.glob` hoa/thường trong module A thành finding C; điều phối đã ghi nợ riêng.

**Bằng chứng chạy và giới hạn.**

- Luật9: lệnh `do` bằng bộ quét SHA-256 `1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c`, Python 3.13.18, rc 0 có `HOAN_TAT`: **219=216 GIET+3 TUONG_DUONG**, baseline16/16, khoB rỗng. Manifest và ca đích khớp executor. [Tổng hợp](luat9_summary.json), [ledger](ledger_A.tsv). Ba tương đương đã đọc lại đúng diff: thêm `~` sau tên ref không đổi kiểm tiền tố; SHA_RE neo `^…\Z` khiến match/fullmatch tương đương; kiểu từ SafeLoader có type equality/is tương đương.
- `chay_suite`: **31/31** ca (17 D2b+14 D cũ/CRLF), rc 0 cả Python 3.13.18 và3.12.3/Linux; [49 mutant khai báo](declared.log) rc 0.
- Audit đầy đủ A/B executor:1784→1801 ca nền,2009→2058 mutant; mọi2007 mutant cũ bị giết vẫn bị giết đúng tập ca đích/đối chứng. Cùng38 skip nền,1 skip mutant; `r1187_spec_packet_type` đỏ cả 2, không phải finding delta.
- Tự chạy **30 mảnh**: nền2–15 và đột biến4/16 trên mỗi base/head. Nền base `{'passed': 1579, 'skipped': 38, 'failed': 15}`, head `{'passed': 1596, 'skipped': 38, 'failed': 15}`. Cùng tập lỗi socket B4 và skip; không thiếu ca cũ, không có ca pass ở base thành fail ở head; D2b17/17 pass. Đột biến4/16: base `{'killed': 125, 'failed': 1}`, head `{'killed': 128, 'failed': 1}`. Giữ failed/tín dụng giả do socket, không chuyển thành GIET. Kiểm chéo hai ID `b4_vc_bo_han_tuong` và `b4_vc_bo_tran_byte` trên cả base/head đều cùng tín dụng giả; [rc kiểm chéo](cross_mutants_receipts.json). Mảnh cùng số có thể đổi tập mutant sau thêm delta; audit đủ theo ID là vế đối chiếu toàn bộ. [Tổng hợp](shards_summary.json), [command/rc từng mảnh](shards/receipts.json).
- Ruff 0.15.15 `--no-cache --select F` hai tệp: rc 1 cảbase/head,16 chẩn đoán nền, delta0 sau chuẩn hóa số dòng nhúng trong F811. Pin/probe contract riêng rc 0,3 mục, không lỗi. [Ruff trên checkout thật và base](ruff_actual_summary.json).
- `git diff --numstat f602325 HEAD`:2 tệp,+407/−13, trong trần450. `git diff --check f602325 HEAD` rc 0. HEAD/tree, tracked/index/untracked/ignored không đổi ở snapshot đầu/cuối. `.codex/` rỗng có từ đầu. Không suy snapshot thành bằng chứng về mọi thời điểm trong lịch sử chạy.
- Kho được cấp chỉ có master `f602325`: đo71 tệp đánh giá,10931 mục trong `ops/land`,0 nhóm trùng khóa; kết quả71/71 của lượt 2 và3 bằng nhau. `b4b79bf` không có object, nên số73/11056 trong handoff chỉ được audit, chưa tự đo. [Danh mục](catalog.json), [kết quả head](real_head.tsv).
- `not_run` của reviewer: Windows native, CI/network, full tl selftest và registration main, nền mảnh0/1/CA_DAI cùng15 mảnh đột biến còn lại. Có audit evidence executor cho phần đầy đủ; không nhận là tự chạy.

**M3 required — bàn giao điều phối trên DESKTOP-T9R33P2/Python 3.12.10.** Dựng exact base/head trong cùng lệnh, ghi test IDs/rc và quyền symlink; chạy đủ tập bắt buộc, không tính skip là xanh. Ưu tiên A/a, dir/file, common-prefix; symlink YAML/dir và mục ngoàiK2; link tới thư mục có target xuất hiện sau link trong tar (ghi os.walk dirs/files); byte `os.readlink`/data_filter; dấu chấm cuối/tên dành riêng/backslash/ADS; cấu hình sản phẩm `core.autocrlf=true` (harness cô lậpglobal nên chưa đo cấu hình này); MAX_PATH và Unicode ở đường tạm. Danh sách chi tiết có trong `m3_windows` của JSON. Windows CI được miễn theo authority trong prompt/lease; Windows local chưa được miễn.

Không có finding cần executor vá trong lượt này. Review code neo duy nhất exact SHA trên; M3 local, các gate/authority trước merge vẫn chưa được verdict này thay thế.

KET_LUAN: approve
