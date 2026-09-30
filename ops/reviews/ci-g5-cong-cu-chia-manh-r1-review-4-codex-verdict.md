# Cross-review độc lập — packet #668, lượt 4

Trạng thái lúc khởi tạo: `dang_review`. Kết luận cuối ở cuối tệp.
reviewed_sha: 971e14c1550bcbc3d1523791f8174f78a45edbf9

Cross-review độc lập lượt 4. Chỉ đo, phản chứng trên bản sao /tmp; không sửa mã sản phẩm.

HƯỚNG 1: Neo review và registry
  giả thuyết : Bundle đúng SHA/spec; registry hiện tại không hồi quy.
  lệnh       : git -C cay-kho rev-parse HEAD; sha256sum SPEC.md;
               python evidence/env.py python -u /tmp/review668-r4/.claude/dev/ci_dang_ky_test.py
  output     : HEAD=971e14c1550bcbc3d1523791f8174f78a45edbf9;
               SPEC=dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15;
               PHẢN CHỨNG: 1013/1013 đỏ đúng; TỔNG: ĐẠT.
  kết luận   : KHÔNG PHẢI LỖI. Log evidence/registry.log. Chạy bản sao /tmp, không chạy --chay/CI.

HƯỚNG 2: Răng bản vá F1/F3 bằng các phản chứng CÓ SẴN
  giả thuyết : Các ca có tên nhưng không thực sự cắn bản vá ngữ nghĩa workflow.
  lệnh       : python evidence/env.py python -u evidence/ablation.py
  output     : control suite_ok=True, F1=20, F3=28, escaped=[];
               gỡ job_keys: 3 LỌT; job shape: 5 LỌT; step keys/shell: 7 LỌT;
               action with: 2 LỌT; setup env: 1 LỌT; mỗi suite_ok=False.
  kết luận   : KHÔNG PHẢI LỖI trên các nhánh đã đo. Dùng nguyên phan_chung trong cây, không tự soạn
               workflow/chuỗi điều khiển hoặc ký tự ẩn. Log đầy đủ evidence/ablation*.log.

  Bổ sung HƯỚNG 2: ablation `splitlines` ⇒ 27/28 ca F3 LỌT, suite_ok=False;
               đối chứng cả 28/28 đỏ đúng. Ca NBSP vẫn bị chặn bởi nhánh không đột biến.

HƯỚNG 3: Hồi quy gate trọn vẹn và công cụ nền
  giả thuyết : Gate giao mảnh làm mất cổng nền/tự kiểm, hoặc thay đổi gây hồi quy ngoài phạm vi.
  lệnh       : CONG_CU_TEST_BAN_KINH=manh python evidence/env.py python -u /tmp/review668-r4/ops/cong_cu_test.py;
               python evidence/env.py python -u evidence/compat.py
  output     : gate rc=0; TỰ KIỂM SONG SONG (N126): ĐẠT;
               SỐ LIỆU: ca=56 · đột biến=254 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT.
               actionlint 1.7.7 head/base rc=0; t152 head/base 1/1 qua, 0 bỏ qua, 0 hỏng.
               Ruff 0.15.8 head/base rc=1, cùng 6 finding F, RUFF_DELTA_ZERO=True.
  kết luận   : KHÔNG PHẢI LỖI ở gate và các phép đo đã nêu; Ruff đang đo thêm phiên bản ghim 0.15.15.
               Log evidence/gate.log, compat.log, ruff.json. Dòng giao mảnh KHÔNG chứng minh đã đo đủ 254.

HƯỚNG 4: Main — liệt kê quyết định và đột biến độc lập (đang đo)
  giả thuyết : t54 chỉ đo các kịch bản có sẵn; đầu vào lỗi khác còn sống qua 56 ca.
  lệnh       : python evidence/env.py python -u evidence/main_mutants.py
  output     : TOTAL_MUTATIONS 39; config_ignore {'qua': 56}; skip_prechecks/skip_ca/shard_never/
               shard_k/shard_n/shard_ra/partition/ignore_base_red đều giết đúng t54, 1/56.
  kết luận   : LỖI (P2) sơ bộ F7, cùng lớp F2/F5/F6: main nuốt cấu hình sai vẫn qua mọi ca.
               Chờ đo xong toàn bảng để chốt phạm vi. Cặp neo/thay và đủ 56 trạng thái: evidence/main-*.json.

