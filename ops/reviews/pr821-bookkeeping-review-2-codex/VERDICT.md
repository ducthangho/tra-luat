Reviewed commit: a982787024a953a6266aa33c842453deadafd1f3
Verdict: approve P1=0 P2=0 P3=0

Reviewer: Codex, provider OpenAI, phiên API có shell cục bộ, transport machine. Review độc lập với executor Claude; không xác nhận model ID/effort của từng request. Authority/phạm vi theo yêu cầu cross-review lượt 2 của chủ kho. KHO `/home/user/rv773` chỉ đọc; không fetch, không gọi mạng, không sửa ref hay cấu hình. `git status --porcelain` đầu/cuối rỗng. Tree head: `05d7882d9c8f1198cd909a0608a0a716a4a36f90`.

## Findings

Không phát hiện P1/P2/P3 trong phạm vi yêu cầu. Hai finding lượt 1 đã đóng thật:

- F01: `merge-d8b15cb.txt` có đầy đủ OID, hai cha và tree, được ba lời khai cha/tree trỏ trực tiếp. Lời khai event trỏ `readback-events-779.json`, chứa actor/time/app tương ứng. Không suy từ hai cha thành không conflict, hoặc từ app null thành người bấm tay.
- F02: tiêu đề không còn khai checkout master chưa đo. Transcript mới ghi HEAD `8e150cf0d9f046a761c49448c8173ad501f53a1c`, tree `6e8e27cde969a7b6bd8a54758bda4b24508ad18f`, hash script và đủ lệnh 14+1 tên. `git rev-parse 8e150cf '8e150cf^{tree}'` khớp. `git diff 8e150cf a982787 -- .claude/dev/packet_loop.py` rỗng; hash script hiện tại cũng đúng `c15ac9330a084d4a10d559885dbeb606c841ca4ad22a6ca51686c681e59f8634`. Đây là phép đo offline trước commit vá, được khai đúng; không tự nhận chạy trên a982787 hay chạy mới CI.

## Đã đo

Đọc cả hai commit message, diff `924527c..8e150cf`, `8e150cf..a982787` và toàn PR. Toàn PR hiện đổi 6 tệp (thêm transcript merge ở lượt 2); YAML chỉ bổ sung nguồn và giải thích phạm vi 14+1, không đổi nghĩa nghiệp vụ.

Lệnh cổng:

```sh
git -C /home/user/rv773 show e0e0eac:ops/land_evidence_nguon.py > /tmp/len.py
python3.13 -B /tmp/len.py --root /home/user/rv773
mkdir -p /tmp/rv821-r2-base
git -C /home/user/rv773 archive 924527c | tar -x -C /tmp/rv821-r2-base
python3.13 -B /tmp/len.py --root /tmp/rv821-r2-base
```

Head rc=0: `2 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC`, `TỔNG: ĐẠT`. Base rc=1: đúng 6×L1 ở post_merge_checks[0/2/3], spec.nguon, merge_3, review.codex_connector. Log: [head-gate.txt](head-gate.txt), [base-gate.txt](base-gate.txt).

Chạy lại mọi lệnh trong cả bốn transcript, dùng Python3.13 `-B`, đường dẫn tuyệt đối cho script và JSON. Đã đọc `kiem-gate --help`; lệnh đầy đủ và rc thực trong [measured-r2.txt](measured-r2.txt), script tái hiện [audit821r2.py](audit821r2.py).

