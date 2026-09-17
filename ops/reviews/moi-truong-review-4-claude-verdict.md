verdict: changes_requested
reviewed_sha: 81f7067c6f16

# CROSS-REVIEW LƯỢT 4 — packet #546 `MOI-TRUONG-CONG-CU-DO-DUOC` r1/g1

| | |
|---|---|
| `reviewed_sha` | `81f7067c6f16` |
| `base_sha` | `f27a28ffa3cc` · `numstat` **3 tệp, +308 / −3** |
| lượt trước | `7412077d9fb7` — lượt 3, `LỚP 8` mở |
| kết luận | **`changes_requested`** — `LỚP 8` **ĐÓNG, có răng trên Windows THẬT**; nhưng **MỘT hồi quy MỚI**: `LỚP 9` [P2] |
| assurance | **`advisory_review`** |

## HIỆN VẬT ĐO, KÈM BĂM

Output thô của lượt chạy trên máy Windows của chủ kho, giải trực tiếp từ bản tải về — không gõ lại,
**đã chuẩn hoá về LF** nên `sha256` trên đĩa **bằng** `sha256` của blob (bài học lượt 2):

| tệp | sha256 (đĩa == blob) | bytes |
|---|---|---|
| `ops/reviews/moi-truong/windows-81f7067-TONGKET-lop8.txt` | `278b20b7b6d0667b57a4494319d09b009490e5a77a3e99374c74647b1379f5d3` | 814 |

`N1`–`N4` log đầy đủ nằm ở `_HOP_NAP` trên Drive của chủ kho. Mọi trích dẫn từ chúng trong verdict
này đều nguyên văn, tra lại được.

## TÔI RÚT MỘT DỰ ĐOÁN

Cuối lượt 3 tôi nói với chủ kho rằng lượt này *"dự kiến **`approve`**"*. **Sai, và tôi rút.**
Packet gây một hồi quy do chính nó (`LỚP 9`), và nó chỉ lộ ra khi đo trên **đường dẫn thật** của
chủ kho. Dự đoán ấy dựa trên bằng chứng Linux ở đường dẫn sạch — đúng thứ lượt này chứng minh là
không đủ.

## `LỚP 8` — ĐÓNG, xác nhận trên Windows THẬT

`t155_m3_hook_cuc_bo_ghi_dau_vet_truoc_cong_remote` chạy trên **hook thật**: trỏ `CLAUDE_PROJECT_DIR`
vào sandbox, `unset CLAUDE_CODE_REMOTE`, đòi tệp dấu vết **tồn tại** và trường thứ hai **là `cuc_bo`**.

Hai đột biến, chạy trên `MINGW64_NT-10.0-26200`, `D:\Quốc hội\tl546`, head `81f7067c6f16`:

```
N2 (nen)                          : 1/1 qua, 0 bo qua, 0 hong  =>  DAT
N3 (go dong ghi dau vet o nhanh chan): 0/1 qua, 0 bo qua, 1 hong  =>  DAT — dot bien BI GIET
N4 (giu ghi dau vet, BO nhan cuc_bo) : 0/1 qua, 0 bo qua, 1 hong  =>  DAT — dot bien BI GIET
```

Bộ đo **tự chứng minh đột biến đã áp** (`dem dong truoc = 1` · `sau = 0` ở cả N3 lẫn N4), nên
"sống sót" không thể bị nhầm với "chưa áp". Hai khẳng định, hai đột biến riêng, mỗi cái giết đúng
ca đích. **Đây là thứ lượt 3 đòi và lần này có thật** — khác hẳn `7412077` nơi gỡ cùng dòng ấy mà
không ca nào đỏ.

## `LỚP 9` [P2, MỚI] — hai tính năng của CÙNG packet này đánh nhau

`t150_doctor_do_bien_utf8_in_ca_khi_xanh` (ca của `M2`, **do packet này thêm**) khẳng định:

```python
bang(rc == 0 and "BIEN UTF-8" in "\n".join(in_dong) and "CANH BAO" not in "\n".join(in_dong),
     "xanh in du khong canh bao")
```

`"CANH BAO" not in` **toàn bộ** đầu ra `doctor`. Nhưng `M5` — **cũng của packet này** — in đúng chữ
`CANH BAO` khi đường dẫn kho có dấu cách hoặc ký tự ngoài ASCII.

Phản chứng **một biến**, chạy trên Linux, cùng một commit, chỉ đổi đường dẫn:

| đường dẫn chạy từ | `t150` |
|---|---|
| `…/scratchpad/wt81` (ASCII, **không** dấu cách) | **1/1 qua** |
| `…/duong ASCII/tl546` (**có dấu cách**, vẫn ASCII) | **0/1 qua, 1 hỏng** |
| `…/Quốc hội/tl546` (dấu cách + ngoài ASCII) | **0/1 qua, 1 hỏng** |

