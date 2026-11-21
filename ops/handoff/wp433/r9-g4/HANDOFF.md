# Handoff executor — wp433 r9 g4 (BUNDLED-TACH-MANH r9), sau review offline lượt 1

Nhánh này CHỈ chứa hồ sơ bàn giao (`ops/handoff/**`). Nhánh code `agent/wp433-r9-g4-claude` CHƯA được đẩy; SHA ứng viên
cục bộ được chuyển bằng git bundle bên cạnh tệp này (ADR-0060 M12). Số mục protocol của run này: §12 (run kế nhiệm đo lại
trước khi làm), §8.3 (vá theo lớp, bảng đóng lớp), §10.1/§12 bất biến (a) (worker gate), §7 và §3.2.1 (handoff, ba mốc).

Đo lại đầu run (2026-11-21T00:02Z): `git ls-remote` không có ref `agent/wp433-r9-g*`; đặc tả r9 sha256
`8b0f376c…7691` khớp; `lease_publish.py check ops/leases/wp433-r9-g4-claude.yaml` rc 0 tại `85effae7`, hết hạn
2026-11-22T00:00:59Z; verdict lượt 1 sha256 `61e355e1…3fb` khớp.

```yaml
schema_version: 1
packet_id: wp433
generation: 4
spec_hash: 8b0f376c8f009bcad3df018be9d47f4737d669e8a52d364339e8611e4d837691
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_015GtxrbWXRVpeaJ4iY1zhVn
base_sha: 0f9aa2a2cc697129e1f5be72feddf60986286865
head_sha: 36dc91a5d70df511721745d057a2eb0d0c0e37df
status: needs_followup
summary: >-
  Va chung 4 lop cua review offline luot 1 (F01-F04) tren 4e74fe1 va them khoa V32 theo dac ta r9:
  loader, cong va writer tu choi symlink tai ten manh. Fragment 32 khoa. Commit cuoi la manifest tai sinh.
  Chua push nhanh code.
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
  - {name: "N1 fragment 32 khoa", status: passed, evidence: "doi chung run() True, 32/32 khoa True"}
  - {name: "N2 ma tran dot bien", status: passed, evidence: "43 dot bien, sai=0, rc 0; moi dot bien mot tien trinh moi, du 32 khoa, tap False == tap dich"}
  - {name: "Dong lop F01-F04", status: passed, evidence: "dong-lop-36dc91a.txt: cung dot bien/phan chung, ban cu 4e74fe1 de lot, ban moi bat duoc"}
  - {name: "N3 tl selftest", status: passed, evidence: "rc 0, 1785/1785 (base 1784/1784) tren cay da commit"}
  - {name: "N3 release-verify --strict", status: passed, evidence: "rc 0, ok true, 186 == 186; tai sinh manifest tren candidate cho diff RONG"}
  - {name: "N3 test-fragments-check", status: passed, evidence: "rc 0, ok true, shards 168748/130941 B"}
  - {name: "N3 bundle_fragment_check", status: passed, evidence: "rc 0, ok true, failed [], case_count 19"}
  - {name: "N3 workflow-audit --strict", status: passed, evidence: "rc 0, ok true, py_size.fail [], warn [], files_scanned 74"}
  - {name: "N3 golden-test", status: passed, evidence: "rc 0, ok true"}
  - {name: "N3 eol_policy_test", status: passed, evidence: "rc 0, 32/32 tren cay da commit"}
  - {name: "N3 ruff F", status: passed, evidence: "4480 o base va o head tren 5 tep (delta 0); fragment: All checks passed"}
  - {name: "N3 git diff --check / doctrine-scan / adr-song", status: passed, evidence: "rc 0 / rc 0 / rc 0"}
  - {name: "N4 phan chung muc dich", status: passed, evidence: "ap 2 tep tu a8a3b3ca: manh 168748/146627 B, tfc ok true, py_size.warn [], selftest rc 0 1786/1786"}
  - {name: "Windows native", status: not_run, evidence: "mien theo Q4 (§4c); xem muc Rui ro ve V32 tren Windows"}
  - {name: "CI GitHub", status: not_run, evidence: "nhanh code chua day (ADR-0060 M5/M12)"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: 36dc91a5d70df511721745d057a2eb0d0c0e37df
  selected_groups: [full]
  full_fallback_reason: "packet sensitive, cham release/manifest va hop dong fragment; selector chua activate (§10.1) => full"
remaining_work:
  - "Review offline luot 2 theo §8.3 tren dung 36dc91a (dieu phoi goi)."
  - "Sau approve: day nhanh code MOT lan, mo PR nhap, doi chieu PR head == SHA da approve."
next_role: reviewer
manual_next_action: "Nhap bundle, doi chieu commit/tree/cha, review offline luot 2 theo §8.3 tren 36dc91a."
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## Ba mốc Git (§3.2.1)

| mốc | giá trị |
|---|---|
| Immutable acceptance baseline | `0f9aa2a2cc697129e1f5be72feddf60986286865` |
| Continuation base | `4e74fe1c4001ec9c83935ef831d77330b23981b0` (lease g4 `start_from_sha`; ứng viên của lượt review 1) |
| Reviewed candidate | `36dc91a5d70df511721745d057a2eb0d0c0e37df`, tree `02c26a52bfc95696682e7dbe2705247140cb272e`; 2 commit trên continuation base (`471f725` vá, `36dc91a` manifest), 9 commit trên baseline |

`origin/master` lúc bàn giao: `010046f2141799ec6ffc9cfa1322d49df3f3f680`; `0f9aa2a..010046f` chỉ đổi tệp dưới `ops/**`, không
chạm write set.

## Numstat

`0f9aa2a..36dc91a` (đo theo trần): 9 tệp, **+436 / −61** (trần 9 tệp, 450 dòng thêm; còn dư 14).

```
2	4	.githooks/eol_policy_test.py
18	13	RELEASE_MANIFEST.json
1	1	references/golden/workflow_audit.json
277	0	scripts/test_fragments/wp433_bundled_tach_manh.py
22	5	scripts/tl_core/release.py
95	26	scripts/tl_core/test_fragments.py
4	2	scripts/tl_selftest.py
2	10	scripts/tl_test_fragments_bundled.py
15	0	scripts/tl_test_fragments_bundled_2.py
```

`4e74fe1..36dc91a` (phần vá của run này): fragment +91/−59 · `test_fragments.py` +5/−0 · `release.py` +1/−1 · manifest
+11/−11 · hai tệp bundled tái sinh (+1/−2, +1/−0).

## Bảng đóng lớp F01–F04 (§8.3)

Phép kiểm đóng lớp: `dong_lop.py <repo> 4e74fe1 36dc91a` áp CÙNG một đột biến (F01–F03) hoặc CÙNG một phản chứng (F04) lên
bản cũ và bản mới, mỗi lần một clone và một tiến trình mới. Kết quả nguyên văn ở `dong-lop-36dc91a.txt` (rc 0).

| class_slug | biểu hiện đã quét | cách vá chung | bản cũ `4e74fe1` | bản mới `36dc91a` | nhãn executor tự đánh |
|---|---|---|---|---|---|
| `shard-size-byte-oracle` (F01) | V5 là vế duy nhất đo ĐƠN VỊ cắt mảnh; V4/V6 đo ranh bằng ASCII (không đo đơn vị); V27–V29, V31 đo độ dài trên `bytes` nên không có biến thể "đếm ký tự" | V5 dùng pad `đ` (2 byte UTF-8/ký tự); cỡ dòng kỳ vọng tính tay trên bytes (`_dong`), hai ranh giữ nguyên: tổng BẰNG hạn và vượt đúng 1 B | đột biến `len(line) + 1`: `run()` True 31/31 (LỌT) | cùng đột biến: `run()` False, đỏ đúng `V5` | ĐÃ VÁ THẬT |
| `shard-ast-shape-oracle` (F02) | `_gan` là chỗ DUY NHẤT đọc hình dạng AST mảnh sinh ra; dùng ở V3, V4, V8, V9 và nhóm ranh V5/V6 | `_gan` chỉ bỏ đúng MỘT docstring đầu; mọi câu lệnh khác (kể cả `ast.Expr`) vào danh sách hình dạng theo tên kiểu nút | đột biến thêm biểu thức `0` vào mảnh 1: `run()` True 31/31 (LỌT) | cùng đột biến: `run()` False, đỏ đúng `V8`; biến thể một-mảnh (`f02b`) đỏ đúng `V3` | ĐÃ VÁ THẬT |
| `bundle-gate-fixture-oracle` (F03) | V23–V29 (bảy khoá cổng) đều lấy tên và bytes đĩa từ generator; thiếu ca stale ở mảnh CHÍNH trong topology nhiều mảnh | cây cổng do `_van` render TAY từ nhóm khai sẵn, độc lập generator; V24 đo stale ở CẢ mảnh chính lẫn mảnh phụ; V27–V29 so vế kỳ vọng với đầu ra generator và vế thực tế với bytes đĩa dựng tay | đột biến "cổng bỏ so mảnh chính": `run()` True 31/31 (LỌT) | cùng đột biến: `run()` False, đỏ đúng `V24` | ĐÃ VÁ THẬT — kèm một giới hạn, xem dưới |
| `shard-symlink-follow` (F04) | mọi đường I/O tại tên mảnh: loader `_read_bundled_module` (mảnh 1 và mảnh khai), cổng đọc bytes từng mảnh, writer ghi từng mảnh; nhánh xoá mảnh lạc `unlink()` xoá chính liên kết (không đi theo); `_runtime_fragment_topology` chỉ hỏi tồn tại rồi giao loader | cùng một chốt `is_symlink()` trước I/O ở cả ba đường, cùng kiểu với `_candidate_path` của base; writer kiểm MỌI tên trước khi ghi tệp đầu tiên; thêm khoá V32 | phản chứng symlink tại mảnh 1: cổng `ok: true`, loader nạp `wp9001_a`, writer ghi đè đích symlink | cùng phản chứng: cổng `ok: false`, loader `BUNDLED_MODULE_CONTRACT`, writer `BUNDLED_MODULE_CONTRACT`, đích giữ nguyên `giu nguyen` | ĐÃ VÁ THẬT — kèm một giới hạn, xem dưới |

Nhãn trên là lời khai của executor; reviewer lượt 2 mới là người gắn nhãn theo §8.3.

**Giới hạn còn lại, khai thẳng:**

- F03: khoá cổng KHÔNG đòi cây dựng tay ở trạng thái `ok` ("đối chứng current" mà verdict gợi ý). Lý do cơ chế: một khoá
  đòi `ok` trên bytes dựng tay sẽ đỏ dưới MỌI đột biến định dạng generator (v4, v7, v8, v9, g), làm V4/V7/V8/V9 mất đột
  biến đơn đích mà N2 của đặc tả bắt buộc. Đối chứng `current` vẫn có ở hai chỗ: (a) N3 `test-fragments-check` trên cây
  thật `ok: true`; (b) đột biến `v24` và `f03` chỉ đỏ được vì trên mã không đột biến bytes dựng tay BẰNG bytes generator
  (nếu lệch, cổng luôn STALE và hai đột biến ấy sống).
- F04: chốt là `is_symlink()` rồi mới I/O, nên còn khoảng đua kiểm-rồi-mở (verdict đã nhắc). Tôi giữ cùng kiểu với chốt
  sẵn có của base và không dùng `O_NOFOLLOW` (API chỉ có trên POSIX; trần dòng còn 14). Reviewer coi đây là P2 thì cần
  vá riêng.
- F04: cổng coi symlink tại tên mảnh như mảnh VẮNG (`GENERATED_BUNDLE_STALE`, `actual_bytes: null`), không có mã lỗi riêng.

## Bundle

- Tệp: `wp433-r9-g4-36dc91a.bundle`, 72.815 B, sha256 `b2f474c494bf345dd5627a0730746355c12a65aa9e22d60d8a1bdb295b8bc8ab`.
- Dựng: `git bundle create wp433-r9-g4-36dc91a.bundle 0f9aa2a2cc697129e1f5be72feddf60986286865..agent/wp433-r9-g4-claude`.
- Nhập: `git bundle verify <tệp>` rồi `git fetch <tệp> agent/wp433-r9-g4-claude:agent/wp433-r9-g4-claude`; đối chiếu HEAD,
  `HEAD^{tree}` và chuỗi cha (`36dc91a~2` phải là `4e74fe1c4001ec9c83935ef831d77330b23981b0`).

## Phép đo (Linux, Python 3.13.18, giờ UTC 2026-11-21)

Rig như lượt trước: `do_n3.sh` dựng hai clone đầy đủ trong MỘT lệnh, nền `0f9aa2a`, sau `36dc91a`; lệnh, rc, giờ ở `do/tong.txt`.

| phép đo | base `0f9aa2a` | candidate `36dc91a` |
|---|---|---|
| `python .githooks/eol_policy_test.py` | rc 0, 32/32 | rc 0, 32/32 |
| `python scripts/tl.py --selftest` (cây đã commit) | rc 0, 1784/1784 | rc 0, **1785/1785** |
| `release-manifest --out RELEASE_MANIFEST.json` rồi `git diff --numstat` | — | rc 0, diff **rỗng** |
| `release-verify RELEASE_MANIFEST.json --strict --json` | — | rc 0, `ok: true`, 186 == 186 |
| `test-fragments-check --json` | rc 0, `ok: true`, 285.112 B | rc 0, `ok: true`, 168.748 / 130.941 B |
| `.github/checks/bundle_fragment_check.py --json` | rc 0, 18 ca | rc 0, `ok: true`, `failed: []`, 19 ca |
| `workflow-audit --strict --json` | rc 0, 73 tệp | rc 0, `ok: true`, `fail: []`, `warn: []`, 74 tệp |
| `golden-test --json` | rc 0, `ok: true` | rc 0, `ok: true` |
| ruff F trên 5 tệp | 4480 | 4480 (delta 0) |
| `git diff --check`, `doctrine-scan`, `adr-song` | rc 0 | rc 0 |
| `git status --short` sau đo | sạch | sạch |

Ranh mảnh đã dời so với `4e74fe1` (195.706 / 101.657 B): fragment của packet lớn thêm nên fragment đứng cuối mảnh 1 chuyển
sang mảnh 2. Đây là hành vi gom tham lam đã nêu ở §7 của đặc tả; cả hai mảnh ≤ 200.704 B.

N4 (`do_n4.sh`, bản sao `36dc91a`, hai tệp từ `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`): mảnh 168.748 / 146.627 B;
`test-fragments-check` rc 0 `ok: true`; `py_size.warn: []`; selftest rc 0, 1786/1786.

Verdict lượt 1 đo selftest 1770/1784 ở base và EOL 29/32 trong môi trường `env -i` của reviewer; trong môi trường của
executor cả hai xanh trọn ở base lẫn candidate. Hai rig khác nhau; tôi không đo được nguyên nhân 14 ca đỏ phía reviewer.

## Ma trận đột biến N2

`ma_tran_dot_bien.py <repo>`; kết quả trên exact `36dc91a` ở `ma-tran-dot-bien-36dc91a.txt` (rc 0, `sai=0`, 43 đột biến).
Đột biến đơn đích `v1`…`v31` giữ như lượt trước (riêng `v31` nay phình mảnh thật 40.000 B vì ranh mảnh đã dời). Thay đổi:

| đột biến | tập đích |
|---|---|
| f01: đếm ký tự thay vì byte | V5 |
| f02: mảnh 1 thêm biểu thức · f02b: một mảnh nhiều fragment thêm biểu thức | V8 · V3 |
| f03: cổng bỏ so mảnh chính | V24 |
| v32a: loader đọc xuyên symlink · v32c: cổng đọc xuyên symlink · v32d: writer ghi xuyên symlink | V32 (mỗi cái) |
| q: cổng chỉ so mảnh 1 | V24, V25, V32 (thêm V32: mảnh phụ là symlink bị bỏ qua) |
| c: generator bỏ hạn mảnh | V4–V11, V25, V28, V29, V31 (V24 rời tập: cây cổng dựng tay nên cổng vẫn STALE) |
| g, a | không đổi: V1,V2 · V13,V14,V15 |

## Rủi ro và chưa đo

- **V32 trên Windows:** đặc tả đòi "nền không tạo được symlink ⇒ khoá False". Trên Windows không có quyền tạo symlink,
  `wp433_bundled_tach_manh` sẽ ĐỎ, tức selftest thiếu một ca. Chưa đo (Windows miễn theo Q4).
- **Lease g4, mục `merge_conditions` M-1** vẫn ghi "đặc tả r7 (V1–V31)" trong khi `spec_hash` là r9 (V1–V32). Tôi làm theo
  `spec_hash`; nêu ra để điều phối sửa chữ.
- CI GitHub trên `36dc91a` chưa chạy (nhánh code chưa đẩy). Nhánh BUNDLE của V31 không có đột biến riêng (như lượt trước).
- Thân comment handoff trên #433 không được đọc ngược so từng byte; nguồn có thẩm quyền là tệp này.
