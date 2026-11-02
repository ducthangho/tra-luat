VERDICT: approve
Reviewed commit: 3e46a4b790b770e513ab05b0b3faf0dc88796903

Reviewed tree: 11f0c80b6ca510bcf6d0d6fce6c2afdd531842f2
Product-diff base: 5775864b04a18c5afe1aafcbb23e54525ce8a3d8
Immutable acceptance baseline: d2e3052d479d140b7e7b91df41ec4914fab7d544
Packet: wp835, revision 4, generation 4; sensitive; lượt review 3 theo prompt.snapshot.
Review axes: spec, standards_security. Ngưỡng approval: không còn P0/P1/P2.

Không phát hiện finding P0/P1/P2/P3 mới sau review toàn bộ diff sản phẩm và kiểm theo lớp trên exact head này. Approval là kết luận review nội dung; N4 vẫn failed trong sandbox, N6 chưa đo. Không dùng verdict này để khai mọi gate đã đạt, đã landed hoặc đã kích hoạt lease 360 phút.

## Spec, authority và phạm vi

Đọc bytes bằng `git show <ref>:<path>`, tự băm bằng SHA-256; tất cả khớp prompt/lease, rc 0:

| Spec trên ref được giao | Commit ref đã đọc | SHA-256 |
|---|---|---|
| `origin/ops/wp835-r4-g4-lease:ops/specs/wp835-lease-6h-governance-r4.md` | `a0d703c81595e654988ad61587d9ff1746513259` | `72bd63610f45a6295e18add2238a0e24d73bedefe8d4d9264608a4ccbef4e05e` |
| `origin/ops/wp835-r3-g3-lease:ops/specs/wp835-lease-6h-governance-r3.md` | `d3c6a5e9ab34e809550607945ad6a08bd9e594ae` | `71403df80d133e4568cb891ae5ab41de937a9d1d1086a92f7255323568596ddc` |
| `origin/ops/wp835-r2-g2-lease:ops/specs/wp835-lease-6h-governance-r2.md` | `b294226de35761b99e8c88922e632fd71d01d48e` | `da98e225c1e0bb419b83c368d2b3112309bd95316a4787c18f91f79bdbc57833` |

Đối chiếu thêm r4 tại OID ghim trong lease `898ea7aa5b61073e9efc06ea539989d46c582429`: cùng blob `bfb52683884c318d66261b53bb56d73f3159c181`, cùng hash. r3 tại `df88ca47bed9f9b0423969737d4468be3b9a0726` và r2 tại `53cf373` cũng cùng hash tương ứng. Product tree không có local copy ba spec; không chép spec vào checkout.

Lease g4 khớp revision/generation/base/spec hash, sensitive, reviewer Codex CLI / họ openai / machine. Tự tính effective-write-set hash theo JSON gọn UTF-8 của danh sách NFC, casefold, sắp xếp: `ae300eec65dc080b26e03ba374282011ac946ca40dc88bf141dd63bfa1db1f46`, khớp lease. Handoff chỉ thuộc nhánh lease; write set sản phẩm là protocol và ADR-0056. Lease g3/g4 có bia mộ hai chiều. Lease Executor g4 đã rút hạn tới `2026-10-25T17:35:00Z`; lượt này chỉ review theo assignment hậu merge, không dùng lease ấy làm quyền thi công. Prompt giao lượt 3 dẫn quyết định nâng trần tại #835 comment `6406009892`; không tự reset budget hoặc gọi thêm reviewer. Không GET/readback GitHub theo lệnh cấm mạng.

`git diff --stat 5775864 3e46a4b` rc 0: đúng hai tệp, **+62 −3** (protocol +11 −3, ADR +51), dưới trần r4 hai tệp/150 dòng thêm.

## Bằng chứng độc lập

Python thực chạy là `/usr/bin/python`, có `-B` và `PYTHONDONTWRITEBYTECODE=1`. Full selftest chạy tuần tự trong hai clone scratch base/head dựng cùng một script, cùng cách clone local không hardlink, checkout exact OID và ghim `core.abbrev=7`. Doc-claims dùng một cặp clone sạch riêng để tránh fixture của selftest ảnh hưởng phép đo.

