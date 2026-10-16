verdict: changes_requested
reviewed_sha: e48423a2719f64a5dfa2f85363874dfadf6c10f8
spec_sha256: fd1138c32ad750b9f52411d3d8cba39483584dfcec0cb2c479aa312cc16a4a98
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Chạy như SUBAGENT do phiên điều phối giao (lượt 11), cùng họ Claude với phiên soạn r11 ⇒ không độc lập khác họ. Model/effort là CẤU HÌNH được giao, không phải runtime evidence (PROTOCOL :710–711): lượt này không sinh `modelUsage`, không có `session_run_id`; có được giao qua định nghĩa `review-opus-max` hay không: KHÔNG ĐO ĐƯỢC từ phía tôi. Biên nhận của lượt (nếu ghi) phải tự khai `che_do: subagent_trong_phien_dieu_phoi`, mức `review_deferred`. Không mạng, không đăng GitHub, không commit/push, không sửa `cay-kho`; chỉ ghi dưới `$R/goi/` và `mktemp -d -p "$R"`.

Kết luận nội dung: **0 P1 / 2 P2 / 0 P3** (theo lớp; 5 finding F11-1…F11-5).
P2: `thu-tu-677-bo-ngo-o-dieu-kien-cap` (VÁ SINH LỖI MỚI; lượt 7, 8, 9, 10, 11) · `tuong-tac-677-kiem-ke-t70-chua-neu` (VÁ SINH LỖI
MỚI; lượt 8, 9, 10, 11). P3: 0 lớp — `hop-dong-dong-bang-thieu-neo` và `so-do-nen-khong-khop` ĐÃ VÁ THẬT; hai biểu hiện mức P3 mới
(F11-3, F11-5) cùng cơ chế với hai lớp P2 nên gộp vào đó.

Trả lời câu hỏi gốc, áp cho r11.
(1) Phạm vi: r11 đổi đúng những gì nó khai — 15 hàng định danh/closure, objective, write set, §1, §2, §5, Phụ lục A, A1, A4–A7, A9,
A10 giống byte r10; A2 chỉ đổi câu r7→r8 (HƯỚNG 1).
(2) Làm đúng từng chữ r11 thì packet land được hợp lệ trong trường hợp thường — không P1. Nhưng hai bảo đảm r11 tuyên bố rộng hơn
phép đo, đo được: chuỗi cấp CẤP NHẦM khi một lease còn hạn giữ hai tệp theo dạng write set mà PROTOCOL §5 cho phép (prefix `ops/`;
cả hoa/thường và mục dạng ánh xạ) hay khi `remote.origin.vcs` đổi chương trình vận chuyển (HƯỚNG 5, 6); và phép quét động A8 —
khai là tiêu chí nghiệm thu của "phần (i) mà vị từ tĩnh không thấy" — để lọt ca gọi helper qua đường lạ rồi tự bắt `BoQuaNen`
(N9, N10: qua t70, t193, q1, q2, q3 ở 3.11 lẫn 3.12; HƯỚNG 12). Cả hai có cách vá đã chạy (HINT nhóm 1, 2).
Trọng tâm lượt 11: bộ thử phiên soạn tái lập đủ (r10 17 · HINT 5 · r11 1); bộ thử lượt 10 trên khối r11 (bộ chấm độc lập đọc từng
chữ) 0 CẤP nhầm nhưng lộ quy tắc "chạy lại MỘT lần" không thoả được theo chữ (F11-3); S15 đúng là không đo được bằng git (HƯỚNG 8);
không đường nào CẤP khi một bước KHÔNG chạy — chỉ khi bước CHẠY mà đo sai thứ (HƯỚNG 9). A8 đúng chữ XANH trên nền ở 3.11.15 và
3.12.3 (4 lượt, K ổn định {t199, t203}); M1–M6 + 8 đường lượt 10 đỏ; vế K không báo nhầm với ứng viên làm đúng (M7, một lệnh) nhưng
so BẰNG và ví dụ t199 mâu thuẫn (F11-5); lý do không thành ca test đứng (HƯỚNG 14).
(3) Hai P3 lượt 10 ĐÃ VÁ THẬT (HƯỚNG 15). (4) Số hạng r11 (ci.yml, blob, diff, tọa độ, Q-băm, cổng biên nhận, 419,9/687,2 s truy được)
khớp; đo live lúc soạn KHÔNG ĐO ĐƯỢC ở đây (HƯỚNG 16). (5) Tỷ lệ vá thật 10→11 = **2/4 = 50%** (chi tiết ở ĐỐI CHIẾU).

## KIỂM ĐẦU VÀO
- `sha256sum $R/SPEC.md` -> fd1138c32ad750b9f52411d3d8cba39483584dfcec0cb2c479aa312cc16a4a98 (khớp)
- `git -C $R/cay-kho rev-parse HEAD` -> e48423a2719f64a5dfa2f85363874dfadf6c10f8 (khớp)
- `sha256sum $R/PROMPT.md` -> 86256edb8b5591ed557e92a7b970e23ed32d13399fd9392cbc28a2501d07f40c (khớp băm điều phối trao)
- PROMPT nhắc `luot6/`, `q10-readback.json`, `r6-r7.diff` — KHÔNG có trong $R (đoạn ấy của PROMPT viết cho lượt 7); thay bằng `readback-5911243074.json` (Q10) … `readback-5928886724.json` (Q13).
- Công cụ: python3.11 3.11.15 · 3.12.3 · 3.13 (có), PyYAML 6.0.1, git 2.43.0, GNU patch, shellcheck, actionlint; không mạng. Thư mục đo: `$R/do11.LslY` (mktemp; TMPDIR trong đó). kho.git: 9 nhánh + 41 tag (KHÔNG phải 456 nhánh máy chủ).

