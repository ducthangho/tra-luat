# WP-PXA r1 — Review mã trước khi đo (lượt review 1/2)

- **Reviewer:** Claude subagent mới, chỉ đọc. Model tự khai `claude-opus-5-5`, effort `KHONG_do_duoc` (phiên điều phối yêu cầu xhigh).
- **Cách review:** review tĩnh, vì container không có PowerShell.
- **Đối tượng:** commit `04b382719`.
  - `ProximaActivation.psm1`: `4f1316d8…`
  - `ProximaActivation.Tests.ps1`: `81a3f986…`
  - `SKILL.md`: `21171c12…`

  Mã do Codex Executor viết ở lượt 2/3, run `007eff9e`.

## Verdict: `approve_with_fixes`, không có P0

**Phần đúng**
- Kiểm cây artifact và fence khớp đặc tả; thứ tự mã lỗi đúng; không đi vào junction; mọi exception đều trả `NOT_MEASURED`.
- Không có cú pháp chỉ có ở PS7. Mọi lời gọi .NET đều có trong .NET Framework 4.8.
- Counterexample hợp lệ: anchor là duy nhất; chạy trong tiến trình mới cùng edition; chỉ được tính khi đúng ca đích đỏ.
- SKILL.md vẫn giữ PM05 và PM07 đạt.

**P1**
- **P1-1 (psm1:237):** chốt profile để lọt khi `"--user-data-dir=C:\a b\prof"` được bao ngoặc kép nguyên tham số, đúng dạng `list2cmdline`, .NET và PS7 sinh ra cho đường dẫn có dấu cách. Dạng `-user-data-dir=` và `/user-data-dir=` cũng bị bỏ sót.
  - Sửa: tách token, bỏ dấu `"`, rồi khớp `^(?:--|-|/)user-data-dir(?:=(.*))?$`.
  - Thêm test cho dạng có ngoặc kép, ca âm tiền tố (`prof2`, `prof\sub`), và đột biến `Equals→StartsWith`.
- **P1-2 (psm1:261-262):** Proxima có CommandLine null hoặc rỗng (elevated, hoặc chạy dưới user khác) bị coi là "không phải profile này".
  - Sửa: trả `NOT_MEASURED` kèm pid, trước khi lấy khoá. Thêm test.

**P2**
1. Đường dẫn tương đối được resolve theo current directory của tiến trình, không theo `$PWD`.
2. Tệp khoá là link thì `SetLength(0)` cắt cụt tệp đích.
3. Kiểm tiến trình xảy ra trước khi lấy khoá. Cần kiểm lại sau khi lấy khoá và ghi rõ race này.
4. Snapshot tiến trình rỗng vẫn được coi là đã đo. Cần đòi snapshot chứa `$PID`.
5. Lỗi binding tham số lọt ra ngoài thay vì trả `NOT_MEASURED`.
6. `.Keys` chưa được bọc qua `PSBase`.
7. Fence không kiểm `ArtifactSha256` có đủ 64 ký tự hex, và chấp nhận Plan có host trùng.
8. Fence chưa có test cho trường hợp host trong receipt khác tên tệp, và `"passed":"true"` ở dạng chuỗi.
9. `MutableRelative` chưa được kiểm hợp lệ.
10. `-ilike` phụ thuộc culture (tr-TR).
11. Harness chưa ngang PM harness: chưa từ chối output nằm trong repo, chưa đòi mỗi ID chạy đúng một lần, child chưa có timeout.
12. SKILL.md thiếu phần giới hạn: snapshot, profile phải tồn tại sẵn, không thấy tiến trình elevated, và chưa nhắc tệp test.
13. `PROFILE_BUSY` không kèm pid và quy tắc nào đã kích hoạt.

## Xử lý
Toàn bộ P1 và P2 giao Executor **Fable 5.2** (đổi Executor theo chỉ thị chủ kho ngày 18/11; lease g3). Lượt review 2/2 do **Codex `gpt-6-astra`** chạy trên Windows sẽ kiểm bản sửa cùng kết quả đo.
