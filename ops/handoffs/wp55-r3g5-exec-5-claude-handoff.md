# Handoff §7 — wp55 revision 3, generation 5, EXECUTOR `claude`, attempt 2/3

```yaml
schema_version: 1
event: executor_handoff
packet_id: wp55
packet_issue: 55
mission_issue: 54
revision: 3
generation: 5
phase_key: F3-03
lease_id: wp55-r3-exec-5-claude-20260815
role: executor
provider: claude
reviewer_provider_required: codex        # §8 — executor là claude

spec_path: ops/specs/wp55-r3-spec.md
spec_branch: ops/wp55-r3-spec
spec_hash: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
spec_hash_verified: true                 # sha256sum khớp, đo 2026-08-15T04:45Z
prompt_sha256: b91b5fe54a7a92814c3857a409ed15ac28eec8a97babdb053fb775bd6ca02cbd
prompt_sha256_verified: true

base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
reviewed_sha_start: e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8   # head XUẤT PHÁT, khớp lease
head_sha: 38194b5c2a934b8f09a2e647a583f254c86d4152

branch_intended: claude/wp55-r3g5-f3-03  # KHÔNG đẩy được — xem §COLLISION
branch_actual: claude/wp55-r3g5-f3-03-alt-38194b5
pull_request: null                       # CHƯA mở — chờ chủ kho gỡ va chạm nhánh
evidence_branch: ops/wp55-r3g5-exec-5-evidence

status: work_complete_delivery_blocked
blocked_on: branch_collision_two_live_executors
```

---

## 1. Bảy finding đã đóng · finding thứ TÁM không đụng tới

Verdict lượt 6 (`codex`, lease `wp55-r3-review-6-codex-20260814`, neo `e6e4b73`) nêu TÁM finding.
Bản gốc verdict đã đọc từ `ops/wp55-r3-review-6-codex-verdict.md` trên nhánh `ops/wp55-verdict-6`
(sha256 `d34f5310eeb8f8871df364ac1161c1172c023a16f5398ca52252b53147382d53`, 10677 byte).

**Nhánh ấy XUẤT HIỆN GIỮA PHIÊN**: lúc 04:45Z quét `refs/heads/ops/*` KHÔNG có nó, lúc 04:53Z có.
Bốn lượt trước không đọc được bản gốc là vì lý do này, không phải vì bỏ qua.

| # | finding | severity | trạng thái |
|---|---|---|---|
| 1 | `review-transition-bypasses-record-review` | P1 | ĐÓNG |
| 2 | `void-reviewing-accepts-attempt-zero` | P1 | ĐÓNG |
| 3 | `doctrine-html-quoted-angle-bypass` | P1 | ĐÓNG |
| 4 | `doctrine-common-term-fail-open` | P1 | ĐÓNG |
| 5 | `ac18-mutation-not-per-class` | P2 | ĐÓNG |
| 6 | `ac19-false-positive-matrix-incomplete` | P2 | ĐÓNG |
| 7 | `ac14-codepage-void-attempt-uncovered` | P2 | ĐÓNG |
| 8 | `ac20-archive-tree-suite-not-self-contained` | P2 | **KHÔNG ĐỤNG** — `spec_revision_required`, chủ kho chốt hoãn sang revision 4 |

Cả bốn P1 đã được **tái lập ĐỘC LẬP** trên `e6e4b73` trước khi vá (probe 5/11), không đọc chay verdict.

## 2. TÁM CON SỐ — bốn ma trận, cùng dụng cụ, trước/sau

Dụng cụ giữ NGUYÊN giữa hai lần đo. Ba probe đầu là probe của generation 4, không sửa một byte.

| ma trận | dụng cụ | TRƯỚC (`e6e4b73`) | SAU (`38194b5`) |
|---|---|---|---|
| **lọt** | `probe-doctrine` (40 ca g4) + 6 ca chiều-lọt của probe P1 | **43/46** | **46/46** |
| **bắt-oan** | `probe-oan` (15 ca g4) + 2 ca chiều-tha của probe P1 | **17/17** | **17/17** |
| **lease** | `probe-lease` (28 hình dạng) | **28/28** | **28/28** |
| **codepage** | lệnh con có stdout được ma trận suite phủ | **10/11** | **11/11** |

