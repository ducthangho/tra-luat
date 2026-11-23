reviewed_sha: 7c429aa7300ea9c5ff765521ca70bed49239a39e
verdict: approve

**APPROVE nội dung candidate trên exact SHA.** Bốn lớp lịch sử đã được kiểm đóng; không còn P0/P1/P2/P3 mở và không có finding mới. Việc gỡ phép đo chạy chồng không cắt M1–M4/A1–A5. Đây là verdict review nguồn; không xác nhận thay cho gate Windows, toàn registry, CI hoặc audit/ủy quyền merge còn phải hoàn tất riêng.

## Neo và phạm vi

Tree `7b8ab1bacea6ed0a78114d946c689395121a2efe`; base `8048551a9b1eb886c126d2a1a4df0f95fb285964`; cha/lượt 8 `beccb067e8e0da0d12f7526e7dddf15592b8cb7e`. HEAD/tree và SPEC SHA-256 `bd0a880b91d00a044247d4219dc2eefbf833de4958b0e2ff3d9a907588b1350e` đã tự xác minh. Chỉ thị offline `runs/5e31e2f1/prompt.snapshot`, lượt 9/10, #1322 r1 lease g2; metadata nháp/g1 trong SPEC không thay chỉ thị hiện hành.

Reviewer: Codex, provider `openai_codex`, họ `openai`, execution_surface `codex_service`, transport `machine` (API agent có shell). Executor theo prompt: Claude Code / họ `claude` (không có phép đo runtime của executor ở đây). Model/effort phục vụ reviewer: `KHONG_DO_DUOC`; không tự cấp receipt cross-approved hoặc quyền merge. Sandbox `workspace-write`; checkout được đối xử read-only, không khai mount read-only. Không gọi mạng. Scratch bằng `mktemp -d -p goi review9.XXXXXX`: `goi/review9.My7hQl` (R). Snapshot đầu gồm băm mọi tệp kể cả ignored/untracked và Git status/diff/index.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: `goi/lich_su/luot8-VERDICT.md`, SHA `beccb067e8e0da0d12f7526e7dddf15592b8cb7e`; lịch sử lượt 1–7 được giữ. Mọi nhãn bên dưới lấy từ phép đo lượt này; đã quét các đường cấp tín hiệu còn tồn tại trước khi chốt lớp F4.

