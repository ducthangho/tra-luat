# Prompt review lượt 8 — vá P1/P2 lượt 7 + một chốt BỊ TƯỚC RĂNG

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8). CHỈ ĐỌC.
Nguồn có thẩm quyền là TỆP CÓ BĂM trong kho (lease + prompt này).

## Lượt 7 đã ra gì

`changes_requested` trên `fe55f2ce`:
- **P1** — `t115` chỉ hỏi `"env" in _k` chứ không hỏi GIÁ TRỊ ⇒ `env=moi_truong → env=None`
  SỐNG SÓT. Đây là **lượt thứ NĂM** của lớp "đo ĐỒ GIẢ chứ không đo HỢP ĐỒNG".
- **P2** — lời bào chữa của người vá cho việc không sửa `rest-kho` **không đứng vững**
  (`any(...)` coi `None` và `False` như nhau ⇒ kết luận khả dụng KHÔNG đổi).
- Ghi nhận `t116` có thể TỰ LỪA (bạn chứng minh được), nhưng không coi là chặn land.

## Và một chuyện lượt 7 KHÔNG thấy — người vá tự phát hiện khi chạy đột biến

`probe_github_bo_qua_moi_truong_chuan_hoa` — **đột biến CÓ SẴN của master**, canh
`t113` — **SỐNG SÓT** sau bản vá lượt 7. Không dòng logic nào sai. Nguyên nhân:
`chay_dot_bien` thay chỗ khớp **ĐẦU TIÊN**, mà khối chuẩn hoá env người vá chép vào
`_suc_khoe_mcp_github` **trùng khít từng chữ** với khối của `_do_github` VÀ đứng
**trước** nó trong tệp. Đột biến nhắm `_do_github` lặng lẽ nhảy sang bản sao, nên
`t113` không chết nữa. Một chốt bị TƯỚC RĂNG chỉ vì TRÙNG CHỮ.

Chữa bằng cách tách `_env_da_chuan()`.

## Lượt 8 xét gì

1. **`_env_da_chuan` có thật sự trả răng cho `t113` không?** Đo: đột biến
   `probe_github_bo_qua_moi_truong_chuan_hoa` phải GIẾT `t113` trở lại.

2. **`t117` — chốt chặn CẢ LỚP "tước răng", và người vá ĐÃ TỰ CHẠY phép đo này.**
   Định viết mục này thành câu hỏi cho bạn, rồi nhớ luật của kho (nghĩ ra phép thử mà
   không chạy thì phép thử ấy không tồn tại) nên chạy luôn. Kết quả ĐO ĐƯỢC:
   - trên nhánh này: 95 mục `DOT_BIEN`, **1 chỗ trùng**
   - trên master `c7ad260`: **CŨNG 1 chỗ trùng, cùng mục** — `hook_phien_bo_phep_so_nang_luc`
     (`_do_hook_cu` và `_do_launcher_cu` cùng dòng `thieu = sorted(cua_master - dang_co)`)

   Tức món nợ đó CÓ SẴN, không phải do bản vá MCP. Nó vào DANH SÁCH CHO PHÉP của `t117`
   kèm lý do, và danh sách ấy có CHỐT NGƯỢC: nếu mục kia hết trùng thì `t117` ĐỎ và bắt
   gỡ nó ra — để danh sách cho phép không thành một lời khai chết.

   **Việc của bạn ở mục này:** (a) chạy lại phép đếm ấy độc lập — con số có khớp không;
   (b) `t117` có lỗ nào không (nó đọc `DOT_BIEN` đã nạp và `launcher.py` — có tự lừa
   được như `t116` không?); (c) lời khai "latent chứ chưa hỏng" về
   `hook_phien_bo_phep_so_nang_luc` có đúng không — `t88` có THẬT SỰ còn chết vì đột
   biến ấy không, hay nó cũng đã mất răng từ trước mà chưa ai đo?

3. **Oracle `env` nay đòi ĐÚNG OBJECT (sentinel + `is`).** Còn đường nào để một bản vá bỏ
   qua tham số mà vẫn qua? (Người vá đã phải sửa ORACLE chứ không sửa mã cho đột biến
   `env_da_chuan_tra_ve_os_environ_THO` — vì "env là dict khác None" vẫn qua, `os.environ`
   cũng là dict.)

4. **`rest-kho` đổi `False → None`.** Có làm sai nghĩa gì không? Ca khoá nó là một phép
   kiểm **NGUỒN** (`'("rest-kho", None, "khong doc duoc slug' in nguon`) chứ không phải
   phép kiểm HÀNH VI — đó là chốt yếu; nói rõ nó yếu tới đâu, và có đường nào làm nó
   xanh giả không.

5. **`t116`/`t117` — người vá nay KHAI THẲNG giới hạn tự-lừa trong docstring.** Lời khai ấy có
   đúng phạm vi không, hay vẫn rộng/hẹp hơn thứ đo được?

6. **Số nền.** Tự chạy (`PYTHONPATH=/tmp/cryp`, `TMPDIR` ghi được):
   ```
   python3 .claude/dev/launcher_test.py            # người vá đo: 117/117
   python3 .claude/dev/launcher_test.py --dot-bien # người vá đo: 94/94
   ```
   Nền master `c7ad260`: **114/114** và **74/74**, đo trên WORKTREE THẬT. Đòi delta = 0 đỏ.
   Rồi **tự nghĩ ít nhất HAI đột biến**, ưu tiên mục 2.

7. **Câu TỔNG.** Đã tới ngưỡng land chưa — nếu chưa, thiếu ĐÚNG cái gì, nói thành danh
   sách ĐÓNG ĐƯỢC. Nếu không tìm được đột biến sống sót, nói rõ là vì chốt đã đóng lớp
   hay vì hết hướng.

## Ngoài phạm vi (đừng báo lại)

- `.github/workflows/**`, `.claude/skills/**` dùng `gh`.
- Lời khai phạm vi của nhãn MCP — lượt 2 đo độc lập, lượt 5/6 xác nhận.
- `ci.yml` không chạy `launcher_test.py` (đã đo `grep -c` = 0).
- Chốt `tao-tag` cấm `luu-tru/*` — đang sửa bằng thay đổi RIÊNG, review riêng.
- `t116` tự-lừa được — đã ghi nhận, đã khai trong docstring, không phải chặn land.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
