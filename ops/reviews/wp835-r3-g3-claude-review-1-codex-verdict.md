VERDICT: changes_requested
Reviewed commit: 3785f9535398db04fb36a5eaa095166a8e048f1e

Reviewed tree: fd0c97ff1ae2f5e595502ada69dc2d449fdebbcd
Acceptance base: d2e3052d479d140b7e7b91df41ec4914fab7d544
Base tree: bf2449d9ab695a6ddfdd75575d75186e9ac981b3
Packet: wp835, revision 3, generation 3; sensitive; lượt 1 của r3/g3.
Review axes: spec, standards_security. Ngưỡng approval áp dụng: không còn P0/P1/P2.

## Finding — 1 lớp, 1 finding P2

**WP835-R3-01 — P2 — `dac-ta-ratchet-docs-da-loi-thoi`: cần revision acceptance trước khi bỏ yêu cầu ratchet.**

Vị trí: `docs/adr/0056-lease-no-progress-six-hours.md:41`–43; hợp đồng nguồn trên lease ref: `ops/specs/wp835-lease-6h-governance-r3.md:34`–37 và :46–47.

Executor đúng về kỹ thuật: trên base đã không còn ratchet số tài liệu để tăng. Nhưng spec r3 không chỉ cho phép sửa tối đa bốn tệp: D3 yêu cầu kê khai/tăng ratchet, N4 còn yêu cầu phản chứng **bỏ sửa ratchet phải làm r291 đỏ**. Spec :7–9 ghi quyết định chủ kho “Thêm hai tệp”. Phép đo dưới đây chứng minh yêu cầu phản chứng ấy không đúng trên base được đóng băng. Giữ nguyên hai tệp là hợp lý cho sản phẩm, nhưng không thể tự coi đó là hoàn thành N4. Đoạn provenance mới ở ADR :41 vẫn gọi companion là “ratchet đếm tài liệu”, dù ratchet đó đã bị bỏ từ #794.

Bằng chứng độc lập, script Python trích và chạy đúng hàm `_c291_docs_ngoai_goi` bằng AST, dùng `tl_core.release` thật, `_ROOT209` lần lượt trỏ base/head hoặc fixture ngoài checkout; rc 0:

```text
CONSUMER_IDENTICAL True
base docs_md 79 r291 True
head docs_md 80 r291 True
BASE_CONSUMER_ON_HEAD_UNCHANGED_RATCHET True
EXTRA_DOC 81 r291 True
PACKAGE_RATCHET_192_TO_193 r291 False
```

Hai blob không đổi giữa base/head:

```text
scripts/tl_selftest.py  a1c861d8b148a4cbb713ed380553d892c8c25cca
RELEASE_MANIFEST.json  3dddd00f6b45dd27c5f307e9f289be8599f6af6a
```

Cách đo: đọc AST từ `scripts/tl_selftest.py`, lấy duy nhất FunctionDef tên `_c291_docs_ngoai_goi`; compile/exec với `_ROOT209`, `_rel209=tl_core.release`, `_j209=json`; gọi hàm. Fixture sao chép `docs/` và manifest của head rồi thêm một Markdown bình thường. Đột biến chỉ thay duy nhất `len(paths) == 192` thành `len(paths) == 193` trong consumer trích ra. Đây là probe consumer, không phải lời khai đã chạy full suite trên từng biến thể. Full suite trên base/head cũng đều báo `[OK] r291_docs_ngoai_goi`.

