# HANDOFF — `LEASE-DANG-WINDOWS` (#238), Executor lượt 4 (`codex`)

- Provider `openai_codex`; execution surface Codex workspace service; transport machine; role Executor.
- Bản vá nguyên vẹn: `73/73 đạt; đã chạy=73, bỏ qua=0`; `rc=0`.
- Bản vá + X1: `64/65 đạt; đã chạy=65, bỏ qua=8`; `rc=1`; ca đỏ thật: `t73_nen_posix_khong_duoc_bo_qua_ca_nao`.
- X1 không kèm bản vá: `64/64 đạt; đã chạy=64, bỏ qua=8`; `rc=0` (XANH, tái hiện đúng lỗ).
- `git diff --numstat ba82b06f..HEAD` trên write-set: `2 4 .github/workflows/ops-publish-lease.yml`; `122 16 ops/lease_publish_test.py`; tổng 2 tệp, `+124/-20`, dư 1/125 dòng thêm.
- Cổng kế thừa: suite với ba biến GitHub và `gh` vắng vẫn `73/73`; actionlint 1.7.7 với ShellCheck 0.9.0 có mặt `rc=0`; M1–M4/A5/D3/D4 và 8 guard giết `15/15`; P1-1/P1-2/P1-2(b), W6′/W7′/W8/W9 đều đỏ.
- `chua_do_duoc`: W3′ và hành vi P1-3 trên `windows-latest` thật ở exact head mới; ShellCheck có/vắng trên runner Windows; nguyên nhân gốc tám ca/t49 và argv t49 thật; `gh` thật.
