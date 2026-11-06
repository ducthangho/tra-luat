reviewed_sha: `3408591b7b318578a17c9b1ba00c1b87cee4f688`
spec_sha256: `c9bc8acac6710f8395b4ca88c69ef39dfaa1b3acbf468aa0eea2b3f7d530ef74`
provider: `openai_codex`
model/effort tự khai: Codex dựa trên GPT-6; mã model triển khai và effort không được surface hiện tại cung cấp để tự xác minh. Không suy danh tính model từ yêu cầu trong spec.
execution_surface: `codex_cli`; transport: `machine`, theo `../run/112cc186/run.json` của run hiện tại `112cc186a8d9426688fa26e857f60d10`.
verdict: `approve`

**Kết luận:** approve **đặc tả r9** trên đúng SHA/băm nêu trên. F19 đã vá thật; không phát hiện P1/P2/P3 mới. Đây không phải approval cho implementation hay quyền merge/land; các gate pha thi công giữ nguyên.

## Phạm vi và preflight

- Review độc lập toàn bộ `ops/specs/wp1179-c1a1b-r9.md`; không sửa kho được review.
- `git rev-parse HEAD`: rc=0, đúng reviewed_sha trên.
- `git rev-parse --is-shallow-repository`: rc=0, `false`.
- `git status --short`: rc=0, rỗng.
- `sha256sum ops/specs/wp1179-c1a1b-r9.md`: rc=0, đúng spec_sha256 trên.
- Tree HEAD: `6e15e75228a6eaa2462fa6d28816a6fc10eb24f9`; `origin/master` trong mirror là `d26b36f5d2f952c2d952d58517571ffe27c4f826`, đã là tổ tiên của reviewed_sha (rc0).
- Probe và bằng chứng mới chỉ ghi trong sandbox; Python chạy `-B` và `PYTHONDONTWRITEBYTECODE=1`.

## F19 — ĐÃ VÁ THẬT

| Nội dung | Trạng thái |
|---|---|
| r8→r9 không đổi oracle | Đạt: §1–§6 nguyên byte sau khi bỏ riêng cột đột biến A12; tiêu chí và nền A12 nguyên byte. Phần còn lại của diff là lịch sử/authority/lượt mới. |
| A12(h) giết lỗi reader cục bộ, không restart | Đạt: G8 `khong_do_duoc` → `qua`; G7 vẫn `khong_do_duoc`; đếm đúng 1 lần khởi tạo tiến trình. Đối chứng (e) vẫn không giết cùng mutant. |
| A12(f) giết ghi đè kết quả hoàn tất thành unknown | Đạt: G1–G5 `qua` → `khong_do_duoc`. Đánh giá lại thuần vẫn giữ vector, như r9 đã nói rõ. |
| A12(e)/(h) giết restart | Đạt: (e) G1–G8 → `qua`; (h) G8 → `qua`; mỗi mutant có 2 lần khởi tạo tiến trình. |
| A12(f2) giết xoá memo | Đạt: G4/G5 `qua` → `khong_do_duoc`; G1–G3 giữ kết quả. |

Lệnh: `PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/tmp" python -B verify_r9.py > evidence/verify-r9.log 2>&1`, **rc=0**. Output cuối: `F19_ALL_5_NAMED_WITNESSES_PASS`. Mỗi bản đúng qua trước; từng mutant bị `TinHieuChotCa` mang đúng tên ca đích. Trace: `evidence/r9-verification.json`; diff: `evidence/r8-r9.diff`. Đây là probe của reviewer trên object thật và batch reader thật, không phải acceptance của mã C1a1b chưa được triển khai.

## Review theo lớp

Áp ADR-0060 M2 và protocol §8.3: giữ slug qua các lượt, kiểm các đường cùng cơ chế, không coi tổng suite xanh là bằng chứng đóng từng lớp. Đối tượng là **đặc tả r9**, không phải PR thi công.

