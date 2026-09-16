verdict: changes_requested
reviewed_sha: 8765d43aecfe71dfd5ed99d429010071817fac45

# CROSS-REVIEW LƯỢT 1 — packet #546 `MOI-TRUONG-CONG-CU-DO-DUOC` r1/g1

| | |
|---|---|
| PR | #549 · nhánh `agy/moi-truong-r1-g1` |
| `reviewed_sha` | `8765d43aecfe71dfd5ed99d429010071817fac45` (17-09 01:46:34 +0700) |
| `base_sha` | `dd274415408bd1c6b4279c8e2cf9671057520f23` |
| executor | `antigravity` · reviewer `claude` · lease `moi-truong-r1-g1-antigravity` |
| kết luận | **`changes_requested`** — **6 LỚP**: 2 P1 · 2 P2 · 2 P3 (đếm bằng máy từ chính tệp này) |
| assurance | **`advisory_review`**, KHÔNG phải `cross_approved` — xem cuối |

## ĐỐI CHIẾU LƯỢT TRƯỚC

`khong_ap_dung` — đây là lượt **1** của packet này. Không có slug nào để phán canonical.

## BẢNG ĐO — liệt kê CẢ cái khớp, không chỉ cái lệch

| khẳng định | PR/lease khai | đo được | khớp? |
|---|---|---|---|
| write set đúng ba đường | 3 | `numstat` = **3 tệp**, đúng ba đường của lease | **KHỚP** |
| trần ADR-0044 `sensitive` | ≤ 3 tệp, ≤ 300 dòng thêm | **+234 / −2** | **KHỚP** |
| `AL_VER` khớp 4 chỗ trong `ci.yml` | 4 chỗ, `1.7.7` | `grep -nE 'AL_VER:'` ⇒ **4** dòng, **cả 4** = `1.7.7` | **KHỚP** |
| M1 — `doctor` ĐO `actionlint` + `shellcheck` | có | `doctor` in `khong actionlint` / `co shellcheck` | **KHỚP** |
| M1 — không tính vào `DUNG_DUOC` | có | `bat_buoc: False` cả hai | **KHỚP** |
| M2 — in cả khi xanh | có | `t150` ca 1 đo đúng điều đó | **KHỚP** |
| M5 — đo đường dẫn có dấu cách / ngoài ASCII | có | `t153` 3 ca dương + 2 ca âm | **KHỚP** |
| M6 — mỗi chốt một đột biến riêng | có | bảng `DOT_BIEN` có `m1_`, `m2_`, `m3_`, `m5_` | **KHỚP** |
| M3 — ba trạng thái `ĐÃ CHẠY`/`CHƯA CHẠY`/`KHÔNG ĐO ĐƯỢC` | có | ba nhãn **có mặt**, nhưng **gán SAI cả hai chiều** | **LỆCH — LỚP 1** |
| M4 — hook "ĐẶT" hai biến UTF-8 | có | biến chết theo tiến trình hook; phiên **không bao giờ** thấy | **LỆCH — LỚP 2** |

## BẢNG SĂN — 10 hướng, mỗi hướng lệnh + output thật

