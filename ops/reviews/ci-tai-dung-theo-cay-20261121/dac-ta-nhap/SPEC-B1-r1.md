# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B1` (revision 1)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B1** · `revision`: **1** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Cùng `CI-TAI-DUNG-THEO-CAY-B2` thay packet `CI-TAI-DUNG-THEO-CAY-B` (r1 sha256
  `57ccbf1d65f9ccf7061e732222d9d11cae6704e69aee06251de9e98dfce34b75`, r2 sha256
  `587e59cf83b5db6f0289d999ab50e9fbce4abd13f454c188bbc8c4b9b6fc76fe`; r2 review lượt 1 `changes_requested`; cả hai chưa từng
  được duyệt). Thay đổi so với B r2: mục 10.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**). Packet anh em:
  `CI-TAI-DUNG-THEO-CAY-A` r3 (ADR-0068) và `CI-TAI-DUNG-THEO-CAY-B2` r1 (bật). B1 **không** phụ thuộc A: B1 không đổi job nào
  chạy hay không, nên không cần luật mới. B2 phụ thuộc cả A lẫn B1.
- `nguon_cap_viec`: như đặc tả A r3 (chỉ thị *"Soạn Đ2"* 16-11-2026, ba câu trả lời, *"Soạn r2"* 20-11-2026, và lựa chọn tách
  packet thay cho nâng trần).
- `review_class`: **sensitive** — sửa `.github/workflows/ci.yml` (thêm quyền `actions: read` cho một job) và bộ phân loại
  của CI (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (**E5**). Điều kiện merge theo `ADR-0060`; M3
  Windows **`required`** (diff chạm `.github/workflows/**` và thêm dòng có `subprocess`): chạy `python
  ops/ci_duong_nhanh_test.py` trên máy Windows của chủ kho theo `ADR-0057`, `ADR-0058`, `ADR-0059`, hai lượt (BASE và ứng
  viên) cùng máy. Bộ này không có lượt Windows trong CI (`.github/workflows/ci.yml:761`, `if: runner.os == 'Linux'`).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r3.)

## 0. Vấn đề và thiết kế

Mục 0 của đặc tả A r3 có số đo. B1 dựng toàn bộ bộ xét tái dùng nhưng **chỉ chạy bóng**: lượt `push` lên `master` tính và
ghi lại nhóm nào tái dùng được, rồi vẫn chạy đủ như hiện nay. B2 mới bật việc bỏ job, sau khi số lượt bóng đủ theo
`ADR-0068` Q8. Số dòng dưới đây đo trên `origin/master` `45bae8d0`.

Ràng buộc đo được (gồm các phát hiện của review lượt 1 trên B r2):

- Kế hoạch của `gate-registry` không lấy từ bộ phân loại. Nó lấy từ `doc_diff()` (`git diff --name-only --no-renames
  GOC...DAU`, với lượt `push` thêm phép GOC là tổ tiên của DAU) rồi `ke_hoach()`, cả hai trong
  `.claude/dev/ci_dang_ky_test.py` (`:860-878`, `:889-901`); GOC/DAU theo sự kiện (`ci.yml:1108-1110`). Review lượt 1 dựng
  được phản chứng git thật: đổi tên ở P1, sửa nội dung ở P2 ⇒ cùng cây, cùng cha, mà hai kế hoạch khác nhau. Nên nhóm `nhanh`
  chỉ tái dùng khi **kế hoạch** tính bằng chính hai hàm ấy trên đầu vào của hai sự kiện bằng nhau (`ADR-0068` Q7).
- `.claude/dev/ci_dang_ky_test.py` nạp `yaml` ngay đầu tệp (`:24`); `chuan-bi` chạy `python3` của hệ thống, không có
  PyYAML (đo: nạp mô-đun trong Python không site-packages ⇒ `ModuleNotFoundError: No module named 'yaml'`). Nên ở lượt
  `push`, `chuan-bi` cài `actions/setup-python` 3.12 và `PyYAML==6.0.3` trước bước xét, như các job khác của `ci.yml`. Lượt
  `pull_request` không thêm bước này (không làm chậm PR).
