# Cross-review vòng 7 — PR #455

**approve_with_findings — 4 P2, 1 P3; không chứng minh P0/P1 mới.** Hai phản chứng assurance/surface của R6-01 đã bị khóa thật; đường mất surface Web của R6-02 đã được loại bỏ. Bản vá mới còn lỗi xử lý nguồn, chặn quá rộng đối với Human Auditor, và thiếu bằng chứng cho một phần các chốt mới. Không nâng các lỗi này thành P1 để kéo dài review.

- `reviewed_sha`: `ca960160b477cd16346a293aaa8752772a9921d4`
- `reviewed_tree`: `12d89e44e117c283186e66a1d27d81a47c7a5820`
- Base diff: `5a78c150106ae381461354c77ba2023834330bbd`, tree `2e42173bfadd3869dfcc40ca2734723172fb58eb`; base là tổ tiên HEAD, `git merge-base --is-ancestor`: rc=0.
- Phạm vi: `git diff 5a78c150106ae381461354c77ba2023834330bbd HEAD`, 8 tệp, +845/−221. Axes: `spec`, `standards_security`. Review Class: `sensitive`, do cổng identity/evidence và launcher.
- Reviewer: `openai_codex`, Codex service/API với shell trong Linux container, transport `machine`. Chỉ thị phiên định danh agent GPT-6; backend/model version không có chứng thực độc lập. Không khai một run CLI đã được launcher chứng thực. Context độc lập với Executor Claude.
- Authority: yêu cầu trực tiếp của user giao vòng 7, exact head/base, write set duy nhất `VERDICT.md`. Không có Packet revision/spec hash/generation/lease riêng để xác minh; không tự cấp chúng. Chỉ thị này giao review hiện tại, không cấp quyền chuyển state, vòng kế tiếp, GitHub approval hoặc land.

Preflight đã tự đo: origin `https://github.com/ducthangho/tra-luat`; detached; `is-shallow-repository=false`; **1.748 commit**; worktree ban đầu sạch; `core.abbrev=7`. Đã đọc CONTEXT, protocol, CLAUDE, kế hoạch đa provider, sáu verdict lịch sử và diff hiện tại. Phạm vi không thay legal/corpus/runtime skill; không dùng execution surface AG hoặc ChatGPT Web.

Các gate chạy trong clone tạm độc lập tại `/tmp/pr455-r7-5kW5ZW/baseline`, cùng HEAD/tree, cấu hình `core.abbrev=7`. Phản chứng chỉ dùng fixture/receipt có sẵn và đột biến mã hoặc nguồn bảng trên bản sao ngoài cây review. **Không soạn payload receipt/văn bản tấn công mới.** Không sửa tệp tracked, không commit/push.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding/chốt vòng 6 | Kết quả tự đo |
|---|---|
| R6-01: chỉ cấm `cross_approved` | **ĐÃ VÁ THẬT phản chứng này.** Chèn `cam &= {"cross_approved"}` trước `if khai in cam`, giữ neo mutant nội bộ: rc=1, **40/41**, c36 chỉ ra hai nhánh còn lọt; 48/48 mutant nội bộ vẫn chạy. |
| R6-01: chỉ kiểm surface cho hai provider | **ĐÃ VÁ THẬT phản chứng này.** Đặt `hd=None` cho provider ngoài Web/Codex ngay trước điều kiện kiểm: rc=1, **39/41**, c36 chỉ ra ba provider, c38 cũng bắt alias; không lấy lỗi giàn giáo làm kill. |
| R6-01: hai literal `CONG_CU`/`KHA_NANG` | **ĐÃ VÁ THẬT bằng thay nguồn.** Replay phép xóa riêng từng literal: rc=0, 1 receipt fixture đạt, 0 vi phạm/0 chưa đo; vẫn đủ 5 hợp đồng. Hai literal không còn cấp provider nên hai guard cũ không còn nghĩa vụ. |
| R6-02: xóa riêng dòng surface Web | **ĐÃ VÁ THẬT phản chứng cũ.** Replay `sources.py` của R6, thích nghi tên bản đồ: xóa `execution_surface: chatgpt_web` khỏi AGENTS vẫn giữ 5 hợp đồng, rc=0, 1 đạt/0 vi phạm/0 chưa đo. **Bản vá sinh lỗi mới ở xử lý nguồn cấu trúc:** R7-01; chưa khóa hết đường đối chiếu mới: R7-03. |
| R6-03: mô tả “bộ ba” khi chưa đọc transport | **Đã thêm phép so transport dạng chuỗi khi khai.** c36/m41 chạy qua; không coi đó là kiểm transport bắt buộc hoặc xác thực transport thực tế. Trên head này có **1/15** receipt đạt v2 khai transport, không phải 0/15. |
| Connector: bí danh trước phép kiểm | c38/m40 qua. `_chuan_hoa_provider` được dùng ở `_mri` và `_thieu`; alias `anthropic → anthropic_claude`. Không tái hiện đường mượn surface trên fixture có sẵn. |
| Connector: đường dẫn tuyệt đối/`..` | c37 qua; khôi phục `.lstrip("./")` trên bản sao làm c37 đỏ vì receipt được nhận sai, đối chứng c18 vẫn sạch. **Bản vá sản phẩm đóng phản chứng**, nhưng m43 hiện tại đo khác lời khai: R7-04. |