| Finding / biểu hiện kế thừa | Nhãn §8 | Bằng chứng tự đo trên candidate |
|---|---|---|
| F1: thứ tự phụ thuộc lịch, kể cả tái mở lượt 4 | ĐÃ VÁ THẬT | `f1_deterministic.py` nguyên bản lượt 8 trên 3.13.18 và 3.12.3: mỗi nền gốc 100/100 SONG_SOT, T3 100/100 GIET. Lịch đợi mọi future xong + hash đảo vẫn bị bắt. |
| F2: thiếu chốt làm nóng `_NEN` | ĐÃ VÁ THẬT | `acceptance.py`: N=1/4 đều 62 khóa/62 baseline, mỗi khóa một lần, không thiếu/thừa, 0 baseline sau mutant. T6/T7 GIET. |
| F3/F3a: tử số theo việc, thiếu/thừa/sai tên/thứ tự | ĐÃ VÁ THẬT | 8 dãy kết quả trên kế hoạch m1,m2: chỉ dãy đúng rc=0; 7 dãy lỗi rc=1. T8/T18/T19 GIET. |
| F3b: cắt cả việc và kết quả còn bốn | ĐÃ VÁ THẬT | `job_variants.py`: c67 xanh nhưng c68 rc=3; main N=1/4 rc=1; `coverage_readback.py`: kế hoạch 409, gọi/trả 4, tên không khớp. |
| F3c: lặp việc đầu / sửa danh sách của caller | ĐÃ VÁ THẬT | Lặp: c67/c68 rc=3, 409 calls nhưng 1 việc duy nhất, main rc=1; xóa danh sách: c67 rc=4/c68 rc=3, main rc=1. Caller giữ kế hoạch độc lập. |
| F3d: gắn tên đúng nhưng chạy nhầm việc/kết quả | ĐÃ VÁ THẬT | T20/T21 GIET; biến thể bọc lại nhãn có 409 calls/1 việc, chỉ 1/409 chi tiết khớp, bị c68 thật chặn rc=3. Main vô hiệu ca có thể xanh, không dùng riêng nó làm bằng chứng đóng. |
| F4/F4a: nuốt lỗi luồng điều phối c65 | ĐÃ VÁ THẬT | Cơ chế điều phối cũ vắng trong AST. c65 hiện gọi helper trực tiếp; lỗi trước/sau collector n=1/n=4 và callback trong Future thật đều không GIET (`faults9-313.log`, `faults9-312.log`). |
| F4b: test c68 lồng đổi lỗi child thành chốt | ĐÃ VÁ THẬT | Producer/consumer `xet_c68`, c68 cũ và các seam lồng đều đã gỡ; c68 hiện là test danh tính/kết quả, không gọi child thật. Quét đủ 12 bang và boundaries không thấy đường chuyển HONG/TIN_DUNG_GIA lồng thành chốt. Script neo c68 cũ không được tính là đã chạy. |
| F4c: c70 bắt RuntimeError vô can | ĐÃ VÁ THẬT | c70 cũ và caller không còn; các kiểm sức khỏe fixture còn lại ném RuntimeError ra ngoài bang. Hai pha fake + cleanup được đo độc lập, lỗi trả rc=4 hoặc timeout/HONG. |
| F4d: hàng mới cuối c70/c71 nhận lỗi riêng vô can | ĐÃ VÁ THẬT | `LoiHaTangLong`, `TIEN_TO_HA_TANG_C68`, c70/c71 và seam không còn. Không thay bằng test lồng mới; lỗi ở các phép c64–c68 còn sống không cấp GIET. |
| F4e: rào abort/BrokenBarrierError/chậm callback | ĐÃ VÁ THẬT | AST và trace runtime xác nhận không còn `Barrier.wait` trong candidate. BrokenBarrierError ở callback fake còn sống được đo cả pha 0/1, trả TIN_DUNG_GIA. Gỡ phép phụ không cắt M4/A3; xem đối chiếu SPEC. |
| F4f: chậm worker/submit hoặc abort gần hạn | ĐÃ VÁ THẬT | Không còn phân loại dựa vào số ID luồng, thời gian rào hay cấu hình pool. Lịch fake chậm vẫn SONG_SOT; handshake hết 10 s ở cả hai pha là TIN_DUNG_GIA, thread chết/treo là HONG, không GIET. Các lịch trên Barrier cũ không còn điểm tiêm. |
| F4g: cấu hình thuộc pool khác được dùng cấp GIET | ĐÃ VÁ THẬT | Chạy lại phản chứng lượt 8 trên cha cho GIET giả với abort/chậm; candidate 6/6 SONG_SOT và 0 lần gọi rào (cả 3.13/3.12). Alias public lưu trước patch cũng 3/3 SONG_SOT/0 rào. Cơ chế bị gỡ hoàn toàn, không chuyển sang phép đo phụ khác; ma trận 56 × 2 phủ phần còn sống. |

## BẢNG LỚP

Lịch sử gồm **4 lớp, 13 biểu hiện**: F1 (tái mở lượt 4 vẫn cùng biểu hiện), F2, F3/F3a + F3b + F3c + F3d, F4/F4a + F4b + F4c + F4d + F4e + F4f + F4g. Đếm biểu hiện theo ID ổn định; các biến thể đầu vào không tăng số. Không tách/gộp lớp; không tính mỗi lượt tái diễn thành lớp mới. F2 được đặt slug lần đầu bên dưới theo ánh xạ 1:1, giữ nguyên ID/nguồn và độ nghiêm trọng P2 lịch sử. `—` ở cột mức mở nghĩa là không còn finding mở, không phải hạ severity lịch sử.

