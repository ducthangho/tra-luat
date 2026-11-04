# Đặc tả packet `CI-CONCURRENCY-MASTER` r1: mỗi commit master có group concurrency riêng, không lượt nào bị thay chỗ

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `CI-CONCURRENCY-MASTER`, revision 1, generation 1 |
| packet_issue | #1132 (dùng chính Issue lỗi làm Packet Issue, như #1120 cho `KIEM-MERGE-M9`) |
| nguon_cap_viec | Issue #1132 của chủ kho (01-11-2026), mục *Đề xuất* 1 và 3. Chủ kho mở phiên riêng ngày 02-11-2026 (`session_015GtxrcJvhJaXc7eNPaoNM4`), chốt chín câu hỏi Q1–Q9 bằng một câu: *"Đồng ý tất cả"* |
| review_class | `sensitive`: chạm `.github/workflows/**`, tức cổng gác phát hành |
| base | `origin/master` lúc cấp lease (đo khi soạn, 02-11 ~01:25Z: `9091cf5`) |
| executor / reviewer | `anthropic_claude`, chính phiên soạn spec (Q8) / `openai_codex` qua `launcher.py run` trên clone độc lập, và connector `@codex review` trên PR draft |
| windows | `not_required`, **do chủ kho quyết** (Q6). Theo M3 bước 2, mặc định là `required`. Lý do miễn: biểu thức `concurrency` do máy chủ GitHub đánh giá, không chạy trên runner nào. Windows CI theo ma trận vẫn chạy như thường |
| full_mutant_audit | bắt buộc (M9: diff chạm `.github/workflows/**` và `ops/**/*.py`), chủ kho **giữ** (Q6) |

## 1. Vì sao: số đo

