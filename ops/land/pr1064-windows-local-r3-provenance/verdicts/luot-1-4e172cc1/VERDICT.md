verdict: changes_requested
reviewed_sha: 144c96ad15071d0d9c2061b34d17f2c13b647e70
Kết quả: 0 P0, 2 P1, 0 P2, 0 P3.

Đã review hai trục **Spec** và **Standards/Security**, áp ngưỡng packet: phải hết P0–P3 mới được approved. Ba cổng và ba ca chính đạt; hai vi phạm đặc tả bên dưới chặn approval.

Provider: `openai_codex`; model: GPT-6 (Codex, theo định danh được cung cấp trong phiên); bề mặt quan sát được: Codex agent qua API với shell cục bộ; transport: `machine/local`; Linux/bash. Không tự khẳng định tên model chi tiết/effort hoặc tên CLI không đo được. Phiên reviewer độc lập; không đọc verdict cũ, không sửa cây làm việc `cay-kho/`. Chỉ đặt `git config core.abbrev 7` theo yêu cầu tường minh của prompt.

Neo: base `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`; reviewed tree `da01907cc8ce6c294ef08075b09a72d84999077f`; spec SHA-256 `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`. `diff.patch` khớp byte với diff base..HEAD; clone không shallow. Lease r3/g1, effective review class `sensitive`, write set và băm spec khớp. Đây là review nội dung; không tự cấp quyền merge/land hoặc xác nhận snapshot ngoài sandbox thay phiên điều phối.

### mo-rong-dieu-kien-khoa-con-song [P1]

- Vị trí: `cay-kho/docs/adr/0059-windows-local-nhip-tim-khoa.md:37`.
- Bằng chứng: câu “Không đọc được giờ khởi động của một tiến trình như thế thì cũng coi là còn sống” thêm một điều kiện chặn tiếp nhận. `spec-r3.md:33–36` chỉ quy định tiến trình `python.exe` không phải MCP **khởi động sau** UTC bắt đầu khoá; không quy định đồng nhất giờ khởi động chưa biết với thoả điều kiện ấy. ADR-0057 mục 4 (`:38–39`) chỉ yêu cầu ghi tiến trình khác vào kết quả đo và không tự dừng; ADR-0058 mục 3 (`:33–40`) cũng không có điều kiện thay thế này.
- Hậu quả: với khoá quá hạn và một `python.exe` không phải MCP nhưng không đọc được giờ khởi động, executor bị buộc coi khoá còn sống và đợi, dù chưa xác lập được quan hệ thời gian mà đặc tả đóng băng yêu cầu. Đây là luật mạnh hơn/rộng hơn spec; hơn nữa “một tiến trình như thế” có thể được đọc là đã biết nó khởi động sau khoá, hoặc chỉ biết nó là python không phải MCP.
- Đề xuất: bỏ câu bổ sung này, giữ đúng điều kiện đã duyệt. Nếu cần chính sách cho giờ khởi động không đo được thì đưa nó vào thay đổi đặc tả được chủ kho duyệt trước; không tự thêm vào ADR của packet hiện tại.
- Lớp: **mở rộng điều kiện chuẩn tắc ngoài spec**. Đã quét toàn bộ năm mục Quyết định, ba ca và các mục giữ nguyên/phương án bị loại; các chi tiết giữ UTC bắt đầu, đọc dòng bốn trường và miễn chặn gia hạn khoá của chính phiên giải thích đúng spec, không phát hiện biểu hiện độc lập khác cùng lớp.

### chep-doctrine-vao-bang-protocol [P1]

