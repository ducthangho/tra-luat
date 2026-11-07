Review vòng 3 xong. Kết luận: **changes_requested**. r3 đóng được cả 11 finding vòng 2 của tôi, nhưng có một lỗ P1 mới cùng hình dạng với G01 vòng 2, cộng ba lỗ P2.

**Lỗ P1: K7 vẫn không bao giờ đạt trên dữ liệu thật, lần này qua `chan_buoc`.** K7 gọi nguyên trạng `ci_provenance.chan_buoc`. Hàm này trả True cho mọi bước có khoá `env:` ở mức bước.
- Trong `ci.yml` thật, bước luật của `gate-nhanh-manh` ×8, `gate-cong-cu` ×8, `gate-registry`, `gate-cong-cu-gop` và hai bước của `gate-ops` đều có `env:` (biến chọn mảnh hoặc chế độ). Vậy 19/22 job của một run land bị chặn.
- Cả 34 run có provenance đều không thể ra `passed`.
- Chỉ cần cho phép `env:` mức bước là 34/34 run qua phần YAML của K7.
- Fixture `F-ok` chứa đúng `gate-registry`. Giữ nguyên YAML thì ca A1 đỏ; cắt `env:` đi thì lại thành fixture tự đặt.
- A15 chỉ so tên bước, nên không ca nào bắt được lỗi này.

**Ba lỗ P2:**
- **Hồ sơ nhiều PR không đạt được L-7.** Các hồ sơ ghi `prs[*].merge_commit` và không có `merge_commit` ở mức gốc (pr1042-pr1068, pr1095-pr1101) không có *lời khai land* nào. Hồ sơ dạng ấy chỉ còn đường hạ `landed: false`.
- **`tom` luôn dùng `LUAT_HIEN_HANH`.** Sau lần thêm luật đầu tiên, các run trước mốc đổi luật không đo lại được, nên trạng thái mà ca A9(b) đòi không công cụ nào sinh ra.
- **D2b vẫn nhận `owner_waived` như lời khai thuần.** Chỉ cần ghi chữ ấy là né được toàn bộ D2b.

Các con số mới hoặc đổi của r3 đều tái lập được. Lệch duy nhất là bảng ba dạng tệp trộn hai cách đếm (P3). Kho không bị sửa. Script đo nằm dưới `/tmp/claude-0/-home-user-tra-luat/c92183b3-a8f8-5623-a5f6-065b91f250aa/scratchpad/review/r3-claude/work/` (`do_r3.py`, `k7_that.py`, `k7_tat_ca.py`, `k7_tat_ca_env.py`, `neo_r3.py`, `simB9x/`).

