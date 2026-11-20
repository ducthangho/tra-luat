# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B1` (revision 4)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B1** · `revision`: **4** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Thay r3 (sha256 `814dfccaafcfed524fdaa733c94dfac3e6b1abd88a97b729005c18e4a2b6cb46`, review lượt 4
  `changes_requested`), r2 (`940f6a2e307ada5807d9a8b4f0ad204cd155d1e8f898f7c53ab8e63a0783e677`) và r1
  (`fd24105a394ea8a4a020c3f3af08964a82d4a8c81658991f6acfff8e3512ebf2`); cả ba chưa từng được duyệt. Cùng
  `CI-TAI-DUNG-THEO-CAY-B2` thay packet `CI-TAI-DUNG-THEO-CAY-B` (r1 `57ccbf1d…`, r2 `587e59cf…`). Thay đổi so với r3: mục 11.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**). Packet anh em:
  `CI-TAI-DUNG-THEO-CAY-A` r4 (ADR-0068) và `CI-TAI-DUNG-THEO-CAY-B2` r4 (kiểm lại và bật). B1 **không** phụ thuộc A: B1
  không đổi job nào chạy hay không. B2 phụ thuộc A và B1.
- `nguon_cap_viec`: như đặc tả A r4, cộng quyết định chủ kho ngày 20-11-2026 qua phiên điều phối
  (`local_cb926020-5197-4d05-9c66-1cdadb7f4591`), nguyên văn *"Vá tiếp"*, trả lời câu hỏi E1 "hoãn Đ2 hay vá tiếp" sau review
  lượt 4.
- `review_class`: **sensitive** — sửa `.github/workflows/ci.yml` (thêm quyền `actions: read`, thêm một job) và bộ phân loại
  của CI (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (**E5**). Điều kiện merge theo `ADR-0060`; M3
  Windows **`required`** (diff chạm `*.ps1`, `.claude/dev/**`, `.github/workflows/**`): trên máy Windows của chủ kho theo
  `ADR-0057`, `ADR-0058`, `ADR-0059`, BASE và ứng viên cùng máy, chạy `python ops/ci_duong_nhanh_test.py` và `pwsh
  .claude/dev/chay-cong-windows_test.ps1`. Bộ thứ nhất không có lượt Windows trong CI (`.github/workflows/ci.yml:761`).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r4.)

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho, cùng lần duyệt băm đặc tả này (E2 gộp vào lần duyệt E5)
  can_cu: >-
    Ước theo khối ở mục 1 là 600 dòng thêm trên năm tệp. Không tách được: biên nhận lượt PR, gói commit merge, bộ xét lượt
    push và tệp bằng chứng lưu đầu vào thô dùng chung một định dạng, một bảng nhóm và một hàm quyết định; tách thì packet sau
    phải sửa lại định dạng của packet trước, và giai đoạn bóng chỉ bắt đầu khi cả hai đã land. Hai tệp `.ps1` vào write set vì
    bản gương Windows duyệt mọi job trừ `chuan-bi`. Tham chiếu numstat: #674 (7e5958e) +618 dòng mã, +3608 dòng test; #1343
    (b8bc64f) +226 dòng.
  tran_cu: "sensitive ≤ 6 tệp và ≤ 450 dòng thêm (ADR-0053)"
  tran_moi: "≤ 6 tệp và ≤ 650 dòng thêm"
