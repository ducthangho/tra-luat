reviewed: ops/specs/wp1509-r1.md @ 1e5ffcb6bdceb348d7a3338e7e9ce1e4782c088f
spec_sha256: a8f5cec6b20cc1726d0ac03ab0c8d2b321b9b5c14d8b6097b3f40f99c8f82ff0
verdict: request_changes
reviewer: codex (cross-provider, độc lập)

Báo cáo lượt 1. Chín lớp cần sửa: 5 P1, 4 P2; không đủ điều kiện approve. Candidate tree: `195d743e1348e396becdd04771c05bb9ccda8ea9`.

Phạm vi: đặc tả và mã nền được cung cấp, không phải review mã `don_rac.py` chưa tồn tại. Không dùng mạng, `gh`, fetch hoặc push tới kho thật. Kho giả và bằng chứng nằm ngoài `repo/`, trong workspace này. Provider: `openai_codex`; họ model `openai` theo identity của phiên; model/effort thực phục vụ và phân biệt CLI/Desktop không đo được từ gói review. Không tái sử dụng ngữ cảnh Executor.

## BẢNG LỚP

| class_slug | finding IDs | biểu hiện | mức cao nhất còn mở | cách sửa chung | phép kiểm đóng lớp |
|---|---|---|---|---|---|
| lease-bia-mo-dao-nghia | F01 | H3.4 gắn True với chưa bị thay, bỏ trạng thái None | P1 | Viết bảng chân trị đúng API | Lease sống không bia mộ giữ nhánh; thay hai chiều không giữ vì lease cũ; một chiều không đo được |
| hop-dong-tai-su-dung-lease-thieu | F02 | Phụ thuộc PyYAML; origin cố định; phạm vi ref; cấu trúc wrapper | P2 | Chốt hợp đồng adapter, dependency và miền ref trước khi đóng băng | Chạy bare với remote khác origin, runtime chuẩn, lease chỉ trên tag; đối chiếu write set |
| packet-chua-duoc-chung-minh | F03 | Tên nhánh thay bằng chứng thuộc packet; X chỉ merged; may thiếu phạm vi packet | P1 | Dùng một quan hệ packet–PR–ref đã xác minh và chứng cứ land | Ca ngoài packet, fork trùng tên, PR land sai packet/nhánh đích, hai packet trên máy |
| d7-tu-noi-dieu-kien-giu | F04 | Ngoại lệ agent-, hạ tuổi dưới 24 giờ, tệp giữ mất thành danh sách rỗng | P1 | Giữ điều kiện D7 và phân biệt không có cấu hình với không đọc được cấu hình | Ca app agent- chưa lưu trữ, tuổi 1 giờ với ngưỡng 0, đường dẫn --giu sai |
| ban-sao-luu-khong-phuc-hoi-du | F05 | Mất thao tác xoá tệp; bỏ gói >30 MB; chưa bảo đảm bản sao sống ngoài đích xoá | P1 | Bản sao đầy đủ, kiểm được và tồn tại độc lập là tiền điều kiện gỡ | Phục hồi so byte/trạng thái; quá hạn mức, lỗi ghi, trùng tên, backup lồng trong đích đều giữ |
| neo-commit-bi-xoa-cung-clone | F06 | Tag chỉ cục bộ và remote-tracking stale được tính là bản lưu an toàn | P1 | Chứng minh ref/object còn truy xuất được sau khi gỡ | Commit chỉ ở tag cục bộ hoặc remote-tracking stale không cho xoá clone |
| chay-kho-khong-co-bien-ghi-ro | F07 | H1 ghi/prune gương; N6 không quan sát clone, nhánh local, backup hoặc comment | P2 | Chốt ngoại lệ cache và danh sách tác động; đo toàn bộ trạng thái liên quan | Đột biến ghi ở từng nhánh thao tác đều đỏ, không chỉ ba phép liệt kê N6 |
| nghiem-thu-khong-phu-tung-chot | F08 | N2 tính theo H ghép nhiều chốt; chưa có ma trận ca đích; H14/H15 thiếu oracle cụ thể | P2 | Ánh xạ từng điều kiện độc lập và đầu ra tới ca/đột biến | Bỏ riêng từng chốt phải giết đúng đột biến bằng TinHieuChotCa |
| mau-ci-thieu-phan-chung | F09 | MOI chỉ đòi mẫu dương; N4 chỉ thử xoá đăng ký; N1/N5 không thử output sai | P2 | Kiểm mẫu thật qua chính consumer CI với output đối chứng | Chấp nhận đủ dương; bác mutant thiếu/0, thiếu dòng, hậu tố sai, đỏ kèm xanh |

