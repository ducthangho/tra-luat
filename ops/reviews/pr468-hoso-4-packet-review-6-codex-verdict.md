# VERDICT — cross-review PR #468, lượt 6

verdict: changes_requested
reviewed_sha: 2adb6819caee0225d7b7e4f0c4e8c16f2faa7e73

Kết luận: **changes_requested**. 7 finding P1 và 4 P2; P3 cũ đã đóng. P1 cũ chưa đủ bằng chứng để đóng, nhưng không tìm được phản chứng H mới ngoài ranh giới công khai.

Reviewer: Codex / OpenAI, phiên độc lập qua API, shell cục bộ. Transport: tệp trong sandbox. Không dùng mạng để xác minh GitHub, không commit/push vào ref được giao. Test có kho git giả lập nằm trong do-review/tmp. Đã đọc protocol §8/12/13 trước, áp khung tai-lieu/cross-review-SKILL.md; chỉ thị PROMPT cấm mạng ưu tiên hơn bước đăng verdict lên PR của skill. **Chưa đăng GitHub hoặc lập receipt/merge authorization.**

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `span-rong-nuot-ti-le-vo-can`: **VÁ HỜ về nghĩa vụ xác nhận**. Hai cơ chế cũ bị chặn trong bộ mới: **1213 ca / 0 đỏ giả / 0 bỏ sót**; Đ1=0 trên bộ đã đo. Đ2: **6/8 formatter có stdout xanh thật, H bác 0/6**, 2 formatter chưa đo được bản in xanh. Không gán hai suite lỗi nền thành lỗi H, không suy 0/8. Thiếu bộ ca lịch sử nên giữ P1 ở mức bằng chứng; chi tiết finding bên dưới.
- `uoc-kich-thuoc-lo-con-tinh-nhan-ac`: **ĐÃ VÁ THẬT**. Trích blob e5ab4b7 và HEAD, đo bằng git diff --no-index --numstat từ tệp rỗng: T' **21+26**, H **21+29** additions. Không còn tính NHAN của A-c vào ước mới; vẫn phân biệt số dòng mẫu và additions triển khai.
- Lượt 5 không có verdict hoàn tất; không coi các bản dở là approval. Finding bia mộ cùng slug từ lịch sử được giữ nguyên khi tái xuất hiện trong snapshot.

## BẢNG ĐO