```

## 0. Vấn đề và thiết kế

Mục 0 của đặc tả A r4 có số đo. B1 dựng biên nhận ở lượt `pull_request` và bộ xét ở lượt `push` lên `master`, nhưng **chỉ
chạy bóng**: bộ xét tính và ghi lại nhóm nào tái dùng được, rồi lượt `push` vẫn chạy đủ như hiện nay. Lệnh kiểm lại độc lập
(`kiem-lai-tai-dung`) và việc bỏ job thuộc B2. Số dòng dưới đây đo trên `origin/master` `45bae8d0`.

**Mô hình tin cậy.** Biên nhận do chính mã của cây đang test tạo ra; cây ấy bằng cây của M, tức bằng mã sẽ nằm trên `master`.
Nên biên nhận đáng tin đúng bằng mã trên `master`. Các phép dưới đây nhắm lỗi (của bộ xét, của dữ liệu, của mạng) và lời khai
không khớp thực tế, không nhắm một `ci.yml` cố ý gian lận đã được merge.

**Bộ xét hai tầng, để kiểm lại được.** Bốn lượt review đã tìm lỗ ở hợp đồng kiểm lại, lần nào cũng cùng một gốc: lệnh kiểm
lại phải dựng lại quyết định từ những nguồn đổi theo thời gian (danh sách lượt REST, trạng thái lượt, artefact hết hạn). B1 r4
đổi thiết kế để gốc ấy biến mất:

- **Tầng thu** gọi REST, git, tải artefact, đọc log, và ghi **nguyên văn** mọi thứ đã đọc vào thư mục `dau-vao/` của tệp
  bằng chứng (URL, thời điểm UTC, mã HTTP, thân phản hồi; zip biên nhận nguyên byte; dòng log kèm id job và số dòng).
- **Tầng quyết định** là một hàm thuần `quyet_dinh_tai_dung(dau_vao)` chỉ đọc các đầu vào thô ấy (cộng các sự kiện git suy từ
  SHA, vốn bất biến), trả `(quyet_dinh, nhom, ly_do)`. Hằng `PHIEN_BAN_QUYET_DINH` trong `ops/ci_duong_nhanh.py` đánh số phiên
  bản hàm; một ca ghim sha256 mã nguồn của các hàm quyết định với hằng ấy, nên đổi logic mà không tăng phiên bản thì ca đỏ.
- Sau khi ghi, bộ xét **đọc lại** thư mục `dau-vao/` từ đĩa, chạy lại hàm thuần, và đòi kết quả bằng quyết định vừa tính; khác
  thì bước xét rc ≠ 0 (output bóng rỗng theo điều kiện `outcome`).

Lệnh kiểm lại của B2 nhờ đó chỉ còn hai việc: xác thực từng đầu vào thô với nguồn của nó (dữ liệu attempt 1 của một lượt
đã xong, log, zip và git không đổi; danh sách lượt thì có luật nhất quán riêng ở B2), và chạy lại đúng hàm thuần trên đầu
vào đã lưu, tức phép lặp lại tất định.

**Dòng áp dụng.** Tập nhóm thực sự được dùng (ở B1 là output bóng; ở B2 là output điều khiển job) do biểu thức Actions quyết
định từ `outcome` của hai bước, không do bộ xét. Một bước thứ năm của `chuan-bi`, `if: always()` ở lượt `push`, in dòng
`TAI_DUNG_AP_DUNG: xet=<outcome> tai=<outcome> bo=<tập hiệu lực>`, ba giá trị lấy từ biểu thức qua `env`. Lệnh kiểm lại của B2
đọc tập hiệu lực từ dòng này thay vì suy từ artefact (review lượt 4, S5).

Ràng buộc đo được:

- **Danh tính lượt PR** (review lượt 3 R5, lượt 4 S2). Commit merge tổng hợp của lượt PR không đọc lại được sau khi PR đóng,
  và dòng `HEAD is now at <h> Merge <P2> into <P1>` của `actions/checkout` chỉ cho SHA rút gọn và **tiêu đề** commit (một commit
  một cha cũng có thể mang tiêu đề ấy). Nên job biên nhận tải lên **git bundle** chứa đúng commit đang checkout
  (`git bundle create … HEAD ^HEAD^1 ^HEAD^2`). Bộ xét lấy object từ bundle; SHA của object là băm của chính nội dung (cây,
  cha, thông điệp), nên cha và cây đọc từ object là của commit có SHA ấy. Dòng `HEAD is now at` trong log `chuan-bi` lượt PR
  (attempt 1) còn được dùng để buộc SHA ấy với lần checkout thật: `<h>` phải là tiền tố của SHA object.
- **Định nghĩa workflow nguồn.** Với sự kiện `pull_request`, Actions chạy `.github/workflows/ci.yml` tại commit merge tổng hợp
  (`GITHUB_SHA`). Biên nhận ghi `GITHUB_SHA` và blob OID của `ci.yml` tại `HEAD`; bộ xét đòi `GITHUB_SHA` bằng SHA object, blob
  đọc từ object bằng blob ghi trong biên nhận và bằng blob tại M.
- **Kế hoạch của `gate-registry`** lấy từ `doc_diff()` rồi `ke_hoach()` trong `.claude/dev/ci_dang_ky_test.py` (`:860-878`,
  `:889-901`), GOC/DAU và `CI_DANG_KY_DOT_BIEN_MANH` lấy từ `env` của bước registry (`ci.yml:1108-1111`). `doc_diff()` trả
  `None` khi không đo được, và `ke_hoach(None)` vẫn trả một kế hoạch hợp lệ (review lượt 2, N6); nên đọc hai diff riêng, loại
  nhóm `nhanh` khi một bên `None`, rồi mới so kế hoạch.
- `.claude/dev/ci_dang_ky_test.py` nạp `yaml` ngay đầu tệp (`:24`); `chuan-bi` chạy `python3` của hệ thống không có PyYAML.
  Ở lượt `push`, `chuan-bi` cài `actions/setup-python` 3.12 và `PyYAML==6.0.3` trước bước xét (cùng bản ghim `t31` đòi).
- Mọi bước mới có thể hỏng; bóng không được đổi hành vi CI. Mọi bước mới ở `chuan-bi` (năm bước) có `continue-on-error: true` và
  `timeout-minutes`; output `*_bong` chỉ mang giá trị khi bước xét và bước tải bằng chứng cùng `outcome == 'success'` (review
  lượt 3, R6).
- **Không thêm phụ thuộc cho check bắt buộc**: biên nhận do job riêng `bien-nhan-cay` tạo, `needs: chuan-bi`, không job nào
  `needs` nó, `continue-on-error: true` cấp job, `timeout-minutes` 3. Job ấy vẫn chiếm một runner và có thể xếp hàng; B1
  **không** hứa thời gian của check bắt buộc hay của toàn lượt không đổi. C5, C6 đo các đại lượng ấy để báo, không có ngưỡng
  đạt (review lượt 4, S6).
- Ảnh runner so ở job `chuan-bi` hai lượt (`ADR-0068` Q3, G3): bước phân loại ghi thêm output `anh_os`, `anh_version` từ biến
  `ImageOS`, `ImageVersion`; job biên nhận chép hai giá trị ấy vào biên nhận.
- `ops/ci_provenance.py` đã có `goi_that(url)` (`:79-96`): GET REST, theo chuyển hướng bằng tay và không mang token sang host
  khác. B1 dùng lại hàm ấy.
- Bốn nhóm tái dùng và job `ubuntu-latest` của từng nhóm:

  | nhóm | job | chỉ số ma trận `manh` | phút runner (cộng trung vị từng job, lượt `push` từ 17-11) |
  |---|---|---|---|
  | `cong_cu` | `gate-cong-cu`, `gate-cong-cu-gop` | 0–7, — | 146,4 |
  | `ops` | `gate-ops` | — | 25,3 |
  | `nhanh` | `gate-nhanh-manh`, `gate-nhanh-gop`, `gate-registry` | 0–7, —, — | 33,1 |
  | `packet_loop` | `gate-packet-loop-manh`, `gate-packet-loop` | 0–15, — | 41,7 |

**Bảng consumer của `ci.yml`.** Liệt kê bằng `git grep -l -E "workflows/ci\.yml|ci\.yml"` trên `*.py`, `*.ps1`, `*.sh`,
`*.yml` (trừ `ops/reviews/`, `ops/land/`) của `45bae8d0`: 21 tệp mã và 4 workflow (không tính `ci.yml`). Mỗi dòng nói tệp đọc
gì và phép đo trên bản YAML chứng kiến làm đúng mục tiêu của B1 (bản chứng kiến của review lượt 4, `thu/b1-r3-witness.yml`;
r4 thêm bước bundle vào job biên nhận):

| consumer | đọc gì của `ci.yml` | B1 đụng? | phép đo |
|---|---|---|---|
| `ops/ci_duong_nhanh_test.py` | toàn bộ hình dạng (`y01`–`y16`, `KHUNG_JOB`, `RUN_BUOC_PACKET`…) | có, trong write set | harness `pins` lượt 3, 4: sau khi cập nhật các họ ở mục 3.6 ⇒ 15/15 guard `y*` `DAT` |
| `.claude/dev/chay-cong-windows_test.ps1`, `.claude/dev/chay-cong-windows.ps1` | mọi job trừ `chuan-bi`: dấu vân `$DauVanCi`, gương lệnh hay dòng `KHÔNG CHẠY` (`:1248-1252`, `:1310-1315`, `:1399-1412`) | có (job mới), trong write set | harness `windows` lượt 4: thêm dấu vân và dòng `KHÔNG CHẠY` ⇒ tương đương `t32` rc 0 |
| `.claude/dev/ci_dang_ky_test.py` | `if:` cấp job của job G5, registry, packet-loop; băm `BAM_GATE_*`; `loi_ruff_ci`; `loi_workflow_dot_bien_du` (bước, trần, `env` của `gate-registry`) | không | harness lượt 3: `loi_gate_nhanh`, `loi_vung_thiet_lap`, `loi_g5_workflow` không lỗi; đo 20-11 trên máy soạn: `loi_workflow_dot_bien_du` rỗng |
| `ops/lease_publish_test.py` | `t161` (ma trận `os`), `t162` (biểu thức `os`), `t31` (ghim PyYAML) | không | đo 20-11: không job nào khai `os` riêng; mọi lệnh cài PyYAML ghim `6.0.3` |
| `ops/cong_cu_test.py` | `t6` (bước trước G5 của `gate`), cây có `ci.yml` | không | harness lượt 3: `t6` thật đạt |
| `scripts/tl_selftest.py` | khoá thứ tự `core.abbrev 7`, `fetch-depth: 0`, `- name: doc-claims-check` (`:27797-27803`) | không | đo 20-11: `ok3` đúng trên nền và bản chứng kiến |
| `.claude/dev/launcher_test.py` | năm chỗ ghim `AL_VER` (`:6398-6404`) | không | đo 20-11: 5 chỗ, cùng `1.7.7` |
| `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`, `ops/ci_provenance_test.py`, `.claude/dev/chon_reviewer_test.py`, `.claude/dev/gate_lifecycle.py` | tên check bắt buộc, đường dẫn trong danh sách, fixture tổng hợp | không | đọc mã: không phân tích job hay bước của `ci.yml` thật |
| `.claude/dev/launcher.py`, `.claude/hooks/session-start.sh`, `ops/bien_nhan_v2.py`, `ops/bien_nhan_v2_test.py`, `ops/cai_actionlint.sh`, `ops/codex_cloud_setup.sh`, `ops/cong_cu.py`, `ops/specs/wp1434-r3/do/thu_thap.py` | chỉ nhắc trong chú thích hay tài liệu | không | đọc mã |
| `.github/workflows/ci-dot-bien-du.yml`, `launcher-windows.yml`, `ops-publish-lease.yml`, `ops-thu-hoi-admission.yml` | chú thích; `ci-dot-bien-du.yml` được `loi_workflow_dot_bien_du` so với `gate-registry` | không | như dòng `ci_dang_ky_test.py` |

Người thi hành chạy lại cột "phép đo" trên `ci.yml` ứng viên thật trước khi giao review (C7).

## 1. write_set

- `.github/workflows/ci.yml` (job `chuan-bi` và job mới `bien-nhan-cay`)
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.claude/dev/chay-cong-windows_test.ps1`
- `.claude/dev/chay-cong-windows.ps1`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set (`ai-dang-giu` trên kho bare khớp máy
chủ), đo ngay trước khi cấp. Lúc soạn, ba tệp đầu thuộc `wp1448-r2-g1-claude` (mục 9) ⇒ lease B1 chờ lease ấy nhả hay hết hạn.