- **Vá ở đâu:** người điều phối/chủ kho sửa hợp đồng D3/N4 tại nguồn spec, rồi cập nhật provenance ADR :41–43 theo quyết định ấy. Không sửa harness để tạo lại một bất biến giả.
- **Vá thế nào:** đường rẻ nhất là revision được chủ kho chấp thuận, ghi companion không cần đổi trên base này, thay phản chứng N4 bằng các thuộc tính thực sự còn hiệu lực; cập nhật spec hash/lease/generation theo protocol §3.2. Reviewer không có quyền cấp ngoại lệ này. Tái sinh manifest chỉ cần khi nội dung tệp trong gói thực sự đổi.
- **Ca khóa:** bảo toàn phép đo base/head, thêm tài liệu vẫn xanh và ratchet gói sai phải đỏ; nghiệm thu full selftest N/N trong runtime tạo được fixture Git. Điều kiện N4 cũ phải được thay bằng authority có vết trước khi đóng finding; chỉ suite xanh không đóng được bất nhất hợp đồng.
- **Rủi ro của cách vá:** miễn cả các companion khi runtime trong gói thật sự đổi, hoặc hợp thức hóa bỏ acceptance bằng lời khai executor. Revision cần ghi rõ phạm vi ngoại lệ chỉ là ratchet docs đã được bỏ trên base này.

Mức P2 vì đây là sai lệch hợp đồng nghiệm thu và provenance cần giải quyết trước approval; chưa thấy thay đổi runtime hay kích hoạt lease 360 phút trái phép. Không có P0/P1/P3 mới. Hai biểu hiện của cùng lớp là N4 bất khả dụng và mô tả ratchet docs tại ADR; không tách thành nhiều finding để đếm lặp.

**Trả lời câu hỏi lệch đặc tả: (b).** Write set tự nó là trần, không phải sàn; chỉ việc diff có hai thay vì bốn tệp không buộc xin phép. Ở đây còn có yêu cầu nội dung D3 và acceptance âm N4 tường minh, nên cần chủ kho chấp thuận revision cho phần ấy. Không nên tăng 192→193 hay dựng lại ratchet docs chỉ để thỏa văn bản cũ.

## Neo spec, lease và môi trường

Đọc blob bằng `git show <ref>:<path>` và tự SHA-256 bytes bằng `hashlib.sha256`; cả hai lệnh/đối chiếu rc 0:

| Nguồn authoritative | Commit ref đã đọc | Blob | SHA-256 |
|---|---|---|---|
| r3, `origin/ops/wp835-r3-g3-lease:ops/specs/wp835-lease-6h-governance-r3.md` | 74072a3d7958986a04bce647554251ab5f870e9d | 2b5a27da98f87cf3c5c001f2653812f875c986fc | 71403df80d133e4568cb891ae5ab41de937a9d1d1086a92f7255323568596ddc |
| r2, `origin/ops/wp835-r2-g2-lease:ops/specs/wp835-lease-6h-governance-r2.md` | b294226de35761b99e8c88922e632fd71d01d48e | 479992490f4ef8642882c6f3c358cc178fadf0fd | da98e225c1e0bb419b83c368d2b3112309bd95316a4787c18f91f79bdbc57833 |

Đọc lại r3 tại OID ghim `df88ca47bed9f9b0423969737d4468be3b9a0726` và r2 tại `53cf373` cũng cho đúng hai hash trên. Không có local spec copy ở product tree; không chép spec vào checkout.

Lease `ops/leases/wp835-r3-g3-claude.yaml` trên ref r3 khớp revision/generation/spec/base, class sensitive và reviewer Codex CLI. Tự tính write-set hash theo công thức trong lease cho `fa59517725ec0632dc7584988b0fbea3a15b0e265fe7a7c591a3bb989f05b929`, khớp. Bốn đường sản phẩm là protocol, ADR-0056, selftest và manifest; handoff chỉ trên nhánh lease. Diff thực tế nằm trong tập này: **2 tệp, +61 −3**, dưới trần 4 tệp/200 dòng thêm.

Repository origin: `https://github.com/ducthangho/tra-luat.git`; checkout detached đúng reviewed SHA. Local `origin/master=cdc4e80bc439fa974775f319dccac5bf2fc955fe`; `git diff --name-only <base> origin/master` chỉ có `ops/land/**`. Đây là cache offline, không phải phép đo remote còn tươi. Lease ghi hạn tuyệt đối `2026-10-27T14:58:00Z`; trạng thái/heartbeat live không được kiểm qua GitHub.

