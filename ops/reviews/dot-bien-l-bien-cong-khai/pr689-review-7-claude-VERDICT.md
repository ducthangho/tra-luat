# Review MÃ lượt 7 (chạy lại lần 2) — PR #689 / packet #677

- reviewer: Sonnet 5.5, effort high (TỰ KHAI); nhãn: `advisory_review` (cùng họ Claude với executor)
- reviewed_sha: `3c308b304d9bed46afba2ca698d94d7c31a77a01` (đo `git -C cay-kho rev-parse HEAD`); cha `8e630c0`; A8 `89fc4fa`
- spec `SPEC-r8.md` sha256 đo lại: `4dfbfd69e161d55aa28f2685741cdcf11fcd5171438081e9eb63815c69bb4094` (khớp PROMPT `4dfbfd69…4094`)
- Môi trường: Linux 4 CPU, python3.11, ruff 0.15.8; Windows KHÔNG ĐO ĐƯỢC. Cây tạm: /tmp/claude-0/-home-user-tra-luat/0c469e32-6eae-522a-ad2b-aacdd0027d2d/scratchpad/rv689-l7/w7.E2UW/{va,nen,nen89,suite}. Giàn `do7/` (chay_ca.py: một ca/một tiến trình, phân hạng CHOT/BANG/SAI_LY_DO theo traceback) kế thừa từ hai lượt chết; MỌI số dưới đây do lượt này đo lại. `BAO-CAO-VA.md` không được tin.
- Lượt này bị giới hạn thời gian (container khởi động lại ~20 phút) nên Mục 1 chỉ đo đột biến then chốt.

Nhật ký tăng dần.

## Đợt 0 — nền (đo lượt này)
- A7(2): `git -C cay-kho diff --numstat $(merge-base HEAD origin/master=c16bec6) HEAD -- ops/lease_publish_test.py ops/lease_publish.py` ⇒ `598 15 ops/lease_publish_test.py` ⇒ 598 ≤ 600 (dư 2). A7(1) `--name-only` hai tệp ⇒ chỉ `ops/lease_publish_test.py`. `git diff --check 8e630c0 3c308b3` rc=0.
- A8: `do7/a8.py 89fc4fa 3c308b3` ⇒ `A8 so khoi 18 18 cung ten True lech []` (`_chay_buoc_dang` + t51–t68 byte-exact).
- ruff F (`ruff check --select F --no-cache` trên `ops/lease_publish_test.py`): @8e630c0 ⇒ 9 lỗi, @3c308b3 ⇒ 9 lỗi ⇒ delta = 0 (chi tiết bộ lỗi: xem mục 3).
- "Gọn 17 dòng" — `ast.dump` từng định nghĩa cấp module 8e630c0→3c308b3: 322→322 định nghĩa, 315 giống, 7 khác: t154, _toa_do_that, t195, _lech_m4, t198, t201, t202. Các hàm bị gọn (_ca_doc_than_buoc, _chay_buoc_dang_that, _yaml_that, _lech_tap_i/ii, t199, t200) KHÔNG nằm trong danh sách khác ⇒ AST y hệt ⇒ gọn không đổi hành vi.
- Toàn suite py3.11 chạy nền → `suite-py311.log` (kết quả ghi ở mục 3).

## Mục 1 — F-E / F-F / P4 bằng phép đo (lượt này; đột biến trên bản sao `va@3c308b3`)

Giàn: `python3 -B do7/mut.py <cây va> <out> <đột biến,…> t195_,…,t202_` (8 ca, MỘT tiến trình/ca), `do7/tom.py` tóm tắt. Nền `nen` (không đột biến): 8/8 QUA. Mọi ô đỏ dưới đây đều được giàn phân hạng `CHOT` (`TinHieuChotCa` ném từ `chot()` mà bên gọi là CHÍNH ca ghi trong bảng); không ô nào là `SAI_LY_DO`/`CHOT_TU_*`. Đầu ra gốc: `m1a.out m1b.out m1c.out`.

### 1a. F-E (nhật ký `gh` giả) — đột biến ở đồ giả/helper/sản phẩm