Nguồn của mọi lớp: lượt 1 trên OID ở đầu báo cáo. Các biểu hiện cùng cơ chế đã được quét qua H1–H15 và N1–N9. Số biểu hiện ghi theo nội dung từng dòng bảng, không đồng nhất với số lớp hay số finding.

## BẢNG ĐO

| việc | lệnh/phép đo | kết quả |
|---|---|---|
| HEAD | `git -C repo rev-parse HEAD` | Khớp OID được giao |
| Băm bản review | `Get-FileHash SPEC.md -Algorithm SHA256` | Khớp băm được giao |
| Bản authoritative và bản local | `python -B -X utf8 review_probe.py`: băm bytes của `git show HEAD:ops/specs/wp1509-r1.md` và SPEC.md | Cùng `a8f5cec6…ff0`; nguồn A tại `26bc9b9f083e60704f607f374efeb3f7bdeb0843` có băm `d8320e6195658d109cc26fcaa7d28425590d458f5b91cf09f68416d60e4c7b71` |
| Bảng chân trị thực | Probe `tombstones` | CÒN_HẠN; không bia mộ → null/None; một chiều → false; hai chiều → true |
| Bare/caller | Probe `bare_scan`, `non_origin_default`, `non_origin_explicit_check_false` | Đọc được lease và wrapper đúng trên bare với loader JSON fixture; đổi origin thành upstream làm default call báo Chan; tắt đối chiếu nội bộ sau preflight thì đọc được |
| Lease chỉ ở tag | `python -B -X utf8 review_tag_probe.py` | rc0; blob lease vẫn đọc được qua refs/tags/tag-only-lease, scanner trả 0 lease. Lần đầu chưa cô lập vì tracking ref stale còn giữ lease; đã bỏ đúng ref ấy trong kho giả và giữ cả hai kết quả trong JSON |
| Stdlib thực | Probe subprocess `python -S -B -c …` | rc1, Chan thiếu PyYAML; không cài dependency hoặc gọi mạng |
| Bản vá deletion | Probe Git thật `deleted_file_patch` | status `D tracked.txt`; lệnh H10 cho 0 byte, diff đầy đủ cho 144 byte. Chưa chạy restore round-trip sản phẩm vì chưa có sản phẩm |
| Tệp quá hạn mức | Probe `oversize_untracked` | 32.505.856 byte (31 MiB), diff 0 byte, H10 không yêu cầu tar; không thực hiện gỡ |
| Neo tag cục bộ | Probe Git thật `local_only_tag` | H9 count=0; bỏ loại trừ tag thì count=1; mirror không có object commit ấy; không thực hiện gỡ |
| Dispatch thực qua seam | Probe `registry_dispatch`: gọi chính `chay_moi` với runner ghi nhận lời gọi | rc0; runner được gọi cho ops/don_rac_test.py; test mới ngoài NHE/MAU_DAY_DU/DA_NOI. Đây là seam test, không phải chạy suite mới |
| Phản chứng mẫu dương yếu | Probe `registry_weak_positive`: chính `bang_chung_xanh` | Cả good, partial_mutants 2/3, zero_mutants 0/0, trailing_red đều true. Mẫu là phản ví dụ được spec cho phép, không phải mẫu implementation chưa tồn tại |
| Numstat hiện tại | `git diff --numstat 5259239d763c9ffc1677f033bd9a9cf23ede9299..HEAD` | `143 0 ops/specs/wp1509-r1.md`; mới có đặc tả. Chưa đo N8 cho implementation năm tệp |
| Checkout chỉ đọc | So `snapshot-before.json` / `snapshot-after.json` | HEAD/tree, index hash, diff HEAD, status có untracked/ignored và nội dung 8 tệp được băm đều bằng nhau; status rỗng, changed_paths=[] |
| Chữ ký lease | Đọc `repo/ops/lease_publish.py:713`, `:783`, `:806`, `:2623` | Cả ba hàm tồn tại; `_bia_mo_doi_xung` trả `None`, `False`, `True`; `True` là ĐÃ bị thay |
| Luật nguồn | `git -C repo show wp1507-nhap:ops/specs/wp1507-r1.md` và bản nháp ADR-0068 cùng ref | Đã đọc D1–D12; đặc biệt D3/D4/D6/D7/D9; không coi ADR nháp là luật đã land |
| Phụ thuộc runtime | Gọi `_quet_lease_toan_kho` trên bare fixture, Python hiện có | FAILED do `Chan: KHÔNG_XÁC_ĐỊNH: thiếu PyYAML`; đúng nhánh mã :745–747, chưa phải lỗi dữ liệu lease |
| Registry | Đọc `ci_dang_ky_test.py:38`, `:77`, `:672`, `:711`, `:795`, `:808`, `:891`, `:1305`, `:2979` | Thêm MOI đủ để dispatch test mới; DANG_KY là MOI ∪ DA_NOI; không cần thêm vào DA_NOI, NHE hay MAU_DAY_DU |
| Workflow | Đọc `repo/.github/workflows/ci.yml:1039`, `:1046`, `:1104` | Job 150 phút; một suite 5.400 giây; bước registry bỏ qua khi duong_nhanh. Diff có mã mới của B không chỉ gồm hồ sơ nên không đi đường tắt đó |
| Bộ chọn nhẹ | `ke_hoach` :891–902; caller :2980–2983 | Chỉ các bộ trong NHE có chế độ nhẹ; bộ mới mặc định day_du. Không có nghĩa vụ thêm MAU_DAY_DU cho một bộ ngoài NHE |
| Consumer mẫu | `bang_chung_xanh` :711–715, `chay_moi` :1344–1350 | Consumer chỉ tự so số khi regex có đúng hai nhóm; không tự biết cặp số nào là CA hay DOT BIEN. Mẫu mới phải tự chứng minh cả hai |
| L2 / write set | Đối chiếu §3 với §4 và API hiện hữu | Ba mục tiêu có đường dẫn; không cần sửa workflow để dispatch. Nhưng yêu cầu stdlib/all-ref của F02 chưa thực hiện được nguyên văn bằng helper hiện có |
| E4/E5 | ADR-0067 :29–43; SPEC :13, :120, :129, :141 | Không tự phân loại B thành E4/E5 chỉ vì nó viết công cụ có --ap-dung. Phạm vi được khai chỉ thi công/test giả/dry-run, không sửa authority gate. Kết luận này đòi sửa ranh giới dry-run F07 và không nới luật nguồn như F04 |
| nang_tran | ADR-0053 :34–46; SPEC :17–25 | Có đủ bốn trường; can_cu nói rõ là ước tính và lý do không tách. Chưa có numstat implementation theo yêu cầu ADR; N8 phải bổ sung số đo thật trước review mã/công bố, chép khối vào lease. Không coi 1.650 là số đã đo |

