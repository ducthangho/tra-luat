# KẾ HOẠCH — LỚP ĐIỀU PHỐI RÀ SOÁT HỒ SƠ DỰ THẢO LUẬT (trên skill tra-luat)

> Trạng thái: ĐỀ XUẤT (chưa triển khai). Phạm vi: lớp điều phối phía trên skill — KHÔNG đụng `scripts/tl.py`
> trừ khi nêu rõ. Nguồn gốc: phiên kiến trúc 2026-07-25 (nhánh `claude/legal-document-review-architecture-dlbrut`).
> Tài liệu nền: `references/QUY_TRINH_RA_SOAT_3_TANG.md` · `references/CHECKPOINT_TEST_PLAN.md` · ADR-0001.

---

## A. MÔ TẢ BÀI TOÁN

Rà soát hồ sơ văn bản dự thảo luật là tác vụ dài, nhiều bước, frontier động:

1. Nạp hồ sơ (nhiều văn bản) vào Profile.
2. Lập kế hoạch rà nhiều bước cho cả hồ sơ.
3. Rà từng bước: kết hợp NLM (định vị/quan hệ) + đọc file trực tiếp (nguyên văn từ cache/raw).
4. Ghi kết quả trung gian ra outputs.
5. Giữa chừng phát hiện văn bản mới → nạp bổ sung → rà thêm.
6. Gặp lỗi skill → sửa → nạp lại → chạy tiếp.
7. Lặp đến khi hết kế hoạch → tổng hợp & trình bày theo yêu cầu người dùng.

**Mục tiêu:** chạy đầu-cuối tự trị, người chỉ chạm HAI ĐẦU (giao việc + nghiệm thu); giữa chừng máy tự chạy,
trừ các điểm dừng có chủ đích (mục B.4).

## B. NGUYÊN TẮC KIẾN TRÚC (đã chốt)

1. **Một skill lõi + command quy trình mỏng.** KHÔNG tách runtime thành nhiều skill (tránh drift VERSION/deploy).
   Quy trình đóng gói dạng lớp mỏng theo pattern `/gate`, `/release-checklist` sẵn có.
2. **Agent theo tiêu chí CÁCH LY CONTEXT, không phân vai.** Mô hình hub-and-spoke: phiên chính điều phối và là
   **bên ghi duy nhất tại mỗi thời điểm**; mọi agent con read-only (bài học rogue-edit). Agent trả JSON theo
   schema cố định, phiên chính chỉ nhận kết luận (G5 §11 — giữ context sạch).
3. **Worklist loop + kế-hoạch-là-file, KHÔNG graph engine.** Frontier động (văn bản mới phát sinh) mô tả bằng
   hàng đợi trong PLAN file, không phải DAG tĩnh. **State nằm trong file, không nằm trong context** — điều kiện
   để kế nhiệm phiên: "phiên chính" là VAI TRÒ chuyển giao tuần tự, không phải một cửa sổ context bất tử.
4. **Điểm dừng có chủ đích (giữ nguyên, không tự động hoá qua):** hook duyệt `--apply`/`*-delete`/`--clear-stale`;
   deploy tay ở LIVE (`upload-skill-to-Package.cmd`); kết luận cuối + ký do người rà soát (Mục G).

## C. KIẾN TRÚC ĐÍCH — THÀNH PHẦN

```
NGƯỜI: giao việc (kickoff contract) ──► PHA 0 tiền kiểm (doctor/precheck/cookie) ── fail → DỪNG SỚM
                                                       │ ok
        ┌──────────────── VÒNG LẶP WORKLIST (phiên chính) ────────────────────────────┐
        │ đọc PLAN.json → lấy đơn vị pending → spawn agent tl-rasoat (read-only)      │
        │ ← nhận JSON phát hiện đã verify → append BANG_MASTER → cập nhật PLAN        │
        │ văn bản mới phát hiện → append hàng đợi PLAN (trong phạm vi uỷ quyền → nạp) │
        │ lỗi skill → BUGS_FOUND.md + workaround, chỉ dừng khi CHẶN ĐỨNG              │
        │ cạn context/ngân sách NLM → chốt checkpoint + note bàn giao → phiên KẾ NHIỆM│
        └── ĐK DỪNG: hết pending + hàng đợi rỗng + phát hiện đã verify ──► thoát ─────┘
                                                       │
                             PHA 4 tổng hợp (context sạch, chỉ đọc outputs)
                                                       │
NGƯỜI: nghiệm thu (duyệt Phiếu A–G, duyệt lô lệnh --apply chờ, ký)
```