Bắt được dòng gây ra:

```
rc = 0
co 'BIEN UTF-8' ? True
co 'CANH BAO'   ? True    <-- t150 doi phai FALSE
   CANH BAO DUONG DAN: duong dan kho chua dau cach ('/…/duong ASCII/tl546')
```

Nên ca ấy **xanh trên CI** (đường sạch) và **đỏ trên máy chủ kho** — đúng nền packet nhắm tới.

Cùng họ `LỚP 6` (*chuỗi phủ định chứa chuỗi khẳng định*) nhưng ở dạng khác: **một khẳng định quá
RỘNG, khớp cả cảnh báo không liên quan**. Và trớ trêu đúng chỗ đáng nhớ — `M5` sinh ra để phát
hiện đường dẫn có dấu cách, rồi chính nó làm đỏ một ca của `M2`.

**Hướng vá — đề xuất, không chỉ định.** Hỏi *"không có `CANH BAO` **về biến UTF-8**"* thay vì
*"không có `CANH BAO` nào"*: neo `CANH BAO` và `UTF-8` trên **cùng một dòng**, hoặc kiểm mục
`bien_utf8` trong `doctor --json` — ca đã có sẵn dòng đọc JSON ấy. Ước lượng **1–3 dòng**.

**Phản chứng bắt buộc trước khi đẩy:** chạy `t150` từ một đường dẫn **có dấu cách**. Không có phép
thử ấy thì không biết bản vá có đóng được `LỚP 9` hay chỉ đang xanh nhờ đường dẫn sạch.

## BA CA HỎNG trên Windows — phân loại, không gộp

`N1` (bộ test trọn vẹn trên Windows): `169/172 ca ĐÃ CHẠY QUA (tổng 189, bỏ qua 17, hỏng 3)`.

| ca | có ở base `f27a28f`? | phán |
|---|---|---|
| `t53_doctor_bao_du_khi_du` | **có** | **ĐỎ SẴN** — A/B dựng hai vế trong MỘT lệnh, delta 0 |
| `t73_doctor_phai_do_bash_va_npm` | **có** | **ĐỎ SẴN trên Windows** — chết vì `UnicodeDecodeError: 'charmap' codec can't decode byte 0x90` trong `subprocess._readerthread` ⇒ stdout về `None` ⇒ `json.loads(None)` `TypeError`. Đúng lớp `L4`, và đúng nợ `HOOK-KHONG-DAT-DUOC-BIEN-CHO-PHIEN` |
| `t150_doctor_do_bien_utf8_in_ca_khi_xanh` | **KHÔNG — ca MỚI của packet này** | **`LỚP 9`**, hồi quy do chính packet |

Nói rõ để không ai gộp ba con số ấy thành "packet làm hỏng ba ca": **hai đỏ sẵn, một mới.**

## CHÍN LỚP tại `81f7067`

| lớp | trạng thái | phán quyết ĐỘC LẬP? |
|---|---|---|
| `LỚP 1a` | **đóng một phần** — dấu vết tự tạo mà TƯƠI vẫn `DA_CHAY` | không (HINT) |
| `LỚP 1b` | đóng | không (HINT) |
| `LỚP 2` | **ĐÓNG** + nợ `HOOK-KHONG-DAT-DUOC-BIEN-CHO-PHIEN` | **CÓ** |
| `LỚP 3` | đóng | không (HINT) |
| `LỚP 4` | **ĐÓNG** | **CÓ** |
| `LỚP 5` | đóng | không (HINT) |
| `LỚP 6` | đóng | **CÓ** |
| `LỚP 7` | **ĐÓNG** — xác nhận Windows | **CÓ** |
| `LỚP 8` | **ĐÓNG** — xác nhận Windows, hai đột biến bị giết | **CÓ** |
| `LỚP 9` **MỚI** | **MỞ** — hồi quy do chính packet | **CÓ** |

Sáu lớp có phán quyết độc lập. Bốn lớp còn lại vẫn dính **vòng tròn HINT** — executor áp
`HINT-546-luot1.patch` của chính reviewer này; điều đó không đổi ở lượt này.

## CỔNG ĐÃ CHẠY TẠI CHỖ

