verdict: blocked
reviewed_sha: 7f028a731c9b81c7c510edc881fddfa6977291a3
so_p1: 0  so_p2: 8  so_p3: 0
so_the_hien: 11

Không approve. `sensitive` cần approve tường minh. Có lỗi trong chính hợp đồng r4: A9 bỏ lọt phần viết trong merge; A17 loại phần M8 đang bắt buộc khỏi tập được thêm. Protocol §3.2 yêu cầu `blocked` và revision mới khi finding cho thấy spec thiếu. Không tự thay nghiệm thu bằng cách đếm khác hoặc tự mở write set. Các lỗi bộ đo là lỗi của bằng chứng dùng nghiệm thu, không tự nhận chúng là cổng sản phẩm đang chạy.

Review đã ghi tăng dần từ trước đối chứng; nhật ký giữ ở `probes/journal3.md`. Bản này tổ chức lại các phép đã chạy. Không sửa `cay-kho/`, không commit/push, không mạng, không transcript, không tự soạn payload tấn công. Các biến thể là Markdown/số học và bản sao bộ đo. Cây sao ở `probes/tmp/tree`; TMPDIR nằm trong sandbox. Tất cả kết quả dưới đây neo head ở đầu tệp, không neo `56cfce5`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| slug | phán canonical | cơ chế và phép tự đo |
|---|---|---|
| `sai-dai-luong-hoi-tu` | **ĐÃ VÁ THẬT** | `work-packet:167–187` khóa tử/mẫu vào tập slug lớp duy nhất; thể hiện chỉ truy vết. Mẫu 0 là không xác định; bỏ qua vòng đó khi xét chuỗi xác định. `review3.py prior`: unit/domain/sequence gốc True, bỏ từng chốt False; chuỗi `[1/3,None,1/3]` bắn, nhân thể hiện vẫn 1/3. Không yêu cầu reset chuỗi theo gợi ý reviewer cũ: quy tắc skip đã được khai rõ và vẫn giữ đầu ra M5. |
| `phep-do-doctrine-khong-du-rang` | **CHƯA VÁ** | Skill work:245–258 đã khai đúng giới hạn, không nhận đã đóng lớp. Nhưng `gates3.py scanner`: gốc 0; chép câu trần ADR 0; chép §5.1 0; chép §12 6. Hai phản chứng còn sống; A7/A13 vẫn được r4 kế thừa. Cải thiện lời khai không sửa cơ chế và không thay nghiệm thu. |
| `bien-goi-y-thanh-menh-lenh` | **ĐÃ VÁ THẬT** | `work:137–145` cho chọn khác, buộc tái dẫn xuất/tự đo/giải thích, giữ nghĩa vụ đóng cả lớp. `review3.py prior` kiểm từng chốt gốc True, gỡ False. Ca chọn sửa bộ sinh thay bộ đọc được phép nếu đủ ba điều kiện; chép hint mà chưa tự đo không đạt. |

Phép làm đỏ các bản vá trên KHÔNG tính vào tám hướng săn. Không có bản vá hội tụ/quyền chọn phương án bị mất trong merge. Slug doctrine giữ nguyên dù lời khai đã tốt hơn.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py prior`.

```text
unit original= True remove= False
domain original= True remove= False
sequence original= True remove= False
rates= [0.3333333333333333, None, 0.3333333333333333] stop= True
class_rate duplicated instances= 0.3333333333333333
được** chọn cách khác original= True remove= False
tái dẫn xuất original= True remove= False
tự đo original= True remove= False
giải thích original= True remove= False
doctrine limitation= True admits red cases survive= True
```

## BẢNG SĂN

Các phép đọc văn bản dưới đây là phản chứng hợp đồng, không giả chạy một executor. Phép đột biến parser đọc lại tệp sao trong `probes/tmp/`; không sửa nguồn. Bảng liệt kê cả kết luận không phải lỗi. Hướng 1 kiểm ranh giới mục, hướng 2 kiểm cardinality/ý nghĩa của bảng, hướng 8 kiểm oracle của runner: ba tầng độc lập, không phải đếm ba tên cho cùng một ca.

**HƯỚNG 1: Ranh giới mục của bộ đọc**

Giả thuyết: Bảng thiếu có thể được thay bằng bảng ở mục khác.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 1`

```text
missing stop table; later # table: (True, 'ok')
unit table removed locally; appended elsewhere: (True, 'ok')
unit header followed by another ##: (True, 'ok')
```

Kết luận: LỖI: chỉ dừng tại `## `; heading cấp `#` lọt. Bảng đơn vị tìm toàn tệp và tắt ranh giới. Hai đường đọc ngoài mục vẫn sống. Biến thể `#` là mục mới cấp cao hơn, không phải tiểu mục `###` còn nằm trong mục cũ.

**HƯỚNG 2: Cardinality và ý nghĩa của bảng**

Giả thuyết: Bộ đọc dùng tập/tên trường có thể làm mất số hàng hoặc đơn vị.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 2`

```text
4 data rows (duplicate sensitive): (True, 'ok')
wrong units: (True, 'ok')
```

Kết luận: LỖI: bốn hàng với sensitive trùng vẫn ĐẠT; đảo đơn vị thể hiện/lớp vẫn ĐẠT. Sản phẩm gốc đúng ở hai chỗ này; lỗi nằm ở sức phân biệt của bằng chứng nghiệm thu.

**HƯỚNG 3: A9 bỏ phần viết trong merge**

Giả thuyết: Hai khoảng diff bỏ sót resolution viết ngay trong merge.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 3`

