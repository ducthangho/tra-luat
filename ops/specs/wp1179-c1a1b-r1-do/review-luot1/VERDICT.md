reviewed_sha: 24354e7709da4d6aa0299e4eff982b7d50b98d76
spec_sha256: 3dc6a2b9cd6dcf85a11dab3aa5fb8d44bf7945f61071e20bb33405e2521f6d04
model/effort (tự khai): Codex, nền GPT-6 theo chỉ thị phiên; tên model cụ thể và mức effort không được môi trường công bố, không xác nhận gpt-6-astra/xhigh.
provider: OpenAI
execution_surface: agent có shell cục bộ, qua API
transport: tool calls trực tiếp; không phải ChatGPT Web/human_mediated
verdict: changes_requested

Review **đặc tả**, không phải nghiệm thu implementation C1a1b. Có 4 P2 và 1 P3 mở. Lớp `phan-loai-vang-va-khong-do-duoc` tái diễn; cần checkpoint theo §7 trước vòng vá tiếp.

Đã xác nhận HEAD và SHA-256 đúng yêu cầu; `git status --short` rỗng. Kho được review chỉ đọc; mọi prototype và bản sao nằm trong sandbox.

| Mục cần phán xét | Kết luận ở tầng đặc tả | Căn cứ |
|---|---|---|
| P2 ABI/output/N6 | **CHƯA ĐÓNG trọn vẹn** | ABI đã viết rõ và N6 ban đầu/drift đã tách; nhưng acceptance chưa bảo vệ quan hệ outer `ok` và byte stdout, F3. Không đồng nhất lỗi này với phá module JSON thuần. |
| P2 nullable/mode-type S/C | **CHƯA ĐÓNG** | G6 khớp producer, kể cả gitlink vắng object; G7 bác symlink mà producer thực thi và phát receipt được, F2. |
| P2 budget profile | **ĐÃ ĐÓNG ở tầng đặc tả về neo phép đo** | Đo lại 5.444 commit / 8.480.418 byte; hệ số 9,184 và ngoại suy 77,89 MB đúng. Đây là căn cứ chọn trần bảo thủ, không phải nghiệm thu timeout/memory hay Windows. |
| `mo-rong-module-pha-hop-dong-json-thuan` | **ĐÃ ĐÓNG ở tầng đặc tả** | §2.1 tách module, write set loại module JSON cũ, A1/A3 giữ nguyên byte/kết quả. Blob cũ `3490ea0…` khớp; suite nền 156/156, 162/162, equivalent 9. Chưa có implementation mới để chứng nhận runtime. |
| `phan-loai-vang-va-khong-do-duoc` | **CHƯA ĐÓNG** | G1/A7 yêu cầu unknown dù đã xác minh đầy đủ chuỗi và MOC tồn tại; trái luật iff của §0.2/§2.3, F4. Đây là lần tái diễn sau lịch sử ba lượt, không đặt lại lớp. |

Phạm vi đối chiếu lượt trước là ba P2 và hai slug được cung cấp trong Issue/prompt. Không có ba verdict/log scratch nguyên văn, nên không tuyên bố đã audit nội dung ngoài các mô tả đó. Bảng lớp hiện tại: F1 `dat-lai-ngan-sach-khi-doi-truc` (P2); F2 `predicate-consumer-khong-khop-producer` (P2); F3 `dot-bien-tuong-duong-hoac-thieu` (P2, nối lớp của C1a1a §5.0, ba biểu hiện A9/A18/ABI); F4 giữ nguyên slug kế thừa (P2); F5 `so-do-ke-thua-chua-do-lai` (P3). Trong hai lớp được yêu cầu đối chiếu riêng, 1/2 đóng ở tầng đặc tả; không dùng tỷ lệ này suy ra đã hội tụ toàn packet.

### F1 — P2 — `dat-lai-ngan-sach-khi-doi-truc`

**Vị trí:** §8 dòng 359–364; §10 dòng 383 (đối chiếu §0 dòng 43–46).