Các probe chính chạy ngày 24-11-2026, từ 15:55Z đến khoảng 15:56:36Z. Lệnh `python -B -X utf8 review_probe.py` kết thúc rc0. Bằng chứng: [script probe](review_probe.py), [kết quả JSON](review-evidence/probe-results.json), [snapshot trước](review-evidence/snapshot-before.json), [snapshot sau](review-evidence/snapshot-after.json), [nguồn D1–D12](review-evidence/wp1507-r1-source.md). Mỗi kết luận có giới hạn riêng trong bảng; rc0 của probe không phải N1/N4/N5 đạt.

Về thẩm quyền: nếu sửa F04 để trở về D7 thì không cần tự coi việc viết công cụ là E4/E5. Nếu giữ các ngoại lệ trái D7 hoặc đổi luật để xử F06 thì phải giải quyết quyết định nguồn/E3, không được dùng câu “không chạm E3–E5” ở dòng 141 để tự đóng băng revision ấy.

### Đối chiếu H với luật nguồn

| H | luật | kết quả review |
|---|---|---|
| H1 | D4.4 | So tập tên là đúng; phải giải quyết miền ref/caller F02 và ghi trong dry-run F07 |
| H2 | D4.2–3 | Đọc lỗi chặn toàn cục và phân trang là phù hợp; cần ghi rõ dùng chung preflight cho pr |
| H3 | D4.1–6 | Merge ancestry, nhánh mặc định/luu-tru, PR head/base, CAS và giữ khi không đo được đều có; H3.4 sai bảng chân trị F01 |
| H4 | D3a | Có lease và prefix ops/wpN-; nhận diện PR bằng tên chưa đủ F03 |
| H5 | D4.5, D9 | Readback và rc4 phù hợp; nhánh còn cũng có thể do lỗi quyền/hạ tầng, không nên mặc định mọi lỗi là CAS |
| H6 | D3b, D6 | Thiếu chứng minh land của đúng packet F03 |
| H7 | D6 | Chốt ancestry phù hợp. Fork hoặc SHA lệch được giữ theo hướng thận trọng; phải khai phần D6 chưa đo được thay vì nói đã đóng mọi PR đủ điều kiện |
| H8 | D3c, D7 | Có worktree/clone; thiếu chế độ giới hạn theo packet F03 |
| H9 | D7 | Điều kiện bảo vệ bị nới F04; neo chỉ cục bộ không bảo toàn commit F06 |
| H10 | D7 | Bản vá không bảo toàn đủ công việc F05 |
| H11 | D7 | Có ancestry, worktree guard và CAS; cần ca riêng cho giữ theo tên/SHA/đường dẫn, lỗi đo và dry-run |
| H12 | D7 | Có marker và issue đóng, giữ khi API lỗi; chưa chốt kiểu marker/packet_issue, kho dùng truy vấn issue, giới hạn phạm vi packet |
| H13 | D7 | Có mốc 90 ngày; cần thống nhất bố cục UTC với H10 và cách biết thư mục thực sự do công cụ tạo |
| H14 | D9 | Các nhóm dữ liệu chính đủ; schema item, trạng thái dự kiến và mã D7.* chưa đủ oracle, F08 |
| H15 | D4.6, D9 | Có bốn mã thoát; cần ca riêng mỗi mã và quy tắc lỗi từng mục so với toàn cục, F08 |

