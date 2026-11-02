verdict: approve
reviewed_sha: f46115b42220620bb681abcad6399542c9b7c7b0
spec_sha256: dee36a1148bc1fe8a934a9dceb74dbe0eab7d3a2830908d7f15afb3293f0812e
Ket qua: 0 P0, 0 P1, 0 P2, 0 P3.

Đóng finding còn lại của lượt 2; giữ đóng F1/F2 lượt 1. Không phát hiện finding mới sau khi chạy lại cùng phép đo trên base và HEAD. Approve nội dung tại exact SHA dòng 2; **không tuyên bố toàn bộ nghiệm thu đã đạt hoặc đủ điều kiện merge**: A4 nguyên trạng còn thiếu một phần do sandbox, A5 chưa đo được vì offline. Không phản đối quyết định chủ kho chấp nhận giới hạn vĩnh viễn.

## Phạm vi, authority và định danh

- Packet #825, revision 1, generation 1, lease `wp825-r1-g1-claude`, class `sensitive`. Ngưỡng riêng của assignment: không còn P0/P1/P2/P3.
- Immutable acceptance baseline: `c7174bfe03b3acd22cfa055b5fce176129d29542`. Reviewed candidate: dòng 2; tree `4c6001c924fb21acc35d027ee2696ef3c469df2a`.
- Nguồn spec authoritative offline: commit `18a5f89442545943ac7a4965063dc7db01ed8a5a`, ref local `refs/remotes/origin/ops/wp825-r1-g1-lease`, blob `ops/specs/wp825.md`. `git show` khớp byte bản giao `../SPEC.md`; SHA-256 tự đo ở dòng 3. Lease cùng ref khớp packet/r1/g1/base/write set/class/trần 10 lượt theo ADR-0055. Không làm mới ref qua mạng.
- Diff base→HEAD khớp `../diff.patch`: đúng hai tệp, ADR mới 85 dòng và đúng một dòng §20. Diff `df3e103b6b0c8ac9259c040a518c7baf99f46790`→HEAD khớp `../diff-tu-l2.patch`, chỉ đổi tiêu đề ADR. Bốn tệp runtime/test có byte giống nhau ở base/HEAD; `packet_loop.py` cũng giống nhau.
- Reviewer theo `../run/2f47926d/run.json`: `provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine`, run `2f47926da5a74a45ad321ae45e2fb541`. Executor theo lease khai Claude/claude_code. Không đo độc lập model/effort thực sự phục vụ từng response hoặc byte lời duyệt AskUserQuestion; không suy các dữ kiện đó từ cấu hình/lease.
- Linux, Python 3.13.18. Không gọi mạng, không dùng credential thật, không chạy login/LIVE, không push/đăng verdict/merge/land hay chuyển state điều phối. Mọi scratch, bản base, mutant và artifact nằm ngoài `cay-kho/`.
- Snapshot đầu/cuối khớp HEAD/tree, status, diff/index và nội dung 10.814 path tracked/untracked/ignored, không path đổi (`evidence/final-integrity.json`). Đây là hai mốc quan sát nội dung, không phải chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên hay đo mọi metadata hệ tệp. Checkout được giữ read-only theo chỉ thị, không được mount read-only riêng.

## Lệnh tái lập và giới hạn phép đo

Từ `cay-kho/`, các lệnh sau đã chạy, rc=0:

```bash
python3 -B ../evidence/review_checks.py
python3 -B ../evidence/check_facts.py
env -i PATH=/usr/local/bin:/usr/bin:/bin LANG=C.UTF-8 PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/../evidence/tmp" python3 -B ../evidence/repro_probe.py
python3 -B ../evidence/supplement.py
python3 -B ../evidence/final_audit.py
```

Bốn script đầu lấy từ `evidence-l2/`: chỉ thay HEAD SHA trong `review_checks.py` và run ID trong `check_facts.py`; `repro_probe.py` và `supplement.py` giữ nguyên byte. Hash `repro_probe.py`: `442b8e512ab4e8f8445d342d87961a50b4475562e14c0fb324a62c2778ffe6ef`, đúng phép đo lượt 1/2. Runner nghiệm thu dùng môi trường sạch không kế thừa credential, tắt bytecode, TMPDIR tuyệt đối ngoài checkout, bỏ Git config system/global và ghim `core.abbrev=7`. Base xuất bằng `git archive` từ exact baseline vào `evidence/base/`.

