# Hoàn thiện kế hoạch + đồng bộ protocol — phiên 22-08-2026

**Giao việc:** `ops/prompts/phien-hoan-thien-ke-hoach-20260822.md` (PR #230, chưa land).
**Nền đo:** `master` = `a5bfe07`, đo lúc `2026-08-22T03:05Z`.

> **Tệp này KHÔNG phải lease và không cấp việc cho ai.** `docs/PROTOCOL_DA_PHIEN.md` §7: prompt và
> handoff không mang thẩm quyền. Thứ giao việc là Packet Issue kèm lease còn hiệu lực (§3.2 và §4).
> Phiên nào đọc §2 hay §3 rồi bắt tay làm là tự cấp việc cho mình.

**THỨ TỰ packet không nằm ở đây.** Nó ở `ops/HANG_DOI_PACKET.md` (PR #229). Tệp này chỉ đóng góp
**PHÉP ĐO** để điền cột trạng thái của tệp ấy, và một đề xuất cắt packet cho phần chưa có Issue.
Dựng chỗ thứ hai nói cùng chuyện là đúng cái bệnh #229 sinh ra để chữa.

---

## 1. Đo lại bảng "Nền đã đo" — hai dòng KHÔNG tái lập nguyên trạng

| # | verdict | đo được |
|---|---|---|
| 1 | tái lập đúng | **1** commit `6f49692`, **+22/−15** |
| 2 | tái lập đúng | `0043`→**0** · `0044`→**0** · `0045`→**0** |
| 3 | **nửa tái lập** | xem dưới |
| 4 | tái lập đúng | **0/8** |
| 5 | tái lập, nhưng **khai thiếu hai bậc** | xem dưới |
| 6 | **cấu trúc tái lập, trạng thái không có lệnh** | xem §2 |

### 1.1 Dòng 3 — câu chữ đọc ra hai số khác nhau

Vế có lệnh kèm tái lập đúng: `grep -c 'PLAT-X' ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` → **0**.
Đo thêm cùng cách: `AG-` → **0**, `SLICE-` → **0**, `PLAT-M` → **0**.

Vế *"0 commit từ 19-08"* **không có lệnh kèm**, và hai cách đọc ra hai số:

```
git log --oneline --since=2026-08-19 origin/master -- ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md | wc -l   # 2
git log --oneline --since=2026-08-20 origin/master -- ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md | wc -l   # 0
```

Hai commit ấy là `f6e0037` (19-08 13:44) và `3cc7f09` (19-08 12:44). Ý định gần như chắc chắn là
*"không đổi KỂ TỪ 19-08"*, tức số **0**, và tôi dùng số đó — nhưng nói ra thay vì lặng lẽ chọn.

### 1.2 Dòng 5 — bệnh là 222/230, không phải hai field

Hai con số của bản giao việc đúng (`review_class` 10/49 · `^spec_sha256` 11/49 = `spec_sha256` 5 +
`spec_sha256_required` 6), và cổng đọc **0** dòng cả hai. Nhưng đo toàn bộ:

**49 lease trên `master` dùng 230 tên trường khác nhau · `ops/lease_publish.py` đọc 8 · 222 trường
khai mà không cổng nào kiểm.** Trong đó **16 trường khai ở 100% lease** và vẫn không ai đọc.

> **Con số này đã SAI một lần: bản đầu ghi 215/207.** Phép đo cũ dùng regex đòi khoá toàn chữ thường
> nên bỏ sót 15 khoá có chữ HOA — và nó còn ship kèm một *lệnh tái lập* dùng chính cái regex ấy, tức
> tái lập trung thành một con số sai. Một phiên khác đo bằng `yaml.safe_load`, ra 230, và nhắn sang.
> Cột giữa (cổng đọc **8**) hai bên khớp tuyệt đối — chính chỗ khớp ấy khoanh được lỗi vào phép liệt
> kê khoá. Chi tiết và lệnh đã sửa: `ops/NO_KY_THUAT.md` §14.

Đã ghi thành nợ có tên `LEASE-KHAI-MA-CONG-KHONG-DOC` (`ops/NO_KY_THUAT.md` §14), kèm lệnh tái lập
và kèm **cảnh báo đọc số**: 230 là số *tên trường*, không phải số *lỗ hổng* — nhiều trường cố ý là
ghi chú cho người (`*_note`, `*_ghi_chu`, `canh_bao_*`) và không nên có cổng.

Vì sao con số đúng lại đổi kết luận: **2** làm mục D trông như một bản vá hai dòng; **222** cho thấy
nó là một **quyết định phạm vi** — phải chọn tập trường nào lên hợp đồng, tập nào rớt xuống ghi chú
tự do. Đó là lý do §3 cắt nó thành bốn packet chứ không phải một.

### 1.3 Một con trỏ chết thứ năm, không có trong bản giao việc

`ops/lease_publish_test.py:1302` (docstring `t34`) viết *"`t42` bên dưới canh cho docstring này không
trôi rộng ra"*. `t42` **đã bị gỡ có chủ đích** — chú thích dòng 2004 của cùng tệp nói rõ, và nợ đã
chuyển sang `ops/NO_KY_THUAT.md` §11. Câu trong docstring không được sửa theo.

```
grep -n 't42' ops/lease_publish_test.py      # 1302 (lời khai) và 2004 (chú thích gỡ)
grep -c '^def t42' ops/lease_publish_test.py # 0
```

Cùng hình dạng với bốn con trỏ chết của PR #230. **Tệp này thuộc write set của lease #227 đang còn
hiệu lực**, nên phiên này KHÔNG sửa — ghi lại để phiên giữ lease ấy, hoặc packet kế tiếp trên tệp
ấy, sửa một dòng.

---

## 2. Trạng thái packet — đo bằng HIỆN VẬT trên `master`, không bằng nhãn Issue

**Nhãn Issue không trả lời được câu hỏi này, và đo được là nó nói SAI.** `#215` mang nhãn
`state:landed` trong khi `#206` mang `state:ready` — mà hiện vật của cả hai đều có trên `master`.
`#194` mang `state:running` trong khi PR #204 của nó đã merge từ 21-08.

Mỗi dòng dưới đây có **một lệnh chạy được** trả lời "hiện vật có trên master chưa".

| Issue | packet | nhãn Issue | HIỆN VẬT | lệnh |
|---|---|---|---|---|
| #194 | `PLAT-M4` | `state:running` | **CÓ** | `grep -c mcp-endpoint .claude/dev/launcher.py` → 9 |
| #195 | `PLAT-X2` | `state:integrated` | **CÓ** | `grep -n '#195' .github/workflows/ops-publish-lease.yml` → dòng 159 |
| #197 | `PROTO-01-FIX` | `state:leased` | **CÓ** | `git merge-base --is-ancestor 6f49692 origin/master` → rc 0 |
| #200 | `PLAT-X3` | `state:integrated` | **CÓ** | `grep -c actionlint .github/workflows/ci.yml` → 2 · `…ops-publish-lease.yml` → 4 |
| #203 | `PLAT-X4` | `state:running` | **CÓ** | `grep -c thay_wrapper ops/lease_publish_test.py` → 3 |
| #206 | `PLAT-X5` | `state:ready` | **CÓ** | `ls ops/cai_actionlint.sh ops/chay_lease_publish_test.sh` |
| #215 | `SLICE-B-C` | `state:landed` | **CÓ** | `grep -c 'PLAT-X5-required-status-check' ops/NO_KY_THUAT.md` → 2 |
| #188 | `PLAT-X1` | `state:ready` | **KHÔNG** | `grep -c write_set ops/lease_publish.py` → **0** |
| #209 | `PLAT-X6` | `state:ready` | **KHÔNG** | chưa có lease |
| #219 | `AG-T0-01B` | `state:leased` | **KHÔNG** | `grep -ci antigravity .claude/dev/launcher.py` → **0** |
| #220 | `PLAT-X7` | `state:proposed` | **KHÔNG** | `grep -c reviewer_model ops/lease_publish.py` → **0** |
| #225 | `PLAT-X8` | `state:proposed` | **KHÔNG** | `grep -c review_class ops/lease_publish.py` → **0** |
| #227 | `LEASE-DANG` | `state:running` | **KHÔNG** | `git diff --stat origin/master origin/codex/lease-dang-exec-1 -- ops/lease_publish*` → +471/−11 |
| #177 | `W0-R1B` | `state:ready` | **KHÔNG** | `grep -c review_calls .claude/dev/packet_loop.py` → **0** |
| #178 | `W0-RC` | `state:ready` | **một phần** | 40 đột biến đã có trong `packet_loop_test.py`; "9 cửa không có phản chứng" chưa đo lại |

**Đề xuất cho `ops/HANG_DOI_PACKET.md` (#229):** thêm một cột `lệnh đo` bên cạnh cột trạng thái, và
đổi "Điều kiện rời hàng đợi" thành *"hiện vật có trên master, CHỨNG MINH BẰNG LỆNH TRONG BẢNG"*.
Không có cột ấy thì cột trạng thái là lời khai gõ tay, và nó sẽ trôi đúng như nhãn Issue đã trôi.

### 2.1 Sổ lease — đo trên MỌI ref, không chỉ `master`

`master` giữ **49/93** tệp lease (**52%**). Đúng những lease mới nhất — tức khả nghi nhất — nằm trên
nhánh `ops/**`/`codex/**` chưa merge. Đo lúc `03:05Z`: **24** lease chưa hết hạn, **16** trong số đó
**không có trên `master`** — phân bố theo Issue: `#227`→9 · `#217`→4 · `#213`→2 · `#215`→1.

> **Cái bẫy đã sập ngay khi viết mục này.** Bản nháp ghi **13**, sai vì script kiểm của tôi khớp
> `lease_expires_at_utc:\s*"?` — chỉ nháy KÉP, trong khi YAML ghi nháy ĐƠN (`'2026-08-23T01:00:00Z'`).
> Regex không khớp ⇒ mọi lease bị đọc thành "không có hạn" ⇒ đếm ra **0** chưa hết hạn, và tôi suýt
> ghi con số của một phép đo khác. Nó chỉ lộ vì đã chạy lại TỪNG lệnh đã chép vào tài liệu này thay
> vì tin bản nháp. Lệnh dưới đây nhận cả hai loại nháy.

Lệnh tái lập đầy đủ ở `ops/NO_KY_THUAT.md` §12 (PR #230) và bài học `SỔ LEASE KHÔNG NẰM MỘT CHỖ`
trong `CLAUDE.md`. Bản rút gọn:

```
git fetch origin '+refs/heads/*:refs/remotes/origin/*'
git for-each-ref --format='%(refname)' 'refs/remotes/origin/**' | while read r; do
  git ls-tree -r --name-only "$r" ops/leases/ ; done | sort -u | wc -l     # 93
ls ops/leases/*.yaml | wc -l                                              # 49
```

**Nhắc lại điều bài học đã phải sửa một lần:** *"chưa hết hạn"* KHÔNG phải *"còn hiệu lực"*. Không
trường nào trong tệp lease nói nó đã tiêu, và trạng thái Issue không trả lời được — phải đi tìm hiện
vật của packet trên `master`, tức đúng bảng ở §2. Trong 24 lease chưa hết hạn, phần lớn thuộc packet
đã land; hai lane thật sự đang chạy là **#227** (tới `23-08T01:00Z`) và **#219** (tới `23-08T02:05Z`).

---

## 3. Mục D — cắt phần còn lại cho vừa trần `ADR-0044`

### 3.1 Còn lại những gì

`ops/THAM_DINH_KE_HOACH_20260821.md` §"Kế hoạch thi hành" liệt kê **8** chốt cho mục D. Hai đã tách
thành packet riêng:

| chốt | đã đi đâu |
|---|---|
| cross-provider theo họ model | `PLAT-X7` (#220), `proposed`, chưa đặc tả |
| (liên quan) lớp review hiệu lực | `PLAT-X8` (#225), đặc tả bản 3b `308d0cf4…`, **chưa lease** |

Còn lại **6 chốt chưa có Issue**: neo đặc tả (`spec_*`) · băm tồn tại thật · 4 mức
`assurance_target` · căn cứ nâng trần · timestamp không ở tương lai · reservation gate + hình dạng
kế thừa.

### 3.2 Vì sao KHÔNG gói được thành một packet — bằng số, không bằng cảm tính

`ADR-0044`: packet `sensitive` chạm authority = **≤ 3 tệp và ≤ 300 dòng thêm**. Write set của cả sáu
chốt là `ops/lease_publish.py` + `ops/lease_publish_test.py` = **2 tệp**, nên tệp không phải ràng
buộc. **Dòng thêm mới là ràng buộc**, và giá thật đo từ chính kho:

| tiền lệ | phạm vi | dòng thêm | mỗi mối quan tâm |
|---|---|---|---|
| `PLAT-M4` (#204, đã land) | 1 mối quan tâm, 2 tệp | +351 | ~351 |
| `#227` nhánh `codex/lease-dang-exec-1` | 2 mối quan tâm, 2 tệp | +471 | ~235 |
| `PLAT-X4` (#203) | nhiều, 4 tệp | +721 | — |

Lệnh: `git diff --stat origin/master origin/codex/lease-dang-exec-1 -- ops/lease_publish.py ops/lease_publish_test.py`

Giá quan sát được là **~235–350 dòng cho MỘT mối quan tâm** khi tính cả phản chứng. Dưới trần 300
dòng, con số ấy nói thẳng: **một packet mang được một chốt, hai chốt chỉ khi chúng dùng chung máy
móc.** Sáu chốt gộp một packet ước ~1.400–2.000 dòng — lớn hơn cả `PLAT-X4`, thứ đã ăn ba vòng
review và tám finding, và lớn hơn gói `X4+X5` (1.133 dòng) mà `ADR-0044` đã dùng làm bằng chứng để
bác phương án gộp.

### 3.3 Đề xuất bốn packet — thứ tự neo theo ĐỘ PHỦ ĐO ĐƯỢC, không theo cảm giác dễ

| thứ tự | packet đề xuất | chốt | trường và độ phủ trên 49 lease | vì sao đứng đây |
|---|---|---|---|---|
| **D1** | `moc-thoi-gian-lease` | `leased_at_utc` không ở tương lai; `leased_at_utc < lease_expires_at_utc` | `leased_at_utc` **49/49 khai · 0 đọc** | phủ 100% lease, máy móc chỉ là hai phép so ngày — rẻ nhất mà phủ rộng nhất; không đụng `kiem()` sâu nên rebase sau #227 gần như không đau |
| **D2** | `neo-dac-ta` | `spec_path` + `spec_sha256_required` + `spec_status`; băm phải trỏ tệp CÓ THẬT | `spec_path` 17/49 · `spec_sha256_required` 6/49 · `spec_sha256` 5/49 | máy móc **đã có**: `_kiem_neo_prompt` làm đúng việc ấy cho `prompt_path`/`prompt_sha256_required` (`RC_NEO=6`). Đây là mở rộng, không phải viết mới — nên là chốt đắt-giá-trị/rẻ-công thứ hai |
| **D3** | `can-cu-nang-tran` | khối `nang_tran{ai_nang, can_cu, tran_cu, tran_moi}`; thiếu thì từ chối | `nang_tran` **1/49** · `attempts_limit` 49/49 · `review_rounds_limit` 22/49 | `ADR-0043` khai thẳng cổng phải làm việc này và **chưa có dòng nào**; nhưng nó phải đứng sau D1/D2 vì nó sửa đúng vùng `kiem()` mà #227 đang chạm |
| **D4** | `hinh-dang-ke-thua` | `supersedes_lease` / `tiep_noi_lease` phải trỏ lease có thật; reservation gate | `hinh_dang_ke_thua` 3/49 · `supersedes_lease` 4/49 | phủ hẹp nhất và cần đọc **nhiều tệp lease cùng lúc** — máy móc khác hẳn ba cái trên. Làm cuối |

**`assurance_target` (49/49 khai · 0 đọc) KHÔNG nằm trong bốn packet trên — cố ý.** Bốn mức assurance
chỉ định nghĩa được sau khi `PLAT-X8` (#225) dựng `effective_review_class`; làm trước là dựng một
thang trên một lời khai chưa được đo, đúng bệnh mà #225 sinh ra để chữa. Đề xuất: nó thành **packet
kế nhiệm của #225**, không phải một dòng của mục D.

### 3.4 Chỗ bốn packet này chen vào hàng đợi #229

Hàng đợi hiện tại: `#227 → #225 → #209 → #220 → mục D`. Bốn packet trên thay ô cuối:

```
#227 → #225 → #209 → #220 → D1 → D2 → D3 → D4
```

**D1 và D2 KHÔNG chen lên trước được** dù rẻ hơn, và lý do là va chạm NỘI DUNG chứ không phải cửa sổ
lease: cả hai thêm chốt vào `kiem()` và vào khối hằng sau `RC_NEO` — đúng hai vùng `#227` đang sửa
(+112 dòng trong `ops/lease_publish.py`). Dời hiệu lực chỉ chữa cửa sổ, không chữa va chạm nội dung —
xem `ops/RUT_LEASE_PLAT_X8_20260821.md`.

### 3.5 Cái đề xuất này KHÔNG cấp

Không dòng nào ở đây là một lease, và không packet nào ở đây có Issue. `D1`–`D4` là **tên đề xuất**,
chưa phải `packet_id`. Muốn chạy thì người giữ kho mở Issue + đặc tả (`.claude/skills/soan-spec/`
xuất ra `ops/specs/<packet-id>.md` kèm `sha256` — đúng đầu vào mà chốt `spec_sha256` của **D2** sẽ
đọc), rồi cấp lease theo §4.

---

## 4. Việc A đã làm — và cổng chứng minh nó không chết được

Người giữ kho chọn phương án *"§ quy tắc đang hiệu lực + ca máy"* (in-session, 22-08-2026).

**Bệnh, đo được:** `docs/PROTOCOL_DA_PHIEN.md` trỏ ADR bằng **một dòng phạm vi** (`ADR-0017 đến
ADR-0035`). Có **45** ADR; protocol nhắc tên **4**; **41** ADR không được nhắc lần nào, gồm trọn
`0036`–`0045` — mười ADR quản trị, trong đó ba ADR người giữ kho vừa duyệt.

**Lệnh phải chạy trên `origin/master`, KHÔNG trên cây làm việc** — vì chính bản vá này đã đưa con
số 41 về 0, nên chạy trên cây đã sửa sẽ đo trạng thái SAU rồi trình bày như trạng thái TRƯỚC. Bản
nháp của tài liệu này viết đúng lỗi ấy và chỉ lộ khi chạy lại từng lệnh:

```
git show origin/master:docs/PROTOCOL_DA_PHIEN.md > /tmp/proto_master.md
ls docs/adr/*.md | wc -l                                            # 45
for f in docs/adr/*.md; do n=$(basename $f); n=${n%%-*}; \
  grep -q "$n" /tmp/proto_master.md || echo "$n"; done | wc -l    # 41  (TRƯỚC)
python3 .claude/dev/packet_loop.py adr-song --root .                # 45/45 (SAU)
```

**Đã làm:**

1. `docs/PROTOCOL_DA_PHIEN.md` §20 — bảng định tuyến, **một dòng cho mỗi ADR**, 45/45. Cột cuối là
   *"cổng đã ĐO"* với **ba** giá trị chứ không hai: `0 cổng` (phép đo mạnh) · `có nhắc: <tệp>×<n>`
   (**PROXY, không phải bằng chứng cưỡng chế**) · `chưa đo`. Đo được **8 ADR mà không tệp cổng nào
   nhắc tới khái niệm của nó**: `0032` `0037` `0038` `0039` `0040` `0043` `0044` `0045` — bảy trong
   tám thuộc dải quản trị `0036`–`0045`.
2. Dòng 7 thay bằng **đúng một dòng** trỏ §20 — cố ý giữ nguyên số dòng để `docs/PROTOCOL_DA_PHIEN.md:751`
   mà `ADR-0043` neo vào không xê dịch. Đã kiểm: dòng 751 sau khi sửa vẫn là câu cũ.
3. `.claude/dev/packet_loop.py adr-song` (`RC_ADR = 9`) — ĐỎ khi: thiếu dòng · con trỏ chết · dòng
   trùng · ADR không có dòng `Trạng thái` đọc được · thiếu §20 · kho thật mà thiếu `docs/adr/` ·
   **hai tệp cùng số ADR** · **tên tệp lệch dạng** (hai luật cuối: xem §4.2).

**Bằng chứng dương, không phải `rc=0`:**

```
python3 .claude/dev/packet_loop.py adr-song --root .
# adr-song: sạch — 45 ADR trên đĩa, 45 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])
```

Hai số **BẰNG NHAU** và bằng số tệp thật, chứ không chỉ mã thoát.

**Cổng có răng — 14 đột biến, mỗi luật một cái:**

| đột biến | ca đích chết | đối chứng khác họ |
|---|---|---|
| `adr_bo_kiem_thieu_dong` | 2 | 3 còn sống |
| `adr_bo_kiem_con_tro_chet` | 1 | 3 còn sống |
| `adr_bo_kiem_trung_dong` | 1 | 3 còn sống |
| `adr_noi_ngoai_le_cho_moi_ADR` | 1 | 3 còn sống |
| `adr_tha_khi_thieu_thu_muc` | 1 | 3 còn sống |
| `adr_hang_nhan_ca_van_xuoi` | 1 | 3 còn sống |
| `adr_gom_map_de_bi_nuot` | 2 | 3 còn sống |
| `adr_tha_ten_tep_la` | 2 | 3 còn sống |
| `adr_rong_allowlist_ten_tep` | 1 | 3 còn sống |

`adr_noi_ngoai_le_cho_moi_ADR` là hình dạng đã trả giá ở `v1.36.68`: **nới danh sách cho phép để
chứa chính thứ đang tấn công**. Không có nó thì không biết ca đích đang đo danh sách hay đo thứ khác.

**Delta so `origin/master` = 0 ĐỎ, cả hai bộ:**

| bộ | master | nhánh này |
|---|---|---|
| `.claude/dev/packet_loop_test.py` | 185/185 đạt | **208/208 đạt** (+23 ca) |
| `ops/lease_publish_test.py` | 41/42 (`t33` fail-close vì thiếu `actionlint`) | 41/42, **cùng nguyên nhân** |

**Một cổng có sẵn đã bắt lỗi của tôi, và đó là bằng chứng nó đang sống:** ma trận codepage
`cp1252`/`cp1258` lấy danh sách lệnh con từ chính `build_parser()` chứ không kê tay, nên lượt chạy
đầu ĐỎ với *"THIẾU PHỦ lệnh con ['adr-song']"*. Đã thêm `adr-song` vào kịch bản — lệnh này in tiếng
Việt lúc thành công nên nó thuộc kịch bản ấy thật.

**Hai nợ có tên mới:** `ops/NO_KY_THUAT.md` §13 (`ADR-0016-THIEU-DONG-TRANG-THAI`) và §14
(`LEASE-KHAI-MA-CONG-KHONG-DOC`).

### 4.2 Finding cross-review trên chính PR này — và vì sao nó đáng hơn một bản vá

Codex review PR #233 ở exact head `cbd14439bb` và ra **một P2 thật**: cổng gom tệp bằng
`{f.name[:4]: f for f in glob("*.md")}`, nên hai tệp cùng bốn chữ số đầu thì cái sau **ĐÈ** cái
trước trong dict.

**Không nhận lời khai của bot — đã dựng phản chứng TRƯỚC khi vá**, trên bản cổng lúc ấy:

```
docs/adr/0001-goc.md  +  docs/adr/0001-ban-sao-len-lut.md      (2 tệp trên đĩa)
§20 có ĐÚNG MỘT dòng `ADR-0001`
⇒ adr-song: sạch — 1 ADR trên đĩa, 1 dòng trong §20, khớp 1–1     rc=0
```

**Chỗ đau không phải con số sai, mà là nó phá đúng thứ tôi khoe.** §4 viết *"hai số BẰNG NHAU và
bằng số tệp thật"* làm bằng chứng dương. Nhưng cả hai số đều rút ra từ **cùng cái map đã bị nuốt**,
nên chúng bằng nhau **bất kể** bao nhiêu tệp biến mất. Luật rút ra rộng hơn ca này:

> **Hai số bằng nhau chỉ là bằng chứng khi chúng đến từ HAI phép đếm ĐỘC LẬP.** Hai số cùng nguồn
> thì phép so chỉ chứng minh nguồn ấy tự nhất quán với chính nó.

Cùng họ với `rc=0` bị lừa, chỉ tinh vi hơn một bậc: ở đây có số, số khớp, và số vẫn nói dối.

Bản vá còn đóng một lỗ **thứ hai** mà finding chỉ ra ở vế sau: `f.name[:4].isdigit()` im lặng bỏ mọi
tên khác dạng, nên một ADR đặt tên sai (`045-thieu-mot-so.md`) biến mất **không dấu vết**. Nay ba
trạng thái: khớp dạng ⇒ là ADR · nằm trong danh sách CHO PHÉP (`README.md`) ⇒ cố ý không phải ADR ·
còn lại ⇒ **không đo được, ĐỎ**. Đã kiểm 45 tệp thật đều khớp dạng trước khi siết, nên siết
không gãy kho.

**Dạng tên tệp, ghi ĐÚNG NHƯ MÃ chứ không ghi gần đúng:** `^(\d{4})-[0-9a-z]([0-9a-z-]*[0-9a-z])?\.md$`.
Nó chặt hơn `^\d{4}-[0-9a-z-]+\.md$` ở đúng một chỗ: ký tự đầu và cuối của phần
slug phải là chữ-số, nên `0046--draft.md` và `0046-draft-.md` bị TỪ CHỐI (`0046-a--b.md` thì
được — dấu nối đôi ở GIỮA không sao). Lượt review thứ hai của codex bắt đúng chỗ này: bản
trước quảng cáo dạng lỏng trong khi mã chạy dạng chặt. Chọn giữ mã chặt và sửa văn bản, vì
dấu nối đầu/cuối là chữ ký của một cái tên gõ nhầm và 0/45 tệp thật dùng nó. Để văn bản khỏi
trôi khỏi mã lần nữa, **thông điệp lỗi in ra chính `_ADR_TEN_TEP.pattern`** thay vì một bản
chép tay.

**Bốn ca mới + ba đột biến**, trong đó `adr_gom_map_de_bi_nuot` **dựng lại nguyên văn cơ chế cũ** —
ai vô tình viết lại như cũ thì ca đích ĐỎ ngay.

**Một bẫy tự sập khi vá, ghi ra vì nó là bẫy đã có tên trong `CLAUDE.md`:** bản vá viết lại đúng hai
dòng mà hai đột biến cũ (`adr_bo_kiem_thieu_dong`, `adr_bo_kiem_con_tro_chet`) neo vào, nên hai đột
biến ấy **mất mỏ neo** — tức sẽ không mutate gì cả. Đúng họ *"đột biến CHƯA TỪNG ĐƯỢC CHẠY"*. Ở đây
bộ test **có** lưới: `thieu = [t for t, _ in cap if t not in goc]` in ĐỎ khi mỏ neo vắng — nên nó
đằng nào cũng lộ; tôi chỉ bắt sớm hơn bằng một lượt kiểm `count == 1` cho **cả 43** đột biến. Nói
đúng công trạng: lưới đã có sẵn, không phải tôi dựng.

### 4.1 Cái Việc A KHÔNG chữa — nói thẳng

- **`adr-song` chưa nằm trong CI.** Nó chạy khi ai đó gõ, và `.github/workflows/ci.yml` chưa gọi.
  Một cổng không ai gọi là cổng không có ai canh — cùng hình dạng với nợ `PLAT-X5-required-status-check`
  (§9 sổ nợ). Nối vào CI đụng `.github/workflows/ci.yml`, ngoài phạm vi phiên tài liệu này.
- **Cột "cổng đã ĐO" chỉ mạnh ở giá trị `0 cổng`.** `có nhắc: <tệp>×<n>` đo sự CÓ MẶT của cái tên,
  không đo cưỡng chế — kho đã trả giá bốn lần cho đúng chỗ đó (`which(gh)` · `rest-chung` ·
  `gh auth status` · `mcp` gộp). Biến nó thành phép đo thật cần một phản chứng cho từng ADR, tức
  một packet riêng.
- **Bảng §20 không phán xử HIỆU LỰC.** Đo được bốn cách viết cho cùng một nghĩa, và `ADR-0036` ghi
  *"Superseded một phần bởi ADR-0041"* — khớp tiền tố `Superseded` sẽ loại một ADR **vẫn còn hiệu
  lực một phần**. Cổng cố ý chỉ đòi CÓ MẶT; ai muốn cổng đọc được hiệu lực thì phải chuẩn hoá từ
  vựng trạng thái trước, và đó là một quyết định, không phải một bản vá.

---

## 5. Khai VƯỢT NGƯỠNG — theo đúng cửa thoát của `ADR-0044`

Thay đổi của phiên này: **6 tệp · +1440/−2**. Trần `ADR-0044` cho packet `sensitive` chạm authority
là **≤ 3 tệp và ≤ 300 dòng thêm**. Khai thay vì lờ đi, và tách hai phần vì rủi ro của chúng khác họ:

| phần | tệp | dòng thêm | rủi ro |
|---|---|---|---|
| **mã + phản chứng** | `.claude/dev/packet_loop.py` · `.claude/dev/packet_loop_test.py` | +797 | chạy sai |
| **văn bản** | `CLAUDE.md` · `docs/PROTOCOL_DA_PHIEN.md` · `ops/NO_KY_THUAT.md` · `ops/HOAN_THIEN_KE_HOACH_20260822.md` | +643 | viết sai chữ |

```
git diff --numstat $(git merge-base origin/master HEAD)
```

**Phần mã: 2 tệp, +797.** Trong đó **phản chứng chiếm phần lớn**
(`packet_loop_test.py` +561: 27 ca + 16 đột biến); cổng chỉ +236. Cắt cho vừa 300 nghĩa là cắt phản
chứng, tức đổi một con số lấy chính thứ làm cổng có răng — `CLAUDE.md` gọi đúng cái đó là *"chỗ các
ca đi chết"*. Đây cũng không phải authority theo nghĩa hẹp của `ADR-0044`: `packet_loop.py` không cấp
lease và không gác đường đăng; thứ ấy là `ops/lease_publish.py`, mà phiên này **không đụng**.

**Phần văn bản: +643 trên 4 tệp.** Không dòng nào nằm trên đường chạy của `scripts/tl.py` hay của
cổng đăng lease. Ngưỡng của `ADR-0044` neo từ số đo về **chi phí review MÃ** (`PLAT-M4` 2 tệp/+351 →
một vòng một finding; `PLAT-X4` 4 tệp/+721 → ba vòng tám finding); áp nguyên si sang một thay đổi tài
liệu là áp sai đối tượng. Tiền lệ đã được chấp nhận: PR #210 khai đúng lý lẽ này cho 13 tệp/+861.

**Nếu người review thấy ngược lại, tách được sạch theo bốn nhóm:** (1) cổng `adr-song` + phản chứng ·
(2) §20 của protocol + dòng 7 · (3) hai mục sổ nợ · (4) tài liệu này. Nhóm (1) và (2) phải đi cùng
nhau — cổng đo §20, nên tách rời thì một trong hai nhánh có cổng đỏ.

**Va chạm đã biết, khai trước để người merge không phải tự tìm:**

| tệp | va với | xử |
|---|---|---|
| `ops/NO_KY_THUAT.md` | PR #230 thêm `## 12.` | phiên này bắt đầu từ `## 13.` và nói ra ngay trong §13. #230 không land ⇒ đánh số lại |
| `CLAUDE.md` | PR #229 thêm 8 dòng quanh dòng 527 | phiên này sửa quanh dòng 517, cách 10 dòng — merge sạch nếu #229 land trước |
| `ops/lease_publish*` | lease `#227` còn hiệu lực tới `23-08T01:00Z` | phiên này **KHÔNG đụng**; con trỏ chết `t42` ở §1.3 để lại cho phiên giữ lease ấy |
| `ops/NO_KY_THUAT.md` | lease `slice-b-c-exec-1-claude-20260821` (#215), `access: read-write`, **chưa hết hạn** tới `22-08T06:40Z` | xem §5.1 |

### 5.1 Một va chạm write set THẬT — và một phép đo hỏng suýt giấu nó

`ops/NO_KY_THUAT.md` nằm trong `write_set` của một lease **chưa hết hạn** lúc phiên này ghi vào đó.
Nhưng packet `#215` **đã land** — hiện vật có trên `master` (§2), nên quyền ghi ấy **đã tiêu**. Đây
đúng là nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`: *"chưa hết hạn"* không phải *"còn hiệu lực"*, và
không trường nào trong tệp lease nói ra điều đó — phải đi tìm hiện vật mới biết.

**Chỗ đáng ghi hơn là cách nó suýt bị giấu.** Phép quét va chạm chạy TRƯỚC khi ghi báo **0 va chạm**,
và con số ấy SAI: script khớp `lease_expires_at_utc:` theo sau bởi nháy KÉP tuỳ chọn, trong khi YAML
ghi nháy ĐƠN. Không lease nào đọc được hạn ⇒ tất cả rơi khỏi tập "chưa hết hạn" ⇒ báo sạch. **Cùng
một regex hỏng cắn hai lần trong một phiên** — lần kia ở §2.1, biến 16 thành 0. Một phép đo an toàn
trả về RỖNG trông y hệt một phép đo trả về SẠCH, đúng bài học *"vắng mặt vì sạch và vắng mặt vì chưa
chạy nhìn giống hệt nhau"*.

**Chốt rẻ, dùng được ngay — và nó là điều kiện tối thiểu cho mọi phép quét lease sau này:** in số
lease **ĐỌC ĐƯỢC HẠN** bên cạnh số va chạm, rồi **thoát khác 0 khi hai số không bằng nhau**.
`đọc được 93/93` cạnh `va chạm 0` là một kết luận; `đọc được 0/93` cạnh `va chạm 0` là một lỗi. Hai
số bằng nhau chính là dạng bằng-chứng-dương mà `CLAUDE.md` đòi cho mọi cổng.

Đây cũng là đầu vào cụ thể cho nợ `SO-LEASE-KHONG-NAM-MOT-CHO`: lệnh *"lease nào đang giữ đường dẫn
X"* khi được viết phải mang sẵn chốt này, kẻo nó thành cổng câm ngay từ ngày đầu.
