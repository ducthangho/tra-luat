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
   - **Lệnh mới `do-wd --repo o/r --run ID --out TỆP`.**
     - Đọc REST `actions/runs/ID` để lấy `node_id`, `event`, `head_sha`, `path`, `run_attempt`.
     - Gọi GraphQL `node(id)` → `WorkflowRun { databaseId file { path repositoryFileUrl } checkSuite { commit { oid } } }`.
     - Tải blob tại OID trong `repositoryFileUrl` qua REST `contents/<path>?ref=<OID>` (raw), rồi tính **git blob OID** (`sha1("blob <n>\0"+bytes)`) và **sha256**.
     - Mọi lời gọi mạng đi qua hàm tiêm `goi`, như P-A. Token đọc từ `GH_TOKEN` hoặc `GITHUB_TOKEN`; không bao giờ in token.
   - **OID định nghĩa** là OID trong `repositoryFileUrl` đã xác minh, và chỉ lấy từ đó (protocol §10.2.2: *"Không đồng nhất REST run head với … workflow-definition SHA"*). `head_sha` của REST và `checkSuite.commit.oid` được ghi thành **trường riêng**, không bắt buộc bằng OID định nghĩa. Riêng run có `event` thuộc `{push, workflow_dispatch, schedule}`, ba giá trị này phải bằng nhau, lệch thì `failed`. Mọi `event` khác (`pull_request`, `pull_request_target`, …) chỉ ghi lại, không so.
   - **Điều kiện `passed`** (mọi điều phải đúng):
     - `databaseId` bằng `--run`;
     - `repositoryFileUrl` khớp đúng mẫu `^https://github.com/<repo>/blob/<oid40>/<path>$`;
     - `<repo>` bằng `--repo`;
     - `<path>` bằng `file.path` và bằng `path` của REST run;
     - quan hệ OID theo `event` như trên;
     - tải được blob, có đủ `blob` và `sha256`.
   - **Bảng trạng thái và mã thoát.** Mỗi đầu vào cho đúng một kết quả. JSON luôn được ghi khi đã đọc được REST run, kể cả lúc `not_measured` hay `failed`.

     | đầu vào | trạng thái | rc | `ly_do` |
     |---|---|---|---|
     | đủ điều kiện `passed` | `passed` | 0 | — |
     | phép so lệch (repo, path, `databaseId`, OID theo `event`) | `failed` | 12 | tên phép so lệch |
     | REST run khác 2xx | `not_measured` (JSON tối thiểu) | 3 | `rest_run_<mã>` |
     | GraphQL HTTP khác 2xx | `not_measured` | 3 | `graphql_http_<mã>` |
     | GraphQL 200 có `errors` (kể cả khi có dữ liệu một phần) | `not_measured` | 3 | `graphql_errors` |
     | `node` null, `file` null, hoặc `checkSuite` null | `not_measured` | 3 | `node_null`, `file_null`, `checksuite_null` |
     | URL không chứa OID 40 hex | `not_measured` | 3 | `url_khong_oid` |
     | thân phản hồi không phải JSON, hoặc thiếu trường bắt buộc | `not_measured` | 3 | `phan_hoi_hong` |
     | tải blob khác 2xx | `not_measured` | 3 | `blob_http_<mã>` |
     | sai đối số | `not_measured` (JSON tối thiểu, nếu `--out` đọc được) | 2 | `sai_doi_so` |

   - **JSON đầu ra** (schema cố định, `schema: wd/1`):
     `{schema, repo, run_id, run_attempt_luc_do, event, node_id, run_number, created_at, path, repository_file_url, oid_dinh_nghia, head_sha_rest, check_suite_commit, blob, sha256, trang_thai, ly_do, loi_graphql, nguon: "ops/ci_provenance.py do-wd"}`.
     `loi_graphql` là danh sách `{path, type, message}` lấy từ `errors[]`. `message` đã lọc chuỗi giống token (`gh[pousr]_…`, `github_pat_…`) và cắt ở 300 ký tự.
     **JSON tối thiểu** (cho rc 2/3 khi chưa có dữ liệu) có `{schema, repo?, run_id?, trang_thai: not_measured, ly_do}`. Collector **luôn** ghi JSON khi `--out` đọc được. Bước workflow ghi thêm một JSON dự phòng `{schema: wd/1, trang_thai: not_measured, ly_do: collector_khong_ghi_rc_<rc>}` khi collector không ghi được tệp nào. Nhờ vậy `wd.json` luôn tồn tại để in và tải lên.
     Mốc Workflow definition là trường **của run**, không phải của attempt: `WorkflowRun.file` không có attempt. `run_attempt_luc_do` chỉ ghi lại attempt lúc đo.
   - **`thu --wd-run WD_RUN_ID`.** Không nhập tệp do người đưa vào. `thu` tự lấy bằng chứng qua REST rồi kiểm theo thứ tự:
     - (a) `actions/runs/WD_RUN_ID`: `path` bằng `.github/workflows/ops-do-workflow-definition.yml`, `head_branch` bằng nhánh mặc định, `event` bằng `workflow_dispatch`, `conclusion` là `success`, cùng repo;
     - (b) đúng **một** artifact tên `workflow-definition-<run>` (với `<run>` là `--run` của `thu`), `expired: false`; tải zip, sha256 của zip bằng `digest` của artifact;
     - (c) trong zip có đúng một tệp `wd.json`, đúng schema `wd/1`, `repo`/`run_id` bằng đối số, `path` bằng `path` của REST run trong lần `thu`, `trang_thai: passed`;
     - (d) **tính lại**: tải blob tại `oid_dinh_nghia` qua REST `contents?ref=` rồi tính lại blob và sha256, phải bằng giá trị trong `wd.json`; `repository_file_url` dựng lại từ `repo`/`oid`/`path` phải bằng giá trị trong `wd.json`; với `event` thuộc `{push, workflow_dispatch, schedule}`, `oid_dinh_nghia` phải bằng `head_sha` của REST run.
     - Sai ở bước nào ⇒ mốc giữ `not_measured` với `ly_do: wd_khong_hop_le:<bước>:<trường>`. Đạt cả bốn ⇒ mốc `passed`, ghi kèm `wd_run_id`, `artifact_id` và `artifact_sha256`.
     - Không có `--wd-run` thì hành vi của P-A **giữ nguyên từng byte**.
     - Giới hạn tin cậy: (a)–(c) neo bằng chứng vào một lượt workflow trên nhánh mặc định do GitHub ghi lại; không chứng minh gì thêm về người bấm chạy.
