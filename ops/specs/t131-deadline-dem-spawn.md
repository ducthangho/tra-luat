# Đặc tả packet T131-DEADLINE-DEM-SPAWN — revision 1

| mục | nội dung |
|---|---|
| `packet_id` | `T131-DEADLINE-DEM-SPAWN` |
| `packet_issue` | `#676` |
| `nguon_cap_viec` | Nợ 1/3 của packet `#579` `DANG-LEASE-DAU-TRUOC-KIEM-SAU` (đã land: PR `#589` → `ddc41ec`; bookkeeping PR `#592` → `10e859d`), ghi trong human audit `pull/589#issuecomment-5857502345`. Đặc tả tiền nhiệm: `ops/specs/dang-lease-dau-truoc-kiem-sau-r30.md` (sha256 `c8a72a41f3678afa3638811eef59afc6b987e05eafec226748043dbcdb730dc2`), §0.29, §0.30. |
| `review_class` | `sensitive` — tệp là bộ test của cổng đọc lease; không rõ lớp ⇒ mức chặt nhất (protocol §8). |
| `base` | `origin/master` `1741e0a` (đo 05:55Z 29-09-2026). |

## 1. Vấn đề — đo được

Ca `t131_S8_tam_tran_bound_tru_1_bound_bound_cong_1_va_deadline` trong `ops/lease_publish_test.py`, đoạn
"deadline theo clock tiêm", chốt:

```python
chot(rc == 12 and "deadline" in td and "kill" not in td and kho.memo == {}, ...)
```

Nó suy "chặn TRƯỚC spawn" từ THÔNG ĐIỆP. Dưới đột biến `S8-bo-deadline` (bỏ `if con <= 0:` trong
`KhoObject._con_thoi_gian`, `ops/lease_publish.py`), `KhoObject.doc` vẫn spawn `cat-file`; nếu reader đọc xong mà
child chưa thoát thì `p.wait(timeout=0)` ném, và thông điệp "hết deadline reader chờ cat-file … kết thúc" cũng chứa
`deadline`, không chứa `kill`, `memo` rỗng ⇒ `t131` QUA sai.

Đo lại 05:4xZ 29-09-2026 trên bản sao tạm của `1741e0a` (20 lượt mỗi ô; script đo ở phụ lục A):

| lịch | `t131` gốc | `t192` gốc | `t131` đột biến | `t192` đột biến |
|---|---|---|---|---|
| L0 tự nhiên | xanh 20/20 | xanh 20/20 | đỏ 20/20 | đỏ 20/20 |
| L1 ép `join` chờ reader xong khi `timeout <= 0` | xanh 20/20 | xanh 20/20 | đỏ 20/20 (`rc=0`) | đỏ 20/20 (`rc=0`) |
| L2 = L1 + `Popen.wait(timeout <= 0)` ném `TimeoutExpired` | xanh 20/20 | xanh 20/20 | **xanh 20/20 — LỌT** | đỏ 20/20 (vế đếm spawn: "phải 0 lần spawn cat-file, có 1") |

Cửa ép được kích hoạt 20/20 lượt trên bản đột biến và 0/20 trên bản gốc ở L1/L2 — cột gốc xanh vì bản gốc
KHÔNG BAO GIỜ tới cửa ấy, không phải vì lịch ép câm.

`t192_S8_het_deadline_la_12_va_KHONG_spawn_cat_file_dem_bang_Popen` (thêm bởi `#579`) đã đo đúng thứ `t131` khai,
bằng cách đếm `subprocess.Popen`; catalog `t139` đã trỏ `S8-bo-deadline` về `t192`.

## 2. Quyết định của chủ kho (trong phiên 29-09-2026, "Đồng ý khuyến nghị")

- **Q1 = (b):** gỡ phần deadline khỏi `t131`, docstring khai rõ `t131` KHÔNG đo deadline-trước-spawn; `t192` là ca
  DUY NHẤT đo điều đó. Không đo trùng, không còn chốt suy từ thông điệp.
