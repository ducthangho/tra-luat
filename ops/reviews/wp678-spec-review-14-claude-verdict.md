verdict: changes_requested
reviewed_sha: 284a03fa6eff0356a79cca2926b889a6a98896f0
spec_sha256: ec4d97f5488cc5da27a97daec9b617428e42774139fa632fe6008b315e59b0ed
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Chạy như subagent do phiên điều phối giao. Model/effort là CẤU HÌNH được giao, không phải runtime evidence. Chỉ dẫn hệ thống tôi nhận trùng NGUYÊN VĂN 7 dòng thân `~/.claude/agents/review-opus-max.md` (sha256 `e225b81c…b792c`) — CÓ dấu hiệu lượt này dựng từ định nghĩa ấy; model/effort đang phục vụ: KHÔNG ĐO ĐƯỢC. Không mạng, không đăng GitHub, không commit/push, không sửa `$R/cay-kho`; chỉ ghi dưới `$R/goi/` và thư mục `mktemp -d -p "$R"` (`$R/w14.Xjll`).

Kết luận nội dung: **0 P1 / 1 P2 / 0 P3** (theo lớp).
- **P2 `tuong-tac-677-kiem-ke-t70-chua-neu` — CÒN MỞ** (lượt 8–14). Phần r14 nhận từ HINT 13 có răng và tái lập được từng số (chạy lại `chay14.py` nguyên byte: 52/52 hàng × 2 bản và 4 lượt quét đủ, 0 lệch). Hai biểu hiện mới: **F14-1** (VÁ HỜ) — r14 thay câu bao theo tính chất của HINT 13 bằng danh sách giới hạn theo API, và E8n/E8n2 (bản sao chạy trong luồng `threading` khởi động LÚC NẠP module) lọt mọi cổng kể cả vế lật ở cả hai bản (5/5), oracle ĐỎ, không có trong danh sách; câu H2 còn khai mọi bản sao *"vào K nhờ vế lật"*. **F14-2** (VÁ SINH LỖI MỚI) — vế lật đổi `os.name` TOÀN TIẾN TRÌNH và *"trả giá trị lúc vào khung"*: ca HỢP LỆ chạy guard hay `pathlib` song song bị báo vào K (V6 cả hai bản; V1 3.11), `os.name` kẹt `nt` (V1, cả hai bản), và một ca như thế đặt đầu `CA` kéo 9 ca nền chạy sau nó vào K ⇒ (q3) ĐỎ oan. HINT nhóm 1 (4 hunk, A8): cài `threading.setprofile` trước khi nạp, đếm độ sâu + trả gốc sau mỗi ca, khai tạo tác toàn tiến trình, giới hạn THEO TÍNH CHẤT (α/β/γ) để biến thể mới rơi vào "trong giới hạn đã khai". Đo: bộ quét đề xuất khác `quet14` đúng ba hàng trên 60 biến thể × 2 bản (bắt E8n, E8n2; hết báo nhầm V1), quét đủ nền giống hệt.
- **`chinh-xac-hoa-so-hieu-va-tham-chieu` (P3 lượt 12–13) — ĐÃ VÁ THẬT.** Ba câu HINT nhóm 2 vào r14 nguyên văn và đúng khi đo ĐỘC LẬP trên `adg2`; bốn chỗ phiên soạn tự sửa đúng; mọi số MỚI của r14 đo lại khớp.
- **Không có P1:** khối chuỗi lệnh và `s5.py` giống byte r13; các hàng bảng, closure, năm điều kiện cấp không đổi ngoài số revision; A1–A7 không đòi ca đa luồng nên F14-2 khó tự xảy ra với executor làm đúng chữ.

Tỷ lệ vá thật 13→14 (§12, chỉ báo): U = 2 lớp, F = 1 ⇒ **1/2 = 50%**; theo finding 3/4. Chuỗi: 7→8 0/5, 8→9 2/7, 9→10 1/4 (2/4), 10→11 2/4, 11→12 0/2, 12→13 1/3, 13→14 1/2.


## KIỂM ĐẦU VÀO

```
$ sha256sum $R/SPEC.md $R/SPEC-r13.md
ec4d97f5488cc5da27a97daec9b617428e42774139fa632fe6008b315e59b0ed  SPEC.md       # khớp PROMPT
711b7b74e55ee14bb666b467abdc92d9aab5e4ddc5f97cbb68753241d03e4bb1  SPEC-r13.md   # khớp PROMPT
$ git -C $R/cay-kho rev-parse HEAD
284a03fa6eff0356a79cca2926b889a6a98896f0                                       # khớp reviewed_sha
$ git -C $R/cay-kho config core.abbrev
7
$ sha256sum $R/PROMPT.md
52b6f271bed3f1e71b87f93b0c077915ea50397ee5cbe7fefa2e4e9bcb4829e2
```

## NHẬT KÝ TĂNG DẦN

Đường `rv/`, `anh/`, `hint/`, `tai_lap/`, `kq_tai/` là tương đối `$R/goi/do/` (hiện vật chép từ thư mục tạm; `README_do.txt` mô tả cách tái lập).