### Đối chiếu N và khả năng làm đỏ

| N | phép làm đỏ / giới hạn |
|---|---|
| N1 | Thiếu/sai dòng, lệch tử/mẫu hoặc rc khác 0 phải đỏ. Chưa khóa số dương và mẫu consumer, F09 |
| N2 | Có ý định dùng TinHieuChotCa và đột biến đúng ca đích; chưa phủ từng chốt trong H ghép, F08 |
| N3 | Có tình huống cạnh tranh và oracle rõ: nhánh còn, loi, rc4. Đạt ở cấp thiết kế |
| N4 | Xoá dòng đăng ký là đột biến có răng cho tính đầy đủ của sổ; không kiểm chất lượng regex, F09 |
| N5 | Job thiếu output test mới/không chạy phải đỏ. Chưa đo CI; mẫu bốn dòng cần được kiểm như N1, F09 |
| N6 | Ba snapshot đổi làm đỏ nhưng không chứng minh mọi lệnh không ghi, F07 |
| N7 | Lỗi Ruff F trên hai tệp làm đỏ. Chưa có hai tệp; chưa chạy lint sản phẩm |
| N8 | Ngoài năm đường dẫn hoặc vượt 1.800 dòng thêm làm đỏ. Đây là số đo diff implementation tương lai, không thay bằng ước tính |
| N9 | Một P0/P1/P2 còn mở hoặc reviewed SHA lệch làm đỏ. Lượt này chưa đạt |

## FINDINGS

### F01 lease-bia-mo-dao-nghia [P1] H3.4 đảo nghĩa bia mộ hai chiều và bỏ trạng thái lease chưa bị thay

- vị trí: `SPEC.md:49`; `repo/ops/lease_publish.py:806`; `repo/ops/lease_publish.py:2631`.
- phép đo / lập luận: API trả `None` khi không có bia mộ, `True` khi có đủ liên kết cũ–mới và mới–cũ, `False` khi có bia mộ không xác nhận được. H3 lại mô tả “chưa bị thay hai chiều (`_bia_mo_doi_xung` là `True`)”. Hiện thực theo giá trị này có thể bỏ qua lease còn hạn không có bia mộ và xoá nhánh đang được giữ. Caller hiện có dùng `da_chet = bia_mo is True`, rồi giữ khi còn hạn và `not da_chet`.
- đề xuất sửa: Chốt bảng ba trạng thái trong H3; lấy đúng `muc['lease']` từ kết quả quét và truyền cả danh sách wrapper vào `_bia_mo_doi_xung`. Thêm ca/đột biến riêng cho lease còn hạn không bia mộ, bia mộ hai chiều, một chiều và lỗi hạn.

