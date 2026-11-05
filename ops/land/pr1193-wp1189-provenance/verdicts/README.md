# Bàn giao biên nhận review offline — WP #1189 LEASE-PUBLISH-GHIM-PYTHON r1 g1

Executor `session_015GtxrauwJ84GSjQMdV2Gqn` bàn giao cho phiên ghi hồ sơ `ops/land/pr1193-wp1189-*`.
Bốn lượt Codex offline (launcher `run`), đều `approve`:

| lượt | reviewed_sha | launcher run |
|---|---|---|
| r1 | 3ca0da3b94a3078199ca8712bc26aa3b04009226 | b7531bef |
| r2 | d5d3c8ffc021db8a99c366c7520b4f063cd27ab8 | 9ec06d66 |
| r3 | 3b430923c88f67041ce79ce9b2f8aac0e53a28b4 | 51d21cd5 |
| r4 | 275869169e134758bb145565d28f0b0897a92f87 | 0c0787b3 |

Mỗi `rN/` là thư mục sandbox của lượt đó (PROMPT.md, VERDICT.md, SPEC.md, a1_check.py, patch, review-evidence/).
`rN/run-<id>/` chép nguyên `run.json`, `prompt.snapshot`, `stdout.log`, `stderr.log`, `checkpoint.json` của launcher.
Không chép: clone kho (`cay-kho/`, `review-evidence/base-repo/`) và tệp > 1 MiB; tệp > 1 MiB có sha256 + cỡ trong `OMITTED.txt`.
Quét `scripts/pkg_secret_scan.py` rc=0 (phản chứng: bơm khoá giả vào bản sao ⇒ rc=1). Băm từng tệp ở `SHA256SUMS`.