- 15:4xZ Diff theo từ r13→r14 (`tai_lap/wdiff2.py`, `difflib` theo dòng rồi theo từ): 29 vùng đổi theo dòng (`r13-r14.diff` có 17 hunk), khớp danh sách chỗ đổi trong PROMPT (đầu tệp, bảng chỗ đổi, `thay_the_cho`, `nguon_cap_viec`, `depends_on`, nền nghiệm thu, §2, §3, §4, A8, §8, §9, §10).
- 15:4xZ Dựng bản sao trung thực cây công cụ phiên soạn r14 (thư mục tạm `$R/w14.Xjll/sp/`, dựng lại theo `README_do.txt`): `chay14.py`, `quet14.py`, `mo_phong_nt14.py`, `dung_e8_14.py` chép nguyên byte từ `$R/r14do/p2`; phụ thuộc `cr678-r13/r13do/l2b/{goc_ab.py,nen,quet13.py,s13.py,bt}` ĐỌC từ `$SP/cr678-r13` (ngoài `$R`, chỉ đọc, chép vào thư mục tạm); `adg2` thay bằng symlink tới `$R/kho.git` (cùng cây `ab457c6`). Kiểm: `goc_ab.py` hash-object = `7dd06ab6…a081`; cây `nen` 233/233 tệp cùng OID với `ab457c6`, 0 lệch, 0 vắng; `quet14.py` − `quet13.py` = đúng vế lật + K ghi `lớp@module` + `q1_chi` (diff); E8h–E8m dựng lại bằng `dung_e8_14.py` khớp từng byte `$R/r14do/p2/bt14` (6/6); E8a–E8g của lượt 13 khớp byte giữa `$R/luot13/do/e8` và `$SP/cr678-r13/goi/do/e8` (7/7).
- 15:5xZ Chạy lại `chay14.py` NGUYÊN BYTE (pha A 52 hàng × 2 bản, pha B quét đủ nền `quet13` rồi `quet14` × 2 bản; tối đa 2 lượt quét nặng song song).
- 15:5xZ Phạm vi: trích khối chuỗi lệnh (dòng 63–99, 37 dòng) và `s5.py` (dòng 119–325, 207 dòng) từ CẢ r13 lẫn r14 rồi `cmp` ⇒ rc=0 cả hai; `git hash-object` `s5.py` r14 = `c730245ceea8cc5368d5ef84f8e296cd35102694`, sha256 `708790485694…02f6`, 0 dấu chéo ngược. Vùng 100–118 khác r13 đúng một dòng (114, OID `…2e01`); vùng 326–542 khác đúng chỗ HINT nhóm 2.
- 15:5xZ Áp `luot13/HINT.patch` lên bản chép r13: dry-run rc=0, áp rc=0, 4 dòng `succeeded`, 0 `offset`/`fuzz`; sha256 sau áp `38eeafbf…8758` = `luot13/do/hint/SPEC_all.md`, 2556 dòng. So bản ấy với r14 (`wdiff2.py`): HINT nhóm 2 vào r14 NGUYÊN VĂN; nhóm 1 vào r14 kèm ba sửa của phiên soạn (vế E8h trong câu H2; đoạn *Phiên soạn r14 đo lại vế lật*; đoạn giới hạn viết lại — bỏ câu bao "bản sao guard mà vế ấy không nhận ra hay không tới được" và chú "E8e: luồng ngoài profile", thay bằng danh sách bốn mục theo API).
- 15:56Z Đọc `$SP/adg2` (CHỈ ĐỌC, `GIT_OPTIONAL_LOCKS=0`; mtime `.git` trước/sau không đổi, `find -newer` rỗng): `origin/master` = `ab457c6`, `diff --quiet ab457c6 refs/remotes/origin/master -- <hai tệp>` rc=0, `ls-tree` 2 dòng (blob `93cff2f…`, `7dd06ab…`), `cat-file -t 35e7f9c…` rc=128, `FETCH_HEAD` mtime 15:16:38.706Z (475 dòng = 1 master + 474 `not-for-merge`).
- 15:56Z Chạy lại `do_anh_r13.py` (từ gốc `adg2`, `-B -I`, ghi JSON vào thư mục tạm): JSON giống hệt `r14do/p3/anh_r13.json` (20/20 khoá). Đếm ĐỘC LẬP bằng mã của tôi (`anh/dem_doc_lap.py`: liệt kê theo pathspec `ops/leases`, hạn tự so với mốc 12:18:00Z): 473 ref, 589 cặp, 37081 mục `100644 blob`, `write_set` 1384 + 23 prefix, `effective_write_set` 123 mục ở 23 cặp có khoá = 21 danh sách + 2 `null`, 59 cặp thiếu cả hai khoá (59 hết hạn) = 39 `scope_files` + 6 `scope_files_can_xet` + 6 `delta_scope_files` + 8 không trường, 6 cặp còn hạn (wp685 ×5, wp710 ×1) — khớp mọi số r14 khai.
- 15:57Z Chạy lại `ten_tep_11.py` (bản chép, `-B -I`): đầu ra giống hệt `ten_tep_11.out` (rc=11 ở 9, rc=12 ở LF, rc=1 ở không-UTF-8). Chạy lại `kiem_so_r13.py` với MỘT thay đổi (thư mục GHI tạm `D` trỏ vào thư mục tạm của tôi; mọi đường đọc giữ nguyên): đầu ra giống hệt `kiem_so_r13.out` (75 phép so: 72 KHỚP, 3 LỆCH = H1, G1, G2; G2 gồm hai tọa độ ⇒ bốn chỗ sửa).
- 15:53Z–15:54Z Pha A chạy lại nguyên byte: 52/52 hàng × 2 bản, so từng hàng với `r14do/p2/kq/ma_tran_3.1x.jsonl` (sha biến thể, `t70`/`t193`/`t204`, S13, rc oracle, trả nền, `.pyc`, và N, K, N − D, H − D, H2 − D, `q1_chi`, `so_ca`, `dat` của cả `quet13` lẫn `quet14`): **0 hàng lệch** ở cả hai bản.
- 15:54Z–16:05Z Biến thể của tôi (`rv/dung_rv14.py`, cùng mẫu `dung_e8_14.py`; bộ chạy `rv/chay_rv.py` chép logic từng hàng của `chay14.pha_a`): E8n, E8n2, E8q, E8w, E8w2 (họ E8) và V1, V6, V7 (hợp lệ). Lặp `quet14 --chi t204` 5 lần mỗi biến thể × 2 bản. Kịch bản lan: V1 đặt ĐẦU `CA` (`t000_…`), quét `--chi t000,t01_,t02,t03,t04,t05`.
- 16:10Z–16:17Z Đề xuất của tôi `rv/quet14b.py` = `quet14.py` + ĐÚNG ba thay đổi: (a) `threading.setprofile` cài TRƯỚC khi nạp module (hàm profile chưa làm gì tới lúc nạp xong); (b) lật theo bộ đếm độ sâu toàn tiến trình có khoá (khung guard đầu tiên vào thì lưu gốc, khung cuối cùng ra thì trả gốc); (c) sau MỖI ca còn khung mở hay `os.name` khác gốc thì ghi ca vào L và trả gốc. `rv/chay_b.py`: `quet14` và `quet14b` trong MỘT lệnh, cùng cây, trên NỀN + 38 cũ + 13 E8 + 8 biến thể của tôi + kịch bản V1-đầu-`CA`, 3.11 ‖ 3.12.
- 16:19Z E8p (bản sao nhập `os` qua `__import__` riêng, đọc ảnh `os.name` chụp lúc dựng) qua `rv/chay_rv.py`.
- 16:18Z bắt đầu quét ĐỦ nền cho đề xuất (`rv/chay_du_b.py`: clone đầy đủ từ `$R/kho.git`, `checkout --detach ab457c6`, `core.abbrev 7`; `quet14` rồi `quet14b` trên CÙNG clone; MỘT lệnh mỗi bản; tối đa 2 lượt nặng cùng lúc).
- 16:18:22Z–16:52:24Z Quét ĐỦ nền cho đề xuất (`rv/chay_du_b.py`, MỘT lệnh mỗi bản, `quet14` rồi `quet14b` trên cùng clone đầy đủ từ `$R/kho.git`): 3.11 `quet14` 16:18:22Z–16:29:58Z (695,1 s), `quet14b` 16:29:58Z–16:43:08Z (788,1 s); 3.12 `quet14` 16:23:21Z–16:39:39Z (977,0 s), `quet14b` 16:39:40Z–16:52:24Z (762,9 s); cả bốn lượt cùng mọi tập (BẢNG ĐO, dòng cuối).
- 16:33:32Z–16:39:25Z `rv/lap5.sh` (hiện vật bền của phép lặp 5 lần): E8n, E8n2 `K0/lat0` ×5 ở cả hai bản; V1 3.11 `K=t204:NotImplementedError@builtins/lat300/OSLECH` ×5, 3.12 `K0/lat300/OSLECH` ×5; V6 `K=t204:TinHieuChotCa@lease_publish_test/lat150` ×5 ở cả hai bản; 0 `.pyc`.
- 16:52Z–16:54Z HINT dựng bằng `hint/mk_hint14.py` (thay theo số dòng, `assert` nội dung đầu/cuối; số quét đủ điền từ `hint/so_du.py` có `assert` từng tập), kiểm bằng `hint/kiem_hint.sh` (DRY-RUN dưới). Hiện vật chép vào `$R/goi/do/` (`README_do.txt` mô tả cách tái lập; đường `rv/`, `anh/`, `hint/`, `tai_lap/`, `kq_tai/` dưới đây là tương đối `goi/do/`).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 13 (Claude Opus 5.5 max, trên `35e7f9c`; VERDICT `372efdfe…c244` 233 dòng, HINT `c4f73b98…41ce` 2 nhóm/4 hunk — băm đo lại khớp): 0 P1 / 1 P2 / 1 P3. Nhãn finding theo PROTOCOL §8 (`ab457c6` :679–680: `ĐÃ VÁ THẬT` · `VÁ HỜ` · `VÁ SINH LỖI MỚI` · `CHƯA VÁ`); nhãn lớp theo §8.3 (:799–802: chỉ `ĐÃ VÁ THẬT` khi mọi biểu hiện trong phạm vi đã đóng và không còn biểu hiện cùng cơ chế do bản vá sinh ra). Mọi bằng chứng dưới đây tôi tự đo.

