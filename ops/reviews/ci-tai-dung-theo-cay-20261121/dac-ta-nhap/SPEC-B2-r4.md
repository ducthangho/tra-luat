# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B2` (revision 4)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B2** · `revision`: **4** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Thay r3 (sha256 `a729dd7c3d931e87e54e293c83415eeda265fa46f063ab8c5bec7798f677a7a7`, review lượt 4
  `changes_requested`), r2 (`17cfb8c2f3c81a918c7960cc83ec0abfda247c4fe36816a4dd448f2bea8ee1e1`) và r1
  (`f705edcff5dfea3a00040361f53a3a694438ababa01dc2fe1f7db400f86e6d77`); cả ba chưa từng được duyệt. Thay đổi so với r3: mục 12.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**). Packet anh em: `CI-TAI-DUNG-THEO-CAY-A`
  r4 (ADR-0068) và `CI-TAI-DUNG-THEO-CAY-B1` r4 (biên nhận, bộ xét hai tầng, chạy bóng).
- **Phụ thuộc để cấp lease:** A đã land và B1 đã land. **Điều kiện bật** (`ADR-0068` Q8) là tiêu chí D0 **trước merge**, đo
  bằng chính lệnh `kiem-lai-tai-dung` của packet này.
- `nguon_cap_viec`: như đặc tả A r4, cộng quyết định *"Vá tiếp"* ngày 20-11-2026 (đặc tả B1 r4).
- `review_class`: **sensitive** — đổi job nào chạy ở lượt `push` lên `master` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, chứa commit land của A và của B1.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (**E5**). Điều kiện merge theo `ADR-0060`; M3
  Windows **`required`** (diff chạm `*.ps1`, `.claude/dev/**`, `.github/workflows/**`): trên máy Windows của chủ kho theo
  `ADR-0057`–`ADR-0059`, BASE và ứng viên cùng máy, chạy `python ops/ci_duong_nhanh_test.py`, `python
  .claude/dev/ci_dang_ky_test.py` (không `--chay`) và `pwsh .claude/dev/chay-cong-windows_test.ps1`.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r4.)

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho, cùng lần duyệt băm đặc tả này (E2 gộp vào lần duyệt E5)
  can_cu: >-
    Ước theo khối ở mục 1 là 485 dòng thêm trên sáu tệp, trong đó 150 là ca và đột biến của lệnh kiểm lại. Không tách được:
    lệnh kiểm lại là thước đo của điều kiện bật (D0) nên phải có trước khi bật, và bật mà không có nó thì không đo được D5.
  tran_cu: "sensitive ≤ 6 tệp và ≤ 450 dòng thêm (ADR-0053)"
  tran_moi: "≤ 6 tệp và ≤ 550 dòng thêm"
