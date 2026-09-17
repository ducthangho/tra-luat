verdict: changes_requested
reviewed_sha: b61b3ce472f8624c0d23875fc24c7437e284f09e

# CROSS-REVIEW LƯỢT 2 — packet #546 `MOI-TRUONG-CONG-CU-DO-DUOC` r1/g1

| | |
|---|---|
| `reviewed_sha` | `b61b3ce472f8624c0d23875fc24c7437e284f09e` |
| `base_sha` (merge-base với `origin/master`) | `f27a28ffa3cc` |
| lượt trước | `8765d43a` — verdict lượt 1, `changes_requested`, 6 LỚP; bổ sung `LỚP 7` sau đó |
| kết luận | **`changes_requested`** — **2 LỚP còn mở** (`LỚP 2` P1 · `LỚP 7` P1), **1 LỚP đóng MỘT PHẦN** (`LỚP 1a`), `LỚP 4` chưa đụng |
| assurance | **`advisory_review`** — xem mục cuối, có một vòng tròn phải khai |

## HIỆN VẬT ĐO, KÈM BĂM

Hai tệp dưới đây là **output thô** của lượt chạy trên máy Windows của chủ kho, giải trực tiếp
từ bản tải về — không gõ lại.

**Một điều phải khai, vì nó suýt thành một băm sai trong hồ sơ:** bản gốc dùng **CRLF**; kho có
`.gitattributes` khai `* text=auto eol=lf`, nên git **chuẩn hoá về LF khi lưu**. Băm tính trên tệp
CRLF **không khớp** blob (`V4`: `1 119 B` → `1 098 B`; `TONGKET`: `611 B` → `597 B`). Bảng dưới
ghi băm của **thứ ĐÃ LƯU**, tức thứ `git show <ref>:<đường dẫn> | sha256sum` trả về:

| tệp | sha256 (blob, LF) | bytes |
|---|---|---|
| `ops/reviews/moi-truong/windows-b61b3ce-V4.log` | `02c34fbe5f0c0bffe470ad82f523b90b83787e36396d5e6f556ae4e9a39dbf3b` | 1 098 (gốc CRLF 1 119) |
| `ops/reviews/moi-truong/windows-b61b3ce-TONGKET.txt` | `58e0998595cd7dc286ac46ae1820bd0d56cedf5a81b25a91a14c0df6bc2c71ad` | 597 (gốc CRLF 611) |

Nội dung **không đổi một ký tự**; chỉ dạng xuống dòng đổi, và điều đó được khai ra thay vì để
người kiểm tự vấp phải.

`V0.log`–`V3.log` (19 KB – 137 KB) **không** đưa vào kho — chúng nằm ở `_HOP_NAP` trên Drive của
chủ kho. Mọi trích dẫn từ chúng trong verdict này đều kèm **số dòng**, tra lại được.

## ĐIỀU PHẢI KHAI TRƯỚC MỌI THỨ KHÁC — VÒNG TRÒN

Executor áp `HINT-546-luot1.patch` của **chính reviewer này** gần như nguyên bản. Đo được, không suy:

```
_HAN_DAU_VET_HOOK_GIAY = 12 * 3600        launcher.py:3659   <- nguyen van tu HINT
_CAC_DUONG_VET_HOOK = (hai duong)         launcher.py:3656   <- nguyen van tu HINT
PATH_GOC="$PATH"                          session-start.sh:44 <- nguyen van tu HINT
ghi_dau_vet_hook()                        session-start.sh:55 <- nguyen van tu HINT
t154_m3_dau_vet_CU_KHONG_con_la_DA_CHAY   launcher_test.py:6021 <- nguyen van tu HINT
m3b_bo_kiem_do_tuoi_dau_vet               launcher_test.py:7001 <- nguyen van tu HINT
```

Nghĩa là với `LỚP 1a` · `LỚP 1b` · `LỚP 3` · `LỚP 5`, **reviewer đang chấm bản vá của chính mình**. Ở #543 đúng chuyện này làm hai trong sáu lớp thành vòng tròn và `approve` phải hạ xuống `advisory_review`. Phán quyết "đóng" cho bốn lớp ấy **không có giá trị độc lập** — coi như executor đã chép một lời giải được đưa sẵn, và người chấm là người đưa.

**Hai lớp KHÔNG dính vòng tròn** — và cũng là hai lớp còn mở — là `LỚP 2` và `LỚP 7`: HINT không chạm tới chúng. Trọng lượng của lượt này nằm ở đó.

## ĐIỀU MỚI CỦA LƯỢT NÀY: có số từ WINDOWS THẬT

Lượt 1 đo trên Linux trong container. Lượt này chủ kho chạy trên máy Windows của chính mình, và đó là lần đầu trong chuỗi #546 reviewer có số từ đúng nền mà packet nhắm tới.

