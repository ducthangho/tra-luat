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

### Trạng thái sau lượt 2

Ngân sách Codex của lease đã hết (2/2). Executor dừng ở Review Rescue Checkpoint và chờ chủ kho quyết.