Ba ca lọt hụt lúc TRƯỚC, đúng bằng ba probe của verdict:
`mer<span title=">">ged:…` rc=0 · `## Người có thẩm quyền` rc=0 · `Người có thẩm quyền` rc=0.
Lệnh con thiếu ở ma trận codepage: `void-attempt`.

## 3. KHÔNG LÙI — chứng minh bằng byte, không bằng lời

Ba probe generation 4 chạy lại trên bản đã vá cho output **KHÔNG ĐỔI TỪNG BYTE** (`diff` rỗng):

```text
probe-doctrine  40/40  · LỌT: không · BẮT OAN: không     diff TRƯỚC/SAU: rỗng
probe-oan       15/15  · BẮT OAN: không                  diff TRƯỚC/SAU: rỗng
probe-lease     28/28  · LỌT/TRACEBACK/BẮT OAN: không    diff TRƯỚC/SAU: rỗng
```

⇒ 18 lớp doctrine và 16 hình dạng lease đóng ở generation 4 **vẫn đóng**.

## 4. Gate — rc đọc TRỰC TIẾP từng lệnh, không qua pipe

| lệnh | kết quả |
|---|---|
| `packet_loop_test.py` (nhánh) | nền **136/136**, **34 đột biến**, `TỔNG: ĐẠT`, rc=0 |
| `doctrine-scan --root .` | rc=0, sạch 4 tệp |
| `tl.py --selftest` | **1696/1696**, rc=0 |
| `doc-claims-check --strict --json` | `flags=[]`, rc=0 |
| `release-verify --strict --json` | `ok=true`, `checked_file_count=179`, `failed=[]`, `extra_files=[]`, rc=0 |
| `golden-test` (không `--write`) | rc=0 |
| `eol_policy.py --all --json` | `scanned=304`, `violations=0`, rc=0 |
| `release-bundle` ×2 head + ×1 `fbe5ab9e` | **cả BA** `20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590` |
| `git diff --name-status fbe5ab9e..38194b5` | **đúng 6 tệp**, trùng khít `write_set` |

### AC 20 — cây ĐÃ MERGE, neo SHA BẤT BIẾN

`MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7` (fetch lúc 06:10Z; verdict lượt 6 đo trên
`3d2c52d`, master đã tiến từ đó).

```text
git archive $MASTER | tar -x -C $merged                      rc=0
git diff --binary fbe5ab9e..<head> | git -C $merged apply     rc=0
doctrine-scan --root $merged                                  rc=0, sạch 4 tệp
GIT_DIR="$PWD/.git" packet_loop_test.py trên $merged          rc=0
```

**KHAI THẲNG:** có dùng `GIT_DIR` trỏ object store kho nguồn. Công thức nguyên văn trong spec
KHÔNG mang điều kiện ấy và chạy nguyên văn thì suite đỏ — đó chính là finding thứ tám, đã hoãn
sang revision 4. Không khai suông rằng "công thức spec chạy được".

Kết quả trên cây ĐÃ MERGE **trùng khít** với trên nhánh:

```text
                     nền        đột biến   TỔNG    rc
nhánh 38194b5        136/136    34/34      ĐẠT     0
cây merge 2531366    136/136    34/34      ĐẠT     0
```

Hai phép đo nói **cùng một chuyện** — đó là điều AC 20 đòi. Để đạt được điều này phải loại nhóm ca
ĐỌC CÂY THẬT (`doctrine_scan_repo_that_sach`) khỏi vế "ca ngoài tập vẫn XANH": dưới đột biến
`noi_dung_mot_minh_thanh_co_chua`, ca ấy ĐỎ trên cây merge (vì `CLAUDE.md` của master có câu văn
xuôi ở dòng 82–83) mà XANH trên nhánh. Khác biệt đến từ CÂY, không từ chốt đang đo. Ca ấy vẫn chạy
đầy đủ ở vòng nền.

## 5. Ba chỗ phép đo HAI VẾ bắt được mà bản một-vế không thấy

