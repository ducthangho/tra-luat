verdict: dang_review
reviewed_sha: c8f52b6c89fcc62ed63b6e358892d7bbaf5be73b

Mọi phép đo ứng viên dùng SHA trên, trừ khi ghi rõ bản sao đột biến hoặc baseline.

HƯỚNG 1: Workflow — ngữ nghĩa thực thi ngoài câu lệnh G5
  giả thuyết : Đổi shell của bước gom khiến --gop không chạy nhưng validator vẫn xanh.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python3 evidence/workflow_probe.py
  output     : original []; gop.shell.syntax-only []; actionlint_mutated_rc 0.
               Cùng script `python ops/cong_cu_test.py --gop manh`, thư mục manh vắng:
               bash --noprofile --norc -e -o pipefail {0}: rc=1, [G-thu-muc].
               bash -n {0}: rc=0, stdout='', stderr=''.
  kết luận   : LỖI (P1), F1. `loi_g5_workflow` không ràng buộc shell nên có bước gom xanh mà chưa kiểm mảnh nào.
               Bản sao /tmp/rv668-copy từ SHA ứng viên; workflow phản chứng lưu evidence/workflow-shell.yml.
               Đo tại chỗ, không chạy GitHub Actions. Shell syntax-only là cấu hình hợp lệ qua actionlint.
               Các đối chứng include/exclude, continue-on-error cấp job, if upload/download đều bị bắt.
               Env kế thừa, runs-on, working-directory và giá trị matrix.os lọt validator; chưa suy tất cả thành fail-open.

HƯỚNG 2: Gom — định dạng, tập mảnh, vân tay và trạng thái bản ghi
  giả thuyết : Bộ thiếu/sai vẫn có thể được --gop nhận xanh.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python3 evidence/aggregate_probe.py
  output     : valid_synthetic rc=0, GOM MẢNH 8/8, ca=55, đột biến=242, lỗi đột biến=0.
               missing rc=1 [G-tap]; duplicate/hidden_extra rc=1 [G-dem]; head/hash rc=1 [G-van-tay];
               bool rc=1 [G-dau]; huge rc=1 [G-tap]; n_fake rc=1 [G-so-manh]; all_n_fake rc=1 [G-tap];
               BOM rc=1 [G-dau]; record_missing/target_wrong rc=1 [G-ban-ghi];
               target_survives/target_fake_credit/target_skipped rc=1, lỗi đột biến=1.
               renamed/CRLF/blank_LF rc=0; blank_CRLF rc=1 [G-dong-la]; all_n_2 rc=0, đủ 242.
  kết luận   : KHÔNG PHẢI LỖI trong các đầu vào đã thử. Tên tệp không thuộc hợp đồng danh tính; N=2 vẫn phủ đủ 242.
               Bộ dựng dùng _ket_thuc_manh + _ban_ghi_du_gia, KHÔNG phải bằng chứng 242 đột biến đã chạy.
               Gom xác minh cấu trúc dữ liệu đo, không xác thực nguồn gốc chống người cố ý chế bản ghi.
               Không dựng đường dẫn thoát cây hoặc nội dung nhạy cảm. Log đầy đủ: evidence/aggregate.log.

HƯỚNG 3: Vân tay và đa nền — LF/CRLF, checkout, không Git
  giả thuyết : Cùng run nhưng Windows băm khác Linux do autocrlf; thiếu Git lại được gom nhận.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python3 evidence/platform_probe.py
  output     : check-attr: text=auto, eol=lf; bytes_LF=7259, CRLF=0.
               git cat-file --filters với core.autocrlf=false/true: rc=0, cùng sha256
               1aeac8e21fbdaf81657163c8320037ecf8738a33135fe8d3a020f5d43efe1ac1.
               without_git: head=None. Bản sao đổi CRLF: băm b7d9242a… khác bản LF.
               Cả gate/mảnh/gom đều Force LF trước checkout; checkout không ghi đè ref.
  kết luận   : KHÔNG PHẢI LỖI qua phép đo byte/filter tại chỗ. CRLF tự tạo gây lệch băm đúng thiết kế;
               các chốt G-head/M-head không chấp nhận thiếu HEAD. Chưa chạy trên runner Windows/PR thật.
               Không khẳng định đã đo GitHub merge-ref; chỉ đọc cùng cấu hình checkout trong ba job.

