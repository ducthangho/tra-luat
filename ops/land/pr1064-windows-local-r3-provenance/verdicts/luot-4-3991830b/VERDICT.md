verdict: changes_requested
reviewed_sha: ea9c0dc036120a0c0a07d2a61a56a8dc5520c7fa
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

Review hai trục Spec và Standards/Security, packet `WINDOWS-LOCAL-MAY-CHU-KHO` r3 g1, mission `gh-1035`, effective review class `sensitive`; áp ngưỡng 0 P0–P3 của đặc tả. Ba cổng bắt buộc đạt, nhưng lời khai quyết định ca D10 còn vượt phạm vi chứng cứ.

### d10-suy-khong-ton-tai-tu-danh-sach-chua-ro-pham-vi [P2]

**Vị trí:** `cay-kho/docs/adr/0059-windows-local-nhip-tim-khoa.md:64–69`, nhất là dòng 68; đối chiếu mục 2 tại dòng 35–37. Lớp lỗi: nâng việc vắng trong một danh sách thành bằng chứng chắc chắn về thời điểm tạo tiến trình, khi chưa xác định phạm vi và thời điểm của phép lấy danh sách.

**Bằng chứng:** `chung-cu-d10.txt:24–30` thực sự có `BAT_DAU=2026-10-30T09:01:16.5807497Z`, khoá bắt đầu `09:01:16Z`, và dòng `TAI_TRUOC` liệt kê đúng bốn PID ADR đã chép, không có 26296. Tuy nhiên, đây là output `Get-Content -Raw selftest-ketqua.txt`, không phải output của lệnh truy vấn tiến trình có phạm vi đã xác minh. Bản chép không chứa lệnh/bộ lọc tạo `TAI_TRUOC`, nguồn `selftest.ps1`, hoặc timestamp riêng của mẫu tiến trình. Vị trí một trường sau `BAT_DAU` trong tệp kết quả không tự chứng minh lúc thu thập dữ liệu của trường ấy. `chung-cu-d10.txt:50–52` cũng không cung cấp `CreationDate` hay sự kiện tạo tiến trình.

Lệnh `python3 -B review_checks.py d10` (rc=0) xác nhận: `PID_26296_in_TAI_TRUOC=false`, `CreationDate_value_in_evidence=false`, `producer_Get_CimInstance_command_in_evidence=false`, `TAI_TRUOC_observation_timestamp_in_evidence=false`, `selftest_ps1_source_files=[]`. Đây là đo giới hạn của bundle, không phải chứng minh PID có tồn tại trong mẫu bị bỏ sót.

Do đó, bước từ “không có 26296” sang “PID 26296 chưa tồn tại sau 09:01:16Z, nên được tạo sau giờ bắt đầu khoá” chưa được chứng minh. Có thể dùng bằng chứng âm để suy một cận thời gian tạo tiến trình, nhưng phải chứng minh mẫu bao phủ mọi `python.exe` liên quan, không loại chính phiên/PID đó, và được lấy sau mốc khoá. Hiện văn bản gọi dữ liệu này là “nguồn quyết định” và khẳng định đã áp được điều kiện thời gian của mục 2. Thiếu mắt xích ấy có hậu quả trực tiếp đối với tiêu chí D10 của đặc tả §3: kết luận “không tiếp nhận” đang được khẳng định chắc hơn phép đo cho phép.

**Đề xuất sửa:** sửa đoạn lập luận ca D10 ở ADR-0059, nơi đưa ra kết luận thời gian, giữ nguyên quy tắc mục 2 và số đo đóng băng D10–D12. Đường sửa ít tốn nhất là bổ sung nguồn chỉ đọc của script đã sinh `TAI_TRUOC`, chứng minh bộ lọc và thứ tự/thời điểm lấy mẫu, rồi ghi rõ đây là suy luận gián tiếp và các tiền đề của nó. Bằng chứng trực tiếp `CreationDate`/sự kiện tạo tiến trình là đường mạnh hơn nếu còn nguồn lưu trữ. Nếu không có nguồn đủ, phải khai phần giờ tạo PID chưa đo được, giữ D10 chưa nghiệm thu và bàn giao nhu cầu bổ sung chứng cứ; không biến nó thành kết quả đã chứng minh hoặc tự thêm một luật fail-closed ngoài đặc tả.

