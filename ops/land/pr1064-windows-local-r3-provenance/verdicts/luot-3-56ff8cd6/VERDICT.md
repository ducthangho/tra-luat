verdict: changes_requested
reviewed_sha: 14795688f2ce2e24c3d4f3f467d862f6772f45fb
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

Review độc lập hai trục **Spec** và **Standards/Security**, áp tiêu chí 0 P0–P3 của đặc tả. Có **1 lớp / 1 biểu hiện còn mở**. Các cổng xanh và đúng write set; chưa đạt ca nghiệm thu D10.

Neo: base `adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc`; tree `96fa900fc9977eafe1768ad52d19a25fa16d2b82`. Đặc tả có SHA-256 `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973`, bằng từng byte với blob trên `origin/ops/windows-local-may-chu-kho-r3-lease`. `diff.patch` bằng từng byte với `git diff base HEAD`. Lease r3/g1 đúng packet/mission, effective review class `sensitive`.

Provider reviewer: `openai_codex`; môi trường chạy lệnh: Linux, bash, Python 3.13.18, transport công cụ trực tiếp. Model/effort từng request, launcher receipt và snapshot §8.2 do điều phối chụp ngoài sandbox không được tự đo trong lượt này; không suy chúng từ danh tính GitHub hay rc của cổng.

### d10-ket-luan-phu-thuoc-gia-dinh [P1]

- **Vị trí:** `cay-kho/docs/adr/0059-windows-local-nhip-tim-khoa.md:62–67`, điều kiện chi phối ở dòng 33–39; đối chiếu `spec-r3.md:21–22,63–67`.
- **Lớp:** ca nghiệm thu kết luận chắc chắn từ một tiền đề chưa được chứng minh. Biểu hiện còn mở là D10. Đặc tả yêu cầu reviewer đi qua **số đo D10** phải ra “không tiếp nhận”. ADR dòng 65–67 tự xác nhận D10 không ghi `CreationDate` và kết luận chỉ đứng trên giả định PID 26296 được tạo sau 09:01:16Z. Mục 2 chỉ chặn khi điều kiện giờ tạo ấy đúng. `ADR-0057` mục 4 chỉ yêu cầu ghi nhận tiến trình và không tự dừng; nó không cung cấp một điều kiện chặn khác khi thiếu giờ tạo.
- **Bằng chứng chạy được:** `PYTHONDONTWRITEBYTECODE=1 python3 review_audit.py` rc=0; kết quả lưu trong `review-audit.json`. `14:03:16Z - 18113 s = 09:01:23Z` là giờ bắt đầu **lượt**, đúng phép tính ở dòng 66, nhưng chưa quyết định giờ tạo PID. Liệt kê hai giá trị giả định để kiểm điều kiện trong văn bản, không coi đây là số đo Windows:

  | Giờ tạo PID giả định | Mâu thuẫn số đo D10/D11 đã cho? | Mục 2 chặn tiếp nhận? |
  |---|---|---|
  | 09:01:10Z, trước giờ khoá 09:01:16Z | Không; văn bản không ràng buộc giờ tạo PID bằng giờ bắt đầu lượt | Không |
  | 09:01:20Z, sau giờ khoá và trước giờ bắt đầu lượt 09:01:23Z | Không | Có |

  Khi không còn tiến trình nào khác thoả mục 2, nhánh đầu vẫn cho tiếp nhận sau kiểm tải và ghi lý do 3(b) theo `ADR-0058:38–40`. Nhánh sau bắt ghi PID/lệnh rồi đợi. Câu “bước kiểm tải lúc ấy trả giá trị này” (`ADR-0059:63–64`) không cung cấp giá trị thực tế để chọn nhánh.