Đo trong lượt 6 ngày **07-09-2026 UTC**, từ 06:14Z; UTC/giây/băm chi tiết nằm trong JSON/log đi kèm. “Số học khớp” chỉ xác nhận phép tính trên các ô đã in, không xác nhận nguồn CI lịch sử. Mọi số mới dùng mẫu số của bộ reviewer; không chép sang mẫu số 311.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Exact HEAD / tree | 2adb6819caee0225d7b7e4f0c4e8c16f2faa7e73 | HEAD đúng; tree c3c7bdaba867463ca33123025d7ac999b58fb6a3 | có |
| Môi trường git | core.abbrev=7; không shallow; cây sạch | 7; false; status --porcelain rỗng trước/sau | có |
| Phạm vi diff d28c4b1→reviewed SHA | numstat.txt và diff.patch; thuần ops/ | 14 tệp; +3388/−0; cả 2 hiện vật khớp git diff từng byte; không có runtime diff | có |
| doctrine-scan | rc=0, 7 tệp, 0 chỗ chép | rc=0, 7/0; 06:17:56Z | có |
| adr-song | rc=0, 46/46 | rc=0, 46/46; có ngoại lệ ADR0016 thiếu trạng thái | có |
| doc-claims-check --strict --json | rc=0, ok=true, advisory=367 | rc=0, ok=true, 106 tệp, claims_flagged=advisory_count=367 | có |
| ci_dang_ky_test.py không --chay | rc=0, 51/51 | rc=0, PHẢN CHỨNG 51/51, TỔNG ĐẠT | có |
| packet_loop_test / lease_publish_test trên exact HEAD | EVIDENCE chưa chạy lại; biên bản khai delta0 trên 7eb1145 | KHÔNG ĐO ĐƯỢC delta lịch sử; không chạy lại hai suite trong lượt này | chưa xác minh |
| SHA-256 đặc tả GATE | 8cca700cba9c2312d05bf64eee3d4a5bda5317cb45e244ed22161b4ddcc83c62 | 8cca700cba9c2312d05bf64eee3d4a5bda5317cb45e244ed22161b4ddcc83c62 | có |
| Bản sao spec GATE / write set / dependency | khớp spec–lease | bản sao bằng byte; 2 tệp; depends_on=[] | có |
| SHA-256 đặc tả LO | 3aafd766abd1fdcfa55a23e2f2716efbcbd8dc2505ddf9fe6dc878074a675067 | 3aafd766abd1fdcfa55a23e2f2716efbcbd8dc2505ddf9fe6dc878074a675067 | có |
| Bản sao spec LO / write set / dependency | khớp spec–lease | bản sao bằng byte; 1 tệp; depends_on=['GATE-TACH-JOB-CAT-CHI-PHI'] | có |
| SHA-256 đặc tả 2A | 2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759 | 2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759 | có |
| Bản sao spec 2A / write set / dependency | khớp spec–lease | bản sao bằng byte; 2 tệp; depends_on=['GATE-TACH-JOB-CAT-CHI-PHI', 'LO-319-LINUX-BANG-CHUNG-XANH'] | có |
| SHA-256 đặc tả 2B | 417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521 | 417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521 | có |
| Bản sao spec 2B / write set / dependency | khớp spec–lease | bản sao bằng byte; 2 tệp; depends_on=['GATE-TACH-JOB-CAT-CHI-PHI', 'LO-319-LINUX-BANG-CHUNG-XANH', 'MUTANT-WINDOWS-SUBAGENT-GHI-DETECT'] | có |
| Chuỗi chung | GATE→LO→2A→2B | dependency 0/1/2/3; cùng giao .claude/dev/ci_dang_ky_test.py; không có chu trình | có |
| Số ô null lease | 6 ô mỗi nháp; GATE Issue vẫn nói .yaml.nhap | GATE .yaml=0; LO/2A/2B .yaml.nhap=5 mỗi tệp | không |
| Trường lease §4 | đủ trường hợp đồng | GATE thiếu literal write_set_hash, heartbeat_at, lease_until (3); chỉ hạn có bí danh lease_expires_at_utc | không đủ |
| Schema §3.2 trong lease | spec dẫn protocol | objective/acceptance_criteria không là key (2), có mục tiêu/nghiệm thu dạng văn xuôi trong spec; chưa có projection được giao | chưa chứng minh ánh xạ |
| Ba mỏ neo GATE lúc cấp | đo lại lúc 03:37:33Z 07-09 | 3/3 vẫn 1b3caa1 giữ chỗ; d28c4b1 có timestamp 01:50:09Z trước lúc cấp; drift +8 dòng ci.yml/+1 consumer | thiếu readback |
| Thời hạn GATE | 1440 phút; không phải trần run90 | 03:37:33Z 07-09→03:37:33Z 08-09 = 1440 phút | có |
| Bia mộ ở HEAD | GATE thay #456; #456 trỏ ngược | hai chiều khớp, lease check rc=0 | có |
| A9 mọi bản #456 đã hết giữ | 0 bản cũ còn hiệu lực khi bắt tay | snapshot 2 blob #456: 1 có bia mộ, 1 chưa có; ci.yml 1 người giữ, registry 2 | chưa đạt trong snapshot |
| ai-dang-giu thật | đối chiếu cả ref máy chủ | 2 lệnh rc=12; git HTTPS bị chặn với GIT_ALLOW_PROTOCOL=file; KHÔNG ĐO ĐƯỢC máy chủ | chưa xác minh |
| Ref/lease trong snapshot | historical 295/298/299 và 9/10 ref có mốc cũ | hiện 1 local head, 2 origin refs không HEAD; bare mirror 2 heads; 85 cặp blob/path lease; không có master ref | khác snapshot; không bác số cũ |
| Trôi 1b3caa1→28cb898 | 46 commit | 46 commit | có |
| Cây 426bfc0 và merge1b3caa1 | diff rỗng | 0 tệp khác | có |
| Additions #456 ở 0c5e889 | consumer+76/−5; pretooluse+68/−0; tổng+144/−5 | 76/5; 68/0; 144/5 | có |
| ci.yml tại 1b3caa1 | 39 bước/10 if/588 dòng/0 run trùng/trần60 | 39 bước/10 if/588 dòng/0 thân run trùng/trần60 | có |
| ci.yml tại 28cb898 | 40 bước/10 if/596 dòng/trần60 | 40 bước/10 if/596 dòng/0 thân run trùng/trần60 | có |
| ci.yml tại HEAD | đã merge master, giữ runtime | 40 bước/10 if/596 dòng/0 thân run trùng/trần60 | có |
| Consumer Ruff khi tách | ([],3)→([1 lỗi],3) | ([],3)→([CI không provision Ruff trước test registry],3); 3 job, mỗi job mới 9 bước đầu | có |
| Số dòng khối T' / H | T'=21+26; H=21+29 | git diff --no-index: 21+26 và 21+29 additions, rc=1 vì có diff | có |
| Diff runtime 1b3caa1→e5ab4b7 | rỗng | 0 dòng | có |
| Hai băm khối H | c23bcd01… / bde441a0… | c23bcd019182023496cb3d9817c6553a0074c77bca26c0a0d1f71a4f5104e45c / bde441a08d129a962d862fe237003997610238edc8e87b7948d35de875e5f165 (gồm newline cuối) | có |
| Consumer tham chiếu / số dạng | 8 MOI, 1 mục Windows/2 dạng; SPAN giữ nguyên | tệp consumer bằng byte với cây; 8 MOI; 1/2 Windows; 8/8 SPAN giữ nguyên, 8/8 MOI đổi kiểu | có |
| Số cặp H trong grammar Linux | 13/13 | 13 cặp nhóm bắt trên 11 bản ghi của 8 mục (kiểm nguồn); khác phép đo stdout đủ8 | có |
| Bộ tấn công độc lập | ngoài danh sách ranh giới phải kiểm cả hai chiều | 1213 hàng / 0 đỏ giả / 0 bỏ sót / 0 ngoại lệ; gồm 625 tổ hợp số | Đ1=0 trong bộ này |
| Phân rã 1213 hàng | bộ reviewer mới | bare-span=10, canonical=8, duplicate=100, exhaustive=625, grammar-equivalent=40, grammar-hole=33, old-law7=8, pair=91, prose=288, windows=10 | số mới |
| Đ2 | 8 formatter thật rc=0 | đã chạy cả8; sau sửa rig nhanh có6 bản xanh, H bác0/6; 2 chưa có bản xanh | KHÔNG ĐO ĐƯỢC đủ8 |
| Chạy thật chon_reviewer_test.py | bản in thật rc0, mốc06-09 | 2026-09-07T06:15:49.921057+00:00; 0.69s; rc=0; BASE/H đếm đỏ=0/0; stdout 2746 ký tự/2765 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout chon_reviewer_test.py | a5807082… | a58070829bf0732f81f9e4fa601196637467cea0528ed7e362ed8da48a82ede7 | có |
| SPAN chon_reviewer_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=2745 ký tự/2764 byte; cặp trong span=1; cặp nhóm H=1 | thiếu match nếu rc1 |
| Chạy thật gh_readback_test.py | bản in thật rc0, mốc06-09 | 2026-09-07T06:15:50.611850+00:00; 0.13s; rc=0; BASE/H đếm đỏ=0/0; stdout 40 ký tự/40 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout gh_readback_test.py | 0a476a97… | 0a476a97ea3c334220ff9bee8485d720a8ab62acc17eb1e4a59e3d33c67f2cc2 | có |
| SPAN gh_readback_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=38 ký tự/38 byte; cặp trong span=1; cặp nhóm H=1 | thiếu match nếu rc1 |
| Chạy thật mcp_gh_test.py | bản in thật rc0, mốc06-09 | 2026-09-07T06:15:50.740712+00:00; 0.18s; rc=1; BASE/H đếm đỏ=1/1; stdout 589 ký tự/718 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout mcp_gh_test.py | b3034838… | ab5eefde5db37e2f429a1dc418cf30893763ade21fc1dce9af5f7a77a649ec7e | không thay được stdout lịch sử |
| SPAN mcp_gh_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=None ký tự/None byte; cặp trong span=None; cặp nhóm H=2 | thiếu match nếu rc1 |
| Chạy thật mcp_github_doc_test.py | bản in thật rc0, mốc06-09 | 2026-09-07T06:15:50.925121+00:00; 0.45s; rc=0; BASE/H đếm đỏ=0/0; stdout 55 ký tự/55 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout mcp_github_doc_test.py | 82f89e9d… | 82f89e9d5170cc190c941b9b5e247c69623d98f135217d8c8495c806074f033b | có |
| SPAN mcp_github_doc_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=53 ký tự/53 byte; cặp trong span=1; cặp nhóm H=1 | thiếu match nếu rc1 |
| Chạy thật probe_mang_test.py | bản in thật rc0, mốc06-09 | 2026-09-07T06:15:51.373382+00:00; 1.69s; rc=0; BASE/H đếm đỏ=0/0; stdout 457 ký tự/497 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout probe_mang_test.py | c9997dac… | c9997dac6d36e60d76b48d5b71e1b87fd60f0c387682061d09382d0585fd54a1 | có |
| SPAN probe_mang_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=0; span=456 ký tự/496 byte; cặp trong span=3; cặp nhóm H=3 | thiếu match nếu rc1 |
| Chạy thật pretooluse_guard_test.py | 270s/rc1/3 ca đỏ (06-09) | 2026-09-07T06:15:53.065047+00:00; 432.99s; rc=1; BASE/H đếm đỏ=1/1; stdout 9475 ký tự/9490 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout pretooluse_guard_test.py | pretooluse canonical chưa có stdout xanh | 00bb4b944b12cca20b33fd8ce77ba8280e1becd4249e41aced15803ecab44004 | không thay được stdout lịch sử |
| SPAN pretooluse_guard_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=None ký tự/None byte; cặp trong span=None; cặp nhóm H=2 | thiếu match nếu rc1 |
| Chạy thật subagent_ghi_detect_test.py | 88s rồi75s/rc0 (06-09) | 2026-09-07T06:23:06.054973+00:00; 124.95s; rc=0; BASE/H đếm đỏ=0/0; stdout 8325 ký tự/8340 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout subagent_ghi_detect_test.py | 449578d8… | 56f4f998bed4b71e294e8d159fc624e6313d5102778838778d097a6d45026573 | không thay được stdout lịch sử |
| SPAN subagent_ghi_detect_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=53 ký tự/54 byte; cặp trong span=2; cặp nhóm H=2 | thiếu match nếu rc1 |
| Chạy thật nhanh_don_duoc_test.py | 33s rồi34s/rc0 (06-09) | 2026-09-07T06:29:05.920108+00:00; 18.50s; rc=0; BASE/H đếm đỏ=0/0; stdout 491 ký tự/491 byte | mốc mới; 0/6 đỏ giả H |
| Băm stdout nhanh_don_duoc_test.py | 366795e4… | 366795e45727a70aa7e6ed4ee64c6a1f0bd952dc1191b901c5d40479c722ad96 | có |
| SPAN nhanh_don_duoc_test.py | số nhóm/cặp trong spec; chiều dài theo đúng bản in | groups=2; span=3 ký tự/3 byte; cặp trong span=1; cặp nhóm H=1 | thiếu match nếu rc1 |
| nhanh trước sửa rig | không có lời khai cùng môi trường | rc1, 0/8; 3,33s; 8515 ký tự/8531 byte; bị dịch vụ ký commit fixture chặn | lỗi rig; giữ log riêng |
| nhanh stdout chi tiết | 10 MUTANT: 8×1/1 + 2×3/3; tổng8/8 | đúng 10 dòng, 8×1/1, 2×3/3, tổng8/8 | có |
| Ca nền/bảng mutant | pre39/34; sub33/22/6/1; nhanh8/10 | AST/module: 39/34; 33/22/6/1; 8/10 | có |
| Spawn subagent-base | 438 | 438 Popen; 5.88s; kết quả 33/33 True | có |
| Spawn subagent-empty | 438 | 438 Popen; 5.72s; kết quả 1 | có |
| Spawn nhanh-base | 136 | 136 Popen; 1.76s; kết quả [] | có |
| Spawn nhanh-mutants | 35 | 35 Popen; 18.62s; kết quả 10 | có |
| Nhánh mutant nhanh | 5+3×N với N10; đầy đủ136+35 | 5+3×10=35; 136+35=171 | có |
| Subagent đầy đủ/kênh2/kênh3 (lịch sử) | 10045 spawn, chênh9607; kênh2 10 spawn/6exec; kênh3 6spawn | KHÔNG ĐO ĐƯỢC lại riêng các đại lượng này; không suy từ thời gian toàn suite | chưa xác minh |
| Mutant H no_positions | bảng PR trên311 có mẫu số khác | trên1213: 5 đổi màu, 11 ngoại lệ (không tính ngoại lệ là răng) | bộ mới; dead-bool0 khớp |
| Mutant H no_unique | bảng PR trên311 có mẫu số khác | trên1213: 51 đổi màu, 0 ngoại lệ (không tính ngoại lệ là răng) | bộ mới; dead-bool0 khớp |
| Mutant H no_positive | bảng PR trên311 có mẫu số khác | trên1213: 42 đổi màu, 0 ngoại lệ (không tính ngoại lệ là răng) | bộ mới; dead-bool0 khớp |
| Mutant H remove_dead_bool | bảng PR trên311 có mẫu số khác | trên1213: 0 đổi màu, 0 ngoại lệ (không tính ngoại lệ là răng) | bộ mới; dead-bool0 khớp |
| D9 đầu cặp 5000 chữ số | A9: BASE1 không ngoại lệ; bảng D9: BASE EXC | 2 fixture pretooluse/nhanh: BASE=H=ValueError; vị trí mutant mcp: BASE0/H ValueError | A9 tự mâu thuẫn; không tính Đ1 |
| Bảng Issue464 nguyên chuỗi | True/True/False | False/False/False: lệch2/3; thêm TONG:DAT đúng khoảng trắng thành True/True/False | không |
| Đường Issue465 | .claude/dev/subagent_ghi_detect_test.py | không tồn tại; .claude/hooks/subagent_ghi_detect_test.py tồn tại | không |
| Số học từ bảng job 9 | n9,min40.20,max49.62,range9.42,median45.58,mean45.08 | n=9, min=40.20, max=49.62, range=9.42, median=45.58, mean=45.08, margin60=10.38 | khớp số học; nguồn KHÔNG ĐO ĐƯỢC |
| Số học từ bảng job 11 | n11,min40.20,max50.48,range10.28,median46.02,mean45.84 | n=11, min=40.20, max=50.48, range=10.28, median=46.02, mean=45.84, margin60=9.52 | khớp số học; nguồn KHÔNG ĐO ĐƯỢC |
| Ước tách Windows | 15.77/21.03/13.03; tổng49.83 phút | 15.77/21.03/13.03; tổng49.83 phút | số học khớp; chưa đo sau tách |
| Ước tách Ubuntu | 7.42/14.31/4.83; tổng26.56 phút | 7.42/14.31/4.83; tổng26.56 phút | số học khớp; chưa đo sau tách |
| Ước billing/giảm max job | 110.65→126.22;+15.57/+14.1%; max−51.3% | 110.65→126.22;+15.57/+14.07%; max−51.3194%; giảm22.17 phút, biên A1=3.97 | số học khớp; hệ số×2 chưa kiểm hóa đơn |
| 11 head cùng tải? | coi biên độ là nhiễu runner | 1 head39 bước không receipt-v2;10 head40 bước có receipt-v2 | không cùng tải |
| Biên mới có thể dùng làm ngưỡng? | A1≤25; mục nợ yêu cầu nới theo phương sai | phản mô hình28 phút: A1 đỏ; ngưỡng minh hoạ21.03+10.28=31.31 thì xanh | mâu thuẫn; chưa chọn ngưỡng mới |
| Hiện vật lịch sử | do_h/law7/prior131/do_t2 + các gói, TSV, manifest | 12 tên artifact inventory đều0; 6 tên file git-log kiểm đều0 dòng | KHÔNG ĐO ĐƯỢC |
| Bảng H/mutant cũ | 311 có kỳ vọng +54 ranh giới;14 mutants; 419 ca lượt5 | KHÔNG ĐO ĐƯỢC lại nguyên bộ; có bộ mới1213 nhưng không thay dữ liệu lịch sử | chưa xác minh |
| Bảng bước và tỷ lệ | buoc_master.tsv2062 hàng/12 cột; tỷ lệ1.07–9.74, median từng bước | KHÔNG ĐO ĐƯỢC; không có TSV/log nguồn hoặc mã trích | chưa xác minh |
| hint_provenance | 40 hunk, 4 bị bác | 0 hiện vật; KHÔNG ĐO ĐƯỢC4/4 lý do bác | chưa xác minh |
| Tình trạng Issue/lease nháp | 6 null, chưa có Issue/Mission | 4 Issue thân463–466 có băm; GATE có Mission467; nháp còn5 null; GATE0 | lời mô tả đã cũ |
| Chẩn đoán mạng trong Issue | 4 Issue vẫn nói proxy cấm WebSocket | 4 bản chiếu trái đính chính03:55Z; nguyên nhân thật KHÔNG ĐO ĐƯỢC trong review này | không nhất quán |
| Guard --kiem-bang đối chứng cwd | các ca pretooluse lỗi môi trường | gọi nhầm từ root sandbox rc4; gọi đúng cay-kho rc0, runtime97+7=104, 8 lệnh write-scope, 26/26 help; flags425 xác nhận/35 chưa đo; Ruff0.15.8 | chỉ chẩn đoán rig; không thay suite xanh |

