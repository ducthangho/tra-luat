Verdict: request_changes
Reviewed commit: 183e28f4b59467895c411db7f565dd21769ee511
Spec sha256: 6c21bd26b64aa5a57925875789a8d9f9f3132a00ae53416b1ac4d0ad703e3eef

Bản vá phát hiện được verdict đuôi HOA trên Linux; hai đột biến bắt buộc đều bị ca phản chứng bắt đúng nguyên nhân. Head đạt toàn suite `268/268`, validator biên nhận đạt, byte hai verdict không đổi. Tuy nhiên, hai biên nhận và README mới khẳng định sai rằng không có run.json/prompt để kiểm chứng, trong khi các hiện vật đúng hai lượt review đã có ngay trong base. Có **1 P2, 1 P3**; không đủ ngưỡng approve.

Reviewer: OpenAI Codex, phiên độc lập với executor Claude; shell/tools thực chạy trong sandbox Linux qua transport machine. Không tự chứng nhận model/effort runtime cụ thể. Không sửa nội dung `cay-kho/`; thay đổi cấu hình duy nhất là `git config core.abbrev 7` theo chỉ thị. Không cấp quyền merge/land và không đăng thông điệp ra ngoài. Kết luận chỉ áp dụng exact SHA ở dòng 2.

Các lệnh dưới đây chạy từ sandbox, trừ khi ghi “trong cay-kho”. Các lượt Python dùng `PYTHONDONTWRITEBYTECODE=1`; các lượt test có thể tạo commit fixture dùng thêm `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`. Script tái hiện và log nằm trong sandbox, ngoài cây được review.

**Findings**

- [P2] wp1006-runtime-artifacts-falsely-absent: `ops/reviews/wp929-g1-codex-luot1-VERDICT.receipt.yaml:83`, biên nhận lượt 2 dòng 26, 61, 80–81; `ops/reviews/README.md:794` và hai hàng mục lục mới — `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py` — cả hai lượt có `present_at_base ...-run.json`, `prompt_hash_matches=True`, `verdict_copy_equal=True`, run_id/head khớp receipt; `ma_thoat=0`, thời lượng `1337.003` / `594.161` giây — sửa lời khai và caveat để dẫn đúng hiện vật đã có, phân biệt thiếu chứng nhận model với thiếu run.json; đồng bộ README.
- [P3] wp1006-listing-boundaries-unmeasured: `ops/lease_publish_test.py:1847`–1854, ca `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen` — `PYTHONDONTWRITEBYTECODE=1 python3 measure_mutations.py` rồi `PYTHONDONTWRITEBYTECODE=1 python3 probe_listing.py` — `c2_no_is_file` và `c4_case_sensitive_receipts` đều sống (`1/1 đạt`), nhưng probe bổ sung cho `contract_matches=False`, trong khi control `True` — thêm fixture thư mục có đuôi verdict và tệp có đuôi `.RECEIPT.YAML`, đòi bộ liệt kê bỏ thư mục/nhận tệp; gắn hai đột biến để khóa M1.

P2 là lỗi dữ liệu chứng cứ mới thêm, không phải yêu cầu nâng assurance. Cụ thể, ngay tại base `79dbaf4` đã có bộ:

`ops/land/pr933-wp929-provenance/verdicts/wp929-r1-g1-claude-review-{1,2}-codex-{run.json,prompt.md,stderr-header.txt,verdict.md}`.

`audit_receipts.py` chạy `git show <base>:<tệp>` và so byte với head cho cả tám tệp. `git log --format='%H %cI %s' -- <run.json>` chỉ ra commit thêm `f46ddf5e64d5e938a334d46084b1b865d609c4b0` lúc `2026-10-26T01:25:13+00:00`; `git merge-base --is-ancestor f46ddf5e64d5e938a334d46084b1b865d609c4b0 <base>` rc=0. Hai run.json ghi:

| Dữ liệu đo từ hiện vật | Lượt 1 | Lượt 2 |
|---|---|---|
| run_id | `0d78fe118c6340fda716921de68a5d06` | `3536a415068645adab6cfed3e3de5f03` |
| head | `8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95` | `227dcdebc62c9275f9df09056f66e2124ed5f14c` |
| ma_thoat | `0` | `0` |
| thoi_luong_giay | `1337.003` | `594.161` |
| SHA-256 prompt, khớp tệp prompt.md | `5104ab547b0136c34c67cad01cf082add93a62283bfd4bc624c29fe738c5a4af` | `35f2eb79ff5990b071239fe46c9464e5963ded6037768b396c5a98aea55733f5` |
| Có trường model_phuc_vu | `False` | `False` |
| Verdict ở hồ sơ land trùng byte verdict ở reviews | `True` | `True` |

