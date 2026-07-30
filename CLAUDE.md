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
7. Deploy — xem "## Quy ước deploy" bên dưới. KHÔNG tự chạy khi user chưa duyệt.
   Windows: user double-click `upload-skill-to-Package.cmd`. Linux/Cowork: `./scripts/deploy-package.sh --push`.

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

## Quy ước deploy (AI ĐẨY Package — chốt 30-07-2026)
**Vì sao cần:** Package là MỘT fileId duy nhất (`SKILL_FILEID = 1H5kAt3SRVP7…`) và `drive-push` GHI ĐÈ nội
dung, giữ fileId. KHÔNG có LockService như registry ⇒ **last-writer-wins, im lặng, không cảnh báo**. Sự cố
30-07-2026: hai phiên song song đẩy cùng fileId trong ~20 phút (v1.35.77 rồi v1.35.78); lần đó vô hại vì phiên
sau build từ master mới nhất và đã bao gồm việc của phiên trước — nhưng nếu ngược chiều thì Package THỤT LÙI
âm thầm, và mọi phiên Cowork mới bootstrap bản cũ.

1. **Ai đẩy:** phiên nào bump VERSION cho đợt đó thì phiên ĐÓ đẩy, sau khi user duyệt. Phiên khác KHÔNG đẩy
   trong lúc đợt đang mở. Hai đường (`upload-skill-to-Package.ps1` · `deploy-package.sh --push`) vào CÙNG
   fileId ⇒ quy ước áp dụng như nhau, không có ngoại lệ "tôi chỉ đẩy nhanh một bản".
2. **TRƯỚC khi build:** `git fetch origin master` + xác nhận HEAD KHÔNG tụt sau `origin/master`. Tụt sau ⇒
   merge/rebase + chạy lại gate TRƯỚC, không build. (Build từ cây tụt sau = đóng gói bản thụt lùi.)
3. **TRƯỚC khi push:** đọc tên file Package ĐANG có trên Drive
   (`gws drive files get --params '{"fileId":"1H5kAt3SRVP7…","fields":"name,size,md5Checksum"}'`).
   Nếu version trên Drive **≥** version sắp đẩy ⇒ **DỪNG, hỏi user** — nghĩa là phiên khác vừa đẩy.
   Đây là chốt chống thụt lùi duy nhất; không có nó thì mục 1-2 chỉ là lời hứa.
   **ĐÃ CƯỠNG CHẾ trong `deploy-package.sh` từ v1.35.79** (rc=3, chặn TRƯỚC `drive-push`; bằng-số cũng
   chặn). Cố ý ghi đè: `--force-older`. Đường `.ps1` bên Windows CHƯA có chốt này — nếu deploy từ đó
   thì phải tự kiểm mục 3 bằng tay.
4. **SAU khi push:** không tin thông báo "đã đẩy". Tải lại từ Drive và đối chiếu **md5/sha256 + VERSION**
   (`deploy-package.sh` bước 5 làm sẵn). Chưa byte-match thì coi như CHƯA deploy.
5. **Thêm/xoá tệp trong cây ⇒ tái sinh `RELEASE_MANIFEST.json`, và ghi lại golden NẾU số đếm kiểm kê đổi.**
   Bỏ bước này thì phiên deploy KẾ TIẾP ăn gate đỏ không phải do nó (bài học r238: `nlm_auth_convert.py`
   làm `files_scanned` 67→68, golden không ghi lại ⇒ `golden` + `determinism` đỏ trên master cho phiên sau).
   Nhắc: `golden-test --write` vẫn CẤM cho diff của một move (R6); chỉ ghi lại khi đã KIỂM diễn biến thực tế
   và xác nhận diff đúng là kiểm kê hợp lệ — kiểm bằng `git diff -- references/golden/` TRƯỚC khi commit.
6. **`core.abbrev` phải = 7 khi chạy gate** (CI ghim `--global`; `deploy-package.sh` ghim repo-local).
   Không ghim ⇒ golden/determinism/doc-claims-check đỏ giả theo kích thước repo — xem ★ v1.35.78 (r241).
7. **Đo nền trước khi nghi bản vá của mình:** gate đỏ ⇒ chạy lại trên `origin/master` sạch, so DELTA. Đỏ sẵn
   thì nói rõ "đỏ sẵn, delta = 0" chứ đừng vá lung tung (cùng doctrine với ngưỡng ruff ở §Quy trình sửa code).

<important if="phát triển Claude Code artifacts">
## Kho tham chiếu Claude Code
Khi cần best practice về Claude Code (agents, commands, skills, hooks,
memory, subagents...), ĐỌC trong ./claude-code-best-practice/best-practice/
TRƯỚC khi dùng kiến thức huấn luyện. Repo này là nguồn ưu tiên.
Cập nhật kho: cd claude-code-best-practice && git pull
(Clone dev-only local — .gitignore + loại bundle qua _RELEASE_EXCLUDE_DIRS; KHÔNG có trong gói deploy.)
</important>
