# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B` (revision 2)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B** · `revision`: **2** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm E5, mục
  `pham_vi_e`). Thay `ops/specs/CI-TAI-DUNG-THEO-CAY-B-r1.md` (sha256
  `57ccbf1d65f9ccf7061e732222d9d11cae6704e69aee06251de9e98dfce34b75`, chưa từng được duyệt, giữ trong kho). Thay đổi so
  với r1: mục 10.
- `packet_issue`: **chưa có**. Packet anh em: `CI-TAI-DUNG-THEO-CAY-A` (ADR-0068 và protocol, đặc tả
  `ops/specs/CI-TAI-DUNG-THEO-CAY-A-r2.md`). **B phụ thuộc A**: base của B phải chứa commit land của A; chưa có thì không
  cấp lease B.
- `nguon_cap_viec`: như packet A r2 (chỉ thị *"Soạn Đ2"* 16-11-2026, ba câu trả lời, và *"Soạn r2"* 20-11-2026). Luật mà
  packet này thi hành là `ADR-0068` (do A thêm).
- `review_class`: **sensitive** — sửa `.github/workflows/ci.yml` và bộ phân loại chế độ chạy của CI (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease, phải chứa commit land của A.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (chạm E5). Điều kiện merge theo `ADR-0060`,
  gồm lượt Windows của `ops/ci_duong_nhanh_test.py` và `.claude/dev/ci_dang_ky_test.py`.

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r2.)

## 0. Vấn đề và thiết kế

Mục 0 của đặc tả A r2 có số đo. Thiết kế dưới đây chốt theo các ràng buộc đo được trên `origin/master` `45bae8d0`
(20-11-2026); số dòng là số trên commit ấy.

- Job `gate` có bước **chỉ chạy trên `master`**: `release-verify strict (lane LAND — manifest committed)`
  (`.github/workflows/ci.yml:501`), là bước bắt lệch `RELEASE_MANIFEST.json` mà lượt PR không bắt được (`CLAUDE.md`
  §Quy ước deploy mục 5). Job `gate` cũng có bước `tl selftest (co bang chung exact-identity)` chỉ chạy khi không phải
  `pull_request` (`:342-374`). Nên ở chế độ tái dùng, **job `gate` chạy đủ**.
- Tám job còn lại chia thành bốn **nhóm tái dùng**; mỗi nhóm hoặc bỏ cả, hoặc chạy cả:

  | nhóm | job | số job `ubuntu-latest` | phút runner (cộng trung vị từng job, lượt `push` từ 17-11) |
  |---|---|---|---|
  | `cong_cu` | `gate-cong-cu` (ma trận `manh` 0–7), `gate-cong-cu-gop` | 8 + 1 | 146,4 |
  | `ops` | `gate-ops` | 1 | 25,3 |
  | `nhanh` | `gate-nhanh-manh` (ma trận `manh` 0–7), `gate-nhanh-gop`, `gate-registry` | 8 + 1 + 1 | 33,1 |
  | `packet_loop` | `gate-packet-loop-manh` (ma trận `manh` 0–15), `gate-packet-loop` | 16 + 1 | 41,7 |

  `gate-registry` thuộc nhóm `nhanh` vì nó đọc kết quả `gate-nhanh-gop` (`CI_DANG_KY_GOP_KQ`) và lập kế hoạch theo diff
  của sự kiện (`CI_DANG_KY_SU_KIEN`, `CI_DANG_KY_GOC`, `CI_DANG_KY_DAU`, `:1108-1110`), nên nhóm này phải qua `ADR-0068`
  Q7.
- Ở lượt PR, nhóm `packet_loop` có thể nghỉ cả nhóm (`packet_loop=bo_qua`, `ops/ci_duong_nhanh.py:406-421`); khi ấy lượt
  `push` không tái dùng được nhóm này và chạy nó, đúng điều #1353 đòi.
- Ở lượt PR làn `duong_nhanh`, các job vẫn `success` nhưng bỏ bước nặng. Nên điều kiện "job `success`" chưa đủ; biên
  nhận phải ghi `che_do` của lượt PR, và chỉ `day_du` mới tái dùng được.