`evidence/*.json` lưu command/cwd/rc/stdout/stderr của lệnh con; rc=0 của runner không thay rc của test. Log tổng: `review-checks.log`, `check-facts.log`, `probe-repro.log`, `supplement.log`, `final-audit.log`. Một lần đầu script tổng hợp cuối đọc quá cuối tệp đã trả rc=1 (`final-audit-initial-error.log`); sửa giới hạn trích dòng trong scratch rồi chạy lại rc=0. Không sửa sản phẩm để làm xanh.

Sandbox chỉ cho ghi workspace và `/tmp`. `/tmp/.git` hiện tồn tại; constructor `_KhoCodex` từ chối mọi descendant. Vì vậy không thể dùng TMPDIR ngoài `/tmp` như executor đã làm với `/var/tmp` trong quyền hiện hành. Không xóa thư mục của sandbox, không bỏ chốt constructor trong các lệnh A4. Phép đo bổ sung cấp dirfd riêng, dùng read/write sản phẩm và auth INERT/probe giả; constructor kiểm ancestor/ACL bị thay bằng fixture. **Không dùng kết quả fixture để khai A4 nguyên trạng xanh.**

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding / lớp | Bằng chứng tự đo trên HEAD | Phân loại |
|---|---|---|
| Lượt 2: `loi-ghi-khong-suy-ra-probe-lap` [P2], còn ở tiêu đề ADR | Tiêu đề ADR:1 nay là “Chấp nhận vĩnh viễn khả năng probe lặp khi không ghi được trạng thái từ chối Codex”. Không còn kết luận chắc chắn lần sau probe. Ma trận 24 tổ hợp vẫn tái lập hai phản chứng `[1,0]`, và thân ADR:19–32/§20:1548 khớp điều kiện. | **ĐÃ VÁ THẬT**; đóng P2 lượt 2. |
| Lượt 1 F1 [P1], cùng lớp trên | ADR:15–32 nhận cả state đã promote rồi mới lỗi và state không đọc được; không còn “mọi lần thêm đúng 1”, “cùng lý do” vô điều kiện hay bảo đảm state không đổi. Tiêu đề và §20 cùng thu hẹp thành khả năng. | **ĐÃ VÁ THẬT**, giữ đóng toàn bộ lớp; không thấy lỗi mới từ đổi tiêu đề. |
| Lượt 1 F2: `grep-ten-khong-do-khai-niem` [P2] | Đo lại hai regex × sáu vị trí × base/HEAD; định danh đều 0, khái niệm launcher 4. ADR:65–85 và §20 phân biệt “có nhắc”, consumer metadata và cưỡng chế quyết định. | **ĐÃ VÁ THẬT**, giữ đóng. |

## BANG NGHIEM THU

Các lệnh dưới đã chạy với cwd gốc từng cây, môi trường của runner. Với base, cwd là `../evidence/base/`.

| Tiêu chí | Lệnh chạy được | Kết quả / kết luận |
|---|---|---|
| A1 | `python3 -B .claude/dev/packet_loop.py adr-song --root .` | HEAD rc=0, `60 ADR trên đĩa, 60 dòng trong §20`; base rc=0, 59/59. Trên bản sao bỏ đúng dòng ADR-0061 rồi gọi cùng consumer: rc=9, báo có tệp mà thiếu dòng §20. **ĐẠT dương/âm**. |
| A2 | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | Base/HEAD rc=0, quét 10 tệp, 0 chỗ chép doctrine. **ĐẠT**. |
| A3 dương | `python3 -B ../evidence/review_checks.py`: nối whitespace ADR, kiểm năm chuỗi | `evidence/a3.json`: `CODEX_HOME`, `_danh_dau_auth_hong`, tên ca launcher, `g7_nuot_loi_ghi_trang_thai`, `#825` đều true. **ĐẠT**. |
| A3 âm | Hai lệnh `rg -c` dưới đây trên đủ sáu tệp; đọc các nhánh runtime và consumer `packet_loop.py:1917–2009` | Không tự khai cổng thực thi quyết định chấp nhận; ADR khai đúng proxy “có nhắc” và việc `adr-song` đọc metadata. **ĐẠT**. `explicit_zero_gates: false` là đúng văn bản đã sửa, không phải A3 âm thất bại. |
| A4 launcher | `python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra --lan 1` | Base/HEAD rc=0, `1/1 qua, 0 bo qua, 0 hong`. **ĐẠT riêng ca này**. |
| A4 materializer | `python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do --lan 1` | Base/HEAD rc=1, `0/1 qua`, setup `OSError: Codex home is inside a repository`. **FAILED khi chạy; KHÔNG ĐO ĐƯỢC hành vi nguyên trạng** do ancestor `/tmp/.git`. |
| A4 credential | `python3 -B .claude/dev/codex_cred_test.py` | Base/HEAD rc=1, nền `13/18 đạt`, `TỔNG: ĐỎ`; t6/t9/t16/t18 OSError, t15 sai kỳ vọng do chốt repo. Nền đỏ nên không chạy đột biến full suite. **FAILED khi chạy; KHÔNG ĐO ĐƯỢC TỔNG: ĐẠT nguyên trạng**. |
| A5 | Check run `ci.yml` trên exact head dòng 2 | **KHÔNG ĐO ĐƯỢC / not_run**, theo chỉ thị offline; không có check-run readback exact-head trong bundle. Local gate không thay CI. |

