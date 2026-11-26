tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

# DON-REF-DO-TAG-LUU-TRU r1: `ops-don-ref` đo tag `luu-tru/*` và đóng nhánh mặc định không đo (đặc tả đóng băng)

## packet_id · packet_issue
- `packet_id`: `DON-REF-DO-TAG-LUU-TRU`, revision 1, generation 1.
- `packet_issue`: chưa có. Mở sau khi chủ kho duyệt băm tệp này; số Issue không nằm trong tệp để băm không đổi.

## nguon_cap_viec
Không có dòng kế hoạch. Việc sinh từ một lần dọn ref có thật, ngày 25-11-2026, của packet #1475 (đã land, PR #1498):
- run `45677461580` tạo tag `luu-tru/wp1475-r1-leases` → `c46e26908cd38ab5778cfa6fa19ceead9fe3baa8`;
- run `45677566316` (thử khô) DỪNG ở `ops/wp1475-r1-g1-lease` (cùng SHA ấy): *"còn 10 commit CHƯA có trong master … Merge
  vào master trước, hoặc tạo tag giữ chúng"*. Tag giữ đúng SHA ấy đã có từ run trước, nhưng code không kiểm tag;
- run `45677710837` xoá thật `coord/wp1475-r1-g2-staging` và `coord/wp1475-r1-g3-staging` mà không có phép đo tổ tiên
  hay tag nào: `coord/` không có nhánh nào trong `case` của bước chốt.

Chủ kho chọn bảy quyết định Q1–Q7 theo khuyến nghị ngày 25-11-2026. Nội dung của chúng nằm ở mục `muc_tieu` dưới đây.

## review_class
`sensitive`. Lý do: tệp chạm là `.github/workflows/`, workflow cấp lại quyền xoá ref mà sandbox cố ý không cho
(`docs/PROTOCOL_DA_PHIEN.md` §8.3).

## pham_vi_e
**Chạm E5.** `docs/adr/0067-danh-sach-dong-va-uy-quyen-thuong-truc.md` định nghĩa E4 theo *"luật của
`.github/workflows/ops-don-ref.yml`"*. Packet này sửa chính luật ấy, tức đổi ranh giới thẩm quyền xoá ref. Vì vậy chủ kho
phải duyệt băm của tệp này, và chủ kho audit packet; review độc lập approve thôi thì không đủ.
Không chạm E4: packet không xoá hay tạo ref nào. Mọi lần chạy workflow thật để kiểm sau land là việc riêng, theo luật mới.

## write_set
- `.github/workflows/ops-don-ref.yml`
- `ops/don_ref_chot_test.sh`
- `CLAUDE.md`
- `ops/specs/don-ref-do-tag-luu-tru-r1.md`
- `ops/leases/don-ref-do-tag-luu-tru-r1-g1-claude.yaml`
- `ops/acceptance/don-ref-do-tag-luu-tru/r1/VERDICT.md`

## ngoai_pham_vi
- Luật xoá **TAG** và luật **tạo tag**: không đổi. Tag dưới `luu-tru/` và dưới tên vùng làm việc vẫn cấm xoá. Tag tên khác
  vẫn xoá được như hiện nay. Packet chỉ đổi luật xoá **nhánh**.
- Bước LÀM (xoá bằng `--force-with-lease=<ref>:<sha ghim>`) và chốt GHIM SHA: không đổi.
- Cấm nhánh mặc định và danh sách ký tự/dạng tên: không đổi.
- Nhánh `ops/wp1475-r1-g1-lease` còn trên GitHub: packet không xoá nó. Xoá sau land là một lần chạy workflow riêng.
- `.claude/dev/launcher.py`, `docs/GOI_AGENT_DA_NEN.md`, `ops/reviews/README.md`: không sửa. Tệp README ấy nói `luu-tru/*`
  là ref bền; luật mới làm điều đó đúng hơn, không làm nó sai.

## muc_tieu
Mỗi mục chiếu vào một đường dẫn trong `write_set`.

1. **Một phép đo "có tag lưu trữ giữ"** (`.github/workflows/ops-don-ref.yml`). Phép đo chỉ tính tag có tên bắt đầu bằng
   `luu-tru/`. Nó so `commit.sha` đã dereference từ `repos/<kho>/tags` (phân trang đủ) với SHA đầu nhánh vừa đọc.
   Có **ba** kết quả: `giữ` · `không giữ` · `KHÔNG ĐO ĐƯỢC`. Kết quả thứ ba làm bước chốt DỪNG (exit 2).
   Gặp lỗi `gh` ở bất kỳ trang nào thì trả `KHÔNG ĐO ĐƯỢC`, không trả `không giữ`.
