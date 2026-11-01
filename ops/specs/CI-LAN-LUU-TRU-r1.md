# Đặc tả packet `CI-LAN-LUU-TRU` r1: làn lưu trữ cho PR, push master và `workflow_dispatch` (ADR-0060 M11, packet D — phần D1)

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587

| trường | giá trị |
|---|---|
| packet_id | `CI-LAN-LUU-TRU`, revision 1, generation 1 |
| packet_issue | ghi ở comment đầu của Issue mở cùng đặc tả này |
| nguon_cap_viec | packet kế nhiệm **D** của `ADR-0060` M11 (*"gọn hiện vật review, validator cho làn lưu trữ"*), đo ở `ADR-0060` S8. Chủ kho chốt 01-11-2026 qua ba vòng hỏi trong phiên `session_015GtxrcRSrPnyeixJVDudWu`; một trong các quyết định là **tách D thành D1 (CI, đặc tả này) và D2 (README `ops/reviews` + `t27`, đặc tả sau)** |
| review_class | `sensitive`: sửa `.github/workflows/ci.yml` (§8: *"workflow/CI authority"*) |
| base | `origin/master` lúc cấp lease (đo khi soạn, 06:42Z 01-11: `7eeb1d9a`) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run` (offline, neo SHA ứng viên) + connector `@codex review` trên PR draft |
| depends_on | không có. Chạy song song với packet C (#1106); write set không giao (§3) |

Ưu tiên của chủ kho cho packet này: **gọn, chạy nhanh, hiệu năng quy trình hơn độ chặt của vật chứng.**

## 1. Vì sao — số đo (01-11-2026, 06:00–06:45Z)

| # | sự kiện | số đo |
|---|---|---|
| S1 | PR #1071 (chỉ chạm `ops/reviews/**`, 73 tệp), run `41183318847` (`pull_request`) | `chuan-bi` in `che_do=duong_nhanh`, **vậy mà** vẫn tốn **khoảng 51 runner-phút Ubuntu**: `gate-registry` 22,9 · `gate-ops` 9,8 · `gate` 7,4 · 8 mảnh `gate-nhanh-manh` khoảng 9,5 · `gate-packet-loop` 0,4. `gate-registry` và `gate-nhanh-manh` không có điều kiện `che_do` nào (`JOB_CO_IF_CHO_PHEP` trong `ops/ci_duong_nhanh_test.py`, dòng 2436) |
| S2 | cùng head `0104461`, run `41183317816` (`workflow_dispatch`) | **khoảng 256 phút** trên Windows (`gate-packet-loop (windows-latest)` 83,7 · `gate-registry (windows-latest)` 81,7 · `gate-ops (windows-latest)` 47,2 · `gate (windows-latest)` 17,8 · 8 mảnh khoảng 22). Đây là nguồn của con số 84 phút trong `ADR-0060` S8: nó đến từ một lượt **dispatch**, không phải từ lượt PR |
| S3 | `ci.yml`, output `che_do` của `chuan-bi` | chỉ `pull_request` được phân loại; push master và `workflow_dispatch` luôn `day_du` (dòng 71) |
| S4 | 200 merge gần nhất trên base ghim `7eeb1d9a10aea8e1805b66fbf3d68549eb6778da` (đo 07:50Z 01-11; lệnh: `git log --first-parent --merges -200 --format=%H 7eeb1d9a…`, mỗi merge `M` lấy `git diff --name-only --no-renames -z M^1 M` rồi tách theo NUL; merge cũ nhất ngày 19-10-2026; 0 merge có diff rỗng) | nhóm theo tập tệp đổi: **95** merge mọi tệp dưới `ops/{reviews,land}/**` · **26** merge mọi tệp dưới 4 tiền tố hồ sơ và có ít nhất một tệp `specs`/`leases` · **79** merge có ít nhất một tệp ngoài 4 tiền tố. Phải dùng `-z`: không có nó, git đặt tên tệp có dấu trong dấu nháy và merge `7471f95f` (tệp `HƯỚNG 10 - HINT tren ban sao.log`) bị xếp nhầm ra ngoài vùng — bản `ea6ab70` của đặc tả này đếm sai 94/80 vì thế (review offline lượt 2); bản `9dcc0cb` còn đếm cả commit không phải merge nên ra 59/22/53. Trong 95 merge thuần lưu trữ, **38** có tệp đuôi `.py/.sh/.ps1/.yml`, gần như toàn bộ là bản sao sandbox nằm sâu từ 4 cấp trở xuống (`git ls-files 'ops/land/*.py' 'ops/reviews/*.py'`: 651 tệp, 1 ở 3 cấp, 650 sâu hơn) |
| S5 | push master của merge thuần lưu trữ | run `41278662487` (merge #1075, chỉ `ops/reviews`) chạy `day_du`, còn `in_progress` sau 25 phút. Merge chỉ đổi đặc tả: #1098 khoảng 56 phút, #1103 khoảng 40 phút |

## 2. Thay đổi

### 2.1 Bộ phân loại (`ops/ci_duong_nhanh.py`)

Giữ nguyên allowlist **4 tiền tố** `ops/{land,leases,reviews,specs}/**`, ba trạng thái và tính fail-close hiện có. Thêm:

1. **Quay về `day_du` dù đường dẫn nằm trong allowlist**, khi có ít nhất một tệp đổi:
   - **mã cấp nông**: tệp đặt **thẳng** dưới một trong bốn tiền tố (đúng 3 thành phần đường dẫn, vd `ops/land/x.py`) có đuôi trong tập
     `{.py, .sh, .bash, .ps1, .psm1, .bat, .cmd, .js, .mjs}`. Bản sao nằm sâu hơn (vd `ops/reviews/<lượt>/run/x.py`) vẫn đi đường nhanh
     (quyết định chủ kho: *"Chỉ chặn cấp nông"*). `.yaml`/`.yml` **không** thuộc tập này, vì `ops/land/*.yaml` cấp nông là hồ sơ land;
   - **mode git** ở phía mới là `100755`, `120000` (symlink) hoặc `160000` (gitlink). Hiện các ca này đi đường nhanh rồi bị `kiem-re` đánh ĐỎ;
     sau thay đổi thì chúng quay về làn thường. Riêng symlink và gitlink, `kiem-re` **giữ** chốt ĐỎ của nó (phòng thủ hai lớp);
   - **đổi mode** của đường dẫn có mặt ở **cả hai** phía (mode cũ ≠ mode mới, khác `000000`), theo cả hai chiều: `100644 → 100755` và `100755 → 100644`.
     Tệp mới hay tệp bị xoá **không** là đổi mode: chúng chỉ chịu luật mode phía mới ở gạch trên (`000000 → 100644` đi đường nhanh, xoá tệp đi đường nhanh).
   Rename ra/vào vùng mã đã được `--no-renames` xử lý (`t12`); diff hỗn hợp đã quay về `day_du`. Giữ nguyên.
2. **Phân loại `push`** (chỉ `refs/heads/master`). Diff `before..after`, với `before = github.event.before` và `after = github.sha`.
   **KHÔNG ĐO ĐƯỢC ⇒ `day_du`** khi: `before` vắng, sai mẫu SHA hoặc toàn số 0; `before` không phải tổ tiên của `after` (force push); git lỗi;
   hoặc diff rỗng. Tệp ngoài allowlist, hay một điều kiện ở mục 1 ⇒ `day_du`.
3. **Phân loại `workflow_dispatch`**. Thêm input `che_do`, kiểu `choice`, gồm `tu_dong` (mặc định) và `day_du`.
   - `day_du` ⇒ `day_du`, không phân loại.
   - `tu_dong` ⇒ diff `merge-base(origin/<nhánh mặc định>, github.sha)..github.sha`. **Diff rỗng ⇒ `day_du`**: dispatch trên chính master,
     hay trên một ref không có gì mới, là lời yêu cầu chạy đủ. Diff `day_du` theo luật PR thì `day_du`. Không đo được ⇒ `day_du`.
   - Input vắng (gọi bằng API cũ) đọc như `tu_dong`.
4. Mọi `che_do` khác `pull_request` in một dòng log riêng (`DUONG_NHANH: su_kien=<e> …`), giống dòng log của PR hiện nay.

Luật PR không đổi, trừ mục 1.

### 2.2 `ci.yml`

1. `chuan-bi`:
   - bước checkout và bước phân loại chạy cả với `push` và `workflow_dispatch`, có thêm env `before`/input `che_do`;
   - output `che_do` bỏ vế `github.event_name == 'pull_request' &&`. Bước phân loại vắng hoặc hỏng thì vẫn rơi về `day_du`;
   - output `os`: khi `che_do == duong_nhanh` thì **ép `["ubuntu-latest"]`** bất kể `runner_set` hay nhãn `windows`
     (quyết định chủ kho: *"Ép chỉ Ubuntu"*). Muốn Windows trên PR lưu trữ thì dispatch với `che_do=day_du`.
2. **`gate-registry`, `gate-nhanh-manh` và `gate-nhanh-gop`**: thêm `if:` **mức bước** theo `che_do` để bỏ các bước nặng; job vẫn khởi động và báo kết quả.
   Thêm một bước `DUONG_NHANH - liet ke buoc bo qua (job <tên>)` như các job đã có. Với `gate-nhanh-gop`: bước gộp
   (`ops/nhanh_don_duoc_test.py --gop-dich manh`) mang `if: … != 'duong_nhanh'`, và một bước riêng chỉ chạy khi `== 'duong_nhanh'` in
   `GOM: KHÔNG ĐO — duong_nhanh, 0 mảnh`. **Không** sửa consumer `ops/nhanh_don_duoc_test.py`: ở `day_du` (hay `che_do` vắng/lạ) bước gộp
   vẫn chạy và vẫn từ chối khi thiếu mảnh (`_loi_gop_dich`: `khong co bien nhan manh nao`). Đường `KHÔNG ĐO` của `wp892` thuộc
   `gate-cong-cu-gop`, không phải job này.
3. **Danh sách CHO PHÉP, không phải danh sách bỏ.** Trên đường nhanh, trong sáu job `gate`, `gate-ops`, `gate-packet-loop`,
   `gate-registry`, `gate-nhanh-manh`, `gate-nhanh-gop`, **mọi** bước phải mang `if:` có vế `needs.chuan-bi.outputs.che_do != 'duong_nhanh'`,
   nối `&&` ở mức ngoài cùng với điều kiện cũ nếu có. Chỉ trừ các bước thuộc **tập cho phép**, khai bằng tên/`uses` nguyên văn trong
   `ops/ci_duong_nhanh_test.py`:
   - `Force LF checkout (hash parity với manifest)`, `actions/checkout@v4`, `actions/setup-python@v5`, `cài PyYAML + jsonschema (…)`;
   - các bước chỉ chạy khi `che_do == 'duong_nhanh'`: liệt kê bước bỏ, `kiem-re`, `GOM: KHÔNG ĐO`;
   - `ci-duong-nhanh selftest` và `bien-nhan v2 selftest` (job `gate-ops`): đang chạy trên đường nhanh hôm nay, giữ nguyên.
   Mọi bước khác bị bỏ trên đường nhanh của cả ba sự kiện (quyết định chủ kho: *"Bỏ, chỉ giữ kiem-re"*). Đo trên `c6dd7b33` (07:50Z 01-11),
   tập ấy gồm: cài `actionlint`/`shellcheck`/`rg`/Ruff, G5, `py_compile`, các selftest của `gate`, `tl selftest (co bang chung exact-identity)`
   (hiện chỉ có `if: github.event_name != 'pull_request'`, tức sẽ chạy đủ trên push/dispatch đường nhanh: finding connector `4434801200`),
   `tai len gate-evidence`, `workflow-audit`, `doc-claims-check`, `ci-phamvi`, hai bước `release-verify`, `tl_boot smoke`, `don-nhanh selftest`.
   Không thêm validator mới. Vì sao dùng danh sách cho phép: danh sách bỏ phải đoán trước mọi bước nặng, nên thua ngay từ thiết kế. Bản
   `c6b6680` của đặc tả này dùng danh sách bỏ và đã bỏ sót `tl selftest`. Bước thêm vào sáu job này về sau mặc định bị bỏ trên đường nhanh,
   trừ khi được đưa vào tập cho phép.
4. Bước `kiem-re` hiện nhận cặp gốc/đầu từ `github.event.pull_request.*`. Với `push` và `workflow_dispatch`, `chuan-bi` xuất thêm
   hai output `goc`/`dau` (đúng cặp đã dùng để phân loại); `kiem-re` đọc chúng. Thiếu ⇒ `kiem-re` ĐỎ (fail-close), không rơi về PR env.
5. Không dùng `paths:` hay `paths-ignore:`. Không thêm job mới. Không đổi tên job, tên check hay `timeout-minutes`.

### 2.3 Test

- `ops/ci_duong_nhanh_test.py`: ca cho từng luật ở §2.1 và cho dạng mới của `ci.yml` (cập nhật bảng job/bước đang ghim, gồm `JOB_CO_IF_CHO_PHEP` và danh sách bước bỏ).
- `ops/lease_publish_test.py`: `t162` (evaluator output `os` của `chuan-bi`) thêm các vế `che_do`. Không chạm ca nào khác của tệp.
- `.claude/dev/ci_dang_ky_test.py`: chỉ sửa ở mức cần cho G5/registry khớp dạng `if:` mới. Không cần thì không chạm, và §3 khai lại.
- `ops/cong_cu_test.py`: chỉ `t6`. Hiện `t6` đòi bước cài shellcheck của job `gate` **không có `if:`** (dòng 365), nên bỏ bước ấy
  trên đường nhanh làm `t6` ĐỎ (review offline lượt 1 đo trong bộ nhớ). Sửa thành: mỗi bước cài trước G5 hoặc không có `if:`, hoặc có
  `if:` đúng nguyên văn `needs.chuan-bi.outputs.che_do != 'duong_nhanh'`; bước G5 `kiem-tra` mang cùng `if:` ấy. Giữ allowlist lệnh
  setup và chốt thứ tự G5 như cũ.

## 3. Write set

1. `.github/workflows/ci.yml`
2. `ops/ci_duong_nhanh.py`
3. `ops/ci_duong_nhanh_test.py`
4. `ops/lease_publish_test.py`
5. `.claude/dev/ci_dang_ky_test.py`
6. `ops/cong_cu_test.py` (chỉ `t6`)

`ops/specs/CI-LAN-LUU-TRU-r1.md` chỉ nằm trong PR đặc tả, không sửa trong PR thi công. PR thi công có tối đa 6 tệp, đúng trần.

Quét người giữ lúc soạn (06:40Z 01-11, sau khi fetch đủ, so `ls-remote` với `for-each-ref`: thiếu 0/734): `ops/lease_publish.py ai-dang-giu` cho
năm đường dẫn 1–5 cùng `ops/reviews/README.md` ⇒ **`NGƯỜI_GIỮ 0`** ở cả sáu. `ops/cong_cu_test.py` thêm sau review lượt 1; quét lại cả sáu tệp của write set lúc 07:18Z (base `c6dd7b33`) ⇒ `NGƯỜI_GIỮ 0`. Đo lại trước khi cấp lease.

**Không giao với packet C**: C giữ `.claude/dev/packet_loop.py`, `.claude/dev/packet_loop_test.py`, `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`,
`docs/PROTOCOL_DA_PHIEN.md`, `.claude/skills/land-packets/SKILL.md`. D1 không gọi `kiem-merge` hay `kiem-dong-wp`.

**Trình tự với D2**: `ops/lease_publish_test.py` có mặt ở cả D1 (`t162`) và D2 (`t27`), nên D2 chỉ được cấp lease sau khi D1 land.

### Trần — khai `nang_tran` ngay khi đóng băng

```yaml
nang_tran:
  ai_nang: ducthangho   # chủ kho, protocol §2; chọn "Khai nang_tran 650 ngay" ở vòng hỏi thứ ba, 01-11-2026, phiên session_015GtxrcRSrPnyeixJVDudWu
  can_cu: >-
    ƯỚC TÍNH lúc soạn, chưa phải numstat: 350–450 dòng thêm trên 4–5 tệp (bộ phân loại khoảng 80, ci.yml khoảng 50, ca test và đột biến khoảng 250–300),
    tức sát trần 450. Packet B (#1094) phải mở thêm hai PR đặc tả chỉ để nâng trần giữa chừng (#1098, #1103). Tách tiếp D1 thì
    bộ phân loại land mà ci.yml chưa gọi nó, hoặc ngược lại. Chưa có numstat thật: đo lại ở A9.
  tran_cu: "≤ 6 tệp / ≤ 450 dòng thêm (ADR-0053)"
  tran_moi: "≤ 6 tệp / ≤ 650 dòng thêm"
```

## 4. Nghiệm thu (mỗi dòng: ca, và đột biến làm nó ĐỎ)

| # | tiêu chí | đột biến / phép đo làm ĐỎ |
|---|---|---|
| A1 | PR chỉ thêm `ops/land/x.py` (3 thành phần) ⇒ `day_du`; `ops/reviews/a/run/x.py` ⇒ `duong_nhanh`; `ops/land/x.yaml` ⇒ `duong_nhanh` | bỏ luật mã cấp nông ⇒ ca thứ nhất ĐỎ; đếm sai số thành phần (≥3 thay vì ==3) ⇒ ca thứ hai ĐỎ; thêm `.yaml` vào tập đuôi ⇒ ca thứ ba ĐỎ |
| A2 | dưới allowlist: tệp mới mode `100755`, symlink mới, gitlink mới ⇒ `day_du`; đổi mode `100755→100644` ⇒ `day_du` (cô lập luật đổi mode); sửa nội dung một tệp đang `100755`, mode giữ nguyên ⇒ `day_du` (cô lập luật mode phía mới); tệp mới `100644` và xoá một tệp ⇒ `duong_nhanh` | gỡ luật mode phía mới ⇒ ca sửa nội dung tệp `100755` ĐỎ; gỡ luật đổi mode ⇒ ca `100755→100644` ĐỎ; tính thêm/xoá là đổi mode ⇒ ca tệp mới `100644` ĐỎ |
| A3 | `kiem-re` vẫn ĐỎ với symlink/gitlink khi bị gọi thẳng | gỡ chốt `kiem_mode_git` ⇒ ĐỎ |
| A4 | `push`: `before` vắng / toàn số 0 / sai mẫu / không phải tổ tiên / git lỗi / diff rỗng ⇒ `day_du`; push thuần lưu trữ ⇒ `duong_nhanh`; push có mã ⇒ `day_du` | gỡ từng chốt ⇒ ca của chốt ấy ĐỎ; bỏ kiểm tổ tiên ⇒ ca force push ĐỎ |
| A5 | `workflow_dispatch`: input `day_du` ⇒ `day_du`; `tu_dong` + diff thuần lưu trữ ⇒ `duong_nhanh`; `tu_dong` + diff rỗng ⇒ `day_du`; input vắng ⇒ như `tu_dong`; input lạ ⇒ `day_du` | đổi luật diff rỗng thành `duong_nhanh` ⇒ ĐỎ; đọc input lạ như `tu_dong` ⇒ ĐỎ |
| A6 | `t162` (sau khi mở rộng): output `os` ⇒ `["ubuntu-latest"]` khi `che_do == duong_nhanh` ở cả ba sự kiện, kể cả `runner_set=windows-only` và PR có nhãn `windows`; mọi tổ hợp `day_du` giữ đúng giá trị cũ | bỏ vế ép Ubuntu ⇒ ĐỎ; ép cả khi `day_du` ⇒ ĐỎ |
| A7 | trên cây node `yaml.compose` của `ci.yml` (không trên dict): mọi bước của sáu job ở §2.2 mục 3 hoặc thuộc tập cho phép (so nguyên văn tên/`uses`), hoặc có `if:` với vế nguyên văn `needs.chuan-bi.outputs.che_do != 'duong_nhanh'` nối `&&` ở mức ngoài cùng; mỗi job có bước liệt kê bước bỏ, khớp từng chữ tên bước; `tl selftest` có cả hai vế (`event_name != 'pull_request'` và `che_do`). Một ca riêng ghim rằng `tl selftest` **không** thuộc tập cho phép | thêm một bước mới không `if:`, nằm ngoài tập cho phép ⇒ ĐỎ; gỡ vế `che_do` khỏi `tl selftest` ⇒ ĐỎ; nối bằng `\|\|` thay `&&` ⇒ ĐỎ; đổi `!=` thành `==` ⇒ ĐỎ; khoá `if` trùng trong một bước ⇒ ĐỎ; nới tập cho phép để chứa `tl selftest` ⇒ ca ghim ĐỎ |
| A7b | `kiem-re` với cặp `goc`/`dau` hợp lệ ⇒ rc=0, và với cặp vắng hoặc sai mẫu ⇒ rc≠0, **riêng cho từng sự kiện** `push` và `workflow_dispatch` (bốn ca) | `kiem-re` luôn trả lỗi khi không phải PR ⇒ hai ca hợp lệ ĐỎ; đọc env PR khi output vắng ⇒ hai ca vắng ĐỎ |
| A8 | `ci.yml` không có `paths:`/`paths-ignore:` ở mọi cò; ba check bắt buộc vẫn có job mang đúng tên cũ; `actionlint` rc=0 trên `ci.yml` (delta so nền = 0) | thêm `paths-ignore` ⇒ ĐỎ; đổi tên job ⇒ ĐỎ |
| A9 | `git diff --numstat <base> <ứng viên>`: chỉ các tệp trong §3, ≤ 650 dòng thêm. Kiểm riêng staged, unstaged và untracked trước khi đóng băng | thêm tệp thứ sáu ngoài §3 ⇒ ĐỎ |
| A10 | `ops/ci_duong_nhanh_test.py`, `ops/lease_publish_test.py`, `.claude/dev/ci_dang_ky_test.py` N/N trên Linux; Windows theo `ADR-0060` M3 (chạm `.github/workflows/**`): nền và ứng viên, so tập test ID đỏ | ca đỏ có ở ứng viên mà không có ở nền ⇒ ĐỎ |
| A11 | `full_mutant_audit` theo `ADR-0060` M9: **bắt buộc** (chạm `.github/workflows/**` và `ops/**/*.py`), hoặc waiver `owner_waived` đúng scope §10.2.3 | thiếu receipt và thiếu waiver khi merge ⇒ ĐỎ |
| A12 | **Canary sau land** (`chưa đo được` tới khi đo thật). PR lưu trữ thật đầu tiên sau land (chỉ `ops/{reviews,land}/**`, không có mã cấp nông), cùng run push master của merge ấy: mỗi run **≤ 12 runner-phút**, tính bằng tổng `completed_at − started_at` của mọi job (`actions/runs/<id>/jobs`), **0** job mang nhãn `windows-latest` có `runner_id ≠ 0`, ba check bắt buộc ở trạng thái `success` (không `skipped`), log `chuan-bi` có dòng `che_do=duong_nhanh`, và log bước `kiem-re` của `gate-ops` báo đạt. **Dispatch** đo riêng: phiên land gọi một lượt `workflow_dispatch` (`che_do=tu_dong`, `runner_set` mặc định) trên head của chính PR canary; cùng bốn điều kiện trên, kể cả 0 job Windows. Người đo là phiên land của D1; số đo và id run ghi lên Issue | một run > 12 phút ⇒ ĐỎ; có job Windows chạy thật ⇒ ĐỎ; một check bắt buộc vắng mặt hoặc `skipped` ⇒ ĐỎ; log thiếu dòng `che_do=duong_nhanh` (tức run nhanh vì lý do khác) ⇒ ĐỎ |

Lượt model bị loại **không** thuộc nghiệm thu của D1. Luật hiện hành, để phiên sau khỏi chạy thừa hay thiếu review:
- `ADR-0060` M8 (*Làn lưu trữ*) **đã** miễn cross-review bằng model và Windows cho PR lưu trữ — nhưng chỉ PR chứa bản ghi thụ động trong
  `ops/reviews/**` và `ops/land/**`. PR có `ops/specs/**` hay `ops/leases/**` đi làn thường theo M8, dù CI vẫn cho nó đi đường nhanh
  (allowlist 4 tiền tố của #674, giữ nguyên ở D1). Đường nhanh của CI và làn lưu trữ của M8 là hai khái niệm khác nhau; D1 không gộp chúng.
- `ADR-0060` M6 vẫn đòi connector sạch trên đúng head trước khi bỏ draft, kể cả với PR lưu trữ. Miễn connector cho làn lưu trữ là nợ ở §6.

## 5. Ngoài phạm vi

- README `ops/reviews` và `t27`: thuộc **D2** (đặc tả sau). Chủ kho đã chọn hướng: README chỉ trỏ nguồn, `t27` đọc biên nhận tự đủ, không di trú 339 biên nhận hiện có.
- Không di trú các mục cũ ở `ops/reviews` (5139 tệp) và `ops/land` (3761 tệp).
- Không đổi allowlist 4 tiền tố. Không thêm validator nội dung mới cho hồ sơ.
- Không sửa chú thích `full_mutant_audit` ở `gate-nhanh-manh` (nợ của `ADR-0060`). Nếu bước bị thêm `if:` nằm cạnh chú thích ấy thì để nguyên chữ.

## 6. Nợ (làm sau khi packet C land)

- **`LAN-LUU-TRU-MIEN-CONNECTOR`**: PR làn lưu trữ M8 (chỉ `ops/{reviews,land}/**`) không đòi connector. Cross-review đã được M8 miễn; phần
  còn thiếu là M6. Cần sửa `ADR-0060` M6 và `docs/PROTOCOL_DA_PHIEN.md`, hai tệp nằm trong write set của C. Trong lúc chờ, PR lưu trữ vẫn
  đòi connector theo M6, trừ khi chủ kho miễn từng lần.
- **`LAN-LUU-TRU-ADR-0060-S8`**: dòng S8 của `ADR-0060` gán 84 phút cho "PR sổ sách", trong khi số ấy đến từ một lượt `workflow_dispatch` (S2).
  Sửa câu chữ cùng lúc với nợ trên.

## 7. `chua_do_duoc`

- Cấu hình ruleset `master` (check nào bắt buộc): từ phiên web trả HTTP 403. Đặc tả giữ đúng tên ba job của #674 và không bỏ job ở mức job.
- `github.event.before` trên push merge của GitHub có luôn là first-parent của `github.sha` hay không: đọc theo tài liệu, chưa tự đo. Bộ phân loại không dựa
  vào điều đó, chỉ đòi `before` là tổ tiên.
- Phút tính tiền thật (billing) khác thời lượng job: A12 đo thời lượng job.
- Có `origin/<nhánh mặc định>` trong checkout của dispatch hay không: chưa đo trên runner. Thiếu ⇒ không đo được ⇒ `day_du`, nên chỉ mất tốc độ, không mất an toàn.

## 8. `hinh_dang_ke_thua`

D1 không phải packet khắc phục. Chép từ chỉ thị giao việc các lớp đã lặp ở packet B (#1094), để quét sớm:

- *kiểm SAU khi bộ phân tích đã chuẩn hoá* (khoá YAML `on`/`true`/`1.0`, khoá trùng): **3** lượt ⇒ A7 kiểm trên cây node `yaml.compose`;
- *tin TÊN ref thay vì đo OID*: **2** lượt ⇒ A4 đo tổ tiên bằng OID, `before` phải khớp mẫu 40 hex;
- *so bằng mà Python coi `1 == True == 1.0`*: **2** lượt ⇒ so input `che_do` bằng `type(x) is str` rồi mới so chuỗi;
- gọi `bash` trần trong test bị cổng #570 chặn ⇒ dùng `ops/bash_nen.py::tim_bash()`;
- đột biến chết vì ngoại lệ là tín dụng giả; đừng đổi ngoại lệ thành assertion để lấy tín dụng.