| class_slug | Finding IDs và biểu hiện | Mức nghiêm trọng cao nhất còn mở | Nguồn lượt/SHA | Cách vá chung | Phép kiểm đóng lớp | Trạng thái lớp |
|---|---|---|---|---|---|---|
| `chot-thu-tu-phu-thuoc-lich` | F1: lịch hoàn tất/tập Future làm T3 sống | — (lịch sử P2) | L1 `c2b00c7…`; mở lại L4 `8edfc110…` | Dùng executor điều khiển với Future thật, handshake và hash không đơn điệu; kiểm sức khỏe đối chứng trước chốt | F1 tất định 3.13/3.12: gốc 100/100 xanh, T3 100/100 GIET; lifecycle và lỗi hai instance không cấp GIET giả | ĐÃ VÁ THẬT |
| `thieu-chot-lam-nong-nen` | F2: thiếu chốt làm nóng/bỏ sót/trùng baseline | — (lịch sử P2) | L1 `c2b00c7…`, đóng từ L2 `c3bf526…` | Tách prewarm trước vòng; phủ ba bảng đích; c67 + T6/T7 | N=1/4: 62 khóa một lần trước mutation; T6/T7 GIET ở cả 3.13/3.12; c67 gốc xanh | ĐÃ VÁ THẬT |
| `thieu-ket-qua-van-bao-xanh` | F3/F3a đếm sai/thiếu/thừa; F3b cắt việc; F3c lặp hoặc đổi kế hoạch; F3d gắn đúng tên nhưng sai việc/kết quả | — (lịch sử cao nhất P2; F3 ban đầu P3) | L1 `c2b00c7…`; L5 `d547a6c…`; L6 `a016722…`; đóng L7 `56279e0…` | Caller sở hữu kế hoạch độc lập; kiểm tên/thứ tự/số lần; co_ten gắn tên theo đối số; c68 dùng kết quả phân biệt có SONG_SOT | 8 dãy kết quả; 12 biến thể job + gốc; 409 việc thực/duy nhất ở N=1/4; c67/c68 thật chặn các biến thể; T8/T18–T21 GIET | ĐÃ VÁ THẬT |
| `loi-luong-nen-bi-tinh-la-giet-dung` | F4/F4a luồng điều phối; F4b test lồng c68; F4c/F4d c70/c71; F4e/F4f rào/lịch; F4g cấu hình pool không gắn việc | — (lịch sử P2) | L2–L8: `c3bf526…`, `01f3ce6…`, `8edfc110…`, `d547a6c…`, `a016722…`, `56279e0…`, `beccb067…` | Gỡ cơ chế phụ ngoài M4/A3; giữ chốt thứ tự/miền và truyền ngoại lệ Future; kiểm sức khỏe bằng RuntimeError ngoài bang | A/B F4g trên cha và candidate; AST không còn producer/consumer cũ; đọc đủ 12 bang mới; 56 fault/control × 2 Python, boundaries và lifecycle; không còn GIET giả trong phạm vi đã đo | ĐÃ VÁ THẬT |

Ánh xạ slug còn thiếu: `(chưa có slug, F2 ở L1)` → `thieu-chot-lam-nong-nen`; lý do: định danh lần đầu đúng cơ chế của F2, không tách/gộp hay reset lịch sử. Phép đối chiếu cùng F2 là c67 + T6/T7 và đo toàn 62 khóa. Các slug F1/F3/F4 giữ nguyên như lịch sử.

Giới hạn bảng: đóng lớp trong mã candidate và phạm vi hồi quy đã kiểm, không chứng minh mọi runner tùy ý cùng tiến trình là đáng tin. `co_ten` không phải chữ ký bảo vệ trước tác nhân tùy ý sửa code/kết quả. Không còn phép đo hạ tầng nào đang treo để đóng bốn lớp; nghiệm thu Windows/CI/toàn registry vẫn được ghi riêng, không tự coi là đạt.

