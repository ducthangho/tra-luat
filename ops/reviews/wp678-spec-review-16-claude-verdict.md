verdict: changes_requested
reviewed_sha: e39b73ed6f054178211c228e7d886eb9ed981f43
spec_sha256: 38637ba34099ece359d55baa160edeccbe8d2066c2451ae0d9f77c2dae83bbe1
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Subagent do phiên điều phối giao; model/effort là CẤU HÌNH được giao, không phải runtime evidence (model/effort đang phục vụ: KHÔNG ĐO ĐƯỢC). Không mạng, không đăng GitHub, không commit/push, không sửa `$R/cay-kho`; chỉ ghi dưới `$R/goi/` và thư mục `mktemp` `$R/w16.tEKT` (của lượt chết, dùng lại) cùng các thư mục tạm đã dọn.

Đây là lượt THỨ HAI của reviewer lượt 16: lượt đầu bị cắt khi container khởi động lại (~00:05Z), chỉ kịp bước 0 và một diff
theo từ r15→r16 (`w16.tEKT/wd.out`, `segs.txt`) cùng bản chép cây công cụ (`w16.tEKT/sp/`, `rv16/chay_rv15.py`,
`dung_rv15.py`). Lượt chết chỉ được dùng làm DỮ LIỆU; mọi kết luận dưới đây ĐO LẠI (bước 0, cây công cụ: `cmp` với nguồn)
hay ĐO MỚI ở lượt này (nhãn trong NHẬT KÝ).

Kết luận: **0 P1 / 1 P2 / 0 P3** (theo lớp).
- **P2 `tuong-tac-677-kiem-ke-t70-chua-neu` — CÒN MỞ** (lượt 8–16). Theo tiêu chí Q15 (PROMPT), cả hai finding là lỗi CỦA
  CHÍNH định nghĩa nhóm, không phải một cách né cổng mới trong nhóm đã khai:
  - **F16-1 — luật xếp nhóm KHÔNG TẤT ĐỊNH** (A8 :1487–1504), bốn chỗ đo được, hai chỗ đổi QUYẾT ĐỊNH phân hạng:
    câu (4) thiếu chữ *"của bản sao"* mà định nghĩa (β) có, nên guard GỐC — dưới seam luôn nhận `nen="nt"`, ĐO: 1/12/3/13/3/1
    khung ở `t51`/`t199`/`t203`/G1/G1b/G3, **0** lần đọc `os.name` — rơi vào (β) theo chữ (G1, G1b: (β) hay ngoài mọi nhóm);
    câu (5) đòi *"một thứ X … phép thử một biến"*: G2 chỉ đổi kết cục khi đặt CÙNG LÚC `__name__` và `sys.platform`
    (đo hai bản), còn *"đổi"* chưa định nghĩa nên đặt `os.name`=`nt` suốt ca làm kết cục đổi THOÁI HOÁ ở mọi ca dựng `Path`;
    câu (2) đọc theo chữ gặp `t125` (chạy lại TOÀN suite trong tiến trình con; đo trên D1, 12 biến thể kia theo đọc mã) nên 13/13 biến thể ở hàng (3)–(5) của §9 thành (γ);
    câu (1) *"ĐỎ ở MỌI lượt đã đo"* cho G6 nhãn (1) hay (α) tuỳ số lượt.
  - **F16-2 — (δ) KHÔNG THỰC SỰ BAO HẾT**: G1 (sửa `t199`) và G1b (sửa chuỗi nhánh `nt` của `t203`) lọt `t70`, `t193`, ca đích,
    (S) r13, `ruff` (delta 0), `quet13`/`quet14`/`quet14b` ở 3.11 và 3.12, và QUÉT ĐỦ (clone `ab457c6`, hai bản: (q1)–(q5) ĐẠT), ĐỎ trên Windows thật theo đọc mã,
    mà KHÔNG có X: kết cục dưới bộ quét (K `TinHieuChotCa`) đã BẰNG kết cục trên Windows; lỗ nằm ở (q3)/(q5) so TẬP TÊN với nền,
    và `t199`, `t203` vốn ở K của nền. Lập luận đủ (chữ MỚI của r16, từ HINT lượt 15 của chính tôi) chỉ chứng *"kết cục bằng
    nhau"*, không chứng *"cổng thấy"*; §9 *"ngoài mọi nhóm: không có biến thể nào"* sai khi tính G1, G1b.
  - Lớp lượt 15: **F15-1 VÁ SINH LỖI MỚI** (D1–D5, D7 nay thuộc (δ), đo; bản vá sinh F16-1, F16-2); **F15-2 ĐÃ VÁ THẬT**.
- **Không có P1**: khối chuỗi lệnh và `s5.py` giống byte r15 (`cmp` theo vùng rc=0 ×2, OID `c730245c…2694`); closure, năm điều
  kiện cấp và A1–A7 không đổi; luật xếp và Q15 chỉ đổi cách PHÂN HẠNG review, không đổi cổng của executor.
- **Số MỚI của r16**: mọi số hạng đo lại được đều KHỚP (BẢNG ĐO, 22 hàng); KHÔNG ĐO ĐƯỢC: REST (không mạng), Windows thật.
- **HINT** 1 nhóm / 5 hunk (A8 + §9): phạm vi "khung guard" (loại `t125`), câu (1) tất định bằng đọc mã, câu (2) ca tự tạo
  tiến trình con, câu (4) chỉ guard BẢN SAO (guard gốc dưới seam là seam), câu (5) TẬP X và phép thử BẰNG kết cục Windows;
  nghĩa vụ handoff cho ca của nền thuộc K, H − D, H2 − D bị đổi; lập luận đủ nói rõ *"bằng"* khác *"cổng thấy"*; đoạn
  *Review lượt 16 đo*; hàng §9. Dry-run: DRY-RUN dưới.

Tỷ lệ vá thật 15→16 (§12, PROTOCOL `ab457c6` :1087–1093): U = {`tuong-tac-677-kiem-ke-t70-chua-neu`}, F = ∅ ⇒ **0/1 = 0%**
theo lớp; theo finding **1/2** (F15-2 ĐÃ VÁ THẬT, F15-1 VÁ SINH LỖI MỚI). Chuỗi: … 12→13 1/3, 13→14 1/2, 14→15 0/1,
**15→16 0/1** ⇒ hai chuyển tiếp LIỀN NHAU dưới 50% (14→15, 15→16): PROTOCOL :1091–1093 *"thì dừng vòng vá và đưa bằng chứng
tới Review Rescue Checkpoint"* — Q15 dòng 12 nói Q13 (lặp không trần) chỉ còn áp cho các lớp KHÁC (LƯU Ý 2). Lớp mới
ngoài U: không. `tuong-tac-677-…` nay ở CHÍN lượt (8–16).

## BƯỚC 0 — định danh
```
$ date -u; sha256sum $R/SPEC.md $R/SPEC-r15.md   # ĐO LẠI 2026-10-08T00:12:08Z
38637ba34099ece359d55baa160edeccbe8d2066c2451ae0d9f77c2dae83bbe1  SPEC.md
41791ab0f4f9e7bf6352c39c3a96f2173f9a3248782a899935fa491fc1833569  SPEC-r15.md
$ git -C $R/cay-kho rev-parse HEAD
e39b73ed6f054178211c228e7d886eb9ed981f43
$ git -C $R/cay-kho config core.abbrev
7
```
Khớp cả ba ⇒ không `blocked` vì định danh.

## NHẬT KÝ TĂNG DẦN (w = `$R/w16.tEKT`, thư mục `mktemp` của lượt chết, dùng lại; mọi lệnh `python3 -B`)