```text
literal A9 before: 77	1	.claude/skills/cross-review/SKILL.md; 139	0	.claude/skills/work-packet/SKILL.md
literal A9 after: ''
literal total=216; second-path-count=0; EVIDENCE alternative total=410; final delta=194
fixture B->H= (2, 2) M->F= (2, 2) B->F= (305, 2) literal_sum= 4 hidden_merge_additions=301
```

Kết luận: LỖI: fixture đúng hai tệp ở cả hai khoảng, 2+2=4 nhưng delta cuối 305. Phần 301 dòng do resolution thêm không phải delta upstream. Mệnh đề “không thể che vi phạm” sai. Trên head thật tổng nguyên văn là 216 và khoảng sau rỗng; 410 là công thức khác.

**HƯỚNG 4: A17 với thêm dòng và nghĩa vụ M8**

Giả thuyết: Không xoá byte nào chưa đủ giữ nghĩa; whitelist có thể mâu thuẫn M8.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 4`

```text
cross delta additions= 55 deletions= 0
hunks: ['@@ -219,0 +220,18 @@ Hợp đồng `reviewed_sha` và xử lý khi head đổi: xem protocol §8/§13', '@@ -415,0 +434,37 @@ chọn tiến trình bằng mẫu và quan sát danh sách còn lại.']
add-only contradiction: minus= 0 A1= (True, 'ok') A2= (True, 'ok')
full A17 allowlist rejects added unrelated sentence=True; minus-only predicate=False
```

Kết luận: LỖI ở phạm vi nghiệm thu: +18 dòng M8 không thuộc A1'/A2'. Phản chứng thêm câu trái nghĩa vẫn −0 và A1/A2 xanh; toàn bộ whitelist A17 sẽ loại câu ấy, nên không nói spec hoàn toàn không cấm thêm sai. Chính phép tự phán chỉ dựa −0 là không đủ. Các byte #521 thật sự còn nguyên.

**HƯỚNG 5: Đích của con trỏ mới**

Giả thuyết: §3.2/§8/§12 có nội dung đúng như lời hứa hay không.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 5`

```text
3.2 review_class enum= True
8 contains definitions P1/P2/P3= [('P1', True), ('P2', False), ('P3', False)]
12 contains definitions P1/P2/P3= [('P1', False), ('P2', False), ('P3', False)]
12 recurrence= True
local max-severity / stable-slug= True True
```

Kết luận: KHỚP với trục review_class ở §3.2 và ngưỡng tái xuất hiện ở §12. LỖI ở lời hứa định nghĩa P1/P2/P3: §8 không có P2/P3, §12 không có cả ba; P1 ở §8 chỉ là nhắc tới. Mục tối đa severity và slug ổn định vẫn còn trong adapter.

**HƯỚNG 6: A16: số chi khác ngân sách**

Giả thuyết: Schema biên nhận xanh có thể không chứng minh số lượt CI đã chi bằng 0.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 6`

```text
pr529-review-1-codex-verdict.receipt.yaml top keys= schema_version,receipt_id,kind,packet_id,packet_slug,lease_id,lease_id_ghi_chu,phase_key,luot,role,provider,executor_provider,cross_provider,assurance,assurance_ghi_chu,verdict,verdict_path,verdict_sha256,verdict_bytes,reviewed_sha,reviewed_base,evidence_url,evidence_url_ghi_chu,verdict_sha256_do_tu_dau,phan_loai_finding,phan_loai_finding_ghi_chu,so_p1,so_p2,so_p3,so_the_hien,findings_ids,noi_dung_do_duoc_van_dung,model_reviewer_identity,nang_luc_do_cua_goi,hien_vat_reviewer_vao_kho,tuan_thu_cam_cua_reviewer,github_submitter_identity,anchor,khong_do_duoc,codex_connector_cung_head,delivered,delivered_by,authoritative_source,receipt_written_by,receipt_written_at_utc,recorder_cung_la_nguoi_thi_cong,receipt_khong_khai
explicit CI type-b count key= False
pr529-review-2-codex-verdict.receipt.yaml top keys= schema_version,receipt_id,kind,packet_id,packet_slug,lease_id,lease_id_ghi_chu,phase_key,luot,role,provider,executor_provider,cross_provider,assurance,assurance_ghi_chu,verdict,verdict_path,verdict_sha256,verdict_bytes,reviewed_sha,reviewed_base,evidence_url,evidence_url_ghi_chu,verdict_sha256_do_tu_dau,phan_loai_finding,phan_loai_finding_ghi_chu,so_p1,so_p2,so_p3,so_the_hien,findings_ids,doi_chieu_luot_truoc,noi_dung_do_duoc_van_dung,model_reviewer_identity,nang_luc_do_cua_goi,hien_vat_reviewer_vao_kho,tuan_thu_cam_cua_reviewer,github_submitter_identity,anchor,khong_do_duoc,codex_connector_cung_head,delivered,delivered_by,authoritative_source,receipt_written_by,receipt_written_at_utc,recorder_cung_la_nguoi_thi_cong,receipt_khong_khai
explicit CI type-b count key= False
```

Kết luận: LỖI ở biên nhận lượt 2: chỉ ghi N=0 và CI tự động chưa kết luận, không khai số loại (b) đã chi. KHÔNG PHẢI LỖI ở lượt 1: prose ghi N=0 và KHÔNG gọi CI tay, đủ nghĩa zero; không ép tên trường tự nghĩ ra. Không lấy session_run_id của reviewer làm CI run_id.

**HƯỚNG 7: Liên kết findings_ids với BẢNG LỚP sau rút gọn**

Giả thuyết: Có thể đọc cột 2 thành thể hiện và làm findings_ids đổi đơn vị.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 7`

