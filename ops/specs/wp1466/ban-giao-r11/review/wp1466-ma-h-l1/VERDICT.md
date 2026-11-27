verdict: blocked
reviewed_sha: da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd
base_sha: 695916ea3bfffdd7b2e8fcb94b0740b3c421fe70
spec_sha256: 28de9d574cb617442845c47db3ec5c65cd832386511775dfdd68ee7243ea6f7c
reviewer: {provider: codex, model_family: openai, surface: codex_cli, transport: machine, effort: high, session_id: KHONG_DO_DUOC}
review_class: sensitive
review_axes: [Spec, Correctness, Tests, Standards/Security]
assurance: chưa cấp cross_approved; đích human_audited sau audit chủ kho
dem: {so_lop_mo: 2, so_bieu_hien_mo: 5, P0: 0, P1: 0, P2: 1, P3: 1}

Không đủ điều kiện approve. Còn một lớp P2 về hợp đồng đếm bản sao (Q3 chưa quyết) và một lớp P3 về độ phủ kiểm ID. Chọn **blocked** theo đặc tả §11: tìm thấy thiếu sót của đặc tả phải ra revision mới. Định nghĩa vận hành của phép (3) hẹp hơn lời hứa “nhân đôi … ở chỗ hiển thị bất kỳ”; không quy lỗi cho executor vì đã thực hiện đúng định nghĩa hẹp. Các gate chưa có bằng chứng dương được ghi riêng, không tự chuyển thành finding mới hay gọi là đã đạt.

Đây là review mã lượt 1, lời gọi Codex 11/13 theo giao việc; không tính các lượt review đặc tả thành lượt review mã. Không sửa kho, không push, không gọi API ghi. Hồ sơ kết thúc ngày 26-11-2026 UTC; mọi phép đo gắn H ở metadata. `effort: high` là cấu hình yêu cầu trong PROMPT; model/effort thực phục vụ và session ID không có biên nhận để kiểm độc lập. Không dùng danh tính executor làm bằng chứng cho reviewer.

## BẢNG LỚP — lớp MỞ

| slug lớp | finding IDs/biểu hiện | hạng cao nhất còn mở | nguồn lượt/SHA | phương án vá chung | phép kiểm đóng lớp |
|---|---|---|---|---|---|
| `phep-dem-ban-sao-khong-phu-ca-tep` | F01.a–d: chữ dính trước/sau khối; dòng chỉ dấu cách; trọn mục có đoạn nối; bản sao dính chữ ở đầu tệp | P2 | executor lượt 1 Q3; reviewer mã lượt 1 / da4e876 | chốt hợp đồng chung về bản sao, đồng bộ đặc tả/ADR/phép đếm | 7 khoá × vị trí × biên; nếu giữ lời hứa, bản sao thêm chữ phải đỏ, bản che xanh; đột biến đếm trọn đơn vị phải chết |
| `ca-id-chi-do-mot-gia-tri` | F02: sáu ca G8 đều quy về ID 99 | P3 | reviewer mã lượt 1 / da4e876 | thêm đại diện miền số và mutant chỉ nhận 99 | nền bổ sung xanh; mutant bị ca ID khác 99 giết; ba đối chứng khác họ sống |

Số biểu hiện đếm theo bốn dạng F01 và một dạng F02; 23 đầu vào lọt không phải 23 finding. F01 giữ đúng slug executor đã đặt; HANDOFF mục 7 đã nối nó với họ lịch sử `khoa-khong-neo-vi-tri-va-duy-nhat` (P1 của review đặc tả). Không đổi tên hay xoá lịch sử P1, không tính cùng phản chứng hai lần. Hạng P2 ở đây phản ánh mâu thuẫn hợp đồng về bản sao; không thấy đường sửa nội dung tại địa chỉ gốc mà vẫn qua băm.

Q3 chưa được miễn. Q0, Q2, Q4 và miễn Windows được dùng đúng nội dung chủ kho cung cấp trong PROMPT. Điều kiện của packet trong đặc tả §1 còn chặt hơn M1 mặc định: mọi P3 phải đóng, không dùng miễn P3. Review này không tạo nợ hoặc miễn mới.

## BẢNG LỚP ĐÃ ĐÓNG/ĐÃ KIỂM

Đối chiếu lịch sử §19 và handoff trên H. “Đã kiểm” chỉ áp dụng phạm vi ghi trong cột bằng chứng; không tuyên bố đóng nợ kế nhiệm.