Chạy thêm `python3 -B scripts/tl.py doc-claims-check --strict`: rc=0, `ok: true`, 381 advisory nền (`evidence/doc-claims.json`). Gate này kiểm hình thức, không thay đối chiếu ngữ nghĩa.

A1–A3 đạt; A4 mới xác nhận nguyên trạng một ca, không nhận toàn tiêu chí đạt; A5 chưa đo. Lời khai executor về hai ca 1/1 và 18 ca/18 đột biến tại TMPDIR=/var/tmp không bị bác bởi lỗi setup reviewer, nhưng cũng không thay bằng chứng độc lập còn thiếu.

## BANG DO

Số dòng mã/test dưới đây trùng base/HEAD. `evidence/source-facts.json` lưu trích mã kèm dòng/hash hai cây; `check_facts.py` lưu provenance, đăng ký ca/đột biến và tính duy nhất mỏ neo. Các dòng ADR dùng HEAD.

| Khẳng định | Đo được (lệnh/consumer) | Khớp? |
|---|---|---|
| Accepted, r1/g1, băm spec; chủ kho chọn ADR | `git show refs/remotes/origin/ops/wp825-r1-g1-lease:ops/specs/wp825.md`; lease cùng ref; `sha256sum ../SPEC.md` | Khớp metadata local. Lựa chọn chủ kho nhận làm authority đầu vào theo prompt; không đo byte hội thoại hay GitHub trực tiếp. |
| Nợ #825 sinh từ #484, PR #792 | `rg -n 'codex-rejected-state-khong-ghi-duoc' ops/land/pr792-wp484-land-evidence.yaml ops/handoff/wp484-g7-claude.md` | Khớp hồ sơ local (land evidence:142, handoff:52); không tái xác nhận sự kiện mạng. |
| Ghi danh tính credential bị từ chối qua `_KhoCodex` dưới CODEX_HOME | `sed -n '3540,3617p' .claude/dev/launcher.py`; `_credential_id`:3554, `_ghi_rejected`:3578, `_danh_dau_auth_hong`:3589 | Khớp helper: lấy danh tính từ bytes đã probe, ghi `credential-recovery.json`; catch OSError/ValueError/UnicodeError trả False. Materializer gọi `_ghi_rejected` trực tiếp ở :3704. |
| Đã nhớ id thì chặn credential ấy | `_dang_cho_snapshot`:3607–3616; launcher guard:3875; materializer:3674–3678; credential guard:518 | Khớp. Đối chứng thành công ở cả ba lối cho `[1,0]` và đúng id trong state. |
| Không dựng chỗ lưu dự phòng | `rg -n 'credential-recovery\.json|codex-rejected-state-khong-ghi-duoc' .claude/dev/launcher.py .claude/dev/codex_cred.py`; đọc ba nhánh ghi | Khớp phạm vi mã được xét: một file/backend state, không nhánh fallback. Không suy thành kiểm mọi dịch vụ ngoài kho. |
| Tiêu đề: chấp nhận khả năng probe lặp | Đọc ADR:1 cùng :15–32; `python3 -B ../evidence/repro_probe.py` | Khớp điều kiện có thể xảy ra, không còn suy lỗi ghi ⇒ chắc chắn probe lại. |
| State đọc được, chưa nhớ id, credential giữ nguyên, vẫn bị từ chối, lỗi trước promote lặp ⇒ probe lặp | `repro_probe.py`, chế độ `fail_before_replace`, hai lượt cả ba lối/cả hai cây | Khớp: `[1,1]`, không nhớ id, auth cũ nguyên vẹn. |
| “Mỗi lượt đi đến nhánh này gọi helper probe một lần” | Đọc `_probe_snapshot`:3619–3636, `chuan_bi_xac_thuc`:3665–3729, `_do_codex_song`:3859–3901, `cmd_kiem`:482–529; fixture đếm helper | Khớp phạm vi nhánh trực tiếp. Materializer chỉ probe khi có auth cũ khác snapshot, thời gian phù hợp, chưa bị rejected/history chặn, apply thật. Không thấy >1 helper trong một lượt trực tiếp đi tới nhánh lỗi đã khai. |
| Đơn vị helper, chưa đo request mạng trong CLI | ADR:20–21; `_kiem_song` tại `codex_cred.py:183–222` spawn một `codex exec`; `_do_codex`:3990/3998 có return loại trừ nhau | Khớp mức lời khai. Không nâng một helper/subprocess thành đúng một HTTP request hoặc bảo đảm cho mọi lệnh tổng hợp. Wrapper `lenh_run`:2165–2168 và `_chuan_bi_va_bo_snapshot`:3228–3232 dừng khi materializer thất bại. |
| Ghi hỏng có thể đã đổi state; lần sau 0 probe, lý do khác | `_KhoCodex.write`:3388–3391 replace trước fsync thư mục POSIX; `repro_probe.py` chế độ `fail_dir_fsync_after_replace` | Khớp: cả ba lối `[1,0]`, đúng id đã lưu. Không diễn giải False thành mọi file giữ nguyên. |
| State không đọc được cũng chặn, materializer có lỗi chung | `_dang_cho_snapshot`:3615–3616; materializer outer catch:3726–3728; fixture `unreadable_state_after_probe` | Khớp: `[1,0]`, không nhớ id; lý do lượt sau khác lỗi ghi đầu tiên. |
| Không bảo đảm mọi lỗi I/O/xen kẽ; không ghi sai trạng thái trong fixture | `repro_probe.py`: 24 tổ hợp × hai lượt; kiểm `auth_unchanged`, `unprobed_old_recorded`, `target_recorded` | Khớp giới hạn ADR:31–32. Mọi tổ hợp giữ auth cũ, không ghi id credential chưa probe; chỉ xác nhận các trường hợp đã đo, không chứng minh bảo đảm tổng quát hoặc giải quyết #824. |
| Launcher báo lý do CHẶN lỗi ghi riêng | `launcher.py:3895–3897`; A4 launcher; `supplement.py` với `g7_nuot_loi_ghi_trang_thai` | Khớp: `KHÔNG ghi được trạng thái chờ snapshot sau khi … — CHẶN: sửa CODEX_HOME (quyền/dung lượng) trước khi thử lại`. Baseline qua, mutant bị assertion đúng ca bắt trên base/HEAD. |
| Materializer báo lỗi ghi riêng, giữ credential cũ | `launcher.py:3704–3709`; fixture I/O và ca/mutant đích | Khớp: `CHỜ snapshot mới: auth bị từ chối nhưng KHÔNG ghi được trạng thái chờ (OSError) — CHẶN; giữ credential cũ`. Baseline fixture qua, mutant lỗi “lý do bị gộp”; A4 nguyên trạng vẫn thiếu do môi trường. |
| `codex_cred.cmd_kiem` báo lỗi ghi riêng, trả ĐỎ | `codex_cred.py:524–529`; fixture gọi thật `cmd_kiem`, ca t16/mutant `t16_nuot_loi_ghi` | Khớp: prefix lỗi ghi, đuôi `CHẶN: sửa CODEX_HOME trước khi thử lại`, rc=2. Baseline fixture qua, mutant lỗi “lỗi ghi bị nuốt”. |
| Ba lối đều có ca và đột biến khóa | `check_facts.py` AST; `supplement.py`; bảng ca bên dưới | Khớp đăng ký, mỗi mỏ neo đúng 1 lần; cả sáu mutant (ba tên × hai cây) bị đúng assertion ca đích bắt, sáu baseline qua. Materializer/t16 dùng seam constructor, không thay full suite. |
| Hai ca 1/1, suite TỔNG: ĐẠT đã đo lúc 00:5xZ trên c7174bf | Lệnh tái lập ADR:49–51 đã chạy trên exact base và HEAD | Có lệnh và ca thật; reviewer chỉ tái chứng nhận launcher 1/1. Chưa tái chứng nhận full historical pass/thời điểm vì lỗi setup; không khai lời lịch sử sai chỉ từ lỗi sandbox. |
| Sửa quyền/dung lượng rồi thử lại; login hoặc chuan-bi khôi phục | Đọc `_ghi_rejected`, ba nhánh ghi; parser `codex_cred.py`, `lenh_chuan_bi`:4946–4958 và materializer | Hướng gỡ khớp có điều kiện. Snapshot từ biến phải đủ điều kiện, không thể dùng lại id đã biết hỏng; không chạy login/chuan-bi với credential thật. |
| Dự phòng thường hỏng cùng nguyên nhân, mua thêm ít | Đọc ADR:59–63 | Được ghi rõ “suy luận, CHƯA ĐO trên từng loại hỏng”. Không dùng fault injection ở đây để chứng minh đầy đĩa/quyền/read-only thực hoặc mọi chỗ dự phòng cùng hỏng. |
| Sáu cổng: định danh 0, khái niệm launcher 4 | Hai regex trên từng tệp/base/HEAD; log `*-gate-*.json`, `*-concept-*.json` | Khớp bảng dưới. Chỉ là proxy; không nâng thành số cổng cưỡng chế. |
| §20 đúng một dòng/bốn cột; Accepted, giới hạn, ba lối và cổng khớp ADR | `git diff --numstat BASE HEAD`; `final_audit.py` bỏ đúng dòng mới rồi so byte protocol với base; A1 dương/âm | Khớp. Protocol còn lại nguyên byte, dòng :1548 nằm trong bảng parser đọc. |
| `adr-song` đọc đăng ký/metadata, không thực thi quyết định chấp nhận | `sed -n '1917,2010p' .claude/dev/packet_loop.py`; đối chiếu ba luồng runtime | Khớp: đọc các ADR để kiểm hiện diện/trạng thái, không xử lý probe/fallback. Không kết luận từ grep tên rằng không reader nào đọc file metadata. |