```

## 0. Vấn đề và thiết kế

B1 r4 đã ghi, ở mọi lượt `push` lên `master`: tệp bằng chứng có quyết định của hàm thuần `quyet_dinh_tai_dung` cùng mọi đầu vào
thô của nó (thư mục `dau-vao/`), và dòng `TAI_DUNG_AP_DUNG` cho tập nhóm thực sự được dùng. B2 làm ba việc:

1. Lệnh `kiem-lai-tai-dung`: với một lượt `push`, xác thực từng đầu vào thô với nguồn của nó, chạy lại hàm thuần trên đầu vào
   đã lưu, kiểm bảy bất biến đọc thẳng từ `ADR-0068`, và kiểm kết quả job của chính lượt `push` với tập đã đánh dấu. Lệnh này đo
   điều kiện bật Q8 (D0) và quan sát sau land (D5). rc 0 của lệnh **không** thay bốn mốc §10.2.2 mà `ADR-0068` Q6 đòi khi ghi
   `landed`; hồ sơ land vẫn thu bốn mốc ấy cho cả lượt `push` lẫn lượt `pull_request`.
2. Nối output của bộ xét vào điều kiện cấp tám job; hằng `CHE_DO_XET` thành `"bat"`.
3. Job `gate` thêm bước `kiem-tai-dung` tự tính lại phép chứng minh bằng git và in dấu hiệu dương.

**Vì sao thiết kế lệnh kiểm lại đổi ở r4.** Ba revision trước bắt lệnh kiểm lại dựng lại quyết định từ nguồn đổi theo thời
gian, và bốn lượt review đều tìm ra một đường lọt mới ở đúng chỗ ấy (F8, N3, R2–R5, S3–S5). r4 bỏ việc dựng lại: hàm quyết
định là hàm thuần có phiên bản ghim (B1 r4), nên phát lại trên đầu vào đã lưu là phép tất định; việc còn lại là xác thực đầu
vào, phép này so một bản lưu với một nguồn, không cần suy luận về thời điểm.

Bảng bốn nhóm và tám job ở đặc tả B1 r4 mục 0. Chốt đang ghim hình dạng mà B2 đổi (số dòng trên `origin/master` `45bae8d0`;
B1 land trước sẽ dời số, người thi hành đo lại):

- `ops/ci_duong_nhanh_test.py`: `TAP_CHO_PHEP` và `y03` (`:75`, `:2479`), `Y04_IF_JOB_CHE_DO` và `y04` (`:2506`, `:2515`),
  `y06` (job bắt buộc `gate`, `gate-ops`, `gate-packet-loop` không được nghỉ cả job, `BAT_BUOC` `:68`, `:2559`), `y07` (bước bị
  bỏ tự nói lý do, `:2569`), `JOB_CO_IF_CHO_PHEP` và `y11` (`:2844`, `:2849`), `IF_BUOC_CHUAN` và `y12` (`:2620`, `:2859`),
  `y13` (`:2879`), `RUN_BUOC_PACKET` và `y14` (`:2899`, `:2926`), `KHUNG_JOB` (`:2702`). Review lượt 2 đo bằng hàm guard thật:
  chỉ tám điều kiện cấp job đã làm `y04`, `y06`, `y11`, `y13` đỏ; thêm bước ở `gate` làm thêm `y03`, `y07`, `y12`, `y14` đỏ. Review
  lượt 3 và 4 (harness `pins`, gọi guard thật) đo: cập nhật đủ các họ chốt liệt kê ở đây ⇒ 15/15 guard `y*` `DAT`, và
  `loi_gate_nhanh`, `loi_vung_thiet_lap`, `loi_g5_workflow`, `loi_ruff_ci` của bộ đăng ký không lỗi.
- `.claude/dev/ci_dang_ky_test.py`: `BAM_GATE_REGISTRY` (`:836`), `BAM_GATE_NHANH` (`:840`), `G5_MANH_IF` (`:1425`),
  `G5_GOP_IF` (`:1431`), tập `_if_duoc` (`:1454`), nhánh `gate-packet-loop-manh` (`:1523`), nhánh `gate-registry` của
  `_job_if_duoc_phep` (`:594`) và của `loi_g5_workflow` (`:1524-1525`).
- `.claude/dev/chay-cong-windows_test.ps1`: bảng dấu vân `$DauVanCi` (`:1343`, dấu vân gồm `if` cấp job; review lượt 4 đo
  chín dấu vân đổi khi áp đủ B2: tám job của nhóm và `gate`) và ca `t32` (`:1409`): mọi job trừ `chuan-bi` có gương lệnh trong
  `.claude/dev/chay-cong-windows.ps1` hoặc có tên trong dòng `KHÔNG CHẠY`/`THAY BẰNG`.
- `ops/cong_cu_test.py` `t6` khoá các bước của `gate` **trước** bước G5 (`:339`); bước mới đặt **sau** G5 để khỏi sửa tệp ấy.
- `y06` có lý do: job bắt buộc nghỉ cả job thì check bắt buộc đọc như xanh trên PR. Ở lượt `push` lên `master` không có check
  bắt buộc nào. B2 mở một ngoại lệ hẹp đúng vế `tai_dung_bo` cho `gate-ops` và `gate-packet-loop`; mọi điều kiện khác vẫn bị
  `y06` chặn.
- Bảng consumer của `ci.yml` (đặc tả B1 r4 mục 0): B2 chỉ đổi các tệp trong write set; người thi hành chạy lại cột "phép đo"
  của bảng ấy trên `ci.yml` ứng viên (D6).

## 1. write_set

- `.github/workflows/ci.yml`
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.claude/dev/ci_dang_ky_test.py`
- `.claude/dev/chay-cong-windows_test.ps1`
- `.claude/dev/chay-cong-windows.ps1`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set (`ai-dang-giu` trên kho bare khớp máy
chủ), đo ngay trước khi cấp, đủ sáu đường dẫn.

B2 **không** sửa các hàm quyết định của B1: ca ghim `BAM_QUYET_DINH` của B1 đỏ nếu sửa mà giữ phiên bản; tăng phiên bản thì
D0 không đạt được, vì phiên bản mới chưa chạy bóng lượt nào (mục 3.1 i).

Kích thước ước theo khối (dòng thêm):

| khối | tệp | ước |
|---|---|---|
| `kiem-lai-tai-dung`: đọc lượt, dòng áp dụng, artefact, schema theo trạng thái | `ops/ci_duong_nhanh.py` | 35 |
| xác thực đầu vào thô (REST attempt 1, danh sách lượt, zip, log, ảnh, `env`, git, phiên bản, chế độ) | `ops/ci_duong_nhanh.py` | 60 |
| phát lại hàm thuần, bảy bất biến | `ops/ci_duong_nhanh.py` | 35 |
| jobs lượt `push` theo chế độ | `ops/ci_duong_nhanh.py` | 25 |
| lịch sử `--tu`, dòng tổng, băm bảng | `ops/ci_duong_nhanh.py` | 35 |
| `kiem-tai-dung`, output thật, `CHE_DO_XET` | `ops/ci_duong_nhanh.py` | 30 |
| tám điều kiện, bước `gate`, output, biểu thức `ghi-ap-dung` | `.github/workflows/ci.yml` | 22 |
| ca và đột biến của `kiem-lai-tai-dung` (fixture `dau-vao/`, REST giả giữ trạng thái) | `ops/ci_duong_nhanh_test.py` | 150 |
| cập nhật chốt, ca và đột biến khác | `ops/ci_duong_nhanh_test.py` | 60 |
| chốt của bộ đăng ký | `.claude/dev/ci_dang_ky_test.py` | 20 |
| dấu vân Windows, dòng `KHÔNG CHẠY` | hai tệp `.ps1` | 13 |
| **cộng** | | **485** |