| slug/nhóm đã có | kết luận trên H | bằng chứng dương và giới hạn |
|---|---|---|
| `neo-sai-don-vi-khop`, `neo-thieu-nghia-vu` | giữ phần đã vá: băm trọn 7 đơn vị tại địa chỉ | N5 7/7; các ca xoá câu/xoá khoá và mutant đều đạt; F01 riêng về bản sao |
| `kiem-chuoi-khong-doc-cau-truc` | giữ phần byte thô đã vá trong wp1466 | 35/35 biến thể byte độc lập; CRLF, splitlines, rstrip, che tại chỗ có mutant bị giết; phần ngữ nghĩa #1469 không nghiệm thu ở đây |
| `khoa-khong-neo-vi-tri-va-duy-nhat` | địa chỉ và bản sao đứng thành đơn vị đã kiểm; không kết luận đóng toàn bộ tính duy nhất | đổi tiêu đề cha rc9, hai mục cùng đường rc9, 7 bản sao nguyên đơn vị rc9; F01 là giới hạn còn mở được nối từ handoff |
| `tieu-chi-dong-xoa-khong-do-hanh-vi` | phạm vi cú pháp của H đạt | cả hai khối N8 in ĐẠT; đăng ký cũ giữ nguyên; không tái chạy toàn bộ 65 biến thể phá khối N8 của lịch sử |
| `dem-khong-khai-tap-ca`, `nghiem-thu-khoa-so-ca-trai-quyen-them` | tập đếm và quyền thêm được giữ | 57/57 ⊆ T=60; 26/26 ⊆ 29 mới; chênh CASES và Linux đều 60 |
| `doi-chung-khac-ho-chon-nham-doctrine`, `ma-tran-dem-doi-loi-thay-doi-mau` | vòng đo thật đạt trong tập yêu cầu | 29/29 mới và 21/21 cũ: ca đích chết, mỗi mutant có 3 đối chứng khác họ sống |
| `moc-dot-bien-tu-khop-trong-khai-bao`, `doi-diem-goi-cong-chua-du-yeu-cau` | giữ phần đã vá | ca kiểm mốc nằm trong nền 63/63; mutant bỏ lời gọi giết 54 ca; rc6 cũ vẫn giữ |
| Q0: con trỏ ca bị hiểu là selftest | đã kiểm sửa theo lớp trên r9 | protocol byte-exact với p1–p6; `doc-claims-check --strict` H và base đều `ok:true`, 0 flags |
| Q2: bỏ sót khối trước tiêu đề đầu | đã vá đúng phần khối độc lập; lớp F01 vẫn mở | ba mutant phần đầu giết 2/1/1 ca; mutant reviewer bỏ khối ngắn bị giết 1; bản sao dính chữ còn lọt |
| Q4: trạng thái ADR dẫn r9 | đúng quyết định | N1 byte-exact; ngày 2026-11-26, URL kết thúc `issuecomment-7192181084` |

Các lớp đã chuyển theo E2/E5 sang #1469, #1470, #1484 giữ nguyên trạng thái lịch sử, không tính là được vá bởi H này. Review mã lượt 1 không có tỷ lệ hội tụ giữa hai lượt mã để báo; không lấy số đóng của review đặc tả làm tử số cho mã.

## BẢNG SĂN

Lệnh chạy từ thư mục giao việc, trừ khi ghi `out/h`. `run_logged.py` lưu nguyên argv, cwd, output, rc và thời gian tại `logs/<nhãn>.log`. Các script kiểm độc lập và JSON phản chứng nằm cạnh verdict. Với hướng đường dẫn/chuỗi độc hại chỉ dùng fixture có sẵn; không tự dựng payload. Bảng có hơn tám giả thuyết độc lập; dòng phần đầu là kiểm bổ sung cùng F01, không tính như lớp mới.