### F02 hop-dong-tai-su-dung-lease-thieu [P2] Hợp đồng helper không đáp ứng nguyên văn stdlib, remote tuỳ chọn và mọi ref

- vị trí: `SPEC.md:37`, `SPEC.md:42`, `SPEC.md:48`, `SPEC.md:51`, `SPEC.md:85`; `repo/ops/lease_publish.py:531`, `:543`, `:713`, `:745`, `:772`.
- phép đo / lập luận: (a) `_quet_lease_toan_kho` import PyYAML, không phải thư viện chuẩn; chạy trực tiếp đã thất bại đúng chốt thiếu PyYAML. (b) Mặc định `doi_chieu_ref=True` gọi `ls-remote --heads origin`, không nhận `--remote`; phép so trong helper chỉ tìm nhánh thiếu, không kiểm tập bằng nhau như H1. Caller phải so đúng nguồn ở H1 rồi dùng `doi_chieu_ref=False`, hoặc thiết lập origin đúng nguồn. (c) `_cac_ref_cuc_bo` chỉ liệt kê `refs/heads` và `refs/remotes`, không quét tag/ref khác. Một lease chỉ trên tag vẫn là lease “trên mọi ref” theo câu chữ H3/D4 nhưng bị bỏ qua. (d) Kết quả là wrapper `{lease, blob, path, ref}`; bộ phân loại nhận dict bên trong, hàm bia mộ nhận dict cùng danh sách wrapper, không phải danh sách lease phẳng. Không phải các hàm không tồn tại hoặc không dùng được trên bare; vấn đề là hợp đồng chưa chốt đúng.
- đề xuất sửa: Khai rõ dependency PyYAML và cách cung cấp, hoặc revision yêu cầu stdlib. Chốt adapter và xử lý `Chan(12)` thành kết quả giữ/rc3 thích hợp. Chốt miền “mọi ref” với A: nếu gồm tag/ref khác, helper và cách fetch phải được mở rộng, kèm mở write set/revision; không tự viết reader thứ hai. Nếu ý nguồn chỉ là mọi branch ref thì sửa rõ ở cả nguồn và đặc tả theo đúng quyền. Các thay đổi này phải được giải quyết trước thi công, không để executor vượt write set.

### F03 packet-chua-duoc-chung-minh [P1] Có thể đóng PR khi chưa chứng minh đúng packet đã land

- vị trí: `SPEC.md:51`, `SPEC.md:56`, `SPEC.md:62`, `SPEC.md:71`, `SPEC.md:73`; `repo/CONTEXT.md:43` và `repo/CONTEXT.md:45`.
- phép đo / lập luận: H4 dùng ranh giới tên `wpN` thay cho quan hệ “PR của packet” của D3/D6. Hai PR ở hai head repo khác nhau có cùng `head.ref` đều có thể khớp; H6 không có guard cùng kho như H7. Một PR đã được packet khác sử dụng/đổi liên kết nhưng vẫn mang tên wpN cũng khớp. Chiều ngược lại, PR thực thuộc N với tên tuỳ ý và không có lease khả dụng không được nhận diện. Riêng `--land-pr X` chỉ cần `merged=true`: X có thể thuộc packet khác hoặc mới merge vào integration branch. `merged` không đồng nghĩa `landed` theo từ vựng kho; lúc đó mọi PR N được đóng sớm và ghi lý do sai. Cuối cùng D3c đòi phạm vi worktree/clone/local branch của packet, nhưng H8–H12 chỉ mô tả quét toàn máy; không có nghĩa của `may --packet N`.
- đề xuất sửa: Chốt nguồn bằng chứng quan hệ packet–PR–head repo/ref và cách xử lý mâu thuẫn/không đo được; tên chỉ là nguồn tìm ứng viên, không đủ quyền đóng. X phải được chứng minh là kết quả đã land của N vào canonical theo contract nguồn. Dùng cùng quan hệ đó để giới hạn `may --packet`, hoặc ghi rõ phần D3c được giao nơi khác và điều chỉnh mục tiêu. Ca đóng lớp gồm PR đúng packet tên không theo mẫu, fork trùng tên, wpN0, X sai packet, X chỉ merged vào integration, hai packet có dữ liệu cùng máy.

### F04 d7-tu-noi-dieu-kien-giu [P1] H9 tự thêm các đường vượt hàng rào D7