2. **Nhánh `luu-tru/**`** (cùng tệp): đổi phép "tag BẤT KỲ giữ" sang phép đo của mục 1 (Q2).
3. **Nhánh vùng làm việc** `ops|claude|codex|agent|mission|dispatcher/**` (cùng tệp): cho xoá khi `behind_by = 0` **hoặc**
   mục 1 trả `giữ` (Q1). `behind_by` khác 0 mà mục 1 trả `không giữ` thì DỪNG. Một trong hai phép đo trả
   `KHÔNG ĐO ĐƯỢC` mà phép kia không cho qua thì cũng DỪNG.
4. **Mọi nhánh khác** (cùng tệp): thêm nhánh `*)` vào `case` của bước chốt. Nhánh này áp đúng luật của mục 3, kể cả
   `coord/`, `ccr-*`, `do-ci/` và mọi tiền tố chưa có tên (Q3). Không còn đường nào xoá nhánh mà không đo.
   Với `xoa-tag` trên tên ngoài các vùng được bảo vệ, nhánh `*)` giữ đúng hành vi cũ (xem `ngoai_pham_vi`).
5. **Thông báo DỪNG** (cùng tệp): câu DỪNG của mục 3 và mục 4 nói đúng thứ code chấp nhận (Q4). Phải nêu đủ hai đường:
   `merge vào <nhánh mặc định>` và `tạo tag luu-tru/* trỏ đúng <sha40 đầu nhánh>`. Bỏ câu "hoặc tạo tag giữ chúng" không
   nói loại tag.
6. **Phản chứng** (`ops/don_ref_chot_test.sh`). Đồ giả `gh` phải trả cả **tên** tag lẫn SHA để phép lọc `luu-tru/` có thứ
   để đo. Đồ giả giữ trạng thái, đúng luật đã có của tệp: không diễn kịch bản. Ca `"ref thường + XOA thì QUA"` (dòng 120
   trên `d0868db`) hiện **khoá chính lỗ fail-open** của mục 4. Ca ấy phải đổi thành hai ca: không có phép đo nào cho qua
   ⇒ DỪNG; `behind_by = 0` ⇒ QUA.
7. **Doc** (`CLAUDE.md`, chỉ mục *Đẩy ref từ phiên Claude Code trên web*): câu *"nhánh vùng làm việc xoá được khi
   `behind_by = 0`"* và câu *"Nhánh `luu-tru/**` xoá được khi commit CÒN TAG GIỮ"* đổi theo mục 2–4. Thêm một câu: nhánh
   ngoài mọi vùng nay chịu cùng phép đo. Không sửa đoạn nào khác của tệp (Q5).
8. **Hồ sơ packet** (`ops/specs/…`, `ops/leases/…`, `ops/acceptance/…/VERDICT.md`): tệp này, lease, và verdict review.

## nghiem_thu
Nền đo 18:44Z 25-11-2026 trên `origin/master` `d0868db`: `bash ops/don_ref_chot_test.sh` ⇒ `don_ref: 105/105 đạt`. Đơn vị
của 105 là **phép kiểm** (mỗi lần biến `QUA` hoặc `HONG` tăng), không phải số ca, finding hay đột biến. Trên nền có 58 dòng
`ca`, 25 dòng `lam`; phần còn lại là các phép kiểm phụ `doi_ra` · `doi_log_chot` · `doi_ra_lam` · `doi_log` và `actionlint`.

Mỗi tiêu chí dưới đây ghi phép đo làm nó ĐỎ. Đột biến chạy trên bản sao tạm của tệp YAML, không sửa tệp thật.