- Vị trí: `cay-kho/docs/PROTOCOL_DA_PHIEN.md:1539`, ô mô tả ADR-0059.
- Bằng chứng: `spec-r3.md:51–57` yêu cầu đăng ký một dòng ADR-0059 nhưng cấm “chép doctrine vào protocol”. Ô mới chép cả tần suất “ít nhất 30 phút một lần”, điều kiện không tiếp nhận theo 3(a)/3(b) với python không phải MCP và giờ bắt đầu, luật `ngat=co`/loại thời lượng, đọc lại và cách nhả. Đây là các luật vận hành đã có tại ADR-0059 mục 1–5 (`:26–54`), không chỉ tên/chỉ dẫn tới ADR.
- Hậu quả: các điều kiện và con số có hai chỗ ở; executor có thể dùng bảng như luật vận hành rút gọn. Chẳng hạn ô có tần suất ghi lại và thao tác nhả nhưng không mang đủ điều kiện còn giữ đúng session khi ghi, cách gia hạn của chính phiên hay bước ghi sổ đo. Cổng `doctrine-scan` xanh không bác lỗi này: mã ở `.claude/dev/packet_loop.py:1625–1640` mặc định quét adapter/CLAUDE.md, không kiểm ô mô tả protocol để tìm bản sao từ ADR.
- Đề xuất: rút ô thành mô tả định tuyến ngắn tới ADR-0059 và phạm vi nó bổ sung; bỏ các tần suất, điều kiện và thao tác cụ thể khỏi ô. Giữ `Accepted`, cột `không cổng — kỷ luật executor`, phần bổ sung trong ô ADR-0058 và con trỏ trung tính ở §10.2.
- Lớp: **sao chép luật vào nơi chỉ định tuyến**. Đã quét cả ba chỗ protocol thay đổi: chỉ ô ADR-0059 có biểu hiện này; con trỏ `:1015` trung tính và ô ADR-0058 `:1538` chỉ thêm đúng nội dung spec yêu cầu. Không đề nghị sửa các dòng cũ ngoài phạm vi packet.

## Ba ca

Các bước dưới đây chỉ suy từ ADR-0057/0058/0059; số dòng tính trên cây reviewed SHA. Không dùng cơ chế khoá hay quy tắc tiến trình từ bên ngoài để lấp chỗ trống.

**(i) A bị ngắt → khoá quá hạn, tiến trình A đã dừng → B tiếp nhận theo 3(a) → A kết nối lại.**

1. Dòng khoá A quá UTC hạn nên hết hiệu lực theo ADR-0058 mục 3(a), `:33–34`. Việc A bị ngắt được ghi `ngat=co` theo ADR-0059 mục 3, `:40–43`; nó không trao lại quyền ghi khoá cho A.
2. B chạy bước kiểm tải theo ADR-0059 mục 2, `:33–38`, dẫn tới lệnh kiểm python ở ADR-0057 mục 4, `:38–39`. Với giả thiết tiến trình A đã dừng và không có tiến trình khác thoả điều kiện mục 2, không có điều kiện chặn tiếp nhận.
3. B ghi sổ đo trước, nêu session/UTC của khoá A và lý do (a), rồi thay nội dung khoá bằng dòng của B: ADR-0058 `:38–40` và ADR-0059 `:39`. Dòng mới theo năm trường ở ADR-0059 `:26–30`, với hạn không quá hai giờ kể từ lần ghi.
4. A kết nối lại phải đọc `KHOA.txt` trước: ADR-0059 mục 4, `:44–45`. Dòng mang session B nên A không còn giữ khoá, theo `:46`. Điều kiện “chỉ ghi lại khi dòng hiện có vẫn mang session_id của chính mình” không thoả.
5. Khi khoá B còn hiệu lực, `:47` buộc A đợi. A không được ghi nhịp tim/gia hạn bằng session A lên dòng B. Nếu A đang hoàn tất lượt cũ và muốn nhả, mục 5 `:53–54` vẫn bắt đọc lại **theo mục 4**, nên cũng không được xoá dòng B.

Kết quả: **dòng B giữ nguyên**; đúng ca mẫu tại ADR-0059 `:58–60`. Nếu về sau khoá B cũng hết hiệu lực, đó là lần xin tiếp nhận mới theo `:47–48` và mục 2, không phải quyền gia hạn cũ của A. Khe đọc–ghi không nguyên tử được khai tại `:52`, không bị coi là đã khắc phục trong packet này.