Các phép đo chính: `python do-review/harness.py`; `python do-review/attack_h.py`; `python do-review/run_real.py`; `python do-review/rerun_nhanh.py`; `python do-review/run_gates.py`; `python do-review/audit_static.py`; `python do-review/recheck_contracts.py`; `python do-review/extra_checks.py`; `python do-review/count_spawn.py`; `sha256sum` bốn spec (lưu do-review/sha256sum.log).

Mã H trích nguyên văn nằm tại `do-review/h_tong.py` và `do-review/h_predicate.py`, ghép với consumer thật bằng `harness.py`. `chay_moi`, `mau_theo_nen` và chuỗi SPAN giữ nguyên. Bộ mới chứa oracle hai chiều, bảng trường hợp và các đầu vào nguyên chuỗi; `attack-h-cases.json` là dữ liệu tái lập. Đ2 chỉ nhận đầu ra từ `_chay_that` có rc=0; bản nhanh chạy lại chỉ tắt ký commit trong tiến trình tạo fixture, không sửa test/formatter.

### span-rong-nuot-ti-le-vo-can  [P1]  Hai cơ chế cũ đã bị chặn trong bộ mới, nhưng chưa đủ bằng chứng đóng P1

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:221`, `:273`, `:354`, `:715`, `:794`.

VẤN ĐỀ: phân loại **VÁ HỜ về nghĩa vụ xác nhận toàn thiết kế**, không khẳng định đã tìm được một lỗ H mới. H khắc phục được selector đòi payload và kiểm luật 7 bằng vị trí trong các ca tôi tự dựng; bộ mới 1213/0/0 và các mutant xác nhận chốt thật có tác dụng. Tuy nhiên không replay được bộ cũ vì thiếu hiện vật, và Đ2 chỉ có 6/8 bản in xanh thật. Không thể biến 0/6 thành 0/8 hoặc tự cho các formatter lỗi nền là pass. P1 chưa đủ điều kiện đóng trên hồ sơ giao ở SHA này.

ĐÃ THỬ VÁ: trích nguyên văn hai khối H thành tệp chạy được, ghép vào consumer thật và thử trên bộ mới; không sửa branch. Không đề xuất vá regex tiếp khi chưa biết H hỏng chỗ nào. Phần cần bổ sung là fixture/bản in có băm và phép đo Đ2 trên môi trường đúng. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/attack_h.py` → **1213 ca/0 đỏ giả/0 bỏ sót**, `python do-review/extra_checks.py` kiểm độc lập 4 mutant; `python do-review/run_real.py` + `python do-review/rerun_nhanh.py` → **6/8 formatter rc=0, H bác 0/6**. **Đ1=0 trong bộ đã đo; Đ2=0/6, còn 2 KHÔNG ĐO ĐƯỢC**. D9 là ranh giới công khai, không tính là Đ1. Không có phép đo nào ở đây cho phép nói Đ1/Đ2 đã chạm ngưỡng ≥1; giữ P1 vì nghĩa vụ bằng chứng chưa hoàn tất, không vì bịa một phản chứng mới.

