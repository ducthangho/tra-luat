# Prompt review lượt 3 — `doctor`: đo GitHub theo đúng đường MCP

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8 cross-provider). CHỈ ĐỌC.

Nguồn có thẩm quyền của lượt này là TỆP CÓ BĂM trong kho (lease + prompt này). Comment
trên #55 chỉ là bản chiếu.

## Hai lượt trước đã xảy ra gì

| lượt | SHA | verdict | finding | đột biến reviewer báo sống sót |
|---|---|---|---|---|
| 1 | `4ff2c6bf` | changes_requested | 1×P1, 2×P2 | 2 (`M1` tên phân biệt hoa/thường, `M2` bỏ bắt lỗi JSON) |
| 2 | `fc484213` | changes_requested | 2×P2 | 2 (`M12` mất `capture_output`, `M13` mất `timeout`) |

Lượt 1 P1 bác đúng một lời khai tuyệt đối của người vá ("tiến trình con KHÔNG đo được
MCP") bằng `claude mcp list`. Lượt 2 xác nhận lời khai phạm vi đã đủ hẹp, giữ nhánh
`Connected → KHONG_DO_DUOC`, và tìm thêm hai P2.

**HAI LƯỢT ĐỀU TÌM ĐƯỢC ĐỘT BIẾN SỐNG SÓT, và cả hai lần lý do GIỐNG NHAU: bộ test đo
ĐỒ GIẢ chứ không đo HỢP ĐỒNG.** Lượt 1 vì chỉ giả `subprocess.run` mà không giả
`shutil.which`; lượt 2 vì đồ giả `run` nuốt mọi kwargs. Đó là chỗ đáng nghi nhất của
lượt này — xem mục 4.

## Lượt 3 xét gì

Bản vá mới là commit đơn `109c427`, vá hai P2 của lượt 2 và làm một việc thứ ba lớn hơn
cả hai: **đưa toàn bộ đột biến VÀO KHO**.

1. **Hai bản vá P2 có kín không?**
   - `_doc_mcp_json` nay kiểm cả GIÁ TRỊ của khoá `github` phải là object. Còn hình dạng
     nào lọt? Đặc biệt: `{"servers": {"github": {...}}}` khi `mcpServers` tồn tại nhưng
     rỗng/`null`; khoá `github` trùng nhau khác hoa/thường (`github` và `GitHub` cùng lúc);
     giá trị là object RỖNG `{}`.
   - `_suc_khoe_mcp_github` nay tách phần trạng thái bằng `rpartition(" - ")` rồi khớp
     `_RE_MCP_KHOE = r"[^a-z]*connected\b"`. **Soi kỹ chỗ này** — nó thay một danh sách
     cấm dò chuỗi con bằng một danh sách cho phép neo đầu, và đó đúng loại thay đổi dễ
     đúng-cho-ca-đã-biết mà sai cho ca chưa biết. Nghĩ ra dòng CLI làm nó phân loại sai
     theo CẢ HAI chiều: một trạng thái XẤU bị đọc thành `khoe`, và một trạng thái TỐT bị
     đọc thành `hong`. Ví dụ đáng thử: URL hoặc tên server có chứa ` - `; trạng thái
     nhiều đoạn (`Connected - 3 tools`); `Connected (stale)`; dòng có màu ANSI; CRLF.

2. **Trạng thái thứ ba mới có đúng chỗ không?** Dòng CLI không tách được `" - "` nay trả
   `khong_do_duoc` chứ không phải `hong`. Xét: đó là fail-open hay fail-close? Ở tầng tiêu
   thụ `khong_do_duoc` rơi vào `chua_chung_minh` nên `--doi-kha-dung` vẫn đỏ — kiểm lại
   bằng phép đo, đừng tin câu này.

3. **Việc đưa đột biến vào `DOT_BIEN` có thật sự mua được gì không?** Mười một mục mới,
   và một mục cũ (`github_dem_CO_MAT_gh_la_da_xac_thuc`) bị GỠ vì đoạn nó nhắm đã biến mất
   ở commit trước. Xét hai câu hỏi tách bạch:
   - Mục bị gỡ: kế thừa (`github_api_cho_gh_lat_nhan_tro_lai`) có thật sự phủ được ý định
     cũ không, hay đây là một chốt bị mất mà lời khai làm nó trông như được thay?
   - Mười một mục mới: có mục nào **giết được ca đích vì lý do SAI** không (ví dụ đột biến
     làm mã ném lỗi cú pháp/`NameError` nên ca chết vì crash chứ không vì hợp đồng)? Ba mục
     đã hiện `(JSONDecodeError)` `(AttributeError)` `(TypeError)` trong output — với những
     mục ấy, hãy nói rõ đó là oracle hợp lệ hay là chết vì crash.

4. **CHỖ ĐÁNG NGHI NHẤT — đồ giả trong `t105`.** Nay nó đòi `capture_output` `text`
   `timeout` dương. Hai lượt trước bạn đều tìm được đột biến sống sót ở đúng lớp này.
   **Tìm lượt thứ ba.** Gợi ý hướng: đồ giả có kiểm `cmd` đủ chặt không (đổi
   `["claude","mcp","list"]` thành lệnh khác thì sao); có ràng buộc gì về SỐ LẦN gọi không
   (một bản vá gọi `claude mcp list` ba lần vẫn xanh?); `Rc.stderr` không bao giờ được dùng
   — che được gì; `_k.get("timeout")` chỉ đòi > 0 nên `timeout=0.001` qua được.

5. **`gh` còn lật được nhãn không** — `_do_github_api` VÀ tầng tiêu thụ (`ok_kha_dung`,
   `--doi-kha-dung`, `chua_chung_minh`). Giữ từ hai lượt trước; đừng bỏ vì đã hỏi hai lần.

6. **Số nền.** Chạy và tự đo, đừng lấy số của người vá:
   ```
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py
   TMPDIR=/dev/shm python3 .claude/dev/launcher_test.py --dot-bien
   ```
   Người vá đo cùng lúc, cùng máy: suite master `e38b0be` **104/104**, nhánh **105/105**;
   đột biến master **61/61**, nhánh **71/71**. Đòi delta = 0 ca đỏ.

   **Lượt 2 KHÔNG chạy hết được suite** — sandbox cắt tiến trình ngay sau `t62`, chỗ các ca
   thao tác cây tiến trình. Nếu lượt này cũng vậy thì nói **KHÔNG ĐO ĐƯỢC** cho số tổng
   (đừng suy ra từ số của người vá), và chạy riêng phần đổi bằng `--lap-ca`. Nếu chạy được
   trọn thì nói rõ — chính nó là dữ liệu mới.

   Rồi **tự nghĩ ít nhất HAI đột biến** trên **bản sao tạm** và cho biết có bị bắt không.

## Ngoài phạm vi (đã biết, đừng báo lại)

- `.github/workflows/**` dùng `gh` — đúng, runner GitHub không có MCP.
- `.claude/skills/**` và `docs/**` còn lệnh `gh`; lệch với "mọi việc GitHub đi bằng MCP"
  nhưng ngoài phạm vi lượt này.
- Lời khai phạm vi của nhãn `CHUA_XAC_THUC` (agent sắp sinh vs phiên đang chạy) — lượt 2
  đã đo độc lập và xác nhận. Chỉ báo lại nếu bạn có phép đo NGƯỢC LẠI.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings   (id kebab, mức P1/P2/P3, mô tả, lệnh tái lập, kết quả đo được)
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