```
HƯỚNG 1: dấu vết TỰ TẠO BẰNG TAY có bị nhận là "hook đã chạy" không
  giả thuyết : nếu doctor chỉ hỏi tep.is_file() thì một tệp bất kỳ cũng cho ĐÃ CHẠY
  lệnh       : mkdir -p .claude/.packet_state && date -u > .../session-start.ran
               python3 .claude/dev/launcher.py doctor | grep hook-da-chay
  output     : DA_CHAY  hook-da-chay ĐÃ CHẠY (dấu vết: .claude/.packet_state/session-start.ran
               lúc 2026-09-16T18:56:21Z)          <-- hook CHƯA TỪNG chạy trong cây này
  kết luận   : LỖI

HƯỚNG 2: dấu vết CŨ 30 NGÀY có bị nhận là "hook đã chạy" không
  giả thuyết : nếu không đo độ tươi thì một dấu vết cũ bất kỳ vẫn cho ĐÃ CHẠY
  lệnh       : os.utime(dau_vet, now-30*86400); doctor | grep hook-da-chay
  output     : DA_CHAY  hook-da-chay ĐÃ CHẠY (dấu vết: ... lúc 2026-08-17T00:00:00Z)
  kết luận   : LỖI — nó CÓ mốc giờ trong tay, IN RA, mà không phán xét gì

HƯỚNG 3: hook CHẠY THẬT rồi thoát rc!=0 — doctor khai gì
  giả thuyết : nếu khối ghi dấu vết nằm SAU nhánh `exit 1` thì hook chạy mà không để dấu
  lệnh       : rm -rf .claude/.packet_state .tl_state
               bash .claude/hooks/session-start.sh ; echo rc=$?
               ls .claude/.packet_state/ ; doctor | grep hook-da-chay
  output     : hook rc=1   (đã cài xong actionlint, doctor sau đó thấy `co actionlint 1.7.7`)
               .claude/.packet_state/  -> RỖNG
               CHUA_CHAY  hook-da-chay CHƯA CHẠY — hook chua chay lan nao trong cay nay
  kết luận   : LỖI — chiều NGƯỢC lại của HƯỚNG 1/2. Sai cả hai chiều.

HƯỚNG 4: `export` trong hook có sống qua tiến trình hook không
  giả thuyết : nếu không, thì M4 "ĐẶT hai biến" không tới được phiên — tức không vá gì
  lệnh       : python3 -c "print(os.environ.get('PYTHONUTF8'))"   # trước
               bash .claude/hooks/session-start.sh
               python3 -c "print(os.environ.get('PYTHONUTF8'))"   # sau
  output     : truoc: PYTHONUTF8=None  PYTHONIOENCODING=None
               sau  : PYTHONUTF8=None  PYTHONIOENCODING=None
               doctor: CANH BAO chua dat du hai bien UTF-8
  kết luận   : LỖI — và đây là MỤC TIÊU CHÍNH của cả packet

HƯỚNG 5: actionlint cài xong thì PHIÊN có thấy không
  giả thuyết : `export PATH` trong hook chỉ sửa PATH của hook; nhánh lùi /tmp/actionlint
               không nằm trên PATH của phiên ⇒ cài xong mà phiên không dùng được
  lệnh       : python3 -c "'~/.local/bin' in PATH? ; '/tmp/actionlint' in PATH?"
  output     : ~/.local/bin CO tren PATH? True
               /tmp/actionlint CO tren PATH? False
  kết luận   : KHÔNG ĐO ĐƯỢC nhánh lùi — chạy dưới root nên `chmod 555` không chặn được
               `mkdir`, không ép được nhánh ấy. Tiền đề (PATH) thì ĐO ĐƯỢC.

HƯỚNG 6: ba đường ghi dấu vết có được gitignore không
  giả thuyết : ghi vào đường không ignore ⇒ bẩn `git status --porcelain`
  lệnh       : git check-ignore -q <từng đường>
  output     : IGNORED    .claude/.packet_state/session-start.ran
               IGNORED    .tl_state/session-start.ran
               KHONG IGN  .claude/session-start.ran        <-- nhánh thứ BA của hook
               KHONG IGN  .git/session-start.ran           <-- reader ĐỌC, writer KHÔNG ghi
  kết luận   : LỖI (tiềm ẩn + bất đối xứng)

HƯỚNG 7: `AL_VER` có thật sự khớp 4 chỗ trong ci.yml không
  lệnh       : grep -nE 'AL_VER' .github/workflows/ci.yml
  output     : 97: AL_VER: 1.7.7 · 199: · 634: · 698:   (4 dòng, cả 4 = 1.7.7)
  kết luận   : KHÔNG PHẢI LỖI — lời khai ĐÚNG

HƯỚNG 8: write set và trần ADR-0044
  lệnh       : git diff --numstat dd27441 8765d43
  output     : 87/2 launcher.py · 118/0 launcher_test.py · 29/0 session-start.sh
               => 3 tệp, +234/-2
  kết luận   : KHÔNG PHẢI LỖI — không ghi ra ngoài write set, không vượt trần

HƯỚNG 9: ca ĐỎ `t53` là hồi quy của packet hay đỏ sẵn
  giả thuyết : nếu đỏ sẵn trên nền thì không phải việc của packet này
  lệnh       : dựng CẢ HAI vế trong MỘT lệnh (clone + checkout + core.abbrev),
               rồi `launcher_test.py --lap-ca t53_doctor_bao_du_khi_du --lan 1`
  output     : nen (dd27441): rc=1 | LAP t53...: 0/1 qua, 0 bo qua, 1 hong
               sau (8765d43): rc=1 | LAP t53...: 0/1 qua, 0 bo qua, 1 hong
  kết luận   : KHÔNG PHẢI LỖI của packet — **delta = 0**

HƯỚNG 10: phép đối chiếu CHÉO mà lease bắt buộc chạy trên mã nào
  giả thuyết : nhánh neo dd27441 và chưa merge master ⇒ packet_loop_test là bản TRƯỚC #543
  lệnh       : git merge-base --is-ancestor f27a28f 8765d43 ; python3 packet_loop_test.py
  output     : KHONG (chưa merge master)
               nền: 282/282 đạt · BỎ QUA: 1 · PLT_RC=0
  kết luận   : LỖI (quy trình) — `282/282` là bộ TRƯỚC #543; master nay `291/291`
```

