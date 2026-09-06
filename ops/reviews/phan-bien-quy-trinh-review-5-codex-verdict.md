# Review độc lập lượt 5 — PR #452 sau merge

**Kết luận: `changes_requested` — 3 finding P2, 1 finding P3; không có P1.** Hai bản vá test đã sửa được phản chứng cụ thể của lượt 4. Tuy nhiên, bộ phân hạng vẫn cấp tín dụng giết cho một crash vô can qua subprocess, và chốt shell mới có đường báo sạch khi phép đo hỏng. Nên mở PR vá riêng cho hai lỗi mã này; hai finding tài liệu có thể gom vào một PR hiệu chỉnh.

## Mỏ neo và phạm vi

- `reviewed_sha`: `4951f5517cc9cc7fbde060aa11c7ca5e5db0823c`.
- `reviewed_tree`: `f79e4e5b7dd4cbe0dc6c03b5f8e860fae86b9912`.
- Diff chính: `2fb43fc8e3fd6dacd6bb9e42731e751d3de2e262` → `bbf05eae1d2993eabb94db65452062a0c576fbee`, 7 tệp.
- `bbf05ea` là tổ tiên của HEAD. Sáu tệp nguồn/test/tài liệu chính của các probes không đổi giữa `bbf05ea` và HEAD (`git diff --quiet`, rc=0). Cây HEAD có thay đổi khác do merge; verdict này **không review toàn bộ phần chênh đó**.
- Authority: yêu cầu trực tiếp của người dùng và toàn bộ `prompt.snapshot` lượt 5; SHA-256 prompt: `9475fab239f4a23ba0db9523eddd1037c54c78e95be054e6a0395324b04b6993`. Đây là review ad-hoc sau merge, không tự tạo Packet/lease/generation/spec hash hoặc reset review budget. Không có Packet revision/generation được cấp trong chỉ thị; không khai rằng đã xác minh các trường ấy.
- Role: reviewer độc lập; provider `openai_codex`; model GPT-6/Codex theo danh tính phiên; execution surface: **Codex service qua API, có công cụ shell**; transport `machine`. Không phải ChatGPT Web. Không có receipt độc lập chứng thực model/session của lượt này; không tự cấp approval/land authority.
- Phạm vi có harness dùng chung; xem là ít nhất `systemic`, áp mức thận trọng `sensitive` cho kết luận về cổng. Không sửa nguồn, không commit/push/merge/deploy/LIVE. Chỉ tạo `VERDICT.md` trong clone được giao.
- Clone sạch lúc bắt đầu; detached đúng HEAD; 1710 commit; `core.abbrev=7`; remote `https://github.com/ducthangho/tra-luat`. Hai clone phục vụ thử nghiệm dựng cùng một lệnh tại `/tmp/rv5-audit/{head,before}`; đột biến chỉ ở thư mục tạm.
- Linux, Python 3.11.15, PyYAML 6.0.1, jsonschema 4.26.0, actionlint 1.7.7, Bash 5.2.21. Không có shellcheck thật trên PATH. `t2` vẫn đo được bằng actionlint thật và cơ chế che shellcheck sẵn có; không dùng điều này để khai đã chạy toàn bộ luật ShellCheck.

## ĐỐI CHIẾU LƯỢT TRƯỚC / H1

