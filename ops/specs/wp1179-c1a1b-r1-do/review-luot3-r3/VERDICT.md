# Cross-review wp1179 C1a1b r3 — lượt 3

- reviewed_sha: `0924f4f69b26728a29faa970d1660aff6dc176ad`
- spec_sha256: `779f9384cf87aacd9bbe3c5737c9585ef4c408178df8fc7b4c3121fa31aab039`
- reviewed_tree: `e8997f59b248abf43b6c0744c5fd2463b233fd54`
- provider: `openai_codex`; execution_surface: `codex_cli`; transport: `machine`, theo `../run/f2172e8b/run.json` (launcher đang chạy, chưa phải receipt terminal).
- run_id: `f2172e8bba424b169857d04ed9250764`; sandbox: `workspace-write`, cây review được đối xử read-only; toàn bộ prototype/output nằm trong sandbox.
- model/effort tự khai: nhận diện Codex/GPT-6 theo chỉ thị phiên; `model_served=KHONG_DO_DUOC`, `effort_served=KHONG_DO_DUOC`. `run.json` hiện không có hai trường phục vụ này; không suy `gpt-6-astra/xhigh` từ yêu cầu trong spec.
- verdict: `changes_requested` — F6–F8 vá thật ở tầng đặc tả; còn **F9, một P2** về cấp ngân sách từ lịch sử chưa biết đủ.

## Nhật ký tăng dần

- Đã đọc prompt.snapshot và AGENTS.md, xác minh HEAD và băm spec đúng; `git status --porcelain` rỗng. Chỉ ghi vào sandbox.
- Đã hoàn tất kiểm F6–F8, bảng lớp, toàn bộ A1–A20 và các mục §0–§11; kết quả cuối có F9 P2, không P1/P3 mới.
- Phạm vi: toàn bộ r3, xác minh riêng F6–F8, review theo lớp ADR-0060 M2, đo lại các con số. Chỉ thị hiện tại thay quyết định human audit cũ và cho phép lượt review này; không coi thay đổi thẩm quyền sau commit là finding.

## F6–F8

| Finding | Phán xét | Bằng chứng |
|---|---|---|
| F6 | **VÁ THẬT** | §2.3 dòng 215–216, G7/G8 dòng 267–283 và A11 dòng 399 thống nhất resolve → mode → OID → blob. Probe thật 2 luật × 3 lỗi blob × 2 quan hệ OID: lệch ⇒ `do`, **0 lần đọc leaf**; khớp ⇒ `khong_do_duoc`, đúng sự kiện và 1 lần đọc. Mutant đọc trước so OID đổi `do→khong_do_duoc` ở đủ 6 witness. [classification-r3.txt](evidence/classification-r3.txt), rc 0. |
| F7 | **VÁ THẬT** | §4 dòng 381–385 và A18 dòng 406 khai bản sao suite/sổ, gốc kho tường minh, child dương trước, cờ chống đệ quy và lỗi nạp đúng tệp. Dựng lại với **toàn bộ suite JSON thật**: child dương rc 0; ImportError/SyntaxError/vắng module rc 1, không tổng; caller nuốt ImportError rc 0 và in tổng chỉ JSON ⇒ đúng `TinHieuChotCa(g_dong_tong_e2e: …)`. Thiếu registry bị child dương bác trước khi tiêm. N=0/M>0 và M=0/N>0 tách riêng; fixture trùng tree phân biệt được guard bị bỏ. [a18-r3.txt](evidence/a18-r3.txt), rc 0. |
| F8 | **VÁ THẬT** | A6 dòng 394 khớp §2.2: JSON K1/K2 đỏ dưới trần ⇒ G0 `qua`, G1–G9 `khong_chay`; quá trần ⇒ G0 `do`, JSON null; K4 đỏ vẫn cho G chạy. Dùng `kiem_json` thật, K1 `{}` 2 byte, K2 receipt 38 khóa 1.856 byte. Mutant G0=`khong_chay` vi phạm đúng oracle K1/K2. [classification-r3.txt](evidence/classification-r3.txt), rc 0. |

Các phán xét trên là **đóng biểu hiện ở tầng đặc tả**, không phải nghiệm thu triển khai C1a1b: module mới chưa tồn tại. Prototype A18 giữ ca/đột biến JSON thật nhưng nhóm Git là smoke prototype; số 157/163 trong log của nó **không** phải tổng suite C1a1b.

## Bảng lớp — ADR-0060 M2 / protocol §8.3

