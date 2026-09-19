# `R330-RIG-QUYET-MAU-VA-NGOAI-LE-BI-NUOT` — revision 1

| trường | giá trị |
|---|---|
| `packet_id` | `R330-RIG-QUYET-MAU-VA-NGOAI-LE-BI-NUOT` |
| `packet_issue` | #565 |
| `revision` | 1 |
| `executor` | `claude` |
| `assurance_target` | `human_audited` |
| `review_class` | `sensitive` — chạm `scripts/tl_selftest.py` (harness dùng chung) và `RELEASE_MANIFEST.json` |
| `base` | `dc85dd0a34188238aa6537ce843ff3688e488fd3` |

## `nguon_cap_viec`

Nợ #565. Chỉ thị chủ kho, nguyên văn nhãn phương án đã chọn: **"Cấp rộng — vá cả `_t110`"**
(bản chiếu: `issues/565#issuecomment-5742376675`).

## Hai khuyết tật — CÙNG GỐC, khác bán kính

Gốc chung: **rig quyết màu của phép đo thay vì nội dung được đo.**

### `Đ1` — `_goi` để `TemporaryDirectory.__exit__` quyết màu ca `r330`

Chuỗi năm mắt. Mỗi mắt có phép đo hoặc dòng mã, không mắt nào là suy diễn nối suy diễn:

| # | mắt | bằng chứng | đo lúc |
|---|---|---|---|
| 1 | `_goi` dùng `TemporaryDirectory()` làm **context manager**; `ignore_cleanup_errors` mặc định `False` ⇒ `__exit__` **NÉM** | `scripts/tl_selftest.py`, thân `_c330_deploy_msg_khong_chay_lenh` | đọc mã |
| 2 | Trên Windows `shutil.which("bash")` ra **alias WSL** | `C:\Windows\system32\bash.EXE`; `uname -s` → `Linux`; có `/mnt/c` | 19-09-2026, máy chủ kho |
| 3 | WSL **giữ handle trên cwd** sau khi tiến trình con trả về | **16/20 = 80%** thư mục tạm không xoá được, `PermissionError [WinError 32]` trên chính **THƯ MỤC** | 10:53Z 19-09-2026 |
| 4 | `__exit__` ném `PermissionError` ra ngoài `_goi` | hệ quả của (1)+(3) | — |
| 5 | `_t110` nuốt nó thành `cases.append((name, False))` | `scripts/tl_selftest.py`, thân `_t110` | đọc mã |

**Kiểm số học:** `_goi` được gọi **hai** lần mỗi lượt (`_goi(_old)` và `_goi(_new[0])`) ⇒
`P(≥1 lần hỏng) ≈ 1 − 0,2² = 0,96`. Quan sát thực **3 đỏ / 1 xanh = 75%** trên bốn lượt. `n = 4`
nên KHÔNG đòi khớp chính xác — đòi **cùng hướng và cùng bậc**, và nó đạt.

**Bốn quan sát mà `Đ1` giải thích, và không quan sát nào mâu thuẫn với nó:**

| quan sát | `Đ1` nói gì |
|---|---|
| Chập chờn | Tuỳ WSL đã nhả handle chưa — bản chất thời gian |
| Chỉ Windows | Không WSL ⇒ không giữ handle |
| Linux luôn xanh | Đo 15:58Z 19-09-2026 trên `dc85dd0a` trong container này: `tl --selftest` `rc=0`, **`1710/1710`**, `r330` **`[OK]`** |
| Không do bản vá | `deploy-package.sh` (`693ef9a46dca7d9c`) và `.ps1` (`03bcccba890844e6`) **giống nhau từng byte** ở hai vế |

**Một giả thuyết đã bị BÁC, ghi lại vì đó là dữ liệu chứ không phải lượt chạy phí:** bộ đo bản 2
được viết để bắt *"`goi.txt` hiện muộn ở phía Windows"*. Kết quả: `thay_ngay` **20/20**,
`hien_muon` **0**, `khong_hien` **0**, `hien_ra_sau_giay` max **0,0**. Cuộc đua hiển thị tệp
**không phải** nguyên nhân. `Đ1` đến từ một dòng phụ trong cùng log mà bộ đo không được viết để hỏi.

### `Đ2` — `_t110` nuốt MỌI ngoại lệ, phủ MỌI ca

```python
def _t110(name, fn):
    try:
        cases.append((name, bool(fn())))
    except Exception:
        if os.environ.get("TL_SELFTEST_DEBUG"):
            import traceback as _tb110; _tb110.print_exc()
        cases.append((name, False))
```

Không đặt `TL_SELFTEST_DEBUG` thì **không một ký tự** chẩn đoán. Nên mọi ca chết vì hạ tầng
(`PermissionError`, `TimeoutExpired`, `OSError`, `ImportError`) trông **y hệt** một ca thất bại vì
mã sai. `Đ1` mất bốn lượt đo để tìm ra **chỉ vì** `Đ2`.