## NHẬT KÝ TĂNG DẦN
- 12:2xZ Khối lệnh r11 trích từ SPEC.md (dòng 59–89, 31 dòng) sha256 3241aa33… = `r11do/chuoi/chuoi_r11.txt` (cmp khớp); SPEC.md = cay-kho/ops/specs/lease-id-ep-kieu-yaml-r11.md (cmp khớp); `git diff --name-status 423b4ba e48423a` = đúng 5 dòng A (r7–r11).
- 12:2xZ Dựng lại văn bản r10 + HINT lượt 10 (`patch -p0 --fuzz=0` lên bản sao): rc=0, 11/11 hunk, 8 hunk offset (2/15), 1319 dòng, sha256 001251f7…755d — KHỚP §9.
- 12:22:51Z–12:23:40Z Bộ thử phiên soạn (`harness.py` chép sang `do11.LslY/chuoi/`, CHỈ đổi 2 đường dẫn LP/R10 sang bản cùng băm trong $R) chạy 32 kịch bản × 3 văn bản: CẤP nhầm r10 17 · HINT 5 (S15 S16 S18 S24 S25) · r11 1 (S15) — KHỚP bảng §10. `r11do/chuoi/ht_tatca.out` để lại là bản TRƯỚC khi sửa S19 (cột HINT S19 ghi KXĐ; bảng §10 và lượt chạy lại của tôi: CẤP) — khớp lời khai "S19 chạy lại sau khi sửa cách dựng".
- 12:24:04Z–12:24:28Z `dot_bien_r11.py`: mọi dòng khớp §10 (gỡ endpoint ⇒ 6/6 CẤP; ref đầy đủ ⇒ S9b/S10b CẤP; OID 7 ký tự ⇒ S17 CẤP; no_replace ⇒ S16; cong_cu_oid ⇒ S18; master ⇒ S24; v_ls ⇒ S25; nong ⇒ S19; rc/dem/cong_cu riêng hay ba lớp ⇒ không CẤP; bốn lớp ⇒ S8a, S21, S14 CẤP, S8c lệch tình cờ). 0 .pyc.
- 12:2xZ Thử textconv: `.git/info/attributes` `ops/*.py diff=giong` + `diff.giong.textconv=true` ⇒ `git diff --quiet A B -- ops/a.py` vẫn rc=1 (quick mode so OID) ⇒ (v) KHÔNG bị lừa — KHÔNG PHẢI LỖI.
- 12:29:24Z–12:29:34Z Kịch bản MỚI (`do11.LslY/chuoi/kich_ban_moi.py`, cùng harness, chấm đúng chữ từng văn bản), máy chủ có lease CÒN_HẠN giữ `ops/lease_publish_test.py`:
  N1 nhánh máy chủ `claude/lease-moi/HEAD` ⇒ r11 KXĐ (`ai-dang-giu` CHẶN [12] "cache thiếu nhánh" vì chính nó bỏ ref đuôi `/HEAD`) — fail-close, KHÔNG PHẢI LỖI an toàn;
  **N2 write_set `ops/` (prefix thư mục, PROTOCOL :267) ⇒ r10/HINT/r11 đều CẤP NHẦM**; N2 `Ops/Lease_Publish_Test.py` (case-fold, PROTOCOL :273) ⇒ cả ba CẤP; đối chứng exact ⇒ KHÔNG CẤP rc=11;
  **N3 `remote.origin.vcs=guong` (helper phục vụ mirror cũ; `get-url` vẫn in URL cho phép, `endpoint.khop`=1) ⇒ cả ba CẤP NHẦM**; đối chứng không vcs ⇒ KHÔNG CẤP rc=11. Hiện vật: N3 máy chủ thật `claude/lease-khac`=70913817…, `may_chu.raw` ghi 89fc2033… (mirror). 0 .pyc.
- 12:35:54Z–12:41:56Z Phép quét động A8 viết ĐỘC LẬP theo văn xuôi đặc tả (`do11.LslY/quet/quet_a8.py`; `<gốc>/ops` đầu sys.path, nạp module, vá `_ly_do_bo_qua_workflow` nen mặc định `nt` per-ca bằng `mock.patch.dict`, chạy MỌI ca, đạt/N/K với `except BaseException`), clone đủ `163fd5d` (`git clone --no-hardlinks kho.git` + `checkout --detach`), cwd = gốc, `python`/`python3` trỏ đúng bản, PYTHONDONTWRITEBYTECODE=1, hai lượt SONG SONG: 3.12.3 361,9 s; 3.11.15 311,6 s. Cả hai: 198 ca = 184 đạt + N 12 + K 2; q1 N == SO_BO_QUA đúng cặp (true); q2 N − D = ∅; K = {t199:TinHieuChotCa, t203:TinHieuChotCa} — KHỚP lời khai "K chỉ còn t199, t203". Sau lượt: status --porcelain --ignored 0 dòng, 0 .pyc. Thời gian khác số đặc tả (419,9 s một mình) — cùng bậc, phụ thuộc máy, không phải lỗi.
- 12:41:13Z–12:41:38Z Chuỗi ĐỀ XUẤT r12 (`chuoi_r12.txt` = r11 + 2 cặp dòng: `git config --get-regexp '^remote\.origin\.'` theo danh sách cho phép; `ai-dang-giu ops/`) trên 32 kịch bản + kịch bản mới: 32 kịch bản cũ GIỐNG HỆT r11 (chỉ S15 CẤP); N2_prefix ⇒ KHÔNG CẤP rc=11; N3_vcs ⇒ KXĐ (remote.cfg 3 dòng); còn CẤP: N2_case (hoa/thường) và N2_dict (mục write_set dạng ánh xạ `{type: prefix, path: ops/}`) — `_lease_cham_duong` chỉ nhận chuỗi, so nguyên chuỗi ⇒ phải KHAI giới hạn.
- 12:42:35Z–12:43:30Z Pha nhanh 19 biến thể × {3.11.15, 3.12.3} (biến thể M1–M7, N1–N8, R11–R13 của phiên soạn chép từ scratch chung `r11do/bt/`, gốc `goc.py` = blob `163fd5d:ops/lease_publish_test.py` sha256 09cf6c78…; cộng N9, N10 của reviewer), mỗi biến thể chép đè rồi trả gốc, kiểm sha256, sau mỗi biến thể `status --porcelain --ignored` 0 dòng và 0 .pyc: KHỚP lời khai §10 (M1–M3, N1–N8 ⇒ t70 1/1, t193 1/1 (trừ N5@3.12 0/1), N−D = {t204}; R13 ⇒ t193 0/1 + N−D; M5, M6 ⇒ chỉ K bắt; M7, R11, R12 ⇒ không bắt nhầm). MỚI: **N9 (gọi `globals()["_chay_buoc_dang_that"]` rồi `except BoQuaNen: return`) và N10 (gọi qua `globals()` trong luồng, nuốt `BoQuaNen`) ⇒ t70 1/1, t193 1/1, t204 1/1, N ∅, K ∅, N−D ∅ ở cả hai bản** — trái (i), (ii) mà lọt cả ba vế q1/q2/q3; chỉ tập H (lời gọi thật, `sys.setprofile`) chứa t204.
- 12:45:20Z–12:45:42Z Bộ thử LƯỢT 10 (`kich_ban.sh` nguyên byte 2ecdbee1…, `chuoi_lib.sh` lượt 10 nạp nguyên văn) + lớp phủ của reviewer chạy ĐÚNG từng dòng khối r11 trong shell hiện tại, PATH công cụ có thêm `wc`; bộ chấm độc lập đọc từng chữ bảng tiêu chí: 0 CẤP nhầm trên S0–S10b, S1n, S2n. S4, S5, S8c: đọc-chữ ⇒ KXĐ ngay lần 1 (thieu=1 ⇒ chung=mc−1 nên "mọi điều kiện khác đạt" không thể đúng); đọc-ý (như bộ chấm phiên soạn) ⇒ chạy lại ⇒ KHÔNG CẤP rc=11.
- 12:48:48Z Cổng biên nhận trên `163fd5d` (bn10.py lượt 10 chép sang thư mục đo; python3.12): `_thieu` 0/0/1/2/0; `kiem()`/CLI ba mẫu rc 0/1/2; sha256 38cda51c… — KHỚP mục (a).
- 12:4xZ Q10–Q13, Q8 readback: sha256/byte khớp số đặc tả ghi (69cc35b1…/2151, 392069d1…/1741, 4c9d5e19…/1648, 5f1ff74e…/1662, 3a8c40a6…/1187), 0 thực thể HTML; mọi dòng không rỗng của các dải khai "chép từng byte" có mặt nguyên văn.
- 12:46:32Z–12:58:22Z MỘT lệnh 3.11.15 (`chay_cap.sh`): nền 298,8 s (N 12 = sổ, N−D ∅, K {t199, t203}) rồi ứng viên M7 410,2 s (199 ca, N = sổ + t204, q1 đạt, N−D ∅, K = nền) ⇒ vế K không báo nhầm với ứng viên làm đúng; trả gốc, status 0 dòng, 0 .pyc.
- 12:46:32Z–13:04:51Z MỘT lệnh 3.12.3 có `--h` (setprofile): nền 503,4 s (N, K y lượt không profile; H − D = {t193}) rồi ứng viên N9 594,5 s (199 ca = 185 đạt + N 12 + K 2): q1 đạt, N−D ∅, K = nền ⇒ **q1–q3 đều ĐẠT**; H − D = {t193, t204} ≠ nền. Trả gốc, status 0 dòng, 0 .pyc.
- 13:00:15Z–13:01:12Z Khối lệnh trích từ bản đặc tả SAU khi áp HINT (35 dòng; lệnh = `chuoi_r12.txt` khi bỏ chú thích) chạy lại 41 kịch bản: y kết quả `chuoi_r12.txt`.
- 13:0xZ #687 r3: `050e6257` 01:02:10Z, sha256 d4d6715d…543e, câu M2 "Phải đo bằng chạy thật, không suy từ tên" có mặt — KHỚP. Khối `coord` trên kho không có thư mục `.github/coordination/`: `ls-tree` rc=0, 0 dòng (tiêu chí "ít nhất 1 dòng" ⇒ KXĐ); rev hỏng rc=128.
- 13:05Z HINT.patch cuối: dry-run đúng lệnh PROMPT rc=0, 8/8 hunk; áp thật rc=0, khớp byte bản kỳ vọng dựng độc lập; mỗi nhóm áp riêng rc=0 (mục DRY-RUN). Dọn bằng `shutil`: bản sao cay-kho, clone quét, thư mục kịch bản (giữ script, log, JSON).

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 10 (Claude Opus 5.5 max, subagent, trên `42292b4`): 0 P1 / 2 P2 / 2 P3, bốn lớp, F10-1…F10-7. Nhãn theo PROTOCOL :636 /
§8.3 (lớp ĐÃ VÁ THẬT chỉ khi mọi biểu hiện trong phạm vi đã đóng, bản vá không sinh biểu hiện cùng cơ chế, không còn phần phải đo).