Kích thước ước theo khối (dòng thêm):

| khối | tệp | ước |
|---|---|---|
| lệnh `bien-nhan-cay` (gồm bundle, `GITHUB_SHA`, blob `ci.yml`), output ảnh runner | `ops/ci_duong_nhanh.py` | 45 |
| tầng thu: đọc lượt, jobs (phân trang), artefact zip, log `chuan-bi` qua `goi_that`, ghi nguyên văn vào `dau-vao/` | `ops/ci_duong_nhanh.py` | 60 |
| hàm thuần `quyet_dinh_tai_dung`: phép chung (4a–4e, gồm lấy object từ bundle) | `ops/ci_duong_nhanh.py` | 60 |
| bảng nhóm và phép theo nhóm (4f) | `ops/ci_duong_nhanh.py` | 25 |
| kế hoạch registry (4g), xử lý `None` | `ops/ci_duong_nhanh.py` | 25 |
| output dạng chuẩn, tệp bằng chứng, ghi `khong_xet`, tự kiểm đọc lại | `ops/ci_duong_nhanh.py` | 40 |
| job `chuan-bi` (năm bước mới, output có điều kiện) và job `bien-nhan-cay` | `.github/workflows/ci.yml` | 65 |
| fixture git (gồm bundle) và API giả | `ops/ci_duong_nhanh_test.py` | 70 |
| ca (gồm ca ghim phiên bản hàm quyết định) | `ops/ci_duong_nhanh_test.py` | 100 |
| đột biến (khoảng 48 dòng bảng) | `ops/ci_duong_nhanh_test.py` | 60 |
| cập nhật mười họ chốt ghim | `ops/ci_duong_nhanh_test.py` | 40 |
| dấu vân và dòng `KHÔNG CHẠY` cho job mới | hai tệp `.ps1` | 10 |
| **cộng** | | **600** |