§8 mặc định cấp PR thi công một trục mới, `init` về 0, và chỉ tính tiếp ≥ 4 lời gọi nếu chủ kho yêu cầu. Điều này trái chỉ thị tiếp nhận `6679422380`: “Trần sẽ được khai bằng dòng `tran_loi_goi_codex` trong spec đóng băng. ADR-0055 hoặc ADR-0052, số đã dùng tính từ ≥ 4.” Giữ lịch sử ở bảng khác không bảo toàn ngân sách nếu bộ đếm dùng để cấp lượt đã về 0. §10 gọi đây là quyết định “chờ chủ kho”, nhưng §8 lại cho nó hiệu lực mặc định. Trần 10 của ADR-0055 hợp lệ không tự cấp quyền đổi phạm vi bộ đếm.

**Phép đo:** `sed -n '276,330p' <scratchpad>/i1179.md` và `sed -n '354,383p' <mirror>/ops/specs/wp1179-c1a1b-r1.md`, rc 0; nguồn bàn giao yêu cầu tính từ ≥ 4, đặc tả ghi “trục riêng”/“init đặt bộ đếm 0”. Đọc PROTOCOL §8.3/§12, rc 0: đổi packet/baseline không reset lịch sử và budget. Ba phép kiểm OID của ADR-0055 đạt (log `evidence/basic.txt`): `cat-file -e L:path` rc 0; `L^1:path` rc 128; L thuộc first-parent master.

**Đề xuất:** mặc định tiếp tục `used >= 4 + các lời gọi r1 đã sinh output`, tính riêng reserved/limit và connector. Nếu muốn tách trục, yêu cầu quyết định bền thay đúng chỉ thị bàn giao trước khi áp dụng; ghi cơ chế reconcile state thay vì coi `init=0` là bằng chứng ngân sách mới. Không suy số lượt còn lại chính xác từ cận dưới ≥ 4.

### F2 — P2 — `predicate-consumer-khong-khop-producer`

**Vị trí:** §2.4 bảng G7 dòng 185–196, A11 dòng 305; §10 điểm 4.

Lý do “Python đã thực thi tệp này tại C” không suy ra entry phải là `100644/100755`. Python thực thi symlink bình thường. Workflow hiện tại lấy `oid_bo_kiem_da_chay` bằng `git rev-parse C:ops/lease_publish.py`, không kiểm mode hoặc lấy OID target của symlink. Vì thế G7/A11 bắt buộc bác một hình dạng mà chính producer/workflow vẫn phát receipt. Tách predicate S/C đã giải quyết việc dùng chung một predicate, nhưng predicate C mới chưa khớp producer.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_graph.py`, rc 0, chi tiết argv/rc tại `evidence/graph.txt`. Trong clone `--shared`, commit mới trên MOC thật đặt `ops/lease_publish.py` là symlink nội bộ tới `ops/checker_real.py` chứa nguyên byte producer tại base. Lệnh `python -B ops/lease_publish.py kiem-thu-hoi-github H --canonical-base A --nhanh-mac-dinh master --receipt ...` rc 0, `TAP_THU_HOI_RONG`. Lệnh workflow `git rev-parse C:ops/lease_publish.py` rc 0, trả OID symlink `203e9c185dec2f21482a7f1138284d2bcf531bab`. Bổ sung đúng các trường bằng các phép đọc local của workflow: `kiem_json` trả `ok=true`, cả K1–K5 `qua`; G7 theo bảng buộc `do`. Đây là phép đo local producer, không khai có run GitHub hay provenance thật.

**Quét cùng lớp:** G6 đã đo đủ năm mode cuối: producer trả OID ngay cả gitlink có commit vắng, chỉ đọc hai tree; vắng trả `None`, ancestor blob ném `Chan`. Các ô G6 khớp. G8 thực sự có `cat-file blob` + sha256 trong workflow, nhưng cổng mode regular cũng không nằm trong các lệnh thu thập đó; không suy từ phép đo local rằng GitHub chạy YAML symlink.

**Đề xuất:** chốt rõ predicate C là tương thích producer hay chính sách mới chặt hơn. Nếu tương thích, mô hình hóa đúng symlink và giới hạn lời khai về “mã đã chạy”; nếu cấm symlink có chủ đích, cần căn cứ/authority cho thay đổi đó và ca chứng minh, không ghi việc Python chạy được là bằng chứng của regular mode. Ghi riêng giới hạn chưa đo của workflow-definition trên GitHub.

### F3 — P2 — `dot-bien-tuong-duong-hoac-thieu`

**Vị trí:** đồ thị fixture dòng 279–285; A4–A5 dòng 298–299; A9 dòng 303; A18 dòng 312.

A9 yêu cầu đột biến so `T` với `tree(S)` làm “ca G4” đỏ, nhưng ca chỉ được mô tả là đổi T sang “tree khác”; không chốt `tree(H) != tree(S)` hoặc chọn `T = tree(S)`. Một fixture hợp lệ theo đồ thị ở dòng 283–285 có tất cả commit dùng cùng tree: so với H và so với S tương đương trên mọi ca đổi trường T. Ngay khi hai tree khác nhau, chọn T thứ ba khác cả hai vẫn cho `do/do`; không giết mutant ở ca đích. Tổng suite đỏ ở ca dương không thay chứng minh đúng ca đích mà dòng 289 yêu cầu.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_graph.py`, rc 0; đồ thị thật trên MOC, `tree(S)=3882586…`, `tree(H)=1dfdae4…`, T đổi sang empty tree `4b825dc…`: oracle đúng `do`, mutant so S cũng `do`, `target_changes=False`. Chọn T bằng tree(S) mới được `do/qua`; fixture dương được `qua/do`. Log và OID đầy đủ trong `evidence/graph.txt`, `evidence/graph-ids.json`.

