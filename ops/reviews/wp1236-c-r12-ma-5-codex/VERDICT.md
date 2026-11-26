Review độc lập lượt 5, đợt C wp1236 r12/g1 — **changes_requested**.

`reviewed_sha`: `8aab9dabb6f3f150e4ab1872e37757c2620912c3`  
Tree: `5474259bbb71e3be6e3f7d3eaf4661142906ca0d`  
Base: `f602325574c62184caf16309631f5f680ca5cee2`  
Spec SHA256: `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`.

**C05 — P2 — archive-loc-mat-du-lieu-kiem** tại `.claude/dev/packet_loop.py:3988–3990`.

Chốt mới chưa thực thi điều cấm “đích chứa dấu chéo ngược”. Trên POSIX, một tệp thường có thể mang chính byte đó trong tên. Khi symlink trỏ đúng tên ấy, `normpath` giữ nguyên, membership đạt, CLI trả rc 0, in `D2b ĐẠT` và `ĐÓNG ĐƯỢC WP`, trái kỳ vọng rc 12 `kiem_tep:not_measured:symlink` của luật được giao. Đã đo trên mã nguyên bản, Linux Python 3.13.18 và 3.12.3; không mô phỏng OS cho phản chứng này.

Quét cùng lớp: tên lá chứa dấu chéo ngược, thành phần thư mục chứa dấu đó, tệp mode100755 và symlink lồng đều lọt. Bằng chứng: `paths-3.13.18.json`, `paths-3.12.3.json`, `modes.json`; script tái hiện là fixture vô hại trong scratch, không phải patch sản phẩm. Không khẳng định Windows native cũng nhận tên literal này.

Hướng sửa: kiểm điều cấm trên đích thô trước chuẩn hoá, giữ phép so byte với tệp thường; không đổi dấu chéo ngược thành `/` hoặc gộp case/NFC. Khoá bằng ca cho từng biến thể trên và đột biến bỏ riêng điều cấm, cạnh đối chứng regular/executable/nested rc0 và YAML link rc12. Đề xuất là mô tả hướng, không có patch gate.

Đối chiếu lượt trước:

- `archive-loc-mat-du-lieu-kiem`: **VA_MOT_PHAN**. C03 case/NFC/backslash-alias của probe cũ: d5a7d85 rc0 → HEAD rc12 dưới mô hình tep. C05 còn mở cùng lớp.
- `symlink-tren-dia-lech-cay`: **VA_MOT_PHAN**, giữ alias của lớp trên, không đếm thành lớp mới.
- `hop-dong-dau-ra-duong-dan-tu-do`: **DA_VA_THAT**; LF ở cả passed/waived rc12 `duong_dan_sai`.
- C04: hành vi missing/file_parent trước `..` không đổi (rc12 ở cả hai head), nhưng quyết định chủ kho7180063460 đã siết K2 và thay tiêu chí cũ. Không gọi đổi acceptance là vá mã hay đóng cả lớp.

Hội tụ lớp lượt4→5: **0/1**; `lop_lap_lan_ba` vẫn chứa `archive-loc-mat-du-lieu-kiem`. Giữ lịch sử1/2/4/5 và trần6, không tự cấp vòng tiếp theo.

Các phép đo:

- 17/17 ca `cong_d2b_*` đạt, không skip; 17/17 `d2b_k2_*` bị đúng ca đích giết, đối chứng sạch.
- Ma trận36×7: baseline0 lệch; mỗi `cho_ten_lk8…lke` bị đúng một biến thể ChotB4 bắt. Các kết quả xanh này không phủ C05.
- Luật9 tái sinh228 mục khớp artifact, ledger225 GIET+3 TUONG_DUONG khớp byte; mẫu độc lập8 mục: {'SONG': 3, 'GIET': 5}, baseline16/16, rc0. Không khai chạy lại toàn bộ228/234.
- Legacy14/14 trên base và head. Corpus71 hồ sơ trong candidate cho cùng kết quả:51 đạt,10 failed,10 not_measured. `ops/land` có0 symlink. Ref origin/master thiếu trong checkout; phép so corpus dùng ref tổng hợp trong bản bare scratch, không chứng nhận remote authority hay76 hồ sơ của master mới.
- Ruff0.15.15: cả hai vế rc1,16 lỗi nền; delta0, pin/probe contract3 kiểm tra đạt. Diff +429/−13, đúng2tệp, trong trần450; `git diff --check f602325 HEAD` rc0. Snapshot Git và hash hai tệp trước/sau không đổi.

Bốn quyết định thiết kế: phạm vi cây con chặt hơn nhưng đã được điều phối đồng ý, không thấy chặn oan corpus hiện có. Mode100755 qua; gitlink160000 thật bị inventory chặn rc8. K2 non-YAML regular vẫn rc0, YAML link do module chặn12; symlink trước lỗi K1 vẫn là lý do đầu. Với đường không chuẩn tắc, native3.12/3.13 ra8 do filter đổi byte; mô hình giữ văn bản sau kiểm an toàn cho phép cả link hỏng chuẩn hoá trúng tệp, nhưng chưa dựng được đường phân giải thành thư mục. Vì vậy không tuyên bố mọi link hỏng đều bị chặn hoặc đã chứng minh mọi nền. Đích tuyệt đối chỉ phân tích bằng lời, không soạn payload; đích rỗng đo được rc8, không gọi là rc12 của membership.

M3 Windows **required**, reviewer **not_run**. Bằng chứng base118/118→head135/135, Python3.12.10, các biến thể lk4…lke là lời khai điều phối trong prompt/handoff, không phải phép đo của reviewer. Không dùng mô hình Linux để khẳng định NTFS chuẩn hoá NFC. Full A/B là log executor:38 ca và1mutant skipped mỗi vế; `r1187_spec_packet_type` đỏ sẵn ở cả hai. Không nâng skipped/not_run thành pass.

Identity: `openai_codex / codex_cli / machine/local`, run `845189ec5e834d1ba278b0b6c0b854c7`; model/effort phục vụ `KHONG_DO_DUOC`, effort yêu cầu high. Sandbox workspace-write, repository được giữ read-only theo thao tác; mọi artifact trong work/. Không gọi mạng/GitHub, không sửa/commit/push repository.

CHƯA ĐỦ ĐIỀU KIỆN MERGE: C05 P2 còn mở. Đây là verdict nội dung offline trên exact SHA, không cấp quyền merge/land.

KET_LUAN: changes_requested