Trích đoạn stderr được đọc bằng `cat ...-stderr-header.txt` có `OpenAI Codex v0.164.0`, `model: gpt-6-astra`, `reasoning effort: xhigh`. Đây là lời khai của CLI trong một trích đoạn; không tự chứng minh model thực phục vụ hay băm toàn stderr. Giữ giới hạn về model là đúng, nhưng không thể lấy lý do “run.json không vào kho” hoặc “prompt đầy đủ và mã thoát không kiểm được”. Tiền đề “không có run.json” trong SPEC M4 cũng bị phép đo bác bỏ; cần đính chính tiền đề này theo quy trình của chủ packet.

Hướng vá P2 rẻ nhất nằm ở hai receipt và các hàng README mới: neo hiện vật trên commit có thật, ghi run_id/head/rc/thời lượng/prompt hash theo nguồn đo được; giữ `model_da_chay: KHONG_DO_DUOC` nếu chưa đủ chứng nhận, nêu đúng lý do thiếu `model_phuc_vu` và chỉ có stderr excerpt. Giữ hạn chế approve lượt 2 không neo head merge. Kiểm khóa: chạy lại `audit_receipts.py`, validator v2 và t27; đối chiếu từng lời phủ nhận sự tồn tại của hiện vật với Git. Rủi ro cần tránh: không nâng `cross_approved` chỉ từ header CLI, không coi `provider: local_process`/`execution_surface: subprocess` trong run.json là chứng nhận model, không sửa byte verdict lịch sử.

P3 là nợ độ phủ, không phải lỗi bộ liệt kê hiện tại. `probe_listing.py` tạo các tên thường, nằm hoàn toàn trong thư mục tạm: một thư mục `folder-VERDICT.md`, một tệp `real-VERDICT.md`, một tệp `sample.RECEIPT.YAML`. Control trả đúng `['real-VERDICT.md']` và `['sample.RECEIPT.YAML']`. Mutant bỏ `is_file()` trả thêm thư mục; mutant glob riêng receipt trả `[]`. Cả hai vẫn qua ca phản chứng sẵn có. Hướng vá tại test của helper vì đây là hai thuộc tính được M1 nêu rõ; giữ ca dương và âm mục lục hiện tại. Rủi ro: đừng biến thử nghiệm bộ liệt kê thành chốt buộc toàn `_kiem_muc_luc` phải chấp nhận mọi cách viết hoa của tên sidecar khi các chốt khác có hợp đồng riêng. Không cần sửa helper đang đúng. Chưa chạy toàn suite dưới từng mutant; phạm vi “sống” ở đây là ca `t27_phan_chung_*` đã nêu.

**Preflight và phạm vi**

`git config core.abbrev 7` chạy trước các phép đo Git trong `cay-kho/`. Các lệnh và output đã đo:

| Lệnh | Output / kết quả |
|---|---|
| `git rev-parse HEAD HEAD^{tree}` | `183e28f4b59467895c411db7f565dd21769ee511`; `b729fb12936f8c5c69fd381e0bd10d131345f820` |
| `git rev-parse 79dbaf443f90daece751d9ab2537796bbd6084bf^{tree}` | `b95fb2108ab139c9a31f6f107797b00aa704ab34` |
| `git branch --show-current` | rỗng: detached |
| `git rev-parse --is-shallow-repository` | `false` |
| `sha256sum SPEC.md` | khớp đầy đủ dòng 3 |
| `git diff --stat <base> HEAD` | `4 files changed, 252 insertions(+), 6 deletions(-)` |
| `git diff --name-only <base> HEAD` | chỉ `ops/lease_publish_test.py`, `ops/reviews/README.md`, hai receipt wp929 mới |
| `git diff --check <base> HEAD` | rc=0, output rỗng |
| `audit_receipts.py`: so byte `git diff <base> HEAD` với `DIFF.patch` | `DIFF.patch_byte_equal=True` |
| `git status --porcelain=v1 --ignored`, đầu/cuối review | rỗng; cây nguồn sạch |

Kiểm cuối lưu tại `evidence/final-integrity.log`; kiểm write set và diff tại `evidence/receipt-audit.log`. Môi trường thực đo: Linux x86_64, Python 3.13.17, Ruff 0.17.3, actionlint 1.7.7, ShellCheck 0.9.0, Pandoc 3.1.3.

**Head/base và các đột biến**

Trên head, trong `cay-kho`: `python3 ops/lease_publish_test.py --chi-ca=t27_` → rc=0, `lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0`. Cả `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc` và ca phản chứng mới đều `QUA` (`evidence/head-t27.log`).

