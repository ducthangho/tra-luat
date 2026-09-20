# SPEC — WINDOWS-FIXTURE-POSIX-t131-t132, revision 1

Packet Issue: **#578**. Kế thừa từ #541 (đã LANDED), nơi hai ca này bị `prohibited_actions`
cấm vá vì ngoài phạm vi spec r3.

## Mục tiêu

`t131` và `t132` của `ops/lease_publish_test.py` phải **đo được điều chúng khai** trên Windows
thật, hoặc — nếu không đo được — phải **khai thẳng** là không đo được, chứ không xanh rỗng.

Đây **không** phải packet "làm cho hai ca xanh". Một ca xanh vì fixture bị nới lỏng cho tới khi
nó thôi ném là một ca vô dụng, và tệ hơn ca đỏ: nó tuyên một điều chưa ai đo.

## Hai khuyết tật — đã định vị, ghi kèm để không phải tìm lại

### M1 — `t131`: fixture viết script `.sh` rồi bắt nền chạy

`ops/lease_publish_test.py`, trong thân `t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline`:

```python
im = s / "git-im-lang.sh"
im.write_text("#!/bin/sh\nsleep 30\n", encoding="utf-8"); im.chmod(0o755)
```

Trên Windows: `chmod(0o755)` gần như vô nghĩa, shebang không được nền đọc, `subprocess` nạp
thẳng một `.sh` cho ra `OSError: [WinError 193] %1 is not a valid Win32 application`.

Hệ quả **phải khai**: điều `t131` khai trong docstring — *bảy trần count/byte/depth biên
INCLUSIVE*, *deadline theo clock tiêm*, *subprocess im lặng bị KILL* — **chưa từng được đo trên
Windows**. Ca chết trước khi tới đó.

Cùng lớp với #570 (`t35–t40`). #570 đã dựng `ops/bash_nen.py`, bộ giải bash **quyết bằng phép
thử NĂNG LỰC** chứ không lọc theo tên. Rất có thể đó là thứ M1 cần — **phải đo, không được suy**.

### M2 — `t132`: `unlink()` loose object của `.git` khi tiến trình git có thể còn giữ

```python
loose = cay / ".git" / "objects" / c1[:2] / c1[2:]
chot(loose.is_file(), "fixture cần loose object của c1")
loose.unlink()
```

POSIX cho `unlink` một tệp đang mở; Windows thì không. Trước dòng ấy ca đã chạy
`git clone --depth=1`, `git fetch --unshallow`, và mở/đóng `KhoObject`.
Quan sát được: `PermissionError: [WinError 5] Access is denied` trên đúng đường
`…\lp_*\kho\.git\objects\<2>\<38>`.

**KHÔNG cùng gốc với `CASE T6` của #568** — đã đo: T6 nổ ở `td.cleanup()` trong `finally`,
còn M2 nổ ở thân ca; và `class San.__exit__` dùng `shutil.rmtree(..., ignore_errors=True)`
nên không thể ném. Gộp hai thứ này là ghi một nguyên nhân sai vào hồ sơ.

## Tiêu chí nghiệm thu

| | |
|---|---|
| **N1** | `t131` **QUA** trên Windows thật, và ca đó thực sự chạy tới phần deadline/kill — chứng minh bằng một chốt đọc được trong đầu ra, không phải bằng việc nó không ném. |
| **N2** | `t132` **QUA** trên Windows thật, và bước "xoá loose object" thực sự xảy ra — chốt phải phân biệt được "đã xoá" với "bỏ qua vì không xoá được". |
| **N3** | Cả hai ca **vẫn QUA trên Linux**. Không được chữa Windows bằng cách làm hỏng POSIX. |
| **N4** | Mỗi ca giết được **ít nhất một đột biến** nhắm đúng hành vi nó khai, và giết **đúng lý do** (neo LÝ DO, không chỉ neo `rc`). |
| **N5** | Nếu một phần của `t131` **không đo được** trên Windows, khai thẳng bằng `KHÔNG ĐO ĐƯỢC` và nêu vì sao — **không** im lặng bỏ phần ấy. |
| **N6** | Kích thước: **≤ 1 tệp, ≤ 250 dòng thêm**, đo bằng `git diff --numstat` so `merge-base(origin/master, HEAD)`. Vế nền tính bằng **phép tính**, không ghim hằng số. |

## Phạm vi

**Trong:** `ops/lease_publish_test.py` — chỉ thân hai ca `t131`, `t132` và các trợ thủ chúng dùng riêng.

**Ngoài, cấm chạm:**
- `ops/lease_publish.py` — mã sản phẩm. Nếu phép đo cho thấy khuyết tật nằm ở **đó**, **DỪNG** và xin revision; đừng vá lén qua đường test.
- `CASE T6` (#568) · `t35–t40` (#570) · `t125` (#562) · `t150` (#552) · `r378` (#574).
- `.github/workflows/**` · `ops/cong_cu.py` · `ops/bash_nen.py`.

`ops/bash_nen.py` **được đọc và được gọi**, nhưng không được sửa — nó thuộc write set của #570.

## Kỷ luật bắt buộc

- **"Một cổng không thể ĐỎ thì không phải cổng."** Trước khi dùng một chốt để phán quyết, bắt nó giết một đột biến đã biết trước.
- **Fail-close ba trạng thái**: `có` / `không` / `KHÔNG ĐO ĐƯỢC`. Trạng thái thứ ba làm cổng ĐỎ. Đừng làm tròn LÊN (#401).
- **Không gọi hai ca này là "chập chờn".** Chúng đỏ **có quy luật** trên Windows và xanh trên Linux — khác biệt nền, không phải ngẫu nhiên.
- **Phán quyết cuối đo trên Windows thật.** Executor chạy trên đám mây, không có Windows; chủ kho chạy hộ và gửi log. Log phải **TỰ KHAI** `sha256` bộ đo, bản, và `ref` nào trỏ tới HEAD.
- Một hình dạng lỗi lặp lần thứ **BA** ⇒ DỪNG, hỏi *"có nên làm việc này không"*.

## Điều kiện dừng

- Vượt 1 tệp hoặc 250 dòng thêm ⇒ DỪNG, handoff.
- Phải chạm `ops/lease_publish.py` hay bất kỳ đường nào ngoài write set ⇒ DỪNG, xin revision.
- `ai-dang-giu` cho `ops/lease_publish_test.py` trả khác `rc=0` / `NGƯỜI_GIỮ 0` ⇒ **chưa được chạm**.