| lớp (lượt 10) | finding lượt 10 | trạng thái finding trên r11 | trạng thái LỚP lượt 11 | bằng chứng tự đo |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2) | F10-1 origin là mirror (S7a/S7b); F10-2 "0 dòng" là bằng chứng âm (S8a/S8b); F10-3 tên `origin/master` bị che (S9b/S10b) | **ĐÃ VÁ THẬT** cả ba | **VÁ SINH LỖI MỚI** (P2) | 32×3 của phiên soạn: r11 chỉ CẤP ở S15 (giới hạn đã khai); kịch bản lượt 10 trên khối r11: 0 CẤP nhầm (HƯỚNG 2, 3) |
| | (mới, CÓ TỪ r10) F11-1 `ai-dang-giu` khớp write set bằng nguyên chuỗi, hẹp hơn §5 (prefix `ops/`, hoa/thường, mục dạng ánh xạ); F11-2 `remote.origin.vcs` đổi chương trình vận chuyển mà URL vẫn qua danh sách cho phép | — | | N2, N3 ⇒ r10, r10+HINT, r11 đều CẤP nhầm (HƯỚNG 5, 6) |
| | (mới, DO r11 SINH) F11-3 quy tắc "chạy lại MỘT lần" đọc từng chữ không thoả được | — | | S4, S5, S8c đọc-chữ ⇒ KXĐ ngay (HƯỚNG 3) |
| `tuong-tac-677-kiem-ke-t70-chua-neu` (P2) | F10-4 bảy (tám) đường gọi lạ lọt `t70`/`t193`; F10-5 G − D đo ở 3.11 | **ĐÃ VÁ THẬT** | **VÁ SINH LỖI MỚI** (P2) | N1–N8, M1–M3, R13 ⇒ N−D = {t204}; M5, M6 ⇒ K; ở 3.11 lẫn 3.12 (HƯỚNG 11) |
| | (mới, DO r11 SINH) F11-4 lời khai mới "phép quét động là tiêu chí nghiệm thu của phần (i) mà vị từ tĩnh không thấy" — ca gọi helper qua đường lạ rồi tự bắt `BoQuaNen` lọt cả ba vế; F11-5 ví dụ "`t199` đạt dưới `nt`" mâu thuẫn K của chính r11; vế K so BẰNG nên ca nền rời K là báo động giả | — | | N9, N10 qua t70/t193/q1/q2/q3 ở 3.11 lẫn 3.12; t199 ∈ K dưới seam (HƯỚNG 12, 13) |
| `hop-dong-dong-bang-thieu-neo` (P3) | F10-6 hiệu lực miễn trừ đo bằng bộ lọc tên | **ĐÃ VÁ THẬT** | **ĐÃ VÁ THẬT** | ba lệnh `coord` ở 5 mốc: 4 dòng · khớp `0` · neo 2 dòng; thư mục vắng ⇒ 0 dòng ⇒ KXĐ (HƯỚNG 15) |
| `so-do-nen-khong-khop` (P3) | F10-7 "#677 đóng băng ở r7" | **ĐÃ VÁ THẬT** | **ĐÃ VÁ THẬT** | `f860ab7` tạo r8 17:09:42Z 29-09; vắng ở `163fd5d`, có ở `b7e32e0`; là tệp `ops/specs/` duy nhất trong 118 tệp; master không có r9 (HƯỚNG 15) |

Lớp lượt 7–9 đã đóng — có tái phát không (lệnh `grep -n -i 'codex\|claude -p\|phương án B\|session_run_id\|điểm dừng\|dưới 50%'
SPEC.md` rồi đọc từng dòng): `q10-he-qua-mat-nhan-dien-giai`, `dong-reviewer-loi-khai-rong-hon-do`, `duong-review-b-chua-do-dau-cuoi`,
`dieu-kien-dung-12-doc-mot-chuyen-tiep` — KHÔNG tái phát (codex chỉ còn ở tên tệp lease `wp55-r4-review-viet-lai-codex…` và ở
lịch sử; `claude -p`/B/`session_run_id` chỉ ở trích Q12, lịch sử, phép đo validator; §12 đọc hai chuyển tiếp ở :1087–1089, :1162).