```
os     : Microsoft Windows 10.0.26200
pwsh   : 7.6.6
bash   : C:\Program Files\Git\bin\bash.exe   (uname = MINGW64_NT-10.0-26200)
kho    : D:\Quốc hội\tl546   (worktree detached tai b61b3ce472f8)
AL_VER : 1.7.7
luc    : 2026-09-17T15:33:08+07:00
```

Năm biến thể, khác nhau **đúng một biến** là "hai biến UTF-8 có tới được shell chạy bộ test hay không":

| biến thể | cách đặt biến | kết quả |
|---|---|---|
| **V0** nền | không đặt | **harness SẬP** — không in nổi dòng tổng kết |
| **V1** | `export` TRỰC TIẾP trong shell chạy test | **`lease_publish: 133/148 đạt; đã chạy=148, bỏ qua=7`**, `=== RC = 1` |
| **V2** | chạy hook như TIẾN TRÌNH CON | **harness SẬP** — giống hệt V0 |
| **V3** | `source` hook vào chính shell | **`133/148`** |
| **V4** | (không chạy bộ test) | hook **bỏ qua ở dòng 40**, không để lại dấu vết |

`133/148` **khớp đúng con số CI Windows** mà bàn giao lease đã ghi, và 15 ca đỏ trong `V1.log` **trùng khít danh sách** ấy (`t129`–`t133`, `t136`, `t138`, `t139`, `t144`–`t147`, `t149`–`t151`). Hai đường đo độc lập ra cùng một số ⇒ rig của lượt này đo đúng thứ CI đo.

## LỚP 2 — `M4` đặt biến trong tiến trình CON [P1, CÒN MỞ]

Bằng chứng sạch nhất có thể, **ba dòng trong cùng một tệp `V2.log`**, cách nhau 15 dòng:

```
:45  PYTHONUTF8      : 1             <- doctor CUA HOOK, ben trong tien trinh hook
:58  === HOOK RC = 0                 <- hook chay xong, thanh cong
:60  PYTHONUTF8       = <chua dat>   <- TIEN TRINH CHA, ngay sau do
:83  UnicodeDecodeError: 'charmap' codec can't decode byte 0x90 in position 135
```

Hook đặt được biến **cho chính nó**; tiến trình cha không nhận được gì; rồi bộ test sập đúng lỗi cp1258 mà hai biến ấy sinh ra để chặn.

Phản chứng hai chiều, trên cùng một máy, cùng một lượt: **V2 ≡ V0** (cùng sập), **V2 ≢ V1** (V1 ra `133/148`). Nếu V2 ra `133/148` thì `LỚP 2` sai và tôi phải rút; nó không.

`M4` khai *"hook ĐẶT hai biến"*. Hook không đặt được cho ai, trừ khi có người `source` — và không tài liệu nào của packet nói phiên sẽ `source` hook.

**Hiện trạng mã, `b61b3ce`:** `export PYTHONUTF8=1` / `export PYTHONIOENCODING=utf-8` vẫn nguyên ở `session-start.sh:48-49`. `t152` vẫn chỉ kiểm **chuỗi có mặt trong tệp** (`"PYTHONUTF8=1" in hook_txt`) — một chốt đo VĂN BẢN cho một khẳng định về HÀNH VI.

**Công bằng với executor:** hook *không thể* đặt biến cho tiến trình cha. Đó là giới hạn của tiến trình, không phải cẩu thả. Cái sai nằm ở **lời khai**, và ở chỗ chốt không thể đỏ.

**Hướng — đề xuất, không chỉ định.** Ba đường tôi thấy, và không đường nào miễn phí:
1. Đổi lời khai `M4` cho khớp thứ nó làm được, và đổi `t152` thành phép đo HÀNH VI (chạy hook như con, đọc biến ở cha, **đòi `<chua dat>`** — tức khoá đúng giới hạn thay vì khoá một ảo tưởng).
2. Chuyển việc đặt biến sang chỗ thật sự tới được phiên: `.claude/settings.json` — nhưng lease **cấm** đụng tệp đó, nên đây là phát hiện về chính đặc tả, phải đi qua revision mới.
3. Khai `source` là cách gọi bắt buộc — V3 chứng minh nó chạy (`133/148`), nhưng nó đổi hợp đồng gọi hook và cần chủ kho duyệt.

## LỚP 7 — `M4` đặt thiết bị đo sau một cánh cửa đóng sẵn [P1, CÒN MỞ]

`V4.log`, trên Windows, tại `b61b3ce`:

```
=== PWD   : /d/Quốc hội/tl546
=== UNAME : MINGW64_NT-10.0-26200
so dong hook = 641
CLAUDE_CODE_REMOTE (sau khi go) = <chua dat>
[session-start] khong phai moi truong remote — bo qua
=== HOOK RC = 0
KHONG_CO_DAU_VET packet_state
KHONG_CO_DAU_VET tl_state
CHUA_CHAY  hook-da-chay CHƯA CHẠY — hook chua chay lan nao trong cay nay
```

`so dong hook = 641` xác nhận đúng head đã áp HINT. Chốt `CLAUDE_CODE_REMOTE != "true"` ở **dòng 38**, `exit 0` ở **dòng 40**; `ghi_dau_vet_hook` ở **dòng 55**, tức **vẫn sau cánh cửa**. Trên máy cá nhân, `_do_hook_da_chay` trả `CHUA_CHAY` **vô điều kiện** — chạy hook bao nhiêu lần cũng thế.

Chốt dòng 38 là **chính sách có chủ đích** (*"Máy cá nhân đã có sẵn công cụ theo ý người dùng; cài đè vào đó là vượt quyền"*), có sẵn trên `origin/master`, **không phải executor thêm**. Cái sai là **chọn sai phương tiện**: packet sinh ra để đo môi trường Windows CỤC BỘ, mà thiết bị đo lại gắn vào một tệp remote-only theo thiết kế.

**Và HINT của tôi cũng không cứu chỗ này** — tôi dời khối ghi dấu vết lên sớm nhưng vẫn sau dòng 38. Tôi đóng cửa `exit 1` (thiếu công cụ) và bỏ sót cửa `exit 0` (không remote), hai cửa cùng hình dạng.

**Hướng — đề xuất.** Ba điều tôi cho là phải có: (a) dấu vết ghi **trước** dòng 38; (b) dấu vết ghi **NHÁNH ĐÃ ĐI**, không chỉ mốc giờ; (c) `_do_hook_da_chay` phân biệt *"chạy và cài"* với *"chạy rồi bỏ qua theo thiết kế"* — trên máy cá nhân, bỏ qua là trạng thái **LÀNH**, báo `CHUA_CHAY` cho nó là **báo động giả**.

**Chú ý thẩm quyền:** `A3` đã đóng băng khai **đúng ba nhãn**. Thêm nhãn thứ tư là đổi acceptance ⇒ **revision 2** theo §3.2. Muốn khỏi revision thì giữ ba nhãn và để thông điệp nói ra nhánh đã đi.

## LỚP 1a — ĐÓNG MỘT PHẦN, và phần còn lại vẫn được `t151` khẳng định là ĐÚNG [P2]

Đã đóng: dấu vết **CŨ** không còn cho `DA_CHAY` (`_HAN_DAU_VET_HOOK_GIAY = 12h`, `launcher.py:3659`), có ca `t154` và đột biến riêng `m3b_bo_kiem_do_tuoi_dau_vet`.

**Chưa đóng:** dấu vết **TỰ TẠO BẰNG TAY nhưng TƯƠI** vẫn cho `DA_CHAY`. Và `t151` ca (b) (`launcher_test.py:5982-5985`) tạo tệp bằng `write_text` rồi **khẳng định `DA_CHAY` là đúng** — hook chưa từng chạy trong cây ấy.

Đây là phạm vi tôi **đã tự khai** trong HINT lượt 1 (*"đóng nốt cần khái niệm phiên mà kho chưa có, tôi không bịa"*). Nêu lại ở đây vì nó phải nằm trong hồ sơ chứ không chỉ trong một patch: **`M3` vẫn không trả lời được câu nó được hỏi** — nó đo *"có ai để lại dấu trong cây này gần đây không"*, không đo *"hook đã chạy cho PHIÊN NÀY chưa"*.

## LỚP 4 — CHƯA ĐỤNG [P2]

`DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC", "DA_CHAY"})` (`launcher.py:3797`) vẫn nới tập THẨM QUYỀN TOÀN CỤC cho một nhu cầu CỤC BỘ. Executor không khai đã đóng (commit chỉ nêu `1a/1b/3/5/6`), nên đây là **khai đúng**, không phải bỏ sót âm thầm. Vẫn còn mở.

Lượt 1 ghi `K3`: chưa dựng được phản chứng vì chưa có `KHA_NANG` thứ hai trả `DA_CHAY`. **Nay đã có** — `hook-da-chay` chính là nó. Nên lớp này giờ **đo được**, và lượt sau không còn cớ để `KHÔNG ĐO ĐƯỢC`.

## LỚP 3 · LỚP 5 · LỚP 6 — ĐÓNG (nhưng 3 và 5 dính vòng tròn)