HƯỚNG 4: Tương thích các bộ khác và delta baseline
  giả thuyết : Thêm hai job làm lệch registry, AL_VER hoặc quy ước workflow.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 python3 evidence/compat_probe.py
               PYTHONDONTWRITEBYTECODE=1 python3 <root>/.claude/dev/launcher_test.py --lap-ca t152_hook_cai_dat_va_khop_al_ver_ci --lan 1
               <root> = cay-kho (c8f52b6…) và /tmp/rv668-base (f8a7829…).
  output     : actionlint rc=0 cả hai; ruff --select F rc=1 cả hai, cùng 6 F841 (5 launcher + 1 cong_cu), delta=0.
               t24/t31/t35/t161/t162 PASS cả hai; t152 1/1 qua, 0 bỏ qua, 0 hỏng, rc=0 cả hai.
               Registry lần đầu rc=1 cả hai do git commit fixture bị cấu hình commit.gpgsign=true của sandbox.
  kết luận   : KHÔNG PHẢI LỖI trên các phép đo đã hoàn tất; registry đang đo lại với môi trường Git đã sửa.
               Không sửa cấu hình cay-kho; evidence/with_git_env.py chỉ thêm commit.gpgsign=false, core.abbrev=7 vào env tiến trình.
  bổ sung đo lại HƯỚNG 4: `python3 evidence/with_git_env.py python3 <root>/.claude/dev/ci_dang_ky_test.py`
               head: PHẢN CHỨNG 965/965 đỏ đúng; TỔNG ĐẠT; rc=0.
               base: PHẢN CHỨNG 938/938 đỏ đúng; TỔNG ĐẠT; rc=0.
               Log: evidence/registry-{head,base}-fixed.log. Lỗi ký commit ban đầu là môi trường, không tính finding.

HƯỚNG 5: Chốt M1/M4 ở main — đột biến ngoài danh sách có sống sót?
  giả thuyết : Các ca chỉ kiểm _doc_che_do, không kiểm rằng main thực sự đo bán kính khi vắng biến mới.
  lệnh       : python3 evidence/with_git_env.py python3 -u evidence/missing_guard_probe.py
  output     : MUTATION review668_default_skips_radius; states {'qua': 55}; TARGET ('qua', None).
               _ket_luan_ban_kinh: đích t53 vẫn XANH ⇒ đột biến không giết được gì; 1 lỗi.
               SECONDS 34.7; rc=0 của script đo (script đã phát hiện mutant sống, không có nghĩa mutant bị giết).
  kết luận   : LỖI (P2), F2. Trên bản sao thay duy nhất `if che_do == "gate":` bằng
               `if che_do in ("gate", "du"):`. Toàn bộ CA vẫn qua; đây là bỏ đo ở hành vi mặc định,
               không phải rig hỏng hoặc ca bị bỏ qua. M4 yêu cầu mỗi chốt M1–M3 có ca + đột biến riêng.
               Đang chạy thêm CLI mặc định của bản sao đột biến để xác nhận ảnh hưởng đầu-cuối.

HƯỚNG 6: Tệp cũ khi mảnh đỏ và cấu hình bị từ chối sớm
  giả thuyết : Mảnh thất bại có thể để lại kết quả lần trước.
  lệnh       : python3 evidence/with_git_env.py python3 evidence/stale_probe.py
  output     : MANH=8/8: rc=2 [C-pham-vi], old_file_unchanged=True.
               MANH=0/8 + BAN_KINH=manh: rc=2 [C-ca-hai], old_file_unchanged=True.
               Tiêm một CA nền đỏ, giữ nguyên main/cleanup: rc=1 [M-nen], output_exists=False.
  kết luận   : KHÔNG PHẢI LỖI fail-open đã chứng minh. Nhánh mảnh nền đỏ xoá tệp cũ đúng.
               Giới hạn: nhánh cấu hình sai trả sớm giữ tệp cũ. Workflow hiện tại không upload sau lỗi bước G5;
               M2 chỉ ghi rõ xoá/không ghi ở mảnh đã vào chạy CA. Không nâng quan sát này thành P1/P2.
               Phép đo nền đỏ dùng rig rút CA còn một ca và bỏ tiền kiểm, không khai là chạy mảnh thật.

