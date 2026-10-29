verdict: changes_requested
reviewed_sha: f7659a2f911e4a686d2b312ce046f3625a563b93
Kết quả: 0 P0, 6 P1, 1 P2, 1 P3.

## BẢNG ĐO
| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Danh tính/phạm vi | f7659a2 trên base 4488444, đúng 2 tệp | Hướng 1/7: HEAD đúng; tree 629fb10af4dd84631518a66705d3e4ee83f05e15; status rỗng; +307/-289 = 596 dòng | Khớp |
| Spec đóng băng | SHA256 9a155cb9…3b1ca | `sha256sum` = 9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca | Khớp |
| Lời khai 1: gate head | rc=0, nợ 1/60/0, surface chua=0 | `gate-head.log`: 244 đạt, 11 miễn, 42 nợ lược đồ, 0 lỗi/unknown, 297 receipt, TỔNG: ĐẠT | Khớp ở lượt danh nghĩa |
| Lời khai 2: suite | 87/87, 99/99, 2/2 | `suite.log`, rc=0, đủ ba tỷ lệ; 81/99 mutant có đối chứng | Khớp; chưa chứng minh mọi chốt mới có răng |
| Lời khai 3 / M1 / B1 | Bỏ đọc mốc/lịch sử; hai ca có mốc vẫn rc=1; rg 0 dòng | Hướng 13: c86 qua; rg 0 dòng; diff không còn hàm mốc/lịch sử | Khớp |
| Lời khai 4 / M2 / B2 | Mọi lỗi đọc/phân tích/git trong ba luật và băm-đọc receipt rc=2; không nợ chết | Hướng 4/5: reviewer đo 8/8 tổ hợp B2 đạt; còn git mất→0, ref tree thật→1, run.json-thư-mục→0/1 và --sinh-no→traceback/1; test B2 thiếu tổ hợp | Không: 4 finding hành vi và 1 P2 phạm vi đo |
| Lời khai 5 / M3 / B3 | OID theo 4 ngữ cảnh, OID thật thuần luôn tra | c71/c78/c87 trong full suite đạt; git mất với OID thật thuần trả 0; r2/r4 sống sót | Đạt ngữ cảnh khi git hoạt động; lỗi đo/thiếu răng còn mở |
| Lời khai 6 / M4 / B4 | Cửa sổ 3 dòng có từ provider, không citation; hai khai báo cùng dòng; citation sau cũng loại | c79/c83/c88 đạt; 20 verdict: 7 lời khai chính tắc, 6 mismatch đều caveat; r5/r6 sống sót | Đạt hành vi nguyên trạng và corpus; thiếu răng biên |
| Lời khai 7 / M5 / B5 | 61 nợ 1/60/0; bỏ 3 L-SURFACE chết; bánh cóc | `audit_corpus.py`: 61/61 tuple có chứng cứ Git; gate r2 trên dữ liệu base/head rc0; nợ rỗng đều rc1 đúng 61 dòng; c75 đạt | Khớp |
| Lời khai 8: đột biến mốc/neo cũ | Bỏ m77/86/87/90/93; neo lại m76/83/84/92 | `mutation-inventory.log`: gỡ đúng 5 ID, thêm 94–102; bốn neo cũ đều CÓ RĂNG/giet_that | Khớp |
| M6: từng chốt có đột biến | Test M1–M5 và đột biến mỗi chốt | 9 mutant riêng ngoài m94–m102/m85; 5 sống sót qua 87/87, có phản chứng không tương đương | Không: 2 finding thiếu răng (4 selector + 1 biên mã hóa) |
| B6: literal/folded | m78 giết literal; folded hồi quy và docstring khai giới hạn | `b1-b6.log`: m78 chỉ giết khoi_lit; khoi_gap vẫn có; giới hạn ở inline comment, chưa ở docstring | Đạt hành vi; P3 diễn đạt |
| B7: không phá gì | N/N, mutant cũ có răng, F delta0, doctrine/diff sạch; numstat đối chiếu ADR-0044 | Hướng 7: đủ N/N; F541 base=head=1; doctrine/diff rc0; 2 tệp/596 dòng dưới 1.000 | Khớp cục bộ; việc đã ghi numstat vào PR KHÔNG ĐO ĐƯỢC vì không gọi mạng |
| B8: nền B1–B4 | B1=0; B2 directory ném; B3 token thuần thiếu=0; B4=[1,1,1] | `baseline-complete.log`: B1=[0,0], B3=[0,0,0,0,0], c71=[1,0,2], OID thật thuần=[1,1], B4=[1,1,1], hai thứ tự=[1,1]; base directory IsADirectoryError | Khớp; status qua của logger nền không phải test pass (tắt assertion HEAD để thu đủ kết quả) |
| Ứng viên thật | Mọi receipt và verdict có run_json | 297 receipt; 99 token ancestry/97 resolve; 2 token ngày bỏ đúng; 20 verdict, 10 dòng qua cửa sổ, 7 giá trị chính tắc + 3 diễn đạt tự do | Không thấy lỗi corpus ngoài giới hạn heuristic được spec thừa nhận |
| CI pull_request | Merge commit, fetch-depth=0, không origin/HEAD | `ci.log`: merge 2 parent/đúng tree head/shallow=false/origin HEAD vắng/gate rc0; ref tree thật fallback sai ở hướng 10 | PR local bình thường đạt; ref hỏng không đạt |
| Biên M2 với lỗi lập trình | Nhiệm vụ yêu cầu phản chứng | Tiêm NameError vào _bo_dau: rc2, stderr nêu NameError, không traceback | Biên có chuyển lỗi lập trình thành rc2; không gán bug tiêm là bug production |
| HINT.patch | patch -p0, dry-run exact head/fuzz=0 | `hint-dry-run-final.log`: checking file ops/bien_nhan_v2.py, rc0; 4 phản chứng hành vi chuyển rc2 trên clone hint | Đạt phạm vi hint một phần; chưa áp cây thật/chưa full-suite hint |