| # | Thành phần | Dạng | Ghi chú |
|---|---|---|---|
| C1 | `PLAN.json` hồ sơ | file outputs, máy-đọc-được | văn bản × đơn vị rà × trạng thái (pending/doing/done) + hàng đợi phát sinh + note bàn giao + quota NLM còn lại |
| C2 | Bảng master phát hiện | JSONL/JSON append-only | schema = bảng C Pha 4; đầu vào duy nhất của `rasoat_phuluc.py` |
| C3 | Vòng lặp `/rasoat-hoso` | reference + command mỏng | kịch bản worklist loop; LIVE đọc từ `references/`, dev có wrapper `.claude/commands/` |
| C4 | Agent rà đơn vị `tl-rasoat` | prompt mẫu (read-only) | Tầng 1→3 + VERIFY cho MỘT đơn vị; cấp quota NLM trong prompt; trả JSON schema C2 |
| C5 | `BUGS_FOUND.md` + chính sách degrade-and-continue | quy ước trong quy trình | lỗi có workaround → ghi + đi vòng; chỉ blocker mới dừng chờ người |
| C6 | Kickoff contract | mẫu giao việc | phạm vi hồ sơ, uỷ quyền ghi (nạp văn bản THUỘC hồ sơ), ngân sách, chính sách lỗi |

**Lưu ý đóng gói:** zip deploy LOẠI `.claude/` → mọi thứ LIVE cần phải nằm ở `references/` + 1 dòng vocab trong
`SKILL.md`. `.claude/commands/` + `.claude/agents/` chỉ là wrapper dev-side. Agent cho LIVE = phiên chính spawn
general-purpose với prompt mẫu trong references (LIVE không có file agent riêng).

## D. HIỆN TRẠNG ĐÁP ỨNG (đối chiếu 2026-07-25)

Tầng công cụ ~85% · tầng điều phối ~35% · tổng ~65–70%.

| Yêu cầu | Mức | Đã có / Còn thiếu |
|---|---|---|
| Nạp hồ sơ vào Profile | ~95% | profile-promote/ingest-*, apply fail-closed (plan-hash+confirm), 3 van NLM, bảng tay, --resume |
| Rà NLM + đọc file | ~90% | quy trình 3 tầng, rasoat_worksheet (Tầng 1 tất định), tra_cuu --cite --exact, nlm_qa verify, nlm_log |
| Write-safety registry | ~90% | precheck, WAL journal, resume, undo, journal --close |
| Nạp bổ sung giữa chừng | ~70% | đường nạp đủ; THIẾU hàng đợi động máy-đọc-được |
| Kế hoạch mức HỒ SƠ | ~40% | worksheet chỉ per-văn-bản, định dạng cho người; THIẾU PLAN.json (C1) |
| Vòng lặp rà đến hết plan | ~30% | `tl loop` hiện có là loop vệ sinh registry, KHÔNG phải worklist rà; THIẾU C3+C4 |
| Sửa skill giữa chừng | ~60% | ADR-0001 bundle, gate, tl_boot self-heal; THIẾU C5 |
| Tổng hợp & trình bày | ~75% | rasoat_phuluc, văn phong/thể thức references; ⚠ LỆCH: `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` được QUY_TRINH + rasoat_phuluc.py tham chiếu nhưng KHÔNG có trong repo |
| Kế nhiệm phiên | ~50% | journal/resume phủ phần ghi; THIẾU note bàn giao trạng thái rà (gộp vào C1) |

## E. KẾ HOẠCH TRIỂN KHAI

Ràng buộc chung: KHÔNG đụng `tl.py` (trừ H7 nếu lộ bug thật — theo đúng quy trình sửa code + test `rXX_`).
File mới cho LIVE đặt ở `references/`/`templates/` (vào zip); SKILL.md đổi → bump VERSION 3 chỗ + CHANGELOG
+ nhắc re-import Capabilities.

### Đợt 1 — Nền tảng state (điều kiện tiên quyết của mọi thứ sau)

| Hạng mục | Sản phẩm | Nghiệm thu |
|---|---|---|
| H1. Khôi phục/tạo bảng master | `templates/MAU_BANG_TONG_HOP_PHAT_HIEN.json` (schema bảng C: nguyên văn-cite → căn cứ → phân tích → xử lý & lộ trình → định tuyến phụ lục → mức chắc chắn) | `rasoat_phuluc.py` đọc được file mẫu; tham chiếu trong QUY_TRINH hết đứt |
| H2. Schema PLAN hồ sơ | `references/RASOAT_PLAN_SCHEMA.md` + JSON mẫu (C1: trạng thái, hàng đợi, bàn giao, quota) | Claude sinh được PLAN từ một hồ sơ mẫu bằng tay theo schema; không cần code mới |

