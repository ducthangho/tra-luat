# Thẩm định AG-T0-03 sau khi land, và hợp nhất hai kế hoạch thi công

> **Trạng thái:** hồ sơ thẩm định + biên bản quyết định. Không cấp authority.
> Authority nằm ở Packet Spec, GitHub facts và receipt đã verify.
>
> Mọi con số dưới đây là **đo được**, kèm cách tái lập. Không con số nào gõ tay.

Nền đo: `origin/master` `47847b1812c2703a385549b767f6bf1ce979db4b`
(AG-T0-03 đã land qua PR #175, squash).
Mọi lượt chạy đặt `core.abbrev 7` — đúng như `.github/workflows/ci.yml` ghim.

---

## 1. Hai phép đo môi trường phải ghim trước, nếu không mọi kết luận sau đều sai

### 1.1 `git fetch` qua proxy phiên remote NÓI DỐI; chỉ `git ls-remote` là sự thật

Đo được: sau khi `git push` trả `rc=0`, `git fetch origin --prune` vẫn trả về ref CŨ.
`git ls-remote origin` cùng lúc trả ref MỚI, đúng.

Hệ quả: bài học "đăng lên GitHub xong phải ĐỌC NGƯỢC VỀ" **không chỉ áp cho đường
GitHub API** — nó áp cho cả đường git. Và công cụ đọc ngược phải là `ls-remote`,
không phải `fetch`, vì `fetch` có tầng cache riêng.

### 1.2 Selftest ĐỎ GIẢ 2 ca khi `core.abbrev` = 8

Đo được trên clone đủ lịch sử (1155 object ⇒ git tự nới abbrev lên 8):

```
core.abbrev = 8 (mặc định)  -> 1695/1697, rc=1
                               [FAIL] r218_docclaims_l2_sha_khong_ton_tai
                               [FAIL] r264_doc_claims_phu_docs
core.abbrev = 7 (CI ghim)   -> 1697/1697, rc=0
```

Cơ chế đã được ghi sẵn trong chú thích của `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`:
ngưỡng L2 lấy từ `git rev-parse --short`, mà git nới độ dài viết tắt theo số object.
Ngưỡng 8 trùng độ dài tiền tố UUID notebook ⇒ 18 tiền tố bị hô `SHA_NOT_A_COMMIT`.

CI xanh vì ghim `core.abbrev 7`. **Máy dev không ghim thì đỏ oan** — và đỏ oan này
đứng TRƯỚC mọi cổng khác, nên nó che mất phép đo thật. Ai thẩm định trên clone đủ
lịch sử mà bỏ qua điều này sẽ kết luận "master đang đỏ" — sai.

---

## 2. Thẩm định AG-T0-03: một lỗi làm hỏng đúng tính năng của chính packet

### 2.1 Phép đo

| commit | `tl registry-coverage` (đường người vận hành chạy) | `golden-test` |
|---|---|---|
| `33bfd8d0` (trước F8) | 166/196 = **84.69 %** | rc=0 |
| `7ea03ad4` (sau F8)   | 0/196 = **0.00 %**   | **rc=2 — ĐỎ** |

### 2.2 Căn nguyên

F8 muốn gộp thêm `NESTED_COMMAND_META` chứ không chỉ `COMMAND_META` — **ý định đúng**.
Nhưng bản vá đổi

```python
meta = getattr(tl_module, "COMMAND_META", all_command_meta())   # fallback GÁNH VIỆC
```

thành

```python
raw_top = getattr(tl_module, "COMMAND_META", {})                # fallback thành RỖNG
```

Đường sản xuất truyền `tl_module=_TL`, tức chính `scripts/tl.py`. Mà `tl.py` **không
export** bảng metadata nào — `COMMAND_META` và `NESTED_COMMAND_META` là hằng
module-level của `tl_core/command_registry.py`. Nên meta thành rỗng, và báo cáo tuyên
bố toàn bộ CLI không có lệnh nào được đăng ký.

Đây là lớp lỗi "vá một finding bằng cách gỡ mất thứ đang gánh việc" — bản vá đúng ý
định, sai hệ quả, và hệ quả nằm ở nhánh mà không test nào đi qua.

### 2.3 Đã được chặn trước khi land

Phiên thi công tự phát hiện và vá bằng guard `hasattr` trước khi merge. Master hiện
đo đúng 84.69 %, `golden-test` rc=0. **Finding này khép.**

### 2.4 Vì sao 7/7 ca unit vẫn XANH trong khi tính năng hỏng hoàn toàn

Mọi ca trong `scripts/tl_core/command_registry_test.py` hoặc:

- gọi `compute_parser_coverage(parser)` — `tl_module=None`, rơi vào nhánh ĐÚNG; hoặc
- truyền `MockTLModule` — một mock **có sẵn** `COMMAND_META`.

Mock dựng đúng cái mà module thật thiếu, nên nó che chính xác chỗ thủng. Cùng họ với
bài học đã ghi ở `launcher.py`: **"ca có MẶT khác ca có ĐO"**.

---

## 3. Hai lỗ còn hở SAU khi land — và cách đã vá

Nhánh: `fix/ag-t0-03-regression-guard`, nền `47847b1`.

### 3.1 Lỗi đã vá nhưng KHÔNG có gì giữ

Guard `hasattr` chặn được, nhưng không ca nào cưỡng chế nó ⇒ nó quay lại được bất cứ lúc nào.

Đã thêm `r332_registry_coverage_duong_san_xuat` vào `scripts/tl_selftest.py`. Ca này
**không import hàm và không mock** — chạy `scripts/tl.py registry-coverage --json`
bằng subprocess, đúng như người vận hành và CI gọi, rồi đòi hai điều:

1. `coverage_percent > 0` và `registered_leaf_commands > 0` — phản chứng trực tiếp;
2. số của đường CLI **khớp** số của `validate_registry` — chặn tái diễn "hai đường
   cho hai đáp số" mà chỉ một đường bị golden soi.

**Phản chứng đã chạy** (đây là điều kiện để ca được coi là gánh việc, không phải trang trí):

```
gỡ guard `hasattr`  -> [FAIL] r332 · 1697/1698 · rc=1
giữ guard           -> [OK]   r332 · 1698/1698 · rc=0
```

### 3.2 Bộ unit test của packet CHƯA TỪNG chạy trong CI

`scripts/tl_core/command_registry_test.py` không nằm trong `scripts/test_fragments/`
nên `tl.py --selftest` không khám phá ra nó.

Bằng chứng: ở lượt land, selftest đếm **1697/1697 trên CẢ master lẫn nhánh packet** —
7 ca mới không hề được tính. Nghĩa là bằng chứng "7/7 ca" chỉ tái lập được bằng tay,
và CI sẽ không bao giờ đỏ khi ai đó làm hỏng `compute_parser_coverage`.

Đã thêm bước CI riêng chạy thẳng tệp. Giữ nguyên vị trí tệp (không chuyển sang
`test_fragments/`) để không đụng vào topology gói đang sát trần 200.

### 3.3 Cổng đo tại chỗ trên nhánh vá

```
unit test packet            7/7        rc=0
tl selftest              1698/1698     rc=0   (transport 12/12)
golden-test                            rc=0
gen_instructions           44/44       rc=0
doc-claims-check --strict              rc=0
bundled-fragment                       rc=0
eol-policy 30/30 · pre-push 9/9        rc=0
gate lifecycle             28/28       rc=0
lease-publish              31/31       rc=0
file_count 180 (trần 200, còn 20 khe)
```

---

## 4. Kết quả thật mà packet AG-T0-03 phơi ra

Đây là giá trị của packet, tách khỏi lỗi ở trên:

```
tổng lệnh lá          196
đã có metadata        166   (84.69 %)
CHƯA có metadata       30
trong đó RỦI RO CAO     4   hygiene plan · hygiene reconcile
                            profile-file-add · reconcile
```

30 lệnh không có metadata nghĩa là ~15 % bề mặt CLI **không đi qua hệ phân loại rủi
ro** — registry là thứ lái `risk` / `requires_confirm` / `write_scope`. Bốn lệnh rủi
ro cao mang cờ ghi (`--apply`/`--delete`/`--trash`/`--write`/`--purge`) mà không khai
metadata là nợ đáng đóng trước, không phải đóng đủ 30.

Lưu ý về phép đo "rủi ro cao": nó là heuristic theo **danh sách cờ cứng**. Danh sách
đó chưa được phản chứng nào ghim, nên một lệnh ghi dùng cờ ngoài danh sách sẽ lọt.
Đây là hạn chế đã biết của `parser_tree_coverage.v1`, không phải lỗi.

---

## 5. Hợp nhất hai kế hoạch

Hai kế hoạch đang cùng sống:

- **cũ** — `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md` (lane `W0-*`/`W1-*`/`W2-*`)
- **mới** — `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` + `ops/KE_HOACH_THI_CONG_ANTIGRAVITY.md`

### 5.1 DÙNG ĐƯỢC — giữ nguyên

| Thứ | Vì sao giữ |
|---|---|
| Review bundle (§5) + validation receipt (§9) | Đã có hạ tầng CHẠY ĐƯỢC: `ops/chatgpt_review/` với 3 schema, `build_bundle.py`, `validate_note.py`, bộ test. Phần chắc nhất của kế hoạch mới. |
| Ba tầng Review Class `routine`/`systemic`/`sensitive` | Tương thích ngược với cột rủi ro từng packet của kế hoạch cũ — không phải làm lại bảng packet. |
| Nguyên tắc **Evidence Defect thắng Review Class** | Ý mạnh nhất trong cả hai kế hoạch: khuyết tật bằng chứng (SHA rút gọn, gate skip, head stale) chặn land bất kể tầng rủi ro. |
| Quy trình 8 bước (§4 kế hoạch AG) | Thực chất là protocol §12 viết lại. Đã được cưỡng chế bằng `.claude/dev/packet_loop.py`. Không cần xây mới. |
| Non-convergence: dừng sau N vòng | Đúng nguyên tắc; xem §5.2 về việc N đang mâu thuẫn. |

### 5.2 CẦN ĐIỀU CHỈNH

**(a) Cột write-set trong bảng packet đang sai có hệ thống.**
AG-T0-03 khai 3 tệp (`command_registry.py`, `workflow.py`, `test_fragments/<packet>.py`),
thực tế đụng **10** tệp. `references/golden/parser_surface.json` bị khai thuộc AG-T0-05
nhưng AG-T0-03 buộc phải đụng.

Đây **không phải vi phạm phạm vi** — là tái sinh cơ học bắt buộc khi thêm một lệnh.
Kế hoạch phải tách **write set** (thứ người viết tay) khỏi **derived set**
(`references/golden/*.json`, `RELEASE_MANIFEST.json` — thứ máy sinh lại). Không tách
thì cổng phạm vi sẽ báo vi phạm giả ở mọi packet có thêm lệnh.

**(b) Quy ước vị trí test chưa được cưỡng chế.**
Kế hoạch ghi `scripts/test_fragments/<packet>.py`; thi công làm khác, và hậu quả đo
được là test tàng hình với cả selftest lẫn CI (§3.2). Phải chọn một: cưỡng chế quy ước
fragment, hoặc bắt buộc khai bước CI trong Packet Spec. Bản vá hiện tại đi đường thứ hai.

**(c) Ngân sách review MÂU THUẪN giữa hai kế hoạch.**
Kế hoạch mới: tối đa **2 vòng** model review mỗi PR. `W0-R1` của kế hoạch cũ vừa xây
xong "ngân sách review tách khỏi ngân sách executor + Review Rescue Checkpoint" và đã
chạy **4 vòng**. Hai mô hình không tương thích — phải quyết một trước khi nhận packet
review tiếp theo.

**(d) Kế hoạch Antigravity §3 tự mâu thuẫn với kế hoạch đa provider §12.**
§12 cấm lưu trạng thái động (số PR, đã land chưa, nợ review) trong tài liệu kế hoạch
tĩnh. §3 lưu đúng những thứ đó (`landed_reaudit_pending (PR #163)`…). Một trong hai
phải nhường — nếu không, tài liệu sẽ trôi khỏi sự thật đúng như §12 cảnh báo.

### 5.3 BỎ

| Thứ | Vì sao bỏ |
|---|---|
| `W0-C1`, `W1-C2a` (lane "Codex candidate") | Codex hết quota là vật cản thường trực, không phải sự cố. Kế hoạch đa provider đã thay bằng AG + ChatGPT Web. |
| Toàn bộ **M3 / `W2-*`** (Blocking Authority, GitHub App publisher, Check Run canary) | Chính kế hoạch cũ đã gác sau điều kiện "chỉ khi số đo yêu cầu". Chưa có số đo nào yêu cầu, và kế hoạch mới không cần. |
| Giả định "Codex là reviewer chéo của hồ sơ" | Không còn đúng. Reviewer chéo nay là tập hợp AG / ChatGPT Web / Human Auditor / Claude, chọn theo Review Class. |

### 5.4 GIỮ — quyết định đã lấy

`#177` (W0-R1B) và `#178` (W0-RC) là packet của kế hoạch cũ trên `packet_loop.py`, và
bảng packet của kế hoạch mới không có chúng.

**Quyết: GIỮ.** Lý do: `packet_loop.py` vẫn là thứ cưỡng chế các điều kiện dừng của
protocol §12 mà **cả hai** kế hoạch đều dựa vào. Hai packet này vá lỗ thật trong nó —
`#177` là trần review đang tự nguyện, `#178` là 9 cửa cưỡng chế không có phản chứng.
Bỏ chúng là bỏ nền móng mà kế hoạch mới đứng lên.

Hệ quả: lane `W0-R*` **không** bị kế hoạch mới thay thế. Nó chạy song song, và
`#177` vẫn phụ thuộc `W0-R1 integrated`.

### 5.5 Hiện vật của kế hoạch cũ trên master

```
CÓ   .claude/dev/launcher.py · launcher_test.py
CÓ   .claude/dev/packet_loop.py · packet_loop_test.py
CÓ   .claude/dev/gate_lifecycle.py · gate_lifecycle_test.py
—    .claude/dev/review_connector.py                       (W0-C1, đã BỎ)
—    .github/workflows/review-connector-shadow.yml         (W1-C2b, đã BỎ)
—    ops/review_receipt.py                                 (W0-R2, còn treo)
—    .github/coordination/schemas/review_verdict.v1.schema.json  (W1-P1, còn treo)
```

---

## 6. Nợ còn treo

1. **Cross-review codex cho `W0-R1`.** Assurance hiện là `same_provider_approved`
   (reviewer Fable 5, cùng nền Claude với executor). Đo được lúc thẩm định:
   `codex exec` trả `You've hit your usage limit ... try again at Aug 20th, 2026 6:23 AM`.
   Lưu ý: `codex login status` trả `rc=0 Logged in` KỂ CẢ khi hết quota — token còn
   hạn 159,6 h, nghẽn là quota chứ không phải xác thực. Chỉ
   `python3 .claude/dev/launcher.py doctor --kiem-song` cho tín hiệu trung thực.

2. **Hai re-audit của kế hoạch Antigravity** (`AG-T0-04`/PR #163, `AG-T0-02`/PR #164),
   cả hai `landed_reaudit_pending` vì `reviewed_sha` là SHA rút gọn và stale.

3. **`fix/ag-t0-03-regression-guard` chưa land** — chờ review rồi human land trên
   exact SHA, đúng §12.

4. **Nhánh `agent/ag-t0-03-parser-coverage` là nhánh mồ côi.** GitHub đã xoá nó khi
   merge PR #175; một lượt push sau đó đã hồi sinh nó ở `83cd05a`. Nội dung không còn
   giá trị (phần hữu ích đã nằm trong master + nhánh vá). Cần xoá bằng tay: proxy của
   phiên remote CHẶN xoá ref (403) dù cho phép tạo/cập nhật.
