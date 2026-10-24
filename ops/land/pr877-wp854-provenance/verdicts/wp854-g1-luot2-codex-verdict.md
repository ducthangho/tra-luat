verdict: approve
reviewed_sha: b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb
reviewed_tree: 375e869086e98b8e782238eaf73def5cb9734ce4
base_sha: 4581cfa5124ef803bfda10ce4de499b0ed31380e
previous_reviewed_sha: 88dc1a92d8af8ec7072897921ef3960250d3a660

**Không còn P0/P1/P2 được phát hiện; cả hai finding lượt 1 đã đóng theo phép đo dưới đây.** N5 Windows thật **KHÔNG ĐO ĐƯỢC**, tách khỏi verdict mã. P3 bằng uid khác cũng **KHÔNG ĐO ĐƯỢC**; phép đo thực bổ sung dùng uid0 không có DAC override đã tái hiện và xác nhận sửa lỗi.

Review độc lập trên bản sao tạm lấy từ Git archive; không sửa checkout `cay-kho/`. Báo cáo được tạo với `verdict: pending` trước phép đo và cập nhật tăng dần; chốt sau khi cả ma trận và kiểm tra cuối hoàn tất.

Provider: OpenAI/Codex, model_family=openai; công cụ shell Linux trong phiên agent (`codex_service`, transport=machine). Không tự xác nhận served-model, launcher attestation, GitHub submitter hoặc cấp receipt/assurance. Review theo hai trục spec và standards/security, lớp sensitive; không merge, push, deploy hoặc gọi LIVE.

## ĐỐI CHIẾU LƯỢT TRƯỚC

### child-temp-env-escapes-suite-root  [P2] — ĐÃ VÁ THẬT / đã đóng

Đo lại đúng lớp lỗi của lượt 1: previous `88dc1a9` và head `b952c10` cùng rc=0, CA45/45, DOT BIEN25/25, 37 GIẾT (25 product + 11 test + 1 settings), 0 sống. Previous còn **8 mục ngoài gốc** ở `/tmp/wp854-r2-direct-previous-aff9sayq`:

```text
tl-subagent-snap/
tl-subagent-snap/a11.json
tl-subagent-snap/a11b.json
tl-subagent-snap/a18.json
tl-subagent-snap/a23.json
tl-subagent-snap/a24.json
tl-subagent-snap/a6.json
tl-subagent-snap/a9.json
```

Head có `outside=/tmp/wp854-r2-direct-head-gfypy3fl`, `remaining=[]`, `remaining_count=0`; cả hai gốc riêng `tl329-bo-*` đã mất. Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/direct.py`; mỗi suite chạy trực tiếp, đầy đủ, TMPDIR/TEMP/TMP cùng trỏ một thư mục rỗng riêng. Raw `direct-{previous,head}.log`, JSON tương ứng, `direct-summary.log` trong `review-evidence/`; harness rc=0.

### cleanup-callback-assumes-unary  [P3] — ĐÃ VÁ THẬT trong phép đo không có DAC override

**Đã đóng ở phép đo directory0500 dưới uid hiện tại KHÔNG có DAC override** (`CapEff=CapPrm=CapBnd=0`):

```text
PYTHONDONTWRITEBYTECODE=1 python3 -I <temp>/native_permission.py <temp>
IDENTITY 0 ['CapEff:\\t0000000000000000'] PYTHON 3.13.16
previous: TypeError: open() missing required argument 'flags' (pos 2); exists=True; mode=0o200
head: PermissionError [Errno 13] Permission denied: PosixPath('/tmp/wp854-r2-dir0500-4f67mtml');
      filename=/tmp/wp854-r2-dir0500-4f67mtml; exists=True; mode=0o500
