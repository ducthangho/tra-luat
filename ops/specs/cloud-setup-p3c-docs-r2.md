# Đặc tả packet `CLOUD-SETUP-P3C-DOCS` r2 (errata của r1): tài liệu theo webapp `2.21.2q` và đánh dấu `CODEX_AUTH_JSON` là đường cũ

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

| trường | giá trị |
|---|---|
| packet_id | `CLOUD-SETUP-P3C-DOCS`, revision 2 (errata của r1: chỉ sửa một vế của câu M3 và dòng S4 — mục `errata_r2` cuối tệp), generation 1 |
| packet_issue | #1224 |
| nguon_cap_viec | Chủ kho giao mục 2 ngày 04-11-2026 ("dọn các tài liệu còn nhắc CODEX_AUTH_JSON") trong phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4`; vòng hỏi 05-11 Q6 (chỉ tài liệu đang dùng, không gỡ code, không sửa hồ sơ lịch sử) và Q8(a) (tách khỏi #1223 theo trần ADR-0053) chủ kho trả "theo khuyến nghị" |
| review_class | `sensitive` — classifier `ops/lease_publish.py:58–66,360–382` mặc định `sensitive` cho đường dẫn không có trong bảng |
| base | `origin/master` lúc cấp lease |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run` (offline, ADR-0060 M12) + connector `@codex review` trên PR draft |
| luật merge | ADR-0060 mặc định theo ADR-0062 |
| windows | `not_required` — diff chỉ Markdown (ADR-0060 M3) |
| packet anh em | #1223 `CLOUD-SETUP-P3C-CONTRACT` — write set rời nhau; thứ tự land không ràng buộc |

## 1. Vì sao — số đo (05-11-2026, `origin/master` = `48d2665`)

| # | sự kiện | số đo |
|---|---|---|
| S1 | hướng dẫn tool dev cũ | `references/DEV_TOOLING_GUIDE.md:57` "hiện hành `references/Code.2.21.2p.gs`"; webapp LIVE đo 08:21Z là `2.21.2q` |
| S2 | mô tả gói sai sẵn | `references/DELTA_v1.19.md:8` "gói … chỉ kèm snapshot `.gs` của hai bản mới nhất (`2.21.2o`, `2.21.2p`)"; `RELEASE_MANIFEST.json` có ba: `references/Code.2.21.2o.gs`, `…2p.gs`, `…2q.gs` (Codex phản biện nêu, tôi đo lại) |
| S3 | `CODEX_AUTH_JSON` trong tài liệu đang dùng | `docs/GOI_AGENT_DA_NEN.md` 7 dòng (86, 116, 121, 145, 177, 220, 241); `CLAUDE.md` 4 dòng (673, 676, 683, 795). Không câu nào nói biến đã là đường cũ |
| S4 | đường hiện hành | hook phiên 05-11 in `CODEX_AUTH_JSON present=0` và `agent_creds: ĐÃ NẠP — rev=3; codex auth.json: giữ bản đĩa`; code ĐỌC giá trị biến VẪN CÒN ở hook phiên (`.claude/hooks/session_start.py:140`) và `.claude/dev/launcher.py:3646`; `.claude/dev/codex_cred.py` không đọc giá trị mà SINH base64 cho biến và GỠ biến khỏi môi trường con (`pop` ở dòng 130, 194) — errata r2. Số lần nhắc tên biến: `.claude/hooks/session_start.py` 7, `.claude/hooks/session-start.sh` 7, `.claude/dev/launcher.py` 13, `.claude/dev/codex_cred.py` 14 |

## 2. Thay đổi (mỗi mục chiếu vào một đường dẫn ở §3)

- **M1 → `references/DEV_TOOLING_GUIDE.md`**: dòng 57 "hiện hành `references/Code.2.21.2q.gs`".
- **M2 → `references/DELTA_v1.19.md`**: dòng 8 thành "ba bản mới nhất (`2.21.2o`, `2.21.2p`, `2.21.2q`)".
- **M3 → `docs/GOI_AGENT_DA_NEN.md`**: chèn đúng khối trích dẫn sau (nguyên văn; cách ngắt dòng tuỳ ý) ngay dưới tiêu đề
  `### Để không phải nhập mã lại mỗi phiên` (base dòng 82) và TRƯỚC đoạn bắt đầu `Container phiên remote là` (base dòng 84 —
  đoạn có lần nhắc `CODEX_AUTH_JSON` đầu tiên của mục trên base); câu chữ theo phản biện GPT 05-11:

  ```
  > **Đường cũ (05-11-2026).** `CODEX_AUTH_JSON` là cơ chế cấu hình cũ, không dùng cho thiết lập mới. Đường hiện
  > hành là `agent_creds`: P2b nạp credential lúc mở phiên, P3 ghi ngược khi `Stop`. Code vẫn còn đọc `CODEX_AUTH_JSON`
  > để tương thích (hook phiên, `.claude/dev/launcher.py`; `.claude/dev/codex_cred.py` còn sinh và gỡ biến); đường ấy
  > chưa gỡ, việc gỡ là packet riêng `CODEX-AUTH-JSON-GO-CODE`.
  ```

  Không xoá hay sửa các đoạn bên dưới (chúng kể lịch sử).
