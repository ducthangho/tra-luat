# Handoff executor — wp433 r9 g3 (BUNDLED-TACH-MANH r8)

Nhánh này CHỈ chứa hồ sơ bàn giao (`ops/handoff/**`), không chứa tệp nào thuộc write set code. Nhánh code
`agent/wp433-r9-g3-claude` CHƯA được đẩy; SHA ứng viên cục bộ được chuyển bằng git bundle bên cạnh tệp này
(ADR-0060 M12). Số mục protocol của bước này: §7 (handoff), §3.2.1 (ba mốc), §10.1/§12 bất biến (a) (worker gate), §13.

```yaml
schema_version: 1
packet_id: wp433
generation: 3
spec_hash: 9fb283ceb3633aeeffa20a16610b6f3be3caa785809410c8795dd9ea9666eba4
provider: claude
model_family: claude
execution_surface: claude_code
transport: machine/local
role: executor
session_id: session_015GtxrbWXRVpeaJ4iY1zhVn
base_sha: 0f9aa2a2cc697129e1f5be72feddf60986286865
head_sha: 4e74fe1c4001ec9c83935ef831d77330b23981b0
status: needs_followup
summary: >-
  Tach scripts/tl_test_fragments_bundled.py thanh hai manh (195706 B va 101657 B, han manh 196608 B dong nguon);
  loader chi nap manh duoc khai; cong test-fragments-check so tung manh va bao manh lac; fragment 31 khoa V1-V31;
  commit cuoi la RELEASE_MANIFEST.json tai sinh (185 -> 186 tep). Chua push nhanh code.
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
  - {name: "N1 fragment 31 khoa", status: passed, evidence: "doi chung run() True, 31/31 khoa True (ma-tran-dot-bien-4e74fe1.txt dong doi_chung)"}
  - {name: "N2 ma tran dot bien", status: passed, evidence: "36 dot bien, sai=0, rc 0; moi dot bien mot tien trinh moi, du 31 khoa, tap False == tap dich"}
  - {name: "N3 tl selftest", status: passed, evidence: "rc 0, 1785/1785 (base 1784/1784) tren cay da commit"}
  - {name: "N3 release-verify --strict", status: passed, evidence: "rc 0, ok true, expected_file_count 186 == checked_file_count 186; tai sinh manifest tren C cho diff RONG"}
  - {name: "N3 test-fragments-check", status: passed, evidence: "rc 0, ok true, shards 195706/101657 B"}
  - {name: "N3 bundle_fragment_check", status: passed, evidence: "rc 0, ok true, failed [], case_count 19"}
  - {name: "N3 workflow-audit --strict", status: passed, evidence: "rc 0, ok true, py_size.fail [], warn [], files_scanned 74"}
  - {name: "N3 golden-test", status: passed, evidence: "rc 0, ok true"}
  - {name: "N3 eol_policy_test", status: passed, evidence: "rc 0, 32/32 tren cay da commit"}
  - {name: "N3 ruff F", status: passed, evidence: "4480 o base va o head tren 5 tep (delta 0); fragment moi: All checks passed"}
  - {name: "N3 git diff --check / doctrine-scan / adr-song", status: passed, evidence: "rc 0 / rc 0 / rc 0"}
  - {name: "N4 phan chung muc dich", status: passed, evidence: "ap 2 tep tu a8a3b3ca: manh 195706/117343 B, tfc ok true, py_size.warn [], selftest rc 0 1786/1786"}
  - {name: "Windows native", status: not_run, evidence: "mien theo Q4 cua dac ta (§4c)"}
  - {name: "CI GitHub", status: not_run, evidence: "nhanh code chua day (ADR-0060 M5/M12: day sau khi review offline approve)"}
test_selection:
  gate_tier: T2
  selector_policy_sha: null
  tested_sha: 4e74fe1c4001ec9c83935ef831d77330b23981b0
  selected_groups: [full]
  full_fallback_reason: "packet sensitive, cham release/manifest va hop dong fragment; selector chua activate (§10.1) => full"
remaining_work:
  - "Review offline theo §8.3 tren dung 4e74fe1 (dieu phoi goi)."
  - "Sau approve: day nhanh code MOT lan, mo PR nhap, doi chieu PR head == 4e74fe1."
next_role: reviewer
manual_next_action: "Nhap bundle, doi chieu commit/tree/cha, review offline theo §8.3 tren 4e74fe1."
copyable_prompt: null
failure: {fingerprint: null, category: null}
successors: []
```

## Ba mốc Git (§3.2.1)

| mốc | giá trị |
|---|---|
| Immutable acceptance baseline | `0f9aa2a2cc697129e1f5be72feddf60986286865` (tree `da48b7d3aa2c430499461a35c82f52a96ff5e07f`) |
| Continuation base | `0f9aa2a2cc697129e1f5be72feddf60986286865` (lease g3 `start_from_sha`; g1, g2 chưa từng đẩy gì) |
| Reviewed candidate | `4e74fe1c4001ec9c83935ef831d77330b23981b0`, tree `a45d67ba35d157e87960beb9185c0989daeeb07d`, 7 commit trên baseline |

