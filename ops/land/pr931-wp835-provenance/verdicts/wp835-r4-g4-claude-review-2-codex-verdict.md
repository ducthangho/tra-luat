VERDICT: approve
Reviewed commit: 87fd7611001ebffd20a87c934fcf578644984b4b

Reviewed tree: c19aed8e16e2bf4560c422f4c8f8974368303b46
Acceptance base: d2e3052d479d140b7e7b91df41ec4914fab7d544
Base tree: bf2449d9ab695a6ddfdd75575d75186e9ac981b3
Packet: wp835, revision 4, generation 4; sensitive; lượt Codex 2/2 tính chung g3+g4.
Review axes: spec, standards_security. Ngưỡng nội dung: không còn P0/P1/P2.

Không phát hiện P0/P1/P2/P3 mới trong phạm vi E4 và diff đã giao. WP835-R3-01 được đóng. Approval này là kết luận review nội dung trên exact SHA; KHÔNG xác nhận mọi gate của Packet đã đạt hoặc cấp quyền push/merge/land/deploy. N4 tại sandbox vẫn failed do fixture Git, N6 chưa chạy; không đổi hai trạng thái này thành passed.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: verdict lượt 1 trên `3785f9535398db04fb36a5eaa095166a8e048f1e`, tree `fd0c97ff1ae2f5e595502ada69dc2d449fdebbcd`. Ref g3 trong checkout được giao chưa có verdict; `git show origin/ops/wp835-r3-g3-lease:ops/reviews/wp835-r3-g3-claude-review-1-codex-verdict.md` trả rc 128. Đã đọc cùng đường dẫn từ bản kho cục bộ `../lz`, ref g3 tại `d3c6a5e9ab34e809550607945ad6a08bd9e594ae`, không fetch mạng. Verdict nguồn SHA-256: `8f56beff1830cf42c133b3517ef865c417881e4a9a440ad401e02d5b493dc5d6`.

| Finding / lớp nguồn | Severity cũ | Đối chiếu trên head mới | Trạng thái |
|---|---|---|---|
| WP835-R3-01 / `dac-ta-ratchet-docs-da-loi-thoi` | P2 | Cả hai biểu hiện đã xử lý: r4 E1/E2 bỏ D3.3/D3.4 và phản chứng ratchet docs bất khả dụng; ADR :40–44 mô tả đúng diff hai tệp và nguyên nhân không sửa companion. Probe consumer độc lập xác nhận docs được đếm từ cây, còn ratchet gói vẫn hoạt động. | **ĐÃ VÁ THẬT — đóng** |

Một lớp, một finding, hai biểu hiện; không có lớp mới hoặc tái mở. U=1, F=1, tỷ lệ đóng lớp 1/1. Đây là đóng lớp bất nhất hợp đồng/provenance, không phải bằng chứng N4 đã đạt N/N.

Hai tệp companion vốn đã không đổi ở head lượt 1; commit `87fd761` không phải thao tác hoàn nguyên chúng. Thay đổi của lượt này là revision hợp đồng và sửa provenance ADR. Đã kiểm cả ba mốc base / head lượt 1 / head mới bằng `git rev-parse <oid>:<path>` và so bytes:

| Tệp | Blob ở cả ba mốc | SHA-256 bytes |
|---|---|---|
| `scripts/tl_selftest.py` | `a1c861d8b148a4cbb713ed380553d892c8c25cca` | `fc5717653cc19715d487c720c5d2ab2a4bc7e0400c4c2a8b0d10f304a57c0cfc` |
| `RELEASE_MANIFEST.json` | `3dddd00f6b45dd27c5f307e9f289be8599f6af6a` | `3f0b2f25921eba6fde2e8e40244c06de762f012bed0cb0e3163bf65f93ab4859` |

## Spec, lease và phạm vi

Tự SHA-256 bytes từ `git show <ref>:ops/specs/wp835-lease-6h-governance-rN.md`, rc 0; cả ba khớp hash assignment/lease:

| Spec | OID ref cục bộ đã đọc | SHA-256 |
|---|---|---|
| r4, `origin/ops/wp835-r4-g4-lease` | `e2ff789ee6be551492ded7b179951d477506b0a4` | `72bd63610f45a6295e18add2238a0e24d73bedefe8d4d9264608a4ccbef4e05e` |
| r3, `origin/ops/wp835-r3-g3-lease` | `74072a3d7958986a04bce647554251ab5f870e9d` | `71403df80d133e4568cb891ae5ab41de937a9d1d1086a92f7255323568596ddc` |
| r2, `origin/ops/wp835-r2-g2-lease` | `b294226de35761b99e8c88922e632fd71d01d48e` | `da98e225c1e0bb419b83c368d2b3112309bd95316a4787c18f91f79bdbc57833` |