## Findings

### R7-01-nguon-hong-thanh-ket-toi  [P2]  Nguồn hợp đồng hỏng vẫn thành vi phạm receipt hoặc crash lúc import

**TỆP/DÒNG:** `ops/bien_nhan_v2.py:178` (`_provider_chinh_tac._bang`), `:209–231` (nạp các cột/bí danh), `:556–574` (`_thieu`, đặc biệt `if prov and prov not in PROVIDER_HOP_DONG`).

**VẤN ĐỀ:** Bảng có cấu trúc chưa được kiểm đủ cấu trúc. `_bang` trả hàng bất kỳ số cột; hai vòng unpack alias nằm ngoài khối bắt lỗi. Kiểm kiểu chỉ áp cho tên provider, bỏ surface/transport. Đồng thời, khi đọc nguồn thất bại, `_HD={}` làm mọi provider thành “không hợp đồng”; chốt mới trong `_thieu` vẫn kết luận assurance sai dù `PROVIDER_NGUON_HONG` đã có lỗi. Đây là cùng hình dạng **lỗi đo bị biến thành lỗi dữ liệu**, tái xuất ở cả nơi tạo và nơi dùng kết quả nguồn.

**PHẢN CHỨNG ĐÃ CHẠY:** `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr455-r7-5kW5ZW/source_probe.py` → rc=0, `SOURCES_COMPLETE`. Script chỉ sửa nguồn ở cây tạm rồi gọi `python3 <cây-tạm>/ops/bien_nhan_v2.py --root <clone-review>`, đọc **68 receipt nguyên byte**:

| Biến đổi nguồn | rc CLI | Kết quả thật |
|---|---:|---|
| Đối chứng đầy đủ | 0 | 15 đạt, 11 miễn trừ, 42 nợ, 0 vi phạm/0 chưa đo |
| Thiếu riêng launcher.py | 2 | **11 vi phạm oan**, 1 chưa đo; thông báo kết tội `openai_codex`/`anthropic` không hợp đồng |
| Hàng `_PROVIDER_BI_DANH` mất cột đích | 1 | stdout rỗng, `ValueError: ... expected 2, got 1`, crash lúc import |
| Hàng `_BE_MAT_BI_DANH` mất cột đích | 1 | cùng crash tại vòng unpack riêng |
| Transport Codex trong bảng thành `None` | 1 | 1 receipt nguyên byte bị kết tội; **0 chưa đo**, hợp đồng được báo là `[None]` |
| Surface Codex trong bảng thành `None` | 1 | 9 receipt nguyên byte bị kết tội; **0 chưa đo** |

c28 nguyên bản vẫn qua vì cây gương dùng `_bn_neo` không khai assurance; không chạm nhánh kết tội mới. Đây không phải bằng chứng receipt giả được duyệt trên cây nguyên bản, nên P2.

**GỢI Ý VÁ:** Hai phần phải cùng đóng. (1) Cho `_bang` nhận schema từng bảng: 4 cột với `_TRANSPORT_CONTRACTS`, 3 với `_PROVIDER_NGOAI_CLI`, 2 với mỗi bảng alias. Kiểm arity trước unpack; provider/surface/transport và hai đầu alias phải là chuỗi không rỗng; kiểm đích alias tồn tại đúng miền. Trả lỗi có tên bảng/hàng/cột qua `_provider_chinh_tac`, không để lỗi dữ liệu nguồn thoát lúc import. Có thể dùng `ast.literal_eval` cho literal rồi validate, không thực thi launcher. (2) Trong `_thieu`, chỉ suy giới hạn theo provider/hợp đồng **khi nguồn đã đo được**; nguồn lỗi phải giữ `chua_do` của `kiem`, không sinh lời kết tội “không có hợp đồng”. Giữ các kiểm kiểu/SHA/identity độc lập với nguồn và giữ rc=2; không chữa bằng map dự phòng.

**CA TEST KHOÁ:** Dùng lại 68 receipt nguyên byte hoặc một receipt `cross_approved` đang đạt như receipt R6 cho ca nguồn hỏng, ngoài fixture tối thiểu hiện tại. Các hàng bảng trên phải cho rc=2, lý do đúng nguồn, không traceback và không thêm vi phạm do hợp đồng. Mutant bỏ kiểm arity của **từng** bảng alias, bỏ kiểm kiểu surface/transport, và bỏ điều kiện nguồn-là-dùng-được tại `_thieu` phải chết độc lập. Receipt sai thực sự trong một lượt lỗi hỗn hợp vẫn được báo sai ở kiểm không phụ thuộc nguồn.

**BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ:** Chỉ bọc unpack sẽ còn 11 cáo buộc oan; chỉ thêm guard trong `_thieu` sẽ còn crash và `[None]`. Bắt mọi `Exception` rồi trả dữ liệu rỗng sẽ che lỗi lập trình. Bỏ mọi kiểm khi nguồn lỗi lại che vi phạm độc lập. Không đổi “chưa đo được hợp đồng” thành “provider được miễn kiểm và cổng xanh”.