**Đề xuất:** bắt buộc hai tree S/H khác nhau; ca đích đặt `T=tree(S)` và xác nhận oracle G4 là `do` trên bản đúng, `qua` trên mutant. Khóa riêng G5; audit mọi predicate ghép theo §5.0, không coi một ca âm bất kỳ là witness cho phép thay toán hạng.

**Biểu hiện cùng lớp ở A18:** ca `g_dong_tong` chỉ gọi hàm dựng dòng tổng **thuần**, nhưng mutant “nuốt lỗi import” nằm ở caller thực hiện import. Đưa cờ lỗi giả vào formatter không đo được caller nuốt lỗi. `PYTHONDONTWRITEBYTECODE=1 python -B probe_registry.py`, rc 0 (`evidence/registry.txt`): cả caller đúng và caller nuốt `ImportError` đều qua bốn ca âm của formatter; chạy caller thật thì bản đúng không in tổng, bản nuốt lỗi in `157/157 … 163/163` và regex **thật** của sổ nhận xanh. Sổ cũng nhận dòng cũ JSON-only `156/156 … 162/162`; tự nó không phân biệt nhóm Git đã chạy. Cần ca end-to-end chạy entrypoint suite với import Git hỏng, kiểm rc và toàn bộ stdout bằng regex thật, rồi giết mutant ở chính đường import.

**Biểu hiện cùng lớp ở ABI:** §2.2 dòng 100/104 yêu cầu serialization và `ok` tương đương JSON qua + mọi G qua. A4 chỉ nêu tập khóa, kiểu bộ đếm, trạng thái và tiền tố lý do; A5 chỉ đọc rc. Các ca G đỏ A7–A14 kiểm trạng thái luật, không yêu cầu outer `ok=false`. `PYTHONDONTWRITEBYTECODE=1 python -B probe_abi.py`, rc 0 (`evidence/abi.txt`), trích đúng các predicate công bố: mutant `ok=json.ok` vẫn qua A4, giữ rc 12/13 và trạng thái G1 đúng, nhưng xuất `ok=true` khi G1 đỏ/không đo được; serializer bỏ `sort_keys` cũng qua oracle A4. Đây là mô hình kiểm độ phân biệt của tiêu chí, không phải tuyên bố đã chạy verifier C1a1b chưa tồn tại. Cần ma trận ABI/rc đầy đủ, kiểm iff `ok`, kiểu bool, byte stdout chuẩn hóa, và mutant tương ứng. Bảng nghĩa vụ §5.0 bắt buộc nhưng để dành việc dựng bảng cho thi công không sửa được các witness cụ thể còn thiếu/sai ở r1.