- `github.event.before` của lượt `push` không luôn bằng P1 (lượt `push` mang nhiều commit). `ADR-0068` Q2 đòi bằng.
- `ops/ci_provenance.py` đã có `goi_that(url)` (`:79-96`): GET REST, theo chuyển hướng bằng tay và **không** mang token sang
  host khác. B1 dùng lại hàm ấy để tải artefact, không viết bộ gọi REST mới.
- Ảnh runner (`ImageOS`, `ImageVersion`) chỉ đo được ở job tự đọc biến của mình; B1 so ảnh của job `chuan-bi` hai lượt
  (`ADR-0068` Q3, G3).
- Chốt đang ghim hình dạng job `chuan-bi`, đều trong `ops/ci_duong_nhanh_test.py`: `y02` (output, `:2467-2476`), `y10` (chỉ
  hai bước của `chuan-bi` được `continue-on-error`, `CHO_PHEP_NUOT_LOI` `:2982`), `y12` (`if:` cấp bước, `IF_BUOC_CHUAN` `:2620`), `y13`
  (topology: khoá cấp job gồm `permissions`, khoá và thứ tự bước, `:2879`), `y16` (trần thời gian của `chuan-bi`,
  `:2961-2980`), `KHUNG_JOB` (ảnh chụp đầu từng job, gồm `outputs`, `timeout-minutes` của `chuan-bi`, `:2702`). Bản gương Windows bỏ qua `chuan-bi` (`.claude/dev/chay-cong-windows_test.ps1:1249`, `:1311`).
  `.claude/dev/ci_dang_ky_test.py` chỉ đọc output `os` của `chuan-bi` (`:633-658`), B1 không đổi output ấy. Nên write set
  không cần hai tệp ấy.
- Bốn nhóm tái dùng và số job `ubuntu-latest` của từng nhóm:

  | nhóm | job | chỉ số ma trận `manh` | phút runner (cộng trung vị từng job, lượt `push` từ 17-11) |
  |---|---|---|---|
  | `cong_cu` | `gate-cong-cu`, `gate-cong-cu-gop` | 0–7, — | 146,4 |
  | `ops` | `gate-ops` | — | 25,3 |
  | `nhanh` | `gate-nhanh-manh`, `gate-nhanh-gop`, `gate-registry` | 0–7, —, — | 33,1 |
  | `packet_loop` | `gate-packet-loop-manh`, `gate-packet-loop` | 0–15, — | 41,7 |

## 1. write_set

- `.github/workflows/ci.yml` (chỉ job `chuan-bi`)
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set (`ai-dang-giu` trên kho bare khớp máy
chủ). Lúc soạn, **cả ba** đang thuộc `wp1448-r2-g1-claude` (mục 9) ⇒ lease B1 chờ lease ấy nhả hay hết hạn.

Kích thước ước theo khối (dòng thêm):

| khối | tệp | ước |
|---|---|---|
| lệnh `bien-nhan-cay` | `ops/ci_duong_nhanh.py` | 30 |
| tải và đọc lượt, jobs (phân trang), artefact zip, qua `goi_that` | `ops/ci_duong_nhanh.py` | 35 |
| phép chung (mục tiêu 4a–4e) | `ops/ci_duong_nhanh.py` | 45 |
| bảng nhóm và phép theo nhóm (4f) | `ops/ci_duong_nhanh.py` | 25 |
| kế hoạch registry (4g) | `ops/ci_duong_nhanh.py` | 20 |
| output, tệp bằng chứng | `ops/ci_duong_nhanh.py` | 15 |
| lệnh `kiem-lai-tai-dung` | `ops/ci_duong_nhanh.py` | 30 |
| job `chuan-bi` | `.github/workflows/ci.yml` | 40 |
| fixture git và API giả | `ops/ci_duong_nhanh_test.py` | 60 |
| ca | `ops/ci_duong_nhanh_test.py` | 90 |
| đột biến (khoảng 30 dòng bảng) | `ops/ci_duong_nhanh_test.py` | 45 |
| cập nhật `y02`, `y10`, `y12`, `y13`, `y16`, `KHUNG_JOB` | `ops/ci_duong_nhanh_test.py` | 15 |
| **cộng** | | **450** |