Ước 485 vượt trần 450 của `ADR-0053`; khối `nang_tran` xin 550 cùng lần duyệt băm (**E2** gộp vào lần duyệt **E5**).

## 2. ngoai_pham_vi

- Biên nhận, bộ xét, hàm quyết định, bảng nhóm, dạng chuẩn của `tai_dung_bo`, dòng `TAI_DUNG_AP_DUNG`: B1 (B2 chỉ đổi
  `CHE_DO_XET`, thêm output thật và cho biểu thức `bo` của `ghi-ap-dung` theo output ấy).
- Luật: A.
- Lượt `pull_request`, `workflow_dispatch`, Windows CI: không đổi job nào chạy.
- Các bước bên trong tám job: không sửa.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — lệnh `kiem-lai-tai-dung --run <id lượt push>`. Mọi phép đọc jobs của một lượt dùng **attempt 1**
   (`runs/<id>/attempts/1/jobs`, đủ trang). Kết quả mỗi lượt là một dòng
   `KIEM_LAI: run=<id> sha=<M> che_do=<…> phien_ban=<n> quyet_dinh=<…> ap_dung=<tập> rc=<0|1|2> loi=<mã,…>`.
   - a. **Lượt và dòng áp dụng.** REST lượt `push` (attempt 1): sự kiện `push`, nhánh mặc định, `path`
     `.github/workflows/ci.yml`, `status` `completed`. Log job `chuan-bi` attempt 1 có đúng một dòng
     `TAI_DUNG_AP_DUNG: xet=<x> tai=<t> bo=<H>`; H là tập hiệu lực (dạng chuẩn hay rỗng). H khác rỗng mà `x` hay `t` khác
     `success` ⇒ rc 1.
   - b. **Artefact.** `t` bằng `success` ⇒ artefact `bien-nhan-tai-dung` phải đọc được (vắng hay không tải được ⇒ rc 2). `t` khác
     `success` ⇒ artefact có thể vắng. Artefact không đọc được thì `nhom` coi như không có và D (mục g) bằng H.
   - c. **Lượt xét lỗi** (`x` khác `success`): trạng thái `khong_ap_dung`. Không phát lại, không kiểm bất biến (đầu vào có thể dở
     dang). Tập đánh dấu D = tập `nhom` trong artefact nếu có, hợp với H (H rỗng theo biểu thức). Chỉ kiểm phép (g) trên D. Đếm
     vào `xet_loi`.
   - d. **Schema theo trạng thái** (khi `x` bằng `success`). Mọi trạng thái: `phien_ban` 2, `che_do_xet`,
     `phien_ban_quyet_dinh`, `run_id` bằng id lượt, `run_attempt` 1, `quyet_dinh`, `nhom`, `ly_do`, M, `before`. `tai_dung` ⇔
     `nhom` khác rỗng; `khong_xet` và `khong_tai_dung` ⇒ `nhom` rỗng. Trường của lượt nguồn: có giá trị khi có nguồn, `null` khi
     `ly_do` cho biết không có nguồn. `t` bằng `success` ⇒ H bằng dạng chuẩn của `nhom`. `che_do_xet` bằng hằng `CHE_DO_XET`
     trong `ops/ci_duong_nhanh.py` tại M; `phien_ban_quyet_dinh` bằng hằng `PHIEN_BAN_QUYET_DINH` tại M (đọc bằng `git show`).
     Vi phạm ⇒ rc 1 (`sai`).
   - e. **Xác thực đầu vào thô** (khi `x` bằng `success`). Mỗi đầu vào trong `dau-vao/` so với nguồn của nó; lệch ⇒ rc 1 (`sai`),
     không đọc được nguồn ⇒ rc 2:
     - phản hồi REST của lượt nguồn: đọc lại `runs/<id>/attempts/1` và jobs attempt 1, các trường hàm thuần dùng bằng bản lưu;
     - danh sách lượt `pull_request` cho P2, lưu lúc t0: đọc lại danh sách; mọi lượt có `created_at` ≤ t0 phải có trong bản lưu; lượt
       bản lưu ghi chưa `completed` thì jobs attempt 1 của nó không được có job xong trước t0;
     - zip biên nhận lưu nguyên byte: sha256 bằng bản ghi, bằng sha256 của zip tải lại từ lượt nguồn;
     - dòng log đã lưu: đọc lại log job ấy (attempt 1), dòng ở số dòng ấy bằng nguyên văn;
     - ảnh runner: bằng các dòng `Runner Image` trong log `Set up job` của job `chuan-bi` hai lượt (dạng dòng do B1 C5 ghi);
     - giá trị môi trường đã lưu (`before`, `che_do`, `GITHUB_REF`): bằng khối `env:` mà Actions in ở đầu bước xét trong log
       `chuan-bi` của lượt `push` (dạng đo ở D4);
     - sự kiện git: tính lại từ SHA bằng git.
   - f. **Phát lại và bất biến** (khi `x` bằng `success` và (e) đạt). Nếu `phien_ban_quyet_dinh` bằng hằng của head đang chạy
     lệnh: chạy `quyet_dinh_tai_dung` trên `dau-vao/` đã lưu, `(quyet_dinh, nhom, ly_do)` phải bằng bản ghi (`ly_do` so như tập);
     khác ⇒ rc 1 (`lech_ham`). Khác phiên bản ⇒ không phát lại, ghi `phien_ban_khac`. Bất kể phiên bản, bảy bất biến đọc thẳng từ
     `ADR-0068` trên đầu vào đã xác thực, không qua hàm quyết định; vi phạm ⇒ rc 1 (`sai`):
     - I1 (`tai_dung` ⇔ tập khác rỗng): đã ở (d);
     - I2 (Q1, Q2): tập khác rỗng ⇒ M có đúng hai cha `[P1, P2]` và `before` bằng P1;
     - I3 (Q2): object lấy từ bundle có SHA bằng `sha` và `github_sha` của biên nhận, cha `[P1, P2]`, cây bằng `M^{tree}`, và `<h>`
       của dòng `HEAD is now at` là tiền tố SHA ấy; `git merge-tree --write-tree P1 P2` ra `M^{tree}`;
     - I4 (Q3): lượt nguồn thuộc chính kho, `path` đúng, `conclusion` `success`, `run_attempt` 1; ảnh hai job `chuan-bi` bằng nhau;
     - I5 (Q3): mỗi nhóm trong tập có đủ tập chỉ số ma trận ở lượt nguồn, mọi job `success`;
     - I6 (Q4, G1): blob `ci.yml` của object bằng `ci_yml_blob` và bằng blob tại M;
     - I7 (Q7): `nhanh` trong tập ⇒ hai diff khác `None` và hai kế hoạch bằng nhau, tính lại bằng `doc_diff`, `ke_hoach`,
       `doc_bien_manh` của `.claude/dev/ci_dang_ky_test.py` **tại M**.
   - g. **Jobs của chính lượt `push`.** Tập đánh dấu D = `nhom` ghi trong artefact hợp với H. Chế độ `bong`: mọi nhóm trong D có
     đủ tập chỉ số và mọi job `success`; khác ⇒ in `VI_PHAM_Q8: <nhóm> <job> <kết luận>`, rc 1. Chế độ `bat`: mỗi job của nhóm
     trong H ở **hình dạng REST của job nghỉ cấp job** (đo ở D4, không suy từ bảng ma trận) với kết luận `skipped`, khác ⇒
     `LECH_BAT: …`, rc 1; nhóm trong D mà không trong H kiểm như chế độ `bong`. Nhóm ngoài D: không kiểm.
   - h. **rc.** Phép (g) luôn chạy khi đọc được jobs của lượt `push`, kể cả khi phép trước đó lỗi. 2 khi một nguồn cần cho phép đang áp dụng không đọc được (mạng, 404, hết hạn, log vắng dòng
     `TAI_DUNG_AP_DUNG`); 1 khi đọc được mà sai; 0 khi mọi phép áp dụng đạt. Danh sách job của lượt `push` rỗng ⇒ rc 2. Lượt
     có cả lỗi rc 1 và rc 2 ⇒ rc 1, `loi` liệt kê đủ.
   - i. **`kiem-lai-tai-dung --tu <commit land của B1>`.** Ghi thời điểm cắt t_cat (UTC). Liệt kê **mọi** lượt `ci.yml` sự
     kiện `push` trên nhánh mặc định có `created_at` ≤ t_cat và `head_sha` nhận commit ấy làm tổ tiên (`git merge-base
     --is-ancestor`), đủ trang. Mỗi lượt đúng một dòng `KIEM_LAI`. Bảng in kèm sha256 của chính nó. Dòng tổng:
     `Q8: tai_dung=<a> · vi_pham=<b> · sai=<c> · lech_ham=<d> · rc2=<e> · xet_loi=<f> · phien_ban=<v> · tong=<n> · tu=<id đầu>..<id cuối> · cat=<t_cat>`,
     với v là `PHIEN_BAN_QUYET_DINH` của head đang chạy lệnh, và:
     - a: số lượt phiên bản v có H khác rỗng, H bằng dạng chuẩn của `nhom`, rc 0 — đếm lượt có nhóm **đã xác minh**, không đếm nhãn;
     - b: số lượt có `VI_PHAM_Q8`, **toàn bảng**;
     - c: số lượt phiên bản v có `sai`;
     - d: số lượt phiên bản v có `lech_ham`;
     - e: số lượt rc 2, **toàn bảng**;
     - f: số lượt xét lỗi, để báo.

     Không có cửa sổ trượt: b và e tính trên mọi lượt từ commit land của B1, vì Q8 nói "không lượt nào". a, c, d tính trên lượt
     phiên bản v, vì chúng hỏi về đúng hàm sắp bật; một lượt phiên bản khác có `sai` vẫn được in trong bảng. Mất artefact hay
     log của một lượt làm lượt ấy rc 2 và không bao giờ làm một số đếm giảm.