```text
## `BẢNG LỚP`

Verdict **phải** mang mục này. **Mỗi finding thuộc ĐÚNG MỘT `lop_loi`** — finding không có lớp thì
verdict **thiếu**, không phải *"chưa phân loại"*.

| `lop_loi` | các slug thuộc lớp | **bản vá theo lớp** \| lý do vá lẻ |
|---|---|---|

Cột thứ ba là cột có răng: mỗi lớp khai **một thay đổi đóng cả lớp**, hoặc khai **lý do** phải vá lẻ.
Bỏ nó thì bảng tụt xuống thành bảng phân loại thuần.

| trường | đếm gì |
|---|---|
| `so_p1` · `so_p2` · `so_p3` | số **LỚP** ở mỗi hạng |
| `so_the_hien` | tổng số **THỂ HIỆN** |
| `findings_ids` | slug của **LỚP**, kebab-case |

Một LỚP = một **cơ chế** sinh cùng hình dạng lỗi; hạng của lớp là hạng **cao nhất** trong các thể
hiện. Slug là **khoá đếm** — giữ NGUYÊN qua các lượt cho cùng một lớp. Ngưỡng lặp lại và định nghĩa
P1/P2/P3: xem protocol `§8`/`§12`.

**Reviewer phải GỌI TÊN khi một vòng đóng finding bằng cách CẮT TIÊU CHÍ** hoặc thu hẹp phạm vi, chứ
đừng ghi nhận nó là đã vá.


binding phrase surviving merge= True unique class assignment= True
one class x, two instances x-1/x-2: required findings_ids=[x], so_p2=1, so_the_hien=2; instance IDs cannot replace class slug
```

Kết luận: KHÔNG PHẢI LỖI trên hợp đồng đọc toàn mục: mỗi finding đúng một lớp, findings_ids là slug lớp, lớp là cơ chế, slug giữ nguyên. Cột 2 không được đổi nghĩa khai tường minh của findings_ids. Chưa có validator so bằng tập; không tự coi thiếu cổng là lỗi mới vì spec nhận đây là kỷ luật đọc.

**HƯỚNG 8: runner A18 có phân biệt tiêu chí đích không?**