Runner cũ chỉ chạy đúng tập `phai_chet` do mutant tự khai. Runner mới chạy TRỌN suite cho từng
đột biến và đòi cả hai vế: ca đích ĐỎ **và** mọi ca ngoài tập vẫn XANH.

1. **Bốn đột biến cũ khai THIẾU tập giết** — `same_failure_2_thanh_99` giết 2 (khai 1);
   `noi_danh_sach_cho_phep_chua_ten_gia_mao` 2 (khai 1); `tach_begin_attempt_khoi_ham_chung`
   8 (khai 7); `tra_ve_fail_open_thieu_lease` 4 (khai 1).
2. **`ha_NFKC_ve_NFC` khai SAI một ca** — nó liệt `ac18_nfkc_ligature_ff` vào tập phải-chết
   nhưng ca ấy KHÔNG chết: `"ﬀ".casefold()` cũng cho `"ff"`. Verdict lượt 6 đã nêu đúng chỗ này.
3. **PHÁT HIỆN MỚI, ngoài verdict — ca `nbsp_phu_hai_lop` KHÔNG chứa ký tự NBSP nào.**
   `cat -A` trên `e6e4b73` cho `local controller` với khoảng trắng THƯỜNG. Nó khớp cụm cấm
   nguyên văn ⇒ đo ca NỀN, không đo lớp chuẩn hoá nào. Đó mới là lý do CƠ HỌC khiến "không đột
   biến nào giết được nó", chứ không phải "phủ hai lớp" như chú thích cũ giải thích.
   **Cùng loại lỗi với ca khai `Cf` mà không có ký tự `Cf`** — verdict bắt được ca kia, ca này lọt.
   Nay viết bằng escape ` ` để mắt thường thấy được.

Ngoài ra, đo trực tiếp cho thấy chú thích cũ khai "NBSP phủ HAI lớp" là **sai số lớp**: thực tế
NBSP đi qua BA đường (NFKC · `_PHAN_CACH` · `str.split()`), và gỡ riêng phép thu gọn khoảng trắng
giết **0** ca. Lớp `thu_gon_khoang_trang` nay có ISOLATE thật là ca TAB.

## 6. Bảng đột biến — hai loại, khai rõ loại nào

- **30 đột biến PHẪU THUẬT** (hai vế): giết đúng tập đã khai, mọi ca còn lại vẫn XANH.
- **4 đột biến MỘT VẾ**, mỗi cái kèm lý do đo được vì sao không thể phẫu thuật:
  `init_tu_cap_lease_nhu_bug_goc` (phá chính bộ đồ gá, 41 ca chết),
  `bo_ca_hai_duong_gap_tuong_thich` (39), `bo_casefold` (33),
  `bo_ca_ba_duong_phu_nbsp` (NBSP ba lớp phủ chồng).

Thêm hai chốt cơ học biến lời hứa thành mã thoát:
`AC 18` — mọi ca lớp lách (42) phải có ít nhất một đột biến;
`AC 19` — mọi lớp ở chiều lọt (17 lớp) phải có ít nhất một ca bắt-oan, kèm bảng ánh xạ LỚP→CA.

## 7. Việc cho phiên sau (successor §7)

1. **Va chạm nhánh — CẤP BÁCH.** Xem §COLLISION dưới đây. Chủ kho phải quyết trước khi có PR.
2. **Bất đồng diễn giải AC 2 ↔ AC 19** giữa hai bản (§COLLISION mục 3). Đây là câu hỏi **mức
   spec**, executor không tự nới — cần chủ kho hoặc reviewer chốt.
3. **`ops-publish-lease.yml` chỉ trigger trên `ops/leases/**`** nên handoff/heartbeat dưới
   `ops/handoffs/**` KHÔNG bao giờ tới #55. Đây là lý do cơ học của "ghi vào kho rồi mà vẫn im
   lặng" suốt bốn lượt. Sửa là mở rộng `paths` — việc của một packet riêng, không nới ở đây.