**ĐỘ TIN:** cao; phản chứng chạy trên dữ liệu hiện hữu, không sửa receipt.

### R7-02-human-bi-cam-audit  [P2]  Hằng “không hợp đồng” loại luôn đường Human Audit mà protocol cho phép

**TỆP/DÒNG:** `ops/bien_nhan_v2.py:264–274`, `:562–574`; `.claude/dev/launcher.py:163–167`; test tại `ops/bien_nhan_v2_test.py:1287–1296`. Nguồn đối chiếu: `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md:34`, `docs/PROTOCOL_DA_PHIEN.md:508` và `:609`.

**VẤN ĐỀ:** Câu “`human` là provider KHÔNG có hợp đồng nào trong kho” không đúng với bảng provider chuyển tiếp: bảng ấy đã khai `human / manual_audit / human`. Protocol §8 cho `human_audited` với audit độc lập, có evidence bền trên exact SHA. Nhưng hằng chép tay chỉ giữ tên `human` ở allowlist; `_thieu` cấm toàn bộ `ASSURANCE_CAN_DOC_LAP`, trong đó có chính `human_audited`. Vì vậy mọi receipt v2 mới khai đúng provider human và mức này đều bị nhánh mới loại, bất kể bổ sung bằng chứng gì. Hai audit lịch sử trong nợ không chứng minh đường mới hoạt động.

**PHẢN CHỨNG ĐÃ CHẠY:** `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr455-r7-5kW5ZW/inspect.py` → rc=0, `INSPECTION_COMPLETE`; `HUMAN_BRANCH = {allowed_name: true, has_contract: false, human_audited_in_no_contract_ban: true}`. Đọc các điều khoản trên và nhánh `_thieu` xác định đường cấm vô điều kiện theo tên. **KHÔNG ĐO ĐƯỢC một receipt v2 human-audit hợp lệ end-to-end:** cây không có fixture ấy và lượt review bị cấm tự soạn nội dung attestation mới. Không khai hai receipt human lịch sử đã bị cổng nguyên bản từ chối; chúng vẫn là nợ đóng băng.

**GỢI Ý VÁ:** Đưa hợp đồng Human Auditor vào nguồn cấu trúc chính tắc, với bộ ba đã khai `human / manual_audit / human`; loại `human` khỏi tập “không hợp đồng”. Đồng thời biểu diễn policy assurance của vai auditor trong nguồn có cấu trúc và cho `_thieu` đọc: mức có thẩm quyền của human là `human_audited`, không tự cấp `cross_approved`/`same_provider_approved`. Sửa c36 đang lấy `sorted(PROVIDER_KHONG_HOP_DONG)[0]` làm đại diện; tập này có thể rỗng sau khi hợp nhất nguồn. Ca không-hợp-đồng có thể dùng fixture Codex có sẵn với map hợp đồng bị gỡ riêng trong module tạm. Cập nhật oracle policy tương ứng, vẫn đòi độc lập/evidence; nếu chưa có verifier cho evidence human thì báo chưa đo được, không tuyên bố human không có thẩm quyền theo luật.

**CA TEST KHOÁ:** Executor/điều phối cung cấp fixture human-audit đầy đủ theo protocol, cùng ca thiếu độc lập và hai mức assurance dành cho model. Mutant đưa human trở lại cấm `human_audited` phải làm ca dương đỏ; mutant cấp mọi mức assurance cho human phải làm ca âm đỏ. Khi thiếu đường xác minh evidence, kiểm rõ trạng thái thứ ba. Lượt này chưa có phản chứng end-to-end cho các ca mới đó.

**BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ:** **Chỉ thêm tuple human mới đóng một nửa:** map hiện tại không tự giới hạn mức assurance, nên dễ mở nhầm hai mức model. Chỉ xóa nhánh cấm sẽ tái mở quyền cho provider chưa có hợp đồng. Không suy tên actor/GitHub submitter thành audit độc lập; không nâng hai bản ghi nợ lịch sử thành v2 bằng suy đoán.

**ĐỘ TIN:** cao về mâu thuẫn luật và nhánh cấm; chưa đo fixture v2 human hoàn chỉnh.

### R7-03-chot-nguon-va-parity-con-mu  [P2]  Ma trận nguồn và parity chưa khóa các phần mới của hợp đồng

**TỆP/DÒNG:** `ops/bien_nhan_v2_test.py:276` (`_dot_bien_tep`), `:890–944` (c28); chốt sản phẩm tại `ops/bien_nhan_v2.py:225`, `:245–252`.

**VẤN ĐỀ:** c28 chỉ thử mất bảng alias **provider**, không mất bảng alias **surface**; chỉ thử AGENTS lệch **transport**, không lệch **surface**. Parity vẫn so bốn hằng cũ, bỏ qua `PROVIDER_HOP_DONG`, `PROVIDER_BI_DANH` và trạng thái lỗi nguồn. Tên provider bằng nhau không bảo đảm các ràng buộc đi kèm bằng nhau.

**PHẢN CHỨNG ĐÃ CHẠY:** Trên mỗi cây tạm, giữ nguyên suite và mọi fixture, chỉ đổi đúng một đoạn sản phẩm rồi chạy `python3 <cây-tạm>/ops/bien_nhan_v2_test.py`:

```python
# A: giữ nguyên neo cũ, bỏ riêng phép đối chiếu surface của AGENTS
'            if g and g.group(1) not in hop_dong[ten][khoa]:'
# ->
'            if khoa == "be_mat":\n                g = None\n            if g and g.group(1) not in hop_dong[ten][khoa]:'

# B: bỏ riêng chốt thiếu bảng alias surface
'    if bd is None or bd_bm is None:'
# ->
'    if bd is None:'
```

**Cả A và B:** rc=0, **41/41 ca · 48/48 mutant thường · 1/1 tự kiểm · 30/48 đối chứng · TỔNG: ĐẠT**, không lỗi giàn giáo. Đây là độ phủ hồi quy thiếu, không khẳng định chốt nguyên bản hiện đã bị gỡ.

`PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr455-r7-5kW5ZW/rig_probe.py` → rc=0, `RIG_PARITY_COMPLETE`: bơm mất hàng `_BE_MAT_BI_DANH` vào **riêng bản launcher mà rig chép**, rồi gọi `_dot_bien_tep` với đột biến đường dẫn hiện có. Cả **4/4 hằng parity vẫn bằng nhau**, nhưng `PROVIDER_HOP_DONG` khác. Receipt `phan-bien-quy-trinh-review-1-claude-verdict.receipt.yaml` nguyên byte: `_mri` trên nguồn gốc trả `None`; trong gương lại từ chối `claude_code_cli`. Đây là phản chứng chốt parity, không phải phát hiện cây gương nguyên bản tự lệch trong lần chạy nền.

**GỢI Ý VÁ:** Mở c28 theo các thành phần của schema nguồn: mỗi bảng bắt buộc, mỗi cột đối chiếu, mỗi trạng thái nguồn phải có hàng riêng. Đưa các ca R7-01 vào cùng ma trận, không chỉ thêm hai mutant A/B. Trong `_dot_bien_tep`, kiểm byte hai nguồn phụ đã chép khi chúng không phải đích đột biến; bổ sung parity các map hợp đồng/bí danh và trạng thái lỗi, hoặc một snapshot chuẩn hóa chứa chúng. `_cay_guong` phải khai riêng phần nguồn cố ý thay. Mutant hợp lệ làm đổi map cần khai đúng phần miễn parity; không dùng cờ bỏ mọi parity.

**CA TEST KHOÁ:** A/B phải bị assertion ca nền bắt, với đối chứng đủ nguồn vẫn xanh. Ca rig bơm mất alias trên phải bị phân `LoiDungCa` trước khi chạy ca đích và không nhận “CÓ RĂNG”. Giữ một ca nguồn không đổi qua cả hai builder; đối chiếu hành vi bằng receipt lịch sử nguyên byte. Phần nội dung AGENTS lệch surface mới cần điều phối chuẩn bị fixture; reviewer chỉ đo phép làm yếu sản phẩm.

**BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ:** Thêm parity map một cách máy móc sẽ kết tội mutant đang cố ý sửa map (m20/m29/m39); cần khai delta cụ thể. So map lấy lại từ chính module lỗi vẫn không thay oracle độc lập. So byte phải tách nguồn cố ý sửa và chú ý việc `read_text/write_text` đổi newline trên Windows. **Chỉ vá ma trận sẽ còn rig mù; chỉ vá parity sẽ còn hai phép làm yếu qua toàn suite.**

**ĐỘ TIN:** cao về hai mutant sống và giới hạn parity đã bơm; chưa thấy lệch tự phát ở builder nguyên bản.

### R7-04-m43-giet-vi-cau-chu  [P2]  m43 chưa dựng lại lỗi chuẩn hóa đường dẫn mà nó khai đã khóa

**TỆP/DÒNG:** `ops/bien_nhan_v2_test.py:1336` (assert c37), `:1891–1896` (m43); `_neo_git` tại `ops/bien_nhan_v2.py:665–674`.

**VẤN ĐỀ:** m43 chỉ đổi guard absolute/`..` thành `False`, giữ normalizer mới. Guard so path với URL ngay sau đó vẫn từ chối fixture. c37 làm mutant chết vì **thông báo khác**, còn mô tả m43 nói đường dẫn được chuẩn hóa rồi lọt. Đối chứng dương không phát hiện được sai khác ý nghĩa này: cả hai kiểu từ chối đều giữ c18 sạch. Giống R2-04 về tín dụng đo sai thuộc tính, không phải crash tính thành kill.

**PHẢN CHỨNG ĐÃ CHẠY:** `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr455-r7-5kW5ZW/path_probe.py` → rc=0, `M43_TRACE_COMPLETE`. Script trích nguyên lambda m43 bằng AST, trace `kiem` bên trong **c37 có sẵn**, không đổi dữ liệu:

| Bản | Kết quả fixture có `../../` | c37 / đối chứng c18 |
|---|---|---|
| Nguyên bản | 1 lỗi, 0 đạt, lỗi đường dẫn tương đối | `qua` / sạch |
| m43 hiện tại | **vẫn 1 lỗi, 0 đạt**, chuyển sang “KHÔNG neo thứ nó khai” | `giet_that` / sạch |
| Khôi phục `.lstrip("./")` | **0 lỗi, 1 đạt**, nhận sai thật | `giet_that` / sạch |

