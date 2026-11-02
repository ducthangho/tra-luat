Verdict: request_changes
Reviewed commit: a8f74709578f3c68833d366ed80b66fc10fbf0a3

Hoàn tất cross-review PR #1119 lượt 1: **request_changes — 0 P0, 0 P1, 0 P2, 2 P3**. Ba tệp cache nguồn bị bỏ mà không khai, và hai caveat #1114 mô tả sai rằng DIFF.patch không vào kho. Cổng HEAD/base đều đạt, đột biến băm bị chặn đúng cả bốn biên nhận, các mỏ neo/telemetry đối chiếu được đều khớp; README giữ đủ hàng cũ và thêm đúng 23 hàng. Ngưỡng người dùng yêu cầu không còn P0/P1/P2/P3 chưa đạt. Không cấp quyền merge/land.

Nhật ký tăng dần và kết quả phép đo ở dưới; các script ở gốc sandbox, output trong `evidence/`. Chỉ dùng git và tệp tại chỗ; dữ kiện GitHub ngoài các nguồn đó: KHÔNG ĐO ĐƯỢC.

Finding đã xác nhận:

- [P3] bo-sot-cache-khong-khai: `ops/reviews/pr1114-review-1-codex/OMITTED.txt:1` — `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py` — nguồn có 50 tệp, lưu 44; 6 tệp vắng nhưng chỉ 3 tệp được khai. Ba tệp thiếu khai là `evidence/ruff-cache-created/.gitignore` (35 bytes), `evidence/ruff-cache-created/0.17.3/12591984194595340168` (252 bytes), `evidence/ruff-cache-created/CACHEDIR.TAG` (43 bytes), tất cả `declared=false`. Chính VERDICT gốc dòng 138 nói cache đã chuyển vào evidence. Hướng vá: giữ cache ngoài kho nếu chủ ý, thêm từng đường dẫn/sha256/bytes/lý do vào OMITTED.txt rồi tái sinh SHA256SUMS; hoặc chép nguyên byte đủ ba tệp. Kiểm lại toàn bộ tập nguồn, kể cả tệp ẩn/thư mục con, phải không còn nguồn vắng mà thiếu khai. Rủi ro vá: cập nhật OMITTED.txt mà quên manifest làm sha256sum đỏ; không sửa VERDICT nguồn.

- [P3] caveat-loai-diff-sai: `ops/reviews/pr1114-review-{1,2}-codex-verdict.receipt.yaml:89` và `ops/reviews/README.md:857,863` — `PYTHONDONTWRITEBYTECODE=1 python3 audit_claims.py` (đối chiếu byte: `python3 audit_bytes.py`) — cả hai caveat `TEP-LON-KHONG-VAO-KHO` khai `DIFF.patch ... KHONG vao kho`, nhưng `pr1114-review-1-codex/DIFF.patch` (1913 bytes) và `pr1114-review-2-codex/DIFF.patch` (4160 bytes) tồn tại, khớp nguồn/git diff và nằm trong SHA256SUMS. Hướng vá: thu hẹp mô tả hai biên nhận này theo đúng các tệp bỏ trong OMITTED.txt; cập nhật hai hàng README tương ứng. Kiểm rằng mọi tên tệp được khai bỏ thực sự vắng và README vẫn khớp từng caveat. Rủi ro vá: sửa hàng cũ hoặc nhầm hai biên nhận #1110 vốn thực sự bỏ DIFF.patch; giữ nguyên hiện vật/verdict gốc.

Preflight — `PYTHONDONTWRITEBYTECODE=1 python3 prepare_audit.py`: HEAD/tree/base, status, phạm vi và DIFF.patch ở `evidence/preflight.json`; 254 đường dẫn đổi, `out_of_scope=[]`, `input_patch_equal=True`. Hai bản sao `work/head`, `work/base` đã ghim `git config core.abbrev 7`; `audit.gitconfig` áp cho phép đo git trên clone gốc.

