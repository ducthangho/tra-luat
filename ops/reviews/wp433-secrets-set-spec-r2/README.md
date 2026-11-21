# Bằng chứng §0b — SECRETS-SET-BUNDLE-KIEU r2

Đo ngày 2026-11-21, khoảng 07:28–07:35Z, trên Linux, Python 3.13.18. Một lệnh dựng hai clone đầy đủ (không shallow) dưới `/dev/shm`, đặt `core.abbrev 7`. Mỗi vế dùng `HOME`/`TMPDIR` tạm riêng.

- **nen:** origin/master `1e397c89d69f451694a2252103ea97ec274ab43f`, tree `b1b95b50…`.
- **sau:** nen áp hai tệp ghim từ `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c` (`scripts/tl_gws.py`, `scripts/test_fragments/wp433_secrets_set_bundle.py`). Sau đó tái sinh bundled bằng `write_bundled_modules(scripts/test_fragments, scripts)` và manifest bằng `tl.py release-manifest --out RELEASE_MANIFEST.json`. Kết quả commit cục bộ `0a3f3edc94fcc5c299c8ade80e7e8dfcf04c9a34`, tree `8d23a5eabc6c0d419298a249a84c133bdc9afff2`.

| tệp | nội dung |
|---|---|
| `nguyen-mau-tl_gws.diff` | diff `tl_gws.py` nen→sau (M1 + M2, +5/−1) |
| `numstat.txt` | numstat nen→sau, 4 tệp +211/−8 |
| `{nen,sau}.selftest.tail.txt` | dòng cuối selftest: 1785/1785 và 1786/1786, cả hai rc 0 |
| `{nen,sau}.tfc.json` | `test-fragments-check --json` |
| `{nen,sau}.bfc.json` | `.github/checks/bundle_fragment_check.py --json` (19 và 20 ca) |
| `{nen,sau}.rv.json` | `release-verify RELEASE_MANIFEST.json --strict --json`, 186 == 186 |
| `{nen,sau}.wa.json` | `workflow-audit --strict --json` |
| `{nen,sau}.golden.json` | `golden-test --json` |

Ruff F trên 4 tệp `scripts/` cho 0 lỗi ở cả hai vế. `doctrine-scan` rc 0 ở cả hai vế. `eol_policy_test` đạt 32/32 ở cả hai vế. Ruff F trên fragment: All checks passed.

`tl_gws.py` trên nen có cùng blob với `0f9aa2a` (`fbeb9421`), nên bằng chứng hành vi của r1 ở `../wp433-secrets-set-spec-r1/` vẫn đúng.