| Slug lớp | Nguồn / biểu hiện đã quét | Mức mở cao nhất | Kết quả, cách vá chung và phép đóng |
|---|---|---|---|
| `mo-rong-module-pha-hop-dong-json-thuan` | draft0–2; r1; §2.1–2.2, A1–A4 | — | Không tái mở. Module JSON byte-identical với base; API mới bao nguyên dict. Giữ audit byte/hash và đối chiếu JSON cho cả dương/K1/K2/K4 trên implementation. |
| `phan-loai-vang-va-khong-do-duoc` | F4/r1, **F6/r2**, r3 §2.3×§2.4, A7/A10–A14/A20 | — | F6 vá thật; đã quét cả G6 và G8, vắng entry/ancestor sai mode khác missing object. Cặp không-MOC và mất commit giữa chuỗi ra `do/unknown`. Giữ thứ tự đọc trong bảng làm nguồn duy nhất; kiểm ô luật×E trên mã tương lai. |
| `dot-bien-tuong-duong-hoac-thieu` | F3/r1, **F7/r2**; A4/A5/A9/A11/A13/A18/A20 | — | F7 vá thật; không còn ép mutant hạ tầng vào module Git. Child dương chống tín dụng từ lỗi setup, hai tree trùng được đưa chủ động vào guard. Các witness A4/A9 phân biệt được; các disposition cuối vẫn cần audit mã triển khai, không lấy prototype làm `witness_killed` của sản phẩm. |
| `oracle-trang-thai-g0-mau-thuan` | **F8/r2**; ABI/A6/A13 | — | Vá thật. G0 luôn qua/do, chỉ G1–G9 bị skip. Ca guard biên và K1/K2 dưới trần có oracle nhất quán. |
| `predicate-consumer-khong-khop-producer` | F2/r1; G6/G7/G8/A10/A11 | — | Không tái mở. Đo producer thật cho 5 mode, symlink nội bộ chạy được; G7/G8 so chính OID entry và hash chuỗi đích. Bác gitlink/thư mục là chỗ chặt hơn producer đã khai; không suy nội dung target là mã đã chạy hay GitHub đã nạp symlink workflow. |
| `dat-lai-ngan-sach-khi-doi-truc` | F1/r1, đã vá ở §8 r2; **F9 mới tại §11.1 r3** | **P2** | **Tái mở**, 1 biểu hiện mới: cận dưới lịch sử được dùng để cấp số dư cục bộ. Cần reconcile hoặc cận trên chứng minh được; kiểm cùng trace bộ đếm với U thật khác nhau. Không đổi slug để xóa lịch sử F1. |
| `so-do-ke-thua-chua-do-lai` | F5/r1; §1 S2–S6, §11.5 | — | Không tái mở. Số 5.444/1.084/4.360/64, 531.751/8.480.418 byte, +650/−93, drift +698/−92 tái lập. Thời gian chỉ là phép đo một máy/bộ đệm ấm; không đối xử lịch sử S7/S8/holder như số đo live. |
| `nguon-duoc-tin-ma-chua-xac-minh` | lịch sử C1a1a §6, r3 §2.3/N6/§5/§6/§11 | — | Không thấy biểu hiện mới ngoài F9 đã gán một lớp riêng. Hash bytes, lọc GIT_*, replace và hai lần đọc ref có witness. Không tuyên bố đóng lớp lịch sử của toàn chuỗi: nguồn API của caller, run provenance, receipt thật S≠C và holder live vẫn ngoài phép đo này. |

**Đếm riêng:** 8 lớp kế thừa đã quét; 1 lớp mở hiện tại / 1 finding mới (F9); không thêm slug mới. Với tập mở cuối lượt 2 gồm 3 lớp của F6/F7/F8, 3/3 đã vá ở tầng đặc tả ⇒ tỷ lệ chuyển tiếp **100%**; lớp F9 tái mở từ lượt 1 báo riêng, không đưa vào tử số. Tỷ lệ này không đủ để approve.

## Audit toàn bộ A1–A20

“Phân biệt” trong bảng là kiểm tính khả thi/độ phân biệt của acceptance, có dẫn phép đo hoặc lập luận; **không** ghi các gate implementation chưa tồn tại là passed.

