verdict: changes_requested
reviewed_sha: babceec2399169f968664b82c096b41b8b8db78b
packet: LEASE-HOI-TOAN-KHO (#244), PR #275, lease r2/r3 (`lease-hoi-toan-kho-exec-1r2-codex-20260823` →
`lease-hoi-toan-kho-exec-1r3-codex-20260823`)
reviewer: claude (cross-review lượt 2, nền khác executor `codex`)

## ĐỐI CHIẾU LƯỢT TRƯỚC

- **git-wrapper-nuot-loi-fail-open (P1)**: **ĐÃ VÁ THẬT** — chạy `ops/lease_publish_test.py` trên mã
  gốc (`reviewed_sha`) → `95/96` (chỉ `t33` đỏ, thiếu `actionlint`). Áp lại ĐÚNG đột biến lượt 1 nêu
  (`_git()`: `if p.returncode != 0: raise Chan(...)` → `return ""`) vào bản sao sandbox
  (`work/tree_mut_p1`) → `94/96`, đỏ THÊM đúng một ca: `t95_git_that_bai_phai_fail_close_khong_duoc_nuot_loi`,
  thông điệp `"t95: _git() coi rc != 0 là thành công (trả chuỗi thay vì Chan)"` — nói ĐÚNG lỗ nó hứa
  bịt, không phải đỏ vì lý do khác ⇒ không phải vá hờ. Hỏi ngược thêm: đổi tên `_git`→`_git2` toàn bộ
  tệp (mọi lời gọi lẫn định nghĩa) → `t95` đỏ với `AttributeError: ... has no attribute '_git'`, tức
  đứt LỚN chứ không xanh giả — `t95` thật sự đi qua `_git()` thật của module vừa nạp lại (`_nap_cong()`
  nạp module MỚI mỗi lần, và `_git.__globals__` chính là `__dict__` của module đó nên `mod.GOI_GIT = …`
  chạm đúng biến toàn cục mà `_git()` tra), không phải một bản sao chết.

- **lease-cham-duong-so-chua-thay-vi-so-bang (P2)**: **ĐÃ VÁ THẬT** — mã gốc `95/96`. Áp đột biến
  lượt 1 nêu (`==` → `duong in x`) vào bản sao sandbox (`work/tree_mut_p2`) → `94/96`, đỏ thêm đúng
  `t96_lease_cham_duong_khop_tuyet_doi_khong_phai_chua`, thông điệp `"write_set dài hơn nhận duong làm
  tiền tố vẫn bị coi là khớp"` — đúng nội dung lỗ. Hỏi ngược: `grep _lease_cham_duong` trong
  `ops/lease_publish.py` chỉ có **một** điểm gọi (`lenh_ai_dang_giu`, dòng 678) — không có đường gọi
  thứ hai bỏ qua hàm này để `t96` (đo hàm con trực tiếp) có thể bị mù; không cần thêm ca tích hợp
  qua `ai-dang-giu` để đóng lỗ này.

- **bien-het-han-khong-co-ca (P3, `_phan_loai_lease` biên `<=`/`<`)**: **CHƯA VÁ** — đúng như lượt 1 tự
  khai ("ĐÃ THỬ VÁ: không"). Xác nhận diff của lượt vá này (`diff.patch`, byte-khớp
  `git diff 13e3a9c babceec`) CHỈ thêm `t95`/`t96`, không đụng `_phan_loai_lease`. Áp lại đột biến
  `<=`→`<` vào bản sao (`work/verify_p3_boundary`, đã có `t95`/`t96`) → `94/96`, không ca nào đỏ mới
  (chỉ tác dụng phụ tự-neo của `t94`, y hệt lượt 1 đã ghi) ⇒ vẫn sống sót, đúng khai báo. Chấp nhận
  được ở mức "chưa vá" vì lượt 1 tự đánh giá độ tin "vừa" và rủi ro thực tế gần bằng không; không nâng
  cấp thành blocker.

