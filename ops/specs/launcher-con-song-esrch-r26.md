# ĐẶC TẢ — `LAUNCHER-CON-SONG-ESRCH` — **revision 26 — hiệu lực theo quyết định chủ kho, event Mission và lease neo đúng băm toàn tệp**

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp685` (ID bền, `wp<issue>`); tên đọc được: `LAUNCHER-CON-SONG-ESRCH`. Lease dùng tên nào cũng phải kèm `packet_issue: 685`. |
| `revision` | **26 — hiệu lực theo quyết định chủ kho, event Mission và lease neo đúng băm toàn tệp.** Revision 26 được soạn làm đầu vào cho quyết định MCR-686-08 (đổi executor theo quyết định chủ kho, ô `nguon_cap_viec` mục (r24); r25 thay bản soạn r24 sau cross-review lượt 1 trên r24, mục (r25); r26 thay bản soạn r25 sau cross-review lượt 2 trên r25, mục (r26)). Hiệu lực được xác định bởi quyết định chủ kho trên SHA-256 toàn tệp (công thức băm ở dưới), event Mission đọc lại khớp và lease neo đúng băm ấy. Trước khi đủ các điều kiện đó, revision này không cấp quyền thi công; sau khi đủ, chỉ run/generation của lease mới áp dụng revision này. Generation ấy do MCR và lease mới định, tệp này không ghi số. So với r23 (bản đóng băng cuối), r26 đổi ba ô danh tính — `executor`, `environment`, reviewer — cùng vế mức review của ô closure `required_checks` mà ba ô ấy kéo theo, đổi các câu tự nhắc revision hiện hành, thêm vài dữ kiện cùng câu hệ quả của việc đổi nền, và thêm các câu về vai trò của phiên điều phối kiêm executor, về `copyable_prompt` mà phiên ấy điền và về biên nhận `cross_approved`; danh sách đủ là hợp của ba bảng "Thay đổi so với r25" (r25 → r26), "Thay đổi so với r24" (r24 → r25) và "Thay đổi so với r23" (r23 → r24), mọi thứ ngoài ba bảng ấy giữ nguyên chữ của r23. Lease `wp685-r23-g4-codex-20261007` và `wp685-r23-g4b-codex-20261007` được cấp theo r23; theo lời điều phối, g4b hết hạn 2026-10-08T23:00:00Z với `attempts_used: 0` và không có nhánh `agent/wp685*` (phiên soạn r24, r25 và r26 không đọc #686). r26 không áp dụng hồi tố cho hai lease ấy, cho lease `wp685-r20-g3-codex-20261007`, hay cho hồ sơ attempt 3/3 tại event #686 `6031263612`. |
| `thay_the_cho` | (r26) r25 = `ops/specs/launcher-con-song-esrch-r25.md`, SHA-256 `bc3d6f40ebcc74aed20d2f85ab3f40318bc2e351a4cfa44d289014dfed441b31`, commit `0aba473d24b534eea47f47e44fae842202c67dfb` (blob `c479b6f79404e4159a86aadcd38b42c28bf7b215`) — bản soạn ngay trước r26, chưa đóng băng; không event Mission hay lease nào neo nó. r26 sửa r25 theo cross-review lượt 2 trên r25 (VERDICT sha256 `bd84b8a1…6641`, `HINT.patch` sha256 `683f8ad6…ad15`; mục (r26) của `nguon_cap_viec`); danh sách đủ các chỗ đổi, kể cả các chỗ sửa tay ngoài `HINT.patch`, là bảng "Thay đổi so với r25" ở dưới. (r25) r24 = `ops/specs/launcher-con-song-esrch-r24.md`, SHA-256 `be3b416b80681f17a82fa57219c2dac3b0cc52e363890f6bf18ae2a825376fab`, commit `0c91271b27f44f582fc378a4a0def347c02e2fb8` (blob `142031564ad7ad7fe8db7358704c4210367e012a`) — bản soạn ngay trước r25, chưa đóng băng; không event Mission hay lease nào neo nó. r25 = r24 + `HINT.patch` (sha256 `0f90fc6f…1eb4`) của cross-review lượt 1 trên r24 (VERDICT sha256 `67a89d25…0224`; mục (r25) của `nguon_cap_viec`), rồi sửa tay đúng các chỗ ở cột "HINT lệch phép đo" và hàng cuối của bảng "Thay đổi so với r24" ở dưới — hai hunk HINT trên bảng "Thay đổi so với r23" và đoạn "Kiểm lúc soạn r24" không áp, nên r25 không bằng r24 + `HINT.patch` từng byte. (r24) r23 = `ops/specs/launcher-con-song-esrch-r23.md`, SHA-256 `96387f833a0f102742b5f9c86948f2b3f0597d3032dd1817ce732557ae2af939`, commit `063c59dc63a8637e70cf1036e263d09fdabb1c5c` (blob `2ebcd7c2a4e7428b5faadbf3bb8f31e3bb8c4b7a`; cùng blob ở commit `e766eb3` của nhánh metadata) — bản đóng băng mà Mission r6, r7 và lease g4, g4b neo. Về hiệu lực, r26 thay r23 chỉ khi đủ các điều kiện ở ô `revision`. r24 = r23 + đổi ô `executor`, `environment`, reviewer theo quyết định chủ kho (ô `nguon_cap_viec`, mục (r24)) và các câu tự nhắc revision hiện hành — bảng "Thay đổi so với r23" ở dưới; vế mức review của ô closure `required_checks` đổi ở r25, không ở r24. Phần còn lại của ô này là chữ của r23, giữ làm lịch sử (câu "giữ nguyên byte so với r20" trong đó nói về r23, không về r24, r25 hay r26): r22 = `ops/specs/launcher-con-song-esrch-r22.md`, SHA-256 `e9f9e056f4d756849863aa95368a7e044e6e2b50c0a5c7105f3fb1e4e2ad3c5d`, commit `8b026b1daa42ec038389a100c52a380bd0a84a4e` (blob `285957cf514c0d644a2b740925a441c2e88d9f53`) — bản soạn ngay trước r23. r21 = `ops/specs/launcher-con-song-esrch-r21.md`, SHA-256 `1edd6c754ee39645b53e6e0e68c42ece0966b2aa6722fac8d0ea2e7318bf9aef`, commit `1be5beec2430fd428337d1855cca964c28a7b4b3` (blob `e067762e88bd90c777720e748d9577eef309f828`) — bản soạn ngay trước r22. Về hiệu lực, r23 thay r20 = `ops/specs/launcher-con-song-esrch-r20.md`, SHA-256 `645d9a8b2b6887699999fdc349e81d0373bf4705d077ef0878e70def6449ce64`, commit `3d3095305f3525b64aca2508663eecbc20ac19f9` (blob `8481c4708c7f9e5ea0e700a7e81e95bf4fba0b7c`) — chỉ khi đủ các điều kiện ở ô `revision`. r20 thay r19 (`40a14a6e…c604f`) sau quyết định reroute ở [#686 comment 6030761544](https://github.com/ducthangho/tra-luat/issues/686#issuecomment-6030761544); chi tiết ở ô này của r20. r21 = r20 + `HINT.patch` của cross-review Claude trên r20 (chi tiết ở ô này của r21). r22 = r21 + `HINT.patch` của cross-review Claude trên r21 (sha256 `f545c1d6…17cf`; bản gộp do điều phối dựng, sha256 `e67c0a01…f964`), rồi sửa tay ba lớp của VERDICT ấy (sha256 `f4b9fd85…e3be`) sau khi đo lại — bảng "Thay đổi so với r21" ở dưới. r23 = r22 + chỉ các câu tự mô tả trạng thái/hiệu lực, viết lại cho đúng ở cả trước lẫn sau khi đóng băng (mục 7, O4, của VERDICT cross-review Codex trên r22, sha256 `1ccc428f…2543`) — bảng "Thay đổi so với r22" ở dưới. Objective, write set, risk/review class, ô `executor`, danh tính reviewer, hai ô closure `required_checks` và `land_obligations`, và ba khối mã nhúng giữ nguyên byte so với r20; generation áp dụng r23 không ghi trong tệp (ô `revision`). Acceptance so với r20 đổi ở §7 B6: vế ĐỎ khi về khối môi trường của log (r21) kèm ngoại lệ cho log được dùng lại đủ bốn mỏ neo (r22), và phần nghĩa vụ bằng chứng nêu khối ấy (r22). Ngoài §7, mặc định phạm vi đo lại bằng chứng cũ cũng đổi so với r20 (đoạn "Mỏ neo bằng chứng dùng lại", phần (3)). |
| `packet_issue` | **#685** |
| `mission_issue` | **#686** (Mission Issue, object ID `5628902742`). Thân #686 khai ngay đầu rằng nó do phiên agent đăng hộ chủ kho bằng credential chủ kho; nguồn thẩm quyền là các câu trả lời của chủ kho được trích trong đó (Q0–Q4 trong thân; Q5 ở comment `5888633201`, xem `nguon_cap_viec`). |
| `nguon_cap_viec` | (r1) Chỉ thị chủ kho 29-09-2026: *"mở packet riêng cho bản vá launcher (race ProcessLookupError) đi"*. Nguồn lỗi: PR #679, job `gate-ops (ubuntu-latest)` `109303373142`, phân tích ở PR #679 comment `5885963131`. (r2) đến (r13) Cross-review lượt 1 đến lượt 12 trên PR #688, cùng chỉ thị điều phối cho r12 và r13: nguyên văn ở ô này của r13 (sha256 `1ef830ab…97b9`), r12 (sha256 `fba80c32…e89fe2`) và r11 (sha256 `830d5ce4…5604`; ô ấy trỏ tiếp về r10, r9, r8, r7), không chép lại. Còn hiệu lực từ (r9): **quyết định chủ kho** 2026-09-30T06:42:25Z, nguyên văn *"#688: ngay trong packet này"* — lỗi rc=124 do `comm` không giải mã được SỬA trong `wp685`; neo: PR #688 comment `5905670017` (phiên agent đăng hộ; r11 ĐỌC qua REST: comment có trên PR #688, đăng 2026-09-30T06:42:43Z, chứa đúng câu ấy — §10). Còn hiệu lực từ (r11): quyết định chủ kho về lượt lặp và điểm dừng (§11 mục 2), điều kiện cấp lease Q5 (§11 mục 4). Còn hiệu lực từ (r13): **quyết định chủ kho về kích thước thi hành** — trần ADR-0044 **≤ 1400 dòng thêm**, quyết định 2026-10-01T00:42:15Z, neo PR #688 comment `5922387653`; THAY quyết định ≤ 600 (00:29:39Z, comment `5922248948`) vì con số đưa vào câu hỏi trước thiếu helper — nguyên văn, neo và lý do ở §4, mục "Ngoại lệ ADR-0044". **(r14)** Cross-review lượt 13 trên PR #688, reviewed commit `da119d74ea4a9d25f17857bd278ca3e58989c1ec` (r13, commit CỤC BỘ theo `quy_uoc_review`; spec sha256 khớp băm r13). Reviewer Claude Opus 5.5, effort max — **`advisory_review`, CÙNG HỌ với executor và phiên soạn, KHÔNG phải `cross_approved`**; họ model là tự khai. Kết luận `changes_requested`, **0 P1 / 0 P2 / 2 P3**: `kich-thuoc-thi-hanh-vuot-adr-0044` (P3 — phần P2 của lượt 12 ĐÃ ĐÓNG; VÁ SINH LỖI MỚI: lời khai §4 rộng hơn đo), `khai-khong-do-duoc-ma-do-duoc` (P3, TÁI PHÁT — nhãn mục 5 bảng bất khả thi và trục C cũ đi vì chính luật `T3` của r12); `chot-tinh-bien-chua-khep` ĐÃ ĐÓNG; `ma-tran-loi-thieu-chot` không tái phát — điều kiện dừng của §11 mục 2 KHÔNG kích hoạt. VERDICT sha256 `2bbac4e8d1c7f46eb9eeb529b41f998618ed67288b2364d90dde5f487a073fb0`, `HINT.patch` sha256 `1ca8b3d87c5d3ebacc50b7f3217da1bdde1b5d08810ff092bb02bce4a586f7ab`; phiên soạn r14 đo cả hai bằng `sha256sum` trước mọi việc khác và lại lúc đóng băng, khớp chỉ thị (bảng 16). Bản chiếu VERDICT lượt 13 trên PR #688: phiên soạn r14 KHÔNG đọc PR (không REST, không MCP) — CHƯA ĐO. **Chỉ thị cho r14** (lời điều phối cấp, không có neo GitHub): r14 = r13 + HINT lượt 13 (đổi tên tệp CHỈ trên dòng `---`/`+++`), rồi đóng hai lớp P3 — tự liệt kê HẾT lời khai của §4 và của mục 5 bảng bất khả thi, đối chiếu từng cái với phép đo: sửa số học, thu hẹp lời khai về đúng thứ đo được, thay CHƯA ĐO đã được đo bằng số đo có nguồn; mục 5 đổi nhãn theo đo, chỉ giữ phần hở thật với lý do đúng; đo `git diff --quiet fc852ff 20ec8d5 --` hai tệp write set, giữ nền `423b4ba` nếu write set không đổi. **(r15)** Cross-review lượt 14 trên PR #688, reviewed commit `0586ab7e68de4a7f4ca1ecf733206cd7bb3ed88d` (r14, commit CỤC BỘ theo `quy_uoc_review`; spec sha256 khớp băm r14). Reviewer Claude Opus 5.5, effort max — **`advisory_review`, CÙNG HỌ với executor và phiên soạn, KHÔNG phải `cross_approved`**; họ model là tự khai. Kết luận `changes_requested`, **0 P1 / 0 P2 / 2 P3**: `khai-khong-do-duoc-ma-do-duoc` (P3 — hai chỗ lượt 13 ĐÃ ĐÓNG; VÁ SINH LỖI MỚI: §10 "Răng của bộ sinh" rộng hơn đo, B2 mục 5 gạch 1 hẹp hơn đo), `kich-thuoc-thi-hanh-vuot-adr-0044` (P3 — bốn chỗ lượt 13 ĐÃ ĐÓNG; VÁ SINH LỖI MỚI: bảng 16 dòng 13 ghi số DÒNG thành số LẦN); `ma-tran-loi-thieu-chot` không tái phát — điều kiện dừng của §11 mục 2 KHÔNG kích hoạt; không lớp nào của lượt 9 đến 12 tái phát. VERDICT sha256 `b5f0811ce5031b5403ce0593988048722023a4ee1a890f2f8e7dda5d36f8da0e`, `HINT.patch` sha256 `4ba3aee315be2f154c10885c73a8770f765688a9dcfa7e8c61d26e837143d13f`; phiên soạn r15 đo cả hai bằng `sha256sum` trước mọi sửa và lại lúc đóng băng — VERDICT khớp chỉ thị, HINT khớp số VERDICT khai. Bản chiếu VERDICT lượt 14 trên PR #688: comment `5925622594` theo lời điều phối; phiên soạn r15 KHÔNG đọc PR (không REST, không MCP) — CHƯA ĐO. **Chỉ thị cho r15** (lời điều phối cấp, không có neo GitHub): việc nhỏ, chỉ header — r15 = bản gộp r14 + HINT lượt 14 (điều phối dựng sẵn, sha256 `fffa8ba0…95b8`), kiểm hai chỗ HINT sửa bằng `grep` trên chính tệp, tự rà toàn tệp chỗ cùng lớp còn sót; đổi `revision`, `thay_the_cho`, bảng "Thay đổi so với r14", thêm mục (r15) vào ô này, đổi mọi câu tự nhắc tên tệp r14 thành r15 mà không đổi tham chiếu lịch sử; không thêm phép đo mới; giữ nguyên ba khối mã nhúng. **(r16)** Cross-review lượt 15 trên PR #688, reviewed commit `13660c450fa711d7e02637401cfda676ad436ac2` (r15, commit CỤC BỘ theo `quy_uoc_review`; spec sha256 khớp băm r15). Reviewer Claude Opus 5.5, effort max — **`advisory_review`, CÙNG HỌ với executor và phiên soạn, KHÔNG phải `cross_approved`**; họ model là tự khai. Kết luận `changes_requested`, **0 P1 / 0 P2 / 1 P3**: `so-lieu-noi-bo-lech` (P3, TÁI PHÁT — lớp lượt 6, đóng lượt 7; hai biểu hiện: số đếm mà bảng thay đổi ở đầu r15 gán cho r15 là số của bản gộp, và câu B7 của §10 — có từ r9 — lệch §7 và lệch hồ sơ review); hai lớp lượt 14 ĐÃ VÁ THẬT; `ma-tran-loi-thieu-chot` không tái phát — điều kiện dừng của §11 mục 2 KHÔNG kích hoạt; không lớp nào của lượt 9 đến 13 tái phát. VERDICT sha256 `d6f3b4762736e56be4f88d5be7c57ccc16d0d12abd6a36828fdf197851897732`, `HINT.patch` sha256 `f884f418fd052c0f697ebbc61c9566bf54eb1e36d450fea8df450e1cb5b0110c`; phiên soạn r16 đo cả hai bằng `sha256sum` trước mọi sửa và lại lúc đóng băng — VERDICT khớp chỉ thị, HINT khớp số VERDICT khai. Bản chiếu VERDICT lượt 15 trên PR #688: comment `5928898872` theo lời điều phối; phiên soạn r16 KHÔNG đọc PR (không REST, không MCP) — CHƯA ĐO. **Chỉ thị cho r16** (lời điều phối cấp, không có neo GitHub): việc nhỏ, chỉ header — r16 = bản gộp r15 + HINT lượt 15 (điều phối dựng sẵn, sha256 `98c89519…20bd`); thay bảng thay đổi bằng bảng của r16, thêm mục (r16) vào ô này, đổi mọi câu tự nhắc tên tệp r15 thành r16 mà không đổi tham chiếu lịch sử; bảng mới và mục này không trích nguyên văn chuỗi nào mà tệp đếm bằng `grep`, và mọi số `grep` mà r16 khai về chính nó phải đo lại trên chính tệp r16; rà toàn tệp các lời khai cùng lớp (lượt nào đã đo gì); không thêm phép đo mới về mã; giữ nguyên ba khối mã nhúng. **(r17)** Cross-review lượt 16 trên PR #688, reviewed commit `ac234c479c13ec4ca3bf82626fcb61b1e8d7b426` (r16, commit CỤC BỘ theo `quy_uoc_review`; spec sha256 khớp băm r16). Reviewer Claude Opus 5.5, effort max — **`advisory_review`, CÙNG HỌ với executor và phiên soạn, KHÔNG phải `cross_approved`**; họ model là tự khai. Kết luận `changes_requested`, **0 P1 / 0 P2 / 1 P3**: `so-lieu-noi-bo-lech` (VÁ SINH LỖI MỚI); `ma-tran-loi-thieu-chot` không tái phát — điều kiện dừng của §11 mục 2 KHÔNG kích hoạt. Chi tiết chỉ ở chính VERDICT, sha256 `73bbc20b10e280884fa43df764877927754fce2ae429a4f8df483cfe55ed3c75`; `HINT.patch` sha256 `cbdc376a407e93147c17f9ff51202b8a33e366637e3cc22c7a3b8fd645ae3d38`; phiên soạn r17 đo cả hai bằng `sha256sum` trước mọi sửa và lại lúc đóng băng. Bản chiếu VERDICT lượt 16 trên PR #688: comment `5929647804` theo lời điều phối; phiên soạn r17 KHÔNG đọc PR (không REST, không MCP) — CHƯA ĐO. **Chỉ thị cho r17** (lời điều phối cấp, không có neo GitHub): việc nhỏ, chỉ header — r17 = bản gộp r16 + HINT lượt 16 (điều phối dựng sẵn, sha256 `b7398e95…d1bc`); không sửa câu nào ngoài phần đầu tệp, đoạn HINT sửa và các câu tự nhắc tệp hay lease của revision hiện hành; không tự rà sửa câu thân; viết ngắn, trỏ VERDICT thay vì chép số. **(r18, 05-10-2026)** Chủ kho duyệt đổi executor sang Google Antigravity / Gemini 3.1 Pro High tại Mission #686 comment `5988699983`, trả lời đúng MCR đề xuất ở comment `5988682502`; đây là quyết định về provider, không tự cấp lease. Mission Plan revision 3 đã được cài bằng manual bootstrap tại #686 comment `5992836950`, plan hash `38b2b3ef9d4a410e2a6a00fdc1861611fd39295b7652062d2988ebc3513feb8a`; wp709 đã landed tại #709 comment `6020718211`. r18 vẫn là DỰ THẢO vì chưa đóng băng/cấp lease riêng (câu này tả lúc soạn r18). **(r19)** Mission #686 MCR-686-03, quyết định chủ kho 07-10-2026 tại [comment 6027925595](https://github.com/ducthangho/tra-luat/issues/686#issuecomment-6027925595): *"Cho phép codex vừa làm executor vừa làm reviewer, có hint patch, tiếp đi"* — executor Codex, reviewer Codex ở phiên/context độc lập, assurance tối đa `same_provider_approved`, human audit exact SHA trước land. **(r20)** Reroute generation 3 tại [comment 6030761544](https://github.com/ducthangho/tra-luat/issues/686#issuecomment-6030761544) (đề xuất ở `6030719075`); MCR-686-05 đề xuất ở `6030894126`, chủ kho duyệt ở `6030902827` (trên một băm r20 trước đính chính, `e4134ec3…f34d`) và duyệt lại đúng băm r20 `645d9a8b…ce64` ở `6030965299` — đọc từ bản REST của các comment ấy do điều phối cấp. **(r21)** Cross-review đặc tả trên PR #688, reviewed commit `3d3095305f3525b64aca2508663eecbc20ac19f9` (r20; spec sha256 khớp băm r20). Reviewer Claude Sonnet 5.5, effort max — `advisory_review`, KHÁC họ executor và phiên soạn r18–r20 theo lời tự khai, KHÔNG phải `cross_approved` của PR thi hành, KHÔNG thay `human_audited`. Kết luận `changes_requested`, **0 P1 / 2 P2 / 3 P3**; năm slug ở bảng "Thay đổi so với r20". VERDICT sha256 `1cdbbd4949c9a35a389cedc927ae85d80428d87e2c7f8ec0a5c6b724f4e6dec9`, `HINT.patch` sha256 `346f7fa2c58648ed73f9e06b92752cc81bd9922c7437847d3be108beddaf448e`; phiên soạn r21 đo cả hai bằng `sha256sum` trước mọi sửa. Bản chiếu VERDICT trên PR #688: comment `6034918124` theo lời điều phối; phiên soạn r21 KHÔNG đọc PR — CHƯA ĐO. **Chỉ thị cho r21** (lời điều phối cấp, không có neo GitHub): r21 = bản gộp r20 + HINT, đối chiếu VERDICT và tự đo lại từng lớp, tự liệt kê hết đường cùng cơ chế trước khi vá; trạng thái đề xuất, chưa đóng băng, chưa có MCR; không khai r21 có hiệu lực, được duyệt hay thay lease g3; giữ executor, generation, reviewer của r20 trừ chỗ lớp vá đòi đổi; ba khối mã nhúng giữ nguyên byte. Phiên soạn r21: Claude Opus 5.5 (họ anthropic, tự khai) — CÙNG họ với reviewer của lượt sinh ra r21, nên một review r21 muốn tính là độc lập với phiên soạn thì cần reviewer họ khác. **(r22)** Cross-review đặc tả trên PR #688, reviewed commit `1be5beec2430fd428337d1855cca964c28a7b4b3` (r21; spec sha256 khớp băm r21). Reviewer Claude Sonnet 5.5, effort max — `advisory_review`, KHÁC họ executor nhưng CÙNG họ anthropic với phiên soạn r21 (VERDICT tự khai), KHÔNG phải `cross_approved` của PR thi hành, KHÔNG thay `human_audited`, KHÔNG thay MCR. Kết luận `changes_requested`, **0 P1 / 0 P2 / 3 P3**; ba slug ở bảng "Thay đổi so với r21". VERDICT sha256 `f4b9fd8584f8f620a2967ba81c16474608d32c968b74d27370f218dd5147e3be`, `HINT.patch` sha256 `f545c1d66a05c1519d81cc717400971d7d13be195c1d04ae23347e18ca0c17cf`; phiên soạn r22 đo cả hai bằng `sha256sum` trước mọi sửa. Bản chiếu VERDICT trên PR #688: comment `6036776986` theo lời điều phối; phiên soạn r22 KHÔNG đọc PR — CHƯA ĐO. **Chỉ thị cho r22** (lời điều phối cấp, không có neo GitHub): r22 = bản gộp r21 + HINT, kiểm từng lớp và tự đo lại, rà hết đường cùng cơ chế; chỉ sửa đúng ba lớp, không viết đoạn mới dài; câu về trạng thái phải neo thời điểm và nguồn hoặc diễn đạt không thời gian; không trích nguyên văn chuỗi mà tệp tự đếm; trạng thái đề xuất, chưa đóng băng, chưa có MCR; r20 vẫn là băm lease g3 neo; ba khối mã nhúng giữ nguyên byte. Phiên soạn r22: Claude Opus 5.5 (họ anthropic, tự khai) — cùng họ với reviewer của lượt sinh ra r22. **(r23)** Hai cross-review đặc tả trên r22, cùng reviewed commit `8b026b1daa42ec038389a100c52a380bd0a84a4e` (r22; `spec_sha256` ở header của cả hai VERDICT khớp băm r22). (a) Codex `gpt-6.1-sol` (`reviewer_provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine` — header VERDICT, tự khai) — KHÁC họ anthropic của phiên soạn r21, r22, r23, CÙNG họ với executor; kết luận `approve`, **0 P1 / 0 P2 / 0 P3**, không có `HINT.patch`; VERDICT sha256 `1ccc428f36a3e8489c92d1b41496cd43f97dcf1c28ba10bbfc757b5ed4052543`; mục 7 (O4) của nó khuyến nghị soạn revision 23 trước đóng băng và cho mẫu văn xuôi đúng ở cả hai phía — nguồn của bảng "Thay đổi so với r22"; bản chiếu trên PR #688: comment `6039140503` theo lời điều phối. (b) Claude Sonnet 5.5 (`reviewer_provider: anthropic`, `execution_surface: claude_code`, `transport: machine/local` — header VERDICT, tự khai) — CÙNG họ với phiên soạn; kết luận `approve`, **0 P1 / 0 P2 / 0 P3**, không có `HINT.patch`; VERDICT sha256 `313344478482557c67d89f9e05f69267da3d45762b5cf6bad9d14a24b20d1589`; chỉ thị không nêu bản chiếu của VERDICT này. Cả hai là review ĐẶC TẢ (VERDICT tự nêu): không phải approval mã thi hành, KHÔNG thay `human_audited`, KHÔNG thay quyết định chủ kho. Phiên soạn r23 đo cả hai VERDICT bằng `sha256sum` trước mọi sửa; KHÔNG đọc PR — bản chiếu CHƯA ĐO. **Chỉ thị cho r23** (lời điều phối cấp, không có neo GitHub): chủ kho chọn soạn r23 để đóng băng, kèm bản nháp MCR-686-06 (ngoài tệp này); r23 = r22 + chỉ sửa các câu tự mô tả trạng thái/hiệu lực thành câu đúng ở cả hai phía của việc đóng băng, theo O4; generation tương lai lấy từ MCR/lease, không ghi cứng; objective, B1–B8, closure, write set, ba khối mã nhúng và thân §1–§10 bằng r22 từng byte, trừ đúng các câu tự mô tả. Phiên soạn r23: Claude Opus 5.5 (họ anthropic, tự khai). **(r24)** Quyết định chủ kho đổi executor, cho trong phiên Claude Code `https://claude.ai/code/session_01CSM7GNazhN6uGJb4v1TqBT` ngày 2026-10-09 (khoảng 16:4xZ; lời điều phối cấp, không có neo GitHub — bản ghi bền là comment chủ kho trên #686 neo sha256 của `ops/missions/mcr-686-08.yaml` và plan hash Mission r8), nguyên văn câu trả lời: *"Đổi executor sang Claude (tôi)"*. Bối cảnh theo lời điều phối (phiên soạn r24 không đọc #686): lease g4b (Codex Desktop trên Windows của chủ kho) hết hạn 2026-10-08T23:00:00Z, `attempts_used: 0`, không có nhánh `agent/wp685*`, và chưa có event Mission nào cho g4b sau comment cấp quyền `6049189081`. Nghĩa, theo lời điều phối: executor = Claude (phiên Claude Code cloud; `anthropic_claude`, `claude_code`, `machine/local`, container Linux cloud), reviewer = Codex, khác họ; objective, B1–B8, write set hai tệp, nền `ab457c6`, review class `sensitive` và land obligations giữ nguyên. Protocol §3.1.1 và §3.2: đổi executor hay environment cần revision và generation mới ⇒ r24 và MCR-686-08. Phiên soạn r24: Claude Opus 5.5 (họ anthropic, tự khai) — chính phiên điều phối mà câu trả lời của chủ kho chọn làm executor ("(tôi)"; trailer `Claude-Session` của commit r24 trỏ đúng phiên ấy), tức CÙNG PHIÊN với executor mới, không chỉ cùng họ; hệ quả về vai trò ở ô reviewer. r24 chưa qua cross-review đặc tả. **(r25)** Cross-review lượt 1 trên r24 (exact `fe68876480c10ae7c24520020354ecdb2b4f4a11`, spec sha256 `be3b416b…6fab`): reviewer Claude Opus 5.5 (tự khai), cùng họ và cùng cây phiên với phiên soạn ⇒ `advisory_review`, không phải `cross_approved`; `VERDICT.md` sha256 `67a89d25c6901b59e38fc9cc83944e3a936f680b3b3acb4ec7bcfa517ec70224`, `changes_requested`, 1 P1 / 1 P2 / 3 P3 (năm lớp ở bảng "Thay đổi so với r24"); `HINT.patch` sha256 `0f90fc6f9db031c2be9d255eae7d4312a94355c5f5294ac851758af08b021eb4`. Chỉ thị điều phối: sửa thành revision mới r25, tệp r24 giữ nguyên byte làm lịch sử. Phiên soạn r25: subagent Claude Opus 5.5 (họ anthropic, tự khai) của cùng phiên điều phối. r25 chưa qua cross-review đặc tả. **(r26)** Cross-review lượt 2 trên r25 (exact `6c6e3d891274f50a36014cf8cd4440449af8987d`, spec sha256 `bc3d6f40…1b31`): reviewer Claude Opus 5.5 (tự khai), cùng họ và cùng cây phiên với phiên soạn ⇒ `advisory_review`, không phải `cross_approved`; `VERDICT.md` sha256 `bd84b8a1b724ce36078acf8344b13d158e5a89099eecedf31fb61eb502f66641`, `changes_requested`, 0 P1 / 0 P2 / 2 P3 (hai lớp ở bảng "Thay đổi so với r25"); `HINT.patch` sha256 `683f8ad682a36e033acdddaae1adb410d7e3527ca0a09ab7d23afb83c6f1ad15`. Chỉ thị điều phối: sửa thành revision mới r26, tệp r25 giữ nguyên byte làm lịch sử. Phiên soạn r26: subagent Claude Opus 5.5 (họ anthropic, tự khai) của cùng phiên điều phối. r26 chưa qua cross-review đặc tả. |
| `quy_uoc_review` | **(r8, chủ kho chốt 30-09; dữ kiện do phiên điều phối cấp, phiên soạn r8 không kiểm trên GitHub)** Từ r8, mỗi revision chỉ được commit CỤC BỘ và được review trên CHÍNH commit cục bộ ấy; PR chỉ được đẩy khi review ra **0 P1 / 0 P2 / 0 P3**. Thứ định danh revision là sha256 của tệp cộng OID commit, không phải tên nhánh. |
| `objective` | `_con_song` không bao giờ để một ngoại lệ `OSError` của phép hỏi `/proc/<pid>/stat` thoát ra; tiến trình biến mất giữa chừng (ESRCH) được báo là đã chết; lỗi khác KHÔNG được đọc thành "đã chết" chỉ vì không stat được, và một zombie vẫn được báo là đã chết khi nội dung `/proc/<pid>/stat` còn đọc được. **(r9, quyết định chủ kho 2026-09-30T06:42:25Z, lời điều phối cấp: "#688: ngay trong packet này")** Năm chỗ đọc `/proc/<pid>/stat` của launcher — `_khoa_danh_tinh`, `_thanh_vien_nhom`, `_chup_cay` và hai khối đọc của `_con_song` — không bao giờ đọc một tiến trình CÒN SỐNG thành "đã biến mất", "đã chết" hay "không có khoá" chỉ vì `comm` không giải mã được hay locale không phải UTF-8 (Q-A.7): `run --deadline-utc` không trả 124 và `stop` không trả 0 khi tiến trình của cây còn sống, và tên chương trình không phải ASCII không làm lượt chạy trả 10 (B8). **(r10)** Khoá danh tính Linux giữ đúng định dạng nền `linux:<starttime>`, để `stop` của một bản launcher khác vẫn so được khoá trong `run.json` (Q-A.7). |
| `review_class` | **`sensitive`** — protocol §8: *"launcher hoặc gate lifecycle"*. |
| `risk` | **`sensitive`**: cùng lý do. |
| `executor` | (r24) `claude` — Claude Opus 5.5 (`claude-opus-5-5`, họ `anthropic`; trong biên nhận khai `provider: anthropic_claude`), `execution_surface: claude_code`, `transport: machine/local` (giá trị duy nhất mà `RUNTIME_CAPABILITIES` của `ops/lease_publish.py` nhận cho `claude`), theo quyết định chủ kho ở ô `nguon_cap_viec`, mục (r24); generation do MCR-686-08 và lease mới định, tệp này không ghi số. Executor chạy trong một checkout cô lập mới và không tự review. Lịch sử: r20 đến r23 giao `codex` — GPT-6 Astra, `execution_surface: codex_desktop`, `transport: machine/local` (generation 3, 4). Candidate local `4c404f9a50b24730f823b5c22376548c6ee67e4f` của generation 3 là checkpoint, không phải approval, và chỉ có ở máy executor cũ (đoạn "Mỏ neo bằng chứng dùng lại", phần (5)). Attempt và same-failure history của các generation trước giữ làm dữ liệu; trần của generation mới do MCR định. |
| `environment` | (r24) `cloud` — container Linux của phiên Claude Code cloud chạy executor; các lệnh Linux của B1–B6 và B8 chạy ngay trong container ấy, và container phải là một **môi trường Linux đạt tiêu chí máy kiểm dưới đây**; tên bản phân phối không cố định. (r20 đến r23: `local` — Codex Desktop trên Windows, lệnh Linux chạy trong WSL của máy executor hay một Linux khác.) **Tiêu chí (r21, cross-review lớp `moi-truong-nghiem-thu-khai-sai`)**, đo bằng các lệnh mở đầu MỖI log của B1–B6 và B8, ghi đầu ra nguyên văn kèm giờ UTC: (a) `uname -s` in đúng `Linux`, kèm đầu ra của `uname -r` và `uname -m`; (b) `cat /etc/os-release` đọc được, có `ID=` không rỗng và `VERSION_ID=` không rỗng (giá trị tính sau khi bỏ một cặp nháy bao ngoài) — (r22) `VERSION_ID` là trường tuỳ chọn của os-release, nên khi tệp không có `VERSION_ID=` hay có mà rỗng thì dùng `BUILD_ID=` nếu không rỗng, không thì `VERSION_CODENAME=` không rỗng, theo đúng thứ tự ấy, và bộ năm bên dưới dùng đúng trường được chọn; (c) `python3.11 -V` rc=0 và dòng đầu ra bắt đầu bằng `Python 3.11.` với ký tự ngay sau là chữ số (số vá), `python3.12 -V` cũng vậy với `Python 3.12.` (không gọi `python` trần, như B6); (d) ghi thêm nguyên văn `uname -a`. **Dạng khối** (r22; để người và máy đọc cùng một cách): đứng trước mọi dòng khác của log, kể cả dòng lệnh nguyên văn của chính log; dòng đầu `# UTC <YYYY-MM-DDTHH:MM:SSZ>`; rồi bảy lệnh đúng thứ tự liệt kê ở (a)–(d) — `uname -s`, `uname -r`, `uname -m`, `cat /etc/os-release`, `python3.11 -V`, `python3.12 -V`, `uname -a` — mỗi lệnh là một dòng `$ <lệnh>`, đầu ra nguyên văn và một dòng `# rc=<số>` — rc=0 của (c) đọc ở dòng này; dấu CR cuối dòng bỏ đi trước mọi phép so, trong khối và trong bộ năm. Thiếu khối ấy, hay (a), (b) hoặc (c) không đạt ⇒ log ấy không phải bằng chứng (vế ĐỎ khi (r21) của B6, kèm ngoại lệ (r22) ở đó cho log được dùng lại đủ bốn mỏ neo). **Cùng môi trường** — điều kiện (iv) của đoạn "Mỏ neo bằng chứng dùng lại" — nghĩa là bằng nhau TỪNG BYTE bộ năm: `ID`, `VERSION_ID` (hay trường được chọn ở (b); giá trị như ở (b)), `uname -r`, `uname -m`, và dòng `-V` của đúng bản Python của dòng bằng chứng; `uname -a` chỉ để ghi, không đem so (nó còn chứa tên máy và chuỗi bản dựng). Dữ kiện, không phải phép đo của phiên soạn r21: bảng lịch sử r18 ghi Ubuntu-Clean gọi được 3.11.17 và 3.12.3; sổ Mission #686 comment `6031263612` ghi Ubuntu-Clean có cả hai còn Debian không có Python — tức Debian trên máy ấy không đạt (c); kiểm trên chính máy ấy: KHÔNG ĐO ĐƯỢC (lý do 2). Phiên soạn r21 chạy (a)–(d) trên container của mình (ra `Linux`, `6.18.44-fc-v77`, `x86_64`, `ID=ubuntu`, `VERSION_ID="24.04"`, `Python 3.11.15`, `Python 3.12.3`, mỗi lệnh rc=0; một tên `python3.99` không có ⇒ rc=127) chỉ để chứng tỏ tiêu chí cho kết quả máy phân biệt được — container ấy không phải môi trường nghiệm thu. (r24) Phiên soạn r24 chạy (a)–(c) trên container của mình lúc 2026-10-09T16:38:27Z (ra `Linux`, `6.18.44-fc-v80`, `x86_64`, `ID=ubuntu`, `VERSION_ID="24.04"`, `Python 3.11.15`, `Python 3.12.3`, mỗi lệnh rc=0) — dữ kiện, không phải bằng chứng nghiệm thu: môi trường nghiệm thu là container của chính run executor, đo bằng khối ở đầu mỗi log. Container cloud có thể được dựng lại giữa hai phiên với `uname -r` khác (r21 ghi `-fc-v77`, r24 đo `-fc-v80`), nên điều kiện (iv) chỉ so trên bộ năm đọc trong log, không suy từ tên nền. Không tiêu chí nào của ô này cần Windows. Các phép đo Windows của packet — số thật của sàn đột biến B4, Python 3.13, `launcher-windows.yml` — vốn ở sau merge (Q4; §10 lý do 2), không thuộc phía executor, và không đổi khi đổi nền executor; thứ duy nhất mất đi là KHẢ NĂNG một executor trên Windows tự chạy thêm ở máy mình, mà r20 đến r23 không đòi. Phạm vi đo tiếp và điều kiện dùng lại bằng chứng: đoạn "Mỏ neo bằng chứng dùng lại" bên dưới. |
| reviewer | `codex`, phiên/context độc lập với Executor, checkout read-only; model thực tế phải khai trong verdict. (r24) Executor nay là `claude` (họ anthropic) còn reviewer là `codex` (họ openai), khác họ ⇒ review đạt `cross_approved` nếu 0 P1/P2/P3, đủ bằng chứng exact SHA và đủ bằng chứng họ model theo PROTOCOL §8 mục 1 (`khong_do_duoc` không đủ) (r20 đến r23, khi executor là `codex`, mức ấy là `same_provider_approved`); vì `sensitive`, cần thêm `human_audited` trên chính SHA đó trước land. Reviewer đọc exact SHA ứng viên trong checkout read-only riêng. (r25; r26 sửa) Executor là chính phiên điều phối (ô `nguon_cap_viec`, mục (r24)), nên từ lúc cấp lease phiên ấy chỉ giữ vai executor trên wp685 (PROTOCOL §1 mục 8): không tự dispatch hay dựng sandbox cho reviewer của chính ứng viên mình, không soạn assignment riêng cho reviewer ấy, không ghi event review hay biên nhận — PROTOCOL §7: *"Executor không tự tạo review có thẩm quyền; nếu chưa có automation, nó chỉ xuất prompt thủ công nói trên và dừng."* (r26) Prompt thủ công ấy là `copyable_prompt` của handoff (PROTOCOL §7; mẫu `docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md`, mục "Prompt Reviewer có thể sao chép"): executor điền đúng các trường của mẫu, không thêm hướng thử hay gợi ý, rồi dừng; đó là tiện ích bootstrap, không phải assignment. Reviewer Codex do chủ kho hay một phiên khác phiên executor gọi; `codex` có sẵn trong container của executor không đổi điều đó. (r25) Biên nhận `cross_approved` của packet này (đo bằng `ops/bien_nhan_v2.py` của `ab457c6` trên biến thể của `wp523-r14-review-1-codex`): phải xác định được họ executor — `executor_provider: anthropic_claude` hay khối `model_executor_identity` (vắng ⇒ ĐỎ); vai nào khai đè `model` thì vai ấy cần `model_evidence` (`do_may` kèm `model_evidence_ref`, hay `khai_co_audit` kèm người audit; vắng hay `khong_do_duoc` ⇒ ĐỎ); vẫn cần `session_run_id` hay `phien_doc_lap`. Cổng không bắt nhãn `same_provider_approved` gán cho cặp executor `anthropic_claude`, reviewer `openai_codex` (đo: ĐẠT), nên đúng nhãn là việc của người ghi biên nhận. **Từ vựng biên nhận (r21, cross-review lớp `o-reviewer-lech-luat-hien-hanh`; đo bằng `ops/bien_nhan_v2.py` của `ab457c6` trên biên nhận có sẵn `wp523-r14-review-1-codex` và `assurance-ho-model-review-1-claude`, chín biến thể, mỗi biến thể đổi một trường — hai biến thể `same_provider_approved` đổi thêm `assurance` — so với nền 186 ĐẠT rc=0):** `codex` ở ô này là tên của từ vựng LEASE (`PROVIDER_FAMILIES` của `ops/lease_publish.py`). Trong `model_reviewer_identity` của `ops/reviews/*.receipt.yaml`, reviewer Codex khai `provider: openai_codex` (ghi `codex` ⇒ ĐỎ, ngoài danh sách cho phép), `surface: codex_desktop` hay `codex_cli`, và `transport: machine` hoặc bỏ trường (`machine`, vắng ⇒ ĐẠT rc=0; `machine/local`, `local`, `human` ⇒ ĐỎ rc=1; `assurance: same_provider_approved` với `machine` ⇒ ĐẠT, với `machine/local` ⇒ ĐỎ). `machine/local` là cách khai legacy mà chỉ cổng lease nhận (`RUNTIME_CAPABILITIES`; lease g3 dùng nó cho executor, hợp lệ ở cổng ấy). Biên nhận của reviewer Claude cho cùng packet (`land_obligations` ghi sổ verdict kèm receipt) thì NGƯỢC chiều: `provider: anthropic_claude`, `surface: claude_code`, `transport: machine/local` (`machine` ⇒ ĐỎ; `surface: claude_code_subagent` ⇒ ĐỎ). Nguồn hợp đồng: `_TRANSPORT_CONTRACTS` và `_PROVIDER_NGOAI_CLI` của `.claude/dev/launcher.py` — tệp trong write set, nhưng chốt `M` cấm đổi mức module nên packet này không sửa được chúng. Protocol §8: HINT không được chứa mã launcher; chỉ được chứa mã TEST thuần. (Câu ấy có ở r17 và r18; r19 bỏ, r21 khôi phục.) Reviewer có thể đính patch-as-hint trong verdict dạng artifact, không push ref, mang nhãn nguyên văn của ràng buộc 1 ở PROTOCOL §8; với packet `sensitive` này hint chỉ đủ điều kiện cho hunk TEST thuần vào `.claude/dev/launcher_test.py` — hunk vào `.claude/dev/launcher.py`, hunk hỗn hợp hay đường dẫn không phân loại được đi đường mô tả hướng (PROTOCOL §8, ba ràng buộc của patch-as-hint); executor khai `hint_provenance`; hints không cho quyền ghi branch Executor. Các review trước generation 3 — và (r24) mọi review của generation 3, 4 — là lịch sử, không mang verdict sang candidate mới. |
| `depends_on` | Packet #709 (provider adapter) — ĐÃ LAND, PR #712 merge `ab457c651eb4428705f0492163080b661c858b72`, receipt #709 comment `6020718211`; Packet #668 (Mission #686 Q1: xếp sau #668) — **ĐÃ LAND** (PR #696, merge `423b4ba`). Lease cuối của nó, `ci-g5-cong-cu-chia-manh-r1-g3-claude`, đã rút hạn về `2026-09-30T09:55:00Z` (commit `86b23c0f5c2becf17ede9f951892a1d2b40df141`, đầu nhánh `ops/cap-lease-ci-g5-cong-cu-chia-manh`; đọc thẳng từ tệp lease). **Đo ở r10** (§8): `ai-dang-giu .claude/dev/launcher_test.py` ⇒ `NGƯỜI_GIỮ 0`, rc=0 (10:46:54Z 30-09; g1, g2, g3 của #668 đều `HẾT_HẠN`); `ai-dang-giu .claude/dev/launcher.py` ⇒ `NGƯỜI_GIỮ 0`, rc=0 (10:47:06Z). Không còn phụ thuộc lease nào đang giữ write set lúc đo. Hai tệp vẫn phải đo lại lúc cấp lease (Q5 điều kiện 1, §11 mục 4); r11 đến r16 KHÔNG đo lại `ai-dang-giu`. (r11) Commit rút hạn `86b23c0` nay là tổ tiên của `origin/master` `fc852ff` (Merge PR #697). Số lease của r3 (người giữ 1, hạn 07:41Z): ô này của r9. |
| nền nghiệm thu | **(r10) DỜI sang `origin/master` `423b4ba14078701859b9e6ac101a68a3fc4ddef4`** (Merge PR #696, #668). Lý do, đo: `git -C <worktree> fetch -q origin master` rc=0 (10:45:10Z 30-09); `git ls-remote origin refs/heads/master` ⇒ `423b4ba…`; `git diff --quiet 89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=1**. Diff (`git diff --stat`): chỉ `launcher_test.py`, 2 dòng thêm, 1 dòng xoá, trong `t152_hook_cai_dat_va_khop_al_ver_ci` (hunk `@@ -5997,7 +5997,8 @@`, dòng đổi là dòng 6000 trên `89fc4fa`): assertion đếm `AL_VER` trong `ci.yml` đổi từ 4 chỗ sang 5, cộng một dòng chú thích. `launcher.py` giữ blob `561ff7a1840d65a6fc9953947f71cabe4947b3c9` (sha256 `808ce5b3…9fc0`); `launcher_test.py` đổi blob `abf7f6ca…` ⇒ `3f02fb94abece5aa331f68fc890367cab50ac7a4` (sha256 `882ac43f…97cc`, 8355 dòng). Mọi số nền đo lại trên `423b4ba` ở §8 (số ca, hậu tố, `DOT_BIEN`, dòng runner, ruff, suite, CI). Nền `89fc4fa` vẫn là nền của mọi số đo hành vi `launcher.py` trong tệp này, vì blob `launcher.py` không đổi. Lượt đo nền của r3 đến r9: ô này của r9. **(r11) Nền GIỮ `423b4ba`**, đo: `git ls-remote origin refs/heads/master` ⇒ `fc852fff7da37f1669569572b79571446e61c294` (15:31:19Z 30-09); fetch vào kho bare của rig r11 (không đụng ref của worktree): `423b4ba` là tổ tiên của `fc852ff` (rc=0), 29 commit giữa hai đầu, `git diff --quiet 423b4ba fc852ff -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0**, `git diff --stat 423b4ba fc852ff -- .claude .github` rỗng — write set và CI không đổi byte nào. **(r12) Nền GIỮ `423b4ba`**, đo: `git ls-remote origin refs/heads/master` ⇒ vẫn `fc852fff…c294` (22:33:02Z 30-09); trên đối tượng cục bộ của worktree (không fetch): `423b4ba` là tổ tiên của `fc852ff` (rc=0), `git diff --quiet 423b4ba fc852ff -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ rc=0, `git diff --stat 423b4ba fc852ff -- .claude .github` rỗng. **(r13) Nền GIỮ `423b4ba`**, đo: `git ls-remote origin refs/heads/master` ⇒ vẫn `fc852fff…c294` (00:46:55Z 01-10); trên đối tượng cục bộ của worktree (không fetch): `423b4ba` là tổ tiên của `fc852ff` (rc=0), 29 commit giữa hai đầu, `git diff --quiet 423b4ba fc852ff -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ rc=0, `git diff --stat 423b4ba fc852ff -- .claude .github` rỗng. **(r14) Nền GIỮ `423b4ba`**, đo: `git ls-remote origin refs/heads/master` ⇒ `20ec8d5d0e86cb7dc01f202c7596407a957e5961` (04:41:44Z 01-10; commit "Merge pull request #689 …"); trên đối tượng cục bộ của worktree (không fetch; ref `origin/master` cục bộ đã trỏ `20ec8d5`): `fc852ff` là tổ tiên của `20ec8d5` (rc=0, 22 commit), `423b4ba` là tổ tiên của `20ec8d5` (rc=0, 51 commit), `git diff --quiet fc852ff 20ec8d5 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ **rc=0**, cùng lệnh từ `423b4ba` ⇒ rc=0, `git diff --stat 423b4ba 20ec8d5 -- .claude .github` rỗng. `fc852ff..20ec8d5` đổi đúng hai tệp, cả hai ngoài write set: `ops/land/pr684-wp677-land-evidence.yaml` (mới, +256) và `ops/lease_publish_test.py` (+600 / −15, có hunk trong thân `t154` — B7, §8). **(r15) Nền GIỮ `423b4ba`, phiên soạn r15 KHÔNG đo lại** (không `ls-remote`, không `fetch`; r15 chỉ sửa câu chữ): lần đo cuối của phiên soạn là của r14 ngay trên; cross-review lượt 14 đo lại trên kho của sandbox review — `fc852ff` và `423b4ba` là tổ tiên của `20ec8d5`, write set không đổi, `.claude .github` rỗng, bốn tệp CI bằng nhau ở `423b4ba` và `20ec8d5` (VERDICT lượt 14, HƯỚNG 6; số của reviewer). **(r16) Nền GIỮ `423b4ba`, phiên soạn r16 KHÔNG đo lại** (không `ls-remote`, không `fetch`; r16 chỉ sửa câu chữ): lần đo cuối của phiên soạn vẫn là của r14; cross-review lượt 15 đo lại trên kho của sandbox review — `fc852ff` và `423b4ba` là tổ tiên của `20ec8d5` (rc=0; 22 và 51 commit), write set không đổi từ cả hai, `.claude .github` rỗng, `ci.yml` và `launcher-windows.yml` cùng sha256 ở `423b4ba` và `20ec8d5` (VERDICT lượt 15, HƯỚNG 7; số của reviewer). Nền tiếp nối (continuation base): khai riêng lúc cấp lease (protocol §3.2.1); đầu `origin/master` còn trôi thì đo lại lúc ấy, theo cùng luật dời nền. **(r21) Nền GIỮ `423b4ba`**, phiên soạn r21 đo trên đối tượng của một kho cục bộ (không `fetch`, không `ls-remote`): ref `origin/master` cục bộ trỏ `ab457c651eb4428705f0492163080b661c858b72`; `423b4ba` là tổ tiên của nó (rc=0; 150 commit); `git diff --quiet 423b4ba ab457c6 -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒ rc=0, blob `561ff7a1…`/`3f02fb94…` ở cả hai. Đầu `origin/master` trên GitHub lúc soạn r21: CHƯA ĐO. Ba mốc Git của generation 3 và chỗ lệch giữa lease g3 với sổ Mission: đoạn "Mỏ neo bằng chứng dùng lại", phần (5). |
| `spec_hash` | Xem **Công thức băm** ngay dưới. Giá trị **không** nằm trong tệp này. |

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit đã đóng
băng: `sha256sum ops/specs/launcher-con-song-esrch-r26.md`, không loại dòng nào. Giá trị được công
bố **ngoài** tệp: comment trên #685 và lease, kèm OID commit + đường dẫn. Khối closure dưới đây
nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau. Đổi bất kỳ byte nào
⇒ revision mới, băm mới, lease mới. Băm của r1 (`ee44238c…37d9`), r2 (`de9c553a…9ce4`), r3 (`7ef008f8…a895`),
r4 (`2c84a1bd…ae67`), r5 (`a0842320…7928`), r6 (`fadad3c7…3c99`), r7 (`3fc04fe5…5286`), r8 (`2ae6ee04…2aa3`),
r9 (`1a629c89…a3cf`), r10 (`e3ae8741…4bde16`), r11 (`830d5ce4…5604`), r12 (`fba80c32…e89fe2`), r13 (`1ef830ab…97b9`),
r14 (`8a8cb1c0…ef0d`), r15 (`f0e9d580…1b99`), r16 (`1d75b228…2971`), r17 (`36bb1214…48cbf`), r18 (`bfd490ac…ee68f`) và r19 (`40a14a6e…c604f`) KHÔNG còn dùng để cấp lease; r21 (`1edd6c75…9aef`) và r22 (`e9f9e056…3c5d`), hai bản soạn trước r23, cũng không dùng để cấp lease. r20 (`645d9a8b…ce64`) là băm mà lease g3 neo — đọc trên nhánh metadata `95f961e`: trong 136 tệp lease ở đó, g3 là tệp duy nhất mang băm r20, còn g1 mang r18, g2 và g2b mang r19, và cả ba khai `da_bi_thay_the`. (r24) r23 (`96387f83…e939`) là băm mà Mission r6, r7 và lease g4, g4b neo (ô `thay_the_cho`). (r25) r24 (`be3b416b…6fab`), bản soạn ngay trước r25, không dùng để cấp lease. (r26) r25 (`bc3d6f40…1b31`), bản soạn ngay trước r26, cũng không dùng để cấp lease. Lease không neo băm r26 thì không áp dụng r26: lease g3 làm theo r20, lease g4 và g4b làm theo r23. Băm r26 tính theo công thức này, giá trị nằm ngoài tệp như mọi revision; lease áp dụng r26 neo đúng băm ấy, kèm các điều kiện ở ô `revision`. Không revision nào tự cấp authority: authority chỉ đến từ quyết định chủ kho trên đúng băm, event Mission đọc lại khớp và lease.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2), điền tay theo **miễn trừ có
phạm vi** ở Mission Issue #686: chỉ `wp685`, hết hiệu lực ở lần đầu một policy canonical cho closure
xuất hiện trên nhánh mặc định.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null` — chưa có policy canonical; descriptor thay thế là miễn trừ ở #686 |
| `effective_write_set` | `.claude/dev/launcher.py` · `.claude/dev/launcher_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR thi hành, **tên context** (r11 đọc bằng REST: run `36696528580` — lượt `push` master của `423b4ba`, workflow `gate`/`.github/workflows/ci.yml`, 14 job; run `36737283472` — workflow `thu-hoi`/`ops-thu-hoi-admission.yml`, `pull_request_target`, PR #602): `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-registry (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`; hai job #668 thêm từ nền `423b4ba` — `gate-cong-cu-gop (ubuntu-latest)` và tám context của ma trận `gate-cong-cu`: `gate-cong-cu (ubuntu-latest, 0)`, `gate-cong-cu (ubuntu-latest, 1)`, `gate-cong-cu (ubuntu-latest, 2)`, `gate-cong-cu (ubuntu-latest, 3)`, `gate-cong-cu (ubuntu-latest, 4)`, `gate-cong-cu (ubuntu-latest, 5)`, `gate-cong-cu (ubuntu-latest, 6)`, `gate-cong-cu (ubuntu-latest, 7)`; và `thu-hoi` — các check này có thật và phải xanh (PR không nhãn chỉ có `ubuntu-latest`: job `chuan-bi`; run trên là lượt `push`, tên ở lượt PR đọc lại trên lượt chạy đầu của PR thi hành), nhưng **KHÔNG check nào trong số đó chạy `launcher_test.py`** (`gate-registry` chạy chín bộ thuộc `MOI`, không có `launcher_test.py`; xem §8). **Đỏ sẵn trên nền (r11 đo):** ở run `36696528580`, `gate-registry (ubuntu-latest)` (job `109832781748`) ĐỎ ở bước 11 `test registry (phạm vi + các bộ chưa được nối)` — log: `ops/nhanh_don_duoc_test.py` rc=-9 sau 4500,384 s, ngoài write set; nếu vẫn đỏ sẵn trên nền của PR thi hành thì ghi "đỏ sẵn, delta 0" kèm lượt nền (CLAUDE.md, Quy ước deploy mục 7), không sửa gì ngoài write set. Ngoài các check CI, **bắt buộc** bằng chứng cục bộ Linux B1–B6 và B8 neo exact candidate SHA, **chạy trên `python3.11` và `python3.12`** (B6; lệnh nguyên văn, giờ UTC, rc, dòng tổng), đính vào handoff và reviewer đọc trước merge; Codex review độc lập `cross_approved` với 0 P1/P2/P3 (r25: executor `claude` họ anthropic, reviewer `codex` họ openai — ô reviewer; r20 đến r23, khi executor là `codex`, vế này ghi `same_provider_approved`, và r24 giữ nguyên chữ ấy dù đã đổi executor) và human audit exact SHA `human_audited` |
| `land_obligations` | Chủ kho human audit trên exact SHA + ủy quyền merge (không tự merge/approve); đọc kết quả `launcher-windows.yml` ở lượt `push` lên master sau merge, cả job Windows lẫn job Ubuntu, và báo — kể cả dòng `DOT BIEN:` của bước `Tu dot bien` trên Windows: `DUOI SAN` (dưới sàn 70 % của `--dot-bien`) là ĐỎ của packet này, không phải đỏ sẵn (§7 B4, r7); ghi sổ verdict + HINT vào `ops/reviews/` kèm receipt và mục README; thu hồi lease sau land; đóng #685 |

**Descriptor nguồn closure** = `{mission_issue: 686, object_id: 5628902742}`. Neo bằng object ID + số Issue, vì thân Issue sửa được. (r11) Đường
đọc MCP chuẩn hoá thực thể HTML trong thân issue (CLAUDE.md), nhưng REST thì không: r11 đọc được `id` của #686 =
`5628902742` và băm thân `2af24e28…d9de` (§10) — ghi để đối chiếu, không thay neo.

**Lease chép gì, AI so (r21, cross-review lớp `lease-sao-closure-khong-do-duoc`; r22 sửa câu về `ops/lease_publish.py`; đo trên `ab457c6` và trên nhánh metadata `95f961e` của lease g3):** trong mã cổng (trừ `ops/reviews/` và các tệp `_test.py`), `ops/lease_publish.py` đọc nhiều trường lease khác (ví dụ `provider`, `executor`, `reviewer`, `transport`, `lease_expires_at_utc`, `thay_the_cho`, `da_bi_thay_the`, `prompt_path`, `prompt_sha256_required`; không liệt kê hết — phiên soạn r22 đếm bằng AST 84 khoá chuỗi hằng mà tệp đọc qua `.get()` hay chỉ số, không riêng khoá lease) nhưng trong các trường closure chỉ đọc `write_set` (để tính lớp review, và để `ai-dang-giu` biết lease giữ đường nào) và `effective_review_class` (cùng `review_class`); KHÔNG tệp cổng nào đọc `spec_hash`, `spec_sha256_required`, `mission_issue`, `change_policy_sha`, `write_set_hash`, `start_from_sha`, `required_checks`, `land_obligations` hay `object_id` (`grep -rln` từng khoá: 0 tệp; `effective_write_set` chỉ có ở `ops/chatgpt_review/build_bundle.py`). `BAT_BUOC` của `ops/lease_publish.py` là danh sách năm trường BẮT BUỘC, không phải danh sách trường được phép. Vậy phép so là việc của EXECUTOR, ngay sau khi đọc lease và trước khi ghi mã: với mỗi trường closure mà lease CÓ — `spec_hash` và `spec_sha256_required` (bằng sha256 của tệp này theo công thức ở trên), `effective_write_set` hay `write_set` (đúng hai đường exact của ô closure), `effective_review_class`, `change_policy_sha`, `mission_issue` — giá trị trong lease phải BẰNG giá trị ở đây; lệch ⇒ **DỪNG** và báo điều phối. `required_checks`, `land_obligations` và `object_id`: 0/136 tệp lease trên `95f961e` (0/132 trên `ab457c6`) mang các khoá ấy, nên không có bản chép để so; chúng bị ràng buộc qua `spec_hash` (tệp này chứa chúng), và lease vắng chúng KHÔNG phải lệch. `write_set_hash`: không đặc tả hay cổng nào định công thức; trên `95f961e`, 45 lease mang trường này — 41 theo "sha256 các đường đã sắp xếp, nối bằng LF, có LF cuối", 4 (g1, g2, g2b, g3 của wp685) theo sha256 của `json.dumps` danh sách đã sắp xếp. Hai đường của tệp này cho `0a2ec511e97d0e14ff9be00f73e539bf638d78639d8eda25fb52ebf46e1c9f65` theo cách thứ nhất và `ae3e61d02ad972d642942871d4d83cb48b3d4ba87244fdfe1cc18333bc6db053` theo cách thứ hai — đúng giá trị lease g3 mang. Lease cấp theo r26 (nếu có) khai giá trị theo cách thứ nhất; r26 không xét lại lease g3, g4, g4b. (r24) Dữ kiện, đo trên commit `26d4711`: lease g4 và g4b cũng mang `ae3e61d0…3053`, tức cách thứ hai, trái câu tương ứng của r23 — ghi để lease cấp theo r26 không chép theo chúng.

**Hiệu lực r26.** Revision 26 được soạn làm đầu vào cho quyết định MCR-686-08. Hiệu lực được xác định bởi quyết định chủ kho
trên SHA-256 toàn tệp, event Mission đọc lại khớp và lease neo đúng băm ấy. Trước khi đủ các điều kiện đó, revision này
không cấp quyền thi công; sau khi đủ, chỉ run/generation của lease mới áp dụng revision này. Lease g3 được cấp theo r20,
lease g4 và g4b theo r23; hồ sơ attempt 3/3 tại event #686 `6031263612` và mọi hồ sơ của g4, g4b không bị revision này áp
dụng hồi tố. Không câu nào của r26 tự cấp quyền, đổi lease cũ, hay đổi việc mà một attempt đã làm theo revision cũ. Thiếu
một trong ba điều kiện trên ⇒ r26 chỉ là hồ sơ và r23 vẫn là revision mà Mission r7 neo. Đoạn "Hiệu lực r20" ngay dưới
giữ nguyên chữ của r20, trừ câu về phạm vi đo tiếp và dùng lại bằng chứng.

**Hiệu lực r20 và impact analysis.** Chủ kho duyệt reroute generation 3 tại
[#686 comment 6030761544](https://github.com/ducthangho/tra-luat/issues/686#issuecomment-6030761544)
sau đề xuất chi tiết ở comment `6030719075`. Mission revision 5 và MCR-686-05 chỉ thay
điều phối generation/lease; objective, acceptance B1–B8, two-path effective write set,
provider, review class, required checks, land obligations và canonical base của r19 giữ nguyên.
Spec r19 là lịch sử generation 2; các câu bên dưới kể `generation 2`, `Mission r4`,
hoặc đo ở r19 là lịch sử, không cấp authority cho generation 3. Lease g2b phải
supersede; Mission r5/event/projection và lease g3 phải đọc lại khớp trước khi
executor tiếp tục. 2/3 attempt đã dùng, cùng lớp thiếu E đã lặp hai lần;
generation mới không xoá lịch sử này. Phạm vi đo tiếp và điều kiện dùng lại bằng chứng của các attempt trước:
r21 thay câu của r20 về chỗ này bằng đoạn **Mỏ neo bằng chứng dùng lại** ngay dưới — câu r20 nêu một con số và
các ký hiệu viết tắt không neo vào băm nào (cross-review lớp `bang-chung-tai-dung-khong-neo`).
E/D phải có artifact bất biến và readback SHA-256 trước approval; exact-head gates
còn trống phải có command/rc/positive evidence. Same-provider review độc lập
không thay human audit exact-SHA của Packet sensitive; một code push sau khi đủ
nghiệm thu và 0 P1/P2/P3, CI chỉ ở merge readiness.

**Mỏ neo bằng chứng dùng lại (r21, cross-review lớp `bang-chung-tai-dung-khong-neo`; r22 chép nguyên văn câu nền).** Luật
nền là PROTOCOL §10 (`docs/PROTOCOL_DA_PHIEN.md` của `ab457c6`), nguyên văn: *"Evidence chỉ được reuse khi tested
SHA/tree, policy/catalog, runner, OS/runtime matrix và artifact hash (nếu có) khớp chính xác; head hoặc một identity
đổi thì chạy lại."* Đoạn này biến các đại lượng ấy thành phép đo cho packet này; policy/catalog ở đây là định nghĩa
phép đo của B5 (A/W, D, (E)) — bằng nhau từng byte từ r17 tới r22 (đoạn kiểm), nên một revision đổi B5 là một
identity đổi. Chỗ nào không neo được thì ĐO LẠI — không có ngoại lệ kiểu "đã đo ở attempt trước".

**(1) Ký hiệu.** "E118" = 83 tên `DS-E-HANG-MUC` + 35 tên `DS-E-KHAC` của (E) mục 6 (`DS-E-C3` thêm khi ứng viên tách
trạng thái trong hàm trợ giúp). "D65" = 65 control của D mục 4 (17 nhãn, 48 tiểu nhãn); "D6" = sáu phép đảo thứ tự liệt
kê tại đó. "W0 strict" = tiêu chí W0 của bảng A/W ở B5, áp qua (E) mục 2: sống sót, bộ đếm seam ≥ 1; hạng
`CHƯA CÓ CHỐT NGƯỢC` không đạt. Tập áp dụng = biến thể (E) có đích ở `t156_...`/`t157_...` thuộc các hướng
thoát/sai/bắt/bọc/đếm/cú pháp/dạng đọc của (E) mục 2 — tức TRỪ biến thể có đích ca B8 (chỉ A1); biến thể hướng thay
thế, tám đối chứng của `B2-parse`, (j1) và hai phép giả gọi lại hàm trợ giúp (W0 của bốn nhóm này phải đỏ VÔ CAN, không
phải sống sót); và hai đối chứng sống (đo bằng SONG và nhân chứng dương, (E) mục 5). Số phần tử của tập là thuộc tính của BẢNG (E) của
ứng viên — một tên có thể ứng với nhiều bản, và cột đích đo bằng A1 — nên không suy được từ đặc tả. Con số 102 (41 đã
đo trên 3.11, 61 còn thiếu) của review g2b (#685 comment `6030695601`) là số của bảng `48293768…` ở phần (3), không
phải tham số của đặc tả. Danh sách 61 tên mà điều phối nêu ở #686 comment `6030719075` chỉ có ĐƯỜNG DẪN trên máy
executor; các nguồn phiên soạn r21 đọc được (đặc tả, review g2b, sổ Mission #686, lease g3) không có băm nào của nó ⇒
nó KHÔNG xác định phạm vi. Phạm vi W0 strict phải đo = tập áp dụng trừ các dòng dùng lại đủ bốn mỏ neo ở (2) (phạm
vi đo lại của các phép khác: bảng ở (3)); handoff nộp cả hai bảng và reviewer tính lại phép trừ bằng máy.

**(2) Bốn mỏ neo.** Một dòng, log hay tập lệnh cũ chỉ được dùng lại khi đủ cả bốn và đo thấy BẰNG nhau: (i) **bytes** —
tệp đọc lại được từ kênh nộp ở (4), và sha256 của bytes đọc lại BẰNG một băm đã công bố TRƯỚC run hiện tại tại một
comment có `id`, trực tiếp hoặc qua một manifest mà chính băm của manifest đã được công bố như vậy; (ii) **ứng viên** —
`git rev-parse HEAD` và tree ghi trong log bằng exact candidate và tree của lượt review mới; (iii) **runtime** — dòng
`python3.1x -V` trong log bằng dòng ấy của môi trường đang dùng; (iv) **môi trường** — bộ năm của ô `environment` bằng
nhau. Một mỏ neo lệch hay vắng ⇒ dòng ấy KHÔNG dùng lại, đo lại.

**(3) Hiện trạng bằng chứng của attempt 2** (ứng viên `4c404f9a50b24730f823b5c22376548c6ee67e4f`, tree
`1d431ed721ee62f5de1eba1e6da387fcc29bd891`), đo trên nguồn phiên soạn r21 đọc được (readback #686 tới comment
`6031267262`, 2026-10-07T05:00:15Z; phiên soạn r22 đọc cùng các nguồn ấy) — không phải trên tệp của executor:

| bằng chứng | mỏ neo có trong nguồn đọc được | mỏ neo thiếu | hệ quả |
|---|---|---|---|
| bảng (E): W0 trên 3.11 (41 dòng), W0 trên 3.12, hành vi E118 | (i) băm bảng `4829376821d4070c3edc594083bff50634f16ee8f95b7c17fdad3d0584675b06` và (ii) ứng viên, tree — cùng ở #685 comment `6030695601` | bytes chưa nằm ở commit hay artifact nào (cùng comment ghi chúng chỉ là tệp scratch cục bộ); (iii) số vá Python và (iv) môi trường: không có ở nguồn nào đọc được | dùng lại chỉ khi executor nộp đúng bảng ấy lên kênh nộp, sha256 bytes đọc lại BẰNG `48293768…`, và log của từng dòng mang (iii), (iv) đạt; không thì đo lại cả ba thứ của hàng này (cùng thiếu (iii), (iv)) — tức cả bảng (E) theo (E) mục 2, gồm W0 strict của tập áp dụng, trên MỖI bản Python |
| tập lệnh (A/W, D, (E), B8, `chot_tinh_r12.py`) của attempt 2 | không có băm riêng ở nguồn đọc được (review g2b nêu băm bảng, manifest và handoff, không nêu băm tập lệnh), trừ `chot_tinh_r12.py` mà sha256 cố định ở khối B2; chỉ neo được qua manifest nếu nó có liệt kê | bytes (tệp ở máy executor) | dòng đo bằng một tập lệnh chưa neo (i) KHÔNG dùng lại — PROTOCOL §10 tính runner là một identity |
| manifest | băm `33ea4383ceb482d63287dde70a23389f9147d3fa9eb976d7c47a58b722bea62a`, ở cùng comment và ở các event của sổ Mission | cùng comment đòi tính LẠI manifest sau log cuối, tức manifest ấy không phủ log cuối | chỉ neo (i) cho tệp nó có liệt kê; tệp sinh sau nó không có mỏ neo (i) |
| D (D65, D6), `--dot-bien`, suite, gate exact-head đã chạy | không có băm riêng ở nguồn đọc được; chỉ neo được qua manifest trên nếu nó có liệt kê | bytes, (iii), (iv) | đo lại, trừ khi đi được đường manifest và đủ (ii), (iii), (iv) |
| handoff g2b | băm `ffb9609e8cb496bfc749b7f6efc9db700eb2386107625d93594e847a462448a4` | bytes (đường dẫn trên máy executor) | không phải bằng chứng nghiệm thu; chỉ là mỏ neo (i) cho tệp nó liệt kê kèm băm |

Về `--dot-bien`: review g2b ghi 230/230 ở 3.11 và 3.12, kèm một ca POSIX không đo được mỗi lượt, và ghi rằng ca ấy
không phải đạt. Nói thẳng: với nguồn đọc được lúc soạn r21, KHÔNG bằng chứng nào của attempt 2 đủ bốn mỏ neo — thiếu
chung bytes, (iii) và (iv). Mặc định là ĐO LẠI; chỉ dòng nào executor neo đủ mới được bỏ khỏi phép đo. Tệp của
executor (bảng, log, manifest, handoff, danh sách 61) với phiên soạn r21: KHÔNG ĐO ĐƯỢC (lý do 3) — chỉ có ở máy
executor.

**(4) Kênh nộp E/D — đo phía GHI trước.** (E) mục 3 vẫn đòi tệp trong một commit (nhánh bằng chứng riêng, ngoài write
set) hoặc artifact; các nguồn đọc được (readback #686 tới 2026-10-07T05:00:15Z) không ghi lần đo phía ghi nào, và
attempt 2 hụt đúng bước này (`ED-immutable-artifact-missing`, #686 comment `6030711659`). PROTOCOL §4, nguyên văn:
*"Executor lease chỉ cấp quyền thi công trong write set/generation và hạn của nó."* — nên TÊN ref bằng
chứng (hay kênh artifact) và quyền đẩy lên nó phải do điều phối hoặc chủ kho nêu ở một nguồn có `id`; đặc tả không tự
nêu (§11 mục 5). Đầu mỗi run, TRƯỚC khi đo nặng: đẩy một tệp thăm dò nhỏ lên đúng ref ấy, rồi đo ở PHÍA ĐẾN —
`git ls-remote --exit-code origin <ref>` phải rc=0 và in đúng OID vừa đẩy; trong một kho RỖNG vừa tạo, `git fetch <remote> <ref>`
rồi `git show <OID>:<đường dẫn> | sha256sum` phải bằng sha256 bản gửi. Đọc lại trong CHÍNH kho vừa commit, hay trong kho/worktree lấy từ nó (cross-review trên r21 đo, phiên soạn r22 đo lại với git 2.43.0: `git clone` hay `git worktree` của kho ghi vẫn `git show` được commit CHƯA đẩy, rc=0, đúng băm), KHÔNG phải
phép đo: phiên soạn r21 dựng một kho bare cục bộ làm phía đến — chưa đẩy mà `git show <OID>:probe.txt` ở kho ghi vẫn
rc=0 và đúng băm; `git ls-remote` không cờ trả rc=0 với đầu ra rỗng khi ref không có (thêm `--exit-code` ⇒ rc=2); kho
rỗng `fetch` ⇒ rc=128. Sau khi đẩy: `ls-remote` in đúng OID, kho rỗng `fetch` rc=0, `show` ra đúng băm. Chỉ hai phép
đo phía đến phân biệt được đã đẩy với chưa đẩy; vế ĐỎ r9 của B6 ("tệp nộp không đọc lại được từ commit hay artifact đã khai") và (E) mục 3 ("reviewer đọc lại tệp từ chính commit hay artifact ấy") — cùng D mục 6, nơi nộp "cùng kênh" với (E) mục 3 — đọc theo nghĩa phía đến ấy: reviewer `fetch` vào kho rỗng hoặc tải artifact theo ID, không đọc ở kho hay worktree của executor. Artifact: tải về theo ID vào thư mục rỗng rồi so sha256. Không ghi
được, hay phía đến không ra đúng ⇒ DỪNG, báo điều phối, không chạy đo nặng. Phía ghi lên GitHub với phiên soạn r21:
KHÔNG ĐO ĐƯỢC (lý do 5) — chỉ thị cấm đẩy.

**(5) Ba mốc Git (PROTOCOL §3.2.1).** Handoff kèm bảng ba mốc: immutable acceptance baseline = `423b4ba14078701859b9e6ac101a68a3fc4ddef4`
(ô nền nghiệm thu); continuation base = *"OID được phép bắt đầu run/generation tiếp theo, kèm authority cho việc
tiếp tục"* (PROTOCOL §3.2.1, nguyên văn), authority ấy có `id` — và OID mà run THẬT SỰ bắt đầu phải bằng nó; reviewed
candidate = *"exact head và tree thật sự đưa ra review"* (cùng chỗ). Lệch đo được — BA giá trị cho cùng một mốc: tệp lease g3 khai `start_from_sha` =
`base_sha` = `ab457c651eb4…`; event cấp lease g3 (#686 comment `6031241730`, 04:57:49Z) còn mang `attempt_source_head` =
`c9f2469efe8a…`, giá trị có từ event bắt đầu attempt 2 (`6029724105`, 02:37:37Z); event bắt đầu attempt 3
(`6031263612`, 04:59:54Z) ghi `attempt_source_head` = `4c404f9a…`, bằng `prior_generation_candidate_head` của cùng event,
với `mcr_decision_url` trỏ quyết định chủ kho `6030965299`. Không cổng nào đọc `start_from_sha` (đo ở đoạn descriptor
closure), và PROTOCOL §3.2.1 nói *"Các tên trên mô tả nghĩa vụ evidence, không tự thêm field vào schema."* — nên
theo hồ sơ tới 2026-10-07T05:00:15Z, nền tiếp nối của attempt 3 là OID ở event bắt đầu attempt (`4c404f9a…`; nguồn
authority: quyết định chủ kho `6030761544` duyệt đề xuất `6030719075`, nơi candidate local ghi là đầu vào kế thừa) —
đó là mô tả hồ sơ, không là nghĩa vụ mới của attempt 3. Lease cấp theo r26 (nếu có) khai `start_from_sha` bằng nền
tiếp nối mà authority của chính lease ấy cho phép, và handoff của nó khai đúng OID ấy cùng nguồn; r26 không định trước OID ấy. (r24) Executor cloud không với tới tệp chỉ có ở máy executor cũ: `4c404f9a…` không có trong kho mà phiên soạn r24 đọc (`git cat-file -t` báo lỗi, sau khi đã fetch mọi nhánh), nên mọi dòng bằng chứng neo vào nó hay vào tệp ở máy ấy được ĐO LẠI, không dùng lại. Ba OID `4c404f9a…`, `1d431ed7…`, `c9f2469e…`
không có trong kho cục bộ của phiên soạn r21 (`git cat-file -t` rc=128 cả ba); quan hệ tổ tiên của `4c404f9a…` với
`ab457c6`: KHÔNG ĐO ĐƯỢC (lý do 3) — sổ Mission ghi `code_pushed: false`, commit chỉ có ở máy executor.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm.
**Ba trạng thái:** có · không · `KHÔNG ĐO ĐƯỢC` — nhãn thứ ba chỉ đi với MỘT lý do trong danh sách ĐÓNG ở §10 (r12);
việc làm được mà chưa làm là CHƯA ĐO.

**Thay đổi so với r25** (mỗi dòng một lớp của VERDICT cross-review lượt 2 trên r25 — sha256 `bd84b8a1…6641`, mức
`advisory_review`; slug là tên lớp trong bảng lớp của VERDICT). Phép dựng: bytes của r25 ở commit `0aba473`, cùng
MCR-686-08 ở `6c6e3d8` và hai bản nháp lease/prompt g5, áp `HINT.patch` (sha256 `683f8ad6…ad15`, 4 tệp, 8 hunk) bằng
`patch -p0 --fuzz=0` trên một bản sao ngoài worktree (dry-run rc=0, áp rc=0, 0 tệp `.orig`/`.rej`; phần đặc tả sau áp
có sha256 `6057bf22…a86b`, trùng số VERDICT ghi), `cp` thành tệp r26, rồi sửa tay đúng các chỗ ở cột "HINT lệch phép
đo" và hàng cuối. Cả ba hunk đặc tả của HINT đều áp, kể cả hunk sửa hàng `phien-dieu-phoi-kiem-executor-chua-khai` của
bảng "Thay đổi so với r24": đó là đính chính trong khối lịch sử (nhãn mục của câu PROTOCOL dòng 598–599 thành §7 ở hai chỗ), ngoài ra bảng ấy, đoạn "Kiểm lúc
soạn r25" và mọi khối lịch sử dưới chúng giữ nguyên chữ của r25, và mọi số đếm trong đó là của tệp r25.

| slug lớp | hạng | chỗ sửa trong r26 | đo lại của phiên soạn r26 | HINT lệch phép đo |
|---|---|---|---|---|
| `phien-dieu-phoi-kiem-executor-chua-khai` | P3 | ô reviewer: câu vai trò trích đúng mục PROTOCOL của câu ấy (§7), bỏ "soạn prompt" khỏi việc cấm, thêm "không soạn assignment riêng cho reviewer ấy" và câu `copyable_prompt` theo mẫu D0; bảng "Thay đổi so với r24", hàng P2: nhãn mục của câu dòng 597–598 thành §7 ở hai chỗ (đính chính) | PROTOCOL ở `6c6e3d8` (sha256 `8d65413c…997f`): câu *"Executor không tự tạo review có thẩm quyền…"* ở dòng 598–599, dưới `## 7.` (dòng 424; `## 4.` ở dòng 232, `## 8.` ở dòng 602); dòng 505–508 bắt mỗi phiên điền `copyable_prompt` theo `docs/prompts/MANUAL_SUCCESSOR_HANDOFF_D0.md`, mẫu có mục "Prompt Reviewer có thể sao chép" ở dòng 56 | HINT viết câu mới không nhãn; r26 gắn `(r25; r26 sửa)` cho câu vai trò và `(r26)` cho câu `copyable_prompt`. HINT ghi rằng khi giữ bảng "Thay đổi so với r24" làm lịch sử thì không áp hunk sửa hàng P2 của bảng ấy; r26 vẫn áp, để mọi chỗ trích câu dòng 598–599 đều ghi §7, và ghi đính chính ở đây |
| `mo-ta-thay-doi-hep-hon-diff` | P3 | ô `thay_the_cho`, mục (r25): câu tả phép dựng r25 nói thêm phần sửa tay và hai hunk HINT lượt 1 không áp | 17 hunk giữa r24 + phần đặc tả của HINT lượt 1 (sha256 `ec8b71c3…01d7`) và r25 | mục (r26) mới của ô ấy tả r26 bằng bảng này, không bằng phương trình |
| (không phải lớp) đầu tệp và câu tự nhắc | — | tiêu đề; `revision`; `thay_the_cho` (thêm r25 ở đầu); mục (r26) của `nguon_cap_viec`; công thức băm (tên tệp; r25 không dùng cấp lease; câu lease neo băm); đoạn "Hiệu lực r26" thay đoạn "Hiệu lực r25"; câu lease của revision hiện hành ở đoạn "Lease chép gì" và ở phần (5); §4 trỏ tệp r26; §11 mục 4 và mục 5 trỏ băm r26; bảng này và đoạn kiểm r26 | — | HINT viết trên r25 tại chỗ nên các câu tự nhắc vẫn nêu r25 |

**Kiểm lúc soạn r26** (phiên soạn r26, không phải phép đo trên launcher hay ứng viên; mọi số đếm dưới đây đo trên chính
tệp r26 cuối cùng, trong worktree có HEAD `6c6e3d8`): r25 khớp sha256 đầy đủ ghi ở ô `thay_the_cho` và blob
`c479b6f7…`; `VERDICT.md` và `HINT.patch` khớp mục (r26) của `nguon_cap_viec`. `diff -U0` r25 → r26: 15 hunk;
`diff -U0` r23 → r26: 15 hunk; mọi dòng đổi nằm ở phần đầu tệp (trước §1), ở một dòng của §4 và ở §11 mục 4, mục 5;
từ §1 tới hết §10, mọi dòng khác bằng r25 và r23. Sáu khối có rào của r26, trích bằng máy, BẰNG sáu khối của r25 từng
byte. `kiem_nhan_r12.py` (bản vừa trích) trên chính tệp r26: 47 nhãn, 0 sai dạng, rc=0 ở `python3.11`,
`python3.12`, `python3.13`. 9 bảng ở phần đầu tệp (trước §1): mỗi hàng đúng số cột của bảng mình. Tên tệp r26 có ở
đúng 2 dòng (công thức băm, §4). 0 dấu chéo ngược, 0 CR, 0 dấu bỏ-qua-CI. Băm và số dòng của chính tệp r26 không ghi ở
đây (công thức băm). Mọi chỗ trích câu *"Executor không tự tạo review có thẩm quyền"* đều ghi §7.

**Thay đổi so với r24** (mỗi dòng một lớp của VERDICT cross-review lượt 1 trên r24 — sha256 `67a89d25…0224`, mức
`advisory_review`; slug là tên lớp trong bảng lớp của VERDICT). r25 = bytes của r24 ở commit `0c91271` + `HINT.patch`
(sha256 `0f90fc6f…1eb4`) áp bằng `patch -p0 --fuzz=0` trên một bản sao ngoài worktree (dry-run rc=0, áp rc=0, 0 tệp
`.orig`/`.rej`; bản sau áp có sha256 `ec8b71c3…01d7`, trùng số VERDICT ghi), `cp` thành tệp r25, rồi sửa tay đúng các
chỗ ở cột "HINT lệch phép đo" và hàng cuối. Bảng "Thay đổi so với r23" và đoạn "Kiểm lúc soạn r24" ngay dưới đoạn kiểm
r25 giữ nguyên chữ của r24 (HINT có sửa hai khối ấy; r25 trả chúng về bytes của r24), làm lịch sử: mọi số đếm và mọi chỗ
nói "tệp", "phần đầu tệp" trong hai khối ấy là của tệp r24, không phải tệp r25.

| slug lớp | hạng | chỗ sửa trong r25 | đo lại của phiên soạn r25 | HINT lệch phép đo |
|---|---|---|---|---|
| `closure-con-doi-same-provider` | P1 | ô closure `required_checks`: vế mức review thành Codex `cross_approved` + `human_audited`, chữ `same_provider_approved` ghi là của r20 đến r24; ô `revision`, ô `thay_the_cho` nói theo | `grep -c same_provider` trên tệp r24: 3 dòng; PROTOCOL §8 mục 1 và mục 3 (tệp ở `fe68876`, dòng 606 và 609): hai nhãn định nghĩa theo họ model, dòng 696 chỉ nói một chiều | HINT gắn nhãn `(r24:` cho chú thích lịch sử ở closure và ghi "r20 đến r23"; r25 đổi thành `(r25:` và thêm r24, vì tệp r24 vẫn mang chữ `same_provider_approved` ở ô ấy |
| `phien-dieu-phoi-kiem-executor-chua-khai` | P2 | mục (r24) của `nguon_cap_viec`: cùng PHIÊN, không chỉ cùng họ; ô reviewer: câu vai trò (PROTOCOL §1 mục 8, §7) | trailer `Claude-Session` của `0c91271`, `fe68876`, `26d4711`: cả ba trỏ cùng một phiên; PROTOCOL dòng 39 (§1 mục 8) và dòng 597–598 (§7) | HINT gắn nhãn `(r24)` cho câu vai trò ở ô reviewer; r25 đổi thành `(r25)`. Câu ở mục (r24) của `nguon_cap_viec` giữ nhãn ấy vì nó nói về phiên soạn r24 |
| `tu-vung-bien-nhan-chua-theo-cross-approved` | P3 | ô reviewer: vế bằng chứng họ model trong câu `cross_approved`; câu về trường biên nhận `cross_approved` | CHƯA ĐO lại: dùng phép đo M5 của VERDICT trên `ops/bien_nhan_v2.py` (sha256 `38cda51c…`) | HINT gắn nhãn `(r24)` cho câu biên nhận; r25 đổi thành `(r25)` |
| `mo-ta-thay-doi-hep-hon-diff` | P3 | ô `revision`: câu tóm tắt nói hợp của hai bảng thay đổi | `diff -U0` r23 → r24: 14 hunk; `diff` Mission r7 → r8: khoá `effort: medium` của wp685 bị bỏ (MCR-686-08 nay nhắc) | HINT sửa câu tóm tắt và cả bảng "Thay đổi so với r23", đoạn "Kiểm lúc soạn r24" ngay trong r24 (một ô của bảng; số hunk 14 → 15, số chỉ đúng cho bản r24 đã vá); r25 viết lại câu tóm tắt theo hai bảng và trả hai khối ấy về bytes của r24 |
| `tran-luot-review-codex-khong-can-cu` | P3 | không sửa tệp này (HINT không chạm đặc tả); MCR-686-08 đưa `review_rounds_limit` ra cho chủ kho xác nhận, không thì lease dùng 2 | `rg review_rounds -g '*.py'` trừ `ops/leases/`: 0 tệp; PROTOCOL dòng 695 và 713 | — |
| (không phải lớp) đầu tệp và câu tự nhắc | — | tiêu đề; `revision`; `thay_the_cho` (thêm r24 ở đầu); mục (r25) của `nguon_cap_viec`; công thức băm (tên tệp; r24 không dùng cấp lease; câu lease neo băm); đoạn "Hiệu lực r25" thay đoạn "Hiệu lực r24"; câu lease của revision hiện hành ở đoạn "Lease chép gì" và ở phần (5); §4 trỏ tệp r25; §11 mục 4 và mục 5 trỏ băm r25; bảng này và đoạn kiểm r25 | — | HINT viết trên r24 nên các câu tự nhắc vẫn nêu r24 |

**Kiểm lúc soạn r25** (phiên soạn r25, không phải phép đo trên launcher hay ứng viên; mọi số đếm dưới đây đo trên chính
tệp r25 cuối cùng, trong worktree có HEAD `fe68876`): r24 khớp sha256 đầy đủ ghi ở ô `thay_the_cho` và blob
`14203156…`; `VERDICT.md` và `HINT.patch` khớp mục (r25) của `nguon_cap_viec`. `diff -U0` r24 → r25: 15 hunk;
`diff -U0` r23 → r25: 15 hunk; mọi dòng đổi nằm ở phần đầu tệp (trước §1), ở một dòng của §4 và ở §11 mục 4, mục 5;
từ §1 tới hết §10, mọi dòng khác bằng r24 và r23. Sáu khối có rào của r25, trích bằng máy, BẰNG sáu khối của r24 từng
byte. `kiem_nhan_r12.py` (bản vừa trích) trên chính tệp r25: 47 nhãn, 0 sai dạng, rc=0 ở `python3.11`,
`python3.12`, `python3.13`. Tám bảng ở phần đầu tệp (trước §1): mỗi hàng đúng số cột của bảng mình. Tên tệp r25 có ở
đúng 2 dòng (công thức băm, §4). 0 dấu chéo ngược, 0 CR, 0 dấu bỏ-qua-CI. Băm và số dòng của chính tệp r25 không ghi ở
đây (công thức băm).

**Thay đổi so với r23** (một dòng; nguồn: quyết định chủ kho ở ô `nguon_cap_viec`, mục (r24)). r24 = bytes của r23 ở commit
`26d4711` rồi sửa đúng các câu ở cột giữa. Bảng "Thay đổi so với r22" và đoạn "Kiểm lúc soạn r23" ngay dưới giữ nguyên
chữ của r23, làm lịch sử: mọi số đếm và mọi chỗ nói "tệp", "phần đầu tệp" trong các khối ấy là của tệp r23 hay r22.

| nguồn | chỗ sửa trong r24 | giữ nguyên chữ của r23 |
|---|---|---|
| quyết định chủ kho đổi executor (ô `nguon_cap_viec`, mục (r24)) | tiêu đề; ô `revision`; ô `thay_the_cho` (thêm r23 ở đầu); công thức băm (tên tệp; băm r23 và lease neo nó; câu lease neo băm); thêm mục (r24) của `nguon_cap_viec`; ô `executor` (viết lại, r20 đến r23 thành lịch sử); ô `environment` (câu mở đầu, và một ghi chú (r24) sau câu về container r21); ô reviewer (mức assurance, câu về review cũ); đoạn "Hiệu lực r24" thay đoạn "Hiệu lực r23"; câu lease của revision hiện hành ở đoạn "Lease chép gì" (kèm dữ kiện `write_set_hash` của g4, g4b) và ở phần (5) (kèm câu về candidate ở máy cũ); §4 trỏ tệp r24; §11 mục 4 và mục 5 trỏ băm r24; bảng này và đoạn kiểm r24 | objective, write set, risk/review class, closure (`required_checks`, `land_obligations`), B1–B8, tiêu chí máy kiểm (a)–(d) và dạng khối của ô `environment`, từ vựng biên nhận của ô reviewer, ba khối mã nhúng, §1–§10 trừ một câu của §4 |

**Kiểm lúc soạn r24** (phiên soạn r24, không phải phép đo trên launcher hay ứng viên; mọi số đếm dưới đây đo trên chính
tệp r24 cuối cùng, trong worktree dựng từ `26d4711`): r23 khớp sha256 đầy đủ ghi ở ô `thay_the_cho` và blob
`2ebcd7c2…`; trên `26d4711` có tệp r18, r19, r20, r23, và tám chữ số đầu băm của cả bốn khớp số ghi ở công thức băm.
`diff -U0` r23 → r24: 14 hunk; mọi dòng đổi nằm ở phần đầu tệp (trước §1), ở một dòng của §4 và ở §11 mục 4, mục 5; từ §1
tới hết §10, mọi dòng khác bằng r23. Sáu khối có rào của r24, trích bằng máy, BẰNG sáu khối của r23 từng byte; ba khối mã
nhúng: `chot_tinh_r12.py` 412 dòng `add42b31…`, khối B8 353 dòng `60ee8d5f…`, `kiem_nhan_r12.py` 19 dòng `13f7728d…`.
`kiem_nhan_r12.py` (bản vừa trích) trên chính tệp r24: 47 nhãn, 0 sai dạng, rc=0 ở `python3.11`, `python3.12`,
`python3.13` — bằng r23. Các bảng ở phần đầu tệp (trước §1): mỗi hàng đúng số cột của
bảng mình. Tên tệp r24 có ở đúng 2 dòng (công thức băm, §4). 0 dấu chéo ngược, 0 CR, 0 dấu bỏ-qua-CI. Băm và số dòng
của chính tệp r24 không ghi ở đây (công thức băm).

**Thay đổi so với r22** (một dòng; nguồn: mục 7 — O4 — của VERDICT cross-review Codex trên r22, sha256 `1ccc428f…2543`;
O4 là khuyến nghị biên tập trước đóng băng, không phải finding: VERDICT ấy ghi 0 P1 / 0 P2 / 0 P3). r23 = bytes của r22
ở commit `8b026b1` rồi sửa đúng các câu ở cột giữa. Bảng "Thay đổi so với r21" và đoạn "Kiểm lúc soạn r22" ngay dưới
đoạn kiểm r23 giữ nguyên chữ của r22, làm lịch sử: mọi số đếm và mọi chỗ nói "tệp", "phần đầu tệp" trong hai khối ấy là
của tệp r22, không phải tệp r23.

| nguồn | chỗ sửa trong r23 | giữ nguyên chữ của r22 |
|---|---|---|
| O4, VERDICT Codex trên r22 (sha256 `1ccc428f…2543`) | câu tự mô tả trạng thái/hiệu lực, viết lại để đúng cả trước lẫn sau khi đóng băng, và câu tự nhắc revision hiện hành: tiêu đề; ô `revision`; ô `thay_the_cho`; công thức băm (tên tệp; r21, r22 không dùng cấp lease; câu lease neo băm); đoạn "Hiệu lực r23" thay đoạn "Hiệu lực r22"; câu lease của revision hiện hành ở đoạn "Lease chép gì" và ở phần (5); §4 trỏ tệp r23; §11 mục 4 và mục 5 trỏ băm r23; thêm mục (r23) của `nguon_cap_viec`, bảng này và đoạn kiểm r23 | objective, write set, ô `executor`, closure, B1–B8, ba khối mã nhúng, §1–§10 trừ một câu của §4; các quan sát khác của cùng VERDICT (O1, O5) không áp |

**Kiểm lúc soạn r23** (phiên soạn r23, không phải phép đo trên launcher hay ứng viên; mọi số đếm dưới đây đo trên chính
tệp r23 cuối cùng): r1 đến r22 — sha256 khớp 22/22 số ghi ở công thức băm (r20, r21, r22 còn khớp số đầy đủ ở ô
`thay_the_cho`), `git diff --quiet HEAD --` hai mươi hai tệp ⇒ rc=0 trên HEAD `8b026b1`, `git status --short` chỉ có
tệp r23; hai VERDICT trên r22 khớp ô `nguon_cap_viec`. `diff -U0` r22 → r23: 12 hunk; mọi dòng đổi nằm ở phần đầu
tệp (trước §1), ở một dòng của §4 và ở §11 mục 4, mục 5; từ §1 tới hết §10, mọi dòng khác bằng r22. Sáu khối có rào của
r23, trích bằng máy, BẰNG sáu khối của r22 từng byte; ba khối mã nhúng trùng băm ghi trong tệp: `chot_tinh_r12.py` 412
dòng `add42b31…35b6`, khối B8 353 dòng `60ee8d5f…75ff`, `kiem_nhan_r12.py` 19 dòng `13f7728d…3b45`. B5 bằng nhau từng
byte ở cả bảy revision từ r17 tới r23. `kiem_nhan_r12.py` (bản vừa trích) trên chính tệp r23: 47 nhãn, 0 sai dạng, rc=0
ở `python3.11`, `python3.12`, `python3.13` — bằng r22. Sáu cụm trích PROTOCOL ở phần đầu tệp khớp nguyên văn như ở r22
(so với `docs/PROTOCOL_DA_PHIEN.md` của `ab457c6` sau khi gộp khoảng trắng). Sáu bảng ở phần đầu tệp (trước §1): mỗi
hàng đúng số cột của bảng mình. Tên tệp r23 có ở đúng 2 dòng (công thức băm, §4). 0 dấu chéo ngược, 0 CR, như r22; 0
dấu bỏ-qua-CI. Băm và số dòng của chính tệp r23 không ghi ở đây (công thức băm).

**Thay đổi so với r21** (mỗi dòng một lớp của VERDICT cross-review Claude trên r21 — sha256 `f4b9fd85…e3be`; slug là
tên lớp trong bảng lớp của VERDICT). r22 = bản gộp r21 + `HINT.patch` (sha256 `f545c1d6…17cf`) do điều phối dựng sẵn
(sha256 `e67c0a01…f964`), `cp` thành tệp r22 trước mọi sửa tay; phiên soạn r22 dựng lại bản gộp ấy trên một bản sao
r21 ngoài worktree (`patch -p0 --fuzz=0`, rc=0) và `cmp` BẰNG. Mỗi lớp được đo lại trước khi sửa; cột cuối ghi chỗ
HINT lệch phép đo. Bảng này và đoạn kiểm ngay dưới không trích nguyên văn chuỗi nào mà VERDICT hay đoạn kiểm đếm
bằng `grep`.

| slug lớp | hạng | chỗ sửa trong r22 | đo lại của phiên soạn r22 | HINT lệch phép đo |
|---|---|---|---|---|
| `khoi-moi-truong-b6-thieu-dang-va-gia-dinh-versionid` | P3 | ô `environment`: (b) trường thay `VERSION_ID` có điều kiện đo được và thứ tự cố định, giá trị bỏ nháy; (c) định nghĩa số vá; dạng khối liệt kê bảy lệnh theo thứ tự, CR bỏ trước mọi phép so; §7 B6: nghĩa vụ bằng chứng nêu khối, vế ĐỎ (r21) có ngoại lệ cho log dùng lại đủ bốn mỏ neo | rig đọc khối theo đúng chữ r22 trên một khối chạy thật ở container phiên soạn và mười ba biến thể tổng hợp có đáp án định trước (os-release kiểu Arch, kiểu Debian sid, có cả hai trường thay, không trường nào, `VERSION_ID` rỗng; CRLF; số vá có hậu tố, thiếu số vá, rc=127; đảo thứ tự lệnh, thiếu `uname -a`, dòng đứng trước khối, `Darwin`): 14/14 khớp đáp án; bản CRLF cho bộ năm bằng bản LF | HINT đặt điều kiện thay theo loại bản phân phối, không đo được, và cho hai trường thay mà không có thứ tự; chỉ bỏ CR khi so `Linux`; không định nghĩa số vá; mốc áp dụng của vế ĐỎ là lúc TẠO log, không đo được từ ngoài, và nêu tên r21 |
| `mo-neo-r21-hep-hon-quy-tac-va-lech-chu-nguon` | P3 | đoạn mỏ neo: câu nền PROTOCOL §10, câu PROTOCOL §4 và ba cụm của §3.2.1 chép nguyên văn; (1) phạm vi W0 strict; bảng (3): hàng bảng (E), hàng tập lệnh; (4) phía đến phủ cả D mục 6; đoạn lease chép gì; §11 mục 5 | PROTOCOL của `ab457c6`; AST `ops/lease_publish.py` của `ab457c6`; `git grep` chín khoá trên mã cổng; probe kho bare cục bộ (clone, worktree); sổ Mission #686 (finding theo từng attempt) | HINT ghi `write_set` chỉ để tính lớp review, trong khi `ai-dang-giu` cũng đọc nó; hàng bảng (E) thu hẹp phần đo lại về tập áp dụng, trong khi hàng ấy gồm cả hành vi E118; hàng tập lệnh xếp `chot_tinh_r12.py` vào nhóm không có băm; §11 mục 5 gán mã thiếu artifact cho hai attempt, attempt 1 không mang mã ấy; câu nền §10 vẫn là tóm tắt và thiếu policy/catalog |
| `tu-tham-chieu-r21-thi-hien-tai-va-lease-lich-su` | P3 | ô `revision` và đoạn "Hiệu lực r22": attempt 3 nói không thời gian, neo event; công thức băm: câu về lease neo r20 giới hạn theo nhánh đã đọc; (5): bỏ câu định trước OID cho handoff của lease sau, neo "hồ sơ" theo giờ; (3), (4): neo nguồn và giờ; câu tự nhắc revision hiện hành đổi sang r22 | readback #686 (comment cuối 2026-10-07T05:00:15Z; event `6031263612`); `git show` bốn lease wp685 trên `95f961e` | HINT vẫn dùng thì hiện tại kèm mốc; câu lease duy nhất neo r20 không nêu nhánh đã đo; giữ cụm hồ sơ hiện có; câu handoff của lease sau giả định lease ấy tiếp từ `4c404f9a…`; HINT viết trên r21 nên các câu tự nhắc vẫn nêu r21 |
| (không phải lớp) đầu tệp và câu tự nhắc | — | tiêu đề; `revision`; `thay_the_cho`; mục (r22) của `nguon_cap_viec`; bảng này thay bảng của r21; đoạn kiểm; §4 trỏ tệp r22; §11 mục 4 thêm vế r22 | — | — |

**Lịch sử r1 → r21** — không chép lại. Bảng "Thay đổi so với r16" và đoạn kiểm lúc đóng băng r17 nằm nguyên văn ở đầu
r17 (sha256 `36bb1214…48cbf`), và r18, r19, r20 giữ nguyên hai khối ấy từng byte (r18 thêm bảng lịch sử ngay dưới đường
kẻ; r19, r20 dùng đoạn "Hiệu lực"); bảng "Thay đổi so với r20" và đoạn kiểm lúc soạn r21 nằm nguyên văn ở đầu r21
(sha256 `1edd6c75…9aef`); các bảng trước nữa: đoạn này của r17. Các tệp ấy bất khả xâm phạm, cùng thư mục.

**Kiểm lúc soạn r22** (phiên soạn r22, không phải phép đo trên launcher hay ứng viên; mọi số đếm dưới đây đo trên chính
tệp r22 cuối cùng): r1 đến r21 — sha256 khớp 21/21 số ghi ở công thức băm (r20 và r21 còn khớp số đầy đủ ở ô
`thay_the_cho`), `git diff --quiet HEAD --` hai mươi mốt tệp ⇒ rc=0 trên HEAD `1be5bee`, `git status --short` chỉ có
tệp r22; `VERDICT.md` và `HINT.patch` khớp ô `nguon_cap_viec`; bản gộp của điều phối tái lập được (`cmp` rc=0). Sáu
khối có rào của r22, trích bằng máy, BẰNG sáu khối của r21 từng byte; ba khối mã nhúng trùng băm ghi trong tệp:
`chot_tinh_r12.py` 412 dòng `add42b31…35b6`, khối B8 353 dòng `60ee8d5f…75ff`, `kiem_nhan_r12.py` 19 dòng
`13f7728d…3b45`. B5 bằng nhau từng byte ở r17, r19, r20, r21 và r22. Danh sách ĐÓNG ở (E) mục 6 trích lại: 83 + 35 + 2
= 120 tên, 0 trùng. `kiem_nhan_r12.py` (bản vừa trích) trên chính tệp r22: 47 nhãn, 0 sai dạng, rc=0 ở
`python3.11`, `python3.12`, `python3.13` — r21 cũng 47 (r22 không thêm, không bớt nhãn). Sáu cụm trích PROTOCOL trong
ngoặc kép ở phần đầu tệp (năm cụm do r22 chép, một có từ trước) so với `docs/PROTOCOL_DA_PHIEN.md` của `ab457c6` sau
khi gộp khoảng trắng: khớp nguyên văn cả sáu. Năm bảng ở phần đầu tệp (trước §1): mỗi hàng đúng số cột của bảng mình.
Tên tệp r22 có ở đúng 2 dòng (công thức băm, §4). 0 dấu chéo ngược, 0 CR, như r21; 0 dấu
bỏ-qua-CI. Băm và số dòng của chính tệp r22 không ghi ở đây (công thức băm).

---


**Lịch sử r18 — impact analysis tại thời điểm soạn r18, không phải Q5/generation 2:** #668 đã đóng và PR #696 đã merge; hai tệp write set không đổi từ `423b4ba14078701859b9e6ac101a68a3fc4ddef4` đến `8c98afacb9285aa71e5200739236284f7a190d4f` (`git diff --quiet` rc=0). Ngày 05-10-2026, `ai-dang-giu` trên mirror 459 nhánh trả rc=0, `NGƯỜI_GIỮ 0` cho từng tệp. Phải đo lại ngay trước cấp lease. Mission Plan revision 3 đã được cài bằng event bootstrap #686 comment `5992836950`, plan hash `38b2b3ef9d4a410e2a6a00fdc1861611fd39295b7652062d2988ebc3513feb8a`. wp709 đã landed theo #709 comment `6020718211`; #686 comment `6020724444` gỡ dependency cho wp685. Chưa có spec r18 đóng băng hoặc Packet generation/lease wp685; vì vậy r18 chưa được coi là `ready`.

Đọc GitHub Contents API tại nền nghiệm thu `423b4ba14078701859b9e6ac101a68a3fc4ddef4` và canonical `ab457c651eb4428705f0492163080b661c858b72` ngày 07-10-2026: blob `.claude/dev/launcher.py` cùng là `561ff7a1840d65a6fc9953947f71cabe4947b3c9`; blob `.claude/dev/launcher_test.py` cùng là `3f02fb94abece5aa331f68fc890367cab50ac7a4`. Nền nghiệm thu có thể giữ về nội dung hai tệp; continuation base mới vẫn phải khai riêng khi cấp lease.

Q5 đo lại ngày 07-10-2026 trên mirror cách ly của GitHub, 467 `refs/heads/*`, `master=ab457c651eb4428705f0492163080b661c858b72`: `python ops/lease_publish.py ai-dang-giu <path> --root <mirror>` trả rc=0 và `NGƯỜI_GIỮ 0` cho cả `.claude/dev/launcher.py` lẫn `.claude/dev/launcher_test.py`; các lease được liệt kê đều hết hạn. Đây là phép đo chuẩn bị, **phải quét lại ngay trước lúc cấp lease** sau khi r18 được đóng băng và review.

| Lịch sử: thay đổi r18 so với r17 | Trạng thái khi soạn r18 |
|---|---|
| Executor Claude Sonnet 5.5 high → Google Antigravity Gemini 3.1 Pro High | Chủ kho duyệt tại #686 comment `5988699983`; Mission revision 3 đã cài, wp709 đã landed; chưa cài Packet generation/lease wp685. |
| Environment `cloud` → `local` qua `agy` trên Windows | Ubuntu-Clean đã gọi được Python 3.11.17 và 3.12.3 ngày 07-10-2026; B6 chưa chạy trên ứng viên, executor phải đo cả hai sau lease. |
| Write set, objective, acceptance B1–B8, review class và land obligations | Giữ nội dung r17, trừ số chỗ đọc `/proc/<pid>/stat` ở objective, §3 mục 7, §4, §6 mục 3 và B8: bốn → năm (mã nền có bốn lời đọc, ứng viên thêm lời đọc thứ hai ở `_con_song`); reviewer r18 phải kiểm ảnh hưởng của thay đổi executor/environment. |
| Spec hash và lease | Hash r18 chỉ công bố sau khi đóng băng; chưa có lease r18. |

## 1. Vấn đề

`.claude/dev/launcher.py:650–651` (trên `89fc4fa`), hàm `_con_song` (định nghĩa ở dòng 629), nhánh
không phải Windows: dòng 650 gán đường `/proc/<pid>/stat` cho một biến `Path`, và dòng 651 là (trích một
dòng, protocol §8 — đặc tả không chứa mã launcher ngoài ví dụ này):

```python
    if trang_thai.exists():
```

`Path.exists()` nằm **ngoài** khối `try`. `pathlib` chỉ nuốt errno `(2, 20, 9, 40)`
(`pathlib._IGNORED_ERRNOS`, đo trên Python 3.11.15). Tiến trình đang bị thu hồi làm `stat()` trả
**ESRCH** (errno 3) ⇒ `ProcessLookupError` thoát lên `_con_song_dung_khoa` → `_giet_rieng` → nơi gọi.

Bằng chứng CI (job `109303373142`, PR #679, head `aecdccd`): `t125` chạy toàn suite A/B **song
song**; vế B đỏ đúng một ca, `t154`:

```
ProcessLookupError: [Errno 3] No such process: '/proc/36606/stat'
```

**Phản chứng chạy được, bảng 1 — PID đang sống** (đo lại 11:11:47Z 29-09, Python 3.12.3, trên bản
sao tạm của launcher `89fc4fa`; seam: vá `pathlib.Path.stat` ném lỗi cho đúng đường
`/proc/<pid>/stat` của PID đang xét, `read_text` và `os.kill` không bị vá; PID sống = chính tiến
trình đang chạy):

| bản | ESRCH | EACCES | EIO | không seam: PID sống / PID không tồn tại |
|---|---|---|---|---|
| nền `89fc4fa` | **ném** `ProcessLookupError` | **ném** `PermissionError` | **ném** `OSError` | `True` / `False` |
| bản vá RỘNG (`except OSError: return False`) | `False` | **`False` — SAI** | **`False` — SAI** | `True` / `False` |
| bản vá HẸP **của r1** (OSError khác ⇒ rơi thẳng về `os.kill(pid, 0)`) | `False` | `True` | `True` | `True` / `False` |
| bản r2 (Q-A dưới đây) | `False` | `True` | `True` | `True` / `False` |

**Phản chứng chạy được, bảng 2 — zombie CHƯA `wait`** (cùng lúc, cùng Python; con thật do ca sinh
bằng `start_new_session`, nhận SIGTERM thật, đọc `/proc/<pid>/stat` thấy trạng thái `Z`, KHÔNG được
`wait` trong lúc đo; dọn bằng PID tường minh ở `finally`; seam chỉ vá `Path.stat` của PID ấy).
Cột cuối gọi `_giet_cay(pid, khoa)` trên một con còn SỐNG có seam EACCES ở `stat`, để SIGTERM thật
biến nó thành zombie; mã deadline suy từ `KetGiet.tron_ven` theo `launcher.py:1669`
(`tron_ven` ⇒ `MA_QUA_HAN` 124; ngược lại `MA_GIET_HUT` 125):

| bản | zombie, không seam | zombie, EACCES ở `stat` | zombie, EIO ở `stat` | zombie, EACCES ở CẢ `stat` lẫn `read_text` | `_giet_cay` con sống + SIGTERM + EACCES ở `stat` |
|---|---|---|---|---|---|
| nền `89fc4fa` | `False` | **ném** `PermissionError` | **ném** `OSError` | **ném** `PermissionError` | **ném** `PermissionError` |
| bản vá RỘNG | `False` | `False` | `False` | `False` | `tron_ven=True` ⇒ 124, 0,1 giây — đúng ở ca này, nhưng bảng 1 cho thấy nó sai ở PID sống |
| bản vá HẸP **của r1** | `False` | **`True` — SAI** | **`True` — SAI** | `True` | `tron_ven=False`, `me_da_chet=False` ⇒ **125**, 2,4 giây, 23 lần hỏi `stat` |
| bản r2 | `False` | `False` | `False` | `True` (bảo thủ, xem Q-A) | `tron_ven=True` ⇒ **124**, 0,1 giây, 2 lần hỏi `stat` |

Ba bản Python có trong container cho cùng kết quả ở các ô khoá của bảng 2 (hàng HẸP r1 và hàng r2,
cột EACCES ở `stat` và cột `_giet_cay`): 3.11.15 (11:11:58Z), 3.12.3 (11:11:47Z), 3.13.12 (11:12:01Z).
CI Linux của `ci.yml` dùng `python-version: "3.12"`; job `launcher` của `launcher-windows.yml` dùng
3.13 trên Windows và 3.11 trên Ubuntu.

**Bản "r2" trong các bảng 1, 2 và 3 là bản NHÁP của phiên soạn**, dựng ở bản sao tạm chỉ để kiểm hợp
đồng Q-A có thoả được và đo ra số trên. Nhãn "r2" ở đó chỉ bản nháp dựng theo Q-A.1–4 của r2 (r3 không
đổi Q-A.1–4; r4, r5, r6 và r7 cũng không), KHÔNG phải revision đặc tả r2. Bản nháp không nằm trong đặc tả này, không phải bản vá
đã được chứng nhận; executor tự viết bản của mình theo lời văn Q-A và tự đo lại.

Cross-review lượt 2 tái đo hai bảng trên bằng bản dựng độc lập của họ (VERDICT lượt 2, hướng 2,
11:23:21Z, ba bản Python): các ô khoá khớp (hàng HẸP r1 và hàng r2, `_giet_cay` 125 với 23 lần hỏi
`stat` so với 124 với 2 lần; thời gian 2,32 giây và 0,10 giây ở rig của họ — không phải hằng số). Bảng 1
và 2 ở trên giữ nguyên số r2 đã đo; phiên soạn r3 KHÔNG chạy lại chúng. Phiên soạn r3 chỉ chạy lại
probe `matrix_extra` của lượt 2 (bảng 3) và tự đo thêm bảng 4.

**Bảng 3 — đầu vào mới của r3** (chạy lại lúc 11:46:05Z 29-09, Python 3.12.3, probe `matrix_extra` trong
bản sao rig của cross-review lượt 2; các hàng "biến thể" là đột biến do reviewer dựng ở tệp `x_*.py` của
rig, phiên soạn không viết). Seam: `Path.stat` của PID sống (chính tiến trình probe) ném EACCES; với cột
đầu, `Path.stat` ném một đối tượng `RuntimeError` dựng sẵn; với ba cột nội dung, `Path.read_text` của đúng
đường `/proc/<pid>/stat` trả chuỗi cho sẵn, `<pid>` là PID của probe:

| bản | `RuntimeError` ở `stat` | nội dung rỗng | `<pid> (x)` | `<pid> (x) ` (khoảng trắng cuối) | số lần `read_text` trong lời gọi |
|---|---|---|---|---|---|
| bản nháp Q-A | thoát CHÍNH đối tượng ấy | `True` | `True` | `True` | 1 |
| biến thể "bắt `Exception` ở phép hỏi" | **bị nuốt** (`_con_song` trả `True`) | `True` | `True` | `True` | 1 |
| biến thể "nội dung hỏng ⇒ `False`" | thoát đúng đối tượng | **`False`** | **`False`** | **`False`** | 1 |
| biến thể "tầng đọc chỉ bắt `OSError`" | thoát đúng đối tượng | `ValueError` thoát | `IndexError` thoát | `IndexError` thoát | 1 |
| biến thể "đọc lần hai" | thoát đúng đối tượng | `True` | `True` | `True` | **2** |

Ba biến thể có chữ đậm (nuốt sentinel, `False` cho nội dung hỏng, đọc hai lần) là ba đường mà B1–B5 của r2
để lọt: cả ba PASS hai ca mẫu `t156_...` và `t157_...` do reviewer dựng theo B1–B3b của r2 (VERDICT lượt
2, hướng 3, 11:30:37Z; phiên soạn r3 chạy lại `mutations` lúc 11:46:12Z ra cùng kết quả: bảy đột biến của
r2 chết đúng nhãn, ba biến thể mới PASS cả hai ca, đối chứng `NameError` chết bằng `NameError`). Hàng
"tầng đọc chỉ bắt `OSError`" là **phản chứng phụ**: nó ĐỎ bằng lỗi vô can (`ValueError`/`IndexError`), nên
không được tính là đột biến bị giết đúng lý do.

**Bảng 4 — "nội dung không phân tích được" là những ngoại lệ nào** (phiên soạn r3 tự đo, Python 3.12.3;
biểu thức tách trạng thái của `launcher.py:654`; chuỗi thử dựng tay, `comm` thử thật):

| đầu vào | kết quả (đo 11:46:33Z) |
|---|---|
| rỗng | `ValueError` |
| thiếu dấu đóng ngoặc, ví dụ `32000 x S 1` | `ValueError` |
| hết chuỗi ngay sau dấu đóng ngoặc, `32000 (x)` và `32000 (x) ` | `IndexError` cả hai |
| đầy đủ, `32000 (x) S 1` | `'S'`, không ném |
| `comm` = byte `ff fe` + `ab` (con tự đặt bằng `prctl(PR_SET_NAME)`), `read_text` thật trên `/proc/self/stat` | `UnicodeDecodeError`: là `ValueError`, **không** là `OSError` (`preferred_encoding` `utf-8`; cùng kết quả với `LC_ALL=C.UTF-8`) |
| cùng loại `comm` ấy, PID ĐANG SỐNG, nền `89fc4fa`, không seam (đo 11:46:40Z) | `_con_song(pid)` = **`False`**, `os.kill(pid, 0)` thành công |

Dòng cuối là quan sát về nhánh CŨ, xem §2; nó không thuộc phạm vi sửa.

**Bảng 5 — ba ô tầng đọc mà r3 bỏ đo (r4 thêm; số của cross-review lượt 3, phiên soạn r4 chỉ ĐỌC log)**
(reviewer chạy probe `holes` lúc 12:42:57Z 29-09, Python 3.12.3, trong rig của họ; các hàng "biến thể" là
đột biến do reviewer dựng, phiên soạn không viết và KHÔNG chạy lại). Seam: `Path.stat` của PID sống (chính
tiến trình probe) ném EACCES, và `Path.read_text` của đúng đường `/proc/<pid>/stat` ném một đối tượng dựng
sẵn — cột 2: `ProcessLookupError` (ESRCH); cột 3: `OSError` (EIO); cột 4: một sentinel `KeyboardInterrupt`.
Ở mọi ô bộ đếm ghi 1 lần chạm `stat` và 1 lần chạm `read_text`. Cột cuối là kết quả của hai ca dựng theo
B1–B3b của r3 (tức hai ca mẫu r3 mô tả):

| bản | ESRCH ở `read_text` | EIO ở `read_text` | `KeyboardInterrupt` ở `read_text` | hai ca mẫu r3 |
|---|---|---|---|---|
| bản dựng theo Q-A r3 | `True` | `True` | thoát CHÍNH đối tượng ấy | PASS, PASS |
| biến thể "tầng đọc chỉ bắt `PermissionError`" | **thoát** `ProcessLookupError` | **thoát** `OSError` | thoát đúng đối tượng | PASS, PASS |
| biến thể "ESRCH ở tầng đọc ⇒ `False`" | **`False`** | `True` | thoát đúng đối tượng | PASS, PASS |
| biến thể "nuốt riêng `KeyboardInterrupt` ở tầng đọc" | `True` | `True` | **bị nuốt** (`_con_song` trả `True`) | PASS, PASS |

Ba biến thể là ba đường mà B1–B5 của r3 để lọt: cả ba PASS hai ca mẫu, vì r3 chỉ đặt đầu vào EACCES ở tầng
đọc và ghi ba ô còn lại là "KHÔNG ĐO ĐƯỢC" (lý do r3 nêu: EACCES đại diện cho họ `OSError`). Hàng thứ hai
phá đồng thời hai ô (ESRCH và EIO ở tầng đọc) nên cho **bốn sai lệch quan sát** trên ba biến thể: ESRCH ở
tầng đọc thoát; EIO ở tầng đọc thoát; ESRCH ở tầng đọc bị đọc thành "đã chết"; `KeyboardInterrupt` ở tầng
đọc bị nuốt. Cả bốn đo được ngay bằng seam cục bộ, không cần kernel hay đua thật; EACCES không đại diện
được cho họ `OSError`, vì một bản chỉ bắt `PermissionError` ở tầng đọc qua cả hai ca mẫu. Khi thêm đầu vào
tầng đọc vào cùng helper, reviewer thấy mỗi biến thể chết bằng `TinHieuChotCa` đúng ô của nó và bản dựng
đúng không chết (xem B5).

**Bảng 6 — chiều kết quả của bước PID dự phòng (r5 thêm; số của cross-review lượt 4 và số phiên soạn r5 tự đo)**

Phần A — số của reviewer lượt 4 (`04-fallback.log`, 13:34:58Z 29-09, Python 3.12.3; phiên soạn r5 chỉ ĐỌC log).
Seam: `Path.stat` của PID xét ném EACCES; `Path.read_text` của đúng đường `/proc/<pid>/stat` ném lỗi cho
sẵn; `os.kill` không bị vá. Bản "đúng" là bản dựng theo Q-A r4; bản "sai" là bản trả `True` ngay sau lỗi đọc,
không hỏi PID nào:

| đầu vào | bản đúng | bản sai |
|---|---|---|
| PID con đã `wait`, `stat` EACCES + `read_text` EACCES | `False` | **`True`** |
| PID con đã `wait`, `stat` EACCES + `read_text` EIO | `False` | **`True`** |
| PID con đã `wait`, `stat` EACCES + `read_text` ESRCH | `False` | **`True`** |
| PID sống, `read_text` ESRCH; `kill(pid, 0)` lần lượt thành công / ESRCH / EPERM / EIO | `True` / `False` / `True` / `False`, 1 lời gọi mỗi đầu vào | `True` ở cả bốn, **0 lời gọi** |
| hai ca mẫu của r4 (không có nhãn `B2-pid-du-phong`), và phép D | PASS, PASS; D PASS, PASS | **PASS, PASS; D PASS, PASS** |

Dòng cuối là lỗ: bản sai qua toàn bộ nghiệm thu của r4 mà báo "sống" cho PID đã chết.

Phần B — phiên soạn r5 chạy lại ma trận của reviewer (15:33:49Z 29-09, Python 3.12.3, rig sao chép, 4 tiểu
nhãn × 8 đầu vào đọc = 32 lời gọi) trên năm bản: bản đúng (ứng viên dựng theo Q-A r4) và bốn biến thể của lớp
(k) — k1 là biến thể của reviewer (tệp trùng từng byte với biến thể "trả `True` ngay" của họ, đo bằng `cmp`),
k2–k4 do phiên soạn r5 dựng, chỉ ở bản sao rig. Cột "nới" là cùng ma trận với mọi assertion của nhãn bị bỏ
(đầu vào vẫn chạy nguyên), ghi số lần chạm `stat` / `read_text` / `kill(pid, 0)` cộng dồn:

| bản | hai ca mẫu r4 | ma trận, assertion hiệu lực | ma trận, nới (stat / read / kill) |
|---|---|---|---|
| bản đúng | PASS, PASS | PASS | PASS; 32 / 32 / 32 |
| k1: trả `True` ngay | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong song kill count 0` | PASS; 32 / 32 / **0** |
| k2: gọi `kill(pid, 0)`, bỏ kết quả | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong da-wait result True` | PASS; 32 / 32 / 32 |
| k3: tự xử lý `kill`, mọi `OSError` ⇒ `False` | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong eperm result False` | PASS; 32 / 32 / 32 |
| k4: tự xử lý `kill`, `OSError` khác ⇒ `True` | PASS, PASS | `TinHieuChotCa:B2-pid-du-phong eio result True` | PASS; 32 / 32 / 32 |

Bốn biến thể cùng qua hai ca mẫu của r4 và mỗi biến thể chết ở một tiểu nhãn KHÁC nhau: mỗi trong bốn kết quả
(`song`, `da-wait`, `eperm`, `eio`) có đúng một mutant độc chiếm. Ở cột "nới" mọi biến thể chạy đủ 32 đầu vào
(seam đã chạm, không phải tắt đầu vào), nên cái chết ở cột trước là do assertion chứ không do thiếu thiết lập.
Đây là lý do B5 dòng (k) có bốn dòng (k1–k4) chứ không một: mutant của HINT lượt 4 chỉ chạm `song`.

**Bảng 7 — `Path.exists()` nuốt những ngoại lệ nào của `stat` (r6 thêm; số của cross-review lượt 5 và số phiên
soạn r6 tự đo lại)**

Reviewer lượt 5 đo `ValueError` ở seam `Path.stat` (`07-boundary.log`, 15:56:32Z–15:57:47Z 29-09): bản đúng cũng
trả về bình thường, nên không dùng được làm chốt. Phiên soạn r6 đo lại độc lập (16:20:07Z 29-09, ba bản Python
3.11.15, 3.12.3, 3.13.12 — cùng kết quả cả ba). Probe: vá đúng một hàm của `pathlib.Path`, chỉ cho đúng đường
`/proc/<pid>/stat` của tiến trình probe, ném MỘT đối tượng dựng sẵn; gọi `Path.exists()` trên đường ấy; so danh
tính đối tượng thoát ra. Bộ đếm lần chạm seam bằng 1 ở cả mười ô.

| ngoại lệ do seam ném | seam đặt ở `Path.stat` | seam đặt ở `Path.exists` |
|---|---|---|
| `ValueError` | `exists()` trả `False`, không ném (**bị nuốt**) | thoát, đúng đối tượng ấy |
| `UnicodeDecodeError` | `exists()` trả `False`, không ném (**bị nuốt**) | thoát, đúng đối tượng ấy |
| `IndexError` | thoát, đúng đối tượng ấy | thoát, đúng đối tượng ấy |
| `RuntimeError` | thoát, đúng đối tượng ấy | thoát, đúng đối tượng ấy |
| `KeyboardInterrupt` | thoát, đúng đối tượng ấy | thoát, đúng đối tượng ấy |

Hệ quả cho bảng không gian (§7 B2): ô "nhóm phân tích × tầng hỏi" đặt seam ở `Path.stat` chỉ đo được
`IndexError`; `ValueError` và `UnicodeDecodeError` ở seam ấy là **bất khả thi** (thư viện nuốt trước khi ngoại lệ
tới mã launcher, đo ba Python), nên ba đầu vào của ô đặt seam ở `Path.exists` — hàm mà nền thực sự gọi. Việc đặt
seam ở đó buộc ứng viên hỏi bằng `exists()`; ứng viên hỏi bằng lời gọi khác thì seam không chạm và ca ném lỗi
thường (quy ước chung ở §7), không tính là ĐẠT.

**Bảng 8, 9, 10 — số đo của phiên soạn r6, r7, r8 trên rig riêng** (prototype, KHÔNG phải ứng viên của executor):
nguyên văn ở §1 của r8 (sha256 `2ae6ee04…2aa3`), kèm "Đính chính bảng 8" của r7 và đoạn "Không chạy lại ở r8" —
không chép lại (r9, thu gọn). Mọi chỗ trong tệp này viết "bảng 8", "bảng 9" hay "bảng 10" (kèm số dòng) trỏ vào đúng
bảng ấy của r8, cùng số dòng. Chúng là số ĐO của bản nháp theo r6–r8; ràng buộc hiện hành nằm ở §3 và §7, không ở đó.

**Bảng 11 — số đo của phiên soạn r9 trên rig riêng (r9 thêm; KHÔNG phải ứng viên của executor)**

Rig r9: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho. Nền: `git archive 89fc4fa .claude/dev` (blob
`561ff7a1…`, `abf7f6ca…`, đo bằng `git hash-object`). Ứng viên nháp ESRCH: bản nháp theo r8 của reviewer lượt 8 (chép;
cùng ứng viên nháp r7–r8). **Ứng viên nháp Q-A.7** (dạng `read_text(encoding="latin-1")` ở năm lời đọc): phiên soạn
dựng lại độc lập bằng thay chuỗi, **trùng từng byte** (`cmp`) bản nháp latin-1 của reviewer lượt 8; M1–M5, M12 cũng
trùng từng byte bản reviewer; ba biến thể `errors="surrogateescape"` mới. Helper: helper của reviewer lượt 8 (chép)
đặt mặc định r9 (payload theo dõi, loại (2) như r7, `B2-dem-doc 4` kill 0, đuôi `e1 ba`) cộng loại `read args` do
phiên soạn r9 cài. Bốn ca B8: khối mã test ở mục B8 (trùng byte). `_con_song_that` đọc bytes. `PYTHONDONTWRITEBYTECODE=1`;
con dọn bằng PID tường minh, kiểm cuối 0 tiến trình sót. Ba Python 3.11.15, 3.12.3, 3.13.12 (UTF-8 mode), trừ khi ghi
khác; giờ UTC 30-09-2026. Mã rig không nằm trong đặc tả (protocol §8).

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bốn ca B8 × 12 bản | ma trận ở mục B8, **trùng từng ô ở ba Python**; mọi ô đỏ là `TinHieuChotCa` đúng ca và đúng loại | 09:03:39Z–09:11:54Z |
| 2 | `t156`/`t157` trên helper r9 | ứng viên nháp Q-A.7: SONG, SONG; nền: `B1 seam escaped`, `B3b-giet-cay seam escaped`; ứng viên nháp theo r8: `B2-eacces read args [((), {})]`, SONG | 09:12:09Z; 09:13:26Z; 09:14:56Z |
| 3 | A1/A2/W1/W0 cho 54 dòng, 55 cặp | **55/55** được chấp nhận | như dòng 2 |
| 4 | (E) trên ứng viên nháp Q-A.7 | bộ r8 chép từ rig phiên soạn r8 (93 dòng: 78 hạng mục cùng 15 dòng khác, chạy trên bản sao ứng viên mang đúng các dấu neo của bộ ấy) **93/93**; bộ r9 trọng tâm **33/33** (34 cặp); tách trong hàm trợ giúp **4/4**; B8: dòng 1. Ánh xạ vào (E) mục 6: **111/111 tên có phép đo đúng kỳ vọng** ở ba Python (và 23 dòng đo thêm ngoài danh sách — quét và lặp — cũng đúng). Trong đó: fp, fp2–fp6, fp6b, khác đối số và hai phép giả gọi lại hàm trợ giúp VÔ CAN ở A1, W1, W0; (j1) VÔ CAN (`LookupError`); `d0_value_thoat`, `d0_decode_thoat`, `d0_index_thoat` CHẤP NHẬN; mười hai dạng đọc lệch (`errors=` bốn cách, `cp1252`, `encoding="utf-8"` tường minh; × Đ0, Đ) và M4, M5 chết `read args` ở đầu vào đọc đầu tiên (A1 `B2-dem-lan` hay `B2-eacces`; W1 `B2-nhanh-cu song` hay `B2-eacces`); `d0_giai_ma_lai_utf8` ⇒ `B2-nhanh-cu utf8-hong-that result False`; `d_giai_ma_lai_utf8` ⇒ `B2-dem-doc 4 kill count 1` (W1 `B3-zombie result True`); hai đối chứng sống SONG | như dòng 2 |
| 5 | phép D | bản đúng xanh (`t156` 56 đơn vị, `t157` 1, đúng thứ tự); **65/65 control đỏ**, báo đúng đơn vị thiếu; **6/6** phép đảo `missing=[]`, `order=False`; control RỖNG bị đánh "không đỏ đúng" | như dòng 2 |
| 6 | danh sách ĐÓNG, trích bằng máy từ CHÍNH tệp này (3.12.3) | (E) mục 6: 83 + 26 + 2 = 111 tên, 0 trùng, số đếm khớp dòng đầu nhóm; 78 tên trích theo luật của reviewer lượt 8 từ bảng mở rộng r9 nằm trong 83 (5 còn lại: trục G); 65 khoá control của D trích từ thứ tự thực thi và bảng tiểu nhãn; phép so tập tên: đủ ⇒ XANH, thiếu / thừa / lặp / đổi tên một dòng ⇒ ĐỎ, cả (E) lẫn D | 09:29:51Z |
| 7 | kênh git cục bộ | ba tập lệnh rig (231 / 162 / 174 ký tự `'` `"` `<` `>`) qua commit, push, clone, `git show <OID>:<tệp>`: sha256 khớp cả ba. GitHub thật: r9 ghi "KHÔNG ĐO ĐƯỢC" (phía đọc đo ở r11 — bảng 13 dòng 16; phía ghi: lý do 5 của §10) | 09:20:45Z |
| 8 | B6, 3.12.3, hai vế trong MỘT lệnh (mỗi vế: clone từ worktree, checkout `5f7485c`, `core.abbrev` 7, chép tệp của vế, chạy) | nền `187/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 1)`; ứng viên nháp + helper r9 + bốn ca B8: `193/194 … (tong 195, bo qua 1, hong 1)`; hỏng duy nhất ở cả hai vế `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn) ⇒ **delta 0**; `--dot-bien` `176/176 dat (1 khong do duoc)` cả hai vế, hạng 176 mục cũ giống hệt, 7 dòng có kiểu ngoại lệ trong ngoặc ở CẢ hai vế (nền, không phải delta) | 09:16:54Z–09:22:08Z |
| 9 | ruff F (nhị phân `ruff` 0.15.8; `python3.12 -m ruff` vắng) | nền 5 F841, ứng viên nháp + helper r9 + B8: 5 F841, cùng năm dòng ⇒ delta 0 | 09:21:56Z |
| 10 | `git grep` trên `5f7485c` mọi lời đọc `/proc/…/stat` | ngoài `launcher.py`: đúng ba chỗ của §5; cộng `launcher_test.py:2142` (`/proc/1/comm`, chẩn đoán môi trường) | 09:20:53Z |

Không chạy lại ở r9: phép đo `stop`, locale ASCII, khoá không đổi định dạng và `cp1252` (số của lượt 8, ghi tại chỗ);
payload `bytes` qua helper; sàn Windows (suy ra từ bảng 9 dòng 10). Lời khai r9 về locale giải mã được 15 byte (Latin-1
thật) — "KHÔNG ĐO ĐƯỢC" — là SAI (cross-review lượt 9, lớp `khai-khong-do-duoc-ma-do-duoc`): `localedef -i en_US -f
ISO-8859-1 <thư mục>/en_US.ISO-8859-1` chạy được (reviewer: không cần root — §10), và `LOCPATH=<thư mục> LC_ALL=en_US.ISO-8859-1
PYTHONUTF8=0` cho `locale.getpreferredencoding(False)` = `ISO-8859-1` ở ba Python; trong locale ấy `t158` của khối r9
QUA trên launcher NỀN — ca có mặt mà không đo (sửa ở B8). Cơ chế payload theo dõi dạng `bytes` cũng đo được (lượt 9, ba
Python: cùng bảng phân hạng với `str`); qua helper đầy đủ: chưa đo. Số đo r10 của cả hai: bảng 12.

**Bảng 12 — số đo của phiên soạn r10 trên rig riêng (r10 thêm; KHÔNG phải ứng viên của executor)**

Rig r10: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` đặt vào trong rig;
`PYTHONDONTWRITEBYTECODE=1`. Nền `423b4ba` (`git show`). Ứng viên nháp và biến thể `launcher.py`: CHÉP từ rig
cross-review lượt 9 (chỉ đọc), kiểm bằng `diff` trước khi dùng — `cand_a` (latin-1) và `cand_b` (bytes) so nền 20 và 36
dòng; M1–M5, ba `surrogateescape` mỗi bản 2 dòng so `cand_a`, M12 4 dòng; `cand_split` (tách khối kill K0) 12 dòng thêm
so `cand_a`; `WK` (bỏ giải mã ở cả hai chỗ dựng khoá) 4 dòng, `WK1` và `WK2` (một chỗ) 2 dòng so `cand_b`; `WC_crash`
(launcher ném `RuntimeError` khi `comm` không ASCII, tức chết `rc=1`). Phiên soạn r10 tự dựng thêm `P701` = `cand_b` với
f-string lồng cùng loại dấu nháy ở `_khoa_danh_tinh` (cú pháp PEP 701, chỉ hợp lệ từ 3.12). `launcher_test.py` thử =
nền `423b4ba` + `_con_song_that` đọc bytes + khối B8 **trích bằng máy từ chính tệp r10** + helper `t156`/`t157` của
rig r9 (chép, sha256 `635d93fa…0494`); hai bản `DANG_DOC_QA7` (latin-1, bytes). Ô: `TH` = `TinHieuChotCa` (ghi LOẠI),
`VO_CAN` = lỗi thường, `BO_QUA`, `QUA`. "sót" = tiến trình mang dấu của con/mẹ/cháu B8 còn trong `/proc` sau mỗi bản.
Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC 30-09-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bốn ca B8 (khối r10, 281 dòng) × 18 bản, ba Python | mười một bản của bảng B8 (nền, `cand_a`, M1–M5, M12, ba `surrogateescape`) **trùng TỪNG Ô bảng B8** ở cả ba Python; `cand_b`, `cand_split` QUA ×4; `WK` QUA / QUA / `khong giet duoc` ("khoa danh tinh KHAC") / QUA; `WK1` QUA / QUA / `khong giet duoc` (khoá KHÁC) / `124 noi doi`; `WK2` QUA / QUA / `124 noi doi` / `124 noi doi`; 0 ô lệch giữa ba Python | 10:52:31Z–11:03:48Z |
| 2 | launcher chết vô can (`WC_crash`, rc=1) và cú pháp PEP 701 (`P701`) qua bốn ca B8 | `WC_crash`: bốn ô lỗi thường ở ba Python — `t158`, `t159` là `RuntimeError: dieu kien dung: launcher khong ket thuc bang ma han chot 124/125/10 kem so JSON: rc=1`; không ô nào là `TinHieuChotCa`. `P701`: ở 3.11 bốn ô lỗi thường (`t158`, `t159` cùng lỗi điều kiện dựng, stderr là `SyntaxError`; `t160`, `t161` `SyntaxError` khi nạp launcher); ở 3.12 và 3.13 QUA ×4 — chỉ vế 3.11 bắt được | như dòng 1 |
| 3 | `P701` ngoài suite; ruff | `python3.11 P701.py --help` rc=1 `SyntaxError: f-string: unmatched '('`; 3.12, 3.13 rc=0. `ruff check --select F`: mặc định `All checks passed!`, `--target-version py311` 1 lỗi (`invalid-syntax … on Python 3.11`); `cand_a`, `cand_b`, nền: 0 lỗi ở cả hai chế độ | 11:00:11Z |
| 4 | hạn sống của con B8 (mã do `_k124_ma_con` sinh, chạy một mình, không ai giết; 3.11.15) | tự thoát rc=0 sau 120,4 s, đúng 1200 nhịp | 10:52:43Z–10:54:44Z |
| 5 | điều kiện dựng hỏng: dòng `prctl` của cháu thay bằng `pass` | `t160`, `t161`: lỗi thường `dieu kien dung: comm cua chau chua doi`, 0 tiến trình sót, ba Python | 11:03:56Z–11:04:50Z |
| 6 | locale ISO-8859-1 (`localedef -i en_US -f ISO-8859-1` vào `LOCPATH` trong rig, rc=0; `LC_ALL=en_US.ISO-8859-1 PYTHONUTF8=0` ⇒ `getpreferredencoding(False)` = `ISO-8859-1` ở ba Python) | `t158`, `t159` BỎ QUA có khai ở mọi bản; `t160`, `t161`: nền và M12 `read args`, `cand_a` QUA, `WK` `t160` `khong giet duoc` (khoá KHÁC) — không phụ thuộc locale; `t156` trên `cand_a`: lỗi thường `dieu kien dung: read_text() giai ma duoc 15 byte`; ba Python | 10:59:09Z; 11:03:56Z–11:05:11Z |
| 7 | helper `t156`/`t157` (helper r9) trên hai cấu trúc khối kill, ba Python | `cand_a` (dùng chung) và `cand_split` (tách K0): SONG, SONG; đếm AST `os.kill` (`_con_song` cộng hàm nó gọi trực tiếp) 1 và 2. `k0_ESRCH_sai`, `k0_EPERM_sai`, `k0_EIO_sai`: trên `cand_a` chết ở nhãn đứng trước `B2-pid-du-phong` (`da-wait result True`, `eperm result False`, `eio result True`), trên `cand_split` chết đúng `B2-nhanh-cu` (`vang-da-wait result True`, `vang-eperm result False`, `vang-eio result True`); `t157` QUA ở cả sáu | 11:03:51Z–11:04:49Z |
| 8 | tiến trình sót sau mỗi bản (quét `/proc`, dấu của con/mẹ/cháu B8) | 0 ở mọi dòng 1–7, TRỪ chín bản đầu của lượt 3.11 dòng 1: `SOT=1`, chính PID của phép đo dòng 4 chạy song song (PID trùng tệp PID của nó), tự thoát ở hạn sống; lượt 3.11 chạy lại riêng: 0 ở cả mười hai bản, ma trận trùng lượt đầu từng ô; quét cuối toàn `/proc` (11:17:02Z): 0 | 11:05:12Z–11:07:58Z |
| 9 | danh sách ĐÓNG (E) mục 6, trích bằng máy từ tệp r10 | `DS-E-HANG-MUC` 83/83, `DS-E-KHAC` 27/27, `DS-E-C3` 2/2, tổng 112, 0 trùng | 11:18:37Z (lúc đóng băng) |
| 10 | nền `423b4ba` (§8) | AST: 189 ca = 155 `t` + 34, hậu tố lớn nhất 155; `DOT_BIEN` 174 (`:7013`), `DOT_BIEN_HARNESS` 3 (`:7931`); ruff 0 / 5 F841 ở cả hai chế độ; `_dot_bien_du_san`: (231, 65) đạt, biên 4 · (237, 65) đạt, biên 6 · (237, 71) đạt, biên 0 · (238, 66) đạt, biên 5 · (238, 72) KHÔNG đạt | 10:47Z–10:47:54Z |
| 11 | `git grep` trên `423b4ba` | chuỗi `linux:` trong `launcher.py`: đúng `:362`, `:494`; lời đọc `stat` ngoài `launcher.py`: đúng `gate_lifecycle.py:906`, `:933`, `ci_dang_ky_test.py:913` | 11:05:12Z |
| 12 | B6, hai vế trong MỘT lệnh cho mỗi Python (mỗi vế: clone từ clone sạch, checkout `423b4ba`, `core.abbrev` 7; vế sau chép `cand_a` và `launcher_test.py` thử) | `python3.11`: nền `188/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 0)` rc=0; nháp `194/194 … (tong 195, bo qua 1, hong 0)` rc=0. `python3.12`: nền `187/188 … (tong 189, bo qua 1, hong 1)` rc=1; nháp `193/194 … (tong 195, bo qua 1, hong 1)` rc=1. Bỏ qua duy nhất ở mọi vế: `t62` (fixture Windows); hỏng duy nhất ở cả hai vế 3.12: `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn ở 3.12, XANH ở 3.11 — nền khác nhau theo bản Python, đúng lý do phải so delta trong CÙNG một bản). **Delta 0 ở cả hai Python.** Vế nháp: `launcher.py` sha256 `2b93bc1e…1c0e` (`cand_a`), `launcher_test.py` sha256 `6fe7f02c…0f79`. `--dot-bien` hai vế: KHÔNG chạy lại ở r10 | 11:08:02Z–11:16:34Z |

**Bảng 13 — số đo của phiên soạn r11 trên rig riêng (r11 thêm; KHÔNG phải ứng viên của executor)**

Rig r11: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` trong rig, riêng cho mỗi bản;
`PYTHONDONTWRITEBYTECODE=1`. Nền `423b4ba` (`git show`; `launcher.py` sha256 `808ce5b3…9fc0`, `launcher_test.py`
`882ac43f…97cc`). Bản nháp `launcher.py`: 46 bản CHÉP từ rig cross-review lượt 10 (chỉ đọc; `nen` bằng nền từng byte;
mọi bản kiểm bằng phép so dòng theo hàm với nền), cộng 16 bản phiên soạn r11 dựng bằng tập lệnh thay thế có neo (mỗi
neo đúng một lần): `g_d0_open`, `g_d_open`, `SW_khoa`, `SW_nhom`, `SW_chup`, `SW_d0`, `SW_d`, `CAT_khoa`, `TASK_khoa`,
`DIRFD_khoa`, `SL2_khoa`, `ZB_nhom`, `ZB_chup`, `MEBO`, `MEHAN`, `D0_KIEMDL` — 62 bản. Khối B8: trích bằng máy từ
CHÍNH tệp r11 (351 dòng, `950b880a…7bad`); để đối chiếu còn khối r10 (`893b31ce…8366`, trích từ tệp r10), khối bản gộp
HINT (`b929f2b1…091a`, trích từ bản chỉ-HINT) và bản nháp đầu của khối r11 (thước đo `open` tính mọi đường). Helper:
helper r9 (`635d93fa…0494`) tách từ tệp thử của rig r10 — dựng lại tệp ấy đúng từng byte. Tệp test thử: nền
`423b4ba` + `_con_song_that` đọc bytes + khối B8 r11 + helper (latin-1 `c4267574…7905`, bytes `6f07a7cf…3ed8`).
Bộ lái gọi thẳng hàm ca, đặt `PR_SET_CHILD_SUBREAPER` rồi thu hồi mọi hậu duệ mồ côi SAU ca cuối (zombie vẫn nằm trong
`/proc` suốt lúc ca chạy, như dưới PID 1 của container — ngữ nghĩa ca không đổi; các ô trùng bảng 12 và lượt 10 từng
ô). Ô: `TH` = `TinHieuChotCa` (ghi LOẠI), lỗi thường, `BO_QUA`, `QUA`. Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC
30-09-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | bốn ca B8, khối r11, 54 bản × ba Python | 11 hàng cũ của bảng B8, ba hàng r10 (`WK`, `WK1`, `WK2`) và ba bản latin-1 (`WKa`, `WKa1`, `WKa2`) TRÙNG TỪNG Ô bảng 12 và lượt 10; `cand_a`, `cand_split`, `cand_b`, `cand_b_split` QUA ×4; chín `SX*` và ba `SW_*` của ba hàm ngoài: `_khoa_danh_tinh` ⇒ `t160`, `t161` `124 noi doi`, `_thanh_vien_nhom` ⇒ `t161` `124 noi doi`, `_chup_cay` ⇒ `t160` `124 noi doi`, `t161` `khong giet duoc`; mười `OPEN*`/`PATHOPEN`, `TASK_khoa`, `CAT_khoa`, `g_d0_open` ⇒ `t160`, `t161` `read args` (`open ngoai loi doc Path`); `RTcp1252_khoa` ⇒ `read args` (đối số); `g_d_open`, `SW_d` QUA ×4 (B8 không chạm đường mới); `SW_d0` ⇒ `t160`, `t161` `khong giet duoc`; `ZB_nhom` ⇒ `t158`, `t159` `qua han khong giet duoc`, `t160` `khong giet duoc`; `ZB_chup` QUA ×4; `MEBO` ⇒ `t160` `124 noi doi` (mẹ sống); `WC_crash` bốn ô lỗi thường; `P701` 3.11 bốn ô lỗi thường, 3.12/3.13 QUA ×4; **0 ô lệch giữa ba Python ngoài `P701`**; bộ lái thu hồi 2–4 con mồ côi mỗi bản, 0 con còn sống lúc hết ca | 15:50:44Z–16:03:21Z |
| 2 | thước đo `open` — đối chiếu | khối HINT (3.12): `TASK_khoa`, `CAT_khoa` QUA ở `t160`, `t161`; `g_d0_open` `read args ['open ngoai Path: 51829 su kien open, 51783 loi doc Path']`; khối r11: ba bản ấy `read args` (dòng 1); `DIRFD_khoa` ⇒ `read args` (sự kiện `'/proc/<pid>'`, `'stat'`), ba Python; `SL2_khoa` (`//proc/…`) ⇒ QUA ở `t160`, `t161`, ba Python — giá đã khai của bộ lọc; bản nháp đầu của khối r11 (tính mọi đường) với `_k124_khoa_that` không giải mã ascii (biến thể rig của khối): `cand_a`, `cand_b` QUA ở `t160`, `t161`, ba Python — KHÔNG có đỏ oan; khối r11 cùng biến thể: QUA; log của `TASK_khoa` trên bản nháp đầu ghi `…/encodings/__pycache__/latin_1.cpython-312.pyc` (3.12) — nạp module lười trong cửa sổ; `encodings.ascii`, `encodings.latin_1` không có trong `sys.modules` lúc khởi động (locale UTF-8, ba Python) và vẫn không có ngay trước cửa sổ | 15:50:44Z–16:05:29Z |
| 3 | khung ca, ca chậm, khối r11, ba Python | `nen_WAITK` và `M12_WAITK`: `t158` `qua han khong giet duoc` (rc=124, `tu thoat=han_song`, 122,1–122,2 s), `t159` `qua han khong giet duoc` (rc=10, `han_song`, 121,6–121,7 s); `cand_a_WAITK`: QUA ×2 (4,4–4,5 s); `KILLNEVER`: `t160` `khong giet duoc` (`chau tu thoat=han_song`, `me rc=-15`, 120,3–120,5 s), `t161` `khong giet duoc` (`han_song`, 120,1–120,2 s); `MEHAN`: `t160` `khong giet duoc` (`chau tu thoat=None`, `me rc=0`, 127,2–127,3 s); `MEBO`: `t160` `124 noi doi` (`me rc=None`, 2,5 s); 0 con sống lúc hết ca | 16:04:19Z–16:18:49Z |
| 4 | khung ca — đối chiếu trên khối HINT và r10 (3.12) | khối HINT: `MEBO` `t160` QUA; `MEHAN` `t160` lỗi thường `dieu kien dung: _giet_cay qua 60 s …` (127,2 s); `KILLNEVER` `t160` cùng lỗi thường (120,4 s); khối r10: `MEBO`, `MEHAN` `t160` QUA (`MEHAN` 127,2 s) — cả ba đường xanh hay lỗi thường trên khối cũ, ĐỎ đúng loại trên khối r11 (dòng 3); lượt 10 (VERDICT) đo `nen_WAITK`, `M12_WAITK` trên khối r10: `t158` QUA sau 122 s | 16:04:19Z–16:08:51Z |
| 5 | dấu tự thoát — probe gọi thẳng mã khối (3.12) | con: SIGTERM rc=-15 và SIGKILL rc=-9 ⇒ không dấu; tệp `comm` không ghi được ⇒ rc=1, dấu `ngoai_le`, `_k124_ket_luan` ném `RuntimeError: dieu kien dung …` (không phải `TinHieuChotCa`); cháu: SIGTERM ⇒ vẫn sống, không dấu, SIGKILL rc=-9 ⇒ không dấu; hết hạn: con rc=0 sau 120,4 s, 1200 nhịp, dấu `han_song`; cháu rc=0, dấu `han_song` | 15:47:29Z; 16:04:19Z–16:06:23Z |
| 6 | helper `t156`/`t157` (tệp test thử latin-1), ba Python | `cand_a`, `cand_split` SONG, SONG; nền `B1 seam escaped`, `B3b-giet-cay seam escaped`; M4 `B2-dem-lan read args`, M5 `B2-eacces read args`; `g_d0_open` `B2-nhanh-cu song read count 0`; `g_d_open` `B2-eacces read count 0`; `SW_d0` `B3-zombie result True`; `SW_d` `B2-parse p2 kill count 0`; `D0_KIEMDL` `B2-nhanh-cu p3 parse error escaped (IndexError …)`; `t157` QUA ở mọi bản trừ nền | 15:52:11Z–15:57:20Z |
| 7 | helper, dạng bytes (tệp test thử bytes) | `cand_b`, `cand_b_split`: `t156` `B2-eacces read count 0`, `t157` QUA, ba Python — helper của phiên soạn chỉ seam `read_text` | 15:55:55Z |
| 8 | chốt tĩnh phần còn lại (luật r11), 62 bản | chạy bằng 3.11: 44 ĐỎ, 18 ĐẠT (danh sách ở B2 của r11; r12 thay luật ấy — kết quả r12 trên cùng 62 bản: bảng 14 dòng 2); 3.13 khác đúng một dòng: `P701` ĐẠT | 16:05:53Z |
| 9 | điều kiện dựng hỏng: dòng `prctl` của cháu thay bằng `pass` | `t160`, `t161`: lỗi thường `dieu kien dung: comm cua chau chua doi`, 0 tiến trình sống lúc hết ca, ba Python | 16:04:43Z |
| 10 | locale | `setpriv --reuid 65534 --regid 65534 --clear-groups`: `uid` trong tiến trình 65534; mở thẳng đường dẫn của thư mục đích bị chặn (thư mục cha 0700); `localedef -i en_US -f ISO-8859-1 /proc/self/fd/7/en_US.ISO-8859-1` rc=0, tệp thuộc `nobody`; `localedef -i ru_RU -f KOI8-R` / `CP1251` / `ISO-8859-5` rc=0; `LOCPATH=… LC_ALL=… PYTHONUTF8=0` ⇒ `getpreferredencoding(False)` đúng tên, giải mã được 15 byte `_K124_COMM` ở cả năm locale, ba Python; bốn ca B8 (3.12) trên nền, `cand_a`, `cand_b`, M12, `WK`, `OPENl1_khoa` trong bốn locale giải mã được (ISO-8859-1 dựng bằng uid 65534, KOI8-R, CP1251, ISO-8859-5): ô Y HỆT nhau ở cả bốn — `t158`, `t159` BỎ QUA có khai; `t160`, `t161`: nền và M12 `read args [('read_text', (), {})]`, `cand_a`, `cand_b` QUA, `WK` `t160` `khong giet duoc` (khoá KHÁC) và `t161` QUA, `OPENl1_khoa` `read args` (open ngoài) — khớp bảng 12 dòng 6 | 15:38:33Z; 16:18:49Z–16:21:26Z |
| 11 | kernel thật dưới uid 65534, mọi PID trong `/proc` (`/proc` gắn `rw,relatime`) | `os.kill(pid, 0)`: EPERM 2329 / 2330 / 2331 (3.11 / 3.12 / 3.13), thành công 1 (chính nó), ESRCH 2 (PID ngoài `pid_max`), **0 EACCES**; `stat` và đọc `/proc/<pid>/stat`: thành công ở mọi PID (2341 / 2342 / 2344), 0 lỗi | 15:40:39Z; 16:12:32Z |
| 12 | B4 — `platform.system` giả Darwin, Windows, FreeBSD | `t158`–`t161` BỎ QUA ×4 ở ba nền giả × ba Python; móc audit KHÔNG được cài | 16:00:09Z |
| 13 | B6, hai vế trong MỘT lệnh cho mỗi Python (hai vế dựng trong cùng một vòng lặp: clone kho bare của rig, checkout `423b4ba`, `core.abbrev` 7, không nông; vế sau chép `cand_a` `48756818…` và tệp test thử latin-1; mỗi lượt suite bọc subreaper ở CẢ HAI vế, `--nhat-ky`) | `python3.11`: nền `188/188 ca DA CHAY QUA (tong 189, bo qua 1, hong 0)` rc=0; nháp `194/194 ca DA CHAY QUA (tong 195, bo qua 1, hong 0)` rc=0. `python3.12`: nền `187/188 … (tong 189, bo qua 1, hong 1)` rc=1; nháp `193/194 … (tong 195, bo qua 1, hong 1)` rc=1. Bỏ qua duy nhất ở mọi vế: `t62`; hỏng duy nhất ở cả hai vế 3.12: `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc` (đỏ sẵn; nguyên nhân đo ở lượt 10: PEP 668 của bản 3.12 cài sẵn). **Delta 0 ở cả hai Python**, trùng số bảng 12. Nhật ký ca: 189/189 và 195/195 vào = ra, `# XONG TRON VEN` cả bốn lượt; bốn ca B8 và hai ca helper QUA trong toàn suite; mồ côi thu hồi sau lượt: 5 / 8 / 5 / 7, 0 còn sống | 16:21:39Z–16:30:39Z |
| 14 | ruff 0.15.8 `--select F`, mặc định và `--target-version py311` | nền `launcher_test.py` 5 F841 (2566, 3387, 3629, 4110, 6062); tệp test thử latin-1 và bytes: đúng 5 F841 ấy, cùng dòng; `launcher.py` nền, `cand_a`, `cand_b`: `All checks passed!` — delta 0 ở cả hai chế độ | 16:02:05Z |
| 15 | danh sách ĐÓNG (E) mục 6, trích bằng máy từ tệp r11 | `DS-E-HANG-MUC` 83/83, `DS-E-KHAC` 35/35, `DS-E-C3` 2/2, tổng 120, 0 trùng; đủ tám tên mới | 16:09:43Z (đo lại lúc đóng băng: 16:31:43Z) |
| 16 | REST (GET, `Authorization: Bearer` bằng `GITHUB_PAT`; mọi lời gọi 200 kèm `X-Github-Request-Id`) | run `36696528580`: `push`, `master`, `423b4ba`, workflow `gate` (`ci.yml`), 14 job — tên context ở ô `required_checks`; `gate-registry (ubuntu-latest)` `failure` ở bước 11, log: `ops/nhanh_don_duoc_test.py` rc=-9 sau 4500,384 s; run `36737283472` (`thu-hoi`, `pull_request_target`, PR #602): job `thu-hoi`; #686 `id` 5628902742, thân 3243 byte, sha256 `2af24e28…d9de`, 12 `"` thô, 0 thực thể HTML; comment `5888633201`, `5905670017`, `5907480436`, `5909554178`, `5913959273` (§10); tệp r1 qua `contents` (`3915f46`): sha256 `ee44238c…37d9` = bản cục bộ = `git show` sau `git fetch` | 15:31:42Z–15:58:17Z |
| 17 | nền | `git ls-remote origin refs/heads/master` ⇒ `fc852fff…c294`; kho bare của rig: `423b4ba` là tổ tiên, 29 commit, write set rc=0, `.claude .github` không đổi; `86b23c0` là tổ tiên của `fc852ff`; `9887bfc` không là tổ tiên (rc=1) | 15:31:19Z |
| 18 | zombie của container (đếm `/proc`, trạng thái `Z`) | trước mọi phép đo của r11: 2242, cả 2242 có `PPid` 1; sau ma trận, ca chậm, locale: 2242 / 2242; sau B6: 2242 / 2242 — r11 không để lại zombie nào dưới PID 1; mọi lượt lái và bọc: 0 con còn sống lúc hết, 0 con còn lại sau thu hồi | trước lúc dựng rig (lệnh đếm đầu không in giờ); 16:21:26Z; 16:30:47Z |

**Bảng 14 — số đo của phiên soạn r12 trên rig riêng (r12 thêm; KHÔNG phải ứng viên của executor)**

Rig r12: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` trong rig; `PYTHONDONTWRITEBYTECODE=1`.
Container khởi động lại giữa lượt soạn (uptime 1 phút lúc 22:16:36Z 30-09): mọi kết quả trước đó bị BỎ và đo lại từ đầu.
Nền `423b4ba` (`launcher.py` `808ce5b3…9fc0`). Bản nháp `launcher.py`: 31 bản của rig cross-review lượt 11 và 62 bản
của rig r11 — ĐỌC tại chỗ, không sửa, không chép đè; 45 bản đường vào và hai đột biến (a), (b) do phiên soạn r12 dựng
bằng thay chuỗi có neo (mỗi neo đúng số lần khai). Tệp test thử có helper r9 và khối B8 r11: CHÉP từ rig r11
(latin-1 `c4267574…7905`, bytes `6f07a7cf…3ed8`, đo lại băm). Bộ lái có sinh tiến trình đặt `PR_SET_CHILD_SUBREAPER`,
chỉ giết và `waitpid` con của CHÍNH nó. Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC 30-09-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | áp `HINT.patch` lượt 11 | bản sao r11 trong rig: `patch -p0 --fuzz=0` rc=0, 9/9 hunk, ba hunk nhóm 2 báo offset 25/27/27, 0 fuzz, 2740 dòng / 327 826 byte, sha256 `9e1ac379…9b84` = bản gộp VERDICT; trong worktree: `cp` r11 → r12, `sed -E` đổi tên tệp trong HINT (4 lần nhắc, cả 4 trên dòng `---`/`+++`), `patch -p0 --fuzz=0` rc=0, `cmp` bằng bản trên, 0 tệp `.orig`/`.rej` | ngay sau 22:16:36Z (lệnh không in giờ) |
| 2 | chốt tĩnh r12 (`chot_tinh_r12.py`, `add42b31…35b6`), 141 bản, `python3.11` và `python3.13` | bốn ứng viên nháp ĐẠT, rc=0, 13/13 (latin-1) hay 14/14 (bytes) đối chứng ĐỎ đúng luật; nền ĐỎ `H` ở ba hàm. 31 bản rig reviewer: 6 ĐẠT / 25 ĐỎ (29 bản của log/28: 6 / 23 — luật HINT: 11 / 18); 62 bản rig r11: 12 / 50; 44 đường vào tự liệt kê: 5 / 39; rig r12: `cand_a`, (a), (b) ĐẠT, nền ĐỎ. Mọi bản ĐẠT có đủ đối chứng ĐỎ đúng luật. 3.11 và 3.13 cùng kết cục trên 141 bản trừ `P701` (3.11 không parse được, 3.13 ĐẠT). Một lượt lô trước đó phân loại dạng đọc SAI (bộ phân loại của rig đọc `read_bytes()` ở chỗ khác trong tệp) — bỏ, sửa bộ phân loại, chạy lại | 23:02:45Z–23:15:30Z |
| 3 | luật đề nghị của HINT lượt 11 — CHÍNH `rig/chot_tinh_ast.py` của reviewer (chỉ đọc) — trên 44 đường vào r12 | 37 ĐẠT, 7 ĐỎ (một đỏ oan: chú thích thành dòng trong thân); 3.11 = 3.13 | sau 23:15:30Z (lệnh không in giờ) |
| 4 | đột biến chính script chốt — 15 đột biến (tắt hay nới đúng một luật, kể cả thêm `setattr` vào T3 và `os.open` vào T6) × `cand_a`, `cand_b` | 30/30 đúng kỳ vọng ở 3.11 và 30/30 ở 3.13: rc=2 và đúng đối chứng của luật ấy hết ĐỎ (`khoa_luon_hop_le` trên latin-1: không áp dụng, rc=0). Lượt đầu (22:57:06Z–22:58:19Z) lộ `tat_M` rc=0 — nhánh so từng câu của `M` không có đối chứng riêng — và một đột biến rig quá thô; sửa script (một phép so danh sách) và đột biến, đo lại | 22:59:45Z–23:02:37Z |
| 5 | `cs_subprocess` — tiến trình con qua `subprocess.run` trong khối Đ0 của `_con_song` | chốt tĩnh ĐẠT (3.11, 3.13); helper `t156`: `B2-nhanh-cu song read count 0` ở ba Python | sau 23:03:28Z (lệnh không in giờ) |
| 6 | nới tuần tự (B5, "Chốt ngược") — `t156` của helper r9, mỗi lượt nới thêm đúng nhãn vừa giết | `cand_a` sống ngay; (a) gỡ bản vá: 12 nhãn; (b) bản RỘNG: 11 nhãn, đúng tập của (a) trừ `B1`; nền: 14 nhãn; ba Python cùng số; 0 con sót, zombie toàn máy 1 → 0 | 22:31:42Z–22:32:04Z |
| 7 | khối B8 r12 (353 dòng, `60ee8d5f…75ff`) | AST bỏ mọi docstring BẰNG khối r11 ở ba Python; trích bằng máy từ tệp r12, `cmp` trùng khối đã chạy; bốn ca (3.12): nền `124 noi doi` / `qua han khong giet duoc` / `124 noi doi` / `124 noi doi`, `cand_a` QUA ×4; bộ lái thu hồi 4 và 2 con mồ côi, 0 còn sống; zombie 0 → 0 | 23:02:56Z–23:03:28Z |
| 8 | REST (GET, `Authorization: Bearer` bằng `GITHUB_PAT`; `HTTP/1.1 200 OK` sau dòng CONNECT của proxy, kèm `X-Github-Request-Id`) | PR #688: 12 comment, trang 2 rỗng; lượt 11 = `5920625021`; so thân comment lượt 10, 11 với tệp VERDICT: §10, gạch đầu dòng "Dữ kiện do điều phối cấp" | 22:32:13Z |
| 9 | nền | `git ls-remote origin refs/heads/master` ⇒ `fc852fff…c294`; đối tượng cục bộ của worktree: `7f26814` KHÔNG là tổ tiên (rc=1), `423b4ba` là tổ tiên (rc=0), write set rc=0, `.claude .github` rỗng; `git log -G'^VERSION = '` trên `launcher.py`: 8 commit, giá trị 1.0.0 → 1.5.0 (7 lần đổi, đọc từng commit và cha) | 22:33:02Z |
| 10 | nhãn `KHÔNG ĐO ĐƯỢC` — `kiem_nhan_r12.py` (§10, `13f7728d…3b45`) | bản chỉ-HINT lượt 11: 41 nhãn (`grep -o` 37 — bốn nhãn gãy dòng), 28 sai dạng, rc=1; r12 lúc đóng băng và hai đối chứng: dòng cuối bảng này | xem dòng cuối |
| 11 | nhãn lúc đóng băng — `kiem_nhan_r12.py` trên chính tệp r12 | 42 nhãn (`grep -o` cũng 42: không nhãn nào gãy dòng), 0 sai dạng, rc=0; đối chứng trên bản sao r12: bỏ một "(lý do 4)" ⇒ rc=1 đúng một chỗ; thêm một nhãn không lý do gãy qua hai dòng ⇒ rc=1 đúng một chỗ | 23:21:41Z; chạy lại sau lần sửa cuối |
| 12 | băm đầu vào lúc đóng băng | `VERDICT.md` `0a7d934c…6f80`, `HINT.patch` `207859e3…4f5b`, r1 đến r11 (`ee44238c` … `830d5ce4`): khớp số đo lúc bắt đầu (22:16:36Z) và số ghi ở đầu tệp | 23:23:15Z |
| 13 | vệ sinh | zombie toàn máy: 0 lúc bắt đầu (22:16:36Z, container vừa khởi động), 0 lúc đóng băng; 0 tiến trình còn sống mang đường dẫn rig r12; `git status --short` chỉ có tệp r12, HEAD `7f26814` | 23:23:15Z |

**Bảng 15 — số đo của phiên soạn r13 trên rig riêng (r13 thêm; KHÔNG phải ứng viên của executor)**

Rig r13: thư mục trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` trong scratchpad; `PYTHONDONTWRITEBYTECODE=1`.
Nền `423b4ba` (`launcher.py` `808ce5b3…9fc0`, `launcher_test.py` `882ac43f…97cc`, lấy bằng `git show`). Ứng viên tham
chiếu do phiên soạn r13 dựng bằng thay chuỗi có neo (mỗi neo đúng một lần; cách dựng ở §4); bản `cand_a`, `cand_b` và
tệp test thử `test_by.py` của rig cross-review lượt 12 chỉ ĐỌC. Bộ bọc có sinh tiến trình đặt `PR_SET_CHILD_SUBREAPER`,
chỉ giết và `waitpid` hậu duệ của CHÍNH nó. Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC 01-10-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | băm đầu vào | `VERDICT.md` `0fae0179…409a`, `HINT.patch` `f901250d…8a1d`: khớp chỉ thị và khớp số ghi trong bản chiếu `5922115123`; r1 đến r12: khớp số ghi ở đầu tệp trước khi áp HINT; lúc đóng băng: dòng 11 | trước 00:30Z (lệnh không in giờ) |
| 2 | áp `HINT.patch` lượt 12 | bản sao r12 trong rig: `patch -p0 --fuzz=0` rc=0, 9/9 hunk, nhóm 2 báo offset 2, nhóm 3 offset 41, 0 fuzz, 3366 dòng / 373 566 byte, sha256 `127a8cb4…0b5a` = bản gộp VERDICT. Biểu thức `sed -E` của chỉ thị (đổi MỌI chỗ nhắc tên tệp): HINT nhắc tên tệp r12 ở 7 dòng — 6 dòng `---`/`+++` và dòng ngữ cảnh 79 (câu §4 "Đặc tả này (…)") — nên dòng ngữ cảnh cũng bị đổi, hunk nhóm 2 FAILED, rc=1 (đo trên bản sao, không đụng worktree). Trong worktree: `cp` r12 → r13, `sed -E` CHỈ trên dòng bắt đầu bằng `---` hay `+++` (6 dòng đổi), `patch -p0 --fuzz=0` rc=0, 9/9, cùng offset, `cmp` BẰNG bản gộp, 0 tệp `.orig`/`.rej`; sau đó r13 tự sửa hai câu nhắc tên tệp (Công thức băm; §4) | rig: 00:30Z; worktree: 00:47:07Z |
| 3 | kích thước diff thi hành — ứng viên tham chiếu (§4), `git diff --no-index --numstat` so nền | `launcher.py` +21 / −5; `launcher_test.py`: chỉ `_con_song_that` cộng khối B8 +358 / −2, thêm helper +1096 / −2, đủ +1312 / −2 ⇒ tổng **+1333 / −7**, 2 tệp. Dựng lại lúc 00:54:50Z ra cùng sha256 (`bdf38658…6a40`, `a9b0494b…f6ab`). Ứng viên `cand_a`, `cand_b` của reviewer lượt 12: `launcher.py` +19 / −5 và +27 / −13 | 00:54:50Z; `cand_a`, `cand_b` khoảng 00:37Z (lệnh không in giờ) |
| 4 | ứng viên tham chiếu đúng đặc tả | chốt tĩnh `chot_tinh_r12.py` (trích bằng máy từ r12, `add42b31…35b6`): `python3.11` và `python3.13` ĐẠT rc=0, 13 đối chứng ĐỎ đúng luật (`K` không áp dụng ở dạng latin-1); nền ĐỎ rc=1. Sáu ca mới, `python3.12 launcher_test.py --lap-ca tNNN --lan 1` từng ca, bọc subreaper: ứng viên QUA 6/6; nền (`launcher.py` nền cùng tệp test ứng viên) ĐỎ 6/6 đúng loại — `B1 seam escaped`, `B3b-giet-cay seam escaped`, `B8-sau-sinh 124 noi doi`, `B8-luc-sinh qua han khong giet duoc` (rc=10), `B8-setsid 124 noi doi`, `B8-me-thoat 124 noi doi`; 0 mồ côi còn sống phải giết. Nạp module ứng viên (`python3.12`): 17 nhãn (16 + 1), 48 tiểu nhãn, 57 đơn vị, 195 ca, `DOT_BIEN` 228, harness 3, `DANG_DOC_QA7` dạng latin-1 | chốt tĩnh 00:54:50Z; sáu ca 00:38:33Z–00:39:09Z; số đếm sau 00:39:09Z (lệnh không in giờ) |
| 5 | phần "đặc" (đếm theo AST: bỏ dòng trống, dòng chỉ có chú thích, dòng docstring) | khối B8 353 = 42 + 9 + 30 + **272**; helper r9 737 = 100 + 11 + 14 + **612**; phần thêm của `launcher.py` 21 = 4 dòng chú thích + **17** | 00:54:50Z |
| 6 | 54 mục `DOT_BIEN` của ứng viên tham chiếu | 216 dòng (bốn dòng mỗi mục); 54/54 chuỗi cũ xuất hiện đúng một lần trong ứng viên; bảng rig r8 mỗi dòng một cặp, dòng (c) hai ca đích. Chạy `--dot-bien` trên chúng: CHƯA ĐO | 00:54:50Z |
| 7 | chốt tĩnh, tự liệt kê chỗ ghi lỗi (§7 B2, "Răng của đối chứng") | 14 chỗ `loi.append` trong `kiem`; tắt từng chỗ trên bản sao script, `python3.11`, ứng viên latin-1 của rig r13 và `cand_b` bytes: rc=2 ở 9 chỗ (dòng script 198, 218, 231, 233, 236, 238, 240, 245, 250), rc=0 ở 5 chỗ (193, 210, 225, 242, 252) — hai ứng viên như nhau. Biến thể: hai `def` mới cùng tên, bản sau gọi `os.open` ⇒ nguyên văn 1, tắt 210 ⇒ 1, tắt 225 ⇒ 1, tắt cả hai ⇒ 0; `def _chup_cay` thứ hai trả `{}` ⇒ nguyên văn 1, tắt 193 ⇒ 0; `def _khoa_danh_tinh` thứ hai ⇒ nguyên văn 1, tắt 193 ⇒ 2. Lượt in đầu của bảng rc biến thể ra 0 ở mọi ô — tạo tác của vỏ (`$(basename …)` trong cùng lệnh `echo` đặt lại `$?`), BỎ và đo lại bằng biến giữ mã thoát | 00:56:26Z–00:57:39Z; biến thể 00:58:30Z–00:59:08Z |
| 8 | REST (GET, `Authorization: Bearer` bằng `GITHUB_PAT`, 200 kèm `X-Github-Request-Id`) | PR #688 có 15 comment; `5922115123` (00:19:49Z, 2117 ký tự), `5922248948` (00:29:51Z, sha256 thân `32707eed…f53c`), `5922387653` (00:42:33Z, `d537d59e…c26d`); cả ba: 0 thực thể HTML, 0 CR | 00:59:15Z |
| 9 | nền | `git ls-remote origin refs/heads/master` ⇒ `fc852fff…c294`; đối tượng cục bộ của worktree: `423b4ba` tổ tiên (rc=0), 29 commit, write set rc=0, `.claude .github` rỗng; `417071e` KHÔNG là tổ tiên (rc=1) | 00:46:55Z |
| 10 | nhãn lúc đóng băng — `kiem_nhan_r12.py` (trích bằng máy từ r13, `13f7728d…3b45`) trên chính tệp r13 | 40 nhãn (`grep -o` cũng 40: không nhãn nào gãy dòng), 0 sai dạng, rc=0. r12 và bản gộp HINT: 42 mỗi bản (đo cùng lúc). Từ bản gộp sang r13, so từng ngữ cảnh: bỏ ba lần NHẮC tên (ô `nguon_cap_viec` của r12, tên hạng A/W cũ, câu §10 do HINT thêm — nay viết lại), thêm một lần nhắc trong ghi chú đổi tên hạng ⇒ 40. Đối chứng trên bản sao r13: xoá lý do ngay sau một nhãn ⇒ rc=1 đúng một chỗ; thêm một nhãn không lý do gãy qua hai dòng ⇒ rc=1 đúng một chỗ. Lượt đầu của đối chứng thứ nhất xoá nhầm một "(lý do 4)" nằm trong lời mô tả của bảng 14, không đứng sau nhãn ⇒ rc=0: đối chứng đặt sai chỗ, không phải máy kiểm mù — dựng lại | 01:01:46Z–01:02:13Z; chạy lại sau lần sửa cuối |
| 11 | băm lúc đóng băng | `VERDICT.md`, `HINT.patch`: khớp dòng 1; r1 đến r12: sha256 khớp 12/12 số ghi ở đầu tệp (r12 đủ 64 ký tự `fba80c32…e89fe2`), và `git diff --quiet HEAD --` mười hai tệp ⇒ rc=0 (không đổi byte nào so commit `417071e`) | 01:01:19Z–01:01:26Z |
| 12 | vệ sinh | zombie toàn máy 0; 0 tiến trình còn sống mang đường dẫn rig r13; bộ bọc subreaper: 0 hậu duệ còn sống phải giết ở mọi lượt; `git status --short` chỉ có tệp r13, HEAD `417071e` | 01:01:19Z |

**Bảng 16 — số đo của phiên soạn r14 trên rig riêng (r14 thêm; KHÔNG phải ứng viên của executor)**

Rig r14: thư mục `mktemp -d` trong scratchpad của phiên soạn, ngoài kho; `TMPDIR` trong rig; `PYTHONDONTWRITEBYTECODE=1`.
Nền `423b4ba` (`launcher.py` `808ce5b3…9fc0`, `launcher_test.py` `882ac43f…97cc` — `git show 423b4ba:` cho cùng băm).
Ứng viên tham chiếu r13 dựng lại bằng chính `dung.py` của rig r13; ứng viên độc lập, log và kịch bản của rig cross-review
lượt 13 chỉ ĐỌC (bộ đếm dòng đặc `dem_dac.py` của rig ấy được chạy, không sửa). Tập lệnh A/W và D, bộ dựng biến thể
mục 5 và bộ bọc là mã RIG của phiên soạn r14, không phải mã đề nghị. Bộ bọc có sinh tiến trình đặt
`PR_SET_CHILD_SUBREAPER`, chỉ giết và `waitpid` hậu duệ của CHÍNH nó. Ba Python 3.11.15, 3.12.3, 3.13.12; giờ UTC 01-10-2026.

| # | phép đo | kết quả | giờ UTC |
|---|---|---|---|
| 1 | băm đầu vào | `VERDICT.md` `2bbac4e8…3fb0`, `HINT.patch` `1ca8b3d8…f7ab`: khớp chỉ thị; VERDICT ghi `reviewed_sha` `da119d74…` = HEAD của worktree và `spec_sha256` `1ef830ab…97b9` = `sha256sum` r13; r1 đến r13: sha256 khớp 13/13 số ghi ở đầu tệp, `git diff --quiet HEAD --` mười ba tệp ⇒ rc=0; lúc đóng băng: dòng 15 | trước 04:26:24Z (lệnh không in giờ); r1 đến r13 04:43:09Z |
| 2 | áp `HINT.patch` lượt 13 | bản sao r13 trong rig: `patch -p0 --fuzz=0` rc=0, 5/5 hunk, hai hunk nhóm 2 offset 16, 0 fuzz, 3519 dòng / 399 024 byte, sha256 `7135e5c8…30d1`, `cmp` BẰNG bản gộp trong thư mục áp thật của rig lượt 13; HINT: tên tệp ở 4 dòng, cả 4 là `---`/`+++`, 0 CR, 0 dấu chéo ngược. Trong worktree: `cp` r13 → r14, `sed -E` CHỈ trên dòng `---`/`+++` (4 dòng đổi), `patch -p0 --fuzz=0` rc=0, cùng offset, `cmp` BẰNG bản gộp, 0 tệp `.orig`/`.rej` | rig 04:26:24Z; worktree 04:26:34Z |
| 3 | ứng viên tham chiếu r13, dựng lại (§4) | `dung.py` (`b96dc942…b3b4`) chép vào rig r14 cùng tệp nền và khối B8 của rig r13; helper r9 (`635d93fa…0494`, 737 dòng, rig r11) và `mutants7.json` (`ba7047cd…d878`, rig r8) — băm khớp §4 — nối bằng liên kết tượng trưng, không chép. Ra `launcher.py` `bdf38658…6a40` (4324 dòng), `launcher_test.py` `a9b0494b…f6ab` (9665 dòng) = §4, `cmp` BẰNG bản của rig r13; 54/54 neo đúng một lần. `git diff --no-index --numstat` so nền: `launcher.py` +21 / −5; `launcher_test.py` chỉ B8 +358 / −2, B8 và helper +1096 / −2, đủ +1312 / −2 ⇒ **+1333 / −7**. `cand_a`, `cand_b` của rig lượt 12: `launcher.py` +19 / −5 và +27 / −13 | 04:32:56Z; `cand_a`, `cand_b` giữa 04:43:09Z và 04:46:17Z (lệnh không in giờ) |
| 4 | phần đặc (cách đếm của bảng 15 dòng 5) | khối B8 353 = 42 + 9 + 30 + **272**; helper r9 737 = 100 + 11 + 14 + **612**; helper của ứng viên độc lập lượt 13 532 = 86 + 9 + 27 + **410**; dòng thêm của `launcher.py` tham chiếu 21 = 4 chú thích + **17**, 0 trống; 54 mục `DOT_BIEN` tham chiếu: 216 dòng, 0 trống, 0 chú thích; `_con_song_that`: 2 dòng mã ⇒ 272 + 612 + 17 + 216 + 2 = **1 119** | sau 04:32:56Z (lệnh không in giờ) |
| 5 | ứng viên độc lập của cross-review lượt 13 (đọc) | `launcher.py` `12b09aa3…bfbc` +27 / −5, trong đó 10 dòng chú thích, 0 trống; `launcher_test.py` `02ff1fb5…ca99` +1108 / −2 theo bốn hunk: +1 (`import errno`), +2 / −2 (`_con_song_that`), +889 (khối B8 353, helper 532, 4 dòng trống nối), +216 (54 mục `DOT_BIEN`) ⇒ **+1135 / −7**. Log lượt 13 (đọc): chốt tĩnh ĐẠT ở 3.11 và 3.13 (log/03); sáu ca QUA và nền ĐỎ 6/6 ở 3.12 (log/05, 06); phép D tối giản 56 + 1 đơn vị đúng thứ tự, không control, không phép đảo, log không ghi bản Python (log/07); A/W 55/55 ở 3.12 và 3.11 (log/09, 20); `--dot-bien` 230/230 ở 3.12 và 3.11 (log/08, 21); B6 delta 0 ở 3.11 và 3.12 (log/13) | sau 04:32:56Z (lệnh không in giờ) |
| 6 | sáu ca mới và số đếm (ứng viên tham chiếu) | `python3.12 launcher_test.py --lap-ca tNNN --lan 1` từng ca, bọc subreaper: ứng viên QUA 6/6; nền (`launcher.py` nền, cùng tệp test) ĐỎ 6/6 đúng loại — `B1 seam escaped`, `B3b-giet-cay seam escaped`, `B8-sau-sinh 124 noi doi`, `B8-luc-sinh qua han khong giet duoc: rc=10`, `B8-setsid 124 noi doi`, `B8-me-thoat 124 noi doi`; 0 tiến trình còn lại sau mỗi lượt. Nạp module (`python3.12`): 195 ca, `DOT_BIEN` 228, harness 3, `DANG_DOC_QA7` dạng latin-1 | 04:46:17Z–04:46:52Z |
| 7 | `--dot-bien` trên ứng viên tham chiếu (r13: CHƯA ĐO) | `python3.12`: `DOT BIEN: 230/230 dat (1 khong do duoc tren nen nay)`, rc=0, 41,3 s; `python3.11`: cùng dòng, rc=0, 37,4 s. Ở cả hai: 54 mục `wp685_*` `OK giet 1/1` ((c) `2/2`), tên ca trần, 0 dòng mới có kiểu ngoại lệ trong ngoặc; bộ bọc: 0 mồ côi còn sống phải giết, 0 tiến trình còn lại | 04:33:54Z; 04:34:35Z |
| 8 | phép D trên ứng viên tham chiếu (r13: CHƯA ĐO) | tập lệnh rig r14 cho API của helper r9 — control đặt bằng ba công tắc test-only có sẵn của helper (mặc định NỚI, bỏ một đầu vào, đảo thứ tự hai nhãn), gán lúc chạy trong tiến trình đo, không sửa mã sản phẩm; 57 đơn vị và thứ tự CHÉP từ bảng tiểu nhãn và "Thứ tự thực thi cố định" ở §7, không lấy từ helper. `python3.12` và `python3.11`: bản đúng XANH (`t156` 56 đơn vị, `t157` 1, 404 lần `bang`); **65/65 control** đỏ, mỗi cái báo đúng đơn vị thiếu; control RỖNG (bỏ một đơn vị không tồn tại) xanh, tức bị đánh "không đỏ đúng" như thiết kế; **6/6 phép đảo** `missing=[]`, `order=False`; rc=0 | 04:36:48Z; 04:37:06Z |
| 9 | A/W 55 cặp trên ứng viên tham chiếu (r13: CHƯA ĐO) | tập lệnh rig r14, mỗi cặp một tiến trình; bảng (nhãn, tiểu nhãn, loại) CHÉP từ lời văn B5 (a)–(m) (loại chỉ ở (k5), (l1)–(l29), (m1)–(m5)); bản đột biến dựng từ chính 54 mục `wp685_*` của ứng viên. `python3.12` và `python3.11`: **55/55 chấp nhận**, 0 ĐỎ, 0 `CHƯA CÓ CHỐT NGƯỢC`; A1 báo ở nhãn đứng TRƯỚC (hợp lệ) đúng năm dòng như ứng viên độc lập lượt 13 — (c) `B2-eacces read count 0`, (j1) `B2-eacces read count 2`, (j2) `B2-doc-hong EACCES read count 2`, (k1) `B2-doc-hong EACCES kill count 0`, (k5) `B2-doc-hong EACCES kill count 2`. Răng của bộ xét (3.12): bản không đột biến ⇒ ĐỎ (A1, W1 sống); (a) với nhãn sai `B3-song` ⇒ ĐỎ; (l1) với loại sai ⇒ ĐỎ; (d2) với tiểu nhãn sai ⇒ ĐỎ; (m5) với nhãn đứng TRƯỚC đích ⇒ ĐỎ. Một đối chứng đặt sai chỗ: (a) với nhãn `B2-eio` ⇒ chấp nhận — bản gỡ vá để EIO của phép hỏi thoát nên chết THẬT ở `B2-eio`; không phải bộ xét mù | 04:37:33Z; 04:38:03Z; đối chứng sau 04:38:29Z (lệnh không in giờ) |
| 10 | chốt tĩnh và mục 5 bảng bất khả thi, trên ứng viên thứ hai | `chot_tinh_r12.py` trích bằng máy từ tệp r14 theo luật ở B2: 412 dòng, `add42b31…35b6`, `cmp` BẰNG bản rig r13. `python3.11`: ứng viên tham chiếu ĐẠT rc=0. Bảy biến thể MỘT vị trí của `_con_song` (mỗi neo đúng một lần) — `except (OSError, MemoryError)` ở tầng hỏi; hỏi lại khi `InterruptedError`; `TimeoutError` riêng ⇒ `True` ở Đ0: ĐỎ rc=1, `T3 _con_song: ten toan cuc ngoai danh sach <tên>` ở cả ba; `except (OSError, subprocess.SubprocessError)` ở tầng hỏi; hỏi lại khi `InterruptedError` nêu GIÁN TIẾP (`[os][0].sys.modules["builtins"].InterruptedError`); hỏi lại khi `e.errno == 4`; `e.errno == 12` ⇒ `True` ở khối kill (ứng viên này dùng chung khối ấy cho K và K0): ĐẠT rc=0 cả bốn. Cả bảy QUA `t156`, `t157`, `t160`, `t161` (`python3.12`, bọc subreaper); đối chứng: bản `wp685_a` ĐỎ `t156` `B1 seam escaped` | chốt tĩnh 04:40:02Z–04:40:20Z; bốn ca 04:40:31Z–04:41:14Z |
| 11 | tập tên mà `T3`, `T6` cho phép trong `_con_song` và `def` mới | `symtable` như script, trên `launcher.py` nền, `python3.11` và `python3.13` như nhau: 17 tên (11 tên toàn cục của `_con_song` nền cộng 6 tên thêm), trong đó 6 lớp ngoại lệ — `IndexError`, `OSError`, `PermissionError`, `ProcessLookupError`, `UnicodeDecodeError`, `ValueError`; 4 cặp `T6` — `os.kill`, `platform.system`, `subprocess.SubprocessError`, `subprocess.run` — trong đó 1 lớp ngoại lệ. Tập lớp nêu TRỰC TIẾP được: 7 | sau 04:41:14Z (lệnh không in giờ) |
| 12 | nền | `git ls-remote origin refs/heads/master` ⇒ `20ec8d5d…5961`; đối tượng cục bộ của worktree, không fetch: `fc852ff` và `423b4ba` là tổ tiên của `20ec8d5` (rc=0; 22 và 51 commit), write set rc=0 từ cả hai, `.claude .github` rỗng; `fc852ff..20ec8d5` đổi đúng hai tệp ngoài write set (`ops/land/pr684-wp677-land-evidence.yaml` mới +256; `ops/lease_publish_test.py` +600 / −15, có hunk trong thân `t154`); `da119d7` KHÔNG là tổ tiên (rc=1) | 04:41:44Z |
| 13 | các lời khai khác của §4 | ADR-0044 trên `423b4ba` và `20ec8d5`: packet `sensitive` chạm authority "≤ 3 tệp và ≤ 300 dòng thêm", vượt thì dừng TRƯỚC review hoặc khai lý do trong spec; protocol: dòng ADR-0044 của bảng §20 ghi "**0 cổng**" (`20ec8d5`), §8, đoạn patch-as-hint cho packet `sensitive`, dòng 604–605 (`423b4ba`): "authority/gate/runtime … launcher" bị loại trừ tường minh; `soan-spec` §3 "Đo trước khi hỏi" có "kích thước dự kiến" (`423b4ba`, `20ec8d5`); `0044` xuất hiện 0 lần ở r1 đến r12 và ở VERDICT, HINT lượt 1 đến 11 (lượt 12: 26 DÒNG theo `grep -c` — VERDICT 22, HINT 4 —, tức 32 LẦN theo `grep -o` — 27 và 5; r15 sửa đơn vị, cross-review lượt 14). Hai comment quyết định: câu hỏi, nhãn chọn và không chọn, mô tả kèm — nguyên văn có trong thân; sha256 thân `d537d59e…c26d` và `32707eed…f53c` khớp §4 — đo trên tệp REST mà rig r13 lưu (15 comment), KHÔNG đọc lại GitHub; thân `5922387653` ghi phạm vi "chỉ áp cho wp685, từ r13 trở đi" dưới nhãn "diễn giải của phiên agent, không phải lời chủ kho" | sau 04:41:44Z (lệnh không in giờ) |
| 14 | nhãn lúc đóng băng — `kiem_nhan_r12.py` (trích bằng máy từ r14, `13f7728d…3b45`, `cmp` BẰNG bản rig r13) trên chính tệp r14 | 44 nhãn (`grep -o` cũng 44: không nhãn nào gãy dòng), 0 sai dạng, rc=0, ở `python3.11`, `python3.12`, `python3.13`; r13: 40; bản gộp HINT lượt 13: 42 (đo cùng lượt). Từ bản gộp sang r14, so từng ngữ cảnh: bốn nhãn giữ nguyên lý do, chỉ đổi câu quanh nó; thêm hai nhãn, cả hai "(lý do 4)" cho câu hỏi `stat` thật có bao giờ ném `subprocess.SubprocessError` — một ở mục 5 B2, một ở bảng "Thay đổi so với r13". Đối chứng trên bản sao r14: xoá lý do ngay sau nhãn errno của mục 5 ⇒ rc=1 đúng một chỗ; thêm một nhãn không lý do gãy qua hai dòng ⇒ rc=1 đúng một chỗ (45 nhãn) | 04:59:15Z; chạy lại sau lần sửa cuối |
| 15 | băm lúc đóng băng | `VERDICT.md`, `HINT.patch`: khớp dòng 1; r1 đến r13: tiền tố sha256 của cả 13 tệp có trong đầu tệp này (13/13), và `git diff --quiet HEAD --` mười ba tệp ⇒ rc=0 (không đổi byte nào so commit `da119d7`). Ba khối mã thuần trích bằng máy từ tệp r14 bằng CẢ bộ trích của rig r13 lẫn của rig lượt 13: `chot_tinh_r12.py` 412 dòng `add42b31…35b6`, khối B8 353 dòng `60ee8d5f…75ff`, `kiem_nhan_r12.py` 19 dòng `13f7728d…3b45` — trùng số ghi trong tệp; neo của khối B8 xuất hiện đúng một lần. Lượt trích đầu ra SAI: câu §4 mà phiên soạn r14 vừa viết chép nguyên văn neo ấy, tạo một lần xuất hiện ĐỨNG TRƯỚC B8, nên bộ trích (lấy lần đầu) trả khối chốt tĩnh thay cho khối B8 — sửa câu §4, đo lại | 05:00:21Z; trích: lượt sai 05:01:07Z, chạy lại sau lần sửa cuối |
| 16 | vệ sinh | zombie toàn máy 0 trên 89 tiến trình; 0 tiến trình mang đường dẫn rig r14 ngoài chính lệnh kiểm; các lượt có bọc: 0 tiến trình còn lại sau lượt; `git status --short` chỉ có tệp r14, HEAD `da119d7` | 05:00:21Z |

**Đính chính lời khai của chính phiên soạn — hai lần, cùng hình dạng.** Lần một (r1 §1): bản vá đăng ở
PR #679 comment `5885963131` và thân #685 là bản **RỘNG**; nó đóng ESRCH nhưng biến một
`PermissionError` trên PID **đang sống** thành "đã chết" — đúng lớp lời khai sai *"trả 124 khi tiến
trình còn sống"* mà CLAUDE.md đã trả giá. Lần hai (r2): bản **HẸP** r1 chữa lỗi ấy rồi mở lỗ ở chiều
kia — `kill(pid, 0)` THÀNH CÔNG với zombie, nên bản HẸP báo "còn sống" cho cây đã chết và deadline
trả 125 thay vì 124. Chính r1 §7 B3 chỉ đo PID **đã `wait`**, tức đo đúng chỗ không có zombie. Cross-review
lượt 1 bắt được điều này bằng phép đo (VERDICT hướng 3), không phải bằng đọc.

## 2. Phạm vi đã đo (grep + đọc luồng trên `89fc4fa`)

- Trong `launcher.py` chỉ **một** lời gọi `.exists()` trên đường `/proc`: `:651`.
- Ba chỗ đọc `/proc` khác đều nằm trong `try` bắt `OSError`: `:359` (`_khoa_danh_tinh`, một
  `read_text`), `:430` và `:484` (mỗi chỗ một `iterdir`; phép đọc `stat` bên trong ở `:436` và
  `:490` cũng có `try`). Không cùng HÌNH lỗi (không ngoại lệ nào thoát) nhưng cùng NGHĨA "đọc lỗi ⇒ coi như đã
  chết" (r8, đo ở gạch đầu dòng dưới). **(r9) Chủ kho đã trả lời §11.1: SỬA ở packet này** — chỉ phần giải mã
  (Q-A.7); phạm vi bắt của các `try` ấy giữ nguyên.
- Nhánh hiện có ngay dưới `:651`: khi `exists()` trả `True` mà `read_text` ném `OSError`,
  `ValueError` hoặc `IndexError` (`:655`), hàm trả `False`. Đó là hành vi CŨ (cross-review lượt 1,
  hướng 7: nó bỏ PID khi `read_text` bị EACCES). Packet này **không** đổi kết quả, phạm vi bắt hay số lần
  của nhánh ấy (Q-A.3); (r9) chỉ đổi CÁCH GIẢI MÃ của phép đọc (Q-A.7). **Quan sát mới của r3** (đo 11:46:40Z
  29-09, Python 3.12.3, `launcher.py` của `89fc4fa`, không seam): một tiến trình ĐANG SỐNG mà `comm` chứa byte
  không phải UTF-8 (con tự đặt bằng `prctl(PR_SET_NAME)`) làm `read_text` ném `UnicodeDecodeError`, và nhánh cũ
  trả `_con_song(pid)` = **`False`** trong khi `os.kill(pid, 0)` thành công. Tức nhánh cũ khai "đã chết" cho tiến
  trình còn sống. r3–r8 để ngoài phạm vi; **(r9) nay SỬA** theo quyết định chủ kho (§11.1): với Q-A.7 nội dung
  ấy đọc được, nên `B2-nhanh-cu utf8-hong-that` đòi `True`. Đọc lỗi THẬT (`OSError`) ở nhánh cũ vẫn ⇒ `False` như
  nền (Q-A.3). Tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC (lý do 4).
  **Đo thêm ở cross-review lượt 7 (ba Python; r8 ghi "ngoài phạm vi" — r9: TRONG phạm vi, §11.1).** (i) Kích hoạt THẬT, không cần `prctl`: kernel cắt `comm` ở 15 byte, nên một chương trình tên tiếng
  Việt — ví dụ `kiểm_tra_tiến_trình.sh` — có `comm` là UTF-8 bị cắt giữa ký tự; `read_text` thật ném
  `UnicodeDecodeError`, và `_con_song` = `False` cho tiến trình ĐANG SỐNG ở nền lẫn ứng viên nháp. (ii) Cùng lớp đi
  tới 124: `_khoa_danh_tinh` (`:359`) trả `None` và `_thanh_vien_nhom` (`:436`) bỏ qua tiến trình khi phép đọc lỗi,
  nên `_giet_cay` vào nhánh "tiến trình đã biến mất" (`:896–920`) và trả `tron_ven=True`. Đầu-cuối (3.12.3): `launcher.py
  run --deadline-utc` trên một con đổi `comm` như thế SAU lúc sinh (đo bằng `prctl`; một wrapper exec chương trình
  tên tiếng Việt cho cùng `comm` hỏng, như (i)) ⇒ **rc=124**, `ly_do_dung='qua han: tien trinh da khong con chay'`,
  `giet_tron_ven=True`, trong khi con VẪN SỐNG và chưa nhận tín hiệu nào — ở nền và ở ứng viên nháp như nhau
  (phiên soạn r8 chạy lại tập lệnh ấy: cùng kết quả, bảng 10 dòng 10; r9: `t158` trên nền, bảng 11). Nếu `comm` đã
  hỏng ngay lúc sinh thì `khoa=None` và lượt chạy trả rc=10 ("tu choi giet"), con cũng còn sống. Vậy câu
  "không cùng dạng lỗi" của r7 đúng về HÌNH (không ngoại lệ nào thoát) mà không đúng về NGHĨA: `:359` và
  `:436`/`:490` cùng lớp "đọc lỗi ⇒ coi như đã chết" mà objective cấm cho `_con_song`, và nó đi tới đúng mã 124 mà
  B3b khoá. Bản vá ESRCH không gây ra nó (nền cho cùng kết quả). **(r9) Chủ kho đã trả lời §11.1: sửa ở packet
  này** (Q-A.7, B8; write set không đổi). Đo thêm ở cross-review lượt 8 (3.11.15 / 3.12.3 / 3.13.12): (iii) `stop` trên
  con đổi `comm` sau lúc sinh ⇒ rc=0 "tien trinh da khong con chay" trong khi con vẫn ghi nhịp (+9–10 byte trong 1 s; ba
  Python, nền và ứng viên theo r8 như nhau; bản nháp Q-A.7: rc=0 "SIGTERM: cay da sach", con đã chết) — `stop` trả 0
  đúng khi `_giet_cay` báo `tron_ven`, nên hai đầu vào `_giet_cay` trực tiếp của B8 phủ nó;
  (iv) locale ASCII (`PYTHONUTF8=0 PYTHONCOERCECLOCALE=0 LC_ALL=C`) với `comm` UTF-8 HỢP LỆ `tệp_ổn` (10 byte, không bị
  cắt) ⇒ `_khoa_danh_tinh` `None`, `_con_song` `False`, quét nhóm và ảnh chụp không thấy tiến trình — kích hoạt không chỉ
  là tên bị cắt; (v) `launcher_test._con_song_that`, phép kiểm sống ĐỘC LẬP của bộ test, cùng khuôn `read_text()`, cũng
  trả `False` cho tiến trình ấy; (vi) tên chương trình tiếng Việt (exec qua symlink `kiểm_tra_tiến_trình`) cho ĐÚNG 15
  byte `comm` hỏng ngay lúc sinh, không cần `prctl` (ba Python).
- `_con_song` có năm nơi gọi trong `launcher.py`: `:607` (`_con_song_dung_khoa`), `:857` và `:882`
  (`_giet_windows`, tức nhánh Windows), `:1020` và `:1039` (`_giet_cay`). Đo bằng AST (lần lên cây
  cha tới hàm bao, 10:2xZ 29-09; cross-review lượt 1 đo lại độc lập ra đúng năm nơi, 10:52Z):
  **không** lời gọi nào nằm trong thân một `try` bao ngoài, nên `ProcessLookupError` từ `:651` thoát
  thẳng khỏi các hàm ấy.
- Executor phải **grep lại** trên nền tiếp nối trước khi sửa và khai mọi chỗ mới tìm thấy.

## 3. Quyết định

- **Q-A — ngữ nghĩa bản vá.** Q-A.1–6 là **suy luận của phiên soạn** (từ docstring của `_con_song`, từ bài học
  124/125 và bài học zombie trong CLAUDE.md, và từ VERDICT lượt 1 và lượt 2); **KHÔNG phải quyết định chủ kho**. r2
  sửa Q-A của r1 theo lượt 1; r3 đến r8 KHÔNG đổi ngữ nghĩa Q-A.1–6, chỉ viết tường minh điều đã hàm ý — mỗi lần
  làm rõ ghi tại chỗ kèm revision; danh sách từng lần: đoạn này của r8 (sha256 `2ae6ee04…2aa3`). **r9 ĐỔI ngữ
  nghĩa ở đúng một trục — cách giải mã phép đọc `/proc/<pid>/stat` —** theo quyết định chủ kho (§11.1): mệnh đề r8
  ở Q-A.3 và Q-A.4 bị THAY, và thêm Q-A.7. PHẠM VI sửa là quyết định chủ kho; DẠNG sửa (hai dạng đọc cho phép) là
  suy luận của phiên soạn, đo ở bảng 11. Chủ kho có thể bác bằng revision mới. Hợp đồng, bằng lời:
  1. Phép hỏi `stat`/`exists` trên `/proc/<pid>/stat` được thực hiện **đúng một lần** mỗi lời gọi
     `_con_song`, và không thử lại.
  2. `ProcessLookupError` ở phép hỏi ấy ⇒ trả `False` (tiến trình đã biến mất).
  3. Phép hỏi không ném lỗi ⇒ hai nhánh sẵn có giữ **nguyên xi**: tệp có ⇒ đọc trạng thái (kể cả
     hành vi cũ ở §2 khi đọc lỗi); tệp vắng ⇒ rơi về `os.kill(pid, 0)` như cũ. **(r7, cross-review lượt 6,
     không đổi ngữ nghĩa)** Điều khoản này nay có đầu vào riêng — nhãn `B2-nhanh-cu` ở §7: r6 không có đầu vào
     nào đi vào hai nhánh sẵn có với đọc lỗi/nội dung hỏng, hay với tệp vắng trên PID sống, nên bản vá đổi
     chúng qua hết nghiệm thu (đo được, xem `B2-nhanh-cu`). "Nguyên xi" gồm cả kết quả, phạm vi bắt và SỐ LẦN,
     đúng như mã nền `launcher.py:651–664` trên `89fc4fa`: nhánh tệp có đọc đúng một lần, không gọi `kill`, và bắt
     đúng ba nhóm `OSError`, `ValueError`, `IndexError` (⇒ `False`; ngoại lệ khác thoát nguyên); nhánh tệp vắng
     gọi `kill(pid, 0)` đúng một lần với ngữ nghĩa sẵn có của Q-A.4 (i), không đọc nội dung, và không thêm mệnh
     đề bắt nào (nhóm phân tích, `Exception`, `BaseException` ở đó thoát nguyên — cùng khối mã với tầng K).
     **(r9, ĐỔI ngữ nghĩa theo quyết định chủ kho — thay mệnh đề r8 cùng chỗ.)** "Nguyên xi" KHÔNG còn gồm cách
     giải mã: phép đọc của nhánh tệp có tuân Q-A.7; mọi phần khác của điều khoản này giữ nguyên (kết quả, phạm vi bắt
     ba nhóm, số lần). Lý do đo được (cross-review lượt 8, ba Python): mệnh đề r8 "`read_text()` không đối số" GIỮ
     `_con_song` = `False` cho tiến trình SỐNG có `comm` không giải mã được, và qua `_con_song_dung_khoa` →
     `_giet_rieng`/`_con_lai` điều đó làm `_giet_cay` bỏ qua cháu `setsid` rồi báo "SIGTERM: cay da sach" — 124 khi
     cháu còn sống (B8, đột biến M4). Mệnh đề r8 nguyên văn: Q-A.3 của r8 (sha256 `2ae6ee04…2aa3`).
  4. `OSError` khác (EACCES, EIO, …) ⇒ **không** kết luận. Không stat được chưa có nghĩa là không đọc
     được. Trước hết **thử đọc nội dung** `/proc/<pid>/stat`: đọc được và trạng thái là `Z` ⇒ `False`;
     đọc được và không phải `Z` ⇒ `True`. Không đọc được (mọi `OSError`, hoặc nội dung không phân tích
     được) ⇒ rơi về `os.kill(pid, 0)` với ngữ nghĩa sẵn có (`PermissionError` ⇒ `True`,
     `ProcessLookupError` ⇒ `False`). Bước đọc này cũng chỉ làm **một lần**. **Làm rõ (r4, không đổi
     ngữ nghĩa):** `ProcessLookupError` (ESRCH) do chính phép ĐỌC ném ra cũng thuộc "mọi `OSError`" ⇒
     rơi về `os.kill(pid, 0)` và trả `True` cho PID sống; nó KHÔNG được đọc thành "tiến trình đã biến mất"
     như ESRCH của phép HỎI ở bước 2. Chỉ `os.kill(pid, 0)` mới quyết định sống hay chết ở đường này. **Làm rõ (r5, không đổi ngữ
     nghĩa):** (i) "ngữ nghĩa sẵn có" là khối `os.kill(pid, 0)` của nền (`launcher.py:657–664` trên `89fc4fa`):
     `ProcessLookupError` ⇒ `False`, `PermissionError` ⇒ `True`, `OSError` khác (ví dụ EIO) ⇒ `False`, không
     lỗi ⇒ đi tiếp như cũ; (ii) hệ quả của "chỉ `os.kill(pid, 0)` mới quyết định" là đường lỗi đọc và đường nội
     dung hỏng phải THỰC SỰ gọi nó (đúng một lần) và trả đúng kết quả của nó — trả `True` ngay, hoặc gọi nó
     rồi bỏ kết quả, đều là vi phạm, kể cả khi PID đang xét là PID sống nên `True` trùng kết quả đúng.
     **Làm rõ (r6, không đổi ngữ nghĩa):** (i) "`OSError` khác (EACCES, EIO, …)" là một LỚP ngoại lệ, không phải
     danh sách trắng errno: mọi `OSError` không phải `ProcessLookupError` ở phép hỏi đều đi vào bước đọc, dù
     mang errno nào (kể cả EPERM); bản vá phân nhánh theo errno, hoặc chỉ nhận một tập errno hữu hạn, là vi
     phạm; (ii) đường lỗi mới KHÔNG được thêm mệnh đề bắt nào ở bước `kill(pid, 0)` ngoài ba mệnh đề của khối
     nền (`ProcessLookupError`, `PermissionError`, `OSError`); ngoại lệ ngoài họ `OSError` do bước này ném
     ra (nhóm phân tích, `Exception` khác, `BaseException` khác) thoát nguyên đối tượng, không bị bắt và không
     bị bọc lại thành đối tượng khác (`raise … from …`).
     **(r9, ĐỔI — thay mệnh đề r8 cùng chỗ.)** Phép đọc của bước 4 tuân Q-A.7; nội dung THẬT có `comm` không phải
     UTF-8 là ĐỌC ĐƯỢC, không phải "không phân tích được": trạng thái `Z` ⇒ `False`, khác `Z` ⇒ `True`, không gọi kill.
     Mệnh đề r8 ("`read_text()` không đối số; lỗi giải mã ⇒ rơi về kill") trái vế zombie của objective: lượt 8 đo zombie
     `comm` hỏng + seam EACCES ở `stat` ⇒ ứng viên theo r8 `_con_song` = `True` (vì `kill(zombie, 0)` thành công), bản
     giải mã bền `False` (ba Python).
  5. Phạm vi bắt, **theo từng tầng** (r3 viết lại cho rõ theo lớp `ma-tran-loi-thieu-chot`; r2 chỉ nói
     "họ `OSError`" và để hở chỗ nội dung hỏng ở bước 4). Từ r6 có **ba tầng** (H, Đ, K) của đường mới; từ r7
     bảng không gian mở rộng ở §7 B2 thêm hai tầng Đ0, K0 của hai nhánh sẵn có (Q-A.3) và liệt kê từng ô của cả năm;
     câu chữ dưới đây là hợp đồng, bảng là danh sách kiểm:
     · **Tầng hỏi** (H; `stat`/`exists`): chỉ bắt họ `OSError`. Mọi ngoại lệ khác thoát ra nguyên đối
       tượng — cả ngoại lệ thuộc `Exception` nhưng không thuộc `OSError` (ví dụ `RuntimeError`) lẫn
       ngoại lệ thuộc `BaseException` nhưng không thuộc `Exception` (ví dụ `KeyboardInterrupt`), và cả
       nhóm lỗi phân tích (`ValueError`, `UnicodeDecodeError`, `IndexError`): nhóm này chỉ được bắt cục bộ ở
       tầng đọc và KHÔNG được đưa vào nhóm bắt của phép hỏi (lượt 5 đo được bản làm vậy qua toàn bộ nghiệm
       thu của r5). Ranh giới là ngoại lệ THOÁT KHỎI phép hỏi vào mã launcher: `Path.exists()` tự nuốt
       `ValueError` (kể cả `UnicodeDecodeError`, con của nó) phát sinh bên trong `stat` — đo trên ba bản
       Python (§1 bảng 7) — nên không đòi launcher phục hồi một ngoại lệ thư viện đã nuốt; còn `IndexError` từ
       `stat` thoát qua `exists()` nguyên vẹn, và mọi ngoại lệ ném thẳng từ `exists()` thoát nguyên. Vì vậy
       nhóm phân tích ở tầng hỏi được đo bằng seam đặt ở `Path.exists`, không phải `Path.stat` (B2,
       `B2-thoat-parse`).
     · **Tầng đọc** (Đ; bước 4): bắt `OSError` của phép đọc, và các lỗi **phân tích cục bộ** của nội dung
       đọc được (`ValueError` — kể cả `UnicodeDecodeError`, là con của nó — và `IndexError`); phần bọc
       chỉ gồm đúng phép đọc và biểu thức tách trạng thái, không bọc thêm gì, và tuyệt đối không bọc
       phép hỏi hay bước `kill`. Nhận diện "không phân tích được" bằng kiểm tra dữ liệu thay cho bắt ngoại
       lệ cũng được; Q-A không quy định cách — nhưng kiểm tra dữ liệu phải nhận ra MỌI dạng nội dung hỏng ở
       bảng 4, không chỉ một dạng (bản chỉ nhận ra chuỗi rỗng là vi phạm, B5 dòng (l16)). Ngoại lệ ngoài hai
       nhóm ấy (ví dụ `RuntimeError`, `KeyboardInterrupt`) thoát ra nguyên đối tượng.
     · **Tầng kill** (K; bước `os.kill(pid, 0)` mà đường lỗi rơi vào): chỉ ba mệnh đề của khối nền, với ngữ
       nghĩa ở Q-A.4 (r5 và r6 làm rõ); mọi ngoại lệ khác thoát nguyên đối tượng.
     · Bản vá KHÔNG được dùng `except Exception` hay `except BaseException` ở cả ba tầng, và KHÔNG được bọc lại
       ngoại lệ thoát ra thành đối tượng khác. Ngoại lệ `OSError` thoát ra khỏi đường lỗi mới là vi phạm
       objective.
  6. Nhánh Windows và Darwin, thứ tự các nhánh khác: không đổi.
  7. **(r9) Giải mã bền ở CẢ NĂM chỗ đọc `/proc/<pid>/stat`** — `_khoa_danh_tinh` (`:359`), `_thanh_vien_nhom`
     (`:436`), `_chup_cay` (`:490`) và hai khối đọc của `_con_song` (nhánh tệp có; đường lỗi mới). Phép đọc là MỘT
     trong hai dạng, executor chọn, khai trong handoff và trong MỘT hằng `DANG_DOC_QA7` của `launcher_test.py` (tên
     phương thức `Path`, args, kwargs — helper và B8 dùng chung): `read_bytes()` rồi tách trên bytes (các trường số giải
     mã ASCII), hoặc `read_text(encoding="latin-1")` (song ánh byte ↔ ký tự). Cả hai không phụ thuộc locale và không bao
     giờ ném `UnicodeDecodeError`. Vi phạm: `read_text()` không đối số (phụ thuộc locale — đo: locale ASCII làm cả `comm`
     UTF-8 hợp lệ nổ), mọi `encoding=` khác (đo: `cp1252` ném ở byte 0x81), và mọi `errors=`. Nói cho đúng: `errors=
     "replace"` hay `"surrogateescape"` KHÔNG sai hành vi ở locale tương thích ASCII (đo lượt 8: không ném, tách đúng,
     trên `comm` hỏng lẫn `comm` UTF-8 hợp lệ, ở locale UTF-8 và `LC_ALL=C`, ba Python); chúng bị loại để dạng đọc là
     danh sách cho phép ĐÓNG, kiểm được bằng `read args`, và không phụ thuộc locale theo cấu trúc — muốn nhận thì mở
     rộng danh sách và khai. **Định dạng khoá có CHỐT (r10, cross-review lượt 9, lớp `khoa-dinh-dang-khong-co-chot`).**
     Khoá danh tính Linux là `linux:` ghép chuỗi thập phân ASCII của trường 22 (`starttime`) — đúng như nền; dạng bytes
     phải giải mã ASCII trường ấy TRƯỚC khi ghép. Trên nền `423b4ba` khoá Linux được dựng ở ĐÚNG hai chỗ (`git grep`
     chuỗi `linux:` trong `launcher.py`): `:362` (`_khoa_danh_tinh`) và `:494` (`_chup_cay`); nhánh Darwin, Windows
     (`darwin:`, `win:`) ngoài phạm vi (Q-A.6). Ứng viên thêm chỗ dựng khoá thì khai trong handoff, và chỗ ấy cũng theo
     định dạng này. Ca bắt, theo tổ hợp: lệch ở MỘT chỗ ⇒ khoá lệch nội bộ ⇒ `t160`/`t161` đỏ; lệch ở CẢ HAI chỗ (nhất
     quán nội bộ, ví dụ `linux:b'…'`) ⇒ `t160`, `t161` lấy khoá của mẹ bằng phép đọc BYTES độc lập theo định dạng nền
     (`_k124_khoa_that`, đúng tình huống sổ `run.json` do một bản launcher khác ghi) ⇒ `_giet_cay` từ chối (khoá KHÁC) ⇒
     `t160` đỏ `khong giet duoc`; biến thể (E) `g_to_hop_dinh_dang_khoa`. Đo ba tổ hợp trên khối r10: bảng 12. Lý do
     đo được (VERDICT lượt 9, sha256 `0f1b3bdc…ddfa`): bản bytes lệch cả hai chỗ QUA bốn ca B8 của r9 và toàn suite,
     còn `stop` xuyên phiên bản trả rc=10 "khoa danh tinh KHAC" và để con SỐNG. Phạm vi bắt, số lần hỏi/đọc/kill và mọi
     hành vi khác của bốn hàm không đổi. Khoá bằng B8 (bốn ca; `t160`, `t161` còn đòi `read args` trên MỌI lời đọc
     `/proc/<pid>/stat` trong cửa sổ quanh `_giet_cay`, tức cả bốn hàm), bằng hai đầu vào nội dung thật,
     và bằng loại `read args` của helper (quy ước chung, "Seam thay CẢ lời gọi").
     **Phép tách, API đọc và phần còn lại của ba hàm ngoài có CHỐT (r11, cross-review lượt 10, lớp
     `ma-tran-loi-thieu-chot`).** r11 TỰ LIỆT KÊ đường vào của hai trục còn thiếu ở CẢ năm chỗ đọc trước khi vá — bảng
     "Năm chỗ đọc × hai trục" ở B2 là danh sách có thẩm quyền, mỗi ô một đầu vào, một chốt, một tên (E), một số đo.
     (i) Phép tách: tách trường theo dấu `)` CUỐI như nền (dạng bytes: `rindex(b")")`). Hai đường sai: tách theo `)`
     ĐẦU (`index`, `find`, `partition(b") ")`, `split(b")", 1)`, biểu thức chính quy không tham lam) và tách cả dòng
     theo khoảng trắng (`split()[k]`) — cả hai lệch trường khi `comm` chứa `) ` hay khoảng trắng (tên thật kiểu
     `tep (1).sh`). (ii) API: danh sách cho phép đóng ở MỌI API — trong bốn hàm, nội dung `/proc/<pid>/stat` chỉ được
     đọc bằng đúng lời gọi `Path` của `DANG_DOC_QA7` trên đúng đường `/proc/<pid>/stat`; `open()`, `io.open`,
     `Path.open()`, `os.open`, đường `/proc/<pid>/task/…`, `dir_fd`, tiến trình con, fd mở từ trước đều là vi phạm như
     một `encoding=` lạ. (iii) Phần còn lại của ba hàm ngoài — phạm vi bắt, vòng lặp, số lần đọc, decorator, docstring,
     mọi câu không thuộc phép đọc — giữ nguyên so nền THEO AST (r12; r11 viết "TỪNG BYTE" và so ký tự từng dòng); chú
     thích `#` không vào AST nên đặt ở đâu cũng được. Khoá bằng chốt tĩnh ở B2, vì hai trục động không phủ hết: sự kiện
     `open` không thấy fd mở trước cửa sổ, thước đo `open` bỏ đường tuyệt đối không bắt đầu bằng `/proc/` (`SL2_khoa`,
     bảng 13), và không đầu vào nào đo phạm vi bắt hay số lần đọc của ba hàm này. (iv) (r12, cross-review lượt 11, lớp
     `chot-tinh-bien-chua-khep`) Ngoài bốn hàm `_con_song`, `_khoa_danh_tinh`, `_thanh_vien_nhom`, `_chup_cay`, tệp
     `launcher.py` không đổi so nền theo AST, trừ giá trị chuỗi của `VERSION` (`git log -G'^VERSION = '` trên tệp
     ra 8 commit: commit tạo tệp và 7 lần đổi giá trị); chỉ được THÊM câu `def` mức module mang tên mới làm hàm trợ
     giúp của `_con_song`; `_con_song` và các `def` mới theo danh sách cho phép T1–T7 của chốt tĩnh (B2). Lý do đo được: decorator và phép gán lại tên ở mức
     module đổi hành vi ba hàm ngoài mà không chạm dòng nào trong thân (VERDICT lượt 11, `DECO_khoa`, `REBIND2_nhom`
     QUA bốn ca B8), và mọi đường như thế nằm NGOÀI thân: liệt kê từng cách viết bị cấm là danh sách cấm, nên r12 liệt
     kê điều ĐƯỢC PHÉP thay vì điều bị cấm. (r13, cross-review lượt 12) Danh sách cho phép ấy khép ở mức MODULE
     (luật `M`, so AST nguyên câu); trong thân `_con_song` và `def` mới, T3 và T6 chỉ khép cách viết TRỰC TIẾP — thuộc
     tính trên một biến cục bộ hay một biểu thức không bị xét, xem "Giới hạn, khai thẳng" của chốt tĩnh ở B2.
     Chốt động: cháu của `t160`, `t161` mang `comm` `_K124_COMM_CHAU` (có `) ` và khoảng trắng); `read args` của B8 đòi
     không sự kiện audit `open` nào trên `/proc/…`, đường tương đối hay fd số xảy ra NGOÀI một lời đọc `Path` đã ghi; ở
     hai khối đọc của `_con_song` thêm seam của helper ("Seam thay CẢ lời gọi": đọc bằng đường khác thì seam không thấy,
     đếm đọc ra 0). Lý do đo được (VERDICT lượt 10, sha256 `88538f7c…85f8`, ba Python): với khối r10, chín biến thể
     tách theo `)` đầu và mười biến thể đọc qua `open()`/`Path.open()` QUA cả bốn ca B8, còn với `comm` có `) ` hay
     byte 0x81 chúng cho `124 noi doi` hay `khong giet duoc`. r11 đo thêm (bảng 13): đường khoảng trắng ở cả năm chỗ,
     API ở hai khối đọc của `_con_song`, đường `task` mà bộ lọc của HINT không thấy, tiến trình con. Biến thể (E):
     mục 6.

  **Hệ quả còn lại, khai thẳng:** nếu cả `stat` lẫn phép đọc nội dung đều không dùng được và PID là
  một zombie, hàm báo "còn sống" (vì `kill(pid, 0)` thành công với zombie), và deadline trả 125 thay
  vì 124. Đó là hướng fail-closed — khai "chưa giết được", không khai sai "đã giết" — và là đúng cái
  giá của lời hứa *"không tự khẳng định đã chết khi không có bằng chứng"*. Bảng 2 (cột 4) đo ra
  đúng như vậy. Nó là hành vi được chấp nhận của r2, không phải lỗi cần sửa ở đây.

  **Nội dung `/proc/<pid>/stat` hỏng — hai đường, hai kết quả, CÓ CHỦ Ý (r3 nói thẳng điều r2 chỉ để
  suy ra).** Hành vi mong đợi lấy đúng từ mã sẵn có, `launcher.py:652–656` trên `89fc4fa`: nhánh CŨ
  (phép hỏi thành công, tệp có) bọc phép đọc và biểu thức tách trạng thái trong một khối bắt `OSError`,
  `ValueError`, `IndexError` và trả **`False`**. Q-A.3 giữ nhánh ấy nguyên xi (§2). Nhánh MỚI (phép hỏi
  ném `OSError` khác ESRCH): nội dung đọc được nhưng không phân tích được ⇒ **rơi về `os.kill(pid, 0)`**
  như Q-A.4 đã viết, tức trả `True` cho PID sống, KHÔNG trả `False`. Hai đường lệch nhau về nội dung
  hỏng, và chính độ lệch ấy là chỗ một bản vá dùng chung MỘT khối bắt cho cả hai đường sẽ trượt sang
  `False` trên đường mới (đột biến (i) ở B5). Dạng nội dung "không phân tích được" đã đo (bảng 3):
  rỗng, và thiếu dấu đóng ngoặc ⇒ `ValueError`; hết chuỗi ngay sau dấu đóng ngoặc, có hoặc không có
  khoảng trắng cuối ⇒ `IndexError`; không giải mã được ⇒ `UnicodeDecodeError` (con của `ValueError`,
  KHÔNG thuộc `OSError`). Dạng thứ tư không phải suy diễn: `comm` của tiến trình đặt được bằng
  `prctl(PR_SET_NAME)` với byte không phải UTF-8, và khi đó `read_text` thật trên `/proc/<pid>/stat`
  ném đúng `UnicodeDecodeError` (bảng 4). (r9) Với Q-A.7, dạng thứ tư không còn xảy ra ở nội dung THẬT — nó chỉ
  còn là đầu vào seam (`p4`).
- **Mission #686 Q1:** ca khoá trong `.claude/dev/launcher_test.py`; xếp sau #668.
- **Lịch sử Mission #686 Q3 tại r18 (đã bị MCR-686-03 thay thế cho wp685 generation 2):** executor Google Antigravity / Gemini 3.1 Pro High; nguồn: #686 comment `5988699983`.
- **Mission #686 Q4:** không chạy CI Windows trên PR (không gắn nhãn `windows`, không gọi tay).
  `launcher-windows.yml` tự chạy ở `push` master với `paths: .claude/dev/**`, nên **lần merge là
  lần đo Windows đầu tiên** của bản vá; đọc kết quả ấy là một `land_obligation`.
- **Hệ quả của Q4 cộng chỉ thị thường trực "không chạy CI trên PR làm bằng chứng"** (nói thẳng,
  không che): trên PR thi hành, **không có lượt CI nào chạy `launcher_test.py`** — job `launcher` bị
  tắt trên PR không nhãn `windows` (Q4), và `gate-registry` không chạy tệp này (§8). Bằng chứng thay
  thế duy nhất trước merge là log cục bộ Linux ở B6, chạy trên `python3.11` (bản Ubuntu của `launcher-windows.yml`
  hậu-merge) và `python3.12` (bản của `ci.yml`); 3.13 trên Windows chỉ đo sau merge.

## 4. `write_set`

- `.claude/dev/launcher.py`
- `.claude/dev/launcher_test.py`

Không đường dẫn nào khác. Đặc tả này (`ops/specs/launcher-con-song-esrch-r26.md`) là hồ sơ của lượt
soạn, không thuộc write set thi hành.

**Kích thước thi hành — ADR-0044 (r13, cross-review lượt 12, lớp `kich-thuoc-thi-hanh-vuot-adr-0044`; r14 thu hẹp lời
khai theo cross-review lượt 13; NGOẠI LỆ do chủ kho duyệt).**
`docs/adr/0044-nguong-kich-thuoc-packet-theo-do-luong.md` (Accepted; bảng §20 của protocol: 0 cổng —
kỷ luật, không có máy canh): packet `sensitive` chạm authority ≤ 3 tệp và ≤ 300 dòng thêm theo `git diff --numstat`;
vượt một ngưỡng thì dừng TRƯỚC review để revision thiết kế, hoặc khai lý do trong spec. Launcher thuộc nhóm
authority/gate/runtime (protocol §8, đoạn patch-as-hint cho packet `sensitive`). `soan-spec` §3 đòi đo kích thước dự
kiến trước vòng hỏi; r1–r12 không đo (cross-review lượt 12: 0 lần nhắc ADR-0044 ở mọi revision và mọi lượt; r14 đo lại
mọi câu của đoạn này: bảng 16 dòng 13).

*Số đo — ứng viên tham chiếu của phiên soạn r13* (bảng 15; dựng lại ĐÚNG byte ở bảng 16 dòng 3; mã RIG, KHÔNG phải mã
đề nghị; dựng theo đặc tả và khớp các số kỳ vọng sau — 17 nhãn / 48 tiểu nhãn / 57 đơn vị, 195 ca đăng ký, 228 mục
`DOT_BIEN` cộng 3 harness; chốt tĩnh ĐẠT, sáu ca mới QUA, nền ĐỎ đúng loại; (r14, bảng 16 dòng 7–9, `python3.11` và
`python3.12`) phép D xanh với 65/65 control đỏ đúng và 6/6 phép đảo, A/W 55/55 cặp chấp nhận, `--dot-bien` 230/230 —
r13 (§4, §10) và HINT lượt 13 ghi các phép ấy là CHƯA ĐO), `git diff --no-index --numstat` so nền `423b4ba`:

| tệp / phần | thêm / xoá | nguồn của phần ấy |
|---|---|---|
| `launcher.py` | +21 / −5 | Q-A ở `_con_song`, Q-A.7 dạng latin-1 ở năm chỗ đọc, 4 dòng chú thích nguồn (17 dòng mã) |
| `launcher_test.py` — `_con_song_that` đọc bytes | +2 / −2 | §6 mục 3 |
| `launcher_test.py` — khối B8 r12 cộng 3 dòng trống nối | +356 | §7 B8, trích bằng máy (`60ee8d5f…75ff`, 353 dòng) |
| `launcher_test.py` — helper cùng `t156`, `t157`, cộng 1 dòng trống | +738 | helper r9 (`635d93fa…0494`, 737 dòng) |
| `launcher_test.py` — 54 mục `DOT_BIEN` | +216 | §7 B5, bốn dòng mỗi mục theo định dạng bảng nền |
| **tổng, 2 tệp** | **+1333 / −7** | `launcher_test.py` riêng: +1312 / −2 |

Bỏ dòng trống, dòng chú thích và docstring (đếm theo AST): khối B8 272, helper 612, phần thêm của `launcher.py` 17,
cộng 54 mục `DOT_BIEN` 216 và `_con_song_that` 2 (hai phần này không có dòng trống hay chú thích — đo, bảng 16 dòng 4)
⇒ 272 + 612 + 17 + 216 + 2 = 1 119 — kết luận không phụ thuộc cách viết chú thích. (r14, cross-review lượt 13: r13 viết
"khối B8 272, helper 612, phần thêm của `launcher.py` 17 ⇒ tổng khoảng 1 119" — ba số hạng ấy cộng ra 901; câu hỏi
gửi chủ kho trích dưới liệt kê 21 + 356 + 738 + 216 = 1 331, bỏ sót +2 của `_con_song_that`; tổng 1 333 của bảng là
đúng.) Dạng bytes của `launcher.py` (ứng viên `cand_b` của reviewer lượt 12) là +27 / −13 thay cho +21 / −5 (bảng 16
dòng 3). Với trần 600, phần còn lại cho helper là 5 dòng (600 − 21 − 358 − 216); với trần 300, riêng `launcher.py`,
`_con_song_that` và khối B8 đã là 379.

*Cách đo.* Bộ dựng của rig r13 (`dung.py`, sha256 `b96dc94227c2aa4f67035769d414d0df6b198513436e9bf9f27f4d7e3e6fb3b4`)
KHÔNG nhúng vào đây vì nó chứa mã `launcher.py` ứng viên (protocol §8). Các bước của nó đủ để dựng một ứng viên CÙNG
HÌNH; dựng lại ĐÚNG byte thì cần hai tệp nêu ở "Giới hạn" cuối đoạn (r14 sửa chữ "đủ để dựng lại" của r13 — rộng hơn đo):
(1) nền: `git show 423b4ba:.claude/dev/launcher.py` (`808ce5b3…9fc0`) và `…/launcher_test.py` (`882ac43f…97cc`);
(2) `launcher.py` ứng viên (sha256 `bdf3865883130bfd787d3192ec41a798497abc8c85cc772532b5842312086a40`, 4324 dòng): trong
`_con_song`, phép hỏi và nhánh tệp có của nền thay bằng hình của ứng viên nháp r7 (rig r8) — phép hỏi trong `try`,
`ProcessLookupError` ⇒ `False`, `OSError` ⇒ đánh dấu "không rõ"; nhánh tệp có giữ nguyên trừ lời đọc; đường "không rõ"
đọc một lần, tách theo `)` cuối, so `Z`, mọi lỗi đọc hay phân tích ⇒ rơi xuống khối `os.kill(pid, 0)` của nền — cộng bốn
dòng chú thích nguồn; ba hàm ngoài chỉ đổi lời đọc thành `read_text(encoding="latin-1")` kèm chú thích cuối dòng;
không đổi `VERSION`; (3) `launcher_test.py` ứng viên (sha256
`a9b0494b4b36d384a70f4a940d0e3c808ed5407ad1bfe8795368985001c8f6ab`, 9665 dòng): `_con_song_that` đọc `read_bytes()`, tách
theo `rindex(b")")`, so `b"Z"`; ngay trước dòng `DOT_BIEN = [` chèn khối B8 r12 (khối mã `python`
cuối mục B8, 353 dòng, kiểm bằng sha256 `60ee8d5f…75ff` ghi ở B8 — B8 không viết luật trích thành chữ như script chốt
ở B2; rig r13 và r14 trích bằng neo của riêng rig — khối mã `python` đầu tiên sau câu khai băm ấy ở B8 — rồi so
sha256 với số ghi ở B8; neo ấy xuất hiện đúng một lần trong tệp) rồi
helper r9; cuối bảng `DOT_BIEN` nền thêm 54 mục bốn dòng (tên; chuỗi cũ; chuỗi mới; danh sách ca đích), chuỗi lấy từ
bảng 54 dòng của rig r8 (`mutants7.json`, sha256 `ba7047cdab08bdaef92986e172a99225a221ba32dd12e3fd9d9e2b59fc99d878`; mỗi
dòng một cặp, dòng (c) hai ca đích) sau khi đổi lời đọc sang dạng latin-1 — 54/54 chuỗi cũ xuất hiện đúng một lần trong
ứng viên; (4) `git diff --no-index --numstat` từng tệp so nền, tách phần bằng ba tệp trung gian (thêm khối B8; thêm
B8 và helper; đủ). Giới hạn, khai thẳng: helper r9 và `mutants7.json` chỉ có trong rig tạm của các phiên soạn
(scratchpad của phiên soạn, ngoài kho; §10), nên NỘI DUNG của phần +738 (helper) và +216 (chuỗi của 54 mục) KHÔNG tái
lập được từ kho hay từ sandbox review — băm chỉ định danh hai tệp ấy, không dựng lại được chúng (r14 sửa chữ "tái lập
được từ băm" của r13; cross-review lượt 13: sandbox không có hai tệp ⇒ +738 của ứng viên tham chiếu KHÔNG ĐO ĐƯỢC (lý
do 3) ở đó). SỐ DÒNG +216 thì dựng lại được từ lời văn B5 và định dạng bảng nền (54 × 4; reviewer lượt 13 ra đúng 216
trên chuỗi của chính mình). (r14 sửa HINT lượt 13, vốn viết "+738 và +216 KHÔNG tái lập được" rồi "+216 dựng lại được"
— tự mâu thuẫn.) Trong scratchpad của phiên soạn hai tệp vẫn có, băm khớp: r14 dựng lại ứng viên ĐÚNG byte và đo lại
từng phần (bảng 16 dòng 3). Việc 54 mục giết đúng ca: r13 ghi CHƯA ĐO; r14 ĐO (bảng 16 dòng 7, 9). Kích thước của
executor là số đo trên CHÍNH mã của họ, không suy từ bảng này.
**Số đo độc lập (r14, cross-review lượt 13; mã RIG của reviewer, dựng lại từ lời văn §6–§7, không dùng helper r9 hay
`mutants7.json`; bảng 16 dòng 5):** `launcher.py` +27 / −5 (17 dòng mã như tham chiếu, cộng 10 dòng chú thích nguồn
theo §6 mục 1); `launcher_test.py` +1108 / −2 (helper `t156`/`t157` 532 dòng — đặc 410 —, khối B8 353, 54 mục
`DOT_BIEN` 216, `_con_song_that` 2, `import errno` 1, 4 dòng trống nối) ⇒ **+1135 / −7**; 195 ca, `DOT_BIEN` 228 + 3
(VERDICT lượt 13). Các phép lượt 13 chạy trên ứng viên ấy, kèm bản Python theo log của rig lượt 13: chốt tĩnh ĐẠT
(`python3.11`, `python3.13`); sáu ca mới QUA, nền ĐỎ 6/6 đúng loại (`python3.12`); phép D tối giản — 56 + 1 = 57 đơn vị
đúng thứ tự, không chạy 65 control hay phép đảo, log không ghi bản Python; A/W 55/55 cặp, `--dot-bien` `230/230 dat (1
khong do duoc)` và B6 delta 0 (cả ba ở `python3.11` lẫn `python3.12`). (r14 tách bản Python theo từng phép: HINT lượt 13
viết một đuôi "— ở `python3.11` lẫn `python3.12`" chung cho cả câu.) Kích thước helper phụ thuộc cách viết (532 so 737
dòng): +1 333 và +1 135 là HAI mẫu, không mẫu nào là cận của mọi hiện thực đúng đặc tả.

*Ngoại lệ ADR-0044 — thể thức.*
- **Trần cũ:** ≤ 300 dòng thêm (ADR-0044, packet `sensitive` chạm authority). Trần ≤ 3 tệp GIỮ NGUYÊN (packet chạm 2).
- **Trần mới: ≤ 1400 dòng thêm**, cộng cả hai tệp write set, đo bằng `git diff --numstat <base>..<head> --
  .claude/dev/launcher.py .claude/dev/launcher_test.py`. Chỉ cho `wp685`, từ r13 trở đi — phạm vi này là diễn giải của
  phiên agent ghi trong comment `5922387653` dưới nhãn "diễn giải của phiên agent, không phải lời chủ kho" (bảng 16
  dòng 13; r13 ghi không kèm nguồn). Biên so số đo: 1400 − 1333 = 67 dòng (mẫu tham chiếu), 1400 − 1135 = 265 dòng
  (mẫu độc lập lượt 13).
- **Ai duyệt, neo:** chủ kho, quyết định lúc 2026-10-01T00:42:15Z; neo PR #688 comment `5922387653`, đăng
  2026-10-01T00:42:33Z (phiên agent đăng hộ bằng credential chủ kho, tư cách lời khai có neo; r13 đọc qua REST, sha256
  thân `d537d59ee051880461a1a2fc76462a0959e13ebbc0022b5ede96a9171f84c26d`; r14 đối chiếu lại nguyên văn và băm trên bản
  REST mà rig r13 lưu, không đọc lại GitHub — bảng 16 dòng 13). Câu hỏi, nguyên văn: *"#688 (wp685): con số
  ≥ 484 dòng tôi đưa lúc nãy THIẾU — nó chưa tính helper t156/t157 (reviewer đã ghi 'chưa kể helper'). Ứng viên tham
  chiếu dựng đúng đặc tả đo được +1333/−7 dòng trên 2 tệp: launcher.py +21, khối B8 +356, helper t156/t157 +738, 54
  mục DOT_BIEN +216 (ứng viên qua 6/6 ca mới, nền đỏ đúng loại, chốt tĩnh ĐẠT). Bỏ dòng trống/chú thích vẫn ~1119.
  Vượt trần 600 bạn vừa duyệt. Chọn lại?"* Lựa chọn ĐÃ CHỌN, nguyên văn nhãn: *"Duyệt ≤ 1400 (Recommended)"*, mô tả
  kèm: *"Giữ đặc tả như r12; r13 khai kích thước đo được 1333 + lý do (mã sản phẩm ~21 dòng, còn lại là test/đột
  biến), trần 1400; vượt thì dừng hỏi."* KHÔNG chọn: *"Thu hẹp helper"*, *"Tách packet"*.
- **Quyết định bị THAY:** PR #688 comment `5922248948` (quyết định lúc 2026-10-01T00:29:39Z, đăng 00:29:51Z, cùng cách
  đăng hộ; sha256 thân `32707eed3a078c1f71f6ca7c8ebddc2519f5032edfe6ba7b4b4c8ec4b505f53c`) chọn *"Duyệt vượt trần, ≤ 600
  (Recommended)"*, mô tả kèm *"r13 khai kích thước dự kiến + lý do (phần lớn là test/đột biến, mã launcher chỉ ~20
  dòng) và trần mới 600 do bạn duyệt; vượt 600 thì dừng hỏi."*; không chọn *"Duyệt vượt trần, không giới hạn"*,
  *"Tách packet"*. Lý do bị thay: câu hỏi của quyết định ấy đưa con số "≥ 484 dòng thêm" — cận dưới của cross-review
  lượt 12 CHƯA tính helper `t156`/`t157` (VERDICT ghi "chưa kể helper"), tức thiếu đúng phần lớn nhất. Ứng viên tham
  chiếu đo +1333, vượt 600; phiên soạn r13 DỪNG và báo thay vì tự nới, chủ kho quyết lại (comment `5922387653` ghi
  đính chính ấy). Con số chống đỡ một câu về THẨM QUYỀN thì phải là số đo đủ phần, không phải cận dưới.
- **Lý do (ADR-0044 "khai lý do trong spec"):** mã sản phẩm 21 dòng thêm (17 dòng mã); 1312 dòng còn lại là MÃ TEST
  mà các quyết định đã có bắt buộc — khối B8 (sửa lỗi 124 ngay trong packet, quyết định chủ kho 2026-09-30T06:42:25Z),
  helper với hợp đồng chốt theo bảng không gian (B1–B5, (E), D — cross-review lượt 1 đến 11) và 54 mục đột biến của B5.
- **Điều kiện dừng của executor:** đo `git diff --numstat <base>..<head> --` hai tệp write set TRƯỚC khi nộp review;
  tổng dòng thêm > 1400, hay số tệp > 3 ⇒ DỪNG, không nộp review, hỏi chủ kho — không tự tách packet, không xén ca, nhãn
  hay mục `DOT_BIEN` để lọt trần. Ghi numstat thật vào handoff, theo từng phần như bảng trên.

## 5. `ngoai_pham_vi`

- (r9) `:359`, `:430`/`:436`, `:484`/`:490` NAY Ở TRONG phạm vi, chỉ phần giải mã (Q-A.7; chủ kho trả lời §11.1);
  phạm vi bắt của các `try` ấy và mọi hành vi khác giữ nguyên. Vẫn ngoài phạm vi — cùng khuôn `read_text()` trên
  `/proc/<pid>/stat`, `git grep` trên `reviewed_sha` ra đúng ba chỗ ngoài `launcher.py`/`launcher_test.py`; cross-review
  lượt 8 đo trên một cháu CÒN SỐNG có `comm` 15 byte hỏng (ba Python; `comm` thường: cả ba đúng):
  · `.claude/dev/gate_lifecycle.py` `_khoa_pid_proc` (`:899–910`) ⇒ `None` (`tick:…` cho `comm` thường); `_khoa_pid`
    khi ấy lùi về `ps lstart` (khoá `giay:…`, khác định dạng);
  · `.claude/dev/gate_lifecycle.py` `_cac_hau_due` (`:913`, đọc ở `:933`) ⇒ cháu ấy VẮNG khỏi tập hậu duệ — cây giết
    của gate lifecycle bỏ sót nó, cùng hình với B8-setsid của launcher;
  · `.claude/dev/ci_dang_ky_test.py` `_pid_song` (`:904–916`, đọc ở `:913`; AST trên `89fc4fa` và `423b4ba`, r10 — r9
    ghi `:903–913`) ⇒ `[]` cho cháu ấy, theo PID lẫn theo nhóm — phép dò
    rò tiến trình của CI coi nó đã chết.
  **Nợ, KHÔNG sửa ở đây: `DOC-PROC-STAT-GIAI-MA-NGOAI-LAUNCHER`** — ba chỗ trên, hai tệp ngoài write set (một thuộc
  gate lifecycle, một là bộ test CI; người giữ lease của `ci_dang_ky_test.py`: mục "`.github/workflows/**`
  và `.claude/dev/ci_dang_ky_test.py`" của §5; của `gate_lifecycle.py`: chưa đo). Đề nghị packet riêng, cùng Q-A.7
  và một ca khoá kiểu B8 cho từng tệp. Packet này không phụ thuộc chúng (B8 đo `launcher.py` đầu-cuối). Phiên soạn
  r9 đếm lại bằng `git grep` trên `5f7485c` (bảng 11), phiên soạn r10 trên `423b4ba` (bảng 12): ngoài `launcher.py`
  đúng ba chỗ ấy (`gate_lifecycle.py:906`, `:933`, `ci_dang_ky_test.py:913`), cùng số dòng ở cả hai nền; thêm `launcher_test.py:2142` đọc `/proc/1/comm` với `encoding="utf-8"` — phép
  chẩn đoán môi trường bọc trong `_do_an_toan`, không phải phép kiểm sống, ngoài lớp này.
- Nhánh Windows và Darwin của `_con_song`.
- `t125`/`t154` trong `ops/lease_publish_test.py`: không sửa; chúng chỉ là nơi lỗi lộ ra.
- `.github/workflows/**` và `.claude/dev/ci_dang_ky_test.py`. `DA_NOI` (`ci_dang_ky_test.py:69–78`,
  13 mục, trong đó có `launcher_test.py`) chỉ giúp `kiem()` xác nhận rằng có một dòng `run:` trong
  workflow nhắc tới tệp test; nó **không** đưa tệp vào nhóm `MOI` mà `gate-registry` thực thi
  (`ci_dang_ky_test.py:37–53`, 9 mục, không có `launcher_test.py`). Q4 giữ nguyên: PR không nhãn
  `windows` chưa đo `launcher_test.py` qua CI; B6 cục bộ là bằng chứng bắt buộc trước merge. Muốn
  thêm job Linux chạy suite này trên PR thì phải mở revision, authority và write set riêng — packet
  này không tự sửa CI. (Đo 11:14Z 29-09: `ai-dang-giu .claude/dev/ci_dang_ky_test.py` ⇒ `NGƯỜI_GIỮ 2`,
  gồm #668 và `ci-duong-nhanh-ho-so-r2-g3-claude`; thêm một lý do để không đụng tệp này.)
- Chạy lại job CI của PR #679: không làm (chỉ thị thường trực).

## 6. `muc_tieu`

1. `.claude/dev/launcher.py` — Chặn lỗi của phép hỏi `trang_thai.exists()` theo Q-A: `ProcessLookupError`
   ⇒ `False`; `OSError` khác ⇒ thử đọc nội dung trước (đúng một lần), rồi mới rơi về `os.kill(pid, 0)` —
   kể cả khi đọc lỗi hoặc nội dung không phân tích được (Q-A.4, và đoạn làm rõ ở §3: đường mới KHÁC đường
   cũ ở điểm này). Bảo toàn phép phân biệt zombie trong đường lỗi mới. Kèm chú thích theo idiom của tệp
   (nguồn lỗi ESRCH: PR #679, job `109303373142`; nguồn lỗ zombie: cross-review lượt 1 trên PR #688;
   nguồn ba đường nuốt sentinel / nội dung hỏng / đọc hai lần: cross-review lượt 2 trên PR #688; nguồn ba
  đường ESRCH ở tầng đọc / EIO ở tầng đọc / nuốt riêng `KeyboardInterrupt` ở tầng đọc: cross-review lượt 3
  trên PR #688; nguồn việc bước `kill(pid, 0)` phải thực sự được gọi và trả đúng kết quả trên đường lỗi
  đọc/nội dung hỏng: cross-review lượt 4 trên PR #688; nguồn việc nhóm phân tích không được bắt ở tầng hỏi và
  việc phạm vi bắt phải đúng ở cả ba tầng hỏi, đọc, kill: cross-review lượt 5 trên PR #688; nguồn việc hai nhánh
  sẵn có phải giữ nguyên xi cả số lần, không hỏi/đọc lại theo lớp ngoại lệ, và tách trạng thái theo dấu `)` cuối:
  cross-review lượt 6 trên PR #688). (r12) `_con_song` và mọi hàm trợ giúp mới của nó theo danh sách cho phép T1–T7
  của chốt tĩnh (Q-A.7 (iv), B2); chú thích `#` đặt ở đâu cũng được.
2. `.claude/dev/launcher_test.py` — **Sáu ca mới** (r9; r8: hai), tên nối tiếp hậu tố lớn nhất: `t156_...` (B1, B2,
   B3, B4) và `t157_...` (B3b) dựng trên MỘT helper theo nhãn (quy ước chung ở §7), cộng bốn ca B8 `t158_...` đến
   `t161_...` KHÔNG dùng helper (§7 B8). Hậu tố `t155` là lớn nhất của các ca mang tiền tố `t` trên `89fc4fa` (đếm
   ở §8); executor **đo lại hậu tố trên nền tiếp nối** trước khi đặt tên vì #668 cũng giữ tệp này. Các mục
   `DOT_BIEN` mới: **đúng theo danh sách ở B5, và chỉ ở đó** — §6 không lặp lại con số. Số ca mới và số mục đột
   biến là hai đơn vị khác nhau. Helper và các đơn vị nhãn nằm trong `t156_...`, `t157_...`; không thêm tệp, không
   thêm ca đăng ký nào ngoài sáu ca này, không sửa runner `--dot-bien`.
3. (r9) `.claude/dev/launcher.py` — Q-A.7 ở năm chỗ đọc (§3), kèm chú thích theo idiom của tệp (nguồn: quyết định
   chủ kho, PR #688 comment `5905670017`; cross-review lượt 7 và lượt 8 trên PR #688). `.claude/dev/launcher_test.py` — bốn ca B8, hằng
   `DANG_DOC_QA7`, loại `read args` của helper, và `_con_song_that` đọc BYTES: đó là phép kiểm sống ĐỘC LẬP mà `t62`,
   `t63`, `t66`, `t67` dùng, và với `read_text()` nó báo "đã chết" cho chính tiến trình B8 cần thấy (đo lượt 8). Write
   set hai tệp là ĐỦ: năm chỗ đọc và mọi nơi gọi của chúng ở `launcher.py`; mọi ca, helper và đột biến ở
   `launcher_test.py`. (r11; r12 viết lại theo AST) Ở ba hàm ngoài `_con_song` chỉ được đổi đúng phép đổi mà chốt tĩnh
   (B2) cho phép — lời đọc thành lời gọi đã khai, và với dạng bytes thêm hằng `")"`, `"Z"` thành bytes cùng biểu thức dựng
   khoá (luật `H`, `K`); nguồn chú thích thêm: cross-review lượt 10 và lượt 11 trên PR #688.
   (r12) Chú thích `#` theo idiom đặt ở đâu cũng được, kể cả thành DÒNG riêng trong thân ba hàm này: chốt tĩnh r12 so
   AST, chú thích không vào AST (đo: `CMT_khoa`, `CMTR_khoa`, `chu_thich_moi_noi` ĐẠT — bảng 14); docstring thì VÀO AST
   nên không được đổi (đo: `docstring_khoa` ĐỎ luật `H`); không decorator, không thêm câu mức module nào ngoài `def`
   mới (Q-A.7 (iii), (iv); B2).

## 7. `nghiem_thu`

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3). Đột biến chạy trên **bản sao tạm**, bằng chính
`python3.11 .claude/dev/launcher_test.py --dot-bien` và `python3.12 …` (B6: không gọi `python` trần). Quy ước chung cho hai ca `t156_...`, `t157_...` (bốn ca B8 có
quy ước riêng ở mục B8; hằng `DANG_DOC_QA7` dùng chung):

- Mỗi `bang(...)` mang **nhãn** ở đầu thông điệp (`B1`, `B2-eacces`, …) để một đột biến chết đúng chốt
  của nó phân biệt được với chết ở chốt khác của cùng ca. Tám nhãn gồm nhiều đầu vào có tên — `B2-doc-hong`,
  `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`, `B2-parse`, `B2-dem-doc`, `B2-pid-du-phong`, `B2-nhanh-cu` (r7) —
  còn mang **tiểu nhãn**
  ngay sau nhãn, cách một dấu cách (bảng tiểu nhãn ở ngay sau bảng không gian B2). Nhãn là đơn vị của thứ tự
  thực thi và của tham số CHẠY/NỚI của helper; tiểu nhãn là đơn vị của phép quan sát D và của điều kiện khớp ở
  B5 (r4).
- Seam stat/read chỉ chạm đúng `/proc/<pid>/stat` của PID đang xét, có **bộ đếm lần chạm**; ca xác nhận seam đã
  chạm ở từng lời gọi (seam không chạm ⇒ ca không đo gì). Lấy khoá danh tính **trước** khi đặt seam. Seam không
  được giao lỗi nào thì chỉ ĐẾM rồi chuyển tiếp thật — đó là cách các đầu vào đường cũ giữ `stat` và phép đọc thật
  mà vẫn đếm được; (r9) khi lời gọi thật ném, seam chỉ-đếm KHÔNG ghi gì và để ngoại lệ đi nguyên — ngoại lệ ấy là VÔ
  CAN (loại ghi nhận (2) chỉ còn observer `kill`, xem dưới). Observer `os.kill(pid, 0)` (chỉ cặp PID đang xét và tín
  hiệu 0; ghi lại rồi chuyển tiếp thật, hoặc ném lỗi seam; tín hiệu khác hay PID khác chuyển tiếp nguyên vẹn) đặt ở
  (r7): mọi đầu vào mà đường Q-A đi qua bước kill — tầng K (`B2-doc-hong`, `B2-parse`, `B2-dem-doc` tiểu nhãn `3`,
  `B2-pid-du-phong`, và tiểu nhãn `kill`/`kill-*` của `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`) và tầng K0
  (mọi tiểu nhãn `vang*` của `B2-nhanh-cu`) — cùng các đầu vào tầng Đ0 (phần tệp có của `B2-nhanh-cu` và lời gọi
  đường cũ của `B3-zombie`) và (r9) `B2-dem-doc 4` (đường Đ đọc được), để đếm được con số 0. Ba đầu vào tầng hỏi của `B2-thoat-parse` đặt seam ở `Path.exists` (bảng 7), và
  bộ đếm của chính seam ấy phải ≥ 1 — bằng 0 (ứng viên không hỏi bằng `exists()`) thì ca ném lỗi thường,
  không phải `bang`, và executor đổi seam sang hàm `Path` mà ứng viên thực sự gọi rồi khai vào handoff.
- **Seam thay CẢ lời gọi — đối số của lời gọi, và cách khoá (r8 lập; r9 sửa theo Q-A.7 và cross-review lượt 8).**
  Seam ném lỗi hay trả chuỗi dựng sẵn thì thay nguyên lời gọi, nhưng VẪN NHẬN đủ đối số của lời gọi — câu r8 "không
  thấy đối số" sai: lượt 8 đo seam trả payload ghi được `((), {})` cho ứng viên và `((), {'encoding': 'utf-8'})` cho
  biến thể `encoding="utf-8"` tường minh, ở Đ0 và ở Đ. (r9) Mọi chỗ trong đặc tả viết `Path.read_text`/`read_text`
  cho seam, bộ đếm hay payload của phép đọc `/proc/<pid>/stat` trong launcher: đọc là phương thức theo `DANG_DOC_QA7`
  (`read_text` hay `read_bytes`), payload `str` hay `bytes` tương ứng. (r11) Chính điều này là chốt trục API ở hai khối
  đọc của `_con_song`: lời đọc KHÔNG đi qua phương thức đã khai thì seam không thấy và đếm đọc ra 0 — đo (bảng 13, ba
  Python): `g_d0_open` ⇒ `B2-nhanh-cu song read count 0`, `g_d_open` ⇒ `B2-eacces read count 0`; và ngược lại, helper
  chỉ seam `read_text` (helper của phiên soạn) đặt trước ứng viên bytes ĐÚNG cũng ra `B2-eacces read count 0` — helper
  phải seam (ít nhất) đúng phương thức của `DANG_DOC_QA7`. Rà mọi seam của hai ca:
  · Phép đọc (ném hay trả payload, ở Đ, Đ0, K, ma trận `B2-pid-du-phong` và các đầu vào chỉ-đếm): seam GHI (args,
    kwargs) của từng lời gọi trên đúng đường, và ca đòi MỌI bản ghi BẰNG `DANG_DOC_QA7` (loại assertion `read args`,
    xét ngay sau đếm đọc, ở mọi đầu vào có đếm đọc). Vì thế một dạng đọc lệch chết ở đầu vào ĐẦU TIÊN có đọc trên
    đường ấy (Đ0: `B2-dem-lan`; Đ: `B2-eacces`), trước khi tới hai đầu vào nội dung THẬT — `B2-nhanh-cu
    utf8-hong-that` ⇒ `True` (Đ0), `B2-dem-doc 4` ⇒ `True`, đọc được, kill 0 (Đ) — và đuôi UTF-8 hỏng trong `comm`
    của `B3-zombie` (zombie trên đường mới ⇒ `False`). Răng RIÊNG của ba đầu vào ấy là cho vi phạm ĐÚNG đối số mà SAI
    hành vi: giải mã lại UTF-8 sau khi đọc (biến thể (E) `d0_giai_ma_lai_utf8`, `d_giai_ma_lai_utf8`; bảng 11).
    `newline` (3.13) chỉ đổi cách dịch CR, mà phần sau `)` cuối do kernel ghi và không có CR: suy luận, không đo.
  · `Path.stat` và `Path.exists` (ném) che `follow_symlinks`: `/proc/<pid>/stat` là tệp thường, không phải
    symlink (`lstat`, bảng 10 dòng 7), nên tham số ấy không đổi kết quả.
  · ĐƯỜNG DẪN và API: mọi seam khoá theo đúng chuỗi `/proc/<pid>/stat` của PID đang xét, cộng bộ đếm. Ứng viên
    đọc hay hỏi bằng đường khác hoặc API khác (`open`, phương thức đọc không phải dạng khai, `os.path.exists`) không
    chạm seam ⇒ bộ đếm 0
    ⇒ ca đỏ: `read count 0` ở đầu vào đòi đọc 1, hoặc lỗi thường "seam không chạm" ở đầu vào có seam ném (đo ba
    biến thể, bảng 10 dòng 4). Observer `kill` khoá theo cặp (PID, 0); gọi bằng tín hiệu khác hay API khác ⇒
    `kill count 0`.
  Hai đầu vào nội dung THẬT có **điều kiện dựng**: con đặt `comm` bằng đúng 15 byte
  `6b 69 e1 bb 83 6d 5f 74 72 61 5f 74 69 e1 ba` (tức `'kiểm_tra_tiến_trình'.encode()[:15]`, viết dạng byte để lời
  gọi sinh con không phụ thuộc locale — dạng chuỗi làm chính lời gọi sinh con ném `UnicodeEncodeError` ở locale
  ASCII, đo), ca xác nhận bằng phép đọc bytes độc lập rằng `comm` đã đổi, rồi xác nhận NGOÀI cửa sổ đếm rằng
  `read_text()` thật trên đường ấy ném `UnicodeDecodeError`. Một trong hai không đạt ⇒ lỗi thường, KHÔNG `bang`
  (locale giải mã được 15 byte ấy, ví dụ Latin-1, làm điều kiện không dựng được thay vì làm ca đỏ giả).
- **Quy ước đếm theo ĐƯỜNG (r7; HINT lượt 6 viết bản đầu, r7 viết lại theo trục C của bảng không gian mở rộng ở
  B2).** Q-A.1 (hỏi đúng một lần), câu "bước đọc này cũng chỉ làm một lần" của Q-A.4, câu "phải THỰC SỰ gọi
  `kill(pid, 0)` (đúng một lần)" của r5, và "nguyên xi" của Q-A.3 là thuộc tính của MỌI đường, không riêng
  `B2-dem-lan`, `B2-dem-doc`, `B2-pid-du-phong`. Trong mỗi lời gọi `_con_song`, ca đòi:
  · **hỏi** ĐÚNG 1 trên mọi đường (seam ở `Path.stat`, loại `stat count`; seam ở `Path.exists` cho ba đầu vào
    `hoi-*` của `B2-thoat-parse`, loại `exists count`);
  · **đọc** ĐÚNG 1 trên đường Đ (đường mới) và đường Đ0 (tệp có); ĐÚNG 0 trên đường K0 (tệp vắng); loại
    `read count`;
  · **kill** ĐÚNG 1 trên đường K và K0; ĐÚNG 0 trên đường Đ0; loại `kill count`.
  Q-A không quy định số lần đọc hay số lời gọi `kill` trên đường ESRCH, trên đường mà phép hỏi ném ngoại lệ
  ngoài họ `OSError`, và số lời gọi `kill` trên đường Đ khi đọc được: ở đó ca không đòi gì (và không đặt
  observer) — TRỪ `B2-dem-doc 4` (r9): Q-A.4 (r9) nói nội dung thật có `comm` không phải UTF-8 là ĐỌC ĐƯỢC, "không gọi
  kill", và ở đó số lời gọi `kill` là dấu hiệu duy nhất phân biệt "đọc được" với "rơi về kill" (cả hai trả `True`
  cho tiến trình sống), nên ca đặt observer và đòi kill 0. Một ngoại lệ có chủ ý khác: `B2-dem-lan` đi đường Đ0 (lần hỏi đầu là `stat` thật) nhưng là nhãn của trục
  hỏi, nên chỉ giữ phép "đọc ≤ 1" của HINT và không đặt observer `kill`; đọc ĐÚNG 1 và kill 0 trên Đ0 do
  `B2-nhanh-cu` và lời gọi đường cũ của `B3-zombie` đo. `B1` đếm hỏi theo TỪNG lời gọi (cộng dồn 1, 2, 3 qua
  ba lời gọi); `B3-zombie` đếm (hỏi, đọc) cộng dồn (1, 1), (2, 2) qua hai lời gọi đường mới, rồi lời gọi đường cũ
  hỏi 1, đọc 1, kill 0. `B3-song`, `B3-da-wait` không có seam nên không đếm; `B3b-giet-cay` chỉ đòi seam đã chạm,
  vì `_giet_cay` gọi `_con_song` nhiều lần. Danh sách mỗi đầu vào đòi gì: bảng trục C ở B2. Lý do đo được: bản vá
  chỉ hỏi lại `exists()` khi gặp ESRCH, hay chỉ khi gặp `OSError` không phải `PermissionError`, hay chỉ đọc lại
  khi phép đọc gặp EPERM, qua hết hai ca r6, phép D và toàn suite — các nhãn r6 chỉ đòi seam "đã chạm" (≥ 1)
  (cross-review lượt 6); và trên helper dựng đúng theo HINT (chỉ đòi hỏi 1, đọc ≤ 1, và kill chỉ ở hai nhãn), bản
  vá đọc thêm trên đường tệp vắng, gọi `kill` trên đường tệp có, hay gọi `kill` lần hai chỉ khi phép đọc gặp EPERM
  vẫn lọt (bảng 9 dòng 7).
- **Thứ tự assertion TRONG một đầu vào (r8, cross-review lượt 7).** Mỗi đầu vào xét theo thứ tự: (1) ngoại lệ thoát
  (phân hạng theo bốn loại, hay danh tính sentinel); (2) kết quả; (3) đếm hỏi; (4) đếm đọc rồi (r9) `read args`; (5)
  đếm kill. Riêng `B2-pid-du-phong`: (1) ngoại lệ thoát; (2) đếm kill; (3) kết quả; (4) đếm hỏi; (5) đếm đọc rồi
  `read args`. Bước mà đầu vào không
  đòi (không đặt observer, không đếm) thì bỏ, giữ thứ tự các bước còn lại. Loại assertion mà B5 và (E) nêu cho từng
  dòng GIẢ ĐỊNH thứ tự này. Đo, 3.12.3: helper chỉ đổi sang "đếm trước, kết quả sau" làm 9/55 cặp đỏ vì lệch loại ở
  rig lượt 7 ((i), (l3), (l5), (l13), (l14), (l18), (l20), (m1), (m3)) và 8/55 ở rig r8 (cùng danh sách trừ (i), vì
  dòng (i) không nêu loại ở B5; bảng 10 dòng 9), dù ứng viên, helper và 54 dòng đều đúng.
- Ca chỉ chuyển thành `bang(False, ...)` ngoại lệ **có gốc đo được từ chính ca** (r6 nêu đủ bốn loại; r5 chỉ
  nêu loại đầu): (1) đối tượng do seam tạo ra, so bằng danh tính (`is`); (2) ngoại lệ THẬT mà observer của
  `os.kill(pid, 0)` vừa chuyển tiếp — observer ghi lại đối tượng rồi ném lại đúng nó, nên danh tính biết trước khi nó
  thoát (cần cho `B2-pid-du-phong` tiểu nhãn `da-wait`, nơi ESRCH là của kernel chứ không của seam). **(r9) Loại (2)
  CHỈ còn observer `kill`, như r7 — phần r8 mở rộng sang seam chỉ-đếm của `Path.stat` và phép đọc bị BỎ.** Mọi ngoại lệ
  thật đi qua seam chỉ-đếm — `UnicodeDecodeError` của một đột biến đọc lệch dạng, lỗi đối số (`TypeError`,
  `LookupError`), lỗi của một lời gọi thêm — là VÔ CAN. Lý do: (i) phần mở rộng cấp tín dụng giả — lượt 8 đo (ba
  Python) dòng (j1) viết bằng lần đọc thứ hai `read_text(encoding="khong-co-ma-nay")` chết vì `LookupError` được ghi
  `seam escaped`, W0 sống, nên A1/W1/W0 CHẤP NHẬN như giết thật (19/54 dòng B5 không nêu loại); (ii) phần ấy sinh ra
  chỉ để W0 của `d0_value_thoat`, `d0_decode_thoat` khỏi chết vì `UnicodeDecodeError` THẬT của `utf8-hong-that`, mà
  với Q-A.7 đầu vào ấy không còn ném gì trên ứng viên đúng. Đo (lượt 8 và bảng 11, ba Python): loại (2) như r7 +
  Q-A.7 ⇒ 54 dòng 55/55 cặp, hai biến thể ấy CHẤP NHẬN, (j1) VÔ CAN ở A1, W1 và W0; (3) ngoại lệ mới có chuỗi `__cause__` (tức `raise … from …`) chứa một đối tượng loại (1) hoặc (2) —
  bản vá bọc lại ngoại lệ thay vì để nó thoát nguyên đối tượng (Q-A.5); thông điệp ghi `seam wrapped`;
  (4) chỉ ở `B2-parse`, ở các đầu vào parse `p1`–`p3` của `B2-pid-du-phong` (đúng các đầu vào của `B2-parse`), và ở
  hai đầu vào `p1`, `p3` của `B2-nhanh-cu` (r7, cột Đ0): lỗi của phép tách trạng thái mà PAYLOAD THEO DÕI do seam cấp
  tự ném (r9 — `B2-parse` mô tả; nhận bằng DANH TÍNH đối tượng lỗi do seam tạo sẵn, không còn kiểu, đối số, hàm, dòng
  hay số lần). Chuỗi `__context__` (ngữ cảnh ngầm) KHÔNG được tính: một ngoại lệ vô can ném ra
  trong lúc xử lý lỗi seam luôn mang `__context__` là lỗi seam, và nếu tính nó thì ngoại lệ vô can bị ghi
  nhầm thành bằng chứng (đã đo, bảng 8, đối chứng `ctrl`). Cấm `except Exception`/`except BaseException`
  rồi đổi mọi thứ thành `TinHieuChotCa`: mọi ngoại lệ ngoài bốn loại trên giữ hạng vô can (runner in kiểu
  ngoại lệ trong ngoặc sau tên ca — đó là tín dụng giả).
- Sinh tiến trình con: `start_new_session`, tín hiệu thật, dọn bằng **PID tường minh** trong `finally`
  (`kill` rồi `wait`); không `pkill`, không đoán nhóm. Nếu không dựng được điều kiện (ví dụ con không
  chuyển sang `Z` trong thời hạn có trần), ca ném lỗi thường, KHÔNG dùng `bang`.
- **Cấu trúc theo nhãn, MỘT helper dùng chung (r3, lớp `chot-nguoc-khong-co-lap`; r4 thêm điều kiện về mặc
  định, xem phép D ở B5).** Mỗi nhãn là một
  đơn vị độc lập gồm: đầu vào (seam + lời gọi) và nhóm assertion mang nhãn ấy (kết quả, không-lộ-ngoại-
  lệ, seam đã chạm, bộ đếm). Hai ca `t156_...`, `t157_...` gọi CÙNG một helper dựng từ các đơn vị đó; helper nhận hai
  tham số tuỳ chọn mà ca đăng ký KHÔNG truyền — tập nhãn CHẠY (mặc định: tất cả, theo thứ tự dưới đây)
  và tập nhãn NỚI (mặc định: rỗng); tên tham số do executor đặt. **"Nới nhãn L"** nghĩa là: đầu vào của
  L vẫn chạy nguyên (seam vẫn đặt, lời gọi vẫn thực hiện), nhưng MỌI assertion mang nhãn L bị bỏ, và
  nếu một ngoại lệ thuộc bốn loại ghi nhận của quy ước chung ở trên (đối tượng do seam của L tạo ra, so bằng danh
  tính; ngoại lệ thật mà observer `kill` đã ghi; ngoại lệ bọc lại; lỗi do payload theo dõi của `B2-parse` ném, r9)
  thoát khỏi lời gọi thì nó bị nuốt; mọi ngoại lệ khác vẫn thoát. Nới KHÔNG được là cách để bỏ đầu vào, bỏ thiết
  lập hay trả sớm. Helper chỉ phục vụ hai ca `t156_...`, `t157_...` (§6.2): phép đo dùng tham số là lời gọi TRỰC
  TIẾP helper từ tập lệnh bằng chứng của executor, trên bản sao đột biến (cùng cách B5 đã đòi gọi thẳng hàm ca) —
  không phải một ca đăng ký thêm và không sửa runner `--dot-bien`. **Mặc định của hai tham số là một phần của
  hợp đồng và được khoá RIÊNG bằng phép D** (mặc định: mọi nhãn chạy, tập nới rỗng); không được suy
  ra từ việc một đột biến sản phẩm chết ở ca đăng ký, vì đột biến ấy có thể chết ở một nhãn khác.
- **Thứ tự thực thi cố định** trong `t156_...`, đúng thứ tự liệt kê ở đây: `B1`, `B2-eacces`, `B2-eio`,
  `B2-eperm-hoi`, `B2-doc-hong`, `B2-tin-hieu`, `B2-dem-lan`, `B2-exception`, `B2-thoat-parse`, `B2-parse`, `B2-dem-doc`,
  `B2-pid-du-phong`, `B2-nhanh-cu` (r7), `B3-song`, `B3-da-wait`, `B3-zombie`. `bang` ném ở assertion sai ĐẦU TIÊN, nên nhãn báo là nhãn đầu tiên trong
  thứ tự này; B5 dựa vào điều đó. Trong một nhãn có tiểu nhãn, các đầu vào cũng chạy theo thứ tự cố định
  của bảng tiểu nhãn, và assertion sai đầu tiên quyết định tiểu nhãn báo. `t157_...` chỉ có
  `B3b-giet-cay`. B4 không phải nhãn (nó là điều kiện nền).

**Ca `t156_...`**

- **B1 (mục 2) — ESRCH.** Seam ném `ProcessLookupError(errno.ESRCH, …)`. Gọi `_con_song(os.getpid())`,
  `_con_song_dung_khoa(os.getpid(), <khoá thật>)` và `_giet_rieng({<pid con đã wait>: "k"}, 0)`: không
  ngoại lệ nào thoát; hai hàm đầu trả `False`. Nhãn `B1`.
  **ĐỎ khi:** chạy trên nền `89fc4fa` ⇒ `ProcessLookupError` thoát ⇒ ca đổi đúng đối tượng ấy thành
  `bang(False, …)` của chính nó, loại `seam escaped` (dòng (a)); hoặc phép hỏi để ESRCH rơi cùng nhánh với
  `OSError` khác, vào bước đọc rồi trả `True` cho PID sống, loại `result True` (dòng (l2)); hoặc (r7) phép hỏi gặp
  ESRCH thì hỏi `exists()` lại một lần rồi mới trả `False` — kết quả đúng, nhưng bộ đếm hỏi cộng dồn theo lời gọi
  lệch, loại `stat count` (dòng (m4)). `B1` chỉ đo ESRCH ở tầng HỎI (kết quả đúng `False`); ESRCH ở tầng ĐỌC là
  nhãn khác, `B2-doc-hong` tiểu nhãn `ESRCH` (kết quả đúng `True`), và không nhãn nào thay được nhãn kia.
- **B2 (mục 2) — miền lỗi khác ESRCH, chống bản rộng và bản hẹp giả.** Trên `os.getpid()` (PID sống):
  - `B2-eacces`: seam `PermissionError(errno.EACCES, …)` ⇒ `_con_song` trả **`True`**, không ngoại lệ nào
    thoát. **ĐỎ khi** bản RỘNG (`except OSError: return False`) ⇒ `False` (dòng (b)); hoặc bản chỉ bắt
    `ProcessLookupError` — bản vá tối thiểu cho đúng ESRCH — nên EACCES thoát (dòng (l1)).
  - `B2-eio`: seam `OSError(errno.EIO, …)` ⇒ `True`, không ngoại lệ nào thoát. **ĐỎ khi** bản chỉ bắt
    `PermissionError`: EIO thoát ra, trái objective "mọi `OSError`" (dòng (d1)); hoặc bản cho
    `PermissionError` vào bước đọc nhưng trả `False` cho `OSError` khác (dòng (l3)).
  - `B2-eperm-hoi` (r6) — seam `PermissionError(errno.EPERM, …)` ở `Path.stat` của PID sống ⇒ `True`, không
    ngoại lệ nào thoát. EACCES và EPERM cùng lớp `PermissionError`, khác errno; nhãn này đo việc bản vá đối xử
    theo LỚP chứ không theo errno (Q-A.4, r6). **ĐỎ khi:** phép hỏi chỉ nhận một tập errno hữu hạn (EACCES và
    EIO) nên EPERM thoát (dòng (l4)); hoặc phép hỏi phân nhánh riêng cho EPERM và trả `False` (dòng (l5)).
    Giới hạn khai thẳng: errno là tập MỞ. EACCES, EPERM, EIO là ba đại diện; một bản vá nhận đúng ba errno ấy
    và từ chối errno thứ tư (ví dụ ENOMEM) qua được nghiệm thu này. Bản vá như thế vẫn là vi phạm Q-A.4 (r6),
    nhưng phép đo chỉ chứng minh tới ba đại diện: KHÔNG ĐO ĐƯỢC (lý do 4) cho errno thứ tư trở đi.
  - `B2-doc-hong` (r4 mở rộng; r3 chỉ có đầu vào EACCES; r6 thêm `EPERM`) — bốn đầu vào, tiểu nhãn `EACCES`,
    `EIO`, `ESRCH`, `EPERM`, chạy đúng thứ tự ấy. Mỗi đầu vào: seam EACCES ở `Path.stat` của PID sống và seam ở
    `Path.read_text` của đúng đường `/proc/<pid>/stat` của PID ấy ném MỘT đối tượng dựng sẵn — lần lượt
    `PermissionError(errno.EACCES, …)`, `OSError(errno.EIO, …)`, `ProcessLookupError(errno.ESRCH, …)`,
    `PermissionError(errno.EPERM, …)`.
    Mỗi đầu vào phải trả **`True`** (không đọc được thì rơi về `kill(pid, 0)`, không tự khẳng định đã
    chết) và không ngoại lệ nào thoát. (r7) Observer `os.kill(pid, 0)` chuyển tiếp thật và ca đòi đúng MỘT lời gọi
    (quy ước đếm): đầu vào `EPERM` ở tầng đọc không nằm trong ma trận của `B2-pid-du-phong`, nên thiếu phép đếm này
    thì bản vá gọi `kill` lần hai chỉ khi phép đọc gặp EPERM lọt hết (rig r7, biến thể (E)
    `k_kill_lai_khi_doc_EPERM`: lọt helper dựng theo HINT, chết ở tiểu nhãn `EPERM` loại `kill count` trên helper r7). **ESRCH ở tầng đọc KHÔNG phải ESRCH ở tầng hỏi:** ở tầng hỏi kết quả
    đúng là `False` (`B1`), ở tầng đọc kết quả đúng là `True` — hai ô có kỳ vọng NGƯỢC nhau, nên một bản vá
    dùng chung một nhánh xử lý ESRCH cho cả hai tầng chết ở đúng một trong hai nhãn, và hai nhãn này
    KHÔNG thay được cho nhau. Ca đổi chỉ đúng đối tượng do seam tạo ra thành `TinHieuChotCa` khi nó thoát
    (quy ước chung); ngoại lệ khác giữ hạng vô can. **ĐỎ khi:** tầng đọc chỉ bắt `PermissionError` (EIO
    và ESRCH thoát — tiểu nhãn báo là `EIO`, đầu vào đầu tiên làm nó thoát; dòng (d2)); đường đọc hỏng trả
    `False` cho mọi lỗi (tiểu nhãn `EACCES`; dòng (g1)); đường đọc hỏng chỉ trả `False` riêng cho
    `ProcessLookupError` còn lỗi khác vẫn hỏi PID dự phòng (tiểu nhãn `ESRCH`; dòng (g2)). Năm dòng của r6, mỗi
    dòng một hướng còn thiếu của bảng không gian: đọc không bắt `OSError` nào, chỉ bắt nhóm phân tích (tiểu nhãn
    `EACCES`, thoát; dòng (l10)); đọc nhận errno EACCES và EIO mà không nhận ESRCH (tiểu nhãn `ESRCH`, thoát;
    dòng (l11)); đọc nhận errno EACCES, EIO, ESRCH mà không nhận EPERM (tiểu nhãn `EPERM`, thoát; dòng (l12));
    đọc trả `False` riêng cho EPERM (tiểu nhãn `EPERM`; dòng (l13)); đọc cho `PermissionError` rơi về bước kill
    nhưng trả `False` cho `OSError` khác (tiểu nhãn `EIO`; dòng (l14)).
  - `B2-tin-hieu` (r4 mở rộng; r3 chỉ có tầng hỏi; r6 thêm `kill`) — ba đầu vào, tiểu nhãn `hoi`, `doc`, `kill`,
    chạy theo thứ tự ấy. `hoi`: `Path.stat` của PID sống ném MỘT sentinel `KeyboardInterrupt` dựng sẵn. `doc`:
    `Path.stat` ném EACCES và `Path.read_text` của đúng PID ấy ném một sentinel `KeyboardInterrupt` KHÁC.
    `kill`: `Path.stat` ném EACCES, `Path.read_text` ném EACCES (để rơi về bước kill), và observer của
    `os.kill(pid, 0)` ném một sentinel `KeyboardInterrupt` THỨ BA (đếm lần chạm; r7: đúng 1, quy ước đếm). Mỗi đầu vào: ca bắt
    ngay quanh lời gọi và so **đúng đối tượng** (`is`); trả về bình thường thay vì truyền sentinel ra ⇒
    `bang(False, …)`. Ngoại lệ khác giữ hạng vô can (bọc lại bằng `raise … from …` thì theo quy ước chung là
    `seam wrapped`, cũng `bang(False, …)`). **ĐỎ khi:** nuốt `BaseException` quanh phép hỏi (tiểu nhãn
    `hoi`); nuốt riêng `KeyboardInterrupt` ở tầng đọc dù `RuntimeError` vẫn được truyền ra (tiểu nhãn `doc`);
    thêm mệnh đề bắt `BaseException` vào khối `kill` (tiểu nhãn `kill`; dòng (l25)). Sentinel ở tầng hỏi KHÔNG
    thay phép đo tầng đọc hay tầng kill, và sentinel `RuntimeError` của `B2-exception` không thay sentinel
    `KeyboardInterrupt` của nhãn này: bản vá nuốt riêng `KeyboardInterrupt` giữ `RuntimeError` thoát nguyên
    nên `B2-exception` xanh với nó.
  - `B2-dem-lan`: seam theo thứ tự — lần hỏi thứ nhất đi `stat` thật, lần thứ hai ném ESRCH; một lời gọi
    `_con_song` phải chạm seam **đúng một lần** và trả đúng theo trạng thái thật. **ĐỎ khi** bản vá gọi
    `exists()` lần hai: `ProcessLookupError` từ lần hai thoát ra, hoặc bộ đếm lần chạm ≠ 1.
  - `B2-exception` (r3; r6 thêm `kill`) — miền `Exception` KHÔNG thuộc `OSError` (sentinel `RuntimeError`),
    **ba tầng, ba đầu vào, cùng một nhãn**; tiểu nhãn theo thứ tự `hoi`, `doc`, `kill`. Thông điệp `bang` ghi
    tiểu nhãn ngay sau nhãn. (Bản HINT lượt 5 đặt thêm tiểu nhãn `hoi-parse` ở đây, dùng `IndexError`; r6 chuyển
    nó sang nhãn riêng `B2-thoat-parse` vì nhóm phân tích có ba thành viên và ba tầng, xem ngay dưới.)
    · `hoi`: seam `Path.stat` của PID sống ném MỘT đối tượng `RuntimeError` dựng sẵn. `_con_song` phải
      để CHÍNH đối tượng ấy thoát ra. Ca bắt ngay quanh lời gọi và so bằng danh tính (`is`); trả về
      bình thường (kể cả `True`) thay vì ném ⇒ `bang(False, …)`. Đối tượng khác thoát ra ⇒ không bắt
      (vô can).
    · `doc`: seam `Path.stat` ném EACCES (để vào bước 4 của Q-A) và seam `Path.read_text` của đúng
      PID ấy ném MỘT đối tượng `RuntimeError` dựng sẵn khác; chính đối tượng đó phải thoát ra. Cùng
      cách bắt và so như `hoi`.
    · `kill`: seam `Path.stat` ném EACCES, `Path.read_text` ném EACCES (để rơi về bước kill), và observer
      của `os.kill(pid, 0)` ném MỘT `RuntimeError` dựng sẵn thứ ba (đếm lần chạm; r7: đúng 1); chính đối tượng đó phải
      thoát ra. Cùng cách bắt và so như `hoi`.
    **ĐỎ khi:** phép hỏi (`hoi`; dòng (h1)), khối đọc (`doc`; dòng (h2)) hoặc khối `kill` (`kill`; dòng
    (l26)) bắt `Exception`; hoặc phép hỏi bắt `Exception` rồi ném `RuntimeError` mới bằng `raise … from …`
    (`hoi`, thông điệp `seam wrapped`; dòng (l9)). Lý do có nhãn này: `KeyboardInterrupt` ở `B2-tin-hieu`
    thuộc `BaseException` nên bản `except Exception` cho nó thoát nguyên, và một mình nó không phân biệt được
    `except OSError` với `except Exception` (bảng 3: `RuntimeError` bị nuốt trong khi B1–B3b của r2 vẫn PASS).
  - `B2-thoat-parse` (r6, nhóm phân tích `ValueError`, `IndexError`, `UnicodeDecodeError` phải THOÁT NGUYÊN ở
    tầng hỏi và tầng kill — nơi Q-A.5 không cho bắt chúng) — sáu đầu vào, tiểu nhãn theo thứ tự `hoi-index`,
    `hoi-value`, `hoi-decode`, `kill-index`, `kill-value`, `kill-decode`. Mỗi đầu vào ném MỘT sentinel dựng
    sẵn, ca bắt ngay quanh lời gọi và so **đúng đối tượng** (`is`) như `B2-exception`:
    · `hoi-*`: seam ở **`Path.exists`** (không ở `Path.stat`: bảng 7 — `exists()` nuốt `ValueError` và
      `UnicodeDecodeError` phát sinh trong `stat`, nên ở `Path.stat` chỉ `IndexError` đo được; ba tiểu nhãn dùng
      cùng một seam để cùng một phép đo) ném lần lượt `IndexError`, `ValueError`, `UnicodeDecodeError` dựng sẵn
      (đối số dựng tay, ví dụ `UnicodeDecodeError('utf8', bytes([255]), 0, 1, 'x')`, byte 255 không giải mã được).
      `_con_song` phải để chính đối tượng thoát ra: không đọc dự phòng, không trả kết quả sống/chết.
    · `kill-*`: seam `Path.stat` ném EACCES, `Path.read_text` ném EACCES (để rơi về bước kill), observer của
      `os.kill(pid, 0)` ném lần lượt `IndexError`, `ValueError`, `UnicodeDecodeError` dựng sẵn (đếm lần chạm;
      r7: đúng 1); chính đối tượng đó phải thoát ra. (r7) Ba đầu vào `hoi-*` đòi seam `Path.exists` chạm đúng 1,
      loại `exists count`.
    Thứ tự `index`, `value`, `decode` có chủ ý: `ValueError` là cha của `UnicodeDecodeError`, nên bản bắt
    `ValueError` chết ở `value` (đứng trước) còn chỉ bản bắt riêng `UnicodeDecodeError` mới chết ở `decode`.
    **ĐỎ khi** (mỗi tiểu nhãn một dòng): phép hỏi bắt thêm `IndexError` (dòng (l6)), `ValueError` (dòng
    (l7)) hoặc riêng `UnicodeDecodeError` (dòng (l8)) — bản HINT lượt 5 gọi hợp ba thứ ấy là (h3), chết ở
    `hoi-index`; khối `kill` thêm mệnh đề bắt `IndexError` (dòng (l27)), `ValueError` (dòng (l28)) hoặc riêng
    `UnicodeDecodeError` (dòng (l29)). Nhóm phân tích ở tầng hỏi và kill KHÔNG có nguồn tự nhiên đã biết
    (sentinel do ca dựng); việc `pathlib` hay kernel thật sinh chúng: KHÔNG ĐO ĐƯỢC (lý do 4) và không cần cho ô này —
    ô đo hợp đồng "thoát nguyên" của Q-A.5, không đo tần suất.
  - `B2-parse` (r3) — nội dung đọc được nhưng KHÔNG phân tích được, trên đường MỚI (Q-A.4 và đoạn làm
    rõ ở §3; đường cũ trả `False` và không thuộc nhãn này). Bốn đầu vào (tiểu nhãn `p1`–`p4`, chạy theo
    thứ tự ấy), PID sống (`os.getpid()`), seam `Path.stat` ném EACCES, và seam `Path.read_text` của đúng
    đường `/proc/<pid>/stat`: (p1) trả chuỗi rỗng; (p2) trả chuỗi thiếu dấu đóng ngoặc, ví dụ
    `<pid> x S 1`; (p3) trả chuỗi hết ngay sau dấu đóng ngoặc, ví dụ `<pid> (x)`, và cả biến thể có khoảng
    trắng cuối (cùng tiểu nhãn `p3`, hai payload); (p4) ném một
    `UnicodeDecodeError` do ca dựng sẵn (dạng "không giải mã được", có thật: bảng 4). Mỗi đầu vào:
    `_con_song(os.getpid())` phải trả **`True`** (rơi về `kill(pid, 0)`), không ngoại lệ nào thoát.
    **Phân hạng ngoại lệ thoát ra khỏi `_con_song` ở nhãn này (r6 đổi; r3–r5 cấm đổi MỌI ngoại lệ thành
    `TinHieuChotCa`).** Cái giá của lệnh cấm ấy, đo được ở lượt 5 và r6: mọi bản KHÔNG bắt
    `ValueError`, `IndexError` hay `UnicodeDecodeError` ở tầng đọc chỉ chết bằng lỗi vô can, tức tín dụng giả
    (bảng 3, hàng "tầng đọc chỉ bắt `OSError`"), nên ba ô của hàng nhóm phân tích × tầng đọc (hướng
    "thoát") không có đột biến nào chết đúng lý do. Quy tắc mới, hai trường hợp:
    · (p4) `UnicodeDecodeError` do CHÍNH seam dựng: danh tính biết trước ⇒ thoát ra thì `bang(False, …)`
      (thông điệp `seam escaped`), theo quy ước chung.
    · (p1)–(p3) lỗi của phép tách, nhận bằng DANH TÍNH (r9, cross-review lượt 8 — thay luật "kiểu, đối số, nguồn"
      của r6–r8): seam cấp payload là một PAYLOAD THEO DÕI — kiểu con của `str` (hay của `bytes` nếu Q-A.7 chọn bytes)
      mà các phép tách của nền (`rindex`, `index`, cắt lát, `split`, lấy phần tử `[i]` của danh sách `split` trả về)
      đều trả đối tượng theo dõi cùng loại, và khi hỏng thì ném MỘT đối tượng lỗi do seam TẠO SẴN cho đầu vào ấy
      (`ValueError('substring not found')` ở `p1`, `p2`; `IndexError('list index out of range')` ở `p3` — đối số chỉ
      để đọc log). `_con_song` để thoát chính đối tượng ấy SAU khi seam đọc đã chạm ⇒ `bang(False, …)`, thông điệp
      `parse error escaped`; bọc lại bằng `raise … from …` với nguyên nhân là nó ⇒ `parse error wrapped`. Không còn lời
      khai hàm / nguyên dòng / số lần, không `linecache`. Vì sao đổi: luật vị trí của r7–r8 (chuỗi con → nguyên dòng →
      thêm số lần) nhận ra NƠI ném chứ không nhận ra DỮ LIỆU bị tách, nên mỗi lượt lại có một phép giả mới. Đo lượt 8
      (ba Python), dưới luật r8: (fp6b) thử lại CHÍNH dòng tách đã khai trên chuỗi rỗng trong một vòng lặp (không
      thêm bản sao, số lần không đổi), coi `UnicodeDecodeError` là không đọc được; và (c3) ứng viên tách trong hàm trợ
      giúp (r8 cho phép) gọi lại hàm ấy trên `"0 (x)"` trong nhánh `IndexError` ⇒ A1 và W1 `TH … parse error escaped`,
      W0 SỐNG — tín dụng giả qua đủ bốn phép (bản thô fp6, và bản c3 gọi lại trên chuỗi rỗng: A1, W1 TH, W0 vô can —
      lọt hai phép); r8 §10 khai ca hàm trợ giúp "KHÔNG ĐO ĐƯỢC (chưa dựng)". Dưới payload theo dõi: 54 dòng 55/55
      cặp; `ctrl`, fp…fp6, fp6b và hai phép giả c3 chết VÔ CAN ở A1, W1, W0; ứng viên tách hai dòng (C2) và tách trong hàm trợ giúp (C3) có (l15), (l17)
      CHẤP NHẬN — không cần khai gì. Phiên soạn r9 đo lại trên ứng viên nháp Q-A.7 (bảng 11 dòng 3–4, ba Python): cùng kết quả. Giới hạn (thay giới hạn cũ): ứng viên phải tách trên CHÍNH payload bằng các phép ấy;
      tách bằng phép khác (biểu thức chính quy, `partition`, chuẩn hoá chuỗi trước khi tách) làm (l15)/(l17) chết VÔ CAN
      — đỏ ồn ào, không tín dụng giả; executor mở rộng payload theo dõi cho phép mình dùng và khai. Đột biến ĐỔI chính
      phép tách (như (m5)) vẫn hợp lệ vì các dòng ấy nhắm kết quả. Ngoại lệ không phải đối tượng do seam tạo — kể cả
      cùng kiểu, cùng đối số — là vô can.
    Đối chứng (bắt buộc; mỗi cái phải chết VÔ CAN ở A1, W1 và W0 — dưới payload theo dõi chúng vô can theo cấu trúc,
    giữ làm hồi quy): khác đối số (`ctrl`, bảng 8); cùng đối số khác nguồn (fp, lượt 6); fp2, fp3 (lượt 7); fp4, fp5
    (r8); và (r9) fp6, fp6b cùng hai phép giả gọi lại hàm trợ giúp nếu ứng viên tách trong hàm trợ giúp. Luật r6–r8 và số đo của
    chúng: nguyên văn ở `B2-parse` của r8 (sha256 `2ae6ee04…2aa3`).
    **ĐỎ khi** (tám dòng, mỗi hướng của bảng không gian một dòng): đường nội dung hỏng trả `False` ⇒ chết bằng
    assertion kết quả `True` ở `p1` (dòng (i)); tầng đọc không bắt `ValueError` ⇒ chết ở `p1` (dòng (l15));
    kiểm tra dữ liệu chỉ nhận ra chuỗi rỗng mà không bắt `ValueError` ⇒ `p1` qua, chết ở `p2` (dòng (l16));
    tầng đọc không bắt `IndexError` ⇒ chết ở `p3` (dòng (l17)); `IndexError` ⇒ `False` ⇒ chết ở `p3` (dòng (l18));
    phép đọc chỉ bắt `OSError` còn phần tách bọc riêng nên `UnicodeDecodeError` thoát ⇒ chết ở `p4` (dòng (l19));
    `UnicodeDecodeError` ⇒ `False` ⇒ chết ở `p4` (dòng (l20)); tầng đọc bọc lại `ValueError` tự nhiên thành
    `RuntimeError` bằng `raise … from …` ⇒ chết ở `p1` (dòng (l21), thông điệp `parse error wrapped`).
  - `B2-dem-doc` (r3) — số lần ĐỌC nội dung. Gọi `_con_song` TRỰC TIẾP (không qua `_con_song_dung_khoa`), trên
    `os.getpid()` ở đầu vào 1–3 và trên PID con ở đầu vào 4, bốn đầu vào (tiểu nhãn `1`, `2`, `3`, `4`, chạy theo thứ tự ấy; `4` thêm ở r8): (1) `stat` EACCES +
    `read_text` thật thành công; (2) `stat` EIO + `read_text` thật thành công; (3) `stat` EACCES +
    `read_text` ném EACCES (đọc lỗi); (4) (r8; r9 đổi kỳ vọng) con THẬT có `comm` UTF-8 hỏng, `stat` EACCES + phép đọc
    THẬT theo Q-A.7 ⇒ ĐỌC ĐƯỢC, trạng thái khác `Z` ⇒ `True`, không rơi về kill (chi tiết ngay dưới đoạn ĐỎ khi). Trong mỗi
    đầu vào, số lần phép đọc chạm đúng đường `/proc/<pid>/stat` của PID ấy **bên trong cửa sổ
    lời gọi `_con_song`** phải bằng **đúng 1** (gồm cả nhánh đọc thành công lẫn nhánh đọc lỗi). Cửa sổ
    đếm chỉ bao lời gọi: mọi lần đọc kiểm soát do chính ca thực hiện (ví dụ đọc để xác nhận trạng
    thái) nằm NGOÀI cửa sổ — lượt 2 đã đo trường hợp nhầm: cộng lần đọc kiểm soát vào thì bản đúng
    báo 2 (VERDICT lượt 2, hướng 7). Phép đọc khoá của wrapper (`_khoa_danh_tinh`, `:359`) không thuộc
    bộ đếm này vì ca gọi trực tiếp. Bộ đếm là lớp quan sát: nó chuyển tiếp sang phép đọc thật và
    KHÔNG thay nội dung, trừ ở các đầu vào "đọc hỏng" đã khai (đầu vào (3) này, và bốn đầu vào của
    `B2-parse`). Giữ nguyên các kiểm đếm `stat` hiện có (`B2-dem-lan`). (r7, quy ước đếm) Mỗi đầu vào còn đòi hỏi
    đúng 1; đầu vào `3` (đường K) đặt observer `os.kill(pid, 0)` chuyển tiếp thật và đòi đúng 1 lời gọi; (r9) đầu vào `4` là đường Đ ĐỌC ĐƯỢC: observer vẫn đặt và đòi đúng 0 lời gọi. **ĐỎ khi** (đột biến (j)): bộ
    đếm ≠ 1, tức đọc lại lần hai, ở nhánh nào cũng vậy — lần đọc thứ hai đặt sau lần đọc thành công làm
    đầu vào `1` đỏ đầu tiên; lần đọc thứ hai đặt trong xử lý đọc lỗi chỉ chạm ở đầu vào `3`.
    **Đầu vào `4` (r8 lập; r9 đổi kỳ vọng theo Q-A.7).** Con sinh bằng `start_new_session`, tự gọi `prctl(PR_SET_NAME, …)`
    với đúng 15 byte của `'kiểm_tra_tiến_trình'.encode()[:15]` — thứ kernel làm với một chương trình tên tiếng Việt
    (lượt 8 đo: exec qua symlink tên ấy cho đúng 15 byte này, không cần `prctl`). Điều kiện dựng (xác nhận `comm` bằng
    bytes, rồi `read_text()` KHÔNG đối số thật ném `UnicodeDecodeError` ngoài cửa sổ đếm — chứng tỏ đầu vào có răng với
    cách đọc của nền) và cách viết 15 byte: quy ước chung, mục "Seam thay CẢ lời gọi"; dọn con bằng PID tường minh. Kỳ
    vọng r9: `True`, hỏi 1, đọc 1, `read args` đúng `DANG_DOC_QA7`, kill 0 (observer đặt). Kỳ vọng r8 (`kill count 1`)
    khoá đúng lỗi chủ kho quyết sửa (bản nháp Q-A.7 đỏ ở đó, lượt 8). Đo: trên helper KHÔNG có `read args` (lượt 8, ba
    Python) ứng viên theo r8 đỏ ở đây `kill count 1`; trên helper r9 (bảng 11) nó chết sớm hơn ở `B2-eacces read args`,
    và răng riêng của đầu vào này là biến thể (E) `d_giai_ma_lai_utf8` (đúng đối số, sai hành vi) ⇒ `B2-dem-doc 4 kill
    count 1`. Vị trí `B2-parse` cũng dùng được (lượt 8 đo: loại (2) mở rộng r8 ⇒ W0 của (i), (l15), (l16), (l19), (l21)
    sống 5/5; loại (2) hẹp ⇒ 1/5 — r8 khai "KHÔNG ĐO ĐƯỢC (chưa thử)"); với Q-A.7 đầu vào không còn ném, r9 giữ
    `B2-dem-doc`.
  - `B2-pid-du-phong` (r5, thêm sau cross-review lượt 4) — khoá KẾT QUẢ và VIỆC THỰC HIỆN của bước PID dự
    phòng ở Q-A.4, thay vì suy từ `True` trên PID sống. Q-A.4 nói khi không đọc được thì chỉ `os.kill(pid, 0)`
    quyết định sống hay chết; mọi nhãn ở trên đặt đầu vào đọc lỗi hoặc hỏng lên PID SỐNG, nên một bản trả `True`
    ngay sau lỗi đọc — không hỏi PID nào — qua được chúng (lượt 4 đo: qua cả hai ca mẫu của r4 lẫn D) mà vẫn
    báo "sống" cho một PID con đã `wait`. Bốn tiểu nhãn theo thứ tự: `song`, `da-wait`, `eperm`, `eio`. Mỗi
    tiểu nhãn chạy CÙNG tám đầu vào đọc, theo thứ tự: EACCES, EIO, ESRCH (ba lỗi đọc của `B2-doc-hong`), p1,
    p2, p3 không khoảng trắng cuối, p3 có khoảng trắng cuối, p4 (đúng các đầu vào của `B2-parse`: bốn tiểu nhãn, năm lần đọc vì p3 có hai payload), luôn với
    seam `stat` EACCES để vào bước 4. Tổng 4 × 8 = 32 lời gọi `_con_song` trực tiếp. Con số 32 ở đây là số
    đầu vào của nhãn, KHÔNG phải số control của D (D có 65 control ở r8; 63 ở r7; HINT lượt 6 đề nghị 49; 43 ở r6). Ma trận vẫn tám đầu vào đọc: đầu vào
    `EPERM` ở tầng đọc (r6 thêm ở `B2-doc-hong`) không đưa vào ma trận, vì ma trận đo chiều kết quả của bước
    kill chứ không đo phạm vi bắt của bước đọc.
    · `song`: PID là chính tiến trình; `kill` thật thành công ⇒ kết quả `True`.
    · `da-wait`: PID con đã `kill` và `wait` (chết hẳn, không phải zombie); `kill` thật ném ESRCH ⇒ `False`.
    · `eperm`: PID là chính tiến trình; seam CHỈ ở `os.kill` với đúng PID ấy và tín hiệu 0 ném
      `PermissionError(errno.EPERM, …)` ⇒ `True`.
    · `eio`: như `eperm` nhưng seam ném `OSError(errno.EIO, …)` ⇒ `False`.
    Kết quả kỳ vọng của `eperm` và `eio` là ngữ nghĩa SẴN CÓ của khối `os.kill(pid, 0)` ở nền
    (`launcher.py:657–664` trên `89fc4fa`: `ProcessLookupError` ⇒ `False`, `PermissionError` ⇒ `True`, `OSError`
    khác ⇒ `False`); Q-A.4 chỉ nêu hai lỗi đầu, nên r5 ghi rõ lỗi thứ ba ở Q-A.4 (không đổi ngữ nghĩa).
    Observer của `os.kill` chỉ chạm đúng cặp (PID, 0): ghi lại từng lời gọi rồi CHUYỂN TIẾP thật (`song`,
    `da-wait`) hoặc ném lỗi seam (`eperm`, `eio`); tín hiệu khác hay PID khác chuyển tiếp nguyên vẹn; không
    bọc seam ấy quanh thiết lập hay dọn con. Khi `kill` thật ném (tiểu nhãn `da-wait`: ESRCH của kernel), observer
    ghi lại CHÍNH đối tượng ấy rồi ném lại đúng nó (r6; quy ước chung, loại 2) — nhờ đó một bản vá để ESRCH thật
    thoát ra khỏi `_con_song` vẫn bị nhận ra bằng danh tính, thay vì chết bằng lỗi vô can. Trong mỗi lời gọi ca
    đòi, theo thứ tự (quy ước chung, "Thứ tự assertion"): không ngoại lệ ghi nhận nào thoát; đúng MỘT lời gọi
    `kill(pid, 0)`; kết quả đúng như trên; bộ đếm seam `stat` = 1 và `read` = 1. Nới nhãn vẫn chạy mọi đầu vào và
    observer, chỉ bỏ assertion. Phân hạng ngoại lệ thoát ra khỏi `_con_song` theo quy ước chung (bốn loại) và, cho
    p1–p3, theo quy tắc của `B2-parse` (payload theo dõi, r9). Không đổi ngữ nghĩa Q-A.3/.4.
    **ĐỎ khi** (lớp (k), mỗi tiểu nhãn có một mutant độc chiếm về KẾT QUẢ, đã đo ở bảng 6): bản trả `True`
    ngay, không hỏi PID ⇒ `song` (số lời gọi `kill` bằng 0; dòng (k1)); bản hỏi PID nhưng bỏ kết quả ⇒ `da-wait`
    (PID đã `wait` được báo `True`; (k2)); bản tự xử lý `kill` và trả `False` cho `PermissionError` ⇒ `eperm`
    ((k3)); bản tự xử lý `kill` và trả `True` cho `OSError` khác ⇒ `eio` ((k4)); bản hỏi `kill` hai lần (một lần
    trong xử lý lỗi đọc, một lần ở khối chung) ⇒ `song`, bộ đếm bằng 2 ((k5), r6). Ba hướng "thoát" của khối
    `kill` (r6, lớp (l)): khối chỉ bắt `PermissionError` nên ESRCH thật thoát ⇒ `da-wait` (dòng (l22)); khối chỉ
    bắt `ProcessLookupError` nên EPERM thoát ⇒ `eperm` (dòng (l23)); khối bỏ mệnh đề `OSError` nên EIO thoát ⇒
    `eio` (dòng (l24)). `B3-da-wait` (không seam) KHÔNG thay được `da-wait` của nhãn này: nó không đi qua
    đường lỗi mới.
  - `B2-nhanh-cu` (r7, cross-review lượt 6; r7 mở rộng từ năm thành **mười chín** đầu vào (r8: **hai mươi**, thêm `utf8-hong-that`) theo bảng không gian mở
    rộng) — hai nhánh SẴN CÓ của Q-A.3, tức phép hỏi KHÔNG lỗi: cột **Đ0** (tệp có ⇒ đọc) và cột **K0** (tệp vắng
    ⇒ `kill(pid, 0)`). Tiểu nhãn theo thứ tự cố định dưới đây. Kỳ vọng là hành vi CŨ (§2, mã nền
    `launcher.py:651–664` trên `89fc4fa`) mà Q-A.3 giữ nguyên xi — KHÔNG phải lời khẳng định rằng hành vi ấy "đúng".
    · Cột Đ0 — PID là chính tiến trình (`os.getpid()`); `Path.stat` THẬT (chỉ đếm, không ném) nên `exists()` đúng;
      observer `os.kill(pid, 0)` chuyển tiếp thật; mỗi đầu vào đòi hỏi 1, đọc 1, kill **0**:
      `song`: `read_text` thật ⇒ **`True`**.
      `EACCES`, `EIO`, `ESRCH`, `EPERM`: `read_text` của đúng đường ấy ném MỘT đối tượng dựng sẵn — lần lượt
      `PermissionError(errno.EACCES, …)`, `OSError(errno.EIO, …)`, `ProcessLookupError(errno.ESRCH, …)`,
      `PermissionError(errno.EPERM, …)` ⇒ **`False`**.
      `p1`: `read_text` trả chuỗi rỗng ⇒ `ValueError` tự nhiên của phép tách ⇒ **`False`**. `p3`: trả `<pid> (x)` ⇒
      `IndexError` tự nhiên ⇒ **`False`**. Hai đầu vào này dùng payload theo dõi của `B2-parse` (r9)
      để hướng "thoát" chết đúng lý do. `p4`: `read_text` ném MỘT `UnicodeDecodeError` dựng sẵn ⇒
      **`False`**. (HINT lượt 6 gọi `p1` là `rong`; r7 đổi tên cho khớp `B2-parse`.)
      `utf8-hong-that` (r8 lập; r9 ĐẢO kỳ vọng theo Q-A.7): PID là con THẬT đã đổi `comm` như đầu vào `4` của
      `B2-dem-doc` (cùng điều kiện dựng); `stat` và phép đọc THẬT (chỉ đếm), observer chuyển tiếp thật ⇒ **`True`**
      (tiến trình SỐNG), hỏi 1, đọc 1, `read args` đúng `DANG_DOC_QA7`, kill 0. Kỳ vọng r8 `False` là chính lời khai
      sai mà chủ kho quyết sửa: bản vá nháp Q-A.7 của lượt 8 đỏ ở đây với kỳ vọng r8 (`result True`). Trên helper KHÔNG
      có `read args` (lượt 8, ba Python) đột biến M4 đỏ ở đây `result False`; trên helper r9 M4 chết sớm hơn ở `read
      args` (A1 `B2-dem-lan`, W1 `B2-nhanh-cu song`), và răng riêng của đầu vào này là biến thể (E) `d0_giai_ma_lai_utf8`
      ⇒ `result False` (bảng 11). Với Q-A.7 đầu vào này không còn sinh ngoại lệ thật, nên W0 của `d0_value_thoat`,
      `d0_decode_thoat` không cần loại (2) mở rộng (đo lượt 8 và bảng 11: hai biến thể CHẤP NHẬN).
      `tin-hieu`: `read_text` ném MỘT sentinel `KeyboardInterrupt` dựng sẵn ⇒ chính đối tượng ấy thoát (so `is`).
      `exception`: `read_text` ném MỘT sentinel `RuntimeError` dựng sẵn ⇒ chính đối tượng ấy thoát.
    · Cột K0 — mỗi đầu vào đòi hỏi 1, đọc **0**, kill **1**; trừ `vang-da-wait`, `Path.stat` của PID ném
      `FileNotFoundError(errno.ENOENT, …)` — `exists()` NUỐT errno 2 (`_IGNORED_ERRNOS`) và trả `False`, tức "tệp
      vắng" trên PID ĐANG SỐNG:
      `vang`: observer chuyển tiếp thật ⇒ **`True`**.
      `vang-da-wait`: PID con đã `kill` và `wait`; `stat` THẬT (chỉ đếm), `/proc/<pid>` đã mất nên `exists()` trả
      `False`; observer chuyển tiếp thật, `kill` thật ném ESRCH, observer ghi lại chính đối tượng ấy (quy ước chung,
      loại 2) ⇒ **`False`**.
      `vang-eperm`: observer ném `PermissionError(errno.EPERM, …)` ⇒ **`True`**. `vang-eio`: observer ném
      `OSError(errno.EIO, …)` ⇒ **`False`**.
      `vang-tin-hieu`, `vang-exception`, `vang-index`, `vang-value`, `vang-decode`: observer ném MỘT sentinel dựng
      sẵn — lần lượt `KeyboardInterrupt`, `RuntimeError`, `IndexError`, `ValueError`, `UnicodeDecodeError` — và chính
      đối tượng ấy phải thoát (so `is`).
    Thứ tự có chủ ý, như ở các nhãn khác: `tin-hieu` trước `exception` (bản bắt `BaseException` chết ở `tin-hieu`,
    bản chỉ bắt `Exception` mới tới `exception`); `vang-value` trước `vang-decode` (`ValueError` là cha của
    `UnicodeDecodeError`); `vang-exception` trước ba đầu vào nhóm phân tích (bản bắt `Exception` ở K0 chết ở
    `vang-exception`). Cột K0 dùng CÙNG khối mã kill với tầng K ở nền; nó có đầu vào riêng vì bản vá có thể tách
    hai khối (đo: một khối K0 tách riêng mà đúng ngữ nghĩa thì cả hai ca xanh và D xanh — bảng 9 dòng 6, đối chứng —
    còn khối tách riêng mà sai thì chỉ các đầu vào K0 bắt được).
    **ĐỎ khi** (lớp (m) ở B5): nhánh cũ hợp nhất khối đọc về hướng `kill` (đọc lỗi hay nội dung hỏng ⇒ rơi về
    `kill(pid, 0)` thay vì `False`; dòng (m1), chết ở `EACCES`); nhánh cũ bắt `BaseException` (dòng (m2)); tệp vắng ⇒
    trả `False`, bỏ bước `kill` (dòng (m3)). Mọi hạng mục khác của cột Đ0 và K0 — từng thành viên × từng hướng —
    có MỘT biến thể của phép (E) ở B5 thay vì dòng `DOT_BIEN` (lý do: sàn Windows, B4); danh sách ở bảng không
    gian mở rộng. Đã đo (cross-review lượt 6, ba Python, rig reviewer): bản hợp nhất về `kill` qua HẾT hai ca r6,
    phép D và toàn suite (189/190, bằng ứng viên đúng), mà `_giet_cay` trên một con thật có phép đọc của `_con_song`
    bị EACCES lật **124 → 125** (0,11 giây → 2,36 giây; 2 → 23 lần đọc); bản "tệp vắng ⇒ `False`" báo "đã chết" cho
    PID sống; bản bắt `BaseException` nuốt `KeyboardInterrupt`. Đo ở r7 (rig riêng, ba Python): năm đầu vào của HINT
    lượt 6 để lọt 33 biến thể của hai cột này — 13 ở Đ0, 20 ở K0 (bảng 9 dòng 7); với mười chín đầu vào, 28 trong số
    ấy chết bằng `TinHieuChotCa` đúng tiểu nhãn và đúng loại, 5 biến thể "thay thế" ở K0 làm ca đỏ bằng lỗi vô can
    (không lọt; hướng "thay thế" không có loại ghi nhận — xem bảng không gian mở rộng). Đơn vị của nhãn này không có dòng `DOT_BIEN` nào giết đúng lý do (bảng 9 dòng 8):
    `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `exception` (r8 thêm `utf8-hong-that`) — chúng có biến thể (E) giết
    đúng lý do, nhưng (E) và phép D chỉ chạy MỘT lần, trước merge; sau merge chỉ còn assertion của hai ca, chạy ở mỗi
    lượt suite mà không ai đo lại rằng chúng còn đỏ được. Răng BỀN (đo lại ở mỗi lượt `--dot-bien`): KHÔNG CÓ (r8 sửa
    chữ "KHÔNG ĐO ĐƯỢC" của r7 — không có dòng `DOT_BIEN` nào để đo), cùng tình trạng với `B3-song`, `B3-da-wait`.
  - **Bảng không gian phạm vi bắt ngoại lệ (r6; thay "ma trận tầng × miền" của r3–r5) — DANH SÁCH CÓ THẨM
    QUYỀN của lớp `ma-tran-loi-thieu-chot`; B5 trỏ về đây.** Vì sao thay: lớp này đã mở qua năm lượt cross-review
    liên tiếp và lần nào cũng lộ ô kế bên ô vừa vá (lượt 2: ba đường; lượt 3: ba ô tầng đọc; lượt 4: chiều kết quả
    của bước PID dự phòng; lượt 5: nhóm phân tích ở tầng hỏi). Bảng cũ được lập THEO các finding của từng lượt review, nên mỗi
    lần chỉ thêm đúng hàng vừa bị chỉ. r6 liệt kê TOÀN BỘ không gian trước, theo hai trục sinh ra mọi mệnh
    đề `except` mà một bản vá có thể viết — **lời khai của r6, và lượt 6 đo ra nó rộng hơn phép liệt kê**: ba tầng
    dưới đây chỉ là tầng của ĐƯỜNG MỚI, nhánh cũ của Q-A.3 nằm ngoài. Bảng r6 giữ nguyên ngay dưới (15 ô, số của
    r6); "Bảng không gian MỞ RỘNG (r7)" sau nó liệt kê mọi đường và là danh sách có thẩm quyền từ r7:
    · **Hàng** — các nhóm ngoại lệ mà Q-A phân biệt (năm): **R1** `ProcessLookupError` (ESRCH); **R2** `OSError`
      khác, tức lớp gồm `PermissionError` (EACCES, EPERM) và `OSError` thường (EIO) — danh sách errno chỉ là ví
      dụ (Q-A.4, r6); **R3** nhóm phân tích `ValueError`, `IndexError`, `UnicodeDecodeError`; **R4** `Exception`
      khác (`RuntimeError` làm đại diện); **R5** `BaseException` không thuộc `Exception` (`KeyboardInterrupt`
      làm đại diện).
    · **Cột** — các tầng mà một mệnh đề bắt có thể đứng (ba): **H** phép hỏi (`stat`/`exists`); **Đ** phép đọc
      (`read_text` cộng biểu thức tách trạng thái); **K** bước `os.kill(pid, 0)` mà đường lỗi rơi vào. Q-A.5 của r5
      chỉ nêu H và Đ; r6 thêm K vì Q-A.4 đặt một bước thứ ba có phạm vi bắt riêng (khối nền có ba mệnh đề), và
      r5 đã cho thấy một bản vá tự dựng lại phạm vi ấy cho đường lỗi mới (dòng (k3), (k4)).
    · **Hướng** — mỗi thành viên của một ô có hai cách sai. Ô "phải xử lý" (kết quả xác định): **thoát** (mệnh
      đề bắt thiếu nên ngoại lệ thoát ra) và **sai** (bắt nhưng trả sai kết quả). Ô "phải thoát nguyên": **bắt**
      (nuốt) và **bọc** (thoát nhưng bằng đối tượng khác, `raise … from …`). Hướng chỉ phân biệt được bằng
      LOẠI assertion nằm SAU tiểu nhãn trong thông điệp: `seam escaped`, `seam wrapped`, `parse error escaped`,
      `parse error wrapped`, `sentinel identity`, `result <giá trị>`, `kill count <n>`, và (r7, quy ước đếm)
      `stat count`, `exists count`, `read count`. Log A1/W1 phải ghi loại này.
    Mỗi ô ghi: (i) Q-A yêu cầu gì; (ii) đầu vào (nhãn, tiểu nhãn); (iii) đột biến vi phạm RIÊNG ô ấy, kèm dòng B5.

    | ô | hàng × tầng | (i) Q-A yêu cầu | (ii) đầu vào | (iii) đột biến (hướng: dòng B5) |
    |---|---|---|---|---|
    | R1-H | ESRCH × hỏi | bắt ⇒ `False` (Q-A.2) | `B1` | thoát: (a) · sai (rơi về bước đọc, trả `True`): (l2) |
    | R2-H | `OSError` khác × hỏi | không kết luận, vào bước đọc (Q-A.4) | `B2-eacces` (EACCES), `B2-eio` (EIO), `B2-eperm-hoi` (EPERM) | EACCES thoát: (l1) · EACCES sai: (b) · EIO thoát: (d1) · EIO sai: (l3) · EPERM thoát: (l4) · EPERM sai: (l5) |
    | R3-H | nhóm phân tích × hỏi | thoát nguyên (Q-A.5) | `B2-thoat-parse`: `hoi-index`, `hoi-value`, `hoi-decode` (seam ở `Path.exists`, bảng 7) | bắt `IndexError`: (l6) · bắt `ValueError`: (l7) · bắt riêng `UnicodeDecodeError`: (l8) |
    | R4-H | `Exception` khác × hỏi | thoát nguyên | `B2-exception`: `hoi` | bắt: (h1) · bọc: (l9) |
    | R5-H | `BaseException` × hỏi | thoát nguyên | `B2-tin-hieu`: `hoi` | bắt: (e1) |
    | R1-Đ | ESRCH × đọc | rơi về `kill(pid, 0)`; PID sống ⇒ `True` (Q-A.4, r4) | `B2-doc-hong`: `ESRCH` | thoát: (l11) · sai (`False`): (g2) |
    | R2-Đ | `OSError` khác × đọc | như R1-Đ | `B2-doc-hong`: `EACCES`, `EIO`, `EPERM` | EACCES thoát: (l10) · EACCES sai: (g1) · EIO thoát: (d2) · EIO sai: (l14) · EPERM thoát: (l12) · EPERM sai: (l13) |
    | R3-Đ | nhóm phân tích × đọc | rơi về `kill(pid, 0)` (Q-A.4, .5) | `B2-parse`: `p1`, `p2` (`ValueError` tự nhiên), `p3` (`IndexError` tự nhiên), `p4` (`UnicodeDecodeError` do seam) | `ValueError` thoát: (l15) ở `p1`, (l16) ở `p2` · `ValueError` sai: (i) · `IndexError` thoát: (l17) · `IndexError` sai: (l18) · `UnicodeDecodeError` thoát: (l19) · `UnicodeDecodeError` sai: (l20) · bọc: (l21) |
    | R4-Đ | `Exception` khác × đọc | thoát nguyên | `B2-exception`: `doc` | bắt: (h2) |
    | R5-Đ | `BaseException` × đọc | thoát nguyên | `B2-tin-hieu`: `doc` | bắt: (e2) |
    | R1-K | ESRCH × kill | `False` (Q-A.4, r5) | `B2-pid-du-phong`: `da-wait` | thoát: (l22) · sai (`True`): (k2) |
    | R2-K | `OSError` khác × kill | `PermissionError` (EPERM) ⇒ `True`; `OSError` khác (EIO) ⇒ `False` (Q-A.4, r5) | `B2-pid-du-phong`: `eperm`, `eio` | EPERM thoát: (l23) · EPERM sai: (k3) · EIO thoát: (l24) · EIO sai: (k4) |
    | R3-K | nhóm phân tích × kill | thoát nguyên (Q-A.5, r6) | `B2-thoat-parse`: `kill-index`, `kill-value`, `kill-decode` | bắt `IndexError`: (l27) · bắt `ValueError`: (l28) · bắt riêng `UnicodeDecodeError`: (l29) |
    | R4-K | `Exception` khác × kill | thoát nguyên | `B2-exception`: `kill` | bắt: (l26) |
    | R5-K | `BaseException` × kill | thoát nguyên | `B2-tin-hieu`: `kill` | bắt: (l25) |

    **Kiểm đếm bảng r6 (số của r6, đo bằng tập lệnh trên rig r6, xem bảng 8; tổng hiện hành ở bảng mở rộng
    ngay dưới):** 15 ô; 15 ô có đầu vào và có ít nhất một đột
    biến; 42 hạng mục (thành viên × hướng; KHÔNG gồm hướng `bọc` của mười một thành viên, xem bảng mở rộng
    ngay dưới) — T1 14, T2 17, T3 11 — và cả 42 có ít nhất một đột biến chết đúng
    tiểu nhãn và đúng loại assertion; 43 dòng B5 nằm trong bảng (một hạng mục, `ValueError` thoát ở tầng đọc, có
    hai dòng vì hai dạng nội dung hỏng khác nhau `p1` và `p2`). **Sáu dòng B5 nằm NGOÀI bảng** vì chúng không
    thuộc trục "ngoại lệ nào": (c) bỏ phép đọc (zombie); (f) hỏi lần hai; (j1), (j2) đọc lần hai; (k1) không
    hỏi PID; (k5) hỏi PID hai lần — tất cả là trục ĐẾM và QUYẾT ĐỊNH (`B2-dem-lan`, `B2-dem-doc`,
    `B2-pid-du-phong`, `B3-zombie`). 43 + 6 = 49 dòng.

    **Bảng không gian MỞ RỘNG (r7) — MỌI đường của `_con_song` nhánh Linux, liệt kê TRƯỚC rồi mới đóng. Từ r7 đây
    là DANH SÁCH CÓ THẨM QUYỀN của lớp `ma-tran-loi-thieu-chot`; B5 và phép (E) trỏ về đây.** Bảng r6 ở trên chỉ là
    15 ô của ĐƯỜNG MỚI. Lượt 6 đo được bảy bản vá trái Q-A đi qua chỗ bảng ấy không liệt kê (VERDICT lượt 6, hướng 3:
    bốn qua cả hai ca r6, D và toàn suite, ba qua hai ca r6 và D; bảng đối chiếu của cùng VERDICT ghi "6" — r7 theo
    danh sách tường minh ở hướng 3) — nhánh cũ, hỏi/đọc lại có điều kiện, cú pháp phép tách — và trên rig r7, một helper dựng đúng theo HINT lượt 6 — tức ba chỗ ấy đã được
    vá — vẫn để lọt 34 biến thể trái Q-A (bảng 9 dòng 7). Nên r7 không vá theo ô được chỉ mà đếm lại từ ĐƯỜNG:
    · **Đường** (theo mã nền `launcher.py:650–664` và Q-A): phép hỏi H chạy đúng một lần rồi rẽ nhánh — tệp có ⇒
      phép đọc cũ **Đ0**; tệp vắng ⇒ bước kill cũ **K0**; ESRCH ⇒ `False`; `OSError` khác ⇒ phép đọc mới **Đ**, đọc
      được thì kết quả theo trạng thái, không đọc được hay nội dung hỏng thì bước kill mới **K**; ngoại lệ ngoài họ
      `OSError` ⇒ thoát nguyên. Năm tầng H, Đ0, K0, Đ, K là năm CỘT. Nhánh Windows và Darwin: ngoài phạm vi (Q-A.6).
    · **Hàng** — R1–R5 như bảng r6, cộng **R0** "không lỗi": phép của tầng trả bình thường (hỏi: tệp có hoặc tệp
      vắng; đọc: nội dung đọc được, trạng thái `Z` hoặc không; kill: thành công).
    · **Hướng** — ô "phải xử lý": thoát, sai; ô "phải thoát nguyên": bắt, bọc, và (r7) **thay thế** — ném một đối
      tượng MỚI không có `from` (chỉ mang `__context__`). Hướng thay thế không có loại ghi nhận, THEO THIẾT KẾ: tính
      `__context__` đã bị bác vì tự cấp tín dụng giả (bảng 8 dòng 6). Bản vá thay thế vẫn làm ca đỏ (lỗi vô can),
      nên không lọt nghiệm thu; nó chỉ không phân hạng được thành "giết thật" nếu là một mục đột biến.
    · **Ba trục vuông góc**: **C** đếm (hỏi, đọc, kill) × đường; **S** cú pháp phép tách (`comm` chứa `)` và khoảng
      trắng) × {Đ0, Đ}; **N** nơi gọi `_con_song` (năm nơi, §2).
    Mỗi ô ghi (i) Q-A yêu cầu gì; (ii) đầu vào; (iii) đóng bằng gì — một dòng B5 (mục `DOT_BIEN`, răng BỀN: đo lại ở
    mỗi lượt `--dot-bien`) hoặc MỘT biến thể của phép (E) ở B5 (tập lệnh bằng chứng cục bộ, đo một lần trước merge;
    tên biến thể dưới đây là tên trong rig r7, executor đặt tên của mình và khai ánh xạ). Mười lăm ô của bảng r6 giữ
    nội dung như trên; bảng dưới chỉ thêm cho chúng hàng R0 và hai hướng bọc, thay thế.

    | ô | (i) Q-A yêu cầu | (ii) đầu vào | (iii) đóng bằng (hướng: dòng B5, hoặc E = biến thể của phép (E)) |
    |---|---|---|---|
    | R0-H | hỏi một lần; tệp có ⇒ Đ0, tệp vắng ⇒ K0 (Q-A.1, .3) | tệp có: `B2-nhanh-cu song` và mọi đầu vào Đ0; tệp vắng: `B2-nhanh-cu vang*`, `B3-da-wait` | tệp có sai (bỏ đọc, đi kill): E `h_co_bo_doc` · tệp vắng sai (⇒ `False`, không kill): (m3) |
    | R0-Đ0 | đọc được: `Z` ⇒ `False`, không `Z` ⇒ `True` (nguyên xi) | `B2-nhanh-cu song`, `utf8-hong-that` (r9: nội dung THẬT, `comm` không phải UTF-8); lời gọi đường cũ của `B3-zombie` | không-`Z` sai: E `d0_ok_khongZ_sai` · `Z` sai: E `d0_ok_Z_sai` |
    | R0-K0 | `kill` thành công ⇒ `True` (nền, Linux) | `B2-nhanh-cu vang` | sai: E `k0_ok_sai` |
    | R0-Đ | đọc được: `Z` ⇒ `False`, không `Z` ⇒ `True` (Q-A.4) | `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-dem-doc 1`, `2`, `4` (r9: nội dung THẬT); hai lời gọi đường mới của `B3-zombie` | không-`Z` sai: E `d_ok_khongZ_sai` · `Z` sai: E `d_ok_Z_sai` (bỏ đọc: (c), tính ở trục C) |
    | R0-K | `kill` thành công ⇒ `True` (Q-A.4) | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `B2-pid-du-phong song` | sai: E `k_ok_sai` (không gọi kill: (k1), tính ở trục C) |
    | R1-Đ0 | ESRCH ở phép đọc cũ ⇒ `False` | `B2-nhanh-cu ESRCH` | thoát: E `d0_ESRCH_thoat` · sai: E `d0_ESRCH_sai` |
    | R2-Đ0 | `OSError` khác ở phép đọc cũ ⇒ `False` | `B2-nhanh-cu EACCES`, `EIO`, `EPERM` | EACCES thoát: E `d0_EACCES_thoat` · EACCES sai: (m1) · EIO thoát / sai: E `d0_EIO_thoat` / `d0_EIO_sai` · EPERM thoát / sai: E `d0_EPERM_thoat` / `d0_EPERM_sai` |
    | R3-Đ0 | nhóm phân tích ở nhánh cũ ⇒ `False` | `B2-nhanh-cu p1` (`ValueError` tự nhiên), `p3` (`IndexError` tự nhiên), `p4` (`UnicodeDecodeError` do seam) | `ValueError` thoát / sai: E `d0_value_thoat` / `d0_value_sai` · `IndexError` thoát / sai: E `d0_index_thoat` / `d0_index_sai` · `UnicodeDecodeError` thoát / sai: E `d0_decode_thoat` / `d0_decode_sai` |
    | R4-Đ0 | thoát nguyên | `B2-nhanh-cu exception` | bắt: E `d0_exception_bat` · bọc: E `d0_exception_boc` · thay thế: E `d0_exception_thaythe` |
    | R5-Đ0 | thoát nguyên | `B2-nhanh-cu tin-hieu` | bắt: (m2) · bọc: E `d0_tin-hieu_boc` · thay thế: E `d0_tin-hieu_thaythe` |
    | R1-K0 | ESRCH ở `kill` ⇒ `False` | `B2-nhanh-cu vang-da-wait` (ESRCH thật, observer ghi lại) | thoát: E `k0_ESRCH_thoat` (và (l22) khi khối kill còn dùng chung) · sai: E `k0_ESRCH_sai` |
    | R2-K0 | EPERM ⇒ `True`; EIO ⇒ `False` | `B2-nhanh-cu vang-eperm`, `vang-eio` | EPERM thoát / sai: E `k0_EPERM_thoat` / `k0_EPERM_sai` ((l23) khi dùng chung) · EIO thoát / sai: E `k0_EIO_thoat` / `k0_EIO_sai` ((l24) khi dùng chung) |
    | R3-K0 | thoát nguyên | `B2-nhanh-cu vang-index`, `vang-value`, `vang-decode` | mỗi thành viên — bắt: E `k0_<tv>_bat` ((l27)–(l29) khi dùng chung) · bọc: E `k0_<tv>_boc` · thay thế: E `k0_<tv>_thaythe` |
    | R4-K0 | thoát nguyên | `B2-nhanh-cu vang-exception` | bắt: E `k0_exception_bat` ((l26) khi dùng chung) · bọc: E `k0_exception_boc` · thay thế: E `k0_exception_thaythe` |
    | R5-K0 | thoát nguyên | `B2-nhanh-cu vang-tin-hieu` | bắt: E `k0_tin-hieu_bat` ((l25) khi dùng chung) · bọc: E `k0_tin-hieu_boc` · thay thế: E `k0_tin-hieu_thaythe` |
    | 15 ô r6, hướng bọc | thoát nguyên | như bảng r6 | R4-H: (l9) · R3-H ×3, R5-H: E `h_<tv>_boc` · R4-Đ, R5-Đ: E `d_<tv>_boc` · R3-K ×3, R4-K, R5-K: E `k_<tv>_boc` |
    | 15 ô r6, hướng thay thế | thoát nguyên | như bảng r6 | R3-H ×3, R4-H, R5-H: E `h_<tv>_thaythe` · R4-Đ, R5-Đ: E `d_<tv>_thaythe` · R3-K ×3, R4-K, R5-K: E `k_<tv>_thaythe` |

    `<tv>` là tên thành viên: `index`, `value`, `decode`, `exception`, `tin-hieu`. "Khi khối kill còn dùng chung":
    (l22)–(l29) sửa khối kill của nền, mà ở ứng viên nháp khối ấy phục vụ cả K lẫn K0; đo trên rig r7, A2 của (l22),
    (l23), (l24), (l27), (l28), (l29) chết đúng lý do ở tiểu nhãn `vang-*` tương ứng (bảng 9 dòng 2). Bản vá TÁCH khối
    K0 ra riêng thì chỉ biến thể E của cột K0 đo được nó.

    **Trục C — đếm × đường** (quy ước đếm ở §7; "—" nghĩa là Q-A không quy định, ca không đòi):

    | đường | hỏi | đọc | kill | đầu vào đo | đóng bằng |
    |---|---|---|---|---|---|
    | H: ESRCH ⇒ `False` | 1 | — | — | `B1` (cộng dồn theo lời gọi) | hỏi lại khi ESRCH: (m4) |
    | H: ngoại lệ ngoài họ `OSError` thoát | 1 | — | — | `B2-tin-hieu hoi`, `B2-exception hoi` (seam `stat`); `B2-thoat-parse hoi-*` (seam `exists`) | hỏi lại sau khi bắt: E `h_thoat_hoi_lai` |
    | Đ0: tệp có | 1 | 1 | 0 | `B2-dem-lan` (hỏi; đọc ≤ 1), `B2-nhanh-cu` phần Đ0, lời gọi đường cũ của `B3-zombie` | hỏi hai lần: (f) · đọc hai lần: E `d0_doc_hai_lan` · gọi kill: E `d0_them_kill` |
    | K0: tệp vắng | 1 | 0 | 1 | `B2-nhanh-cu` phần K0 | hỏi hai lần: E `k0_hoi_hai_lan` · đọc thêm: E `k0_them_doc` · kill hai lần: E `k0_kill_hai_lan` (không kill: (m3), tính ở R0-H) |
    | Đ: đọc được | 1 | 1 | — (0 ở `B2-dem-doc 4`, r9) | `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-dem-doc 1`, `2`, `4`, hai lời gọi đường mới của `B3-zombie` | hỏi lại khi `OSError` khác EACCES: E `d_hoi_lai_khac_EACCES` (bản vá sai của lượt 6) · đọc hai lần: (j1) · không đọc: (c) |
    | Đ → K: đọc lỗi hay hỏng | 1 | 1 | 1 | `B2-doc-hong`, `B2-parse`, `B2-dem-doc 3`, `B2-pid-du-phong`, tiểu nhãn `kill`/`kill-*` của ba nhãn sentinel | hỏi lại: E `k_hoi_hai_lan` · đọc lại: (j2) — thêm E `d_doc_lai_khi_EPERM` (bản vá sai của lượt 6) · kill hai lần: (k5) — thêm E `k_kill_lai_khi_doc_EPERM` · không gọi kill: (k1) |

    Hỏi, đọc hay gọi kill lại CÓ ĐIỀU KIỆN theo lớp ngoại lệ không cần hạng mục riêng: phép đếm đứng ở MỌI đầu vào
    của đường, nên bản vá chỉ lặp lại khi gặp lớp X chết ở đầu vào mang lớp X (đo: ba biến thể có điều kiện của lượt
    6 và r7, bảng 9 dòng 6 và 11). Giới hạn: lớp X không có đầu vào nào — (i) errno thứ tư (phân nhánh theo errno SỐ)
    ⇒ KHÔNG ĐO ĐƯỢC (lý do 4), như mục 3 của danh sách bất khả thi dưới đây; (ii) lớp nêu bằng TÊN ngoài danh sách `T3`
    (ví dụ hỏi lại khi `InterruptedError`) ⇒ chốt tĩnh ĐỎ; (iii) `subprocess.SubprocessError` (cặp `T6` của nền) hay lớp
    nêu GIÁN TIẾP ⇒ lọt cả hai lớp kiểm — đo, mục 5 (r14; tên lớp TRONG danh sách `T3` đều có đầu vào ở bảng không gian,
    nên rơi vào luật đếm ở trên; HINT lượt 13 viết "lớp con cụ thể nêu bằng TÊN thì chốt tĩnh ĐỎ" — rộng hơn đo).

    **Trục S — cú pháp phép tách.** Đầu vào: một zombie thật có `comm` = `x) R (y`, nội dung
    `<pid> (x) R (y) Z …`; chỉ phép tách theo dấu `)` CUỐI mới đọc ra `Z`. S-Đ: hai lời gọi đường mới của `B3-zombie`
    (seam EACCES ở `stat`), đóng bằng (m5). S-Đ0 (r7): lời gọi đường cũ của `B3-zombie` (không seam lỗi, chỉ đếm),
    đóng bằng E `d0_tach_ngoac_dau`. (r11, cross-review lượt 10) S ở ba hàm ngoài `_con_song` (Q-A.7): đầu vào là cháu
    của `t160`, `t161` mang `comm` `_K124_COMM_CHAU` = `tep (1) ` cộng 7 byte cuối của `_K124_COMM` (15 byte, có `) `,
    khoảng trắng, đuôi UTF-8 hỏng); đóng bằng ba biến thể (E) `s_khoa_tach_ngoac_dau`, `s_nhom_tach_ngoac_dau`,
    `s_chup_tach_ngoac_dau` (DS-E-KHAC, đích là ca B8 như `g_to_hop_dinh_dang_khoa`; bảng mở rộng là đường của
    `_con_song` nên số hạng mục không đổi). Đường thứ hai của trục S (tách cả dòng theo khoảng trắng) ở cả năm chỗ đọc
    dùng CHUNG đầu vào và chốt của đường `)` đầu — cả hai `comm` (`x) R (y`, `_K124_COMM_CHAU`) đều có khoảng trắng, và
    hằng ấy viết cứng trong đặc tả; đo trên rig (bảng 13), không thêm tên (E).

    **Trục G × API (r11, cross-review lượt 10).** `read args` của `t160`, `t161` đòi mọi sự kiện audit `open` trên
    `/proc/…`, đường tương đối hay fd số trong cửa sổ nằm TRONG một lời đọc `Path` đã ghi (B8, assertion (3)), nên đọc
    bằng API ngoài lời gọi đã khai bị bắt kể cả khi hành vi đúng. Hai khối đọc của `_con_song` còn chốt ở helper: seam
    `Path` thay CẢ lời gọi, nên đọc bằng đường khác thì seam không thấy và đếm đọc ra 0. Năm biến thể (E) thêm cho năm
    hạng mục sẵn có `g_khoa`, `g_nhom`, `g_chup`, `g_d0`, `g_d`, không tăng số hạng mục: `g_khoa_open`, `g_nhom_open`,
    `g_chup_open`, `g_d0_open`, `g_d_open` (giữ cách giải mã của ứng viên, chỉ đổi lời đọc sang `open()` — DS-E-KHAC).

    **Năm chỗ đọc × hai trục (r11) — liệt kê TRƯỚC khi vá; danh sách có thẩm quyền của hai trục S và API.** Đường S:
    (s1) tách theo `)` ĐẦU — `index`, `find`, `partition(b") ")`, `split(b")", 1)`, biểu thức chính quy không tham
    lam; (s2) tách cả dòng theo khoảng trắng — `split()[k]`. Đường API: (a1) `open()`/`io.open`/`codecs.open`;
    (a2) `Path.open()`; (a3) `os.open` rồi `os.read`; (a4) đường khác tới cùng nội dung — `/proc/<pid>/task/<pid>/stat`,
    `dir_fd` tương đối, và đường tuyệt đối không bắt đầu bằng `/proc/` (`//proc/<pid>/stat`, `/dev/fd/<n>`); (a5) tiến
    trình con (ví dụ `cat`); (a6) fd mở TRƯỚC cửa sổ. Số đo: bảng 13 (ba Python).

    | chỗ đọc (nền `423b4ba`) | S: đầu vào · chốt · (E) · đo | API: đầu vào · chốt · (E) · đo |
    |---|---|---|
    | `_khoa_danh_tinh` `:359`–`:362` | cháu `t160`, `t161` (`_K124_COMM_CHAU`) · (1)/(2) của `t160`, `t161` · `s_khoa_tach_ngoac_dau` · s1 (`SXa`, `SXb`, `SXp`) và s2 (`SW`): `t160`, `t161` `124 noi doi` | cửa sổ `t160`, `t161` · `read args` (open ngoài lời đọc đã ghi) phủ a1–a3, a4 trên `/proc/…` hay tương đối, a5 — a5 qua fd ống mà `Popen` bọc bằng `io.open` · `g_khoa_open` · a1/a2/a3 (`OPEN*`, `PATHOPEN`), a4 (`TASK_khoa`, `DIRFD_khoa`), a5 (`CAT_khoa`): `read args` (open ngoài); a4 dạng `//proc/…` (`SL2_khoa`): B8 QUA — chốt tĩnh ĐỎ; a6 và mọi đường khác: chốt tĩnh |
    | `_thanh_vien_nhom` `:436`–`:438` | như trên · `s_nhom_tach_ngoac_dau` · s1, s2: `t161` `124 noi doi` (`t160` QUA — cháu `setsid` không nằm trong nhóm của mẹ) | như trên · `g_nhom_open` · `OPEN*_nhom`: `read args` (open ngoài); a6: chốt tĩnh |
    | `_chup_cay` `:490`–`:494` | như trên · `s_chup_tach_ngoac_dau` · s1, s2: `t160` `124 noi doi`, `t161` `khong giet duoc` | như trên · `g_chup_open` · `OPEN*_chup`: `read args` (open ngoài); a6: chốt tĩnh |
    | `_con_song` Đ0 (nhánh tệp có) | zombie `x) R (y` — lời gọi đường cũ của `B3-zombie` · `B3-zombie` · `d0_tach_ngoac_dau` · s2 (`SW_d0`): `t156` `B3-zombie result True` | helper (seam thay cả lời gọi) và cửa sổ `t160`, `t161` (qua `_con_lai`) · đếm đọc; `read args` (open ngoài) · `g_d0_open` · `t156` `B2-nhanh-cu song read count 0`; `t160`, `t161` `read args` (open ngoài) |
    | `_con_song` Đ (đường lỗi mới) | zombie `x) R (y` + seam EACCES ở `stat` — hai lời gọi đường mới của `B3-zombie` · (m5) · `luot6_m5` · s2 (`SW_d`): `t156` `B2-parse p2 kill count 0` | helper · đếm đọc · `g_d_open` · `t156` `B2-eacces read count 0`; B8 không chạm (như M5): QUA ×4 |

    Ô nào dùng CHUNG một chốt với ô khác thì đã ghi; không ô nào chỉ có lời văn. Giới hạn: một đầu vào mỗi trục mỗi
    chỗ (một `comm` có `) ` cho ba hàm ngoài, một zombie cho hai khối của `_con_song`); đường thứ ba của trục S hay trục
    API mà danh sách trên chưa nêu: chốt tĩnh phủ ở ba hàm ngoài, seam đếm đọc phủ ở `_con_song` (mọi đường không đi qua
    lời gọi `Path` đã khai); hành vi riêng của một đường chưa ai nêu: CHƯA ĐO — nêu được thì dựng được biến thể và đo
    được, như mọi đường trong bảng. (r12) Ở `_con_song` chốt tĩnh r12 bắt thêm `open()` (luật `T3`) và `os.open`/`os.read`
    (luật `T6`) — đo: `g_d0_open`, `g_d_open`, `cs_open`, `cs_os_open` ĐỎ; tiến trình con qua `subprocess.run` thì KHÔNG
    (cặp có sẵn ở `_con_song` nền) — `cs_subprocess` ĐẠT chốt tĩnh, helper bắt (bảng 14).

    **Chốt tĩnh (r12, cross-review lượt 11, lớp `chot-tinh-bien-chua-khep` — THAY luật dòng "Chốt tĩnh phần còn lại"
    của r11; luật r11 và đoạn HINT lượt 11 về nó: B2 của r11, sha256 `830d5ce4…5604`, và `HINT.patch` lượt 11.)** Q-A.7
    hứa: ngoài phép đọc, `_khoa_danh_tinh`, `_thanh_vien_nhom`, `_chup_cay` KHÔNG đổi; ở ba hàm này hành vi đúng CHÍNH LÀ
    hành vi của nền, nên phép so với nền đo đúng lời hứa. Lượt 11 đo luật r11 (so ký tự từng dòng trong vùng `def` đến
    `end_lineno`) hở bốn biên: (i) hai hiện thực đúng lời văn cho hai kết luận ngược nhau trên cùng `cand_a`, tuỳ cách
    dựng dấu nháy từ `DANG_DOC_QA7`; (ii) decorator và phép gán lại tên ở mức module nằm ngoài vùng ấy — `DECO_khoa` (thử
    lại khi `None`: đổi số lần đọc), `REBIND2_nhom` (nuốt `BaseException`, trả `[]`: đổi phạm vi bắt) QUA bốn ca B8 ở ba
    Python; (iii) chỉ đòi đầu ra, không script, không đối chứng buộc ĐỎ; (iv) §6 đòi chú thích trong thân mà luật (a)
    cấm dòng mới. HINT lượt 11 vá (i) bằng `ast.dump` của riêng các dòng được đổi và (ii) bằng luật đếm ràng buộc trên
    các câu ĐỈNH của module, vẫn so ký tự mọi dòng khác. Đo luật ấy bằng CHÍNH script của reviewer (`rig/chot_tinh_ast.py`
    lượt 11, chỉ đọc) trên 44 đường vào r12 tự liệt kê dưới đây (bảng 14; 3.11 và 3.13 như nhau): 37 ĐẠT — kể cả gán
    trong `if`, `for`, walrus, `except … as`, `globals()[…] =`, `setattr(sys.modules[…], …)`, gán lại `Path`, mọi đường qua
    `_con_song` hay `def` mới, khoá bytes đọc lại `/proc`; 7 ĐỎ, trong đó 1 đỏ oan (chú thích thành dòng trong thân).
    **Đường vào, liệt kê TRƯỚC khi vá** — mọi cách đổi hành vi ba hàm ngoài mà không đổi phép đọc: (w1) đổi thân, chữ
    ký, docstring; (w2) decorator; (w3) ràng buộc lại tên ở mức module — gán, gán trong `if`/`for`/`try`, walrus,
    `import … as`, `except … as`, `del` rồi `def` lại, `class` trùng tên, `globals()[…] =`, `setattr(sys.modules[…], …)`,
    `__code__ =`; (w4) đổi thứ ba hàm dùng ở mức module — gán lại `Path`, `platform`, `__builtins__`; (w5) đổi các thứ ấy
    LÚC CHẠY từ hàm được phép đổi (`_con_song`, hàm trợ giúp mới) — `global`, `import`, `setattr`/`globals()`/`exec`,
    thuộc tính dunder (`__code__`, `__dict__`), gán thuộc tính (`Path.read_text = …`, `platform.system = …`), thuộc tính
    lạ của tên toàn cục (`os.sys`), giá trị mặc định hay decorator của `def` mới (chạy lúc nạp module); (w6) dạng bytes:
    biểu thức dựng khoá là chỗ tự do từ r11 — đọc lại `/proc` hay gọi hàm trong đó. Liệt kê cách VIẾT của từng đường là
    danh sách cấm (CLAUDE.md), nên r12 đóng theo điều ĐƯỢC PHÉP, bốn luật:
    · **`H`** — mỗi hàm canh: CẢ nút `def` (decorator, chữ ký, docstring, thân) BẰNG nền theo AST — không so dòng hay
      cột, nên chú thích `#` tự do — sau ĐÚNG phép đổi của dạng đã khai, và CHỈ trong thân nhánh `if he == "Linux":`:
      lời gọi `.read_text()` thành lời gọi dựng từ `DANG_DOC_QA7`; dạng bytes thêm hằng `")"`, `"Z"` thành bytes (nhánh
      Darwin của `_thanh_vien_nhom`, `_chup_cay` cũng có hằng `"Z"` — đo trên nền: 3 hằng `")"`/`"Z"` mỗi hàm, 2 trong
      nhánh Linux — nên phép đổi ngoài nhánh Linux sẽ đỏ oan). Hình dạng nền (mỗi hàm: số lời gọi, số hằng, số f-string
      `linux:`) khác số đã biết thì script dừng rc=3. Đóng (w1), (w2).
    · **`K`** — dạng bytes: biểu thức dựng khoá chỉ được ghép `sau[19]` ĐÚNG một lần bằng f-string, `+`, `.decode(…)`,
      `int()`, `str()`; định dạng khoá do chốt động giữ (`_k124_khoa_that`, Q-A.7). Đóng (w6).
    · **`M`** — mọi câu mức module ngoài bốn hàm BẰNG nền theo AST (MỘT phép so danh sách: độ dài và từng câu), trừ giá
      trị chuỗi của `VERSION`; chỉ được THÊM câu `def` mang tên chưa có ở mức module của nền và không trùng tên dựng sẵn.
      Đóng (w3), (w4). (r13 sửa câu r12 "mỗi tên được canh ràng buộc đúng một lần ở mức module là hệ quả, không cần luật
      đếm riêng" — rộng hơn đo.) Phép so trên BỎ QUA mọi `def` mang tên bốn hàm, nên ràng buộc ấy do phép ĐẾM riêng
      "đúng một `def` mức module" của script giữ, không phải hệ quả: r13 đo (`python3.11`, bảng 15 dòng 7) — thêm một
      `def _chup_cay` thứ hai trả `{}` ⇒ script nguyên văn ĐỎ rc=1 (`M _chup_cay: 2 def muc module`), tắt phép đếm ⇒ ĐẠT
      rc=0; với `_khoa_danh_tinh` thứ hai, tắt phép đếm ⇒ rc=2 vì đối chứng tách không dựng được (bắt gián tiếp).
    · **`T1`–`T7`** — `_con_song` và mọi `def` mới: T1 không `global`/`nonlocal`; T2 không `import` (`_con_song` nền
      không có); T3 tên toàn cục được đọc — theo `symtable`, đúng phạm vi kể cả lambda lồng — thuộc tập tên toàn cục của
      `_con_song` nền (`IndexError`, `OSError`, `Path`, `PermissionError`, `ProcessLookupError`, `ValueError`,
      `_khoa_danh_tinh`, `os`, `platform`, `str`, `subprocess`; đo bằng `symtable` ở 3.11 và 3.13) cộng `UnicodeDecodeError`,
      `bytes`, `int`, `len`, `isinstance`, `bool` và tên các `def` mới — cần tên khác thì khai và ra revision mới; T4 không
      thuộc tính dunder; T5 không gán hay xoá thuộc tính hoặc chỉ số; T6 thuộc tính của một tên toàn cục chỉ là cặp có
      trong `_con_song` nền (`os.kill`, `platform.system`, `subprocess.run`, `subprocess.SubprocessError`); T7 decorator
      và chữ ký của `_con_song` BẰNG nền, `def` mới không decorator, không giá trị mặc định. Đóng cách viết TRỰC TIẾP
      của (w5) — tên toàn cục, `global`/`import`, dunder, gán thuộc tính hay chỉ số, cặp thuộc tính trên tên toàn cục,
      decorator và giá trị mặc định của `def` mới; đường GIÁN TIẾP thì không (r13, đo lượt 12: "Giới hạn, khai thẳng").
    **Script chốt r12 là mã kiểm thuần của đặc tả, chạy NGUYÊN VĂN** — trích bằng máy: các dòng nằm giữa dòng rào mở
    khối mã `python` đầu tiên SAU dòng chứa cụm "Script chốt r12 là mã kiểm thuần" và dòng rào đóng kế tiếp, nối bằng
    xuống dòng, cộng một xuống dòng cuối; sha256 của bytes trích ra phải bằng số ghi ngay dưới khối.
    Chỉ có MỘT hiện thực, nên (i) không thể tái diễn. Chạy bằng
    `python3.11` (PEP 701: `P701` chỉ ĐỎ ở 3.11 — bảng 14): `python3.11 chot_tinh_r12.py <launcher.py của nền>
    <launcher.py ứng viên> <launcher_test.py ứng viên>`; dạng đọc lấy từ CHÍNH hằng `DANG_DOC_QA7` của `launcher_test.py`
    ứng viên (ngoài hai dạng của Q-A.7 ⇒ rc=3). **Đối chứng buộc ĐỎ, dựng từ CHÍNH ứng viên, chạy cùng lượt**: mười bốn,
    mỗi LUẬT ít nhất một cái — không phải mỗi nhánh mã: năm trong mười bốn chỗ ghi lỗi chưa có đối chứng riêng (r13
    đo), "Răng của đối chứng" (dạng latin-1 bỏ
    `khoa_bytes` ⇒ mười ba) — nền (`H`), tách theo `)` đầu ở
    `_khoa_danh_tinh` (`H`), decorator trên `_thanh_vien_nhom` (`H`), gán lại tên ở mức module (`M`), `def` trùng tên
    import `Path` (`M`), `global`, `import`, `setattr`, dunder, gán thuộc tính, `os.open` trong `_con_song` (`T1`–`T6`),
    đổi giá trị mặc định của `_con_song` (`T7`), `def` mới có `global` (`T1` ở hàm mới), khoá bytes `"linux:" + str(pid)`
    (`K`). Mỗi đối chứng phải ĐỎ với lỗi MỚI (so với chính ứng viên) toàn thuộc đúng luật của nó, không thì rc=2; rc=0
    chỉ khi ứng viên ĐẠT VÀ mọi đối chứng ĐỎ đúng luật. Nền tiếp nối: script so với chính nền được truyền vào; nền
    thiếu một trong bốn `def` hay nhánh Linux của ba hàm canh lệch hình dạng đã biết ⇒ rc=3 ⇒ revision mới, không
    dẫn xuất lại.
    **Đo (bảng 14; `python3.11` và `python3.13` trên bản sao trong rig):** bốn ứng viên nháp dựng độc lập (hai latin-1,
    hai bytes, hai cấu trúc `_con_song`) ĐẠT, mọi đối chứng ĐỎ đúng luật; nền ĐỎ `H` ở cả ba hàm. 31 bản của rig
    reviewer lượt 11: 6 ĐẠT (`cand_a`, `cand_b`, `Q1_khoa`, `CMTR_khoa`, `CMT_khoa`, `SX_d0`), 25 ĐỎ — trên đúng 29 bản
    của log/28 lượt 11: 6 ĐẠT, 23 ĐỎ (luật HINT: 11 ĐẠT, 18 ĐỎ); khác HINT theo đúng thiết kế: `CMT_khoa` (dòng chú thích
    trong thân) nay ĐẠT; `MEBO`, `KILLNEVER` (`M`), `g_d_open`, `g_d0_open` (`T3`: `open`), `CHUP_PPID_by`, `CHUP_PGID_by`
    (`H`: chỉ số `ppid`/`pgrp` nằm ngoài biểu thức khoá) nay ĐỎ. 62 bản của rig r11: 12 ĐẠT — bốn ứng viên, và `M4`,
    `M5`, `SW_d`, `SW_d0`, `D0_KIEMDL` (ngữ nghĩa của `_con_song`), `WK`, `WK1`, `WK2` (khoá bytes bỏ giải mã: `K` cho
    qua, chốt động bắt) — 50 ĐỎ. 44 đường vào tự liệt kê (w1)–(w6), dựng từ `cand_a`, `cand_b`: 39 ĐỎ đúng luật, 5 ĐẠT
    hợp lệ (chú thích ở mọi chỗ; khoá bytes `int(sau[19])`; khoá bytes bỏ giải mã; hàm trợ giúp tách trạng thái;
    `VERSION` đổi giá trị). 3.11 và 3.13 cùng kết cục trên 141 bản trừ đúng một: `P701` (3.11 ĐỎ, không parse được;
    3.13 ĐẠT).
    **Răng của đối chứng — đột biến CHÍNH script** (bảng 14): 15 đột biến, mỗi cái tắt hay nới đúng một luật — kể cả
    nới danh sách cho phép để chứa tên tấn công (`setattr` vào T3, `os.open` vào T6, như CLAUDE.md đòi) — chạy trên
    `cand_a` và `cand_b`: 30/30 cho rc=2 với đúng đối chứng của luật ấy hết ĐỎ (`khoa_luon_hop_le` trên dạng latin-1:
    không áp dụng, rc=0), ở cả 3.11 và 3.13. Lượt đầu của phép đo này lộ một nhánh KHÔNG có đối chứng riêng: phần `M` từng
    so độ dài và so từng câu bằng hai nhánh mã, đối chứng gán lại tên chỉ chạm nhánh độ dài, nên tắt nhánh so từng câu
    vẫn rc=0 — r12 gộp thành một phép so danh sách rồi đo lại. (r13, cross-review lượt 12: bộ 16 đột biến script của
    reviewer, `python3.11` và `python3.13`, trên hai ứng viên dựng độc lập.) Mười hai đột biến tắt hay nới một luật cho
    rc=2 như trên; ba NHÁNH mã không có đối chứng riêng — phép đếm "đúng một `def` mức module" cho bốn hàm (`M`), `T7`
    cho `def` mới, `T5` cho gán/xoá CHỈ SỐ: tắt nhánh nào cũng vẫn rc=0 trên cả hai ứng viên. Hai nhánh có tác dụng thật:
    `def` mới có giá trị mặc định chạy mã lúc NẠP module (`T7`), gán chỉ số qua bí danh của `os` (`T5`) — script nguyên
    văn ĐỎ rc=1, bản tắt nhánh cho rc=0 ĐẠT. Mã đóng băng bằng sha256 nên ba nhánh vẫn chạy trên mọi ứng viên; thứ
    thiếu chỉ là đối chứng chứng tỏ chúng đỏ được TRÊN ứng viên đang xét, nên lời khai đúng là "mỗi LUẬT một đối
    chứng", không phải "mỗi nhánh mã".
    (r13, phiên soạn tự liệt kê — bảng 15 dòng 7.) Script có mười bốn chỗ ghi lỗi (`loi.append` trong `kiem`). Tắt LẦN
    LƯỢT từng chỗ trên bản sao script, `python3.11`, trên hai ứng viên (latin-1 của rig r13; bytes `cand_b` của reviewer
    lượt 12): chín chỗ có đối chứng dựa vào (rc=2 — so hàm canh của `H`/`K`, so mức module của `M`, `T1`, `T2`, `T4`,
    `T5` cho thuộc tính, `T6`, `T3` cho tên ngoài danh sách, `T7` của `_con_song`); năm chỗ không (rc=0) — ba chỗ
    reviewer đã đo ở trên, cộng hai chỗ chưa ai chỉ: `M` "def mới trùng tên" và `T3` "không tìm thấy bảng ký hiệu". Hai
    chỗ sau cùng bắt MỘT đầu vào — hai `def` mới cùng tên, bản sau gọi `os.open`: script nguyên văn ĐỎ rc=1 với cả hai
    lỗi, tắt một chỗ vẫn ĐỎ rc=1, tắt cả hai ⇒ ĐẠT rc=0. Mỗi mã luật (`H`, `K`, `M`, `T1`–`T7`) có ít nhất một đối chứng
    ĐỎ đúng luật trên cả hai ứng viên (`K`: chỉ dạng bytes) — đó là phạm vi của lời khai. r13 KHÔNG thêm đối chứng cho
    ba nhánh reviewer chỉ: danh sách tự liệt kê dài hơn danh sách được chỉ (năm so ba), vá theo danh sách được chỉ là
    đúng hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba" (§9 mục 13), và mọi đối chứng mới đổi băm script, tức
    một vòng đo mới cho mọi bản đã đo. Script và băm khối giữ nguyên (`add42b31…35b6`).
    **Giới hạn, khai thẳng:** chốt tĩnh không đo NGỮ NGHĨA của `_con_song` — `SX_d0`, `SW_d`, `SW_d0`, `M4`, `M5`,
    `D0_KIEMDL`, hai đột biến (a), (b) của "Chốt ngược" đều ĐẠT chốt tĩnh; bảng không gian mở rộng, helper và B8 đo phần
    ấy. `subprocess.run` là cặp có sẵn ở `_con_song` nền nên T6 cho qua tiến trình con trong `_con_song` (`cs_subprocess`
    ĐẠT; helper bắt: `t156` `B2-nhanh-cu song read count 0`, ba Python). Khoá bytes bỏ giải mã qua `K` (chốt động bắt:
    hàng `g_to_hop_dinh_dang_khoa` của bảng B8). Cách viết hợp lệ khác bị ĐỎ ồn ào thay vì xanh giả: khoá bytes bằng
    `%` (`K`), hàm trợ giúp `async def` (`M`), tên dựng sẵn ngoài danh sách (`T3`), sửa docstring của ba hàm (`H`) —
    muốn nhận thì mở rộng danh sách bằng revision mới.
    **(r13, cross-review lượt 12) Chốt tĩnh là phép kiểm CÁCH VIẾT TRỰC TIẾP, không phải hộp cát.** `T3`, `T6` xét tên
    toàn cục và cặp (tên toàn cục, thuộc tính) ở dạng viết thẳng; thuộc tính trên một biến cục bộ hay một biểu thức
    không bị xét. Đo lượt 12 (3.11, 3.13; bản RIG dựng từ một ứng viên đúng, KHÔNG phải đường tự nhiên của executor):
    trong thân `_con_song`, bí danh `m = os` rồi `m.sys.modules['builtins'].setattr(platform, 'system', …)`, dạng
    `[os][0].sys…`, khung generator `(x for x in ()).gi_frame.f_globals.update(…)` và `….gi_frame.f_builtins['setattr']`
    — cả bốn ĐẠT chốt tĩnh (rc=0) và đổi hành vi ba hàm canh ngay sau MỘT lời gọi `_con_song`. B8 bắt hai (`t160`, `t161`
    `124 noi doi`); bản gán lại `_thanh_vien_nhom` thành hàm trả `[]` qua `gi_frame.f_globals` QUA cả bốn ca B8, và với
    cháu CÙNG NHÓM sinh SAU ảnh chụp (mẹ có handler SIGTERM sinh cháu phớt lờ SIGTERM) `_giet_cay` trả `tron_ven=True`
    ("SIGTERM: cay da sach") khi cháu còn sống — ba Python; nền và ứng viên đúng SIGKILL được cháu. Phần gián tiếp vì
    vậy là GIỚI HẠN đã khai, không tiêu chí nào đỏ. Siết được: `T6` thành danh sách cho phép TÊN thuộc tính trên MỌI
    gốc (tên thuộc tính của `_con_song` nền cộng `read_bytes`, `decode`) và tên module chỉ làm gốc trực tiếp của một cặp
    nền — đo lượt 12 trên bản sao RIG của script: hai ứng viên và sáu bản hợp lệ ĐẠT, 0 đối chứng hỏng, năm bản gián
    tiếp ĐỎ; nhưng đó là revision mới với băm script mới, không bắt buộc cho packet này.

```python
# chot_tinh_r12.py - CHOT TINH cua dac ta wp685 r12 (§7 B2). MA KIEM THUAN cua dac ta: executor chay NGUYEN VAN
# (trich bang may tu dac ta, doi chieu sha256 cua khoi), KHONG dan xuat lai.
# Dung: python3.11 chot_tinh_r12.py <launcher.py NEN> <launcher.py UNG VIEN> <launcher_test.py UNG VIEN>
# Ma thoat: 0 = DAT (ung vien qua moi luat VA moi doi chung DO dung luat); 1 = ung vien DO; 2 = co doi chung
# khong DO dung luat hay khong dung duoc (chot mat rang); 3 = dau vao hong (doc/parse nen, hinh dang nen la,
# DANG_DOC_QA7 thieu hay ngoai danh sach).
# Luat (ma luat dung dau moi dong loi):
#   H  ba ham canh: CA nut `def` (decorator, chu ky, docstring, than) BANG nen theo AST sau DUNG phep doi cua dang
#      doc da khai, va chi trong than nhanh `if he == "Linux":`. Chu thich `#` khong vao AST nen dat o dau cung duoc.
#   K  (chi dang bytes) bieu thuc dung khoa `linux:` la cho trong: chi ghep `sau[19]` DUNG mot lan bang f-string,
#      `+`, `.decode(...)`, `int()`, `str()`.
#   M  muc module: moi cau lenh ngoai bon ham (`_con_song` va ba ham canh) BANG nen theo AST, tru gia tri chuoi cua
#      `VERSION`; chi duoc THEM cau `def` ten moi (khong trung ten muc module cua nen, khong trung ten dung san).
#   T1..T7 `_con_song` va moi `def` moi: T1 khong global/nonlocal; T2 khong import (nen khong co); T3 ten toan cuc
#      doc duoc thuoc {ten toan cuc cua `_con_song` nen} + TEN_THEM + ten cac `def` moi; T4 khong thuoc tinh dunder;
#      T5 khong gan/xoa thuoc tinh hay chi so; T6 thuoc tinh cua ten toan cuc chi la cap (ten, thuoc tinh) co trong
#      `_con_song` nen; T7 decorator, chu ky cua `_con_song` BANG nen, `def` moi khong decorator, khong gia tri mac dinh.
import ast
import builtins
import copy
import hashlib
import symtable
import sys

CANH = ("_khoa_danh_tinh", "_thanh_vien_nhom", "_chup_cay")
TU_DO = "_con_song"
BON = CANH + (TU_DO,)
# Hinh dang nen trong than nhanh Linux: [loi goi .read_text() khong doi so, hang ")", hang "Z", f-string "linux:..."]
HINH = {"_khoa_danh_tinh": [1, 1, 0, 1], "_thanh_vien_nhom": [1, 1, 1, 0], "_chup_cay": [1, 1, 1, 1]}
DANG_CHO_PHEP = (("read_text", (), {"encoding": "latin-1"}), ("read_bytes", (), {}))
TEN_THEM = ("UnicodeDecodeError", "bytes", "int", "len", "isinstance", "bool")
KHE = "KHE_KHOA_TU_DO"
NL = chr(10)


class Hong(Exception):
    pass


def so(a, b, d):
    """So cau truc hai cay AST (khong so vi tri dong/cot); tra (ma, duong) o cho lech dau tien, None neu bang."""
    if isinstance(a, ast.Name) and a.id == KHE:
        return None if khoa_hop_le(b) else ("K", d)
    if isinstance(a, ast.AST):
        if type(a) is not type(b):
            return ("=", d + " " + type(a).__name__ + "/" + type(b).__name__)
        for f in a._fields:
            r = so(getattr(a, f, None), getattr(b, f, None), d + "." + f)
            if r:
                return r
        return None
    if isinstance(a, list):
        if not isinstance(b, list) or len(a) != len(b):
            return ("=", d + " so phan tu")
        for i, (x, y) in enumerate(zip(a, b)):
            r = so(x, y, d + "[" + str(i) + "]")
            if r:
                return r
        return None
    return None if (type(a) is type(b) and a == b) else ("=", d + " " + repr(a)[:30] + "/" + repr(b)[:30])


def khoa_hop_le(e):
    if not isinstance(e, ast.expr):
        return False
    n = 0
    for x in ast.walk(e):
        if isinstance(x, ast.Subscript):
            s = x.slice
            if not (isinstance(x.value, ast.Name) and x.value.id == "sau" and isinstance(s, ast.Constant)
                    and type(s.value) is int and s.value == 19):
                return False
            n += 1
        elif isinstance(x, ast.Call):
            f = x.func
            if not ((isinstance(f, ast.Name) and f.id in ("int", "str"))
                    or (isinstance(f, ast.Attribute) and f.attr == "decode")):
                return False
        elif isinstance(x, ast.Name):
            if x.id not in ("sau", "int", "str"):
                return False
        elif isinstance(x, ast.Attribute):
            if x.attr != "decode":
                return False
        elif not isinstance(x, (ast.JoinedStr, ast.FormattedValue, ast.Constant, ast.BinOp, ast.Add, ast.Load,
                                ast.keyword)):
            return False
    return n == 1


def la_linux(n):
    t = getattr(n, "test", None)
    return (isinstance(n, ast.If) and isinstance(t, ast.Compare) and isinstance(t.left, ast.Name)
            and t.left.id == "he" and len(t.ops) == 1 and isinstance(t.ops[0], ast.Eq)
            and len(t.comparators) == 1 and isinstance(t.comparators[0], ast.Constant)
            and t.comparators[0].value == "Linux")


class DoiKhoa(ast.NodeTransformer):
    def __init__(self, khe):
        self.n, self.khe = 0, khe

    def visit_JoinedStr(self, x):
        if x.values and isinstance(x.values[0], ast.Constant) and str(x.values[0].value).startswith("linux:"):
            self.n += 1
            if self.khe:
                return ast.Name(id=KHE, ctx=ast.Load())
        return x


def mong_doi(ham, dang):
    """Ham nen sau phep doi DUY NHAT duoc phep, CHI trong than nhanh `if he == "Linux":`."""
    e = copy.deepcopy(ham)
    nhanh = [n for n in ast.walk(e) if la_linux(n)]
    if len(nhanh) != 1:
        raise Hong(ham.name + ": nen co " + str(len(nhanh)) + " nhanh Linux")
    ten, a, k = dang
    la_bytes = ten == "read_bytes"
    dk = DoiKhoa(la_bytes)
    nhanh[0].body = [dk.visit(c) for c in nhanh[0].body]
    dem = [0, 0, 0, dk.n]
    for c in nhanh[0].body:
        for x in ast.walk(c):
            if (isinstance(x, ast.Call) and isinstance(x.func, ast.Attribute) and x.func.attr == "read_text"
                    and not x.args and not x.keywords):
                dem[0] += 1
                x.func.attr = ten
                x.args = [ast.Constant(value=v) for v in a]
                x.keywords = [ast.keyword(arg=kk, value=ast.Constant(value=vv)) for kk, vv in k.items()]
            elif isinstance(x, ast.Constant) and type(x.value) is str and x.value in (")", "Z"):
                dem[1 if x.value == ")" else 2] += 1
                if la_bytes:
                    x.value = x.value.encode()
    if dem != HINH[ham.name]:
        raise Hong(ham.name + ": hinh dang nen " + str(dem) + " != " + str(HINH[ham.name]))
    return e


def la_def(n):
    return isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef))


def dinh(t):
    d = {}
    for n in t.body:
        if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef, ast.ClassDef)):
            d.setdefault(n.name, []).append(n)
    return d


def toan_cuc(tb):
    ra = set()
    for s in tb.get_symbols():
        if s.is_global() or s.is_declared_global():
            ra.add(s.get_name())
    for c in tb.get_children():
        ra |= toan_cuc(c)
    return ra


def bang_ham(top, ten):
    v = [c for c in top.get_children() if c.get_name() == ten and str(c.get_type()).lower().endswith("function")]
    return v[0] if len(v) == 1 else None


def la_version(n):
    return (isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name)
            and n.targets[0].id == "VERSION" and isinstance(n.value, ast.Constant) and type(n.value.value) is str)


class Nen:
    def __init__(self, t):
        self.t = t
        d = dinh(t)
        for h in BON:
            if len(d.get(h, [])) != 1:
                raise Hong("nen: " + h + " khong phai dung mot def muc module")
        self.ham = {h: d[h][0] for h in BON}
        top = symtable.symtable(ast.unparse(t), "nen", "exec")
        self.ten_module = {s.get_name() for s in top.get_symbols()} | set(dir(builtins))
        self.g = toan_cuc(bang_ham(top, TU_DO))
        f = self.ham[TU_DO]
        self.cap = {(x.value.id, x.attr) for x in ast.walk(f)
                    if isinstance(x, ast.Attribute) and isinstance(x.value, ast.Name) and x.value.id in self.g}
        self.imp = [ast.dump(x) for x in ast.walk(f) if isinstance(x, (ast.Import, ast.ImportFrom))]


def kiem(nen, u, dang):
    loi = []
    d = dinh(u)
    for h in BON:
        if len(d.get(h, [])) != 1:
            loi.append("M " + h + ": " + str(len(d.get(h, []))) + " def muc module, phai dung 1")
    for h in CANH:
        if len(d.get(h, [])) == 1:
            r = so(mong_doi(nen.ham[h], dang), d[h][0], h)
            if r:
                loi.append(("K " if r[0] == "K" else "H ") + r[1])
    moi, giu_u = [], []
    for n in u.body:
        if la_def(n) and n.name in BON:
            continue
        if isinstance(n, ast.FunctionDef) and n.name not in nen.ten_module:
            moi.append(n)
            continue
        giu_u.append(n)
    giu_n = [n for n in nen.t.body if not (la_def(n) and n.name in BON)]
    ten_moi = [n.name for n in moi]
    if len(set(ten_moi)) != len(ten_moi):
        loi.append("M def moi trung ten: " + ",".join(sorted(ten_moi)))
    vn = [n for n in giu_n if la_version(n)]
    if len(vn) == 1:        # CHI gia tri chuoi cua VERSION duoc doi: chuan hoa ve nen truoc khi so
        giu_u = [ast.Assign(targets=n.targets, value=vn[0].value) if la_version(n) else n for n in giu_u]
    r = so(giu_n, giu_u, "muc module")
    if r:
        i = r[1][len("muc module["):].split("]")[0] if r[1].startswith("muc module[") else ""
        x = giu_u[int(i)] if i.isdigit() and int(i) < len(giu_u) else None
        loi.append("M " + r[1] + " | dong ung vien " + str(getattr(x, "lineno", "?")))
    top = symtable.symtable(ast.unparse(u), "ung_vien", "exec")
    cho = nen.g | set(TEN_THEM) | set(ten_moi)
    ds = ([d[TU_DO][0]] if len(d.get(TU_DO, [])) == 1 else []) + moi
    for f in ds:
        tb = bang_ham(top, f.name)
        if tb is None:
            loi.append("T3 " + f.name + ": khong tim thay bang ky hieu")
            continue
        g = toan_cuc(tb)
        for n in ast.walk(f):
            dong = " dong " + str(getattr(n, "lineno", "?"))
            if isinstance(n, (ast.Global, ast.Nonlocal)):
                loi.append("T1 " + f.name + ":" + dong + " " + type(n).__name__ + " " + ",".join(n.names))
            elif isinstance(n, (ast.Import, ast.ImportFrom)) and ast.dump(n) not in nen.imp:
                loi.append("T2 " + f.name + ":" + dong + " import")
            elif isinstance(n, ast.Attribute):
                if n.attr.startswith("__") and n.attr.endswith("__"):
                    loi.append("T4 " + f.name + ":" + dong + " ." + n.attr)
                if not isinstance(n.ctx, ast.Load):
                    loi.append("T5 " + f.name + ":" + dong + " gan/xoa ." + n.attr)
                if isinstance(n.value, ast.Name) and n.value.id in g and (n.value.id, n.attr) not in nen.cap:
                    loi.append("T6 " + f.name + ":" + dong + " " + n.value.id + "." + n.attr)
            elif isinstance(n, ast.Subscript) and not isinstance(n.ctx, ast.Load):
                loi.append("T5 " + f.name + ":" + dong + " gan/xoa chi so")
        la = sorted(g - cho)
        if la:
            loi.append("T3 " + f.name + ": ten toan cuc ngoai danh sach " + ",".join(la))
        if f.name == TU_DO:
            for fld in ("decorator_list", "args", "returns"):
                r = so(getattr(nen.ham[TU_DO], fld), getattr(f, fld), TU_DO + "." + fld)
                if r:
                    loi.append("T7 " + r[1])
        elif f.decorator_list or f.args.defaults or any(x is not None for x in f.args.kw_defaults):
            loi.append("T7 " + f.name + ": def moi co decorator hay gia tri mac dinh")
    return loi


def ham_cua(t, ten):
    v = [n for n in t.body if la_def(n) and n.name == ten]
    if len(v) != 1:
        raise Hong("khong dung duoc doi chung: " + ten + " co " + str(len(v)) + " def")
    return v[0]


def cau(s):
    return ast.parse(s).body


def dc_nen(nen, u):
    return copy.deepcopy(nen.t)


def dc_tach(nen, u):
    t = copy.deepcopy(u)
    x = [n for n in ast.walk(ham_cua(t, "_khoa_danh_tinh")) if isinstance(n, ast.Attribute) and n.attr == "rindex"]
    if len(x) != 1:
        raise Hong("khong dung duoc doi chung tach: " + str(len(x)) + " .rindex")
    x[0].attr = "index"
    return t


def dc_deco(nen, u):
    t = copy.deepcopy(u)
    ham_cua(t, "_thanh_vien_nhom").decorator_list.append(ast.parse("_chup_cay", mode="eval").body)
    return t


def dc_gan_lai(nen, u):
    t = copy.deepcopy(u)
    i = t.body.index(ham_cua(t, "_thanh_vien_nhom"))
    t.body[i + 1:i + 1] = cau("_thanh_vien_nhom = _thanh_vien_nhom")
    return t


def dc_def_trung(nen, u):
    t = copy.deepcopy(u)
    t.body += cau("def Path():" + NL + "    return None")
    return t


def dc_con_song(dong):
    def dung(nen, u):
        t = copy.deepcopy(u)
        f = ham_cua(t, TU_DO)
        f.body[0:0] = cau(dong)
        return t
    return dung


def dc_mac_dinh(nen, u):
    t = copy.deepcopy(u)
    f = ham_cua(t, TU_DO)
    if len(f.args.defaults) != 1:
        raise Hong("khong dung duoc doi chung mac dinh")
    f.args.defaults[0] = ast.Constant(value=1)
    return t


def dc_phu(nen, u):
    t = copy.deepcopy(u)
    t.body += cau("def _dc_ham_moi():" + NL + "    global os" + NL + "    return None")
    return t


def dc_khoa(nen, u):
    t = copy.deepcopy(u)
    f = ham_cua(t, "_khoa_danh_tinh")
    v = [n for n in ast.walk(f) if isinstance(n, ast.Return) and n.value is not None
         and any(isinstance(s, ast.Subscript) and isinstance(s.slice, ast.Constant) and s.slice.value == 19
                 for s in ast.walk(n.value))]
    if len(v) != 1:
        raise Hong("khong dung duoc doi chung khoa")
    v[0].value = ast.parse(chr(34) + "linux:" + chr(34) + " + str(pid)", mode="eval").body
    return t


DOI_CHUNG = [
    ("nen", "H", dc_nen),
    ("tach_ngoac_dau", "H", dc_tach),
    ("decorator", "H", dc_deco),
    ("gan_lai_muc_module", "M", dc_gan_lai),
    ("def_ten_cu", "M", dc_def_trung),
    ("global", "T1", dc_con_song("global os")),
    ("import", "T2", dc_con_song("import os")),
    ("setattr", "T3", dc_con_song("setattr(pid, 'x', 1)")),
    ("dunder", "T4", dc_con_song("pid.__class__")),
    ("gan_thuoc_tinh", "T5", dc_con_song("pid.x = 1")),
    ("thuoc_tinh_toan_cuc", "T6", dc_con_song("os.open")),
    ("mac_dinh", "T7", dc_mac_dinh),
    ("def_moi_global", "T1", dc_phu),
    ("khoa_bytes", "K", dc_khoa),
]


def doc_dang(src):
    v = [n for n in ast.parse(src).body if isinstance(n, ast.Assign) and len(n.targets) == 1
         and isinstance(n.targets[0], ast.Name) and n.targets[0].id == "DANG_DOC_QA7"]
    if len(v) != 1:
        raise Hong("DANG_DOC_QA7: " + str(len(v)) + " phep gan muc module, phai dung 1")
    dang = ast.literal_eval(v[0].value)
    if dang not in DANG_CHO_PHEP:
        raise Hong("DANG_DOC_QA7 ngoai danh sach cho phep: " + repr(dang))
    return dang


def main(argv):
    if len(argv) != 4:
        print("dung: chot_tinh_r12.py <launcher.py nen> <launcher.py ung vien> <launcher_test.py ung vien>")
        return 3
    try:
        b = [open(p, "rb").read() for p in argv[1:4]]
        dang = doc_dang(b[2].decode("utf-8"))
        nen = Nen(ast.parse(b[0].decode("utf-8")))
        for h in CANH:
            mong_doi(nen.ham[h], dang)
    except (OSError, SyntaxError, ValueError, Hong) as e:
        print("DAU VAO HONG:", type(e).__name__, e)
        return 3
    print("CHOT TINH r12 | python", sys.version.split()[0], "| sha256 nen", hashlib.sha256(b[0]).hexdigest(),
          "| ung vien", hashlib.sha256(b[1]).hexdigest(), "| test", hashlib.sha256(b[2]).hexdigest(),
          "| DANG_DOC_QA7", repr(dang))
    try:
        u = ast.parse(b[1].decode("utf-8"))
    except (SyntaxError, ValueError) as e:
        print("UNG VIEN: DO 1 | P khong parse duoc:", e)
        return 1
    try:
        loi = kiem(nen, u, dang)
    except Hong as e:
        print("DAU VAO HONG:", e)
        return 3
    print("UNG VIEN:", "DAT" if not loi else "DO " + str(len(loi)) + " | " + " ; ".join(loi))
    hong_dc = 0
    for ten, ma, dung in DOI_CHUNG:
        if ma == "K" and dang[0] != "read_bytes":
            print("DOI CHUNG", ten, "[K]: khong ap dung (dang latin-1: bieu thuc khoa phai BANG nen, luat H)")
            continue
        try:
            moi = [x for x in kiem(nen, dung(nen, u), dang) if x not in loi]
        except Hong as e:
            print("DOI CHUNG", ten, "[" + ma + "]: KHONG DUNG DUOC |", e)
            hong_dc += 1
            continue
        dung_luat = bool(moi) and all(x.split(" ", 1)[0] == ma for x in moi)
        print("DOI CHUNG", ten, "[" + ma + "]:", "DO DUNG LUAT" if dung_luat else "KHONG DO DUNG LUAT",
              "|", " ; ".join(moi)[:200])
        hong_dc += 0 if dung_luat else 1
    rc = 1 if loi else (2 if hong_dc else 0)
    print("KET LUAN:", {0: "DAT", 1: "DO (ung vien)", 2: "DO (doi chung khong do dung luat)"}[rc], "| rc=" + str(rc))
    return rc


if __name__ == "__main__":
    sys.exit(main(sys.argv))
```

    Khối trên: 412 dòng, sha256 `add42b31beeaece6e3cf546d3915a153099bfe7a232995b0e1546bbd4a5735b6`, 0 dấu chéo ngược —
    trùng từng byte tệp đã chạy ở mọi phép đo chốt tĩnh của bảng 14.

    **Trục N — nơi gọi** (§2): `:607` (`_con_song_dung_khoa`) — đo qua `B1` (trực tiếp và qua `_giet_rieng`),
    `B3-zombie`, và `B3b-giet-cay` (`_giet_cay` → `_con_lai` → `:607`); `:857`, `:882` (`_giet_windows`) — nhánh
    Windows, ngoài phạm vi (Q-A.6); `:1020`, `:1039` (`_giet_cay` khi `_con_lai` trả `None`, tức không đo được cây)
    — không đầu vào nào của hai ca đi qua, nhưng ĐO ĐƯỢC bằng một seam (r8, cross-review lượt 7): `Path.iterdir`
    ném EACCES riêng cho `/proc` ⇒ `_chup_cay`, `_thanh_vien_nhom` trả `None` ⇒ `_con_lai()` là `None`. Con sống,
    seam EACCES ở `Path.stat`: ứng viên nháp ⇒ `tron_ven=False`, **125** ("SIGTERM: me da chet, KHONG do duoc cay",
    0,10 giây); đột biến (c) ⇒ **125** (2,31 giây) — số của reviewer lượt 7 (3.12.3); phiên soạn r8 đo lại ở ba
    Python, cùng kết quả (bảng 10 dòng 8). Hai nơi ấy dựng `KetGiet(…, False, …)` — `ca_cay` viết cứng
    `False` — nên mã LUÔN là 125; `_con_song` ở đó chỉ đổi `me_da_chet` và thời lượng. Không có rủi ro 124/125 do
    bản vá tại hai nơi ấy; không bắt buộc thêm đầu vào.

    **Trục G — dạng phép đọc (r9, Q-A.7).** Năm hạng mục, mỗi chỗ đọc `/proc/<pid>/stat` một hạng mục, hướng "lệch
    dạng" (đọc bằng dạng ngoài danh sách cho phép): `g_khoa` (`_khoa_danh_tinh`), `g_nhom` (`_thanh_vien_nhom`),
    `g_chup` (`_chup_cay`), `g_d0`, `g_d` (hai khối đọc của `_con_song`). Đầu vào: bốn ca B8 (hành vi đầu-cuối);
    `read args` ở mọi đầu vào có đếm đọc của `t156_...` (G-Đ0, G-Đ) và ở `t160`, `t161` (mọi lời đọc trong cửa sổ, cả
    năm chỗ); hai đầu vào nội dung thật và đuôi `comm` của `B3-zombie` (hành vi khi đối số đúng). Đóng bằng MỘT biến
    thể E mỗi hạng mục: M1–M5 của B8 (trả lời đọc về `read_text()` không đối số). Thêm cho hạng mục sẵn có, không tăng
    số hạng mục: `d0_giai_ma_long`, `d_giai_ma_long` (`errors="replace"` ở G-Đ0, G-Đ); `g_khoa_errors`, `g_nhom_errors`,
    `g_chup_errors` (`errors="surrogateescape"` ở ba hàm ngoài `_con_song`: hành vi đúng ở locale UTF-8, chỉ `read
    args` của `t160`/`t161` bắt được); `d0_giai_ma_lai_utf8`, `d_giai_ma_lai_utf8` (đúng đối số, giải mã lại UTF-8 sau
    khi đọc — răng riêng của hai đầu vào nội dung thật). Tổ hợp `g_to_hop_khoa_nhom` = M12 (B8). Số đo: bảng 11. (r10)
    Tổ hợp `g_to_hop_dinh_dang_khoa` (B8, Q-A.7 "định dạng khoá có CHỐT"): dạng bytes bỏ giải mã trường số ở CẢ HAI chỗ
    dựng khoá (`_khoa_danh_tinh`, `_chup_cay`) — đúng đối số, sai định dạng khoá; miễn "một vị trí" như M12, cùng lý do:
    mỗi vị trí đơn lẻ đã bị `t160`, `t161` giết (hai hàng đối chiếu của bảng B8; lượt 9 và bảng 12, ba Python), chỉ
    tổ hợp nhất quán mới né được thước đo nội bộ — và bị khoá độc lập `_k124_khoa_that` bắt (Q-A.7). (r11,
    cross-review lượt 10, lớp `khoa-dinh-dang-khong-co-chot`) **Định nghĩa chung cho CẢ HAI dạng của Q-A.7:** biến thể
    `g_to_hop_dinh_dang_khoa` là MỘT định dạng khoá khác nền `linux:<chuỗi thập phân ASCII>`, NHẤT QUÁN ở cả hai chỗ
    dựng khoá, đúng đối số đọc. Dạng bytes: bỏ bước giải mã trường số (khoá `linux:b'…'`). Dạng latin-1 — không có bước
    giải mã để bỏ — dùng `!r` ở cả hai chỗ (`f"linux:{sau[19]!r}"`, khoá `linux:'…'`). Tự liệt kê (r11): hai dạng × ba
    tổ hợp vị trí (chỉ `_khoa_danh_tinh`, chỉ `_chup_cay`, cả hai) = sáu bản; nơi SO khoá (`:607`, `:896`, `:921`,
    `lenh_stop` qua `run.json`) chỉ so chuỗi, không dựng — không cần hàng riêng. Đo cả sáu trên khối r11, ba Python
    (bảng 13): dạng nào cũng vậy — cả hai chỗ ⇒ `t160` `khong giet duoc` (khoá KHÁC), ba ô kia QUA; chỉ
    `_khoa_danh_tinh` ⇒ `t160` `khong giet duoc`, `t161` `124 noi doi`; chỉ `_chup_cay` ⇒ `t160`, `t161` `124 noi doi`
    — trùng số lượt 10 và bảng 12. Mỗi vị trí đơn lẻ đã bị giết, nên miễn "một vị trí" giữ nguyên lý do.

    **Kiểm đếm bảng mở rộng** (đếm từ bảng; biến thể và kết quả đo ở bảng 9, 10 và 11): 30 ô (6 hàng × 5 tầng), ô nào cũng
    có đầu vào. **129 hạng mục**:
    · 95 hạng mục thoát/sai/bắt/bọc = 53 ở 15 ô r6 (42 theo cách đếm của r6, cộng 11 hướng bọc) + 42 ở 15 ô mới
      (hàng R0: 8; cột Đ0: 18; cột K0: 16). Có dòng B5: **45** (42 của r6, cộng (m1), (m2), (m3)). Có biến thể E: **50**
      (11 hướng bọc cũ, cộng 39 hạng mục mới).
    · 19 hạng mục thay thế (H 5, Đ 2, K 5, Đ0 2, K0 5): 19 biến thể E, kỳ vọng ca ĐỎ bằng lỗi vô can.
    · 13 hạng mục đếm (trục C: hỏi trên 6 đường, đọc trên 4, kill trên 3): 5 có dòng B5 ((m4); (f); (j1) cùng (c);
      (j2); (k1) cùng (k5)), 8 có biến thể E (một trong số ấy là bản vá sai của lượt 6).
    · 2 hạng mục cú pháp: (m5) và một biến thể E.
    Tổng: 54 dòng B5 phủ 51 hạng mục (ba cặp dòng chung hạng mục: (l15)/(l16), (c)/(j1), (k1)/(k5)); 78 hạng mục có
    biến thể E. Không hạng mục nào chỉ có lời văn. Đo trên rig r7 (bảng 9 dòng 2 và 6, ba Python): 55/55 cặp của 54
    dòng được chấp nhận; 87 biến thể E có kỳ vọng "chết" hay "đỏ" đều đúng kỳ vọng — 78 biến thể hạng mục, 5 bản vá
    sai khác của lượt 6 (trùng (m1)–(m5)), 2 biến thể lặp có điều kiện, 2 đối chứng của luật `B2-parse` — và hai đối
    chứng kỳ vọng sống thì sống.
    **(r9)** Trục G thêm **5** hạng mục ⇒ **134 hạng mục**; 54 dòng B5 vẫn phủ 51; **83** hạng mục có biến thể E
    (78 + 5). Bộ (E) của r11: **118 dòng** = 83 hạng mục + 35 dòng khác (r10: 110 = 83 + 27; r9: 109 = 83 + 26) — 12
    biến thể thêm của trục G (r11 thêm năm `g_*_open`, một cho mỗi chỗ đọc), 3 biến thể trục S ở ba hàm ngoài (r11), 2
    tổ hợp (M12; r10 thêm `g_to_hop_dinh_dang_khoa`), 2
    biến thể lặp có điều kiện (`d_doc_lai_khi_EPERM`, `k_kill_lai_khi_doc_EPERM`), 5 bản vá sai của lượt 6 trùng
    (m1)–(m5), 8 đối chứng luật `B2-parse` (khác đối số; fp; fp2–fp6; fp6b), 1 đối chứng loại (2) ((j1) sai đối số), 2
    đối chứng sống — cộng 2 phép giả gọi lại hàm trợ giúp nếu ứng viên tách trong hàm trợ giúp. Danh sách tên ĐÓNG:
    (E) mục 6. Bộ 95 của r8 và bộ 89 của r7: đoạn này của r8 (sha256 `2ae6ee04…2aa3`).

    **Ô hoặc phần của ô bất khả thi / `KHÔNG ĐO ĐƯỢC` — mỗi cái kèm lý do và phép đo** (không ô nào bị bỏ trống
    mà không nói):
    1. R3-H tại seam `Path.stat`, thành viên `ValueError` và `UnicodeDecodeError`: **bất khả thi** ở seam ấy —
       `exists()` nuốt chúng trước khi tới launcher (bảng 7, ba bản Python, 16:20:07Z 29-09). Đo được ở seam
       `Path.exists`, nên ba đầu vào của R3-H dùng seam đó. `IndexError` đo được ở cả hai seam; chọn `Path.exists`
       cho đồng nhất.
    2. R3-H và R3-K: **KHÔNG ĐO ĐƯỢC** (lý do 4) rằng hệ điều hành hay `pathlib` thật có bao giờ sinh nhóm phân tích ở
       hai tầng ấy. Nguồn tự nhiên chưa biết, sentinel do ca dựng; ô đo hợp đồng "thoát nguyên", không đo tần suất.
    3. R2 ở cả ba tầng: errno là tập MỞ. EACCES, EPERM, EIO là ba đại diện; bản vá nhận đúng ba errno ấy và
       từ chối errno thứ tư (ví dụ ENOMEM) qua nghiệm thu. **KHÔNG ĐO ĐƯỢC** (lý do 4) cho errno thứ tư trở đi. Phân nhánh
       theo errno (danh sách trắng hai hoặc ba errno; EPERM riêng) đã có đột biến: (l4), (l5), (l11), (l12), (l13).
    4. R2-K, thành viên EACCES: gộp vào EPERM — `PermissionError` là lớp chung của hai errno và mệnh đề bắt
       giống hệt. `os.kill(pid, 0)` trả EACCES trên kernel thật: r7–r10 ghi "KHÔNG ĐO ĐƯỢC (chưa thử)" — sai nhãn, chưa
       thử không phải không đo được (lớp `khai-khong-do-duoc-ma-do-duoc`). **(r11) ĐÃ THỬ:** dưới uid 65534,
       `os.kill(pid, 0)` trên mọi PID trong `/proc` (2329–2331 PID) ⇒ EPERM ở mọi PID khác chủ, thành công ở chính nó,
       ESRCH với hai PID ngoài `pid_max`, **0 EACCES**, ba Python (bảng 13). Trên các PID đã thử kernel không sinh
       EACCES ở phép này; gộp vào EPERM là gộp một thành viên chỉ seam sinh ra.
    5. Lớp ngoại lệ ngoài năm hàng: con của `OSError` như `TimeoutError`, `InterruptedError`, `BlockingIOError`
       đi cùng R2 (mệnh đề `OSError`); `MemoryError`, `RecursionError`, `TypeError` đi cùng R4; `SystemExit`,
       `GeneratorExit` đi cùng R5. Không có đầu vào riêng — bộ tương đương theo LỚP CHA mà mọi mệnh đề tự
       nhiên bắt. Đột biến liệt kê riêng một lớp con (ví dụ `except (OSError, MemoryError)`) không có đầu vào động,
       nhưng phần lớn ĐO ĐƯỢC bằng chốt tĩnh (r14, cross-review lượt 13; r6 đến r13 ghi "KHÔNG ĐO ĐƯỢC", r12 gắn lý do 4
       đúng ở revision thêm luật `T3`). Bốn hạng; hạng thứ nhất, thứ hai và thứ tư đo trên HAI ứng viên — ứng viên độc
       lập của lượt 13 (VERDICT lượt 13, HƯỚNG 12) và ứng viên tham chiếu r13 (bảng 16 dòng 10, 11) —, hạng thứ ba chỉ
       trên ứng viên tham chiếu:
       · Tập lớp nêu TRỰC TIẾP được trong `_con_song` và `def` mới là ĐÓNG: `T3` cho 17 tên, trong đó 6 lớp ngoại lệ
         (`IndexError`, `OSError`, `PermissionError`, `ProcessLookupError`, `UnicodeDecodeError`, `ValueError` — lớp nào
         cũng có đầu vào ở R1–R3); `T6` cho 4 cặp, trong đó 1 lớp (`subprocess.SubprocessError`). Tên lớp NGOÀI tập ấy ⇒
         chốt tĩnh ĐỎ, rc=1 (`python3.11`), theo cách nêu (r15, cross-review lượt 14 đo; r14 chỉ ghi dạng thứ nhất): tên
         toàn cục ⇒ `T3 <hàm>: ten toan cuc ngoai danh sach <tên>`; thuộc tính của một tên toàn cục được phép, ví dụ
         `subprocess.TimeoutExpired` hay `os.error` ở tầng hỏi ⇒ `T6 <hàm>: dong <n> <tên>` —, trong khi `t156`, `t157`,
         `t160`, `t161` QUA (`python3.12`): lượt 13 đo năm bản (chính ví dụ trên ở tầng hỏi, `LookupError` và
         `ArithmeticError` ở tầng đọc, hỏi lại khi `InterruptedError`, `TimeoutError` riêng ở Đ0), r14 đo ba (`MemoryError`
         ở tầng hỏi, hỏi lại khi `InterruptedError`, `TimeoutError` riêng ⇒ `True` ở Đ0).
       · `subprocess.SubprocessError` — lớp DUY NHẤT của tập đóng không có đầu vào: `except (OSError,
         subprocess.SubprocessError)` ở tầng hỏi ĐẠT chốt tĩnh và QUA bốn ca ở cả hai ứng viên (đo). Một đầu vào seam ném
         đúng lớp ấy ở tầng hỏi (kỳ vọng "thoát nguyên" như R4) dựng được: CHƯA ĐO — r14 không thêm, vì thêm đầu vào là đổi
         bảng không gian, bảng tiểu nhãn và các số kỳ vọng (D, §8), còn chỉ thị của lượt này là thu hẹp lời khai. Hậu
         quả trên đầu vào thật chỉ có khi phép hỏi thật ném lớp ấy; `stat` thật có bao giờ ném nó: KHÔNG ĐO ĐƯỢC (lý do
         4). (HINT lượt 13 viết "`stat` không ném nó nên mệnh đề ấy vô hại về hành vi" — một lời khai "không bao giờ"
         không nhãn.)
       · Lớp nêu GIÁN TIẾP — thuộc tính trên một biểu thức, không trên tên toàn cục: r14 đo hỏi lại khi
         `[os][0].sys.modules["builtins"].InterruptedError` ⇒ ĐẠT chốt tĩnh rc=0, QUA bốn ca. Đây là giới hạn đã khai của
         chốt tĩnh (B2, "Chốt tĩnh là phép kiểm CÁCH VIẾT TRỰC TIẾP, không phải hộp cát"; phương án siết `T6` ở đó là
         revision mới).
       · Phân nhánh theo errno SỐ (hỏi lại khi `e.errno == 4`; `e.errno == 12` ⇒ `True` ở khối kill): ĐẠT chốt tĩnh và QUA
         bốn ca ở cả hai ứng viên (đo). Bắt được MỌI errno thứ tư: **KHÔNG ĐO ĐƯỢC** (lý do 4), như mục 3.
    6. Mở rộng phạm vi khối `try` sang thêm câu lệnh (bọc luôn `kill` vào khối đọc): không có dạng tự nhiên đã
       biết cho đường lỗi này; hệ quả của nó — nhóm phân tích bị bắt ở tầng K — đã đo qua R3-K.
    7. (r7) R2-K0, thành viên EACCES: gộp vào EPERM như R2-K (mục 4), cùng lý do.
    8. (r7) Cột Đ0 dùng MỘT payload cho mỗi thành viên nhóm phân tích (`p1` rỗng cho `ValueError`, `p3` không khoảng
       trắng cuối cho `IndexError`); `p2` và payload thứ hai của `p3` không lặp lại ở Đ0. Hình dạng "kiểm tra dữ liệu
       thay cho bắt ngoại lệ" ở nhánh cũ (như (l16) ở nhánh mới): r7–r10 ghi "KHÔNG ĐO ĐƯỢC" (chưa có biến thể), sai
       nhãn (chưa dựng). **(r11) ĐÃ DỰNG VÀ ĐO:** bản Đ0 chỉ bắt `OSError` rồi kiểm dữ liệu nhận MỘT dạng hỏng (nội dung
       rỗng) ⇒ `t156` `B2-nhanh-cu p3 parse error escaped (IndexError …)`, ba Python (bảng 13) — `p3` giết nó. Một
       biến thể không chứng minh mọi cách kiểm dữ liệu đều bị bắt (giới hạn chung của (E)).
    9. (r7) errno thứ tư và lớp con cụ thể ở cột Đ0 và K0: cùng phân hạng như mục 3 và 5 (r14: ở Đ0, `TimeoutError`
       riêng ⇒ chốt tĩnh ĐỎ — lượt 13 và r14; ở khối kill, `e.errno == 12` ⇒ `True` ĐẠT chốt tĩnh và QUA bốn ca — lượt
       13 ở K0, r14 ở khối dùng chung cho K và K0 của ứng viên tham chiếu).
    10. (r7; r8 sửa) Trục N, `:1020` và `:1039`: không đầu vào của hai ca đi qua, nhưng đo được bằng seam
       `Path.iterdir("/proc")` — mã luôn 125 ở hai nơi ấy (xem trục N).
    11. (r7) Hướng thay thế: không có loại ghi nhận theo thiết kế (xem "Hướng" ở trên). Đo trên rig r7: cả 19 biến
       thể thay thế làm ca đỏ bằng `RuntimeError` vô can ở A1, W1 và W0 (bảng 9 dòng 6) — tức không lọt nghiệm thu;
       phân hạng "giết thật" cho hướng này: bất khả thi theo thiết kế, không phải thiếu đo.

    **Bộ tương đương và đầu vào không có đột biến độc chiếm (yêu cầu (b) của r6).** Trên rig r6 (bảng 8) cho mỗi
    đột biến chạy TỪNG nhãn riêng lẻ và ghi tiểu nhãn chết đầu tiên: 49 đột biến cho 37 chữ ký khác nhau; 11 bộ
    tương đương theo tiểu nhãn gồm 23 đột biến — (d1, l3), (d2, l14), (g2, l11), (h1, l9), (i, l15, l21),
    (k3, l23), (k4, l24), (l4, l5), (l12, l13), (l17, l18), (l19, l20). (Nói rõ ở r7, theo cross-review lượt 6: bộ
    số 37 / 11 / 23 chỉ tái lập được với cách cài (g1) của rig r6, tức đổi CẢ nhóm phân tích sang `False` — chạm thêm
    ô R3-Đ của (i); với (g1) chỉ đổi mệnh đề `OSError`, đúng ánh xạ "R2-Đ EACCES sai", reviewer đo ra 36 chữ ký, 12
    bộ / 25 đột biến, bộ thêm là (g1, l10).) Hai đột biến cùng bộ luôn là hai HƯỚNG
    của cùng một thành viên (thoát và sai, hoặc bắt và bọc), cùng chết ở một tiểu nhãn nhưng ở hai loại
    assertion khác nhau (đã đối chiếu thông điệp A1/W1 của từng bộ trên rig, 16:46Z–16:48Z 29-09): tiểu nhãn không
    tách được chúng, LOẠI assertion tách được, nên log phải ghi loại (xem trên) và A1/W1 phải cùng loại với dòng.
    **Đơn vị không có dòng B5 nào lấy làm đích** (đếm trên 36 đơn vị của bảng tiểu nhãn r6; đơn vị r7 thêm, nếu có,
    ghi ở mô tả nhãn của chúng): `B2-dem-doc`
    tiểu nhãn `2` (`stat` EIO + đọc thật; mọi cách tự nhiên đọc hai lần đều chết ở `1` hoặc `3` trước),
    `B3-song` (đối chứng dương, không seam) và `B3-da-wait` (PID đã `wait`, không seam). Đo trên rig r6 khi chạy
    riêng từng nhãn: `B2-dem-doc 2` vẫn bị (d1) và (l3) làm chết (assertion EIO của nó hoạt động, nhưng đó là
    đầu vào của ô R2-H); `B3-da-wait` KHÔNG bị đột biến nào làm chết đúng lý do — (l22) chỉ làm nó chết VÔ CAN
    (A2 của (l22): khi nới `B2-pid-du-phong`, ESRCH THẬT thoát ở `B3-da-wait`, nơi không có observer, nên là
    `ProcessLookupError` vô can chứ không phải `TinHieuChotCa`; đo lại ở cross-review lượt 6); `B3-song` cũng
    KHÔNG đột biến nào của B5 làm chết. Răng RIÊNG của ba đơn vị này — một đột
    biến lấy đúng chúng làm đích — chưa được đo: **CHƯA ĐO** ở packet này (r11 sửa nhãn "KHÔNG ĐO ĐƯỢC" của r6–r10:
    dựng được, chưa dựng); chúng vẫn được khoá bằng
    assertion và bằng phép D (control bỏ đơn vị ấy đỏ), và đột biến giết chúng nếu có nằm trong 174 mục cũ, không
    đo ở đây. r5 còn hai đơn vị nữa trong tình trạng ấy (`B2-parse p2`, và payload thứ hai của `p3` dùng chung
    tiểu nhãn `p3`); r6 cho `p2` một dòng đích (l16) và giữ payload thứ hai của `p3` chung tiểu nhãn với payload
    đầu, không tách. **(r7)** Trên rig r7 (helper r7, 55 đơn vị; (g1) chỉ đổi mệnh đề `OSError`; bảng 9 dòng 8):
    54 dòng cho **40** chữ ký, **13** bộ / **27** đột biến — (c, l1), (d1, l3), (d2, l14), (g1, l10), (g2, l11),
    (h1, l9), (i, l15, l21), (j2, k1), (l12, l13), (l17, l18), (l19, l20), (l2, m4), (l4, l5). So với các bộ của r6:
    (k3, l23) và (k4, l24) tách ra, vì (l23), (l24) sửa khối kill dùng chung nên chết thêm ở `vang-eperm`,
    `vang-eio` còn (k3), (k4) thì không; ba bộ mới (c, l1), (j2, k1), (l2, m4) do quy ước đếm r7 (cùng tiểu nhãn,
    khác loại assertion). Reviewer lượt 6 đo trên helper theo HINT cũng ra 40 / 13 / 27 nhưng với các bộ KHÁC —
    (k3, l23), (k4, l24) thay cho (c, l1), (j2, k1): tổng trùng không chứng minh thành phần trùng. Đơn vị không có
    dòng B5 nào giết bằng `TinHieuChotCa` khi chạy riêng nhãn, trên 55 đơn vị của r7: **9** — `B2-nhanh-cu` `EIO`,
    `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `exception`, cùng `B3-song` và `B3-da-wait` (vẫn chỉ (l22) chết vô can ở
    đó); `B2-dem-doc 2` nay bị (d1) và (l3) giết. Bảy đơn vị của `B2-nhanh-cu` có biến thể E giết đúng lý do (đo
    một lần); `B3-song` và `B3-da-wait` không có biến thể E nào lấy làm đích — răng riêng: CHƯA ĐO (r11 sửa nhãn). Số bộ là
    số ĐO trên một cách cài, không suy từ văn bản (xem đính chính sau bảng 8 về (g1)). **(r8)** Hai đơn vị mới
    (`B2-nhanh-cu utf8-hong-that`, `B2-dem-doc 4`) không có dòng B5 nào lấy làm đích — suy từ B5, không đo lại chữ ký
    ở r8 — nên danh sách trên thành **11** trên 57 đơn vị; cả hai có biến thể E giết đúng lý do (bảng 10 dòng 4; với
    kỳ vọng r9: `d0_giai_ma_lai_utf8`, `d_giai_ma_lai_utf8`, bảng 11).

    **Bảng tiểu nhãn — danh sách ĐỘC LẬP các đơn vị assertion, thứ tự cố định** (nguồn của phép quan sát D
    ở B5; viết ở đây, không suy từ cấu hình của helper). Nhãn không liệt kê ở đây (`B1`, `B2-eacces`,
    `B2-eio`, `B2-eperm-hoi`, `B2-dem-lan`, `B3-song`, `B3-da-wait`, `B3-zombie` trong `t156_...`; `B3b-giet-cay`
    trong `t157_...`) không có tiểu nhãn, mỗi nhãn là một đơn vị:

    | nhãn | tiểu nhãn theo thứ tự | số đơn vị |
    |---|---|---|
    | `B2-doc-hong` | `EACCES`, `EIO`, `ESRCH`, `EPERM` | 4 |
    | `B2-tin-hieu` | `hoi`, `doc`, `kill` | 3 |
    | `B2-exception` | `hoi`, `doc`, `kill` | 3 |
    | `B2-thoat-parse` | `hoi-index`, `hoi-value`, `hoi-decode`, `kill-index`, `kill-value`, `kill-decode` | 6 |
    | `B2-parse` | `p1`, `p2`, `p3`, `p4` | 4 |
    | `B2-dem-doc` | `1`, `2`, `3`, `4` (r8) | 4 |
    | `B2-pid-du-phong` | `song`, `da-wait`, `eperm`, `eio` | 4 |
    | `B2-nhanh-cu` (r7) | `song`, `EACCES`, `EIO`, `ESRCH`, `EPERM`, `p1`, `p3`, `p4`, `utf8-hong-that` (r8), `tin-hieu`, `exception`, `vang`, `vang-da-wait`, `vang-eperm`, `vang-eio`, `vang-tin-hieu`, `vang-exception`, `vang-index`, `vang-value`, `vang-decode` | 20 |

    Tổng: 16 nhãn của `t156_...` + 1 của `t157_...` = 17 nhãn; tám nhãn có tiểu nhãn gồm **48** đơn vị (r8; r7: 46); các
    nhãn còn lại (tám trong `t156_...`, một trong `t157_...`) mỗi nhãn một đơn vị ⇒ 48 + 9 = **57 đơn vị** (r7: 46 + 9 = 55)
    (HINT lượt 6: 17 nhãn, 32 + 9 = 41; r6: 16 nhãn, 27 + 9 = 36). Đo trên rig r7 (bảng 9 dòng 4): 17 nhãn, 46 tiểu
    nhãn, 55 đơn vị.
    Đo trên rig cross-review lượt 7 với hai đầu vào r8 (ba Python): t156 56 đơn vị + t157 1 = 57; D 65/65 control,
    6/6 phép đảo; 54 dòng vẫn 55/55 cặp. Đo lại trên rig riêng của phiên soạn r8 (ba Python, bảng 10 dòng 2 và 3): cùng
    các số ấy.

    Bốn điều r3–r5 đã đo là sai nếu làm tắt, điều thứ năm r6 thêm, thứ sáu r7 thêm, thứ bảy r8 thêm, thứ tám r9 thêm: (1) EACCES ở tầng đọc **không đại
    diện** cho họ `OSError` — một bản chỉ bắt `PermissionError` ở tầng đọc qua cả hai ca r3 (bảng 5); (2) ESRCH ở
    tầng hỏi **không thay** ESRCH ở tầng đọc, kỳ vọng ngược nhau; (3) sentinel `RuntimeError` **không thay**
    sentinel `KeyboardInterrupt` ở tầng đọc; (4) `True` trên PID sống **không chứng minh** đã hỏi PID (bảng 6):
    phải có PID đã `wait` (kết quả `False`), có quan sát đúng lời gọi `kill(pid, 0)`, và có kết quả EPERM/EIO của
    chính lời gọi ấy; (5) **một sentinel của nhóm này không đại diện cho nhóm khác và một tầng không đại diện
    cho tầng khác** — `RuntimeError` ở tầng hỏi không thay `IndexError`/`ValueError`/`UnicodeDecodeError` ở tầng
    hỏi (bản HINT lượt 5 qua hai ca r5 và phép D mà vẫn nuốt `IndexError`), và mọi sentinel ở tầng hỏi hay đọc
    không thay cho tầng kill; (6, r7) **đường mới không đại diện cho nhánh cũ, khối kill dùng chung không đại diện
    cho khối kill tách riêng, và phép đếm ở vài nhãn không đại diện cho phép đếm trên mọi đường** — một helper dựng
    đúng theo HINT lượt 6 để lọt 34 biến thể trái Q-A (bảng 9 dòng 7); (7, r8; r9 sửa tiền đề) **một seam thay CẢ lời
    gọi không đại diện cho lời gọi thật** — kết quả của nó không phụ thuộc cách giải mã của lời gọi, nên cách giải mã
    phải khoá bằng đầu vào nội dung THẬT và bằng `read args` (seam vẫn NHẬN đủ đối số: lượt 8 đo; câu r8 "không thấy
    đối số" sai); (8, r9) **đúng đối số không đại diện cho đúng hành vi** — `read args` bắt mọi dạng đọc lệch, nhưng
    giải mã lại sau khi đọc thì chỉ đầu vào nội dung thật bắt (bảng 11). Đây là chốt của hợp đồng Q-A, không phải lời
    khai rằng kernel thật đã sinh các lỗi ấy. Handoff phải ghi từng đầu vào và nhãn giết (kèm tiểu nhãn và loại
    assertion).
- **B3 (mục 2) — đối chứng dương, và zombie chưa `wait`.** Không seam: `_con_song(os.getpid())` ⇒
  `True` (nhãn `B3-song`); `_con_song` trên PID con đã `wait` ⇒ `False` (nhãn `B3-da-wait`). Rồi một
  con thật, session riêng, SIGTERM thật,
  đọc `/proc/<pid>/stat` bằng phép đọc **độc lập với launcher** cho tới khi thấy `Z`, **chưa `wait`**;
  đặt seam EACCES chỉ ở `Path.stat` của PID ấy (để `read_text` thật vẫn đọc được): `_con_song` và
  `_con_song_dung_khoa` đều phải `False`. Nhãn `B3-zombie`. **(r7; r9 thêm đuôi)** Con đặt `comm` = `x) R (y` cộng
  hai byte `e1 ba` (UTF-8 hỏng ở đuôi) bằng `prctl(PR_SET_NAME)` TRƯỚC khi nhận SIGTERM, và ca xác nhận bằng phép đọc
  BYTES độc lập rằng `(x) R (y` + `e1 ba` + `)` có trong `/proc/<pid>/stat` (không có ⇒ ném lỗi thường, không dùng
  `bang`): nội dung khi ấy là `<pid> (x) R (y…) Z …`, chỉ phép tách theo dấu `)` CUỐI mới đọc ra `Z` (Q-A.4 "đọc được
  và trạng thái là `Z` ⇒ `False`"), và (r9) chỉ phép đọc theo Q-A.7 mới đọc được nó trên đường MỚI: một phép đọc
  giải mã UTF-8 chặt rơi về `kill`, mà `kill(zombie, 0)` thành công ⇒ `result True` (lượt 8 đo M5 chết ở đây khi chạy
  riêng nhãn, ba Python; trên helper r9 A1 của M5 dừng sớm hơn ở `B2-eacces read args`, và biến thể đúng đối số
  `d_giai_ma_lai_utf8` chết ở đây với W1 `B3-zombie result True` — bảng 11). Hai lời gọi
  đường mới đếm (hỏi, đọc) cộng dồn (1, 1), (2, 2). **(r7) Lời gọi thứ ba, đường CŨ**, trên cùng zombie ấy, sau khi
  gỡ seam EACCES: seam chỉ ĐẾM (`stat` và `read_text` thật) và observer `os.kill(pid, 0)` chuyển tiếp thật —
  `exists()` đúng nên đi nhánh tệp có (Đ0): `_con_song` phải `False`, hỏi 1, đọc 1, kill 0. Lời gọi này là đầu
  vào của ô R0-Đ0 (`Z` đọc được) và S-Đ0 (bảng không gian mở rộng); cùng nhãn `B3-zombie`, không tiểu nhãn, xếp
  SAU các assertion của hai lời gọi đường mới.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung trên đường lỗi mới, rơi thẳng về `kill(pid, 0)` ⇒ `True`; hoặc
  đường mới tách theo dấu `)` ĐẦU TIÊN ⇒ đọc ra `R`, trả `True` (dòng (m5); đo ở cross-review lượt 6: qua hết
  hai ca r6, D và toàn suite vì mọi `comm` thật trong r6 không có `)`); hoặc (r7, biến thể E) nhánh cũ tách theo
  dấu `)` đầu tiên (`d0_tach_ngoac_dau`) hay bỏ trạng thái khi đọc được (`d0_ok_Z_sai`) — hai biến thể này lọt
  helper dựng theo HINT (bảng 9 dòng 7) vì ở đó `B3-zombie` chỉ gọi đường mới.
  B3 cũ của r1 (chỉ PID đã `wait`) giữ làm đối chứng nhưng KHÔNG đủ: nó xanh với bản HẸP r1.
- **B4 (mục 2) — nền.** Ngoài Linux (`LA_WINDOWS`, Darwin) sáu ca mới (hai ca helper, bốn ca B8) **trả chuỗi lý
  do** (BỎ QUA có khai theo quy ước sẵn của tệp), không trả QUA: nhánh `/proc` không tồn tại ở đó.
  **Hệ quả lên sàn đột biến Windows (r7, cross-review lượt 6).** Mỗi dòng B5 nhắm hai ca này thành hạng
  `KHONG DO DUOC` của runner trên Windows mà vẫn nằm trong mẫu của `_dot_bien_du_san` (`TY_LE_DOT_BIEN_TOI_THIEU_PHAN_MUOI = 7`: ít
  nhất 70 % mục phải đo được, không thì `--dot-bien` in `DUOI SAN` và rc=1 — chính bước `Tu dot bien` của
  `launcher-windows.yml` mà land_obligation đọc). Ước lượng TĨNH (cận dưới: ca trả chuỗi ở đầu thân dưới
  `if LA_WINDOWS` / `os.name == 'nt'` / `platform.system() != 'Linux'`, cộng mục mang giới hạn `('posix', …)`):
  nền 11/177 mục không đo được; sau r6 60/226 (73,45 %, trần 67 ⇒ biên 7); với lớp (m) 65/231 (71,86 %, trần 69
  ⇒ biên 4). Mỗi dòng Linux-only thêm về sau ăn khoảng 0,7 mục biên. Executor khai phép tính này (lệnh + số)
  trong handoff; số THẬT trên Windows: KHÔNG ĐO ĐƯỢC (lý do 2) trước merge (Q4) — đọc dòng `DOT BIEN: …` của job Windows
  ở lượt push master và coi `DUOI SAN` là đỏ của packet.
  **Đo lại ở r7 và biên còn lại** (tập lệnh ước lượng của reviewer lượt 6 chạy trên tệp test đã lắp của rig r7,
  01:41:30Z 30-09; bảng 9 dòng 10). Mẫu của sàn là `len(DOT_BIEN) + len(DOT_BIEN_HARNESS)` (runner nền,
  `launcher_test.py:8294` trên `423b4ba`, `:8293` trên `89fc4fa`), và dưới sàn thì `--dot-bien` in `!! DUOI SAN`
  rồi trả 1 (`:8298–8303`; `89fc4fa`: `:8297–8302`). Sau r7 (54 dòng
  mới, như HINT): **65/231 không đo được trên Windows, 71,86 % đo được, trần 69 ⇒ biên 4 mục** — cận dưới tĩnh: ca
  bỏ qua giữa thân không đếm được, nên biên THẬT có thể nhỏ hơn. Thêm n dòng Linux-only nữa: n = 1, 2, 3, 4, 5, 6 ⇒
  biên 3, 2, 2, 1, 0, 0 (vẫn đạt); **n = 7 ⇒ `DUOI SAN`** (69,75 %). Đây là giới hạn CỨNG, đo được, của cách làm
  "thêm một mục đột biến cho mỗi ô": 78 hạng mục của bảng không gian mở rộng không có dòng B5 riêng, và đưa chúng
  vào `DOT_BIEN` sẽ làm Windows rơi xuống dưới sàn ngay (231 + 78 = 309 mục, 65 + 78 = 143 không đo được, còn
  166/309 = 53,72 % đo được — suy bằng số học từ cùng phép đếm, không dựng và không chạy). Vì vậy r7 đến r10 giữ
  `DOT_BIEN` ở 54 dòng và đo các hạng mục còn lại bằng phép (E) trong tập lệnh bằng chứng cục bộ (B5); r9, r10 đặt
  các biến thể lớp 124 (M1–M5, M12; r10 thêm `g_to_hop_dinh_dang_khoa` — B8) ở (E) cùng lý do, nên biên vẫn 4.
  **Giới hạn CỨNG ở trên chỉ đúng cho dòng mà MỌI ca đích đều BỎ QUA trên Windows** (r10, cross-review lượt 9, lớp
  `rang-ben-b8-bo-sot-phuong-an`): runner đếm một dòng là đo được khi còn ít nhất một ca đích chạy (`can_do =
  len(phai_chet) - len(bo_qua)`, `launcher_test.py:8034` trên `423b4ba`), nên một dòng có thêm ĐÍCH ĐA NỀN — một ca
  TĨNH chạy mọi nền, ví dụ AST kiểm năm lời đọc `/proc/<pid>/stat` đúng `DANG_DOC_QA7` — không ăn biên. Đo (lượt 9,
  runner `chay_dot_bien()` thật, 3.12.3, sáu dòng M1–M5, M12 cộng một ca tĩnh làm đích phụ): Linux M1 `giet 4/4`, M2,
  M3, M4 `3/3`, M5 `1/1` (rig không có `t156`), M12 `5/5`; Windows giả lập (`platform.system`) cả sáu `giet 1/1` qua
  ca tĩnh ⇒ 237 mục, 65 không đo được, 72,57 %, **biên 6**; không có ca tĩnh ⇒ năm dòng `KHONG DO DUOC`. Trên Windows
  dòng ấy chỉ đo DẠNG đọc; hành vi vẫn đo lại ở Linux mỗi lượt. Biến thể thứ bảy `g_to_hop_dinh_dang_khoa` sai ĐỊNH
  DẠNG KHOÁ, không sai dạng đọc, nên ca tĩnh ấy không bắt được nó: đưa nó vào `DOT_BIEN` là thêm một dòng Linux-only
  (có ca tĩnh: 238 / 66 ⇒ 72,27 %, biên 5; không có ca tĩnh: 238 / 72 ⇒ 69,75 %, `DUOI SAN` — tính bằng chính
  `_dot_bien_du_san` của `423b4ba`, bảng 12). Đổi cân bằng này — thêm dòng `DOT_BIEN`, thêm ca tĩnh, hay cho các ca
  chạy nhánh `/proc` trên Windows bằng seam — là quyết định của điều phối/chủ kho, r7 đến r10 không tự chọn (§11.3).

**Ca `t157_...`**

- **B3b (mục 2) — chốt tiêu thụ `_giet_cay`.** Con thật CÒN SỐNG, session riêng, `khoa` lấy trước seam;
  seam EACCES ở `Path.stat` của PID ấy; gọi `_giet_cay(pid, khoa)` để SIGTERM thật biến con thành
  zombie chưa `wait`; kết quả phải có `tron_ven=True` (phía deadline ánh xạ 124, `launcher.py:1669`).
  Nhãn `B3b-giet-cay`. Dọn PID con và `wait` trong `finally`. Ca này riêng để đột biến (c) ở B5 làm
  **cả hai** ca `t156_...` lẫn `t157_...` đỏ, mỗi ca bằng `TinHieuChotCa` của chính nó.
  **ĐỎ khi:** đột biến bỏ phép đọc nội dung ⇒ `tron_ven=False` ⇒ tương ứng 125 (bảng 2, hàng HẸP r1).
  **Phạm vi của chốt (r8; r9 sửa).** B3b chỉ phủ lỗi của PHÉP HỎI. Lỗi của phép ĐỌC khoá danh tính, quét nhóm và
  ảnh chụp khi `comm` không giải mã được (124 / 0 / 10 cho tiến trình còn sống, §2) do B8 khoá (r9).

**B8 (r9, lớp `sua-124-trong-packet`, quyết định chủ kho 30-09) — bốn ca khoá `t158_...` đến `t161_...`: `comm`
không giải mã được KHÔNG được làm 124 (hay `stop` rc=0) nói dối.** Bất biến: "124 ⇔ cả cây ĐÃ CHẾT" và "`stop`
rc=0 ⇔ cây đã sạch" không phụ thuộc cách giải mã `comm`. Kích hoạt THẬT: kernel cắt `comm` ở 15 byte nên tên tiếng
Việt thành UTF-8 hỏng; locale không phải UTF-8 làm cả `comm` UTF-8 hợp lệ nổ (§2). **Bốn ca đăng ký riêng, KHÔNG dùng
helper** (r9 chọn; HINT lượt 8 khuyến nghị bốn nhãn của `t157_...`): dạng bốn ca là dạng đã ĐO (lượt 8, bảng 11), dạng
nhãn chỉ có số học (21 nhãn / 61 đơn vị / 69 control); bốn ca riêng giữ helper, A/W và D của `t156_...`, `t157_...`
đúng như r8 (17 nhãn / 48 tiểu nhãn / 57 đơn vị / 65 control).
  · `t158` `B8-sau-sinh` — `run --deadline-utc` (hạn 3 s) trên con đổi `comm` thành 15 byte hỏng 0,5 s SAU lúc sinh
    (launcher đã lấy khoá với `comm` bình thường); con ghi nhịp 0,1 s/lần ra tệp.
  · `t159` `B8-luc-sinh` — như trên, nhưng chương trình là symlink tên `kiểm_tra_tiến_trình` trỏ tới Python: `comm`
    hỏng NGAY lúc exec, không `prctl`.
  · `t160` `B8-setsid` — khoá của mẹ lấy bằng phép đọc BYTES độc lập theo định dạng nền (`_k124_khoa_that`, r10), rồi
    `_giet_cay` gọi trực tiếp: mẹ (session riêng) sinh cháu `setsid`; cháu phớt lờ SIGTERM, đổi `comm`.
  · `t161` `B8-me-thoat` — lấy khoá của mẹ (cùng cách, r10), mẹ thoát, rồi `_giet_cay`; cháu CÙNG NHÓM đổi `comm`, còn
    sống.
Điều kiện dựng (không đạt ⇒ lỗi thường, KHÔNG `bang`): `comm` của con/cháu đọc bằng BYTES đúng 15 byte ấy (cháu:
`_K124_COMM_CHAU`, r11); ở `t158`
khoá trong sổ khác `None`; tên tiếng Việt tạo được; ở `t160`, `t161` observer ghi được ít nhất một lời đọc. Assertion
theo thứ tự; thông điệp mở đầu bằng tên đầu vào rồi LOẠI: (1) `124 noi doi` — không được có 124 (hay `tron_ven=True`)
cùng một tiến trình còn sống hoặc nhịp còn tăng sau 1 s; (2) `qua han khong giet duoc` (`t158`, `t159`) hay `khong
giet duoc` (`t160`, `t161`) — quá hạn phải GIẾT THẬT; (3) chỉ ở `t160`, `t161`: `read args` — observer ghi (phương
thức, args, kwargs) MỌI lời đọc `Path` trên `/proc/<số>/stat` trong cửa sổ quanh `_giet_cay`, mọi bản ghi phải BẰNG
`DANG_DOC_QA7`, và (r11) KHÔNG sự kiện audit `open` nào trên `/proc/…`, trên đường tương đối hay trên fd số được xảy
ra NGOÀI một lời đọc đã ghi — lời đọc `Path` đã khai trên đúng `/proc/<số>/stat` là đường mở tệp DUY NHẤT được phép
(Q-A.7 (ii); kiểm ở ba hàm ngoài VÀ khối đọc nhánh tệp có của `_con_song`, vì `_con_lai` gọi nó trong cửa sổ). Thông
điệp: `read args ['open ngoai loi doc Path: <n> su kien, vd […]']`. HINT lượt 10 đếm "số `open` BẰNG số lời đọc" trên
đúng đường `/proc/<số>/stat`; r11 đổi sang "không `open` nào ngoài" vì hai phép đo (bảng 13): bộ lọc đường của HINT
không thấy `/proc/<pid>/task/<pid>/stat` (`TASK_khoa` QUA ở `t160`, `t161` với khối HINT, 3.12), và bỏ qua fd số,
tức ống của tiến trình con (`CAT_khoa`, cùng kết quả). Đường tuyệt đối KHÔNG bắt đầu bằng `/proc/` không tính, PHÒNG XA chứ không phải lỗi đã gặp: máy
nạp module mở `.pyc` một cách lười ngay trong cửa sổ (đo: log của `TASK_khoa` ghi `…/encodings/__pycache__/latin_1…pyc`),
nên một lần nạp lười ngoài lời đọc đã ghi ở một ứng viên đúng sẽ thành đỏ oan. Với bốn ứng viên nháp điều đó KHÔNG xảy
ra (đo: bản nháp tính mọi đường cho `cand_a`, `cand_b` QUA ở `t160`, `t161`, ba Python, kể cả khi `_k124_khoa_that`
không giải mã ascii — `read_text(encoding=…)` tra codec BÊN TRONG lời đọc đã ghi, còn `bytes.decode("ascii")` đi đường
tắt của CPython, không nạp module). Giá phải khai: đường tuyệt đối tới cùng nội dung mà không bắt đầu bằng `/proc/`
(`//proc/<pid>/stat` — POSIX giữ hai dấu `/` đầu; `/dev/fd/<n>`) thước đo này không thấy — đo: `SL2_khoa` QUA ở `t160`,
`t161` — và chốt tĩnh bắt (ba hàm ngoài), seam đếm đọc bắt (`_con_song`). Cùng giá (r12, đo lượt 11, 3.12): ống
`os.pipe` đọc bằng `os.read`, và tệp tạm do tiến trình con ghi, không sinh sự kiện `open` nào được tính — `PIPE_khoa`,
`TMPF_khoa` QUA cả bốn ca B8; chốt tĩnh r12 ĐỎ cả hai, luật `H` (bảng 14). Docstring `_k124_audit` của khối r11 nói "ống
của tiến trình con đều là `open` NGOÀI" — rộng hơn phép đo: chỉ đúng cho ống PIPE mà `subprocess` bọc bằng `io.open`
(`CAT_khoa`). r12 sửa docstring ấy NGAY TRONG khối (khối dưới), không đổi mã. `t158`, `t159` chạy
launcher ở tiến trình con nên không có observer. Phép kiểm sống đọc BYTES riêng (và `_con_song_that` phải đọc bytes —
§6 mục 3). **Khung ca tự canh điều kiện đo của chính nó (r10, cross-review lượt 9, lớp `b8-khung-ca-thieu-chot`):**
(a) con của `t158`, `t159` tự ghi PID vào `<tệp nhịp>.pid` trước mọi việc khác; `finally` chờ tệp ấy tối đa 2 s rồi
dọn bằng PID ấy, chỉ khi `/proc/<pid>/cmdline` mang đường tệp nhịp của ca — KHÔNG dọn theo PID do launcher-đang-thử
báo; (b) HẠN SỐNG: con ghi tối đa 1200 nhịp (khoảng 120 s) rồi tự thoát, mẹ và cháu của `t160`, `t161` là
`time.sleep(120)` — dọn hỏng thì tiến trình vẫn tự chết; **và (r11, cross-review lượt 10) chết vì HẾT HẠN không phải
bị giết, ca phải ĐỎ đúng loại.** Con và cháu ghi dấu `<tệp>.tu_thoat` ở `finally` — `han_song` khi hết hạn,
`ngoai_le` khi chết vì ngoại lệ; tín hiệu mặc định giết tiến trình KHÔNG chạy `finally`, và ca không phải cha của con
(`t158`, `t159`: cha là launcher, launcher `wait` nó) hay của cháu nên không đọc được mã thoát. Mẹ của `t160` là con
TRỰC TIẾP của ca, nên đọc bằng MÃ THOÁT: `poll()` âm ⇔ tín hiệu giết, `None` ⇔ còn sống, ≥ 0 ⇔ tự thoát. Dấu
`han_song` hay mẹ có mã ≥ 0 ⇒ assertion (2) ĐỎ (`qua han khong giet duoc` / `khong giet duoc`; thông điệp ghi `tu
thoat=han_song` hay `me rc=0`); dấu `ngoai_le` ⇒ lỗi thường (điều kiện dựng: con/cháu chết vô can không được thành
tín dụng); assertion (1) của `t160` tính cả mẹ còn sống (lời (1) nói "một tiến trình còn sống", mã r10 chỉ hỏi cháu).
r11 BỎ hai chốt thời gian của HINT lượt 10 (`n2 >= 1200` và `_giet_cay` quá 60 s ⇒ lỗi thường): lỗi thường không phải
ĐỎ đúng loại; thời gian là đại lượng thay thế, không phải phép đo "có bị giết không"; và chốt 60 s đứng TRƯỚC
assertion nên biến chính các ca "không giết" thành lỗi thường (đo: `MEHAN`, `KILLNEVER` trên khối HINT ⇒ `dieu kien
dung: _giet_cay qua 60 s`; cùng hai bản trên khối r11 ⇒ `TinHieuChotCa` `khong giet duoc` — bảng 13). Lý do đo được (VERDICT lượt 10): launcher nói dối (nền, M12) cộng chờ
con KHÔNG hạn sau `_giet_cay` (`p.wait()` thay `p.wait(timeout=5)`) làm `t158` QUA sau 122 s với khối r10 — ca duy
nhất giết M12 đơn lẻ; `_giet_cay` chờ mãi không SIGKILL làm `t160`, `t161` QUA sau 120 s. **Đường vào r11 tự liệt kê
trước khi vá** — mỗi đường một chốt và một đột biến RIG chứng răng (không phải biến thể (E): như WAITK/KILLNEVER của
lượt 10, chúng sửa khung chạy của launcher chứ không phải một vị trí Q-A); số đo ở bảng 13:

| đường "không bị giết mà trông như đã chết/đã sạch" | ca | chốt (r11) | đột biến rig |
|---|---|---|---|
| con tự thoát ở 1200 nhịp | `t158`, `t159` | dấu `han_song` ⇒ (2) | `nen_WAITK`, `M12_WAITK` (chờ con không hạn) |
| cháu tự thoát ở `time.sleep(120)` | `t160`, `t161` | dấu `han_song` ⇒ (2) | `KILLNEVER` (vòng chờ SIGTERM không bao giờ SIGKILL) |
| mẹ tự thoát ở `time.sleep(120)` | `t160` | mã thoát ≥ 0 ⇒ (2) | `MEHAN` (bỏ sót gốc, chờ 125 s sau SIGKILL cháu) |
| mẹ còn sống khi `_giet_cay` báo `tron_ven` | `t160` | `poll()` là `None` ⇒ (1) | `MEBO` (bỏ sót gốc khi ảnh có hậu duệ) |
| con/cháu chết vì ngoại lệ (không bị giết, chưa hết hạn) | cả bốn | dấu `ngoai_le` ⇒ lỗi thường | probe (bảng 13): tệp `comm` không ghi được ⇒ `ngoai_le` ⇒ `RuntimeError` |
| mẹ của `t161` thoát | `t161` | không phải đường: mẹ thoát CÓ CHỦ Ý và được `wait` trước `_giet_cay` | — |

(c) `_k124_run` đòi sổ JSON có `pid` và rc là một kết cục hạn
chót của `run` (124, 125 hay 10; `launcher.py:1669`, `:1684`), khác thì lỗi thường — launcher CHẾT vô can (`rc=1`) không
được thành `TinHieuChotCa` `qua han khong giet duoc`; (d) `t158`, `t159` trả chuỗi BỎ QUA có khai khi
`locale.getpreferredencoding(False)` giải mã được 15 byte hỏng: ở đó lỗi 124 không tái hiện được, và ca biết mình không
đo gì. `t160`, `t161` KHÔNG BỎ QUA theo locale: `read args` và chốt định dạng khoá của chúng không phụ thuộc locale nên
vẫn đo được, chỉ assertion (1), (2) mất nghĩa ở đó (bảng 12; r11 đo lại ở bốn locale giải mã được: bảng 13). Hai đầu vào nội dung thật của `t156` thì ném lỗi thường ở
locale ấy (điều kiện dựng, quy ước chung) — hai đơn vị trong 57, BỎ QUA sẽ tắt cả ca; (e) `_k124_me_chau` giết mẹ và
cháu trước khi ném lỗi điều kiện dựng, và `t161` dọn cả mẹ. Lý do đo được (VERDICT lượt 9, sha256 `0f1b3bdc…ddfa`,
khối r9): launcher chết `rc=1` ⇒ `t159` ra `TinHieuChotCa` đúng ca, đúng LOẠI (tín dụng giả) và hai con sống vô hạn;
`prctl` vô hiệu ⇒ bốn tiến trình sót; locale ISO-8859-1 ⇒ `t158` QUA trên launcher NỀN. Đo trên khối r10: bảng 12; trên
khối r11: bảng 13.
Đo (khối r9: bảng 11; khối r10: bảng 12; khối r11 ngay dưới: bảng 13 — 3.11.15 / 3.12.3 / 3.13.12, ma trận trùng từng
ô; ứng viên nháp Q-A.7 dạng latin-1 trừ các hàng ghi "bytes"). Mỗi ô đỏ là `TinHieuChotCa` của đúng ca đích, ghi LOẠI;
không ô nào chết vô can. Mười một hàng đầu và ba hàng r10 trùng từng ô giữa khối r10 (bảng 12) và khối r11 (bảng 13);
các hàng r11 là số của khối r11:

| bản | `t158` | `t159` | `t160` | `t161` |
|---|---|---|---|---|
| nền `89fc4fa`; ứng viên nháp theo r8 (y hệt nhau) | `124 noi doi` (rc=124, con sống, nhịp 74→84) | `qua han khong giet duoc` (rc=10, con sống) | `124 noi doi` ("SIGTERM: cay da sach", cháu sống) | `124 noi doi` ("tien trinh da khong con chay", cháu sống) |
| ứng viên nháp Q-A.7 | QUA | QUA | QUA | QUA |
| M1 — `_khoa_danh_tinh` đọc lại bằng `read_text()` không đối số | QUA | `qua han khong giet duoc` | `124 noi doi` | `124 noi doi` |
| M2 — `_thanh_vien_nhom` như thế | QUA | QUA | `read args` | `124 noi doi` |
| M3 — `_chup_cay` như thế | QUA | QUA | `124 noi doi` | `khong giet duoc` |
| M4 — khối đọc nhánh tệp có của `_con_song` như thế | QUA | QUA | `124 noi doi` | `124 noi doi` |
| M5 — khối đọc đường mới của `_con_song` như thế | QUA | QUA | QUA | QUA |
| M12 — M1 cùng M2 (hai vị trí) | `124 noi doi` | `qua han khong giet duoc` | `124 noi doi` | `124 noi doi` |
| `errors="surrogateescape"` ở `_khoa_danh_tinh` / `_thanh_vien_nhom` / `_chup_cay` (ba bản, mỗi bản một chỗ) | QUA | QUA | `read args` | `read args` |
| `g_to_hop_dinh_dang_khoa` (r10; r11: cả hai dạng) — dạng bytes: bỏ giải mã trường số ở `_khoa_danh_tinh` VÀ `_chup_cay` (khoá `linux:b'…'`); dạng latin-1: `!r` ở cả hai chỗ (khoá `linux:'…'`); với khối r9 cả bốn ô QUA | QUA | QUA | `khong giet duoc` (khoá KHÁC) | QUA |
| (r10, đối chiếu tổ hợp; r11: cả hai dạng) chỉ `_khoa_danh_tinh` lệch định dạng | QUA | QUA | `khong giet duoc` (khoá KHÁC) | `124 noi doi` |
| (r10, đối chiếu tổ hợp; r11: cả hai dạng) chỉ `_chup_cay` lệch định dạng | QUA | QUA | `124 noi doi` | `124 noi doi` |
| (r11) `s_khoa_tach_ngoac_dau` — `_khoa_danh_tinh` tách theo `)` ĐẦU (latin-1 `index(")")`; bytes `index(b")")` hay `partition(b") ")`; ba bản); cùng ô: tách cả dòng theo khoảng trắng (rig); với khối r10 cả bốn ô QUA (lượt 10) | QUA | QUA | `124 noi doi` | `124 noi doi` |
| (r11) `s_nhom_tach_ngoac_dau` — như thế ở `_thanh_vien_nhom` (ba bản + khoảng trắng); khối r10: QUA ×4 | QUA | QUA | QUA | `124 noi doi` |
| (r11) `s_chup_tach_ngoac_dau` — như thế ở `_chup_cay` (ba bản + khoảng trắng); khối r10: QUA ×4 | QUA | QUA | `124 noi doi` | `khong giet duoc` |
| (r11) `g_khoa_open` / `g_nhom_open` / `g_chup_open` — lời đọc qua `open()`, `io.open(…, "rb")`, `Path.open()`, giữ cách giải mã (mười bản, mỗi bản một chỗ); cùng ô: `/proc/<pid>/task/…` (`TASK_khoa`), `dir_fd` (`DIRFD_khoa`), tiến trình con (`CAT_khoa`); khối r10: QUA ×4; khối HINT: bảng 13 | QUA | QUA | `read args` (open ngoài lời đọc đã ghi) | `read args` (open ngoài lời đọc đã ghi) |
| (r11) `g_d0_open` — khối đọc nhánh tệp có của `_con_song` qua `open()` (còn chết ở helper: `t156` `B2-nhanh-cu song read count 0`) | QUA | QUA | `read args` (open ngoài lời đọc đã ghi) | `read args` (open ngoài lời đọc đã ghi) |
| (r11) `g_d_open` — khối đọc đường mới qua `open()`: B8 không chạm, như M5; chết ở helper `t156` `B2-eacces read count 0` | QUA | QUA | QUA | QUA |
| (r11, rig) `//proc/<pid>/stat` ở `_khoa_danh_tinh` (`SL2_khoa`) — thước đo `open` không tính đường tuyệt đối ngoài `/proc/`; chốt tĩnh ĐỎ | — | — | QUA | QUA |
| (r11, rig) dạng bytes, so `Z` bằng literal str ở `_thanh_vien_nhom` (`ZB_nhom`) — zombie của chính ca còn trong nhóm | `qua han khong giet duoc` | `qua han khong giet duoc` | `khong giet duoc` | QUA |
| (r11, rig) như thế ở `_chup_cay` (`ZB_chup`) — vô hại cho kết cục: zombie trong ảnh chụp bị `_con_song_dung_khoa` loại; chốt tĩnh ĐỎ | QUA | QUA | QUA | QUA |
| (r11, rig, khung ca) launcher bỏ sót MẸ khi ảnh có hậu duệ (`MEBO`) | QUA | QUA | `124 noi doi` (mẹ sống) | QUA |

M5 không chạm B8 (đường mới chỉ chạy khi `stat` lỗi): nó chết ở `t156_...` `B2-eacces read args` (A1 và W1). M4 chết
thêm ở `t156_...` (`read args`; A1 `B2-dem-lan`, W1 `B2-nhanh-cu song`). Với helper KHÔNG có `read args` (lượt 8) M4
chết ở `B2-nhanh-cu utf8-hong-that result False` và M5 ở `B2-dem-doc 4 kill count 1` và `B3-zombie result True`.
**`t158` KHÔNG bị đột biến ĐƠN nào giết**: `_giet_cay` chỉ kết luận "tien trinh da khong con chay" khi khoá danh tính
VÀ quét nhóm cùng mù, nên ca này khoá một TỔ HỢP; M12 là tổ hợp tối thiểu và chết ở cả bốn ca. M12 là đột biến HAI
vị trí — trái quy tắc "một vị trí" của B5 và (E) — và được MIỄN, có lý do: mỗi vị trí của nó đã có biến thể đơn giết
riêng (M1 ở `t159`; M2 ở `t160` `read args` và `t161`), nên không có câu hỏi "vị trí nào bị giết"; M12 chỉ đo đúng
điều `t158` sinh ra để đo — phản chứng đầu-cuối của sự cố chủ kho quyết sửa.
**Chỗ đặt M1–M5, M12 và `g_to_hop_dinh_dang_khoa` (r11: cùng chỗ cho ba `s_*_tach_ngoac_dau` và năm `g_*_open`):
phép (E)** (B5 (E) mục 1 và 6), KHÔNG vào `DOT_BIEN` — cân bằng
r7–r8 giữ nguyên (B4); răng BỀN của bốn ca B8 vì vậy: KHÔNG CÓ (như các hạng mục (E)). `g_to_hop_dinh_dang_khoa` là tổ
hợp hai vị trí, MIỄN như M12 và cùng lý do: mỗi vị trí đơn lẻ đã có ca giết riêng (hai hàng đối chiếu ở bảng trên). Với
biến thể (E) mà đích là một ca B8, chỉ A1 áp dụng (gọi thẳng hàm ca trên bản sao đột biến; không có helper, không có
nhãn để nới): chết bằng `TinHieuChotCa` của đúng ca, thông điệp mở đầu bằng đúng tên đầu vào, đúng LOẠI như bảng trên.
Đưa các biến thể ấy vào `DOT_BIEN` là câu hỏi §11.3 — ba phương án và giá của từng cái ở B4; chọn phương án nào khác
hiện trạng cũng ⇒ revision mới.
Write set ĐỦ (năm chỗ đọc và mọi nơi gọi ở `launcher.py`; ca, helper, đột biến ở `launcher_test.py`); ba chỗ cùng khuôn
ngoài write set: nợ ở §5.

Mã test đã đo (MÃ TEST THUẦN — executor tự dẫn xuất lại, tự đo; `DANG_DOC_QA7` phải là dạng ứng viên của executor
khai). Nguồn: khối r9 (233 dòng, sha256 `b60434e9…aeeb`) cộng nhóm `khoa-dinh-dang-khong-co-chot` và nhóm
`b8-khung-ca-thieu-chot` của HINT lượt 9 (khối bản gộp HINT: 279 dòng, sha256 `225a10ce…5868`), cộng ba sửa của r10: con
có hạn sống 1200 nhịp, `_k124_don_con` chờ tệp PID, chú thích đầu khối ghi r10 (khối r10: 281 dòng, sha256
`893b31ce…8366`); (r11) cộng nhóm `ma-tran-loi-thieu-chot` và nhóm `b8-khung-ca-thieu-chot` của HINT lượt 10 (khối
bản gộp HINT: 315 dòng, sha256 `b929f2b1…091a` — phiên soạn r11 trích lại từ bản chỉ-HINT, khớp), rồi ba sửa của r11:
thước đo `open` thành danh sách cho phép (mọi `open` trên `/proc/…`, đường tương đối, fd số phải nằm trong một lời đọc
đã ghi), dấu tự thoát của con và cháu thay hai chốt thời gian của HINT, mẹ của `t160` đọc bằng mã thoát — khối r11:
351 dòng, sha256 `950b880a90b014b0646484282858272ae8888a966f331940a5f0831227ca7bad`, `cmp` trùng khối đã chạy ở rig r11
(bảng 13, ba Python). **(r12) Khối dưới: 353 dòng, sha256
`60ee8d5f6087cd7e7862f91bd27690d2d18bfef2f2cb03f06fcad522673d75ff`, 0 dấu chéo ngược** = khối r11 đổi ĐÚNG docstring
của `_k124_audit` (4 → 6 dòng; lớp `chot-tinh-bien-chua-khep`, cross-review lượt 11) và chữ "r11" → "r12" ở dòng chú
thích thứ hai. Không đổi mã, đo: AST của hai khối sau khi bỏ mọi docstring BẰNG nhau ở ba Python; khối r12 trích bằng
máy từ CHÍNH tệp r12, `cmp` trùng khối đã chạy, bốn ca B8 (3.12): nền ĐỎ ×4 đúng loại của bảng B8, `cand_a` QUA ×4
(bảng 14). Mọi số đo khác của khối trong tệp này là số của khối r11 (bảng 13) — vẫn áp dụng vì mã không đổi.

```python
# ---------------------------------------------------------------------------------------------
# B8 — ca khoá lớp `sua-124-trong-packet` (MÃ TEST THUẦN của đặc tả r12; executor tự dẫn xuất lại,
# tự đo). Bất biến: "124 ⇔ cả cây ĐÃ CHẾT" và "stop rc=0 ⇔ cây đã sạch" không phụ thuộc cách giải
# mã `comm`. Kích hoạt THẬT: kernel cắt `comm` ở 15 byte, nên tên tiếng Việt thành UTF-8 hỏng.
# ---------------------------------------------------------------------------------------------
_K124_COMM = bytes.fromhex("6b69e1bb836d5f7472615f7469e1ba")   # 'kiểm_tra_tiến_trình'.encode()[:15]
# Cháu của t160/t161 (r11): comm có `) ` (tên thật kiểu `tep (1).sh`) + đuôi UTF-8 hỏng — phủ trục S ở ba hàm ngoài:
# phép tách theo `)` ĐẦU (index/partition/split) lệch trường ở _khoa_danh_tinh, _thanh_vien_nhom, _chup_cay.
_K124_COMM_CHAU = b"tep (1) " + _K124_COMM[8:]                 # 15 byte: 'tep (1) ra_ti' + e1 ba
_NL = chr(10)

# Dạng đọc /proc/<pid>/stat theo Q-A.7 mà ứng viên KHAI (một chỗ, helper t156/t157 và B8 dùng chung):
# (tên phương thức Path, args, kwargs) — ví dụ ("read_bytes", (), {}) nếu chọn đọc bytes.
DANG_DOC_QA7 = ("read_text", (), {"encoding": "latin-1"})


def _k124_song(pid: int) -> bool:
    """Sống THẬT theo /proc đọc BYTES — không giải mã `comm`; zombie = đã chết."""
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    except (FileNotFoundError, ProcessLookupError):
        return False
    return nd[nd.rindex(b")") + 2:].split()[0] != b"Z"


def _k124_locale_giai_ma_duoc() -> bool:
    """`read_text()` không đối số giải mã theo mã hoá này; giải mã được 15 byte hỏng thì lỗi 124 KHÔNG tái hiện được."""
    import locale
    try:
        _K124_COMM.decode(locale.getpreferredencoding(False))
    except (UnicodeDecodeError, LookupError):
        return False
    return True


def _k124_don_con(tn):
    """Dọn con B8 bằng PID do CHÍNH con ghi (không tin PID launcher-đang-thử báo), chỉ khi cmdline mang đường nhịp."""
    tp = Path(str(tn) + ".pid")
    _k124_cho_tep(tp, 2.0)
    try:
        pid = int(tp.read_text())
        with open(f"/proc/{pid}/cmdline", "rb") as f:
            cua_ta = str(tn).encode() in f.read()
    except (OSError, ValueError):
        return
    if cua_ta:
        with contextlib.suppress(OSError):
            os.kill(pid, signal.SIGKILL)


_K124_MO = {"cai": False, "bat": False, "trong": 0, "ngoai": []}


def _k124_audit(ev, args):
    """Cửa sổ B8: mọi sự kiện audit `open` trên `/proc/…`, trên đường tương đối (`dir_fd`) hay trên fd số phải nằm
    TRONG một lời đọc Path đã ghi — danh sách cho phép ở tầng API (`open()`, `Path.open()`, `os.open`, đường
    `/proc/<pid>/task/…`, và ống PIPE mà `subprocess` bọc bằng `io.open` trên fd số, đều là `open` NGOÀI). Thước đo
    này KHÔNG thấy đường tuyệt đối ngoài `/proc` (`//proc/…`, tệp tạm) hay ống `os.pipe` đọc bằng `os.read` (đo) —
    phần ấy do chốt tĩnh và seam đếm đọc giữ. Đường tuyệt đối ngoài `/proc` không tính vì máy nạp module mở `.pyc`
    của codec một cách lười, ngay trong cửa sổ (đo)."""
    if _K124_MO["bat"] and ev == "open" and not _K124_MO["trong"]:
        p = args[0] if isinstance(args[0], int) else os.fsdecode(args[0])
        if isinstance(p, int) or not p.startswith("/") or p.startswith("/proc/"):
            _K124_MO["ngoai"].append(p)


@contextlib.contextmanager
def _k124_ghi_doc():
    """Ghi (phương thức, args, kwargs) của MỌI lời đọc Path trên /proc/<số>/stat trong cửa sổ, và ghi mọi sự kiện
    audit `open` xảy ra NGOÀI các lời đọc ấy: lời đọc Path đã ghi là đường mở tệp DUY NHẤT được phép."""
    if not _K124_MO["cai"]:
        sys.addaudithook(_k124_audit)          # không gỡ được; ngoài cửa sổ hook không làm gì
        _K124_MO["cai"] = True
    ghi = []
    goc = {t: (t in Path.__dict__, getattr(Path, t)) for t in ("read_text", "read_bytes")}

    def boc(ten, g):
        def f(self, *a, **k):
            p = str(self)
            if not (p.startswith("/proc/") and p.endswith("/stat") and p[6:-5].isdigit()):
                return g(self, *a, **k)
            ghi.append((ten, a, k))
            _K124_MO["trong"] += 1
            try:
                return g(self, *a, **k)
            finally:
                _K124_MO["trong"] -= 1
        return f
    for t, (_co, g) in goc.items():
        setattr(Path, t, boc(t, g))
    _K124_MO.update(bat=True, trong=0, ngoai=[])
    try:
        yield ghi
    finally:
        _K124_MO["bat"] = False
        for t, (co, g) in goc.items():
            if co:
                setattr(Path, t, g)
            else:
                delattr(Path, t)


def _k124_ma_con(tep_comm, tep_nhip, cho: float, doi_comm: bool) -> str:
    """Con: ghi PID của chính nó, (tuỳ chọn) chờ `cho` giây rồi đổi comm thành 15 byte hỏng, ghi comm THẬT
    (bytes) ra tệp, rồi ghi nhịp mỗi 0,1 s — tối đa 1200 nhịp (khoảng 120 s) rồi tự thoát: hạn sống. Mọi lối
    thoát KHÔNG do tín hiệu ghi `<tệp nhịp>.tu_thoat` (`han_song` / `ngoai_le`) — ca không phải cha của con."""
    dong = ["import ctypes, os, time",
            f"open({str(tep_nhip) + '.pid'!r}, 'w').write(str(os.getpid()))",
            "ly_do = 'ngoai_le'",
            "try:",
            f"    time.sleep({cho})"]
    if doi_comm:
        dong.append(f"    ctypes.CDLL(None).prctl(15, bytes.fromhex({_K124_COMM.hex()!r}), 0, 0, 0)")
    dong += ["    nd = open('/proc/%d/stat' % os.getpid(), 'rb').read()",
             f"    open({str(tep_comm)!r}, 'wb').write(nd[nd.index(b'(') + 1:nd.rindex(b')')])",
             f"    f = open({str(tep_nhip)!r}, 'a')",
             "    for _ in range(1200):",
             "        f.write('.'); f.flush(); time.sleep(0.1)",
             "    ly_do = 'han_song'",
             "finally:",
             f"    open({str(tep_nhip) + '.tu_thoat'!r}, 'w').write(ly_do)"]
    return _NL.join(dong) + _NL


def _k124_tu_thoat(tep):
    """Dấu TỰ THOÁT mà chính tiến trình ghi ở `finally`: `han_song`, `ngoai_le`; None = không tự thoát (tín hiệu
    giết nó, hay nó còn sống). Tín hiệu mặc định giết tiến trình KHÔNG chạy `finally`, nên dấu phân biệt được hai
    đường mà "đã chết" gộp làm một."""
    try:
        return Path(str(tep) + ".tu_thoat").read_text()
    except FileNotFoundError:
        return None


def _k124_tu_thoat_vo_can(ten, tu):
    if tu not in (None, "han_song"):
        raise RuntimeError(f"dieu kien dung: {ten} tien trinh do ca sinh chet vi {tu} - khong bi giet, khong het han")


def _k124_cho_tep(p, han=10.0):
    het = time.time() + han
    while time.time() < het:
        if p.exists() and p.stat().st_size:
            return True
        time.sleep(0.05)
    return False


def _k124_run(s, lenh):
    """`launcher.py run --deadline-utc` thật (hạn 3 s); trả (rc, sổ run.json dạng --json)."""
    repo = tao_repo(s)
    r = chay("run", "--workspace", str(repo), "--run-root", str(s / "runs"), "--json",
             "--deadline-utc", mai_sau(3), "--", *lenh)
    so = {}
    dong = [d for d in r.stdout.splitlines() if d.startswith("{")]
    if dong:
        so = json.loads(dong[-1])
    if not so.get("pid") or r.returncode not in (MA_QUA_HAN, 125, MA_DANH_TINH):
        raise RuntimeError(f"dieu kien dung: launcher khong ket thuc bang ma han chot 124/125/10 kem so JSON: "
                           f"rc={r.returncode}, stderr={r.stderr[-160:]!r}")
    return r.returncode, so


def _k124_ket_luan(ten, rc, pid, tn):
    """Hai assertion, đúng thứ tự: (1) 124 KHÔNG đi cùng cây còn sống; (2) quá hạn phải GIẾT — con TỰ THOÁT ở hạn
    sống là KHÔNG bị giết (ĐỎ); con chết vì ngoại lệ là lỗi điều kiện dựng (không phải TinHieuChotCa)."""
    n1 = tn.stat().st_size if tn.exists() else 0
    time.sleep(1.0)
    n2 = tn.stat().st_size if tn.exists() else 0
    tu = _k124_tu_thoat(tn)
    _k124_tu_thoat_vo_can(ten, tu)
    song = bool(pid) and _k124_song(pid)
    bang(not (rc == MA_QUA_HAN and (song or n2 != n1)),
         f"{ten} 124 noi doi: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}")
    bang(rc == MA_QUA_HAN and not song and n2 == n1 and tu is None,
         f"{ten} qua han khong giet duoc: rc={rc}, con {pid} song={song}, nhip {n1}->{n2}, tu thoat={tu}")


def _k124_dang_doc(ten, ghi):
    """(3) `read args`: mọi lời đọc /proc/<pid>/stat trong cửa sổ đúng DANG_DOC_QA7, và không `open` nào ngoài chúng."""
    if not ghi:
        raise RuntimeError(f"dieu kien dung: {ten} khong co loi doc /proc/<pid>/stat nao")
    lech = sorted({repr(x) for x in ghi if x != DANG_DOC_QA7})
    if _K124_MO["ngoai"]:                      # mở tệp ngoài lời đọc Path đã ghi: danh sách cho phép đóng ở MỌI API
        lech.insert(0, f"open ngoai loi doc Path: {len(_K124_MO['ngoai'])} su kien, vd {_K124_MO['ngoai'][:2]}")
    bang(not lech, f"{ten} read args {lech[:3]}")


def _k124_khoa_that(pid: int) -> str:
    """Khoá theo ĐỊNH DẠNG NỀN `linux:<starttime>` (trường 22), đọc BYTES độc lập — neo định dạng khoá của Q-A.7."""
    bat, _K124_MO["bat"] = _K124_MO["bat"], False      # lời đọc của CHÍNH ca: không đếm vào `open` của cửa sổ
    try:
        with open(f"/proc/{pid}/stat", "rb") as f:
            nd = f.read()
    finally:
        _K124_MO["bat"] = bat
    return "linux:" + nd[nd.rindex(b")") + 2:].split()[19].decode("ascii")


@ca
def t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song():
    """`run --deadline-utc`: con đổi comm thành UTF-8 hỏng SAU khi launcher lấy khoá (nền 89fc4fa:
    rc=124, `giet_tron_ven=True`, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/prctl/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [PY, "-c", _k124_ma_con(tc, tn, 0.5, True)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: con chua doi comm thanh 15 byte hong")
            if not so.get("khoa_danh_tinh"):
                raise RuntimeError("dieu kien dung: comm hong TRUOC luc lay khoa (ca nay can SAU)")
            _k124_ket_luan("B8-sau-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


@ca
def t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc():
    """Tên chương trình tiếng Việt ⇒ comm hỏng NGAY LÚC SINH (kernel cắt 15 byte), không cần prctl
    (nền 89fc4fa: `khoa=None`, rc=10, con vẫn sống)."""
    if platform.system() != "Linux":
        return "bo qua: comm/proc chi co tren Linux"
    if _k124_locale_giai_ma_duoc():
        return "bo qua: locale hien hanh giai ma duoc 15 byte comm hong - loi 124 khong tai hien duoc o day"
    with San() as s:
        ten = s / "kiểm_tra_tiến_trình"
        try:
            os.symlink(PY, ten)
        except (OSError, UnicodeEncodeError) as e:
            raise RuntimeError(f"dieu kien dung: khong tao duoc ten tieng Viet: {e}")
        tc, tn = s / "comm.bin", s / "nhip.txt"
        try:
            rc, so = _k124_run(s, [str(ten), "-c", _k124_ma_con(tc, tn, 0.0, False)])
            pid = so.get("pid")
            if not (_k124_cho_tep(tc, 1) and tc.read_bytes() == _K124_COMM):
                raise RuntimeError("dieu kien dung: comm luc sinh khong phai 15 byte hong")
            _k124_ket_luan("B8-luc-sinh", rc, pid, tn)
        finally:
            _k124_don_con(tn)


_K124_MA_CHAU = _NL.join([
    "import ctypes, os, signal, sys, time",
    "signal.signal(signal.SIGTERM, signal.SIG_IGN)",
    "ly_do = 'ngoai_le'",
    "try:",
    "    ctypes.CDLL(None).prctl(15, bytes.fromhex(sys.argv[2]), 0, 0, 0)",
    "    open(sys.argv[1], 'w').write(str(os.getpid()))",
    "    time.sleep(120)",
    "    ly_do = 'han_song'",
    "finally:",
    "    open(sys.argv[1] + '.tu_thoat', 'w').write(ly_do)"]) + _NL
_K124_MA_ME = _NL.join([
    "import subprocess, sys, time",
    "subprocess.Popen([sys.executable, '-c', sys.argv[5], sys.argv[2], sys.argv[3]],",
    "                 start_new_session=(sys.argv[1] == '1'))",
    "if sys.argv[4] == 'thoat':",
    "    sys.stdin.readline()",
    "    sys.exit(0)",
    "time.sleep(120)"]) + _NL


def _k124_me_chau(s, setsid: bool, me_thoat: bool):
    tp = s / "chau.pid"
    me = subprocess.Popen([PY, "-c", _K124_MA_ME, "1" if setsid else "0", str(tp), _K124_COMM_CHAU.hex(),
                           "thoat" if me_thoat else "o_lai", _K124_MA_CHAU],
                          start_new_session=True, stdin=subprocess.PIPE)
    chau = None
    try:
        if not _k124_cho_tep(tp):
            raise RuntimeError("dieu kien dung: chau chua ghi pid")
        chau = int(tp.read_text())
        with open(f"/proc/{chau}/stat", "rb") as f:
            nd = f.read()
        if nd[nd.index(b"(") + 1:nd.rindex(b")")] != _K124_COMM_CHAU:
            raise RuntimeError("dieu kien dung: comm cua chau chua doi")
    except BaseException:
        if chau:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
        with contextlib.suppress(OSError):
            me.kill()
        me.wait()
        raise
    return me, chau


@ca
def t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM():
    """Cháu `setsid()` (killpg không với tới), comm hỏng, phớt lờ SIGTERM: chỉ ẢNH CHỤP + kiểm
    sống/khoá từng pid giết được nó. Phủ `_chup_cay`, `_con_song` nhánh tệp có, `_khoa_danh_tinh`."""
    if platform.system() != "Linux":
        return "bo qua: setsid/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, True, False)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            me_rc = me.poll()   # mẹ là con TRỰC TIẾP của ca: None = còn sống; < 0 = tín hiệu giết; >= 0 = tự thoát
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-setsid", tu)
            bang(not (kg.tron_ven and (song or me_rc is None)),
                 f"B8-setsid 124 noi doi: {kg.mo_ta}; chau {chau} song={song}, me rc={me_rc}")
            bang(kg.tron_ven and not song and tu is None and me_rc is not None and me_rc < 0,
                 f"B8-setsid khong giet duoc: tron_ven={kg.tron_ven}, chau song={song}, chau tu thoat={tu}, "
                 f"me rc={me_rc}, {kg.mo_ta}")
            _k124_dang_doc("B8-setsid", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()


@ca
def t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong():
    """Mẹ đã thoát, cháu CÙNG NHÓM comm hỏng còn sống: `_khoa_danh_tinh(me)` = None là ĐÚNG (mẹ đã
    biến mất) và chỉ phép quét nhóm còn thấy cháu. Phủ `_thanh_vien_nhom` (và `_chup_cay` theo nhóm)."""
    if platform.system() != "Linux":
        return "bo qua: nhom tien trinh/proc chi co tren Linux"
    m = _tai_launcher_thu()
    with San() as s:
        me, chau = _k124_me_chau(s, False, True)
        try:
            with _k124_ghi_doc() as ghi:
                khoa = _k124_khoa_that(me.pid)
                me.stdin.write(b"x" + _NL.encode())
                me.stdin.close()
                me.wait(timeout=10)
                kg = m._giet_cay(me.pid, khoa)
            song = _k124_song(chau)
            tu = _k124_tu_thoat(s / "chau.pid")
            _k124_tu_thoat_vo_can("B8-me-thoat", tu)
            bang(not (kg.tron_ven and song), f"B8-me-thoat 124 noi doi: {kg.mo_ta}; chau {chau} song")
            bang(kg.tron_ven and not song and tu is None, f"B8-me-thoat khong giet duoc: tron_ven={kg.tron_ven}, "
                                                          f"chau song={song}, chau tu thoat={tu}, {kg.mo_ta}")
            _k124_dang_doc("B8-me-thoat", ghi)
        finally:
            with contextlib.suppress(OSError):
                os.kill(chau, signal.SIGKILL)
            with contextlib.suppress(OSError):
                me.kill()
            me.wait()
```

**Các chốt chung**

- **B5 (mục 2) — `DOT_BIEN`: DANH SÁCH CÓ THẨM QUYỀN DUY NHẤT của đột biến mới.** Mọi chỗ khác trong
  đặc tả (kể cả §6) chỉ trỏ về đây; riêng không gian các ĐƯỜNG, bảng không gian mở rộng ở B2 (r7) là bản liệt
  kê có thẩm quyền của các Ô và hạng mục, và mỗi dòng dưới đây thuộc một hạng mục của bảng ấy: 46 dòng ở trục
  "ngoại lệ nào × tầng nào" (kể cả cột Đ0 và hàng R0), 8 dòng ở trục đếm C và cú pháp S ((c), (f), (j1), (j2),
  (k1), (k5), (m4), (m5)); kiểm đếm ở B2. Hạng mục không có dòng ở đây được đo bằng phép (E) bên dưới, KHÔNG
  bằng mục `DOT_BIEN` (sàn Windows, B4). Executor **đếm lại** trên mã thực thi và khai. **Mười ba LỚP**
  đột biến (a)–(m), mỗi lớp trỏ đích là ca mới; số mục `DOT_BIEN` thật là số **dòng biến thể** dưới đây, suy
  ra từ quy tắc ngay sau danh sách (kỳ vọng **năm mươi tư**; r6: bốn mươi chín). Mỗi dòng nêu vị trí mã, hành vi bị đổi, và
  nhãn giết kèm tiểu nhãn mong đợi (tiểu nhãn: bảng ngay sau bảng không gian B2); các dòng (k5), (l1)–(l29) và
  (m1)–(m5) còn nêu LOẠI assertion mà thông điệp chết phải mang (xem "loại assertion" ở B2):
  (a) gỡ bản vá (trả `:651` về nguyên dạng nền) ⇒ `t156_...` đỏ ở `B1`;
  (b) thay bản vá bằng bản RỘNG ⇒ `t156_...` đỏ ở `B2-eacces`;
  (c) bỏ phép đọc nội dung trên đường lỗi mới, chỉ hỏi `kill(pid, 0)` ⇒ **cả** `t156_...` (đỏ ở
  `B3-zombie`) **và** `t157_...` (đỏ ở `B3b-giet-cay`);
  (d) hai dòng, hai vị trí — (d1) ở phép hỏi chỉ bắt `PermissionError` (giữ nhánh ESRCH riêng), để EIO thoát ⇒ `t156_...` đỏ ở
  `B2-eio`; (d2) ở tầng đọc chỉ bắt `PermissionError` thay cho `OSError` (vẫn bắt lỗi phân tích) ⇒
  `t156_...` đỏ ở `B2-doc-hong`, tiểu nhãn `EIO` (ESRCH ở tầng đọc cũng thoát nhưng đứng sau EIO trong thứ
  tự nên không phải tiểu nhãn báo);
  (e) hai dòng, hai vị trí — (e1) nuốt `BaseException` quanh phép hỏi ⇒ `t156_...` đỏ ở `B2-tin-hieu`,
  tiểu nhãn `hoi`; (e2) ở tầng đọc nuốt riêng `KeyboardInterrupt`, vẫn truyền `RuntimeError` ra ⇒ `t156_...`
  đỏ ở `B2-tin-hieu`, tiểu nhãn `doc`;
  (f) hỏi `exists()` lần hai ⇒ `t156_...` đỏ ở `B2-dem-lan`;
  (g) hai dòng, CÙNG vị trí (tầng đọc), hai hành vi — (g1) trả `False` cho mọi lỗi đọc (`OSError`; nói rõ ở r7: rig r6 cài (g1) đổi CẢ nhóm
  phân tích sang `False`, tức chạm thêm ô R3-Đ của (i) — hai cách cài cho hai số bộ tương đương khác nhau, xem
  đính chính sau bảng 8) ⇒ `t156_...` đỏ ở
  `B2-doc-hong`, tiểu nhãn `EACCES`; (g2) chỉ trả `False` riêng cho `ProcessLookupError`, các lỗi đọc khác
  vẫn hỏi PID dự phòng ⇒ `t156_...` đỏ ở `B2-doc-hong`, tiểu nhãn `ESRCH`;
  (h) hai dòng, hai vị trí — thay bắt `OSError` bằng `Exception`, giữ nhánh ESRCH riêng: (h1) ở phép hỏi ⇒
  `t156_...` đỏ ở `B2-exception`, tiểu nhãn `hoi`; (h2) ở khối đọc ⇒ `t156_...` đỏ ở `B2-exception`, tiểu
  nhãn `doc`; cả hai với sentinel `RuntimeError`;
  (i) khi phân tích nội dung hỏng, trả `False` thay vì hỏi PID dự phòng ⇒ `t156_...` đỏ ở `B2-parse`
  (tiểu nhãn `p1`, đầu vào đầu tiên) bằng assertion kết quả, không phải `ValueError` vô can;
  (j) hai dòng, hai vị trí — đọc nội dung dự phòng lần hai: (j1) đặt sau lần đọc thành công ⇒ `t156_...`
  đỏ ở `B2-dem-doc`, tiểu nhãn `1`; (j2) đặt trong xử lý lần đọc lỗi ⇒ `t156_...` đỏ ở `B2-dem-doc`, tiểu
  nhãn `3`.

  (k) năm dòng, CÙNG vị trí (chỗ đường đọc lỗi hoặc nội dung hỏng quyết định sống hay chết, Q-A.4), năm hành
  vi — bốn dòng đầu bỏ hoặc bóp méo đúng MỘT chiều của bước PID dự phòng, nên mỗi dòng chết ở một tiểu nhãn kết
  quả riêng của `B2-pid-du-phong`; dòng thứ năm (r6) là trục đếm: (k1) trả `True` ngay, không hỏi `kill(pid, 0)` ⇒ `t156_...` đỏ ở
  `B2-pid-du-phong`, tiểu nhãn `song` (số lời gọi `kill(pid, 0)` bằng 0); (k2) gọi `kill(pid, 0)` đúng một lần
  nhưng BỎ kết quả, luôn trả `True` ⇒ đỏ ở tiểu nhãn `da-wait` (PID đã `wait`, kết quả `True` thay vì `False`;
  số lời gọi bằng 1 nên `song` xanh); (k3) tự xử lý `kill` trên đường lỗi mới, mọi `OSError` kể cả
  `PermissionError` ⇒ `False` ⇒ đỏ ở tiểu nhãn `eperm` (kết quả `False` thay vì `True`); (k4) tự xử lý `kill`
  trên đường lỗi mới, `ProcessLookupError` ⇒ `False` nhưng `OSError` khác ⇒ `True` ⇒ đỏ ở tiểu nhãn `eio` (kết
  quả `True` thay vì `False`); (k5) hỏi `kill(pid, 0)` trong xử lý lỗi đọc RỒI để khối chung hỏi lần nữa (hai lời
  gọi, kết quả vẫn đúng) ⇒ đỏ ở tiểu nhãn `song`, loại `kill count`, bộ đếm bằng 2 — dòng này khác (k1) ở chỗ
  (k1) có 0 lời gọi. Cả bốn dòng đầu đều xanh với hai ca mẫu của r4 (không có nhãn này); không dùng
  `B3-da-wait` (không seam) thay cho PID đã `wait` TRÊN đường lỗi mới. Vì sao bốn dòng chứ không một: HINT
  lượt 4 đề nghị một dòng (k) ở tiểu nhãn `song`; nhưng khi `song` đã giết mutant bằng bộ đếm thì kết quả
  `da-wait`, `eperm`, `eio` không còn mutant nào chạm tới, và tiểu nhãn nào không có mutant độc chiếm thì
  chỉ còn được giữ bởi assertion chứ chưa được đo có răng (đúng chỗ r4 đã nêu cho tiểu nhãn `EIO` của
  `B2-doc-hong`). Đã đo (bảng 6): k2, k3, k4 qua hai ca mẫu của r4 và chết đúng một tiểu nhãn mỗi cái;
  giữ nguyên mọi dòng (a)–(j).

  (l) hai mươi chín dòng (r6), MỘT dòng cho mỗi hướng còn thiếu của bảng không gian ở B2; mỗi dòng ghi ô của bảng
  trong ngoặc vuông, nhãn và tiểu nhãn giết, và loại assertion. Nhóm theo tầng:
  · Tầng H (phép hỏi) —
  (l1) [R2-H] phép hỏi chỉ bắt `ProcessLookupError` (bản vá tối thiểu cho đúng ESRCH), `OSError` khác thoát
  ⇒ đỏ ở `B2-eacces`, loại `seam escaped`;
  (l2) [R1-H] phép hỏi để ESRCH rơi cùng nhánh với `OSError` khác (vào bước đọc, không có nhánh `False` riêng)
  ⇒ đỏ ở `B1`, loại `result True`;
  (l3) [R2-H] phép hỏi cho `PermissionError` vào bước đọc nhưng trả `False` cho `OSError` khác, giữ nhánh ESRCH
  riêng ⇒ đỏ ở `B2-eio`, loại `result False`;
  (l4) [R2-H] phép hỏi chỉ nhận `OSError` mang errno EACCES hoặc EIO (danh sách trắng), errno khác thoát, giữ
  nhánh ESRCH riêng ⇒ đỏ ở `B2-eperm-hoi`, loại `seam escaped`;
  (l5) [R2-H] phép hỏi trả `False` riêng cho errno EPERM, còn lại vào bước đọc ⇒ đỏ ở `B2-eperm-hoi`, loại
  `result False`;
  (l6) [R3-H] phép hỏi thêm `IndexError` vào nhóm bắt ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `hoi-index`, loại
  `sentinel identity`;
  (l7) [R3-H] phép hỏi thêm `ValueError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `hoi-value`, loại `sentinel identity`;
  (l8) [R3-H] phép hỏi thêm riêng `UnicodeDecodeError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `hoi-decode`, loại
  `sentinel identity`. (Bản
  HINT lượt 5 đề nghị MỘT dòng (h3) gộp `OSError`, `ValueError`, `IndexError` vào phép hỏi; đo trên rig r6 dòng
  ấy chết ở `hoi-index`, cùng chỗ với (l6), nên nó và (l6) là một bộ tương đương theo tiểu nhãn. r6 tách theo
  thành viên để `hoi-value` và `hoi-decode` cũng có đột biến độc chiếm: (l6), (l7), (l8) chết ở ba tiểu nhãn
  khác nhau, thứ tự `index`, `value`, `decode` có chủ ý vì `ValueError` là cha của `UnicodeDecodeError`.)
  (l9) [R4-H] phép hỏi bắt `Exception` rồi ném `RuntimeError` mới bằng `raise … from …` ⇒ đỏ ở `B2-exception`,
  tiểu nhãn `hoi`, loại `seam wrapped`;
  · Tầng Đ (phép đọc) —
  (l10) [R2-Đ] tầng đọc chỉ bắt `ValueError` và `IndexError`, `OSError` thoát ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn
  `EACCES`, loại `seam escaped`;
  (l11) [R1-Đ] tầng đọc chỉ nhận `OSError` mang errno EACCES hoặc EIO ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn `ESRCH`,
  loại `seam escaped`;
  (l12) [R2-Đ] tầng đọc chỉ nhận errno EACCES, EIO hoặc ESRCH ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn `EPERM`, loại
  `seam escaped`;
  (l13) [R2-Đ] tầng đọc trả `False` riêng cho errno EPERM ⇒ đỏ ở `B2-doc-hong`, tiểu nhãn `EPERM`, loại
  `result False`;
  (l14) [R2-Đ] tầng đọc cho `PermissionError` rơi về bước kill nhưng trả `False` cho `OSError` khác ⇒ đỏ ở
  `B2-doc-hong`, tiểu nhãn `EIO`, loại `result False`;
  (l15) [R3-Đ] tầng đọc không bắt `ValueError` (chỉ `OSError` và `IndexError`) ⇒ đỏ ở `B2-parse`, tiểu nhãn
  `p1`, loại `parse error escaped`;
  (l16) [R3-Đ] tầng đọc thay bắt `ValueError` bằng kiểm tra dữ liệu chỉ nhận ra chuỗi rỗng ⇒ `p1` qua, đỏ ở
  `B2-parse`, tiểu nhãn `p2`, loại `parse error escaped`;
  (l17) [R3-Đ] tầng đọc không bắt `IndexError` ⇒ đỏ ở `B2-parse`, tiểu nhãn `p3`, loại `parse error escaped`;
  (l18) [R3-Đ] tầng đọc trả `False` riêng cho `IndexError`, phần còn lại rơi về kill ⇒ đỏ ở `B2-parse`, tiểu
  nhãn `p3`, loại `result False`;
  (l19) [R3-Đ] phép đọc chỉ bắt `OSError` còn biểu thức tách bọc riêng bắt `ValueError` và `IndexError`, nên
  `UnicodeDecodeError` do `read_text` ném thoát ⇒ đỏ ở `B2-parse`, tiểu nhãn `p4`, loại `seam escaped`;
  (l20) [R3-Đ] tầng đọc trả `False` riêng cho `UnicodeDecodeError` ⇒ đỏ ở `B2-parse`, tiểu nhãn `p4`, loại
  `result False`;
  (l21) [R3-Đ] tầng đọc bọc lại `ValueError` tự nhiên thành `RuntimeError` mới bằng `raise … from …` ⇒ đỏ ở
  `B2-parse`, tiểu nhãn `p1`, loại `parse error wrapped`;
  · Tầng K (khối `kill`) —
  (l22) [R1-K] khối `kill` chỉ có mệnh đề `PermissionError`, ESRCH thật thoát ⇒ đỏ ở `B2-pid-du-phong`, tiểu
  nhãn `da-wait`, loại `seam escaped` (đối tượng là ngoại lệ THẬT mà observer đã ghi lại);
  (l23) [R2-K] khối `kill` chỉ có mệnh đề `ProcessLookupError`, EPERM thoát ⇒ đỏ ở `B2-pid-du-phong`, tiểu
  nhãn `eperm`, loại `seam escaped`;
  (l24) [R2-K] khối `kill` bỏ mệnh đề `OSError` (giữ hai mệnh đề kia), EIO thoát ⇒ đỏ ở `B2-pid-du-phong`, tiểu
  nhãn `eio`, loại `seam escaped`;
  (l25) [R5-K] khối `kill` thêm mệnh đề bắt `BaseException` ⇒ đỏ ở `B2-tin-hieu`, tiểu nhãn `kill`, loại
  `sentinel identity`;
  (l26) [R4-K] khối `kill` thêm mệnh đề bắt `Exception` ⇒ đỏ ở `B2-exception`, tiểu nhãn `kill`, loại
  `sentinel identity`;
  (l27) [R3-K] khối `kill` thêm mệnh đề bắt `IndexError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `kill-index`, loại
  `sentinel identity`;
  (l28) [R3-K] khối `kill` thêm mệnh đề bắt `ValueError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn `kill-value`, loại
  `sentinel identity`;
  (l29) [R3-K] khối `kill` thêm mệnh đề bắt riêng `UnicodeDecodeError` ⇒ đỏ ở `B2-thoat-parse`, tiểu nhãn
  `kill-decode`, loại `sentinel identity`.
  (m) năm dòng (r7, cross-review lượt 6) — cột Đ0 của Q-A.3 và hai trục đếm / cú pháp (xem `B2-nhanh-cu` và
  bảng không gian mở rộng ở B2):
  (m1) [R2-Đ0 EACCES, hướng sai; bản vá chạm cả R1–R3 × Đ0] nhánh cũ: đọc lỗi hay nội dung hỏng ⇒ rơi về
  `kill(pid, 0)` thay vì `False` (hợp nhất hai khối đọc về hướng `kill`) ⇒ đỏ ở `B2-nhanh-cu`, tiểu nhãn `EACCES`
  (đầu vào lỗi đầu tiên của cột Đ0; `song` đứng trước và vẫn đúng), loại `result True`;
  (m2) [R5-Đ0, hướng bắt] nhánh cũ bắt `BaseException` ⇒ đỏ ở `B2-nhanh-cu`, tiểu nhãn `tin-hieu`, loại
  `sentinel identity`;
  (m3) [R0-H, tệp vắng, hướng sai] `exists()` trả `False` ⇒ trả `False`, bỏ `kill(pid, 0)` ⇒ đỏ ở `B2-nhanh-cu`,
  tiểu nhãn `vang`, loại `result False`;
  (m4) [trục C, đường ESRCH, hỏi] ESRCH ở phép hỏi ⇒ hỏi `exists()` lại một lần rồi mới trả `False` ⇒ đỏ ở `B1`,
  loại `stat count`;
  (m5) [trục S, Đ] đường mới tách trạng thái theo dấu `)` ĐẦU TIÊN ⇒ đỏ ở `B3-zombie`, loại `result True`.
  Mỗi dòng (l) là một thay đổi ở một vị trí mã. Dòng (l16) là hình dạng "kiểm tra dữ liệu thay cho bắt ngoại
  lệ" mà Q-A.5 cho phép nhưng chỉ khi nó nhận ra mọi dạng nội dung hỏng. Cả 29 dòng và bảng không gian đều
  đến từ MỘT phép liệt kê trước khi vá (§9), không từ danh sách các finding.

  **Quy tắc mục `DOT_BIEN` (r3; r4 cập nhật cho (d), (e), (g); r5 cho (k); r6 cho (h), (k), (l); r7 cho (m)).**
  (a)–(m) ở trên là mười ba LỚP. Mỗi mục `DOT_BIEN` là một bản sao đột biến có tên riêng và làm đúng một thay đổi ở đúng
  một vị trí mã (một mục ghép hai vị trí thì không tách được vị trí nào bị giết, nên không hợp lệ); hai biến
  thể KHÁC HÀNH VI ở cùng một vị trí (như (g1) và (g2), hay (k1) đến (k5)) cũng là các mục riêng. Vì thế số mục
  `DOT_BIEN` = số **dòng biến thể** ở danh sách trên: (a), (b), (c), (f), (i) mỗi lớp một dòng (5);
  (d), (e), (g), (h), (j) mỗi lớp hai dòng (10); (k) năm dòng (5); (l) hai mươi chín dòng (29); (m) năm dòng
  (5) ⇒ **năm mươi tư mục `DOT_BIEN`**. Dòng (c) làm đỏ hai ca nên mang hai kết quả đích, do đó năm mươi tư dòng
  cho **năm mươi lăm cặp (dòng, ca đích)**. Executor đếm lại trên mã của chính mình và khai từng dòng (một dòng
  không dựng được ở cách triển khai đã chọn phải khai `KHÔNG ĐO ĐƯỢC` kèm lý do 4 của §10 — không có vị trí mã tương
  ứng — và nêu vị trí thiếu,
  không lặng lẽ bỏ). Con số "năm mươi tư" là kỳ vọng suy ra, không phải danh sách thứ hai: danh sách có thẩm quyền vẫn là (a)–(m) cùng quy
  tắc này. Lịch sử của con số (bảy mục ở r2 đến năm mươi tư ở r7, cùng các con số HINT lượt 4, lượt 5 đề nghị):
  nguyên văn ở đoạn này của r7 (sha256 `3fc04fe5…5286`) — không chép lại (r8, thu gọn). r7 đến r10 KHÔNG thêm dòng
  nào ngoài năm dòng (m) của HINT lượt 6, dù có 83 hạng mục không có dòng riêng (78 của bảng mở rộng, 5 của trục G):
  dòng Linux-only thứ bảy đã đưa Windows xuống dưới sàn (B4); các hạng mục ấy, và bảy biến thể lớp 124 (M1–M5, M12,
  `g_to_hop_dinh_dang_khoa` — B8), được đo bằng phép (E).

  Mỗi đột biến phải chết **bằng `TinHieuChotCa` của đúng ca đích, đúng nhãn — đúng tiểu nhãn khi dòng của nó
  nêu tiểu nhãn (r4) — và đúng loại assertion khi dòng nêu loại (r6)**, không bằng lỗi vô can
  (bài học *"ĐỘT BIẾN BỊ GIẾT KHÔNG PHẢI ĐỘT BIẾN BỊ GIẾT ĐÚNG LÝ DO"*). Runner hiện có in tên ca kèm
  kiểu ngoại lệ trong ngoặc khi ngoại lệ KHÔNG phải `TinHieuChotCa`, và vẫn cho `OK giet 1/1` — nên
  KHÔNG dùng riêng rc hay chữ `OK` của runner. Phân hạng bằng cách đọc kiểu ngoại lệ, tên ca và nhãn
  (gọi thẳng hàm ca trên bản đột biến để đọc thông điệp `TinHieuChotCa`; runner chỉ in tên ca) và khai
  **ba hạng**: giết thật / tín dụng giả / sống sót, mỗi mục một dòng. Kèm một đối chứng cố ý vô can (ví
  dụ đột biến gây `NameError`) để chứng minh cách phân hạng không cấp tín dụng giả; r6 thêm đối chứng thứ hai
  cho quy tắc nhận ra ngoại lệ tự nhiên của `B2-parse` (một `ValueError` khác đối số phải chết vô can, bảng 8);
  r7 thêm đối chứng thứ ba (cùng kiểu, cùng đối số, khác nguồn), r8 thêm fp2–fp5, r9 thêm fp6, fp6b và hai phép
  giả gọi lại hàm trợ giúp — danh sách và luật ở `B2-parse` (r9: payload theo dõi, mọi đối chứng vô can theo cấu trúc; đo lượt 8,
  ba Python).
  Hạng "tín dụng giả" gồm mutant chết vì ngoại lệ vô can, và mutant chết bằng `TinHieuChotCa` của một ca KHÁC
  ca đích. Chết ở một nhãn khác của CÙNG ca đích thì không phải tín dụng giả nhưng phải khớp quy tắc nhãn của
  phép (A1) dưới đây.

  **Chốt ngược — hai phép đo riêng, không gộp (r3, lớp `chot-nguoc-khong-co-lap`).** Câu của r2 ("nới ca
  đích để nó không kiểm chốt ấy nữa thì mục tương ứng phải chuyển sang sống sót") không xác định phạm vi,
  và khi nhiều assertion phủ giao nhau thì đọc nó theo nghĩa nào cũng sai: đọc là "nới đúng nhãn mà cả ca
  phải sống" thì bác một bộ test đúng; đọc là "tắt cả ca" thì có cặp đỏ/xanh mà không chứng minh nhãn
  nào có răng. Số đo (rig của cross-review lượt 2, dựng theo B1–B3b của r2, chạy lại lúc 11:46:05Z và 11:46:12Z 29-09):
  nới riêng `B1` thì (a) vẫn chết ở `B2-eacces`; nới riêng `B2-eacces` thì (b) vẫn chết ở `B2-eio`; để cả
  ca sống, (a) phải nới cả năm nhãn `B1`, `B2-eacces`, `B2-eio`, `B2-doc-hong`, `B3-zombie`, còn (b) phải
  nới ba nhãn `B2-eacces`, `B2-eio`, `B2-doc-hong` (các số này là số của rig lượt 2 dựng theo B1–B3b của
  r2). **(r12 ĐO, cross-review lượt 11, lớp `khai-khong-do-duoc-ma-do-duoc` — r4 đến r11 ghi "KHÔNG ĐO ĐƯỢC, chưa ai
  nới tuần tự" cho con số hiện hành.)** Nới tuần tự trên helper r9 (`635d93fa…0494`, 17 nhãn) với `cand_a` của reviewer
  lượt 11 (bảng 14; `python3.11`, `python3.12`, `python3.13` cùng số): mỗi lượt gọi `t156` với tập NỚI thêm đúng nhãn vừa
  giết, tới khi ca sống. (a) gỡ bản vá phải nới **12** nhãn — `B1`, `B2-eacces`, `B2-eio`, `B2-eperm-hoi`, `B2-doc-hong`,
  `B2-tin-hieu`, `B2-exception`, `B2-thoat-parse`, `B2-parse`, `B2-dem-doc`, `B2-pid-du-phong`, `B3-zombie`; (b) bản RỘNG
  phải nới **11** — đúng tập ấy trừ `B1`; nền `423b4ba` (không có Q-A.7) phải nới 14 — thêm `B2-dem-lan` và `B2-nhanh-cu`
  (`read args`); `cand_a` sống ngay, không nới gì. Đó là các chốt có ích chồng lên nhau, không phải test
  yếu, và **không được xoá cho gọn**. r3 tách hai phép đo, mỗi dòng biến thể chạy CẢ HAI, ở từng ca đích
  ((c): làm riêng cho `t156_...` và cho `t157_...`):
  · **(A) CA ĐẦY ĐỦ.** Gọi hàm ca đăng ký (mặc định của helper: mọi nhãn chạy theo thứ tự, không nới) trên
    bản sao đột biến. Đo hai lần: **A1** không nới gì; **A2** nới đúng nhãn đích, mọi nhãn khác vẫn hiệu lực.
  · **(W) WITNESS CÔ LẬP.** Gọi TRỰC TIẾP cùng helper ấy (không viết lại assertion ở chỗ thứ hai — hai
    bản sẽ trôi lệch), chỉ chạy đầu vào của nhãn đích. Đo hai lần: **W1** nhãn đích không bị nới; **W0**
    nhãn đích bị nới.

  | phép | đầu vào chạy | assertion còn hiệu lực | kết quả cần có |
  |---|---|---|---|
  | A1 | mọi nhãn, đúng thứ tự | mọi assertion của mọi nhãn (kể cả kiểm seam đã chạm và bộ đếm); assertion sai đầu tiên ném | chết bằng `TinHieuChotCa` của ca đích; nhãn báo = nhãn đích, hoặc một nhãn đứng TRƯỚC nhãn đích trong thứ tự thực thi (khai rõ nhãn nào — hợp lệ). Nếu báo ở nhãn đích thì tiểu nhãn báo phải là tiểu nhãn của dòng (khi dòng nêu tiểu nhãn) và loại assertion phải là loại dòng nêu (khi dòng nêu loại; r6) |
  | A2 | mọi nhãn, đúng thứ tự | mọi assertion trừ nhãn đích | KHÔNG đòi gì; khai "sống sót" hoặc "chết ở nhãn Y" (Y là nhãn giết kế tiếp, luôn khác nhãn đích) |
  | W1 | chỉ đầu vào của nhãn đích | chỉ assertion mang nhãn đích | chết bằng `TinHieuChotCa` mà thông điệp mở đầu bằng nhãn đích, rồi đúng tiểu nhãn của dòng khi dòng nêu tiểu nhãn, rồi đúng loại assertion khi dòng nêu loại (r6) |
  | W0 | chỉ đầu vào của nhãn đích (vẫn chạy nguyên) | không assertion nào của nhãn đích; còn lại chỉ lỗi thiết lập và ngoại lệ vô can | sống sót (helper trả về bình thường); bộ đếm seam của nhãn ≥ 1 (chứng tỏ đầu vào ĐÃ chạy) |

  Tiêu chí, mỗi dòng biến thể: **ĐỎ** khi A1 sống sót; khi A1 báo nhãn đứng SAU nhãn đích (nhãn đích
  không còn răng hoặc ánh xạ sai); khi A1 hoặc W1 chết ở nhãn đích nhưng ở tiểu nhãn KHÁC tiểu nhãn của
  dòng (r4: đầu vào của dòng không còn răng riêng, hoặc bị đầu vào khác che); khi A1 hoặc W1 chết đúng nhãn và
  tiểu nhãn nhưng ở loại assertion KHÁC loại dòng nêu (r6: hai hướng của cùng một thành viên dùng chung một
  tiểu nhãn, xem "bộ tương đương" ở B2, nên loại là thứ duy nhất tách chúng); khi W1 không chết đúng nhãn
  đích; khi W0 không sống sót; hoặc khi phép D bên dưới đỏ. Hạng
  **`CHƯA CÓ CHỐT NGƯỢC`** (không phải giết, không phải sống sót) khi W0 chết bằng ngoại lệ vô can hoặc bộ đếm seam
  của W0 bằng 0 — dòng ấy chưa có chốt ngược, và handoff khai thẳng như vậy. (r13 đổi tên hạng: r12 gọi nó bằng đúng
  tên của nhãn trạng thái `KHÔNG ĐO ĐƯỢC` của §10, trong khi đây là kết quả của một phép đo ĐÃ chạy — cross-review lượt
  12; ngữ nghĩa và điều kiện không đổi.) A2 là dữ kiện cho log, không phải điều
  kiện đạt. **Không tính là chứng cứ ngược:** bỏ cả ca hoặc trả sớm; nới bằng cách xoá đầu vào; kết luận
  "sống" từ một W0 mà đầu vào không chạy. **Không nới suite thường:** ca đăng ký không truyền hai
  tham số tuỳ chọn CHẠY/NỚI. A1 KHÔNG tự chứng minh mặc định này: mutant có thể chết ở nhãn đứng trước
  nhãn đích, trong khi W1 truyền tập NỚI rỗng tường minh lại bật nhãn bị tắt ở suite thường.

  **(D) Chốt mặc định độc lập — QUAN SÁT thứ ĐÃ CHẠY, bắt buộc trước khi nhận bằng chứng A/W (r4, lớp
  `chot-nguoc-khong-co-lap`).** Vì sao cần: lời khai của r3 rằng chính A1 khoá mặc định "không nới" của
  helper là SAI. Lượt 3 nới mặc định của helper (test-only, trên bản sao) để chứa `B3-zombie`, rồi chạy
  A/W cho mọi dòng của r3: cả **mười ba cặp (dòng, ca đích)** của mười hai mục vẫn đạt. Cơ chế: dòng (c)
  bỏ toàn bộ phép đọc dự phòng nên A1 chết sớm ở `B2-doc-hong` (một nhãn hợp lệ đứng TRƯỚC `B3-zombie`,
  được A1 chấp nhận), còn W1 truyền tập NỚI rỗng tường minh nên bật lại `B3-zombie` và chết đúng nhãn;
  không phép nào nhìn thấy rằng ở ca đăng ký `B3-zombie` đã bị tắt. Ràng buộc bằng suy luận từ bằng
  chứng giết mutant sản phẩm không khoá được một thuộc tính của chính harness; D phải quan sát trực tiếp.
  1. **Đối tượng đo.** Trên ứng viên KHÔNG đột biến, gọi hai hàm ca đăng ký (`t156_...`, `t157_...`) đúng
     như suite thường, không override CHẠY/NỚI.
  2. **Quan sát.** Bọc `bang` bằng một observer chỉ ghi và chuyển tiếp nguyên vẹn (không đổi kết quả,
     không trả sớm, hoàn nguyên trong `finally`), ghi MỌI lần `bang` được gọi trong cả hai ca — kể cả
     lần đúng — dưới dạng (nhãn, tiểu nhãn nếu có) lấy từ đầu thông điệp.
  3. **Đối chiếu.** Tập ghi được phải BẰNG danh sách đơn vị ở "bảng tiểu nhãn" (ngay sau bảng không gian B2:
     57 đơn vị — 17 nhãn, trong đó tám nhãn tách thành 48 tiểu nhãn (r8; r7: 55 / 46); HINT lượt 6: 41 / 17 / tám / 32; r6: 36 / 16 /
     bảy / 27), và thứ tự xuất hiện lần đầu của từng đơn
     vị trong mỗi ca phải đúng thứ tự cố định ở §7. Danh sách kỳ vọng viết CỨNG trong tập lệnh bằng chứng
     theo §7, KHÔNG lấy từ cấu hình CHẠY/NỚI của chính helper (lấy từ đó thì D đo helper bằng helper).
     Chỉ ghi seam đã chạm hay nhãn được chọn KHÔNG chứng minh assertion có hoạt động.
  4. **Control (D phải đỏ).** Trên bản sao TEST, không đụng mã sản phẩm: (i) lần lượt làm mặc định NỚI
     chứa từng nhãn trong **17 nhãn** ⇒ D đỏ, báo đúng nhãn thiếu; (ii) lần lượt bỏ assertion của từng
     tiểu nhãn trong **48 tiểu nhãn** (r8; r7: 46) của tám nhãn tách được (bỏ MỘT đầu vào, giữ các đầu vào khác của
     cùng nhãn) ⇒ D đỏ, báo đúng tiểu nhãn thiếu. Bản mặc định đúng phải xanh. Kỳ vọng **65 control**
     (17 + 48; r7: 63 = 17 + 46; HINT lượt 6: 49 = 17 + 32; r6: 43 = 16 + 27) cộng hai lần xanh của bản đúng, và ít nhất sáu phép đảo
     thứ tự hai nhãn đều đỏ với tập vẫn đủ: `B1`↔`B2-eacces`, `B2-thoat-parse`↔`B2-exception`,
     `B2-pid-du-phong`↔`B3-song`, `B2-dem-doc`↔`B2-pid-du-phong`, `B2-eperm-hoi`↔`B2-doc-hong` (năm cặp của r6) và
     `B2-pid-du-phong`↔`B2-nhanh-cu` (r7). Đo lượt 8 và bảng 11: 6/6 `missing=[] order=False`, ba Python.
  5. **Chỗ đặt.** D và control của nó nằm ở tập lệnh bằng chứng cục bộ của executor, như phép A/W: D chỉ quan sát
     hai ca của helper; không thêm ca đăng ký, không sửa runner `--dot-bien`, không tăng số mục `DOT_BIEN` sản phẩm.
  6. **Nghĩa vụ nộp và log (r8 thêm phần nộp, cross-review lượt 7).** Nộp kèm handoff chính tập lệnh của D và BẢNG
     control máy đọc được — mỗi dòng: KHOÁ control, thứ bị đổi trên bản sao test (nhãn thêm vào tập NỚI mặc định, hay
     đầu vào bị bỏ), đơn vị thiếu kỳ vọng; cộng danh sách 57 đơn vị viết cứng và sáu cặp đảo thứ tự — dưới dạng TỆP,
     cùng kênh và cùng cách tính sha256 như (E) mục 3; reviewer chạy lại trên đúng SHA ứng viên. (r9) KHOÁ control là
     `nhan:<nhãn>` cho 17 nhãn (thứ tự thực thi ở quy ước chung, cộng `B3b-giet-cay`) và `tieu:<nhãn>/<tiểu nhãn>` cho
     48 tiểu nhãn (bảng tiểu nhãn) — 65 khoá, trích được bằng máy từ chính tệp này (bảng 11). Bảng control có ĐÚNG một
     dòng cho mỗi khoá, và tập lệnh ĐỎ khi thiếu, thừa hay lặp dòng — thiếu một control không phải "control không đỏ",
     nên r8 không bắt được. Control RỖNG (không đổi gì so với bản test) để D xanh, nên rơi đúng vào điều kiện "control
     không đỏ" ở câu cuối mục này (đo ở rig r8 06:35:23Z và bảng 11: bỏ một đơn vị không tồn tại ⇒ D xanh ⇒ control bị
     đánh "không đỏ đúng"). Log: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca,
     và từng dòng control kèm đơn vị thiếu. **Không nhận A1/A2/W1/W0 là đủ** nếu thiếu D, thiếu tập lệnh hay bảng
     control, nếu bản đúng đỏ, hoặc nếu bất kỳ control nào không đỏ.
  Đã đo: lượt 3 đến phiên soạn r7 — D của r6, VERDICT lượt 6, bảng 9 dòng 3 (không chép lại); phiên soạn r8 — bảng
  10 dòng 3 (65 control đỏ, 6/6 phép đảo). **Phiên soạn r9** (bảng 11; ba Python; helper r9 có `read args`, ứng viên
  nháp Q-A.7; 57 đơn vị viết cứng): bản đúng xanh (`t156` 56 đơn vị, `t157` 1, đúng thứ tự); **65 control đều đỏ**,
  mỗi cái báo đúng đơn vị thiếu; 6/6 phép đảo đỏ với `missing=[]`, `order=False`; control RỖNG bị đánh "không đỏ
  đúng".
  **CHƯA ĐO:** tập lệnh bằng chứng của executor và D trên mã của executor.

  **(E) Săn theo bảng không gian mở rộng — MỘT biến thể cho mỗi hạng mục không có dòng B5, trong tập lệnh bằng
  chứng cục bộ, KHÔNG vào `DOT_BIEN` (r7; r9 thêm trục G và B8).** Vì sao cần: 83 hạng mục (78 của bảng mở rộng, 5 của
  trục G) không có mục `DOT_BIEN` riêng, và không được có (B4: dòng Linux-only thứ bảy đưa Windows xuống dưới sàn).
  Không có (E) thì răng của các hạng mục ấy chỉ là lời văn — đúng loại "danh sách tự liệt kê, cho là hết" mà §9 đếm.
  1. **Đối tượng.** Với mỗi hạng mục không có dòng B5 (bảng không gian mở rộng, cột (iii) ghi "E"; trục G), executor
     dựng MỘT biến thể của CHÍNH ứng viên của mình: một thay đổi ở một vị trí mã, vi phạm hạng mục ấy (chạm thêm hạng
     mục khác thì A1 được báo ở nhãn đứng trước, như một dòng B5 — ví dụ đo được: bản trả `False` cho nội dung đọc
     được ở nhánh cũ chết trước ở `B2-dem-lan`, W1 vẫn chết đúng `B2-nhanh-cu song`). Với trục G, biến thể là M1–M5
     của B8. Cộng 35 dòng khác (r11; r10: 27; r9: 26), tên ở mục 6: mười hai biến thể thêm của trục G (B2, "Trục G";
     r11 thêm năm `g_*_open`, một cho mỗi chỗ đọc, "Trục G × API"); ba biến thể trục S ở ba hàm ngoài (r11, B2 "Trục
     S"); hai tổ hợp —
     M12 và `g_to_hop_dinh_dang_khoa` (miễn "một vị
     trí", B8); hai biến thể lặp có điều kiện ("đọc lại chỉ khi EPERM", "kill lần hai chỉ khi đọc gặp EPERM"); năm bản
     vá sai của cross-review lượt 6 trùng (m1)–(m5); tám đối chứng của luật `B2-parse` (khác đối số; cùng đối số khác
     nguồn; fp2–fp5 của r8; fp6, fp6b của lượt 8 — xem `B2-parse`); một đối chứng của loại (2): (j1) viết bằng lần đọc
     thứ hai sai đối số (`LookupError`), phải VÔ CAN; và hai đối chứng phải SỐNG: `song_K0_tach_rieng` — bản ĐỔI CẤU
     TRÚC khối kill của K0 mà ĐÚNG ngữ nghĩa nền (ứng viên dùng chung một khối kill cho K và K0 thì TÁCH K0 ra; ứng viên
     đã tách thì GỘP lại), chứng tỏ các đầu vào K0 không bắt oan một cấu trúc hợp lệ khác; và `song_ba_errno` — bản danh
     sách trắng ba errno (giới hạn đã khai ở mục 3 của danh sách bất khả thi — phải sống, không thì phép đo đang đo thứ
     khác). Ứng viên tách trạng thái trong một hàm trợ giúp thì cộng hai phép giả gọi lại hàm ấy (mục 6). Trên ứng viên
     nháp bộ này có 89 biến thể ở r7, 95 ở r8, 109 ở r9, 110 ở r10 và 118 ở r11 (tám tên mới của r11 đo ở bảng 13; 110
     tên cũ không chạy lại hết).
     **Tập tên và cấu trúc mã (r10, cross-review lượt 9, lớp `doi-chung-gia-dinh-mot-cau-truc`).** Tập TÊN ở mục 6 cố
     định; cấu trúc mã không thêm, bớt hay đổi tên nào. r10 chọn cách **định nghĩa đối chứng độc lập với cấu trúc**,
     KHÔNG khoá cấu trúc. Lý do: Q-A quy định ngữ nghĩa, không quy định cấu trúc; §7 cho phép cả khối kill dùng chung lẫn
     tách riêng (`B2-nhanh-cu`; bảng mở rộng, "khi khối kill còn dùng chung"); khoá một cấu trúc là thêm một ràng buộc
     không quyết định nào đặt ra, và biến `song_K0_tach_rieng` thành đối chứng SỐNG cho một cấu trúc bị cấm. Rà từng
     tên: (i) mọi tên hạng mục, kể cả `k0_*`, là "một thay đổi ở một vị trí mã vi phạm hạng mục ấy" — không phụ thuộc
     cấu trúc: với khối kill dùng chung, thay đổi ấy chạm cả K và A1 được báo ở nhãn đứng trước (luật chung ở trên; đo
     trên ứng viên dùng chung: bảng 11 dòng 4), với khối đã tách nó chỉ chạm K0 (đo ba biến thể `k0_*` trên ứng viên
     tách: bảng 12); (ii) CHỈ `song_K0_tach_rieng` gắn với cấu trúc, và định nghĩa trên (đổi theo chiều ngược với ứng
     viên) cho một bản KHÁC ứng viên ở mọi cấu trúc, nên không rơi vào "bản giống hệt ứng viên" của mục 3; tên là KHOÁ,
     giữ nguyên dù ứng viên đã tách; (iii) `DS-E-C3` giữ điều kiện "chỉ khi ứng viên tách trạng thái trong hàm trợ
     giúp". Câu r8–r9 "số của executor có thể khác nếu cấu trúc mã khác" bị bỏ vì mâu thuẫn với danh sách ĐÓNG (thiếu
     tên ⇒ ĐỎ). Executor khai ánh xạ biến thể → tên ở mục 6.
  2. **Đo.** Mỗi biến thể có đích ở `t156_...`/`t157_...` chạy A1, A2, W1, W0 như một dòng B5. Biến thể hướng
     thoát/sai/bắt/bọc/đếm/cú pháp/dạng đọc: tiêu chí y hệt tiêu chí của một dòng B5 (A1 chết bằng `TinHieuChotCa`
     đúng đích hoặc ở nhãn đứng trước; W1 đúng nhãn, tiểu nhãn, loại; W0 sống, bộ đếm ≥ 1). Biến thể có đích là ca B8:
     chỉ A1 (B8). Biến thể hướng thay thế: ca ĐỎ ở A1, W1 và cả W0 bằng lỗi vô can (không lọt, và nới nhãn không che
     được); đó là hạng "đỏ vô can theo thiết kế", không tính giết thật. Tám đối chứng của luật `B2-parse`, (j1) và hai
     phép giả gọi lại hàm trợ giúp: đỏ VÔ CAN ở A1, W1 và W0. Hai đối chứng sống: cả hai ca SONG, D xanh, VÀ nhân
     chứng dương của mục 5 đúng — thiếu nhân chứng thì đối chứng sống không phân biệt được với bản RỖNG.
  3. **Chỗ đặt, nộp và log.** Như D: tập lệnh bằng chứng cục bộ, không thêm ca đăng ký, không sửa runner, không tăng
     `DOT_BIEN`. Log: lệnh nguyên văn, giờ UTC, rc, và mỗi biến thể một dòng (tên, tên ở mục 6, đích, A1, A2, W1, W0,
     bộ đếm, chấp nhận hay lý do đỏ). Nộp kèm handoff (i) chính tập lệnh bằng chứng (A/W, D, (E), B8; r12: cả
     `chot_tinh_r12.py` — nguyên văn khối ở B2, sha256 khớp số ghi ở đó) và (ii) BẢNG
     biến thể máy đọc được — mỗi dòng: tên, tên ở mục 6, các cặp (neo, thay) trên ứng viên, ca / nhãn / tiểu nhãn /
     loại kỳ vọng; reviewer chạy lại chúng trên đúng SHA ứng viên trước khi kết luận. Tập lệnh phải ĐỎ khi: một biến
     thể có neo không xuất hiện ĐÚNG MỘT lần trong ứng viên, hoặc cho ra bản giống hệt ứng viên (đo chốt ở rig r8,
     bảng 10 dòng 6: rc=3, không ghi biến thể); (r9) tập tên ở cột "tên ở mục 6" của bảng KHÁC danh sách ĐÓNG ở mục 6
     — thiếu, thừa hay lặp một tên (lượt 8 đo: trích bằng máy từ lời văn bảng mở rộng r8 ra 50 tên và bỏ sót 7 đứng
     sau " / " cùng 1 mục văn xuôi, tức r8 không gì đỏ khi bảng thiếu hạng mục; r9 thay luật sinh khoá bằng danh sách
     ĐÓNG viết tại chỗ và đặt tên cho mục văn xuôi ấy). **Kênh nộp (r9): TỆP trong một commit (nhánh bằng chứng riêng,
     ngoài write set thi hành) hoặc artifact, KHÔNG dán vào thân comment**; handoff ghi OID commit (hay ID artifact),
     đường dẫn và sha256; reviewer đọc lại tệp từ chính commit hay artifact ấy (`git show <OID>:<đường dẫn>`) rồi mới
     tính sha256. Lý do: thân comment đọc qua MCP bị chuẩn hoá `'` `"` `>` `<` thành thực thể HTML (CLAUDE.md, đo
     22-08-2026); lượt 8 mô phỏng trên ba tập lệnh rig đổi 229 / 162 / 1248 ký tự ⇒ sha256 lệch. Kênh GitHub thật:
     r8–r10 ghi "KHÔNG ĐO ĐƯỢC"; **(r11) phía đọc ĐO ĐƯỢC** — tệp r1 của chính đặc tả trên nhánh
     `ops/spec-launcher-con-song-esrch` (`3915f46`, có `'` ×2, `"` ×22, `<` ×6, `>` ×6) đọc lại bằng `git fetch` +
     `git show` và bằng REST `contents` đều ra đúng sha256 `ee44238c…37d9` (bảng 13); phía ghi là `git push` một blob
     định danh bằng băm nội dung, phiên soạn không đẩy (chỉ thị điều phối) nên không thử; kênh git cục bộ: bảng 11.
     **Không nhận bằng chứng B5 là đủ** nếu thiếu (E), thiếu
     tập lệnh hay bảng, hoặc có biến thể nào không đúng kỳ vọng.
  4. **Giới hạn khai thẳng (r8 sửa câu "răng BỀN" của r7).** (E) chạy MỘT lần trước merge; nó không nằm trong
     `--dot-bien` nên KHÔNG được đo lại ở các lượt sau. Phép D cũng nằm trong tập lệnh cục bộ và cũng chạy MỘT lần.
     Vậy răng BỀN (đo lại ở mỗi lượt `--dot-bien`) của 83 hạng mục ấy và của bốn ca B8: KHÔNG CÓ. Thứ còn lại sau merge
     chỉ là assertion của các ca — chạy ở mỗi lượt suite, nhưng không phép nào đo lại rằng chúng còn đỏ được với vi
     phạm. Một biến thể cho mỗi hạng mục cũng không chứng minh mọi cách viết vi phạm hạng mục ấy đều bị bắt.
  5. **Nhân chứng dương cho hai đối chứng sống (r8, cross-review lượt 7).** "Hai ca SONG, D xanh" không phân biệt
     được đối chứng thật với bản rỗng, nên mỗi đối chứng kèm MỘT phép đo chứng tỏ nó thật khác ứng viên: bản danh
     sách trắng ba errno ⇒ `_con_song(os.getpid())` với seam `OSError(errno.ENOMEM, …)` ở `Path.stat` phải THOÁT
     `OSError` errno 12 trong khi ứng viên trả `True`; bản ĐỔI CẤU TRÚC K0 ⇒ **số nút gọi `os.kill` (AST) trong thân
     `_con_song` cộng thân mọi hàm mức module của `launcher.py` mà `_con_song` gọi trực tiếp, mỗi hàm tính một lần,
     KHÁC ứng viên** (r10; dạng r8–r9 "HAI lời gọi, ứng viên: một" chỉ đúng cho ứng viên dùng chung). Đã đo: ENOMEM ⇒
     ứng viên `True`, danh sách trắng `OSError errno=12`, bản rỗng `True` (ba Python; reviewer lượt 7, bảng 10 dòng 6);
     phép đếm ⇒ ứng viên dùng chung 1, ứng viên tách 2 (lượt 9; bảng 12).
  6. **(r9) Danh sách tên ĐÓNG của bảng (E)** — mỗi tên đúng MỘT dòng. `DS-E-HANG-MUC`: 78 tên của bảng mở rộng
     (cột (iii), khai triển `<tv>`) cộng 5 của trục G; `DS-E-KHAC`: 35 dòng khác (r11; r10: 27; r9: 26); `DS-E-C3`: chỉ khi ứng viên tách
     trạng thái trong hàm trợ giúp. Tên ở đây là KHOÁ; tên biến thể của executor tự đặt và ánh xạ vào khoá. Dòng đầu
     mỗi nhóm ghi số tên, để tập lệnh tự kiểm số đếm:

```
DS-E-HANG-MUC 83
h_co_bo_doc d0_ok_khongZ_sai d0_ok_Z_sai k0_ok_sai d_ok_khongZ_sai d_ok_Z_sai k_ok_sai
d0_ESRCH_thoat d0_ESRCH_sai d0_EACCES_thoat d0_EIO_thoat d0_EIO_sai d0_EPERM_thoat d0_EPERM_sai
d0_value_thoat d0_value_sai d0_index_thoat d0_index_sai d0_decode_thoat d0_decode_sai
d0_exception_bat d0_exception_boc d0_exception_thaythe d0_tin-hieu_boc d0_tin-hieu_thaythe
k0_ESRCH_thoat k0_ESRCH_sai k0_EPERM_thoat k0_EPERM_sai k0_EIO_thoat k0_EIO_sai
k0_index_bat k0_value_bat k0_decode_bat k0_index_boc k0_value_boc k0_decode_boc
k0_index_thaythe k0_value_thaythe k0_decode_thaythe k0_exception_bat k0_exception_boc k0_exception_thaythe
k0_tin-hieu_bat k0_tin-hieu_boc k0_tin-hieu_thaythe
h_index_boc h_value_boc h_decode_boc h_tin-hieu_boc d_exception_boc d_tin-hieu_boc
k_index_boc k_value_boc k_decode_boc k_exception_boc k_tin-hieu_boc
h_index_thaythe h_value_thaythe h_decode_thaythe h_exception_thaythe h_tin-hieu_thaythe
d_exception_thaythe d_tin-hieu_thaythe
k_index_thaythe k_value_thaythe k_decode_thaythe k_exception_thaythe k_tin-hieu_thaythe
h_thoat_hoi_lai d0_doc_hai_lan d0_them_kill k0_hoi_hai_lan k0_them_doc k0_kill_hai_lan d_hoi_lai_khac_EACCES k_hoi_hai_lan
d0_tach_ngoac_dau
g_khoa g_nhom g_chup g_d0 g_d
DS-E-KHAC 35
d0_giai_ma_long d_giai_ma_long g_khoa_errors g_nhom_errors g_chup_errors d0_giai_ma_lai_utf8 d_giai_ma_lai_utf8
g_khoa_open g_nhom_open g_chup_open g_d0_open g_d_open
s_khoa_tach_ngoac_dau s_nhom_tach_ngoac_dau s_chup_tach_ngoac_dau
g_to_hop_khoa_nhom g_to_hop_dinh_dang_khoa d_doc_lai_khi_EPERM k_kill_lai_khi_doc_EPERM
luot6_m1 luot6_m2 luot6_m3 luot6_m4 luot6_m5
dc_khac_doi_so dc_fp dc_fp2 dc_fp3 dc_fp4 dc_fp5 dc_fp6 dc_fp6b dc_j1_sai_doi_so
song_K0_tach_rieng song_ba_errno
DS-E-C3 2
dc_c3_goi_lai_rong dc_c3_goi_lai_index
```

  Đã đo: r7 và r8 — bảng 9 dòng 6, 7, 11, 12 và bảng 10 dòng 4 (ứng viên nháp theo r7–r8). **r9** (bảng 11, ba
  Python, ứng viên nháp Q-A.7 — KHÔNG phải mã của executor): đủ 109 dòng cộng hai dòng `DS-E-C3`, mỗi dòng đúng kỳ
  vọng; danh sách mục 6 trích lại được bằng máy từ chính tệp này, và tập lệnh so tập tên ĐỎ khi thiếu, thừa hay lặp.
  **r10** (bảng 12, ba Python): tên mới `g_to_hop_dinh_dang_khoa` chết đúng `t160` `khong giet duoc`; ứng viên tách K0
  (chiều gộp của nó chính là ứng viên dùng chung) SONG ở `t156`, `t157` và QUA bốn ca B8; ba biến thể `k0_*` trên hai
  cấu trúc; danh sách mục 6 trích lại bằng máy từ tệp r10: 83 + 27 + 2 = 112 tên, 0 trùng. 109 tên còn lại không
  chạy lại ở r10 (số của r9). **r11** (bảng 13, ba Python, khối B8 r11): tám tên mới — `s_*_tach_ngoac_dau` (chín bản
  `SX*`, latin-1 và bytes) chết đúng ca B8 và đúng LOẠI của hàng bảng B8; `g_khoa_open`, `g_nhom_open`, `g_chup_open`
  (mười bản `OPEN*`/`PATHOPEN`) và `g_d0_open` chết `read args` (open ngoài lời đọc đã ghi) ở `t160`, `t161`,
  `g_d0_open` còn chết ở `t156` `B2-nhanh-cu song read count 0`; `g_d_open` chết ở `t156` `B2-eacces read count 0`
  (B8 không chạm); `g_to_hop_dinh_dang_khoa` ở cả hai dạng chết `t160` `khong giet duoc` (khoá KHÁC); danh sách mục 6
  trích lại bằng máy từ tệp r11: 83 + 35 + 2 = 120 tên, 0 trùng, số đếm khớp dòng đầu nhóm. Các tên cũ có đích B8
  (M1–M5, M12) chạy lại trên khối r11: trùng bảng 12; tên cũ khác không chạy lại. **CHƯA ĐO:** (E) trên mã của executor.

  **Log mỗi dòng biến thể**: tên mục và vị trí, ca đích, nhãn đích và tiểu nhãn (nếu có), loại assertion
  (nếu dòng nêu; r6), A1 (nhãn, tiểu nhãn và loại báo), A2 (sống sót hoặc nhãn Y — đây là "các nhãn khác vẫn giết nó trong ca đầy đủ"; danh
  sách ĐỦ mọi nhãn giết được nó cần nới tuần tự và không bắt buộc), W1, W0 kèm bộ đếm seam.
  Cách làm là khả thi, không phải lời hứa: năm mươi tư dòng (năm mươi lăm cặp) đã được chấp nhận trên bản nháp Q-A
  (KHÔNG phải ứng viên của executor) ở rig reviewer lượt 6 (phương án r7, dựng trước khi có r7, ba Python), ở rig
  phiên soạn r7 (bảng 9 dòng 2, 4, 9; runner thật 53 dòng `giet 1/1`, (c) `giet 2/2`), r8 (bảng 10 dòng 2), r9
  (bảng 11 dòng 3) và ở rig reviewer lượt 7, lượt 8 (ba Python, theo VERDICT); chi tiết từng rig tới r9: đoạn này
  của r7 (sha256 `3fc04fe5…5286`, dòng cross-review lượt 6) và của r9 (sha256 `1a629c89…a3cf`). r10 không chạy lại.
  Trên ứng viên tham chiếu của §4 và trên ứng viên độc lập của reviewer — cũng KHÔNG phải ứng viên của executor —:
  rig phiên soạn r14 (bảng 16 dòng 9) và rig reviewer lượt 13, lượt 14, lượt 16 (`python3.11` và `python3.12`, theo
  VERDICT). Rig nào chạy cách làm này trước phương án năm mươi tư dòng thì chạy trên B5 nhỏ hơn — của revision lúc
  ấy, hay của phương án HINT mà chính lượt ấy đề nghị (ví dụ lượt 5: hai mươi mục, hai mươi mốt cặp) —; số từng rig:
  đoạn này của r7 và VERDICT lượt 2 đến lượt 6. (r16 sửa, cùng lớp với B7 ở §10: r10 đến r15 gán năm mươi tư dòng
  cho rig reviewer lượt 2 đến lượt 6, và không kể các lượt đo về sau. r17 sửa lại, cross-review lượt 16: câu r16
  viết — ở đây và ở bảng thay đổi đầu r16 — bỏ lượt 6 khỏi danh sách năm mươi tư dòng, trong khi VERDICT lượt 6,
  hướng 12, ghi 55/55 cặp ở ba Python trên phương án năm mươi tư dòng mà r7 áp, và nói rig nào trước r7 chạy
  cách làm này thì chạy trên B5 của revision lúc ấy — lệch VERDICT lượt 5 và lượt 6; phần r16 sửa đúng là lượt 2
  đến lượt 5.) **Chưa có:** năm mươi tư dòng chạy trên ứng viên của executor.
- **B6 (cả write set) — delta và bằng chứng cục bộ thay CI.** **Phiên bản Python GHIM (r10, cross-review lượt 9,
  lớp `bang-chung-khong-ghim-python-san`): mọi lệnh dưới đây chạy HAI lần, bằng `python3.11` (bản của job Ubuntu
  `launcher-windows.yml` hậu-merge, `:64`) và bằng `python3.12` (bản của `ci.yml`); KHÔNG gọi `python` trần**
  (container soạn r10: `python` là 3.11.15 — một sự tình cờ của máy, không phải hợp đồng). Bằng chứng thay CI không
  được hẹp hơn CI nó thay. 3.13 (Windows) chỉ đo sau merge (Q4).
  `python3.1x .claude/dev/launcher_test.py` toàn suite **delta = 0 ca đỏ** so với nền, ở TỪNG bản Python, đo **cả hai
  vế trong một lệnh** trên cùng rig (bài học "PHÉP ĐO DELTA SO HAI VẾ": nền và ứng viên cùng dựng bằng một vòng lặp,
  cùng bước). Số trên bản nháp (không thay phép đo của executor): rig r9, 3.12.3, nền `89fc4fa` — bảng 11 dòng 8; rig
  r10, nền `423b4ba`, 3.11 và 3.12 — bảng 12; rig r11, cùng nền, khối B8 r11 — bảng 13 dòng 13. `python3.1x .claude/dev/launcher_test.py --dot-bien`: không đột biến cũ
  nào đổi hạng. `ruff check --select F --target-version py311 .claude/dev/launcher.py .claude/dev/launcher_test.py`
  (nhị phân `ruff`; `python -m ruff` vắng trong container này): delta F = 0 (ruff vắng: cài được mà chưa cài là CHƯA ĐO,
  không cài được vì không có mạng thì ghi `KHÔNG ĐO ĐƯỢC` kèm lý do 1 của §10; không bao giờ ghi 0). Nền trên `423b4ba`
  (10:47:54Z 30-09, ruff 0.15.8), có và không có `--target-version py311` như nhau:
  `launcher.py` 0 lỗi F; `launcher_test.py` 5 lỗi F, cả năm F841 (dòng 2566, 3387, 3629, 4110, 6062; trên `89fc4fa`
  dòng cuối là 6061). "delta = 0" nghĩa là ứng viên KHÔNG hơn số nền ấy, đo lại trên nền tiếp nối. Lý do ghim đo
  được (VERDICT lượt 9; đo lại ở bảng 12): một bản dạng bytes dùng f-string lồng CÙNG loại dấu nháy (cú pháp PEP 701,
  chỉ hợp lệ từ 3.12) qua suite 3.12 như ứng viên đúng, trong khi `python3.11 launcher.py --help` ⇒ rc=1
  `SyntaxError`; ruff mặc định (kho không có cấu hình ruff) báo `All checks passed!`, chỉ `--target-version py311` bắt.
  **Nghĩa vụ bằng chứng.** Mọi lệnh B1–B6 và B8 chạy **cục bộ trên Linux, đúng SHA ứng viên** (ghi
  `git rev-parse HEAD` cùng log), ở từng bản `python3.11` và `python3.12`, mỗi bản một log. Log mỗi lệnh gồm: khối môi trường ở đầu log (dạng ở ô `environment`; r22; log dùng lại: ngoại lệ ở vế ĐỎ (r22) dưới), rồi lệnh
  **nguyên văn**, giờ UTC bắt đầu, `python3.1x --version`, rc, và
  **dòng tổng nguyên văn** của runner (số qua / chạy / bỏ qua / đỏ; với `--dot-bien` là dòng tổng và
  ba hạng của B5). Log của B5 còn kèm **từng dòng biến thể** với bốn phép đo A1/A2/W1/W0 như đã định
  ở B5 (kỳ vọng năm mươi tư dòng, cũng là năm mươi tư mục `DOT_BIEN`, năm mươi lăm cặp đích), và **log của phép
  D**: lệnh nguyên văn, giờ UTC, rc, dòng xanh của bản đúng cho từng ca đăng ký, và từng dòng trong 65 control (r8; r7: 63)
  (17 mức nhãn, 48 mức tiểu nhãn) cùng các phép đảo thứ tự, kèm đơn vị thiếu; và **log của phép (E)** (B5): mỗi biến
  thể một dòng, kèm ánh xạ sang tên ở (E) mục 6; **log của bốn ca B8** trên ứng viên và A1 của mười bốn biến thể lớp
  124 (M1–M5, M12, `g_to_hop_dinh_dang_khoa`; r10 — cộng ba `s_*_tach_ngoac_dau`, ba `g_*_open` của ba hàm ngoài và
  `g_d0_open`, r11); **đầu ra nguyên văn của `chot_tinh_r12.py`** (B2; r12 thay chốt r11) chạy bằng `python3.11`
  trên SHA ứng viên — dòng `UNG VIEN: DAT`, mọi dòng `DOI CHUNG … DO DUNG LUAT` (13 dòng với dạng latin-1, 14 với dạng
  bytes) và `KET LUAN: DAT | rc=0` — kèm sha256 của tệp script đã chạy;
  và phép tính sàn Windows của B4 (lệnh + số). Đính vào handoff; reviewer đọc **trước** merge. Xanh của `gate-registry` KHÔNG thay
  cho log này (§8). Sau merge, `launcher-windows.yml` chạy ở lượt `push` master: đọc kết quả cả
  Windows lẫn Ubuntu (`land_obligation`), kể cả dòng `DOT BIEN:` của bước `Tu dot bien`, đừng suy thành công từ
  việc đã đẩy.
  **ĐỎ khi:** ứng viên có thêm ca đỏ, đột biến cũ đổi hạng, thêm lỗi F, handoff thiếu log nguyên văn cho
  bất kỳ lệnh nào trong B1–B6 và B8 (ở TỪNG bản Python 3.11 và 3.12; r10), hoặc thiếu log phép D, bản đúng không xanh
  ở D, hay có control của D không
  đỏ; hoặc thiếu log phép (E), hay có biến thể (E) không đúng kỳ vọng; hoặc (r8) thiếu tập lệnh bằng
  chứng, bảng biến thể của (E) hay bảng control của D kèm sha256 (B5 (E) mục 3, D mục 6), thiếu nhân chứng dương
  của hai đối chứng sống ((E) mục 5), hay reviewer chạy lại chúng ra kết quả khác log; hoặc (r9) tập tên của bảng
  (E) khác danh sách ĐÓNG ở (E) mục 6, bảng control của D thiếu, thừa hay lặp khoá (D mục 6), tệp nộp không đọc lại
  được từ commit hay artifact đã khai hoặc sha256 không khớp bytes đọc lại, hay bất kỳ ca B8 nào không QUA trên ứng
  viên; hoặc (r10) handoff thiếu kết quả `git grep -n 'linux:' .claude/dev/launcher.py` trên SHA ứng viên, hay kết quả
  ấy có chỗ dựng khoá ngoài hai chỗ của Q-A.7 mà handoff không khai; hoặc (r11; r12 thay) handoff thiếu đầu ra của
  `chot_tinh_r12.py`, sha256 tệp script khác sha256 khối ở B2, hay script trả rc khác 0 (ứng viên ĐỎ, có đối chứng không
  ĐỎ đúng luật, hay đầu vào hỏng); hoặc (r21, cross-review lớp `moi-truong-nghiem-thu-khai-sai`) một log của B1–B6
  hay B8 không mở đầu bằng khối môi trường của ô `environment` ở đầu tệp — đầu ra nguyên văn của các lệnh (a)–(d) kèm
  giờ UTC — hay khối ấy không đạt (a), (b) hoặc (c); (r22) ngoại lệ: log được dùng lại đủ bốn mỏ neo của đoạn "Mỏ neo bằng chứng dùng lại" ở đầu tệp không bị ĐỎ vì thiếu khối, miễn bộ năm của mỏ neo (iv) đọc được trong chính log ấy — log sinh trong run đang nộp nó không vào được ngoại lệ này, vì mỏ neo (i) đòi băm công bố TRƯỚC run. Sau merge: `DUOI SAN` ở bước `Tu dot bien` của lượt push master là ĐỎ của packet (B4).
- **B7 — bằng chứng từ nơi lỗi lộ ra (không phải cổng).** Chạy `ops/lease_publish_test.py` với seam
  ESRCH chèn vào `launcher.py` bản sao tạm, hoặc chạy `t154` lặp nhiều lần song song: chỉ để khai,
  **không** dùng làm tiêu chí vì race chập chờn không đỏ ổn định (luật L3). Cross-review lượt 1
  (hướng 10) đã chạy `t154` với seam ở bản sao: nền ném `ProcessLookupError`, bản HẸP r1 qua.
  Cross-review lượt 2 (hướng 13, 11:29:11Z 29-09) chạy lại trên bản dựng theo Q-A r2: nền ném
  `ProcessLookupError` sau 1 lần chạm seam; bản dựng qua, 31 lần chạm seam, 4,87 giây, các tiến trình con
  cháu được thu hồi hết. Cross-review lượt 3 (12:50:55Z 29-09) đo lại trên bản dựng theo Q-A r3: nền ném
  `ProcessLookupError` sau 1 lần chạm seam (1,43 giây); bản dựng qua, 31 lần chạm seam, 5,136 giây, con cháu
  thu hồi hết. Đó là số của reviewer trên bản nháp, không phải phép đo trên ứng viên của executor và không
  do phiên soạn r3, r4, r5, r6 hay r7 chạy lại; thời lượng không phải hằng số.

## 8. Số đo nền (thời điểm đo cạnh từng số)

- **(r14) Nền GIỮ `423b4ba`** — `git ls-remote origin refs/heads/master` ⇒ `20ec8d5d…5961` (04:41:44Z 01-10); trên đối
  tượng cục bộ của worktree, không fetch: `423b4ba` và `fc852ff` là tổ tiên của `20ec8d5`, write set rc=0, `.claude
  .github` rỗng (ô nền nghiệm thu; bảng 16 dòng 12). Ngoài write set, `ops/lease_publish_test.py` đổi giữa `fc852ff` và
  `20ec8d5` (+600 / −15), có hunk trong thân `t154` — chỗ lỗi lộ ra của B7, không phải cổng; số B7 ở §7 là của các lượt
  review đầu, trên bản `t154` cũ; r14 không chạy lại. Mọi số nền dưới đây vẫn là số của `423b4ba`.
- **(r12) Nền GIỮ `423b4ba`** — `git ls-remote origin refs/heads/master` ⇒ vẫn `fc852fff…c294` (22:33:02Z 30-09); trên
  đối tượng cục bộ của worktree, không fetch: `423b4ba` là tổ tiên của `fc852ff` (rc=0), write set rc=0, `.claude .github`
  rỗng (ô nền nghiệm thu; bảng 14). Mọi số nền dưới đây vẫn là số của `423b4ba`.
- **(r11) Nền GIỮ `423b4ba`** — đầu `origin/master` trôi sang `fc852ff` (15:31:19Z 30-09), write set và `.claude`,
  `.github` không đổi byte nào (ô nền nghiệm thu; bảng 13 dòng 17); mọi số nền dưới đây vẫn là số của `423b4ba`.
  Đo thêm bằng REST (bảng 13 dòng 16): lượt `push` master của `423b4ba` (run `36696528580`) ĐỎ ở `gate-registry
  (ubuntu-latest)` vì `ops/nhanh_don_duoc_test.py` rc=-9 sau 4500,384 s — ngoài write set, đỏ sẵn trên nền (ô
  `required_checks`).

- **(r10) Nền nghiệm thu DỜI sang `423b4ba`** (worktree của phiên soạn, HEAD `468c88e`, sạch trừ tệp r10 mới):
  `git fetch -q origin master` rc=0 (10:45:10Z 30-09, xong 10:45:11Z); `git rev-parse origin/master` ⇒
  `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (Merge PR #696, commit lúc 2026-09-30T16:30:11+07:00), trùng `git ls-remote
  origin refs/heads/master`; `git rev-list --count c16bec6..origin/master` ⇒ 44. `git diff --quiet
  89fc4fac8cea65979cc2483043dc8cd07a6e8518 origin/master -- .claude/dev/launcher.py .claude/dev/launcher_test.py` ⇒
  **rc=1**: một hunk ở `t152` (ô nền nghiệm thu). `-- .claude .github` ⇒ rc=1, 4 tệp (`ci_dang_ky_test.py`,
  `launcher_test.py`, `.claude/hooks/session-start.sh`, `.github/workflows/ci.yml`; 278 dòng thêm, 10 xoá);
  `launcher-windows.yml` không đổi (`git diff --quiet` rc=0). `89fc4fa..423b4ba`: 91 commit (76 không merge), 61 tệp,
  15 426 dòng thêm, 54 xoá (11:01:04Z). Blob trên `423b4ba`: `launcher.py` `561ff7a1…` (không đổi, 4308 dòng),
  `launcher_test.py` `3f02fb94…` (8355 dòng). `468c88e` chưa là tổ tiên của `origin/master` (rc=1). **Phép so hai
  nguồn ref (r10, trên clone sạch trong rig r10, 10:46:50Z):** `git ls-remote --heads origin` và `git for-each-ref
  refs/remotes/origin` (bỏ `HEAD`) cùng 457 tên, `comm` hai chiều rỗng, `--is-shallow-repository` false. Lượt đo nền
  r3 đến r9 (nền `89fc4fa`, `c16bec6`): §8 của r9 — không chép lại.
- **Độ dài `_con_song` trên nền** (r7, AST `end_lineno` trên bản sao `launcher.py` của `89fc4fa` trong rig r7,
  02:00:46Z 30-09, Python 3.12.3): dòng 629–672, **44 dòng** (kể cả docstring). Khớp số cross-review lượt 6 đo; §9
  của r6 ghi nhầm "77 dòng (629–705)".

- Kích thước (`git show <ref>:<tệp> | wc -l`, r10): trên `423b4ba` — `launcher.py` 4308 dòng (blob `561ff7a1…`, sha256
  `808ce5b3…9fc0`), `launcher_test.py` 8355 dòng (blob `3f02fb94…`, sha256 `882ac43f…97cc`); trên `89fc4fa` —
  `launcher_test.py` 8354 dòng (blob `abf7f6ca…`, sha256 `433af9d4…556a`). Lượt đo kích thước r3–r9: §8 của r9.
- **Số ca của `launcher_test.py`, đếm bằng AST** (hàm mức đỉnh mang decorator `@ca`). r10 trên `423b4ba` (10:47Z 30-09,
  Python 3.12.3) và trên `89fc4fa` (cùng lúc): **189 ca đăng ký = 155 ca tiền tố `t<số>` + 34 ca khác**, hậu tố lớn
  nhất `t155`, 155 hậu tố phân biệt, không hổng trong 1..155 — cả hai nền như nhau (bản vá #696 không thêm ca). Phân
  rã nhóm `r` (`r01`–`r21`, `r345`×5, `r347`×2, `r351`×3, `r348`×2, `r349`×1) và các lượt đếm r3–r9: §8 của r9. **155
  không phải tổng suite**: nó là hậu tố lớn nhất của một nhóm; bản r1 dùng nó làm tổng và sai. Nghiệm thu B6 phải
  đối chiếu số đăng ký, số chạy, số bỏ qua và số đỏ, không suy tổng từ hậu tố. Sau packet này, số đăng ký kỳ vọng
  tăng đúng bằng số ca mới ở §6.2 (**sáu**) — executor đếm lại trên nền tiếp nối và khai.
- `DOT_BIEN` ở `launcher_test.py:7013` trên `423b4ba` (`:7012` trên `89fc4fa`): **174 mục**; `DOT_BIEN_HARNESS` ở
  `:7931` (`:7930`): 3 mục (AST, r10, cả hai nền cùng số). Đây là số mục ĐỘT BIẾN, khác số ca. Số mục mới: xem B5
  (**mười ba** lớp, kỳ vọng **năm mươi tư** mục `DOT_BIEN`); sau packet: bảng sản phẩm 174 + 54 = **228**, cộng 3 mục
  `DOT_BIEN_HARNESS` = **231** mục; số ca đăng ký 189 + 6 = **195** — số kỳ vọng suy ra, chưa đo trên ứng viên của
  executor. r7 đến r10 KHÔNG thêm dòng `DOT_BIEN` nào ngoài lớp (m) (B4, B5); phép (E) và bốn ca B8 không thuộc
  `DOT_BIEN` nên không đổi 228 / 231. Số nhãn 17; 48 tiểu nhãn + 9 đơn vị đơn = 57 đơn vị; D có 65 control (r8 đến
  r10). Các kỳ vọng của r3 đến r7 và của HINT lượt 4 đến lượt 6: §8 của r7, r9.
- **Lease** (r10; `ai-dang-giu` của `ops/lease_publish.py` bản `origin/master`, `python3` = 3.11.15). Lượt thứ nhất
  chạy ở kho chính `/home/user/tra-luat` sau `git fetch --prune` đủ ref và sau khi đưa nhánh `master` cục bộ về
  `origin/master` (tụt 44, fast-forward): **`CHAN [12]`, rc=12** cho cả hai tệp (10:46:23Z) — nhánh cục bộ
  `ops/spec-lease-id-ep-kieu-yaml` của một phiên khác khai upstream không còn trên máy chủ. Phiên soạn r10 KHÔNG sửa
  cấu hình nhánh của phiên khác; thay vào đó đo trên một clone sạch trong rig r10 (`git clone --no-checkout
  --reference`, origin là GitHub, 10:46:50Z; phép so hai nguồn ref 457/457 ở gạch đầu dòng trên):
  `.claude/dev/launcher_test.py` ⇒ rc=0, `NGƯỜI_GIỮ 0: không có` (10:46:54Z; `ci-g5-cong-cu-chia-manh-r1-g1-claude`,
  `-g2-`, `-g3-` đều `HẾT_HẠN`); `.claude/dev/launcher.py` ⇒ rc=0, `NGƯỜI_GIỮ 0` (10:47:06Z). Tệp lease g3 trên
  `86b23c0`: `lease_expires_at_utc: '2026-09-30T09:55:00Z'` (thu hồi bằng rút hạn). Clone sạch chỉ có nhánh cục bộ
  `master`; hai commit chỉ có ở kho chính, không có trên máy chủ (`git log --branches --not --remotes`: `468c88e`,
  `5f7485c`) chỉ chạm `ops/specs/launcher-con-song-esrch-r8.md`, `-r9.md` — không tệp lease nào. Số lease của r3: §8
  của r9.
- **Đường thực thi `launcher_test.py` trong CI** (r10, AST và YAML trên `423b4ba`; các lượt đo r1–r9 trên `89fc4fa`:
  §8 của r9 — cùng kết luận):
  - `ci_dang_ky_test.py`: `MOI` = dict ở `:37–53`, **9 mục**, KHÔNG có `launcher_test.py`; `DA_NOI` = set ở `:69–78`,
    **13 mục**, có `launcher_test.py`. `kiem()` (`:578–612`) chỉ đòi mỗi mục `DA_NOI` có một dòng `run:` nhắc tới nó
    trong workflow — "đã nối", **không** "được `gate-registry` chạy". `chay_moi` (`:962–1037`) mặc định `moi=MOI`;
    `--chay` khai ở `:2176`, nhánh `if ns.chay` ở `:2208` (trên `89fc4fa`: `:2011`, `:2043`). Vậy **`gate-registry`
    chạy 9 bộ, 0 lượt gọi `launcher_test.py`**.
  - `ci.yml`: bảy job (`chuan-bi`, `gate`, `gate-cong-cu`, `gate-cong-cu-gop`, `gate-ops`, `gate-registry`,
    `gate-packet-loop`; hai job `gate-cong-cu*` do #668 thêm), khai `python-version: "3.12"`; không bước `run:` nào
    của job nào nhắc `launcher_test` hay `launcher.py`.
  - `launcher-windows.yml` (không đổi so với `89fc4fa`): `:64` chọn Python 3.13 cho Windows, 3.11 cho Ubuntu; dòng
    nhắc `launcher_test.py` ở `:104` (suite), `:107` (`--dot-bien`), `:206` (probe `t62`). Job `launcher`: PR chỉ chạy
    khi có nhãn `windows`; push master chạm `paths: .claude/dev/**` thì chạy cả Windows lẫn Ubuntu; gọi tay
    `workflow_dispatch` tuỳ `runner_set`. Theo Q4 hai đường đầu không xảy ra trên PR này.
- Suite `launcher_test.py` trên nền: số của r7 đến r9 (nền `89fc4fa`/`c16bec6`, 3.12.3, `187/188 … (tong 189, bo qua
  1, hong 1)`, hỏng duy nhất `r351_KHONG_co_chi_thi_thi_van_phai_dat_moc`, đỏ sẵn): §8 của r9 và bảng 11 dòng 8. r10
  trên `423b4ba` (bảng 12 dòng 12): `python3.11` ⇒ `188/188 … (tong 189, bo qua 1, hong 0)`, rc=0; `python3.12` ⇒
  `187/188 … (tong 189, bo qua 1, hong 1)`, rc=1, hỏng `r351` — **nền khác nhau theo bản Python**, nên delta chỉ so
  trong CÙNG một bản. B6 vẫn bắt executor đo cả hai vế trên nền tiếp nối, ở cả hai bản Python.
- Ruff nền trên `423b4ba` (10:47:54Z 30-09, nhị phân `ruff` 0.15.8; `python -m ruff` vắng), có và không có
  `--target-version py311` như nhau: `launcher.py` 0 lỗi F, `launcher_test.py` 5 lỗi F (F841 ×5). Chi tiết ở B6. Số
  trên `89fc4fa` (r3, r9): cùng 0 / 5.
- Tìm Issue/PR có sẵn cho `ProcessLookupError` / `_con_song` ⇒ 0 kết quả (phép đo của r1; r2 đến r10 KHÔNG đo lại).
  Tìm Issue cho quan sát `comm` không phải UTF-8 (§2): chưa làm.

Mọi con số phải được **đo lại** trước cấp lease và trước land (L5).

## 9. `hinh_dang_ke_thua`

`khong_ap_dung`: không phải packet khắc phục một lượt thất bại. Hình dạng đáng canh, ghi để lượt thi
hành không lặp: *"vá một lỗ mà mở lỗ khác trong cùng hàm"* / *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"* — năm lần trước khi r5 được review; lượt 5 đo lần thứ **sáu**, và r6 là revision đầu tiên ĐỔI CÁCH LÀM thay
vì vá tiếp: liệt kê toàn không gian trước; lượt 6 đo lần thứ **bảy** — chính phép liệt kê của r6 đã bỏ sót nhánh cũ
— và r7 mở rộng phép liệt kê sang MỌI đường; lượt 7 đo lần thứ **tám** — seam thay cả lời gọi; lượt 8 đo lần thứ
**chín** — chính các bản vá r8; lượt 9 đo lần thứ **mười** — chính các bản vá r9; lượt 10 đo lần thứ **mười một**;
lượt 11 đo lần thứ **mười hai** — ở chính chốt tĩnh của r11; lượt 12 đo lần thứ **mười ba** — ở chính phép đo răng của
chốt tĩnh r12; lượt 13 đo lần thứ **mười bốn** — ở chính lời khai mà r13 viết để đóng lớp; lượt 14 đo lần thứ **mười
lăm** — ở chính các câu r14 viết khi tự liệt kê lời khai. Các mục là lịch sử của cùng một lớp, không phải mười lăm
finding độc lập:
1–7. (lượt 0 đến lượt 6) nguyên văn ở §9 của r6 (mục 1–6) và của r7 (mục 7), sha256 `fadad3c7…3c99` và
   `3fc04fe5…5286`. Mỗi lần một dòng: (1) bản RỘNG; (2) bản HẸP r1 mất zombie; (3) ba đường không chốt của r2; (4) ba
   ô tầng đọc của r3 và lời khai "A1 khoá mặc định"; (5) chiều kết quả của PID dự phòng; (6) nhóm phân tích ở tầng
   hỏi; (7) bảng không gian r6 chỉ là tầng của ĐƯỜNG MỚI — r7 chữa bằng không gian từ ĐƯỜNG (30 ô, 129 hạng mục) và
   khai giới hạn cứng: sàn đột biến Windows (B4: biên 42 → 7 → 4).
8. **(lượt 7, mới ở r8 — lần thứ TÁM)** nguyên văn ở §9 mục 8 của r8 (sha256 `2ae6ee04…2aa3`). Tóm tắt: seam thay CẢ
   lời gọi đo mệnh đề bắt, không đo phép đọc, nên tham số giải mã nằm ngoài mọi trục; r8 thêm hai đầu vào nội dung
   thật, điều kiện dựng, loại (2) mở rộng cho seam chỉ-đếm, luật nguồn thêm số lần.
9. **(lượt 8, mới ở r9 — lần thứ CHÍN)** Ba bản vá của r8 cùng ĐÚNG ở chỗ được chỉ và cùng mở một đường chưa ai chỉ:
   (i) loại (2) mở rộng cấp tín dụng giả cho lỗi đối số ((j1) `LookupError`); (ii) luật vị trí `B2-parse` thêm số lần
   vẫn thua một phép giả chạy lại CHÍNH dòng đã khai (fp6b) và một phép giả gọi lại hàm trợ giúp (c3) — lần thứ ba
   của cùng luật; (iii) mệnh đề "`read_text()` không đối số" viết ra để khoá cách đọc của nền đã KHOÁ luôn lỗi 124 mà
   chủ kho quyết sửa. r9 chữa theo lớp và THU HẸP thay vì phình: bỏ hẳn luật vị trí (payload theo dõi, nhận bằng danh
   tính), bỏ hẳn phần mở rộng của loại (2), và đổi trục giải mã từ "giữ như nền" sang danh sách cho phép đóng (Q-A.7)
   khoá bằng `read args` cộng hành vi. Chính r9 cũng có dấu hiệu của hình dạng này: `read args` đặt ngay sau đếm đọc
   che răng hành vi của hai đầu vào nội dung thật (M4, M5 chết sớm ở `read args`), nên r9 thêm hai biến thể "đúng đối
   số, sai hành vi" để hai đầu vào ấy có răng riêng — đo được, không suy (bảng 11).
10. **(lượt 9, mới ở r10 — lần thứ MƯỜI)** Hai bản vá của r9 cùng ĐÚNG ở chỗ được chỉ và cùng mở một đường chưa ai
   chỉ: (i) Q-A.7 mở dạng bytes và KHAI "khoá giữ định dạng" mà không tiêu chí nào đỏ được — mọi phép so khoá dùng
   khoá do CHÍNH ứng viên sinh; (ii) danh sách ĐÓNG của (E) biến câu r8 "số có thể khác nếu cấu trúc khác" và nhân
   chứng viết cho MỘT cấu trúc thành mâu thuẫn. r10 chữa bằng một thước đo ĐỘC LẬP với ứng viên (khoá đọc bytes theo
   định dạng nền) và bằng định nghĩa đối chứng không phụ thuộc cấu trúc, rồi tự rà các đường kế bên: mọi chỗ dựng
   khoá và cả ba tổ hợp lệch, mọi tên gắn cấu trúc trong danh sách đóng, mọi lệnh `python` trần. Cả ba lớp P2 của
   lượt 9 nằm ở HỢP ĐỒNG BẰNG CHỨNG, không ở ngữ nghĩa của `_con_song` (VERDICT lượt 9, HƯỚNG 7: ngữ nghĩa đúng ở mọi
   nơi gọi).
11. **(lượt 10, mới ở r11 — lần thứ MƯỜI MỘT)** r9 mở ba hàm ngoài vào phạm vi, r10 thêm trục định dạng khoá, và
   hai trục còn lại của chính các chỗ đọc ấy — cú pháp phép tách và API đọc — không có ô; bản vá hạn sống của r10 thì
   biến "không giết" thành xanh. Chủ kho chọn áp HINT và lặp tiếp (§11.2). r11 áp HINT rồi TỰ LIỆT KÊ đường vào của
   hai trục ở CẢ năm chỗ đọc trước khi vá, và tìm được bốn đường HINT không phủ, mỗi đường đo được: API ở hai khối đọc
   của `_con_song` (không ô, không tên (E) — thước đo của HINT có bắt `g_d0_open` ở B8 dù HINT chỉ khai ba hàm ngoài,
   đo; `g_d_open` thì B8 không chạm, chỉ helper bắt);
   đường `/proc/<pid>/task/…` mà bộ lọc đường của HINT không thấy; tiến trình con (fd ống) mà bộ lọc bỏ qua vì là fd
   số; và phần còn lại của ba hàm ngoài (phạm vi bắt, số lần đọc, fd mở trước) mà không trục động nào đo. Hai đường đầu đóng bằng động, hai đường sau bằng MỘT chốt tĩnh — ở đó hành vi đúng là hành vi nền nên phép so
   dòng đo đúng lời hứa. Với hạn sống: bốn đường "không bị giết mà trông như đã chết" (con, cháu, mẹ tự thoát; mẹ còn
   sống), mỗi đường một chốt và một đột biến rig. Chính phiên soạn r11 cũng suýt ghi một lời khai rộng hơn phép đo:
   thấy đường `.pyc` trong log của thước đo `open` thì suy ra "bản nháp đầu đỏ oan ứng viên bytes đúng" và viết vào
   đặc tả; phép đối chiếu dựng ngay sau đó cho `cand_b` QUA (bảng 13) — lời khai bị gỡ trước khi đóng băng, bộ lọc giữ
   lại và được ghi đúng là PHÒNG XA, kèm cái giá của nó (`SL2_khoa`).
12. **(lượt 11, mới ở r12 — lần thứ MƯỜI HAI)** `ma-tran-loi-thieu-chot` đóng, nhưng cơ chế MỚI mà r11 dùng để đóng nó —
   chốt tĩnh theo dòng — có biên ở đúng chỗ không ai chỉ: ngoài vùng `def` đến `end_lineno` (decorator, gán lại tên) và
   ngay trong lời văn (so ký tự). HINT lượt 11 vá đúng hai chỗ được chỉ; đo bằng chính script của reviewer, luật ấy vẫn
   để lọt 37 trên 44 đường vào mà r12 tự liệt kê (§7 B2). r12 đổi cách làm thay vì vá tiếp: đóng theo điều ĐƯỢC PHÉP
   trên toàn `launcher.py` (luật `H`, `K`, `M`, `T1`–`T7`), MỘT script làm hiện thực, mỗi luật một đối chứng dựng từ
   chính ứng viên, và đo răng từng đối chứng bằng đột biến chính script — phép đo ấy lộ ngay một nhánh không có đối
   chứng riêng (phần `M`), sửa trước khi đóng băng. Lớp `khai-khong-do-duoc-ma-do-duoc` cũng đổi từ quét tay sang phép
   kiểm bằng máy (§10), và phép `grep` theo dòng mà HINT đề nghị tự nó mù với nhãn gãy dòng (41 so 37, bảng 14).
13. **(lượt 12, mới ở r13 — lần thứ MƯỜI BA)** Phép đo răng của r12 lộ MỘT nhánh không đối chứng (phần `M`) và r12 vá
   đúng nhánh ấy; lượt 12 đo thêm ba nhánh (đếm `def` của bốn hàm, `T5` cho chỉ số, `T7` cho `def` mới) và bốn đường
   gián tiếp mà `T3`, `T6` không xét. r13 TỰ LIỆT KÊ trước khi sửa — 14 chỗ ghi lỗi của script, năm chỗ không đối chứng
   nào dựa vào, tức thêm hai chỗ reviewer chưa chỉ (bảng 15 dòng 7) — và vì thế KHÔNG vá theo danh sách ba nhánh: THU
   HẸP lời khai về đúng phạm vi đo được ("mỗi LUẬT một đối chứng"; chốt tĩnh khép cách viết TRỰC TIẾP, không phải hộp
   cát), không đổi script. Cùng lượt, lớp mới `kich-thuoc-thi-hanh-vuot-adr-0044` lặp hình dạng ở một tầng khác: cận
   dưới "≥ 484, chưa kể helper" đi vào câu hỏi gửi chủ kho và một quyết định THẨM QUYỀN (trần 600) dựng trên nó; đo
   đủ phần thì ra 1333 và quyết định phải làm lại (§4).
14. **(lượt 13, mới ở r14 — lần thứ MƯỜI BỐN)** r13 sửa đúng ba chỗ nhãn mà lượt 12 chỉ, trong khi chính luật `T3` của
   r12 đã làm sai một nhãn KHÁC không ai chỉ (mục 5 bảng bất khả thi, trục C); và mục kích thước mà r13 viết để đóng một
   lớp P2 tự khai rộng hơn đo (tái lập, số hạng). HINT lượt 13 sửa đúng các chỗ nó chỉ; chính các dòng nó viết có năm
   chỗ lệch so với đo hay với nguồn, và nó để nguyên hai lời khai rộng hơn đo của r13 (bảng "Thay đổi so với r13",
   đầu r14). r14 không vá theo danh sách ấy: TỰ LIỆT KÊ mọi lời khai của §4 và mọi chỗ
   mang lời khai "lớp con cụ thể không đo được" — thêm ba chỗ HINT không chạm (mục 9, §10 lý do 4, §10 "Răng của bộ
   sinh") — rồi ĐO thay vì chép số: dựng lại ứng viên tham chiếu đúng byte, đo các phép r13 để CHƯA ĐO, đo mục 5 trên
   ứng viên thứ hai (bảng 16). Không thêm luật, ca hay dòng `DOT_BIEN`.
15. **(lượt 14, mới ở r15 — lần thứ MƯỜI LĂM)** Các chỗ lượt 13 chỉ đều ĐÃ ĐÓNG (VERDICT lượt 14), nhưng chính các câu
   r14 viết trong phép tự liệt kê lệch đo ở ba chỗ: §10 "Răng của bộ sinh" rộng hơn đo (năm lớp con TRONG danh sách
   `T3` thì `T3` cho qua — đo trên `PermissionError` ở Đ và Đ0: chốt tĩnh ĐẠT, ca động ĐỎ), B2 mục 5 gạch 1 hẹp hơn đo
   (tên ngoài tập nêu dạng thuộc tính ĐỎ ở `T6`, không ở `T3`), và bảng 16 dòng 13 — dòng r14 thêm để đo lại §4 — ghi số DÒNG thành số LẦN. Đúng hình dạng r14 tự chỉ
   ra ở HINT lượt 13 ("rộng hơn đo"), viết lại ở chỗ khác. r15 sửa đúng ba câu theo HINT lượt 14, tự rà toàn tệp các
   câu cùng lớp (bảng "Thay đổi so với r14"); không đổi script, luật, ca, phép đo hay dòng `DOT_BIEN`.

Mỗi bản vá/đặc tả đều ĐÚNG và CÓ RĂNG ở chỗ nó phủ; lỗ nằm ở đường KHÔNG ai chỉ. Các phép đo chỉ chứng
minh các đường đã thử. Miền kiểm của r12 (r13 đến r16 không đổi) gồm ESRCH, EACCES, EPERM, EIO, zombie, ngoại lệ ngoài `OSError`
(`Exception` và `BaseException`) ở cả năm tầng hỏi, đọc mới, kill mới, đọc cũ, kill cũ, nhóm phân tích ở cả năm
tầng (tự nhiên ở hai tầng đọc, sentinel ở tầng hỏi và hai tầng kill), số lần hỏi/đọc/kill theo từng đường, cú
pháp phép tách (`)` đầu và khoảng trắng) với `comm` chứa `)` ở cả năm chỗ đọc (r11: thêm ba hàm ngoài), nội dung THẬT có `comm` không phải UTF-8 ở cả hai tầng đọc,
dạng phép đọc ở cả năm chỗ đọc (r9), API đọc ở cả năm chỗ đọc (r11), phần còn lại của ba hàm ngoài và của `launcher.py` theo AST với nền, cùng danh sách cho phép cho `_con_song` và hàm trợ giúp mới (r12; r11 so dòng), định dạng khoá danh tính ở cả hai chỗ dựng khoá và hai dạng (r10, r11), khung ca B8 không nhận "tự thoát" là "bị giết" (r11), và **kết quả của bước PID dự phòng (sống, đã `wait`, EPERM, EIO) cùng số lần
gọi `kill(pid, 0)`**; bảng không gian mở rộng ở B2 ghi rõ ô, đầu vào và chốt từng hướng. B2 khoá bản RỘNG và các
biến thể tầng đọc, B3/B3b khoá bản HẸP r1, B8 khoá lỗi 124 do giải mã; các lớp còn lại ở B5 và (E) khoá những biến
thể đã liệt kê. **Không coi một danh sách mutant hữu hạn là bằng chứng đã liệt kê hết mọi đường**; executor và
reviewer vẫn phải kiểm các đường mới xuất hiện trong chính cách triển khai được chọn.

**Ngưỡng ba lần đã chạm — câu hỏi đặt cho điều phối/chủ kho, r4 đến r10 KHÔNG tự trả lời.** CLAUDE.md dạy đếm
hình dạng lỗi chứ không chỉ đếm lỗi: cùng một hình dạng lặp từ ba lần trở lên thì câu hỏi đúng là "có nên
làm việc này theo cách này không", không phải "vá thế nào". Đường hiện tại (giữ phép hỏi `exists()` rồi
dựng thêm một đường lỗi có đọc + `kill(pid, 0)`, Q-A.1–4) tự nó sinh ra nhiều đường cần chốt — số dòng biến thể của
B5: bảy ở r2, mười hai ở r3, mười lăm ở r4, mười chín ở r5, bốn mươi chín ở r6, năm mươi tư từ r7 (cộng 89 biến thể
(E) ở r7, 95 ở r8, 109 ở r9, 110 ở r10, 118 ở r11 đến r16); số đơn vị assertion: 22 ở r4, 26 ở r5, 36 ở r6, 55 ở r7, 57 ở r8 đến r16. Bước nhảy
19 → 49 của r6 là giá của việc liệt kê đủ không gian thay vì vá theo finding; với một hàm dài 44 dòng trên nền
(dòng 629–672, kể cả docstring; §8), nghiệm thu nay cần 134 hạng mục, và sàn đột biến Windows chặn cứng việc đưa
chúng vào `DOT_BIEN` (B4) — nên phần lớn răng (83 hạng mục (E) và bốn ca B8) chỉ đo được MỘT lần. Có thể cân nhắc
một cấu trúc ít đường hơn (ví dụ dùng chính phép đọc làm phép hỏi), nhưng nó đổi hành vi nhánh cũ mà Q-A.3 cấm
đổi, và r4 đến r10 chưa đo phương án nào. Dữ kiện mới: lần thứ chín và thứ mười đều do chính các bản vá của lượt
trước sinh ra; r9 THU HẸP (bỏ hai luật) và r10 thêm một thước đo độc lập thay vì thêm luật; lần thứ mười một nằm ở
ba hàm ngoài mà r9 mở và ở khung ca của r10; lần thứ mười hai nằm ở chốt tĩnh của r11, và r12 thay nó bằng danh sách
cho phép thay vì vá thêm luật; lần thứ mười ba nằm ở phép đo răng của chính chốt r12, và r13 THU HẸP lời khai thay vì
thêm đối chứng theo danh sách của reviewer; lần thứ mười bốn nằm ở chính lời khai của r13 và của HINT lượt 13, và r14
tự liệt kê rồi đo từng lời khai thay vì sửa theo danh sách được chỉ; lần thứ mười lăm nằm ở chính các câu r14 viết
trong phép tự liệt kê ấy, và r15 chỉ sửa câu chữ theo phép đo của lượt 14. Có hỏi lại quyết định gốc hay không là việc của điều phối/chủ kho — lượt
này chủ kho chọn lặp tiếp, kèm điểm dừng (§11.2).

## 10. `chua_do_duoc`

Lịch sử theo từng revision của mục này: §10 của r10 (sha256 `e3ae8741…4bde16`), r9 (sha256 `1a629c89…a3cf`) và r8
(sha256 `2ae6ee04…2aa3`) — không chép lại. Dưới đây là các giới hạn HIỆN HÀNH.

**(r12, THU HẸP lớp `khai-khong-do-duoc-ma-do-duoc`, tái phát từ lượt 7 đến lượt 11) Nhãn `KHÔNG ĐO ĐƯỢC` chỉ đi với
MỘT lý do trong danh sách ĐÓNG, ghi ngay sau nhãn dạng "(lý do N)":** (1) cần mạng hay GitHub mà phiên không có, hay
công cụ bắt buộc không cài được vì thiếu mạng; (2) cần Windows (hay nền khác) thật trước merge — Q4; (3) không có neo
hay dữ liệu gốc để đo (lời điều phối không có neo GitHub, họ model tự khai); (4) bất khả thi theo định nghĩa — tập mở
(errno của `OSError` là số nguyên tuỳ ý, lớp con tuỳ ý — (r14) trừ lớp nêu TRỰC TIẾP trong `_con_song` và `def` mới,
nay là tập ĐÓNG nhờ `T3`, `T6`: B2 mục 5), tần suất ngoài thực tế, xác suất tái dùng PID, "không bao giờ"
trên đầu vào mở, và (r13) một dòng đột biến không có vị trí mã tương ứng ở cách triển khai đã chọn (B5; nêu vị trí
thiếu); (5) chỉ đo được bằng một thao tác bị cấm (sửa ref hay cấu hình của phiên khác; ghi lên GitHub khi chỉ
thị cấm). Lý do kiểu "chưa làm", "chưa thử", "chưa dựng", "không so", "chưa ai …" là **CHƯA ĐO**. HINT lượt 11 đề nghị
bốn lý do đầu; r12 thêm (5) cho phía GHI của kênh GitHub (r12 dùng nó cả cho kết quả `ai-dang-giu` ở kho chính; r13
bỏ — kết quả ấy ĐÃ đo, gạch đầu dòng "Lease và ref" dưới đây). Nhãn TRÍCH từ revision hay lượt cũ đứng ngay sau dấu nháy
kép; nhãn NHẮC như một tên (định nghĩa, luật, hạng của một phép đo) đứng trong backtick. (r13) TÊN HẠNG
của một phép đo đã chạy không phải nhãn trạng thái của đặc tả và không mang lý do của danh sách này: hạng của phép A/W
(B5) nay mang tên riêng `CHƯA CÓ CHỐT NGƯỢC` (r12 đặt trùng tên nhãn — cross-review lượt 12); hạng `KHONG DO DUOC` mà
runner `--dot-bien` của nền in ra là chuỗi của mã nền, giữ nguyên. **Kiểm lúc đóng băng bằng máy
— `grep -n` theo dòng như HINT đề nghị là KHÔNG đủ:** nó bỏ sót nhãn bị ngắt dòng (đo trên bản chỉ-HINT lượt 11:
`grep -o` đếm 37, văn bản gộp khoảng trắng có 41 — bốn nhãn gãy qua hai dòng; bảng 14). Tập lệnh dưới gộp mọi khoảng
trắng rồi đòi mỗi nhãn ở một trong ba dạng; rc=1 kèm từng chỗ sai. Máy kiểm HÌNH THỨC (nhãn có lý do trong danh sách);
lý do có đúng không vẫn là việc người đọc — nhưng người đọc nay chỉ đọc các chỗ `(lý do N)`, không quét cả tệp.

```python
# kiem_nhan_r12.py - moi nhan `KHÔNG ĐO ĐƯỢC` trong dac ta (ke ca bi ngat dong) phai o MOT trong ba dang:
# (i) ngay sau nhan (sau dau ** neu co) la " (lý do N" voi N trong danh sach DONG 1..5 cua §10;
# (ii) ngay truoc nhan la dau nhay kep: TRICH nhan cua mot revision hay luot cu;
# (iii) ngay truoc nhan la dau backtick: NHAC ten nhan (dinh nghia, luat, hang cua mot phep do).
import sys
t = " ".join(open(sys.argv[1], encoding="utf-8").read().split())
N = "KHÔNG ĐO ĐƯỢC"
i, sai, dem = t.find(N), [], 0
while i >= 0:
    dem += 1
    sau = t[i + len(N):].lstrip("*")
    co_ly_do = sau.startswith(" (lý do ") and sau[8:9] in ("1", "2", "3", "4", "5")
    if not (co_ly_do or t[i - 1:i] in (chr(34), chr(96))):
        sai.append(t[max(0, i - 70):i + len(N) + 25])
    i = t.find(N, i + 1)
print("nhan:", dem, "| sai dang:", len(sai))
for s in sai:
    print("   ", s)
sys.exit(1 if sai else 0)
```

Đo (bảng 14): bản chỉ-HINT lượt 11 — 41 nhãn, 28 sai dạng, rc=1; r12 lúc đóng băng — số ở bảng 14, 0 sai dạng, rc=0;
đối chứng trên bản sao r12: xoá một "(lý do 4)" ⇒ rc=1 đúng một chỗ; thêm một nhãn không lý do gãy qua hai dòng ⇒ rc=1
đúng chỗ ấy. Hai nhãn lượt 11 chỉ ra được ĐO chứ không chỉ đổi nhãn: nới tuần tự (B5, "Chốt ngược") và so comment
VERDICT với tệp VERDICT (gạch đầu dòng "Dữ kiện do điều phối cấp" dưới đây).

- **Mọi số đo của đặc tả là số trên bản NHÁP của phiên soạn hay reviewer, không phải mã của executor.** CHƯA ĐO trên
  ứng viên của executor: năm mươi tư dòng B5 (năm mươi lăm cặp), 118 dòng (E) (cộng hai dòng `DS-E-C3` nếu áp
  dụng), phép D và 65 control, bốn ca B8, suite hai vế ở `python3.11` và `python3.12`, `--dot-bien`, ruff delta,
  tập lệnh bằng chứng, `chot_tinh_r12.py` trên ứng viên, và tiểu nhãn/loại trong thông điệp giết theo ĐÚNG chuỗi của đặc tả.
  Helper của r6 đến r11 là helper của phiên soạn (r9: chép helper reviewer lượt 8 rồi cài `read args`; r10, r11: chép
  helper r9, sha256 `635d93fa…0494`, r11 tách lại từ tệp thử của rig r10 và dựng lại đúng từng byte; r12 chép tệp thử
  của rig r11, `c4267574…7905` và `6f07a7cf…3ed8`, chứa helper ấy — dùng cho phép nới tuần tự và `cs_subprocess`), không phải
  của executor; hợp đồng helper ở §7 là lời văn. Mặc định "không
  nới" của helper phải đo riêng bằng D; A1 có chốt phủ giao nhau nên không chứng minh được điều này một mình.
- Số của các rig r5 đến r14 chỉ có trong rig tạm của từng phiên soạn (thư mục `mktemp -d` trong scratchpad, ngoài
  kho) — **KHÔNG tái lập được từ kho**; dựng lại từ đặc tả là đủ. Rig r9: bảng 11. Rig r10: bảng 12. Rig r11: bảng 13
  (bản nháp `launcher.py` chép từ rig cross-review lượt 10, kiểm bằng diff; phiên soạn r11 dựng thêm các bản mới; helper
  chép rig r9 qua rig r10; khối B8 trích từ chính tệp r11). ĐO LẠI ở r11: bốn ca B8 trên các bản của bảng 13, các ca
  chậm của khung ca, helper trên các biến thể `_con_song`, locale, điều kiện dựng hỏng, B4, B6 hai vế ở hai Python,
  ruff, chốt tĩnh. KHÔNG chạy lại ở r10, r11 (số hiện hành là của r9, bảng 11): A/W của 54 dòng B5, phép D và 65
  control, phần lớn 110 tên (E) cũ (r11 chạy lại những tên có đích B8 và các tên `_con_song` của bảng 13),
  `--dot-bien` hai vế. Rig r12: bảng 14 (bản nháp `launcher.py` đọc từ rig cross-review lượt 11 và rig r11, không sửa;
  phiên soạn r12 dựng thêm 45 bản đường vào, hai đột biến (a), (b) và 15 đột biến của chính script chốt). ĐO LẠI ở r12:
  chốt tĩnh r12 trên 141 bản ở hai Python, nới tuần tự trên helper ở ba Python, bốn ca B8 với khối r12 trên nền và
  `cand_a` (3.12), REST, nền. KHÔNG chạy lại ở r12 (số hiện hành của bảng 13): B6 hai vế, ruff, locale, kernel, B4, ca
  chậm của khung ca, phần còn lại của bốn ca B8 trên các biến thể, helper trên các biến thể `_con_song` ngoài
  `cs_subprocess`; và của bảng 11: A/W, D, phần lớn (E). Rig r13: bảng 15. Rig r14: bảng 16 — ứng viên tham chiếu r13
  dựng lại đúng byte; ĐO LẠI ở r14 trên ứng viên ấy: A/W 55 cặp, phép D và 65 control, `--dot-bien` (`python3.11` và
  `python3.12`); sáu ca mới (`python3.12`); chốt tĩnh (`python3.11`) và bảy biến thể mục 5 B2 (chốt tĩnh `python3.11`,
  bốn ca `python3.12`). Cho ứng viên tham chiếu, số hiện hành của A/W và D là bảng 16, không còn là bảng 11.
- **Nhánh Windows và Darwin: không đo** (Q4); lần đo Windows đầu tiên là lượt push master sau merge. **Sàn đột biến
  Windows (B4): số THẬT KHÔNG ĐO ĐƯỢC (lý do 2) trước merge**; số hiện hành là ước lượng tĩnh cận dưới của r7 (biên 4), không
  đổi vì `DOT_BIEN` không đổi — suy ra, không đo lại ở r8 đến r10 (phép tính biên bằng `_dot_bien_du_san` của
  `423b4ba` ở B4 là số học trên số đếm, không phải lượt `--dot-bien` trên Windows). Cross-review mô phỏng Darwin/Windows
  bằng seam hay `platform.system` giả (ca trả chuỗi BỎ QUA, không tính là QUA) ở lượt 1 đến 5 và lượt 8 đến 14, theo
  VERDICT; lượt 6 chỉ mô phỏng nhánh Windows của `_con_song`; lượt 7 và lượt 15 không mô phỏng. Đó là mô phỏng nhánh,
  KHÔNG phải hệ điều hành thật, và không thay `land_obligation`. (r16 sửa, cùng lớp với B7 dưới đây: r4 đến r8 chỉ kể
  lượt 3, r9 đến r15 kể lượt 3 và lượt 8 — thiếu so với VERDICT.) Bảng 11 đo ba
  Python ở dòng 1–5; dòng 6–10 chỉ ở 3.12.3 hay không phụ thuộc Python. Bảng 12: số Python ghi ở từng dòng.
- **Kernel thật.** ESRCH thật trên `/proc/<pid>/stat` chỉ thấy một lần ở CI (job `109303373142`); EACCES/EIO/EPERM ở
  `stat` hay phép đọc của PID sống, sentinel ở mọi tầng, nhóm phân tích ở tầng hỏi và kill, ENOENT ở `stat` của PID
  sống, lỗi của `kill(pid, 0)` — tất cả là đầu vào do seam đặt ra. Việc hệ điều hành thật sinh chúng: r10 ghi
  "KHÔNG ĐO ĐƯỢC"; **r11 đo ở cấu hình của container** (bảng 13): dưới uid 65534, `/proc` gắn `rw,relatime` (không
  `hidepid`), `stat` và đọc `/proc/<pid>/stat` THÀNH CÔNG ở mọi PID (2341–2344, ba Python), `kill(pid, 0)` chỉ ra EPERM
  hay ESRCH, 0 EACCES — tức ở cấu hình này kernel KHÔNG sinh các lỗi ấy; cấu hình khác (`hidepid`, LSM): CHƯA ĐO
  (chưa dựng). Dùng `stat`, phép đọc và `kill` THẬT: `vang-da-wait`, lời gọi đường cũ của `B3-zombie`, hai đầu vào
  nội dung thật và bốn ca B8. Tần suất `comm` không phải UTF-8 ngoài thực tế: KHÔNG ĐO ĐƯỢC (lý do 4).
- **Giải mã.** Hai đầu vào nội dung thật và B8 chỉ đo MỘT dạng `comm` không giải mã được (UTF-8 bị cắt giữa ký tự,
  15 byte); điều kiện dựng đo được ở UTF-8 mode và locale ASCII (bảng 10 dòng 7); locale giải mã được 15 byte ấy
  (ISO-8859-1): ĐO ĐƯỢC bằng `localedef` vào `LOCPATH` riêng (cross-review lượt 9; bảng 12 — r9 ghi "KHÔNG ĐO ĐƯỢC" là
  sai). **(r11, lớp `khai-khong-do-duoc-ma-do-duoc`, TÁI PHÁT ở hai lời khai của r10 — sửa bằng phép đo của chính
  phiên soạn r11, bảng 13.)** "Không cần root": ĐO ĐƯỢC — `setpriv --reuid 65534 --regid 65534 --clear-groups` chạy
  `localedef -i en_US -f ISO-8859-1` vào thư mục đích 0777 truyền bằng fd đã mở (`/proc/self/fd/7/…`; đọc thẳng đường
  dẫn thì bị chặn vì thư mục cha 0700 — đo, cùng lượt) ⇒ `uid` trong tiến trình 65534, rc=0, tệp thuộc `nobody`; locale
  ấy cho `ISO-8859-1` và giải mã được 15 byte ở ba Python. r10 ghi "KHÔNG ĐO ĐƯỢC" là sai: bị chặn ở ĐƯỜNG DẪN, không ở
  năng lực. Locale giải mã được mà KHÔNG phải ISO-8859-1: ĐO ĐƯỢC — `localedef -i ru_RU -f KOI8-R`, `-f CP1251`, `-f
  ISO-8859-5` đều rc=0; `getpreferredencoding(False)` ra đúng tên ấy và cả ba giải mã được 15 byte ở ba Python; B8
  trong bốn locale giải mã được (ISO-8859-1 dựng bằng uid 65534, KOI8-R, CP1251, ISO-8859-5): `t158`, `t159` BỎ QUA
  có khai, `t160`, `t161` như ISO-8859-1 của bảng 12 dòng 6 (bảng 13). r10 ghi "KHÔNG ĐO ĐƯỢC (không dựng)" là sai:
  chưa dựng không phải không đo được. Đối số giải mã: ĐO ĐƯỢC bằng seam ghi
  đối số (lượt 8; r8 khai "KHÔNG ĐO ĐƯỢC" từ tiền đề sai), khoá bằng `read args` (bảng 11). `cp1252` đo được là không
  bền (lượt 8); bộ giải mã khác không cần đo vì Q-A.7 chỉ nhận hai dạng. `newline`: suy luận, không đo. Ứng viên dạng
  BYTES: bốn ca B8 đo được (lượt 9, bảng 12 và bảng 13, ba Python: QUA ×4); qua helper `t156`/`t157`: helper của phiên
  soạn chỉ seam `read_text`, và r11 ĐO rằng nó không phục vụ dạng bytes — ứng viên bytes đúng chết `B2-eacces read
  count 0` ở ba Python (bảng 13; quy ước "Seam thay CẢ lời gọi" đòi seam đúng phương thức của `DANG_DOC_QA7`); qua
  helper seam `read_bytes`: CHƯA ĐO (chưa dựng). Payload `bytes`: cơ chế đo được (lượt 9, ba Python, cùng bảng phân
  hạng với `str`); qua helper đầy đủ: CHƯA ĐO (chưa dựng). `errors="replace"`/`"surrogateescape"` bị loại vì danh sách đóng, không vì hành vi (lượt 8 đo
  chúng đúng hành vi ở locale tương thích ASCII).
- **Nhận diện lỗi phép tách của `B2-parse` (payload theo dõi).** Giới hạn: ứng viên phải tách trên chính payload bằng
  các phép payload phủ; phép khác (biểu thức chính quy, `partition`, chuẩn hoá trước khi tách) làm (l15)/(l17) chết vô
  can — đỏ ồn ào, không tín dụng giả. Đo (lượt 8 và bảng 11, ba Python): tách hai dòng và tách trong hàm trợ giúp có
  (l15), (l17) chấp nhận; fp…fp6b và hai phép giả gọi lại hàm trợ giúp vô can.
- **Răng của bộ sinh chỉ tới ngữ pháp của nó** (bảng 8). Không phủ: kiểm tra dữ liệu thay bắt ngoại lệ ngoài (l16);
  tên lớp con cụ thể của `OSError`/`Exception`/`BaseException` (r15 sửa câu r14 "nêu trực tiếp thì chốt tĩnh `T3`
  bắt" — rộng hơn đo, cross-review lượt 14: tên NGOÀI tập đóng của B2 mục 5 thì chốt tĩnh ĐỎ, `T3` hay `T6`; năm lớp
  con TRONG danh sách `T3` — `PermissionError`, `ProcessLookupError`, `IndexError`, `ValueError`, `UnicodeDecodeError` —
  thì chốt tĩnh cho qua và đầu vào động R1–R3 bắt: chỉ bắt `PermissionError` ở Đ (dòng (d2)) hay ở Đ0 ĐẠT chốt tĩnh
  rc=0, ĐỎ `t156` `B2-doc-hong EIO` / `B2-nhanh-cu EIO`, loại `seam escaped`; hở: `subprocess.SubprocessError` — B2
  mục 5); errno thứ năm trở đi; `finally`; `else` gắn sai; mở
  rộng khối `try` sang câu lệnh khác — mỗi cái CHƯA ĐO bằng bộ sinh (ngoài ngữ pháp của nó; dựng tay được — r11 dựng
  và đo một: kiểm dữ liệu ở nhánh cũ, mục 8 danh sách bất khả thi ở B2). Nhánh cũ, hỏi/đọc lại có điều kiện, cú pháp phép tách,
  tham số của lời gọi đọc, dạng phép đọc và định dạng khoá nằm ngoài ngữ pháp ấy; r7–r10 phủ bằng bảng không gian mở rộng, trục C, S,
  G, hai đầu vào nội dung thật, `read args`, khoá độc lập `_k124_khoa_that` và B8.
- **Răng của phép (E) chỉ tới MỘT biến thể mỗi hạng mục, và chỉ MỘT lần** (83 hạng mục và bốn ca B8; B4, B5): một
  biến thể mỗi hạng mục không chứng minh mọi cách viết vi phạm đều bị bắt. Răng riêng của `B3-song` và `B3-da-wait`
  (không biến thể nào lấy làm đích): CHƯA ĐO (r11 sửa nhãn — dựng được, chưa dựng). Kênh nộp qua GitHub thật: phía đọc
  ĐO ĐƯỢC ở r11 (byte-exact, hai client — B5 (E) mục 3, bảng 13); phía ghi không thử (phiên soạn không đẩy).
- **Dữ kiện do điều phối cấp — (r11) phần lớn nay ĐỌC ĐƯỢC qua REST** (GET, `Authorization: Bearer` bằng
  `GITHUB_PAT`, mã 200 kèm `X-Github-Request-Id` — tới GitHub thật; 15:39:53Z 30-09; bảng 13). r2–r10 ghi cả nhóm là
  "KHÔNG ĐO ĐƯỢC từ phiên soạn"; đúng với đường MCP (chuẩn hoá thân) và với các lượt REST bị proxy chặn đã ghi trong
  CLAUDE.md, không đúng với phiên này. Đọc được: #686 có `id` = `5628902742` (khớp object ID của descriptor), thân
  3243 byte, sha256 `2af24e288730933f43b8e05e00688815fbe3d2a4974a77797b0b6d4354aed9de`, 12 dấu `"` thô và 0 thực thể
  HTML (REST không chuẩn hoá); comment `5888633201` trên #686 (2026-09-29T10:45:55Z, Q5 — §11 mục 4); `5905670017` trên
  PR #688 (06:42:43Z, chứa nguyên văn *"#688: ngay trong packet này"* kèm giờ 06:42:25Z); `5907480436` (lượt 8,
  08:39:42Z), `5909554178` (lượt 9, 10:40:32Z), `5913959273` (lượt 10, 15:03:40Z) trên PR #688 — lúc soạn r11,
  PR #688 có 11 comment.
  **(r12; REST như trên, 22:32:13Z 30-09; bảng 14)** PR #688 có 12 comment — lượt 1 đến lượt 11 cộng comment quyết
  định; lượt 11 là `5920625021` (22:12:07Z). **So comment VERDICT với tệp VERDICT — r11 ghi "không so", HINT lượt 11
  đổi thành CHƯA ĐO; r12 ĐO** trên thân thô của REST (0 thực thể HTML, 0 CR), lượt 10 (`5913959273` với VERDICT lượt 10
  `88538f7c…85f8`) và lượt 11 (`5920625021` với VERDICT lượt 11 `0a7d934c…6f80`): thân comment KHÔNG bằng byte tệp
  VERDICT và không là chuỗi con của nhau (2 718 so 65 404 byte; 3 042 so 42 916 byte) — comment tự khai là "bản chiếu
  của tệp verdict cục bộ", dạng tóm tắt; mọi dữ kiện máy kiểm được trong thân đều khớp tệp: ba sha256 (VERDICT, HINT,
  spec) đúng bytes các tệp và không có sha256 nào khác, reviewed commit đúng, các cặp (slug, hạng) trùng bảng lớp của
  VERDICT (5/5 và 2/2), số P1/P2/P3 trùng dòng `lớp:` của VERDICT, nhãn `changes_requested`, số dòng khai (630 dòng
  VERDICT lượt 10; bản gộp 2442 và 2740 dòng). Nguồn có thẩm quyền vẫn là TỆP có băm, comment là bản chiếu (CLAUDE.md).
  **(r13; REST như trên, đọc lần cuối 00:59:15Z 01-10, `X-Github-Request-Id` có; bảng 15)** PR #688 có 15 comment — thêm
  `5922115123` (00:19:49Z, bản chiếu VERDICT lượt 12), `5922248948` (00:29:51Z, quyết định ≤ 600) và `5922387653`
  (00:42:33Z, quyết định ≤ 1400 thay nó); thân thô của cả ba: 0 thực thể HTML, 0 CR. Bản chiếu `5922115123` so với tệp VERDICT
  lượt 12: tóm tắt, không bằng byte (2117 ký tự); mọi dữ kiện máy kiểm được trong thân đều khớp — reviewed commit
  `417071e…`, sha256 spec, VERDICT, HINT, tiền tố `127a8cb4` của bản gộp, 503 dòng VERDICT (`wc -l`). Hai comment quyết
  định: nguyên văn và sha256 thân ở §4, mục "Ngoại lệ ADR-0044"; cả hai tự khai là do phiên agent đăng hộ bằng
  credential chủ kho, tư cách lời khai có neo — r13 kiểm được nội dung đã đăng, không kiểm được transcript.
  **(r14)** Phiên soạn r14 KHÔNG đọc GitHub (không REST, không MCP): mọi số GitHub trên đây là của r13 trở về trước;
  comment PR #688 sau 00:59:15Z 01-10, kể cả bản chiếu VERDICT lượt 13 nếu có: CHƯA ĐO. Hai comment quyết định được
  đối chiếu lại trên tệp REST mà rig r13 lưu (bảng 16 dòng 13), không phải trên GitHub.
  **(r15)** Phiên soạn r15 cũng KHÔNG đọc GitHub: bản chiếu VERDICT lượt 14 là comment `5925622594` trên PR #688 theo
  lời điều phối — có trên PR hay không, thân khớp tệp VERDICT hay không: CHƯA ĐO.
  **(r16)** Phiên soạn r16 cũng KHÔNG đọc GitHub: bản chiếu VERDICT lượt 15 là comment `5928898872` trên PR #688 theo
  lời điều phối — có trên PR hay không, thân khớp tệp VERDICT hay không: CHƯA ĐO.
  VẪN KHÔNG ĐO ĐƯỢC (lý do 3) từ phiên soạn: ô `quy_uoc_review`, quyết định chủ kho cho r11 và chỉ thị cho r12 đến r16
  (lời điều phối, không có neo GitHub); họ model tự khai của reviewer lượt 6 đến lượt 15. Thân Issue sửa được sau khi băm,
  nên neo vẫn là object ID cộng số Issue; băm trên ghi để đối chiếu.
- **Lease và ref:** r10 ĐO (§8): hai nguồn ref 457/457 trên clone sạch, `NGƯỜI_GIỮ 0` cho cả hai tệp write set. Ở kho
  chính cùng lệnh ra `CHAN [12]` vì một nhánh cục bộ của phiên khác (§8) — đó là kết quả ĐÃ ĐO ở kho chính (công cụ
  tự trả "không xác định", rc=12), không phải nhãn thứ ba của đặc tả; câu "ai đang giữ" được trả lời bằng clone sạch
  ở trên. r12 ghi "(lý do 5)" là sai (cross-review lượt 12): một bản sao kho chính với cấu hình nhánh của CHÍNH bản
  sao không phải thao tác bị cấm.
  Số ấy là của 10:46Z–10:47Z 30-09; r11 đến r16 KHÔNG đo lại; đo lại lúc cấp lease (Q5 điều kiện
  1, §11 mục 4), và đừng suy "người giữ 0" từ một tập ref chưa so hai nguồn.
- **B7 (`t154`)**: chỉ có số của reviewer — các phiên soạn từ r3 không chạy lại. Bản nháp, `t154` cũ: lượt 1 đến lượt
  4 (§7 ghi số của lượt 1 đến 3; lượt 4, hướng 8: nền ném `ProcessLookupError` sau 1 lần chạm seam, 1,211 giây; bản
  dựng theo Q-A r4 qua, 54 lần chạm, 4,938 giây). Ứng viên độc lập, `t154` MỚI của `20ec8d5`: lượt 14 (hướng 10) và
  lượt 15 (hướng 4) cùng kết quả — không seam: nền và ứng viên QUA; seam ENOENT ⇒ ESRCH trên `/proc/<pid>/stat`: nền
  ĐỎ `ProcessLookupError` sau 1 lần chạm, ứng viên QUA, 7 lần chạm. (r9 đến r15 ghi "chỉ có số của reviewer lượt 2
  đến lượt 4" — sót lượt 1, lệch §7, và chưa có lượt 14; r16 sửa, cross-review lượt 15.)
- **Số kỳ vọng sau packet** (§8, B5): 195 ca đăng ký; 228 mục `DOT_BIEN` sản phẩm, 231 kèm `DOT_BIEN_HARNESS`; 17 nhãn,
  48 tiểu nhãn, 57 đơn vị, 65 control. Rig r9 đếm ra 195 ca (bảng 11 dòng 8) và 17 / 48 / 57 / 65 (dòng 5); `DOT_BIEN`
  của rig r9 giữ 174 + 3 (không thêm dòng; `--dot-bien` 176/176). Rig r10: số ca của suite hai vế ở bảng 12. (r13)
  Ứng viên tham chiếu của §4 đếm 195 ca, 228 mục `DOT_BIEN` cộng 3 harness, 17 / 48 / 57 (bảng 15 dòng 4); 65 control và
  việc 54 mục mới giết đúng ca: CHƯA ĐO ở r13. (r14) ĐO trên chính ứng viên ấy (bảng 16 dòng 6–9): 195 ca, 228 + 3
  (nạp module, `python3.12`); ở `python3.11` và `python3.12`: phép D 56 + 1 = 57 đơn vị, 65/65 control đỏ đúng, 6/6
  phép đảo; `--dot-bien` 230/230, 54 mục mới giết đúng ca đích; A/W 55/55 cặp. Ứng viên độc lập của cross-review lượt
  13: §4, "Số đo độc lập". Không phải phép đo trên mã của executor.
- (r10 đến r16) **Kích thước và băm** (của TỆP ĐẶC TẢ; kích thước diff thi hành ở §4). Số dòng và số byte chính xác của một revision không ghi trong chính tệp (ghi vào
  thì số tự đổi); đo bằng `wc -lc` trên tệp đã đóng băng. So sánh: r10 2362 dòng / 270 260 byte; bản chỉ-HINT lượt 10
  2442 / 279 045 (sha256 `6cc5e18e…0ad6`, trùng bản gộp VERDICT lượt 10 khai). Băm: phiên soạn r11 đo `VERDICT.md`,
  `HINT.patch` của lượt 10 và r1 đến r10 bằng `sha256sum` trước khi áp HINT và lại lúc đóng băng, khớp cả mười hai.
  r11: 2704 dòng / 323 028 byte; bản chỉ-HINT lượt 11: 2740 / 327 826 (sha256 `9e1ac379…9b84`, trùng bản gộp VERDICT
  lượt 11 khai). Phiên soạn r12 đo `VERDICT.md`, `HINT.patch` của lượt 11 và r1 đến r11 bằng `sha256sum` trước khi áp
  HINT và lại lúc đóng băng (bảng 14). (r13) r12: 3318 dòng / 367 327 byte; bản chỉ-HINT lượt 12: 3366 / 373 566
  (sha256 `127a8cb4e07347b0707efef425c49689270d65efe876f89a33471585dfe70b5a`, trùng bản gộp VERDICT lượt 12 khai). Phiên
  soạn r13 đo `VERDICT.md`, `HINT.patch` của lượt 12 và r1 đến r12 bằng `sha256sum` trước khi áp HINT và lại lúc đóng
  băng (bảng 15). (r14) r13: 3493 dòng / 395 790 byte; bản chỉ-HINT lượt 13: 3519 / 399 024 (sha256
  `7135e5c8c6504e7bcd677b716e8a9461033af07b8cbf6adad30a039f484b30d1`, trùng bản gộp VERDICT lượt 13 khai). Phiên soạn
  r14 đo `VERDICT.md`, `HINT.patch` của lượt 13 bằng `sha256sum` trước khi áp HINT, r1 đến r13 trước mọi sửa tay, và
  cả hai nhóm lại lúc đóng băng (bảng 16). (r15) r14: 3614 dòng / 423 534 byte; bản chỉ-HINT lượt 14: 3620 / 424 477
  (sha256 `fffa8ba0262b2c286fc84cd08532cc0d673ccdfefce8f4f1954265ed6a2595b8`, trùng bản gộp VERDICT lượt 14 khai). Phiên
  soạn r15 đo `VERDICT.md`, `HINT.patch` của lượt 14 và r1 đến r14 bằng `sha256sum` trước mọi sửa, và cả hai nhóm lại
  lúc đóng băng (đoạn "Kiểm lúc đóng băng r15" ở đầu r15). Đính chính (r16, cross-review lượt 15 đo): bảng "Thay
  đổi so với r14" ở đầu r15 khai năm số `grep -cF` theo cặp "r14 / r15" — ba ở dòng lớp
  `khai-khong-do-duoc-ma-do-duoc`, hai ở dòng lớp `kich-thuoc-thi-hanh-vuot-adr-0044`; vế sau (0, 1, 0, 0, 1) là số
  của bản chỉ-HINT lượt 14 (`fffa8ba0…95b8`). Trên chính r15 (`f0e9d580…1b99`) cả năm lớn hơn đúng 1 — 1, 2, 1, 1,
  2 — vì chính ô bảng ấy trích nguyên văn chuỗi nó đếm (lần thừa ở dòng 63 hay 64 của r15); cùng bẫy với neo B8 lúc
  đóng băng r14 (bảng 16 dòng 15). Phiên soạn r16 đếm lại năm chuỗi trên bản chỉ-HINT lượt 14 dựng lại (sha256 khớp) và
  trên r15: cùng các số trên; trên r14: 1, 0, 1, 1, 0 — vế trước của bảng ấy đúng. Đơn vị là DÒNG, như `grep -cF`;
  theo LẦN (`grep -o`), hai chuỗi của dòng lớp thứ hai trên r15 là 2 và 3, vì ô ấy trích mỗi chuỗi hai lần.
  (r16) r15: 3646 dòng / 430 433 byte; bản chỉ-HINT lượt 15:
  3656 / 431 753 (sha256 `98c895191dda8b55a63458f3e58b8af85e5d0fad20dae0d61ac3b391193a20bd`, trùng bản gộp VERDICT lượt
  15 khai). Phiên soạn r16 đo `VERDICT.md`, `HINT.patch` của lượt 15 và r1 đến r15 bằng `sha256sum` trước mọi sửa, và
  cả hai nhóm lại lúc đóng băng (đoạn "Kiểm lúc đóng băng r16" ở đầu r16).
- PID con đã `wait` bị hệ điều hành tái dùng giữa lúc `wait` và lúc đo: xác suất KHÔNG ĐO ĐƯỢC (lý do 4). Ở `B2-pid-du-phong`
  `da-wait`, PID bị tái dùng thì `kill(pid, 0)` thật thành công và ca báo `TinHieuChotCa` cho một bản ĐÚNG (dương tính
  giả); chạy lại là cách phân biệt; ca không khoá được khe này. Ở B8, PID của con hay cháu bị tái dùng giữa lúc giết
  và lúc kiểm sống: cùng giới hạn.

## 11. Câu hỏi mở — chủ kho trả lời TRƯỚC khi cấp lease (r8; r9; r10; r11; r12; r13; r14; r15; r16)

1. **ĐÃ TRẢ LỜI (r9).** Chủ kho, 2026-09-30T06:42:25Z (lời điều phối cấp; neo: PR #688 comment `5905670017`, phiên
   agent đăng hộ — phiên soạn r9 KHÔNG kiểm trên GitHub): *"#688: ngay trong packet này"*. Lớp "đọc lỗi ⇒ coi như đã
   chết" do giải mã ở `:359`, `:436`, `:490` và hai khối đọc của `_con_song` được sửa ở packet này: Q-A.7, B8; write
   set không đổi. Ba chỗ cùng khuôn ngoài write set: nợ ở §5. Tần suất ngoài thực tế: KHÔNG ĐO ĐƯỢC (lý do 4).
2. Ngưỡng ba lần của hình dạng "vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba" — nay mười lăm lần (§9): có hỏi lại
   quyết định gốc (cấu trúc của đường lỗi mới) hay không. Câu hỏi đã nêu từ r4; r9, r10 chỉ thêm dữ kiện, không tự trả
   lời. **ĐÃ TRẢ LỜI CHO LƯỢT NÀY (r11).** Chủ kho, 2026-09-30, trả lời trắc nghiệm (lời điều phối cấp, không có neo
   GitHub; phiên soạn r11 không kiểm được), nhãn đã chọn nguyên văn: *"Áp HINT, lặp tiếp (Recommended)"*. Nghĩa, theo
   lời điều phối: r11 = HINT lượt 10 — một hằng `comm` cho trục tách của ba hàm, một thước đo đếm `open` cho trục API
   đọc, thay vì liệt kê API — rồi review lượt 11; **nếu lớp `ma-tran-loi-thieu-chot` tái phát lần thứ mười thì DỪNG
   và thu hẹp**, không vá tiếp. r11 giữ đúng hai thước đo ấy (hằng `_K124_COMM_CHAU`; thước đo `open`, chỉ đổi từ "đếm
   bằng số lời đọc" sang "không `open` nào ngoài lời đọc đã ghi" vì phép đo — bảng 13) và THÊM đúng những gì phép tự
   liệt kê đường vào đòi (B2, bảng "Năm chỗ đọc × hai trục"; chốt tĩnh phần còn lại). Quyết định gốc (cấu trúc đường
   lỗi mới) KHÔNG được hỏi lại ở lượt này. **(r12)** Lượt 11 đo `ma-tran-loi-thieu-chot` ĐÃ ĐÓNG — không tái phát lần
   thứ mười — nên điều kiện dừng KHÔNG kích hoạt; r12 theo chỉ thị điều phối (ô `nguon_cap_viec`): HINT lượt 11 rồi đóng
   hai lớp P3. Lần thứ mười hai của hình dạng nằm ở CHÍNH cơ chế mới của r11 (chốt tĩnh theo dòng), và r12 đổi cách làm
   thay vì vá tiếp: danh sách cho phép trên toàn `launcher.py` (§7 B2) thay cho danh sách dòng. Quyết định gốc vẫn
   KHÔNG được hỏi lại. **(r13)** Lượt 12 đo `ma-tran-loi-thieu-chot` không tái phát, nên điều kiện dừng KHÔNG kích hoạt;
   r13 theo chỉ thị điều phối (ô `nguon_cap_viec`): HINT lượt 12 rồi đóng một lớp P2 và hai lớp P3. Lần thứ mười ba
   của hình dạng nằm ở phép đo răng của chính chốt r12 (§9 mục 13), và r13 THU HẸP lời khai thay vì thêm đối chứng.
   Quyết định gốc vẫn KHÔNG được hỏi lại. Câu hỏi về kích thước thi hành (ADR-0044) đã hỏi và ĐÃ TRẢ LỜI ở lượt soạn
   r13 — trần ≤ 1400 dòng thêm, THAY quyết định ≤ 600; nguyên văn, neo và lý do ở §4, mục "Ngoại lệ ADR-0044".
   **(r14)** Lượt 13 đo `ma-tran-loi-thieu-chot` không tái phát, nên điều kiện dừng KHÔNG kích hoạt; r14 theo chỉ thị
   điều phối (ô `nguon_cap_viec`): HINT lượt 13 rồi đóng hai lớp P3. Lần thứ mười bốn của hình dạng nằm ở chính lời khai
   của r13 và của HINT lượt 13 (§9 mục 14); r14 tự liệt kê và đo từng lời khai, không thêm luật. Trần 1400 và điều kiện
   dừng giữ nguyên; mẫu độc lập lượt 13 (+1135) cho biên 265. Quyết định gốc vẫn KHÔNG được hỏi lại.
   **(r15)** Lượt 14 đo `ma-tran-loi-thieu-chot` không tái phát, nên điều kiện dừng KHÔNG kích hoạt; r15 theo chỉ thị
   điều phối (ô `nguon_cap_viec`): HINT lượt 14, chỉ sửa câu chữ. Lần thứ mười lăm của hình dạng nằm ở chính các câu r14
   viết khi tự liệt kê lời khai (§9 mục 15). Trần 1400 và điều kiện dừng giữ nguyên. Quyết định gốc vẫn KHÔNG được hỏi
   lại.
   **(r16)** Lượt 15 đo `ma-tran-loi-thieu-chot` không tái phát, nên điều kiện dừng KHÔNG kích hoạt; r16 theo chỉ thị
   điều phối (ô `nguon_cap_viec`): HINT lượt 15, chỉ sửa câu chữ. §9 KHÔNG thêm mục: VERDICT lượt 15 xếp biểu hiện ở
   bảng thay đổi của r15 vào `so-lieu-noi-bo-lech` (TÁI PHÁT), không vào hai lớp lượt 14, và ghi rằng xếp theo VỊ TRÍ
   thì nó đọc thành "VÁ SINH LỖI MỚI" của hai lớp ấy — đếm nó là lần thứ mười sáu hay không là việc của điều phối, r16
   không tự quyết. Trần 1400 và điều kiện dừng giữ nguyên. Quyết định gốc vẫn KHÔNG được hỏi lại.
3. Cân bằng `DOT_BIEN` và phép (E) (B4): r10 và r11 giữ 54 dòng và đo 83 hạng mục cùng bảy biến thể lớp 124 (M1–M5, M12,
   `g_to_hop_dinh_dang_khoa`) bằng (E) MỘT lần — răng BỀN của bốn ca B8: KHÔNG CÓ. (r11: tám tên mới — ba
   `s_*_tach_ngoac_dau`, năm `g_*_open`; bảy có đích B8, `g_d_open` đích helper — cũng chỉ ở (E); số dưới đây CHƯA
   tính chúng, và chọn (b) hay (c) có đưa chúng vào `DOT_BIEN` hay không thì tính lại bằng cùng `_dot_bien_du_san`.
   Chốt tĩnh — r11, và `chot_tinh_r12.py` của r12 — là phép kiểm trên ứng viên, không phải dòng `DOT_BIEN`.) Ba phương án, số của B4 (cận dưới
   tĩnh; biên tính bằng `_dot_bien_du_san` của `423b4ba`):
   (a) giữ hiện trạng ⇒ biên 4, không có răng BỀN cho B8;
   (b) đưa M1–M5, M12 vào `DOT_BIEN` như dòng Linux-only ⇒ 71/237 không đo được trên Windows, 70,04 %, **biên 0**;
   thêm `g_to_hop_dinh_dang_khoa` ⇒ `DUOI SAN`. Hạ sàn hay đánh dấu dòng Linux-only ra khỏi mẫu số thì phải sửa
   runner `--dot-bien`, mà đặc tả cấm, và sàn 70 % là luật chung của kho;
   (c) **(r10, cross-review lượt 9, lớp `rang-ben-b8-bo-sot-phuong-an`)** đưa M1–M5, M12 vào `DOT_BIEN` KÈM một ca
   TĨNH chạy mọi nền làm đích phụ (ví dụ AST kiểm năm lời đọc đúng `DANG_DOC_QA7`) ⇒ **biên 6** (reviewer lượt 9 đo
   bằng runner thật, Windows giả lập: 237 mục, 65 không đo được, 72,57 %); thêm `g_to_hop_dinh_dang_khoa` (ca tĩnh
   không bắt được nó) ⇒ biên 5. Được: Linux đo lại hành vi bốn ca B8 ở MỖI lượt `--dot-bien` (răng BỀN). Giá: thêm
   một ca đăng ký (sửa §6 mục 2, §8 số ca và số mục `DOT_BIEN`); trên Windows dòng ấy chỉ đo DẠNG đọc; đo Windows
   THẬT: KHÔNG ĐO ĐƯỢC (lý do 2) trước merge.
   r10 KHÔNG chọn. Chủ kho giữ (a) ⇒ lease r10; chọn (b) hay (c) ⇒ revision mới (đổi B4, B5, B8, §6, §8). r11 và r12
   cũng không chọn; giữ (a) ⇒ lease r12. r13 cũng không chọn; giữ (a) ⇒ lease r13 (kích thước ở §4 là của phương án (a)).
   r14 cũng không chọn; giữ (a) ⇒ lease r14. r15 cũng không chọn; giữ (a) ⇒ lease r15. r16 cũng không chọn; giữ (a)
   ⇒ lease r16. Về mặt lịch sử r17 đã chọn (a); nếu lease từng được cấp tại r17 thì nó phải neo vào hash của r17, nhưng không có bằng chứng nào ở đây cho thấy lease đã thực sự được cấp; tại thời điểm soạn r18, r18 còn là DỰ THẢO và chưa có lease (lịch sử).
4. **(r11) Điều kiện cấp lease của Q5 — ĐÃ ĐỌC, không phải câu hỏi mới.** Mission #686 comment `5888633201` (phiên
   agent đăng hộ chủ kho; đăng 2026-09-29T10:45:55Z), r11 đọc qua REST lần đầu (r2 đến r10 không đọc): chủ kho *"Cấp
   lease cho wp 678, wp685 (khi #668 nhả launcher_test.py)"*, kèm ba điều kiện, TẤT CẢ đo lại ngay trước khi cấp:
   (1) `ai-dang-giu` cho `.claude/dev/launcher.py` và `.claude/dev/launcher_test.py` đều `NGƯỜI_GIỮ 0` — r11 đến r16
   KHÔNG đo lại; (2) lease neo `spec_hash` của r1 `ee44238c…37d9` "trừ khi đặc tả đổi revision trước đó" — tại thời điểm soạn r18, r18 còn là DỰ THẢO; lease generation 1 về sau đã neo r18, còn mỗi generation về sau neo băm của revision mà nó được cấp (g2: r19; g3: r20; công thức ở đầu tệp) — (r21; r22, r23, r24, r25, r26 thay) lease cấp theo r26 (nếu có) neo băm r26, còn lease g4, g4b neo r23 và lease g3 neo r20 (điều kiện hiệu lực: ô `revision`); (3) #668 land trước và đổi write set thì nền nghiệm thu phải
   dời bằng revision mới trước khi cấp — r10 đã dời sang `423b4ba`, r11, r12, r13 đo write set không đổi tới `fc852ff`,
   và r14 đo không đổi tới `20ec8d5`; r15 và r16 không đo lại (ô nền nghiệm thu).
5. **(r22) TÊN ref bằng chứng và quyền đẩy lên nó** (đoạn "Mỏ neo bằng chứng dùng lại", phần (4)) — đặc tả không tự
   nêu và không cấp. Điều phối hoặc chủ kho nêu tên ref (hay kênh artifact) và quyền đẩy ở một nguồn có `id` TRƯỚC khi
   cấp lease neo băm r26; chưa có thì executor DỪNG ở bước thăm dò phía ghi, không chạy đo nặng. Đây là bước attempt 2
   của generation 2 hụt (`ED-immutable-artifact-missing`, #686 comment `6030711659`; các mã finding của attempt 1, event
   `6029697859`, không có mã ấy).