## Tỷ lệ hội tụ §12 — lượt 8 → 9

- U = {`loi-luong-nen-bi-tinh-la-giet-dung`} — lớp duy nhất còn mở cuối lượt 8.
- F = {`loi-luong-nen-bi-tinh-la-giet-dung`} — đã kiểm đóng toàn lớp trên candidate, không chỉ F4g.
- **|F|/|U| = 1/1 = 100%.** Không cộng F1/F2/F3 vốn đã đóng vào tử số.
- Lớp mới: **0**. Lớp tái mở: **0**. Biểu hiện mới: **0**. Lớp/biểu hiện còn mở: **0/0**.
- Phần chưa đo: Windows thật, A4 toàn registry, CI/audit và canary như mục KHÔNG ĐO ĐƯỢC; không dùng tỷ lệ này để miễn các nghĩa vụ đó.
- Lịch sử F4 xuất hiện L2–L8 được bảo toàn; đây là phép đo sau checkpoint thứ hai được prompt giao, không tự gia hạn budget hoặc cấp lượt 10.

## Finding mới

Không có finding mới P0/P1/P2/P3 sau quét theo lớp. F3/P3 nguyên thủy đã đóng bằng bằng chứng, không cần waiver. Không có gợi ý bản vá vào candidate.

## Đối chiếu phạm vi việc gỡ phép đo chạy chồng

Đã đọc M1–M4/A1–A5 từ SPEC đúng băm. SPEC dòng 62 (M4) ghi: “một ca chạy bộ máy song song của M2 với hàm đột biến giả trả kết quả theo thứ tự xong bị đảo, và đòi đầu ra đúng thứ tự `DOT_BIEN`; một ca cho miền biến M1”. Dòng 70 (A3) ghi: “Thứ tự: ca tự kiểm M4 với thứ tự xong bị đảo ⇒ đầu ra vẫn đúng thứ tự `DOT_BIEN`”; đột biến yêu cầu là “gom theo `as_completed`”. Không dòng nào yêu cầu phép đo chạy chồng, Barrier, hoặc T4.

M2 vẫn yêu cầu vòng thực thi song song qua `ThreadPoolExecutor(N)` và bản gốc được tính trước/dưới khóa. Candidate giữ `chay_theo_thu_tu` dùng `ThreadPoolExecutor(n)` + `map`, giữ `lam_nong_nen` trước vòng và chỉ bỏ phép đo phụ ở c65/T4. M4/A3 vẫn gọi chính helper bằng executor điều khiển có Future thật, đối chứng `as_completed` trước phép thử, rồi chốt kết quả thứ tự; T3 vẫn có răng. Vì vậy việc gỡ phần phụ không tự cắt acceptance. Quyết định checkpoint được prompt dẫn #1322 comment 7046235668; không xác minh comment qua mạng và không lấy lời dẫn ấy thay phép đối chiếu SPEC.

## Quét lớp F4 trên các đường còn tồn tại

`class_scan.py` lập danh sách AST từ base/candidate rồi reviewer đọc từng đường: **12 lời gọi `bang` mới** tại c64 (4), `_thu_tu_tat_dinh` (1), c65 (1), c66 (2), c67 (3), c68 (1). Không thêm đường ném `TinHieuChotCa` trực tiếp. Đây là danh sách hỗ trợ kiểm chứng, không lấy số lượng AST làm bằng chứng đóng lớp.

