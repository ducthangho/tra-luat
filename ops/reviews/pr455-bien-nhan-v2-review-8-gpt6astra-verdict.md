# Cross-review vòng 8 — lượt cuối — PR #455

**approve_with_findings: 1 P2 về độ phủ hồi quy, 2 P3 về hồ sơ bằng chứng. Chưa chứng minh P0/P1 mới.** Các phản chứng cụ thể R7-01, R7-02, R7-04, R7-05 đã được xử lý; R7-03 đóng các phản chứng cũ nhưng phần neo luật mới vẫn có hai phép làm yếu đi qua toàn suite. Không tự mở thêm vòng review, không suy verdict này thành quyền land.

- `reviewed_sha`: `c0f18ac1fac53d72cb8e458fc20611dd8099fedc`.
- `reviewed_tree`: `6a7d319395e2a16d4ee07bd94bf0463734d3af50`.
- Diff chính: `b912e5f..c0f18ac`, 6 tệp; đối chiếu thêm `ca960160..c0f18ac`, 13 tệp.
- Reviewer độc lập với Executor Claude; provider `openai_codex`, bề mặt Codex service/API có shell Linux, transport `machine`. Chỉ thị phiên định danh GPT-6; không có chứng thực độc lập backend/model version hay launcher run của phiên này.
- Authority: chỉ thị trực tiếp của người dùng giao review exact head và ghi `VERDICT.md` ngoài clone. Không được cung cấp Packet revision/spec hash/generation riêng để xác minh; không tự cấp chúng.

Đã đo tại `cay-kho/`: detached đúng head; 1.759 commit reachable từ HEAD; không shallow; **339 ref tổng, trong đó 299 ref remote-tracking**; `core.abbrev=7`. Vì vậy “299 ref” đúng khi có đơn vị remote-tracking như EVIDENCE, không phải tổng mọi ref. Linux, Python 3.11.15, PyYAML 6.0.1. Worktree sạch trước và sau phép đo. Mọi thay đổi phục vụ phản chứng nằm trong `/tmp`, ngoài clone. Không tự soạn chuỗi thoát, đồng tự Unicode hay đường dẫn tấn công; các fixture loại đó được chạy nguyên từ cây. Không commit/push vào kho được review.

## Ba phép bác của điều phối và hợp đồng human

1. **Lớp quyền: phép bác chưa chứng minh được kết luận cuối.** Ghi được bằng Python chỉ xác minh đường ghi ấy ở môi trường ấy. Hook cho `Edit` đi qua chỉ loại được chính hook trong phép thử đó. `pretooluse_guard.py:947` trả ngay khi tool không phải `Bash`; nó không kiểm đường dẫn Edit. Chưa có phép đo dương xác định thành phần CLI đã từ chối, cũng chưa loại hết các lớp còn lại. Báo cáo executor nói “hệ thống quyền của nền Claude Code”, không nhất thiết có nghĩa “hệ thống tệp”. Kết luận “CLI là nghi vấn” hợp lý; “đã đo ba lớp, nên executor sai lớp” rộng hơn bằng chứng. Chi tiết R8-02.

2. **Tên chép tay trên `4488ff1`: điều phối bác đúng.** `git show 4488ff1:ops/bien_nhan_v2.py` dòng 269 là `PROVIDER_KHONG_HOP_DONG = frozenset({"human"})`; dòng 273–274 hợp nó vào danh sách cho phép. Sau vá hằng này đã bị gỡ. Số 0 trên head mới không áp ngược được cho head cũ.