---

## LỚP 1 — `M3` ĐO SAI **CẢ HAI CHIỀU**: dấu vết ≠ "hook đã chạy cho phiên này"  **[P1]**

**TỆP/DÒNG:** `.claude/dev/launcher.py` `_do_hook_da_chay` · `.claude/hooks/session-start.sh` khối ghi dấu vết ở CUỐI tệp

**VẤN ĐỀ.** Đây là mục tiêu **trung tâm** của packet — `doctor` phải trả lời *"hook đã CHẠY chưa"*. Bản này trả lời sai theo cả hai chiều, mỗi chiều có phản chứng chạy được:

- **Dương tính giả (HƯỚNG 1, 2):** `_do_hook_da_chay` chỉ hỏi `tep.is_file()`. Một tệp **tự tạo bằng tay** ⇒ `ĐÃ CHẠY`. Một dấu vết **cũ 30 ngày** ⇒ vẫn `ĐÃ CHẠY`, và nó **in ra** mốc giờ `2026-08-17` mà không phán xét gì.
- **Âm tính giả (HƯỚNG 3):** khối ghi dấu vết nằm ở **cuối** `session-start.sh`, **sau** nhánh `exit 1` khi thiếu công cụ bắt buộc. Đo được: hook chạy, **cài xong actionlint**, thoát `rc=1`, **không để lại dấu vết nào** ⇒ `doctor` khai `CHƯA CHẠY` cho một lần hook **đã chạy**.

Hình dạng lỗi thì kho đã đặt tên rồi: `hook-phien` so **băm tệp** (*"tệp có mới không"*), và mục `KHA_NANG` mới so **sự tồn tại tệp** (*"đã từng có ai để lại dấu chưa"*). **Không cái nào trả lời câu hỏi được hỏi.** Đây đúng là *"đếm sự CÓ MẶT thay vì KHẢ NĂNG"* — lỗi mà chính Issue #546 trích ra để mở packet.

**Và bộ test KHOÁ hành vi sai lại.** `t151` ca (b) tạo dấu vết bằng tay rồi **khẳng định** `DA_CHAY` là đúng. Nên nó không chỉ bỏ sót lỗi — nó biến lỗi thành hợp đồng. Không ca nào phủ chiều âm tính giả.

**ĐÃ THỬ VÁ:** có — `HINT-546-luot1.patch`, đo được ba chiều (xem mục HINT).

**ĐỘ TIN:** cao.

---

## LỚP 2 — `M4` đặt biến trong tiến trình CON; PHIÊN không bao giờ thấy  **[P1 về mục tiêu, xếp P2 vì vá được ở chỗ khác]**

**TỆP/DÒNG:** `.claude/hooks/session-start.sh` — `export PYTHONUTF8=1` / `export PYTHONIOENCODING=utf-8`

**VẤN ĐỀ.** Cả packet sinh ra từ một phép đo: trên máy Windows của chủ kho, **không biến** ⇒ `109/148`, **hai biến UTF-8** ⇒ `126/148`. Bản vá đặt hai biến ấy **bên trong hook**. Hook là **tiến trình con**; `export` chết theo nó. Đo hai chiều (HƯỚNG 4): cha trước `None`/`None`, cha sau — vẫn `None`/`None`.

Nên với phiên gọi hook bằng `bash`, **con số `109/148` không đổi một ca nào**. Bản vá chỉ có tác dụng nếu ai đó `source` hook — và không tài liệu nào của packet nói phải làm thế.

**Nói cho công bằng:** hook **không thể** tự đặt biến cho phiên cha — đó là giới hạn của tiến trình, không phải cẩu thả. Cái sai là **lời khai**: `M4` viết *"ĐẶT hai biến"* và `t152` chỉ kiểm chuỗi `PYTHONUTF8=1` **có mặt trong tệp hook**, chứ không kiểm nó có tác dụng. Một chốt kiểm văn bản cho một khẳng định về hành vi.

