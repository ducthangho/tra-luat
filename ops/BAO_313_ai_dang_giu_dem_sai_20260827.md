# BÁO #313 — `ai-dang-giu` đếm NGƯỜI_GIỮ cao hơn sự thật, HAI nguyên nhân độc lập

Phát hiện trong lúc điều phối #318/#319/#334 ngày 27-08-2026. Cả hai đều **tái lập được**, và cả
hai đều làm con số **CAO HƠN** sự thật — tức sai theo chiều AN TOÀN (thừa người giữ, chặn oan).
**Chiều nguy hiểm — làm MẤT một lease đang sống rồi cho phép cấp lease chồng — CHƯA AI ĐO.**

Cả hai đụng `ops/lease_publish.py`, NGOÀI mọi write set phiên này đang giữ. Nên đây là BÁO CÁO,
không phải bản vá.

---

## A. Đếm TRÙNG khi hai ref mang HAI PHIÊN BẢN NỘI DUNG của cùng một lease

### Nguyên nhân, đọc thẳng từ mã

`_quet_lease_toan_kho` (`ops/lease_publish.py:273`) khai ngay ở docstring:

> *"Đọc mỗi cặp (blob, đường dẫn) lease đúng một lần trên mọi ref cục bộ."*

Khoá chống trùng là `(blob, duong)` — tức **băm NỘI DUNG + đường dẫn**, KHÔNG phải `lease_id`.
Rồi `lenh_ai_dang_giu` (`:668`) gom vào một **LIST**:

```python
nguoi_giu.append(lease_id)
...
print(f"NGƯỜI_GIỮ {len(nguoi_giu)}: " + (", ".join(sorted(nguoi_giu)) or "không có"))
```

`list` chứ không phải `set`. Hai phiên bản nội dung ⇒ hai mục ⇒ `len()` đếm hai.

### Tái lập tối thiểu — có ĐỐI CHỨNG

```bash
git init tai_lap && cd tai_lap && mkdir -p ops/leases
# viết một lease hợp lệ bất kỳ, write_set: [duong/dan/thu.py], hết hạn 2099
git add -A && git commit -m A && git branch nhanh-B
# đổi ĐÚNG MỘT dòng ghi chú, KHÔNG đổi lease_id
git commit -am B
git remote add origin "$PWD"
git update-ref refs/remotes/origin/master master
git update-ref refs/remotes/origin/nhanh-B nhanh-B
python3 ops/lease_publish.py ai-dang-giu duong/dan/thu.py --root .
```

**Kết quả:**

```
CÒN_HẠN  thu-nghiem-exec-1-claude-20260827  refs/heads/master:...
CÒN_HẠN  thu-nghiem-exec-1-claude-20260827  refs/heads/nhanh-B:...
NGƯỜI_GIỮ 2: thu-nghiem-exec-1-claude-20260827, thu-nghiem-exec-1-claude-20260827
```

Cùng một `lease_id` in **hai lần** — bản in tự nó đã là bằng chứng.

**Đối chứng:** đồng bộ hai ref về cùng nội dung rồi chạy lại ⇒ `NGƯỜI_GIỮ 1`. Nên biến độc lập
đúng là *nội dung lệch*, không phải *có hai ref*.

### Gặp thật ngoài đời

`ai-dang-giu .claude/dev/mcp_gh_test.py` trả `NGƯỜI_GIỮ 2:
mcp-gh-cuu-ho-exec-1r6-codex-20260827, mcp-gh-cuu-ho-exec-1r6-codex-20260827` chỉ vì nhánh
**cục bộ** `ops/cap-lease-tach-314` tụt sau bản đã đẩy. Đồng bộ nhánh cục bộ ⇒ `NGƯỜI_GIỮ 1`.

### Lời khai của #313 ca 4 chưa đúng hết

Commit `d3897be` khai *"dem NGUOI_GIU theo LEASE chu khong theo (lease x ref)"*. Đúng **khi hai ref
cùng nội dung** — vì khoá `(blob, duong)` đã gộp chúng. **Hỏng khi nội dung lệch.** Lời khai nên
sửa cho khớp, hoặc dedup nên đổi sang `lease_id`.

### Hướng sửa

`nguoi_giu` thành `set`, hoặc dedup theo `lease_id` trước khi đếm. Và khi một `lease_id` xuất hiện
với **nhiều blob khác nhau**, đó tự nó là dữ kiện đáng in ra — nó nghĩa là sổ sách đang phân kỳ.

---

## B. Mỗi revision còn hạn bị tính thành MỘT người giữ riêng

