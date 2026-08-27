# ĐẶC TẢ PACKET — `CHON-REVIEWER-THEO-DO-PHUC-TAP`

```yaml
packet_id: CHON-REVIEWER-THEO-DO-PHUC-TAP
revision: 1
generation: 1
review_class: sensitive          # sua chinh duong REVIEW - thu quyet dinh ai kiem cai gi
executor: codex
reviewer: claude
assurance_target: cross_approved
```

> Chủ kho ra lệnh trực tiếp 27-08-2026: *"executor thì dùng codex, xhigh. reviewer thì chọn từ
> opus 5 high cho tới fable 5 max tùy độ phức tạp. nếu chưa implement trong skill thì lưu ý đưa
> vào để implement việc chọn mô hình theo độ phức tạp."*

## 0. Vấn đề — ba phép đo, không phải ba lo ngại

Đo 27-08-2026 trong chính container này, `claude` 2.1.247. **Cả ba đều FAIL-OPEN.**

**(a) `--effort` sai ⇒ CẢNH BÁO rồi IM LẶNG lùi về mặc định.**

```
$ claude --effort khong-ton-tai -p "x"
Warning: Unknown --effort value 'khong-ton-tai' — ignoring it and using the default effort.
          Valid values: low, medium, high, xhigh, max.
```

Gõ nhầm một bậc nỗ lực ⇒ reviewer chạy ở mức mặc định, và **không có gì trong kết quả nói ra
điều đó**. Một lượt review "xhigh" có thể chưa bao giờ là xhigh.

**(b) `--model` sai ⇒ `rc=0`.**

```
$ claude --model claude-khong-ton-tai-9 -p "OK"; echo "rc=$?"
"claude-khong-ton-tai-9" is not a model this version of Claude Code recognizes...
[claude-code:unrecognized_model] {"model":"claude-khong-ton-tai-9","query_source":"sdk"}
There's an issue with the selected model. It may not exist or you may not have access to it.
rc=0
```

Đúng bài học `CLAUDE.md`: *"Cổng xanh nhờ `rc=0` là cổng CÓ THỂ BỊ LỪA — phải đòi BẰNG CHỨNG
DƯƠNG"*. Một harness chỉ đọc `rc` sẽ ghi nhận "review đã chạy" cho một lượt **không có review nào**.

**(c) `--output-format json` là chỗ DUY NHẤT nói thật, và nó nói ngược `rc`.**

| yêu cầu | `rc` | `subtype` | `is_error` | `modelUsage` |
|---|---|---|---|---|
| `claude-opus-5` | 0 | `success` | `false` | `{"claude-opus-5": {..., "canonicalModel": "claude-opus-5"}}` |
| `claude-fable-5` | 0 | `success` | `false` | `{"claude-fable-5": {..., "canonicalModel": "claude-fable-5"}}` |
| `claude-khong-ton-tai-9` | 0 | **`success`** | **`true`** | **`{}`** |

`rc` và `subtype` **cùng nói dối**; `is_error` + `modelUsage` nói thật. Đây là bằng chứng dương
duy nhất đo được, và nó là của HARNESS — khác hẳn *lời tự khai của mô hình*. Lời tự khai
(`{"model_id_ban_dang_chay": ...}`) cũng trả đúng ở hai ca hợp lệ, nhưng **một mô hình có thể
sai về chính nó**, nên nó KHÔNG được dùng làm chốt. Đo cả hai để nói rõ vì sao chọn cái nào.

**(d) Và chưa có chỗ nào trong kho ghi chọn mô hình theo cái gì.**

```
grep -rn "fable\|--effort\|--model" .claude/skills/    ⇒  0
```

Nay executor là `codex` còn reviewer là `claude` với **bốn** bậc khả dĩ. Không có luật thì mỗi
lượt một người chọn một kiểu, và chọn thấp thì lỗ lọt — đúng điều đo được ở #341/#342/#343:
mỗi packet cần 3–4 lượt mới sạch.

## 1. `write_set`

```
.claude/dev/chon_reviewer.py            # MOI
.claude/dev/chon_reviewer_test.py       # MOI
.claude/skills/cross-review/SKILL.md
```

**Đúng ba đường. Không đụng gì khác** — đặc biệt KHÔNG đụng `launcher.py`, `packet_loop.py`,
`scripts/tl.py`, `.github/workflows/**`. Cần đụng thì DỪNG và báo, đừng tự mở rộng.

## 2. `ngan_sach_kich_thuoc`

| | |
|---|---|
| tệp tối đa | **3** |
| dòng thêm tối đa | **520** |

Vượt ⇒ DỪNG và NÉN. Đang viết hơn 520 dòng nghĩa là đang làm một packet khác.

## 3. `.claude/dev/chon_reviewer.py` — hợp đồng CHÍNH XÁC

Hai nửa, và nửa thứ hai mới là nửa có răng.