| Slug lớp | Nguồn / biểu hiện | Kết quả lượt 9, cách kiểm đóng lớp | Mức còn mở |
|---|---|---|---|
| `dot-bien-tuong-duong-hoac-thieu` | F3/F7/F14/F18; F19(a,b) ở r8 `caa5a0ec6a6bbc699c70dcfbd2541cb9ac9aec73` | **ĐÃ VÁ THẬT ở tầng đặc tả**. Đo 5 witness đúng tên cho F19 và các mutant phải giữ; đối chứng cục bộ ở (e) vẫn sống. Rà cả ABI, A9, A18, parser, guard kích thước/lưu trữ/memo và disposition nhóm chốt. | — |
| `phan-loai-vang-va-khong-do-duoc` | draft0–2, F4/F6/F11/F13/F16/F17 | Không tái mở. Bảng đóng × G6/G7/G8, tập đọc OID, alias và ba tài nguyên chung cùng kết quả. f2/deadline sau G3 cho hai vector khác nhau đúng luật. | — |
| `mo-rong-module-pha-hop-dong-json-thuan` | draft0–2; §0.2, A1–A3 | Không tái mở. Module mới tách riêng, JSON giữ nguyên byte/ba khoá, K3–K5 đỏ không chặn chẩn đoán Git; đối chiếu module JSON thật và suite nền. | — |
| `predicate-consumer-khong-khop-producer` | F2; G6/G7/G8 | Không tái mở. G6 không đọc leaf, nhận cả gitlink vắng; G7/G8 nhận ba mode blob, so OID trước đọc; symlink so chính blob đích chuỗi, giới hạn được khai. | — |
| `oracle-trang-thai-g0-mau-thuan` | F8; A6 | Không tái mở. G0 qua trên JSON nhỏ sai K1/K2; G0 do và JSON null khi quá trần; G1–G9 skip đúng hai nhánh. | — |
| `dat-lai-ngan-sach-khi-doi-truc` | F1/F9/F10; §8/§11, A21 | Không tái mở. `cap = allowance = 3`, `U_max` unknown; số đếm thô chỉ tăng cận dưới. CLI thật đọc lại limit=3; lời gọi thứ 4 bị chặn. | — |
| `huong-dan-cli-khong-khop-parser` | F12/F15; §11.2, A22 | Không tái mở. Init đủ mission rc0, thiếu rc2; limit0 rc2; rescue ID/URL rc2/0 trên state thử phù hợp. Không biến lời thuật/cặp cờ thành lệnh tự đứng. | — |
| `so-do-ke-thua-chua-do-lai` | F5; S2–S6 và §11.5 | Không tái mở. Đo lại trên đúng base: 5.444−1.084=4.360, giao lịch sử producer=64; byte/count/profile và +650/−93 khớp. | — |
| `nguon-duoc-tin-ma-chua-xac-minh` | lớp kế thừa C1a1a; N6/N7 | Không có biểu hiện mới trong scope: băm bytes, loại ảnh hưởng replace/env; exact ref ban đầu và ref cuối tách biệt. C vẫn tự khai, không chứng minh provenance run. | — |

Tập lớp mở cuối r8: **1** (`dot-bien-tuong-duong-hoac-thieu`, F19). Lượt 9 đóng **1/1 = 100%** ở tầng đặc tả; **0 lớp mới**, **0 lớp tái mở**. Hai biểu hiện của F19 không bị gộp mất: được kiểm riêng ở bảng trên. Nghĩa vụ kiểm mã cuối vẫn thuộc pha thi công theo chính §4, không dùng prototype để cấp `cross_approved` cho mã chưa tồn tại.

## Rà toàn bộ r9 / A1–A23

