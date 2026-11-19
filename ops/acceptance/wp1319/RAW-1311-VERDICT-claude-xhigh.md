# WP1319 — Verdict độc lập trên raw 13/11 (ASUS), chỉ đọc

verdict: request_changes

Phạm vi được nhận (approve_scoped từng phần, KHÔNG nâng cả hàng): toàn vẹn gói P4; FAIL của controller trong ca gây lỗi được giữ là FAIL;
băm mã operator trước = sau; khôi phục **dữ liệu tệp** của profile thử (7957 tệp, byte-exact) trên OS thật; soak 30 phút với
healthcheck chỉ đọc `/v1/stats`, `totalRequests` = 0. Các hàng còn lại là `partial` hoặc `not_evidenced`, và có hai lời khai công khai
(§11 #6, #10) mà raw không đỡ. Phần nội dung gói P3 **chưa đo được** (máy ASUS ngừng trả lời giữa chừng, xem "Giới hạn").

- Reviewer: phiên con chỉ đọc, gọi từ phiên điều phối. Host: ASUS-LAPTOP qua Desktop Commander `7404cfba`. Thời điểm đọc: 2026-11-18 khoảng 04:47–05:10Z.
- Model/effort quan sát được: model tự khai qua môi trường là `claude-opus-5-5`; effort `KHONG_do_duoc`; served model theo từng request `KHONG_do_duoc`.
- Cách đo: `certutil -hashfile` cho tệp trên đĩa; SHA-256 của entry zip tính trong bộ nhớ qua `System.IO.Compression.ZipFile.OpenRead` (dispose sau mỗi lần). Không giải nén ra đĩa, không ghi tệp trên host, không chạy test, không gọi mạng hay model.
- Không mở nội dung nào dưới `profile\`, `closed-profile-backup\`, `isolated-home\`. Hai tệp `closed-profile-backup-manifest.json` trong zip chỉ được băm, không đọc nội dung.

## 1. Toàn vẹn

| Đối tượng | Kỳ vọng | Đo (certutil / trong bộ nhớ) | Kết quả |
|---|---|---|---|
| P4 `wp1298-ASUS-activation-20261112\recovery-native-acceptance-20261113.zip` | `97e9b78f…a3d8dc` | `97e9b78f62a3bd73c3a2550309e44e2e25a956367f2d7b3d9cf83de781a3d8dc` | khớp |
| P3 `mission1238-asus-20261112-P3\ASUS-native-canary-evidence.zip` | `147714ad…eceff` | `147714ade0daaac048e51445ef5e9775e9f44008d906a093060a953b643eceff` | khớp |
| P4: từng entry so `export-manifest.json` (byte + sha256) | 41 entry | `manifest_entries=41 zip_entries=42 ok=41 bad=0 extra_in_zip=export-manifest.json` | **41/41 khớp**, 0 lệch. Entry dư duy nhất là chính manifest (`99cfbaf4e0d30695fa936259835c502df3308effe826ec8c7ef4bfd328d90192`, 6627 byte), không tự liệt kê, đúng thiết kế của `collect_native_20261113.py` |
| P3: từng entry so `evidence-manifest.json` | 118 entry | **KHONG_do_duoc** — ASUS ngừng phản hồi trước bước này | chưa kiểm |

Không có lệch nào → **không có P1 về toàn vẹn**. Nhưng toàn vẹn entry P3 mới chỉ được bảo đảm ở mức băm cả gói.

Băm entry P4 dùng làm bằng chứng bên dưới (tính trong bộ nhớ, khớp manifest):

| Entry | Byte | sha256 |
|---|---|---|
| `recovery-normal-r2/activation-result.json` | 5175 | `dbf2f53b93da63ca5d4909a35f66aea5137d06debc12cb7689e51232b98f04cc` |
| `recovery-normal-r2/display-guardian-result.json` | 451 | `631ec538841bb162ebc4960393f8fcecd4ff823f4a24984aea947efa3cf564ec` |
| `recovery-normal-r2/execution-wrapper-result.json` | 608 | `aa15a368a0ec955a100e23808cb008d42c3bb8940e435f47cc1d02673051e75a` |
| `recovery-normal-r2/approved-source-binding.json` | 1309 | `06652a5f3a0532f0c2b75c05e261ba6c0a86924f2a1955f3180b910f47e29efc` |
| `recovery-normal-r2/source-after-run.json` | 1299 | `96ae2b03b276778266b64474d04eb9ce3a18efcda2bba2086284151761a6cb24` |
| `recovery-normal-r2/dependency-result.json` | 12142 | `05877d0dcfe5ceb9d0a98215460374423e471486bf236895e91b8aaead03fd9d` |
| `recovery-induced-failure-r2/activation-result.json` | 5278 | `6da34288476a96a2de536fcbeaf271649a2a5a3eff1c32bee042ccf325c5fa59` |
| `recovery-induced-failure-r2/induced-fixture-result.json` | 485 | `6c033bed2c0596c6177bea0ad048be547196b58d323a1bddb1a03fcbc80f8379` |
| `recovery-induced-failure-r2/induced-display-guardian-result.json` | 448 | `76e50695590d059700e4a058ba83e8357a2dacfe499cea306f64d10503df0985` |
| `recovery-induced-failure-r2/approved-source-binding.json` | 1414 | `fc26b909f0e1fa4b1cf46c459380aa922da3f255869760a38752f7f6fd93f506` |
| `recovery-induced-failure-r2/source-after-run.json` | 1403 | `6ebf0ba9c03d39d06464ec73081928389dbe27c3217480fdefa6d3062e04e71a` |
| `*/code/run_activation.py` (cả hai ca) | 14024 | `6004fceac13b3529bad81193de293bde03e17a86f7e608875cf671dd5253417c` |
| `*/code/recover_matching_data.py` | 3803 | `e2625de7a9fe65da9b4c7872a32e9e2da5bf824b96bff4194d40496413e9ba6f` |
| `*/code/operator_safety.py` | 2259 | `f5a630541f54706a8dbaa8eab59b7299db5183ec5242e9365a55dd20e8d32308` |
| `*/code/test_recovery.py` | 13597 | `f91cd0da732a0d3cf1e8914af2406ba94f98e1d0dd87400554110efb9927ba19` |
| `*/code/test_native_lock.py` | 1163 | `6d8e136ec0d8e65332f4de7a1aad8c411106f32b755e1e02b8eb89c6abb9c33a` |
| `*/code/build_variants.py` | 3661 | `98b859feadd40f154ff0020feb21f97bb78002cdc309328372d2eef8c29da1eb` |
| `recovery-induced-failure-r2/code/induced_sequence_20261113.py` | 5049 | `d8497bd65ed82f65bb05e5b95d1affbab7c481c63a22ad78ac4db813e91d3eb2` |
| `parent-code/win_activation_lease.py` | 5232 | `8b6b3a8c6acd8e4ba3748c5ec270abf1284851f948ccab44d1b9ffd2fdf2eac6` |

Tệp trên đĩa ngoài zip được trích dẫn bên dưới: **chưa băm lại** trong lượt này (ASUS ngừng trả lời). Bốn tệp có băm do phiên điều phối đo
(`RAW-1311-POINTERS.md`), ghi là `dispatcher_measured`, chưa tái đo: `runtime-after-verification-20261113.json` `d25f0353…98de`,
`recovery-native-export-20261113.json` `7c2cafd4…e493`, `expected-updater-251-20261113.json` `e6c9ab00…a05c`,
`Proxima-Setup-5.5.0.exe` `959c14c1…ebf8`. Các tệp còn lại (R1, `post-review-hardening\`, `approved-rerun-20261112\`, script gốc) ghi `sha256: KHONG_do_duoc`.

## 2. Bảng theo hàng (chỉ dựa trên raw)

Loại bằng chứng: `real_os` (tiến trình/hệ tệp thật trên ASUS) · `fixture` (tiêm lỗi/giả lập) · `inert_consumer` (ranh giới ứng dụng giả, không chạy Proxima) · `carry_forward`.

| Hàng | Verdict | Loại bằng chứng (theo vế) | Marker nguyên văn | Nguồn | sha256 |
|---|---|---|---|---|---|
| §11 #6 artifact sai nguồn/hỏng không kích hoạt | **partial** | Vế dương (artifact đúng mới được chạy): `real_os`. Vế âm (đưa artifact sai/hỏng và bị từ chối): **not_evidenced** | `"manifest_verified_files": 3225` / `3226`; trong mã: `assert s256.hexdigest()==row['sha256'] and p.stat().st_size==row['bytes'],rel` và `VerifiedReadLease` (`'Artifact identity or digest mismatch'`); `"feed_version": "5.5.0 pinned; no newer installer offered"` | entry `recovery-normal-r2/activation-result.json`; `*/code/run_activation.py`; `parent-code/win_activation_lease.py` | `dbf2f53b…04cc`; `6004fcea…417c`; `8b6b3a8c…eac6` |
| | | Tải bộ cài từ GitHub release và so digest: `real_os` (12/11) | `fetch('https://github.com/Zen4-bit/Proxima/releases/download/v5.5.0/Proxima-Setup-5.5.0.exe',…,'959c14c1…')`, `assert sha(p)==expected,('DIGEST_MISMATCH',name)`; `"full_manifest_matches": 3225`, `"unexpected_files": 0` | đĩa `stage_native.py`, `staging-result.json` | KHONG_do_duoc |
| §11 #7 máy bận hoãn / updater trùng bị khóa | **partial** | Khóa host loại trừ hai chủ: `real_os` (smoke 12/11, ngoài zip). Máy bận → **hoãn**: **not_evidenced** (mã chỉ dừng fail-closed, chưa từng kích hoạt). Khóa updater trùng của chính Proxima/electron-updater: **not_evidenced** | `"checks": ["second native writer denied atomically", "legacy read-write competitor denied", "read-only metadata remains available", "clean release permits next owner"]`; trong mã: `assert lock.tell()==0,'HOST_BUSY'`; `"host_lock_released": true` | đĩa `post-review-hardening\native-lock-test-result.json` (12/11 09:09Z); entry `*/code/run_activation.py`, `*/code/operator_safety.py`; entry normal `activation-result.json` | KHONG_do_duoc; `6004fcea…417c`; `f5a63054…2308`; `dbf2f53b…04cc` |
| §11 #8 promotion fence (máy đầu FAIL chặn máy sau) | **not_evidenced** | — | Raw P4 chỉ có một host. Hai FAIL trước (R1 `"error": "AssertionError('SOAK_OBSERVATION_GAP')"`; `post-review-hardening` `"error": "TimeoutExpired(…)"`) được nối tiếp bằng lượt chạy lại **trên chính ASUS**, không có máy thứ hai nào để chứng minh bị chặn | đĩa `activation-result.json` (gốc), `post-review-hardening\activation-result.json` | KHONG_do_duoc |
| §11 #9 phục hồi binary + dữ liệu được kiểm thử | **partial** | Dữ liệu: `real_os` (profile thử, 7957 tệp byte-exact, khôi phục qua staging + rename, rồi chạy lại baseline khỏe). Binary: `real_os` nhưng yếu — "rollback binary" là chạy lại thư mục `baseline\` đặt song song, không phải khôi phục binary bị ghi đè tại chỗ; `Proxima.exe` hai biến thể cùng băm | `"profile_files_restored_byte_exact": 7957`, `"profile_manifest_equal_before_restart": true`, `"binary_variant": "baseline"`, `"exe_sha256": "6990dce4…f886"`, `"real_cross_version_migration": false`; ca gây lỗi: `"audit": {"injected_failures": 1, "restore_calls": 1, "baseline_restart_calls": 1}` | entry normal + induced `activation-result.json`; `induced-fixture-result.json`; `variant-build-result.json` trên đĩa (`"base_runtime_SHA256"` = `"repaired_runtime_SHA256"`) | `dbf2f53b…04cc`; `6da34288…fa59`; `6c033bed…8379`; KHONG_do_duoc |
| §11 #10 file khóa / đĩa đầy / rollback thất bại | **not_evidenced** | Chỉ có **mã test** `fixture`/`inert_consumer`; **không có tệp kết quả** nào trong raw. Ca gây lỗi native duy nhất là lỗi health tiêm vào, và rollback sau đó **thành công**; nhánh "rollback thất bại" chưa từng chạy native. Dự trữ đĩa chỉ có vế dương | trong `test_recovery.py`: ca `"disk-full"`, `"partial-copy"`, `"promotion-failure"`, `"restart-failure"`, `native_locked_profile`, ghi kết quả ra `"result-" + sys.platform + ".json"`, scope `"…inert application boundary; not Electron, NSIS, cross-version migration or live ASUS proof"`. Quét raw (bỏ thư mục profile/cache): **không có** `result-win32.json`. `execution-wrapper-result.json` r2 chỉ có phase `"prepare_followup.py"` và `"run_activation.py"`. Vế dương: `"data_backup_reserve": {"snapshot_bytes": 111602416, "required_free_bytes": 1296946656, "free_bytes": 12198817792}` | entry `*/code/test_recovery.py`; entry `recovery-normal-r2/execution-wrapper-result.json`; entry normal `activation-result.json` | `f91cd0da…ba19`; `aa15a368…e75a`; `dbf2f53b…04cc` |
| §11 #11 healthcheck không inference | **passed (scoped)** — chỉ cho soak P4 trên ASUS, profile thử, mọi provider tắt, không đăng nhập | `real_os`: mỗi mẫu GET `/v1/stats`, khẳng định bộ đếm của app bằng 0; proxy owned từ chối mọi lưu lượng ra ngoài | `"health_samples": 180`, `"actual_soak_seconds": 1800.0005000999954`, `"last_stats": {"uptime": "1805s", "totalRequests": 0, "totalErrors": 0, …}`; mã: `assert stats['totalRequests']==0 and stats['totalErrors']==0,stats`; `"blocked_external_application_requests"` chỉ có `fonts.googleapis.com` ×3. Lưu ý: `"inference_calls": 0` là **hằng gán sẵn** trong `report={…}`, không phải phép đo | entry normal `activation-result.json`; entry `*/code/run_activation.py` | `dbf2f53b…04cc`; `6004fcea…417c` |
| U4 hành vi updater thực tế được kiểm soát | **partial** | `real_os`: electron-updater thật được trỏ `app-update.yml` về feed owned `127.0.0.1` phục vụ đúng 5.5.0, có kiểm log bắt buộc. Nhánh có bản mới hơn (autoDownload / autoInstallOnAppQuit / tải về và kiểm integrity): **not_evidenced** | mã: `cfg.write_text(f'provider: generic\nurl: http://127.0.0.1:{feedserver.server_port}/pinned/…')`, `assert 'electron-updater not available' not in log and '[AutoUpdater] Already on latest version:' in log,'NO_REAL_UPDATER_CHECK'`; kết quả: `"pinned_feed_requests": 1` mỗi lượt, `"feed_requests": [{"path": "/pinned/latest.yml", …} ×3]`, `"feed_version": "5.5.0 pinned; no newer installer offered"`. Sau chạy: `"baseline_asar_official_byte_equal": true`, `"only_four_unpacked_metadata_entries_changed": true`, `"runtime_or_profile_mutation": false` | entry normal `activation-result.json`; entry `*/code/run_activation.py`; đĩa `runtime-after-verification-20261113.json` | `dbf2f53b…04cc`; `6004fcea…417c`; `d25f0353…98de` (dispatcher_measured) |
| U7 soak / retention / theo dõi: phương pháp + ngưỡng + owner | **partial** | Phương pháp + ngưỡng soak: `real_os` (ngưỡng nằm trong **mã**, không phải văn bản chính sách). Retention: **not_evidenced**. Owner: **not_evidenced**. Cửa sổ theo dõi sau promotion: **not_evidenced** | mã: `deadline=now+datetime.timedelta(minutes=75)`, `assert last is None or now-last<45,'SOAK_OBSERVATION_GAP'`, nhịp mẫu `min(end,time.monotonic()+10)`, `run('repaired-soak','repaired',1800)`, `p.wait(timeout=20)`; kết quả `"planned_soak_seconds": 1800`, `"actual_soak_seconds": 1800.0005000999954`, `"health_samples": 180` | entry `*/code/run_activation.py`; entry normal `activation-result.json` | `6004fcea…417c`; `dbf2f53b…04cc` |
| U8 restore profile/đăng nhập trên profile thử | **partial** (vế dữ liệu đạt; vế đăng nhập không có bằng chứng) | Dữ liệu: `real_os`. Đăng nhập/phiên: **not_evidenced** | `"profile_files_restored_byte_exact": 7957`, `"closed_before_copy": true`, `"synthetic_marker_removed": true`, `"real_profile_used": false`; mã tạo profile: `settings={'providers':{n:{'enabled':False,'loggedIn':False} for n in ['perplexity','chatgpt','claude','gemini']},…}` | entry normal `activation-result.json`; entry `*/code/run_activation.py`; entry `*/code/recover_matching_data.py` | `dbf2f53b…04cc`; `6004fcea…417c`; `e2625de7…9e6f` |
| U12 binary 5.5.0 ↔ upstream | **partial** | `real_os`: bộ cài tải từ URL release GitHub chính thức, băm khớp digest ghim; giải nén (không cài) và 3225 tệp khớp manifest. Nối release asset với **commit nguồn** upstream (chữ ký, attestation, build provenance): **not_evidenced**. Nguồn của digest kỳ vọng và của `official-manifest.gz.b64`: không ghi trong raw | `stage_native.py`: URL `…/Zen4-bit/Proxima/releases/download/v5.5.0/Proxima-Setup-5.5.0.exe`, digest `959c14c1…ebf8`; `staging-result.json`: `"official_installer_sha256": "959c14c1…"`, `"runtime_exe_sha256": "6990dce4…"`, `"full_manifest_matches": 3225`, `"source_policy_decision": "https://github.com/ducthangho/tra-luat/issues/1298#issuecomment-6817175314"`; `runtime-after-verification`: `"binary_and_official_installer_pin_matches": true` | đĩa `stage_native.py`, `staging-result.json`, `runtime-after-verification-20261113.json` | KHONG_do_duoc; KHONG_do_duoc; `d25f0353…98de` (dispatcher_measured) |

### U8 — nói rõ đã khôi phục gì và KHÔNG bảo đảm gì
- **Đã khôi phục:** toàn bộ cây tệp của một profile **thử** do chính `run_activation.py` tạo (`profile=R/'profile'`), gồm dữ liệu ứng dụng tự sinh trong lúc chạy, `settings.json` do script viết (bốn provider `enabled: False`, `loggedIn: False`), các sentinel `qa-rollback-sentinel.txt` và một tệp đánh dấu `synthetic-migration-probe.json`. Cách làm: sao lưu khi app đã đóng, sau lượt `repaired` thì copy bản sao lưu sang staging, kiểm manifest, đổi tên, kiểm manifest lần nữa, rồi chạy lại `baseline` 45 s khỏe và kiểm `qaBaselineSentinel`. Kết quả: 7957 tệp khớp byte theo sha256.
- **KHÔNG bảo đảm:** (a) phiên đăng nhập/cookie/token còn dùng được — profile **chưa từng đăng nhập** nên phép thử này không đo được điều đó; (b) profile thật; (c) migration schema thật khác phiên bản (`"real_cross_version_migration": false`, `"cross_version_profile_migration": "not tested; both runtime variants are5.5.0, updater-only delta"`); (d) khôi phục trong lúc app còn mở (chỉ thử khi đã đóng); (e) restore thất bại chỉ có mã test, không có kết quả.

## 3. FAIL được giữ, băm mã trước/sau, credential/profile

**FAIL của controller giữ nguyên (đạt):**
- entry `recovery-induced-failure-r2/activation-result.json` (`6da34288…fa59`): `"passed": false`, `"error": "InjectedHealthFailure('INJECTED_POST_ACTIVATION_HEALTH_FAILURE_AFTER_GRACEFUL_REPAIRED_CLOSE')"`, đồng thời `"recovery": {"attempted": true, "passed": true, "stage": "complete", …}` — khôi phục thành công **không** đổi FAIL thành PASS.
- entry `induced-fixture-result.json` (`6c033bed…8379`): `"passed": true` là verdict của **fixture**, kèm `"controller_expected_verdict": "FAIL"`, `"expected_failure_observed": true`. Mã fixture khẳng định `assert raw['passed'] is False and 'INJECTED_POST_ACTIVATION_HEALTH_FAILURE' in raw['error']`.
- `collect_native_20261113.py` (đĩa, sha256 KHONG_do_duoc) chặn xuất gói nếu vi phạm: `assert fault['passed'] is False and fault['recovery']['passed']`.
- Ngữ nghĩa có trong mã: `run_repaired_then_restore` gọi restore rồi `raise` lại lỗi gốc (`"""A failed healthcheck remains FAIL even when matching-data recovery succeeds."""`).
- Phân loại: lỗi là `fixture` (tiêm qua monkeypatch `run` và `run_repaired_then_restore` lúc chạy, lượt repaired rút từ 1800 s xuống 45 s), chạy trên tiến trình và hệ tệp thật (`real_os`). Scope tự ghi: `"operator-induced failure after real repaired45s graceful close; real endpoints need not fail"`.
- Các FAIL lịch sử vẫn còn trên đĩa, không bị ghi đè: R1 `activation-result.json` gốc (`"passed": false`, `"error": "AssertionError('SOAK_OBSERVATION_GAP')"`, `"forced_cleanup": true`) và `post-review-hardening\activation-result.json` (`"passed": false`, `"host_lock_released": false`). Hai tệp này **không** nằm trong zip P4.

**Băm mã trước = sau (đạt, với một lưu ý):**
- "Trước": `approved-source-binding.json` do `normal_guardian_20261113.py` viết từ hằng `EXPECTED` **trước** khi chạy, sau khi `assert all(hashlib.sha256(raw[n]).hexdigest()==EXPECTED[n] for n in EXPECTED)`.
- "Sau": `source-after-run.json`, `"all_equal": true`. 12 tệp (normal) và 13 tệp (induced, thêm `induced_sequence_20261113.py` `d8497bd6…3eb2`) khớp từng băm với "trước", với entry `code/*` trong zip và với `recovery-upload-20261113\source-manifest.json`.
- Lưu ý: `source-after-run.json` **không có trong thư mục raw** `recovery-normal-r2\` hay `recovery-induced-failure-r2\`; nó được **sinh lúc xuất gói** bởi `collect_native_20261113.py` (`payload[name+'/source-after-run.json']=…`), tức đo lúc export (03:16Z), không phải ngay khi job kết thúc.

**Không dùng credential/profile thật (lời khai, phần lớn là hằng gán sẵn):**
- `"real_profile_used": false` (normal + induced `activation-result.json`, `display-guardian-result.json`); `"real_credentials_or_profiles_used": false`, `"profile_contents_exported": false` (`recovery-native-export-20261113.json`, `7c2cafd4…e493` dispatcher_measured). Cả ba là **hằng** trong mã, không phải phép đo.
- Phần đo được: `child_env()` chỉ cho qua danh sách biến hệ thống (`'SYSTEMROOT','WINDIR',…`), `HOME/USERPROFILE/APPDATA/LOCALAPPDATA` trỏ vào thư mục owned, `--user-data-dir` là profile thử do script tạo, provider tắt và `loggedIn: False`.
- Zip **có** hai `closed-profile-backup-manifest.json` (1 500 309 và 1 500 323 byte; `3d588d2d…08da`, `f050187c…6cb`), là danh sách đường dẫn + băm của profile thử. Đây là metadata, không phải nội dung; lượt này không đọc chúng.

## 4. Raw KHÔNG có (mà kế hoạch / bảng U đòi)
1. Raw P5 trên VM (`f7281f27`/`810f79bb`): không có trong hai thư mục. Vì vậy §11 #8 không có bằng chứng, và lời khai "ASUS passed before VM canary" không kiểm được.
2. Hồ sơ P6: ma trận ca U1–U12, runbook vận hành / gỡ bỏ, retention, review exact-artifact, quyết định source-policy dưới dạng văn bản trong raw (chỉ có link `issuecomment-6817175314`).
3. Scheduler / kiểm release hằng ngày: không có tác vụ hay log nào.
4. Cài NSIS thật: `"real_installer_executed": false`, `"Proxima_installer_executed": false` (chỉ giải nén bằng 7-Zip portable).
5. Migration khác phiên bản: `"real_cross_version_migration": false`.
6. Kết quả chạy `test_recovery.py` trên Windows (`result-win32.json`): không có. Kết quả `test_native_lock.py` chỉ có từ lượt `post-review-hardening` 12/11, không có trong lượt r2 và không có trong zip.
7. Nhánh updater khi có bản mới hơn (tải về, kiểm integrity bằng `UpdateIntegrity.js` đã vá, cài khi thoát) và ca artifact sai nguồn/hỏng bị từ chối.
8. Chữ ký Authenticode / attestation / build provenance nối release asset với commit nguồn upstream.
9. Phiên đăng nhập sau restore (U8); profile thật (cố ý không dùng).
10. Log request độc lập phía cổng REST của Proxima (healthcheck chỉ dựa vào bộ đếm `/v1/stats` app tự báo).
11. Owner và ngưỡng soak/retention ở dạng chính sách (chỉ có trong mã).
12. Nội dung gói P3: chưa đọc được trong lượt này (xem Giới hạn).

## 5. Lời khai công khai (cột "Lời khai công khai" trong MATRIX.md) mà raw mâu thuẫn hoặc không đỡ
- **§11 #6** "P4 coverage: artifact/download/cache/metadata → fault-injection": gói P4 không chứa kết quả fault-injection nào về artifact/download/cache/metadata. Chỉ có kiểm băm vế dương. **Không đỡ.**
- **§11 #10** "P4 coverage: filelock/reserve/partialcopy/rollbackfailure": các ca này chỉ tồn tại dưới dạng mã trong `test_recovery.py`, không có tệp kết quả, và lượt r2 không chạy chúng (`execution-wrapper-result.json` chỉ có `prepare_followup.py` + `run_activation.py`). **Không đỡ.**
- **§11 #7** "P4: busy/dual lock": vế dual lock có smoke native ngày 12/11 (ngoài zip). Vế "busy → hoãn" chỉ là `assert … 'HOST_BUSY'` (dừng, không hoãn) và chưa từng kích hoạt. **Đỡ một phần.**
- **§11 #9** "7957 matching files restored; 1 fault/1 restore/1 baseline restart": **đỡ** (`"profile_files_restored_byte_exact": 7957`, `"audit": {"injected_failures": 1, "restore_calls": 1, "baseline_restart_calls": 1}`). Nhưng "phục hồi binary" chỉ là chạy lại thư mục baseline song song, cùng `Proxima.exe`.
- **U4** "ASAR bằng nhau, 4 mục metadata đổi": **đỡ** (`"baseline_asar_official_byte_equal": true`, `"asar_packed_payload_unchanged": true`, `"only_four_unpacked_metadata_entries_changed": true`). Lưu ý: biến thể soak 30 phút là `repaired` (bốn tệp electron-updater thay từ `repair_source` `efa4f122…`), **không phải** 5.5.0 upstream nguyên bản.
- **U7** "P4 normal 1800s/180 mẫu": **đỡ** về số. Không đỡ phần ngưỡng/owner/retention mà bảng U đòi.
- **U12** "P6 daily check 5.5.0/same asset digest": raw không có P6 và không có kiểm hằng ngày; chỉ có một lần ghim digest lúc staging 12/11. **Không đỡ** phần "daily".
- **§11 #8** "P5: ASUS passed before VM canary": không có raw VM. **Không kiểm được.**
- `RAW-1311-POINTERS.md` (bản chiếu nội bộ): câu "`source-after-run.json`: 12 tệp mã operator… Cả hai lượt dùng cùng bộ băm" chưa chính xác — ca induced có **13** tệp; và tệp này sinh lúc export, không phải raw lúc chạy.

## 6. Findings

**P1:** không có.

**P2**
- **F1 (P2).** Hai lời khai coverage (§11 #6, #10) dựa trên **mã test** mà raw không chứa kết quả chạy (`result-win32.json` vắng; r2 không chạy `test_recovery.py`). Không được nâng hai hàng này nhờ P4. Muốn nâng thì phải có raw chạy native của từng ca, kèm `rc` và tệp kết quả có băm.
- **F2 (P2).** Không có ca âm native cho §11 #6 (artifact sai/hỏng) và cho nhánh updater có bản mới (U4). Toàn bộ chạy với feed `"5.5.0 pinned; no newer installer offered"`, nên mã integrity đã vá trong electron-updater chưa từng được kích hoạt.
- **F3 (P2).** §11 #8 promotion fence không có bằng chứng: raw chỉ có một host, và các FAIL trước đó (R1, post-review-hardening) được xử lý bằng chạy lại trên chính host ấy.
- **F4 (P2).** Toàn vẹn entry gói P3 (118 entry so `evidence-manifest.json`) và nội dung P3 (`native-canary-result.json`, `G1-handoff-result.json`, `flow-ps51\`, `flow-ps7\`) **chưa được đọc** trong lượt này. Mọi kết luận về P3 trong verdict này chỉ dừng ở băm cả gói.

**P3**
- **F5.** `"inference_calls": 0`, `"real_profile_used": false`, `"real_installer_executed": false`, `"real_credentials_or_profiles_used": false`, `"profile_contents_exported": false`, `"controller_source_modified": false` đều là **hằng gán sẵn** trong mã, không phải số đo. Bằng chứng đo được thật cho "không inference" là `last_stats.totalRequests == 0` qua 180 mẫu cộng danh sách request bị proxy chặn.
- **F6.** Ca induced mang `"scope": "fresh all-registered-data rollback plus full uninterrupted30min soak; …"` (hằng chép từ controller) trong khi lượt repaired thật chỉ chạy 45 s (`"planned_soak_seconds": 45`). Người đọc lướt có thể nhận nhầm ca induced là một soak 30 phút.
- **F7.** `source-after-run.json` của cả hai ca được sinh lúc export (03:16Z) chứ không phải lúc job đóng. Nó vẫn đúng ở mức "sau chạy", nhưng nên ghi rõ trong bản chiếu.
- **F8.** Gói P4 không mang theo các lượt FAIL lịch sử (R1 08:57Z 12/11, post-review-hardening 09:44Z) và lượt `approved-rerun-20261112` (chạy controller cũ `71ac0c1a…`, vốn thiếu restore khi health fail). Chúng còn trên đĩa, chưa có băm. Nên băm và đóng băng chúng cùng gói nếu dùng làm lịch sử.
- **F9.** "Rollback binary" là đổi giữa hai thư mục dựng sẵn có cùng `Proxima.exe` (`6990dce4…`). Chỉ phần ASAR header và bốn tệp JS khác nhau. Đây không phải khôi phục binary đã bị updater ghi đè tại chỗ.

## 7. Giới hạn
- **ASUS ngừng trả lời khoảng 04:54Z** (Desktop Commander: `Timeout - no response from device`, "Last seen" tăng dần lên 15 phút; đã thử lại sau khoảng 1,5, 3 và 4 phút). Lúc kết thúc lượt, `list_devices` báo ASUS **`Offline`**, "Last seen: 18m ago". Vì vậy chưa làm được: liệt kê và so entry P3, đọc `evidence-manifest.json`, `native-canary-result.json`, `G1-handoff-result.json`, `evidence-export.json`, `flow-ps51\`, `flow-ps7\`; băm lại các tệp đĩa ngoài zip; trích marker `[AutoUpdater] Already on latest version:` thẳng từ `repaired-soak.stdout`. Hiện chỉ suy ra marker này từ assert trong mã cộng `"passed": true`. Một lệnh `start_process` (certutil trên `evidence-manifest.json`) và một `read_file` / `list_directory` có thể vẫn còn treo phía host; cả hai đều chỉ đọc.
- Một lần `list_directory` với `depth: 2` trên `post-review-hardening\` đã vô tình liệt kê **tên** tệp cấp một trong `profile\` và `closed-profile-backup\` của thư mục đó. Không mở tệp nào, và verdict này không chép tên nào.
- `test_recovery.py`, `test_native_lock.py`, `induced_sequence_20261113.py` được **đọc mã**, không chạy. Mọi khẳng định về ca âm dựa trên việc có hay không có tệp kết quả.
- "real_os" ở đây nghĩa là tiến trình `Proxima.exe` thật (bản giải nén, không cài) chạy trên ASUS với profile thử, proxy và feed owned. Đó không phải môi trường vận hành, gateway hay VM.
- Không đọc `ops/acceptance/wp1319/r1/*`. Không đọc GitHub. Không có review của người.
- Model / effort: `claude-opus-5-5` theo môi trường tự khai; effort `KHONG_do_duoc`.

---
sha256 bản gốc của reviewer: `847182540476d0f8d8b448f4201b8a89aab9badc3b37da672bec82807d7c5819` (chép nguyên văn, không sửa).