3. **Số thứ tự: neo được một chuỗi BỐN đợt cụ thể nếu định nghĩa hình dạng là “lỗi đo bị báo thành vi phạm của receipt”.** Các neo là R4-02 tại `4ef73e6` (thiếu launcher); R5-01 tại `670071b` (bảng transport rỗng); finding connector tại `670071b`, vá trong `b7a53ba` (Git thao tác thứ sáu trả 127 bị gọi là mỏ neo trỏ hụt); R7-01 tại `ca960160` (nguồn hỏng vẫn suy không hợp đồng, cùng các ô sai kiểu). Đã đọc verdict và `git show b7a53ba -- ops/bien_nhan_v2.py` để xác minh các neo lịch sử này; không khai đã chạy lại toàn bộ các phiên lịch sử. **Không tìm được đợt thứ năm theo định nghĩa đó trong hồ sơ được đối chiếu.** R6-02 là thiếu dữ liệu nguồn nhưng báo sạch; R3-02 là thiếu độ phủ, không phải thêm một lần sản phẩm kết tội oan. Nếu gộp cả crash, mất trạng thái và lỗi giàn đo vào “cùng hình dạng” thì phải định nghĩa và lập danh sách lại. Bỏ số thứ tự là lựa chọn biên tập chấp nhận được; “không neo được” quá tuyệt đối. Hai số vẫn còn ở docstring `_muc_cam_theo_provider` và README, nên CHANGELOG chưa làm hồ sơ hết mâu thuẫn.

**Bộ ba `("human", "manual_audit", "human")` đúng nguyên hàng Human Auditor của kế hoạch đa provider §2.** Trên sáu hợp đồng hiện tại, phân vùng bằng transport cho kết quả phù hợp hàng ấy và c41. Nhưng §8 không định nghĩa định lý tổng quát “transport human ⇔ reviewer là người”; hai câu neo chỉ nói về mức review. Đây là quy ước diễn giải mới, không phải phép xác minh danh tính. Một provider tương lai có tập transport đúng `{human}` sẽ vào nhánh người; tập transport hỗn hợp sẽ vào nhánh mô hình. Chưa có hàng tương lai/hỗn hợp đó trên head này, nên không biến giả thuyết thành P1/P2 sản phẩm. Khi mở rộng nguồn, nên khai vai reviewer/policy assurance tường minh trong dữ liệu có cấu trúc, thay vì để transport tự quyết định vai; phải có ca cho vai chưa biết và hợp đồng hỗn hợp. Không nâng hai audit lịch sử đang là nợ.

## Findings

### R8-01-neo-protocol-che-nhau  [P2]  Xóa cả hai câu neo cùng lúc làm test mù khi mất riêng một chốt

TỆP/DÒNG: `cay-kho/ops/bien_nhan_v2_test.py:905` (`_cay_guong`, lấy danh sách neo từ module sản phẩm), `:1068–1071` (hàng PROTOCOL của c28). Chốt sản phẩm tại `cay-kho/ops/bien_nhan_v2.py:322`.

VẤN ĐỀ: c28 có một hàng làm mất **cả hai** neo PROTOCOL; `_ghi_nguon` xóa mọi câu lấy từ `_NEO_LUAT_CHEP_TAY` của chính sản phẩm. Bỏ kiểm riêng một luật thì luật kia vẫn làm hàng đó đỏ. c41 đối chiếu hằng assurance nhưng không kiểm phụ thuộc vào từng neo. Vì vậy lời khai “từng câu neo” không đúng với khả năng phân biệt của ma trận. Đây là độ phủ hồi quy của phần mới, không phải khẳng định hai chốt đang vắng trên bản nguyên gốc.

PHẢN CHỨNG ĐÃ CHẠY: từ `cay-kho/`, chạy `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/rv13-review/mutations.py`. Hai bản sao, mỗi bản chỉ thêm một nhánh `continue` trong vòng `for luat, tep, cau in _NEO_LUAT_CHEP_TAY`, lần lượt khi `luat == "ASSURANCE_CUA_NGUOI"` và `luat == "ASSURANCE_CUA_MO_HINH"`. **Cả hai rc=0; 45/45 ca, 57/57 mutant thường, 2/2 tự kiểm, 39/57 đối chứng; TỔNG: ĐẠT**, không lỗi giàn giáo.

Để loại mutant tương đương, chạy tiếp `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/rv13-review/anchor_witness.py`, dùng nguyên hai receipt của `_cay_guong`, chỉ xóa riêng câu có sẵn trong bản sao PROTOCOL:

| Câu bị xóa | Sản phẩm gốc | Bỏ chốt người | Bỏ chốt mô hình |
|---|---:|---:|---:|
| Neo `ASSURANCE_CUA_NGUOI` | rc=2 | **rc=0, TỔNG: ĐẠT** | rc=2 |
| Neo `ASSURANCE_CUA_MO_HINH` | rc=2 | rc=2 | **rc=0, TỔNG: ĐẠT** |

