Phát hiện 1 — URL có credential nhúng vẫn được probe

- Bằng chứng đo được:

```text
'file:///etc/passwd' => ('khong_do_duoc', "`url` khong phai http(s): 'file:///etc/passwd'", False) urlopen_calls= []
'ftp://x/y' => ('khong_do_duoc', "`url` khong phai http(s): 'ftp://x/y'", False) urlopen_calls= []
'gopher://x/y' => ('khong_do_duoc', "`url` khong phai http(s): 'gopher://x/y'", False) urlopen_calls= []
'http://user:REVIEW_SECRET@127.0.0.1/mcp' => ('mo', 'HTTP 200', True) urlopen_calls= [('http://user:REVIEW_SECRET@127.0.0.1/mcp', 'user:REVIEW_SECRET@127.0.0.1', 'POST', 8.0)]
'https://user:REVIEW_SECRET@example.test/mcp' => ('mo', 'HTTP 200', True) urlopen_calls= [('https://user:REVIEW_SECRET@example.test/mcp', 'user:REVIEW_SECRET@example.test', 'POST', 8.0)]
```

Lệnh là script Python gọi `_do_mcp_endpoint()` với `urlopen` giả và ghi lại request. Credential xuất hiện nguyên văn trong cả `req.full_url` và `req.host`.

- Mức: **P2**.
- Invariant bị cắt: probe chỉ được chấp nhận URL mạng thuộc cấu trúc cho phép và không đưa bí mật từ cấu hình vào URL/network stack. Kiểm tra tiền tố `http(s)://` chưa phải allowlist cấu trúc; nó vẫn nhận `userinfo`.
- Gợi ý vá: parse bằng `urllib.parse.urlsplit`; chỉ nhận `scheme in {"http", "https"}`, `hostname` hợp lệ, đồng thời từ chối nếu `username` hoặc `password` khác `None`. Bổ sung ca `http://user:secret@host/...` và `https://...` khẳng định `khong_do_duoc` và `urlopen` không được gọi.

Các phép đo còn lại đạt:

```text
142/142 ca DA CHAY QUA (tong 143, bo qua 1, hong 0)
SUITE_RC=0
DOT BIEN: 132/132 dat  (1 khong do duoc tren nen nay)
MUT_RC=0
DOCTOR_RC=0 JSON_RC=0 TOKEN_LEAK=NO
```

`t115` còn răng:

```text
mcp_endpoint_tinh_vao_LAM_DUOC_VIEC OK  giet 2/2: t115_duong_MCP_phai_duoc_DO_va_KHONG_duoc_tinh_la_lam_duoc_viec, t143_mcp_endpoint_do_DAU_KIA_cua_day_va_KHONG_duoc_tinh_la_lam_duoc_viec
```

Không có số ca trùng; diff đúng hai tệp. Lời khai nền `MO_DUN_PY` được xác nhận: base đã có bốn chỗ, delta không sửa chúng. Chốt cuối: `git status --short` rỗng và HEAD vẫn là exact head yêu cầu.

VERDICT: changes_requested
Reviewed commit: 5813fc450efe3cb349b082044708d27a589b69fb
