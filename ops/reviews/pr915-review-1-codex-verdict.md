verdict: changes_requested
reviewed_sha: 2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

Đã đo độc lập tại exact SHA chỉ định, tree `6f299d7f70269ec32522fc4ea28c9d2d70c5424b`; base `50a59a945026a2ab2f97dc0e7ef7b5a540e17652`. Một lớp P1, hai hiện vật review: tự khai sai bề mặt chạy trong verdict #870/#889, chưa đính chính qua caveat. Câu sửa CLAUDE.md, byte/băm/OID/số P của ba biên nhận và mọi cổng được yêu cầu đều khớp.

Reviewer: codex; provider: openai_codex; transport: machine/tool-mediated. Execution surface/model của chính lượt này: KHÔNG ĐO ĐƯỢC độc lập từ hiện vật launcher được giao; phiên có công cụ shell, không suy danh tính backend từ tên agent. Review theo chỉ thị trực tiếp của chủ kho, không packet/lease, chỉ đọc cay-kho/. Không tự cấp assurance/approval/land. Các blob lịch sử chỉ dùng đối chiếu nguồn mà receipt đang khai; workflow hiện hành luôn lấy ở HEAD được giao.

Mọi hướng được nối vào báo cáo sau khi chạy. H2 lần đầu rc=1 do helper giả định base/tree phải là dòng YAML riêng; verdict #896 ghi chúng trong văn xuôi. Đã sửa helper ngoài checkout và đo lại trọn ba biên nhận thành công; giữ cả transcript lần đầu để không che lỗi phép đo. Đây không phải lỗi repository. Hai SyntaxWarning của Python 3.13 ở docstring test có sẵn, không làm các ca thất bại.

Lệnh tái lập các hướng từ thư mục giao việc: `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py <tên-hướng>`. Script chạy các cổng từ cay-kho/, đặt TL_CACHE_DIR ở review-evidence/cache, tắt bytecode và GIT_OPTIONAL_LOCKS. Bảng H2/H5 giữ đầy đủ SHA; toàn bộ stdout cổng dài nằm ở review-evidence/.