## BẢNG SĂN

Review chỉ đọc tại exact SHA trên; mọi đột biến trên bản sao ngoài cay-kho/, không gọi mạng, không push. Gate hiện hữu xanh nhưng có bốn đường lỗi ĐO ra sai trạng thái, năm chốt thiếu răng (gộp hai finding), một thiếu sót ma trận B2 và một P3 docstring. Log/script tái lập nằm trong thư mục giao việc này. Không suy môi trường thực thi/model phục vụ từ tên launcher hay tên reviewer.

HƯỚNG 1: danh tính cây và phạm vi đóng băng
  giả thuyết : snapshot hoặc spec khác đối tượng được giao.
  lệnh       : `git -C cay-kho status --short; git -C cay-kho rev-parse HEAD; git -C cay-kho rev-parse --is-shallow-repository; sha256sum cay-kho/ops/specs/NO-CAU-LICH-SU-BIEN-NHAN-r2.md; cat numstat.txt`.
  output     : status rỗng; HEAD=f7659a2f911e4a686d2b312ce046f3625a563b93; shallow=false; sha256=9a155cb9995b225129dc11de03e2d6d9811a9c53321151e0389214a85d33b1ca; numstat: 139/185 ops/bien_nhan_v2.py, 168/104 ops/bien_nhan_v2_test.py.
  kết luận   : KHÔNG PHẢI LỖI. Đúng SHA, đúng hai tệp, +307/-289 = 596 dòng thay đổi, dưới 1.000 dòng của spec.

HƯỚNG 2: cổng hiện tại trên exact head
  giả thuyết : lời khai rc=0/số nợ không tái lập.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .` (cwd cay-kho; log `evidence/gate-head.log`).
  output     : `244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 297`; `câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0`; `TỔNG: ĐẠT`; rc=0.
  kết luận   : KHÔNG PHẢI LỖI ở phép đo danh nghĩa; còn phải kiểm độc lập sự đúng của nợ.

HƯỚNG 3: lỗi thực thi git bị đổi thành token thường
  giả thuyết : `_commit_cua` làm mất rc của git; M3 bỏ token thuần khi git HỎNG như khi token không tồn tại.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py boundaries` (bản sao `/tmp/wp960-r2-review-copy`; fixture `_kho_cau`, `_commit_tien_to_so`, `_ghi_bn_cau` có sẵn; chỉ đổi PATH sau dựng kho).
  output     : `pure-real-control`: OID=dbffbbc94a7488c35d0a4050c1d26ffad20fa8ad, câu `Ban dbffbbc chua vao master.` ⇒ rc=1, đúng một L-ANCESTRY, unknown=[]; `pure-real-git-absent` cùng fixture ⇒ rc=0, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC, `TỔNG: ĐẠT`, stderr rỗng. `_git` đo trực tiếp khi PATH không chứa git ⇒ `[127, "FileNotFoundError: ... 'git'"]`. Đối chứng `Commit deadbeef` ⇒ rc=2 cả trước/sau lỗi git. Log `evidence/boundaries.log`.
  kết luận   : LỖI — M2 không chuyển mọi lỗi gọi git thành rc=2. Ngoài ra đột biến `_bo_dau` ném NameError ⇒ rc=2 với tên lỗi hiện rõ ở stderr (`programming-name-error`); không xem đây là bug production đã có, và không lập finding riêng chỉ từ lỗi lập trình được tiêm.

### git-hong-thanh-token-thuong [P1] Lỗi gọi git vẫn trả sạch cho OID toàn chữ/số không có ngữ cảnh
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1113`, `1221`–`1223` (cùng `_git:805`).
VẤN ĐỀ: `_git` đổi lỗi thực thi thành rc=127, `_commit_cua` gộp mọi rc khác 0 thành None. Nhánh M3 coi None của token thuần như bằng chứng token không phải OID và bỏ qua. Vì vậy một lỗi ĐO thành SẠCH; biên `except Exception` mới không bao giờ thấy lỗi đã bị đổi thành giá trị trả về. Đây là đường còn hở của M2, đồng thời làm mất tính chất M3 “token tra ra commit luôn là ứng viên”.
ĐÃ THỬ NGHIỆM: `python3 -u probe_review.py boundaries` ⇒ OID thật dbffbbc… đã merge vào master của kho fixture, `Ban dbffbbc chua vao master.` bình thường rc=1; chỉ đổi PATH làm git không chạy ⇒ CLI rc=0, `TỔNG: ĐẠT`, stderr rỗng. Log `evidence/boundaries.log`.
GỢI Ý VÁ: ở `_git`/`_commit_cua` và caller M3, giữ riêng lỗi vận hành/rc bất thường với “tra thành công nhưng không thấy commit”, đưa lỗi vận hành sang `KhongDoDuoc`; khóa cặp OID thật thuần chữ không nhãn và git vắng/hỏng bằng CLI rc=2. Giữ đối chứng `deadbeef`/số Actions không tồn tại và git hoạt động vẫn rc=0. Rủi ro: không được biến rc=1 hợp lệ của phép resolve token thường thành vi phạm hay rc=2 đại trà; phân biệt ref vắng hợp lệ với kho/git hỏng.
ĐỘ TIN: cao

HƯỚNG 4: ma trận B2 và phép đo phủ test
  giả thuyết : c77/c82/c84/c89/c90 có đủ bốn nguồn × hai trạng thái nợ và kiểm stderr như B2.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py b2coverage` (spy chỉ ghi tham số `kiem`, gọi nguyên các ca có sẵn).
  output     : cả 5 ca `qua`; c77: 8 lời gọi, mỗi loại có/không nợ; c82: 2 lời gọi đều `debt=[]` (một alias vòng, một alias dùng lại); c84: 1 lời gọi `debt=[]`; c89: 1 lời gọi, không truyền `no_cau_lich_su` (nợ mặc định chỉ có tên kho thật, không có receipt fixture); c90: 2 lời gọi có/không nợ nhưng lỗi là RuntimeError tự tiêm, không phải ba nguồn còn thiếu. Log `evidence/b2coverage.log`.
  kết luận   : LỖI nghiệm thu B2: thiếu tổ hợp và thiếu kiểm CLI/stderr cho alias/tree. Đo bổ sung của reviewer không thay thế ca khóa của executor.

