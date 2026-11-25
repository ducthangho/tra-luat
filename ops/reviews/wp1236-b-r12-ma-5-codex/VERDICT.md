Review mã wp1236 đợt B, r12/g1, lượt **5/6: approve**. Không phát hiện P0–P2 mới hoặc P3 mới sau một lượt quét toàn diff. Điều kiện nội dung còn lại của lượt 4 là B02, nay xử lý bằng lời miễn chủ kho neo exact SHA do điều phối cung cấp.

Ứng viên `bca55c1cd09c57180d60b05d5ca1813828ae1d10`, tree `14f1571aada834fc22ea32c29076df8834c05bd6`, base `f602325574c62184caf16309631f5f680ca5cee2`. SHA-256 spec `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`; bytes bản local khớp blob `e5583bc042448517b94eadda57231dfc60e0a284` tại base. HEAD/tree không đổi so lượt4. Diff đúng hai tệp write set, **506 dòng thêm ≤560**, 11 dòng xoá.

Provider/surface/transport: `openai_codex / codex_cli / machine`; run `a8703b65f7124891991a369b4672fcb5`. Model/effort phục vụ: `KHONG_DO_DUOC`; effort yêu cầu `high`. Linux, Python3.13.18, Ruff0.15.15. Sandbox thực tế `workspace-write`; checkout được xử lý read-only, mọi scratch/cache/output nằm trong `work/`, không dùng mạng.

| Lớp / finding | Đối chiếu lượt4 →5 | Bằng chứng / disposition |
|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` / B01 | `DA_VA_THAT` giữ nguyên | 810 ô B +8396 phần tử c36;648 ô c37 theo oracle độc lập,4 probe ngữ nghĩa;12+23 probe lịch sử đạt |
| Cùng lớp / B02 | Kỹ thuật vẫn `VA_MOT_PHAN`; `owner_waived` | Miễn trên đúng H; nợ `WP1236-B02-bat-bien-bo-sinh-test-dot-A` |

Lời miễn trích trong prompt từ [#1236 issuecomment-7156364013](https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-7156364013), thời điểm do điều phối cung cấp `2026-11-25T07:53:18Z`:

```text
mien_p3: bca55c1cd09c57180d60b05d5ca1813828ae1d10 nghiem-thu-khong-co-lap-chot-dich
```

Tôi **dựa vào trích dẫn do điều phối cung cấp**, không tự kiểm được tác giả comment hay đọc lại GitHub. Chỉ thị được cung cấp: “Cho miễn P3, ghi nợ và xử lý ở packet sau”. K5 của `kiem-merge` phải tự đọc dòng miễn trên GitHub. Đây là đóng điều kiện M1 bằng miễn, không phải bằng sửa mã; vì vậy bảng lớp vẫn `VA_MOT_PHAN`, hội tụ **lượt4→5 =0/1**, U có1 lớp, F rỗng. Giữ lịch sử lớp tái diễn ở lượt1–5 và checkpoint, không nâng tỷ lệ do miễn.

| Phép đo trong lượt5 | rc | Kết quả |
|---|---:|---|
| `python3 -B ops/land_evidence_nguon_test.py` | 0 | CA38/38; DOT BIEN145/145; TU KIEM2; TONG DAT |
| `python3 -B ops/land_evidence_nguon.py --root .` | 0 | 174 hồ sơ:149 ĐẠT +25 cutover;0 vi phạm;0 không đo được |
| Ruff `--no-cache --select F`, hai tệp head/base | 0/0 | 0 lỗi cả hai;delta0 |
| Ruff pin/probe contract, đo riêng | 0 | RUFF_CONTRACT3 [] |
| `git diff --check f602325574c62184caf16309631f5f680ca5cee2 HEAD` / numstat | 0/0 | Không lỗi whitespace;đúng write set và trần |
| Ledger và oracle c37 | 0/0 | Khớp từng phần tử hiện vật;648 ô đúng,4 đối chứng ngữ nghĩa |
| Probe lịch sử missing/scope | 0/0 | 12/12 và23/23 |
| Probe ưu tiên L8 độc lập | 0 | 4/4;56 băm khớp,0 giao với25 cutover |
| Kiểm hiện vật luật9 | 0 | Manifest550/624 tái sinh khớp byte;76 delta GIET và0 hồi quy kế thừa trong hiện vật |

Quét Spec và Standards/Security xác nhận: L5 cutover chạy trước L8; module từ `--root` nạp trước miễn L8; module thiếu trên hồ sơ được miễn L8 vẫn rc2 KHÔNG ĐO ĐƯỢC; lỗi nạp/chạy/SystemExit và kiểu trả về sai được xử lý. Miễn L8 gắn tên + băm chính byte đã nạp, không đọc lại đĩa hoặc xoá vi phạm luật khác. Phép đo dùng byte lệch trong khi đĩa giữ bản được miễn đã phát đúng L8 và “mất miễn trừ”. Một assertion của probe reviewer ban đầu đòi danh sách ghi chú chỉ có L8 nên đỏ do ghi chú L3 hợp lệ; đã sửa assertion trong scratch và chạy lại4/4. Không sửa sản phẩm.

Luật9: lượt5 **không chạy lại full `do`**, không nhận kết quả hiện vật là phép chạy mới. Kế thừa evidence lượt4 trên chính H:76/76 delta đã được reviewer lúc đó chạy lại,6 cặp kế thừa đã đo (5 GIET/GIET,1 SONG/SONG);542 cặp ngoài mẫu chưa được đo lại độc lập. B02 ngoài bảng đóng giữ nguyên nợ, không nâng thành P2.

**M3 Windows vẫn required.** Điều phối báo Windows local trên DESKTOP-T9R33P2 xanh đúng H:1786/1786 selftest,38/38 ca,145/145 mutant,tập ca đỏ `ci_duong_nhanh_test` bằng nền,delta0; nguồn [issuecomment-7161189686](https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-7161189686). CI PR#1526 xanh và connector completed/không finding cũng là lời khai trong prompt. Tôi không chạy hay xác minh độc lập các phần ấy; giữ `not_run`/reported riêng. Miễn Windows CI theo lease không viết lại thành pass.

Snapshot đầu/cuối: exact HEAD/tree, diff/index, untracked/ignored và băm 17938 tệp tracked giữ nguyên; chỉ có thư mục ignored `.codex/` rỗng sẵn có. Hai mốc không chứng minh toàn bộ lịch sử ghi. Command,rc thật,hash log,giới hạn và các trạng thái nằm trong [VERDICT.json](VERDICT.json). Đây là verdict mã offline; không cấp quyền merge/land hoặc chứng nhận human audit.

Kiểm schema: `python3 ../kiem_verdict_lop.py ../work/VERDICT.json --vong 5`; **rc 0, HOP_LE (§8.3): 0 finding, 1 lop**; stdout tại [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: approve
