# Handoff wp433 r11 g1: BUNDLED-GATE-ORACLE-FRESHNESS

- **Packet:** `wp433`, revision 11, generation 1. `spec_packet_id: BUNDLED-GATE-ORACLE-FRESHNESS`. Issue #433.
- **Đặc tả:** `ops/specs/BUNDLED-GATE-ORACLE-FRESHNESS-r5.md` @ `5bd8463e9d9093c026a36e44e1daa3679ee4a765`, sha256 `5ae3d269551dd6791aafc33e0c498bda7103fef28e85bf6a79cb4ed4d5f26159`.
- **Lease:** `ops/leases/wp433-r11-g1-claude.yaml`, đăng ở https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7067277085.
- **Ngoại lệ E2:** https://github.com/ducthangho/tra-luat/issues/433#issuecomment-7067161081

## Ba mốc Git (protocol §3.2.1)

| mốc | OID | ghi chú |
|---|---|---|
| Immutable acceptance baseline | `29c22f7d1f92321978d4d1dff16bd80d9ea744e0` | base của đặc tả. A0 đo trên mốc này lúc soạn đặc tả |
| Continuation base | `e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8` | `origin/master` lúc cấp lease. `29c22f7d..e2f28fb` chỉ đổi 108 tệp dưới `ops/`. Băm cây của `scripts` `.githooks` `.github` `.claude` `references` `RELEASE_MANIFEST.json` `CHANGELOG.md` `VERSION` TRÙNG giữa hai mốc (đo 18:17Z) |
| Reviewed candidate | `4f648e5b784aa4e19f0385eee68cd75e69e1dd18` | nhánh `agent/wp433-r11-g1-claude`, PR #1496. Commit cuối là manifest (`4f648e5`), commit trước là W1+W2 (`dbc0de9`) |

## Thi công
1. Tạo `agent/wp433-r11-g1-claude` từ `e2f28fb`.
2. Áp `va.py`, lấy bằng `git show 5bd8463e9:ops/reviews/bundled-gate-oracle-spec-r5/va.py` (sha256 `e909f641…`). Lệnh in "da ap 11 thay the".
3. Chạy `write_bundled_modules('scripts/test_fragments','scripts')`: W2 +1/−1, W3 không đổi. Commit `dbc0de9`.
4. Chạy `python scripts/tl.py release-manifest --out RELEASE_MANIFEST.json`: W4 +5/−5. Commit `4f648e5`, là commit cuối.
5. Đẩy đúng một lần. Đọc ngược `ls-remote` ra `4f648e5b…`, khớp.

Không lệch khỏi `va.py`, nên các ca `a7_` của ma trận giữ nguyên.

## Nghiệm thu A0–A6

Lệnh: `bash do_nghiem_thu.sh <repo> e2f28fb… 4f648e5… 5bd8463e9… <ra>` (tệp trong thư mục này). Script dựng HAI clone đầy đủ trong MỘT lệnh, trên đĩa. Đầu ra nằm trong `do/`. `do/tong.txt` ghi lệnh, rc, giờ bắt đầu và giờ kết thúc của từng bước. Thời gian đo: 18:28:15–18:57:06Z ngày 21-11-2026.