| Phạm vi | Đối chiếu và kết quả |
|---|---|
| §2.1, A1–A3 | ABI JSON cũ và module mới không trộn. Blob JSON tại base và HEAD cùng `3490ea0ee40081c0eba2d121f5b19a67a021a54b`; suite và registry cũng cùng blob. Receipt dựng từ đồ thị thật được `kiem_json` nhận; các ca K1/K2/K4 trả đúng vector cũ. |
| §2.2, A4–A6 | Bốn khoá top-level; bool riêng int; tập trạng thái đóng; `json=null` iff G0 do; serializer ASCII/sort_keys/newline xác định. Mô hình ưu tiên rc cho dương/đỏ/unknown/hỗn hợp/JSON đỏ/G0 đỏ = **0/12/13/12/12/12**. Tham số/N6 ban đầu có rc2 và stdout rỗng; chưa có CLI Git sản phẩm để đo byte stdout thật. |
| §2.3/§2.4 G1, A7; N1/N3/N4 | Fixture dùng MOC thật và clone shared. C=B/MOC qua; P/E/X do. Chuỗi Q không MOC đầy đủ cho do; xoá Q1 mới trong clone cho unknown đúng G1. Không dùng engine ancestry của Git để quyết luật; không thay hằng MOC. |
| G2/G3, A8; N2/N5 | S=B/C=A là strict ancestor ngược chiều, G2 do; H=X làm G3 do; S=C inclusive qua. Ràng buộc mọi parent, không cắt theo ngày/độ sâu/commit-graph rõ. |
| G4/G5, A9 | Ba root tree đôi một khác OID; T=tree(S) làm G4 do, tree_S=tree(H) làm G5 do; ca guard root trùng được bác. Guard fixture là nghĩa vụ mutant hạ tầng riêng, không lấy mutant module thay thế. |
| G6, A10; N8 | Đo cả 5 mode với OID khớp và null, vắng với null/hex, ancestor blob với null/hex. Gitlink tới object không tồn tại vẫn qua khi khớp; không đọc leaf. `KhoObject.tim` producer được đối chiếu trực tiếp. |
| G7/G8, A11; F6/N7 | Cả hai luật: 100644/100755/120000 qua; 160000/40000 do; vắng/non-tree do; OID khớp + blob vắng unknown; **OID lệch + blob vắng do**. G8 sha256 trên nội dung blob và ca sha256 lệch đúng. Bác gitlink/tree chặt hơn producer đã khai rõ; không suy rằng G7 chứng minh nội dung Python thực thi. |
| Reader, A12 | Missing, băm lệch, replace, env, chết sớm/muộn/sau G3, framing đồng bộ/hỏng có đối chứng. Tập đọc và vector được đo trên object thật. F19 đóng như bảng riêng; mutant lỗi cục bộ được kiểm có đúng **1** lần start, không ghép thêm restart. |
| §2.5, A5/A14; N6 | `for-each-ref` exact-name cần lọc đúng tên, không nhận ref con theo prefix. Đo ref con/đổi/xoá trên clone; G9 unknown khi drift/vắng. N6 ban đầu rc2 khác G9; G9 qua tiến trình riêng, không bị reader chết làm hỏng. Nguồn ba OID caller vẫn là hợp đồng C1b. |
| §2.6, A13 | Cap walk cục bộ theo phép đi; cap object theo OID; cap tổng chặn đọc mới; deadline chặn mọi luật chưa hoàn tất kể cả memo/G9. Đã đo guard dương/âm cho object, tổng và thời điểm memo. Kết quả hoàn tất giữ nguyên. Biên G0 8.388.608/8.388.609 có oracle phân biệt. |
| §3, A15 | Write set đúng **2 đường**, module mới + suite cũ đã đăng ký, không sửa sổ. Trần ≤750 dòng là ngoại lệ có authority được prompt xác nhận. Ước ~710 được ghi là ước, không phải số đo; chưa có mã để nghiệm thu numstat. Danh sách holder là lịch sử và có yêu cầu đo lại trước lease. |
| A16/A17 | Windows local trên máy chủ kho vẫn required; phải base/candidate cùng máy/cùng lệnh, không tính skip. Miễn full mutant ở lượt Windows tập trung không miễn CI Windows hay M9 full_mutant_audit Ubuntu/waiver đúng scope. Chưa có mã thi công nên không khai đã nghiệm thu hai tiêu chí này. |
| A18 | Child dương đứng trước fault injection; đủ bản chép suite/hai module/registry, ROOT chứa MOC truyền rõ, cờ chống đệ quy. Âm phải đúng lỗi import Git và không có dòng tổng khớp regex. N_git/M_git zero tách riêng, tổng cộng hai nhóm; caller nuốt import là mutant suite riêng. Không còn lỗi setup/mapping như F3/F7. |
| A19 | Doctrine/ADR và diff check riêng spec xanh. Ruff không chạy được do môi trường thiếu module; không tính là pass. Gate mã thi công vẫn phải làm ở pha thi công. |
| A20 | Đối chiếu từng sự kiện E với cột đọc: G1–G8 đọc object, G9 đọc ref riêng; OID lệch không làm phát E trên blob chưa đọc. A20 yêu cầu bảng nghĩa vụ từ mệnh đề, không sinh ngược từ số ca; ca không phân biệt/tương đương chưa chứng minh phải unresolved. |
| A20b | Đối chiếu đủ **12 chốt** với producer (c1/c2, t1–t10). Probe an toàn đo 7 dạng tree hỏng × 3 vị trí, c1 thiếu/sai và c2 sai tại H1, cùng đối chứng hợp lệ. t2 bỏ riêng còn bị t5/t3 che; bỏ nhóm t2+t3+t5 phân biệt trên mẫu không dấu cách. Các tên mang ý nghĩa thoát thư mục chỉ rà bằng lời/nguồn theo chỉ thị, không tự dựng payload (chi tiết dưới). |
| A21/A22, §8/§11 | CLI thật đã đo limit=3, default=2, limit0/mission thiếu bị bác, record-codex-call chặn trước lần4; rescue nhận URL và bác ID. State này là fixture parser trong sandbox, không phải journal thật của packet. Đường phục hồi journal production vẫn unknown như spec khai. |
| A23 | Oracle không gọi Reader/evaluate/module sản phẩm; bảng tập đọc **10/10** khớp OID. Guard âm OID/storage/size/memo phân biệt; alias mới loose và không nằm nguồn, xoá có hiệu lực thật; alias cũ bị bác. Xoá/băm lệch object chung làm G6/G7 unknown, G4/G8 qua. |
| §5–§7, §10/§11.7 | Scope giữ C1a1b; C1a2/C1b, T2/Q17/#564/#656/#499 và tối ưu #1160 không bị kéo vào. Receipt thật S≠C, Windows/cold cache và symlink workflow vẫn chưa đo, không làm bằng chứng mạnh hơn thực tế. |