| Tiêu chí | Kết quả và giới hạn phép đo |
|---|---|
| A1 | Diff byte module JSON giữa base và reviewed SHA rc 0; blob `3490ea0ee40081c0eba2d121f5b19a67a021a54b`. Đổi byte làm diff khác là oracle phân biệt trực tiếp. |
| A2 | Chạy suite trên clone base: 156/156 ca, 162/162 killed, 9 equivalent, 0 unresolved, rc 0. `kiem()` registry: base 29/29, thêm module Git vẫn 29/29, thêm test riêng thành 30/29 và lỗi đúng đường. Số nhóm JSON phải giữ khi implementation xuất hiện. |
| A3 | `kiem_json` thật được dùng với dương/K1/K2/K4 trong các probe. So dict nguyên vẹn phân biệt hằng giả/khóa thừa; việc nạp đúng đường và không sửa sys.path vẫn phải đo trên module mới. |
| A4 | [ABI witness](evidence/abi-witness-r3.txt) chạy serializer subprocess cho cả 5 tổ hợp a–e: byte đúng; bỏ sort đổi byte ở cả 5. `ok=json.ok` bị b bác, bỏ JSON bị d bác, bool→int bị kiểm kiểu bác. Tập khóa/kiểu/trạng thái đóng đủ; CLI sản phẩm chưa có, không khai đã test CLI C1a1b. |
| A5 | Ưu tiên mixed `do+unknown` phải rc 12; đảo thứ tự ra 13. Ref đầu/đổi/xóa được đo trên Git thật, tách rc 2 ban đầu và rc 13 cuối. “Mỗi vế §2.5” gồm cả check-ref-format sau regex và từng OID; cần giữ riêng bằng chứng stderr một dòng/stdout rỗng. Không có CLI để đo hết ca tham số lúc này. |
| A6 | F8 vá thật như bảng trên; guard quá kích thước và JSON đỏ dưới trần không còn xung đột. K3/K4/K5 đỏ không chặn Git theo ABI. |
| A7 | Graph thật trên MOC: C=B và MOC nhận; C=P/E/X bác. All-parent nhận sai E; bỏ bound nhận sai P; bỏ biên bác sai MOC. Không-MOC 675 commit đủ ⇒ do; xóa Q1 mới trong scratch ⇒ unknown sau 1 commit. Không xóa object trong mirror/alternates. Khi C gặp sớm, cột đọc vẫn đòi đi tới MOC/root; không lấy việc thấy C làm chứng cứ rằng bound MOC đã tồn tại. |
| A8 | Git ancestry thật: B≤A rc 1, đảo A≤B rc 0; A≤X rc 1 trong khi mutant dùng C=B ra 0. Equality được nhận. Nhánh rẽ không bị gán tín dụng cho mutant đảo chiều. |
| A9 | S/C/H đôi một khác tree; T=tree(S) và tree_S=tree(H) đều đổi do→qua dưới mutant đích. Empty tree là đối chứng, không phải witness chính. Guard tự kiểm nhận fixture trùng tree; bỏ guard đổi màu trong prototype. |
| A10 | Producer `KhoObject.tim` thật đọc 2 tree, nhận OID cả 5 mode, không đọc leaf; gitlink OID không có object vẫn trả entry. Vắng trả None; ancestor blob ném KHÔNG_XÁC_ĐỊNH. Bảng G6 phân biệt null/hex và mode/type đúng theo metadata; không dùng G6 thay G7. |
| A11 | F6 được đo thêm cả lỗi hash/type ngoài missing. Symlink checker và workflow đo bằng Git thật, OID entry khác target, sha256 chuỗi đích khác target. Các mode bác/OID lệch/hash lệch đều có predicate riêng; rc 12/13 cần đồng thời kiểm vector để các luật đỏ khác không che ca đích. |
| A12 | Loose object có tên OID nhưng bytes khác: cat-file rc 0 mà rehash false. Replace bật trả bytes thay, tắt trả bytes gốc. GIT_OBJECT_DIRECTORY không lọc gây missing; lọc thì đọc đúng. Vector dependency H→G3/G4, không→G1 là đúng. Phần Windows chưa chạy. |
| A13 | 50.000/5.444=9,1844; bình quân 1.557,754960 byte/commit, ngoại suy 77.887.747,979 byte; max commit 8.477. Biên G0 8.388.607/8.388.608/8.388.609 ⇒ qua/qua/do. Witness mẫu per-walk [3,1,4] so shared-counter khác đúng G2; byte object/memo có witness riêng. Trần total và wall đã có ca riêng ở spec; timeout của pipe thật, cleanup/RSS và toàn bộ walker chưa đo (module chưa tồn tại), không coi clock seam là profile Windows. |
| A14 | Ref thật đổi và xóa sau lần đọc đầu phân biệt được; oracle phải đọc G9 unknown và rc 13, không nhận lỗi ban đầu rc 2 thay thế. |
| A15 | Write set chỉ 2 tệp; trần ≤750 đã được user xác nhận. ~710 là **ước**, chưa có diff implementation để nhận. Numstat toàn nhánh đặc tả gồm log và merge master không phải kích thước thi công. |
| A16 | Required theo ADR-0060 M3; lệnh bao cả nhóm Git và mutant suite, không miễn Windows CI. Khi thi công phải giữ danh sách test ID/kết quả từng lượt nền/ứng viên như M3, không chỉ dòng tổng. `not_run` trong review đặc tả này. |
| A17 | M9 áp vì `.claude/dev/**`; cần receipt Ubuntu exact SHA hoặc waiver scope hợp lệ. Full mutant audit/waiver `not_run/not_present`, không suy từ suite JSON. |
| A18 | F7 vá thật, log có dương và 3 lỗi nạp; mutant caller bị bắt tại ca đích, lỗi setup không nhận tín dụng. Pure guard N/M kiểm tách, nhóm in sai dạng/ca lỗi không được phát tổng. Đột biến hạ tầng chỉ đặt trên bản sao suite. |
| A19 | Diff-check riêng r3 rc 0; diff-check toàn gói rc 2 do whitespace log lịch sử, ghi nguyên ở metrics. Không quy log bất biến ngoài tệp review thành finding nội dung r3; không khai toàn gói xanh. Ruff/doctrine/adr-song của **implementation** chưa nghiệm thu; không chạy gate toàn kho để thay cho mã chưa có. |
| A20 | Hợp đồng nghĩa vụ theo luật×E và disposition nguồn §5.0 vẫn bắt buộc; không cho tổng ca thay audit nghĩa vụ. Đã đo Git cho missing/hash/type, và mô hình vector target/non-target cho 7 E; mô hình vector không chứng minh đã chạy mọi ô trên implementation. G4/G5 chỉ cần commit, nên tree có kiểu blob là E của G6/G7/G8, không tự lan lên G4/G5. |