### Đợt 2 — Lớp điều phối

| Hạng mục | Sản phẩm | Nghiệm thu |
|---|---|---|
| H3. Vòng lặp rà hồ sơ | `references/RASOAT_HOSO_LOOP.md` (kịch bản worklist: đọc PLAN → spawn → append → cập nhật → ĐK dừng → chốt checkpoint) + wrapper dev `.claude/commands/rasoat-hoso.md` + 1 dòng vocab SKILL.md | chạy khô trên PLAN mẫu: đúng thứ tự, đúng ĐK dừng, PLAN cập nhật sau mỗi đơn vị |
| H4. Agent rà đơn vị | prompt mẫu `tl-rasoat` trong `references/RASOAT_HOSO_LOOP.md` (read-only, quota NLM trong prompt, output JSON schema H1) + wrapper dev `.claude/agents/tl-rasoat.md` (cùng khung ranh giới cứng như tl-auditor) | agent rà 1 đơn vị thật, trả JSON hợp lệ schema, KHÔNG ghi file nào; phát hiện đối chiếu được với rà tay |

### Đợt 3 — Tự trị hoá

| Hạng mục | Sản phẩm | Nghiệm thu |
|---|---|---|
| H5. Degrade-and-continue + bug ledger | mục mới trong `QUY_TRINH_RA_SOAT_3_TANG.md`: phân loại lỗi (workaround/blocker), format `BUGS_FOUND.md`, quy tắc "sửa nóng CHỈ khi chặn đứng; còn lại gom vá sau lượt rà" | bơm 1 lỗi giả lập giữa vòng rà → vòng lặp ghi ledger và chạy tiếp, không dừng |
| H6. Kickoff contract + tiền kiểm | mẫu giao việc trong `RASOAT_HOSO_LOOP.md` (phạm vi, uỷ quyền nạp văn-bản-thuộc-hồ-sơ, ngân sách NLM, chính sách lỗi) + bước Pha 0 bắt buộc: doctor/precheck/tuổi cookie — fail → dừng TRƯỚC khi rà | cookie giả >14 ngày → dừng sớm ở Pha 0 với thông báo 1 dòng |

### Đợt 4 — Kiểm chứng LIVE

| Hạng mục | Sản phẩm | Nghiệm thu |
|---|---|---|
| H7. Chạy thật 1 hồ sơ nhỏ (2–3 văn bản) trên Cowork LIVE | log đếm: số lần người phải xen vào giữa chừng + lý do; PLAN/bảng master/phiếu ra đúng | ≤2 lần xen giữa chừng; mỗi lần đều thuộc danh mục điểm-dừng-có-chủ-đích (B.4) |
| H8. Kiểm chứng kế nhiệm | kill phiên giữa đơn vị đang rà → mở phiên mới | phiên mới đọc PLAN + note bàn giao, rà tiếp đúng chỗ, không lặp lại đơn vị done, mất tối đa 1 đơn vị dở |

### Định nghĩa HOÀN THÀNH toàn kế hoạch

Một hồ sơ thật chạy đầu-cuối: người giao việc 1 lần, nghiệm thu 1 lần; giữa chừng ≤2 điểm dừng thuộc B.4;
kill-phiên giữa chừng resume được; sản phẩm cuối = dự thảo Phiếu A–G + bảng master + danh sách đề xuất
chờ duyệt `--apply` + `BUGS_FOUND.md`.

## F. RỦI RO & GIẢM THIỂU

| Rủi ro | Giảm thiểu |
|---|---|
| Cookie NLM chết giữa vòng rà (Cowork không tự refresh) | H6 tiền kiểm tuổi cookie; cron `secrets-set --nlm` phía local (COWORK_PROJECT.md §3) |
| Lỗi skill chặn đứng ở LIVE (deploy là bước tay) | H5 degrade-and-continue; tần suất giảm dần theo mỗi fix khoá test `rXX_` |
| Hai phiên cùng cầm quyền ghi (vi phạm single-writer) | quy ước trong H3: nhận vai = ghi `session_claim` vào PLAN; registry đã có LockService+RMW làm lưới dưới |
| LIVE drift (kết luận lỗi đo trên bản trễ) | mọi báo lỗi skill trong `BUGS_FOUND.md` ghi rõ VERSION đo được (CONTEXT.md — LIVE vs canonical) |
| Agent con vượt quota NLM | quota ghi trong prompt + bắt buộc `nlm_log.py add`; phiên chính đối chiếu CSV sau mỗi đơn vị |