- vị trí: `SPEC.md:64`, `SPEC.md:65`, `SPEC.md:67`; D7 trong `review-evidence/wp1507-r1-source.md`.
- phép đo / lập luận: D7 giữ phiên app Claude chưa lưu trữ tại `.claude/worktrees/<tên phiên>`, không miễn tên `agent-*`. H9 miễn cả lớp tên này mà không đo trạng thái phiên, nên phiên chưa lưu trữ có tên agent-x có thể bị gỡ. D7 đặt 24 giờ; `--tuoi-gio` chỉ có mặc định, không có cận dưới: giá trị 0/1 có thể cho xoá thư mục vừa đổi. H9 còn biến tệp giữ vắng thành danh sách rỗng, không phân biệt không truyền `--giu` với đã truyền nhầm đường dẫn/tệp từng tồn tại nhưng bị mất. Trường hợp sau là mất bằng chứng bảo vệ, không phải bằng chứng rằng không có mục giữ. Đây là ba sự nới điều kiện, không chỉ lựa chọn cách hiện thực.
- đề xuất sửa: Bảo vệ toàn bộ miền app theo luật nguồn cho tới khi có phép đo archive đáng tin; không suy quyền xoá từ prefix. Khóa mốc tối thiểu 24 giờ hoặc revision luật nguồn được chủ kho chấp nhận. Phân biệt không cấu hình giữ với cấu hình không đọc/không parse được; trường hợp sau phải giữ và ghi không đo được. Đột biến phải lần lượt bỏ từng guard, không dùng một ca H9 đại diện.

### F05 ban-sao-luu-khong-phuc-hoi-du [P1] H10 cho phép gỡ khi bản vá không chứa đủ công việc chưa commit

- vị trí: `SPEC.md:68`, `SPEC.md:69`, `SPEC.md:70`, `SPEC.md:75`.
- phép đo / lập luận: `--diff-filter=d` loại bỏ các deletion. Khi thay đổi duy nhất là xoá tracked.txt, `status.txt` ghi việc xoá nhưng `diff.patch` không có thao tác để phục hồi đúng trạng thái làm việc; apply bản vá vào HEAD sẽ làm tệp xuất hiện lại. Với tệp chưa theo dõi 31 MiB, diff không chứa dữ liệu ấy và H10 không tạo tar, nhưng câu tiếp theo vẫn cho gỡ. Danh sách tên không phục hồi được nội dung. N2 “bỏ lưu bản vá” không bắt được bản vá tồn tại nhưng thiếu dữ liệu. Cùng bất biến phục hồi còn thiếu ở vị trí lưu: không cấm `--sao-luu` nằm trong clone sắp xoá; nhiều `--goc-clone` có thư mục cùng tên có thể cùng đi tới `<UTC>/<tên>`. Không có tiền điều kiện xác minh bản sao đã ghi thành công, duy nhất và sống sau khi gỡ.
- đề xuất sửa: Bỏ bộ lọc loại deletion; đòi bản sao phục hồi đủ trạng thái cần giữ trước mọi remove. Khi dữ liệu vượt hạn mức hoặc ghi/đọc lại bản sao thất bại, giữ nguyên đích và ghi lý do; nếu muốn bỏ dữ liệu >30 MB phải giải quyết lại quyết định nguồn, không suy từ việc “không tạo gói”. Quy định backup nằm ngoài mọi đích gỡ, ID tránh trùng và cách xác minh. Kiểm bằng khôi phục vào cây mới rồi so nội dung và trạng thái, với deletion, binary, untracked lớn, lỗi ghi, cùng basename và backup lồng trong đích. Không cần xoá dữ liệu thật để tái hiện.

### F06 neo-commit-bi-xoa-cung-clone [P1] H9 coi ref bên trong clone sắp xoá là bằng chứng commit đã an toàn