Byte — `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`: kết quả `evidence/bytes.json`, ánh xạ chi tiết `evidence/pr*-mapping.json`; 237 tệp nguồn được đối chiếu. Output `mapping_failures=[]`, manifest sạch, original_diff_equal=true cả bốn; ba thiếu khai được chỉ ra ở omissions của #1114 lượt 1; đây là phép đo mới, không dùng bảng mapping của executor làm đầu vào.

Cổng base — `PYTHONDONTWRITEBYTECODE=1 python3 audit_gates.py base`: bien-nhan rc=0, land rc=0, direct rc=0, doctrine rc=0, diff-check rc=0. Lệnh và output nguyên văn: `evidence/base-gates.json`, `evidence/base-*.stdout/.stderr`.

Cổng head — `PYTHONDONTWRITEBYTECODE=1 python3 audit_gates.py head`: bien-nhan rc=0, land rc=0, direct rc=0, doctrine rc=0, diff-check rc=0. Lệnh và output nguyên văn: `evidence/head-gates.json`, `evidence/head-*.stdout/.stderr`.

Biên nhận — `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py`: 328 đối chiếu, 0 lệch. Từng trường/lệnh git nằm ở script; expected/actual ở `evidence/receipt-checks.json`, tóm tắt `evidence/receipts.json`. Giới hạn: đối chiếu run.json là đối chiếu hiện vật, không tự xác thực nhà cung cấp/phiên máy chủ.

README — `PYTHONDONTWRITEBYTECODE=1 python3 audit_readme.py`: 1217 → 1240 hàng `| `; thêm 23, mất 0; 4 hàng mục lục + 19 caveat khớp biên nhận. Dùng multiset để bắt cả mất/trùng dòng; chi tiết `evidence/readme.json`. Nội dung caveat vẫn được kiểm riêng, không coi khớp nhau là tự đúng.

Nội dung kết luận/tiền lệ — `PYTHONDONTWRITEBYTECODE=1 python3 audit_claims.py`: 45 đối chiếu kết luận/hiện vật lịch sử, 0 lệch; 22 trường cố định × 3 tiền lệ × 4 biên nhận, lệch 0. Không coi đối chiếu log cũ là chạy lại suite lịch sử. Hai caveat #1114 cùng `claims_DIFF_omitted=true`, `DIFF_present=true`, `DIFF_in_manifest=true`, `DIFF_in_OMITTED=false` (P3 caveat-loai-diff-sai). Chi tiết `evidence/claims.json`.

Đột biến — `PYTHONDONTWRITEBYTECODE=1 python3 audit_mutations.py`: 4 lần đổi duy nhất verdict_sha256 trên bản sao `work/mutant`, từng lần hồi nguyên; 8 / 8 lần cổng bien_nhan_v2 và t26 đỏ, nêu đúng tên biên nhận bị đổi. Chi tiết command/rc/output ở `evidence/mutations.json`, `evidence/mutant-*.stdout/.stderr`.

Kiểm cuối — `PYTHONDONTWRITEBYTECODE=1 python3 final_audit.py`: rc=0; 10459 tệp clone gốc trước/sau, changed/added/removed=[]; status rỗng; HEAD/tree giữ nguyên; DIFF.patch vẫn khớp; `git diff --check f4b513d HEAD` rc=0, không output. Bản đột biến đã hồi nguyên, status rỗng; 4 đột biến/8 lần chặn đúng tên. Classifier có cùng blob tại HEAD và cả bốn reviewed_sha. Kết quả: `evidence/final-integrity.json`.

Bảng cổng đo lại: chạy từ `work/base` và `work/head`, `PYTHONDONTWRITEBYTECODE=1`, `core.abbrev=7`. Lệnh bao và rc: `python3 audit_gates.py {base,head}`; toàn bộ stdout/stderr đã lưu.