| Đường cấp chốt | Phân biệt hành vi và hạ tầng |
|---|---|
| c64 miền cấu hình | So giá trị/mặc định và chỉ bắt ValueError ở đầu vào cố ý sai. Lỗi OSError của resolver truyền rc=4, không vào `bang`. |
| c65 n=1 và thứ tự n=4 | Lời gọi helper trực tiếp; lỗi trước/sau collector không bị nuốt. Fake truyền lỗi callback bằng `Future.set_exception`; hai kiểm tra sức khỏe fixture ném RuntimeError ngoài `bang`. Không còn phép đo chạy chồng. |
| Bộ thực thi điều khiển F1 | Vẫn có **luồng hoàn tất Future**; không tuyên bố đã gỡ mọi luồng phụ. Đã đo riêng cả instance đối chứng (pha 0) và instance của runner (pha 1): constructor/submit/callback/result/cleanup, luồng chết/treo, handshake hết 10 s, lịch chậm. |
| c66 miền trước ca + kết quả đúng kế hoạch | Spy và main thật trong fixture, không có subprocess lồng. Lỗi OSError/MemoryError trước/sau main truyền rc=4; chỉ kết quả hành vi sai mới qua `bang`. |
| c67 baseline trước mutation | Child được giả trong ca để ghi nhật ký đồng bộ dưới Lock, không kiểm phân hạng lỗi của child thật bằng `bang`. Lỗi runner/pool ctor/cleanup/thread_start truyền rc=4. |
| c68 đúng kết quả của chính việc | Hàm giả có kết quả riêng gồm SONG_SOT; không tự gọi chay_dot_bien_test/phan_hang lồng. Lỗi runner/pool ctor/cleanup/thread_start truyền rc=4. |
| Runner đột biến và phân hạng | Target/neo/baseline được kiểm trước child; timeout=124/HONG; rc=4 không đổi thành GIET dù có marker. Ranh giới được đo bằng `runner_boundaries.py`. |

`faults9.py` là phép tiêm trên **child đột biến chú thích vô hại** qua `chay_dot_bien_test` và `phan_hang` thật, baseline ngoài xanh. Trên 3.13: **56 phép = 5 SONG_SOT + 42 TIN_DUNG_GIA + 9 HONG, 0 GIET**. Năm SONG_SOT gồm 3 đối chứng c65/c67/c68 không lỗi và 2 lịch hoàn tất chậm nhưng hợp lệ. 9 HONG gồm 5 timeout tại seam 3 s và 4 SystemExit/KeyboardInterrupt. Có nhật ký điểm tiêm; log c66 có redirect stderr trong ca nên `MEASURE.injections` là xác nhận điểm tiêm. Timeout 3 s không phải đã đợi 300 s thật; handshake hết hạn trong fake vẫn đợi 10 s thật. Không dùng rc=0 của script thay các hạng child.

**F4g A/B:** giữ nguyên `association_repro.py`/`association_driver.py` lượt 8, thay bản sao nguồn đúng SHA. Trên cha `beccb067…`, helper pool 2 + pool chính alias 4: không lỗi SONG_SOT; abort **GIET giả** 0,184 s; chậm việc thứ tư **GIET giả** 10,695 s. Control không helper với cùng lỗi là TIN_DUNG_GIA. Trên candidate, 6/6 tổ hợp control/helper × none/abort/late_fourth đều SONG_SOT, **`waits=[]` trong mọi child**. Kết quả này chứng minh đường lỗi đã bị gỡ; không gọi đó là “đã tiêm lỗi rào và được truyền đúng”. Cùng phép candidate chạy lại trên 3.12; biến thể alias public lưu trước patch cũng 3/3 SONG_SOT, không gọi rào.

AST xác nhận không còn tên thực thi `Barrier`, `HAN_CHONG_C65`, `ghi_cau_hinh`, `xet_c68`, `c68_loi_luong_nen_la_tin_dung_gia`, c69/c70/c71 cũ, `_loi_cua_c68`, `_chay_c68_qua_seam`, `LoiHaTangLong`, `TIEN_TO_HA_TANG_C68`. `c68_moi_viec_dung_ket_qua_cua_no` hiện tại là ca khác, đã đo, không gộp với c68 cũ chỉ vì trùng số.

