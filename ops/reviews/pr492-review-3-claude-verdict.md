verdict: approve
reviewed_sha: 457affd49fabb8f6d891b93460e93255170c8784
reviewed_base: c0a5cbe89a90588115262e1a2c3ac84cbd98be9e
reviewed_spec_sha256: 465538364b1a3f9477782fba79869bbd1c9351140e3fa9df50451baae22f9c79
reviewed_adr0047_sha256: b9975929c52e12767417b46b47829c265230117fe65df6a9fd22540d4868fdab
reviewed_files_sha256: lease_publish.py 0b6ab5b9e82463535d899b1be57d2479a37094b19b77600a24dfc4552b5742a8 · lease_publish_test.py bc9df203be4cdb87130307377634fb9c9a4a05d2e314783415e1dd423e277a75 · ops-thu-hoi-admission.yml f7e5fd2d0fb38caa064632355fd98d51acd2fddbe03886754ead848db443ea62
model_tu_khai: khởi phiên harness báo `claude-fable-5` (effort max, đúng phân công); GIỮA LƯỢT harness đổi tuyên bố sang `claude-opus-4-8` (hai lần cập nhật môi trường). Tự khai theo tuyên bố của harness, KHÔNG có phép đo độc lập model build; nêu cả hai để trung thực. Kỷ luật review không đổi theo nhãn model.
provider: anthropic
review_class: sensitive
lease: wp488-thu-hoi-lease-a0-exec-1-claude-20260909
review_round: 3
started_at_utc: 2026-09-10T03:4xZ

**KHÔNG P1. KHÔNG P2 executor vá được trong packet ⇒ `approve`.** Bản vá `bd4ecd4..457affd` ĐÚNG là HINT lượt 2 (F10 code+test, khớp TỪNG DÒNG với `HINT.luot2.patch`) + F12 workflow (đúng khuôn `CHECKER_RC=0; … || CHECKER_RC=$?; [ … -eq 0 ] || exit "$CHECKER_RC"`), không có dòng nào ngoài phạm vi đã khai. F10/F11/F12 ĐÓNG, đo hai chiều: cả ba catch/guard nay có RĂNG ở chốt chịu lực (`TinHieuChotCa`), không phải lỗi vô can. Không mở lỗ MỚI. Các mục còn mở (F07 pin `upload-artifact`, F08 manifest ADR-0047 lớp 2, Q7, `DESCRIPTOR_Q13_SHA256=None`) ĐÃ CÓ CHỦ (chủ kho/A1), đều fail-close, **KHÔNG chặn merge A0** — chỉ chặn bật required check / duyệt mỏ neo đầu tiên (A1). F13/F14 là P3 executor khai không vá, không mở lỗ, không chặn.

**Khai báo sự cố môi trường (không phải lỗi executor):**
1. Harness TỰ ĐỘNG bơm nội dung `cay-kho/CLAUDE.md` vào ngữ cảnh (khi một lệnh Bash `cd cay-kho` làm cwd trôi vào kho — đúng sự cố lượt 2 đã gặp). Tệp thuộc danh sách CẤM ĐỌC của phân công; tôi KHÔNG yêu cầu và KHÔNG dùng nội dung đó — mọi hợp đồng trích trong verdict dẫn từ `SPEC.md`/`ADR-0047.md`/`EVIDENCE.md`/`VERDICT.luot{1,2}.md` và từ mã/số đo. Sau đó tôi reset cwd về thư mục review và chạy git bằng `git -C cay-kho …`. `docs/PROTOCOL_DA_PHIEN.md`, `.claude/**`, `ops/reviews/**` KHÔNG đọc.
2. Nhãn model của phiên đổi giữa lượt (fable-5 → opus-4-8) như ghi ở `model_tu_khai`.