| lớp (lượt 13) | finding lượt 13 | nhãn finding trên r14 | nhãn LỚP lượt 14 | bằng chứng tự đo |
|---|---|---|---|---|
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P2) | F13-1 họ E8: lời khai *"Còn lại … E5f"* và *"H2 thấy cả BẢN SAO"* rộng hơn phép đo | **VÁ SINH LỖI MỚI** (kèm phần VÁ HỜ) | **CÒN MỞ** (lượt 8–14) | Phần đã đóng: chạy lại `chay14.py` nguyên byte ⇒ 52/52 hàng × 2 bản trùng hiện vật phiên soạn; E8a/c/d/f/i/j/k/m vào K, E8b/E8h vào N, E8e/E8g/E8l lọt đúng như khai, nền + 38 cũ cùng tập ở hai bộ quét, năm ca hợp lệ không báo nhầm. Phần VÁ HỜ (F14-1): E8n, E8n2 — bản sao chạy trong luồng `threading` khởi động LÚC NẠP module — lọt mọi cổng kể cả vế lật ở cả hai bản (5/5), oracle ĐỎ; không nằm trong danh sách giới hạn r14, trong khi r14 bỏ câu bao theo tính chất của HINT 13. Phần SINH LỖI MỚI (F14-2): vế lật (HINT 13 → r14) lật `os.name` TOÀN TIẾN TRÌNH và "trả giá trị lúc vào khung": ca HỢP LỆ V6 vào K ở cả hai bản (5/5); V1 vào K ở 3.11 và để `os.name` kẹt `nt` ở cả hai bản (5/5); V1 đặt đầu `CA` kéo 9 ca nền chạy sau nó vào K (`quet14` 1/12 đạt, `quet13` 10/12). `quet13` (r13, không lật) không báo nhầm ở cả ba |
| `chinh-xac-hoa-so-hieu-va-tham-chieu` (P3) | (a) "123 mục ở 23 lease (thêm 2 null)" | **ĐÃ VÁ THẬT** | **ĐÃ VÁ THẬT** | r14 :439–442 = HINT nhóm 2 nguyên văn; đếm độc lập trên `adg2`: 123 mục ở 21 cặp + 2 cặp `null` = 23 cặp có khoá, 0 danh sách rỗng |
| | (b) "59 cặp … khai `scope_files`" | **ĐÃ VÁ THẬT** | | đếm độc lập: 39 / 6 / 6 / 8, cả 59 hết hạn ở mốc 12:18:00Z |
| | (c) "mười một dạng … rc=11 ở …" kể 9 | **ĐÃ VÁ THẬT** | | r14 :508–509 kể đủ chín dạng; `ten_tep_11.py` chạy lại: rc=11 ×9, rc=12 LF, rc=1 không-UTF-8 |
| | bốn chỗ ngoài HINT do phiên soạn r14 tự tìm | **ĐÃ VÁ THẬT** | | OID `s5.py` r12 = `2f6bde6c90098dd0781252984c5ede31efb62e01` (trích từ r12 :114–225, 112 dòng) ⇒ `…2e01` ở :20, :114, :2300, không còn `…1e01` ngoài câu mô tả việc sửa; `_ls_tree_z` :1977, `_quet_lease_toan_kho` :641–701 (AST `lineno`/`end_lineno` trên blob `93cff2f`); §2: lệnh hai mẫu của r12 ra 19, riêng `"lease_id"` ra 16 (trên cả `ab457c6` lẫn `1741e0a`) |

Lớp đã đóng ở lượt 13 — `thu-tu-677-bo-ngo-o-dieu-kien-cap`: KHÔNG tái phát (khối chuỗi lệnh và `s5.py` giống byte r13, `cmp` rc=0). Lớp lượt 7–11: KHÔNG tái phát (hàng `objective`, `review_class`, `risk`, `executor`, `environment`, `reviewer` và các hàng closure không nằm trong 26 vùng khác giữa r13+HINT13 và r14).

**Tỷ lệ vá thật 13→14 (§12 :1087–1093 trên `ab457c6`, chỉ báo).** U = 2 lớp mở cuối lượt 13 (`tuong-tac-677-…`, `chinh-xac-hoa-…`); F = {`chinh-xac-hoa-so-hieu-va-tham-chieu`} ⇒ **1/2 = 50%** (không < 50%). Theo finding: lượt 13 có 4 finding (F13-1; P3 a, b, c) ⇒ ĐÃ VÁ THẬT **3/4** (bốn chỗ P3 mà phiên soạn r14 tự tìm thêm không phải finding của lượt 13, không tính vào tử hay mẫu). Chuỗi: 6→7 N/A, 7→8 0/5, 8→9 2/7, 9→10 1/4 (2/4), 10→11 2/4, 11→12 0/2, 12→13 1/3, **13→14 1/2**. Chuyển tiếp 13→14 không dưới 50% nên không tạo cặp "hai chuyển tiếp liền nhau < 50%" mới; luật một lớp ở ba lượt (:1098–1100) vẫn áp cho `tuong-tac-677-…` (lượt 8–14, bảy lượt). Lớp MỚI ở lượt 14 (ngoài U): không — F14-1, F14-2 cùng đơn vị nghĩa (phép quét động của A8 đo đúng thứ nó khai hay không) nên nối slug cũ theo §8.3, không đổi khoá.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `tuong-tac-677-kiem-ke-t70-chua-neu` | **P2** (CÒN MỞ; lượt 8–14) | **F14-1** (VÁ HỜ của F13-1): danh sách giới hạn r14 (A8 :1337–1343) liệt kê THEO API (*"luồng `_thread` thô"*, *"`sys.setprofile(None)`"*) sau khi bỏ câu bao theo tính chất của HINT 13; E8n/E8n2 — bản sao chạy trong luồng `threading` khởi động LÚC NẠP module — lọt mọi cổng kể cả vế lật ở cả hai bản (5/5), oracle ĐỎ; người đọc đúng chữ tin luồng `threading` được phủ (A8 nêu `threading.setprofile`, E8m vào K). Câu H2 (:1216–1218) còn khai *"ca ấy vào K … nhờ vế lật"* cho MỌI bản sao ở module nạp lại, trái chính đoạn giới hạn. **F14-2** (VÁ SINH LỖI MỚI): vế lật đổi `os.name` TOÀN TIẾN TRÌNH và *"trả giá trị lúc vào khung"*; ca HỢP LỆ chạy guard hay `pathlib` song song vào K (V6 ở cả hai bản; V1 ở 3.11), `os.name` kẹt `nt` sau ca (V1, cả hai bản), và kéo mọi ca chạy sau vào K (V1 đầu `CA`: `quet14` 1/12 đạt so với `quet13` 10/12) ⇒ (q3) ĐỎ oan, không có lối khai nào trong chữ r14 | HINT nhóm 1 (4 hunk, A8): (1) cài `threading.setprofile` TRƯỚC khi nạp; lật theo bộ đếm độ sâu toàn tiến trình có khoá, trả giá trị GỐC khi khung guard cuối cùng ra; sau mỗi ca trả gốc và ghi ca vào L; (2) câu H2 thêm điều kiện cần (khung guard chạy dưới hàm profile, khớp tên hay bytecode, đọc `os.name` của module `os` thật); (3) khai tạo tác toàn tiến trình (V6) và L như tạo tác của seam: handoff nêu, không tự tính là đạt; (4) đoạn *Review lượt 14 đo* + giới hạn THEO TÍNH CHẤT (α) không chạy dưới hàm profile, (β) không khớp tên/bytecode hay không đọc `os` thật, (γ) tiến trình con — biến thể mới rơi vào một nhóm là trong giới hạn đã khai | `rv/chay_b.py` (MỘT lệnh, cùng cây, `quet14` ‖ `quet14b`, 60 biến thể × 2 bản): khác ĐÚNG ba hàng (E8n, E8n2 vào K `BoQuaNen@ban_sao_204`; V1 đạt, không lệch `os.name`), V1-đầu-`CA` 10/12 đạt K 2 như `quet13`; quét đủ nền: xem BẢNG ĐO. Giới hạn của phương án: V6 vẫn vào K (tạo tác toàn tiến trình, chỉ KHAI được, không khử được khi còn lật `os.name`); E8e, E8l, E8q, E8g, E8p, E5f vẫn lọt (nay nằm trong nhóm tính chất); Windows thật KHÔNG ĐO ĐƯỢC (oracle là mô phỏng, và cũng lật toàn tiến trình) |
| `chinh-xac-hoa-so-hieu-va-tham-chieu` | (P3 ở lượt 12–13) **ĐÃ VÁ THẬT** ở lượt 14 | — | — | ba câu HINT nhóm 2 vào r14 nguyên văn và đúng khi đo độc lập trên `adg2`; bốn chỗ phiên soạn tự sửa đúng; mọi số MỚI của r14 đo lại khớp (BẢNG ĐO) |

