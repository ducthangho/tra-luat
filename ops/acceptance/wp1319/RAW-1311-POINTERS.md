# WP1319 — Con trỏ gói raw cuối 13/11 (tìm thấy 18/11)

Đọc ngày 2026-11-18, khoảng 04:30–04:45Z, từ phiên điều phối `session_015GtxrapMSm976JLC7Fp1HM`, qua Desktop Commander trên ASUS `7404cfba`.
Lúc đọc máy vừa online lại. `D:\tl-win\KHOA.txt` rỗng. Có tiến trình Codex của phiên khác đang chạy; phiên này không đụng tới.
Phiên này **chỉ đọc**: liệt kê, băm bằng `certutil -hashfile` và đọc entry zip qua `System.IO.Compression`. Không giải nén ra đĩa, không ghi tệp, không chạy test.
Dữ liệu vẫn **ở trên ASUS** và không được tải lên kho công khai. Tệp này chỉ ghi con trỏ và băm.

## Vị trí và băm (sha256)
Gốc chung: `C:\Users\admin\tl-work\`.

| Tệp | Byte | sha256 | Tự khai trong |
|---|---|---|---|
| `wp1298-ASUS-activation-20261112\recovery-native-acceptance-20261113.zip` (P4, 42 entry) | 891 471 | `97e9b78f62a3bd73c3a2550309e44e2e25a956367f2d7b3d9cf83de781a3d8dc` | `recovery-native-export-20261113.json` (`archive_sha256` khớp) |
| `wp1298-ASUS-activation-20261112\recovery-native-export-20261113.json` | 336 | `7c2cafd4f7c08aacf9ffbbb3c75ff1fdf2f4adc3e6ba1055c8ac16983aebe493` | |
| `wp1298-ASUS-activation-20261112\runtime-after-verification-20261113.json` | 805 | `d25f0353cc204cca9a9f2244eaa01b0675d08ad80ea769c2c58fd1adb9d898de` | |
| `wp1298-ASUS-activation-20261112\expected-updater-251-20261113.json` | 29 174 | `e6c9ab004c9a71dd05698a4dae4b28b6e77b89437abed8f89b7f220aaf9ea05c` | |
| `wp1298-ASUS-activation-20261112\P3-evidence-export-20261113.b64` | 206 804 | `93bab58edc6d7f52d204639bced1bd96a821a3049c10d09eb1d281aa27ac09c2` | |
| `wp1298-ASUS-activation-20261112\Proxima-Setup-5.5.0.exe` (bộ cài chính thức, dùng để unpack NSIS) | 161 754 969 | `959c14c1ba489deb53bdaa34e83939fb18f9d7ade58a48a03d361ad1dd12ebf8` | |
| `mission1238-asus-20261112-P3\ASUS-native-canary-evidence.zip` (P3, 118 entry) | 155 062 | `147714ade0daaac048e51445ef5e9775e9f44008d906a093060a953b643eceff` | `evidence-export.json` (`sha256` khớp, `source_M` = `b0b5480`) |
| `mission1238-asus-20261112-P3\evidence-manifest.json` | 19 154 | `35cc813cf575652dc82462059291d8d0450eba0f4f3a8e0c88fcab8e2a8eeee7` | |
| `mission1238-asus-20261112-P3\native-canary-result.json` | 4 849 | `3a4b91b4cf1104a820004a5a8b0d041d71f23087a18da5b2f069be125c40f420` | |
| `mission1238-asus-20261112-P3\G1-handoff-result.json` | 7 524 | `05814804e9aea3f330bba85c95bbc7aca688c1c6669765f59aeff7040212ef30` | |

Thư mục raw đầy đủ, chưa băm từng tệp:
- `wp1298-ASUS-activation-20261112\` gồm khoảng 121 nghìn tệp, 3,8 GB. Bên trong có `recovery-normal-r2\`, `recovery-induced-failure-r2\`, `recovery-upload-20261113\` (mã operator và `source-manifest.json`), `approved-rerun-20261112\`, `post-review-hardening\`, `baseline\`, `repaired\`, `official\`, `closed-profile-backup\` và `profile\`. Hai thư mục cuối là profile thử; **không đọc**.
- `mission1238-asus-20261112-P3\` gồm khoảng 14,5 nghìn tệp, 1,5 GB.

## Đọc thẳng từ entry trong zip P4 (chưa phải review)
- `recovery-normal-r2/activation-result.json` ghi `passed: true`. Các lượt chạy:
  - baseline 45 s;
  - `repaired-soak` có `actual_soak_seconds` 1800,0, `health_samples` 180, `totalRequests` 0, `totalErrors` 0, `graceful_exit`, `forced_cleanup: false`;
  - rollback-restart.

  Phạm vi tự ghi: *"fresh all-registered-data rollback plus full uninterrupted30min soak; R1 invalid observation gap preserved"*.
- `recovery-induced-failure-r2/activation-result.json` ghi `passed: false`, tức FAIL của controller được giữ nguyên.
- `induced-fixture-result.json` ghi `passed: true`, `controller_expected_verdict: FAIL`, `injected_failures` 1, `restore_calls` 1, `baseline_restart_calls` 1, `profile_files_restored` 7957, `source_after_run_equal: true`.
- `source-after-run.json`: `all_equal: true`. Lượt normal có 12 tệp mã operator, lượt induced có **13** (thêm `induced_sequence_20261113.py`); các tệp chung trùng băm, ví dụ `run_activation.py` là `6004fcea…`. Tệp này được sinh lúc export (03:16Z), không nằm trong thư mục raw (reviewer F7).
- `runtime-after-verification-20261113.json`: `dependency_files_exact` 251, `binary_and_official_installer_pin_matches`, `baseline_asar_official_byte_equal`, `asar_packed_payload_unchanged`, `only_four_unpacked_metadata_entries_changed`, `runtime_or_profile_mutation: false`, `source_updater_head` `efa4f122…`.
- `recovery-native-export-20261113.json`: `real_credentials_or_profiles_used: false` và `profile_contents_exported: false`.

## Hệ quả cho ma trận (chưa nâng hàng nào lên passed; cần review độc lập trên chính các tệp này)
- §11 #9 và U8: chứng minh được khôi phục **dữ liệu tệp** của profile thử (7957 tệp). **Không** có bằng chứng giữ phiên đăng nhập. Ngay raw cũng tự ghi là không dùng credential hay profile thật.
- §11 #6, #7, #10, U4, U7, U12: đã có raw để đối chiếu. Vẫn phải đọc `test_*`, `dependency-result` và `post-review-hardening\` mới phân được ca nào là OS thật, ca nào là fixture.
- **Vẫn thiếu:** raw P5 trên VM; hồ sơ P6 (ma trận ca U1–U12, runbook gỡ, retention và rollback, các review exact-artifact, quyết định source-policy và target). Hai cái này không có trong hai thư mục trên.