| # | tiêu chí | ca phải có (tên gợi ý) | đột biến làm ca ĐỎ |
|---|---|---|---|
| A1 (m1, m3) | `ops/**`, `behind_by = 3`, tag `luu-tru/x` trỏ đúng SHA ⇒ QUA, `rc=0`, dòng `cho phép` | `"ops/**: còn commit ngoài mặc định NHƯNG tag luu-tru giữ thì QUA"` | bỏ nhánh "hoặc có tag" ⇒ `rc=2` |
| A2 (m1) | như A1 nhưng tag tên `v9.9.9` trỏ đúng SHA ⇒ DỪNG `rc=2` | `"ops/**: tag KHÔNG thuộc luu-tru/ thì không tính"` | bỏ lọc tên `luu-tru/` ⇒ `rc=0` |
| A3 (m1) | tag `luu-tru/x` trỏ SHA KHÁC ⇒ DỪNG | `"ops/**: tag luu-tru trỏ SHA khác thì DỪNG"` | so tiền tố SHA thay vì cả 40 ký tự, hoặc bỏ so SHA ⇒ `rc=0` |
| A4 (m1) | `gh` hỏng ở trang 2 của `repos/tags`, `behind_by = 3` ⇒ DỪNG, câu có `KHÔNG ĐO ĐƯỢC` | `"ops/**: gh hỏng giữa phân trang tag thì DỪNG"` | nuốt lỗi `gh` (`|| true` trước phép so) ⇒ câu DỪNG mất chữ `KHÔNG ĐO ĐƯỢC` |
| A5 (m1) | tag `luu-tru/x` ở trang 2 ⇒ QUA | `"ops/**: tag luu-tru ở TRANG SAU vẫn QUA"` | bỏ `--paginate` ⇒ `rc=2` |
| A6 (m2) | `luu-tru/**` nhánh, chỉ tag `v9.9.9` giữ ⇒ DỪNG | `"luu-tru/**: tag KHÔNG thuộc luu-tru/ thì không tính"` | trả mục 2 về phép "tag bất kỳ" ⇒ `rc=0` |
| A7 (m2) | ba ca `luu-tru/**` đã có (dòng 126, 138, 139 trên `d0868db`) vẫn cho đúng `rc` cũ khi tag mang tên `luu-tru/…` | sửa dữ liệu ca cũ cho đồ giả mới, không đổi `rc` mong đợi | (bất biến; răng đến từ A6) |
| A8 (m4) | `coord/x`, `behind_by = 2`, không tag ⇒ DỪNG | `"tiền tố NGOÀI danh sách: không phép đo nào cho qua thì DỪNG"` | xoá nhánh `*)` ⇒ `rc=0` (hành vi cũ) |
| A9 (m4) | `tmp-probe-2`, `behind_by = 0` ⇒ QUA | thay ca dòng 120 | ép nhánh `*)` luôn DỪNG ⇒ `rc=2` |
| A10 (m4) | `coord/x`, không đọc được `behind_by`, không tag ⇒ DỪNG, câu có `KHÔNG ĐO ĐƯỢC` | `"tiền tố NGOÀI danh sách: không đo được thì DỪNG"` | coi `behind_by` rỗng là 0 ⇒ `rc=0` |
| A11 (m4) | `xoa-tag` trên tag tên thường (`tmp-tag`) ⇒ `rc` như trên `d0868db` | ca đối chứng | (bất biến của `ngoai_pham_vi`; đo trên nền trước khi sửa) |
| A12 (m5) | câu DỪNG của A2 và A8 khớp **toàn bộ** chuỗi `tạo tag luu-tru/* trỏ đúng <sha40>`, với `<sha40>` là SHA của ca; và **không** chứa `tạo tag giữ chúng` | trong A2, A8 | đổi câu về bản cũ ⇒ vế dương ĐỎ; khớp tiền tố `tạo tag` ⇒ vế âm ĐỎ |
| A13 (m6) | tổng `don_ref: N/N đạt` với hai số bằng nhau, N > 105 phép kiểm (nền) | cả tệp | — (đòi bằng chứng dương, không đọc `rc`) |
| A14 (m6) | đồ giả `gh` có trạng thái: đúng **một** lời gọi xoá, đúng endpoint, cho ca QUA của bước LÀM | ca bước LÀM đã có, chạy lại trên nhánh `coord/x` | bỏ lệnh xoá ở bước LÀM ⇒ nhật ký đồ giả không có lời gọi |
| A15 (m7) | `CLAUDE.md` mục *Đẩy ref*: vế dương có câu nói xoá nhánh vùng làm việc khi `behind_by = 0` **hoặc** có tag `luu-tru/*` trỏ đúng đầu nhánh, và câu nói nhánh ngoài mọi vùng chịu cùng phép đo. Khớp trên văn bản đã nối dòng trong phạm vi từng đoạn (L6 b). Vế âm: câu cũ "xoá được khi `behind_by = 0` so với nhánh mặc định" đứng một mình không còn | `rg` sau khi nối đoạn, ghi lệnh vào VERDICT | hoàn nguyên đoạn ⇒ vế dương ĐỎ |
| A16 | `actionlint` trên tệp workflow: delta so `d0868db` = 0 finding (có `shellcheck` mặt) | ca `actionlint` đã có | thêm `${{ }}` rỗng trong chú thích `run` ⇒ ĐỎ |
| A17 | `git diff --numstat d0868db..HEAD` toàn write set: ≤ 6 tệp, ≤ 450 dòng thêm | đo, ghi vào VERDICT | — (vượt ⇒ điểm dừng của `ADR-0053`, xem `luat_dung`) |
| A18 | `python .claude/dev/packet_loop.py doctrine-scan --root .` ⇒ `rc=0` | — | — (bất biến) |