Giả thuyết: tổng rc khác 0 có thể ghi “giết” khi tiêu chí đích còn xanh.

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/harness3.py`.

Output thật, trích gọn:

```text
noop rc=1
A1'-1 ... DOT BIEN KHONG DOI GI ... ca nay KHONG DO GI
=== TONG: 6/7 bi giet ===
always_red rc=2
!! DOI CHUNG DUONG DO => bay ca duoi KHONG chung minh duoc gi
wrong_target rc=0
A1'-1 ... rc=1 GIET A1'=DAT A1 stub | A2'=DO A2 detects any text change
A1'-2 ... rc=1 GIET A1'=DAT A1 stub | A2'=DO A2 detects any text change
A1'-3 ... rc=1 GIET A1'=DAT A1 stub | A2'=DO A2 detects any text change
=== TONG: 7/7 bi giet ===
goc KHONG bi cham: DUNG
```

Kết luận: chốt no-op và đối chứng dương **KHỚP**; chốt tiêu chí đích **LỖI**. Fixture checker có lỗi được đặt trong bản sao, đối chứng gốc vẫn xanh. Đây không phải cáo buộc bảy ca gốc chết sai tiêu chí: output gốc cho thấy chúng chết đúng. Nó chứng minh runner không thực hiện hợp đồng “tiêu chí đích đỏ” của A18. Output đầy đủ: `probes/harness-noop.txt`, `harness-always_red.txt`, `harness-wrong_target.txt`.

## BẢNG ĐO

| lời khai/tiêu chí | phép đã chạy và kết quả | phán |
|---|---|---|
| Exact head + hai cha | `python3 probes/facts3.py`: HEAD đúng; tree `e7def178463b6547eb888a7dd02728b90075916e`; cha 1 `6b46012`, cha 2 `dc02c9b` | KHỚP |
| Spec hash | `sha256sum SPEC.md` = `78388d3e25f780fd18581a47353e5560965d92f2f347379ef5da235e1e941bfa` | KHỚP bản sandbox/lease; blob spec không có trên HEAD, không chứng thực lời khai đo từ ref nguồn |
| Hai verdict bất biến | `facts3.py`: bản cấp, blob HEAD, receipt hash/bytes đều khớp; mỗi bản có hàng Mục lục | KHỚP; không sửa byte nào |
| Hai patch được cấp | `facts3.py`: diff so master và diff phép merge bằng byte output git | KHỚP |
| #521 +247/−147 | `git -C cay-kho diff --numstat dc02c9b^1 dc02c9b -- .claude/skills/cross-review/SKILL.md`: 247/147 | KHỚP delta Git; thời điểm land GitHub KHÔNG ĐO ĐƯỢC |
| Xung đột 2 hunk/82 dòng | `facts3.py` chạy merge-tree trên DB sao: rc=1, 2 hunk [218,252], [450,500], 86 dòng gồm marker | 82 nếu bỏ hai marker biên mỗi hunk; 80 nếu bỏ cả separator. Không coi khác quy ước đếm là finding |
| 8/10 mẫu vắng | Bộ mười mẫu cụ thể không kèm lệnh trong bundle hiện tại | KHÔNG ĐO ĐƯỢC đúng phép này; không tự chọn mười mẫu để ra số đã khai |
| A1'/A2' gốc | `TMPDIR="$PWD/probes/tmp" PYTHONDONTWRITEBYTECODE=1 python3 probes/dotbien.py`: rc=0 dương | KHỚP nội dung gốc |
| A18 7/7 | Cùng lệnh: bảy ca rc=1; A1'-3/A2'-4 báo VẮNG BẢNG đúng mục | KHỚP bảy ca hữu hạn; không đủ chứng minh toàn hợp đồng |
| Gỡ bản vá ranh giới | `review3.py rollback`: A1'-3 trở lại `['lop_loi']`; A2'-4 trở lại bảng 4 cột | KHỚP lời khai chết sai lý do trước vá; còn đường khác ở hướng 1 |
| A17 +39/−0 | `git diff --numstat dc02c9b HEAD -- ...cross-review/SKILL.md`: **55/0**; hai hunk +18 và +37 | KHÔNG KHỚP 39; giữ byte cũ là thật; phán whitelist ĐẠT không đủ |
| A9 139+139 | Trước merge work +139; so master mới work +139; #521 không sửa work | KHỚP hai số, nhưng khoảng thứ hai không phải merge→head |
| A9 410, thực 194, chỉ fail-closed | `review3.py 3`: literal 216+0; mốc thay thế 216+194=410; delta master→head 194; fixture literal 4 < delta 305 | SAI lời khai về công thức và chiều khiếm khuyết |
| Scope sản phẩm | `facts3.py`: đúng hai skill + ops/reviews; 55+139=194 | KHỚP delta trực tiếp; không tự dùng thay A9 đã đóng băng |
| A3/M4, A4/M5, A5/M6 | Đọc work:148–210; cấm vá lẻ lần 3, công thức lớp/miền rõ, scope shrink không tính vá; cross:468 gọi tên | KHỚP văn bản; không giả đây là cổng thực thi |
| A6/M7, A8/M10 | Đọc bảng CI và đoạn giới hạn; N=0 trước merge, run_id hàng b, c cấm, 0 cổng nói rõ | KHỚP văn bản; lịch sử gọi CI KHÔNG ĐO ĐƯỢC |
| A7/A13 | `gates3.py scanner`: gốc 0, trần 0, §5.1 0, §12 6 | Lớp cũ CHƯA VÁ; lời khai giới hạn trong skill nay KHỚP |
| M8/M9 | Cross:220–236 giữ hai nguyên nhân + đo drift; work giữ ba nghĩa vụ hậu merge | KHỚP về giữ nội dung; A17 không cho phần M8 thêm vào (finding riêng) |
| A14 | `gates3.py gates`: bien-nhan rc=0, 2 biên nhận phân biệt; v2 rc=0, 116 ĐẠT, 11 legacy, 42 nợ, 0 vi phạm, 0 không đo được, tổng 169 | KHỚP; không suy ra A16 |
| A15/t27 | `gates3.py gates`: t27 chạy riêng rc=0, 1/1, bỏ qua 0; hai hàng index được đọc trực tiếp | KHỚP phần đã chạy |
| A16 | `review3.py 6` + đọc cả prose trong YAML | Lượt 1 đủ nghĩa zero; lượt 2 chỉ khai budget, chưa khai consumption |
| doctrine-scan | `gates3.py gates`: rc=0, 7 tệp | KHỚP output; không chứng minh không sao chép mọi doctrine |
| adr-song | Cùng script: rc=0, 48 ADR/48 dòng | KHỚP |
| idiom-ba-ten | rc=0, 9 đột biến, 7 tệp, bỏ qua 0, ĐẠT | KHỚP |
| doc-claims-check --strict | rc=0, strict=true | KHỚP |
| release-verify --strict --json | rc=0, ok=true, expected=checked=180, hash match=true | KHỚP |
| git diff --check rc=0 | `facts3.py`: so dc02c9b→HEAD **rc=2**, whitespace tại verdict lượt 1 dòng 117/118; diff working-tree trống thì rc=0 | Lời khai thiếu mốc. Không yêu cầu sửa hiện vật bất biến, không tạo lớp mới từ whitespace lịch sử |
| tl.py --selftest 1710/1710 | NOT_RUN | KHÔNG ĐO ĐƯỢC; không cần full selftest để phân xử hợp đồng văn bản đã blocked |
| lease-publish 155/155 | NOT_RUN toàn suite; chỉ t27 chạy riêng | KHÔNG ĐO ĐƯỢC toàn suite; suite chứa thao tác tạo commit và cài/lấy công cụ, không chạy dưới cấm commit/mạng của lượt |
| Sandbox false/abbrev7/sạch | `facts3.py`: shallow=false, abbrev=7, status rỗng; ancestry base→head rc=0 | KHỚP vế local |
| 361↔361, thiếu0/thừa1 nguồn↔mirror | Không có tập nguồn độc lập trong sandbox; không gọi ls-remote mạng | KHÔNG ĐO ĐƯỢC; số ref local không thay phép so hai nguồn |
| Bốn cổng nền↔sandbox | Đã đo vế sandbox trên bản sao cùng head | KHÔNG ĐO ĐƯỢC vế nền, không kết luận môi trường tương đương |
| Actions gate/thu-hoi; cancelled run; không CI tay | Chỉ EVIDENCE thuật lại | KHÔNG ĐO ĐƯỢC, không tính xanh/không tiêu CI |
| #521 lease + 358 ref/36 tệp | Theo chỉ thị chỉ ghi nhận, không tìm thêm | KHÔNG ĐO ĐƯỢC hai giả thuyết lease; không phán bên nào vi phạm |
| Hai lần grep khác nhau, harness từng đọc rc sai | Không có hai tiến trình/lịch sử gốc để lặp lại | KHÔNG ĐO ĐƯỢC sự kiện quá khứ; phép hiện tại lấy rc trực tiếp, dùng Python |
| M13/M14 không có cổng, probes nháp | Đã đọc skill và chạy probes tách biệt | KHỚP giới hạn; bộ đo vẫn là đối tượng review, không được miễn lỗi |
| Hiện vật lượt 3 sẽ đổi head | Chưa giao vào kho; M8 có tên nợ | Không phán trước approve còn hiệu lực trên head tương lai |

Lệnh cổng đầy đủ và output riêng nằm trong `probes/gates3.py`, `probes/gate-*.txt`; facts có JSON ở `probes/facts3.json`. Không dùng exit code của lệnh cuối một chuỗi làm rc cổng.

### phep-do-doctrine-khong-du-rang  [P2]  Danh sách cụm chưa đo được hai nhánh sao chép bắt buộc

CƠ CHẾ SINH LỚP: Scanner so cụm đã liệt kê, không đo mọi cách sao chép doctrine. Bản vá chỉ sửa claim, không thay cơ chế hoặc nghiệm thu A7/A13.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| D1 | work:245–258; A7/A13 kế thừa | Câu trần canon nguyên văn từ ADR-0043 thêm vào bản sao cross; scanner rc=0. |
| D2 | cùng cơ chế | Nguyên mục §5.1 thêm vào bản sao cross; scanner rc=0. |

VẤN ĐỀ: Không được coi khai nợ là đạt tiêu chí bắt buộc. Không có lỗi tự nhận “đã đóng” mới; phần lời khai của lượt 2 đã được sửa đúng.

ĐÃ THỬ VÁ: Không sửa scanner ngoài write set. Cần điều phối xử lý phạm vi hoặc revision nghiệm thu; không thay scanner bằng một predicate mới rồi khai A7/A13 đã đạt.

ĐÃ THỬ NGHIỆM: `python3 probes/gates3.py scanner`: 0/0/0/6; sao tạm phục hồi byte, bản review không chạm.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### bo-doc-bang-vuot-ranh-gioi-muc  [P2]  Bộ đo lấy nội dung ngoài mục đang nghiệm thu

CƠ CHẾ SINH LỚP: Ranh giới được nhận diện bằng đúng chuỗi `## `; riêng bảng đơn vị còn tắt kiểm ranh giới. Việc tìm toàn tệp cấp tín dụng cho một mục đã mất bảng.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| R1 | probes/do_a1a2.py:bang_sau; A1 | Thay bảng dừng bằng con trỏ, đặt bảng hợp lệ sau heading cấp # của mục khác: A1 True. |
| R2 | probes/do_a1a2.py:A2/dv | Header bảng đơn vị có thể đọc qua ## mới; chuyển bảng đơn vị sang phụ lục vẫn A2 True. |