Như vậy mỗi mutant thực sự bỏ một hành vi fail-close, không chỉ đổi thông báo. Mã tái lập ở phụ lục.

GỢI Ý VÁ: trong test, thêm bảng oracle độc lập gồm ba bộ `(tên_luật, tệp, câu_neo)` hiện hành; không lấy bảng này từ `bnv2._NEO_LUAT_CHEP_TAY`. Mở `_cay_guong` để xóa **một neo được chỉ định**, hoặc dùng `sua_protocol` hiện có. Tách hàng PROTOCOL thành hai lượt: mỗi lượt chỉ mất một câu, giữ câu kia nguyên byte. Assert mẫu xóa khớp đúng một lần, rc=2, thông báo nêu đúng tên luật, không có `TỔNG: ĐẠT`, không kết tội receipt. Giữ ca đủ nguồn và ca mất cả tệp. Thêm hai mutant `continue` như phép đo; không cần đổi parser sản phẩm chỉ để khóa lỗi test này.

CA TEST KHOÁ: hai hàng đơn lẻ trên phải giết độc lập hai mutant; c18/đủ nguồn vẫn sạch khi mutant còn hiệu lực. Một phép xóa mục khỏi bảng neo sản phẩm cũng phải bị oracle độc lập phát hiện, thay vì kéo fixture co theo.

BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ: chép oracle nhưng tiếp tục cho builder lấy câu từ sản phẩm vẫn giữ phụ thuộc vòng; chỉ thêm mutant bỏ toàn bộ vòng lặp vẫn không phân biệt từng neo. Oracle câu chữ cần cập nhật cùng thay đổi protocol có chủ ý. Khóa từng câu không giải quyết ngữ nghĩa substring khi câu thành ví dụ/trích dẫn.

ĐỘ TIN: cao; hai mutant sống qua toàn suite và có witness hành vi đối xứng.

### R8-02-ket-luan-lop-quyen-vuot-phep-do  [P3]  CHANGELOG gọi suy luận loại trừ là phép đo lớp quyền CLI

TỆP/DÒNG: `cay-kho/CHANGELOG.md:372–379`; đối chiếu `cay-kho/.claude/hooks/pretooluse_guard.py:947–948` và `BAO_CAO_EXECUTOR.md` §0.

VẤN ĐỀ: đoạn mới viết “đo ba lớp” nhưng chỉ có hai phép thử, rồi khẳng định lớp thứ ba bằng loại trừ. Hai phép đó không tạo một tập nguyên nhân đầy đủ; cũng không tái hiện đúng lời gọi Edit, môi trường, policy và phiên đã bị từ chối. `rc=0` của hook tự nó còn không có nghĩa allow: hook trả 0 cả khi xuất `permissionDecision: ask`.

PHẢN CHỨNG ĐÃ CHẠY: `python3` gọi hook bằng `subprocess.run`, gửi JSON `tool_name: Edit`, `tool_input.file_path` trỏ launcher thật → **rc=0, stdout/stderr rỗng**. Đọc mã xác định nhánh trả trước khi xét đường dẫn. Đối chứng chỉ gửi vào hook một lệnh `golden-test --write` dưới tên tool Bash, không thi hành lệnh ấy → **rc=0, stdout có `permissionDecision: ask`**. Chép launcher vào cây tạm rồi đọc/ghi lại cùng bytes → byte-match. **KHÔNG ĐO ĐƯỢC quyết định từ chối CLI của phiên executor gốc**; không ghi thử lên cây review hay gọi lại phiên model để suy đoán nguyên nhân.

GỢI Ý VÁ: thay đoạn CHANGELOG bằng hai kết quả có phạm vi và một giả thuyết: “đường ghi Python đo được; hook này không yêu cầu chặn Edit trong payload đã thử; nghi vấn lớp quyền CLI, chưa có trace quyết định của phiên gốc”. Bỏ “đo ba lớp” và khẳng định executor đã sai lớp. Muốn kết luận CLI thì bổ sung log quyết định trực tiếp có phiên/version/policy/tool/path tương ứng; không lấy việc đổi công cụ ghi được làm bằng chứng cho quyết định của công cụ trước.