- 00:12Z (ĐO LẠI) bước 0: băm, HEAD, `core.abbrev`, `status` 0 dòng — khớp.
- 00:14Z (ĐO LẠI) cây công cụ lượt chết `w/sp/` so nguồn `$SP/cr678-r13`, `$SP/cr678-r14` (CHỈ ĐỌC): `cmp` 6/6 tệp, `diff -rq nen` rc=0; `w/rv16/chay_rv15.py`, `dung_rv15.py` `cmp` = `luot15/do/rv15/` .
- 00:16Z (ĐO MỚI) 68 biến thể của ma trận r15 chép từ bảy thư mục nguồn (danh sách `BT` của `chay15.py`) vào `w/bt68`: 68/68 khớp `sha` của `r15do/kq/ma_tran_3.11.jsonl`. D dựng lại `w/btD`: 8/8 `bt.sha256`.
- 00:18Z (ĐO MỚI) `ruff` 0.15.8 `check --no-cache --isolated --select F` (`w/do/ruff_tat_ca.txt`): nền 9 lỗi; 76 biến thể (68 + 8 D): 75 delta 0, `N10_luong_nuot` +1 F401 (vốn bị vế H bắt) ⇒ cổng `ruff` không đổi hàng nào của bảng §9.
- 00:20Z (ĐO MỚI) `w/do/cong.py` tổng hợp cổng (câu (1)) từ hiện vật `r15do/kq` + `r16do/kq16`: 57 ĐỎ / 19 lọt; mọi hàng E5f, E8, V, D của bảng §9 khớp dữ liệu (lật, K, L, oracle, `t193` D6, E8w2 chỉ 3.12) — `w/do/cong.out`.
- 00:2xZ (ĐO LẠI) §3 Q15, dòng dõi, bản chiếu, nền, §10 (a)(b), A8 *Phiên soạn r16 đo lại*: BẢNG ĐO.
- 00:32:27Z–00:35:53Z (ĐO MỚI) `w/rv16/chay_rv16.py` (chép logic hàng của `chay_rv15.py`; ca đích theo biến thể; thêm `quet14b_x.py` = `quet14b.py` + 6 chỗ thay có `assert`, nút tắt mặc định — đối chứng `q14bx` = `q14b` ở MỌI hàng hai bản) trên NEN (`t199`, `t203`, `t51`), G1–G6 (`w/rv16/dung_rv16.py`, băm `w/rv16/btG.sha256`), D1, D5, D7, E8a, E8g, E8p; MỘT lệnh 3.11.15 ‖ 3.12.3; trả nền 16/16 mỗi bản, 0 `.pyc` (`w/do/rv16_tom.txt`).
- 00:38Z (ĐO MỚI) G6 bản 1 tôi dựng SAI (tham chiếu helper chỉ trong hàm lồng ⇒ `t70` ĐỎ, H − D) — bỏ; bản 2 (`goi = m2._chay_buoc_dang_that` cấp đỉnh): ma trận một lượt `quet14b` K hai bản; lặp 10 (`--lap 10`): 3.11 K 6/10, 3.12 K 8/10.
- 00:39:46Z– (ĐO MỚI, phép đo dài, nền) `w/rv16/chay_du16.py`: MỘT lệnh 3.11 ‖ 3.12, mỗi bản một clone `--shared` từ `$R/kho.git` (chỉ đọc), `checkout --detach ab457c6`, `core.abbrev 7`; `quet14b.py` QUÉT ĐỦ trên nền, G1, G1b liền nhau trên cùng clone, chạy từ gốc; rồi (3.12) `--chi-ca=t125_` trên D1. Xong 01:16:03Z (3.11 xong 01:07:01Z); kết quả ở HƯỚNG 6, 11 và CHI TIẾT F16-2 (`w/do/so_du16.out`).
- 00:4xZ (ĐO LẠI) BẢNG ĐO: dòng dõi, Q15, bản chiếu, nền `adg2` (chỉ đọc, mtime trước = sau), §10 (a) áp HINT 15 trong `mktemp`, khối/`s5.py` `cmp` theo vùng, định nghĩa reviewer, số A8/§9 trên hiện vật lượt 15 và phiên soạn r16.
- 00:5xZ HINT nháp `w/hint/mk_hint16.py` (thay chuỗi có `assert`, `diff -u --label`): 1 nhóm, 5 hunk, 0 dấu chéo ngược. `ruff` G6 bản 2 (`9f06fd81…`): delta 0.
- 01:02:18Z (ĐO MỚI) G7 (`ca9ddda8…`, sửa `t51`): một hàng `chay_rv16.py` (ánh xạ ca đích `G7` → `t51` thêm vào `dich_cua`), hai bản: `quet13`/`quet14`/`quet14b` N = {`t51`}, `q1_chi` true, K rỗng; `t193` rc=1 `0/1`; oracle ĐỎ *"bỏ qua không dẫn xuất được từ runs-on"*; `t51_`, `t70_` 1/1; (S) 0; `ruff` delta 0.
- 01:16:03Z (ĐO MỚI) phép đo dài xong: quét ĐỦ nền, G1, G1b hai bản ⇒ (q1)–(q5) ĐẠT cả G1, G1b (cùng tập với nền; lật 118 | 120 | 118 ở cả hai bản); `t125` trên D1: `t204_moi` vào cả hai tiến trình con; hai clone tự xoá.
- 01:2xZ HINT cuối (thêm câu quét đủ, câu `t125`, câu đối chứng G7): 1 nhóm, 5 hunk, 0 dấu chéo ngược; `kiem_hint16.sh`: dry-run rc=0, 5/5, áp thật rc=0, băm sau áp = `SPEC_moi.md` (`95e0a776…a05a`, 2926 dòng), khối và `s5.py` giữ OID (DRY-RUN dưới).
- 01:19:43Z (ĐO LẠI) toàn vẹn cuối lượt: `SPEC.md` `38637ba3…`, `SPEC-r15.md` `41791ab0…`, `luot15/VERDICT.md` `93da81f8…`, `luot15/HINT.patch` `90e749bf…` giữ băm; `cay-kho` HEAD `e39b73ed…`, `status --porcelain` 0 dòng; `kho.git` `origin-master` = `ab457c6…`. Dọn: `w/bt68`, `w/btD` (dựng lại được, băm ở `goi/do/rv16/*.sha256`), HOME/TMPDIR tạm, symlink python; 0 `.pyc`; `$R` 285 MB.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 15 (Claude Opus 5.5 max, trên `b533621`; VERDICT `93da81f8…0697` 248 dòng, HINT `90e749bf…0a92` 1 nhóm/4 hunk — băm đo lại
khớp): 0 P1 / 1 P2 / 0 P3. Nhãn finding theo PROTOCOL §8 (`ab457c6` :679–680); nhãn lớp theo §8.3 (:799–802: chỉ `ĐÃ VÁ THẬT` khi
mọi biểu hiện trong phạm vi đã đóng, không còn biểu hiện cùng cơ chế do bản vá sinh ra, không còn phần phải đo). Mọi bằng
chứng dưới đây tự đo ở lượt này.

| lớp (lượt 15) | finding lượt 15 | nhãn finding trên r16 | nhãn LỚP lượt 16 | bằng chứng tự đo |
|---|---|---|---|---|
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P2) | F15-1: bộ (α)(β)(γ) chưa vét; D1–D5, D7 lọt mà không thuộc nhóm nào | **VÁ SINH LỖI MỚI** | **CÒN MỞ** (lượt 8–16) | Phần đã đóng: r16 thêm (δ) là nhóm VÉT + lập luận đủ + luật xếp; D1–D5, D7 nay thuộc (δ): D1 đặt `__name__`=`__main__` ⇒ K `BoQuaNen@ban_sao_204`, D7 đặt `sys.platform`=`win32` ⇒ K (hai bản, `quet14b_x.py`); D2, D5 (`os.name` ngoài khung), D3 (`__name__`), D4 (`sys.getprofile()`) theo đọc mã; bảng §9 khớp dữ liệu ở mọi hàng. Phần SINH LỖI: luật xếp mới không tất định (F16-1) và lời khai VÉT không bao hết (F16-2: G1, G1b) |
| | F15-2 (mức P3): V10 làm bộ quét chết, kết cục không cố định | **ĐÃ VÁ THẬT** | | A8 :1278–1279 khai *"một ca như V10 còn có thể làm CHÍNH bộ quét chết … kết cục của nó đổi giữa các lượt: gặp thì handoff nêu, không tự tính là đạt"*; đoạn *Review lượt 15 đo* có số theo tính chất (V10 × 20: 3.11 K 20/20, L 16/20; 3.12 L 19/20, chết 1/20 — đo lại trên `luot15/do/rv15/kq_v10_20.jsonl`: khớp); hai câu cũ của phiên soạn r15 giữ như lời khai có ngày (r16 §9 (5) nói rõ) |

