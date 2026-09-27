---
kieu: dac_ta_packet
packet: CI-GATE-TACH-GATE-OPS
packet_id: CI-GATE-TACH-GATE-OPS
ban: r2
trang_thai: dong_bang_khi_dang_bam
nguon_cap_viec: >-
  Chỉ thị chủ kho cho phiên Claude Code 27-09-2026: "tiếp tục nghiên cứu tối ưu CI … Hướng 2 — đo rồi rút ngắn job
  `gate` của `.github/workflows/ci.yml` … không làm yếu cổng nào". Quyết định trong phiên (AskUserQuestion, 27-09):
  vòng 1 chọn "3 job, tách cả G5 selftest"; vòng 3, sau khi đo lease thấy `ops/cong_cu_test.py` đang bị #570 giữ,
  chọn "H2a ngay: 2 job, chỉ sửa ci.yml" — tách G5 selftest để lại packet sau (H2b), làm khi #570 land.
  Ruleset: "Chủ kho thêm context trước merge". Tên job: `gate-ops`.
  r2 (Review Rescue Checkpoint sau Codex CLI lượt 2/2 trên `6f2b0f9`, verdict blocked, P2
  `spec-hua-windows-sau-land-sai-ma-tran`): chủ kho chọn "Revision r2 + 1 lượt Codex" và cho Windows "Không, ghi
  'chưa đo'". r2 CHỈ sửa lời khai Windows (§3, §10) và thêm ghi chú A1 (§6); thiết kế, write set, nghiệm thu giữ nguyên.
ghi_chu_hinh_dang: Chưa cổng nào đọc tệp này. Nó là DỮ LIỆU cho lease và cho reviewer.
---

# `CI-GATE-TACH-GATE-OPS` — tách job `gate-ops` khỏi `gate` để cắt thời gian tường của PR (bản **r2**)

- `packet_id`: **`CI-GATE-TACH-GATE-OPS`** · `revision`: 2 · `generation`: 2 (dự kiến) — r1 `93d19ef2…` bị thay bởi bản này
- `review_class`: **`sensitive`** — sửa `.github/workflows/ci.yml` (đường chính sách; `gate_lifecycle.py:68`,
  `chon_reviewer.py:46`, `ops/lease_publish.py:60` coi là nhạy cảm) và đổi cổng nào chạy trong job bắt buộc.
