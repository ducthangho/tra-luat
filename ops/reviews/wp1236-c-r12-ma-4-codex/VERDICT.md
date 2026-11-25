**changes_requested — wp1236 C r12, lượt 4/6.** Có hai finding mở: C03 P1 và C04 P2, cùng lớp `archive-loc-mat-du-lieu-kiem`. Bản vá đóng cơ chế Windows cùng tên đã báo, nhưng phép so khớp chuỗi đích còn bỏ sót alias và chặn thừa đích hỏng. Những phản chứng mới là phép đo mô hình hệ tệp, không phải kết quả Windows native.

Reviewed SHA: `d5a7d8510af03e0d08545f677ad5de687e0264f4`; tree: `241bd084f5979b02a1221d7d645e113227feee59`.
Parent lượt 3: `dbe650d2a3c3fb6da9573ea485adc65934efdc78`; base: `f602325574c62184caf16309631f5f680ca5cee2`.
Spec SHA256: `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`, blob `e5583bc042448517b94eadda57231dfc60e0a284`, revision12/generation1. Lease/write set đúng hai tệp Python; +420/−13, dưới trần450. Snapshot Git trước/sau giống nhau. Repository được giữ read-only; mọi bản sao/thử nghiệm ở `work/`, không gọi mạng.

Reviewer: `openai_codex / codex_cli / machine/local`, CLI0.170.0, run `f21c6446bf6741959a71c4ca1a4ca208`. Model và effort phục vụ: **KHÔNG ĐO ĐƯỢC** từ run; high là yêu cầu. Wrapper khai generic `local_process/subprocess/machine`, executable là Codex CLI. Sandbox thực tế workspace-write; reviewer tuân thủ read-only, không tự nhận sandbox read-only. Linux, Python3.13.18; đo đối chứng một số đường bằng `/usr/bin/python3` 3.12.3. Không tự cấp assurance hay quyền land.

| Lớp | Đối chiếu HEAD | Mức mở cao nhất | Vá chung và phép đóng lớp |
|---|---|---|---|
| `archive-loc-mat-du-lieu-kiem` | `VA_MOT_PHAN` — biểu hiện cũ đã đóng; bản vá sinh C04 và chưa đóng C03 | P1 | Bảo toàn cây và phân giải đúng đối tượng K2 theo semantics đa nền. Đóng bằng C01 cũ, C4, alias case/separator/NFC, intermediate missing/file và Windows native. |
| `hop-dong-dau-ra-duong-dan-tu-do` | `DA_VA_THAT` | — | Giữ miền ký tự owner đã chấp thuận; LF trong passed/waived đều rc12, ca miền ký tự và mutant đạt. |
| `symlink-tren-dia-lech-cay` | Alias của C01, `VA_MOT_PHAN`; không tạo lớp độc lập để đặt lại bộ đếm | C03 P1, C04 P2 | Cùng cách vá và phép đóng C01. |

C01 xuất hiện ở lượt1, lượt2, lượt4: **lần thứ ba**. Owner đã quyết “Vá + nâng trần6” theo chỉ thị được cấp (issuecomment-7170968907); review này không tự gia hạn hay mở rộng Packet. `|F|/|U|` lượt3→4 là **N/A (0/0)** vì cuối lượt3 không có lớp mở; không ghi 100%. Hai finding mới gộp dưới C01 vì cùng mất tương ứng giữa cây Git, bản bung và đối tượng K2.