- vị trí: `SPEC.md:65`, `SPEC.md:66`, `SPEC.md:70`; D7 nguồn.
- phép đo / lập luận: Dựng clone có HEAD chứa commit duy nhất chưa push và một tag cục bộ trỏ HEAD. `git rev-list --count HEAD --not --remotes --tags` bằng 0 vì chính tag trong clone ấy. H9 thông qua, H10 xoá toàn clone cùng `.git`, tag và object duy nhất. Biên nhận SHA/đường dẫn không phục hồi object. Tương tự, remote-tracking ref là cache cục bộ: nếu remote đã mất ref/object thì cache ấy không chứng minh dữ liệu còn ở đâu sau xoá. Với linked worktree, common object database có thể sống ngoài đích; không được áp cùng kết luận đó cho standalone clone.
- đề xuất sửa: Phân biệt worktree và clone; yêu cầu neo/object còn truy xuất được bên ngoài phạm vi xoá, hoặc tạo/kiểm bundle cứu hộ đầy đủ trước khi gỡ. Giữ khi không chứng minh được. Đây là lỗ an toàn được kế thừa từ câu D7 “ref remote hay tag”, không phải riêng B dịch sai: sửa phải đi qua A/revision có thẩm quyền, ghi rõ xung đột với quyết định nguồn theo E3 nếu cần đổi quyết định, rồi cập nhật B. Không âm thầm coi tag cục bộ là tag trên máy chủ.

### F07 chay-kho-khong-co-bien-ghi-ro [P2] Lời hứa chạy khô và phép đo N6 không bao cùng tập tác động

- vị trí: `SPEC.md:39`, `SPEC.md:42`, `SPEC.md:68`, `SPEC.md:71`, `SPEC.md:73`, `SPEC.md:75`, `SPEC.md:112`.
- phép đo / lập luận: “chỉ ghi biên nhận” ở dòng 39 mâu thuẫn với H1 luôn dựng/cập nhật bare mirror và prune ref trong nó. Nếu gương được coi là ngoại lệ cache thì phải nói rõ. Ngay cả khi cho phép cache, N6 chỉ so remote heads, PR mở và worktree list: xoá một standalone clone H10, nhánh cục bộ không gắn worktree H11, thư mục marker H12, bản vá cũ H13, hoặc thêm comment rồi không đóng PR H6 đều có thể giữ nguyên ba phép đo. `--giu`/`--sao-luu` và file người dùng cũng không được quan sát. Vì vậy lời khai “dry-run không ghi” có thể xanh dù dữ liệu trên máy đổi.
- đề xuất sửa: Chốt write allowlist của dry-run: chỉ receipt, hay thêm mirror riêng do công cụ quản lý; không prune một gương người dùng chưa được xác minh ownership. Mọi mutation phải qua chung chế độ áp dụng, kể cả comment, prune, backup và retention. Bổ sung snapshot nội dung/ref của clone, nhánh local, thư mục thường, backup và trạng thái PR liên quan; ca đột biến riêng từng đường. N6 phải ghi giới hạn snapshot đầu/cuối như protocol §8.2, không tuyên bố chứng minh mọi ghi tạm rồi hoàn nguyên.

### F08 nghiem-thu-khong-phu-tung-chot [P2] Một ca và một đột biến mỗi H không kiểm được các H chứa nhiều điều kiện độc lập

- vị trí: `SPEC.md:46`, `SPEC.md:64`, `SPEC.md:68`, `SPEC.md:78`, `SPEC.md:81`, `SPEC.md:104`.
- phép đo / lập luận: N2 có thể được đáp ứng cho H3 bằng ca dương/âm và các mutant bắt buộc về PR/lease/CAS, trong khi H3.1 ancestry và H3.2 nhánh mặc định/luu-tru không có mutant nào. H9 có thể chỉ thử app/tuổi mà bỏ commit chưa an toàn, danh sách giữ và lỗi đo. H10 có thể chỉ thử sự hiện diện của patch, không phục hồi deletion/binary/untracked. H11 có thể thử worktree mà bỏ ancestry/keep/CAS local. H15 chỉ cần một cặp ca 0/4 thì mã 2/3 chưa được canh. H14 “cùng các mục ở dạng sẽ làm” chưa xác định kiểu item/trạng thái dự kiến; D7.* chưa có danh mục, nên hai tác giả có thể tạo JSON khác nhau mà cùng tự viết test xanh. H10 `<UTC>` và H13 tên ngày cũng chưa có định dạng chung/ownership oracle.
- đề xuất sửa: Thêm ma trận chốt → fixture dương/âm → ca đích → đột biến → oracle, phủ từng tiểu điều kiện và mỗi mã thoát. Chốt schema biên nhận tối thiểu, dự kiến so với đã thực hiện, nhận diện backup do công cụ tạo và phân loại lỗi theo mục/toàn cục. Không cần đóng băng tên mọi hàm, nhưng phải đóng băng tính chất nào khiến test đỏ. Test giả gh phải duy trì trạng thái repo/PR và cho thay đổi trạng thái, không chỉ trả kịch bản sẵn.