**Tỷ lệ vá thật 10→11 (§12 :1043–1049, chỉ báo).** U = 4 lớp mở cuối lượt 10. ĐÃ VÁ THẬT: `hop-dong-dong-bang-thieu-neo`,
`so-do-nen-khong-khop` ⇒ **2/4 = 50%** (không < 50%). Hai lớp P2 không vá thật vì bản vá r11 sinh biểu hiện cùng cơ chế
(F11-3, F11-4/F11-5) và còn biểu hiện có từ trước chưa đóng (F11-1, F11-2). Chuỗi: 6→7 `N/A`, 7→8 0/5, 8→9 2/7, 9→10 1/4 (2/4),
10→11 2/4. Luật một lớp ở ba lượt (:1054–1056) vẫn kích hoạt: `thu-tu-677-…` lượt 7, 8, 9, 10, 11; `tuong-tac-677-…` lượt 8, 9,
10, 11. Q13 đã quyết lặp tiếp nên đây là số báo cáo. Gợi ý cho checkpoint (không phải điều kiện): phần còn lại của cả hai lớp
không nằm ở chữ của đặc tả mà ở NGỮ NGHĨA của hai dụng cụ đặc tả mượn (`ai-dang-giu` khớp nguyên chuỗi; seam `nt` chỉ đo kết
cục) — cùng hình dạng "đổi câu hỏi" như Q9: khai giới hạn và mở packet riêng thay vì vá thêm chữ.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` | **P2** (VÁ SINH LỖI MỚI; lượt 7, 8, 9, 10, 11) | F11-1 (hàng `depends_on` :40 "Đây là kiểm loại trừ write set của protocol"; bước (iv) :81–84): `ai-dang-giu` so mục `write_set` bằng NGUYÊN CHUỖI (`_lease_cham_duong` :546–549) trong khi PROTOCOL :267 cho prefix thư mục và :272–273 đòi NFC + case-fold; master có lease prefix (`ops/reviews/wp538/`…); `_khop_tien_to` :140–142 cùng tệp đã khớp prefix ⇒ lease còn hạn `write_set: [ops/]` (cũng `Ops/Lease_Publish_Test.py`, và mục ánh xạ `{type: prefix, path: ops/}`) ⇒ r11 CẤP nhầm. F11-2 (:65–66, :121–124): URL cho phép không ghim chương trình vận chuyển — `remote.origin.vcs` ⇒ `fetch`/`ls-remote` qua helper phục vụ mirror cũ, `endpoint.khop`=1 ⇒ CẤP nhầm. F11-3 (P3, :110): "thieu khác 0 trong khi mọi điều kiện khác … đạt" không thoả được (chung = mc − thieu) | HINT nhóm 1 (6 hunk): thêm `git config --get-regexp '^remote\.origin\.'` theo danh sách cho phép (2 dòng) và `ai-dang-giu ops/`; bảng tiêu chí; sửa chữ quy tắc chạy lại; đoạn lý do; Giới hạn khai hoa/thường, Unicode, mục ánh xạ, đồng hồ, và chính xác hoá S15; thu hẹp câu "kiểm loại trừ write set của protocol"; §10 ghi phép đo | Kiểm: chuỗi đề xuất trên 32 kịch bản + 9 kịch bản mới: 32 cũ giữ nguyên kết quả, N2 (`ops/`) ⇒ KHÔNG CẤP rc=11, N3 ⇒ KXĐ (remote.cfg 3 dòng); gỡ từng cặp ⇒ chính kịch bản ấy CẤP (đó là kết quả r11). Giới hạn: N2 hoa/thường và dạng ánh xạ vẫn CẤP (khai, mở packet riêng); `GIT_EXEC_PATH`/proxy và S15 không đóng được bằng chuỗi |
| `tuong-tac-677-kiem-ke-t70-chua-neu` | **P2** (VÁ SINH LỖI MỚI; lượt 8, 9, 10, 11) | F11-4 (A8 :706 "tiêu chí nghiệm thu … của phần (i) mà vị từ tĩnh không thấy", §4 :516): ca GỌI THẬT helper qua `globals()` rồi tự bắt `BoQuaNen` (N9), hay gọi trong luồng rồi nuốt `BoQuaNen` (N10) — trái (i), (ii) — qua `t70` 1/1, `t193` 1/1, và cả q1, q2, q3 (N ∅, K ∅, N−D ∅) ở 3.11 lẫn 3.12; A8 "ĐỎ khi … nghĩa vụ ở §4 không được đo là đạt" nên tiêu chí này không kiểm được (i). F11-5 (P3, §4 :510–511 "ca đạt dưới `nt` (như `t199` …)" vs A8 :719 "K là 2 ca (`t199`, `t203` …)"): t199 ∈ K dưới seam; (q3) so BẰNG nên ca nền rời K là báo động giả | HINT nhóm 2 (2 hunk): thêm vế H (`sys.setprofile` + `threading.setprofile`, ca có lời gọi THẬT tới code object hai helper) và (q4) H − D ứng viên = H − D nền; (q3) đổi thành K ứng viên − K nền rỗng; sửa ví dụ t199; ghi phép đo | Kiểm: nền 3.12 có setprofile ⇒ H − D = {t193}, N/K y lượt không profile; N9, N10, M1–M3, M5, N1–N8, R13 ⇒ H − D thêm t204; M7, R11, R12 ⇒ H − D = nền (không báo nhầm); quét đủ cùng lệnh với nền (3.12.3, có setprofile; nền 503,4 s, N9 594,5 s, 12:46:32Z–13:04:51Z): N bằng sổ, N − D rỗng, K bằng nền ⇒ q1, q2, q3 đều ĐẠT; chỉ H − D = {t193, t204} khác nền {t193}. Giới hạn: seam chỉ MÔ PHỎNG `nt`; Windows thật KHÔNG ĐO ĐƯỢC; lời gọi trong tiến trình con không thấy |

0 lớp P3 riêng: hai P3 của lượt 10 đã vá thật; hai biểu hiện mức P3 mới (F11-3, F11-5) thuộc đúng cơ chế của hai lớp P2 nên gộp vào đó.

## BẢNG SĂN

HƯỚNG 1: Đầu vào và phạm vi r10→r11
  giả thuyết : r11 đổi đúng những gì bảng "Thay đổi so với r10" khai; giá trị closure, objective, write set, A1, A4–A7, A9, A10 giữ byte.
  lệnh       : `diff -u SPEC-r10.md SPEC.md | tail -n +3 | sha256sum`; so theo đề mục `## ` và theo hàng bảng (python); `diff` khối A2.
  output     : thân diff tự dựng = thân `r10-r11.diff` (d150b555…); §1, §2, §5, Phụ lục A GIỐNG; 15 hàng (objective, review_class, risk, executor, environment, change_policy_sha, effective_write_set, effective_review_class, required_checks, land_obligations, packet_issue, mission_issue, schema_version, spec_hash, packet_id) GIỐNG; A1, A4–A7, A9, A10 GIỐNG; A2 khác đúng 1 dòng (r7→r8); A3 2 dòng; A8 37 dòng; write set GIỐNG.
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 2: Bộ thử của phiên soạn trên khối r11
  giả thuyết : bảng 32 kịch bản × 3 văn bản và bảng đột biến của §10 tái lập được.
  lệnh       : chép `harness.py`, `kich_ban_r11.py`, `dot_bien_r11.py` sang `do11.LslY/chuoi/`, CHỈ đổi LP/R10 sang bản cùng băm trong $R (dd17b94c…, 892c8006…), dựng `ap/base11.md` bằng `patch -p0 --fuzz=0` HINT lượt 10 (001251f7…, 1319 dòng); `python3.11 kich_ban_r11.py`; `python3.11 dot_bien_r11.py`.
  output     : 12:22:51Z–12:23:40Z, CẤP nhầm r10 17 · HINT 5 (S15 S16 S18 S24 S25) · r11 1 (S15); đột biến 12:24:04Z–12:24:28Z khớp từng dòng §10; 0 .pyc.
  kết luận   : KHÔNG PHẢI LỖI (tái lập). Ghi chú: `r11do/chuoi/ht_tatca.out` là bản trước khi sửa S19 (cột HINT KXĐ), khớp lời khai "S19 chạy lại".