HƯỚNG 5: MỚI — CLI --gop có thực truyền phán quyết thành mã thoát?
  giả thuyết : t52 gọi _gom_manh trực tiếp; dây nối _main_gop và mã thoát không được ca nào canh.
  lệnh       : python evidence/env.py python -u evidence/extra_mutants.py;
               python evidence/env.py python -u evidence/wiring.py
  output     : gop_exit {'qua': 56}; gop_skip {'qua': 56}; gop_fingerprint {'qua': 56}.
               CLI thật với thư mục rỗng: control rc=1 [G-rong]; gop_exit rc=0 [G-rong];
               gop_skip rc=0, stdout='GOM MẢNH 8/8'.
  kết luận   : LỖI (P2), F8: thiếu răng M3/M4 tại CLI. Mã gốc hiện tại từ chối bộ rỗng đúng;
               đây là đột biến sống, không phải khẳng định bộ rỗng đang được head gốc nhận xanh.
               Cặp neo/thay và đủ 56 trạng thái: evidence/extra-gop_*.json; hậu quả: evidence/wiring.log.

HƯỚNG 6: MỚI — nguồn vân tay thật, ngoài các vân tay giả của t52/t54
  giả thuyết : Các ca kiểm so sánh và chuyển tiếp vân tay nhưng không kiểm nguồn hash/HEAD thật.
  lệnh       : python evidence/env.py python -u evidence/extra_mutants.py;
               python evidence/env.py python -u evidence/wiring.py
  output     : fingerprint_constant {'qua': 56}; fingerprint_head_constant {'qua': 56}.
               Sửa nội dung tệp test dưới cùng HEAD: control hash_changed=True, head_matches=True;
               constant hash: hash_changed=False; constant HEAD: head_matches=False.
  kết luận   : LỖI (P2), F9: chốt nhận diện mã đo thiếu răng. Cả writer và gom có thể cùng nhận hằng số,
               nên các phép so sánh của t52 vẫn xanh dù mất ràng buộc với nội dung/HEAD thực.
               Mã gốc hiện tại tính vân tay đúng trong đối chứng. evidence/extra-fingerprint_*.json, wiring.log.

HƯỚNG 7: Gom bản ghi sai và phân hoạch ở các biên N
  giả thuyết : Gom chỉ so tập tên mà bỏ bán kính/trạng thái của bản ghi, hoặc phân hoạch lệch ở N khác 8.
  lệnh       : python evidence/env.py python -u evidence/gather_probe.py
  output     : control GOM MẢNH 8/8, 254 đột biến, lỗi=0;
               missing_case/extra_case/no_kill/extra_kill/fake_credit/skip_target/unknown_state/
               bad_reason/wrong_target/child_error_record: 10/10 lỗi=1.
               N=2/3/8/16 đều total=254, unique=254; N=8: [32,32,32,32,32,32,31,31].
  kết luận   : KHÔNG PHẢI LỖI trên đầu vào đã đo. Bộ control là BKCON TỔNG HỢP để đo gom, không phải A1
               đã thực đo 254 đột biến. Dòng đầu GOM MẢNH cũng xuất hiện ở một số bộ đỏ; phán quyết còn
               phải đọc số lỗi/mã thoát. evidence/gather-probe.log.

