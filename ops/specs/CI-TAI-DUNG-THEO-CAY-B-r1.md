# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B` (revision 1)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B** · `revision`: **1** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm E5, mục
  `pham_vi_e`).
- `packet_issue`: **chưa có**. Packet anh em: `CI-TAI-DUNG-THEO-CAY-A` (ADR-0068 và protocol, đặc tả
  `ops/specs/CI-TAI-DUNG-THEO-CAY-A-r1.md`). **B phụ thuộc A**: base của B phải chứa commit land của A; chưa có thì không
  cấp lease B.
- `nguon_cap_viec`: như packet A (chỉ thị chủ kho 16-11-2026 *"Soạn Đ2"* và ba câu trả lời: chỉ `push` lên `master`; luật
  mới qua ADR; hai packet, ADR trước). Luật mà packet này thi hành là `ADR-0068` (do A thêm).
- `review_class`: **sensitive** — sửa `.github/workflows/ci.yml` và bộ phân loại chế độ chạy của CI (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, phải chứa commit land của A.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (chạm E5). Điều kiện merge theo `ADR-0060`,
  gồm lượt Windows của `ci_duong_nhanh_test.py` và `ci_dang_ky_test.py`.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Đo ba phép *Hiệu lực* của hai ADR: xem đặc tả A, cùng thời điểm.)

## 0. Vấn đề và thiết kế

Mục 0 của đặc tả A có số đo. Thiết kế dưới đây đã chốt với các ràng buộc đo được trên `origin/master` `9c1661f7`
(16-11-2026):

- Job `gate` có bước **chỉ chạy trên `master`**: `release-verify strict (lane LAND — manifest committed)`
  (`.github/workflows/ci.yml:500-502`), là bước bắt lệch `RELEASE_MANIFEST.json` mà lượt PR không bắt được (`CLAUDE.md`
  §Quy ước deploy mục 5). Job `gate` cũng có bước `tl selftest (co bang chung exact-identity)` chỉ chạy khi không phải
  `pull_request` (`:341-373`). Nên ở chế độ tái dùng, **job `gate` chạy đủ**; chỉ bảy job khác bị bỏ.
- Bảy job bị bỏ: `gate-cong-cu`, `gate-cong-cu-gop`, `gate-ops`, `gate-nhanh-manh`, `gate-nhanh-gop`, `gate-registry`,
  `gate-packet-loop`. Theo trung vị từng job ở báo cáo 15-11 (§2.5 của
  `ops/specs/CI-TOI-UU-THOI-GIAN-BAO-CAO-20261115.md`), `gate` khoảng 12 trong khoảng 295 phút runner của một lượt đầy đủ.
- Lượt `push` chỉ có ma trận `ubuntu-latest`, và không check bắt buộc nào của cổng merge đọc lượt `push`. `kiem-merge`
  (K2 CI) đọc check trên head PR trước merge (`.claude/dev/packet_loop.py:3596`). Nên bỏ job ở lượt `push` không đổi nghĩa
  cổng merge.
- `ops/ci_provenance.py` ghi job `skipped` là `skipped`, không vỡ (`:385-386`).
- Lượt PR không lưu cha của commit merge tổng hợp ở chỗ đọc được sau khi PR đóng (`pull_requests` của run rỗng với cả
  1.203 lượt `pull_request` trong dữ liệu tải 16-11). Nên lượt PR phải tự để lại **biên nhận cây** (artefact) lúc chạy.
- Ba tệp đang ghim hình dạng `if:` mà thiết kế này đổi: `ops/ci_duong_nhanh_test.py` (`y04_tap_buoc_mang_if_che_do_khop_dung`
  và các đột biến `y04_*`), `.claude/dev/ci_dang_ky_test.py` (`_job_if_duoc_phep`, `G5_MANH_IF`, nhánh `gate-registry`
  trong `loi_g5_workflow`). Hai tệp ấy vào write set.

Luồng:

1. Lượt `pull_request`, job `chuan-bi`: sau bước phân loại, ghi biên nhận cây và tải lên artefact `bien-nhan-cay`.
2. Lượt `push` lên nhánh mặc định, job `chuan-bi`: bộ phân loại ra `day_du` như cũ, rồi xét tái dùng theo năm điều kiện
   của `ADR-0068` Q2, Q3. Đạt ⇒ `che_do=tai_dung`. Không đạt hay lỗi ⇒ giữ `day_du` (Q5).
3. `che_do=tai_dung`: bảy job bị bỏ ở cấp job; job `gate` chạy đủ và thêm một bước tự tính lại phép chứng minh bằng git,
   in `TAI_DUNG: DAT …`.

## 1. write_set

- `.github/workflows/ci.yml`
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.claude/dev/ci_dang_ky_test.py`

Điều kiện cấp lease như A (`ai-dang-giu` trên kho bare khớp máy chủ). Đo 16-11-2026 trên `D:/tlscan.git` (249/249 nhánh):
kết quả từng đường dẫn ghi ở mục 9 (đo lúc soạn).

Kích thước dự kiến: khoảng 420 dòng thêm (`ci.yml` khoảng 45, `ci_duong_nhanh.py` khoảng 140, test khoảng 225,
`ci_dang_ky_test.py` khoảng 10), dưới trần 450 của `ADR-0053`. Tham chiếu: packet đường nhanh #674 (PR #703) thêm 618 dòng
mã và 3.608 dòng test cho một bộ phân loại trọn vẹn; packet này chỉ thêm một nhánh vào bộ ấy.

## 2. ngoai_pham_vi

- Luật (ADR-0068, protocol): packet A.
- Lượt `pull_request`, `workflow_dispatch`, Windows, merge một cha: không tái dùng (`ADR-0068` Giới hạn).
- `ops/ci_provenance.py`, `ops/land_evidence_nguon.py`, `.claude/dev/packet_loop.py`: không sửa (mục 0).
- `ops/cong_cu_test.py`, `ops/nhanh_don_duoc_test.py`: không sửa. Job gom của chúng bị bỏ ở cấp job khi `tai_dung`, nên
  mã gom không gặp giá trị `che_do` mới.
- Đổi tên hay nghĩa của `duong_nhanh`: không. `tai_dung` là giá trị `che_do` thứ ba, riêng.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — lệnh `bien-nhan-cay`: in đúng một dòng JSON với các khoá `phien_ban` (1), `su_kien`,
   `run_id`, `run_attempt`, `sha` (commit đang checkout), `cha` (danh sách cha của `sha`, đúng thứ tự `git rev-list
   --parents`), `cay` (`sha^{tree}`), `che_do` (chế độ của chính lượt ấy), `image_os`, `image_version` (biến môi trường
   `ImageOS`, `ImageVersion` của runner). Thiếu một giá trị hay git lỗi ⇒ rc ≠ 0 và không in gì.
2. `.github/workflows/ci.yml` — job `chuan-bi`, chỉ khi `github.event_name == 'pull_request'`: bước chạy `bien-nhan-cay`
   (`continue-on-error: true`, có `timeout-minutes`) ghi tệp, rồi `actions/upload-artifact` tên `bien-nhan-cay`,
   `overwrite: true`. Bước hỏng không làm `chuan-bi` đỏ; thiếu biên nhận chỉ làm lượt `push` sau này chạy đủ.
3. `ops/ci_duong_nhanh.py` — hàm xét tái dùng, gọi trong `main()` khi và chỉ khi: sự kiện `push`, `GITHUB_REF` là
   `refs/heads/<nhánh mặc định>`, và bộ phân loại hiện có ra `day_du`. Hàm trả `tai_dung` khi đủ:
   - a. commit `M` (`CI_DUONG_NHANH_MERGE`) có đúng hai cha `P1`, `P2`;
   - b. REST `actions/workflows/ci.yml/runs?event=pull_request&head_sha=P2` có một lượt mà `head_repository.full_name`
     bằng `GITHUB_REPOSITORY`, `path` bằng `.github/workflows/ci.yml`, `status` `completed`, `conclusion` `success`; xét
     tối đa 5 lượt, mới nhất trước;
   - c. jobs của lượt ấy (`filter=latest`, đủ trang): với **mỗi** tên trong bảy job bị bỏ, có ít nhất một job mang tên ấy
     (đúng tên hoặc tên kèm ma trận) và **mọi** job mang tên ấy là `success`;
   - d. artefact `bien-nhan-cay` của lượt ấy tải được và đọc được: `su_kien` `pull_request`, `run_id` đúng lượt, `cha`
     bằng đúng `[P1, P2]`, `cay` bằng `M^{tree}`, `che_do` `day_du`, `image_os` và `image_version` bằng của lượt `push`;
   - e. `git merge-tree --write-tree P1 P2` chạy trên lượt `push` ra đúng `M^{tree}`.
   Mọi lỗi (HTTP, JSON, zip, git, hết giờ: tổng không quá 120 giây) ⇒ `day_du`, và in một dòng lý do. Đạt ⇒ in một dòng
   `TAI_DUNG: run=<id> attempt=<n> cay=<tree>`, ghi output `che_do=tai_dung`, `goc=P1`, `dau=P2`, `hop=M`,
   `tai_dung_run`, `tai_dung_attempt`. Header `Authorization` gắn kiểu không đi theo chuyển hướng (URL tải artefact là URL
   ký sẵn).
4. `.github/workflows/ci.yml` — job `chuan-bi`: `permissions` cấp job đúng `contents: read` và `actions: read`; bước phân
   loại nhận token qua `env` (`${{ github.token }}`); thêm output `tai_dung_run`, `tai_dung_attempt`.
5. `.github/workflows/ci.yml` — bảy job bị bỏ: điều kiện cấp job thêm vế `needs.chuan-bi.outputs.che_do != 'tai_dung'`
   (nối bằng `&&` vào điều kiện đang có, hoặc là điều kiện duy nhất nếu job chưa có). Chỉ đúng chuỗi `tai_dung` mới bỏ;
   rỗng, vắng hay lạ ⇒ chạy (fail-close).
6. `.github/workflows/ci.yml` + `ops/ci_duong_nhanh.py` — job `gate`: bước mới, `if:` đúng
   `needs.chuan-bi.outputs.che_do == 'tai_dung'`, chạy lệnh `kiem-tai-dung` với `goc`, `dau`, `hop` từ `chuan-bi`: tính lại
   (a) và (e) bằng git trên checkout của `gate`, in `TAI_DUNG: DAT run=<id> attempt=<n> cay=<tree> cha=<P1>,<P2>`; lệch
   hay thiếu ⇒ rc ≠ 0. Các bước khác của `gate` giữ nguyên điều kiện, nên chạy đủ ở `tai_dung`.
7. `ops/ci_duong_nhanh_test.py` — ca và đột biến cho mục 1, 3, 5, 6 theo bảng ở mục 4; cập nhật `y04` cho tập `if:` mới;
   thêm ca canh `ADR-0068` Q4: mọi `if:` có `github.ref` hay `github.event_name` trong `ci.yml` nằm trong job `gate` hoặc
   `chuan-bi`, và tập job mang vế `!= 'tai_dung'` đúng bằng bảy job.
8. `.claude/dev/ci_dang_ky_test.py` — cập nhật các chốt ghim `if:` cấp job (`_job_if_duoc_phep`, `G5_MANH_IF`, nhánh
   `gate-registry` của `loi_g5_workflow`) cho điều kiện mới; giữ nguyên mọi chốt khác.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| B1 | `python ops/ci_duong_nhanh_test.py` in dòng tổng `N/N` với hai số bằng nhau, rc 0, trên Ubuntu (job `gate-ops`) và Windows (lượt `workflow_dispatch` `windows-only` trên head) | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở B2 |
| B2 | Mỗi chốt có ca riêng và **đột biến riêng** trong bảng đột biến của tệp test, mỗi đột biến giết đúng ca của nó: (1) thiếu khoá biên nhận ⇒ rc ≠ 0; (3a) một cha ⇒ `day_du`; (3b) `head_repository` khác, `path` khác, `conclusion` khác — ba đột biến; (3c) một job bị bỏ `skipped` trong lượt PR, hay vắng — hai đột biến; (3d) `cha` đảo thứ tự, `cay` lệch, `che_do` `duong_nhanh`, `image_version` lệch, `run_id` lệch — năm đột biến; (3e) `merge-tree` ra cây khác; (3) lỗi HTTP, JSON hỏng, zip hỏng, hết giờ ⇒ `day_du` — bốn đột biến; sự kiện `pull_request`/`workflow_dispatch` và ref không phải nhánh mặc định ⇒ không xét — hai đột biến; (6) `kiem-tai-dung` với cha lệch hay cây lệch ⇒ rc ≠ 0 — hai đột biến | một đột biến sống, hay chết vì lỗi khác lý do của chốt (bộ phân hạng của tệp test) | chính bảng ấy |
| B3 | Ca canh Q4 (mục tiêu 7) đỏ khi: thêm một bước có `if:` theo `github.ref` vào `gate-ops`; bỏ vế `tai_dung` khỏi một trong bảy job; thêm vế ấy vào `gate` | ca vẫn xanh | ba đột biến YAML ấy (đo trên bản sao của `ci.yml` như các đột biến `yml_*` hiện có) |
| B4 | `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) rc 0 và `gate-registry` xanh trên PR | rc ≠ 0 | trả `G5_MANH_IF` về chuỗi cũ ⇒ đỏ |
| B5 | Phép đo đầu-cuối trước land, trên dữ liệu thật: một workflow đo tạm trên nhánh `do-ci/**` (không merge) gọi lệnh phân loại với môi trường giả lập lượt `push` lên `master` cho một merge commit dựng tại chỗ có cha `[base, H]`, trong đó `H` là head của PR B và `base` là cha đầu tiên của commit merge tổng hợp mà lượt PR xanh của `H` đã checkout. Ba vế: (i) đúng `base` ⇒ `che_do=tai_dung`, `tai_dung_run` bằng id lượt PR ấy; (ii) đổi `ImageVersion` ⇒ `day_du`; (iii) dựng merge commit trên một `base` khác có cây khác ⇒ `day_du` | vế (i) không ra `tai_dung`, hay (ii)/(iii) ra `tai_dung` | — (phép đo hành vi thật; răng nằm ở B2) |
| B6 | `actionlint` trên `ci.yml` không thêm finding so với `origin/master` (delta 0, cùng nền có `shellcheck`) | thêm finding | — |
| B7 | Sau land (**chưa đo được** tới lúc ấy): người land B đọc mười lượt `push` lên `master` đầu tiên sau commit land của B. Với mỗi lượt `tai_dung`: bảy job `skipped`, job `gate` `success` và có dòng `TAI_DUNG: DAT`, và người land tự chạy lại phép (a), (e) bằng git trên máy mình ra cùng kết quả. Với mỗi lượt `day_du`: log `chuan-bi` có dòng lý do. Ghi số lượt mỗi loại | một lượt `tai_dung` mà phép tính lại ra khác; một lượt không có dòng chế độ | — |