HƯỚNG 3: Bộ thử của lượt 10 trên khối r11, bộ chấm độc lập đọc từng chữ
  giả thuyết : bộ chấm của phiên soạn là cách ĐỌC bảng tiêu chí; một bộ chấm đọc từng chữ có thể ra khác.
  lệnh       : `kich_ban.sh` lượt 10 nguyên byte (2ecdbee1…) + `do11.LslY/l10/chuoi_lib.sh` (nạp nguyên văn lib lượt 10, chạy đúng từng dòng khối r11 trong shell hiện tại, PATH công cụ thêm `wc`) + `cham_r11.py` (chữ | ý).
  output     : 12:45:20Z–12:45:42Z: 0 CẤP nhầm ở cả hai cách đọc trên S0–S10b, S1n, S2n. S4/S5/S8c: đọc-chữ ⇒ "KXĐ (iii|vii dem {may_chu.raw 2, mc 2, chung 1, thieu 1, master 1, master.chung 1})" ngay lần 1; đọc-ý ⇒ chạy lại ⇒ "KHÔNG CẤP (iv) rc=11".
  kết luận   : LỖI mức P3 (F11-3, thuộc lớp `thu-tu-677-…`): quy tắc chạy lại không thoả được theo chữ; fail-close nên không cấp nhầm.

HƯỚNG 4: Đường mới — miền ref của `ai-dang-giu` (nhánh đuôi `/HEAD`)
  giả thuyết : `_cac_ref_cuc_bo` bỏ MỌI ref đuôi `/HEAD` (A9 của chính đặc tả nêu) ⇒ lease còn hạn trên nhánh `x/HEAD` lọt.
  lệnh       : `git check-ref-format refs/heads/claude/HEAD` rc=0; push rc=0; kịch bản N1, N1_head_sau trong `kich_ban_moi.py`.
  output     : r10/HINT/r11 ⇒ `CHAN [12] KHÔNG_XÁC_ĐỊNH: cache thiếu nhánh máy chủ` ⇒ KXĐ; đối chứng nhánh tên thường ⇒ KHÔNG CẤP rc=11.
  kết luận   : KHÔNG PHẢI LỖI (fail-close nhờ phép so tên của chính `ai-dang-giu`; hệ quả chỉ là mất tính sống khi máy chủ có nhánh như vậy).

HƯỚNG 5: Đường mới — phép khớp write set của `ai-dang-giu` so với PROTOCOL §5
  giả thuyết : `_lease_cham_duong` so nguyên chuỗi; §5 cho prefix thư mục, đòi NFC + case-fold.
  lệnh       : quét lease trên 9 nhánh của kho.git (`git ls-tree -r <ref> -- ops/leases` + `yaml.safe_load`); kịch bản N2_prefix, N2_case, N2_doichung, N2_dict.
  output     : 132 cặp (blob, đường dẫn): 233 mục chuỗi chính tắc, 4 mục prefix thư mục (`ops/reviews/doctrine-scan/`, `ops/reviews/wp538/` ×2, `ops/reviews/wp540/`), 40 lease review `write_set` null. N2_prefix (`write_set: [ops/]`, hạn 2026-12-31): 40/40 bước rc=0, `adg.2` chỉ liệt kê `HẾT_HẠN khac-g1-claude` ⇒ `NGƯỜI_GIỮ 0` ⇒ r10/HINT/r11 **CẤP**; N2_case, N2_dict ⇒ **CẤP**; đối chứng exact ⇒ KHÔNG CẤP rc=11.
  kết luận   : LỖI (F11-1, P2): chuỗi CẤP nhầm khi một lease còn hạn giữ hai tệp theo dạng §5 cho phép; câu "Đây là kiểm loại trừ write set của protocol" rộng hơn phép đo.

HƯỚNG 6: Đường mới — chương trình vận chuyển chọn bằng cấu hình kho
  giả thuyết : `git remote get-url --all` in URL, không in helper; `remote.origin.vcs` đưa fetch/ls-remote qua `git-remote-<vcs>`.
  lệnh       : kịch bản N3_vcs (helper `connect` exec `git upload-pack <mirror cũ>`), N3_doichung.
  output     : `endpoint` = đường dẫn máy chủ, `endpoint.khop` 1; máy chủ thật `claude/lease-khac` = 70913817…, `may_chu.raw` = 89fc2033… (mirror); `adg.2` ⇒ `NGƯỜI_GIỮ 0` ⇒ r10/HINT/r11 **CẤP**; đối chứng ⇒ KHÔNG CẤP rc=11.
  kết luận   : LỖI (F11-2): cùng cơ chế "chuỗi kết luận từ thứ nó không ghim". Mức thực tế thấp (cần helper cài sẵn) nhưng đo được rẻ bằng `git config --get-regexp '^remote\.origin\.'`.

HƯỚNG 7: `git diff --quiet` ở (v) có bị textconv cục bộ lừa không
  lệnh       : kho tạm, `.git/info/attributes` `ops/*.py diff=giong`, `diff.giong.textconv=true`; `git diff --quiet A B -- ops/a.py`.
  output     : rc=1 (cả `--exit-code`, `--no-textconv`, `diff-tree --quiet` đều rc=1).
  kết luận   : KHÔNG PHẢI LỖI.

HƯỚNG 8: Lời khai S15 `KHÔNG ĐO ĐƯỢC từ phía client`
  giả thuyết : có tiêu chí chỉ-git nào tách S15 khỏi trạng thái hợp lệ không; kênh thứ hai có đo được không.
  lệnh       : đọc ảnh `thua` của S15 (harness) và suy theo cấu trúc; không có mạng để đo REST.
  output     : S15 để lại đúng một dòng `thua` (nhánh bị giấu, OID cũ) — y hệt nhánh đã xoá trên máy chủ mà `fetch` không prune; `fetch --prune` thì xoá luôn nhánh bị giấu khỏi đệm ⇒ vẫn CẤP. Kênh thứ hai (REST `git/matching-refs/heads/`, MCP) đi qua cùng proxy của container ⇒ chỉ bắt được cắt bớt riêng kênh git. REST trên GitHub thật: KHÔNG ĐO ĐƯỢC ở đây.
  kết luận   : KHÔNG PHẢI LỖI — lời khai đứng với nghĩa "không đo được bằng git"; HINT nhóm 1 chỉ chính xác hoá chữ.

HƯỚNG 9: Chuỗi có đường nào CẤP khi một bước không chạy
  lệnh       : S1n/S2n (bỏ fetch) trên cả hai bộ thử; bộ chấm của phiên soạn (`rc.get(k) not in ("0","BO")`) và của tôi (thiếu bản ghi rc ⇒ KXĐ); bảng đột biến "bốn lớp".
  output     : bỏ fetch ⇒ KXĐ; thiếu rc ⇒ KXĐ; chỉ gỡ cả bốn lớp (rc, dem, command -v, master) mới CẤP. Nhưng bước CHẠY mà không đo đúng thứ nó khai thì có: N2 (`ai-dang-giu` chạy, khớp hẹp), N3 (`fetch`/`ls-remote` chạy, hỏi mirror).
  kết luận   : KHÔNG PHẢI LỖI ở vế "không chạy"; vế "chạy mà đo sai thứ" là F11-1, F11-2.