| Finding lượt 4 | Kết quả tự kiểm |
|---|---|
| **R4-01** — gộp locator với băm | **ĐÃ VÁ THẬT ở phân rã số và MVP-2**. Đọc YAML tại bốn snapshot `c03a409`, `2fb43fc`, `bbf05ea`, HEAD đều ra **44 / 3 / 3 / 32 = 82**. Ba locator-only đều khai `ban_thao_chua_duyet`. Không kiểm băm/thẩm quyền từng lease; “44 có trường băm” không phải 44 đã tuân thủ. Trang §1 vẫn dùng câu “lease đang làm đúng bằng tên khác” mà không có bằng chứng cho quần thể đó; nên viết dưới dạng rủi ro có điều kiện. |
| **R4-02** — quyết định mâu thuẫn | **VÁ HỜ**. §1 mới có thứ tự 1–5 và khai rõ thứ tự là phán đoán; phần cũ lớn đã chuyển sang I với nhãn hết hiệu lực. Nhưng phụ lục E vẫn tự gọi là bản đã sửa, gọi MVP-4 là số một; liên kết nội bộ không được chuyển theo mục mới. Chốt shell không phát hiện các lệch này. R5-02, R5-04. |
| **R4-03** — sai quần thể reviewer đã tiếp xúc | **ĐÃ VÁ THẬT trong kết luận hiện hành**. Tự đọc ba Git snapshot: câu `61–99%` vắng ở `07eb236`, `ba76a78`, có ở `d3bc218`. §1.3 rút suy luận nhân quả provider; README thêm đính chính và giữ receipt lịch sử. Không sửa hồi tố receipt lượt 3 là phù hợp. |
| **R4-04** — crash được tính là giết | **VÁ HỜ ở cấp lớp; phản chứng cụ thể đã vá thật**. Mutant t13 mới giữ metadata, trả JSON hợp lệ và chết đúng assertion trạng thái. Chạy lại **replacement t13 cũ lấy nguyên từ AST bản trước** dưới bộ phân hạng mới → `tin_dung_gia: JSONDecodeError`. Nhưng crash qua subprocess vẫn lọt, R5-01. |
| **R4-05** — ba ca comment đo nhầm head | **ĐÃ VÁ THẬT trong phạm vi ba ca**. Control đạt; gỡ lời gọi sổ comment → cả ba đỏ vì đòi rc=5 nhưng được 0. Gỡ riêng kiểm sai transition chỉ làm ca sai transition đỏ; gỡ kiểm consumed chỉ làm ca dùng lại đỏ. Không thấy hồi quy do thêm HEAD hoặc `_doi_ly_do`. |

**Bộ phân hạng và âm tính giả:** chạy 5 tự kiểm có sẵn, tất cả đúng kết quả mong đợi. Chạy riêng **18 cặp control–mutant hiện có**, đọc chi tiết assertion của từng đích: 18 control qua, 18 mutant chết đúng thuộc tính đang đo; **không thấy âm tính giả trong tập này**. Không suy thành bộ phân hạng đã đúng với mọi crash/fixture; các ca tự kiểm đều nằm trong cùng tiến trình và bỏ sót đường R5-01.

**Quét lớp comment/SHA:** chọn toàn bộ ca có `_doi(5,...)`/`_doi_ly_do(5,...)`, thêm `record_post*` và đối chứng transition hợp lệ: **11 ca control đều đạt**, ghi lại args/rc/stderr từng lời gọi. Gỡ sổ comment làm đúng bốn ca sổ comment đỏ (ba ca vừa vá và ca dùng lại); các ca SHA vẫn qua. Neo `chưa có trong sổ` và `thiếu --comment-id` phân biệt được nhánh hiện hành. Neo `accepted` yếu hơn vì chỉ là tên state, nhưng trong các đường lỗi hiện tại đã đọc không thấy thông báo cạnh tranh làm ca này xanh nhầm. Không ghi finding chỉ vì khả năng đổi câu chữ trong tương lai; nếu ổn định giao diện lỗi thì dùng reason code, không assert nguyên văn cả stderr.

## R5-01 — P2: `bang()` ở chốt khởi chạy vẫn biến crash thành `giet_that`

**Vị trí:** `ops/cong_cu_test.py:493–498`, cùng `:580` và `_tu_kiem_phan_hang` tại `:852`.

Lớp ngoại lệ riêng chỉ chứng minh lỗi đi qua `bang()` của ca đang chạy. Nó không chứng minh **assertion nghiệp vụ đích** đã chạy. Ca t22 dùng chính `bang()` để kiểm subprocess khởi chạy thành công trước khi đọc các kết quả A/B/C/D.