4. **Finding thứ tám** vẫn treo, chờ revision 4.
5. **Mutex phiên**: đã có nhánh `ops/successor-packet-session-mutex` trong kho — va chạm lần này
   là bằng chứng vận hành cho đúng packet đó.

## COLLISION — HAI EXECUTOR CÙNG SỐNG TRÊN MỘT LEASE

Đo lúc `2026-08-15T06:21:52Z`, `git ls-remote` + `git log`:

```text
refs/heads/claude/wp55-r3g5-f3-03  →  2cccf1ea61859f1b051adb646294ead285dac39c
  author/commit date : 2026-08-15T05:27:16+00:00
  subject            : "wp55 r3g5: đóng 7 finding lượt 6 — 4 P1 ở tầng + 3 P2 bộ test tự chứng minh"
  parent             : e6e4b73  (CÙNG head xuất phát)
  đổi                : ĐÚNG 6 tệp write_set
```

Phiên này bắt đầu 04:45Z và commit `ecf1980` lúc ~06:05Z. Nhánh kia được đẩy 05:27Z — **trong khi
phiên này đang chạy**. Hai phiên executor cùng lease `wp55-r3-exec-5-claude-20260815`.

**Đã KHÔNG force-push** (lease cấm, và đó là hành vi phá huỷ). Công việc của phiên này đẩy lên
`claude/wp55-r3g5-f3-03-alt-38194b5`, **KHÔNG phải** nhánh packet, và **không mở PR** — để chủ kho
quyết, không phải để tranh chỗ.

### Ba khác biệt đo được giữa hai bản

Đo bản kia bằng **cùng bộ probe**, không đọc chay:

| | `2cccf1ea` (phiên kia) | `38194b5` (phiên này) |
|---|---|---|
| probe P1 (11 ca) | **10/11** | **11/11** |
| ca lệch | `F4e` — `Chỉ người có thẩm quyền mới cấp được lease; phiên worker thì không.` → **rc=6** | → **rc=0** |
| tệp đụng | 2 (`packet_loop.py`, `packet_loop_test.py`) | 3 (thêm `work-packet/SKILL.md`) |

**KHÔNG phải họ cẩu thả.** Họ CHUYỂN CÓ CHỦ ĐÍCH ca `oan_term_giua_cau` từ tập BẮT-OAN sang tập
LỌT (`cum_don_cau_van_xuoi_mot_dong`), có ghi lý do: AC 2 đòi bơm một cụm trong danh sách là phải
ĐỎ, và một adapter viết câu ấy đang chép nội dung bảng vai trò chứ không trỏ về protocol.

Hai cách đọc, cả hai đều có căn cứ trong spec:

- **Bản kia:** AC 2 thắng — cụm trong danh sách xuất hiện ở adapter là ĐỎ, trừ đúng ca văn xuôi
  ngắt dòng kể lại kết quả đo mà AC 19 nêu đích danh.
- **Bản này:** AC 19 rộng hơn thế, và `oan_term_giua_cau` là **ca đã ĐÓNG ở generation 4** —
  lease lượt này viết thẳng *"lùi một ca là hỏng, không phải đánh đổi"*. Verdict lượt 6 cũng
  **không** yêu cầu lật ca ấy: ba probe của finding 4 chỉ nói heading trần, dòng trần, ô bảng.

Đây là **câu hỏi mức spec**, nên phiên này KHÔNG tự chốt và cũng không sửa spec (đổi băm là vô
hiệu chính lease). Trình cả hai để chủ kho / reviewer `codex` quyết.

### Đường ghi #55 — 403 lượt thứ NĂM, cơ chế đã truy ra

```text
api.github.com/.../pulls/115           HTTP 403   (thân là văn bản proxy Anthropic, không phải GitHub)
api.github.com/.../pulls/115/reviews   HTTP 403
WebFetch github.com/.../pull/115       HTTP 404   (kho riêng tư)
git clone / fetch / ls-remote / push   rc=0
```

1. **Không phải thiếu token** — `GITHUB_PAT`, `GH_TOKEN`, `GITHUB_TOKEN` đều có mặt trong
   container (chỉ kiểm sự tồn tại, không đọc giá trị, không dùng).
