# Handoff executor — wp433 r9 g5 (BUNDLED-TACH-MANH r9), sau review offline lượt 2

Nhánh này CHỈ chứa hồ sơ bàn giao (`ops/handoff/**`). Nhánh code `agent/wp433-r9-g5-claude` CHƯA được đẩy; SHA ứng viên
cục bộ được chuyển bằng git bundle bên cạnh tệp này (ADR-0060 M12). Số mục protocol của run này: §12 (run kế nhiệm đo lại
trước khi làm), §8.3 (vá theo lớp, bảng đóng lớp), §10.1/§12 bất biến (a) (worker gate), §7 và §3.2.1 (handoff, ba mốc).

Đo lại đầu run (2026-11-21T03:2xZ): lease `ops/leases/wp433-r9-g5-claude.yaml` tại `9f11ed7c` —
`python ops/lease_publish.py check` rc 0 ("ĐĂNG ĐƯỢC", hết hạn 2026-11-22T03:29:20Z); đặc tả r9 sha256 `8b0f376c…7691` khớp;
verdict lượt 2 `luot2-codex-36dc91a.txt` sha256 `83c8a284…a5d700` khớp; bundle g4 sha256 `b2f474c4…c8ab` khớp,
`git bundle verify` ok, `agent/wp433-r9-g4-claude` = `36dc91a5…` tree `02c26a52…`.