HƯỚNG 10: A8 — phép quét động đúng chữ có xanh trên nền
  lệnh       : `quet_a8.py` viết ĐỘC LẬP theo văn xuôi A8; clone đủ `163fd5d` từ kho.git; `PATH=bin3xx:$PATH TMPDIR=… PYTHONDONTWRITEBYTECODE=1 python quet_a8.py <gốc>` từ gốc.
  output     : 3.12.3 361,9 s và 3.11.15 311,6 s (song song, 12:35:54Z–12:41:56Z); lượt nền thứ hai 3.11.15 298,8 s (12:46:32Z–12:51:31Z); 3.12.3 có setprofile 503,4 s (12:46:32Z–12:54:56Z). Mọi lượt: 198 ca = 184 đạt + N 12 + K 2; q1 N == SO_BO_QUA đúng cặp; q2 N − D = ∅; K = {t199:TinHieuChotCa, t203:TinHieuChotCa}. Sau lượt: status 0 dòng, 0 .pyc.
  kết luận   : KHÔNG PHẢI LỖI (xanh trên nền, K ổn định qua 4 lượt, 2 bản Python).

HƯỚNG 11: A8 — M1–M7 + tám đường lượt 10 + R11–R13 có đỏ
  lệnh       : `chay_nhanh.sh` (chép biến thể, `--chi-ca=t70_`, `t193_`, `t204_`, quét chỉ t204 có `--h`, trả gốc, kiểm sạch), 3.11.15 và 3.12.3.
  output     : M1–M3, N1–N8 ⇒ t70 1/1, t193 1/1 (N5@3.12 t193 0/1), N−D = {t204}; R13 ⇒ t193 0/1, N−D = {t204}; M5 ⇒ K t204:TinHieuChotCa; M6 ⇒ K t204:AssertionError; M7, R11 ⇒ N ∋ t204, N−D ∅, K ∅; R12 ⇒ N ∅, K ∅ — y lời khai §10, cả hai bản.
  kết luận   : KHÔNG PHẢI LỖI (tái lập).

HƯỚNG 12: A8 — ca gọi helper qua đường lạ rồi TỰ BẮT `BoQuaNen`
  giả thuyết : q1–q3 chỉ thấy kết cục; ca tự bắt kết thúc bằng đạt nên lọt dù trái (i), (ii).
  lệnh       : biến thể N9 (`globals()["_chay_buoc_dang_that"](…)`, `except BoQuaNen: return`), N10 (gọi qua `globals()` trong `threading.Thread`, nuốt `BoQuaNen`), không thêm `mong`/sổ/literal; pha nhanh + quét đủ cùng lệnh với nền.
  output     : pha nhanh, cả 3.11 và 3.12: t70 1/1, t193 1/1, t204 1/1 (posix), N ∅, K ∅, N−D ∅, H−D = {t204}. quét đủ cùng lệnh với nền (3.12.3, có setprofile; nền 503,4 s, N9 594,5 s, 12:46:32Z–13:04:51Z): N bằng sổ, N − D rỗng, K bằng nền ⇒ q1, q2, q3 đều ĐẠT; chỉ H − D = {t193, t204} khác nền {t193}.
  kết luận   : LỖI (F11-4, P2): A8 khai là "tiêu chí nghiệm thu … của phần (i) mà vị từ tĩnh không thấy" nhưng không thấy lớp ca này; vế H đo lời gọi thật bắt được, không báo nhầm trên M7/R11/R12.

HƯỚNG 13: A8 — vế K có báo động giả không
  lệnh       : quét đủ nền rồi M7 (làm đúng) trong MỘT lệnh, 3.11.15; đọc t199, t203, `nem_nt`.
  output     : MỘT lệnh 3.11.15 (12:46:32Z–12:58:22Z): nền 298,8 s, ứng viên M7 410,2 s — M7 199 ca, N = sổ + t204 (q1 đạt), N − D rỗng, K = {t199, t203} = nền ⇒ không báo nhầm; status 0 dòng, 0 .pyc sau khi trả gốc. t199/t203 thuộc K vì seam vá `_ly_do_bo_qua_workflow` mà không vá `os.name` (t203 so `os.name == "nt"`; t199 tự vá `os.name` từng ô). §4 :510–511 lấy t199 làm ví dụ "ca đạt dưới `nt`".
  kết luận   : LỖI mức P3 (F11-5, thuộc lớp `tuong-tac-677-…`): ví dụ mâu thuẫn số đo của chính r11; (q3) so BẰNG nên một ca nền rời K (không phải vi phạm) cũng làm ĐỎ; một ca mới tự vá `os.name` kiểu t199 vào K dù có thể đạt trên Windows thật. Với ứng viên làm đúng (M7): không báo nhầm.

HƯỚNG 14: Lý do không đưa phép quét thành ca test
  lệnh       : đọc `t125` (:4666), `AB_HAN_GIAY` (:58), `t156` (:7030), docstring `t193` (:10614–10625); #687 r3 (`050e6257`, sha256 d4d6715d…543e).
  output     : t125 chạy lại TOÀN suite trong hai tiến trình con dưới trần dẫn xuất, chống đệ quy bằng argv; một ca quét-mọi-ca sẽ chạy lại mọi ca trong mỗi con. Docstring t193 có "phép quét MỌI ca ngoài suite"; #687 r3 có "Phải đo bằng chạy thật, không suy từ tên".
  kết luận   : KHÔNG PHẢI LỖI — lý do (1) có nhãn "suy luận từ cấu trúc, chưa dựng thử" đúng mức; (2)–(4) đứng; "cái giá" khai thẳng.

HƯỚNG 15: Hai P3 lượt 10
  lệnh       : ba lệnh `coord` ở 89fc4fa, 20ec8d5, 163fd5d, a6de9d1, 7e5958e (kho.git, `LC_ALL=C GIT_NO_REPLACE_OBJECTS=1`); kho tạm không có thư mục; `git log --diff-filter=A -- ops/specs/dot-bien-l-bien-cong-khai-r8.md`.
  output     : mỗi mốc `ls-tree` rc=0 4 dòng · `coord.khop` `0` (grep rc=1) · `coord.neo` rc=0 2 dòng; thư mục vắng ⇒ rc=0 0 dòng (tiêu chí "ít nhất 1 dòng" ra KXĐ); rev hỏng rc=128. r8: `f860ab7` 2026-09-29T17:09:42Z, `cat-file -e` 163fd5d rc=128, b7e32e0 rc=0; 118 tệp 163fd5d..a6de9d1, 1 dưới `ops/specs/`; không có r9+.
  kết luận   : ĐÃ VÁ THẬT cả hai.