### Đo được

`ai-dang-giu .claude/dev/packet_loop.py` ⇒ **`NGƯỜI_GIỮ 4`**:
`khoa-neo-be-rong` r2, r3, r7, cộng `uy-quyen-merge-neo-hien-vat-exec-1`.

Nhưng chuỗi thật là r1 → r2 → r3 → r4 → r5 → r6 → r7, mỗi bản đều có `thay_the_cho` trỏ ngược về
bản trước. Chỉ **r7** là bản sống.

### Nguyên nhân: MỘT sự thật lưu HAI CHIỀU, và chiều dư trôi lệch

`_phan_loai_lease` chỉ loại một lease khi chính nó mang `da_bi_thay_the` — **liên kết XUÔI**.
Đo trên kho:

| lease | `thay_the_cho` (ngược) | `da_bi_thay_the` (xuôi) |
|---|---|---|
| r1 | — | **THIẾU** |
| r2 | r1 | **THIẾU** |
| r3 | r2 | **THIẾU** |
| r4 | r3 | r5 |
| r5 | r4 | r6 |
| r6 | r5 | r7 |
| r7 | r6 | — (đúng, r7 là bản sống) |

r1, r2, r3 thiếu liên kết xuôi. r1 thoát vì đã HẾT_HẠN; r2 và r3 còn hạn nên bị tính.

**Nhưng liên kết xuôi là thứ SUY RA ĐƯỢC.** Mọi lease X mà có lease Y khai `thay_the_cho == X` đều
đã bị thay — không ngoại lệ. Suy từ chuỗi ngược trên chính kho:

```
NGƯỜI_GIỮ THẬT = 2  (khoa-neo-be-rong-exec-1r7, uy-quyen-merge-neo-hien-vat-exec-1)
Công cụ in     = 4
```

Sai **gấp đôi**.

### Đây KHÔNG chỉ là "ai đó quên điền trường"

Schema đang lưu **cùng một sự thật hai lần**, và bản dư trôi lệch — đúng bệnh mà `doctrine-scan`
sinh ra để chặn ở tầng tài liệu, nhưng chưa ai áp cho tầng lease. Bắt người soạn lease duy trì cả
hai chiều là bắt họ giữ đồng bộ hai bản chiếu bằng tay; ba trong bảy bản đã trượt.

Đáng nói thêm: cổng `_kiem_bia_mo` (land ở PR #316) **ĐÒI** chuỗi hai chiều và so `da_bi_thay_the`
bằng **CHUỖI VÔ HƯỚNG** — nên quan hệ *"một lease bị HAI lease thay"* không biểu diễn được. Phiên
này đã gặp: r4 của #314 bị #318 và #319 cùng thay, và chỉ mang được một tên. Đã báo #313 trước đó.

### Hướng sửa

Suy `đã bị thay` từ chuỗi `thay_the_cho` thay vì đòi điền tay; giữ trường xuôi làm **tuỳ chọn**
để đọc cho tiện, và nếu nó có mặt mà **mâu thuẫn** với chuỗi ngược thì `KHÔNG_XÁC_ĐỊNH` —
fail-close, đừng chọn một trong hai.

---

## Vì sao hai cái này đáng sửa dù đều sai theo chiều an toàn

Một phép đếm cao hơn sự thật thì **chặn oan**, và chặn oan dạy người ta bỏ qua phép đếm. Chính
phiên này đã hai lần suýt kết luận sai vì nó: một lần tưởng `mcp_gh_test.py` có hai người giữ,
một lần tưởng `packet_loop.py` có bốn. Cả hai lần đều phải đo tay mới ra sự thật.

Và cả hai lần đều bắt được **chỉ vì có người nghi con số**. Không tầng nào cảnh báo.

## Chỗ KHÔNG ĐO ĐƯỢC

- **Chiều nguy hiểm chưa ai đo**: nhánh cục bộ tụt sau LÀM MẤT một lease đang sống. Chốt fail-close
  của #313 ca 4 (`KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy chủ`) có vẻ đóng đúng đường ấy — phiên này
  gặp nó bắn thật một lần, đúng lúc một nhánh lease mới xuất hiện giữa hai lần đo. Nhưng chưa ai
  dựng ca chứng minh nó đóng HẾT.
- Chưa đo hành vi khi một `lease_id` xuất hiện với hơn hai blob.
- Không đăng được báo cáo này lên #313: proxy chặn mọi lời gọi `api.github.com` trong phiên này,
  kể cả `GET`. Tệp nằm trên nhánh `ops/cap-lease-tach-314`.