VẤN ĐỀ: Lời khai đã sửa hết đường đọc sang mục khác không đứng vững. Bảy ca gốc được sửa đúng, nhưng phạm vi parser chưa được khóa.

ĐÃ THỬ VÁ: Chưa cung cấp patch sản phẩm. Hướng sửa: parse section theo cấp heading và khối bảng liên tục, neo bảng đơn vị vào đúng mục; dùng cả đối chứng heading # và ##. Chỉ sửa default bool không đóng đường A2 tắt guard.

ĐÃ THỬ NGHIỆM: `review3.py rollback` tái lập hai lỗi cũ; `review3.py 1` chạy ba biến thể mới trên tệp sao, đều True. Đừng dùng ca ### còn trong section làm bằng chứng vượt mục.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### bo-do-bang-chi-kiem-ten-khong-kiem-nghia  [P2]  Tập tên làm mất số hàng và đơn vị

CƠ CHẾ SINH LỚP: Chiếu bảng sang dict/tập hoặc chuỗi chứa tên trường làm rơi ràng buộc cardinality và quan hệ field→unit.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| N1 | probes/do_a1a2.py:A1/d | Bốn hàng data gồm hai sensitive trở thành ba khóa; A1 True dù spec đòi đúng ba hàng. |
| N2 | probes/do_a1a2.py:A2/phang | so_the_hien đếm lớp và findings_ids là slug thể hiện vẫn True; parser chỉ kiểm tên có mặt. |

