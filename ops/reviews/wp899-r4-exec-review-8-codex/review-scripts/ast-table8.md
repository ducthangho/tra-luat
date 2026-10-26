| kiểu AST | số nút | toán tử / phép đo |
|---|---:|---|
| `Add` | 5 | Không có toán tử số học riêng; probe BinOp/AugAssign ở trên. |
| `And` | 17 | Được đổi qua BoolOp. |
| `Assign` | 21 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `Attribute` | 49 | Không có toán tử riêng; thử startswith/endswith, rstrip/lstrip, fullmatch/match, search/match; 2 survivor tương đương. |
| `AugAssign` | 1 | Không; đổi cộng thành trừ bị giết. |
| `BinOp` | 8 | Không; thử bỏ từng vế (Add/BitOr), không có survivor phân biệt được. |
| `BitOr` | 3 | Không có toán tử riêng; probe giữ từng vế BinOp. |
| `BoolOp` | 25 | Có: and↔or, bỏ từng vế. |
| `Call` | 109 | Một phần: chỉ bỏ đối số khi ≥2 đối số vị trí (14/109 nút); 95 nút còn lại không có toán tử riêng. |
| `Compare` | 37 | Có: DOI_SO_SANH, từng toán tử trong chuỗi. |
| `Constant` | 159 | Một phần: bool, int ±1, chuỗi khác rỗng; None/chuỗi rỗng không có toán tử riêng. |
| `Continue` | 1 | Không; chưa thử xóa Continue riêng. |
| `Dict` | 7 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `Eq` | 5 | Được đổi qua Compare. |
| `ExceptHandler` | 2 | Không. Bỏ RecursionError khỏi tuple bắt lỗi: mutant sống 52/52 và đổi A18 (F10/P2). |
| `Expr` | 11 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `For` | 3 | Không; các mẫu số bước/thứ tự được đo qua tests; chưa thử toán tử For riêng. |
| `FunctionDef` | 10 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `GeneratorExp` | 8 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `If` | 15 | Có: cố định test True/False. |
| `IfExp` | 12 | Có: lấy từng nhánh. |
| `In` | 6 | Được đổi qua Compare. |
| `Is` | 12 | Được đổi qua Compare. |
| `IsNot` | 2 | Được đổi qua Compare. |
| `Lambda` | 1 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `List` | 8 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `ListComp` | 7 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `Load` | 391 | Nút context, không có toán tử riêng. |
| `LtE` | 2 | Được đổi qua Compare. |
| `Name` | 321 | Không; thử đổi any/all tại tên hàm gọi, bị giết. |
| `NamedExpr` | 5 | Không; hai thay đổi h:=a/z bị giết; các binding khác chưa thử riêng. |
| `Not` | 11 | Được bỏ qua UnaryOp. |
| `NotEq` | 4 | Được đổi qua Compare. |
| `NotIn` | 7 | Được đổi qua Compare. |
| `Or` | 8 | Được đổi qua BoolOp. |
| `Return` | 20 | Có: tra_None (2 phép không đổi nguồn được loại đúng). |
| `SetComp` | 1 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `Slice` | 5 | Không có toán tử riêng; thử step/reverse/biên động. :1:2 sống nhưng tương đương. |
| `Store` | 66 | Nút context, không có toán tử riêng. |
| `Sub` | 1 | Không có toán tử riêng; probe giữ từng vế BinOp. |
| `Subscript` | 57 | Không có toán tử riêng; thử dịch i±1, GIET trong operator probe. |
| `Try` | 2 | Không có toán tử riêng; lỗ nhánh bắt lỗi như trên. |
| `Tuple` | 22 | Không. Tuple trong ExceptHandler là lỗ đã đo; xem gap8-results.json. |
| `USub` | 2 | Không có toán tử riêng (hằng int con vẫn được đổi). |
| `UnaryOp` | 13 | Một phần: bỏ Not (11/13); USub không có toán tử riêng. |
| `arg` | 21 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `arguments` | 11 | Không có toán tử riêng; các nút con có thể được đột biến. Chưa có mutant sống phân biệt được được chứng minh cho riêng kiểu này. |
| `comprehension` | 16 | Một phần: bỏ if-filter (4/16 nút có filter); không đổi iterable/target. |
| `keyword` | 1 | Không; key= của sorted chưa thử riêng. |
