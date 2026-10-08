verdict: changes_requested
reviewed_sha: f958e147754bed8e9e7034dd28450681f19c3db0
spec_sha256: f173e7cf2f132dacdf34d9ab00cc966a5a7d5705baffcc585d577beed5ee5a3b
model/effort tự khai: Claude Opus 5.5 (`claude-opus-5-5`), effort max — KHÔNG phải codex. Chạy như SUBAGENT do phiên
điều phối giao (lượt 8), tức đúng đường mà r8 tuyên bố bỏ cho lượt review THI HÀNH. Lời khai model/effort là CẤU HÌNH được
giao, không phải runtime evidence (PROTOCOL :710–711): lượt này không sinh `modelUsage`, không có `session_run_id`. Biên
nhận của lượt (nếu ghi) phải tự khai `che_do: subagent_trong_phien_dieu_phoi`, mức `review_deferred`. Cùng họ Claude với
phiên soạn r8 ⇒ KHÔNG độc lập khác họ. Không sửa `cay-kho` tại chỗ, không mạng, không đăng GitHub, không commit/push; ghi
chỉ dưới `$R/goi/` và các thư mục `mktemp -d -p "$R"`. Lượt này không gọi `claude` THẬT (CLI cần mạng): mọi phép đo đường
`claude -p` dùng một `claude` GIẢ hoặc quét chuỗi tĩnh của nhị phân, và được ghi đúng nhãn ấy.

Kết luận nội dung: **0 P1 / 4 P2 / 3 P3** (theo lớp; 10 finding F8-1…F8-10).
P2: `hop-dong-dong-bang-thieu-neo` (VÁ SINH LỖI MỚI) · `dong-reviewer-loi-khai-rong-hon-do` (TÁI PHÁT, nâng từ P3) ·
`duong-review-b-chua-do-dau-cuoi` (MỚI) · `thu-tu-677-bo-ngo-o-dieu-kien-cap` (CÒN MỞ phần tổng quát).
P3: `q10-he-qua-mat-nhan-dien-giai` (TÁI PHÁT) · `so-do-nen-khong-khop` (TÁI PHÁT) · `tuong-tac-677-kiem-ke-t70-chua-neu` (MỚI).

Trả lời câu hỏi gốc. (1) r8 đổi ĐÚNG phạm vi nó khai: 5 giá trị closure, `objective`, `executor`, `environment`, §1, §2,
§5, Phụ lục A giống từng byte r7; §4/§6 mỗi mục một dòng tọa độ; §7 chỉ đổi số đo/tọa độ (Hướng 1). (2) Dời nền sang
`20ec8d5` đo lại KHỚP mọi con số (600/15 ba phạm vi; 18 hàm thêm, 2 đổi thân; suite 195/195 và 187/187 dựng hai vế một lệnh;
ruff 9 lỗi F như nhau ở hai vế; A1, A3 tái lập) và A1–A10 còn đúng nghĩa sau #677 — kèm một kiểm kê `t70` r8 bỏ sót (P3). (3) Phương án B KHÔNG
vượt quyền (closure byte-identical, chặt hơn đường r7, trong phạm vi Q10, thất bại thì dừng hỏi chủ kho) và **không phải
quyết định của chủ kho** — r8 không nói thẳng điều này (P3). Nhưng B được đóng băng thành tiêu chí trước khi chạy thử một
lượt qua launcher, nên: tiêu chí (b) trỏ vào `run.json` vốn không lưu argv (đo); `session_run_id` = `run_id` launcher không
đo độc lập (validator nhận mọi chuỗi, đo); và đúng dạng lệnh r8 bắt buộc bị chốt trust của launcher chặn ở sandbox mới (đo
`CHAN [15]`). (4) Làm đúng từng chữ r8 thì packet KHÔNG land sai, nhưng lượt review thi hành chắc chắn dừng lại hỏi chủ kho
(trust/quyền), và đọc nghiêm (b) thì vế review không bao giờ đạt nếu không ra revision mới — nên 0 P1, các lớp ấy P2.

## TIỀN KIỂM
- `sha256sum $R/SPEC.md` ⇒ `f173e7cf…5a3b` (khớp) · `git -C $R/cay-kho rev-parse HEAD` ⇒ `f958e147…db0` (khớp) ⇒ không `blocked`.
- `cmp SPEC.md cay-kho/ops/specs/lease-id-ep-kieu-yaml-r8.md` khớp; `cmp SPEC-r7.md …-r7.md` khớp; `core.abbrev` = 7.
- `luot7/VERDICT.md` `992eb9f0…794c`, `luot7/HINT.patch` `72289e06…b445` (khớp PROMPT).
- `r7-r8.diff` = `diff -u SPEC-r7.md SPEC.md` (bỏ 2 dòng tiêu đề: sha256 hai bên `52074386…4693`).
- Commit r8: `git diff --numstat 088511f f958e14` ⇒ `890 0 ops/specs/lease-id-ep-kieu-yaml-r8.md` (chỉ thêm đúng tệp ấy);
  cha `088511f`, cha của nó `423b4ba` (nhánh spec rẽ từ `423b4ba`, nền nghiệm thu r8 là `20ec8d5` — khai đúng ở PROMPT/r8).
- PROMPT nhắc mà `$R` KHÔNG có: `luot6/`, `q10-readback.json`, `r6-r7.diff` (`ls`: No such file) — phần ấy của PROMPT là của
  lượt 7; lượt này đối chiếu r7→r8. Thay thế có: `readback-5911243074.json` (Q10), `-5912559230` (Q11), `-5888631719` (Q8).
- Object VẮNG khỏi `kho.git` (`rev-parse --verify`): `6112b89`, `35e23d7` ⇒ mọi lời khai về hai commit ấy: KHÔNG ĐO ĐƯỢC.
  Có mặt: `89fc4fa 423b4ba 20ec8d5 8e630c0 3c308b3 adad5f5 11f73ac fc852ff 44620e8 088511f 03a7219 1741e0a 85124dc`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 7 (Claude Opus 5.5 max, subagent, trên `088511f`): 0 P1 / 2 P2 / 3 P3, năm lớp. Đối chiếu từng finding trên r8:

| lớp (lượt 7) | finding lượt 7 | trạng thái trên r8 | bằng chứng tự đo |
|---|---|---|---|
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` (P2) | F7-1(i) nguồn thứ tự yếu hơn master | ĐÃ VÁ THẬT | r8 §10 dẫn đặc tả #677 r7 (`44620e8`, tổ tiên `20ec8d5`) và Q11; Q11 13/13 dòng khớp từng byte thân REST |
| | F7-1(ii) "không phải điều kiện Q8" chưa đo | ĐÃ VÁ THẬT | thân Q8: sha256 `3a8c40a6…c45e`, 1187 byte, chuỗi `677` xuất hiện **0** lần (khớp r8) |
| | F7-1(iii) điều kiện dời nền bất đối xứng | phần #677 ĐÃ VÁ (điều kiện (5), nền `20ec8d5`); **phần tổng quát CHƯA VÁ** ⇒ lớp **CÒN MỞ** | (4) vẫn chỉ nêu #687, (5) chỉ #677; "Nền tiếp nối … không thay nền này" (Hướng 10). Tự phê: HINT nhóm 1 của lượt 7 tự nó hẹp (chỉ thêm #677) — đúng hình dạng *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"* |
| `hop-dong-dong-bang-thieu-neo` (P2, tái mở) | F7-2 model/effort của lượt thi hành không đo được; định nghĩa ngoài băm | model: ĐÃ VÁ (modelUsage, vị từ phân biệt hai chiều); định nghĩa: ĐÃ VÁ (điều kiện (d), băm khớp); effort: khai `KHONG_do_duoc` đúng — nhưng neo mới của (b) trỏ vào hiện vật không chứa argv (F8-1), và điều kiện (3) cho review đặc tả vẫn neo "Opus 5.5 max" vào đường không đo được (F8-2) ⇒ **VÁ SINH LỖI MỚI** | Hướng 3, 8 |
| `q10-he-qua-mat-nhan-dien-giai` (P3) | F7-3 đoạn "Hệ quả" Q10 mất nhãn | biểu hiện Q10 ĐÃ VÁ THẬT (r8 :228–229 có nhãn); biểu hiện mới cùng cơ chế ở `nguon_cap_viec` (Q11) ⇒ **TÁI PHÁT** | Hướng 3, 4 |
| `dong-reviewer-loi-khai-rong-hon-do` (P3) | F7-4a "phiên mới" cho subagent | đường subagent bỏ, nhưng câu "phiên và context mới" tái xuất cho `claude -p`, trái chính phép dò của r8 ⇒ **TÁI PHÁT** | Hướng 9 |
| | F7-4b "validator bác" vô điều kiện | ĐÃ VÁ THẬT | r8 nêu "Validator không tự phát hiện subagent…"; validator G4/G5 khớp |
| | F7-4c "§8.1 dành advisory_review cho ChatGPT Web" | ĐÃ VÁ THẬT | câu đúng :715–716 |
| | (mới, cùng lớp) | `session_run_id`=`run_id` không đo độc lập (F8-4); tiền lệ dẫn sai tệp (F8-5) ⇒ nâng **P2** | Hướng 2, 9 |
| `so-do-nen-khong-khop` (P3) | F7-5a §8 "Ref." thiếu nhãn r6 | ĐÃ VÁ THẬT | r8 :534–536 gắn nhãn r8/r7/r6 |
| | F7-5b §10 lý do r6 cho băm #682 | ĐÃ VÁ THẬT | r8 :708–710 |
| | (mới) | §9 "Nhóm 1, 3, 4, 5 … 6/6 hunk" mà bốn nhóm ấy là 5 hunk (F8-9) ⇒ **TÁI PHÁT** | Hướng 7 |

Tín hiệu hội tụ §12 (:1043–1056): U (lớp mở cuối lượt 7) = 5; F (lớp ĐÃ VÁ THẬT theo §8.3) = 0 ⇒ tỷ lệ **0/5 = 0%**. Nếu
người điều phối bác việc nối F8-9 vào `so-do-nen-khong-khop` thì F = 1 ⇒ 20%; cả hai đều < 50%. Chuyển tiếp trước (6→7) là
`N/A` (U rỗng), nên đây là tỷ lệ xác định ĐẦU TIÊN; chuyển tiếp 8→9 cũng < 50% ⇒ dừng vòng vá, Review Rescue Checkpoint.
Lớp mới ở lượt 8: 2 (`duong-review-b-chua-do-dau-cuoi`, `tuong-tac-677-kiem-ke-t70-chua-neu`).
`hop-dong-dong-bang-thieu-neo` nay có mặt ở lượt **1, 2, 7, 8** — bốn lượt. §12 :1054–1056 đòi xét lại cách làm **tại
checkpoint**; r8 đã đổi cách (B) nhưng không qua checkpoint nào và không chạy thử, và lớp lại hiện. Khuyến nghị (không phải
finding): trước r9, đưa câu "lượt review thi hành chạy bằng đường nào" lên chủ kho — B cần chủ kho quyết trust/quyền đằng nào
cũng phải hỏi (lớp `duong-review-b-chua-do-dau-cuoi`); A (subagent, `review_deferred`, nhãn trung thực) thì không đạt
`same_provider_approved`. Hỏi lúc soạn rẻ hơn hỏi giữa lượt review khi lease đang chạy.

## BẢNG LỚP

| slug lớp | hạng | biểu hiện | phương án | phép kiểm / giới hạn |
|---|---|---|---|---|
| `hop-dong-dong-bang-thieu-neo` | **P2** | F8-1: tiêu chí (b) đòi "argv có `--effort max` đọc từ `run.json`", mà `run.json` CỐ Ý không lưu argv (`_tom_tat_lenh`: chỉ `chuong_trinh`, `so_doi_so`, `van_tay`) — đo bằng launcher thật + `claude` giả: không chuỗi `--effort`/`--model`/`max` nào; tiền lệ `pr492-review-4` cũng ghi effort là "ATTESTATION … KHÔNG ĐO ĐƯỢC từ các JSON kèm". F8-2 (mức P3): điều kiện (3) "review sạch bằng lượt Opus 5.5 `max`" — đường đang dùng cho review ĐẶC TẢ (subagent, chính lượt 8) không đo được model, r8 không nói (3) kiểm thế nào | HINT nhóm `hop-dong-dong-bang-thieu-neo` (2 hunk): (b) neo vào phép tính lại `van_tay` từ argv nguyên văn trong biên nhận; ghi chú Q10: (3) với lượt subagent ⇒ `review_deferred`, model/effort là cấu hình, nguồn đo `KHONG_do_duoc` | Kiểm: biên nhận có argv, `van_tay` tính lại = `run.json`; đã đo hai chiều (`max` khớp, `high` lệch). Giới hạn: effort THỰC TẾ vẫn KHÔNG ĐO ĐƯỢC; `van_tay` 64 bit; phương án (3) khác (bắt cả review đặc tả đi đường B) thuộc quyền người điều phối/chủ kho |
| `dong-reviewer-loi-khai-rong-hon-do` | **P2** (nâng từ P3) | F8-3: "Tiến trình `claude -p` là phiên và context mới" — trái phép dò của chính r8 (`session_id` = `CLAUDE_CODE_SESSION_ID` phiên gọi) và trái quét tĩnh nhị phân `claude` (tiến trình con nhận `CLAUDE_CODE_SESSION_ID` của cha + `CLAUDE_CODE_CHILD_SESSION=1`). F8-4: `session_run_id` := `run_id` launcher là thứ validator đọc làm "BẰNG CHỨNG ĐỘC LẬP TƯỜNG MINH" (:694–710), nhưng validator nhận MỌI chuỗi (đo: session ID của chính phiên điều phối, hay `'x'`, đều 0 lỗi); r8 không quy định ai phóng lượt, không đòi so với session executor ⇒ `same_provider_approved` (§8 mục 3 "không fork context Executor") được ghi mà không phép đo nào chạm tính độc lập. F8-5: tiền lệ dẫn `don-nhanh-base-review-7` có 0 `session_run_id`, 0 `modelUsage`, schema 1; tiền lệ đúng là `pr492-review-4` | HINT nhóm `dong-reviewer-loi-khai-rong-hon-do` (2 hunk): sửa câu "phiên mới"; tiền lệ đúng; thêm vào (c): phiên phóng ≠ phiên executor, ghi `session_id` của lượt + `CLAUDE_CODE_SESSION_ID` của phiên phóng, so với session ID executor trong handoff (PROTOCOL :710) | Kiểm: ba giá trị có trong biên nhận và khác session executor. Giới hạn: tiến trình con có dùng chung context với phiên gọi không — KHÔNG ĐO ĐƯỢC (cần gọi API); phép kiểm đề xuất đo độc lập với EXECUTOR, không với phiên điều phối |
| `duong-review-b-chua-do-dau-cuoi` | **P2** (MỚI) | F8-6: đúng dạng r8 bắt buộc (`launcher.py run … -- claude -p …`, không `--bo-qua-probe`, sandbox clone mới ngoài kho) bị probe `claude_trust` của launcher chặn: đo `CHAN [15]: probe nang luc khong dat: claude_trust=KHONG_DO_DUOC`, rc=15 (HOME không khoá trust); có khoá trust đúng đường dẫn ⇒ rc=0. PROTOCOL :706 cấm tự chấp nhận trust/đổi quyền để làm probe xanh (r8 tự dẫn :706–707). Phiên headless chưa trust còn bỏ `permissions.allow` (adapter `cross-review/SKILL.md` :248–250) ⇒ `permission_denials` khó rỗng. Tiền lệ `same_provider_approved` duy nhất qua launcher (`pr492-review-4`) có `run.json` ở lớp `local_process` (lệnh sau `--` không tên `claude`) ⇒ probe trust không áp cho nó. §10 r8 không liệt kê chốt này dù đọc được từ mã (`68d1867`, 23-08) | HINT nhóm `duong-review-b-chua-do-dau-cuoi` (2 hunk): ghi chú bootstrap trust/quyền dưới closure — chủ kho quyết TRƯỚC lượt, `run.json` phải ghi `probe.claude_trust.trang_thai: DAT`, cấm bọc để né probe; §10 ghi phép đo và đòi một lượt khói thật qua launcher trước khi đóng băng | Kiểm: `run.json.probe.claude_trust` = `DAT` + quyết định chủ kho trong biên nhận. Giới hạn: hành vi `claude -p` thật (trust, quyền công cụ ở `-p`, trôi model giữa lượt) KHÔNG ĐO ĐƯỢC ở đây (không mạng) |
| `thu-tu-677-bo-ngo-o-dieu-kien-cap` | **P2** (CÒN MỞ) | F8-7: điều kiện dời nền chỉ kích hoạt theo TÊN (#687 ở (4), #677 ở (5)); hàng nền nghiệm thu còn nói "Nền tiếp nối, nếu khác, phải được khai riêng lúc cấp lease, không thay nền này" ⇒ một packet THỨ BA land thay đổi `ops/lease_publish*.py` rồi nhả lease thì (1)–(5) đều qua và lease được cấp trên nền cũ — đúng điều "không cấp trên nền cũ" mà (4) sinh ra để chặn. Write set này là điểm nóng: trên `20ec8d5`, 23 tệp lease khai giữ ít nhất một trong hai tệp, thuộc 8 packet khác nhau, chưa kể #677/#687. r8 §10 khai lớp "đóng theo Q11" | HINT nhóm `thu-tu-677-bo-ngo-o-dieu-kien-cap` (2 hunk): (4) thêm phần tổng quát hoá đo được (`git diff --quiet <nền> origin/master -- <hai tệp>`: 0 cấp được, 1 dời nền, khác ⇒ không cấp); hàng nền nghiệm thu khớp theo; §10 tách phần đã đóng/phần đóng bằng (4) | Kiểm: lệnh trên rc=0 lúc cấp. Chặt hơn Q8, không nới. Giới hạn: packet nào đang/sẽ đổi write set — KHÔNG ĐO ĐƯỢC (mạng) |
| `q10-he-qua-mat-nhan-dien-giai` | P3 (TÁI PHÁT) | F8-8: `nguon_cap_viec` viết r8 "áp HINT lượt 7 trong một lần" như hệ quả quyết định Q11 — cụm ấy chỉ có trong đoạn "Hệ quả" mà chính comment Q11 gắn nhãn "diễn giải của phiên agent", và r8 KHÔNG áp nhóm 2 như viết (§9). Thẩm quyền của B không được nêu: B không có trong lựa chọn của Q10 hay Q11 | HINT nhóm `q10-he-qua-mat-nhan-dien-giai` (1 hunk): tách lựa chọn chủ kho khỏi diễn giải; nói thẳng B là lựa chọn của phiên soạn r8 trong phạm vi Q10, không phải quyết định chủ kho | Kiểm: dòng `nguon_cap_viec` |
| `so-do-nen-khong-khop` | P3 (TÁI PHÁT) | F8-9: §9 "Nhóm 1, 3, 4, 5 áp nguyên văn (`patch -p0 --fuzz=0`, rc=0, **6/6** hunk)" — bốn nhóm ấy là **5** hunk (đếm `@@` theo `# lop:` của `luot7/HINT.patch`: 1+1+1+2); áp CẢ HINT lên r7 mới ra 6/6 (đo, rc=0) | HINT nhóm `so-do-nen-khong-khop` (1 hunk): ghi đúng "5 trong 6 hunk" và tách phép áp cả HINT | Kiểm: đếm hunk. Lệnh thật của phiên soạn: KHÔNG ĐO ĐƯỢC |
| `tuong-tac-677-kiem-ke-t70-chua-neu` | P3 (MỚI) | F8-10: tọa độ r8 của tương tác #677 liệt kê `t195`–`t202` mà bỏ `t70` (:2995, M6 của #677) — nó ghim một tập LITERAL các ca nhắc `_chay_buoc_dang`/`_chay_buoc_dang_that`. A3 bắt "dùng lại bộ trích sẵn có" ⇒ ca A3 mới làm `t70` ĐỎ (đo trên bản sao `20ec8d5`: thêm một ca gọi helper ⇒ `t70` `0/1`; cây gốc `1/1`), trái A8 nếu executor không biết cập nhật | HINT nhóm `tuong-tac-677-kiem-ke-t70-chua-neu` (1 hunk) | Kiểm: `t70` xanh trên ứng viên, tên ca A3 trong `mong` |

