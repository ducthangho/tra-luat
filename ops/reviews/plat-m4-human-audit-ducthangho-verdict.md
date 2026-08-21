# AUDIT CỦA NGƯỜI — `PLAT-M4` (#194 / PR "#204"), neo `a9e021d`

**Tệp này là BẢN CHIẾU, không phải nguồn có thẩm quyền — và chiều ấy NGƯỢC với mọi
verdict khác trong thư mục này.**

Với verdict của một mô hình, nguồn có thẩm quyền là tệp có băm trong kho, còn comment
trên GitHub chỉ là bản chiếu. Với một lượt `human_audited` thì ngược lại: thứ §8 đòi là
**danh tính bền trên GitHub** của người audit, mà danh tính ấy chỉ tồn tại ở phía GitHub.
Một tệp trong kho không mang được nó — bất kỳ phiên nào có quyền ghi cũng tạo được tệp
này. Nên **nguồn có thẩm quyền là comment `5367254650`**; tệp này chỉ để tra ngoại tuyến.

- Người audit: `ducthangho` (`author_association: OWNER`)
- Đăng lúc: `2026-08-21T08:16:14Z`
- Nguồn: https://github.com/ducthangho/tra-luat/pull/204#issuecomment-5367254650

---

## Nguyên văn

## human_audited — PLAT-M4 (#194), người audit: @ducthangho

Reviewed commit: a9e021de28d03e7edc9077b42678f6af22a3b684

Tôi tự đọc `git diff origin/master...a9e021d -- .claude/dev/` (2 tệp, +184/−19 và
+359/−6) và đặc tả `ops/specs/plat-m4-v0.md`. Ba chốt tôi soi trực tiếp:

1. `_do_mcp_endpoint` — không nhánh từ chối nào mang dữ liệu từ `url` ra mô tả,
   kể cả `scheme`.
2. `_ = p_ep.port` nằm TRONG `try` quanh `urlsplit`, nên port phi số rơi vào
   nhánh `khong_do_duoc` trước khi dựng `Request`.
3. `_doc_mcp_json` chỉ in `scheme://host`, không nội suy `url` thô.

Bằng chứng máy tôi đối chiếu, không tự chạy lại: `gate` success trên **cả
ubuntu lẫn windows** tại đúng head này (run 32460168667, 0 bước lỗi);
`launcher_test` 142/142; `--dot-bien` 139/139 với hai mutant mới giết 1/1 đúng
ca đích; `tl selftest` 1698/1698.

### Ba điều tôi chấp nhận TƯỜNG MINH khi ký

- **R2 hoãn, chưa vá.** Hai đột biến còn sống (`timeout`, `jsonrpc`). Căn cứ:
  cùng lỗ có sẵn ở `_do_rest_github` trên master ⇒ nợ NỀN, không phải hồi quy
  của packet. Nợ `mcp-probe-thieu-mutant-canh-timeout-va-than-JSONRPC`, cò trả
  theo write set, ghi ở `no_hoan_co_can_cu` trong biên nhận lượt 3.
- **Vượt trần kích thước `sensitive`** (ADR-0044 ≤300 dòng thêm; thực tế +543).
  Chấp nhận có ghi, không tách packet — tách sau ba vòng review sẽ làm mất hiệu
  lực bằng chứng đã có.
- **Head cuối chưa qua nhà cung cấp thứ hai.** `cross_approved` không đạt được:
  bộ lọc nội dung của nhà cung cấp cắt lượt chạy, đo được là cấu trúc (hai mẫu
  dương + một đối chứng âm). Chữ ký này THAY cho nó, không cộng vào nó.

`review_class` đúng của packet là **`sensitive`**, không phải `systemic` như
`ops/specs/plat-m4-v0.md:11` khai — đã đính chính ở
`ops/DINH_CHINH_REVIEW_CLASS_PLAT_M4.md`.

VERDICT: approve
Reviewed commit: a9e021de28d03e7edc9077b42678f6af22a3b684
