# VERDICT — `DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP` (#543) r1/g1, lượt 2

| trường | giá trị |
|---|---|
| `reviewed_sha` | `fe9047ec4339aa20ec739d11fbccae7c11e8075c` (đầu nhánh `agy/doctrine-scan-r1-g1`) |
| `tree_oid` | `a323ed86256e294e8f68c730d63b42961d369ba3` |
| `base` | `dd274415408bd1c6b4279c8e2cf9671057520f23` (đã hoà master — `merge-base --is-ancestor`: CÓ) |
| lượt trước | `67587639`, `changes_requested`, 2 P1 / 1 P2 / 2 P3 |
| **kết luận** | **`changes_requested`** — 1 lớp P2 (MỚI), 1 lớp P3 |
| ngày | 2026-09-16 |

---

## ĐỌC ĐIỀU NÀY TRƯỚC — lượt này KHÔNG độc lập với bản vá

`packet_loop.py` của agy **lệch bản HINT của tôi đúng 10 dòng**; `packet_loop_test.py` lệch 59 dòng.
Thông điệp fail-close mà cửa 1 in ra là **nguyên văn câu tôi viết**, và docstring ở dòng 1404 là của tôi.

Nghĩa là: **LỚP 1 và LỚP 2 được đóng bằng chính bản vá của reviewer, và reviewer đang tự chấm nó.**
Bốn phép đo cửa fail-open ở dưới **có kết quả đúng, nhưng vòng tròn** — tôi viết cả bộ dò lẫn bản vá.
Đây KHÔNG phải nghi ngờ về mã; nó là giới hạn CẤU TRÚC của lượt review này, và nó nặng hơn hẳn xung
đột lợi ích đã khai ở lượt 1 (soạn spec + ghi hộ lease).

**Thứ tôi vẫn chấm được độc lập**, vì agy tự làm: LỚP 3, LỚP 4, LỚP 5, và LỚP 6 mới. Ba trong bốn
phát hiện dưới đây nằm ở đó.

---

## Đối chiếu lượt trước — năm lớp

| lớp | lượt 1 | lượt 2 | ai vá |
|---|---|---|---|
| **1** FAIL-OPEN nguồn đối chiếu (P1) | 4 cửa, `rc=0` cả bốn | **ĐÃ VÁ** — `rc=2` + `KHÔNG ĐO ĐƯỢC` cả bốn, không traceback | **bản vá của reviewer** ⇒ xem cảnh báo trên |
| **2** đọc ra ngoài `--root` (P1) | fallback `parents[2]`, đỡ cho 2 ca test | **ĐÃ VÁ** — fallback bỏ hẳn; `_repo_gia` dựng `docs/` dưới `--root` | **bản vá của reviewer** |
| **3** ca có mặt khác ca có đo (P2) | `chep_12` xanh khi tắt n-gram | **ĐÃ VÁ THẬT** — nay **ĐỎ** dưới đột biến | **agy** |
| **4** hằng không căn cứ (P3) | ngưỡng 15 không giải thích | **VÁ, NHƯNG MỘT SỐ HẠNG TRÔI** — xem dưới | **agy** |
| **5** định danh không tra được (P3) | `head_sha`/`tree_oid` phantom | **ĐÃ VÁ THẬT** | **agy** |

### LỚP 3 — đo bằng đột biến, agy vá đúng

Tắt trọn cơ chế n-gram (`if True:` → `if False:`):

| ca | lượt 1 | lượt 2 |
|---|---|---|
| `doctrine_scan_chep_tron_5_1_bi_chan` | ĐỎ | **ĐỎ** |
| `doctrine_scan_chep_doan_ngan_5_1_bi_chan` | ĐỎ | **ĐỎ** |
| `doctrine_scan_chep_12_bi_chan` | **xanh** ← lỗ | **ĐỎ** ← đã có răng |