| hướng/giả thuyết | lệnh đã chạy | OUTPUT THẬT/kết quả |
|---|---|---|
| Địa chỉ có phụ thuộc tiêu đề cha, và có bắt oan tiêu đề con ngoài vùng khoá? | `python3 -B out/probes.py` | `ancestor/rename-root-heading: rc=9`; `ancestor/insert-child-before-K03: rc=0`, 2/2 đúng |
| Hai mục có cùng đường tiêu đề có bị lọt? | `python3 -B out/extra_probes.py` | `same-path-duplicate-K01 rc 9 expected 9`; K03 cùng kết quả |
| Byte có bị chuẩn hoá ngầm ở cuối đơn vị? | `python3 -B out/probes.py` | `raw-byte`: total 35, matched 35; 7 khoá × CR/TAB/NBSP/U+2028/BOM, tất cả rc9; BOM đầu tệp rc9 |
| Ranh giới dòng rỗng có bị đếm nhầm thành khối? | cùng lệnh | `blank-boundary`: 5/5, rc0; `eof/remove-final-newline: rc=0` |
| Vùng che có bị đếm như bản hiển thị? | `python3 -B out/extra_probes.py` | 14/14 bản sao trong fence/comment của 7 khoá rc0; tổng `EXTRA 25 / 25` |
| Chốt HTML có thực sự được gọi? | `python3 -B out/run_cases.py out/h out/base out/cases db-moi` | `inv_bo_chan_html → giết 1 ca đích · 3 đối chứng khác họ còn sống`; nền 63/63; dùng ca HTML có sẵn |
| Gốc resolve và liên kết trong/ngoài có phân biệt? | cùng lệnh | `inv_bo_kiem_duoi_goc → giết 1 ca đích · 3 đối chứng khác họ còn sống`; ca liên kết nội bộ xanh, không skip |
| Hậu tố/chuẩn hoá ID có làm lọt hay bắt oan tên nợ? | `python3 -B out/probes.py`; `python3 -B out/extra_probes.py` | `id-boundary`8/8, fullwidth rc9; `ID-debt-outside rc 0`; `prose-id-no-pipe rc 0`; ID00/01/09/10/28/98/99 đều rc9 |
| Bộ test có phân biệt miền ID với một giá trị cố định? | `python3 -B out/reviewer_mutants.py all-stock`; `… extended` | `ALL-STOCK 63 / 63 SKIP 0` dưới mutant chỉ 99; bổ sung nền 69/69, mutant bị giết 6, đối chứng 3 sống ⇒ F02 |
| Bản sao có thêm chữ ngoài đơn vị có còn bị đếm? | `python3 -B out/probes.py` | `copies`: total 33, matched 15, green 18; `preamble`: total 10, matched 5, green 5 ⇒ F01 |
| Bản vá phần đầu có ca đủ nhạy với độ dài khối? | `python3 -B out/reviewer_mutants.py extended` | `rv_preamble_drop_short_blocks → giết 1 ca đích · 3 đối chứng khác họ còn sống`; `TỔNG: ĐẠT` |
| Nguồn hỏng có biến thành im lặng xanh? | `python3 -B out/probes.py` | `input-error/invalid-utf8: rc=2`; `input-error/empty: rc=2`, đều có lỗi, không xanh. Cổng nguồn cũ chạy trước cổng mới; đây không đo nhánh đọc lỗi ở lần đọc thứ hai |
| Chữ mới có phá bộ dò claim hoặc sinh lỗi lint? | doc-claims H/base và `python3 -B out/lint_delta.py` | cả hai `ok:true`, `flags:[]`, advisory 392; Ruff thêm 0/mất 0 |

JSON `probes.json` lưu stdout/stderr thật của từng CLI. Script cố ý trả rc0 sau khi thu phản chứng; **không dùng rc của script ấy để gọi hành vi đạt**. 99 đầu vào trong `probes.py`: 76 đúng kỳ vọng, 23 phản chứng cho F01. `extra_probes.py`: 25/25 đúng. Dạng HTML giữa dòng trong Q3 chỉ được mô tả, chưa dựng thêm; không tính là phản chứng thực nghiệm thứ năm.

## BẢNG ĐO