CA TEST KHOÁ: kiểm hồ sơ có log dương cho thành phần được quy nguyên nhân; bản sửa prose từ “nghi vấn” thành “đã đo CLI chặn” mà không có log phải bị review bác. Không thêm test khớp câu chữ, không yêu cầu tái tạo một từ chối không còn môi trường gốc.

BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ: đổi nhãn từ CLI sang “nền” mà không thu hẹp độ chắc chắn chỉ chuyển lỗi sang tên khác. Không khái quát một lần Edit qua hook thành “mọi hook/đường ghi đều cho phép”.

ĐỘ TIN: cao về giới hạn logic và hành vi hook đã chạy; chưa xác định nguyên nhân từ chối lịch sử.

### R8-03-so-hang-va-mau-so-khong-cung-phep-do  [P3]  Bảng sửa lời khai vẫn đếm nhầm đối chứng và đổi mẫu số receipt

TỆP/DÒNG: `cay-kho/CHANGELOG.md:352–356`, `:411`, `:445–447`; cùng câu “cả sáu rc=2” trong `BAO_CAO_EXECUTOR.md` §1.

VẤN ĐỀ: bảng nguồn của reviewer có **sáu lượt, gồm một đối chứng và năm nguồn hỏng**, không phải sáu nguồn hỏng đều rc=2. Bảng transport so `1/15` receipt **đạt** ở mốc cũ với `2/17` tệp **tự khai v2** ở mốc mới. Sau đó văn bản còn nói `1/15` “không khớp”, dù đây đúng là số trên tập đạt cũ. Phép bác tên chép tay đúng không chứng minh số transport cũng sai. Số kill m49 “11 receipt thật” cũng cần neo về tập 68 receipt của executor, không gán cho tập hiện hành 69 receipt.

PHẢN CHỨNG ĐÃ CHẠY: replay `source_probe.py` của R7, chỉ bổ sung chép nguồn PROTOCOL mới → **baseline rc=0; năm biến thể hỏng đều rc=2, 0 vi phạm, không traceback**, trên 69 receipt. Đếm bằng `git ls-tree` + `git show` + `yaml.safe_load`: `4488ff1` có **68 receipt, 16 tự khai v2, 1 khai transport**; head này có **69 receipt, 17 tự khai v2, 2 khai transport**. Chạy gate head này → **16 đạt v2**. Các receipt khai transport là lượt 6 ở mốc cũ, lượt 6 và 7 ở mốc mới. Trích lambda m49 từ AST rồi chạy c40 khi mutant còn hiệu lực → `giet_that`, thông báo **“thiếu launcher.py: 12 biên nhận THẬT bị KẾT TỘI vì lỗi ở NGUỒN”**. Không phải 11 trên head này.

Đối chiếu thêm bằng bộ kiểm tại head này trên byte receipt lấy từ từng mốc: 15 receipt đạt/1 có transport ở tập `4488ff1`, 16/2 ở tập HEAD; mỗi tập có đúng một receipt tự khai v2 thuộc nợ đóng băng (`bien-nhan-review-s2-review-4-codex-verdict.receipt.yaml`). Đây là kiểm lại tập hiện vật lịch sử bằng cổng hiện hành, không phải tuyên bố đã chạy lại executable cũ của `4488ff1`.

GỢI Ý VÁ: sửa câu nguồn thành “1 đối chứng rc=0; 5 nguồn hỏng rc=2; cả 6 không có vi phạm/traceback”. Tách transport thành hai hàng có cùng đơn vị qua hai mốc: “trên tệp tự khai v2: 1/16 → 2/17”; “trên receipt đạt v2: 1/15 → 2/16”. Bỏ kết luận `1/15` sai, giữ phép bác `0 tên chép tay` trên mốc cũ. Với m49 ghi rõ “11 trên tập executor 68 receipt; đo lại head hiện hành là 12 trên 69”. Không sửa các số lịch sử đã có head đúng thành số hiện tại. Khi sửa CHANGELOG, tái sinh manifest theo quy trình kho và chạy release-verify; không chỉnh golden chỉ để khớp prose.

