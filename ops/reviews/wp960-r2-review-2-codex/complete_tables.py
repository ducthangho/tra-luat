from pathlib import Path
p=Path('VERDICT.md');s=p.read_text()
s=s.replace('Đang đối chiếu phản chứng cũ.', '''| slug lượt 1 | trạng thái | lệnh chạy lại trên HEAD | output thật |
|---|---|---|---|
| git-hong-thanh-token-thuong | ĐÓNG phản chứng cũ; còn đường object rỗng ở finding mới | `python3 -u probe_review.py boundaries` và `rawcli` | Cùng OID thuần chữ `dbffbbc…`, git lành rc=1; PATH không git rc=2, không traceback; c91/m103 giết vì fixture git_vang, không phải lỗi khác. |
| b2-chua-do-du-ma-tran | ĐÓNG | `python3 -u probe_r2.py matrix`; `python3 -u probe_review.py errors` | c91 14/14 lời gọi main rc=2, đủ receipt-thư-mục / alias vòng / ref tree thật × có/không nợ; stderr nêu nguồn, không NỢ CHẾT/Traceback. JSON hỏng vẫn có c77 và phản chứng CLI reviewer. |
| run-json-thu-muc-thanh-khong-ap | ĐÓNG | `python3 -u probe_review.py errors`; `python3 -u probe_r2.py symlinks` | run-directory cả hai trạng thái nợ rc=2, không NỢ CHẾT; m106 chết đúng run_json_thu_muc. |
| nhanh-mac-dinh-tree-bi-bo-qua | ĐÓNG phản chứng tree; còn ref hỏng theo finding mới | `python3 -u probe_review.py auxiliary`; `python3 -u probe_r2.py refs` | Ref tree thật không fallback, KhongDoDuoc và CLI rc=2; ref vắng thật vẫn fallback; m104 chết đúng nhanh_la_tree. |
| sinh-no-ngoai-bien-doc-receipt | ĐÓNG MỘT PHẦN | `python3 -u probe_review.py auxiliary`; `python3 -u probe_r2.py matrix` và `yaml_errors` | Phản chứng cũ IsADirectoryError đã rc=2 ở cả hai cờ; c92 cũng khóa byte UTF8/YAMLError. Timestamp sai và YAML lồng sâu vẫn `--sinh-no` traceback/rc=1, finding sinh-no-van-thoat-loi-yaml. |
| bien-utf8-receipt-chua-co-rang | ĐÓNG | `python3 -u probe_mutations.py r8-receipt-encoding`; mutation m107 ở `measure_target_mutants.py` | Bỏ riêng UnicodeDecodeError làm c91 đỏ đúng nguồn receipt UTF8; nguyên trạng subprocess rc=2; mutant subprocess rc=1/Traceback. |
| b6-docstring-chua-khai-gioi-han | ĐÓNG | `python3 -u probe_r2.py matrix`; selected m78 trong `measure_target_mutants.py` | Docstring nói rõ >- chỉ hồi quy/không có chốt riêng. m78 giết đúng khoi_lit, danh sách bị nhận vẫn có khoi_gap. |
| bo-chon-moi-chua-khoa-bien | ĐÓNG | `python3 -u probe_mutations.py r2-commit-boundary r4-backtick-close r5-provider-boundary r6-window-next`; selected m110–m113 | Từng guard cũ đều bị c87/c88 giết đúng assertion Precommit / backtick-chi-mo / notprovider / provider-dong-sau. Không dùng thất bại giàn giáo làm răng. |

Log: `evidence/old-{boundaries,errors,auxiliary,rawcli,mutants}.log`, `evidence/matrix.log`, `evidence/target-mutants-final.log`. 7 finding đóng phản chứng cũ, 1 đóng một phần; đóng phản chứng cụ thể không đồng nghĩa lớp lỗi đã đóng.''')
s=s.replace('`ops/bien_nhan_v2.py:1159`–`1164`','`ops/bien_nhan_v2.py:1152`–`1156`')
s=s.replace('`ops/bien_nhan_v2.py:1117`–`1123`, `1142`','`ops/bien_nhan_v2.py:1120`–`1124`, `1141`')
p.write_text(s)