ĐỘ TIN: cao với kết quả cục bộ; chưa đủ với hợp đồng tất cả formatter.

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Lease GATE đã cấp nhưng snapshot còn bản #456 chưa thu hồi

TỆP/DÒNG: `ops/leases/gate-tach-job-cat-chi-phi-exec-1-claude-20260906.yaml:112`; `ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml:101`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:549`.

VẤN ĐỀ: hai chiều GATE↔#456 đúng trên HEAD, nhưng ref `refs/remotes/origin/claude/gate-tach-job-cat-chi-phi` vẫn chứa blob #456 `8b2103c06687546379a17f6deafc97f1fe0173fd` không có `da_bi_thay_the`, còn hạn tới 14:30:07Z 07-09. Snapshot lúc 06:22Z: `.claude/dev/ci_dang_ky_test.py` có **2 người giữ** (GATE và #456); `ci.yml` có **1**. Đây là chính lớp lỗi cũ đã được đặc tả nhận diện; việc thêm bia mộ ở một ref chưa đạt A9. Không khẳng định đã có hai executor cùng sửa, nhưng điều kiện bắt tay chưa đạt.

ĐÃ THỬ VÁ: không sửa ref/lease; hướng xử lý là thu hồi mọi bản còn giữ hoặc đợi hết hạn rồi cấp lại phù hợp. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/audit_static.py`, gọi hàm đọc snapshot `_quet_lease_toan_kho(..., doi_chieu_ref=False)` rồi chính `_phan_loai_lease`/`_bia_mo_doi_xung`: 2 blob #456, một bia mộ đối xứng, một chưa thu hồi. `lease_publish.py check <lease GATE>` rc=0; lệnh `ai-dang-giu` chính thức rc=12 do bước đối chiếu HTTPS bị chặn bằng GIT_ALLOW_PROTOCOL=file. Số 2 là số **snapshot cục bộ**, GitHub trực tiếp **KHÔNG ĐO ĐƯỢC**; không bỏ chốt mạng để khai gate xanh.