**Hướng vá đề nghị (KHÔNG có trong HINT vì nó đụng thiết kế):** hook ghi vào dấu vết rằng nó *đã cố* đặt hai biến; `doctor` đọc dấu vết ấy, thấy hook có cố mà môi trường hiện tại vẫn thiếu ⇒ in đúng nguyên nhân (*"hook đặt biến nhưng biến chết theo tiến trình hook — phiên phải tự đặt, hoặc `source` hook"*) thay vì chỉ khuyên chung chung.

**ĐỘ TIN:** cao cho phép đo; **vừa** cho hướng vá (chưa chạy).

---

## LỚP 3 — cài công cụ rồi khai thành công, trong khi PHIÊN có thể không thấy  **[P2]**

**TỆP/DÒNG:** `.claude/hooks/session-start.sh`, khối `actionlint`

**VẤN ĐỀ.** `AL_DICH="${HOME}/.local/bin"`, lùi về `/tmp/actionlint` khi `mkdir` hỏng. Sau khi cài, hook `export PATH="$AL_DICH:$PATH"` **cho chính nó** rồi in `[session-start] actionlint: <ver>`. Nhưng `export` ấy chết cùng hook (cùng gốc LỚP 2).

Đo được (HƯỚNG 5): ở container này `~/.local/bin` **có sẵn** trên PATH nên cài xong phiên thấy — **do may của môi trường, không do hook**. `/tmp/actionlint` thì **không** trên PATH. Nên nhánh lùi tạo ra đúng *"CÓ MẶT ≠ DÙNG ĐƯỢC"*: hook in thành công, phiên vẫn mù.

**KHÔNG ĐO ĐƯỢC:** tôi **không ép được** nhánh lùi trong container này — chạy dưới `root` nên `chmod 555` không làm `mkdir` thất bại. Cơ chế đọc từ mã; tiền đề PATH thì đo được. Nói thẳng vậy thay vì khai đã chạy.

**ĐÃ THỬ VÁ:** có — HINT kiểm bằng PATH **gốc của phiên** (chụp trước khi hook tự nối PATH) và hạ xuống `CANH BAO` khi phiên không thấy.

**ĐỘ TIN:** vừa.

---

## LỚP 4 — nới một tập THẨM QUYỀN TOÀN CỤC để phục vụ một nhu cầu CỤC BỘ  **[P2]**

**TỆP/DÒNG:** `.claude/dev/launcher.py` — `DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC", "DA_CHAY"})`

**VẤN ĐỀ.** Tập này là **định nghĩa toàn cục** của *"khả năng đã được chứng minh"*, dùng ở `elif tt not in DA_CHUNG_MINH_KHA_DUNG: chua_chung_minh.append(...)` cho **mọi** `KHA_NANG`. Thêm `"DA_CHAY"` để một khả năng mới đi qua là nới luật chung cho một ca riêng.

Hôm nay vô hại — chỉ `hook-da-chay` trả `DA_CHAY`. Nhưng khối chú thích **ngay phía trên dòng ấy** cảnh báo đúng chuyện này: *"Sửa một đầu mà để đầu kia y nguyên thì chưa sửa gì"*. Và kho đã trả giá cho hình dạng *"nới danh sách"* nhiều lần.

**Hướng vá:** để **từng `KHA_NANG` tự khai** trạng thái nào tính là đã chứng minh (`"trang_thai_dat": {"DA_CHAY"}`), mặc định `{"DUNG_DUOC"}`. Luật chung không đổi; ca riêng khai ở chỗ riêng.

**ĐÃ THỬ NGHIỆM:** KHÔNG ĐO ĐƯỢC — chưa có `KHA_NANG` thứ hai trả `DA_CHAY` để dựng phản chứng. Đây là finding về **thiết kế**, không phải về hành vi hiện tại.

**ĐỘ TIN:** vừa.

---

## LỚP 5 — bất đối xứng writer/reader của danh sách đường dấu vết  **[P3]**

**TỆP/DÒNG:** `launcher.py` `_CAC_DUONG_VET_HOOK` (4 đường) · `session-start.sh` vòng `for d in ...` (3 đường)

**VẤN ĐỀ.** Hai danh sách **không khớp**, và lệch theo cả hai chiều:

- reader đọc `.git/session-start.ran` — writer **không bao giờ** ghi vào đó;
- writer có nhánh thứ ba `$GOC/.claude` — `git check-ignore` cho **KHÔNG IGNORE**, nên nếu nhánh ấy trúng thì hook **làm bẩn `git status --porcelain`**, đúng phép kiểm mà cross-review đòi phải rỗng. Chú thích ngay trên nó lại khai *"thư mục an toàn đã có trong .gitignore"* — **lời khai rộng hơn phép đo**.

Xác suất trúng nhánh ba thấp (hai nhánh đầu hầu như luôn `mkdir` được), nên P3 — nhưng nó là **bom hẹn giờ**, không phải lỗi thẩm mỹ.

**ĐÃ THỬ VÁ:** có — HINT rút cả hai danh sách về **đúng hai đường đã đo là được ignore**, và ghi lý do tại chỗ.

**ĐỘ TIN:** cao.

---

## LỚP 6 — phép đối chiếu CHÉO chạy trên mã test CŨ HƠN MASTER  **[P3, quy trình]**

**VẤN ĐỀ.** Lease đòi chạy `packet_loop_test.py` làm phép đối chiếu chéo vì bốn điểm nối với #543. Nhánh neo `dd27441` và **chưa merge master** (đo: `merge-base --is-ancestor f27a28f 8765d43` ⇒ KHÔNG). Nên bộ chạy là bản **TRƯỚC #543**: `282/282`. Master nay `291/291` — **9 ca mới** mà phép đối chiếu này **chưa từng thấy**.

Nó **qua** (`PLT_RC=0`), và điều đó không sai — nhưng nó **không chứng minh** thứ lease muốn nó chứng minh.

**Hướng vá:** merge `origin/master` vào nhánh packet rồi chạy lại; khi đã merge thì mốc A/B là **merge base**, không còn là `dd27441`.

**ĐỘ TIN:** cao.

---

## HINT PATCH

`HINT-546-luot1.patch` — **7 hunk**, **+106 / −22**, 10 020 B,
`sha256 a7bc102c586f7806fae0a5d7fd4472ba838b046c79dfdf615c5d4b4ebe991d20`.
Chạm **ba** đường, **cả ba đều trong write set** của lease: `launcher.py` · `launcher_test.py` · `session-start.sh`.

Áp được, đã chạy chứ không suy — từ gốc cây làm việc:
`patch -p0 --fuzz=0 --dry-run` ⇒ **rc=0**, rồi áp thật ⇒ **rc=0**.

**Phản chứng ĐỔI MÀU sau khi áp — ba ca, chạy thật:**

| ca | TRƯỚC vá | SAU vá |
|---|---|---|
| dấu vết **cũ 30 ngày** | `DA_CHAY` | **`KHONG_DO_DUOC`** — *"dau vet ... CU 720h (> 12h ...): no chung minh hook TUNG chay, khong chung minh hook chay cho phien nay"* |
| dấu vết **tươi** | `DA_CHAY` | `DA_CHAY` — **không bắt oan** |
| hook chạy rồi **thoát rc=1** | `CHUA_CHAY` (sai) | **`DA_CHAY`** — dấu vết nay ghi **SỚM**, trước mọi đường thoát |

### Bản HINT ĐẦU của tôi SAI, và bộ test của agy bắt được

Ghi ra đây vì nó nói một điều tốt về bộ test này. Bản HINT đầu chỉ chạm **hai** tệp và **làm đỏ `t117`**:

```
HONG t117_moi_mau_dot_bien_phai_khop_DUNG_MOT_cho:
  [('m3_doc_bam_tep_thay_vi_dau_vet', 'dem=0 mong=1', '    for rel in _CAC_DUONG_VET_HOOK:')]
```

Bản vá đổi `if tep.is_file():` thành `if not tep.is_file(): continue`, nên **mồi neo của đột biến `m3` chết** — đột biến không còn khớp chỗ nào. `t117` của agy tồn tại đúng để bắt chuyện đó, và nó bắt được. **Đổi mã thì phải đổi cả đột biến neo vào mã ấy**; tôi đã quên, bộ test thì không.

