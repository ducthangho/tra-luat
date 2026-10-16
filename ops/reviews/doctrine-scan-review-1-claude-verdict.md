# VERDICT — `DOCTRINE-SCAN-DAO-SANG-DANH-SACH-CHO-PHEP` (#543) r1/g1, lượt 1

| trường | giá trị |
|---|---|
| `reviewed_sha` | `67587639bf06092afbc025d5848ea989f057317a` (đầu nhánh `agy/doctrine-scan-r1-g1`) |
| `tree_oid` | `9d11526a13b77373384234f5457c6d1f97293f78` |
| `base` | `19de56693d06813e6743a30113d0fb87bff3e196` |
| `spec_hash` | `60dbefa1f617be36ecd4ac93743d9def0ddc063f06ae09e7af0e002c7c80b0cf` — ĐÃ ĐO, khớp bản đóng băng |
| executor | `google_antigravity` |
| reviewer | `anthropic_claude`, phiên điều phối (xem `chua_do_duoc`) |
| **kết luận** | **`changes_requested`** — 2 lớp P1, 1 lớp P2, 2 lớp P3 |
| ngày | 2026-09-16 |

Phân theo **LỚP**, không theo thể hiện riêng lẻ. Mỗi lớp liệt kê **HẾT cửa vào đã tìm được**,
mỗi cửa một phép đo. Đọc `rc` TRỰC TIẾP, không qua pipe.

---

## Việc agy làm ĐƯỢC — đo trước khi chê

| phép đo | kết quả |
|---|---|
| `doctrine-scan --root .` trên head agy | `rc=0` · `sạch — đã quét 7 tệp, 0 chỗ chép doctrine` |
| `adr-song --root .` | `rc=0` · `48 ADR / 48 dòng §20, khớp 1–1` |
| `packet_loop_test.py` trên head agy | `rc=0` · **287/287** |
| A/B cùng rig clone, dựng trong MỘT lệnh | nền `dd27441` **282/282** → head agy **287/287**; **+5 ca, 0 hồi quy** |
| ghi ngoài write set | **không** — 5 tệp chạm đều nằm trong `write_set` của lease |
| lease | byte-identical bản đã đăng; hạn `2026-09-17T10:57:23Z`, còn hiệu lực |
| A1 chiều DƯƠNG | chép 25 từ nguyên văn ⇒ `rc=6`, bắt đúng |
| A4 ca ÂM | adapter chỉ gồm con trỏ (`§3.2`, `assurance_target`…) ⇒ `rc=0`, không bắt oan |
| A5 một phần | agy CÓ mỏ neo đột biến `bo_kiem_chep_protocol` cho cơ chế mới |

Cơ chế n-gram **có răng thật**. Các lớp dưới đây nói về chỗ nó KHÔNG có răng, không phải
về việc nó vô dụng.

---

## LỚP 1 — FAIL-OPEN: *"không đọc được"* bị nuốt thành *"không có"* · **P1**

`_doc_nguon_protocol` trả `[]` cho **bốn tình huống khác hẳn nhau**, rồi người gọi viết
`if proto_words:` — nên cả bốn thành *"bỏ qua trong im lặng"*. Cổng báo **sạch** trong khi
adapter chép nguyên văn 25 từ.

**Bốn cửa, đo được từng cửa** (adapter chép 25 từ nguyên văn trong mọi ca; đối chứng
protocol thật cho `rc=6`, nên phép đo có răng):

| cửa | tình huống | `rc` | bắt chép? |
|---|---|---:|---|
| 1 | protocol vắng ở `--root` **và** vắng ở đích fallback | **0** | không |
| 2 | protocol có nhưng **không phải UTF-8** | **0** | không |
| 3 | protocol đọc được nhưng **ngắn hơn ngưỡng n-gram** | **0** | không |
| 4 | protocol chỉ gồm **code fence** ⇒ rỗng sau khi bỏ fence | **0** | không |

> **Cửa 1 suýt thành tín dụng giả.** Lần đo đầu nó cho `rc=1`; kiểm lại thì đó là
> `ModuleNotFoundError: launcher` — bản sao script cô lập không import được, tức chết vì
> **lỗi vô can**. Phải chép trọn `.claude/dev/` mới đo đúng, và khi ấy nó là `rc=0`.

**Vì sao đây là P1 chứ không phải nit:** chính hàm `cmd_doctrine_scan` đã **fail-CLOSE** cho
tệp ĐÍCH — `except (OSError, UnicodeDecodeError) as e: _die(RC_ARG, ...)`. Hàm mới đặt chính
sách **NGƯỢC LẠI** cho tệp NGUỒN, **cùng một cặp ngoại lệ**, cách nhau mười lăm dòng. Không
phải quên một ca hiếm — là đảo một quy ước đang hiện diện ngay trên màn hình.

Và nó vi phạm chốt ba trạng thái của kho: `có` · `không` · **`KHÔNG ĐO ĐƯỢC`**, trong đó
trạng thái thứ ba phải làm cổng **ĐỎ**. `CLAUDE.md`: *"một cổng tự tắt khi thiếu công cụ là
cổng không tồn tại đúng lúc nó cần nhất"*.