2. `ops/ci_duong_nhanh.py` + `.github/workflows/ci.yml` — job `chuan-bi`: `CHE_DO_XET` thành `"bat"`; thêm output
   `tai_dung_bo`, `tai_dung_run`, `tai_dung_cha`, `tai_dung_cay` (từ bước xét của B1), cùng điều kiện như output bóng: chỉ mang
   giá trị khi bước xét và bước tải bằng chứng cùng `outcome == 'success'`, khác thì chuỗi rỗng; giữ các output `*_bong`. Biểu
   thức `bo` của bước `ghi-ap-dung` bằng đúng biểu thức của output `tai_dung_bo`.
3. `.github/workflows/ci.yml` — tám job của bốn nhóm: điều kiện cấp job thêm vế
   `!contains(needs.chuan-bi.outputs.tai_dung_bo, ',<nhóm>,')`, nối bằng `&&` vào điều kiện đang có, hoặc là điều kiện duy
   nhất nếu job chưa có. Chỉ chuỗi chứa đúng `,<nhóm>,` mới làm nhóm nghỉ; bộ xét của B1 chỉ phát dạng chuẩn, và (d) bắt mọi
   lệch giữa H và dạng chuẩn của `nhom`.
4. `.github/workflows/ci.yml` + `ops/ci_duong_nhanh.py` — job `gate`: bước mới **sau** bước G5, `if:` đúng
   `needs.chuan-bi.outputs.tai_dung_bo != ''`, chạy lệnh `kiem-tai-dung` với `tai_dung_bo`, `tai_dung_run`, `tai_dung_cha`,
   `tai_dung_cay` và `github.sha`: M có đúng hai cha bằng `tai_dung_cha`; `M^{tree}` bằng `tai_dung_cay` và bằng
   `git merge-tree --write-tree P1 P2`; in `TAI_DUNG: DAT run=<id> cay=<tree> cha=<P1>,<P2> nhom=<danh sách>`; lệch hay thiếu ⇒
   rc ≠ 0. Các bước khác của `gate` giữ nguyên điều kiện.