**Phát hiện MỚI ngoài ba mục trên — xem mục cuối `## BẢNG ĐỘT BIẾN` và finding
`kiem-dau-toan-kho-bo-qua-git-loi-that`: đây KHÔNG phải lỗ coverage như P1/P2, mà là một lỗi hành vi
ĐANG SỐNG trong `ops/lease_publish.py` tại `reviewed_sha`, không cần đột biến gì để lộ ra.**

## BẢNG ĐO

| khẳng định | EVIDENCE khai | đo được | khớp? |
|---|---|---|---|
| `reviewed_sha` | `babceec239916…` | `git -C cay-kho rev-parse HEAD` → `babceec2399169f968664b82c096b41b8b8db78b` | ✅ |
| head lượt 1 | `13e3a9c…` | `git log --oneline -5` → `babceec` có cha đúng `13e3a9c` | ✅ |
| `ops/lease_publish_test.py` (nền/sandbox) | `95/96` / `95/96` | chạy trong `cay-kho` → `95/96 đạt; đã chạy=96, bỏ qua=0`, đỏ duy nhất `t33` | ✅ (chỉ đo được MỘT bản trong sandbox; không có bản "nền" độc lập thứ hai để đối chiếu chéo — ghi nhận giới hạn, không phải lệch) |
| `doc-claims-check --strict` | `rc=0` | `python3 scripts/tl.py doc-claims-check --strict` → `"ok": true`, `rc=0` | ✅ |
| đột biến P1 → `94/96`, đỏ `t33`+`t95` | khai đúng | tự dựng lại đột biến, chạy → `94/96`, đỏ đúng `t33`+`t95`, thông điệp đúng nội dung | ✅ |
| đột biến P2 → `94/96`, đỏ `t33`+`t96` | khai đúng | tự dựng lại đột biến, chạy → `94/96`, đỏ đúng `t33`+`t96`, thông điệp đúng nội dung | ✅ |
| ngân sách: 2 tệp / 337 dòng thêm | khai đúng | `git diff --numstat 8222c101 babceec` → `ops/lease_publish.py +151`, `ops/lease_publish_test.py +186` = **337**, 2 tệp — khớp TỪNG SỐ | ✅ |
| trần ngoại lệ ADR-0044 (≤3 tệp/≤380 dòng) | không vượt | 2 ≤ 3, 337 ≤ 380 | ✅ trong trần |
| `write_set` (LEASE.yaml) = diff thật | `ops/lease_publish.py`, `ops/lease_publish_test.py` | hai tệp trong `git diff 8222c101 babceec --stat` đúng bằng hai đường trong `write_set`, không thừa | ✅ |
| nội dung `diff.patch` = diff lượt vá (13e3a9c→babceec) | (đại diện) | `diff diff.patch <(git diff 13e3a9c babceec)` → rỗng, byte-khớp | ✅ |
| sha256 `SPEC.md` | `ffca019e…5da87` | `sha256sum SPEC.md` → khớp từng ký tự | ✅ |
| `git rev-parse --is-shallow-repository` | `false` | đo trong `cay-kho` → `false` | ✅ |
| Ref 182/182, `comm` hai chiều rỗng | đo trên sandbox mirror | `ls-remote --heads origin` = 182, `for-each-ref origin` (loại HEAD) = 182, `diff` hai tập → rỗng — **nhưng đây là mirror cục bộ (`kho.git`) do sandbox tự tạo, KHÔNG phải phép đo trên kho nguồn GitHub trước khi clone mà EVIDENCE nói tới** | ⚠️ tự nhất quán (182/182) nhưng KHÔNG tái lập được đúng phép đo đã khai — EVIDENCE tự khai đúng giới hạn này ("KHÔNG ĐO ĐƯỢC từ sandbox"), không phải một chỗ hổng mới |

## BẢNG ĐỘT BIẾN