Nguồn đặc tả: `ops/specs/BUNDLED-TACH-MANH-r8.md` tại `69b8bf32ddcf69477907d58cd6b4b13da77bd1e2` (nhánh
`ops/bundled-tach-manh-spec`), sha256 `9fb283ce…eba4` — tự đo, khớp. Lease `ops/leases/wp433-r9-g3-claude.yaml` cùng commit:
`lease_publish.py check` rc 0. Ngoại lệ bundled + manifest + trần: comment `7047878267` trên #433.

`origin/master` lúc bàn giao là `48d372e14f190dae83a75ccbca8ee9a0b25635c5`; `0f9aa2a..48d372e` chỉ thêm 3 tệp `ops/**` của
packet khác, không chạm write set.

## Numstat `0f9aa2a..4e74fe1`

```
2	4	.githooks/eol_policy_test.py
18	13	RELEASE_MANIFEST.json
1	1	references/golden/workflow_audit.json
245	0	scripts/test_fragments/wp433_bundled_tach_manh.py
22	5	scripts/tl_core/release.py
90	26	scripts/tl_core/test_fragments.py
4	2	scripts/tl_selftest.py
2	9	scripts/tl_test_fragments_bundled.py
14	0	scripts/tl_test_fragments_bundled_2.py
```

9 tệp, **+398 / −60** (trần: 9 tệp, 450 dòng thêm).

## Bundle

- Tệp: `wp433-r9-g3-4e74fe1.bundle`, 60.645 B, sha256 `24a2bec3be01f83319ad60a7a0b20d5f1f2dbf774477480e1787bc38c4929f1d`.
- Dựng: `git bundle create wp433-r9-g3-4e74fe1.bundle 0f9aa2a2cc697129e1f5be72feddf60986286865..agent/wp433-r9-g3-claude`.
- Nhập: trong clone đầy đủ có `0f9aa2a`: `git bundle verify <tệp>` rồi
  `git fetch <tệp> agent/wp433-r9-g3-claude:agent/wp433-r9-g3-claude`; đối chiếu `git rev-parse` HEAD, `HEAD^{tree}` và cha.
- Hai tệp bundled chỉ sinh bằng `write_bundled_modules(scripts/test_fragments, scripts)`; manifest chỉ sinh bằng
  `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json`. Tái sinh cả hai trên `4e74fe1` cho diff rỗng (đã đo).

## Phép đo (Linux, Python 3.13.18, giờ UTC 2026-11-20)

Rig: `do_n3.sh` dựng HAI clone đầy đủ (`shallow=false`) dưới `/dev/shm` trong MỘT lệnh, `core.abbrev 7`, `TMPDIR` dưới
`/dev/shm`; nền `0f9aa2a`, sau `4e74fe1`. Lệnh, rc và giờ từng bước ở `do/tong.txt`.

| phép đo | base `0f9aa2a` | candidate `4e74fe1` |
|---|---|---|
| `python .githooks/eol_policy_test.py` | rc 0, 32/32 | rc 0, 32/32 |
| `python scripts/tl.py --selftest` (cây đã commit) | rc 0, 1784/1784 | rc 0, **1785/1785** |
| `release-manifest --out RELEASE_MANIFEST.json` rồi `git diff --numstat` | — | rc 0, diff **rỗng** |
| `release-verify RELEASE_MANIFEST.json --strict --json` | — | rc 0, `ok: true`, 186 == 186 |
| `test-fragments-check --json` | rc 0, `ok: true`, 285.112 B | rc 0, `ok: true`, 195.706 / 101.657 B |
| `.github/checks/bundle_fragment_check.py --json` | rc 0, 18 ca | rc 0, `ok: true`, `failed: []`, 19 ca |
| `workflow-audit --strict --json` | rc 0, 73 tệp | rc 0, `ok: true`, `fail: []`, `warn: []`, 74 tệp |
| `golden-test --json` | rc 0, `ok: true` | rc 0, `ok: true` |
| ruff F trên 5 tệp | 4480 | 4480 (delta 0) |
| `git diff --check`, `doctrine-scan`, `adr-song` | rc 0 | rc 0 |
| `git status --short` sau đo | sạch | sạch |

N4 (`do_n4.sh`, bản sao của `4e74fe1`, hai tệp lấy bằng `git show a8a3b3ca2fe5f48d8e6db64a8c6abacf97526b8c:<đường>`, không
commit): mảnh 195.706 / 117.343 B; `test-fragments-check` rc 0 `ok: true`; `workflow-audit --strict` rc 0, `py_size.warn: []`;
selftest rc 0, 1786/1786.

Điều kiện dừng §6 của đặc tả: 2 mảnh, cả hai ≤ 200.704 B; không ca selftest nào đổi trạng thái ngoài +1 ca mới.

## Ma trận đột biến N2

