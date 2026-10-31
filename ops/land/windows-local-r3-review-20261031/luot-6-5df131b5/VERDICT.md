verdict: approved
reviewed_sha: c13505a2c36a70c47f5c740146fd5ad6794a9882
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Review độc lập hai trục **Spec** và **Standards/Security**, provider `openai_codex`. Không phát hiện finding có bằng chứng trên candidate này. Áp ngưỡng riêng của packet: chỉ approved khi hết toàn bộ P0–P3.

## Phạm vi và neo

- HEAD đầu/cuối: `c13505a2c36a70c47f5c740146fd5ad6794a9882`; tree `60473672685b3ee89383abda5a44fe853041bc6c`.
- Base `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc` tồn tại và là tổ tiên của HEAD; clone không shallow.
- `spec-r3.md`: SHA-256 `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`. Bytes khớp cả ref lease đã cấp và spec tại head PR #1062 `471ad5391c2bcc1d0ee7871907233313db28e9b6`, blob `93f1248aeca8c0d229f0f896434115f246e7b621`.
- `chung-cu-d10.txt`: SHA-256 `2e802ecf92f21c8c73552096344c9d6da3c5445aa82bd6534e838fdc9914d60a`, khớp prompt.
- `diff.patch` khớp byte với `git diff base HEAD`. Diff đúng **2 tệp, 103 dòng thêm, 2 dòng xoá**, nằm trong effective write set của lease r3 g1, class `sensitive`. ADR-0057/0058 không đổi.
- Review đọc protocol §8, §10.2, §20 và toàn bộ ADR-0057/0058/0059. Không có verdict cũ được cấp; không suy kết quả các lượt trước từ commit message.

## Đối chiếu Spec và Standards/Security

Các vị trí dưới đây là dòng trong checkout `cay-kho/`.

| Nghĩa vụ | Vị trí và kết quả |
|---|---|
| Nhịp tim, trường thứ năm, ít nhất 30 phút/lần, hạn ≤2 giờ từ lần ghi | ADR-0059:26–32 có đủ. Giữ nguyên UTC bắt đầu khi ghi lại; nhịp tim không tạo điều kiện hết hiệu lực mới. Việc tính hạn từ lần ghi thực hiện đúng thay đổi đã duyệt ở spec:31–32, không giữ nhầm mốc bắt đầu ban đầu của ADR-0058:30–31 cho mọi lần gia hạn. |
| Không tiếp nhận khoá còn tiến trình sống | ADR-0059:33–39: kiểm tải trước 3(a)/(b), xét `python.exe`, giờ tạo đổi sang UTC, sau UTC bắt đầu, loại MCP; ghi PID/lệnh rồi đợi. Loại trừ 3(c) tường minh; giữ thứ tự ghi sổ rồi thay khoá của ADR-0058:38–39. |
| Lượt bị ngắt | ADR-0059:40–43 có `ngat=co` trong `ghi_chu`, khoảng ngắt nếu đo được, loại thời lượng khỏi rà soát ADR và cấm tự đổi nguồn/ngủ. Không đổi cấu trúc cột sổ đo ở ADR-0057:45–46. |
| Đọc lại, nối lại và gia hạn | ADR-0059:44–52 yêu cầu đọc trước mỗi lần ghi lại, chỉ gia hạn/nhịp tim khi session còn khớp; mất quyền thì quay về luật lấy khoá. Dòng riêng đã quá hạn vẫn gia hạn được sau kiểm tải; tiến trình riêng không bị chặn nhầm bởi mục 2. |
| Nhả khoá | ADR-0059:53–54 định nghĩa 0 byte, đọc lại theo mục 4, nhả khi xong cả lượt đỏ/bỏ. Điều kiện còn là phiên giữ khoá kết hợp mục 4 ngăn xoá dòng phiên khác. |
| D10–D12 và giới hạn cưỡng chế | Toàn bộ ba hàng ADR-0059:20–22 khớp spec:21–23, chỉ khác markup backtick ở D11. ADR-0059:88–93 có mục 0 cổng và nói rõ công cụ ngoài phạm vi. |
| Con trỏ protocol §10.2 | Protocol:1015 chỉ thêm ADR-0059 vào câu vị trí tài liệu, không tạo nghĩa vụ chạy local, khoá hay merge mới. |
| Bảng protocol §20 | Protocol:1539 có đúng một hàng ADR-0059; cột cổng đúng `không cổng — kỷ luật executor`. Dòng 1538 của ADR-0058 chỉ đổi ô mô tả bằng phần `khoá bổ sung bởi ADR-0059`; các ô còn lại và dòng ADR-0057 giữ nguyên. |
| Không chép doctrine vào protocol | Dựng lại protocol từ base bằng đúng ba phép sửa con trỏ/ô mô tả/hàng mới cho kết quả bằng toàn bộ tệp HEAD. Các quy tắc chi tiết vẫn nằm ở ADR. `doctrine-scan` riêng nó chỉ chứng minh phạm vi scanner, không thay đối chiếu này. |
| Bảo toàn ranh giới | ADR-0059:80–86 giữ phạm vi máy, sổ đo theo máy, cấm dừng tiến trình khác và cấm sửa hồi tố. Không thay CI/branch protection/điều kiện local cộng thêm của ADR-0057:33–35, 51–57; không thêm đường truy cập máy ngoài ADR-0058:22–28. |

