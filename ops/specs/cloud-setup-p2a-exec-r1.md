# Đặc tả packet — `CLOUD-SETUP-P2A-EXEC` (revision 1)

- `packet_id`: **CLOUD-SETUP-P2A-EXEC** · `packet_issue`: **#1038** (Issue cha #1008) · `revision`: **1** · trạng thái:
  **BẢN NHÁP — CHƯA ĐÓNG BĂNG.** Chỉ đóng băng sau bước LIVE (mục *Bước LIVE trước đóng băng*), vì mục tiêu 3 cần fileId thật.
  Băm `sha256` ghi trên Issue #1038 và PR khi đóng băng, không ghi trong tệp · soạn 30-10-2026, phiên
  `session_015GtxraXfMD1t2FJLzzGDr4`.
- `nguon_cap_viec`: chỉ thị trực tiếp của chủ kho (Issue cha #1008, chuỗi `cloud-setup`). P2 tách thành P2a/P2b (vòng 1 Q6);
  phạm vi P2a chốt qua ba vòng hỏi trong phiên nói trên (vòng 1 Q1–Q7 "đồng ý khuyến nghị cả bảy"; vòng 2 Q8–Q12 và vòng 3
  Q13–Q18 "đồng ý khuyến nghị cả sáu"). Không có dòng kế hoạch nào trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.
- `review_class`: **sensitive** — chạm ranh giới credential (đặt token vào môi trường tiến trình con) và hook
  `.claude/hooks/pretooluse_guard.py` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 09:17Z 30-10: `757bde56`). Mọi phép đo kích thước/delta đo so merge-base
  (`git diff origin/master...HEAD`).
- `nang_tran`: chủ kho đồng ý vòng 3 Q17 trong phiên nói trên (đồng ý cả sáu khuyến nghị Q13–Q18). Trần của packet này:
  **≤ 13 tệp / ≤ 450 dòng thêm** (thay `ADR-0053` CHỈ cho packet này — trần dòng giữ nguyên, trần tệp nâng vì các tệp cơ học
  mà mỗi lệnh `tl` mới kéo theo, đo trên P1: merge `09e05945` chạm 13 tệp). Vượt 450 dòng ⇒ bỏ bớt ca test phụ, KHÔNG xin
  nâng thêm. Neo nguyên văn lời duyệt vào Issue #1038 lúc đóng băng.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: nang_tran vòng 3 Q17 (≤ 13 tệp / ≤ 450 dòng thêm; thay ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)

(OID là commit LAND của `ADR-0052` và `ADR-0053`, cùng giá trị đặc tả P1 r4 đã đo; đo lại lúc đóng băng.)

## Vấn đề (một đoạn)

