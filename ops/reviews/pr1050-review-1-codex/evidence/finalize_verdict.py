from pathlib import Path
p=Path('VERDICT.md');s=p.read_text()
rows='''| Khóa review và phạm vi | c24875d, base b29da0b; 32 tệp, +11630/−0, ops/reviews + ops/land | `git rev-parse`, `git diff --numstat`; `evidence/final-integrity.log`: đúng OID, tree `9382f751…`, đúng 32/11630/0 | Có |
| Hai commit ghi sổ | e788a5d hiện vật; c24875d biên nhận/land | `git log b29da0b..c24875d`, đúng hai commit; artifact commit là tổ tiên c24875d rc 0 | Có |
| Chưa merge PR ghi sổ | Mỏ neo thấp trên nhánh PR | `git rev-parse origin/master` = b29da0b; `git merge-base --is-ancestor c24875d b29da0b` rc 1, không suy trạng thái PR trực tuyến | Khớp ancestry snapshot; không gọi mạng |
| Nguồn lease | origin/ops/wp1037-r1-g1-lease | Đóng băng thành OID `a34b9a38cda2669f9a90958c69bb6f2faa0f4353`; mọi `git show` nguồn dùng OID này | Có |
| Bản phẳng và VERDICT lượt 1 | Nguyên byte; 14251 byte, e33a3c3e…d2a95b | `python3 evidence/measure_artifacts.py`: flat = directory = source blob; cùng hash | Có |
| Bản phẳng và VERDICT lượt 2 | Nguyên byte; 10679 byte, 2f482565…49feaf | Cùng script: cả ba bản khớp byte/hash | Có |
| PROMPT lượt 1 và 2 | Bản gốc; hash ca20a3a0… / d1d75feb… | Cùng script: 3977 / 3907 byte; source_equal và HEAD_equal True | Có |
| run.json lượt 1 và 2 | Bản gốc | Cùng script: 10930 / 10492 byte, hash 58050918… / 21dfe28a…; source_equal True | Có |
| Manifest các thư mục | SHA256SUMS đầy đủ | Cùng script: 6/6 + 6/6 + 11/11 OK; không thiếu/thừa; `measure_receipts.py` kiểm thêm 6/6 mục manifest nguồn | Có |
| Checkpoint và stdout/stderr | Cùng run đúng hash | `measure_artifacts.py`: cả hai lượt sha256_match=True, bytes_match=True; checkpoint head/prompt/run ID khớp | Có về nội bộ; không có bản handoff riêng cho 3 tệp phụ |
| schema_version, kind, receipt_id | 2 / review_delivery_receipt / hậu tố hash verdict | `python3 evidence/measure_receipts.py`: đúng schema/kind, receipt_id_hash_suffix=True cả hai | Có |
| packet_id, packet_issue, revision, generation, lease_id | #1037; r1/g1; wp1037-r1-g1-claude | Cùng script: từng khóa receipt bằng lease; cả hai = True | Có |
| Review class và vai | reviewer codex; executor claude; sensitive | Lease `risk: sensitive`, code trong ops; receipt hai class sensitive; protocol ops-sensitive | Có |
| verdict và số P0..P3 lượt 1 | changes_requested; 0/0/1/2 theo finding | Script đếm `^- [P*]`: 0/0/1/2; verdict gốc `request_changes` được chuẩn hóa đúng | Có |
| verdict và số P0..P3 lượt 2 | approve; 0/0/0/0 | Script đếm đúng; bảng gốc không finding | Có |
| findings_ids và xử lý lượt trước | Ba slug P2/P3 lượt 1; lượt 2 đã đóng | Slug/hạng khớp các dòng finding gốc; lượt 2 có bảng ĐÃ VÁ THẬT cho cả ba; nội dung là bản gốc byte-identical | Có về ghi sổ; không tái chạy mutant code của packet |
| reviewed_sha / reviewed_tree lượt 1 | 016852ae7acc22a75bae9505febd1697a1ab79ba | Receipt = run = dòng 2 verdict; Git tree `6907a286e95a2c6e86c7c08c0ec700dc2a75ef58` = verdict | Có |
| reviewed_sha / reviewed_tree lượt 2 | 91466322f705658ed51b80c7c152f6b77f4f90c6 | Receipt = run = dòng 2 verdict; Git tree `c20eace3f4aacea3f33afc5861688cb94d64cf3d` = verdict/land | Có |
| base SHA | Base packet 757bde5; base PR ghi sổ b29da0b | Lease base `757bde561d09738858506aecf5de2f050a5f0d5e`; Git diff và PR readback khớp; không nhầm hai loại base | Có |
| Khóa tree/base/mức model | Receipt dùng model_evidence; không có khóa tree/base trực tiếp | Script xác nhận absent_optional_fields; §7 không bắt các khóa tùy chọn này; tree/base được kiểm từ nguồn khác | Không tính vắng khóa là lỗi |
| verdict_path/hash/bytes | Trỏ đúng bản phẳng, đúng hash và byte | `measure_receipts.py`: hash_equal=True, bytes_equal=True cho cả hai; đường dẫn đúng basename chuẩn | Có |
| evidence_url và anchor | Blob ghim e788a5d, cùng nhánh, strength thấp | `git show <OID>:<path>` bằng byte verdict; e788a5d → c24875d rc 0; không khai đã có canonical anchor mạnh | Có |
| reviewed_sha_to_tien và land_merge_commit | Hai reviewed SHA là tổ tiên b29da0b; head cuối là cha 2 | `git merge-base --is-ancestor` cả hai rc 0; `b29da0b^2` = 9146632 | Có |
| Run ID/head/prompt/state/rc/duration | 4d0668e2… / e400a320…; xong; rc 0; 934.249 / 567.318 s | `measure_receipts.py` + `artifacts.log`: đúng từng giá trị, prompt hash khớp; checkpoint cùng run | Có |
| Thời gian chạy thuộc lease | 09:08:51Z và 09:34:41Z trong cửa sổ 08:57Z–17:53Z | Script RUN_START_IN_LEASE=True cả hai | Có |
| model_* reviewer và mức bằng chứng | gpt-6-astra served; do_may; 27 / 19 sự kiện; xhigh | `receipts.log`: model_phuc_vu_trang_thai=DO_DUOC; mọi event cùng model; effort trạng thái DO_DUOC, [xhigh] | Có cho served model/effort |
| model_yeu_cau / CLI flags / version | gpt-6-astra; codex-cli 0.164.0 và command khai trong receipt | run chỉ giữ program/arg count/fingerprint; CLI_VERSION_METADATA_FIELDS=[]; raw stdout/stderr không có version | KHÔNG ĐO ĐƯỢC độc lập cấu hình yêu cầu/phiên bản |
| Provider/surface/transport/run identity | openai_codex/codex_cli/machine và session_run_id | `measure_receipts.py`: cả bốn trường bằng run metadata ở hai lượt | Có theo nguồn được giữ |
| Độc lập và assurance | Lượt 1 cross_reviewed; lượt 2 cross_approved | Hai run ID riêng, prompt riêng; model reviewer khác họ executor trong lease; lượt 1 không approve, lượt 2 approve 0/0/0/0 | Có trong phạm vi evidence; không nâng thành authority merge |
| Executor model / người vận chuyển | Claude theo lease; submitter ducthangho, chưa đăng bản chiếu | Lease khai claude-opus-5-5/claude; `actor_nguon` gắn (b); không có runtime executor hoặc readback push/comment PR #1050 | Lời khai đã tách; không xác nhận độc lập |
| Caveat read-only và scripts | Workspace có write; clean lúc phóng; scripts evidence ngoài repo | Run worktree_sach=True; permission observations có workspace write; các evidence/* không trong gói; run1 sampling KHONG_DO_DUOC, run2 DO_DUOC | Đúng giới hạn caveat; không bảo đảm RO toàn lịch sử |
| README hai hàng mục lục | Đúng file/receipt/verdict/SHA/bytes, không trùng | `evidence/readme.log`: TOC_COUNT=1 mỗi lượt; cả 6 link đích tồn tại; nội dung khớp receipt | Có |
| README bốn hàng caveat | Mỗi caveat của mỗi verdict có hàng riêng | readme.log: COUNT=1 mỗi cặp; t27 baseline 2/2 | Có |
| Land schema/identity/recorded_by | Schema 1, land_operator, cùng phiên executor chỉ ghi sổ; owner merge | Khóa chuẩn §7 có; PR API merged_by=ducthangho. Nhận dạng phiên/operator thực là lời khai; hồ sơ không tự gọi đó là người đã chứng minh | Đúng schema; phần phiên không đo độc lập |
| Authorization | Comment owner nêu điều kiện; không exact SHA | `measure_ci.py`: author OWNER ducthangho, 17:25:09Z, contains_authorized_head=False; PR API xác nhận merge, không thay exact-SHA approval | Có |
| Merged/head/base/parents/tree | Merge b29da0b, head 9146632, parents 8cdb15a + 9146632, tree 24a37be… | `measure_ci.py`: API và Git object khớp từng giá trị; diff hai cặp cùng hash 40b6d80f… và +120/−4 chỉ tệp test | Có |
| Spec và lease provenance | Spec hash 253f12ae…; lease snapshot a34b9a3; write set và hash | `measure_artifacts.py`, `measure_receipts.py`: spec hash đúng, lease byte-identical b1738f6f…, write_set_hash d7872905… đúng | Có |
| Lease đã nhả | `measured … DA NHA`, điều kiện (2) xong | `evidence/lease-timeline.log`: CÒN_HẠN lúc snapshot và commit; còn 718 giây; không bia mộ | **Không — P1 nha-lease-truoc-khi-het-han** |
| PR Ubuntu run | 41033737059, attempt1, pull_request, head9146632, success, 23/23 Ubuntu | `python3 evidence/measure_ci.py`: tổng=độ dài array=23, success=23, đúng head/attempt/labels | Có cho Run và job metadata |
| Windows attempts | 41069257658; attempt1 13success/2failure/1skipped; attempt2 15success/1skipped | ci.log: đúng counts, run failure→success; 14 nhãn Windows + 1 Ubuntu + 1 không runner mỗi array | Có |
| Windows runner và N/N | gate-ops job 124108765783; 95/95,137/137,2/2; lease255/255 | Jobs ghi runner1000026073/windows-latest/success; không có output N/N; hồ sơ nói rõ thuat_lai, log không lưu | Khớp metadata; N/N KHÔNG ĐO ĐƯỢC độc lập |
| Root cause Windows và runner_set input | Câu measured nói thiếu shellcheck, lỗi cai_cong_cu.sh/#1045; tên check windows-only | ci.log chỉ có hai step G5 fail, step cài shellcheck success; không có log chẩn đoán hay input dispatch | **Khai rộng — P2 nguyen-nhan-windows-khai-do-thieu-log** |
| Codex connector | not_measured/thuat_lai, ready17:28:26Z rồi merge17:28:50Z | Không lưu readback comment6529077259; không nhận running hoặc kết luận connector là đo độc lập | Đã hạ nhãn đúng; KHÔNG ĐO ĐƯỢC |
| Gate push master pending | Run41099184556 trên b29da0b pending lúc17:37Z | Snapshot runs: eventpush, attempt1, pending/null, head đúng; lời văn có mốc snapshot | Có ở snapshot; không suy trạng thái về sau |
| Bốn mốc CI §10.2.2 | Run measured; Checkout/definition/output chưa đo | REST files có Run identity; không có checkout log, exact definition blob/hash hoặc command/rc/marker CI; hồ sơ không nhận chúng là ĐẠT | Đúng trạng thái thiếu nguồn; HTTP403 thuật lại |
| assurance_81.thuc_thi | Reviewer lượt2 DAT; model/effort/sandbox đo được | Run2: 19 gpt-6-astra, xhigh, sandbox_trang_thai DO_DUOC và permission observations đúng mô tả; ghi giới hạn lấy mẫu | Có; không thay CI provenance |
| landed:false và việc còn thiếu | Chưa đủ post-merge evidence và approval exact SHA | Nguồn thiếu các mốc CI, owner comment không SHA; source code đã vào master qua diff giống byte | Đúng; điều kiện nhả lease phải sửa theo P1 |
| Sáu cổng | Yêu cầu rc0, marker dương/N=N | `evidence/baseline-*.log/.rc`: cả sáu rc0, TỔNG ĐẠT hoặc sạch; t26 1/1, t27 2/2, t138 1/1 | Có |
| Răng cổng trên dữ liệu | Byte verdict / hàng README / số P1 | `python3 evidence/measure_mutations.py`: byte→t26 đỏ; xóa mục lục/caveat→t27 đỏ; so_p1 đổi→sáu cổng vẫn xanh | Có răng hash/mục lục; **không có răng số đếm** |
| Gợi ý và nguyên trạng cây | HINT chỉ sửa dữ liệu, reviewer không sửa checkout gốc | `patch --dry-run --fuzz=0 -p0` rc0; thử áp/gate trên clone rồi phục hồi; final-integrity: cả hai cây sạch, 32/32 tệp gốc khớp HEAD | Có |'''
old='| Phạm vi | PR #1050, HEAD c24875d, base b29da0b | Đang xác minh checkout, diff và nguồn tại SHA cố định | Chưa chốt |'
assert s.count(old)==1;s=s.replace(old,rows)
s=s.replace('TỆP/DÒNG: `ops/land/pr1041-wp1037-land-evidence.yaml:70` (đoạn 69–72), `:83` (điều kiện 2); nguồn `ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt:82`, `:115`.','TỆP/DÒNG: `ops/land/pr1041-wp1037-land-evidence.yaml:70` (đoạn 69–72), `:83` (điều kiện 2); nguồn `ops/land/pr1041-wp1037-provenance/lease-wp1037-r1-g1.yaml.txt:80`, `:117`.')
# Đặt toàn bộ nhật ký thử trước findings, giữ nguyên nội dung đã ghi.
marker='\n## FINDINGS\n';a,b=s.split(marker,1);findings,later=b.split('\n### Hướng 13',1);s=a+'\n### Hướng 13'+later+marker+findings
p.write_text(s)