Phần còn lại của lớp lượt 15 (PROMPT mục 2): (a) V10 làm bộ quét chết — **ĐÃ ĐÓNG** (trên). (b) Điều kiện thứ tư của câu H2 —
**ĐÃ ĐÓNG**: A8 :1262–1265 *"VÀ kết cục của ca không phụ thuộc, trong hay ngoài khung guard, thứ gì khác … Bốn điều kiện là
điều kiện CẦN"*; D1, D2, D4, D7 có 1 lần lật mỗi lượt (`r16do/kq16`, `w/rv16/kq`) ⇒ khớp chữ *"D1, D2, D4, D7 thoả ba điều
kiện đầu"*. (c) Vòng đời hàm profile luồng chính — **ĐÃ ĐÓNG**: A8 :1241–1243 *"cài quanh MỖI ca và gỡ sau ca"* khớp
`quet14b.py` (`sys.setprofile(prof)` trước `f()`, `sys.setprofile(None)` trong `finally`); `quet14b_x.py` nút tắt = `quet14b.py`
ở mọi hàng. (d) (δ) là nhóm vét — **VÁ SINH LỖI MỚI** (F16-1, F16-2).

Lớp đã đóng ở lượt 14 (`chinh-xac-hoa-so-hieu-va-tham-chieu`) và lượt 7–13: KHÔNG tái phát — 22 hàng số ở BẢNG ĐO khớp;
khối chuỗi lệnh, `s5.py`, closure, objective không nằm trong 12 hunk r15→r16 ngoài các câu khai *"r16 cũng vậy"*.

## BẢNG LỚP
| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `tuong-tac-677-kiem-ke-t70-chua-neu` | **P2** (CÒN MỞ; lượt 8–16) | **F16-1**: luật xếp nhóm A8 :1487–1504 không tất định — (4) *"Có khung guard … mà … quyết định `nt` của nó không đọc `os.name`"* không giới hạn ở guard BẢN SAO như (β) :1468–1470, mà guard gốc dưới seam không bao giờ đọc `os.name` (đo 0 lần ở 33 khung mỗi bản) ⇒ G1, G1b, G3 vào (β) theo chữ; (5) *"một thứ X … phép thử một biến … đổi"*: G2 không có X một biến nào, có X hai biến; *"đổi"* nhận cả đổi thoái hoá (`NotImplementedError` khi đặt `os.name`); (2) theo chữ gặp `t125`; (1) phụ thuộc số lượt (G6). **F16-2**: (δ) không bao hết — G1, G1b lọt mọi cổng, ĐỎ trên Windows theo đọc mã, không X (kết cục quét = kết cục Windows); lỗ ở (q3)/(q5) so TẬP TÊN với nền mà `t199`, `t203` vốn ở K/H2 − D của nền; lập luận đủ không bắc cầu từ *"kết cục bằng"* sang *"cổng thấy"* | HINT 1 nhóm/5 hunk: (A) A8 sau câu tạo tác seam: (q3)–(q5) so tên ⇒ handoff liệt kê ca của nền thuộc K, H − D, H2 − D (`t71`, `t72`, `t73`, `t98`, `t193`, `t199`, `t203`) mà mã (đóng bao) khác nền, không tự tính là đạt; (B) lập luận đủ: guard gốc nhận `nen` từ seam; *"bằng"* ≠ *"cổng thấy"*; (C) luật xếp: phạm vi khung guard loại `t125`; (1) tất định bằng đọc mã; (2) ca tự tạo tiến trình con; (4) guard BẢN SAO; (5) TẬP X, phép thử đặt cùng lúc, kết cục phải BẰNG kết cục Windows; (D) đoạn *Review lượt 16 đo*; (E) hàng §9 | `w/rv16/chay_rv16.py` (MỘT lệnh, hai bản; `quet14b_x.py` nút tắt = `quet14b.py`), `--lap 10` cho G6, quét đủ `w/rv16/chay_du16.py`; dry-run HINT. Giới hạn: Windows thật KHÔNG ĐO ĐƯỢC (G1, G1b ĐỎ là đọc mã; oracle ĐỎ cả ở nền nên không phân biệt); phép thử một biến của tôi đặt thứ cả ca, không tại chỗ đọc |
## BẢNG SĂN

### Bảng xếp nhóm của reviewer (mục 1) — so bảng §9 r16

Dữ liệu cổng: `w/do/cong.out` (68 + 8 biến thể, hiện vật `r15do/kq`, `r16do/kq16`), `w/do/rv16_tom.txt` (G1–G6 và đối chứng, đo
mới 00:32Z–00:38Z; G7 01:02Z; hai bản), `ruff` (`w/do/ruff_tat_ca.txt`, `w/do/ruff_G.txt`). Cột **ĐỌC Ý** là cách đọc của tôi: câu (2)
chỉ tính tiến trình con do CHÍNH ca (hay mã nó chạy) tạo; câu (4) chỉ xét guard của BẢN SAO, như chữ (β) ở đoạn giới hạn;
câu (5) cho X là một TẬP. Cột **ĐỌC CHỮ** là kết quả khi áp đúng từng chữ của luật xếp r16 :1487–1504 (xem F16-1).

| biến thể | câu (ĐỌC Ý) | nhãn ĐỌC Ý | §9 r16 | ĐỌC CHỮ khác ở đâu | căn cứ đo |
|---|---|---|---|---|---|
| V1, V7 | (0) | hợp lệ, sạch | (0) sạch | — | cổng xanh, L rỗng; lật 300 \| 0 |
| V6, V8, V9, V10 | (0) | hợp lệ, tạo tác đã khai | (0) tạo tác | — | K hay L ở hai bản (V10 3.12 L, 3.11 K+L) |
| E8a, c, d, f, i, k, m, n, n2, r, s, t; E8j; E8b, E8h; E8w; E8w2; D6 | (1) | bị bắt | (1) | — | K/N/`t70`/`t193` như §9; E8w2 chỉ 3.12 |
| E5f | (2) | (γ) | (2) (γ) | — | 0 lật; ca tự gọi tiến trình con |
| E8v, E8u, E8e, E8l, E8q | (3) | (α) | (3) (α) | câu (2) chữ: (γ) — ca chạy lại trong tiến trình con của `t125` | 0 lật cả năm |
| E8g, E8p | (4) | (β) | (4) (β) | câu (2) chữ: (γ) | E8g 0 lật; E8p 1 khung guard, **0** lần đọc `os.name` thật (`doc_os` [1, 0]) |
| D1, D2, D3, D4, D5, D7 | (5) | (δ) | (5) (δ) | câu (2) chữ: (γ) | D1: đặt `__name__`=`__main__` ⇒ K `BoQuaNen@ban_sao_204`; D7: đặt `sys.platform`=`win32` ⇒ K; D2, D5: X = `os.name` ngoài khung; D3: `__name__`; D4: `sys.getprofile()` |
| **G1** (sửa `t199`) | (5) | **NGOÀI MỌI NHÓM** | — | câu (4) chữ: (β) (13 khung guard gốc qua seam, **0** lần đọc `os.name`); câu (2) chữ: (γ) | K `TinHieuChotCa@lease_publish_test` = nền, mọi bộ quét, hai bản; mọi phép thử một biến: không đổi hay đổi THOÁI HOÁ |
| **G1b** (sửa chuỗi nhánh `nt` của `t203`) | (5) | **NGOÀI MỌI NHÓM** | — | như G1 (3 khung, 0 lần đọc) | K `TinHieuChotCa` + H2 − D = nền; mọi phép thử một biến: không đổi |
| G2 (`__name__` VÀ `sys.platform`) | (5) | (δ), X = {`__name__`, `sys.platform`} | — | câu (5) chữ (một biến): đặt `__name__` ⇒ đạt, đặt `sys.platform` ⇒ đạt ⇒ *"không chỉ ra được"* ⇒ NGOÀI MỌI NHÓM; đặt cả hai ⇒ K | `w/do/rv16_tom.txt` |
| G3 (guard gốc, `nen` theo `sys.platform`) | (5) | (δ), X = `sys.platform` | — | câu (4) chữ: (β) (1 khung, 0 lần đọc) | đặt `sys.platform` ⇒ N, N − D, H2 − D (bị bắt) |
| G4 (rẽ theo tên đối tượng guard) | (5) | (δ), X = seam (thứ mới cùng tính chất) | — | câu (2) chữ: (γ) | bỏ seam ⇒ N; oracle ĐỎ (nó không có seam) |
| G5 (xoá tệp đang mở) | (5) | (δ), X = ngữ nghĩa hệ tệp Windows (không đặt được ⇒ đọc mã) | — | — (không khung guard nào) | mọi bộ quét đạt; oracle mù |
| G7 (sửa `t51` TRONG SỔ: ném lại `BoQuaNen` với `tep` là chuỗi) | (1) | bị bắt | — | — | `quet14b` (q1) xanh (N `t51` khớp sổ, K rỗng) nhưng `t193` `0/1` ở hai bản (M3 chạy `main()`: *"không dẫn xuất được"*); oracle ĐỎ cùng chuỗi; `ruff` delta 0 |
| G6 (ngẫu nhiên: khung ca hay `_thread` thô) | (1) hay (3) tuỳ số lượt | bị bắt / (α) | — | câu (1) *"ĐỎ ở MỌI lượt đã đo"*: một lượt ⇒ (1); 10 lượt ⇒ (3) | ma trận 1 lượt K hai bản; lặp 10: K 6/10 (3.11), 8/10 (3.12) |