**Phép kiểm đóng lớp:** người review phải nối được chuỗi nguồn → bộ lọc bao phủ `python.exe`/không loại PID 26296 → mẫu lấy sau `09:01:16Z` → PID 26296 vắng ở mẫu nhưng hiện diện lúc `13:59:37Z` → cận thời gian tạo thoả mục 2. Đối chứng: danh sách chỉ chứa MCP, danh sách loại tiến trình phiên mình, hoặc mẫu lấy trước khoá đều không được dùng để kết luận cận ấy. Đây là phép kiểm chứng cứ thủ công; chưa chạy được trên máy Windows gốc vì không có quyền truy cập máy ấy trong lượt này.

**Rủi ro khi sửa:** suy từ giờ bắt đầu lượt, giờ tạo/ghi tệp log hoặc 18113 s sẽ lặp lại cùng lớp; từ chối mọi tiếp nhận khi thiếu giờ tạo sẽ thêm điều kiện ngoài spec. Đã quét cả bảng D10–D12, ba ca và phương án bị loại: bảng số đo không khẳng định `CreationDate`; biểu hiện cần sửa là chuỗi suy luận tại dòng 64–69, không tách thêm finding cho các câu cùng chuỗi. Tổng: 1 lớp, 1 chuỗi biểu hiện.

## Ba ca

Các §1–§10 của ADR-0057 và §1–§3 của ADR-0058 dưới đây là các mục đánh số trong phần Quyết định. Đường đi chỉ dùng quy tắc của ba ADR. Phần kiểm chứng D10 đối chiếu thêm đúng bản chép được giao.

### (i) A bị ngắt, B tiếp nhận, A kết nối lại

1. A đang chạy thì mất truy cập: ADR-0059 mục 3, dòng 40–43 yêu cầu ghi `ngat=co` và loại thời lượng khỏi rà soát; không tự đổi nguồn/ngủ. Điều này không tự xoá khoá hay tạo một điều kiện hết hiệu lực mới (mục 1, dòng 31–32).
2. Đến lúc quá hạn, khoá A hết hiệu lực theo ADR-0058 §3(a), dòng 33–35. Tiến trình A đã dừng theo đầu vào ca.
3. Trước khi tiếp nhận, B kiểm tải theo ADR-0058 dòng 38 và ADR-0059 mục 2, dòng 33–37. Trong ca được mô tả tại ADR-0059 dòng 58–59, B không thấy tiến trình nào thoả mục 2 nên không bị chặn.
4. B ghi sổ nêu khoá cũ/lý do (a), rồi thay khoá bằng dòng của B: ADR-0058 dòng 38–40, được ADR-0059 dòng 39 giữ nguyên thứ tự. Dòng mới có trường nhịp tim theo ADR-0059 dòng 26–30.
5. A kết nối lại phải đọc trước khi ghi: ADR-0059 mục 4, dòng 44–48. Thấy `session_id` của B thì A không còn giữ khoá. Khoá B còn hiệu lực trong ca được mô tả ở dòng 60, nên A đợi; không được ghi nhịp tim/gia hạn đè lên dòng B.

**Kết quả: dòng B giữ nguyên.** Không tìm thấy đường cho A lấy quyền từ dòng A đã lưu trong trí nhớ. Nếu về sau khoá B cũng hết hiệu lực, đó là một lần xin tiếp nhận mới theo mục 2 và ADR-0058 §3, không phải hồi sinh quyền của A.

### (ii) Khoá A quá hạn, chưa ai tiếp nhận, A kết nối lại

1. Khoá quá hạn theo ADR-0058 §3(a), dòng 34. Việc quá hạn không làm tệp tự rỗng.
2. A đọc `KHOA.txt`, thấy dòng vẫn mang `session_id` A: ADR-0059 dòng 44–45.
3. ADR-0059 dòng 49–51 cho đúng trường hợp này: A chạy bước kiểm tải rồi được gia hạn. Mục 2 chỉ chặn việc tiếp nhận khoá **của phiên khác**, nên tiến trình của chính A không tạo vòng chặn gia hạn.
4. Khi ghi lại, A giữ `UTC bắt đầu`, đặt nhịp tim bằng giờ hiện tại, đặt hạn không quá 2 giờ từ lần ghi: ADR-0059 dòng 26–30; ADR-0058 dòng 32 cung cấp hành vi gia hạn.

**Kết quả: A gia hạn được**, kể cả khi tiến trình của A vẫn chạy trong thư mục riêng theo ADR-0057 §5. Không cần tuyên bố bỏ khoá hoặc đổi `session_id` để làm việc này.