### b2-chua-do-du-ma-tran [P2] Ba nguồn hỏng chưa có đủ ca có nợ và bằng chứng stderr theo B2
HÌNH DẠNG: khac
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2871`, `2911`, `2982`–`3000`.
VẤN ĐỀ: B2 đòi bốn nguồn hỏng, MỖI nguồn chạy cả có/không nợ tương ứng, rc=2, stderr không Traceback/NỢ CHẾT. Receipt-thư-mục (c89), alias vòng (c82), nhánh mặc định là tree (c84) đều chưa có lượt với mục nợ tương ứng. c82/c84 gọi API và chỉ xét exception/thống kê, không đo stderr CLI; c89 có bắt stdout/stderr nhưng không assert hai chuỗi cấm. c90 chỉ bù một lỗi RuntimeError giả, không đáp ứng ba fixture được nêu rõ ở B2.
ĐÃ THỬ NGHIỆM: `python3 -u probe_review.py b2coverage` ghi nguyên lời gọi của năm ca: c82=2 lần không nợ, c84=1 lần không nợ, c89=1 lần không truyền nợ; c77 đủ 8 lần; c90 đủ 2 lần nhưng nguồn khác. Log `evidence/b2coverage.log`.
GỢI Ý VÁ: tại ba ca trên, lặp hai bộ nợ chứa đúng khóa/tệp và gọi CLI với allowlist fixture được tiêm; assert rc=2, không traceback và không NỢ CHẾT trên stderr. Giữ ca alias dùng lại không vòng và ca git hợp lệ làm đối chứng. Rủi ro: tránh lĩnh tín dụng từ vi phạm schema fixture hay exception của giàn giáo; từng đột biến phải giết đúng assertion của ca đích.
ĐỘ TIN: cao

HƯỚNG 5: bốn nguồn hỏng B2 qua CLI và các lỗi mã hóa
  giả thuyết : một tổ hợp thiếu của B2 thực sự thành sạch/vi phạm hoặc traceback.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py errors`; đúng builder hiện hữu, đổi receipt thành thư mục / JSON lỗi / truyền tree như c84 / alias vòng như c82; mỗi loại lặp có/không nợ.
  output     : 8/8 tổ hợp B2 rc=2, `traceback=false`, `dead=false`. Receipt UTF8 lỗi, receipt YAML lỗi, run.json UTF8 lỗi: 6/6 tổ hợp cũng rc=2, không traceback/nợ chết. Đổi run.json từ tệp thành THƯ MỤC ⇒ không nợ rc=0 `TỔNG: ĐẠT`, có nợ rc=1 `NỢ CHẾT`, cả hai `L-SURFACE chua_do_duoc 1`. Log `evidence/errors.log`.
  kết luận   : KHÔNG PHẢI LỖI ở 14 tổ hợp đầu; LỖI ở phân loại đường dẫn run.json có nhưng không đọc được (thư mục).