Hạng: **0 P1 / 1 P2 / 0 P3** (theo lớp). Vì sao F14-2 không là P1: A1–A7 không đòi ca đa luồng nào (`grep` A1–A7: 0 chỗ *luồng/thread/song song*), nên executor làm đúng chữ r14 khó tự vấp; nhưng tiêu chí (q3) báo oan cho một lớp ca hợp lệ và chữ r14 (*"đúng trong khung"*, *"trả giá trị lúc vào khung"*) khai chính xác hơn cơ chế ⇒ P2. Vì sao câu H2 không là P1 (*"r14 tự mâu thuẫn"*): đó là câu MÔ TẢ, không tiêu chí (q1)–(q5) nào đọc nó, và chính câu ấy trỏ tới đoạn giới hạn cụ thể hơn; xếp chung F14-1.

## BẢNG SĂN

Mẫu: `HƯỚNG n: tên / giả thuyết / lệnh / output / kết luận`.

- HƯỚNG 1: phạm vi r13→r14 / khối chuỗi lệnh và `s5.py` khai không đổi byte / trích theo vùng rồi `cmp` (NHẬT KÝ) / rc=0 cả hai; OID `c730245c…2694` / KHÔNG PHẢI LỖI.
- HƯỚNG 2: tái lập bộ thử phiên soạn / số r14 có tái lập bằng chính dụng cụ ấy / `chay14.py` nguyên byte; `do_anh_r13.py`, `ten_tep_11.py`, `kiem_so_r13.py` (chỉ đổi thư mục ghi) / pha A 0/52 hàng lệch × 2 bản; pha B 0 lệch tập ở 4 lượt quét đủ; ba tệp đầu ra giống hệt / KHÔNG PHẢI LỖI.
- HƯỚNG 3: E8n, E8n2 — luồng `threading` khởi động LÚC NẠP chạy bản sao / `threading.setprofile` chỉ áp cho luồng khởi động sau lời gọi, mà bộ quét cài sau khi nạp ⇒ khung guard bản sao không có hàm profile / `rv/chay_rv.py` + lặp 5 lần `quet14 --chi t204` / `t70` `t193` `t204` rc=0, S13 0, `quet13`/`quet14` K rỗng, 0 lần lật, 5/5 ở cả hai bản; oracle rc=1 `ĐỎ t204_moi: BoQuaNen` ở cả hai bản / **LỖI** — P2 F14-1 (không nằm trong danh sách giới hạn r14; `quet14b` bắt cả hai).
- HƯỚNG 4: E8q — ca thay hàm profile bằng hàm khác `None` / cùng cơ chế E8l / như trên / lọt mọi cổng ở cả hai bản; oracle 3.11 rc=0 (mù), 3.12 rc=1 / trong giới hạn đã khai theo CƠ CHẾ (họ E8l; handoff r14 có `sys.setprofile`) nhưng chữ r14 chỉ nêu `None` — gộp vào phương án nhóm (α).
- HƯỚNG 5: E8w — module `profile` thay hàm profile / có thể lọt như E8l / như trên + traceback / K `AssertionError@builtins` ở cả hai bản, do `profile.py` `trace_dispatch_return` (3.11 :292, 3.12 :293) khi có hàm profile ngoài; suite posix rc=0; oracle rc=1 / KHÔNG PHẢI LỖI (bị bắt, dù không nhờ vế lật).
- HƯỚNG 6: E8w2 — `cProfile` / 3.11 `cProfile` thay hàm của `sys.setprofile`, 3.12 thì không / như trên + đo `sys.getprofile()` khi `cProfile` bật (3.11: đối tượng `cProfile.Profile`, sau `disable` là `None`; 3.12: vẫn hàm cũ) / 3.11 lọt (oracle rc=0, mù), 3.12 K `BoQuaNen@ban_sao_204` (1 lần lật) / KHÔNG PHẢI LỖI (A8 đòi đạt ở CẢ HAI bản nên 3.12 đủ để ĐỎ).
- HƯỚNG 7: E8p — bản sao nhập `os` qua `__import__` riêng (ảnh `os.name`) / vế lật đổi module `os` thật nên guard đọc ảnh không thấy `nt` / như trên / lọt mọi cổng ở cả hai bản (1 lần lật); oracle rc=0 cả hai bản (mù vì cùng cơ chế) / KHÔNG ĐO ĐƯỢC kết cục Windows; đưa vào nhóm (β) của phương án như điều kiện cần, không tính là finding riêng.
- HƯỚNG 8: V1 — ca HỢP LỆ, hai luồng cùng gọi guard với `nen="posix"` / *"trả giá trị lúc vào khung"* sai khi hai khung guard xen nhau trên hai luồng / lặp 5 lần; thêm kịch bản đặt ca đầu `CA` / 3.11 K `NotImplementedError` 5/5, `os_name_lech_sau_quet` true 5/5 ở cả hai bản; đầu `CA`: `quet14` 1/12 đạt K 11 (t01 ×4, t02, t02b, t02c, t02d, t03, t04, t05) so `quet13` 10/12 K 2; suite posix 1/1 / **LỖI** — P2 F14-2 (VÁ SINH LỖI MỚI).
- HƯỚNG 9: V6 — ca HỢP LỆ, luồng nền dựng `Path` trong lúc luồng chính gọi guard / `os.name` toàn tiến trình nên luồng khác thấy `nt` / lặp 5 lần / `quet14` K `TinHieuChotCa` 5/5 ở cả hai bản (`NotImplementedError: cannot instantiate 'WindowsPath'` trong luồng nền); `quet13` K rỗng; suite posix 1/1 / **LỖI** — P2 F14-2; với `quet14b` vẫn K (không khử được khi còn lật `os.name`, chỉ khai).
- HƯỚNG 10: V7 — bản sao chỉ đọc hằng / vế lật có báo nhầm khi chỉ nạp bản sao / ma trận / `t70`/`t193`/`t204` rc=0, `quet14` K rỗng, oracle rc=0 / KHÔNG PHẢI LỖI.
- HƯỚNG 11: năm ca hợp lệ của r13 (M7, R11, R12, L1, E5c) / vế lật báo nhầm / ma trận chạy lại / `quet14` = `quet13` (M7, R11 vào N đúng sổ; ba ca kia rỗng) ở cả hai bản / KHÔNG PHẢI LỖI.
- HƯỚNG 12: guard trong khung đã lật / guard dựng `Path` mới thì 3.11 ném `NotImplementedError` thay `BoQuaNen` / đọc thân guard `ab457c6` :613–621 (AST `lineno`/`end_lineno`) / guard chỉ đọc `tep` có sẵn, `yaml`, `_nhan_runs_on`; E8a, c, d, f, i, j, k, m vào K bằng `BoQuaNen@…` (không `NotImplementedError`) / KHÔNG PHẢI LỖI.
- HƯỚNG 13: oracle với ca đồng thời / oracle cùng cơ chế lật toàn tiến trình nên cũng báo oan / chạy oracle trên V1, V6 / V6 rc=1 ở cả hai bản, V1 rc=1 ở 3.11 / quan sát: không số nào của r14 dựa vào oracle trên ca đồng thời; khai trong phương án.
- HƯỚNG 14: số MỚI của r14 (trọng tâm 2) / P3 do số tự khai mới / BẢNG ĐO / mọi số đo được đều khớp / KHÔNG PHẢI LỖI.
- HƯỚNG 15: §9 :2017 *"lệnh cũ có nháy kép ra 19 dòng"* (chữ r13, không đổi) có lệch cùng kiểu câu §2 vừa sửa / đọc + đếm / lệnh cũ hai mẫu ra 19, nhất quán với §9 (5) của r14 / KHÔNG PHẢI LỖI, ngoài phạm vi.
- HƯỚNG 16: danh tính lượt này / — / `sha256sum ~/.claude/agents/review-opus-max.md` / `e225b81c…b792c`, 1175 byte, mtime 2026-09-29; thân 7 dòng của tệp trùng nguyên văn chỉ dẫn hệ thống tôi nhận / quan sát: CÓ dấu hiệu dựng từ định nghĩa ấy; model/effort đang phục vụ KHÔNG ĐO ĐƯỢC.