c37 nguyên bản đã có khả năng bắt regression; thứ sai là mutant và lời giải thích tín dụng.

**GỢI Ý VÁ:** Thay phần biến đổi của m43 bằng việc khôi phục normalizer cũ, giữ nguyên c37 và đối chứng c18:

```python
lambda: _dot_bien_tep(
    '    khai_duong = str(d.get("verdict_path") or "").strip()',
    '    khai_duong = str(d.get("verdict_path") or "").strip().lstrip("./")')
```

Hình dạng này đã chạy trên cây tạm và cho hàng cuối của bảng. Đổi tên mutant thành tên nói rõ phục hồi `lstrip`. Nếu muốn giữ mutant cũ để canh diagnostic, ghi đúng đó là kiểm thông báo, không tính nó như phép chứng minh traversal được nhận. *“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”*.

**CA TEST KHOÁ:** Dùng nguyên c37: dưới mutant normalizer, receipt sai phải thật sự thành 0 lỗi/1 đạt trước khi assertion giết nó; hai đối chứng path đúng và `./` vẫn qua. Mutant “chỉ đổi thông báo từ chối” không được nhận tín dụng cho thuộc tính chấp nhận sai. Không cần viết payload mới để khóa phản chứng đã có.

**BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ:** Nới assertion c37 để nhận mọi thông báo mà vẫn giữ mutant cũ sẽ chỉ làm m43 mất răng; cần đổi mutant cùng lúc. Không đòi mọi mutant trong suite chỉ có một failure: điều cần đo là thuộc tính mục tiêu có thực sự thay đổi.

**ĐỘ TIN:** cao; đã trace lỗi/số đạt và đối chứng khi từng mutant còn hiệu lực.

### R7-05-ho-so-do-phu-sai  [P3]  Biên nhận mới đổi lỗi nguồn R6-02 thành lỗi “độ phủ”

**TỆP/DÒNG:** `ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml:3–5`; đối chiếu R6-02 trong tệp verdict được receipt neo.

**VẤN ĐỀ:** Header nói “ca hai P2 deu ve DO PHU”. R6-01 là độ phủ; R6-02 là **hành vi sản phẩm** khi nguồn mất riêng surface vẫn báo sạch. Chính verdict giải thích đã đo nguồn không đủ hợp đồng, và không gọi nó là lỗi test. Bản tóm tắt mới làm nhẹ sai loại vấn đề mà vòng vá này được giao đóng.

**PHẢN CHỨNG ĐÃ CHẠY:** Đọc header bằng `cat ...review-6-codex-verdict.receipt.yaml`, đọc R6-02 trong verdict; `inspect.py` xác nhận blob verdict neo `e9ff74b912ecbc88de3e8430509f1bfdcb384ed0` khớp byte và SHA-256. Đây là đối chiếu văn bản nguồn đã xác minh, không phải đo thêm một lỗi runtime.

**GỢI Ý VÁ:** Chỉ sửa tóm tắt của receipt: ghi một P2 về độ phủ (R6-01), một P2 về phân loại nguồn không đủ hợp đồng (R6-02), một P3 về mô tả phạm vi transport (R6-03). Giữ verdict lịch sử nguyên byte và các trường hash của verdict. Khi cập nhật báo cáo head, dùng số đã đo **1/15** receipt khai transport, **5 tên chính tắc + 1 alias từ bảng + 1 tên human chép tay**; không tiếp tục lời khai “0/15” hoặc “không tên nào chép tay” của prompt.

**CA TEST KHOÁ:** Đối chiếu từng finding ID/severity/loại lỗi với verdict neo Git. Đột biến báo cáo gom R6-02 thành “chỉ độ phủ” phải bị review tài liệu bác. Không đề nghị thêm test khớp chuỗi cho một chỉnh sửa prose có thể đảo ngược.

**BẢN VÁ NÀY CÓ THỂ ĐẺ RA GÌ:** Sửa luôn verdict lịch sử sẽ phá chuỗi byte/hash. Thay một số hiện tại bằng số chép tay mới mà không ghi head/điều kiện sẽ trôi lần nữa. 0/14 trong chú thích cũ có thể là số tại thời điểm bản vá; không viết lại lịch sử ấy như thể lúc đó đã có receipt thứ 15.

**ĐỘ TIN:** cao.

## Bốn vùng mỏng và giới hạn còn lại