5. `ops/ci_duong_nhanh_test.py` — cập nhật chốt ở mục 0 (gồm ngoại lệ hẹp của `y06`); ca và đột biến theo mục 4; ca canh "tập
   job mang vế `tai_dung_bo` đúng bằng tám job của bảng nhóm; `gate`, `chuan-bi`, `bien-nhan-cay` không mang"; ca canh biểu
   thức `bo` của `ghi-ap-dung` bằng biểu thức output `tai_dung_bo`.
6. `.claude/dev/ci_dang_ky_test.py` — cập nhật các chốt ở mục 0 cho điều kiện mới, sau khi rà hành vi; giữ nguyên mọi chốt
   khác.
7. `.claude/dev/chay-cong-windows_test.ps1` — cập nhật `$DauVanCi` cho chín job có dấu vân đổi.
8. `.claude/dev/chay-cong-windows.ps1` — bước `kiem-tai-dung` của `gate` có dòng `KHÔNG CHẠY` kèm lý do (chỉ có nghĩa ở lượt
   `push` lên `master` của CI), để `t32` xanh.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| D0 | **Trước merge**, điều kiện bật `ADR-0068` Q8: `kiem-lai-tai-dung --tu <commit land của B1>` chạy trên head ứng viên in dòng tổng với a ≥ 20, b = 0, c = 0, d = 0, e = 0. Bảng đầy đủ và sha256 của nó đính vào handoff | a < 20; b, c, d hay e > 0 | các đột biến lịch sử ở D2 |
| D1 | Trên Ubuntu (CI của PR): `python ops/ci_duong_nhanh_test.py` (job `gate-ops`) và `python .claude/dev/ci_dang_ky_test.py --chay` (job `gate-registry`) in dòng tổng `N/N` hai số bằng nhau, rc 0. Trên máy Windows của chủ kho (`ADR-0060` M3, BASE và ứng viên): ba lệnh ở đầu tệp, mỗi lệnh có dòng tổng hai số bằng nhau và rc 0 | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở D2 |
| D2 | Đột biến riêng, mỗi cái chết đúng ca của nó (bộ phân hạng của tệp test). Mỗi ca dựng `dau-vao/` và REST giả **giữ trạng thái** rồi gọi lệnh thật. Bảng ở ngay dưới | một đột biến sống, hay chết vì lý do khác chốt | chính bảng ấy |
| D3 | `actionlint` trên `ci.yml` không thêm finding so với BASE (delta 0, cùng nền có `shellcheck`) | thêm finding | — |
| D4 | Trước land, trên dữ liệu thật, ba phép: (i) lấy một lượt bóng có H khác rỗng và `kiem-lai-tai-dung` rc 0 (ghi id, SHA); trên một workflow đo tạm `do-ci/**`, chạy bước `kiem-tai-dung` với các output ghi trong artefact của lượt ấy ⇒ in `TAI_DUNG: DAT` với đúng run nguồn; đổi đầu vào `tai_dung_cay` thành một cây khác ⇒ rc ≠ 0; đổi `tai_dung_cha` ⇒ rc ≠ 0. (ii) trên một workflow đo tạm có một job ma trận và một job thường cùng nghỉ ở cấp job bằng đúng dạng điều kiện của mục tiêu 3, đọc REST `runs/<id>/attempts/1/jobs`; lưu nguyên phản hồi làm fixture của ca chế độ `bat`. (iii) từ log thật của một lượt bóng: lưu khối `env:` ở đầu bước xét và các dòng `Runner Image` làm fixture của phép (e) | `TAI_DUNG: DAT` vắng; một trong hai đầu vào sửa vẫn rc 0; thiếu một trong ba fixture thật | hai đầu vào sửa ở (i) |
| D5 | Sau land (**chưa đo được** tới lúc ấy): mười lượt `push` lên `master` đầu tiên sau commit land của B2, chọn theo `created_at`, ghi id và SHA trước khi đọc kết quả. Với mỗi lượt: `kiem-lai-tai-dung --run <id>` (chế độ `bat`) rc 0; lượt có H khác rỗng thì `gate` có dòng `TAI_DUNG: DAT`. Ghi số lượt theo từng H | `kiem-lai-tai-dung` rc ≠ 0 trên một lượt; thiếu `TAI_DUNG: DAT` khi H khác rỗng | răng của `kiem-lai-tai-dung` ở D2 |
| D6 | Trước khi giao review: chạy cột "phép đo" của bảng consumer (đặc tả B1 r4 mục 0) trên `ci.yml` ứng viên; mọi dòng ra như bảng | một consumer ngoài write set đỏ | — (răng ở các ca của từng consumer) |