```

Raw: `review-evidence/native-no-dac.log`. Tệp probe đọc được (0644), archive cha 0755. Đổi sang uid khác: **KHÔNG ĐO ĐƯỢC** (runuser/setpriv bị sandbox chặn); không gán phép đo này cho `nobody`. Lượt probe đầu lỗi JSON serialize PosixPath khi in head, đã sửa riêng harness, đo lại cả hai và giữ log đầu.

## BẢNG ĐO

| Phép đo | Output / kết luận |
|---|---|
| Preflight | HEAD `b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb`; tree `375e869086e98b8e782238eaf73def5cb9734ce4`; worktree sạch. |
| SPEC / write set | SHA256 `30f079b73a42e39f8dd3a537e6dfa9ca9ad07205ea52b42894f948e30123a434` khớp lease; diff base/head đúng một tệp `.claude/hooks/subagent_ghi_detect_test.py`, `69 + / 1 -`. |
| Runtime | Linux uid=0; `runuser` có; Python 3.11.17 / 3.12.3 / 3.13.16; Ruff 0.17.1. |
| Ruff F base/head | `python3 -m ruff check --no-cache --select F <archive>/.claude/hooks/subagent_ghi_detect_test.py` ⇒ cả hai rc=0, `All checks passed!`, delta=0 (`review-evidence/ruff.log`). |
| P3 với uid khác | `runuser -u nobody` ⇒ `cannot set groups: Operation not permitted`; `setpriv --reuid=65534 --regid=65534 --keep-groups` ⇒ `setresuid failed: Invalid argument`. **KHÔNG ĐO ĐƯỢC** bằng uid khác; phép đo bổ sung uid0/CapEff0 đã ghi ở trên. |
| Khôi phục env / ngoại lệ | `probes.py environment <head>` rc=0: 54 tổ hợp (`3^3 × 2`: vắng/rỗng/đường Unicode riêng cho mỗi biến × return/raise); env trả đúng, child Python dùng gốc riêng, RuntimeError giữ identity, gốc đã dọn. |
| Callback Python 3.13.16 / 3.12.3 / 3.11.17 | `probes.py callbacks` rc=0 từng bản: tệp thật 0444 dưới sim được xoá; lần lượt `onexc` / `onexc` / `onerror`. `open`, `scandir`, unlink EIO, rmdir EBUSY đều giữ cùng object ngoại lệ/errno/filename sau 3 lần, 0 chmod. |
| Kênh exec / settings | `probes.py channels <head>` rc=0; 11 neo đều=1; 11 test mutant + 1 settings mutant GIẾT; survivors=[]; env active không đổi, env ngoài trả đúng, outside_entries=[]. |
| N4 AST / bảng | 71 hàm cũ không đổi; 45 ca, 25 product, 11 test, 1 settings giữ nguyên so base. |
| P2 trực tiếp previous/head đầy đủ | Cả hai rc=0, CA45/45, DOT BIEN25/25, DAT; 37 GIẾT, survivors=[]; ngoài gốc **8→0**. |
| Base sim nhẹ | `rc=0`, `loi_ha_tang='dọn thư mục tạm thất bại: /tmp/bo-0nu0hah5 còn'`, CA45/45, `DOT BIEN 25 muc CHE DO NHE`, DAT; harness rc=0. |
| Base sim đầy đủ | `rc=0`, `loi_ha_tang='dọn thư mục tạm thất bại: /tmp/bo-wig32gbp còn'`, CA45/45, DOT BIEN25/25, DAT; harness rc=0. |
| Head sim nhẹ | `rc=0`, `loi_ha_tang=None`, CA45/45, `DOT BIEN 25 muc CHE DO NHE`, DAT; harness rc=0. |
| Head sim đầy đủ | `rc=0`, `loi_ha_tang=None`, CA45/45, DOT BIEN25/25, DAT; harness rc=0. |
| Head thường đầy đủ qua registry | `rc=0`, `loi_ha_tang=None`, CA45/45, DOT BIEN25/25, DAT; harness rc=0; toàn lệnh ma trận rc=0. |
| P3 bổ sung Python cũ | Python 3.11.17 / 3.12.3, cùng uid0 CapEff0: cả previous và head trả PermissionError trỏ `.../file`, directory giữ0500; không gán TypeError của 3.13 cho các bản Python này. `native-other-python.log`, rc=0 từng bản. |

Ma trận N3 chạy trong **một lệnh**: `bash review-evidence/matrix.sh > review-evidence/matrix.log 2>&1`, script export `PYTHONDONTWRITEBYTECODE=1` rồi gọi nguyên `python3 -I sim/chay.py` cho cả base/head, nhẹ/đầy đủ, sim/thường. Sim được cài ở cha và con theo harness đã cấp; không sửa registry. `rc` in bởi harness là mã suite con; `HARNESS_EXIT=0` tự nó không chứng minh pass vì `sim/chay.py` chỉ in kết quả. Base có `loi_ha_tang` là **ĐỎ như mong đợi**, dù ca và mutation xanh. Head phải có cả rc=0 lẫn infra=None cùng các điểm dương.

Thiết lập archive đầu bị lỗi vì Git kế thừa `commit.gpgsign=true`, signer cố gọi dịch vụ cục bộ và bị sandbox chặn; đây không phải lỗi PR. Log giữ ở `review-evidence/setup-initial-failed.log`. Lần dựng lại tắt signing/hook cho commit fixture cục bộ; không dùng remote. Archive cần Git HEAD để ca t21 có Git top-level; commit fixture không đại diện reviewed SHA.

## BẢNG SĂN

Ba hướng mới dưới đây nhắm phạm vi env toàn cục và phân loại callback của commit sửa, ngoài các lượt A/B bắt buộc. Lệnh chung đặt `TASK_TMP=$(cat review-evidence/temp-root.txt)`; mỗi lệnh dùng `PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/probes.py <action> "$TASK_TMP/head"`. Output thật ở `review-evidence/hunts.log`, harness mỗi hướng rc=0.

| Giả thuyết / hướng | Lệnh (`<action>`) và output thật | Kết luận |
|---|---|---|
| 1. Inner wrapper ném lỗi có thể khôi phục nhầm env của outer, làm child kế tiếp thoát gốc | `nested`: `HUNT_NESTED {"trace": ["inner exception preserved", "outer child still uses outer root"], "nested": true, "roots_removed": true, "env_restored": true}`. Có child Python thật ở cả inner/outer; gốc inner là con của outer. | KHÔNG PHẢI LỖI |
| 2. Khôi phục env trước cleanup có thể làm mất trạng thái khi cleanup và body cùng hỏng, hoặc biến lỗi dọn thành xanh | `cleanup_failure`: `body_rc=0, observed_rc=1`; `body_rc=7, observed_rc=7`; cả hai in `TONG: DO — don goc tam cua bo that bai: PermissionError: [Errno 13] persistent cleanup sentinel: 'held-file'`. `HUNT_DUAL_FAILURE {"same_body_exception": true, "env_restored": true, "cleanup_attempted": 3}`. Probe xác nhận env phục hồi trước mỗi lần cleanup. | KHÔNG PHẢI LỖI |
| 3. Filter callable mới có thể chặn retry unlink hợp lệ hoặc nuốt lỗi chia sẻ bền | `transient`: `failures=1, unlink_attempts=2, chmod_calls=1, removed=true`; `failures=99, unlink_attempts=6, chmod_calls=3, removed=false, same_exception=true`. Inject vào unlink thật của rmtree; lỗi bền cuối vẫn cùng PermissionError và cây còn, lỗi nhất thời xoá được. | KHÔNG PHẢI LỖI |

N5 Windows thật: KHÔNG ĐO ĐƯỢC trong phiên offline; tách khỏi verdict mã.

## RĂNG CỦA COMMIT SỬA

`PYTHONDONTWRITEBYTECODE=1 python3 -I review-evidence/teeth.py` ⇒ rc=0, `ALL_THREE_KILLED /tmp/wp854-r2-teeth.oaTLTb`.
Mỗi mutant được dựng riêng bằng `mktemp -d` + `git -C cay-kho archive b952c106ba6bbf94699bda5fe5fb2f6d7f7256fb`; sửa đúng một neo trong bản sao. Mỗi phép đo có head nguyên làm control xanh. Raw: `review-evidence/teeth.log`.

| Gỡ riêng phần sửa | Control xanh | Mutant đỏ | Kết luận |
|---|---|---|---|
| Bỏ dòng đặt env | m9 hook thật + ca t6 trong wrapper: rc=0, outside=[] | rc=0, ca vẫn đúng `unknown`, outside=`[tl-subagent-snap, tl-subagent-snap/a6.json]`, measurement_pass=false | GIẾT bởi đo thoát gốc; không giả vờ suite rc đỏ |
| Bỏ khôi phục env | `{TMPDIR: absent, TEMP: '', TMP: /tmp/old-distinct-sentinel}` được trả đúng | Ba biến cùng còn trỏ `/tmp/tl329-bo-55l0u67o` đã bị xoá; measurement_pass=false | GIẾT bởi đo trạng thái env |
| Bỏ điều kiện lọc callback | Cùng object PermissionError, filename đúng, 0 chmod | TypeError `open() missing required argument 'flags' (pos 2)`; chmod `/fixture/protected-dir`→0200; measurement_pass=false | GIẾT bởi đo giữ nguyên lỗi |

Không mutant nào sống. Harness rc=0 nghĩa là cả ba phản chứng đã bắt được mutant, không phải mutant đạt.

## FINDINGS MỚI VÀ KIỂM TRA CUỐI

Không phát hiện finding mới có phép đo; hai lớp finding trước là **ĐÃ VÁ THẬT**, không đổi slug để xoá lịch sử. Các phép đo env/exec/callback, ba hướng săn và ba mutant gỡ bản sửa không cho thấy bản sửa mở lỗi mới trong phạm vi đã đo.

Kiểm tra cuối sau mọi lượt chạy (`review-evidence/final-checks.json`): worktree `cay-kho/` sạch; HEAD/tree vẫn đúng hai OID ở đầu báo cáo; `git diff --check <base> <head>` rc=0. Diff thật khớp byte `diff.patch`/`numstat.txt`, chỉ `.claude/hooks/subagent_ghi_detect_test.py` (`69/1`). Cả năm lượt ma trận có positive evidence đúng; 2 base lỗi infra như mong đợi, 3 head không lỗi infra. Không đổi source checkout, registry, product hook, ca/assertion hoặc bảng mutant.

## GIỚI HẠN NGHIỆM THU

- **N5 Windows thật: KHÔNG ĐO ĐƯỢC.** Không đọc log GitHub trong phiên offline. Executor phải đo riêng bằng log `gate-registry (windows-latest)` trên exact head; Linux sim không thay thế N5. Không dùng phần chưa đo này để đổi verdict mã theo chỉ thị review.
- **Uid khác / nobody: KHÔNG ĐO ĐƯỢC.** Có phép đo bổ sung thực trên directory0500 bằng uid0 không có DAC override và các callback thật của cả hai API; không khai đã chạy bằng nobody.
- Không đo Windows ACL/share flags/junction/long-path bằng sim readonly; không chạy gate toàn kho, release hay LIVE ngoài packet. Các phép tiêm lỗi bền chỉ kiểm hành vi báo lỗi của helper.
- Hai lỗi thiết lập harness đã được giữ nguyên trong raw log: Git signing fixture bị sandbox chặn và JSON serialize PosixPath. Các phép đo hợp lệ chạy lại sau khi sửa riêng harness; không sửa nguồn PR để chữa rig.