- **Transport khuyết:** phép đọc chỉ so một chuỗi không rỗng; không có allowlist filename/hash phân biệt receipt cũ/mới. Bỏ transport không né được chốt surface hoặc lệnh cấm assurance của Web, nhưng phép so transport sẽ không chạy. Tương tự, `_chuoi` trả `None` cho sai kiểu/rỗng nên “có mặt” chưa đồng nghĩa được validate. Không có fixture mới được phép dùng để chứng minh một attestation mới khai sai được nhận; **chưa đo**, không thêm P1. Nếu muốn đóng nợ: giữ ngoại lệ cho 14 hiện vật khuyết đang đạt bằng filename+hash, định nghĩa yêu cầu receipt mới và ca sai kiểu/khuyết; đừng chỉ ép trường mới lên lịch sử. Phải phân biệt transport reviewer với transport người đăng.
- **ASSURANCE_CAM_DONG_BANG:** phần cấm đích danh trong AGENTS §4 đúng là một provider Web. Điều khoản AG–AG phụ thuộc cặp Executor–Reviewer, không thể chép thành cấm vô điều kiện cho AG. Câu neo hiện chỉ được tìm bằng substring; chưa đo ngữ nghĩa/vị trí khi câu chuyển thành ví dụ hoặc trích dẫn. Không coi một chuỗi hiện diện là bằng chứng parser đã hiểu doctrine.
- **PROVIDER_KHONG_HOP_DONG:** không tự nở là phù hợp với allowlist đóng; vấn đề cụ thể là đặt `human` sai miền theo R7-02. c31 còn lấy chính hằng này để loại phần thừa nên không phải oracle độc lập về quyền thêm vào tập ấy. Không báo một phép hợp thêm Web vào tập này là bypass: tên Web đã có trong tập provider, phép đó không đổi tập cho phép và đã bị loại khỏi bằng chứng finding.
- **Cây gương:** không tái hiện lệch tự phát ở lần chạy nền. Đã chứng minh parity mù với alias surface bị làm mất riêng trong bản sao. Chưa đo Windows/CRLF, crash/cleanup/reorder của rig hoặc mọi nguồn tương lai; không suy vài lần chạy hữu hạn thành chứng minh parity tổng quát.

## Phụ lục — script phản chứng đã chạy

Lưu từng khối dưới vào tệp cùng tên **ngoài repository**, rồi chạy từ root clone bằng `PYTHONDONTWRITEBYTECODE=1 python3 <đường-dẫn-script>`. Đây là đúng mã của bốn script đã chạy ở trên, giữ khả năng tái lập khi thư mục tạm mất. Các script không đổi receipt; trường hợp rig chỉ sửa bản nguồn được chép vào thư mục tạm. Cặp đột biến A/B và kết quả chạy toàn suite đã ghi riêng ở R7-03.

### source_probe.py

```python
import ast, os, subprocess, sys, tempfile, shutil, json
from pathlib import Path

R = Path.cwd()
S = (R / '.claude/dev/launcher.py').read_text()
nodes = {n.targets[0].id: n for n in ast.parse(S).body
         if isinstance(n, ast.Assign) and isinstance(n.targets[0], ast.Name)}

def edit(table, change):
    n = nodes[table]
    old = ast.get_source_segment(S, n.value)
    assert S.count(old) == 1
    return S.replace(old, repr(change(ast.literal_eval(n.value))), 1)

variants = {
    'baseline': S,
    'missing_launcher': None,
    'provider_alias_short_row': edit('_PROVIDER_BI_DANH', lambda v: (v[0][:1],) + v[1:]),
    'surface_alias_short_row': edit('_BE_MAT_BI_DANH', lambda v: (v[0][:1],) + v[1:]),
    'codex_transport_none': edit('_TRANSPORT_CONTRACTS', lambda v: tuple(
        r[:3] + (None,) if r[0] == 'openai_codex' else r for r in v)),
    'codex_surface_none': edit('_TRANSPORT_CONTRACTS', lambda v: tuple(
        r[:2] + (None,) + r[3:] if r[0] == 'openai_codex' else r for r in v)),
}
for label, source in variants.items():
    with tempfile.TemporaryDirectory(prefix='r7-source-') as td:
        t = Path(td)
        (t / 'ops').mkdir()
        (t / '.claude/dev').mkdir(parents=True)
        shutil.copyfile(R / 'ops/bien_nhan_v2.py', t / 'ops/bien_nhan_v2.py')
        shutil.copyfile(R / 'AGENTS.md', t / 'AGENTS.md')
        if source is not None:
            (t / '.claude/dev/launcher.py').write_text(source)
        q = subprocess.run([sys.executable, str(t / 'ops/bien_nhan_v2.py'),
                            '--root', str(R)], capture_output=True, text=True,
                           env={**os.environ, 'PYTHONDONTWRITEBYTECODE': '1'})
        print(json.dumps({'label': label, 'rc': q.returncode, 'stdout': q.stdout,
                          'stderr': q.stderr}, ensure_ascii=False))
print('SOURCES_COMPLETE')
```

### path_probe.py