| khẳng định (đặc tả/handoff) | khai | đo được | khớp? |
|---|---|---|---|
| Exact H, kiểm đầu tiên | da4e876890a1ebe99bb87de9e9a3b4f63c9fd5dd | HEAD đúng; tree `84018dbd9db5edcb1397e63d81911fc0320247aa` | có |
| Đặc tả đóng băng, kiểm trước review | sha256 28de9d57…ea6f7c | đúng toàn bộ băm ở metadata; blob `823e62c4f50c45425b38d2c71c04852e1dfc1543` | có |
| Lease/nguồn/phạm vi | r9 g2, base695916e, nhánh claude/wp1466-r9-g2 | `AUTHORITY 13 / 13`; snapshot lease c9a7a9838e82145ef7323ae34cac04c89f973706, hết hạn 2026-11-29T17:05Z; hash write set/spec khớp | có, trong snapshot |
| N1 ADR | khối adr, thay đúng giá trị | `N1 byte_exact=True`, 14.385 byte; sha256 `2da0db8a25bbbef3eba520353e07f4ad808f0bba0db3864d724b6b4a4fb945cc` | có |
| Sáu số Cưỡng chế | 0,11,0,0,0,0 | tự chạy đúng sáu lệnh; cùng số. `grep -c` rc1 ở kết quả0 là quy ước grep, không phải phép đo vắng | có |
| N2 protocol | base + đúng p1–p6 | `N2 byte_exact=True`; sha256 `3453ab9b6d7d7d803c4f852a03e1179e65884230f1723a5ef1ca62a95d80e29a` | có |
| N3 adr-song | H 67/67; base 66/66 | đúng, output sạch; 40/40 ca adr_song đạt, không skip | có |
| N4 doctrine-scan | sạch trên H và cổng chặn vi phạm | cây gốc và clone H đều quét 12 tệp sạch; ca bắt buộc đạt, nhưng F01 có 23 phản chứng | một phần |
| N5 băm độc lập | 7 khoá = khoa = hằng mã | `N5 7/7 tự băm = khoa = INV_KHOA_PROTOCOL`; parser riêng không import mã/hàm che sản phẩm | có |
| N6(a–d,f), đăng ký | 57 bắt buộc, T60; tổng 1864/Linux 1863 | 57/57; T60; 1804→1864, Linux 1803→1863; nền 63/63 không skip | có |
| N6(e) toàn bộ nền | 16 mảnh + hai CA_DAI | 16/16 mảnh hoàn tất: 1808/1823 đạt, 15 đỏ, 38 bỏ qua; đủ 1861 tên duy nhất; carrier đúng 1. Gom rc1. Hai CA_DAI chưa chạy | chưa cấp đạt |
| N7 đột biến mới | 26 bắt buộc, thực 29 | 26/26 có mặt; nền 63/63; 29/29 chết đúng lý do, mỗi mutant 3 đối chứng sống, TỔNG ĐẠT | có |
| N8 phạm vi mã/test | hai chế độ đạt | `PHẠM VI [ma]: ĐẠT`; `PHẠM VI [test]: ĐẠT`, khối trích nguyên từ spec | có |
| N9 hành vi cũ | doctrine 132, ADR 40, kiểm mốc, mutant21 | nền 132/132 +21/21; ADR 40/40; ca mốc đã đạt trong nền 63/63 của N7 | có |
| N10 Ruff F delta | base3+13, H3+13 | cùng 16 lỗi; thêm 0/mất 0 theo bộ mã/thông điệp bỏ số dòng/dòng nguồn; tl.py cùng 12 lỗi có sẵn | có; không phải lint sạch |
| Ký tự lạ trong .py | không thêm | packet_loop 0→0; test 12→12, giữ số thật của base hiện tại | có |
| N11 selftest/diff-check | handoff khai 1789/1789 | H 1773/1789; base 1773/1789, cùng 16 tên lỗi; diff-check sạch | không tái lập N/N |
| N12 kích thước | 4 tệp,+443−4,3 commit | 78/−1;170/−1;46/−2;149/−0; tất cả mode 100644; 443≤450,4≤6 | có |
| doc-claims strict | r9 hết 3 cờ L12 | H/base đều `ok:true`, `flags:[]`, `claims_flagged:392`, advisory 392 | có |
| N13 CI PR | sáu nhãn job success trên exact H | chỉ chạy được các bước cục bộ; H chưa push | KHÔNG ĐO ĐƯỢC |
| N14 full mutant audit | ci-dot-bien-du.yml success đúng H | không có run CI; chỉ 29 mới+21 cũ và 2 mutant reviewer tại chỗ | KHÔNG ĐO ĐƯỢC |
| N15 kiem-merge/master | đủ điều kiện trên H | chưa có PR/CI/assurance; không chạy hành động ghi | KHÔNG ĐO ĐƯỢC |
| N16 sau land | push master và đột biến đêm xanh | chưa land | CHƯA ĐẾN GIAI ĐOẠN |