Lệch so §9: KHÔNG ở mọi hàng §9 có (ĐỌC Ý). ĐỌC CHỮ đổi nhãn của 13/13 biến thể ở hàng (3)–(5) của §9 sang (γ) (câu (2) gặp `t125`).
Hàng §9 *"(5) ngoài mọi nhóm: không có biến thể nào trong số đã đo"* không còn đúng khi tính G1, G1b (ĐỌC Ý).

### Hướng

Mẫu: `HƯỚNG n: tên / giả thuyết / lệnh / output / kết luận`.

- HƯỚNG 1: phạm vi r15→r16 / khối lệnh và `s5.py` không đổi byte / trích theo vùng (mở ``` sau đoạn *Chuỗi lệnh đo điều kiện cấp*, khối ```python kế tiếp) rồi `cmp`, `git hash-object` (`w/do/khoi_r1x.txt`, `w/do/s5_r1x.txt`) / khối r15 :62–98 ↔ r16 :64–100 rc=0 (37 dòng, 4270 byte, OID `6ccd8418…`); `s5.py` r15 :118–324 ↔ r16 :120–326 rc=0 (207 dòng, 9886 byte, OID `c730245c…2694`), 0 dấu chéo ngược; `r15-r16.diff` 12 hunk, mọi hunk khớp bảng thay đổi đầu r16 / KHÔNG PHẢI LỖI.
- HƯỚNG 2: Q15 nguyên văn (mục 3) / thân REST có thực thể HTML ở dòng 7 / `html.unescape` dòng 7 rồi so từng byte dòng 3–12 với r16 :934–943 / 10/10 khớp; 37 thực thể số đều ở dòng 7 / KHÔNG PHẢI LỖI (lớp sinh thực thể: KHÔNG ĐO ĐƯỢC với một client, như r16 tự khai).
- HƯỚNG 3: dòng dõi, bản chiếu, nền, §10 (a)(b), A8 *Phiên soạn r16 đo lại* (mục 3) / — / BẢNG ĐO / 22/22 KHỚP (phần đo được); REST: KHÔNG ĐO ĐƯỢC / KHÔNG PHẢI LỖI.
- HƯỚNG 4: bảng §9 có khớp dữ liệu (mục 1) / — / `w/do/cong.py` trên `r15do/kq` + `r16do/kq16` / mọi hàng khớp: lật, K, N, L, oracle, `t193` D6, E8w2 chỉ 3.12; câu *"Các biến thể ở câu (2)–(5) có `t70`, `t193`, `t204` `1/1`, (S) r13 xanh, `quet14.py` cũng không bắt"* đúng 14 biến thể × 2 bản / KHÔNG PHẢI LỖI.
- HƯỚNG 5: cổng `ruff` của câu (1) cho E/V (bảng §9 không khai đã đo) / một biến thể E/V có F mới thì phải lên hàng (1) / `ruff` 0.15.8 trên 76 biến thể / 75 delta 0, `N10` +1 F401 (N10 vốn bị H bắt, không trong §9) / KHÔNG PHẢI LỖI.
- HƯỚNG 6: câu (2) theo chữ / *"khung guard mà lượt chạy thật trên Windows chạy tới nằm trong một tiến trình con"* đúng với mọi ca vì `t125` chạy lại toàn suite / đọc `t125` (goc :5024–5130: `_mo_con_nhom_rieng([sys.executable, <tệp>, CO_AB])` ×2; `_xac_minh_transcript_ab(out, [f.__name__ for f in CA])` đòi đủ MỌI ca) + ĐO `--chi-ca=t125_` trên D1 (3.12, clone đủ, 194,8 s, rc=0): dòng `[A] >>> vao t204_moi` và `[B] >>> vao t204_moi` mỗi dòng 1 lần, mỗi con 202 dòng `>>> vao` (201 ca nền + `t204_moi`) / theo chữ, 13/13 biến thể ở hàng (3)–(5) của §9 thành (γ) (D1 đo; 12 kia đọc mã: mọi ca chạy trong con vì `t125` đòi đủ MỌI ca, và mỗi biến thể chạm một khung guard trên Windows) / **LỖI** — F16-1 (c), chỉ đổi nhãn.
- HƯỚNG 7: câu (4) theo chữ / seam truyền `nen="nt"` nên quyết định của guard GỐC không đọc `os.name` / `quet14b_x.py X_DO_DOC_OS=1` (lớp con `ModuleType` gán `os.__class__`, ghi lần đọc `name` trong khung guard) / `t51` [1, 0], `t199` [12, 0], `t203` [3, 0], G1 [13, 0], G1b [3, 0], G3 [1, 0]; bản sao D1, D7, E8a, G2 [1, 1]; E8p [1, 0]; hai bản / **LỖI** — F16-1 (a): G1, G1b đổi quyết định; G3 đổi nhãn.
- HƯỚNG 8: câu (5) phép thử một biến / kết cục phụ thuộc HAI thứ thì không biến nào một mình đổi được / G2 + `X_TEN`, `X_PLATFORM`, cả hai / riêng: đạt, đạt; cả hai: K `BoQuaNen@ban_sao_204`; hai bản / **LỖI** — F16-1 (b): chữ cho *"ngoài mọi nhóm"* (P2), tính chất cho (δ).
- HƯỚNG 9: *"kết cục … đổi"* chưa định nghĩa / đặt X liệt kê ở (δ) mà kéo theo lỗi vô can thì *"đổi"* thoái hoá / `X_OS_NT_CA=1` / G1 `NotImplementedError` (thay `TinHieuChotCa`); G2, G5, G6, D1, D7, E8a `NotImplementedError`; E8g, E8p `NotImplementedError` (3.11), `FileNotFoundError` (3.12); NEN `t51` và D5: CHÍNH bộ quét chết (`Path.resolve`); `X_TEN=__main__` trên `t199`, G1: `AttributeError` (ca dùng `sys.modules[__name__]`) / **LỖI** — F16-1 (b).
- HƯỚNG 10: câu (1) *"ĐỎ ở MỌI lượt đã đo"* / số lượt quyết định nhãn / G6 bản 2: ma trận 1 lượt rồi `--lap 10` / 1 lượt: K hai bản ⇒ (1); 10 lượt: K 6/10 (3.11), 8/10 (3.12) ⇒ (3) (α) / **LỖI** — F16-1 (d), chỉ đổi nhãn; kèm: cổng nghiệm thu chạy một lần nên G6 lọt được (ước từ 10 lượt: 0,4 × 0,2 ≈ 8%, số của mẫu, không phải tính chất).
- HƯỚNG 11: (δ) có bao hết (mục 1) / (q3)/(q5) so TẬP TÊN với nền, `t199`, `t203` vốn ở K của nền ⇒ sửa chúng thành ĐỎ trên Windows không lộ / G1, G1b: `chay_rv16.py` + quét đủ `chay_du16.py` / `--chi`: K trùng nền cả tên lẫn lớp, suite, (S), `ruff` xanh, hai bản; mọi phép thử một biến không làm kết cục quét BẰNG Windows vì nó ĐÃ bằng; quét ĐỦ, hai bản: nền, G1, G1b cùng 201 ca = 187 đạt + N 12 + K {`t199`, `t203`} (`TinHieuChotCa`), H − D {`t193`}, H2 − D {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`}, L rỗng, status 0, 0 `.pyc` ⇒ (q1)–(q5) ĐẠT cho G1, G1b / **LỖI** — F16-2 (ngoài mọi nhóm theo ĐỌC Ý; (β) theo chữ câu (4) — chính F16-1 (a)).
- HƯỚNG 12: G3, G4, G5 (khác cơ chế) / guard gốc với `nen` tính ngoài khung; rẽ theo định danh seam; ngữ nghĩa hệ tệp / `chay_rv16.py` / G3: đặt `sys.platform` ⇒ N, N − D, H2 − D; G4: bỏ seam ⇒ N, oracle ĐỎ; G5: mọi bộ quét đạt, oracle mù / KHÔNG PHẢI LỖI — trong giới hạn đã khai (δ) (G3 theo chữ (4) là (β), xem F16-1).
- HƯỚNG 13: P1 — r16 tự mâu thuẫn hay làm đúng chữ mà land không hợp lệ / — / đọc A8, §3, §9 với khối lệnh, closure, A1–A7 / câu (4) lệch chữ (β) là lệch giữa luật xếp (dùng cho PHÂN HẠNG review) và định nghĩa nhóm, đọc được theo hai cách, không đổi cổng nghiệm thu; A1–A7 không đòi sửa `t199`, `t203` / KHÔNG PHẢI LỖI ở mức P1.
- HƯỚNG 14: khoảng trống Q14 / r16 có Q13 rồi Q15 / `grep` §3 r15, r16 và `c678_since.json` / không có Q14 ở đâu; r16 không khai Q14 / KHÔNG PHẢI LỖI (cách đánh số của điều phối, không phải lời khai sai).
- HƯỚNG 15: trùng tên D1–D9 (§2, đường `lease_id`) với D1–D7 (biến thể) và D (tập vị từ `t70`) / người đọc nhầm / đọc §2 :741–746 và A8 / ngữ cảnh tách được (bảng §2 vs đoạn A8, §9) / KHÔNG PHẢI LỖI (ghi để r17 cân nhắc đổi tên biến thể).
- HƯỚNG 16: lỗi dụng cụ của chính tôi / — / G6 bản 1 chỉ tham chiếu helper trong hàm lồng / `t70` ĐỎ, H − D: biến thể không đo điều nó định đo / LỖI DỤNG CỤ REVIEW, đã sửa (bản 2) trước khi kết luận; mọi số G6 ở trên là bản 2.
- HƯỚNG 17: danh tính lượt này / — / — / Claude Opus 5.5 max, subagent; model/effort đang phục vụ KHÔNG ĐO ĐƯỢC.

## BẢNG ĐO
| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| §3 Q15: thân `6049086640` (id, tạo 23:42:21Z, `ducthangho` qua app `claude`, `OWNER`, sha256 `4a4ca52e…`, 1766 byte, 15 dòng, 37 thực thể số đều ở dòng 7) | như trái | `r16do/c6049086640.json` (mtime 23:49:02Z): đúng từng mục; dòng 7 có 37 thực thể, 27 loại, cả 37 dạng `&#N;` | KHỚP |
| §3 Q15: dòng 3–12 chép từng byte, dòng 7 sau `html.unescape` | như trái | so r16 :934–943 (bỏ tiền tố `  > `) với dòng 3–12 của thân: **10/10 dòng khớp byte** (279, 0, 38, 109, 296, 0, 9, 221, 452, 59 byte) | KHỚP |
| §3 Q15: thân nêu HAI ví dụ lỗi định nghĩa, mở bằng *"ví dụ"* | như trái | dòng 11: *"(ví dụ không tất định, hoặc tự mâu thuẫn)"* | KHỚP (ví dụ thứ ba *"do phiên điều phối giao kèm"*: KHÔNG ĐO ĐƯỢC) |
| bảng thay đổi: §3 r15 = Q1–Q4, Q7–Q13; r16 thêm Q15 | như trái | `grep '^- \*\*Q'` vùng §3: r15 `Q1 Q2 Q3 Q4 Q7 … Q13`; r16 thêm `Q15`; không có Q14 ở đâu trong r16 | KHỚP (khoảng trống Q14 không được giải thích — không phải lời khai sai) |
| `thay_the_cho` r15 | sha256 `41791ab0…3569`, commit `b5336215…` (cha `284a03f`), 21:57:40Z, 1 commit chạm tệp, 2734 dòng | `cay-kho`: `log --diff-filter=A` = `b5336215… 2026-10-07T21:57:40+00:00 284a03fa…`; 1 commit; `git show b533621:<tệp> \| sha256sum` = `41791ab0…`; 2734 dòng | KHỚP |
| `thay_the_cho`: `adg2` có `refs/remotes/origin/claude/spec-wp678-r7` = `b533621…`; REST trả OID 23:49:59Z–23:50:00Z | như trái | `$SP/adg2` chỉ đọc (mtime `.git`/`FETCH_HEAD`/`index` trước = sau): ref = `b5336215…`; `cat-file -t b533621…` = `commit`; `e39b73ed…` chưa có (`FETCH_HEAD` nay 23:53:34Z); REST: không mạng | KHỚP phần `adg2`; REST KHÔNG ĐO ĐƯỢC |
| VERDICT/HINT lượt 15 | `93da81f8…0697` 248 dòng; `90e749bf…0a92` 1 nhóm 4 hunk | `wc -l` 248; `# lop:` 1, `@@` 4; băm khớp | KHỚP |
| bản chiếu `6049075233` | tạo 23:41:23Z, app `claude`, 2594 byte, sha256 `5780c442…`, 0 thực thể, có hai băm và câu tự mô tả | `r16do/c678_since.json` (mtime 23:49:49Z): đúng từng mục | KHỚP |
| header, §8: nền `ab457c6` (REST 23:48:54Z; `adg2` `FETCH_HEAD` 23:30:26Z, `diff --quiet` rc=0 23:48:50Z, `ls-tree` 2 dòng) | như trái | `r16do/rest_master.out` = `ab457c6…`; `r16do/nen_adg2.out`: 23:48:50Z, rc=0, 2 dòng `93cff2f9…`, `7dd06ab6…`, `FETCH_HEAD` 23:30:26Z; `adg2` hiện tại: `origin/master` = `ab457c6`, `diff --quiet` rc=0, cùng 2 blob | KHỚP (giờ REST: chỉ có hiện vật, không đo lại được) |
| §10 (a) áp HINT 15 lên r15 | rc=0 ×2, 4/4 hunk ở 1206, 1227, 1242, 1403, 0 fuzz/offset, 0 `.orig/.rej`; `122f57bf…2ba5`, 2773 dòng | thư mục `mktemp` (đã dọn): đúng từng mục; `= SPEC_moi1.sha256` lượt 15 và `= r16do/r15_sau_hint.md` | KHỚP |
| §10 (b) 8/8 D khớp `bt.sha256` | như trái | `dung_rv15.py` trên `goc_ab.py` (`git hash-object` = `7dd06ab6…`): `sha256sum -c` 8/8 OK | KHỚP |
| A8 *Phiên soạn r16 đo lại*: 23:52:23Z–23:53:26Z rc=0; trả nền 9/9, 0 `.pyc`, L rỗng, `os.name` không lệch; lật 1 ở E8a, D1, D2, D4, D7, 0 ở D3, D5, D6; oracle; `t193` `0/1` ở D6 | như trái | `r16do/chay_d.log`, `r16do/kq16/rv_3.1x.jsonl`: đúng từng ô ở hai bản (oracle ĐỎ D1, D3 hai bản, D4 chỉ 3.12; mù D2, D5, D7, D4@3.11) | KHỚP |
| A8: `ruff --select F` 9 lỗi ở nền và cả tám tệp D | như trái | `ruff` 0.15.8 `--no-cache --isolated`: nền 9; D1, D1d, D2–D7 mỗi tệp 9, delta 0 | KHỚP |
| header, `depends_on`, §8: khối chuỗi lệnh và `s5.py` không đổi byte | giống từng byte r15, OID `c730245c…2694` | `cmp` theo vùng: khối r15 :62–98 ↔ r16 :64–100 rc=0 (37 dòng, 4270 byte, OID `6ccd8418…`); `s5.py` r15 :118–324 ↔ r16 :120–326 rc=0 (207 dòng, 9886 byte, OID `c730245ceea8cc5368d5ef84f8e296cd35102694`) | KHỚP |
| §4 :640 định nghĩa reviewer | phiên soạn r16 đo 23:49:34Z, cùng băm `e225b81c…`, 1175 byte | `sha256sum ~/.claude/agents/review-opus-max.md` = `e225b81c…b792c`, 1175 byte, mtime 2026-09-29 | KHỚP (giờ đo của phiên soạn: KHÔNG ĐO ĐƯỢC) |
| A8 câu H2: *"D1, D2, D4, D7 thoả ba điều kiện đầu, guard bản sao CÓ bị lật"* | như trái | lật 1 ở D1, D2, D4, D7 (`r16do/kq16`, hai bản); D1, D7 `doc_os` [1, 1] (`w/rv16/kq`) | KHỚP |
| A8 *Review lượt 15 đo*: V10 × 20: 3.11 K 20/20, L ∋ `t204` 16/20; 3.12 L 19/20, chết 1/20; tắt vế lật 0/40 chết | như trái | `luot15/do/rv15/kq_v10_20.jsonl`: `quet14b` 3.11 K 20 L 16; 3.12 L 19 chết 1; `quet14b_tat` 0 chết / 40 | KHỚP |
| §9 (4): lặp 5 lượt D1–D5, D7 sạch ở ba bộ quét, hai bản (36/36 ô 5/5) | như trái | `luot15/do/rv15/kq_lap/lap_3.1x.jsonl`: 6 × 3 × 2 = 36 ô, mỗi ô 5/5 sạch | KHỚP |
| §9 (4): `so_kq.py` 69 hàng mỗi bản, lệch đúng hàng V10; A8: *"67 biến thể kia trùng"* | như trái | 69 = nền + 68; 68 − V10 = 67 biến thể (VERDICT lượt 15 dòng 71 viết *"67 hàng còn lại"* — đúng là 67 BIẾN THỂ, 68 hàng kể nền; lỗi chữ của chính tôi ở lượt 15, r16 viết đúng) | KHỚP |
| §9 bảng xếp: lật, K, N, L, oracle từng hàng | xem bảng §9 | `w/do/cong.out` (hiện vật `r15do/kq`, `r16do/kq16`): V1 300 \| 300, V7 0; E8v, E8u, E8e, E8l, E8q 0; E8g 0, E8p 1; D1, D2, D4, D7 1, D3, D5 0; E8w2 K chỉ 3.12; D6 `t193` rc=1 | KHỚP |
| §9: *"Các biến thể ở câu (2)–(5) có `t70`, `t193`, `t204` `1/1` và (S) r13 xanh, và `quet14.py` cũng không bắt, ở hai bản"* | như trái | 14 biến thể × 2 bản: suite 1/1 ×3, S13 0, `quet14` không xếp `t204` vào N, N − D, K, H − D, H2 − D | KHỚP |
| §9: PROTOCOL :1087–1093, :1098–1100; chuỗi tỷ lệ tới 14→15 | như trái | `kho.git show ab457c6:docs/PROTOCOL_DA_PHIEN.md`: :1087 *"Tín hiệu không hội tụ theo lớp"* … :1093; :1098 *"Một lớp xuất hiện ở ba lượt"* … :1100; chuỗi = VERDICT lượt 15 dòng 20 | KHỚP |
## CHI TIẾT TỪNG LỚP

### Lớp `tuong-tac-677-kiem-ke-t70-chua-neu` (P2, CÒN MỞ; lượt 8–16)

**Phần đã đóng (đo lại độc lập).** Mọi thứ r16 nhận từ HINT 15 có mặt và khớp đo: (δ) là nhóm vét, điều kiện thứ tư của câu
H2, vòng đời hàm profile luồng chính, khai V10 làm bộ quét chết; D1–D5, D7 thuộc (δ) (D1, D7 bằng phép thử một biến, D2–D5 đọc
mã); bảng §9 khớp dữ liệu từng hàng; mọi số mới đo lại được khớp.

**F16-1 — luật xếp nhóm không tất định (P2).** Q15 (PROMPT) đếm *"luật xếp không tất định (cùng biến thể, hai người đọc xếp
khác nhau)"* là finding. Bốn chỗ, mỗi chỗ có phép đo:
- (a) **Câu (4) rộng hơn (β)** — đổi QUYẾT ĐỊNH. Chữ (β) ở đoạn giới hạn (:1468–1470): *"guard của bản sao không khớp tên lẫn
  bytecode …, hay không đọc `os.name` của chính module `os` trong khung guard ấy"*. Chữ câu (4) (:1495–1496): *"Có khung guard
  chạy dưới bộ quét lúc hàm profile hoạt động mà không khớp tên lẫn bytecode, hay quyết định `nt` của nó không đọc `os.name`
  của module `os` thật trong khung ấy? Có ⇒ (β)"* — không có *"của bản sao"*. Seam của bộ quét (`lambda t, j, nen=None,
  job=None: cu(t, j, nen=nen or "nt", job=job)`) truyền `nen="nt"`, nên `(nen or os.name) == "nt"` của guard GỐC không bao giờ
  đọc `os.name`: ĐO trên 33 khung guard gốc mỗi bản (`t51` 1, `t199` 12, `t203` 3, G1 13, G1b 3, G3 1) — 0 lần đọc ở cả hai bản;
  đối chứng guard bản sao D1, D7, E8a, G2 mỗi ca 1 khung 1 lần đọc, E8p 1 khung 0 lần đọc (nó đọc ảnh `os` riêng — đúng (β)).
  Theo CHỮ, mọi biến thể có khung guard gốc dưới bộ quét vào (β) ở câu (4): G1, G1b (ĐỌC Ý: ngoài mọi nhóm ⇒ P2) và G3 (ĐỌC Ý:
  (δ)). Hai người đọc, hai nhãn; ở G1, G1b là hai quyết định phân hạng ngược nhau.
- (b) **Câu (5): "một thứ X … phép thử một biến … đổi"** — đổi QUYẾT ĐỊNH. G2 (bản sao như D1, ném lại chỉ khi `__name__ ==
  "__main__"` VÀ `sys.platform == "win32"`): `X_TEN=__main__` ⇒ đạt, `X_PLATFORM=win32` ⇒ đạt, cả hai ⇒ K `BoQuaNen@ban_sao_204`,
  ở 3.11 và 3.12. Theo chữ *"một thứ X"* + *"phép thử một biến"* thì *"không chỉ ra được"* ⇒ ngoài mọi nhóm ⇒ P2; theo tính chất
  (δ) (*"kết cục phụ thuộc … một thứ mà lượt quét giữ KHÁC"*) thì G2 là (δ). Ngược chiều: *"kết cục dưới bộ quét đổi"* không nói
  đổi THÀNH GÌ — đặt `os.name`=`nt` suốt ca (thứ (δ) liệt kê) làm `Path` ném `NotImplementedError` ở MỌI ca dựng `Path` (G1, G2,
  G5, G6, D1, D7, E8a, E8g, E8p; E8g, E8p ở 3.12 là `FileNotFoundError`), làm chính bộ quét chết ở NEN `t51` và D5, và
  `X_TEN=__main__` làm `t199`, G1 ném `AttributeError` (ca dùng `sys.modules[__name__]`) — người đọc nhận *"đổi"* là đủ thì
  tìm được X cho gần như mọi ca, kể cả G1; người đọc đòi đổi có nghĩa thì không.
- (c) **Câu (2) gặp `t125`** — chỉ đổi NHÃN. `t125` (goc :5024) chạy lại TOÀN suite trong hai tiến trình con và đòi transcript đủ
  MỌI tên trong `CA`, nên trên Windows thật mọi ca chạm guard đều có khung guard trong tiến trình con: theo chữ, 13/13 biến thể ở
  hàng (3)–(5) của §9 (E8v, E8u, E8e, E8l, E8q, E8g, E8p, D1–D5, D7) là (γ), không phải (α)/(β)/(δ) như §9 (mỗi biến thể chạm
  một khung guard trên Windows thật — đọc mã; việc ca chạy trong con đo trên D1). ĐO `--chi-ca=t125_` trên D1 (3.12, clone đủ): `t204_moi` chạy
  trong CẢ HAI tiến trình con (`[A] >>> vao t204_moi`, `[B] >>> vao t204_moi`; 202 ca mỗi con). Vô hại cho phân hạng (r16 tự nói *"chồng nhóm vô hại"*) nhưng là *"cùng biến thể, hai người đọc xếp khác"*.
- (d) **Câu (1) "ĐỎ ở MỌI lượt đã đo"** — chỉ đổi NHÃN. G6 (nhánh ngẫu nhiên: helper bản sao trong khung ca, hay trong luồng
  `_thread` thô rồi ném lại lỗi): ma trận một lượt K ở hai bản ⇒ (1); lặp 10 lượt K 6/10 (3.11), 8/10 (3.12) ⇒ (3) (α). Kèm:
  cổng nghiệm thu chạy một lần nên G6 lọt được với xác suất dương.
- Vì sao P2, không P3: (a) và (b) làm chính tiêu chí phân hạng của Q15 ra hai kết luận ngược nhau trên cùng biến thể (*"tiêu chí
  không kiểm được"*, PROMPT §Hạng). Vì sao không P1: lệch nằm giữa luật xếp (công cụ PHÂN HẠNG review) và định nghĩa nhóm, đọc
  được hai cách, không đổi cổng nghiệm thu hay việc executor làm.

**F16-2 — (δ) không thực sự bao hết (P2).**
- Chữ r16: (δ) *"là nhóm VÉT"* (:1476); lập luận đủ (:1477–1480) *"Ngoài (α)–(δ), mọi khung guard … được thấy, nhận ra và đọc
  `os.name` đã lật, còn mọi thứ khác … hai lượt giữ như nhau, nên kết cục dưới bộ quét bằng kết cục trên `nt` (ca vào K hay L vì
  tạo tác thì handoff nêu như đã khai)"*; luật (5) *"không chỉ ra được ⇒ biến thể ngoài mọi nhóm, tức phản chứng của lập luận
  đủ"*; §9 *"(5) ngoài mọi nhóm: không có biến thể nào trong số đã đo"*. §4 :1008: *"Phép quét động ở A8 (vế N − D và vế K)
  bắt cả hai loại"* (gồm ca kết thúc bằng ngoại lệ khác dưới `nt`).
- Biến thể. G1: thêm vào `t199`, ngay trước `chot(not sai, …)` cuối, `if _ly_do_bo_qua_workflow(that, "dang"): sai.append(…)` —
  posix: guard trả `""` ⇒ xanh; Windows thật: không mock, `os.name`=`nt`, workflow thật chỉ Ubuntu ⇒ guard trả lý do (chính
  vế S2 của `t199` khẳng định điều ấy) ⇒ `chot` ném `TinHieuChotCa` ⇒ `main()` ĐỎ. G1b: trong `t203`, chuỗi mong đợi của nhánh
  `nt` `bỏ qua=1` → `bỏ qua=2` (lỗi gõ ở nhánh chỉ Windows đọc) — posix dùng nhánh posix ⇒ xanh; Windows thật: `main()` in
  `bỏ qua=1` ⇒ `chot` ném ⇒ ĐỎ.
- Đo (`w/do/rv16_tom.txt`, hai bản): `t70`, `t193`, ca đích (`t199_`/`t203_`) `1/1`; (S) r13 rc=0; `ruff` delta 0; `quet13`,
  `quet14`, `quet14b` `--chi` ⇒ K `t199:TinHieuChotCa@lease_publish_test` (G1b: thêm H2 − D `t203`) — TRÙNG nền cả tên lẫn
  lớp, nên (q3), (q5) (so TẬP TÊN với nền: K nền = {`t199`, `t203`}, H2 − D nền ∋ `t203`) xanh. Quét ĐỦ (`w/rv16/chay_du16.py`, clone `ab457c6`, chạy từ gốc, nền rồi G1, G1b, MỘT lệnh hai bản; 3.11 580,1 / 514,1 /
  537,8 s, 3.12 689,4 / 648,6 / 640,6 s): cả ba cùng 201 ca = 187 đạt + N 12 + K {`t199`, `t203`} + H − D {`t193`} + H2 − D {`t71`,
  `t72`, `t73`, `t98`, `t193`, `t203`}, L rỗng, `os.name` không lệch, status 0, 0 `.pyc`; (q1) N = sổ; (q2)–(q5) như nền ⇒ ĐẠT. Oracle
  ĐỎ ở cả nền lẫn biến thể (nó lật `os.name` trong khung guard cả khi `t199` tự mock `posix`) ⇒ không phân biệt; Windows thật
  KHÔNG ĐO ĐƯỢC — ĐỎ là đọc mã.
- Vì sao không có X: kết cục dưới bộ quét (K `TinHieuChotCa`) đã BẰNG kết cục trên Windows (ĐỎ `TinHieuChotCa`) — không có chênh
  nào để một X giải thích. Mọi phép thử một biến (`X_KHONG_SEAM`, `X_TEN`, `X_PLATFORM`, cả hai, `X_OS_NT_CA`) để nguyên K
  `TinHieuChotCa` hoặc đổi THOÁI HOÁ đúng như trên nền `t199`, `t203` (`AttributeError`, `NotImplementedError`). (α) không: mọi
  khung guard trên luồng chính, trong khung ca, profile hoạt động (12–13 lần lật). (γ) không: ca không tạo tiến trình con (trừ
  cách đọc chữ câu (2), F16-1 (c)). (β) không theo định nghĩa (không có bản sao); có theo CHỮ câu (4) — chính F16-1 (a).
- Hệ quả: lập luận đủ đúng chữ (*"kết cục bằng"*) mà không đủ cho điều nó được dùng để kết luận (*"không lọt"*): giữa hai điều
  ấy còn chữ (q1)–(q5), so TẬP TÊN với nền. Người làm đúng chữ r16 tin G1, G1b bị bắt (§4 nói vế K bắt; (δ) nói vét; §9 nói không
  có biến thể ngoài mọi nhóm) ⇒ đủ hai điều kiện P2 của nguyên tắc chống chạy đua; theo Q15 đây đúng là ví dụ thứ ba *"(δ) không
  thực sự bao hết (có biến thể lọt mà không chỉ ra được X)"*.
- Phạm vi: (q3) so tên có từ r11–r12, nhưng lời khai VÉT, lập luận đủ, luật (5) và hàng §9 là chữ MỚI của r16 — và lập luận đủ
  ấy đến từ HINT lượt 15 của chính tôi, bỏ sót bước *"cổng đọc kết cục"*. G1b không cần cố ý: một lỗi gõ ở nhánh `nt` là đủ.
- Phương án (HINT A, B, E): không thêm nhóm thứ năm; biến lỗ thành NGHĨA VỤ có kiểm: handoff liệt kê mọi ca của nền thuộc K,
  H − D, H2 − D của nền (trên `ab457c6`: `t71`, `t72`, `t73`, `t98`, `t193`, `t199`, `t203`) mà thân ca hay hàm cấp module nó
  tham chiếu (đóng bao) khác nền (so `ast.dump`), không tự tính là đạt — cùng cách r16 đã xử lý ca MỚI vào K vì tạo tác; luật
  xếp câu (1) đọc nghĩa vụ ấy như cổng chưa đạt. Giới hạn của phương án: đóng bao theo tên tĩnh, không theo lời gọi động.

## DRY-RUN HINT.patch

Tệp `$R/goi/HINT.patch`: 1 nhóm (`# lop: tuong-tac-677-kiem-ke-t70-chua-neu` ngay trước `--- `), 5 hunk, một tệp đích
`ops/specs/lease-id-ep-kieu-yaml-r16.md` (repo-relative, không tiền tố), 0 dấu chéo ngược. Dựng bằng `w/hint/mk_hint16.py` (thay
chuỗi nguyên văn, mỗi chuỗi cũ `assert` đúng 1 lần; `diff -u --label`); kiểm bằng `w/hint/kiem_hint16.sh` — đúng lệnh PROMPT
trên bản sao `mktemp -d -p "$R"` + `cp -a "$R/cay-kho"` (không đụng `cay-kho`), rồi áp thật trên CHÍNH bản sao ấy, so băm với
bản dựng độc lập `w/hint/SPEC_moi.md`, kiểm khối lệnh và `s5.py`, dọn bản sao (chạy SAU khi hai clone quét đủ đã tự xoá; `$R`
355 MB trước và sau). Output nguyên văn (`w/hint/kiem_hint16.out`, đường `$R` thay chữ):