ĐỘ TIN: cao về snapshot/thiếu readback; không suy trạng thái GitHub hiện tại.

### issue-lo-giu-rang-buoc-cu  [P1]  Issue LO cấm chính thay đổi kiểu MOI mà H bắt buộc

TỆP/DÒNG: `ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md:77`; đối chiếu `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:335`, `:584`, `:700`.

VẤN ĐỀ: Issue nói “Không sửa một ký tự nào trong MOI/MOI_WINDOWS” và giữ hai neo cũ, trong khi đặc tả H bắt buộc đổi MOI thành (SPAN,TONG), sửa MOI_WINDOWS tương ứng và cập nhật các neo A5. Hai nguồn của cùng packet đòi hai kết quả loại trừ nhau; giữ nguyên theo Issue sẽ không ghép được H như đã đo.

ĐÃ THỬ VÁ: dùng cách ghép đúng 7 luật trong harness; đề nghị chiếu lại đoạn phạm vi Issue từ đặc tả H. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/recheck_contracts.py` → rc=0: 8/8 chuỗi SPAN giữ nguyên nhưng 8/8 giá trị MOI đổi kiểu/khác giá trị cũ. `do-review/contracts.json` lưu kết quả.

ĐỘ TIN: cao.

### issue-kiem-lease-sai-write-set  [P1]  Các Issue dùng phép đo thiếu hoặc sai đường dẫn để nói write set rảnh

TỆP/DÒNG: `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:84`; `ops/issues/465-MUTANT-WINDOWS-SUBAGENT-GHI-DETECT.md:8`, `:51`; `ops/issues/466-MUTANT-WINDOWS-NHANH-DON-DUOC.md:53`.

VẤN ĐỀ: #463 chỉ đo ci.yml rồi kết luận packet duy nhất “không bị chặn”, bỏ tệp `.claude/dev/ci_dang_ky_test.py` trong write set mà #464 cùng mốc lại xác nhận #456 đang giữ. #465 đo `.claude/dev/subagent_ghi_detect_test.py` không tồn tại (đúng là `.claude/hooks/...`), đồng thời bỏ đường sổ đăng ký chung. #466 cũng chỉ trình một nửa write set. Một phép đo trả 0 trên đường không tồn tại/không giao không chứng minh đủ điều kiện bắt tay.

ĐÃ THỬ VÁ: không sửa hồ sơ; đề nghị đo mọi đường exact từ lease rồi công bố đủ bảng, giữ chặn nếu còn người giữ khác. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/recheck_contracts.py`: đường #465 khai exists=False, đường hooks exists=True. `python do-review/audit_static.py`: 2/1/2/2 đường trong các lease; snapshot hiện tại GATE: ci.yml 1 người giữ nhưng sổ đăng ký 2 người giữ. Số máy chủ lúc 03:15Z **KHÔNG ĐO ĐƯỢC**, không dùng nó làm kết quả đã tái kiểm.

