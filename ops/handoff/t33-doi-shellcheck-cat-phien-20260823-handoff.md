# Bàn giao — `T33-DOI-SHELLCHECK` (#249), **cắt phiên TRƯỚC khi cấp lease**

Phiên này **soạn đặc tả**. Nó **KHÔNG** cấp lease và **KHÔNG** thi công. Người giữ kho chốt in-session
23-08-2026: *"đi tiếp, nhưng **cắt phiên trước khi cấp lease**"* — một phiên KHÁC thẩm định độc lập
`r2`/`r3` rồi mới cấp.

Tệp này là đầu vào cho phiên ấy. **Đừng đọc nó thay cho đặc tả** — nó chỉ trỏ đường và khai chỗ yếu.

---

## Neo — đọc bằng BĂM, không bằng tên nhánh

Tên nhánh trôi và bị xoá; băm thì không. Tìm ở `master` trước; chưa thấy thì fetch nhánh
`claude/spec-freeze-n3-n1-269-gw47hw`.

| thứ | băm / SHA |
|---|---|
| `ops/specs/t33-doi-shellcheck.md` (r1) | `1405d390ca9376725517d01ef5b8d1abffd6a09d78d2b7206c2f068e7711f4da` |
| `ops/specs/t33-doi-shellcheck-r2.md` | `b9620d17b86f503b12d93359fb6d3423d29c034c29ab372f40cc5d7089b40e71` |
| `ops/specs/t33-doi-shellcheck-r3.md` | `9d55174de5f54bbf6089c179bf54e3b7f0b0c8174a02ab558f99c3df8583667d` |
| lease đã soạn, **CHƯA ĐẨY** | `ops/leases/t33-doi-shellcheck-exec-1-claude-20260823.yaml`, nhánh `ops/cap-lease-t33-doi-shellcheck`, 3 commit trên `origin/master` |
| `base_sha` lease neo | `5561b6b497989447f9185b26abb1bba154564967` |
| PR đặc tả | **#288**, head `f9dae732d8f1c822e33942aa734c0e6798449175` |

**Cả ba bản đặc tả còn hiệu lực.** `r2` và `r3` là **delta**; thứ chúng không nêu thì bản trước
nguyên hiệu lực. `r1` không bị sửa một chữ.

**Băm `r3` đã đổi HAI lần trong lúc review** — `6df98f39…` → `564dc8e1…` → `9d55174d…`. Hai bản đầu đã
khai tử. Nếu bạn đọc một tài liệu nào nhắc băm cũ, tài liệu ấy cũ.

---

## Việc của phiên nhận bàn giao

**Đúng ba việc, theo thứ tự. Việc 1 là lý do phiên bạn tồn tại.**

### 1 · Thẩm định ĐỘC LẬP `r2`/`r3` — đừng nhận lời khai của phiên soạn

Đây là điều người giữ kho mua bằng một lượt phiên. Phiên soạn (`claude`, phiên này) đã **tự viết và
tự chạy** ca `t98`, rồi **tự thẩm định** bảng số của chính nó — và đúng lớp lỗi ấy đã lọt **hai lần**
trong một ngày (xem §`Vì sao có bước này`).

Tối thiểu phải tự **CHẠY**, không đọc:

```
git worktree add --detach <tam> 5561b6b4
# X1 = bo han menh de nen:
#   `if (nen or os.name) == "nt" and nhan and all(`  ->  `if nhan and all(`
# X2 = doi sang TEN TEP:
#   ...                                             ->  `if tep.name != "ops-publish-lease.yml" and nhan and all(`
# VA = chen ca t98 (chep NGUYEN VAN tu r3) ngay TRUOC `def main() -> int:`
```

Tám ô phải khớp **chính xác** bảng `nghiem_thu` của `r3`. Lệch bất kỳ số nào ⇒ **DỪNG**, báo số đo
được, **không sửa cho vừa**.

Cần `actionlint 1.7.7` (`AL_VER=1.7.7 bash ops/cai_actionlint.sh`) **và** `shellcheck` — thiếu
`actionlint` thì `t33` ĐỎ sẵn trên nền, không phải hồi quy.

### 2 · Nếu thẩm định sạch: cấp lease

Lease đã soạn xong và **qua cổng** (`python3 ops/lease_publish.py check <lease>` ⇒ `rc=0` ĐĂNG ĐƯỢC).
Trước khi đẩy, làm **ba** việc, không bỏ việc nào:

1. **Đo lại `base_sha`.** master đi **27 commit trong 1,5 giờ** ngày 23-08. Nếu master đã đi tiếp thì
   `base_sha`/`reviewed_sha_required` phải là HEAD lúc ấy **và bảng `nghiem_thu` phải đo lại** —
   `S8` neo đúng chỗ này.
2. **Đo lại write set** bằng `ops/lease_publish.py ai-dang-giu ops/lease_publish_test.py`, và **tự
   đo** phần khai từng lease đã tiêu. `r3` nói rõ: *"việc khai ấy phải do người cấp đo"*.
3. **Đọc `write_set_da_do_truoc_khi_cap` trong lease và tự quyết có đồng ý không.** Nó khai đây là
   **CHẤP NHẬN RỦI RO CÒN LẠI**, không phải rủi ro đã đo bằng không. Nếu bạn không đồng ý với cách
   khai ấy thì DỪNG, đừng sửa lời khai cho vừa.

Đẩy nhánh `ops/cap-lease-t33-doi-shellcheck` ⇒ workflow `ops-publish-lease.yml` đăng comment lease.
**Đẩy xong phải ĐO là workflow đã chạy** (`list_workflow_runs` lọc theo nhánh) — đừng suy từ việc
`git push` thành công; đã đo được là workflow có `paths:` **không chạy** ở lần đẩy tạo nhánh mới.

### 3 · Thi công: phiên `claude` MỚI, KHÁC cả phiên soạn LẪN phiên bạn

`ADR-0046` §3. Reviewer `codex`, sandbox riêng, **mirror git đầy đủ** — `#250` đo được: ba lượt chỉ có
tệp `.md` cho `4 → 11 → 2` finding và **không con số phân rã nào**; lượt thứ tư có năng lực đo ra
**ba** con số phân rã ngay lượt đầu.

---

## Vì sao có bước này — `S2` đã kêu, lần đầu tiên trong kho

Bộ đếm hình dạng **`A` = 8** (người giữ kho tăng từ 7, in-session 23-08). `S2` là điều kiện DỪNG đã
đăng ký, và nó kích hoạt vì cross-review `codex` trên PR #288 bắt một **lời khai rộng hơn phép đo nằm
trong chính đặc tả** — đặc tả vốn viết ra để chống đúng lớp lỗi đó.

**Câu hỏi kiến trúc `S2` đặt ra, chép nguyên để bạn không phải suy lại:**

> Ba biểu hiện gần nhất — `#270`, `P1` và `P2` của PR #288 — đều sinh trong artefact do **một phiên
> vừa soạn vừa tự thẩm định lời khai của chính nó**. `ADR-0046` §3 cắt phiên giữa *soạn spec* và *thi
> công*, nhưng **không** cắt giữa *soạn* và *tự thẩm định*.

Hai finding cụ thể, cả hai **tái hiện được trên chính tệp**, không cần đo mới:

| | finding | vì sao nó lọt |
|---|---|---|
| `P1` | Coi hiện vật **đã land** là bằng chứng lease **đã chấm dứt**. Bản đầu viết *"rủi ro đã đo được là bằng không"* | Thứ đo là *việc đã land*; thứ khai là *thẩm quyền đã chấm dứt*. **Hai mệnh đề khác nhau**, và chính `r3` tự bác ở hai chỗ khác trong cùng tệp |
| `P2` | Khai *"cả ba phép đo đều trôi"* trong khi bảng của chính nó, **cách 40 dòng**, nói `t33`/`t73`/`numstat` không đổi | Câu **tự nhất quán khi đọc** — có số, có đơn vị, tự giải thích. Chỉ phép đo mới thấy |

Đó là lý do việc 1 của bạn không phải nghi lễ.

---

## Đã làm — hiện vật, không phải lời hứa

| | |
|---|---|
| `r2` | gộp `N1` của `#269` vào packet `#249`; `N1` chiếu vào `ops/lease_publish_test.py` vốn ĐÃ trong write set ⇒ **không nới quyền ghi** |
| `r3` | đo lại toàn bộ trên `5561b6b4` sau khi `#275` merge; ma trận 8 ô; ghi `A = 8` + `S2` |
| lease | soạn đủ trường, `schema_version: 2`, cổng `rc=0`, **chưa đẩy** |
| PR #288 | mở, CI `gate (ubuntu-latest)` xanh trên `bd3ae2bc`; đã xin review lượt 2 trên `f9dae732` |
| 5 lease đã tiêu | đo **riêng từng cái** — `#238`/`#225`/`#255`/`#244` đều CLOSED, hiện vật trên master |

---

## Việc CHƯA làm, nói ra thay vì để bạn phát hiện

1. **`M4` KHÔNG CÓ CỔNG, và kho không có cơ chế canh docstring nào.** Tôi tìm: `t42` — ca mà docstring
   `t34` viện dẫn là *"canh docstring không trôi rộng"* — thật ra khớp **marker nợ ↔ sổ
   `ops/NO_KY_THUAT.md`** hai chiều, **không** đọc văn xuôi. Nên `W14` khai **KHÔNG ĐẠT** theo `L3`.
   Nếu bạn tìm thấy một cơ chế tôi sót thì lời khai ấy rộng hơn phép đo — đó là finding.
2. **Không đo được lease đã chấm dứt — trừ hết hạn.** Nợ `AG-T0-01B`. Muộn nhất của 5 lease:
   `2026-08-24T08:25:00Z`.
3. **Hành vi trên `windows-latest` THẬT: chưa đo.** Cả 8 ô chạy trên Linux. `B5` của `r1` là chỗ đo, và
   đường **chắc chắn** là `workflow_dispatch` trên đúng ref — gắn nhãn `windows` **không đủ** vì
   `ci.yml` khai `pull_request:` mà không khai `types:`.
4. **`M1`/`M2` chưa có số kích thước nào** ⇒ trần **120** là **ước lượng có neo**, không phải số đo.
5. **Issue độ phủ lint chưa mở.** Đo được: **3/5 workflow không cổng nào lint**
   (`ci.yml`, `launcher-windows.yml`, `ops-open-pr.yml`), và `ops-don-ref.yml` chỉ được
   `ops/don_ref_chot_test.sh:310` lint với `-shellcheck= -pyflakes=` — **tắt hẳn**, không chú thích
   nào giải thích. Ngoài phạm vi packet này vì chữa nó cần đụng một mẫu `case` **lọc tên ref**
   (đường an ninh) ở tệp ngoài write set.

---

## Hai lỗ hổng của CỔNG, gặp trong lúc làm — không thuộc packet này

Ghi vì chúng là hiện vật đo được, và vì cả hai cùng họ `write_set_khong_ai_cuong_che`.

1. **`lease_publish.py check` KHÔNG kiểm đặc tả có tồn tại không.** Đo: chạy nó trong một checkout
   **không hề có** `ops/specs/t33-doi-shellcheck-r3.md` ⇒ vẫn `rc=0` ĐĂNG ĐƯỢC. Cổng nhận **lời khai**
   về `spec_path`/`spec_sha256_required`, không đo.
2. **Bộ quét nháp tự viết là thứ nguy nhất.** Bộ quét lease đầu tiên của phiên này đọc trường
   `expires_at` (tên trong protocol §4:260) trong khi tệp lease thật dùng `lease_expires_at_utc` ⇒ trả
   **31/31 `KHÔNG_ĐO_ĐƯỢC`**. Ca chứng (hỏi một đường dẫn bịa ⇒ `0`) **vẫn qua**, nên nó không lộ ra.
   Hỏi bộ quét một ca biết trước đáp án là **cần nhưng chưa đủ**. Nay đã có `ai-dang-giu` — dùng nó,
   đừng tự viết lại.

---

## Bốn chỗ đáng đặt làm mục kiểm của prompt review

1. Ma trận 8 ô — **tự dựng `X1`/`X2`, tự chạy**. Hàng `X2` ⇒ `97/97 rc=0` là căn cứ của cả `M3`.
2. Phép `r4/Q8` — gỡ `@ca` của `t70` (ca **duy nhất** gọi thẳng `_ly_do_bo_qua_workflow`) rồi áp lại
   đột biến; **cả hai vẫn phải ĐỎ**.
3. Còn con số nào trong `r2`/`r3` **mâu thuẫn với bảng của chính nó** không — đó là lớp lỗi vừa lọt.
4. Còn chỗ nào **suy từ "đã land" sang "đã chấm dứt"** không, kể cả gián tiếp.

---

## Công cụ — đo trước, đừng suy từ tài liệu

```
python .claude/dev/launcher.py doctor          # do cong cu + KHA DUNG + bien moi truong
AL_VER=1.7.7 bash ops/cai_actionlint.sh        # /tmp/actionlint co the TON TAI ma khong phai thu muc
git fetch --unshallow origin '+refs/heads/*:refs/remotes/origin/*'   # neu kho nong
git ls-remote --heads origin | sed 's#.*refs/heads/##' | sort > /tmp/mc
git for-each-ref --format='%(refname:lstrip=3)' refs/remotes/origin | grep -v '^HEAD$' | sort > /tmp/cb
comm -23 /tmp/mc /tmp/cb                       # CO tren may chu, THIEU cuc bo -> MU, fail-close
```

`for-each-ref` đọc **bộ đệm cục bộ**, không hỏi máy chủ. Phép so hai nguồn phải là chốt **đầu tiên**
trước khi mở tệp lease nào — và **so bằng TẬP TÊN, không bằng `wc -l`**.