```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```

```
HINT.patch: 16660 byte, sha256 21bff7d5f26c318efa5d9147658a49b04d94af9dd71ac1eb7a19a89f7b12d057
nhóm (# lop:): 1, hunk (@@): 5, dấu chéo ngược: 0
bản sao: $R/tmp.3kTqIgr7VO/cay HEAD e39b73ed6f054178211c228e7d886eb9ed981f43 status 0 dòng
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: tuong-tac-677-kiem-ke-t70-chua-neu
|--- ops/specs/lease-id-ep-kieu-yaml-r16.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r16.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r16.md
Using Plan A...
Hunk #1 succeeded at 1272.
Hunk #2 succeeded at 1467.
Hunk #3 succeeded at 1498.
Hunk #4 succeeded at 1511.
Hunk #5 succeeded at 2309.
done
dry-run rc=0
áp thật rc=0
succeeded: 5
offset|fuzz|FAILED: 0
sha256 sau áp: 95e0a776d0da3faa2d047ffd5980d6127e6237dce2d5423a3db2da949583a05a 2926 dòng
sha256 SPEC_moi: 95e0a776d0da3faa2d047ffd5980d6127e6237dce2d5423a3db2da949583a05a
git status sau áp:  M ops/specs/lease-id-ep-kieu-yaml-r16.md;
.orig/.rej: 0
khoi :64–100 6ccd8418884a7fbf4e56311d2ca2d2ff5b3e7250
s5 :120–326 c730245ceea8cc5368d5ef84f8e296cd35102694
đã dọn bản sao
```