**(ii) Khoá A quá hạn, chưa ai tiếp nhận → A kết nối lại.**

1. ADR-0058 `:34` làm khoá hết hiệu lực; nhưng `:32` đã cho phép phiên còn cần máy ghi lại dòng với hạn mới.
2. A đọc lại theo ADR-0059 `:44–45`. Dòng vẫn mang session A nên điều kiện được ghi lại thoả; nhánh mất khoá ở `:46–48` không kích hoạt.
3. Câu chuyên biệt ở `:49–51` quy định đúng tình huống này: chạy bước kiểm tải rồi được gia hạn. Theo ADR-0057 `:38–39`, tiến trình phiên khác được ghi vào kết quả và không được tự dừng. Mục 2 của ADR-0059 chỉ xét tiếp nhận khoá **của phiên khác** (`:33`, `:51`), nên không tạo chặn gia hạn của A.
4. A ghi lại đủ năm trường; UTC bắt đầu giữ nguyên, nhịp tim là giờ hiện tại, hạn không quá hai giờ từ lần ghi: ADR-0059 `:26–30`. Sau đó tiếp tục nhịp tim ít nhất 30 phút một lần (`:28`).

Kết quả: **A gia hạn được**; đúng ca tại `:61`. Biến thể tiến trình test của chính A trong thư mục riêng còn chạy cũng gia hạn được, nhờ ngoại lệ tường minh `:50–51` và quy tắc cô lập ADR-0057 mục 5, `:40–41`.

**(iii) D10.**

1. Dòng cũ không có hạn, UTC bắt đầu 09:01:16Z; tới thời điểm tiếp nhận 13:58:02Z đã quá hai giờ. ADR-0058 `:35` phân loại hết hiệu lực theo 3(b), khớp bảng D10 của ADR-0059 `:20`.
2. Trước khi thay dòng, B phải kiểm tải: ADR-0059 `:33–34`. Số đo tại `:20` có PID 26296 chạy `tl.py --selftest` lúc 13:59:37Z; ca D10 `:62–64` xác định đây không phải MCP.
3. Ca D10 nối với thời lượng 18113 s của cùng session trong D11 (`:21`): 14:03:16Z trừ 18113 s = **09:01:23Z**, sau UTC bắt đầu khoá **7 s**. Script `review_checks.py` đã tính lại, không lấy nhịp tim hay giờ gia hạn thay UTC bắt đầu.
4. PID là python không phải MCP, khởi động sau UTC bắt đầu khoá; ADR-0059 `:35–37` vì vậy coi khoá còn sống. B phải ghi sổ đo nêu PID/lệnh và đợi, không chuyển sang bước thay dòng của ADR-0058 `:39`.

Kết quả: **không tiếp nhận**. Không cần dùng câu bổ sung về giờ khởi động không đọc được đang bị finding P1. Khoảng 14:01:44Z đến 14:03:16Z là **92 s**, khớp lời khai chồng nhau khoảng 1,5 phút.

Các biến thể gần đã đối chiếu:

| Biến thể | Câu áp dụng và kết quả |
|---|---|
| Dòng bốn trường của ADR-0058, còn hạn | ADR-0059 `:31–32` giữ cách đọc cũ; không biến thiếu nhịp tim thành hết hiệu lực. Phiên khác đợi theo `:47`. |
| Dòng bốn trường của phiên khác đã quá hạn | ADR-0058 3(a), không phải 3(b); ADR-0059 mục 2 kiểm tải/PID trước tiếp nhận, rồi giữ thứ tự ghi sổ–thay dòng. |
| Dòng vẫn của A, A còn tiến trình trong thư mục riêng | ADR-0059 `:49–51`: kiểm tải rồi gia hạn được, không tự chặn bởi chính tiến trình A. |
| A định nhả khi dòng đã là B | ADR-0059 `:53` dẫn về toàn bộ mục 4, đặc biệt `:45–47`; A không còn giữ khoá nên không ghi rỗng dòng B. |
| A đọc thấy tệp rỗng | ADR-0059 `:46–48`: mất quyền gia hạn cũ; phải kiểm tải rồi lấy khoá mới. Không được nhảy qua bước này bằng nhịp tim. |
| 3(c), có tuyên bố bỏ khoá đúng chủ phiên | ADR-0058 `:36–39` đòi bằng chứng tuyên bố và kiểm tải/ghi sổ; ADR-0059 `:38` miễn riêng điều kiện chặn mục 2, không miễn các bước cũ. |
| Python là MCP, hoặc đã biết khởi động trước/đúng UTC bắt đầu khoá | Không thoả phép kiểm “không phải MCP”/“sau” ở ADR-0059 `:35–36`; riêng điều kiện này không chặn. Kiểm tải, ghi sổ và cấm dừng tiến trình phiên khác vẫn còn. |
| Python không phải MCP, không đọc được giờ khởi động | Câu mới `:37` bắt coi là còn sống dù chưa biết quan hệ giờ; đây là phản ví dụ của finding `mo-rong-dieu-kien-khoa-con-song`. |

## Đối chiếu nội dung và lời khai