**Đo:** thêm duy nhất `raise KeyError("rv5_unrelated_crash")` ở đầu `_bash_windows` trên bản sao. T22 control là `qua`. Mutant chết với child rc=1, stdout rỗng, traceback `KeyError`; không tới phép kiểm chọn Git Bash. `_chay_1_ca` vẫn trả:

```text
giet_that — gọi _bash_windows hỏng: rc=1 ... KeyError: 'rv5_unrelated_crash'
```

Chạy toàn bán kính bằng `_do_ban_kinh`: **chỉ t22 chết**, không có ca `tin_dung_gia`. Vì vậy cả kiểm tên ca, bán kính 1/23 và nhánh xét `gia` của runner đều không ngăn được tín dụng này. Đây là lỗi phân hạng theo hợp đồng của chính bộ test, không khẳng định crash không phải lỗi sản phẩm cần bắt.

**Hậu quả:** thêm một mutant hỏng khởi chạy vẫn được báo “giết đúng”, dù chưa thử thuộc tính mutant muốn đo; bản vá R4-04 chưa đóng cả lớp.

**Cách vá:** tại harness, tách lỗi dựng fixture/khởi chạy/giải mã khỏi tín hiệu assertion nghiệp vụ; tại t22, kiểm child chạy được bằng đường không cấp tín dụng giết đích. Gắn định danh **chốt**, không chỉ tên ca, nếu một ca có nhiều loại assertion. Không dùng tìm chuỗi `Traceback` làm cơ chế chung. Những ca có chủ đích kiểm process crash phải khai riêng thuộc tính đó.

**Ca khóa:** giữ nguyên mutant t22 hiện có (bỏ loại SystemRoot) → phải giết thật ở phép so A; mutant crash ở trên → tín dụng giả; control → qua. Thêm tự kiểm subprocess vào bộ phân hạng. **Rủi ro sửa:** hạ mọi rc khác 0 thành tín dụng giả sẽ làm mất tín dụng hợp lệ của ca kiểm mã thoát; phải phân biệt theo hợp đồng của từng chốt.

**Tái hiện đã chạy:** `python -B /tmp/rv5-audit/probes.py` → rc=0, xem `probes.json` các khóa `t22_control`, `t22_crash`. Script thu thập thành công không phải mutant đạt. Phép đo dùng mã test thật, không giả exception của harness. **Đáng mở PR vá riêng.**

## R5-02 — P2: chốt shell đồng nhất phép đo thất bại với “không tìm thấy”

**Vị trí:** `ops/kiem_trang_quyet_dinh.sh:17–25`, nhất là điều kiện `if ... grep -nE` tại dòng 18.

`grep` trả 1 khi không khớp và 2 khi không thực hiện được phép đo, nhưng cả hai đều rơi xuống nhánh in sạch. `set -euo pipefail` không chữa được lệnh nằm trong điều kiện `if`. Kiểm số dòng cũng không xác minh đủ hai mốc cấu trúc.

**Phản chứng trên bản sao, giữ nguyên nội dung quyết định:**

| Đầu vào/phép gây lỗi | Mã thật | Quan sát |
|---|---:|---|
| Tài liệu nguyên trạng | 0 | “đã soi 77 dòng” |
| Đổi pattern trong bản sao script thành regex không hợp lệ | **0** | stderr `grep: Invalid regular expression`, stdout vẫn “trang quyết định sạch” |
| Bỏ mốc mở | 2 | KHÔNG ĐO ĐƯỢC, đúng |
| Tệp không tồn tại | 2 | awk không mở được tệp; không báo sạch |
| Cắt tài liệu ngay trước PHỤ LỤC, giữ nguyên §1/§2 | **0** | Thiếu mốc kết thúc vẫn báo soi 77 dòng và sạch |
| Đổi tên mốc PHỤ LỤC, giữ toàn bộ nội dung | **1** | Quét tràn sang lịch sử, quy thành lỗi nội dung quyết định |