- Lượt `push` chỉ có ma trận `ubuntu-latest`, và không check bắt buộc nào của cổng merge đọc lượt `push`. `kiem-merge`
  (K2 CI) đọc check trên head PR trước merge (`.claude/dev/packet_loop.py:3646`). Bỏ job ở lượt `push` không đổi nghĩa
  cổng merge.
- `ops/ci_provenance.py` ghi job `skipped` là `skipped`, không vỡ (`:385-386`).
- Lượt PR không lưu cha của commit merge tổng hợp ở chỗ đọc được sau khi PR đóng (`pull_requests` của run rỗng với cả
  1.203 lượt `pull_request` trong dữ liệu tải 16-11). Nên lượt PR phải tự để lại **biên nhận cây** (artefact) lúc chạy.
- Các chốt đang ghim hình dạng `if:` mà thiết kế này đổi: trong `ops/ci_duong_nhanh_test.py`, `y11` (`JOB_CO_IF_CHO_PHEP`,
  `:2849`), `y12` (`IF_BUOC_CHUAN`) và ảnh chụp đầu job (`:2711-2712`); trong `.claude/dev/ci_dang_ky_test.py`, `_if_duoc`
  (`:1454`), nhánh `gate-packet-loop-manh` (`:1523`), nhánh `gate-registry` và `G5_MANH_IF` của `loi_g5_workflow`. Hai tệp
  ấy vào write set.

Luồng:

1. Lượt `pull_request`, job `chuan-bi`: sau bước phân loại, ghi biên nhận cây và tải lên artefact `bien-nhan-cay`.
2. Lượt `push` lên nhánh mặc định, job `chuan-bi`: bộ phân loại chạy như cũ (`che_do`, `packet_loop` không đổi nghĩa),
   rồi xét tái dùng theo `ADR-0068`; output mới `tai_dung_bo` là danh sách nhóm được bỏ, dạng `,ops,nhanh,` (rỗng nếu
   không nhóm nào).
3. Mỗi job của một nhóm có thêm vế `!contains(needs.chuan-bi.outputs.tai_dung_bo, ',<nhóm>,')` ở điều kiện cấp job. Job
   `gate` chạy đủ và thêm một bước tự tính lại phép chứng minh bằng git, in `TAI_DUNG: DAT …` khi `tai_dung_bo` khác rỗng.

## 1. write_set