D5 không đòi có lượt tái dùng trong mười lượt; không có thì ghi "chưa quan sát được tái dùng", không phải đạt.

**Bảng đột biến D2.** Cột "kỳ vọng" là kết quả của lệnh trên fixture; mỗi dòng là một ca và một đột biến làm ca ấy đổi màu.

| # | fixture (một lượt, trừ khi ghi) | kỳ vọng |
|---|---|---|
| 1 | log `chuan-bi` vắng dòng `TAI_DUNG_AP_DUNG` | rc 2 |
| 2 | `t` `success`, artefact vắng | rc 2 |
| 3 | `t` `failure`, artefact vắng, mọi nhóm chạy `success` | rc 0, `khong_ap_dung` (đối chứng dương) |
| 4 | `x` `failure` sau khi đã ghi `tai_dung` `{ops}`; `t` `success`; H rỗng; chế độ `bat`; mọi nhóm chạy `success` | rc 0, `khong_ap_dung` (đối chứng dương, review lượt 4 S5) |
| 5 | như 4 nhưng một job `ops` `failure` | rc 1, `VI_PHAM_Q8` |
| 6 | H khác rỗng mà `x` `failure` | rc 1 |
| 7 | `tai_dung` với `nhom` rỗng | rc 1 (`sai`, I1) |
| 8 | `khong_tai_dung` với `nhom` khác rỗng | rc 1 (`sai`, I1) |
| 9 | `x`, `t` `success`, H khác dạng chuẩn của `nhom` | rc 1 (`sai`) |
| 10 | hai kế hoạch registry khác nhau, ghi trung thực cả hai, `nhom` có `nhanh` (fixture rename của review lượt 1) | rc 1 (`sai` I7 và `lech_ham`) |
| 11 | phản hồi jobs nguồn đã lưu khác jobs attempt 1 đọc lại | rc 1 (`sai`) |
| 12 | danh sách lượt PR đã lưu thiếu một lượt có `created_at` ≤ t0 | rc 1 (`sai`) |
| 13 | lượt PR lưu `in_progress` mà jobs attempt 1 xong trước t0 | rc 1 (`sai`) |
| 14 | sha256 zip đã lưu khác zip tải lại | rc 1 (`sai`) |
| 15 | dòng log đã lưu khác log đọc lại | rc 1 (`sai`) |
| 16 | ảnh đã lưu khác dòng `Runner Image` | rc 1 (`sai`) |
| 17 | `before` đã lưu khác khối `env:` của bước xét | rc 1 (`sai`) |
| 18 | `phien_ban_quyet_dinh` khác hằng tại M | rc 1 (`sai`) |
| 19 | `che_do_xet` khác hằng `CHE_DO_XET` tại M | rc 1 (`sai`) |
| 20 | object bundle một cha, tiêu đề `Merge <P2> into <P1>` | rc 1 (`sai`, I3) |
| 21 | đuôi `sha` của biên nhận đổi, tiền tố giữ nguyên | rc 1 (`sai`, I3) |
| 22 | blob `ci.yml` của object khác blob tại M | rc 1 (`sai`, I6) |
| 23 | đột biến hàm thuần (cùng phiên bản) trả nhóm khác | rc 1 (`lech_ham`) |
| 24 | lượt phiên bản khác v | không phát lại, `phien_ban_khac`; không vào a, c, d |
| 25 | chế độ `bong`, một job của nhóm trong D `failure` | rc 1, `VI_PHAM_Q8` |
| 26 | attempt 1 có job nhóm `failure`, attempt 2 xanh | rc 1, `VI_PHAM_Q8` |
| 27 | chế độ `bat`, một job của nhóm trong H đã chạy | rc 1, `LECH_BAT` |
| 28 | chế độ `bat`, đúng theo fixture REST thật của D4 (ii) | rc 0 (đối chứng dương) |
| 29 | chế độ `bat`, làn `duong_nhanh`, `khong_xet` | rc 0 (đối chứng dương) |
| 30 | merge một cha; `before` khác P1; không nguồn hợp lệ; ảnh khác — bốn fixture | rc 0, phát lại bằng bản ghi (bốn đối chứng dương) |
| 31 | lỗi mạng khi đọc lại một nguồn | rc 2 |
| 32 | lịch sử: lượt 0 đánh dấu `ops` và đỏ; lượt 1–20 tốt | b = 1, D0 không đạt |
| 33 | như 32 nhưng artefact lượt 0 mất (`t` `success`) | e = 1 và b = 1 (H còn trong log), D0 không đạt (review lượt 4 S3) |
| 34 | như 33 nhưng cả log lượt 0 cũng mất | e = 1, D0 không đạt |
| 35 | 20 lượt tốt phiên bản 1, rồi 5 lượt tốt phiên bản 2; head phiên bản 2 | a = 5, D0 không đạt |
| 36 | 20 lượt nhãn `tai_dung` mà `t` `failure` (H rỗng) | a = 0 |
| 37 | đột biến `--tu` chỉ đọc trang đầu (fixture 120 lượt) | `tong` khác số lượt fixture, ca đỏ |
| 38–48 | điều kiện cấp job: bỏ vế khỏi từng job trong tám job; thêm vế vào `gate`; đổi `',ops,'` thành `'ops'`; mở ngoại lệ `y06` cho một điều kiện khác | ca canh tương ứng đỏ |
| 49–51 | `kiem-tai-dung`: cha lệch; `tai_dung_cay` lệch với `M^{tree}`; `merge-tree` ra cây khác | rc ≠ 0 |
| 52 | biểu thức `bo` của `ghi-ap-dung` khác biểu thức output `tai_dung_bo` | ca canh đỏ |