## BẢNG SĂN

Thư mục đo (đều `mktemp -d -p "$R"`): `do.rdwd` (trích tệp hai nền, `r7r8.re.diff`), `lch.MJCe` (launcher + `claude` giả),
`suite.9Cnb` (suite hai vế), `a13.fISi` (clone `20ec8d5`: A1/A3, validator), `t70.sh9R` (đột biến kiểm kê `t70`),
`lz.XA7J` (lease trên master), `hint7.HkKR` (áp HINT lượt 7 lên r7), `hint8.6iOC` (bộ sinh HINT, `ky_vong.md`),
`apthat.2mVw` (áp thật + áp từng nhóm), `tmp.AYZPgcpjyR` và `tmp.MPm0JIMpN4` (hai lần dry-run; lần cuối trên tệp ở `goi/`).
Công cụ: Python 3.11.15, PyYAML 6.0.1, git 2.43.0, shellcheck 0.9.0, actionlint 1.7.7, ruff 0.15.8 (nhị phân; `python -m
ruff` vắng), GNU patch 2.7.6. Mười một hướng: 7 gợi ý (đã dời sang r7→r8) + 4 tự thêm (8–11).

```
HƯỚNG 1: Phạm vi thay đổi r7 → r8
  giả thuyết : r8 đổi lén byte kỹ thuật (A*, write set, closure) ngoài phạm vi nó khai.
  lệnh       : diff -u SPEC-r7.md SPEC.md (== r7-r8.diff); python: tách theo "## ", so từng mục; tách hàng bảng "| k | v |".
  output     : GIỐNG byte: §1, §2, §5, Phụ lục A. KHÁC: §3 (-4 +36 dòng), §4 (-1 +1: tên tệp tự tham chiếu), §6 (-1 +1:
               tọa độ t178), §7 (-8 +24: số đo/tọa độ A1, A2, A3, A8, A9), §8 (-13 +28), §9 (+9), §10 (-9 +41).
               Hàng GIỐNG byte: schema_version, packet_id, packet_issue, objective, review_class, risk, executor, environment,
               spec_hash, change_policy_sha, effective_write_set, effective_review_class, required_checks, land_obligations.
               Hàng KHÁC: revision, thay_the_cho, mission_issue, nguon_cap_viec, reviewer, depends_on, nền nghiệm thu.
               Áp HINT lượt 7 lên r7 (patch rc=0, 6 hunk) rồi so với r8: numstat 183/61 — phần dư là B, Q11, số đo nền mới.
  kết luận   : KHÔNG PHẢI LỖI — r8 chỉ đổi đúng những gì bảng đầu tệp khai.
```

