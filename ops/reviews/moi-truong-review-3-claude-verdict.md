verdict: changes_requested
reviewed_sha: 7412077d9fb7

# CROSS-REVIEW LƯỢT 3 — packet #546 `MOI-TRUONG-CONG-CU-DO-DUOC` r1/g1

| | |
|---|---|
| `reviewed_sha` | `7412077d9fb7` |
| `base_sha` (merge-base với `origin/master`) | `f27a28ffa3cc` · `numstat` **3 tệp, +296 / −3** |
| lượt trước | `b61b3ce472f8` — verdict lượt 2, `changes_requested`, `LỚP 2` + `LỚP 7` mở |
| kết luận | **`changes_requested`** — **BẢY lớp gốc đã xử lý xong**, nhưng **MỘT phát hiện MỚI**: `LỚP 8` [P2] |
| assurance | **`advisory_review`** |

## HIỆN VẬT ĐO, KÈM BĂM

Output thô của lượt chạy trên máy Windows của chủ kho, giải trực tiếp từ bản tải về — không gõ lại.
**Đã chuẩn hoá về LF trên đĩa** để `sha256` trên đĩa **bằng** `sha256` của blob (bài học lượt 2:
`.gitattributes` khai `* text=auto eol=lf`, nên tệp CRLF lưu vào git sẽ cho băm khác):

| tệp | sha256 (đĩa == blob) | bytes |
|---|---|---|
| `ops/reviews/moi-truong/windows-7412077-V4.log` | `6c35ee2c4ca8d6f246a014753499511bf1f72d0af8dcdcc86b05c702516376af` | 1084 |
| `ops/reviews/moi-truong/windows-7412077-TONGKET.txt` | `135e4c3aeb8a8b6961b7e95ee28db22cbb1af4dc4ed68e0986192ef8934176bb` | 664 |

`V0.log`–`V3.log` nằm ở `_HOP_NAP` trên Drive của chủ kho, không đưa vào kho.
**`V3.log` của lượt này KHÔNG dùng được** — xem `K1`.

## TÁM LỚP — trạng thái tại `7412077`

| lớp | trạng thái | phán quyết ĐỘC LẬP? |
|---|---|---|
| `LỚP 1a` | **đóng một phần** — dấu vết tự tạo mà TƯƠI vẫn `DA_CHAY`; thông điệp nay nêu nhánh | không (HINT) |
| `LỚP 1b` | đóng | không (HINT) |
| `LỚP 2` | **ĐÓNG** — lời khai đã khớp thực tế, có phép đo HÀNH VI · **mở nợ `HOOK-KHONG-DAT-DUOC-BIEN-CHO-PHIEN`** | **CÓ** |
| `LỚP 3` | đóng | không (HINT) |
| `LỚP 4` | **ĐÓNG** — `frozenset({"DUNG_DUOC"})` + đột biến riêng | **CÓ** |
| `LỚP 5` | đóng | không (HINT) |
| `LỚP 6` | đóng | **CÓ** |
| `LỚP 7` | **ĐÓNG** — xác nhận trên Windows THẬT | **CÓ** |
| `LỚP 8` **MỚI** | **MỞ** — bản vá `LỚP 7` không có chốt nào canh (đột biến SỐNG SÓT) | **CÓ** |

Năm lớp có phán quyết độc lập (lượt 2 chỉ có một), kể cả `LỚP 8` mới. Bốn lớp còn lại vẫn dính **vòng tròn HINT** — executor áp `HINT-546-luot1.patch` của chính reviewer này; phán quyết "đóng" cho `1a/1b/3/5` **không có giá trị độc lập**, và điều đó không đổi ở lượt này.

## LỚP 7 — ĐÓNG, xác nhận trên Windows

Mã, `session-start.sh`:

```
36  GOC="${CLAUDE_PROJECT_DIR:-...}"          <- doi LEN truoc cong
37  ghi_dau_vet_hook() { local nhan="${1:-chay}"; ... }
50  if [ "${CLAUDE_CODE_REMOTE:-}" != "true" ]; then
51    ghi_dau_vet_hook "cuc_bo" || true        <- GHI TRUOC khi thoat
53    exit 0
56  ghi_dau_vet_hook "remote" || echo "CANH BAO: ..."
```

Đo trên máy chủ kho (`MINGW64_NT-10.0-26200`, `/d/Quốc hội/tl546`, `CLAUDE_CODE_REMOTE` **không đặt**):

