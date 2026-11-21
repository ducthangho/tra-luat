# WP1488 r1 — verdict review độc lập

Nguồn có thẩm quyền là tệp này trong kho. Mỗi lượt chép nguyên văn `scratch/VERDICT.md` do reviewer ghi; sha256 ghi kèm
là băm của tệp gốc trong sandbox review. Liên kết tương đối trong nguyên văn trỏ tới tệp trong sandbox, không có trong kho.

## Lượt 1 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 1/2

- Exact head được review: `2847860c3b6278b47674e417d5967735ffde8d59`. Chạy 2026-11-21T08:48:14Z → 08:52:34Z, rc 0.
- sha256 `scratch/VERDICT.md`: `87f69bb9b76a77a002e1717b1685b33e0f0a30a81b189dda25394725d8702699`.
- Kết luận: `request_changes` (2 P2, 1 P3).

### Nguyên văn

> # Review độc lập packet #1488 r1
> 
> reviewed_sha: 2847860c3b6278b47674e417d5967735ffde8d59  
> verdict: request_changes  
> reviewer: codex (OpenAI), codex_cli, read-only  
> transport: machine/local  
> tree: 6edac4622a4e8d6e7612de009e68a30e300306fe
> 
> HEAD khớp `HEAD_SHA.txt`, cây sạch trước và sau review, base `8656dc0176ed108e12c209ba55c91a1f6f9d612f` là tổ tiên. SHA-256 đặc tả khớp `1661834fbec3076d9c354999f42cb140594deb1140f1f4cdae18ab400cd0c0c8`. Diff nằm trong write set. Từ `ab298a882a34c732986e3efb8164ee0dc88c796d` đến head chỉ đổi `RESULTS.md`.
> 
> ## Findings
> 
> - **P2 · `ops/cai_cong_cu.sh:63,222–234`**. Bước chép chỉ nhìn tệp chờ, nên có thể ghi đường dẫn cũ khi kết quả cuối cùng là `GIU_PATH` hoặc rơi về stdout. Tôi tái hiện bằng công thức stub gọi bộ chọn thành công, sửa bản `rg` đầu PATH thành bản tốt rồi gọi bộ chọn lần nữa. Lần hai ghi `GIU_PATH`, script trả 0 và vẫn thêm đường dẫn của lần gọi đầu. Biến thể làm rỗng kênh rồi echo ứng viên cũng trả 0 và vẫn thêm đường dẫn. Công thức hiện hành trong YAML gọi bộ chọn tối đa một lần mỗi lượt. Để đáp ứng B5, chỉ chép khi kênh cuối có kết quả `DICH` hợp lệ tương ứng với tệp chờ, đồng thời giữ nhánh lỗi B3 và thông báo lỗi kênh. Bổ sung hai fixture trên vào ca r1488 và chốt đúng các dòng của tệp đích.
> - **P2 · `.claude/dev/launcher_test.py:12041–12054`, `ops/acceptance/wp1488/RESULTS.md:35`**. Ca C tạo dấu `di` trong công thức thử lại rồi chờ `xong` trước `exit 0`. Vì vậy writer cũ đã ghi **trước khi công thức thử lại kết thúc**, ngược với thứ tự N1 và lời khai. Ca thực sự đo cách ly khi hai lượt chồng nhau. Đột biến riêng chỉ đọc tệp cũ chứa đường dẫn `muon` đỏ tại C, nên assertion có lực đo cho cửa sổ này. Hãy phát dấu từ shell cha sau khi thu mã thoát lượt thử lại, chẳng hạn tại stub chép tệp chờ, chờ writer xác nhận đã ghi rồi tiếp tục chép. Dùng đột biến đọc thêm tệp cũ ở đúng thời điểm đó để chốt ca.
> - **P3 · `.claude/dev/launcher_test.py:12021,12427,12693`**. `_wp868_chay` gọi `.strip()` trước `splitlines()`, còn `_wp1045_chay` dùng `.split()`. Dòng trắng đầu/cuối bị mất và D tách đường dẫn có dấu cách thành nhiều token. Đột biến riêng đổi `printf '%s\n'` thành `printf '%s\n\n'` ở bước ghi tệp chờ vẫn qua toàn bộ ca r1488. Hãy đọc trực tiếp tệp đích bằng `read_text().splitlines()` hoặc kiểm byte với LF mong đợi, rồi chạy lại đột biến và D với thư mục chứa dấu cách.
> 
> ## Review B1–B6 và độ phủ
> 
> - B1 ghi tệp chờ trước `DICH`; lỗi redirection trả 1. B2 chép một lần sau vòng lặp và trước nhánh lỗi. Với công thức hiện hành, `RC_CAI != 0` chặn chép; mỗi lần thử có `kq` hoặc `kq-thu-lai-<k>` riêng và bước chép chỉ dùng biến hiện hành. Lượt `source` kế tiếp tạo `TAM_CAI` mới. `declare +x` và `export -n` gỡ thuộc tính export sau phép gán, kể cả allexport. Probe với TMPDIR có dấu cách, ngoặc, glob, dấu đô la và backslash trả 0, ghi đúng đường dẫn và dọn thư mục. Các phép mở tệp đều quote tên.
> - B3 in dòng báo ra stderr, đặt `RC_CAI=1`, dùng nhánh lỗi cũ. Probe `--bat-buoc` cho `cat` thất bại riêng ở công cụ tùy chọn đã báo lỗi, chạy công cụ bắt buộc kế tiếp, chỉ thêm đường dẫn của công cụ sau và dọn thư mục tạm. Ca E đo nhánh chạy trực tiếp. Ca D đo công thức tùy chọn trả lỗi, chưa đo lỗi **chép** ở lượt `source`.
> - B4 có cách ly theo từng lượt. C có bằng chứng writer đã chạy nhưng lệch thời điểm, như finding. A/A' đo lần thử lại đầu tiên; nhóm r1479 đo các tên kênh và thứ tự ở các lần tiếp theo.
> - B5 các nhánh thông thường vẫn giữ stdout JSON, rc và cleanup, với ngoại lệ fixture nhiều lần gọi hoặc ghi đè kênh nêu ở finding P2. Khi `--win`, dữ liệu staging là kết quả `cygpath -w` cộng LF, còn kênh `DICH` dùng đường dẫn POSIX. `r858_cai_windows_chon_ban_chay_duoc` qua với cygpath giả trên Linux. B6 đúng theo diff.
> - Sáu đột biến mới đo ghi trực tiếp, bỏ RC, đọc kênh đầu, nuốt lỗi chép, chép hai lần và nuốt lỗi ghi tệp chờ. Bảng `wp1488_sh_*` thiếu đột biến đổi thứ tự ghi tệp chờ và `DICH` (B1), bỏ các điều kiện tệp chờ khác rỗng hoặc đích khác rỗng và đổi vị trí khối chép (B2), chặn đi tiếp ở lỗi chép tùy chọn (B3), chỉ đọc nhầm khi writer cũ ghi muộn (B4), và các nhánh `GIU_PATH`, stdout, đích vắng/rỗng, cleanup (B5). Một số hành vi B5 có phép đo và đột biến cũ. Ca F chốt lỗi ghi tệp chờ nhưng không quan sát trạng thái kênh `DICH` tại thời điểm lỗi. A/A' chỉ tìm chuỗi `"DAT"`, chưa parse JSON để chốt schema hoặc trạng thái chính xác của công cụ.
> 
> ## Đối chiếu RESULTS.md và lệnh
> 
> - [preflight.log](preflight.log) ghi từng lệnh và rc 0, gồm `rev-parse`, `status --porcelain`, `merge-base --is-ancestor`, `sha256sum`, hai phép diff và `bash -n`.
> - Hai bản clone cục bộ dùng `git clone -q --no-hardlinks repo scratch/{head,base}` (chạy riêng cho từng đích), `git checkout -q --detach <SHA>` và `git config core.abbrev 7`, đều rc 0. Các phép đo chạy với TMPDIR dưới scratch, Linux x86_64 và Python 3.13.18.
> - `python .claude/dev/launcher_test.py --lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan 3` → **3/3**, rc 0, khớp lời khai về kết quả A–F với giới hạn nêu trên. `python .claude/dev/packet_loop.py doctrine-scan --root .` → **12 tệp, 0 chỗ chép**, rc 0. [head-cases.log](head-cases.log)
> - `python .claude/dev/launcher_test.py --lap-ca TEN --lan 1` cho đủ 34 tên thuộc sáu nhóm, mỗi clone **33 qua, 1 lỗi môi trường**. Ca `r858_goc_tam_tranh_to_tien_co_git` rc 1 ở cả hai vì `/tmp/.git` tồn tại, nên ca chọn `/var/tmp`, nơi thao tác tạo thư mục bị từ chối với EROFS. 33 lệnh còn lại trên mỗi clone rc 0. Lời khai base 34/34 dùng môi trường thiếu `/tmp/.git`. Bản dựng thử 33/34 trước khi sửa ca hình dạng chưa được so lại. [head-cases.log](head-cases.log), [base-cases.log](base-cases.log)
> - `python scratch/probe.py base` → rc 1, `TinHieuChotCa` tại A, installer rc 0 và tệp chứa `tot2`. `python scratch/probe.py base-detail` → probe rc 0, installer rc 1 và tệp chứa `tot` ở B. Hai kết quả khớp lời khai. [base.log](base.log), [base-detail.log](base-detail.log)
> - `python scratch/extra.py` → rc 0 ở lần đã sửa fixture (lần đầu rc 1 vì probe đặt stub sai thư mục ứng viên). Sáu đột biến mới đều chết bằng `TinHieuChotCa`, lần lượt tại A, B, A, E, A' và F như lời khai. Cùng lệnh đo lỗi chép tùy chọn và TMPDIR ký tự lạ. [extra-fixed.log](extra-fixed.log), [extra.log](extra.log)
> - `python scratch/probe.py blank-line` → rc 0 (đột biến sống). `python scratch/probe.py late-only` → rc 1 (`TinHieuChotCa` tại C). `python scratch/probe.py giu-dat`, `fallback`, `giu-path` → probe rc 0, installer lần lượt rc 0, 0, 3 và đều có dòng staging cũ. [blank-line.log](blank-line.log), [late-only.log](late-only.log), [giu-dat.log](giu-dat.log), [fallback.log](fallback.log), [giu-path.log](giu-path.log)
> - `python ops/lease_publish.py check ops/leases/wp1488-r1-g1-claude.yaml` trong head → rc 0. [lease-check.log](lease-check.log)
> - `TMPDIR="$PWD/scratch/tmp" python -u scratch/probe.py cai-sh` → **86/86**, 0 bỏ qua, rc 0. Dùng runner gốc với ba bảng được lọc trong bộ nhớ, chỉ giữ các mục `cai_sh` của `DOT_BIEN_HOOK`. `wp858_sh_nuot_loi_ghi_github_path` chết 2/2 ở đúng hai ca khai báo. [cai-sh.log](cai-sh.log)
> 
> ## Phần chưa đo
> 
> - Toàn bộ suite và toàn bộ `--dot-bien` chưa chạy. Kiểm registry bằng import, rc 0 mỗi vế, xác nhận 454 → 455 ca và 789 → 795 đột biến tổng, tức +1/+6. Các tỷ lệ 452/452 → 453/453 và 782/782 → 788/788, danh tính hai ca bỏ qua và bảy đột biến Windows chưa được xác minh độc lập bằng lần chạy toàn bộ.
> - GitHub connector đọc kết quả theo exact SHA. Workflow `gate` còn chạy khi chốt báo cáo, `lease-pr` đã thành công, workflow Windows bị bỏ qua. Đọc cấu hình required checks qua GitHub API trả 403. Trang Checks qua web báo cache miss. N4 chưa có kết luận CI xanh. [gate](https://github.com/ducthangho/tra-luat/actions/runs/44886577232), [lease-pr](https://github.com/ducthangho/tra-luat/actions/runs/44886577191), [Windows](https://github.com/ducthangho/tra-luat/actions/runs/44886577190)
> - macOS/Windows thật và file command của runner GitHub Actions thật chưa được đo. Các phép đo hành vi dùng stub Linux và tệp đích giả.

### Executor xử lý (sửa ở `b7a280e`)

| Finding | Kiểm lại | Xử lý |
|---|---|---|
| P2 chép khi kết quả cuối là `GIU_PATH` hoặc rơi về stdout | Thật. Kịch bản G (bộ chọn ra `DICH`, sửa `rg` đầu PATH, gọi lại ⇒ `GIU_PATH`): head `2847860` rc 0 mà `$GITHUB_PATH` có dòng. | Thêm điều kiện kênh CUỐI là `DICH` (`_tl1488_kenh_la_dich`, hàm, không biến). Kịch bản G, H; đột biến `wp1488_sh_bo_xet_kenh_dich` chết ở (G). |
| P2 ca C đo trước khi lượt thử lại thoát | Thật: dấu `di` phát từ trong công thức. | `cat` giả đầu PATH phát `di` lúc script đọc kênh `kq-thu-lai-*` (sau khi lượt thử lại đã thoát, trước bước chép) và chờ writer ghi xong. Fixture chốt cả `di` lẫn `xong`. Đột biến `wp1488_sh_doc_tep_cho_cu_ghi_muon` (đọc thêm tệp chờ của lượt đầu chỉ khi writer muộn đã ghi) chết ĐÚNG ở (C). |
| P3 strip/split che dòng trắng | Thật: đột biến `printf '%s\n\n'` sống. | So nguyên byte của tệp `$GITHUB_PATH` ở mọi kịch bản. Đột biến `wp1488_sh_tep_cho_dong_trang` chết ở (A'). |
| Độ phủ: lỗi chép ở lượt `source` (B3) | Đúng là thiếu. | Kịch bản I: `--bat-buoc`, `$GITHUB_PATH` là thư mục ⇒ công cụ tuỳ chọn báo đi tiếp, công cụ bắt buộc dừng, đúng hai dòng báo. Đột biến `wp1488_sh_chep_loi_thoat_ngay` chết ở (I). |

Không làm (độ phủ reviewer liệt kê, ngoài các chốt trên): đột biến đổi thứ tự ghi tệp chờ/`DICH` trong bộ chọn và bỏ điều
kiện `-s`/`-n` riêng lẻ. Lý do: thứ tự ấy chỉ đổi kết quả khi ghi `DICH` lỗi mà ghi tệp chờ được, vốn đã đi nhánh lỗi; hai
điều kiện `-s`/`-n` là chốt rỗng của B5 mà `r858_*` (`$GITHUB_PATH` rỗng/vắng ⇒ vẫn DAT) đã đo ở mức hành vi.