Kỷ luật: read-only mức git với `cay-kho/` (kiểm cuối — HEAD `457affd`, worktree **0 dòng porcelain**, sha256 ba tệp khớp đầu lượt); mọi bản sao/đột biến nằm trong `scratch/luot3/`; `sys.dont_write_bytecode`/`PYTHONDONTWRITEBYTECODE=1` (không .pyc rớt vào kho); không mạng; không dựng ca thuộc lớp cấm — các ca âm chỉ CHẠY/ĐỘT BIẾN BẢN SAO của t150 và t129/t130/t136/t139/t149 có sẵn. Fixture non-UTF-8 là bytes/tên latin-1 thông thường trong kho Git thật.

## Bản vá so HINT

| Đường | Kỳ vọng | Đo được |
|---|---|---|
| `ops/lease_publish.py` (F10) | = hunk mã của `HINT.luot2.patch` | **KHỚP TỪNG DÒNG** (so cơ học sau khi chuẩn hoá header hunk; 14 dòng hunk) |
| `ops/lease_publish_test.py` (t150) | = hunk test của `HINT.luot2.patch` | **KHỚP TỪNG DÒNG** (41 dòng hunk) |
| `.github/workflows/ops-thu-hoi-admission.yml` (F12) | chỉ `CHECKER_RC=0; … || CHECKER_RC=$?; [ … -eq 0 ] || exit "$CHECKER_RC"` | **ĐÚNG KHUÔN** — thêm `CHECKER_RC=0`; nối `|| CHECKER_RC=$?` vào lời gọi python (bỏ dòng `CHECKER_RC=$?` chết); thêm guard `[ "$CHECKER_RC" -eq 0 ] || { echo "bộ kiểm canonical rc=$CHECKER_RC" >&2; exit "$CHECKER_RC"; }`. Kèm 1 dòng CHÚ THÍCH và 1 `echo … >&2` trong thân guard — **không phải dòng ngoài phạm vi**: chú thích không có hành vi, `echo >&2` khớp ĐÚNG idiom của MỌI guard `exit 12` khác trong chính tệp (dòng 75–96, 109). numstat `bd4ecd4..HEAD` = wf +4/−2 · mã +5/−2 · test +34/−0, khớp EVIDENCE. |

Kết luận mục 1 phân công: **executor KHÔNG sửa gì ngoài F10 (HINT lượt 2) + F12.** Không finding.

## F10–F14 → trạng thái

| F | Hạng | Trạng thái | Bằng chứng đã chạy tại HEAD `457affd` |
|---|---|---|---|
| **F10** consumer Q13 nổ UnicodeDecodeError | P2 (lượt 2) | **ĐÓNG** | `_kiem_so_rong_khi_chua_kich_hoat` nay bọc `try/except UnicodeDecodeError` quanh `cat-file blob`, `p=None` rơi vào Chan 12 THÔNG ĐIỆP CŨ. Probe `policy_nonutf8_consumer` (kho Git thường, marker retired + policy `b'{"a": "\xc3\x28"}'`): `ai-dang-giu … --root <kho>` ⇒ **rc=12, `Traceback` không xuất hiện**, đúng thông điệp "…policy … vắng hoặc không phải JSON object (Q13)". t150(a) QUA. Đột biến `mut_kiemrong_nocatch` (bỏ catch mới) ⇒ t150 **GIẾT ở `TinHieuChotCa`** ("policy không phải UTF-8 làm CLI nổ UnicodeDecodeError — hợp đồng đòi Chan 12"). |
| **F11** chốt catch của `_ls_tree_z` thiếu răng | P3 (lượt 2) | **ĐÓNG** | Đột biến `mut_lstree_nocatch` (xoá `except UnicodeDecodeError` của `_ls_tree_z`) nay **GIẾT ở `TinHieuChotCa`** tại t150(b) ("tên không phải UTF-8 làm CLI nổ UnicodeDecodeError") — lượt 2 SỐNG, nay CHẾT đúng nơi khai. Probe tên tệp non-UTF-8: rc=12, không traceback, thông điệp "ls-tree -z … có tên không phải UTF-8". |
| **F12** `CHECKER_RC=$?` dòng chết dưới `set -e` | P3 (lượt 2) | **ĐÓNG** | Demo `set -euo pipefail`: khuôn CŨ (`false; X=$?; echo`) thoát tại `false`, `X=$?` KHÔNG bao giờ chạy ⇒ trường `checker_rc` chỉ có thể là 0. Khuôn MỚI: rc thật vào biến — `(exit 12)` ⇒ exit **12**; `(exit 8)`⇒**8**; `(exit 4)`⇒**4**; đường thành công `CHECKER_RC=0` qua `set -u` (đã khởi tạo), guard KHÔNG thoát, tới bước sau. actionlint 1.7.7 **rc=0** + shellcheck 0.9.0 **rc=0** trên workflow/run block mới. |
| **F13** rò 3 fd ống đường deadline | P3 (lượt 2) | Executor khai KHÔNG vá — chấp nhận | Child bị killpg+reap (không rò tiến trình, t145 đo); bounded 1 lần/lời gọi chết; Chan 12 kết thúc CLI ngay. Không mở lỗ, không chặn A0. Ghi nhận cho consumer chạy dài A1+. |
| **F14** clock snapshot per-record M4 | P3 (lượt 2) | Executor khai KHÔNG vá — chấp nhận | Lệch micro-giây theo chiều CHẶT→lỏng trong một lần chạy; mọi revocation vẫn 12 ở inactive. Không mở lỗ, không chặn A0. |