Script `ma_tran_dot_bien.py <repo>`; kết quả trên exact `4e74fe1` (cây sạch) ở `ma-tran-dot-bien-4e74fe1.txt`: rc 0,
`sai=0`. Mỗi đột biến áp lên một BẢN SAO cây (`git ls-files`) và chạy trong một tiến trình MỚI; kết quả là bản đồ khoá của
chính lần `run()` ấy; khoá vắng tính là False. Mọi dòng: `run()` False, đủ 31 khoá, không văng, tập False == tập đích.

| đột biến | tập đích |
|---|---|
| v1: generator một-mảnh thêm LF, wrapper bù lại (hai chỗ) | V1 |
| v2: wrapper một-mảnh thêm LF | V2 |
| v3: một mảnh nhiều fragment vẫn khai SHARDS | V3 |
| v4: đảo thứ tự dòng trong mảnh | V4 |
| v5: cắt khi BẰNG hạn; v5b: đơn vị byte bỏ +1 LF | V5 |
| v6: hàng xóm ghép vào mảnh quá hạn | V6 |
| v7: tên mảnh 3 sai | V7 |
| v8: mảnh 1 thêm một phép gán | V8 |
| v9: khai thiếu mảnh cuối | V9 |
| v10: wrapper trả mảnh cuối | V10 |
| v11: writer ghi sai bytes mảnh phụ | V11 |
| v12: writer không xoá tệp lạc | V12 |
| v13: nạp thêm tệp không khai | V13 |
| v14: mảnh phụ thiếu ⇒ mã lỗi khác | V14 |
| v15: đường mảnh thiếu luôn là mảnh 1 | V15 |
| v16: bỏ kiểm thứ tự xuyên mảnh | V16 |
| v17: bỏ kiểm trùng ở loader | V17 |
| v18: mảnh k≥2 được mang SHARDS | V18 |
| v19: nhận SHARDS rỗng | V19 |
| v20: nhận SHARDS không liên tục | V20 |
| v21: mảnh 1 bỏ qua câu lệnh thừa | V21 |
| v22: mảnh k≥2 bỏ qua câu lệnh thừa | V22 |
| v23: cổng bỏ `extra_shards` | V23 |
| v24: cổng chỉ xét mảnh phụ có mặt hay không | V24 |
| v25: mảnh phụ thiếu đọc thành rỗng | V25 |
| v26: thiếu mảnh 1 báo STALE | V26 |
| v27: một mảnh băm theo chuỗi có tên | V27 |
| v28: băm nhiều mảnh bỏ tên | V28 |
| v29: `shards[].expected_bytes` lệch 1 | V29 |
| v30: hạn mảnh 200000 | V30 |
| v31: mảnh nhiều fragment phình 9000 B | V31 |
| g: đổi dòng chú thích đầu tệp sinh ra | V1, V2 |
| a: loader nạp mọi tệp đánh số, bỏ khai báo | V13, V14, V15 |
| q: cổng chỉ so mảnh 1 | V24, V25 |
| c: generator bỏ hạn mảnh | V4–V11, V24, V25, V28, V29, V31 |

## Lựa chọn của executor cần reviewer soi

1. **V3 dùng fixture một-mảnh riêng** (hai fragment nhỏ), không chung với V1/V2: hằng ghim của V1/V2 đã kéo theo "không
   có SHARDS", nên chung fixture thì không đột biến nào phá riêng được V3.
2. **Cây cổng (V23–V29) lấy bytes generator rồi ghi thẳng**, không qua writer: trạng thái `current` của cổng theo định
   nghĩa là "bằng generator", nên không dựng được hoàn toàn độc lập với generator. Fixture loader (V13–V22) viết tay.
3. **V5/V6 so RANH mảnh** (tên trong mỗi mảnh đã sắp xếp); thứ tự trong mảnh do V4 đo. Nhờ vậy đột biến v4 chỉ phá V4.
4. **Đột biến c phá 13 khoá**, rộng hơn câu "V4–V10 lẫn V31" ở §4b: V11 và các vế cổng nhiều-mảnh cũng cần ≥ 2 mảnh.
5. **Nhánh BUNDLE của V31** chỉ được `bundle_fragment_check` chạy tới (gói giải nén); ma trận đột biến chạy ở topology DEV.
6. Lịch sử nhánh có 7 commit vì đặc tả đi r1 → r8 trong lúc thi công; commit `f05ae54` sửa `release.py` theo cách đọc V28
   của r7, commit `8fa006c` hoàn tác theo r8. Diff tổng `0f9aa2a..4e74fe1` của `release.py` bằng nguyên mẫu (+22/−5).

## Chưa đo

- Windows native (miễn theo Q4).
- CI GitHub trên `4e74fe1` (nhánh code chưa đẩy).
- Mọi đột biến ngoài 36 đột biến trên; nhánh BUNDLE của V31 không có đột biến riêng.
- `kiem-github` của lease (hai lớp GitHub) — `check` nói rõ nó không chạy hai lớp ấy.