| đột biến | ca đáng lẽ đỏ | kết quả trên 96/97 ca | sống sót? |
|---|---|---|---|
| `_git()`: `rc!=0` → `return ""` thay vì `raise Chan` | `t95` | `94/96`, đỏ đúng `t95` | bị giết |
| `_lease_cham_duong`: `duong in x` thay `x == duong` | `t96` | `94/96`, đỏ đúng `t96` | bị giết |
| Đổi tên `_git`→`_git2` toàn tệp (kiểm `t95` không xanh giả) | `t95` (phải đỏ dạng khác — lỗi nạp, không phải xanh) | `93/96`, `t95` đỏ bằng `AttributeError` | bị giết (đúng cách — không xanh giả) |
| `_phan_loai_lease`: biên `han <= bay_gio` → `han < bay_gio` | (không có — P3 cũ) | `94/96`, không ca nào mới đỏ | **SỐNG SÓT** — đã biết từ lượt 1, CHƯA VÁ |
| `_quet_lease_toan_kho`: khoá dedup `(blob, duong)` → chỉ `blob` | (không có) | `95/96`, không ca nào đỏ | **SỐNG SÓT**, nhưng KHÔNG nâng thành finding: hai lease khác nhau trùng `blob` nghĩa là NỘI DUNG YAML byte-giống-hệt (blob = hash nội dung), mà lease luôn mang `lease_id`/timestamp riêng ⇒ xác suất thực tế ~0; ghi nhận minh bạch, không phải bug đáng vá |
| **`_kiem_dau_toan_kho`: `GOI_GIT("rev-parse","--git-dir")` trả `rc=128` (git lỗi thật, `.git/` đã xác nhận có mặt)** | (không có ca nào — đây là lỗ **THẬT**, không cần đột biến để lộ) | chạy TRỰC TIẾP trên `ops/lease_publish.py` KHÔNG SỬA GÌ (`reviewed_sha`) → không ném `Chan`, hàm `return None` lặng lẽ | **KHÔNG PHẢI "SỐNG SÓT SAU ĐỘT BIẾN" — ĐÂY LÀ HÀNH VI THẬT CỦA MÃ HÔM NAY**, xem finding bên dưới |

### kiem-dau-toan-kho-bo-qua-git-loi-that  [P1]  `_kiem_dau_toan_kho` gọi thẳng `GOI_GIT`, bỏ qua `_git()`, và fail-OPEN khi git lỗi thật — LỖI ĐANG SỐNG, không phải đột biến giả định

TỆP/DÒNG: `ops/lease_publish.py:496-519` (hàm `_kiem_dau_toan_kho`, cụ thể khối 506-511)

VẤN ĐỀ: Verdict lượt 1 khẳng định *"Toàn bộ M1/M2/M3 … đi qua đúng MỘT điểm gọi git: `_git()`"* —
khẳng định đó **SAI**. `_kiem_dau_toan_kho` (một phần của M3, do CHÍNH packet này thêm vào giữa
`base_sha` và `13e3a9c` — xem `git diff 8222c101 babceec -- ops/lease_publish.py`, hunk thêm hàm này)
gọi thẳng `GOI_GIT("rev-parse", "--git-dir", cwd=root)`, **không** đi qua `_git()`:

```python
if not (root / ".git").exists():
    return                              # (1) hợp lệ: không phải kho — bỏ qua fixture
try:
    Path(tep).resolve().relative_to(root)
except ValueError:
    return                              # (2) hợp lệ: bản sao rời
try:
    p = GOI_GIT("rev-parse", "--git-dir", cwd=root)
except OSError:
    return                              # (3) KHÔNG hợp lệ — .git ĐÃ xác nhận có ở (1)
if p.returncode != 0:
    return                              # (4) KHÔNG hợp lệ — cùng lý do
```

Nhánh (1)/(2) là bỏ qua CÓ CHỦ Ý (fixture/bản sao rời — đúng như comment tại chỗ và đúng tinh thần
`t93`/A7). Nhưng tới nhánh (3)/(4), `.git/` **đã được xác nhận tồn tại** ở nhánh (1); một lệnh `git`
thất bại ở đây (binary lỗi, quyền tệp, đĩa hỏng, `.git` là worktree/submodule pointer bất thường…)
**không còn là "không phải kho"** — nó là **git LỖI THẬT**, đúng "trạng thái thứ ba"
(`KHÔNG_XÁC_ĐỊNH`) mà toàn bộ packet này sinh ra để cưỡng chế. Hàm `return` lặng lẽ thay vì
`raise Chan(RC_KHONG_XAC_DINH, …)`.

