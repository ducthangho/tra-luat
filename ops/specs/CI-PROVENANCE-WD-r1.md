# Đặc tả packet `CI-PROVENANCE-WD` r1: đo mốc Workflow definition §10.2.2 bằng workflow Actions chỉ đọc (P-B, phần 1)

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `CI-PROVENANCE-WD`, revision 1, generation 1 |
| packet_issue | ghi ở comment đầu của Issue mở cùng đặc tả này |
| nguon_cap_viec | packet kế nhiệm **B** của `ADR-0060` M11 (*"collector bốn mốc: phần còn lại của #899"*); `packet_sau` P-B của đặc tả `wp899-r4` (commit `8809f13`, dòng 27); nợ `P-B-CHUA-CO-ISSUE` trong `ops/land/pr945-wp899-land-evidence.yaml`. Chủ kho mở theo chỉ thị 31-10-2026 trong phiên `session_015GtxrYPjZCTZeRiazdssgq`: *"Mở packet B collector bốn mốc luôn"* |
| review_class | `sensitive` — thêm định nghĩa workflow (§8: *"workflow/CI authority"*) |
| base | `origin/master` lúc cấp lease (đo khi soạn: `9a03544`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run` (offline, neo SHA ứng viên) + connector `@codex review` trên PR draft |
| depends_on | `ADR-0060` đã land (`36d7c5d`) |

## 1. Vì sao — số đo (31-10-2026)

| # | sự kiện | số đo |
|---|---|---|
| S1 | `ops/ci_provenance.py` (P-A) | mốc Workflow definition **luôn** `not_measured`, lý do `graphql_bi_chan_trong_phien_claude; cho P-B` (dòng 34, 368) |
| S2 | GraphQL trong phiên web | HTTP 403 *"GitHub GraphQL is not available from Claude Code sessions"* (CLAUDE.md, đo trên 8 run) |
| S3 | đường hiện dùng | chủ kho chạy `gh api graphql` tay rồi dán output, hoặc phiên chạy `gh` trên máy Windows của chủ kho qua Desktop Commander (tiền lệ `bccb97c`; packet #1085 đo run `41218603332` theo đường này lúc 16:15Z) |
| S4 | hệ quả | PR "duyệt landed" riêng (#949, #951, #953, #956); `landed: true` chờ người |

## 2. Thay đổi

Chỉ phần **mốc Workflow definition**. Phần *"tái hiện logic chế độ của sổ đăng ký"* của P-B **không** thuộc packet này.

1. **`ops/ci_provenance.py`**
   - Lệnh mới `do-wd --repo o/r --run ID --out TỆP`. Lệnh gọi GraphQL `node(id)` → `WorkflowRun { databaseId file { path repositoryFileUrl } checkSuite { commit { oid } } }`, với `node_id` lấy từ REST `actions/runs/ID`. Sau đó tải blob tại OID trong `repositoryFileUrl` qua REST `contents/<path>?ref=<OID>` (raw), rồi tính **git blob OID** (`sha1("blob <n>\0"+bytes)`) và **sha256** của bytes.
   - Ghi JSON vào `--out`: `{run_id, node_id, run_number, created_at, path, repository_file_url, oid, blob, sha256, trang_thai, ly_do?}`.
   - Mọi lời gọi mạng đi qua hàm tiêm `goi`, đúng như P-A, để test chạy offline. Token đọc từ biến `GH_TOKEN` hoặc `GITHUB_TOKEN`; không in token.
   - Ba trạng thái theo §10.2.3:
     - `passed` khi mọi điều sau đều đúng: `databaseId` bằng `--run`; `repositoryFileUrl` khớp đúng mẫu `https://github.com/<repo>/blob/<oid40>/<path>`; `<repo>` bằng `--repo`; `<path>` bằng `file.path` và bằng `path` của REST run; `<oid40>` bằng `checkSuite.commit.oid` và bằng `head_sha` của REST run; tải được blob.
     - `not_measured` khi `file` là null, GraphQL trả `errors`, HTTP khác 2xx, hoặc URL không chứa OID 40 hex (ví dụ chỉ chứa tên ref).
     - `failed` khi bất kỳ phép so nào ở trên lệch.
   - Mã thoát: 0 khi `passed`; 12 khi `failed`; 2 khi sai đối số; 3 khi REST hoặc GraphQL trả khác 2xx (trạng thái `not_measured`).
   - Lệnh `thu` nhận thêm `--wd TỆP`: nếu tệp là JSON do `do-wd` sinh, cùng `run_id`, `trang_thai: passed`, thì mốc `workflow_definition` lấy từ tệp; ngược lại giữ `not_measured` như cũ, kèm lý do. Không có `--wd` thì hành vi của P-A **giữ nguyên từng byte**.
2. **`.github/workflows/ops-do-workflow-definition.yml` (mới)**
   - Chỉ có `on: workflow_dispatch`, một input `run_id` kiểu chuỗi.
   - `permissions: {contents: read, actions: read}`, không quyền nào khác.
   - Một job `ubuntu-latest`: checkout nhánh mặc định (mã canonical, không bao giờ checkout ref do input chỉ định); chạy `python ops/ci_provenance.py do-wd --repo "$REPO" --run "$RUN_ID" --out wd.json`, với `RUN_ID` và `REPO` truyền qua `env:`, **không** nội suy biểu thức Actions vào thân `run:`; in `wd.json` ra log và step summary; tải `wd.json` lên làm artifact `workflow-definition-<run_id>`.
   - Không ghi Issue, PR hay kho. Không dùng secret nào ngoài `GITHUB_TOKEN`.
   - Không viết cú pháp biểu thức Actions trong chú thích của `run:` (bài học `ops-don-ref.yml`).
3. **`ops/ci_provenance_test.py`** — thêm các ca offline, xem §4 A2–A7.
4. **`.claude/skills/land-packets/SKILL.md`** — mục *"Mốc Workflow definition khi phiên không gọi được GraphQL"* thêm đúng một câu trỏ tới đường mới: gọi workflow qua MCP `actions_run_trigger`, đọc kết quả bằng `get_job_logs` hoặc artifact. Giữ nguyên đường cũ làm dự phòng; 0 dòng xoá.

## 3. Write set
`ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.github/workflows/ops-do-workflow-definition.yml` (planned) ·
`.claude/skills/land-packets/SKILL.md`. Bốn tệp, trần `sensitive` ≤ 6 tệp / ≤ 450 dòng thêm.

## 4. Nghiệm thu

| # | tiêu chí | phép đo làm nó ĐỎ |
|---|---|---|
| A1 | `python ops/ci_provenance_test.py` N/N, hai số bằng nhau; mọi ca P-A cũ vẫn đạt | xoá nhánh `--wd` ⇒ ca A6 đỏ |
| A2 | ca `wd_passed`: GraphQL và REST giả khớp nhau ⇒ `passed`, `blob` bằng `git hash-object` của bytes, `sha256` đúng | đột biến tính blob bằng sha1 thuần (không header `blob <n>\0`) ⇒ đỏ |
| A3 | ca `wd_file_null`, `wd_graphql_errors`, `wd_http_403`, `wd_url_ref_khong_oid` ⇒ `not_measured`, rc 3 hoặc 0 theo hợp đồng, không bao giờ `passed` | đột biến coi URL có tên ref là hợp lệ ⇒ `wd_url_ref_khong_oid` đỏ |
| A4 | ca lệch: `repo` khác, `path` khác `file.path`, OID trong URL khác `checkSuite.commit.oid`, OID khác `head_sha` của REST, `databaseId` khác `--run` ⇒ `failed`, rc 12. Mỗi phép so có một ca riêng | gỡ từng phép so ⇒ đúng ca của nó đỏ; năm đột biến, năm ca |
| A5 | ca `wd_sai_doi_so`: `--run` không phải số nguyên dương, `--repo` sai dạng ⇒ rc 2 | — |
| A6 | ca `thu_voi_wd`: `thu --wd` nhận JSON `passed` cùng `run_id` ⇒ mốc `passed`; JSON khác `run_id`, hoặc `trang_thai` khác `passed` ⇒ giữ `not_measured`; không có `--wd` ⇒ `provenance.yaml` y hệt bản P-A trên cùng dữ liệu giả | đột biến nhận JSON khác `run_id` ⇒ đỏ |
| A7 | ca `workflow_tinh` (đọc chính tệp YAML): `on` chỉ có `workflow_dispatch`; `permissions` đúng `{contents: read, actions: read}`; không có `${{` trong bất kỳ thân `run:` nào; bước chạy gọi đúng `python ops/ci_provenance.py do-wd`; không có bước `uses:` nào ngoài `actions/checkout` và `actions/upload-artifact`; checkout không có `ref:` lấy từ input | đột biến thêm `pull-requests: write`, hoặc chèn `${{ inputs.run_id }}` vào thân `run:` ⇒ đỏ |
| A8 | `actionlint .github/workflows/ops-do-workflow-definition.yml` rc=0 (cần `shellcheck` để đo đủ; thiếu thì ghi rõ) | — |
| A9 | `git diff --numstat`: đúng bốn tệp của §3, ≤ 450 dòng thêm; `land-packets/SKILL.md` +1/−0 | chạm tệp thứ năm |
| A10 | Windows theo `ADR-0060` M3: `required` (chạm `.github/workflows/**` và `ops/*.py`). Hai lượt nền và ứng viên trên máy Windows của chủ kho: A1 và A8 | ca đỏ có ở ứng viên mà không có ở nền |
| A11 | `full_mutant_audit` theo `ADR-0060` M9: **bắt buộc**, vì diff chạm `ops/**/*.py` và `.github/workflows/**` | thiếu receipt khi merge |
| A12 | **Canary sau land** (đo được khi và chỉ khi workflow có trên nhánh mặc định): gọi workflow cho run `41218603332` ⇒ JSON `passed`, `blob` `82d9f239ff311bd1ba3d3021119b5a2f7f699ffc`, `sha256` `ce9a3ec0f777a5165477c73b8fc9b9c098e8c3a9f5517c7499649670e84913fb` (khớp số đo tay ở S3) | lệch ⇒ ĐỎ; GraphQL từ chối `GITHUB_TOKEN` ⇒ `KHÔNG ĐO ĐƯỢC`, packet chưa `landed` |

## 5. Ngoài phạm vi
- Phần *"tái hiện logic chế độ của sổ đăng ký"* (marker Gate) của P-B: packet sau.
- Tự động gắn kết quả vào hồ sơ land hay bản ghi sổ trên Issue: packet C hoặc D của `ADR-0060` M11.
- Sửa `ci.yml` và chú thích dòng 869.

## 6. `chua_do_duoc`
- `GITHUB_TOKEN` với `actions: read` có đọc được `WorkflowRun.file` qua GraphQL không: chỉ đo được ở canary A12, sau land. Nếu không đọc được thì workflow trả `not_measured` (rc 3), không đỏ giả và không xanh giả. Khi ấy packet ở trạng thái merged, chưa `landed`.
- Thời lượng `full_mutant_audit` (A11) trên ứng viên: ước tính trong kho khoảng 2,6 giờ mỗi mảnh, chưa đo cho packet này. Chủ kho có thể miễn theo `ADR-0060` M1, M9.
- Thời lượng A10 trên Windows: chưa đo cho `ci_provenance_test.py`.

## 7. hinh_dang_ke_thua
Kế thừa từ `wp899-r4`, bài học của P-A: *mọi lời gọi mạng qua một hàm tiêm*; *thiếu dữ liệu là `not_measured`, không bao giờ `passed`*; *năm trạng thái §10.2.3*. Không có lớp finding mở nào được chuyển sang.