Runtime: Linux x86_64, Python `/usr/bin/python` 3.13.17; Git 2.43.0; ripgrep 15.2.0. `core.abbrev=7` trong checkout được giao và hai clone thử nghiệm. Có yaml/requests/cryptography; không có module Ruff. Hai clone base/head được dựng cùng một script, cùng quy trình `git clone --no-hardlinks --no-checkout`, checkout exact OID, ghim abbrev; không fetch mạng.

## Phép đo gate

Lệnh Python dùng `-B`/`PYTHONDONTWRITEBYTECODE=1`; cache ngoài checkout. Full suite chạy tuần tự trong hai clone scratch `/tmp/wp835-review-958a0a8a-6zcp923z/{base,head}`, không chạy đồng thời heavy gate. Các lệnh dưới đọc đúng candidate/base đã neo; không sửa checkout được review.

| Tiêu chí / lệnh | rc thật | Bằng chứng và disposition |
|---|---:|---|
| N2: `python -B .claude/dev/packet_loop.py adr-song --root .` | 0 | **passed**: 55 ADR trên đĩa, 55 dòng §20, khớp 1:1; ngoại lệ trạng thái ADR-0016 có sẵn |
| N3: `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | **passed**: quét 10 tệp, 0 chỗ chép doctrine |
| N3: `git diff --check d2e3052d479d140b7e7b91df41ec4914fab7d544 3785f9535398db04fb36a5eaa095166a8e048f1e` | 0 | **passed**: output rỗng |
| N4: `python -B scripts/tl.py --selftest`, head | 1 | **failed**: `== tl selftest 1729/1731 ==`; 243.20 s; r291 OK |
| Đối chứng cùng lệnh, base | 1 | **failed**: `== tl selftest 1729/1731 ==`; 234.49 s; r291 OK; tập FAIL bằng head, delta 0 |
| N4: probe consumer AST mô tả ở finding | 0 | **passed phép đo**: không sửa ratchet vẫn xanh; **failed yêu cầu phản chứng N4 hiện hành** |
| N5: `python -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, head | 0 | **passed**: `ok=true`, expected=checked=192, failed/extra/missing/required_missing đều rỗng |
| N5: `python -B scripts/tl.py doc-claims-check --strict --json`, base và head | 2 / 2 | **failed cả hai lần chạy**; **passed tiêu chí delta=0**: cùng 1 hard flag và cùng 396 advisories, danh sách bằng nhau hoàn toàn; files_scanned 114→115 |
| Ruff pin/probe contract: `runpy.run_path('.claude/dev/ci_dang_ky_test.py')['loi_ruff_ci']()`; thoát theo errors/count | 0 | **passed riêng contract**: `RUFF_CONTRACT 3 []`; không phải bare lint |
| `python -m ruff --version` | 1 | `No module named ruff`; bare lint **not_run**, không cài công cụ hay đổi bootstrap để che giới hạn |

Hai FAIL selftest trên cả hai cây:

```text
[FAIL] r226_nguong_l2_troi_theo_abbrev_va_ci_ghim
[FAIL] r268_l2_trichotomy_theo_trang_thai_object
[OK] r291_docs_ngoai_goi
== tl selftest 1729/1731 ==
```

Tái chạy riêng hai FunctionDef gốc với observer chỉ ghi nhận kết quả `subprocess.run`, không đổi kết quả trả về: cả hai trả False; các `git -c user.email=t@t -c user.name=t commit -q -m c1/c2` của fixture đều rc 128, stderr có `socket: operation not permitted` khi công cụ ký commit gọi MCP localhost. Một mini-repo độc lập cũng đo `init/add` rc 0, `commit` rc 128, `rev-parse HEAD` rc 128. Không tắt ký commit hoặc nới sandbox để ép xanh. Vì vậy bằng chứng executor `1731/1731` **không tái lập được trong runtime này**; không gọi N4 positive passed dù delta đỏ bằng 0.

