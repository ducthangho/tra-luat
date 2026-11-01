# Đặc tả packet `ADR-0060-MAC-DINH` r1: ADR-0060 thành luật mặc định, đóng băng ADR-0054

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `ADR-0060-MAC-DINH`, revision 1, generation 1 |
| packet_issue | ghi ở comment đầu của Issue mở cùng đặc tả này |
| nguon_cap_viec | chỉ thị chủ kho `ducthangho` ngày 01-11-2026 trong phiên `session_015GtxrYPjZCTZeRiazdssgq`, giao cho phiên `session_015GtxramaGcW4MVoHByjp3Z` sau khi packet C land (PR #1116, merge `aeecf9f`). Chủ kho muốn: ADR-0060 thành luật mặc định, bỏ dòng khai M10, đóng băng ADR-0054, chuyển các bất biến còn giá trị sang protocol, cập nhật §20 |
| ưu tiên | chủ kho đặt gọn nhẹ, tốc độ và hiệu năng quy trình **trên** độ chặt của vật chứng |
| review_class | `sensitive`, vì sửa cổng `kiem-merge` trong `.claude/dev/packet_loop.py` (§20) |
| base | `origin/master` lúc cấp lease. Đo khi soạn (16:20Z 01-11): `c82047d` |
| depends_on | #1120 `KIEM-MERGE-M9` land. Lease của nó đang giữ `.claude/dev/packet_loop.py` và `.claude/dev/packet_loop_test.py` (`ai-dang-giu` rc=11, đo 16:15Z 01-11). Lease packet này chỉ cấp sau khi lease ấy hết hiệu lực |
| executor / reviewer | `anthropic_claude` (Claude Code remote, Linux) / `openai_codex` qua `launcher.py run` trên clone độc lập, cùng connector `@codex review` trên PR draft |
| windows | `required` theo M3 (diff chạm `.claude/dev/**`); chủ kho đã chọn **miễn** (`owner_waived`, A10). Comment miễn phải neo SHA ứng viên |
| full_mutant_audit | bắt buộc theo M9; **giữ**, không miễn (A11) |

## 1. Vì sao — số đo (01-11-2026, đo trên `c82047d` lúc 16:00–16:20Z)

| # | sự kiện | số đo |
|---|---|---|
| S1 | ADR-0060 M10 | luật chỉ áp khi đặc tả có **đúng một** dòng `dieu_kien_merge: ADR-0060@<OID>` hợp lệ; thiếu dòng ⇒ luật cũ |
| S2 | dòng khai trong kho | 5 tệp trong `ops/specs/` mang dòng `dieu_kien_merge` |
| S3 | cổng | `kiem-merge` K1 (`packet_loop.py`, hàm `k1` trong `cmd_kiem_merge`) đỏ khi số dòng khớp `LUAT_0060_RE` khác 1 |
| S4 | ADR-0054 | §20 ghi *"Accepted — chưa kích hoạt"*. Chỉ chính ADR-0054 chứa chuỗi `kích hoạt \`ADR-0054\``, nên `_che_do_0054` không ra True được, tức nhánh `luat_adr0054` của máy trạng thái chưa bao giờ chạy |
| S5 | ADR-0054 trong protocol | 16 dòng của `docs/PROTOCOL_DA_PHIEN.md` nhắc `ADR-0054` (dòng 241–1541), phần lớn là nhánh *"packet áp ADR-0054 / chưa áp"* |
| S6 | trùng nội dung | bốn mục của ADR-0054 có bản tương ứng trong ADR-0060: §1 push ↔ M5, §2 review offline ↔ M12, §3 dừng theo hạng ↔ M1, §4 theo lớp ↔ M2 |

## 2. Quyết định đã chốt (hai vòng hỏi chủ kho, 01-11-2026)

| # | câu hỏi | chủ kho chọn |
|---|---|---|
| Q1 | phạm vi | làm trọn (luật, cổng, test) trong một packet; đợi #1120 land rồi mới cấp lease |
| Q2 | đặc tả cũ có dòng khai | chấp nhận nhưng thừa: có thì vẫn kiểm OID, không có thì áp mặc định |
| Q3 | đóng băng ADR-0054 | chỉ tài liệu. Code `MAY-ADR-0054` trong `packet_loop.py` giữ nguyên, ở trạng thái ngủ |
| Q4 | luật cũ (nhánh "chưa áp" của bảng ngưỡng §8) | bỏ hẳn. Còn một luật duy nhất |
| Q5 | chỗ sửa M10 | một ADR mới `ADR-0061`, ngắn. `ADR-0060` không đổi byte nào |
| Q6 | miễn trước | miễn Windows (A10), giữ `full_mutant_audit` (A11) |
| Q7 | bất biến chuyển sang protocol | cả ba: (a) cổng tại chỗ trước push · (b) push thêm vì CI đỏ · (c) nhánh sổ sách ngoài luật đếm push |
| Q8 | K1 | 0 dòng ⇒ đạt; 1 dòng ⇒ phải hợp lệ như cũ; ≥ 2 dòng ⇒ đỏ |
| Q9 | ba skill (`cross-review`, `land-packets`, `work-packet`) | không sửa. Câu *"Packet áp ADR-0060"* vẫn đúng khi mọi packet đều áp |
| Q10 | tên và trần | `ADR-0060-MAC-DINH` r1; trần chuẩn ADR-0053 (sensitive) và ADR-0055 (lời gọi Codex) |

**Cách đọc (c) cùng ADR-0060 M5.** M5 viết *"Không không gian tên nào được miễn đếm"*. Câu ấy nhắm vào việc đẩy CODE
ứng viên sang một tên ref khác (xem mục *Phương án bị loại* của ADR-0060). Bất biến (c) nói về nhánh **chỉ chứa sổ
sách** (`ops/leases/**`, `ops/specs/**`, biên nhận, bia mộ): chúng không chứa tệp nào của write set code, nên không
phải lần push code. Hai câu không mâu thuẫn. ADR-0061 phải viết rõ: một nhánh chứa bất kỳ tệp nào thuộc write set
code của packet thì là nhánh code và bị đếm, bất kể tên.

## 3. Write set

| # | đường dẫn | việc |
|---|---|---|
| W1 | `docs/adr/0061-adr-0060-mac-dinh-va-dong-bang-adr-0054.md` | tệp mới |
| W2 | `docs/adr/0054-push-mot-lan-dung-va-theo-hang-va-review-theo-lop.md` | chỉ khối `Trạng thái` ở đầu tệp |
| W3 | `docs/PROTOCOL_DA_PHIEN.md` | gộp nhánh, thêm bất biến, §20 |
| W4 | `.claude/dev/packet_loop.py` | K1 |
| W5 | `.claude/dev/packet_loop_test.py` | ca K1 mới + đột biến |

Tổng: 5 tệp. Dự kiến 150–250 dòng thêm. Trần ADR-0053 (sensitive): 6 tệp / 450 dòng thêm.

## 4. Mục tiêu

1. **(W1)** `ADR-0061`, trạng thái `Accepted`, gồm đúng bốn điều:
   - **N1 — thay M10 của ADR-0060.** ADR-0060 áp cho mọi packet chưa merge, kể từ commit land của ADR-0061 trên
     first-parent `master`. Không hồi tố packet đã merge. Dòng khai `dieu_kien_merge` thành tuỳ chọn: không có ⇒ áp;
     đúng một dòng ⇒ phải qua ba phép đo OID của M10 cũ, sai ⇒ đỏ (không còn rơi về luật cũ); từ hai dòng ⇒ đỏ.
   - **N2 — bỏ luật cũ.** Nhánh *"packet chưa áp"* của bảng ngưỡng §8 protocol hết hiệu lực. Bảng §8 chỉ còn trỏ
     sang ADR-0060.
   - **N3 — đóng băng ADR-0054.** ADR-0054 không bao giờ được kích hoạt. Bất biến (a)(b)(c) chuyển sang protocol
     (mục tiêu 3). Code `MAY-ADR-0054` giữ nguyên, ngủ; gỡ nó là việc của một packet khác nếu cần.
   - **N4 — cách đọc (c) cùng M5**, như đoạn *Cách đọc* ở §2 của đặc tả này.
2. **(W2)** Khối `Trạng thái` của ADR-0054 đổi thành *"Đóng băng (2026-11-…, `ADR-0061`) — không kích hoạt; bất biến
   còn giá trị đã chuyển sang `docs/PROTOCOL_DA_PHIEN.md`"*. Thân ADR không đổi.
3. **(W3)** Trong `docs/PROTOCOL_DA_PHIEN.md`:
   - **3a.** Mọi nhánh *"packet áp `ADR-0054`"* / *"packet chưa áp"* / *"packet áp `ADR-0060`"* được gộp thành một
     câu theo ADR-0060. Hai đoạn mô tả code ngủ (dòng 241–243 khi đo) được giữ nhưng ghi rõ nhánh ấy không còn đường
     kích hoạt.
   - **3b.** Thêm một mục ngắn gồm ba bất biến (a)(b)(c), mỗi bất biến một đoạn, nguồn ghi `ADR-0054` §1 và
     `ADR-0061`:
     - (a) trước lần push chính, trên đúng SHA sẽ đẩy: `python scripts/tl.py --selftest` ⇒ `N/N` hai số bằng nhau;
       các cổng đặc tả liệt kê; `git diff --check`;
     - (b) lần push thêm vì CI đỏ chỉ được sửa CI, không mang bản vá finding review; SHA mới phải review offline
       approve và chạy lại (a) trước khi đẩy; ghi SHA trước/sau, check đỏ, nguyên nhân vào biên nhận;
     - (c) nhánh chỉ chứa sổ sách nằm ngoài luật đếm push; nhánh chứa tệp thuộc write set code thì bị đếm, bất kể tên.
   - **3c.** §20: dòng `ADR-0054` đổi trạng thái thành *"Đóng băng bởi `ADR-0061`"*; dòng `ADR-0060` bỏ cụm *"cho
     packet có dòng khai `dieu_kien_merge` hợp lệ"* và ghi *"M10 bị thay bởi `ADR-0061`"*; thêm dòng `ADR-0061` kèm
     cột cổng `packet_loop.py` `kiem-merge` K1.
4. **(W4)** K1 của `kiem-merge`: kiểm `spec_hash` như cũ; sau đó 0 dòng khớp `LUAT_0060_RE` ⇒ đạt; đúng 1 dòng ⇒
   ba phép đo OID như cũ; ≥ 2 dòng ⇒ đỏ. Thông báo đỏ nêu số dòng đếm được. Không đổi K0, K2–K7 hay `kiem-dong-wp`.
5. **(W5)** Ca mới `cong_c_k1_khong_dong` (đặc tả không có dòng khai ⇒ `kiem-merge` rc=0) và hai đột biến có đích
   (bảng đột biến của `packet_loop_test.py`). Các ca cũ `cong_c_k1_l2` và `cong_c_k1_hai_dong` giữ nguyên, vẫn đỏ.

## 5. Nghiệm thu

Mọi phép khớp chuỗi trên `.md` chạy trên văn bản đã nối dòng **trong phạm vi từng đoạn** (L6 b). "Đoạn" = các dòng
liền nhau giữa hai dòng trống; một dòng bảng tính là một đoạn.

| # | mục tiêu | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|---|
| A1 | 1 | `python3 .claude/dev/packet_loop.py adr-song --root .` rc=0, và W1 có dòng `Trạng thái` chứa `Accepted` | xoá dòng `ADR-0061` khỏi §20 ⇒ `adr-song` khác 0 (đột biến tay, ghi lệnh + rc vào biên nhận) |
| A2 | 1 | W1 có đủ N1–N4. Vế dương: mỗi đoạn N1…N4 bắt đầu bằng `**N1` … `**N4`, đếm theo từng nhãn, mỗi nhãn đúng 1 | xoá đoạn N3 ⇒ đếm nhãn `**N3` = 0 |
| A3 | 2 | Vế dương: khối `Trạng thái` của W2 chứa `Đóng băng` và `ADR-0061`. Vế âm: `git diff B..H -- W2` chỉ chạm các dòng trước dòng tiêu đề `## 1.` | sửa một dòng trong `## 3.` ⇒ phép đo vị trí diff đỏ |
| A4 | 3a | Vế âm, đếm theo từng cụm trên W3 tại H: `packet chưa áp` = 0; `packet áp \`ADR-0054\`` = 0; `luật cũ` chỉ còn trong đoạn mô tả code ngủ hoặc không còn. Vế dương: đoạn ngay sau bảng ngưỡng §8 chứa `ADR-0060` và `ADR-0061` | giữ lại một nhánh *"packet chưa áp"* ở dòng 638 ⇒ đếm = 1 |
| A5 | 3b | Vế dương, mỗi bất biến một phép đo riêng trên đoạn của nó: (a) chứa `--selftest` và `git diff --check`; (b) chứa `chỉ được sửa CI` và `review offline`; (c) chứa `sổ sách` và `bất kể tên` | xoá đoạn (b) ⇒ phép đo (b) đỏ còn (a)(c) xanh |
| A6 | 3c | §20: dòng bảng bắt đầu `\| \`ADR-0054\` \|` chứa `Đóng băng`; dòng `\| \`ADR-0060\` \|` chứa `ADR-0061` và không chứa `cho packet có dòng khai`; dòng `\| \`ADR-0061\` \|` tồn tại và chứa `kiem-merge` | để nguyên dòng `ADR-0060` cũ ⇒ vế âm đỏ |
| A7 | 4, 5 | `python3 .claude/dev/packet_loop_test.py` ⇒ N/N hai số bằng nhau; trong đó `cong_c_k1_khong_dong`, `cong_c_k1_l2`, `cong_c_k1_hai_dong` cùng đạt | đột biến **M-a**: K1 đòi lại đúng một dòng ⇒ `cong_c_k1_khong_dong` đỏ. Đột biến **M-b**: K1 nhận `len(khai) >= 1` và lấy dòng đầu ⇒ `cong_c_k1_hai_dong` đỏ. Cả hai nằm trong bảng đột biến của test, chết bằng assertion của đúng ca đích |
| A8 | 4 | `ruff check --select F .claude/dev/packet_loop.py` delta so base = 0 | thêm một tên không định nghĩa ⇒ delta F821 = 1 |
| A9 | toàn bộ | trên H: `python3 .claude/dev/packet_loop.py doctrine-scan --root .` rc=0; `python scripts/tl.py --selftest` N/N; `git diff --check B..H` rỗng | bất kỳ lệnh nào khác 0 |
| A10 | Windows | `owner_waived` (Q6), neo SHA ứng viên bằng comment chủ kho trên PR | không có comment neo SHA H ⇒ K5/K6 của `kiem-merge` đỏ |
| A11 | M9 | `full_mutant_audit` (`ci-dot-bien-du.yml`) `success` trên H, hoặc K7 nếu #1120 đã land | run thiếu hoặc `conclusion` ≠ `success` ⇒ K7 đỏ |
| A12 | kích thước | `git diff --numstat B..H`: đúng 5 tệp W1–W5, tổng dòng thêm ≤ 450 | thêm tệp thứ 7 hoặc vượt 450 ⇒ đỏ |
| A13 | canary sau land | packet đầu tiên sau land có đặc tả **không** mang dòng `dieu_kien_merge` chạy `kiem-merge` qua K1 | `chưa đo được` cho tới packet ấy. Người đo: executor của packet ấy, dẫn rc và dòng K1 vào biên bản M8 của nó |

Chạy thử trên nền `c82047d` (16:20Z 01-11): `adr-song` rc=0, `doctrine-scan` rc=0 (tiêu chí bất biến, xanh sẵn là
đúng). A1 vế "W1 có dòng Accepted", A2–A7 đo hành vi mới nên trên nền là màu "chưa làm" (W1 chưa tồn tại; protocol
còn 16 dòng nhắc ADR-0054; ca `cong_c_k1_khong_dong` chưa có).

## 6. Ngoài phạm vi

- Gỡ code `MAY-ADR-0054` (`luat_adr0054`, `_che_do_0054`, `accept`, `mo-lai`, `chu-kho-duyet`): chủ kho chọn chỉ tài
  liệu (Q3). Test 61 chỗ nhắc ADR-0054 giữ nguyên.
- Sửa ADR-0060: không đổi byte nào (Q5).
- Ba skill adapter: không sửa (Q9).
- K7 `full_mutant_audit`: thuộc #1120.
- Xoá dòng `dieu_kien_merge` khỏi 5 đặc tả cũ: đặc tả đã đóng băng không sửa đè.

## 7. hinh_dang_ke_thua

`khong_ap_dung`: packet này không khắc phục packet nào.

## 8. chua_do_duoc

- A13 chỉ đo được sau land.
- Trạng thái lease của #1120 lúc cấp lease: phải đo lại bằng `ai-dang-giu` sau khi fetch đủ ref và so TẬP tên
  `ls-remote` với `for-each-ref`.
- Số dòng thêm thật: 150–250 là ước tính, chưa đo.