ĐỘ TIN: cao về lỗi đường và thiếu phạm vi; không suy lịch sử GitHub.

### lease-gate-cap-that-con-ho-so-nhap  [P1]  Lease đã cấp vẫn dùng mỏ neo giữ chỗ và thiếu trường hợp đồng

TỆP/DÒNG: `ops/leases/gate-tach-job-cat-chi-phi-exec-1-claude-20260906.yaml:27`, `:72`, `:75`, `:85`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:6`, `:17`.

VẤN ĐỀ: lease mang event cấp thật, Issue #463/Mission #467 và giờ cấp 03:37:33Z 07-09, nhưng cả ba SHA vẫn là 1b3caa1 được chú thích chính trong lease là “chỗ giữ, KHÔNG phải giá trị cấp”. Spec đòi đo lại lúc cấp và đã ghi master trôi 46 commit từ tối trước; d28c4b1 trong bundle có thời gian commit 01:50:09Z, trước giờ cấp, và khác cả hai tệp write set (+8/+1 dòng). Không có readback gắn ba neo cũ với lúc cấp. Theo §4 còn thiếu `write_set_hash`, `heartbeat_at`, `lease_until`; `lease_expires_at_utc` có thể là bí danh của hạn nhưng không thay hash hoặc thời điểm heartbeat. §3.2: mục tiêu/acceptance có văn xuôi ở spec, song spec vẫn nói chưa có Issue/Mission/chưa đóng băng; chưa có projection/ánh xạ schema được giao để chứng minh hồ sơ đã vào ready đầy đủ. `check rc=0` không kiểm đủ hợp đồng này.

ĐÃ THỬ VÁ: không tự điền SHA/giờ/authority thay chủ kho; đề nghị cấp/chiếu lại hồ sơ từ readback exact base, bổ sung schema hoặc chỉ rõ projection có băm chứa các trường đó, đồng bộ trạng thái nháp/cấp thật. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/audit_static.py` và `lease_publish.py check <GATE>`: băm spec khớp, publisher rc=0, GATE **0** trường null, ba nháp sau **5** null mỗi tệp (không phải 6 như chú thích), thiếu ba tên trường §4 nói trên. `git diff --numstat 1b3caa1 d28c4b1 -- <hai đường>` → +1/+8; timestamp d28c4b1 = 2026-09-07T08:50:09+07:00. Master **trực tiếp tại giờ cấp KHÔNG ĐO ĐƯỢC**; kết luận chắc chắn là hồ sơ không cung cấp phép đo bắt buộc, không đoán SHA thực tế khi cấp.

ĐỘ TIN: cao về trường/neo/khai báo; vừa về lịch sử cấp thực tế do thiếu readback.

### thieu-hien-vat-quyet-dinh-h-va-chi-phi  [P1]  Các bảng quyết định thiết kế không có dữ liệu để tái tính

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:236`, `:354`, `:401`, `:722`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:184`; `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md:124`; `EVIDENCE.md:9`.

VẤN ĐỀ: `do_h.py`, `do_h.json`, `law7.json`, `prior131.json`, `do_t2.json`, `executor-luot4-va/`, `executor-luot3-va/`, `MANIFEST.sha256`, `mruns_all.tsv`, `buoc_master.tsv` không có trong cây/bundle tài liệu; lịch sử refs được giao cũng không có các tệp đo chính. Vì thế **KHÔNG ĐO ĐƯỢC** lời khai 311 hàng, 49+5 ranh giới nguyên bản, 14 mutant/kill-list và 419 ca lượt 5; **KHÔNG ĐO ĐƯỢC** 2062 hàng/12 cột cùng các tỷ lệ bước Windows/Ubuntu làm cơ sở chọn hướng và ngưỡng. Tính lại số học từ các ô đã in không xác minh dữ liệu đầu vào. EVIDENCE đã tự khai thiếu; lời tự khai đó không thay phép đo ở chỗ quyết định theo PROMPT/§8.

ĐÃ THỬ VÁ: đã dựng bộ độc lập 1213 hàng và chạy 8 test, nhưng không gán số mới cho các hiện vật lịch sử vắng mặt; đề nghị giao script, fixture nguyên byte, kỳ vọng, JSON/TSV và manifest có băm ở trong bundle. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/audit_static.py` → danh sách `artifact_paths` rỗng cho 12 tên được kiểm; `git log --all --format= --name-only -- '**/do_h.py' '**/law7.json' '**/prior131.json' '**/hint_provenance.json' '**/buoc_master.tsv' '**/mruns_all.tsv'` → 0 dòng. Số học 11 job/9 job và ước tách khớp các ô in (`contracts.json`), nhưng nguồn log/giây và thuộc tính success/head chưa tái kiểm được. Bản in lịch sử mcp b3034838…/2171 ký tự/2251 byte cũng **KHÔNG ĐO ĐƯỢC**; bản in mới rc=1 không thay bản cũ.

ĐỘ TIN: cao.

### hint-provenance-bon-hunk-khong-co-de-kiem  [P1]  Không có bốn hunk bị bác hoặc lý do để kiểm provenance

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:234`; `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md:108`.

VẤN ĐỀ: spec khai H lấy nguyên văn từ gói reviewer có `hint_provenance.json` 40 hunk và executor tái dẫn xuất từng hunk; biên bản nói còn 4 hunk bị bác cần kiểm. Bundle không có bảng provenance, định danh 4 hunk, nội dung trước/sau hoặc bốn lý do bác. Do đó reviewer không thể đánh giá bốn lý do như nhiệm vụ yêu cầu, hay xác nhận phạm vi hint theo §8. Không khẳng định đã chép trái phép; kết luận là **thiếu bằng chứng bắt buộc**.