| Tiêu chí / command thực chạy | rc thật | Kết quả |
|---|---:|---|
| N1: script so bytes/đoạn văn base/head và bất biến lease | 0 | **passed trong phạm vi tài liệu**, chi tiết dưới đây |
| N2: `python -B .claude/dev/packet_loop.py adr-song --root .` | 0 | **passed**: 55 ADR trên đĩa, 55 dòng §20, khớp 1–1; ngoại lệ ADR-0016 có sẵn |
| N3: `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | **passed**: quét 10 tệp, 0 chỗ chép doctrine |
| N3: `git diff --check 5775864b04a18c5afe1aafcbb23e54525ce8a3d8 3e46a4b790b770e513ab05b0b3faf0dc88796903` | 0 | **passed**: output rỗng |
| N4: `python -B scripts/tl.py --selftest`, head | 1 | **failed**: `1729/1731`; 221.914 s; `[OK] r291_docs_ngoai_goi` |
| Cùng command trên base `5775864…` | 1 | **failed**: `1729/1731`; 214.329 s; cùng hai FAIL, **delta = 0** |
| N5: `python -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`, head | 0 | **passed**: `ok=true`, expected=checked=192, package hash match=true; failed/extra/missing/required_missing rỗng |
| N5: `python -B scripts/tl.py doc-claims-check --strict --json`, base/head | 2 / 2 | Hai lần chạy **failed**; tiêu chí **delta=0 passed**: cùng 1 hard flag và 396 advisory, cả hai danh sách bằng nhau; files_scanned 114→115 |
| r4 E1: so nguyên byte với `d2e3052…` | 0 | **passed**: harness và manifest không đổi; cả 192 đường trong manifest cũng giữ nguyên byte |
| N7: đọc ADR :6, :26–38 và dòng ADR-0056 §20 | 0 | **passed trong phạm vi tài liệu**: giữ `CHƯA KÍCH HOẠT VẬN HÀNH` |

Hai FAIL full selftest ở cả base/head:

```text
[FAIL] r226_nguong_l2_troi_theo_abbrev_va_ci_ghim
[FAIL] r268_l2_trichotomy_theo_trang_thai_object
[OK] r291_docs_ngoai_goi
== tl selftest 1729/1731 ==
```

Đã chạy lại đúng hai FunctionDef gốc bằng AST trên hai cây, với observer `subprocess.run` chỉ ghi nhận, không sửa kết quả trả về. Cả hai hàm trả False. Các lệnh fixture `git -c user.email=t@t -c user.name=t commit -q -m c1/c2` đều rc 128: signer gọi MCP localhost bị `socket: operation not permitted`, kết thúc bằng `fatal: failed to write commit object`. Không tắt ký commit hoặc nới sandbox. Đây là lỗi môi trường đo được; **N4 N/N chưa được chứng minh**, dù delta lỗi bằng 0.

Hard flag doc-claims chung là `docs/AUDIT_LAUNCHER_VONG_3.md:462`, claim `f08e45b`, `SHA_NOT_A_COMMIT`. Kho được cấp là shallow; không suy đây là hồi quy. Một phép đo đầu dùng clone head đang chạy selftest bị ảnh hưởng bởi thư mục fixture và giảm hai advisory; đã loại kết quả ấy, dựng lại cả hai clone sạch và đối chiếu được hai danh sách bằng nhau.

Log full selftest đã đối chiếu size/SHA-256 với result JSON của chính lượt này:

- Head: 78.396 bytes; `932fd5db63277c73e32474f3b3af99f35ec5d5779f10dda87b4aed8551630e80`.
- Base: 78.396 bytes; `29659461654b85c12335c03dfbd839dcbb986c96671387e64bd0bc62560e8371`.

## Kiểm nội dung theo lớp

1. **N1 / ngưỡng và bất biến:** `docs/PROTOCOL_DA_PHIEN.md:268`, :279–295 và ADR :9–29 giới hạn 360 phút cho lease mới sau activation; lease cũ giữ byte/giá trị đã đóng dấu, muốn đổi phải có lease kế nhiệm được cấp quyền riêng. Đoạn `review_sla` bằng byte sau khi chỉ thay đúng phần ngưỡng; +2 giờ, fail-closed khi thiếu/không parse/mơ hồ, hết SLA trở về đồng hồ thường đều giữ. Từ câu heartbeat 15 phút sau `changes_requested` tới trước đoạn retention cũng nguyên byte. Đoạn worker stale/cấm cherry-pick nguyên byte. Hạn tuyệt đối, generation, bia mộ và exact head được bảo toàn; không lease YAML nào đổi.

2. **Đổi số / §20:** lấy dòng thêm/xóa của `git diff 062292b2c75be8c316a0cf7347290574efa10861 a62ba1f38abe1f4d4f33181d0898ff0902365afe -- docs/PROTOCOL_DA_PHIEN.md`, đổi tên ADR lease 0055→0056 rồi so diff hiện tại: bằng nhau. Hai dòng §20 ADR-0052/ADR-0055 và tệp ADR-0055 của #919 giữ nguyên byte. ADR-0056 ngay sau ADR-0055, phần A tăng dần, toàn bảng khớp 1:1 tệp ADR. Không lẫn với ADR-0055 của #919 hoặc nợ máy #816.

3. **Provenance ADR:** :3–7 ghi lịch sử port r3/g3, :42–44 bổ sung quyết định r4, không khai mọi gate đã chạy hoặc controller đã được xác minh. So ADR r2 sau đổi số: chỉ ba khối provenance/trạng thái, câu đo lại base mới và write set thay đổi. Đã quét tĩnh bytes ở cả base r2/r3 trên các tệp `.py/.sh/.ps1/.yml/.yaml` ngoài `ops/leases/` và `ops/land/` (729/751 tệp), tìm `heartbeat_required_minutes`, 30 phút/minutes, 1800, 30×60; đọc các hit và consumer lease. Quét thêm 12 tệp JS/GAS/CMD tại base r3 không có hit lease/ngưỡng. Không tìm thấy controller thu hồi 30 phút trong phạm vi đo. Đây là phép quét tĩnh có giới hạn, không chứng minh mọi cách mã hóa ngưỡng hay controller ngoài; chính ADR :33–38 cũng khai chưa đo controller ngoài. Policy change-impact vắng tại hai base và candidate: `git cat-file -e <sha>:.github/coordination/change-impact.v1.json` rc 128 với lỗi đích danh path không tồn tại.

4. **Câu 30 phút còn lại / ADR-0017:** quét toàn protocol. :280 và :1494 là lịch sử ngưỡng bị thay; :1307 là nhận định phương án đầu vào “assignee + label + TTL 30 phút”, không phải luật thu hồi hiện hành. Không thấy câu vận hành bị bỏ sót. ADR-0017 giữ nguyên byte; ADR-0056 supersede đúng câu ngưỡng và giữ các phần còn lại. Trạng thái Accepted không bị dùng làm activation.

5. **Merge và phạm vi:** `git show -s --format=%P 3e46a4b…` rc 0 cho hai cha `87fd7611001ebffd20a87c934fcf578644984b4b` và `5775864b04a18c5afe1aafcbb23e54525ce8a3d8`. Bytes toàn diff `git diff --binary d2e3052… 87fd761…` bằng `git diff --binary 5775864… 3e46a4b…`, SHA-256 `6b194d21bff6b94d8a59b955b060d7f962633f509b86eee7ffc9d23ff27ffa44`. Base drift chỉ 37 tệp `ops/land/**`; merge không thêm thay đổi sản phẩm. Hai blob E1 không đổi so baseline: harness `a1c861d8b148a4cbb713ed380553d892c8c25cca`, manifest `3dddd00f6b45dd27c5f307e9f289be8599f6af6a`. Đã so bytes cả 192 tệp trong manifest, không chỉ số đếm.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 2 trên `87fd7611001ebffd20a87c934fcf578644984b4b` không có finding mở. Đã đọc verdict từ ref g4 được giao, SHA-256 `1f38d44ca0dfe7dbb28bece08562f1d495c3ab464e4d5af92090674106567973`; không dùng approval ấy thay review head mới.

| Lớp / finding lịch sử | Nguồn | Đối chiếu độc lập trên candidate | Trạng thái |
|---|---|---|---|
| `dac-ta-ratchet-docs-da-loi-thoi` / WP835-R3-01, P2 | Lượt 1, `3785f9535398db04fb36a5eaa095166a8e048f1e`; đã đóng ở lượt 2 | r4 E1/E2 thay D3/N4 lỗi thời; ADR :42–44 đúng diff. Consumer r291 trích bằng AST từ harness thật: base 79 docs → True; head 80 → True; fixture thêm Markdown thành 81 → True; đổi duy nhất ratchet gói 192→193 → False. | **ĐÃ VÁ THẬT**, tiếp tục đóng |

Một lớp lịch sử, một finding, hai biểu hiện (hợp đồng N4 và provenance ADR), không lớp mới/tái mở. U của lượt liền trước rỗng, tỷ lệ F/U là **N/A**. Probe consumer chứng minh ratchet docs đã bỏ và ratchet gói vẫn có; không thay bằng chứng full N/N.

## Phần chưa chạy, identity và tính read-only

- **not_run / not_measured:** N6 check-run `ci.yml`, remote PR head/fence, readback comment nâng trần/authority GitHub, hậu-merge gate, trạng thái bookkeeping và controller ngoài. Không gọi mạng GitHub theo assignment; không nhận CI/land/activation là passed.
- **not_run:** Windows/parity, bare Ruff lint. Ruff pin/probe contract qua `runpy.run_path('.claude/dev/ci_dang_ky_test.py')['loi_ruff_ci']()` rc 0, `RUFF_CONTRACT 3 []`. `python -B -m ruff --version` rc 1, `No module named ruff`; không cài dependency hoặc biến contract thành lint pass. Không có check skipped được tính thành pass.
- Reviewer: `provider=openai_codex`, `model_family=openai`, `execution_surface=codex_cli`, `transport=machine`, run `7f235b78590a47819fcd14273553e1c0`, context mới độc lập với Executor. `run.json` của lượt này xác nhận provider/surface/transport; `codex --version` rc 0: `codex-cli 0.164.0`. Header hiện chỉ có “Reading additional input from stdin...”; exact model variant/effort phục vụ **not_measured**. Executor theo lease: claude / claude-opus-5-5 / họ claude / claude_code / machine/local / cloud, session `session_016aK6Uy4CzUZFKnDmoHRQps`; đây là khai báo lease, chưa kiểm receipt runtime độc lập. Assurance target là `cross_approved`; verdict không tự ghi state assurance hoặc thay receipt identity/vận chuyển. GitHub submitter: null. Caller cần hoàn tất terminal receipt sau khi run kết thúc.
- Runtime: Linux x86_64, Python 3.13.17, Git 2.43.0; checkout detached, origin `https://github.com/ducthangho/tra-luat.git`, `core.abbrev=7`. Sandbox thực tế `workspace-write`, approval policy `never`; read-only checkout là kỷ luật phiên, không khai toàn cây bị sandbox cưỡng chế read-only.
- Snapshot đầu/cuối bằng nhau: 5.744 path tracked/untracked/ignored, hash nội dung 5.737, chỉ metadata 7 path theo bộ lọc tên nhạy cảm. HEAD/tree, diff/index-diff và trạng thái đều không đổi; ignored `.codex/` có sẵn. Snapshot SHA-256 `2f5fcf126396e40620337bb28980e9ee29a952ee3ae6ca5013298239b082f979`. Các clone test không đổi tracked bytes. Snapshot chỉ chứng minh không có delta quan sát ở hai mốc, không chứng minh toàn lịch sử hoặc nội dung các path chỉ đo metadata.
- Scratch phép đo: `/tmp/wp835-review3-7f235b78-jyo7eoxz`. Không sửa/commit/push repository được review; fixture Git chỉ nằm ngoài repository. Chỉ ghi kết quả `VERDICT.md` vào output được giao.