Bán kính khác nhau, và đó là lý do chủ kho chọn phương án rộng: `Đ1` là **một** ca, `Đ2` là **mọi**
ca trong `tl_selftest` (`1710` ca, đo 15:58Z 19-09-2026).

Cùng họ #568 (`ops/nhanh_don_duoc_test.py` vứt chẩn đoán của con ở lớp phân hạng), nhưng rộng hơn
và ở tệp khác. **Hai packet, KHÔNG gộp** — write set rời nhau.

## `write_set` — HAI đường

```
scripts/tl_selftest.py
RELEASE_MANIFEST.json
```

Đo `ai-dang-giu` lúc **15:58Z 19-09-2026**: cả hai **`NGƯỜI_GIỮ 0`**. Không giao với packet nào
đang mở (#566 giữ `ops/bien_nhan_v2*.py` + `docs/**`; #568 giữ `ops/nhanh_don_duoc_test.py`).

Hai tệp, trong trần `ADR-0044:5` cho class `sensitive` (≤3 tệp, ≤300 dòng thêm).
**Không xin ngoại lệ nào** — và nếu lúc thi công đo ra >300 thì **DỪNG và xin lại**, không tự làm
tròn. Tiền lệ đã trả giá ở #566 lượt này: đo ra 412, dừng, xin, được nới lên 420.

`RELEASE_MANIFEST.json` **bắt buộc** có mặt trong write set: `scripts/tl_selftest.py` **nằm trong**
manifest (`CLAUDE.md` §Quy ước deploy mục 5 nêu đích danh), nên sửa **nội dung** nó làm `sha256`
lệch dù `file_count` **không** đổi. `file_count` đo 15:58Z 19-09-2026 = **180**.

## `ngoai_pham_vi` — CỐ Ý không làm

| thứ | vì sao |
|---|---|
| Bỏ `bash` khỏi `r330`, hay ghim `bash` về Git Bash | `r330` sinh ra để đo **hành vi backtick của bash**; đổi bộ thông dịch là đổi thứ nó đo. Và alias WSL chạy `bash` ĐÚNG — chỉ **dọn dẹp** là hỏng |
| Thêm `retry` cho `rmtree` | Che tín hiệu, và không cần: `ignore_errors` đã đủ vì thư mục tạm do HĐH dọn |
| Đổi `_t110` thành **ném** ra ngoài | Sẽ làm một ca hạ tầng giết cả lượt chạy **1710** ca. Phải **IN**, không phải **NÉM** |
| Chạm bất kỳ ca `rXXX` nào khác trong `tl_selftest` | Ngoài phạm vi; lease siết bằng `PHAM_VI_TREN_TL_SELFTEST` |
| Đổi `file_count` trong manifest | Không tệp nào được thêm/xoá. Giữ **180** |

## `muc_tieu`

| # | mục tiêu | chiếu vào |
|---|---|---|
| **M1** | `_goi` không để dọn dẹp quyết màu: `mkdtemp` + `finally: rmtree(ignore_errors=True)` thay cho context manager. Giá trị trả về đo XONG **trước** khi dọn | `scripts/tl_selftest.py` |
| **M2** | `_t110` **IN** kiểu ngoại lệ và thông điệp khi nuốt, **KHÔNG** điều kiện `TL_SELFTEST_DEBUG`. Biến ấy giữ nguyên nghĩa "in **cả traceback**" | `scripts/tl_selftest.py` |
| **M3** | M2 **không** đổi kết quả: `cases` vẫn nhận `(name, False)`, số ca và thứ tự y hệt. Chỉ **thêm** dòng in | `scripts/tl_selftest.py` |
| **M4** | Dòng in của M2 mang **kiểu** VÀ **thông điệp**; thông điệp nhiều dòng phải tới nơi, hoặc khai rõ đã cắt **bao nhiêu ký tự** | `scripts/tl_selftest.py` |
| **M5** | Ca `rXXX` mới khoá M1 và M2/M4, kèm đối chứng phân biệt được hai chốt | `scripts/tl_selftest.py` |
| **M6** | Tái sinh `RELEASE_MANIFEST.json` bằng `python3 scripts/tl.py release-manifest`; `file_count` giữ **180** | `RELEASE_MANIFEST.json` |

## `nghiem_thu` — mỗi tiêu chí nêu phép đo làm nó ĐỎ

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| **A1** | M1: bơm một `rmtree` **luôn ném** `PermissionError` ⇒ `_goi` vẫn trả đúng `True`/`False` | Quay `_goi` về context manager ⇒ ca ĐỎ |
| **A2** | M1: giá trị trả về được tính **TRƯỚC** khi dọn | Đổi thứ tự (dọn trước, đọc sau) ⇒ ca ĐỎ |
| **A3** | M2: `fn` ném `RuntimeError("MOC-B")` **không** đặt `TL_SELFTEST_DEBUG` ⇒ stdout chứa **cả** `RuntimeError` **và** `MOC-B` | Bọc dòng in lại trong `if os.environ.get(...)` ⇒ ca ĐỎ |
| **A4** | M3: cùng đầu vào ⇒ danh sách `cases` **bằng đúng** bản trước vá (tên, thứ tự, giá trị) | Đổi `False` thành `True`, hoặc bỏ `cases.append` ⇒ ca ĐỎ |
| **A5** | M4: thông điệp có dòng thứ hai mang chuỗi mốc ⇒ dòng in chứa nó, hoặc in nhãn cắt **kèm số ký tự** | Nuốt lặng phần sau dòng đầu ⇒ ca ĐỎ |
| **A6** | `TL_SELFTEST_DEBUG` vẫn in traceback | Bỏ nhánh traceback ⇒ ca ĐỎ |
| **A7** | `python3 scripts/tl.py --selftest` ⇒ `rc=0`, **N/N hai số BẰNG NHAU**. Nền `dc85dd0a` đo **15:58Z 19-09-2026** trong container này: `rc=0`, **`1710/1710`**. Ứng viên = `1710 + số ca mới` | Bất kỳ ca nào đỏ |
| **A8** | `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true` **và** `expected == checked`; `file_count` = **180** | Quên tái sinh manifest ⇒ `sha256` lệch ⇒ ĐỎ |
| **A9** | `golden-test` và `determinism-audit --strict` — chỉ ghi lại golden **nếu** số đếm kiểm kê thật sự đổi, và phải kiểm `git diff -- references/golden/` **trước** khi commit | Ghi golden mà chưa kiểm diff ⇒ vi phạm R6 |
| **A10** | `numstat`: **2** đường, additions **≤ 300** | Vượt ⇒ DỪNG và xin lại |

**A8 có một bẫy phải nói thẳng:** lane PR **KHÔNG** bắt được lệch manifest.
`release-verify strict (lane LAND)` trong `ci.yml` có `if: github.ref == 'refs/heads/master'`, còn
lane WORKER sinh manifest **TẠM** từ chính cây nên nó **hấp thụ** mọi thay đổi nội dung ⇒ **PR
xanh, master ĐỎ**. Nên A8 phải chạy **tại chỗ**, đúng lệnh của lane LAND, **trước** khi merge.

**A2 và A1 phải phân biệt được bằng đầu vào.** Nếu một đột biến giết được cả hai thì chúng là bộ
**tương đương** và ta chỉ đang đo một thứ — bài học đo được ở #566 lượt này (`m76` phải đổi đối
chứng vì đối chứng cũ đỏ theo).

