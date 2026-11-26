# Audit công cụ bảng — mã đã đọc trước khi chạy

Công cụ được băm lại đúng d872efd21c9d7870d2a633206264958e6e8c52bf17e970b9446ee2b2876997fb. `table-static.json` kiểm 108/108 neo xuất hiện đúng một lần, bytes sau thay khác trước và parse AST được. Kiểm này không thay chạy test.

`mot()` ghi một tệp trên clone worker, chạy `python -B <tệp> --mot-ca <tên đầy đủ>`. GIET đòi **rc 3 và stdout sau strip bắt đầu đúng DO:<ca phản chứng đang chạy>:**. Rc4 hoặc rc3 sai tên không tự thành GIET. Nếu một ca HONG rồi ca sau GIET, GIET thắng; công cụ giữ HONG chỉ khi không ca nào giết. Đây là phân hạng theo ca phản chứng (c38/c39/c40/a136), không theo ca đích bên trong chúng.

Cần phân biệt hai tầng: a135/c36/c37 là ca đích; a136/c40/c39 là ca kiểm chúng. Nếu ca đích trả rc4, phép so chính xác của ca phản chứng có thể ném TinHieuChotCa và tạo rc3 ngoài. Ví dụ bỏ bool(ra) sẽ làm đường bộ sinh rỗng lỗi IndexError; a136 phát hiện mục tiêu không trả rc3 yêu cầu. Một mutant TypeError tùy ý ở ca đích cũng có thể bị gọi GIET theo cùng cơ chế. Do đó kết quả bảng KHÔNG tự chứng minh mọi đột biến có lỗi nghiệp vụ thay vì lỗi runtime bên trong; phải đọc từng phép sửa và kiểm trace của bản nguyên vẹn. Các probe công cụ sẽ ghi riêng cả lỗi ở tầng ngoài lẫn tầng trong, không xóa sự khác nhau này.

`main()` đòi nguồn sạch (status tracked/untracked thường), clone vào --ra/wN, checkout exact SHA, ghim core.abbrev 7. Một luồng sở hữu duy nhất một worker, xử lý các chỉ số k,k+N,...; không hai đột biến cùng ghi một worker. `finally` khôi phục tệp trước đột biến kế. Chạy tiến trình mới với -B cho mỗi ca, cùng PYTHONDONTWRITEBYTECODE=1 trong review. Clones mới không có pyc, không chia sẻ object Python hoặc NHO_YAML; -B ngăn ghi pyc, không phải một cơ chế tổng quát cấm đọc pyc cũ. Khi tái dùng worker cũ có ignored pyc, công cụ không kiểm chúng; kết luận lần này chỉ áp clone mới đã quan sát.

Chống thao tác rỗng ở hai tầng: `mot` đòi neo đúng một lần; `main` có assert neo != moi cho mọi việc. Gọi riêng mot với neo==moi không được chặn ở helper đó, nhưng đường CLI chuẩn có chặn; Python lần này optimize=0 và reviewer cũng tự kiểm bytes của toàn bảng.

Rc0 toàn công cụ đòi 4 baseline trả chính xác (0,""), mọi worker sạch sau khôi phục và không có SONG/HONG chưa được gán tương đương. Nhãn TUONG_DUONG chỉ dùng cho mutant thật SONG cùng khóa TD có lập luận; công cụ không chứng minh lập luận. Reviewer đã kiểm cả bốn. Công cụ không tự chứng minh danh sách M đủ mệnh đề hoặc mọi ô KAD hợp lý; hai phần đó được kiểm riêng.

Giới hạn báo lỗi: `chay()` chỉ trả stdout, bỏ stderr; SyntaxError có thể được xếp HONG đúng rc nhưng mất chẩn đoán. `dong` của từng GIET bị cắt 400 ký tự. Review lưu thêm các probe có stdout/stderr đầy đủ; không suy tín hiệu ca đích từ đoạn đuôi đã cắt.