Thông tin phiên/preflight:
- Reviewer: OpenAI Codex, họ GPT-6 theo cấu hình phiên; không có phép đo độc lập model ID/effort.
- Execution: công cụ terminal trong sandbox API; transport local tool execution, không đăng GitHub.
- Review class sensitive; ngưỡng áp dụng theo yêu cầu người dùng: không còn P1/P2/P3.
- SHA ứng viên đã xác nhận c8f52b6c89fcc62ed63b6e358892d7bbaf5be73b; tree 8e449d5d62e4d80147cb074280c157c89025e751.
- Baseline f8a7829cc44f296c25faf1a6439b603ba840f70b; SPEC sha256 khớp dd2ada1b8511bec1c6c30ffdd7a94a3c34f4024836761878caf73ce339516b15.
- Diff đo lại: đúng 5 tệp, +728/-28; áp trần ~800 được user xác nhận trong prompt, không dùng trần 600 cũ làm finding.
- Linux, Python 3.11.15 (workflow ghim 3.12), actionlint 1.7.7, Ruff 0.15.8. Ruff delta dùng cùng bản cho hai SHA;
  không khai đã đo bare lint bằng Ruff 0.15.15 ghim trên CI.
- Cây cay-kho giữ nguyên; mọi đột biến nguồn/workflow nằm trong /tmp hoặc cây tạm do harness tạo.
  Sandbox cho phép ghi workspace, không phải cơ chế mount read-only. Snapshot Git sạch chỉ xác nhận delta quan sát được.

HƯỚNG 7: 30 g668_* — kiểm đúng lý do, không lấy tổng số giết làm bằng chứng
  giả thuyết : Mutant được ghi giết nhưng control hỏng/rig hỏng; chốt G-tong bị bỏ quên.
  lệnh       : python3 evidence/with_git_env.py python3 -u evidence/mutant_scenarios.py
               python3 evidence/summarize_scenarios.py
               PYTHONDONTWRITEBYTECODE=1 python3 -u evidence/run_mutants.py (đang chạy bán kính toàn CA, 2 tiến trình).
  output     : TOTAL 30 nonzero_child_rc 0 unchanged 0 (cửa tự kiểm trên từng tệp đột biến).
               bo_thu_muc: khong_co G-thu-muc→G-rong; bo_rong: rong G-rong→G-so-manh;
               bo_head: head_gom_none G-head→G-van-tay; bo_tep_thuong: tep_la G-tep→G-dau;
               bo_tap: thieu/trung G-tap→G-dem; tin_ten_cua_manh: chuyen→rc0, xoa G-ban-ghi→G-tong;
               bo_con: ghi_con M-con→M-loi; bo_xoa_cu: ghi_loi/ghi_con/ghi_head giữ đúng thẻ nhưng còn tệp;
               các chốt kiểu/khoá/phiên bản/vân tay/dòng/số mảnh/N/đếm đều có ca riêng chuyển từ đỏ sang xanh;
               9 chốt C-* đổi đúng kịch bản tương ứng sang nhận cấu hình sai.
               phan_manh_chong: control dung chuyển GOM MẢNH 3/3→G-phan-hoach, đúng thuộc tính phân hoạch.
  kết luận   : KHÔNG PHẢI LỖI tín dụng giả ở kiểm kịch bản. Chi tiết đủ 30 tên: evidence/mutant-scenario-summary.log;
               log thô giữ nguyên cả đường dẫn tạm: evidence/mutant-scenarios.log.
               G-tong đúng là dự phòng trên mã nguyên bản: _nhan_ket_qua_con đòi tập tên của mỗi nhóm bằng phan[k];
               G-phan-hoach đòi tổng kích thước và hợp của các nhóm bằng DOT_BIEN ⇒ ket có đúng tập DOT_BIEN.
               Đã tới G-tong khi gỡ kiểm phân hoạch bản ghi (tin_ten_cua_manh + xoa), phù hợp lời khai dự phòng.
               Không dùng lập luận G-tong để miễn các chốt main thiếu độ phủ ở F2.