### (iii) D10

1. Khoá dạng cũ bắt đầu `2026-10-30T09:01:16Z`; lúc `13:58:02Z` đã quá 2 giờ, nên hết hiệu lực theo ADR-0058 §3(b), dòng 35; đúng bảng D10 tại ADR-0059 dòng 20.
2. Đây là khoá của phiên khác, chưa có bằng chứng tuyên bố bỏ theo (c), nên ADR-0059 mục 2, dòng 33–38 áp dụng. Phải kiểm tải trước khi tiếp nhận; chỉ được đi tiếp nếu không vướng điều kiện tiến trình còn sống.
3. Bảng D10 và đoạn ca tại ADR-0059 dòng 62–64 nêu PID 26296 chạy `tl.py --selftest`, không phải MCP. Điều kiện còn lại ở dòng 35 là thời gian tạo PID phải sau giờ bắt đầu khoá. Các số `1758/1758`, `18113 s` và giờ kết thúc không tự trả lời điều kiện này; chính dòng 64 cũng phân biệt giờ bắt đầu lượt với giờ tạo tiến trình.
4. ADR-0059 dòng 65–68 dùng `BAT_DAU` và việc PID vắng trong `TAI_TRUOC` để khẳng định thời gian tạo thoả điều kiện. **Nếu nhận khẳng định ấy như một tiền đề**, mục 2 bắt buộc: không tiếp nhận, ghi sổ nêu PID/lệnh rồi đợi, đúng câu kết tại dòng 69.
5. Đối chiếu bản chép gốc: dữ liệu hiện có chỉ xác nhận những trường đã ghi; chưa xác minh phạm vi/thời điểm mẫu như finding ở trên. Vì vậy bước 4 là một suy luận chưa đủ chứng cứ, không phải một phép đối chiếu `CreationDate` đã được thực hiện. Không dùng hiểu biết bên ngoài hoặc tự thêm quy tắc “không có CreationDate thì luôn đợi” để lấp khoảng trống.

**Kết quả đọc nguyên lời ADR: “không tiếp nhận”. Kết quả kiểm chứng tiền đề D10: chưa đủ căn cứ để nghiệm thu ca này.** Đây là finding P2 về lời khai chứng cứ, không phải phát hiện rằng quy tắc mục 2 cho phép tiếp nhận một PID đã xác minh thoả điều kiện.

### Biến thể gần

| Biến thể | Đường đi theo văn bản và kết quả |
|---|---|
| Tiến trình chính A còn chạy khi A gia hạn dòng A quá hạn | ADR-0059 dòng 49–51 cho gia hạn sau kiểm tải; mục 2 chỉ xét khoá phiên khác. Không bị chặn bởi chính mình. |
| Dòng bốn trường của ADR-0058, chưa có nhịp tim | ADR-0059 dòng 31–32 giữ cách đọc cũ: quá hạn theo §3(a), không biến thành dòng ba trường §3(b), không hết hiệu lực chỉ vì thiếu trường thứ năm. Khi người giữ ghi lại, mục 1 yêu cầu dạng có nhịp tim. |
| Dòng ba trường cũ còn PID thoả điều kiện thời gian, không phải MCP | Hết hiệu lực theo ADR-0058 §3(b), nhưng ADR-0059 mục 2 vẫn chặn tiếp nhận; đồng hồ không vượt qua chốt tiến trình. |
| Chủ khoá đã tuyên bố bỏ có bằng chứng theo §3(c) | ADR-0059 dòng 38 loại (c) khỏi chốt tiến trình. ADR-0058 dòng 36–40 vẫn buộc có bằng chứng, kiểm tải, ghi sổ rồi thay khoá; không được tự dừng tiến trình. |
| A chuẩn bị nhả, đọc thấy dòng B còn hiệu lực | ADR-0059 mục 5 dẫn sang mục 4; dòng 46 xác nhận A không còn giữ khoá, dòng 47 buộc đợi. Nghĩa vụ nhả tại dòng 53–54 áp cho phiên giữ khoá: A không được làm rỗng dòng B. |
| A chuẩn bị nhả, đọc thấy dòng B đã hết hiệu lực | A vẫn không còn giữ khoá (dòng 46). Muốn lấy lại phải đi toàn bộ đường lấy khoá tại dòng 47–48 và mục 2; không được dùng thao tác nhả để bỏ qua tiếp nhận hợp lệ. Chỉ sau khi lấy hợp lệ mới có quyền nhả với tư cách người giữ. |
| A nhả khi dòng vẫn là A, kể cả lượt đỏ hoặc bỏ | Đọc lại theo mục 4, rồi ghi đúng tệp rỗng 0 byte theo mục 5. Không xoá tên tệp, không ghi dấu cách/newline thay cho rỗng. |
| Hai phiên cùng đọc trước khi một phiên ghi | ADR-0059 dòng 52, 75 và ADR-0058 dòng 48–49 khai rõ khe đua còn tồn tại. Không coi đọc lại hoặc nhịp tim là compare-and-swap. Đây là giới hạn được spec cho phép, không phải finding mới. |