- **M4 → `CLAUDE.md`**: nối vào CUỐI gạch đầu dòng "Refresh token của codex XOAY VÒNG …" (base dòng 795) đúng câu sau (nguyên
  văn; ngắt dòng tuỳ ý):

  ```
  **Từ 05-11-2026 biến này là đường cũ**: `agent_creds` (P2b/P3) thay thế; code đọc biến vẫn còn để tương thích và
  chưa gỡ — xem khối đầu mục *Để không phải nhập mã lại mỗi phiên* trong `docs/GOI_AGENT_DA_NEN.md`.
  ```

  KHÔNG sửa dòng 673–683 (kể sự cố 15-08-2026, là lịch sử).
- **M5 → `changelog.d/wp-1224.md`**: ghi chú thay đổi.

## 3. Write set

```yaml
write_set:
  - CLAUDE.md
  - changelog.d/wp-1224.md
  - docs/GOI_AGENT_DA_NEN.md
  - ops/handoff/wp1224-g1-claude.md
  - references/DELTA_v1.19.md
  - references/DEV_TOOLING_GUIDE.md
```

Diff PR: đúng **5 tệp**. Dự kiến ≤ 25 dòng thêm. Trần `ADR-0053` (≤ 6 tệp / ≤ 450 dòng thêm): **đạt**.

`references/DEV_TOOLING_GUIDE.md` và `references/DELTA_v1.19.md` nằm trong `RELEASE_MANIFEST.json`; worker KHÔNG tái sinh manifest
và KHÔNG sửa `VERSION`/`CHANGELOG.md` (`docs/PROTOCOL_DA_PHIEN.md:855–865`). Phiên land tái sinh manifest trên head PR trước merge.
`CLAUDE.md` và `docs/**` không nằm trong manifest.

Trần lời gọi Codex: `ADR-0055` ⇒ cứng **10**; ngân sách mềm **2**.

## 4. Nghiệm thu

Phép đo chuỗi theo L6 của `soan-spec`: vế dương trên nội dung MỚI, vế âm trên nội dung CŨ, đếm từng tệp; với câu văn xuôi (M3, M4)
đo trên văn bản đã gộp khoảng trắng TRONG TỪNG ĐOẠN (không nối qua dòng trống), vì Markdown ngắt cột tuỳ người viết.

| ID | phép đo | đột biến làm ĐỎ |
|---|---|---|
| A1 | `DEV_TOOLING_GUIDE.md`: `2.21.2p` 0 lần trong dòng "hiện hành …", cụm `` hiện hành `references/Code.2.21.2q.gs` `` đúng 1 lần | để `2p` ⇒ ĐỎ |
| A2 | `DELTA_v1.19.md`: script lấy tập `references/Code.*.gs` trong `RELEASE_MANIFEST.json` của base và tập `.gs` liệt kê trong đoạn "Gói phát hành chỉ kèm snapshot …"; hai tập BẰNG nhau, và con số chữ ("ba") khớp lực lượng | xoá `2.21.2q` khỏi đoạn ⇒ ĐỎ; để chữ "hai" ⇒ ĐỎ |
| A3 | `docs/GOI_AGENT_DA_NEN.md`: khối trích dẫn của M3, sau khi bỏ tiền tố `> ` và gộp khoảng trắng trong đoạn, BẰNG ĐÚNG văn bản M3 (cũng gộp khoảng trắng), xuất hiện đúng 1 lần; nằm giữa dòng tiêu đề `### Để không phải nhập mã lại mỗi phiên` và đoạn bắt đầu `Container phiên remote là`, không có đoạn nào khác xen giữa | xoá BẤT KỲ một mệnh đề nào ("không dùng cho thiết lập mới" · "Đường hiện hành là `agent_creds`" · "Code vẫn còn đọc" · "đường ấy chưa gỡ") ⇒ ĐỎ (mỗi mệnh đề một đột biến); dời khối xuống cuối mục ⇒ ĐỎ |
| A4 | `CLAUDE.md`: câu M4 (gộp khoảng trắng) xuất hiện đúng 1 lần, nằm TRONG gạch đầu dòng bắt đầu `- **Refresh token của codex XOAY VÒNG` (trước gạch đầu dòng kế tiếp) | bỏ câu ⇒ ĐỎ; xoá vế "chưa gỡ" ⇒ ĐỎ; dời câu sang gạch đầu dòng khác ⇒ ĐỎ |
| A5 | vế âm cho cả hai tệp M3/M4: không đoạn nào vừa có `CODEX_AUTH_JSON` vừa có một trong các cụm "đã gỡ", "đã bỏ", "không còn hỗ trợ", "removed" mà không có phủ định "chưa"/"không" đứng ngay trước (phép đo theo đoạn) | thêm câu "code đọc CODEX_AUTH_JSON đã gỡ" ⇒ ĐỎ |
| A6 | `CLAUDE.md` dòng 673–683 của base giữ nguyên byte (so đoạn `git show <base>:CLAUDE.md` với ứng viên theo nội dung, không theo số dòng) | sửa đoạn sự cố 15-08 ⇒ ĐỎ |
| A7 | `git diff --numstat <base> <cand>`: đúng 5 tệp của write set (trừ handoff); không có `VERSION`, `CHANGELOG.md`, `RELEASE_MANIFEST.json` | thêm tệp thứ 6 ⇒ ĐỎ |
| A8 | bất biến (a): `git diff --check` rc 0; `doctrine-scan` rc 0; doc-claims-check như gate rc 0; `python scripts/tl.py --selftest` N/N | — |
| A9 (sau land, phiên land) | tái sinh `RELEASE_MANIFEST.json` trên head PR trước merge; gate master xanh gồm `release-verify strict (lane LAND)` | — |