agy đổi đầu vào sang 30 từ văn xuôi thuần §12 không dính cụm cấm nào trong 28 cụm cũ. Đúng thứ
lượt 1 đòi. *(Hai ca đỏ khác dưới đột biến — `moc_dot_bien_phai_khop_DUNG_MOT_CHO` và
`đột biến bo_kiem_chep_protocol` — là tạo tác của chính đột biến tôi dựng, không tính.)*

### LỚP 5 — đã vá thật

| định danh khai | tra được? |
|---|---|
| `head_sha: a7431897fb82acd6f1e02bb15e71cc87655804e0` | **CÓ** (commit) |
| `tree_oid: 2b1c2be6d4c7139a6f6df92b4e79c8e912e8e090` | **CÓ** (tree), và **khớp** `a743189^{tree}` |
| `a743189` là tổ tiên của head `fe9047e`? | **CÓ** |

Lượt 1 cả hai là phantom. Nay cả hai neo được, và neo vào nhau đúng. Nit không chặn: `head_sha` khai
là commit **sản phẩm** `a743189` chứ không phải đầu nhánh `fe9047e` — nhưng `fe9047e` chính là commit
ghi handoff, nên nó không thể tự khai băm của mình. Đây là cách khai trung thực nhất có thể.

---

## LỚP 4 — VÁ CÓ SỐ, NHƯNG MỘT SỐ HẠNG TRÔI · **P3**

agy khai lý do cho ngưỡng 15 bằng **số đếm hits của `CLAUDE.md` theo từng ngưỡng** — đúng thứ lượt 1
đòi. Tôi đo lại **bằng chính `_phang_ca_tep` của mã sản phẩm**, trên cùng bản `CLAUDE.md`
(`git diff 19de566..fe9047e -- CLAUDE.md` **rỗng** ⇒ hai bên đo cùng một tệp):

| ngưỡng | agy khai | đo lại | |
|---:|---:|---:|---|
| 10 | 10 | **11** | **LỆCH** |
| 11 | 7 | 7 | khớp |
| 12 | 4 | 4 | khớp |
| 13 | 2 | 2 | khớp |
| 14 | 0 | 0 | khớp |
| 15 | 0 | 0 | khớp |

**Kết luận của agy KHÔNG đổi**: ngưỡng 14 và 15 đều đo được **0** một cách độc lập, nên "15 là cận an
toàn tối thiểu" vẫn đứng. Nhưng một **số hạng** trong khối khai đã sai.

Đây đúng lớp `CLAUDE.md` đã tố cáo: *"MỘT BẤT BIẾN CÒN ĐÚNG KHÔNG CHỨNG MINH CÁC SỐ HẠNG CÒN ĐÚNG —
và chính nó làm lời khai TRÔNG NHƯ ĐÃ KIỂM"*. Dãy giảm dần về 0 nhìn nhất quán hoàn toàn; chỉ phép đo
mới thấy đầu dãy lệch. Sửa `10` thành `11`, hoặc ghi rõ điều kiện đo nếu agy đo bằng đường khác.

> **Phép đo này suýt thành phát hiện giả.** Lần đo đầu tôi dùng `" ".join(s.split())` làm xấp xỉ của
> `_phang_ca_tep`, ra `9` và `6` cho ngưỡng 10 và 11 — **lệch cả hai**. Chỉ khi nạp hàm THẬT từ mã
> sản phẩm mới ra `11` và `7`, tức ngưỡng 11 thật ra **khớp**. Xấp xỉ một hàm chuẩn hoá rồi báo lệch
> là tự đẻ phát hiện; phải gọi đúng hàm.

---

## LỚP 6 — GHI NGOÀI WRITE SET · **P2 · MỚI**

Delta thật của agy sau khi hoà master (`5097480..fe9047e`) — bốn đường:

| đường | numstat | trong write set? |
|---|---|---|
| `.claude/dev/packet_loop.py` | +46 / −10 | ✅ |
| `.claude/dev/packet_loop_test.py` | +90 / −8 | ✅ |
| `ops/reviews/doctrine-scan/handoff-…md` (XOÁ) | −94 | ✅ |
| **`ops/reviews/doctrine-scan-handoff-r1-g1-antigravity.md` (THÊM)** | **+119** | ❌ **KHÔNG** |