ĐÃ THỬ VÁ: không bịa bốn lý do; đề nghị bổ sung provenance có source/hash/path/hunk, quyết định nhận/bác và phản chứng của từng quyết định. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `rg -n --hidden 'hint_provenance|4 hunk' tai-lieu cay-kho/ops` chỉ dẫn về lời nhắc; inventory/lịch sử tệp provenance cho 0 hiện vật. **KHÔNG ĐO ĐƯỢC 4/4 lý do bác**. Chỉ hai tiền tố băm khối H được xác nhận bằng mã trích thực tế; việc này không xác nhận 40 hunk.

ĐỘ TIN: cao về thiếu hiện vật; không có kết luận về tính đúng/sai của từng lý do.

### a9-khai-sai-base-ngoai-le  [P2]  A9 nói BASE không ném ngoại lệ, trái mã thật và chính bảng D9

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:737`, `:744`, `:812`; bảng D9 tại `:395`; Issue #464 `:69`.

VẤN ĐỀ: A9 và chua_do_duoc nói BASE nhận chuỗi 5000 chữ số thì trả 1 không ném, ngoại lệ chỉ là thuộc tính H; bảng D9 cùng tệp lại ghi BASE=EXC. BASE đang gọi int() trên nhóm đầu, nên 5000 chữ số ở nhóm ấy cũng ném ValueError. A9 là yêu cầu chẩn đoán hữu ích nhưng lời khai so nền không đúng; ca này thuộc ranh giới D9 đã công khai, **không** tính vào Đ1 hay gán thành lỗ xanh mới.

ĐÃ THỬ VÁ: không sửa nguồn; đề nghị gắn cùng fixture nguyên byte cho cả hai vế và sửa lời khai BASE. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: gọi `replay` của `do-review/harness.py` với `TONG: CA <5000 số 9>/<5000 số 9> dat · DOT BIEN 34/34 bi giet\nTONG: DAT\n` và riêng `<5000 số 9>/<5000 số 9>\n` của nhanh: **BASE=ValueError, H=ValueError ở cả 2 ca**, xem `do-review/d9-comparison.json`. Đặt số dài vào cặp mutant không được BASE bắt của mcp cho BASE=0/H=ValueError (`contracts.json`), càng cho thấy phải chỉ rõ fixture.

ĐỘ TIN: cao.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  Diễn giải biên độ khác tải thành nhiễu rồi cho phép nới A1

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:120`, `:429`, `:599`; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:35`.

VẤN ĐỀ: biên độ 10,28 phút của 11 job trên 11 head được diễn giải là nhiễu runner; chua_do_duoc còn yêu cầu nới A1 theo “phương sai” trong khi A1 đóng băng ≤25,00 và dặn không nới. Các head không cùng khối lượng: 1b3caa1 có 39 bước, không có bien-nhan v2; 10 head kia có 40 bước, thêm selftest này. Dải quan sát không cô lập nguyên nhân runner và không phải phương sai (đơn vị phút bình phương). Vì thế chưa đủ cơ sở để quyết định tăng ngưỡng; thay acceptance cần revision theo §3.2. Ngưỡng mới cũng chưa được xác định, nên hai người có thể chấm khác một kết quả.

ĐÃ THỬ VÁ: không tự chọn ngưỡng; đề nghị giữ A1 hiện hành tới khi có phép so cùng head/cùng bộ bước và quyết định revision minh thị, gọi đúng đại lượng biên độ. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/extra_checks.py` đọc YAML ở đủ 11 git head: 1×39 bước, 10×40 bước. `recheck_contracts.py` tái tính các số đã in: dải 10,28; ước max sau tách 21,03; biên A1 3,97. Ví dụ 28 phút trượt ngưỡng 25 nhưng qua ngưỡng minh hoạ 21,03+10,28=31,31 — đây là phản mô hình cho sự mơ hồ, không phải ngưỡng được tác giả chọn. Nhiễu runner thật và bảng bước gốc **KHÔNG ĐO ĐƯỢC** vì không có TSV/log.

ĐỘ TIN: cao về khác tải và mâu thuẫn văn bản; không ước lại nhiễu.

### issue-chep-nham-du-lieu-va-chan-doan-cu  [P2]  Thân Issue còn mẫu đầu vào và mô tả của bộ khác

TỆP/DÒNG: `ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md:15`; `ops/issues/465-MUTANT-WINDOWS-SUBAGENT-GHI-DETECT.md:15`; các Issue #463:80, #464:92, #465:42, #466:43.

VẤN ĐỀ: bảng #464 lại bỏ dòng TONG: DAT nhưng khai hai hàng đầu trả True — lỗi ví dụ đã được sửa trong spec chính. #465 chép điểm quan sát 8/8 và seam NHANH_DON_DUOC của bộ nhanh sang subagent (thật in CA33/33 · DOT BIEN22/22), còn nói bản vá không đổi điểm quan sát trong khi M2/M5 đòi dòng Windows riêng. Cả bốn Issue vẫn quy lỗi mạng cho proxy cấm WebSocket dù biên bản cùng PR có đính chính 03:55Z rằng kết luận đó sai, nguyên nhân chưa biết. Các sai lệch này làm nội dung đưa cho chủ kho khác bản đặc tả và phần đính chính.

