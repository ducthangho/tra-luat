# CROSS-REVIEW lượt 7 — codex

Verdict: **changes_requested**

Mỏ neo: `69bc3cede6085bf6229ac95a44da4aae9e51ee42` (base so sánh `c775c0a5b0bf0816e913ba0b300d898fec3c58b0`).

## Findings

### HIGH — suite chuẩn vẫn giết caller trong chính môi trường reviewer

`python3 .claude/dev/launcher_test.py` không bao giờ in tổng kết: nó dừng ngay sau dòng bỏ qua `t62`. Bản khai trước khi runner tự tách là:

```text
moi truong: pid=2 pgid=1 sid=1 truong_nhom=False chung_nhom_voi_cha=True job_control=? ns_pid=pid:[4026532315] init=3
nhom tien trinh: da tach sang session moi (pgid=2)
```

Đây chính là tiêu chí HIGH mà đề bài đặt ra. Ép từ ngoài bằng `setsid python3 ...` cũng không cứu suite chuẩn: bản khai thành `pid=2 pgid=2 sid=2 ...`, rồi vẫn mất caller sau `t62`. Như vậy giả thuyết “bịt fail-open `killpg` là đủ để suite chạy hết bên reviewer” sai. Mutation runner sống vì nó chỉ gọi các ca đích riêng lẻ; đó không phải bằng chứng suite tuần tự an toàn.

Phải truy tiếp ca đầu sau `t62` (`t63`) và bảo đảm suite chuẩn hoàn tất trong namespace này mà không cần vỏ bọc ngoài. Hiện không thể nghiệm thu một bộ test có thể giết chính tiến trình gọi.

### HIGH — `inherit = "all"` mở rộng rò bí mật không cần thiết và `exclude` không phải chính sách tổng quát

Khối tại `.claude/hooks/session-start.sh:241-250` truyền toàn bộ môi trường cho mọi lệnh con, chỉ loại bốn tên được quan sát trên một máy tại một thời điểm. Phép quét tên không thể chứng minh an toàn cho các bí mật có tên như `PGPASSWORD`, `DATABASE_URL`, `REDIS_URL`, `SSH_AUTH_SOCK`, biến vendor mới, hoặc token đặt dưới tên không khớp mẫu. Danh sách này sẽ lỗi thời ngay khi môi trường thay đổi.

Quan trọng hơn, trong chính flow của hook, `CODEX_AUTH_JSON` đã được khôi phục vào `~/.codex/auth.json` trước khi policy được ghi. Sau đó Codex và lệnh con có thể đọc credential từ file chuẩn; mở lại JSON credential cho *mọi* subprocess không còn cần để tái dựng credential. Nếu hook không chạy thì policy này cũng không được cài, nên nó không tạo đường cứu hộ độc lập. Hãy bỏ `inherit="all"`, hoặc dùng allowlist/set tối thiểu với mô hình bí mật rõ ràng; không nên đổi một credential cần thiết thành toàn bộ môi trường kế thừa.

### MEDIUM — hook có thể làm hỏng `config.toml` hợp lệ của người dùng bằng bảng trùng

Khối `.claude/hooks/session-start.sh:256-265` chỉ gỡ bảng có marker do hook quản lý, rồi luôn prepend một `[shell_environment_policy]`. Nếu config người dùng đã có bảng cùng tên nhưng không có marker (một cấu hình Codex hoàn toàn hợp lệ), kết quả chứa hai bảng TOML cùng tên và Codex từ chối parse. Trường hợp chỉ có một marker bị hỏng cũng tạo bản sao chồng lên ở mỗi lượt. Tính bất biến chỉ đúng với đúng cặp marker nguyên vẹn và không có bảng sẵn có.

Phải parse/merge bảng hiện hữu hoặc từ chối có chẩn đoán; cần test chạy lặp, bảng đã tồn tại không marker, và marker thiếu một đầu. Việc đặt bảng trước `[projects...]` là đúng về scope TOML nhưng không giải quyết duplicate-table.