Hậu quả không phải lý thuyết: `_kiem_dau_toan_kho` được gọi ở **đầu** `kiem()` (dòng 535, TRƯỚC cả
kiểm trường bắt buộc) — và `kiem()` là cổng mà `lenh_check`/`lenh_body`/`lenh_kiem_github` (tức lệnh
`check`/`body`/`kiem-github` mà `.github/workflows/ops-publish-lease.yml` gọi trước khi đăng comment
lease thật lên PR/Issue) đều đi qua. Đây CHÍNH XÁC là "cổng đăng lease" mà `CLAUDE.md` liệt hẳn một
mục dài (`LEASE-DANG review 5`, `rc=6 bị bỏ qua im lặng` = fail-open thật) và LEASE.yaml của packet
này còn trích lại nguyên văn cảnh báo đó (`canh_bao_cho_nguoi_thi_hanh`). Khi git tạm lỗi giữa lúc
CI chạy, `_kiem_dau_toan_kho` không ném lỗi — nó chỉ IM LẶNG bỏ qua chốt "lease này đã đăng rồi",
để `kiem()` đi tiếp như chưa có gì, mở đường đăng TRÙNG một lease đã đăng (đúng loại sự cố mà `A7`/
`t93` được viết ra để chặn, chỉ khác là bây giờ nó bị vòng qua bởi một điều kiện tiên quyết fail-open).

Đây KHÔNG phải "thiếu ca test cho mã đúng" như P1/P2 của lượt 1 — mã HIỆN TẠI đã sai. Chạy thẳng
(không đột biến gì) trên `ops/lease_publish.py` tại `reviewed_sha`:

```
mod.GOI_GIT = <hàm giả trả CompletedProcess(rc=128)>
mod._kiem_dau_toan_kho({"lease_id": "DUNG"}, <tệp trong kho fixture có .git/>, <root>)
→ trả None, KHÔNG ném Chan   # đã chạy thật, xem work/tree_t97probe
```

ĐÃ THỬ VÁ: có — patch tại `goi-va/ops/lease_publish.py`. Thay khối (3)/(4) bằng một lời gọi `_git(root,
"rev-parse", "--git-dir")` (bỏ hẳn `try/except OSError` và kiểm `returncode` tay), tận dụng đúng
`_git()` mà P1 vừa khoá chặt — nhất quán với phần còn lại của M1/M2/M3, không thêm đường fail-close
thứ hai để rồi lại trôi lệch với đường thứ nhất.