## Đối chiếu đặc tả và các lời khai khác

| Tiêu chí | Đối chiếu độc lập |
|---|---|
| Nhịp tim trường 5, ít nhất mỗi 30 phút; hạn ≤2 giờ từ lần ghi | ADR-0059 dòng 26–32 đầy đủ; giữ UTC bắt đầu làm mốc so tiến trình. Không thêm điều kiện hết hiệu lực ngoài (a)–(c). |
| Không tiếp nhận khoá còn tiến trình | Dòng 33–39 khớp điều kiện `python.exe`, thời gian sau UTC bắt đầu, không phải MCP, chỉ (a)/(b), không áp (c); vẫn giữ thứ tự ghi sổ trước thay khoá. Vấn đề chứng minh riêng ca D10 ở finding. |
| Lượt bị ngắt | Dòng 40–43 có `ngat=co`, khoảng mất truy cập nếu đo được, loại thời lượng khỏi rà soát, không tự đổi nguồn/ngủ; §10 của ADR-0057 có ở dòng 48–49. Protocol §3.1 thực sự cấm tự sửa power policy ở dòng 95–97. |
| Đọc lại, gia hạn, nhả | Dòng 44–54 đủ các nhánh tự giữ / đã bị tiếp nhận / rỗng / quá hạn; nhả 0 byte ngay cả khi đỏ hoặc bỏ. Các ca và biến thể đã đi ở trên. |
| Số đo D10–D12 | `review_checks.py structure` so riêng ô số đo với §1 spec, cho cả ba `*_measurement_equal=true`. Phiên, thời điểm, PID, `1758/1758`, `18113 s`, `356a27e` giữ nguyên. Chồng lấn `14:01:44Z`→`14:03:16Z` = 92 s, phù hợp “khoảng 1,5 phút”; `21:17:25Z`→`01:35Z` hôm sau >4 giờ. Không tự nâng số đo mất truy cập thành phép đo giờ tạo PID. |
| Phạm vi theo máy, cột sổ, CI và quyền tiến trình | ADR-0059 dòng 73–77 giữ ADR-0058 §1–§2, ADR-0057 §2 và §4–§10. Không mở thêm máy ngoài `list_devices`, không thay CI, không cấp quyền dừng tiến trình khác. Không tìm thấy luật mới mạnh hơn spec tại các mục quyết định này. |
| Protocol §10.2 | Dòng 1015 chỉ nêu nơi chứa quy ước ở ba ADR, không tạo nghĩa vụ mới. |
| Protocol §20 | Đúng một hàng ADR-0059 ở dòng 1539, cột cổng đúng `không cổng — kỷ luật executor`. Hàng ADR-0058 dòng 1538 chỉ thêm phần yêu cầu vào ô mô tả. Script phục hồi ba sửa đổi được phép cho ra protocol bằng bản base từng byte: không có thay đổi khác hoặc doctrine chép thêm. |
| “Không cổng nào cưỡng chế” | ADR-0059 dòng 79–84 khai đúng giới hạn. Tìm `KHOA.txt`, `CreationDate`, `ngat=co` trên sáu tệp cổng protocol §20 chỉ định: không hit (rg rc=1). Tìm thêm mã `.py/.ps1/.sh/.yml/.yaml`, loại hồ sơ `ops/land`, `ops/reviews`, `ops/leases`, `ops/specs`: không hit (git grep rc=1). Đọc `packet_loop.py:1916–2007` cho thấy `adr-song` kiểm bảng/trạng thái/cấu trúc metadata, không cưỡng chế luật khoá. “Không đọc nội dung” được hiểu là không diễn giải doctrine; scanner có đọc bytes để tìm metadata. |