## BẢNG ĐO

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Neo đối tượng | HEAD 2789cbb…; base 50a59a9 | `review_probe.py preflight` (H1): HEAD đầy đủ, tree=6f299d7f70269ec32522fc4ea28c9d2d70c5424b; base=50a59a945026a2ab2f97dc0e7ef7b5a540e17652 | Có |
| Nguồn diff và cây đầy đủ | diff.patch/numstat tại head được giao | H1: `git diff`/`--numstat` khớp từng byte; is_shallow=false; core.abbrev=7; status rỗng | Có |
| Phạm vi ba commit | 3bc4244 sửa CLAUDE; 7cfe062 hiện vật; 2789cbb biên nhận/README | `review_probe.py provenance` (H4): lần lượt 1, 91, 4 tệp; danh sách đầy đủ ở review-evidence/*-numstat.txt | Có |
| t162 đọc từ workflow | Chỉ output os của chuan-bi | `review_probe.py static_scope` (H14): `raw_expr = wf_data["jobs"]["chuan-bi"]["outputs"]["os"]`; H8: đổi exclude/needs/if đều t162 PASS | Có |
| t162 đánh giá ngữ cảnh thật | push/PR thường/PR windows/từng runner_set | `review_probe.py workflow` (H8): chạy nguyên t162 trên bản sao workflow baseline PASS; bỏ nhánh windows-only ⇒ FAIL với kết quả hai OS | Có, cho các ngữ cảnh ca assert; không thay việc đọc từng job |
| Phân biệt output os với ma trận job | t162 không đọc exclude/if cấp job | H8: 6/6 đột biến độc lập ở hai job vẫn t162 PASS; H14 xác minh các chỗ đọc workflow trong AST | Có |
| Chốt G5 kiểm exclude | Mảnh/gom có chốt riêng | H8: bỏ exclude của gate-cong-cu hoặc gate-cong-cu-gop ⇒ loi_g5_workflow báo matrix sai | Có |
| Chốt G5 kiểm needs/if | Hai job mảnh/gom bị ghim needs/if | H8: lần lượt bỏ needs/if ở từng job ⇒ 4/4 lỗi đúng thông điệp; baseline không lỗi | Có |
| Phạm vi gate-cong-cu* | Phần mảnh/gom được kiểm | H8: tại SHA này prefix chỉ có [gate-cong-cu, gate-cong-cu-gop], khớp hai hằng JOB_G5_MANH/GOP | Có; không suy cho mọi gate* hay job thêm trong tương lai |
| t161 | Chỉ kiểm cấu trúc, không đánh giá biểu thức | H14: t161 PASS; AST có 0 lời gọi evaluator; mã kiểm nguồn matrix.os và output fromJSON | Có |
| Bản phẳng #870 | 79752 byte; sha256 8b222ab3… | `review_probe.py receipts` (H2 đo lại): 79752; hash đầy đủ 8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6; flat==original | Có |
| Bản phẳng #889 | 34167 byte; sha256 c5fe298a… | H2 đo lại: 34167; c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612; flat==original | Có |
| Bản phẳng #896 | 63341 byte; sha256 3feaad3e… | H2 đo lại: 63341; 3feaad3e207ae2dea5323cb6f831ba2980546ec1d3febeead6d415baccbbb803; flat==original | Có |
| Ba reviewed_sha/tree/base | 06a50c5/0fa694d/9e9a74b; 094e8d1/55f5edf/e63961f; 816f439/3da0ce2/1ccc314 | H2 đo lại: đầy đủ OID khớp verdict, run.head, git rev-parse tree; diff/numstat của từng thư mục khớp git diff base..reviewed_sha | Có; OID đầy đủ ở output H2 |
| Head đã merge của ba PR | Reviewed SHA là parent thứ hai của 5f288ea/6ac385f/27dcc3b | H2 đo lại: `git rev-parse <merge>^2` khớp từng reviewed_sha | Có, từ Git cục bộ |
| Kết quả và so_p* #870/#889 | #870 approve 0/0/0/0; #889 approve 0/0/0/0 | H2 đo lại: dòng 1/dòng Kết quả và cả bốn số trong từng receipt khớp | Có |
| Kết quả và so_p* #896 | changes_requested 0/0/1/0; finding t162-khong-khoa-toan-bo-ma-tran-job | H2 đo lại: dòng Kết quả và receipt đều 0/0/1/0; finding và HINT nằm trong hiện vật | Có; đây là số lịch sử, khác finding của lượt #915 này |
| SHA256SUMS ba thư mục | Các hiện vật nguyên vẹn | `review_probe.py hashes` (H3): `sha256sum -c SHA256SUMS` rc=0 cả ba; 31/22/32 OK; không tệp bỏ sót ngoài manifest tự thân | Có |
| evidence_url | Neo commit 7cfe062, chỉ mang hiện vật | H4: 7cfe06212cb43f92d5753940116079e671d9c385; 91 tệp đều nằm trong ba thư mục hoặc ba bản phẳng, 0 receipt; URL blob khớp byte verdict | Có; đối chiếu Git offline, không gọi URL |
| Launcher version/rc/state | 1.5.0; ma_thoat 0; xong; worktree_sach true | `review_probe.py run_metadata` (H5): cả ba trường khớp run.json; run ID khớp session_run_id | Có cho metadata đã lưu |
| Thời lượng launcher | 496.137; 380.787; 712.54 giây | H5: số trong receipt khớp run.json; hiệu timestamp tương ứng 496.137080; 380.787461; 712.539633 | Có trong sai số làm tròn 0.001 giây |
| Băm PROMPT.md | 2c58af0d…; 00773f21…; 27dbb858… | H5: sha256 thực ba PROMPT.md khớp đầy đủ prompt_sha256 trong run.json và tiền tố trong ghi chú | Có; hash đầy đủ ở H5 |
| stdout/checkpoint | Metadata run neo hiện vật | H5: stdout_byte/stdout_sha256/checkpoint_sha256 đều khớp byte tệp trong thư mục | Có |
| 14 dòng đầu stderr | Lưu header; full log 1287629/2085807/1076780 byte không vào kho | H5: ba header đều 14 dòng, v0.163.0/model/effort/session khớp sidecar; stderr_byte trong run.json đúng ba số | Đo được header/metadata; hash/byte full stderr không kiểm lại được vì thiếu log đầy đủ |
| Assurance | cross_reviewed; KHÔNG cross_approved vì không khoá model | H5: recursive model_keys=[] cả ba run.json; header tự khai gpt-6.1-sol/xhigh; receipt để model_da_chay KHONG_DO_DUOC | Có về giới hạn bằng chứng; không xác nhận backend model |
| Bề mặt tự khai trong hai verdict | #870/#889 codex_service; #889 còn nói không chạy qua codex exec | `review_probe.py identity_claims` (H11): launcher + receipt + header CLI mâu thuẫn câu tự khai; không caveat nói codex_service | KHÔNG — một P1, hai hiện vật review |
| Surface đối chứng #896 | codex_cli | H11: VERDICT.md:7, run.json:47 và receipt.surface đều codex_cli | Có |
| Hai snapshot gốc #870 | 672374 byte mỗi tệp; cùng hash 5b88623b…; KHÔNG vào kho | `review_probe.py snapshot_caveats` (H6): không tracked snapshot; hash đầy đủ chỉ xuất hiện ở README/receipt, không có byte artifact để băm | KHÔNG ĐO ĐƯỢC hash/kích thước/đẳng nhất gốc; caveat đã khai rõ vắng, không tính thêm finding |
| P2-DA-VA-CHUA-REVIEW-LAI | Đã áp nguyên hint ở 3bc4244 | `review_probe.py patch_history` (H7): patch -p0 --fuzz=0 rc=0 trên blob parent trong /tmp; kết quả đúng byte 3bc4244 và HEAD | Có về bản vá; “chưa review lại” là lời khai lịch sử, không chứng minh vắng review bên ngoài bằng Git |
| 14 caveat + 3 hàng mục lục | 17 hàng README mới | `review_probe.py index_claims` (H12): 5/4/5 caveat + mỗi verdict 1 hàng; 14 mô tả khớp nguyên nội dung receipt | Có với các caveat đã khai; còn thiếu caveat P1 của H11 |
| Mỏ neo và lời khai con người | Ancestry cũ, người giao việc/submitter/session executor theo (b) | H2/H4 đo được ancestry và commit; không có raw conversation/audit để độc lập xác minh người chỉ thị, ai viết verdict hay tính độc lập thực tế | Phân biệt lời khai và Git; không nâng thành đo máy |
| Cổng bien_nhan_v2 | Đạt | `review_probe.py mandatory_gates` (H9): rc=0; 232 ĐẠT v2, 11/11 legacy, 42 nợ, 0 vi phạm/không đo được, tổng 285; TỔNG: ĐẠT | Có |
| Cổng doctrine-scan | Sạch | H9: rc=0; quét 10 tệp, 0 chỗ chép doctrine | Có |
| Cổng doc-claims-check | ok=true | H9: rc=0; JSON "ok": true; raw stdout/stderr lưu ở review-evidence/gate-2.* | Có |
| t26/t27/t138 | Gọi riêng từng hàm phải đạt | `review_probe.py required_cases` (H10): mỗi hàm chạy riêng trong subprocess, rc=0 và dòng DAT | Có; t138 là ca receipt admission trên kho giả, không phải đo model identity |
| Quét bí mật ba thư mục | Sạch | H10: python3 scripts/pkg_secret_scan.py ops/reviews/<từng thư mục>, rc=0, stdout/stderr rỗng cả ba | Có theo bộ mẫu scanner |
| HINT.patch mới | Caveat sửa surface, giữ nguyên các verdict | `python3 build_hint.py` (H13): dry-run/apply -p0 --fuzz=0 rc=0; t26/t27 đạt trên bản sao; bỏ từng cảnh báo ⇒ t27 FAIL đúng ID | Có trên bản sao; chưa áp trên cây thật |
| Checkout cuối lượt | Chỉ đọc cay-kho/ | `review_probe.py final_integrity` (H15): snapshot cả .git/content/mode/symlink trước/sau bằng nhau, status kể cả ignored rỗng; HEAD/tree giữ nguyên | Có; không gọi mạng/push |

## BẢNG SĂN


### HƯỚNG 1: Neo SHA, cây sạch và diff

  giả thuyết : Có thể đang chấm nhầm cây hoặc diff.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py preflight` (cwd thư mục giao việc)

  output :

```text
HEAD=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f
tree=6f299d7f70269ec32522fc4ea28c9d2d70c5424b
is_shallow=false
core.abbrev=7
status=''
base_sha=50a59a945026a2ab2f97dc0e7ef7b5a540e17652
provided_diff_byte_match=True
provided_numstat_byte_match=True
commits=3bc4244fe5533a71b197a0efb8f79e40175c1a3e
7cfe06212cb43f92d5753940116079e671d9c385
2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f
snapshot_before_files=6211
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 2: Ba biên nhận: byte, OID và số finding

  giả thuyết : Biên nhận có thể lệch hiện vật hoặc lịch sử Git.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py receipts` (cwd thư mục giao việc)

  output :

```text
pr870-review-2-codex:
  sha256=8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6 bytes=79752
  reviewed_sha=06a50c5feea77c2654f31edd26efeed7eeee62f5 tree=0fa694daf17e10c37fc3e61690531ade4bd528bf base=9e9a74b2a396ef458d25c51a5563efafbb45ba0c
  verdict=approve counts=[0, 0, 0, 0]; Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.
  checks={"base_sha": true, "counts": true, "diff_patch": true, "flat_equals_original": true, "git_tree": true, "merge_second_parent": true, "numstat": true, "reviewed_sha": true, "reviewed_tree": true, "run_head": true, "verdict": true, "verdict_bytes": true, "verdict_sha256": true}
  diff_numstat='21\t9\tCLAUDE.md\n'
pr889-review-2-codex:
  sha256=c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612 bytes=34167
  reviewed_sha=094e8d17ae4dfcf21dca63702c9262267bdc072c tree=55f5edf2f8601c976f390e8994193129a71203a1 base=e63961f27b53e66db8e6600009f97d5706743063
  verdict=approve counts=[0, 0, 0, 0]; Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.
  checks={"base_sha": true, "counts": true, "diff_patch": true, "flat_equals_original": true, "git_tree": true, "merge_second_parent": true, "numstat": true, "reviewed_sha": true, "reviewed_tree": true, "run_head": true, "verdict": true, "verdict_bytes": true, "verdict_sha256": true}
  diff_numstat='12\t0\tCLAUDE.md\n'
Traceback (most recent call last):
  File "/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/review_probe.py", line 147, in <module>
    try: globals()[mode]()
         ~~~~~~~~~~~~~~~^^
  File "/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/review_probe.py", line 47, in receipts
    fields={k:re.search(r'^'+k+r':\s*(.+)$',s,re.M).group(1) for k in ['verdict','reviewed_sha','reviewed_tree','base_sha']}
              ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
AttributeError: 'NoneType' object has no attribute 'group'
rc=1
```

  kết luận : CHƯA KẾT LUẬN — xem lỗi phép đo

### HƯỚNG 3: Toàn vẹn và độ đầy đủ SHA256SUMS

  giả thuyết : Manifest có thể sai băm hoặc bỏ sót tệp.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py hashes` (cwd thư mục giao việc)

  output :

```text
pr870-review-2-codex: sha256sum -c SHA256SUMS rc=0; OK=31; manifest=31; files=31; unlisted=[]; missing_files=[]
pr889-review-2-codex: sha256sum -c SHA256SUMS rc=0; OK=22; manifest=22; files=22; unlisted=[]; missing_files=[]
pr896-review-1-codex: sha256sum -c SHA256SUMS rc=0; OK=32; manifest=32; files=32; unlisted=[]; missing_files=[]
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 4: Mỏ neo evidence_url và phạm vi ba commit

  giả thuyết : URL có thể neo commit trộn code với hiện vật.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py provenance` (cwd thư mục giao việc)

  output :

```text
pr870-review-2-codex: evidence_commit=7cfe06212cb43f92d5753940116079e671d9c385; URL_blob_equals_verdict=True
  evidence_commit_files=91 artifacts_only=True receipts=0
pr889-review-2-codex: evidence_commit=7cfe06212cb43f92d5753940116079e671d9c385; URL_blob_equals_verdict=True
  evidence_commit_files=91 artifacts_only=True receipts=0
pr896-review-1-codex: evidence_commit=7cfe06212cb43f92d5753940116079e671d9c385; URL_blob_equals_verdict=True
  evidence_commit_files=91 artifacts_only=True receipts=0
3bc4244: changed_files=1; 50a59a945026a2ab2f97dc0e7ef7b5a540e17652
7cfe062: changed_files=91; 3bc4244fe5533a71b197a0efb8f79e40175c1a3e
2789cbb: changed_files=4; 7cfe06212cb43f92d5753940116079e671d9c385
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 5: Metadata launcher và giới hạn model

  giả thuyết : Thời lượng, prompt hoặc mức assurance có thể bị khai quá.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py run_metadata` (cwd thư mục giao việc)

  output :

```text
pr870-review-2-codex: run=2699e2d8b1a54b8e86bfa3efb9a4b61b duration=496.137 timestamps=496.137080 rc=0 state=xong worktree_sach=True
  prompt_sha256=2c58af0d239a7c590e30c346a719cbcde8cdb124f49ecac9bcb8e094c2dcd5a9; checks={"checkpoint_hash": true, "duration_note": true, "duration_timestamps": true, "ma_thoat": true, "prompt_note": true, "prompt_sha256": true, "run_id": true, "stdout_bytes": true, "stdout_hash": true, "trang_thai": true, "version": true, "worktree_sach": true}
  model_keys=[]; assurance=cross_reviewed assurance_KHONG_dat=cross_approved
  stderr_header_lines=14 full_stderr_declared_bytes=1287629 model/session=['OpenAI Codex v0.163.0', 'model: gpt-6.1-sol', 'reasoning effort: xhigh', 'session id: 01a16ec6-03be-7c62-b0ec-c81586ab4b57']
pr889-review-2-codex: run=d955f9efb3624041b86dcf97f2624175 duration=380.787 timestamps=380.787461 rc=0 state=xong worktree_sach=True
  prompt_sha256=00773f21a7131d479374c5f8bf74b0d9dd65790a030aa731d36d97374daeb8b0; checks={"checkpoint_hash": true, "duration_note": true, "duration_timestamps": true, "ma_thoat": true, "prompt_note": true, "prompt_sha256": true, "run_id": true, "stdout_bytes": true, "stdout_hash": true, "trang_thai": true, "version": true, "worktree_sach": true}
  model_keys=[]; assurance=cross_reviewed assurance_KHONG_dat=cross_approved
  stderr_header_lines=14 full_stderr_declared_bytes=2085807 model/session=['OpenAI Codex v0.163.0', 'model: gpt-6.1-sol', 'reasoning effort: xhigh', 'session id: 01a16ec6-03c2-7890-927d-fe64aa125aa6']
pr896-review-1-codex: run=64761d8e6164462d870c3d534d325dd2 duration=712.54 timestamps=712.539633 rc=0 state=xong worktree_sach=True
  prompt_sha256=27dbb8587c61127252703aac2f1737e38f36e2839f8022763ada9818c5f091c7; checks={"checkpoint_hash": true, "duration_note": true, "duration_timestamps": true, "ma_thoat": true, "prompt_note": true, "prompt_sha256": true, "run_id": true, "stdout_bytes": true, "stdout_hash": true, "trang_thai": true, "version": true, "worktree_sach": true}
  model_keys=[]; assurance=cross_reviewed assurance_KHONG_dat=cross_approved
  stderr_header_lines=14 full_stderr_declared_bytes=1076780 model/session=['OpenAI Codex v0.163.0', 'model: gpt-6.1-sol', 'reasoning effort: xhigh', 'session id: 01a16ec6-03c0-72c0-ac25-dccfeef0cd62']
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 6: Đối chiếu caveat snapshot vắng khỏi kho

  giả thuyết : Có thể chứng minh hash hai snapshot chỉ bằng hiện vật đã lưu.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py snapshot_caveats` (cwd thư mục giao việc)

  output :

```text
tracked_snapshot_files=[]
exact_hash_mentions=['ops/reviews/README.md', 'ops/reviews/pr870-review-2-codex-verdict.receipt.yaml']
artifact_with_claimed_hash=[]
ops/reviews/pr870-review-2-codex/VERDICT.incremental.md:68: snapshot_hashed_files=4843
ops/reviews/pr870-review-2-codex/VERDICT.md:89: snapshot_hashed_files=4843
ops/reviews/pr870-review-2-codex/VERDICT.md:973: Snapshot [trước](review-snapshot-before.json) / [sau](review-snapshot-after.json) bao gồm hash nội dung mọi tệp trong checkout, symlink và HEAD/index/config/packed-refs, cùng diff/index và trạng thái tracked/untracked/ig
ops/reviews/pr870-review-2-codex/evidence-preflight.txt:6: snapshot_hashed_files=4843
ops/reviews/pr870-review-2-codex/review_finalize.py:128:             content += 'Snapshot [trước](review-snapshot-before.json) / [sau](review-snapshot-after.json) bao gồm hash nội dung mọi tệp trong checkout, symlink và HEAD/index/config/packed-refs, cùng diff/index và trạng t
ops/reviews/pr870-review-2-codex/review_probe.py:51:     (OUT / 'review-snapshot-before.json').write_text(json.dumps(snap, ensure_ascii=False, indent=2))
ops/reviews/pr870-review-2-codex/review_probe.py:57:     print('snapshot_hashed_files=' + str(len(snap['files'])))
ops/reviews/pr870-review-2-codex/review_probe.py:304:     before = json.loads((OUT / 'review-snapshot-before.json').read_text())
ops/reviews/pr870-review-2-codex/review_probe.py:306:     (OUT / 'review-snapshot-after.json').write_text(json.dumps(after, ensure_ascii=False, indent=2))
KET_LUAN: KHONG DO DUOC hash/672374 bytes cua hai snapshot goc vi KHONG co byte goc trong hien vat; chi do duoc loi khai + transcript tu chep. Caveat da khai ro KHONG vao kho.
rc=0
```

  kết luận : KHÔNG ĐO ĐƯỢC

### HƯỚNG 2: Ba biên nhận: byte, OID và số finding

  giả thuyết : Biên nhận có thể lệch hiện vật hoặc lịch sử Git.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py receipts` (cwd thư mục giao việc)

  output :

```text
pr870-review-2-codex:
  sha256=8b222ab37b7de41499829abb52d1958043ee8fd2969212596277aacc211026a6 bytes=79752
  reviewed_sha=06a50c5feea77c2654f31edd26efeed7eeee62f5 tree=0fa694daf17e10c37fc3e61690531ade4bd528bf base=9e9a74b2a396ef458d25c51a5563efafbb45ba0c
  verdict=approve counts=[0, 0, 0, 0]; Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.
  checks={"base_sha": true, "counts": true, "diff_patch": true, "flat_equals_original": true, "git_tree": true, "merge_second_parent": true, "numstat": true, "reviewed_sha": true, "reviewed_tree": true, "run_head": true, "verdict": true, "verdict_bytes": true, "verdict_sha256": true}
  diff_numstat='21\t9\tCLAUDE.md\n'
pr889-review-2-codex:
  sha256=c5fe298af73bb6081ecf44638b7fce7e7dd220c11c3ddcee5ba5fcc234a4b612 bytes=34167
  reviewed_sha=094e8d17ae4dfcf21dca63702c9262267bdc072c tree=55f5edf2f8601c976f390e8994193129a71203a1 base=e63961f27b53e66db8e6600009f97d5706743063
  verdict=approve counts=[0, 0, 0, 0]; Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.
  checks={"base_sha": true, "counts": true, "diff_patch": true, "flat_equals_original": true, "git_tree": true, "merge_second_parent": true, "numstat": true, "reviewed_sha": true, "reviewed_tree": true, "run_head": true, "verdict": true, "verdict_bytes": true, "verdict_sha256": true}
  diff_numstat='12\t0\tCLAUDE.md\n'
pr896-review-1-codex:
  sha256=3feaad3e207ae2dea5323cb6f831ba2980546ec1d3febeead6d415baccbbb803 bytes=63341
  reviewed_sha=816f43988eb3012726120ad00166a989cc2b9af6 tree=3da0ce24590dfcf2e60805b2bef76687cdd64405 base=1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e
  verdict=changes_requested counts=[0, 0, 1, 0]; Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.
  checks={"base_sha": true, "counts": true, "diff_patch": true, "flat_equals_original": true, "git_tree": true, "merge_second_parent": true, "numstat": true, "reviewed_sha": true, "reviewed_tree": true, "run_head": true, "verdict": true, "verdict_bytes": true, "verdict_sha256": true}
  diff_numstat='31\t34\tCLAUDE.md\n27\t0\tops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml\n3\t0\tops/land/pr889-claude-md-bai-hoc-c-provenance/SHA256SUMS.txt\n6\t0\tops/land/pr889-claude-md-bai-hoc-c-provenance/readback-blob-claude-md-094e8d1-6ac385f.txt\n436\t0\tops/land/pr889-claude-md-bai-hoc-c-provenance/readback-comments-889-sau-review-lai.json\n29\t0\tops/land/pr889-claude-md-bai-hoc-c-provenance/readback-reactions-pr-889-sau-review-lai.json\n'
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 7: Tái lập nguyên HINT.patch cũ tại commit sửa

  giả thuyết : Caveat có thể dẫn sai commit hoặc bản vá khác hint.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py patch_history` (cwd thư mục giao việc)

  output :

```text
patch -p0 --fuzz=0 rc=0; patching file CLAUDE.md
HINT_result_equals_3bc4244=True; equals_reviewed_HEAD=True
hint_commit=3bc4244fe5533a71b197a0efb8f79e40175c1a3e
pr870-review-2-codex: prior_P2_note=(a) Luot truoc: pr870-review-1-codex (changes_requested tren b38fce8; P2 da va o 06a50c5).
pr889-review-2-codex: prior_P2_note=(a) Luot truoc: pr889-review-1-codex (changes_requested tren 8d5cccb; P2 da va o 094e8d1).
pr896-review-1-codex: prior_P2_note=(a) Luot truoc: khong co cross-review CLI truoc; Codex connector P2 tren 0bb792b da va o 816f439.
CHUA_REVIEW_LAI la loi khai trang thai luc ghi so; khong suy tu lich su Git rang khong he co review ngoai kho.
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 8: Đột biến độc lập exclude, needs, if và output os

  giả thuyết : Câu mới có thể khai rộng hơn t162 hoặc chốt G5 thực sự kiểm.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py workflow` (cwd thư mục giao việc)

  output :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
actual_gate_cong_cu_prefix_jobs=['gate-cong-cu', 'gate-cong-cu-gop']
g5_shard=gate-cong-cu; g5_aggregate=gate-cong-cu-gop; all_prefix_jobs_covered=True
chuan_bi.outputs.os='${{ (github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\') && \'["windows-latest"]\' || (github.event_name == \'workflow_dispatch\' || contains(github.event.pull_request.labels.*.name, \'windows\')) && \'["ubuntu-latest","windows-latest"]\' || \'["ubuntu-latest"]\' }}'
gate-cong-cu: {"if": "${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", "needs": "chuan-bi", "strategy": {"fail-fast": false, "matrix": {"exclude": [{"manh": 1, "os": "windows-latest"}, {"manh": 2, "os": "windows-latest"}, {"manh": 3, "os": "windows-latest"}, {"manh": 4, "os": "windows-latest"}, {"manh": 5, "os": "windows-latest"}, {"manh": 6, "os": "windows-latest"}, {"manh": 7, "os": "windows-latest"}], "manh": [0, 1, 2, 3, 4, 5, 6, 7], "os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}}}
gate-cong-cu-gop: {"if": "${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", "needs": ["chuan-bi", "gate-cong-cu"], "strategy": {"fail-fast": false, "matrix": {"exclude": [{"os": "windows-latest"}], "os": "${{ fromJson(needs.chuan-bi.outputs.os) }}"}}}
baseline: t162=PASS; loi_g5_workflow_errors=0
gate-cong-cu__remove_exclude: t162=PASS; loi_g5_workflow_errors=1
  gate-cong-cu: matrix phải đúng os + manh [0, 1, 2, 3, 4, 5, 6, 7] + exclude [{'os': 'windows-latest', 'manh': 1}, {'os': 'windows-latest', 'manh': 2}, {'os': 'windows-latest', 'manh': 3}, {'os': 'windows-latest', 'manh': 4}, {'os': 'windows-latest', 'manh': 5}, {'os': 'windows-latest', 'manh': 6}, {'os': 'windows-latest', 'manh': 7}], thấy {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': [0, 1, 2, 3, 4, 5, 6, 7]}
gate-cong-cu__remove_needs: t162=PASS; loi_g5_workflow_errors=1
  gate-cong-cu: needs/if phải đúng 'chuan-bi'/"${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", thấy None/"${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}"
gate-cong-cu__remove_if: t162=PASS; loi_g5_workflow_errors=1
  gate-cong-cu: needs/if phải đúng 'chuan-bi'/"${{ needs.chuan-bi.outputs.che_do != 'duong_nhanh' }}", thấy 'chuan-bi'/None
gate-cong-cu-gop__remove_exclude: t162=PASS; loi_g5_workflow_errors=1
  gate-cong-cu-gop: matrix phải đúng os + exclude [{'os': 'windows-latest'}], thấy {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
gate-cong-cu-gop__remove_needs: t162=PASS; loi_g5_workflow_errors=1
  gate-cong-cu-gop: needs/if phải đúng ['chuan-bi', 'gate-cong-cu']/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", thấy None/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}"
gate-cong-cu-gop__remove_if: t162=PASS; loi_g5_workflow_errors=1
  gate-cong-cu-gop: needs/if phải đúng ['chuan-bi', 'gate-cong-cu']/"${{ !cancelled() && contains(fromJson(needs.chuan-bi.outputs.os), 'ubuntu-latest') }}", thấy ['chuan-bi', 'gate-cong-cu']/None
output_os__remove_windows_only_branch: t162=FAIL; loi_g5_workflow_errors=0
  t162_assertion=dispatch windows-only phải chỉ chạy windows-latest, nhận được: ['ubuntu-latest', 'windows-latest']
KET_LUAN: t162 chi doc outputs.os tu workflow; exclude/needs/if cua CA HAI job manh/gom co chot rieng. Khong khai moi gate* deu duoc loi_g5_workflow bao phu.
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 9: Ba cổng bắt buộc trên exact checkout

  giả thuyết : Gate có thể đỏ, hoặc JSON thiếu ok=true.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py mandatory_gates` (cwd thư mục giao việc)

  output :

```text
command=python3 ops/bien_nhan_v2.py --root .; rc=0
  stdout_tail=['', 'bien_nhan_v2: 232 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 285', 'TỔNG: ĐẠT']; stderr_tail=[]
command=python3 .claude/dev/packet_loop.py doctrine-scan --root .; rc=0
  stdout_tail=['doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine']; stderr_tail=[]
command=python3 scripts/tl.py doc-claims-check --json; rc=0
  ok=true; JSON_keys=['ok', 'schema', 'roots', 'files_scanned', 'claims_flagged', 'flags', 'advisories', 'by_layer', 'advisory_count', 'layers', 'layers_skipped', 'basis', 'strict']
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 10: Gọi riêng t26/t27/t138 và quét bí mật

  giả thuyết : Hiện vật có thể làm hỏng kiểm biên nhận, mục lục, hoặc chứa bí mật.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py required_cases` (cwd thư mục giao việc)

  output :

```text
t26_: rc=0; stdout='t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi: DAT (goi rieng ham)\n'; stderr="ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\\s'\n  2. **Nhận nhầm văn xuôi.** `^\\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một\nops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\\d'\n  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ\n"
t27_: rc=0; stdout='t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: DAT (goi rieng ham)\n'; stderr="ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\\s'\n  2. **Nhận nhầm văn xuôi.** `^\\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một\nops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\\d'\n  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ\n"
t138_: rc=0; stdout='t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR: DAT (goi rieng ham)\n'; stderr="ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\\s'\n  2. **Nhận nhầm văn xuôi.** `^\\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một\nops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\\d'\n  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ\n"
python3 scripts/pkg_secret_scan.py ops/reviews/pr870-review-2-codex: rc=0; stdout=''; stderr=''; SACH (rc=0, khong co phat hien)
python3 scripts/pkg_secret_scan.py ops/reviews/pr889-review-2-codex: rc=0; stdout=''; stderr=''; SACH (rc=0, khong co phat hien)
python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-1-codex: rc=0; stdout=''; stderr=''; SACH (rc=0, khong co phat hien)
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 11: Tự khai bề mặt chạy trong verdict so launcher

  giả thuyết : Metadata tự khai trong hiện vật có thể trái launcher và thiếu đính chính.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py identity_claims` (cwd thư mục giao việc)

  output :

```text
pr870-review-2-codex: VERDICT.md:9: execution_surface: codex_service (agent có công cụ shell; không phải ChatGPT Web)
  run.json:47 execution_surface=codex_cli; lenh={"chuong_trinh": "codex", "so_doi_so": 9, "van_tay": "b1e1e9e45b5742c2"}
  receipt model_reviewer_identity.surface=codex_cli
  caveat_ids=['HO-MODEL-REVIEWER-KHONG-DO-DUOC', 'STDERR-CHI-GIU-HEADER', 'CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY', 'SCRIPT-DO-DOC-DUONG-DAN-SANDBOX', 'SNAPSHOT-CAY-KHONG-VAO-KHO']
  service_in_caveat=False
pr889-review-2-codex: VERDICT.md:9: Quyền và phạm vi theo chỉ thị trực tiếp `runs/d955f9ef/prompt.snapshot`. Reviewer: Codex, họ model OpenAI/GPT-6; provider `openai_codex`, execution surface `codex_service`, transport `machine` theo phân loại repository cho agent có shell không chạy qua `codex exec`/Desktop. Không có receipt máy để chứng nhận biến thể model/effort hoặc assurance. Không gọi mạng, không push, không sửa `cay-kho/`; chỉ ghi artifact ở thư mục cha.
  run.json:47 execution_surface=codex_cli; lenh={"chuong_trinh": "codex", "so_doi_so": 9, "van_tay": "4f5bee90d5c1511a"}
  receipt model_reviewer_identity.surface=codex_cli
  caveat_ids=['HO-MODEL-REVIEWER-KHONG-DO-DUOC', 'STDERR-CHI-GIU-HEADER', 'CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY', 'SCRIPT-DO-DOC-DUONG-DAN-SANDBOX']
  service_in_caveat=False
pr896-review-1-codex: VERDICT.md:7: Reviewer `codex`; provider `openai_codex`; execution_surface `codex_cli`; transport `machine`. Run `64761d8e6164462d870c3d534d325dd2`; header CLI khai `gpt-6.1-sol`, effort `xhigh`, session `01a16ec6-03c0-72c0-ac25-dccfeef0cd62` (đọc `runs/64761d8e/run.json` và đầu `stderr.log`; header không chứng minh model phục vụ ở máy chủ). Không có GitHub submitter vì không đăng/push. Sandbox khai `workspace-write`; read-only đối với `cay-kho/` được giữ bằng phạm vi lệnh, bytecode bị tắt. Không gọi mạng, không dùng subagent, không sửa nguồn review.
  run.json:47 execution_surface=codex_cli; lenh={"chuong_trinh": "codex", "so_doi_so": 9, "van_tay": "2abc89c910586650"}
  receipt model_reviewer_identity.surface=codex_cli
  caveat_ids=['HO-MODEL-REVIEWER-KHONG-DO-DUOC', 'STDERR-CHI-GIU-HEADER', 'CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY', 'SCRIPT-DO-DOC-DUONG-DAN-SANDBOX', 'P2-DA-VA-CHUA-REVIEW-LAI']
  service_in_caveat=False
policy: ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:39-51 phan biet codex_cli va codex_service; lich su codex exec giu codex_cli.
README:5-11 giu nguyen verdict co bam, dua dinh chinh vao verdict_usage_caveats va bang canh bao.
KET_LUAN: LOI — pr870 luot2 va pr889 luot2 khai sai codex_service trong ca ban phang va ban thu muc; pr889 con phu nhan chay qua codex exec; chua co caveat dinh chinh surface. Mot lop loi, hai hien vat review.
rc=0
```

  kết luận : LỖI

### HƯỚNG 12: 17 hàng README so từng biên nhận

  giả thuyết : Mục lục có thể sai số hàng, thiếu caveat hoặc chép khác mô tả.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py index_claims` (cwd thư mục giao việc)

  output :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
pr870-review-2-codex: caveat_rows=5; index_rows=1; receipt_caveats=5
  HO-MODEL-REVIEWER-KHONG-DO-DUOC: text_matches_receipt=True
  STDERR-CHI-GIU-HEADER: text_matches_receipt=True
  CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY: text_matches_receipt=True
  SCRIPT-DO-DOC-DUONG-DAN-SANDBOX: text_matches_receipt=True
  SNAPSHOT-CAY-KHONG-VAO-KHO: text_matches_receipt=True
pr889-review-2-codex: caveat_rows=4; index_rows=1; receipt_caveats=4
  HO-MODEL-REVIEWER-KHONG-DO-DUOC: text_matches_receipt=True
  STDERR-CHI-GIU-HEADER: text_matches_receipt=True
  CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY: text_matches_receipt=True
  SCRIPT-DO-DOC-DUONG-DAN-SANDBOX: text_matches_receipt=True
pr896-review-1-codex: caveat_rows=5; index_rows=1; receipt_caveats=5
  HO-MODEL-REVIEWER-KHONG-DO-DUOC: text_matches_receipt=True
  STDERR-CHI-GIU-HEADER: text_matches_receipt=True
  CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY: text_matches_receipt=True
  SCRIPT-DO-DOC-DUONG-DAN-SANDBOX: text_matches_receipt=True
  P2-DA-VA-CHUA-REVIEW-LAI: text_matches_receipt=True
new_caveat_rows=14; new_index_rows=3; total=17
KET_LUAN: 17 hang khop bien nhan; t27 chi kiem cac id DA KHAI, khong phat hien caveat can them cho sai surface (Huong11).
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### verdict-khai-sai-execution-surface  [P1]  Hai verdict tự khai sai bề mặt chạy, chưa có caveat đính chính

TỆP/DÒNG:
- `ops/reviews/pr870-review-2-codex-verdict.md:9` và bản nguyên byte `ops/reviews/pr870-review-2-codex/VERDICT.md:9`.
- `ops/reviews/pr889-review-2-codex-verdict.md:9` và bản nguyên byte `ops/reviews/pr889-review-2-codex/VERDICT.md:9`.
- Nơi bổ sung đính chính: `ops/reviews/pr870-review-2-codex-verdict.receipt.yaml:91`, `ops/reviews/pr889-review-2-codex-verdict.receipt.yaml:91`, `ops/reviews/README.md:701` và `:706`.

VẤN ĐỀ: Hai verdict vừa đưa vào kho đều khai `codex_service`. Verdict #889 còn giải thích rằng agent “không chạy qua `codex exec`/Desktop”. Tại chính SHA được chấm, hai `run/run.json:47` ghi `execution_surface: codex_cli`; `lenh.chuong_trinh` là `codex`, header là `OpenAI Codex v0.163.0`, và chính biên nhận mới ghi `model_reviewer_identity.surface: codex_cli`. Đây là mâu thuẫn về bề mặt chạy có bằng chứng tại chỗ, độc lập với việc KHÔNG ĐO ĐƯỢC model phía máy chủ. Chính sách `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:39–51` phân biệt rõ hai bề mặt, giữ các lượt `codex exec` là CLI.

Biên nhận khai trường surface đúng, nhưng không đính chính câu sai trong `verdict_usage_caveats`; README cũng không cảnh báo mâu thuẫn ấy. `ops/reviews/README.md:5–11` quy định đính chính bản nguyên văn có băm phải nằm trong caveat và được nâng lên bảng cảnh báo. Caveat về họ model hiện có không nói tới `codex_service`, nên không sửa được mệnh đề sai khác này. Một lớp lỗi, hai hiện vật review, đếm một P1 theo định nghĩa của chỉ thị: khẳng định sai về sự thật đo được tại HEAD. Không yêu cầu đổi kết quả review lịch sử 0/0/0/0 hay nâng assurance.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py identity_claims` (H11), rc=0: cả hai bản ghi nguyên văn `codex_service`, launcher/receipt `codex_cli`, `service_in_caveat=False`; #896 làm đối chứng có surface nhất quán. H9/H10 cho thấy mọi cổng bắt buộc và t26/t27/t138 vẫn xanh: các cổng đó không phát hiện nghĩa của mâu thuẫn metadata này.

GỢI Ý VÁ:
- Vá ở đâu: thêm caveat `VERDICT-KHAI-SAI-EXECUTION-SURFACE` vào hai sidecar trên và hai hàng tương ứng trong README. Giữ nguyên các bản verdict, băm, số finding lịch sử và các manifest; đây là bản ghi nguyên văn được bảo toàn.
- Vá thế nào: chỉ rõ câu sai ở dòng 9, dẫn run ID và trường surface trong launcher, đính chính thành `codex_cli`. Ghi rõ đính chính surface không chứng nhận model/effort. `HINT.patch` thực hiện cách vá này trên ba tệp.
- Ca khoá: trên bản sao ngoài checkout, áp hint với `patch -p0 --fuzz=0`; gọi riêng t26/t27 phải xanh. Xoá từng hàng cảnh báo mới khỏi README nhưng giữ caveat: t27 phải đỏ, nêu đúng ID và đúng verdict. Đã chạy hai đột biến, đều đỏ đúng lý do; xem H13.
- Rủi ro bản vá: vô tình sửa verdict lịch sử sẽ làm lệch hash; sửa assurance thành `cross_approved` sẽ khai quá khả năng xác minh. Hint chỉ bổ sung caveat/mục lục. Các cổng sẵn có giữ ID đã khai, không chứng minh tự phát hiện mọi câu surface sai mới.

ĐỘ TIN: cao.

### HƯỚNG 13: Kiểm HINT.patch và hai đột biến mất cảnh báo trên bản sao

  giả thuyết : Gợi ý có thể không áp được bằng patch -p0, phá băm verdict, hoặc không được t27 bảo vệ.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 build_hint.py > review-evidence/hint-check.log 2>&1` (cwd thư mục giao việc; mọi thay đổi thử ở /tmp/pr915-hint-check-*).

  output :

```text
HINT.patch files=3; paths=['ops/reviews/README.md', 'ops/reviews/pr870-review-2-codex-verdict.receipt.yaml', 'ops/reviews/pr889-review-2-codex-verdict.receipt.yaml']
patch --dry-run -p0 --fuzz=0 rc=0; 'checking file ops/reviews/README.md\nchecking file ops/reviews/pr870-review-2-codex-verdict.receipt.yaml\nchecking file ops/reviews/pr889-review-2-codex-verdict.receipt.yaml\n'
patch -p0 --fuzz=0 rc=0
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi: DAT tren ban sao da ap hint
t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: DAT tren ban sao da ap hint
remove_new_README_caveat pr870-review-2-codex: t27 FAIL; README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr870-review-2-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr870-review-2-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.
remove_new_README_caveat pr889-review-2-codex: t27 FAIL; README.md: caveat 'VERDICT-KHAI-SAI-EXECUTION-SURFACE' của pr889-review-2-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr889-review-2-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.
KET_LUAN: patch hop le; t26/t27 nen xanh; hai dot bien bo canh bao deu do; khong sua hien vat verdict/hash.
```

  kết luận : KHÔNG PHẢI LỖI của hint; đã kiểm bản sao. Hint chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit.

### HƯỚNG 14: AST và ca t161 đối chiếu phạm vi câu văn

  giả thuyết : Có thể t162 đọc thêm trường workflow, hoặc t161 thật sự đánh giá biểu thức.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py static_scope` (cwd thư mục giao việc)

  output :

```text
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:2961: SyntaxWarning: invalid escape sequence '\s'
  2. **Nhận nhầm văn xuôi.** `^\s*#.*NỢ CÓ TÊN` cho phép chữ tuỳ ý chen trước cụm, nên một
/tmp/claude-0/-home-user-tra-luat/008916a5-97d8-5ef4-ac28-34381e972d65/scratchpad/cr3-pr915.iS5d/cay-kho/ops/lease_publish_test.py:5104: SyntaxWarning: invalid escape sequence '\d'
  KHÔNG neo đầu dòng là `lease_publish: (\d+)/(\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ
t162 workflow reads=['wf_ci = HERE.parent / ".github" / "workflows" / "ci.yml"', 'wf_data = yaml.safe_load(wf_ci.read_text(encoding="utf-8"))', 'raw_expr = wf_data["jobs"]["chuan-bi"]["outputs"]["os"]']
t162 wf_data direct accesses=["wf_data['jobs']"]
t161 evaluator_calls=0
t161_M3_chot_nguon_duy_nhat_ma_tran_ci: DAT
python=3.13.16; PyYAML=6.0.3; platform=linux
rc=0
```

  kết luận : KHÔNG PHẢI LỖI

### HƯỚNG 15: Toàn vẹn checkout cuối lượt

  giả thuyết : Phép đo có thể đã ghi bytecode, đổi Git metadata hoặc làm bẩn cây nguồn.

  lệnh : `PYTHONDONTWRITEBYTECODE=1 python3 review_probe.py final_integrity` (cwd thư mục giao việc)

  output :

```text
snapshot_before_files=6211; snapshot_after_files=6211
added=[]; removed=[]; changed_content_or_mode=[]
status_with_ignored=''; HEAD=2789cbb6a0c7ded65fc4e448de7f24b7fe4b425f
tree=6f299d7f70269ec32522fc4ea28c9d2d70c5424b
KET_LUAN: toan bo byte, quyen tep va symlink trong cay-kho/ (gom .git) giu nguyen; khong network/push trong luot nay.
rc=0
```

  kết luận : KHÔNG PHẢI LỖI


## Kết luận kiểm tra bắt buộc

| Lệnh (cwd cay-kho/) | rc | Dòng kết luận thật |
|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | 0 | `bien_nhan_v2: 232 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 285`; `TỔNG: ĐẠT` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | JSON `"ok": true` |
| Gọi riêng `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi()` | 0 | `DAT (goi rieng ham)` |
| Gọi riêng `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc()` | 0 | `DAT (goi rieng ham)` |
| Gọi riêng `t138_A12_bien_nhan_receipt_du_truong_va_neo_doc_lap_cay_PR()` | 0 | `DAT (goi rieng ham)` |
| `python3 scripts/pkg_secret_scan.py ops/reviews/pr870-review-2-codex` | 0 | stdout/stderr rỗng; không phát hiện |
| `python3 scripts/pkg_secret_scan.py ops/reviews/pr889-review-2-codex` | 0 | stdout/stderr rỗng; không phát hiện |
| `python3 scripts/pkg_secret_scan.py ops/reviews/pr896-review-1-codex` | 0 | stdout/stderr rỗng; không phát hiện |

Đã kiểm HINT trên bản sao, không áp vào cay-kho/. Snapshot cuối xác nhận nguồn và .git không đổi. Hai snapshot gốc #870 và full stderr lịch sử vắng khỏi kho: không xác nhận hash/byte của dữ liệu không được giao. Các giới hạn ấy đã được caveat công khai; finding yêu cầu sửa ở lượt này chỉ là mâu thuẫn surface chưa được đính chính.