Pattern lỗi là fault injection vào mã đo; không nói regex hiện hành đang sai. Nó chứng minh nhánh xử lý lỗi của grep không có ngữ nghĩa mã 2 như mong muốn. Thiếu mốc cuối còn cho hai kết luận 0/1 tùy phần văn bản phía sau, thay vì báo không xác định được phạm vi.

**Cách vá:** bắt riêng trạng thái grep (0=khớp, 1=không khớp, khác=KHÔNG ĐO ĐƯỢC), kiểm đúng một cặp mốc theo thứ tự và rào đóng trước khi kết luận nội dung. Báo lỗi công cụ/mốc bằng rc=2. **Ca khóa:** bảng trên phải cho 0/2/2/2/2/2 theo thứ tự; thêm đối chứng chứa chuỗi cấm thật phải rc=1. **Rủi ro sửa:** đặt ngưỡng dòng tùy tiện hoặc parser quá rộng sẽ lại bắt oan tài liệu hợp lệ; cố định cấu trúc được hỗ trợ và báo phạm vi đo rõ ràng.

**Tái hiện đã chạy:** `python -B /tmp/rv5-audit/shell-probes.py` → rc=0; mã của từng lần gọi shell lưu trong `shell-probes.json`. **Đáng mở PR vá riêng**, có thể cùng PR R5-01 nếu vẫn giữ phạm vi review rõ.

**Các giới hạn khác của H2 đã đo:** mẫu khớp token `61%` nhưng không khớp `61,0%` — cả hai token lấy từ chính tài liệu hiện hữu, không soạn câu tấn công mới. Chuyển nguyên hàng đang tuyên bố **rút** 61% từ phụ lục lên phần được quét → rc=1, dù hàng ấy không khôi phục kết luận đã rút. Vì vậy đây chỉ là kiểm chuỗi cấm; nó không tự chứng minh nhất quán ngữ nghĩa. Sửa định dạng số có thể làm lọt, trích dẫn để bác có thể làm đỏ giả. Cách rẻ là hạ đúng lời khai của công cụ; đừng hứa một blacklist văn bản sẽ hiểu mọi cách diễn đạt. Chưa chạy thêm các hình thức nội dung nhạy cảm hoặc tự soạn chuỗi khai thác, đúng ràng buộc giao việc.

## R5-03 — P2 / H4: cổng mirror được chọn để thi công kiểm sai tập đầu vào

**Vị trí:** `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md:42`; ý tưởng tương tự ở `:483–486`. Đối chiếu `docs/PROTOCOL_DA_PHIEN.md:539–559`.

Bước số 2 mới chọn điều kiện “**verdict** mang khẳng định định lượng mà không kèm bằng chứng đã cấp mirror”. Protocol §8 đòi phân loại các khẳng định phụ thuộc kho trong **đặc tả, handoff, bảng bằng chứng hoặc verdict** ngay khi đóng bundle. Chỉ kiểm verdict bỏ sót trường hợp con số cần review nằm trong spec/bảng đầu vào mà verdict không lặp lại nó. Nếu hiểu verdict là đầu ra của lượt sắp chạy, kiểm ở đó còn quá muộn để cấp năng lực cho lượt ấy.

**Hậu quả:** có thể cấp bundle thiếu mirror cho đúng người cần đo số; reviewer chỉ trả kết luận định tính thì điều kiện đã chọn không kích hoạt. Việc “đã cấp mirror” cũng cần bằng chứng chạy được và đúng dữ liệu, không chỉ trường tự khai có mặt. Đây là lỗi của thiết kế đang được chọn trong trang quyết định, **chưa phải lỗi runtime của một cổng đã triển khai**. Ý tưởng cũ đã có trong phụ lục bản trước; diff mới đưa nó thành bước thi công hiện hành.

**Cách vá:** sửa hợp đồng bước 2 tại trang quyết định theo tập đầu vào đầy đủ và thời điểm preflight của §8; ghi cụ thể cách xác minh kho/commit/ref cần thiết và một lệnh đo được trong sandbox. Không bắt mọi review thuần văn xuôi phải có mirror chỉ để đủ trường.

