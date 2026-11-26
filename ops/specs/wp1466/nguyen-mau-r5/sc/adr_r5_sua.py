"""Ba chỗ sửa khối `adr` của r5 (Q3, Giới hạn, Phương án bị loại). Dùng: python adr_r5_sua.py <tệp> — sửa tại chỗ, mỗi chỗ đúng 1 lần."""
import sys
CU_Q3 = """của §12. Mỗi đơn vị có một ĐỊA CHỈ: đường tiêu đề đầy đủ của mục chứa nó và thứ tự của nó trong mục ấy. Cổng đỏ khi mục
ấy không có đúng một lần, khi đơn vị ở địa chỉ ấy lệch băm BYTE ghi trong mã, và khi cùng những byte ấy còn xuất hiện ở
một chỗ khác. Cổng không chọn câu đại diện và không nhận dạng viết tương đương: đổi một byte là đỏ. Nó cũng đỏ khi một ID
bất biến đứng trên một dòng bảng ngoài tiểu mục §1.1. Sửa một đơn vị khoá vì thế luôn đi qua một packet có review sửa mã
cổng. Không đọc được nguồn, hay nguồn có vùng mà cổng không phân tích được, là không đo được, và làm cổng đỏ.
"""
MOI_Q3 = """của §12. Mỗi đơn vị có một ĐỊA CHỈ: đường tiêu đề đầy đủ của mục chứa nó và thứ tự của nó trong mục ấy. Cổng đọc BYTE
THÔ của tệp; biên của mục và của khối chỉ là dòng rỗng, tức dòng không có byte nào. Cổng đỏ khi mục ấy không có đúng một
lần, khi đơn vị ở địa chỉ ấy lệch băm byte ghi trong mã hay có dòng nằm trong vùng không render, và khi còn một bản hiển
thị khác mang cùng những byte ấy. Cổng không chọn câu đại diện và không nhận dạng viết tương đương: đổi, thêm hay bớt một
byte trong khoảng dòng của một đơn vị là đỏ. Nó cũng đỏ khi một ID bất biến đứng trên một dòng bảng ngoài tiểu mục §1.1.
Sửa một đơn vị khoá vì thế luôn đi qua một packet có review sửa mã cổng. Không đọc được nguồn, hay nguồn có vùng mà cổng
không phân tích được, là không đo được, và làm cổng đỏ.
"""
CU_GH = """  phải sửa địa chỉ trong mã cổng ở cùng PR.
"""
MOI_GH = """  phải sửa địa chỉ trong mã cổng ở cùng PR.
- Số dòng rỗng không thuộc đơn vị nào: thêm hay bớt một dòng rỗng giữa hai khối, hay ở cuối một mục, không đổi đơn vị
  nào và không đổi thứ tự khối, nên cổng xanh. Một dòng chỉ có dấu cách, tab hay CR không phải dòng rỗng.
"""
CU_PA = """- Chuẩn hoá khoảng trắng trước khi băm: một khối thụt bằng tab thành khối mã mà băm không đổi.
"""
MOI_PA = """- Chuẩn hoá khoảng trắng trước khi băm: một khối thụt bằng tab thành khối mã mà băm không đổi.
- Đọc tệp qua lớp văn bản rồi cắt khoảng trắng cuối mục: lớp ấy đổi CR LF thành LF và bỏ dấu cách cuối dòng, nên bảy
  biến thể CR LF và hai biến thể dấu cách cuối qua được cổng (review đặc tả lượt 4).
"""
p = sys.argv[1]
t = open(p, encoding="utf-8").read()
for cu, moi in ((CU_Q3, MOI_Q3), (CU_GH, MOI_GH), (CU_PA, MOI_PA)):
    assert t.count(cu) == 1, cu[:60]
    t = t.replace(cu, moi, 1)
open(p, "w", encoding="utf-8", newline="\n").write(t)
print("ok")