ĐÃ THỬ NGHIỆM (chạy thật, không suy diễn — cả hai chiều trong `work/verify_t97_unpatched` và
`work/verify_t97_patched`):
1. Thêm ca `t97_kiem_dau_toan_kho_phai_fail_close_khi_git_that_bai` (đặt tại
   `goi-va/ops/lease_publish_test.py`) vào **`ops/lease_publish.py` CHƯA SỬA** (nguyên trạng
   `reviewed_sha`) → `95/97 đạt`, đỏ đúng `t33` + `t97` (thông điệp đúng: *"coi git lỗi thật … là
   'không phải kho' và bỏ qua lặng lẽ"*) — xác nhận lỗ CÓ THẬT trên chính commit đang xét, không phải
   dựng chuyện.
2. Áp patch gợi ý (`goi-va/ops/lease_publish.py`) + ca `t97` → `96/97 đạt`, chỉ còn `t33` đỏ (thiếu
   `actionlint`, không liên quan) — vá xong không sinh hồi quy: `t94` vẫn báo `đột biến mã sản phẩm:
   đã chạy=10, bị giết=10` (không anchor nào của `t94` chạm vùng vừa sửa).
3. Đối chứng âm: patch KHÔNG đổi hành vi khi `.git/` thật sự không tồn tại (nhánh (1) vẫn `return`
   sớm, không đụng `_git()`) — không phá vỡ đường fixture hợp lệ mà `t93` đang dùng; `t93` vẫn xanh
   sau patch (nằm trong `96/97`).

ĐỘ TIN: cao — không phải suy luận từ đột biến giả định, mà đo trực tiếp hành vi CÓ THẬT của mã tại
`reviewed_sha`, patch đối chứng cả hai chiều (trước/sau, cộng một ca âm cho nhánh hợp lệ).

**Vì sao đây là `changes_requested`, không phải điểm cộng cho lượt sau:** lease hiện tại
(`viec_cua_luot_nay` trong `LEASE.yaml`) khoanh rõ *"CHỈ áp gói vá của cross-review lượt 1 … KHÔNG
sửa mã sản phẩm"* — đúng cho P1/P2 vì mã ở đó ĐÚNG. Nhưng finding này đòi sửa **mã sản phẩm thật**
(`_kiem_dau_toan_kho`), không thể đóng chỉ bằng thêm test — nằm ngoài đúng ranh giới mà lượt này tự
đặt ra cho chính nó. Không có tầng nào cưỡng chế ranh giới đó (cùng họ `write_set_khong_ai_cuong_che`
đã ghi trong `LEASE.yaml`), nên đây là chỗ phải DỪNG và xin vòng/lease kế tiếp cho phép sửa mã sản
phẩm, đúng điều kiện dừng *"Ngoài `write_set` … DỪNG"* được viết rộng ra thành *"ngoài phạm vi lượt
này đã tự khai … DỪNG"*.

## Phạm vi / ngân sách

Diff của lượt này (`13e3a9c` → `babceec`) chỉ chạm `ops/lease_publish_test.py`, nằm trong `write_set`.
Tổng diff (`base_sha` → `reviewed_sha`): 2 tệp, 337 dòng thêm — trong trần ĐÃ NỚI (3 tệp/380 dòng).
Không tệp nào khác bị chạm. Không vi phạm phạm vi.

## Điều kiện dừng chưa thoả

`LEASE.yaml.ngoai_le_ADR_0045.ba_dieu_kien_ADR_0045.human_readback_truoc_land` vẫn ghi **BẮT BUỘC —
CHƯA làm**. Không đổi bởi verdict này: dù kết luận gì, packet KHÔNG được land tới khi chủ kho tự đọc
lại diff.

## Kết luận

Hai finding P1/P2 của lượt 1 đã được vá THẬT — cả hai đã tự chạy đột biến gốc, hai ca mới (`t95`,
`t96`) đỏ đúng lý do, và một phép hỏi-ngược (đổi tên `_git`) xác nhận `t95` không xanh giả. Phạm vi
và ngân sách đúng cam kết. Nhưng trong lúc đột biến lại toàn bộ A1–A8 và dò các đường gọi git khác
(đúng nhiệm vụ 4 của prompt), phát hiện một lỗi HÀNH VI ĐANG SỐNG — không phải lỗ coverage — tại
`_kiem_dau_toan_kho`: nó bỏ qua `_git()` mà P1 vừa khoá, và fail-open khi `git rev-parse --git-dir`
thất bại thật sự trên một kho `.git/` đã xác nhận tồn tại, nằm ngay trên đường "cổng đăng lease" mà
lịch sử kho này (`LEASE-DANG` review 5, trích lại trong chính `LEASE.yaml` của packet) đã trả giá cho
đúng hình dạng lỗi này. Không có ca nào trong 96 ca hiện có chạm tới nhánh đó — ca `t97` (mới, tại
`goi-va/ops/lease_publish_test.py`) đỏ ngay trên `reviewed_sha` không cần đột biến gì, và xanh sau
patch gợi ý (`goi-va/ops/lease_publish.py`) không sinh hồi quy.

Vì đây là sửa MÃ SẢN PHẨM, nằm ngoài ranh giới lượt này tự đặt ("chỉ vá test, không sửa sản phẩm"),
đề nghị `changes_requested`: xin lease/vòng kế tiếp áp patch `_kiem_dau_toan_kho` (gợi ý sẵn tại
`goi-va/`), rồi review lại toàn bộ diff mới (vì lần này có đụng sản phẩm, verdict lượt 1 hết hiệu lực
với head mới, đúng quy tắc đã ghi trong chính `LEASE.yaml` của packet: *"Sửa mã sản phẩm sẽ làm
verdict lượt 1 hết hiệu lực với head mới"*).