Base được xuất bằng `git archive 79dbaf443f90daece751d9ab2537796bbd6084bf` vào `base-copy/`, không checkout lại cây nguồn. Chạy cùng selector trên `base-copy/ops/lease_publish_test.py` → rc=0, `lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0` (`evidence/base-t27.log`). Đây là phép đo base xanh trên Linux dù chưa liệt kê hai verdict HOA và chưa có hai receipt.

`measure_mutations.py` chép nguồn thành các bản riêng dưới `mutations/<tên>/ops/lease_publish_test.py`; không dùng `.pyc`. Mỗi bản chạy CLI `--chi-ca=t27_phan_chung_`, đúng một ca `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`. Log tổng hợp: `evidence/mutations-summary.log`; log riêng: `evidence/mutation-<tên>.log`.

| Đột biến | rc, kết quả | Thông báo / chốt thực sự |
|---|---|---|
| control | 0, `1/1` | `QUA` |
| (a) helper trả `sorted(thu_muc.glob("*" + duoi))` | 1, `0/1` | `bộ liệt kê không thấy đủ cả hai cách viết đuôi — nó đang phụ thuộc nền` |
| (b) như (a), xóa đúng chốt tự kiểm bộ liệt kê trong fixture | 1, `0/1` | `verdict đuôi -VERDICT.md vắng khỏi mục lục mà _kiem_muc_luc vẫn XANH — chốt mù với đuôi HOA trên nền này (lỗi #1006)` |
| c1: bỏ `lower()` của tên | 1, `0/1` | cùng lỗi bộ liệt kê như (a) |
| c2: bỏ `is_file()` | 0, `1/1`, **SỐNG** | fixture chưa có thư mục giả dạng verdict |
| c3: đổi `f.relative_to(goc)` thành `f.relative_to(HERE.parent)` | 1, `0/1` | `ValueError: ... is not in the subpath of ...` ở lượt đối chứng dương; không tính đây là tín dụng bắt lỗi glob |
| c4: chỉ dùng glob cho `.receipt.yaml`, giữ nhánh verdict nguyên | 0, `1/1`, **SỐNG** | fixture chưa có đuôi receipt viết HOA |
| c5: `_kiem_muc_luc` chỉ `return` | 1, `0/1` | cùng thông báo “vẫn XANH” như (b) |
| c6: `_kiem_muc_luc` luôn ném lỗi đúng tên verdict/cột | 1, `0/1` | lỗi mục lục thoát ra ở đối chứng dương; chặn quá rộng bị bắt |

Trace độc lập trong cùng script (`evidence/fixture-trace.log`) ghi hai lần gọi checker thật:

1. Fixture âm có `README.md`, `moi-VERDICT.md`, `thuong-verdict.md`, `thuong-verdict.receipt.yaml`. Checker ném `AssertionError: README.md: verdict 'moi-VERDICT.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'...`.
2. Fixture dương có thêm `moi-VERDICT.receipt.yaml` và hàng mục lục tương ứng. Checker trả về bình thường.

Vì vậy ca có đo đúng việc thiếu verdict HOA khỏi mục lục, và không xanh rỗng khi checker bỏ qua công việc; cũng không chấp nhận checker luôn đỏ. Đột biến (b) chết vì nhánh kiểm thật bị mù, không phải vì danh sách fixture rỗng hay lỗi import/đường dẫn.

Khác biệt với câu chữ M3 cần giữ rõ: nhánh âm hiện tại cố ý **không có receipt cho verdict HOA**; receipt fixture còn lại chỉ có `verdict_path`, không phải một receipt v2 hoàn chỉnh. Ca đo hợp đồng của `_kiem_muc_luc`, không đo validator v2. Cách dựng này bắt được hồi quy glob: nếu ngay từ đầu có receipt HOA với đuôi receipt thường, vòng duyệt receipt có thể phát hiện mục lục thiếu và che mất việc vòng duyệt verdict đã mù. Nếu cần phủ nguyên văn tình huống M3 “kèm biên nhận hợp lệ”, nên thêm ca riêng, giữ ca mồ côi này.

**Đối chiếu từng nhóm lời khai (a) của hai receipt**

Lệnh tổng: `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py` → rc=0, `AUDIT_COMPLETED`. Script tự băm/đếm/đọc Git, không dùng các số receipt làm kết quả mặc định. Log: `evidence/receipt-audit.log`.