- **LỚP 3** đóng: `PATH_GOC="$PATH"` (`:44`) + kiểm trong shell sạch `env -u PATH PATH="$PATH_GOC"` (`:185`). *Bản vá từ HINT của reviewer.*
- **LỚP 5** đóng: `_CAC_DUONG_VET_HOOK` còn đúng **hai** đường, cả hai đều được gitignore; hết bất đối xứng writer/reader. *Bản vá từ HINT của reviewer.*
- **LỚP 6** đóng **độc lập với HINT**: `packet_loop_test.py` trên cây này đến từ `a743189` (bản sau #543), không còn là bản cũ hơn master; và chạy thật trong **clone** tại `b61b3ce` cho **`TỔNG: ĐẠT`**, rc=0. Đây là lớp duy nhất trong bốn lớp "đã đóng" mà phán quyết của tôi **có giá trị độc lập**.

## CỔNG ĐÃ CHẠY TẠI CHỖ (Linux, worktree tại `b61b3ce`)

| cổng | kết quả |
|---|---|
| `launcher_test.py` | `186/187 ca ĐÃ CHẠY QUA (tổng 188, bỏ qua 1, hỏng 1)`, rc=1 |
| — ca hỏng `t53_doctor_bao_du_khi_du` | **ĐỎ SẴN**: A/B dựng **cả hai vế trong MỘT lệnh** ⇒ nền `f27a28f` `0/1 qua, 1 hong` · sau `b61b3ce` `0/1 qua, 1 hong` ⇒ **delta = 0** |
| `doctrine-scan` | **rc=0** |
| `adr-song` | **rc=0** — *48 ADR trên đĩa, 48 dòng §20, khớp 1–1* |
| `doc-claims-check --strict` | **rc=0** (`core.abbrev=7`) |
| `git diff --check` | **rc=0** |
| `packet_loop_test.py` (đối chiếu CHÉO, chạy trong **CLONE**) | **`TỔNG: ĐẠT`**, rc=0 |
| `numstat` vs `f27a28f` | **3 tệp, +284 / −2** |

**Trần ADR-0044 `sensitive`: ≤ 3 tệp, ≤ 300 dòng thêm.** Đang ở **284** ⇒ còn **16 dòng**. Vá `LỚP 2` + `LỚP 7` gần như chắc chắn vượt ⇒ **DỪNG và xin ngoại lệ TRƯỚC khi đẩy**, đúng điều kiện dừng của lease. Đừng vá hờ để lách trần.

**Một tạo tác của rig, ghi ra để không ai đọc nhầm:** `packet_loop_test.py` chạy trong **git worktree** cho hàng loạt ca `void_*` ĐỎ với lý do `'workspace la git worktree; dung ban clone doc lap'` — `chay_cac_probe()` từ chối worktree theo thiết kế. Đó là **rig**, không phải mã. Số dùng được phải lấy từ **clone**.

## CHƯA ĐO ĐƯỢC — đừng đọc thành "đã loại trừ"

| # | thứ | vì sao |
|---|---|---|
| K1 | `V3` thiếu mốc `=== RC =` dù bộ test đã in `133/148` | dựng phép thử tổng hợp (CRLF lẫn LF) **không tái hiện được**; không có lời giải, không đoán |
| K2 | `V3` ra `133/148` qua đường "khớp đầu tiên" | chưa đối chiếu với đuôi `V3.log`; `V1` thì **đã** đối chiếu và khớp |
| K3 | `LỚP 4` có hở THẬT không | nay đã có ứng viên phản chứng (`hook-da-chay`) nhưng lượt này chưa dựng |
| K4 | `LỚP 7` trên nền remote (`CLAUDE_CODE_REMOTE=true`) | chỉ đo trên máy cá nhân; nhánh remote chưa đo ở lượt này |

## ASSURANCE — `advisory_review`, KHÔNG phải `cross_approved`

Ba lý do độc lập:

1. **Vòng tròn HINT** — bốn trong sáu lớp "đã đóng" được vá bằng chính patch của reviewer (mục đầu).
2. **Không có `session_run_id`** — lượt review chạy trong phiên điều phối; checkout riêng có thật (worktree + clone detached tại `b61b3ce`), context thì không.
3. **`antigravity` xuất hiện 0 lần trong `docs/PROTOCOL_DA_PHIEN.md`** ⇒ `cross_approved` **không khai được** dù muốn. Nợ có tên: `PROTOCOL-CHUA-BIET-ANTIGRAVITY`. Lease đã khai `human_audited` từ đầu.

Thêm một điều đáng ghi cho hồ sơ: **`LỚP 7` không do lượt review tìm ra** — nó đến từ một lượt chạy PowerShell của chủ kho trên máy thật. 10 hướng săn của lượt 1 không hướng nào chạm tới, vì tất cả đo trên Linux nơi `CLAUDE_CODE_REMOTE=true`. Đó là bằng chứng bằng số cho luận điểm *"reviewer không đo được thì review chỉ là soát chính tả"*: năng lực ĐO mở ra cả một LỚP, không phải nỗ lực đọc.