P1 (#1009, land `09e05945`) dựng tệp mã hoá `tl_agent_creds.enc` mang ba khoá `codex_auth`, `claude_oauth_token`,
`antigravity_api_key` (`scripts/tl_gws.py:1090`, đo 08:55Z 30-10). `bootstrap` chỉ ghi `auth.json` của Codex; token Claude và
khoá Gemini thì **chỉ báo tên** (`scripts/tl_gws.py:1249`), không đưa tới đâu cả. Hằng `AGENT_CREDS_FILEID` vẫn rỗng
(`scripts/tl_gws.py:1089`). Chủ kho chọn KHÔNG export hai khoá ấy vào môi trường chung của phiên (vòng 1 Q3, phương án C):
một lệnh mới giải mã trong bộ nhớ và đặt biến **chỉ cho đúng tiến trình con** cần nó.

## `write_set`

1. `scripts/tl_gws.py`
2. `scripts/tl_core/cli.py`
3. `scripts/tl.py` (chỉ sửa tập `_CREDS_LAZY_CMDS`)
4. `scripts/tl_core/command_registry.py` (chỉ thêm metadata cho `agent-creds-exec`)
5. `scripts/tl_core/command_registry_test.py` (chỉ sửa số đếm ratchet)
6. `references/golden/parser_surface.json` (chỉ tái sinh)
7. `references/golden/workflow_audit.json` (chỉ tái sinh)
8. `references/golden/tool_inventory_inventory_decision.json` (chỉ tái sinh)
9. `.claude/hooks/pretooluse_guard.py` (chỉ thêm `agent-creds-exec` vào `_TL_LENH_GHI`)
10. `.claude/hooks/pretooluse_guard_test.py` (chỉ sửa số đếm ghim `= 105` ở ca liên quan)
11. `scripts/tl_selftest.py`
12. `changelog.d/wp-1038.md`
13. `RELEASE_MANIFEST.json`

Mười ba tệp = trần (`nang_tran`). Tệp 4–10 là danh sách P1 r4 đã chứng minh mỗi lệnh `tl` mới kéo theo (đặc tả
`ops/specs/cloud-setup-p1-bundle-r4.md`, phần mở đầu: CI đỏ ở đúng các tệp ấy khi thiếu chúng). Đo 09:17Z 30-10 trên `757bde56`:
`command_registry_test.py` ghim `198` lệnh lá / `200` node; `pretooluse_guard_test.py:637-640` ghim `= 105` lệnh ghi;
manifest 193 tệp. Đo `ai-dang-giu` cho cả 13 đường dẫn lúc cấp lease (chưa đo — bản nháp).

## `ngoai_pham_vi`

| thứ | vì sao |
|---|---|
| Cài, cấu hình (`modelProvider: gemini`) và đo `agy` | P2b #1039 (vòng 3 Q14): chưa đo `agy` đọc settings ở đâu. |
| Nối `bootstrap` vào `.claude/hooks/session-start.sh`, `ops/codex_cloud_setup.sh` | P2b #1039 (vòng 1 Q4). |
| `references/RUNBOOK.md` | P2b #1039. |
| Export token Claude / khoá Gemini vào môi trường chung, ghi chúng ra tệp | Vòng 1 Q3 (C), vòng 2 Q8–Q9: chỉ tiến trình con thấy. |
| Đặt `GOOGLE_API_KEY` hay biến nào khác ngoài `GEMINI_API_KEY` | Vòng 3 Q18: P2b đo `agy` rồi mới thêm. |
| Bộ đệm tệp mã hoá hoặc bản giải mã | Vòng 3 Q16: tải mỗi lần gọi. |
| Ghi ngược `auth.json` (CAS), tải lại jar NLM khi 401 | P3. |
| Đổi khoá, tạo tệp thật, bật anyone-with-link | Bước LIVE của chủ kho TRƯỚC đóng băng (vòng 2 Q10), không phải mã của packet. |
| Kiểm độ mạnh `TL_MASTER_KEY` trong lệnh mới | Đường ĐỌC — luật Q11 của P1 (vòng 3 Q15). |
| Metadata/snapshot cho lệnh nào khác `agent-creds-exec` | Mở tệp cơ học chỉ cho đúng lệnh này. |

## `muc_tieu`

Mỗi dòng chiếu vào đúng một đường dẫn ở `write_set` (L2).

1. `scripts/tl_gws.py` — lệnh `agent-creds-exec`:
   - cú pháp `tl agent-creds-exec [--claude] [--gemini] -- <lệnh> [đối số…]`; không có cờ nào trong hai, hoặc không có lệnh sau
     `--` ⇒ rc 2, không tải, không chạy con;
   - fileId theo thứ tự `TL_AGENT_CREDS_FILEID` > hằng `AGENT_CREDS_FILEID` (cùng thứ tự `bootstrap` của P1); rỗng ⇒ rc 4;
   - tải bằng `_public_curl_bytes` MỖI lần gọi, giải mã bằng `TL_MASTER_KEY` trong bộ nhớ; không kiểm độ mạnh khoá (đường ĐỌC);
   - tải lỗi, thiếu `TL_MASTER_KEY`, giải mã lỗi, `schema != 1`, hoặc thiếu (hay rỗng) đúng khoá được yêu cầu ⇒ **rc 4 và
     KHÔNG chạy tiến trình con** (fail-close);
   - môi trường con = bản sao `os.environ` + `CLAUDE_CODE_OAUTH_TOKEN` (khi `--claude`) và/hoặc `GEMINI_API_KEY` (khi
     `--gemini`); môi trường của chính tiến trình `tl` KHÔNG đổi;
   - chạy con bằng danh sách argv, không `shell=True`; `argv[0]` resolve qua `shutil.which` (bẫy `codex.CMD` trên Windows —
     CLAUDE.md, mục `launcher.py run` không tự giải shim); không resolve được ⇒ rc 127, không chạy;
   - stdin/stdout/stderr thừa kế thẳng; trả nguyên rc của con;
   - không in giá trị credential ở bất kỳ nhánh nào; dòng chẩn đoán (stderr) chỉ nêu TÊN biến đã đặt.
2. `scripts/tl_core/cli.py` — parser `agent-creds-exec` với `--claude`, `--gemini` và phần lệnh còn lại sau `--`.
3. `scripts/tl_gws.py` — ghi fileId thật của `tl_agent_creds.enc` (từ bước LIVE) vào hằng `AGENT_CREDS_FILEID`. Giá trị:
   **ĐIỀN LÚC ĐÓNG BĂNG**.
4. `scripts/tl.py` — thêm `agent-creds-exec` vào `_CREDS_LAZY_CMDS` (lệnh không cần config webapp). Không đổi lệnh nào khác.
5. `scripts/tl_core/command_registry.py` — metadata cho `agent-creds-exec` theo khuôn dòng `agent-creds-set`; lệnh chạy một
   tiến trình tuỳ ý mang credential ⇒ `read_only=False`, có gate nếu `validate_registry` đòi (không thì `WRITE_CMD_NO_GATE`).
   Không sửa metadata lệnh khác.
6. `scripts/tl_core/command_registry_test.py` — số đếm ratchet 198→199 lệnh lá, 200→201 node (đúng số `compute_parser_coverage`
   đo trên head), kể cả dòng mô tả; không đổi logic ca.
7. `references/golden/parser_surface.json` — tái sinh bằng `TL_WRITE_PARSER_SURFACE=1 python scripts/tl.py --selftest`; diff chỉ
   được mang `agent-creds-exec`.
8. `references/golden/workflow_audit.json`, `references/golden/tool_inventory_inventory_decision.json` — tái sinh bằng
   `python scripts/tl.py golden-test --write`; `git diff -- references/golden/` chỉ được mang lệnh mới và số đếm tương ứng.
   Diff có thứ khác ⇒ DỪNG.
9. `.claude/hooks/pretooluse_guard.py` — thêm `agent-creds-exec` vào `_TL_LENH_GHI` (subagent PHẢI bị chặn: lệnh đặt credential
   vào tiến trình khác — vòng 2 Q8). Không sửa logic guard.
10. `.claude/hooks/pretooluse_guard_test.py` — số `= 105` → số `--kiem-bang` đo trên head (dự kiến 106); thêm
    `agent-creds-exec …` vào bộ ca deny cạnh `agent-creds-set --new` nếu ca ấy liệt kê lệnh. Không đổi logic ca.
11. `scripts/tl_selftest.py` — các ca ở `nghiem_thu`, hermetic: không mạng, không Drive; tải công khai thay bằng đồ giả GIỮ
    TRẠNG THÁI đếm lời gọi; tiến trình con là `sys.executable` chạy một script tạm in ra TÊN biến có mặt và băm giá trị.
12. `changelog.d/wp-1038.md` — fragment changelog.
13. `RELEASE_MANIFEST.json` — tái sinh sau khi các tệp thuộc manifest đổi nội dung.
14. CI hai nền: context bắt buộc ở tiêu chí L1 xanh trên Ubuntu (lượt PR) VÀ Windows (`workflow_dispatch`
    `runner_set=windows-only` trên cùng head) — chủ kho đòi "không còn lỗi trên Windows" cho chuỗi này (issuecomment-6495628501).

## `nghiem_thu`

Tiền tố ca `r1000_` (đo 09:17Z 30-10: số `r` lớn nhất trong `scripts/tl_selftest.py` là `r999`; đã có thì lấy số kế tiếp còn
trống và ghi handoff). Mỗi ca kèm đột biến đổi màu (L3), chạy trên BẢN SAO TẠM.

| # | mục tiêu | tiêu chí | phép đo làm ĐỎ (đột biến) |
|---|---|---|---|
| A1 | 1 | `r1000_exec_dat_bien_chi_cho_con`: `--claude --gemini -- <con>` ⇒ con thấy hai biến với ĐÚNG giá trị (so băm); `os.environ` của tiến trình `tl` sau lệnh KHÔNG có hai biến (nếu trước đó vắng) | gán `os.environ[...]` thay vì env của con ⇒ ĐỎ (vế môi trường cha) |
| A2 | 1 | `r1000_exec_chi_dat_khoa_duoc_yeu_cau`: chỉ `--gemini` ⇒ con có `GEMINI_API_KEY`, KHÔNG có `CLAUDE_CODE_OAUTH_TOKEN` (môi trường gốc không có) ; chỉ `--claude` ⇒ ngược lại | đặt cả hai bất kể cờ ⇒ ĐỎ |
| A3 | 1 | `r1000_exec_fail_close`: năm ca — tải lỗi · thiếu `TL_MASTER_KEY` · khoá sai · `schema` khác 1 · thiếu khoá được yêu cầu (và khoá rỗng) ⇒ mỗi ca rc 4 và con chạy **0** lần (đếm từng ca riêng — L6c) | đổi nhánh "thiếu khoá" thành chạy con không biến ⇒ ĐỎ |
| A4 | 1 | `r1000_exec_tra_nguyen_rc_con`: con thoát 0 và 7 ⇒ `tl` trả 0 và 7 | trả cố định 0 ⇒ ĐỎ |
| A5 | 1 | `r1000_exec_khong_in_gia_tri`: sentinel riêng cho từng khoá; stdout + stderr của `tl` ở MỌI nhánh (thành công, năm nhánh A3, rc 127) không chứa sentinel nào (đo từng sentinel riêng) | thêm `print` giá trị ở nhánh lỗi ⇒ ĐỎ |
| A6 | 1 | `r1000_exec_doi_so_sai`: không cờ nào ⇒ rc 2; không có lệnh sau `--` ⇒ rc 2; cả hai ⇒ tải công khai **0** lời gọi | bỏ kiểm "thiếu lệnh" ⇒ ĐỎ |
| A7 | 1 | `r1000_exec_khong_shell`: đối số con chứa `;`, `&&`, `$(…)` được con nhận NGUYÊN VĂN, không được shell diễn giải | đổi sang `shell=True` ⇒ ĐỎ |
| A8 | 1 | `r1000_exec_resolve_which`: tên trần resolve qua `shutil.which` (đồ giả `which` đếm lời gọi); tên không resolve được ⇒ rc 127, con 0 lần | dùng `argv[0]` thô ⇒ ĐỎ (đồ giả `which` 0 lời gọi) |
| A9 | 1 | `r1000_exec_env_thang_hang`: `TL_AGENT_CREDS_FILEID` đặt ⇒ đồ giả tải nhận đúng id của biến dù hằng khác rỗng | đảo thứ tự ⇒ ĐỎ |
| A10 | 1 | `r1000_exec_tai_moi_lan`: hai lần gọi liên tiếp ⇒ đồ giả tải đếm **2** | thêm bộ đệm (lần hai không tải) ⇒ ĐỎ |
| A11 | 1 | `r1000_exec_khong_ghi_dia`: trong suốt lời gọi (in-process, tiến trình con thay bằng đồ giả ghi nhận env), mọi lời gọi `builtins.open`/`io.open` ở chế độ ghi hoặc nối, `os.open` có cờ `O_WRONLY`/`O_RDWR`/`O_CREAT`, và `tempfile.mkstemp`/`NamedTemporaryFile`/`TemporaryFile`/`mkdtemp` được bọc bằng đồ giả ĐẾM lời gọi (vẫn chuyển tiếp) ⇒ tổng **0** lời gọi ghi; thêm vế sentinel: không tệp nào dưới HOME tạm, cwd tạm, `tempfile.gettempdir()` tạm (đặt `TMPDIR`/`TEMP`/`TMP` vào thư mục tạm của ca) chứa byte sentinel của khoá sau lời gọi. Phép đếm lời gọi bắt cả tệp tạm bị xoá trước lúc kiểm | đột biến ghi bản giải mã bằng `tempfile.NamedTemporaryFile(delete=True)` rồi đọc lại ⇒ ĐỎ (đếm 1); đột biến ghi bản mã hoá ra cwd ⇒ ĐỎ |
| B1 | 3 | `AGENT_CREDS_FILEID` khác rỗng và bằng đúng giá trị LIVE ghi ở Issue #1038 (khớp nguyên chuỗi; vế âm: trên base `757bde56` hằng rỗng) | để rỗng ⇒ ĐỎ |
| C1 | 2 | `tl agent-creds-exec --help` rc 0, chứa `--claude` và `--gemini` (vế âm: base chưa có lệnh) | xoá `add_parser("agent-creds-exec"…)` ⇒ ĐỎ |
| C2 | 4 | `r1000_exec_khong_goi_load_creds` — HAI vế, cả hai bắt buộc. **(a) Phép đo chính, không phụ thuộc máy:** gọi `main()` của `tl` in-process với `argv` `agent-creds-exec --claude -- <con>`, `load_creds` (tên tra ở `tl`) thay bằng đồ giả ĐẾM lời gọi rồi ném lỗi riêng ⇒ đồ giả đếm **0** lời gọi và rc 4 với thông báo của lệnh. **(b) CLI thật trong bản sao tạm:** chép `scripts/` sang thư mục tạm, cwd tạm, HOME tạm, không `TL_WEBAPP`/`TL_TOKEN`/`TL_MASTER_KEY`; TIỀN ĐIỀU KIỆN đo trực tiếp: mọi đường của `profile_env._config_candidates()` (cwd · gốc skill · `scripts/` · `~/.tra_luat_config.json` · `/tmp/tra_luat_config.json`, `scripts/tl_core/profile_env.py:58-69`) đều không tồn tại — có đường nào tồn tại (vd `/tmp/tra_luat_config.json` trên máy dev) thì vế (b) ĐỎ với thông báo nêu đường ấy, KHÔNG được tha hay bỏ qua; đạt tiền điều kiện ⇒ rc 4 với thông báo của lệnh, không phải thông báo thiếu credential webapp | bỏ lệnh khỏi `_CREDS_LAZY_CMDS` ⇒ ĐỎ ở vế (a) (đồ giả đếm 1) bất kể máy có config hay không |
| H1 | 5 | `python scripts/tl.py workflow-audit --strict --json` rc 0, `registry.issues == []` | xoá metadata lệnh ⇒ ĐỎ (`UNREGISTERED_PARSER_CMD`) |
| H2 | 7 | `r77a_parser_surface_matches_snapshot` ĐẠT không đặt `TL_WRITE_PARSER_SURFACE`; diff snapshot chỉ mang `agent-creds-exec` | khôi phục snapshot base ⇒ ĐỎ |
| H3 | 6 | `python scripts/tl_core/command_registry_test.py` rc 0 | trả số về 198 ⇒ ĐỎ |
| H4 | 8 | `golden-test --json` rc 0 `ok: true` và `determinism-audit --strict --json` rc 0 | khôi phục một golden về base ⇒ ĐỎ |
| H5 | 9, 10 | `python .claude/hooks/pretooluse_guard.py --kiem-bang` rc 0; `pretooluse_guard_test.py` đạt hết; một lệnh Bash `python scripts/tl.py agent-creds-exec --claude -- x` từ subagent ⇒ deny | gỡ lệnh khỏi `_TL_LENH_GHI` ⇒ ĐỎ |
| G1 | 11 | `python scripts/tl.py --selftest` trên Ubuntu VÀ Windows, `core.abbrev=7`: delta so base = 0 ca đỏ mới, mọi `r1000_*` ĐẠT. Nền 1758/1758 (đơn vị: ca selftest) — đo trên `09e05945` bởi job `gate` run 41017062295; đo lại trên base lúc cấp lease | một `r1000_*` đỏ, hay ca đạt trên base mà đỏ trên head ⇒ ĐỎ |
| J1 | 13 | `release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked` | sửa một byte tệp manifest sau tái sinh ⇒ ĐỎ |
| K1 | — | `ruff check --select F` trên các tệp `.py` của write set: delta so base = 0 | thêm tên chưa định nghĩa ⇒ ĐỎ |
| K2 | — | `git diff --numstat origin/master...HEAD` ⇒ ≤ 13 tệp và ≤ 450 dòng thêm (tổng mọi tệp) | vượt ⇒ ĐỎ; DỪNG hỏi chủ kho |
| L1 | 14 | Context bắt buộc như tiêu chí L1 của P1 r4 (đọc lại ma trận `ci.yml` lúc nghiệm thu; lệch thì theo `ci.yml`): Ubuntu lượt PR, Windows `workflow_dispatch` `runner_set=windows-only` trên CÙNG head; `skipped`/vắng ngoài hai ngoại lệ đã nêu ở P1 r4 ⇒ ĐỎ | một context bắt buộc đỏ do packet ⇒ ĐỎ |
| M1 | 1 (LIVE, sau land) | Trên laptop, với `TL_MASTER_KEY` mới và hằng đã land. Tiến trình gọi đo phải XOÁ `GEMINI_API_KEY` và `CLAUDE_CODE_OAUTH_TOKEN` khỏi môi trường CỦA CHÍNH NÓ trước khi gọi (biến User trên laptop vẫn giữ; chỉ tiến trình đo không thấy). Con là một script in sha256 của `os.environ.get('GEMINI_API_KEY','')`. Băm kỳ vọng do phiên đo tính riêng từ khoá đã nạp vào bundle ở bước LIVE 5 (đọc biến User, không in giá trị). (i) `agent-creds-exec --gemini -- <con>` ⇒ rc 0 và băm con in ra BẰNG băm kỳ vọng; (ii) đối chứng: chạy `<con>` trực tiếp từ cùng tiến trình đã xoá biến ⇒ băm của chuỗi rỗng — chứng minh giá trị ở (i) đến từ bundle chứ không từ môi trường kế thừa | chưa đo được tới khi chạy thật; vế (ii) chính là phản chứng "bỏ chèn biến" (không có chèn ⇒ băm rỗng ≠ kỳ vọng). Ai đo: phiên điều phối qua Desktop Commander, hỏi chủ kho trước |

C1 khớp chuỗi trên đầu ra `--help` (không phải Markdown — L6b không áp dụng), có vế âm trên base (L6a). A3, A5 đếm từng ca /
từng sentinel riêng (L6c); A11 đếm lời gọi ghi chứ không chỉ đọc trạng thái đĩa cuối lượt. Không có lời khai "N lời gọi" dạng chữ (L6d), không có lời khai "không cổng nào cưỡng chế" (L6e).

## Kích thước dự kiến

**Ước tính, chưa đo** (09:17Z 30-10), đối chiếu numstat P1 trên merge `09e05945`: `tl_gws.py` ~70, `cli.py` ~6, `tl.py` 1–2,
`command_registry.py` ~3, `command_registry_test.py` ~5, `parser_surface.json` ~2, hai golden ~25, guard ~1, test guard ~3,
selftest ~150, changelog ~8, manifest ~20 ⇒ **khoảng 300 dòng thêm trên 13 tệp**. Trần 13 tệp / 450 dòng. Lời gọi Codex theo
`ADR-0052` (8); hết chưa sạch ⇒ Review Rescue Checkpoint (`ADR-0037`).

## Bước LIVE trước đóng băng (chủ kho duyệt từng bước; phiên điều phối chạy qua Desktop Commander)

1. ✅ `git pull --ff-only` kho trên laptop → `757bde5` (30-10 ~09:10Z).
2. ✅ `tl secrets-keygen` → `C:\Users\admin\tl-work\tl_master_key_new.txt`, ACL chỉ `ASUS-LAPTOP\admin`; 43 ký tự / 31 khác nhau.
3. ☐ Mã hoá lại `tl_secrets.enc` bằng khoá mới: `secrets-stage` (KHÔNG phải `secrets-set` — `secrets-set` giải mã và mã hoá
   bằng cùng một khoá, `scripts/tl_gws.py:991-1035`), ghi đè tại chỗ `SECRETS_FILEID`. Trước đó kiểm (chỉ đọc) bundle trên
   Drive không có khoá nào mà config laptop thiếu.
4. ☐ Chủ kho đặt `CLAUDE_CODE_OAUTH_TOKEN` (`claude setup-token`) và `GEMINI_API_KEY` vào biến User trên laptop.
5. ☐ `tl agent-creds-set --new --codex --claude-token-env --antigravity-key-env` → fileId `F` (lệnh chỉ IN fileId, không lưu
   vào đâu — `scripts/tl_gws.py:1213`); bật anyone-with-link cho `F`; rồi kiểm bằng một tiến trình MỚI đặt
   `TL_AGENT_CREDS_FILEID=F` (chỉ trong tiến trình đó) và `TL_MASTER_KEY` mới: `bootstrap` ⇒ `agent_creds: ĐÃ NẠP` và
   `rev=1`. Không dựa vào hằng `AGENT_CREDS_FILEID` (còn rỗng tới lúc thi hành) hay vào một `TL_AGENT_CREDS_FILEID` có
   sẵn trong môi trường (có thể trỏ bundle cũ). `F` điền vào mục tiêu 3 và tiêu chí B1.
6. ☐ Cập nhật `TL_MASTER_KEY` (biến User laptop; chủ kho dán vào Claude Code web và Codex cloud).

## `hinh_dang_ke_thua`

`khong_ap_dung` — không khắc phục packet nào. Ghi chú từ P1 (#1009) cho người thi hành: P1 vượt trần ba lần vì write set thiếu
tệp cơ học (r2→r3→r4); packet này đã liệt kê sẵn các tệp ấy. Vòng review P1 chạm S5 (cùng hình dạng finding ba lượt) — chủ kho
đặt luật (a)+(c) ở issuecomment-6494782891; áp lại nếu tái diễn.

## `chua_do_duoc`

- FileId thật của `tl_agent_creds.enc` (mục tiêu 3, B1): có sau bước LIVE 5.
- `agy` có đọc `GEMINI_API_KEY` khi gọi qua `agent-creds-exec` không: chưa chạy thật (laptop có `agy`, container không) — P2b
  đo; M1 chỉ đo biến tới được tiến trình con.
- Hành vi của `CLAUDE_CODE_OAUTH_TOKEN` với `claude -p` thật: chưa đo; P2b đo khi nối setup.
- Tín hiệu (Ctrl-C) chuyển tiếp tới con trên Windows: không có ca hermetic đo được; ghi handoff nếu thấy lệch.
- Số dòng thật: đo lúc thi hành (K2).
- `ai-dang-giu` 13 đường dẫn, OID land ADR, nền selftest trên base: đo lại lúc đóng băng và lúc cấp lease (L5).
