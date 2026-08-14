# wp55 r3g4 · PHỤ LỤC 1 — đính chính con trỏ verdict lượt 5, và kiểm lại theo BẢN GỐC

Lease `wp55-r3-exec-4-claude-20260814` · attempt 1/3 · head `e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8`.

## 1 · Con trỏ chết đã thay bằng bản gốc — đã xác minh

| mục | kết quả đo |
|---|---|
| `POSTED-COPY.md` trên `ops/wp55-r2-review-5-verdict` | **đã xoá** ở `7b6d535` (`git show` rc=128) |
| bản GỐC `ops/wp55-verdict-5:ops/reviews/wp55-r2-review-5-codex-verdict.md` | `git show` rc=0 |
| sha256 | `d1d04452d0ab2df917c1f1f9aa46d52aa554fdf497480ab176780a462a43623e` ✓ khớp |
| byte | `4392` ✓ khớp |
| prompt nhiệm vụ | `dd9f01cc…` ✓ **KHÔNG đổi** |
| spec revision 3 | `e321f811…` ✓ **KHÔNG đổi** |

**Một cái bẫy đã sập vào chính tôi, ghi lại vì nó là doctrine:** lần kiểm đầu tôi đọc
`origin/ops/wp55-r2-review-5-verdict` từ **ref cục bộ CŨ** (`3af03a4`, fetch từ đầu phiên)
và thấy POSTED-COPY vẫn còn — kết luận ngược với đính chính. Chỉ sau `git fetch` lại
(`3af03a4..7b6d535`) mới thấy đúng. **`rc` đọc từ một remote-tracking ref chưa fetch lại
thì nói dối y như `rc=0` của một pipe.** Phải fetch trước khi đo, không chỉ trước khi đọc.

## 2 · Kiểm lại HAI finding của bản gốc bằng CHÍNH fixture và lệnh của nó

Bản gốc nêu **hai** P1 (`merged-tree-doctrine-false-positive`, `partial-lease-authority-bypass`).
P1 thứ ba trong lease (`doctrine-rendering-bypass-nfkc`) đến từ `chatgpt-codex-connector[bot]`
trên PR #92, không từ verdict này — hai nguồn khớp nhau, không mâu thuẫn.

| finding | verdict đo tại `546ecf9` | đo lại tại `e6e4b73` |
|---|---|---|
| merged-tree (lệnh nguyên văn của verdict) | `rc=6`, `CLAUDE.md:82` | **`rc=0`, sạch, 4 tệp** |
| partial-lease (fixture nguyên văn: chỉ `expires_utc`) | `rc=0`, "bắt đầu lượt 1/3 — state running" | **`rc=8`**, nêu đích danh 3 khoá thiếu |
| `lease` là chuỗi | `rc=1` + **Traceback** | **`rc=8`, traceback=NO** |
| `expires_utc` là số | `rc=1` + **Traceback** | **`rc=8`, traceback=NO** |

`doctrine_entity_probes` của verdict (decimal/hex/named/no-semicolon/nbsp/soft-hyphen = 6,
double-encoded `&amp;#58;` = 0) trùng khớp với các ca `C1–C5`, `B5`, `A9` trong danh sách
đóng của tôi — hai phiên độc lập đo ra cùng một bảng.

## 3 · Đối chiếu số gate với bằng chứng của verdict

| gate | verdict (546ecf9) | phiên này (e6e4b73) |
|---|---|---|
| `packet_loop_test` | 54/54 · 11/11 đột biến | **109/109 · 23/23 đột biến** |
| `tl --selftest` | 1694/1696 rc=1, phải override `commit.gpgsign` mới ra 1696/1696 | **1696/1696 rc=0, KHÔNG cần override** (`commit.gpgsign=true` ở đây vẫn 1696/1696) |
| `doc-claims-check` | ok, flags 0 | ok, **flags 0** |
| `release-verify` | expected 179 · checked 179 · failed 0 · extra 0 | **expected 179 · checked 179 · failed 0 · extra 0** |
| `golden-test` | ok, cases 20 | ok, **cases 20** |
| `doctrine_scan_merged_tree` | **rc=6**, 1 finding | **rc=0**, 0 finding |

Không có gì trong bản gốc đòi sửa thêm. Bản vá đứng nguyên.

## 4 · Đường ghi GitHub — verdict CHỨNG THỰC đây là lỗi môi trường, không phải phiên im lặng

Mục `delivery` của bản gốc:

```yaml
delivery:
  pr_review: not_posted
  issue_evidence: not_posted
  reason: gh unavailable; no GitHub connector exposed; lease is read-only with empty write_set
```

Nghĩa là **phiên reviewer lượt 5 cũng không đăng được** — cùng bức tường, khác vai. Cộng
với phiên này, đó là **hai phiên liên tiếp** hoàn thành việc rồi tắc ở đúng một chỗ. Kết
luận "ba lease trước chết vì không có dấu vết sống" nên đọc lại: dấu vết không thiếu vì
phiên lười, mà vì **đường ghi bị chặn ở tầng proxy**.

Đo lại trong phiên này, 2026-08-15 02:23 giờ VN:

```text
GET  api.github.com/repos/ducthangho/tra-luat/issues/55           HTTP=403
POST api.github.com/repos/ducthangho/tra-luat/issues/55/comments  HTTP=403
{"message":"GitHub access is not enabled for this session. An org admin must
 connect the Claude GitHub App for this organization."}
git push                                                          OK
```

403 với CẢ token lẫn không token ⇒ không phải thiếu quyền của token, mà là chặn ở tầng
phiên. Đề nghị: hoặc bật GitHub App cho org, hoặc đổi điều kiện heartbeat của lease sang
**commit trên nhánh `ops/**`** — đường duy nhất còn sống, vẫn có mốc thời gian và vẫn
kiểm được, và chính là cách phụ lục này được ghi.