- **Hậu quả / mức độ:** P1 vì chưa đạt tiêu chí bắt buộc ở §3 đặc tả, dù đã khai trung thực giới hạn phép đo. Đây không phải kết luận rằng PID thật được tạo trước khoá, hay phép tính 18113 giây bị sai.
- **Đề xuất sửa cụ thể:** bổ sung chứng cứ gốc neo đúng PID/lượt/máy và cho thấy `CreationDate > 2026-10-30T09:01:16Z`, rồi dẫn chứng ấy trong đoạn D10 để áp mục 2 không cần giả định. Có thể dùng nhật ký gốc nếu nó chứng minh được thứ tự tạo PID và ghi khoá; không sửa hồi tố sổ đo. Nếu chứng cứ đó không tồn tại, phải có thay đổi đặc tả/tiêu chí được chủ kho duyệt trước khi coi D10 đạt. Chỉ đổi câu thành “giả định” hoặc dùng giờ bắt đầu lượt thay giờ tạo PID không đóng finding; tự thêm luật chặn khi không biết giờ tạo cũng cần authority vì vượt luật đóng băng.
- **Quét cùng lớp:** đã đối chiếu toàn bộ ADR-0059, các lần nhắc PID/`CreationDate`, đoạn ba ca, bảng D10–D12 và phương án bị loại. Bảng số đo chép đúng; phép suy 09:01:23Z, chồng 92 giây và quá hạn khoảng 4 giờ 17 phút đều đúng. Dòng 35 là điều kiện quy phạm đúng đặc tả; dòng 79–82 khai giới hạn cưỡng chế. Không tách những câu cùng gốc ở D10 thành nhiều finding. Phép đóng lớp: bằng chứng quyết định tiền đề thời gian của D10 hoặc acceptance mới có thẩm quyền, rồi đi lại cả ba ca và các biến thể bên dưới.

## Ba ca

Các bước sau chỉ áp câu chữ ADR-0057/0058/0059. Chúng là diễn giải văn bản; không phải chạy khoá trên máy Windows.

**(i) A bị ngắt → khoá quá hạn, tiến trình A đã dừng → B tiếp nhận 3(a) → A kết nối lại.**

1. Theo `ADR-0058:33–35`, quá hạn ghi trong dòng là hết hiệu lực theo 3(a).
2. B kiểm tải theo `ADR-0057:38–39` và `ADR-0059:33–37`. Trong ca đã cho không còn tiến trình A và B không thấy tiến trình thoả mục 2, nên điều kiện “không tiếp nhận” không kích hoạt.
3. Theo `ADR-0058:38–40` và `ADR-0059:39`, B ghi sổ đo nêu session/UTC cũ, lý do (a), rồi thay bằng dòng của B. Dòng mới có định dạng năm trường ở `ADR-0059:26–30`.
4. A kết nối lại phải đọc trước khi ghi theo `ADR-0059:44–45`; dòng hiện có mang session B, nên A không được ghi lại như chủ khoá cũ.
5. Theo `ADR-0059:46–48`, A không còn giữ khoá; với khoá B còn hiệu lực, A đợi. **Kết quả: dòng B giữ nguyên**, khớp câu minh hoạ `ADR-0059:58–60` và đặc tả. Không có bước nào cho A khôi phục dòng đã lưu trước khi ngắt.

**(ii) Khoá A quá hạn, chưa ai tiếp nhận, A kết nối lại.**

1. Quá hạn làm khoá hết hiệu lực theo `ADR-0058:33–35`, nhưng không tự đổi session trong tệp.
2. A đọc lại theo `ADR-0059:44–45`, thấy dòng vẫn mang session A.
3. `ADR-0059:49–51` nói rõ trường hợp ấy được gia hạn sau kiểm tải. Mục 2 chỉ xét **khoá của phiên khác**, nên không đưa điều kiện chặn tiếp nhận vào việc A gia hạn chính dòng mình.
4. A kiểm tải theo `ADR-0057:38–39`, ghi nhận tiến trình ngoài phiên nếu có, không tự dừng chúng. Sau đó ghi lại với nhịp tim hiện tại, giữ UTC bắt đầu, hạn không quá hai giờ kể từ lần ghi (`ADR-0059:26–30`). **Kết quả: A gia hạn được**, khớp `ADR-0059:61`. Thay đổi cách tính hạn nằm đúng §3 được bổ sung; không phải thay các phần ADR khác.

**(iii) D10.**

1. Dòng dạng cũ không có hạn, ghi 09:01:16Z; tại thời điểm 13:58Z đã hơn hai giờ. `ADR-0058:35` cho hết hiệu lực theo 3(b), như `ADR-0059:62`.
2. B phải kiểm tải (`ADR-0057:38–39`, `ADR-0059:33–34`). Ca cho biết có PID 26296 chạy `tl.py --selftest`, không phải MCP (`ADR-0059:20,62–64`). Chỉ biết PID còn sống chưa hoàn tất điều kiện mục 2.
3. `ADR-0059:35–37` còn yêu cầu giờ tạo PID sau UTC bắt đầu khoá. `ADR-0059:65–67` thừa nhận số đo không có giờ tạo đó. Tính giờ bắt đầu lượt ở dòng 66 không bổ sung dữ kiện thiếu.
4. Nếu giờ tạo sau 09:01:16Z, mục 2 bắt **không tiếp nhận**, ghi PID/lệnh rồi đợi. Nếu giờ tạo không sau mốc ấy và không có tiến trình khác thoả điều kiện, mục 2 không chặn; `ADR-0058:38–40` cho ghi lý do 3(b) rồi tiếp nhận.
5. **Kết quả từ dữ kiện được cung cấp: chưa quyết định được, không chứng minh được “không tiếp nhận” bắt buộc.** Hai nhánh đã nêu là finding P1 ở trên.