HƯỚNG 8: Chế độ gate trọn vẹn và N126 sau tách _phong_con
  giả thuyết : Tách đường phóng con làm gate hoặc tự kiểm song song sai.
  lệnh       : CONG_CU_TEST_TIEN_TRINH=2 CONG_CU_TEST_BAN_KINH=manh python3 evidence/with_git_env.py python3 -u cay-kho/ops/cong_cu_test.py
  output     : cong_cu_test: 55/55 đạt; tổng=55, bỏ qua=0, tiền kiểm bỏ qua=0.
               CỔNG TRÊN CÂY THẬT: ĐẠT · nguon_tep=git · nguon_noi_dung=blob-index.
               TỰ KIỂM SONG SONG (N126): ĐẠT.
               BÁN KÍNH ĐỘT BIẾN (242 đột biến): GIAO cho job gate-cong-cu + gate-cong-cu-gop.
               SỐ LIỆU: ca=55 · đột biến=242 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT; rc=0.
  kết luận   : KHÔNG PHẢI LỖI qua phép đo gate/N126; log evidence/gate-fixed.log.
               N126 vẫn đo 3 đột biến thật cả tuần tự và song song cùng các ca vận chuyển giả, đối chiếu nội dung/thứ tự.
               A4 viết “không phóng tiến trình con bán kính nào” rộng hơn M1 giữ nguyên tự kiểm: gate vẫn phóng con ở N126.
               Hiểu hợp đồng nhất quán là không phóng vòng ĐẦY ĐỦ 242 đột biến. Không tính tự kiểm được giữ theo M1 là finding.
               Chưa chạy CLI mặc định nguyên bản hết 242 đột biến/A5; không suy full-pass từ N126.
  bổ sung HƯỚNG 5 (CLI thực, bản sao đột biến):
               `CONG_CU_TEST_TIEN_TRINH=2 python3 evidence/with_git_env.py python3 -u /tmp/rv668-copy/ops/cong_cu_test.py`
               Vắng mọi biến chế độ: 55/55, N126 ĐẠT, thông báo GIAO bán kính, SỐ LIỆU đột biến=242 lỗi=0, rc=0.
               Không chạy vòng đầy đủ; log evidence/default-mutated.log. Đã hoàn nguyên bản sao sau phép đo.
               F2 là thiếu răng test được chứng minh bằng mutant; không nói code ứng viên hiện đang bỏ vòng mặc định.
  bổ sung HƯỚNG 1 (thư mục tồn tại, có đúng 1/8 mảnh hợp lệ do writer dựng):
               Cùng lệnh --gop manh: shell bash chuẩn rc=1 [G-tap] tập mảnh [0] ≠ 0..7;
               shell bash -n {0} rc=0, stdout/stderr rỗng. Trường hợp này mô hình hoá download đã có artifact,
               nên không cần giả định download-artifact thành công khi không tìm thấy bất kỳ artifact nào.
  bổ sung hoàn tất HƯỚNG 7 (bán kính toàn CA qua _ban_kinh_moi_dot_bien):
               TOTAL 30 ERRORS 0 SECONDS 672.7; rc=0.
               30 bản ghi, mỗi bản ghi đúng 1 giet_that ở ca đích, tổng tin_dung_gia=0.
               Mọi dòng ok có bán kính 1/55; lý do từng ca đích lưu evidence/mutants-records.json và evidence/mutants.log.
               Giới hạn môi trường của lượt này: t47 bo_qua ở cả 30 bản ghi do ký commit fixture; t52/t53 đích đều chạy.
               Không giấu skipped, không khai lượt này 55 ca đều đã đo. Kiểm kịch bản riêng đã dùng env Git sửa.