Lệnh N1/N2/N5: `python3 -B out/independent.py`. Tệp `units.json` có đường tiêu đề, vị trí và băm; các khoảng dòng H lần lượt K01 49–82, K02 31–47, K03 851–894, K04 747–751, K05 1170–1176, K06 1178–1183, K07 1185–1188. N8: `python3 -B out/do-pham-vi.py ma out/base-packet_loop.py out/h-packet_loop.py` và chế độ `test` trên hai blob test. Sổ: `python3 -B out/so-dang-ky.py out/base out/h`. Các argv còn lại đầy đủ ở dòng đầu mỗi log.

Bộ chạy `run_cases.py` sao từ script executor sau khi đọc; dùng API thật `packet_loop_test_manh.chay`, không lấy kết quả executor làm bằng chứng. Phép băm, dò độc lập, mutant reviewer, so lint và kiểm authority do reviewer tự viết. Không tuyên bố mọi script là triển khai độc lập.

## Các gate cục bộ bổ sung và giới hạn môi trường

16 mảnh (`python3 -B out/full_shards.py`) đã hoàn tất: **1808/1823 đạt, 15 đỏ, 38 bỏ qua**, tổng 1861 ca được chọn,1861 tên duy nhất, carrier chỉ chạy ở mảnh 0. Gom bằng bộ chính thức báo `GOM: 15 lỗi · 16 mảnh · 1861 ca bắt buộc`, rc1: 14 mảnh đỏ cộng trạng thái job failure. Cả 15 ca đỏ trùng tên và nguyên thông báo với base, đều do socket bị sandbox chặn; 0 ca mới đỏ. 38 skip là 37 ca Windows native và `luong_canonical_chay_that`; không tính skip là đạt. Xem `shards-summary.json`, `shards/`, `logs/shard-*.log` và `logs/shards-aggregate.log`. Hai CA_DAI chưa chạy; N6(e) chưa đạt.

`pretooluse_guard_test` chạy đầy đủ H và base, đều **41/44**, cùng 3 ca t11/t15/t33 đỏ, cùng 4 mutant còn sống (m17,m18,m23,m26). Bộ chạy từ chối công bố điểm đột biến khi nền đỏ. Delta tên ca/mutant bằng 0; không tạo finding hồi quy và không gọi gate này đạt (`pretooluse-delta.json`).

`ci_dang_ky_test.py --chay`: phần hợp đồng đạt 33/33 đăng ký, 4/4 launcher Windows, 3/3 Ruff CI và 1677/1677 phản chứng. Pha chạy 18 bộ đã hoàn tất 7 bộ: 6 đạt, `mcp_gh_test` đỏ như base. Reviewer dừng nhánh bổ sung này bằng Ctrl-C (session exit130), vì các gate nền đã đỏ được đối chiếu và bộ pretooluse được đo riêng đầy đủ ở cả H/base. 11 bộ còn lại không có kết quả hoàn tất từ lượt này; không tuyên bố --chay hay gate-registry đạt. Xem `ci-registry-partial.json`, `logs/ci-registry.log`.

Đã đối chiếu riêng toàn bộ 15 ca `cong_b4_vc_*` và `cong_b4_gt4_*` trên base: 0/15 đạt, 0 skip; mọi ca cùng PermissionError khi tạo socket. Dữ liệu tên ca và lỗi nguyên văn ở `b4-base-results.json`; không gọi các ca này là đạt do lỗi có sẵn.

Đã đạt: idiom nền 7/7 và vòng mutant `TỔNG: ĐẠT`; gen_instructions 44/44; command_registry 10 tests/OK; ci_phamvi 7/7 và kiểm băm đạt. `workflow-audit --strict`, `golden-test`, `determinism-audit --strict`, `release-check --full`, `release-verify RELEASE_MANIFEST.json --strict` đều có `ok:true`. EOL kiểm 18.092 tệp, `ok:true`, `violations:[]`. Đây là bằng chứng bước cục bộ, không thay job GitHub.

Selftest H/base cùng 16 lỗi: 8 ca r973_bootstrap, r226, r268, 5 ca wp433, wp727_tl_gws_refresh; tên đầy đủ và output ở `logs/selftest.log`, `logs/selftest-base.log`, `summary.json`. Không có lỗi mới trong phép so tập. Môi trường có `.git` bảo vệ trên đường tổ tiên của thư mục tạm, ảnh hưởng các phép kiểm home/credential; một số fixture Git còn vướng dịch vụ ký commit bị sandbox chặn. Chỉ khẳng định nguyên nhân khi output cho thấy; không suy mọi lỗi đều cùng nguyên nhân.

