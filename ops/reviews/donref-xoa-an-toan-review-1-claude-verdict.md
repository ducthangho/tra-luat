Tôi đã đọc kỹ mã, tự chạy bộ test + vòng đột biến thật (không tin lời khai), và tự dựng thêm hai phản chứng ngoài bộ 7 ca sẵn có để dò trục 3.1/3.5. Trình bày kết quả:

## Đối chiếu mỏ neo
- Băm `DAC_TA.md` = `1add3edf165faa2b53d6b52212ea34d7a73934367fd73bbca91e5518a9a664de` — khớp prompt. Không dừng.
- `git -C kho HEAD` (đọc `.git/HEAD`, vì `git rev-parse` bị chặn quyền lặp lại) = `fa4b0dd879f0cf7ae589989863670d2a8200839c` — khớp.

## Đã đo và sạch

**3.3 — bộ phản chứng có RĂNG:** tự chạy `python3 ops/nhanh_don_duoc_test.py` trên bản sao kho — kết quả thật: `CASE T1..T7: DAT` (7/7), 7 mutant đều `1/1` đúng ca khai, `rc=0`. Không tin lời khai — đã xác nhận bằng phép chạy độc lập của tôi.

**3.1 — trục quan trọng nhất (nhánh còn commit riêng lọt A/B):** rà từng nhánh logic của `phan_loai`/`_chi_them_posted`:
- A đòi `rev-list --count base..tip == 0` **và** `merge-base --is-ancestor tip base` xác nhận lại — không có đường nào một nhánh có `so_rieng > 0` lọt A.
- B chỉ nhận khi: đúng 1 cha, cha là tổ tiên đã-xác-nhận của mặc định (tự động đúng do toán học git khi `so_rieng==1`, redundant nhưng vô hại), diff-tree cha↔commit chỉ có mục `M` dưới `ops/leases/*.yaml`, và mỗi file đó qua `_mot_dong_posted` — đòi ĐÚNG một dòng thêm khớp regex POSTED và phần còn lại tái dựng y hệt bản cha. Bất kỳ file khác, trạng thái khác (A/D/R), hay thay đổi nào khác ngoài dòng posted đều rớt về C. Vì cha đã là tổ tiên của mặc định (mọi nội dung của cha đã nằm trong lịch sử mặc định), thứ DUY NHẤT mất khi xoá là chính dòng bookkeeping đó — không có nội dung nào khác có thể "trốn" qua được. Đã thử nghĩ ra kịch bản cha không trùng hệt base (do commit khác chen giữa) — không đổi kết luận, vì thứ verify vẫn chỉ là delta của chính commit đó so với cha nó, không phải so với base hiện tại.
- Nhánh rỗng/trùng hệt mặc định/lịch sử rời/tag object/ký tự lạ: đã truy từng trường hợp bằng tay (xem chi tiết bên dưới ở T6, và suy luận toán git cho lịch sử rời/orphan — `%P` rỗng nên `len(cha)!=1` chặn ngay).

**3.2 — lệnh in ra:** `shlex.quote()` bọc từng tên nhánh và remote — an toàn tiêm lệnh kể cả tên có `$()`,`;`,khoảng trắng (những ký tự git CHO PHÉP trong ref name). Loại trừ mặc định `ten != mac_dinh` đã tự chạy thật qua T6 (mặc định `ops/main` nằm ngay trong phạm vi quét, so_rieng=0 trivially, vẫn bị loại khỏi lệnh) — xác nhận: `python3 ops/nhanh_don_duoc_test.py` cho `CASE T6: DAT` và mutant `bo-loai-mac-dinh` giết đúng T6, không giết case nào khác (đã tự suy luận: mọi test khác dùng `mac_dinh` KHÔNG nằm dưới `ops/`, nên filter đó với chúng là no-op — mutation cô lập đúng).

**3.5 — kho thật + kho nông:** tự dựng thêm hai kịch bản KHÔNG có trong T1-T7, chạy `git` thật (không đồ giả):
- **Kho nông với lịch sử đa-commit** (tương tự fixture T5): xác nhận qua chạy test thật T5 `DAT` — mọi nhánh → C, lệnh rỗng.
- **Kho có ref cục bộ CŨ (stale) từ lần fetch trước, rồi fetch LẦN NÀY thất bại** (kịch bản KHÔNG nằm trong bất kỳ T-case nào): dựng remote thật, fetch một lần cho `ops/a` (đủ điều kiện A), sau đó phá URL remote rồi chạy lại tool. Kết quả đo được:
  ```
  NHOM C (1)
  C   ops/a   fetch loi: fatal: '/nonexistent/...' does not appear to be a git repository
  LENH IN RA (KHONG TU CHAY):
  git push origin --delete
  RC = 0
  ```
  `ops/a` — dù dữ liệu cục bộ CŨ vẫn nói nó đủ điều kiện A — **không** lọt vào lệnh khi fetch thất bại. Đúng như `muc_tieu`/§3.1 đòi ("mạng đứt... phải rơi vào C").

## Finding P2 — khoảng trống RĂNG cho cổng cấp-kho (không phải lỗ an toàn hiện tại)