2. **`.github/workflows/ops-do-workflow-definition.yml` (mới)**
   - Chỉ có `on: workflow_dispatch`, một input `run_id` kiểu chuỗi.
   - `permissions: {contents: read, actions: read}` ở mức workflow. Job không khai `permissions` riêng.
   - Một job `ubuntu-latest` gồm các bước:
     - `actions/checkout` với `ref: master` (chuỗi cố định) và `persist-credentials: false`;
     - cài `PyYAML==6.0.3`, cùng bản ghim mà `t31` kiểm;
     - một bước `run:` duy nhất chạy collector, lưu `rc`, ghi JSON dự phòng nếu `wd.json` chưa có, in `wd.json` ra log và `$GITHUB_STEP_SUMMARY` **kể cả khi rc khác 0**, rồi `exit` đúng mã đó;
     - `actions/upload-artifact` với `if: always()` và `path: wd.json`, chỉ tệp này.
   - `RUN_ID`, `REPO` và `GH_TOKEN` truyền qua `env:` của bước collector (`GH_TOKEN` lấy từ token của chính lượt chạy, không phải secret nào khác). Thân `run:` không chứa `${{`, không có `eval`, và chỉ gồm đúng các lệnh nêu ở trên.
   - Không ghi Issue, PR hay kho. Không dùng secret nào ngoài `GITHUB_TOKEN`. Không viết cú pháp biểu thức Actions trong chú thích.
3. **`ops/ci_provenance_test.py`** — thêm các ca offline của §4. Có thêm một đường đột biến **YAML**: test đọc workflow thật, áp từng đột biến lên bản sao trong bộ nhớ, rồi chạy lại kiểm tĩnh. Ngoài ra chạy **chính thân `run:`** của workflow bằng `bash`, với một `python` giả ghi lại argv, để đo binding biến và đường đi khi `rc` khác 0.
4. **`.claude/skills/land-packets/SKILL.md`** — mục *"Mốc Workflow definition khi phiên không gọi được GraphQL"* thêm đúng một câu trỏ tới đường mới: gọi workflow qua MCP `actions_run_trigger`, đọc kết quả bằng `get_job_logs` hoặc artifact. Giữ nguyên đường cũ làm dự phòng; 0 dòng xoá.

## 3. Write set
`ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.github/workflows/ops-do-workflow-definition.yml` (planned) ·
`.claude/skills/land-packets/SKILL.md`. Bốn tệp, trần `sensitive` ≤ 6 tệp / ≤ 450 dòng thêm.
`ops/ci_provenance_test.py` đã có trong sổ `MOI` của `.claude/dev/ci_dang_ky_test.py` (dòng 57); workflow mới không phải test
nên không cần đăng ký.

## 4. Nghiệm thu (mỗi dòng: ca, và đột biến làm nó ĐỎ)