HƯỚNG 9: Mảnh 0/8 thật — thiếu năng lực đo có bị xanh nhầm?
  giả thuyết : Ca bị bỏ qua ở nền khiến mảnh vẫn ghi artifact xanh.
  lệnh       : PYTHONDONTWRITEBYTECODE=1 CONG_CU_TEST_TIEN_TRINH=2 CONG_CU_TEST_MANH=0/8 CONG_CU_TEST_MANH_RA=/tmp/rv668-real/m-0.txt python3 -u ops/cong_cu_test.py
               (cwd=cay-kho, SHA ứng viên; lần đầu giữ cấu hình Git sandbox).
  output     : Nền 54/54, tổng=55, bỏ qua=1; MẢNH 0/8 (31/242 đột biến; 2 tiến trình).
               KHÔNG_ĐO_ĐƯỢC bn_giai_ma_hong_thanh_traceback: đích t47… bị BỎ QUA — không dựng được INDEX … stage={'0'}.
               ĐỎ mảnh 0/8 [M-loi]: 1 lỗi đột biến — không ghi tệp; rc=1.
  kết luận   : KHÔNG PHẢI LỖI: thiếu phép đo ca ĐÍCH kéo mảnh đỏ đúng; không được coi đây là mảnh đạt.
               Log evidence/shard0.log. Đang chạy lại cùng mảnh với env Git sửa; không đổi mã ứng viên.
  bổ sung hoàn tất HƯỚNG 9 (môi trường Git đã sửa, SHA ứng viên nguyên bản):
               `CONG_CU_TEST_TIEN_TRINH=2 CONG_CU_TEST_MANH=0/8 CONG_CU_TEST_MANH_RA=/tmp/rv668-real-fixed/m-0.txt python3 evidence/with_git_env.py python3 -u cay-kho/ops/cong_cu_test.py`
               Nền 55/55, bỏ qua=0; MẢNH 0/8: 31/31 đột biến bán kính 1; rc=0.
               `python3 evidence/with_git_env.py python3 evidence/mixed_probe.py`
               REAL records=31 unique=31 one_correct_kill_each=True skipped=0.
               MIXED:31_REAL_211_SYNTHETIC rc=0; GOM MẢNH 8/8; ca=55 đột biến=242 lỗi=0; 242 dòng ok.
               REAL_RECORD_TARGET_SURVIVES rc=1; lỗi đột biến=1, 241 dòng ok.
               REAL_RECORD_DELETED rc=1 [G-ban-ghi], thiếu g668_che_do_bo_tran_tren.
               Bản ghi thật giữ ở evidence/real-m-0.txt; log evidence/shard0-fixed.log, evidence/mixed.log.
               Phân hoạch đo thêm N=2..16 bằng evidence/geometry_probe.py: mỗi N tổng=242, unique=242, exact=True.
  kết luận cuối HƯỚNG 9: KHÔNG PHẢI LỖI ở mảnh thật và các phản chứng đã chạy. A1 trọn 8 mảnh thật chưa đo.

Bảng trạng thái nghiệm thu (không suy rộng từ tổng suite):

