# ĐO t33 SAU KHI CÀI actionlint, và vá tận gốc việc dựng gói review

Ngày `2026-09-07`. Vá hai nợ còn lại sau khi PR #468 đạt verdict `approve`.

## 1. `t33_workflow_dang_lease_phai_qua_actionlint` — nay ĐÃ ĐO

Full-gate ngày `2026-09-07` cho `lease rc=1` ở **cả hai vế**. Tôi đã ghi đúng rằng đó là
fail-close chứ không phải hồi quy, nhưng phải nói thêm một điều quan trọng: **ca `t33` khi ấy
không đỏ, cũng không xanh — nó KHÔNG CHẠY.**

`ops/lease_publish_test.py:1338` nói rõ chủ ý: *"`actionlint` phải XANH … và THIẾU công cụ là
ĐỎ."* Vậy `rc=1` là hành vi ĐÚNG, không phải lỗi mã. Cách đóng là **cài công cụ rồi đo**, không
phải nới phép kiểm.

Đã cài bằng **script ghim sẵn của kho** `ops/cai_actionlint.sh` (`AL_VER=1.7.7`, đúng bản CI ghim
ở `.github/workflows/ci.yml:97`), có đối chiếu băm — `rc=0`.

> Tự khai: lần đầu tôi cài bằng `curl` tuỳ tiện, **không đối chiếu băm**. Đó đúng thứ kỷ luật của
> kho này bác bỏ. Đã gỡ bản ấy và cài lại bằng script của kho trước khi đo.

Đo lại bộ `lease` trên **cả hai vế** của full-gate:

| vế | sha | rc | kết quả |
|---|---|---:|---|
| nền | `b416830` | **0** | `121/121 đạt; đã chạy=121, bỏ qua=0` |
| sau | `f77f198` | **0** | `121/121 đạt; đã chạy=121, bỏ qua=0` |

`out` = 8649 B ở cả hai vế. **DELTA vẫn 0**, và `rc=1` cuối cùng của full-gate đã biến mất.
Trước: 120/121, `rc=1`. Nay: **121/121, `rc=0`**.

CI **đã** cài `actionlint` từ trước (`ci.yml:98`, `duyet-phan-chung.yml:54`,
`ops-publish-lease.yml`). Nên đây chưa bao giờ là lỗ hổng của kho — chỉ là container chạy gate
thiếu công cụ. Nợ nằm ở chỗ dựng môi trường đo, và mục 2 vá đúng chỗ đó.

## 2. `ops/dung_goi_review.sh` — vá tận gốc, không vá triệu chứng

Ba lỗi liên tiếp có **cùng một gốc**: việc dựng gói hiện vật cho reviewer nằm rải rác trong
scratchpad từng phiên, không phải một thứ chạy được trong kho.