```python
import ast, sys, importlib.util, json, shutil
from pathlib import Path
sys.dont_write_bytecode = True
R = Path.cwd()
s = importlib.util.spec_from_file_location('t', R / 'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(s)
s.loader.exec_module(t)
node = next(n for n in ast.walk(ast.parse((R / 'ops/bien_nhan_v2_test.py').read_text()))
            if isinstance(n, ast.Call) and isinstance(n.func, ast.Name)
            and n.func.id == 'do' and n.args and isinstance(n.args[0], ast.Constant)
            and n.args[0].value.startswith('m43_'))

def run(label, mutate):
    original, cong, measures = t.bnv2, t.CONG, []
    try:
        mutate()
        real = t.bnv2.kiem
        def measure(*a, **kw):
            result = real(*a, **kw)
            measures.append({'errors': result[0], 'stats': result[1]})
            return result
        t.bnv2.kiem = measure
        result = t._chay_1(t.c37_URL_phai_neo_DUNG_duong_dan_bien_nhan_khai)
        t.bnv2.kiem = real
        control = t._sach_hoan_toan(t.c18_neo_git_DUNG_thi_qua)
        print(json.dumps({'label': label, 'test': result, 'control': control,
                          'fixture_results': measures}, ensure_ascii=False))
    finally:
        if 'real' in locals():
            t.bnv2.kiem = real
        t.bnv2, t.CONG = original, cong
        for p in t._TAM_DOT_BIEN:
            shutil.rmtree(p)
        t._TAM_DOT_BIEN.clear()

run('baseline', lambda: None)
run('m43_as_shipped', lambda: eval(compile(ast.Expression(node.args[1]),
    '<m43-from-AST>', 'eval'), t.__dict__)())
run('restore_lstrip', lambda: t._dot_bien_tep(
    '    khai_duong = str(d.get("verdict_path") or "").strip()',
    '    khai_duong = str(d.get("verdict_path") or "").strip().lstrip("./")'))
print('M43_TRACE_COMPLETE')
```

### rig_probe.py

```python
import ast, sys, importlib.util, shutil, json
from pathlib import Path
import yaml
sys.dont_write_bytecode = True
R = Path.cwd()
s = importlib.util.spec_from_file_location('t', R / 'ops/bien_nhan_v2_test.py')
t = importlib.util.module_from_spec(s)
s.loader.exec_module(t)
real_copy, goc, cong = shutil.copyfile, t.bnv2, t.CONG

def copy_missing_alias(src, dst, *a, **kw):
    result = real_copy(src, dst, *a, **kw)
    if Path(dst).name == 'launcher.py':
        p = Path(dst)
        source = p.read_text()
        n = next(n for n in ast.parse(source).body if isinstance(n, ast.Assign)
                 and getattr(n.targets[0], 'id', '') == '_BE_MAT_BI_DANH')
        old = ast.get_source_segment(source, n.value)
        assert source.count(old) == 1
        p.write_text(source.replace(old, '()', 1))
    return result

try:
    shutil.copyfile = copy_missing_alias
    t._dot_bien_tep(
        '    if khai_duong and (khai_duong.startswith("/") or ".." in Path(khai_duong).parts):',
        '    if False:')
    keys = ('PROVIDER_CHO_PHEP', 'ALLOWLIST_CUTOVER', 'NO_DA_DO', 'ANCHOR_LOAI_CHO_PHEP')
    print('PARITY_PASSED', {k: getattr(t.bnv2, k) == getattr(goc, k) for k in keys})
    print('CONTRACTS_EQUAL', t.bnv2.PROVIDER_HOP_DONG == goc.PROVIDER_HOP_DONG)
    p = R / 'ops/reviews/phan-bien-quy-trinh-review-1-claude-verdict.receipt.yaml'
    d = yaml.safe_load(p.read_text())
    print('UNCHANGED_RECEIPT', p.name, 'original_mri', goc._mri(d), 'mirror_mri', t.bnv2._mri(d))
finally:
    shutil.copyfile = real_copy
    t.bnv2, t.CONG = goc, cong
    for p in t._TAM_DOT_BIEN:
        shutil.rmtree(p)
    t._TAM_DOT_BIEN.clear()
print('RIG_PARITY_COMPLETE')
```

### inspect.py

```python
import sys, importlib.util, hashlib, subprocess, json
from pathlib import Path
import yaml
sys.dont_write_bytecode = True
R = Path.cwd()
s = importlib.util.spec_from_file_location('m', R / 'ops/bien_nhan_v2.py')
m = importlib.util.module_from_spec(s)
s.loader.exec_module(m)
print('PROVIDERS', sorted(m.PROVIDER_CHO_PHEP), 'ALIASES', m.PROVIDER_BI_DANH,
      'NO_CONTRACT', sorted(m.PROVIDER_KHONG_HOP_DONG), 'ERROR', m.PROVIDER_NGUON_HONG)
print('HUMAN_BRANCH', {'allowed_name': 'human' in m.PROVIDER_CHO_PHEP,
      'has_contract': 'human' in m.PROVIDER_HOP_DONG,
      'human_audited_in_no_contract_ban': 'human_audited' in m.ASSURANCE_CAN_DOC_LAP})
ds = [(p, yaml.safe_load(p.read_text())) for p in (R / 'ops/reviews').glob('*.receipt.yaml')]
v2 = [(p, d) for p, d in ds if p.name not in m.ALLOWLIST_CUTOVER
      and p.name not in m.NO_DA_DO and not m._thieu(d)]
transports = [(p.name, d['model_reviewer_identity'].get('transport'))
              for p, d in v2 if 'transport' in d['model_reviewer_identity']]
print('PASSING_STRUCTURAL', len(v2), 'TRANSPORT_PRESENT', len(transports), transports)
p = R / 'ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.receipt.yaml'
d = yaml.safe_load(p.read_text())
sha, path = d['evidence_url'].split('/blob/')[1].split('/', 1)
q = subprocess.run(['git', 'show', sha + ':' + path], capture_output=True)
a = subprocess.run(['git', 'merge-base', '--is-ancestor', sha, 'HEAD'])
print('R6_RECEIPT', json.dumps({'sha': sha, 'schema': m._thieu(d),
      'git': m._neo_git(R, p.name, d), 'blob_rc': q.returncode, 'ancestry_rc': a.returncode,
      'hash': hashlib.sha256(q.stdout).hexdigest(),
      'hash_match': hashlib.sha256(q.stdout).hexdigest() == d['verdict_sha256'],
      'bytes_match': q.stdout == (R / path).read_bytes(), 'size': len(q.stdout)}))
print('INSPECTION_COMPLETE')
```

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container; Python **3.11.15**, Git **2.43.0**, PyYAML **6.0.1**; `PYTHONDONTWRITEBYTECODE=1`. Mã thoát lấy trực tiếp từ subprocess/công cụ tiến trình. Log và script tiện ích ở `/tmp/pr455-r7-5kW5ZW`; chúng không phải receipt bền trên GitHub.