Ước 600 vượt trần 450 của `ADR-0053`; khối `nang_tran` ở đầu tệp xin trần 650 cùng lần duyệt băm (**E2** gộp vào lần duyệt
**E5**).

## 2. ngoai_pham_vi

- Lệnh `kiem-lai-tai-dung`, bỏ job, điều kiện cấp job, bước `kiem-tai-dung` của `gate`, chốt của
  `.claude/dev/ci_dang_ky_test.py`: B2.
- Luật (ADR-0068, protocol): A.
- Lượt `workflow_dispatch`, Windows, merge một cha, lượt `push` nhiều commit: không xét tái dùng.
- `ops/ci_provenance.py`, `.claude/dev/ci_dang_ky_test.py`: chỉ **nạp** để dùng hàm, không sửa.
- Nghĩa của `che_do` và `packet_loop`: không đổi.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — bước phân loại hiện có ghi thêm output `anh_os`, `anh_version` (giá trị `ImageOS`,
   `ImageVersion`; rỗng khi vắng). Lệnh mới `bien-nhan-cay --ra <thư mục>` ghi hai tệp vào thư mục ấy:
   - `bien-nhan-cay.json`: một đối tượng JSON với `phien_ban` (2), `su_kien`, `run_id`, `run_attempt`, `github_sha` (biến
     `GITHUB_SHA`), `sha` (`git rev-parse HEAD`), `cha` (cha của `HEAD`, đúng thứ tự `git rev-list --parents`), `cay`
     (`HEAD^{tree}`), `ci_yml_blob` (`git rev-parse HEAD:.github/workflows/ci.yml`), `che_do`, `goc`, `dau` (đúng hai giá trị
     `gate-registry` của lượt ấy nhận làm `CI_DANG_KY_GOC`, `CI_DANG_KY_DAU`), `anh_os`, `anh_version` (của `chuan-bi`, nhận qua
     `env`);
   - `nguon.bundle`: `git bundle create nguon.bundle HEAD ^<cha 1> ^<cha 2>`.
   `HEAD` không có đúng hai cha, thiếu một giá trị hay git lỗi ⇒ rc ≠ 0, không ghi tệp nào.
2. `.github/workflows/ci.yml` — job mới `bien-nhan-cay`: `if:` đúng `github.event_name == 'pull_request'`, `needs: chuan-bi`,
   `runs-on: ubuntu-latest` (không ma trận), `continue-on-error: true` cấp job, `timeout-minutes` 3; checkout đủ sâu để có hai
   cha của commit merge tổng hợp; chạy `bien-nhan-cay`; `actions/upload-artifact` tên `bien-nhan-cay` chứa hai tệp,
   `overwrite: true`, `retention-days: 90`. Không job nào `needs` job này.
3. `.github/workflows/ci.yml` — job `chuan-bi`: `permissions` cấp job đúng `contents: read`, `actions: read`; thêm output
   `anh_os`, `anh_version` (từ bước phân loại) và `tai_dung_bo_bong`, `tai_dung_run_bong`, `tai_dung_cha_bong`,
   `tai_dung_cay_bong`. Mỗi output `*_bong` lấy giá trị của bước xét **chỉ khi** `steps.xet-tai-dung.outcome == 'success'` và
   bước tải `bien-nhan-tai-dung` có `outcome == 'success'`; khác thì chuỗi rỗng. Chỉ khi `github.event_name == 'push'`, sau bước
   phân loại: `actions/setup-python` 3.12; cài `PyYAML==6.0.3`; bước `xet-tai-dung` chạy `python ops/ci_duong_nhanh.py
   xet-tai-dung` với token qua `env` (`${{ github.token }}`), `github.event.before`, `github.sha`, `che_do` của bước phân loại,
   ảnh runner; rồi `actions/upload-artifact` tên `bien-nhan-tai-dung` (tệp bằng chứng và thư mục `dau-vao/`),
   `retention-days: 90`; rồi bước `ghi-ap-dung` với `if: always() && github.event_name == 'push'` in dòng
   `TAI_DUNG_AP_DUNG: xet=<outcome bước xét> tai=<outcome bước tải> bo=<tập hiệu lực>`, trong đó tập hiệu lực là đúng biểu thức
   của output `tai_dung_bo_bong`; ba giá trị đi qua `env`, không chèn biểu thức vào thân `run`. **Cả năm bước mới** (cài
   Python, cài PyYAML, xét, tải bằng chứng, ghi áp dụng) có `continue-on-error: true` và `timeout-minutes`; tổng trần các bước
   của `chuan-bi` nhỏ hơn trần job, trần job tối đa 30 (`y16`). **Không job nào đọc output `*_bong`.**