- `.github/workflows/ci.yml`
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`
- `.claude/dev/ci_dang_ky_test.py`

Điều kiện cấp lease như A (`ai-dang-giu` trên kho bare khớp máy chủ). Kết quả đo lúc soạn r2 ở mục 9.

Kích thước dự kiến: khoảng 440 dòng thêm (`ci.yml` khoảng 45, `ci_duong_nhanh.py` khoảng 160, test khoảng 220,
`ci_dang_ky_test.py` khoảng 15), sát trần 450 của `ADR-0053`. Tham chiếu: packet đường nhanh #674 (PR #703) thêm 618 dòng
mã và 3.608 dòng test cho một bộ phân loại trọn vẹn; packet này thêm một nhánh vào bộ ấy.

## 2. ngoai_pham_vi

- Luật (ADR-0068, protocol): packet A.
- Lượt `pull_request`, `workflow_dispatch`, Windows, merge một cha: không tái dùng (`ADR-0068` Giới hạn).
- `ops/ci_provenance.py`, `ops/land_evidence_nguon.py`, `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test_manh.py`:
  không sửa (mục 0).
- `ops/cong_cu_test.py`, `ops/nhanh_don_duoc_test.py`: không sửa. Job gom của chúng bị bỏ ở cấp job khi nhóm được tái dùng,
  nên mã gom không gặp trạng thái mới.
- Nghĩa của `che_do` và `packet_loop`: không đổi. `tai_dung_bo` là output thứ ba, riêng.
- `.github/workflows/packet-loop-dot-bien.yml`: không sửa.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — lệnh `bien-nhan-cay`: in đúng một dòng JSON với các khoá `phien_ban` (1), `su_kien`,
   `run_id`, `run_attempt`, `sha` (commit đang checkout), `cha` (danh sách cha của `sha`, đúng thứ tự `git rev-list
   --parents`), `cay` (`sha^{tree}`), `che_do` (chế độ của chính lượt ấy), `tep_doi` (danh sách đường dẫn đổi mà bộ phân
   loại đã dùng, sắp xếp), `image_os`, `image_version` (biến môi trường `ImageOS`, `ImageVersion` của runner). Thiếu một
   giá trị hay git lỗi ⇒ rc ≠ 0 và không in gì.
2. `.github/workflows/ci.yml` — job `chuan-bi`, chỉ khi `github.event_name == 'pull_request'`: bước chạy `bien-nhan-cay`
   (`continue-on-error: true`, có `timeout-minutes`) ghi tệp, rồi `actions/upload-artifact` tên `bien-nhan-cay`,
   `overwrite: true`. Bước hỏng không làm `chuan-bi` đỏ; thiếu biên nhận chỉ làm lượt `push` sau này chạy đủ.
3. `ops/ci_duong_nhanh.py` — hàm xét tái dùng, gọi trong `main()` khi và chỉ khi: sự kiện `push`, `GITHUB_REF` là
   `refs/heads/<nhánh mặc định>`, và bộ phân loại hiện có ra `che_do=day_du`. Phần chung cho mọi nhóm:
   - a. commit `M` (`CI_DUONG_NHANH_MERGE`) có đúng hai cha `P1`, `P2`;
   - b. REST `actions/workflows/ci.yml/runs?event=pull_request&head_sha=P2` có một lượt mà `head_repository.full_name`
     bằng `GITHUB_REPOSITORY`, `path` bằng `.github/workflows/ci.yml`, `status` `completed`, `conclusion` `success`; xét
     tối đa 5 lượt, mới nhất trước;
   - c. artefact `bien-nhan-cay` của lượt ấy tải được và đọc được: `su_kien` `pull_request`, `run_id` đúng lượt, `cha`
     bằng đúng `[P1, P2]`, `cay` bằng `M^{tree}`, `che_do` `day_du`, `image_os` và `image_version` bằng của lượt `push`;
   - d. `git merge-tree --write-tree P1 P2` chạy trên lượt `push` ra đúng `M^{tree}`.
   Theo nhóm, với jobs của lượt ấy (`filter=latest`, đủ trang), một nhóm được tái dùng khi:
   - e. với mỗi job của nhóm, số job tên ấy chạy trên `ubuntu-latest` bằng đúng số ở bảng mục 0, và mọi job ấy `success`;
     hằng số số job sống trong `ops/ci_duong_nhanh.py` và có ca test đối chiếu với ma trận của `ci.yml`;
   - f. riêng nhóm `nhanh` (`ADR-0068` Q7): `tep_doi` của biên nhận bằng tập tệp đổi mà bộ phân loại tính cho lượt `push`.
   Mọi lỗi (HTTP, JSON, zip, git, hết giờ: tổng không quá 120 giây) ⇒ không nhóm nào, và in một dòng lý do. Có nhóm ⇒ in một
   dòng `TAI_DUNG: run=<id> attempt=<n> cay=<tree> nhom=<danh sách>`, ghi output `tai_dung_bo` (dạng `,a,b,`),
   `tai_dung_run`, `tai_dung_attempt`, `tai_dung_cha` (`P1,P2`). Header `Authorization` gắn kiểu không đi theo chuyển
   hướng (URL tải artefact là URL ký sẵn).
4. `.github/workflows/ci.yml` — job `chuan-bi`: `permissions` cấp job đúng `contents: read` và `actions: read`; bước phân
   loại nhận token qua `env` (`${{ github.token }}`); thêm bốn output ở mục tiêu 3.
5. `.github/workflows/ci.yml` — tám job của bốn nhóm: điều kiện cấp job thêm vế
   `!contains(needs.chuan-bi.outputs.tai_dung_bo, ',<nhóm>,')`, nối bằng `&&` vào điều kiện đang có, hoặc là điều kiện duy
   nhất nếu job chưa có. Chỉ khi chuỗi chứa đúng `,<nhóm>,` mới bỏ; rỗng, vắng hay lạ ⇒ chạy (fail-close).
6. `.github/workflows/ci.yml` + `ops/ci_duong_nhanh.py` — job `gate`: bước mới, `if:` đúng
   `needs.chuan-bi.outputs.tai_dung_bo != ''`, chạy lệnh `kiem-tai-dung` với `tai_dung_cha`, `tai_dung_bo`, `tai_dung_run`
   từ `chuan-bi` và `github.sha`: tính lại (a) và (d) bằng git trên checkout của `gate`, in
   `TAI_DUNG: DAT run=<id> attempt=<n> cay=<tree> cha=<P1>,<P2> nhom=<danh sách>`; lệch hay thiếu ⇒ rc ≠ 0. Các bước khác
   của `gate` giữ nguyên điều kiện.
7. `ops/ci_duong_nhanh_test.py` — ca và đột biến theo bảng ở mục 4; cập nhật `y11`, `y12` và ảnh chụp đầu job cho điều
   kiện mới; thêm ca canh `ADR-0068` Q4: mọi `if:` có `github.ref` hay `github.event_name` trong `ci.yml` nằm trong job
   `gate` hoặc `chuan-bi`; thêm ca canh bảng nhóm: mỗi job mang vế `tai_dung_bo` thuộc đúng một nhóm, mọi job ngoài `gate`
   và `chuan-bi` thuộc một nhóm, và số job ma trận khớp hằng số.
8. `.claude/dev/ci_dang_ky_test.py` — cập nhật các chốt ghim `if:` cấp job (`_if_duoc`, nhánh `gate-packet-loop-manh`,
   nhánh `gate-registry`, `G5_MANH_IF`) cho điều kiện mới; giữ nguyên mọi chốt khác.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| B1 | `python ops/ci_duong_nhanh_test.py` in dòng tổng `N/N` với hai số bằng nhau, rc 0, trên Ubuntu (job `gate-ops`) và Windows (lượt `workflow_dispatch` `windows-only` trên head) | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở B2 |
| B2 | Mỗi chốt có ca riêng và **đột biến riêng** trong bảng đột biến của tệp test, mỗi đột biến giết đúng ca của nó: (1) thiếu khoá biên nhận ⇒ rc ≠ 0; (3a) một cha ⇒ không nhóm nào; (3b) `head_repository` khác, `path` khác, `conclusion` khác — ba đột biến; (3c) `cha` đảo thứ tự, `cay` lệch, `che_do` `duong_nhanh`, `image_version` lệch, `run_id` lệch — năm đột biến; (3d) `merge-tree` ra cây khác; (3e) một job của nhóm `skipped`, một job vắng, một mảnh thừa — ba đột biến, và đột biến thứ tư bỏ chốt "mọi job" để chỉ còn "có ít nhất một job"; (3f) `tep_doi` lệch thì nhóm `nhanh` bị loại mà ba nhóm kia vẫn được — một đột biến bỏ chốt (3f); (3) lỗi HTTP, JSON hỏng, zip hỏng, hết giờ ⇒ không nhóm nào — bốn đột biến; sự kiện `pull_request`/`workflow_dispatch` và ref không phải nhánh mặc định ⇒ không xét — hai đột biến; (6) `kiem-tai-dung` với cha lệch hay cây lệch ⇒ rc ≠ 0 — hai đột biến | một đột biến sống, hay chết vì lỗi khác lý do của chốt (bộ phân hạng của tệp test) | chính bảng ấy |
| B3 | Ca canh Q4 và ca canh bảng nhóm (mục tiêu 7) đỏ khi: thêm một bước có `if:` theo `github.ref` vào `gate-ops`; bỏ vế `tai_dung_bo` khỏi một trong tám job; thêm vế ấy vào `gate`; đổi `manh` của `gate-packet-loop-manh` thành 0–14 mà không đổi hằng số | ca vẫn xanh | bốn đột biến YAML ấy (đo trên bản sao của `ci.yml` như các đột biến `yml_*` hiện có) |
| B4 | `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) rc 0 và `gate-registry` xanh trên PR | rc ≠ 0 | trả `G5_MANH_IF` về chuỗi cũ ⇒ đỏ |
| B5 | Phép đo đầu-cuối trước land, trên dữ liệu thật: một workflow đo tạm trên nhánh `do-ci/**` (không merge) gọi lệnh phân loại với môi trường giả lập lượt `push` lên `master` cho một merge commit dựng tại chỗ có cha `[base, H]`, trong đó `H` là head của PR B và `base` là cha đầu tiên của commit merge tổng hợp mà lượt PR xanh của `H` đã checkout. PR B đổi `.github/workflows/ci.yml`, tệp nằm trong `PHU_THUOC_PACKET_LOOP`, nên lượt PR của nó chạy đủ bốn nhóm. Ba vế: (i) đúng `base` ⇒ `tai_dung_bo` bằng `,cong_cu,ops,nhanh,packet_loop,` và `tai_dung_run` bằng id lượt PR ấy; (ii) đổi `ImageVersion` ⇒ rỗng; (iii) dựng merge commit trên một `base` khác có cây khác ⇒ rỗng | vế (i) ra khác, hay (ii)/(iii) ra khác rỗng | — (phép đo hành vi thật; răng nằm ở B2) |
| B6 | `actionlint` trên `ci.yml` không thêm finding so với `origin/master` (delta 0, cùng nền có `shellcheck`) | thêm finding | — |
| B7 | Sau land (**chưa đo được** tới lúc ấy): người land B đọc mười lượt `push` lên `master` đầu tiên sau commit land của B. Với mỗi lượt có `tai_dung_bo` khác rỗng: các job của nhóm được bỏ `skipped`, các job còn lại chạy, job `gate` `success` và có dòng `TAI_DUNG: DAT`, và người land tự chạy lại phép (a), (d) bằng git trên máy mình ra cùng kết quả. Với mỗi lượt rỗng: log `chuan-bi` có dòng lý do. Ghi số lượt theo từng tập nhóm | một lượt tái dùng mà phép tính lại ra khác; một lượt không có dòng lý do hay dòng `TAI_DUNG` | — |