Bảng năm vế L6: D0 và D1 khớp dòng tổng do máy in một dòng (vế âm: rc ≠ 0, a < 20, một số đếm khác 0); (b), (d) không áp dụng
(một dòng, chữ số); (c) đếm theo từng đột biến ở D2; (e) không có lời khai "0 cổng". Dòng `TAI_DUNG: DAT`: tiền tố cố định do mã
in, nội dung kiểm lại bằng `kiem-lai-tai-dung`.

## 5. luat_dung

- Trần kích thước: trần của khối `nang_tran` (550 dòng thêm) nếu chủ kho duyệt băm đặc tả này, không thì 450 của `ADR-0053`;
  ước theo bảng ở mục 1. Người thi hành đo `git diff --numstat` khi xong; vượt trần đang áp ⇒ dừng và hỏi chủ kho mã **E2**,
  mang `git diff --numstat` từng tệp, khối nào vượt ước, trần đang áp và trần xin, lý do không tách được.
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã dùng, finding còn mở
  và số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Thiếu một trong hai phụ thuộc cấp lease ⇒ không cấp lease (không phải điểm hỏi).
- D0 có a < 20 và mọi số đếm khác bằng 0 ⇒ giữ PR chưa merge, đo lại khi có thêm lượt bóng (không phải điểm hỏi).
- D0 có e > 0: nguồn còn đọc được (lỗi mạng) ⇒ đo lại. Nguồn mất vĩnh viễn (artefact hay log hết hạn, hay không bao giờ có) ⇒
  hỏi chủ kho mã **E1** (đường cụt theo Q8 với lịch sử này), mang đủ ba thứ của bảng `ADR-0067`: **gốc rễ** (các lượt rc 2
  cùng nguyên nhân mất nguồn, bảng D0 và sha256); **các phương án đã thử và vì sao hỏng** (đọc lại nguồn, tìm bản lưu khác);
  **một đề xuất** (sửa luật A để định nghĩa điều kiện mở lịch sử mới, tức revision `ADR-0068` qua duyệt E5, hay dừng Đ2).
- D0 có b > 0 ⇒ không bật; Q8 không cho bật với lịch sử này kể cả sau khi sửa bộ xét. Người giữ việc tìm gốc rễ rồi hỏi chủ kho
  mã **E1**, mang: **gốc rễ** (lỗi bộ xét, hay lỗi chập chờn của nhóm mà bộ xét không thấy được; kèm bảng D0 và các dòng
  `VI_PHAM_Q8`); **các phương án đã thử và vì sao hỏng**; **một đề xuất** (sửa bộ xét rồi sửa luật A để mở lịch sử mới, hay dừng
  Đ2). Nếu gốc rễ là lỗi chập chờn của chính nhóm, câu hỏi mang thêm mã **E3**: **quyết định** bị mâu thuẫn ("Soạn r2" và
  "Vá tiếp", 20-11-2026, tức làm Đ2); **bằng chứng** (như trên); **hậu quả nếu giữ nguyên** (bật thì lượt `push` bỏ đúng nhóm có
  thể đỏ ở lượt sau, tức che lỗi chập chờn của nhóm ấy).
- D0 có c > 0 hay d > 0 ⇒ không bật. Lỗi của lệnh kiểm lại ⇒ sửa trong packet này rồi đo lại. Lỗi của bộ xét hay hàm quyết định
  ⇒ revision của B1 (tăng `PHIEN_BAN_QUYET_DINH`; phép đếm a bắt đầu lại cho phiên bản mới, b và e của lịch sử giữ nguyên).
  Không phải điểm hỏi, trừ khi cùng một hình dạng lỗi lặp lại sau khi đã thiết kế lại ⇒ **E1**, mang: **gốc rễ** (kèm các lần
  lặp); **các phương án đã thử và vì sao hỏng**; **một đề xuất**.
- Lượt sớm nhất của lịch sử còn 14 ngày hay ít hơn tới hạn lưu 90 ngày (artefact và log) mà D0 chưa đạt ⇒ hỏi chủ kho mã **E2**
  (giới hạn hạn lưu), mang: **mức đã dùng** (số ngày đã qua của hạn lưu, ngày hết hạn của lượt sớm nhất); **còn thiếu bao
  nhiêu** (20 − a lượt, ước số ngày theo số lượt bóng trung bình mỗi ngày); **để làm gì** (giữ lịch sử đo được cho D0, bằng một
  packet riêng lưu bảng D0 cùng `dau-vao/` thành bằng chứng bền).