- **Q2:** `S8-bo-deadline` KHÔNG nhắm lại `t131`.
- **Q3:** write set ở §3; lease ghi phạm vi `cham_t131`; KHÔNG chạm `t132`.
- **Q4:** chạy `t125` A/B ≥ 40 lượt trên head cuối, đăng số làm căn cứ cho `#562`/`#619`.
- **Q5:** packet này đi trước hai packet anh em (`#579-nợ-2`, `#579-nợ-3`), nhưng CHỦ KHO xếp thứ tự.

## 3. `write_set`

- `ops/lease_publish_test.py` — CHỈ: thân và docstring của `t131`; chú thích dòng `S8-bo-deadline` trong catalog
  `t139`; docstring `t192` nếu câu "lease cấm chạm `t131`" cần sửa cho khỏi sai sau packet này.
- `ops/specs/t131-deadline-dem-spawn.md` — tệp này, chỉ mang theo; sha256 phải giữ nguyên ở head.

## 4. `ngoai_pham_vi`

- `t132` và mọi ca khác của `ops/lease_publish_test.py` — lease `#579` từng cấm `cham_t131_t132`; packet này chỉ mở `t131`.
- `ops/lease_publish.py` — hành vi sản phẩm đúng; lỗi nằm ở phép đo.
- Bảy trần bound, hai phép đo alternate, và phần "subprocess IM LẶNG bị kill" của `t131` — giữ NGUYÊN, không đổi
  một ký tự logic.
- Phần "trước deadline phải đọc được" (`deadline=100.5`) của `t131` — `t192` vế `100.5` đã đo đúng một spawn và
  `rc=0`; gỡ cùng phần deadline để `t131` không còn đoạn deadline nào. Nếu reviewer thấy cần giữ, đó là revision mới.
- Mọi packet anh em; mọi chạy CI/full CI trên PR (chủ kho cấm làm bằng chứng).

## 5. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Xoá đoạn "deadline theo clock tiêm" (hai khối `KhoObject(..., bay_gio=lambda: 100.0, deadline=...)`) khỏi `t131`. | `ops/lease_publish_test.py` |
| M2 | Docstring `t131` khai: không còn đo deadline; trỏ `t192`; nêu lý do (suy từ thông điệp, lịch L2 lọt 20/20). Tên hàm GIỮ nguyên (catalog `t139` và tài liệu tham chiếu tên). | `ops/lease_publish_test.py` |
| M3 | Chú thích dòng `S8-bo-deadline` trong `t139` bỏ vế "lease cấm chạm nó", thay bằng "`t131` không còn đo deadline (packet `#676`)". Ca đích vẫn `t192`. | `ops/lease_publish_test.py` |
| M4 | Docstring `t192`: câu "Lease cấm chạm `t131`/`t132`, nên phép đo nằm ở ca riêng" cập nhật cho đúng sau packet này. | `ops/lease_publish_test.py` |

## 6. `nghiem_thu` — mỗi tiêu chí kèm phép đo làm nó ĐỎ

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| N1 (M1) | `t131` gốc xanh 20/20 ở L0; trong thân `t131` không còn lời gọi nào mang keyword `bay_gio` (đo bằng `ast`, không `grep`). Khối subprocess-im-lặng dùng `deadline=time.monotonic() + 0.6` và KHÔNG có `bay_gio` — nó ở lại, nên phép đo KHÔNG được là "không còn `deadline=`". | Khôi phục một khối clock tiêm ⇒ phép đo `ast` đỏ. |
| N2 (M1) | `S8-bo-deadline` làm `t192` đỏ 20/20 ở L0 và 20/20 ở L2 (phụ lục A). | Gỡ vế đếm spawn khỏi `t192` trên bản sao ⇒ L2 xanh (đã đo ở `#579`: 4/20 khi bỏ chốt đếm). |
| N3 (M1) | Bảy trần + alternate + subprocess-im-lặng của `t131` vẫn có răng: `S8-bo-tran-parent` và `S8-bo-tran-tree-edges` (catalog `t139`) vẫn GIET qua `t131`. | Chính catalog `t139`: hai mutant ấy chuyển SỐNG ⇒ `t139` đỏ. |
| N4 (M3) | `t139`: mẫu số 37, giết thật 34, SỐNG có chủ đích 3, tín dụng giả 0 — bằng nền đo 05:54Z 29-09 trên `1741e0a`. | Bất kỳ số nào lệch ⇒ `t139` in dòng khác; đối chiếu số với nền. |
| N5 | `t125` A/B không lệch: 1 lượt trong gate; ≥ 40 lượt trên head cuối (Q4) và đăng số. | Một lượt lệch ⇒ ghi, không làm tròn; đó là dữ liệu cho `#562`/`#619`. |
| N6 | Toàn suite `ops/lease_publish_test.py` N/N (hai số BẰNG nhau); `t186` xanh (không thêm `len(<x>.calls)`). | Suite in N−k/N. |
| N7 | `ruff check --select F ops/lease_publish_test.py` delta so `1741e0a` = 0; `doctrine-scan` rc 0. | Delta ≠ 0. |
| N8 | Diff so merge-base chỉ chạm đúng §3. | `git diff --name-only` có tệp khác. |