Các `fault_matrix.py`, `schedule_matrix.py`, `config_matrix.py` nguyên bản neo vào Barrier/HAN_CHONG/ghi_cau_hinh hoặc hàm `ham` cũ **không còn áp dụng nguyên trạng**; không chạy rồi ghi xanh giả. Phép đo đường còn sống được tái dẫn xuất trong `faults9.py`; `lifecycle_probes.py` và phản chứng F1 vẫn chạy nguyên bản.

Đo bổ sung M2 bằng `executor_contract.py` trong scratch, dùng ThreadPoolExecutor chuẩn có lớp con chỉ ghi nhận rồi gọi `super`: N=1 chạy trên luồng ca; N=2/4/8 tạo đúng một pool tương ứng, nhận đủ n+2 việc, n việc đầu có n worker thực, kết quả giữ thứ tự. Barrier chỉ là dụng cụ độc lập của reviewer trong phép này, không thêm vào candidate hoặc biến thành tiêu chí nghiệm thu mới.

Ma trận `faults9.py` trên **3.12.3** cũng đủ 56 phép, đúng **5 SONG_SOT + 42 TIN_DUNG_GIA + 9 HONG, 0 GIET**. Tất cả 11 mutation harness trên 3.12 cũng GIET. `evidence_check.py` đọc lại log và kiểm số hàng, hạng, xác nhận điểm tiêm, đối chứng, việc không gọi rào và việc restore; mọi kiểm tra đạt. Đây là audit hiện vật của phép đo, không thay các phép đo gốc.

## Phép đo độc lập

- `scope_audit.py`: diff Git khớp `goi/diff.patch`; một đường trong write set, +248/−4; `git diff --check` rc=0. AST 398 DOT_BIEN và 2 TU_KIEM cũ giữ nguyên; trong hàm cũ chỉ `main` đổi. Năm tệp của bản sao khớp byte checkout.
- Bare lint: `python3.13 -B -m ruff check --select F --no-cache` trên base/candidate trong cùng script: rc=0/0, delta=0. Ruff của đúng interpreter là 0.17.6; executable `ruff` trong PATH là 0.16.9 và không được dùng cho phép lint này. Đây không phải Ruff pin/probe contract của workflow.
- `recheck.py mutants`: 11/11 GIET trên cả 3.13 và 3.12, gồm T1/T2/T3/T5/T6/T7/T8/T18/T19/T20/T21; đọc hạng và marker, không chỉ mã thoát script.
- `acceptance.py`: 12 giá trị env sai đều subprocess rc=2, stdout 0 byte, spy thấy 0 ca/0 vòng; 1–8 hợp lệ; 18 tổ hợp nền/CPU đúng; generator tiêu thụ đúng một lần. A1 ngắn qua main/helper thật + tác vụ giả: gốc byte-equal N=1/4, T3 khác byte.
- `coverage_readback.py`: gốc N=1/4 đều kế hoạch 409, thực gọi 409 việc duy nhất, có đủ 11 mục harness, mỗi việc đúng một lần, 409/409 tên và chi tiết khớp. Các biến thể cắt/lặp/đổi nhãn được giữ riêng.
- `runner_boundaries.py`: chỉ đổi neo chú thích đã bị gỡ sang khai báo BIEN_TIEN_TRINH trên bản script trong R. Neo vắng/lặp/không thay đổi, target vắng và baseline rc=3/4/124 đều HONG, không gọi child; rc=3 sai marker và rc=4 dù đúng marker đều TIN_DUNG_GIA; rc=124 HONG.
- `lifecycle_probes.py` trên cả 3.13/3.12: fixture 100/100 xanh, 20 vòng × c65/c66/c67/c68 = 80/80 xanh, không luồng dư; restore đúng ThreadPoolExecutor. Lỗi submit/worker/cleanup của fake đều rc=4/TIN_DUNG_GIA; lỗi submit chờ 10 s thật rồi dọn luồng.