Chạy thử trên nền trước khi đóng băng (18:44Z 25-11, `d0868db`): A1, A6, A8, A10 là ca mới nên chưa chạy được; hành vi nền
đo bằng run thật: A1 ứng với `45677566316` (DỪNG), A8 ứng với `45677710837` (QUA), tức đúng màu "chưa làm". A9 trên nền ra
QUA vì nền không đo gì, nên A9 chỉ có răng cùng A8. A11 phải đo trên nền trước khi sửa.

Tiêu chí chỉ đo được sau land: một lần chạy thử khô thật `xoa-nhanh ops/wp1475-r1-g1-lease` phải ra `cho phép` (tag
`luu-tru/wp1475-r1-leases` đã giữ `c46e269`). Người đo: phiên land. Bằng chứng: id run và dòng log. Trạng thái tới lúc ấy:
`chưa đo được`.

## tran_*
Hai dòng khai ở đầu tệp. Không khai `nang_tran`.
- Dự kiến kích thước (đo trên ba lần sửa gần nhất của chính hai tệp code: `a5804eb` +132, `1eebf90` +171, `bfde1b1` +36
  dòng thêm): code và test khoảng 150–200 dòng thêm, cộng hồ sơ packet. Tổng dự kiến dưới 450 dòng thêm, 6 tệp.
- Lời gọi Codex: theo bảng của `ADR-0055` với dòng khai trên. Không có ngân sách mềm.

## luat_dung
- `ADR-0053`: vượt 6 tệp hoặc 450 dòng thêm ⇒ dừng TRƯỚC review để sửa thiết kế. Không tự khai `nang_tran`. Nếu cần
  nâng trần thì đó là **E2**, mang theo mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- `ADR-0055`: chạm trần lời gọi Codex ⇒ dừng; hỏi chủ kho là **E2**.
- Credential Codex chết (container đo 18:30Z 25-11: bản chụp `CODEX_AUTH_JSON` cũ 33,5 h) ⇒ **E2**.
- `docs/PROTOCOL_DA_PHIEN.md` §12 (hội tụ, Review Rescue Checkpoint): áp nguyên văn.
- Một hình dạng finding lặp lại sau khi đã đổi thiết kế ⇒ **E1**, mang gốc rễ, các phương án đã thử, một đề xuất.
- Bằng chứng cho thấy một quyết định Q1–Q7 không đạt mục tiêu ⇒ **E3**.

## hinh_dang_ke_thua
`khong_ap_dung`: packet sửa cổng, không khắc phục một packet trước.
Bối cảnh, không phải bộ đếm: năm commit gần nhất chạm hai tệp code (`a5804eb` · `bfde1b1` · `1eebf90` · `cb12da5` ·
`1ea9c1c`). Ba trong số đó (`a5804eb`, `bfde1b1`, `1eebf90`) cùng một hình dạng: **chốt cấm theo tên được đổi thành phép
đo**. Packet này là lần thứ tư, áp hình dạng ấy cho nhánh `*)`. Lần thứ tư cùng hình dạng thì reviewer nên hỏi: còn
nhánh `case` nào cấm hay cho phép theo tên mà không đo không.

## chua_do_duoc
- Danh sách nhánh có tiền tố ngoài vùng làm việc trên GitHub, đo 18:44Z 25-11: `ccr-*` 3, `do-ci/` 5, `luu-tru/` 1. Sau
  land, các nhánh ấy chỉ xoá được khi đo qua. Tôi chưa kiểm từng nhánh có `behind_by = 0` không, vì điều đó không chặn
  packet.
- Đồ giả `gh` không mô phỏng giới hạn tốc độ API của `repos/tags`. Kho có bao nhiêu tag và phân trang mấy trang trên
  GitHub thật thì chưa đo từ phiên này.
- Hành vi trên runner thật của nhánh `*)` chỉ đo được sau land (tiêu chí sau-land ở trên).