Tham chiếu đo bằng `git diff --numstat` (theo review lượt 1): packet #674 (`7e5958e`) thêm 90 dòng `ci.yml`, 618 dòng bộ phân
loại, 3.608 dòng test; packet #1343 (`b8bc64f`) thêm 226 dòng vào bốn tệp này cho một tính năng hẹp hơn. Ước 450 không có dư
địa; vượt trần lúc thi hành ⇒ luật dừng ở mục 5.

## 2. ngoai_pham_vi

- Bỏ job, điều kiện cấp job, bước `kiem-tai-dung` của `gate`, chốt của `.claude/dev/ci_dang_ky_test.py` và bản gương Windows:
  B2.
- Luật (ADR-0068, protocol): A.
- Lượt `pull_request`, `workflow_dispatch`, Windows, merge một cha, lượt `push` nhiều commit: không xét tái dùng.
- `ops/ci_provenance.py`, `.claude/dev/ci_dang_ky_test.py`: chỉ **nạp** để dùng hàm, không sửa.
- Nghĩa của `che_do` và `packet_loop`: không đổi.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — lệnh `bien-nhan-cay`: in đúng một dòng JSON với các khoá `phien_ban` (1), `su_kien`,
   `run_id`, `run_attempt`, `sha` (commit đang checkout), `cha` (cha của `sha`, đúng thứ tự `git rev-list --parents`), `cay`
   (`sha^{tree}`), `che_do` (chế độ của lượt ấy), `goc` và `dau` (đúng hai giá trị mà `gate-registry` của lượt ấy nhận làm
   `CI_DANG_KY_GOC`, `CI_DANG_KY_DAU`), `image_os`, `image_version`. Thiếu một giá trị hay git lỗi ⇒ rc ≠ 0, không in gì.
2. `.github/workflows/ci.yml`, job `chuan-bi`, chỉ khi `github.event_name == 'pull_request'`: bước chạy `bien-nhan-cay`
   (`continue-on-error: true`, có `timeout-minutes`) ghi tệp, rồi `actions/upload-artifact` tên `bien-nhan-cay`,
   `overwrite: true`. Bước hỏng không làm `chuan-bi` đỏ.
3. `.github/workflows/ci.yml`, job `chuan-bi`: `permissions` cấp job đúng `contents: read`, `actions: read`; chỉ khi
   `github.event_name == 'push'`: `actions/setup-python` 3.12, cài `PyYAML==6.0.3`, rồi bước `xet-tai-dung`
   (`continue-on-error: true`, `timeout-minutes` ≤ 5) chạy `python ops/ci_duong_nhanh.py xet-tai-dung` với token qua `env`
   (`${{ github.token }}`), `github.event.before`, `github.sha`, `che_do` của bước phân loại; rồi `actions/upload-artifact` tên
   `bien-nhan-tai-dung` (`if: always()` trong cùng điều kiện sự kiện). Thêm output `tai_dung_bo_bong` (từ bước xét). **Không
   job nào đọc output ấy.** Tổng trần thời gian các bước vẫn nhỏ hơn trần job (`y16`); được nâng trần job, tối đa 30.
