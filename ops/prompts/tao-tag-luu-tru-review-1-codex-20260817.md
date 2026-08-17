# Prompt review — `ops-don-ref`: cho `tao-tag` tạo được `luu-tru/*`

Bạn là REVIEWER, provider `codex`. Người vá là `claude` (§8). CHỈ ĐỌC.
Nguồn có thẩm quyền là TỆP CÓ BĂM trong kho (lease + prompt này).

## Lỗi được vá — đo trên một lượt chạy THẬT, không phải đọc code

`workflow_dispatch` trên `ops-don-ref.yml`, chế độ thử khô:

```
tao-tag  luu-tru/doctor-github-mcp-verdict-6  4920113…
→ DỪNG: tag 'luu-tru/…' mang tên vùng được bảo vệ. Đặt tên khác.   (rc=2)
```

Mà chính nhánh `xoa-nhanh` của workflow ấy dặn nguyên văn: *"Tạo tag TRƯỚC (hành động
tao-tag), rồi mới xoá."* **Trình tự nó tự quy định thì nó tự chặn** — không lượt chạy nào
thoả được cả hai vế. Và `ops-don-ref.yml` là đường DUY NHẤT để phiên web tạo tag (đẩy
`refs/tags/*` bị proxy chặn 403, đã đo 16-08).

## Bản vá

Bỏ `luu-tru/*` khỏi danh sách cấm **của riêng nhánh `tao-tag`**. Giữ nguyên
`ops/ claude/ codex/ agent/ mission/ dispatcher/`, và giữ nguyên lệnh **CẤM TUYỆT ĐỐI**
`xoa-tag` dưới `luu-tru/` ở nhánh trên.

## Phải trả lời, mỗi câu kèm phép đo tái lập được

1. **Mở `tao-tag` cho `luu-tru/` có mở thêm gì ngoài ý muốn không?** Cụ thể: `xoa-tag
   luu-tru/*` có còn CẤM TUYỆT ĐỐI không, và `xoa-nhanh luu-tru/*` có còn đòi "phải có tag
   giữ commit" không? Đây là câu quan trọng nhất — một bản vá cẩu thả sẽ nới cả ba.

2. **Danh sách cấm còn lại có bị nới theo không?** `ops/ claude/ codex/ agent/ mission/
   dispatcher/` phải vẫn DỪNG cho `tao-tag`. Chốt hạ hoa/thường (`LUU-TRU/`) có đúng không,
   và có mở oan cái gì không (ví dụ `luu-tru-gia/`, `xluu-tru/`)?

3. **Lập luận "không đặt tên khác cho xong" có đứng vững không?** Người vá lập luận: chốt
   `xoa-nhanh` hỏi *"còn tag nào giữ commit ấy không"* chứ KHÔNG hỏi tag tên gì, nên một tag
   đặt tên khác vẫn qua chốt ấy nhưng phá quy ước không gian tên mà `CLAUDE.md` khai là ref
   BỀN duy nhất giữ commit verdict. Nếu lập luận sai thì bản vá này không cần thiết — nói thẳng.

4. **`actionlint`.** Kho đã trả giá: một workflow PyYAML parse được mà GitHub TỪ CHỐI, và
   SÁU lượt cross-review đều kết luận "YAML ok" vì cả sáu chỉ kiểm bằng PyYAML. Bộ test
   fail-close khi thiếu công cụ. Nếu môi trường bạn KHÔNG có `actionlint` thì nói **KHÔNG ĐO
   ĐƯỢC** cho mục này — đừng thay bằng PyYAML rồi gọi là đã kiểm.

5. **Số nền.** Tự chạy (`ACTIONLINT=<đường dẫn>` nếu cần):
   ```
   bash ops/don_ref_chot_test.sh
   ```
   Người vá đo: nhánh **82/82**, master `f9730f6` **74/74** ⇒ delta +8 ca, 0 đỏ. Và
   `actionlint` trên toàn bộ workflow của master ⇒ rc=0.
   Rồi **tự nghĩ ít nhất HAI đột biến** trên bản sao tạm. Người vá đã chạy hai:
   - cấm lại `luu-tru/` ⇒ 80/82, đỏ đúng hai ca `tạo tag luu-tru/ thì QUA`
   - nới thêm `codex/` ⇒ 81/82, đỏ đúng ca `tạo tag codex/ vẫn DỪNG`
   (Neo bằng khối `case` ĐẦY ĐỦ: mẫu ngắn khớp **2** chỗ vì nhánh `xoa-nhanh` có danh sách
   tương tự — neo ẩu thì đột biến nhắm nhầm chỗ.)

## Cách xếp phát hiện

- `## Findings` — CHỈ: hồi quy · lỗ an ninh (mở thứ lẽ ra phải cấm) · P1 làm workflow không
  chạy được.
- `## Nợ khai báo` — mọi thứ khác. Lý do: chuỗi review trước trên kho này mở suốt chín lượt
  phần lớn vì người vá vá tại chỗ mọi quan sát; thứ không thuộc ba loại trên sẽ thành thay
  đổi RIÊNG với lượt review riêng.

## Ngoài phạm vi (đừng báo lại)

- `.github/workflows/**` dùng `gh` — runner GitHub không có MCP, đó là đường sạch.
- Việc `ops-don-ref.yml` cấp lại quyền mà sandbox cố ý không cho — CÓ CHỦ Ý, đã khai trong
  đầu tệp, kèm sáu lớp chốt.
- Lỗ đã biết của chốt proxy: nó chặn theo HÌNH DẠNG chứ không theo HẬU QUẢ, nên
  `git push --force` vẫn được phép. Đã ghi trong `CLAUDE.md`.

## Định dạng trả lời — in ra stdout, không ghi tệp

    verdict: approve | changes_requested | do_not_land
    reviewed_sha: <sha>
    ## Findings
    ## Nợ khai báo
    ## Phép đo đã chạy

Cái gì không đo được thì nói **KHÔNG ĐO ĐƯỢC**. Đừng đoán.