## Trả lời các câu hỏi kỹ thuật

- Lời giải `.pyc` **đủ giải thích đúng con số lượt 6**. Trên bản cũ `c775c0a`, mutant `do_codex_tin_DONG_DAU_thay_vi_ma_thoat` là `SAI, giet 0/1`, tổng `49/50`; trên `69bc3ce` cả hai lượt đều là `OK, giet 1/1`, tổng `56/56` (mỗi lượt có 1 mục chỉ đo được trên Windows).
- Tên tệp riêng là lớp quyết định ở runner. Xoá `.pyc` bảo vệ cache sót từ lượt trước; tắt ghi bytecode có phép đo riêng và tránh sinh cache mới. `invalidate_caches()` không có phản chứng riêng và với `spec_from_file_location` + đường dẫn riêng + xoá pyc thì về thực tế là lớp thừa; nó không gây hại nhưng không nên khai là đã chứng minh độc lập. `_nap_sach` chỉ xoá `cache_from_source(duong)` của đúng fixture; phạm vi không rộng. Việc nuốt lỗi xoá/cache là chấp nhận được vì các lớp sau vẫn chạy, nhưng khi xoá thất bại thì bảo đảm phụ thuộc lớp còn lại chứ không còn là “xoá sạch”.
- Không thấy đường `killpg` nào khác trong `_giet_cay` vượt chốt `dung_killpg`; cả SIGTERM và SIGKILL đều được canh. `_con_lai()` dùng `[]` cho phần nhóm khi không nhận trách nhiệm không tự làm sai `me_da_chet/ca_cay` đối với ảnh chụp, nhưng nó cố ý không thể phát hiện tiến trình gia nhập/sinh sau ảnh. Khe này rộng hơn mô tả “gia nhập nhóm”: nó gồm mọi hậu duệ xuất hiện sau snapshot và mọi tiến trình đổi quan hệ khiến snapshot không chứa nó. Finding suite ở trên cho thấy chưa thể dựa vào lập luận để coi đường này an toàn.
- Đảo chiều `t92(c)` là đúng hợp đồng fail-closed: không đo được pgid thì không `killpg`, nhưng ảnh có khóa danh tính vẫn phải bị giết riêng; ảnh rỗng thì từ chối. Test mới không phải nới cho vừa bản vá ở điểm đó.
- Whitelist `DA_CHUNG_MINH_KHA_DUNG={"DUNG_DUOC"}` và `--doi-kha-dung` fail-closed là đúng. Mặc định rc=0 là lựa chọn tương thích, nhưng người gọi cần bằng chứng phải thực sự dùng cờ; JSON `ok_kha_dung=false` vẫn giữ tín hiệu. `t98` ghim `KHA_NANG`/`CONG_CU` đúng cho unit test tầng tổng hợp, nhưng cần thêm integration test CLI để giữ liên hệ parser/cờ/JSON thật.
- Cảnh báo sớm không thành chốt đỏ thường trực sau khi loại `id_token`: `SAP_HET_HAN` mặc định vẫn rc=0. Không thấy token value bị in; chỉ tên token, số giờ và `last_refresh`. Hai tầng lọc `id_token` là phòng thủ hợp lý.

## Bằng chứng chạy

- Bước 0: `false`; `core.abbrev=7`; HEAD đúng SHA; diff đúng 5 tệp yêu cầu.
- `git diff --check c775c0a... HEAD`: sạch.
- Suite chuẩn, HOME tạm: caller mất sau `t62`, không tổng kết — tái lập cả không và có `setsid` ngoài.
- `69bc3ce --dot-bien`, HOME tạm, hai lượt: `56/56 đạt`, 1 không đo được trên POSIX ở mỗi lượt.
- `c775c0a --dot-bien` từ `git archive` trong thư mục tạm: `49/50 đạt`, đúng mutant nêu trên `giet 0/1`.
- Không đọc hoặc in giá trị biến môi trường/token; không đụng auth thật.
- `git status --porcelain` cuối: sạch.

