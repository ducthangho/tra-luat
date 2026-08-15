# Hướng dẫn kích hoạt `ops-mirror-spec` — 5 bước, dừng được ở bất kỳ bước nào

Viết cho PowerShell trên Windows (`D:\Quốc hội\tra-luat`). **Mỗi lệnh một dòng** — lần
trước hỏng vì tôi đưa cú pháp nối dòng `\` của bash.

Trạng thái hiện tại: bản chiếu #119 **đã có khối `mirror`** và đã kiểm `check` rc=0.
Workflow **chưa có trong kho**, nên chưa có gì tự chạy. Bạn đang ở vạch xuất phát an toàn.

---

## Bước 0 · đồng bộ và tự kiểm (chưa đổi gì)

```powershell
cd 'D:\Quốc hội\tra-luat'
git fetch --prune origin
git checkout ops/successor-packet-session-mutex
git pull --ff-only origin ops/successor-packet-session-mutex
```

Kiểm mỏ neo — hai lệnh này phải ra CÙNG một con băm:

```powershell
Get-FileHash -Algorithm SHA256 ops\specs\wp119-r1-spec.md | Select-Object -Expand Hash
```

Đòi `1740B1C5C0B999C48C24B4AEAD29A6BC9B97C58EB483D42DD0A03714C9CE0A97`
(PowerShell in HOA; so không phân biệt hoa thường với `1740b1c5…`).

---

## Bước 1 · ĐẶT RULESET TRƯỚC — đừng merge rồi mới đặt

Đây là việc duy nhất đóng nốt phần còn thủng. Chưa có nó thì cửa này quy về
*"ai push được vào `ops/**` thì GHI ĐÈ được thân issue"*.

GitHub → repo → **Settings → Rules → Rulesets → New ruleset → New push ruleset**:

- **Enforcement status**: `Active`
- **Bypass list**: thêm chính bạn (`ducthangho`) — nếu không, chính bạn cũng không sửa
  được workflow nữa.
- **Rules → Restricted file paths**, thêm hai mẫu:

```
.github/workflows/**
ops/mirror_spec*.py
```

Cân nhắc thêm `ops/lease_publish*.py` — cửa lease đang có cùng khuyết ấy và chú thích
trong `ops-publish-lease.yml` đã tự khai.

> **Tôi không kiểm được bước này từ phiên agent** (`api.github.com` trả 403), nên tên
> menu có thể lệch chút theo phiên bản GitHub. Nếu không thấy "push ruleset", dùng
> **branch ruleset** cho `master` với cùng danh sách đường dẫn — hiệu quả tương đương cho
> đường merge, nhưng KHÔNG chặn push thẳng vào nhánh `ops/**`. Khác biệt ấy đáng biết.

**Kiểm đã ăn chưa:** thử push một sửa đổi vặt vào `.github/workflows/ci.yml` từ một nhánh
phụ. Phải bị TỪ CHỐI. Nếu qua trơn thì ruleset chưa ăn — dừng, đừng đi tiếp.

---

## Bước 2 · áp diff và đưa vào master

```powershell
git checkout master
git pull --ff-only origin master
git checkout -b ops/them-mirror-spec
git apply ops\proposals\ops-mirror-spec.diff
git status
```

`git status` phải hiện ĐÚNG 3 tệp mới, không hơn:

```
.github/workflows/ops-mirror-spec.yml
ops/mirror_spec.py
ops/mirror_spec_test.py
```

Chạy bộ phản chứng TRƯỚC khi commit:

```powershell
python ops\mirror_spec_test.py
```

Đòi `nền: 21/21 đạt`, 9 dòng `ok  <đột biến> → giết …`, và `mirror_spec: ĐẠT`.
**Bất kỳ dòng `ĐỎ` nào ⇒ dừng, đừng commit.**

```powershell
git add .github/workflows/ops-mirror-spec.yml ops/mirror_spec.py ops/mirror_spec_test.py
git commit -m "ops: cầu git->API chiếu spec len than Issue, kem 21 phan chung + 9 dot bien"
git push -u origin ops/them-mirror-spec
```

Rồi mở PR vào `master` và **tự review**. Ba câu nên hỏi khi đọc diff:

1. `permissions` có đúng `contents: read` + `issues: write` không? Có `contents: write`
   là sai — cửa này không ghi ngược gì vào kho.
2. Step "lấy NHÁNH MẶC ĐỊNH" có còn nguyên không? Đó là lớp 4 (finding P1 của PR #104).
   Mất nó thì bộ kiểm nằm cùng nhánh với thứ nó kiểm.
3. Chốt `guard` có còn `startswith` không? Đổi thành `in` là mở cửa cho dấu giả mạo nằm
   giữa bài — `t20` bắt đúng chuyện đó.

**Chưa merge thì chưa có gì chạy.** Workflow chỉ sống khi có mặt trên nhánh được push.

---

## Bước 3 · kích hoạt lần đầu — chuẩn bị thân #119

Chốt QUYỀN SỞ HỮU sẽ **từ chối** ghi đè một thân do người viết. Nên lần đầu bạn phải tự
mở khoá, chọn MỘT trong hai:

- **Cách A (khuyến nghị)** — xoá trống thân #119 trên web, lưu. Thân rỗng ⇒ cho ghi.
- **Cách B** — dán đúng một dòng này lên đầu thân hiện tại rồi lưu:

```
<!-- ops-mirror-spec v1 -->
```

Sau đó push bản chiếu KÈM NHÃN kích hoạt:

```powershell
git checkout ops/successor-packet-session-mutex
git commit --allow-empty -m "wp119: chieu spec len than #119 [mirror-spec]"
git push origin ops/successor-packet-session-mutex
```

> Commit rỗng KHÔNG kích hoạt được: bộ lọc `paths` của GitHub đòi tệp
> `ops/specs/**-than-issue.md` phải THAY ĐỔI trong lượt push. Nếu muốn chạy mà không sửa
> nội dung thật, thêm một dòng trắng vào cuối bản chiếu rồi commit kèm `[mirror-spec]`.
> Tôi ghi rõ chỗ này vì nó là cái bẫy dễ mất 15 phút.

---

## Bước 4 · xác minh, và biết dấu hiệu hỏng

Vào tab **Actions → "ops — chiếu spec lên thân Issue bằng git"**. Log phải có:

```
nền: 21/21 đạt                  ← bộ kiểm của NHÁNH MẶC ĐỊNH chạy trước
ok: chiếu ops/specs/wp119-r1-spec.md → issue #119, băm khớp 1740b1c5c0b9…
cho ghi đè thân #119 — thân rỗng
đã chiếu ops/specs/wp119-r1-than-issue.md → thân issue #119
đọc lại KHỚP BYTE ✓
```

Dòng cuối là dòng quan trọng nhất. Kho này ĐÃ TỪNG bị đường đăng làm biến dạng ký tự —
thân #55 tới giờ còn `&#34;` nguyên văn ở đúng chỗ đáng ra là dấu nháy kép. Nếu thấy:

```
⚠ đọc lại LỆCH — đường đăng làm biến dạng nội dung:
```

thì job ĐỎ và **thân #119 đã bị ghi bằng nội dung méo**. Xử lý: đọc phần `diff` trong log
để biết ký tự nào bị đổi, rồi báo lại — đó là dữ liệu quý, nó xác nhận lớp mã hoá vẫn
hỏng và ảnh hưởng tới mọi đường đăng khác của kho.

Các dòng CHẶN thường gặp và nghĩa của chúng:

| log | nghĩa | sửa |
|---|---|---|
| `CHẶN(6): băm spec LỆCH` | sửa spec mà quên cập nhật bản chiếu | cập nhật `spec_hash` trong khối `mirror` |
| `CHẶN(8) thân #119: … do NGƯỜI viết` | chưa mở khoá | làm Bước 3 |
| `CHẶN(8): packet_issue LỆCH` | bản chiếu và spec khai hai số khác nhau | sửa cho khớp |
| `thân #119 đã đúng nội dung — KHÔNG gọi PATCH` | **không phải lỗi** — chốt idempotent | không cần làm gì |

---

## Bước 5 · lùi lại nếu đổi ý

Cửa chưa merge: xoá nhánh `ops/them-mirror-spec`, xong.

Cửa đã merge và bạn muốn tắt: đổi `Enforcement` hoặc revert commit. Cách nhanh nhất mà
không đụng git — **xoá nhãn khỏi thói quen**: không commit nào mang `[mirror-spec]` thì
workflow không bao giờ chạy. Nó là opt-in tường minh, không phải cơ chế nền chạy ngầm.

Thân issue đã bị ghi đè thì **không tự khôi phục được** — GitHub không giữ lịch sử thân
issue qua API. Đó chính là lý do Bước 3 bắt bạn tự mở khoá bằng tay, và lý do chốt quyền
sở hữu tồn tại.

---

## Thứ tự KHÔNG được đảo

```
Bước 1 (ruleset)  →  Bước 2 (merge)  →  Bước 3 (kích hoạt)
```

Merge trước khi có ruleset là mở một cửa GHI ĐÈ mà chưa có khoá. Với cửa chỉ thêm comment
thì đảo thứ tự còn chấp nhận được; với cửa ghi đè thì không.