Đã quét các nhóm lỗi về nghĩa trên toàn ADR mới: ghi khi session đã đổi (mục 1/4/5 và các ví dụ), áp nhầm chốt tiếp nhận vào gia hạn của chính mình (mục 2/4), thay đổi điều kiện hết hiệu lực/format cũ (mục 1/2/4 và phần giữ nguyên), và lời khai vượt quá dữ liệu đo (bảng D10–D12, diễn giải D10, phương án bị loại). Không có biểu hiện còn mở trong các nhóm này. Rủi ro đọc–ghi không nguyên tử được khai ở ADR-0059:52, 84 và đã nằm ngoài spec; không coi nó là lỗi mới cần công cụ nguyên tử trong packet này.

## Tham chiếu và phạm vi chứng cứ

- Các con trỏ § đều tồn tại: §3 Hạn khoá của ADR-0058 là mục quyết định 3 ở dòng 29–40; §3/§4/§5/§10 của ADR-0057 lần lượt ở 36–37/38–39/40–41/48–49. Protocol §3.1:95–97 có đúng cấm tự sửa power policy. Không có tham chiếu sai vị trí trong ADR mới.
- Đã đọc lại [PR #1062](https://github.com/ducthangho/tra-luat/pull/1062) và [comment duyệt 6537481455](https://github.com/ducthangho/tra-luat/pull/1062#issuecomment-6537481455) qua GitHub connector. Comment của `ducthangho` nêu đúng full spec hash, blob, head và cho cấp lease r3 g1 mission gh-1035. [Mission #1035](https://github.com/ducthangho/tra-luat/issues/1035) tồn tại đúng mục tiêu Windows local. Băm cũ trong PR body không được dùng thay băm đã duyệt.
- [Issue #1021](https://github.com/ducthangho/tra-luat/issues/1021) tồn tại đúng packet biên nhận; commit `356a27e1378b2162bbc0be2ec06ff08fdacbdead` có trong clone, đúng wp1021. [PR #1029](https://github.com/ducthangho/tra-luat/pull/1029) đã merge ADR-0058 tại `eaf83fd78ad3a85a6758d0e81be233b5fedcdf6c` ngày 30-10; [PR #1049](https://github.com/ducthangho/tra-luat/pull/1049) đã merge tại đúng base `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`. Đây là đối chiếu tham chiếu, không phải review lại các packet ấy.
- Session giữ khoá `session_015GtxrbUPS7zGdffB8Sfo8Y`, session tiếp nhận `session_015GtxrcrefBJpLr7fGUSPtB`, giờ khoá, PID 26296 và giờ kết thúc khớp `chung-cu-d10.txt`:24–34, 46–48. Nguồn script, đường dẫn kết quả, mốc sửa script 09:00:26Z và mốc ghi `scripts/tl.py` 09:01:22.7691466Z khớp các dòng 13, 56, 72–120.
- Khoảng chồng D10: 14:03:16 − 14:01:44 = **92 giây**, đúng “khoảng 1,5 phút”. D12: 21:17:25 ngày 30-10 → ~01:35 ngày 31-10 = **4 giờ 17 phút 35 giây**, đúng “hơn 4 giờ”.
- ADR-0059:64–65 chỉ nói không tìm thấy Security 4688 trong ngày được truy vấn, phù hợp `chung-cu-d10.txt`:50–51. Nó không nâng output rỗng thành chứng minh máy chưa bật audit; cũng không coi 18113 giây là `CreationDate`.
- D11/D12 được kiểm với đặc tả đóng băng, không được khai là đã đo lại máy. Không truy cập máy chủ kho trong lượt này. D10 chỉ được kiểm từ bản chép nguồn đã cấp và băm; phép suy cận dưới được đánh giá riêng ở ca (iii).
- Không tự xác nhận model/effort phục vụ từng request, identity executor hay snapshot launcher bằng dữ liệu ngoài phạm vi được cấp. Snapshot đầu/cuối §8.2 do điều phối thực hiện bên ngoài sandbox theo prompt; lượt này kiểm HEAD/tree và trạng thái checkout quan sát được. Sandbox thực tế cho phép ghi workspace; việc giữ checkout không đổi là ràng buộc review và bằng chứng quan sát, không được khai thành cơ chế filesystem read-only.

## Ba ca

### (i) A bị ngắt → quá hạn, tiến trình A dừng → B tiếp nhận 3(a) → A kết nối lại

1. Theo ADR-0058:33–35, quá hạn làm khoá A hết hiệu lực theo 3(a). Tiến trình A đã dừng là tiền đề của ca.
2. B chạy kiểm tải theo ADR-0057:38–39 và ADR-0059:33–37. Không thấy tiến trình thuộc điều kiện mục 2, nên không bị chặn tiếp nhận.
3. B ghi dòng sổ đo nêu session/UTC khoá A và lý do (a), sau đó thay khoá bằng dòng B: ADR-0058:38–39 và ADR-0059:39. Đây là lần lấy khoá mới hợp lệ, không phải nhịp tim của A.
4. A kết nối lại phải đọc `KHOA.txt` theo ADR-0059:44–45. Dòng mang session B nên điều kiện “chỉ ghi lại khi … session_id của chính mình” không thoả.
5. ADR-0059:46–48 xác định A không còn giữ khoá. Khi dòng B còn hiệu lực, A phải đợi; ví dụ ADR-0059:58–60 ghi đúng kết quả này.

**Kết quả: dòng B giữ nguyên.** A không thể dùng quyền gia hạn cũ, nhịp tim hay thao tác nhả để xoá/ghi đè B. Nếu ở thời điểm khác dòng B cũng hết hiệu lực, mục 4 chỉ cho A đi qua một lần lấy khoá mới với kiểm tải/mục 2, không cho ghi lại vô điều kiện; đó là nhánh khác đã có trong spec:43–44.

### (ii) Khoá A quá hạn nhưng chưa ai tiếp nhận; A kết nối lại

1. ADR-0058:34 cho biết dòng đã quá hạn. Điều này không tự chứng minh dòng đã thuộc session khác.
2. A đọc lại theo ADR-0059:44–45; session trong dòng vẫn là A.
3. ADR-0059:49–51 quy định trực tiếp: dòng vẫn của chính mình, quá hạn, chưa ai tiếp nhận → chạy kiểm tải rồi được gia hạn.
4. Bước kiểm tải ADR-0057:38–39 ghi nhận tiến trình khác và cấm tự dừng chúng; bản thân bước này không cấm gia hạn. Mục 2 ADR-0059:33 chỉ xét khoá **của phiên khác**.
5. A ghi lại dòng của mình: giữ UTC bắt đầu; hạn mới không quá 2 giờ từ lần ghi; nhịp tim là giờ hiện tại theo ADR-0059:26–30. Ví dụ dòng 61 nhất quán với nhánh này.

**Kết quả: A gia hạn được.** Ngay cả khi tiến trình của A trong thư mục riêng còn chạy, dòng 50–51 nói rõ nó không chặn gia hạn. Không có vòng lặp buộc A đợi chính mình.

### (iii) D10

Các bước quyết định dưới đây dùng chữ trong ADR-0057/0058/0059. Đối chiếu với tệp chứng cứ chỉ kiểm độ đúng của lời khai, không đưa thêm quy tắc vào ADR.

1. Khoá ba trường ghi 09:01:16Z đã quá 2 giờ: ADR-0058:35, ADR-0059:62. Nó đủ điều kiện hết hiệu lực 3(b), nhưng chưa đủ điều kiện được tiếp nhận.
2. Phiên tiếp nhận phải kiểm tải theo ADR-0057:38 và ADR-0059:33–34. Tình huống tại ADR-0059:62–63 cho thấy PID 26296 chạy `tl.py --selftest`, không phải MCP.
3. Còn phải xác định PID được tạo sau 09:01:16Z: ADR-0059:35 và 63. Không lấy “giờ bắt đầu lượt” từ 18113 giây làm giờ tạo; cũng không có số đo `CreationDate` trực tiếp từ sổ đo/4688: dòng 64–65.
4. ADR-0059:67–74 đưa nguồn quyết định: script ghi khoá, ngủ 3 giây, fetch/checkout, lấy toàn bộ `python.exe` thành `TAI_TRUOC`, **sau đó** mới gọi selftest; kết quả có `BAT_DAU=09:01:16.5807497Z`, bốn PID 23252/5772/12720/26716. Mẫu lấy sau mốc checkout 09:01:22.77Z, do đó sau giờ bắt đầu khoá.
5. Mẫu bao phủ đúng loại tiến trình cần xét và không có 26296; sổ đo 13:59:37Z sau đó có PID 26296 chạy selftest. Theo chính lập luận ADR-0059:76–78, tiến trình ấy được tạo sau mẫu, nên sau 09:01:16Z.
6. Điều kiện mục 2 đã đủ: Python, không phải MCP, tạo sau UTC bắt đầu khoá. ADR-0059:35–37 và 77–78 yêu cầu coi khoá còn sống, không tiếp nhận, ghi PID/lệnh vào sổ rồi đợi. Không đi tiếp đến thao tác thay khoá của ADR-0058:39.

**Kết quả: không tiếp nhận.** Lập luận là cận dưới suy từ một mẫu âm có nguồn/phạm vi/thứ tự rõ, không phải giờ tạo đo trực tiếp. `chung-cu-d10.txt`:104–108 thực sự có bộ lọc theo tên, không loại PID, lấy mẫu trước lệnh selftest; dòng 30 có đúng bốn PID đã nêu. ADR dùng đúng phạm vi chứng cứ này.

### Biến thể gần

- **A gia hạn khi chính tiến trình A còn chạy:** mục 4, ADR-0059:49–51 cho phép sau kiểm tải; mục 2 không áp cho khoá của mình. Không phát sinh chặn sai.
- **Dòng bốn trường ADR-0058:** ADR-0059:31–32 bảo lưu cách đọc. Nếu quá hạn và bị phiên khác tiếp nhận thì vẫn đi qua mục 2; thiếu trường nhịp tim không tự tạo điều kiện hết hiệu lực. Khi chủ ghi lại thì dùng dòng năm trường theo mục 1.
- **Dòng ba trường ADR-0057:** ADR-0058:35 vẫn cho điều kiện 3(b); D10 chứng minh mục 2 áp được vào nhánh này. Không hồi tố sửa dòng cũ.
- **Nhả khi dòng đã thuộc B:** ADR-0059:53 dẫn lại mục 4; A đọc thấy B thì theo dòng 45–46 không còn quyền ghi lại/không còn là phiên giữ khoá. A không được ghi 0 byte. Nếu tệp đã rỗng thì A cũng không còn giữ khoá; không được dùng “nhả” làm lần ghi không kiểm tra quyền.
- **3(c), có bằng chứng phiên giữ khoá bỏ:** ADR-0058:36–40 vẫn đòi bằng chứng, kiểm tải, ghi sổ trước khi thay. ADR-0059:38 miễn chốt còn sống của mục 2; không miễn cấm dừng tiến trình khác.
- **Nhịp tim đã hơn 30 phút nhưng hạn chưa qua:** ADR-0059:31 không thêm điều kiện hết hiệu lực; bên khác vẫn phải đợi theo mục 4. Vi phạm nhịp tim không tự cấp quyền tiếp nhận sớm.
- **A bị ngắt rồi lượt đỏ/bỏ:** ghi `ngat=co`, loại thời lượng khỏi rà soát theo mục 3; nếu vẫn giữ dòng thì đọc lại và nhả 0 byte theo mục 5. Nếu mất dòng vào B thì bảo toàn dòng B. Không tự sửa chế độ nguồn.

## Đã chạy

Các gate chạy trong `cay-kho/` với `PYTHONDONTWRITEBYTECODE=1`, tránh sinh bytecode trong checkout. `BASE` dưới đây là `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`; `HEAD` là reviewed SHA đầy đủ ở dòng 2.

| Lệnh | rc | Kết quả thật |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `c13505a2c36a70c47f5c740146fd5ad6794a9882` |
| `sha256sum spec-r3.md chung-cu-d10.txt` | 0 | Hai băm đúng như mục neo ở trên. |
| `git -C cay-kho config core.abbrev 7` | 0 | Không output; đọc lại `git config --local --get core.abbrev` rc=0, output `7`. Trước lệnh cũng đã là 7. |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | `ok: true`, `flags: []`, `files_scanned: 118`, `advisory_count: 381`, `sha_lens: [7, 40]`, `strict: false`. Stderr rỗng. Chạy lại để lưu JSON đầy đủ sau khi output lần đầu quá dài; cùng rc=0. |
| `git diff --numstat BASE HEAD` | 0 | `3  2  docs/PROTOCOL_DA_PHIEN.md`; `100  0  docs/adr/0059-windows-local-nhip-tim-khoa.md`. Tổng 2 tệp, +103/−2. |
| `git diff --name-only BASE HEAD` | 0 | Đúng hai path nêu trên. |
| `git diff --exit-code BASE HEAD -- 'docs/adr/0057-*' 'docs/adr/0058-*'` | 0 | Không output, hai ADR cũ không bị chạm. |
| `git diff --check BASE HEAD` | 0 | Không output. |
| `PYTHONDONTWRITEBYTECODE=1 python3 review_audit.py` (tại sandbox) | 0 | `ALL AUDIT CHECKS PASSED (content/metadata only; scenario reasoning is in VERDICT.md)`. Kiểm độc lập băm, diff byte-exact, write set/trần, ba phép sửa protocol, D10–D12, PID/mốc thời gian và Git objects. Từng lệnh Git con/rc có trong `review-audit.txt`. |
| `rg -n -e 'KHOA[.]txt' -e 'ngat=co' -e 'CreationDate' -e 'do-luong[.]csv' -e 'ADR-0059' .claude/dev/packet_loop.py ops/lease_publish.py .claude/dev/launcher.py .claude/dev/gate_lifecycle.py .github/workflows/ci.yml .github/workflows/ops-publish-lease.yml` | 1 | Không match trong sáu tệp cổng, phù hợp lời khai không có cổng cưỡng chế. Đây là tìm kiếm, rc=1 nghĩa không có kết quả. |
| `git status --porcelain=v1 --untracked-files=all --ignored` | 0 | Output rỗng sau các gate/audit: tracked, untracked và ignored sạch. |
| `git rev-parse HEAD 'HEAD^{tree}'` | 0 | HEAD/tree cuối khớp hai giá trị ở mục neo. |

GitHub read-only: `github_get_pr_info` cho 1062/1029/1049; `github_fetch_issue` cho 1035/1021; `github_fetch_issue_comments` cho 1062 đều trả `isError: false` (không có shell rc). Chỉ lấy comment duyệt đúng ID làm evidence authority; không dùng verdict của người khác làm kết luận review.

Hiện vật ngoài checkout: `review_audit.py`, `review-audit.txt`, `doc-claims-check.json`, `doc-claims-check.stderr.txt`, `github-reference-readback.json`. Một lượt `rg` thăm dò ban đầu có rc=2 vì tên `scripts/tl_doc_claims.py` không tồn tại; đã loại path đoán ấy và quét lại đúng sáu tệp cổng ở bảng trên, không dùng lượt lỗi làm bằng chứng âm. Không chạy trên Windows/máy chủ kho; không khai có bằng chứng Windows của candidate hay quyền merge/land từ verdict này.
