verdict: approve
reviewed_head: a7da46390177cdc2d64f516dedac19857bee86dd
reviewed_sha: a7da46390177cdc2d64f516dedac19857bee86dd
reviewed_tree: f26533b3a570204ce5d7cbb3fadaa7097ede8d46
review_class: sensitive
provider: openai_codex
model: gpt-6.1-sol
model_family: openai
reasoning_effort: xhigh
execution_surface: codex_cli
transport: machine
review_round: 1/2

## Kết luận

**Approve bản vá trên exact SHA/tree nêu trên.** Không phát hiện finding P0/P1/P2/P3 còn mở do diff gây ra: đúng ba timeout lên 150, hai hằng băm được tính lại đúng hàm, neo đột biến vẫn bắt lỗi, hai snapshot chỉ đổi đúng giá trị được phép. Đã thực hiện năm hướng săn độc lập.

**N4 chưa đạt đầy đủ trong sandbox:** bộ đường nhanh ở cả BASE và HEAD cùng rc 1, `CA: 103/104`, `DOT BIEN: 387/392`, `TONG: DO` vì socket bị chặn; delta BASE/HEAD = 0. Registry gốc cũng bị signer loopback chặn; lượt bổ sung tắt ký riêng commit fixture đạt `1070/1070`, `TỔNG: ĐẠT` ở cả hai. Không chuyển lỗi môi trường thành kết quả xanh. Approval này là kết luận review diff; chưa xác nhận các gate CI/Windows thực hoặc đủ điều kiện merge/land.

## Neo và môi trường

| Cây | Commit đo đầu và cuối | Tree đo đầu và cuối | Trạng thái |
|---|---|---|---|
| HEAD `cay-kho/` | `a7da46390177cdc2d64f516dedac19857bee86dd` | `f26533b3a570204ce5d7cbb3fadaa7097ede8d46` | sạch đầu/cuối |
| BASE `nen/` | `1797c32530fba381afd4009340a3fa558b7e37b0` | `35ca3317ab8b3e9692d1cf17eb59f16ce135189a` | sạch đầu/cuối |

