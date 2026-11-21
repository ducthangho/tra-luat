# Codex review mã — PR #1496, packet wp433 r11 (BUNDLED-GATE-ORACLE-FRESHNESS)

Bạn là REVIEWER Codex độc lập (provider openai_codex, surface codex_cli), READ-ONLY đối với kho sản phẩm.
Thư mục làm việc: thư mục chứa tệp này. Kho đã clone đầy đủ ở `./kho` (không shallow), HEAD detached tại
ứng viên. KHÔNG push, KHÔNG gọi mạng, KHÔNG sửa `./kho` theo cách để lại commit; mọi bản sao, script, đột
biến phải đặt trong thư mục con MỚI của thư mục này (vd `./rv/`). Không đọc secrets. Không xoá gì ngoài
thứ bạn tự tạo.

## Định danh (kiểm trước khi làm bất cứ gì; lệch thì DỪNG và ghi vào verdict)
- reviewed_sha (ứng viên C): `4f648e5b784aa4e19f0385eee68cd75e69e1dd18`, tree `33f7b4183f408dafc029ecf860aab9857f244365`
- base (continuation): `e2f28fb39c519511a61d1fdba5b1fc8f77bb76b8`; immutable acceptance baseline: `29c22f7d1f92321978d4d1dff16bd80d9ea744e0`
- Đặc tả: `git -C kho show 5bd8463e9d9093c026a36e44e1daa3679ee4a765:ops/specs/BUNDLED-GATE-ORACLE-FRESHNESS-r5.md`,
  sha256 phải là `5ae3d269551dd6791aafc33e0c498bda7103fef28e85bf6a79cb4ed4d5f26159`.
- Hiện vật đặc tả: `git -C kho show 5bd8463e9:ops/reviews/bundled-gate-oracle-spec-r5/<tệp>` (README nêu băm).
- Lease: `git -C kho show 536dd3c603782c07d320a2c3345d0f8785bd0ec7:ops/leases/wp433-r11-g1-claude.yaml` — review_class `sensitive`.
- Handoff executor: `git -C kho show bc4fc8e:ops/handoff/wp433/r11-g1/HANDOFF.md` và `.../do/*` (đầu ra đo của executor — chỉ là LỜI KHAI, bạn phải đo lại).
- `diff.patch`, `numstat.txt` cạnh tệp này: diff base..C.
- Nguồn finding gốc: `git -C kho show 3f5641c8:ops/reviews/bundled-tach-manh-cr/luot3-codex-5293a85.txt` (F10, F11).
- Luật: `kho/docs/PROTOCOL_DA_PHIEN.md` §8, §8.3, §12, §13; `kho/docs/adr/0060-*` (severity, tìm theo lớp); `kho/CLAUDE.md`.

## Phạm vi và tiêu chí chặn (chủ kho đã chốt — đọc §7 và §9 của đặc tả, Q7 theo E1)
Packet CHỈ sửa oracle trong `scripts/test_fragments/wp433_bundled_tach_manh.py` (W1) và tái sinh hai tệp phái sinh
(W2 `scripts/tl_test_fragments_bundled.py` bằng `write_bundled_modules`; W4 `RELEASE_MANIFEST.json` bằng `release-manifest`,
commit cuối). Lớp `bundle-gate-fixture-oracle` đã mở 6 lần; chủ kho chốt phạm vi. Một finding CHẶN (P0–P2) khi và chỉ khi nó chỉ ra:
(a) một đột biến mà base GIẾT (fragment có khoá đỏ, hoặc văng) nhưng C để SỐNG — hồi quy so với base, kể cả ngoài ma trận;
(b) lỗi của mã sản phẩm hoặc C làm hỏng hành vi ngoài phạm vi (bundle/manifest sai, selftest/cổng đỏ, đổi tệp ngoài write set);
(c) tiêu chí A0–A6 của đặc tả đo sai trên C (đỏ, xanh giả, không tái lập được) hoặc C không đúng đặc tả (M1–M4, write set, `va.py`).
Đột biến sống trên CẢ base lẫn C là nợ `bundled-gate-oracle-to-hop`: ghi P3, không chặn. Ghi nhận các P3 đã biết RV5-F1..F3 (xem handoff), không báo lại.