Nguồn đặc tả authoritative trong bản clone: ref `origin/ops/windows-local-may-chu-kho-r3-lease` tại commit `f21107edbd87756d4835f9ba3b785253c4734653`, path `ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md`, blob `93f1248aeca8c0d229f0f896434115f246e7b621`. Bytes bằng `spec-r3.md` và có SHA-256 yêu cầu. Commit `471ad5391c2bcc1d0ee7871907233313db28e9b6` cũng chứa đúng blob đó, phù hợp nguồn PR #1062 được lease khai. Lease local khớp r3 g1, mission #1035, hai path write set và authority comment `6537481455`; `reviewed_sha_required` còn ghi base nhưng ngay dòng ghi chú của lease nói review từng lượt neo đúng SHA lượt đó, nên không đọc base ấy thành head phải review.

Tham chiếu ADR-0058 §3 *Hạn khoá*, ADR-0057 §3 *Khoá*, §4 *Kiểm tải*, §5 *Cô lập*, §10 *Xem xét lại* đều tồn tại và đúng nội dung. Ba OID D10/D12 `757bde5`, `e9f7872`, `356a27e` resolve thành commit trong clone. Bản chép D10 xác nhận đúng hai session `session_015GtxrbUPS7zGdffB8Sfo8Y` và `session_015GtxrcrefBJpLr7fGUSPtB`; session D11/D12 `session_015GtxrZ1Tt93F4NLUUhKYQy` được chép khớp spec. Chứng cứ được giao chỉ phủ D10; không tự nhận đã đo lại D11/D12 trên máy gốc.

Giới hạn: không có raw readback GitHub của PR #1062 / issuecomment-6537481455 hoặc Mission #1035 trong bundle để xác minh độc lập actor/body của các object đó. Đã đối chiếu với nguồn spec/lease và Git objects được giao; không gọi sự khớp nội bộ ấy là phép GET xác minh authority trên GitHub. Không dùng việc chưa đo remote này làm một cáo buộc sai lời khai. Không có verdict cũ được giao nên không khai đã đóng finding của những lượt trước.

## Đã chạy

Môi trường: Linux, bash, `Python 3.13.18`. Reviewer `openai_codex`, họ model `openai`, phiên độc lập theo assignment; transport công cụ trực tiếp `machine`, không qua người chép. Không có runtime receipt trong read scope để tự xác nhận exact model variant/effort hoặc launcher metadata; phần đó do phiên điều phối đối chiếu, không suy từ tên actor. Không tự cấp assurance/merge authority.

Các lệnh ba cổng chạy với cwd là `cay-kho/`, `PYTHONDONTWRITEBYTECODE=1`, `TL_CACHE_DIR=../review-evidence/cache`, `TMPDIR=../review-evidence/tmp`. Lần lưu JSON doc-claims dùng cùng các thư mục đó dưới dạng đường dẫn tuyệt đối. Chỉ ghi scratch trong sandbox; ngoại lệ repo duy nhất được prompt yêu cầu là `git config core.abbrev 7`.