## Đối chiếu phần ngoài acceptance

- **§2.1–§2.5:** K1/K2 mới chặn G; JSON null iff G0 do; `ok` iff và rc 12 ưu tiên 13 khép kín trên các vector hợp lệ. Bảng G7/G8 giờ cùng thứ tự đọc, G6 giữ predicate riêng. N6 ràng buộc exact ref, không DWIM, không cho dùng master tự khai để thay ref; nguồn tham số qua API thuộc C1b. Không thấy mâu thuẫn ABI mới.
- **§2.6:** profile khớp base; chỉ G1/G2 bị chặn trên bởi lịch sử master, G3 có thể mang lịch sử ngoài master và đã khai. 8 MiB/object, 128 MiB tổng và 60 s là giới hạn chính sách, không phải chứng minh đã đo toàn bộ đồ thị 50.000 commit hay giới hạn RSS. Memo phải giữ đếm unique object, kể cả OID bị hỏi dưới expected type khác; audit mã thực tế không được suy tính chất ấy chỉ từ tên cache key.
- **§3/§5/§6:** phương án B khả thi với registry hiện hành; không sửa producer/sổ. C1a2, C1b, T2/Q17, #656/#564/#499 và #1160 còn ngoài phạm vi; không nâng “ok” thành quyền land. Không đo mới được receipt thật S≠C, Windows/cold cache, quota/reservation và GitHub workflow symlink.
- **§8/§11 vs ADR-0055/0052/protocol §12:** cả 3 dòng khai ADR hợp lệ trên snapshot: từng OID có file tại L, chưa có tại L^1, thuộc first-parent origin/master, các rc **0/128/0**; không có dòng ADR-0052. Trần 10 của thời điểm spec không miễn lý do cấp lời gọi sau lượt đầu, cũng không nhập trục vòng/attempt. F9 là lỗi ở nhánh phục hồi mới, không phải đòi ghi hồi tố trần 16. Lịch sử used≥6, reserved unknown không tự là reservation.
- **§11.2–11.3:** lời thuật Rescue không được khai thành `record-rescue`; state guard chỉ nhận blocked/rescue_required. R3 đã khai đường tái lập chưa đo, không tự tạo journal. Bảng handoff theo §3.2.1 có thể giữ thông tin chưa có schema, không thay transition authority. Chỉ thị hiện tại là căn cứ cho lượt 3; không hồi sinh auto-review cũ bằng đổi provider hoặc dùng draft4.
- **§0/§7/§9/§10:** giữ lịch sử, không reset các lớp hay cộng số P cũ vào số mở hiện tại. Các câu human audit/2 lượt/no-more-Codex là quyết định tại commit, đã bị chỉ thị lượt này thay thế; không báo finding chỉ vì cập nhật quyền đến sau commit. Quyền merge/land không phát sinh từ verdict này.
- **§11.5–11.7:** diff `889334fb→08bcb51f` đúng 1 tệp +698/−92; toàn bộ đường phụ thuộc đã kiểm 0 delta. Holder/branch-count lịch sử không chứng minh holder live hiện nay: mirror hiện có 780 branch heads + origin/HEAD, chưa đối chiếu remote live. Trước lease vẫn cần phép đo mới theo spec.