| Thuộc tính | Lượt 1 | Lượt 2 |
|---|---|---|
| SHA-256 verdict | `8a392561044c0ae6b9d504260149ff441fb8ec81cfe828fd8e06bd8f27c80bbf` | `40d42d53d7b30f7e703eced0376803907aa3b3a57d1d62dd697adcac25c30e49` |
| Byte | `11158` | `12184` |
| Dòng Verdict và ánh xạ receipt | `request_changes` → `changes_requested` | `approve` → `approve` |
| Dòng Reviewed commit | `8a6d795c982fc7e9da2fbfd28a75ca25d5f3eb95` | `227dcdebc62c9275f9df09056f66e2124ed5f14c` |
| Đếm finding P0/P1/P2/P3 từ dòng finding | `0/0/1/3` | `0/0/0/1` |
| Byte head so với base | bằng nhau | bằng nhau |
| Byte head so với blob neo `8d3f655` | bằng nhau | bằng nhau |
| `git log --format=%H -- <verdict>` | đúng 1 commit: `8d3f6553b5b63dac9d8e79c8e017a0d5a4335cb5` | cùng kết quả |
| `git log --diff-filter=A ...`, và `git log --all ...` | mỗi lệnh đúng 1 commit trên | cùng kết quả |
| `git merge-base --is-ancestor <reviewed_sha> ab94c4f` | rc=0 | rc=0 |
| Committer time của reviewed_sha, UTC | `2026-10-25T16:12:52Z` | `2026-10-25T16:42:31Z` |

`findings_ids` khớp cả thứ tự lẫn hạng: lượt 1 có `wp929-tree-is-not-activation-file` P2, `wp929-filename-boundaries-unmeasured` P3, `wp929-git-error-guards-unmeasured` P3, `wp929-nfc-unmeasured` P3; lượt 2 chỉ còn `wp929-git-error-guards-unmeasured` P3. Bộ đếm nhận cả cú pháp `- [P*]` và `- **[P3]`, không đếm lại các đoạn nhắc finding đã đóng.

`ops/leases/wp929-r1-g1-claude.yaml` xác nhận packet 929, revision 1, generation 1, lease ID, provider `claude`, execution_surface `claude_code`, model tự khai `claude-opus-5-5`. Băm đặc tả wp929 thực đo là `79251bee45fc39003d13438d741c4e6319dc80ea6b480dc1b931c93d0c6a7ae6`, khớp lease và dòng 3 hai verdict.

Cửa sổ lease đọc từ YAML: `[2026-10-25T15:30:00Z, 2026-10-26T00:33:00Z)`. Script chuyển timezone và kiểm bất đẳng thức cho hai reviewed commits và commit neo: tất cả `inside=True`. Commit neo có committer time `2026-10-25T17:29:37Z`, subject chứa `handoff(#929)`. Đây là kiểm thời điểm commit nằm trong cửa sổ, không suy thời điểm chạy review chỉ từ commit time.

`git merge-base --is-ancestor 8d3f655 <base>`, `8d3f655 fe46e7e`, `fe46e7e <base>` đều rc=0. `git show -s --format='%H %cI %P%n%s' fe46e7e` nêu merge nhánh `ops/wp929-r1-g1-lease`, khớp mô tả mỏ neo. Hai `evidence_url` được parse/so đúng commit neo và đường dẫn verdict; byte blob ở neo khớp băm. Không cần dựa vào việc URL blob có tải được qua HTTP để xác minh Git object này.

`git show -s --format='%H %cI %P%n%s' ab94c4f` cho merge commit `ab94c4fb01d0d122d2f00a1f2c386c6a191349c5`, thời gian `2026-10-26T07:29:09+07:00` (= `00:29:09Z`), subject `Merge pull request #933 ...`, parent thứ hai `f3b54d260bcdecf5b6d2348730a958e168bf7330`. Commit `f3b54d2` có parent đầu `227dcdebc62c9275f9df09056f66e2124ed5f14c`, parent thứ hai master `36057e8292bcb3b27ceb64b461d7cf29057a8ba3`. Vì thế cảnh báo reviewed_sha lượt 2 khác head merge là có cơ sở; không đọc ancestry thành approve exact merge SHA.

Validator thật, trong `cay-kho`: `python3 ops/bien_nhan_v2.py --root .` → rc=0:

```text
bien_nhan_v2: 246 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 299
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
```

Log: `evidence/receipt-validator.log`. Validator xanh không phủ định P2: nó không xác minh lời phủ nhận sự tồn tại của các hiện vật runtime trong văn xuôi mới thêm.

**README và dòng trống bị xóa**