HƯỚNG 16: Số hạng r11
  lệnh       : `git diff --stat|--quiet 163fd5d 7e5958e -- <2 tệp>`; `git ls-tree` hai rev; `git show <rev>:.github/workflows/ci.yml | grep -n`; tọa độ §4 trên goc.py; bản ghi `r11do/kq/*.jsonl` của phiên soạn; readback Q8/Q10–Q13; bn10.py.
  output     : diff --stat rỗng rc=0, --quiet rc=0; blob 1b4de528…/2eba10ab… ở cả hai rev; ci.yml :574/:590/:630 (163fd5d) → :628/:670/:711 (7e5958e); §4 :3035–3036, :3039–3054, :3057–3073, :569–575, :10613–10744, :10649–10650, :2756–2757, :10869–10870 đúng; 198 ca, 11506 dòng; 419,9 s = lượt `p3 M5 3.12` 12:03:42Z–12:10:43Z (một mình), 687,2 s = lượt `du M7 3.12` 11:38:14Z–11:49:42Z (song song); K 11 (không sys.path) / 2 (có) truy được ở bản ghi; Q-băm khớp; `_thieu` 0/0/1/2/0, mẫu rc 0/1/2.
  kết luận   : KHÔNG PHẢI LỖI. Thời gian quét của tôi (298,8–361,9 s; 503,4 s có setprofile) khác số đặc tả — cùng bậc, phụ thuộc máy.

HƯỚNG 17: #703 (đường nhanh CI) có làm vế `gate-ops` của `required_checks` vắng mặt trên PR thi hành không
  lệnh       : `git show 7e5958e:.github/workflows/ci.yml | sed -n '590,720p'`; `git diff --name-status a6de9d1 7e5958e`.
  output     : bước `lease-publish selftest` chỉ bỏ khi `che_do == 'duong_nhanh'`, tức diff chỉ gồm `ops/{land,leases,reviews,specs}/**`; #703 đổi ci.yml, `.claude/dev/ci_dang_ky_test.py`, thêm `ops/ci_duong_nhanh{,_test}.py`.
  kết luận   : KHÔNG PHẢI LỖI (PR thi hành đổi `ops/lease_publish*.py` nên không vào đường nhanh).

## BẢNG ĐO

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| sha256 SPEC.md / HEAD | fd1138c3… / e48423a2… | fd1138c3… / e48423a2… | có |
| khối lệnh = bộ thử phiên soạn | "chạy đúng khối dưới đây" | 31 dòng, sha256 3241aa33… = `chuoi_r11.txt` (cmp) | có |
| áp HINT lượt 10 lên r10 | rc=0, 11/11, 8 offset (2/15), 1304→1319, 001251f7…755d | y hệt | có |
| cấp nhầm 32 kịch bản | r10 17 · HINT 5 · r11 1 (S15) | 17 · 5 · 1 | có |
| đột biến từng chốt | endpoint/ref/OID/no_replace/công cụ/master/v.ls/nong ⇒ CẤP; bốn lớp | y hệt (30 dòng output) | có |
| 40 bước | 30 dòng + 10 dòng (vii) | 30 dòng không chú thích; (ii) 1 + (iii) 9 = 10 | có |
| r11 là kiểm loại trừ write set của protocol | :40 | `ai-dang-giu` khớp nguyên chuỗi; prefix `ops/`, hoa/thường, mục ánh xạ ⇒ CẤP nhầm | **không** (F11-1) |
| `get-url` là đúng máy chủ được hỏi | :121–124 | `remote.origin.vcs` ⇒ fetch/ls-remote hỏi mirror, URL vẫn qua | **không** (F11-2) |
| quy tắc chạy lại MỘT lần | :110 | đọc chữ không thoả được (S4, S5, S8c) | **không** (F11-3, P3) |
| S15 KHÔNG ĐO ĐƯỢC từ client | :140 | không tách được bằng git; kênh 2 cùng proxy | có (chữ nên hẹp lại) |
| `diff --quiet 163fd5d 7e5958e` | rc=0; stat rỗng | rc=0; rỗng | có |
| blob hai tệp | 1b4de528… / 2eba10ab… | y hệt ở hai rev | có |
| ci.yml | :574/:590/:630 → :628/:670/:711 | y hệt | có |
| `coord` ở 5 mốc | 4 dòng, khớp 0, neo 1 dòng mỗi tệp | y hệt | có |
| #677 r8 | f860ab7 17:09:42Z, #699 b7e32e0, tệp ops/specs duy nhất trong 118 | y hệt | có |
| cổng biên nhận | 0,0,1,2,0; rc 0/1/2 | y hệt | có |
| CLI a6de9d1/7e5958e "0 KHÔNG ĐO ĐƯỢC" | phiên soạn đo với 457 ref | `4bc9432` vắng trong kho.git | KHÔNG ĐO ĐƯỢC |
| A8 nền | N 12 = sổ, N−D ∅, K {t199,t203}, 3.11 + 3.12 | y hệt (4 lượt) | có |
| A8 M1–M6 + 8 đường | bắt hết; M7/R12 không bắt nhầm | y hệt (pha nhanh, 2 bản) | có |
| A8 "tiêu chí nghiệm thu của phần (i) mà vị từ tĩnh không thấy" | :706 | N9, N10 lọt q1–q3 | **không** (F11-4) |
| "ca đạt dưới nt (như t199)" | :510–511 | t199 ∈ K dưới seam (TinHieuChotCa) | **không** (F11-5, P3) |
| thời gian quét | 419,9 s một mình; 687,2 s song song | truy được ở bản ghi phiên soạn; tôi đo 298,8–361,9 s (song song), 503,4 s có setprofile | có (khác máy) |
| tọa độ §4, 198 ca, 11506 dòng | :3035… | y hệt | có |
| Q8, Q10–Q13 trích từng byte | sha256/byte | khớp; mọi dòng không rỗng của dải có mặt | có |
| #687 r3 | d4d6715d…543e, 050e625 | y hệt | có |
| đo live 11:22Z (456 ref, #704 giữ `ops/lease_publish_test.py` tới 2026-10-02T09:55Z) | :40, §8 | không mạng; nhánh `claude/no-ton-677-687` không có trong kho.git | KHÔNG ĐO ĐƯỢC |

## CHI TIẾT TỪNG LỚP

### `thu-tu-677-bo-ngo-o-dieu-kien-cap` — P2 (VÁ SINH LỖI MỚI; lượt 7, 8, 9, 10, 11)

Cơ chế chung r11 tự gọi tên: *chuỗi kết luận từ thứ nó không ghim*. r11 ghim BYTE của công cụ đo (`cong_cu.oid` = `nen.oid`)
nhưng nhận KẾT LUẬN của nó như kết luận của quy tắc protocol; và ghim CHUỖI URL nhưng không ghim chương trình nói với URL.
- F11-1 (P2, có từ r10): `_lease_cham_duong` (`ops/lease_publish.py` :546–549) đòi mục `write_set` là `str` và bằng NGUYÊN CHUỖI
  đường dẫn sau `strip()`/`removeprefix("planned:")`. PROTOCOL :267 "Write set chỉ nhận đường dẫn chính xác hoặc prefix thư mục",
  :270–273 NFC + case-fold; lược đồ §3.2 viết mục write set dạng `{type, path}`. Chính tệp ấy có `_khop_tien_to` (:140–142) khớp
  prefix cho tính lớp review. Master đang có 4 mục prefix. Kịch bản N2 (lease còn hạn `write_set: [ops/]`) ⇒ 40/40 bước rc=0,
  `adg.2` không liệt kê lease ấy ⇒ CẤP ở r10, r10+HINT, r11; tương tự `Ops/Lease_Publish_Test.py` và `{type: prefix, path: ops/}`.
  Hàng `depends_on` gọi năm điều kiện là "kiểm loại trừ write set của protocol" — rộng hơn phép đo.
- F11-2 (có từ r10): `remote.origin.vcs` ⇒ `fetch`, `ls-remote` (cả `ls-remote` bên trong `ai-dang-giu`) đi qua `git-remote-<vcs>`;
  `get-url` vẫn in URL cho phép. Kịch bản N3 CẤP ở cả ba văn bản. Đo được rẻ: liệt kê `remote.origin.*` theo danh sách cho phép.
- F11-3 (P3, r11 sinh): :110 "`thieu` khác 0 trong khi mọi điều kiện khác của (iii) hay (vii) đạt" — `chung` = `mc` − `thieu` nên
  "mọi điều kiện khác" (gồm `mc` = `chung`) kéo theo `thieu` = 0; đọc từng chữ không bao giờ chạy lại. Fail-close.
Phương án (HINT nhóm 1) đã chạy trên chính bộ thử: 32 kịch bản cũ giữ nguyên, N2(`ops/`) ⇒ không cấp, N3 ⇒ KXĐ; phần còn lại
(hoa/thường, Unicode, mục ánh xạ, đồng hồ, `GIT_EXEC_PATH`/proxy, S15) khai làm giới hạn và phát hiện ngoài spec.

### `tuong-tac-677-kiem-ke-t70-chua-neu` — P2 (VÁ SINH LỖI MỚI; lượt 8, 9, 10, 11)

Cơ chế chung r11 tự gọi tên: *kiểm kê tĩnh đo TÊN, không đo KẾT CỤC*. r11 chuyển sang đo KẾT CỤC dưới seam `nt` — nhưng kết cục
không lộ LỜI GỌI khi ca tự bắt `BoQuaNen`.
- F11-4 (P2, r11 sinh lời khai): A8 :706 khai phép quét là "tiêu chí nghiệm thu của (iii), và của phần (i) mà vị từ tĩnh không
  thấy"; A8 "ĐỎ khi … nghĩa vụ ở §4 không được đo là đạt". N9/N10 trái (i) (không tham chiếu cấp đỉnh) và (ii) (không có trong
  `mong`), qua t70, t193 và cả q1–q3 ở 3.11 lẫn 3.12 ⇒ nghĩa vụ (i) không kiểm được bằng tiêu chí đã khai. Hệ quả: chốt kiểm kê
  của #677 (`t70`, "matrix có Windows phải chạy lại bảy ca") bị đi vòng. Vế H (`sys.setprofile` + `threading.setprofile` theo
  code object của hai helper) bắt N9/N10/M5 và mọi đường lạ, nền H − D = {t193}, không báo nhầm M7/R11/R12.