Bản HINT hiện tại vì thế chạm thêm `launcher_test.py` để:
1. cập nhật mồi neo `m3_doc_bam_tep_thay_vi_dau_vet` theo mã mới;
2. thêm ca `t154_m3_dau_vet_CU_KHONG_con_la_DA_CHAY` (ba nhánh: tươi ⇒ `DA_CHAY`, cũ ⇒ `KHONG_DO_DUOC`, không có ⇒ `CHUA_CHAY`);
3. thêm đột biến **riêng** `m3b_bo_kiem_do_tuoi_dau_vet` — gỡ ngưỡng độ tươi thì `t154` phải ĐỎ. Không có nó thì chốt mới **không có răng**, đúng thứ `M6` đòi.

### Phạm vi HINT — nói thẳng để không ai đọc rộng hơn

- Đóng **LỚP 1b** trọn vẹn, **LỚP 1a một phần**: dấu vết **cũ** hết được nhận, nhưng dấu vết **tự tạo và TƯƠI** thì **vẫn** cho `DA_CHAY`. Đóng nốt cần một khái niệm *"phiên"* mà kho chưa có — tôi **không bịa ra** ở đây.
- Đóng **LỚP 3** (chỉ hạ xuống `CANH BAO` khi phiên không thấy công cụ) và **LỚP 5** (rút hai danh sách về đúng hai đường đã đo là được ignore).
- **KHÔNG** đụng **LỚP 2** và **LỚP 4** — hai lớp thiết kế, chỉ có hướng vá bằng lời.
- **Đây là GỢI Ý, không phải chỉ thị.** Executor toàn quyền vá cách khác. Nhưng nếu áp gần nguyên bản thì **phải khai độ lệch số dòng** trong bàn giao ngược — ở #543 đúng việc này làm hai trong sáu lớp thành **vòng tròn** và `approve` phải hạ xuống `advisory_review`.

## CỔNG ĐÃ CHẠY TẠI CHỖ

| cổng | kết quả |
|---|---|
| `launcher_test.py` trên `8765d43` | `185/186 ca ĐÃ CHẠY QUA (tổng 187, bỏ qua 1, hỏng 1)`, rc=1 |
| — ca hỏng `t53_doctor_bao_du_khi_du` | **ĐỎ SẴN trên nền `dd27441`** (A/B dựng cùng một lệnh) ⇒ **delta = 0** |
| — ca bỏ qua `t62` | Windows-only; trên Linux bỏ qua là đúng |
| `packet_loop_test.py` (đối chiếu chéo) | `282/282 đạt · BỎ QUA 1`, **rc=0** — nhưng là bộ **trước #543**, xem LỚP 6 |
| `patch -p0 --fuzz=0` HINT | dry-run **rc=0**, áp thật **rc=0** |
| `launcher_test.py` trên cây ĐÃ ÁP HINT | `186/187 ca ĐÃ CHẠY QUA (tổng **188**, bỏ qua 1, hỏng 1)` — ca hỏng vẫn **chỉ** là `t53` (đỏ sẵn). Tổng 187 → **188**: **+1 ca mới** (`t154`), **0 hồi quy**, `t117` xanh trở lại |

## ASSURANCE — `advisory_review`, KHÔNG phải `cross_approved`

Hai lý do độc lập:

1. **Không có `session_run_id`.** Lượt này chạy TRONG phiên điều phối, không phải một tiến trình reviewer riêng neo bởi `launcher.py run`. Checkout riêng thì có thật (**clone** rời, detached tại `8765d43`); **context** thì không.
2. **Chính phiên này soạn spec r1 và ghi hộ lease g1** cho #546. Reviewer đang chấm việc thi công trên đặc tả do mình viết. Khác provider thì VẪN THẬT — diff do agy viết — nhưng độc lập thì chỉ một phần.

Và `antigravity` xuất hiện **0 lần** trong `docs/PROTOCOL_DA_PHIEN.md`, nên `cross_approved` **không khai được** dù muốn (nợ `PROTOCOL-CHUA-BIET-ANTIGRAVITY`). Lease đã khai `assurance_target: human_audited` từ đầu.

## CHƯA ĐO ĐƯỢC

| # | thứ | vì sao |
|---|---|---|
| K1 | nhánh lùi `/tmp/actionlint` của LỚP 3 | chạy dưới `root`, `chmod` không ép được `mkdir` hỏng |
| K2 | hành vi trên **Windows thật** | không có nền Windows trong phiên này; đã giao chủ kho phép thử ba biến thể V1/V2/V3 để đo LỚP 2 |
| K3 | LỚP 4 có hở thật không | chưa có `KHA_NANG` thứ hai trả `DA_CHAY` để dựng phản chứng |

---
_Generated by [Claude Code](https://claude.ai/code)_