Ghi rõ về B7: tiêu chí này **không** đòi phải có lượt `tai_dung` trong mười lượt; không có lượt nào thì ghi "chưa quan sát
được `tai_dung`", không phải đạt. Không chọn lượt canary theo dự đoán kết quả (bài học tám revision của
`THU-HOI-ADMISSION-MERGE-BASE-B`).

## 5. luat_dung

- Trần kích thước `ADR-0053`: dự kiến khoảng 420 dòng thêm. Vượt ⇒ dừng; nâng trần là **E2** (mang số `git diff
  --numstat`, tệp nào phình, vì sao không tách được).
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ **E2**.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- A chưa land ⇒ không cấp lease B (phụ thuộc, không phải điểm hỏi).
- Cần sửa một tệp ngoài write set để giữ cổng xanh (ví dụ một bộ test khác ghim hình dạng `ci.yml`) ⇒ dừng phiên, revision
  mới của đặc tả mở rộng write set; không tự sửa. Không phải điểm hỏi chủ kho, trừ khi revision ấy vượt trần (**E2**).
- Phép đo B5 vế (i) không ra được `tai_dung` sau khi đã xét lại thiết kế (ví dụ API không cho tải artefact bằng token của
  job) ⇒ **E1**, mang lệnh, mã HTTP và các phương án đã thử.

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — sửa `ci.yml` và bộ phân loại quyết định job nào chạy. Chủ kho duyệt băm đặc tả và audit trước merge.

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Hai lớp lỗi đã gặp ở các packet cùng vùng, người thi hành nên đọc trước:
`kiem-re-cua-fail-close-chua-co-ca` (#674, nhắc ở docstring `kiem_mode_git` của `ops/ci_duong_nhanh.py`) và lớp "canary
chọn theo dự đoán" của `THU-HOI-ADMISSION-MERGE-BASE-B`.

## 8. chua_do_duoc

- Token `github.token` của job `chuan-bi` với `actions: read` có tải được artefact của lượt khác qua REST
  `actions/artifacts/<id>/zip` hay không: chưa chạy trong kho này; B5 là phép đo đầu tiên.
- Repo đang để quyền mặc định của `GITHUB_TOKEN` là gì: chưa đo; mục tiêu 4 khai quyền cấp job nên không phụ thuộc.
- Tỷ lệ lượt `push` sẽ ra `tai_dung` sau land: lịch sử 01→15-11 là 25/79; tương lai chưa biết.
- Biến `ImageOS`, `ImageVersion` có mặt trên `ubuntu-latest`: theo tài liệu runner-images; chưa đo trong kho này, B5 đo.
- Một lượt PR được chạy lại một phần (`re-run failed jobs`) có giữ artefact `bien-nhan-cay` của attempt trước không: chưa
  đo; mục tiêu 3d chỉ đòi `run_id` đúng, không đòi `run_attempt`.

## 9. Đo lúc soạn (16-11-2026)

- `origin/master` `9c1661f76d5f4ef811aa349df102989cc2e2d53d` (11:2xZ).
- `ai-dang-giu` trên `D:/tlscan.git`, 249/249 nhánh, tập tên khớp máy chủ (thiếu cục bộ 0, thừa 0):

  | đường dẫn | quét (UTC) | kết quả |
  |---|---|---|
  | `.github/workflows/ci.yml` | 11:25:57Z–11:27:06Z | `NGƯỜI_GIỮ 0` |
  | `ops/ci_duong_nhanh.py` | 11:27:06Z–11:28:13Z | `NGƯỜI_GIỮ 0` |
  | `ops/ci_duong_nhanh_test.py` | 11:28:13Z–11:29:21Z | `NGƯỜI_GIỮ 0` (ba lease `HẾT_HẠN` của `wp1325`; Issue #1325 `CLOSED` lúc 10:43Z) |
  | `.claude/dev/ci_dang_ky_test.py` | 11:29:21Z–11:3xZ | `NGƯỜI_GIỮ 0` (lease `HẾT_HẠN` không tính) |

  Người cấp lease đo lại ngay trước khi cấp (L5); lúc ấy A đã land nên base khác.
- Không PR mở nào (`gh pr list --state open`, 7 PR, đo 11:1xZ) có tệp nào thuộc write set của A hay B.