4. `ops/ci_duong_nhanh.py` — lệnh `xet-tai-dung`. Phép chung, lỗi ở một phép ⇒ không nhóm nào (`ADR-0068` Q5):
   - a. sự kiện `push`, `GITHUB_REF` là `refs/heads/<nhánh mặc định>`, `che_do` là `day_du`;
   - b. commit M (`github.sha`) có đúng hai cha P1, P2, và `github.event.before` bằng P1;
   - c. REST `actions/workflows/ci.yml/runs?event=pull_request&head_sha=P2` có lượt mà `head_repository.full_name` bằng
     `GITHUB_REPOSITORY`, `path` bằng `.github/workflows/ci.yml`, `status` `completed`, `conclusion` `success`,
     `run_attempt` bằng 1; xét tối đa 5 lượt, mới nhất trước;
   - d. artefact `bien-nhan-cay` của lượt ấy tải được qua `goi_that` và đọc được: `phien_ban` 1, `su_kien` `pull_request`,
     `run_id` đúng lượt, `run_attempt` 1, `sha` 40 hex, `cha` bằng `[P1, P2]`, `cay` bằng `M^{tree}`, `che_do` `day_du`,
     `image_os` và `image_version` bằng của chính job `chuan-bi` đang chạy;
   - e. `git merge-tree --write-tree P1 P2` ra đúng `M^{tree}`.

   Phép theo nhóm, lỗi ⇒ chỉ nhóm ấy bị loại:
   - f. jobs của lượt ấy (`filter=latest`, đủ trang): với mỗi job của nhóm, tập job `ubuntu-latest` mang tên ấy khớp
     **đúng** tập chỉ số ma trận ở bảng mục 0 (mỗi chỉ số một lần; job không ma trận đúng một lần), và mọi job ấy `success`.
     Bảng nhóm là hằng trong `ops/ci_duong_nhanh.py`;
   - g. riêng nhóm `nhanh`: nạp `.claude/dev/ci_dang_ky_test.py` bằng `importlib` theo đường dẫn; kế hoạch
     `ke_hoach(doc_diff(env_pr))` bằng `ke_hoach(doc_diff(env_push))`, với `env_pr` = sự kiện `pull_request`, GOC/DAU là
     `goc`/`dau` của biên nhận, và `env_push` = sự kiện `push`, GOC là `github.event.before`, DAU là M. Nạp hay tính lỗi ⇒
     loại nhóm `nhanh`.

   Tổng thời gian không quá 120 giây. Kết quả: in một dòng `TAI_DUNG_BONG: nhom=<danh sách> run=<id> cay=<tree>` (danh sách
   rỗng thì kèm lý do từng phép trượt); ghi output bước `tai_dung_bo` dạng `,a,b,` (rỗng nếu không nhóm nào), `tai_dung_run`, `tai_dung_attempt`,
   `tai_dung_cha` (`P1,P2`); ghi tệp JSON bằng
   chứng gồm P1, P2, M, cây, lượt nguồn (id, attempt), id và sha256 của zip biên nhận, nội dung biên nhận, id và kết luận
   từng job theo nhóm, hai kế hoạch registry, ảnh runner hai lượt, và quyết định cùng lý do của từng nhóm.
5. `ops/ci_duong_nhanh.py` — lệnh `kiem-lai-tai-dung --run <id lượt push>`: đọc artefact `bien-nhan-tai-dung` của lượt ấy,
   tính lại mục tiêu 4 độc lập từ REST và git cục bộ, rồi so: tập nhóm tính lại phải bằng tập nhóm đã ghi. Với mỗi nhóm được
   ghi là tái dùng được, đọc jobs của chính lượt `push` ấy: job nào của nhóm khác `success` thì in `LECH_BONG: <nhóm> <job>
   <kết luận>`. rc 0 khi tập bằng nhau và không có `LECH_BONG`; rc 1 khi lệch; rc 2 khi không đọc được. Đây là thước đo của
   `ADR-0068` Q8 (điều kiện bật B2).