### F4 — P2 — `phan-loai-vang-va-khong-do-duoc`

**Vị trí:** §0.2 dòng 61; §2.3 dòng 146–149; G1 dòng 160 và A7 dòng 301.

Luật chung khẳng định `khong_do_duoc` **khi và chỉ khi thiếu bytes đã xác minh**; kết luận từ bytes đã xác minh phải là `qua/do`. G1/A7 lại bắt buộc `khong_do_duoc` khi đã đi hết first-parent tới root và không gặp MOC. Đây có thể là một kết quả âm đã đo đầy đủ, ngay cả khi object MOC có sẵn trong kho. Cụm “kho không chứa mốc” không đúng với tình huống đó. Hai điều khoản buộc hai cách phân loại khác nhau cho cùng dữ liệu; vì vậy lớp này chưa đóng dù các ô path vắng của G6–G8 đã rõ hơn.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_classification.py`, rc 0 (`evidence/classification.txt`). Dựng Y từ P theo A7 bằng `commit-tree`, rc 0. `git cat-file -e MOC^{commit}` rc 0. Duyệt first-parent Y tới root bằng `cat-file --batch`, tự băm SHA-1 từng commit: **674 commit**, `found_MOC=False`, **0** object thiếu/hỏng, tiến trình rc 0. Tất cả bytes cần để kết luận MOC vắng khỏi chuỗi đã có; G1/A7 vẫn đòi `khong_do_duoc`.

**Quét cùng lớp:** G6 path vắng và ancestor blob đã được kiểm với producer (F2); object gitlink cuối vắng không phải thiếu bytes cần cho G6. G7/G8 blob cần đọc mà vắng được phân biệt đúng với entry vắng. G9 drift và vượt ngân sách đã được liệt kê là căn cứ mất phép đo; trường hợp G1 trên chưa có ngoại lệ nhất quán.

**Đề xuất:** quyết định một nghĩa duy nhất: nhánh không đi qua MOC sau khi duyệt đầy đủ là `do`, hoặc mở rộng định nghĩa trạng thái thứ ba thành thiếu tiền đề tin cậy và khai ngoại lệ G1 rõ ở mọi nơi. Ca nghiệm thu phải phân biệt “MOC object vắng/hỏng” với “MOC có mặt nhưng không trên chuỗi”. Đây là lần xuất hiện tiếp của lớp đã có ở ba lượt trước; theo §7 dòng 351–352 cần Review Rescue Checkpoint trước vòng vá tiếp, không chỉ sửa riêng A7.

### F5 — P3 — `so-do-ke-thua-chua-do-lai`

**Vị trí:** §1 S4 dòng 70; §6 điểm 5 dòng 339 (và nghĩa vụ nguồn C1a1a §8: “Spec C1a1b phải chép và đo lại từng dòng”).

S4 giữ số khảo sát **1.795 / 37**, chưa làm phép đo lại N1 dù mirror đủ dữ liệu. Đo trên đúng base hiện nay là **4.360** commit ngoài first-parent, **64** commit trong số đó chạm producer, không còn là 1.795 / 37. Tệp đã ghi rõ đây là số cũ, nên finding là thiếu nghiệm thu phép đo kế thừa, không cáo buộc giả số liệu và không ảnh hưởng predicate G1.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_counts.py`, rc 0 (`evidence/counts.txt`). `git rev-list 889334fb` rc 0: 5.444 OID; `git rev-list --first-parent 889334fb` rc 0: 1.084 OID; hiệu tập = 4.360. Giao hiệu tập với `git log --format=%H 889334fb -- ops/lease_publish.py` (rc 0) = 64.

