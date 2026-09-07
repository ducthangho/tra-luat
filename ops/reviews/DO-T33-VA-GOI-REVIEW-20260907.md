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
| P1 lượt 12 `mirror-thieu-ref-khong-du-do-a9` | gói chỉ mang 3 tên nhánh | `clone` mặc định; `ai-dang-giu` **chỉ quét `refs/heads/*`** nên remote-tracking ref không được đếm |
| P3 lượt 13 `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu` | `EVIDENCE.md` không khai cách trích số và phần bỏ sót | viết tay mỗi lượt |
| `t33` không đo được | container thiếu `actionlint` | không có bước cài công cụ trước khi đo |

Script làm cả ba: clone mirror **đủ mọi ref**, **vật chất hoá** từng nhánh thành `refs/heads/*`,
cài công cụ bắt buộc bằng bản ghim của kho, sinh `EVIDENCE.md` **tự khai cách trích và phần bỏ
sót**, rồi lập manifest.

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

## Điều bản ghi này KHÔNG chứng minh

- Không đóng gói lại các gói review CŨ. `ops/reviews/pr468-*` giữ nguyên như đã giao.
- Không chạm `ops/lease_publish.py`. Lỗ hổng `any(...)` trong `_kiem_bia_mo` **vẫn nguyên** và
  thuộc packet riêng đang chờ chủ kho cấp lease.
- Không đo được trạng thái CI của PR trên GitHub: bộ công cụ GitHub của phiên chỉ có **44 tool**,
  không có nhóm workflow/actions.
- Số ref **305** là mốc lúc `2026-09-07` và **đang tăng** — mỗi nhánh mới cắt từ `master` lại
  mang thêm một bản sao lease chưa bia mộ. Trước đó đo được 9, rồi 11, nay 305 ref tổng.