### run-json-thu-muc-thanh-khong-ap [P1] Nguồn run.json là thư mục bị coi như vắng và làm nợ chết
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1250`–`1253`.
VẤN ĐỀ: `not p_rj.is_file()` gộp “nguồn không có” với “nguồn có nhưng là thư mục”. Phép miễn không áp chỉ dành cho nguồn vắng; nguồn đang có mà không đọc được phải là KHÔNG ĐO ĐƯỢC theo M2. Hiện tại không thử đọc nên biên lỗi mới không thấy IsADirectoryError. Có mục nợ L-SURFACE thì lỗi nguồn còn bị kết luận thành NỢ CHẾT. Đây là đường tồn tại ở base, vẫn trong phạm vi M2 đã cam kết đóng lớp lỗi I/O/đọc nguồn; không quy là regression mới tạo bởi r2.
ĐÃ THỬ NGHIỆM: `python3 -u probe_review.py errors`, fixture `_kho_surface` có run.json đã commit; chỉ thay tệp đó bằng thư mục cùng tên. Không nợ ⇒ CLI rc=0, TỔNG: ĐẠT; có khóa `(r.receipt.yaml, verdict_path, L-SURFACE)` ⇒ rc=1, NỢ CHẾT. Đối chứng JSON lỗi/UTF8 lỗi cùng nguồn ⇒ rc=2, không NỢ CHẾT. Log `evidence/errors.log`.
GỢI Ý VÁ: tại phân loại nguồn L-SURFACE, chỉ miễn nguồn thực sự vắng; nguồn tồn tại nhưng không phải tệp đọc được phải sinh `chua[k_sf]`. Khóa fixture đổi đúng tệp→thư mục ở cả hai trạng thái nợ; giữ ca run.json thật sự vắng của c73. Rủi ro: phân biệt đường dẫn ngoài kho, symlink gãy và lỗi stat/quyền truy cập; không để stat lỗi bị coi như nguồn vắng.
ĐỘ TIN: cao

HƯỚNG 6: nền B8 (đo bằng mã base, fixture B1/B3/B4 của head)
  giả thuyết : các fixture mới không tái hiện đúng cột nền của spec.
  lệnh       : clone local mirror, checkout `44884446f71c89e25f9a72ac58e4f597db63c1ba`; `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py baseline` (tắt riêng assertion kỳ vọng HEAD để thu hết kết quả, giữ nguyên builder và mã gate base).
  output     : B1 review/ancestry=[0,0]; B3 40-hex/backtick/sau-commit/tu-thuong/so-run=[0,0,0,0,0]; B4 i/ii/iii=[1,1,1]; hai thứ tự của c83=[1,1]. Log `evidence/baseline.log`.
  kết luận   : KHÔNG PHẢI LỖI, khớp nền B1/B3/B4 của spec; B2 nền còn kiểm độc lập receipt-thư-mục.

Ghi chú giàn giáo reviewer: lượt đầu thử chạy mọi ca dưới `_dot_bien_tep` bị c42 dọn `_TAM_DOT_BIEN`, xóa chính tệp mutant và làm các ca sau lỗi FileNotFoundError. Đã dừng hai lượt bằng rc=130; không tính chúng là răng hoặc finding sản phẩm. Phép đo đột biến sẽ chuyển sang bản sao toàn kho, ghi log mới có hậu tố `valid`.

HƯỚNG 7: suite đầy đủ, đột biến cũ và kiểm tra không phá gì
  giả thuyết : suite xanh do bỏ ca, mất răng cũ, lint delta hay doctrine/diff sai.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 cay-kho/ops/bien_nhan_v2_test.py > evidence/suite.log 2>&1`; `ruff check --no-cache --select F --output-format json` trên hai tệp exact head và byte lấy bằng `git show 4488444:<tệp>`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check 4488444 HEAD`.
  output     : suite rc=0, `87/87 ca đạt · 99/99 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 81/99 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`; không thấy chuỗi sandbox `Codex home is inside a repository`. Ruff base/head đều đúng một F541 cùng tệp test dòng 1677 `f-string without any placeholders`, delta=0. Doctrine rc=0: `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`. Diff-check stdout rỗng, rc=0. Log `evidence/suite.log`, `evidence/ruff-{base,head}.json`, `evidence/doctrine.log`.
  kết luận   : KHÔNG PHẢI LỖI ở các gate hiện hữu; suite hiện hữu xanh không bác bỏ các phản chứng độc lập.

HƯỚNG 8: kiểm kê toàn bộ ứng viên thực và sự thật của 61 mục nợ
  giả thuyết : OID theo ngữ cảnh sinh unknown mới hoặc M4 vẫn đóng băng lời trích thành nợ surface.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u audit_corpus.py`; quét 297 receipt bằng YAML và mọi verdict có run_json, ghi câu/token/cửa sổ và chứng cứ từng mục vào `evidence/corpus.json`; mỗi OID của nợ được resolve và `git merge-base --is-ancestor <commit> 4488444` trực tiếp tại kho base.
  output     : `receipts 297 debt 61 verified 61 law_counts {'L-ANCESTRY': 60, 'L-REVIEW': 1}`; `tokens 99 resolved 97`; hai token không resolve là `20260917` (ci-windows-review-5/chuoi_verdict_ghi_chu) và `20260822` (lease-dang-windows-review-3/verdict_usage_caveats[15].noi_dung), cả hai mandatory=false. `run_json_receipts 20 selected_verdicts 9 selected_lines 10 mismatch_verdicts 6`. Trong 10 dòng qua cửa sổ có 7 lời khai dùng giá trị surface chính tắc, 3 dòng tự mô tả không chứa giá trị chính tắc; 6 mismatch đều có caveat. Một lời khai chính tắc đúng ở pr896-review-1. Ba nợ surface cũ pr896-review-{2,3,7} không còn mismatch. Nợ review: SHA c595292cb63fb8c09d7d7b482cda20f9d5f0917f, receipt round1 so receipt round2 cùng SHA. Log `evidence/corpus.log`, chi tiết tất cả tuple và ngữ cảnh ở `evidence/corpus.json`.
  kết luận   : KHÔNG PHẢI LỖI trên corpus này. Khớp 61 tuple thật và 6/6 caveat, không phát hiện bắt nhầm/bỏ sót ngoài heuristic được spec thừa nhận. M3 không thêm unknown trên 297 receipt hiện tại; con số “3 token” trong spec là phép đo cũ tại 20a2e2b, không áp đặt cho base lease 4488444.