| cổng | nền | kết quả |
|---|---|---|
| `launcher_test.py` | Linux @ `81f7067` | `187/188 (tổng **189**, bỏ qua 1, hỏng 1)` — ca hỏng duy nhất `t53`, **đỏ sẵn** |
| `launcher_test.py` | **Windows @ `81f7067`** | `169/172 (tổng 189, bỏ qua 17, hỏng 3)` — phân loại ở bảng trên |
| `packet_loop_test.py` (chéo, **CLONE**) | Linux | **`TỔNG: ĐẠT`**, rc=0 |
| `doctrine-scan` · `adr-song` · `doc-claims-check --strict` · `git diff --check` | Linux | **rc=0** cả bốn |

Tổng ca 188 → **189** (đúng **+1**: `t155`).

**Trần ADR-0044 sau ngoại lệ chủ kho: ≤ 3 tệp / ≤ 340 dòng thêm. Đang ở `308 / 340` — còn 32 dòng.**
Vá `LỚP 9` ước 1–3 dòng ⇒ **thừa sức**, không cần xin thêm.

## MỘT LỖI CỦA CHÍNH BỘ ĐO NÀY — khai để không ai đọc nhầm

Bản đầu của script đo `LỚP 8` báo `N3 / N4 : KHÔNG ĐẠT — ĐỘT BIẾN SỐNG SÓT`, tức **suýt khai
`LỚP 8` chưa đóng** trong khi đo tay cho thấy đã đóng. Nguyên nhân truy được:

```
$env:TEMP tren Linux = []   (RONG)
Join-Path $env:TEMP "…"  ->  Cannot bind argument to parameter 'Path' because it is null
```

Đường dẫn tạm rỗng ⇒ **đột biến không hề được áp** ⇒ ca chạy trên bản gốc và tất nhiên xanh ⇒
script kết luận "sống sót". Đúng bệnh *"ca có MẶT khác ca có ĐO"*, lần này nằm trong bộ đo.

Chữa **bằng cách bỏ cả lớp**, không vá `$env:TEMP`: toàn bộ *copy + đột biến + chạy* dồn vào **một
tải trọng bash** dùng `mktemp -d`, và tải trọng **tự đếm dòng trước/sau** rồi thoát mã riêng nếu
lệch. Nay không còn cách nào báo "sống sót" cho một đột biến chưa áp — trường hợp ấy ra
`KHÔNG ĐO ĐƯỢC`.

Đây là lỗi báo cáo **thứ tám** của bộ đo do tôi viết trong chuỗi này, và là lần đầu nó suýt **lật
ngược một kết luận đúng**. Nếp đang áp từ lượt 2 giữ nguyên: **đọc thẳng từ log, không tin dòng
tổng kết của mình.**

## CHƯA ĐO ĐƯỢC

| # | thứ | vì sao |
|---|---|---|
| K1 | `LỚP 7`/`LỚP 8` trên nhánh **remote** (`CLAUDE_CODE_REMOTE=true`) | chỉ đo nhánh `cuc_bo`; dòng 56 có ghi dấu vết `remote` nhưng chưa chạy thật |
| K2 | `t150` hỏng trên Windows **chỉ** vì `LỚP 9`, hay còn nguyên nhân thứ hai | phản chứng Linux tái hiện đủ bằng dấu cách; chưa tách riêng phần ngoài-ASCII trên Windows |
| K3 | `t155` bỏ qua im lặng khi thiếu `bash` | nhánh `if not bash: return "bo qua vi khong co bash"` — trên cả hai nền đã đo đều có bash, nên chưa dựng được ca âm. **P3**, không chặn |

## ASSURANCE — `advisory_review`

**Vòng tròn HINT** (`1a/1b/3/5`) · **không có `session_run_id`** · **`antigravity` xuất hiện 0 lần**
trong `docs/PROTOCOL_DA_PHIEN.md` ⇒ `cross_approved` **không khai được**. Lý do thứ ba là **trần
cứng**, đang được xử bằng packet riêng (#551, spec đã đóng băng, chưa cấp lease).

## ĐIỀU ĐÁNG GHI CHO HỒ SƠ

`LỚP 9` là **lần thứ ba** trong chuỗi #546 mà phát hiện đắt nhất đến từ **chạy trên nền thật**, không
từ đọc mã: `LỚP 7` (chủ kho chạy PowerShell), `LỚP 2` (V2 ≡ V0 trên Windows), nay `LỚP 9` (đường dẫn
có dấu cách). Cả ba đều **xanh trên CI**.

Cụ thể hơn cho `LỚP 9`: CI chạy ở đường dẫn sạch, nên ca ấy sẽ **xanh vĩnh viễn trên CI** và **đỏ
vĩnh viễn trên máy chủ kho**. Một cổng chỉ đỏ ở nơi không ai nhìn là cổng sẽ bị bỏ qua — và ở đây
"nơi không ai nhìn" lại chính là **máy của người giữ kho**.
