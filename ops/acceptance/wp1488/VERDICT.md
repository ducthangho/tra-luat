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

## Lượt 2 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 2/2 (hết ngân sách lease)

- Exact head được review: `e21001f90e99be1ef3ec953c787b72b0f6b89a8c` (mã trùng `b7a280e`). Chạy 2026-11-21T09:15:15Z → 09:22:04Z, rc 0.
- sha256 `scratch/VERDICT.md`: `2c5c31e0d9546381daeff210529cd019704310e2aed374eb33d33303ce12dd7f`.
- Kết luận: `request_changes` (2 P2, 2 P3). Các finding lượt 1 reviewer xác nhận đã đóng (bảng probe trong nguyên văn).

### Nguyên văn

> # Review độc lập WP1488 r1 · lượt 2/2
> 
> reviewed_sha: e21001f90e99be1ef3ec953c787b72b0f6b89a8c  
> verdict: request_changes  
> reviewer: codex (OpenAI), codex_cli, read-only  
> transport: machine/local  
> tree: afb458f292253d78982b809a5b036be217760005
> 
> HEAD khớp `HEAD_SHA.txt`. Base `8656dc0176ed108e12c209ba55c91a1f6f9d612f` là tổ tiên. SHA-256 đặc tả khớp `1661834fbec3076d9c354999f42cb140594deb1140f1f4cdae18ab400cd0c0c8`. Diff nằm trong write set. Sau `b7a280e` chỉ đổi RESULTS và VERDICT. Cây `repo/` sạch. Phép đo chạy trong clone và fixture dưới `scratch/` trên Linux x86_64, Python 3.13.18.
> 
> ## Findings
> 
> - **P2 · `ops/cai_cong_cu.sh:224–237`**. Script dùng hai lần đọc độc lập cho quyết định ghi và cho kết quả cài. `case "$(cat …)"` xét chuỗi kể cả khi `cat` trả lỗi. Probe `partial` cho `cat` lần đầu in đủ `DICH` rồi trả 9, lần hai trả 9. Installer đã thêm đường dẫn, sau đó báo lỗi đọc kênh và thoát 7. Probe `transient` cho lần đầu lỗi với stdout rỗng và lần hai đọc thành công. Installer trả 0, JSON có `DAT` nhưng thiếu dòng cần ghi. Hãy đọc kênh đúng một lần khi công thức cuối trả 0, giữ sentinel và nhánh lỗi đọc rc 7, rồi dùng cùng kết quả cho bước chép và phân nhánh PATH. Thêm hai biến thể `cat` trả lỗi trên vào r1488, chốt mã thoát, thông báo và tệp đích rỗng khi lần đọc thất bại.
> - **P2 · `ops/cai_cong_cu.sh:80–82,224–226`**. Điều kiện mới chỉ khớp tiền tố. Probe `different-dich` gọi bộ chọn cho `goc/usr/bin`, rồi công thức ghi `DICH` cho thư mục `other` cũng có rg chạy được. Installer trả 0 và thêm `goc/usr/bin` vào tệp CI dù PATH nội bộ dùng `other`. Finding lượt 1 đã hết ở GIU_PATH và stdout, còn thiếu kiểm tra tệp chờ tương ứng với đường dẫn trong kết quả cuối. Ca tái hiện dùng công thức stub. Các công thức hiện hành có bộ chọn gọi nó một lần ở cuối. Gắn danh tính đường dẫn POSIX vào dữ liệu chờ và chỉ chép khi nó khớp kênh đã đọc, giữ nguyên dòng đã đổi qua `cygpath -w` trên Windows. Thêm probe hai thư mục đều đạt vào r1488 và chốt cả PATH nội bộ lẫn nội dung tệp CI.
> - **P3 · `.claude/dev/launcher_test.py:12044–12062`**. Trên head hiện tại, lần `cat` kênh cuối diễn ra sau khi công thức thử lại thoát, nên ca C đo được cửa sổ N1. Stub dùng mẫu `*kq-thu-lai-*` trên `"$*"`, khớp cả tệp chờ và lần đọc kênh sau chép. Đổi riêng helper sang Bash `$( < "$KENH_KQ" )` vẫn xanh. Ghép thay đổi ấy với đột biến đọc cũ trước lệnh chép cũng vẫn xanh. Khi đó dấu phát ở `cat` tệp chờ, và một phép đọc nhầm đặt trước lệnh chép có thể xảy ra trước khi writer cũ ghi. Dùng hook có chủ đích tại bước chép, hoặc khớp chính xác đối số kênh và chốt lần kích hoạt diễn ra ở điểm cần đo. Thêm đối chứng thay cơ chế đọc kênh và kiểm tra đột biến đọc cũ vẫn đỏ tại C hoặc fixture báo rõ điểm đồng bộ đã đổi.
> - **P3 · `.claude/dev/launcher_test.py:12024–12025,12075–12089,12105–12125` và `ops/acceptance/wp1488/RESULTS.md:28`**. Khẳng định so nguyên byte ở mọi kịch bản vượt phép đo. `read_text` chuẩn hóa CRLF, và đột biến riêng ghi CRLF qua r1488. E và I chỉ kiểm rc và stderr vì đích là thư mục. Hãy dùng `read_bytes()` cho các đích là tệp, mô tả E/I theo đúng assertion, và dùng đột biến CRLF để chốt lại lời khai nguyên byte. P3 lượt 1 về dòng trắng và đường dẫn có dấu cách đã đóng.
> 
> ## Đối chiếu lượt 1 và review B1–B6
> 
> | Probe tái dựng từ verdict lượt 1 | rc probe | rc installer | Kết quả |
> |---|---:|---:|---|
> | `giu-dat` | 0 | 0 | DAT, đích rỗng |
> | `fallback` | 0 | 0 | DAT, đích rỗng |
> | `giu-path` | 0 | 3 | Công cụ chưa DAT, đích rỗng |
> | `blank-line` | 1 | 0 | `TinHieuChotCa` tại A', thấy LF thừa |
> | `late-only` | 1 | 0 | `TinHieuChotCa` tại C, thấy dòng `muon` |
> 
> - **B1/B2**. Bộ chọn ghi tệp chờ trước `DICH`, lỗi ghi trả 1. Đường append duy nhất nằm sau retry và trước xử lý lỗi. `RC_CAI != 0` chặn append ở công thức cuối thất bại. Probe trên base tái hiện A với installer rc 0 và dòng `tot2`, B với installer rc 1 và dòng ứng viên. Ca r1488 với script `2847860` đỏ ở G.
> - **B3**. Lỗi append đặt `RC_CAI=1`. E đo đường gọi trực tiếp. I đo hai lỗi append với installer rc 1, thông báo đi tiếp cho công cụ tùy chọn và lần append thứ hai của công cụ bắt buộc. D đo công thức tùy chọn lỗi rồi ghi đúng một dòng của công cụ bắt buộc. Chạy lại D/I với đường dẫn có dấu cách cho kết quả trên và cả hai dọn sạch TMPDIR.
> - **B4**. Mỗi lượt giữ đường dẫn kênh riêng từ `kq` tới `kq-thu-lai-<k>`; subshell nền giữ giá trị của lượt nó, còn lượt `source` thứ hai tạo `TAM_CAI` mới. Mọi lần mở tệp quote biến. Probe `odd` chạy `bash -a` với TMPDIR chứa dấu cách, glob, đô la, backslash và nháy đơn, trả 0, ghi đúng và dọn sạch. `declare +x` ở lượt đầu và `export -n` ở retry gỡ export của biến kênh sau phép gán.
> - **B5**. G đo nhánh GIU_PATH và H đo stdout fallback sau khi staging đã có dữ liệu. Kênh vắng hoặc sai tiền tố cố định vẫn trả 7 và đích rỗng. Helper nằm trong điều kiện nên errexit giữ luồng xử lý, nhưng trạng thái `cat` đầu bị bỏ qua như finding P2. Trên đường bình thường bước đọc/chép giữ stdout dành cho JSON, cleanup vẫn ở các nhánh cũ. `--win` ghi đầu ra `cygpath -w` vào staging; kênh DICH giữ đường dẫn POSIX cho PATH nội bộ.
> - **B6**. Diff giữ nguyên YAML công thức, launcher, hook và workflow.
> 
> ## Độ phủ và đối chiếu RESULTS.md
> 
> - A/A' chốt rc, dấu apt update, chuỗi DAT và nội dung tệp. G kiểm thêm thông báo GIU_PATH. H có phép đo thật vì công thức đã tạo staging trước khi xóa kết quả kênh. Các ca này tìm chuỗi DAT trong stdout. Schema JSON và danh tính công cụ chưa được assert ở các điểm đó. I chốt rc khác 0, cảnh báo tùy chọn và hai lỗi ghi. Đột biến thoát ngay đỏ đúng tại I.
> - 10 đột biến `wp1488_sh_*` đều chết bằng `TinHieuChotCa`, theo thứ tự bảng RESULTS là A, B, A', E, A', F, G, A', I, C. Đột biến `wp858_sh_nuot_loi_ghi_github_path` chết ở cả hai đích khai báo. [Chi tiết assertion](mut-detail.log)
> - Trong nhóm `wp1488_sh_*`, B1 thiếu đổi thứ tự staging/DICH. F thấy lỗi staging mà chưa nhìn kênh trước cleanup. Đột biến riêng đổi thứ tự sống, rc 0. B2 thiếu bỏ riêng `-s`/`-n` và di chuyển khối append qua các ranh giới retry/xử lý lỗi. B3 có cả đường trực tiếp và tùy chọn. B4 có đột biến đọc kênh cố định và đọc cũ muộn. B5 thiếu đột biến riêng cho stdout sau staging, kênh thiếu/hỏng sau staging, DICH khác staging, đọc kênh hai lần và cleanup. Các ca và đột biến cũ vẫn đo một phần B5, gồm đích vắng và lỗi đọc kênh cố định. Việc thiếu các đột biến bổ sung này khác với N2, vốn liệt kê năm đột biến bắt buộc và cập nhật neo cũ.
> - Số đăng ký đo bằng import là **454 ca / 789 đột biến** ở base và **455 / 799** ở head, đúng delta +1/+10. Tái chạy ca mới **3/3** trên `ab298a8`, **2/2** trên đúng `b7a280e`, **3/3** trên head, cả ba rc 0. Nhóm 34 ca cho **33 qua, 1 lỗi môi trường** ở cả base và head. Lời khai base 34/34 dùng môi trường thiếu `/tmp/.git`. Ở đây `/tmp/.git` tồn tại, ca `r858_goc_tam_tranh_to_tien_co_git` chọn `/var/tmp` và gặp EROFS, rc 1. Ca hình dạng hiện qua ở cả hai vế.
> - Doctrine scan khớp **12 tệp, 0 chỗ chép**, rc 0. Windows giả qua, và đột biến bỏ đổi `cygpath -w` chết ở ca Windows lẫn ca hình dạng.
> - Probe riêng cho H nới điều kiện để kênh rỗng cũng được chép. Ca đỏ đúng ở H. Probe ghép thay cách đọc với đột biến đọc cũ sống tại C. [Phản chứng H và C](extra-check.log)
> 
> ## Lệnh và mã thoát
> 
> - `git -C repo rev-parse HEAD`, `cat HEAD_SHA.txt`, `git -C repo status --porcelain`, `git -C repo rev-parse 'HEAD^{tree}'`, `git -C repo merge-base --is-ancestor 8656dc0 HEAD`, `sha256sum repo/ops/specs/wp1488-r1.md`, hai lệnh diff theo prompt, `git -C repo diff --check 8656dc0..HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py` và `git -C repo diff --quiet b7a280e HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py` đều rc 0. Kiểm lại HEAD, sạch và hash trước khi chốt.
> - `git clone -q --no-hardlinks repo scratch/{head,base,b7,ab}` chạy riêng mỗi đích, `git checkout -q --detach SHA` và `git config core.abbrev 7` từng clone đều rc 0.
> - `python -u scratch/run.py cases` và `python -u scratch/run-base.py cases` đều rc 0 ở wrapper ghi log. Mỗi wrapper chạy `bash -n ops/cai_cong_cu.sh` và `python .claude/dev/packet_loop.py doctrine-scan --root .`, rc 0. `python ops/lease_publish.py check ops/leases/wp1488-r1-g1-claude.yaml` rc 0 trên head, rc 2 trên base vì tệp lease của packet chưa tồn tại. Từng lệnh `python .claude/dev/launcher_test.py --lap-ca TEN --lan 1` và rc thật nằm trong log, chỉ ca EROFS rc 1 ở mỗi vế. [Head](cases.log), [Base](base-cases.log)
> - `python .claude/dev/launcher_test.py --lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan N` trong các clone head (`N=3`), b7 (`N=2`) và ab (`N=3`), với TMPDIR dưới scratch, đều rc 0.
> - `python scratch/probe.py TEN` chạy riêng từng probe. Năm mã thoát lượt 1 ở bảng trên. `base-A` và `old-G` rc 1 bằng `TinHieuChotCa`; `base-B`, `missing`, `corrupt`, `different-dich`, `transient`, `partial`, `odd`, `crlf`, `no-cat-hook` đều rc 0 ở probe. Mã installer và tệp đích nằm trong từng `probe-TEN.log`. `crlf` và `no-cat-hook` là đột biến pass toàn ca.
> - `python -u scratch/mut-detail.py`, `python -u scratch/source-check.py` và `python -u scratch/extra-check.py` đều rc 0 ở wrapper. Log ghi từng assertion hoặc mã installer, gồm ca D/I với dấu cách và kiểm cleanup. [D/I](source-check.log)
> 
> - `python -u scratch/run-filtered.py mut` gọi `main --dot-bien` sau khi lọc bảng trong bộ nhớ chỉ còn `cai_sh`. **DOT BIEN: 90/90 dat**, không bỏ qua, rc 0, khớp RESULTS. Lần đầu `python -u scratch/run.py mut` cũng ghi 90 đột biến OK và runner trả tuple `(0, 0)`, nhưng wrapper truyền tuple cho `sys.exit` nên process rc 1. Lần chạy qua CLI đã sửa wrapper. [CLI lọc cai_sh](cai-sh-cli.log), [Lần gọi runner trực tiếp](cai-sh.log)
> 
> ## Phần chưa đo
> 
> - Toàn bộ suite và toàn bộ `--dot-bien` chưa chạy trong lượt review này. Số tổng registry khớp, nhưng các tỷ lệ suite `452/452 → 453/453`, full mutation `782/782 → 788/788 → 792/792`, hai ca và bảy đột biến bỏ qua vẫn là lời khai của executor. Bản dựng thử trước khi sửa ca hình dạng cũng chưa được dựng lại để đo 33/34.
> - N4 chưa có bằng chứng CI xanh trên exact head. Connector GitHub trả thành công khi đọc workflow và job theo SHA. `lease-pr` success, Windows skipped, `gate` vẫn in progress ở lần đọc cuối. Combined status trả danh sách rỗng. [Gate](https://github.com/ducthangho/tra-luat/actions/runs/44888691485) · [Lease](https://github.com/ducthangho/tra-luat/actions/runs/44888691448) · [Windows](https://github.com/ducthangho/tra-luat/actions/runs/44888691422)
> - macOS/Windows thật và tệp lệnh của runner GitHub Actions thật chưa được đo. Các ca nền tương ứng ở đây dùng stub trên Linux.

### Review Rescue Checkpoint sau lượt 2 → revision 2

Ngân sách Codex của lease r1 hết (2/2). Hai lượt cùng chỉ một gốc: HAI nguồn sự thật (tệp chờ và kênh đọc độc lập). Chủ kho
chọn qua AskUserQuestion (21-11-2026 ~09:35Z) **"Thiết kế lại, Codex lượt 3"**, rồi duyệt đặc tả r2 `ops/specs/wp1488-r2.md`
(sha256 `692325c7…add0`). Lease `wp1488-r2-g2-claude` thay `wp1488-r1-g1-claude` (bia mộ hai chiều); trần Codex cả packet 3.

### Executor xử lý (sửa ở `42b5386`, đặc tả r2)

| Finding | Kiểm lại | Xử lý |
|---|---|---|
| P2 đọc kênh hai lần | Thật. | Kênh đọc ĐÚNG MỘT LẦN khi `RC_CAI = 0` (đọc lỗi ⇒ 7); chính `KQ` ấy quyết bước chép và phân nhánh PATH (`sh.count('cat -- "$KENH_KQ"') == 1` được chốt trong `r858_hinh_dang…`). K1 (in đủ rồi lỗi) và K2 (lỗi không in) ⇒ rc 7, tệp rỗng. Đột biến `wp1488_sh_doc_kenh_rieng_truoc` (dựng lại thứ tự r1: quyết định chép bằng một lần đọc riêng trước) chết ở (K1). |
| P2 DICH khác tệp chờ | Thật. Kịch bản J: script `b7a280e` ĐỎ (ghi thư mục X trong khi PATH nội bộ dùng Y). | Tệp chờ hai dòng (POSIX `$dich` + dòng sẽ thêm); chép chỉ khi dòng (1) bằng `DICH` của lần đọc duy nhất, khác thì cảnh báo. J chốt rc 0, `DAT`, phiên bản của Y trong JSON, tệp rỗng, có cảnh báo. Đột biến `wp1488_sh_bo_so_danh_tinh` chết ở (J). |
| P3 móc thời điểm của C | Thật. | Móc khớp ĐÚNG `cat -- <…>/kq-thu-lai-1`; fixture chốt riêng móc ĐÃ kích hoạt ("điểm đồng bộ đã đổi" nếu không) và writer ĐÃ ghi. Đột biến `wp1488_sh_doc_tep_cho_cu_ghi_muon` chết ở (C). |
| P3 "so nguyên byte" rộng hơn phép đo | Thật (CRLF qua `read_text`). | `read_bytes()` ở mọi kịch bản có tệp đích; E/I mô tả đúng là chốt rc + stderr. Đột biến `wp1488_sh_tep_cho_crlf` chết ở (A'). |

Ghi chú đo được: `wp1488_sh_chep_loi_khong_dat_rc` (bỏ `|| RC_CAI=1`) chết ở (I), không ở (E). Ở lời gọi trực tiếp, hàm
trả 1 không có `||` thì `set -e` cũng thoát 1, nên (E) không phân biệt được; chỉ lượt `source` (I) phân biệt đường `RC_CAI`
với errexit. Bảng `cai_sh` (mọi packet): 92/92.

## Lượt 3 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 3/3 (hết trần cả packet) · đặc tả r2

- Exact head được review: `129d59baacacb5f8881b1dd9ac5ef965a6de1383` (mã trùng `42b5386`). Chạy 2026-11-21T10:20:28Z → 10:26:54Z.
- `codex exec` thoát rc 1 sau khi đã ghi `scratch/VERDICT.md` đầy đủ (xem đuôi log khi đọc lại); nội dung verdict là nguồn.
- sha256 `scratch/VERDICT.md`: `36002c43a4f9f96f61e3e3398b4bd055fbbda6fa553d651530ca305f173523ab`.
- Kết luận: `request_changes` (1 P2, 3 P3). Các finding lượt 2 reviewer xác nhận đã đóng (bảng probe trong nguyên văn).

### Nguyên văn

> # Review độc lập WP1488 r2 · lượt 3/3
> 
> reviewed_sha: 129d59baacacb5f8881b1dd9ac5ef965a6de1383  
> verdict: request_changes  
> reviewer: codex (OpenAI), codex_cli, read-only
> 
> HEAD khớp `HEAD_SHA.txt`, cây sạch, base `8656dc0176ed108e12c209ba55c91a1f6f9d612f` là tổ tiên. SHA-256 của đặc tả r2 khớp `692325c7cd0dc50aee52a92b36ffb5075f585f5a285375a0a0a2686b73fcadd0`. Diff trong write set. Sau `42b5386` chỉ đổi RESULTS và VERDICT. Lease r2 qua kiểm tra cục bộ. Các phép đo chạy trên Linux trong clone dưới `scratch/`.
> 
> ## Findings
> 
> - **P2 · `ops/cai_cong_cu.sh:81,229–235` · LF trong đường dẫn phá phép so danh tính.** Hai lượt chọn và đọc dùng định dạng phân cách bằng LF, nhưng bên ghi cho phép LF trong đường dẫn POSIX. Probe truyền ứng viên hợp lệ `<sân>/a<LF>b` qua biến môi trường, gọi bộ chọn, rồi đặt kênh thành `DICH<LF><sân>/a` cho một thư mục khác cũng chạy được. Dòng đầu trong tệp chờ tình cờ khớp `DICH` cuối. Script trả 0, JSON báo dùng rg 8.8.8 của `<sân>/a`, và thêm đúng chuỗi sai `b'b\n'` vào tệp CI. Với kênh nguyên vẹn, cùng đường dẫn LF chạy được nội bộ nhưng bỏ qua ghi CI do so lệch. Hãy từ chối LF trong hai trường trước khi tạo tệp chờ khi bật `GITHUB_PATH`, với lỗi rõ ràng theo B1, và giữ đường dẫn nguyên văn khi đích vắng hoặc rỗng. Thêm biến thể của J với hai thư mục trên, chốt stderr, mã thoát theo chính sách từ chối và tệp đích rỗng. [Probe trùng tiền tố](newline-collision.log) · [Probe kênh nguyên vẹn](newline-valid.log)
> - **P3 · `ops/cai_cong_cu.sh:76,229–235` · Chấp nhận tệp chờ sai dạng.** Với dòng (1) đúng và dòng (2) rỗng, probe trả 0, JSON DAT và ghi `b'\n'`. Tình huống cũng có thể đến từ `cygpath -w` trả 0 nhưng stdout rỗng. Với dòng thứ ba thừa, helper trả 0 và chép dòng (2) bình thường. Hãy kiểm payload gồm đúng hai dòng và dòng (2) có giá trị, báo lỗi qua B3 khi tệp sai dạng, đồng thời từ chối đầu ra chuyển đổi rỗng ngay ở bộ chọn. Thêm test tệp một dòng, dòng (2) rỗng, dòng (3) thừa và stub Windows trả 0 với stdout rỗng. [Probe](probes.log)
> - **P3 · `.claude/dev/launcher_test.py:12078,12100,18286` · Thiếu phép đo độc lập cho dữ liệu chờ và lỗi đọc.** F tạo thư mục *trước khi bộ chọn ghi*, E/I làm hỏng *đích append*. Đột biến riêng nuốt lỗi đọc tệp chờ sống qua r1488. Đột biến riêng đảo thứ tự ghi tệp chờ và kênh cũng sống. Đột biến dòng trắng r1 nay chèn LF ở đích append. Chèn một dòng trắng ngay trong tệp chờ sống qua r1488, dù ca hình dạng r858 bắt thay đổi literal. Thêm fixture thay tệp chờ sau khi bộ chọn thành công, chốt lỗi đọc ở cả gọi trực tiếp và optional source, chốt dữ liệu thô của staging và chốt kênh vẫn chưa có DICH nếu ghi staging thất bại. Giữ đột biến tại từng điểm tương ứng. [Probe đột biến riêng](probes.log) · [Chi tiết đột biến](mut-detail.log)
> 
> - **P3 · `ops/cai_cong_cu.sh:226–241,244–247` · Lượt sau thừa hưởng dữ liệu của lượt tùy chọn thất bại dưới `allexport`.** Chạy `bash -a … --bat-buoc` với đích append là thư mục. Tiến trình ngoài trong công thức bắt buộc thấy `KQ=DICH<LF><ứng viên tùy chọn>` và hàm `_tl1488_chep_github_path` trong môi trường. Trên base cùng probe, các mục này vắng. `KENH_KQ` và `TAM_CAI` vắng ở cả hai vế. Hãy gỡ thuộc tính export của `KQ` sau lần gán cuối, và của helper sau định nghĩa. Thêm biến thể I dùng `bash -a`, trong đó tiến trình con ở lượt hai xác nhận bốn mục đều vắng. [Probe allexport](export.log)
> 
> ## B1–B6 và độ phủ
> 
> - B1/B2. Với dữ liệu hợp lệ, đường append duy nhất ở dòng 235, sau retry và dưới điều kiện `RC_CAI = 0`. `KQ` có một lần đọc có xét rc, giữ sentinel. Cả bước chép và phân nhánh PATH trích từ cùng chuỗi. K1/K2 không thể chép trước khi lỗi đọc dẫn tới rc 7. J dùng phiên bản 9.9.9 để chứng minh chọn Y, đồng thời chốt tệp đích rỗng và stderr. Ranh giới là rc công thức cuối. Probe `postcheck` cho công thức trả 0 sau khi xóa executable, append xảy ra rồi kiểm cuối trả 3. Phép kiểm cuối nằm ngoài điều kiện B2.
> - B3. Đọc staging một dòng hoặc đọc staging là thư mục đều báo lỗi và trả 1 ở đường trực tiếp. Probe optional với staging một dòng đi tiếp và công cụ bắt buộc ghi đúng một dòng. Đích append là thư mục cho hai chẩn đoán ở I và rc 1. Kênh cuối mất ở optional source vẫn thoát toàn batch với rc 7. D, I, optional-read và optional-channel đều dọn hết thư mục tạm. D và optional-read cho hai bản JSON từ những lượt kiểm vốn có. I và optional-channel thất bại trước khi có stdout. [Probe source](source-probe.log)
> - B4. Subshell giữ `KENH_KQ` của chính lượt. Mỗi retry có tên riêng và mỗi lượt source có `TAM_CAI` mới. C phát dấu ở `cat -- …/kq-thu-lai-1` sau khi retry thoát, kiểm cả dấu kích hoạt lẫn dấu bộ chọn nền ghi xong. Thay `cat` bằng builtin làm C đỏ tại chốt đồng bộ. Đột biến đọc tệp cũ khi writer ghi muộn làm C đỏ vì mất dòng đúng, với cảnh báo lệch danh tính. Dấu cách đầu/cuối, glob, dollar, nháy đơn và backslash trong đường dẫn vẫn giữ đúng byte ở probe `odd` dưới `bash -a`. Các lần mở tệp đều quote. `IFS= read -r` xử lý khoảng trắng và backslash.
> - B5/B6. G và H tạo staging trước, sau đó thực sự đi qua GIU_PATH và stdout fallback. Kênh mất/hỏng trả 7. Staging vắng giữ rc 0 khi DICH hợp lệ. Các ca cũ kiểm đích vắng/rỗng. Stub Windows kiểm đường dẫn POSIX cho PATH và dòng ghi là kết quả `cygpath -w`. YAML, launcher, hook và workflow nằm ngoài delta.
> - A/A' đo retry, DAT và byte đích. B đo lỗi công thức và đích rỗng. D đo lượt tùy chọn lỗi rồi lượt bắt buộc ghi đúng. E/I đo rc và stderr ở đích là thư mục. C/J/K1/K2 đều có phép đo về hành vi khai báo. K2 đo rc 7 trên lỗi chập chờn, còn wrapper riêng đếm đúng một lần đọc cho cả K1 và K2. Các assertion DAT/phiên bản của ca mới tìm chuỗi trong stdout. Chúng chưa parse JSON hay kiểm cleanup. Có thể làm rõ hai điểm này bằng kiểm JSON theo tên công cụ và assert thư mục tạm rỗng.
> - Khoảng trống trong riêng nhóm `wp1488_sh_*`. B1 thiếu đột biến đảo thứ tự và kiểm đúng hai dòng staging. B2 thiếu bỏ riêng guard đích rỗng/vắng hoặc staging vắng, dịch vị trí chép qua biên retry và nhánh lỗi, và phân kỳ ở lần đọc thành công thứ hai. B3 thiếu nuốt lỗi **đọc** staging. B4 đã đo kênh đầu và writer muộn, thiếu phép đo riêng về dữ liệu từ lượt source trước dưới allexport. B5 thiếu đột biến riêng cho GIU_PATH/stdout fallback, cleanup và định dạng JSON. Có đột biến cũ kiểm đích vắng, dạng kênh và lỗi đọc kênh. Lập luận hai guard chồng nhau chỉ giải thích trường hợp giữ nguyên phép so danh tính và dữ liệu chờ hợp lệ.
> 
> ## Probe và mã thoát
> 
> | Probe | rc probe | rc installer | Kết quả |
> |---|---:|---:|---|
> | partial / transient | 0 / 0 | 7 / 7 | Mỗi probe đếm một lần cat, tệp rỗng |
> | different-dich | 0 | 0 | DAT 9.9.9, tệp rỗng, cảnh báo |
> | giu-dat / fallback / giu-path | 0 / 0 / 0 | 0 / 0 / 3 | Cả ba tệp rỗng |
> | crlf / blank-line | 1 / 1 | 0 / 0 | `TinHieuChotCa` tại A', thấy CRLF / LF thừa |
> | late-only | 1 | 0 | `TinHieuChotCa` tại C, tệp thiếu dòng đúng |
> | no-cat-hook | 1 | — | `TinHieuChotCa` tại C, điểm đồng bộ đã đổi |
> | missing / corrupt | 0 / 0 | 7 / 7 | Kênh mất hoặc sai tiền tố, tệp rỗng |
> | odd | 0 | 0 | Byte đường dẫn chính xác, cleanup sạch |
> | newline / newline-collision | 0 / 0 | 0 / 0 | Tệp rỗng kèm cảnh báo / ghi `b'b\n'` |
> | one-line / read-dir | 0 / 0 | 1 / 1 | Lỗi đọc staging, tệp rỗng |
> | empty-line / extra-line / no-staging | 0 / 0 / 0 | 0 / 0 / 0 | Ghi LF / ghi dòng (2) / tệp rỗng |
> | postcheck | 0 | 3 | Công thức rc 0, append trước kiểm cuối |
> | order / no-read-error | 0 / 0 | theo fixture | Hai đột biến riêng sống qua ca r1488 |
> 
> ## Đối chiếu RESULTS.md và lệnh
> 
> - Hai lệnh diff yêu cầu, `git diff --check`, `git diff --quiet 42b5386..HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py`, `git merge-base --is-ancestor 8656dc0 HEAD`, kiểm SHA và sạch, `sha256sum`, clone/checkout và `git config core.abbrev 7` đều rc 0.
> - `python scratch/run.py repo checks` rc 0. Từng lệnh `bash -n ops/cai_cong_cu.sh`, `python .claude/dev/packet_loop.py doctrine-scan --root .` và `python ops/lease_publish.py check ops/leases/wp1488-r2-g2-claude.yaml` rc 0. Doctrine quét 12 tệp, 0 chỗ chép. Lease check đo cục bộ. [Log](checks.log)
> - `python scratch/run.py repo r1488` gọi đúng CLI `--lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan 3`, rc 0, 3/3. Đối chiếu ba lần chạy lịch sử bằng `python scratch/run.py {ab,b7,r2} r1488 {3,2,2}` (từng cặp tương ứng) đều rc 0, lần lượt 3/3, 2/2, 2/2 như khai. [HEAD](head-r1488.log) · [ab](ab-r1488.log) · [b7](b7-r1488.log) · [r2](r2-r1488.log)
> - `python scratch/run.py {repo,base} cases` chạy từng clone riêng. Cả hai bên 33 rc 0, một rc 1, wrapper rc 1. Ca duy nhất lỗi là `r858_goc_tam_tranh_to_tien_co_git`. Tại đây `/tmp/.git` tồn tại, fixture chọn `/var/tmp` chỉ đọc và gặp EROFS. Ca hình dạng và stub Windows qua cả hai vế. Vì vậy không tái lập được 34/34 trong môi trường khai; delta hai vế vẫn bằng 0. [HEAD](head-cases.log) · [Base](base-cases.log)
> - `python scratch/probe.py TEN` chạy từng hàng như bảng. Các lượt `newline` có giá trị trong bảng dùng biến môi trường. Lần dựng đầu nhúng LF trực tiếp vào công thức một dòng và installer rc 2 do cú pháp, đã chạy lại bằng fixture đúng. `python scratch/source-probe.py` rc 0 ở wrapper. `python scratch/probe.py base-B` rc 0, installer rc 1 và có dòng ứng viên như khai. [Base B](base-B.log)
> - `python scratch/detail.py` kiểm từng đích. Các phản chứng dùng script base, `2847860`, `b7a280e` đỏ lần lượt ở A, G, J. 12 đột biến r1488 chết bằng `TinHieuChotCa`, thứ tự bảng RESULTS là A, B, A', I, A', J, A', A', I, C, K1, F. Đột biến wp858 đổi neo chết ở cả Linux và hình dạng. Lần gọi detail đầu rc 1 vì đọc đúng lúc clone probe đang có đột biến riêng, lần chạy lại lấy script từ Git HEAD. [Chi tiết](mut-detail.log)
> - `python scratch/run.py {base,repo} registry` rc 0 mỗi vế, đo 454/789 và 455/801 mục đăng ký, khớp delta +1/+12. Mẫu số thực thi và tỷ lệ thắng của toàn bộ đột biến cần phép chạy riêng.
> 
> - `python scratch/run.py repo mut` rc 0. Wrapper lọc `DOT_BIEN_HOOK` trong bộ nhớ theo loại `cai_sh`, rồi gọi CLI `--dot-bien`. Dòng cuối `DOT BIEN: 92/92 dat`, khớp RESULTS. [Log cai_sh](head-mut.log)
> - `python scratch/export-probe.py` rc 0. Hai installer rc 1 như dự kiến. Probe thứ hai dùng đầu ra phân cách bằng NUL để giữ nguyên giá trị KQ nhiều dòng. [Log allexport](export.log)

### Review Rescue Checkpoint sau lượt 3 → revision 3

Trần Codex (3) hết. Ba lượt liền ra ca biên mới quanh cùng một thứ: tệp chờ. Chủ kho chọn qua AskUserQuestion (21-11-2026
~10:30Z) **"Bỏ tệp chờ (r3), Codex lượt 4"**, rồi duyệt đặc tả r3 `ops/specs/wp1488-r3.md` (sha256 `691a710c…16d7`). Lease
`wp1488-r3-g3-claude` thay `wp1488-r2-g2-claude` (bia mộ hai chiều); trần Codex cả packet 4.

### Executor xử lý (sửa ở `f8747c4`, đặc tả r3)

| Finding | Xử lý |
|---|---|
| P2 LF trong đường dẫn phá phép so danh tính | Không còn phép so danh tính (bỏ tệp chờ). Dòng `$GITHUB_PATH` dựng thẳng từ `DICH` của lần đọc kênh duy nhất; `DICH` hay dòng đã đổi có `\n`/`\r` ⇒ từ chối, `RC_CAI=1`. Kịch bản L-LF, L-CR (đường dẫn qua biến môi trường); đột biến `wp1488_sh_bo_tu_choi_xuong_dong` chết ở (L-LF). |
| P3 tệp chờ sai dạng; `cygpath -w` rc 0 mà rỗng | Không còn tệp chờ. Dòng đổi rỗng ⇒ từ chối. Kịch bản W (cygpath giả `CYGPATH_W_RONG`); đột biến `wp1488_sh_bo_tu_choi_dong_rong` chết ở (W). |
| P3 thiếu đột biến cho đọc tệp chờ / thứ tự ghi | Không còn tệp chờ nên không còn hai điểm ấy. `cygpath` giả nay IN rồi mới thoát 37 khi hỏng, nên `wp858_sh_nuot_loi_cygpath_w` đo việc xét mã thoát chứ không nhờ chuỗi rỗng. |
| P3 `KQ` và hàm mới lộ export dưới `bash -a` | `export -n KQ` sau lần gán cuối, `export -nf _tl1488_ghi_github_path` sau định nghĩa. Kịch bản M (`bash -a` + `--bat-buoc`, tiến trình con lượt sau chụp `env`); đột biến `wp1488_sh_kq_lo_export` và `wp1488_sh_ham_lo_export` chết ở (M). |

Kèm theo: (J) đổi kỳ vọng — PATH nội bộ và `$GITHUB_PATH` cùng là `DICH` mà công thức tự ghi (một nguồn); script r2
`42b5386` ĐỎ ở (J). Đột biến `wp1488_sh_doc_kenh_cu_ghi_muon` viết lại để đọc SAU khi móc của (C) kích hoạt (bản đầu chọn tệp
trước lúc writer muộn ghi nên sống); nay chết ở (C). Ba đột biến wp858 (`nuot_loi_cygpath_w`, `github_path_khong_qua_cygpath`,
`github_path_vang_khong_mac_dinh`) dời neo sang `_tl1488_ghi_github_path`. Bảng `cai_sh` (mọi packet): 93/93.

## Lượt 4 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 4/4 (hết trần cả packet) · đặc tả r3

- Exact head được review: `50a3566c7b09c5bcfe5ea4071ec49a2aaeab265e` (mã trùng `f8747c4`). Chạy 2026-11-21T11:14:42Z → 11:26:54Z, rc 0.
- sha256 `scratch/VERDICT.md`: `a7a82a2621877e6151e6e3be0649af01e12a456c3897c73ccc6b59c81217117a`.
- Kết luận: `request_changes` (1 P2, 2 P3). Các finding lượt 3 reviewer xác nhận đã đóng (bảng probe trong nguyên văn).

### Nguyên văn

> # Review độc lập WP1488 r3 · lượt 4/4
> 
> reviewed_sha: 50a3566c7b09c5bcfe5ea4071ec49a2aaeab265e
> verdict: request_changes
> reviewer: codex (OpenAI), codex_cli, read-only
> 
> HEAD khớp `HEAD_SHA.txt`. Cây sạch và base `8656dc0176ed108e12c209ba55c91a1f6f9d612f` là tổ tiên. SHA-256 đặc tả khớp `691a710c1fea5309f677c2a7bf38815897befeb7bb248275b17c3df952f216d7`. Diff nằm trong write set. Sau `f8747c48b52573a8f64c4dc2a190031f67e1f83a` chỉ đổi RESULTS và VERDICT. Kiểm lease r3 cục bộ qua.
> 
> ## Findings
> 
> - **P2 · `ops/cai_cong_cu.sh:222–224` · Nhận nhầm lượt dùng `--win`.** Trên stub Windows, `chon_thu_muc_chay_duoc "--win" git …` hoặc dùng tab trước `--win` ghi đường dẫn POSIX, rc 0. Base ghi đường đã đổi `W:<dir>` vì bộ chọn nhận đối số thực. Với `: 'chon_thu_muc_chay_duoc --win git' && chon_thu_muc_chay_duoc git …`, hoặc nhánh `--win` không chạy, head vẫn đổi `W:<dir>`, còn base ghi `<dir>`. Một lần gọi thật ở giữa chuỗi, dạng literal như bản kê hiện tại, chạy đúng. Hãy lấy chế độ chuyển đổi từ thông tin gắn với **kết quả cuối thực sự được ghi**, qua cùng lần đọc kênh. Nếu cần metadata thì cập nhật hợp đồng định dạng đã đóng băng trước khi triển khai. Thêm ca stub Windows so byte cho đối số có nháy/tab và đối chứng chuỗi dữ liệu hoặc nhánh không chạy, giữ thêm ca công thức không dùng bộ chọn đi qua stdout. Năm công thức Windows hiện hành dùng đúng literal nên các ca hiện tại vẫn xanh. [Head](head-probes-final.log) · [Base](base-probes-final.log)
> - **P3 · `ops/cai_cong_cu.sh:224–229` · Mất LF cuối trước khi kiểm dữ liệu đã đổi.** Stub `cygpath -w` trả 0 và in `W:<dir>\n\n`. Bash bỏ mọi LF ở đuôi khi lấy kết quả, helper chấp nhận và append `W:<dir>\n`. Kết quả hai dòng vượt kiểm tra B2. LF giữa hoặc CR còn nguyên thì head từ chối đúng. Hãy giữ stdout bằng sentinel trong khi kiểm mã thoát, bỏ tối đa một LF kết thúc dòng của giao thức, rồi từ chối LF/CR còn lại và payload rỗng. Mở rộng W với stub in thêm một LF ở đuôi, LF giữa và CR, chốt rc 1, stderr và tệp rỗng. [Probe](head-probes-final.log)
> - **P3 · `.claude/dev/launcher_test.py:12052,12171–12185,18336` · Chưa khóa một lần đọc trên đường thành công và việc kiểm dữ liệu Windows sau đổi.** K1/K2 kiểm đường lỗi đọc đầu. C chốt writer muộn, không đếm lần đọc. Đột biến riêng đọc thêm đúng một lần chỉ sau lần đầu thành công sống qua r1488. Đột biến riêng chỉ kiểm LF/CR trong DICH, bỏ kiểm đầu ra `cygpath`, cũng sống. Hãy đếm lượt mở kênh ở đường thành công và thêm stub trả hai payload phân biệt, hoặc thành công lần đầu rồi lỗi lần hai. Bổ sung W như trên và gắn mỗi đột biến riêng vào ca đích. [Đột biến riêng](detail-own.log)
> 
> ## B1–B6
> 
> - B1/B2/B4. Trong `cai_cong_cu.sh` chỉ có một lệnh append, ở helper sau vòng retry và trong nhánh `RC_CAI=0`. Bộ chọn chỉ ghi kênh kết quả. `cat -- "$KENH_KQ"` chỉ đọc một lần, giữ LF qua sentinel, rồi hai nhánh dùng cùng `KQ`. Mỗi retry dùng tệp riêng. C đợi writer cũ ghi thành công trong lần đọc kênh cuối thật. Mỗi lượt source có `TAM_CAI` mới. Công thức thật của actionlint gọi `ops/cai_actionlint.sh:226`, tự append sau kiểm phiên bản. Đường ghi đó có từ base và nằm ngoài thay đổi stdout fallback theo §5. Các công thức selector hiện hành do helper ghi đúng một lần. Probe postcheck cho công thức rc 0 rồi kiểm cuối rc 3 ở cả base và head, với một dòng đã ghi. Điều kiện B2 là mã của công thức cuối.
> - B3. Lỗi chuyển đổi, từ chối hoặc append thất bại đều báo stderr và đặt `RC_CAI=1` trước nhánh lỗi. E và I đo đích là thư mục. I đi tiếp qua công cụ tùy chọn và kết thúc khác 0 ở công cụ bắt buộc, với hai chẩn đoán. Lỗi đọc kênh trực tiếp giữ rc 7, kể cả nếu cat in đủ rồi lỗi. Các lệnh sau append nằm ngoài phạm vi chính sách đó.
> - B5. G/H cho rc 0 và tệp rỗng trên head khi selector trước đó đã ghi DICH nhưng kết quả cuối là GIU_PATH hoặc kênh rỗng. Base từng append ở lần gọi selector đầu của chính fixture G/H. Công thức stdout thuần không gọi selector giữ rc 0, DAT và tệp rỗng ở cả hai vế. Windows không qua selector và đi qua stdout cũng giữ hành vi ấy. Một công thức tự ghi DICH được xử lý theo B2 như J. Guard đích vắng/rỗng trả trước kiểm đường dẫn hay chuyển đổi, để PATH nội bộ dùng giá trị nguyên văn. Đường dẫn dấu cách đầu/cuối, glob, dollar, nháy đơn và backslash ghi chính xác dưới `bash -a`. Cả M và probe lỗi append dưới allexport đều không thấy `KQ` hay helper trong môi trường con lượt sau. Biến local `_tl1488_w` được allexport trong phạm vi helper, nên tiến trình cygpath có thể thấy đường dẫn vốn đã có trong argv. Sau khi helper trả về, biến local hết phạm vi. Dọn tạm dùng nhánh cũ, stdout JSON do checker cũ phát.
> - B6. YAML, launcher, hook phiên và workflow giữ nguyên theo diff.
> 
> ## Probe đối chứng
> 
> | Probe | RC installer head | Kết quả |
> |---|---:|---|
> | newline | 1 | Tệp rỗng, báo xuống dòng |
> | newline-collision | 0 | DICH cuối là thư mục tiền tố `a`, ghi đúng `a\n`; rg ở đó là 8.8.8 |
> | one-line / empty-line / extra-line / read-dir / no-staging | 0 mỗi ca | Can thiệp đúng tên staging r2 không tác động kết quả, mỗi ca ghi đúng DICH |
> | odd | 0 | Giữ nguyên byte đường dẫn dưới allexport |
> | missing / corrupt | 7 / 7 | Tệp rỗng, lỗi đọc / sai dạng |
> | partial / transient | 7 / 7 | Tệp rỗng, đúng một lần cat ở mỗi ca |
> | second-success | 0 | Một lần cat thành công, lần thứ hai nếu có sẽ lỗi, tệp đúng |
> | postcheck | 3 | Ghi một dòng, có JSON checker; base cùng rc |
> | Windows literal / có nháy / tab / khớp trong dữ liệu / nhánh không chạy | 0 mỗi ca | Chỉ literal đúng như base, bốn biến thể còn lại lệch như finding |
> | Windows stdout / -w lỗi / -w rỗng / -w LF giữa / -w CR / -w LF thừa ở đuôi | 0 / 1 / 1 / 1 / 1 / 0 | Năm ca đầu tệp rỗng, ca cuối ghi đường dẫn đã đổi |
> | allexport append-fail | 1 | Công cụ tùy chọn đi tiếp, no leak trong env của lượt sau, thư mục tạm rỗng |
> 
> `python scratch/probes.py head` và `python scratch/probes.py base` dùng fixture Linux và cygpath giả. Mã wrapper và mã installer nằm riêng trong log. Tôi chạy lại sau khi đổi fixture staging sang đúng tên dùng ở r2 và đặt hai executable vào đúng thư mục của công thức batch. [Head](head-probes-final.log) · [Base](base-probes-final.log)
> 
> ## Độ phủ và đối chiếu RESULTS.md
> 
> - A/A' có dấu update, rc, DAT và byte đích. B/D đo lỗi công thức và byte đích. C chốt cả hai dấu đồng bộ, rc và byte đích. E/I chốt stderr và rc ở đích là thư mục. G/H đo kết quả cuối. J chốt 9.9.9 và byte Y. L-LF/L-CR đo DICH có newline. M chốt môi trường con và hai dòng thành công. W đo stdout chuyển đổi rỗng. K1/K2 chốt rc 7, stderr và tệp rỗng. Không thấy kịch bản liệt kê nào chỉ dựng fixture rồi bỏ assertion. K1/K2 không đếm lượt đọc, A/J chỉ tìm chuỗi trong stdout thay cho parse JSON, và r1488 không chốt cleanup. Docstring và chẩn đoán C còn nhắc tệp chờ của r2 dù fixture đã đổi.
> - **B1** có đột biến append trực tiếp và neo hình dạng. Thêm một ghi khác trong bộ chọn chưa được đo hành vi. **B2** có bỏ guard RC, ghi đôi, dòng trắng, CRLF, bỏ từ chối newline và đọc riêng trước. Còn thiếu ca đột biến đọc lần hai sau lần đầu thành công, bỏ kiểm riêng dữ liệu đã đổi, giữ sai một LF dư, phân loại nhầm cú pháp `--win`, và chỉ bỏ cổng chạy theo DICH. Ba neo wp858 đo conversion, rc của conversion và đích unset. **B3** có nuốt rc và thoát ngay, I phân biệt với errexit. Lỗi conversion hoặc từ chối riêng ở công cụ tùy chọn chưa có phép đo riêng. **B4** có đột biến chọn kênh lượt đầu sau writer muộn, chưa có mutant chọn kênh retry trung gian hoặc của source trước. **B5** có hai đột biến export và các ca G/H, chưa có mutant riêng phá GIU_PATH/stdout trong 13 mục mới. Cleanup optional có đột biến cũ wp1045. Ca cũ cũng đo đích vắng/rỗng, định dạng kênh và stdout JSON.
> - RESULTS ghi ba đổi neo wp858 rồi liệt kê cả mục thứ tư `wp858_sh_nuot_loi_ghi_github_path`. Có bốn mục động đến helper mới. Mục thứ tư chết ở E khi gọi r1488 riêng, và có hai đích đăng ký là r858 Linux và hình dạng. Đột biến bỏ hẳn `cygpath -w` nằm ở wp858, tổng số wp1488 mới là 13.
> - Phản chứng bằng script cũ với ca r3 hiện hành đỏ tại A trên `8656dc0`, G trên `2847860`, J trên `b7a280e` và J trên `42b5386`. Assertion ở `b7a280e` dùng kỳ vọng r3 trong phép chạy này. Lời khai lịch sử mô tả kỳ vọng r2. Probe A/B riêng tái lập base có một dòng từ lượt lỗi, head có tệp rỗng. Rc A/B lần lượt 0/1 ở cả hai vế. A parse JSON và thấy DAT. [Phản chứng](detail-old.log) · [Base](base-probes-final.log) · [Head](head-probes-final.log)
> - 13 đột biến wp1488 đều chết bằng `TinHieuChotCa`. Theo đúng thứ tự bảng RESULTS, các chốt là A, B, I, A', A', A', I, C, L-LF, L-LF, M, M, W. Ba neo wp858 được nêu tên chết ở các đích đã khai, cả đích động lẫn hình dạng. Đột biến riêng thêm LF vật lý ở append đỏ tại A'. Hai đột biến riêng còn lại sống như nêu trong finding. [Chi tiết](detail-table.log) · [Đột biến riêng](detail-own.log)
> - Bộ đăng ký có 454 ca và 789 đột biến trên base, 455 và 802 trên exact head. Delta +1/+13 khớp. Nếu cùng 7 mục không đo được như lời khai, số đo được tương ứng là 782 và 795. Đây là đối chiếu mẫu số đăng ký. [Base](base-registry.log) · [Head](head-registry.log)
> 
> ## Lệnh và mã thoát
> 
> - `bash scratch/preflight.sh` rc 0. Từng lệnh `rev-parse`, `cmp`, `status --porcelain`, `sha256sum -c`, `merge-base --is-ancestor`, hai lệnh diff theo yêu cầu và hai lệnh liệt kê tệp đều rc 0. `git diff --check 8656dc0..HEAD` rc 2 vì khoảng trắng cuối dòng trong trích dẫn verdict lịch sử. Cùng lệnh giới hạn ở hai tệp mã rc 0. Clone bằng `git clone -q --no-hardlinks repo scratch/<đích>`, checkout detached theo SHA và đặt `core.abbrev 7`, rc 0. `GIT_OPTIONAL_LOCKS=0 git -C repo status --porcelain` sau phép đo rc 0, rỗng. [Preflight](preflight.log)
> - `python scratch/run.py head repeat 3` gọi `python .claude/dev/launcher_test.py --lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan 3`. Rc 0, 3/3. Cùng wrapper trên `ab298a8`, `b7a280e`, `42b5386`, `f8747c4` với 3/2/2/2 lượt cho đúng 3/3, 2/2, 2/2, 2/2, đều rc 0. [Exact head](head-repeat.log) · [ab298a8](ab298a8-repeat.log) · [b7a280e](b7a280e-repeat.log) · [42b5386](42b5386-repeat.log) · [f8747c4](f8747c4-repeat.log)
> - `python scratch/run.py head cases` và `python scratch/run.py base cases` chạy đủ sáu nhóm, từng ca bằng `--lap-ca TEN --lan 1`. Mỗi vế 33 lệnh rc 0 và một lệnh rc 1, wrapper rc 1. Ca lỗi duy nhất là `r858_goc_tam_tranh_to_tien_co_git`. Sandbox có `/tmp/.git`, nên ca chọn `/var/tmp` và gặp EROFS. Delta bằng 0 giữa hai vế tại đây. Executor khai 34/34 trên base khi `/tmp/.git` vắng. Bản dựng thử trước khi cập nhật neo có 33/34 theo lời khai, chưa được dựng lại. [Exact head](head-cases.log) · [Base](base-cases.log)
> - `python scratch/run.py head checks` rc 0. `bash -n ops/cai_cong_cu.sh`, `python .claude/dev/packet_loop.py doctrine-scan --root .` và `python ops/lease_publish.py check ops/leases/wp1488-r3-g3-claude.yaml` đều rc 0. Doctrine quét 12 tệp, 0 chỗ chép, khớp RESULTS. Lease check chỉ đo cục bộ. [Log](head-checks.log)
> - `python scratch/run.py {base,head} registry`, từng vế rc 0. `python scratch/probes.py {base,head}`, từng vế rc 0 ở cả lần đầu và lần đã sửa fixture. `python scratch/detail.py table`, `old` và `own`, mỗi wrapper rc 0. Trong log chi tiết, `rc_equiv=1` là ngoại lệ assertion được wrapper bắt, không phải mã thoát tiến trình wrapper.
> - `python scratch/collision-json.py head` rc 1 ở lần đầu do probe đọc nhầm khóa JSON. Sau khi dùng `ban_thay.mac_dinh`, rc 0, xác nhận byte tệp đích và phiên bản 8.8.8. [Lần đầu](collision-json-initial.log) · [Lần đo](collision-json.log)
> - `python scratch/edge.py` rc 0. Với đích unset/rỗng, installer rc 0, byte đích rỗng, PATH nội bộ tìm đúng rg 9.9.9 trong đường dẫn có LF. Ép GIU_PATH khi rg chưa DAT cho rc 3 và tệp rỗng. Kênh mất ở lượt tùy chọn thoát batch rc 7, lượt sau chưa chạy. Từ chối DICH có LF ở lượt tùy chọn cho batch rc 0, chỉ ghi dòng của công cụ bắt buộc. Hai probe batch dọn hết thư mục tạm. [Log](edge.log)
> - `python scratch/run.py <clone> cai-sh` lọc `DOT_BIEN_HOOK` theo loại trong bộ nhớ rồi gọi `main` với `--dot-bien`. Trên `b7a280e`, `42b5386` và exact head, rc 0 mỗi vế, dòng cuối lần lượt là `DOT BIEN: 90/90 dat`, `DOT BIEN: 92/92 dat` và **`DOT BIEN: 93/93 dat`**, khớp RESULTS. Lần đầu gọi thẳng `chay_dot_bien` trên base và head cho 80/80 và 93/93, cả hai trả tuple `(0, 0)` nghĩa là 0 lỗi và 0 mục không đo được. Wrapper đầu truyền tuple vào `SystemExit` nên thoát 1, đã sửa ở lần gọi qua CLI. [Exact head](head-cai-sh.log) · [b7a280e](b7a280e-cai-sh.log) · [42b5386](42b5386-cai-sh.log) · [Base lần đầu](base-mut.log) · [Head lần đầu](head-mut.log)
> - Probe shell `bash -a -c` định nghĩa một hàm với `local _tl1488_w="$1"` rồi so môi trường con trong và sau lời gọi, rc 0. Biến xuất hiện chỉ trong phạm vi hàm.
> - GitHub connector đọc workflow theo exact SHA và đọc job của gate, cả hai trả thành công. Tại lần kiểm cuối, `lease-pr` success, workflow Windows skipped và `gate` in progress. Kết quả này chưa xác nhận N4 xanh. [Lease](https://github.com/ducthangho/tra-luat/actions/runs/44898169090) · [Windows](https://github.com/ducthangho/tra-luat/actions/runs/44898169109) · [Gate](https://github.com/ducthangho/tra-luat/actions/runs/44898169152)
> - `python scratch/run.py base suite` và `python scratch/run.py head suite` gọi toàn bộ `python .claude/dev/launcher_test.py`, cả hai rc 1. Base **429/444 qua, 10 bỏ qua, 15 lỗi, tổng 454**. Head **430/445 qua, 10 bỏ qua, 15 lỗi, tổng 455**. `diff -u` trên danh sách tên ca lỗi/bỏ qua rc 0, hai danh sách giống hệt. Có hai ca POSIX/native Windows bỏ qua như lời khai và tám ca không dựng được venv/pip. Các lỗi trùng nhau ở hai vế gồm hai lỗi EROFS ở `/var/tmp`, nhóm Codex home/credential và hai ca r1335 phụ thuộc launcher khởi chạy được. Tôi đo delta +1 ca qua, 0 lỗi mới trong môi trường này. Số tuyệt đối 452/452 và 453/453 của executor không tái lập ở sandbox này. [Base](base-suite.log) · [Exact head](head-suite.log)
> 
> ## Không đo được
> 
> - Toàn bộ `--dot-bien` ngoài `cai_sh` chưa chạy. Các kết quả 782/782, 788/788, 792/792, 794/794, 795/795 và bảy trường hợp Windows không đo được là lời khai executor. Phép kiểm bộ đăng ký xác nhận delta +13 trên head. Số 15 trong commit message `f8747c4` lệch với 13 mục thực tế như RESULTS đã đính chính.
> - Chưa chạy native macOS/Windows hay dùng `$GITHUB_PATH` thật trên runner. Các phép thử Windows dùng cygpath giả trên Linux. Gate trên exact SHA chưa trả kết luận ở lần đọc cuối.

### Review Rescue Checkpoint sau lượt 4

Trần Codex (4) hết; lượt 4 không có P0/P1. Chủ kho chọn qua AskUserQuestion (21-11-2026 ~12:10Z) **"Sửa 2 P3, nợ P2"**:
sửa hai P3 trong phạm vi đặc tả r3, ghi P2 thành nợ có tên, KHÔNG gọi thêm Codex; chủ kho duyệt merge trên bằng chứng của
executor.

### Executor xử lý (sửa ở `7a8823b`, đặc tả r3)

| Finding | Xử lý |
|---|---|
| P3 `$( )` ăn LF đuôi của `cygpath -w` | Đọc qua sentinel `x`, bỏ đúng một LF kết thúc dòng; LF/CR còn lại bị chốt xuống dòng từ chối. `cygpath` giả thêm `CYGPATH_W_KIEU=du_lf\|cr`; (W) chạy ba biến thể (rỗng, thừa LF đuôi, CR). Script `f8747c4` ĐỎ ở (W-du-lf). Đột biến `wp1488_sh_cygpath_an_lf` và `wp1488_sh_chi_xet_dich` (chỉ xét `DICH`, bỏ xét dòng đã đổi) chết ở (W-du-lf). |
| P3 thiếu phép đếm một lần đọc trên đường thành công | (K3): `cat` giả đầu PATH đếm số lần mở kênh `*/kq`; đường thành công phải đúng 1 lần. Đột biến `wp1488_sh_doc_kenh_hai_lan` (đọc thêm một lần sau lần đầu thành công) chết ở (K3). |
| **P2 nhận biết `--win` bằng chuỗi trong `LENH`** | **Nợ có tên `WP1488-WIN-THEO-LENH`** (chủ kho chọn). Script nhận chế độ Windows khi `LENH` chứa đúng chuỗi `chon_thu_muc_chay_duoc --win ` (có dấu cách). Năm công thức Windows hiện có trong `ops/cong_cu.yaml` viết đúng literal nên chạy đúng (`r858_cai_windows…` đạt). Sai khi: `"--win"` có nháy, tab thay dấu cách, chuỗi ấy nằm trong dữ liệu, hoặc nằm ở nhánh không chạy. Sửa tận gốc phải mang chế độ `--win` qua kênh kết quả, tức đổi định dạng kênh đã đóng băng (B5). |

Hai neo `wp858_sh_nuot_loi_cygpath_w` và `wp858_sh_github_path_khong_qua_cygpath` dời theo dòng `cygpath -w` mới. Bảng `cai_sh`
(mọi packet): 96/96.

## Lượt 5 — Codex (OpenAI), `codex_cli`, read-only · lời gọi 5/5 (hết trần cả packet) · đặc tả r4, chỉ xét delta r4

- Exact head được review: `7b35edcc8cfbb562ef2cfad6edee5a9c3db22d6b` (mã trùng `ab83dd3`). Chạy 2026-11-21T13:59:36Z → 14:04:03Z, rc 0.
- sha256 `scratch/VERDICT.md`: `7d5bc9bc14f540bccef7c26a2c235c8534938a80841d2e4fa3726afbd5ff4b2e`.
- Kết luận: `request_changes` (1 P2, 2 P3).

### Nguyên văn

> reviewed_sha: 7b35edcc8cfbb562ef2cfad6edee5a9c3db22d6b
> verdict: request_changes
> reviewer: codex (OpenAI), codex_cli, read-only
> reviewed_tree: 605ac8b0256a5811b36653f6c18ef6038b1e9b29
>
> # Packet #1488 r4 · lượt 5
>
> HEAD khớp `HEAD_SHA.txt`, worktree sạch trước và sau review. SHA-256 của spec là `a4888c7e5aae5cf1057cd93db754a1e16acacf52e841fb7398d35afc0454d1ad`, khớp yêu cầu và lease revision 4 generation 4. So với mã `ab83dd3638ae0bc8a6f2aec35ae789c06dd7c66f` trong §9, HEAD chỉ đổi `RESULTS.md`. Phép đo chạy trong clone dưới `scratch/`, với Linux, Bash 5.2.21, Python 3.13.18 và `cygpath` giả.
>
> ## Findings
>
> - **P2 — Kênh sai dạng kích hoạt nhánh Windows.** Tại `ops/cai_cong_cu.sh:243`, Bash bỏ byte NUL trong command substitution. Công thức thử ghi các byte `DICH_WIN\x00\n<dir POSIX tốt>` rồi trả 0. r4 cảnh báo `ignored null byte in input`, nhưng gọi `cygpath -w`, ghi một dòng `W:<dir>`, dùng PATH đã chọn và trả 0. Cùng đầu vào trên r3 trả 7 và giữ tệp đích rỗng. Theo B5, nhãn hỏng phải trả 7. Kiểm tra byte ngay trong lần đọc duy nhất, trước khi chuyển dữ liệu vào biến Bash, giữ nguyên xử lý lỗi đọc và LF cuối. Thêm ca ghi nhãn có NUL, đòi rc 7, tệp rỗng và log `cygpath` rỗng. Probe `bad-nul-tag` đã đỏ trên HEAD.
> - **P3 — Các ca r4 bỏ lọt nhãn sai gần với nhãn hợp lệ.** Tại `.claude/dev/launcher_test.py:12197` và `:12797`, ca hành vi (N) dùng kênh hợp lệ và ca hình dạng chỉ tìm nhánh hợp lệ. Đột biến riêng thêm `DICH_WINx*) DICH="" ;;` sau nhánh PATH hợp lệ sống qua cả bốn ca đích. Với kênh `DICH_WINx\n<dir>`, HEAD trả 7, đột biến đi tới hậu kiểm và trả 3. Thêm ca ghi trực tiếp nhãn có hậu tố và nhãn thiếu payload, chốt rc 7, chẩn đoán kênh hỏng, tệp rỗng và không có lần gọi đổi đường dẫn. Probe `bad-prefix` đã xanh trên HEAD và đỏ trên bản đột biến.
> - **P3 — Hai dòng trong bảng đột biến §9 ghi nhầm assertion đầu tiên.** Tại `ops/acceptance/wp1488/RESULTS.md:170` và `:173`, `wp1488_sh_bo_chon_luon_dich` và `wp1488_sh_dich_win_khong_doi` được ghi chết ở (W-rong). Chạy từng đột biến trên mã tương đương cho thấy cả hai chết ở (I-win), trước (W-rong), với rc 0 và hai dòng trong tệp đích. Đột biến thứ hai cũng chết ở ca Windows riêng như lời khai. Sửa bảng theo kết quả của các lượt chạy riêng có in nội dung `TinHieuChotCa`.
>
> ## Đối chiếu B1, B2, B5
>
> - Bộ chọn đánh dấu theo đối số đầu đã phân tích của lần gọi thực. Khi tên trần đã DAT, `GIU_PATH` vẫn được ghi. Probe với hai lần gọi liên tiếp theo cả hai thứ tự xác nhận lần ghi cuối quyết định chế độ. Công thức tự ghi đè kênh theo cả hai chiều cũng cho kết quả theo nhãn cuối. Vì công thức có quyền ghi kênh, nó có thể tự khai `DICH_WIN` dù không hề gọi bộ chọn với `--win`. Đây là hệ quả của B2 lấy chính nội dung cuối làm nguồn cho cả hai nhánh. Hai probe đổi chế độ giữa lần thử thất bại và lần #1479 thành công đều lấy kết quả của lần thành công.
> - Kênh được đọc sau retry, khi `RC_CAI=0`. Hai mẫu `DICH` và `DICH_WIN` đòi LF ngay sau nhãn và payload có ít nhất một ký tự. `DICH_WINx` và `DICH_WIN` thiếu payload trả 7 trong probe. `GIU_PATH` không ghi và giữ PATH. Kênh rỗng dùng dòng cuối stdout, không ghi. Nhánh `DICH_WIN` dùng đường POSIX cho PATH nội bộ và đường đã đổi cho tệp đích. Ngoại lệ với byte NUL nêu ở P2.
> - Hàm ghi dùng hai đối số, `GITHUB_PATH` và lệnh `cygpath` tra qua PATH. Hàm không đọc `LENH`. Tệp đích rỗng/vắng làm hàm trả 0 trước khi đổi đường dẫn. Khi đổi lỗi, nhánh Windows đặt `RC_CAI=1`. (I-win) đã đo lượt `source` của công cụ tùy chọn đi tiếp. Ca Windows riêng đo lỗi khi gọi trực tiếp. Việc gỡ export và dọn thư mục vẫn qua các chốt cũ.
> - (N) chốt byte chính xác và JSON DAT. Fixture dùng thư mục POSIX và `cygpath` giả là nơi duy nhất trong công thức thử sinh ra `W:`. Probe ghi log xác nhận hai ca dương gọi đúng `-u` rồi `-w`, hai ca âm không gọi. (I-win) chốt chẩn đoán từ nhánh lỗi, thông báo đi tiếp và đúng một dòng của công cụ bắt buộc. Probe độc lập còn xác nhận hai lời gọi đều nhận thư mục của công cụ tùy chọn và lời gọi `-w` giả trả 37.
> - Năm đột biến r4 có chốt cho phát nhãn, bỏ suy từ văn bản, nhận nhãn trong PATH, truyền chế độ đổi và truyền lỗi. Chưa có đột biến riêng cho ranh giới nhãn hỏng, hai lần gọi trái chế độ, công thức ghi đè nhãn Windows, thay đổi chế độ giữa các retry, hay nhánh `DICH_WIN` khi vắng `GITHUB_PATH`. Chốt hình dạng đếm đúng một dòng `cat -- "$KENH_KQ"`, nhưng K3 đo lượt thành công POSIX. Đếm bằng stub trong một ca thành công `DICH_WIN` sẽ phủ lượt đọc phụ chỉ xảy ra ở nhánh mới.
>
> ## Lệnh và mã thoát
>
> Các lệnh clone, `git -C repo rev-parse HEAD`, `git -C repo status --porcelain`, `sha256sum repo/ops/specs/wp1488-r4.md`, `git -C repo rev-parse 'HEAD^{tree}'`, `git -C repo diff 7a8823b..HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py`, `git -C repo diff --check 7a8823b..HEAD` và `git -C repo diff --exit-code ab83dd3 HEAD -- ops/cai_cong_cu.sh .claude/dev/launcher_test.py` đều rc 0. Clone bằng `git clone --no-hardlinks repo scratch/clone`. Các phép thử dùng thư mục tạm dưới `scratch/`.
>
> | Lệnh trong `scratch/clone` | rc | Kết quả |
> |---|---:|---|
> | `python .claude/dev/launcher_test.py --lap-ca r1488_github_path_chi_ghi_khi_thanh_cong --lan 2` | 0 | 2/2, 0 bỏ qua |
> | `python .claude/dev/launcher_test.py --lap-ca r858_hinh_dang_cong_thuc_cai --lan 1` | 0 | 1/1 |
> | `python .claude/dev/launcher_test.py --lap-ca r868_hinh_dang_kenh_ket_qua --lan 1` | 0 | 1/1 |
> | `python .claude/dev/launcher_test.py --lap-ca r868_ghi_kenh_hong_thi_dung --lan 1` | 0 | 1/1 |
> | `python .claude/dev/launcher_test.py --lap-ca r858_cai_windows_chon_ban_chay_duoc --lan 1` | 0 | 1/1 |
> | `python .claude/dev/launcher_test.py --lap-ca r868_kenh_rieng_khong_doc_stdout_trinh_cai --lan 1` | 0 | 1/1 |
> | `bash -n ops/cai_cong_cu.sh` | 0 | Cú pháp đạt |
> | `python .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | 12 tệp, 0 chỗ chép doctrine |
>
> `python scratch/review_mutants.py` và `python scratch/review_mutants.py --detail` gọi harness một lần cho từng đột biến, mỗi lần chọn đúng một mục `DOT_BIEN_HOOK`. Wrapper chỉ ghi kết quả và trả rc 0. Số giết bên dưới do harness phân loại theo `TinHieuChotCa`.
>
> | Đột biến | Giết | Assertion đầu tiên đo được |
> |---|---:|---|
> | `wp1488_sh_bo_chon_luon_dich` | 1/1 | (I-win), §9 ghi (W-rong) |
> | `wp1488_sh_quyet_theo_lenh` | 1/1 | (N-nhay) |
> | `wp1488_sh_path_bo_nhanh_dich_win` | 2/2 | (N-nhay) và ca Windows riêng, đều rc 7 |
> | `wp1488_sh_dich_win_khong_doi` | 2/2 | (I-win), §9 ghi (W-rong), và ca Windows riêng |
> | `wp1488_sh_dich_win_loi_khong_dat_rc` | 1/1 | (I-win), rc 1 và tệp rỗng |
> | `wp868_sh_ham_in_stdout_thay_kenh` | 2/2 | ca hình dạng và writer muộn không tới điểm đánh dấu vì không có dòng GITHUB_PATH |
> | `wp868_sh_ghi_dich_nuot_loi` | 2/2 | ca ghi kênh lỗi (nhãn DICH) và ca hình dạng |
> | `wp1488_sh_bo_chon_ghi_thang` | 1/1 | (A) |
> | `wp1488_sh_chep_loi_khong_dat_rc` | 1/1 | (I) |
> | `wp1488_sh_chep_loi_thoat_ngay` | 1/1 | (I) |
> | `wp1488_sh_doc_kenh_rieng_truoc` | 1/1 | (L-LF) |
> | `review_accept_dich_winx` | 0/4 | Đột biến reviewer sống |
>
> | Phép đo bổ sung từ thư mục workspace | rc | Kết quả |
> |---|---:|---|
> | `python scratch/review_probes.py` | 1 | 13/14 kỳ vọng đạt, đỏ ở `bad-nul-tag` |
> | `REVIEW_R3=1 python scratch/review_probes.py N-nhay N-tab N-data N-dead` | 1 | r3 sai cả bốn như §9, r4 đạt cả bốn |
> | `REVIEW_R3=1 python scratch/review_probes.py bad-nul-tag` | 0 | script r3 trả 7, tệp đích rỗng |
> | Gọi ca r1488 hiện hành qua `python -` với `CAI_SH_DANG_DUNG` trỏ script r3 lấy bằng `git show` | 1 | `TinHieuChotCa` tại (N-nhay), khớp §9 |
> | `REVIEW_MUTANT=1 python scratch/review_probes.py bad-prefix` | 1 | đột biến riêng trả 3 thay vì 7 |
> | `python scratch/review_iwin.py` | 0 | xác nhận độc lập (I-win) |
> | `ruff check --no-cache --select F --output-format concise <launcher_test.py>` trên từng vế | 1 mỗi vế | 5 F841 trên mỗi vế, delta 0 như §9 |
> | `shellcheck <cai_cong_cu.sh>` trên từng vế | 1 mỗi vế | 1 SC1090 trên mỗi vế, delta 0 như §9 |
> | `test ! -e /tmp/.git` | 1 | Môi trường reviewer có `/tmp/.git` |
>
> ## Chưa đo
>
> Chưa tái chạy toàn bộ suite hai vế `453/453` (455 đăng ký, 2 bỏ qua), toàn bộ mutation `798/798 → 803/803` (7 không đo được mỗi vế), hoặc xác minh danh tính các ca bỏ qua và các đột biến không đo được. Delta +5 mục đột biến đối chiếu được từ diff. Phép đo này chỉ chạy lại 5 mục mới và 6 mục đổi neo, nên lời khai về toàn bộ các đột biến r1–r3 ngoài tập đó, thời gian chạy và delta hồi quy toàn suite vẫn chưa được xác nhận độc lập. Fixture trung gian trước khi có (I-win) và CI PR chưa được đo. Kiểm tra Windows dùng stub trên Linux. Log và mã probe nằm trong `scratch/`.

### Executor đo lại P2 (trước Review Rescue Checkpoint)

Cùng fixture `_wp868_chay`, công thức tự ghi kênh `<nhãn>\0\n<dir>`; chỉ đổi `ops/cai_cong_cu.sh`:

| Script | `DICH\0` | `DICH_WIN\0` |
|---|---|---|
| `8656dc0` (base) | rc 0, nhận `DICH` (base ghi `$GITHUB_PATH` trong bộ chọn nên tệp rỗng) | rc 7 (nhãn lạ) |
| `7a8823b` (r3) | rc 0, tệp = `<dir>` | rc 7 (nhãn lạ) |
| `ab83dd3` (r4) | rc 0, tệp = `<dir>` | rc 0, tệp = `W:<dir>` |

Cả ba vế đều in cảnh báo `ignored null byte`. Nghĩa là: Bash bỏ NUL khi đọc kênh là lớp có từ wp868 (base nhận `DICH\0\n…`);
r4 không tạo lớp ấy mà mở nó sang nhãn mới. Chỉ công thức tự ghi byte NUL vào kênh mới chạm tới; công thức nằm trong
`ops/cong_cu.yaml` của kho. P3 thứ hai đúng: bảng đột biến §9 đo TRƯỚC khi thêm (I-win), mà (I-win) đứng trước (W) nên
nay chết ở (I-win).
