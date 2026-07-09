# DEPENDENCIES — Phụ thuộc runtime + runtime-overlay (tách từ SKILL.md §9, Pha F v1.34.0)

## 9. PHỤ THUỘC
`pip install -r requirements.txt`. Cần env `TL_WEBAPP` / `TL_TOKEN` (mirror `tra_luat_config.json`).

### Runtime overlay v1.18.0 — các lệnh bổ sung khi thiếu bộ rasoat đầy đủ
- `--profile <name>` + `tl profile-info --json`: đọc config v2 đa-corpus; VBQPPL là profile nền lấy token/webapp, profile đang dùng quyết định folder/notebook/registry/manifest.
- `tl link-priority <url...> --json`: xếp link tải cho người dùng theo TVPL → LuatVietnam → Công báo → official khác; không đổi canonical official-first.
- `tl slot-audit --notebook-id <id> [--manifest f.json]`: đếm slot theo `nlm_notebook_id`, phát hiện `NOTEBOOK_FULL` giả do registry cũ đếm mọi `nlm_status`.
- Cache manifest tách theo profile: `vbqppl` dùng cache cũ, profile khác dùng thư mục con `~/.tra_luat_cache/<profile>/`.
- `tl extract --sohieu <số hiệu/tên> --dieu N`: tự chọn canonical từ manifest, export text ra đĩa và chỉ in Điều cần xem.
- `tl exists <số hiệu/tên> [--refresh]`: cổng chống overclaim thay cho `reg_get name_contains`; nếu không thấy thì trả `UNKNOWN_NOT_ABSENT` và yêu cầu kiểm tiếp bằng số hiệu/chủ đề/QT-5.
- `tl source-map <số hiệu/tên...> [--refresh]`: sau boot, lập bản đồ nguồn rà soát theo VBHN-first; dùng cho nhóm luật trước khi query/extract thật.
- `tl relation-check --base <số hiệu gốc> --subject <trích yếu> [--amendment <số hiệu sửa đổi>] --json`: quét corpus/NLM để bắt bản sửa đổi đã có nhưng thiếu `goc/sua_doi`; nếu có `missing_links` thì hỏi người dùng ghi registry ngay.
- `tl vbhn-check --subject <trích yếu> --goc <số hiệu> --year <năm>`: cổng QT-5 sau `source-map`; trả query ngoài corpus nếu manifest không có hit.
- `tl vbhn-verify --text-file <txt> --expect-title ... --expect-goc ... --expect-year ... --official-required`: gate nội dung + nguồn chính thức; bản tự ghép/provisional không được chốt canonical.
- `tl vbhn-compare --official-text <txt> --candidate-text <txt> --focus "Điều 53"`: so bản chính thức với bản tự ghép để bắt thiếu footnote, giữ tham chiếu cũ, khác điều trọng tâm.
- `tl instruction-audit --file <instruction.md>`: fail nếu Instruction thiếu `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, hoặc còn mở đường `research_import/source_add(url)` nạp thẳng NLM.
- `tl instruction-audit --generate --target <project|nlm|both|config> --print-text`: sinh khối Instruction chuẩn từ `scripts/gen_instructions.py` và tự kiểm.
- `tl locate <số hiệu/tên> [--refresh]`: ưu tiên manifest offline; nếu thấy `WARN=OMNIBUS_NARROW_TITLE_CHECK`, `TITLE_METADATA_MISMATCH`, `ORPHAN_CAT`... thì phải chạy `tl status`/`tl hygiene plan --json` trước khi dùng làm nguồn rà soát.
- `tl hygiene scan`: quét duplicate/orphan/title-mismatch, bắt cả dòng số hiệu rỗng mà `vb_status` không thấy.
- `tl hygiene plan <query>`: chọn canonical theo NLM/cat/số hiệu/hiệu lực và lập danh sách đưa QUARANTINE; với VBHN tái sử dụng số hiệu, cụm được tách theo năm/chủ đề/gốc để không quarantine nhầm văn bản khác; chỉ thực thi khi `--apply --confirm yes`.
- `tl rasoat ...`: nếu thiếu script chuyên sâu thì trả `RASOAT_FALLBACK_PLAN`, không crash.

Overlay độc lập có `_fallback` cho core runtime; các pipeline chuyên sâu `rasoat_*`, `backfill_*`, `registry_orchestrator.py` vẫn thuộc bộ skill đầy đủ. Cài overlay lên base skill để chạy tự động toàn phần; nếu chạy riêng, `tl doctor` sẽ báo thiếu optional thay vì crash.

Ưu tiên dùng `python scripts/tl.py ...`. Nếu cần gọi client tối thiểu thì cú pháp fallback là `python scripts/_fallback/gas.py ACTION key=value`; không dùng cú pháp cũ `gas.py get ACTION`.



### v1.18.0 multi-corpus + link priority + notebook slot guard
- Thêm mô hình `corpus profile`: `vbqppl` giữ webapp/token và corpus pháp điển; `vbthuong`/profile dự án có folder, notebook, registry, manifest riêng. `--profile`/`TL_PROFILE` overlay config v2.
- Khi tra cứu ở profile P: manifest/registry P trước, miss mới fallback VBQPPL; QA xuyên corpus dùng `cross_notebook_query` với notebook P + VBQPPL, canonical của P thắng.
- Link tải cho người dùng ưu tiên TVPL/LuatVietnam/Công báo vì tiện tải Word/PDF và xem hiệu lực; canonical lưu/đối chiếu vẫn official-first.
- `slot-audit` và tài liệu .gs yêu cầu `nlm_slots/nlm_preflight` đếm theo `nlm_notebook_id == notebookId`, sửa lỗi `NOTEBOOK_FULL` giả.
- Tài liệu chi tiết: `references/MULTI_CORPUS_PROFILE_V1_18.md`.

### v1.17.25 external-ingest + Instruction gate
- Từ log Nghị định 129/2025: không được nạp thẳng PDF vào notebook tạm bằng `research_import`/`source_add(url)`. `research_*` chỉ discovery; nguồn mới phải đi QT-3 rồi mới `nlm_push`.
- Thêm `scripts/gen_instructions.py` thật, không còn chỉ nhắc trong tài liệu. Output mọi target có `SKILL_OF_RECORD`, `ingest_handoff`, `confirm_gate_web`, official-first, ưu tiên docx/GDoc, và mặc định notebook đang dùng.
- Thêm `tl instruction-audit` để kiểm Instruction/Project prompt; selftest fail nếu thiếu các khối bắt buộc.
- Tài liệu chi tiết: `references/EXTERNAL_INGEST_GATE.md`.

### v1.17.24 amendment gate best-combined
- Hợp nhất thêm nhánh `amendment existence gate`: `source-map` tự quét `amendment_candidates` theo chủ đề/dấu hiệu "sửa đổi", kể cả khi registry thiếu `goc/sua_doi`.
- Nếu phát hiện bản sửa đổi liên quan, `source-map` trả `AMENDMENT_CANDIDATE_IN_CORPUS`, `UNLINKED_AMENDMENT_CANDIDATE`, `VBHN_RECHECK_REQUIRED`, `PAUSE_AND_ASK_USER`; phải dừng và hỏi người dùng trước khi rà tiếp.
- Thêm `tl exists` để kiểm tra hiện diện bằng `source-map` chuẩn hóa; không còn phải dùng `reg_get name_contains` thô.
- `tl vbhn-check --goc <số hiệu>` tự suy trích yếu từ manifest nếu không truyền `--subject`, để sinh query kiểu `"luật thi đua khen thưởng" "hợp nhất"` và `site:thuvienphapluat.vn ...`.

### v1.17.22 stale relation guard
- Từ log Luật Thi đua, khen thưởng: không được kết luận văn bản sửa đổi/VBHN vắng mặt chỉ vì `vb_status` thiếu quan hệ; có thể văn bản đã ở corpus/NLM nhưng registry trống `goc/sua_doi`.
- Thêm `tl relation-check` để quét theo số hiệu gốc + chủ đề + số hiệu sửa đổi đã biết; nếu phát hiện bản sửa đổi đã có, trả `RELATION_BACKFILL_REQUIRED` và hành động `BACKFILL_SUA_DOI_ON_BASE`/`BACKFILL_GOC_ON_AMENDMENT`.
- `tl vbhn-check`/`relation-check` gợi ý cả query web đơn giản như `"luật <chủ đề>" "hợp nhất"` và `site:thuvienphapluat.vn ...`; nguồn secondary chỉ để phát hiện nhanh, canonical vẫn official-first.
- Tài liệu chi tiết: `references/STALE_RELATION_GUARD.md`.

### v1.17.17 merge hardening
- Giữ nền `v1.17.15-vbhn-hygiene-guards` và bổ sung lại `tl vbhn-normalize --json` để report-only các việc cần backfill/rename VBHN và ghost NLM.
- Chặn lỗi tên rỗng match mọi query: mọi so khớp tên phải yêu cầu `nk` không rỗng; tránh NLM ghost lọt vào `locate/source-map/hygiene plan`.
- `_goc_keys` xử lý đúng `goc` dạng list/dict; khóa hygiene VBHN sạch hơn khi manifest lưu nhiều số hiệu gốc.
- `registry_hygiene.py` đồng bộ flag với `tl.py`: `VBHN_SOHIEU_NORMALIZED_FROM_SHORT_VPQH`, `VBHN_NAME_MISSING_YEAR`, `NLM_GHOST_SOURCE`.

### v1.17.19 VBHN cấp Bộ phải có năm
- Từ log "lô 33 đổi tên": VBHN cấp Bộ (`NN/VBHN-BYT`, `05/VBHN-BGDĐT`, `2279/VBHN-BLĐTBXH`...) cũng là VBQPPL, không được để tên/metadata thiếu năm.
- `tl.py` và `registry_hygiene.py` nhận diện số hiệu VBHN cấp Bộ, gắn `VBHN_MINISTRY_SCOPE`, `VBHN_MINISTRY_MISSING_YEAR`, `VBHN_MINISTRY_NAME_MISSING_YEAR` để đưa vào `title_mismatch_candidates`.
- `tl vbhn-normalize --json` report-only mẫu tên riêng cho cấp Bộ: `VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>`; thiếu `issue_year` thì bắt backfill từ dòng ngày ban hành trước khi rename.
- Không quarantine/move văn bản cấp Bộ theo số hiệu trần; phải verify năm + chủ đề + nội dung, vì số hiệu cấp Bộ cũng có thể tái dùng theo năm.

### v1.17.15 VBHN hygiene/source-map guard
- Chuẩn hóa runtime số hiệu VBHN VPQH thiếu đoạn `VBHN`: `19-VPQH`/`40-VPQH` được xem như `19-VBHN-VPQH`/`40-VBHN-VPQH`.
- Sửa parser năm trong tên có underscore (`_2024_`, `_2026_`), tránh cảnh báo sai `VBHN_MISSING_YEAR_OR_DATE`.
- `hygiene` không còn gom VBHN theo số hiệu trần; tách theo số hiệu + năm/chủ đề/gốc/md5 để không quarantine nhầm các văn bản khác cùng số.
- Hạ điểm nguồn NLM rỗng metadata (`NLM_GHOST_SOURCE`) và tách file `.docx/.pdf` gốc cạnh GDoc thành `sidecar_source_files`, giảm báo động giả.
- Tài liệu chi tiết: `references/VBHN_HYGIENE_GUARDS.md`, `references/VBHN_MINISTRY_YEAR_GUARD.md`.


### v1.17.14 VBHN official-first gate
- Từ log ATVSLĐ: bản tự ghép VBHN có lỗi quy phạm ở Điều 53 và thiếu footnote; từ nay không tự ghép VBHN làm bản dùng.
- Thêm `tl vbhn-verify --official-required` và `tl vbhn-compare` để chặn/chứng minh khác biệt giữa bản chính thức và bản tạm.
- Quy trình khi thiếu VBHN: hỏi người dùng nạp file chính thức vào `_HOP_NAP`; nếu buộc dựng bản tạm để phân tích thì gắn provisional, không add NLM/canonical, và quarantine khi có bản chính thức.
- Tài liệu chi tiết: `references/VBHN_OFFICIAL_FIRST.md`.


### v1.17.13 VBHN QT-5 verification gate
- Hợp nhất bản `vbhn_qt5`: thêm `tl vbhn-check`, `tl vbhn-verify`, `tl vbhn-check --scan`.
- Giữ guard v1.17.12: `NO_VERIFIED_VBHN_IN_CORPUS`, `VBHN_NUMBER_REUSE_RISK`, `VBHN_BARE_NUMBER`, `VBHN_MISSING_YEAR_OR_DATE`.
- Quy trình bắt buộc với luật đã sửa đổi: `source-map → vbhn-check → vbhn-verify → mới chốt nguồn rà soát`.
- Tài liệu chi tiết: `references/VBHN_QT5_VERIFICATION.md`.


### v1.17.12 VBHN year/reuse guard
- Không kết luận "không có VBHN" từ manifest/corpus. Khi không thấy VBHN đã xác minh, `source-map` trả `NO_VERIFIED_VBHN_IN_CORPUS` + `QT5_WEB_REQUIRED` và gợi ý query theo trích yếu/chủ đề + "hợp nhất".
- Số VBHN có thể tái sử dụng theo năm; hit theo `14/VBHN-VPQH` phải verify ngày ban hành + tiêu đề + dòng "được sửa đổi, bổ sung bởi..." trước khi tin.
- `hygiene/registry-doctor` gắn `VBHN_BARE_NUMBER`, `VBHN_MISSING_YEAR_OR_DATE` cho VBHN tên trơ/thiếu năm, để bắt kiểu `VBHN_14-VBHN-VPQH`.


### v1.17.11 best-combined source-map
- Hợp nhất `source-map hotfix` với runtime-log hardening: `source-map` chọn VBHN liên quan qua trường `goc`, vẫn xuất `WARN`/`risky_candidates` từ `_title_flags`.
- `_entry_score` đồng bộ hơn với `registryRank_` 2.21.2b: cộng điểm VBHN như tiebreaker, trừ điểm bản hết hiệu lực/thay thế.
- Tài liệu chi tiết: `references/REALRUN_4LAWS_SOURCE_MAP_FIXES.md`.


### v1.17.10 post-run hardening
- Từ log chạy thật: `locate/hygiene/registry-doctor` nay phát hiện nhãn tên hẹp nhưng quan hệ sửa nhiều luật (`OMNIBUS_NARROW_TITLE_CHECK`) và mismatch tên-metadata, tránh chọn nhầm kiểu `Luat_57-2024-QH15_Bao_hiem_y_te`.
- `tl locate` nhận `--refresh/--debug`, ưu tiên manifest đầy đủ trước webapp `find` để thấy metadata/cờ cảnh báo.


### v1.17.9 hotfix
- Khép version post-deploy `2.21.2b` trong CLI/contract/SKILL/RUNBOOK.
- Thêm `requirements.txt` rỗng-phụ-thuộc để lệnh cài đặt trong tài liệu không lệch thực tế.
- `tl extract --find` tìm chuỗi sau Unicode NFC normalize, tránh âm tính giả khi grep tiếng Việt có dấu.
- `tl hygiene/reconcile` không parse tên `Mẫu_*/PL_*` thành số hiệu văn bản, tránh QUARANTINE nhầm phụ lục/biểu mẫu làm việc.


### v1.17.19 safe issue_year parser
- (Lịch sử) parser `issue_year` an toàn (từ bản 2.21.2d) — logic này tiếp tục được giữ trong `Code.2.21.2i.gs`.

### v1.17.20 registry hygiene parity
- Đồng bộ `registry_hygiene.py` với parser an toàn của `tl.py`: không lấy năm từ `tukhoa/keywords/trich_yeu`, tránh làm mất cờ `VBHN_MISSING_YEAR_OR_DATE` khi chạy hygiene độc lập.
- Tên VBHN phải chứa đúng năm ban hành đã xác định; năm của văn bản gốc trong tên/keyword không được coi là đạt.
- (Lịch sử v1.17.20) parser năm an toàn ở server-side; bản target/EXPECT hiện hành là `2.21.2i`.

### v1.17.21 lessons hardening
- Không dùng `reg_get name_contains` để kết luận văn bản vắng mặt; phải chạy ít nhất `tl source-map <tên/chủ đề>` và `tl locate/status <số hiệu>`.
- `_fallback/gas.py` cảnh báo khi gọi `reg_get name_contains`; `hygiene scan` có thêm `duplicate_identity_groups`, `duplicate_sohieu_groups_raw`, và cờ `NLM_STATUS_MISMATCH`.


