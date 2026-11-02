Verdict: approve
Reviewed commit: 294f0eb7eaae7b142bd6a3e89a18f512c4b819d0
Spec sha256: c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2; Chung sha256: 4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0

**Kết luận lượt 8/8:** không có finding mới do merge; 0 P0/P1/P2, giữ nguyên 1 lớp P3 từ lượt 7. Ba tệp write set giống từng byte với head đã được approve. Phần master mang vào chỉ sửa hai hồ sơ `ops/land/`, không đổi phụ thuộc của mã/test đang xét. Ngưỡng approve áp dụng đúng prompt: không còn P0/P1/P2. Verdict chỉ neo commit dòng 2, **không cấp quyền push/merge/land**.

Đã đọc toàn văn `/tmp/claude-0/-home-user-tra-luat/cfb946be-069e-511e-96e0-556502ab8797/scratchpad/runs/f5ff20ab/prompt.snapshot`. Gốc làm việc là thư mục chứa `src/`, `out/`, `tham-chieu/` tại `scratchpad/rv8`, không phải thư mục chứa snapshot. Review độc lập, offline, giới hạn vào xác minh merge; không review lại thiết kế đã duyệt ở lượt 7.

Reviewer: Codex/OpenAI, họ `openai`; executor theo lease bản chép: Claude, họ `claude`; packet #834/revision 1/generation 1, `review_class: sensitive`, `assurance_target: cross_approved`. Thực thi shell qua công cụ trong môi trường Linux, transport `machine`. Exact serving model/effort/session và nhãn launcher `codex_cli` không được đo độc lập trong phiên này; không tự tạo receipt assurance hoặc suy identity từ tài khoản đăng. Ngoại lệ một lần ở comment `issuecomment-6409611375` là chỉ thị do prompt cung cấp, chưa xác minh online.

**1. Hash và định danh Git — tất cả khớp.** `python -B out/measure_review.py` rc=0. Các lệnh đầy đủ, rc, stdout/stderr nằm trong `MEASUREMENTS.json`; kết quả cấu trúc trong `IDENTITY.json`. Bảng lệnh dưới dùng OID rút gọn để dễ đọc; script thực thi bằng OID đủ 40 hex.

| phép đo | rc | output chính |
|---|---:|---|
| `sha256sum src/ops/specs/wp834.md` | 0 | `c57ef4d86592218729b811efede7909803d75b6d18ca0d0c3e5059848b44a9d2` |
| `sha256sum src/ops/specs/may-adr-0054-chung.md` | 0 | `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0` |
| `sha256sum tham-chieu/VERDICT-luot7.md` | 0 | `37f009b88c8f9aca7ae4a09d431f1046f8b7ca09978d2e75e47ce6e57cd68488` |
| `git -C src show 294f0eb:<mỗi đường dẫn đặc tả>` + SHA-256 byte stdout | 0 | hai blob exact head cũng khớp hash ở dòng 3, không chỉ worktree |
| `git -C src rev-parse HEAD` | 0 | `294f0eb7eaae7b142bd6a3e89a18f512c4b819d0` |
| `git -C src rev-parse 'HEAD^{tree}'` | 0 | `a2f15eb8b8001429f187e5c30c907d597123542f` |
| `git -C src rev-parse refs/remotes/origin/master` | 0 | `9372ecd93bd95350c90dfc75d3f0d014b4f932ed` |
| `git -C src show -s --format=%P 294f0eb` | 0 | `8ac10ce47d2587c91637d74d299e3c781025be1e 9372ecd93bd95350c90dfc75d3f0d014b4f932ed` |
| `git -C src merge-base --is-ancestor 8ac10ce 294f0eb` | 0 | stdout rỗng: đúng là tổ tiên |
| `git -C src merge-base --is-ancestor 9372ecd 294f0eb` | 0 | stdout rỗng: đúng là tổ tiên |
| `git -C src merge-base --is-ancestor ab344da5f07cce673d97056b70b002911c4d5082 294f0eb` | 0 | stdout rỗng: base lease là tổ tiên |
| `git -C src merge-base 8ac10ce 9372ecd` | 0 | `356eb262cbd491b9599b56d5f7c41c93dd9a28a1` |
| `git -C src rev-parse --is-shallow-repository` | 0 | `false` |
| `git -C src symbolic-ref -q HEAD` | 1, kỳ vọng | stdout rỗng: detached HEAD |
| `git -C src status --porcelain=v1 --untracked-files=all`; `git diff --exit-code`; `git diff --cached --exit-code` trong src | mỗi lệnh 0 | đều rỗng; `.git` là thư mục thật, không symlink |

