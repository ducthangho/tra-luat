# Heartbeat — wp55 r3 generation 5, executor `claude`, attempt 2/3

**Lease:** `wp55-r3-exec-5-claude-20260815` · hết hạn `2026-08-16T05:00:00Z`
**Nhánh làm việc:** `claude/wp55-r3g5-f3-03`, xuất phát `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8`

## ĐƯỜNG ĐĂNG #55 KHÔNG DÙNG ĐƯỢC — đây là lượt 403 thứ NĂM liên tiếp

Đo lúc `2026-08-15T04:47Z`, đọc rc trực tiếp:

```text
curl https://api.github.com/repos/ducthangho/tra-luat/pulls/115           HTTP 403
curl https://api.github.com/repos/ducthangho/tra-luat/pulls/115/reviews   HTTP 403
WebFetch https://github.com/ducthangho/tra-luat/pull/115                  HTTP 404 (kho riêng tư)
git ls-remote / fetch / clone                                             rc=0
```

Thân 403 là văn bản của **proxy Anthropic**, không phải của GitHub:

> `GitHub access is not enabled for this session. An org admin must connect the Claude GitHub App for this organization.`

**Ba điều cần nói thẳng, vì bốn lượt trước đã mất thời gian vào đúng chỗ này:**

1. **Không phải thiếu token.** `GITHUB_PAT`, `GH_TOKEN`, `GITHUB_TOKEN` đều CÓ trong container
   (chỉ kiểm sự tồn tại, không đọc giá trị). Proxy chặn ở tầng mạng nên token không cứu được.
2. **MCP `github` không nạp.** `.mcp.json` (trỏ `api.githubcopilot.com`, `Bearer ${GITHUB_PAT}`)
   nằm trên `master`, nhưng phiên khởi động ở `/home/user` KHÔNG có kho — nên tệp ấy chưa bao giờ
   được đọc. Kho được gắn giữa phiên bằng `add_repo`; tới lúc đó danh sách MCP đã chốt.
3. **Đường `push → Actions → API` CÓ, nhưng KHÔNG phủ heartbeat.**
   `.github/workflows/ops-publish-lease.yml` chỉ kích hoạt với
   `paths: ops/leases/**.yaml|yml`. Tệp dưới `ops/handoffs/**` và `ops/evidence/**`
   **không kích hoạt workflow nào**, nên handoff của generation 4 nằm trong kho mà
   không hề tới #55. Đây là lý do cơ học của việc "ghi vào kho rồi mà vẫn im lặng".

**Việc cần người có quyền làm** (executor không được tự nới, không được tự đăng):
đăng hộ nội dung này lên #55, hoặc mở rộng `paths` của workflow sang `ops/handoffs/**`
trong một packet riêng. Executor KHÔNG viết lease giả để mượn đường đăng của
`ops/leases/**` — làm vậy là lách chính cái cổng uỷ quyền mà packet này đang dựng.

## Nhịp

| mốc UTC | việc |
|---|---|
| 04:45 | BƯỚC 0 xong — băm prompt `b91b5fe5…02cbd` KHỚP, băm spec `e321f811…ae22d` KHỚP, head xuất phát `e6e4b73` KHỚP, kho không nông, `core.abbrev=7` |
| 04:47 | đo đường ghi GitHub → 403/404 (bảng trên) |
| 04:50 | đo NỀN bốn ma trận trên `e6e4b73` — suite 109/109 + 23 đột biến; lọt 40/40; bắt-oan 15/15; lease 28/28 |
| 04:52 | probe bốn finding P1 → **5/11**, tái lập ĐỘC LẬP cả bốn finding của verdict lượt 6 |
| 04:54 | `ops/wp55-verdict-6` XUẤT HIỆN trên remote (04:45 chưa có) → đọc được BẢN GỐC verdict, BƯỚC 2 hết bị chặn |
| 05:02 | vá MỘT lượt ở tầng 4 chỗ trong `packet_loop.py`; probe P1 → **11/11**; ba ma trận g4 KHÔNG ĐỔI từng byte |
| 05:10 | sửa bộ test: ma trận codepage sinh từ parser, ánh xạ lớp→ca, runner HAI VẾ |
| 05:15 | đang đo tập giết THẬT của từng đột biến (chạy trọn suite mỗi đột biến) |

Phiên còn sống. Nếu tệp này ngừng cập nhật quá 45 phút thì coi là phiên chết.

---

## Nhịp — cập nhật 05:42Z

| mốc UTC | việc |
|---|---|
| 05:20 | ba gate độc lập XANH: `release-verify` ok=true checked=179 failed=[] extra=[]; `golden-test` rc=0; `eol_policy` scanned=304 violations=0 |
| 05:25 | `tl --selftest` **1696/1696** rc=0 — khớp số "không được lùi" của lease |
| 05:30 | `release-bundle` ×2 trên head + ×1 từ `fbe5ab9e` → **cả BA cùng** `20c89545…8590`, đúng con số lease ghi |
| 05:32 | `git diff --name-status fbe5ab9e` → **đúng 6 tệp**, trùng khít write_set |
| 05:35 | đo tập giết THẬT của từng đột biến (chạy TRỌN suite cho mỗi đột biến) |
| 05:42 | sửa xong bảng đột biến theo SỐ ĐO, chạy lại gate lần cuối |

### Ba chỗ phép đo hai-vế bắt được mà bản một-vế KHÔNG thấy

1. **Bốn đột biến cũ khai THIẾU tập giết.** `same_failure_2_thanh_99` giết 2 (khai 1);
   `noi_danh_sach_cho_phep_chua_ten_gia_mao` giết 2 (khai 1); `tach_begin_attempt_khoi_ham_chung`
   giết 8 (khai 7); `tra_ve_fail_open_thieu_lease` giết 4 (khai 1). Runner cũ chỉ chạy đúng tập
   tự khai nên phần dôi ra không bao giờ hiện.

2. **`ha_NFKC_ve_NFC` khai SAI một ca.** Nó liệt `ac18_nfkc_ligature_ff` vào tập phải-chết,
   nhưng đo ra ca ấy KHÔNG chết: `"ﬀ".casefold()` cũng cho `"ff"`, nên hạ NFKC về NFC không đủ.
   Suite vẫn xanh vì runner không đối chiếu lời khai với phép đo. Verdict lượt 6 đã nêu đúng chỗ này.

3. **Ca `nbsp_phu_hai_lop` KHÔNG chứa NBSP nào** — `cat -A` trên `e6e4b73` cho `local controller`
   với khoảng trắng THƯỜNG. Nó khớp cụm cấm nguyên văn, tức đo ca NỀN, không đo lớp nào; đó mới là
   lý do cơ học khiến "không đột biến nào giết được nó", chứ không phải "phủ hai lớp" như chú thích
   cũ giải thích. **Cùng loại lỗi với ca khai `Cf` mà không có ký tự `Cf`** — verdict lượt 6 bắt
   được ca kia, ca này lọt. Đây là phát hiện MỚI của lượt này, không có trong verdict.

Phiên còn sống.
