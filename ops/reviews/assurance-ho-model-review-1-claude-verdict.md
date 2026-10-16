# Verdict lượt 1 — Packet #551 `ASSURANCE-NEO-VAO-HO-MODEL` (r2/g2)

- **Kết luận:** `changes_requested`
- **Neo `reviewed_sha`:** `f4684e45d77bf7c4aa9144b92b8043bb1774de68`
- **PR:** [#557](https://github.com/ducthangho/tra-luat/pull/557) · nhánh `claude/assurance-ho-model-r2-g2`
- **Đặc tả:** `ops/specs/assurance-neo-vao-ho-model-r2.md`, `sha256 567e68745b6d22aa4e095062f886f90810ff5f004a6b74b6da967d5dcff54192`
- **Lease:** `assurance-ho-model-r2-g2-claude`
- **Thời điểm đo:** `2026-09-18T08:23Z` (phép đo chạy trong khoảng `08:12Z`–`08:23Z`)

## 0. HAI GIỚI HẠN CỦA CHÍNH LƯỢT NÀY — đọc trước mọi phát hiện

**(a) Xung đột lợi ích đã khai.** Phiên này **viết đặc tả r2** mà lượt này đem ra đối chiếu, và
**ghi cả hai lease** (gen 1 và gen 2) của packet. Nó KHÔNG viết bản vá — phần độc lập về
*triển khai* là thật — nhưng phần đối chiếu *tiêu chí nghiệm thu* là tự chấm bài mình ra đề.
Cụ thể: `A1`–`A12` do phiên này soạn, nên một tiêu chí soạn SAI sẽ không bị lượt này bắt.

**(b) Lượt này KHÔNG PHẢI `cross_approved` — theo đúng luật mà chính bản vá đang dựng.**
Executor là một phiên Claude Code; reviewer là phiên này, cũng họ model `claude`. Áp
`_giai_ho_model_reviewer` / `_giai_ho_model_executor` của bản vá lên chính cặp này ⇒ `claude` vs
`claude` ⇒ `same_provider_approved`. Lease khai `reviewer_provider: codex`; để đạt `cross_approved`
vẫn phải có một lượt codex. Verdict này là **`advisory_review`**.

## 1. Bảng đo — kê CẢ cái khớp

Rig: hai vế dựng trong **MỘT** lệnh (`rig557.py`), clone thật có lịch sử, `checkout --detach`,
`core.abbrev 7`, `shallow=false`, `status --porcelain` rỗng cả hai vế. `rc` đọc TRỰC TIẾP.

| cổng | nền `d705623` | ứng viên `f4684e4` | delta |
|---|---|---|---|
| `ops/bien_nhan_v2.py` | rc=0 · `124 ĐẠT v2 · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 177` | rc=0 · **cùng số** | 0 |
| `ops/bien_nhan_v2_test.py` | rc=0 · `48/48 ca · 63/63 CÓ RĂNG · 2/2 tự kiểm` | rc=0 · `51/51 ca · 65/65 CÓ RĂNG · 2/2 tự kiểm` | +3 ca, +2 đột biến |
| `doctrine-scan` | rc=0 | rc=0 | 0 |
| `adr-song` | rc=0 · 49 ADR / 49 dòng §20 | rc=0 · **50 / 50** | +1, khớp 1–1 |
| `doc-claims-check --strict` | rc=0 | rc=0 | 0 |
| `git diff --check` | rc=0 | rc=0 | 0 |
| `release-verify --strict --json` | rc=0 · `ok=true` | rc=0 · `ok=true`, `expected == checked == 180` | 0 |

Write set: **đúng 6 đường** đã khai, **165 dòng thêm** / 18 xoá — dưới trần 250 của ngoại lệ
ADR-0044 đã cấp. Không chạm đường nào ngoài write set.

`A1` **ĐẠT, đo bằng máy chứ không bằng mắt**: câu neo CŨ còn `0` lần trong PROTOCOL, câu neo MỚI
đúng `1` lần, và cả `3` mục của `_NEO_LUAT_CHEP_TAY` đối chiếu ngược về tệp nguồn đều `đếm=1`.

**Đột biến `m62`/`m63` có răng THẬT, không phải tín dụng giả.** Bộ test có bộ phân hạng
`TinHieuChotCa` (`ops/bien_nhan_v2_test.py:118`), và cả hai được xếp `giet_that` — tức ca đích đỏ
vì **chốt của nó**, không vì một ngoại lệ vô can. Đây là chỗ bản vá làm tốt và đáng nói ra.

## 2. Phát hiện

### P1-1 — Thiếu trường executor thì chốt **IM LẶNG BỎ QUA**, và **8/50** biên nhận thật của kho đang ở đúng trạng thái ấy

`ops/bien_nhan_v2.py:730` — `if ho_rev and ho_exec and ho_rev == ho_exec:`. Hai vế rỗng làm
điều kiện sai ⇒ không lỗi nào được thêm ⇒ `cross_approved` **qua**.

Đo trên toàn bộ biên nhận của kho, bằng CHÍNH hàm của bản vá:

```
TONG bien nhan khai cross_approved : 50
  KHAC ho model (chot DE qua, dung) : 42
  CUNG ho model (chot PHAI chan)    : 0
  ho EXECUTOR RONG -> chot BO QUA   : 8      <-- fail-OPEN
```

Tám tệp: `don-nhanh-base-review-{1,2}`, `n5-lenh-hook-windows-review-{1,2}`,
`t33-doi-shellcheck-review-{1,2,3,4}` (`-codex-verdict.receipt.yaml`). Cả tám có `ho_rev=gpt` và
`ho_exec` RỖNG. Đây **không** là ca giả định: chúng là tám lời khai `cross_approved` mà cổng mới
không kiểm được câu hỏi duy nhất nó sinh ra để hỏi.

Ca đối chứng biết trước đáp án (chứng minh rig không hỏng): `claude review codex` ⇒ **QUA**;
`claude review claude` ⇒ **CHẶN**. Rồi bỏ `executor_provider` khỏi ca thứ hai ⇒ **QUA**.

Đây là doctrine `None ≠ False` / ba trạng thái: `có` · `không` · **`không đo được`**, và trạng
thái thứ ba phải làm cổng ĐỎ. ADR-0050 của chính bản vá **đã có tên cho nó** (`khong_do_duoc`),
nhưng cổng không bao giờ ánh xạ "thiếu trường" về mức ấy.

**Đề xuất:** thiếu một trong hai vế ⇒ `khong_do_duoc` ⇒ **từ chối** `cross_approved` (hoặc tối
thiểu liệt vào `KHÔNG ĐO ĐƯỢC` thay vì `ĐẠT`). Tám biên nhận cũ xử theo `ALLOWLIST_CUTOVER`/`NO_DA_DO`
như tiền lệ đã có, chứ không nới luật cho chúng.

### P1-2 — Bảng mặc định `google_antigravity → gemini` **tái mở đúng cái lỗ mà ADR-0050 sinh ra để bịt**

`ops/bien_nhan_v2.py:157`. Đo:

```
agy (khong khai model) <- claude review   rev=claude exec=gemini  -> **QUA** (cross_approved)
agy KHAI model claude  <- claude review   rev=claude exec=claude  -> CHAN        [doi chung]
```

Chính ADR-0050 trích `ops/specs/ag-t0-01b-r3.md:47-51` làm căn cứ: *"Một phiên AG đặt
`--model claude-opus-4-6-thinking` rồi được một phiên Claude Code review là cùng một họ model,
khác vỏ công cụ — tức `same_provider_approved` đội lốt `cross_approved`"*. Bản vá bịt ca ấy **chỉ
khi biên nhận tự khai model**, và **mặc định** ca ấy sang `gemini` khi không khai. Nhưng biên nhận
không khai model là ca THƯỜNG, không phải ca hiếm: `50/50` biên nhận `cross_approved` hiện có mức
bằng chứng model RỖNG.

Nói cho đúng hình dạng: một **giá trị mặc định đang khẳng định một sự thật chưa ai đo**. Cùng họ
`ĐÃ ĐẶT ≠ DÙNG ĐƯỢC` — ở đây là *ĐÃ KHAI PROVIDER ≠ ĐÃ BIẾT MODEL*. Và nó làm packet **đạt mục
tiêu bằng cách giả định đúng cái nó phải đo**.

**Đề xuất:** bảng mặc định chỉ dùng cho provider mà hãng **cố định một họ model** (`openai_codex`,
`anthropic_claude`). Với vỏ công cụ **đa model** (`google_antigravity`, `openai_api`, `llm`) thì
provider **không suy ra được** họ model ⇒ `khong_do_duoc` ⇒ đòi khai model tường minh. Nếu chủ kho
muốn agy đi đường nhanh thì đó là một **ngoại lệ có tên, có hạn**, không phải một dòng bảng im lặng.

### P1-3 — Thang ba mức bị **LẬT NGƯỢC**: `do_may` là đường RẺ NHẤT, và mức bịa đặt cũng qua

`ops/bien_nhan_v2.py:734` chỉ đặc biệt hoá đúng một chuỗi, `khai_co_audit`. Đo:

| mức bằng chứng khai | kết quả |
|---|---|
| `khai_co_audit`, thiếu người audit | **CHẶN** |
| `do_may` (không ai đo gì) | **QUA** |
| `khong_do_duoc` | **QUA** |
| `xin_the` (mức BỊA ĐẶT) | **QUA** |
| RỖNG | **QUA** |

Ba hệ quả, cả ba đo được:

1. Mức mà ADR gọi là **MẠNH NHẤT** (`do_may`) có **ÍT ràng buộc nhất**. Muốn né đòi hỏi người
   audit thì chỉ cần gõ `do_may` — không cổng nào hỏi lấy một câu. Thang khuyến khích đi ngược
   với thang an toàn.
2. `khong_do_duoc` — nghĩa đen là *"không xác minh được model thực tế"* — vẫn cấp `cross_approved`.
3. Trường là **chuỗi mở**: không có tập giá trị hợp lệ. Đây đúng bài học đã trả giá
   (`v1.36.68`, PR #104): **danh sách CẤM không bao giờ đủ, phải đảo thành danh sách CHO PHÉP** —
   mà ở đây thậm chí chưa có danh sách cấm, chỉ có một ca đặc biệt.

**Đề xuất:** `MUC_BANG_CHUNG_MODEL = {"do_may", "khai_co_audit", "khong_do_duoc"}` là **allowlist**;
giá trị ngoài tập ⇒ ĐỎ. `khong_do_duoc` và RỖNG ⇒ không đủ cho `cross_approved`. `do_may` phải trỏ
được một hiện vật đo (trường `model_evidence_ref`: `run_id`/đường dẫn telemetry), đúng như
`docs/GOI_AGENT_DA_NEN.md` đã làm với `modelUsage[*].canonicalModel` — kho đã có vị từ
`kiem_ket_qua` trong `.claude/dev/chon_reviewer.py`, đừng dựng mức "đo máy" mà không nối vào nó.

### P2-1 — `_ho_model_cua_ten` phân biệt **CÁCH VIẾT**, không phân biệt **HỌ**

`ops/bien_nhan_v2.py:648` nhận đúng ba họ (`claude` · `gpt` · `gemini`); mọi tên khác rơi xuống
`return t`, tức **chuỗi thô** thành "một họ riêng". Đo:

```
grok-4      vs grok-3      -> **KHAC ho (QUA)**
llama-70b   vs llama-8b    -> **KHAC ho (QUA)**
deepseek-v3 vs deepseek-r1 -> **KHAC ho (QUA)**
claude-opus-5 vs Claude Opus 5 -> cung ho (CHAN)   [doi chung, dung]
```

Với `cross_approved`, câu hỏi là *"có CHẮC hai bên khác họ không"*. Không nhận ra tên thì câu trả
lời đúng là **không chắc**, chứ không phải **khác**. Bản vá trả lời "khác" ⇒ fail-open lần thứ ba,
cùng gốc với P1-1 và P1-3. Nguyên văn của reviewer ngoài trong bài học kho:
*"distinguishes spelling, not authority"*.

**Đề xuất:** tên không nằm trong bảng nhận diện ⇒ `khong_do_duoc` ⇒ ĐỎ. Kèm ca đột biến: **nới**
bảng nhận diện để nuốt một tên lạ phải làm ca đích ĐỎ — không có đột biến ấy thì không biết ca
đang đo bảng hay đo thứ khác.

### P2-2 — §20 khai `ADR-0050` là **0 cổng** trong khi **cùng commit** dựng cổng đọc nó

`docs/PROTOCOL_DA_PHIEN.md:1389` ghi cột "cổng nào ĐỌC luật ấy" = `**0 cổng**`. Nhưng cùng commit:
`_NEO_LUAT_CHEP_TAY` neo nguyên văn câu §8 mới, và `_thieu` cưỡng chế tách họ model — tức
`ops/bien_nhan_v2.py` **là** cổng đọc luật ấy, mạnh hơn `ADR-0049` (chỉ "có nhắc").

Dòng ấy sai ngay lúc được viết, và `adr-song` **không** bắt được: nó canh đăng ký + trạng thái,
không canh tính đúng của cột phủ. Đây là sổ ADR tự khai thiếu năng lực mình đang có — chiều sai
hiếm, nhưng vẫn là sổ nói không đúng.

**Đề xuất:** đổi thành `ops/bien_nhan_v2.py` (`_NEO_LUAT_CHEP_TAY` + chốt tách họ model).

### P2-3 — ADR-0050 gán một quyết định cho chủ kho mà **không neo được vào đâu**

`docs/adr/0050-...md:3` — *"Accepted (2026-09-17, chỉ thị chủ kho `ducthangho`, thực thi theo
Packet #551)"*. Không có URL, không có comment id. Hai chỗ lệch đo được:

- **ngày `2026-09-17`** đứng TRƯỚC cả lúc đặc tả r2 đóng băng (`2026-09-18T07:45Z`) lẫn comment chỉ
  thị `#551 issuecomment-5726836582`;
- chỉ thị nguyên văn của chủ kho mà phiên này ghi lại được là *"Cấp Revision 2 cho Packet #551 đi"*
  — một chỉ thị **cấp revision**, không phải một quyết định kiến trúc "neo vào họ model". Nội dung
  ấy đến từ **đặc tả**, mà đặc tả do phiên review này viết.

Một câu chống đỡ **THẨM QUYỀN** thì không còn là câu mô tả; nó là một lời khai và phải có mỏ neo bền.

**Đề xuất:** neo `granted_on_instruction` (URL comment) ngay trong ADR, hoặc viết đúng nguồn:
*"quyết định kiến trúc do đặc tả r2 `567e6874…` đề xuất, chủ kho cấp Revision 2 tại <URL>"*.

### P3-1 — `"o1" in t` / `"o3" in t` là khớp chuỗi con trên tên tự do

`ops/bien_nhan_v2.py:655`. Chưa tìm được tên model thật nào va chạm, nên để P3 — nhưng nó cùng
hình dạng với P2-1 và sẽ chết theo nếu đảo sang bảng nhận diện tường minh.

## 3. Tổng kết theo LỚP

| lớp | mã | trạng thái |
|---|---|---|
| fail-open khi thiếu dữ kiện | `P1-1` · `P2-1` | chưa vá — **cùng một gốc, ba đường vào** |
| mặc định khẳng định sự thật chưa đo | `P1-2` | chưa vá |
| thang bằng chứng không có danh sách CHO PHÉP | `P1-3` | chưa vá |
| sổ/ADR khai sai phạm vi | `P2-2` · `P2-3` | chưa vá |
| khớp chuỗi con | `P3-1` | chưa vá |

**Lưu ý khi vá — bài học #513:** `P1-1`, `P1-3`, `P2-1` là **ba đường vào của MỘT lỗ**: "không biết"
bị đọc thành "khác nhau". Đừng vá theo danh sách này rồi dừng. Hãy **tự liệt kê hết đường trước**
(thiếu trường · mức bằng chứng lạ · tên model lạ · provider đa model · `mri` không phải dict), đóng
cả loạt, và cho **mỗi đường một chốt riêng** để đột biến gỡ từng cái đều làm một ca ĐỎ. Ba chốt
không phân biệt được bằng đầu vào thì chúng là bộ tương đương và bạn chỉ đang đo một cái.

## 4. Việc ngoài bản vá (không tính là phát hiện)

`origin/master` đã tiến tới `eb15657d` (merge PR #553) SAU khi nhánh này rẽ, nên `eb15657d`
**không** là tổ tiên của `f4684e45`. Cổng `thu-hoi` đòi quan hệ ấy và sẽ `CHAN [12]` ở lượt chạy
kế. Đây là hệ quả của lần merge do phiên này thực hiện, **không** phải khuyết tật của bản vá: merge
`origin/master` vào nhánh packet (đừng rebase) rồi neo verdict lượt sau vào head SAU merge.
Write set của hai bên rời nhau hoàn toàn nên không có xung đột nội dung dự kiến.

## 5. Chưa đo được

- **`gate (windows-latest)`** — chủ kho đặt `manual_ci_budget: 0`. Không gọi `workflow_dispatch`,
  không gọi tay lane `windows`. Là **KHÔNG DÙNG PHƯƠNG TIỆN**, không phải "đã đo và xanh".
- **Lượt `cross_approved` thật** — cần một lượt codex theo `reviewer_provider` của lease. Lượt này
  cùng họ model với executor, nên tự nó là `same_provider_approved` theo đúng luật đang xét.
- **Tám biên nhận `ho_exec` RỖNG có thật sự khác họ model hay không** — không có dữ liệu model
  trong tệp, và transcript của các lượt ấy không còn. Đúng nghĩa `khong_do_duoc`.

---

**Nguồn có thẩm quyền là tệp có băm trong kho; mọi bản đăng lên GitHub chỉ là bản chiếu.**
