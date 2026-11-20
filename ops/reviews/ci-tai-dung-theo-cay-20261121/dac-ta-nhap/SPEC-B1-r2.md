# Đặc tả packet — `CI-TAI-DUNG-THEO-CAY-B1` (revision 2)

- `packet_id`: **CI-TAI-DUNG-THEO-CAY-B1** · `revision`: **2** · trạng thái: nháp, chờ chủ kho duyệt băm (chạm **E5**, mục
  `pham_vi_e`). Thay r1 (sha256 `fd24105a394ea8a4a020c3f3af08964a82d4a8c81658991f6acfff8e3512ebf2`, review lượt 2
  `changes_requested`, chưa từng được duyệt). Cùng `CI-TAI-DUNG-THEO-CAY-B2` thay packet `CI-TAI-DUNG-THEO-CAY-B` (r1 sha256
  `57ccbf1d65f9ccf7061e732222d9d11cae6704e69aee06251de9e98dfce34b75`, r2 sha256
  `587e59cf83b5db6f0289d999ab50e9fbce4abd13f454c188bbc8c4b9b6fc76fe`). Thay đổi so với r1: mục 10.
- `packet_issue`: **chưa có**. Issue và lease mở sau khi chủ kho duyệt băm (**E5**). Packet anh em:
  `CI-TAI-DUNG-THEO-CAY-A` r4 (ADR-0068) và `CI-TAI-DUNG-THEO-CAY-B2` r2 (kiểm lại và bật). B1 **không** phụ thuộc A: B1
  không đổi job nào chạy hay không. B2 phụ thuộc A và B1.