**Ca khóa đề xuất, chưa triển khai/chưa chạy cổng mới:** bundle chỉ có con số phụ thuộc kho trong spec, verdict không chứa số, thiếu mirror → từ chối trước review; cùng bundle có mirror dùng được → qua; mirror có tệp nhưng không đọc được revision cần đo → không đo được. **Rủi ro sửa:** bộ lọc đoán đơn vị số hoặc chỉ đếm có thư mục `.git` sẽ tái tạo đúng lỗi “có mặt ⇒ có khả năng”.

**Tái hiện đối chiếu đặc tả đã chạy, rc=0:**

```bash
sed -n '39,45p' ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md
sed -n '539,559p' docs/PROTOCOL_DA_PHIEN.md
```

Đây là finding tĩnh với tình huống thiếu đầu vào được mô tả bằng lời, không khai đã đo hành vi của cổng chưa tồn tại. **Nên sửa trong PR tài liệu trước khi giao triển khai bước 2.**

## R5-04 — P3 / H3: đổi mục nhưng để lại con trỏ và “bản đã sửa” của thứ tự cũ

**Vị trí:** tài liệu `:156`, `:438–440`, `:462`, `:483–490`, `:755`.

Sau tái cấu trúc không còn mục §0, nhưng đoạn **mới sửa** tại 438/462 vẫn dẫn “xem §0”. Bảng số nay ở phụ lục A. Phụ lục E tự giới thiệu “dưới đây là bản đã sửa, xếp lại theo thứ tự rẻ-trước”, rồi gọi MVP-4 là việc số một và hoãn phần còn lại theo MVP-1; §1 đã chọn một thứ tự khác. Cuối J vẫn có câu “R4-02 ... CHƯA xử lý”. Nhãn lịch sử chung ở đầu phụ lục giảm mức nghiêm trọng, nhưng chưa đáp ứng lời hứa §1.4 rằng thứ tự và trạng thái khớp phần bằng chứng.

**Hậu quả:** người theo liên kết kiểm chứng từ trang quyết định gặp mốc không tồn tại và khó phân biệt phiên bản khuyến nghị. Đây là lỗi biên tập, không chứng minh runtime hỏng.

**Cách vá:** đổi con trỏ tự dẫn sang A/E/F phù hợp; giữ lịch sử nhưng gắn revision/trạng thái hết hiệu lực ngay phần E/J liên quan hoặc chuyển thứ tự cũ vào mục I. **Ca khóa:** kiểm con trỏ nội bộ resolve; đọc riêng bảng §1 và mục E phải thấy rõ chỉ bảng nào có hiệu lực. **Rủi ro sửa:** thay toàn bộ chuỗi § bằng máy có thể sửa nhầm tham chiếu sang protocol; phân biệt con trỏ tự dẫn và nguồn ngoài.

**Tái hiện đã chạy, rc=0:**

```bash
rg -n '^#|xem §0|Phân rã đúng ở §0|MVP-4.*SỐ MỘT|CHƯA xử lý' ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md
```

**Không cần mở PR riêng chỉ cho P3 này**; gom cùng R5-03.

## H3 — Bảo toàn nội dung và giới hạn kết luận

**Sạch về thất lạc nội dung thực chất trong diff đã so:** đã đọc diff, đối chiếu các dòng bị xóa với toàn văn bản mới bằng multiset dòng rồi kiểm tay những dòng không còn. Khối kết luận cũ chuyển nguyên sang I; các xóa còn lại là metadata/header cũ, phép đếm được thay, kết luận provider bị rút. Không tìm thấy một đoạn bằng chứng quan trọng bị xóa ngoài chủ đích tái cấu trúc. Không coi mọi câu sai được giữ trong mục I có nhãn hết hiệu lực là finding mới.

Receipt lượt 4 mới thêm khớp **SHA-256 khai báo và 24.917 byte** của verdict lưu trong kho. README có hàng mục lục và caveat đính chính. Điều này chứng minh tính nhất quán nội bộ bản lưu, không chứng minh byte của output gốc bên ngoài hay identity người đã review.