### Ca và đột biến của cả ba lối

| Lối | Ca / dòng test | Đột biến / dòng đăng ký | Kết quả bổ sung base và HEAD |
|---|---|---|---|
| Launcher | `r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra`, launcher_test.py:9154 | `g7_nuot_loi_ghi_trang_thai`, :13393 | Baseline PASS; mutant `TinHieuChotCa`, lỗi ghi bị nuốt. |
| Materializer | `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`, :9069 | `g7_f01_materializer_gop_loi`, :13401 | Baseline PASS; mutant `TinHieuChotCa`, lý do bị gộp. Fixture thay constructor. |
| Credential | `t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra`, codex_cred_test.py:449 | `t16_nuot_loi_ghi`, :570 | Baseline PASS; mutant `AssertionError`, lỗi ghi bị nuốt. Fixture thay constructor. |

`evidence/target-mutants.json` lưu từng baseline/mutant, lỗi và việc có dùng seam constructor. Không có lối nào thiếu lỗi to hoặc thiếu ca/đột biến đích trong phạm vi ba nhánh được xét. ADR dẫn tệp/ca t16; mutation t16 có thật trong mã dù ADR không chép tên nó.

### Ma trận cùng phương pháp lượt 1/2

Kết quả giống nhau trên base và HEAD, ở launcher/materializer/cmd_kiem:

| Lỗi chèn / đối chứng | Helper probe qua hai lượt | State nhớ đúng id sau hai lượt |
|---|---|---|
| Lỗi trước replace state | `[1,1]` | Không |
| Lỗi fsync thư mục sau replace | `[1,0]` | Có |
| State không đọc được sau probe đầu | `[1,0]` | Không |
| Ghi thành công | `[1,0]` | Có |

Ở mọi tổ hợp, auth cũ giữ nguyên và không ghi id credential chưa probe. Hai phản chứng có lượt sau trả chờ snapshot/id đã thất bại, hoặc materializer báo lỗi đọc/ghi state chung. `evidence/{base,head}-probe-repro.json` ghi nguyên kết quả/lý do từng lượt. Đây là lỗi I/O chèn có kiểm soát, không đo mạng, mất điện, Windows hay mọi loại lỗi trên OS thật.

### Đếm đủ sáu vị trí cổng

Đã chạy riêng hai lệnh sau trên từng tệp, cả base và HEAD:

```bash
rg -c 'ADR-0061|0061-codex' <tep>
rg -c 'codex-rejected-state-khong-ghi-duoc|_danh_dau_auth_hong|KHÔNG ghi được trạng thái' <tep>
```

| Tệp | Định danh base/HEAD | Khái niệm base/HEAD |
|---|---|---|
| `ops/lease_publish.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.claude/dev/packet_loop.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.claude/dev/launcher.py` | 0/0, rc=1/1 | 4/4, rc=0/0 |
| `.claude/dev/gate_lifecycle.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.github/workflows/ci.yml` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.github/workflows/ops-publish-lease.yml` | 0/0, rc=1/1 | 0/0, rc=1/1 |

Không khớp nghĩa là stdout rỗng/rc=1, không phải stdout in `0`. Bốn dòng khái niệm ở launcher:3589,3702,3895,3896. Theo §20:1487–1498, “có nhắc” là proxy; đọc consumer metadata và các nhánh runtime riêng mới hỗ trợ kết luận có phạm vi về quyết định chấp nhận. Phần Cưỡng chế và dòng §20 hiện khai đúng mức này.

## Tiền đề spec và handoff

Mục **Sự thật đã đo** của SPEC vẫn nói “Mỗi lần gọi tốn thêm 1 lần probe, và lần nào cũng … cùng lý do”. Ma trận giữ nguyên phương pháp lượt 1 bác tính tuyệt đối ấy. **A1–A5 không yêu cầu mọi lần gọi phải đúng một probe**: A4 yêu cầu các ca dẫn chạy xanh. Vì vậy không yêu cầu ADR giữ lời khai sai để khớp tiền đề, không tự sửa spec đóng băng và không coi đây là thay nghĩa vụ nghiệm thu.

Executor cần ghi lệch tiền đề vào `ops/handoff/wp825-g1-claude.md`, kèm điều kiện state còn đọc được/chưa nhớ id và hai nhánh 0 probe; khai `hint_provenance` cho các hunk đã dùng từ lượt 1/2. Nếu authority muốn đổi nghĩa vụ nghiệm thu thì cần revision đúng protocol. Prompt cho biết handoff chưa có trong bundle; phép `git show` trên ref lease local đã lưu trả rc=128 do thiếu path. **KHÔNG ĐO ĐƯỢC** bản handoff cập nhật hoặc provenance ở ngoài bundle/ref này; không suy thành khẳng định executor chưa ghi ở nơi khác. Đây là lưu ý handoff đã có từ lượt trước, không phải finding mới phản đối quyết định chủ kho.

Câu “Mỗi lượt đi đến nhánh này … một lần” đã có phạm vi nhánh/helper; câu “số lần gọi suy từ luồng mã” không tự nhận số request mạng đã đo. Lời “đã đo” về test có lệnh tái lập; historical pass/thời điểm vẫn được ghi là chưa tái chứng nhận đầy đủ. Nhãn suy luận chưa đo về chỗ lưu dự phòng rõ ràng, không trộn với kết quả fault injection.

## Bảng lớp, finding và artifact

| Lớp lịch sử | Kết quả trên exact HEAD | Finding mở |
|---|---|---|
| `loi-ghi-khong-suy-ra-probe-lap` | Đóng cả thân ADR, §20 và tiêu đề | 0 |
| `grep-ten-khong-do-khai-niem` | Giữ đóng; đo lại đủ sáu vị trí/hai regex/hai cây | 0 |

Không còn finding P0/P1/P2/P3 trong phạm vi rà soát; không có mục `### <slug> [P…]` còn mở. `HINT.patch` để rỗng vì không có thay đổi đề nghị; không áp patch vào checkout.

Chưa đo được: A4 đầy đủ với constructor nguyên trạng ở temp không có ancestor `.git`; full 18 ca/18 mutation ở nền xanh; CI exact-head A5; số HTTP request/retry thật; Windows, mất điện, đầy đĩa/quyền/read-only thực; khả năng chỗ dự phòng sống sót; byte lời duyệt, model/effort phục vụ từng response và handoff cập nhật. Các phần này không được ghi là passed. Cần bằng chứng A4/A5 còn thiếu trước khi tuyên bố đủ điều kiện merge theo lease; verdict này không cấp merge/land authority.
