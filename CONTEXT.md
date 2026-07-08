# CONTEXT — Ngôn ngữ chung của dự án tra-luat

Thuật ngữ chuẩn dùng trong SKILL.md, CHANGELOG, commit message và các phiên làm việc.
File này là TỪ ĐIỂN — không chứa chi tiết triển khai. Quyết định kiến trúc ở `docs/adr/`.

## Bản thể & phát hành

- **Canonical** — cây git chính thức duy nhất tại `D:\Quốc hội\tra-luat` (remote `github.com/ducthangho/tra-luat`).
  Chỉ canonical được đánh số VERSION và publish. Số version không phát từ canonical là không hợp lệ.
- **Nhánh song song** — phiên làm việc khác (Cowork/Chat/Codex…) sửa skill trên bản copy. Sản phẩm hợp lệ duy nhất
  của nhánh song song là **bundle** (không phải version mới, không phải publish). Xem ADR-0001.
- **Bundle** — zip giao nộp từ nhánh song song: giữ nguyên VERSION fork-point, kèm `BUNDLE_META.json`
  (commit gốc, danh sách file đổi, test thêm). Canonical merge bundle rồi mới đánh số.
- **LIVE (Package)** — file zip trên Drive Package (fileId cố định) mà Cowork/Chat thực tải qua `tl_fetch.sh`.
  LIVE có thể TRỄ so canonical (drift) — kết luận "skill có lỗi X" phải nói rõ đo trên LIVE hay canonical.
- **Deploy** — `tl drive-push` đưa zip canonical lên LIVE, giữ fileId. Luật vận hành: **xanh là deploy ngay**
  (gate xanh ⇒ push cùng ngày + verify tải lại VERSION; SKILL.md đổi ⇒ nhắc user re-import Capabilities).
- **Re-import** — user nạp lại zip vào Cowork Settings→Capabilities; bắt buộc khi SKILL.md đổi, vì agent đọc
  bản import chứ không phải bản Drive.

## Chất lượng & gate

- **Gate xanh** — đủ bộ: `--selftest` + `workflow-audit --strict` + `golden-test` + `determinism-audit --strict`
  + `gen_instructions --selftest` + `release-bundle` ×2 cùng SHA-256 + `release-verify` trong gói giải nén.
- **Golden** — fixture JSON tất định tại `references/golden/`. Độ chặt đã chốt: PASS/FAIL so bản canonical-hoá,
  cộng check **raw-stability** (stdout thô chạy ×2 phải trùng byte) — không so raw-bytes với fixture.
- **Characterization test** — test đặc tả hành vi hiện có của một cụm lõi cũ, viết TRƯỚC khi tách cụm đó
  khỏi tl.py (điều kiện bắt buộc của lộ trình về đích 2.500 dòng).
- **Grandfather** — nợ-đã-biết ghi ở `registry.warnings` (advisory, không fail strict), có deadline siết.
  Đã chốt: 6 lệnh ghi đụng Drive/NLM/registry-corpus siết ở Pha G; 6 backfill/plan siết pha kế tiếp.
- **Command registry** — `tl_core/command_registry.py`: metadata risk/gate/card/contract của LỆNH CLI;
  nguồn sự thật cho tool-inventory/workflow-audit. KHÁC **registry corpus** (Google Sheet `tra_luat_registry`
  — sổ cái văn bản pháp luật). Nói trần "registry" trong ngữ cảnh vận hành corpus = registry corpus.

## Kiến trúc skill

- **Kernel (SKILL.md)** — doctrine agent đọc mỗi phiên; đích Pha F: 20-35KB, chỉ bất biến + con trỏ references.
  Quy trình đổi kernel: draft ở `references/SKILL_KERNEL_DRAFT.md` → user duyệt → thay thật → re-import.
- **tl_core** — package module tách từ tl.py (Pha B trở đi); tl.py là CLI facade duy nhất, bên ngoài không
  gọi tl_core trực tiếp. Đích dài hạn: tl.py ≈ 2.500 dòng (facade + parser skeleton + stubs).
- **bind(tl)** — cơ chế copy-globals cấp helper cho module tl_core trong GIAI ĐOẠN DI CƯ; là giàn giáo,
  không phải kiến trúc đích (xem ADR-0002). Module tl_core cấm đọc bare mutable-global của tl.
- **Stub ủy quyền** — hàm trong tl.py chỉ forward sang tl_core (giữ tương thích selftest/parser/tham chiếu chéo).
