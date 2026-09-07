**Tiêu đề:** `LO-319-LINUX-BANG-CHUNG-XANH — bịt lỗ "0/0 bi giet" ở chính vị từ, không ở từng mẫu`

> **CHƯA ĐỦ ĐIỀU KIỆN BẮT TAY.** Issue này công bố đặc tả đã đóng băng để chủ kho quyết định.
> Hai điều kiện chưa thoả, ghi ở mục cuối. Đừng cấp lease trước khi đọc mục ấy.

## Vấn đề đo được

`bang_chung_xanh(text, mau)` (`.claude/dev/ci_dang_ky_test.py:205`) chỉ soi **hai nhóm bắt** của
regex — mà ở `MOI` hai nhóm ấy là cặp số **CA**. Cặp số **đột biến** nằm ngoài nhóm bắt nên **không
bao giờ được nhìn tới**. Đo 17:45Z 06-09-2026 trên `1b3caa1`, gọi thẳng hàm:

| đầu vào (nền Linux; mẫu `pretooluse` đòi cả dòng kết `TONG: DAT` — bản đầu của bảng bỏ dòng ấy nên hai hàng đầu thật ra trả `False`, finding P2 `issue-chep-nham-du-lieu-va-chan-doan-cu` lượt 6) | hôm nay | đúng ra |
|---|---|---|
| `TONG: CA 39/39 dat · DOT BIEN 34/34 bi giet` + `TONG: DAT` | `True` | `True` |
| `TONG: CA 39/39 dat · DOT BIEN 0/0 bi giet` + `TONG: DAT` | **`True`** ⛔ | `False` |
| `TONG: CA 0/39 dat · DOT BIEN 34/34 bi giet` + `TONG: DAT` | `False` | `False` |

`DOT BIEN 0/0 bi giet` là đúng hình dạng *"tập rỗng thoả `not song`"* mà bài học **#319** sinh ra để
chặn. Lỗ có sẵn **từ trước** #456: #456 bịt phía **Windows** và **cố ý không** bịt phía Linux vì M4
của nó đóng băng hành vi Linux — cross-review lượt 1 bắt đúng chỗ này và bản vá phải lùi (`426bfc0`).

**Lỗ chạm 2 mục `MOI`** — `pretooluse_guard_test.py:38` và `subagent_ghi_detect_test.py:39`, **cùng
một chuỗi regex**, hai dòng kề nhau. Trên cả sổ: **13** cặp `n/m`, **7** đã kiểm, **6** chưa
(đơn vị: số lần xuất hiện `\d+/\d+` trong span). `probe_mang_test.py` (0 nhóm bắt) được tha **hoàn
toàn**: 3 cặp, 0 kiểm.

## Cái BẪY — vì sao phải vá ở vị từ, không ở từng mẫu

Mệnh đề `len(m.groups()) != 2` trả `True` **vô điều kiện** cho mọi mẫu có số nhóm khác 2. Nên cách
hiển nhiên nhất — bắt cặp đột biến thành nhóm 3/4 — làm hàm **ngừng kiểm cả cặp CA**:

```
mẫu 2 nhóm, "CA 0/39 · DOT BIEN 0/0"  -> False   (đúng)
mẫu 4 nhóm, "CA 0/39 · DOT BIEN 0/0"  -> True    (SAI, đo 17:45Z 06-09-2026)
```

Hôm nay chưa mẫu nào có 1/3/4 nhóm nên mệnh đề ấy **đang ngủ**; nó thức dậy đúng lúc ai đó vá theo
hướng hiển nhiên.

## §12 — hình dạng này đã hỏng BỐN LẦN, và câu hỏi thuộc CHỦ KHO

**Đây là phần quan trọng nhất của Issue.** Trong sáu vòng soạn + năm lượt cross-review, cùng một
nguyên nhân gốc — *số làm bằng chứng đến từ vùng mà hợp đồng không khoanh* — tái phát **bốn lần**,
qua bốn thiết kế: **A-b → A-c → T → T'**. Reviewer khác nền hạ được **cả bốn**.

Thiết kế hiện tại trong đặc tả là **H**, tức **bản thứ NĂM**. `PROTOCOL §12` nói: *"Cùng hình dạng
lỗi xuất hiện lần thứ ba bắt buộc xem lại có nên tiếp tục cách làm đó, không chỉ vá lần thứ tư."*

Đặc tả **không tự trả lời** câu ấy. Nó đặt lên bàn **ba lựa chọn** (`:205-211`) — (1) tiếp H trong
write set 1 tệp · (2) mở revision đổi **bên IN**, 9 tệp, vượt trần `sensitive` `ADR-0044` · (3) dừng
packet và tách lại — kèm **năm điều kiện đo được Đ1–Đ5** (`:221-227`) làm chốt tự động chuyển hướng.