## Lệnh, rc và evidence

Mọi lệnh Python dưới đây chạy với `PYTHONDONTWRITEBYTECODE=1 python -B`, cwd là sandbox (riêng suite nền cwd `sandbox/baseline`). Các probe cũ được **chép sang sandbox mới**, sửa neo SHA/spec r3 trước khi chạy; không ghi lại sandbox lượt trước. Các probe cùng dùng graph chạy nối tiếp.

| Lệnh / rc | Bằng chứng |
|---|---|
| `probe_graph.py` / 0 | [graph.txt](evidence/graph.txt), [graph-ids.json](evidence/graph-ids.json): graph trên MOC, producer, mode, replace, symlink; rc từng lệnh con có trong log. |
| `probe_counts.py` / 0; `probe_budget.py` / 0 | [counts.txt](evidence/counts.txt), [budget.txt](evidence/budget.txt): S4, diff byte, kích thước commit và G0. |
| `../cay-kho/ops/specs/wp1179-c1a1b-r1-do/do_profile.py ../cay-kho 889334fb87c25136a13c6776a40a25b401820e04 601a0f18c83057fa079d204122660f5697fc6389` / 0 | [profile-r3.txt](evidence/profile-r3.txt): 410 commit/531.751 byte/0,013 s; 5.444 commit/8.480.418 byte/0,232 s. |
| `.claude/dev/doc_receipt_thu_hoi_test.py` trên base / 0 | [json-baseline-r3.txt](evidence/json-baseline-r3.txt): 156/156, 162/162, equivalent 9, unresolved 0. |
| `probe_classification_r3.py` / 0 | [classification-r3.txt](evidence/classification-r3.txt): F6, F8 và A7 dùng object/ref thật; kết quả G là prototype bảng. |
| `probe_a18_r3.py` / 0 | [a18-r3.txt](evidence/a18-r3.txt): F7; stdout/stderr từng child ở `a18-r3/`, các child âm rc 1 là kết quả mong đợi, caller mutant rc 0 là witness bị bắt. |
| `probe_abi_witness_r3.py` / 0 | [abi-witness-r3.txt](evidence/abi-witness-r3.txt): ma trận ABI, serializer subprocess, tính phân biệt witness số học; không phải implementation. |
| `probe_reader.py`, `probe_acceptance.py`, `probe_symlink_workflow_r2.py` / mỗi lệnh 0 | [reader.txt](evidence/reader.txt), [acceptance.txt](evidence/acceptance.txt), [workflow-symlink-r2.txt](evidence/workflow-symlink-r2.txt). Giữ hậu tố r2 của probe tái sử dụng, kết quả là lần chạy này. |
| `probe_registry_r2.py` / 0 | [registry-r2.txt](evidence/registry-r2.txt): 29/29 và 30/29, chỉ sửa clone scratch. |
| `probe_call_budget_r2.py` / 0; `probe_metrics_r3.py` / 0 | [call-budget-r2.txt](evidence/call-budget-r2.txt), [metrics-r3.txt](evidence/metrics-r3.txt): F9, số đo S2/S5/§11.5, byte hashes, diff-check riêng/toàn gói tách biệt. |
| `probe_declarations.py` / 0 | [declarations.txt](evidence/declarations.txt): opt-in ADR và refs snapshot; không phải fetch/live authority. |

