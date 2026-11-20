# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B2` (revision 2)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B2** · `revision`: **2** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Thay r1 (sha256 `f705edcff5dfea3a00040361f53a3a694438ababa01dc2fe1f7db400f86e6d77`, review lượt 2
  `changes_requested`, chưa từng được duyệt). Thay đổi so với r1: mục 10.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**). Packet anh em: `CI-TAI-DUNG-THEO-CAY-A`
  r4 (ADR-0068) và `CI-TAI-DUNG-THEO-CAY-B1` r2 (biên nhận và chạy bóng).
- **Phụ thuộc để cấp lease:** A đã land và B1 đã land. **Điều kiện bật** (`ADR-0068` Q8) là tiêu chí D0 **trước merge**, đo
  bằng chính lệnh `kiem-lai-tai-dung` của packet này (lệnh chưa tồn tại thì chưa đo được).
- `nguon_cap_viec`: như đặc tả A r4.
- `review_class`: **sensitive** — đổi job nào chạy ở lượt `push` lên `master` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, chứa commit land của A và của B1.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (**E5**). Điều kiện merge theo `ADR-0060`; M3
  Windows **`required`** (diff chạm `*.ps1`, `.claude/dev/**`, `.github/workflows/**`): trên máy Windows của chủ kho theo
  `ADR-0057`–`ADR-0059`, BASE và ứng viên cùng máy, chạy `python ops/ci_duong_nhanh_test.py`, `python
  .claude/dev/ci_dang_ky_test.py` (không `--chay`) và `pwsh .claude/dev/chay-cong-windows_test.ps1`.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r4.)

## 0. Vấn đề và thiết kế

B1 đã ghi, ở mọi lượt `push` lên `master`, nhóm nào tái dùng được (output `*_bong`, artefact `bien-nhan-tai-dung` với
`che_do_xet` `bong`). B2 làm ba việc:

1. Lệnh `kiem-lai-tai-dung`: tính lại độc lập quyết định của một lượt `push` từ REST và git, so **đủ** bằng chứng, và kiểm kết
   quả thực thi của chính lượt `push` theo chế độ (`bong`: nhóm được đánh dấu phải chạy `success`; `bat`: nhóm ấy phải nghỉ).
   Lệnh này đo điều kiện bật Q8 (D0) và quan sát sau land (D5).
2. Nối output của bộ xét vào điều kiện cấp tám job; bộ xét ghi `che_do_xet` `bat`.
3. Job `gate` thêm bước `kiem-tai-dung` tự tính lại phép chứng minh bằng git và in dấu hiệu dương.

Bảng bốn nhóm và tám job ở đặc tả B1 r2 mục 0. Chốt đang ghim hình dạng mà B2 đổi (số dòng trên `origin/master` `45bae8d0`;
B1 land trước sẽ dời số, người thi hành đo lại):

- `ops/ci_duong_nhanh_test.py`: `TAP_CHO_PHEP` và `y03` (`:75`, `:2479`), `Y04_IF_JOB_CHE_DO` và `y04` (`:2506`, `:2515`),
  `y06` (job bắt buộc `gate`, `gate-ops`, `gate-packet-loop` không được nghỉ cả job, `BAT_BUOC` `:68`, `:2559`), `y07` (bước bị
  bỏ tự nói lý do, `:2569`), `JOB_CO_IF_CHO_PHEP` và `y11` (`:2844`, `:2849`), `IF_BUOC_CHUAN` và `y12` (`:2620`, `:2859`),
  `y13` (`:2879`), `RUN_BUOC_PACKET` và `y14` (`:2899`, `:2926`), `KHUNG_JOB` (`:2702`). Review lượt 2 đo bằng hàm guard thật:
  chỉ tám điều kiện cấp job đã làm `y04`, `y06`, `y11`, `y13` đỏ; thêm bước ở `gate` làm thêm `y03`, `y07`, `y12`, `y14` đỏ.
- `.claude/dev/ci_dang_ky_test.py`: `BAM_GATE_REGISTRY` (`:836`), `BAM_GATE_NHANH` (`:840`), `G5_MANH_IF` (`:1425`),
  `G5_GOP_IF` (`:1431`), tập `_if_duoc` (`:1454`), nhánh `gate-packet-loop-manh` (`:1523`), nhánh `gate-registry` của
  `_job_if_duoc_phep` (`:594`) và của `loi_g5_workflow` (`:1525`).
