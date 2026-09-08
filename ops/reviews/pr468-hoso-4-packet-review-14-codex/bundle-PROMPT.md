# Cross-review PR #468 — LƯỢT 14, `ducthangho/tra-luat`

Bạn là **reviewer khác nền** (executor Claude; bạn Codex).
`reviewed_sha` = `922956a7048fd23eea1c9f88aeb986e076f10e24` · lượt 13 review `f77f198`.
Diff `f77f198..922956a`: **72 tệp** (`numstat.txt`, `diff-sau-luot13.patch`).

Lượt 13 (`VERDICT-luot13.md`) ra **`approve` — 0 P1 · 0 P2 · 1 P3**. Nhưng nó review head CŨ.
Head hiện tại thêm ba nhóm hiện vật mà **chưa ai review**:

1. `ops/reviews/pr468-hoso-4-packet-review-13-codex*` — verdict + biên nhận + gói lượt 13
2. `ops/reviews/full-gate-pr468-20260907/` — bằng chứng full-gate chạy MỘT lần
3. hai dòng thêm vào `ops/reviews/README.md` và `GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md`

Toàn bộ nằm trong `ops/` — **không một dòng mã chạy được**. Xác minh điều đó trước, đừng nhận.

## NHIỆM VỤ 1 — P3 lượt 13 đã vá chưa?

`evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu` [P3]: bảng EVIDENCE không khai cách trích
số và phần bỏ sót. Executor nói đã áp cho `full-gate-pr468-20260907/README.md`. Kiểm: README ấy có
bảng "CÁCH TRÍCH SỐ" phân loại nguồn và mục "phần bỏ sót" không? Nó có ĐỦ, hay chỉ có hình thức?

## NHIỆM VỤ 2 — bằng chứng full-gate có TRUNG THỰC không?

`full-gate-pr468-20260907/` khai: nền `b416830` so sau `f77f198`, **DELTA=0**, và

| bộ | rc hai vế | out |
|---|---|---|
| `cidk` | 0/0 | 2934 B |
| `ploop` | 0/0 | 8752 B |
| `lease` | **1/1** | 8971 B |
| `doctrine-scan` | 0/0 | 69 B |
| `adr-song` | 0/0 | 113 B |
| `doc-claims-check` | 0/0 | 70861 B |

- Từ hiện vật trong gói, **tái tính** được bao nhiêu số trên? Cái nào chỉ là lời khai?
- `lease rc=1` được giải thích là thiếu `actionlint` ⇒ fail-close đúng, **không phải hồi quy**, và
  README ghi thẳng *"ca t33 CHƯA TỪNG ĐƯỢC ĐO"*. Lời khai ấy đúng hay đang che một lỗi thật?
- Hai tệp `*.lease.norm.out` đã **chuẩn hoá** tên thư mục tạm; bản thô KHÔNG kèm. Điều đó có làm
  phép so DELTA mất giá trị không?
- `cidk`/`ploop` chỉ giữ **5 dòng cuối**. Dòng lỗi giữa stdout sẽ không thấy. Có phải bỏ sót nguy hiểm?
- Executor tự khai *"không bộ nào `out=0B`"* là phép kiểm chống xanh giả. Kiểm lại khẳng định ấy.

## NHIỆM VỤ 3 — manifest, và một cái bẫy đã bắt được executor

Gói lượt 13 và full-gate đều có `ARTIFACTS.sha256`. Nhưng manifest của các gói review ghi
**bố cục sandbox** (`VERDICT.md`, `do-review13/...`), không phải bố cục trong kho; ánh xạ khai ở
`DOC-MANIFEST.md`.

Executor đã một lần chạy `sha256sum -c` từ thư mục manifest và thấy **4 gói `OK=0/N`**, suýt báo
kho hỏng, rồi tự phát hiện phép kiểm của mình sai chứ kho không hỏng.

- Kiểm lại cho ĐÚNG: theo ánh xạ `DOC-MANIFEST.md`, **mọi** manifest trong `ops/reviews/**` có
  `rc=0` không? Nêu số `N/N` cho từng gói.
- `DOC-MANIFEST.md` của gói 13 có khai ĐỦ ánh xạ không, hay còn tệp không nói tới?
- Có tệp nào trong gói **không** nằm trong manifest không?

## NHIỆM VỤ 4 — biên nhận lượt 13

`pr468-hoso-4-packet-review-13-codex-verdict.receipt.yaml`: đối chiếu `verdict_sha256`,
`verdict_bytes`, `reviewed_sha`, `thoi_luong_giay`, `ma_thoat`, `so_lan_chet_truoc_khi_xong` với
`run.json` và tệp verdict thật. Trường `model_bang_chung` tự khai **KHÔNG ĐO ĐƯỢC** model từ tệp
session — lời khai yếu ấy có được ghi đúng mức không, hay đang khai mạnh hơn bằng chứng?

## Phạm vi cứng

- CHỈ ĐỌC/GHI TRONG SANDBOX. `cay-kho/` detached `922956a`, sạch, 306 `refs/heads` (do
  `update-ref` tạo CÓ CHỦ Ý — không phải rác). `status --porcelain` phải RỖNG khi xong.
- Không cấp lease, không đăng Issue/PR, không merge, không sửa kho thật.
- Không nâng `timeout-minutes` (`PROTOCOL §12`).
- **KHÔNG chạy bộ test dài, KHÔNG gọi CI.** Được: nạp module + gọi hàm, `yaml.safe_load`,
  `git` chỉ đọc, `lease_publish.py check`, `ai-dang-giu`, `doc-claims-check`, `doctrine-scan`,
  `adr-song`, `sha256sum`. Không đóng được bằng phép ngắn ⇒ ghi
  `KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)`.
- **Ghi kết luận ra `VERDICT.md` NGAY khi có.**

## GÓI VÁ GỢI Ý — bắt buộc cho mọi P1/P2
Nhãn: *"chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit"*.

## Định dạng `VERDICT.md`
```
verdict: approve | changes_requested | blocked
reviewed_sha: 922956a7048fd23eea1c9f88aeb986e076f10e24
base_da_review_truoc: f77f19895e00835d71644d82f1c54e9b519ccfe6
so_lan_luot_nay_bi_chet_va_phong_lai: <số>

## BẢNG ĐO
| khẳng định | hồ sơ khai | tôi đo được | khớp? |

### <slug>  [P1|P2|P3]  <tiêu đề>
TỆP/DÒNG: · VẤN ĐỀ: · ĐÃ THỬ VÁ: · GÓI VÁ: · ĐÃ THỬ NGHIỆM: · ĐỘ TIN:
```
**Giữ NGUYÊN slug.** `approve` là kết quả hợp lệ — mục tiêu là **hết P1**, không phải verdict đẹp.