Hard flag doc-claims chung: `docs/AUDIT_LAUNCHER_VONG_3.md:462`, claim `f08e45b`, `SHA_NOT_A_COMMIT`. `git cat-file -t f08e45b` rc 128; clone được cấp là shallow. Có thể do độ sâu, chưa chứng minh lịch sử đầy đủ; không quy thành hồi quy của patch.

Log selftest đã đối chiếu SHA-256 với result JSON bằng tl-auditor chỉ đọc, theo CLAUDE.md bước 5:

- Head: 78,396 bytes; `5fe555ab0d233a3ff7f62bc631474d8245480af74e610c6d96771d869980c352`.
- Base: 78,396 bytes; `dfc93ac1142261a554cc6bf9b9b010788fa406a2f2e9cf02a0cd5521ac46ad80`.

Các kết quả N/N dùng marker tổng cuối; không lấy tổng số dòng `[OK]` vì log có suite con.

## Đối chiếu các lớp nội dung

1. **N1 / biên lease:** đọc diff base/head và so nguyên đoạn `review_sla` sau khi chỉ chuẩn hóa đúng phần đổi ngưỡng: bằng nhau. Mẫu lease thêm 360 có điều kiện sau activation; §4 chỉ áp lease mới, lease cũ giữ giá trị đã đóng dấu. `lease_until` tuyệt đối, generation, fencing/bia mộ, exact head được bảo toàn và nêu rõ; đoạn worker stale/cấm cherry-pick giữ nguyên. Heartbeat 15 phút sau changes_requested, review_sla +2 giờ, xử lý thiếu/mơ hồ và hết SLA giữ nguyên. Không lease YAML nào đổi. Đây là đối chiếu văn bản, không là thử controller vận hành.
2. **Đổi số và §20:** lấy changed-line streams của `git diff 062292b2c75be8c316a0cf7347290574efa10861 a62ba1f38abe1f4d4f33181d0898ff0902365afe`, đổi `ADR-0055` nghĩa lease thành `ADR-0056`, rồi so với diff protocol hiện tại: bằng nhau. Dòng §20 ADR-0052 và ADR-0055 bằng byte so base. ADR-0056 ngay sau ADR-0055, phần A tăng dần, không số trùng. ADR-0055 của #919 giữ nguyên.
3. **Port r2:** r2 thực đo +58 −3, ADR 47 dòng; r3 +61 −3, ADR 50 dòng. Ngoài đổi số, diff ADR đúng ba khối: Trạng thái/provenance r3; câu đo lại tại base mới; mô tả write set. Không có nội dung port thêm khác. Khối write set có bất nhất đã nêu tại WP835-R3-01.
4. **Provenance controller:** quét bytes tại base bằng regex `heartbeat_required_minutes|30 phút|minutes\s*=\s*30` trên 852 tệp tracked `.py/.sh/.yml/.yaml/.ps1` ngoài `ops/leases/`: bốn match, gồm hai assertion rasoat, một fixture tuổi NLM, một comment thời lượng Ubuntu; không match nào là controller thu hồi lease. Đọc thêm consumer lease trong `ops/lease_publish.py` và `packet_loop.py`; không phát hiện ngưỡng thu hồi 30 phút. Mã thực thi không đổi base/head. Đây là quét mã tĩnh có phạm vi, không chứng minh controller ngoài hoặc mọi cách biểu diễn số tương đương. `git cat-file -e <base>:.github/coordination/change-impact.v1.json` rc 128 ở cả base r2/r3, xác nhận policy vắng mặt.
5. **30 phút còn lại:** `docs/PROTOCOL_DA_PHIEN.md:1307` là bảng nhận định phương án thiết kế đầu vào “assignee + label + TTL 30 phút”; không phải luật ngưỡng hiện hành nên không cần sửa. Tham chiếu 30 phút ở §4/§20 là lịch sử ngưỡng bị thay. Không phát hiện câu vận hành khác bị bỏ sót trong protocol.
6. **N7 / ADR-0017:** ADR-0056 giữ nguyên `CHƯA KÍCH HOẠT VẬN HÀNH` (:6), ngưỡng mới chỉ cấp sau xác minh controller (:26–38); §20 cũng ghi chưa kích hoạt. ADR-0017 không đổi blob; ADR mới chỉ supersede câu ngưỡng, các phần còn lại được giữ. Không thấy tuyên bố 360 phút đã hoạt động hay mâu thuẫn mới về expiry/review SLA.