| # | sự kiện | số đo |
|---|---|---|
| S1 | khối hiện tại | `.github/workflows/ci.yml` dòng 52–56: `group: ${{ github.workflow }}-${{ github.event.pull_request.number \|\| github.ref }}`, `cancel-in-progress: ${{ github.ref != 'refs/heads/master' }}`. Mọi push master rơi vào **một** group |
| S2 | hành vi GitHub | mỗi group giữ tối đa một lượt đang chạy và một lượt pending. Có lượt mới vào hàng thì lượt pending cũ bị huỷ, 0 job. `cancel-in-progress: false` chỉ bảo vệ lượt **đang chạy** |
| S3 | đã xảy ra (đo 01-11) | 5 commit master có lượt push bị huỷ, 0 job: `f2102fc` 41336643336 · `de06112` 41336765681 · `b01c0ac` 41339603053 · `c165a5d` 41356843718 · `2609cd8` 41357029677 |
| S4 | còn chưa có run `success` (đo 02-11 ~01:20Z) | `b01c0ac`, `2609cd8`. Ba commit kia đã có run qua đường vòng: `f2102fc` dispatch 41356691133 · `c165a5d` dispatch 41361081437 (#1140) · `de06112` attempt 2 của 41336765681 |
| S5 | đang xảy ra (đo 02-11 ~01:25Z) | `9091cf5`, run 41370526683, `pending` sau `c7174bf` (41365578445, `in_progress`). Lần push master kế tiếp sẽ huỷ nó |
| S6 | cùng lớp lỗi | `.github/workflows/launcher-windows.yml` dòng 38–40: khối y hệt S1 |
| S7 | máy đang khoá khối cũ | `ops/ci_duong_nhanh_test.py` dòng 2704 (`KHUNG_TOP`, ca `y13_khoa_topology_cua_ci_yml_ngoai_than_run`) chép nguyên văn `group` cũ. Đột biến `yml_concurrency_luon_huy` ở dòng 3730 neo vào dòng `cancel-in-progress`. `launcher-windows.yml` **không** có ca nào khoá concurrency (đo bằng `grep -n concurrency` trên `ops/*.py` và `.claude/dev/*.py`) |
| S8 | chi phí | kho `public`; `billable.UBUNTU.total_ms = 0` trên run 41360582742 (`run_duration_ms` 1181000). Không đo được là có tốn tiền hay không. Chi phí thấy được là **số job chạy đồng thời**: run 41360582742 có 15 job Ubuntu |

## 2. Thay đổi

### 2.1 `ci.yml` và `launcher-windows.yml`

Ở cả hai tệp, `group` đổi thành (nguyên văn, một dòng):

```
group: ${{ github.workflow }}-${{ github.event.pull_request.number || (github.ref == 'refs/heads/master' && github.sha) || github.ref }}
```

`cancel-in-progress` **giữ nguyên**. Hệ quả theo sự kiện:

- PR: group theo số PR như cũ. Lượt mới huỷ lượt cũ như cũ.
- push hoặc dispatch trên master: mỗi SHA một group. Hai commit khác nhau không thay chỗ nhau. Đánh đổi (chủ kho đã chấp nhận, Q2): các lượt master chạy song song và tranh slot job đồng thời với PR. Thứ phải chịu là **chờ runner**, không phải **mất gate**.
- push hoặc dispatch trên nhánh khác master: group theo ref như cũ.
- Còn một ca: hai lượt trên **cùng một** SHA master (vd. dispatch gate lại) vẫn chung group. Lượt thứ ba trên cùng SHA sẽ thay chỗ lượt thứ hai đang pending. Ca này không làm mất gate của một commit nào, vì lượt thứ nhất vẫn chạy trọn trên đúng SHA đó.

Chú thích ngay trên `group` trong `ci.yml` (dòng 53–54, Issue gọi là dòng 45) viết lại để khai đúng hành vi: *GitHub giữ tối đa một lượt pending mỗi group, nên master có group riêng theo SHA; `cancel-in-progress: false` một mình không đủ*. Trích #1132. Chú thích **không** chứa cú pháp biểu thức Actions rỗng (bài học `ops-don-ref.yml`, run `31971137920`). `launcher-windows.yml` có thêm một dòng chú thích cùng nghĩa.

### 2.2 `ops/ci_duong_nhanh_test.py`

- `KHUNG_TOP['concurrency']['group']` đổi thành chuỗi mới ở §2.1, khớp từng byte.
- Ca mới `y13b_concurrency_master_theo_sha`. Ca đọc **cả hai** tệp workflow bằng YAML và đòi `concurrency.group` của mỗi tệp **bằng đúng** chuỗi §2.1 (vế dương, so nguyên chuỗi, không so chuỗi con). Ca cũng đòi `cancel-in-progress` bằng đúng biểu thức cũ (vế âm, chặn ai đó "vá" bằng cách tắt huỷ trên PR).
- Hai đột biến mới trong bảng đột biến của tệp, đích là ca tương ứng:
  - `yml_concurrency_group_ve_ref`: đưa `group` của `ci.yml` về chuỗi cũ S1 ⇒ `y13` **và** `y13b` đỏ.
  - `launcher_concurrency_group_ve_ref`: đưa `group` của `launcher-windows.yml` về chuỗi cũ ⇒ `y13b` đỏ. Nếu bộ đột biến của tệp chỉ biết đột biến `ci.yml` thì executor được thêm một cơ chế đột biến cho tệp thứ hai **trong cùng tệp test**. Không thêm được thì dừng và hỏi, không cắt đột biến.

## 3. Write set

`.github/workflows/ci.yml` · `.github/workflows/launcher-windows.yml` · `ops/ci_duong_nhanh_test.py` · `ops/specs/CI-CONCURRENCY-MASTER-r1.md` (chép **nguyên byte** từ nhánh lease vào commit đầu của nhánh thực thi). **Bốn tệp**, đếm theo `git diff --numstat <base> <H>`, ước khoảng 130 dòng thêm, tính cả tệp đặc tả. Trần `ADR-0053`: 6 tệp / 450 dòng thêm.

**Ref ngoài write set, khai trước:** nhánh thử `ops/thu-concurrency-1132` (§4, A5). Nhánh này chứa đúng một tệp workflow thử, **không** merge vào master. Phiên web không xoá được ref, nên sau khi land phải dọn bằng `ops-don-ref.yml`. Việc dọn phải xin chủ kho, vì cần gõ `XOA`.

## 4. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `python ops/ci_duong_nhanh_test.py` ra N/N, hai số bằng nhau, N = nền + 1 (thêm `y13b`) | bất kỳ ca đỏ; N ≠ nền + 1 |
| A2 | đo nền trước khi sửa: chạy `y13b` (đã viết) trên `ci.yml`/`launcher-windows.yml` **của base** ⇒ phải **ĐỎ** ở cả hai tệp. Ghi output vào biên bản | `y13b` xanh trên base ⇒ ca không đo gì, đỏ |
| A3 | hai đột biến §2.2 bị giết **đúng ca đích**, tức chết ở assertion của `y13b` hoặc `y13`. Traceback hay lỗi vô can không tính. Đột biến cũ `yml_concurrency_luon_huy` vẫn bị giết | đột biến sống, hoặc chết ngoài ca đích ⇒ đỏ |
| A4 | `actionlint` trên hai tệp workflow: delta so `origin/master` = 0. `actionlint` thiếu ⇒ `KHÔNG ĐO ĐƯỢC`, đỏ. Ghi kèm `shellcheck` có mặt hay vắng (bài học 23-08) | finding mới ⇒ đỏ |
| A5 | **phản chứng trên GitHub thật**: nhánh `ops/thu-concurrency-1132`, workflow `thu-concurrency.yml`, chỉ `on: push` cho đúng nhánh đó, một job `sleep 120`. Thay `refs/heads/master` bằng `refs/heads/ops/thu-concurrency-1132` để nhánh thử đóng vai master. **Vế cũ:** khối S1, đẩy một commit mồi, rồi ba commit cách nhau ≤ 15 s ⇒ lượt **giữa** phải `cancelled`, 0 job (`runner_id` vắng). **Vế mới:** khối §2.1, cùng thủ tục ⇒ cả ba lượt `success`. Biên bản ghi SHA và run id của cả 8 lượt (mỗi vế 1 mồi + 3), lấy bằng `list_workflow_runs` lọc theo nhánh. Lần đẩy đầu không sinh lượt nào thì ghi `vắng mặt`, đừng đoán nguyên nhân | vế cũ không ra `cancelled` ⇒ phản chứng không tái hiện được lỗi: **dừng, hỏi chủ kho**, không kết luận gì cho vế mới. Vế mới có lượt `cancelled` ⇒ đỏ |
| A6 | `git diff --numstat <base> <H>`: đúng bốn tệp §3, ≤ 450 dòng thêm | tệp thứ năm ⇒ đỏ |
| A7 | chú thích `ci.yml`: vế âm `rg -F "phải chạy trọn" .github/workflows/ci.yml` ⇒ 0 dòng trong khối `concurrency`. Vế dương: đoạn chú thích mới (nối dòng trong phạm vi đoạn, L6b) chứa cụm `một lượt pending` và `#1132` | còn câu cũ, hoặc thiếu một trong hai cụm ⇒ đỏ |
| A8 | `doctrine-scan`, `adr-song`, `doc-claims-check` xanh, delta so master = 0 | — |
| A9 | M9: một lượt `ci-dot-bien-du.yml` (`workflow_dispatch` trên nhánh thực thi) `success` tại head cuối. `kiem-merge` trên PR với readback của lượt ấy ra rc 0 **trước khi bỏ draft** | run đỏ ⇒ sửa hoặc hỏi chủ kho, không tự miễn |
| A10 | CI PR của ứng viên xanh, đọc `labels` từng job. Chú ý: chính PR này **không** đo được hành vi master mới. Hành vi ấy chỉ đo được sau land, ở A11 | — |
| A11 | **chưa đo được tới sau land.** Hai push master liên tiếp đầu tiên sau merge: cả hai phải có lượt `ci.yml` push chạy job thật (`runner_id` ≠ 0), không lượt nào `cancelled` vì concurrency. Người đo: executor, hoặc phiên land. Bằng chứng đọc lại: `list_workflow_runs` branch=master event=push | một lượt master `cancelled`, 0 job ⇒ mở lại #1132 |

## 5. Ngoài phạm vi

- **Chốt hậu kiểm** (#1132 đề xuất 2: mỗi commit first-parent master phải có run `success`). Packet sau (Q1).
- **Gate lại** các commit chưa có run `success`: `b01c0ac`, `2609cd8`, `9091cf5` nếu S5 xảy ra, và mọi commit khác đo được lúc land. Chỉ **đề xuất** sau land, không chạy trong packet (Q9).
- Các workflow khác: `ops-don-ref.yml` (`cancel-in-progress: false` có chủ đích, group riêng) và `ops-open-pr.yml` (`cancel-in-progress: true`) không gác master theo push. Không đổi.
- `ci-dot-bien-du.yml`: không đọc khối concurrency ở packet này.

## 6. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục của một packet có biên nhận. Đường đi vòng M8 ở #1120 (issuecomment-6566496567, PR #1140) là thao tác vận hành, không có bộ đếm hình dạng lỗi để chép.

## 7. `chua_do_duoc`

- Giới hạn job đồng thời của gói tài khoản và thời gian chờ runner khi hai lượt master chạy song song: chưa đo. Sẽ thấy ở A11.
- Có tốn tiền hay không (S8 `billable` = 0): không đo được từ phiên này.
- Hành vi của GitHub ở S2 có tài liệu và có 5 lần quan sát (S3). A5 là phản chứng chạy được duy nhất. Nếu A5 vế cũ không tái hiện được thì mệnh đề S2 vẫn ở trạng thái quan sát, chưa phải phép đo.