```yaml
schema_version: 1
packet_id: wp433
generation: 5
spec_hash: 8b0f376c8f009bcad3df018be9d47f4737d669e8a52d364339e8611e4d837691
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_015GtxrbaSKjX5Yd9LLvKZHe
base_sha: 0f9aa2a2cc697129e1f5be72feddf60986286865
head_sha: 5293a855564e8966092d49542be3bb29d5ed3787
status: needs_followup
summary: >-
  Va theo LOP 3 P2 cua review offline luot 2 (F05 shard-ast-shape-oracle, F06 bundle-gate-fixture-oracle,
  F07 shard-symlink-follow) va P3 F08 (ly do khoa vang) tren 36dc91a. Fragment 32 khoa. Commit cuoi la manifest
  tai sinh. Numstat 0f9aa2a..H: 9 tep, +447/-62 (tran 450). Chua push nhanh code.
changed_paths:
  - .githooks/eol_policy_test.py
  - RELEASE_MANIFEST.json
  - references/golden/workflow_audit.json
  - scripts/test_fragments/wp433_bundled_tach_manh.py
  - scripts/tl_core/release.py
  - scripts/tl_core/test_fragments.py
  - scripts/tl_selftest.py
  - scripts/tl_test_fragments_bundled.py
  - scripts/tl_test_fragments_bundled_2.py
tests:
  - {name: "N1 fragment 32 khoa", status: passed, evidence: "doi chung trong ma tran: run=True so_nhan=32 do=(rong)"}
  - {name: "N2 ma tran dot bien", status: passed, evidence: "ma-tran-dot-bien-5293a85.txt: 49 dot bien, sai=0, rc 0; moi dot bien mot tien trinh moi, du 32 khoa, tap False == tap dich"}
  - {name: "Dong lop F05-F08", status: passed, evidence: "dong-lop-5293a85.txt: rc 0, sai=0; moi lop co >=1 dot bien/phan chung 36dc91a de lot, ban moi bat dung tap dich"}
  - {name: "N3 tl selftest", status: passed, evidence: "rc 0, 1785/1785 (base 1784/1784) tren cay da commit; sau M8 lai 1785/1785"}
  - {name: "N3 release-manifest tai sinh", status: passed, evidence: "rc 0, git diff --numstat RONG"}
  - {name: "N3 release-verify --strict", status: passed, evidence: "rc 0, ok true, expected_file_count 186 == checked_file_count 186, failed []"}
  - {name: "N3 test-fragments-check", status: passed, evidence: "rc 0, ok true, current, shards 170024/130941 B"}
  - {name: "N3 bundle_fragment_check", status: passed, evidence: "rc 0, ok true, failed [], case_count 19"}
  - {name: "N3 workflow-audit --strict", status: passed, evidence: "rc 0, ok true, py_size.warn [], fail [], files_scanned 74 (base 73)"}
  - {name: "N3 golden-test", status: passed, evidence: "rc 0, ok true, 20 ca (core.abbrev=7)"}
  - {name: "N3 eol_policy_test", status: passed, evidence: "rc 0, 32/32 (base 32/32)"}
  - {name: "N3 ruff F", status: passed, evidence: "python -m ruff 0.15.15 (ban ghim CI): 4480 o base va o head tren 5 tep (delta 0); fragment: All checks passed"}
  - {name: "N3 git diff --check / doctrine-scan / adr-song", status: passed, evidence: "rc 0 / rc 0 / rc 0"}
  - {name: "N4 phan chung muc dich", status: passed, evidence: "ap 2 tep tu a8a3b3ca: manh 170024/146627 B, tfc ok true, py_size.warn [], selftest rc 0 1786/1786"}
  - {name: "Windows native", status: not_run, evidence: "mien theo Q4"}
  - {name: "CI GitHub", status: not_run, evidence: "nhanh code chua day (ADR-0060 M5/M12)"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: 5293a855564e8966092d49542be3bb29d5ed3787
  selected_groups: [full]
  full_fallback_reason: "packet sensitive, cham release/manifest va hop dong fragment; selector chua activate (§10.1) => full"
remaining_work:
  - "Review offline luot 3 theo §8.3 tren dung 5293a85 (dieu phoi goi; Codex PR 2/10 da dung)."
  - "Sau approve: day nhanh code MOT lan, mo PR nhap, doi chieu PR head == SHA da approve."
next_role: reviewer
manual_next_action: "Nhap bundle, doi chieu commit/tree/cha, review offline luot 3 theo §8.3 tren 5293a85."
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## Ba mốc Git (§3.2.1)

| mốc | giá trị |
|---|---|
| Immutable acceptance baseline | `0f9aa2a2cc697129e1f5be72feddf60986286865` |
| Continuation base | `36dc91a5d70df511721745d057a2eb0d0c0e37df` (lease g5 `start_from_sha`; ứng viên của review lượt 2) |
| Reviewed candidate | `5293a855564e8966092d49542be3bb29d5ed3787`, tree `761eaebc2ac723bcecae8a408902892099e85268`; 2 commit trên continuation base (`9c79054` vá, `5293a85` manifest) |

`head_sha == tested_sha == 5293a85…`. Commit cuối `5293a85` chỉ đổi `RELEASE_MANIFEST.json` (+7/−7), sinh bằng
`python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json` (Q7). Không amend.

## Numstat

`0f9aa2a..5293a85` (đo theo trần): **9 tệp, +447 / −62** (trần 9 tệp, 450 dòng thêm; còn dư 3).

```
2	4	.githooks/eol_policy_test.py
18	13	RELEASE_MANIFEST.json
1	1	references/golden/workflow_audit.json
287	0	scripts/test_fragments/wp433_bundled_tach_manh.py
22	5	scripts/tl_core/release.py
96	27	scripts/tl_core/test_fragments.py
4	2	scripts/tl_selftest.py
2	10	scripts/tl_test_fragments_bundled.py
15	0	scripts/tl_test_fragments_bundled_2.py
```

`36dc91a..5293a85` (phần vá của run này): fragment +42/−32 · `test_fragments.py` +1/−1 · bundled mảnh 1 +1/−1 (sinh bằng
`write_bundled_modules`, không sửa tay) · manifest +7/−7. Không vế kiểm nào bị cắt để vừa trần.

## Bảng đóng lớp F05–F08 (§8.3)

Mỗi lớp: tự liệt kê HẾT đường vào trước, đóng cả loạt, rồi `dong_lop.py <repo> 36dc91a 5293a85` áp CÙNG đột biến/phản chứng
lên bản cũ và bản mới (mỗi lần một clone, một tiến trình mới). Kết quả nguyên văn: `dong-lop-5293a85.txt` (rc 0, `sai=0`).
Tiêu chí: bản mới đỏ ĐÚNG tập đích ở mọi dòng, VÀ mỗi lớp có ≥1 dòng bản cũ để lọt.

| class_slug | đường vào đã liệt kê | cách vá chung | bản cũ `36dc91a` | bản mới `5293a85` | nhãn executor tự đánh |
|---|---|---|---|---|---|
| `shard-ast-shape-oracle` (F05, P2) | `_gan` là chỗ DUY NHẤT đọc hình dạng; đường vào là mọi dạng câu lệnh loader từ chối, ở mảnh chính VÀ mảnh phụ: Assign nhiều đích, Assign đích không phải `Name` (tuple), AnnAssign, AugAssign, Expr, Import, If (và mọi kiểu nút khác) | hình dạng chỉ mang tên khi nút là `ast.Assign` với ĐÚNG một đích `ast.Name` — cùng luật `_read_bundled_module`; mọi dạng khác ⇒ tên kiểu nút. Giá trị đọc rộng (mọi đích `Name`) để V4/V9 không chết theo; chỉ hình dạng phán. V8 đo cả mảnh 1 (`[SOURCES, SHARDS]`) lẫn mọi mảnh phụ (`[SOURCES]`) | 10 dạng: LỌT 7 (chính nhiều đích; phụ nhiều đích/AnnAssign/AugAssign/Expr/Import/If); 3 đã bắt (2 qua văng `AttributeError` lan V4–V9) | cả 10 dạng: đỏ ĐÚNG `V8`, không văng; loader trả `BUNDLED_MODULE_CONTRACT` cho cả 10 ở cả hai bản | ĐÃ VÁ THẬT |
| `bundle-gate-fixture-oracle` (F06, P2) | quyết định current/stale của cổng × {một mảnh, nhiều mảnh} = 4 ô; trước vá chỉ đo ô "stale nhiều mảnh" (V24). Thêm: vế kỳ vọng của cây cổng lấy từ generator thật nên đột biến định dạng generator lan sang khoá cổng | `cong()` GHIM vế kỳ vọng ở biên gọi generator (thay tạm `tf.generate_bundled_modules` bằng chính bytes `_van`, khôi phục trong `finally`), không còn gọi generator thật. V27 thêm: một mảnh current ⇒ `(rc, ok, status) == (0, True, "current")` VÀ một mảnh stale ⇒ `GENERATED_BUNDLE_STALE`. V28 thêm: nhiều mảnh current ⇒ ok | `one_skip`, `one_red`, `multi_red`: cả ba LỌT (`run` True) | `one_skip`, `one_red` đỏ đúng `V27`; `multi_red` đỏ đúng `V28` | ĐÃ VÁ THẬT |
| `shard-symlink-follow` (F07, P2) | mọi chỗ hỏi/đọc/ghi tên mảnh: (1) `_runtime_fragment_topology` `exists()` mảnh 1 — LỖ: symlink đứt ⇒ `False` ⇒ topology `none` ⇒ 0 ca; (2) `load_test_id_index` dùng cùng topology; (3) loader `_read_bundled_module` (`is_symlink()` trước `is_file()`, phủ cả đứt lẫn trỏ đúng); (4) cổng: `is_file()` mảnh 1 (đứt ⇒ MISSING, trỏ đúng ⇒ đọc vòng chung có `not is_symlink()` ⇒ STALE), mảnh phụ cùng vòng; (5) writer: `is_symlink()` mọi tên trước khi ghi; nhánh xoá mảnh lạc `unlink()` xoá chính liên kết | (1) `exists() or is_symlink()` ⇒ mọi mục tại tên mảnh 1 đi qua chốt hợp đồng của loader. V32 đo thêm symlink ĐỨT ở mảnh 1 và mảnh phụ, cho cả loader runtime, cổng và writer (đích đứt không bị tạo ra) | symlink đứt ở mảnh 1: runtime trả **0 ca** | runtime `BUNDLED_MODULE_CONTRACT` cho cả đứt và trỏ đúng; cổng `ok: false`; đột biến bỏ vá (1) đỏ đúng `V32` (ma trận `f07_…`) | ĐÃ VÁ THẬT — kèm giới hạn dưới |
| `v32-symlink-denial-diagnostic` (F08, P3) | mọi khoá văng đều mất lý do (không riêng V32) | `run()` ghi `_LY_DO[V..] = "<KiểuLỗi>: <thông điệp>"` cho MỌI khoá văng; V32 vẫn fail-closed | giả lập `PermissionError` khi tạo symlink: V32 đỏ, không có lý do | V32 đỏ, `_LY_DO["V32"] = "PermissionError: [Errno 1] …"` | ĐÃ VÁ THẬT |
| `lease-acceptance-version-drift` (F09, P3) | câu M-1 trong lease | ngoài write set executor; lease g5 do điều phối ghi đã neo M-1 ở r9/V1–V32 (đọc lại `9f11ed7c`) | — | — | đóng phía điều phối (không phải executor) |

Nhãn trên là lời khai của executor; reviewer lượt 3 mới là người gắn nhãn theo §8.3.

**Giới hạn còn lại, khai thẳng:**

- F07: `_runtime_fragment_topology` còn hỏi `fragment_root.exists()` cho THƯ MỤC `test_fragments` (không phải tên mảnh): symlink
  đứt tại thư mục ấy rơi về topology bundle. Ngoài phạm vi F07 (tên mảnh); không vá, nêu ra.
- F07: khoảng đua kiểm-rồi-mở (`is_symlink()` rồi I/O) vẫn còn như lượt trước; chưa dựng phản chứng.
- F06: cách ghim thay tạm thuộc tính module `tl_core.test_fragments.generate_bundled_modules`; đúng vì `release.py` import
  tên ấy TẠI LÚC GỌI. Nếu sau này `release.py` import ở mức module, cây cổng của fragment sẽ dùng generator thật lại (khoá
  cổng vẫn đo, nhưng mất cô lập). Hệ quả đo được trên ma trận: đột biến `c` (bỏ hạn mảnh) rời V25/V28/V29; `f03` thêm V27
  vì đột biến ấy làm cổng bỏ qua stale ở cả ca một mảnh (V27 mới đo). Hai tập đích đã sửa trong `ma_tran_dot_bien.py`.

## Ma trận đột biến N2

`ma_tran_dot_bien.py <repo>` trên exact `5293a85`: `ma-tran-dot-bien-5293a85.txt` (rc 0, `sai=0`, 49 đột biến + đối chứng).
Thêm so với lượt trước:

| đột biến | tập đích |
|---|---|
| f05: mảnh 1 gán nhiều đích (`SHARDS = EXTRA = …`) · f05b: mảnh phụ thêm `X: int = 0` | V8 · V8 |
| f06: `one_skip` · `one_red` · `multi_red` | V27 · V27 · V28 |
| f07: topology bỏ qua symlink đứt (gỡ vá) | V32 |
| đổi tập: f03 `{V24}` → `{V24, V27}`; c bỏ V25, V28, V29 | xem Giới hạn F06 |

## Phép đo (Linux, Python 3.13.18, git 2.43.0, giờ UTC 2026-11-21)

`chay_het.sh` gọi `do_n3.sh`: hai clone đầy đủ trong MỘT lệnh (nền `0f9aa2a`, sau `5293a85`, `core.abbrev 7`, dưới `/dev/shm`),
rồi `do_n4.sh`. Lệnh, rc, giờ: `do/tong.txt`, `do/chay-het.log`, `do/n4.log`.

| phép đo | base `0f9aa2a` | candidate `5293a85` |
|---|---|---|
| `python .githooks/eol_policy_test.py` | rc 0, 32/32 | rc 0, 32/32 |
| `python scripts/tl.py --selftest` (cây đã commit) | rc 0, 1784/1784 | rc 0, **1785/1785** |
| `release-manifest --out RELEASE_MANIFEST.json` rồi `git diff --numstat` | — | rc 0, diff **rỗng**; selftest sau đó rc 0 1785/1785 |
| `release-verify RELEASE_MANIFEST.json --strict --json` | — | rc 0, `ok: true`, 186 == 186, `failed: []` |
| `test-fragments-check --json` | rc 0, `ok: true` | rc 0, `ok: true`, 170.024 / 130.941 B |
| `.github/checks/bundle_fragment_check.py --json` | rc 0 | rc 0, `ok: true`, `failed: []`, 19 ca |
| `workflow-audit --strict --json` | rc 0, 73 tệp | rc 0, `ok: true`, `warn: []`, `fail: []`, 74 tệp |
| `golden-test --json` | rc 0 | rc 0, `ok: true`, 20 ca |
| `python -m ruff` 0.15.15 F trên 5 tệp | 4480 | 4480 (delta 0); fragment sạch |
| `git diff --check`, `doctrine-scan`, `adr-song` | rc 0 | rc 0 |
| `git status --short` sau đo | sạch | sạch |

N4 (`do_n4.sh`, bản sao `5293a85`, hai tệp từ `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`): mảnh 170.024 / 146.627 B;
`test-fragments-check` rc 0 `ok: true`; `py_size.warn: []`; selftest rc 0 **1786/1786**. Không commit phần áp.

**Tạo tác rig, khai thẳng (`do/luot1-bi-dung.txt`):** lượt `chay_het` đầu bị dừng ở hạn 30 phút của tác vụ nền; trước đó
selftest base cho 1783/1784 và head 1784/1785, cùng MỘT ca đỏ `wp1099_nlm_nap_lai` ("không đọc được base
references/RASOAT_HOSO_LOOP.md"): fragment ấy `git show 358451e8…` mà commit đó không có trong clone (không ref nào tới).
Đã fetch theo OID và gắn tag cục bộ trong kho nguồn của rig (không đẩy), chạy lại toàn bộ: xanh trọn như bảng trên. Hai
clone là shallow (kho nguồn của container shallow); không phép đo nào ở đây hỏi lịch sử ngoài các OID đã fetch.

## Bundle

- Tệp: `wp433-r9-g5-5293a85.bundle`, 47.365 B, sha256 `9cd88bfd0f5407993a318a42a328db888109b88e9ea3568876ef51a4a5eab513`.
- Dựng: `git bundle create wp433-r9-g5-5293a85.bundle 0f9aa2a2cc697129e1f5be72feddf60986286865..agent/wp433-r9-g5-claude`.
- Nhập: `git bundle verify <tệp>` rồi `git fetch <tệp> agent/wp433-r9-g5-claude:agent/wp433-r9-g5-claude`; đối chiếu HEAD
  `5293a855…`, `HEAD^{tree}` `761eaebc…`, `HEAD~2` phải là `36dc91a5d70df511721745d057a2eb0d0c0e37df`.

## Chưa đo

CI GitHub trên exact SHA (nhánh code chưa đẩy) · Windows native (miễn Q4) · khoảng đua symlink · human audit.
Thân comment handoff trên #433 không được đọc ngược so từng byte; nguồn có thẩm quyền là tệp này.