HƯỚNG 9: CI pull_request không origin/HEAD
  giả thuyết : chọn nhánh mặc định hoặc nợ phụ thuộc checkout branch thay vì merge commit.
  lệnh       : clone local độc lập tại `/tmp/wp960-r2-ci`; xóa symref origin/HEAD, ghim origin/master=4488444; tạo commit-tree hai parent base/head với tree exact head rồi checkout detached; chạy gate nguyên byte head. Log `evidence/ci.log`.
  output     : merge=1ca858c22fd0a8c5fa717abf45a8c1a1c84de424; parents=`44884446f71c89e25f9a72ac58e4f597db63c1ba f7659a2f911e4a686d2b312ce046f3625a563b93`; tree=629fb10af4dd84631518a66705d3e4ee83f05e15; shallow=false; origin_HEAD_rc=128; gate_rc=0, TỔNG: ĐẠT; nợ 1/60/0, surface chua_do_duoc=0.
  kết luận   : KHÔNG PHẢI LỖI trên mô phỏng merge local này. Không gọi GitHub Actions/network; không tuyên bố CI online đã đo. Cây được giao có origin/HEAD trỏ candidate branch, nên phép audit nợ còn ghim rõ base canonical và mô phỏng này loại hẳn origin/HEAD để không phụ thuộc symref ấy.

Bổ sung kết quả hướng 8/B5: gate HEAD trên dữ liệu HEAD và base lease đều rc=0, 0 lỗi/0 unknown, nợ 1/60/0. Cùng hai cây dữ liệu với nợ câu lịch sử rỗng đều rc=1, đúng 61/61 dòng ba luật, unknown=0 (`evidence/corpus.log`, bốn dòng cuối).

HƯỚNG 10: nhánh mặc định hỏng so với tree được tiêm; đường CLI sinh nợ
  giả thuyết : c84 chỉ tiêm tree qua tham số nên bỏ qua bộ chọn nhánh, hoặc một cờ CLI còn nằm ngoài biên I/O.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py auxiliary` (fixture git c71; `git update-ref refs/remotes/origin/master HEAD^{tree}`, giữ local master; fixture receipt-thư-mục c89 cho hai cờ sinh nợ).
  output     : `default-tree-fallback`: origin/master=dca1f5b27650c0ff672a64cbb303c5e278e959da (tree); `_nhanh_mac_dinh` chọn local master=0dda7648f3476baeba72b8572a393498ca61a22c; CLI rc=1, một L-ANCESTRY, 0 KHÔNG ĐO ĐƯỢC, `TỔNG: ĐỎ`. `--sinh-no` ném IsADirectoryError ra khỏi main; `--sinh-no-cau-lich-su` cùng nguồn rc=2, không traceback. Log `evidence/auxiliary.log`.
  kết luận   : LỖI — tree ở ref thật không được bảo vệ như tree được tiêm trong c84; và đường sinh nợ cũ chưa có biên băm/đọc.

### nhanh-mac-dinh-tree-bi-bo-qua [P1] Ref mặc định có nhưng không phải commit bị thay bằng local master
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1117`–`1122`.
VẤN ĐỀ: `_nhanh_mac_dinh` coi mọi `_commit_cua(...) is None` như ref không có, thử ref tiếp theo rồi kết luận ancestry bằng local master. Khi origin/master thực sự có nhưng là tree, thông tin canonical hỏng bị bỏ qua; gate trả vi phạm/sạch thay vì KHÔNG ĐO ĐƯỢC như M2/B2 đòi. c84 tiêm trực tiếp tree vào `kiem(... nhanh_mac_dinh=tree)` nên không chạy đường chọn nhánh này. Đây là đường nền còn hở trong phạm vi M2, không phải regression do vòng try mới.
ĐÃ THỬ NGHIỆM: `python3 -u probe_review.py auxiliary` dựng git thật bằng `_kho_cau`; không origin/HEAD, `update-ref refs/remotes/origin/master <tree>` thành công; CLI tự chọn local master rồi rc=1 với 0 unknown. Trong hướng 5, truyền đúng tree ấy bằng đường c84 thì rc=2. Log `evidence/auxiliary.log`, `evidence/errors.log`.
GỢI Ý VÁ: trong `_nhanh_mac_dinh`, phân biệt ref vắng với ref tồn tại nhưng không resolve thành commit; trường hợp sau phải KhongDoDuoc, không fallback. Khóa fixture ref tree thật và giữ fixture không origin/HEAD nhưng origin/master commit hợp lệ. Rủi ro: không được chặn fallback khi ref thực sự vắng (CI thường không origin/HEAD), cũng không suy nhánh local là canonical khi remote đang hỏng.
ĐỘ TIN: cao

### sinh-no-ngoai-bien-doc-receipt [P1] Cờ sinh nợ lược đồ vẫn thoát traceback khi đọc receipt lỗi
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1406`–`1410`, `1452`–`1462`.
VẤN ĐỀ: `--sinh-no` được dispatch trước try của main; `_sinh_no` đọc/parse/băm receipt không đổi lỗi sang KhongDoDuoc. Cùng nguồn thư mục `*.receipt.yaml` mà đường gate và `--sinh-no-cau-lich-su` trả 2, đường này vẫn ném IsADirectoryError (tiến trình CLI thông thường sẽ traceback/rc=1). M2 đã bao gồm lỗi khi băm-đọc receipt, không chỉ ba luật. Đây là lỗi nền còn tồn tại, không quy là regression mới của r2.
ĐÃ THỬ NGHIỆM: `python3 -u probe_review.py auxiliary`, cùng fixture c89: `main([--root,...,--sinh-no])` ném IsADirectoryError; đổi duy nhất cờ thành `--sinh-no-cau-lich-su` ⇒ rc=2, stderr nêu đúng tên receipt, không traceback. Log `evidence/auxiliary.log`.
GỢI Ý VÁ: bọc đọc/parse/băm ở `_sinh_no`, chuyển lỗi nguồn thành KhongDoDuoc và đặt dispatch trong biên CLI tương ứng; khóa subprocess cho cả hai cờ trên fixture directory/UTF8/YAML lỗi. Rủi ro: không in khối nợ như thành công khi sinh dữ liệu chưa trọn; giữ stdout/rc0 của dữ liệu hợp lệ.
ĐỘ TIN: cao

Bổ sung hướng 6/B8: mã base thật trên receipt-thư-mục ném `IsADirectoryError` (log `evidence/base-errors.log`, dòng `base-receipt-directory`), khớp cột nền B2. Lượt `base-real` trong log đó đã tiêm NO_DA_DO={} theo helper fixture nên KHÔNG phải cổng base nguyên trạng; loại khỏi kết luận. Đo lại CLI không tiêm bằng `python3 /tmp/wp960-r2-base-repo/ops/bien_nhan_v2.py --root /tmp/wp960-r2-base-repo` ⇒ rc=0, 42 nợ lược đồ, nợ câu lịch sử 1/60/3, TỔNG: ĐẠT (`evidence/gate-base.log`). R2 sinh lại nợ 1/60/0 trên dữ liệu base đã được xác minh riêng ở hướng 8.

Bổ sung hướng 3/10 bằng TIẾN TRÌNH CLI THẬT: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py rawcli` ⇒ cùng OID thật thuần chữ, subprocess khi git hoạt động rc=1/no traceback; PATH không có git rc=0/no traceback. Receipt-thư-mục với `--sinh-no` subprocess rc=1, `Traceback` + IsADirectoryError; `--sinh-no-cau-lich-su` rc=2, không Traceback (`evidence/raw-cli.log`). Các trạng thái không chỉ là giá trị main được gọi trong tiến trình reviewer.