**2. Write set và trần diff — đạt.** Lệnh thực thi:

```sh
git -C src diff --exit-code 8ac10ce47d2587c91637d74d299e3c781025be1e 294f0eb7eaae7b142bd6a3e89a18f512c4b819d0 -- .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py docs/PROTOCOL_DA_PHIEN.md
```

rc=0, stdout/stderr rỗng. Ngoài diff, đã gọi `git rev-parse <commit>:<path>` ở cả hai commit, đọc byte bằng `git show` và so trực tiếp byte cũ = byte head = byte worktree.

| tệp | blob OID ở cả `8ac10ce` và `294f0eb` | kết quả |
|---|---|---|
| `.claude/dev/packet_loop.py` | `9b2410e1a97a91068a67a03a977a6148a1c64ee7` | cùng OID, cùng byte |
| `.claude/dev/packet_loop_test.py` | `fda3b94fa7a5a3e05ee9133dddf1f17fdbfa6b70` | cùng OID, cùng byte |
| `docs/PROTOCOL_DA_PHIEN.md` | `5d107a4b88055e99b60dcee3638ee1a120e79ce0` | cùng OID, cùng byte |

`git -C src diff --numstat 9372ecd93bd95350c90dfc75d3f0d014b4f932ed 294f0eb7eaae7b142bd6a3e89a18f512c4b819d0` rc=0:

```text
181  1  .claude/dev/packet_loop.py
262  3  .claude/dev/packet_loop_test.py
4    1  docs/PROTOCOL_DA_PHIEN.md
```

Đúng ba đường dẫn, **447 dòng thêm ≤ 450**, 5 dòng xoá. Diff protocol chỉ nằm trong §4. `git -C src diff --check 9372ecd 294f0eb` rc=0, output rỗng.

**3. Phần master mang vào và phụ thuộc — không có thay đổi liên quan.** `git -C src diff --stat 8ac10ce 294f0eb` rc=0:

```text
ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml | 16 ++++++++++++++++
ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml | 16 ++++++++++++++++
2 files changed, 32 insertions(+)
```

Đã đọc toàn bộ `MASTER_DRIFT.diff`: mỗi tệp chỉ thêm khối ghi điều kiện chủ kho duyệt landed, vẫn ghi `landed: false`. So `git diff --raw --no-abbrev 8ac10ce 294f0eb` với `git diff --raw --no-abbrev 356eb26 9372ecd`: cả hai rc=0, byte output giống nhau; không có sửa merge riêng ngoài delta master.

`git -C src diff --exit-code 356eb26 9372ecd -- ops/lease_publish.py ops/bien_nhan_v2.py .claude/dev/launcher.py AGENTS.md docs/adr docs/PROTOCOL_DA_PHIEN.md` rc=0, rỗng. Đối chiếu OID ở master cũ/mới:

| phụ thuộc | OID ở cả `356eb26` và `9372ecd` | kết quả |
|---|---|---|
| `ops/lease_publish.py` | `ca480114ae7a893bef985f29dbbd962dc156212b` | giống |
| `ops/bien_nhan_v2.py` | `62ce28be6116664c1799058909ab1ea96f70cc66` | giống |
| `.claude/dev/launcher.py` | `9c38fb1c6562c07ffe744ee4365f23cc5941c417` | giống |
| `AGENTS.md` | `5fea56ea9d14c2922d8771e7fc5bd69d728a000e` | giống |
| `docs/adr` | `c008a2d66f174546a53832dc18d73cfda783a230` | giống |
| `docs/PROTOCOL_DA_PHIEN.md` | `76a8a3ea2e9d612310663dcf1e49c3861c7d7144` | giống |