4. `ops/ci_duong_nhanh.py` — lệnh `xet-tai-dung`, hai tầng như mục 0. Tầng thu ghi vào `dau-vao/` mọi phản hồi REST đã đọc
   (URL, thời điểm UTC, mã HTTP, thân nguyên văn, mọi trang), zip biên nhận nguyên byte, đoạn log đã dùng (id job, attempt, số
   dòng, dòng nguyên văn), và các giá trị môi trường đã dùng (`GITHUB_REF`, `GITHUB_REPOSITORY`, `before`, `che_do`, ảnh runner).
   Tầng quyết định là hàm thuần `quyet_dinh_tai_dung(dau_vao)`: không gọi mạng, không đọc đồng hồ hay biến môi trường; sự kiện
   git (cha, cây, `merge-tree`, blob, object trong bundle) nó tự tính từ SHA bằng git cục bộ. Hằng `PHIEN_BAN_QUYET_DINH`
   (số nguyên, bắt đầu 1), hằng `BAM_QUYET_DINH` (sha256 mã nguồn các hàm quyết định, ca ở mục 6 ghim) và hằng `CHE_DO_XET`
   (`"bong"` ở B1; B2 đổi thành `"bat"`), để lệnh kiểm lại đối chiếu hai trường ấy với tệp tại M. Phép chung, lỗi ở một
   phép ⇒ không nhóm nào (`ADR-0068` Q5):
   - a. sự kiện `push`, `GITHUB_REF` là `refs/heads/<nhánh mặc định>`, `che_do` là `day_du`;
   - b. commit M (`github.sha`) có đúng hai cha P1, P2, và `github.event.before` bằng P1;
   - c. REST `actions/workflows/ci.yml/runs?event=pull_request&head_sha=P2` có lượt mà `head_repository.full_name` bằng
     `GITHUB_REPOSITORY`, `path` bằng `.github/workflows/ci.yml`, `status` `completed`, `conclusion` `success`,
     `run_attempt` bằng 1; xét tối đa 5 lượt, mới nhất trước;
   - d. artefact `bien-nhan-cay` của lượt ấy tải được qua `goi_that` và có đủ hai tệp. Biên nhận: `phien_ban` 2, `su_kien`
     `pull_request`, `run_id` đúng lượt, `run_attempt` 1, `che_do` `day_du`, `anh_os` và `anh_version` khác rỗng và bằng ảnh
     của job `chuan-bi` đang chạy. Bundle: `git bundle verify` đạt; lấy object `HEAD` của bundle vào một ref tạm; SHA object
     bằng `sha` và bằng `github_sha` của biên nhận; cha **đọc từ object** bằng `[P1, P2]`; cây đọc từ object bằng `M^{tree}`;
     blob `ci.yml` đọc từ object bằng `ci_yml_blob` và bằng blob `ci.yml` tại M. Log job `chuan-bi` của lượt ấy (attempt 1) có
     đúng một dòng `HEAD is now at <h> Merge <P2> into <P1>` với `<h>` là tiền tố của SHA object;
   - e. `git merge-tree --write-tree P1 P2` ra đúng `M^{tree}`.

   Phép theo nhóm, lỗi ⇒ chỉ nhóm ấy bị loại:
   - f. jobs attempt 1 của lượt ấy (`runs/<id>/attempts/1/jobs`, đủ trang): với mỗi job của nhóm, tập job `ubuntu-latest` mang
     tên ấy khớp **đúng** tập chỉ số ma trận ở bảng mục 0 (mỗi chỉ số một lần; job không ma trận đúng một lần), và mọi job ấy
     `success`. Bảng nhóm là hằng trong `ops/ci_duong_nhanh.py`;
   - g. riêng nhóm `nhanh`: nạp `.claude/dev/ci_dang_ky_test.py` bằng `importlib` theo đường dẫn; đọc `doi_pr =
     doc_diff(env_pr)` và `doi_push = doc_diff(env_push)` **riêng** (`env_pr` = sự kiện `pull_request`, GOC/DAU là `goc`/`dau`
     của biên nhận; `env_push` = sự kiện `push`, GOC là `github.event.before`, DAU là M). Một bên `None` ⇒ loại `nhanh`. Rồi so
     `ke_hoach(doi_pr, manh=m)` với `ke_hoach(doi_push, manh=m)`, `m = doc_bien_manh({"CI_DANG_KY_DOT_BIEN_MANH": <giá trị env
     ấy của bước registry trong ci.yml của M>})`. Khác nhau, nạp lỗi hay tính lỗi ⇒ loại `nhanh`.

   Bước xét **luôn** ghi tệp bằng chứng ở lượt `push`, kể cả khi 4a hay 4b trượt (`quyet_dinh` `khong_xet` kèm lý do, không
   gọi REST). Tổng thời gian không quá 120 giây. Thứ tự: ghi tệp bằng chứng và `dau-vao/`; đọc lại `dau-vao/` từ đĩa, chạy lại
   hàm thuần, đòi kết quả `(quyet_dinh, nhom, ly_do)` bằng kết quả vừa tính (khác ⇒ rc ≠ 0, không ghi output); ghi output bước
   **sau cùng**. Kết quả: in một dòng
   `TAI_DUNG_BONG: nhom=<danh sách> run=<id> cay=<tree>` (danh sách rỗng thì kèm lý do từng phép trượt); output bước
   `tai_dung_bo` ở **dạng chuẩn** (tên nhóm trong bảng, không lặp, sắp theo thứ tự bảng, bao bởi dấu phẩy: `,a,b,`; rỗng nếu
   không nhóm nào), `tai_dung_run`, `tai_dung_cha` (`P1,P2`), `tai_dung_cay`. Tệp `bien-nhan-tai-dung.json`: `phien_ban` 2,
   `che_do_xet` `bong`, `phien_ban_quyet_dinh`, `quyet_dinh` (`khong_xet`, `khong_tai_dung` hay `tai_dung`; `tai_dung` khi và
   chỉ khi tập nhóm khác rỗng) kèm `ly_do` là danh sách mã phép trượt (ví dụ `4b_before`, `4c_khong_nguon`, `4f:ops`, so như
   tập), `run_id` và `run_attempt` của chính lượt `push`, P1, P2, M, cây, `before`, blob `ci.yml` tại M,
   blob `ops/ci_duong_nhanh.py` tại M, lượt nguồn (id, attempt), id và sha256 của zip biên nhận, nội dung biên
   nhận, SHA object lấy từ bundle, dòng `HEAD is now at` và id job `chuan-bi` nguồn, tên, id, `run_attempt` và kết luận từng job
   theo nhóm, `doi_pr`, `doi_push`, hai kế hoạch registry, ảnh runner hai lượt, và quyết định cùng lý do của từng nhóm. Trường
   không áp dụng cho một trạng thái mang giá trị `null`, không vắng.
5. `.claude/dev/chay-cong-windows_test.ps1` và `.claude/dev/chay-cong-windows.ps1` — ghim dấu vân job `bien-nhan-cay` trong
   `$DauVanCi`; bước chạy `bien-nhan-cay` có dòng `KHÔNG CHẠY` kèm lý do (chỉ có nghĩa ở lượt `pull_request` của CI), để `t32`
   xanh.