**Đề xuất:** thêm số đo mới neo exact base, lệnh và cách đếm; giữ 1.795 / 37 ở lịch sử nếu cần. Với số ref, mirror hiện có 777 nhánh + `origin/HEAD`, khác snapshot 776: đã có nhánh `claude/spec-1179-c1a1b` của chính review này; khai riêng thời điểm/tập ref thay vì coi hai snapshot là cùng phạm vi. Chênh thời gian profile giữa các lần chạy là biến thiên đo, không phải bằng chứng số lịch sử sai.


### Phép đo độc lập và phạm vi kết luận

Quy ước: `<mirror>` là `../cay-kho` tính từ sandbox, base đầy đủ `889334fb87c25136a13c6776a40a25b401820e04`; MOC đầy đủ `601a0f18c83057fa079d204122660f5697fc6389`. Mọi script `probe_*.py` nằm cạnh verdict, gọi từ sandbox bằng `PYTHONDONTWRITEBYTECODE=1 python -B <script>`. Git chỉ ghi vào các clone/snapshot trong sandbox. Các phép đọc `rev-list`/`merge-base` là oracle độc lập của reviewer, không đề nghị dùng chúng trong reader sản phẩm.

| Phạm vi | Lệnh / rc | Output và kết luận |
|---|---|---|
| Identity | `git rev-parse HEAD HEAD^{tree} origin/master --is-shallow-repository`; `sha256sum ops/specs/wp1179-c1a1b-r1.md`, rc 0 | HEAD đúng header; tree `93fb483b1ec506e70de72c1b027d795d65008be8`; base đúng; shallow=false; băm đặc tả đúng. |
| S1, S6 | Trong clone `baseline` tại base: `python -B .claude/dev/doc_receipt_thu_hoi_test.py`, rc 0 | `156/156 ca QUA · 162/162 dot bien GIET`; witness 162, equivalent 9, unresolved 0; 11,349 s. Hợp đồng JSON tự khai C không chứng minh provenance vẫn đúng. |
| S2 | `git rev-list --first-parent --count 601a0f18^..889334fb`, rc 0 | **411** commit gồm MOC; khớp. |
| S2/S3 | `python -B <mirror>/ops/specs/wp1179-c1a1b-r1-do/do_profile.py <mirror> <base> <MOC>`, hai lượt rc 0 | **410 / 531.751 byte**, 0,027 / 0,027 s; **5.444 / 8.480.418 byte**, 0,345 / 0,330 s. Số lượng/byte khớp; thời gian dao động quanh phép đo cũ 0,030 và 0,337/0,341 s. Reader profile dừng trước khi đọc MOC; 410 là số object đã đọc/cạnh tới MOC, không phải số commit inclusive. |
| S4 | `probe_counts.py`, rc 0 | **4.360 / 64**, F5. |
| S5 | `git diff --stat 601a0f18 889334fb -- ops/lease_publish.py .github/workflows/ops-thu-hoi-admission.yml`, rc 0 | **2 tệp, +650/−93**, khớp. |
| §2.6 | `probe_budget.py`, rc 0 | Trung bình **1.557,754960 byte/commit**; 50.000 commit ≈ **77.887.747,979 byte**; 50.000/5.444 = **9,184423**; commit lớn nhất trong tập **8.477 byte**. Guard prototype ở 8.388.607 và 8.388.608 cho JSON qua, 8.388.609 cho G0 đỏ/json null. |
| §3 holder | `probe_holders.py`, rc 0 của script; bốn lệnh `python -B ops/lease_publish.py ai-dang-giu <path> --root <holder-copy>` | Ba đường module mới/suite/module JSON: **0 holder, rc 0**. Registry: **1 holder `wp1236-a1-r7-g1-claude-remote-20261106`, rc 11**. Khớp bảng. |
| Sổ CI / phương án B | `probe_registry.py`, rc 0; `python -B .claude/dev/ci_dang_ky_test.py` trong `baseline`, rc 0 | `kiem`: **29/29**, thêm module vẫn 29/29; thêm test mới báo lỗi, 30/29. Check sổ đầy đủ: **1070/1070 phản chứng**, `TỔNG: ĐẠT`. Regex nhận tổng cộng, không nhận dòng nhóm; nguy cơ wiring ở F3. |
| N5, N6 | `probe_acceptance.py`, rc 0 | S=B,C=A: ancestry đúng rc 1, đảo rc 0; G3 H=X: đúng rc 1, mutant so C rc 0. Ref đọc đầu đúng, sau đổi khác, sau xóa rỗng: triển khai tách rc 2/13 khả thi. |
| Reader | `probe_graph.py`, `probe_reader.py`, rc 0 | Replace bật: `cat-file --batch` rc 0 nhưng hash bytes lệch OID hỏi; tắt replace thì khớp. Loose object hỏng vẫn `cat-file` rc 0, rehash bắt lệch. `GIT_OBJECT_DIRECTORY` gây `missing` khi không lọc, object đúng khi lọc. Object vắng có dòng `missing` dù git rc 0. Các mutant A12 có witness thật. |