**Chủ kho ĐÃ CHỌN 07-09-2026: lựa chọn (1) — tiếp H.** Dấu vết bền: https://github.com/ducthangho/tra-luat/issues/464#issuecomment-5567158069; khi cấp lease, `granted_on_instruction` neo vào đó.

## Bằng chứng cho H — và giới hạn của bằng chứng ấy

Executor đo H: **0 đỏ giả / 0 bỏ sót** trên 311 hàng có kỳ vọng qua bốn bộ ca; 16/16 ca selector của
verdict lượt 4 trả `1`; đột biến trả selector cũ giết 16/16; `mH13` khai thẳng là **mã chết** `0/311`.
Reviewer khác nền tự viết bộ tấn công riêng: **163 ca + 256 ca vét cạn = 419 ca, 0 hỏng**, và xác
nhận độc lập `mH13` là mã chết.

**Đọc đúng mức:** `419` ca không hỏng là bằng chứng về **BỘ CA**, không phải bằng chứng H đúng — các
bộ ca do bên bị đo và bên đo cùng nghĩ ra, và reviewer chỉ chạy được ~10 phút trước khi chết vì hạ
tầng. Ba lượt trước nó hạ được A-c và T' bằng ca mà bộ ca trước đó **không có**.

Executor tự khai **5 ranh giới H chưa đóng** (`chua_do_duoc` #1): `54/54/0` khi grammar khai `/\d+` ·
`039/39` · chữ số Unicode `３９/３９` · số 5000 chữ số ⇒ `ValueError` · `nhanh` `0/0 (xong)`.
Không formatter hiện có in ca nào trong năm ca ấy.

Ca 5000 chữ số nay có **tiêu chí A9** riêng: `chay_moi` phải trả `1` và **không ném ngoại lệ**, số mục
được xét = 8. Lý do là ngoại lệ không bắt **giết cả bộ** ⇒ mất phán quyết của 7 định dạng còn lại.
Nói cho đúng mức: đó là **fail-closed** (`rc=1` ⇒ cổng ĐỎ), **không** phải cổng vắng mặt. **Đính chính
theo finding P2 `a9-khai-sai-base-ngoai-le` (lượt 6):** BASE cũng gọi `int()` trên nhóm bắt, nên số
5000 chữ số nằm ở cặp **CA** làm BASE ném `ValueError` y hệt H (reviewer đo cả hai vế: `BASE=H=ValueError`);
khi số dài nằm ở cặp **đột biến** — vùng BASE không nhìn tới — BASE **không ném và nhận xanh** (`chay_moi`
trả `0`; lượt 7 đo: `BASE=0, H=ValueError` — bản trước của câu này viết "trả `1`", SAI, finding P2 lượt 7).
A9 vì vậy là tiêu chí chẩn đoán cho H, không phải một hồi quy so với BASE.

## Phạm vi

**1 tệp**: `.claude/dev/ci_dang_ky_test.py`. `rg -n 'bang_chung_xanh'` ngoài tệp ấy ⇒ **0** kết quả.
**`MOI`/`MOI_WINDOWS` theo đúng thiết kế H của đặc tả** (bản đầu của Issue viết *"không sửa một ký tự nào"* —
trái với chính đặc tả, finding P1 `issue-lo-giu-rang-buoc-cu` lượt 6): **chuỗi regex `SPAN` giữ NGUYÊN
VĂN 8/8**, còn **kiểu giá trị đổi** thành cặp `(SPAN, TONG)` (mục *"Thiết kế H"* luật 1–2). Ba chốt của
cross-review #456 được **neo lại** theo mục *"Ca đang khoá"* của đặc tả: `p456-mau-linux-KHONG-DOI-so-voi-base`
so phần `SPAN` (`MOI[_P456][0] == _MAU_BASE456`) + hằng canonical của `TONG`;
`p456-linux-A-B-tung-dau-vao-khop-base` khai đúng ba giá trị mới thay vì `is` bằng nhau; ca
`p456-linux-nhan-0-tren-0-Y-HET-base` **đảo chiều và đổi tên**, không bị xoá.

## Ràng buộc

- Mọi phản chứng đi qua chính `chay_moi`, **không** gọi thẳng `bang_chung_xanh` — khuyết tật "làm
  tròn" nằm ở nơi TIÊU THỤ (bài học r6/#401, đã trả giá ba lần trong đúng tệp này).
- Mỗi tiêu chí nghiệm thu nêu **đơn vị**.
- **Không đụng `.github/workflows/ci.yml`**, và **không** đề xuất nâng `timeout-minutes`
  (`PROTOCOL §12`, điều kiện DỪNG — đã nâng 2 lần, 3 mức: `25 → 45 → 60`).

## HAI ĐIỀU KIỆN CHƯA THOẢ — đọc trước khi cấp lease

> **⚠ ĐÍNH CHÍNH 09:3xZ 07-09-2026 — câu nói về `WebSocket` ngay dưới đây là SAI.**
> `codex doctor` đo trực tiếp: WS handshake tới đúng endpoint ấy **THÀNH CÔNG** (`HTTP 101
> Switching Protocols`), và `respect system proxy: disabled` ⇒ codex **không đi qua** proxy kia.
> `Connection refused (os error 111)` là **CHẬP CHỜN**, nguyên nhân **chưa biết** — không phải
> chính sách chặn. Cross-review lượt 6 VÀ lượt 7 đều đã chạy được ở đúng môi trường này.
> Chi tiết + tự phê: `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md` mục ĐÍNH CHÍNH.

**(1) Chưa có `cross_approved`.** Lượt 5 **chết năm lần** vì hạ tầng — chữ ký `Connection refused (os error 111)` trên đường tái kết nối WebSocket của `codex`. **Đính chính 03:55Z 07-09-2026:** chẩn đoán *"proxy không cho `WebSocket upgrades`"* ở bản đầu là **SAI** (`codex doctor`: handshake `HTTP 101`, codex không đi qua proxy egress); nguyên nhân thật **CHƯA BIẾT**, đường codex **mở nhưng chập chờn**. Lượt 6 (07-09-2026, phóng có giám sát) đã chạy trọn. Kết quả lượt 6 trên
`reviewed_sha` `2adb681`: `changes_requested`, 7 P1 / 4 P2. Cho packet này: P1 cũ
`span-rong-nuot-ti-le-vo-can` xếp **VÁ HỜ về nghĩa vụ xác nhận** — reviewer tự dựng **1213 ca, 0 đỏ giả /
0 bỏ sót** (Đ1 = 0 trên bộ ấy), Đ2 `0/6` bản in xanh thật bị bác ở lượt 6; executor bổ sung `mcp_gh` (0/1) và — sau khi đặt đúng Ruff 0.15.15 lên PATH — `pretooluse` xanh thật (`CA 39/39 · DOT BIEN 34/34`, rc=0, 0/1) ⇒ **Đ2 = 0/8** (`d2-that-results.json` trong gói lượt 6);
giữ P1 vì hồ sơ **thiếu hiện vật để tái tính** (bộ 311 hàng, `do_h.py`, `law7.json`, `prior131.json`
không có trong kho) chứ **không** vì tìm được phản chứng H mới. P3 `uoc-kich-thuoc-lo-con-tinh-nhan-ac`
**ĐÃ VÁ THẬT**. Verdict: `ops/reviews/pr468-hoso-4-packet-review-6-codex-verdict.md`; bộ ca + harness
+ bản in của reviewer nằm TRONG KHO ở `ops/reviews/pr468-hoso-4-packet-review-6-codex/`. Biên bản lượt 5:
`ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md`.

**(2) Tiền nhiệm còn giữ write set.** Đo **03:15Z 07-09-2026**:

```
ai-dang-giu .claude/dev/ci_dang_ky_test.py
  NGƯỜI_GIỮ 1: mutant-khong-chay-tren-windows-exec-1-claude-20260906
```

Đó là lease của #456 — packet **đã land** (`1b3caa1`) nhưng lease hết hạn `14:30:07Z 07-09`, **còn
~11,2 giờ**. Cấp lease mới cho cùng đường dẫn mà không thu hồi bản cũ là **tự tạo cửa sổ hai writer**.
Lease mới phải khai `thay_the_cho`, và tệp lease cũ phải được đặt `da_bi_thay_the` — chốt
`_kiem_bia_mo` đòi **hai chiều**. `check rc=0` **không** thay được phép đo này: đo 21:02Z 06-09,
`check` cho `rc=0` với `thay_the_cho: []` ngay trong lúc #456 còn giữ.

Phép canh hai nguồn ref chạy trước phép đo trên: máy chủ **299** / cục bộ **299**, `comm -23` **rỗng**
⇒ không mù.

## Đích

Một cổng đang **CÓ MẶT và CÓ CHẠY mà vẫn không đo** thì nhìn giống hệt một cổng xanh. Packet này làm
nó nhìn thấy.

---

**Đặc tả đóng băng:** `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md` @ `d85365463259615537c4fb96acd2408d917d9bd2` (commit ĐẦU TIÊN chứa bản có băm dưới đây; `b743f17` là bản trước đính chính lượt 6–7, băm `3aafd766…` — finding P1 `issue-lo-neo-commit-cu-kem-bam-moi` lượt 7)
**`spec_sha256`:** `4db18266746e220b5745a341faa1307a105b1ace457e31c6af5dcf461d3c86ae`
**`review_class`:** `sensitive` · **`base_sha`:** `1b3caa1` · **`depends_on`:** `GATE-TACH-JOB-CAT-CHI-PHI`
**Lease nháp:** `ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap` (5 ô null —
`packet_issue` đã điền `464`; bản đầu ghi 6)