| Lệnh thực trong mỗi bản sao | Base | HEAD | Delta |
|---|---|---|---|
| `python3 ops/bien_nhan_v2.py --root .` | rc0; 287 ĐẠT v2, tổng 340 | rc0; 291 ĐẠT v2, tổng 344 | +4 v2; vi phạm 0→0; KHÔNG ĐO ĐƯỢC 0→0 |
| `python3 ops/land_evidence_nguon.py --root .` | rc0; 75 ĐẠT, 25/28 miễn trừ, tổng 100 | cùng output | 0 |
| `python3 ../../direct_gates.py .` | rc0; 3 PASS | rc0; 3 PASS | 0 |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | rc0; quét 10 tệp, 0 chỗ chép doctrine | cùng output | 0 |
| `git diff --check f4b513d HEAD` | rc0; rỗng | rc0; rỗng | 0 |

Ba hàm được gọi trực tiếp: `t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi`, `t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc`, `t27_phan_chung_verdict_duoi_HOA_thieu_muc_luc_phai_DO_tren_moi_nen`. Hai SyntaxWarning về escape trong lease_publish_test.py xuất hiện ở cả base và HEAD; không có lỗi mới. Biên nhận: legacy 11/11 và nợ 42 giữ nguyên; nợ câu lịch sử L-REVIEW=1, L-ANCESTRY=60, L-SURFACE=0 giữ nguyên (`evidence/{base,head}-bien-nhan.stdout`).

Byte/độ phủ — lệnh `PYTHONDONTWRITEBYTECODE=1 python3 audit_bytes.py`, output `evidence/bytes.json`:

| Thư mục | Tệp nguồn cấp | Chép khớp byte | Vắng, khai đúng hash/bytes | Vắng chưa khai | SHA256SUMS entries/rc |
|---|---:|---:|---:|---:|---|
| pr1110-review-1-codex | 61 | 58 | 3 | 0 | 59/rc0 |
| pr1110-review-2-codex | 46 | 44 | 2 | 0 | 45/rc0 |
| pr1114-review-1-codex | 50 | 44 | 3 | 3 | 45/rc0 |
| pr1114-review-2-codex | 93 | 91 | 2 | 0 | 92/rc0 |

Bốn bản phẳng bằng VERDICT nguồn. Tập manifest phủ đúng mọi tệp đã lưu trừ chính SHA256SUMS, gồm OMITTED.txt; không thiếu, thừa hoặc trùng mục. Lệnh thật `sha256sum -c SHA256SUMS` chạy riêng trong từng thư mục, lần lượt 59/45/45/92 dòng OK. Tổng 250 tệp nguồn cấp: 237 chép khớp byte, 10 vắng đã khai đúng, 3 vắng chưa khai. Các thư mục cay-kho/work/copies và nguồn con không được cấp trong đầu vào không nằm trong phép kiểm kê này.

Hai DIFF.patch bị bỏ của #1110: `git diff c6dd7b3 e137f8c` và `git diff fb74c6e 3a3aac5` đều sinh **261239 bytes**, SHA256 `79c3d941cbfbc0cb32301c73d00237885aaf275bfef3aef347c1a5ded42968b6`, bằng byte nguồn. Bốn launcher.err đều 0 bytes, SHA256 `e3b0c44298fc1c149afbf4c8996fb92427ae41e4649b934ca495991b7852b855`. Bốn tệp nguồn >500 KB bị bỏ có kích thước 2043534, 822015, 838749, 1415498 bytes; hash/bytes đều khớp OMITTED.txt (`evidence/bytes.json`).

Ba tệp thiếu khai của P3 bo-sot-cache-khong-khai — output do audit_bytes.py tự băm, tiền tố đường dẫn `nguon/review1114a/evidence/ruff-cache-created/`:

| Tệp | Bytes | SHA256 |
|---|---:|---|
| `.gitignore` | 35 | `9e3a60f1e6ec4ae60215c11d54b171392745ec25e9dded433d5bd921363af316` |
| `0.17.3/12591984194595340168` | 252 | `d001930daafa34484d4322965804766ba8b1fce65cd1999142048c4f36b41588` |
| `CACHEDIR.TAG` | 43 | `5953156d7e0c564a427251316eaf26f8870e6483ae2197f916b630e4f93e31ae` |

Biên nhận — lệnh `PYTHONDONTWRITEBYTECODE=1 python3 audit_receipts.py`: mỗi biên nhận 82 đối chiếu, tổng 328, `failures=[]`. Dữ liệu actual/expected từng trường nằm trong `evidence/receipt-checks.json`.

| PR/lượt | reviewed_sha | tree | run_id | Giây / sự kiện model | sandbox_trang_thai |
|---|---|---|---|---|---|
| pr1110-review-1-codex | `e137f8ce1215e0e6a6c8fbc1aa949b31fa2e4e7d` | `49821da8bbf5787a4e10ffcc854354e6c72f9cf8` | `0f91d66df4fd4d16bfeeabfc8246333c` | 420.462 / 21 | KHONG_DO_DUOC |
| pr1110-review-2-codex | `3a3aac561ba359c08dfe92d95584b56494fc12d4` | `2fc9c77d7fb38e2b09b755bb125cb1dff4a33562` | `cac7c0b6484f455e985fd7bc40a44fb8` | 374.648 / 23 | DO_DUOC |
| pr1114-review-1-codex | `e101b11e9586de3125f811ec4f42a89af69de8f2` | `b2c8cab562f146cafd255fe8942c158b8c6c0f7d` | `df61ed4f35124a258437eef00af715aa` | 613.423 / 32 | KHONG_DO_DUOC |
| pr1114-review-2-codex | `51435a44659c4026539497a47ace971a71a64f40` | `7c160ae144195d4f22089ec49d39e45033030381` | `a545a3bc36754793a48a3e2d8dccd599` | 745.124 / 33 | KHONG_DO_DUOC |

Cả bốn run.json ghi ma_thoat=0, trang_thai=xong, mọi sự kiện model gpt-6-astra và effort xhigh; duration khớp hiệu timestamp sau làm tròn 3 chữ số. Prompt SHA256 bằng PROMPT.md; run/launcher/checkpoint và băm stdout/stderr khớp. Caveat SANDBOX-KHONG-DO-DUOC có đúng ở #1110 lượt 1, #1114 lượt 1 và lượt 2; vắng đúng ở #1110 lượt 2. KHONG_DO_DUOC không chứng minh không có sandbox: các run đó vẫn có mẫu quan sát, nhưng sampler ghi lỗi DanhTinhDoi.

Các lệnh git trong audit_receipts.py cho: `f4b513d^2=3a3aac561ba359c08dfe92d95584b56494fc12d4`, `fb74c6e^2=51435a44659c4026539497a47ace971a71a64f40`; `git merge-base --is-ancestor e137f8c f4b513d` và `... e101b11 fb74c6e` đều rc0. Hai lượt 1 không được đồng nhất với head cuối. Hai merge đều là tổ tiên origin/master tại chỗ; ngày commit 2026-11-01 và message mang đúng số PR. Đây là phép đo git, không xác nhận yêu cầu API merge đã gửi.

`git merge-base --is-ancestor cf5acfa HEAD` rc0; cả bốn URL neo đúng commit `cf5acfa7282ec42ef282015fa27fc642a4515588`, đúng verdict_path; `git show <anchor>:<path>` bằng byte verdict và hash receipt. `_tinh_lop_tu_write_set` trên từng diff base..reviewed_sha cho sensitive ở cả bốn, số đường dẫn lần lượt 46/46/1/1. Dòng verdict, Reviewed commit, số finding P0/P1/P2/P3=0/0/0/0 khớp nguồn; caveat P3 không bị đếm thành finding.

