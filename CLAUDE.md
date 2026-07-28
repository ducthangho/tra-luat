# tra-luat — Claude Code Project (dev-side, KHÔNG vào zip deploy)

## Vai trò
Dev/operator cho skill tra-luat. Không tự ý ghi Drive/NLM/registry khi người dùng chưa yêu cầu rõ.
Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package — không mang file này).

## Nguồn sự thật
- `scripts/tl.py` là runtime chính; `VERSION` + hằng `VERSION` trong tl.py + header `SKILL.md` phải khớp nhau
  (selftest có guard `skill_md_version_matches_VERSION`).
- `references/API_CONTRACT.md` là hợp đồng webapp (EXPECT_VERSION trong tl.py phải khớp).
- `SKILL.md` là lõi skill — sửa phải nêu lý do + đổi cả vocab/flag nếu thêm cờ mới.
- Kiến trúc ghi/đọc: GHI registry CHỈ qua GAS webapp (LockService + RMW nguyên tử); Drive đọc/push qua gws CLI
  (PRIMARY từ v1.29.0). KHÔNG thêm đường ghi thứ ba (Drive MCP/Sheets MCP).

## Quy trình sửa code
1. `git status` / `git log --oneline -5`
2. Sửa tối thiểu, giữ idiom comment "vX.Y.Z (bằng chứng) — fix"
3. `python -m ruff check --select F scripts/tl.py` — tiêu chí là **DELTA so master = 0**, KHÔNG phải "0 tuyệt đối".
   Nền ĐO 29-07-2026 (v1.35.60): tl.py **12 F821 + 0 F401**; tl_selftest **3914 F821 + 1 F401**.
   12 F821 (10 tên: `build_parser` `load_creds` `norm_sohieu` `_active_profile` `_cache_file` `_dang_bare_key`
   `_entry_drive_id` `_reassemble_parts` `_sha256_file` `_sohieu_key_entry`) là BY DESIGN: stub-farm gán qua
   `globals()[tên]` từ bảng `_STUB_MAP` nên ruff không thấy tĩnh — đã kiểm HÀNH VI: cả 10 resolve sau import,
   không tên nào bị gọi trước lúc bảng stub chạy (đường cứu hộ `_selfheal_module` không có caller mức module).
   Mốc trôi: v1.34.14 = 0 F821 → v1.34.15 (`bfd18ea`, I10 nén 488 stub → `_STUB_MAP` + factory) = 217 → I11 = 11 → r201 = 12.
   **F401 = 0 nhờ `# noqa` CÓ CHỦ ĐÍCH, KHÔNG phải vì xoá import** (r224): `base64` `datetime` `hashlib`
   `unicodedata` `zipfile` ở đầu tl.py là MẶT NAMESPACE dùng chung — 1646 hàm tl_core được re-home
   `__globals__` về tl.py nên tra tên toàn cục ở ĐÂY, kể cả khi tệp gốc đã tự import (profile_mgmt.py có
   `import datetime` riêng mà vẫn NameError khi tl.py thiếu). Số hàm re-home tra từng tên: unicodedata 19 ·
   base64 9 · hashlib 3 · datetime 2 · zipfile 0. **ĐỪNG "dọn import thừa" ở dòng đó** — gate đã ĐỎ 2 lượt vì việc này.
   Ruff KHÔNG nằm trong gate ⇒ ngưỡng này do người giữ; thấy số lạ thì đo lại master TRƯỚC khi nghi bản vá của mình.
4. `python scripts/tl.py --selftest` (phải N/N, thêm test rXX_ cho mỗi fix)
5. Output DÀI (selftest N case, audit/golden JSON, gate logs) → giao agent `tl-auditor` (read-only) tiêu hoá,
   phiên chính chỉ nhận kết luận — giữ context sạch (G5 §11 kế hoạch guard-va-boc-tl-core).
6. `git diff` → CHANGELOG.md (mục ★ vX.Y.Z) → commit
7. Deploy = user double-click `upload-skill-to-Package.cmd` (KHÔNG tự chạy)

## Bài học đắt giá (đã trả giá, không lặp lại)
- **Đối chiếu nhánh/patch ngoài: BẮT BUỘC test HÀNH VI 2 CHIỀU** (fixture họ chạy trên ta + phản chứng bơm vào
  bản họ), KHÔNG grep chuỗi. Mỗi PORT/REJECT phải có bằng chứng chạy được, khoá bằng test rXX_.
- **Ghi giá trị RỖNG qua reg_bulk/upsert bị webapp BỎ QUA** — xoá field phải đi `reg_clear` (`_journaled_reg_clear`).
- Mọi số hiệu/tên VBQPPL phải có NĂM (VBHN thiếu năm = collision — số tái dùng theo năm).
- Subagent KHÔNG được sửa `tl.py` canonical (bài học rogue-edit) — agent chỉ read-only; vá code do phiên chính làm.
- registry claim NLM là ESTIMATE — slot/FULL/overflow phải neo `nlm-get`/`nlm-reconcile` LIVE.

## Cấm
- Không tự chạy lệnh có `--apply` / `source-delete` / `reg-delete` / `--clear-stale` khi user chưa duyệt (hook sẽ hỏi).
- Không đọc/ghi secrets (`*.enc`, `tl_secrets*`, `*cookie*`, `*token*`, `credentials*`) ngoài đúng quy trình
  `gws-auth-stage`/`secrets-set` mà user yêu cầu.
- Không dùng Drive MCP/Sheets MCP để sửa corpus/registry.
- Không dùng RAG/NLM để trả NGUYÊN VĂN điều luật — nguyên văn chỉ từ nguồn đã verify (extract/web official).

## Khi đóng gói
Bump VERSION (3 chỗ) → CHANGELOG → selftest N/N → user tự chạy cmd (script tự loại .git/.claude/.githooks/
CLAUDE.md/config/enc + quét token). Verify sau deploy: Package trả VERSION mới.

<important if="phát triển Claude Code artifacts">
## Kho tham chiếu Claude Code
Khi cần best practice về Claude Code (agents, commands, skills, hooks,
memory, subagents...), ĐỌC trong ./claude-code-best-practice/best-practice/
TRƯỚC khi dùng kiến thức huấn luyện. Repo này là nguồn ưu tiên.
Cập nhật kho: cd claude-code-best-practice && git pull
(Clone dev-only local — .gitignore + loại bundle qua _RELEASE_EXCLUDE_DIRS; KHÔNG có trong gói deploy.)
</important>
