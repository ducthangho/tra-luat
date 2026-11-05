# Đặc tả packet `K6K7-MERGE-BASE` r2: K6/K7 của `kiem-merge` tính diff từ merge-base(H, master đọc từ máy chủ)

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `K6K7-MERGE-BASE`, revision 2, generation 1 |
| packet_issue | #1212 |
| nguon_cap_viec | P-A trong `ops/specs/K3-CONNECTOR-STATE-r1.md` §5 (sha256 `ec6e9f3e…0d9a`). Chủ kho duyệt mở theo Q9 ("mở P-A ngay") ở #1211 issuecomment-6650045245 (05-11-2026 04:55Z), qua phiên điều phối `session_015GtxrYPjZCTZeRiazdssgq`. r2 thay r1 (`ops/specs/K6K7-MERGE-BASE-r1.md`, sha256 `97e2fae6…1fb2`, đã duyệt ở #1212 issuecomment-6650249746) sau phản biện Proxima (§9); chủ kho duyệt hướng r2 trực tiếp trong phiên soạn đặc tả ngày 05-11-2026 (*"Duyệt theo khuyến nghị, soạn và đóng băng hai r2"*) |
| trạng thái | `proposed`. r2 chờ chủ kho duyệt `spec_hash`. **Đừng neo lease vào băm r1**: r1 khẳng định sai rằng `origin/master` cục bộ cũ chỉ làm cổng chặt hơn (§1.3) |
| review_class | `sensitive`: sửa cổng `.claude/dev/packet_loop.py` (`docs/PROTOCOL_DA_PHIEN.md` §20) |
| base | `origin/master` lúc cấp lease, và **phải chứa** merge của PR #1194 (#1187) và của packet `K3-CONNECTOR-STATE` (#1211, đặc tả r2) (§3.1). Thứ tự chủ kho chốt trên `packet_loop.py`: #1187 → #1211 → #1212 → #1210. Lúc soạn (05-11 05:0xZ) master là `e626648` |
| executor / reviewer | như #1211 Q7: executor `anthropic_claude` (một phiên Claude Code mới), reviewer `openai_codex` qua `launcher.py run` cộng connector `@codex review` trên PR draft |
| windows | `required` (ADR-0060 M3 bước 2: diff chạm `.claude/dev/**`) |
| full_mutant_audit | bắt buộc (ADR-0060 M9) |

## 1. Vì sao: số đo

Phép đo: gọi thẳng `_diff_raw`, `_phan_loai_windows` (với `spec = b""`) và `_cham_m9` của `.claude/dev/packet_loop.py` tại master
`e626648`, trên ref `refs/pull/N/head` vừa fetch. Thời điểm: 05-11-2026 05:00Z–05:05Z.

### 1.1 Mã hiện hành

- `kiem-merge` nhận `--base B`. Đặc tả gốc (`ops/specs/DIEU-KIEN-MERGE-CONG-r1.md` dòng 40, 46) chỉ định nghĩa B là "40 hex".
  K0 đòi B là tổ tiên của H và của `refs/remotes/origin/master`, và B ≠ H.
- K6 (`_phan_loai_windows(root, a.base, h, spec)`) và K7 (`_cham_m9(root, a.base, h)`) cùng dùng `_diff_raw(root, B, H)`.
  Đó là `git diff --raw --no-renames -z B H`, tức diff hai chấm giữa **cây** B và **cây** H.
- ADR-0060 M3 và M9 chỉ nói "diff chạm …", không nói diff tính từ đâu.

### 1.2 Hệ quả: master được merge vào nhánh sau base

Khi nhánh merge master vào (update-branch), cây H chứa mọi thay đổi của master từ B tới điểm merge. `B..H` vì thế không còn là
"thay đổi của packet". Nó là thay đổi của packet **cộng** một đoạn master.

Đo trên 51 PR `refs/pull/1140..1210/head` đọc được: **10** PR có head là commit merge, cha thứ hai nằm trên master.
Bảng so hai base cho từng PR:
- "cũ" = `merge-base(H^1, H^2)`, điểm rẽ trước lần merge, xấp xỉ base của lease;
- "mới" = `H^2`, bằng `git merge-base --all H H^2` (mọi ca ra đúng 1 kết quả).