```
# VERDICT wp1236 r3 vòng 3
spec_sha256: e4166c02939f154c1d434b97840655d6184e028085f8ec8fe5b99bed885f5f22
## Finding vòng 2 của tôi
- G01: ĐÓNG — K7 nay so tên bước REST với `buoc` của provenance và với bước YAML; đo trên fe84620: mọi bước luật khớp đúng một `buoc` success và đúng một bước YAML, 0 tên trùng trên 754 job. Nhưng hệ quả G01 canh ("K7 không bao giờ đạt trên dữ liệu thật") tái phát qua `chan_buoc` ⇒ H01.
- G02: ĐÓNG — tiền đề sửa thành `bash -e {0}`; K7 đọc YAML (`continue-on-error`, `chan_buoc`, ống không pipefail); số Q6 26/9/1 trên 36 bước khớp. Phần dư về `shell: bash` ghi ở H05(d).
- G03: ĐÓNG — L-7 chỉ đòi *lời khai land*, `not_measured` cho run khác được phép, có ca B8. Định nghĩa lời khai land lại bỏ sót hồ sơ nhiều PR ⇒ H02.
- G04: ĐÓNG — `url_hop_le` truyền vào; D2b chép ba tệp; lỗi nạp ra rc 8; có B9 và D8. m-B9 không có răng ⇒ H06; cách module nạp `ci_provenance` chưa chốt ⇒ H05(e).
- G05: ĐÓNG — neo lấy từ đúng một chỗ, không thừa kế, `run_attempt` bắt buộc, có nhánh `moc_10_2_2` + `ci_master`, ca A18 (f/g/h). Ghi chú mẫu hồ sơ ở H07.
- G06: ĐÓNG cho L8/L-7 — `owner_waived` đòi URL, SHA bằng head neo và lý do ≥ 10 ký tự; giới hạn actor ghi ở Q10. D2b vẫn nhận lời khai thuần ⇒ H04.
- G07: ĐÓNG — có A20. m-A20b có thể tương đương ⇒ H06.
- G08: ĐÓNG — đã sửa 5→1 (tổng 64), 35→36, 16→13 và bỏ câu gán sai. Bảng ba dạng còn trộn hai cách đếm ⇒ H07.
- G09: ĐÓNG — (a) L8 tự đòi provenance, ca C3; (b) sửa câu về log; (c) rc 8, ca D8; (d) chuẩn hoá bỏ ký tự không phải chữ/số, ca A17; (e) câu định vị theo băm, "master trước rồi nhánh".
- G10: ĐÓNG — tách A1/A2; `can_cu` có numstat và tiền lệ +721; `nang_tran` đủ bốn trường của ADR-0053.
- G11: ĐÓNG — cấm đuôi mở, nhận diện bước theo tên REST, `F-luat` có vế âm. Cặp tên `tl selftest` theo sự kiện ⇒ H07.
## Findings mới
- id: H01
  severity: P1
  vi_tri: Thiết kế mục 5, K7 gạch `chan_buoc` (dòng 200); F-ok (dòng 460–464); A15 (dòng 487); A14 (dòng 486)
  van_de: K7 dùng nguyên trạng `chan_buoc`, mà hàm này chặn mọi bước có khoá `env:` mức bước (`set(s) - KHOA_BUOC`); các bước luật thật mang `env:` chọn mảnh/chế độ, nên mọi run `ci.yml` thật đều không thể ra `passed` — đường dương của L8, L-7 và D2b lại chết, và mọi hồ sơ landed bị đẩy sang `owner_waived`.
  bang_chung:
    · `python -I work/k7_that.py fe84620 …/pr1231…/provenance.yaml`: 21/46 bước luật bị CHAN. Lý do duy nhất là `khoa:env`: `gate-ops` ('ci-duong-nhanh selftest…', 'lease-publish selftest…'), `gate-nhanh-manh` ×8, `gate-cong-cu` ×8, `gate-registry` ('test registry…', env `CI_DANG_KY_*`), `gate-cong-cu-gop`.
    · `python -I work/k7_tat_ca.py` trên 34 tệp provenance: 30 run có 19 hoặc 30 job trong J bị chặn. 4 run còn lại là `launcher-windows.yml`, có job Windows không có luật. Kết quả: 0/34 run có thể `passed`.
    · Phản thực tế `k7_tat_ca_env.py` (thêm `env` vào `KHOA_BUOC`): 34/34 run qua phần YAML. Nguyên nhân duy nhất là khoá `env`.
    · Chính `ci_provenance` có 264 mục `dau_duong` `che_do_khong_xac_dinh`, tức cùng vị từ này là một nguyên nhân khiến provenance không bao giờ ghi `passed`.
    · `F-ok` chứa `gate-registry`: giữ nguyên `env:` thì A1 đỏ; cắt đi thì fixture không khớp thật (hình dạng thứ hai, lần 2).
    · A15 chỉ so tên bước, không chạy các vị từ YAML, nên không ca nào đỏ.
  de_xuat:
    · K7 dùng vị từ riêng `chan_k7`: giữ mọi điều kiện của `chan_buoc` (defaults, `env:` mức job/workflow, shell lạ, GITHUB_ENV/PATH ở bước trước), trừ khoá `env:` mức bước.
    · Cho phép `env:` mức bước khi nó là dict và tập khoá ⊆ tập CHO PHÉP khai theo từng bước trong `LUAT_v1` (chép từ `ci.yml` lúc soạn, nằm trong phần băm).
    · Mở rộng A15: chạy ĐỦ K7-YAML trên `F-that` cho cả 22 job J ⇒ 0 bị chặn. Đột biến "gọi `chan_buoc` nguyên trạng" ⇒ A15 đỏ (19 job). Đột biến "thêm một khoá env ngoài tập cho phép" ⇒ đỏ.
    · `F-ok` giữ nguyên văn `env:` của bước 'test registry'.
    · Ghi hình dạng thứ hai lần 2 vào `hinh_dang_ke_thua`.
- id: H02
  severity: P2
  vi_tri: *Lời khai land* (dòng 256–257); bảng luật, dòng L-7 (dòng 264); Q8 (dòng 630–632); B1–B8
  van_de: *Lời khai land* đòi head của neo bằng `merge_commit` ở MỨC GỐC, nhưng hồ sơ land nhiều PR ghi `prs[*].merge_commit` và không có `merge_commit` gốc, nên chúng không bao giờ có lời khai land ⇒ L-7 trượt chắc chắn, kể cả khi dùng `owner_waived`; đường duy nhất còn lại là `landed: false`.
  bang_chung:
    · `work/do_r3.py`: 5/123 hồ sơ thiếu `merge_commit` gốc; 3 trong số đó là landed theo L-6: pr1042-pr1068 (DAT kiểu b, `landed_20261031`), pr721, pr732.
    · `work/neo_r3.py`: pr1042-pr1068 có 6 lời khai, neo hợp lệ (`run_id`/`run_attempt`/`sha` = `prs[i].merge_commit`) nhưng `land=False` cả 6. pr1095-pr1101 có 2 lời khai, `land=False`.
    · Hai hồ sơ dạng này được thêm ngày 31-10 và 04-11, tức hình dạng còn đang dùng.
  de_xuat: Tập head land = {`merge_commit` gốc} ∪ {`prs[*].merge_commit`}. Đòi ≥ 1 lời khai land hợp lệ cho MỖI head trong tập. Thêm ca B10 (hồ sơ hai PR, đủ hai lời khai ⇒ DAT; thiếu một ⇒ TRUOT), kèm đột biến "chỉ đọc `merge_commit` gốc" ⇒ B10 đỏ. Bổ sung hệ quả này vào Q8.
- id: H03
  severity: P2
  vi_tri: Thiết kế mục 1 (dòng 137–143); mục 4 `tom` (dòng 177); *Đường sửa* (dòng 280); A9(b) (dòng 481)
  van_de: `tom` luôn ghi `LUAT_HIEN_HANH` (miền mở), trong khi K2 chỉ nhận phiên bản có miền chứa run; sau lần thêm `LUAT_v2` đầu tiên ở mốc R, không công cụ nào sinh được tệp hợp lệ cho run < R — trạng thái mà A9(b) khẳng định là `passed` — nên "đường sửa: chạy `tom` nếu log còn hạn" gãy cho mọi run trong hạn lưu log trước R.
  bang_chung: Dòng 142: "`tom` dùng phiên bản ấy". Dòng 177: "Dùng `LUAT_HIEN_HANH`". Dòng 138: ngoài miền ⇒ `luat_ngoai_mien_hieu_luc`. Tệp của A9(b) là tệp viết tay, không do `tom` sinh. Thêm nữa, hai đầu miền đều tính cả nên run R thuộc cả v1 lẫn v2.
  de_xuat: `tom` chọn phiên bản DUY NHẤT có miền chứa `run`; 0 hoặc >1 phiên bản ⇒ dừng, `not_measured`. Đòi các miền rời nhau. Thêm ca T6 (bản sao có v2, run < R ⇒ `tom` ghi băm v1 và `kiem` ra `passed`), kèm đột biến "`tom` dùng `LUAT_HIEN_HANH`" ⇒ T6 đỏ.
- id: H04
  severity: P2
  vi_tri: Bảng luật, dòng D2b (dòng 265: "`owner_waived` giữ nghĩa cũ của D2"); D6 (dòng 558)
  van_de: Ở M8, `owner_waived` vẫn là token thuần trong `DAT_MOC`, trong khi L-7 đòi ba điều kiện; viết `gate_output: owner_waived` là né trọn D2b, đúng thứ Issue gọi là "lời khai thuần" — cộng với H01, đường M8 trên thực tế chỉ còn lời khai.
  bang_chung:
    · `packet_loop.py:3095` `DAT_MOC = ("passed", "owner_waived")`; `:3475` chỉ kiểm thuộc tập.
    · D6 đòi rõ "không đòi `gate_output_nguon`".
    · D2b đã chép sẵn `ops/kiem_ho_so_land.py` (có `_url_hop_le`) mà không dùng.
  de_xuat: Với `owner_waived`, D2b đòi khoá gốc `gate_output_mien: <chuỗi>` thoả ba điều kiện của *Lời khai* (URL qua `_url_hop_le` canon, SHA bằng `merge_commit`, lý do ≥ 10 ký tự). Sửa D6 và thêm D9 kèm đột biến. Hoặc ghi thẳng vào `ngoai_pham_vi` và trình một Q mới cho chủ kho.
- id: H05
  severity: P3
  vi_tri: Thiết kế (dòng 131–132, mục 3–5, dòng 169–177, 197–202); D2b (dòng 267–271); D7 (dòng 559)
  van_de: Việc dùng lại `ci_provenance` chưa chốt đủ chi tiết.
  bang_chung:
    · (a) `ghep_buoc` cần `buoc` do `tach_buoc` sinh (khoá `gio`), nhưng `tach_buoc` không có trong danh sách hàm dùng lại.
    · (b) `ghep_buoc` trả `(k, chỉ số YAML)`, không trả số bước REST. `tom` phải tự dựng lại `ung` (logic nội bộ). `kiem` không kiểm số `STEP` với gì cả (`buoc` của provenance không có `number`), nên số ấy là trường tự do.
    · (c) `kiem`/`tom` đọc workflow tại `head_sha`, trong khi `ci_provenance` đọc tại SHA checkout. Hai thứ khác nhau ở run `pull_request`.
    · (d) K7 nói "`shell:` không đặt pipefail", nhưng `chan_buoc` chỉ cho shell bash/pwsh/sh, và GitHub chạy `shell: bash` khai tường minh bằng `-eo pipefail`. 9/36 bước luật có `shell: bash`.
    · (e) `packet_loop` không đặt `sys.path`, nên cách module nạp `ci_provenance` quyết định canon. D7 chỉ sửa module ở cây làm việc, không sửa `ci_provenance.py`.
  de_xuat:
    · (a)–(b): liệt kê `tach_buoc`; kiểm `buoc[số-1].name == name`, hoặc bỏ trường số.
    · (c): đọc workflow tại `moc.checkout[*].sha`, như `ci_provenance`.
    · (d): ghi rõ `shell: bash` tính là có pipefail.
    · (e): chốt nạp bằng `spec_from_file_location(Path(__file__).with_name(…))`; thêm D7b: sửa `ci_provenance.py` ở cây làm việc ⇒ vẫn ra `D2b`.
- id: H06
  severity: P3
  vi_tri: B9 (dòng 526); A20 (dòng 492)
  van_de: Hai đột biến được khai là "có răng" nhưng không làm ca đích đỏ.
  bang_chung:
    · `work/simB9x`: module có `import kiem_ho_so_land` ở đầu, `kiem_ho_so_land` nạp module LƯỜI ⇒ "nạp hai lần không đệ quy" vẫn XANH (in `nap hai lan OK; l7 = True True`). Vậy m-B9 tương đương với B9.
    · m-A20b ("bỏ tự kiểm băm khi nạp"): phần thiết kế không có phép tự kiểm lúc nạp, còn A20(a) do test tự tính lại băm, nên gỡ phép kiểm trong module không làm (a) đỏ.
  de_xuat: B9 đòi `'kiem_ho_so_land' not in sys.modules` sau khi nạp module trong tiến trình sạch. Thêm A20(c): bản sao module có một mục khoá ≠ băm ⇒ nạp hoặc `kiem` trả `not_measured` (`so_luat_hong`). Đặc tả hoá phép tự kiểm lúc nạp.
- id: H07
  severity: P3
  vi_tri: Bảng ba dạng (dòng 98–106); chua_do_duoc 3 (dòng 648–649); *Neo* quy tắc 2 (dòng 248–250); `LUAT_v1` nhận diện bước (dòng 150–151)
  van_de: Bảng số trộn hai cách đếm, một mục "chưa đo" đã đo được, và hai hệ quả chưa ghi.
  bang_chung:
    · `work/dang_tep.py` (cách đếm cho ra `tu_do` 13/11 mà đặc tả dùng): `danh_gia` 6 (4 chỉ dạng này), `tom` 4 (4 chỉ dạng này). Đặc tả ghi 6 (2) và 7 (3), tức hai hàng theo cách đếm có `phan-chung`, một hàng theo cách kia.
    · Tên bước trùng: 0 trên 754 job provenance; 0 tên `ten_du_kien` trùng trong YAML tại 3163f4d. chua_do_duoc 3 đo được offline ngay.
    · `tl selftest` có hai tên bước loại trừ nhau theo sự kiện ('luot PR…' khi `pull_request`, 'co bang chung…' khi khác). Mô hình tên bước không có phương án thay thế, nên lời khai dương cho run PR không thể `passed`.
    · 0/15 lời khai `moc_10_2_2` thật có `ci_master` kèm `run_attempt` (chỉ pr1155 có `ci_master`, và thiếu attempt). Hồ sơ mới chép mẫu pr1193/pr1197 sẽ ĐỎ `thieu_neo`.
  de_xuat: Đếm cả ba hàng cùng một cách. Chuyển chua_do_duoc 3 sang "đã đo". Ghi rõ `LUAT_v1` chọn biến thể push và hệ quả cho run PR (hoặc cho mỗi bước luật một tập tên thay thế). Ghi mẫu neo cho hồ sơ mới.
- id: H08
  severity: P3
  vi_tri: *Neo của lời khai* (dòng 253–254); mục 6 (dòng 209–212)
  van_de: "Lời khai trích tệp" chưa định nghĩa: cách tách đường dẫn khỏi chuỗi lời khai hiện chỉ có ở `land_evidence_nguon.token_nguon`/`phan_giai`; module không được nạp tệp ấy (D2b không chép), nên dễ sinh bộ tách thứ hai, trôi lệch với L1.
  bang_chung: `land_evidence_nguon.py:122` (`token_nguon`), `:143` (`phan_giai`, thứ tự provenance → ops/land → gốc). Đặc tả không nhắc hai hàm này.
  de_xuat: Truyền hàm tách token vào giống `url_hop_le`, hoặc đặc tả luật tách. Thêm vế A18: token trỏ tệp ngoài `<hồ sơ>-provenance/` ⇒ hành vi xác định.
## Đã đo lại, khớp
- sha256 đặc tả `e4166c02…` = `repo/ops/specs/wp1236-r3.md`; HEAD `d0fd4a7` = `3163f4d` + đặc tả.
- Tên khoá: 42/22/2/1/1. Dạng giá trị: 44/1/3/1/9/6 = 64; chuỗi khác duy nhất là pr1155.
- Lời khai: 46 hồ sơ; 44 hồ sơ có lời khai khác `not_measured`, tổng 61; 22 có / 22 không có provenance.
- L5: 9 tên; pr679 MẤT MIỄN TRỪ ⇒ 8 hồ sơ thật sự được miễn ⇒ L8 hồi tố 36; bảng 36 dòng khớp đúng tập.
- `tu_do` 13/11.
- `merge_commit` gốc 118/123 (thiếu: pr1042, pr1095, pr721, pr732, pr838).
- Chuẩn hoá tên khoá không thêm khoá mới.
- Provenance: 28 hồ sơ / 34 tệp; 753 `not_measured` + 1 `failed`.
- Ruff 0.17.3: `packet_loop` 1 F841, `packet_loop_test` 2 F541, bốn tệp `ops/` và `ci_dang_ky_test` 0.
- `land_evidence_nguon`: 98 · 25/28 · 0 · 0 · 123, rc 0. `kiem_ho_so_land`: 49/49, rc 0.
- Q6: 26/9/1 trên 36 bước.
- Tên job/bước/labels của `F-ok` có thật trong provenance pr1231; fe84620 có trong kho; `ghep_buoc` passed 23/23 job pr1231.
- Bước `chuan-bi` có `continue-on-error: true`; 0 bước luật có `|` mà thiếu pipefail.
- Không kiểm được (không có trong clone hoặc cần mạng): nhánh `ops/wp1240-r1-g1-lease` và tệp nguồn N1/N2; con số 755 nhánh; câu "run id tăng đơn điệu".
KET_LUAN: changes_requested
```