### 3.1 `chon(review_class, duong_dan, so_dong, luot, bac_truoc=None)` → `(model, effort, giai_thich)`

VỊ TỪ THUẦN. Nhận dữ liệu làm đối số — điều kiện để có ca BIẾT TRƯỚC ĐÁP ÁN
(bài học `MOC_MO_HO_CO_SAN`, PR #343).

**Vùng, phân loại theo TIỀN TỐ đường dẫn, ALLOW-LIST:**

| vùng | tiền tố |
|---|---|
| `cong` | `.github/workflows/`, `.claude/hooks/`, `.claude/dev/packet_loop`, `ops/lease_publish` |
| `giao-thuc` | `docs/PROTOCOL_DA_PHIEN.md`, `docs/adr/`, `.claude/skills/` |
| `runtime` | `scripts/` |
| `dev` | `.claude/dev/` (phần còn lại), `ops/` (phần còn lại) |
| `tai-lieu` | `references/`, `*.md` ở gốc |
| **`khong-biet`** | **mọi đường dẫn KHÔNG khớp bảng trên** |

`khong-biet` KHÔNG được bỏ qua. Đường dẫn không phân loại được là đường ta chưa nghĩ tới, và
bài học `lease-authority-spoof` nói thẳng: danh sách CẤM thua từ trong thiết kế, phải đảo thành
danh sách CHO PHÉP — mà allow-list thì bắt buộc phải có nhánh "ngoài danh sách" và nhánh ấy
phải ĐẨY LÊN, không phải tha.

**Điểm — cộng dồn, tất định:**

```
+2  review_class == "sensitive"
+2  cham vung `cong`
+1  cham vung `giao-thuc`
+1  so_tep >= 5
+1  so_dong >= 400
+1  luot >= 3
+3  co vung `khong-biet`
```

**Bậc:**

| điểm | model | effort |
|---|---|---|
| `<= 0` | `claude-opus-5` | `high` |
| `1–2` | `claude-opus-5` | `xhigh` |
| `3–4` | `claude-fable-5` | `xhigh` |
| `>= 5` | `claude-fable-5` | `max` |

**BÁNH CÓC (`bac_truoc`) — không bao giờ TỤT bậc giữa các lượt của cùng một packet.** Truyền
`bac_truoc=(model, effort)` của lượt trước; kết quả phải `>=` bậc ấy. Lý do: lượt sau thường có
diff NHỎ hơn (chỉ còn phần vá), nên điểm tụt và reviewer bị hạ cấp **ĐÚNG LÚC** vừa có bằng chứng
là lượt trước chưa đủ. `bac_truoc=None` ở lượt 1.

`giai_thich` phải liệt kê từng khoản điểm đã cộng và bậc cuối — để người đọc verdict biết vì sao,
không phải tin một con số.

### 3.2 `kiem_dinh_danh(model, effort)` → ném `KhongDoDuoc` nếu sai

ALLOW-LIST, so BẰNG NHAU:

```
MO_HINH_CHO_PHEP = ("claude-opus-5", "claude-fable-5")
NO_LUC_CHO_PHEP  = ("low", "medium", "high", "xhigh", "max")
```

**Bí danh (`opus`, `fable`, `sonnet`) phải BỊ TỪ CHỐI** dù CLI chấp nhận: bí danh trỏ "bản mới
nhất", tức một mục tiêu DI ĐỘNG, và cả kho này neo mọi thứ bằng định danh bền. Một verdict ghi
`model: opus` không tái lập được sau khi bí danh trỏ chỗ khác.

### 3.3 `kiem_ket_qua(yeu_cau_model, ket_qua_json)` → ném `KhongDoDuoc` nếu không chứng minh được

VỊ TỪ THUẦN — nhận **dict đã phân tích**, KHÔNG tự gọi CLI. Một ca test phải chạy được offline,
không mạng, không xác thực; hàm nào tự gọi CLI thì ca của nó không tồn tại ở CI.

ĐỎ khi bất kỳ điều nào:

- `ket_qua_json` là `None`/không phải dict ⇒ KHÔNG ĐO ĐƯỢC;
- `is_error` là `True` **hoặc thiếu** (thiếu = không đo được, `None != False`);
- `modelUsage` rỗng/thiếu;
- `modelUsage` có **nhiều hơn một** khoá (không xác định được model nào đã chạy);
- `canonicalModel` khác `yeu_cau_model`, **hoặc thiếu** — và nếu thiếu thì lùi về so KHOÁ của
  `modelUsage`, chứ không tha.

**KHÔNG được đọc `rc` hay `subtype` làm bằng chứng ĐẠT.** Bảng ở §0(c) là lý do; ghi lý do ấy
vào chú thích ngay tại hàm, không phải chỉ ở đây.

### 3.4 CLI

`python3 .claude/dev/chon_reviewer.py --review-class sensitive --duong-dan a.py,b.md --so-dong 120 --luot 1`
→ in `model`, `effort`, `giai_thich`; `--json` cho dạng máy đọc. Thoát 0 khi chọn được, khác 0
khi `kiem_dinh_danh` từ chối.

## 4. `.claude/dev/chon_reviewer_test.py` — phản chứng

Chạy `python3 .claude/dev/chon_reviewer_test.py`, thoát 0 khi ĐẠT.

**Bắt buộc:**

1. Ca BIẾT TRƯỚC ĐÁP ÁN cho **cả bốn** bậc, mỗi bậc ít nhất một ca.
2. Ca cho `khong-biet`: một đường dẫn lạ (`vi-du/la.txt`) phải đẩy lên bậc cao nhất.
3. Ca BÁNH CÓC hai chiều: `bac_truoc` cao hơn ⇒ giữ bậc cao; `bac_truoc` thấp hơn ⇒ KHÔNG bị kéo xuống.
4. Ca `kiem_dinh_danh`: bí danh `opus`/`fable` bị TỪ CHỐI; `claude-opus-5` được nhận; effort sai bị TỪ CHỐI.
5. Ca `kiem_ket_qua`, dùng ĐÚNG ba bản ghi JSON đo được ở §0(c) làm fixture: hai ca hợp lệ ĐẠT,
   ca `claude-khong-ton-tai-9` (`is_error: true`, `modelUsage: {}`) ĐỎ.
6. Ca `modelUsage` **hai khoá** ⇒ ĐỎ. Ca thiếu `is_error` ⇒ ĐỎ.
7. Ca ĐƠN ĐIỆU: thêm một khoản điểm không bao giờ làm bậc TỤT (chạy qua mọi tổ hợp
   `review_class` × vùng × ngưỡng, so bằng chỉ số bậc).

**ĐỘT BIẾN — mỗi bản vá một đột biến, và runner phải đòi giết ĐÚNG VÀ CHỈ ĐÚNG tập ca đã khai**
(chạy từng đột biến trên TOÀN BỘ ca, không phải chỉ tập đích). Tối thiểu:

| đột biến | phải giết |
|---|---|
| bỏ nhánh `khong-biet` (coi như không cộng điểm) | ca 2 |
| bỏ bánh cóc | ca 3 |
| nhận bí danh vào allow-list | ca 4 |
| `kiem_ket_qua` đọc `subtype == "success"` thay vì `is_error` | ca 5 |
| `kiem_ket_qua` tha khi `modelUsage` nhiều khoá | ca 6 |
| `is_error` thiếu ⇒ đọc thành `False` | ca 6 |

Nền có ca ĐỎ ⇒ **TỪ CHỐI công bố điểm đột biến** (bài học P1 của PR #342).

## 5. `.claude/skills/cross-review/SKILL.md` — mục mới

Thêm **một** mục, đặt ngay sau `## Bước 0 — CÔNG CỤ`. Nội dung bắt buộc:

- bảng bậc ở §3.1 (điểm → model/effort) và câu bánh cóc;
- **ba cái bẫy đo được ở §0**, kèm đúng số đo, kèm câu *"`rc` và `subtype` cùng nói dối"*;
- hai lệnh: chọn bậc TRƯỚC khi phóng, và kiểm `modelUsage` SAU khi phóng;
- cú pháp phóng reviewer claude headless:
  `claude --model <id> --effort <bac> --output-format json -p ... < PROMPT.md`
- câu giới hạn: mục này KHÔNG thay §8 của protocol, nó chỉ nói **chọn bậc nào**.

**KHÔNG chép doctrine** — `packet_loop.py doctrine-scan --root .` phải `rc=0`.

## 6. Cổng phải xanh trước khi mở PR

```
python3 .claude/dev/chon_reviewer_test.py
python3 .claude/dev/packet_loop.py doctrine-scan --root .
python3 .claude/dev/packet_loop.py adr-song --root .
python3 scripts/tl.py doc-claims-check --strict --json
python3 scripts/tl.py workflow-audit  --strict --json
python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
python3 ops/lease_publish_test.py
git config core.abbrev 7        # BAT BUOC truoc khi chay cong
```

Cổng nào đỏ ⇒ **đo nền trên `origin/master` sạch rồi so DELTA**; đỏ sẵn thì nói "đỏ sẵn,
delta = 0", đừng vá lung tung.

## 7. Điều KHÔNG được làm

- không đụng đường nào ngoài `write_set`;
- không gọi `claude`/`codex` LIVE bên trong ca test — fixture là dữ liệu đã đo ở §0;
- không đọc `rc` làm bằng chứng ĐẠT ở bất cứ đâu;
- không tự merge, không tự đẩy lên `master`, không tạo PR khác;
- nghĩ ra được một hướng hỏng thì **biến ngay thành ca `rXX_`**, đừng để nó nằm trong chú thích.