Ghi rõ về B7: tiêu chí này **không** đòi phải có lượt tái dùng trong mười lượt; không có lượt nào thì ghi "chưa quan sát
được tái dùng", không phải đạt. Không chọn lượt canary theo dự đoán kết quả (bài học tám revision của
`THU-HOI-ADMISSION-MERGE-BASE-B`).

## 5. luat_dung

- Trần kích thước `ADR-0053`: dự kiến khoảng 440 dòng thêm. Vượt ⇒ dừng; nâng trần là **E2** (mang số `git diff
  --numstat`, tệp nào phình, vì sao không tách được).
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ **E2**.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- A chưa land ⇒ không cấp lease B (phụ thuộc, không phải điểm hỏi).
- Lease khác đang giữ một đường dẫn của write set (lúc soạn: `wp1448-r2-g1-claude` giữ ba tệp, mục 9) ⇒ chờ lease ấy nhả hay
  hết hạn (phụ thuộc, không phải điểm hỏi).
- Cần sửa một tệp ngoài write set để giữ cổng xanh (ví dụ một bộ test khác ghim hình dạng `ci.yml`) ⇒ dừng phiên, revision
  mới của đặc tả mở rộng write set; không tự sửa. Không phải điểm hỏi chủ kho, trừ khi revision ấy vượt trần (**E2**).