**C03 — P1: phép giao chuỗi chính xác vẫn cho thư mục qua K2 khi tên/separator có alias.** Vị trí: [packet_loop.py:3987](../repo/.claude/dev/packet_loop.py#L3987), đoạn tính `thu_cay`, `tro`, `thu_cay & tro`.

Guard chỉ dùng `posixpath.normpath` rồi so tên nguyên trạng. Inventory vẫn có đủ tên, loại, hash: một tên thư mục duy nhất không kích hoạt kiểm va chạm NFC/casefold. Nếu chuỗi đích chỉ khác hoa/thường, hoặc dùng dấu phân cách Windows, guard không tìm thấy thư mục. Khi symlink được liệt kê trong nhóm tệp và tên link không kết thúc `.yaml`, module cũng bỏ qua; CLI in `D2b ĐẠT` và `ĐÓNG ĐƯỢC WP`.

[models.json](models.json), do [probe_models.py](probe_models.py) chạy, ghi cùng product nguyên vẹn và cùng Git tree:

| Mô hình alias | previous, walk thường | HEAD, walk thường | previous, walk `tep` | HEAD, walk `tep` |
|---|---:|---:|---:|---:|
| Khác hoa/thường | 12 | 12 | 0 | **0** |
| Separator Windows | 12 | 12 | 0 | **0** |
| Tên tương đương NFC/NFD | 12 | 12 | 0 | **0** |

Mỗi bản ghi có raw_target, physical_target, `referent_is_directory=true`, stdout/stderr thật. Mô hình thay cách hệ tệp phân giải alias, giữ `readlink` nguyên chuỗi và xếp link vào danh sách tệp; không thay mã sản phẩm/Git/hash/oracle. Cặp walk thường rc12 kiểm chứng module nhận đúng K2 khi hệ tệp phân loại link là thư mục. Mô hình case/separator mô phỏng cơ chế Windows đã được điều phối mô tả; **chưa đo native cho các ca mới**. NFC là mô hình hệ tệp tương đương tên, không phải khẳng định NTFS chuẩn hoá NFC. Linux case-sensitive nguyên trạng không phân giải alias nên rc0 ở đó không tự nó là lỗi.

Đề xuất: sửa resolver ngay trước guard, duyệt từng thành phần theo inventory Git với chính sách tên/separator tường minh cho các nền hỗ trợ. Giữ raw bytes để kiểm hash. Thêm oracle alias rc12 dưới `tep`, rồi chạy native Windows với link tạo trước đích; đối chứng file không `.yaml` vẫn rc0. Bổ sung mutant resolver vào manifest Luật9. Rủi ro: casefold hoặc đổi separator vô điều kiện có thể làm sai miền POSIX; chỉ thay phép giao bằng casefold là chưa đủ.

**C04 — P2: `normpath` xoá thành phần thiếu hoặc là tệp thường trước `..`, gây chặn thừa.** Vị trí: [packet_loop.py:3988](../repo/.claude/dev/packet_loop.py#L3988).

Đích có thành phần trung gian không tồn tại, hoặc là tệp thường, rồi tới `..` và tên thư mục thật không phân giải thành thư mục. Link không `.yaml` này nằm ngoài K2. `normpath` vẫn rút gọn thành tên thư mục có trong `thu_cay`, khiến guard mới trả `not_measured:symlink` trước khi module xét hồ sơ.

[models.json](models.json), các scenario `missing` và `file_parent`: previous rc0 có `D2b ĐẠT`; HEAD rc12 `kiem_tep:not_measured:symlink`, ở cả walk thường và `tep`. Bản ghi xác nhận `is_symlink=true`, `referent_exists=false`, `referent_is_directory=false`. Hồ sơ nền là fixture provenance hợp lệ, các bước D1–D4 khác giữ nguyên.

Phép đo này giữ nguyên linkname sau khi chạy safety filter, mô phỏng tar giữ nguyên chuỗi đích. Trên Linux native Python3.13.18/3.12.3 được cấp, data filter đổi chuỗi đích, nên cả previous và HEAD đều rc8 vì hash không khớp: **không tuyên bố đã đo hồi quy native**. Cũng **chưa tìm thấy hồ sơ thật hiện có bị chặn oan**: `ops/land/` tại HEAD có0symlink; 71 hồ sơ local được chạy qua previous/HEAD cho kết quả giống từng dòng. Finding là hồi quy hợp đồng K2 đo được dưới điều kiện bộ giải nén giữ chuỗi, không phải sự cố corpus đang có.

Đề xuất: resolver chỉ xử lý `..` sau khi đã xác định thành phần trước là thư mục và đã xử lý link theo cây. Giữ phân biệt missing/file/directory và vòng; không đổi thành cấm mọi symlink. Khóa bằng cặp đối chứng giữ linkname: intermediate directory rc12, missing/file rc0 khi K1/K2 khác hợp lệ; đo lại Windows3.12.10. Rủi ro: thay resolver có thể ảnh hưởng link chain, vòng, ra ngoài gốc; phải giữ safety filter, hash và giới hạn bước.

**Quét các đường cùng lớp.** Kết quả `tep` dưới đây là mô hình, kể cả khi chạy trên Linux; chưa thay thế native Windows. `paths-3.13.18.json` và `paths-3.12.3.json` gồm12 scenario ×2product ×2walk cho mỗi interpreter. Với matrix, chỉ4mutant guard mới được chạy đủ29biến thể; toàn bộ53mutant D2b được chạy riêng với ca khai báo. Không nhận đã độc lập chạy matrix29×16.

| Đường | Phép đo/đọc độc lập | Mutant/giới hạn |
|---|---|---|
| Link tạo trước thư mục đích, cùng tên | `direct`, C4 lk4: previous tep0→HEAD12; native Linux12 | `d2b_k2_tin_dia`, `d2b_k2_dich_tho` bị ChotB4; thứ tự tar là cơ chế được cấp |
| Đích chứa `/`, thư mục con | `slash_target`, `nested`, C4 lk7: tep0→12; native12 | `tin_dia`, `dich_tho`; native Windows của reviewer chưa đo |
| Gốc bản bung, `..` qua thư mục có thật | `root`, C4 lk6: tep0→12; native12 | `d2b_k2_bo_goc`, `tin_dia`, `dich_tho` |
| Link→link→thư mục | `chain`: tep0→12; native12 | Đo riêng không có mutant chain chuyên biệt. Lập luận terminal link đúng với tên/separator được resolver nhận, không chữa C03 |
| Vòng link không `.yaml` | `cycle`: cả previous/HEAD, cả walk đều0 | Không có đích thư mục; ngoài K2. Chưa có mutant vòng riêng |
| Link file không `.yaml` | `file_link`, C4 lk5: cả hai0 | `d2b_k2_moi_symlink` bị giết bởi ca này và mô hình lk5 |
| Link `.yaml` cùng provenance thường | `yaml_link`, probe C01 cũ:12; module trực tiếp cũng not_measured:symlink | `d2b_loc_mat_symlink` và các mutant inventory/hash C4 đều GIET; việc bắt `.yaml` vẫn ở module |
| Alias case/NFC/Windows separator | models.json: plain12, tep0 | C03; bộ ca khai báo chưa khóa oracle này; không tạo mutant sản phẩm ngoài manifest |
| Intermediate thiếu/tệp thường trước `..` | models.json: previous0→HEAD12; native hai Python8/8 | C04; không có mutant chuyên biệt được chạy |
| `..` sau link | Phân tích: nếu link trung gian trỏ thư mục thì chính terminal directory-link trong inventory đã đủ K2; nếu hỏng/tới file, phải giữ thất bại phân giải. C04 kiểm hai trường hợp thiếu/file thường | Không khai đã chạy mọi biến thể intermediate-link; resolver mới cần ca riêng |
| Đích tuyệt đối/ngoài gốc | Chỉ phân tích: data-filter cấm link ngoài destination, `_d2b` quy lỗi đo về rc8; hash bắt thay đổi chuỗi. Đích ra khỏi provenance nhưng còn trong bản bung và trỏ ancestor được `root` bao phủ | Không soạn payload vượt biên; không có phép đo native cho toàn miền này |
| Junction | Chỉ phân tích: Git120000/archive không biểu diễn junction như mode riêng và tar không có nhánh tự tạo junction. Nếu môi trường ngoài thay bản bung bằng reparse point, cần phép đo Windows riêng; inventory/hash không phải bằng chứng mọi reparse point đều được chặn | Không tạo junction hay payload; chưa đo |
| Passed/waived và đầu vào sai | Guard mới chỉ trong `passed`; `owner_waived` vẫn dùng `kiem_mien`; sai type/path/OID/mode/module đều nằm17ca+53mutant | Không phát hiện hồi quy D2b khác; không suy full suite pass |

Mẫu `_chup_workspace` ở launcher.py:1049 nhận link trong cả hai danh sách, `lstat` trước đọc nội dung và băm raw target. D2b hiện cũng thấy link trong hai danh sách và băm raw target, nên C03 **không phải bỏ sót inventory**; nó phân loại sai đối tượng K2 ở bước sau. Mẫu không thực hiện chính sách K2 nên không thể sao chép nguyên mọi-link⇒reject. Skill “Ca symlink Windows native” yêu cầu fixture thật, `target_is_directory` và separator Windows; product `git archive`→tar vẫn cần kiểm thứ tự tạo/link text riêng. C03 separator Windows là một khác biệt chưa được bộ ca hiện hành khóa.

Guard đổi ưu tiên báo symlink trước K1 trong nhánh passed; cả hai đều chặn, không phát hiện đây là lỗi độc lập. `doc_danh_gia`/neo run-attempt-head vẫn được gọi. Hai mục nợ ngoài write set và master mới không được tự sửa; không nhận merge gate đã đạt.

**Phép kiểm và bằng chứng.** Chạy từ `repo`; tất cả lệnh thử dùng `-B`, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR tuyệt đối dưới `work/tmp` khi cần. Các script reviewer đặt TMPDIR bên trong.

| Command hoặc wrapper | rc thật | Bằng chứng dương / trạng thái |
|---|---:|---|
| `python3 -B ../work/run_checks.py suite` | 0 | [targeted.json](targeted.json), [targeted.log](targeted.log):17/17 `cong_d2b_*`,0skip |
| `python3 -B ../work/run_checks.py mutants` | 0 | [declared.log](declared.log):53/53 `d2b_*` GIET, `oan=[]`; command con và hash ở checks_receipts.json |
| `python3 -B ../bang_chung/cong_cu/ma_tran_c4.py . d2b_k2_` | 0 | [matrix.log](matrix.log):29variants, original0lệch;4mutant đều chết bởi ChotB4 đúng hướng |
| `python3 -B ../work/legacy.py` | 0 | [legacy.json](legacy.json):14/14 cả base/HEAD (D1–D4/CRLF) |
| `python3 -B ../work/probe_paths.py`, cùng script bằng `/usr/bin/python3 -B` | 0 mỗi lệnh | paths JSON của3.13.18 và3.12.3;96 observations tổng |
| `python3 -B ../work/probe_models.py` | 0 | [models.json](models.json):20observations, chứa gate0 sai và gate12 chặn thừa; rc0 của probe nghĩa đo xong, **không phải oracle pass** |
| `python3 -B ../lich_su/probe_behavior.py` và `python3 -B ../work/prior_directory.py` | 0 mỗi lệnh | [prior_behavior.log](prior_behavior.log), [case_directory.json](case_directory.json):C01/C02 cũ đúng; collision rc8 cả native/model |
| `python3 -m ruff check --no-cache --select F --output-format json .claude/dev/packet_loop.py .claude/dev/packet_loop_test.py` | **1** |16lỗi nền ở HEAD và base; so code/message có chuẩn hóa số dòng: new=[], removed=[]; [audit_final.json](audit_final.json). Ruff lint **failed**, delta passed |
| `loi_ruff_ci()` qua Python | 0 của wrapper |errors=[],count3; Ruff0.15.15. Pin/probe khác bare lint |
| `git diff --numstat f602325 HEAD`; `git diff --check f602325 HEAD` | 0 mỗi lệnh |2tệp,+420/−13; whitespace sạch; [snapshot_after.json](snapshot_after.json) |
| Luật9 `quet_dot_bien.py chay` trên sample12; ledger.py trên bộ229 | 0 mỗi lệnh | [luat9_sample.log](luat9_sample.log), [ledger.log](ledger.log), [ledger.tsv](ledger.tsv) |
| `do_kho_that.py` với previous và HEAD trên local origin/master | 0 mỗi lệnh |71dòng identical:51DAT,10failed,3skipped-job,1non-land,6provenance0; [real_head.tsv](real_head.tsv) |

Để tái lập finding, chạy `python3 -B ../work/probe_models.py` và đọc trường stdout, stderr, observed trong models.json. Script chỉ dùng fixture cục bộ vô hại dưới work, không thay product. Mọi tên đích thử đều nằm trong scratch; không tạo nội dung vượt biên/tấn công. Kết quả rc12 là gate fail theo K2; rc8 là không đo được; không gộp chúng.

Luật9: tái sinh manifest đúng229record, bằng byte/nội dung bộ executor; khối90dòng trích khớp source; ledger tái tạo khớp byte. Audit bộ đầy đủ:226GIET+3SONG được phân loại tương đương. Reviewer chạy **TAP_CON12**, gồm toàn bộ9mutant trong đoạn guard mới và3tương đương cũ:9GIET,3SONG sạch,0lỗi chạy,0lỗi vô can. Không khai chạy lại toàn229. Ba tương đương: suffix `~` không đổi startswith remote; regex SHA neo cả hai đầu làm match/fullmatch như nhau; lớp builtin từ YAML cho `type(ra)==int` và `is int` như nhau. `import posixpath` ngoài khối AST; adapter ghép whole module giữ import và các ca link thực thi nó, nhưng không suy đã mutation-test việc bỏ import. Không tự dựng mutant product ngoài manifest, nên không tạo P3 `ngoai_bang_dong`.

Audit A/B executor bằng ab_so.py ([ab_audit.md](ab_audit.md)):1784→1801ca,38skip mỗi bên;2009→2062mutant,1skip và `r1187_spec_packet_type` đỏ ở cả hai; không mất ca/kill đã có. Đây là **audit log**, không phải reviewer chạy full suite. Kiểm độc lập hồi quy giới hạn14legacy,17D2b,53mutant, corpus71 và probes. Native Windows: chỉ có lời khai điều phối base118/118, HEAD135/135 Python3.12.10 tạo symlink được; không xác minh lại, không tính cho C03/C04 mới.

**Giới hạn và điều kiện đóng.** Full Linux/Windows suites, CI, live remote/master mới, rebase/merge: not_run. Các skip executor vẫn là skipped. `core.abbrev` của checkout chưa pin (config rc1); không sửa repo và không chứng nhận golden/full gate phụ thuộc short hash. Mô hình là bằng chứng logic có điều kiện, không chứng nhận native. Snapshot Git trước/sau không thay byte attestation mọi file ignored; `.codex/` ignored có sẵn. Runtime model/effort chưa có bằng chứng phục vụ. Review `sensitive` này chưa đạt điều kiện approve vì P1/P2 còn mở; không cấp `cross_approved`, `human_audited` hoặc quyền land. Bản vá sau phải neo SHA mới và kiểm lại các oracle đóng lớp, giữ write set/trần hiện hành.

KET_LUAN: changes_requested