| # | tiêu chí | đột biến làm ĐỎ |
|---|---|---|
| A1 | `python ops/ci_provenance_test.py` N/N, hai số bằng nhau; mọi ca P-A cũ vẫn đạt | xoá nhánh `--wd-run` ⇒ A6 đỏ |
| A2 | `wd_passed` (event `push`): `passed`, `blob` bằng `git hash-object` của bytes, `sha256` đúng | (a) blob tính bằng sha1 thuần; (b) sha256 tính trên bytes đã bỏ dòng cuối ⇒ mỗi đột biến một vế đỏ |
| A3 | Mỗi dòng `not_measured` của bảng ở §2.1 là một ca, đòi **đúng** rc và `ly_do` ghi trong bảng | đột biến coi URL có tên ref là hợp lệ ⇒ `url_khong_oid` đỏ; đột biến bỏ kiểm `errors` khi có dữ liệu một phần ⇒ `graphql_errors` đỏ; ca `graphql_errors_hai_field` (một lỗi ở `file`, một ở `checkSuite`) ⇒ `loi_graphql` giữ đủ hai `path` khác nhau, đột biến gộp lỗi thành chuỗi ⇒ đỏ; ca rc 2 và `rest_run_404` ⇒ JSON tối thiểu được ghi |
| A4 | Mỗi phép so có một ca `failed` riêng, rc 12, `ly_do` đúng tên: `repo`, `url_path≠file.path`, `file.path≠REST path` (URL và `file.path` khớp nhau nhưng REST khác), `databaseId`, `oid≠head_sha` (event `push`), `oid≠check_suite` (event `push`) | gỡ từng phép so ⇒ đúng ca của nó đỏ; sáu đột biến, sáu ca |
| A4b | Ca dương `pull_request_synthetic` và `pull_request_target`: OID định nghĩa khác `head_sha` và khác `check_suite_commit` ⇒ vẫn `passed` | đột biến so OID với mọi `event` ⇒ đỏ |
| A5 | `wd_sai_doi_so`: `--run` không phải số nguyên dương, hoặc `--repo` sai dạng ⇒ rc 2, không ghi tệp | đột biến chấp nhận `--run 0` ⇒ đỏ |
| A6 | `thu --wd-run`, với REST và artifact giả: bằng chứng hợp lệ ⇒ `passed`, ghi đủ `wd_run_id`/`artifact_id`/`artifact_sha256`. Mỗi bước sai một ca, giữ `not_measured` với `wd_khong_hop_le:<bước>`: run không phải workflow này; nhánh khác nhánh mặc định; `event` khác `workflow_dispatch`; không có artifact hoặc có hai artifact; digest zip lệch; `wd.json` tối giản; **JSON đầy đủ, hash đúng độ dài, cùng repo/run/path, `passed`, nhưng `blob` hoặc `sha256` bị giả** (tính lại lệch); URL giả; OID khác `head_sha` với event `push`. Không có `--wd-run` ⇒ `provenance.yaml` y hệt bản P-A trên cùng dữ liệu giả | đột biến bỏ bước (d) tính lại ⇒ ca hash giả đỏ; đột biến bỏ kiểm digest ⇒ ca digest lệch đỏ; đột biến bỏ kiểm nhánh ⇒ ca nhánh khác đỏ |
| A7 | Kiểm tĩnh trên chính tệp YAML (mọi job, mọi bước): `on` chỉ có `workflow_dispatch`; quyền hiệu lực đúng `{contents: read, actions: read}`, không job nào khai quyền riêng; checkout có `ref: master` cố định và `persist-credentials: false`; chỉ hai `uses:` (`actions/checkout`, `actions/upload-artifact`); upload `path` đúng `wd.json`; không có `${{` và `eval` trong thân `run:`; bước collector có `env.GH_TOKEN` lấy từ token của lượt chạy và token **không** xuất hiện trong thân `run:`; lời gọi collector nằm trong dòng lệnh thật (không phải chú thích), ở bước không bị `if:` tắt | mỗi đột biến YAML một ca đỏ: thêm `pull-requests: write` ở job; bỏ `ref`; đổi `ref` thành `${{ github.sha }}`; bỏ `persist-credentials`; thêm `eval "$RUN_ID"`; đổi upload `path` thành `.`; chuyển lời gọi collector vào chú thích; bỏ `GH_TOKEN` khỏi `env` |
| A7b | Chạy thân `run:` bằng `bash` với `python` giả. Với `RUN_ID='1; touch PWNED'`: argv phải chứa `--run` theo sau bởi **đúng một** đối số bằng nguyên chuỗi đó; điều kiện an toàn đi kèm là không có tệp `PWNED`. Python giả trả rc 3 và **không ghi** `wd.json` ⇒ bước vẫn ghi JSON dự phòng, in vào summary, rồi thoát rc 3 | đột biến bỏ nháy quanh `"$RUN_ID"` ⇒ argv tách thành `1;` `touch` `PWNED` ⇒ assertion một-đối-số đỏ; đột biến bỏ JSON dự phòng ⇒ không có `wd.json` ⇒ đỏ; đột biến thoát trước khi in summary ⇒ đỏ |
| A8 | `actionlint` trên tệp mới rc=0, đo khi có `shellcheck`; thiếu `shellcheck` thì ghi `KHÔNG ĐO ĐỦ`, không tính đạt | ca phụ: một bản YAML vẫn parse được nhưng sai hợp đồng Actions (`on: workflow_dispatch` với `inputs.run_id.type: number123`) ⇒ actionlint rc≠0 |
| A9 | `git diff --numstat <base_oid> <candidate_oid>` sau khi đóng băng: đúng bốn tệp của §3, ≤ 450 dòng thêm; `land-packets/SKILL.md` +1/−0. Trước khi đóng băng, kiểm riêng các trạng thái staged, unstaged và untracked | thêm tệp thứ năm ở mỗi trạng thái ⇒ đỏ |
| A10 | Windows theo `ADR-0060` M3 (bước 2: chạm `.github/workflows/**`): **nền** chạy `ci_provenance_test.py` (tập test ID và kết quả); **ứng viên** chạy `ci_provenance_test.py` cùng A8 trên tệp mới. Áp đủ M3 (a)–(c): hai lượt chạy trọn, so tập test ID đỏ, ca đỏ thuộc write set thì chủ kho quyết. Nền không có tệp workflow mới, nên A8 chỉ đo trên ứng viên và **không** dùng lỗi "không có tệp" ở nền làm mốc | ca đỏ có ở ứng viên mà không có ở nền ⇒ ĐỎ |
| A11 | `full_mutant_audit` theo `ADR-0060` M9: **bắt buộc** (diff chạm `.github/workflows/**` và `ops/**/*.py`). Bỏ qua chỉ khi có waiver `owner_waived` đúng scope theo §10.2.3 | thiếu receipt hoặc waiver khi merge |
| A12 | **Canary sau land**, đo được khi và chỉ khi workflow có trên nhánh mặc định: gọi workflow cho run `41218603332` ⇒ `passed`, `oid_dinh_nghia` `634d5a28973cd2f39175283b45fb820c5b0819e5`, `blob` `82d9f239ff311bd1ba3d3021119b5a2f7f699ffc`, `sha256` `ce9a3ec0f777a5165477c73b8fc9b9c098e8c3a9f5517c7499649670e84913fb` (khớp số đo tay ở S3) | lệch ⇒ ĐỎ; `GITHUB_TOKEN` bị từ chối ở GraphQL ⇒ `KHÔNG ĐO ĐƯỢC` kèm `ly_do` theo endpoint/field, packet chưa `landed` |

