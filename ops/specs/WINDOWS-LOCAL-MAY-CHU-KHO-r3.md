# Đặc tả packet `WINDOWS-LOCAL-MAY-CHU-KHO` r3: nhịp tim cho khoá, không tiếp nhận khoá còn tiến trình sống, và ghi lượt bị ngắt

tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544

| trường | giá trị |
|---|---|
| packet | `WINDOWS-LOCAL-MAY-CHU-KHO` (mission `gh-1035`), revision 3, generation 1 |
| review_class | `sensitive` (cổng lease tính `sensitive` cho `docs/PROTOCOL_DA_PHIEN.md`, tiền lệ r1, r2) |
| write set | `docs/adr/0059-windows-local-nhip-tim-khoa.md` (planned), `docs/PROTOCOL_DA_PHIEN.md` |
| base | `origin/master` lúc cấp lease (đo khi soạn: `adb3d2e`, merge của PR #1049) |
| executor | `anthropic_claude` (Claude Code remote, Linux) |
| reviewer | `openai_codex` qua `launcher.py run`, phiên mới, neo đúng head, có snapshot §8.2 đầu/cuối |
| depends_on | r2 đã land (`ADR-0058`, PR #1029, `landed: true` ở PR #1049) |

## 1. Vì sao
`ADR-0058` có hiệu lực từ 30-10-2026. Trong ngày đầu dùng nó, sổ đo `D:\tl-win\do-luong.csv` và khoá
`D:\tl-win\KHOA.txt` trên ASUS-LAPTOP ghi được ba lỗ mà r2 không phủ. Số đo đọc lại qua Desktop Commander lúc ~01:35Z ngày 31-10.

| # | sự kiện | số đo | bài học |
|---|---|---|---|
| D10 | tiếp nhận một khoá còn sống | Dòng sổ đo `2026-10-30T13:58:02Z` của `session_015GtxrcrefBJpLr7fGUSPtB` ghi tiếp nhận khoá của `session_015GtxrbUPS7zGdffB8Sfo8Y` theo `ADR-0058` 3(b), với lý do "dạng cũ không có hạn, đã quá 2 giờ" (khoá ghi lúc 09:01:16Z). Dòng `13:59:37Z` của chính phiên tiếp nhận ghi "có PID 26296 `tl.py --selftest` của phiên khác đang chạy". Dòng của phiên giữ khoá ghi selftest ấy xong lúc 14:03:16Z, khoá bị ghi đè lúc 14:01:44Z, nên hai phiên chồng nhau khoảng 1,5 phút. | 3(a) và 3(b) chỉ xét đồng hồ. Một lượt chạy dài hơn 2 giờ, vì máy ngắt giữa chừng, vẫn bị coi là khoá bỏ rơi trong khi tiến trình của nó còn chạy |
| D11 | máy ngắt giữa lượt chạy | Dòng `09:01:16Z` (`session_015GtxrbUPS7zGdffB8Sfo8Y`): `tl --selftest` 1758/1758 nhưng mất 18113 s; Desktop Commander không truy cập được từ ~09:06Z (Offline lúc 10:22Z và 11:25Z). Dòng `16:13:56Z` (`session_015GtxrZ1Tt93F4NLUUhKYQy`): lượt 1 lúc 14:05Z bị cắt khi máy offline ~14:16Z–15:25Z, phải chạy lại lượt 2 từ 15:26:48Z. | ADR-0057 và ADR-0058 không nói một lượt bị ngắt thì ghi sổ thế nào, và thời lượng của nó có được đếm không |
| D12 | khoá quá hạn không được nhả | `KHOA.txt` lúc ~01:35Z ngày 31-10 còn dòng `session_015GtxrZ1Tt93F4NLUUhKYQy` `2026-10-30T19:17:25Z` hạn `2026-10-30T21:17:25Z` (`#1021 C7 head 356a27e`), tức đã quá hạn hơn 4 giờ. | 3(a) xử lý được (khoá hết hiệu lực), nhưng "xoá nội dung khi xong" của `ADR-0057` §3 không có cách nhả nào được định nghĩa rõ |

## 2. Thay đổi
1. **Thêm ADR-0059** tại `docs/adr/0059-windows-local-nhip-tim-khoa.md`, trạng thái `Accepted` khi chủ kho duyệt `spec_hash`.
   ADR này **chỉ bổ sung cho §3 (Hạn khoá)** của `ADR-0058` và §3 (Khoá) của `ADR-0057`, theo cùng cách `ADR-0058` sửa `ADR-0057`.
   Mọi điểm khác của hai ADR giữ nguyên. Không sửa tệp `ADR-0057` và `ADR-0058`.
   - **Nhịp tim.** Dòng khoá thêm trường thứ năm:
     `<session_id>\t<UTC bắt đầu>\t<UTC hạn>\t<việc>\t<UTC nhịp tim>`.
     Phiên giữ khoá ghi lại dòng, với nhịp tim là giờ hiện tại, ít nhất 30 phút một lần trong lúc còn chạy.
     Hạn vẫn không quá 2 giờ kể từ lần ghi (gia hạn như `ADR-0058`).
   - **Không tiếp nhận khoá còn tiến trình sống.** Trước khi tiếp nhận một khoá hết hiệu lực theo 3(a) hoặc 3(b) của
     `ADR-0058`, chạy bước kiểm tải (§4 của `ADR-0057`). Nếu thấy một tiến trình `python.exe` khởi động sau UTC bắt đầu
     của khoá cũ và không phải tiến trình MCP, thì khoá được coi là **còn sống**: không tiếp nhận, ghi một dòng sổ đo
     nêu PID và lệnh đã thấy, rồi đợi. Quy tắc này không áp dụng cho 3(c), vì ở đó phiên giữ khoá đã tuyên bố bỏ.
   - **Lượt bị ngắt.** Nếu máy Offline hoặc Desktop Commander không truy cập được trong lúc một lượt đang chạy,
     dòng sổ đo của lượt ấy ghi `ngat=co` trong `ghi_chu`, kèm khoảng thời gian không truy cập được nếu đo được.
     Thời lượng của lượt bị ngắt không dùng cho rà soát ADR. Khi kết nối lại mà còn cần máy, phiên giữ khoá ghi lại
     dòng khoá ngay (nhịp tim và hạn mới) trước khi chạy tiếp. Không tự đổi chế độ nguồn hoặc ngủ của máy (protocol §3.1);
     việc chống ngủ là của chủ kho.
   - **Nhả khoá.** Nhả khoá là ghi tệp `KHOA.txt` rỗng (0 byte). Phiên giữ khoá nhả ngay khi xong, kể cả khi lượt đỏ
     hoặc bị bỏ.
   - **Số đo D10–D12** của §1, kèm mục "không cổng nào cưỡng chế" (vẫn 0 cổng, như ADR-0057 và ADR-0058).
2. **`docs/PROTOCOL_DA_PHIEN.md`:**
   - thêm đúng một dòng ADR-0059 vào bảng §20, cột cổng `không cổng — kỷ luật executor`;
   - sửa ô mô tả của dòng ADR-0058 trong §20 để thêm "khoá bổ sung bởi `ADR-0059`". Chỉ sửa ô ấy;
   - câu con trỏ ở §10.2 đổi thành nhắc cả `ADR-0057`, `ADR-0058` và `ADR-0059`, vẫn là câu trung tính
     (finding P1 lượt 1 của r1: con trỏ không được tạo thêm nghĩa vụ).

   Không chép doctrine vào protocol.

## 3. Tiêu chí xong
- `python .claude/dev/packet_loop.py adr-song --root .` rc=0.
- `doctrine-scan` rc=0; `python scripts/tl.py doc-claims-check --json` cho `ok`.
- Diff chạm đúng 2 tệp của write set, không chạm `docs/adr/0057-*` và `docs/adr/0058-*`.
- Review chéo Codex qua `launcher.py run` trên đúng head, có snapshot §8.2 đầu/cuối, tới khi 0 P0–P3.
- Nếu chạy local trên Windows thì theo chính luật khoá mới, và ghi sổ đo.

## 4. Trần
- Kích thước: ≤ 2 tệp / ≤ 140 dòng thêm.
- Lời gọi Codex: 10, theo dòng khai ADR-0055.

## 5. Ngoài phạm vi
- Không viết công cụ khoá nguyên tử, công cụ nhịp tim hay bộ đọc sổ đo. Khoá vẫn là tệp văn bản không nguyên tử.
- Không sửa CI, không đổi check bắt buộc, không đổi chế độ nguồn của máy chủ kho.
- Không sửa hồi tố các dòng sổ đo hay khoá đã có.