CA TEST KHOÁ: đối chiếu từng số hạng, tập mẫu và head bằng truy vấn Git/YAML; khi replay nguồn phải in nhãn từng lượt cùng rc. Bản báo cáo gộp baseline vào nhóm nguồn hỏng, hoặc đổi mẫu số “đạt” thành “tự khai” không ghi đơn vị, phải bị bác. Không cần thêm assertion cố định 69 receipt hay 12 lỗi vào suite: số đó sẽ đổi khi thêm receipt hợp lệ.

BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ: thay 11 bằng 12 khắp lịch sử làm mất tính đúng của số tại head cũ. Tái đóng băng số lượng hiện vật trong test cũng có thể chặn oan receipt mới. Hai tập receipt khác nhau dù chênh đúng một phần tử.

ĐỘ TIN: cao.

## Phần bản vá đã được đo và các vùng mỏng

| Hạng mục | Kết quả |
|---|---|
| R7-01 | Năm nguồn hỏng trong script R7 nay rc=2, không kết tội, không crash import. c28 có 34 hàng và lượt hỗn hợp; c40 chạy receipt thật. m46–49 bị bắt trong suite. |
| R7-02 | Hàng human đúng nguồn §2; c41 dương, âm và evidence chưa có verifier đều chạy. m50–52 bị bắt. Chỉ chứng minh hợp đồng/khai báo, không xác thực audit thật. |
| R7-03 | m54/m55 bị bắt; `rig_probe.py` dừng bằng `LoiDungCa` do byte launcher lệch, trước ca đích; m53 tự kiểm đúng `gian_giao`. 11 hằng parity có thật. Còn R8-01. |
| R7-04 | `path_probe.py` nguyên từ verdict R7: m43 hiện hành làm fixture sai được nhận **0 lỗi/1 đạt** trước khi c37 giết ở assertion chấp nhận sai; c18 vẫn sạch. Không lấy đổi thông báo làm bằng chứng. |
| R7-05 | Header receipt lượt 6 nay phân đúng ba loại. Verdict lượt 6 không đổi byte so với b912e5f, SHA-256 khớp receipt. |

**Chín nhóm c28 không có mutant riêng:** danh sách prose của executor nở thành **11 hàng**, vì nhóm arity và nhóm đích bí danh mỗi nhóm có hai hàng. Tôi đã chạy từng hàng hiện có với một phép làm yếu sản phẩm trên bản sao (`row_teeth.py`): cả 11 đều vi phạm ít nhất một assertion của c28. Chín lượt đổi mã thoát hoặc làm crash; **hai lượt bỏ kiểm kiểu ở đích bí danh vẫn rc=2 do kiểm đích tồn tại phía sau, và chỉ thiếu thông báo kiểu mong đợi**. Hai lượt đó là răng diagnostic, không phải bằng chứng dữ liệu sai được nhận. Không có cơ sở nói một trong 11 hàng “không thể đỏ”; cũng không biến việc thiếu mutant riêng cho từng hàng thành finding. Khoảng trống đo được nằm ở hai neo bị xóa chung, ngoài 11 hàng này.

**Substring PROTOCOL:** mất riêng mỗi câu đang làm sản phẩm gốc rc=2, đã đo. Tôi chưa dựng phép đổi câu thành trích dẫn/ví dụ; không chứng minh parser hiểu hiệu lực pháp quy của prose. Nếu cần bảo đảm vị trí/ngữ nghĩa, điều phối phải cung cấp ca nguồn cho câu còn hiện diện nhưng không còn là điều khoản hiệu lực; hướng vá là nguồn policy có cấu trúc hoặc ràng buộc vùng điều khoản có thẩm quyền. R8-01 chỉ khóa hai phụ thuộc hiện có.

**Lược đồ chặt:** tuple literal, một assignment module, ô chuỗi không thừa khoảng trắng là giới hạn thực sự của reader. Một refactor Python hợp lệ, ví dụ chuyển sang assignment có type annotation, có thể bị reader từ chối. Head này dùng đúng dạng reader hỗ trợ; chưa có sửa nguồn hợp lệ trong diff bị bắt oan. Đây là hợp đồng tương thích cần ghi rõ khi sửa launcher, không phải lý do bỏ fail-close hay báo P1 giả định. AST tĩnh cũng không chứng minh giá trị runtime nếu tương lai có phép cập nhật bảng sau khai báo.

