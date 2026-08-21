> **CẢNH BÁO — ĐÂY LÀ BẢN DỰNG LẠI, KHÔNG PHẢI BẢN GỐC BYTE-CHO-BYTE.**
>
> Sandbox của lượt 1 (`runs/4b31278d/stdout.log`, 3926 byte) đã bị xoá khi phiên điều phối
> khởi động lại, và verdict ấy **chưa từng được ghi vào kho** — lỗi của phiên điều phối, đúng
> thứ rủi ro nó vẫn cảnh báo người khác. Bản dưới đây được dựng lại từ ngữ cảnh phiên, KHÔNG
> có băm để đối chiếu. Đọc nó như **lời thuật lại**, không như bản gốc neo bằng băm.
>
> Con số và kết luận thì tra được ở chỗ khác: `VERDICT: changes_requested`,
> `Reviewed commit: cbc57214be1f33b93c5d04e4363c2bcce87439b6`, một finding P1.

## Finding P1 — GHIM SHA vẫn còn TOCTOU và có thể xoá commit chưa được đo

Trong `ops-don-ref.yml`, workflow: (1) đọc SHA hiện tại; (2) so với SHA ghim; (3) sau đó mới gọi
`DELETE`. Một push vẫn có thể chen giữa bước 2 và 3. `concurrency: ops-don-ref` không khoá các
push bên ngoài workflow. Endpoint GitHub chỉ nhận tên ref, không có `expected_sha`/CAS trong cùng
request — tài liệu chính thức xác nhận tham số xoá chỉ gồm `owner`, `repo`, `ref`.

Bằng chứng chạy được trên bản sao `git archive`:

- Ghim và lần GET cuối trả `S1=b4e5c5f9ef85e652fa2cc98bb3474036519d663c`.
- Đồ giả trạng thái đẩy nhánh sang `S2=872679c360a43a4b12221749901aa0cf231566ac` sau khi tạo
  phản hồi GET nhưng trước DELETE.
- Mong đợi: đỏ, không DELETE.
- Thực tế: bước làm `rc=0`, gọi DELETE đúng một lần, báo "đã xoá", và nhật ký xác nhận chính
  `S2` bị xoá.
- Harness mở rộng: `102/105`, `rc=1`, với ba bằng chứng đỏ: `rc=0, mong 1`; DELETE đếm được
  `1, mong 0`; `đã xoá chính SHA mới S2`.

Nếu `S2` là commit chưa vào nhánh mặc định, invariant quan trọng nhất bị cắt. Mô tả trong
`CLAUDE.md` rằng phép đọc lại "đóng" khe đo–xoá cũng chưa đúng.

Gợi ý vá: hướng rẻ nhất và an toàn ngay là khôi phục cấm xoá vùng làm việc cho tới khi có
primitive xoá nguyên tử; hướng giữ chức năng là dùng thao tác ref-update gửi expected old OID
trong cùng giao dịch, chẳng hạn đường Git transport với explicit lease, sau khi chứng minh thật
trên GitHub runner — không dùng REST DELETE vô điều kiện. Test khoá: chuyển trạng thái `S1 → S2`
sau GET cuối, đòi ref `S2` vẫn tồn tại và không có DELETE; mutant bỏ lease/CAS hoặc quay lại REST
DELETE phải chết.

## Đã đo và sạch

- Lease revision 1 còn hạn; prompt trong lease khớp SHA-256 `18bc3605…`.
- HEAD, branch ref và reviewed target cùng là `cbc57214…`; tree `837d7f4b…`.
- `diff.patch` khớp byte với diff từ merge-base `07b96ce7…`, đúng ba path trong write set.
- Bộ nguyên bản trên archive: `102/102`, `rc=0`; actionlint của workflow đích qua.
- KHO giữ nguyên: HEAD không đổi, worktree và index đều sạch.

## Chưa đo được — GIẢ THUYẾT

Do stop condition đã kích hoạt, reviewer **không tiếp tục các trục còn lại**. Chưa xác nhận:
lịch sử rời, ngưỡng 250 commit, các mutant M1–M6, mutant chèn bước YAML, toàn bộ năm workflow
bằng actionlint, lập luận M2, hay các race liên quan đầu nhánh mặc định. **Không mục nào trong
số này được coi là sạch.**

VERDICT: changes_requested
Reviewed commit: cbc57214be1f33b93c5d04e4363c2bcce87439b6