`python3 audit_claims.py` cho 45 đối chiếu kết luận/log lịch sử khớp. Cụ thể: #1110 lượt 1 có 41 bản sao/2 khai bỏ/116 đối chiếu trong nguồn verdict; cả hai lượt #1110 có delta README lịch sử +4, mất0; diff ops/reviews giữa hai lượt rỗng. #1114 cả hai lượt có 52/52 và 80/80 trong log nguồn; lượt 2 cộng lại các worker được 26/1800→0/1800, đếm 20 chuyển R→Z/1200, thời gian suite tăng 15.017 s (4.92%). Các con số này đối chiếu câu ket_luan với hiện vật nguồn của lượt cũ, không phải số hiện vật được ghi sổ trong PR #1119 và không phải chạy lại review lịch sử.

Tiền lệ pr1058 lượt 1/2 và pr1075 lượt 1: 22 trường cố định × 3 × 4 đều bằng nhau (`evidence/claims.json.precedent`). Các khác biệt nội dung có căn cứ: pr1058 lượt 1 changes_requested nên có assurance_KHONG_dat và không có ket_luan; bốn verdict mới approve nên cross_approved và có ket_luan. Caveat head-cuối được thêm cho hai lượt 1, sandbox caveat theo run tương ứng; không phát hiện lệch tiền lệ khác ngoài mô tả loại DIFF sai đã nêu.

Đột biến — `PYTHONDONTWRITEBYTECODE=1 python3 audit_mutations.py`, chỉ thay ký tự đầu verdict_sha256 từng tệp trong `work/mutant`, không chạm clone gốc. Output nguyên văn trong `evidence/mutant-*.stdout/.stderr`:

| Biên nhận | Băm trước→sau (tiền tố) | bien_nhan_v2 | t26 | Đích bị báo đỏ |
|---|---|---:|---:|---|
| pr1110-review-1-codex-verdict.receipt.yaml | 74409dde8964→04409dde8964 | rc1 | rc1 | đúng tệp; foreign_receipts=[] |
| pr1110-review-2-codex-verdict.receipt.yaml | a7a69903810e→07a69903810e | rc1 | rc1 | đúng tệp; foreign_receipts=[] |
| pr1114-review-1-codex-verdict.receipt.yaml | c4dd8f14224f→04dd8f14224f | rc1 | rc1 | đúng tệp; foreign_receipts=[] |
| pr1114-review-2-codex-verdict.receipt.yaml | 51eec0ee8a1f→01eec0ee8a1f | rc1 | rc1 | đúng tệp; foreign_receipts=[] |

bien_nhan_v2 báo `blob tại evidence_url băm ... nhưng biên nhận khai verdict_sha256 ...`; t26 báo `LỆCH BĂM`. Hai t27 vẫn PASS ở mỗi bản đột biến. Chỉ dùng đột biến hash để đáp ứng yêu cầu mỗi biên nhận một trường đo được; không suy rằng đã thử đột biến riêng mọi trường reviewed_sha/evidence_url.

Giới hạn: GitHub hiện tại, nội dung/job CI Windows thật và kết quả CI ngoài các tệp cấp, quyền credential/actor đăng, chỉ thị chủ kho trong phiên executor, giá trị expectedHeadSha gửi lên API, URL còn phục vụ trên GitHub: **KHÔNG ĐO ĐƯỢC**. Dòng “Windows that do o CI ngoai luot review” được coi là lời khai ngoài review, không là phép đo của lượt này. Phiên/nhà cung cấp độc lập phía máy chủ, toàn bộ argv chạy lịch sử và phiên bản CLI ngoài hiện vật được cấp: **KHÔNG ĐO ĐƯỢC**. Đã đối chiếu metadata hiện vật; không nâng tính mạnh của nó thành xác thực ngoài nguồn. Các thư mục nguồn con/cây kho lịch sử đã bị loại khỏi đầu vào không được tự suy là đã kiểm byte. Không dựng nội dung nhạy cảm và không chạy mạng.