```
HƯỚNG 2: Mức assurance và validator
  giả thuyết : (a) mức r8 khai lệch `_thieu`; (b) `session_run_id` = `run_id` launcher là bằng chứng độc lập thật.
  lệnh       : clone 20ec8d5 (a13.fISi), nạp ops/bien_nhan_v2.py, `_thieu` trên biên nhận THẬT pr492-review-4 và đột biến
               (PROVIDER_NGUON_HONG = None; bien_nhan_v2 giống hệt 423b4ba..20ec8d5, `git diff --quiet` rc=0).
  output     : G0 nguyên bản (same_provider_approved, session_run_id launcher)          ⇒ 0 lỗi
               G1 session_run_id = session ID của chính phiên điều phối (chuỗi công khai ở thân Q11) ⇒ 0 lỗi
               G2 session_run_id = 'x'                                                    ⇒ 0 lỗi
               G3 bỏ session_run_id, không phien_doc_lap                                  ⇒ 2 lỗi
               G4 thêm che_do: subagent_trong_phien_dieu_phoi                             ⇒ 1 lỗi ("tự khai chạy trong phiên điều phối")
               G5 G4 + assurance review_deferred                                          ⇒ 0 lỗi
               G6 mô hình khai human_audited                                              ⇒ 1 lỗi
               Số dòng r8 dẫn: PROTOCOL :562, :565–567, :568, :652, :658, :662–663, :681–682, :706–707, :710–716, :714–715,
               :718–721; bien_nhan_v2 :703, :709–726, :725, :734–737, :793–796 — ĐÚNG nội dung r8 gán.
  kết luận   : (a) KHÔNG PHẢI LỖI. (b) LỖI P2 (F8-4, lớp dong-reviewer-loi-khai-rong-hon-do): validator chỉ đòi CÓ MẶT
               một chuỗi; tính độc lập phải do tiêu chí của đặc tả đo, r8 không có tiêu chí ấy.
```

```
HƯỚNG 3: Closure, phương án B, thẩm quyền, tiêu chí (a)–(e)
  giả thuyết : B vượt quyền phiên soạn; (a)–(e) không đo được thật.
  lệnh       : so hàng closure r7/r8 (Hướng 1); đọc thân Q10, Q11 (readback), PROTOCOL :587, :1054–1056, ADR-0037;
               chon_reviewer.kiem_ket_qua trên JSON tổng hợp; sha256 ~/.claude/agents/review-opus-max.md (CHỈ ĐỌC, không in thân).
  output     : 5 giá trị closure GIỐNG byte. Lựa chọn Q10: "chỉ đổi reviewer/required_checks sang Opus 5.5 max, hạ assurance
               tương ứng vì cùng họ" — không nêu cơ chế chạy. Lựa chọn Q11: không nhắc reviewer. Cụm "áp HINT lượt 7" chỉ ở
               đoạn "Hệ quả" mang nhãn diễn giải. ⇒ B là lựa chọn của phiên soạn r8, KHÔNG phải quyết định chủ kho.
               PROTOCOL :587 "Dispatcher … quyết định fallback/reroute"; miễn trừ #682 cho đổi closure bằng revision mới.
               (a) kiem_ket_qua: opus+haiku đòi opus ⇒ ĐẠT; đòi sonnet ⇒ KhongDoDuoc; opus+sonnet ⇒ KhongDoDuoc "mô hình LẠ";
                   thiếu modelUsage ⇒ KhongDoDuoc; is_error true ⇒ KhongDoDuoc (JSON tổng hợp; JSON thật của phép dò 01:07Z vắng).
               (b) run.json không lưu argv — Hướng 8. (c) session_run_id — Hướng 2, 9; trust/quyền — Hướng 8.
               (d) định nghĩa: sha256 e225b81cf2fb…b792c, 1175 byte, mtime 2026-09-29T23:07:37Z, frontmatter model
                   claude-opus-5-5, effort max, tools Read, Write, Edit, Bash, Grep, Glob (KHỚP r8). (e) quyết định được.
               Ghi nhận (không phải lớp): chon_reviewer.chon cho packet này chọn claude-fable-5 (xhigh ở lượt 1, max từ lượt 3),
               và kiem_dinh_danh("claude-opus-5-5","max") ném "model ngoài allow-list"; nhưng không luật nào bắt dùng bộ
               chọn ấy (grep: chỉ adapter/CLAUDE.md/spec nhắc), Q10 chọn đích danh Opus 5.5, và (a) chỉ gọi kiem_ket_qua.
  kết luận   : thẩm quyền: KHÔNG PHẢI LỖI (không đổi giá trị closure, chặt hơn đường r7, trong phạm vi Q10, thất bại ⇒ hỏi chủ
               kho). Nhãn thẩm quyền: LỖI P3 (F8-8). (a), (d), (e): KHÔNG PHẢI LỖI. (b): LỖI P2 (F8-1). (c): LỖI P2 (F8-4, F8-6).
```

```
HƯỚNG 4: Nguyên văn Q10, Q11, Q8 (readback REST trong $R)
  lệnh       : python: body.encode('utf-8') ⇒ sha256, số byte, đếm thực thể HTML; so từng dòng trích (bỏ tiền tố "  >").
  output     : Q11 5912559230: sha256 392069d1…8106, 1741 byte, 0 thực thể, tạo 2026-09-30T13:44:59Z, app `claude`,
               OWNER; r8 :241–253 = thân dòng 5–17: 13/13 khớp từng byte (kể cả nhãn "Hệ quả").
               Q10 5911243074: sha256 69cc35b1…2d2f, 2151 byte, 0 thực thể; r8 :221–226 = khối liên tục tại thân dòng 7–12.
               Q8 5888631719: sha256 3a8c40a6…c45e, 1187 byte, 0 thực thể, app `claude`; điều kiện 2, 3 viết "cross-review";
               "677" xuất hiện 0 lần.
               #682 (thân issue): KHÔNG có trong $R và không bản chép nào trong kho (`git grep` ba cụm ⇒ 0) ⇒ "hai dòng chép
               từng byte từ dòng 29 và 31", sha256 76bee6fb…, 3416 byte: KHÔNG ĐO ĐƯỢC.
  kết luận   : KHÔNG PHẢI LỖI ở mọi phần đo được.
```