| tiêu chí | kết quả | tệp |
|---|---|---|
| A0 (base `e2f28fb`) | `r11_size_only`, `r11_one_stale_ok`, `r11_missing_ok_narrow` cho `do=` rỗng; `r11_ann_empty` cho `do=V4,V5,V6,V8,V9`; `r11_duplicate` cho `do=V4,V5,V6,V8`. Ma trận rc 1, `sai=55` | `mt-nen.out` |
| A1/A2/A3 (C) | `DON_DICH: 32/32`, `TONG: 125 dot bien + doi chung, sai=0`, rc 0 | `mt-sau.out` |
| A4 (C, base cho cùng số) | `== tl selftest 1786/1786 ==` · `test-fragments-check` ok, current · bundle checker ok, `failed: []`, 20 ca · `release-verify --strict` ok, 186 == 186 · `workflow-audit --strict` fail và warn rỗng, 74 · golden ok, 20 ca · EOL `32/32 dat` · ruff `All checks passed!` · doctrine-scan, adr-song rc 0 (66/66) · `diff --check` rc 0 | `sau-*.out`, `nen-*.out` |
| A5 | name-only gồm `RELEASE_MANIFEST.json`, W1 và W2; numstat +54/−26 trên 3 tệp; chạy lại hai bộ sinh xong thì `git status --porcelain` rỗng | `sau-namestat.out`, `sau-numstat.out`, `sau-status.out` |
| A6 | `DON_DIEU: base giet 72 ca do duoc; C yeu di 0; C thieu 0`, rc 0 | `a6.out` |

Băm hiện vật dùng khi đo (`do/hv-bam.txt`): `ma_tran_r11.py` `9314f531…`, `doi_chieu_don_dieu.py` `95671804…`. Cả hai khớp README của `ops/reviews/bundled-gate-oracle-spec-r5/`.

## Nợ và P3 đã biết
- **`bundled-gate-oracle-to-hop` (P2, Q7):** 13 ca `no_` trong ma trận.
- **RV5-F1:** bốn đột biến sống trên cả hai cây (m07, m09, m10, m15). Nên thêm vào nợ khi đóng nợ.
- **RV5-F2:** `gan.setdefault(k, literal_eval(...))` tính giá trị trước khi kiểm. Base văng y như vậy, nên không phải hồi quy.
- **RV5-F3:** §7 đặc tả ghi "chín chốt", A3 có mười. Răng của phần mở rộng V8 được đo gián tiếp qua các ca `r11_rv4_s*`.

## Review và CI trên exact head `4f648e5` (cập nhật 19:36Z 21-11)

**CI GitHub** (PR #1496): 26 check run, 25 thành công, 1 bỏ qua (`gate-packet-loop-manh`, bỏ qua theo điều kiện của workflow), 0 đỏ.
- CI chạy trên merge `bac598d`, có cha là `e2f28fb` và `4f648e5`.
- Cây của `bac598d` là `33f7b418…`, TRÙNG cây của C.

**Codex lượt 1** (`launcher.py run` `4341bdc9`): model `gpt-6.2-sol`, effort `xhigh`, cả hai đo được (`DO_DUOC`); chạy 1700 s.
- Kết luận: `changes_requested`, chỉ một finding chặn là R11-A4 (P2).
- R11-A4 là lỗ BẰNG CHỨNG A4, không phải lỗi mã: trong sandbox có `.git` chỉ đọc gắn lên thư mục tổ tiên của `TMPDIR`, nên ba cổng đỏ y hệt nhau trên base lẫn C.
- Các tiêu chí A0–A3, A5, A6 đạt. 13 hướng săn không có hồi quy. R11-C1..C4 là nợ P3 theo Q7.
- Hồ sơ: `ops/reviews/bundled-gate-oracle-freshness-pr1496/luot1/`.

**Codex lượt 2, xác minh** (`873e0a10`): effort `xhigh`, chạy 350 s.
- Kết luận: `approve`. R11-A4 **ĐÃ VÁ THẬT**, dựa trên log CI trên cây trùng C và số đo của executor ngoài sandbox.
- 0 finding P0–P2 còn mở.
- Hồ sơ: `ops/reviews/bundled-gate-oracle-freshness-pr1496/luot2/`.

**Budget đã dùng:**
- Codex review PR: 2/10 (ADR-0055).
- CI Ubuntu: 1/3.
- Windows native: 0 (miễn).
- Phiên executor: 1/2.

## Chưa làm
- Chủ kho audit `human_exact_head_audit.v1` trên `4f648e5` và duyệt merge.
- Rút hạn lease sau land.

Không merge, không deploy, không ghi LIVE.