`mcp_gh_test` H/base đều 38/42, cùng 4 ca A5/A6-302/A6-303/A7 lỗi PermissionError; vòng đột biến của bộ này từ chối đo vì nền đỏ (`logs/mcp-gh-base.log` và `logs/ci-registry.log`). `codex_cred_test` H/base đều 13/18, cùng 5 ca đỏ; không tính hồi quy của H. `pre_push_test` mặc định cả hai sập khi ký commit. Chạy lại cả H/base với cấu hình Git chỉ áp dụng cho tiến trình (`GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null GIT_CONFIG_COUNT=0`) cho 9/9 mỗi phía. Không sửa cấu hình Git chung. Những điều chỉnh này không biến selftest hoặc CI đầy đủ thành đạt.

Môi trường Linux, Python 3.13.18, Git 2.43, Ruff 0.15.15; không đồng nhất ảnh CI Python 3.12. Không chạy Windows, theo miễn C3/E2 đã được cung cấp. Không xác minh tình trạng GitHub hiện thời hoặc lease mới ngoài ảnh ref ngày 26-11; không thể suy từ snapshot rằng không có lease phát sinh sau đó. Không chạy hai ca dài CA_DAI (`wp1303_target_human_chain`, `wp1303_target_supported_pairs`), không chạy toàn bộ 2106 mutant, không có biên nhận GitHub N13–N16. Chưa tái lập được một bộ nền đầy đủ xanh nên không cấp assurance.

## Thẩm quyền, phạm vi và dấu vết git plumbing

Đã đọc nguyên văn chỉ thị cross-review của kho, các mục protocol được yêu cầu, M1–M12/ADR0060, ADR0062, ADR0063 và CLAUDE.md; áp dụng đặc tả r9, quyết định đã cung cấp, lease trong snapshot. Kho clone độc lập đầy đủ, ghim core.abbrev 7. Tất cả script, fixture và log viết trong `out/`; source `cay-kho` chỉ đọc.

HANDOFF lượt 1 thừa nhận đã dùng git plumbing sau khi chốt ghi tệp từ chối; lượt 2/3 dùng git apply. Trên exact H, kiểm tree/diff cho đúng 4 đường dẫn write set, mode 100644, không tệp thứ năm, không lệch nội dung ADR/protocol hay phần AST cũ. Không thấy dấu vết nội dung nằm ngoài phạm vi do cách ghi ấy để lại. Điều này **không chứng minh thao tác lịch sử đã được cho phép**, cũng không xoá sự kiện đi vòng chốt; giữ sự kiện cho audit human_audited của chủ kho. Commit đầu còn nhãn r8 g1 trong subject, hai commit sau đưa nội dung về r9 g2; không dùng subject thay lease/spec của H.

So băm toàn bộ cây gốc trước/sau: 19.076 tệp, 0 đường thay đổi; HEAD/tree/status không đổi (`snapshot-delta.json`). Đầu ra kiểm và clone dùng thử nằm ngoài kho gốc. Không có patch giao nộp, không hành động land/merge trong lượt reviewer này.

### phep-dem-ban-sao-khong-phu-ca-tep [P2] Bản sao nguyên byte có thêm chữ vẫn qua chốt duy nhất

TỆP/DÒNG: `.claude/dev/packet_loop.py:1774`; `docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md:42` (Q3, nhất là dòng 46–47); đặc tả r9 §0, §8.3, N4.

VẤN ĐỀ: `so_ban` chỉ băm trọn mục/khối. Thêm chữ bên ngoài bản sao làm khối chứa nó dài hơn, nên mất phép đếm dù nguyên byte của đơn vị vẫn hiển thị. Mã theo đúng định nghĩa hẹp của phép (3), nhưng không thực hiện lời hứa “nhân đôi nó ở chỗ hiển thị bất kỳ” và “khi còn một bản hiển thị khác mang cùng những byte ấy”. Q3 chưa có quyết định; không tự miễn hoặc chuyển thành nợ.

CÁC BIỂU HIỆN CÙNG LỚP ĐÃ QUÉT: `out/probes.py` dùng script độc lập lấy đơn vị, quét cả bảy khoá. 33 biến thể bản sao cuối tệp: 18 trả rc 0; 10 biến thể phần đầu: 5 trả rc 0. Phần bị lọt gồm K02, K03, K04, K05, K06, K07; K01 bị chốt ID bổ sung bắt. Chi tiết và stdout/stderr từng phép ở `out/probes.json`.

