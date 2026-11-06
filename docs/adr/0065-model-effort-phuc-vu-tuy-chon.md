# ADR-0065 — Model/effort phục vụ của reviewer là trường ghi nếu đo được

- **Trạng thái:** Accepted — quyết định chủ kho https://github.com/ducthangho/tra-luat/issues/1240#issuecomment-6662892793
  (*"(a) hồi tố, (b) không bắt buộc"*); đáp án Q1/Q2 https://github.com/ducthangho/tra-luat/issues/1240#issuecomment-6663218706
  (*Q1 "Có, theo provider"*, *Q2 "Không tính"*).
- **Nguồn:** packet `ASSURANCE-81-MODEL-EFFORT-TUY-CHON` #1240, đặc tả `ops/specs/assurance-81-model-effort-tuy-chon-r1.md`
  (sha256 `e7c67078…487e`).

## Bối cảnh

`docs/PROTOCOL_DA_PHIEN.md` §8.1 đòi ghi model và effort thực tế của cặp Executor–Reviewer, và câu *"Evidence fallback
hoặc không đủ nhận dạng thì chưa nhận assurance"* đã làm nhiều hồ sơ land thành `CHUA_DAT` chỉ vì không đo được model
hoặc effort phục vụ. Luật L7 của `ops/land_evidence_nguon.py` cưỡng chế điều ấy bằng máy: khai
`reviewer_assurance_81: DAT` mà `thuc_thi.model` hoặc `thuc_thi.effort` không phải lời khai `measured` thì ĐỎ.
Đợt hạ cấp r24 (#748) hạ 13 hồ sơ chỉ vì *"họ model reviewer khong_do_duoc"*.

Thực tế, CLI chỉ công bố model/effort trong header, nhiều lượt không ghi được, và giá trị ấy không thay đổi điều reviewer
đã đọc: thứ neo một review là exact SHA, mã thoát, băm đầu ra và verdict. Chủ kho chỉ thị ngày 05-11-2026: model và
effort chỉ là tuỳ chọn, không bắt buộc.

## Quyết định

(i) Model và effort phục vụ của reviewer là trường **ghi nếu đo được**, ở MỌI packet, không ngoại lệ — kể cả packet đòi
"reviewer cùng model, effort cao hơn". Đo được thì ghi; không đo được thì ghi `KHONG_DO_DUOC` (hoặc lời khai
`not_measured …`), hoặc bỏ trống.

(ii) `KHONG_DO_DUOC` ở hai trường ấy không làm assurance §8.1 thành `CHUA_DAT` và **không chặn landed**.

(iii) Các mốc vẫn bắt buộc: exact SHA, `ma_thoat`, `stdout_sha256`, verdict và sandbox mode. Provider, execution surface,
transport và session/run ID vẫn phải nhận dạng được; thiếu chúng thì vẫn chưa nhận assurance.

(iv) Theo Q1: model phục vụ không đo được thì họ model lấy theo identity provider — Claude Code ⇒ họ `claude`, Codex ⇒
họ `openai` (protocol dòng 10, ADR-0050 mục 3, `HO_MODEL_MAC_DINH` trong `ops/bien_nhan_v2.py`). Provider không gắn một
họ duy nhất (`google_antigravity` và provider nhiều họ khác) vẫn phải khai `model_family`; với các provider ấy, họ model
không đo được vẫn là `khong_do_duoc` theo §8 mục 1.

(v) Hồi tố theo quyết định (a): các hồ sơ land bị hạ chỉ vì model/effort/họ model được mở lại ở một packet RIÊNG, sau khi
ADR này land, theo quy tắc nhóm G1/G2/G3/N0 của đặc tả (mục *Hồi tố*). Theo Q2, hồ sơ không có khối `thuc_thi` không bị
tính là thiếu sandbox mode khi xét hồi tố; hồ sơ đã có `thuc_thi` vẫn bị đòi sandbox. Mỗi lô hồi tố cần comment duyệt
riêng của chủ kho; danh sách chính thức đo lúc cấp lease của packet hồi tố, không lấy ảnh chụp trong đặc tả.

(vi) `.claude/dev/launcher.py` không đổi: launcher vẫn đo và ghi `model_phuc_vu*`, `effort_phuc_vu*` khi đo được.

## Cổng

`ops/land_evidence_nguon.py` luật L7: khi khai `DAT`, `thuc_thi.sandbox_mode` vẫn bắt buộc là lời khai `measured`
(`L7_KHOA`); `thuc_thi.model`, `thuc_thi.effort` (`L7_KHOA_TUY_CHON`) được vắng, có mặt thì phải là chuỗi `measured …`
hoặc `not_measured …`. Giá trị rác (rỗng, `DAT`, null, sai kiểu) vẫn ĐỎ. `MIEN_TRU_L7` giữ nguyên.
`ops/kiem_ho_so_land.py` (L-6) và `packet_loop.py kiem-merge` K4 đã không đọc model/effort nên không đổi.

## Hệ quả

- Luật chỉ NỚI: mọi hồ sơ ĐẠT trước vẫn ĐẠT sau (đo bằng A7 của đặc tả).
- Một lượt Codex không đo được model vẫn có thể thành `cross_approved` vì họ model lấy theo provider.
- Mất một tín hiệu cảnh báo: lượt chạy bị fallback sang model khác mà không ai đo sẽ không bị chặn. Chấp nhận, vì header
  CLI vốn không chứng minh mọi request giữ model ấy (§8.1), tức tín hiệu cũ đã yếu.