6. `ops/ci_duong_nhanh_test.py` — ca và đột biến theo bảng ở mục 4; cập nhật `y02`, `y10`, `y12`, `y13`, `y16`, `KHUNG_JOB`
   cho các bước mới của `chuan-bi`; ca canh `ADR-0068` Q4 (mọi `if:` có `github.ref` hay `github.event_name` nằm trong job `gate` hoặc
   `chuan-bi`); ca canh bảng nhóm (tên job và tập chỉ số ma trận khớp `ci.yml`, mọi job ngoài `gate` và `chuan-bi` thuộc
   đúng một nhóm); ca canh "không job nào đọc `tai_dung_bo_bong`".

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| C1 | `python ops/ci_duong_nhanh_test.py` in dòng tổng `N/N` hai số bằng nhau, rc 0: trên Ubuntu (job `gate-ops` của PR) và trên máy Windows của chủ kho (`ADR-0060` M3: BASE và ứng viên, cùng máy, cùng lệnh) | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở C2 |
| C2 | Mỗi chốt có ca riêng và **đột biến riêng** trong bảng đột biến của tệp test, chết đúng ca của nó (bộ phân hạng của tệp): (1) thiếu một khoá biên nhận ⇒ rc ≠ 0; (4a) sự kiện `pull_request`, `workflow_dispatch`, ref khác nhánh mặc định, `che_do` `duong_nhanh` — bốn đột biến; (4b) một cha, `before` khác P1 — hai; (4c) `head_repository` khác, `path` khác, `conclusion` khác, `run_attempt` 2 — bốn; (4d) `phien_ban` 2, `run_id` lệch, `cha` đảo thứ tự, `cay` lệch, `che_do` `duong_nhanh`, `image_version` lệch — sáu; (4e) `merge-tree` ra cây khác — một; (4f) một job `skipped`, một chỉ số vắng, một chỉ số lặp, bỏ chốt "mọi job" — bốn, mỗi cái chỉ loại đúng nhóm của nó; (4g) phản chứng đổi tên của review lượt 1 làm hai kế hoạch khác ⇒ loại riêng `nhanh` mà ba nhóm kia vẫn được; nạp `ci_dang_ky_test.py` lỗi ⇒ loại riêng `nhanh` — hai; lỗi HTTP, JSON hỏng, zip hỏng, hết giờ ⇒ không nhóm nào — bốn; (5) `kiem-lai-tai-dung` trên bằng chứng sửa tay: đổi lượt nguồn sang lượt làn `duong_nhanh`, bỏ một mảnh, đổi kế hoạch, thêm một job khác `success` ở lượt `push` ⇒ rc 1 — bốn | một đột biến sống, hay chết vì lý do khác chốt | chính bảng ấy |
| C3 | Ca canh Q4, bảng nhóm và "không job nào đọc `tai_dung_bo_bong`" đỏ khi: thêm bước có `if:` theo `github.ref` vào `gate-ops`; đổi `manh` của `gate-packet-loop-manh` thành 0–14; thêm `needs.chuan-bi.outputs.tai_dung_bo_bong` vào `if:` của một job | ca vẫn xanh | ba đột biến YAML ấy (trên bản sao `ci.yml`, như các đột biến `yml_*` hiện có) |
| C4 | `actionlint` trên `ci.yml` không thêm finding so với BASE (delta 0, cùng nền có `shellcheck`) | thêm finding | — (cổng hiện hành) |
| C5 | Đo đầu-cuối trước land, mục 4 bên dưới | vế (i) không ra đủ bốn nhóm khi đủ tiền đề; vế (ii)–(iv) ra khác rỗng | — (răng ở C2) |
| C6 | Sau land (**chưa đo được** tới lúc ấy): mười lượt `push` lên `master` đầu tiên sau commit land của B1, chọn theo thứ tự `created_at`, ghi id và SHA trước khi đọc kết quả. Mỗi lượt có dòng `TAI_DUNG_BONG` và artefact `bien-nhan-tai-dung`; `kiem-lai-tai-dung --run <id>` chạy trên máy người land cho từng lượt. Ghi số lượt có nhóm tái dùng được, theo từng tập nhóm, và mọi dòng `LECH_BONG` | một lượt thiếu dòng hay artefact; `kiem-lai-tai-dung` rc 1 vì tập nhóm tính lại khác tập đã ghi | — (răng của `kiem-lai-tai-dung` ở C2 mục 5) |