Đọc kết quả: dry-run rc=0, 5 dòng `succeeded`, 0 `FAILED`, 0 fuzz, 0 offset; áp thật rc=0; sha256 sau áp BẰNG bản dựng độc lập
(`95e0a776…a05a`, 2926 dòng); đúng một tệp đổi; 0 `.orig`/`.rej`; khối chuỗi lệnh giữ OID `6ccd8418…`, `s5.py` giữ
`c730245c…2694` ⇒ điều kiện cấp không đổi. HINT chỉ sửa chữ A8 (dụng cụ đo và nghĩa vụ handoff của executor ở scratch, luật
xếp, đoạn đo) và một bảng §9; không đụng write set, closure hay năm điều kiện cấp.

## LƯU Ý CHO PHIÊN ĐIỀU PHỐI (không phải finding)

1. **Danh tính.** Claude Opus 5.5 (`claude-opus-5-5`), effort max, subagent; model/effort đang phục vụ KHÔNG ĐO ĐƯỢC. Lượt này
   KHÔNG sạch nên điều kiện cấp (3) vẫn chưa thoả.
2. **§12.** 15→16 = 0/1 theo lớp (1/2 theo finding). Cùng 14→15 = 0/1 ⇒ HAI chuyển tiếp liền nhau dưới 50%: PROTOCOL `ab457c6`
   :1091–1093 *"thì dừng vòng vá và đưa bằng chứng tới Review Rescue Checkpoint"*. Q15 dòng 12 nói Q13 (lặp không trần) chỉ còn
   áp cho các lớp KHÁC, tức lớp này không còn được Q13 che: dừng hay tiếp là việc của chủ kho tại checkpoint, không phải của
   reviewer. Luật *"một lớp ở ba lượt"* (:1098–1100) áp với `tuong-tac-677-…` ở chín lượt (8–16).