| PR | base cũ | tệp / K6 / K7 (cũ) | base mới | tệp / K6 / K7 (mới) | đổi |
|---|---|---|---|---|---|
| #1146 | `9156fece` | 264 / required / bắt buộc | `8983e1bb` | 69 / required / bắt buộc | — |
| #1150 | `8983e1bb` | 48 / required / bắt buộc | `279a39e3` | 46 / required / **không** | K7 |
| #1152 | `279a39e3` | 197 / required / bắt buộc | `1f0941e9` | 42 / **not_required** / **không** | K6, K7 |
| #1153 | `ff40fd23` | 61 / required / bắt buộc | `5fe92c13` | 40 / required / bắt buộc | — |
| #1191 | `02ddeb4e` | 383 / required / bắt buộc | `1f0941e9` | 39 / **not_required** / **không** | K6, K7 |
| #1192 | `02ddeb4e` | 345 / required / bắt buộc | `1f0941e9` | 1 / required / bắt buộc | — |
| #1197 | `f2e33bc3` | 146 / required / không | `8ffbe51d` | 9 / required / không | — |
| #1200 | `4d258cc8` | 168 / required / bắt buộc | `f2e33bc3` | 1 / **not_required** / **không** | K6, K7 |
| #1203 | `f2e33bc3` | 70 / required / không | `36ef7061` | 47 / **not_required** / không | K6 |
| #1204 | `36ef7061` | 220 / required / bắt buộc | `39d511d2` | 59 / required / bắt buộc | — |

Đếm (đơn vị: PR, trên 10 PR có head là merge):
- K6 đổi từ `required` sang `not_required` ở **4** PR: #1152, #1191, #1200, #1203.
- K7 đổi từ bắt buộc sang không ở **4** PR: #1150, #1152, #1191, #1200.
- Trong 10 PR ấy, hướng sai luôn là **chặt hơn** (đỏ oan), chưa ca nào lỏng hơn. Nếu B mới hơn điểm rẽ thật thì diff có thể
  **hẹp** hơn thay đổi của packet (lỏng). K0 hiện không chặn ca đó: B chỉ cần là tổ tiên chung. Packet này đóng ca ấy bằng
  cách không dùng B cho K6/K7 nữa (§2).

Giới hạn của phép đo: "base cũ" là xấp xỉ, không đọc từ lease. Trên #1200, base của lease (`4d258cc`, theo human audit 6649074827)
trùng đúng giá trị xấp xỉ.

### 1.3 Kho git tạm: ba ca của phản biện (đo 05-11-2026 05:3xZ)

Script `thu_merge.sh` của phiên soạn (scratchpad, không vào kho) dựng kho tạm và so `git diff --name-only M H` với diff của
kết quả merge thật so với master-tip:

| ca | lịch sử | `M..H` | kết quả merge vs master-tip |
|---|---|---|---|
| 1 | master sửa workflow sau B; PR chỉ sửa docs, merge master vào, master tiến tiếp sau đó | `docs/a.md`, `docs/c.md` | y hệt |
| 2 | master sửa workflow; PR không merge master, không đụng workflow | `docs/d.md` | y hệt |
| 3 | `origin/master` cục bộ cũ trỏ D (D sửa workflow); master thật đã lùi về C; PR rẽ từ D | M = D ⇒ chỉ `docs/f.md` | M = C ⇒ thêm `.github/workflows/ci.yml` |

- Ca 1, 2: với merge sạch, `M..H` cho đúng tập đường dẫn mà phép merge đổi. Nói chung `M..H` **bao trùm** tập ấy: đường dẫn
  nào H không đổi so với M thì phép merge ba chiều lấy bản của master. Xung đột thì phải giải **trong** H (dịch vụ không tự
  giải khi merge), nên phần giải nằm trong `M..H`.
- Ca 3: `origin/master` cục bộ cũ làm diff **hẹp đi**, mất đúng tệp workflow. Câu của r1 *"bản cũ chỉ làm cổng chặt hơn"* là
  **sai**. r2 đóng ca này bằng M0 (§2).

## 2. Thay đổi

Trong `cmd_kiem_merge`, K6 và K7 tính diff từ **M** thay cho `--base`, với M định nghĩa như sau:

| # | chốt | thiếu chốt ⇒ |
|---|---|---|
| M0 | `git ls-remote origin refs/heads/master` rc 0, trả **đúng một** dòng có SHA 40 hex R; `git rev-parse refs/remotes/origin/master` = R (ref cục bộ trùng máy chủ ngay lúc đo) | lỗi, 0 hoặc ≥ 2 dòng, hoặc ref cục bộ ≠ R ⇒ K6 và K7 đều KHÔNG ĐO ĐƯỢC, thông báo nêu cả hai SHA và lệnh chữa `git fetch origin master` |
| M1 | `git rev-parse --is-shallow-repository` = `false` | `ValueError` ⇒ K6 và K7 đều KHÔNG ĐO ĐƯỢC (thiếu) |
| M2 | `git merge-base --all H R` (R là SHA của M0, không phải tên ref) rc 0, trả **đúng một** SHA 40 hex. Đó là M | 0 hoặc ≥ 2 kết quả, hoặc git lỗi ⇒ như M1 |
| M4 | M ≠ H | M = H ⇒ K6 và K7 không đạt với thông báo riêng `ĐÃ NẰM TRONG MASTER` (khác `KHÔNG ĐO ĐƯỢC`) |
| M5 | R và M được tính **một lần** trong lệnh và dùng chung cho K6 lẫn K7, không tính lại trong từng hàm | — (chốt cấu trúc, đo bằng đột biến A5) |

- `_diff_raw`, `_phan_loai_windows` và `_cham_m9` giữ chữ ký `(root, b, h, …)`. Chỉ đổi đối số mà `cmd_kiem_merge` truyền vào.
- K0 giữ nguyên, vẫn kiểm `--base`.
- Thông báo thành công và thông báo thiếu của K6/K7 in thêm `M=<sha>`, để người đọc biết diff tính từ đâu.
- Cách lấy M dùng `_git_do` như phần còn lại của tệp.

**M3 của r1 đã bỏ.** M là best common ancestor duy nhất (M2), mà B là tổ tiên chung của H và master (K0), nên B luôn là tổ tiên
của M. Chốt ấy không thể vi phạm, nên đột biến "bỏ M3" không thể bị giết và tiêu chí A5 của r1 không bao giờ đạt.
K0 đọc `refs/remotes/origin/master` cục bộ; sau M0 thì ref ấy bằng R, nên K0 và K6/K7 cùng nhìn một master.

## 3. Write set

`.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` · `ops/specs/K6K7-MERGE-BASE-r2.md` (chép **nguyên byte** vào commit
đầu của nhánh thực thi). Ba tệp. Ước lượng ≤ 40 dòng thêm ở `packet_loop.py`, ≤ 200 ở test, chưa tính tệp đặc tả.
Không sửa ADR: ADR-0060 không định nghĩa gốc của diff (§1.1). Xem §7 Q2.

### 3.1 Người giữ (đo 05-11-2026 05:04Z)

- Phép đo: fetch `+refs/heads/*:refs/remotes/origin/*`, so tập tên máy chủ/cục bộ: 864/866, thiếu 0. Thừa 2 là nhánh đã xoá trên
  máy chủ, vô hại. Sau đó chạy `ops/lease_publish.py ai-dang-giu`.