Lệnh neo: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`, tương tự `nen`. Hai `git --no-optional-locks -C <cây> status --porcelain=v1 --untracked-files=all` đầu/cuối đều rc 0, output rỗng. Cuối lượt bổ sung `status --ignored`, diff tracked, diff cached và `diff --check`: đều rc 0, output rỗng. Mỗi cây có 5.500 tệp ngoài `.git`, toàn bộ nội dung và bit executable khớp bản sao nguyên trạng tạo trước test; không có `__pycache__`. Snapshot chứng minh không có delta quan sát được, không chứng minh lịch sử ghi rồi hoàn nguyên. Mọi test/phản chứng chạy trên bản sao hoặc fixture dưới `out/`.

| Spec đã đọc | SHA256 tự đo bằng `sha256sum` | Kết quả |
|---|---|---|
| `evidence/spec-wp910.md` | `2383ca2e540203e0b449e3f6118d84817f81984e937d463e99a7b862449a6613` | khớp prompt, không đổi ở cuối lượt |
| `evidence/spec-wp910-r2.md` | `c3179d006b46fa82fe144cc1200dab72dbd9e88de28159f541504a7831dde7fc` | khớp prompt, không đổi ở cuối lượt |
| `evidence/spec-wp910-r3.md` | `bb015dc66b08f9c559a0eecb1966558030991135bbf1a8004ac7108509a433bc` | khớp prompt, không đổi ở cuối lượt |

- Đã đọc r1+r2+r3 theo quan hệ DELTA, `AGENTS.md` cùng các quy tắc repository liên quan reviewer/CI. Review theo chỉ thị offline trong `prompt.snapshot`; `lease.yaml` chỉ là bản sao, không suy authority live từ đó.
- `git -C kho.git diff --stat 50a59a9 1797c32`: 31 tệp, +18.393 dòng, tất cả `ops/land/**`; không đổi nguồn đang đo so mốc spec r3.
- `git -C kho.git diff --numstat 1797c32 a7da46390177cdc2d64f516dedac19857bee86dd`: đúng 4 tệp, +8/-8; trong giới hạn ≤4 tệp, ≤450 dòng thêm. `ci_dang_ky_test.py` +3/-3; `ci.yml` +2/-2; `ci-dot-bien-du.yml` +1/-1; `ci_duong_nhanh_test.py` +2/-2. Không có handoff/verdict/manifest trong diff.
- Diff thực lưu `out/actual.diff`; numstat trùng byte bản cung cấp. Diff mặc định Git viết tắt OID 8 ký tự, bản cung cấp 7; lệnh `git -c core.abbrev=7 -C kho.git diff 1797c32 a7da46390177cdc2d64f516dedac19857bee86dd` rc 0, trùng byte `evidence/diff.patch`.
- Header CLI `runs/55874d00/stderr.log:2–10`: OpenAI Codex v0.163.0, model `gpt-6.1-sol`, effort `xhigh`. Đây là khai báo CLI, không suy model từ executor/lease hay tài khoản GitHub.
- Môi trường: Linux, Python 3.13.16, PyYAML 6.0.3, actionlint 1.7.7 tại `/root/.local/bin/actionlint`; **shellcheck và pwsh vắng**. Sandbox `workspace-write`, mạng restricted; không gọi GitHub/web/fetch/cài công cụ. Fixture Git ban đầu tự gọi signer qua loopback nhưng bị socket policy chặn; lượt bổ sung tránh signer cho commit fixture tạm.
- `TMPDIR` riêng là `<sandbox>/out/tmp`; Python dùng `-B` và `PYTHONDONTWRITEBYTECODE=1`. Không sửa checkout nguồn, không tạo patch sản phẩm, không merge/land/deploy.
- Bằng chứng lệnh/rc/output đầy đủ: `out/anchors-start.json`, `out/anchors-end.json`, `out/final-checks.log`.

## Bảng finding

| ID | Mức P0–P3 | Tệp:dòng | Bằng chứng | Hướng sửa bằng lời |
|---|---|---|---|---|
| — | — | — | Không có finding do bản vá gây ra sau các phép đo dưới đây | Không yêu cầu sửa sản phẩm |

Số finding mở trong phạm vi bản vá: **P0=0 · P1=0 · P2=0 · P3=0**. Không cấp ID `F910B-NN` cho lỗi môi trường hoặc quan sát đã tồn tại ở BASE. Quan sát Windows t9 và chú thích cũ nằm ở H2/H3; không biến chúng thành yêu cầu ghi ngoài write set. Đây là vòng 1/2, không có finding vòng trước để đối chiếu.

## Bảng N1–N4 và hai hằng băm

| Tiêu chí | Kết quả | Bằng chứng |
|---|---|---|
| N1 | ĐẠT | `ci.yml:882` gate-nhanh-manh 30→150; `ci.yml:962` gate-registry 105→150; `ci-dot-bien-du.yml:24` dot-bien-du 105→150; diff hai workflow chỉ đúng 3 dòng |
| N2 | ĐẠT | 15 tuple timeout mỗi cây, đúng 3 thay đổi; 12 giá trị còn lại giữ nguyên; launcher trùng byte |
| Hai hằng băm | ĐẠT | Hàm HEAD được import từ bản sao, gọi trên YAML HEAD/BASE; khớp 4/4 hằng mới/cũ; xem bảng dưới |
| Phạm vi hai tệp Python | ĐẠT | Đảo đúng hai hằng và literal timeout-trung ⇒ source registry trùng byte BASE; đảo đúng hai timeout KHUNG_JOB ⇒ source fast test trùng byte BASE |
| Răng đột biến | ĐẠT | Neo 150 có đúng 1 lần; khóa timeout trùng bị actionlint bắt; neo vắng làm chính ca p651 đỏ; timeout mutant yml_gate_timeout_1_phut bị giết đúng ca y13 cả hai cây |
| N3 | ĐẠT trong phạm vi actionlint, không có shellcheck | 4/4 lượt rc 0, stdout/stderr rỗng, delta 0; shellcheck vắng |
| N4 registry — lượt gốc | KHÔNG ĐO ĐƯỢC đầy đủ | Cả hai rc 1 ở fixture Git commit, chưa in TỔNG; signer loopback bị chặn |
| N4 registry — bổ sung cấu hình fixture local | ĐẠT trong cấu hình ghi rõ | Cả hai rc 0, PHẢN CHỨNG 1070/1070, TỔNG: ĐẠT; không sửa mã |
| N4 fast | KHÔNG ĐO ĐƯỢC đầy đủ do sandbox; đã chạy hết | Cả hai rc 1, CA 103/104, DOT BIEN 387/392, TONG: DO; cùng ca/năm mutant bị chặn, delta 0 |
| N5 CI/check run/dispatch | KHÔNG ĐO ĐƯỢC | Review offline không có readback exact head. Không khẳng định CI đã chạy/chưa chạy hay xanh; không tự chọn ngoại lệ phút CI thay chủ kho |

### N1/N2: danh sách timeout lấy từ YAML đã parse

Lệnh `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/out/tmp" python3 -B out/audit.py`, rc 0. Dùng PyYAML `safe_load` trên `ci.yml`, `ci-dot-bien-du.yml`, `launcher-windows.yml` của `out/base` và `out/head`, lấy từng timeout cấp job/bước. Khóa `on` được PyYAML đọc thành `True` nhất quán ở cả hai cây; giá trị timeout là số nguyên. Toàn bộ danh sách:

| Tệp | Job | Bước | BASE | HEAD |
|---|---|---|---:|---:|
| .github/workflows/ci-dot-bien-du.yml | dot-bien-du | cấp job | 105 | 150 |
| .github/workflows/ci-dot-bien-du.yml | dot-bien-gop | cấp job | 10 | 10 |
| .github/workflows/ci-dot-bien-du.yml | dot-bien-manh | cấp job | 360 | 360 |
| .github/workflows/ci.yml | chuan-bi | cấp job | 20 | 20 |
| .github/workflows/ci.yml | chuan-bi | step[1]:actions/checkout@v4 | 10 | 10 |
| .github/workflows/ci.yml | chuan-bi | step[2]:phan-loai | 5 | 5 |
| .github/workflows/ci.yml | gate | cấp job | 150 | 150 |
| .github/workflows/ci.yml | gate-cong-cu | cấp job | 150 | 150 |
| .github/workflows/ci.yml | gate-cong-cu-gop | cấp job | 10 | 10 |
| .github/workflows/ci.yml | gate-nhanh-gop | cấp job | 10 | 10 |
| .github/workflows/ci.yml | gate-nhanh-manh | cấp job | 30 | 150 |
| .github/workflows/ci.yml | gate-ops | cấp job | 150 | 150 |
| .github/workflows/ci.yml | gate-packet-loop | cấp job | 150 | 150 |
| .github/workflows/ci.yml | gate-registry | cấp job | 105 | 150 |
| .github/workflows/launcher-windows.yml | launcher | cấp job | 150 | 150 |

Chuẩn hóa đúng ba timeout HEAD về giá trị BASE ⇒ **toàn bộ dữ liệu đã parse của ba workflow bằng BASE**, bao gồm env/defaults/matrix/needs/if/steps/trigger. Kiểm riêng diff thô chỉ ba cặp dòng timeout. Dữ liệu thô: `out/timeouts-base.json`, `out/timeouts-head.json`, `out/timeout-table.md`, `out/audit.json`.

### Hai hằng băm và phạm vi mã Python

`out/audit.py` dùng `importlib.util.spec_from_file_location()` nạp `out/head/.claude/dev/ci_dang_ky_test.py`, gọi `bam_gate_nhanh(yaml.safe_load(ci_yml))` và `bam_gate_registry(...)` trên HEAD và BASE. Hằng đối chứng BASE lấy từ module bản sao BASE. Không tính băm bằng thuật toán thay thế.

| Hằng | YAML BASE: kết quả hàm HEAD = hằng cũ | YAML HEAD: kết quả hàm HEAD = hằng mới |
|---|---|---|
| `BAM_GATE_NHANH` | `301d30a212b34bcff14390a3353084a9af0385fe917c76ab33a22cdc054e2e26` | `fe061a50668af83b6c9b6939f881ba37a30083bc72a27b52c2e02350835d626b` |
| `BAM_GATE_REGISTRY` | `e2726e28ae7ecc869cd9df6c975e58f71c3c656594a509c9c2e4b9047c47bb4d` | `89516cf77c3ce734feadf348bfea8180254c67e8e8ec62a48e2f6ea1dc038452` |

Hai hàm băm không đổi mã. Diff registry chỉ `.claude/dev/ci_dang_ky_test.py:803`, `:805` và tuple mutant `:2297`; diff fast test chỉ timeout của hai job trong `KHUNG_JOB` ở `ops/ci_duong_nhanh_test.py:2306`, `:2308`. Script tự đảo đúng literal được phép rồi so byte toàn tệp, không chỉ dựa numstat.

`timeout-trung`: chuỗi neo nguyên văn `    timeout-minutes: 150\n` có count=1. Bản sao chèn `timeout-minutes: 5` trước 150 vẫn được dict validator chấp nhận (`[]`) vì PyYAML nuốt khóa trùng, nhưng actionlint rc 1:

```text
out/mutations/timeout-duplicate.yml:25:5: key "timeout-minutes" is duplicated in "dot-bien-du" job. previously defined at line:24,col:5 [syntax-check]
```

`python3 -B out/probes.py` rc 0 thực thi nguyên khối `with` chứa năm ca YAML thô từ bản sao test. Neo thật: 5/5 True. Chỉ đổi neo sang 999 không có trong workflow: `p651-M4-yaml-tho-timeout-trung=False`, bốn ca khác vẫn True. Khối đã thực thi lưu trong `out/mutations/*-executed-block.py`; đây là fixture phản chứng, không phải patch sản phẩm.

`python3 -B out/final_checks.py` rc 0 còn gọi harness thật `chay_mot_dot_bien()` cho `yml_gate_timeout_1_phut`: cả BASE/HEAD trả `GIET`, ca đích `y13_khoa_topology_cua_ci_yml_ngoai_than_run`. Harness tự đòi ca gốc xanh, mutant đổi byte và rc/tên ca đúng. Bằng chứng: `out/fast-timeout-mutant.json`.

### N3: actionlint

Ở từng `out/base` và `out/head`, đã chạy `actionlint -no-color .github/workflows/ci.yml` và `actionlint -no-color .github/workflows/ci-dot-bien-du.yml`: **4/4 rc 0**, stdout/stderr rỗng, delta BASE/HEAD = 0. Phiên bản 1.7.7 (go1.23.4, linux/amd64). **shellcheck không có trên PATH**, nên actionlint không cung cấp bằng chứng kiểm shellcheck. Không cài qua mạng. Toàn bộ lệnh/output: `out/actionlint.json`.

### N4: lượt chạy gốc và lượt bổ sung, không trộn trạng thái

`python3 -B out/run_n4.py <head|base>` lần lượt chạy đúng hai lệnh dưới đây từ bản sao tương ứng, với `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR=<sandbox>/out/tmp`, `PYTHONUNBUFFERED=1`, `GIT_OPTIONAL_LOCKS=0`:

```text
python3 -B .claude/dev/ci_dang_ky_test.py
python3 -B ops/ci_duong_nhanh_test.py
```

Không truyền `--chay` cho lượt gọi chính. Bộ registry có một phản chứng nội bộ sẵn có gọi `--chay` với env cố ý sai để đòi dừng trước khi chạy bộ test; mã test giữ nguyên.

| Lượt | BASE | HEAD | Delta/kết luận |
|---|---|---|---|
| Registry gốc | rc 1, 7.388 s; ĐĂNG KÝ 24/24, launcher 4/4, Ruff contract 3/3, rồi Git commit fixture rc 128; chưa có TỔNG | rc 1, 7.357 s; cùng output/điểm lỗi | delta lỗi = 0; KHÔNG ĐO ĐƯỢC đầy đủ |
| Fast gốc | rc 1, 214.017 s | rc 1, 215.693 s | cùng tổng và tập lỗi; KHÔNG ĐO ĐƯỢC đầy đủ |
| Registry bổ sung fixture local | rc 0, 8.242 s; PHẢN CHỨNG 1070/1070, TỔNG: ĐẠT | rc 0, 8.394 s; cùng tổng | delta 0; ĐẠT với cấu hình fixture dưới đây |

Nguyên nhân registry gốc: cấu hình global `commit.gpgsign=true` khiến Git fixture tại dòng 2127 gọi signer; signer không mở được socket loopback, `fatal: failed to write commit object`. Đã lưu rc/stderr chẩn đoán trong `out/git-fixture-diagnosis.json`. Lượt bổ sung `python3 -B out/run_registry_local.py head` / `... base` chỉ nối **`commit.gpgsign=false` qua `GIT_CONFIG_COUNT` theo tiến trình** để commit fixture giả được tạo cục bộ; giữ các thiết lập kế thừa khác, không sửa config toàn cục/checkout hay mã test. Output bổ sung cả hai có `ĐĂNG KÝ: 24/24`, `LAUNCHER WINDOWS: 4/4 hợp đồng`, `RUFF CI: 3/3 hợp đồng`, `PHẢN CHỨNG: 1070/1070 đỏ đúng`, `TỔNG: ĐẠT`. Ruff ở đây là contract test, không khai bare lint đã chạy.

Output fast nguyên văn **trên cả hai cây**:

```text
[HONG] t20zo_la_khong_phai_tep_thuong_do: PermissionError: [Errno 1] Operation not permitted
CA: 103/104 dat · 0 do · 1 hong
DOT BIEN: 387/392 bi giet dung ly do
TU KIEM PHAN HANG: DAT (5 mau rc, 3 dot bien that)
TONG: DO
```

Năm mutant không được cấp tín dụng giết: `symlink_treo_khong_theo_bi_danh`, `la_bo_chot_tep_thuong`, `la_cho_phep_fifo`, `la_cho_phep_socket`, `la_khong_theo_symlink`. Tất cả ghi `HONG ca dich t20zo_la_khong_phai_tep_thuong_do khong xanh tren ban goc (rc=4)`; stack dừng tại `ops/ci_duong_nhanh_test.py:1702`, `s.bind(ten)`, `PermissionError: [Errno 1] Operation not permitted`.

Tập ca lỗi, tập mutant lỗi và các dòng tổng BASE/HEAD bằng nhau; **toàn bộ log fast trùng byte sau khi thay duy nhất đường dẫn `out/base`/`out/head` thành cùng marker**. Không giả lập socket để tuyên bố xanh, không bỏ ca hoặc sửa harness. 387 mutant còn lại gồm mutant timeout đã được kiểm riêng ở trên. Các warning legacy schema/SyntaxWarning cũng có ở cả hai log.

Lệnh/rc/thời gian/env: `out/n4-base.json`, `out/n4-head.json`, `out/n4-*-registry-local.json`. Log đầy đủ: `out/n4-{base,head}-{registry,fast}.log`, `out/n4-{base,head}-registry-local.log`. N4 đầy đủ vẫn cần môi trường cho phép socket; N5 và Windows native cần readback/runner tương ứng, trạng thái hiện tại **KHÔNG ĐO ĐƯỢC**.

## Các hướng săn

| Hướng | Giả thuyết | Lệnh / phép đo đã chạy | Output thật | Kết luận |
|---|---|---|---|---|
| H1: trần bộ so với job | Trần 5400 hoặc runtime truyền timeout không còn hợp lệ khi đổi job | `python3 -B out/audit.py`; `python3 -B out/probes.py`, nguyên ca `p643-tran-bo-nho-hon-timeout-job` tại `.claude/dev/ci_dang_ky_test.py:2348` | BASE `5400 < 6300=True`; HEAD `5400 < 9000=True`; ca gốc cả hai True. Phản chứng job 90 phút làm ca False. Runtime Mock xác nhận `communicate(timeout=5400)`. | KHÔNG PHẢI LỖI |
| H2: consumer khác, gồm Windows/master | Test/công cụ ngoài write set còn ghim 30/105, làm phát sinh hồi quy | `rg` trên mọi mã `.py/.ps1/.yml/.yaml/.sh/.cmd/.bat/.js/.ts` kể cả tệp ẩn, loại artifact lịch sử; `python3 -B out/probes.py`; đọc `.claude/dev/chay-cong-windows_test.ps1:388` và wrapper `:102` | 113 dòng consumer (`out/search-code-consumers.log`), 29 dòng nghi ghim (`out/search-pinned-timeouts.log`). `HanGiay=6300`, `max(gate*.timeout)=150`, phép t9 `6300 >= 9000=False` TRÊN CẢ BASE VÀ HEAD. Không tìm thấy ghim khác gây hồi quy mới ngoài hai snapshot/hai hằng đã đổi. | KHÔNG PHẢI LỖI của diff; nợ BASE. Chạy PowerShell/Windows native: KHÔNG ĐO ĐƯỢC (`pwsh` vắng). |
| H3: chú thích cũ | Tăng timeout làm chú thích nói 30/105 sai hiện trạng | `rg -n '30 phut\|nay 105\|105 vẫn\|vẫn 60' cay-kho/.claude/dev/ci_dang_ky_test.py cay-kho/.github/workflows/ci.yml`; so byte BASE/HEAD trong `out/audit.py` | `.claude/dev/ci_dang_ky_test.py:804` còn “trần 30 phút”, `:755` còn “nay 105”; `ci.yml:953` còn “105 vẫn cỡ theo UBUNTU”, `:954` còn `gate`/`gate-packet-loop` “vẫn 60” (câu cuối đã sai ở BASE). Các dòng comment đều không đổi. | KHÔNG PHẢI LỖI cần vá trong write set: chỉ ghi nhận theo prompt/spec; không yêu cầu nới diff sửa comment. |
| H4: băm bao workflow | Recompute hằng có thể che việc thay env/defaults hoặc phần job khác | `python3 -B out/audit.py`, import module bản sao; chuẩn hóa đúng ba timeout của HEAD; thử thay riêng workflow `env`, rồi `defaults` trên dict tạm | Toàn bộ YAML HEAD sau chuẩn hóa bằng BASE. Thử env/defaults đều `hash_changes=True` và validator trả lỗi `gate-registry đổi (băm ...)`; hai hàm băm không đổi mã. | KHÔNG PHẢI LỖI |
| H5: đột biến timeout mất răng | Neo 150 sai/no-op hoặc test vẫn nhận xanh khi neo vắng | `python3 -B out/audit.py`; `python3 -B out/probes.py`, thực thi nguyên khối test YAML thô từ bản sao | Neo 150 có 1 lần; bản đột biến đổi byte; validator dict vẫn `[]`, actionlint rc 1 báo khóa trùng. Ca thật `p651-M4-yaml-tho-timeout-trung=True`; đổi riêng neo 999 ⇒ False, bốn ca khác True. | KHÔNG PHẢI LỖI |

H2 là phép đối chiếu điều kiện của t9, không khai đã chạy PowerShell. Tất cả hằng/consumer khác chỉ được kết luận trong phạm vi mã tracked được cung cấp, không suy kết quả CI/Windows thực.

Lệnh tìm consumer đã chạy (rc 0):

```bash
rg -n --hidden -g '*.py' -g '*.ps1' -g '*.yml' -g '*.yaml' \
  -g '*.sh' -g '*.cmd' -g '*.bat' -g '*.js' -g '*.ts' \
  -g '!**/.git/**' -g '!**/ops/land/**' -g '!**/ops/leases/**' \
  -g '!**/ops/reviews/**' -g '!**/ops/specs/**' -g '!**/ops/handoff/**' \
  'gate-nhanh-manh|gate-registry|dot-bien-du|BAM_GATE_NHANH|BAM_GATE_REGISTRY|GIAY_TOI_DA_MOT_BO' \
  cay-kho > out/search-code-consumers.log
```

Đối với H4, dict tạm thêm riêng workflow `env` ⇒ hash `38b62663cb8858fc2124d9240b91ad58c5e14b41a22933ec8e7df064a679be07`, thêm riêng `defaults` ⇒ `bff30cbb1ab2d97bfe3c615ac911b47b6223a352a1e71ae8e51409f75924032e`; cả hai khác hằng mới và validator trả lỗi. Đây là phép thử hành vi phạm vi băm, ngoài phép so cấu trúc BASE/HEAD.

## Chốt bằng chứng cuối lượt

`PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/out/tmp" python3 -B out/final_checks.py` rc 0. Exact commit/tree và SHA256 spec giữ nguyên; cả hai checkout nguồn sạch, kể cả ignored/index, không có bytecode. Kiểm 5.500 tệp mỗi cây với bản sao tạo đầu lượt: không có delta. Hai suite đã kết thúc; không để kết quả đang chạy làm bằng chứng pass.

`VERDICT.md` được tạo với `pending` trước test, cập nhật sau các bước neo/N1–N2/băm/N3/phản chứng/N4, rồi chốt `approve` trong phạm vi review diff với các giới hạn đo đã nêu. Không có live authority hoặc bằng chứng CI xanh được suy ra từ review này.

Thời điểm chốt (UTC): 2026-10-25T01:45:31+00:00