- **Nhịp tim/hạn:** ADR-0059 `:26–32` có đủ trường thứ năm, giờ nhịp tim hiện tại, tần suất 30 phút và hạn ≤2 giờ từ lần ghi. Giữ UTC bắt đầu là chi tiết cần cho phép so tiến trình sau nhiều lần gia hạn. Không thêm điều kiện hết hiệu lực do nhịp tim, không xoá khả năng đọc dòng bốn trường.
- **Ngắt/nhả:** `:40–43` giữ nguyên tên cột `ghi_chu`, thêm `ngat=co`, ghi khoảng ngắt nếu đo được, loại thời lượng khỏi rà ADR và giao việc chống ngủ cho chủ kho. `:53–54` định nghĩa nhả bằng tệp 0 byte, cả khi đỏ/bỏ, kèm đọc lại. Không có luật đổi nguồn hoặc tự dừng tiến trình khác.
- **Tham chiếu theo mục:** ADR-0057 mục 3/4/5/10 thực sự là khoá/kiểm tải/cô lập/xem xét lại (`:36–49`); ADR-0058 mục 3 thực sự là Hạn khoá (`:29–40`). Protocol §3.1 thực sự chứa “không tự sửa power policy” (`:96–98`). Các con trỏ này khớp, không phải mục số được bịa.
- **Protocol:** kiểm bằng script thấy chính xác một dòng ADR-0059, đúng cột cổng; ADR-0058 chỉ đổi ô mô tả bằng hậu tố đã duyệt; §10.2 tại `:1015` vẫn là câu “Quy ước … nằm tại …” trung tính. Toàn bộ protocol chỉ khác base ở đúng ba vị trí đó. Lỗi còn lại là mức độ chép luật trong ô ADR-0059, đã ghi riêng ở trên.
- **D10–D12:** cả ba ô số đo tại ADR-0059 `:20–22` khớp byte với §1 đặc tả, bao gồm session, PID, mốc giờ, N/N, thời lượng và head. D12 tại ~01:35Z ngày 31-10 quá hạn 21:17:25Z ngày 30-10 khoảng **4:17:35**, đúng “hơn 4 giờ”. Phép suy giờ khởi động D10 đúng số học và được ADR gọi rõ là “suy”, không phải `CreationDate` đã đo trực tiếp.
- **Authority:** đã đọc trực tiếp [comment duyệt đặc tả](https://github.com/ducthangho/tra-luat/pull/1062#issuecomment-6537481455): `ducthangho`, `OWNER`, `2026-10-31T01:57:22Z`, đầy đủ hash `f1a666…a973`, blob `93f1248aeca8c0d229f0f896434115f246e7b621`, cho lease r3/g1/gh-1035. [PR #1062](https://github.com/ducthangho/tra-luat/pull/1062) có đúng head `471ad5391c2bcc1d0ee7871907233313db28e9b6`, chưa merge lúc đọc. Tệp ở frozen ref khớp byte/băm/blob; đường tìm đặc tả sau/before merge của ADR-0059 `:6–7` tồn tại.
- **Issue/lịch sử:** [Mission #1035](https://github.com/ducthangho/tra-luat/issues/1035) tồn tại và đúng ô chứa vận hành; [#1021](https://github.com/ducthangho/tra-luat/issues/1021) là **Issue**, có cùng session `session_015GtxrZ1Tt93F4NLUUhKYQy`, và object `356a27e1378b2162bbc0be2ec06ff08fdacbdead` tồn tại với subject `wp1021`. [PR #1029](https://github.com/ducthangho/tra-luat/pull/1029) merge lúc `2026-10-30T04:41:44Z`, khớp ngày ADR-0058 có hiệu lực; [PR #1049](https://github.com/ducthangho/tra-luat/pull/1049) merge tại exact base. Hồ sơ `ops/land/pr1029-windows-local-r2-land-evidence.yaml:206–207` có kết luận bổ sung `landed: true`; không đọc trạng thái lịch sử `false` trước đó thành kết luận cuối.
- **Giới hạn nguồn số đo:** không có bản sổ `do-luong.csv`, `KHOA.txt` hay log tiến trình Windows gốc trong bundle, không chạy Desktop Commander/Windows. Đã xác minh chép đúng đặc tả đóng băng, đối chiếu các session trong ô số đo và tính lại thời gian; chưa độc lập tái đo sự kiện trên máy thật hay xác minh đầy đủ phiên runtime từ hệ thống Claude. Thiếu nguồn thô không được ghi thành phép đo đã chạy hoặc tự tạo finding lên dữ liệu đã được spec cho sẵn.
- **Quét lớp:** ngoài hai lớp finding đã nêu, đã rà hết ADR-0059 và mọi hunk protocol về điều kiện mạnh hơn spec, mâu thuẫn quyền ghi/nhả, lệch định dạng khoá/cột đo, tham chiếu mục/định danh và lời khai cổng. Không thấy biểu hiện độc lập khác có bằng chứng. Ba cổng xanh là bằng chứng cơ học, không phủ định hai lỗi văn bản.

## Đã chạy

Lệnh dưới chạy từ thư mục sandbox, trừ khi ghi `cwd=cay-kho`. Các lệnh Python của cổng đều đặt `PYTHONDONTWRITEBYTECODE=1` để tránh cache trong cây review. `review_checks.py`, `doc-claims-check.json`, `github-readbacks.json` nằm ngoài `cay-kho/`.

| Lệnh/phép kiểm | rc | Dòng kết quả thật / bằng chứng |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `144c96ad15071d0d9c2061b34d17f2c13b647e70` |
| `sha256sum spec-r3.md` | 0 | `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973  spec-r3.md` |
| `git config core.abbrev 7` (`cwd=cay-kho`), rồi `git config --get core.abbrev` | 0 / 0 | `7` |
| `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py adr-song --root .` (`cwd=cay-kho`) | 0 | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `PYTHONDONTWRITEBYTECODE=1 python3 .claude/dev/packet_loop.py doctrine-scan --root .` (`cwd=cay-kho`) | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json > ../doc-claims-check.json` (`cwd=cay-kho`) | 0 | JSON: `"ok": true`, `"files_scanned": 118`, `"flags": []`, `"advisory_count": 381`. `claims_flagged=381` đều là advisory, không phải 381 cờ lỗi cứng. |
| `git diff --numstat adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` (`cwd=cay-kho`) | 0 | `3  2  docs/PROTOCOL_DA_PHIEN.md`; `86  0  docs/adr/0059-windows-local-nhip-tim-khoa.md`. **2 tệp, +89/−2**, trong trần 2 tệp/+140. |
| `git diff --check adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` (`cwd=cay-kho`) | 0 | Không có lỗi khoảng trắng. |
| `git rev-parse --is-shallow-repository` (`cwd=cay-kho`) | 0 | `false` |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_checks.py` | 0 | `PATCH_MATCH=true`; `FILES=2; ADDED=89; DELETED=2; WRITE_SET_MATCH=true; ADR_0057_0058_UNCHANGED=true`; `D10_MEASUREMENT_MATCH=true`; `D11_MEASUREMENT_MATCH=true`; `D12_MEASUREMENT_MATCH=true`; `PROTOCOL_ONLY_3_REQUESTED_LOCATIONS=true; ADR0058_ONLY_DESCRIPTION_CELL=true; ADR0059_ROWS=1; GATE_CELL_MATCH=true; POINTER_MATCH=true`; `STRUCTURAL_CHECKS=PASS (does not validate natural-language rules)`. |
| Phép tính trong `review_checks.py` | 0 | `D10_INFERRED_START=2026-10-30T09:01:23+00:00; AFTER_LOCK_BY_S=7`; `D10_OVERLAP_S=92`; `D12_OVERDUE_AT_01_35=4:17:35`. |
| `rg -n -e 'KHOA\.txt' -e CreationDate -e ngat=co -e 0059` trên sáu tệp cổng (`cwd=cay-kho`) | 1 (không khớp) | Không có output. Phép quét tương đương trong script: `GATE_CONCEPT_SCAN: rg rc=1; 0 matches across 6 gate files`. Sáu tệp: `ops/lease_publish.py`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`, `.claude/dev/gate_lifecycle.py`, `.github/workflows/ci.yml`, `.github/workflows/ops-publish-lease.yml`. Đây hỗ trợ lời khai 0 cổng trong phạm vi các cổng định tuyến, không chứng minh mọi công cụ ngoài kho. |
| `git show -s --format='%H %s' 356a27e` (`cwd=cay-kho`) | 0 | `356a27e1378b2162bbc0be2ec06ff08fdacbdead wp1021: docstring khop dung hanh vi va ca test hien hanh (tu ra soat truoc luot 8)` |
| `git status --porcelain=v1 --untracked-files=all`, `git diff --exit-code`, `git diff --cached --exit-code` cuối lượt (`cwd=cay-kho`) | 0 / 0 / 0 | Đều không có output thay đổi. |
| `git rev-parse HEAD HEAD^{tree}` cuối lượt (`cwd=cay-kho`) | 0 | HEAD `144c96ad15071d0d9c2061b34d17f2c13b647e70`; tree `da01907cc8ce6c294ef08075b09a72d84999077f`, không đổi. |

API đọc bằng công cụ GitHub `github_fetch` (không có shell rc): GET `/repos/ducthangho/tra-luat/issues/comments/6537481455`, `/pulls/1062`, `/issues/1035`, `/issues/1021`, `/pulls/1029`, `/pulls/1049` đều trả object, `isError=false`; các trường đối chiếu lưu ở `github-readbacks.json`. GET `/pulls/1021` trả `NOT_FOUND`/404; đã kiểm đúng `/issues/1021` sau đó, nên không báo nhầm Issue không tồn tại. Không đăng comment/review, không đổi dữ liệu GitHub.

Windows local, full selftest và CI: **not_run** trong lượt reviewer này; không phải các cổng ba lệnh của §3/§4 đã giao. Snapshot nội dung tracked/untracked/ignored trước–sau nằm ngoài sandbox theo prompt và do phiên điều phối giữ; reviewer chỉ xác nhận HEAD/tree và worktree/index sạch ở phạm vi đã tự đo, không tự nhận đã kiểm snapshot ngoại vi.