Log chi tiết: `evidence/basic.txt`, `counts.txt`, `budget.txt`, `holders.txt`, `registry.txt`, `registry-full.txt`, `graph.txt`, `acceptance.txt`, `reader.txt`, `classification.txt`, `abi.txt`. Môi trường đo: Linux 6.18.44-fc-v242, Python 3.13.18; Git theo probe môi trường cuối báo riêng. Giây là wall time của lần chạy này, không chứng minh performance trên máy khác.

**Giới hạn holder/ref:** nguồn cung cấp là mirror đóng băng, không phải fetch trực tiếp GitHub trong phiên này. Đã dựng server local chứa đúng **777 remote branch heads** của mirror (bỏ symbolic `origin/HEAD`), clone từ đó rồi chạy nguyên CLI holder; không sửa hàm phân loại lease. OID/tên ref lưu ở `evidence/mirror-refs.txt` (SHA-256 `a1b371ef25a5a2f67b39ec9d64b7f525c7dd7a7be27e9c778203264677799480`). Kết quả chứng minh holder của snapshot được giao; không chứng nhận trạng thái live hoặc đầy đủ ref tại 07:25:56Z. Spec đã yêu cầu đo mới trước cấp lease, cần giữ yêu cầu đó.

**Giới hạn profile:** số đo làm căn cứ được tái lập; mức 8 MiB/object và 128 MiB/tổng vẫn là lựa chọn theo producer, không suy ra “an toàn tối ưu” từ thời gian 0,34 s. Mọi tổ tiên master là trần trên tập commit G2 khi C hợp lệ, không phải trần trên mọi H của PR trong G3. Không đo Windows, cold cache, timeout tiến trình bị treo hay peak RSS. Những phần đó không được tính là pass; P2 profile đóng ở mức đã có căn cứ đo Linux cho lựa chọn trần, không phải production budget đã nghiệm thu.

### Kiểm ba dòng khai ADR

`probe_declarations.py`, rc 0; log `evidence/declarations.txt`. Đọc nguyên byte đúng blob đặc tả, mỗi token có đúng một dòng hợp mẫu; **0** dòng khai ADR-0052.

| Dòng khai | `cat-file -e L:path` | `cat-file -e L^1:path` | `rev-list --first-parent origin/master` rồi `grep -qx L` |
|---|---:|---:|---:|
| ADR-0055 `d2e3052d479d140b7e7b91df41ec4914fab7d544` | 0 | 128 | 0 / 0 |
| ADR-0053 `8ab100793df9831505f495543a74044b91c2c9ab` | 0 | 128 | 0 / 0 |
| ADR-0060 `36d7c5dcdcbbb27176b75135125b9009f9fe0587` | 0 | 128 | 0 / 0 |