| Command | rc thật | Trạng thái / bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | **passed theo suite:** 41/41, 48/48 thường, 1/1 tự kiểm, 30/48 khai đối chứng, `TỔNG: ĐẠT`. Giới hạn ý nghĩa/độ phủ ở R7-03/R7-04. |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | **passed trên 68 hiện vật:** 15 đạt, 11/11 miễn trừ băm khớp, 42 nợ, 0 vi phạm/0 chưa đo, `TỔNG: ĐẠT`. |
| `python3 .claude/dev/launcher_test.py --nhat-ky /tmp/pr455-r7-5kW5ZW/launcher-journal.log` | 0 | **173/173 ca đã chạy qua, tổng 182, bỏ qua 9, hỏng 0; suite tự in KHÔNG ĐỦ.** Không xác nhận 181/181. |
| `python3 ops/lease_publish_test.py` | 0 | **passed:** 121/121, đã chạy 121, bỏ qua 0. |
| `python3 .claude/dev/packet_loop_test.py` | 0 | **passed:** 278/278, bỏ qua 0; 81 mutant, 78 lớp lách, 35 ca bắt oan, 0 ngoại lệ AC18, `TỔNG: ĐẠT`. |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed:** `ok=true`, checked=expected=180; failed/extra/missing/required_missing/errors rỗng; package hash match=true. Doc-pointer/bare-tool advisory còn được khai riêng. |
| `git diff --check 5a78c150106ae381461354c77ba2023834330bbd HEAD` | 0 | **passed:** không lỗi whitespace; manifest chỉ thay CHANGELOG và tổng byte/hash, giữ 180 tệp. |
| `source_probe.py`, `path_probe.py`, `rig_probe.py`, `inspect.py` qua Python như lệnh tại findings | 0 từng script | Marker lần lượt `SOURCES_COMPLETE`, `M43_TRACE_COMPLETE`, `RIG_PARITY_COMPLETE`, `INSPECTION_COMPLETE`; rc con và phản chứng được tách ở findings. |

Release package hash: `5e7a3111f2cdc3785e932a2f0052ca6195c6d6c000e951eecc407ddc591abd96`.

**Receipt vòng 6 tự qua cổng:** không thuộc miễn trừ/nợ; `_thieu=[]`, `_neo_git=([],[])`. `git show e9ff74b912ecbc88de3e8430509f1bfdcb384ed0:ops/reviews/pr455-bien-nhan-v2-review-6-codex-verdict.md`: rc=0, **25.456 byte**, byte-match tệp hiện tại, SHA-256 `0b249313b99c3e6ec66163f6fe9043d0309926ab0b6877c866a4c024f13ae982`. `git merge-base --is-ancestor e9ff74b912ecbc88de3e8430509f1bfdcb384ed0 HEAD`: rc=0. Đây là ancestry tới HEAD local, không chứng thực launcher/model/delivery ngoài clone.

**failed:** bất biến phân loại nguồn ở R7-01 và khóa hồi quy ở R7-03 bị phản chứng; m43 không chứng minh thuộc tính mô tả. Không có suite nền nào trả lỗi, nhưng launcher chưa đủ bằng chứng.

**skipped:** launcher bỏ t62 Windows; tám ca r345/r347/r348 không dựng được venv/pip với `pypdf==3.17.4` trong sandbox. Không có wheel phù hợp được tìm thấy để chạy bù offline. Các kết quả skip không tính pass. Lease/packet không bỏ ca.

**not_run:** full runtime selftest, workflow-audit/golden/determinism, release-bundle, Windows/CRLF parity, mọi script lịch sử nguyên vẹn, các payload mới về transport/neo câu/nhân thân audit, LIVE/merge/deploy. Không dùng danh sách phép đo executor đưa làm trần độ phủ.

**KHÔNG ĐO ĐƯỢC:** trạng thái GitHub trực tiếp (head PR hiện thời, CI/required checks, protection, delivery, authority điều phối); provenance model/session và launcher artifacts lịch sử ngoài clone. Báo cáo không tự tạo `cross_approved`, approval GitHub hoặc quyền land.

Trong clone được review chỉ tạo `VERDICT.md`; HEAD/tree giữ nguyên OID đầu báo cáo. Hints là đề xuất cho executor tái dẫn xuất và tự đo, không phải bằng chứng một bản vá kế tiếp đã đúng.

verdict: approve_with_findings