| Nguồn / lời khai | Kết quả đối chiếu |
|---|---|
| cha-d347d42.txt | ancestor rc=0; cha thứ nhất d347d42 là d8b15cb, cha thứ hai `76014ce0e76df70d8d3655b8f130747ae4d2cc14` |
| merge-d8b15cb.txt | merge `d8b15cb0730c85e7019aee627c3bfa645a6d3eaf`; cha `73bf92c0db05fead9d7e98c7b4f3643bd72bfcd8` + full f9d84d7; tree `6474598db320df3de03d0251ba9305dde1875b3f`, khác head tree `4e712f37bf014e18e87df07d0f94d0ba353fb3e7` |
| spec-wp775.txt | ref `219dcdaa9d164b8cf7dabb4c126bbfe0e65dfdb7`; blob `898369502c3ad4e4001e9f25692af61d2bf80102`; SHA256 `4b7530c265dddefbebd06ea209d7c0594210f57b391e0d0d353931171fd2b6d8`; cat-file trên origin/master rc=128 vì path vắng; origin/master đúng base `924527c2d67ae36bb20a80147e687a823564ad90` |
| post_merge_checks[0] | attempt 1 cancelled, updated 17:27:24Z; run d347d42 created 17:27:23Z; giữ giới hạn không đo actor/nguyên nhân |
| post_merge_checks[2] | attempt 2 success đúng d8b15cb, 14/14 jobs success; run_started_at 2026-10-18T01:23:44Z, updated 01:52:05Z; thread 4305258340 hiện diện trong readback-review-comments-811.json |
| post_merge_checks[3] | run 39053830242 success đúng d347d42, 14 jobs success, updated 2026-10-17T17:59:39Z; nguồn Git chứng minh cha trực tiếp |
| bookkeeping[0/1] | #775 closed/completed, closed_at 2026-10-17T17:29:48Z, closed_by ducthangho; comment 6237647158 đúng; mở đủ JSON 804–810: cả bảy open, tiêu đề (1/7) đến (7/7) |
| merged_nguon / uy_quyen_land | REST merged=true, merged_at 16:55:50Z, account ducthangho, head/merge SHA khớp; event merged actor ducthangho lúc 16:55:51Z, app null; cha/tree có nguồn Git riêng |
| merge_1 | VERDICT neo full f9d84d7, approve P1=P2=P3=0; SHA256 `a1957436163a0d921b5c29523bd278c82a570307279e0c23e4bf1cf15b62234f` |
| merge_3 | run 39047604566 attempt 2 success đúng full f9d84d7, suite 105821166384; chạy 14 tên suite này rc=0 và thu-hoi suite 105821159612 rc=0; tất cả 15 check ID khớp transcript |
| review.codex_connector | receipt neo f9d84d70fb, không major issue; state full cùng SHA, completed, hai cờ findings=true; lời khai không suy thành sạch |

`merge_3` “15 ten rc=0” trung thực khi đọc cùng phần giải thích 14+1 và pre_merge_checks vốn đã khai run riêng. Không có phép đo một lần gọi chung 15 tên cùng suite. JSON có 16 check runs: 14 CI success + thu-hoi success + launcher skipped ở suite 105821166619. Không che check bắt buộc đỏ; không nhận launcher skipped là pass.

Dùng chính `duyet` / `token_nguon` / `phan_giai` của bộ kiểm để duyệt đủ 13 chuỗi bắt đầu measured, mở nguồn từng chuỗi và đối chiếu các vế. Tất cả token phân giải thành công nằm trong provenance tương ứng; không có trường hợp qua nhờ tên tình cờ tại ops/land hoặc gốc kho. `ci.yml` và `ops/specs/wp775.md` không phân giải nhưng các lời khai ấy có nguồn đúng khác. Không phát hiện con trỏ có sẵn nào qua cổng mà không chứng minh phần measured sau bản vá.

Cũng đọc hai trường lease có measured ở giữa chuỗi: bốn output ai-dang-giu khớp rc=11 và người giữ wp775 trước / wp788 sau bia mộ. Hai tập lưu có 592 tên mỗi tập, sau chuẩn hóa tiền tố dict tên→OID bằng nhau; luc-do.txt ghi 02:03:33Z. Đây là đối chiếu hiện vật đã lưu, không tái chứng nhận fetch/remote của phiên lịch sử.

```sh
cd /home/user/rv773/ops/land/pr779-wp775-provenance
sha256sum -c SHA256SUMS
```

rc=0, 44/44 OK. So tập đường dẫn sau bỏ `./`: 44 tệp ngoài SHA256SUMS, 44 dòng; thiếu=0, thừa=0, trùng=0.

Không thấy transcript khai vượt phép đo sau vá. Các mốc giờ trong tiêu đề là metadata phiên được ghi lại, không phải thời gian có thể độc lập tái chạy; không biến chúng thành chứng nhận thời điểm lịch sử. “Spec chưa vào master” được hiểu là path vắng ở tip master đã đo, không phải khẳng định chưa từng xuất hiện trong toàn lịch sử.

## Ngoài phạm vi

Không chạy CI thực, không tái review runtime wp775 hay bảy nợ #804–#810; không xác minh người bấm merge, credential, model lịch sử, thời điểm fetch hoặc giải quyết thread không được lưu. Không thay chủ kho quyết định landed/merge_4. L1 chỉ đo nguồn tồn tại; kết luận về nội dung ở trên dựa vào review trực tiếp, không suy từ cổng xanh. Không có finding ngoài phạm vi mới.