Ba khai báo đạt kiểm tra OID trong mirror đầy đủ. Khi hash này được dùng cho spec lease, opt-in tương ứng hợp lệ trên snapshot: trần lời gọi 10, trần sensitive 6 tệp/450 dòng thêm, điều kiện merge ADR-0060. Không suy ra chủ kho đã duyệt `nang_tran` 2 tệp/750 dòng, quota đã reserve, hay state đã ghi đủ lịch sử. §3 nêu rõ nâng kích thước đang chờ duyệt nên không có quyền tự áp 750; A15 phải đo diff implementation thật. Diff đang review là **5 tệp/+466 dòng của gói đặc tả và hiện vật**, không phải diff implementation hai đường đã hứa; không khai A15 implementation đã đạt.

### Rà tính khả thi A1–A19

“Khả thi” dưới đây là đánh giá hợp đồng/độ phân biệt; module C1a1b chưa tồn tại, nên không dùng từ “suite C1a1b đã pass”. Phép đo prototype chỉ chứng minh đúng phần được ghi.

| Tiêu chí | Kết quả rà |
|---|---|
| A1 | Khả thi: so byte bằng Git, module cũ tại base/candidate cùng blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b`; sửa byte làm diff khác. |
| A2 | Khả thi với phương án B; nền và sổ đã chạy thật. Cần giữ riêng số JSON 156/162/9 khi gộp, không chỉ nhìn dòng tổng mới. |
| A3 | Equality với `kiem_json` độc lập phân biệt hằng xanh nhờ các ca JSON đỏ; thêm khóa cũng bị phân biệt. Tách module giữ đúng giới hạn JSON thuần. |
| A4 | Hai mutant thêm `giay`/trạng thái ngoài tập có thể bị bắt; thiếu iff outer `ok` và serialization, F3. |
| A5 | Thứ tự rc 12 trước 13 có witness hỗn hợp; N6 ban đầu/đọc lại phân biệt được bằng ref thật. Cần so outer output cùng rc, F3. |
| A6 | Skip K1/K2 so với chạy K4 khả thi, không cần đọc graph bằng dữ liệu K2 sai. Nên chốt riêng G0 đã kiểm kích thước hay được đổi về `khong_chay` sau JSON đỏ trong ma trận ABI; không dựa vào cụm “mọi G” để tránh mô tả thứ tự. |
| A7 | Đã đo đồ thị thật: E giết all-parent, P giết bỏ biên dưới, MOC giết biên exclusive. Ca master không qua MOC mâu thuẫn luật phân loại, F4. |
| A8 | Đã đo: đảo ancestry tại B→A đổi rc 1→0; dùng C thay H ở H=X đổi rc 1→0. Nhánh rẽ đơn thuần không thay witness strict-ancestor. |
| A9 | Witness chỉ định chưa đủ, F3. Cần hai tree khác nhau và T được chọn đúng để làm sai mutant. |
| A10 | G6 khớp thực nghiệm `KhoObject.tim` cho đủ năm leaf modes/vắng/ancestor blob. Đọc gitlink target sẽ gặp object vắng, khác phép so entry; nullable cần cả hai chiều. |
| A11 | Các mutant dùng G6 cho G7/bỏ blob read/bỏ sha256 có thể phân biệt bằng các ca được nêu; nhưng oracle chặn symlink không khớp producer, F2. Kết luận “mutant chết” không chứng minh predicate ấy đúng. |
| A12 | Replace, rehash, env filter đã đo cơ chế thật; bỏ chúng đổi kết quả đúng ca. Đọc `missing` phải xét framing chứ không coi rc 0 của cat-file là thành công. |
| A13 | Biên receipt đã đo với JSON thật. Trần commit và clock tiêm khả thi. Cần obligation tách max-object/max-total, per-walk G1/G2/G3, dùng lại object, stop/cleanup khi git treo; câu “trần byte nhỏ hơn một commit” không riêng chứng minh cả hai trần. Hằng bằng bảng không chứng minh guard chạy. |
| A14 | Đổi/xóa ref sau lần đầu đã đo; bắt buộc ra unknown thay lỗi tham số có thể thực hiện. Kiểm snapshot đầu riêng là cần thiết. |
| A15 | Có thể đo numstat và dirty state. Chưa có mã thi công/owner approval nâng trần, nên chưa nghiệm thu con số 750. |
| A16 | Windows **not_run** trong review này; không thay bằng Linux. Phải có command tập trung cụ thể, ID/kết quả nền và ứng viên, cách loại mutant khỏi lượt tập trung; không sửa registry hay bỏ required test để đạt. Câu “Không Windows CI” nên giới hạn rõ vào allowance của lượt tập trung, không dùng để vô hiệu Windows CI hiện hành/ADR-0060 M3. |
| A17 | Điều kiện M9 phù hợp vùng write set. CI/waiver trên implementation **not_run/not_present**, không dùng suite local thay receipt CI. |
| A18 | Format có thể đi qua regex hiện hành mà không sửa sổ. Ca hàm thuần không phân biệt mutant nuốt import ở caller, F3; cần end-to-end. |
| A19 | Các lệnh gate có thể thực hiện trong clone implementation. Registry nền đã đạt; Ruff/doctrine/adr-song của implementation chưa chạy vì chưa có hai tệp sản phẩm mới. Không khai gate sản phẩm xanh từ số nền. |

**Traceability §2.2–§2.6:** §2.2 → A3–A6/A13 (thiếu oracle ABI nêu F3); §2.3 → A10–A13 (cần thêm disposition cho wrong-type, malformed tree/commit, git chết, cấu hình local/global/system và dùng lại object); §2.4 → A7–A14 (F2–F4); §2.5 → A5/A14 (cần từng input sai, repo/receipt không đọc được và exact-name N6); §2.6 → A13 (cần tách các trần như trên). §4 dòng 289–291 kế thừa bảng nghĩa vụ cho mọi mệnh đề, vì vậy các phần chưa có ca cụ thể phải thành ID/disposition có chứng cứ trong implementation; không suy đã phủ từ A1–A19 hoặc tổng mutant. Không có bằng chứng để tuyên bố toàn bộ predicate §2.2–§2.6 đã được đo ở lượt này.

### Hợp đồng kế thừa, ngân sách và giới hạn cuối

N1–N8 đều có chỗ chiếu: G1, G3, hạ tầng clone/MOC, reader/phân loại, A8, preflight/G9, giới hạn N7 tại §2.2, G6. N1 còn phép đo cũ F5; phân loại reader/G1 còn F4. Erratum r5 chỉ ghi lại ngoại lệ kích thước C1a1a, không tự cấp ngoại lệ C1a1b. Spec cha M9 cũ giả định C=S đã có nợ được ghi; đối chiếu ưu tiên hành vi producer hiện tại đã tách C/S, không áp lại đồng nhất C=S. Chưa có receipt thật C≠S/provenance API; §5/§6 giữ đúng việc này cho C1b/C1a2 và **không** tuyên bố T2/Q16/Q17 đạt.

§0 và §9 không tự xóa ba verdict/lượt mất kết quả; bảng §9 trống đúng với thời điểm commit trước review. Sau lượt này lịch sử biết được tăng thêm một lời gọi đã có output, tức **≥ 5**, không phải formal validated round tự động. Lỗi nằm ở mặc định cấp trục mới tại §8 (F1), không phải cần hồi tố sửa bảng §9 trong commit đang review. Không phát sinh thêm lời gọi model, connector, CI, push hoặc merge trong lượt này.

Trạng thái kho nguồn sau đo: `git status --porcelain=v1 --untracked-files=all --ignored` rc 0, stdout rỗng; HEAD/spec hash được đối chiếu lại. Không sửa kho được review. Snapshot sạch chỉ xác nhận không có delta quan sát được; không phải chứng cứ giám sát mọi thời điểm. Bản verdict này không tự tạo cross-approval receipt, human audit hoặc quyền land.

TONG: P1=0 P2=4 P3=1