`docs/adr` dùng tree OID, các dòng khác dùng blob OID. Protocol trên master có OID riêng với protocol ứng viên vì thay đổi §4 của packet; phép so đúng là master cũ với master mới.

Đã đọc đường phụ thuộc: `packet_loop.py:2391–2420` chép đúng tuple `CANON`; `_che_do_0054` ở dòng 2558 đọc `docs/adr/`, protocol và lịch sử first-parent. Fixture `_kho812` ở test:7659–7682 đọc validator/launcher/AGENTS/protocol rồi dựng kho bare cục bộ. `bien_nhan_v2.py` đọc luật từ AGENTS/protocol, nguồn launcher và `ops/reviews`; `lease_publish.py` quét `ops/leases`/`ops/thu-hoi`. Các vòng quét doctrine nằm dưới thư mục skill/adapter; không quét `ops/land`. Không có đường đọc/import/gọi hai hồ sơ land vừa đổi trong mã/test và các validator liên quan.

`rg -n 'ops/land|pr870-claude-md-bai-hoc-c-land-evidence|pr889-claude-md-bai-hoc-c-land-evidence'` trên packet_loop, test, hai validator và launcher: rc=1, không match; đây là kiểm hỗ trợ, không dùng riêng grep để kết luận. Diff các vùng `.github`, `.claude`, `.agents`, `.githooks`, `docs`, `ops/leases`, `ops/thu-hoi`, `ops/reviews`, AGENTS/CLAUDE giữa hai master đều rỗng (rc=0). Hai lần `git rev-list --first-parent` rc=0: lịch sử cũ được giữ nguyên làm hậu tố, chỉ thêm `9372ecd`; không đổi chuỗi tổ tiên ADR đã có. `python -B out/inspect_dependencies.py` rc=0; lệnh/output đầy đủ ở `DEPENDENCY_CHECKS.json`.

**4. Đo hành vi trên bản sao exact head.** Dù không có phụ thuộc bị master sửa, đã chạy bổ sung cả hai nhóm ca và mutant khai báo của #834. Mọi thử nghiệm dùng `out/copy` (chép nguyên source, HEAD/tree khớp) và fixture dưới `out/tmp`. Môi trường: `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=OUT/tmp`, `GIT_CONFIG_GLOBAL=/dev/null`, `GIT_CONFIG_SYSTEM=/dev/null`, `GIT_OPTIONAL_LOCKS=0`, `GIT_ALLOW_PROTOCOL=file`; bản sao có `core.abbrev=7`. Git fetch/push/ls-remote của fixture chỉ dùng bare repo cục bộ dưới OUT, không gọi mạng/GitHub.

| lệnh | rc | bằng chứng dương | log |
|---|---:|---|---|
| `python -B tham-chieu/chay_ca_va_dot_bien.py out/copy r834_ r834_` | 0 | 63/63 ca nền PASS; 57 mutant, 62/62 quan hệ GIET; 0 SỐNG, 0 TÍN DỤNG GIẢ | `R834.log`, `R834.stderr` |
| `python -B tham-chieu/chay_ca_va_dot_bien.py out/copy r812_` | 0 | 149/149 ca PASS; không bỏ qua ca nào | `R812.log`, `R812.stderr` |
| `python -B out/copy/.claude/dev/packet_loop.py doctrine-scan --root out/copy` | 0 | 10 tệp, 0 chỗ chép doctrine | `DOCTRINE.log`, `DOCTRINE.stderr` |
| `python -B out/copy/.claude/dev/packet_loop.py adr-song --root out/copy` | 0 | 55 ADR / 55 dòng §20, khớp 1–1; ngoại lệ 0016 khai sẵn | `ADR.log`, `ADR.stderr` |