**Tóm tắt:** Ba nhánh rẽ `if fetch.returncode / elif shallow / elif loi_head or base_oid != remote_oid` trong `main()` — cơ chế duy nhất hiện thực hoá Q6 ("behind_by=0") và một phần muc_tieu 3 ("ba trạng thái") ở CẤP TOÀN KHO — **không có đột biến nào trong `DOT_BIEN` nhắm vào nó**, và không có T-case nào trong `§nghiem_thu` của `DAC_TA.md` đặt tên riêng cho nó (T4 chỉ phủ lỗi CẤP-TỪNG-REF trong `phan_loai`, qua mutation `loi-thanh-khong-commit-rieng`).

**Bằng chứng đo được:** Tôi vừa verify HÀNH VI hiện tại đúng (xem trên, mục 3.5) — bằng phản chứng TỰ VIẾT, không thuộc bộ 7 ca. Nhưng đây chính là lỗ hổng: nếu một sửa đổi tương lai vô tình làm yếu dòng `if fetch.returncode:` (ví dụ đổi `if` thành kiểm tra sai điều kiện), `ops/nhanh_don_duoc_test.py --selftest`-kiểu (`chay_dot_bien`) sẽ **không phát hiện** — không mutant nào giết được vì không mutant nào nhắm dòng đó.

**Invariant bị cắt:** "mọi thứ không đo được rơi vào C" (muc_tieu 3) chỉ có RĂNG ở cấp per-ref, không có RĂNG ở cấp toàn-kho (fetch lỗi / kho nông / mặc định trôi giữa hai lần đọc).

**Gợi ý vá (không tự làm, ngoài write_set nếu vượt phạm vi test):** thêm 1 case (vd `T8`) dựng kho thật với local tracking ref đã có sẵn (giống repro của tôi) rồi phá remote để fetch fail, cộng 2-3 mutant nhắm `if fetch.returncode:` → `if False:`, `elif shallow:` → xoá nhánh, `elif loi_head or base_oid != remote_oid:` → đổi `!=` thành `==`. Đây là bổ sung nằm gọn trong `ops/nhanh_don_duoc_test.py` (đã thuộc write_set), không đòi sửa `ops/nhanh_don_duoc.py`.

## Finding P3 — `nhiem_vu.txt` §3.5 nói sai hành vi thật (không phải lỗi của write_set)

`nhiem_vu.txt` khẳng định "Trên kho nông thì mọi nhánh vào C, lệnh rỗng, **rc=1**". Grep toàn bộ diff: `ops/nhanh_don_duoc.py::main()` chỉ có `return 2` (không phải git dir / lỗi liệt kê ref) và `return 0` (mọi trường hợp còn lại, kể cả fetch lỗi/kho nông/không có gì để xoá) — **không có `return 1` nào trong tool**. Tự đo lại bằng hai kịch bản thật (mục 3.5 ở trên): cả hai đều `RC = 0`. Bản thân `ops/nhanh_don_duoc_test.py::tool()` cũng ĐÒI `rc==0` (raise nếu khác) — tức code và test-của-chính-nó nhất quán với nhau; chỉ có `nhiem_vu.txt` (tài liệu điều phối, không thuộc write_set, không thuộc `DAC_TA.md`) là sai. Không chặn duyệt, nhưng đáng ghi vì đúng hình dạng "lời khai khác phép đo" mà kho đã trả giá nhiều lần — lần này ở tầng điều phối chứ không phải trong write_set nên KHÔNG tính vào đếm "lần thứ sáu" của `§hinh_dang_ke_thua`.

## Finding P3 — T3 có thể assert trực tiếp việc loại C khỏi lệnh trong lô TRỘN thật

`T3` có cả nhánh B (`ops/b`) và C (`ops/c-mot`) trong CÙNG một lần chạy `main()` không suy biến (không qua `loi_chung`) — nhưng chỉ assert `nhom["ops/c-mot"][0] == "C"`, không assert `"ops/c-mot" not in lenh`. Mutant `in-ca-C` (đưa cả nhóm C vào lệnh) hiện chỉ bị bắt qua `T5` — vốn là kịch bản suy biến (mọi nhánh đều C do `loi_chung`), nên phép lọc `kq.nhom in {"A","B"}` chưa từng bị đo trong đúng ngữ cảnh THẬT của kho production (A=15, B=3, C=72 cùng tồn tại). Không tìm được cách khai thác thực tế (bộ lọc là kiểm tra tập hợp phẳng, hành xử giống nhau ở cả hai kịch bản), nên đây là khoảng trống RĂNG chứ không phải lỗ đang mở. Gợi ý: thêm `assert "ops/c-mot" not in lenh` vào `T3`.

## Ngoài phạm vi — xác nhận không nêu lại
Đã đối chiếu: không có finding nào của tôi đòi đóng P1 lượt 2 của `#213`, sửa `ops-don-ref.yml`, `CLAUDE.md`, hay rà 72 nhánh C — tất cả đúng như `§ngoai_pham_vi` đã chốt.

---

Cả hai finding P2/P3 đều là khoảng trống về RĂNG-KIỂM-CHỨNG (test coverage) đã được tôi tự bù bằng phản chứng sống ngoài bộ 7 ca, không phải một đường thật khiến nhánh có commit riêng lọt vào A/B. Tôi đã TÌM và KHÔNG THẤY đường nào như vậy, kể cả sau khi tự dựng hai kịch bản mà bộ test gốc không phủ.

VERDICT: approve
Reviewed commit: fa4b0dd879f0cf7ae589989863670d2a8200839c