- Kết quả: cả `packet_loop.py` lẫn tệp test ⇒ **rc 11, `NGƯỜI_GIỮ 1`**: `pr1184-merge-contract-r2-g4-codex-service` (#1187, hạn 05:23:42Z).
- Packet `K3-CONNECTOR-STATE` (#1211, đã duyệt `spec_hash`, chưa có lease) dự kiến giữ **cùng hai tệp**.
- Hệ quả: ba packet nối đuôi trên cùng write set. Thứ tự khuyến nghị: #1187 → #1211 → packet này (§7 Q1). Đo lại `ai-dang-giu` ngay
  trước lúc cấp lease (L5).

## 4. Nghiệm thu

Ca mới trong `.claude/dev/packet_loop_test.py` mang tiền tố `k67mb_`, dựng kho git tạm theo khuôn fixture `_c1106` hiện có.
Đột biến đích phải bị giết **đúng lý do**: ở tín hiệu assertion của ca đích, kèm thông báo mong đợi. Traceback không tính.

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | `packet_loop_test.py` ra N/N, hai số bằng nhau; mọi ca `cong_c_*`, `cong_m9_*`, `k3st_*` cũ vẫn xanh | bất kỳ ca đỏ |
| A2 | ca dương, khuôn #1200: base B; master thêm `.github/workflows/x.yml` sau B; nhánh thêm `ops/specs/a.md` rồi merge master vào ⇒ K6 `not_required` và K7 không bắt buộc. Trên nền (diff `B..H`) ca này **ĐỎ** (`required`, M9 chạm). Hình dạng nền đã đo trên dữ liệu thật #1200 (§1.2); trên fixture thì executor đo trước khi vá | xanh trên nền ⇒ ca không đo gì |
| A3 | ca giữ chặt: nhánh tự sửa `.github/workflows/x.yml` rồi merge master ⇒ vẫn `required` và M9 bắt buộc. Thêm ca merge commit tự sửa tệp workflow khi giải xung đột ⇒ `required`. Thêm ca bao trùm (khuôn Ca 1): master tiến tiếp sau lần merge vào nhánh ⇒ tập đường dẫn của `M..H` bằng tập của kết quả merge thử so với master-tip | xanh khi đột biến bỏ phần thay đổi của merge commit |
| A4 | ca âm, mỗi chốt một ca, K6 và K7 cùng thiếu kèm `KHÔNG ĐO ĐƯỢC`: M1 kho nông · M2 criss-cross (hai merge-base) · M2 `origin/master` vắng · M0 `ls-remote` lỗi · M0 `origin/master` cục bộ cũ hơn máy chủ · M0 khuôn Ca 3 (cục bộ trỏ commit đã bị lùi khỏi master thật; với M0 thì `KHÔNG ĐO ĐƯỢC`, gỡ M0 thì diff mất tệp workflow) · M4 H đã nằm trong master ⇒ thông báo `ĐÃ NẰM TRONG MASTER` | ca nào đạt ⇒ đỏ |
| A5 | đột biến đích, mỗi cái giết ít nhất một ca A2–A4: truyền lại `a.base` cho K6 · truyền lại `a.base` cho K7 (M5: hai đột biến tách riêng) · bỏ `--all` (lấy kết quả đầu) · bỏ chốt shallow · bỏ M0 (dùng ref cục bộ không so) · M0 nhận khi ref cục bộ ≠ R · M2 dùng tên ref thay cho R · bỏ M4 · dùng diff ba chấm `B...H` thay vì M | đột biến sống ⇒ đỏ |
| A6 | **dữ liệu thật**: với từng PR trong bảng §1.2, hàm tính M (đúng mã ứng viên, `origin/master` ghim tại một commit chứa cha thứ hai của H) trả đúng `H^2`, và phân loại K6/K7 khớp cột "mới". Chạy được tại chỗ khi `refs/pull/N/head` còn fetch được; ghi lệnh và kết quả vào biên nhận | lệch một ô ⇒ đỏ |
| A7 | M6: K6/K7 thiếu vì M cùng một điều kiện khác ⇒ thông báo nêu cả hai | — |
| A8 | `git diff --numstat <base> <ứng viên>`: đúng ba tệp §3 | tệp thứ tư ⇒ đỏ |
| A9 | `doctrine-scan`, `adr-song`, `doc-claims-check` xanh | — |
| A10 | Windows (M3 `required`): **một** lượt ca `k67mb_*` và `cong_c_*` trên `tra-luat-win` tại ứng viên, > 0 ca, không ca `skipped`. Lượt nền thì chủ kho miễn (như #1211 Q8) | 0 ca ⇒ đỏ |
| A11 | M9: một lượt `ci-dot-bien-du.yml` `success` tại head cuối, và K7 đạt với readback của lượt ấy | run đỏ ⇒ sửa hoặc hỏi chủ kho |

## 5. Ngoài phạm vi

- K4 khi head đổi vì update-branch sau approve. Đó là P-B, chờ #1187 (#1211 §5).
- Đổi nghĩa `--base` ở K0, hay bỏ hẳn cờ `--base`.
- `_phan_loai_windows`/`_cham_m9` ở nơi gọi khác: hiện chỉ `cmd_kiem_merge` gọi (đo bằng `grep -n` tại `e626648`: 2 lời gọi, cả hai trong `cmd_kiem_merge`).
- Sửa đặc tả gốc `DIEU-KIEN-MERGE-CONG-r1.md`: đặc tả đã đóng băng không sửa đè.

## 6. `hinh_dang_ke_thua`

`khong_ap_dung`: packet này không khắc phục một packet trước. Họ lỗi liên quan để reviewer quét theo lớp (ADR-0060 M2):
- CLAUDE.md *"PHÉP ĐO DELTA SO HAI VẾ"*: chọn sai vế nền sinh hồi quy giả.
- CLAUDE.md *"`git for-each-ref` ĐỌC BỘ ĐỆM CỤC BỘ"*: `origin/master` cục bộ có thể cũ, kho nông làm `merge-base` sai.

## 7. Quyết định của chủ kho

Q1–Q3 duyệt theo khuyến nghị ở #1212 issuecomment-6650249746. Q4 **đảo lại** trong r2 theo phản biện (§9), chủ kho duyệt trực tiếp trong phiên soạn đặc tả 05-11-2026.

- **Q1. Thứ tự với #1211.** Hai packet cùng write set.
  ➡️ Khuyến nghị #1187 → #1211 → packet này. #1211 đã duyệt trước; packet này nhỏ và base phải chứa mã K3 mới.
- **Q2. Có ghi định nghĩa gốc diff vào ADR-0060 (M3/M9) không?**
  ➡️ Khuyến nghị không trong packet này: giữ ba tệp. Ghi nợ một câu cho lần sửa ADR-0060 kế tiếp; #1211 r2 cũng không gộp việc này.
- **Q3. Tính M tự động (§2) hay đòi người gọi truyền `--base` = M và `_die` khi khác?**
  ➡️ Khuyến nghị tự động. Người gọi không phải đổi gì, và base lạ không còn ảnh hưởng K6/K7. Đòi truyền đúng thì mọi lệnh hiện có đỏ cho tới khi người gọi tự tính merge-base, mà đó chính là phép tính lệnh làm được.
- **Q4. `origin/master` cục bộ cũ.** r1: không so với `ls-remote`, vì tưởng hướng sai chỉ là chặt hơn. Ca 3 (§1.3) bác giả định ấy.
  ➡️ r2: so bắt buộc (M0).

## 8. `chua_do_duoc`

- Base thật của lease cho 9/10 PR trong §1.2: phép đo dùng giá trị xấp xỉ `merge-base(H^1, H^2)`, chỉ #1200 được đối chiếu với lease.
- Hành vi trên PR merge master **nhiều lần**: chưa có mẫu trong 51 PR đã đo. M2 vẫn áp; A2/A3 nên có một ca hai lần merge.
- M0 đo một thời điểm: master có thể đổi sau lúc đo mà trước lúc merge. Đó là khe giữa lúc chạy cổng và lúc merge, cùng loại với mọi cổng đọc trạng thái; không đóng được trong lệnh này.
- M0 cần mạng tới `origin` (K0 vốn đã cần, cho `ls-remote` PR head).

## 9. Phản biện r1 → r2 (Proxima, 05-11-2026)

r1 gửi phản biện qua Proxima (VM `tra-luat-win`): prompt hẹp 6 câu, đã bỏ mọi tên thật, kèm mã `_diff_raw`/`_cham_m9`/
`_phan_loai_windows`/`k0` nguyên văn; prompt sha256 `a506bd30dd74a561e55d6b18486901ff4d2b1dead1b2f01971d673f17b917d0e` (đối chiếu
trên VM: khớp), `chatgpt:gpt-6-thinking`, request `f779305f343642ad8cd72a3577650563`, một lần gửi. Câu trả lời lưu ở
`ProximaGateway/results/k3k6-review/answer_k6.txt` trên VM. Mỗi ý được đo lại trên kho git tạm (§1.3) trước khi tiếp thu:

| câu | ý của Proxima | đo lại | trong r2 |
|---|---|---|---|
| Q2 | `origin/master` cục bộ cũ/bị lùi có thể làm diff hẹp đi | **đúng** (Ca 3) | M0 |
| Q4 | M3 bị M2 + K0 kéo theo | đúng; đột biến của nó không thể bị giết | bỏ M3 |
| Q4 | M = H nên là trạng thái riêng | hợp lý | thông báo `ĐÃ NẰM TRONG MASTER` |
| Q1, Q3 | `M..H` khác kết quả merge (Proxima xếp P1) | merge sạch cho y hệt (Ca 1, 2); xung đột phải giải trong H | bác P1; đổi câu thành "bao trùm", thêm ca A3 |
| Q6 | nhánh miễn trừ chạy trước dòng `windows: required` | mã đi đúng thứ tự bước 1 của ADR-0060 M3 | bác |
| Q6 | rename lọt | `--no-renames` báo cả đường dẫn cũ lẫn mới | bác |
| Q5 | 2+ merge-base: giữ fail-closed | đồng ý | không đổi |