## BẢNG ĐO

| khẳng định trong spec (r14, chữ MỚI) | spec khai | đo được (lệnh / hiện vật) | khớp? |
|---|---|---|---|
| đầu tệp, depends_on: khối chuỗi lệnh và `s5.py` không đổi byte | giống từng byte r13, OID `c730245c…2694` | trích vùng 63–99 và 119–325 ở r13 và r14, `cmp` rc=0 ×2; `git hash-object` = `c730245ceea8cc5368d5ef84f8e296cd35102694` | KHỚP |
| r14 giữ nền: `adg2` sau `fetch --prune` (rồi `merge --ff-only`) | 15:16:37Z–15:16:38Z; `origin/master` = `ab457c6` | `FETCH_HEAD` mtime 15:16:38.706Z, 475 nhánh; `HEAD` = `refs/remotes/origin/master` = `ab457c6…`; bước `merge` (đã cập nhật) và giờ bắt đầu không để dấu vết | KHỚP phần đo được; giờ bắt đầu và bước `merge`: KHÔNG ĐO ĐƯỢC |
| điều kiện (4) tại lúc đo | `diff --quiet` rc=0; `ls-tree` 2 dòng (`93cff2f…`, `7dd06ab…`) | trên `$SP/adg2` (chỉ đọc): rc=0; 2 dòng `100644 blob 93cff2f97e01…`, `7dd06ab6e71a…` | KHỚP |
| `thay_the_cho` r13 | sha256 `711b7b74…4bb1`; commit `35e7f9c…` (cha `d5a57c1`); 13:19:19Z; 1 commit; 2521 dòng | `cay-kho`: `git log --diff-filter=A` = `35e7f9c… 2026-10-07T13:19:19+00:00`; 1 commit chạm tệp; `git show 35e7f9c:<tệp>` sha256 `711b7b74…`, 2521 dòng; `rev-parse 35e7f9c^` = `d5a57c1…` | KHỚP |
| r13 chưa có trên GitHub lúc soạn r14 | `cat-file -t 35e7f9c…` không lấy được | `$SP/adg2`: `fatal: … could not get object info`, rc=128 | KHỚP |
| VERDICT / HINT lượt 13 | `372efdfe…c244` 233 dòng; `c4f73b98…41ce` 2 nhóm 4 hunk | sha256 khớp; `wc -l` 233; `# lop:` 2, `@@` 4 | KHỚP |
| bản chiếu #678 comment `6040597259` | tạo 14:53:46Z, app `claude`, 2940 byte, sha256 `078f8708…`, 0 thực thể HTML, câu tự mô tả, dòng `reviewer` ghi `review-opus-max` | `r14do/p3/i678_comments.json`: đúng từng mục | KHỚP (giờ đọc REST 15:10:00Z: KHÔNG ĐO ĐƯỢC, mtime tệp 15:10) |
| `nguon_cap_viec`, §3: tỷ lệ 12→13 | 1/3 theo lớp, 9/9 theo finding | VERDICT lượt 13 dòng 12, 91 | KHỚP |
| §2 lệnh `grep` của r12 | hai mẫu 19 dòng; riêng `"lease_id"` 16 | `grep -n '"lease_id"\|\[.lease_id.\]'` 19; `grep -n '"lease_id"'` 16; `\[.lease_id.\]` 5 — trên blob `93cff2f` và `1b4de52` (`1741e0a`) như nhau | KHỚP |
| OID `s5.py` r12 | `2f6bde6c…2e01` (hai chỗ) | trích r12 :114–225, 112 dòng, `hash-object` `2f6bde6c90098dd0781252984c5ede31efb62e01`; r14 có ở :20, :114, :2300; `…1e01` chỉ còn trong câu mô tả việc sửa (:2043) | KHỚP |
| `_ls_tree_z`, `_quet_lease_toan_kho` | :1977; :641–701 | AST trên `93cff2f`: 1977–2004; 641–701 | KHỚP |
| HINT nhóm 2 (a) | 123 mục ở 21 cặp + 2 cặp `null` (23 có khoá) | đếm độc lập trên ảnh 473 ref (`adg2`): 123 / 21 / 2 / 23; 0 danh sách rỗng | KHỚP |
| HINT nhóm 2 (b) | 39 / 6 / 6 / 8 của 59 | 39 / 6 / 6 / 8; 59/59 hết hạn ở 12:18:00Z | KHỚP |
| HINT nhóm 2 (c) | rc=11 ở chín dạng | `ten_tep_11.py` chạy lại: rc=11 ×9, rc=12 ×1, rc=1 ×1; đầu ra giống hệt `ten_tep_11.out` | KHỚP |
| §4 dòng 639: định nghĩa reviewer | phiên soạn r14 đo 15:17:55Z, cùng băm | `e225b81c…b792c`, 1175 byte, mtime 2026-09-29 | KHỚP (giờ đo của phiên soạn: KHÔNG ĐO ĐƯỢC) |
| A8: phiên soạn r14 đo lại vế lật — khung giờ | 15:04:04Z–15:33:21Z | `r14do/p2/chay14.log` | KHỚP |
| A8: ma trận | nền + 51 biến thể (38 + 7 + 6), trả nền 52/52, 0 `.pyc` | chạy lại nguyên byte: 52/52 × 2 bản, 0 hàng lệch so hiện vật, trả nền 52/52, 0 `.pyc` | KHỚP |
| A8: suite, (S) r13, hai bộ quét giống nhau ở hai bản | trừ N5 | `kiem_a8.py`: chỉ `N5 t193` rc=0 / rc=1 | KHỚP |
| A8: oracle cùng mã thoát ở hai bản | trừ E8l | chỉ E8l (0 / 1) | KHỚP |
| A8: nền + 38 cũ, `quet13` = `quet14` | cùng N, N − D, H − D, H2 − D, tên K | 0 khác ở cả hai bản | KHỚP |
| A8: 13 biến thể E8 | qua `t193`, `t204`, (S) r13; `t70` trừ E8m | đúng vậy (E8m `t70` rc=1) | KHỚP |
| A8: vế lật đưa vào K / N | K: E8a, c, d, f, i, j (`BoQuaNen@lease_publish_test`), k, m; N: E8b, E8h | đúng vậy ở cả hai bản; `q1_chi` False ở E8b, E8h | KHỚP |
| A8: không có vế lật | `quet13` chỉ thấy E8b (N), E8m (H − D) | đúng vậy | KHỚP |
| A8: oracle | ĐỎ 13/13 ở 3.12; 12/13 ở 3.11 (xanh E8l) | đúng vậy | KHỚP |
| A8: quét đủ nền | 201 = 187 + N 12 + K 2; N = sổ; N − D ∅; K {t199, t203}; H − D {t193}; H2 − D {t71, t72, t73, t98, t193, t203}; status 0, 0 `.pyc` | chạy lại cả bốn lượt (`quet13`, `quet14` × 3.11, 3.12): cùng mọi tập, 118 lần lật ở `quet14`, status 0, 0 `.pyc` | KHỚP |
| A8: thời gian quét đủ | 597,3 \| 694,7 s (`quet13`); 562,9 \| 660,6 s (`quet14`) | hiện vật `kq/quet_du_*.json` đúng các số ấy; lượt chạy lại của tôi 679,5 \| 846,1 s; 737,3 \| 835,3 s | KHỚP hiện vật (thời gian khác do tải máy chung) |
| A8: giới hạn khai | E5f; E8e (oracle ĐỎ hai bản); E8g (oracle ĐỎ hai bản); E8l (oracle ĐỎ ở 3.12) | đúng từng mục; NHƯNG thêm E8n, E8n2 lọt mọi cổng ở cả hai bản (oracle ĐỎ) mà danh sách không nêu | **LỆCH** — F14-1 |
| A8: vế lật *"đúng trong khung … ra khỏi khung thì trả giá trị lúc vào khung"* | lật chỉ trong khung guard | `os.name` là thuộc tính module, đổi TOÀN TIẾN TRÌNH: V6 K ở cả hai bản; V1 K ở 3.11 và `os.name` kẹt `nt` ở cả hai bản; V1 đầu `CA`: 1/12 đạt (so 10/12) | **LỆCH** — F14-2 |
| A8: câu H2 | bản sao ở module nạp lại *"vào K (hay N, E8h) nhờ vế lật"* | E8e, E8g, E8l (r14 tự khai), E8n, E8n2, E8q, E8p không vào K | **LỆCH** — F14-1 |
| §9: chuỗi tỷ lệ, tọa độ PROTOCOL | 6→7 N/A … 12→13 1/3; :1087–1093; :1098–1100 | VERDICT lượt 13; `ab457c6:docs/PROTOCOL_DA_PHIEN.md` dòng 1087 (*Tín hiệu không hội tụ*) … 1093, 1098 (*Một lớp xuất hiện ở ba lượt*) … 1100 | KHỚP |
| §9 (1)–(5) | E8h vào N; E8l thiếu ở HINT; E8g oracle ĐỎ; phần còn lại tái lập; nhóm 2 đúng + bốn chỗ | đúng từng mục (ma trận, ảnh, `kiem_so_r13`) | KHỚP |
| §10 (a) | áp HINT 13: rc=0, 4/4, 0 fuzz/offset; `38eeafbf…8758`, 2556 dòng = `SPEC_all.md` | đúng từng mục | KHỚP |
| §10 (c) ảnh 473 ref | 473; 3986; 0; 589; 0; 1384 + 23; 123; 0; 0; 0; 59; 6 (wp685, wp710); 37081; 4 `.nhap` trên 286–296 ref; 299 dưới `ops/reviews/`, 0 giống lease; 2766; 6 | `do_anh_r13.py` chạy lại: JSON giống hệt (20/20 khoá); đếm độc lập khớp các số về cặp lease | KHỚP |
| §10 (e) `kiem_so_r13.py` | 75 phép so: 72 KHỚP, 3 lệch, bốn chỗ | chạy lại (chỉ đổi thư mục ghi tạm): giống hệt; LỆCH = H1, G1, G2 (G2 hai tọa độ) | KHỚP |
| §10 ADR: biên nhận `wp678` | 6 `wp678-spec-review-*` trên `ab457c6`; chỉ chừng ấy trên mọi ref; lượt 7–13 chưa có | `$SP/adg2`, 476 ref (`refs/heads` + `refs/remotes`, bỏ `HEAD`): tên `wp678` duy nhất là `wp678-spec-review-{1..6}-codex-verdict.{md,receipt.yaml}`; 6 `.receipt.yaml` trên `ab457c6` | KHỚP |
| (đề xuất HINT) quét đủ nền bằng bộ quét đề xuất | — | `rv/du_3.1x.json`: `quet14` và `quet14b` trên CÙNG clone `ab457c6`, MỘT lệnh mỗi bản: cả bốn lượt 201 ca = 187 đạt + N 12 + K 2; `q1_N_bang_so` true; N − D rỗng; K {`t199`, `t203`} (`TinHieuChotCa@lease_publish_test`); H − D {`t193`}; H2 − D {`t71`, `t72`, `t73`, `t98`, `t193`, `t203`}; 118 lần lật; `quet14b` L rỗng; `os_name_lech_sau_quet` false; status 0, 0 `.pyc`; 695,1 \| 977,0 s (`quet14`), 788,1 \| 762,9 s (`quet14b`) | giống hệt `quet14` (phương án không đổi nền) |