| Phạm vi | Trạng thái độc lập |
|---|---|
| M1 / gate / N126 | passed trên SHA ứng viên, 55/55, không bỏ qua; F2 chỉ ra thiếu độ phủ nhánh main |
| M2 / mảnh thật | passed 0/8, 31/31; lần môi trường ký commit lỗi đã fail-closed đúng |
| M3 / gom | passed cấu trúc/đối chứng: bộ dựng và bộ hỗn hợp; chưa chứng minh 242 bản ghi thật |
| M4 / 30 g668_* | 30 bị giết đúng lý do; lượt bán kính có t47 skipped, đã khai; thiếu chốt main: F2 |
| M5–M6 / workflow | workflow gốc validator=[], actionlint rc=0; phản chứng shell lọt: F1 |
| A7 | registry, t152, lease subset, actionlint đạt hai SHA; bare Ruff F có 6 lỗi nền, delta=0 cùng Ruff 0.15.8 |
| A1 toàn bộ / A5 CLI mặc định nguyên bản toàn bộ | not_run; không ghi approve cho hai mục này |
| Windows, runner GitHub, latency A9, upload/download thực | not_measured; không chạy CI theo chỉ thị |
| ~93%, ~43 phút của executor/spec | Không đo lại lịch sử CI; không dùng làm căn cứ verdict. Thời gian local đồng thời ở đây không dùng làm benchmark A9 |

Mọi phép đo đã khởi chạy nêu ở các bổ sung trên đã hoàn tất. Các chữ “đang chạy” trong khối trước là trạng thái lúc ghi dần, được thay thế bởi bổ sung hoàn tất.
Kiểm cuối: `git -C cay-kho rev-parse HEAD` vẫn c8f52b6c89fcc62ed63b6e358892d7bbaf5be73b;
`git -C cay-kho diff --exit-code` rc=0; `git -C cay-kho status --porcelain=v1` không có output.
Không sửa mã sản phẩm trong cây ứng viên, không push, không CI. Các script dưới evidence/ là công cụ phản chứng, không phải patch đề nghị áp vào sản phẩm.

Bảng lớp finding (lượt 1; nguồn: SHA ứng viên; 2 lớp, 2 finding):

| slug lớp | finding | mức cao nhất | hướng sửa / phép đo đóng lớp |
|---|---|---|---|
| g5-shell-bo-qua-thuc-thi | F1 | P1 | Ràng buộc ngữ nghĩa thực thi bước gom, ít nhất shell hợp lệ phải thực sự chạy lệnh; thêm phản chứng shell syntax-only. Giữ đối chứng workflow gốc xanh, bộ 1/8 bị gom đỏ. |
| g5-main-thieu-ca-chon-vong-ban-kinh | F2 | P2 | Thêm phép đo qua cửa main/CLI cho nhánh du/gate/manh cùng đột biến riêng. Mutant bỏ vòng mặc định phải bị ca đích giết đúng lý do; phân biệt vòng đầy đủ với con tự kiểm N126. |

Bảng finding cuối:

| ID | mức | tệp:dòng | mô tả | phản chứng chạy được |
|---|---|---|---|---|
| F1 | P1 | .claude/dev/ci_dang_ky_test.py:1118 | Allowlist chỉ đọc run/env/if, không ràng buộc shell: bước gom với `shell: bash -n {0}` được validator nhận, actionlint hợp lệ, trả rc=0 mà không kiểm bất kỳ mảnh nào. Với thư mục 1/8 mảnh, shell chuẩn trả G-tap, shell đổi vẫn xanh. Đây là lỗ bảo vệ cấu hình mới; không khẳng định workflow nguyên bản hiện đang dùng shell sai. | `PYTHONDONTWRITEBYTECODE=1 python3 evidence/workflow_probe.py`; evidence/workflow.log; workflow-shell.yml |
| F2 | P2 | ops/cong_cu_test.py:6351; ops/cong_cu_test.py:7123 | M4 chưa có ca/đột biến riêng gác nhánh main chọn chạy vòng đầy đủ. Đột biến cho cả du đi vào nhánh gate sống sót qua 55/55 ca; CLI mặc định của bản sao trả rc=0, N126 đạt nhưng bỏ vòng đầy đủ. | `python3 evidence/with_git_env.py python3 evidence/missing_guard_probe.py`, sau đó CLI của /tmp/rv668-copy; evidence/missing-guard-fixed.log và default-mutated.log |

verdict: changes_requested
reviewed_sha: c8f52b6c89fcc62ed63b6e358892d7bbaf5be73b