VẤN ĐỀ: Không khẳng định bảng gốc sai: bảng gốc đúng. Claim rằng phép parse nghiệm thu đã đo số hàng/đơn vị là vượt sức đo.

ĐÃ THỬ VÁ: Hướng sửa trên bản sao bộ đo: kiểm số hàng trước khi dựng mapping, bác khóa trùng; kiểm từng giá trị đơn vị của cả so_p1/p2/p3, so_the_hien, findings_ids. Không thêm một từ khóa đơn lẻ để vá riêng fixture.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 2`: duplicate=True; wrong units=True; bản sao lưu/đọc lại từ đĩa.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### a9-bo-sot-delta-trong-merge  [P2]  Khoảng diff bỏ lọt phần resolution, không phải chỉ fail-closed

CƠ CHẾ SINH LỚP: Hai khoảng base→premerge và merge→final không bao phủ phần executor viết trong chính merge; EVIDENCE dùng master-mới→final thay khoảng thứ hai nên đánh giá sai cả số và chiều.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| G1 | SPEC.md:A9; LEASE:S2; EVIDENCE:A9 | Head thật literal=216+0 và 0 đường sau merge. Fixture hai tệp mỗi khoảng: 2+2=4, delta thực305, trong đó301 viết khi resolution. |

VẤN ĐỀ: Cấu hình phản chứng thỏa số đường ở cả hai khoảng và lọt trần300. Vì vậy “không thể che vi phạm” sai. 194 đúng với phép diff trực tiếp hiện tại nhưng chưa là sửa nghiệm thu được cấp quyền.

ĐÃ THỬ VÁ: Không sửa spec đóng băng. Cần revision định nghĩa quyền sở hữu delta resolution và neo hai cha/head; cách đếm phải đo cả merge resolution mà không cộng lại upstream. Fixture dùng các snapshot tệp và git diff --no-index, không tạo commit.

ĐÃ THỬ NGHIỆM: `review3.py 3`: B→H=(2,2), M→F=(2,2), B→F=(305,2). Chưa khẳng định công thức thay thế dùng được cho mọi cấu hình.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### a17-whitelist-bo-roi-m8  [P2]  A17 không cho phần M8 mà hợp đồng vẫn giữ

CƠ CHẾ SINH LỚP: Whitelist cross skill chỉ cho A1'/A2', nhưng M8 vẫn cần phần phân biệt nguyên nhân head đổi; self-pass đo −0 không kiểm các dòng cộng thuộc whitelist.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| W1 | SPEC.md:A17 so với M1–M12; cross:220–237 | Delta thêm18 dòng M8 ở hunk đầu và37 dòng ở hunk sau; tổng55/0, không phải39/0. M8 không thuộc A1/A2. |

VẤN ĐỀ: Giữ M8 là đúng mục tiêu; tự nhận toàn A17 đạt là không đúng hợp đồng hẹp đã viết. Xoá18 dòng để qua whitelist làm mất nghĩa vụ được giữ. Phải phân xử spec, không bắt executor tùy tiện chọn một phía. −0 chứng minh bảo toàn byte, không chứng minh bảo toàn nghĩa.

ĐÃ THỬ VÁ: Không xoá M8, không nới A17 tại chỗ. Hướng revision: đưa M8 vào phạm vi rõ nếu được chủ kho chọn; vẫn audit cả additions. Không yêu cầu đổi docs/protocol ngoài write set.

ĐÃ THỬ NGHIỆM: `review3.py 4`: +55/−0, hai hunk18/37; thêm câu phủ định giới hạn vào bản sao vẫn −0 và A1/A2 True. Whitelist đầy đủ bác câu đó; giới hạn là phép đo self-pass, không phải spec cho phép câu đó.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### con-tro-dinh-nghia-phan-hang-sai-dich  [P2]  Con trỏ không dẫn tới định nghĩa severity đã hứa

CƠ CHẾ SINH LỚP: Rút nội dung thành tham chiếu mà không kiểm đích chứa khái niệm được hứa.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| P1 | cross-review/SKILL.md:465–466 | Dòng “định nghĩa P1/P2/P3: xem §8/§12”; §8 không có P2/P3; §12 không có cả ba. Không có định nghĩa tương ứng ở hai mục. |

VẤN ĐỀ: Reviewer được dẫn tới nội dung assurance/budget thay cho định nghĩa severity. Đây là dòng thêm mới, không đổ toàn bộ thiếu sót nền của #521 cho packet. Phần trỏ trục §3.2 và ngưỡng tái xuất hiện §12 đúng.

ĐÃ THỬ VÁ: Chưa sửa nguồn. Xác định nguồn định nghĩa đang có thẩm quyền rồi trỏ đúng; nếu không có, báo điều phối thiếu nguồn, không tự đổi định nghĩa P1/P2/P3.

ĐÃ THỬ NGHIỆM: `review3.py 5` trích section chính xác và kiểm cả ba tên; đã đọc nội dung §8/§12. Không chỉ coi có chữ P1 là có định nghĩa.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### bien-nhan-thieu-so-ci-da-chi  [P2]  A16 bị bỏ qua bởi phép kiểm schema tổng quát

CƠ CHẾ SINH LỚP: Ngân sách N cho phép bị dùng thay số lượt thực đã chi; schema xanh không chứng thực nghĩa vụ A16.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| C1 | ops/reviews/pr529-review-2-codex-verdict.receipt.yaml:191 | Chỉ “M10 khai N=0” và CI tự động chưa kết luận; không nói đã chi0 lượt(b), không có danh sách run CI của chúng. |

VẤN ĐỀ: A16 yêu cầu phân biệt chưa chi với chưa ghi. Không dùng session_run_id làm CI. Lượt1 có prose KHÔNG gọi CI tay nên không là thể hiện của lớp này. Không bắt tên khóa reviewer tự nghĩ ra.

ĐÃ THỬ VÁ: Không sửa receipt nguồn. Executor cần khai consumption thực có căn cứ: 0 và danh sách rỗng nếu đã đo không có lượt(b); nếu không đo được thì khai không đo được. Không suy sự kiện Actions từ Git hay tự điền0 trong review.

ĐÃ THỬ NGHIỆM: `review3.py 6` liệt kê toàn khóa lồng nhau rồi đọc prose; `gates3.py gates` cho bien-nhan2/v2 xanh dù nghĩa vụ này thiếu. Schema-pass không tương đương A16-pass.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

### dem-dot-bien-khong-theo-tieu-chi-dich  [P2]  A18 đếm lỗi không đúng tiêu chí là giết

CƠ CHẾ SINH LỚP: Runner gộp hai tiêu chí thành một process exit code và dùng rc!=0 để cấp tín dụng cho mọi ca, làm mất liên kết ca→tiêu chí đích.

BẢNG THỂ HIỆN:

| id | vị trí | phép đo |
|---|---|---|
| T1 | probes/dotbien.py:dat = rc != 0 | Checker sao A1 luôn xanh, A2 đỏ khi văn bản đổi; đối chứng dương xanh, bảy ca “giết”, runner rc0; ba ca A1 không làm A1 đỏ. |

VẤN ĐỀ: Sai oracle có thể vượt cả positive-control và no-op-control. Không suy diễn rằng bảy ca nguyên bản đã sai đích; output gốc chứng minh ngược lại.

ĐÃ THỬ VÁ: Hướng sửa: mỗi ca khai expected target; đọc kết quả riêng A1/A2, yêu cầu target đỏ và kiểm non-target theo ca. Giữ đối chứng dương và chốt mutation thực sự thay đổi. Không dùng tổng số7 thay danh sách kết quả.

ĐÃ THỬ NGHIỆM: `python3 probes/harness3.py`: no-op rc1; always-red rc2; wrong-target rc0/7of7. Tất cả là bản sao riêng, không sửa hai probe được cấp.

ĐỘ TIN: cao về phép đo; không suy lịch sử hay authority ngoài sandbox.

## BẢNG LỚP

| lop_loi | các slug thuộc lớp | bản vá theo lớp hoặc lý do vá lẻ |
|---|---|---|
| `phep-do-doctrine-khong-du-rang` | `phep-do-doctrine-khong-du-rang` | Xử lý phạm vi/acceptance scanner với điều phối; giữ giới hạn đã khai đúng. |
| `bo-doc-bang-vuot-ranh-gioi-muc` | `bo-doc-bang-vuot-ranh-gioi-muc` | Khóa section và bảng theo cấu trúc, áp cùng nguyên tắc cho cả hai bộ đọc. |
| `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` | `bo-do-bang-chi-kiem-ten-khong-kiem-nghia` | Giữ cardinality và quan hệ field→unit trong phép đo. |
| `a9-bo-sot-delta-trong-merge` | `a9-bo-sot-delta-trong-merge` | Revision công thức để bao phủ resolution, kiểm đếm thiếu và đếm trùng. |
| `a17-whitelist-bo-roi-m8` | `a17-whitelist-bo-roi-m8` | Revision phân xử M8 và whitelist; audit cả cộng lẫn xoá. |
| `con-tro-dinh-nghia-phan-hang-sai-dich` | `con-tro-dinh-nghia-phan-hang-sai-dich` | Kiểm đích có định nghĩa đã hứa, trỏ nguồn có thẩm quyền. |
| `bien-nhan-thieu-so-ci-da-chi` | `bien-nhan-thieu-so-ci-da-chi` | Khai số đã chi riêng ngân sách, dựa bằng chứng thực. |
| `dem-dot-bien-khong-theo-tieu-chi-dich` | `dem-dot-bien-khong-theo-tieu-chi-dich` | Neo từng mutation vào tiêu chí đích, giữ các control đã đúng. |

findings_ids: [phep-do-doctrine-khong-du-rang, bo-doc-bang-vuot-ranh-gioi-muc, bo-do-bang-chi-kiem-ten-khong-kiem-nghia, a9-bo-sot-delta-trong-merge, a17-whitelist-bo-roi-m8, con-tro-dinh-nghia-phan-hang-sai-dich, bien-nhan-thieu-so-ci-da-chi, dem-dot-bien-khong-theo-tieu-chi-dich]

Đếm: **8 LỚP P2, 11 THỂ HIỆN**; không cộng các lớp cũ đã sạch, số đo khớp, whitespace hiện vật bất biến hoặc giới hạn môi trường vào findings. Bốn dòng đầu là kết quả hiện hành, không phải tổng lịch sử.

Provider: **OpenAI (`openai_codex`)**; vai: Codex reviewer khác nền executor Claude; bề mặt: **Codex service qua API**, công cụ shell sandbox; vận chuyển: **machine**, ghi tệp cục bộ, không đăng PR. Không tự chứng thực model ID/runtime hay launcher run ID không được công cụ cung cấp; không suy chúng từ tên tài khoản vận chuyển.

Không tra được trạng thái GitHub/PR/Actions hiện tại, lịch sử CI gọi tay, thời điểm/authority comment, tập ref nguồn trước clone, cổng phía môi trường nguồn, transcript, hoặc lease #521 đã xoá. Những sự kiện ấy chỉ là nguồn thuật lại; không coi không đo được là xanh hay bằng chứng không xảy ra.

**`VERDICT.md` là nguồn có thẩm quyền; comment PR chỉ là bản chiếu.** Không approve head này hoặc head tương lai. Kết thúc review với `blocked`: điều phối cần revision/lease phù hợp cho thiếu sót spec; executor tự tái dẫn xuất và đo các sửa đổi còn lại theo phạm vi được cấp.

### Phép đo đã chạy: 3

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 probes/review3.py 3`

