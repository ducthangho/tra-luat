# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B2` (revision 1)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B2** · `revision`: **1** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Cùng `CI-TAI-DUNG-THEO-CAY-B1` thay packet `CI-TAI-DUNG-THEO-CAY-B` (xem đặc tả B1 r1).
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**). Packet anh em: `CI-TAI-DUNG-THEO-CAY-A`
  r3 (ADR-0068) và `CI-TAI-DUNG-THEO-CAY-B1` r1 (biên nhận và chạy bóng).
- **Phụ thuộc, đủ cả ba mới cấp lease B2:** (1) A đã land; (2) B1 đã land; (3) điều kiện bật của `ADR-0068` Q8 đã đo đạt:
  ít nhất 20 lượt `push` lên `master` sau land B1 có `TAI_DUNG_BONG` đánh dấu ít nhất một nhóm, và `kiem-lai-tai-dung` trên
  mọi lượt bóng từ land B1 tới lúc đo không in `LECH_BONG` nào và rc 0. Người cấp lease đính kèm bảng đo ấy (id lượt, SHA,
  tập nhóm, rc).
- `nguon_cap_viec`: như đặc tả A r3.
- `review_class`: **sensitive** — đổi job nào chạy ở lượt `push` lên `master` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, chứa commit land của A và của B1.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (**E5**). Điều kiện merge theo `ADR-0060`; M3
  Windows **`required`** (diff chạm `*.ps1`, `.claude/dev/**`, `.github/workflows/**`): trên máy Windows của chủ kho theo
  `ADR-0057`–`ADR-0059`, BASE và ứng viên cùng máy, chạy `python ops/ci_duong_nhanh_test.py`, `python
  .claude/dev/ci_dang_ky_test.py` (không `--chay`) và `pwsh .claude/dev/chay-cong-windows_test.ps1`.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r3.)

## 0. Vấn đề và thiết kế

B1 đã ghi, ở mọi lượt `push` lên `master`, nhóm nào tái dùng được (`tai_dung_bo_bong`). B2 nối output ấy vào điều kiện
cấp job: nhóm có trong `tai_dung_bo` thì mọi job của nhóm nghỉ; job `gate` thêm một bước tự tính lại phép chứng minh bằng
git và in dấu hiệu dương. Bảng bốn nhóm và tám job ở đặc tả B1 r1 mục 0.

Chốt đang ghim hình dạng mà B2 đổi (số dòng trên `origin/master` `45bae8d0`; B1 land trước có thể dời, người thi hành đo lại):

- `ops/ci_duong_nhanh_test.py`: `JOB_CO_IF_CHO_PHEP` và `y11` (`:2844`, `:2849`), `IF_BUOC_CHUAN` và `y12` (`:2620`,
  `:2859`), `y13` (`:2879`), `KHUNG_JOB` (`:2702`).
- `.claude/dev/ci_dang_ky_test.py`: `BAM_GATE_REGISTRY` (`:836`), `BAM_GATE_NHANH` (`:840`), `G5_MANH_IF` (`:1425`),
  `G5_GOP_IF` (`:1431`), tập `_if_duoc` (`:1454`), nhánh `gate-packet-loop-manh` (`:1523`), nhánh `gate-registry` của
  `_job_if_duoc_phep` (`:594`) và của `loi_g5_workflow`.
- `.claude/dev/chay-cong-windows_test.ps1`: bảng dấu vân `$DauVanCi` (`:1343`, dấu vân gồm `if` cấp job) và ca `t32`
  (`:1409`, mọi bước của job `gate*` phải có gương trong `.claude/dev/chay-cong-windows.ps1` hoặc có tên trong dòng
  `KHÔNG CHẠY`/`THAY BẰNG`). Review lượt 1 trên B r2 đo: thêm điều kiện cấp job vào tám job ⇒ tám dấu vân lệch.

## 1. write_set