HƯỚNG 8: MỚI — tiền xử lý biểu thức GitHub trước khi Bash đọc chú thích (CHỈ MÔ TẢ BẰNG LỜI)
  giả thuyết : _dong_lenh và lexer Ruff bỏ chú thích thô, nhưng GitHub thay biểu thức trước khi shell chạy.
  lệnh       : Đọc .claude/dev/ci_dang_ky_test.py:213–274, :1092, :1137–1163 và tài liệu GitHub;
               KHÔNG soạn/chạy payload theo phân công lượt 4.
  output     : _dong_lenh bỏ mọi dòng bắt đầu bằng # sau space/tab; _dong_logic cũng nhảy tới LF khi gặp #.
               Không chốt nào ở hai đường ấy kiểm nội dung chú thích trước khi bỏ nó.
  kết luận   : LỖI (P1), F10, phản chứng BẰNG LỜI theo quyền người dùng cấp:
               Trong run của bước G5 gom, thêm MỘT dòng chú thích trước lệnh gom ghim. Trong chú thích đặt
               biểu thức GitHub gọi fromJSON với một JSON string hằng; chuỗi JSON biểu diễn U+000A,
               tiếp theo lệnh thoát Bash thành công, rồi U+000A. Tệp workflow chỉ chứa dạng escape in được
               của JSON, chưa có LF bên trong chuỗi. Sau GitHub giải biểu thức, LF đầu kết thúc chú thích,
               lệnh thoát trở thành dòng Bash độc lập, nên shell trả 0 trước khi chạy gom. Bộ mảnh sai
               không được kiểm. Không cần đầu vào PR do bên ngoài điều khiển: dùng hằng cũng đủ.
               Validator đọc bản YAML TRƯỚC giải biểu thức: bỏ cả dòng chú thích và chỉ thấy đúng lệnh gom,
               env/shell/needs/artifact/matrix vẫn nguyên. Lexer Ruff cũng bỏ cả dòng ấy; pin vùng registry
               không bao trùm run G5 gom. Đây là suy luận từ mã và ngữ nghĩa được tài liệu xác nhận;
               không khai actionlint hay runner đã chạy phản chứng này. Executor cần viết ca và chạy lại
               actionlint/registry, thêm chốt biểu thức trên TOÀN run trước thao tác bỏ chú thích.
               Nguồn: [GitHub — Script injections](https://docs.github.com/en/actions/concepts/security/script-injections)
               (biểu thức được giải và thay vào script trước khi shell chạy);
               [GitHub — fromJSON](https://docs.github.com/en/actions/reference/workflows-and-actions/expressions#fromjson)
               (fromJSON trả kiểu dữ liệu JSON, gồm string). Không đính chuỗi payload.

HƯỚNG 9: Đối chiếu chú thích đếm phiên bản actionlint
  giả thuyết : Thêm chỗ AL_VER thứ năm nhưng còn chú thích đếm bốn.
  lệnh       : python evidence/env.py python evidence/comment_count.py
  output     : base AL_VER=4, head AL_VER=5; cả hai còn cùng chú thích 't152 đếm 4 dòng'.
  kết luận   : LỖI (P3), F11, .github/workflows/ci.yml:543. Chú thích sai do thay đổi này làm tổng số tăng;
               t152 và hook đã đổi đúng, không ảnh hưởng thực thi. evidence/comment-count.log.

  Bổ sung HƯỚNG 3: lease_publish t24/t31/t35/t161/t162 PASS ở cả head và baseline.
               Lệnh: python evidence/env.py python -u evidence/lease_subset.py; log evidence/lease-subset.log.
               Dòng KHÔNG ĐO ĐƯỢC trong t162 là đối chứng parser ngoài miền được ca chủ động thử, không phải skip.
               Không đo được Ruff đúng pin 0.15.15: pip bị DNS/network chặn, evidence/ruff-install.log.
               Chỉ xác nhận delta F=0 với Ruff 0.15.8, không nhận lời khai 0.15.15 của lượt trước.

HƯỚNG 10: Bán kính chính thức và lỗi cô lập phép đo reviewer
  giả thuyết : 42 đột biến mới đều bán kính 1/56; mẫu cũ không tăng bán kính do t52/t53/t54.
  lệnh       : python evidence/env.py python -u evidence/radii.py new;
               python evidence/env.py python -u evidence/radii.py old
  output     : new TOTAL 42 ERRORS 1 SECONDS 631.8; old TOTAL 9 ERRORS 0 SECONDS 177.8.
               Lỗi duy nhất: f6_main_bo_tien_kiem vẫn giết đúng t54, nhưng t16 nhận FileNotFoundError
               ở /tmp/review668-r4/.claude/dev/review_ablation_append_1.py (tin_dung_gia).
  kết luận   : KHÔNG PHẢI LỖI sản phẩm ở lỗi trên: reviewer đặt bản sao ablation tạm vào cùng cây đo rồi
               xoá trong lúc t16 quét cây, gây race. Giữ nguyên log thất bại evidence/radii-new.log/json;
               đã sửa harness ablation dùng cây RIÊNG để tái lập không tái diễn; đang đo lại riêng mutant
               bị nhiễu bằng evidence/retry_radius.py. Không tính lượt nhiễu đó là 42/42 xanh.
               9 mẫu cũ đều 1/56; gồm 5 bn_* nhắm TEP_TEST và t1_rc_gop, t6_day_g5_sau_py_compile,
               t13_mat_requiredness_khi_tool_bien_mat, t21_git_regex_cat_hau_to. Không suy thành đã đo 212 cũ.

  Chốt HƯỚNG 10: `python evidence/env.py python -u evidence/retry_radius.py` rc=0;
               f6_main_bo_tien_kiem → giết đúng t54 · bán kính 1/56 · ERRORS 0.
               `python evidence/summarize.py`: 42/42 bản ghi đã xác minh độc lập, 2.310 qua + 42 giet_that,
               không bo_qua/tin_dung_gia. 41 phép đo sạch ban đầu + 1 phép đo lại; KHÔNG gọi lượt đầu rc=1 là pass.
               Cả 12 f2_*/f5_*/f6_* giết đúng t54. evidence/radii-new-corrected.json và radius-f6-retry.log.
               Mẫu cũ: qua=484, giet_that=9, bo_qua=11; cả 27 trạng thái t52/t53/t54 đều qua.
               11 bỏ qua ở ca cũ giữ nguyên lý do trong radii-old.json; không tính bỏ qua là đo được.

  Chốt HƯỚNG 4 — F7 (P2), chưa đóng lớp main:
               48 đột biến riêng đã chạy trọn 56 CA: 29 chết đúng t54 (1/56), 19 sống (56/56 qua).
               Lệnh bổ sung: python evidence/env.py python -u evidence/main_more.py.
               Đủ bảng từng tên: evidence/main-matrix.md; cặp neo/thay + trạng thái: evidence/main-<tên>.json.
               Bốn hậu quả bằng main thật với CA/transport giả có chủ đích, writer THẬT:
               • cấu hình sai: control rc=2; config_ignore rc=0;
               • con trả đủ BKCON nhưng rc=1: control rc=1, không tệp; receiver_rc rc=0, ghi tệp mảnh 32/32;
               • bán kính đủ trả lỗi: control rc=1; full_errors rc=0;
               • cổng cây thật trả lỗi: control rc=1; final_loi_cong rc=0 dù in cổng HỎNG.
               Đây là kiểm dây nối, không phải 32 đột biến của mảnh ấy đã đo thật. evidence/wiring.log.
               Root cause của receiver_rc: con_hong trong t54 vừa rc=1 VỪA stdout rỗng; khi ép rc=0,
               thiếu bản ghi vẫn làm đỏ, nên ca không phân biệt được dây rc bị cắt.

Bảng liệt kê quyết định/tham số của `main()` và phép đột biến (các nhánh nghiệp vụ; chuỗi trình bày không tính là chốt):

| Quyết định hoặc dữ liệu main truyền | Đột biến độc lập đã chạy | Kết quả |
|---|---|---|
| Đọc env; dừng cấu hình sai trước CA | config_ignore | Sống 56/56 — F7 |
| Tiền kiểm batch và alias, lấy kết quả bỏ qua | skip_prechecks; precheck_batch_only; precheck_alias_only | Bỏ cả hai chết t54; bỏ riêng một sống — F7 |
| Chạy đủ CA, tập ca đỏ làm căn cứ nhánh mảnh | skip_ca; ignore_base_red | Đều chết t54 |
| Chọn nhánh mảnh | shard_never | Chết t54 |
| k, N, đường ra lấy từ tham_so | shard_k; shard_n; shard_ra | Đều chết t54 |
| Phân hoạch theo k/N | partition; f2_main_manh_do_ca_bang chính thức | Đều chết t54 |
| Nền đỏ HOẶC tiền kiểm không khả dụng; dọn tệp cũ; trả lỗi | ignore_base_red; ignore_precheck; no_cleanup; bad_base_rc | Đều chết t54 |
| Vân tay trao cho writer ở nhánh nền đỏ | cleanup_fingerprint | Chết t54 |
| Phóng con: tập tên, nền rỗng, số worker | launch_empty; launch_baseline; launch_workers | Đều chết t54 |
| Bộ nhận: nhóm, rc, stdout, nền rỗng | receiver_group; receiver_rc; receiver_output; receiver_baseline | Chỉ receiver_rc sống — F7 |
| Nhận thất bại: ket=None, lý do, dừng vòng | f5_main_bo_loi_con; no_reason; no_break | Hai phép đầu chết; đổi break thành continue sống (*) |
| Hợp kết quả của mọi nhóm, giữ cả tên và giá trị | f5_main_bo_nhan; no_values; drop_group | Đều chết t54 |
| Gọi writer; truyền k/N/ra/tên/ket/lý do/vân tay | f5_main_bo_ghi; writer_k_arg; writer_n_arg; writer_ra_arg; writer_ten; no_values; no_reason; no_fingerprint | Đều chết t54 |
| Truyền lỗi writer thành mã thoát mảnh | writer_rc; f5_main_bo_truyen_loi | Đều chết t54 |
| Nhánh đủ/gate: gọi cổng thật với GOC | skip_gate; gate_root | Sống — F7; cửa t45 kiểm helper, không bắt dây gọi main |
| Gọi tự kiểm phân hạng, giàn giáo, song song | skip_classifier; skip_scaffold; skip_parallel | Sống — F7 |
| Truyền tập nền đỏ cho báo cáo/tự kiểm/bán kính | full_baseline; parallel_base_arg; full_base_arg | Sống — F7; kịch bản du/gate của t54 chỉ có nền xanh |
| Cộng lỗi báo cáo nền | full_base_errors | Sống; đường return còn hong, chưa chứng minh xanh sai riêng mutant này (*) |
| Gate bỏ vòng; đủ đo mọi tên + số worker | f2_main_gate_van_do; full_names; full_workers | Đều chết t54 |
| Cộng lỗi kết quả bán kính đủ | full_errors | Sống — F7; hậu quả rc=0 đã đo |
| Mã thoát cuối dựa hong/loi_db/tien_kiem_bo_qua/loi_cong | final_hong; final_loi_db; final_tien_kiem_bo_qua; final_loi_cong | Cả bốn sống; final_hong còn rào loi_nen (*) |

(*) Không đồng nhất một mutant sống với một đường xanh sai: `final_hong` còn lỗi nền trong loi_db,
`full_base_errors` còn hong, còn `no_break` có thể đi tiếp rồi lỗi khi cập nhật ket=None. Ghi đủ 19 survivor theo
nhiệm vụ, nhưng không dùng ba phép này để tự nâng severity. Các survivor còn lại được gộp vào F7 thay vì tạo hàng
chục finding cùng gốc. Bản vá F6 có hiệu quả thực với giá trị/vân tay/tiền kiểm mảnh và worker; chưa phủ mọi dây nối.

  Bổ sung HƯỚNG 8: [mã actionlint v1.7.7, rule_shellcheck.go](https://raw.githubusercontent.com/rhysd/actionlint/v1.7.7/rule_shellcheck.go)
               dòng 119–149 và 162 thay biểu thức bằng dấu gạch dưới trước ShellCheck. Vì vậy kiểm Bash của
               actionlint không phải phép chạy từ vựng sau GitHub nội suy. Căn cứ bổ sung bằng đọc mã nguồn,
               không đổi lời khai rằng phản chứng F10 CHỈ mô tả và chưa chạy payload/actionlint với payload.

Thông tin phiên, đối chiếu và giới hạn:

- Ngưỡng áp dụng: 0 P1/P2/P3 theo prompt; head/tree giữ nguyên:
  `971e14c1550bcbc3d1523791f8174f78a45edbf9` / `95f427bdfe648810193572f8fbc375afe28759f7`.
  Baseline `f8a7829cc44f296c25faf1a6439b603ba840f70b`; spec/hash đã khớp ở HƯỚNG 1.
- 5 tệp, +946/−29; trong trần ~1.100 người dùng cấp. Không lấy trần ~600 trong spec cũ làm finding.
- Reviewer OpenAI Codex, họ GPT-6 theo cấu hình phiên; execution_surface=codex_service qua API/công cụ terminal,
  transport=machine/local. Không có chứng cứ runtime độc lập cho model ID/effort; không tự khai Codex CLI hay
  gpt-6-astra đã được đo. Không tạo human_audited/authorization land.
- Linux/Python 3.11.15; git config core.abbrev=7, identity tạm qua env; PYTHONDONTWRITEBYTECODE=1;
  actionlint=1.7.7; Ruff đã chạy=0.15.8. Không đo được Ruff 0.15.15 do DNS bị chặn.
- Không chạy GitHub CI, không sửa/commit/push mã sản phẩm, không đăng GitHub. Mọi thực thi bộ ca, hook t152,
  đột biến và dữ liệu giả nằm trong /tmp. Checkout `cay-kho` status tracked/ignored cuối đều rỗng;
  evidence/integrity.json. Hook của phép đo chỉ để lại trạng thái ignored trong BẢN SAO /tmp.
- Chưa chạy 8 mảnh THẬT đủ 254 đột biến + gom, CLI mặc định đủ 254, Windows/runner Actions,
  upload/download thực, ruleset hoặc A9. Không nhận A1 ở SHA c8f52b6 làm A1 của head này.
- F10 dùng quyền phản chứng bằng lời người dùng cấp, có đối chiếu mã và nguồn sơ cấp. Không nói đã chạy
  phản chứng đó. Các phản chứng F1/F3 cũ đã chạy nguyên từ cây và đo răng bằng ablation.

Bảng lớp finding:

| Slug lớp | Lịch sử và biểu hiện còn mở | Mức cao nhất | Cách đóng lớp |
|---|---|---|---|
| g5-shell-bo-qua-thuc-thi | F1 → F3 → F10: Bash shell và splitlines đã vá; lớp tiền xử lý biểu thức còn hở | P1 | Kiểm toàn bộ run trước bỏ chú thích; ca biểu thức sinh LF theo mô tả, control chuẩn xanh, ablation giết đúng chốt |
| g5-main-thieu-ca-chon-vong-ban-kinh | F2 → F5 → F6 → F7: truyền rc của con, cấu hình sai và lỗi đủ/gate chưa được kích thích độc lập | P2 | Liệt kê lời gọi/đầu vào/đầu ra main; kịch bản mỗi lỗi độc lập, có rc con khác 0 với stdout vẫn đủ; giữ bán kính 1 |
| g5-gom-cli-thieu-rang | F8: helper đúng nhưng CLI có thể bỏ gom hoặc nuốt lỗi mà cả CA không phát hiện | P2 | Ca qua CLI thật với bộ đạt/bộ sai; riêng chốt gọi gom, vân tay trao vào, mã thoát |
| g5-nguon-van-tay-thieu-rang | F9: hash/HEAD hằng sống; giàn giáo dùng vân tay giả nên không đo nguồn | P2 | Đổi nội dung giữ HEAD và đổi HEAD giữ nội dung trên cây tạm, đo vân tay thật; mutant riêng từng nguồn |
| g5-chu-thich-dem-cu | F11: t152 đã đòi 5 nhưng workflow vẫn chú thích 4 | P3 | Cập nhật chú thích theo số thực hoặc tránh ghim số dễ trôi |

| F<n> | mức | tệp:dòng | mô tả | phản chứng |
|---|---|---|---|---|
| F7 | P2 | ops/cong_cu_test.py:7122, :7143, :7206, :7244, :7294 | t54 chưa phủ mọi dây main. rc con bị ép 0 vẫn sống do ca con_hong đồng thời làm rỗng stdout; các lỗi đủ/gate và invalid config cũng chưa được kích thích độc lập | main_mutants.py + main_more.py: 19/48 sống, mỗi survivor 56/56 qua; wiring.py đo control đỏ/mutant xanh |
| F8 | P2 | ops/cong_cu_test.py:6981, :6987, :6990 | CLI --gop không được selftest gác: bỏ gọi gom, truyền vân tay sai, hoặc nuốt lỗi đều sống | extra-gop_*.json: 3×56/56 qua; CLI thư mục rỗng control=1, hai mutant=0 |
| F9 | P2 | ops/cong_cu_test.py:6867, :6876 | Nguồn sha256_test/HEAD thật không có răng; so sánh vân tay giả không chứng minh vân tay bám mã đang đo | extra-fingerprint_*.json: 2×56/56 qua; wiring.log: hash không đổi khi byte đổi, HEAD không khớp git |
| F10 | P1 | .claude/dev/ci_dang_ky_test.py:1092, :1149 | Bỏ chú thích trước khi xét biểu thức GitHub; fromJSON có thể sinh LF và lệnh thoát thành công trước gom | HƯỚNG 8: phản chứng BẰNG LỜI được user cho phép, nguồn GitHub + mã lexer/actionlint; không tạo/chạy payload |
| F11 | P3 | .github/workflows/ci.yml:543 | Chú thích nói t152 đếm 4 AL_VER, thực tế và t152 đã thành 5 | comment_count.py: base=4/head=5, chú thích giữ 4 |

ĐỐI CHIẾU LƯỢT TRƯỚC — phân biệt vá biểu hiện và đóng lớp:

| Finding trước | Trạng thái lớp | Đối chiếu đã tự đo |
|---|---|---|
| F1 | chưa đóng | ĐÃ VÁ THẬT shell syntax-only/keys/env/with; 20 ca F1 xanh đúng, ablation các nhánh làm lọt. F10 còn trong cùng lớp thực thi workflow |
| F3 | chưa đóng | ĐÃ VÁ THẬT splitlines: 28 ca F3 đỏ đúng, trả splitlines làm 27 lọt. F10 là tầng nội suy trước Bash, chưa được chốt |
| F2 | chưa đóng | ĐÃ VÁ THẬT chọn du/gate/mảnh: 3 f2_* đều 1/56 t54; F7 còn dây lỗi ở main |
| F5 | chưa đóng | ĐÃ VÁ THẬT nhận/ghi/truyền lỗi được gọi tên: 5 f5_* đều 1/56 t54; rc đầu vào receiver còn hở theo F7 |
| F6 | chưa đóng | ĐÃ VÁ THẬT giá trị ket, vân tay trao writer, tiền kiểm mảnh và số worker: 4 f6_* đều 1/56 t54; chưa đóng toàn lớp main (F7). F9 tách riêng nguồn tạo vân tay, không phủ nhận phép chuyển tiếp đã vá |

verdict: changes_requested
reviewed_sha: 971e14c1550bcbc3d1523791f8174f78a45edbf9