C6 không đòi có lượt tái dùng; không có thì ghi "chưa quan sát được tái dùng", không phải đạt. `LECH_BONG` không làm C6 đỏ:
nó là dữ liệu cho điều kiện bật của B2 (`ADR-0068` Q8).

**C5 — phép đo đầu-cuối trước land.** Một workflow đo tạm trên nhánh `do-ci/**` (không merge, `permissions` đúng như
`chuan-bi`) chạy `xet-tai-dung` với môi trường giả lập lượt `push` lên `master`, cho một merge commit M′ dựng tại chỗ có cha
`[base, H]`, trong đó H là head PR của B1 và `base` là cha đầu của commit merge tổng hợp mà lượt PR xanh của H đã checkout
(đọc từ biên nhận). Tiền đề, đo và ghi **trước** khi chấm: lượt PR ấy `run_attempt` 1, đã hoàn tất xanh, đủ bốn nhóm chạy
`success` (B1 sửa `ci.yml`, tệp có trong `PHU_THUOC_PACKET_LOOP`, nên nhóm packet-loop chạy); hai kế hoạch registry của
`(base, H)` và `(base, M′)` bằng nhau; job đo chạy trên cùng `ImageVersion` với `chuan-bi` của lượt PR. Thiếu tiền đề ⇒ ghi
`not_measured` và đo lại ở lượt PR kế, không phải lỗi thuật toán và không phải E1. Bốn vế: (i) đủ tiền đề ⇒ `tai_dung_bo`
bằng `,cong_cu,ops,nhanh,packet_loop,` và `kiem-lai-tai-dung` trên chính lượt đo rc 0; (ii) đổi biến `ImageVersion` ⇒ rỗng;
(iii) M′ dựng trên một `base` khác có cây khác ⇒ rỗng; (iv) `before` khác `base` ⇒ rỗng. Ghi trigger, quyền, giá trị
`before`/ref/SHA giả lập và hiện vật đọc lại.

Bảng năm vế của L6: C1 khớp dòng tổng `N/N` với điều kiện hai số bằng nhau (vế dương; vế âm là rc ≠ 0) — (b), (d) không áp
dụng vì dòng tổng do máy in một dòng, số bằng chữ số; (c) đếm theo từng đột biến ở C2; (e) không có lời khai "0 cổng". Dòng
`TAI_DUNG_BONG` ở C6: khớp tiền tố cố định do mã in, kèm `kiem-lai-tai-dung` đo nội dung.

## 5. luat_dung

- Trần kích thước `ADR-0053`: ước 450 dòng thêm (mục 1). Vượt ⇒ dừng và hỏi chủ kho mã **E2**, mang `git diff --numstat`,
  khối nào vượt ước, trần xin, và phương án thay là chuyển lệnh `kiem-lai-tai-dung` cùng ca của nó sang B2.
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã dùng, finding còn mở
  và số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Lease khác đang giữ một đường dẫn của write set ⇒ chờ (phụ thuộc, không phải điểm hỏi).
- Cần sửa một tệp ngoài write set để giữ cổng xanh ⇒ dừng phiên, revision mới của đặc tả; không tự sửa; không phải điểm hỏi
  trừ khi revision ấy vượt trần (**E2** như trên).
