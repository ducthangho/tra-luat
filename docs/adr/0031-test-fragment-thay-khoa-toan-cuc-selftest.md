# ADR-0031 — Test fragment thay khóa toàn cục selftest

- **Trạng thái:** Accepted (2026-08-03, phiên grilling)

Write-set exclusion theo file là an toàn nhưng `scripts/tl_selftest.py` là nút cổ chai: trên 40 commit kết thúc
ở `origin/master` r324, tệp này bị chạm 18 lần và đã dài 28.144 dòng CRLF. Mỗi fix lại phải có regression test,
nên nếu mọi packet cùng sửa monolith thì hai worker code gần như không thể chạy song song.

`scripts/tl_selftest.py` vì vậy trở thành legacy harness ổn định. Test mới được viết thành fragment chính xác
`scripts/test_fragments/wp<issue>_<slug>.py`; worker auto-discover tất định và từ chối ID trùng, nên hai packet
có hai write set độc lập. Phiên land sinh bundled module `scripts/tl_test_fragments_bundled.py` tất định từ toàn
bộ fragment. Fragment vẫn được track để audit và chạy trong dev/CI nhưng bị loại khỏi release manifest; bundle
chỉ mang module sinh để không ăn trần 200 file. Bundled module là tệp phái sinh land-only và trở thành required
release file cùng lúc activation, không được bật required check trước khi generator/module đã land.

Không dùng `merge=union` cho Python: phép ghép theo dòng có thể đổi thứ tự và không chứng minh semantic merge.
Packet sửa harness, generator hoặc cùng chạm `scripts/tl.py` vẫn tuần tự; không cấp lease theo vùng dòng. Đổi lại
phải xây loader/generator và kiểm cả topology dev lẫn bundle, nhưng contention thường xuyên được chuyển khỏi tệp
2MB sang các fragment packet-owned.

Foundation thi công fragment harness trước maintenance EOL để giảm contention mà chưa cần cửa sổ freeze; mọi
writer của loader/generator phải ghi UTF-8 với LF tường minh, không dựa vào newline mặc định của Windows. Release
filter loại đúng prefix `scripts/test_fragments/`, không loại mọi thư mục trùng basename. Gate phải kiểm theo hành
vi: topology dev chạy fragment; topology bundle không chứa fragment nhưng chứa bundled module; thiếu module phải
fail với lỗi đích danh, không chỉ kiểm “tên thư mục có trong exclude list”.

Worker gate sinh bundled candidate vào thư mục tạm ngoài repo và kiểm byte/topology, không sửa module land-only
trong diff. Land gate dùng đúng generator đó để ghi module canonical; hai đường không được có generator riêng.

Resolver con trỏ tên ca phải lập chỉ mục cả registration `rNNN_*` trong legacy harness lẫn ID
`wp<issue>_<slug>` do fragment cung cấp, kèm phản chứng tên bịa. Nếu chỉ mở namespace mới mà không nối resolver,
điểm mù r326 sẽ tái xuất hiện nguyên vẹn.