```text
literal A9 before: 77	1	.claude/skills/cross-review/SKILL.md; 139	0	.claude/skills/work-packet/SKILL.md
literal A9 after: ''
literal total=216; second-path-count=0; EVIDENCE alternative total=410; final delta=194
fixture B->H= (2, 2) M->F= (2, 2) B->F= (305, 2) literal_sum= 4 hidden_merge_additions=301
```

## Hướng 8 — đo harness

`python3 probes/harness3.py`

```text
noop rc=1
=== DOI CHUNG DUONG (ban goc, chua dot bien) ===
  rc=0  A1'=DAT  ok | A2'=DAT  ok

=== BAY CA DOT BIEN — moi ca doi rc KHAC 0 ===
  A1'-1 sensitive thanh '0 P1 + 0 P2'        !! DOT BIEN KHONG DOI GI (mau khong khop) — ca nay KHONG DO GI
  A1'-2 gop routine voi systemic             rc=1  GIET  A1'=DO   tap review_class = ['routine` hoặc `systemic', 'sensitive'], doi {routine,systemic,sensitive} | A2'=DAT  ok
  A1'-3 thay CA BANG bang con tro tran       rc=1  GIET  A1'=DO   KHONG CO bang trong muc dieu kien dung (rong hoac vang) | A2'=DAT  ok
  A2'-1 bo cot 'ban va theo lop'             rc=1  GIET  A1'=DAT  ok | A2'=DO   BANG LOP co 2 cot, doi 3
  A2'-2 bo bang DON VI DEM                   rc=1  GIET  A1'=DAT  ok | A2'=DO   thieu bang DON VI DEM
  A2'-3 bo cau 'moi finding DUNG MOT lop'    rc=1  GIET  A1'=DAT  ok | A2'=DO   thieu cau "moi finding thuoc DUNG MOT lop_loi"
  A2'-4 thay CA MUC bang con tro tran        rc=1  GIET  A1'=DAT  ok | A2'=DO   KHONG CO bang trong muc BANG LOP (rong hoac vang)

=== TONG: 6/7 bi giet ===
CHOT MAT RANG (dieu kien dung S7 cua lease gen 3):
  - A1'-1 sensitive thanh '0 P1 + 0 P2'

goc KHONG bi cham: DUNG

always_red rc=2
=== DOI CHUNG DUONG (ban goc, chua dot bien) ===
  rc=1  A1'=DO   test all red | A2'=DO   test all red
  !! DOI CHUNG DUONG DO => bay ca duoi KHONG chung minh duoc gi

wrong_target rc=0
=== DOI CHUNG DUONG (ban goc, chua dot bien) ===
  rc=0  A1'=DAT  A1 stub | A2'=DAT  A2 detects any text change

=== BAY CA DOT BIEN — moi ca doi rc KHAC 0 ===
  A1'-1 sensitive thanh '0 P1 + 0 P2'        rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change
  A1'-2 gop routine voi systemic             rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change
  A1'-3 thay CA BANG bang con tro tran       rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change
  A2'-1 bo cot 'ban va theo lop'             rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change
  A2'-2 bo bang DON VI DEM                   rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change
  A2'-3 bo cau 'moi finding DUNG MOT lop'    rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change
  A2'-4 thay CA MUC bang con tro tran        rc=1  GIET  A1'=DAT  A1 stub | A2'=DO   A2 detects any text change

=== TONG: 7/7 bi giet ===

goc KHONG bi cham: DUNG
```
