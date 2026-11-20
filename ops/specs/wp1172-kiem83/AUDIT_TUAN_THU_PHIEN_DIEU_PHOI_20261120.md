# Audit tuân thủ protocol — phiên điều phối Mission #1172 (20-11-2026)

Người audit: một agent Fable 5.2 độc lập, chỉ đọc, đo từ transcript phiên `session_015Gtxrb3cuZ7Nm935R8yA5W`,
các nhánh `ops/wp1448-r1`, `ops/wp1172-plan-r4`, `ops/wp146{0,1,2}-r1`, commit cục bộ `302f76b`/`c5c03ae`,
REST GET trên #1172/#1448/#1460–#1463 và scratchpad của phiên. Đây là bản chép do phiên điều phối lưu lại
để phiên triển khai quy tắc bất biến (ADR-0068) dùng làm đầu vào; nguồn là báo cáo hand-back của agent audit.

Kết luận: lệch ở 23 điểm ngoài §8.3, trong đó 3 điểm chặn ngay. Gốc chung: phiên không đọc
`docs/PROTOCOL_DA_PHIEN.md` và không nạp adapter (`cross-review`, `work-packet`, `soan-spec`) trước 17:17Z, nên mọi
bước review, giao việc và ghi sổ dựng theo HANDOFF và trí nhớ.

## A. Chặn ngay
- **A1 — ADR-0053/0044 kích thước.** `git diff --numstat 64fa515 c5c03ae`: 29 tệp, +5771 dòng (`302f76b`: 21 tệp,
  +3693) trong khi spec wp1448 r2/lease không có `tran_kich_thuoc_sensitive` hay `nang_tran` (trần 3 tệp/300 dòng).
  Phiên vẫn chạy Codex review mã 1 và giao lượt 2. Sửa: dừng PR1 trước review mã 2; trình chủ kho (E2) `nang_tran`
  kèm numstat hoặc tách packet.
- **A2 — §13/§7 handoff trước review.** Review mã 1 chạy khi executor lượt 1 bị cắt, không handoff, cổng chưa N/N.
  Sửa: lượt 2 xuất handoff YAML §7 đủ trường, đăng lên #1448 trước review 2.
- **A3 — đọc protocol và adapter trước.** Lần đầu đọc protocol 17:17Z; 0 lần gọi Skill. Sửa: đọc trọn protocol, §20,
  ADR-0052/0053/0055/0060/0063/0067 và ba SKILL.md; dựng lại prompt từ mẫu adapter.

## B. Phải sửa trước bước kế
- **B1 — trần Codex ADR-0055/0052.** Bốn spec không có dòng `tran_loi_goi_codex: ADR-0055@<oid>` ⇒ trần 2 lời gọi/PR;
  lease/Mission ghi 3. Trần spec-review "4 rồi +2" là ngân sách mềm.
- **B2 — mã E và sổ uỷ quyền (§12, ADR-0067).** 9 câu hỏi chủ kho, 0 câu có mã E; gần như 0 mục sổ
  `uy_quyen_quyet_dinh.v1` cho các quyết định tự đưa (bỏ `ci_dang_ky_test.py` khỏi write set, đổi thiết kế kế hoạch
  bản 6, `full_m9_runs` B1 = 2, A4 not_measured…). Không thấy Issue bản tin quyết định.
- **B3 — đề xuất duyệt băm chưa review.** Bốn lần đề xuất "Duyệt băm (Recommended)" cho bản kế hoạch chưa review lại.
- **B4 — r84 ghi quyết định chủ kho bằng diễn giải** (Q1–Q9) đăng 33 giây sau câu chung chung, băm chưa từng trình.
- **B5 — comment ghi hộ thiếu nhãn** `Quyết định chủ kho — ghi hộ`, nguyên văn, ngữ cảnh; readback chỉ băm khối JSON,
  không so cả body; JSON thiếu `decision_source/approved_by/decision_url`.
- **B6 — verdict/biên nhận chưa lên Issue/kho**; ở 8/10 verdict spec `stdout_sha256` của run.json không nối với tệp
  verdict (runner phải băm chính tệp REVIEW_OUT).
- **B7 — verdict contract §7/§8** thiếu provider/model_family/session_id/review_axes/assurance/independence; gợi ý vá
  thiếu đủ bốn phần; thiếu ĐỐI CHIẾU LƯỢT TRƯỚC.
- **B8 — `core.abbrev` 7** không ghim trong clone reviewer; không đối chiếu cổng mirror.
- **B9 — nhận dạng sandbox reviewer** `KHONG_DO_DUOC`; lease khai `codex_service` nhưng chạy `codex_cli`.
- **B10 — sửa lease packet khác tại chỗ** (bị guard chặn); write set lease lệch spec; lượt 2 chạy Opus mà lease ghi
  Fable — cần lease kế nhiệm hoặc mục sổ.
- **B11 — prompt giao việc** lượt 1 có `$(PROMPT)` chưa bung; lượt 2 không lưu, không băm; thiếu handoff §7,
  heartbeat, `hint_provenance`; prompt đóng băng ghi "SHA given by the coordinator".
- **B12 — ADR-0060 M3/K6 Windows**: diff có 54 dòng `subprocess/pathlib/encoding=`; miễn Windows phải là dòng
  `windows: <H> mien` của chủ kho neo head, không phải câu trong spec.
- **B13 — §8 tối đa hai executor writer đồng thời**; r85 nâng lên 3 mà không nêu mâu thuẫn (E3).
- **B14 — nhãn đối chiếu sai**: chốt tạm dùng `DA_VA_THAT/VA_MOT_PHAN/CHUA_VA/KHONG_DO_DUOC`; protocol dùng bốn nhãn
  `ĐÃ VÁ THẬT · VÁ HỜ · VÁ SINH LỖI MỚI · CHƯA VÁ` theo TỪNG finding trước, rồi lớp; thiếu nguồn lượt/SHA, tỷ lệ |F|/|U|;
  kho đã có `bang_lop` trong `packet_loop.py`.
- **B15 — state máy**: 0 lệnh `packet_loop.py init/record-lease/begin-attempt/transition`; bộ đếm chỉ trong chat/JSON.

## C. Vệ sinh
C1 Packet Issue thiếu schema §3.2 · C2 lease thiếu `heartbeat_at`/`heartbeat_required_minutes` · C3 giao lượt soạn
thứ 4 trước khi r86 cài · C4 không đọc `launcher.py` 1–140 trước `doctor` · C5 dùng `rc` của `tail` thay `PIPESTATUS`.

## Đã tuân thủ
Quét lease trước khi cấp; đăng lease đúng; băm prompt/spec khớp; review qua `launcher.py run` neo head/prompt; clone
review riêng; không đẩy mã, không tự approve/merge; diff trong write set; hồ sơ kế hoạch r4 đủ 9 verdict; đổi thiết
kế khi lớp lặp ba lượt (thiếu mục sổ); backup Drive và đổi executor theo chỉ thị chủ kho; Issue #1460–#1463 trong r85.

## Không đo được
`ai-dang-giu` hiện tại (master cục bộ tụt sau); nội dung phiên trước 06:35Z; executor chạy gate trong worktree liên
kết hay không; nội dung Drive có bí mật hay không; Issue bản tin ngoài 100 issue gần nhất; ADR-0052/0055 có áp cho
review spec/kế hoạch không; `max_run_minutes: 4320`.