- F11-5 (P3): §4 :510–511 lấy t199 làm ví dụ "ca đạt dưới `nt`", trong khi A8 :719 và số đo cho t199 ∈ K dưới seam. (q3) so BẰNG nên
  ca nền rời K (không vi phạm (iii)) làm ĐỎ; nên so "K ứng viên − K nền rỗng".

## DRY-RUN HINT.patch

`$R/goi/HINT.patch`: sha256 `cbc398ef304cccad2021c956e1e576a7afab4546095828d6234deffde0298de4`, 62018 byte, 2 nhóm (`# lop: thu-tu-677-bo-ngo-o-dieu-kien-cap` 6 hunk · `# lop: tuong-tac-677-kiem-ke-t70-chua-neu` 2 hunk), mỗi nhóm là diff riêng so với r11 gốc; sinh bằng `do11.LslY/hint/sinh_hint.py` (thay chuỗi có `assert count == 1`).
Lệnh (đúng PROMPT): `T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"; cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"`.
- dry-run: rc=0; 8/8 hunk (nhóm 1: 6, nhóm 2: 2); không fuzz, không reject.
- áp thật trên cùng bản sao: rc=0; nhóm 2 báo offset 26 dòng; 0 tệp `.rej`/`.orig`; kết quả 1614 → 1666 dòng, sha256 bda2f35f…,
  khớp từng byte bản kỳ vọng dựng độc lập (`do11.LslY/hint/HINT.ky_vong.md`).
- áp riêng từng nhóm lên bản sao r11 mới: nhóm 1 rc=0, nhóm 2 rc=0.
- dòng lệnh mới mang đúng 2 dấu chéo ngược (`'^remote\.origin\.'`), đo bằng `repr()` sau khi ghi.
- khối lệnh trích từ bản đã áp chạy lại 41 kịch bản (HƯỚNG 5, 6; 13:00:15Z–13:01:12Z): 32 kịch bản cũ giữ kết quả r11; N2 (`ops/`)
  ⇒ KHÔNG CẤP rc=11; N3 ⇒ KXĐ; N2 hoa/thường, N2 ánh xạ, S15 ⇒ CẤP (giới hạn mà HINT khai).

## GIỚI HẠN VÀ TOÀN VẸN
- Không mạng: chuỗi chạy thật 11:22Z, 456 ref, lease #704, REST (S15 kênh hai) — KHÔNG ĐO ĐƯỢC. kho.git chỉ 9 nhánh: phép đếm
  dạng write set (132 cặp) là của 9 nhánh ấy, không phải toàn máy chủ; `4bc9432` vắng nên vế CLI "0 KHÔNG ĐO ĐƯỢC" ở a6de9d1/7e5958e
  KHÔNG ĐO ĐƯỢC.
- Seam `nt` chỉ MÔ PHỎNG; Windows thật KHÔNG ĐO ĐƯỢC. Vế H đề xuất không thấy lời gọi trong tiến trình con; H − D nền đo ở 3.12.3
  (lượt đủ); ở 3.11 chỉ đo t204 (pha nhanh).
- Biến thể M*, N1–N8, R* chép (chỉ đọc) từ scratch chung của phiên soạn (`r11do/bt/`), lệch goc.py 5–16 dòng mỗi tệp; N9, N10 do tôi
  dựng. Bộ thử chuỗi: harness phiên soạn (đổi đúng 2 đường dẫn) + kịch bản mới của tôi; lớp phủ cho bộ thử lượt 10 và bộ chấm
  đọc-chữ là diễn giải của tôi về bảng tiêu chí.
- Lỗi đo của chính tôi, ghi để không đọc nhầm: lượt đầu bộ thử lượt 10 (12:45:00Z) ra ô RỖNG vì `KHOI` nở theo `W` mới trong cùng
  dòng gán — chạy lại 12:45:20Z với đường dẫn tuyệt đối; ô rỗng không phải kết quả.
- Thời gian quét của tôi (298,8–361,9 s không profile, song song; 503,4 và 594,5 s có setprofile) khác số đặc tả — cùng bậc, phụ thuộc máy.
- Toàn vẹn: `cay-kho` HEAD e48423a2…, `status --porcelain --ignored` 0 dòng; `r11do/` không đổi (harness.py a6e3affb…); không ghi ngoài
  `$R/goi/` và thư mục mktemp; không commit/push/đăng; không in biến môi trường hay bí mật.
