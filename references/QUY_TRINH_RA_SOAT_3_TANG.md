# QUY TRÌNH RÀ SOÁT VBQPPL 3 TẦNG — kế hoạch thực thi & vòng lặp chuẩn
*(reference của skill tra-luat; áp dụng cho rà soát một văn bản theo 06 tiêu chí HD06. NLM = ĐỊNH VỊ + QUAN HỆ; nguyên văn từ cache/raw; kết luận do người rà soát.)*

> **Ý đồ cốt lõi.** Hỏi NLM theo chủ đề chỉ là **lưới thô** (RAG recall hạn chế, không chứng minh được "vắng mặt"). Hỏi theo từng Điều có recall cao nhưng bất khả thi đại trà. Quy trình này **phân tầng**: rẻ trước — đắt sau, và **chuyển việc kết luận mâu thuẫn sang Claude so nguyên văn từ cache**, không giao cho recall của NLM.

---

## SƠ ĐỒ VÒNG LẶP

```
PHA 0 Khởi động ──► PHA 1 Định vị VB đích ──► PHA 2 Phát hiện VB liên quan + lỗ hổng nguồn
                                                          │
                                                          ▼
                                        PHA 3 Nạp cache DEEP (đích + căn cứ có sẵn)
                                                          │
                                                          ▼
        ┌──────────── VÒNG LẶP RÀ SOÁT (lặp theo từng ĐƠN VỊ RÀ / chế định) ───────────┐
        │  TẦNG 1 Phân tầng (cache, 0 NLM): lọc Điều rủi ro cao                          │
        │  TẦNG 2 Quét thô (NLM scoped, ≤6 câu/phiên): định vị ứng viên mâu thuẫn        │
        │  TẦNG 3 Đào sâu (NLM DEEP theo Điều, CHỈ nhóm rủi ro + cờ T2) → Claude so cache│
        │  VERIFY nguyên văn (cache/raw) ──► ghi phát hiện vào bảng tạm                  │
        └──────────── ĐK DỪNG đơn vị? ──no──► đơn vị kế tiếp ; ──yes──► thoát vòng ──────┘
                                                          │
                                                          ▼
            PHA 4 Tổng hợp & điền Phiếu (A–G) ──► PHA 5 Vệ sinh registry cuối phiên
```

---

## PHA 0 — KHỞI ĐỘNG
- Đọc `tra_luat_config.json` (Drive MCP) → `TL_WEBAPP/TL_TOKEN/TL_MIRROR_ID`.
- `registry_orchestrator.py boot` (ping + changes_pull); `regen2` chỉ khi mất baseline / delta > 40.
- `notebook_get` một lần → bản đồ `nlm_title ↔ source_id`, dùng lại cả phiên.

## PHA 1 — ĐỊNH VỊ VĂN BẢN ĐÍCH
- `vb_status <số hiệu>` → số hiệu thật, VBHN hay gốc, in-force, `superseded_by`/`supersedes`, `nlm_source_id`.
- **VBHN-first**: nếu có `superseded_by = VBHN…` thì rà bản VBHN.
- **Cổng Mục A**: xác định cơ quan chủ trì soạn thảo → có thuộc trách nhiệm rà soát của Ủy ban không. Không thuộc → xử lý điểm 7.1–7.4, dừng rà toàn văn.

## PHA 2 — PHÁT HIỆN VĂN BẢN LIÊN QUAN + SOI LỖ HỔNG NGUỒN (Mục B)
- Đọc manifest/registry (offline). Với mỗi tiêu chí, liệt kê căn cứ đối chiếu và đánh dấu **CÓ/THIẾU** trong corpus:
  - T1 → văn kiện/Nghị quyết/Kết luận của Đảng (thường ở notebook chuyên đề; thiếu → Mục F).
  - T2 → Hiến pháp; NĐ 79/2025; **các luật cùng/cao cấp liên quan** (tìm theo `linhvuc` + `tukhoa`).
  - T3 → điều ước quốc tế/Công ước (kiểm có trong corpus không).
  - T4 → Luật Đầu tư (Phụ lục ngành nghề ĐTKD có điều kiện) + thẩm quyền.
  - T5/T6 → phần lớn từ thực tiễn (ngoài corpus) → Mục F.
- **Đầu ra Pha 2:** danh sách căn cứ + `source_id` VBHN-first; danh sách **lỗ hổng nguồn** (nạp thêm hoặc đẩy Mục F). Làm xong TRƯỚC khi hỏi NLM.

## PHA 3 — NẠP CACHE (DEEP)
- `ingest_to_cache.py` văn bản đích `--method auto` (ưu tiên exportdocx → exporttext → download_file_content → read_file_content). Lấy **bản đồ Chương/Điều + raw verbatim**.
- Nạp cache các căn cứ đối chiếu ĐÃ có trong corpus (để verify + neo câu hỏi).
- Từ bản đồ, **chia văn bản thành ĐƠN VỊ RÀ** theo chế định (vd với BLLĐ: HĐLĐ; tiền lương; thời giờ; kỷ luật–sa thải; lao động đặc thù; công đoàn–đối thoại; tranh chấp; cho thuê lại lao động/dịch vụ việc làm).

---

## VÒNG LẶP RÀ SOÁT — 3 TẦNG (lặp theo từng đơn vị rà)