- `nguon_cap_viec`: như đặc tả A r4.
- `review_class`: **sensitive** — sửa `.github/workflows/ci.yml` (thêm quyền `actions: read`, thêm một job) và bộ phân loại
  của CI (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease.
- Executor **Claude**; reviewer **Codex** độc lập; mức bảo đảm `human_audited` (**E5**). Điều kiện merge theo `ADR-0060`; M3
  Windows **`required`** (diff chạm `.github/workflows/**` và thêm dòng có `subprocess`): chạy `python
  ops/ci_duong_nhanh_test.py` trên máy Windows của chủ kho theo `ADR-0057`, `ADR-0058`, `ADR-0059`, hai lượt (BASE và ứng
  viên) cùng máy. Bộ này không có lượt Windows trong CI (`.github/workflows/ci.yml:761`, `if: runner.os == 'Linux'`).

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

(Ba phép đo *Hiệu lực* của hai ADR: xem đặc tả A r4.)

```yaml
nang_tran:
  ai_nang: chủ kho ducthangho, cùng lần duyệt băm đặc tả này (E2 gộp vào lần duyệt E5)
  can_cu: >-
    Ước theo khối ở mục 1 là 455 dòng thêm trên ba tệp. Không tách được: biên nhận lượt PR và bộ xét lượt push dùng chung một
    định dạng biên nhận và một bảng nhóm; tách thì packet sau phải sửa lại định dạng của packet trước, và giai đoạn bóng chỉ
    bắt đầu khi cả hai đã land. Tham chiếu numstat: #674 (7e5958e) +618 dòng mã, +3608 dòng test; #1343 (b8bc64f) +226 dòng.
  tran_cu: "sensitive ≤ 6 tệp và ≤ 450 dòng thêm (ADR-0053)"
  tran_moi: "≤ 6 tệp và ≤ 550 dòng thêm"
```

## 0. Vấn đề và thiết kế

Mục 0 của đặc tả A r4 có số đo. B1 dựng biên nhận ở lượt `pull_request` và bộ xét ở lượt `push` lên `master`, nhưng **chỉ
chạy bóng**: bộ xét tính và ghi lại nhóm nào tái dùng được, rồi lượt `push` vẫn chạy đủ như hiện nay. Lệnh kiểm lại độc lập
(`kiem-lai-tai-dung`) và việc bỏ job thuộc B2. Số dòng dưới đây đo trên `origin/master` `45bae8d0`.

Ràng buộc đo được:

- Kế hoạch của `gate-registry` lấy từ `doc_diff()` rồi `ke_hoach()` trong `.claude/dev/ci_dang_ky_test.py` (`:860-878`,
  `:889-901`), với GOC/DAU và `CI_DANG_KY_DOT_BIEN_MANH` lấy từ `env` của bước registry (`ci.yml:1108-1111`). `doc_diff()`
  trả `None` khi không đo được, và `ke_hoach(None)` vẫn trả một kế hoạch hợp lệ (review lượt 2, N6): so hai kế hoạch thẳng thì
  hai lần lỗi cũng "bằng nhau". Nên bộ xét đọc hai diff riêng, loại nhóm `nhanh` khi một bên `None`, rồi mới so kế hoạch.
- `.claude/dev/ci_dang_ky_test.py` nạp `yaml` ngay đầu tệp (`:24`), còn `chuan-bi` chạy `python3` của hệ thống không có
  PyYAML. Ở lượt `push`, `chuan-bi` cài `actions/setup-python` 3.12 và `PyYAML==6.0.3` trước bước xét.
- Mọi bước mới đều có thể hỏng (cài đặt, mạng, tải artefact). Bóng không được đổi hành vi CI, nên mọi bước mới có
  `continue-on-error: true` và `timeout-minutes`; tổng trần bước của `chuan-bi` vẫn nhỏ hơn trần job (`y16`).
- Lượt PR không được chậm thêm: biên nhận do một **job riêng** `bien-nhan-cay` tạo, `needs: chuan-bi`, không job nặng nào
  `needs` nó. Job ấy có `continue-on-error: true` cấp job để lỗi của nó không làm lượt PR đỏ. Không dùng ma trận `os`, nên
  không đụng chốt `t161` của `ops/lease_publish_test.py` (chốt chỉ soát job có `strategy.matrix.os`).
- Ảnh runner so ở job `chuan-bi` hai lượt (`ADR-0068` Q3, G3): bước phân loại ghi thêm output `anh_os`, `anh_version` từ
  biến `ImageOS`, `ImageVersion`; job biên nhận chép hai giá trị ấy vào biên nhận.
- `ops/ci_provenance.py` đã có `goi_that(url)` (`:79-96`): GET REST, theo chuyển hướng bằng tay và không mang token sang
  host khác. B1 dùng lại hàm ấy.
- Chốt đang ghim phần B1 đổi, đều trong `ops/ci_duong_nhanh_test.py`: `TAP_CHO_PHEP` (`:75`), `y02` (output của `chuan-bi`,
  `:2467`), `y10` và `CHO_PHEP_NUOT_LOI` (`:2982`, `:2986`), `y12` và `IF_BUOC_CHUAN` (`:2620`, `:2859`), `y13` (topology,
  `:2879`), `y14` và `RUN_BUOC_PACKET` (thân `run` của mọi bước gọi `ci_duong_nhanh`, `:2899`, `:2926`), `y16` (trần thời gian,
  `:2961`), `KHUNG_JOB` (ảnh chụp đầu từng job, `:2702`). Review lượt 2 đo bằng hàm guard thật: sau khi cập nhật các bảng r1
  liệt kê, chỉ còn `y14` đỏ. Bản gương Windows bỏ qua `chuan-bi` và chỉ soát job `gate*`
  (`.claude/dev/chay-cong-windows_test.ps1:1249`, `:1311`, `:1409`); `.claude/dev/ci_dang_ky_test.py` chỉ đọc output `os` của
  `chuan-bi` (`:633-658`). Nên write set không cần hai tệp ấy.
- Bốn nhóm tái dùng và job `ubuntu-latest` của từng nhóm:

  | nhóm | job | chỉ số ma trận `manh` | phút runner (cộng trung vị từng job, lượt `push` từ 17-11) |
  |---|---|---|---|
  | `cong_cu` | `gate-cong-cu`, `gate-cong-cu-gop` | 0–7, — | 146,4 |
  | `ops` | `gate-ops` | — | 25,3 |
  | `nhanh` | `gate-nhanh-manh`, `gate-nhanh-gop`, `gate-registry` | 0–7, —, — | 33,1 |
  | `packet_loop` | `gate-packet-loop-manh`, `gate-packet-loop` | 0–15, — | 41,7 |

## 1. write_set

- `.github/workflows/ci.yml` (job `chuan-bi` và job mới `bien-nhan-cay`)
- `ops/ci_duong_nhanh.py`
- `ops/ci_duong_nhanh_test.py`

Điều kiện cấp lease: không lease nào còn hiệu lực giữ một đường dẫn của write set (`ai-dang-giu` trên kho bare khớp máy
chủ). Lúc soạn, **cả ba** đang thuộc `wp1448-r2-g1-claude` (mục 9) ⇒ lease B1 chờ lease ấy nhả hay hết hạn.

Kích thước ước theo khối (dòng thêm):

| khối | tệp | ước |
|---|---|---|
| lệnh `bien-nhan-cay`, output ảnh runner của bước phân loại | `ops/ci_duong_nhanh.py` | 35 |
| đọc lượt, jobs (phân trang), artefact zip qua `goi_that` | `ops/ci_duong_nhanh.py` | 35 |
| phép chung (mục tiêu 4a–4e) | `ops/ci_duong_nhanh.py` | 45 |
| bảng nhóm và phép theo nhóm (4f) | `ops/ci_duong_nhanh.py` | 25 |
| kế hoạch registry (4g), xử lý `None` | `ops/ci_duong_nhanh.py` | 25 |
| output dạng chuẩn, tệp bằng chứng | `ops/ci_duong_nhanh.py` | 25 |
| job `chuan-bi` (năm bước mới) và job `bien-nhan-cay` | `.github/workflows/ci.yml` | 50 |
| fixture git và API giả | `ops/ci_duong_nhanh_test.py` | 60 |
| ca | `ops/ci_duong_nhanh_test.py` | 85 |
| đột biến (khoảng 32 dòng bảng) | `ops/ci_duong_nhanh_test.py` | 45 |
| cập nhật tám chốt ghim | `ops/ci_duong_nhanh_test.py` | 25 |
| **cộng** | | **455** |

Tham chiếu đo bằng `git diff --numstat`: packet #674 (`7e5958e`) thêm 90 dòng `ci.yml`, 618 dòng bộ phân loại, 3.608 dòng
test; packet #1343 (`b8bc64f`) thêm 226 dòng vào bốn tệp cùng vùng cho một tính năng hẹp hơn. Ước 455 vượt trần 450 của
`ADR-0053`; khối `nang_tran` ở đầu tệp xin trần 550 cùng lần duyệt băm.

## 2. ngoai_pham_vi

- Lệnh `kiem-lai-tai-dung`, bỏ job, điều kiện cấp job, bước `kiem-tai-dung` của `gate`, chốt của
  `.claude/dev/ci_dang_ky_test.py` và bản gương Windows: B2.
- Luật (ADR-0068, protocol): A.
- Lượt `workflow_dispatch`, Windows, merge một cha, lượt `push` nhiều commit: không xét tái dùng.
- `ops/ci_provenance.py`, `.claude/dev/ci_dang_ky_test.py`: chỉ **nạp** để dùng hàm, không sửa.
- Nghĩa của `che_do` và `packet_loop`: không đổi.

## 3. muc_tieu

1. `ops/ci_duong_nhanh.py` — bước phân loại hiện có ghi thêm output `anh_os`, `anh_version` (giá trị biến `ImageOS`,
   `ImageVersion`, chuỗi rỗng khi vắng). Lệnh mới `bien-nhan-cay`: in đúng một dòng JSON với các khoá `phien_ban` (1),
   `su_kien`, `run_id`, `run_attempt`, `sha` (commit đang checkout), `cha` (cha của `sha`, đúng thứ tự `git rev-list
   --parents`), `cay` (`sha^{tree}`), `che_do`, `goc`, `dau` (đúng hai giá trị `gate-registry` của lượt ấy nhận làm
   `CI_DANG_KY_GOC`, `CI_DANG_KY_DAU`), `anh_os`, `anh_version` (của `chuan-bi`, nhận qua `env`). Thiếu một giá trị hay git
   lỗi ⇒ rc ≠ 0, không in gì.
2. `.github/workflows/ci.yml` — job mới `bien-nhan-cay`: `if:` đúng `github.event_name == 'pull_request'`, `needs: chuan-bi`,
   `runs-on: ubuntu-latest` (không ma trận), `continue-on-error: true` cấp job, `timeout-minutes` ≤ 5; checkout đủ sâu để đọc
   cha của commit merge tổng hợp; chạy `bien-nhan-cay` ghi tệp; `actions/upload-artifact` tên `bien-nhan-cay`, `overwrite:
   true`. Không job nào `needs` job này.
3. `.github/workflows/ci.yml` — job `chuan-bi`: `permissions` cấp job đúng `contents: read`, `actions: read`; thêm output
   `anh_os`, `anh_version` (từ bước phân loại) và `tai_dung_bo_bong`, `tai_dung_run_bong`, `tai_dung_cha_bong`,
   `tai_dung_cay_bong` (từ bước xét). Chỉ khi `github.event_name == 'push'`, sau bước phân loại: `actions/setup-python` 3.12;
   cài `PyYAML==6.0.3`; bước `xet-tai-dung` chạy `python ops/ci_duong_nhanh.py xet-tai-dung` với token qua `env`
   (`${{ github.token }}`), `github.event.before`, `github.sha`, `che_do` của bước phân loại, ảnh runner; rồi
   `actions/upload-artifact` tên `bien-nhan-tai-dung`. **Cả năm bước** có `continue-on-error: true` và `timeout-minutes`; tổng
   trần các bước của `chuan-bi` nhỏ hơn trần job, trần job tối đa 30 (`y16`). **Không job nào đọc output `*_bong`.**
4. `ops/ci_duong_nhanh.py` — lệnh `xet-tai-dung`. Phép chung, lỗi ở một phép ⇒ không nhóm nào (`ADR-0068` Q5):
   - a. sự kiện `push`, `GITHUB_REF` là `refs/heads/<nhánh mặc định>`, `che_do` là `day_du`;
   - b. commit M (`github.sha`) có đúng hai cha P1, P2, và `github.event.before` bằng P1;
   - c. REST `actions/workflows/ci.yml/runs?event=pull_request&head_sha=P2` có lượt mà `head_repository.full_name` bằng
     `GITHUB_REPOSITORY`, `path` bằng `.github/workflows/ci.yml`, `status` `completed`, `conclusion` `success`,
     `run_attempt` bằng 1; xét tối đa 5 lượt, mới nhất trước;
   - d. artefact `bien-nhan-cay` của lượt ấy tải được qua `goi_that` và đọc được: `phien_ban` 1, `su_kien` `pull_request`,
     `run_id` đúng lượt, `run_attempt` 1, `sha` 40 hex, `cha` bằng `[P1, P2]`, `cay` bằng `M^{tree}`, `che_do` `day_du`,
     `anh_os` và `anh_version` khác rỗng và bằng ảnh của job `chuan-bi` đang chạy;
   - e. `git merge-tree --write-tree P1 P2` ra đúng `M^{tree}`.

   Phép theo nhóm, lỗi ⇒ chỉ nhóm ấy bị loại:
   - f. jobs của lượt ấy (`filter=latest`, đủ trang): với mỗi job của nhóm, tập job `ubuntu-latest` mang tên ấy khớp **đúng**
     tập chỉ số ma trận ở bảng mục 0 (mỗi chỉ số một lần; job không ma trận đúng một lần), mỗi job `run_attempt` 1, và mọi
     job ấy `success`. Bảng nhóm là hằng trong `ops/ci_duong_nhanh.py`;
   - g. riêng nhóm `nhanh`: nạp `.claude/dev/ci_dang_ky_test.py` bằng `importlib` theo đường dẫn; đọc `doi_pr =
     doc_diff(env_pr)` và `doi_push = doc_diff(env_push)` **riêng**, với `env_pr` = sự kiện `pull_request`, GOC/DAU là `goc`/`dau`
     của biên nhận, và `env_push` = sự kiện `push`, GOC là `github.event.before`, DAU là M. Một bên `None` ⇒ loại `nhanh`. Rồi
     so `ke_hoach(doi_pr, manh=m)` với `ke_hoach(doi_push, manh=m)`, trong đó `m = doc_bien_manh({"CI_DANG_KY_DOT_BIEN_MANH":
     <giá trị env ấy của bước registry trong ci.yml của M>})`. Khác nhau, nạp lỗi hay tính lỗi ⇒ loại `nhanh`.

   Tổng thời gian không quá 120 giây. Kết quả: in một dòng `TAI_DUNG_BONG: nhom=<danh sách> run=<id> cay=<tree>` (danh sách
   rỗng thì kèm lý do từng phép trượt); ghi output bước `tai_dung_bo` ở **dạng chuẩn** (tên nhóm trong bảng, không lặp, sắp
   theo thứ tự bảng, bao bởi dấu phẩy: `,a,b,`; rỗng nếu không nhóm nào), `tai_dung_run`, `tai_dung_cha` (`P1,P2`),
   `tai_dung_cay`; ghi tệp JSON bằng chứng `bien-nhan-tai-dung.json` với `phien_ban` 1, `che_do_xet` `bong`, P1, P2, M, cây,
   `before`, blob OID của `.github/workflows/ci.yml` tại M, lượt nguồn (id, attempt), id và sha256 của zip biên nhận, nội dung
   biên nhận, tên, id, `run_attempt` và kết luận từng job theo nhóm, `doi_pr`, `doi_push`, hai kế hoạch registry, ảnh runner hai
   lượt, và quyết định cùng lý do của từng nhóm.
5. `ops/ci_duong_nhanh_test.py` — ca và đột biến theo bảng ở mục 4; cập nhật `TAP_CHO_PHEP`, `y02`, `y10`, `y12`, `y13`,
   `y14`, `y16`, `KHUNG_JOB` cho các bước và job mới; ca canh `ADR-0068` Q4 (không job nào thuộc một nhóm có `if:` theo
   `github.ref` hay `github.event_name`); ca canh bảng nhóm (tên job và tập chỉ số ma trận khớp `ci.yml`, mọi job ngoài `gate`,
   `chuan-bi` và `bien-nhan-cay` thuộc đúng một nhóm); ca canh "không job nào đọc output `*_bong`, không job nào `needs`
   `bien-nhan-cay`"; ca canh dạng chuẩn của `tai_dung_bo`.

## 4. nghiem_thu

| # | tiêu chí | phép đo làm nó ĐỎ | đột biến phải làm nó đổi màu |
|---|---|---|---|
| C1 | `python ops/ci_duong_nhanh_test.py` in dòng tổng `N/N` hai số bằng nhau, rc 0: trên Ubuntu (job `gate-ops` của PR) và trên máy Windows của chủ kho (`ADR-0060` M3: BASE và ứng viên, cùng máy, cùng lệnh) | số trước khác số sau, hay rc ≠ 0 | mỗi đột biến ở C2 |
| C2 | Mỗi chốt có ca riêng và **đột biến riêng** trong bảng đột biến của tệp test, chết đúng ca của nó (bộ phân hạng của tệp): (1) thiếu một khoá biên nhận ⇒ rc ≠ 0; (4a) sự kiện `pull_request`, `workflow_dispatch`, ref khác nhánh mặc định, `che_do` `duong_nhanh` — bốn; (4b) một cha, `before` khác P1 — hai; (4c) `head_repository` khác, `path` khác, `conclusion` khác, `run_attempt` 2 — bốn; (4d) `phien_ban` 2, `run_id` lệch, `cha` đảo thứ tự, `cay` lệch, `che_do` `duong_nhanh`, `anh_version` lệch, `anh_version` rỗng — bảy; (4e) `merge-tree` ra cây khác — một; (4f) một job `skipped`, một chỉ số vắng, một chỉ số lặp, một job `run_attempt` 2, bỏ chốt "mọi job" — năm, mỗi cái chỉ loại đúng nhóm của nó; (4g) phản chứng đổi tên của review lượt 1 (hai kế hoạch khác) ⇒ loại riêng `nhanh`; một `doc_diff` trả `None`, hai `doc_diff` trả `None` ⇒ loại riêng `nhanh`; diff rỗng thật cả hai bên ⇒ `nhanh` vẫn được; bỏ tham số `manh` ⇒ đột biến bị bắt; nạp `ci_dang_ky_test.py` lỗi ⇒ loại riêng `nhanh` — sáu; lỗi HTTP, JSON hỏng, zip hỏng, hết giờ ⇒ không nhóm nào — bốn; dạng chuẩn: đổi thứ tự, lặp tên, tên lạ — ba | một đột biến sống, hay chết vì lý do khác chốt | chính bảng ấy |
| C3 | Ca canh Q4, bảng nhóm, output bóng và `needs` đỏ khi: thêm bước có `if:` theo `github.ref` vào `gate-ops`; đổi `manh` của `gate-packet-loop-manh` thành 0–14; thêm `needs.chuan-bi.outputs.tai_dung_bo_bong` vào `if:` của một job; thêm `bien-nhan-cay` vào `needs` của `gate`; bỏ `continue-on-error` của một trong năm bước mới | ca vẫn xanh | năm đột biến YAML ấy (trên bản sao `ci.yml`, như các đột biến `yml_*` hiện có) |
| C4 | `actionlint` trên `ci.yml` không thêm finding so với BASE (delta 0, cùng nền có `shellcheck`) | thêm finding | — (cổng hiện hành) |
| C5 | Đo đầu-cuối trước land, mục 4 bên dưới | xem dưới | — (răng ở C2) |
| C6 | Sau land (**chưa đo được** tới lúc ấy): mười lượt `push` lên `master` đầu tiên sau commit land của B1, chọn theo thứ tự `created_at`, ghi id và SHA trước khi đọc kết quả. Mỗi lượt có dòng `TAI_DUNG_BONG`, có artefact `bien-nhan-tai-dung` đọc được với `che_do_xet` `bong`, và kết luận của lượt `push` không đổi so với lúc chưa có B1 (không job nào nghỉ vì B1). Mười lượt PR đầu tiên sau land có artefact `bien-nhan-cay`. Ghi số lượt `push` có nhóm tái dùng được, theo từng tập nhóm, và thời gian thêm của `chuan-bi` | một lượt thiếu dòng hay artefact; một job nghỉ vì B1 | — (quan sát CI thật; kiểm lại nội dung là việc của B2) |

C6 không đòi có lượt tái dùng; không có thì ghi "chưa quan sát được tái dùng", không phải đạt.

**C5 — phép đo đầu-cuối trước land.** Một workflow đo tạm trên nhánh `do-ci/**` (không merge, `permissions` đúng như
`chuan-bi`) chạy `xet-tai-dung` với môi trường giả lập lượt `push` lên `master`, cho một merge commit M′ dựng tại chỗ có cha
`[base, H]`, trong đó H là head PR của B1 và `base` là cha đầu của commit merge tổng hợp mà lượt PR xanh của H đã checkout
(đọc từ biên nhận). Tiền đề, đo và ghi **trước** khi chấm: lượt PR ấy `run_attempt` 1, đã hoàn tất xanh, đủ bốn nhóm chạy
`success` (B1 sửa `ci.yml`, tệp có trong `PHU_THUOC_PACKET_LOOP`, nên nhóm packet-loop chạy); hai diff registry khác `None` và
hai kế hoạch bằng nhau; job đo chạy trên cùng `ImageVersion` với `chuan-bi` của lượt PR. Thiếu tiền đề ⇒ ghi `not_measured`
và đo lại ở lượt PR kế, không phải lỗi thuật toán và không phải E1. Bốn vế, mỗi vế chỉ đổi một biến: (i) đủ tiền đề ⇒
`tai_dung_bo` bằng `,cong_cu,ops,nhanh,packet_loop,`, `tai_dung_run` bằng id lượt PR ấy; (ii) đổi biến `ImageVersion` ⇒
rỗng; (iii) M′ dựng trên một `base` khác có cây khác ⇒ rỗng; (iv) `before` khác `base` ⇒ rỗng. Đo thêm thời gian của năm bước
mới ở `chuan-bi` và thời gian của job `bien-nhan-cay` trên lượt PR của B1. Ghi trigger, quyền, giá trị `before`/ref/SHA giả
lập và hiện vật đọc lại.

Bảng năm vế của L6: C1 khớp dòng tổng `N/N` với điều kiện hai số bằng nhau (vế dương; vế âm là rc ≠ 0) — (b), (d) không áp
dụng vì dòng tổng do máy in một dòng, số bằng chữ số; (c) đếm theo từng đột biến ở C2; (e) không có lời khai "0 cổng". Dòng
`TAI_DUNG_BONG` ở C6: tiền tố cố định do mã in; nội dung do B2 kiểm lại.

## 5. luat_dung

- Trần kích thước: trần của khối `nang_tran` (550 dòng thêm) nếu chủ kho duyệt băm đặc tả này, không thì 450 của `ADR-0053`.
  Người thi hành đo `git diff --numstat` khi xong; vượt trần đang áp ⇒ dừng và hỏi chủ kho mã **E2**, mang `git diff
  --numstat` từng tệp, khối nào vượt ước, trần đang áp và trần xin, lý do không tách được. Không giảm độ phủ test để vừa trần.
- Trần lời gọi Codex theo bảng của `ADR-0055`. Chạm trần ⇒ hỏi chủ kho mã **E2**, mang số lời gọi đã dùng, finding còn mở
  và số lời gọi xin thêm.
- Điểm dừng §12 của protocol và Review Rescue Checkpoint của `ADR-0037`: dẫn nguyên, không chép.
- Lease khác đang giữ một đường dẫn của write set ⇒ chờ (phụ thuộc, không phải điểm hỏi).
- Cần sửa một tệp ngoài write set để giữ cổng xanh ⇒ dừng phiên, revision mới của đặc tả; không tự sửa; không phải điểm hỏi
  trừ khi revision ấy vượt trần (**E2** như trên).
- C5 vế (i) không đạt khi **đã đủ tiền đề**, sau khi đã xét lại thiết kế ⇒ hỏi chủ kho mã **E1**, mang: lệnh và mã HTTP của
  từng lần thử; gốc rễ đã xác định (ví dụ token của job không tải được artefact của lượt khác) và vì sao mỗi cách đã thử hỏng;
  phương án đề xuất.

## 6. pham_vi_e

- E4: **không chạm**.
- E5: **chạm** — sửa `ci.yml` (quyền `actions: read`, job mới) và bộ phân loại. Mỗi việc sau mang mã **E5**: chủ kho duyệt
  băm, cấp lease, audit trước merge. Mỗi lần hỏi E5 mang đủ ba thứ của bảng `ADR-0067`: **diff** (đặc tả này hay diff PR),
  **lý do** (dựng bộ xét tái dùng ở chế độ chạy bóng để đo trước khi bật), và **ai được thêm quyền gì** (job `chuan-bi` được
  quyền `actions: read` để đọc lượt và artefact của chính kho; không ai được thêm quyền ghi).

## 7. hinh_dang_ke_thua

`khong_ap_dung` — không phải packet khắc phục. Lớp lỗi người thi hành nên đọc trước: `kiem-re-cua-fail-close-chua-co-ca`
(#674, docstring `kiem_mode_git` của `ops/ci_duong_nhanh.py`) và lớp "canary chọn theo dự đoán" của
`THU-HOI-ADMISSION-MERGE-BASE-B`. Review lượt 1 và 2 bắt ba lớp: so nhầm consumer, chốt ghim bị bỏ sót, giá trị "không đo
được" bị đồng nhất với kết quả hợp lệ (N6). Cả ba nay có chốt riêng ở C2.

## 8. chua_do_duoc

- Token `github.token` với `actions: read` có tải được artefact của lượt khác qua REST `actions/artifacts/<id>/zip` hay
  không: chưa chạy trong kho này; C5 là phép đo đầu tiên.
- `ImageOS`, `ImageVersion` có mặt trong môi trường job `ubuntu-latest`: theo tài liệu runner-images; C5 đo.
- Thời gian thêm cho `chuan-bi` của lượt `push` và thời gian job `bien-nhan-cay`: chưa đo; C5 và C6 đo.
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
- Chốt `t161` (`ops/lease_publish_test.py`, `_kiem_tra_nguon_duy_nhat_os_ci`) chỉ soát job có `strategy.matrix.os` (đọc mã).

## 10. Thay đổi so với r1

Theo review lượt 2 (Codex, `changes_requested`, 7 P2, 3 P3):

- N1, N3, N9: lệnh `kiem-lai-tai-dung` chuyển sang B2 cùng hai chế độ (bóng, bật) và hợp đồng so đủ bằng chứng; B1 ghi đủ
  trường bằng chứng (gồm `che_do_xet`, blob `ci.yml`, id và `run_attempt` từng job, hai diff) để B2 kiểm. C6 của B1 chỉ quan
  sát, không chấm nội dung.
- N2: thêm `TAP_CHO_PHEP`, `y14` vào danh sách chốt ghim.
- N4: biên nhận PR chuyển sang job riêng không nằm trên đường chờ; mọi bước mới ở `chuan-bi` có `continue-on-error` và trần
  thời gian; C3 có đột biến bỏ `continue-on-error`; C5 đo thêm thời gian.
- N6: đọc hai diff riêng, loại `nhanh` khi một bên `None`; truyền `manh` như registry thật; thêm ba đột biến.
- N10: output `tai_dung_bo` ở dạng chuẩn, có ca và ba đột biến.
- N8: câu E1, E2, E5 mang đủ thứ phải mang theo.
- Ảnh runner của `chuan-bi` đi qua output của bước phân loại vào biên nhận, vì biên nhận nay do job khác tạo.
- N9: ước lại theo khối sau các sửa trên ra 455 dòng; thêm khối `nang_tran` (trần 550) để chủ kho duyệt cùng băm, thay cho
  việc người thi hành hỏi E2 giữa chừng.