3. **Hội tụ.** Hình dạng lặp vẫn là *"lời khai rộng hơn phép đo"*, nay ở tầng LUẬT XẾP và lập luận đủ, không ở một cách viết ca.
   HINT không thêm nhóm thứ năm: F16-2 thành NGHĨA VỤ handoff có kiểm (ca của nền thuộc K, H − D, H2 − D bị đổi, như r16 đã làm
   với ca MỚI vào K), F16-1 thành câu hỏi trả lời bằng đọc mã (không theo số lượt), X là tập, phép thử đòi BẰNG kết cục
   Windows. Sau r17, chỗ còn hỏi được ở lớp này: phép đóng bao của nghĩa vụ handoff có đủ không, và còn đường lọt nào mà kết cục
   dưới bộ quét BẰNG kết cục Windows ngoài các tập so theo tên. Tôi đã thử đường (q1) (so cặp đã `resolve`, yếu hơn bước dẫn xuất lý do
   của `main()`): G7 lọt bộ quét nhưng `t193` M3 (chạy chính `main()` cho mọi ca trong sổ) ĐỎ ở hai bản ⇒ bị bắt. Đường (q2)
   N − D tôi chỉ suy luận (ca ném `BoQuaNen` của module mà không trong D thì vào N − D), không dựng ca. Đó là thử một đường, không
   phải chứng minh hết đường.