```
HƯỚNG 5: Phép đo lúc soạn — dời nền (kho.git, offline)
  lệnh + output (G = git -C $R/kho.git):
   G diff --quiet 89fc4fa 20ec8d5 -- ops/lease_publish.py ⇒ rc=0; blob sha256 dd17b94c…4f83 cả hai, 2206 dòng cả hai  KHỚP
   G diff --numstat {89fc4fa,fc852ff,423b4ba} 20ec8d5 -- ops/lease_publish_test.py ⇒ 600 15 (ba lần)                 KHỚP
   G merge-base --is-ancestor {89fc4fa,8e630c0,fc852ff,423b4ba} 20ec8d5 ⇒ rc=0 (bốn lần)                             KHỚP
   G diff --numstat 423b4ba...8e630c0 -- …test.py ⇒ 596 15; merge-base = 423b4ba                                      KHỚP
   G log 423b4ba..20ec8d5 -- …test.py ⇒ đúng 9 commit test(#677), 11f73ac … adad5f5; sau 8e630c0: 3c308b3, adad5f5     KHỚP
   ast trên hai nền: THÊM 18 hàm (8 ca t195–t202 + 10 phụ, có _chay_buoc_dang_that), BỚT 0, ĐỔI THÂN đúng t70, t154;
     t178/t131/t139/t192/_chay_buoc_dang/_buoc_workflow giống thân (hai hàm cuối không cả dời dòng: 2703, 555)        KHỚP
   G diff --quiet 89fc4fa 20ec8d5 -- .github/workflows/ops-publish-lease.yml ⇒ rc=0                                   KHỚP
   G diff --name-only 89fc4fa 20ec8d5 | wc -l ⇒ 128; tên khớp polic|closure|dispatcher ⇒ 0; dòng thêm nhắc
     change_policy|policy canonical|closure policy ⇒ 16, đều hồ sơ wp678 (spec r2–r6, verdict lượt 3, 4, 6); 423b..20ec ⇒ 0 KHỚP
   G log --first-parent --merges 89fc4fa..20ec8d5 ⇒ 10 merge, 0 nhắc #687                                            KHỚP
   r7: --diff-filter=A và log -1 trên f958e14 ⇒ 088511f; 1 commit chạm; sha256 8cb02436…; 745 dòng                    KHỚP
   20ec8d5 = "Merge pull request #689 …", committer 2026-10-01T07:55:21+07:00 (= 00:55:21Z, cạnh merged_at 00:55:22Z) nhất quán
   kích thước 20ec8d5: test 11087 dòng, 195 ^@ca, ca lớn nhất t202, không t193/t194; 89fc4fa: 10502, 187              KHỚP
   ruff 0.15.8 `check --no-cache --select F` hai tệp, hai vế: rc=1, 9 lỗi (7 F401, 2 F541) đều ở tệp test, cùng tập
     bỏ số dòng; ops/lease_publish.py 0                                                                                  KHỚP
   KHÔNG ĐO ĐƯỢC (mạng/object vắng): 459/459 ref, người giữ live, lease g6/#687, commit 35e23d7/6112b89, REST PR #689.
  kết luận   : KHÔNG PHẢI LỖI ở mọi phép đo làm lại được; phần không làm lại được r8 gắn nhãn "phiên soạn r8 tự đo".
```

```
HƯỚNG 6: Tương tác #677 — A1–A10 còn đúng nghĩa sau +600 dòng (đặc biệt A2)
  lệnh       : đọc đặc tả #677 r7 (20ec8d5) §1, §6, §7, §10.5; đọc t195–t202, t70, _toa_do_that trên 20ec8d5.
  output     : `L` của #677 = gỡ chốt D2 (_tien_kiem_mien_dang). #677 §10.5 tự khai: sau #678, `L` có thể tương đương mã
               thoát ở M3; A2 của #677 chỉ cam kết trên start_from_sha ⇒ khớp A2 r8 ("ca trực tiếp phải giết L").
               t195 khoá M2 (null/list/map + hai dạng tài liệu) dãy lời gọi rỗng; t196/t197 chỉ rc≠0, 0 POST, không "bỏ qua";
               t198 wp-ok-1 đúng dãy 4 lời gọi; t202 bơm vectơ L ghi cứng từ 85124dc (helper bị mock) — đúng lời r8.
               Tọa độ r8: t195 :10642, t196 :10686, t197 :10704, t198 :10733, t199–t202 :10744–11034, helper :10506 — KHỚP;
               t178 câu đích ở :7790 (20ec8d5), :7764 (89fc4fa), thân giống hệt.
               KHÔNG ca nào của #677 khoá hành vi nhận kiểu sai mà wp678 phải đổi ⇒ A8 "delta 0" đạt được.
               NGOẠI LỆ: t70 (:2995) ghim LITERAL tập ca nhắc _chay_buoc_dang/_chay_buoc_dang_that (13 tên). Đột biến trên bản
               sao: thêm một ca gọi helper ⇒ `ĐỎ  t70_W6_…: … kiểm kê ca đọc thân bước lệch tập mong đợi`, 0/1; cây gốc 1/1.
  kết luận   : A1–A10 còn đúng nghĩa: KHÔNG PHẢI LỖI. Thiếu kiểm kê t70: LỖI P3 (F8-10, lớp tuong-tac-677-kiem-ke-t70-chua-neu).
```

```
HƯỚNG 7: Nhất quán nội tại
  lệnh       : grep -n -i 'codex|gpt-6|cross_approved|cross-review' SPEC.md; grep "bốn|năm điều kiện"; đếm hunk luot7/HINT.patch.
  output     : 19 dòng khớp; không chỗ nào còn khai codex là reviewer thi hành (chỉ lịch sử r1–r6, trích PROTOCOL/Q8/Q10).
               "bốn điều kiện" còn lại đều ở Q8 (lời chủ kho) hoặc lịch sử r7; chuẩn tắc r8 nói "năm điều kiện".
               HINT lượt 7: dong-reviewer 1, hop-dong 1, q10 1, so-do 2, thu-tu-677 1 (tổng 6) ⇒ nhóm 1, 3, 4, 5 = 5 hunk.
  kết luận   : LỖI P3 (F8-9: "Nhóm 1, 3, 4, 5 … 6/6 hunk"). Còn lại KHÔNG PHẢI LỖI.
```

```
HƯỚNG 8 (tự thêm): Đường B qua launcher — run.json và chốt trust (launcher THẬT, `claude` GIẢ)
  giả thuyết : (i) run.json có argv như (b) giả định; (ii) dạng lệnh r8 bắt buộc chạy được trong sandbox mới.
  lệnh       : lch.MJCe: clone --no-local --no-hardlinks kho.git, checkout --detach f958e147, core.abbrev 7; `claude` giả
               (sh: --version in một dòng; còn lại in một JSON có modelUsage) gọi bằng ĐƯỜNG DẪN TUYỆT ĐỐI; env -i với HOME giả.
               python3 .claude/dev/launcher.py run --workspace <cay> --run-root <runs> --expected-head f958e147…
                 --prompt-file prompt.md --expected-prompt-sha256 5e388fe1…40ca -- <bin>/claude -p --model claude-opus-5-5
                 --effort max --output-format json "Doc {PROMPT_FILE} roi lam theo"
  output     : CA 1 (04:33:42Z, HOME không .claude.json): `CHAN [15]: probe nang luc khong dat: claude_trust=KHONG_DO_DUOC`,
               rc=15; run.json c81ef9d9: trang_thai hong, giai_doan probe; probe workspace/ghi/spawn DAT, claude_trust KHONG_DO_DUOC.
               CA 2 (04:33:53Z, HOME có projects[<cay>].hasTrustDialogAccepted=true): rc=0, run_id 3778e1da58c844579c2605d0f6a94ec2,
               probe.claude_trust DAT; khoá run.json không có argv; `lenh` = {chuong_trinh: claude, so_doi_so: 8,
               van_tay: 538e84004ead814d}; chuỗi '--effort' 'max' '--model' 'claude-opus-5-5' '-p' 'output-format' trong run.json:
               False cả sáu; có prompt_sha256.
               Tính lại sha256(NUL.join(argv khai báo))[:16] ⇒ 538e84004ead814d KHỚP; đổi '--effort max' → 'high' ⇒ 2f754436ed1cdd9d LỆCH.
               Mã: launcher.py :1425–1440 (_tom_tat_lenh, docstring "KHÔNG lưu đối số nguyên văn"), :1134–1148 (probe claude_trust
               chỉ khi tên lệnh là claude), :1114–1126 (đọc ~/.claude.json theo ĐÚNG đường dẫn). Chốt có từ 68d1867 (23-08);
               đặc tả LAUNCHER-DUNG-WORKSPACE M4: đọc trust, không ghi; đường thoát duy nhất --bo-qua-probe (r8 cấm).
               Tiền lệ pr492-review-4 (10-09, sau 68d1867): "run.json đo lớp launcher local_process/subprocess/machine".
  kết luận   : (i) LỖI P2 (F8-1). (ii) LỖI P2 (F8-6). Giới hạn: `claude` thật không chạy; trust/quyền -p thật KHÔNG ĐO ĐƯỢC.
```