- `.claude/dev/chay-cong-windows_test.ps1`: bảng dấu vân `$DauVanCi` (`:1343`, dấu vân gồm `if` cấp job; review lượt 1 đo
  tám dấu vân lệch) và ca `t32` (`:1409`): mọi bước của job `gate*` có gương trong `.claude/dev/chay-cong-windows.ps1` hoặc có
  tên trong dòng `KHÔNG CHẠY`/`THAY BẰNG`.
- `ops/cong_cu_test.py` `t6` khoá các bước của `gate` **trước** bước G5 (`:339`); bước mới đặt **sau** G5 để khỏi sửa tệp ấy.
- `y06` có lý do: job bắt buộc nghỉ cả job thì check bắt buộc đọc như xanh trên PR. Ở lượt `push` lên `master` không có check
  bắt buộc nào. B2 mở một ngoại lệ hẹp đúng vế `tai_dung_bo` cho `gate-ops` và `gate-packet-loop`; mọi điều kiện khác vẫn bị
  `y06` chặn.

## 1. write_set

- `.github/workflows/ci.yml`
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.claude/dev/ci_dang_ky_test.py`
- `.claude/dev/chay-cong-windows_test.ps1`
- `.claude/dev/chay-cong-windows.ps1`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set (`ai-dang-giu` trên kho bare khớp máy
chủ), đo ngay trước khi cấp, đủ sáu đường dẫn.

Kích thước ước theo khối (dòng thêm): `kiem-lai-tai-dung` (đọc hai lượt, tải lại, so đủ trường, hai chế độ, lịch sử) khoảng
95; `kiem-tai-dung` và đổi output bóng thành output thật khoảng 30; `ci.yml` (tám điều kiện, bước `gate`, output) khoảng 20; ca
và đột biến của `kiem-lai-tai-dung` khoảng 95; cập nhật chốt và ca, đột biến khác trong `ops/ci_duong_nhanh_test.py` khoảng 60;
`.claude/dev/ci_dang_ky_test.py` khoảng 20; dấu vân Windows khoảng 10; dòng `KHÔNG CHẠY` khoảng 3. Cộng khoảng **335**, dưới
trần 450.

## 2. ngoai_pham_vi

- Biên nhận, bộ xét, bảng nhóm, dạng chuẩn của `tai_dung_bo`: B1 (B2 chỉ đổi `che_do_xet` và tên output).
- Luật: A.
- Lượt `pull_request`, `workflow_dispatch`, Windows CI: không đổi job nào chạy.
- Các bước bên trong tám job: không sửa.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — lệnh `kiem-lai-tai-dung --run <id lượt push>`:
   - a. Đọc lượt `push` qua REST: sự kiện `push`, nhánh mặc định, `path` `.github/workflows/ci.yml`, `status` `completed`;
     ghi `run_attempt`. Tải artefact `bien-nhan-tai-dung` của chính lượt ấy qua `goi_that`; đọc JSON: `phien_ban` 1,
     `che_do_xet` thuộc `{bong, bat}`.
   - b. Tính lại **độc lập**, neo vào lượt nguồn đã ghi (id, attempt), các phép 4b–4g của đặc tả B1 r2 bằng git cục bộ (lấy đủ
     object) và REST; so **từng trường** với bản đã ghi: P1, P2, M, cây, `before`, blob OID của `ci.yml` tại M, lượt nguồn,
     id và sha256 của zip biên nhận (tải lại), nội dung biên nhận, tên, id, `run_attempt` và kết luận từng job theo nhóm, hai
     diff, hai kế hoạch, ảnh runner, tập nhóm. Lệch một trường ⇒ rc 1.
   - c. Jobs của chính lượt `push` (`filter=latest`, đủ trang): với mỗi nhóm **được ghi là tái dùng được**, tập job
     `ubuntu-latest` của nhóm phải khớp **đúng** tập chỉ số ma trận. Chế độ `bong`: mọi job ấy `success`, khác thì in
     `LECH_BONG: <nhóm> <job> <kết luận>`. Chế độ `bat`: mọi job ấy `skipped`, khác thì in `LECH_BAT: …`; và mọi job của nhóm
     **không** được ghi là tái dùng phải có mặt và không `skipped`.
   - d. Thiếu dữ liệu, đọc lỗi, danh sách rỗng hay thiếu job ⇒ rc 2 (`KHONG_DO_DUOC`), không bao giờ rc 0 trên tập rỗng.
   - e. rc 0 khi mọi trường bằng nhau và không có `LECH_*`; rc 1 khi lệch; rc 2 khi không đo được.
   - f. `kiem-lai-tai-dung --tu <commit land của B1>`: liệt kê **mọi** lượt `ci.yml` sự kiện `push` trên nhánh mặc định có
     `created_at` sau commit ấy (đủ trang; in id và SHA lượt đầu, lượt cuối, tổng số), chạy (a)–(e) cho từng lượt có artefact,
     ghi lượt không có artefact là `khong_bien_nhan`, và in bảng: id lượt, SHA, `che_do_xet`, tập nhóm, rc. Dòng tổng
     `Q8: <số lượt có tập nhóm khác rỗng và rc 0>/<số lượt có tập nhóm khác rỗng> · rc1=<n> · rc2=<n>`.
2. `ops/ci_duong_nhanh.py` + `.github/workflows/ci.yml` — job `chuan-bi`: bộ xét ghi `che_do_xet` `bat`; thêm output
   `tai_dung_bo`, `tai_dung_run`, `tai_dung_cha`, `tai_dung_cay` (từ bước xét của B1); giữ các output `*_bong`.
3. `.github/workflows/ci.yml` — tám job của bốn nhóm: điều kiện cấp job thêm vế
   `!contains(needs.chuan-bi.outputs.tai_dung_bo, ',<nhóm>,')`, nối bằng `&&` vào điều kiện đang có, hoặc là điều kiện duy
   nhất nếu job chưa có. Chỉ chuỗi chứa đúng `,<nhóm>,` mới làm nhóm nghỉ; bộ xét của B1 chỉ phát dạng chuẩn (ca dạng chuẩn
   của B1), nên chuỗi lạ chỉ có thể đến từ lỗi của bộ xét, và `kiem-lai-tai-dung` bắt lỗi ấy ở D5.
4. `.github/workflows/ci.yml` + `ops/ci_duong_nhanh.py` — job `gate`: bước mới **sau** bước G5, `if:` đúng
   `needs.chuan-bi.outputs.tai_dung_bo != ''`, chạy lệnh `kiem-tai-dung` với `tai_dung_bo`, `tai_dung_run`, `tai_dung_cha`,
   `tai_dung_cay` và `github.sha`: M có đúng hai cha bằng `tai_dung_cha`; `M^{tree}` bằng `tai_dung_cay` và bằng
   `git merge-tree --write-tree P1 P2`; in `TAI_DUNG: DAT run=<id> cay=<tree> cha=<P1>,<P2> nhom=<danh sách>`; lệch hay thiếu ⇒
   rc ≠ 0. Các bước khác của `gate` giữ nguyên điều kiện.
5. `ops/ci_duong_nhanh_test.py` — cập nhật chốt ở mục 0 (gồm ngoại lệ hẹp của `y06`); ca và đột biến theo mục 4; ca canh "tập
   job mang vế `tai_dung_bo` đúng bằng tám job của bảng nhóm; `gate`, `chuan-bi`, `bien-nhan-cay` không mang".
6. `.claude/dev/ci_dang_ky_test.py` — cập nhật các chốt ở mục 0 cho điều kiện mới, sau khi rà hành vi; giữ nguyên mọi chốt
   khác.
7. `.claude/dev/chay-cong-windows_test.ps1` — cập nhật `$DauVanCi` cho các job có dấu vân đổi.
8. `.claude/dev/chay-cong-windows.ps1` — bước `kiem-tai-dung` của `gate` có dòng `KHÔNG CHẠY` kèm lý do (chỉ có nghĩa ở lượt
   `push` lên `master` của CI), để `t32` xanh.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| D0 | **Trước merge**, điều kiện bật `ADR-0068` Q8: `kiem-lai-tai-dung --tu <commit land của B1>` chạy trên head ứng viên in dòng tổng `Q8: a/b · rc1=0 · rc2=0` với a ≥ 20 và a = b. Bảng đầy đủ đính vào handoff | a < 20; rc1 > 0; rc2 > 0 | đột biến trên bản sao artefact thật của một lượt bóng ở D2 |
| D1 | Trên Ubuntu (CI của PR): `python ops/ci_duong_nhanh_test.py` (job `gate-ops`) và `python .claude/dev/ci_dang_ky_test.py --chay` (job `gate-registry`) in dòng tổng `N/N` hai số bằng nhau, rc 0. Trên máy Windows của chủ kho (`ADR-0060` M3, BASE và ứng viên): ba lệnh ở đầu tệp, mỗi lệnh có dòng tổng hai số bằng nhau và rc 0 | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở D2 |
| D2 | Đột biến riêng, mỗi cái chết đúng ca của nó. `kiem-lai-tai-dung` trên bằng chứng sửa tay (fixture trong test): đổi lượt nguồn sang một lượt khác; đổi kế hoạch; bỏ danh sách job của một nhóm; đổi sha256 zip; lượt `push` thiếu một mảnh của nhóm; lượt `push` trả danh sách job rỗng ⇒ rc 2; chế độ `bong` có một job `failure` ⇒ `LECH_BONG`; chế độ `bat` có một job của nhóm chạy ⇒ `LECH_BAT`; chế độ `bat` có một job ngoài nhóm `skipped` ⇒ rc 1; chế độ `bat` đúng hoàn toàn ⇒ rc 0 (đối chứng dương); `--tu` bỏ sót một lượt có artefact ⇒ đột biến bị bắt — mười một. Điều kiện cấp job: bỏ vế khỏi từng job trong tám job (tám đột biến YAML); thêm vế vào `gate`; đổi `',ops,'` thành `'ops'`; mở ngoại lệ `y06` cho một điều kiện khác — ba. `kiem-tai-dung`: cha lệch; `tai_dung_cay` lệch với `M^{tree}`; `merge-tree` ra cây khác — ba | một đột biến sống, hay chết vì lý do khác chốt | chính bảng ấy |
| D3 | `actionlint` trên `ci.yml` không thêm finding so với BASE (delta 0, cùng nền có `shellcheck`) | thêm finding | — |
| D4 | Trước land, trên dữ liệu thật: lấy một lượt bóng có tập nhóm khác rỗng và `kiem-lai-tai-dung` rc 0 (ghi id, SHA); trên một workflow đo tạm `do-ci/**`, chạy bước `kiem-tai-dung` với các output ghi trong artefact của lượt ấy ⇒ in `TAI_DUNG: DAT` với đúng run nguồn. Đổi đầu vào `tai_dung_cay` thành một cây khác ⇒ rc ≠ 0; đổi `tai_dung_cha` ⇒ rc ≠ 0 | `TAI_DUNG: DAT` vắng; một trong hai đầu vào sửa vẫn rc 0 | hai đầu vào sửa ấy |
| D5 | Sau land (**chưa đo được** tới lúc ấy): mười lượt `push` lên `master` đầu tiên sau commit land của B2, chọn theo `created_at`, ghi id và SHA trước khi đọc kết quả. Với mỗi lượt: `kiem-lai-tai-dung --run <id>` (chế độ `bat`) rc 0; lượt có tập nhóm khác rỗng thì `gate` có dòng `TAI_DUNG: DAT`. Ghi số lượt theo từng tập nhóm | `kiem-lai-tai-dung` rc ≠ 0 trên một lượt; thiếu `TAI_DUNG: DAT` khi có nhóm nghỉ | răng của `kiem-lai-tai-dung` ở D2 |

D5 không đòi có lượt tái dùng trong mười lượt; không có thì ghi "chưa quan sát được tái dùng", không phải đạt.

Bảng năm vế L6: D0 và D1 khớp dòng tổng do máy in một dòng (vế âm: rc ≠ 0, a < 20); (b), (d) không áp dụng (một dòng, chữ
số); (c) đếm theo từng đột biến ở D2; (e) không có lời khai "0 cổng". Dòng `TAI_DUNG: DAT`: tiền tố cố định do mã in, nội dung
kiểm lại bằng `kiem-lai-tai-dung`.

## 5. luat_dung

- Trần kích thước `ADR-0053`: ước khoảng 335 dòng thêm. Vượt 450 ⇒ dừng và hỏi chủ kho mã **E2**, mang `git diff --numstat`
  từng tệp, khối nào vượt ước, trần đang áp và trần xin, lý do không tách được.
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã dùng, finding còn mở
  và số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Thiếu một trong hai phụ thuộc cấp lease ⇒ không cấp lease (không phải điểm hỏi).
- D0 chưa đủ 20 lượt ⇒ giữ PR chưa merge, đo lại khi có thêm lượt bóng (không phải điểm hỏi).
- D0 có `rc1` > 0 (có `LECH_BONG` hay lệch trường) ⇒ không bật. Người giữ việc tìm gốc rễ. Lỗi của bộ xét ⇒ revision của B1.
  Gốc rễ là lỗi chập chờn hay khác nền giữa hai lượt ⇒ hỏi chủ kho mã **E3**, mang: quyết định bị đảo (chủ kho chọn "Soạn r2",
  tức làm Đ2, ngày 20-11-2026); bằng chứng (bảng D0, các dòng `LECH_*`, phân tích gốc rễ); hậu quả nếu giữ nguyên (bật thì
  lượt `push` sẽ bỏ đúng những nhóm có thể đỏ ở lượt sau, tức che lỗi chập chờn của nhóm ấy).
- Cần sửa một tệp ngoài write set ⇒ dừng phiên, revision mới; không phải điểm hỏi trừ khi vượt trần (**E2**).

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — đổi job nào chạy ở lượt `push` lên `master`, sửa chốt ghim của bộ đăng ký. Mỗi việc sau mang mã **E5**: chủ
  kho duyệt băm, cấp lease, audit trước merge. Mỗi lần hỏi E5 mang đủ ba thứ của bảng `ADR-0067`: **diff** (đặc tả này hay diff
  PR), **lý do** (bật tái dùng theo `ADR-0068` sau khi điều kiện Q8 đo đạt), và **ai được thêm quyền gì** (không ai được thêm
  quyền; bộ xét của CI được phép làm nhóm job nghỉ ở lượt `push`).

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Ba lớp lỗi từ review lượt 1 và 2 nằm ở đây: chốt ghim bị bỏ sót (F2, N2), quan
sát sau land không kiểm nguồn tái dùng (F8, N3), và thước đo mâu thuẫn với chế độ đang chạy (N1). Đặc tả này liệt kê chốt ghim
theo số dòng, đặt hai chế độ cho `kiem-lai-tai-dung`, và cho D2 đối chứng dương ở chế độ `bat`.

## 8. chua_do_duoc

- Số lượt bóng cần để đủ 20 lượt có tái dùng: tuỳ tỷ lệ merge cây trùng sau #1343; lịch sử 01→15-11 là 25/79.
- Vị trí chốt ghim sau khi B1 (và có thể #1448) land: số dòng ở mục 0 là trên `45bae8d0`.
- Lượt bóng còn artefact bao lâu: theo hạn lưu artefact của kho (mặc định 90 ngày); quá hạn thì lượt ấy là `rc2` ở D0.

## 9. Đo lúc soạn (20-11-2026)

- `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`.
- Số dòng chốt ghim ở mục 0: đo bằng `grep -n` trên bản sao thưa của `45bae8d0`.
- Lease đang giữ write set: ba tệp đầu thuộc `wp1448-r2-g1-claude` (đặc tả B1 r2 mục 9); `.claude/dev/ci_dang_ky_test.py` ⇒
  `NGƯỜI_GIỮ 0` (09:35:51Z–09:39:05Z, 367/367 nhánh). Hai tệp `.ps1` chưa quét; người cấp lease quét đủ sáu đường dẫn ngay
  trước khi cấp.

## 10. Thay đổi so với r1

Theo review lượt 2 (Codex, `changes_requested`, 7 P2, 3 P3):

- N1: `kiem-lai-tai-dung` nay thuộc B2 và có hai chế độ đọc từ artefact (`bong`, `bat`); chế độ `bat` đòi nhóm được đánh dấu
  nghỉ, nhóm còn lại chạy. D2 có đối chứng dương ở chế độ `bat`.
- N3: lệnh tính lại neo vào lượt nguồn đã ghi và so **từng trường**; kiểm đủ tập job của lượt `push`; thiếu dữ liệu ⇒ rc 2;
  thêm `--tu` liệt kê đủ lịch sử bóng; D0 đòi `rc2=0`.
- Điều kiện bật Q8 chuyển từ phụ thuộc cấp lease thành tiêu chí D0 trước merge, vì lệnh đo nó nằm trong chính packet này.
- N2: thêm `TAP_CHO_PHEP`/`y03`, `Y04_IF_JOB_CHE_DO`/`y04`, `y06` (ngoại lệ hẹp), `y07`, `y14` vào danh sách chốt; bước mới
  đặt sau G5 để khỏi đụng `t6` của `ops/cong_cu_test.py`.
- N7: `kiem-tai-dung` nhận `tai_dung_cay` và so với `M^{tree}`; D4 đột biến đúng đầu vào ấy.
- N10: lời hứa về chuỗi lạ thu về đúng phạm vi đo được (producer chuẩn ở B1, lệnh kiểm lại ở D5).
- N8: câu E2, E3, E5 mang đủ thứ phải mang theo.
