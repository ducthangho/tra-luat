# ADR-0016 — Lớp điều phối rà soát hồ sơ: state LAI, một-người-ghi theo claim, anchor biến tái-rà thành phép tính

- Trạng thái: CHẤP NHẬN (grill 25→26-07-2026, 8/8 quyết định do người vận hành chốt; Đợt 1 = r209/v1.35.45)
- Bối cảnh đầy đủ: `docs/KE_HOACH_RASOAT_HOSO_ORCHESTRATION.md` + `docs/WORKFLOW_RASOAT_TU_DONG.md`
  (nhánh kiến trúc `claude/legal-doc-review-architecture-2al46n`); đặc tả vận hành:
  `references/RASOAT_PLAN_SCHEMA.md` + thẻ `references/workflows/rasoat_hoso.json`.

## Quyết định

1. **State LAI hai tầng bền.** State sống-còn (`_meta/rasoat_state.json`: hàng đợi, claim, quota, note bàn
   giao) nằm trên **Drive trong `_meta/` của profile hồ sơ**; sổ nặng (`master/`, approvals, bugs) nằm
   **local ngoài cây skill**, đẩy Drive theo lô ở checkpoint (Claude chat: mỗi đơn vị). Chỉ MẪU bất biến
   (`templates/`) được nằm trong cây và vào zip.
2. **Một-người-ghi theo `session_claim`.** Quyền ghi là VAI TRÒ chuyển giao được, không phải phiên bất tử:
   phiên cầm claim là bên ghi duy nhất; agent rà read-only; worker Q-NLM chỉ gọi NLM và trả JSON.
   Stale-claim takeover: claim quá hạn 30′ mà con trỏ tiến độ không nhích → phiên mới chiếm quyền qua RMW
   nguyên tử (GAS 2.21.2p); còn nhích → phiên sau lùi.
3. **Anchor (neo phụ thuộc) trên từng phát hiện** (`doc_deps.text_hash` + `cite` + `verified_at` + TTL):
   tái-rà định kỳ = so hash + rà phần diff, không làm lại; phát hiện ghi ở chế độ không-NLM mang
   `muc_chac_chan="cho_verify_nlm"` và trả nợ kiểm chéo qua Q-VERIFY.
4. **Guard ratchet con trỏ tài liệu (H9).** `_doc_pointer_findings` (release.py) fail-closed với cặp
   (tài_liệu, con_trỏ) MỚI đứt ở tài liệu SỐNG; `DOCTRINE_APPENDIX.md` là LƯU TRỮ → advisory; 10 nợ cũ
   khoanh baseline hằng số trong code (sửa = qua review), test khoá số đếm.

## Lý do (trade-off thật)

- Drive-only cho mọi state = mỗi cập nhật một GAS call (~2s, 6 call/file đường nạp) → đắt vô ích cho sổ
  nặng; local-only = chết theo sandbox Claude chat (xoá trắng mỗi phiên) → mất kế nhiệm. LAI lấy đúng mặt
  mạnh mỗi bên; cái giá chấp nhận: kill giữa chừng mất tối đa 1 đơn vị dở (tiêu chí H8).
- Single-writer bằng claim mềm (file) thay vì lock cứng: cho phép kế nhiệm khi phiên chết không nhả khoá,
  vẫn có LockService+RMW GAS làm lưới dưới chống ghi đè vật lý (bài học sự cố registry 1313→2).
- Guard fail-closed toàn bộ 80 con trỏ đứt đo được là bất khả thi ngay (sẽ bị vô hiệu hoá); ratchet có
  baseline chặn được cái MỚI từ ngày đầu — mẫu hình "đặc tả chi tiết rồi không bao giờ viết"
  (`build_parts.py`, `nlm_log.py`) không tái diễn.

## Hệ quả

- Đợt 1 (r209): guard H9 + vá đường cứu hộ LÕI (H0 — bỏ con trỏ `build_parts.py`/`tl_rebuild.sh`, cơ chế
  `_parts/` đã bỏ) + template master + mở rộng tối thiểu `rasoat_phuluc.py` (H1/H1b) + thẻ & schema (H2).
- Đợt 2-4 (kịch bản vòng lặp, agent, degrade-and-continue, chạy thật) xây trên nền này — xem kế hoạch.
- Gỡ nợ baseline = xoá mục khỏi frozenset + sửa test số đếm, có chủ đích từng lần.