**Parity:** so bytes ba nguồn phụ và replay receipt qua hai builder đã chạy; không thấy lệch tự phát trên Linux. Nó vẫn là snapshot hữu hạn: c42 so `_mri`/`_thieu`, không chứng minh toàn bộ CLI/Git/IO/cleanup tương đương; `_dot_bien_tep` còn đọc/ghi mã cổng bằng text. Không có phép đo Windows thật, CRLF của bản vá này trên Windows, hay mọi nguồn có thể thêm sau này. Không gọi các giới hạn ấy là regression đã tái hiện.

## Cổng chạy lại

Các lệnh Python dưới chạy từ `cay-kho/` với `PYTHONDONTWRITEBYTECODE=1`; mã thoát được lấy trực tiếp từ tiến trình, không từ pipeline.

| Lệnh | rc và bằng chứng dương |
|---|---|
| `python3 ops/bien_nhan_v2_test.py` | 0; 45/45 ca, 57/57 mutant thường, 2/2 tự kiểm, 39/57 khai đối chứng; TỔNG: ĐẠT |
| `python3 ops/bien_nhan_v2.py --root .` | 0; 16 đạt, 11 miễn trừ, 42 nợ, 0 vi phạm, 0 chưa đo, tổng 69 |
| `python3 .claude/dev/ci_dang_ky_test.py` | 0; 51/51 phản chứng, TỔNG: ĐẠT |
| `python3 .claude/dev/launcher_test.py` | **0 nhưng thiếu phép đo**: 173/173 đã chạy qua, tổng 182, bỏ qua 9, hỏng 0. Một ca Windows, tám ca không dựng được venv/pip. Không tái lập 181/181 của EVIDENCE. |
| `python3 ops/lease_publish_test.py` | 0; 121/121, bỏ qua 0 |
| `python3 .claude/dev/packet_loop_test.py` | 0; nền 278/278, bỏ qua 0; TỔNG: ĐẠT |
| `python3 .claude/dev/idiom_py_test.py` | 0; TỔNG: ĐẠT |
| `python3 .githooks/eol_policy_test.py` | Mặc định rc=1: dựng fixture vướng ký commit qua dịch vụ bị sandbox chặn. Chạy lại với cấu hình tiến trình nêu dưới: **rc=0, 30/30**. |
| `python3 .githooks/pre_push_test.py` | Mặc định rc=1, 0/9 do cùng lỗi dựng commit fixture. Chạy lại với cấu hình tiến trình: **rc=0, 9/9**. |
| `python3 ops/cong_cu_test.py` | 0; 23 ca, 18 mutant, 0 lỗi mutant |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0; 7 tệp, 0 chỗ chép doctrine |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0; 46 ADR/46 dòng; có ngoại lệ trạng thái `0016` như stdout khai |
| `python3 scripts/tl.py golden-test --json` | 0; `ok=true`, `case_count=20`, danh sách có 20 ca |
| `python3 scripts/tl.py doc-claims-check --strict --json` | 0; `ok=true` |
| `python3 scripts/tl.py determinism-audit --strict --json` | 0; `ok=true` |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0; `ok=true`, checked=180, failed/extra rỗng, package_hash_match=true |
| `git diff --check` | 0, không lỗi whitespace |

Hai lượt test Git chạy lại chỉ thêm vào môi trường tiến trình: `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`. Không sửa global config, cấu hình repo hay nguồn test. Đã đọc cấu hình gốc: `commit.gpgsign=true`, chương trình ký `/tmp/code-sign`; stderr của fixture ghi socket dịch vụ ký bị cấm. Kết quả sau điều chỉnh không được trình bày như lệnh mặc định vốn xanh, và lỗi dựng fixture không chứng minh lỗi mới của diff này.

## Phụ lục tái lập R8-01

Hai script đã chạy ở `/tmp/rv13-review/mutations.py` và `/tmp/rv13-review/anchor_witness.py`. Lưu mã sau ngoài repository, chạy từ `cay-kho/` với `PYTHONDONTWRITEBYTECODE=1 python3 <script>`. Script chỉ chép nguồn/receipt, đột biến mã trong cây tạm và dùng Git gốc cho truy vấn đọc; không ghi vào cây được review. Hai lượt suite cần thời gian tương đương hai lượt suite thường.

