# ĐẶC TẢ PACKET — `CONG-CI-PACKET-LOOP` (Issue #277)

```yaml
packet_id: CONG-CI-PACKET-LOOP
packet_issue: 277
revision: 1
generation: 1
review_class: sensitive          # cham .github/workflows/** = duong gac cong phat hanh
executor: claude
reviewer: codex
assurance_target: cross_approved
```

## 0. Vấn đề — một dòng, đo được

```
grep -rn "packet_loop" .github/          ⇒  0
```

`packet_loop_test.py` (231 ca, 58 đột biến, 78 lớp lách) **không có cổng CI nào**. Mọi con số của
mọi packet chạm `.claude/dev/packet_loop*` tới nay đều là **lượt chạy TAY, một nền, phần lớn do
chính người thi công chạy**. Hai P1 của #262 lọt vòng 1 mà không cổng nào thấy.

Và `case_luong_canonical_chay_that` (N10′) — ca **chỉ đo thật trên Windows** — **chưa từng được đo**:
trên Linux nó in `BO QUA n10 (nen posix)`, trên Windows không ai gọi nó.

## 1. `write_set`

```
.github/workflows/ci.yml
.claude/dev/packet_loop_test.py      # CHI khi can co tach nen (M3)
```

Hai đường. Nếu M3 giải được mà không đụng tệp thứ hai thì **đừng đụng**.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **2** |
| dòng thêm tối đa | **90** |

Thấp có chủ ý: packet này là **một step CI cộng (có thể) một cờ**. Vượt ⇒ **DỪNG và NÉN**.
Thấy mình đang viết hơn 90 dòng nghĩa là đang làm một packet khác.

## 3. `muc_tieu`

| # | mục tiêu | tệp |
|---|---|---|
| **M1** | `ci.yml` chạy `packet_loop_test.py`, và **N10′ phải THẬT SỰ ĐO trên `windows-latest`** | `ci.yml` |
| **M2** | Chi phí phút Actions thêm vào **ĐO TRÊN RUNNER THẬT**, ghi vào PR. Ước tính của Issue #277 là cận dưới đo trên container 4 nhân — **KHÔNG được chép lại làm kết quả** | — |
| **M3** | Nếu tách nền (đột biến Linux-only): suite phải có cờ tách, và **thiếu cờ ⇒ CHẠY ĐỦ** | `packet_loop_test.py` |

## 4. `nghiem_thu`

| # | nghiệm thu | phép đo làm nó ĐỎ |
|---|---|---|
| **N1** | `grep -rn "packet_loop" .github/` ⇒ khác 0 | hiển nhiên |
| **N2** | Log job `windows-latest` **KHÔNG** chứa `BO QUA n10` | đọc log job thật, không đọc YAML |
| **N3** | Một đột biến vào `packet_loop.py` làm **job CI ĐỎ** | đẩy đột biến lên một nhánh thử, ĐO job. **Đây là ca quan trọng nhất**: nó phân biệt cổng CÓ RĂNG với cổng CÓ MẶT |
| **N4** | Cờ tách nền: **thiếu cờ ⇒ chạy ĐỦ**; đột biến đảo mặc định thành "bỏ đột biến" ⇒ ca ĐỎ | ca trong `packet_loop_test.py` |
| **N5** | delta so master = 0 cho mọi cổng đang có | nền master đo **TRONG worktree của chính kho** |
| **N6** | Số phút ĐO trên runner được ghi vào PR, kèm **cả hai** con số: tường và tính-tiền | đọc `started_at`/`completed_at` của job |

## 5. Chi phí — số ĐÃ ĐO, và ranh giới của nó

Đo trên container Linux 4 nhân (**KHÔNG phải runner**; coi là **cận dưới**):

| | |
|---|---|
| toàn bộ suite | **79 s** |
| chỉ 231 ca | **34 s** |
| riêng phần đột biến (374 lượt chạy ca) | **45 s** |

Hệ số Windows đo từ hai job THẬT trên `7c54c9f`: `gate (ubuntu)` **340 s** · `gate (windows)` **454 s**
⇒ **×1,34 tường**. Actions **tính tiền Windows ×2**.

| phương án | thêm/lượt (tính tiền) | so nền ~1248 s |
|---|---:|---:|
| cả suite trên cả hai nền | **+291 s** | **+23 %** |
| đột biến Linux-only, ca chạy cả hai nền | **+170 s** | **+14 %** |

**Lý lẽ cho phương án 2 là LẬP LUẬN, không phải phép đo:** phần đột biến đo *răng của bộ test* —
logic thuần Python, không phụ thuộc nền; thứ phụ thuộc nền nằm trong các CA (`platform.system()`,
`mtime`, `os.name`, khối PowerShell của N10′). **Packet có quyền bác lập luận này bằng số.**

`r245` trong `ci.yml` ghi kho đã từng **cạn hạn mức Free ngày 11 hằng tháng** và CI đứng hình —
nên đây là ràng buộc thiết kế, không phải chi tiết.

## 6. `dieu_kien_dung`

- Đo trên runner thật thấy chi phí **vượt xa** §5 ⇒ DỪNG, báo số, hỏi người giữ kho TRƯỚC khi land.
- **Thấy mình định bỏ bớt ca cho rẻ ⇒ DỪNG.** Hạ tiêu chuẩn cổng để lọt ngân sách phút là đổi một
  cổng THẬT lấy một cổng TRANG TRÍ — đúng thứ packet này sinh ra để sửa.
- Vượt **90** dòng hoặc **2** tệp ⇒ DỪNG và NÉN, không nới.
- Thấy mình định sửa `packet_loop.py` (không phải `_test.py`) ⇒ DỪNG: đó là write set của #262,
  và #262 đang `blocked` với hai P1 mở.

## 7. `chua_do_duoc` — khai trước, đừng để reviewer phải tìm

- **Số ở §5 KHÔNG phải số runner.** Container này 4 nhân; runner GitHub có thể khác. M2 tồn tại
  chính vì thế. Ai chép §5 vào PR làm kết quả là vi phạm M2.
- **N3 đòi đẩy một đột biến lên một nhánh thử** để đo job ĐỎ. Nhánh ấy phải xoá sau, và phiên web
  **KHÔNG xoá được ref** — dùng `.github/workflows/ops-don-ref.yml`, hoặc nhờ người giữ kho.
- **Chưa đo được `packet_loop_test.py` chạy bao lâu trên Windows.** Vòng gà-và-trứng: phải nối vào
  workflow mới đo được. Lượt đo đầu tiên CHÍNH LÀ bằng chứng cho M2.