**Độ phủ test: 0/4.** Năm ca agy thêm không ca nào đi đường này.

---

## LỚP 2 — ĐỌC RA NGOÀI `--root`, và nó ĐANG ĐỠ CHO CHÍNH BỘ TEST · **P1**

`_doc_nguon_protocol` lùi về `Path(__file__).resolve().parents[2] / "docs" / ...` — tức kho
chứa **SCRIPT**, không phải cây đang quét. Hệ quả: **`--root` không điều khiển cơ sở so sánh**.
Quét cây X có thể âm thầm đo theo protocol của cây Y, và người chạy không có cách nào biết.

Cùng hình dạng với lỗi `t24` đã ghi nguyên văn trong `CLAUDE.md` (*"`t24` trỏ
`HERE.parent.parent` nên tìm thư mục workflow ở TRÊN gốc kho"*).

**Chỗ đắt hơn — bộ test của chính lượt này đang đứng trên nó.** `_repo_gia` chỉ dựng
`.claude/skills/<tên>/SKILL.md`, **không bao giờ** dựng `docs/PROTOCOL_DA_PHIEN.md`. Nên:

| đột biến | ca ĐỎ | ca vô can bị kéo theo |
|---|---|---|
| gỡ khối fallback `parents[2]` | `doctrine_scan_chep_tron_5_1_bi_chan`, `doctrine_scan_chep_doan_ngan_5_1_bi_chan` | `void_*`, `doi_chieu_*`, `stdout_cp*` — đỏ vì cây sao chép thiếu `.git`, **tín dụng giả, không tính** |

Hai ca ấy khai *"chép §5.1 vào adapter ⇒ ĐỎ"*. Thứ chúng thật sự đo là *"chép văn bản tình cờ
có trong protocol của KHO THẬT ⇒ ĐỎ"*. Cây dưới `--root` chỉ góp phần adapter.

---

## LỚP 3 — CA CÓ MẶT KHÁC CA CÓ ĐO · **P2**

Đột biến **tắt trọn** cơ chế n-gram mới (`if proto_words:` → `if False:`), giữ nguyên 28 cụm cấm:

| ca của agy | dưới đột biến | đo cơ chế mới? |
|---|---|---|
| `doctrine_scan_chep_tron_5_1_bi_chan` | **ĐỎ** | có |
| `doctrine_scan_chep_doan_ngan_5_1_bi_chan` | **ĐỎ** | có |
| `doctrine_scan_chep_12_bi_chan` | **vẫn XANH** | **KHÔNG** |
| `doctrine_scan_adr_0048_...` (ca âm) | xanh | đúng thiết kế |
| `doctrine_scan_con_tro_thuan_tuy_xanh` (ca âm) | xanh | đúng thiết kế |

`chep_12` được thoả bởi **cơ chế CŨ** (đoạn §12 dính một trong 28 cụm cấm). Nó khai phủ A1
nhưng sẽ xanh **kể cả khi toàn bộ cơ chế mới bị xoá**. Spec A1 đòi ba đầu vào; thực đo chỉ
**hai** trong ba chạm tới thứ packet này thêm vào.

*(Hai ca đỏ khác dưới đột biến — `moc_dot_bien_phai_khop_DUNG_MOT_CHO` và
`đột biến bo_kiem_chep_protocol` — là tạo tác của chính đột biến tôi dựng, không phải phát hiện.)*

---

## LỚP 4 — HẰNG KHÔNG CÓ CĂN CỨ · **P3**

`threshold = 15 if is_claude_md else 10`. Spec không đòi bất đối xứng này, mã không giải thích
nó, và nó **nới cổng đúng ở tệp doctrine lớn nhất kho**. Một hằng không khai điều kiện đo sẽ
trôi mà không ai biết — `CLAUDE.md` có nguyên một mục về việc ấy.

Không chặn `approve`, nhưng phải **khai lý do bằng số** hoặc bỏ về một ngưỡng duy nhất.

---

## LỚP 5 — LỜI KHAI ĐỊNH DANH KHÔNG TRA ĐƯỢC · **P3**

Handoff §7 khai `head_sha: f53ac68ed780e9b2b726e0443a3c222d514cd9c1` và
`tree_oid: 630290f8ee0d3cd216cff0cd9c5e1a288903ccf1`. **`git cat-file -e` cho cả hai: KHÔNG
TRA ĐƯỢC.** Head thật `67587639…`, tree thật `9d11526a…`.

Khối handoff là **mỏ neo** của §7. Một mỏ neo trỏ vào object không tồn tại thì tệ hơn không có
mỏ neo: nó khai một định danh mà người đọc tin. Lượt review này neo vào head THẬT.

---

## HINT patch

`ops/reviews/doctrine-scan/HINT-543-luot1.patch` — sha256
`fde1b894c923e8f314e452de818b5eebfcff8fbe7ff3811d0687e4602d342e67`, 7 751 B, 7 hunk,
**+62 / −15** trên 2 tệp. `git apply --check -p1` trên head `6758763`: **áp được**.

Nó đóng LỚP 1 và LỚP 2 **cùng lúc**, vì hai lớp ấy vướng vào nhau: gỡ fallback mà không sửa
`_repo_gia` thì hai ca test đỏ ngay.

| thay đổi | đóng lớp |
|---|---|
| `_doc_nguon_protocol` **fail-close** cả bốn cửa, mỗi cửa một thông điệp `KHÔNG ĐO ĐƯỢC` riêng | 1 |
| thêm `_PROTO_TU_TOI_THIEU = 200` — nguồn nghèo hơn ngưỡng là *chưa đo*, không phải *sạch* | 1 (cửa 3, 4) |
| bỏ nhánh `if proto_words:` (nay luôn khác rỗng) — giữ lại là mở cửa thứ năm | 1 |
| **bỏ hẳn** fallback `parents[2]` | 2 |
| `_repo_gia` luôn dựng `docs/PROTOCOL_DA_PHIEN.md` dưới `--root` | 2 |
| nguồn **TRUNG TÍNH** làm mặc định; ca nào đo hành vi chép thì truyền protocol thật **tường minh** | 2 |
| cập nhật mỏ neo đột biến `bo_kiem_chep_protocol` theo dòng đã đổi | 1 |

**Đo sau khi áp hint:**

| phép đo | trước | sau |
|---|---|---|
| 4 cửa fail-open | `rc=0` cả bốn | **`rc=2` + `KHÔNG ĐO ĐƯỢC`** cả bốn, không traceback |
| `packet_loop_test.py` | 287/287 | **287/287, `rc=0`** |

> **Bản hint đầu của tôi SAI và tôi giữ lại vết.** Bản ấy để `co_protocol=True` làm **mặc
> định** và chép protocol THẬT vào mọi cây giả ⇒ **36** phép kiểm đột biến ĐỎ, vì ba ca đối
> chứng (`doctrine_scan_sach_xanh`, `ac18_nfkc_hai_cham_toan_rong`, `ac19_oan_claude_md_master`)
> không còn độc lập với đường đọc protocol. Đúng hình dạng *"vá một lỗ mà mở lỗ khác"* mà
> `CLAUDE.md` tố cáo — và nó chỉ lộ vì đã CHẠY. Bản nộp dùng nguồn trung tính làm mặc định.

**Hint KHÔNG đụng LỚP 3, 4, 5** — chúng cần quyết định của executor, không nên vá hộ:
`chep_12` phải đổi đầu vào để thật sự chạm cơ chế mới; ngưỡng 15 phải khai lý do bằng số;
handoff phải khai lại định danh tra được.

---

## Chưa đo được

| thứ | vì sao |
|---|---|
| **Mức assurance của lượt này** | Không phóng được reviewer độc lập: `codex` kiểm sống HỎNG `rc=1` (ảnh chụp token 165,6h bị vòng xoay vô hiệu) + hết quota; `claude` **CHƯA_XÁC_THỰC**; `doctor --kiem-song` `rc=12`. Lượt này chạy TRONG phiên điều phối, **không có `session_run_id`**. Vì thế biên nhận khai `advisory_review`, **KHÔNG** khai bất kỳ mức nào thuộc `ASSURANCE_CAN_DOC_LAP`. Khác provider thì VẪN THẬT: diff do agy viết. |
| **A6 của spec** | Đòi *"cross-review khác nền (reviewer `claude`)"*. Chưa thoả vì lý do trên. §8:668 cho `sensitive` đòi **Codex** `cross_approved` hoặc `human_audited`; `antigravity` xuất hiện **0 lần** trong protocol. Nợ có tên: `PROTOCOL-CHUA-BIET-ANTIGRAVITY`. |
| **A7 đủ bộ** | Lượt này chạy `doctrine-scan`, `adr-song`, `packet_loop_test`. Chưa chạy `doc-claims-check --strict`, `release-verify --strict`, `bien_nhan_v2` trên head agy — chúng thuộc nghĩa vụ của executor trước khi báo xong. |
| **Ngưỡng 15 có nới thật bao nhiêu** | Chưa dựng được ca đo *"đoạn chép dài 10–14 từ trong `CLAUDE.md`"* để lượng hoá. LỚP 4 vì thế là P3 theo LÝ LẼ, không theo số. |

## Ghi chú

Spec A6 của #543 yêu cầu verdict vào `ops/reviews/doctrine-scan/` — **thư mục CON**. Đó đúng
caveat `HIEN-VAT-TRONG-THU-MUC-CON-NAM-NGOAI-TAM-BA-CONG` vừa được đóng ở `r374`
(`bien_nhan_v2` dòng 879 và 989, `t26`/`t27` đều glob **tầng đầu**). Tệp verdict này vì thế đặt
ở **tầng đầu** `ops/reviews/`; HINT patch — không phải hiện vật cổng chấm — để trong thư mục con.
Đây là phát hiện về chính đặc tả, nêu ra để revision sau sửa.

Nguồn có thẩm quyền là **tệp có băm** này. Comment GitHub chỉ là bản chiếu.