## 5. Ngoài phạm vi
- Phần *"tái hiện logic chế độ của sổ đăng ký"* (marker Gate) của P-B: packet sau.
- Tự động gắn kết quả vào hồ sơ land hay bản ghi sổ trên Issue: packet C hoặc D của `ADR-0060` M11.
- Sửa `ci.yml` và chú thích dòng 869.

## 6. `chua_do_duoc`
- `GITHUB_TOKEN` với `actions: read` có đọc được `WorkflowRun.file` qua GraphQL không: chỉ đo được ở canary A12, sau land. Nếu không đọc được thì workflow trả `not_measured` (rc 3), không đỏ giả và không xanh giả. Khi ấy packet ở trạng thái merged, chưa `landed`.
- Thời lượng `full_mutant_audit` (A11) trên ứng viên: ước tính trong kho khoảng 2,6 giờ mỗi mảnh, chưa đo cho packet này. Bỏ qua chỉ khi có waiver `owner_waived` đúng scope theo protocol §10.2.3.
- Thời lượng A10 trên Windows: chưa đo cho `ci_provenance_test.py` (trên Linux bộ này chạy quá 10 phút, đo 31-10).
- Quyền `contents: read` + `actions: read` có đủ cho cả trường `checkSuite` của GraphQL không: chỉ đo được ở A12; thiếu quyền thì ghi `ly_do` theo field, không tự thêm quyền.

## 7. hinh_dang_ke_thua
Kế thừa từ `wp899-r4`, bài học của P-A: *mọi lời gọi mạng qua một hàm tiêm*; *thiếu dữ liệu là `not_measured`, không bao giờ `passed`*; *năm trạng thái §10.2.3*. Không có lớp finding mở nào được chuyển sang.
