# Cross-review độc lập — PR #821 (bookkeeping hồ sơ land pr779-wp775), lượt 1

Bạn là reviewer Codex, khác họ với executor (Claude). Vai READ-ONLY với kho: KHÔNG sửa tệp nào trong `KHO`. Chỉ ghi vào
thư mục ra (thư mục làm việc hiện tại) hoặc /tmp. Kết quả bắt buộc: tệp `VERDICT.md` trong thư mục ra.

## Định danh (băm là định danh, không phải tên nhánh)

- Kho `ducthangho/tra-luat`, bản sao tại `KHO=/home/user/rv773`, detached ở exact head.
- Exact head: `8e150cf0d9f046a761c49448c8173ad501f53a1c` (nhánh `claude/bookkeeping-779-nguon`, PR #821).
- Base: master `924527c` (merge #820). Diff: `git -C KHO diff 924527c 8e150cf` — 5 tệp: hồ sơ
  `ops/land/pr779-wp775-land-evidence.yaml` (6 dòng sửa), `ops/land/pr779-wp775-provenance/SHA256SUMS` (+3), và 3 tệp mới
  trong `ops/land/pr779-wp775-provenance/do-lai-nguon-20261018/`.
- Thông điệp commit: `git -C KHO show -s 8e150cf`.
- Ref có trong `KHO`: `origin/master`, `origin/ops/wp775-spec`, `origin/agent/wp773-g1-claude` (head #778 `e0e0eac`).

## Bối cảnh

Packet #773 thêm bộ kiểm `ops/land_evidence_nguon.py` (PR #778): lời khai `measured` phải tự chứa ≥ 1 token tệp nguồn phân
giải được (L1). Hồ sơ `pr779-wp775` vào master sau ảnh chụp miễn trừ nên bị đo, và đỏ 6×L1. PR #821 gắn con trỏ cho 6 lời
khai, cộng 3 transcript đo lại (cha con d347d42, spec wp775, kiem-gate offline trên readback). Mục đích: lời khai vẫn ĐÚNG
và mỗi con trỏ trỏ ĐÚNG tệp chứng minh nó — không chỉ để qua cổng. Tiền lệ: PR #787 (hồ sơ pr772) — review lượt 1 ở đó bắt
một con trỏ chỉ khớp tình cờ (`RELEASE_MANIFEST.json`, đầu vào chứ không phải kết quả).

## Nhiệm vụ — ĐO, đừng chỉ đọc

1. `git -C KHO show e0e0eac:ops/land_evidence_nguon.py > /tmp/len.py`; `cd KHO && python3.13 -B /tmp/len.py --root KHO`
   (đòi `TỔNG: ĐẠT`, 0 vi phạm). Đối chứng trên base: `git -C KHO archive 924527c | tar -x -C <tạm>` ⇒ đúng 6×L1.
2. Với TỪNG con trỏ mới: mở tệp được trỏ, đối chiếu từng số liệu trong câu khai (mốc giờ, conclusion, số job, SHA, suite id,
   blob, sha256). Tự chạy lại các lệnh trong 3 transcript (`git -C KHO …`; kiem-gate:
   `python3.13 -B KHO/.claude/dev/packet_loop.py kiem-gate --help`, rồi chạy lại trên `readback-check-runs-f9d84d7.json`).
   Câu khai gốc `merge_3` nói "kiem-gate 15 ten rc=0" — transcript đo 14 + 1 ở hai suite: có trung thực không, có che gì không?
3. `cd KHO/ops/land/pr779-wp775-provenance && sha256sum -c SHA256SUMS`; tập tệp so với tập dòng.
4. Có lời khai nào đổi NGHĨA? Có token nào phân giải chỉ vì trùng tên tình cờ (tệp ở `ops/land/` hoặc gốc kho)? Duyệt TOÀN BỘ
   lời khai `measured` của hồ sơ (dùng `duyet`/`token_nguon`/`phan_giai` của bộ kiểm) và báo con trỏ nào qua cổng mà không
   chứng minh câu khai — kể cả con trỏ có sẵn từ trước, vì PR này tự nhận làm hồ sơ qua cổng.
5. Transcript có khai quá phép đo không (vd tiêu đề "kho tại master 924527c" — đo được không)?

**NGƯỠNG: chủ kho đòi hết P1, P2 VÀ P3.** Approve chỉ khi P1=0, P2=0, P3=0. Báo đủ mọi P3 thật; thứ ngoài phạm vi ghi riêng.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: 8e150cf0d9f046a761c49448c8173ad501f53a1c`
- Dòng hai: `Verdict: approve` hoặc `Verdict: request_changes`, kèm `P1=a P2=b P3=c`.
- Mỗi finding: mức, tệp:dòng, mô tả, lệnh tái hiện + đầu ra đo được, đề xuất sửa.
- Mục "Đã đo" và "Ngoài phạm vi".