```
[session-start] khong phai moi truong remote — bo qua
=== HOOK RC = 0
CO_DAU_VET packet_state
DA_CHAY  hook-da-chay ĐÃ CHẠY (dấu vết: .claude/.packet_state/session-start.ran
         lúc 2026-09-17T09:50:29Z cuc_bo [bo qua theo thiet ke tren may cuc bo])
```

Ba điều tôi nêu ở lượt 2 đều có: dấu vết ghi **trước** cổng · ghi **NHÁNH ĐÃ ĐI** (`cuc_bo` / `remote`) · `_do_hook_da_chay` phân biệt hai nhánh trong thông điệp **mà vẫn giữ đúng ba nhãn của `A3`** ⇒ **không phải đi qua revision 2**. Đó là đường (A) tôi khuyến nghị, và chọn đúng.

### NHƯNG BẢN VÁ NÀY KHÔNG CÓ CHỐT NÀO CANH — `LỚP 8` [P2, MỚI]

Tôi tự dựng đột biến tái tạo đúng `LỚP 7`: gỡ **một dòng**, `ghi_dau_vet_hook "cuc_bo" || true`
(dòng 51), giữ nguyên mọi thứ khác — tức đưa dấu vết trở lại sau cánh cửa.

```
cay da dot bien: grep -c 'ghi_dau_vet_hook "cuc_bo"'  =>  0   (dong da bi go)
python3 .claude/dev/launcher_test.py
  => 186/187 ca DA CHAY QUA (tong 188, bo qua 1, hong 1)
  => ca hong DUY NHAT: t53_doctor_bao_du_khi_du  (DO SAN, khong lien quan)
```

**Giống hệt bản chưa đột biến.** Không ca nào đỏ. `t151` chạy trên cây tổng hợp (`San()`) nên không
thấy hook thật; `t152` có đọc hook thật nhưng chỉ kiểm `AL_VER`, hai chuỗi `export`, `cai_actionlint`,
`CANH BAO`, và phép đo biến ở tiến trình cha — **không mục nào chạm chuyện dấu vết ghi trước hay sau
cổng**.

Nên: **`LỚP 7` đã vá THẬT — Windows chứng minh — nhưng bản vá ấy không được canh.** Ai dọn dẹp hook,
đổi thứ tự, hay gộp hai lời gọi `ghi_dau_vet_hook` lại làm một sẽ **mở lại `LỚP 7` mà cổng vẫn xanh**.
Đúng nếp kho đã trả giá: *"cửa không có mutant là cửa sẽ âm thầm hở lại."*

**Hướng — đề xuất, không chỉ định.** Một ca đủ, và nó phải chạy trên **hook thật**: dựng cây tạm,
chép hook thật vào, chạy `bash hook` **không** đặt `CLAUDE_CODE_REMOTE`, rồi đòi tệp
`.claude/.packet_state/session-start.ran` **tồn tại** và nội dung chứa nhãn `cuc_bo`. Kèm một đột
biến trong bảng (`m7_bo_ghi_dau_vet_o_nhanh_chan`) gỡ đúng dòng 51 và neo vào ca ấy.

**VA CHẠM VỚI TRẦN, phải nói thẳng:** packet đang ở **`296 / 300`**, còn **4 dòng**. Một ca test tử tế
cộng một mục trong bảng đột biến **không vừa 4 dòng**. Nên `LỚP 8` **không đóng được trong phạm vi
hiện tại** — nó buộc phải đi một trong hai đường, và đó là quyết định của chủ kho:

- **(i) xin ngoại lệ ADR-0044** cho packet này rồi đóng `LỚP 8` tại chỗ; hoặc
- **(ii) khai `LỚP 8` thành nợ có tên** (`LOP7-VA-KHONG-CO-CHOT`) và đóng #546 ở đây, để packet sau
  làm — với hiểu biết rõ ràng rằng cho tới lúc ấy, `LỚP 7` **sống nhờ không ai đụng vào**, không
  phải nhờ một cổng.

Tôi nghiêng **(i)**: `LỚP 7` là lớp duy nhất trong bảy lớp được xác nhận bằng phép đo trên nền thật,
và để nó không có chốt là bỏ phí chính phép đo đắt nhất của cả chuỗi. Nhưng trần là thẩm quyền của
chủ kho, không phải của reviewer.

## LỚP 4 — ĐÓNG, độc lập với HINT

```
DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC"})      launcher.py:3795
```

`DA_CHAY` đã bị gỡ khỏi tập thẩm quyền TOÀN CỤC, nên `hook-da-chay` không còn nới cổng chung cho một nhu cầu cục bộ. Kèm đột biến riêng, có ca đích:

```
("m4_noi_long_da_chung_minh_kha_dung",
 ('DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC"})',
  'DA_CHUNG_MINH_KHA_DUNG = frozenset({"DUNG_DUOC", "DA_CHAY"})'),
 ["t149_doctor_do_actionlint_va_shellcheck"])
```

HINT của tôi **không chạm** lớp này ⇒ phán quyết độc lập. Lượt 2 ghi `K3` *"chưa dựng được phản chứng"*; nay executor tự dựng.

## LỚP 2 — ĐÓNG, kèm một NỢ CÓ TÊN

`t152` nay có phép đo **HÀNH VI**, không còn chỉ dò chuỗi trong tệp:

```python
p = subprocess.run([bash, "-c", f"unset PYTHONUTF8; '{hook_path.as_posix()}' >/dev/null 2>&1 || true; "
                                f"echo -n \"${{PYTHONUTF8:-<chua dat>}}\""], ...)
bang(p.stdout == "<chua dat>", f"tien trinh cha phai <chua dat>: {p.stdout}")
```

Nó chạy hook như **tiến trình con** rồi đọc biến ở **cha**, và **đòi `<chua dat>`** — tức **khoá đúng giới hạn tiến trình** thay vì khẳng định một thứ không đúng. Chốt này **đỏ được**: bất kỳ ai sửa hook theo hướng "làm cho cha thấy biến" mà không đổi cách gọi sẽ làm nó đỏ. Chú thích hook cũng đổi thành `(source hook de co o shell cha)`, tức lời khai nay khớp thực tế.

**Finding của lượt 1 là LỜI KHAI SAI, và lời khai đã đúng ⇒ đóng.**

**Nhưng nhu cầu gốc CHƯA ĐẠT, và tôi mở nợ có tên thay vì để nó chìm:**

> **`HOOK-KHONG-DAT-DUOC-BIEN-CHO-PHIEN`**
> Yêu cầu sinh ra packet này là *"môi trường luôn phải đủ công cụ, biến môi trường cần thiết để chạy"*.
> Trên đường gọi `bash .claude/hooks/session-start.sh`, phiên **vẫn không có** `PYTHONUTF8` /
> `PYTHONIOENCODING`. Đo được trên Windows, cùng một lượt:
> **V1** (đặt trực tiếp) `lease_publish: 133/148` · **V2** (hook là tiến trình con) **harness SẬP,
> giống hệt V0**. Ba đường đi tiếp, không đường nào miễn phí: `.claude/settings.json` (lease **cấm**,
> phải qua revision) · khai `source` là hợp đồng gọi hook (đổi hợp đồng, cần chủ kho duyệt) ·
> chấp nhận và chuyển sang packet khác. **Không thuộc phạm vi #546 như đặc tả đang khai.**

Quyết định đóng lớp này kèm nợ là **quyết định của chủ kho**, ghi lại ở đây để nó có mỏ neo.

## LỚP 1a — VẪN ĐÓNG MỘT PHẦN [P2, KHÔNG chặn]

`t151` nay có ba ca: (a) chưa dấu vết ⇒ `CHUA_CHAY`; (b) dấu vết `cuc_bo` ⇒ `DA_CHAY` + *"bo qua theo thiet ke"*; (c) dấu vết `remote` ⇒ `DA_CHAY` không kèm chữ ấy.

Phần chưa đóng **không đổi**: dấu vết **tự tạo bằng tay nhưng TƯƠI** vẫn cho `DA_CHAY`, và `t151` ca (b)/(c) vẫn khẳng định đó là đúng — cả hai ca đều dựng tệp bằng `write_text`, hook chưa từng chạy.

Đây là phạm vi tôi **đã tự khai** trong HINT lượt 1: đóng nốt cần khái niệm *"phiên"* mà kho chưa có. Nêu lại để nó nằm trong hồ sơ chứ không chỉ trong một patch: **`M3` đo *"có ai để lại dấu trong cây này gần đây không"*, không đo *"hook đã chạy cho PHIÊN NÀY chưa"*.** Không chặn `approve`, nhưng đừng đọc `DA_CHAY` mạnh hơn nghĩa của nó.

Một ghi chú nhỏ, không phải finding: `nhanh = "..." if "cuc_bo" in noi_dung else ""` phân biệt nhánh bằng **khớp chuỗi con**. Ở tập nhãn hiện tại (`cuc_bo`, `remote`) thì không va nhau; nếu sau này thêm nhãn thì nên so **trường đã tách**, không so chuỗi con.

## CỔNG ĐÃ CHẠY TẠI CHỖ (Linux @ `7412077`)