## Phép đo và bằng chứng tái lập

Các lệnh Python dưới chạy từ sandbox với `PYTHONDONTWRITEBYTECODE=1`, `-B`, `TMPDIR="$PWD/tmp"`. Probe cũ đã **chép vào sandbox, đọc mã rồi chạy lại**; `measurements.py`/`cli_probe.py` neo HEAD r9, `guard_audit.py` đọc r9. Bỏ nhãn mutant `local_death` cũ vốn thực chất restart; dùng mutant cục bộ không restart riêng trong `mutation_probe.py`. Không lấy log lượt 8 làm kết quả lượt 9.

| Lệnh | rc / kết quả dương | Evidence |
|---|---|---|
| `python -B graph_probe.py` | 0; **41** lượt mô hình trên Git thật; fixture dương 12 object / 134.396 byte | `evidence/graph-probe.log`, `graph-runs.json`, `graph-oids.json` |
| `python -B verify_r9.py` | 0; **5/5** witness đúng tên, kiểm thêm đối chứng không phân biệt (e) và nguyên byte oracle | `evidence/verify-r9.log`, `r9-verification.json`, `r8-r9.diff` |
| `python -B coverage_probe.py` | 0; **74** lượt mô hình; G1–G8/modes/parser/JSON thật/guard dương-âm | `evidence/coverage-probe.log`, `coverage-runs.json` |
| `python -B guard_audit.py` | 0; **10/10** tập đọc, mutant oracle gọi evaluator bị guard cấu trúc bác; tài nguyên sau G3/G5 đúng | `evidence/guard-audit.log`, `class-scan.txt` |
| `python -B ref_env_probe.py` | 0; ref thay/xoá → G9 unknown; env lọc cho cả G qua, mutant không lọc cho G1–G8 unknown | `evidence/ref-env-probe.log` |
| `python -B measurements.py` | 0 của driver; rc từng lệnh con ghi riêng, gồm rc âm dự kiến và diff toàn cây đỏ | `evidence/measurements.log`, `measurements.json` |
| `python -B cli_probe.py` | 0 của driver; init/status rc0, missing mission/limit0 rc2; call1–3 rc0, call4 rc3; rescue ID rc2 / URL rc0 | `evidence/cli-probe.log`, `cli-runs.json` |
| `python -B final_checks.py` | 0; dựng cả hai bản JSON base/HEAD trong cùng một lệnh, cùng 3 tệp phụ thuộc/cấu trúc, chạy cùng lệnh suite: cả hai **156/156 · 162/162 · equivalent 9 · unresolved 0**. Diff toàn bộ tập phụ thuộc rỗng; t2 đơn tương đương nhưng bỏ nhóm phân biệt. | `evidence/final-checks.log`, `final-checks.json` |