HƯỚNG 11: răng bắt lỗi mã hóa của biên băm/đọc mới
  giả thuyết : m95 chỉ khóa OSError, còn UnicodeDecodeError mới được chuyển sang biên khác mà không ca nào canh.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_mutations.py r8-receipt-encoding r9-rethrow-alias` trên clone toàn kho exact head, gỡ riêng `UnicodeDecodeError` khỏi except (giữ OSError); chạy nguyên 87 ca hiện hữu. Phản chứng: `python3 -u probe_review.py witnesses` và `rawcli` (receipt chỉ đổi nội dung byte sang UTF8 lỗi).
  output     : r8=`87/87`, red=[]; receipt UTF8 lỗi ở mã nguyên trạng subprocess rc=2/no Traceback; cùng fixture dưới r8 subprocess rc=1/Traceback UnicodeDecodeError. Log `evidence/mutations-3-valid.log`, `evidence/mutant-witnesses.log`, `evidence/raw-cli.log`. r9 được đo riêng và giết đúng c82 (86/87); không dùng làm chứng cứ cho r8.
  kết luận   : LỖI — chốt mã hóa mới không có răng, ngoài m94–m102/m85.

### bien-utf8-receipt-chua-co-rang [P1] Bỏ bắt UnicodeDecodeError mà toàn bộ 87 ca vẫn đạt
HÌNH DẠNG: loi-do
TỆP/DÒNG: `ops/bien_nhan_v2.py:1322`; `ops/bien_nhan_v2_test.py:2982`–`3000`, `3656`–`3660`.
VẤN ĐỀ: Sau khi đưa đọc receipt ra khỏi try phân tích YAML, chốt riêng UnicodeDecodeError ở 1322 bảo đảm byte lỗi còn rc=2. m95 chỉ gỡ OSError và c89 chỉ có receipt-thư-mục. Bỏ riêng UnicodeDecodeError (giữ nguyên xử lý I/O) làm byte lỗi thoát traceback/rc=1 mà không một ca nào trong 87 ca hiện hữu đỏ. M6 đòi đột biến từng chốt; đây là thiếu răng thực, không phải mutant tương đương.
ĐÃ THỬ NGHIỆM: `python3 -u probe_mutations.py r8-receipt-encoding` ⇒ 87/87, red=[]; `python3 -u probe_review.py rawcli` ⇒ cùng byte `schema_version: 1\nx: \xff\n`, nguyên trạng subprocess rc=2/no Traceback, mutant rc=1/Traceback UnicodeDecodeError. Log ở hướng 11.
GỢI Ý VÁ: thêm fixture receipt UTF8 lỗi vào vùng c89/các ca M2, assert subprocess rc=2 không traceback, chạy cả có/không nợ và thêm mutant chỉ bỏ bắt UnicodeDecodeError. Rủi ro: không dùng lỗi byte trong verdict/run.json thay thế, vì chúng đi qua biên khác và không khóa 1322; giữ c89 I/O hiện hữu.
ĐỘ TIN: cao

HƯỚNG 12: gợi ý vá chỉ trên clone
  giả thuyết : cách phân biệt lỗi vận hành/ref/nguồn và bọc đường sinh nợ sửa được bốn phản chứng hành vi mà không làm mất đối chứng.
  lệnh       : tạo `HINT.patch` từ clone `/tmp/wp960-r2-hint` của exact head; `patch --dry-run --fuzz=0 -p0 -d /tmp/wp960-r2-review-copy < HINT.patch`; chạy lại `probe_review.py boundaries/errors/auxiliary` với `WP960_REVIEW_COPY=/tmp/wp960-r2-hint` SAU khi tạo patch xong.
  output     : dry-run `checking file ops/bien_nhan_v2.py`, rc=0, không fuzz/offset; git mất với OID thật thuần chữ ⇒ rc=2; đối chứng git hoạt động ⇒ rc=1; token thường không resolve khi git hoạt động ⇒ rc=0; run.json-thư-mục cả có/không nợ ⇒ rc=2, không NỢ CHẾT; ref mặc định tree thật ⇒ KhongDoDuoc và CLI rc=2; cả hai cờ sinh nợ với receipt-thư-mục ⇒ rc=2; 14 tổ hợp nguồn hỏng còn lại vẫn rc=2. Log `evidence/hint-{boundaries,errors,auxiliary}-valid.log`, `evidence/hint-dry-run.log`.
  kết luận   : KHÔNG PHẢI LỖI trong phạm vi phép đo hint này. Đây là gợi ý MỘT PHẦN, chưa áp cây thật, chưa chạy full-suite trên hint, chưa bổ sung các ca/đột biến thiếu; executor phải tái dẫn xuất và đo đủ, không dùng hint làm approval.

HƯỚNG 13: vế âm M1 và răng literal B6
  giả thuyết : còn đường đọc mốc hoặc m78 chết bởi folded thay vì literal như đặc tả mới đòi.
  lệnh       : `rg -n '"dung_tai"|def _moc_|def _commit_them_cau|def _co_cau' cay-kho/ops/bien_nhan_v2.py`; gọi nguyên c86 và c72, rồi áp đúng phép thay của m78 trên bản sao và gọi riêng c72 (`evidence/b1-b6.log`).
  output     : rg 0 dòng (rc=1 nghĩa là không match); B1 `qua`; B6 nền `qua`; B6-m78 `giet_that`, lý do DUY NHẤT: `khối | gãy dòng (khoi_lit) không bị nhận: ['co_dau', 'khoi_gap', 'khong_dau']`. `inspect.getdoc(c72)` chỉ nói cả | và >- được nhận, không có lời khai >- là hồi quy/không có chốt; lời khai ấy hiện nằm ở comment 2690–2692.
  kết luận   : KHÔNG PHẢI LỖI hành vi M1/B1/B6. Có thiếu sót diễn đạt P3 ở vị trí docstring mà B6 yêu cầu; không đánh đồng với lỗi folded của r1 (r2 đã thu hẹp yêu cầu bằng authority trong spec).

### b6-docstring-chua-khai-gioi-han [P3] Lời khai giới hạn folded vẫn nằm ở comment thay vì docstring
HÌNH DẠNG: khac
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2673`–`2674` (lời khai đúng ở comment `2690`–`2692`).
VẤN ĐỀ: B6 đòi docstring khai rõ khối >- chỉ là ca hồi quy, không có chốt riêng trong cổng. Docstring c72 vẫn chỉ nói cả | và >- được nhận. Inline comment đã giải thích đúng giới hạn, nên đây chỉ là thiếu diễn đạt ở đúng nơi yêu cầu, không phải thiếu răng literal hay lỗi nhận folded.
ĐÃ THỬ NGHIỆM: `evidence/b1-b6.log`: `inspect.getdoc(c72)` không có giới hạn trên; m78 giết đúng `khoi_lit`, `khoi_gap` vẫn bị nhận như thiết kế mới.
GỢI Ý VÁ: đưa câu giải thích trong comment 2690–2692 vào docstring c72; giữ assertion/m78 hiện tại. Ca khóa là c72 hiện hữu và kiểm nội dung docstring bằng đọc lại; không cần thêm test máy cho thay đổi diễn đạt này. Rủi ro: đừng khôi phục yêu cầu răng folded mà r2 đã bỏ có chủ đích.
ĐỘ TIN: cao