**Biến thể gần đã rà:**

| Biến thể | Câu áp dụng | Kết quả |
|---|---|---|
| (ii), tiến trình của chính A còn chạy trong thư mục riêng | `ADR-0059:49–51`; `ADR-0057:40–41` | Không chặn gia hạn của A; vẫn kiểm tải. Không có ngoại lệ tương tự khi B tiếp nhận khoá của A. |
| Dòng bốn trường ADR-0058, chưa có nhịp tim | `ADR-0059:31–32`; `ADR-0058:30–35` | Đọc như cũ; xét hạn theo 3(a), không tự coi là dòng ba trường hết hiệu lực theo 3(b). Khi chủ khoá ghi lại thì thêm trường năm. |
| Nhịp tim quá 30 phút nhưng UTC hạn chưa qua | `ADR-0059:28,31–32` | Vi phạm nhịp ghi nhưng không tự tạo điều kiện hết hiệu lực mới; không lấy riêng tuổi nhịp tim để tiếp nhận. |
| A định nhả nhưng đọc thấy dòng B còn hiệu lực | `ADR-0059:53–54` dẫn mục 4; dòng 45–48 | A không còn là phiên giữ khoá, không được ghi tệp rỗng để xoá dòng B. |
| A đọc thấy tệp rỗng sau ngắt | `ADR-0059:46–48` | Không còn giữ khoá; phải kiểm tải rồi lấy khoá mới, không gia hạn mù dòng đã mất. |
| Khoá phiên khác hết hiệu lực vì 3(c), còn tiến trình sống | `ADR-0059:38–39`; `ADR-0058:36–40` | Không áp điều kiện cấm tiếp nhận mục 2; vẫn cần bằng chứng tuyên bố bỏ, kiểm tải, ghi sổ đo rồi thay dòng; không được dừng tiến trình khác. |
| Chỉ có tiến trình MCP sau UTC bắt đầu | `ADR-0059:35–37` | Mục 2 không chặn vì loại MCP được loại trừ; các bước tiếp nhận còn lại vẫn áp dụng. |
| B đã tiếp nhận nhưng sau đó khoá B cũng quá hạn | `ADR-0059:46–48` và mục 2 | A chỉ được lấy lại theo luật tiếp nhận khoá B, không khôi phục quyền giữ khoá A cũ. |

Khe đua giữa đọc và ghi được khai tại `ADR-0059:52,73` và `ADR-0058:48–49`; đặc tả §5 loại công cụ khoá nguyên tử khỏi phạm vi, nên không báo lại giới hạn này thành finding.

## Đối chiếu Spec và Standards/Security