r4 còn được đối chiếu tại OID ghim trong lease `898ea7aa5b61073e9efc06ea539989d46c582429`: cùng blob `bfb52683884c318d66261b53bb56d73f3159c181`. Không có local copy ba spec ở product tree; không chép vào checkout.

Lease g4 khớp revision/generation/base/hash, class sensitive, reviewer Codex CLI / họ openai / machine. Tự tính write-set hash theo JSON gọn của danh sách NFC, casefold, sắp xếp: `ae300eec65dc080b26e03ba374282011ac946ca40dc88bf141dd63bfa1db1f46`, khớp lease. Handoff chỉ thuộc nhánh lease; hai đường sản phẩm là protocol và ADR-0056. Lease g4 khai `thay_the_cho: wp835-r3-g3-claude`; lease g3 ở ref nguồn `../lz` nói trên có `da_bi_thay_the: wp835-r4-g4-claude`.

`git diff --numstat <base> <head>` rc 0: protocol +11 −3; ADR mới +51 −0; tổng **2 tệp, +62 −3**, trong trần E1 hai tệp/150 dòng thêm. `git diff 3785f95 87fd761` rc 0: chỉ ADR :40–44, +4 −3. Không lease YAML, runtime hay manifest nào đổi.

Câu “Revision 4 (chủ kho duyệt 25-10-2026)” tại `docs/adr/0056-lease-no-progress-six-hours.md:42` khớp authority record trong lease g4: `granted_by: ducthangho`, quyết định “Soạn r4, bỏ 2 tệp thừa”, Issue #835 comment `6399670937`, ngày 25-10-2026. Đây là đối chiếu record được cấp; chưa GET/readback bytes comment GitHub. Lease cũng khai giới hạn băm comment không đo được. Không suy thành xác minh remote mới.

Origin đúng `https://github.com/ducthangho/tra-luat.git`; checkout detached đúng head/tree ở trên, `core.abbrev=7`. Local `origin/master` chỉ khác acceptance base ở `ops/land/**`; đây là cache offline, không chứng minh remote fence hiện thời. Hạn tuyệt đối lease g4: `2026-10-27T15:46:00Z`; không xác minh heartbeat/state live qua GitHub.

## Phép đo độc lập N1–N7