| lỗi | biểu hiện | gốc |
|---|---|---|
| P1 lượt 12 `mirror-thieu-ref-khong-du-do-a9` | gói chỉ mang 3 tên nhánh | kiểu clone (bare/hẹp) — xem ĐÍNH CHÍNH bên dưới |
| P3 lượt 13 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu` | `EVIDENCE.md` không khai cách trích số và phần bỏ sót | viết tay mỗi lượt |
| `t33` không đo được | container thiếu `actionlint` | không có bước cài công cụ trước khi đo |

Script làm cả ba: clone mirror **đủ mọi ref**, **vật chất hoá** từng nhánh thành `refs/heads/*`,
cài công cụ bắt buộc bằng bản ghim của kho, sinh `EVIDENCE.md` **tự khai cách trích và phần bỏ
sót**, rồi lập manifest.

### ĐÍNH CHÍNH — chẩn đoán gốc ban đầu của tôi SAI

Bản đầu của tài liệu này (và các báo cáo tôi gửi chủ kho) viết:

> `ai-dang-giu` **chỉ quét `refs/heads/*`**, nên remote-tracking ref không được đếm.

**Sai.** Cross-review PR #477 (P3 `chan-doan-ai-dang-giu-chi-heads-khong-dung`) bắt được, và tôi
đã đọc lại mã để xác nhận:

- `_cac_ref_cuc_bo` (`ops/lease_publish.py:307–321`) chạy
  `for-each-ref refs/heads refs/remotes` — **đọc CẢ HAI** — và tính tên nhánh từ cả
  `refs/remotes/origin/*`.
- `_quet_lease_toan_kho` đọc trọn danh sách ấy.

Tôi tin **banner của CLI** (`ops/lease_publish.py:937` in `PHẠM_VI: quét refs/heads/*`) thay vì đọc
mã. Banner không phản ánh hết hành vi.

Hệ quả: nguyên nhân THẬT của gói 3 ref ở lượt 12 là **kiểu clone** (`clone --bare --no-local`
theo ghi nhận lượt 12), không phải phạm vi quét.

Bước vật chất hoá `refs/heads/*` trong script **vẫn giữ**, nhưng vì lý do KHÁC với lý do tôi
nêu ban đầu: để gói không phụ thuộc tên remote, và để đối chiếu tập tên trực tiếp.

### Bằng chứng đã đo, không phải mô tả

Chạy thật trên kho này:

```
$ bash ops/dung_goi_review.sh <goi> $(git rev-parse origin/master)
ref: nguon=305 mirror=305 cay-kho=305; lech=0/0
GOI DU DE TAI DO: 305/305/305 ref, 0 lech
rc=0
```

- `cay-kho` có **305** `refs/heads`, `origin` = URL thật, HEAD = `b416830`.
- manifest `sha256sum -c` ⇒ **`rc=0`, 2131/2131**.
- `shellcheck` ⇒ **`rc=0`** (cài bằng `ops/cai_cong_cu.sh shellcheck`; thiếu nó thì
  `actionlint` bỏ luật `SC*` trong im lặng).

### Cổng fail-close — đã chứng minh CHẶN, không chỉ chứng minh đường xanh

| ca | mong đợi | đo được |
|---|---:|---|
| thiếu tham số | `rc=2` | **`rc=2`** |
| `--single-branch` thay `--mirror` | `rc=6` | **`rc=6`** — `nguon=305 mirror=1 cay-kho=1; lech=304/304` |

Ca thứ hai tái hiện **đúng lỗi lịch sử** đã sinh ra P1 lượt 12: nếu ai đó dựng gói bằng clone
một nhánh, script chặn ngay thay vì giao một gói mà reviewer không tái đo được.

### Log gốc của phép đo t33

Cross-review PR #477 (P3 `so-do-lich-su-thieu-hien-vat-tai-tinh`) chỉ ra đúng: bản đầu khai
`121/121` và `DELTA=0` mà **không kèm log**, nên đó chỉ là lời khai. Nay đính kèm ở
`ops/reviews/log-t33-20260907/`:

| tệp | nội dung |
|---|---|
| `nen.lease-sau-cai-actionlint.out` / `.err` | stdout/stderr vế nền `b416830`, 8649 B |
| `sau.lease-sau-cai-actionlint.out` / `.err` | stdout/stderr vế sau `f77f198`, 8649 B |
| `moi-truong-va-rc.txt` | lệnh, hai SHA đầy đủ, `rc` hai vế, bản `actionlint`/`shellcheck`, cách cài |

Hai stdout khác nhau **32 dòng** trước chuẩn hoá; sau khi chuẩn hoá tên thư mục tạm ngẫu nhiên
(`sed -E 's/lp_[a-z0-9_]+/LP/g'`) thì **giống hệt, 49/49 dòng**.

Vẫn chưa kiểm lại được, ghi rõ: TSV và manifest của lần đo `305`/`2131` **không còn** — chúng ở
thư mục tạm đã bị ghi đè bởi các lần chạy sau. Hai số ấy là **lời khai của executor, gói này
không đủ để kiểm lại**. Số ref đo lại lúc dựng gói #477 là **306**, mốc khác, không thay số cũ.

## Điều bản ghi này KHÔNG chứng minh

- Không đóng gói lại các gói review CŨ. `ops/reviews/pr468-*` giữ nguyên như đã giao.
- Không chạm `ops/lease_publish.py`. Lỗ hổng `any(...)` trong `_kiem_bia_mo` **vẫn nguyên** và
  thuộc packet riêng đang chờ chủ kho cấp lease.
- Không đo được trạng thái CI của PR trên GitHub: bộ công cụ GitHub của phiên chỉ có **44 tool**,
  không có nhóm workflow/actions.
- Số ref **305** là mốc lúc `2026-09-07` và **đang tăng** — mỗi nhánh mới cắt từ `master` lại
  mang thêm một bản sao lease chưa bia mộ. Trước đó đo được 9, rồi 11, nay 305 ref tổng.

## Cross-review PR #477 bắt được 1 P1 + 3 P2 trong chính script này

Script tự nhận là "vá gốc" nhưng chứa đúng phản mẫu mà kho đã ghi thành luật. Đã vá và tự dựng
lại từng phản chứng:

| finding | mức | lỗi | sau khi vá |
|---|---|---|---|
| `actionlint-co-mat-khong-phai-dung-ban` | **P1** | `if ! command -v actionlint` bỏ qua installer ghim — trái `ops/cai_actionlint.sh:14` *"co mat != dung ban"*; rc trong đối số `printf` không làm `set -e` kích hoạt | luôn gọi installer ghim; bắt `rc` bằng assignment |
| `shellcheck-thieu-van-giao-goi-xanh` | P2 | chỉ ghi `THIEU` rồi đi tiếp, dù thiếu nó thì `actionlint` bỏ luật `SC*` trong im lặng | shellcheck vào danh sách BẮT BUỘC ⇒ `loi 4` |
| `remote-doi-ten-loi-van-khai-url-that` | P2 | hai `\|\| true` nuốt lỗi ⇒ `origin` trỏ sai mà vẫn `rc=0` | `\|\| loi 5` + đọc lại `origin` và đối chiếu |
| `manifest-loc-hau-to-bo-sot-tep-con` | P2 | `grep -v '  \./ARTIFACTS\.sha256$'` chỉ neo cuối dòng ⇒ thư mục tên `nested  .` làm tệp con bị loại | `find ... ! -path './ARTIFACTS.sha256'` |

Phản chứng tự đo sau khi vá:

| ca | mong đợi | đo được |
|---|---|---|
| `AL_VER=` (rỗng) | chặn | **`rc=4`** — *"AL_VER được đặt nhưng RỖNG"* |
| `AL_VER=1x.2y.3z` | chặn | **`rc=4`** — installer từ chối |
| thiếu `shellcheck` (PATH đầy đủ, chỉ gỡ nó) | chặn | **`rc=4`** — *"thieu cong cu bat buoc: shellcheck"* |
| git template có sẵn remote `mirror-cuc-bo` | chặn | **`rc=5`** — *"khong doi ten duoc remote origin"* |
| thư mục `nested  .` | tệp con phải nằm trong manifest | có **1** dòng; sửa nội dung ⇒ `sha256sum -c` **`rc=1`**, `FAILED` đúng tệp ấy |
| `actionlint 0.0.0-GIA` thoát 42 ở ĐẦU PATH | không được tin PATH | **`rc=0`**, `cong-cu.txt` ghi bản **1.7.7** tại thư mục vừa cài — PATH bị bỏ qua |
| đường xanh | qua | **`rc=0`**, `306/306/306` ref, 0 lệch |

Ca cuối là bằng chứng trực tiếp cho P1: trước khi vá, nhánh `command -v` sẽ nhận bản giả rồi
báo gói "ĐỦ ĐỂ TÁI ĐO".