2. **MCP `github` chưa bao giờ nạp** — `.mcp.json` nằm trên `master`, nhưng phiên khởi động ở
   `/home/user` KHÔNG có kho; kho chỉ được gắn giữa phiên, khi danh sách MCP đã chốt.
3. **`push → Actions → API` có thật nhưng không phủ handoff** — workflow chỉ trigger trên
   `ops/leases/**`. Executor KHÔNG viết lease giả để mượn đường đăng: làm vậy là lách đúng cái
   cổng uỷ quyền mà packet này đang dựng.

⇒ **Cần người có quyền đăng hộ handoff này lên #55.**

---

## BỔ SUNG 06:45Z — verdict lượt 7 đã có, và bản này CŨNG hở một ca

Fetch lúc `2026-08-15T06:41Z` thấy thêm `ops/wp55-r3-review-7` chứa
`ops/reviews/wp55-r3-review-7-codex-verdict.md` (commit `4ec5577`, 06:06:47Z):
**verdict `changes_requested`, `reviewed_sha: 2cccf1ea…`** — tức guồng đã coi head của
phiên KIA là bản giao generation 5 và đã soi nó. Phiên kia sau đó đẩy tiếp hai commit
gắn nhãn `g6` lúc 06:29 và 06:35. **Không có lease `exec-6` nào trong kho.**

⇒ Lease generation 5 của phiên này trên thực tế **đã bị vượt qua**. Nói thẳng như vậy,
không tranh chỗ.

### Đo bản của mình bằng CHÍNH probe của verdict lượt 7

Finding P1 lượt 7 (`doctrine-line-break-exemption-bypasses-non-prose`) nói miễn trừ ngắt
dòng rộng hơn AC 19. Chạy đủ bốn probe của nó trên CẢ HAI bản:

| probe | bản này (`38194b5`) | bản kia (`2cccf1ea`) | đòi |
|---|---|---|---|
| `## Chỉ người có` / `## thẩm quyền` | **rc=0 LỌT** | rc=0 LỌT | 6 |
| `- Người có` / `  thẩm quyền` | rc=6 bắt | rc=0 LỌT | 6 |
| `<table><tr><td>Người có` / `thẩm quyền</td></tr></table>` | rc=6 bắt | rc=0 LỌT | 6 |
| code fence `Người có` / `thẩm quyền` | rc=6 bắt | rc=0 LỌT | 6 |

**Bản này đóng 3/4, bản kia 0/4 — nhưng bản này VẪN HỞ ca heading tách dòng.** Không giấu:
đây là cùng họ với finding 4 của lượt 6, và nó nằm trong `write_set`, tức về nguyên tắc vá được.

### Vì sao KHÔNG vá ngay trong lượt này

1. Finding lượt 7 neo `reviewed_sha 2cccf1ea` — head của phiên khác, dưới một lease review
   mà phiên này KHÔNG cầm. Vá theo nó là tự nới phạm vi.
2. Vá đúng phải sửa ranh giới "miễn trừ chỉ dành cho VĂN XUÔI", và điều đó đụng thẳng ca
   canonical của AC 19 (`CLAUDE.md` master dòng 82–83, vốn nằm trong một mục có gạch đầu
   dòng). Sửa một chiều rồi đo một chiều **chính là** cái bẫy lease này cấm — và là cách
   generation 4 hỏng. Làm đúng phải đo lại cả bốn ma trận, không kịp gói trong lượt này.
3. Lease cấm tự mở write set cho phát hiện ngoài spec: **xuất successor §7 rồi dừng**.

### Successor §7 — đề xuất cho lượt sau

`doctrine-line-break-exemption-only-for-prose`, P1, `code_fix_required`:
thu miễn trừ ngắt dòng về đúng bề rộng AC 19 — chỉ tha khi các dòng liên quan là VĂN XUÔI
(không mang dấu cấu trúc: `#`, gạch đầu dòng, `|`, fence, thẻ HTML). Bắt buộc đo CẢ BỐN
ma trận trước/sau, và ca `CLAUDE.md` master dòng 82–83 phải VẪN XANH.