- `risk`: `sensitive` · `environment`: `cloud` · `depends_on`: `[]` (kế thừa hình dạng #463 GATE-TACH-JOB-CAT-CHI-PHI, đã land)
- executor: `anthropic_claude` · `claude_code` · `claude-opus-5-5`
- assurance: Codex CLI tại chỗ (`gpt-6-astra`, `xhigh`, tối đa **2** lượt theo §8) + Codex connector (advisory);
  **`human_audited`** là cổng land.
- base: `origin/master` **`5c79fa2c94b328ae3bbbef52a4cfa820fc40bc4a`** (đo 2026-09-27T09:48Z)

## 1. Phép đo nền

Nguồn: REST `actions/runs/<id>/jobs` (thời gian bước do GitHub ghi), 12 run `ci.yml` sự kiện `pull_request`,
`status=success` gần nhất (run `36292156241` … `36307099123`, đo 2026-09-27T09:3xZ), chỉ `ubuntu-latest`.

| đo | trung vị | min–max | n |
|---|---|---|---|
| job `gate (ubuntu-latest)` | **910 s** | 680–1852 s | 12 |
| job `gate-packet-loop` | ~276 s | 184–300 s | 12 |
| job `gate-registry` (chế độ nhẹ) | ~84 s | 64–90 s | 12 |

Bước nặng của `gate` (trung vị giây, n=12): G5 `cong_cu_test` **296** · lease-publish selftest **156** ·
tl selftest (lượt PR) **120** · bien-nhan v2 selftest **91** · cgroup + gate_lifecycle_test **81** ·
determinism **35** · golden **26** · don-nhanh **26** · eol-policy selftest 19. Tổng trung vị mọi bước 898,5 s.

Runner `ubuntu-latest` của kho (repo **private**, đo `private: true`) có **2 lõi logic** (`so_lop_logic: 2`,
job `108507663436`) ⇒ tách JOB (runner riêng) mới cắt được thời gian tường; song song trong job thì không.

Ruleset `bao-ve-cong-dang-lease` (id 20856202, `active`, nhánh mặc định) bắt buộc đúng hai context
(REST `rulesets/20856202`, đo 2026-09-27T09:4xZ): `gate (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`.

## 2. Thiết kế

Chuyển **nguyên văn** (tên, `run`, `env`, `if`, `shell`, cùng khối chú thích đứng trước) năm bước sau từ job `gate`
sang job MỚI `gate-ops`, giữ thứ tự tương đối của chúng:

1. `bien-nhan v2 selftest`
2. `lease-publish selftest (đo lại setup sau G5)` — giữ `env: AL_VER: 1.7.7` (t35 của `lease_publish_test.py`)
3. `don-nhanh selftest (chốt xoá nhánh)` — giữ `if: runner.os != 'Windows'` và khối `NỢ CÓ TÊN` đi kèm
4. `bo ca gate chay TRONG cgroup duoc uy quyen (Linux)` — giữ `if: runner.os == 'Linux'`, một shell
5. `gate lifecycle selftest (nen khong co cgroup)` — giữ `if: runner.os != 'Linux'` (đi cặp với 4)

`gate-ops`: `needs: chuan-bi`; `strategy` + `runs-on` + `timeout-minutes: 60` + `env` cấp job **bằng đúng** `gate`
(t161: ma trận đọc `needs.chuan-bi.outputs.os`). Bước thiết lập đứng trước năm bước trên, **chép đúng** từ `gate`:
`Force LF checkout …` (3 lệnh `git config`), `actions/checkout@v4` với `fetch-depth: 0`, `actions/setup-python@v5`
3.12, cài PyYAML + jsonschema, cài shellcheck, cài rg.

**KHÔNG** có trong `gate-ops`, có chủ đích:
- bước chạm `ops/cong_cu` (probe/selftest G5) ⇒ `loi_g5_workflow` không đòi `gate-ops` vào `JOB_G5`
  (regex `(?<![A-Za-z0-9_])cong_cu` không khớp `cai_cong_cu.sh`) ⇒ không sửa `.claude/dev/ci_dang_ky_test.py`;
- bước `cài actionlint cho G5` ⇒ số dòng `AL_VER:` trong `ci.yml` giữ **4** (t152 `launcher_test.py:5998-6000`);
  wrapper `ops/chay_lease_publish_test.sh` tự cài actionlint (dòng 22) như hiện nay;
- Ruff ⇒ `loi_ruff_ci` không áp.

`gate` giữ tên (context bắt buộc), giữ G5 selftest (t6 `cong_cu_test.py` đọc `jobs.gate`), tl selftest + tải
`gate-evidence`, doc-claims (tl_selftest r226), determinism, golden, release-*, và mọi bước nhẹ còn lại.

Ước thời gian tường (từ trung vị §1, KHÔNG phải cam kết): `gate` ≈ 910 − 380 ≈ **530 s**; `gate-ops` ≈ 380 + ~30
thiết lập ≈ **410 s** ⇒ PR ~15 → ~9 phút. Phút tính tiền mỗi lượt PR tăng ≈ thời gian thiết lập một job (~30–60 s).

## 3. Ngoài phạm vi

| thứ | lý do |
|---|---|
| tách G5 selftest (`cong_cu_test`, 296 s) sang job riêng | cần sửa `ops/cong_cu_test.py` (t6 + đột biến `t6_day_g5_sau_py_compile`) — tệp đang bị lease #570 g38 giữ (hạn 2026-09-28T09:11Z). Packet H2b sau khi #570 land |
| sửa `ci_dang_ky_test.py`, `launcher_test.py`, `session-start.sh`, `cong_cu_test.py` | thiết kế §2 tránh chạm chúng; chạm ⇒ S1 |
| sửa ruleset GitHub | phiên không có quyền và không nằm trong kho; chủ kho làm (A4) |
| `gate-registry`, `gate-packet-loop`, `chuan-bi`, `on:`, `concurrency` | không đổi; `BAM_GATE_REGISTRY` phải giữ nguyên |
| Windows trước merge | chủ kho quyết định KHÔNG cấp (27-09, rescue r2); ngân sách §7 không cấp `workflow_dispatch`. Push lên master CHỈ chạy ubuntu (`chuan-bi.outputs.os`), nên land KHÔNG tự đo Windows (xem `chua_do_duoc`) |

## 4. Write set — 1 đường

| # | đường dẫn | vì sao |
|---|---|---|
| W1 | `.github/workflows/ci.yml` | thêm job `gate-ops`, chuyển năm bước §2 |

Ngưỡng ADR-0044 (`sensitive`): ≤ 3 tệp, ≤ 300 dòng thêm. Ước: +~230 / −~190 (khối chuyển tính cả hai phía).

## 5. Mục tiêu

| # | mục tiêu | đường |
|---|---|---|
| M1 | job `gate-ops` như §2; năm bước rời `gate`, xuất hiện đúng một lần trong `gate-ops`, nguyên văn | W1 |
| M2 | không bước nào của `gate` gốc bị mất, nhân đôi (ngoài 6 bước thiết lập) hay đổi nội dung | W1 |
| M3 | mọi bộ kiểm đang đọc `ci.yml` vẫn ĐẠT, không sửa tệp nào ngoài W1 | W1 |

## 6. Nghiệm thu

| # | tiêu chí | phép đo làm ĐỎ |
|---|---|---|
| A1 | (Script đối chiếu nằm NGOÀI write set; executor đính kèm nguyên văn + sha256 vào PR, reviewer chạy lại.) Bảo toàn bước: script đối chiếu (parse YAML base `5c79fa2` và head) — tập bước không-thiết-lập của `gate` gốc == (bước không-thiết-lập của `gate` mới) ⊎ (bước không-thiết-lập của `gate-ops`), so từng dict (`name`,`run`,`env`,`if`,`shell`,`uses`,`with`); thứ tự tương đối giữ; bước thiết lập của `gate-ops` bằng đúng bản trong `gate`; khoá cấp job của `gate-ops` (trừ `steps`) bằng đúng `gate`; job khác bằng đúng base | đột biến trên bản sao: bỏ một bước chuyển · nhân đôi một bước · sửa `if` của cgroup · bỏ `env AL_VER` ⇒ script ĐỎ (4/4). Script và kết quả đột biến ghi vào PR |
| A2 | Bộ kiểm hiện có ĐẠT tại chỗ trên head: `ci_dang_ky_test.py` phần chung (`loi_g5_workflow`, `loi_ruff_ci`, `loi_vung_thiet_lap` ⇒ `BAM_GATE_REGISTRY` không đổi); `cong_cu_test.py` t6; `launcher_test.py` t152; `lease_publish_test.py` t35/t42/t161; `tl.py --selftest` r226; `actionlint` trên `ci.yml` delta = 0 so base | bất kỳ bộ nào ĐỎ trên head mà XANH trên base (đo cả hai vế cùng một lệnh) |
| A3 | CI của PR: `gate (ubuntu-latest)` và `gate-ops (ubuntu-latest)` xanh; trong log `gate-ops` có bằng chứng dương của từng bước chuyển (dòng tổng N/N với hai số bằng nhau của lease-publish, bien-nhan, gate_lifecycle_test, don-nhanh `21/21`), và cùng số ca với run nền gần nhất | bước chuyển vắng mặt/`skipped` trên ubuntu, hoặc số ca khác nền |
| A4 | Trước khi báo sẵn sàng merge: ruleset 20856202 có thêm `gate-ops (ubuntu-latest)` (chủ kho thêm), đo lại qua REST | context vắng ⇒ năm bước chuyển ra khỏi cổng bắt buộc ⇒ KHÔNG báo sẵn sàng |
| A5 | Số đo sau: thời gian `gate` và `gate-ops` trên run PR của packet, so trung vị §1 (quan sát, không phải cổng land) | — |

## 7. Ngân sách CI

`0 / 1 / 2` lượt `pull_request` (mỗi lượt = một workflow run). Mỗi lượt chạm `ci.yml` ⇒ `gate-registry` chạy ĐỦ
(`VUNG_CHUNG`, ~55–60 phút). `workflow_dispatch`: **0** trước land.

## 8. Điều kiện dừng

S1 chạm đường ngoài W1 · S2 CI đỏ vì packet · S3 hết 2 lượt Codex ⇒ Review Rescue Checkpoint, hỏi chủ kho ·
S4 push chỉ sau review tại chỗ sạch · S5 > 300 dòng thêm · S6 hết hạn lease ⇒ handoff §7.

## 9. `hinh_dang_ke_thua`

`khong_ap_dung` — không phải packet khắc phục. Tham chiếu hình dạng: #463 (tách job, cùng ma trận/`timeout`/tiền tố).

## 10. `chua_do_duoc`

- Windows: **CHƯA ĐO, và land cũng KHÔNG đo.** Ma trận (`ci.yml` job `chuan-bi`) chỉ thêm `windows-latest` khi sự kiện
  là `workflow_dispatch` hoặc PR mang nhãn `windows` — và gắn nhãn cho PR đang mở KHÔNG tự sinh lượt chạy (`on.pull_request`
  không khai `types`, nên cần cò mới: đẩy commit hoặc đóng/mở PR). Push lên master chỉ ubuntu. Người chịu: chủ kho
  (quyết định 27-09 "Không, ghi 'chưa đo'"). Điểm đo khi được cấp: một `workflow_dispatch` của `ci.yml` trên đúng SHA
  master sau land, đọc log `gate-ops (windows-latest)`: bien-nhan, lease-publish, lifecycle nền không cgroup CHẠY;
  don-nhanh, cgroup `skipped` theo `if:` (như baseline trong `gate`).
- Danh tính người ký lease (#566); effort thực tế của phiên executor.
- Thời gian thiết lập thực của `gate-ops` (ước ~30–60 s) — chỉ đo được trên run thật.