| Lệnh | rc | Kết quả thực tế |
|---|---:|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `ea9c0dc036120a0c0a07d2a61a56a8dc5520c7fa` |
| `git -C cay-kho rev-parse HEAD^{tree}` | 0 | `3ba7ef7995fe7b9822a43cbe33d78e78d222edca` |
| `git -C cay-kho rev-parse --is-shallow-repository` | 0 | `false` |
| `git -C cay-kho merge-base adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` | 0 | `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc` |
| `sha256sum spec-r3.md chung-cu-d10.txt` | 0 | `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973  spec-r3.md`; `2b935861b8a29f9d43835f4ce6a333948c02524ed112daea4129f5cbc790a624  chung-cu-d10.txt` |
| `git -C cay-kho config core.abbrev 7` | 0 | Không stdout; `git -C cay-kho config --get core.abbrev` rc=0, output `7`. |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | 0 | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | 0 | `"ok": true`, `"files_scanned": 118`, `"flags": []`, `"advisory_count": 381`, `"layers_skipped": {}`, `"strict": false`; không có advisory của ADR-0059. |
| `git -C cay-kho diff --numstat adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` | 0 | `3  2  docs/PROTOCOL_DA_PHIEN.md`; `91  0  docs/adr/0059-windows-local-nhip-tim-khoa.md` — đúng 2 tệp, +94/−2, dưới trần +140. |
| `git -C cay-kho diff --check adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` | 0 | Không output. |
| `python3 -B review_checks.py structure` | 0 | `D10_measurement_equal=true`, `D11_measurement_equal=true`, `D12_measurement_equal=true`; `diff_exact: true`, `files: 2`, `added: 94`, `deleted: 2`, `write_set_exact: true`, `protocol_only_authorized_edits: true`, `adr_0057_0058_untouched: true`. |
| `python3 -B review_checks.py d10 > review-evidence/d10-audit.json` | 0 | PID 26296 vắng trong trường `TAI_TRUOC`; không có giá trị `CreationDate`, lệnh producer, timestamp riêng của mẫu hoặc source `selftest.ps1`; khoảng chồng theo giây nguyên `92.0`. |
| `git -C cay-kho cat-file -t 471ad53` và `git -C cay-kho rev-parse 471ad53:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md` | 0, 0 | `commit`; `93f1248aeca8c0d229f0f896434115f246e7b621`. |
| `git -C cay-kho rev-parse 356a27e^{commit}` | 0 | `356a27e1378b2162bbc0be2ec06ff08fdacbdead` |
| `git -C cay-kho rev-parse e9f7872^{commit}` | 0 | `e9f7872b2fd71eacf30413c48aafdca4d76061ae` |
| `git -C cay-kho rev-parse 757bde561d09738858506aecf5de2f050a5f0d5e^{commit}` | 0 | `757bde561d09738858506aecf5de2f050a5f0d5e` |
| `rg -n 'TAI_TRUOC\|selftest-ketqua\|CreationDate\|ngat=co\|KHOA\.txt\|do-luong\.csv'` trên sáu tệp cổng liệt kê dưới đây | 1 | Không hit; rc=1 là kết quả tìm kiếm không khớp, không phải test thất bại. |
| `git -C cay-kho grep -n -I -e KHOA.txt -e CreationDate -e ngat=co -- '*.py' '*.ps1' '*.sh' '*.yml' '*.yaml' ':!ops/land/**' ':!ops/reviews/**' ':!ops/leases/**' ':!ops/specs/**'` | 1 | Không hit trong tập mã đã nêu. |
| `python3 -B review_checks.py snapshot before` | 0 | `files: 8771`, đúng HEAD/tree, `status: ""`. |
| `python3 -B review_checks.py compare` | 0 | `content_delta: []`, `head_equal: true`, `tree_equal: true`, `status_equal: true`, `index_diff_equal: true`, `working_diff_equal: true`. |
| `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored=matching` cuối lượt | 0 | Không output. |

Sáu tệp của lệnh `rg` ở trên: `cay-kho/ops/lease_publish.py`, `cay-kho/.claude/dev/packet_loop.py`, `cay-kho/.claude/dev/launcher.py`, `cay-kho/.claude/dev/gate_lifecycle.py`, `cay-kho/.github/workflows/ci.yml`, `cay-kho/.github/workflows/ops-publish-lease.yml`.

JSON doc-claims được lưu đầy đủ tại `review-evidence/doc-claims-check.json`, SHA-256 `8f3fb01c00ef1ebd850b68c2fed22132c5a5276cb2ae531d1dc7670d865ff5cf`; receipt lệnh/rc ở `review-evidence/doc-claims-check.receipt.json`. Lệnh này chạy hai lần vì stdout lần đầu vượt giới hạn hiển thị; lần hai chỉ để lưu và parse JSON đầy đủ, cả hai rc=0. Các phép đọc có một lần thăm dò tên module `scripts/tl_core/doc_claims.py` không tồn tại (rg rc=2); đã xác định consumer thật là `scripts/tl_core/workflow.py`, không tính lần thăm dò ấy thành gate.

Snapshot riêng ở `review-evidence/before.json` và `after.json` bao phủ bytes/hash/size mọi tệp trong checkout, kể cả ignored/untracked, cùng HEAD/tree/diff/index/status; loại thư mục `.git` khỏi hash nội dung. Snapshot bắt đầu sau cấu hình `core.abbrev=7` được cho phép. Đây là phép so hai mốc của bản clone được giao, không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên; snapshot ngoài sandbox do phiên điều phối thực hiện không được tự khai là đã xác minh ở đây. Không chạy Windows, không chạy heavy selftest/CI, không sửa ADR/protocol hoặc bất kỳ tệp sản phẩm nào.