6. `ops/ci_duong_nhanh_test.py` — ca và đột biến theo bảng ở mục 4; cập nhật `TAP_CHO_PHEP`, `y02`, `Y04_ENV_BUOC_CHE_DO`/`y04`,
   `y10`, `JOB_CO_IF_CHO_PHEP`/`y11`, `y12`, `y13`, `y14`, `y16`, `KHUNG_JOB` cho các bước và job mới, mỗi ngoại lệ hẹp đúng tên
   bước, tên job và biểu thức mới; ca canh `ADR-0068` Q4 (không job nào thuộc một nhóm có `if:` theo `github.ref` hay
   `github.event_name`); ca canh bảng nhóm (tên job và tập chỉ số ma trận khớp `ci.yml`, mọi job ngoài `gate`, `chuan-bi`,
   `bien-nhan-cay` thuộc đúng một nhóm); ca canh "không job nào đọc output `*_bong`, không job nào `needs` `bien-nhan-cay`"; ca
   canh dạng chuẩn của `tai_dung_bo`; ca ghim `BAM_QUYET_DINH` (sha256 mã nguồn các hàm quyết định, đọc bằng `inspect`, bằng hằng;
   đổi hàm mà không đổi hằng và `PHIEN_BAN_QUYET_DINH` ⇒ đỏ); ca hàm thuần (chạy hai lần trên cùng `dau-vao/` ⇒ cùng kết quả;
   chạy với mạng giả ném lỗi khi bị gọi ⇒ không gọi); ca dòng `TAI_DUNG_AP_DUNG` (bước `ghi-ap-dung` có `if: always()`, ba giá
   trị qua `env`, biểu thức tập hiệu lực đúng bằng biểu thức của output `tai_dung_bo_bong`).

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| C1 | `python ops/ci_duong_nhanh_test.py` in dòng tổng `N/N` hai số bằng nhau, rc 0: trên Ubuntu (job `gate-ops` của PR) và trên máy Windows của chủ kho (`ADR-0060` M3, BASE và ứng viên, cùng máy). `pwsh .claude/dev/chay-cong-windows_test.ps1` trên máy ấy xanh trọn, gồm `t32` | số trước khác số sau; rc ≠ 0; `t32` đỏ | mỗi đột biến ở C2; bỏ dấu vân `bien-nhan-cay` ⇒ `t32` đỏ |
| C2 | Mỗi chốt có ca riêng và **đột biến riêng** trong bảng đột biến của tệp test, chết đúng ca của nó (bộ phân hạng của tệp): (1) thiếu một khoá biên nhận; commit một cha; bundle không tạo được ⇒ rc ≠ 0 — ba; (4a) sự kiện `pull_request`, `workflow_dispatch`, ref khác nhánh mặc định, `che_do` `duong_nhanh` — bốn; (4b) một cha, `before` khác P1 — hai; (4c) `head_repository` khác, `path` khác, `conclusion` khác, `run_attempt` 2 — bốn; (4d) `phien_ban` 1, `run_id` lệch, `che_do` `duong_nhanh`, `anh_version` lệch, `anh_version` rỗng, bundle thiếu, bundle hỏng, SHA object khác `sha`, SHA object khác `github_sha`, object có **một cha** nhưng tiêu đề `Merge <P2> into <P1>`, cây object khác `M^{tree}`, blob `ci.yml` của object khác `ci_yml_blob`, log thiếu dòng `HEAD is now at`, `<h>` không là tiền tố SHA object — mười bốn; (4e) `merge-tree` ra cây khác — một; (4f) một job `skipped`, một chỉ số vắng, một chỉ số lặp, một job `run_attempt` 2, bỏ chốt "mọi job" — năm, mỗi cái chỉ loại đúng nhóm của nó; (4g) phản chứng đổi tên của review lượt 1 ⇒ loại riêng `nhanh`; một `doc_diff` trả `None`, hai `doc_diff` trả `None` ⇒ loại riêng `nhanh`; diff rỗng thật cả hai bên ⇒ `nhanh` vẫn được; bỏ tham số `manh`; nạp `ci_dang_ky_test.py` lỗi ⇒ loại riêng `nhanh` — sáu; lỗi HTTP, JSON hỏng, zip hỏng, hết giờ ⇒ không nhóm nào — bốn; dạng chuẩn: đổi thứ tự, lặp tên, tên lạ — ba; trạng thái: `tai_dung` với tập nhóm rỗng, `khong_tai_dung` với tập nhóm khác rỗng — hai; bước xét ghi output rồi lỗi ⇒ output job `*_bong` rỗng; bước tải bằng chứng lỗi ⇒ output job rỗng; lượt `push` làn `duong_nhanh` ⇒ `quyet_dinh` `khong_xet` — ba; hai tầng: `dau-vao/` thiếu một phản hồi mà hàm thuần cần ⇒ tự kiểm đọc lại lệch, bước xét rc ≠ 0, không output; hàm thuần gọi `goi_that` ⇒ ca hàm thuần đỏ; đổi một hàm quyết định mà giữ `BAM_QUYET_DINH` ⇒ ca ghim đỏ; hàm thuần đọc `os.environ` ⇒ ca hàm thuần đỏ — bốn | một đột biến sống, hay chết vì lý do khác chốt | chính bảng ấy |
| C3 | Ca canh Q4, bảng nhóm, output bóng và `needs` đỏ khi: thêm bước có `if:` theo `github.ref` vào `gate-ops`; đổi `manh` của `gate-packet-loop-manh` thành 0–14; thêm `needs.chuan-bi.outputs.tai_dung_bo_bong` vào `if:` của một job; thêm `bien-nhan-cay` vào `needs` của `gate`; bỏ `continue-on-error` của một trong năm bước mới; bỏ điều kiện `outcome` khỏi output `tai_dung_bo_bong`; bỏ `always()` khỏi `if:` của `ghi-ap-dung`; cho biểu thức `bo` của `ghi-ap-dung` khác biểu thức của output `tai_dung_bo_bong` | ca vẫn xanh | tám đột biến YAML ấy (trên bản sao `ci.yml`, như các đột biến `yml_*` hiện có) |
| C4 | `actionlint` trên `ci.yml` không thêm finding so với BASE (delta 0, cùng nền có `shellcheck`) | thêm finding | — (cổng hiện hành) |
| C5 | Đo đầu-cuối trước land, mục 4 bên dưới | xem dưới | — (răng ở C2) |
| C6 | Sau land (**chưa đo được** tới lúc ấy): mười lượt `push` lên `master` đầu tiên sau commit land của B1, chọn theo `created_at`, ghi id và SHA trước khi đọc kết quả. Mỗi lượt có dòng `TAI_DUNG_BONG` và đúng một dòng `TAI_DUNG_AP_DUNG`, có artefact `bien-nhan-tai-dung` đọc được với `che_do_xet` `bong`, và không job nào nghỉ vì B1. Mười lượt PR đầu tiên sau land có artefact `bien-nhan-cay` gồm hai tệp. Ghi để báo (không ngưỡng): số lượt `push` có nhóm tái dùng được theo từng tập nhóm; thời gian thêm của `chuan-bi`; với lượt PR, thời gian xếp hàng và chạy của job biên nhận, thời gian tới khi mọi check bắt buộc xong và thời gian toàn lượt | một lượt thiếu dòng hay artefact; một job nghỉ vì B1 | — (quan sát CI thật; kiểm lại nội dung là việc của B2) |
| C7 | Trước khi giao review: chạy cột "phép đo" của bảng consumer (mục 0) trên `ci.yml` ứng viên thật; mọi dòng ra như bảng | một consumer ngoài write set đỏ | thêm một consumer giả đọc job mới vào bản sao ⇒ phép đo đỏ |