Bảng §2 ghi “lượt 4 đo 6 cổng, tìm 2 hỏng” là tóm tắt không đúng tập: sáu phép H4 lượt 4 là tái hiện sáu cổng lượt 3 và sạch; hai lỗi tìm trong phạm vi mở rộng. Không dùng tỷ lệ 2/6 ấy để suy xác suất cổng hỏng. Các số cũ `10/57`, `2/57`, `31/57` vẫn là nợ đã được lượt 4 nêu, không nhận lại làm finding mới trong lượt này.

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Lệnh suite chạy tại `/tmp/rv5-audit/head`; logs và probes lưu trong `/tmp/rv5-audit/`. Mỗi mã thoát bên dưới được lấy trực tiếp từ process/tool, không suy từ dòng cuối stdout.

| Lệnh / phép kiểm | Trạng thái | Bằng chứng và giới hạn |
|---|---|---|
| `git diff --check 2fb43fc bbf05ea` | **passed, rc=0** | Không lỗi whitespace của diff 7 tệp |
| `git merge-base --is-ancestor bbf05ea HEAD`; `git diff --quiet bbf05ea HEAD -- <6 tệp chính>` | **passed, rc=0 từng lệnh** | Commit có trong HEAD; nguồn chính giống byte; `git-checks.json` giữ args đầy đủ |
| `python -B ops/cong_cu_test.py` | **passed, rc=0** | **23/23, skipped=0; 5 tự kiểm; 18 mutant, lỗi=0**; `congcu.log`. Không phủ crash mới R5-01 |
| `python -B .claude/dev/packet_loop_test.py` | **passed, rc=0** | **278/278, BỎ QUA=0; 81 mutant; TỔNG: ĐẠT**; `packet.log`. Không kiểm tay nội dung mọi assertion trong 81 mutant |
| `python -B /tmp/rv5-audit/mutant-targets.py` | **passed, rc=0** | **18 control qua / 18 đích chết đúng thuộc tính**, đã đọc chi tiết; không thấy âm tính giả trong mẫu |
| `python -B /tmp/rv5-audit/probes.py` | **completed, rc=0; phát hiện failed property** | Phân rã lease bốn snapshot; t13 đúng; t22 crash vẫn nhận tín dụng. `probes.json` |
| Chạy lại replacement t13 cũ lấy từ AST bản trước | **completed, rc=0** | Đích `tin_dung_gia: JSONDecodeError`; `old-t13.json` |
| `python -B /tmp/rv5-audit/packet-probes.py` | **passed, rc=0** | **11 control**, ba cấu hình mutation; args/rc/stderr lưu ở `packet-probes.json` |
| `python -B /tmp/rv5-audit/shell-probes.py` | **completed, rc=0; phát hiện failed properties** | Mã từng shell call trong R5-02; `shell-probes.json` |
| `python -B scripts/tl.py doc-claims-check --strict` | **passed, rc=0** | JSON **`ok: true`**; `doc-claims.log`. Không chứng minh các con số nghiệp vụ của tài liệu đúng |
| Windows thật, full legacy selftest/release gate, CI/billing/branch protection GitHub, LIVE | **not_run** | Ngoài phép đo cục bộ của lượt này; không tuyên bố post-merge gate/land hoàn tất |
| Lượt connector khởi động trên `bbf05ea` được prompt kể lại | **KHÔNG ĐO ĐƯỢC** | Không có kết luận/receipt của lượt đó để nhận làm evidence; không tính là approve |
| Băm + thẩm quyền của 44 lease; tác động nhân quả provider; lợi ích thứ tự MVP; thử người dùng đọc 5 phút | **KHÔNG ĐO ĐƯỢC** | Chưa có phép đo tương ứng; không suy từ trường có mặt hay suite xanh |

Clone được review giữ nguyên HEAD/tree và sạch tới trước khi viết báo cáo. Không có thay đổi tracked; đầu ra duy nhất được thêm là `VERDICT.md`.

verdict: changes_requested