## `hinh_dang_ke_thua`

| hình dạng | số | ghi chú |
|---|---|---|
| `RIG-QUYET-MAU-CUA-PHEP-DO` | **5** | Bốn ca `CLAUDE.md` đã đếm (24-08: worktree ×2, kho-thật-vs-clone, clone+cp+checkout) cộng `Đ1`. **Đã quá** ngưỡng *"lặp ba lần thì hỏi có nên làm thế này không"* ⇒ M1 chữa bằng **KIẾN TRÚC** (không để dọn dẹp nằm trên đường quyết định) chứ không bằng một `try` |
| `NGOAI-LE-BI-NUOT-LANG` | **2** | #568 (`ops/nhanh_don_duoc_test.py`) và `Đ2`. Gặp cái **thứ BA** ⇒ đây là bệnh hệ thống của kho, phải có cổng chung chứ không vá từng tệp |
| `LOI-KHAI-RONG-HON-PHEP-DO` | **3** | Kế thừa #566/#568. Cơ hội tái phát ở đây: khai *"đã chữa `r330`"* trong khi mới chữa **rig** của nó |
| `GIA-THUYET-CHUA-KIEM-VIET-NHU-DA-KIEM` | **1** | Bộ đo bản 2 đã **bác** giả thuyết hiển thị muộn. Đừng viết `Đ1` như thể đã xác nhận trên máy chủ kho — xem `C1` |

## `chua_do_duoc` — ghi thẳng

| # | thứ | trạng thái |
|---|---|---|
| **C1** | Bản vá có làm `r330` xanh trên máy chủ kho không | **KHÔNG ĐO ĐƯỢC từ phiên này** — container không có Windows, không có WSL. `Đ1` là suy luận từ **ba** phép đo khớp nhau (mã · 16/20 handle · 3 đỏ/1 xanh), **không** phải quan sát trực tiếp. Lời khai đúng cho tới khi chủ kho chạy lại: *"nguyên nhân đã xác định, bản vá CHƯA được xác nhận trên nền thật"* |
| **C2** | `gate (windows-latest)` | **KHÔNG DÙNG PHƯƠNG TIỆN** — `manual_ci_budget: 0`. Là **CHỌN** không đo, không phải *"đã đo và xanh"* |
| **C3** | `Đ2` đã làm mất bao nhiêu giờ công trước đây | **KHÔNG ĐO ĐƯỢC.** Biết chắc **một** ca: bốn lượt đo `r330` của đợt #551 |
| **C4** | Có ca `rXXX` nào KHÁC đang đỏ/xanh vì lý do hạ tầng mà chưa ai biết không | **KHÔNG ĐO ĐƯỢC cho tới khi M2 land.** Đó chính là thứ M2 mua — và là lý do phương án rộng được chọn |