## CHI TIẾT TỪNG LỚP

### Lớp 1 — `tuong-tac-677-kiem-ke-t70-chua-neu` (P2, CÒN MỞ; lượt 8–14)

**Phần đã đóng (tái lập độc lập).** Mọi số A8 mà r14 thêm đều tái lập: chạy lại `chay14.py` NGUYÊN BYTE trên bản sao cây công cụ (phụ thuộc chép từ `$SP/cr678-r13`, `adg2` thay bằng `$R/kho.git` cùng cây `ab457c6`) ⇒ pha A 0/52 hàng lệch × 2 bản, pha B 0 lệch tập × 4 lượt quét đủ. Vế lật đúng là có răng với E8a, c, d, f, i, j, k, m (K) và E8b, h (N), không báo nhầm trên nền, 38 biến thể cũ và năm ca hợp lệ.

**F14-1 — giới hạn khai theo API hẹp hơn giới hạn thật (VÁ HỜ của F13-1).**
- HINT lượt 13 khai: *"bản sao guard mà vế ấy không nhận ra hay không tới được, tức … (E8e: luồng ngoài profile …)"*. r14 viết lại thành danh sách bốn mục theo API: *"tiến trình con (E5f); luồng `_thread` thô chạy bản sao (E8e …); thân guard bị sửa … (E8g …); ca tự gọi `sys.setprofile(None)` … (E8l …)"*, và câu H2 khai mọi bản sao ở module nạp lại *"vào K … nhờ vế lật"*. Trong cùng A8, vế H và vế lật nêu `threading.setprofile`, và E8m (bản sao trong `threading.Thread`) được ghi là vào K — nên người đọc đúng chữ tin rằng mọi luồng `threading` được phủ.
- Đo: E8n (luồng thợ `ThreadPoolExecutor` khởi động lúc NẠP module, `submit(int).result()` ở cấp module; ca `t204_moi` nạp bản sao bằng `spec_from_file_location` như E8a rồi `_POOL_204.submit(m2._chay_buoc_dang_that, …).result()`; thêm `t204` vào `mong`) và E8n2 (luồng `threading.Thread` daemon + hai hàng đợi, khởi động lúc nạp): `t70`, `t193`, `t204` rc=0; (S) r13 rc=0; `quet13` và `quet14` (`--chi t204`) không xếp `t204` vào N, K, N − D, H − D, H2 − D, `so_lan_lat` 0 — ở 3.11.15 và 3.12.3, lặp 5/5; oracle `mo_phong_nt14.py` rc=1 `ĐỎ t204_moi: BoQuaNen: (PosixPath('…/ops-publish-lease.yml'), 'dang')` ở cả hai bản; suite posix `1/1 đạt`.
- Cơ chế: `threading.setprofile` chỉ gắn hàm profile cho luồng khởi động SAU lời gọi (`Thread._bootstrap_inner`); `quet14.py` cài nó sau khi nạp module (dòng `sys.setprofile(prof)`/`threading.setprofile(prof)` nằm trong vòng lặp ca), nên luồng khởi động lúc nạp không mang hàm profile ⇒ khung guard bản sao chạy ở đó không bị lật.
- Theo nguyên tắc chống chạy đua của PROMPT: biến thể CỐ Ý né cổng, KHÔNG nằm trong danh sách giới hạn r14, và người làm đúng chữ r14 tin rằng luồng `threading` được bắt ⇒ đủ điều kiện P2. Phương án không đuổi theo từng cách viết: khai giới hạn THEO TÍNH CHẤT (khung guard bản sao không chạy dưới hàm profile; không khớp tên/bytecode hay không đọc `os` thật; tiến trình con) để biến thể mới rơi vào "trong giới hạn đã khai", cộng một thay đổi rẻ có đo (cài `threading.setprofile` trước khi nạp) bắt luôn E8n, E8n2.