### F09 mau-ci-thieu-phan-chung [P2] N4 chứng minh test có trong sổ nhưng không chứng minh CI bác bằng chứng sai

- vị trí: `SPEC.md:87`, `SPEC.md:98`, `SPEC.md:103`, `SPEC.md:110`, `SPEC.md:111`; `repo/.claude/dev/ci_dang_ky_test.py:711`, `:1344`.
- phép đo / lập luận: Đặc tả chỉ yêu cầu “mẫu bằng chứng dương”; N4 chỉ xoá dòng đăng ký. `bang_chung_xanh` không tự kiểm mọi cặp số: nó so hai nhóm nếu và chỉ nếu regex có đúng hai nhóm, còn regex có 0 hoặc hơn 2 nhóm chỉ cần match. Một mẫu bắt CA N/N nhưng để DOT BIEN bằng hai `\d+` có thể nhận `DOT BIEN: 2/3` hoặc `0/0`, và mẫu không neo toàn lời khai có thể nhận output vừa có DAT vừa có DO. `MAU_DAY_DU` không bù cho bộ mới ngoài NHE. N2 tự kiểm phân hạng của harness không thay phép kiểm regex ở tầng consumer; N5 chỉ có mặt bốn dòng cũng không thay phép âm. Mẫu hiện hữu của land_evidence_nguon_test đã dùng số dương/backreference/neo và bác DO, là ví dụ tái sử dụng được nhưng spec chưa buộc kiểm mẫu mới.
- đề xuất sửa: Đưa phản chứng vào `don_rac_test.py` hoặc phần tự kiểm registry trong write set: gọi chính `bang_chung_xanh`/`chay_moi` với pattern đăng ký thật. Dương đúng; âm lệch CA, lệch mutant, 0 mutant, thiếu từng dòng, sai hậu tố, DO kèm DAT, output cũ/chỉ tổng. Chốt phạm vi khớp bốn dòng liền nhau; các vế L6 về ngắt đoạn/chữ-số/cổng không áp dụng cho giao thức stdout cố định thì ghi lý do, không để trống. Xoá đăng ký vẫn giữ là phép kiểm riêng cho N4.

## chua_do_duoc

- Chưa có `ops/don_rac.py` hoặc bộ test để nghiệm thu hành vi sản phẩm. Phép đo tiếp theo chỉ kiểm các giả định của đặc tả trên mã hiện hữu và kho giả.
- Không xác minh GitHub, Mission approval, CI hay thao tác trên kho thật vì phạm vi review cấm mạng.
- Approval nâng trần trong AskUserQuestion, Mission `plan_hash` đầy đủ, `mcr-1506-1` và trạng thái land của A chỉ có lời dẫn trong đặc tả/bản nháp; không suy chúng đã được xác minh từ việc đọc các lời dẫn.
- Khối nang_tran đủ bốn trường nhưng chưa có mã để đo quy mô cuối cùng. Cần numstat thật, lease thực và kiểm lại mốc ADR trước công bố; không yêu cầu lập trình phần B chỉ để review đặc tả này.
- Chưa chạy N1/N4 toàn suite/N5/N6/N7 của sản phẩm. Chạy registry toàn suite không cần thiết để chứng minh dispatch, và môi trường thiếu PyYAML. Các probe có shim JSON chỉ đo hợp đồng scanner/caller trên fixture, không chứng minh parser YAML hoặc CI thật.
- Không chạy thao tác phá huỷ trên dữ liệu thật; không chứng minh thời gian chạy trên Linux/Windows runner, quyền GITHUB_TOKEN, xử lý khoá tệp, race PR thay head sau phép đo, hoặc sandbox ngăn mọi đường ghi. Các giới hạn ấy không được tính là pass.
- Snapshot băm nội dung tám tệp liên quan và trạng thái Git toàn checkout, không băm mọi byte của mọi tệp ignored. Lượt thử snapshot toàn bộ được dừng trước các fixture vì quá chậm. Không khẳng định chưa từng có ghi rồi hoàn nguyên giữa hai mốc; không sửa checkout để chạy probe.
- Schema marker/receipt, tham số bắt buộc mỗi subcommand, H1/H2 có áp cho lệnh pr hay không, chuẩn hoá đường dẫn Windows, symlink/junction và backup ownership cần được chốt khi sửa F03/F05/F07/F08; không được tự suy “không đọc được” thành “không có”.