Hai clone scratch base/head được dựng trong cùng một script, cùng quy trình clone local không hardlink, checkout exact OID, ghim abbrev=7. Cache/output ngoài checkout review, dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`. Full selftest chạy tuần tự, một heavy gate tại một thời điểm. Command Python dưới đây dùng `/usr/bin/python`; cwd là clone tương ứng.

| Tiêu chí / command | rc thật | Kết quả và trạng thái |
|---|---:|---|
| N1: so văn bản base/head và probe bất biến bên dưới | 0 | **passed trong phạm vi văn bản**: lease mới sau activation dùng 360; expiry/fencing/bia mộ/exact head, SLA và heartbeat 15 phút giữ nguyên |
| N2: `python -B .claude/dev/packet_loop.py adr-song --root .` | 0 | **passed**: 55 ADR trên đĩa, 55 dòng §20, khớp 1–1; ngoại lệ ADR-0016 có sẵn |
| N3: `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | **passed**: quét 10 tệp, 0 chỗ chép doctrine |
| N3: `git diff --check d2e3052d479d140b7e7b91df41ec4914fab7d544 87fd7611001ebffd20a87c934fcf578644984b4b` | 0 | **passed**: output rỗng |
| N4: `python -B scripts/tl.py --selftest`, head | 1 | **failed**: `== tl selftest 1729/1731 ==`, 236.68 s; `[OK] r291_docs_ngoai_goi` |
| Đối chứng cùng command, base | 1 | **failed**: `== tl selftest 1729/1731 ==`, 236.81 s; r291 OK; cùng hai FAIL, delta = 0 |
| N5: `python -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed**: `ok=true`, `expected_file_count=checked_file_count=192`; failed/extra/missing/required_missing rỗng; package hash match true; manifest không sửa |
| N5: `python -B scripts/tl.py doc-claims-check --strict --json`, base/head | 2 / 2 | Hai command **failed**; riêng tiêu chí **delta=0 passed**: cùng 1 hard flag và 396 advisory, hai danh sách bằng nhau; files_scanned 114→115 |
| N6: check-run `ci.yml` trên PR exact head | — | **not_run / not_measured**: offline, không gọi mạng GitHub; phải đo sau push được cấp và trước khi báo đủ điều kiện merge |
| N7: đọc ADR :6, :26–38 và dòng ADR-0056 §20 | 0 | **passed trong phạm vi tài liệu**: giữ “CHƯA KÍCH HOẠT VẬN HÀNH”; chỉ áp lease mới sau xác minh controller |

Hai FAIL full selftest ở CẢ base/head:

```text
[FAIL] r226_nguong_l2_troi_theo_abbrev_va_ci_ghim
[FAIL] r268_l2_trichotomy_theo_trang_thai_object
[OK] r291_docs_ngoai_goi
== tl selftest 1729/1731 ==
```

Tái chạy đúng hai FunctionDef gốc qua AST với `_TL_MODULE=tl`, observer `subprocess.run` chỉ ghi kết quả, không sửa return value: cả hai trả False. Các lệnh fixture `git -c user.email=t@t -c user.name=t commit -q -m c1/c2` đều rc 128, stderr có `socket: operation not permitted` khi signer gọi MCP localhost, tiếp theo `fatal: failed to write commit object`; fixture không có HEAD. Đây là lỗi môi trường đo lại, cùng hình dạng lượt 1; không tắt ký commit hoặc nới sandbox để ép xanh. **N4 N/N chưa được chứng minh ở đây**, dù delta lỗi bằng 0. Cần evidence N/N trên exact head ở runtime phù hợp; không nhận lời hứa trong prompt làm pass. Handoff g4 chưa có trong snapshot ref r4 được cấp, nên không có evidence executor thay thế đã validate trong lượt này.

Hard flag doc-claims chung: `docs/AUDIT_LAUNCHER_VONG_3.md:462`, claim `f08e45b`, `SHA_NOT_A_COMMIT`; clone được cấp là shallow. Không quy thành hồi quy của bản vá.

Đối chiếu SHA-256 và size log với JSON kết quả, rc 0:

- Head selftest: 78,396 bytes; `b76154b4bfb0f9a3806a7d5c991d9504a79e16fd6b71f45440b0a6835a8771ab`.
- Base selftest: 78,396 bytes; `f62d2bb12fb65abe485bf5cfe67d458f5b1a67cb78c4fb5d8b892519ed825ec6`.

Dùng marker tổng cuối; không cộng số dòng OK của các suite con.

## Kiểm theo lớp và phạm vi lời khai mới

1. **N1:** nguyên đoạn `review_sla` bằng nhau sau khi chỉ chuẩn hóa phần đổi ngưỡng 30→360. Đoạn stale worker/cấm cherry-pick bằng nhau; ADR-0017 giữ nguyên bytes. Review SLA +2 giờ, thiếu/không parse/mơ hồ thì fail-closed, hết SLA trở lại đồng hồ thường, heartbeat 15 phút sau changes_requested đều giữ. Không thử controller vận hành.
2. **Port r2 / đổi số / §20:** trích dòng thêm/xóa của diff protocol `062292b2c75be8c316a0cf7347290574efa10861..a62ba1f38abe1f4d4f33181d0898ff0902365afe`, đổi tên ADR lease 0055→0056 rồi so diff hiện tại: bằng nhau. Hai dòng §20 ADR-0052 và ADR-0055 của #919 bằng byte so base; ADR-0056 ngay sau ADR-0055. Commit cuối không sửa protocol. Không lẫn ADR-0055 của #919 với ADR lease hay nợ máy #816.
3. **Đoạn ADR vừa sửa:** so bytes toàn bộ 192 đường trong manifest base/head: không đường nào đổi. “Không tệp nào trong gói đổi” đúng trong phạm vi manifest; không suy thành đã phát hành hay LIVE không đổi. Policy `.github/coordination/change-impact.v1.json` vắng ở cả hai acceptance base và head (`git cat-file -e` rc 128, lỗi đích danh path không tồn tại).
4. **Consumer r291:** lấy duy nhất `_c291_docs_ngoai_goi` bằng AST từ harness thật, chạy với `tl_core.release` thật, `_ROOT209` trỏ từng cây/fixture ngoài checkout. Probe rc 0: base 79 docs → True; head 80 docs → True; fixture thêm một Markdown 81 docs → True. Đột biến duy nhất `len(paths) == 192` thành `len(paths) == 193` → False. Đây là probe consumer, không phải full suite từng biến thể. Nó xác nhận ratchet số docs đã bỏ còn ratchet GÓI vẫn có; câu “không còn ratchet nào để kê khai” ADR :44 được đọc trong ngữ cảnh docs ở :43–44, không thành lời khai mọi ratchet của kho đã biến mất.

## Identity, giới hạn và tính read-only

Reviewer: `provider=openai_codex`, `model_family=openai`, `execution_surface=codex_cli`, `transport=machine`; run `6c5f75a9b0ee4b3292bf232418a47eec`; context độc lập với Executor. `run.json` của chính lượt này xác nhận provider/surface/transport; `codex --version` rc 0 là `codex-cli 0.164.0` (cảnh báo không tạo được PATH aliases trên filesystem read-only). Header `stderr.log` rỗng khi đọc; exact model variant/effort phục vụ chưa đo bằng header. Executor theo lease: claude / claude-opus-5-5 / họ claude / claude_code / machine/local / cloud; đây là thông tin lease, chưa kiểm bằng receipt runtime độc lập. Assurance target là cross_approved; verdict không tự ghi state assurance hoặc thay receipt identity/vận chuyển. GitHub submitter: null, chưa đăng. Terminal receipt của chính run cần caller hoàn tất sau khi tiến trình kết thúc.

Môi trường: Linux x86_64, Python `/usr/bin/python` 3.13.17, Git 2.43.0, rg 15.2.0; yaml/requests/cryptography có mặt. Ruff pin/probe contract qua `runpy.run_path('.claude/dev/ci_dang_ky_test.py')['loi_ruff_ci']()` rc 0, `RUFF_CONTRACT 3 []`. `python -B -m ruff --version` rc 1, `No module named ruff`; bare lint **not_run**. Contract xanh không phải lint xanh; không cài công cụ hoặc đổi bootstrap để che giới hạn. Tool managed-environment status không có trong danh sách callable; không có hoạt động Docker hay mạng cần nó.

**not_run:** Windows/full parity, bare Ruff lint, full suite trên hai biến thể consumer, N6 GitHub CI. **not_measured:** controller ngoài/activation, remote fence/authority readback/live lease, exact model/effort runtime và terminal receipt. Không có check skipped nào được tính passed. N4 failed và N6 thiếu evidence vẫn phải được xử lý ở gate phù hợp trước khi Packet được báo đủ điều kiện; approval nội dung không miễn các nghĩa vụ đó.

Sandbox thực tế `workspace-write`, approval policy `never`; read-only checkout là kỷ luật phiên, không khai toàn cây bị sandbox cưỡng chế read-only. Không sửa repository review, không commit/push branch Executor, không gọi mạng GitHub, không merge/land/deploy/LIVE. Chỉ fixture Git sẵn có của selftest/targeted probe có gọi commit trong thư mục tạm.

Snapshot trước/sau bằng nhau ở `rv2`: 5,707 path tracked/untracked/ignored, trong đó hash nội dung 5,702 và chỉ so metadata của 5 path thuộc mẫu nhạy cảm, không đọc nội dung chúng. HEAD/tree, diff và index-diff bằng nhau; tracked/untracked sạch, ignored `.codex/` có sẵn. Snapshot SHA-256 `311af942a05769feb55f32e085dc7664ff882a6de4673507ce98b41e07513a21`. Kho nguồn `lz` đã đọc cũng không có delta: 5,713 path (hash nội dung 5,708, metadata 5), snapshot `1d8d88b59a0189b72f49c40c1a13ddaa3e79d763cd2694255bc37f11ebd88e58`. Hai clone test `git diff --exit-code` rc 0; fixture/cache chỉ ở scratch ngoài checkout. Snapshot chứng minh không có delta quan sát ở hai mốc, không chứng minh toàn lịch sử chưa từng ghi rồi hoàn nguyên hoặc nội dung năm path chỉ đo metadata.

Scratch phép đo: `/tmp/wp835-review2-6c5f75a9-yvig5lx5`. Chỉ ghi tệp kết quả `VERDICT.md` vào output được giao; không tạo thêm review call sau lượt 2/2.