HƯỚNG 14: gỡ chốt bộ chọn mới, ngoài m94–m102/m85
  giả thuyết : các ca mới chỉ khóa nhánh dương, chưa khóa ranh giới từ/backtick và cạnh phải cửa sổ.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_mutations.py r1-commit-case r2-commit-boundary r3-commit-adjacent r4-backtick-close`; `... r5-provider-boundary r6-window-next r7-window-prev`; `... r8-receipt-encoding r9-rethrow-alias`. Mỗi mutant được clone toàn kho exact head, chỉ thay đúng một mẫu code (assert count=1), chạy CẢ 87 ca nguyên trạng. Phản chứng không tương đương: `python3 -u probe_review.py witnesses`.
  output     : cả ba lệnh kết thúc rc=0 (đây là runner đo, không coi rc của runner là răng). Bảng kết quả THẬT:

| mutant | chốt bị gỡ/đổi | ca đạt | ca ĐỎ thật (`TinHieuChotCa`/`giet_that`) |
|---|---|---|---|
| r1-commit-case | bỏ IGNORECASE của từ commit | 86/87 | c87: sau-commit đòi 2 được 0 |
| r2-commit-boundary | bỏ `\b` trước commit | 87/87 | KHÔNG CÓ |
| r3-commit-adjacent | bỏ `\Z`, commit không cần đứng ngay trước token | 84/87 | c40, c14, c76: số ngày 20260917 bị bắt thành OID bắt buộc trên corpus |
| r4-backtick-close | chỉ cần backtick mở, bỏ backtick đóng | 87/87 | KHÔNG CÓ |
| r5-provider-boundary | bỏ `\b` hai đầu provider | 87/87 | KHÔNG CÓ |
| r6-window-next | bỏ dòng sau khỏi cửa sổ M4 | 87/87 | KHÔNG CÓ |
| r7-window-prev | bỏ dòng trước khỏi cửa sổ M4 | 80/87 | c1, c40, c14, c73, c76, c83, c88 |
| r8-receipt-encoding | bỏ bắt UnicodeDecodeError, giữ OSError | 87/87 | KHÔNG CÓ (finding riêng ở hướng 11) |
| r9-rethrow-alias | bỏ ném lại KhongDoDuoc trước except Exception | 86/87 | c82: đòi KhongDoDuoc, không được chuyển thành kết quả API |

  Phản chứng cho bốn selector sống sót: r2 `Precommit 1234567 chua vao master.` rc=0→2; r4 `Ban \`abcdefa chua vao master.` (thiếu backtick đóng) rc=0→2; r5 `notprovider: openai_codex` + khai sai surface rc=0→1; r6 khai sai surface rồi dòng SAU là `provider: openai_codex` rc=1→0. Mỗi cặp chỉ thay code, fixture giữ nguyên; nguyên trạng khớp M3/M4, mutant làm sai định nghĩa. r8 rc=2→traceback/rc=1 qua subprocess. Log `evidence/mutations-{1,2,3}-valid.log`, `evidence/mutant-witnesses.log`, `evidence/raw-cli.log`.
  kết luận   : LỖI — 5/9 chốt được gỡ không làm ca nào đỏ, đã chứng minh không tương đương. 4 selector gộp một finding dưới đây; chốt mã hóa có finding riêng. Không tính các lượt rig hỏng đã loại trước đó.