Tổng ca nền chọn lọc: **212/212 PASS**, không failed/skipped trong tập này. `run_checks.py` kiểm đủ tên ca với inventory, đủ tên mutant, đủ quan hệ ca–mutant và nhãn `GIET`; không coi riêng rc=0 của helper là bằng chứng pass. 57 mutant/62 quan hệ là đúng bộ tiền tố `r834_`; không cộng `r812_bo_generation` hoặc các probe lượt 7 chưa chạy lại. Lý do GIET cụ thể nằm trong `R834.log`; không có mỏ neo thiếu/trùng hay tín dụng do CLI sập. `TEST_INVENTORY.json`, `CHECKS.json`, `R834.json`, `R812.json` lưu số đo. Runner `python -B out/run_checks.py` rc=0. SyntaxWarning có sẵn tại test:3714 không tính thành finding hoặc mutant kill.

**ĐỐI CHIẾU LƯỢT TRƯỚC.** Verdict lượt 7 đã được băm lại và đúng head `8ac10ce47d2587c91637d74d299e3c781025be1e`. Không có bản vá nội dung sau lượt 7; bằng chứng byte/blob ở mục 2 xác nhận nợ cũ còn nguyên. Không dựng finding độ phủ mới trong lượt này.

| slug | hạng | biểu hiện | phép đo | hướng vá |
|---|---|---|---|---|
| `required-mutation-coverage-missing` | P3, **CHƯA VÁ — giữ nguyên lượt 7** | Hai biểu hiện `omit_unanchored_issue_finding` và `allow_noninteger_page_ids`; tên nợ: **bảo vệ neo head của finding issue comment và kiểu ID trang**. | Lượt 8 đo code/test giống từng byte với lượt 7. Theo verdict lượt 7 đã xác minh hash, candidate từ chối đúng còn hai mutant sống 63/63; lượt 8 không chạy lại hai A/B này, không khai chúng đã đóng. | Owner giữ như lượt 7: executor Packet #834 (Claude), chủ kho theo dõi. Thêm hai ca đổi một yếu tố và mutant đúng chốt: issue comment P1 không neo head cạnh kết luận sạch; ID issue comment dạng float. Giữ chốt sản phẩm, gộp/parameter hoá test để không vượt 450 dòng. |

Lý do giữ P3: nợ độ phủ đã phân hạng ở lượt 7, không phải hành vi sai mới do merge. Không đổi slug, nâng hạng hay tự ghi quyết định P3 thay chủ kho trong state máy.

**Toàn vẹn và giới hạn.** Snapshot đầu/cuối bao gồm tracked, untracked, ignored và `.git`: **6375 → 6375 tệp thường, 0 delta byte/mode**, không symlink. HEAD/tree, diff worktree/index, status của `src` và `out/copy` được kiểm lại, đều đúng/sạch; xem `SOURCE_INITIAL.json`, `SOURCE_FINAL.json`, `SOURCE_INTEGRITY.json`, `FINAL_CHECKS.json`. Đây là phép đối chiếu hai mốc, không phải giám sát mọi write trong lịch sử. Sandbox thực tế là workspace-write; nguồn được xử lý chỉ đọc, mọi tệp do reviewer tạo/sửa nằm trong OUT.

`not_run`: full suite `python .claude/dev/packet_loop_test.py` (~50 phút, prompt không bắt buộc reviewer chạy lại), CI online, Windows, bare Ruff lint, các probe thiết kế/A–B riêng của lượt 7 và các nhóm ngoài tập đã nêu. Không nhận lời khai suite executor đang chạy là kết quả độc lập, không suy 212/212 thành N/N toàn repository. Không có finding P0/P1/P2 mới trong phạm vi xác minh merge này. Các artifact cấp OUT được băm trong `ARTIFACTS.json`; bản sao/fixture không thuộc manifest đó.