## Bộ đầy đủ và consumer registry

Ba lượt dùng đúng năm tệp candidate trong `R/original/`; không mock ca, kết quả vòng hay phân hạng. `full_readback.py` đọc receipt và raw stdout/stderr, kiểm mã thoát lẫn bằng chứng dương.

| Chế độ | rc candidate | Thời gian (s) | Stdout/stderr (byte) | Kết quả |
|---|---:|---:|---:|---|
| full-n1 | 0 | 1577.030 | 111/0 | CA 68/68; DOT BIEN 409/409; TU KIEM DAT (2); TONG DAT |
| full-n4 | 0 | 549.061 | 111/0 | CA 68/68; DOT BIEN 409/409; TU KIEM DAT (2); TONG DAT |
| full-default | 0 | 542.451 | 111/0 | CA 68/68; DOT BIEN 409/409; TU KIEM DAT (2); TONG DAT |

**A1 đầy đủ: đạt.** N=1 và N=4 bằng nhau từng byte sau bỏ duy nhất dòng TIEN TRINH; cả ba đầu ra chuẩn hóa cùng SHA-256 `4026278d38a42e69771695101264336dff8edceae7f92a48d2cd594eb14a8bc3`. Lượt env-vắng thật (`full_default.py` loại biến khỏi env child) chọn N=4 và stdout trùng byte với explicit N=4. Thời gian sandbox có tranh chấp giữa các phép đo, không thay canary A6.

`registry_probe.py`: consumer `bang_chung_xanh` + `chay_moi` thật nhận chính log N=4/rc=0 là `CI_DANG_KY ops/ci_provenance_test.py: ĐẠT rc=0`, 0 lỗi; chèn một dòng giữa CA và DOT BIEN ⇒ regex không khớp, 1 lỗi/ĐỎ. Đây là probe một mục registry, không phải toàn `--chay`.

`removal_control.py`: ép runner tuần tự trên bản sao thì c65 riêng lẻ xanh, nhưng T3 trở thành SONG_SOT và nghĩa vụ giết T3 thất bại. Không suy mọi cách giảm worker đều được c65 bắt; M2 thật được kiểm riêng bằng runner chuẩn và `executor_contract.py`.

## M1–M4/A1–A5 và giới hạn nghiệm thu

| Mục | Phép kiểm độc lập | Kết luận |
|---|---|---|
| M1/A2 | Miền 12 giá trị sai, 8 giá trị hợp lệ, 18 tổ hợp nền/CPU, CLI/spy, c64/c66 và T1/T2/T5 | Đạt trong phạm vi đã đo; mô phỏng nền không thay Windows thật |
| M2 | Runner chuẩn tại N=1/2/4/8; prewarm 62 khóa trước mutation; 409 việc duy nhất ở N=1/4; kế hoạch độc lập và kết quả gắn đúng việc | Đạt; chỉ gỡ phép đo chạy chồng phụ, giữ thực thi song song trong sản phẩm test |
| M3 | Log thật N=4; TIEN TRINH đứng đầu, bốn dòng tổng kết liền nhau; consumer thật nhận | Đạt |
| M4/A3 | c64/c65, bộ Future điều khiển, đối chứng âm, T1/T2/T3; 11 mutation harness ở cả 3.13/3.12; quét ngoại lệ không biến thành tín dụng | Đạt; không giảm tiêu chí thứ tự/miền khi bỏ T4 |
| A1 | N=1/N=4 đầy đủ cùng rc=0, cùng 68/68 ca và 409/409 đột biến, bằng byte sau bỏ TIEN TRINH; phép ngắn T3 khác byte | Đạt A1 trên gốc; đối chứng T3 qua phép ngắn/helper thật đã đỏ |
| A4 | Một mục consumer với log N=4 thật đạt; chèn dòng thì bị từ chối | Phép dương/âm riêng bộ này đạt; toàn registry `--chay` not_run |
| A5 | Bare Ruff 0.17.6 base/candidate rc=0/0; N=4 và env-vắng Linux đầy đủ đều đạt, đầu ra trùng byte | Linux mặc định đạt; Windows thật do executor đo riêng, KHÔNG ĐO ĐƯỢC ở đây |