GỢI Ý VÁ: cần chốt lại hợp đồng trong đặc tả và ADR trước khi sửa mã. Nếu giữ lời hứa hiện tại, giữ kiểm địa chỉ/băm nguyên khối tại chỗ và thay riêng việc đếm bản sao bằng đối chiếu dãy dòng nguyên byte có hiển thị. Ca khoá bao phủ cả bảy khoá, phần đầu/thân/cuối và chữ dính trên/dưới; mutant quay về đếm trọn khối phải bị giết. Rủi ro: đếm nhầm bản trong rào/comment, chồng lấn và chi phí quét; cần đối chứng. Hướng thu hẹp lời hứa chỉ hợp lệ sau quyết định chủ kho và revision mới, không phải cách reviewer tự đóng lớp.

ĐÃ THỬ NGHIỆM: `python3 -B out/run_logged.py probes-fixed . python3 -u -B out/probes.py`: 23 phản chứng xanh ngoài mong đợi; log `out/logs/probes-fixed.log`. Lần đầu script reviewer lỗi bytes literal trước khi chạy ca nào, đã sửa script dưới `out/`; giữ log `probes.log`.

ĐỘ TIN: cao về hành vi; mâu thuẫn giữa định nghĩa vận hành và lời hứa phải được chủ kho giải quyết. Các hướng HTML giữa dòng chỉ mô tả, chưa tự dựng payload.

### ca-id-chi-do-mot-gia-tri [P3] Ca kiểm ID không phân biệt regex tổng quát với regex chỉ nhận 99

TỆP/DÒNG: `.claude/dev/packet_loop_test.py:20612` (sáu ca liên tiếp); các đột biến G8 ở dòng 20670–20672.

VẤN ĐỀ: sáu dạng viết đều quy về `INV-99`; không ca nào của G8 dùng một ID thật `INV-01`…`INV-28`. Đổi riêng `_INV_ID_TRAN` từ miền hai chữ số sang đúng 99 khiến chốt bỏ mọi ID thật, nhưng cả sáu ca đích vẫn xanh. Đây là thiếu độ phủ của test, KHÔNG phải lỗi regex đang chạy trên H; vì vậy xếp P3.

CÁC BIỂU HIỆN CÙNG LỚP ĐÃ QUÉT: cả sáu ca dạng chuẩn, không backtick, không gạch đầu, ký tự Cf, gạch mềm và chữ số toàn khoảng; ba mutant G8 chỉ bỏ chốt/đổi định dạng/bỏ chuẩn hoá, không thu hẹp miền số. Kiểm cả sổ CASES và các chỗ `INV-` trong tệp test.

GỢI Ý VÁ: thêm ca `doctrine_inv_*` tại cụm G8 cho ID hiện hành và biên 00/01/09/10/28/98, giữ luật hậu tố; thêm mutant chỉ nhận 99 với ca đích là các ca mới. Script `out/reviewer_mutants.py` chỉ thay sổ trong bộ nhớ và để bộ chạy chuẩn dựng bản sao mã; không phải patch sản phẩm. Nguy cơ: chốt đúng định nghĩa hai chữ số không được vô tình thu về 01–28; giữ đối chứng tên nợ và hậu tố.

ĐÃ THỬ NGHIỆM: `reviewer-id-all-stock.log`: toàn bộ 63/63 ca mới và đối chứng vẫn đạt khi chỉ nhận ID 99. `reviewer-mutants-stock.log`: nền 63/63, mutant `rv_id_only_99` có 6 ca đích VẪN XANH. Thêm sáu ca trong bộ nhớ: `reviewer-mutants-extended-fixed.log` nền 69/69, `rv_id_only_99 → giết 6 ca đích · 3 đối chứng khác họ còn sống`, `TỔNG: ĐẠT`, rc 0. Mutant độc lập `rv_preamble_drop_short_blocks` bị ca phần đầu tệp hiện có giết. Lượt extended đầu tiên khai cả sáu ca 99 làm ca phải chết nên vẫn đỏ; sửa danh sách đích về sáu ca mới, không sửa assertion hay mã H; giữ nguyên log cũ.

ĐỘ TIN: cao. P3 còn mở; không tự ghi nợ hoặc miễn.

Hồ sơ đo: `review-evidence.zip` chứa verdict, script, JSON và log; `SHA256SUMS` ghi băm từng tệp. Không đóng gói các clone/fixture tạm.