- Phép đo B5 vế (i) không ra được tái dùng sau khi đã xét lại thiết kế (ví dụ API không cho tải artefact bằng token của
  job) ⇒ **E1**, mang lệnh, mã HTTP và các phương án đã thử.

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — sửa `ci.yml` và bộ phân loại quyết định job nào chạy. Chủ kho duyệt băm đặc tả, cấp lease và audit trước
  merge.

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Hai lớp lỗi đã gặp ở các packet cùng vùng, người thi hành nên đọc trước:
`kiem-re-cua-fail-close-chua-co-ca` (#674, nhắc ở docstring `kiem_mode_git` của `ops/ci_duong_nhanh.py`) và lớp "canary
chọn theo dự đoán" của `THU-HOI-ADMISSION-MERGE-BASE-B`.

## 8. chua_do_duoc

- Token `github.token` của job `chuan-bi` với `actions: read` có tải được artefact của lượt khác qua REST
  `actions/artifacts/<id>/zip` hay không: chưa chạy trong kho này; B5 là phép đo đầu tiên.
- Repo đang để quyền mặc định của `GITHUB_TOKEN` là gì: chưa đo; mục tiêu 4 khai quyền cấp job nên không phụ thuộc.
- Tỷ lệ lượt `push` sẽ tái dùng được, theo từng nhóm: lịch sử 01→15-11 có 25/79 merge cây trùng (trước #1343); sau #1343,
  tỷ lệ lượt PR có nhóm `packet_loop` nghỉ chưa đo.
- Biến `ImageOS`, `ImageVersion` có mặt trên `ubuntu-latest`: theo tài liệu runner-images; chưa đo trong kho này, B5 đo.
- Một lượt PR được chạy lại một phần (`re-run failed jobs`) có giữ artefact `bien-nhan-cay` của attempt trước không: chưa
  đo; mục tiêu 3c chỉ đòi `run_id` đúng, không đòi `run_attempt`.
- Tập tệp đổi tính theo `P1...P2` (lượt PR) và theo `P1..M` (lượt `push`) có bằng nhau với mọi merge sạch không: chưa
  chứng minh; mục tiêu 3f đo nó cho từng lượt thay vì giả định.

## 9. Đo lúc soạn r2 (20-11-2026)

- `origin/master` `45bae8d07a8cdf06a1ca9a7a2e015a6258169379`.
- Không đổi gì trong `.github/workflows/`, `ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`,
  `.claude/dev/ci_dang_ky_test.py`, `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/` giữa `94cbb36` (đo đầu ngày) và `45bae8d0`.
- `ai-dang-giu` trên `D:/tlscan.git`, tập `refs/heads/*` khớp máy chủ:

  | đường dẫn | quét (UTC) | kết quả |
  |---|---|---|
  | `.github/workflows/ci.yml` | 09:21:48Z–09:26:36Z | `NGƯỜI_GIỮ 1: wp1448-r2-g1-claude` |
  | `ops/ci_duong_nhanh.py` | 09:26:37Z–09:29:47Z | `NGƯỜI_GIỮ 1: wp1448-r2-g1-claude` |
  | `ops/ci_duong_nhanh_test.py` | 09:29:48Z–09:34:11Z | `NGƯỜI_GIỮ 1: wp1448-r2-g1-claude` |
  | `.claude/dev/ci_dang_ky_test.py` | 09:35:51Z–09:39:05Z (lượt đầu 09:34Z `KHÔNG_XÁC_ĐỊNH` vì máy chủ thêm nhánh giữa lượt; làm mới rồi quét lại, 367/367 nhánh) | `NGƯỜI_GIỮ 0` |

  `wp1448-r2-g1-claude` là lease của Issue #1448 (`[Packet proposed][Mission1172] PR1 — Quan sát G5…`), hạn
  `2026-11-23T08:00:00Z`, đọc từ `refs/heads/ops/wp1448-r1:ops/leases/wp1448-r2-g1-claude.yaml`. Hệ quả: ngoài điều kiện A
  đã land, lease B chỉ cấp được khi lease ấy nhả hay hết hạn; và nếu #1448 land trước, mọi mốc `ci.yml` và chốt ghim trong
  đặc tả này phải đo lại — đổi thì revision mới, không sửa đè.

## 10. Thay đổi so với r1

- Tái dùng theo **bốn nhóm job** thay cho bảy job một khối: sau #1343 có thêm `gate-packet-loop-manh` (16 mảnh) và job gom
  `gate-packet-loop` đổi vai; lượt PR có thể cho nhóm packet-loop nghỉ. Output `tai_dung_bo` thay cho `che_do=tai_dung`;
  `che_do` giữ nguyên nghĩa, nên `y04` và các bước theo `che_do` không đổi.
- Biên nhận thêm `tep_doi`; nhóm `nhanh` thêm điều kiện (3f) theo `ADR-0068` Q7, vì `gate-registry` lập kế hoạch theo diff
  của sự kiện.
- Điều kiện (3e) đòi đúng số job ma trận, không chỉ "có ít nhất một".
- Chốt ghim cần cập nhật đo lại trên `45bae8d0`: thêm `y11`, `y12`, ảnh chụp đầu job; số dòng mọi trích dẫn đo lại.
- B2 thêm đột biến cho (3e) và (3f); B3 thêm đột biến bảng nhóm; B5 vế (i) đòi đủ bốn nhóm.