Chạy thử trên base: A1–A4 ĐỎ đúng "chưa làm"; A5, A6 xanh sẵn (canh bất biến, răng từ đột biến). A9 `chưa đo được` cho tới khi land.

## 5. Ngoài phạm vi (nợ có tên)

- `CODEX-AUTH-JSON-GO-CODE`: gỡ đường code đọc `CODEX_AUTH_JSON` (`.claude/hooks/**`, `.claude/dev/launcher.py`,
  `.claude/dev/codex_cred.py` và test) — lane launcher, Windows bắt buộc. Packet riêng (Q6).
- Hồ sơ lịch sử (`ops/specs/**`, `ops/leases/**`, `ops/handoff/**`, `docs/incidents/**`, `docs/research/**`, `ops/prompts/**`,
  `ops/*.md` biên bản): không sửa.
- `CLAUDE.md` dòng 673–683: kể sự cố, giữ nguyên.
- Hợp đồng webapp/`tl.py`: packet anh em #1223.

## 6. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục.

## 7. `chua_do_duoc`

- Môi trường Codex Cloud / laptop có còn ai đặt `CODEX_AUTH_JSON` không: không đo được từ phiên này; tài liệu chỉ khuyến nghị, không
  khẳng định không ai dùng.

## `errata_r2`

- r1 đóng băng: blob `00c1890c90545408f3c846d8a46504ec4daf7206`, sha256 `3a44afd07c80a8362f79fdabb240a3c0a4d680fdea179d35807527ba55012aeb`
  (lease `wp1224-r1-g1-claude`, issuecomment-6654438925). r2 do phiên điều phối `session_015GtxraXfMD1t2FJLzzGDr4` soạn
  ngày 05-11-2026 theo finding P3 `F03` của lượt Codex offline 1 trên ứng viên `96aa2fe` (run `eb9f80d2`), chủ kho chọn (b)
  "ra đặc tả r2" ~10:20Z. Mọi chỗ khác giữ nguyên từng byte so với r1, trừ các mục dưới đây.
- **Tiêu đề, dòng `packet_id`:** r1 → r2, kèm con trỏ tới mục này.
- **M3 (khối trích dẫn nguyên văn):** r1 liệt kê `.claude/dev/codex_cred.py` là nơi "đọc `CODEX_AUTH_JSON` để tương thích";
  đo trên `c5a1c3d`, tệp ấy chỉ sinh base64 cho biến và `pop` biến khỏi môi trường con (dòng 130, 194), không đọc giá trị;
  nơi đọc là hook phiên (`.claude/hooks/session_start.py:140`) và `.claude/dev/launcher.py:3646`. r2 đổi đúng vế trong ngoặc
  thành "(hook phiên, `.claude/dev/launcher.py`; `.claude/dev/codex_cred.py` còn sinh và gỡ biến)". A3 so khối với văn bản
  M3 của r2.
- **S4:** cùng đính chính về vai trò của `codex_cred.py`; số lần nhắc tên biến giữ nguyên.
- **Không đổi:** write set, M1, M2, M4, M5, A1–A9, trần, `tran_*`, ngoài phạm vi.