C6 không đòi có lượt tái dùng; không có thì ghi "chưa quan sát được tái dùng", không phải đạt.

**C5 — phép đo đầu-cuối trước land.** Một workflow đo tạm trên nhánh `do-ci/**` (không merge, `permissions` đúng như
`chuan-bi`) chạy `xet-tai-dung` với môi trường giả lập lượt `push` lên `master`, cho một merge commit M′ dựng tại chỗ có cha
`[base, H]`, trong đó H là head PR của B1 và `base` là cha đầu của commit merge tổng hợp mà lượt PR xanh của H đã checkout
(đọc từ object trong bundle). Tiền đề, đo và ghi **trước** khi chấm: lượt PR ấy `run_attempt` 1, đã hoàn tất xanh, đủ bốn nhóm
chạy `success` (B1 sửa `ci.yml`, tệp có trong `PHU_THUOC_PACKET_LOOP`); hai diff registry khác `None` và hai kế hoạch bằng
nhau; job đo chạy trên cùng `ImageVersion` với `chuan-bi` của lượt PR. Thiếu tiền đề ⇒ ghi `not_measured` và đo lại ở lượt PR
kế, không phải lỗi thuật toán và không phải E1. Bốn vế, mỗi vế chỉ đổi một biến: (i) đủ tiền đề ⇒ `tai_dung_bo` bằng
`,cong_cu,ops,nhanh,packet_loop,`, `tai_dung_run` bằng id lượt PR ấy; (ii) đổi biến `ImageVersion` ⇒ rỗng; (iii) M′ dựng trên
một `base` khác có cây khác ⇒ rỗng; (iv) `before` khác `base` ⇒ rỗng. Ghi thêm, cho B2 dùng: dòng `TAI_DUNG_AP_DUNG` của job đo; dạng các dòng `Runner Image` trong log `Set up job` của job `chuan-bi` lượt PR; log checkout của lượt PR có SHA đầy đủ của commit merge tổng hợp hay không. Ghi để báo: thời gian năm bước mới ở `chuan-bi`, thời gian
xếp hàng và chạy của job `bien-nhan-cay`, thời gian tới khi mọi check bắt buộc xong và thời gian toàn lượt PR. Ghi trigger, quyền,
giá trị `before`/ref/SHA giả lập và hiện vật đọc lại.

Bảng năm vế của L6: C1 khớp dòng tổng `N/N` với điều kiện hai số bằng nhau (vế âm là rc ≠ 0); (b), (d) không áp dụng vì dòng
tổng do máy in một dòng, số bằng chữ số; (c) đếm theo từng đột biến ở C2; (e) không có lời khai "0 cổng". Dòng `TAI_DUNG_BONG`
ở C6: tiền tố cố định do mã in; nội dung do B2 kiểm lại.

## 5. luat_dung

- Trần kích thước: trần của khối `nang_tran` (600 dòng thêm) nếu chủ kho duyệt băm đặc tả này (**E2** gộp **E5**, hồ sơ ở khối
  `nang_tran` và mục `pham_vi_e`), không thì 450 của `ADR-0053`. Người thi hành đo `git diff --numstat` khi xong; vượt trần đang
  áp ⇒ dừng và hỏi chủ kho mã **E2**, mang `git diff --numstat` từng tệp, khối nào vượt ước, trần đang áp và trần xin, lý do
  không tách được. Không giảm độ phủ test để vừa trần.
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã dùng, finding còn mở và
  số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Lease khác đang giữ một đường dẫn của write set ⇒ chờ (phụ thuộc, không phải điểm hỏi).
- Cần sửa một tệp ngoài write set để giữ cổng xanh (C7 đỏ) ⇒ dừng phiên, revision mới của đặc tả; không tự sửa; không phải
  điểm hỏi trừ khi revision ấy vượt trần (**E2** như trên).