ĐÃ THỬ VÁ: đã thử thêm terminator vào fixture trong harness, hai hàng đầu BASE trở về True; đề nghị chiếu lại các đoạn từ đúng spec/bản đính chính, không tạo lời giải thích mạng mới. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python do-review/recheck_contracts.py`: bảng Issue BASE=False/False/False, lệch **2/3** lời khai; thêm terminator thành True/True/False. `outputs/subagent_ghi_detect_test.stdout:66` có tổng CA33/33 · DOT BIEN22/22, rc=0; `nhanh_don_duoc_test.rerun.stdout:19` có 8/8. Đối chiếu văn bản đính chính `ops/reviews/GHI-NHAN-CROSS-REVIEW-LUOT5-KHONG-HOAN-TAT.md:169`; mạng trực tiếp **KHÔNG ĐO ĐƯỢC**, không nhận chẩn đoán cũ hay tự kiểm endpoint.

ĐỘ TIN: cao.

### gate-lease-cam-sua-phan-chung  [P2]  Điều kiện dừng cấm hàm mà nghiệm thu yêu cầu sửa

TỆP/DÒNG: `ops/leases/gate-tach-job-cat-chi-phi-exec-1-claude-20260906.yaml:167`; đối chiếu `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:358`, `:525`.

VẤN ĐỀ: lease cấm đụng “bất kỳ hàm nào khác loi_ruff_ci” trong ci_dang_ky_test.py. Spec cho phép loi_ruff_ci và phản chứng của nó, đòi thêm 4 ca A7 vào phan_chung(). Giữ đúng điều kiện dừng của lease thì không bổ sung được các ca bắt buộc. Không mở lỗ runtime hiện tại nhưng hợp đồng thi công mâu thuẫn.

ĐÃ THỬ VÁ: không sửa lease; đề nghị ngoại lệ rõ cho phần phản chứng A7 trong phan_chung(), đồng bộ lease/spec. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: đọc AST/tệp `ci_dang_ky_test.py` thấy phan_chung là hàm độc lập với loi_ruff_ci; `recheck_contracts.py` đo consumer nền 0 lỗi, YAML đã tách 1 lỗi, xác nhận cần ca đổi màu A7. Đây là đối chiếu hợp đồng, không khai đã thi công 4 ca.

ĐỘ TIN: cao.

## Đánh giá chất lượng câu hỏi §12 — không chọn thay chủ kho

Ba lựa chọn đã tách được chi phí/phạm vi: (1) H trong 1 tệp với hợp đồng hữu hạn; (2) đổi bên in, 8 formatter + 1 consumer = 9 tệp, tối thiểu 3 packet nếu giữ trần 3 tệp; (3) dừng/tách lại và giữ lịch sử finding. Các lựa chọn đủ cụ thể để bàn về hướng đi, và việc H là thiết kế thứ năm được nói rõ. Tuy vậy, số 311/419 và bảng chi phí không có hiện vật; không đủ để coi khuyến nghị (1) đã được chứng minh. Chi phí ≥3 vòng của (2) chỉ là cận dưới từ số tệp, chưa phải lịch thi công đã kiểm độc lập/tự đủ từng slice.

| điều kiện | đo được thế nào | kết luận trên bundle này |
|---|---|---|
| Đ1 | So `chay_moi` với kỳ vọng gắn từng fixture; đếm ca **khác kỳ vọng**, gồm cả bỏ sót có kết quả 0. Cần đóng băng manifest các ca/lớp ranh giới. | Đo được trên bộ mới: 1213/0/0. Bảng viết “số mục ĐỎ” chưa đủ rõ cho chiều bỏ sót; nguyên bộ 49+5 chưa có để đối chiếu ID máy móc. |
| Đ2 | `_chay_that` rc=0, lưu stdout nguyên byte/hash, H đếm trên cả 8 formatter. | Chốt cụ thể, có thể bác được H; hiện 0/6 bị bác, 2 chưa đo được. Cấm coi dữ liệu tổng hợp/canonical là test xanh thật. |
| Đ3 | Một formatter/packet có yêu cầu metadata n/m trên dòng tổng là chứng cứ dương làm điều kiện đạt. | Có thể đo khi có yêu cầu cụ thể; không có snapshot mọi packet đang mở để chứng minh không tồn tại yêu cầu. Chỉ rõ ai ghi/duyệt yêu cầu, lưu nguồn. |
| Đ4 | Additions runtime trên tệp consumer so đúng base sau GATE, không lấy kích thước tài liệu hay net. | Đo được sau thi công; PR hiện runtime delta=0 nên chưa phải phép nghiệm thu ngưỡng. Hai khối H 21+29 không phải tổng additions triển khai. |
| Đ5 | Giữ danh sách 51 ca cũ, đếm ca mới thực sự chạy, kiểm N/N cùng các mutant bắt buộc. | Đo được sau thi công. Cần danh sách tên ca làm mẫu số; N/N suông không quyết được ca bị xoá/skip hay nhãn “test mới viết sai”. A9 cũng phải được kiểm, dù công thức hiện chỉ nêu A1–A6. |

Kết luận chất lượng: phần đặt câu hỏi tiến bộ và đo được ở mức thiết kế; **chưa đủ dữ liệu để chốt tiếp H vô điều kiện**. Chủ kho có thể quyết hướng/revision từ các giới hạn và phản chứng đã ghi, nhưng nên nhận đủ hiện vật trước khi dùng khuyến nghị hiệu quả/chi phí như bằng chứng. Review này không tự chọn (1), (2) hay (3), không cấp lease và không coi §12 đã hoàn tất.

## Giới hạn và bàn giao

Đã đối chiếu cả bốn spec, bốn thân Issue, bốn lease và hunk bia mộ; diff/numstat khớp exact SHA. Write set và dependency giữa bốn spec/lease nhất quán, nhưng các bản chiếu Issue/điều kiện lease còn mâu thuẫn như findings. Các số mới đã ghi cả phần khớp và phần lệch.

**KHÔNG ĐO ĐƯỢC**: stdout xanh thật mcp_gh/pretooluse trong rig này; replay nguyên bộ lịch sử và các kill-list; provenance bốn hunk; nguồn TSV thời lượng/billing; trạng thái GitHub, quyền/branch protection, đủ ref máy chủ tại lúc cấp, Windows thật. Không đánh giá những mục đó là pass. Không cần thêm lượt chạy nguyên các suite đỏ trong cùng rig để xác nhận lại cùng hạn chế.

Gói dữ liệu nằm trong `do-review/`, có `ARTIFACTS.sha256` để kiểm tính toàn vẹn. Không có bản vá branch kèm theo; mọi hướng sửa trong verdict mang nhãn “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”.

verdict: changes_requested