- C5 vế (i) không đạt khi **đã đủ tiền đề**, sau khi đã xét lại thiết kế (ví dụ token của job không tải được artefact của
  lượt khác) ⇒ hỏi chủ kho mã **E1**, mang lệnh, mã HTTP, các phương án đã thử và phương án đề xuất.

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — sửa `ci.yml` (quyền `actions: read`) và bộ phân loại. Mỗi việc sau mang mã **E5**: chủ kho duyệt băm, cấp
  lease, audit trước merge.

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Lớp lỗi người thi hành nên đọc trước: `kiem-re-cua-fail-close-chua-co-ca`
(#674, docstring `kiem_mode_git` của `ops/ci_duong_nhanh.py`) và lớp "canary chọn theo dự đoán" của
`THU-HOI-ADMISSION-MERGE-BASE-B`. Review lượt 1 trên B r2 bắt hai lớp mới, nay thành chốt: so nhầm consumer (F1) và chốt ghim
bị bỏ sót (F2).

## 8. chua_do_duoc

- Token `github.token` với `actions: read` có tải được artefact của lượt khác qua REST `actions/artifacts/<id>/zip` hay
  không: chưa chạy trong kho này; C5 là phép đo đầu tiên.
- `ImageOS`, `ImageVersion` có mặt trong môi trường job `ubuntu-latest`: theo tài liệu runner-images; C5 đo.
- Thời gian thêm cho `chuan-bi` của lượt `push` (cài Python và PyYAML, gọi REST): chưa đo; C5 đo.
- Tỷ lệ lượt `push` tái dùng được, theo nhóm: C6 và giai đoạn bóng đo.

## 9. Đo lúc soạn (20-11-2026)

- `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`. Không đổi gì trong `.github/workflows/`, `ops/ci_duong_nhanh.py`,
  `ops/ci_duong_nhanh_test.py`, `.claude/dev/ci_dang_ky_test.py`, `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/` giữa `94cbb36` và
  `45bae8d0`.
- `ai-dang-giu` trên `D:/tlscan.git` (tập `refs/heads/*` khớp máy chủ): `.github/workflows/ci.yml` (09:21:48Z–09:26:36Z),
  `ops/ci_duong_nhanh.py` (09:26:37Z–09:29:47Z), `ops/ci_duong_nhanh_test.py` (09:29:48Z–09:34:11Z) ⇒ đều `NGƯỜI_GIỮ 1:
  wp1448-r2-g1-claude`. Lease ấy thuộc Issue #1448 (`[Packet proposed][Mission1172] PR1 — Quan sát G5…`), hạn
  `2026-11-23T08:00:00Z`, đọc từ `refs/heads/ops/wp1448-r1:ops/leases/wp1448-r2-g1-claude.yaml`. Nếu #1448 land trước, mọi
  mốc `ci.yml` và chốt ghim trong đặc tả này phải đo lại; đổi thì revision mới, không sửa đè.
- Nạp `.claude/dev/ci_dang_ky_test.py` không có PyYAML ⇒ `ModuleNotFoundError` (đo bằng `python -S`).

## 10. Thay đổi so với B r2

- Tách thành B1 (chạy bóng) và B2 (bật). B1 không bỏ job nào.
- F1 (P1): nhóm `nhanh` so **kế hoạch** registry bằng chính `doc_diff`/`ke_hoach`, không so tập tệp của bộ phân loại; thêm
  phép `before` bằng P1; `chuan-bi` cài Python và PyYAML ở lượt `push` để nạp được mô-đun.
- F2: chốt ghim của B1 liệt kê đủ (`y02`, `y10`, `y12`, `y13`, `y16`, `KHUNG_JOB`), đã kiểm `ci_dang_ky_test.py` và bản gương Windows
  không ghim phần B1 đổi. Chốt ghim của phần bật (`BAM_GATE_REGISTRY`, `BAM_GATE_NHANH`, `G5_GOP_IF`, dấu vân Windows…) sang B2.
- F3: Windows theo `ADR-0060` M3 trên máy chủ kho, không qua `workflow_dispatch` (bộ test không có lượt Windows trong CI).
- F4: `run_attempt` 1 cho cả lượt và biên nhận; kiểm `phien_ban`, `sha`; tập chỉ số ma trận khớp đúng, không chỉ đếm; ảnh
  runner chỉ của `chuan-bi`, khai trong ADR.
- F7: C5 khai tiền đề và trạng thái `not_measured`; thêm vế (iv).
- F8: thêm `kiem-lai-tai-dung` tính lại độc lập và đột biến trên bằng chứng sửa tay; C6 dùng nó.
- F9: ước kích thước theo khối, kèm số đo tham chiếu.
- F10: mọi câu hỏi chủ kho mang mã E kèm thứ phải mang theo; bảng năm vế L6.