- C5 vế (i) không đạt khi **đã đủ tiền đề**, sau khi đã xét lại thiết kế ⇒ hỏi chủ kho mã **E1**, mang: lệnh và mã HTTP của
  từng lần thử; gốc rễ đã xác định (ví dụ token của job không tải được artefact của lượt khác, hay bundle không lấy được object)
  và vì sao mỗi cách đã thử hỏng; phương án đề xuất.

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — sửa `ci.yml` (quyền `actions: read`, job mới) và bộ phân loại. Mỗi việc sau mang mã **E5**: chủ kho duyệt
  băm, cấp lease, audit trước merge. Mỗi lần hỏi E5 mang đủ ba thứ của bảng `ADR-0067`: **diff** (đặc tả này hay diff PR),
  **lý do** (dựng bộ xét tái dùng ở chế độ chạy bóng để đo trước khi bật), và **ai được thêm quyền gì** (job `chuan-bi` được
  quyền `actions: read` để đọc lượt, log và artefact của chính kho; không ai được thêm quyền ghi).

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Bốn lượt review đặc tả đã đếm ba hình dạng lặp lại; mỗi hình dạng nay có cách đo
riêng thay cho lời khai:

| hình dạng | lần | cách đo ở r4 |
|---|---|---|
| chốt ghim hay consumer bị bỏ sót | 4 (F2, N2, R1, S1) | bảng consumer liệt kê bằng `git grep`, mỗi dòng có phép đo; C7 chạy lại trên ứng viên |
| danh tính lượt PR | 3 (F4, R5, S2) | object commit lấy từ bundle (băm nội dung), cộng dòng log của `actions/checkout` |
| hợp đồng kiểm lại chưa kín | 4 (F8, N3, R2–R5, S3–S5) | đổi thiết kế gốc, không vá thêm: bộ xét hai tầng (mục 0), đầu vào thô lưu nguyên văn, hàm quyết định thuần có phiên bản ghim, dòng `TAI_DUNG_AP_DUNG` cho tập hiệu lực; B2 r4 chỉ xác thực và chạy lại |

## 8. chua_do_duoc

- Token `github.token` với `actions: read` có tải được artefact và log của lượt khác qua REST hay không; `git bundle` chạy
  được trên runner với clone `fetch-depth: 0`: chưa chạy trong kho này; C5 là phép đo đầu tiên.
- `ImageOS`, `ImageVersion` có mặt trong môi trường job `ubuntu-latest`: theo tài liệu runner-images; C5 đo.
- Thời gian thêm của `chuan-bi` lượt `push` và của job `bien-nhan-cay`: C5, C6 đo để báo.
- Kích thước thư mục `dau-vao/` mỗi lượt (phản hồi jobs nhiều trang, zip biên nhận): C5 đo để báo.
- Tỷ lệ lượt `push` tái dùng được, theo nhóm: C6 và giai đoạn bóng đo.

## 9. Đo lúc soạn (20-11-2026)

- `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`.
- `ai-dang-giu` trên `D:/tlscan.git` (tập `refs/heads/*` khớp máy chủ): `.github/workflows/ci.yml`, `ops/ci_duong_nhanh.py`,
  `ops/ci_duong_nhanh_test.py` (09:21:48Z–09:34:11Z) ⇒ đều `NGƯỜI_GIỮ 1: wp1448-r2-g1-claude` (Issue #1448, hạn
  `2026-11-23T08:00:00Z`). Hai tệp `.ps1` chưa quét; người cấp lease quét đủ năm đường dẫn ngay trước khi cấp. Nếu #1448 land
  trước, mọi mốc `ci.yml` và chốt ghim trong đặc tả này phải đo lại; đổi thì revision mới.
- Bảng consumer: `git grep` như mục 0 ⇒ 21 tệp mã, 4 workflow. Phép đo trên nền và trên `b1-r3-witness.yml`,
  `b2-r3-witness.yml` của review lượt 4 (chạy bằng `python -S` với PyYAML 6.0.3): khoá thứ tự `tl_selftest` đúng, 5 chỗ
  `AL_VER: 1.7.7`, mọi lệnh cài PyYAML ghim `6.0.3`, không job nào khai `os` riêng, `loi_workflow_dot_bien_du` rỗng — như nhau
  trên cả ba.
- Harness `pins` (lượt 3) và `windows` (lượt 4) của reviewer: xem bảng consumer.

## 10. Thay đổi so với r2

Xem đặc tả r3 mục 11.

## 11. Thay đổi so với r3

Theo review lượt 4 (Codex, `changes_requested`, 5 P2, 2 P3; A r4 đạt):

- S1: write set thêm hai tệp `.ps1` (bản gương Windows duyệt mọi job trừ `chuan-bi`, không chỉ `gate*` như r3 khai sai); thêm
  bảng consumer liệt kê bằng `git grep` và tiêu chí C7.
- S2: lượt PR tải lên git bundle; bộ xét lấy object, đọc cha, cây và blob `ci.yml` từ object, đòi SHA object bằng `sha` và
  `GITHUB_SHA` của biên nhận; dòng log chỉ còn vai buộc SHA với lần checkout. Thêm mô hình tin cậy. Biên nhận lên `phien_ban` 2.
- S6: bỏ mọi lời hứa về thời gian; chỉ hứa không thêm phụ thuộc cho check bắt buộc; C5, C6 đo để báo.
- Bằng chứng ghi `null` cho trường không áp dụng, phiên bản bộ xét (blob `ops/ci_duong_nhanh.py`), SHA object; `retention-days`
  90 cho hai artefact.
- Hợp đồng kiểm lại (S3–S5) hỏng bốn lượt liền theo cùng một hình dạng; đổi thiết kế gốc thay vì vá: bộ xét hai tầng (tầng thu
  lưu nguyên văn đầu vào vào `dau-vao/`; hàm quyết định thuần, có `PHIEN_BAN_QUYET_DINH` và `BAM_QUYET_DINH` ghim), tự kiểm đọc
  lại trước khi ghi output, và bước `ghi-ap-dung` in tập hiệu lực từ biểu thức Actions. `ly_do` thành danh sách mã phép.
- Ước kích thước 600; `nang_tran` xin 650.