## Phần chưa chạy hoặc chưa đo được

- **N6 not_run/not_measured:** không gọi mạng GitHub theo assignment; không kiểm check-run PR, remote fence hiện thời, authority readback hay trạng thái lease live. N6 phải được đo sau bước push được cấp, trước khi báo đủ điều kiện merge; không được coi là xanh từ verdict này.
- **not_run:** Windows/full parity, full suite trên các biến thể thêm docs/đổi ratchet, bare Ruff lint. Không có check nào bị skipped rồi tính thành pass.
- **not_measured:** controller ngoài/activation vận hành; exact model và effort phục vụ executor/reviewer bằng runtime header. Không có handoff `ops/handoff/wp835-g3-claude.md` ở snapshot ref r3 được cấp (`git show` rc 128), nên không nhận lời khai test của executor làm bằng chứng thay phép chạy này.
- **Lịch sử:** spec r2 kể review g1 chưa approve vì master drift; r3 ghi patch r2 chưa từng approve. Không có verdict/receipt g1 trong các ref wp835 được cấp để đối chiếu từng finding trước; không coi bản r2 là approved và không tự reset ngân sách bằng revision này.

## Identity và tính chỉ đọc

Reviewer: `provider=openai_codex`, `model_family=openai`, `execution_surface=codex_cli`, `transport=machine`; role reviewer; context độc lập với executor Claude. Run `958a0a8a12954c9f9fbfc8175b5c4c95`, đối chiếu `runs/958a0a8a/run.json`; `codex --version` rc 0 cho `codex-cli 0.164.0` (có cảnh báo không tạo được PATH aliases vì read-only filesystem). Header `stderr.log` rỗng tại lúc kiểm: không suy exact model/effort từ tên CLI hay submitter. Executor theo lease là claude/claude-opus-5-5, claude_code, machine/local, cloud; đây là khai báo lease, chưa có receipt runtime độc lập. Không cấp `cross_approved` hoặc merge authority trong verdict changes_requested này. GitHub submitter: null, chưa đăng.

Sandbox thực tế `workspace-write`, approval policy never; chỉ đọc checkout là kỷ luật phiên, không khai toàn worktree bị cưỡng chế read-only. Scratch/phản chứng ở ngoài repository được review. Không sửa/commit/push branch executor, không gọi mạng GitHub, không merge/land/deploy/LIVE.

Snapshot đầu/cuối kiểm HEAD/tree, diff/index và SHA-256 nội dung 5,707 tệp tracked/untracked/ignored: **bằng nhau**; snapshot SHA-256 `cc92f9ea0d9e14c0a77948514ee722faccd9a252115299dea1567bc507b837ee`. Tracked/untracked sạch; ignored `.codex/` có sẵn và không đổi. Hai clone test cũng `git diff --exit-code` rc 0; fixtures ignored do suite sinh chỉ nằm trong scratch. Snapshot chứng minh không có delta quan sát được ở hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Chỉ ghi artifact cuối `VERDICT.md` vào thư mục output đã giao.
