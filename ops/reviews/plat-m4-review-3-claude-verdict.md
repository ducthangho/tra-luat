# VERDICT — `PLAT-M4` (#194 / PR "#204"), lượt 3. Reviewer `claude` (same-provider).

Chép nguyên văn kết luận của lượt review, lease `plat-m4-review-3r4-claude-20260821`,
neo `825e97042b86f5e200c2ab8a00b58d8642510353`.

## Chốt neo — tất cả KHỚP
- HEAD đúng neo, `git status --short` RỖNG (kiểm cả đầu lẫn cuối lượt).
- `ops/specs/plat-m4-v0.md` = `63ff22bcc2427850ddd66322ed4a5ac5dcaa03f8d242cc857d12825b601953d1` — khớp.
  Finding P1 của lượt 2 (spec vắng mặt) ĐÃ ĐÓNG.
- Delta `origin/master...HEAD`: đúng hai tệp, `+473/−25`, `git diff --check` rc=0.

## Nền dương
- Suite đầy đủ trên bản sao sạch: **142/142 ca ĐÃ CHẠY QUA** (tổng 143, bỏ qua 1 = `t62`
  fixture Windows, hỏng 0), rc=0.
- Đột biến toàn bảng: **137/137 đạt** (1 không đo được trên nền này — mutant riêng Windows).

## F2 — "URL méo vẫn làm lộ bí mật qua mô tả": ĐÃ ĐÓNG THẬT
Cả bốn đầu vào của lượt 2 (`http:///user:S@host/mcp` · `javascript:user:S@host` ·
`http ://user:S@host/mcp` · `http://?u=user:S@host`) đều `khong_do_duoc`, **0 lời gọi
`urlopen`**, **`desc_has_secret=False`**. Thêm bốn biến thể tấn công THỨ TỰ kiểm
(IPv6 hỏng · scheme-relative `//user:S@host` · scheme HOA · tab/newline WHATWG-strip):
cả bốn cũng 0 lời gọi, 0 lộ. Kiểm kê tay mọi nhánh `return`: không nhánh nào nội suy
`url`, `scheme`, `hostname` hay header.

## F3 — "test chưa khoá biên cấu trúc userinfo": ĐÃ ĐÓNG THẬT
Hai mutant lượt 2 nêu nay đều BỊ GIẾT, đo tay từng cái:
- `if ai_ep != (None, None):` → `if "@" in str(url):` — rc=1, 0/1 qua, chết đúng ở (5d).
- → `if p_ep.username:` — rc=1, 0/1 qua, chết đúng ở (5e).

## Findings

### R1 — P3 · khe VỊ TRÍ PORT chưa được đọc/kiểm
`https://host:SENT/mcp` qua hết ba chốt (không userinfo, scheme https, có hostname) →
`urlopen` ĐƯỢC gọi, sentinel vào `full_url` + `req.host` ở tầng giả. Runtime thật KHÔNG
lộ: `http.client` ném `InvalidURL` **trước khi mở socket**. Nhưng đó là chốt của NGƯỜI
KHÁC — cùng họ "công cụ tự cứu không phải chốt của ta". Gợi ý: đọc `p_ep.port` trong `try`
quanh `urlsplit`.

### R2 — P2 · hai đột biến thật SỐNG SÓT toàn suite
- **mD** `urlopen(req, timeout=timeout)` → `urlopen(req)`: 142/142, rc=0 — SỐNG SÓT. Cắt
  năng lực đã khai `probe-qua-han-ba-trang-thai`.
- **mE** `"jsonrpc": "2.0"` → `"1.0"`: 142/142, rc=0 — SỐNG SÓT. Thân handshake sai giao
  thức mà không ca nào đỏ.
Bất biến bị cắt: chính doctrine viết trong tệp test này ở fake của `claude mcp get`
(*"ĐỒ GIẢ TỰ TỪ CHỐI lời gọi lệch đặc tả — chốt TOÀN PHẦN, không opt-in"*). Fake `urlopen`
mới của `t143` nuốt mọi kwargs: cùng tệp, hai chuẩn.
Ghi chú công bằng: ứng viên `if co_ep is not True:` → `if co_ep is False:` **BỊ GIẾT** bởi
`t117`; ứng viên bỏ `.lower()` ở scheme là mutant TƯƠNG ĐƯƠNG, không tính.

### R3 — P3 · `_doc_mcp_json` nội suy NGUYÊN VĂN `url` vào mô tả nhánh dương
`.mcp.json` khai `https://user:GOCSPX-SENTINEL@host.test/mcp` → mô tả CHỨA sentinel. Hiện
KHÔNG lộ ra ngoài: caller duy nhất vứt `mt_mcp` ở nhánh dương (đã đo: chuỗi tóm tắt sạch,
`urlopen` 0 lần). Nhưng bất biến ghi ngay trong `_do_mcp_endpoint` là *"KHÔNG một nhánh nào
được mang DỮ LIỆU LẤY TỪ url"* — hàm bên cạnh vi phạm ở tầng dựng chuỗi. Khẩu súng đã nạp đạn.

### R4 — P3 · lời khai số đếm trong docstring `t143` TỰ MÂU THUẪN
Khai *"khoá TÁM điều"*, kèm *"(Điều thứ chín…)"*, rồi đoạn cuối vẫn mở đầu *"Và điều thứ
bảy…"* cho CHÍNH điều thứ chín ấy. Đối chiếu thân ca: **cả 9 điều ĐỀU CÓ phép đo thật** —
phần sai chỉ là đánh số. Cùng nhóm: chú thích bảng `DOT_BIEN` viết `t138` trong khi ca hành
vi là `t143`; `t138` nay là ca THẬT của #196 và không đo gì về mcp-endpoint.

## KHÔNG ĐO ĐƯỢC (khai, không làm tròn)
- **Windows**: suite bỏ qua `t62`, 1 mutant không đo được trên nền này.
- **Endpoint MCP thật**: mọi phép đo dùng `urlopen` giả — đo HỢP ĐỒNG, không đo đường mạng.
- **`ops/uy-quyen-194-same-provider-20260821.yaml`**: cố ý không có trong cây, không kiểm
  được từ lượt này.

## Kết luận
F2 và F3 đóng thật, có bằng chứng chạy. Không lỗ P0/P1 mới. R2 là P2 đúng lớp mà packet này
sinh ra để đóng ⇒ `changes_requested`. R1/R3/R4 là P3, vá cùng lượt được.

```
VERDICT: changes_requested
Reviewed commit: 825e97042b86f5e200c2ab8a00b58d8642510353
```