```python
import importlib.util, json, os, shutil, subprocess, sys, tempfile
from pathlib import Path
sys.dont_write_bytecode = True
R = Path.cwd()
S = (R / 'ops/bien_nhan_v2.py').read_text()
old = '    for luat, tep, cau in _NEO_LUAT_CHEP_TAY:'
assert S.count(old) == 1
spec = importlib.util.spec_from_file_location('t', R / 'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(spec)
spec.loader.exec_module(t)
for law in ('ASSURANCE_CUA_NGUOI', 'ASSURANCE_CUA_MO_HINH'):
    new = old + '\n        if luat == ' + repr(law) + ':\n            continue'
    with tempfile.TemporaryDirectory(prefix='r8-mutant-') as td:
        d = Path(td)
        shutil.copytree(R / 'ops/reviews', d / 'ops/reviews')
        for rel in ('AGENTS.md', 'docs/PROTOCOL_DA_PHIEN.md',
                    '.claude/dev/launcher.py', 'ops/bien_nhan_v2_test.py'):
            (d / rel).parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(R / rel, d / rel)
        (d / '.git').write_text('gitdir: ' + str(R / '.git') + '\n')
        mutant = S.replace(old, new)
        (d / 'ops/bien_nhan_v2.py').write_text(mutant)
        p = subprocess.run([sys.executable, str(d / 'ops/bien_nhan_v2_test.py')],
                           capture_output=True, text=True,
                           env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        print(law, 'suite_rc', p.returncode, p.stdout.splitlines()[-2:])
        sentence = next(c for k, _, c in t.bnv2._NEO_LUAT_CHEP_TAY if k == law)
        for label, code in (('baseline', S), ('mutant', mutant)):
            with tempfile.TemporaryDirectory(prefix='r8-witness-') as wt:
                w = Path(wt)
                gate = t._cay_guong(w, sua_protocol=lambda v: v.replace(sentence, ''))
                gate.write_text(code)
                q = subprocess.run([sys.executable, str(gate), '--root', str(w)],
                                   capture_output=True, text=True)
                print(law, label, q.returncode, q.stdout, q.stderr)
```

Kết quả đo riêng các hàng c28 và toàn bộ log cổng còn tại `/tmp/rv13-review/row_teeth.json`, `checks.json`, `source_probe.log`, `path_probe.log`, `rig_probe.log`; log suite gốc tại `/tmp/rv13-bien-test.log`. Các đường dẫn tạm là hiện vật của phiên này; bằng chứng cốt lõi và hình dạng bản vá đã ghi ngay trong verdict để không phụ thuộc việc chúng tồn tại ở phiên sau.

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

**ĐÃ ĐO:** exact HEAD/tree và trạng thái sạch; 34 hàng c28/11 hằng parity; các cổng và rc trong bảng; replay ba script R7; hai mutant neo luật sống cùng witness thay đổi hành vi; 11 phép thử hàng nguồn thiếu mutant riêng với phân biệt răng hành vi/diagnostic; m49 hiện hành; số receipt/transport tại hai mốc; byte/hash verdict lượt 6; hành vi hook với Edit và đối chứng ask. Đã đối chiếu hồ sơ lịch sử để định nghĩa chuỗi bốn đợt, không chỉ tin số thứ tự executor/điều phối.

**KHÔNG ĐO ĐƯỢC:** GitHub trực tiếp, head PR từ xa, `gate`/required checks hiện thời, bằng chứng Windows của head này, protection/land authority, provenance model/session, audit người thật, quyết định permission CLI của phiên executor gốc. **Không chạy:** full release selftest/workflow-audit, release-bundle hai lượt, toàn suite hook, LIVE/merge/deploy. Tám ca launcher phụ thuộc dựng venv/pip và một ca Windows bị bỏ qua; không coi `rc=0` của suite ấy là đủ 182 ca. Không suy CI xanh hoặc đỏ từ việc sandbox không đọc được CI. Những P2/P3 trên cần được ghi nhận theo authority của người giữ; verdict này không tự yêu cầu một vòng review thứ chín.

verdict: approve_with_findings
