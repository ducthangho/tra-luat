# EXTERNAL INGEST GATE — research_* chỉ discovery

Ngày: 2026-06-22  
Phiên bản: skill v1.17.25 · webapp contract 2.21.2d

## Lỗi phát hiện

Trong phiên Nghị định 129/2025/NĐ-CP, workflow đã đi tắt:

- dùng `research_start`/`research_import` để nạp thẳng PDF vào NotebookLM;
- tạo notebook tạm thay vì dùng corpus/folder/notebook đang vận hành;
- không ưu tiên docx/GDoc-convertible hoặc convert trước;
- coi đồng ý "tìm nguồn" như đồng ý "ghi/nạp";
- Instruction sinh cho Claude/NLM không tự ràng buộc với SKILL.md tra-luat và QT-3.

Đây là lỗi quy trình nghiêm trọng vì NLM trở thành nơi chứa nguồn canonical trước khi Drive,
registry, tên chuẩn, folder cat và quan hệ pháp lý được kiểm.

## Quy tắc bắt buộc

1. `research_start`/`research_status` chỉ dùng để phát hiện URL ứng viên.
2. Cấm dùng `research_import` hoặc `source_add(url)` để nạp thẳng VBQPPL làm nguồn dùng.
3. Mọi nguồn mới phải đi QT-3: tải về Drive -> `copy_convert` -> `standardize_name.py` ->
   `organize` -> verify `list cat=<NN>` -> `nlm_push`.
4. Đích mặc định là folder Drive + notebook đang dùng. Không tạo notebook/folder mới nếu
   người dùng không yêu cầu rõ.
5. Official-first: ưu tiên Công báo, vbpl.vn, cổng cơ quan nhà nước. Secondary như
   thuvienphapluat/luatvietnam chỉ dùng để phát hiện nhanh, không chốt canonical nếu chưa
   verify official.
6. Ưu tiên docx/doc/GDoc-convertible hơn PDF. Nếu chỉ có PDF, phải convert/OCR trước; không
   nạp PDF thô làm nguồn canonical khi có thể tạo GDoc chuẩn.
7. Trước khi ghi/nạp, phải trình người dùng duyệt: URL, official|secondary, định dạng,
   cat/folder/notebook đích, tên chuẩn, số hiệu/năm/trích yếu, quan hệ gốc/sửa đổi/VBHN.
8. Nếu lỡ tạo notebook tạm, coi là quarantine; hỏi người dùng trước khi xóa hoặc chuyển nguồn.

## Instruction gate

Mọi Instruction do skill sinh cho Claude Project/NotebookLM phải chứa:

- `SKILL_OF_RECORD`
- `ingest_handoff`
- `confirm_gate_web`
- quy tắc `research_import`/`source_add(url)` discovery-only
- official-first
- ưu tiên docx/GDoc hơn PDF
- mặc định notebook đang dùng

Kiểm bằng:

```bash
python scripts/gen_instructions.py --selftest
python scripts/tl.py instruction-audit --generate --target nlm --json
python scripts/tl.py instruction-audit --file instruction.md --json
```

Nếu audit fail thì không dùng Instruction đó cho phiên có ghi/nạp.
