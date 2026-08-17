# Prompt review lượt 7 — đường MCP ghép vào `_do_github` của #143

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8). CHỈ ĐỌC.

Nguồn có thẩm quyền là TỆP CÓ BĂM trong kho (lease + prompt này).

## Vì sao có lượt 7 dù lượt 6 đã `approve`

Lượt 6 duyệt `45a06e48` trên nền **`e38b0be`**. Trong lúc sáu lượt ấy chạy, **PR #143
land** và sửa CHÍNH `_do_github` theo hướng khác. Bản đang xét là **mã KHÁC trên nền
`c7ad260`** — verdict lượt 6 KHÔNG phủ nó. Đây là lượt review ĐẦU TIÊN của bản hoà.

Cách hoà: lấy MASTER làm nền cho cả hai tệp `.claude/dev/**` (đã kiểm băm: trùng master
từng byte), rồi CHỈ THÊM đường MCP. Ba thứ của nhánh cũ bị BỎ HẲN — trong đó có một
thứ nếu giữ sẽ **lùi** một bản vá đã land (`"REST thang bi proxy chan 403"` nối vô điều
kiện, chính là thứ #143 gỡ).

## Phải trả lời, mỗi câu kèm phép đo tái lập được

1. **Hoà có làm mất/lùi thứ gì của #143 không?** So `origin/master` với head, chỉ
   `.claude/dev/**`. Mọi thứ ngoài phần THÊM phải trùng master từng byte. Nếu có một
   dòng nào của #143 bị đổi mà không khai trong thông điệp commit, đó là finding.

2. **`mcp` KHÔNG được nằm trong `LAM_DUOC_VIEC` — đúng chưa, và có đường nào lách?**
   Lập luận: phép đo hỏi CLI xem server đã duyệt chưa ⇒ chứng minh một tiến trình
   `claude` MỚI SINH thấy gì, KHÔNG chứng minh phiên gọi được `mcp__github__*`. Xét cả
   tầng tiêu thụ (`_tinh_kha_dung`, `--doi-kha-dung`, `chua_chung_minh`).

3. **`_nhan_duong` ba trạng thái.** Người vá đổi kết xuất chung của MỌI đường, không
   riêng `mcp`. Có làm sai nghĩa đường nào của #143 không? Và người vá KHAI rằng
   `rest-kho` (nhánh không đọc được slug) mắc CÙNG BỆNH nhưng cố ý KHÔNG sửa — lời khai
   ấy đúng không, hay đó là né một finding?

4. **`_doc_mcp_json` / `_suc_khoe_mcp_github`.** Khớp tên chính xác · kiểm kiểu ba tầng
   · từ chối MƠ HỒ · `Status:` lấy bản ĐẦU TIÊN · mặc định `khong_do_duoc`. Còn hình
   dạng nào lọt? Đặc biệt: hàm nay nhận `env` từ `_do_github` — truyền `None` có làm
   `subprocess.run` lùi về `os.environ` THÔ (đúng bệnh P2 mà #143 vừa vá) không?

5. **`t115`/`t116` có đo HỢP ĐỒNG hay đo ĐỒ GIẢ?** Sáu lượt trước, lớp này thủng BỐN
   lần liên tiếp. Đồ giả nay tự từ chối lời gọi lệch đặc tả và đếm số lời gọi. **Tìm
   lượt thứ năm.** Và xét `t116`: nó đọc chính tệp test — có tự lừa được không?

6. **Số nền.** Tự chạy, đừng lấy số của người vá. Đặt `PYTHONPATH=/tmp/cryp` nếu
   `cryptography` hỏng; `TMPDIR` ghi được.
   ```
   python3 .claude/dev/launcher_test.py            # người vá đo: 116/116
   python3 .claude/dev/launcher_test.py --dot-bien # người vá đo: 90/90
   ```
   Nền master `c7ad260`: **114/114** và **74/74** — người vá đo trên WORKTREE THẬT sau
   khi một bản chép thiếu `.claude/hooks/` làm `t103`/`t108` đỏ oan. Đòi delta = 0 đỏ.
   Rồi **tự nghĩ ít nhất HAI đột biến** trên bản sao tạm.

7. **Câu TỔNG.** Bản hoà đã tới ngưỡng land chưa — nếu chưa, thiếu ĐÚNG cái gì, nói
   thành danh sách ĐÓNG ĐƯỢC. Nếu không tìm được đột biến sống sót, nói rõ là vì chốt
   đã đóng lớp hay vì hết hướng.

## Ngoài phạm vi (đừng báo lại)

- `.github/workflows/**` và `.claude/skills/**` dùng `gh`.
- Lời khai phạm vi của nhãn MCP (agent sắp sinh vs phiên đang chạy) — lượt 2 đã đo độc
  lập, lượt 5/6 xác nhận.
- Chốt `tao-tag` trong `ops-don-ref.yml` cấm `luu-tru/*` — đã biết, chủ kho chốt sửa
  bằng thay đổi RIÊNG.
- `ci.yml` không chạy `launcher_test.py` — đã đo, đã ghi trong PR.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