Các số neo **base `889334fb87c25136a13c6776a40a25b401820e04`**, không thay bằng HEAD đang review:

| Số đo | Kết quả mới | Lệnh / rc |
|---|---|---|
| S2 first-parent gồm MOC | **411** | `git rev-list --count --first-parent 601a0f18c83057fa079d204122660f5697fc6389^..<base>`; rc0 |
| S2 reader dừng trước đọc MOC | **410 commit / 531.751 byte**, 0,018 / 0,019 s | `python -B do_profile.py <kho> <base> <MOC>` ×2; rc0 |
| S3 mọi tổ tiên | **5.444 / 8.480.418 byte**, 0,228 / 0,192 s | cùng hai lệnh profile; rc0 |
| S4 tập hiệu/giao | all=5.444, first-parent=1.084, hiệu=**4.360**, log producer=64, giao=**64** | `rev-list`, `rev-list --first-parent`, `git log --format=%H <base> -- ops/lease_publish.py`; rc0 từng lệnh, driver tính tập |
| S5 producer+workflow | **2 tệp, +650/−93** (649/92 + 1/1) | `git diff --numstat <MOC> <base> -- ops/lease_publish.py .github/workflows/ops-thu-hoi-admission.yml`; rc0 |
| S6 suite JSON hiện có | **156/156 ca**, **162/162 mutant**, equivalent=**9**, unresolved=**0** | `python -B .claude/dev/doc_receipt_thu_hoi_test.py`; rc0 |
| Sổ test | **29/29** đăng ký, **1.070/1.070** phản chứng | `python -B .claude/dev/ci_dang_ky_test.py`; rc0 |
| Doctrine / ADR | **10 tệp/0 vi phạm**, **64/64** | `packet_loop.py doctrine-scan --root .` / `adr-song`; rc0 |
| §11.5 drift lịch sử | đúng **1 tệp, +698/−92**, `.githooks/eol_policy_test.py` | `git diff --numstat <base> 08bcb51fbed359eaeeca41bc3a0559fe308c0aa9`; rc0 |
| Kích thước spec/suite hiện có | r9 **949 dòng / 112.153 byte**; suite JSON **535 dòng** | `guard_audit.py`; rc0 |

Thời gian mới khác thời gian lịch sử là phép đo mới trên cache/máy này, không phải mâu thuẫn của số liệu lịch sử. Môi trường mới: Linux `6.18.44-fc-v242`, Python `3.13.18`, Git `2.43.0`.