## Việc phải làm
1. Preflight định danh ở trên (SHA, tree, băm đặc tả, băm hiện vật so README, write set khớp lease, numstat ≤ 6 tệp / ≤ 450 dòng thêm, commit cuối chỉ đổi `RELEASE_MANIFEST.json`, W1 trên C trùng byte với `va.py` áp lên base).
2. Dựng TRONG MỘT LỆNH hai clone đầy đủ từ `./kho` (`git clone --no-hardlinks kho rv/nen` checkout base; `rv/sau` checkout C), `core.abbrev 7`, `PYTHONDONTWRITEBYTECODE=1`, `TMPDIR` vào thư mục của bạn. Chạy ma trận hiện vật `ma_tran_r11.py` trên cả hai (SONG SONG, mỗi lượt ~25 phút) rồi `doi_chieu_don_dieu.py`. Kỳ vọng: C rc 0, `DON_DICH: 32/32`, `TONG: 125 … sai=0`; base đúng A0; A6 rc 0.
3. A4/A5 trên C: `python3 scripts/tl.py --selftest` (kỳ vọng 1786/1786 — so với base), `test-fragments-check --json`, `.github/checks/bundle_fragment_check.py --json`, `release-verify RELEASE_MANIFEST.json --strict --json`, `workflow-audit --strict --json`, `golden-test --json`, `.githooks/eol_policy_test.py`, ruff F trên W1; chạy lại `write_bundled_modules` + `release-manifest` thì `git status` sạch.
4. SĂN hồi quy so với base, theo lớp (ADR-0060 M2): bảng ≥ 8 HƯỚNG ĐỘC LẬP, mỗi hướng có giả thuyết, LỆNH, OUTPUT THẬT, kết luận (LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC). Đột biến của `scripts/tl_core/test_fragments.py` (generator/loader/writer) và `scripts/tl_core/release.py` (cổng), chạy trên base VÀ C bằng cùng harness của ma trận. Vùng đáng soi nhất (các lượt review đặc tả đã tìm hồi quy ở đây): đường đọc dữ liệu `_gan()` và các khoá V3–V9 trên các topology `deu`/`lech`/`lon`/`hai`; các oracle cổng V23–V27. Đừng tự soạn nội dung tấn công đường dẫn ra ngoài cây — nếu một hướng cần, mô tả bằng lời.
5. Soi diff như soi mã: tính đúng của `hong()`, `quyet()`, `v8()`, `_gan()`; có đường nào văng/return sớm làm khoá xanh giả không.

## Đầu ra — ghi TĂNG DẦN
Ghi `VERDICT.md` trong thư mục này NGAY từ đầu (khung + preflight), cập nhật sau mỗi bước, để lượt bị cắt vẫn giữ phần đã có.
Khối đầu là YAML:
```yaml
verdict: approve | changes_requested
reviewed_sha: 4f648e5b784aa4e19f0385eee68cd75e69e1dd18
tree: 33f7b4183f408dafc029ecf860aab9857f244365
packet: BUNDLED-GATE-ORACLE-FRESHNESS
lease: wp433-r11-g1-claude
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
```
Rồi: bảng phép đo (lệnh, rc, giờ UTC, kết quả); bảng săn hướng; bảng lớp (§8.3: slug, finding IDs, mức cao nhất, cách vá chung, phép kiểm đóng lớp); Findings (ID, mức P0–P3, slug, vị trí `tệp:dòng`, vì sao, hướng sửa, đột biến/phép đo khoá lại, rủi ro hồi quy). Dòng CUỐI đúng một: `KET_LUAN: approve` hoặc `KET_LUAN: request_changes`.
