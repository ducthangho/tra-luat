# Handoff executor — wp433 r9 g4 (BUNDLED-TACH-MANH r9), sau review offline lượt 2

Nhánh này CHỈ chứa hồ sơ bàn giao (`ops/handoff/**`). Nhánh code `agent/wp433-r9-g4-claude` CHƯA được đẩy; SHA ứng viên
cục bộ được chuyển bằng git bundle bên cạnh tệp này (ADR-0060 M12). Số mục protocol của run này: §12 (run kế nhiệm đo
lại; đếm hội tụ theo lớp), §8.3 (vá theo lớp, bảng đóng lớp), §10.1/§12 bất biến (a), §7 và §3.2.1.

Đo lại đầu run (2026-11-21T01:14Z): `git ls-remote` không có ref `agent/wp433-r9-g*`; đặc tả r9 sha256 `8b0f376c…7691`
khớp; `lease_publish.py check ops/leases/wp433-r9-g4-claude.yaml` rc 0, hết hạn 2026-11-22T00:00:59Z; verdict lượt 2
`ops/reviews/bundled-tach-manh-cr/luot2-codex-36dc91a.txt` @ `2d8c5041` sha256 `83c8a284…a700` khớp.

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
head_sha: 6330653cf15a271d8145aa88b8db2bcbf5c685c4
status: needs_followup
summary: >-
  Va tron ba lop P2 con mo cua review offline luot 2 (F05, F06, F07) va P3 F08. Truoc khi va da liet ke moi duong vao
  cua tung lop (bang duoi). Fragment 32 khoa. Commit cuoi la manifest tai sinh. Chua push nhanh code.
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
  - {name: "N2 ma tran dot bien", status: passed, evidence: "51 dot bien, sai=0, rc 0; moi dot bien mot tien trinh moi, du 32 khoa, tap False == tap dich"}
  - {name: "Dong lop F05-F08", status: passed, evidence: "dong-lop2-6330653.txt: cung dot bien/phan chung, ban cu 36dc91a de lot, ban moi bat duoc"}
  - {name: "N3 tl selftest", status: passed, evidence: "rc 0, 1785/1785 (base 1784/1784) tren cay da commit"}
  - {name: "N3 release-verify --strict", status: passed, evidence: "rc 0, ok true, 186 == 186; tai sinh manifest tren candidate cho diff RONG"}
  - {name: "N3 test-fragments-check", status: passed, evidence: "rc 0, ok true, shards 170163/130941 B"}
  - {name: "N3 bundle_fragment_check", status: passed, evidence: "rc 0, ok true, failed [], case_count 19"}
  - {name: "N3 workflow-audit --strict", status: passed, evidence: "rc 0, ok true, py_size.fail [], warn [], files_scanned 74"}
  - {name: "N3 golden-test", status: passed, evidence: "rc 0, ok true"}
  - {name: "N3 eol_policy_test", status: passed, evidence: "rc 0, 32/32 tren cay da commit"}
  - {name: "N3 ruff F", status: passed, evidence: "4480 o base va o head tren 5 tep (delta 0); fragment: All checks passed"}
  - {name: "N3 git diff --check / doctrine-scan / adr-song", status: passed, evidence: "rc 0 / rc 0 / rc 0"}
  - {name: "N4 phan chung muc dich", status: passed, evidence: "ap 2 tep tu a8a3b3ca: manh 170163/146627 B, tfc ok true, py_size.warn [], selftest rc 0 1786/1786"}
  - {name: "Windows native", status: not_run, evidence: "mien theo Q4 (§4c)"}
  - {name: "CI GitHub", status: not_run, evidence: "nhanh code chua day (ADR-0060 M5/M12)"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: 6330653cf15a271d8145aa88b8db2bcbf5c685c4
  selected_groups: [full]
  full_fallback_reason: "packet sensitive, cham release/manifest va hop dong fragment; selector chua activate (§10.1) => full"
remaining_work:
  - "Review offline luot 3 theo §8.3 tren dung 6330653 (dieu phoi goi)."
  - "Sau approve: day nhanh code MOT lan, mo PR nhap, doi chieu PR head == SHA da approve."
next_role: reviewer
manual_next_action: "Nhap bundle, doi chieu commit/tree/cha, review offline luot 3 theo §8.3 tren 6330653."
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## Ba mốc Git (§3.2.1)

| mốc | giá trị |
|---|---|
| Immutable acceptance baseline | `0f9aa2a2cc697129e1f5be72feddf60986286865` |
| Continuation base | `36dc91a5d70df511721745d057a2eb0d0c0e37df` (ứng viên của lượt review 2; lease g4 vẫn hiệu lực) |
| Reviewed candidate | `6330653cf15a271d8145aa88b8db2bcbf5c685c4`, tree `1af9b30e2ce916077cc77fc08ab5caa383cab591`; `6330653~2 == 36dc91a` (`0fd1bd2` vá, `6330653` manifest) |

`origin/master` lúc bàn giao: `e02d748d29cd5165fc29fa1a5a8e9b94593874c7`; `0f9aa2a..e02d748` không chạm tệp nào ngoài `ops/**`.

## Numstat — ĐÚNG BẰNG TRẦN

`0f9aa2a..6330653`: 9 tệp, **+450 / −62**. Trần là 9 tệp, 450 dòng thêm: **đạt, dư 0 dòng**. Mọi bản vá tiếp theo có
thêm dòng ròng sẽ vượt trần ⇒ phải DỪNG và hỏi chủ kho (E2) trước khi vá.

```
2	4	.githooks/eol_policy_test.py
18	13	RELEASE_MANIFEST.json
1	1	references/golden/workflow_audit.json
290	0	scripts/test_fragments/wp433_bundled_tach_manh.py
22	5	scripts/tl_core/release.py
96	27	scripts/tl_core/test_fragments.py
4	2	scripts/tl_selftest.py
2	10	scripts/tl_test_fragments_bundled.py
15	0	scripts/tl_test_fragments_bundled_2.py
```

Phần vá của run này (`36dc91a..6330653`): fragment +46/−33 · `test_fragments.py` +1/−1 · manifest +7/−7 · mảnh 1 tái sinh +1/−1.

## Liệt kê đường vào TRƯỚC khi vá, và bảng đóng lớp (§8.3)

Phép kiểm đóng lớp: `dong_lop2.py <repo> 36dc91a 6330653`, mỗi dòng một clone mới và một tiến trình mới; kết quả nguyên
văn ở `dong-lop2-6330653.txt` (rc 0). Nhãn là lời khai của executor; reviewer lượt 3 gắn nhãn chính thức.

### F05 `shard-ast-shape-oracle`

Đường vào đã liệt kê — mọi dạng câu lệnh có thể đứng trong một mảnh sinh ra và quyết định của loader:

| dạng | loader | fragment bản cũ `36dc91a` | fragment bản mới |
|---|---|---|---|
| `Assign` một đích là tên, đúng tên và thứ tự | nhận | xanh | xanh |
| `Assign` nhiều đích (`A = B = …`) | từ chối | **xanh (lọt)** | đỏ V8 |
| `Assign` đích không phải tên (thuộc tính, chỉ số, tuple) | từ chối | văng ⇒ đỏ | đỏ V8 |
| `AnnAssign`, `AugAssign` | từ chối | **xanh ở mảnh phụ (lọt)** | đỏ V8 |
| `Expr` ngoài đúng một docstring đầu | từ chối | đỏ ở mảnh 1, **lọt ở mảnh phụ** | đỏ V8 |
| câu lệnh khác (`Import`, `Pass`, `If`…) | từ chối | **lọt ở mảnh phụ** | đỏ V8 |
| sai tên phép gán / sai thứ tự / thừa phép gán | từ chối | đỏ ở mảnh 1, **lọt ở mảnh phụ** | đỏ V8 |
| giá trị không phải literal, `SOURCES` không phải tuple, mục không phải cặp chuỗi | từ chối | **lọt** (oracle chỉ đọc tên) | đỏ V8 |

Cột "bản cũ" của bảng trên: chỉ hai hàng `Assign` nhiều đích (mảnh 1) và `AnnAssign` (mảnh phụ) là ĐÃ ĐO
(`dong_lop2.py`); các hàng còn lại là đọc mã bản cũ, chưa chạy. Cột "bản mới": đã đo cho nhiều đích, `AnnAssign`,
`Expr` và `Import` (ma trận `f05a`–`f05d`, `f02`, `v8`); các dạng khác suy từ cùng một nhánh mã.

Cách vá chung, hai chốt độc lập trong V8: (1) `_gan` chỉ gọi một câu lệnh bằng TÊN khi nó là `Assign` đúng MỘT đích là
`ast.Name`; mọi dạng khác lộ ra bằng tên kiểu nút, và V8 so hình dạng của MỌI mảnh (`[[SOURCES, SHARDS], [SOURCES],
[SOURCES]]`), không chỉ mảnh 1; (2) V8 đưa từng mảnh generator sinh ra qua chính `_read_bundled_module` của loader và
đòi được chấp nhận — phủ luôn các dạng mà oracle AST của fragment không tự liệt kê được (hàng cuối bảng).

| phép kiểm | bản cũ `36dc91a` | bản mới `6330653` |
|---|---|---|
| đột biến mảnh 1 gán nhiều đích (`chain` của reviewer) | `run()` True 32/32 | False, đỏ đúng V8 |
| đột biến mảnh phụ thêm `AnnAssign` (`statement` của reviewer) | `run()` True 32/32 | False, đỏ đúng V8 |
| ma trận: `f05c` mảnh 1 thêm `import`, `f05d` mảnh phụ thêm biểu thức, `f02`, `v8` | — | mỗi cái đỏ đúng V8 |

Nhãn executor: **ĐÃ VÁ THẬT**. Giới hạn: chốt (2) dùng chính loader làm oracle nên một đột biến làm loader DỄ hơn không
được V8 phát hiện; phần ấy do V18–V22 (fixture viết tay) đo.

### F06 `bundle-gate-fixture-oracle`

Đường vào đã liệt kê — quyết định của cổng theo trạng thái đĩa × số mảnh:

| trạng thái đĩa | một mảnh | nhiều mảnh |
|---|---|---|
| hiện hành ⇒ phải `ok` | V27 (mới: đòi rc 0 và `ok`) | V28 (mới: đòi rc 0 và `ok`) |
| mảnh chính lệch bytes ⇒ STALE | V24 (mới) | V24 |
| mảnh phụ lệch bytes ⇒ STALE | không áp dụng | V24 |
| mảnh phụ thiếu ⇒ STALE, `actual_bytes: null` | không áp dụng | V25 |
| mảnh chính thiếu ⇒ MISSING | V26 | cùng nhánh mã với một mảnh (trả về trước khi gọi generator) |
| tệp đánh số lạc ⇒ STALE + `extra_shards` | không đo riêng (cùng một phép `extra`) | V23 |

Cách vá chung: generator bị THAY ở biên gọi của cổng (`tf.generate_bundled_modules` trả các mảnh do `_van` render tay),
nên cả đĩa lẫn vế kỳ vọng của cây cổng đều dựng tay và khoá cổng không còn phụ thuộc generator thật. Nhờ vậy đòi được
`ok` ở trạng thái hiện hành mà không dính chéo với đột biến định dạng generator — giới hạn tôi khai ở lượt trước nay hết.

| phép kiểm | bản cũ `36dc91a` | bản mới `6330653` |
|---|---|---|
| `one_skip`: cổng nhận một mảnh stale | `run()` True 32/32 | False, đỏ đúng V24 |
| `one_red`: cổng từ chối một mảnh hiện hành | `run()` True 32/32 | False, đỏ đúng V27 |
| ma trận: `f06c` cổng từ chối nhiều mảnh hiện hành | — | đỏ đúng V28 |
| đột biến `c` (bỏ hạn mảnh) | đỏ cả V25, V28, V29 | chỉ còn V4–V11, V31: khoá cổng đã rời tập |

Nhãn executor: **ĐÃ VÁ THẬT**. Giới hạn: vì generator bị thay, khoá cổng không đo việc cổng GỌI đúng generator với đúng
thư mục; việc ấy do N3 `test-fragments-check` trên cây thật đo (`ok: true`, hai mảnh).

### F07 `shard-symlink-follow`

Đường vào đã liệt kê — mọi chỗ đọc, ghi hoặc kiểm tên mảnh (`rg` trên `scripts/tl_core/`, `scripts/tl.py`, `.github/checks/`, `.githooks/`):

| chỗ | symlink trỏ đúng | symlink đứt | sau bản vá |
|---|---|---|---|
| `_runtime_fragment_topology`: `bundled_path.exists()` (đường của `load_runtime_fragment_cases` và `load_test_id_index`) | `exists` True ⇒ loader từ chối | **`exists` False ⇒ topology `none`, 0 ca** | thêm `or bundled_path.is_symlink()` ⇒ tới chốt loader |
| `_read_bundled_module`: `is_symlink` rồi `is_file`, `read_text` (mảnh 1 và mảnh khai) | CONTRACT | CONTRACT (`is_symlink` đứng trước `is_file`) | không đổi |
| cổng: `bundled_path.is_file()` | qua, rồi vòng đọc trả `None` ⇒ STALE | MISSING | không đổi; cả hai đều không `ok` |
| cổng: đọc bytes từng mảnh `is_file() and not is_symlink()` | `None` ⇒ STALE | `None` ⇒ STALE | không đổi |
| cổng: liệt kê tệp đánh số lạc (`iterdir`, chỉ so TÊN) | STALE | STALE | không đổi, không đọc nội dung |
| writer: `is_symlink()` cho mọi tên trước khi ghi | từ chối, đích giữ nguyên | từ chối, đích KHÔNG được tạo | không đổi |
| writer: xoá mảnh lạc `unlink()` | xoá chính liên kết | xoá chính liên kết | không đổi |
| `.github/checks/bundle_fragment_check.py`: cờ `has_bundled_module` dùng `is_file()` | đi theo liên kết | False | NGOÀI write set; chỉ là cờ chẩn đoán, không đọc nội dung |

V32 nay đo 4 ca × 3 đường: (mảnh chính, mảnh phụ) × (symlink trỏ đúng, symlink đứt) trên loader RUNTIME
(`load_runtime_fragment_cases`), cổng và writer (đích giữ nguyên bytes; đích của symlink đứt không được tạo ra).

| phép kiểm | bản cũ `36dc91a` | bản mới `6330653` |
|---|---|---|
| mảnh 1 là symlink đứt, `load_runtime_fragment_cases` | trả `[]` (0 ca) | `BUNDLED_MODULE_CONTRACT` |
| ma trận: `f07` gỡ `or is_symlink()` ở topology | — | đỏ đúng V32 |

Nhãn executor: **ĐÃ VÁ THẬT** cho mọi đường trong write set. Còn mở, khai thẳng: (a) khoảng đua kiểm-rồi-mở vẫn còn
(reviewer lượt 2 chưa xác lập P2 cho nó); (b) cờ `has_bundled_module` của `bundle_fragment_check.py` nằm ngoài write set;
(c) phép đo `load_test_id_index` trong `dong_lop2.py` KHÔNG ĐO ĐƯỢC — probe của tôi dựng cây thiếu `tl_selftest.py` nên
cả hai bản cùng ra `TEST_ID_INDEX_READ`; đường ấy chỉ được phủ gián tiếp vì dùng chung `_runtime_fragment_topology`.

### F08 `v32-symlink-denial-diagnostic` (P3) và F09

- F08: `run()` ghi lý do của mọi khoá False-vì-văng vào `_LY_DO`. Giả lập `Path.symlink_to` ném `PermissionError`:
  bản cũ đỏ V32, không lý do; bản mới đỏ đúng V32, `_LY_DO["V32"]` chứa `PermissionError('nen tu choi tao symlink (gia lap)')`.
  Nhãn executor: **ĐÃ VÁ THẬT**. Lý do nằm trong biến của module; harness selftest của kho không in nó ra.
- F09 `lease-acceptance-version-drift`: thuộc lease, điều phối sửa; executor không đụng.

### Đếm hội tụ theo lớp (§12), do executor tự tính — reviewer lượt 3 mới là nguồn

Cuối lượt 2 còn mở U = {`shard-ast-shape-oracle`, `bundle-gate-fixture-oracle`, `shard-symlink-follow`,
`v32-symlink-denial-diagnostic`, `lease-acceptance-version-drift`}. Executor khai đã đóng 4/5 trong phạm vi của mình; lớp
thứ năm thuộc lease. Ba lớp đầu đã xuất hiện ở HAI lượt review (1 và 2); nếu một lớp trong đó xuất hiện lần thứ BA ở
lượt 3 thì theo §12 phiên phải dừng vá và xét lại cách làm, không vá lần thứ tư.

## Bundle

- Tệp: `wp433-r9-g4-6330653.bundle`, 77.329 B, sha256 `ba73a2ce48d4e76b6256ef6ce388a753b00ec227dc9796998cda66621fe3f0f8`.
- Dựng: `git bundle create wp433-r9-g4-6330653.bundle 0f9aa2a2cc697129e1f5be72feddf60986286865..agent/wp433-r9-g4-claude`.
- Nhập: `git bundle verify <tệp>` rồi `git fetch <tệp> agent/wp433-r9-g4-claude:<nhánh cục bộ>`; đối chiếu HEAD,
  `HEAD^{tree}`, và `HEAD~2 == 36dc91a5d70df511721745d057a2eb0d0c0e37df`.

## Phép đo (Linux, Python 3.13.18, giờ UTC 2026-11-21)

Rig: `do_n3.sh` dựng hai clone đầy đủ trong MỘT lệnh, nền `0f9aa2a`, sau `6330653`; lệnh, rc, giờ ở `do/tong.txt`.

| phép đo | base `0f9aa2a` | candidate `6330653` |
|---|---|---|
| `python .githooks/eol_policy_test.py` | rc 0, 32/32 | rc 0, 32/32 |
| `python scripts/tl.py --selftest` (cây đã commit) | rc 0, 1784/1784 | rc 0, **1785/1785** |
| `release-manifest --out RELEASE_MANIFEST.json` rồi `git diff --numstat` | — | rc 0, diff **rỗng** |
| `release-verify RELEASE_MANIFEST.json --strict --json` | — | rc 0, `ok: true`, 186 == 186 |
| `test-fragments-check --json` | rc 0, `ok: true`, 285.112 B | rc 0, `ok: true`, 170.163 / 130.941 B |
| `.github/checks/bundle_fragment_check.py --json` | rc 0, 18 ca | rc 0, `ok: true`, `failed: []`, 19 ca |
| `workflow-audit --strict --json` | rc 0, 73 tệp | rc 0, `ok: true`, `fail: []`, `warn: []`, 74 tệp |
| `golden-test --json` | rc 0, `ok: true` | rc 0, `ok: true` |
| ruff F trên 5 tệp | 4480 | 4480 (delta 0) |
| `git diff --check`, `doctrine-scan`, `adr-song` | rc 0 | rc 0 |
| `git status --short` sau đo | sạch | sạch |

N4 (bản sao `6330653`, hai tệp từ `a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c`): mảnh 170.163 / 146.627 B;
`test-fragments-check` rc 0 `ok: true`; `py_size.warn: []`; selftest rc 0, 1786/1786.

Rig của reviewer (hai lượt) đo selftest, EOL và bundle checker ĐỎ ở cả base lẫn ứng viên với cùng tập ca; rig của
executor xanh trọn ở cả hai. Verdict lượt 2 ghi một nguyên nhân đã đo: `golden` đỏ khi Git không ghim `core.abbrev=7`
(rig executor ghim như CI). Các ca đỏ còn lại phía reviewer tôi KHÔNG ĐO ĐƯỢC nguyên nhân.

## Ma trận đột biến N2

`ma_tran_dot_bien.py <repo>`; kết quả trên exact `6330653` ở `ma-tran-dot-bien-6330653.txt`: rc 0, `sai=0`, 51 đột biến.
Thêm ở run này: `f05a`–`f05d` → V8 · `f06a` → V24 · `f06b` → V27 · `f06c` → V28 · `f07` → V32. Đổi tập đích: `c` → V4–V11, V31.
Giữ nguyên: 31 đột biến đơn đích `v1`…`v31`, `f01`–`f03`, `v32a/c/d`, `g` → V1,V2 · `a` → V13,V14,V15 · `q` → V24,V25,V32.

## Chưa đo

- CI GitHub trên `6330653`; Windows native (miễn Q4) — nền không tạo được symlink thì V32 đỏ theo đúng câu chữ r9.
- Khoảng đua kiểm-rồi-mở của chốt symlink (chỉ đọc mã).
- `load_test_id_index` với symlink đứt (probe không đo được, xem F07).
- Nhánh BUNDLE của V31 không có đột biến riêng.
- Thân comment handoff trên #433 không được đọc ngược so từng byte; nguồn có thẩm quyền là tệp này.