Guard tài nguyên được đo bằng OID thật: cap tổng **300.910** > nhu cầu G6/G7/G8 **3.925 / 115.753 / 15.474**; reset tổng theo luật làm G6–G8 qua. Cap object **111.793**, H1 **300.214**, mọi object khác tối đa **111.792**; bỏ cap làm G3/G4 qua. Fixture thường có cap tổng **912** < **115.753**, bị guard âm bác. Không ghi nhận guard sai là ca skip.

## Ngân sách / authority / giới hạn

- Đối chiếu ADR-0043 (ba trục độc lập, nâng trần có authority), ADR-0052 (cách đếm và điều kiện cấp lượt sau), ADR-0055 (opt-in 10), protocol §12 và các quyết định chủ kho được prompt xác nhận. Spec giữ một lịch sử lời gọi; `U_lower=12` trước lượt này, ít nhất 13 khi lượt này có output; **không** suy ra U chính xác hoặc số dư.
- `cap=3` của pha thi công là allowance có thẩm quyền được khai là ngoại lệ khi U_max unknown, **không** phải bằng chứng tổng chi ≤16. Thêm lượt spec 7/8/9 không tự tăng allowance thi công. Lượt này là lượt xác minh duy nhất, không gọi reviewer hay sub-agent khác.
- Ba token ADR-0055/0053/0060 đều duy nhất; các phép `cat-file -e L:path`, `L^1:path` và membership first-parent cho **0/128/có** trên mirror không shallow. Đây là phép đo ref trong mirror; không khai đã fetch từ mạng trong lượt này.
- `git diff --check <base> <HEAD> -- ops/specs/wp1179-c1a1b-r9.md`: **rc0**. Cùng lệnh không lọc path: **rc2**, whitespace trong các evidence lịch sử. Review này không kết luận toàn cây đủ gate merge và không sửa evidence nguồn.
- Ruff: gọi thật trả **rc1**, `No module named ruff`; **not_run** đối với lint. Mã Git sản phẩm, byte stdout CLI thật, numstat ≤750, Windows local/CI, full mutant audit và receipt thật S≠C: **chưa nghiệm thu**, đúng giai đoạn spec.
- A20b: các chốt tên đặc biệt có thể mang ý nghĩa thư mục hiện tại/cha, phân tách đường dẫn hoặc thư mục quản trị chỉ được đối chiếu bằng lời với từng predicate producer. Cách thử cho executor: đặt một tên chỉ vi phạm đúng chốt đang xét trong tree băm đúng, lần lượt tại ba vị trí có guard OID; kiểm tập luật đích và giữ màu; bỏ đúng chốt phải làm oracle đổi màu. Không tự soạn payload thoát thư mục trong lượt này. Disposition trên **mã cuối** vẫn phải được kiểm như §4 yêu cầu.
- Holder hiện thời, số ref live 776, trạng thái máy Windows, quota và journal dispatcher cũ không được đo mới; các số ấy trong spec được gắn rõ thời điểm/lịch sử hoặc unknown và đòi đo lại trước lease. Không biến chúng thành kết quả hiện thời.

## Finding mới

Không phát hiện finding mới trong đặc tả r9; không tạo F20 giả để ghi các nghĩa vụ thi công chưa đến giai đoạn nghiệm thu.

## Kiểm cuối và tính toàn vẹn

`PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/tmp" python -B snapshot.py evidence/source-after.json evidence/source-before.json`: rc0, **12.919 mục, `delta []`**. So sánh bao gồm hash bytes các tệp ngoài `.git`, HEAD/tree/ref, index, diff staged/unstaged và status có untracked/ignored; hai snapshot bằng nhau. Không sửa kho được review. Spec cuối vẫn đúng băm đầu tệp. `evidence/manifest.sha256` ghi băm probe và log của lượt này.

TONG: P1=0 P2=0 P3=0