- Cần sửa một tệp ngoài write set ⇒ dừng phiên, revision mới; không phải điểm hỏi trừ khi vượt trần (**E2**).

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — đổi job nào chạy ở lượt `push` lên `master`, sửa chốt ghim của bộ đăng ký. Mỗi việc sau mang mã **E5**: chủ
  kho duyệt băm, cấp lease, audit trước merge. Mỗi lần hỏi E5 mang đủ ba thứ của bảng `ADR-0067`: **diff** (đặc tả này hay diff
  PR), **lý do** (bật tái dùng theo `ADR-0068` sau khi điều kiện Q8 đo đạt), và **ai được thêm quyền gì** (không ai được thêm
  quyền; bộ xét của CI được phép làm nhóm job nghỉ ở lượt `push`).

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Ba hình dạng lặp qua bốn lượt review và cách r4 xử lý:

| hình dạng | lần | cách xử lý ở r4 |
|---|---|---|
| chốt ghim hay consumer bị bỏ sót | 4 (F2, N2, R1, S1) | danh sách chốt theo số dòng ở mục 0; bảng consumer của B1 r4 và D6 |
| danh tính lượt PR | 3 (F4, R5, S2) | B1 r4: object từ bundle; ở đây I3, I6 kiểm lại |
| hợp đồng kiểm lại chưa kín | 4 (F8, N3, R2–R5, S3–S5) | đổi thiết kế gốc (mục 0): không dựng lại quyết định từ nguồn đổi theo thời gian; phát lại hàm thuần trên đầu vào đã lưu, xác thực từng đầu vào, bảy bất biến độc lập với hàm, tập hiệu lực đọc từ dòng do biểu thức Actions in, lịch sử không có cửa sổ trượt |

## 8. chua_do_duoc

- Hình dạng REST của job nghỉ cấp job; dạng khối `env:` và dòng `Runner Image` trong log: D4 đo.
- Số lượt bóng cần để a đạt 20: tuỳ tỷ lệ merge cây trùng sau #1343; lịch sử 01→15-11 là 25/79.
- Vị trí chốt ghim sau khi B1 (và có thể #1448) land: số dòng ở mục 0 là trên `45bae8d0`.
- Hạn lưu artefact và log của kho: đặc tả B1 r4 đặt `retention-days: 90` cho hai artefact; hạn lưu log theo cài đặt kho, chưa
  đo trong lần soạn này.

## 9. Đo lúc soạn (20-11-2026)

- `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`.
- Số dòng chốt ghim ở mục 0: đo bằng `grep -n` trên bản sao thưa của `45bae8d0`.
- Lease đang giữ write set: ba tệp đầu thuộc `wp1448-r2-g1-claude` (đặc tả B1 r4 mục 9); `.claude/dev/ci_dang_ky_test.py` ⇒
  `NGƯỜI_GIỮ 0` (09:35:51Z–09:39:05Z, 367/367 nhánh). Hai tệp `.ps1` chưa quét; người cấp lease quét đủ sáu đường dẫn ngay
  trước khi cấp.

## 10. Thay đổi so với r1

Xem đặc tả r3 mục 10.

## 11. Thay đổi so với r2

Xem đặc tả r3 mục 11.

## 12. Thay đổi so với r3

Theo review lượt 4 (Codex, `changes_requested`, 5 P2, 2 P3; A r4 đạt):

- Hợp đồng kiểm lại hỏng bốn lượt liền cùng một hình dạng ⇒ đổi thiết kế gốc cùng B1 r4: phát lại hàm thuần trên `dau-vao/`
  đã lưu, xác thực từng đầu vào với nguồn, bảy bất biến I1–I7 đọc thẳng từ `ADR-0068`.
- S3: bỏ cửa sổ trượt. Vi phạm Q8 và lượt rc 2 tính trên toàn lịch sử; mất artefact hay log chỉ làm lượt thành rc 2, không xoá
  vi phạm (ca 33, 34). Phép đếm a và hai phép c, d tính trên phiên bản hàm quyết định đang bật. Thêm điểm hỏi E1 khi nguồn mất
  vĩnh viễn hay có vi phạm, E2 khi lịch sử sắp quá hạn lưu.
- S4: phát lại so `(quyet_dinh, nhom, ly_do)`; schema theo trạng thái; I1 (`tai_dung` ⇔ tập khác rỗng); a đếm lượt có nhóm đã
  xác minh, không đếm nhãn (ca 7–10, 36). Lý do của `khong_xet`, `khong_tai_dung` được kiểm bằng phát lại trên đầu vào đã xác
  thực, gồm REST và ảnh.
- S5: tập hiệu lực đọc từ dòng `TAI_DUNG_AP_DUNG`; lượt xét lỗi thành `khong_ap_dung` (ca 3, 4); vẫn giữ kiểm Q8 bảo thủ trên tập
  đã ghi (ca 5).
- S2: I3, I6 kiểm object từ bundle, đuôi SHA, commit một cha (ca 20–22).
- S7: một con số ước duy nhất (bảng mục 1, 485), khối `nang_tran` xin 550.
- Thêm D6 (consumer) và D4 (iii) (fixture log thật).