- `.github/workflows/ci.yml`
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.claude/dev/ci_dang_ky_test.py`
- `.claude/dev/chay-cong-windows_test.ps1`
- `.claude/dev/chay-cong-windows.ps1`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set (`ai-dang-giu` trên kho bare khớp máy
chủ), đo ngay trước khi cấp. Lúc soạn, ba tệp đầu thuộc `wp1448-r2-g1-claude` (đặc tả B1 r1 mục 9); B2 vốn còn chờ A, B1 và
giai đoạn bóng.

Kích thước ước theo khối (dòng thêm): `ci.yml` tám điều kiện cấp job và bước `kiem-tai-dung` của `gate` khoảng 20; lệnh
`kiem-tai-dung` và đổi output bóng thành output thật khoảng 30; cập nhật chốt và ca, đột biến trong
`ops/ci_duong_nhanh_test.py` khoảng 60; chốt và đột biến trong `.claude/dev/ci_dang_ky_test.py` khoảng 20; dấu vân Windows
khoảng 10; dòng gương hay `KHÔNG CHẠY` cho bước mới khoảng 3. Cộng khoảng **145**, dưới trần 450.

## 2. ngoai_pham_vi

- Bộ xét, biên nhận, `kiem-lai-tai-dung`: B1 (B2 chỉ dùng).
- Luật: A.
- Lượt `pull_request`, `workflow_dispatch`, Windows CI: không đổi job nào chạy.
- Các bước bên trong tám job: không sửa.

## 3. muc_tieu

1. `.github/workflows/ci.yml` — job `chuan-bi`: thêm output `tai_dung_bo` lấy từ output của bước `xet-tai-dung` của B1; giữ
   `tai_dung_bo_bong` để lần đo sau land so được hai output.
2. `.github/workflows/ci.yml` — tám job của bốn nhóm: điều kiện cấp job thêm vế
   `!contains(needs.chuan-bi.outputs.tai_dung_bo, ',<nhóm>,')`, nối bằng `&&` vào điều kiện đang có, hoặc là điều kiện duy
   nhất nếu job chưa có. Chỉ khi chuỗi chứa đúng `,<nhóm>,` mới nghỉ; rỗng, vắng hay lạ ⇒ chạy.
3. `.github/workflows/ci.yml` + `ops/ci_duong_nhanh.py` — job `gate`: bước mới, `if:` đúng
   `needs.chuan-bi.outputs.tai_dung_bo != ''`, chạy lệnh `kiem-tai-dung` với các output `tai_dung_bo`, `tai_dung_run`,
   `tai_dung_attempt`, `tai_dung_cha` của `chuan-bi` (B2 thêm ba output sau từ bước xét của B1) và `github.sha`: tính lại
   bằng git trên checkout của `gate` phép (4b) và (4e) của B1, in
   `TAI_DUNG: DAT run=<id> attempt=<n> cay=<tree> cha=<P1>,<P2> nhom=<danh sách>`; lệch hay thiếu ⇒ rc ≠ 0. Các bước khác của
   `gate` giữ nguyên điều kiện.
4. `ops/ci_duong_nhanh_test.py` — cập nhật `JOB_CO_IF_CHO_PHEP`, `IF_BUOC_CHUAN`, `y13`, `KHUNG_JOB`; ca và đột biến cho mục
   2 và 3; ca canh "tập job mang vế `tai_dung_bo` đúng bằng tám job của bảng nhóm, `gate` và `chuan-bi` không mang".
5. `.claude/dev/ci_dang_ky_test.py` — cập nhật `BAM_GATE_REGISTRY`, `BAM_GATE_NHANH`, `G5_MANH_IF`, `G5_GOP_IF`, `_if_duoc`,
   hai nhánh điều kiện ở mục 0 cho điều kiện mới, sau khi rà hành vi; giữ nguyên mọi chốt khác.
6. `.claude/dev/chay-cong-windows_test.ps1` — cập nhật `$DauVanCi` cho các job có dấu vân đổi.
7. `.claude/dev/chay-cong-windows.ps1` — bước `kiem-tai-dung` của `gate` có dòng `KHÔNG CHẠY` kèm lý do (chỉ có nghĩa ở lượt
   `push` lên `master` của CI), để `t32` xanh.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| D1 | Trên Ubuntu (CI của PR): `python ops/ci_duong_nhanh_test.py` (job `gate-ops`) và `python .claude/dev/ci_dang_ky_test.py --chay` (job `gate-registry`) in dòng tổng `N/N` hai số bằng nhau, rc 0. Trên máy Windows của chủ kho (`ADR-0060` M3, BASE và ứng viên): ba lệnh ở đầu tệp, mỗi lệnh có dòng tổng hai số bằng nhau và rc 0 | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở D2 |
| D2 | Đột biến riêng, mỗi cái chết đúng ca của nó: bỏ vế `tai_dung_bo` khỏi từng job trong tám job (tám đột biến YAML); thêm vế ấy vào `gate`; đổi chuỗi `',ops,'` thành `'ops'` (khớp chuỗi con); `kiem-tai-dung` với cha lệch, cây lệch, `tai_dung_bo` rỗng mà bước vẫn chạy (ba đột biến) | một đột biến sống, hay chết vì lý do khác chốt | chính bảng ấy |
| D3 | `actionlint` trên `ci.yml` không thêm finding so với BASE (delta 0, cùng nền có `shellcheck`) | thêm finding | — |
| D4 | Trước land, trên dữ liệu thật: chọn một lượt `push` lên `master` đã có `TAI_DUNG_BONG` khác rỗng (ghi id, SHA); dựng lại đúng môi trường của nó trong một workflow đo tạm trên `do-ci/**`, chạy phần `chuan-bi` và `gate` mới với `tai_dung_bo` lấy từ chính artefact `bien-nhan-tai-dung` của lượt ấy. Đòi: `kiem-tai-dung` in `TAI_DUNG: DAT` với đúng run nguồn; trên bản sao artefact đổi `cha` hay đổi cây thì `kiem-tai-dung` rc ≠ 0. Không có lượt bóng nào khác rỗng thì B2 chưa đủ phụ thuộc (3), không cấp lease | `TAI_DUNG: DAT` vắng; bản sao sửa vẫn rc 0 | hai bản sao sửa ấy |
| D5 | Sau land (**chưa đo được** tới lúc ấy): mười lượt `push` lên `master` đầu tiên sau commit land của B2, chọn theo `created_at`, ghi id và SHA trước khi đọc kết quả. Với mỗi lượt có `tai_dung_bo` khác rỗng: đúng các job của nhóm ấy `skipped`, các job khác chạy, `gate` `success` có dòng `TAI_DUNG: DAT`, và `kiem-lai-tai-dung --run <id>` (lệnh của B1, tính lại độc lập từ REST) rc 0. Với lượt rỗng: log `chuan-bi` có lý do. Ghi số lượt theo từng tập nhóm | một lượt mà tập job `skipped` khác tập nhóm ghi; `kiem-lai-tai-dung` rc ≠ 0; thiếu `TAI_DUNG: DAT` khi có nhóm nghỉ | răng của `kiem-lai-tai-dung` ở đặc tả B1 C2 mục 5; D5 tự nó không có đột biến riêng vì nó đọc CI thật sau land |

D5 không đòi có lượt tái dùng trong mười lượt; không có thì ghi "chưa quan sát được tái dùng", không phải đạt. Không chọn
lượt theo dự đoán kết quả.

Bảng năm vế L6: D1 khớp dòng tổng do máy in, vế âm là rc ≠ 0; (b), (d) không áp dụng (một dòng, chữ số); (c) đếm theo từng
đột biến ở D2; (e) không có lời khai "0 cổng". Dòng `TAI_DUNG: DAT` ở D4, D5: tiền tố cố định do mã in, nội dung kiểm lại
bằng `kiem-lai-tai-dung`.

## 5. luat_dung

- Trần kích thước `ADR-0053`: ước khoảng 145 dòng thêm. Vượt ⇒ dừng và hỏi chủ kho mã **E2**, mang `git diff --numstat`,
  trần đang áp và trần xin.
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã dùng, finding còn mở
  và số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Thiếu một trong ba phụ thuộc ⇒ không cấp lease (không phải điểm hỏi).
- Giai đoạn bóng có `LECH_BONG` ⇒ không bật. Người giữ việc tìm gốc rễ (lỗi chập chờn, nền khác, hay lỗi của bộ xét). Lỗi của
  bộ xét ⇒ revision của B1. Gốc rễ là lỗi chập chờn hay nền, nghĩa là lợi ích của Đ2 đổi so với lúc chủ kho chọn ⇒ hỏi chủ
  kho mã **E3**, mang danh sách `LECH_BONG`, số lượt bóng và phân tích gốc rễ.
- Cần sửa một tệp ngoài write set ⇒ dừng phiên, revision mới; không phải điểm hỏi trừ khi vượt trần (**E2**).

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — đổi job nào chạy ở lượt `push` lên `master`, sửa chốt ghim của bộ đăng ký. Mỗi việc sau mang mã **E5**: chủ
  kho duyệt băm, cấp lease, audit trước merge.

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Hai lớp lỗi từ review lượt 1 trên B r2 nằm ở đây: chốt ghim bị bỏ sót (F2) và
quan sát sau land không kiểm nguồn tái dùng (F8). Đặc tả này liệt kê chốt ghim theo số dòng và dùng `kiem-lai-tai-dung` cho
D5.

## 8. chua_do_duoc

- Số lượt bóng cần để đủ 20 lượt có tái dùng: tuỳ tỷ lệ merge cây trùng sau #1343; lịch sử 01→15-11 là 25/79.
- Vị trí chốt ghim sau khi B1 (và có thể #1448) land: số dòng ở mục 0 là trên `45bae8d0`.

## 9. Đo lúc soạn (20-11-2026)

- `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`.
- Số dòng chốt ghim ở mục 0: đo bằng `grep -n` trên bản sao thưa của `45bae8d0`.
- Lease đang giữ write set: xem đặc tả B1 r1 mục 9; `.claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 0` (09:35:51Z–09:39:05Z,
  367/367 nhánh). Hai tệp `.ps1` chưa quét; người cấp lease quét đủ sáu đường dẫn ngay trước khi cấp.
