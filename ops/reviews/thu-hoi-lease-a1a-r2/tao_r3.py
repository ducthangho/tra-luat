from pathlib import Path
s=Path("ops/specs/THU-HOI-LEASE-A1a-r2.md").read_text(encoding="utf-8")
def rep(a,b):
    global s
    assert s.count(a)==1,a[:80]; s=s.replace(a,b)
rep("# ĐẶC TẢ — `THU-HOI-LEASE-A1a` — **revision 2**, bản nháp 7 (chưa đóng băng)",
    "# ĐẶC TẢ — `THU-HOI-LEASE-A1a` — **revision 3**, bản nháp 1 (chưa đóng băng)")
# revision row: prepend r3 note
i=s.index("| `revision` | 2 — **bản nháp 7**.")
rep("| `revision` | 2 — **bản nháp 7**.", "| `revision` | **3** — bản nháp 1. **Chỉ** đổi chỉ dẫn bộ đo THI CÔNG ở §8 mục 2 (F18 lượt 8; §0 vòng 5); mọi phần khác nguyên văn r2. Lịch sử r2 giữ nguyên dưới đây: 2 — **bản nháp 7**.")
rep("| `thay_the_cho` | revision 1 `ops/specs/THU-HOI-LEASE-A1a.md`,",
    "| `thay_the_cho` | **revision 2** `ops/specs/THU-HOI-LEASE-A1a-r2.md`, sha256 `9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd` (400 dòng; đóng băng bằng human audit #652 [`5851587276`](https://github.com/ducthangho/tra-luat/pull/652#issuecomment-5851587276), land ở merge commit `67802bf9`). Tệp r2 **giữ nguyên**. r2 thay cho revision 1 `ops/specs/THU-HOI-LEASE-A1a.md`,")
rep("Trần nâng lần 2 lên **10** (#564 `5851241285`); đã dùng **6/10**. |",
    "Trần nâng lần 2 lên **10** (#564 `5851241285`). Tới lúc r2 đóng băng đã dùng **7/10**; lượt 8 (hậu kiểm connector, PR #658) là **8/10**; r3 dùng tối đa hai lượt còn lại. Từ lượt 9, reviewer **chỉ mô tả bằng lời** mọi sửa nhắm đặc tả (§0 vòng 5). |")
rep("| `dong_bang` | lặp codex tới `approve` (0 P1/P2/P3) hoặc chạm trần 10, rồi **human audit của chủ kho**, rồi merge bằng merge commit (§0 vòng 4).",
    "| `dong_bang` | lặp codex tới `approve` (0 P1/P2/P3) hoặc chạm trần 10, rồi **human audit của chủ kho** neo r3, rồi merge PR #658 bằng merge commit (§0 vòng 4, vòng 5).")
rep("`claude/spec-a1a-r2-20260926`. Tên nhánh sẽ trôi hoặc bị xoá, băm thì không.",
    "`claude/a1a-r2-hau-kiem-connector`. Tên nhánh sẽ trôi hoặc bị xoá, băm thì không.")