`PYTHONDONTWRITEBYTECODE=1 python3 audit_readme.py` → rc=0, `PANDOC_GFM_AUDIT_PASS`. Script dùng renderer độc lập `pandoc --from=gfm --to=html` cho base và head, rồi đọc cấu trúc `<tr>`/`<p>` bằng HTMLParser, không chỉ tìm chuỗi trong Markdown. Log `evidence/readme-render.log`; HTML đầy đủ ở `evidence/readme-base.html` và `evidence/readme-head.html`.

Với từng tên `doctor-github-mcp-review-6-codex-verdict.md`, `don-nhanh-base-review-4-claude-verdict.md`, `don-nhanh-base-review-5-claude-verdict.md`, xét đúng cặp tên + id `ANCESTRY-CHI-TREN-NHANH-LA-TRANG-THAI-LICH-SU`:

| Phiên bản | Hàng bảng chứa cặp | Đoạn văn chứa cặp |
|---|---:|---:|
| Base | 0 | 1 |
| Head | 1 | 0 |

Trong base có dòng rỗng ở dòng 790 trước hàng doctor; ba dòng kế tiếp không có lại header/separator nên trở thành đoạn văn. Không khẳng định các tên verdict ấy hoàn toàn vắng trong mọi hàng khác: don-nhanh còn các cảnh báo khác. Lời khai về **ba hàng bị ngắt bảng cụ thể này** là đúng.

`audit_receipts.py` gọi parser `_bang` hiện tại: bảng cảnh báo từ 731 lên 736 hàng (+3 được nối lại, +2 mới), mục lục 312 lên 314 hàng. Mỗi verdict wp929 có đúng một hàng mục lục và một hàng caveat mới; renderer cũng thấy liên kết receipt và `caveat_rows=1` cho từng verdict. Cấu trúc đúng, nhưng nội dung caveat có lỗi P2 ở trên.

**Gate bổ sung và phần chưa đạt/chưa đo**

Trong `cay-kho`, `PYTHONDONTWRITEBYTECODE=1 GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null python3 ops/lease_publish_test.py` đã chạy xong:

```text
lease_publish: 268/268 đạt; đã chạy=268, bỏ qua=0
EXIT_CODE=0
```

Log nguyên lượt: `evidence/full-suite.log`. Không có ca phải ghi bỏ qua vì thiếu actionlint/shellcheck/mạng trong lượt này. Không suy kết quả Windows từ lượt Linux.

`python3 -m ruff check --no-cache --select F --output-format json ops/lease_publish_test.py`, chạy riêng trên base và head, đều rc=1 với 7 F401 + 2 F541. So đa tập `(code,message)` bỏ vị trí dòng cho `True`: **F delta = 0**, không phải 0 lỗi tuyệt đối. Kết quả ở `evidence/ruff-base.json`, `evidence/ruff-head.json`, `evidence/final-integrity.log`.

`python3 .claude/dev/packet_loop.py doctrine-scan --root .` → rc=0, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` (`evidence/doctrine-scan.log`).

Đã GET qua công cụ GitHub, không khởi chạy workflow hay sửa trạng thái:

- `GET /repos/ducthangho/tra-luat/actions/runs?head_sha=183e28f4b59467895c411db7f565dd21769ee511&per_page=100` trả `total_count=4` (`evidence/ci-runs.json`). [CI lượt PR 40831771127](https://github.com/ducthangho/tra-luat/actions/runs/40831771127) trên exact SHA có `conclusion=cancelled`, không thể ghi A5 xanh.
- `GET /repos/ducthangho/tra-luat/actions/runs/40831770491/jobs?per_page=100` cho [gate-ops Windows](https://github.com/ducthangho/tra-luat/actions/runs/40831770491/job/123307415153), label `windows-latest`, exact head đúng, job `in_progress`, bước `lease-publish selftest` còn `pending` tại lúc đo. A1 trên Windows: **KHÔNG ĐO ĐƯỢC kết quả**, chưa có dòng N/N để xác nhận (`evidence/ci-dispatch-jobs.json`).
- `GET /repos/ducthangho/tra-luat/commits/183e28f4b59467895c411db7f565dd21769ee511/check-runs?per_page=100` trả `total_count=41`, xác nhận `gate-ops (ubuntu-latest)=cancelled`, `gate-ops (windows-latest)=in_progress`, `thu-hoi=failure` (`evidence/ci-check-runs.json`). Chưa truy nguyên admission `thu-hoi`; không gán trạng thái này thành lỗi t27 của packet.

Không có quyền merge/land từ verdict này. Cần sửa P2 và đo lại exact SHA mới; P3 là nợ không chặn riêng lẻ. Bằng chứng CI đang chờ/hủy cũng không được đổi thành PASS.