- **Nhịp tim / hạn / tiếp nhận:** `ADR-0059:26–39` có đủ trường năm, nhịp ít nhất 30 phút, hạn tối đa hai giờ kể từ lần ghi, kiểm tải, so giờ tạo UTC, loại MCP, ghi PID/lệnh rồi đợi và ngoại lệ 3(c). Không thêm điều kiện hết hiệu lực mới. Giữ UTC bắt đầu giúp điều kiện so tiến trình không trượt theo nhịp tim; chưa thấy quy tắc này làm thay đổi ngoài phần khoá được giao.
- **Ngắt / đọc lại / nhả:** dòng 40–54 có `ngat=co`, khoảng không truy cập được nếu đo được, loại thời lượng ngắt khỏi rà ADR, cấm tự đổi nguồn/ngủ, đọc lại và kiểm session trước ghi, trường hợp gia hạn khoá mình quá hạn, nhả 0 byte ngay cả lượt đỏ/bỏ. Ngoại lệ gia hạn tiến trình mình không mở sang việc tiếp nhận khoá phiên khác.
- **Protocol:** chỉ ba chỉnh sửa đúng §2 đặc tả: câu trung tính §10.2 tại `docs/PROTOCOL_DA_PHIEN.md:1015`; đúng ô mô tả ADR-0058 tại dòng 1538 thêm `; khoá bổ sung bởi ADR-0059` với mã Markdown tương ứng; đúng một dòng ADR-0059 tại dòng 1539, cột cổng nguyên văn `không cổng — kỷ luật executor`. `review-audit.json` xác nhận tái dựng toàn bộ tệp protocol bằng ba sửa đổi này cho byte nội dung tương ứng. Dòng đăng ký chỉ định tuyến tới ADR, không lặp ngưỡng/luật thao tác thành nghĩa vụ mới trong protocol.
- **Số đo:** cả ba ô số đo D10–D12 giống nguyên văn §1 đặc tả; cả hàng giống sau khi bỏ dấu backtick bao tên ADR ở bài học D11. Phép suy giờ bắt đầu lượt đúng; giới hạn suy sang giờ tạo PID là finding đã gộp. D10 chồng `92 s ≈ 1,53 phút`; D12 tại ~01:35Z quá hạn `15455 s ≈ 4 giờ 17 phút 35 giây`.
- **Tham chiếu mục:** `ADR-0058:29–40` thực sự là mục 3 Hạn khoá với (a)/(b)/(c); `ADR-0057:36–49` có mục 3 Khoá, 4 Kiểm tải, 5 Cô lập và 10 Xem xét lại; protocol `:95–97` thuộc §3.1 có câu không tự sửa power policy. Không thấy mục được dẫn bị sai số hoặc mất nguồn.
- **Tham chiếu Git/GitHub:** đã đọc lại [comment chủ kho 6537481455](https://github.com/ducthangho/tra-luat/pull/1062#issuecomment-6537481455): tác giả `ducthangho`, `OWNER`, 2026-10-31T01:57:22Z, duyệt đúng toàn bộ spec hash/blob, PR head `471ad5391c2bcc1d0ee7871907233313db28e9b6` và lease r3/g1 mission gh-1035. [PR #1062](https://github.com/ducthangho/tra-luat/pull/1062) tồn tại, chưa merge, đúng head; [Mission #1035](https://github.com/ducthangho/tra-luat/issues/1035) tồn tại. [PR #1029](https://github.com/ducthangho/tra-luat/pull/1029) và [hồ sơ land #1049](https://github.com/ducthangho/tra-luat/pull/1049) đã merge, phù hợp dependency. [#1021 là Issue](https://github.com/ducthangho/tra-luat/issues/1021), không phải PR; phép hỏi nhầm endpoint PR trả 404, hỏi Issue xác nhận tồn tại. Commit `356a27e1378b2162bbc0be2ec06ff08fdacbdead` tồn tại, message gắn #1021 và session `session_015GtxrZ1Tt93F4NLUUhKYQy`, khớp D12. Các session và giờ trong ba ô số đo khớp đặc tả; chưa trực tiếp đọc được sổ đo/CreationDate trên Windows. Dữ liệu đọc lại được lưu ở `github-reference-evidence.json`.
- **Cưỡng chế / an toàn:** có mục “Không cổng nào cưỡng chế” tại `ADR-0059:77–82`. Đọc `packet_loop.py:1916–2011` xác nhận `adr-song` kiểm đăng ký/trạng thái, không thi hành luật khoá. Tìm các tên dữ liệu khoá/nhịp ngắt/giờ tạo trong các script vận hành của `.claude/dev`, `scripts`, `ops` không có hit trong phạm vi đã lọc (bỏ hồ sơ review). Đây là kiểm mã tĩnh có phạm vi, không chứng minh mọi công cụ ngoài kho. ADR vẫn giữ không dừng tiến trình phiên khác, phạm vi máy theo `list_devices`, cô lập, CI và các điều kiện merge. Chưa thấy sai lệch khác ngoài D10.

Giới hạn: không đo Windows local, không gọi Desktop Commander, không sửa sổ đo/khoá hay chạy test nặng. Không dùng cổng tài liệu xanh để khai Windows CI/local xanh. Snapshot đầu/cuối đầy đủ theo §8.2 thuộc phiên điều phối như prompt nêu; kiểm trạng thái Git trong lượt này không thay snapshot đó. Ngoài lệnh cấu hình `core.abbrev 7` được prompt yêu cầu, chỉ ghi các hiện vật review trong sandbox, không sửa nội dung checkout.

## Đã chạy

Các lệnh Python chạy với `PYTHONDONTWRITEBYTECODE=1`. Ba cổng chạy trong `cay-kho/`; script audit chạy từ sandbox. Rc là mã thoát thật; GET GitHub được ghi theo trạng thái phản hồi của connector, không gán rc shell.

| Lệnh | rc / trạng thái | Dòng kết quả thật hoặc trích trường JSON |
|---|---|---|
| `git -C cay-kho rev-parse HEAD` | 0 | `14795688f2ce2e24c3d4f3f467d862f6772f45fb` |
| `git -C cay-kho rev-parse HEAD^{tree}` | 0 | `96fa900fc9977eafe1768ad52d19a25fa16d2b82` |
| `git -C cay-kho rev-parse --is-shallow-repository` | 0 | `false` |
| `sha256sum spec-r3.md` | 0 | `f1a666a32161f0607ac27bc8c3be6963bb6367e64f02825635a75cc8185fa973  spec-r3.md` |
| `git -C cay-kho show origin/ops/windows-local-may-chu-kho-r3-lease:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md` (audit băm/so byte) | 0 | `spec_equals_fetched_branch_blob: true` |
| `git -C cay-kho cat-file -e HEAD:ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md` | 128, dự kiến | `fatal: path 'ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r3.md' does not exist in 'HEAD'` — dùng bản trên ref lease đã kiểm băm theo prompt |
| `git -C cay-kho config core.abbrev 7` | 0 | Không stdout |
| `git -C cay-kho config --get core.abbrev` | 0 | `7` |
| `python3 .claude/dev/packet_loop.py adr-song --root .` | **0 — passed** | `adr-song: sạch — 58 ADR trên đĩa, 58 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | **0 — passed** | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 scripts/tl.py doc-claims-check --json` | **0 — passed**, hai lần | `"ok": true`, `"files_scanned": 118`, `"flags": []`, `"advisory_count": 381`, `"layers_skipped": {}`, `"strict": false` |
| `git -C cay-kho diff --numstat adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` | 0 | `3\t2\tdocs/PROTOCOL_DA_PHIEN.md`; `89\t0\tdocs/adr/0059-windows-local-nhip-tim-khoa.md` — tổng **2 tệp, 92 thêm, 2 xoá** |
| `git -C cay-kho diff --name-only adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD -- 'docs/adr/0057-*' 'docs/adr/0058-*'` | 0 | Không stdout; hai ADR cũ không đổi |
| `python3 review_audit.py` | **0** | `write_set_exact: true`; `size_within_limit: true`; `diff_matches_supplied_patch: true`; `protocol_only_three_specified_edits: true`; hai giá trị giả định giờ tạo cho hai kết quả chặn khác nhau |
| `git -C cay-kho diff --check adb3d2e977daf9b5623bfc9c7b71b361ecbcf4fc HEAD` | 0 | Không stdout |
| `git -C cay-kho show -s --format=fuller 356a27e` | 0 | Commit `356a27e1378b2162bbc0be2ec06ff08fdacbdead`, subject `wp1021: docstring khop dung hanh vi va ca test hien hanh (tu ra soat truoc luot 8)`, session khớp D12 |
| Quét script bằng `rg` (lệnh đầy đủ bên dưới) | 1 | Không hit; phạm vi chỉ là script theo các glob đã khai |
| `git -C cay-kho status --porcelain=v1 --untracked-files=all --ignored` | 0 | Không stdout; kiểm lần cuối cùng HEAD/tree ở cuối lượt |
| GitHub connector `github_fetch` GET `/repos/ducthangho/tra-luat/issues/comments/6537481455` | Thành công | `id: 6537481455`, `author_association: OWNER`, đúng hash được duyệt |
| GitHub connector `github_get_pr_info` #1062 / #1029 / #1049; `github_fetch_issue` #1035 / #1021 | Thành công | Các neo được đối chiếu ở trên; endpoint PR #1021 trả 404 trước khi dùng endpoint Issue đúng |

Lệnh quét script, rc=1 (không hit):

```bash
rg -n 'CreationDate|KHOA\.txt|ngat=co|do-luong\.csv' cay-kho/.claude/dev cay-kho/scripts cay-kho/ops --glob '*.py' --glob '*.sh' --glob '*.ps1' --glob '!**/reviews/**' --glob '!**/review*/**' --glob '!**/verdict*/**'
```

Lần chạy lại `doc-claims-check` chỉ để lưu đầy đủ JSON vì output lần đầu bị giới hạn hiển thị. Toàn bộ JSON, stderr và bản tóm tắt lần lưu nằm ở `doc-claims-check.stdout.json`, `doc-claims-check.stderr.txt`, `doc-claims-check.summary.json`. Hai cổng packet loop có bản ghi ở `packet-loop-gate-results.json`; phép so diff/spec/bảng/số giờ có lệnh Git và rc chi tiết trong `review-audit.json`. Các cổng này không chứng minh tiền đề lịch sử còn thiếu của D10.