| đột biến | ca đỏ (CHOT đúng ca) |
|---|---|
| `L` (gỡ dòng kiểm `lease_id` của sản phẩm, spec §2) | t195 t196 t197 |
| E1a helper `splitlines()[1:]` · E1b `[2:]` (analog `dong[2:]` của advisory) | t198 |
| E1a+L · E1b+L | t196 t197 t198 (t195 xanh — giới hạn đã khai của executor) |
| E2 đồ giả bỏ ghi GET loại số hiệu | t198 t201 |
| E2+L | t195 t196 t197 t198 t201 |
| E3 đồ giả bỏ ghi đường LỖI (#57) | t201 (một chốt duy nhất) |
| E3+L | t195 t196 t197 t201 |
| E4 sản phẩm gọi `GOI_GH("user")` · E4b `GOI_GH("/repos/o/r/issues/55")` | t195 t198 |
| E4+L | t195 t196 t197 t198 |

Kết luận F-E (E1–E4, advisory `dong[2:]`, mutant `L`): **ĐÃ ĐÓNG** ở tầng nhật ký/đồ giả/helper — mỗi đường có ca đích đỏ bằng `chot()` của chính nó.

### 1b. F-E — đường vào THỨ BA ở tầng HÀM QUYẾT ĐỊNH `_lech_m4` (ops/lease_publish_test.py:10719–10727)

Mỗi dòng là MỘT đột biến trên biểu thức so dãy `kq["goi"] != [...]` (dòng 10725):

| đột biến | ca đỏ |
|---|---|
| W3 `sorted(goi) != sorted(mong)` | t202 |
| W4 `set(goi) != {3 phần tử}` | t202 |
| W5 `len(goi) != 4` | t202 |
| **W1 `goi[:4] != mong`** (bỏ qua lời gọi THỪA phía sau) | **8/8 QUA — SỐNG SÓT** |
| **W2 `goi[-4:] != mong`** (bỏ qua lời gọi THỪA phía trước) | **8/8 QUA — SỐNG SÓT** |

Nguyên nhân (đọc `t202`, ops/lease_publish_test.py:10886+; danh sách hàng `M4`): có hàng "nhật ký rỗng / chỉ POST / cắt dòng đầu / đảo thứ tự / thiếu GET loại số hiệu" nhưng **KHÔNG có hàng "thừa lời gọi"** (dãy dài hơn 4). Docstring `t202` khai "nhật ký cắt/thiếu/đảo"; docstring `t198`/`_lech_m4` khai "ĐỦ dãy … đúng thứ tự" và L-lượt-7 khai đóng "rơi/thừa". Hàm THẬT (`!=` nguyên dãy) đỏ khi thừa (đo ở mục 2, B1) nên đây là lỗ của TỰ KIỂM `t202`, không của mã sản phẩm. → **L1** cuối tệp.

### 1c. F-F (tiền đề `_toa_do_that` lỏng hơn sản phẩm)

| đột biến | đơn lẻ | kèm `L` |
|---|---|---|
| F1 hạn `…z` (ô hết hạn, fixture) | t197 t202 | t195 t196 t197 t202 |
| F3 `schema_version: true` | t195 t196 t197 t198 t202 | như đơn lẻ |
| F4 `schema_version: 1.0` | t195 t196 t197 t198 t202 | như đơn lẻ |
| **gỡ FF-hạn** (`FFhan`: trả về phân loại hạn cũ `strptime` trực tiếp, bỏ `_doc_han`) | **t202** | `+F1+L`: t195 t196 t202 |
| `FFhan_luon_OK` (tiền đề hạn luôn OK) | t195 t196 t202 | — |
| `FFsv_eq` (tiền đề `schema_version=1` về `==`) | **8/8 QUA** (xem ghi chú) | — |
| `FFsv_eq` + gỡ tiền đề "trường khác = lease_mau() (repr)" (`FFsv_eq+FP`) | **t202** ("F-F: tiền đề phân loại {'schema_version': True} lệch `kiem()` … (rc=10, hỏng=())") | — |
| `FFsv_eq` + "trường khác" về `==` (`FFsv_eq+FPeq`) | **t202** | — |
| gỡ riêng "trường khác" (`FP_alone`) · "trường khác" về `==` (`FP_eq_alone`) | 8/8 QUA | — |

Ghi chú F-F: `schema_version` được che bởi HAI tiền đề độc lập (`schema_version=1` bằng `repr` VÀ "trường khác … repr"); gỡ MỘT trong hai vẫn xanh (đo: `FFsv_eq`, `FP_alone` đều 8/8 QUA), gỡ CẢ HAI thì `t202` đỏ bằng `chot()` của chính nó. Đây là chiều sâu có chủ đích, không phải lỗ: hai mutant đơn sống sót là TƯƠNG ĐƯƠNG về hành vi trên tập biến thể một-trường.

Vi phân tiền đề ↔ sản phẩm (`do7/fuzz_ff.py`; 252 biến thể MỘT trường cho mọi khoá `lease_mau()` trừ `lease_id`: True/False/0/1/1.0/""/" "/None/[]/{}/chuỗi ép/hoa-thường/khoảng trắng/±1…; so `bool(tiền đề hỏng)` với `kiem()` + `_tien_kiem_mien_dang` thật; đầu ra `fz_*.txt`):

| cây | tiền đề OK mà sản phẩm TỪ CHỐI (lỏng hơn) | ERR_td (ném vô can) | tiền đề chặt hơn sản phẩm (đỏ an toàn) |
|---|---|---|---|
| `nen` @8e630c0 | **4** | **18** | 151 |
| `va` @3c308b3 | **0** | **0** | 154 |
| `va` + `FP_alone` | 0 | 0 | 15 |
| `va` + `FP_eq_alone` | 0 | 0 | 151 |

⇒ F-F (a) hạn, (b) `==` ép số: **ĐÃ ĐÓNG** ở mức một trường; chốt "gỡ FF-hạn" chết ở `t202` bằng `chot()` của nó. KHÔNG ĐO ĐƯỢC: vi phân hai trường (tổ hợp) và phần `kiem_github`/bước ngoài `kiem()` + `_tien_kiem_mien_dang` (loại số hiệu, comment) — phần ấy nằm ở tọa độ chứ không ở tiền đề.

Đột biến B1/B3/P3a–P3f (đồ giả/helper nói sai kiểu khác — đường vào THỨ BA của F-E, `m1d.out`): P3a đồ giả `open("w")`, P3b method cứng GET, P3c cắt tiền tố `repos/o/r/` ⇒ t198 t201 (hai chốt); P3d dedup, P3d' sorted, P3e cắt `[:3]`, P3f bỏ POST ⇒ t198. Tất cả `CHOT` đúng ca.

## Mục 1d — P4 lượt 6 L2 (`doc_pid` nhận `"0"`): `t154` (ops/lease_publish_test.py:6482–6508), đột biến trên `va@3c308b3`, chạy trong `setsid -w` (không bao giờ trao giá trị tới `os.kill`)

Nền `t154` QUA. Ô đỏ đều là `BANG` của chính `t154` (`doc_pid trả đích giết nguy hiểm <n>`). Đầu ra: `m1e.out`.

| đột biến | kết quả |
|---|---|
| D1 regex `[1-9][0-9]*` về `[0-9]+` (gỡ `[1-9]`) | DO BANG `… nguy hiểm 0` |
| D2 bỏ loại PID mình | DO BANG |
| D3 bỏ loại PID cha (gỡ loại trừ PID cha) | DO BANG |
| D4 bỏ cả hai loại | DO BANG |
| D4b D1+D4 (luật `8e630c0`) | DO BANG `… nguy hiểm 0` |
| D5 gỡ vòng tự kiểm | QUA (tự kiểm chính là khoá) |
| D6 D1 + gỡ mẫu `"0"` khỏi tự kiểm · D7 D2 + gỡ mẫu PID mình · D8 D3 + gỡ mẫu PID cha | đều QUA — mỗi mẫu tự kiểm khoá ĐÚNG đường của nó |

⇒ `"0"`, PID mình, PID cha: **ĐÃ ĐÓNG** (ca đích đỏ bằng `bang()` của chính `t154`; ba chốt độc lập, mỗi chốt một mẫu).

Đường THỨ BA tự tìm: mở rộng vòng tự kiểm của bản sao bằng một đích giết nguy hiểm khác, xem `doc_pid` có nhận không (DO = `doc_pid` TRẢ về đích ấy = CHƯA đóng). `SETSID=1` bố cục phẳng (`setsid -w python`); `SETSID=3` bố cục LỒNG (`bash→python→python`, giống lượt con `t125` và bước CI có tầng bọc). Đầu ra `m1f_S1.out`, `m1f_S3.out`:

| đích | phẳng | lồng |
|---|---|---|
| `"1"` (init) | `doc_pid` nhận | nhận |
| `os.getpgrp()` (trưởng nhóm) | từ chối (trùng PID cha) | **nhận** |
| `os.getsid(0)` (phiên) | từ chối | **nhận** |
| ông nội (`/proc/<ppid>/stat`) | **nhận** | **nhận** |

⇒ P4 lượt 6 L2 chỉ **MỘT PHẦN**: đóng ba đích đã liệt kê; họ "đích giết là tổ tiên/trưởng nhóm/phiên/init" còn hở. Mức **P4** (không phải P3): tệp PID do chính cháu của `t154` ghi bằng `os.getpid()` của nó; không nhà ghi nào ghi tổ tiên — lý thuyết, cùng mức lượt 6; PID 1 vô hại trong namespace container. Đúng hình dạng CLAUDE.md "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA". → **L2**.

## Mục 2 — chốt mới có QUÁ CHẶT / giòn không?

**2a. `_lech_m4` đòi đúng dãy và thứ tự — đỏ oan khi sản phẩm đổi VÔ HẠI?** Đột biến SẢN PHẨM vô hại (`do7/dotbien.py` B1, B3; `m1d.out`; 8 ca mỗi ô):
- B1 — `_doc_gh` đọc lặp `comments` thêm MỘT lần (không đổi kết quả): **chỉ `t198` đỏ** (CHOT; thông điệp in nguyên nhật ký 6 lời gọi); t195 t196 t197 t199 t200 t201 t202 xanh.
- B3 — thêm `?per_page=100` vào endpoint `comments`: **chỉ `t198` đỏ** (CHOT). (Cùng đỏ ở `8e630c0` vì `("GET", ep) in goi` so chuỗi endpoint đúng — không phải giá MỚI của lượt 7.)
- Phạm vi nổ: MỘT ca, fail-closed, thông điệp in nguyên nhật ký; sửa = cập nhật HAI literal (`_lech_m4` dòng 10725 và `GOI_M4` ở `t202`). Chỉ áp đường HỢP LỆ M4 (dãy dò → loại số hiệu → cửa cuối → POST) — bỏ lần đọc cửa cuối là hồi quy an ninh thật (TOCTOU) nên ở đây khoá lịch gọi có giá trị. Các đường TỪ CHỐI (t195–t197) không khoá dãy; chúng chỉ đòi "0 POST, không bỏ qua" nên #678 (`LEASE-ID-EP-KIEU-YAML`, đổi đường từ chối) không chạm M4 `wp-ok-1`.
- Đánh giá: **CHẤP NHẬN ĐƯỢC (P4)**. Kèm một việc hồ sơ: docstring `t198` và `t195` (e) còn nguyên lời Q13 "không khoá lịch gọi" mà không dẫn chiếu ngoại lệ có chủ đích của M4 (đã khai ở docstring `_lech_m4`/`t202`).

**2b. `_toa_do_that` nạp sản phẩm MỘT lần mỗi tiến trình (`_toa_do_that.lp`, dòng 10592) — rò trạng thái giữa các ca?** Đo: (i) `lp` chỉ được dùng để gọi `lp._doc_han` (hàm thuần: phân tích chuỗi → `(rc, datetime)`); không mock nào chạm `lp` (các `mock.patch.object(…, "SCRIPT", …)` ở `t200` đổi `SCRIPT` của mô-đun test, còn `t200` KHÔNG truyền `ghi_toa_do` nên không gọi `_toa_do_that`). (ii) Phép đo thứ tự: `do7/chay_ca.py` MỘT tiến trình, ba thứ tự khác nhau — `t202 t197 t196 t195 t198 t200 t201`, đảo hẳn `t200 t201 t198 t197 t196 t195 t202`, và lặp `t197 t197 t202 t202` ⇒ TẤT CẢ QUA (không ca nào đổi kết quả). (iii) `t125` chạy toàn suite HAI lượt con `[A]`,`[B]` (mỗi lượt là một tiến trình riêng) ⇒ mỗi lượt `195/195`. Kết luận: **không rò**. Điều kiện để rò sẽ là `_doc_han` đọc trạng thái toàn cục của mô-đun sản phẩm hoặc một ca viết vào mô-đun `lp` — hiện cả hai đều không. Mức cao nhất: P4 (khoá ngầm: nếu ai cho `_doc_han` đọc giờ/biến môi trường thì ca sẽ thấy trạng thái cũ) — không cần sửa.

**2c. `doc_pid` loại PID cha — đỏ oan trong lượt con `t125`?** Đo: `t154` QUA ở cả ba lượt trong toàn suite: `[A]` (5,600 s), `[B]` (5,599 s) và lượt chính (5,603 s) — `suite-py311.log` dòng 1036/1038/1344. Lý do cấu trúc: PID trong tệp do CHÁU ghi (`os.getpid()` của cháu), khác `os.getpid()`/`os.getppid()` của tiến trình chạy `t154`, kể cả khi `t154` chạy trong lượt con `t125` (cha của nó là lượt `t125`, không phải cháu). Đỏ oan chỉ xảy ra khi PID cháu trùng PID hoặc PID cha của tiến trình test (tái dùng PID) — không đo được (không ép được) ở đây; khi đó `doc_pid` chờ hết hạn rồi ĐỎ có thông điệp (`bang`), không treo/không giết nhầm.

## Mục 3 — hồi quy

- **Toàn suite py3.11** (đã nêu ở Đợt 0; `suite-py311.log`): `env -u GITHUB_ACTOR python3 -B ops/lease_publish_test.py` trong clone sạch `suite@3c308b3` ⇒ dòng cuối `lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0`, `rc=0`; hai lượt con `t125`: `[A] 195/195 … bỏ qua=0`, `[B] 195/195 … bỏ qua=0`; 0 dòng bắt đầu bằng `  ĐỎ`/`  BỎ QUA`/`!!! do`. (Chạy cùng lúc với đột biến ⇒ dưới tải.)
- **Toàn suite py3.12** (`suite-py312.log`, clone `suite2@3c308b3`): `195/195 đạt; đã chạy=195, bỏ qua=0`, `[A]`/`[B]` cùng `195/195`, `rc=0`, 0 dòng ĐỎ/BỎ QUA/`!!! do`.
- **Mẫu đột biến lượt 4–6 vẫn chết** (`m3a.out`, `m3b.out`, `m1a.out`; ca đích đỏ bằng `chot()`/`bang()` của nó):

| đột biến | ca đỏ |
|---|---|
| `L` gốc (gỡ kiểm `lease_id`) | t195 t196 t197 |
| C1 (consumer `t196`/`t197` viết đè quan sát: có GET comments ⇒ rc=1) | t202 |
| C1+L | t195 t202 (t196/t197 bị C1 che, t202 bắt đường nối helper→consumer) |
| C2 (rebind `_chay_buoc_dang_that` bằng wraps ghi I/O ngoài) | t199 |
| A3 (đồ giả: PATH không đặt `gh` giả) | t198 |
| A4 (đồ giả: POST không lưu) | t198 t201 |
| `M_doc_pid_cu` (`doc_pid` về mã cũ: `exists()` + `int(read_text())`) | t154 BANG `doc_pid trả đích giết nguy hiểm 0` |
| `R_rac_E2` (cháu ghi rác `x` vào tệp PID) | t154 BANG `doc_pid` "fixture hỏng … đọc cuối: 'x'" |
| `R_tre_E2` (cháu trễ 1 s giữa `open('w')` và ghi; giả lập cửa sổ RỖNG) | t154 QUA (đúng thiết kế: `doc_pid` chờ tới PID hợp lệ) |
| `R_tre_E1` (E1 trễ ở `launcher_test.py`) | t154 (ops) QUA — mã E1 thuộc `launcher_test`, không thuộc `t154` của `ops/` |
| `K_t200_ghi_toa_do` (`ghi_toa_do=[]` trong `t200` dưới `mock.patch SCRIPT`) | 8/8 QUA (không đường sản phẩm nào đi tới đó; xem 2b) |

- **A7(2) ≤ 600:** `598 15` (đo ở Đợt 0) ⇒ dư 2. **A8:** `A8 so khoi 18 18 cung ten True lech []`. **ruff F delta = 0:** `ops/lease_publish_test.py` @8e630c0 ⇒ 9 (F401 shutil×5, io, contextlib, F541×2), @3c308b3 ⇒ 9 cùng bộ; `ops/lease_publish.py` ⇒ `All checks passed!`. **`git diff --check 8e630c0 3c308b3`** rc=0. **"Gọn 17 dòng" không đổi hành vi:** xem Đợt 0 (`ast.dump`: chỉ 7 định nghĩa khác, đều là nơi đổi theo lượt vá; các hàm bị gọn giống hệt).
- KHÔNG ĐO ĐƯỢC: Windows (không có nền); "chỉ docstring" của t195/t198/t201 (không bóc `ast.dump` riêng docstring, nhưng `diff-luot7.patch` cho thấy t195/t198 đổi docstring) — không ảnh hưởng kết luận (AST khác ⇒ dù sao đã kiểm bằng mutant).

---

## L1 — Hàm quyết định `_lech_m4` bị NỚI về phía "thừa lời gọi" mà `t202` không hàng tự kiểm nào bắt

- Mức: **P3** · MỚI trên `3c308b3` (nằm ở chỗ bản vá vừa thêm; lượt 6 không có dãy ở `_lech_m4`). Cùng hình dạng CLAUDE.md "VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA": F-E chỉ đóng các đường reviewer liệt kê (rơi/thiếu/đảo), nửa "thừa" bị bỏ sót.
- Biểu hiện: `ops/lease_publish_test.py:10725` (`if kq["goi"] != [("GET", ep), …]`) và `t202` (`ops/lease_publish_test.py:10886+`, danh sách hàng `M4 …` — có rỗng/chỉ POST/cắt dòng đầu/đảo/thiếu GET loại số hiệu, KHÔNG có hàng "dãy dài hơn 4"). Lời khai sai phạm vi đo: docstring `t198` (ops/lease_publish_test.py:10736) "nhật ký rơi/**thừa**/đảo lời gọi ⇒ ĐỎ".
- Phép đo tái lập (mục 1b): đột biến `goi[:4] != mong` (W1) và `goi[-4:] != mong` (W2) ⇒ `8/8 QUA` (không ca nào đỏ); trong khi W3/W4/W5 ⇒ `t202` đỏ. Hàm THẬT đỏ khi thừa: B1 (`_doc_gh` đọc lặp thêm một lần) ⇒ `t198` đỏ bằng `chot()` — nên đây là lỗ của TỰ KIỂM, không của mã sản phẩm.
- **Hint patch** (`HINT.patch`, áp được lên `3c308b3`; 1 dòng trong `t202`): thêm HAI hàng vào bảng `M4`, mỗi chiều một hàng:
  `("M4 thừa lời gọi phía sau", True, kq(0, [dau], goi=GOI_M4 + [("GET", ep)])), ("M4 thừa lời gọi phía trước", True, kq(0, [dau], goi=[("GET", ep)] + GOI_M4)),`
  Đã áp vào clone `hint` (đo): `git apply --check` rc=0; toàn suite trên cây vá `195/195 đạt; đã chạy=195, bỏ qua=0` (`[A]`,`[B]` cùng `195/195`), `rc=0`, 0 dòng ĐỎ/BỎ QUA.
  Ca khoá & đột biến (đo trên cây vá, `m2a.out`): W1 ⇒ **t202 ĐỎ (CHOT)**; W2 ⇒ **t202 ĐỎ (CHOT)**; W3/W5 vẫn ⇒ t202 ĐỎ; mỗi hàng độc lập: `W1 + bỏ hàng "sau"` ⇒ QUA, `W1 + bỏ hàng "trước"` ⇒ ĐỎ; `W2 + bỏ hàng "trước"` ⇒ QUA, `W2 + bỏ hàng "sau"` ⇒ ĐỎ (hai hàng là HAI chốt, không tương đương).
  Trần: hint cộng 2 dòng `added` ở `t202`+`t154` (xem L2); đo `git diff --numstat $(merge-base) HEAD` trên cây vá ⇒ `600 15` ⇒ **600 ≤ 600**, không có dư.
- Sửa mã hay hồ sơ: **sửa mã** (chỉ tệp test).

## L2 — `doc_pid` (t154): đích giết nguy hiểm NGOÀI `0`/PID mình/PID cha vẫn lọt (đường thứ ba của P4 lượt 6)

- Mức: **P4** · MANG (lượt 6 L2) — `"0"`/PID mình/PID cha ĐÃ ĐÓNG (mục 1d); họ tổ tiên/trưởng nhóm/phiên/init MỘT PHẦN.
- Biểu hiện: `ops/lease_publish_test.py:6491` (`int(nd) not in (os.getpid(), os.getppid())`) và vòng tự kiểm dòng ~6507 (`for x in ("0", str(os.getpid()), str(os.getppid()))`).
- Phép đo tái lập (mục 1d): mở rộng vòng tự kiểm bằng `"1"` ⇒ `t154` BANG `doc_pid trả đích giết nguy hiểm 1` ở cả hai bố cục; `os.getpgrp()`/`os.getsid(0)` ⇒ bố cục LỒNG (`SETSID=3`) BANG `… nguy hiểm <pid>`, phẳng QUA; ông nội (`/proc/<ppid>/stat`) ⇒ cả hai BANG. Mức P4 vì tệp PID chỉ do cháu của chính `t154` ghi `os.getpid()` (tổ tiên: lý thuyết, cùng mức lượt 6).
- **Hint patch** (phần `t154` của `HINT.patch`): `nguy = {1, os.getpid(), os.getppid(), *(g(0) for g in (getattr(os, "getpgid", None), getattr(os, "getsid", None)) if g)}` thay tuple PID mình/cha trong `doc_pid`, và vòng tự kiểm thêm `"1"` + pgid + sid. `getattr` bảo vệ nền thiếu API (Windows). Đo trên cây vá (`m2b_S1.out` phẳng, `m2b_S3.out` lồng): `nen` QUA cả hai; `H_bo_1` (bỏ `1` khỏi `nguy`) ⇒ **t154 ĐỎ (BANG)** cả hai; `H_regex0` ⇒ ĐỎ cả hai; `H_bo_ppid` ⇒ ĐỎ cả hai; `H_bo_pid` ⇒ ĐỎ ở lồng, QUA ở phẳng (phẳng: pgid của tiến trình = PID mình nên bị chính pgid che); `H_bo_pgid_sid` (bỏ cả getpgid+getsid) ⇒ ĐỎ ở lồng, QUA ở phẳng; `H_bo_getsid`/`H_bo_getpgid` riêng lẻ ⇒ QUA (hai API trùng giá trị trong cả hai bố cục; tương đương). Toàn suite trên cây vá `195/195`, `t154` không đỏ oan trong `[A]`/`[B]` (nested).
- Sửa mã hay hồ sơ: sửa mã nhỏ (chung `HINT.patch`) HOẶC ghi hồ sơ "P4 chấp nhận: nhà ghi PID duy nhất là cháu của `t154`". Không chặn PASS nếu L1 đóng.

## L3 — Chốt chiều sâu "trường khác = lease_mau() (repr)" (`_toa_do_that`)

- Mức: **P4** (quan sát, không cần sửa) · MỚI. Gỡ riêng tiền đề ấy, hay đổi `repr`→`==`, đều ⇒ 8/8 QUA (mục 1c); chỉ gỡ CẢ `schema_version=1` (repr) lẫn nó mới làm `t202` đỏ. Vi phân 252 biến thể một-trường: gỡ tiền đề ⇒ tiền đề chặt hơn sản phẩm giảm 154→15 nhưng KHÔNG thêm ca "tiền đề OK mà sản phẩm từ chối" (0). Tức nó chỉ chặt hơn sản phẩm (đỏ an toàn) và chỉ có răng khi fixture trôi; không phải lớp lỗi. Hồ sơ: docstring `_toa_do_that` đã nói đúng "cộng mọi trường ngoài `lease_id`/hạn phải bằng `lease_mau()`".

## Bảng trạng thái F-E / F-F / P4 và finding cũ

| finding | trạng thái trên `3c308b3` | bằng chứng (lượt này) |
|---|---|---|
| F-E (nhật ký `gh` giả: E1–E4, advisory `dong[1:]`/`dong[2:]`, P3a–f) | **ĐÃ ĐÓNG** ở tầng nhật ký/đồ giả/helper; **MỘT PHẦN** ở hàm quyết định (nửa "thừa" — L1) | mục 1a/1b: mọi ô đỏ CHOT; W1/W2 sống sót |
| F-F (a) hạn `…z`/số không đệm | **ĐÃ ĐÓNG** | `_doc_han` của sản phẩm; `FFhan`/`FFhan_luon_OK` ⇒ t202 CHOT; fuzz 0 lỏng (nền @8e630c0: 4 lỏng + 18 ném) |
| F-F (b) `==` ép số (`True`/`1.0`) | **ĐÃ ĐÓNG** | F3/F4 ⇒ t195–t198,t202 CHOT; `FFsv_eq`+gỡ chốt kép ⇒ t202 CHOT |
| P4 lượt 6 `doc_pid` nhận `"0"`/PID mình/PID cha | **ĐÃ ĐÓNG** | D1–D4b ⇒ t154 BANG; D6–D8 ⇒ mỗi mẫu tự kiểm một chốt |
| P4 họ tổ tiên/pgid/sid/init | **MỘT PHẦN** (mới, cùng lớp) | mục 1d `X_probe_*` — L2 |
| Toàn suite / A7(2) / A8 / ruff delta / `diff --check` / gọn 17 dòng | **ĐẠT** (py3.11, py3.12) | Đợt 0, mục 3 |
| Lượt 4–6 (L gốc, C1+L, rebind wraps C2, chèn trễ `t154`) | **vẫn chết/đúng thiết kế** | mục 3 |

## Bảng lớp | mức | mới/mang | sửa mã hay hồ sơ

| lớp | mức | mới/mang | sửa mã hay hồ sơ |
|---|---|---|---|
| L1 — `_lech_m4`/`t202` thiếu hàng "thừa lời gọi" (W1/W2 sống sót) | **P3** | mới (đường thứ ba của F-E) | sửa mã: `HINT.patch` hàng `t202` (+1 dòng); trần 600 đúng 600 |
| L2 — `doc_pid` họ init/tổ tiên/pgid/sid | P4 | mang (P4 lượt 6, một phần) | sửa mã nhỏ trong `HINT.patch` hoặc hồ sơ |
| L3 — chốt chiều sâu "trường khác" chỉ có răng khi gỡ kép | P4 | mới | hồ sơ (không cần sửa) |
| Độ giòn B1/B3 (chỉ `t198` đỏ; 2 literal) | P4 | mới, đã khai | hồ sơ: dẫn chiếu ngoại lệ Q13 ở docstring `t198` |

Giới hạn đo: Windows KHÔNG ĐO ĐƯỢC; vi phân hai-trường KHÔNG ĐO ĐƯỢC; mục 1 chỉ đo đột biến then chốt vì giới hạn thời gian (lượt hai lượt trước chết do khởi động lại) — các mutant khác (F5–F8, fixture trôi) chỉ có ở lượt nháp trước, KHÔNG được tính vào số của lượt này.

VERDICT: CHANGES_REQUIRED