### bo-chon-moi-chua-khoa-bien [P1] Bốn chốt chọn OID/surface có thể bị đổi sai mà 87 ca vẫn xanh
HÌNH DẠNG: bo-chon-ung-vien
TỆP/DÒNG: `ops/bien_nhan_v2.py:975`, `988`, `1004`, `1148`; `ops/bien_nhan_v2_test.py:2944`–`2980` và dàn đột biến `3670`–`3690`.
VẤN ĐỀ: M6 đòi đột biến từng chốt. Các đột biến hiện tại bỏ toàn bộ ngữ cảnh commit/backtick hoặc điều kiện provider/trích dẫn nhưng không khóa ranh giới “từ commit”, backtick hai đầu, “từ provider”, và việc dòng SAU phải thuộc cửa sổ. Bốn thay đổi riêng làm sai định nghĩa M3/M4 đều sống sót qua 87/87 ca. Đây là thiếu răng test, không tuyên bố các chốt nguyên trạng đang chọn sai corpus thật.
ĐÃ THỬ NGHIỆM: hướng 14 — r2/r4/r5/r6 đều 87/87, red=[]; phản chứng tương ứng cho kết quả 0→2, 0→2, 0→1, 1→0. Mã và mẫu thay nguyên văn có trong `probe_mutations.py` và JSON log; mọi lần chạy được clone lại từ exact head, không sửa cây review.
GỢI Ý VÁ: bổ sung đối chứng âm `Precommit`, backtick thiếu đầu/cuối, `notprovider`/`provider_extra`, và đối chứng provider ở dòng sau (kèm citation ở dòng sau); mỗi chốt có mutant riêng và phải làm đúng ca đích đỏ. Giữ c87/c88/c83 và đối chứng git/caveat hiện hữu. Rủi ro: không thu hẹp M4 chỉ còn provider cùng dòng/trước để làm test dễ qua; không biến mọi token thuần thành bắt buộc hoặc bỏ OID thật.
ĐỘ TIN: cao

Bổ sung hướng 11: r9 đã kết thúc, 86/87, đúng c82 `giet_that`; không phát hiện chốt ném lại alias mất răng. Bổ sung hướng 7/lời khai 8: inventory static so base gỡ đúng `[77,86,87,90,93]`, thêm `[94,95,96,97,98,99,100,101,102]`, giữ 88 ID cũ (gồm hai ca tự kiểm); m76/m83/m84/m92 đều CÓ RĂNG/giet_that trên đúng ca đích (`evidence/mutation-inventory.log`).


## TÍNH TOÀN VẸN VÀ GIỚI HẠN

Kiểm cuối `evidence/final-tree.log`: HEAD vẫn `f7659a2f911e4a686d2b312ce046f3625a563b93`, tree `629fb10af4dd84631518a66705d3e4ee83f05e15`, status rỗng; hai tệp review byte-identical với blob tại SHA được giao, diff-check rc=0. SHA256 cổng `737c7849878e72e9348c1a6ce2e890d2f6e2ff03f6cc22007229575d0880bd3f`; test `66ae3adbf07e36214176370274041c5670503a94169479ef2d7d923ca86457b2`.

Các log mutant/hint có hậu tố `valid` mới là phép đo cuối. Log mutant đầu bị lỗi dọn scratch đã bị loại (giải thích sau hướng 6). Lượt hint đầu bắt đầu trước khi clone được sửa xong cũng không dùng; các phép đo hint `*-valid.log` chạy lại sau dry-run, và `hint-auxiliary-valid.log` đã chạy lại sau khi logger được sửa để ghi cả KhongDoDuoc của bộ chọn nhánh. `base-real` có tiêm NO_DA_DO={} trong log nháp bị loại; CLI base không tiêm ở `gate-base.log` mới là phép đo base. Không log invalid nào được dùng làm finding hoặc răng.

Không đo GitHub Actions/PR online, không tuyên bố regex phủ mọi văn xuôi ngoài định nghĩa heuristic đóng băng. `HINT.patch` là gợi ý một phần đã chạy trên clone, chưa áp cây thật; không thay đổi nợ/receipt, không thay các ca/đột biến còn thiếu. Trong corpus thực không còn finding nguồn gốc câu cho mốc: M1 đã xoá đường đó.

Các finding `loi-do` và `bo-chon-ung-vien` làm tái xuất hiện hình dạng kế thừa trong review r2; theo Q8 / lease M-4, executor phải dừng để chủ kho quyết định hướng tiếp theo. Review này không cấp quyền vá tiếp, merge hoặc land.