Nguồn lịch sử SHA đầy đủ được lưu trong `R/history-sources.json`, đối chiếu với từng `goi/lich_su/luotN-VERDICT.md` (lượt 1 là bản tóm tắt). Source runtime của năm tệp copy được băm trong `R/scope.log`; chỉ khác candidate ở các bản sao mang tên mutation/variant.

## KHÔNG ĐO ĐƯỢC

- Windows thật theo chỉ thị do executor đo riêng. Linux 3.12 và mock Windows không thay vế này; `goi/EVIDENCE.md` ghi lượt exact candidate đang chạy, chưa có raw receipt Windows kết thúc.
- Không gọi mạng nên không xác minh remote refs, lease/budget live, required CI, audit/waiver hoặc comment checkpoint. Protocol copy `goi/PROTOCOL_DA_PHIEN.md` được prompt chỉ định; object `48d372e` không có trong checkout offline (`git show` rc=128), không tuyên bố đã đối chiếu blob với remote.
- A4 toàn registry, full repository selftest/gates, full_mutant_audit chưa chạy trong review này; consumer một mục đã đạt bằng log N=4 thật và đối chứng chèn dòng; phép đó không thay toàn registry.
- Không chạy lại cả bộ đầy đủ trên từng biến thể F3 hoặc trên T3; dùng ca thật c67/c68, main instrumented, readback danh tính và phép A1 ngắn cho các phản chứng ấy. Không suy chúng thành full-suite mutation runs.
- A6 canary sau land chưa tới thời điểm, không dùng thời gian sandbox thay số đo CI.
- Không mô phỏng mọi lịch OS, runtime Python, OOM thật hoặc suspend/resume. Hướng đường dẫn thoát cây chỉ mô tả: ràng buộc đích resolve trong cây tạm và từ chối tên/đường bất thường trước I/O; không soạn hoặc chạy payload thoát cây.

## Xác nhận cuối và hiện vật

`final_snapshot.py`: **17.356 tệp đầu/cuối, 0 đường đổi nội dung**, kể cả `.git`, ignored và untracked. Git HEAD/tree/cha/status/diff/index/config khớp snapshot đầu; checkout sạch. Năm tệp copy vẫn trùng byte checkout; SPEC vẫn đúng SHA-256. Đây là snapshot hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên hoặc mount read-only.

Mọi phép đo đã khởi chạy đều đã kết thúc. `R/command-results.json` ghi lệnh, rc script, thời gian, đường/size/SHA-256 stdout và stderr; raw rc/hạng child nằm trong log từng phép. Đọc rc của script cùng bằng chứng dương/âm; riêng các phép fault có lỗi child là đối chứng cố ý. Có script lượt 8 được chép nhưng không chạy; chỉ danh mục lệnh này xác nhận đã thực hiện.

Tái lập từ thư mục `rv9`, đặt `R=goi/review9.My7hQl`; các lệnh chính:

```sh
python3.13 -B "$R/f1_deterministic.py"
python3.12 -B "$R/f1_deterministic.py"
python3.13 -B "$R/recheck.py" mutants
python3.12 -B "$R/recheck.py" mutants
python3.13 -B "$R/faults9.py"
python3.12 -B "$R/faults9.py"
python3.13 -B "$R/full_runs.py" 1
python3.13 -B "$R/full_runs.py" 4
python3.13 -B "$R/full_default.py"
```

Các script, cặp neo/thay và log đều trong R; không có patch vào `cay/`. `R/evidence-manifest.json` băm hiện vật; `goi/VERDICT.sha256` băm báo cáo cuối. Không gọi mạng, không commit/push/merge/land và không cấp thêm lượt review.