```
HƯỚNG 9 (tự thêm): Độc lập phiên của `claude -p` (quét chuỗi TĨNH nhị phân, không chạy)
  lệnh       : command -v claude ⇒ /opt/node22/bin/claude → /opt/claude-code/bin/claude (ELF 241 MB);
               grep -a -o '.{0,80}"--effort <level>".{0,160}', '…CLAUDE_CODE_SESSION_ID…', 'Hd=\[…\]', 'function t8e…'.
  output     : có option `--effort <level>` "Effort level for the current session"; Hd=["low","medium","high","xhigh","max"];
               giá trị lạ ⇒ cảnh báo "Unknown --effort value … using the default effort". Hàm dựng env cho tiến trình con:
               {CLAUDECODE:"1", CLAUDE_CODE_SESSION_ID: e.sessionId, CLAUDE_CODE_CHILD_SESSION:"1", …}.
  kết luận   : khớp phép dò của r8 (session_id kế thừa) và làm câu "là phiên và context mới" rộng hơn đo: LỖI P2 (F8-3, cùng
               lớp với F8-4). Context có dùng chung không: KHÔNG ĐO ĐƯỢC.
```

```
HƯỚNG 10 (tự thêm): Điều kiện dời nền có kín với packet THỨ BA không
  lệnh       : grep r8 'continuation base|Nền tiếp nối|dời nền|không cấp trên nền cũ'; đọc spec wp698 (claude/spec-wp698 trong
               mirror) làm đối chứng; git archive 20ec8d5 ops/leases + yaml.safe_load, đếm lease có write_set chứa hai tệp.
  output     : r8 có điều kiện dời nền theo TÊN (#687 (4), #677 (5)) và câu "Nền tiếp nối … không thay nền này" — không có
               phép đo tổng quát. Đặc tả wp698 (write set ops/cong_cu_test.py, không giao wp678) dùng luật TỔNG QUÁT:
               "nếu [origin/master lúc cấp] đổi ops/cong_cu_test.py thì phải dời nền bằng revision mới trước khi cấp".
               Lease trên master: 23 tệp giữ ops/lease_publish*.py, 8 packet (#203, #206, #227, #238, #244, #396, #579, #676),
               0 lỗi parse; chưa kể #677, #687.
  kết luận   : LỖI P2 (F8-7, lớp thu-tu-677-bo-ngo-o-dieu-kien-cap CÒN MỞ).
```

```
HƯỚNG 11 (tự thêm): Suite hai vế (một lệnh dựng), A1/A3 tái lập
  lệnh       : suite.9Cnb: for pair in nen89:89fc4fa… nen20:20ec8d5…; do git clone -q --no-local --no-hardlinks kho.git;
               checkout --detach; config core.abbrev 7; done; rồi mỗi vế
               PYTHONDONTWRITEBYTECODE=1 TMPDIR=<S>/tmp timeout 3000 python3 ops/lease_publish_test.py
               a13.fISi: nạp module test của 20ec8d5; _yaml_that(raw) → _doc_yaml → kiem(bo_qua_han=True);
               _chay_buoc_dang_that(_yaml_that("yes"), [_dau_bot("True")]) và (_yaml_that("'fresh-id'")).
  output     : nen89 04:41:38Z–04:46:17Z rc=0 "lease_publish: 187/187 đạt; đã chạy=187, bỏ qua=0"; nhật ký vào/ra 561/561.
               nen20 04:46:17Z–04:51:11Z rc=0 "lease_publish: 195/195 đạt; đã chạy=195, bỏ qua=0"; vào/ra 585/585.
               0 .pyc, status sạch ở cả hai vế.
               A1 (04:43:22Z): true/yes/on bool, 1.5/1.50 float, 0x1F/017/1_000/5 int, 2026-09-29 date: kiem ⇒ qua (cả 10);
               'yes' str ⇒ qua. A3: yes + dấu True ⇒ rc 0, POST 0, có "đã đăng trước đó — bỏ qua"; 'fresh-id' ⇒ rc 0, POST 1.
  kết luận   : KHÔNG PHẢI LỖI — A8 nền, A1 "ĐỎ khi", A3 "ĐỎ khi" của r8 tái lập đúng.
```

## BẢNG ĐO