4. **Oracle.** `mo_phong_nt14.py` lật `os.name` trong khung guard kể cả khi ca tự `mock.patch.object(os, "name", "posix")`, nên
   nó ĐỎ ở `t199`, `t203` NỀN — không phân biệt tạo tác với lỗi thật (G1, G1b). Không trong HINT.
5. **Đọc ngoài `$R` (CHỈ ĐỌC).** `$SP/cr678-r13`, `$SP/cr678-r14` (dụng cụ, biến thể), `$SP/cr678-r15/r15do` (`kq`, ba thư mục
   biến thể), `$SP/adg2` (`GIT_OPTIONAL_LOCKS=0`; mtime `.git`, `FETCH_HEAD`, `index` trước = sau). Không ghi vào đó.

## GIỚI HẠN VÀ TOÀN VẸN

- **Không mạng.** Mọi câu REST của r16 (23:48:54Z, 23:49:01Z–23:49:29Z, 23:49:48Z–23:49:49Z, 23:49:59Z–23:50:00Z): KHÔNG ĐO ĐƯỢC
  ngoài hiện vật `r16do/*` và mtime của chúng.
- **Windows thật KHÔNG ĐO ĐƯỢC.** G1, G1b ĐỎ trên Windows là ĐỌC MÃ (G1 dựa đúng điều vế S2 của `t199` khẳng định; G1b dựa chuỗi
  tổng kết của `main()`); oracle không phân biệt (mục 4). G5 ĐỎ trên Windows là ngữ nghĩa `open()` của CPython trên Windows (không
  chia sẻ quyền xoá) — đọc tài liệu, không đo.
- **Biến thể của tôi là ca DỰNG để đo**; G1b là dạng lỗi gõ có thể xảy ra thật; G1, G2–G7 cố ý.
- **Phép thử một biến của tôi đặt thứ ấy cho CẢ ca** (`quet14b_x.py`), không tại chỗ đọc; chính giới hạn này làm lộ đổi THOÁI
  HOÁ ở F16-1 (b) — một người đặt tại chỗ đọc sẽ không thấy chúng, và đó là lý do chữ (5) phải nói rõ.
- **Sự cố dụng cụ (đã sửa trước khi kết luận).** G6 bản 1 sai (HƯỚNG 16). Một `assert` sai logic trong `mk_hint16.py` làm bộ
  dựng dừng ở lần chạy đầu, sửa rồi chạy lại. Một lệnh chờ `sleep 240` vượt hạn 120 s bị chuyển nền, vô hại.
- **Tài nguyên.** `$R` cao nhất ~0,6 GB (hai clone quét đủ; sau đó bản sao `cay-kho` của dry-run); clone tự xoá; mọi thư mục tạm
  dọn bằng `shutil.rmtree`; cuối lượt `$R` 285 MB.
- **Ràng buộc đã giữ.** Không đăng GitHub, không commit/push, không in biến môi trường hay bí mật; `python3 -B` cho mọi script;
  không `pkill -f`; không sửa `$R/cay-kho` (mọi `patch` trên bản sao `cp -a`).