## 7. `hinh_dang_ke_thua` (L4)

Từ `#579` (đặc tả r29 §0.29, r30 §0.30; cross-review lượt 36, 38, 39): lớp **chốt suy từ THÔNG ĐIỆP thay vì đo
SỰ KIỆN** — lần thứ ba trong chuỗi ấy (lượt 36 dựng được; lượt 38 `pull/589#issuecomment-5856770907` và lượt 39
`…-5857126562` lọt 5/5 lịch kiểm soát). `#579` đã chữa bằng thêm `t192` nhưng không gỡ được `t131` vì lease cấm.
Packet này đóng lớp ấy ở `t131` bằng GỠ, không bằng vá thêm một chốt văn bản.
Họ gần: CLAUDE.md "ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO".

## 8. `chua_do_duoc`

- Windows: không đo từ phiên này (chủ kho chưa cho chạy CI Windows).
- Effort thực tế của executor/reviewer: tự khai, không đo được từ ngoài.
- Lịch L2 là lịch mô phỏng (ép `join`/`wait` bằng patch). Lượt 38 của `#579` dựng lịch có kiểm soát theo cách riêng;
  hai cách chưa được đối chiếu với nhau — chỉ biết cả hai cho `t131` lọt.
- `t125` ≥ 40 lượt: chưa đo; đo trên head cuối (Q4).

## Phụ lục A — script đo

`chay.py <thu_muc> <ten_ca> <so_luot> <lich>`; `lich` = `0` (L0), `1` (L1), `2` (L2). `<thu_muc>` chứa bản sao
`lease_publish.py` + `lease_publish_test.py`; bản đột biến thay đúng một dòng `        if con <= 0:\n` →
`        if False:\n` (khẳng định đếm = 1).

```python
import sys, importlib.util, threading, collections
thu, ca, n = sys.argv[1], sys.argv[2], int(sys.argv[3])
kiem_soat = sys.argv[4] in ("1", "2"); ep_wait = sys.argv[4] == "2"
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location("lpt", f"{thu}/lease_publish_test.py")
m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
if kiem_soat:
    goc_join = threading.Thread.join
    dem_ep = [0]
    def join(self, timeout=None):
        if timeout is not None and timeout <= 0:
            dem_ep[0] += 1
            return goc_join(self)
        return goc_join(self, timeout)
    threading.Thread.join = join
    if ep_wait:
        import subprocess
        goc_wait = subprocess.Popen.wait
        def wait(self, timeout=None):
            if timeout is not None and timeout <= 0:
                raise subprocess.TimeoutExpired(self.args, timeout)
            return goc_wait(self, timeout)
        subprocess.Popen.wait = wait
f = getattr(m, ca); kq = collections.Counter()
for _ in range(n):
    try:
        f(); kq["XANH"] += 1
    except BaseException as e:
        kq["DO:" + type(e).__name__ + ":" + str(e)[:90]] += 1
print(thu, ca[:4], dict(kq), "ep_join=%s" % (dem_ep[0] if kiem_soat else "-"))
```