| khẳng định trong spec | spec khai | đo được | khớp? |
|---|---|---|---|
| sha256 r8 / r7 | f173e7cf…5a3b / 8cb02436…b707 | như khai | có |
| commit tạo r7, 1 commit chạm, 745 dòng | 088511f | 088511f; 1; 745 | có |
| VERDICT/HINT lượt 7 sha256 | 992eb9f0…794c / 72289e06…b445 | như khai | có |
| 5 giá trị closure không đổi | không đổi | giống byte r7 | có |
| `lease_publish.py` giống hệt 89fc4fa↔20ec8d5, blob dd17b94c…4f83 | có | rc=0; blob như khai; 2206 dòng | có |
| numstat test 89fc/fc852ff/423b..20ec8d5 | 600 15 | 600 15 ×3 | có |
| 9 commit test(#677) 11f73ac→adad5f5 | có | đúng 9 | có |
| 18 hàm thêm (8 ca + 10 phụ), đổi thân t70, t154 | có | ast: 18/0/2 | có |
| t178/t131/t139/t192/_chay_buoc_dang/_buoc_workflow giống thân, "chỉ dời dòng" | có | giống thân; hai hàm cuối không dời | có |
| workflow ops-publish-lease giống hệt | có | rc=0 | có |
| 128 tệp đổi, 0 tên polic/closure/dispatcher, 16 dòng hồ sơ wp678, 423b..20ec 0 | có | như khai | có |
| 10 merge first-parent 89fc..20ec, 0 của #687 | có | 10 / 0 | có |
| 8e630c0 tổ tiên 20ec8d5; 423b4ba...8e630c0 ⇒ 596 15; hai commit sau 3c308b3, adad5f5 | có | như khai | có |
| suite nền 20ec8d5 195/195, 89fc4fa 187/187, bỏ qua 0, 0 .pyc | có | như khai (04:41–04:51Z 01-10) | có |
| kích thước 11087 / 195 / t202 / không t193, t194 / 10502 / 187 | có | như khai | có |
| ruff 9 lỗi F (7 F401, 2 F541) hai vế, lease_publish.py 0 | có | như khai | có |
| A1: 10 dạng qua kiem() trên 20ec8d5 | có | qua cả 10 | có |
| A3: yes + dấu True ⇒ rc=0, 0 POST, có "bỏ qua"; fresh-id ⇒ 1 POST | có | như khai | có |
| tọa độ t195…t202, helper, t178 :7789–7790 | có | như khai (câu đích ở :7790) | có |
| t202 bơm vectơ L ghi cứng từ 85124dc | có | docstring + mock helper | có |
| Q11 sha256/byte/0 thực thể/dòng 5–17 chép từng byte | 392069d1…/1741/0/13 | như khai | có |
| Q8 sha256/1187/0 thực thể/0 lần "677" | có | như khai | có |
| Q10 sha256/2151; 6 dòng trích | có | như khai; khối liên tục | có |
| #682: sha256 76bee6fb…, 3416 byte, dòng 29 và 31 | có | thân vắng khỏi $R và kho | KHÔNG ĐO ĐƯỢC |
| PROTOCOL + bien_nhan_v2 giống hệt 423b4ba↔20ec8d5 | có | rc=0 | có |
| định nghĩa review-opus-max e225b81c…, 1175 byte | có | như khai | có |
| kiem_ket_qua ĐẠT opus / ném với sonnet | có | như khai (JSON tổng hợp) | có (JSON thật KHÔNG ĐO ĐƯỢC) |
| JSON của claude không có khoá effort | có | — | KHÔNG ĐO ĐƯỢC (không chạy claude thật) |
| (b) argv có `--effort max` "đọc từ run.json" | đọc được | run.json không lưu argv | **không** (F8-1) |
| tiền lệ don-nhanh-base-review-7: session_run_id launcher, model từ modelUsage | có | 0 session_run_id, 0 modelUsage, schema 1 | **không** (F8-5) |
| "Tiến trình claude -p là phiên và context mới" | có | session_id kế thừa (r8 tự đo) + CHILD_SESSION (tĩnh) | **không** (F8-3) |
| B chạy được với launcher, không --bo-qua-probe, sandbox mới | ngầm định | CHAN [15] (claude_trust) | **không** (F8-6) |
| lớp thu-tu-677-bo-ngo-o-dieu-kien-cap "đóng theo Q11" | đóng | phần tổng quát (iii) còn | **không** (F8-7) |
| "Nhóm 1, 3, 4, 5 … 6/6 hunk" | 6/6 | bốn nhóm = 5 hunk; cả HINT = 6/6 | **không** (F8-9) |
| 459/459 ref, NGƯỜI_GIỮ 0, lease g6 rút hạn 35e23d7, #687 HẾT_HẠN, REST PR #689 | có | cần mạng / object vắng | KHÔNG ĐO ĐƯỢC |
| "64 giây" sau 01:10:00Z | 64 | 01:11:04Z − 01:10:00Z = 64 s | có (số học) |
| 20ec8d5 merge PR #689, merged_at 00:55:22Z | có | commit 00:55:21Z, tiêu đề #689 | có (nhất quán) |

## CHI TIẾT TỪNG LỚP

### `hop-dong-dong-bang-thieu-neo` — P2 (VÁ SINH LỖI MỚI; lượt 1 P2, lượt 2 P1, lượt 7 P2, lượt 8)
- F8-1 (r8 :90–91). Tiêu chí (b) neo phần "effort `max`" của vế review vào "argv … đọc từ `run.json`". Launcher cố ý không lưu
  argv (bí mật có thể nằm trong argv); đo được ở Hướng 8. Đọc nghiêm: (b) không bao giờ đạt ⇒ vế review không đạt ⇒ không land
  được nếu không ra revision mới. Đọc rộng (vân tay): kiểm được nhưng không có trong chữ. Chính sự lệch giữa chữ và hiện vật là
  lỗi; xếp P2 theo rubric "tiêu chí không kiểm được".
- F8-2 (r8 :33 điều kiện (3), :232–234). (3) đòi "review sạch bằng lượt Opus 5.5 `max`"; đường đang dùng cho review ĐẶC TẢ
  (lượt 7, lượt 8: subagent) không có nguồn đo model — đúng lý do r8 bỏ đường ấy cho lượt thi hành. r8 không nói (3) kiểm thế
  nào. Mức P3 trong lớp; HINT chọn cách đọc khớp thực hành hiện tại và Q10 ("review r7, rồi cấp lease … ngay trong phiên này"):
  lượt subagent được tính, ghi `review_deferred`, model là cấu hình. Nếu người điều phối/chủ kho muốn cả review đặc tả đi đường
  B, đổi hunk ấy.
- Phép kiểm đóng lớp: biên nhận lượt thi hành có argv nguyên văn và `van_tay` tính lại khớp `run.json`; (3) quyết định được
  cho cả hai đường. Giới hạn: effort thực tế vẫn KHÔNG ĐO ĐƯỢC — lớp này chỉ đóng được ở mức "neo vào thứ kiểm được".

### `dong-reviewer-loi-khai-rong-hon-do` — P2 (TÁI PHÁT, nâng từ P3)
- F8-3 (r8 :32): "là phiên và context mới". F8-4 (r8 :32, :92): `session_run_id` := `run_id`. F8-5 (r8 :32): tiền lệ dẫn sai.
- Vì sao nâng P2: ở lượt 7 các câu này mô tả; ở r8 chúng là CƠ SỞ cho mức `same_provider_approved` mà validator chỉ kiểm
  bằng sự có mặt của một chuỗi (Hướng 2: G1, G2). Nếu phiên executor tự phóng lượt review (r8 không cấm), tiến trình con mang
  session ID của chính executor mà biên nhận vẫn qua validator.
- Cách vá chung: không suy độc lập từ tiến trình con; đo ở phiên phóng, so với session ID executor đã ghi (PROTOCOL :710 đã
  đòi ghi session/run ID cả hai phía). Phép kiểm đóng lớp: ba giá trị có mặt và khác. Giới hạn: chia sẻ context KHÔNG ĐO ĐƯỢC.

### `duong-review-b-chua-do-dau-cuoi` — P2 (MỚI)
- F8-6 (r8 :32, :80–103, §10 :711–716). B được đóng băng thành tiêu chí sau một phép dò KHÔNG qua launcher (r8 tự khai), nên
  chốt trust của launcher — đọc được từ mã, có từ 23-08 — không lộ. Hệ quả khi làm đúng chữ: lượt review thi hành dừng ở
  `CHAN [15]` ⇒ r8 rơi vào nhánh "launcher chặn ⇒ DỪNG và hỏi chủ kho" — tức chủ kho vẫn bị hỏi, nhưng muộn, giữa lúc lease
  chạy. Vì sao không P1: r8 có nhánh dừng-hỏi, chủ kho chấp nhận trust không cần revision, và land vẫn đòi `human_audited`.
- Cách vá: bootstrap trust/quyền là quyết định của chủ kho, đặt TRƯỚC lượt, có hiện vật kiểm (`run.json.probe.claude_trust`);
  một lượt khói qua launcher trước khi đóng băng revision kế để (a)–(e) viết trên hiện vật có thật.

### `thu-tu-677-bo-ngo-o-dieu-kien-cap` — P2 (CÒN MỞ phần tổng quát)
- F8-7 (r8 :33, :34, :750). Q11 đóng đúng câu hỏi thứ tự #677; điều kiện (5) và nền `20ec8d5` đóng phần #677. Nhưng cơ chế mà
  lượt 7 gọi là biểu hiện (iii) — dời nền chỉ khi một packet ĐƯỢC NÊU TÊN land — còn nguyên cho mọi packet khác, trên một tệp
  điểm nóng (Hướng 10). Vá bằng một phép đo bất biến thay cho danh sách tên (cùng gốc *"danh sách CẤM không bao giờ đủ"*).

### `q10-he-qua-mat-nhan-dien-giai` — P3 (TÁI PHÁT)
- F8-8 (r8 :26). Trả lời thẳng câu PROMPT: **B KHÔNG phải quyết định của chủ kho** (không có trong lựa chọn Q10 hay Q11; chỉ
  "áp HINT lượt 7" xuất hiện trong đoạn Hệ quả có nhãn diễn giải, và HINT lượt 7 nhóm 2 là phương án A, không phải B).

### `so-do-nen-khong-khop` — P3 (TÁI PHÁT)
- F8-9 (r8 :689). Người điều phối có thể bác việc nối slug (đây là số-đếm-lệch-phạm-vi, không phải số nền); nếu bác thì lớp
  này ĐÃ VÁ THẬT và F8-9 thành lớp P3 riêng — hạng và hunk không đổi, chỉ bộ đếm §12 đổi (0/5 → 1/5).

### `tuong-tac-677-kiem-ke-t70-chua-neu` — P3 (MỚI)
- F8-10 (r8 :321–328). Executor sẽ thấy `t70` đỏ khi chạy suite; ghi trước để khỏi đọc nhầm thành hồi quy hay sửa sai chỗ.

## DRY-RUN HINT.patch

`$R/goi/HINT.patch`: 137 dòng, 48934 byte, sha256 `41e3763cedde5ae1e9d8de2f5ddcbda345428f696cc5a69d35cf3fc57aaca400`.
7 nhóm `# lop:` theo thứ tự: `dong-reviewer-loi-khai-rong-hon-do` (2 hunk) · `hop-dong-dong-bang-thieu-neo` (2) ·
`thu-tu-677-bo-ngo-o-dieu-kien-cap` (2) · `duong-review-b-chua-do-dau-cuoi` (2) · `q10-he-qua-mat-nhan-dien-giai` (1) ·
`so-do-nen-khong-khop` (1) · `tuong-tac-677-kiem-ke-t70-chua-neu` (1) = 11 hunk. Mỗi nhóm là diff ĐỘC LẬP trên r8 gốc;
không dòng nào bị hai nhóm sửa, không ngữ cảnh nào chạm dòng nhóm khác sửa (bộ sinh `assert`). Bốn hunk ở hai vùng có dòng kề
nhau do hai nhóm khác nhau sửa (r8 :32 với :33–34 ở bảng đầu tệp; :90–91 với :92 ở ghi chú dưới closure) dùng 0 dòng ngữ cảnh,
để nhóm này không lấy dòng nhóm kia sửa làm ngữ cảnh (dòng cũ vẫn được `patch` kiểm từng byte); các hunk còn lại 3 dòng ngữ cảnh. Sinh bằng `hint8.6iOC/sinh_hint.py` (kiểm sha256
r8 và nội dung từng dòng cũ trước khi thay; 0 dấu chéo ngược trong bộ sinh và trong HINT). Đường dẫn repo-relative, không `a/`/`b/`.

Lệnh (đúng PROMPT), chạy trên tệp đã chép vào `goi/` (cmp khớp bản sinh), 05:02:48Z:
```
T=$(mktemp -d -p "$R") && cp -a "$R/cay-kho" "$T/cay"
cd "$T/cay" && patch -p0 --fuzz=0 --dry-run --verbose < "$R/goi/HINT.patch"
```
Output (T=`$R/tmp.MPm0JIMpN4`, GNU patch 2.7.6): **rc=0**; 7 lần "checking file ops/specs/lease-id-ep-kieu-yaml-r8.md";
"Hunk #1 succeeded at 32." "Hunk #2 succeeded at 92." · "Hunk #1 succeeded at 90." "Hunk #2 succeeded at 237." ·
"Hunk #1 succeeded at 33." "Hunk #2 succeeded at 747." · "Hunk #1 succeeded at 98." "Hunk #2 succeeded at 724." ·
"Hunk #1 succeeded at 23." · "Hunk #1 succeeded at 686." · "Hunk #1 succeeded at 325." · "done". 11/11 succeeded; 0 dòng
FAILED/fuzz/offset/malformed; `git status --porcelain --ignored` của bản sao sau dry-run: 0 dòng.

Áp THẬT (bản sao `apthat.2mVw`, `patch -p0 --fuzz=0`, tuần tự): rc=0; sáu hunk báo offset (5–26 dòng, do nhóm trước chèn dòng),
0 fuzz; 0 tệp `.rej`/`.orig`; `git diff --numstat` 49/12; 890 → 927 dòng; `cmp` với `hint8.6iOC/ky_vong.md` (bản dựng độc lập
bằng Python, áp mọi thay thế trên dòng gốc từ dưới lên) ⇒ KHỚP từng byte. Áp RIÊNG từng nhóm trên bản r8 gốc: cả 7 rc=0,
0 fuzz/offset/FAIL.

Nhãn bắt buộc cho người áp (PROTOCOL §8 :600–601): *"chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm
commit"*. Đây là HINT cho một ĐẶC TẢ; mọi thay đổi thành revision 9, phiên soạn r9 phải đo lại mọi số và băm của chính r9
(kể cả các số mà hunk ghi "review lượt 8 đo": chúng là số của lượt này, không phải phép đo của phiên soạn). HINT không động
vào chỗ phải đổi khi dựng r9 (tiêu đề "revision 8", điều kiện (3) "đó là revision 8", công thức băm, tên tệp) — việc của
người dựng r9, như lượt 7 đã để lại cho r8.

## GIỚI HẠN VÀ TOÀN VẸN
- KHÔNG ĐO ĐƯỢC từ `$R` (không mạng): trạng thái máy chủ (459 ref, người giữ live, lease #677/#687/g6), REST PR #689 và #682,
  object `6112b89`/`35e23d7`, JSON thật của phép dò `claude -p` 01:07Z, mọi hành vi của `claude` THẬT (trust, quyền `-p`, model
  phục vụ, context của tiến trình con có kế thừa từ phiên gọi hay không).
- Đọc NGOÀI `$R` (chỉ đọc, không in thân, không in bí mật): `~/.claude/agents/review-opus-max.md` (băm, cỡ, mtime, 4 khoá
  frontmatter); nhị phân `/opt/claude-code/bin/claude` (quét chuỗi tĩnh, không chạy). Không đọc `~/.claude.json` thật — phép đo
  trust dùng HOME giả trong `lch.MJCe`. Session ID dùng ở G1 là chuỗi đã công khai trong thân Q11, chỉ để thử validator.
- Ghi: chỉ `$R/goi/` và các thư mục `mktemp -d -p "$R"` nêu ở BẢNG SĂN. Mọi clone đo dùng `--no-local --no-hardlinks` (không
  hardlink vào `kho.git`); `kho.git` chỉ đọc (log/show/diff/grep/archive, nguồn clone).
- Chỉ giết/chờ tiến trình do lượt này sinh (một lệnh suite chạy nền, đã kết thúc rc=0); không gọi lệnh giết nào.
- `cay-kho` cuối lượt (05:04:11Z): HEAD `f958e147…`, tree `02aaa0cf07fe…`, `status --porcelain --ignored` 0 dòng, diff/index sạch,
  0 `.pyc` mới. Theo §8.2, snapshot sạch hai mốc không chứng minh chưa từng ghi rồi hoàn nguyên giữa chừng.
- Một lỗi script của chính lượt này (unpack `None` khi so Q10, trước 04:43:22Z) làm lệnh đầu thoát rc=1 sau khi đã in kết quả
  Q11; sửa script và chạy lại phần Q10 riêng — không con số nào trong tệp này lấy từ lần chạy lỗi ngoài dòng Q11 đã in trọn.