**F14-2 — vế lật đổi trạng thái toàn tiến trình (VÁ SINH LỖI MỚI).**
- Chữ r14 (HINT 13): *"lật `os.name` thành `nt` đúng trong khung của MỌI hàm … ra khỏi khung thì trả giá trị lúc vào khung"*. `os.name` là thuộc tính của module `os`: trong lúc khung guard mở, MỌI luồng thấy `nt`; và khi hai khung guard của hai luồng xen nhau rồi ra không theo thứ tự LIFO, phép "trả giá trị lúc vào khung" (ngăn xếp dùng chung, `ngan[-1][0] is frame`) để `os.name` kẹt `nt` tới hết lượt quét. `quet13.py` (r13) không lật nên không bị.
- Đo (ca HỢP LỆ: không dùng helper, gọi guard với `nen="posix"` tường minh nên đạt trên Windows thật; suite posix `1/1`): V1 (hai `threading.Thread` mỗi luồng gọi guard 150 lần) ⇒ `quet14` 3.11: K `t204:NotImplementedError@builtins`, `os_name_lech_sau_quet` true (5/5); 3.12: K rỗng nhưng `os_name_lech_sau_quet` true (5/5). V1 đặt ĐẦU `CA` (`t000_guard_hai_luong_posix`), quét `--chi t000,t01_,t02,t03,t04,t05`: `quet14` 12 ca, 1 đạt, K 11 (`t01` ×4, `t02`, `t02b`, `t02c`, `t02d`, `t03`, `t04`, `t05`; 10 `NotImplementedError` + 1 `FileNotFoundError`) ở CẢ HAI bản; `quet13` cùng tập ca: 10 đạt, K 2 (`t01` `FileNotFoundError` ×2 — tạo tác cây tối thiểu, có ở cả hai bộ quét). V6 (luồng nền `Path("ops") / "x"` liên tục trong lúc luồng chính gọi guard 150 lần) ⇒ `quet14` K `t204:TinHieuChotCa@lease_publish_test` ở cả hai bản (5/5; luồng nền gặp `NotImplementedError("cannot instantiate 'WindowsPath' on your system")`); `quet13` K rỗng.
- Hệ quả cho tiêu chí: (q3) đòi *"tập TÊN của K trên ứng viên trừ tập ấy trên nền rỗng"* ⇒ một ca hợp lệ như trên làm (q3) ĐỎ oan; chữ r14 chỉ có lối khai cho tạo tác của seam kiểu *"vá `os.name` để đo guard"*, không cho loại này. A1–A7 không đòi ca đa luồng, nên xác suất executor tự vấp thấp — vì thế P2 chứ không P1.
- Phương án (đo): bộ đếm độ sâu toàn tiến trình có khoá + trả giá trị gốc sau mỗi ca (tập L) khử V1 và hệ quả lan (10/12 đạt, như `quet13`); V6 không khử được khi còn lật `os.name` (luồng khác thấy `nt` trong lúc guard mở) nên KHAI nó như tạo tác (handoff nêu, không tự tính là đạt). Oracle `mo_phong_nt14.py` cùng cơ chế nên cũng báo ĐỎ ở V6 (cả hai bản) và V1 (3.11) — không số nào của r14 dựa vào oracle trên ca đồng thời.

**Phép kiểm của phương án (bộ quét `rv/quet14b.py`).** `rv/chay_b.py`, MỘT lệnh, cùng cây tối thiểu, `quet14` và `quet14b` lần lượt trên mỗi biến thể (NỀN, 38 cũ, 13 E8, 8 của tôi), 3.11 ‖ 3.12: khác ĐÚNG ba hàng ở mỗi bản (E8n, E8n2: `quet14` K rỗng → `quet14b` K `BoQuaNen@ban_sao_204`; V1: 3.11 K `NotImplementedError` → rỗng, `os_name_lech` true → false; 3.12 `os_name_lech` true → false); 57 hàng còn lại trùng N, N − D, K, H − D, H2 − D, `q1_chi`, `so_ca`, `dat`; trả nền đủ, 0 `.pyc`. Kịch bản V1 đầu `CA`: `quet14b` 10/12 đạt, K 2 (= `quet13`), L rỗng. Quét đủ nền: xem dòng cuối BẢNG ĐO.

### Lớp 2 — `chinh-xac-hoa-so-hieu-va-tham-chieu` (P3 ở lượt 12–13; ĐÃ VÁ THẬT ở lượt 14)

Ba câu HINT nhóm 2 vào r14 NGUYÊN VĂN (so r13+HINT13 với r14: không vùng khác nào ở :436–445, :505–510) và đúng khi đo ĐỘC LẬP trên `adg2` (không chỉ trên hiện vật phiên soạn). Bốn chỗ phiên soạn tự tìm đúng. Tôi rà mọi số MỚI của r14 (đầu tệp, bảng chỗ đổi, `thay_the_cho`, `nguon_cap_viec`, `depends_on`, nền nghiệm thu, §2, §3, §4, A8, §8, §9, §10): mọi số đo được đều khớp (BẢNG ĐO); phần KHÔNG ĐO ĐƯỢC chỉ là giờ của các bước phiên soạn không để hiện vật (giờ bắt đầu `fetch`, bước `merge --ff-only` khi đã cập nhật, giờ đọc REST, giờ băm định nghĩa reviewer). Không còn biểu hiện cùng cơ chế do bản vá sinh ra.

## DRY-RUN HINT.patch

Tệp `$R/goi/HINT.patch`: 1 nhóm (`# lop: tuong-tac-677-kiem-ke-t70-chua-neu` ngay trước `--- `), 4 hunk, một tệp đích `ops/specs/lease-id-ep-kieu-yaml-r14.md` (repo-relative, không tiền tố), 0 dấu chéo ngược. Không có nhóm cho `chinh-xac-hoa-so-hieu-va-tham-chieu` (ĐÃ VÁ THẬT). Dựng bằng `hint/mk_hint14.py`; kiểm bằng `hint/kiem_hint.sh` — đúng lệnh PROMPT trên bản sao `mktemp -d -p "$R"` (không đụng `cay-kho`), rồi áp thật trên CHÍNH bản sao ấy, so băm với bản dựng độc lập `SPEC_moi.md`, kiểm khối lệnh và `s5.py`, dọn bản sao. Output nguyên văn (`hint/kiem_hint.out`):

```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```

```
HINT.patch: 13564 byte, sha256 7a8976acfd7c4305ac60566868f0f2f593cc89b86b39fe5d1e066f21557e85e3
nhóm (# lop:): 1, hunk (@@): 4, dấu chéo ngược: 0
bản sao: /tmp/claude-0/-home-user-tra-luat/8413b80e-5157-5812-ad93-3be1f70600c0/scratchpad/cr678-r14/tmp.GZNdt0LlV1/cay HEAD 284a03fa6eff0356a79cca2926b889a6a98896f0 status 0 dòng
Hmm...  Looks like a unified diff to me...
The text leading up to this was:
--------------------------
|# lop: tuong-tac-677-kiem-ke-t70-chua-neu
|--- ops/specs/lease-id-ep-kieu-yaml-r14.md
|+++ ops/specs/lease-id-ep-kieu-yaml-r14.md
--------------------------
checking file ops/specs/lease-id-ep-kieu-yaml-r14.md
Using Plan A...
Hunk #1 succeeded at 1201.
Hunk #2 succeeded at 1220.
Hunk #3 succeeded at 1231.
Hunk #4 succeeded at 1343.
done
dry-run rc=0
áp thật rc=0
succeeded: 4
offset|fuzz|FAILED: 0
sha256 sau áp: 55fd69a54cd1e8d8b86ddb5f469db2085b70fb761b29a869638dfaf0e3b9c20d 2669 dòng
sha256 SPEC_moi: 55fd69a54cd1e8d8b86ddb5f469db2085b70fb761b29a869638dfaf0e3b9c20d
git status sau áp:  M ops/specs/lease-id-ep-kieu-yaml-r14.md;
.orig/.rej: 0
khối chuỗi lệnh sau áp: giống byte
s5.py sau áp: c730245ceea8cc5368d5ef84f8e296cd35102694
đã dọn bản sao
```