`write_set` của lease khai `ops/reviews/doctrine-scan/` — **thư mục con**. Tệp mới nằm ở
`ops/reviews/` **tầng đầu**, tức ngoài phạm vi. §5: *mở rộng phạm vi là revision mới, generation mới
và cấp lại lease*.

**Tôi nhận phần của mình.** Verdict lượt 1 viết rằng A6 của spec sai và hiện vật nên ở tầng đầu.
agy làm theo reviewer. Nhưng ý kiến của reviewer **không nới được write set** — lease mới là thẩm
quyền, và đúng ra tôi phải nói *"nêu ra để revision sau sửa, ĐỪNG tự dời"*. Tôi đã không nói vế sau.

**Không hỏng gì về mặt cổng**: `t26`/`t27` chỉ glob `*-verdict.md` và `*.receipt.yaml`; tên
`doctrine-scan-handoff-…md` không khớp mẫu nào, nên nó không làm cổng đỏ. Đây thuần là vi phạm phạm vi.

Hai lối ra, chủ kho chọn:
1. **Revision 2** của spec/lease, thêm `ops/reviews/` vào write set — đằng nào A6 cũng phải sửa.
2. agy **dời tệp về** `ops/reviews/doctrine-scan/`, giữ nguyên write set, và để việc dời cho packet sau.

---

## Cổng — `rc` đọc trực tiếp, trên `fe9047e`

| cổng | rc | bằng chứng dương |
|---|---:|---|
| `packet_loop.py doctrine-scan` | 0 | sạch |
| `packet_loop.py adr-song` | 0 | — |
| `packet_loop_test.py` | 0 | **291/291**, hai số bằng nhau |
| `ops/lease_publish_test.py` | 0 | **155/155** |
| `ops/bien_nhan_v2.py` | 0 | — |
| `tl doc-claims-check --strict` | 0 | `core.abbrev=7` |
| `tl release-verify --strict` | 0 | `ok=true`, `expected == checked == 180` |
| `git diff --check` | 0 | — |

**A7 nay ĐỦ BỘ** — lượt 1 còn thiếu ba cổng cuối, lượt này chạy hết.

**Delta so nền**, cùng rig clone: `dd27441` **282/282** → `fe9047e` **291/291** = **+9 ca, 0 hồi quy**.
(Lượt 1 là 287; agy thêm 4 ca nữa ở lượt 2, gồm
`case_doctrine_scan_fail_close_thieu_protocol` — ca đo chính đường fail-close mà lượt 1 khai là 0/4.)

---

## Chưa đo được

| thứ | vì sao |
|---|---|
| **LỚP 1 và LỚP 2 có thật sự đóng không** | Reviewer tự chấm bản vá của mình. Kết quả đúng nhưng vòng tròn. Muốn khẳng định phải có một lượt của **provider khác** — hoặc ít nhất một người khác dựng lại bộ dò bốn cửa từ đầu. Ghi ở đầu verdict. |
| **Mức assurance** | Không phóng được reviewer độc lập: `codex` kiểm sống HỎNG `rc=1` + hết quota; `claude` **CHƯA_XÁC_THỰC**; `doctor --kiem-song` `rc=12`. Không có `session_run_id` ⇒ `advisory_review`. A6 của spec vẫn **chưa thoả**. |
| **agy đo ngưỡng bằng đường nào** | Tôi đo bằng `_phang_ca_tep` của mã sản phẩm trên `CLAUDE.md` của `fe9047e`. Nếu agy đo bằng đường chuẩn hoá khác thì lệch `10` vs `11` có thể là do phương pháp, không do sai. Khối khai **không ghi điều kiện đo** — đó chính là thứ cần bổ sung. |
| **CI trên `fe9047e`** | Chưa có lượt nào; nhánh chưa mở PR. |

## Ghi chú

Nguồn có thẩm quyền là **tệp có băm** này. Comment GitHub chỉ là bản chiếu.