## Findings mới

**KHÔNG CÓ.** Ba nghi vấn "chỗ mới mà bản vá mở ra" (mục 3 phân công) đều ĐÓNG:

1. **`except UnicodeDecodeError` mới có nuốt lỗi KHÔNG phải nguồn hỏng?** KHÔNG. `try` bọc DUY NHẤT lời gọi `GOI_GIT("cat-file","blob",…)`; `GOI_GIT` là `subprocess.run(text=True)`, nên `UnicodeDecodeError` chỉ phát khi git in bytes không giải mã được (blob policy không UTF-8, hoặc stderr non-UTF-8 khi git lỗi) — cả hai đều là "nguồn không giải mã được" = 12 đúng hợp đồng. Catch KHÔNG bắt `OSError`/lỗi khác (khác `_ls_tree_z` vốn bắt cả `OSError`) nên không che bug spawn; đó là hành vi CŨ của đường cat-file, patch không đổi.
2. **`p = None` rồi rơi vào Chan 12 thông điệp cũ — t133/t140/t142 còn đúng?** CÒN. `if p is None or p.returncode != 0 or …` **đoản mạch** ở `p is None` ⇒ không chạm `p.returncode` (không AttributeError), raise Chan với chuỗi Q13 BYTE-IDENTICAL. Patch KHÔNG đổi bất kỳ chuỗi thông điệp nào; t133/t140/t141/t142/t150 QUA trong suite 145/145.
3. **Workflow: `CHECKER_RC` lọt qua `set -u` khi checker thành công? `exit "$CHECKER_RC"` giữ đúng 12/8/4?** ĐÚNG cả hai (demo ở F12). `CHECKER_RC=0` khởi tạo trước nên `set -u` không nổ; `exit "$CHECKER_RC"` giữ nguyên số.

Ngoài ra: workflow permissions vẫn CHỈ ĐỌC (`contents/pull-requests/actions: read` ở cả job lẫn workflow), checkout `base.sha` (S) + `persist-credentials: false`, không checkout cây ứng viên — patch F12 KHÔNG đụng quyền/route ⇒ không hồi quy P1 "workflow chạy code ứng viên hoặc có quyền ghi".

## Còn mở có chủ

Không đổi so lượt 2; **không mục nào là lý do `changes_requested` cho executor**, và **không mục nào chặn merge A0** (đều fail-close tuyệt đối ở A0). Xếp lại đúng chủ:

| Mục | Hạng | Chủ | Chặn gì |
|---|---|---|---|
| F07 — `actions/upload-artifact@v4` pin bằng TAG, không commit (SPEC M9 dòng 454) | P2 | chủ kho (cấp SHA đã readback) | Chặn **A1** (trước khi bật required check). KHÔNG chặn A0: workflow chưa required. |
| F08 — hồ sơ adapter chưa mang identity HTTPS-helper/runtime/thư viện/trust store (ADR-0047 lớp 2 dòng 46–49) | P2 | chủ kho/A1 | Chặn **A1** (duyệt mỏ neo đầu). KHÔNG chặn A0: `PROFILE_ADAPTER_DA_DUYET` rỗng ⇒ mọi discovery production = 12. |
| `DESCRIPTOR_Q13_SHA256 = None` | — | A1 (ghim từ comment 5575587924) | Chặn **A1**. Ở A0 fail-close (marker mới khi mỏ neo None ⇒ 12). |
| Q7 (ADR-0044) — tổng +2282 vượt trần | — | spec r9 §write_set khai ngoại lệ có phạm vi | Không chặn (ngoại lệ đã khai). |
| Ngoài packet: `_quet_lease_toan_kho` (luật cũ) cùng lỗi quote F02; `_du_bao_check` chưa đỡ decode (không tới được ở A0) | P3 | packet luật cũ / A1 | Không chặn A0. |

## Mutant đã chạy

Cơ chế: bản sao trong `scratch/luot3/` (`mut_runner.py`), mỗi mutant một tệp module riêng, thay `_nap_cong`; phân hạng **GIẾT chỉ khi `TinHieuChotCa`** (lớp assertion riêng của ca đích — mã triển khai không giả được), `AssertionError` khác = KILL_ASSERT_KHÁC, lỗi khác = CHẾT_VÔ_CAN.

| Mutant | Nguồn | Ca đích | Kết quả | Ý nghĩa |
|---|---|---|---|---|
| đối chứng t150 HEAD | — | t150 | **SONG(PASS)** | ca xanh trên mã chưa đột biến |
| `mut_kiemrong_nocatch` (F10) | xoá `try/except UnicodeDecodeError` mới của `_kiem_so_rong` | t150(a) | **GIẾT ở `TinHieuChotCa`** | catch F10 có răng, đúng chốt chịu lực |
| `mut_lstree_nocatch` (F11) | xoá `except UnicodeDecodeError` của `_ls_tree_z` | t150(b) | **GIẾT ở `TinHieuChotCa`** | lượt 2 SỐNG → nay CHẾT; F11 đóng |
| catalog t139 (33 mutant) | t139 tại HEAD | từng ca khai | **33 = 30 GIẾT / 3 SỐNG có chủ đích / 0 tín dụng giả** | không đổi so lượt 2 |

Kiểm anchor drift (mục 4 phân công): F10 sửa NHÁNH `metadata` (dòng `cat-file blob`) của `_kiem_so_rong`; catalog anchor chạm hàm này là `M2-bo-chot-so-rong` — nhắm NHÁNH `thu_hoi` (dòng KHÔNG đổi). Không mutant catalog nào neo vào dòng vừa sửa ⇒ kết quả 30/3/0 GIỮ NGUYÊN, không anchor nào đổi kết quả vì bản vá. Không finding.

## Bảng đo lại