| cổng | kết quả |
|---|---|
| `launcher_test.py` | `186/187 (tổng 188, bỏ qua 1, hỏng 1)` |
| — ca hỏng `t53_doctor_bao_du_khi_du` | **ĐỎ SẴN** — A/B dựng **cả hai vế trong MỘT lệnh**: nền `f27a28f` `1 hong` · sau `7412077` `1 hong` ⇒ **delta = 0** |
| `packet_loop_test.py` (chéo, trong **CLONE**) | **`TỔNG: ĐẠT`**, rc=0 |
| `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` | **rc=0** cả bốn |

**Trần ADR-0044 `sensitive`: ≤ 3 tệp, ≤ 300 dòng thêm. Đang ở `296 / 300` — còn ĐÚNG 4 DÒNG.**
Chưa vượt. Nhưng bất cứ việc gì thêm ở packet này — kể cả vá `LỚP 1a` — gần như chắc chắn vượt ⇒
**xin ngoại lệ TRƯỚC khi đẩy**, đừng vá hờ để lách trần.

**Tạo tác của rig, nhắc lại vì nó sẽ lừa người sau:** `packet_loop_test` chạy trong **git worktree**
cho hàng loạt ca `void_*` ĐỎ với lý do `'workspace la git worktree; dung ban clone doc lap'`. Đó là
**rig**, không phải mã. Số dùng được phải lấy từ **clone**.

## CHƯA ĐO ĐƯỢC

| # | thứ | vì sao |
|---|---|---|
| K1 | `V3` (source hook) ở lượt Windows này | `V3.log` mang mốc `09:54:49`, **sau** `TONGKET.txt` (`09:51:07`) ⇒ hai lượt khác nhau, **không đọc chéo**. Con số `V3` của lượt này bỏ trống. |
| K2 | `LỚP 7` trên nhánh **remote** (`CLAUDE_CODE_REMOTE=true`) | chỉ đo nhánh `cuc_bo` trên máy cá nhân; nhánh `remote` có ghi dấu vết ở dòng 56 nhưng lượt này chưa chạy thật |
| K3 | `V1` thiếu mốc `=== RC =` ở lượt Windows này | lượt trước cũng thế, dựng phép thử tổng hợp **không tái hiện được**; không đoán |

## MỘT LỖI CỦA CHÍNH BỘ ĐO NÀY — khai để không ai đọc nhầm `TONGKET.txt`

`TONGKET.txt` của lượt Windows in:

```
V4 : rc_bash=0  LOP 7 TAI HIEN — hook bo qua o dong 40  |  CO dau vet
```

**Nhãn `LOP 7 TAI HIEN` là SAI.** Bộ phân loại của tôi khớp chuỗi `"khong phai moi truong remote"`
**trước**, mà chuỗi ấy **vẫn phải có** ở bản ĐÃ VÁ — chính sách dòng 38 không đổi và không nên đổi.
Thứ phân biệt là **DẤU VẾT**, không phải thông điệp. Kết luận trong verdict này **không** dựa vào
dòng tổng kết ấy; tôi đọc thẳng `V4.log`.

Đây là lỗi báo cáo **thứ bảy** của bộ đo do tôi viết trong chuỗi này (`H1`–`H6` đã khai ở các lượt
trước). Cùng một hình dạng lặp bảy lần: **phần ĐO thì đúng, phần BÁO CÁO thì nói dối.** Theo chính
luật của kho, lặp lần thứ ba trở lên thì câu hỏi đúng là *"có nên làm thế này không"* — nên nếp tôi
áp từ lượt 2: **sau khi có số, đọc thẳng từ log, không tin dòng tổng kết của mình.**

## ASSURANCE — `advisory_review`, KHÔNG phải `cross_approved`

Ba lý do độc lập:

1. **Vòng tròn HINT** — `LỚP 1a/1b/3/5` được vá bằng chính patch của reviewer.
2. **Không có `session_run_id`** — lượt review chạy trong phiên điều phối; checkout riêng có thật
   (worktree + clone detached tại `7412077`), context thì không.
3. **`antigravity` xuất hiện 0 lần** trong `docs/PROTOCOL_DA_PHIEN.md` ⇒ `cross_approved` **không
   khai được** dù mọi lớp đã đóng. Nợ `PROTOCOL-CHUA-BIET-ANTIGRAVITY`.

Lý do (3) là **trần cứng**: nó không phụ thuộc chất lượng công việc của executor. Muốn #546 đạt
`cross_approved` thì phải sửa PROTOCOL trước, và đó là việc của một packet khác.