Môi trường đo: Linux 6.18.44, Python 3.13.18, Git 2.43.0. Không mạng, không model phụ, không CI/connector, không push/merge/LIVE. Không soạn dữ liệu thoát thư mục; symlink thử nghiệm chỉ trỏ tệp nội bộ. Có một lệnh thăm dò gõ nhầm `git diff --no-index ops-placeholder ops-placeholder` trả rc 1 do đường không tồn tại; không dùng nó làm evidence hay finding. Probe metrics ban đầu ghi nhầm tên đường spec A1b; đã sửa thành `THU-HOI-LEASE-A1b.md`, chạy lại rc 0 và lưu output cuối, không suy 0 delta từ đường vắng.


## Finding mới

### F9 — P2 — `dat-lai-ngan-sach-khi-doi-truc`

**Vị trí:** r3 §11.1 dòng 530–532, nối §8 dòng 463–466 và §11.2 dòng 539. Biểu hiện mới của lớp F1: lấy cận dưới U=6 thay số dùng chính xác để cấp hạn mức cục bộ; nhánh “hoặc hạ limit để có biên” cũng không cần một cận trên U có chứng cứ.

Đây là lỗi có ngay ở thời điểm r3, không phải việc r3 chưa ghi quyết định nâng 10→16 về sau. §11.1 thừa nhận U chỉ là ≥6 và còn lại unknown, nhưng đoạn phục hồi lại cho dùng 6 hoặc hạ hạn mức tùy ý. Với lịch sử phù hợp U=7, limit cục bộ 4 cho phép tổng 11 dù vẫn giữ trần 10. Hạ hạn mức xuống 1 cũng không an toàn nếu U=10, vẫn phù hợp U≥6. Chủ kho duyệt “đó là cận dưới” không biến cận dưới thành phép đo; nếu muốn cấp thêm ngoài số dư chưa biết thì cần ngoại lệ ngân sách riêng, ghi đúng thứ được nâng/miễn, không gọi đó là phục hồi 10−U.

**Phép đo:** `PYTHONDONTWRITEBYTECODE=1 python -B probe_call_budget_r2.py`, rc 0; [log](evidence/call-budget-r2.txt). CLI `init` thật nhận limit 4; bốn `record-codex-call` rc 0, lần thứ năm rc 3. State giả chỉ nằm trong sandbox, không tạo lời gọi model hay lease. Bộ đếm không biết lịch sử U: U=6 thì tổng 10, U=7 thì tổng 11 với cùng trace được chấp nhận. Protocol §12 cấm suy số dư khi lịch sử chưa đo đủ; ADR-0055 giữ nguyên cách đếm của ADR-0052.

**Đề xuất:** bỏ nhánh (b) dạng hiện tại; reconcile lịch sử thành U chính xác, hoặc cận trên có chứng cứ U_max rồi cấp `L−U_max` nếu dương. Nếu vẫn unknown thì giữ checkpoint, hoặc ghi ngoại lệ ngân sách có thẩm quyền với allowance và đơn vị riêng; không ghi U=6 vào vị trí dành cho số dùng chính xác. Ca khóa: U_exact=6 cho 4, U_max=7 cho tối đa 3, U_lower=6/upper=unknown không cấp số dương; đổi 10 thành 16 vẫn phải qua cùng kiểm tra. Rủi ro khi sửa: init không nhận 0, không được rơi về mặc định 2; một state cũ riêng lẻ cũng cần đối chiếu các lời gọi ngoài state (timeout/connector/phiên mới).

## Kiểm tra cuối

`PYTHONDONTWRITEBYTECODE=1 python -B probe_final_r3.py` rc **0** ([final-r3.txt](evidence/final-r3.txt)): HEAD/tree/hash spec giữ nguyên, tracked/staged/untracked/ignored đều sạch. Manifest SHA-256 nội dung **12.741 tệp** đầu/cuối giống nhau, **0 delta**; không chỉ kiểm số đường. Đây là bằng chứng không có delta quan sát được ở hai mốc, không tuyên bố sandbox cưỡng chế read-only hay chứng minh lịch sử mọi write. [Băm các probe](evidence/probe-manifest.sha256) lưu kèm để tái chạy.

**Phán quyết cuối:** `changes_requested`. F6–F8 **VÁ THẬT** trên đặc tả r3, nhưng F9 còn mở; chưa đạt điều kiện 0/0/0 của chỉ thị lượt này. Không sửa kho đang review, không tự cấp quyền thi công/merge/land.

TONG: P1=0 P2=1 P3=0