Đọc kết quả: dry-run rc=0, 4 dòng `succeeded`, 0 `FAILED`, 0 fuzz, 0 offset; áp thật rc=0; sha256 sau áp BẰNG bản dựng độc lập; đúng một tệp đổi; 0 `.orig`/`.rej`; khối chuỗi lệnh giống byte, `s5.py` giữ OID `c730245c…2694` ⇒ điều kiện cấp không đổi. HINT chỉ sửa chữ A8 (dụng cụ đo của executor ở scratch); không đụng write set, closure hay năm điều kiện cấp.

## LƯU Ý CHO PHIÊN ĐIỀU PHỐI (không phải finding)

1. **Danh tính lượt này.** Tôi là Claude Opus 5.5 (`claude-opus-5-5`), effort max, subagent do phiên điều phối giao. Chỉ dẫn hệ thống tôi nhận trùng NGUYÊN VĂN 7 dòng thân `~/.claude/agents/review-opus-max.md` (sha256 `e225b81cf2fbdd0f05a54a689cac17db8972b2f8c0684a0a30931875cd4b792c`, 1175 byte, `model: claude-opus-5-5`, `effort: max`) — CÓ dấu hiệu lượt này dựng từ định nghĩa ấy; model/effort đang phục vụ vẫn KHÔNG ĐO ĐƯỢC (cấu hình, không phải runtime evidence). Lượt này KHÔNG sạch (`changes_requested`), nên điều kiện cấp (3) vẫn chưa thoả dù danh tính được xác nhận.
2. **§12.** 13→14 = 1/2 = 50% theo lớp (3/4 theo finding) — không tạo cặp chuyển tiếp liền nhau < 50% mới (12→13 là 1/3). `tuong-tac-677-…` nay có mặt ở bảy lượt (8–14): luật *"một lớp ở ba lượt"* (:1098–1100) đòi xem lại cách làm; Q13 đã quyết lặp không trần. ADR-0048 (trần mười vòng có biên nhận): đây là lượt thứ 14 của chuỗi review đặc tả; áp hay không là việc của điều phối/chủ kho.
3. **Hội tụ.** Lớp P2 còn mở vì cùng một hình dạng các lượt 11–13 đã gọi tên: dụng cụ đo được MÔ TẢ rộng hơn thứ nó đo. Phương án của tôi cố ý KHÔNG đuổi theo cách viết: nó khai giới hạn THEO TÍNH CHẤT (α không chạy dưới hàm profile; β không khớp tên/bytecode hay không đọc `os` thật; γ tiến trình con). Theo đúng nguyên tắc chống chạy đua của PROMPT, mọi biến thể mới rơi vào α/β/γ từ nay là *"trong giới hạn đã khai"*, không phải finding. Phần còn lại là tạo tác báo nhầm (F14-2): bộ đếm độ sâu khử được dạng kẹt và lan (V1), còn dạng luồng khác thấy `nt` trong lúc guard mở (V6) chỉ KHAI được, không khử được khi còn lật `os.name` toàn tiến trình; đóng dứt điểm cả hai chiều cần Windows thật (lượt `windows-latest` của `ci.yml` qua `workflow_dispatch` trên ref thi hành TRƯỚC land) — lựa chọn của chủ kho, không phải chữ đặc tả.
4. **Việc phiên soạn r15 cần làm nếu nhận HINT:** cập nhật bảng *Thay đổi so với r14*, hàng A8, §9 (bộ đếm sau lượt 14), §10; đo lại bằng dụng cụ của chính phiên soạn (tôi chỉ đưa số của `rv/quet14b.py`); quyết có giữ `profile`/`cProfile` và *"mã cấp module MỚI chạy lúc nạp"* trong danh sách handoff hay không.
5. **Đọc ngoài `$R`.** Bộ thử `r14do/` phụ thuộc thư mục ngoài `$R` (`$SP/cr678-r13/r13do/l2b`, `$SP/adg2`, và `kiem_so_r13.py` đọc `$SP/wt-678r7`, `$SP/cr678-r13/{luot12,r13do}`). Tôi CHỈ ĐỌC chúng (chép phần cần vào thư mục tạm; git chỉ đọc với `GIT_OPTIONAL_LOCKS=0`), kiểm `find -newer` trước/sau: 0 tệp đổi. Nhờ `$SP/adg2` mà các số 473 ref / `adg2` — lượt 13 ghi KHÔNG ĐO ĐƯỢC — nay đo được (trạng thái `adg2` sau `fetch` 15:16:38Z).

## GIỚI HẠN VÀ TOÀN VẸN

- **Không mạng.** Trạng thái máy chủ GitHub lúc review: KHÔNG ĐO ĐƯỢC; số "mọi ref" là của `$SP/adg2` (476 ref, `FETCH_HEAD` 15:16:38Z), không phải máy chủ lúc này.
- **Windows thật KHÔNG ĐO ĐƯỢC.** Kết cục "ĐỎ dưới `nt`" của E8n, E8n2 là của oracle mô phỏng `mo_phong_nt14.py` (của phiên soạn, chạy nguyên byte); oracle ấy lật `os.name` toàn tiến trình nên chính nó báo oan ở V6 (cả hai bản) và V1 (3.11); E8p làm nó mù.
- **Ca hợp lệ của tôi là ca DỰNG để đo,** không phải ca packet bắt buộc; A1–A7 không đòi ca đa luồng — lý do F14-2 là P2 chứ không P1.
- **Trần song song.** Pha B của lượt chạy lại (2 lượt nặng) chồng với `rv/chay_b.py` và các lượt lặp (`--chi t204`, nhẹ); lượt quét đủ của đề xuất chạy 3.11 từ 16:18:22Z (sau khi pha B 3.11 xong 16:17:20Z) và 3.12 từ 16:23:21Z (sau khi pha B 3.12 xong 16:22:52Z) ⇒ không lúc nào quá 2 lượt quét ĐỦ cùng lúc. Thời gian quét đủ dài hơn số phiên soạn (tải máy chung, `loadavg` tới ~12 trên 4 lõi); tập kết quả không đổi.
- **Đĩa.** Thư mục tạm của tôi `$R/w14.Xjll` ≤ 0,6 GB lúc cao nhất (hai clone đủ đồng thời); đã dọn toàn bộ sau lượt bằng `shutil.rmtree`, hiện vật cần để tái lập nằm ở `$R/goi/do/`.
- **Toàn vẹn đầu vào.** `PROMPT.md`, `SPEC.md`, `SPEC-r13.md`, `r13-r14.diff` giữ băm; `r14do/`, `luot9/`–`luot13/`, `kho.git/`, readback: 0 tệp mới hơn `PROMPT.md`. `cay-kho`: HEAD `284a03f…`, `status --porcelain --ignored` 0 dòng; `index` giữ mtime 15:38:22Z; chỉ mtime THƯ MỤC `.git` đổi do `git status` tạo/xoá `index.lock`.
- **Ràng buộc đã giữ.** Không đăng GitHub, không commit/push, không in biến môi trường hay bí mật; mọi `patch` trên bản sao `mktemp -d -p "$R"`; chỉ ghi dưới `$R/goi/` và `$R/w14.Xjll` (cùng các thư mục `mktemp` đã dọn).