# §0 vong 5, insert before "F1 là lần thứ 7"
rep("F1 là lần thứ 7 của hình dạng đã đếm ở §7.",
"""### Vòng 5 (mới ở revision 3; mỏ neo #564 [`5852159297`](https://github.com/ducthangho/tra-luat/issues/564#issuecomment-5852159297), 27-09-2026)

| câu | nguyên văn lựa chọn | hệ quả |
|---|---|---|
| F18 lượt 8 (P1, lớp `q6-thieu-kiem-id-ten`): r2 đóng băng bắt executor chạy `do_q6.py`/`mut_q6.py`, đúng bộ đo mang lỗi C5/C6 của hậu kiểm connector #652 | **"Đồng ý, làm đi"** (đề xuất revision 3 tối thiểu) | Revision 3 chỉ đổi chỉ dẫn bộ đo THI CÔNG (§8 mục 2, khối "Bộ đo THI CÔNG"); r2 và hai script gốc giữ nguyên byte làm hồ sơ đo |
| Protocol §13 ràng buộc 3 (patch-as-hint nhắm đặc tả trên packet `sensitive`) | cùng câu trên | Từ lượt 9, reviewer **chỉ mô tả bằng lời** mọi sửa nhắm đặc tả; HINT lượt 1–6 giữ nguyên với nhãn và provenance đã khai |

F1 là lần thứ 7 của hình dạng đã đếm ở §7.""")
rep("""   `2026-09-08T10:17:12Z` cho cùng kết quả — clock không phải một nguồn trôi. Executor chạy lại đúng lệnh trên
   **và** `--tu-kiem` **và** `mut_q6.py` lúc thi công, dán cả ba bản in vào thân PR; lệch digest, lệch số cặp, tự kiểm dưới 31/31, hoặc ma trận đột biến có dòng `LECH`
   ⇒ **DỪNG**, không ghim. Script là hiện vật review (nhánh đặc tả), **không** mở write set A1a.""",
"""   `2026-09-08T10:17:12Z` cho cùng kết quả — clock không phải một nguồn trôi. Các dòng trên (thuật toán, số đo, bảng
   đột biến 21/21) là **hồ sơ đo của r2** và giữ nguyên; chỉ dẫn chạy lúc thi công nằm ở khối ngay dưới.

   **Bộ đo THI CÔNG (revision 3 — thay cho mọi chỉ dẫn chạy `do_q6.py`/`mut_q6.py` ở trên).** Hậu kiểm connector
   #652 và lượt 8 (F18) chứng minh bộ đo r2 có hai lỗ: `do_q6.py` liệt kê bằng `ls-tree` không `-z`, nên tên lease
   có ký tự điều khiển bị git trích dẫn, đuôi thành `.yaml"`, và tệp lọt ra `ngoai_mien` **im lặng** với `rc=0`
   (C5); `mut_q6.py` không đọc mã thoát, nên mutant chết sớm không in `Traceback` được tính `KHOP` (C6). Hai tệp
   gốc giữ nguyên byte (đúng băm trích ở trên) làm hồ sơ; executor **KHÔNG** chạy chúng. Bản vá, cùng thư mục:

   | tệp | sha256 | nội dung |
   |---|---|---|
   | `do_q6_hk.py` | `0ec537e48b34631eee1e6161be2419bb7ba861a5a446b89afd4937672a974967` | thuật toán trên + liệt kê bằng `ls-tree -z`; tên có ký tự điều khiển (`< 0x20`, `0x7F`) ⇒ vi phạm `ten-tep-co-ky-tu-dieu-khien`; byte không-UTF-8 ⇒ vi phạm `ten-tep-khong-phai-utf8`; cả hai ⇒ `rc=3`, xét **trước** đuôi. Tự kiểm **35** ca (31 cũ + `ten-co-tab`, `ten-xuong-dong-sau-duoi`, `ten-DEL-sau-duoi`, `ten-byte-sau-duoi`) |
   | `mut_q6_hk.py` | `c4f04f03cf781089ae51faf1e8e63f1d7773bf301d2d61de0919f85a8428bb94` | ma trận **27** hàng: 22 hàng cũ + `doc-ls-tree-khong-z`, `bo-chot-ky-tu-dieu-khien`, `bo-rieng-DEL`, `bo-chot-utf8`, và đối chứng âm `chet-im-lang-rc2` (khai `mong="LECH"`). Phân hạng đòi mã thoát: tập đích rỗng ⇒ `rc` 0, có đích ⇒ `rc` 1, khác ⇒ `LECH`; bảy assert tự kiểm bộ phân hạng chạy trước ma trận |

   Lúc thi công executor (1) đo `sha256` hai tệp, lệch bảng trên ⇒ **DỪNG**; rồi (2) chạy đúng ba lệnh, `<kho>` như r2:

   ```
   python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py --tu-kiem <kho>
   python3 -B ops/reviews/thu-hoi-lease-a1a-r2/mut_q6_hk.py <tmp> <kho> ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py
   python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6_hk.py <kho> 072181157a27804e69deb35bb792a88c70ac31e3 2026-09-10T04:55:37Z
   ```

   và dán cả ba bản in vào thân PR. **Đạt** khi và chỉ khi **đủ** các điều sau; thiếu một ⇒ **DỪNG**, không ghim:

   | lệnh | tiêu chí dương (đọc bản in, không suy từ `rc` một mình) |
   |---|---|
   | tự kiểm | `rc=0`; dòng cuối đúng `TU_KIEM: 35/35 dat`; **0** dòng bắt đầu `HONG` |
   | ma trận | `rc=0`; dòng cuối đúng `TAT_CA_KHOP`; đúng **27** dòng bắt đầu `DUNG `; **0** dòng bắt đầu `SAI `; dòng `DUNG LECH` **duy nhất** là `chet-im-lang-rc2` — đó là đối chứng âm có chủ đích, không phải mutant lệch. Tiêu chí r2 *"có dòng `LECH` ⇒ dừng"* **không** áp cho bộ này: `LECH` ở đây là kết quả của hàng, còn `DUNG`/`SAI` mới là so với khai |
   | Q6 thật | `rc=0`; bản in `cmp`-bằng `ops/reviews/thu-hoi-lease-a1a-r2/q6-do-2026-09-26.json` (sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61`) — tức vẫn 89/89, 11 cặp, digest `8f372ccd…`, `BIA_MO_LICH_SU = ()` |

   Đo khi soạn r3 (27-09-2026, kho tại `d766717`): tự kiểm 35/35 · ma trận 27/27 `TAT_CA_KHOP` · Q6 `cmp` rc0. Bản in:
   `tu-kiem-q6-2026-09-27.log`, `mut-q6-2026-09-27.log`. Script là hiện vật review, **không** mở write set A1a.""")
Path("ops/specs/THU-HOI-LEASE-A1a-r3.md").write_text(s,encoding="utf-8")