### TẦNG 1 — PHÂN TẦNG (cache, 0 NLM)
> Tự động hóa: `rasoat_worksheet.py --so-hieu <…>` sinh sẵn **Phiếu công tác** (bảng phân tầng SÂU/ĐỐI CHIẾU/— + theo dõi tiến độ) và **Nhật ký NLM (CSV)**. Quy tắc dấu hiệu xem `references/BANG_PHAN_TANG_RUI_RO.md`.
Từ raw của đơn vị rà, lọc **Điều rủi ro cao** = Điều thoả ≥1 dấu hiệu:
- giao quy định chi tiết / "theo quy định của Chính phủ" (rủi ro T2: chưa ban hành chi tiết);
- đặt điều kiện ĐTKD / điều kiện hành nghề / thủ tục hành chính (T4);
- dùng từ định tính/đa nghĩa, thuật ngữ chưa định nghĩa (T5);
- điều chỉnh vấn đề **liên luật** (trùng chủ đề với căn cứ đối chiếu ở Pha 2) (T2/T3);
- điều chỉnh vấn đề mới/đang biến động (T6).
Bỏ qua định nghĩa thuần, điều khoản thi hành, boilerplate.

### TẦNG 2 — QUÉT THÔ (NLM scoped, lưới recall rộng)
- Mỗi phiên: `notebook_query` với `source_ids` đúng (1–3, hard-cap 5), **≤6 sub-question**, reuse `conversation_id` trong cùng scope.
- Câu hỏi định vị/quan hệ (KHÔNG xin nguyên văn để dùng, KHÔNG xin kết luận):
  - nội bộ: cặp Điều mâu thuẫn; Điều giao quy định chi tiết.
  - liên văn bản: trùng/chồng/mâu thuẫn theo từng cặp [đích × 1 căn cứ].
- Mục tiêu: thu **danh sách Điều ứng viên** để Tầng 3 soi kỹ.

### TẦNG 3 — ĐÀO SÂU (NLM DEEP theo Điều) + CLAUDE SO CACHE
- **Chỉ chạy cho** nhóm Điều rủi ro cao (Tầng 1) + Điều bị Tầng 2 gắn cờ.
- Neo câu hỏi vào Điều cụ thể (vd: *"Giới hạn trong Điều 36 và Điều 125 BLLĐ: hai Điều có quy định khác nhau về cùng hành vi không?"*) → retrieval trúng chunk, recall cao hơn hỏi cả luật.
- **Kết luận mâu thuẫn KHÔNG dựa vào câu trả lời NLM**: kéo nguyên văn cả hai Điều từ cache (`tra_cuu.py --cite … --exact`), Claude đặt cạnh nhau so trực tiếp.

### VERIFY (bắt buộc trước khi ghi phát hiện)
- Mọi đoạn «…» NLM → `nlm_qa.py verify`; "failed" → bỏ, lấy lại cache/raw.
- Nguyên văn đưa vào Phiếu **luôn** từ cache/raw, không từ NLM.
- Khẳng định phủ định ("không có trong Phụ lục/luật") → đối chiếu nguồn chính thức, gắn mức "cần kiểm tra".

### ĐIỀU KIỆN DỪNG (mỗi đơn vị rà)
Dừng đơn vị khi: (a) đã soi hết Điều rủi ro cao + Điều bị cờ; (b) các phát hiện đã verify; (c) không còn ứng viên mới phát sinh từ Tầng 3. Nếu Tầng 3 lộ thêm Điều liên quan → thêm vào hàng đợi rồi lặp; nếu ngân sách NLM phiên gần ngưỡng (~20–25 call) → chốt phiên, ghi "đơn vị còn lại: …", tiếp ở phiên sau.

---

## PHA 4 — TỔNG HỢP & ĐIỀN PHIẾU (A–G)
> Văn phong: tuân `references/VAN_PHONG_HANH_CHINH.md` (câu ngắn, chính xác, không đa nghĩa, không viết tắt/tiếng Anh/văn hoa). Phụ lục: dồn phát hiện vào bảng master (`templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json`), rà xong mới chạy `rasoat_phuluc.py` sinh 03–07-BN MỘT LẦN (dedup + đánh số). Ghi mỗi truy vấn NLM bằng `nlm_log.py add`.
- Mỗi phát hiện điền bảng C theo trật tự cố định: nguyên văn → căn cứ đối chiếu (tên+số hiệu+Điều/Khoản) → phân tích → hình thức xử lý & lộ trình → định tuyến phụ lục → (T1: thành phần i–xii) + mức độ chắc chắn.
- Thứ tự ưu tiên xử lý: giải thích (Đ60) → hướng dẫn áp dụng (Đ61) → tạm ngưng → sửa đổi/bổ sung/thay thế/bãi bỏ/ban hành mới. Cơ chế đặc thù NQ 206/2025 **không** áp cho nội dung trái Hiến pháp/trái pháp luật và điều kiện ĐTKD sai thẩm quyền.
- Mục D: đếm theo văn bản gốc, 1 nội dung 1 lần, khớp phụ lục 03–07-BN.
- Mục E định tuyến mẫu; Mục F nội dung chờ xác nhận (gồm lỗ hổng nguồn Pha 2); Mục G checklist + ký.

## PHA 5 — VỆ SINH REGISTRY CUỐI PHIÊN
- Không đụng cấu trúc Drive → `manifest_export`.
- Có move/rename/ingest/add → `manifest_build.py` (regen2 → manifest_export); doc mới thiếu tukhoa → `backfill_keywords_live.py`.

---

## NGÂN SÁCH & GIỚI HẠN (mặc định)
- NLM: ≤6 sub-question/phiên; scope 1–5 source; reuse `conversation_id` cùng scope; tổng ~11–14 call/luật cho lưới thô; Tầng 3 cộng thêm theo số Điều rủi ro cao.
- Cấm: `source_list_drive` toàn notebook làm danh mục; xin NLM trích để dùng/kết luận; gắn hiệu lực khi nguồn không thể hiện; bịa số hiệu/ngày.