| Phép đo | Kết quả tại môi trường review | Bằng chứng |
|---|---|---|
| HEAD / base / origin/master / worktree | `457affd…8c784` / `c0a5cbe…be9e` / `28ba133` / **sạch (0 dòng porcelain, đo cuối lượt)** | `git -C cay-kho rev-parse/status` |
| sha256 SPEC / ADR-0047 / 3 tệp head | khớp cả 5 giá trị được giao (`4655…`, `b997…`, `0b6a…`, `bc9d…`, `f7e5…`) | `sha256sum` đầu lượt |
| bản vá code+test vs `HINT.luot2.patch` | **KHỚP TỪNG DÒNG** cả hai tệp (so cơ học chuẩn hoá header hunk) | `scratch/luot3/patch-actual-code-test.diff` + script so |
| numstat `c0a5cbe..HEAD` | 3 đường: wf +141/−0 · mã +883/−0 · test +1258/−1 = **+2282/−1** (ADR-0044 ngoại lệ khai); name-only = đúng write set | `git diff --numstat/--name-only` |
| numstat `bd4ecd4..HEAD` (bản vá lượt 3) | wf +4/−2 · mã +5/−2 · test +34/−0 | `git diff --numstat` |
| write set ∩ (packet_loop/ops-thu-hoi/ops-publish-lease/ci.yml) | **∅** (write set đúng 3 đường) | name-only |
| master drift `c0a5cbe..origin/master` ∩ write set | **∅** (drift = CHANGELOG/RELEASE_MANIFEST/ops/land/ops/reviews; 2 merge `7693852`,`28ba133`) | `comm -12` |
| `SO_THU_HOI_KICH_HOAT` | `False` (dòng 929) | grep |
| Suite tại HEAD (PATH có actionlint 1.7.7 + shellcheck 0.9.0) | **145/145 đạt; đã chạy=145, bỏ qua=0; rc=0** (t33/t137 CHẠY, không skip) | `scratch/luot3/suite-luot3-lint.log` |
| Suite KHÔNG có actionlint trên PATH | 143/145 (t33/t137 `chua_do_duoc`) — artifact môi trường, không phải lỗi mã | `scratch/luot3/suite-luot3.log` |
| t139 catalog | "mẫu số=33, giết thật=30, SỐNG có chủ đích=3, tín dụng giả=0" | suite log |
| F10/F11 probe (policy non-UTF-8; tên tệp non-UTF-8) | rc=12, `Traceback` không xuất hiện, thông điệp Q13/ls-tree đúng | phiên (importlib) |
| Đột biến bỏ từng catch → t150 | GIẾT ở `TinHieuChotCa` (không lỗi vô can) — cả hai | `scratch/luot3/mut_runner.py` |
| Demo F12 `set -e` | khuôn cũ: `X=$?` chết; khuôn mới: rc 12/8/4 giữ nguyên, thành công CHECKER_RC=0 qua set -u | phiên (bash) |
| actionlint / shellcheck trên workflow mới | rc=0 / rc=0 (run block, bash) | phiên |
| product verdict luật cũ | t53 + t135 có mặt và QUA trong suite 145/145 | suite log |
| chặn oan canonical (Q13) | (giữ từ lượt 2) `c0a5cbe` không có policy/ops-thu-hoi ⇒ chốt Q13 không đỏ oan PR thường — không đo lại lượt này (base không đổi) | VERDICT.luot2 |

## chua_do_duoc

1. **GitHub/Actions thật:** không mạng — không đo run `34401567971` (`457affd`), jobs API thật, quan hệ `workflow_sha`/base.sha trên `pull_request_target` thật, artifact upload/readback, canary A0 (SPEC M9 dòng 466). Các trường F07 (check_run_id, run_attempt filter) chỉ kiểm hình dạng + logic cục bộ.
2. **Suite qua wrapper `chay_lease_publish_test.sh` trong chính `cay-kho/`:** giữ read-only mức git; tôi chạy suite trong `cay-kho/` với `PYTHONDONTWRITEBYTECODE=1` (không qua wrapper) và đo 145/145 rc=0 khi actionlint+shellcheck trên PATH — nhất quán với `suite_sandbox.log` của executor. Số wrapper 145/145 là lời khai executor, khớp số đo của tôi.
3. **Codex connector review độc lập trên `457affd`** (EVIDENCE nhắc comment 5612219372): không mạng, không đọc/đối chiếu được — độc lập với lượt này.
4. **doctrine-scan / doc-claims-check / release-verify / gate ngoài suite:** công cụ nằm trong `.claude/dev/**` thuộc vùng CẤM ĐỌC — không chạy, không chứng nhận các dòng ấy trong EVIDENCE.
5. **Pin `upload-artifact` bằng commit & manifest ADR-0047 lớp 2:** cần chủ kho cấp SHA đã readback / duyệt manifest — ngoài khả năng đo của sandbox (P2 có chủ, chặn A1 không chặn A0).
6. **Model identity:** tự khai theo tuyên bố harness (đổi giữa lượt); không có phép đo độc lập build.
