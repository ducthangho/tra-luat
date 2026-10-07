# ĐẶC TẢ — `CI-G5-CONG-CU-VA-TIEP` (`wp698`) — revision 4, ĐÓNG BĂNG

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp698` (ID bền `wp<issue>`, protocol §3.2); tên đọc được: `CI-G5-CONG-CU-VA-TIEP`. Hai tên cùng chỉ một packet; lease dùng tên nào cũng phải kèm `packet_issue: 698`. |
| `revision` | **4** |
| `thay_the_cho` | **r3**: `ops/specs/ci-g5-cong-cu-va-tiep-r3.md`, sha256 `53bf55fec7ac8553ee8106a615940bb875846ab095e1fcb0544300a2a28dfe1b`, commit `276a65f4514034f359ae55c13caa5e0a6d7db1c4` (cha `c54b502`, là commit của r2). Thứ định danh r3 là **cặp băm này**, không phải tên nhánh chứa nó: tìm commit ở `master` trước, chưa thấy thì ở nhánh mang đặc tả. Lúc soạn r4, trong kho cục bộ chỉ có ref `refs/heads/claude/spec-wp698` chứa `276a65f` (`git for-each-ref --contains`), và comment `6038138825` của #698 ghi commit ấy là "CỤC BỘ, CHƯA ĐẨY"; trạng thái trên máy chủ **KHÔNG ĐO ĐƯỢC** từ phiên soạn r4 (không fetch). r3 bị review lượt 3 trả `changes_requested` (hàng dưới), nên không đi tới xác nhận closure Q10; mọi closure, lease và `spec_hash` từ nay neo **r4**. r4 không sửa byte nào của r1, r2 hay r3 (đo bằng `sha256sum` trước và sau khi soạn). **Dòng dõi:** r1 (`3a555263…4996`, `dcc2cbc`) → r2 (`f69bb398…2c0a`, `c54b502`) → r3 (`53bf55fe…dfe1b`, `276a65f`) → r4 (tệp này). r1 và r2 vẫn được nêu ở các hàng review và ở §0-r2, §0-r3 để truy dòng dõi; chúng không còn là đối tượng closure. |
| review của r1 | **Lượt 1**, reviewer Claude Sonnet 5.5 chạy bằng subagent: `verdict: changes_requested`, `reviewed_sha: dcc2cbcd404856dfc9f878478b054198d1f46ca1`, **0 P1 · 5 P2 · 3 P3 = 8 lớp**. Tệp `VERDICT.md` sha256 `c825a405a9897a21a356c5c721af1ce703f348d3972dd6c07b5a6b922f2f2133`; `HINT.patch` (chỉ văn bản đặc tả, không có mã `ops/cong_cu_test.py`) sha256 `b330820068a6d710351bbfd912e364b224759a533c8de59192b7a5ba0e95a641`. Verdict đã đăng trên #698; ID comment **KHÔNG ĐO ĐƯỢC** từ phiên soạn r2 (phiên này không đọc lại GitHub). Phiên soạn r4 đọc lại #698 qua REST (`gh api …/issues/698/comments`, chỉ đọc): bản chiếu lượt 1 là comment `5920362746`, tạo 2026-09-30T21:52:06Z. Nguồn có thẩm quyền là tệp có băm, không phải bản chiếu. Cách r2 đóng từng lớp: **§0-r2**. |
| review của r2 | **Lượt 2**, reviewer Claude Sonnet 5.5 chạy bằng subagent (tự khai effort "max"): `verdict: changes_requested`, `reviewed_sha: c54b502bff2aaf3e9a40f8b0b37a657fa09174c1`, `spec_sha256: f69bb398…2c0a`, **0 P1 · 4 P2 · 12 P3 = 16 lớp / 56 biểu hiện**. Tệp `VERDICT.md` sha256 `e281338f322250c6a4af17214136bc95f0072435333c1363d24d3b9b4b8e3968`; `HINT.patch` (chỉ văn bản đặc tả, 16 nhóm, 17 hunk) sha256 `83b9df3323d1e2d276c1ff2d2d416a92f2213382347bb8d1cfcf0629cc95e832`. Cả hai băm được phiên soạn r3 đo lại bằng `sha256sum` trước khi dùng: khớp. Phiên điều phối đã chiếu verdict lên #698; ID comment không có trong dữ kiện cấp cho phiên soạn r3, nên **KHÔNG ĐO ĐƯỢC** từ đó. Phiên soạn r4 đọc lại qua REST: bản chiếu lượt 2 là comment `5928410072`, tạo 2026-10-01T09:14:34Z. Nguồn có thẩm quyền là tệp có băm. Cách r3 đóng từng lớp: **§0-r3**. |
| review của r3 | **Lượt 3**, reviewer Claude Sonnet 5.5 chạy bằng subagent (tự khai effort "max"): `verdict: changes_requested`, `reviewed_sha: 276a65f4514034f359ae55c13caa5e0a6d7db1c4`, `spec_sha256: 53bf55fe…dfe1b`, **0 P1 · 2 P2 · 4 P3 = 6 lớp / 11 biểu hiện**; tỷ lệ vá thật lượt 2 → 3 theo §12 là 13/16 = 81,25% (cách đọc nghiêm 12/16). Tệp `VERDICT.md` sha256 `d3d848edec273353371bc714d06f9d9e1c0080c829a3285352732007dee4b955`; `HINT.patch` (chỉ văn bản đặc tả, 6 nhóm, 13 hunk) sha256 `47a2a4b99e1627293283cfa16d4329cea3ec286f02c2b77cd602af2ab7db6074`. Cả hai băm được phiên soạn r4 đo lại bằng `sha256sum` trước khi dùng: khớp. Bản chiếu trên #698 là comment `6038138825`, tạo 2026-10-07T12:42:18Z (đọc lại qua REST lúc soạn r4; thân comment mang đúng hai băm trên). Nguồn có thẩm quyền là tệp có băm. Cách r4 đóng từng lớp: **§0**. |
| `packet_issue` | **#698** (object ID `5646961843`, tạo 2026-09-30T13:09:12Z). Issue và hai comment quyết định (`5912199805`, `5914438647`) đều do **phiên agent đăng hộ chủ kho** bằng credential chủ kho. Vì vậy `author_association: OWNER` không chứng minh chủ kho tự gõ; tư cách của chúng là lời khai có neo (#566). |
| `mission_issue` | RỖNG. #698 không khai Mission. Packet mẹ #668 cũng không khai (đặc tả `ops/specs/CI-G5-CONG-CU-CHIA-MANH-r1.md`). Thẩm quyền của closure do đó đi qua quyết định Q10 (§11). |
| `nguon_cap_viec` | Chỉ thị chủ kho, nguyên văn: *"#668: mở packet tiếp nối cho F48–F50"*, neo ở #668 comment `5911957306` và thân #698. Nguồn phát hiện: verdict cross-review **lượt 22** của phiên `session_01VYtkBy…`, #668 comment `5911284002` (12:27:04Z 30-09). Verdict này mang nhãn `advisory_review`, kết luận `changes_requested` với 0 P1 · 2 P2 · 1 P3, `reviewed_sha` là `8d7faef`, và commit ấy **chưa được đẩy** lên GitHub. Executor và reviewer: #698 comment `5912199805`, nguyên văn *"Chọn opus 5.5 executor. Reviewer để sonnet 5.5 xem"*. **Quyết định chủ kho cho r1:** #698 comment `5914438647`, tạo 2026-09-30T15:30:26Z, gồm hai lượt trả lời trong phiên lúc 15:28:25Z và 15:30:09Z (§11). **r2:** phiên điều phối giao soạn revision 2 theo verdict lượt 1; những chỗ r2 tự quyết thay cho chủ kho được liệt ở §11.1 và chỉ có hiệu lực khi comment Q10 xác nhận closure của r2. **r3:** phiên điều phối giao soạn revision 3 theo verdict lượt 2 (chỉ thị trong phiên; phiên soạn r3 không đọc GitHub); những chỗ r3 tự quyết được liệt ở §11.1 (B) và (C). **r4:** phiên điều phối giao soạn revision 4 theo verdict lượt 3 (chỉ thị trong phiên, 07-10); những chỗ r4 tự quyết được liệt ở §11.1 (D). Mọi điểm của §11.1 (A)–(D) cùng một điều kiện: chỉ có hiệu lực khi comment Q10 xác nhận closure của **r4**. |
| `objective` | Đóng các khe đo trong `ops/cong_cu_test.py` mà phép đo trên nền `fc852ff` tái hiện được (§1, §1.8, §1.9). **(B)** Bốn bộ đọc giá trị ngoài của lớp B — `bk`, `mh`, `ra` của `_doc_che_do` và `head` của `_van_tay` — không có ô bắt các phép chuẩn hoá trước khi nhận: NFKC, bỏ Cf, bỏ TAB, bỏ Zs ngoài ASCII, bỏ Cc, bỏ dấu kết hợp. Với `bk`, `mh`, `ra`: **mọi vị trí** × **mọi thành viên** của tập điểm mã `D698` (định nghĩa bằng thuộc tính Unicode, không liệt kê; §5 M1), so với oracle độc lập. Với `head`: `D698` ở ba vị trí neo cộng đại diện `R698`/`N698` ở mọi vị trí — tổ hợp "thành viên ngoài `R698` × vị trí ngoài ba neo" **không** được đo, và ba dò `x_head_cf2063_at17`, `x_head_cfk_mid_only`, `x_head_sm_mid_only` được khai SỐNG (tập KHAI, §6); cộng ô **nhiều dòng** (r3, M1b): nhiễu, rồi MỖI ký tự mà `str.strip()` bỏ (tập `str.isspace`, dẫn xuất), rồi mã băm, theo cả hai thứ tự. **(C)** `ra` không có ô cho các phép đường dẫn (`normpath`, `expanduser`, `expandvars`, bỏ `./` đầu, bỏ `/` cuối…) ở `_doc_che_do` (M2), và — r3 — ở **mọi tầng hạ nguồn** mà `ra` đi qua: giải gói và hai lời gọi bộ ghi trong `main`, rồi bộ ghi `_ket_thuc_manh` (M2b). **(D)** Nhánh mảnh của `main` không có điểm lực lượng cho vị từ đếm một biến lẫn nhiều biến: trục trọn cộng lưới **tích biên** (M3). **(E)** Tập ngoại lệ mà `_van_tay` bắt phải được đo **chính xác** từ hai phía trên một miền kiểu **dẫn xuất** — r3, M5b: bao đóng bắc cầu của `BaseException.__subclasses__()` lúc chạy — không phải vài kiểu chọn tay. Mỗi đường vào có ít nhất một đột biến canh trong `DOT_BIEN`, chỉ đúng ca đích giết nó bằng `TinHieuChotCa`, bán kính 1; và **mọi** dò của tập dò đóng (Phụ lục C, Phụ lục H và — r4 — Phụ lục J) thuộc A1–A3, A8 phải bị giết khi nghiệm thu, trừ đối chứng, dò tương đương và dò KHAI nêu đích danh ở §2/§6. Lớp (A), tức registry năng lực ngoài cửa sổ (F48), **không** thuộc packet: nợ `registry-nang-luc-ngoai-cua-so` (Q1). Bộ đọc ngoài lớp B — đầu tệp mảnh của `_gom_manh`, `CONG_CU_TEST_TIEN_TRINH`, và (r3) hai bộ đọc `argv`: thư mục `--gop` và cửa ở `argv[1]` — được đo và ghi nợ, không vào mục tiêu (§2, §11.1). **(r4)** Mọi ô mới gọi mã bị đo phải biến **mọi** `BaseException` mà mã ấy ném thành dữ liệu so được với kỳ vọng, ở cả bốn chỗ gọi — `doc` của T1, quét `head`, `main` của T2/T3, bộ ghi T4/T5 (M6); T5 có ô gặp tệp cũ và ô so dòng in (M2b); và mỏ neo của **mọi** mục `DOT_BIEN` có tệp đích `ops/cong_cu_test.py` xuất hiện đúng một lần trong tệp ấy sau khi bảng đã ghi (A5, Phụ lục F bản r4). |
| `review_class` | **`sensitive`**: bộ test gate G5 có vòng đột biến tự kiểm, cùng lớp với #668. Fail-closed theo protocol §8. |
| `risk` | **`sensitive`**: cùng lý do trên. |
| `executor` | `claude`, model Claude Opus 5.5 (`claude-opus-5-5`), theo comment `5912199805`. Effort do phiên tự khai; từ ngoài là **KHÔNG ĐO ĐƯỢC**. |
| reviewer | Claude Sonnet 5.5, **chạy bằng subagent** trong phiên điều phối (quyết định chủ kho, §11 Q6). Chỉ mô tả hướng sửa, không đính patch-as-hint chứa mã (Q14). `HINT.patch` của lượt 1 chỉ sửa văn bản đặc tả; r2 áp nó ở bước đầu rồi sửa tiếp (§0-r2 ghi chỗ nào của HINT bị r2 thay). `HINT.patch` của lượt 2 cũng chỉ sửa văn bản; r3 áp nó ở bước đầu rồi sửa tiếp theo phép đo (§0-r3 ghi chỗ nào của HINT bị r3 thay và vì sao). `HINT.patch` của lượt 3 cũng chỉ sửa văn bản; r4 áp nó ở bước đầu rồi sửa tiếp theo phép đo (§0 ghi chỗ nào của HINT bị r4 thay và vì sao). |
| assurance đạt được | **`review_deferred`.** Hai lý do độc lập. (1) Reviewer tự khai chạy bằng subagent, tức `model_reviewer_identity.che_do` chứa `subagent`. Khi đó `_thieu()` của `ops/bien_nhan_v2.py` từ chối mọi mức trong `ASSURANCE_CAN_DOC_LAP` (`cross_approved`, `same_provider_approved`, `human_audited`), nên biên nhận chỉ được ghi `review_deferred`. (2) Dù chạy phiên độc lập, `cross_approved` cũng không đạt được, vì executor và reviewer cùng họ Claude (protocol §8 mục 1; `ops/bien_nhan_v2.py` từ chối `cross_approved` khi hai bên cùng họ model). **Cổng land là `human_audited`** do chủ kho audit (§8: `sensitive` phải có `cross_approved` hoặc `human_audited`). |
| ngưỡng review | **0 P1 · 0 P2 · 0 P3**. Không giới hạn số vòng (Q5). Trần canon trục VÒNG áp cho packet này là trần của **ADR-0048** (Accepted 2026-09-12), vì đặc tả đóng băng **sau** mốc ấy; ADR-0048 thay đúng con số trục VÒNG của ADR-0043, còn ba trục, trần độc lập và luật `nang_tran` vẫn là của ADR-0043. Con số chỉ có một chỗ ở là ADR-0048; tệp này chỉ **chép** nó vào `tran_cu` của khối `nang_tran` dưới đây vì ADR-0043 đòi trường ấy. Vượt trần là có chủ đích; khối có hiệu lực từ vòng review hợp lệ đầu tiên vượt `tran_cu`. |
| `environment` | **`cloud`**. Mục tiêu r3 gồm ô thuần, miền dẫn xuất, giàn giả trong một tệp test, và (r3, M2b) ô bộ ghi ghi tệp THẬT vào thư mục tạm với tên chứa ký tự của `D698` — hợp lệ trên POSIX (mọi ký tự trừ NUL và `/`), chưa đo trên Windows. r3 không đo đồng hồ ngủ máy và không cần quyền tạo symlink, vì lớp (A) là lớp phụ thuộc năng lực symlink và đã ra ngoài packet. **Không chạy Windows** (quyết định chủ kho, Q8), nên đường Windows của các ô mới không được đo; đây là nợ `windows-chua-do-o-moi-wp698`. |
| `depends_on` | **Chặn cấp lease: lease `wp671-windows-bash-nen-escape-r1-g2-claude` (#671).** Lease này giữ `ops/bash_nen.py` và `ops/cong_cu_test.py` tới `2026-10-01T03:35:00Z`. Tệp lease nằm ở `refs/remotes/origin/ops/cap-lease-671-g1` (commit `1235a32`). Chỉ cấp lease `wp698` khi cả năm điều kiện dưới đây thoả **và được đo lại lúc cấp**; số trong ô này không thay được phép đo lúc cấp. (1) So `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`) theo **tập tên VÀ OID**: thiếu cục bộ 0, lệch OID 0. Không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. (2) `python ops/lease_publish.py ai-dang-giu ops/cong_cu_test.py` ra `NGƯỜI_GIỮ 0`, rc=0. Phải chạy trên clone mà mọi nhánh cục bộ đều không tụt sau `origin` và không nhánh nào khai upstream đã mất; nếu không, bộ quét fail-close `rc=12` trước khi kịp đếm người giữ (xem "Lịch sử đo" ở cuối ô này). (3) Nếu #671 land trước và đổi `ops/cong_cu_test.py` thì phải **dời nền bằng revision mới trước khi cấp**, không cấp trên nền cũ. Nhánh ứng viên `claude/wp671-windows-bash-nen-escape-g1` @ `bd6ad5d` đổi tệp này +163/−22 so với nền `89fc4fa` của nó (đo lại 15:41:32Z 30-09). (4) Chủ kho đã xác nhận closure bằng một comment trên #698 neo `spec_hash` của **tệp này (r4)** (Q10), và lease neo đúng `spec_hash` ấy. (5) Không có lượt review nào đang chạy trên write set. **Hiện trạng đo 15:40:23Z–15:40:36Z 30-09** (clone sạch, `origin` = GitHub, HEAD = `origin/master` = `fc852ff`): máy chủ 459 ref, cục bộ 459, thiếu cục bộ 0, thừa cục bộ 0, lệch tên+OID 0. `ai-dang-giu ops/cong_cu_test.py` ra `NGƯỜI_GIỮ 1: wp671-windows-bash-nen-escape-r1-g2-claude` (nhãn `CÒN_HẠN`), rc=11, kèm 54 dòng `HẾT_HẠN`. Điều kiện (2) **chưa thoả**. Lịch sử đo: lúc 15:04:45Z–15:05:09Z có 458/458 ref và cùng người giữ; lúc 14:43:27Z `ai-dang-giu .github/workflows/ci.yml` ra `NGƯỜI_GIỮ 0`, rc=0. Cũng tại 14:4xZ, kho dùng chung của phiên điều phối cho `rc=12` (`KHÔNG_XÁC_ĐỊNH`: một nhánh cục bộ khai upstream `refs/remotes/origin/ops/spec-lease-id-ep-kieu-yaml`, mà ref này không còn); đó là lỗi của kho cục bộ, không phải kết quả về người giữ. Phiên soạn r2, r3 và r4 đều **không** đo lại ô này (không cấp lease ở bước soạn đặc tả; phiên r3 không có mạng; phiên r4 không fetch, không clone mạng); mọi số trong ô là của lượt soạn r1. Lease #671 đã quá hạn khai (`2026-10-01T03:35:00Z`) theo đồng hồ, nhưng "chưa hết hạn" và "còn hiệu lực" là hai câu hỏi khác nhau và cả hai chỉ trả lời được bằng phép đo lúc cấp (điều kiện (1)–(2)). |
| nền nghiệm thu | **`fc852fff7da37f1669569572b79571446e61c294`** (merge PR #697, bookkeeping #668), theo quyết định chủ kho Q11. Đây là **nền bất biến** để đo diff và nghiệm thu. Bản nháp trước r1 dùng `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (merge PR #696). Đo 15:31:57Z 30-09: `git rev-parse 423b4ba:ops/cong_cu_test.py fc852fff7da37f1669569572b79571446e61c294:ops/cong_cu_test.py` cho hai lần cùng blob `9edea6b1629b46f27758b2073e74210dc73495b7`, và `git diff --quiet 423b4ba fc852fff7da37f1669569572b79571446e61c294 -- ops/cong_cu_test.py` cho rc=0. Hai nền khác nhau ở 66 tệp, tất cả là hồ sơ: `ops/land/` 23, `ops/leases/` 3, `ops/reviews/` 39, `ops/specs/` 1 (`git diff --name-only 423b4ba fc852ff`). **Đo lại lúc soạn r2**: 22:24:51Z 30-09, `git ls-remote origin refs/heads/master` = `fc852fff…`; **03:09:18Z 01-10** = `20ec8d5d0e86cb7dc01f202c7596407a957e5961` (merge PR #689, commit lúc 2026-10-01T00:55:21Z, sau merge PR #692). Fetch vào một kho tạm: `git diff --name-only fc852ff 20ec8d5` = đúng 2 tệp, `ops/land/pr684-wp677-land-evidence.yaml` và `ops/lease_publish_test.py`; `git rev-parse 20ec8d5:ops/cong_cu_test.py` = `9edea6b1…` (trùng nền) và `git diff --quiet fc852ff 20ec8d5 -- ops/cong_cu_test.py` rc=0. `origin/master` đã đổi nhưng **không chạm write set**, nên nền nghiệm thu giữ `fc852ff` theo Q11, không dời; nền tiếp nối lúc cấp lease phải khai riêng (dòng dưới). **Lúc soạn r3** (01-10, không mạng): mirror bare của sandbox review lượt 2 có ref `origin-master` = `20ec8d5d0e86cb7dc01f202c7596407a957e5961` và `git rev-parse 20ec8d5:ops/cong_cu_test.py` = `9edea6b1…` (trùng nền); phiên r3 không đọc lại GitHub, nên `origin/master` hiện hành là **KHÔNG ĐO ĐƯỢC** từ đây và phải đo lúc cấp lease (điều kiện (3) của `depends_on`). **Lúc soạn r4** (07-10, không fetch): ref `origin/master` trong **bộ đệm** của kho chính là `ab457c651eb4428705f0492163080b661c858b72` (merge PR #712); `git rev-parse ab457c6:ops/cong_cu_test.py` = `9edea6b1…` (trùng nền) và `git diff --quiet fc852ff ab457c6 -- ops/cong_cu_test.py` rc=0. Đó là đọc bộ đệm, không hỏi máy chủ (bài học `for-each-ref` trong `CLAUDE.md`), nên `origin/master` trên máy chủ vẫn **KHÔNG ĐO ĐƯỢC** từ phiên soạn r4. Mọi phép đo ở §1.8 và §1.9 chạy trên bản sao `fc852ff` (blob `ops/cong_cu_test.py` = `9edea6b1…`, đo lại bằng `git hash-object`). Nền tiếp nối (continuation base) là `origin/master` lúc cấp lease; nếu nó khác `fc852ff` thì lease phải khai riêng, và nếu nó đổi `ops/cong_cu_test.py` thì phải dời nền bằng revision mới trước khi cấp (cùng lý lẽ với S3). Diff nghiệm thu đo trên `ops/cong_cu_test.py` so với `fc852ff`, cộng với điều kiện A4-f. |
| `spec_hash` | Xem **Công thức băm** dưới đây. Giá trị **không** nằm trong tệp này. |

**Khối `nang_tran`** (ADR-0043: vượt trần phải khai `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`; ADR-0048 giữ nghĩa vụ ấy).
Lease phải chép nguyên khối này:

```yaml
nang_tran:
  truc: vong_review
  tran_cu: 10
  tran_cu_nguon: 'ADR-0048 (Accepted 2026-09-12), truc VONG; dac ta nay dong bang 2026-09-30, sau moc, nen khong ap so cu cua ADR-0043'
  tran_moi: khong_gioi_han_lap_toi_0_P1_0_P2_0_P3
  hieu_luc: 'tu vong review hop le dau tien vuot tran_cu; dinh nghia vong review hop le theo ADR-0043/ADR-0048, khong doi'
  ai_nang: ducthangho
  can_cu: https://github.com/ducthangho/tra-luat/issues/698#issuecomment-5914438647
  khi_nao: '2026-09-30T15:30:09Z'
  ghi_ho: phien agent dang ho chu kho (comment 5914438647, loi khai co neo #566)
  ghi_chu_so_cu: 'comment 5914438647 viet "khong gioi han 2 vong": so 2 la so truc VONG cua ADR-0043 da bi ADR-0048 thay; y quyet dinh (lap toi 0/0/0, khong tran) khong doi'
```

Khối này chỉ nâng trần **trục VÒNG**. Hai trục kia của ADR-0043 (LỜI GỌI `codex_review_calls_used`, ATTEMPT) không bị nâng. Số 2 trong khối `nang_tran` của tiền lệ `wp461-be-mat-thu-hai-cua-codex-exec-1g9-claude-20260925` là trần **LỜI GỌI** (khối ấy khai `truc: loi_goi`), không phải trần vòng; tiền lệ cùng họ `…-1g7-…` ghi trong trường `truc_vong_ghi_chu` rằng trục VÒNG theo ADR-0048 áp cho spec đóng băng từ 2026-09-12 và không bị nâng ở đó (con số chỉ nằm ở ADR-0048 và ở `tran_cu` trên; không chép lại trong câu trích này; đo lại lúc soạn r2 bằng `grep -n`). Khối **không** gỡ checkpoint theo lớp của protocol §12 (xem S6). Đo lúc soạn r2: `grep -c nang_tran` trong `ops/lease_publish.py` và `.claude/dev/packet_loop.py` ra 0 và 0. Tức không có cổng máy nào đọc khối này; ADR-0048 tự khai đúng điều đó và sửa lời khai ngược của ADR-0043 ("thiếu khối thì cổng đăng lease từ chối"). Khối này là hồ sơ thẩm quyền, không phải chốt máy; người cấp lease và reviewer kiểm nó **bằng tay**.

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit
đóng băng: `sha256sum ops/specs/ci-g5-cong-cu-va-tiep-r4.md`, không loại dòng nào. Giá trị
được công bố **ngoài** tệp, trong comment xác nhận closure của chủ kho trên #698 (Q10) và trong
lease, kèm OID commit và đường dẫn. Nếu hai tên `spec_hash` và `spec_sha256` cùng xuất hiện thì
chúng mang **cùng** một giá trị. Đổi bất kỳ byte nào ⇒ revision mới, băm mới, lease mới. Khối
closure dưới đây nằm **trong** tệp, nên một `spec_hash` không thể đi với hai closure khác nhau.

**Closure đóng băng** (các trường dispatcher dẫn xuất, protocol §3.2). Kho chưa có
dispatcher sinh các trường này, cũng chưa có policy canonical cho closure. Khác tiền lệ
`ops/specs/lease-id-ep-kieu-yaml-r6.md` (miễn trừ ở Mission #682), packet này **không có**
descriptor miễn trừ nào: phiên soạn điền tay khối dưới. Theo quyết định Q10, khối chỉ có
hiệu lực khi chủ kho xác nhận bằng một comment trên #698 neo `spec_hash`, và lease chỉ được cấp
sau comment ấy. Đổi bất kỳ giá trị closure nào ⇒ revision mới. Write set không mở rộng.

| trường | giá trị |
|---|---|
| `change_policy_sha` | `null`: chưa có policy canonical |
| `effective_write_set` | `ops/cong_cu_test.py` (exact) |
| `effective_review_class` | `sensitive` |
| `required_checks` | Trên PR, tại exact head. PR chỉ được mở **một lần**, khi review đã đạt 0/0/0; không chạy CI trong vòng lặp (Q7). (a) Bốn context bắt buộc của ruleset `bao-ve-cong-dang-lease` (id `20856202`, đọc lại qua REST lúc 15:40Z 30-09, `updated_at` không đổi so với lần đọc 14:44:35Z): `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, `gate-cong-cu-gop (ubuntu-latest)`. (b) Tám job mảnh, từ `gate-cong-cu (ubuntu-latest, 0)` tới `gate-cong-cu (ubuntu-latest, 7)`; tên job lấy nguyên văn từ lượt hậu-merge `36696528580`. (c) `gate-registry (ubuntu-latest)` với rc=0. Theo quyết định Q9, nếu job này đỏ **vì hết trần** trên một run của PR #698 thì (c) được coi là đạt khi (a) và (b) xanh; phải ghi nợ có neo `gate-registry-het-tran-wp698` kèm run ID/job ID. Quyết định này chỉ áp cho các run của PR #698, và **chỉ miễn (c)**: nguyên văn Q9 nói về `gate-registry`, không nói về (d) hay (e), nên (d) và (e) vẫn bắt buộc. Muốn miễn (d) thì phải có quyết định chủ kho riêng (§11.1). **Định nghĩa tác nghiệp của "đỏ vì hết trần"** — ĐẠT khi cả ba điều sau đúng trên log job `gate-registry` của run ấy: (1) có **đúng một** dòng `CI_DANG_KY … ĐỎ`, và nó là `CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐỎ — LỖI HẠ TẦNG: hết giờ <n> giây, rc=-9`; (2) không dòng `CI_DANG_KY` nào khác mang `ĐỎ` (dòng hợp lệ in `ĐẠT` hoặc `CÁCH LY`); (3) dòng tổng là `TỔNG: ĐỎ` và chỉ do mục ở (1). Tiền lệ có trong kho: `ops/land/pr696-wp668-provenance/trich-log.txt` — job `109832781748` của run `36696528580` có dòng 1962 `CI_DANG_KY_KE_HOACH ops/nhanh_don_duoc_test.py: day_du — diff chạm .github/workflows/ci.yml, ops/cong_cu_test.py`, dòng 2438 `…CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐỎ — LỖI HẠ TẦNG: hết giờ 4500 giây, rc=-9`, dòng 2440 `TỔNG: ĐỎ`; run PR `36689211190` có dòng 2590 `CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐẠT rc=0`. Số "dòng" ở đây và ở S7 là số dòng trong **log thô**, đúng như trích log ghi ở đầu mỗi mục (định dạng `<số dòng log thô>: <nội dung>`, khai ở dòng 2 của tệp trích); trong tệp trích, các mục 1962/2438/2440 nằm ở dòng 23–25, mục 2590 ở dòng 99, hai mục 765/767 của S7 ở dòng 103–104 (đo lúc soạn r3 bằng `grep -n`). PR #698 cũng sẽ chạy chế độ đủ: `.claude/dev/ci_dang_ky_test.py:730` khai `TIEN_TO_CHUNG = ("ops/cai_", "ops/cong_cu")`, và `ops/cong_cu_test.py` khớp tiền tố ấy (đo lúc soạn r2). Thời lượng hai run ấy (reviewer lượt 1 ghi 66,5 phút và 83,3 phút) **KHÔNG ĐO ĐƯỢC** ở r2: trích log trong kho đã bỏ dấu thời gian. (d) Job `thu-hoi` của `.github/workflows/ops-thu-hoi-admission.yml` (`pull_request_target` vào `master`, các kiểu `opened` `reopened` `synchronize` `ready_for_review` `edited`). Job này **chưa là required check**: `ops/lease_publish.py:1093` đặt `SO_THU_HOI_KICH_HOAT = False`, và dòng 6 của workflow tự ghi "chưa là required check" (đo lúc soạn r3 trên `fc852ff`). Đặc tả vẫn giữ (d) làm điều kiện vì nó chặt hơn chữ Q9 theo hướng fail-closed — một lượt `thu-hoi` đỏ trên exact head là tín hiệu provenance (tiền lệ PR #696 ở S7) mà land không được tự bỏ qua — nhưng **không** tự phán đỏ thành thất bại: đỏ ⇒ DỪNG, hỏi chủ kho (S7). Đây là một cách đọc Q9 (§11.1 (B), dòng Q9), chỉ có hiệu lực khi comment Q10 xác nhận. (e) **Không** có lượt Windows (Q8). |
| `land_obligations` | 1. Chủ kho audit (`human_audited`) trên exact head, cộng uỷ quyền merge bền. Không phiên nào tự approve hay tự merge. 2. Verdict mọi lượt review và biên nhận v2 của chúng vào `ops/reviews/`, theo mẫu #668, với nhãn `review_deferred`; gồm cả lượt review đặc tả r1, r2, r3 và r4. 3. Hồ sơ land vào `ops/land/`, theo tiền lệ PR #691 và #697. 4. Đặc tả (r1, r2, r3 và r4) và lease vào master bằng một PR bookkeeping. 5. Thu hồi lease sau land bằng rút hạn. **Không** viết bia mộ `da_bi_thay_the` vào lease đã hết hạn (bài học run `35519177197`/`35519243379` trong `CLAUDE.md`). 6. Đóng #698 và đăng comment nối trên #668. 7. Ghi nợ có tên vào trường `no_con_mo` của hồ sơ land ở mục 3 (tiền lệ: `ops/land/pr696-wp668-land-evidence.yaml`, trường `no_con_mo`): `registry-nang-luc-ngoai-cua-so` (Q1); `so-tien-trinh-nhan-fullwidth` (Q2; gồm cả khe mức đo `t_cf`, `t_tab` của §1.8.6); `windows-chua-do-o-moi-wp698` (Q8); `gom-dau-manh-chuan-hoa-wp698` (§2, §11.1); `doc-argv-chua-co-o-wp698` (r3: thư mục `--gop` và cửa `argv[1]`, §1.9.6, §11.1); `j-chua-co-canh-wp698` (r4: các đường của Phụ lục J chỉ đo ở nghiệm thu, không có canh thường trực, §10, §11.1 (D)); và `gate-registry-het-tran-wp698` nếu xảy ra (Q9). Chủ thể ghi: phiên soạn hồ sơ land. 8. Hồ sơ lượt 22 vào một nhánh `ops/**` kèm băm (Q13). Chủ thể: **người chủ kho chỉ định**, vì executor không có các tệp ấy (phiên soạn r1, r2, r3 và r4 chỉ có băm của chúng trong comment `5911284002`). Việc này **không** chặn land. |

Lease phải **chép** đúng các giá trị trên và khối `nang_tran`, không thêm, không đổi. Lệch ⇒ **DỪNG**.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm. Tập dò đóng
của r4 có **401** dò: Phụ lục C (221 dò — 53 dò của reviewer lượt 1 chép nguyên văn, cộng 168 dò do
phiên soạn r2 liệt kê từ mã) cộng Phụ lục H (145 dò — 64 dò E1–E8 của reviewer lượt 2 chép nguyên văn,
cộng 81 dò R3-* do phiên soạn r3 liệt kê từ mã) cộng Phụ lục J (35 dò `x4_*` do phiên soạn r4 liệt kê từ mã
theo chỗ gọi và tầng; 28 dò `y_*` của reviewer lượt 3 — `evidence/scripts/extra_rv3.py`, sha256 `c1e3d1e8…426f` —
không vào tập đóng vì tên của chúng không theo luật tên của Phụ lục D, nhưng được chạy đối chiếu trên ứng viên đo, §1.10.8);
**danh sách ấy vẫn có thể thiếu**. Reviewer tìm ra
được một đường sống ngoài danh sách thì đường ấy tính là finding (protocol §8, "bảng bằng chứng phải
tự khai giới hạn").
Ba đời ứng viên tham chiếu IMP-R2, IMP-R2F, IMP-R2G (§1.8), ứng viên `IMP-ME` của reviewer lượt 2, các
biến thể đo `v3_*` của phiên soạn r3 (§1.9) và các biến thể đo `v4_*` của phiên soạn r4 (§1.10) là công cụ đo,
**không** phải bản giao, và mã của chúng **không** nằm trong tệp này (Q14 áp theo tinh thần: không có đáp án
dựng sẵn cho executor).
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 0. Thay đổi so với r3 (theo 6 lớp của review lượt 3)

Soạn r4 theo đúng thứ tự: (1) kiểm băm đầu vào bằng `sha256sum` — `VERDICT.md` lượt 3 `d3d848ed…b955`, `HINT.patch`
lượt 3 `47a2a4b9…6074`, r3 `53bf55fe…dfe1b` ở HEAD `276a65f` của nhánh `claude/spec-wp698`: khớp chỉ thị giao việc;
(2) chép r3 vào một thư mục nháp dưới tên r4, đổi đúng sáu dòng `---`/`+++` của `HINT.patch` từ tên r3 sang tên r4 bằng
`sed -E` (phần còn lại của patch giống từng byte bản gốc: so bằng `diff` sau khi bỏ các dòng ấy), rồi
`patch -p0 --fuzz=0` — rc=0, **13/13 hunk** `succeeded`, 0 fuzz (lệch dòng 9, 16, 18, 21, 25 chỉ do áp tuần tự),
2668 → 2699 dòng, 40 dòng thêm / 9 dòng xoá (`git diff --no-index --numstat`), khớp con số reviewer khai; chép bản ấy
thành r4 trong worktree; (3) với mỗi lớp, **tự liệt kê hết đường cùng cơ chế trước khi vá** — theo **chỗ gọi**, theo
**mọi mục** `DOT_BIEN`, theo **mọi chỗ dùng** `tep` — và tự đo lại trên nền `fc852ff` cùng các biến thể đo `v4_*` dựng
từ `v3_all` của phiên soạn r3, Python 3.12.3, bằng chính `_do_ban_kinh` + `_ket_luan_ban_kinh` của tệp và hàm `hang`
của Phụ lục D; mỗi biến thể chỉ khác biến thể chuẩn `v4_all` đúng một chỗ khai, và chỉ được tin sau khi `t52`, `t53`,
`t54` chưa đột biến ra `qua` trên nó; (4) sửa tiếp chỗ HINT mà phép đo cho thấy thiếu hoặc sai. Số đo: §1.10.

| lớp (hạng) | verdict lượt 3 nêu — r4 tự đo lại | r4 đổi gì | phép kiểm đóng lớp |
|---|---|---|---|
| `canh-x3-wr5-nfkc-tu-va-cham-mo-neo` (P2) | Mỏ neo một dòng của canh `x3_wr5_nfkc` có mặt 2 lần khi bảng ghi bằng literal `repr`; dò ra KHÁC; Phụ lục F `so_loi = 0`. Đo lại trên `v4_lit`: đúng như thế (9 ca `tin_dung_gia`; F bản r3 rc=0). Liệt kê thêm: viết **11 hàng r3** bằng chuỗi ba nháy (`v4_tq`) làm **55** mục lệch — gồm **20 mục cũ** trong 416 — và cái chết thành **câm** (SỐNG); **một dòng chú thích** trích nguyên văn một dòng mã (`v4_cu`) làm lệch đúng một mục cũ mà một phép đếm chỉ 54 canh để lọt (§1.10.2). | Luật mỏ neo cho **mọi** mục `DOT_BIEN` (§5); Phụ lục F bản r4 thêm phép `dem-neo` trên cả 470 mục (A5). | Phụ lục F bản r4: `v4_lit` rc=1 (1 lệch), `v4_tq` rc=1 (55), `v4_cu` rc=1 (1, mục cũ), `v4_all` rc=0 (0/470); gỡ chốt `dem-neo` ⇒ `v4_lit` rc=0; ba phản chứng của r3 vẫn đỏ đúng nhãn. |
| `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia` (P2) | Ô bộ ghi làm đúng chữ để `OSError` (tên tệp quá dài sau NFKC) thoát khỏi cửa con ⇒ `x_wr_ra_nfkc` ra `tin_dung_gia`. Đo lại trên `v4_go_wr` (gỡ khối bắt ở bộ ghi): KHÁC. Liệt kê theo chỗ gọi: **bốn** chỗ cùng cơ chế (`doc` của T1, quét `head`, vòng `main`, bộ ghi) cộng M5b; bắt `Exception` thôi thì `SystemExit` vẫn thoát (§1.10.3). | M6 (§5): mọi `BaseException` ở bốn chỗ gọi thành dữ liệu; đổi câu của M1 về ngoại lệ khác `ValueError`; nhóm J-NEM (10 dò) của Phụ lục J. | 10 dò J-NEM: `v4_all` 10/10 GIẾT; `v4_nocatch` 10/10 KHÁC; `v4_exc` (chỉ bắt `Exception`) 6 dò `thoat` KHÁC, 4 dò tự nhiên GIẾT; mỗi cây gỡ **một** chỗ gọi chỉ làm KHÁC đúng các dò của chỗ ấy. |
| `t53-thoi-gian-khong-co-tieu-chi-do` (P3) | Đồng hồ của A4-g đỏ giả khi CPU quá tải; biên "≈ 2,5 phút" ở Δ = 10 s không chứng minh được. Đo lại (§1.10.5): Phụ lục I bản r4 trên `v4_all` (sáu lượt, ba riêng, ba kèm lô 2): Δ tường 5,99–9,71 s, Δ_CPU 5,96–7,51 s, nhưng tỷ lệ r = (C56 + Δ_CPU)/C56 chỉ 1,259–1,308; hai mảnh A5 thật (nền, `v4_all`) cho tỷ lệ CPU mỗi đột biến 1,283 trong khi tỷ lệ giây tường chỉ 1,017 trên máy bận. | A4-g đổi sang **CPU**, đo theo tỷ lệ với thước của chính máy (Phụ lục I bản r4: r = (C56 + Δ_CPU)/C56 ≤ 1,35), đồng hồ thành chỉ báo; §7 đổi mô hình sang cơ sở CPU đo bằng một mảnh A5 thật và tỷ lệ lực lượng của **mảnh lớn nhất** (59/52). | `v4_all` r ≤ 1,31 ở mọi lượt, rc=0; `tv_naive` đỏ `dem` và `cpu`; `tv_cpu` chỉ đỏ `cpu` (r 1,53); `tv_cham` (ngủ) qua — khai ở §10; mảnh ước ở ngưỡng r = 1,35 là 27,9 phút, ở tỷ lệ đo được 26,0–27,1 phút (§7). |
| `ra-ha-nguon-main-bo-ghi-chua-co-o` (P3) | T5 `unlink` và dòng in SỐNG; A2 không đo thành viên ở tầng hạ nguồn. Liệt kê mọi chỗ dùng `tep` ở T5 (`exists`, `is_symlink`, `unlink`, `mkdir`, `write_bytes`, dòng in) và thành viên ngoài `R698` × năm tầng T2–T5 (§1.10.4). | T5: gọi bộ ghi **hai lần** và so dòng in (§5 M2b); nhóm J-T5 (10 dò) và J-TV (15 dò) của Phụ lục J; A2 thêm PHẢI ĐỎ Ở. | J-T5: `v4_all` 10/10 GIẾT; thiếu lần gọi thứ hai (`v4_go_hai`) ⇒ đúng 3 dò gỡ tệp cũ SỐNG; thiếu so dòng in (`v4_go_in`) ⇒ đúng 3 dò dòng in SỐNG. J-TV: `v4_all` 15/15 GIẾT; bỏ đường "mọi thành viên" ở `main` và các khúc tên tệp phủ `D698` ở bộ ghi (`v4_nomem`) ⇒ 15/15 SỐNG; nền 15/15 SỐNG. Đối chiếu: 28 dò `y_*` của reviewer trên `v4_all` ⇒ 27 GIẾT + `y_exc_shutil` SỐNG (tương đương, như verdict xếp) — §1.10.8. |
| `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (P3) | Mệnh đề đầu của A8 "Bậc hai" sai trên ứng viên r3. Đo lại trên ba cây gỡ của `v4_all` (§1.10.6): gỡ riêng miền `E698` ⇒ ba canh E r3 SỐNG lại, năm dò mở rộng vẫn GIẾT; gỡ riêng ba ô r2 ⇒ 10/10 vẫn GIẾT; gỡ cả hai ⇒ ba canh E r3 và năm dò mở rộng SỐNG, hai đối chứng GIẾT. | A8 "Bậc hai" viết lại theo ba cây ấy; giữ câu §1.9.8 mà HINT sửa. | Ba cây gỡ của `v4_all` cho đúng S/G/S (canh E r3), G/G/S (năm dò mở rộng, gồm hai canh E r2), G/G/G (đối chứng) — §1.10.6. |
| `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat` (P3) | r3 khai số ngưỡng đồng hồ riêng lẻ của `HINT.patch` lượt 2 là ba, ở 4 chỗ (HINT chỉ có hai); tên `f49_*`/`f50_*` ở §1.8.7 không tra được trong phụ lục. Đo lại: đúng (§1.10.7). | Giữ HINT (hai ngưỡng; dòng ánh xạ tên ở §1.8.7), sửa câu "là tên r1" của HINT cho đúng hiện vật. | không còn câu nào khai số ngưỡng ấy là ba (`grep -n -i` cụm từ cũ của r3 trên r4: 0 dòng); mọi tên dò/canh trong code span của r4 tra được vào Phụ lục A, C, H, J hoặc tên mục canh, trừ hai mẫu `f49_*`/`f50_*` có chủ đích và 14 tên/mẫu `y_*` tra riêng vào `evidence/` (`kiem_ten.py`, §1.10.7). |

**Chỗ `HINT.patch` lượt 3 sai hoặc thiếu so với phép đo của r4** (r4 giữ ý của mọi nhóm hunk; các điểm dưới là chỗ r4
thay hoặc thêm chữ):

1. **`canh-x3-wr5-nfkc-tu-va-cham-mo-neo`** — HINT đặt phép đếm cho **54 canh**. Đo: văn bản mới kéo cả mỏ neo của
   **mục cũ** (`v4_tq`: 20 mục cũ; `v4_cu`: một mục cũ mà không canh nào dùng chung mỏ neo), nên phép đếm phải phủ mọi
   mục; và "== 1 cho mọi mục" thì đỏ ngay trên nền, vì ba mục `bn_*` của `ops/bash_nen.py` (ngoài write set) có mỏ
   neo xuất hiện 2, 2, 3 lần — r4 so mục có tệp đích khác với số lần trên nền. HINT cũng viết "ghi mỏ neo nhiều dòng
   bằng chuỗi ba nháy nguyên văn thì cả 54 canh tự va chạm" và "tệp tạm lỗi cú pháp, canh ra KHÁC": đo trên `v4_tq`,
   va chạm **vượt** khỏi hàng được viết (24 canh r2, vốn viết bằng chuỗi thoát, cũng lệch) và tệp tạm vẫn biên dịch
   được, nên cái chết là SỐNG câm chứ không phải KHÁC ồn.
2. **`m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia`** — HINT chỉ nói ô bộ ghi và "mọi ngoại lệ". Đo: cùng cơ chế ở
   ba chỗ gọi khác (mỗi chỗ một dò răng ra KHÁC khi gỡ khối bắt ở đúng chỗ ấy), và "mọi ngoại lệ" đọc thành `Exception`
   thì `SystemExit` vẫn thoát. r4: M6, bắt `BaseException`.
3. **`t53-thoi-gian-khong-co-tieu-chi-do`** — HINT chỉ thêm một đoạn số đo vào §7 và hẹn "Revision sau"; nó không sửa
   tiêu chí A4-g, và dải 24,8–30,3 phút của đoạn ấy dùng tỷ lệ số đột biến trung bình 470/416, trong khi mảnh lớn nhất
   mang ⌈470/8⌉ = 59 so với 52 (`_phan_manh` chia theo `i % n`). r4 giữ đoạn số đo của reviewer, đổi tiêu chí và mô hình.
4. **`ra-ha-nguon-main-bo-ghi-chua-co-o`** — HINT để ngỏ "thêm ô tệp cũ tại `tep` và so dòng in, hoặc ghi vào §10" (một
   quyết định giao lại cho executor) và nói "thêm vào T-C các dò thành viên" mà không đính dò vào HINT (tám dò thành
   viên `y_*` chỉ nằm trong `evidence/` của verdict, với tên ngoài luật tên của Phụ lục D). r4 chọn ô và đính dò của
   chính nó (J-TV phủ thêm T5 và hai thành viên ở T3a/T3b mà tám dò ấy không phủ).
   HINT ghi `exists` "cùng ô bộ ghi của T4": đo, hai phép chuẩn hoá đặt ở `exists`/`is_symlink` chỉ GIẾT nhờ năm khúc tên
   mà NFKC vượt 255 byte (chúng ném `OSError`), tức nhờ M6; gỡ khối bắt ở bộ ghi (`v4_go_wr`) thì cả hai ra KHÁC
   (`t52` `tin_dung_gia`), còn dò dòng in dạng `nfkc` trên cùng cây vẫn GIẾT. Câu HINT đúng về CHỖ giết nhưng thiếu
   điều kiện: răng của hai dò ấy là khối bắt của M6 cộng các khúc vượt 255 byte, không phải một chốt riêng của T5
   (§1.10.4).
5. **`bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`** — câu HINT "gỡ riêng ba ô ngoại lệ của r2 VÀ miền `E698` cùng lúc"
   tự mâu thuẫn ("riêng" và "cùng lúc"). r4 viết lại theo ba cây gỡ đo được.
6. **`r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat`** — dòng ánh xạ của HINT viết "Tên canh trong bảng dưới là tên r1":
   r1 không có tên nào trong số ấy (`grep -c f49_nfkc_bk` trên r1 = 0); chúng là tên **mục `DOT_BIEN`** của 16 canh r1
   trong ứng viên tham chiếu IMP-R2, đặt theo mẫu tiền tố `f49_`/`f50_` mà §5 của r1 gợi ý. r4 sửa câu ấy; ánh xạ giữ
   nguyên (đo: cả 16 tên tra được qua nó).

**§12 (2) của protocol** — "một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint" — đã thoả
cho ba họ (`ra`, thời gian/tiêu chí, bậc hai). r4 **không** tự quyết Review Rescue Checkpoint; nó chỉ khai điều kiện,
bản chiếu đã đăng và cách làm đã đổi (S6).

## 0-r3. Thay đổi r2 → r3 (theo 16 lớp của review lượt 2; chữ của r3, giữ để truy dòng dõi)

Chữ của mục này là chữ r3, trừ điểm 5 của danh sách "Chỗ `HINT.patch` lượt 2 sai…" bên dưới: điểm ấy đã được sửa
theo `HINT.patch` lượt 3 (r3 đếm số ngưỡng của HINT lượt 2 là ba, thực là hai — lớp
`r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat`, §0). Mọi "§0" bên trong mục này chỉ chính mục này; "Phụ lục F" và
"Phụ lục I" bên trong mục này và ở §1.9 là **bản r3** của hai phụ lục ấy (`kiem_canh_r3.py` sha256
`1125d6bedde472465031ef5739cc552cfc33be13caa43d30f2ded4176786e988`, `chi_phi_r3.py` sha256
`db512319ac4c8b7768482699091b1e062cb50467cc6b03a31ac636b2cc6dc436`), mà r4 thay bằng bản r4 (§1.10, Phụ lục F, I).

Soạn r3 theo đúng thứ tự: (1) kiểm băm đầu vào (`VERDICT.md` lượt 2 `e281338f…3968`, `HINT.patch` lượt 2
`83b9df33…e832`: khớp), chép r2 rồi áp `HINT.patch` bằng `patch -p0 --fuzz=0` lên bản sao mang đúng tên r2 trong
patch — rc=0, **17/17 hunk**, 0 fuzz (lệch dòng chỉ do áp tuần tự), 1653 → 1708 dòng, 74 dòng thêm / 19 xoá
(`git diff --no-index --numstat`), khớp con số reviewer khai — rồi chép thành r3; (2) với mỗi lớp, **tự liệt kê
hết đường vào trước khi vá** (bài học *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*) và tự đo lại trên nền
`fc852ff`, Python 3.12.3, bằng chính script của reviewer (`extra_probes.py`, `do_reg.py`, `caseclock.py`,
`sanity_case.py`, `show.py`, `run_g.sh`) cộng script mới (Phụ lục F–I) — kể cả đo **chính hướng sửa của HINT**
trên một biến thể làm đúng chữ HINT; (3) sửa tiếp chỗ HINT mà phép đo cho thấy thiếu hoặc sai. Số đo: §1.9.

| lớp (hạng) | verdict lượt 2 nêu — r3 tự đo lại | r3 đổi gì | phép kiểm đóng lớp |
|---|---|---|---|
| `m5-ngoai-le-chi-ba-kieu` (P2) | 12 dò mở rộng tập bắt SỐNG trên `IMP-ME`. Đo lại: `cand` 12/12 SỐNG, và thêm 10/11 dò `x3_exc_*` SỐNG; biến thể theo đúng hướng HINT (miền 45 lớp) còn 7/30 SỐNG (§1.9.3). | M5b: miền `E698` = bao đóng bắc cầu của `BaseException.__subclasses__()` (118 lớp), luật cho phép đóng (bắt ⇔ lớp con của `OSError`/`SubprocessError`), hợp đồng con–cha chứa `B698`; T-E thành 30 dò; 3 canh. | `v3_exc`: 30/30 dò T-E GIẾT đúng `t53`; A8 PHẢI ĐỎ Ở `cand` (22 SỐNG) và `tv_exc` (7 SỐNG); bậc hai: §1.9.8. |
| `ra-ha-nguon-main-bo-ghi-chua-co-o` (P2) | 12 dò `x_main_ra_*`/`x_wr_ra_*` SỐNG. Đo lại: `cand` 12/12 SỐNG, và 37/40 dò T-C của Phụ lục H SỐNG ở mọi tầng T2–T5 (ba dò còn lại là đối chứng); liệt kê bằng `grep -w ra` ra sáu tầng T1–T5 (§1.9.5); thêm hai bộ đọc `argv` mà §2 của r2 chưa liệt kê (§1.9.6). | M2b: bảng tầng T1–T5 dựng bằng `grep -w ra`; ô cho tầng `main` (hai chế độ, 61 đường, kể cả đường chứa mọi `D698`) và ô bộ ghi ghi tệp THẬT; T-C thành 81 dò; 5 canh (mỗi tầng một). | `v3_ra`: 38/40 dò T-C GIẾT đúng ca đích; hai dò còn lại là tương đương (`x3_wr5_normpath`) và đối chứng KHÁC (`x3_wr_ra_lower`); A2 PHẢI ĐỎ Ở `cand` (37 SỐNG); bậc hai trên `v3_go_ra2`: năm canh tầng T2–T5 SỐNG lại, canh T1 vẫn GIẾT (§1.9.8). |
| `head-nhieu-dong-chi-tach-lf-chua-co-o` (P2) | 4 dò tách theo LF SỐNG; 4 dò `splitlines()` chỉ chết nhờ hai ô tình cờ. Đo lại: `cand`: 4 dò LF/CRLF SỐNG, 4 dò `splitlines()` GIẾT (khớp), và 23/41 dò T-B họ `head` của Phụ lục H (ngoài ba dò KHAI) SỐNG; biến thể theo đúng hướng HINT (tập `splitlines`) còn 2 SỐNG (`x3_head_us_last`, `x3_head_emsp_last`) (§1.9.4). | M1b: ô nhiễu cho mọi chuỗi của `T698` = `str.isspace` ∪ {CR LF} (30), cả hai thứ tự, hai độ dài (+120 ô); 2 canh chỉ chết nhờ các ô ấy. | `v3_head`: mọi dò `head` GIẾT đúng `t53` trừ ba dò KHAI; A1 PHẢI ĐỎ Ở `cand` (23 SỐNG) và `tv_head` (2 SỐNG); S2 đo được 121.008 / 122.268; bậc hai trên `v3_go_tach`: hai canh SỐNG lại (§1.9.8). |
| `t53-thoi-gian-khong-co-tieu-chi-do` (P2) | Không tiêu chí thời gian; bản đúng chữ mà ngây thơ chạy cửa con 63–65,5 s. Đo lại (trong tiến trình, §1.9.9): bản nhanh và bản ngây thơ **cùng 122.230 lời gọi `_van_tay`** (đếm lời gọi không phân biệt được), nhưng lời gọi băm tệp > 4 KiB là 67 so với 122.215 (nền 64); cửa con 4,32 s so với 60,77 s. | A4-g bằng Phụ lục I: đếm tất định (≤ 2 × nền) cộng tổng Δ đồng hồ của `t52`+`t53`+`t54` ≤ 10 s (min ba vòng, xen kẽ), ngưỡng suy từ trần 30 phút. | Phụ lục I trên `v3_all`: rc=0, Δ = 7,04 s, 67 lời gọi băm tệp lớn (nền 64); `cand` rc=0 (Δ = 4,94 s); PHẢI ĐỎ Ở `tv_naive` (rc=1, cả hai phép) và `tv_cham` (rc=1, chỉ đồng hồ: Δ = 15,25 s, đếm không đổi) (§1.9.9). |
| `a1-tap-dong-thieu-do-theo-nhom-unicode` (P3) | 18 dò xoá-nhóm; bản danh sách nhóm để lọt 4. Đo lại: `cand` 18/18 GIẾT, `tv_list` 14 GIẾT + 4 SỐNG (khớp); 27 nhóm có mặt trong `D698` (dẫn xuất); 9 dò cho các nhóm còn lại: 8 GIẾT + 1 đối chứng KHÁC trên `cand` (§1.9.7). | A1 (v): một dò cho **mỗi** nhóm có mặt trong `D698` (27, dẫn xuất) trong Phụ lục H; 1 canh. | `tv_list` ĐỎ ở A1 (v) (4 SỐNG); `cand` qua; canh `x_cat_mc_bk` chết đúng `t53` trên `cand`, SỐNG trên `tv_list`. |
| `phu-luc-c-dem-209-lech-221` (P3) | Tiêu đề Phụ lục C ghi 209. Đo lại: `liet_ke` = 221; chế độ `ho` cho đúng 12 dò họ `ngoai-d698`, 209 + 12 = 221. | Giữ chữ HINT. | `do_dot_bien_r2.py … liet_ke ¦ wc -w` = 221. |
| `s1-8-8-nhan-tag-sai` (P3) | "120 Cf (TAG)". Đo lại: 3.11.15: 120 = 97 TAG + 23 Cf khác; 3.12.3: 127 = 97 TAG + 30 Cf khác. | Giữ chữ HINT cho 3.11.15, thêm tách cho 3.12.3. | Vòng qua mọi điểm mã ngoài BMP (§1.9.10). |
| `tran-vong-so-10-hai-cho` (P3) | Con số trần vòng ở hai chỗ. | Giữ câu viết lại của HINT. | Quét máy trên r3 (§1.9.10): con số trục VÒNG chỉ còn ở `tran_cu`. |
| `s6-chep-thieu-quy-tac-dung` (P3) | S6 bỏ ba mệnh đề của §12; mốc "báo trước" không kiểm được. | S6 chép **nguyên văn bằng máy** 14 dòng của protocol (blob `0dedc3d9…`, sha256 đoạn trích `dc93c2a3…`); tính sẵn tỷ lệ chuyển tiếp lượt 1 → 2 (2/8 hoặc 3/8, đều < 50%); khai việc báo trước là lời khai. | So đoạn trích với `docs/PROTOCOL_DA_PHIEN.md` dòng 1043–1056 (sha256 ở S6). |
| `head-moi-vi-tri-moi-thanh-vien-qua-loi` (P3) | `objective` khai "mọi vị trí, mọi thành viên" cho `head`. | Giữ ý HINT (thu hẹp lời khai), sửa hàng bảng mà HINT làm vỡ; ba dò vào tập **KHAI** (Phụ lục D). | Ba dò SỐNG ở nền, `cand` lẫn `v3_head` (§1.9.4) — đúng trạng thái đã khai; Phụ lục D xếp chúng vào KHAI. |
| `a5-canh-khong-kiem-bang-do` (P3) | A5 chỉ so tên. | Phụ lục F so BỘ (mỏ neo, phép thay, ca đích); A5 đòi Phụ lục F ra mã 0. | Phản chứng đã chạy: canh yếu cùng tên ⇒ `lech-bo`; bộ cũ đổi ⇒ `bo-cu`; thiếu dòng ⇒ `tap-ten`; `cand` ⇒ 0 lỗi. |
| `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (P3) | Số hiệu trùng; định nghĩa nhóm để handoff; kết quả phụ thuộc định nghĩa (`nfkc` 6 so với 4, `cc` 6 so với 1). Đo lại cả hai định nghĩa: §1.9.8. | Đổi tên A1-b2; chốt định nghĩa nhóm (`cc` trừ TAB, `nfkc` trừ Zs/Zl/Zp; các giao còn lại nêu đích danh); thêm ba nhóm ô r3. | Cây gỡ theo định nghĩa chốt tái hiện đúng 4 và 1 của bảng r2. |
| `doc-bang-205-vs-211` (P3) | 205/184/138 so với tổng 211/190/144. | Giữ chữ HINT. | Cộng lại từng cột bằng máy: 211/190/144; trừ hai hàng Z (6/6/6) ⇒ 205/184/138. |
| `s11-1-thieu-cach-doc-q4-q9-q13` (P3) | Ba cách đọc chưa liệt kê. | §11.1 thành ba phần: (A) điểm r2, (B) bảng cách đọc phủ đủ 14 câu Q, (C) điểm r3. | Bảng (B) có đúng 14 dòng Q1–Q14. |
| `a4-d-khong-co-phep-do-may` (P3) | A4-d đo bằng mắt. | Phụ lục G (giao hunk `-U0` với khoảng `ast` của sáu hàm). | Phản chứng đã chạy: chạm thân `_van_tay` ⇒ rc=1; chèn ngay sau `_van_tay` ⇒ rc=1; chạm `main` ⇒ rc=1; `cand`, `v3_all` ⇒ rc=0. |
| `thu-hoi-do-khong-co-diem-dung` (P3) | `thu-hoi` "vẫn bắt buộc" mà không có điểm dừng; chưa là required check. | S7b: đỏ ⇒ DỪNG, hỏi chủ kho; `required_checks` (d) nói vì sao vẫn giữ; dẫn log chính xác. | `ops/lease_publish.py:1093` `SO_THU_HOI_KICH_HOAT = False`; trích log dòng 103–104 = mục log thô 765/767. |

**Chỗ `HINT.patch` lượt 2 sai hoặc thiếu so với phép đo của r3** (r3 giữ ý của mọi nhóm hunk; các điểm dưới là
chỗ r3 thay chữ):

1. **`head-moi-vi-tri-moi-thanh-vien-qua-loi`** — hunk `objective` chèn hai dấu xuống dòng vào **giữa một hàng
   bảng** Markdown (dòng 14–15 của bản áp không mở bằng `|`), làm vỡ bảng đầu tệp. r3 viết lại hàng `objective`
   thành một dòng.
2. **`m5-ngoai-le-chi-ba-kieu`** — miền "mọi lớp con cụ thể của `Exception` trong `builtins`, ngoài họ `OSError`"
   (45 lớp) để lọt 7/30 dò T-E trên biến thể làm đúng chữ ấy: năm lớp gốc nằm ngoài `Exception`, `ExceptionGroup`
   (hàm tạo đòi đối số nên bị loại), và lớp ngoài `builtins` (`re.error`, `json.JSONDecodeError`). r3: bao đóng bắc
   cầu của `BaseException.__subclasses__()` (118 lớp), đọc qua `getattr` để ruff không báo F821.
3. **`head-nhieu-dong-chi-tach-lf-chua-co-o`** — tập "mọi ký tự tách dòng Unicode" (tập `str.splitlines`) để lọt
   2/38 dò (`x3_head_us_last`, `x3_head_emsp_last`) trên biến thể làm đúng chữ ấy: đột biến tách theo khoảng
   trắng KHÔNG tách dòng; ba dò cùng họ khác chỉ chết nhờ ô `R698` tình cờ. r3: tập `str.isspace`
   cộng CR LF (30 chuỗi).
4. **`ra-ha-nguon-main-bo-ghi-chua-co-o`** — "thêm vào `_luoi_noi_main` … và vào kịch bản bộ ghi một đường tương tự"
   không tách hai lời gọi bộ ghi của `main` (T3a/T3b), không nói tới T5, và một đường ở bộ ghi không phủ thành viên.
   r3: bảng tầng T1–T5 cùng ô cho từng tầng (§5 M2b).
5. **`t53-thoi-gian-khong-co-tieu-chi-do`** — hai ngưỡng đồng hồ riêng lẻ của HINT (`t53` + 8 s, `t54` + 4 s) không ràng buộc `t52`; thêm một ngưỡng `t52` + 4 s mà HINT không đề nghị và nếu cùng
   chạm trần thì vượt trần 30 phút của job; số nền dẫn là của r2. Chỉ thị giao việc ưu tiên "đếm lời gọi `_van_tay`";
   đo cho thấy đếm lời gọi **không** phân biệt bản nhanh với bản chậm (cùng 122.230). r3: đếm lời gọi băm tệp > 4 KiB
   (tất định) cộng tổng Δ đồng hồ ≤ 10 s suy từ trần (Phụ lục I).
6. **`a5-canh-khong-kiem-bang-do`** và **`a4-d-khong-co-phep-do-may`** — HINT nói "nạp hai phụ lục rồi so" và "spec
   đính script như Phụ lục E" nhưng không đính script. r3 đính Phụ lục F và G, mỗi cái có phản chứng đã chạy.
7. **`bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`** — HINT đổi số hiệu nhưng để định nghĩa nhóm cho handoff. r3
   chốt định nghĩa trong đặc tả (§6 A1) bằng phép đo lại cả hai cách định nghĩa.
8. **`s6-chep-thieu-quy-tac-dung`** — HINT diễn đạt lại §12. r3 chép nguyên văn bằng máy (S6).
9. **`thu-hoi-do-khong-co-diem-dung`** — HINT dẫn "`trich-log.txt` dòng 765–767"; trong tệp trích đó là hai mục log
   thô 765 và 767, ở dòng 103–104 của tệp, thuộc job `thu-hoi` của run `36688032631`. r3 dẫn chính xác (S7b).
10. **`s1-8-8-nhan-tag-sai`** — HINT ghi đúng 97 + 23 cho 3.11.15; bảng ngay trên còn cột 3.12.3 (127 Cf ngoài BMP)
    chưa tách. r3 thêm: 127 = 97 TAG + 30 Cf khác (U+13430…U+1343F thay cho U+13430…U+13438).
11. **`s11-1-thieu-cach-doc-q4-q9-q13`** — HINT thêm ba cách đọc (Q4, Q9, Q13) rồi lại khai "không còn câu hỏi mở";
    còn Q5, Q7, Q10, Q11, Q12, Q14 chưa liệt kê. r3 dùng bảng phủ đủ 14 câu (§11.1 (B)).

**Quét cả tệp tìm chỗ cùng lớp** với điểm 1 (dòng Markdown bị hiểu sai cấu trúc), bằng máy trên bản cuối của r3:
mọi bảng có số ô đều nhau ở mọi hàng (0 hàng lệch, đếm dấu `|` ngoài code span); mọi dòng ngoài khối mã mở bằng
"số + dấu chấm + dấu cách" đều là mục danh sách có chủ đích, trừ **một** chỗ có sẵn từ r2 — ở §1.8.8, dòng mở bằng
`137.` (đuôi của câu "từ 4 tới 137") bị hiểu thành mục danh sách đánh số; r3 nối nó vào dòng trên, không đổi chữ.

## 0-r2. Thay đổi r1 → r2 (theo tám lớp của review lượt 1; chữ của r2, giữ để truy dòng dõi)

Soạn r2 theo đúng thứ tự: (1) chép r1 thành r2 rồi áp `HINT.patch` của reviewer: `sed -E` đổi mọi tên tệp
`ci-g5-cong-cu-va-tiep-r1.md` trong patch thành `ci-g5-cong-cu-va-tiep-r2.md`, rồi `patch -p0 --fuzz=0`
— rc=0, 16/16 hunk, không `.rej`, 26 dòng thêm / 23 dòng xoá (khớp số reviewer ghi); (2) với mỗi lớp,
**tự liệt kê hết đường vào trước khi vá** (bài học *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ
ba"*) rồi đo; (3) sửa tiếp phần HINT mà phép đo cho thấy chưa đủ hoặc sai. Mọi phép đo của r2 chạy
lại **trọn** sau khi container khởi động lại lúc khoảng 22:16Z 30-09; kết quả đo trước lúc ấy bị bỏ.

| lớp (hạng) | r1 sai ở đâu — đo được | r2 đổi gì | phép kiểm đóng lớp |
|---|---|---|---|
| `tran-cu-adr-0043-da-bi-thay` (P2) | Năm chỗ dẫn trần 2 vòng của ADR-0043; `nang_tran` ghi `tran_cu: 2` với `truc: vong_review`; S6 viết "lượt review thứ ba" và bỏ quy tắc không hội tụ. ADR-0048 (Accepted 2026-09-12) đã thay con số trục VÒNG cho đặc tả đóng băng từ mốc ấy; số 2 của tiền lệ `wp461-…-1g9` là trục LỜI GỌI (`truc: loi_goi`, đo lại bằng `grep -n`). | Header `ngưỡng review`; khối `nang_tran` (`tran_cu` theo ADR-0048, thêm `tran_cu_nguon`, `hieu_luc`, `ghi_chu_so_cu`; `truc` giữ `vong_review`); đoạn dưới khối; S6 chép đúng hai quy tắc dừng của protocol §12 (dòng 1047, 1054–1055) và nêu hệ quả với lớp kế thừa; §11 Q5 và dòng "bản nháp đề 2 vòng". Con số chỉ được chép đúng một chỗ (`tran_cu`), còn lại trỏ ADR-0048 (luật "một chỗ ở" của chính ADR ấy). | `grep -n -E` trên r2 với các mẫu `tran_cu`, `ADR-0043`, `ADR-0048`, `2 vòng`: mọi chỗ nêu trần trục VÒNG trỏ ADR-0048; ADR-0043 chỉ còn được dẫn cho ba trục, luật `nang_tran` và lời khai cưỡng chế đã bị ADR-0048 sửa. |
| `ra-thieu-hang-chuan-hoa-lop-b` (P2) | `ra` là bộ đọc thứ tư của `_doc_che_do` mà §2 lớp B bỏ; dò `ra` × {NFKC, Cf, TAB, bỏ `/` cuối, bỏ `./` đầu} sống trên nền và trên IMP-MIN. | `ra` vào lớp B như ba bộ đọc kia (miền M1 áp cho `ra` = `a/b`); M2 thêm ô cấu trúc cho từng phép; 6 canh `ra`. Liệt kê **mọi** bộ đọc cùng họ (§2, "bộ đọc"): bốn trong lớp B, hai ngoài lớp B (đầu tệp mảnh của `_gom_manh`, `CONG_CU_TEST_TIEN_TRINH`) được đo và ghi nợ. | T-C của Phụ lục C: nền 40 SỐNG · IMP-MIN 38 · IMP-GEN 24 · IMP-R2F 0 (§1.8.4). |
| `luc-luong-chi-quet-truc-khong-quet-tich` (P2) | M3 nói "quét trọn miền" nhưng miền là ba trục riêng; ba vị từ hai biến sống trên nền, IMP-MIN, IMP-GEN. | M3 thêm 48 kịch bản tích biên; lời khai đổi thành "trục trọn cộng tích biên"; T-D có 12 dò trong Phụ lục C (7 của reviewer, 5 mới chỉ lệch nền ở điểm có ≥ 2 toạ độ khác 0), cộng 5 canh D của r1; 4 canh D tích. | T-D: nền 11 SỐNG · IMP-MIN 8 · IMP-GEN 8 · IMP-R2F 0; `t54` 1,89 → 2,44 s (Python 3.12.3). |
| `a1-khong-do-vi-tri-thanh-vien` (P2) | A1 chỉ giết 9 dò theo tên phép; M1 đòi "đầu, giữa, cuối" và "dẫn xuất theo lớp" nhưng không tiêu chí nào đo. | M1 thành **miền dẫn xuất** `D698` × mọi vị trí; A1 thành **tập dò đóng có tên** T-B (vị trí đầu/cuối/giữa, **từng chỉ số**, thành viên Cf/NFKC, Zs, Cc, dấu kết hợp, strip hẹp) kèm phép PHẢI ĐỎ Ở trên IMP-MIN và IMP-GEN; bậc hai theo nhóm điểm mã. Tái hiện số reviewer trước khi đổi: 47 dò anh em SỐNG nền 43 · IMP-MIN 28 · IMP-GEN 7 (§1.8.2). | T-B: nền 149 SỐNG · IMP-MIN 133 · IMP-GEN 101 · IMP-R2F 2 (đúng hai dò tương đương). |
| `khai-khong-do-duoc-nhung-do-duoc` (P2) | §4/§10 khai F46 "kiểu ngoại lệ" là không dựng được phép đo, §2 khai Zs "KHÔNG ĐO"; cả hai đo được. | Tập bắt ngoại lệ của `_van_tay` đo được và vào **M5** (3 ô ngoài tập bắt, kỳ vọng lọt); Zs ngoài ASCII vào M1; §2/§4/§10 mang trạng thái đo, không còn "KHÔNG ĐO" nào đo được mà chưa đo. Phần HINT ghi hai mục này thành nợ (`lop-b-ngoai-ba-phep-wp698`, `f46-ngoai-le-van-tay-wp698`) bị r2 **thay**: đo được và sống thì vào mục tiêu. | T-E: nền 5 SỐNG · IMP-R2F 0 SỐNG, 5/5 dò mở rộng GIẾT; dò Zs trong T-B. §10 chỉ còn mục có lý do vì sao không đo. |
| `muc-tieu-m1-m4-cau-chu-thieu-chinh-xac` (P3) | M2 "cả normpath lẫn expanduser đều đổi" mâu thuẫn ví dụ; ô `~/x` phụ thuộc môi trường; M1 không nói cách đặt ký tự vô hình vào nguồn; M4 không có tiêu chí; "đầu, giữa, cuối … đang bị từ chối" không thoả được cho `head` × TAB. | M2: mỗi phép một ô riêng; `HOME`/`USERPROFILE` ghim trong phạm vi quét, đo lại bằng `setpriv` (§1.8.5); M1: `chr()` và phép đếm ký tự nguồn sau khi ghi; M1 dùng kỳ vọng của oracle nên không còn điều kiện "đang bị từ chối"; A7 cho M4. | Đọc M1/M2/M4 và A7; §1.8.5. |
| `tieu-chi-nghiem-thu-thieu-chinh-xac` (P3) | A5 chỉ đếm; A4-b không nói so theo gì; A4-e không có script; "ĐỎ KHI" trộn hai loại; không ghi phiên bản Python; ":2292" không phải nhánh `giet_that`. | A5 kiểm tên và số = 459; A4-b so đa tập (mã, thông điệp) bằng ruff 0.15.15 (đo được bản ghim); A4-e = Phụ lục E; mỗi tiêu chí tách **ĐẠT KHI** với **PHẢI ĐỎ Ở**; Python 3.12 bắt buộc, 3.11 đo thêm; :2318 là nhánh `giet_that`, :2292 là dòng `def _chay_1_ca` (verdict ghi "docstring" — lệch một dòng); A4-f đo bằng `git diff --name-only` và đầu ra để ngoài cây. | §6; §1.8.7 (A4 đo trên nền và IMP-R2 trong một lệnh). |
| `nghia-vu-land-thieu-dinh-nghia-tac-nghiep` (P3) | Q9 chưa có phép thử tác nghiệp; (d) `thu-hoi` còn bắt buộc hay không; `ci_budget` chỉ đếm PR thi công mà không nói; `land_obligations` 7 thiếu nơi ghi, 8 thiếu chủ thể. | `required_checks` (c): định nghĩa ba điều kiện trên log, neo trích log **trong kho**; Q9 chỉ miễn (c), (d) vẫn bắt buộc (§11.1 điểm 6); `ci_budget` khai phạm vi sổ; `land_obligations` 7 ghi vào `no_con_mo`, 8 do người chủ kho chỉ định. | Đọc `required_checks`, `ci_budget`, `land_obligations`, §11.1. |

**Số phận từng nhóm hunk của `HINT.patch`** (năm nhóm, mở bằng `# lop: …`):

- `tran-cu-adr-0043-da-bi-thay` (6 hunk): giữ ý, viết lại. HINT chép con số trần mới vào header, khối,
  S6 và Q5; ADR-0048 đòi con số chỉ có một chỗ ở, nên r2 chỉ chép nó vào `tran_cu` (trường ADR-0043
  bắt buộc) và trỏ ADR-0048 ở mọi chỗ khác. Chú thích YAML `# trục VÒNG …` của HINT trong khối
  `nang_tran` được thay bằng trường `tran_cu_nguon`: lease phải chép nguyên khối, và chú thích YAML là
  thứ dễ rơi khi chép hay khi nạp lại bằng bộ phân tích YAML.
- `khai-khong-do-duoc-nhung-do-duoc` (3 hunk): **thay**. HINT ghi hai đường sống thành nợ
  (`lop-b-ngoai-ba-phep-wp698`, `f46-ngoai-le-van-tay-wp698`); r2 đo lại, cả hai sống, nên vào mục tiêu
  (M1, M5). Dòng §10 *"casefold trên dạng fullwidth: chưa đo"* của HINT được đo: đối chứng
  `s_bk_casefold` bị giết trên nền (§2).
- `muc-tieu-m1-m4-cau-chu-thieu-chinh-xac` (2 hunk): giữ ý `chr()` cộng phép đếm sau khi ghi. Câu
  *"Ô expanduser chỉ có nghĩa khi HOME (POSIX) hoặc USERPROFILE (Windows) được đặt"* rộng hơn phép
  đo: chạy bằng root (có trong passwd), bỏ `HOME`, vẫn ra `/root/x` (§1.8.5); điều kiện đúng là "UID
  không có trong passwd **và** không có `HOME`". A7 giữ ý, thêm mẫu `grep` và điều kiện ĐỎ đo được.
- `tieu-chi-nghiem-thu-thieu-chinh-xac` (3 hunk): giữ `:2318`, giữ so ruff theo (mã, thông điệp), giữ
  kiểm tên ở A5 (thêm số 459). Câu Python 3.12 dẫn số của ứng viên reviewer; r2 thay bằng phép đo của
  chính nó. "Script đếm phải được đính vào một phụ lục" ⇒ Phụ lục E.
- `nghia-vu-land-thieu-dinh-nghia-tac-nghiep` (2 hunk): giữ định nghĩa "đỏ vì hết trần", neo vào
  trích log **trong kho**; bỏ hai thời lượng 66,5 và 83,3 phút vì trích log đã bỏ dấu thời gian nên r2
  không kiểm được (KHÔNG ĐO ĐƯỢC); thêm "Q9 không miễn (d)"; danh sách nợ ở mục 7 đổi theo mục
  tiêu mới; giữ phạm vi sổ CI và chủ thể mục 8.

## 1. Đo lại F48–F50: trên nền `fc852ff`, và trước đó trên `423b4ba`

§1.1–§1.7 là phép đo của lượt soạn r1, giữ nguyên chữ; chỗ nào r2 đo lại hoặc đo thêm thì ở §1.8 (giữ nguyên
chữ của r2); chỗ nào r3 đo lại hoặc đo thêm thì ở §1.9 (giữ nguyên chữ của r3); chỗ nào r4 đo lại hoặc đo thêm thì
ở §1.10. Ngoại lệ duy nhất của "giữ nguyên chữ" là ba chỗ `HINT.patch` lượt 3 sửa và r4 giữ (đoạn ánh xạ tên ở §1.8.7,
dòng `v3_go_exc` ở §1.9.8, câu "hai ngưỡng" ở §1.9.9) — kê ở §0.

Số dòng trích trong §1 là số dòng trên blob `9edea6b1629b…`, blob chung của hai nền.

### 1.1 Dụng cụ, mốc, và vì sao không tin lời thuật lại

Verdict lượt 22 review commit `8d7faef`. Đó là commit merge của `5a071b8` ("lượt 21 của phiên
này", tức phiên `session_01VYtkBy…`) với `cc78b33`. Đo lúc 15:11:55Z 30-09 trên clone sạch đã
fetch đủ 458 ref từ GitHub: `git cat-file -t 8d7faef` và `git cat-file -t 5a071b8` đều báo
*"Not a valid object name"*, còn `cc78b33` có mặt. Blob của năm tệp write set #668 ở `cc78b33`
**bằng** blob ở `423b4ba` và `fc852ff` (`ops/cong_cu_test.py` cùng là `9edea6b1629b…`). Nói cách
khác, mã được review ở lượt 22 = mã trên master **cộng** các thay đổi của `5a071b8`, và các thay
đổi ấy **không có trong kho**. Vì vậy mọi phát hiện của lượt 22 đều phải đo lại, không chép sang.

Bản sao tạm được dựng bằng `git clone --no-checkout`, rồi `checkout` đúng nền, ghim
`core.abbrev 7`, đặt `PYTHONDONTWRITEBYTECODE=1`, và trỏ `TMPDIR` vào scratch. Sau mọi lượt đo,
`git status --short --ignored` của bản sao rỗng. Môi trường: Python 3.11.15, PyYAML 6.0.1,
`_CO_SYMLINK=True`.

Gate nền chạy bằng `CONG_CU_TEST_BAN_KINH=manh python3 ops/cong_cu_test.py`. Trên `fc852ff`,
15:32:18Z–15:35:28Z 30-09; trên `423b4ba`, 14:49:16Z–14:52:34Z. Cả hai lượt đều ra
`cong_cu_test: 55/55 đạt; tổng=56, bỏ qua=1, tiền kiểm bỏ qua=0` và `SỐ LIỆU: ca=56 · đột
biến=416 (giao mảnh) · lỗi đột biến=0 · tiền kiểm bỏ qua=0 · cổng cây thật=ĐẠT`, rc=0. Ca bị bỏ
qua là `t2`, vì container thiếu `jsonschema`.

Phép đo đột biến dùng **chính** `_do_ban_kinh` và `_ket_luan_ban_kinh` của tệp (Phụ lục A),
nên không có đường phân hạng thứ hai. Mỗi đột biến dò được đăng ký đúng hình dạng sáu trường
`("ops/cong_cu_test.py", tìm, thay, "TEP_TEST", _KEM_TEP_TEST, <ca đích>)`, rồi chạy **trọn 56
ca** trên cây tạm riêng. 30 dò được chia cho 4 tiến trình theo chỉ số mod 4, trên container 4
lõi.

- Lượt trên `fc852ff`: 15:35:28Z–15:39:32Z 30-09, script `do_dot_bien.py` sha256
  `3d53b90d16e5fcfb138cff9a1c89a674027d84bca339abcb3e992921532d3d53` (bản trong Phụ lục A),
  mỗi dò mất 28,3–35,4 s.
- Lượt trên `423b4ba`: 14:58:41Z–15:02:39Z, script sha256 `225ca4ef…ae69`, mỗi dò mất
  28,1–32,7 s. Bản script này chỉ khác bản Phụ lục A ở hai dòng chữ: dòng đầu docstring và một
  chú thích từng ghi cứng `423b4ba`. Bảng `P` giống hệt.
- **Hai lượt cho cùng phân hạng ở 30/30 dò.** Mọi mỏ neo xuất hiện đúng 1 lần. Ở cả 30 dòng,
  `t2` là `bo_qua`, và ngoài các ca ghi trong bảng không ca nào chết.

Mức mã đo riêng bằng `do_f49_ma.py` (Phụ lục B). Trên `fc852ff` lượt đo chạy lúc 15:35:28Z với
script sha256 `6707002f3c37cfdfa5cbdf308be288dd9fb40472d8dc855d7cf52c12b2ff0473`. Đầu ra có
sha256 `42ca657c282ec38b87170a3b1b98be32b1affd68169bde375540e5d7da1d741d`, **trùng từng byte**
với lượt 15:03:47Z trên `423b4ba`; bản script ở lượt ấy chỉ khác bản này ở docstring. Mọi ký tự
ngoài ASCII trong hai script đều dựng bằng `chr()`, nên không có chuỗi thoát nguyên văn nào đi
qua lớp vận chuyển.

### 1.2 F48 — chốt AST của registry năng lực: **KHÔNG TÁI HIỆN nguyên văn**; lớp gốc (e) **TÁI HIỆN**

- **Đối tượng của F48 không tồn tại trên nền.** Ở cả hai nền, registry năng lực là một phép
  **hiệu hai ảnh runtime**: `_TRUOC_NANG_LUC = dict(DOT_BIEN)` ở :7422, đăng ký có điều kiện ở
  :7424–:7453, `_TEN_NANG_LUC` ở :7456, và `t52` so `kq["nang_luc"]` (:7889) với oracle `_TEN_SL`
  (:7627). Không có chốt AST nào nhắm vào cửa sổ ấy. Các đường lọt mà verdict nêu (danh sách cho
  phép áp lên tên thuộc tính, danh sách `dk` thiếu `ast.TryStar`, hàm định nghĩa trong cửa sổ
  nhưng gọi sau cửa sổ) đều là lỗ của một chốt do `5a071b8` thêm vào. Chốt ấy không có trong kho,
  nên các đường lọt này **không thể tái hiện** ở đây.
- **Lớp gốc thì tái hiện, và ở dạng RỘNG hơn.** Trên nền không có gì canh phía ngoài cửa sổ, nên
  *mọi* hình dạng đều lọt. Đó chính là "đường (e)" mà verdict lượt 21 của #668
  (`ops/reviews/ci-g5-cong-cu-chia-manh-r1-review-21-claude-verdict.md`, sha256
  `25674d47095f…f07270`, mục H6) xếp là **giới hạn thiết kế do chủ kho chốt ở F39** ("không nạp
  lại, không mô phỏng"), **không phải finding**. Đo: dò đối chứng `c48_trong_cua_so` bị `t52`
  giết, bán kính 1/56. Tám dò ngoài cửa sổ **sống qua cả 56 ca**. Bảy dò trong số đó có phần tác
  dụng nằm SAU dòng quan sát: sáu hình dạng verdict lượt 22 nêu, cộng một dạng gán thẳng. Dò thứ
  tám đặt TRƯỚC ảnh `_TRUOC_NANG_LUC`.
- **Lỗ đang tiềm ẩn, chưa bị dùng.** Đếm bằng AST mọi phép gán chỉ số vào `DOT_BIEN` và mọi lời
  gọi phương thức đổi dict trên `DOT_BIEN` (`pop` `update` `setdefault` `clear` `popitem`), ở mọi
  phạm vi. Trên `fc852ff`, lúc 15:40:23Z, được 9 chỗ: 2 chỗ trước cửa sổ (:2256, :2262, vô điều
  kiện), 7 chỗ trong cửa sổ, **0 chỗ sau mốc :7456**. Kết quả khớp lời khai H4 của lượt 21.
- **Quyết định chủ kho (Q1):** F48 không vào r1. Lớp gốc ghi nợ `registry-nang-luc-ngoai-cua-so`;
  muốn đóng thì mở packet riêng.

### 1.3 F49 — chuẩn hoá đầu vào của bộ đọc: mức mã **KHÔNG TÁI HIỆN**; khe đo **TÁI HIỆN**

- **Mức mã (Phụ lục B).** `_doc_che_do` (:7461–:7487) từ chối **12/12** giá trị thử chứa ký tự
  fullwidth, dạng tương thích NFKC hoặc ký tự Cf, và mỗi giá trị bị từ chối với đúng thẻ.
  - Năm giá trị `CONG_CU_TEST_BAN_KINH`: `manh` bản fullwidth, `manh` cộng U+200B ở cuối,
    U+FEFF ở đầu, U+2060 ở giữa, U+00AD ở giữa. Cả năm ra `[C-ban-kinh]`.
  - Bảy giá trị `CONG_CU_TEST_MANH`: chữ số fullwidth, gạch chéo fullwidth, toàn bộ fullwidth,
    chữ số mũ U+2078, U+200B ở cuối, U+200D ở giữa, U+200E ở đầu. Cả bảy ra `[C-hinh-dang]`.
  - Hai giá trị có TAB (`manh` cộng TAB; `3` TAB `/8`) cũng bị từ chối đúng thẻ.
  - `_van_tay` (:7495–:7505) trả `None` cho 5/5 đầu HEAD không chuẩn (một chữ số fullwidth, toàn
    bộ fullwidth, U+200B ở cuối, U+FEFF ở đầu, U+2060 ở giữa) và cho TAB giữa chuỗi; với đầu HEAD
    hợp lệ thì trả đúng hex.

  Vậy lời *"giá trị NFKC/fullwidth được nhận là hợp lệ"* **không đúng với hai bộ đọc này trên
  nền**.
- **Oracle độc lập đồng ý với mã** trên cùng các giá trị: 15/15 giá trị chế độ (so sau vòng
  JSON, giống cách `t53` so), 7/7 giá trị HEAD, 2/2 giá trị TAB. Vì vậy thêm ô **không** đòi đổi
  `_mong_che_do` (:8052) hay `_mong_git` (:8080). Lần đo đầu so không qua vòng JSON và thấy lệch ở
  ba ô `ra`; đó là tạo tác của rig (tuple so với list), không phải lệch thật, và đã đo lại.
- **Khe đo thì tái hiện.** Chín đột biến chuẩn hoá (ba bộ đọc × ba phép) **sống qua cả 56 ca**
  (bảng §1.6). Các ô hiện có của `t53` (`_luoi_che_do` :8040, 200 ô; `_luoi_git` :8069, 57 ô;
  `bang_env` của `_in_tu_kiem_che_do` :8093) không có ô nào ở dạng NFKC-khác-chính-nó, chứa ký tự
  Cf, hay chứa TAB. Hai dò đối chứng bị giết đúng `t53`, bán kính 1/56: `mh.strip()` bị ô `" 0/8"`
  bắt, `head.lower()` bị các ô `A`/`F` bắt.
- **TAB là phần của F46.** Verdict lượt 22 ghi F46 **ĐÃ ĐÓNG trên `8d7faef`**, nhưng trên nền ba
  dò TAB **sống**. Tức bản vá F46 của `5a071b8` không có trên master. TAB được gộp vào lớp B (Q3).

### 1.4 F49-P3 — `ra` không có ô normpath/expanduser: **TÁI HIỆN**

`_doc_che_do` trả `ra` **nguyên văn**: `a/./b//c`, `~/x` và `a/../b` ra khỏi hàm không đổi (Phụ
lục B). Đó là hành vi đúng. Nhưng hai dò `return "manh", (k, n, os.path.normpath(ra))` và
`… os.path.expanduser(ra)` đều **sống qua cả 56 ca**. Lý do: mọi ô `ra` hiện có (`x`, `y z`,
` y `, hai dấu cách, `a/b c/manh 3.txt`) đều giữ nguyên dưới hai phép này. Hai dò đối chứng thì
chết: `ra.strip()` bị `t53` giết, bán kính 1/56; `os.path.abspath(ra)` bị cả `t53` lẫn `t54` giết,
bán kính 2/56.

### 1.5 F50 — điểm lực lượng của nhánh mảnh: **TÁI HIỆN**, và rộng hơn lời thuật

Nhánh mảnh của `main` (:8227–:8248) rẽ về "nền đỏ" ở :8231 qua điều kiện
`if hong or tien_kiem_bo_qua:`. Các kịch bản mảnh của `t54` (:6884; cửa `--tu-kiem-main` :7905)
chỉ có:

- `bo_qua` ∈ {0, 1};
- `hong` ∈ {0, 1} (`manh_ca_do`, `manh_ca_loi`);
- `tien_kiem_bo_qua` có đúng một phần tử (`manh_tk_batch` hoặc `manh_tk_alias`); không kịch bản
  nào có cả hai.

Đo: `len(bo_qua) == 2` **sống**, đúng như F50. Bốn dò cùng lớp mà verdict **không** nêu cũng
**sống**: `len(bo_qua) >= 2`, `len(bo_qua) == len(CA) - 1`, `len(hong) == 1` (thay cho `hong`), và
`len(tien_kiem_bo_qua) == 1`. Dò đối chứng `len(bo_qua) == 1` bị `t54` giết, bán kính 1/56.
Verdict lượt 22 ghi lớp "lực lượng nhánh mảnh (F47)" chỉ còn hở ở điểm bằng-2 trên `8d7faef`,
nhưng `>= 2` sống trên nền. Nội dung F47 không có trong kho nên không đối chiếu được (§10).

Chi phí đo lúc ~14:58Z trên `423b4ba` (cùng blob): `t54` chạy 2,23 s; cửa `--tu-kiem-main` chạy
219 kịch bản trong 2,17 s, tức khoảng 10 ms mỗi kịch bản. `t52` chạy 4,1 s; `t53` 0,39 s.
`len(CA)` = 56.

### 1.6 Bảng tái hiện (nền `fc852ff`, 15:35:28Z–15:39:32Z; trùng phân hạng 30/30 với lượt `423b4ba`)

"Sống" nghĩa là ca đích vẫn `qua` và **không ca nào trong 56 ca chết**; `_ket_luan_ban_kinh` in
*"đích … vẫn XANH ⇒ đột biến không giết được gì"*. "Giết" nghĩa là `giet_that`, tức
`TinHieuChotCa` mang đúng tên ca đích.

| lớp | dò | ca đích | kết quả trên nền |
|---|---|---|---|
| A (F48) | `c48_trong_cua_so`, đối chứng: đăng ký có điều kiện TRONG cửa sổ | `t52` | giết · 1/56 |
| A (F48) | `e48_sau_cua_so`: đăng ký có điều kiện sau dòng `_TEN_NANG_LUC` | `t52` | **sống** |
| A (F48) | `e48_get_self`: `DOT_BIEN.get.__self__[…] = …` sau cửa sổ | `t52` | **sống** |
| A (F48) | `e48_keys_self_pop`: `DOT_BIEN.keys.__self__.pop(…)` sau cửa sổ | `t52` | **sống** |
| A (F48) | `e48_globals`: `globals()["DOT_BIEN"][…] = …` sau cửa sổ | `t52` | **sống** |
| A (F48) | `e48_ham_trong_goi_sau`: hàm định nghĩa trong cửa sổ, gọi sau | `t52` | **sống** |
| A (F48) | `e48_trystar`: đăng ký trong `try` / `except*` sau cửa sổ | `t52` | **sống** |
| A (F48) | `e48_gan_lai_moc`: đăng ký trong cửa sổ, rồi gán lại `_TEN_NANG_LUC` | `t52` | **sống** |
| A (ngoài lời thuật) | `e48_truoc_anh`: đăng ký có điều kiện TRƯỚC `_TRUOC_NANG_LUC` | `t52` | **sống** |
| B (F49) | `e49_nfkc_bk` · `e49_nfkc_mh` · `e49_nfkc_head` | `t53` | **sống** ×3 |
| B (F49) | `e49_cf_bk` · `e49_cf_mh` · `e49_cf_head` | `t53` | **sống** ×3 |
| B (F46-TAB) | `x46_tab_bk` · `x46_tab_mh` · `x46_tab_head` | `t53` | **sống** ×3 |
| B | `c49_strip_mh` · `c49_lower_head`, đối chứng | `t53` | giết · 1/56 ×2 |
| C (F49-P3) | `e49_ra_normpath` · `e49_ra_expanduser` | `t53` | **sống** ×2 |
| C | `c49_ra_strip`, đối chứng | `t53` | giết · 1/56 |
| C | `c49_ra_abspath`, đối chứng | `t53` | giết · 2/56 (thêm `t54`) |
| D (F50) | `e50_bang_2`: `len(bo_qua) == 2` | `t54` | **sống** |
| D (F47-hình) | `e50_tu_2`: `len(bo_qua) >= 2` · `x50_bang_n_tru_1`: `len(bo_qua) == len(CA) - 1` | `t54` | **sống** ×2 |
| D (ngoài lời thuật) | `x47_hong_bang_1`: `len(hong) == 1` · `x47_tk_bang_1`: `len(tien_kiem_bo_qua) == 1` | `t54` | **sống** ×2 |
| D | `c50_bang_1`, đối chứng: `len(bo_qua) == 1` | `t54` | giết · 1/56 |

Tổng: **30 dò = 24 sống + 6 đối chứng bị giết**. Theo lớp: A 8 sống, B 9 sống, C 2 sống,
D 5 sống. Mỏ neo và phép thay nguyên văn của từng dò nằm trong bảng `P` của Phụ lục A.

### 1.7 Phát hiện phụ, ngoài F48–F50

- `_so_tien_trinh_ban_kinh` (:7082–:7097) đọc `CONG_CU_TEST_TIEN_TRINH` bằng
  `tho.strip().isdigit()` rồi `int(tho)` (:7094). Đo ở Phụ lục B:
  - `１２` (fullwidth) ra **12**; chữ số Ả Rập U+0663 ra **3**;
  - chữ số mũ U+00B2 làm hàm ném `ValueError: invalid literal for int()`, vì `isdigit()` nhận mà
    `int()` từ chối;
  - các giá trị ASCII `3` và ` 3 ` ra 3; chuỗi rỗng và `3` cộng U+200B ra 1.

  `ci.yml` và `ci-dot-bien-du.yml` không đặt biến này (đếm được 0 lần). Đây là chỗ nhận fullwidth
  **ở mức mã**, nhưng không thuộc F49 nguyên văn. Quyết định chủ kho: ghi nợ
  `so-tien-trinh-nhan-fullwidth` (Q2), và A4-d cấm đổi thân hàm này trong r1.
- Ruleset `bao-ve-cong-dang-lease` liệt kê context `gate-cong-cu-gop (ubuntu-latest)` **hai lần**
  (đọc lúc 14:44:35Z và 15:40Z). Chỉ ghi lại; không thuộc packet.
- `ci.yml` trên nền chỉ thêm `windows-latest` vào ma trận khi sự kiện là `workflow_dispatch` hoặc
  PR mang nhãn `windows` (`chuan-bi.outputs.os`). Lượt hậu-merge `36696528580` trên master có 14
  job, **toàn bộ ubuntu**. Vì vậy câu *"Trên master, matrix `os` nhân đôi số mảnh (ubuntu +
  windows)"* trong đặc tả mẹ không khớp `ci.yml` hiện hành. Chủ kho quyết không chạy Windows (Q8).

### 1.8 Đo cho r2 (30-09, sau review lượt 1)

#### 1.8.1 Giàn đo

- **Khởi động lại.** Container của phiên soạn khởi động lại lúc khoảng 22:16Z 30-09, giữa lúc đo.
  Mọi kết quả trước lúc ấy bị **bỏ**; mọi số dưới đây đo lại từ đầu trong khoảng
  22:17Z–03:08:29Z 01-10. Trước khi đo lại: kiểm lại băm của `VERDICT.md` và `HINT.patch`, dựng lại r2 từ
  r1 cộng HINT (ra cùng sha256 với bản dở), so byte các cây đo với nguồn của chúng.
- **Lượt bị cắt.** Lệnh nền nối chuỗi các lô đo bị công cụ dừng ở trần 2 giờ của một tác vụ nền lúc
  khoảng 01:30:54Z 01-10, giữa lượt Phụ lục C trên Python 3.12.3: 156/221 dò đã có kết quả. Mọi tiến
  trình con chết theo; 0 zombie (đo bằng `ps`). Mỗi dòng jsonl chỉ được ghi khi một dò đã đo xong, nên
  không có kết quả dở; 65 dò còn lại chạy tiếp từ 01:39:51Z trên cùng cây, cùng script. Bốn vòng chờ
  của chính phiên này (đợi dòng kết thúc của lô bị cắt) được dừng tay; A5 không chạy theo chuỗi ấy mà
  được khởi động riêng. Một lượt A5 trên IMP-R2F bị **dừng tay** sau 1,5 phút (01:49:22Z–01:51Z) khi
  soát thấy bảng canh thiếu ba họ của §2 (kill cả nhóm tiến trình; 0 tiến trình sót, 0 zombie, không
  tệp mảnh nào được ghi); A5 chạy lại trọn trên IMP-R2G.
- **Cây đo.** (1) **nền**: `git clone --no-checkout` từ kho cục bộ rồi checkout `fc852ff`, ghim
  `core.abbrev 7`; `git hash-object ops/cong_cu_test.py` = `9edea6b1629b46f27758b2073e74210dc73495b7`.
  (2) **IMP-MIN**, **IMP-GEN**: hai ứng viên tham chiếu của reviewer lượt 1, chép từ sandbox của
  reviewer và so byte bằng `cmp` với bản gốc (sha256 `ops/cong_cu_test.py`: IMP-MIN `4739e36f…`,
  IMP-GEN `c7ae1fe0…`). Đó là đúng hai cây reviewer đã đo (dựng lúc 16:03Z); `build_imp.py` hiện có
  của reviewer dựng ra bản khác chúng chỉ ở phần gỡ nhóm bằng biến `GO698` của M3, không đổi hành
  vi khi biến ấy không đặt. (3) **Ba đời ứng viên tham chiếu** do phiên soạn r2 dựng (§1.8.7), mỗi đời một sha256 của
  `ops/cong_cu_test.py`: **IMP-R2** `142d0230…6ac96` — chạy phần lớn phép đo Python 3.11.15 (tập đóng
  209 dò, 40 canh, đột biến cũ, bậc hai trên **IMP-R2-GO** `cd66682b…d3e0`); **IMP-R2F**
  `0fda32da…62b5c3` = IMP-R2 + `N698` + canh `m_cc_head` thay `m_cc_mh` — chạy tập đóng **trọn 221
  dò** bằng Python 3.12.3, 12 dò nhóm ngoài `D698`, 40 canh; **IMP-R2G**
  `485eb176593838e1938947d789902722240b4cd6e445c492afa2bcca514fccf7` = IMP-R2F + 3 hàng canh
  (`m_co_bk`, `q_cf_mid_ra`, `m_cf_tag_ra`) + một hàm gián tiếp `_n698()` (hành vi y hệt khi không gỡ
  nhóm) — **ứng viên cuối**: A5 trọn, A4 và thời gian đo trên nó; bậc hai cho ba canh mới trên
  **IMP-R2G-GO** `255cc8c8…9b01`. Kết quả mang từ đời trước sang đời sau được vì: (a) đời sau chỉ
  **thêm** ô hoặc hàng canh, và một dò tiêm (Phụ lục C) chỉ chạy đúng phép thay của nó, không đọc các
  hàng canh khác; (b) `N698` không thuộc nhóm bậc hai nào và không phép biến đổi nào của các canh trong
  bảng bậc hai đổi U+4E00, U+E000, U+0378. Biến thể `…-GO` khác đời gốc của nó ở hằng `_GO698` (đọc
  biến `GO698`) và bảng lọc nhóm của `D698` — mã chết khi `_GO698` rỗng.
- **Môi trường.** `PYTHONDONTWRITEBYTECODE=1`; `TMPDIR` trong scratch; container 4 lõi; mỗi bước
  tối đa 4 tiến trình và mọi tiến trình con được `wait` (`run4.sh`). Zombie: 0 trước mỗi lô và 0 sau mỗi lô, trừ một lần đếm ra 3 đúng lúc lô cuối kết thúc —
  kiểm lại ngay sau đó: 0 (các vòng chờ nền của phiên kết thúc cùng lúc; đã được thu hồi).
  Python 3.11.15 (mặc định, PyYAML 6.0.1 của hệ thống, **không** `jsonschema`, như lượt r1) và
  Python 3.12.3 kèm PyYAML 6.0.3 + jsonschema 4.26.0 (đúng bản `ci.yml` ghim, cài vào thư mục riêng
  bằng `pip install --target`). Ruff 0.15.8 (hệ thống) và **0.15.15** (bản `ci.yml` ghim, cài riêng).

#### 1.8.2 Tái hiện số của reviewer lượt 1 (trước khi đổi gì)

Chạy chính `do_dot_bien3.py` của reviewer (sha256 `97c273b4db81d7c9…`, khớp tệp trong
`goi/evidence/`) cho 47 dò anh em, trên ba cây, Python 3.11.15:

| cây | SỐNG | GIẾT | `so_neo` |
|---|---|---|---|
| nền | 43 | 4 | 1 ở cả 47 |
| IMP-MIN | 28 | 19 | 1 ở cả 47 |
| IMP-GEN | 7 | 40 | 1 ở cả 47 |

Ba danh sách SỐNG trùng **từng tên** với phụ lục của verdict. Bốn dò GIẾT trên nền là
`s_bk_lower`, `s_bk_strip`, `s_mh_digit_d`, `s2_hong_lt_n`. Bảy dò còn SỐNG trên IMP-GEN:
`m_cf_061c_bk`, `m_cf_tag_bk`, `s2_hong_gt_bq`, `s2_hong_va_khong_bq`, `s2_tk_va_khong_bq`,
`s_bk_strip_zs`, `s_mh_strip_zs`.

#### 1.8.3 Phụ lục A và B chạy lại trên `fc852ff`

- **Phụ lục A** (`do_dot_bien.py`, sha256 `3d53b90d…3d53`, tách lại từ r1 và băm lại: khớp) trên
  nền, 22:36:04Z–22:39:52Z, Python 3.11.15: 30 dò = **24 SỐNG + 6 đối chứng bị giết** —
  `c48_trong_cua_so` (`t52`, 1/56); `c49_lower_head`, `c49_strip_mh`, `c49_ra_strip` (`t53`, 1/56);
  `c49_ra_abspath` (`t53` và `t54`, 2/56); `c50_bang_1` (`t54`, 1/56). Trùng phân hạng §1.6 ở 30/30;
  `so_neo` = 1 ở cả 30; mỗi dò 25,2–34,4 s.
- **Phụ lục B** (`do_f49_ma.py`, sha256 `6707002f…0473`) trên nền: đầu ra sha256
  `42ca657c282ec38b87170a3b1b98be32b1affd68169bde375540e5d7da1d741d`, trùng từng byte với lượt r1.

#### 1.8.4 Tập dò đóng (Phụ lục C) trên bốn cây

Bảng theo họ ở §2. Theo tập của §6 (số dò SỐNG; đối chứng tính trong số dò):

| tập | dò | đối chứng | tương đương | nền | IMP-MIN | IMP-GEN | IMP-R2 | IMP-R2F (3.12) |
|---|---|---|---|---|---|---|---|---|
| T-B (A1) | 155 | 6 | 2 | 149 | 133 | 101 | 8 | 2 (đúng hai dò tương đương) |
| T-C (A2) | 41 | 1 | 0 | 40 | 38 | 24 | 2 | 0 (đối chứng `s_ra_realpath` KHÁC, như nền) |
| T-D (A3) | 12 | 1 | 0 | 11 | 8 | 8 | 0 | 0 |
| T-E (A8) | 7 | 2 | 0 | 5 | 5 | 5 | 0 | 0 |
| ngoài lớp | 6 | 0 | 0 | 6 | 6 | 6 | 6 | 6 |

Số dò SỐNG trên mỗi cây. Bốn cột đầu: Python 3.11.15 (209 dò 22:39:52Z 30-09 – 00:08:24Z 01-10; 12 dò nhóm ngoài `D698` từ 00:53:07Z). Cột IMP-R2F: **trọn 221 dò**, Python 3.12.3 kèm PyYAML 6.0.3 và jsonschema 4.26.0 (nên `t2` chạy và đạt, không bị bỏ qua), 01:07:00Z–01:30:54Z (156 dò; lệnh nền nối chuỗi bị dừng ở trần 2 giờ, §1.8.1) rồi 01:39:51Z–01:49:11Z (65 dò còn lại). `so_neo` = 1 ở mọi dòng của mọi cây. Trên IMP-R2F, mọi dò thuộc A1–A3, A8 ngoài đối chứng và hai dò tương đương đều GIẾT đúng ca đích, bán kính 1/56. Cột IMP-R2 cho thấy vì sao có `N698`: không có nó, 8 dò `m_co_*`, `m_cn_*` SỐNG; 4 dò `m_lo_*` thì chết sẵn vì `D698` đã chứa 2.159 ký tự `Lo` có NFKC khác chính nó (ví dụ U+00AA). Một lượt 56 ca của một dò, 4 tiến trình song song: trung bình 29,8 s trên nền (25,2–38,0), 34,3 s trên IMP-R2 (29,7–41,4), Python 3.11.15; 35,5 s trên IMP-R2F với Python 3.12.3 (31,5–59,5).

#### 1.8.5 Ba phép đo mà r1 khai "không dựng được" hoặc "KHÔNG ĐO"

- **Tập bắt ngoại lệ của `_van_tay`** (phần đo được của F46). Mỏ neo hai dòng
  `except (OSError, subprocess.SubprocessError):` + `head = ""`, thay bằng năm cách mở rộng và hai
  cách thu hẹp (Phụ lục C, họ E). Trên nền: năm dò mở rộng (`Exception`, `BaseException`, thêm `ValueError`, thêm `UnicodeError`, thêm `RuntimeError`) **SỐNG** 5/5; hai dò thu hẹp (`OSError` một mình, `SubprocessError` một mình) bị `t53` giết, bán kính 1/56 — đối chứng. Lý do: `_luoi_git` chỉ ném `OSError`,
  `SubprocessError`, `TimeoutExpired` — đều nằm trong tập bắt — nên không ô nào phân biệt tập bắt
  đúng với tập bắt rộng hơn. Trên IMP-R2 và IMP-R2F (ba ô `ValueError`, `UnicodeDecodeError`, `RuntimeError`):
  năm dò mở rộng **GIẾT** `t53`, bán kính 1/56, 5/5; hai đối chứng vẫn GIẾT.
- **Zs ngoài ASCII**: `strip` và xoá ở mọi vị trí (NBSP, U+2003, U+3000, và cả họ Zs) trên `bk`,
  `mh`, `head`, `ra`: 8/8 dò (`s_bk_strip_zs`, `s_mh_strip_zs`, `s_bk_drop_zs`, `s_mh_drop_zs`, `m_zs_bk`, `m_zs_mh`, `m_zs_head`, `m_zs_ra`) **SỐNG** trên nền, 8/8 **GIẾT** `t53`, bán kính 1/56, trên IMP-R2 và trên IMP-R2F.
- **`HOME` và `expanduser`**: `setpriv --reuid=54321 --regid=54321 --clear-groups` (UID 54321
  không có trong passwd: `getent passwd 54321` rỗng) rồi `python3 -c` in `os.path.expanduser("~/x")`:
  có `HOME=/root` ⇒ `'/root/x'`; bỏ `HOME` (`env -u HOME`) ⇒ `'~/x'`; `HOME=` rỗng ⇒ `'/x'`. Chạy
  bằng root, bỏ `HOME` ⇒ `'/root/x'` (passwd có root). Vậy ô `~/x` chỉ có răng khi `HOME` được
  đặt, hoặc UID có trong passwd; M1/M2 ghim `HOME` và `USERPROFILE` để bỏ phụ thuộc ấy.
- **Ký tự ngoài ASCII trong nguồn nền**: 0 ký tự Cf, 0 ký tự U+FF01…U+FF5E, và đúng một ký tự
  phân biệt có NFKC khác chính nó (U+2026, dấu ba chấm trong chú thích).

#### 1.8.6 Bộ đọc ngoài lớp B

Đo bằng Phụ lục C trên nền (Python 3.11.15), để §2 có trạng thái thay cho "KHÔNG ĐO":

- **Đầu tệp mảnh của `_gom_manh`** (ca đích `t52`): chuẩn hoá `dau["head"]` bằng NFKC, bỏ Cf, bỏ TAB,
  hoặc `strip()` trước khi so với vân tay của tiến trình gom — **SỐNG 4/4** (`g_nfkc_head`,
  `g_cf_head`, `g_tab_head`, `g_strip_head`). Lý do: kịch bản `head` của `_in_tu_kiem_gom` dùng
  `"0" * 40` khác hẳn `"b" * 40`, không có kịch bản nào là biến thể chuẩn-hoá-được của vân tay đúng.
  Hậu quả nếu có đột biến như thế trong mã thật: một tệp mảnh bị sửa có `head` dạng fullwidth hay
  kèm ký tự vô hình vẫn được gom nhận. Ghi nợ `gom-dau-manh-chuan-hoa-wp698` (§11.1 điểm 5).
- **`CONG_CU_TEST_TIEN_TRINH`** (ca đích `t54`): bỏ Cf hoặc bỏ TAB trước `isdigit()` — **SỐNG 2/2**
  (`t_cf`, `t_tab`); `t54` chỉ đặt biến này bằng `"1"` và `"3"`. Cùng họ với nợ mức mã
  `so-tien-trinh-nhan-fullwidth` (Q2) nên gộp vào nợ ấy.

#### 1.8.7 Ứng viên tham chiếu (công cụ đo, không giao)

Mô tả bằng lời, không đính mã (Q14). IMP-R2G (đời cuối) = nền cộng (1) phép quét M1 trong cửa `--tu-kiem-che-do`
(`D698` dẫn xuất lúc chạy, `R698`, `N698`, sinh ô theo luật vị trí, so `_doc_che_do`/`_van_tay` với
`_mong_che_do`/`_mong_git`, trả số ô và ô lệch; cha đòi số ô theo công thức), với `HOME` và
`USERPROFILE` ghim quanh `kq["luoi"]` và phép quét; (2) 12 ô `ra` cấu trúc của M2 trong
`_luoi_che_do`; (3) ba ô ngoại lệ của M5 trong `_luoi_git`, ba dòng trong bảng `nem`, một nhánh
trong `_mong_git`; (4) trục và 48 kịch bản tích của M3 trong `_in_tu_kiem_main` và `t54`; (5) 43
hàng canh ở cuối bảng `DOT_BIEN` có sẵn trước `_TRUOC_NANG_LUC`.

**Số đo trên ứng viên tham chiếu** (Python 3.11.15 trừ khi ghi khác):

- **Kích thước**: IMP-R2G `git diff --numstat` = +191/−5, một tệp (ước cho bản giao ở S5).
- **Hợp đồng đếm M1**: S1/S2 ở M1; `t53` xanh trên cả 3.11.15 và 3.12.3, tức 0 ô lệch giữa mã nền và
  oracle trên toàn miền dẫn xuất.
- **Thời gian**: §7.
- **Canh**: 40 canh của IMP-R2F (bảng canh §5 trừ ba canh thêm ở IMP-R2G) 40/40 GIẾT đúng ca đích,
  bán kính 1/56 (01:01:20Z–01:07:00Z 01-10, Python 3.11.15); trên IMP-R2 (đăng ký `m_cc_mh` thay cho
  `m_cc_head`, vì IMP-R2 dựng trước khi phép đo nền cho thấy `m_cc_mh` là đối chứng) cũng 40/40 GIẾT
  (00:09:16Z–00:15:26Z). Đủ 43 canh của IMP-R2G: đo trong A5 (dưới).
- **Đột biến cũ**: A5 trên IMP-R2G (dưới) đo **cả 416** đột biến cũ cùng 43 canh. Trước đó, trên IMP-R2,
  139 đột biến cũ nhắm `t53`/`t54` (50 + 89, bộ sáu trường y nguyên) đã ra 139/139 GIẾT đúng ca đích,
  bán kính 1/56 (00:27:09Z–00:46:10Z, `do_reg.py` của reviewer).
- **A4 trên nền và IMP-R2G trong một lệnh** (Python 3.12.3, PyYAML 6.0.3, jsonschema 4.26.0;
  03:01:44Z–03:08:29Z; lượt đầu trên IMP-R2F lúc 00:46:32Z–00:53:07Z cho cùng kết luận): (a) nền
  `56/56 đạt; tổng=56, bỏ qua=0`, 416 đột biến, rc=0, 179 s · IMP-R2G `56/56 đạt; tổng=56, bỏ qua=0`, 459 đột
  biến, `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0, 212 s. (b) ruff 0.15.15: hai vế cùng đúng một lỗi
  `F841` (biến `ci` gán mà không dùng), ở :2606 và :2650 — đa tập (mã, thông điệp) bằng nhau, delta 0.
  (c) `ci_dang_ky_test.py`: hai đầu ra giống hệt (`PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, rc=0).
  (e) Phụ lục E: 9 chỗ ghi = 2 trước ảnh / 7 trong cửa sổ / 0 sau mốc ở cả hai vế. (f) IMP-R2G:
  `git status --short` chỉ ` M ops/cong_cu_test.py`; `git diff --name-only fc852fff…` = `ops/cong_cu_test.py`;
  nền: cả hai rỗng.
- **Phụ lục C trên Python 3.12.3**: trọn 221 dò, 01:07:00Z–01:30:54Z (156 dò; lệnh nền nối chuỗi bị dừng ở trần 2 giờ, §1.8.1) rồi 01:39:51Z–01:49:11Z (65 dò còn lại): SỐNG đúng 2 dò thuộc A1–A3, A8 (`m_nfkc_khac_bmp_mh` `m_nfkc_no_bk`, hai dò tương đương), KHÁC đúng đối chứng `s_ra_realpath`, 6 dò ngoài lớp SỐNG, còn lại GIẾT (§1.8.4).
- **A5 trọn** (8 mảnh + `--gop`) trên IMP-R2G, Python 3.12.3 + gói ghim: 01:53:10Z–03:00:59Z 01-10. Tám lượt `CONG_CU_TEST_MANH=k/8` (thư mục ra ngoài cây), mỗi lượt rc=0 và `MẢNH k/8: 58/58` (k = 0, 1, 2) hoặc `57/57` (k = 3…7) `đột biến bán kính 1`, 497–521 s mỗi mảnh; `--gop` rc=0: `GOM MẢNH 8/8`, `SỐ LIỆU GOM: ca=56 · đột biến=459 · lỗi đột biến=0`, 459 dòng `ok`, 0 dòng ĐỎ. Kiểm tên: bộ sáu trường của cả 416 tên cũ y nguyên giữa nền và IMP-R2G; 43 tên mới, đúng 16 tên r1 cộng 27 tên `r2_<dò>` của bảng canh §5. Sau A5, `git status --short` của IMP-R2G chỉ có ` M ops/cong_cu_test.py`; 0 zombie trước và sau.

**Bậc hai trên IMP-R2-GO** (mỗi dòng gỡ một nhóm bằng `GO698`, chạy các canh liệt kê bằng
`do_reg.py` của reviewer — script chạy đúng tên đã đăng ký trong `DOT_BIEN`):

Tên canh trong bảng dưới (`f49_*`, `f50_*`) là tên **mục `DOT_BIEN`** của 16 canh r1 trong ứng viên tham chiếu IMP-R2 —
đặt theo mẫu tiền tố `f49_`/`f50_` mà §5 của r1 gợi ý; r1 không chứa tên nào trong số ấy — không phải tên dò (câu này
do r4 sửa từ chữ của `HINT.patch` lượt 3, §0). Dò cùng mỏ neo và phép thay trong Phụ lục A là: `f49_nfkc_*` ↔ `e49_nfkc_*`, `f49_cf_*` ↔
`e49_cf_*`, `f49_tab_*` ↔ `x46_tab_*`, `f49_ra_*` ↔ `e49_ra_*`, `f50_bang_2` ↔ `e50_bang_2`, `f50_tu_2` ↔ `e50_tu_2`,
`f50_bang_n_tru_1` ↔ `x50_bang_n_tru_1`, `f50_hong_bang_1` ↔ `x47_hong_bang_1`, `f50_tk_bang_1` ↔ `x47_tk_bang_1`.

| gỡ (`GO698`) | canh SỐNG lại | canh vẫn GIẾT (đối chứng chéo, hoặc còn ô khác giết) |
|---|---|---|
| `cf` | 9/9 canh Cf: `f49_cf_bk` `f49_cf_mh` `f49_cf_head` (r1) · `q_cf_lead_bk` `q_cf_mid_head` `p_cf_head_17` `m_cf_tag_bk` `m_cf_061c_bk` `s_ra_cf`; trên IMP-R2G-GO thêm `q_cf_mid_ra` `m_cf_tag_ra` | `f49_nfkc_bk`, `f49_tab_bk` |
| `nfkc` | `f49_nfkc_bk` `f49_nfkc_mh` `f49_nfkc_head` (r1) · `m_nfkc_ngoai_bmp_mh` | `f49_cf_bk`, `f49_tab_mh`, `m_bodau_bk`; `s_ra_nfkc` (ô cấu trúc `x` + U+00A0 và `Ma` + U+0309 + `nh` của M2 cũng đổi dưới NFKC) |
| `nfkc,ra` | — | `s_ra_nfkc`: NFKC còn **ghép** dấu kết hợp — chèn U+0301 vào `a/b` thì NFKC đổi chuỗi, mà U+0301 tự nó có NFKC bằng chính nó nên không thuộc nhóm `nfkc` |
| `nfkc,ra,dau` | `s_ra_nfkc` | — |
| `tab` | `f49_tab_bk` `f49_tab_mh` `f49_tab_head` (r1) · `q_tab_lead_mh` `s_ra_tab` | `f49_cf_mh`, `f49_nfkc_mh` |
| `zs` (Zs, Zl, Zp) | `s_bk_drop_zs` `s_mh_drop_zs` | `s_head_strip_ascii` (Cc khoảng trắng ở hai đầu `head` cũng giết nó) |
| `cc` | `m_cc_head`, `m_cc_ra` (đo bằng dò tiêm của Phụ lục C) | `s_head_strip_ascii`; `m_cc_mh` (đối chứng: ô nền `0/8` + LF giết nó) |
| `zs,cc` | `s_head_strip_ascii` | — |
| `dau` (Mn, hoặc NFD khác chính nó) | `m_bodau_bk` | — |
| `ngoai` (`N698`, IMP-R2G-GO) | `m_co_bk` | — |
| `ra` (12 ô cấu trúc M2) | `s_ra_expandvars` | `s_ra_lstrip_dot`, `s_ra_rstrip_slash`, `f49_ra_normpath`, `f49_ra_expanduser`: miền M1 trên `a/b` cũng giết chúng (thay `a` bằng `.` ra `./b`; chèn `/` ra `a/b/` và `a//b`; thay `a` bằng `~` ra `~/b`) |
| `exc` (3 ô ngoại lệ M5) | `z_exc_all` `z_exc_them_valueerror` | — |
| `tich` (48 kịch bản M3) | `s2_hong_va_khong_bq` `s2_hong_gt_bq` `s2_tk_va_khong_bq` `s3_xor` | `f50_hong_bang_1`, `f50_tk_bang_1` (trục cũng giết) |
| `bq` (trục `bo_qua`) | `f50_bang_2` `f50_tu_2` `f50_bang_n_tru_1` | — |
| `hong` | — | `f50_hong_bang_1` (tích cũng giết) |
| `hong,tich` | `f50_hong_bang_1` | — |
| `tk` | — | `f50_tk_bang_1` (tích cũng giết) |
| `tk,tich` | `f50_tk_bang_1` | — |

Đo 00:15:26Z–00:27:09Z 01-10 (hai dòng `nfkc,ra` và `nfkc,ra,dau` đo thêm 00:27Z–00:29Z, một tiến trình, song song với lô đột biến cũ; ba canh của IMP-R2G đo trên IMP-R2G-GO lúc 01:52Z, Python 3.12.3), Python 3.11.15 nếu không ghi khác. Mọi dòng "SỐNG" nghĩa là ca đích vẫn `qua` và không ca nào
chết; mọi dòng "GIẾT" là `giet_that` đúng ca đích, bán kính 1/56. Không lượt nào ra `tin_dung_gia`.

#### 1.8.8 Kích thước `D698` theo bản Unicode

Đo bằng một vòng qua mọi điểm mã (trừ surrogate) trên từng bản Python, ở độ ưu tiên thấp:

| Python | Unicode | `D698` | trong BMP | ngoài BMP | Cf (ngoài BMP) | NFKC khác chính nó |
|---|---|---|---|---|---|---|
| 3.11.15 | 14.0.0 | 19.588 | 10.982 | 8.606 | 163 (120) | 4.866 |
| 3.12.3 | 15.0.0 | 19.798 | 10.984 | 8.814 | 170 (127) | 4.928 |

Phần trong BMP bằng đúng tập "chọn theo thuộc tính" mà reviewer lượt 1 dùng cho IMP-SWEEP
(10.982 trên 63.488 điểm mã BMP không phải surrogate). Phần ngoài BMP là thứ IMP-SWEEP thiếu và, theo verdict lượt 1,
làm `m_cf_tag_bk` sống ở đó (r2 không đo lại IMP-SWEEP); trong 8.606 điểm mã ấy có 120 Cf (97 TAG ở U+E0001 và U+E0020…U+E007F, 23 Cf khác ở U+110BD, U+110CD, U+13430…U+13438, U+1BCA0…U+1BCA3, U+1D173…U+1D17A; trên 3.12.3, 127 Cf = 97 TAG + 30 Cf khác, U+13430…U+1343F thay cho U+13430…U+13438 — đo lúc soạn r3, §1.9.10), 886 Mn, 782 Ll và 704 Lu (chữ toán
học có NFKC về ASCII), 3.874 So. **Vét cạn cho các dò tập con NFKC** (cả hai bản Python, cùng kết quả): với mỗi điểm mã `c` của tập
con có NFKC(c) ≠ c, đếm những `c` mà NFKC(c) là đoạn con khác rỗng của `manh` (với `bk`), chỉ gồm chữ
số ASCII và `/` (với `mh`), hoặc chỉ gồm hex thường (với `head`) — `No`
đối với `bk`: **0**; "khác trong BMP" đối với `mh`: **0**; mọi cặp (tập con, bộ đọc) còn lại: từ 4 tới 137.
Hai dò `m_nfkc_no_bk` và `m_nfkc_khac_bmp_mh` vì vậy **tương đương** với nền theo cấu tạo:
không đầu vào nào làm chúng lệch nền.

### 1.9 Đo cho r3 (01-10, sau review lượt 2)

#### 1.9.1 Giàn đo

- **Không mạng, không đọc GitHub, không clone từ mạng.** Đầu vào kiểm băm trước khi dùng: `VERDICT.md` lượt 2
  `e281338f…3968`, `HINT.patch` lượt 2 `83b9df33…e832` (khớp chỉ thị giao việc); r2 trong worktree sha256
  `f69bb398…2c0a`, HEAD `c54b502`.
- **Cây nền**: `git clone --shared --no-checkout` từ mirror bare của sandbox review lượt 2, `checkout` `fc852ff`,
  `core.abbrev 7`; `git hash-object ops/cong_cu_test.py` = `9edea6b1629b46f27758b2073e74210dc73495b7`;
  `git status --short` rỗng.
- **Cây đo** = liên kết cứng từ cây nền, rồi thay đúng `ops/cong_cu_test.py` bằng một tệp riêng (một liên kết,
  không chung inode với nguồn). Mỗi cây kèm sha256 (16 ký tự đầu) của `ops/cong_cu_test.py` và `--numstat` so nền:
  - `cand` (`763f30434e446b20`, +150/−4): ứng viên `IMP-ME` của reviewer lượt 2, dựng từ chữ r2, chép từ sandbox
    của reviewer (chỉ đọc). Năm biến thể của reviewer cũng chép nguyên: `tv_exc` (`96746d0fada9941a`, miền ngoại
    lệ theo HINT), `tv_head` (`c17b11622c7a244b`, ô nhiễu theo tập `splitlines` của HINT), `tv_list`
    (`554e8fca3227e87e`, danh sách nhóm thay cho luật), `tv_naive` (`a504b5986035c1c2`, không trỏ `TEP_TEST`),
    `tv_go_nfkc` (`ac360d2dffdc0e4a`), `tv_go_cc` (`90a5a714aae783b8`).
  - Phiên r3 dựng: `tv_go_nfkc_p`, `tv_go_cc_p` (như hai cây trên, định nghĩa nhóm trừ Zs/Zl/Zp và trừ TAB);
    `v3_exc` (`9656ab8902129ddd`, +210/−4 — `cand` + M5b), `v3_head` (`abd3bde79a98338d`, +160/−4 — `cand` + M1b),
    `v3_ra` (`f5869a4fca89aa31`, +200/−4 — `cand` + M2b), `v3_all` (`29454841c7797838`, +271/−4 — cả ba; gốc nhóm
    ngoại lệ đọc qua `getattr`), và ba cây gỡ để đo bậc hai: `v3_go_exc` (`b32255cde7124b4c`), `v3_go_tach`
    (`01a65757a88d6ea9`), `v3_go_ra2` (`92064649882d4d44`) = `v3_all` trừ đúng một hướng. `v3_*` là công cụ đo,
    **không** phải bản giao; mã của chúng không nằm trong tệp này (Q14 theo tinh thần).
- **Kiểm tỉnh táo**: chưa đột biến, `t52`, `t53`, `t54` ra `qua` trên mọi cây đo (`sanity_case.py` của reviewer).
- **Script dò**: bản ghép Phụ lục C + H (366 dò); mọi mỏ neo xuất hiện đúng 1 lần trên nền (`so_neo` = 1 ở mọi
  dòng đã đo). Phân hạng bằng hàm `hang` của Phụ lục D (giống hệt bản r2).
- **Bộ chạy**: `run_g.sh` của reviewer (4 tiến trình, `wait` từng con, canh đĩa), `do_o_nen.json` = `[]` — không bỏ
  ca nào, kể cả `t38` (rò ≈ 1,5 MB mỗi lượt; thư mục tạm dọn sau mỗi lô). Python 3.12.3 (bản `ci.yml` ghim), PyYAML
  hệ thống, **không** `jsonschema` (nên `t2` luôn `bo_qua`). Lô đầu (09:39Z) được dừng có kiểm soát lúc 09:57Z để
  không vượt trần 2 giờ của một tác vụ nền; các dò đã đo giữ nguyên, phần còn lại chạy bằng bộ chạy tiếp được
  (bỏ dò đã có dòng kết quả) từ 10:03Z tới 12:18Z — lô cuối là `v3_all` (158 dò: 113 dò `exc`/`head`/`ra` lúc
  11:35Z–12:09Z, cộng 45 dò lúc 12:10Z–12:18Z). Mọi phép đồng hồ của Phụ lục I chạy **sau** lô cuối. 0 zombie (đo
  bằng `ps` sau lô cuối).
- **Giới hạn khai**: trong mọi lượt đo theo lô (4 tiến trình song song), ca `t47` ra `bo_qua` (`BoQuaMoiTruong`);
  chạy riêng một tiến trình — cả lượt đột biến đơn lẻ lẫn `_chay_1_ca` — thì `t47` ra `qua`. Nguyên nhân **KHÔNG
  ĐO ĐƯỢC**. Hệ quả: bán kính quan sát được trên 54/56 ca (`t2`, `t47` không thể "chết"); không dò nào của §1.9 nhắm
  `t47`, và reviewer lượt 2 thấy `t47` `qua` trên cùng loại lượt.

#### 1.9.2 Tái hiện verdict lượt 2 (trước khi đổi gì)

| khẳng định của verdict lượt 2 | đo lại lúc soạn r3 | khớp? |
|---|---|---|
| sha256 `VERDICT.md` / `HINT.patch` | `e281338f…3968` / `83b9df33…e832` | có |
| HINT áp rc=0, 17 hunk, 1653 → 1708 dòng | rc=0, 17/17, 0 fuzz, 1653 → 1708 | có |
| 12 dò `x_exc_*` SỐNG trên `IMP-ME` | `cand`: 12/12 SỐNG | có |
| biến thể `v_exc`: 12 + 7 dò GIẾT 19/19 | `tv_exc`: 12/12 `x_exc_*` + 7/7 `z_exc_*` GIẾT | có |
| miền của `v_exc`: 45 lớp (3.12.3) | 45 | có |
| 12 dò `x_main_ra_*`/`x_wr_ra_*` SỐNG | `cand`: 12/12 SỐNG (cả trên nền) | có |
| 4 dò tách theo LF/CRLF SỐNG; 4 dò `splitlines()` GIẾT | `cand`: 4 SỐNG; 4 GIẾT | có |
| biến thể `v_head`: 8/8 GIẾT | `tv_head`: 4/4 + 4/4 GIẾT | có |
| `x_head_cf2063_at17`, `x_head_cfk_mid_only`, `x_head_sm_mid_only` SỐNG; ba đối chứng cùng họ GIẾT | `cand`: 3 SỐNG, 3 GIẾT | có |
| 18 dò `x_cat_*` 18/18 GIẾT trên ứng viên; `tv_list` 14 GIẾT + 4 SỐNG (Mc, Me, Pf, Pi) | `cand`: 18/18 GIẾT; `tv_list`: 14 GIẾT + 4 SỐNG (Mc, Me, Pf, Pi) | có |
| F50 ngoài T-D: nền 4 SỐNG + 2 GIẾT; ứng viên 4 GIẾT + 2 SỐNG | nền: 4 SỐNG + 2 GIẾT (`x_f50_h_ge2`, `x_f50_tk_ge2`); `cand`: 4 GIẾT + 2 SỐNG (hai dò hằng giữa) | có |
| bậc hai theo định nghĩa thuộc tính thuần: `nfkc` 6, `cc` 6 SỐNG lại | `tv_go_nfkc` 6, `tv_go_cc` 6 | có |
| cửa con `--tu-kiem-che-do`: 4,2–4,7 s (trỏ `TEP_TEST`) so với 63,0–65,5 s | trong tiến trình: 4,32 s so với 60,77 s | cùng bậc |
| `t52`/`t53`/`t54` nền 4,33–6,97 / 0,40–0,49 / 1,85–2,05 s | 4,14–4,32 / 0,37–0,40 / 1,76–2,09 s | cùng bậc |
| ruff: ứng viên một `F841` ở :2659 | `cand`: một `F841` ở :2659 | có |
| Cf ngoài BMP (3.11.15): 97 TAG + 23 | 97 + 23 | có |
| Phụ lục C: 221 dò | 221 (209 + 12 `ngoai-d698`) | có |
| `SO_THU_HOI_KICH_HOAT = False` ở `ops/lease_publish.py:1093` | :1093 | có |

Khác biệt môi trường so với sandbox lượt 2: `t47` `bo_qua` trong lượt theo lô (§1.9.1); không có ruff 0.15.15 (chỉ
0.15.8, như reviewer); không có `jsonschema` (như reviewer).

#### 1.9.3 M5 — tập bắt ngoại lệ của `_van_tay` (lớp `m5-ngoai-le-chi-ba-kieu`)

- **Miền đo lúc chạy** (cửa con của `v3_exc`; Python 3.11.15 và 3.12.3 cho cùng số): |`B698`| = 67 lớp — mọi giá
  trị của `vars(builtins)` là lớp con của `BaseException`, gồm năm lớp không đi qua `Exception` (`BaseException`,
  `BaseExceptionGroup`, `GeneratorExit`, `KeyboardInterrupt`, `SystemExit`); |`E698`| = 118 = 67 + 51 lớp nạp từ
  thư viện và mô-đun của kho (theo mô-đun: `yaml` 11, `shutil` 7, `lease_publish_test` 4, `subprocess` 3, chính tệp 3
  — `BoQuaMoiTruong`, `LoiDungCa`, `TinHieuChotCa` —, `argparse` 2, `bash_nen` 2, `binascii` 2, `ipaddress` 2, và
  15 mô-đun mỗi mô-đun một lớp); 0 ô lệch; 0 lớp không dựng được (họ `BaseExceptionGroup` dựng bằng hàm tạo như M5b
  nói). Miền của HINT: 45 lớp trên 3.12.3 (`ExceptionGroup` bị loại vì `__new__` không dựng được).
- **Dò** (Phụ lục H khối E1 và R3-EXC, cộng bảy dò `z_exc_*` của Phụ lục C; hạng theo Phụ lục D; G = GIẾT đúng
  `t53`, bán kính 1; S = SỐNG; K = KHÁC; số sau ký hiệu là số dò; tên trong ngoặc là các dò không GIẾT khi chúng
  là thiểu số; — = không đo trên cây ấy; ký hiệu dùng chung cho các bảng ở §1.9.4–§1.9.7):

| nhóm dò | số | nền | `cand` | `tv_exc` (HINT) | `v3_exc` | `v3_all` |
|---|---|---|---|---|---|---|
| `x_exc_*` (E1, 12 kiểu con của `Exception` trong `builtins`) | 12 | S 12 | S 12 | G 12 | G 12 | G 12 |
| `z_exc_*` (Phụ lục C: 5 mở rộng + 2 thu hẹp) | 7 | G 2 · S 5 (`z_exc_all`, `z_exc_base`, `z_exc_them_runtime`, `z_exc_them_unicode`, `z_exc_them_valueerror`) | G 7 | G 7 | G 7 | G 7 |
| `x3_exc_*` ngoài `Exception` (`kbint` `sysexit` `genexit` `bexgroup`) | 4 | S 4 | S 4 | S 4 | G 4 | G 4 |
| `x3_exc_exgroup` (hàm tạo đòi đối số) | 1 | S 1 | S 1 | S 1 | G 1 | G 1 |
| `x3_exc_*` lớp con `Exception` khác (`stopiter` `warning`) | 2 | S 2 | S 2 | G 2 | G 2 | G 2 |
| `x3_exc_*` ngoài `builtins` (`re_error` `json`) | 2 | S 2 | S 2 | S 2 | G 2 | G 2 |
| `x3_exc_menh_de_hai` (thêm mệnh đề `except TypeError`) | 1 | S 1 | S 1 | G 1 | G 1 | G 1 |
| `x3_exc_tran` (`except:` trần) | 1 | S 1 | G 1 | G 1 | G 1 | G 1 |

- Đọc bảng: trên `cand` (đúng chữ r2), 22/30 dò mở rộng SỐNG — chữ M5 của r2 để lọt mọi kiểu ngoài ba kiểu chọn
  tay; trên `tv_exc` (đúng chữ HINT), 7/30 SỐNG — đường thứ ba; trên `v3_exc`, **30/30 GIẾT** đúng `t53`, bán kính 1; `v3_all` (cả ba hướng) cho
  đúng hạng ấy ở cả 30 dò.
  `except:` trần (`x3_exc_tran`) chết ngay trên `cand` vì nó tương đương `BaseException`, mà ô `ValueError` của
  r2 đã bắt. Hai dò thu hẹp `z_exc_oserror_only`, `z_exc_subproc_only` là đối chứng (GIẾT ngay trên nền).

#### 1.9.4 M1b — `head` nhiều thẻ (lớp `head-nhieu-dong-chi-tach-lf-chua-co-o`)

- **Hai tập ký tự, đo bằng vòng qua mọi điểm mã** (trừ surrogate; 3.11.15 và 3.12.3 như nhau): ký tự mà
  `("a" + c + "b").splitlines()` tách thành hai = 10 (U+000A–U+000D, U+001C–U+001E, U+0085, U+2028, U+2029; cộng CR
  LF là chuỗi tách hai ký tự); ký tự có `c.isspace()` = 29, tức 19 khoảng trắng **không** tách dòng (U+0009,
  U+001F, U+0020, U+00A0, U+1680, U+2000–U+200A, U+202F, U+205F, U+3000). `T698` = 29 + CR LF = 30 chuỗi ⇒ 120 ô.
  Cửa con của `v3_head` trả `quet` = `[666094, 121008, [], 0]` (3.11.15) và `[673234, 122268, [], 0]` (3.12.3):
  S1 không đổi, S2 tăng đúng 120, 0 ô lệch.
- **Dò** (Phụ lục H khối E2, E3, E4, E6 và R3-HEAD; đích `t53`):

| nhóm dò | số | nền | `cand` | `tv_head` (HINT) | `v3_head` | `v3_all` |
|---|---|---|---|---|---|---|
| E6: tách theo LF / CRLF (`nl_last` `nl_first` `rsplit_nl` `crlf_last`) | 4 | S 4 | S 4 | G 4 | G 4 | G 4 |
| E2: `splitlines()` (`lastline` `lastline_raw` `firstline` `lastnonblank`) | 4 | S 4 | G 4 | G 4 | G 4 | G 4 |
| E2: `split()` theo khoảng trắng (`split_last` `split_first`) | 2 | G 2 | G 2 | G 2 | G 2 | G 2 |
| R3: tách theo 9 ký tự tách dòng khác LF, lấy phần cuối/đầu (18) + CRLF đầu (1) | 19 | S 19 | G 2 · S 17 | G 19 | G 19 | G 19 |
| R3: tách theo khoảng trắng KHÔNG tách dòng (`tab` `us` `nbsp` `emsp` `ideo`) | 5 | S 5 | G 3 · S 2 (`x3_head_emsp_last`, `x3_head_us_last`) | G 3 · S 2 (`x3_head_emsp_last`, `x3_head_us_last`) | G 5 | G 5 |
| R3: tách theo ký tự không phải khoảng trắng (`zwsp` `chu_g`) | 2 | S 2 | G 2 | G 2 | G 2 | G 2 |
| R3: chọn dòng hex / thẻ dài nhất (`pick_hex` `longest`) | 2 | G 1 · S 1 (`x3_head_pick_hex`) | G 2 | G 2 | G 2 | G 2 |
| E3: thành viên ngoài `R698` × vị trí ngoài neo (`cf2063_at17` `cfk_mid_only` `sm_mid_only`) | 3 | S 3 | S 3 | — | S 3 | S 3 |
| E3/E4: đối chứng cùng họ (`cfk_lead_only` `cfk_trail_only` `nfkc_fwletters`) | 3 | S 3 | G 3 | — | G 3 | G 3 |

- Đọc bảng: trên `cand` (đúng chữ r2), 23 dò T-B SỐNG (ngoài ba dò KHAI): bốn dò tách theo LF/CRLF của reviewer, 17/19 dò tách theo
  một ký tự tách dòng khác (hai dò theo VT chết nhờ ô VT của `R698`), hai dò tách theo khoảng trắng không tách dòng
  (`us`, `emsp`). Trên `tv_head` (đúng hướng HINT: ô nhiễu theo tập `splitlines`), mọi dò tách dòng GIẾT nhưng
  `x3_head_us_last`, `x3_head_emsp_last` vẫn SỐNG — đường thứ ba; ba dò `tab`, `nbsp`, `ideo` chết chỉ nhờ ô `R698`
  tình cờ (đầu 64 = 40 + 24). Trên `v3_head` (ô nhiễu theo `T698`), mọi dò GIẾT đúng `t53`, bán kính 1, trừ đúng ba dò
  của tập KHAI; `v3_all` cho đúng hạng ấy ở cả 44 dò. Hai dò tách theo ký tự không phải khoảng trắng (`x3_head_zwsp_last`, `x3_head_chu_g_last`) đã chết
  ngay trên `cand` nhờ ô chèn đầu/cuối của M1 — đúng lập luận "chỉ khoảng trắng mới cần ô nhiễu" ở §5 M1b. Đối chứng
  (chết ngay trên nền, nhờ ô `hop + " " + hop` của `_luoi_git`): `x_head_split_last`, `x_head_split_first`,
  `x3_head_longest`.

#### 1.9.5 M2b — các tầng hạ nguồn của `ra` (lớp `ra-ha-nguon-main-bo-ghi-chua-co-o`)

- **Liệt kê tầng** (`grep -n -w ra ops/cong_cu_test.py` trên nền, bỏ chuỗi đột biến, oracle và giàn giả): đúng các
  dòng :7468, :7470–:7471, :7485–:7487 (`_doc_che_do`), :7508 và :7514 (`_ket_thuc_manh` nhận `ra`, dựng `tep`),
  :8229, :8232, :8245 (`main`). Trong `_ket_thuc_manh`, sau :7514 mọi chỗ dùng là `tep` (T5). `_phong_con` không
  nhận `ra` (`ra_con` ở :8240–:8243 là đầu ra của tiến trình con, giá trị khác). Bảng tầng: §5 M2b.
- **Ô của biến thể `v3_ra`**: tầng `main` 122 kịch bản (61 đường × 2 chế độ); bộ ghi 456 ô trên 3.12.3 và 452 trên
  3.11.15 (12 cấu trúc + 48 vị trí + 396 hoặc 392 khúc `D698`), 0 ô lệch trên cây chưa đột biến.
- **Dò** (Phụ lục H khối E5 và R3-RA; đích `t54` cho T2/T3, `t52` cho T4/T5; G = GIẾT đúng đích ấy, bán kính 1):

| nhóm dò | số | nền | `cand` | `v3_ra` | `v3_all` |
|---|---|---|---|---|---|
| T2: `x_main_ra_*` (E5, 6 phép) | 6 | S 6 | S 6 | G 6 | G 6 |
| T2: `x3_main_ra_*` (9 phép khác) | 9 | G 2 · S 7 | G 2 · S 7 | G 9 | G 9 |
| T3a: `x3_m3a_ra_*` (lời gọi nhánh nền đỏ, 6 phép) | 6 | S 6 | S 6 | G 6 | G 6 |
| T3b: `x3_m3b_ra_*` (lời gọi nhánh thường, 6 phép) | 6 | S 6 | S 6 | G 6 | G 6 |
| T4: `x_wr_ra_*` (E5, 6 phép) | 6 | S 6 | S 6 | G 6 | G 6 |
| T4: `x3_wr_ra_*` (5 phép khác) | 5 | S 4 · K 1 | S 4 · K 1 | G 4 · K 1 (`x3_wr_ra_lower`) | G 4 · K 1 (`x3_wr_ra_lower`) |
| T5: `x3_wr5_*` (2 phép ở chỗ ghi) | 2 | S 2 | S 2 | G 1 · S 1 (`x3_wr5_normpath`) | G 1 · S 1 (`x3_wr5_normpath`) |
| argv: `x3_gop_dir_*` (3 phép) | 3 | S 3 | S 3 | S 3 | S 3 |
| argv: `x3_cua_*` (2 phép) | 2 | S 2 | S 2 | S 2 | S 2 |

- Đọc bảng: trên `cand` (đúng chữ r2), 37/40 dò T-C SỐNG — ba dò còn lại là đối chứng (dưới); như vậy chữ M2 của
  r2 chỉ đóng tầng T1. Trên `v3_ra`, 38/40 GIẾT đúng ca đích, bán kính 1; hai dò còn lại: `x3_wr5_normpath` SỐNG —
  **tương đương theo cấu tạo** trên mọi đường không có symlink, vì `tep.parent.mkdir(parents=True)` đã tạo mọi
  thư mục cha **trước** khi ghi nên hệ điều hành giải `x/..` đúng như `normpath`; chỉ một symlink trên đường mới
  phân biệt được, mà miền symlink không thuộc lớp B (lớp A/F48, Q1) — và `x3_wr_ra_lower` KHÁC (`tin_dung_gia`)
  ở cả nền, `cand` lẫn `v3_ra`: hạ chữ thường đường dẫn của bộ ghi làm hỏng giàn giáo của `t52` (thư mục tạm có
  chữ hoa) trước khi tới chốt nghiệp vụ — một cái chết vô can, nên nó là **đối chứng giữ hạng KHÁC** như
  `s_ra_realpath`, không tính là GIẾT. Hai đối chứng GIẾT ngay trên nền: `x3_main_ra_lower` (ô `Mixed.TXT`) và
  `x3_main_ra_nfd` (ô `dir/Sub Dir/Mảnh.TXT`). Bốn phép gộp `//`, bỏ `./` đầu, `/./`, bỏ `/` cuối ở T4/T5 tương đương
  theo cấu tạo (`Path()` đã làm), nên không có dò. `v3_all` cho đúng hạng của `v3_ra` ở cả 45 dò.
- **Không giết chéo tầng T1** (vì sao M2b đòi ô T2–T5 đưa `ra` vào **sau** `_doc_che_do`): trên `v3_all`, sáu dò của
  Phụ lục C — bốn dò tầng T1 `s_ra_cf`, `s_ra_rstrip_slash`, `s_ra_expandvars`, `m_cf_tag_ra` (cả bốn là canh của
  r2), cộng `s_head_strip_ascii` và `s2_hong_va_khong_bq` — đều GIẾT đúng ca đích, bán kính 1/56 (12:10Z–12:18Z).
  Lý do theo cấu tạo: kịch bản `_luoi_noi_main` của `t54` thay `_doc_che_do` bằng hàm trả thẳng `(k, n, đường)`,
  còn ô bộ ghi gọi thẳng `_ket_thuc_manh`; một dò sửa `_doc_che_do` vì vậy không chạm ô T2–T5. Nếu ô T2–T5 đi qua
  biến môi trường và `_doc_che_do` thật, các dò tầng T1 (gồm mười canh T1 của bảng canh §5: 2 của r1, 8 của r2) chết thêm ở
  `t54` hoặc `t52`, bán kính 2 — A2 và A5 đỏ (suy từ cấu tạo; không dựng biến thể ấy để đo).

#### 1.9.6 Hai bộ đọc `argv` (nguồn mà r2 chưa liệt kê)

- `grep -n "sys.argv" ops/cong_cu_test.py` trên nền: ngoài chuỗi fixture có đúng bốn chỗ đọc — `--ban-kinh-con`
  (:7281–:7287, giao thức cha–con nội bộ), `--gop` (:7610–:7614), `--tu-kiem-cong-that` (:8187–:8189, cửa tự kiểm
  nội bộ), chọn cửa ở `argv[1]` (:8384). Hai chỗ nhận giá trị từ ngoài được đo bằng dò của Phụ lục H khối R3-ARGV
  (đích `t52`, ca có các kịch bản CLI `cli_*`):

  | dò | nền | `cand` | `v3_ra` | `v3_all` |
  |---|---|---|---|---|
  | `x3_gop_dir_normpath`, `x3_gop_dir_nfkc`, `x3_gop_dir_strip` (chuẩn hoá thư mục sau `--gop`) | S 3 | S 3 | S 3 | S 3 |
  | `x3_cua_strip`, `x3_cua_nfkc` (chuẩn hoá `argv[1]` trước khi chọn cửa) | S 2 | S 2 | S 2 | S 2 |

- Kết luận: cả năm đường SỐNG ở mọi cây — không ô nào của `t52` có thư mục `--gop` hay tên cửa đổi được dưới các
  phép ấy. Theo ranh giới ở §2 (F49 không nói tới `argv`, Q1), hai bộ đọc này được **đo và ghi nợ**
  `doc-argv-chua-co-o-wp698`, không vào mục tiêu (§11.1 điểm 15).

#### 1.9.7 Mọi nhóm Unicode của `D698` (lớp `a1-tap-dong-thieu-do-theo-nhom-unicode`)

- `D698` có mặt **27** nhóm `unicodedata.category` (3.11.15 và 3.12.3 như nhau): Cc Cf Ll Lm Lo Lt Lu Mc Me Mn Nd Nl
  No Pc Pd Pe Pf Pi Po Ps Sc Sk So Zl Zp Zs. Phụ lục H có một dò xoá-cả-nhóm trên `bk` cho **mỗi** nhóm (18 dò
  E7 của reviewer cộng 9 dò `x3_cat_*` cho các nhóm còn lại), dẫn xuất bằng chính luật của `D698`, không chọn tay.

| nhóm dò | số | nền | `cand` | `tv_list` | `v3_all` |
|---|---|---|---|---|---|
| `x_cat_*` (E7, 18 nhóm) | 18 | S 18 | G 18 | G 14 · S 4 (`x_cat_mc_bk`, `x_cat_me_bk`, `x_cat_pf_bk`, `x_cat_pi_bk`) | G 18 |
| `x3_cat_*` (9 nhóm còn lại của `D698`) | 9 | G 2 · S 6 · K 1 | G 8 · K 1 (`x3_cat_ll_bk`) | G 8 · K 1 (`x3_cat_ll_bk`) | G 8 · K 1 (`x3_cat_ll_bk`) |

- Đọc bảng: trên nền 24/27 SỐNG; ba dò còn lại là đối chứng — `x3_cat_cc_bk`, `x3_cat_zs_bk` GIẾT ngay trên nền
  (ô `manh` kèm LF và ô ` manh` của `bang_env`: U+000A là Cc, dấu cách là Zs), `x3_cat_ll_bk` KHÁC (xoá mọi chữ
  thường làm `manh` thành rỗng nên chết cả `t53` lẫn `t54`, bán kính 2 — đối chứng giữ hạng KHÁC như
  `s_ra_realpath`). Trên `cand` (luật `D698`): 26 GIẾT + đối chứng KHÁC — 18/18 dò của reviewer khớp. Trên `tv_list`
  (danh sách nhóm): 4 SỐNG đúng Mc, Me, Pf, Pi như reviewer đo; 9 dò bổ sung của r3 cho cùng hạng trên `cand` và
  `tv_list` (8 GIẾT + 1 đối chứng KHÁC), tức chúng **không** thêm răng trước bản danh sách nhóm — răng ấy nằm ở bốn dò
  Mc, Me, Pf, Pi; r3 thêm chúng để A1 (v) phủ đúng **mọi** nhóm có mặt trong `D698`, dẫn xuất, không chọn tay. `v3_all` cho
  đúng hạng của `cand` ở cả 27 dò.

#### 1.9.8 Bậc hai: định nghĩa nhóm, và ba nhóm ô mới của r3

- **Định nghĩa nhóm quyết định kết quả** (lớp `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`). Bốn cây gỡ, chạy
  bằng `do_reg.py` của reviewer trên các canh đã đăng ký của `cand`:

  | cây | định nghĩa nhóm bị gỡ | canh SỐNG lại | canh vẫn GIẾT |
  |---|---|---|---|
  | `tv_go_nfkc` (reviewer) | `NFKC(c) ≠ c` (gồm cả Zs) | 6: `r2_e49_nfkc_bk` `r2_e49_nfkc_mh` `r2_e49_nfkc_head` `r2_m_nfkc_ngoai_bmp_mh` `r2_s_bk_drop_zs` `r2_s_mh_drop_zs` | 4: `r2_e49_cf_bk` `r2_m_bodau_bk` `r2_s_ra_nfkc` `r2_x46_tab_mh` |
  | `tv_go_nfkc_p` (r3) | `NFKC(c) ≠ c` trừ Zs/Zl/Zp | 4: bốn canh đầu ở trên | 6: thêm `r2_s_bk_drop_zs` `r2_s_mh_drop_zs` |
  | `tv_go_cc` (reviewer) | `Cc` (gồm TAB) | 6: `r2_m_cc_head` `r2_q_tab_lead_mh` `r2_s_ra_tab` `r2_x46_tab_bk` `r2_x46_tab_head` `r2_x46_tab_mh` | 2: `r2_e49_cf_mh` `r2_s_head_strip_ascii` |
  | `tv_go_cc_p` (r3) | `Cc` trừ TAB | 1: `r2_m_cc_head` | 7 |

  Định nghĩa "trừ" tái hiện đúng hai số của bảng §1.8.7 của r2 (`nfkc` 4, `cc` 1) — tức r2 đã dùng nó mà không ghi
  ra; định nghĩa "thuộc tính thuần" cho đúng hai số mà reviewer lượt 2 đo (6 và 6). Đặc tả chốt định nghĩa "trừ"
  (§6 A1-b2). Giao còn lại giữa các nhóm theo định nghĩa ấy (đo trên toàn `D698`, 3.11.15 và 3.12.3): `zs ∩ dau` =
  2 điểm mã (U+2000, U+2001 — NFD của chúng là U+2002, U+2003), `dau ∩ nfkc` = 1.132; mọi cặp khác rời nhau.
- **Ba nhóm ô mới của r3**, đo bằng ba cây `v3_go_*` (= `v3_all` trừ đúng một hướng):

  | cây (gỡ nhóm) | dò SỐNG lại | dò vẫn GIẾT | đọc |
  |---|---|---|---|
  | `v3_go_exc` (gỡ miền `E698` của M5b) | `x_exc_typeerror`, `x3_exc_kbint`, `x3_exc_re_error` | `z_exc_all`, `z_exc_them_valueerror` | ba canh E của r3 chết vì đúng miền M5b; hai canh E của r2 chết vì ba ô của r2 (gỡ riêng ba ô thì chúng vẫn GIẾT vì miền `E698`; chỉ gỡ cả hai mới SỐNG) |
  | `v3_go_tach` (gỡ ô nhiều thẻ của M1b) | `x_head_nl_last`, `x3_head_emsp_last`, `x3_head_us_last`, `x3_head_nel_last` | `x3_head_tab_last`, `x_head_lastline` | hai dò vẫn GIẾT chỉ nhờ ô `R698` tình cờ — nên canh "khoảng trắng không tách dòng" là `x3_head_emsp_last`, **không** phải `x3_head_tab_last` |
  | `v3_go_ra2` (gỡ ô tầng `main` và ô bộ ghi của M2b) | `x_main_ra_normpath`, `x3_m3a_ra_nfkc`, `x3_m3b_ra_cf`, `x_wr_ra_nfkc`, `x3_wr5_nfkc` | `s_ra_cf` (canh T1 của r2) | năm canh T2–T5 của r3 chết vì đúng các ô M2b; canh T5 `x3_wr5_nfkc` đo ở lượt riêng (11:35Z–11:37Z, hai cây cùng lúc): trên cây gỡ chỉ `t2_c` ở `bo_qua` (SỐNG lại), trên `v3_ra` GIẾT `t52_…` bán kính 1/56; `x3_wr5_normpath` SỐNG ở cả `v3_ra`, `v3_all` lẫn cây gỡ — tương đương |

#### 1.9.9 Chi phí và kích thước (lớp `t53-thoi-gian-khong-co-tieu-chi-do`; S5)

- **Đếm lời gọi `_van_tay` trong cửa con `--tu-kiem-che-do`** (chạy trong tiến trình, `_van_tay` được bọc bằng cách
  thay tên toàn cục của mô-đun; Python 3.12.3; 09:29Z–09:30Z, load 1 phút 0,56–0,89):

  | cây | lời gọi | lời gọi băm tệp > 4096 byte | tổng byte băm | giây |
  |---|---|---|---|---|
  | nền | 79 | 64 | 34.138.325 | 0,09 |
  | `cand` (trỏ `TEP_TEST` sang tệp 1 byte trong phép quét) | 122.230 | 67 | 36.810.055 | 4,32 |
  | `tv_naive` (cùng `cand`, bỏ đúng hai dòng trỏ `TEP_TEST`) | 122.230 | 122.215 | 73.409.520.729 | 60,77 |
  | `v3_exc` | 122.348 | 67 | 36.966.760 | 4,72 |
  | `v3_head` | 122.350 | 67 | 36.845.494 | 4,53 |
  | `v3_ra` | 122.230 | 67 | 36.971.461 | 4,65 |

  Số lời gọi của bản nhanh và bản ngây thơ **bằng nhau**: đếm lời gọi `_van_tay` không phân biệt được hai bản; đại
  lượng phân biệt là lời gọi băm tệp lớn (≈ 1.820 lần) và tổng byte. Đó là lý do phép đếm của A4-g đếm lời gọi băm
  tệp > 4 KiB, ngưỡng 2 × nền.
- **Đồng hồ trong tiến trình** (`caseclock.py` của reviewer, ba lần mỗi ca, 09:32Z–09:35Z, load 0,5–1,0; giây):

  | cây | `t52` | `t53` | `t54` |
  |---|---|---|---|
  | nền | 4,14–4,32 | 0,37–0,40 | 1,76–2,09 |
  | `cand` | 4,34–4,76 | 3,97–4,19 | 2,59–2,70 |
  | `v3_exc` | 4,45–4,85 | 3,95–4,22 | 2,58–2,73 |
  | `v3_head` | 4,32–4,57 | 4,26–4,66 | 2,49–2,87 |
  | `v3_ra` (ô bộ ghi ghi trọn bản ghi của mảnh) | 8,51–8,84 | 3,57–4,09 | 2,93–3,39 |
  | `v3_ra` (ô bộ ghi ghi **một** bản ghi — cách M2b mô tả) | 5,67–5,95 | 3,89–4,32 | 3,31–3,37 |
  | `v3_all` (bản đo trước khi đổi sang `getattr`, cùng hành vi) | 5,41–6,36 | 4,64–4,90 | 3,32–3,64 |

  Bản đầu của ô bộ ghi làm `t52` chậm gấp đôi vì mỗi ô ghi trọn bản ghi của một mảnh; M2b vì vậy đòi ghi một tên
  đột biến mỗi ô.
- **Phụ lục I** (A4-g, một lệnh, xen kẽ; Python 3.12.3; 12:18Z–12:27Z, sau khi mọi lô dò đã xong, load 1 phút
  0,76–1,96 đo trước và sau từng lệnh; mỗi lệnh `python3.12 chi_phi_r3.py nen <cây>`, đúng tệp có băm của Phụ lục I):

  | ứng viên | lời gọi `_van_tay` (nền 79) | lời gọi băm tệp > 4 KiB (nền 64) | min `t52` / `t53` / `t54`, giây (nền cùng lệnh) | Δ, giây | `loi` | rc |
  |---|---|---|---|---|---|---|
  | `v3_all` | 122.473 | 67 | 6,04 / 4,65 / 3,48 (4,65 / 0,42 / 2,06) | 7,04 | rỗng | 0 |
  | `cand` | 122.230 | 67 | 4,99 / 4,31 / 2,78 (4,63 / 0,44 / 2,07) | 4,94 | rỗng | 0 |
  | `tv_naive` | 122.230 | 122.215 | 5,00 / 64,22 / 2,85 (4,91 / 0,40 / 2,20) | 64,56 | `dem` (122.215 > 2 × 64), `dong_ho` (64,56 > 10) | 1 |
  | `tv_cham` — `cand` cộng `time.sleep(11)` ở đầu cửa con `--tu-kiem-che-do` (phiên r3 dựng, phản chứng chỉ đồng hồ) | 122.230 | 67 | 4,79 / 15,03 / 2,76 (4,63 / 0,46 / 2,24) | 15,25 | chỉ `dong_ho` (15,25 > 10) | 1 |

  Hai phép của A4-g có răng **riêng**: `tv_naive` đỏ cả hai, `tv_cham` chỉ đỏ đồng hồ (số lời gọi băm tệp lớn không
  đổi). Tổng lời gọi `_van_tay` không ổn định giữa các tiến trình đo: miền `E698` dẫn xuất lúc chạy có 118 lớp trong
  cửa con thật (§1.9.3) nhưng 122 trong tiến trình của Phụ lục I, vì Phụ lục I nạp hai bản mô-đun (đo: nạp riêng
  `v3_all` ⇒ 119, nạp thêm nền ⇒ 122) — thêm một lý do để A4-g không đặt ngưỡng trên tổng lời gọi.
- **Kích thước** (`git diff --numstat fc852ff`, một tệp): `cand` +150/−4; `v3_exc` +210/−4; `v3_head` +160/−4; `v3_ra`
  +200/−4; `v3_all` +271/−4 (ba hướng r3 = +121 so với `cand`, viết không tối ưu số dòng; chưa có 11 hàng canh r3 và
  chú thích M4). Ước cho bản giao: S5.
- **A4 khác trên `v3_all`**: ruff 0.15.8 `--select F` ⇒ đúng một `F841` cùng thông điệp với nền (bản 0.15.15 không có
  trong container r3); trước khi đổi sang `getattr`, ruff báo thêm `F821 Undefined name BaseExceptionGroup` (kho không
  có cấu hình ruff); `.claude/dev/ci_dang_ky_test.py` (không `--chay`) ⇒ đầu ra **giống từng byte** đầu ra nền
  (`PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, rc=0, ≈ 8 s); Phụ lục E ⇒ `sau_moc: []`; Phụ lục G ⇒ giao rỗng.
- **Ước mảnh CI** (mô hình tỷ lệ của r2, §7; ƯỚC, không đo trên runner): mảnh dài nhất ≈ 18,2 × (số đột biến/416)
  × (29,8 + Δ)/29,8 phút. Với Δ = 7,04 s của `v3_all`: 470 đột biến ⇒ ≈ 25,4 phút; đăng ký trọn 350 dò (766 đột
  biến) ⇒ ≈ 41,4 phút. Ngưỡng A4-g Δ = 10 s ⇒ ≈ 27,5 phút với 470. Hai ngưỡng riêng lẻ của `HINT.patch` lượt 2 (Δ = 12 s ⇒ ≈ 28,8 phút) cộng một ngưỡng `t52` + 4 s mà HINT không đề nghị, cùng
  chạm trần (Δ = 16 s) ⇒ ≈ 31,6 phút, vượt trần 30 phút.

#### 1.9.10 Số liệu tĩnh của các lớp P3 và phản chứng của script mới

- **Phụ lục A–E tách lại từ r2 và băm lại**: 5/5 khớp băm khai (`3d53b90d…`, `6707002f…`, `c6a4db8b…`, `c1bdf8d2…`,
  `b0772b01…`). Phụ lục C ở chế độ `liet_ke` in **221** tên; ở chế độ `ho`, họ `ngoai-d698` có đúng **12** dò, tức
  209 + 12 = 221 (lớp `phu-luc-c-dem-209-lech-221`).
- **Cf ngoài BMP của `D698`** (vòng qua mọi điểm mã ≥ U+10000): 3.11.15 — 120 = 97 TAG (U+E0001, U+E0020…U+E007F) +
  23 Cf khác (U+110BD, U+110CD, U+13430…U+13438, U+1BCA0…U+1BCA3, U+1D173…U+1D17A); 3.12.3 — 127 = 97 TAG + 30 Cf khác
  (U+13430…U+1343F thay cho U+13430…U+13438) (lớp `s1-8-8-nhan-tag-sai`).
- **Bảng họ ở §2** cộng lại từng cột bằng máy: 221 · 10 · 211 · 190 · 144 · 16 · 8 · 1, khớp hàng tổng; hai hàng Z
  góp 6 · 0 · 6 · 6 · 6 · 6 · 6 · 0; trừ đi ra 205 / 184 / 138 cho nền / IMP-MIN / IMP-GEN và 2 cho IMP-R2F — đúng chữ
  "ngoài hai hàng Z" (lớp `doc-bang-205-vs-211`).
- **Con số trần trục VÒNG** (lớp `tran-vong-so-10-hai-cho`): quét bằng máy trên bản cuối của r3 — mọi dòng có một
  trong các chữ vòng, trần, `ADR-0048`, `tran_cu` (không phân biệt hoa thường), tìm số mười đứng riêng (không liền
  sau chữ, chữ số, gạch dưới, dấu chấm, dấu phẩy, gạch chéo, gạch nối; không liền trước chữ số, dấu chấm, dấu phẩy):
  một kết quả là trần trục VÒNG — dòng `tran_cu` của khối `nang_tran`; năm kết quả là ngưỡng giây của Δ ở A4-g (§0 hai
  lần, §6, §7, §11.1 (C)), không phải trần vòng; không còn kết quả nào khác. Con số trục VÒNG chỉ còn ở `tran_cu`.
- **S6**: đoạn trích dòng 1043–1056 của `docs/PROTOCOL_DA_PHIEN.md`, blob `0dedc3d922dc86a78c71194b084b4bba7afda517` ở
  cả `fc852ff` lẫn `20ec8d5`; sha256 của 14 dòng nối LF = `dc93c2a34d4a6e64b9ab65285bfb431ad43bdf5b8f73f8a960f4205f311f7715`.
- **`thu-hoi`**: `ops/lease_publish.py:1093` là `SO_THU_HOI_KICH_HOAT = False` (và :1079 ghi "CHƯA KÍCH HOẠT");
  `.github/workflows/ops-thu-hoi-admission.yml` dòng 6 ghi "chưa là required check"; `trich-log.txt` có 104 dòng, mục
  log thô 765 và 767 (job `thu-hoi`, run `36688032631`) ở dòng 103–104; mục 1962/2438/2440 ở dòng 23–25, mục 2590 ở
  dòng 99.
- **Phụ lục D bản r3**: trên 221 tên của Phụ lục C, hàm `tap` mới và hàm `tap` của r2 cho cùng một tập ở mọi tên
  (155 / 41 / 12 / 7 / 6); trên 145 tên của Phụ lục H: T-B 68, T-C 40, T-E 23, T-D 4, ngoài lớp 5, KHAI 5.
- **Phụ lục H**: lệnh ghép cho bản ghép sha256 `37b6e8bd53e8c14bc634a198aa4fabff7400b662d67b38ab80caf90aeef6e55b`;
  bảng `P` và bảng họ của bản ghép trùng từng mục, cùng thứ tự, với script dò mà phiên r3 đã chạy; 366 dò; mọi mỏ neo
  xuất hiện đúng 1 lần trên nền; tên của Phụ lục A và của bản ghép rời nhau.
- **Phụ lục F** (A5 (vi)), trên `cand` với bảng nối 43 dòng `<dò> r2_<dò>`: rc=0, 0 lỗi (43 canh của `cand` trùng từng
  byte với dò cùng tên). Phản chứng trên bản sao của `cand`: đổi phép thay của `r2_s_ra_cf` thành một phép yếu hơn
  (chỉ bỏ U+200B) ⇒ rc=1 `["lech-bo", "s_ra_cf", "r2_s_ra_cf"]`; đổi tệp mục tiêu của bộ cũ `t1_rc_gop` ⇒ rc=1
  `["bo-cu", "t1_rc_gop"]`; bỏ dòng cuối của bảng nối ⇒ rc=1 `["tap-ten", ["r2_s3_xor"]]`.
- **Phụ lục G** (A4-d): khoảng nền của sáu hàm = `_chay_1_ca` 2292–2332, `_ket_luan_ban_kinh` 2353–2422,
  `_so_tien_trinh_ban_kinh` 7082–7097, `_doc_che_do` 7461–7487, `_van_tay` 7495–7505, `main` 8195–8284. `cand` (10
  hunk) và `v3_all` (14 hunk) ⇒ giao rỗng, rc=0. Phản chứng: thêm chú thích cuối dòng 7501 ⇒ rc=1
  (`@@ -7501 +7560 @@`); chèn một dòng thụt lề ngay sau dòng 7505 ⇒ rc=1 (`@@ -7505,0 +7565 @@`); thêm chú thích ở dòng
  8229 của `main` ⇒ rc=1; chèn một hằng mức mô-đun cách `_van_tay` bởi dòng trống ⇒ rc=0.
- **Phụ lục E** (A4-e) trên `v3_all`: `{"tong": 10, "truoc_anh": [2256, 2262, 2316], "trong_cua_so": 7, "sau_moc": []}`
  — chỗ ghi thứ ba trước ảnh là vòng đăng ký canh của `cand`.

### 1.10 Đo cho r4 (07-10, sau review lượt 3)

#### 1.10.1 Giàn đo

- **Mạng:** không fetch, không clone mạng, không ghi gì lên GitHub. Lệnh mạng chỉ là **đọc** qua REST (`gh api`): các
  comment của #698 (ID ba bản chiếu verdict, header), danh sách job của run `36696528580` (thời lượng job và bước, §7) và
  trường `visibility` của kho (§7). Một lệnh đọc log job bị client từ chối vì log nằm ở máy chủ khác (`*.blob.core.windows.net`),
  nên mọi thứ chỉ có trong log job là **KHÔNG ĐO ĐƯỢC**. Đầu vào kiểm băm trước khi dùng (§0). `origin/master` chỉ đọc từ
  bộ đệm (header, hàng nền nghiệm thu).
- **Cây nền:** `git clone --shared --no-checkout` từ kho chính rồi `checkout` `fc852ff`, `core.abbrev 7`;
  `git hash-object ops/cong_cu_test.py` = `9edea6b1629b46f27758b2073e74210dc73495b7`; `git status --short` rỗng.
- **Cây đo** = liên kết cứng từ cây nền (`cp -al`), rồi thay đúng `ops/cong_cu_test.py` bằng một tệp riêng (gỡ liên kết
  trước khi ghi). Mọi biến thể dựng bằng một script từ `v3_all` của phiên soạn r3 (sha256 đầu `29454841c7797838`, còn
  nguyên trong scratch của phiên r3, đo lại bằng `sha256sum`); mỗi phép sửa thay **đúng một** đoạn văn bản có mặt **đúng
  một** lần (script `assert`). Biến thể chuẩn `v4_all` = `v3_all` + 11 hàng canh r3 (tên `r3_<dò>`, cùng bộ với dò cùng
  tên của Phụ lục H, mỏ neo một dòng viết bằng nối chuỗi) + M6 ở bốn chỗ gọi + T5 hai lần gọi và so dòng in. Mỗi biến thể
  khác `v4_all` đúng một chỗ:

  | cây | sha256 (16 ký tự đầu) | `--numstat` so nền | khác `v4_all` ở |
  |---|---|---|---|
  | `v4_all` | `b1744a686501530d` | +291/−4 | — (biến thể chuẩn) |
  | `v4_lit` | `c5ee09ca51fcbf4b` | +291/−4 | 11 hàng canh r3 viết bằng `repr` |
  | `v4_tq` | `3d37cdb35fc5c382` | +327/−4 | 11 hàng canh r3 viết bằng chuỗi ba nháy nguyên văn |
  | `v4_cu` | `a5807b3c92651f1f` | +292/−4 | thêm một dòng chú thích trích nguyên văn `    tep.parent.mkdir(parents=True, exist_ok=True)` ở vùng bảng |
  | `v4_nocatch` | `bd0edcfa6f1a7114` | +280/−4 | không khối bắt nào của M6 (bộ ghi không bắt gì) |
  | `v4_exc` | `53cfeb029f6c62b8` | +291/−4 | bốn khối bắt chỉ bắt `Exception` |
  | `v4_go_t1` · `v4_go_head` · `v4_go_main` · `v4_go_wr` | `59cd92c0c13e37e8` · `8ae4433b36a808e0` · `2bee3827802d9308` · `3b5b1aa2ce1dc79a` | +289 · +286 · +289 · +289 /−4 | gỡ khối bắt ở đúng một chỗ gọi: `doc` · quét `head` · vòng `main` · bộ ghi |
  | `v4_t5_r3` | `70df8ccb1d8d1313` | +291/−4 | bộ ghi gọi một lần, không so dòng in (cách của `v3_all`) |
  | `v4_go_hai` · `v4_go_in` | `b94c14c4a884d4ae` · `ed0629e29bde4b4a` | +291/−4 | chỉ bỏ lần gọi thứ hai · chỉ bỏ phép so dòng in |
  | `v4_nomem` | `d3b88a5ebeb4a17b` | +290/−4 | bỏ đường "mọi thành viên" ở tầng `main` và các khúc tên tệp phủ `D698` ở bộ ghi |
  | `v4_go_e698` · `v4_go_r2exc` · `v4_go_exc2` | `d83042a1816ffb97` · `3e14af0624f9f7f9` · `61898f363ffe3aef` | +286/−4 · +290/−3 · +285/−3 | gỡ miền `E698` · gỡ ba ô ngoại lệ của r2 · gỡ cả hai |
  | `tv_cpu` | `b300ec7518171886` | +292/−4 | thêm một vòng đốt CPU (2 × `TV_CPU_N` lần lặp; biến không đặt thì 0) ở đầu cửa `--tu-kiem-che-do` |

  `tv_naive` (`a504b5986035c1c2`) và `tv_cham` (`7078ffebcef5a42d`) là hai cây của phiên soạn r3 (dựng trên `cand`),
  chép nguyên. `v4_*`, `tv_cpu` là công cụ đo, **không** phải bản giao; mã của chúng không nằm trong tệp này (Q14).
- **Kiểm tỉnh táo:** trước mọi dò, `t52`, `t53`, `t54` chưa đột biến ra `qua` trên cả 20 cây dùng cho dò, đột biến
  hay Phụ lục I, và trên nền (`tinh_tao.py`, gọi `_chay_1_ca` của chính cây). Hai cây phản chứng của Phụ lục F
  (`v4_lechbo`, `v4_bocu`, mỗi cây đổi một bộ trong bảng) không chạy ca nào. Kiểu ngoại lệ của các dò tự nhiên đo riêng
  bằng một lệnh: `Path(os.fsencode(...))` ném `TypeError`; `exists()` trên khúc tên sau NFD, NFKC, NFKD ném `OSError`
  errno 36.
- **Script dò:** bản ghép Phụ lục C + H (sha256 `37b6e8bd…e55b`, đo lại) rồi Phụ lục J theo lệnh ở Phụ lục J — 401 dò,
  366 dò đầu trùng từng mục với bản ghép của r3; mỏ neo của 35 dò J xuất hiện đúng 1 lần trên nền, trên `v4_all`,
  `v4_nomem` và `v4_t5_r3` (cột `so_neo` của mọi dòng đo được = 1, trừ các dòng của §1.10.2 cố ý làm lệch). Phân hạng
  bằng hàm `hang` của Phụ lục D (không đổi).
- **Bộ chạy:** mỗi dò (hay mỗi mục `DOT_BIEN` có sẵn — `chay_muc.py`, cùng đường `_do_ban_kinh`) là một tiến trình, tối
  đa 4 tiến trình cùng lúc (`xargs -P 4`), mỗi tiến trình được `wait`; `TMPDIR` trong scratch, dọn bằng `shutil`.
  Python 3.12.3, PyYAML 6.0.1 của hệ thống, **không** `jsonschema` (nên `t2` luôn `bo_qua`).
- **Máy dùng chung:** 4 lõi; mọi tiến trình ngoài chính lệnh đo dùng 1,1–3,1 lõi trong cửa sổ đo (cột `loi_khac_dung` của
  chín lượt Phụ lục I bản r4 và hai mảnh A5 — `/proc/stat` bận trừ CPU của chính lệnh), loadavg 1 phút ghi được 1,9–7,5.
  Mọi số giây tường ở §1.10 vì vậy đo trên máy **bận**; số CPU tuyệt đối cũng trôi theo tải, tỷ lệ thì không (§1.10.5).

#### 1.10.2 Mỏ neo tự va chạm (lớp `canh-x3-wr5-nfkc-tu-va-cham-mo-neo`)

- **Nền** (`dem_neo.py`, đếm `count(mỏ neo)` trong tệp đích của từng mục): 416 mục; 413 mục là 1, ba mục `bn_*` của
  `ops/bash_nen.py` là 2, 2, 3 (`bn_khong_gap_noi_hang`, `bn_anh_chup_chi_dem_so`, `bn_bo_hang_byte`); 232 mục có tệp
  đích `ops/cong_cu_test.py`, cả 232 là 1; chỉ một mục có mỏ neo không chứa xuống dòng (`t21_git_regex_cat_hau_to`, tệp
  đích `ops/cong_cu.yaml`).
- **Phụ lục F bản r3 và bản r4 trên các biến thể** (`kiem_canh_r?.py nen <cây> <bảng nối 54 dòng> do_dot_bien.py
  do_dot_bien_r4.py`):

  | cây | bản r3: rc · `so_loi` | bản r4: rc · `dem_neo` lệch / mục | lỗi bản r4 nêu |
  |---|---|---|---|
  | `v4_all` | 0 · 0 | 0 · 0 / 470 | — |
  | `v4_lit` | 0 · 0 | 1 · 1 / 470 | `["dem-neo", "r3_x3_wr5_nfkc", 2, 1]` |
  | `v4_tq` | 0 · 0 | 1 · 55 / 470 | 11 canh r3, 24 canh r2, 20 mục cũ (vd `f34_head_no_oserror` 4, `f44_nen_ra_lower` 2, `f18_manh_n_co_dinh` 3) |
  | `v4_cu` | 0 · 0 | 1 · 1 / 470 | `["dem-neo", "f35_writer_parents", 2, 1]`; bản chỉ đếm 54 mục thêm: rc=0 |

  Răng của chính phép đếm: bản r4 với dòng `if so != mong:` đổi thành `if False:` cho `v4_lit` rc=0, 0 lỗi. Ba phản
  chứng của r3, chạy lại bằng bản r4: một canh cùng tên mà phép thay yếu hơn (`r2_s_ra_cf` chỉ bỏ U+200B) ⇒ rc=1
  `["lech-bo", "s_ra_cf", "r2_s_ra_cf"]`; một bộ cũ bị đổi (`t1_rc_gop` trỏ sang `ops/cong_cu.yaml`) ⇒ rc=1
  `["bo-cu", "t1_rc_gop"]`; bảng nối thiếu dòng cuối ⇒ rc=1 `["tap-ten", ["r3_x3_wr5_nfkc"]]`.
- **Hậu quả đo bằng đường A5** (`_do_ban_kinh`, cột `so_neo` là số lần trong tệp của cây):

  | dò hay mục | `v4_lit` | `v4_tq` | `v4_cu` | `v4_all` |
  |---|---|---|---|---|
  | dò `x3_wr5_nfkc` | KHÁC (`so_neo` 2; 9 ca `tin_dung_gia`: `t29` `t31` `t32` `t39` `t42` `t45` `t52` `t53` `t54`) | SỐNG (`so_neo` 2) | — | GIẾT `t52_` 1/56 |
  | mục cũ `f34_head_no_oserror` | — | SỐNG (`so_neo` 4) | — | GIẾT `t53_` 1/56 |
  | mục cũ `f44_nen_ra_lower` | — | SỐNG (`so_neo` 2) | — | GIẾT `t54_` 1/56 |
  | mục cũ `f35_writer_parents` | — | — | SỐNG (`so_neo` 2) | GIẾT `t52_` 1/56 (`NEM:FileNotFoundError` thành dữ liệu) |

  Ở `v4_lit` đột biến rơi vào literal một dòng nên tệp tạm không biên dịch được (ồn); ở `v4_tq` và `v4_cu` nó rơi vào
  văn bản mà tệp vẫn biên dịch được, nên đột biến thành phép thay vô hại và mục ra SỐNG — A5 vẫn đỏ ("đích vẫn XANH")
  nhưng chỉ ra sai nguyên nhân. Phép đếm của Phụ lục F bản r4 bắt cả ba dạng trước khi chạy đột biến nào.

#### 1.10.3 Ngoại lệ ở bốn chỗ gọi (lớp `m2b-o-bo-ghi-de-ngoai-le-thoat-thanh-tin-dung-gia`; M6)

- **Dò** (nhóm J-NEM của Phụ lục J, cộng `x_wr_ra_nfkc` của Phụ lục H; G = GIẾT đúng ca đích, bán kính 1/56; K = KHÁC,
  mọi K ở bảng này là `tin_dung_gia` của chính ca đích — cửa con thoát với mã khác 0; S = SỐNG):

  | dò (chỗ gọi; kiểu ném) | nền | `v4_all` | `v4_nocatch` | `v4_exc` | `v4_go_t1` | `v4_go_head` | `v4_go_main` | `v4_go_wr` |
  |---|---|---|---|---|---|---|---|---|
  | `x4_t1_thoat_ra` (`doc`; `SystemExit`) | S | G | K | K | **K** | G | G | G |
  | `x4_head_thoat` (quét `head`; `SystemExit`) | S | G | K | K | G | **K** | G | G |
  | `x4_t2_thoat_ra`, `x4_t3a_thoat_ra`, `x4_t3b_thoat_ra` (`main`; `SystemExit`) | K ×3 | G ×3 | K ×3 | K ×3 | G ×3 | G ×3 | **K ×3** | G ×3 |
  | `x4_t2_resolve_ra` (`main`; `FileNotFoundError`) | K | G | K | G | G | G | **K** | G |
  | `x4_t4_thoat_ra` (bộ ghi; `SystemExit`) | S | G | K | K | G | G | G | **K** |
  | `x4_t4_bytes_ra` (bộ ghi; `TypeError`) | S | G | K | G | G | G | G | **K** |
  | `x4_t4_nfd_ra`, `x4_t4_nfkd_ra` (bộ ghi; `OSError` tên quá dài) | S ×2 | G ×2 | K ×2 | G ×2 | G ×2 | G ×2 | G ×2 | **K ×2** |
  | `x_wr_ra_nfkc` (Phụ lục H; bộ ghi; `OSError` tên quá dài) | S | G | K | G | — | — | — | **K** |

  Đọc bảng: trên `v4_all` mọi dò GIẾT đúng ca đích; gỡ khối bắt ở **một** chỗ gọi thì đúng và chỉ các dò của chỗ ấy ra
  KHÁC (cột in đậm) — bốn khối bắt là bốn chốt có răng riêng, không phải một bộ tương đương; chỉ bắt `Exception` thì
  sáu dò `SystemExit` ra KHÁC còn bốn dò ném lớp con của `Exception` vẫn GIẾT. Trên nền, dò của T1, `head`, T4 SỐNG (ô
  của nền không có ký tự ngoài ASCII ở `ra`, ngoài BMP ở `head`), còn bốn dò của `main` ra KHÁC vì hai hàng cũ của
  `_luoi_noi_main` có ký tự ngoài ASCII mà vòng kịch bản của nền không bắt.
- **Ba dò tự nhiên của bộ ghi ném vì độ dài tên**: trong 396 khúc tên tệp phủ `D698` (3.12.3; dài nhất 201 byte UTF-8),
  số khúc vượt 255 byte sau chuẩn hoá là NFD 3, NFKC 5, NFKD 8, NFC 0 (đo bằng một vòng trên chính các khúc).

#### 1.10.4 T5 ngoài `write_bytes` và thành viên hạ nguồn (lớp `ra-ha-nguon-main-bo-ghi-chua-co-o`)

- **Mọi chỗ dùng `tep` ở T5** (đọc `_ket_thuc_manh`, :7515–:7533): `exists`, `is_symlink`, `unlink`, `parent.mkdir`,
  `write_bytes` (hai dò của r3), dòng in. Nhóm J-T5 có 10 dò cho năm chỗ ngoài `write_bytes`:

  | dò | nền | `v4_t5_r3` (một lần gọi, không so dòng in) | `v4_go_hai` | `v4_go_in` | `v4_all` | `v4_go_wr` (gỡ khối bắt ở bộ ghi; chỉ chạy dạng `nfkc`) |
  |---|---|---|---|---|---|---|
  | `x4_t5_unlink_nfkc_ra`, `…_strip_ra`, `…_cf_ra` (gỡ tệp cũ ở đường đã chuẩn hoá) | S ×3 | S ×3 | **S ×3** | G ×3 | G ×3 | K ×1 (`nfkc`) |
  | `x4_t5_in_nfkc_ra`, `…_strip_ra`, `…_cf_ra` (dòng in) | S ×3 | S ×3 | G ×3 | **S ×3** | G ×3 | G ×1 (`nfkc`) |
  | `x4_t5_mkdir_nfkc_ra`, `x4_t5_mkdir_normpath_ra` | S ×2 | G ×2 | G ×2 | G ×2 | G ×2 | — |
  | `x4_t5_exists_nfkc_ra`, `x4_t5_symlink_nfkc_ra` | S ×2 | G ×2 | G ×2 | G ×2 | G ×2 | K ×2 |

  Đọc bảng: trên cách viết của r3 (`v4_t5_r3`) đúng sáu dò gỡ tệp cũ và dòng in SỐNG — khớp review lượt 3 (đo ba dò);
  bỏ riêng lần gọi thứ hai thì đúng ba dò gỡ tệp cũ SỐNG, bỏ riêng phép so dòng in thì đúng ba dò dòng in SỐNG: hai chốt
  có răng riêng. Cột `v4_go_wr` tách cơ chế của hàng cuối: gỡ khối bắt `BaseException` ở bộ ghi thì `exists`,
  `is_symlink` và `unlink` dạng `nfkc` ra KHÁC (`t52` `tin_dung_gia`) vì `OSError` của các khúc vượt 255 byte thoát khỏi
  bộ ghi, còn dòng in dạng `nfkc` (không chạm hệ tệp) vẫn GIẾT. Nên trên `v4_all` hai dò `exists`/`is_symlink` GIẾT nhờ
  M6 (§1.10.3), không nhờ chốt nào của T5; r4 không khai răng riêng cho chúng. Dạng `strip`/`cf` của `unlink` và dòng
  in không chạy trên `v4_go_wr`.
- **Thành viên hạ nguồn** (nhóm J-TV: U+2063, U+E0020, U+FF41 — đều thuộc `D698`, không thuộc `R698 ∪ N698` — bị xoá ở
  T2, T3a, T3b, T4 hoặc T5):

  | dò (xoá một thành viên ở tầng) | nền | `v4_all` | `v4_nomem` |
  |---|---|---|---|
  | `x4_t2_{u2063,tag20,fwa}_ra` (T2, `k, n, ra = tham_so`) | S ×3 | G ×3 `t54_` | S ×3 |
  | `x4_t3a_{u2063,tag20,fwa}_ra` (T3a, lời gọi nhánh nền đỏ) | S ×3 | G ×3 `t54_` | S ×3 |
  | `x4_t3b_{u2063,tag20,fwa}_ra` (T3b, lời gọi nhánh thường) | S ×3 | G ×3 `t54_` | S ×3 |
  | `x4_t4_{u2063,tag20,fwa}_ra` (T4, `tep = Path(ra)`) | S ×3 | G ×3 `t52_` | S ×3 |
  | `x4_t5_{u2063,tag20,fwa}_ra` (T5, đường ghi) | S ×3 | G ×3 `t52_` | S ×3 |

  Đọc bảng: `v4_nomem` qua mọi ô cũ của r3 (kiểm tỉnh táo `qua`) nhưng 15/15 dò thành viên SỐNG — đúng biểu hiện "A2
  không đo thành viên ở tầng hạ nguồn" của review lượt 3 (reviewer đo 8/8 trên bốn tầng); trên `v4_all` cả 15 GIẾT đúng
  ca đích, bán kính 1/56. Ba thành viên chọn từ ba họ khác nhau của `D698` — Cf trong BMP, Cf ngoài BMP (TAG), dạng
  tương thích NFKC — để một ô chỉ phủ BMP hay chỉ phủ Cf cũng lộ; chúng không thay cho đường "mọi thành viên", chỉ đo
  rằng nó có mặt ở từng tầng.

#### 1.10.5 Chi phí: CPU, đồng hồ, mảnh A5 (lớp `t53-thoi-gian-khong-co-tieu-chi-do`)

- **Cơ sở trên runner** (đọc qua REST lúc soạn r4): run `36696528580`, tám job `gate-cong-cu (ubuntu-latest, k)` dài
  17,58 · 18,23 · 15,83 · 18,05 · 18,12 · 12,67 · 17,67 · 18,05 phút (k = 0…7); job dài nhất (k = 1) có bước G5 17,82
  phút và các bước khác 0,37 phút; kho `private`. Đó là số mà r2, r3 ghi "12,7–18,2 phút" — khớp, nay có số từng job.
- **Một mảnh A5 thật** (`chay_manh.py`: đúng lệnh A5 `CONG_CU_TEST_MANH=0/8`, tệp mảnh ngoài cây, số tiến trình con mặc
  định; CPU = `getrusage(RUSAGE_CHILDREN)` sau khi `wait`; nền rồi `v4_all`, liền nhau):

  | cây | rc · dòng mảnh | giây tường | CPU (s) | lõi khác dùng | loadavg đầu → cuối | CPU mỗi đột biến | tường mỗi đột biến |
  |---|---|---|---|---|---|---|---|
  | nền | 0 · `MẢNH 0/8: 52/52 đột biến bán kính 1` | 951,2 | 1238,7 | 2,62 | 6,31 → 6,81 | 23,82 | 18,29 |
  | `v4_all` | 0 · `MẢNH 0/8: 59/59 đột biến bán kính 1` | 1097,4 | 1803,8 | 2,20 | 6,81 → 7,46 | 30,57 | 18,60 |

  Tỷ lệ CPU mỗi đột biến 1,283 (review lượt 3, máy nhẹ tải hơn: 21,20 → 27,45, tỷ lệ 1,295); tỷ lệ giây tường mỗi đột biến
  1,017 (review lượt 3: 1,129). Trên máy bận như lúc đo của r4, giây tường gần như không phản ánh phần CPU thêm — đúng lý
  do r4 bỏ đồng hồ khỏi phép làm đỏ.
- **Phụ lục I bản r4** (`chi_phi_r4.py nen <cây>`, Python 3.12.3; "riêng" = chỉ lệnh này của phiên r4 chạy, "kèm lô 2" =
  cùng lúc với ba tiến trình dò của lô 2; cột "lõi khác dùng" tính mọi tiến trình ngoài chính lệnh — phiên khác, và ở
  các lượt kèm lô 2 cả ba tiến trình dò của phiên r4):

  | lượt | điều kiện | Δ_CPU (s) | C56 nền (s) | r | mảnh ước (phút) | Δ tường (s) | lõi khác dùng | loadavg đầu → cuối | lời gọi lớn ứng viên / nền | rc · `loi` |
  |---|---|---|---|---|---|---|---|---|---|---|
  | `v4_all` #1 | riêng | 5,96 | 22,39 | 1,266 | 26,19 | 6,24 | 3,08 | 7,24 → 6,00 | 67 / 64 | 0 · — |
  | `v4_all` #2 | riêng | 6,15 | 22,06 | 1,279 | 26,45 | 6,75 | 2,83 | 6,00 → 5,23 | 67 / 64 | 0 · — |
  | `v4_all` #3 | riêng | 6,79 | 22,05 | 1,308 | 27,05 | 7,24 | 2,41 | 5,11 → 3,88 | 67 / 64 | 0 · — |
  | `v4_all` #4 | kèm lô 2 | 6,32 | 24,44 | 1,259 | 26,03 | 5,99 | 2,66 | 2,10 → 3,67 | 67 / 64 | 0 · — |
  | `v4_all` #5 | kèm lô 2 | 6,61 | 24,08 | 1,275 | 26,36 | 6,27 | 2,97 | 3,95 → 5,34 | 67 / 64 | 0 · — |
  | `v4_all` #6 | kèm lô 2 | 7,51 | 24,53 | 1,306 | 27,02 | 9,71 | 3,01 | 5,07 → 5,31 | 67 / 64 | 0 · — |
  | `tv_naive` | riêng | 63,58 | 21,44 | 3,966 | 82,02 | 64,87 | 2,02 | 3,44 → 3,53 | 122.215 / 64 | 1 · `dem`, `cpu` |
  | `tv_cpu` (`TV_CPU_N=60000000`) | riêng | 12,80 | 24,20 | 1,529 | 31,62 | 13,13 | 2,04 | 3,52 → 3,71 | 67 / 64 | 1 · `cpu` |
  | `tv_cham` | riêng | 4,66 | 23,36 | 1,200 | 24,81 | 15,75 | 1,12 | 3,86 → 1,93 | 67 / 64 | 0 · — |

  Đọc bảng. (a) Trên cùng một ứng viên, sáu lượt cho Δ tường 5,99–9,71 s và Δ_CPU 5,96–7,51 s — CPU tuyệt đối cũng trôi
  theo tải (máy chia lõi cho 1–3 lõi của phiên khác; C56 của nền đi từ 22,05 s lên 24,53 s) — còn tỷ lệ r, chia cho C56 của
  chính lượt, chỉ đi từ 1,259 tới 1,308: đại lượng mà mô hình cần thì ổn định, đại lượng tuyệt đối thì không. Đó là lý do
  phép làm đỏ là r ≤ 1,35 chứ không phải một số giây. (b) r trung bình 1,282 khớp tỷ lệ CPU mỗi đột biến của hai mảnh thật
  (1,283), nên C56 là thước đúng cho một lượt đột biến; C56 (21,44–24,53 s) nhỏ hơn C₀ của mảnh (23,82 s) vì mỗi lượt
  đột biến trong mảnh còn dựng cây tạm — tính với C56 cho r lớn hơn, tức thận trọng. (c) Hai phép làm đỏ có răng riêng:
  `tv_naive` đỏ cả `dem` lẫn `cpu`; `tv_cpu` chỉ đỏ `cpu` (lời gọi lớn 67/64, không đổi). (d) `tv_cham` — bản chậm vì
  **ngủ** 11 s, dựng trên `cand` của r2 nên Δ_CPU nhỏ hơn `v4_all` — qua: phép CPU không thấy thời gian ngủ, chỉ Δ tường
  (15,75 s) thấy; giới hạn khai ở §10. (e) Ở cả sáu lượt, `v4_all` qua với biên 3–7% dưới ngưỡng 1,35; một bản thi công
  tốn CPU hơn biến thể đo chừng ấy thì A4-g đỏ — đó là chủ đích của ngưỡng, không phải đỏ giả.


#### 1.10.6 Bậc hai của A8 (lớp `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan`)

Ba cây gỡ của `v4_all` (mỗi cây chỉ khác `v4_all` ở phần gỡ, kiểm tỉnh táo `qua`), cùng mười dò: bảy dò `z_exc_*` của
Phụ lục C (năm mở rộng, hai thu hẹp là đối chứng) và ba dò cùng tên ba canh E của r3 (Phụ lục H). G = GIẾT `t53_`, bán
kính 1/56; S = SỐNG.

| dò | `v4_go_e698` (gỡ miền `E698`) | `v4_go_r2exc` (gỡ ba ô của r2) | `v4_go_exc2` (gỡ cả hai) |
|---|---|---|---|
| `x_exc_typeerror`, `x3_exc_kbint`, `x3_exc_re_error` (canh E của r3) | S ×3 | G ×3 | S ×3 |
| `z_exc_all`, `z_exc_base`, `z_exc_them_valueerror`, `z_exc_them_unicode`, `z_exc_them_runtime` (năm dò mở rộng; `z_exc_all` và `z_exc_them_valueerror` là dò của hai canh E r2) | G ×5 | G ×5 | S ×5 |
| `z_exc_oserror_only`, `z_exc_subproc_only` (thu hẹp — đối chứng) | G ×2 | G ×2 | G ×2 |

Đọc bảng: hai canh E của r2 (`z_exc_all`, `z_exc_them_valueerror`) có **hai** nguồn giết trên ứng viên r4 — ba ô của r2
và miền `E698` (vốn chứa `ValueError`, `UnicodeDecodeError`, `RuntimeError`) — nên gỡ **riêng** một nguồn thì chúng vẫn
GIẾT, chỉ gỡ **cả hai** mới SỐNG lại; ba canh E của r3 chỉ có một nguồn (miền `E698`), nên gỡ riêng miền ấy là đủ. Mệnh
đề cũ của A8 ("gỡ riêng ba ô ⇒ hai canh E của r2 SỐNG lại") chỉ đúng trên IMP-R2-GO của r2, nơi chưa có `E698` — đúng
như review lượt 3 đo trên ứng viên của nó (`ind2`, `var_go_exc`, `var_go_both`). Hai đối chứng GIẾT trên cả ba cây, vì
chúng thu hẹp tập bắt mà các ô sẵn có (`OSError`, `SubprocessError`, `TimeoutExpired`) đã đo.

#### 1.10.7 Tên và số của lời khai (lớp `r3-khai-ve-hint-va-ten-canh-khong-khop-hien-vat`)

- **Số ngưỡng của HINT lượt 2:** `grep -c -i` cụm từ cũ của r3 trên r3 = 4 dòng (đúng bốn chỗ reviewer lượt 3 nêu), trên
  r4 = 0. Bốn câu ấy nay viết "hai ngưỡng" theo `HINT.patch` lượt 3.
- **Tên dò và tên canh trong code span** (`kiem_ten.py`: lấy mọi code span ngoài khối mã có dạng tên dò, tra vào bảng `P`
  của Phụ lục A và bản ghép C + H + J, vào tên mục `DOT_BIEN` của nền, vào tên canh `r2_<dò>`/`r3_<dò>` của biến thể đo,
  và qua dòng ánh xạ của §1.8.7): r4 có 249 tên; 150 có thẳng trong một phụ lục hay trong `DOT_BIEN` của nền, 18 là tên
  canh của biến thể đo, 20 tra qua dòng ánh xạ, 31 là mẫu có `*`/`{`, 14 là tiền tố luật tên (vd `x3_m3a_ra_`), 14 là
  tên hoặc mẫu `y_*` của reviewer lượt 3 — nằm ngoài các phụ lục (§1.10.8), tra riêng vào `extra_rv3.py` của
  `evidence/`: 9 tên cụ thể đều có, 5 mẫu (kể cả chính `y_*`) mẫu nào cũng khớp ít nhất một dò; còn lại hai mẫu không
  tra được và **có chủ đích**: `f49_*`, `f50_*` (mẫu tên mục `DOT_BIEN` của IMP-R2 mà chính dòng ánh xạ giải thích).
  Cùng phép tra trên r3: 16 tên `f49_*`/`f50_*` cụ thể, tất cả ở §1.8.7, đều tra được qua dòng ánh xạ của HINT lượt 3
  và **không** tra được nếu bỏ dòng ấy — tức dòng ánh xạ phủ đủ.
- **"tên r1":** `grep -c f49_nfkc_bk` trên r1 = 0 (trên r2, r3 có); §5 của r1 chỉ gợi ý tiền tố `f49_`/`f50_` cho tên mục.
  Câu của HINT được sửa (§0 điểm 6).

#### 1.10.8 Hồi quy trên `v4_all`, kích thước, A4 tĩnh

Mọi phép dưới đây chạy trên `nen` (`fc852ff`, clone `--shared` cục bộ) và `cay/v4_all` của giàn §1.10.1, Python
3.12.3, `PYTHONDONTWRITEBYTECODE=1`, chiều 07-10. Hai cây chỉ khác nhau ở `ops/cong_cu_test.py`
(`diff -rq --exclude=.git nen cay/v4_all` ⇒ đúng một dòng, tệp ấy) — đây cũng là phép đo A4-f trên biến thể, vì
`v4_all` không phải một commit để chạy `git diff --name-only`.

- **Hồi quy các dò đã có trên `v4_all`** (bản ghép C + H + J, mỗi dò một tiến trình, tối đa ba tiến trình cùng lúc;
  125 dò và mục):

  | nhóm | số | GIẾT | SỐNG | KHÁC | ghi chú |
  |---|---|---|---|---|---|
  | T-C của Phụ lục C (T1) | 41 | 40 | 0 | 1 | KHÁC: `s_ra_realpath` (bán kính 2, đối chứng, như nền) |
  | T-C của Phụ lục H (T2–T5) | 40 | 38 | 1 | 1 | SỐNG: `x3_wr5_normpath` (tương đương đã khai, §6); KHÁC: `x3_wr_ra_lower` (`tin_dung_gia`, đối chứng, §1.9.5) |
  | dò cùng tên với 11 canh r3, ngoài T-C (T-B 3, T-E 3) | 6 | 6 | 0 | 0 | `x_head_nl_last`, `x3_head_emsp_last`, `x_cat_mc_bk`, `x_exc_typeerror`, `x3_exc_kbint`, `x3_exc_re_error`; năm dò cùng tên còn lại nằm trong T-C ở hai hàng trên, đều GIẾT |
  | Phụ lục J | 35 | 35 | 0 | 0 | §1.10.3, §1.10.4 |
  | mục cũ `f34_head_no_oserror`, `f35_writer_parents`, `f44_nen_ra_lower` (đường A5) | 3 | 3 | 0 | 0 | §1.10.2 |

  Theo từng hàng tầng của bảng §1.9.5 (`x_main_ra_*` 6 · `x3_main_ra_*` 9 · `x3_m3a_ra_*` 6 · `x3_m3b_ra_*` 6 ·
  `x_wr_ra_*` 6 · `x3_wr_ra_*` 5 · `x3_wr5_*` 2), `v4_all` cho đúng hạng và đúng tên ngoại lệ của cột `v3_all`: r4
  không làm sống lại dò T-C nào. T-B, T-D, NGOÀI, KHAI và phần còn lại của T-E thuộc C + H **không** chạy trên
  `v4_all` (r3 cũng chỉ chạy trên `v3_all` 158 dò thuộc các nhóm `exc`, `head`, `ra`, §1.9.1); phần r4 thêm chỉ chạm
  bốn chỗ gọi (khối bắt), T5 và bảng canh, và r4 không khai gì cho những dò chưa chạy (§10).
- **28 dò `y_*` của reviewer lượt 3, chạy đối chiếu** (`python3.12 -I -B extra_rv3.py cay/v4_all <ra> <dò>`, tệp
  của `evidence/scripts/`, sha256 `c1e3d1e8…426f`; bốn tiến trình): **27 GIẾT + 1 SỐNG**. Dò SỐNG là `y_exc_shutil`,
  đúng dò mà verdict lượt 3 đã xếp tương đương (`issubclass(shutil.Error, OSError)` ⇒ `True`, đo lại lúc soạn r4).
  Ba dò T5 mà verdict đo SỐNG trên ứng viên của nó (`y_wr5_unlink_nfkc`, `y_wr5_print_nfkc`, `y_wr5_print_strip`)
  GIẾT trên `v4_all`, cùng `y_wr5_mkdir_nfkc`, `y_wr5_mkdir_normpath`, `y_wr5_exists_nfkc`; 6/6 `y_head_*`, 8/8 dò
  thành viên (`y_main_ra_*` ×3, `y_wr_ra_*` ×3, `y_m3a_ra_u2063`, `y_m3b_ra_u2063`), 5/6 dò ngoại lệ một bước (họ
  `y-exc` của tệp) và 2/2 `y_exc_hai_buoc_*` GIẾT, mỗi dò đúng ca đích, bán kính 1/56.
- **Kích thước:** `git diff --no-index --numstat nen/ops/cong_cu_test.py cay/v4_all/ops/cong_cu_test.py` ⇒ `291 4`.
- **A1 (iv):** lệnh của A1 (iv) in `0 0 ['0x2026']` trên cả `nen` lẫn `v4_all`.
- **A4 tĩnh:**

  | phép | `nen` | `v4_all` | kết luận |
  |---|---|---|---|
  | (a) `CONG_CU_TEST_BAN_KINH=manh python3.12 ops/cong_cu_test.py` | `55/55 đạt; tổng=56, bỏ qua=1`, `đột biến=416 (giao mảnh) · lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0 | như nền, trừ `đột biến=470 (giao mảnh)`; rc=0 | xanh (ca bỏ qua là `t2`, thiếu `jsonschema`) |
  | (b) `ruff check --select F` bằng ruff 0.15.8 | 1 lỗi: `F841 Local variable ci is assigned to but never used` (:2606) | cùng 1 lỗi ấy (:2670) | đa tập (mã, thông điệp) bằng nhau; bản ghim 0.15.15 KHÔNG ĐO ĐƯỢC (§10) |
  | (c) `python3.12 .claude/dev/ci_dang_ky_test.py` | `PHẢN CHỨNG: 1025/1025 đỏ đúng`, `TỔNG: ĐẠT`, rc=0 | như nền | delta 0 |
  | (d) Phụ lục G `giao_a4d_r3.py cay/v4_all fc852ff…` | — | `hunk` 16, `cham` rỗng, rc=0 | xanh |
  | (e) Phụ lục E `ast_dot_bien_r2.py` | `tong` 9, `truoc_anh` [2256, 2262], `trong_cua_so` 7, `sau_moc` rỗng | `tong` 10, `truoc_anh` [2256, 2262, 2327], `trong_cua_so` 7, `sau_moc` rỗng | xanh; dòng 2327 là vòng đăng ký canh wp698, trượt 11 dòng so với 2316 của `v3_all` đúng bằng 11 hàng canh r3 |

  Đồng hồ tường của (a), chỉ báo trên máy dùng chung (không làm tiêu chí): `nen` 227 s, `v4_all` 324 s, hai lượt
  liền nhau 15:19:26–15:28:37Z; loadavg một phút đọc hai lần trong lúc ấy là 4,78 và 6,59 trong khi phiên này chỉ
  chạy một tiến trình đo, tức phần lớn tải là của tiến trình khác.

## 2. Đường vào: liệt kê HẾT trước khi vá

Áp bài học *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*: danh sách dưới đây do phiên soạn tự
dựng từ mã, không chép từ verdict. r1 dựng 24 đường sống trong 4 lớp; review lượt 1 chỉ ra 8 lớp /
52 biểu hiện mà danh sách ấy thiếu. r2 **không** vá theo 52 biểu hiện được chỉ: nó dựng lại danh
sách theo **ba trục** — bộ đọc × họ phép × (vị trí, thành viên) — rồi đo từng ô của tích ấy. Review
lượt 2 chỉ ra 16 lớp / 56 biểu hiện, trong đó ba lớp P2 là đường mà danh sách của r2 thiếu theo **tầng
dòng chảy** của giá trị (tập kiểu ngoại lệ, `ra` sau `_doc_che_do`, cấu trúc nhiều dòng của `head`). r3 thêm
trục thứ tư — **tầng** mà giá trị đi qua sau bộ đọc — và trục thứ năm cho bộ đọc: **nguồn** (`os.environ`,
tiến trình ngoài, tệp, và — thiếu ở r2 — `sys.argv`). Review lượt 3 chỉ ra hai lớp P2 nằm ở **giàn đo** chứ không ở mã
bị đo: một ngoại lệ của mã bị đo thoát khỏi ô thành tín dụng giả, và một mỏ neo bị văn bản mới đứng trước nó kéo đi. r4
thêm vì vậy hai trục cho chính giàn đo: **chỗ gọi** — mọi chỗ mà ô mới gọi mã bị đo (bốn chỗ cộng M5b, §5 M6) — và
**mục** — mọi mục `DOT_BIEN` có mỏ neo trong tệp test (286 mục), không chỉ 54 canh; cộng một trục cho tầng T5: **mọi
chỗ dùng** `tep` (sáu chỗ).

**Bộ đọc cùng họ** (đọc một giá trị do môi trường, tiến trình ngoài hoặc tệp đưa vào, rồi nhận hay
từ chối bằng so khớp). Trên nền, `grep -c -E` với các mẫu `os.environ`, `env.get`, `getenv` cho 61
dòng; bỏ các ca test tự đặt môi trường cho mình, các chuỗi đột biến và oracle `_mong_che_do`, còn
đúng hai chỗ đọc thật: `_doc_che_do` (:7468, ba biến) và `_so_tien_trinh_ban_kinh` (:7092). Cộng
hai bộ đọc không đi qua môi trường — stdout của `git` trong `_van_tay` và đầu tệp mảnh trong
`_gom_manh` — thành sáu. **r3** đếm thêm nguồn `sys.argv`: `grep -n "sys.argv"` trên nền ra bốn chỗ đọc thật
ngoài chuỗi fixture — `--ban-kinh-con` (:7281, giao thức cha–con nội bộ, cùng loại `BKCON`), `--gop <thư mục>`
(:7610), `--tu-kiem-cong-that` (:8187, cửa tự kiểm nội bộ) và chọn cửa ở `argv[1]` (:8384). Hai chỗ nhận giá trị
từ ngoài (workflow gọi `--gop manh`; cửa ở `argv[1]`) được thêm vào bảng — thành tám:

| bộ đọc | hàm | lớp | r2 |
|---|---|---|---|
| `CONG_CU_TEST_BAN_KINH` (`bk`) | `_doc_che_do` | B | mục tiêu (M1) |
| `CONG_CU_TEST_MANH` (`mh`) | `_doc_che_do` | B | mục tiêu (M1) |
| `CONG_CU_TEST_MANH_RA` (`ra`) | `_doc_che_do` | B và C | mục tiêu (M1, M2) — lớp `ra-thieu-hang-chuan-hoa-lop-b` |
| stdout của `git rev-parse HEAD` (`head`) và tập ngoại lệ bắt | `_van_tay` | B và E | mục tiêu (M1, M5) |
| `CONG_CU_TEST_TIEN_TRINH` | `_so_tien_trinh_ban_kinh` | ngoài B | nợ `so-tien-trinh-nhan-fullwidth` (Q2) |
| đầu tệp mảnh (`head`, `sha256_test`) so với vân tay của chính tiến trình gom | `_gom_manh` | ngoài B | nợ `gom-dau-manh-chuan-hoa-wp698` |
| thư mục sau `--gop` | `_main_gop` | ngoài B (r3) | nợ `doc-argv-chua-co-o-wp698` (§1.9.6) |
| cửa ở `argv[1]` | khối `__main__` | ngoài B (r3) | nợ `doc-argv-chua-co-o-wp698` (§1.9.6) |

Ranh giới lớp B: bộ đọc **cấu hình qua biến môi trường và vân tay của chính tiến trình**, đúng phạm vi F49
(§11.1 điểm 1); hai bộ đọc `argv` nằm ngoài vì F49 không nói tới `argv` (Q1), nên chúng được đo và ghi nợ như hai
bộ đọc ngoài lớp khác (§11.1 điểm 15).
Bộ gom so bằng dữ liệu do tiến trình khác ghi, và `CONG_CU_TEST_TIEN_TRINH` đã là nợ của chủ kho;
cả hai được **đo** (hàng Z1, Z2 dưới), không để "KHÔNG ĐO". Các bộ phân tích giao thức con–cha
(`_nhan_ket_qua_con`, dòng `BKCON`) không đọc giá trị cấu hình hay vân tay nên không thuộc họ này.

**Bảng đo** (Phụ lục C, 221 dò). "SỐNG" = không ca nào chết; cột IMP-R2F KHÁC đếm dò chết sai lý
do. Bốn cột đầu đo bằng Python 3.11.15: 209 dò lúc 22:39:52Z 30-09 – 00:08:24Z 01-10, 12 dò
"nhóm ngoài `D698`" trong lô cuối (từ 00:53:07Z 01-10); với nền, IMP-MIN và IMP-GEN, 47 dò của reviewer đo bằng
chính script của reviewer (`do_dot_bien3.py`, định nghĩa khớp từng byte với Phụ lục C). Cột IMP-R2
là bản trước IMP-R2F (thiếu `N698`), nên 8 trong 12 dò mới (`m_co_*`, `m_cn_*`) SỐNG ở đó — đúng lý do
thêm `N698`; 4 dò `m_lo_*` thì chết sẵn vì `D698` đã có ký tự `Lo` có NFKC khác chính nó. Cột IMP-R2F
đo **trọn 221 dò** trên ứng viên cuối bằng Python 3.12.3 ngày 01-10 — 156 dò 01:07:00Z–01:30:54Z, lệnh
nền bị dừng ở trần 2 giờ (§1.8.1), 65 dò còn lại 01:39:51Z–01:49:11Z:

| họ | dò | đối chứng | nền SỐNG | IMP-MIN SỐNG | IMP-GEN SỐNG | IMP-R2 SỐNG | IMP-R2F SỐNG (3.12) | IMP-R2F KHÁC (3.12) |
|---|---|---|---|---|---|---|---|---|
| B Cc ngoài TAB | 3 | 2 | 1 | 1 | 1 | 0 | 0 | 0 |
| B Zs ngoài ASCII | 7 | 0 | 7 | 7 | 7 | 0 | 0 | 0 |
| B `head` strip hẹp | 2 | 0 | 2 | 2 | 1 | 0 | 0 | 0 |
| B dấu kết hợp | 6 | 0 | 6 | 6 | 6 | 0 | 0 | 0 |
| B phép khác (strip, lower, casefold, chữ số Unicode trong regex, NFKD) | 5 | 4 | 1 | 0 | 0 | 0 | 0 | 0 |
| B nhóm ngoài `D698` (Lo, Co, Cn) | 9 | 0 | 9 | 9 | 9 | 6 | 0 | 0 |
| B thành viên Cf | 18 | 0 | 18 | 15 | 6 | 0 | 0 | 0 |
| B thành viên NFKC | 13 | 0 | 13 | 10 | 8 | 2 | 2 | 0 |
| B từng chỉ số (Cf) | 76 | 0 | 76 | 73 | 63 | 0 | 0 | 0 |
| B vị trí đầu/cuối/giữa (Cf, TAB) | 16 | 0 | 16 | 10 | 0 | 0 | 0 | 0 |
| C `ra` × NFKC/Cf/TAB toàn chuỗi | 3 | 0 | 3 | 3 | 0 | 0 | 0 | 0 |
| C `ra` × phép đường dẫn/chuỗi | 11 | 1 | 10 | 8 | 3 | 0 | 0 | 1 |
| C `ra` × thành viên và họ ký tự | 17 | 0 | 17 | 17 | 14 | 2 | 0 | 0 |
| C `ra` × vị trí (đầu/cuối/giữa, từng chỉ số) | 10 | 0 | 10 | 10 | 7 | 0 | 0 | 0 |
| D vị từ một biến (trục) | 4 | 1 | 3 | 0 | 0 | 0 | 0 | 0 |
| D vị từ nhiều biến (tích) | 8 | 0 | 8 | 8 | 8 | 0 | 0 | 0 |
| E tập bắt ngoại lệ `_van_tay` | 7 | 2 | 5 | 5 | 5 | 0 | 0 | 0 |
| Z1 ngoài lớp: đầu tệp mảnh `_gom_manh` | 4 | 0 | 4 | 4 | 4 | 4 | 4 | 0 |
| Z2 ngoài lớp: `CONG_CU_TEST_TIEN_TRINH` | 2 | 0 | 2 | 2 | 2 | 2 | 2 | 0 |
| **tổng** | 221 | 10 | 211 | 190 | 144 | 16 | 8 | 1 |

Đọc bảng:

- **Nền** (`fc852ff`): 205 dò sống ngoài hai hàng Z (211 kể cả Z, khớp hàng tổng), tức mọi họ đều có đường sống
  trước bản vá — tiêu chí không thể xanh trên nền.
- **IMP-MIN, IMP-GEN** (hai ứng viên "thoả chữ r1" của reviewer lượt 1): 184 và 138
  dò sống ngoài hai hàng Z (190 và 144 kể cả Z). Tiêu chí r1 xanh trên cả hai (reviewer lượt 1 đo: 16/16 dò mục tiêu của r1 bị giết đúng
  ca đích trên cả hai); tiêu chí r2 đỏ trên cả hai.
- **IMP-R2F** (Python 3.12.3): 2 dò sống ngoài hai hàng Z. Hai dò ấy là `m_nfkc_no_bk` và `m_nfkc_khac_bmp_mh`, đúng hai dò mà phép vét cạn ở §1.8.8 chứng minh tương đương (không điểm mã nào của tập con có NFKC là đoạn con hợp lệ của bộ đọc) — chúng sống vì không thể chết, không vì thiếu ô. Mọi dò còn lại của T-B, T-C, T-D, T-E: GIẾT đúng ca đích, bán kính 1/56, trừ đối chứng `s_ra_realpath` giữ nguyên hạng KHÁC (giết `t53` và `t54`, bán kính 2) như trên nền — cùng hình dạng với `c49_ra_abspath` của Phụ lục A.
- **Đối chứng** (bị giết ngay trên nền, không đo răng của bản vá): 10 dò — `s_bk_strip` (ô nền ` manh`), `s_bk_lower` và `s_bk_casefold` (ô `MANH`), `s_mh_digit_d` (ô chữ số Ả Rập `so_la`), `m_cc_bk` và `m_cc_mh` (ô `manh` và `0/8` kèm xuống dòng — LF là Cc), `s_ra_realpath` (bán kính 2), `s2_hong_lt_n`, `z_exc_oserror_only`, `z_exc_subproc_only`. `s_bk_casefold` trả lời mục "casefold trên dạng fullwidth: chưa đo" mà HINT để lại: casefold bị ô `MANH` của nền giết; dạng fullwidth hoa casefold ra fullwidth thường, vẫn bị từ chối, nên không mở đường nào ngoài NFKC (đã có dò riêng).
- **Tương đương** (không đầu vào nào phân biệt được với nền): `m_nfkc_no_bk`, `m_nfkc_khac_bmp_mh` (vét cạn §1.8.8, cả Python 3.11.15 lẫn 3.12.3).

**Bảng đo r3** (Phụ lục H, 145 dò; Python 3.12.3; hạng theo Phụ lục D; số liệu chi tiết từng nhóm ở §1.9.3–§1.9.7):

| tập (Phụ lục D) | dò | nền SỐNG | `cand` SỐNG (đúng chữ r2) | biến thể đúng hướng HINT SỐNG | `v3_*` từng hướng SỐNG | `v3_all` SỐNG |
|---|---|---|---|---|---|---|
| T-B | 68 | 62/68 (KHÁC 1) | 23/68 (KHÁC 1) | 6/65 (KHÁC 1) | 0/41 | 0/68 (KHÁC 1) |
| T-C | 40 | 37/40 (KHÁC 1) | 37/40 (KHÁC 1) | — | 1/40 (KHÁC 1) | 1/40 (KHÁC 1) |
| T-D | 4 | 2/4 | 0/4 | — | — | 0/4 |
| T-E | 23 | 23/23 | 22/23 | 7/23 | 0/23 | 0/23 |
| ngoài lớp | 5 | 5/5 | 5/5 | — | 5/5 | 5/5 |
| KHAI | 5 | 5/5 | 5/5 | — | 3/3 | 5/5 |

Ô `a/b (KHÁC k)`: a dò SỐNG trong b dò đã đo trên các cây của cột, k dò hạng KHÁC; — là không đo. Cột "biến thể
đúng hướng HINT" gộp `tv_exc` (T-E), `tv_head` (38 dò `head` của T-B, không gồm sáu dò E3/E4) và `tv_list` (27 dò
xoá-nhóm của T-B). Cột `v3_*` gộp `v3_exc` (T-E), `v3_head` (44 dò `head`, gồm ba dò KHAI) và `v3_ra` (T-C, ngoài
lớp); T-D không thuộc hướng nào của r3 nên chỉ đo trên nền, `cand` và `v3_all`.

Đọc bảng (phần Phụ lục H):

- **Đối chứng** (bị giết ngay trên nền): 11 — họ `head`: `x_head_split_last`, `x_head_split_first`, `x3_head_longest` (ô `hop + " " + hop` của nền); tầng `main`: `x3_main_ra_lower`, `x3_main_ra_nfd` (ô `Mixed.TXT`, `dir/Sub Dir/Mảnh.TXT`); bộ ghi: `x3_wr_ra_lower` (KHÁC — tín dụng giả vì hỏng giàn giáo của `t52`, giữ hạng KHÁC); nhóm Unicode: `x3_cat_cc_bk`, `x3_cat_zs_bk` (GIẾT) và `x3_cat_ll_bk` (KHÁC, bán kính 2, giữ hạng KHÁC); T-D: `x_f50_h_ge2`, `x_f50_tk_ge2`.
- **Tương đương** (không đầu vào nào phân biệt được với nền theo cấu tạo): `x3_wr5_normpath` — trên mọi đường không có symlink (§5 M2b, §1.9.5).
- **KHAI** (SỐNG có chủ đích, lý do ở §6): `x_head_cf2063_at17`, `x_head_cfk_mid_only`, `x_head_sm_mid_only`,
  `x_f50_tk_and_bq_ne3`, `x_f50_h_and_bq_ne3`.
- **Ngoài lớp** (nợ `doc-argv-chua-co-o-wp698`): `x3_gop_dir_normpath`, `x3_gop_dir_nfkc`, `x3_gop_dir_strip`, `x3_cua_strip`, `x3_cua_nfkc` — SỐNG 5/5 ở nền, `cand`, `v3_ra` và `v3_all` (§1.9.6).

**Bảng đo r4** (Phụ lục J, 35 dò; Python 3.12.3; hạng theo Phụ lục D; chi tiết từng cây ở §1.10.3–§1.10.4):

| nhóm (Phụ lục J) | dò | tập | nền SỐNG / KHÁC | `v4_all` GIẾT | biến thể thiếu đúng phần ấy |
|---|---|---|---|---|---|
| J-NEM: ngoại lệ ở bốn chỗ gọi | 10 | T-C 9 · T-B 1 | 6 / 4 | 10 | `v4_nocatch` 10 KHÁC; mỗi `v4_go_<chỗ gọi>` KHÁC đúng các dò của chỗ ấy |
| J-T5: chỗ dùng `tep` ngoài `write_bytes` | 10 | T-C 10 | 10 / 0 | 10 | `v4_t5_r3` 6 SỐNG; `v4_go_hai` 3 SỐNG; `v4_go_in` 3 SỐNG |
| J-TV: thành viên ngoài `R698` × T2–T5 | 15 | T-C 15 | 15 / 0 | 15 | `v4_nomem` 15 SỐNG |

Không dò nào của Phụ lục J là đối chứng hay tương đương; không dò nào thuộc tập KHAI.

Lớp A (F48) giữ nguyên như r1: 8 dò sau/trước cửa sổ sống, đối chứng `c48_trong_cua_so` bị giết
(Phụ lục A); **không** vào r2, nợ `registry-nang-luc-ngoai-cua-so` (Q1).

## 3. `write_set`

- `ops/cong_cu_test.py`

Không có đường dẫn nào khác. Căn cứ: mọi ca đích (`t53`/`t54`), mọi miền ô (`_luoi_che_do`,
`_luoi_git`, `bang_env`, miền dẫn xuất M1, kịch bản của `_in_tu_kiem_main`), bảng `DOT_BIEN` và
mọi hàm bị đột biến đều nằm trong tệp này. `ci.yml` không đổi, vì r2, r3 và r4 không thêm job hay biến môi
trường. `.claude/dev/ci_dang_ky_test.py` cũng không đổi, vì hình dạng G5 giữ nguyên. Bản thân đặc
tả này và các phụ lục của nó là hồ sơ của lượt soạn spec, **không** thuộc write set của lượt thi hành.

## 4. `ngoai_pham_vi`

| thứ | lý do |
|---|---|
| Lớp A (F48 và đường (e)) | Chủ kho quyết không gộp (Q1). Ghi nợ `registry-nang-luc-ngoai-cua-so`; muốn đóng thì mở packet riêng. |
| `_so_tien_trinh_ban_kinh`: mức mã nhận fullwidth và ném ở chữ số mũ; mức đo không có ô cho Cf/TAB | Chủ kho quyết ghi nợ `so-tien-trinh-nhan-fullwidth` (Q2). r2 đo thêm hai dò mức đo (`t_cf`, `t_tab`, §1.8.6): SỐNG 2/2 trên nền. Cả hai thuộc cùng nợ ấy; A4-d vẫn cấm đổi thân hàm. |
| Đầu tệp mảnh của `_gom_manh` (so `head`/`sha256_test` với vân tay của chính tiến trình gom) | Bộ đọc ngoài lớp B theo định nghĩa ở §2 (nó so bằng, không đọc cấu hình). r2 đo bốn dò (`g_*`, §1.8.6): SỐNG 4/4 trên nền. Ghi nợ `gom-dau-manh-chuan-hoa-wp698` (§11.1). |
| Hai bộ đọc `argv` (thư mục `--gop`, cửa ở `argv[1]`) | Ngoài lớp B theo ranh giới ở §2 (F49 không nói tới `argv`, Q1). r3 đo các dò `x3_gop_*`, `x3_cua_*` (§1.9.6) và ghi nợ `doc-argv-chua-co-o-wp698` (§11.1 điểm 15). |
| Patch-as-hint chứa mã và các hint của lượt 22 | Chủ kho quyết không dùng patch-as-hint; reviewer chỉ mô tả hướng (Q14). `HINT.patch` văn bản của review lượt 1, lượt 2 và lượt 3 đã được áp và sửa tiếp (§0-r2, §0-r3, §0). Hồ sơ lượt 22 đưa lên nhánh `ops/**` chỉ để làm hồ sơ, không làm đầu vào (Q13). |
| Đẩy hoặc merge `8d7faef` / `5a071b8` | Không có trong kho, và không có lease. |
| Chạy Windows (`workflow_dispatch` hay nhãn `windows`) | Chủ kho quyết không (Q8); nợ `windows-chua-do-o-moi-wp698`. |
| CI trong vòng lặp vá–review | Chủ kho quyết không; CI chỉ chạy một lần khi mở PR sau lúc review sạch (Q7). |
| Đổi thân `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`, `_chay_1_ca` | §1.3–§1.5 và §1.8 đo được rằng chúng đúng với oracle; khe nằm ở ô đo, không ở mã. Đổi ⇒ S1. Hành vi "ngoại lệ ngoài tập bắt thì lọt" của `_van_tay` là hành vi nền; r2 chỉ ĐO nó (M5). |
| `ci.yml`, `ci_dang_ky_test.py`, ruleset | Không cần cho mục tiêu r2. |
| Nợ `ops/nhanh_don_duoc_test.py` sát trần trong `gate-registry` | Nợ của #668 (quyết định `5910229584`). Packet này chỉ **gặp** nó và xử lý theo Q9, không sửa. |

## 5. `muc_tieu`

Mỗi mục chiếu vào đúng một đường dẫn trong write set (L2): `ops/cong_cu_test.py`.

1. **M1 (lớp B — miền dẫn xuất cho bốn bộ đọc `bk`, `mh`, `ra`, `head`).** Thêm vào cửa con của
   `t53` (`--tu-kiem-che-do`) một phép quét trên miền sau, so với oracle độc lập:
   - **Tập điểm mã `D698`**: mọi điểm mã `c` trong `0…0x10FFFF`, trừ surrogate `U+D800…U+DFFF`,
     sao cho `unicodedata.category(chr(c))` **không** thuộc {`Lo`, `Co`, `Cn`} **hoặc**
     `unicodedata.normalize("NFKC", chr(c)) != chr(c)`. Tập được **dẫn xuất từ thuộc tính** lúc
     chạy, không liệt kê tay (đảo danh sách CẤM thành một luật CHO PHÉP thử). Nó chứa mọi Cc, Cf
     (kể cả TAG ngoài BMP), Zs/Zl/Zp, Mn/Mc/Me, chữ có hoa–thường, chữ số mọi hệ, dấu câu, ký hiệu,
     và mọi ký tự có ánh xạ tương thích NFKC. Kích thước đo (§1.8.8): **19.588** trên Python 3.11.15
     (Unicode 14.0.0), **19.798** trên Python 3.12.3 (Unicode 15.0.0).
   - **Tập đại diện `R698`** (13 điểm mã, mỗi họ ít nhất một): U+200B, U+FEFF, U+200E, U+00AD,
     U+061C, U+E0001 (Cf); U+0009 (TAB); U+00A0, U+3000 (Zs); U+0301 (Mn); U+000B (Cc);
     U+00B2, U+FF10 (NFKC khác chính nó).
   - **Ba điểm mã ngoài `D698`** (`N698`), một đại diện cho mỗi nhóm bị loại: U+4E00 (`Lo`), U+E000
     (`Co`), U+0378 (`Cn`, chưa gán ở cả Unicode 14.0.0 lẫn 15.0.0 — đo). Chúng có NFKC bằng chính
     nó nên không thuộc `D698`; thiếu chúng thì một phép chuẩn hoá xoá cả một nhóm ấy không bị bắt.
   - **Giá trị hợp lệ chuẩn**: `bk` = `manh`; `mh` = `3/8` và `15/16` (kèm `ra` = `x`); `ra` = `a/b`
     (kèm `mh` = `3/8`); `head` = 40 và 64 ký tự đầu của chuỗi `0123456789abcdef` lặp lại, làm
     stdout của `git` giả (như lưới `_luoi_git`).
   - **Vị trí**: giá trị dài ≤ 5 ký tự ⇒ mỗi điểm mã của `D698` được **chèn** ở mọi vị trí
     `0…len` và **thay** ở mọi vị trí `0…len−1`. Hai giá trị `head` ⇒ `D698` ở ba vị trí neo
     (chèn đầu, chèn cuối, thay ở chỉ số `len // 2`), cộng `R698` ở **mọi** vị trí chèn và thay.
     `N698` ở **mọi** vị trí chèn và thay của **mọi** giá trị chuẩn.
   - **Kỳ vọng** từ oracle có sẵn: `_mong_che_do` cho `bk`/`mh`/`ra` (so sau vòng JSON như `t53`),
     `_mong_git(0, v, None)` cho `head`. Không cần đổi hai oracle này cho M1: IMP-R2F đo 0 ô lệch
     trên đúng miền này ở nền (§1.8.7).
   - **Hợp đồng con–cha**: con trả `[số ô _doc_che_do, số ô head, ≤ 10 ô lệch đầu tiên, tổng số ô
     lệch]`. Cha đòi `[S1, S2, [], 0]`, với S1, S2 tính bằng **công thức** từ `len(D698)`,
     `len(R698 ∩ D698)`, `len(N698)` và độ dài các giá trị chuẩn, **không** lặp lại miền; thu hẹp miền (bớt vị
     trí, bớt điểm mã) làm số ô lệch công thức và ca đích ĐỎ. Đo trên IMP-R2F: S1 = 666.094,
     S2 = 120.888 (Python 3.11.15); S1 = 673.234, S2 = 122.148 (Python 3.12.3). Ví dụ trên 3.11.15: S1 = (19.588 + 3) × (9 + 7 + 11 + 7) = 666.094 (vị trí chèn cộng thay của `manh`, `3/8`, `15/16`, `a/b`); S2 = 2 × 19.588 × 3 + (13 + 3) × (81 + 129) = 120.888. r3 cộng ô nhiều thẻ của M1b: S2 thêm 2 × 2 × |`T698`| = 120, tức S2 = 121.008 (3.11.15) và 122.268 (3.12.3) — đo trực tiếp từ cửa con của biến thể `v3_head` (§1.9.4), S1 không đổi. r2 và r3 viết: "Ngoại lệ không
     phải `ValueError` trong `_doc_che_do` làm tiến trình con chết như `doc` hiện có, tức
     `tin_dung_gia`, không phải `giet_that`". **r4 thay câu ấy** (M6): `doc` của cửa con biến mọi `BaseException`
     khác `ValueError` thành `["NEM", <tên kiểu>]`; `_mong_che_do` không bao giờ trả giá trị ấy, nên ô lệch và `t53`
     chết bằng chốt của chính nó.
   - **`HOME`**: phép quét M1 và các ô `ra` (M2) chạy với `HOME` và `USERPROFILE` được đặt về một
     giá trị cố định không bắt đầu bằng `~` (IMP-R2F dùng `/nha698`), khôi phục trong `finally`. Lý
     do đo được ở §1.8.5: UID không có trong passwd cộng không có `HOME` ⇒ `expanduser("~/x")` trả
     nguyên `~/x`, và dò `expanduser` thành tương đương vì môi trường.
   - **Ký tự ngoài ASCII trong nguồn**: dựng bằng `chr()` hoặc từ thuộc tính lúc chạy; không đặt
     ký tự vô hình thẳng vào chuỗi nguồn. Sau khi ghi tệp, ĐO lại trong `ops/cong_cu_test.py`: số ký
     tự Cf và số ký tự U+FF01…U+FF5E phải bằng nền (0 và 0), tập ký tự có NFKC khác chính nó phải
     bằng nền ({U+2026}; đo lúc soạn r2).
   - Cách viết (hàm, tên, chỗ đặt) thuộc executor. Ràng buộc là miền (điểm mã × vị trí), oracle và
     hợp đồng đếm ở trên.
   - **M1b (r3) — `head` nhận một PHẦN của stdout.** Ô một-ký-tự của M1 không dựng được đầu vào mà một đột
     biến "lấy một phần của stdout" (phần sau/trước một ký tự tách, dòng cuối/đầu) nhận khác nền. Lý do, theo
     loại ký tự tách `c`:
     - `c` **không** là khoảng trắng: ô chèn đầu/cuối của M1 (`D698` × ba neo, `N698` mọi vị trí) đã giết đột
       biến — nền giữ `c` nên trả `None`, còn đột biến cắt bỏ `c` rồi trả mã băm (đo: `x3_head_zwsp_last`,
       `x3_head_chu_g_last`, §1.9.4). Với `c` ngoài `D698 ∪ N698` (chữ `Lo` không có ánh xạ NFKC, `Co`, `Cn` khác ba
       đại diện) đây là giới hạn đã khai của M1 (§10).
     - `c` **là** khoảng trắng: `strip()` của nền bỏ `c` ở hai đầu, nên ô đầu/cuối thành tương đương; còn ở giữa
       thì nền lẫn đột biến cùng trả `None`. Cần ít nhất một ký tự nhiễu cộng `c` trước hoặc sau mã băm.
     Thêm vào phép quét `head` của M1, với mỗi giá trị chuẩn `h` (40 và 64 ký tự) và mỗi chuỗi tách `s` của tập
     `T698` = {mọi ký tự `c` (trừ surrogate) có `c.isspace()`} ∪ {CR LF} — **dẫn xuất lúc chạy, không liệt kê** —
     hai ô `"x" + s + h` và `h + s + "x"` (`x` không phải chữ hex, không phải khoảng trắng), kỳ vọng `None` từ
     `_mong_git`. Hợp đồng đếm của M1 cộng thêm đúng 2 × 2 × |`T698`| ô vào S2, tính bằng công thức từ |`T698`|
     (không lặp lại miền). Đo (§1.9.4): |`T698`| = 29 + 1 = 30 trên cả 3.11.15 và 3.12.3 ⇒ +120 ô; S2 =
     121.008 (3.11.15) và 122.268 (3.12.3). `T698` chứa trọn tập ký tự mà `str.splitlines` tách (LF, VT, FF, CR,
     U+001C–U+001E, U+0085, U+2028, U+2029) cộng 19 khoảng trắng không tách dòng (TAB, U+001F, dấu cách, U+00A0,
     U+1680, U+2000–U+200A, U+202F, U+205F, U+3000). Vì sao không dừng ở tập `str.splitlines` như `HINT.patch` lượt
     2 đề nghị: đột biến tách theo một khoảng trắng không tách dòng bị che y hệt — đo: trên biến thể chỉ có tập
     `splitlines`, `x3_head_us_last` (U+001F) và `x3_head_emsp_last` (U+2003) SỐNG; ba dò cùng họ `x3_head_tab_last`,
     `x3_head_nbsp_last`, `x3_head_ideo_last` chỉ chết vì TAB, U+00A0, U+3000 tình cờ thuộc `R698` (ô chèn ở chỉ số
     24 của `head` 64 ký tự cắt ra đúng 40 chữ hex) — đúng hình dạng "chết nhờ ô tình cờ" mà verdict lượt 2 nêu cho
     `splitlines()` (§1.9.4).
2. **M2 (lớp C — phép đường dẫn và chuỗi trên `ra`).** Miền M1 đã phủ các phép một ký tự trên
   `ra`. Thêm vào `_luoi_che_do` các ô `ra` có **cấu trúc**, mỗi phép một ô riêng làm đổi giá trị
   (không ô nào phải bị hai phép cùng đổi): `a/./b//c` và `a/../b` (`normpath`), `~/x`
   (`expanduser`), `$HOME/x` (`expandvars`), `./x` (bỏ `./` đầu), `x/` (bỏ `/` cuối), `a//b` (gộp
   `//`, `str(Path(…))`), `a` + chr(92) + `b` (đổi chéo ngược thành `/`), `X/Y.TXT` (`lower`,
   `casefold`), `M` + U+1EA3 + `nh` (NFD), `Ma` + U+0309 + `nh` (NFC), `x` + U+00A0 (Zs cuối). Kỳ
   vọng nguyên văn từ `_mong_che_do`. `HOME` ghim như M1.
   **M2b (r3) — `ra` ở MỌI tầng hạ nguồn.** Liệt kê bằng `grep -n -w ra` trên nền (§1.9.5), sau khi
   `_doc_che_do` trả về, giá trị `ra` đi qua đúng các tầng dưới; mỗi tầng có chỗ đặt ô riêng:

   | tầng | dòng nền | mã | ô đo (ca đích) |
   |---|---|---|---|
   | T1 | :7468–:7487 | `_doc_che_do` đọc `ra`, kiểm `if not ra`, trả `(k, n, ra)` | M1 (`D698` × vị trí trên `a/b`) và M2 (12 ô cấu trúc) (`t53`) |
   | T2 | :8229 | `main`: `k, n, ra = tham_so` | kịch bản `_luoi_noi_main`, chế độ `manh` và `nen` (`t54`) |
   | T3a | :8232 | `main`, nhánh nền đỏ: `_ket_thuc_manh(k, n, ra, ten, None, …)` | kịch bản `_luoi_noi_main` chế độ `nen` (`t54`) |
   | T3b | :8245 | `main`, nhánh thường: `_ket_thuc_manh(k, n, ra, ten, …)` | kịch bản `_luoi_noi_main` chế độ `manh` (`t54`) |
   | T4 | :7514 | bộ ghi: `tep = Path(ra)` | ô bộ ghi THẬT trong cửa `--tu-kiem-gom` (`t52`) |
   | T5 | :7515–:7533 | bộ ghi dùng `tep`: `exists`/`is_symlink`/`unlink`, `parent.mkdir`, `write_bytes`, dòng in | ô bộ ghi của T4 (`t52`), r4: gọi bộ ghi **hai** lần trên cùng thư mục ô — lần hai gặp tệp cũ nên nhánh `exists`/`is_symlink`/`unlink` chạy — và so dòng in cuối của **mỗi** lần với dòng dựng độc lập từ `Path(p)` (đo §1.10.4) |

   - **Tầng `main` (T2, T3a, T3b).** Thêm vào `_luoi_noi_main`, cho **cả hai** chế độ `manh` (phủ T2 và T3b) và
     `nen` (phủ T2 và T3a), mỗi đường ra sau một kịch bản: (i) 12 đường cấu trúc của M2; (ii) mỗi điểm mã của
     `R698 ∪ N698` ở đầu, giữa và cuối của `a/b` (`c + "a/b"`, `"a" + c + "/b"`, `"a/b" + c`; 16 × 3 = 48 đường);
     (iii) **một** đường chứa mọi điểm mã của `D698 ∪ N698` theo thứ tự tăng, trừ U+0000 (giá trị biến môi trường
     không chứa được NUL) — phủ "mọi thành viên" bằng một kịch bản. Kỳ vọng là nhật ký bộ ghi giả mang **nguyên
     văn** đường ra; phần kỳ vọng hiện có của `t54` đã dựng đúng như vậy cho mọi hàng `_luoi_noi_main`, không cần
     oracle mới. Đo: 61 đường × 2 chế độ = 122 kịch bản. Ở T2/T3, gộp `//`, bỏ `./` đầu, bỏ `/` cuối **không**
     tương đương (nhật ký so nguyên văn), nên ô cấu trúc của M2 là cần.
   - **Ô T2–T5 đưa đường vào SAU `_doc_che_do`**: kịch bản `_luoi_noi_main` thay `_doc_che_do` bằng hàm trả thẳng
     `(k, n, đường)` như mọi hàng hiện có, và ô bộ ghi gọi thẳng `_ket_thuc_manh`. Đi qua biến môi trường và
     `_doc_che_do` thật thì dò tầng T1 — gồm mười canh T1 của bảng canh dưới — chết thêm ở `t54`/`t52`, bán kính 2,
     và A2, A5 đỏ. Đo trên `v3_all` (theo cách thứ nhất): bốn canh T1 của r2 vẫn bán kính 1/56 (§1.9.5).
   - **Tầng bộ ghi (T4, T5).** Thêm vào cửa `--tu-kiem-gom` một lưới ô bộ ghi THẬT: với mỗi đường `p` của (i) và
     (ii), cộng các khúc tên tệp phủ `D698 ∪ N698` (bỏ U+0000 và `/`, chia khúc 50 ký tự, mỗi khúc mở đầu bằng `k`
     để không khúc nào là `.` hay `..`) — gọi `_ket_thuc_manh(0, n, p, …)` với **một** tên đột biến (tệp nhỏ),
     `cwd` là thư mục tạm riêng của ô và `HOME`/`USERPROFILE` ghim vào một thư mục tạm rỗng khác. Kỳ vọng dựng độc
     lập, không gọi bộ ghi: tập mục (tệp và thư mục) dưới thư mục ô bằng tập dựng từ `Path(p)` và các cha của nó,
     sau khi ghép với `cwd` và giải `..`; thư mục `HOME` vẫn rỗng. Đo: 456 ô trên 3.12.3, 452 trên 3.11.15
     (12 + 48 + 396 hoặc 392 khúc). `Path(p)` tự gộp `//`, bỏ `./` đầu, `/./` và `/` cuối (đo:
     `str(Path("a//b"))` = `a/b`, `str(Path("./x"))` = `x`, `str(Path("x/"))` = `x`), nên ba phép ấy ở T4/T5
     **tương đương** theo cấu tạo; `normpath` ở T4 chỉ lộ qua ô có `..`, `expanduser` chỉ qua ô mở đầu bằng `~`. Ở T5,
     `normpath` đặt tại chỗ ghi là **tương đương** trên mọi đường không có symlink, vì `tep.parent.mkdir` đã tạo cha
     trước khi ghi nên hệ điều hành giải `x/..` đúng như `normpath` (đo: `x3_wr5_normpath` SỐNG trên `v3_ra`, §1.9.5).
   - **T5 ngoài `write_bytes` (r4).** Mỗi ô bộ ghi gọi `_ket_thuc_manh(0, n, p, …)` **hai lần liên tiếp** với cùng `p`,
     cùng `cwd`: lần hai gặp đúng tệp mà lần một đã ghi, nên nhánh `if tep.exists() or tep.is_symlink(): tep.unlink()`
     chạy trên một đường mang ký tự của ô (ô cũ của nền chỉ gặp tệp cũ ở tên ASCII, nên một phép chuẩn hoá đặt ở nhánh ấy
     không lộ). Kết quả so là tập mục dưới thư mục ô **cộng** dòng in cuối của mỗi lần gọi; kỳ vọng dòng in dựng độc
     lập là `f"MẢNH 0/{n}: 1/1 đột biến bán kính 1 · ghi {Path(p)}"` cho cả hai lần (ô ghi một tên đột biến). Hai việc
     ấy thay cho phương án "ô tệp cũ tại `tep` hoặc ghi vào §10" của `HINT.patch` lượt 3: gọi lần hai **là** ô tệp cũ,
     dựng không cần mã riêng. Đo ở §1.10.4: thiếu lần gọi thứ hai thì ba dò gỡ tệp cũ của Phụ lục J SỐNG; thiếu so dòng in
     thì ba dò dòng in SỐNG.
   - **Ô bộ ghi biến mọi ngoại lệ do bộ ghi ném thành dữ liệu** (review lượt 3; r4 đặt thành luật chung M6 cho cả bốn chỗ
     gọi). Một đột biến chuẩn hoá `ra` bằng NFKC mở rộng khúc tên 50 ký tự (vd `㈀` → `(가)`) vượt `NAME_MAX` và
     `_ket_thuc_manh` ném `OSError: File name too long`; nếu ô không bắt, ngoại lệ thoát khỏi cửa `--tu-kiem-gom`, con chết
     và `t52` ra `tin_dung_gia` thay vì `giet_that` (đo: dò `x_wr_ra_nfkc` trên ứng viên làm đúng từng chữ ở review lượt 3;
     đo lại trên `v4_go_wr` ở §1.10.3). Ô phải bắt **mọi `BaseException`** do hai lần gọi bộ ghi ném — không chỉ `Exception`,
     vì `SystemExit` cũng thoát khỏi cửa con y như vậy (đo §1.10.3) — ghi `["NEM:" + tên kiểu]` vào chỗ kết quả, rồi so như
     mọi kết quả khác với kỳ vọng dựng độc lập (kỳ vọng không bao giờ mang `NEM:`).
   - Tên tệp trên Windows cấm thêm ký tự (`<>:"|?*`, U+0001…U+001F; chéo ngược là dấu tách), nên ô bộ ghi của r3
     chỉ được đo trên POSIX; nhánh Windows là nợ `windows-chua-do-o-moi-wp698` (Q8). Thêm `cwd` và ghim `HOME`
     trong cửa con thì phải khôi phục trong `finally`.
   - Vì sao không dừng ở hướng của `HINT.patch` lượt 2 ("thêm vào `_luoi_noi_main` các đường cấu trúc … và vào kịch
     bản bộ ghi một đường tương tự"): hướng ấy không tách T3a khỏi T3b (một đột biến chỉ ở lời gọi của nhánh nền
     đỏ chỉ chết bởi kịch bản chế độ `nen`), không nói tới T5, và "một đường" ở bộ ghi không phủ thành viên — đo
     ở §1.9.5.
3. **M3 (lớp D — trục trọn cộng tích biên).** Kịch bản mảnh của `t54`:
   - **Trục** (Q4, giữ từ r1): `len(bo_qua)` ∈ {0, …, len(CA)} với `hong` rỗng và không tiền kiểm
     nào bị bỏ; `len(hong)` ∈ {1, …, len(CA)} với `bo_qua` rỗng; tiền kiểm bị bỏ = cả hai (hai tập
     một phần tử đã có ở nền).
   - **Tích biên** (mới): mọi bộ (h, b, T) với h, b ∈ {0, 1, 2, len(CA)−1, len(CA)}, h + b ≤ len(CA),
     T ⊆ {`batch_behavior_test`, `python_alias_behavior_test`}, và **ít nhất hai** trong ba toạ độ
     khác 0 hoặc khác rỗng (điểm chỉ có một toạ độ khác 0 đã nằm trên trục). `hong` lấy h ca đầu
     của `CA`, `bo_qua` lấy b ca kế tiếp (hai tập rời nhau). Với len(CA) = 56: **48** kịch bản.
   - Kỳ vọng dựng bằng chính các hàm dựng kỳ vọng hiện có của `t54`: ĐỎ ⇔ h > 0 hoặc T ≠ ∅, độc
     lập với b.
   - Lời khai phải khớp phép đo: đây là **trục trọn cộng tích biên**, không phải "quét trọn miền".
     Tích đầy đủ có 4 × Σ_{h=0..56}(57 − h) = 6612 kịch bản; không quét vì chi phí (§7).
4. **M4 (hồ sơ trong tệp).** Mỗi chỗ thêm mới có chú thích neo về #698 và về dò tương ứng. Mọi
   docstring hay chú thích đang khai một lớp là "đã đóng", "mọi …", "trọn" mà §1 và §1.8 đo thấy còn
   hở phải được sửa thành sự thật mới. Executor phải grep để tìm, không chỉ sửa chỗ mình đã biết
   (A7).
5. **M5 (lớp E — tập bắt ngoại lệ của `_van_tay`, đo CHÍNH XÁC từ hai phía).**
   - **Giữ từ r2.** Ba ô `(0, "", kiểu)` ngoài tập bắt trong `_luoi_git` — `ValueError`,
     `UnicodeDecodeError` (lớp con của `ValueError`; là ngoại lệ thật mà `subprocess.run(…, text=True)` ném khi
     stdout không giải mã được — đo: byte 0xFF qua `printf` ⇒ `UnicodeDecodeError`, `isinstance(…, ValueError)`
     đúng, `isinstance(…, (OSError, SubprocessError))` sai) và `RuntimeError` — cùng hàm dựng trong bảng `nem` của
     cửa con và nhánh kỳ vọng `NEM:<tên kiểu>` trong `_mong_git`. Ba ô sẵn có (`OSError`, `SubprocessError`,
     `TimeoutExpired`) đo phía thu hẹp.
   - **M5b (r3) — miền kiểu DẪN XUẤT; hợp đồng là một luật CHO PHÉP đóng.** Hợp đồng: `_van_tay` bắt một ngoại lệ
     thuộc lớp `E` **khi và chỉ khi** `issubclass(E, (OSError, subprocess.SubprocessError))` — đúng hai gốc, không
     gốc nào khác. Ba ô của r2 chỉ chặn việc mở rộng tập bắt sang ba kiểu ấy và tổ tiên của chúng; mọi kiểu khác lọt
     (*"danh sách CẤM không bao giờ đủ"*). Đo hợp đồng trên miền `E698` = **bao đóng bắc cầu của
     `BaseException.__subclasses__()`**, lấy trong tiến trình con đúng lúc quét, cộng chính `BaseException` —
     dẫn xuất lúc chạy, không liệt kê. Lý do chọn miền này: mọi lớp mà một mệnh đề `except` nêu tên được đều là
     lớp con của `BaseException` và đã được nạp, nên miền phủ mọi cách mở rộng tập bắt bằng một lớp đã nạp — kể
     cả lớp nằm ngoài `Exception` (`BaseException`, `BaseExceptionGroup`, `GeneratorExit`, `KeyboardInterrupt`,
     `SystemExit`) và lớp ngoài `builtins` (`re.error`, `json.JSONDecodeError`, …).
     - Mỗi lớp `E` của miền một ô: thay `subprocess.run` bằng hàm ném một **thể hiện** của `E`, gọi `_van_tay()`,
       và đổi **mọi** `BaseException` lọt ra thành dữ liệu `NEM:<E.__name__>` (bắt `Exception` thôi thì
       `SystemExit`, `KeyboardInterrupt`, `GeneratorExit` giết tiến trình con, tức `tin_dung_gia`).
     - Thể hiện dựng bằng `E.__new__(E)`; riêng họ `BaseExceptionGroup` (hàm tạo đòi đối số) dựng bằng
       `E("698", [Exception("698")])` nếu `E` là lớp con của `Exception`, ngược lại `E("698", [BaseException("698")])`.
       Đòi `type(thể hiện) is E`; lớp không dựng được vào một danh sách riêng, và danh sách ấy phải **rỗng**.
     - Kỳ vọng dựng độc lập, không gọi `_van_tay`: `None` nếu `issubclass(E, (OSError, SubprocessError))`, ngược
       lại `NEM:<E.__name__>`.
     - Trong lúc quét, `TEP_TEST` trỏ sang một tệp tạm vài byte (mẫu có sẵn ở khối `kq["byte"]` của cửa con), để
       mỗi ô không băm lại 600 KB (A4-g).
     - Hợp đồng con–cha: con trả `[danh sách khoá "module.qualname" đã đo, ≤ 10 ô lệch đầu, tổng số ô lệch,
       danh sách không dựng được]`. Cha đòi tổng lệch = 0, danh sách không dựng được rỗng, và tập khoá đã đo
       **chứa** tập `B698` mà cha tự dẫn xuất độc lập từ `vars(builtins)` (mọi giá trị là lớp con của
       `BaseException`). Thu hẹp miền — chỉ `Exception`, chỉ `builtins`, bỏ `BaseException` — làm phép chứa ấy
       hoặc các dò `x3_exc_*` của §6 ĐỎ.
     - Đo (§1.9.3, Python 3.11.15 và 3.12.3): |`B698`| = 67, |`E698`| = 118 (67 lớp `builtins` + 51 lớp nạp từ
       thư viện chuẩn, `yaml`, `bash_nen`, `lease_publish_test` và chính tệp), 0 ô lệch trên nền, 0 lớp không dựng
       được. Miền mà `HINT.patch` lượt 2 đề nghị — "mọi lớp con cụ thể của `Exception` trong `builtins` không thuộc
       họ `OSError`, dựng được bằng `__new__`" — có 45 lớp; trên biến thể theo đúng miền ấy, 12/12 dò `x_exc_*`
       GIẾT nhưng 7 dò mở rộng khác SỐNG: `KeyboardInterrupt`, `SystemExit`, `GeneratorExit`, `BaseExceptionGroup`,
       `ExceptionGroup` (hàm tạo đòi đối số nên bị loại khỏi miền), `re.error`, `json.JSONDecodeError`.
   - Không đổi thân `_van_tay` (A4-d). Muốn `_van_tay` bắt thêm kiểu nào là đổi mã, ngoài phạm vi (S1).
6. **M6 (r4) — ngoại lệ do mã bị đo ném là DỮ LIỆU, ở MỌI chỗ gọi của ô mới.** Một đột biến làm mã bị đo ném ngoại lệ
   trên một ô mới phải chết bằng **chốt của ca đích**, không bằng cái chết của cửa con (*"đột biến bị giết không phải
   đột biến bị giết đúng lý do"*). Liệt kê bằng cách đọc mã: các ô mới của r2–r4 gọi mã bị đo ở đúng năm chỗ, và mỗi
   chỗ phải bọc lời gọi trong một khối bắt **mọi `BaseException`**, đổi nó thành một giá trị so được, rồi so như mọi kết
   quả khác với kỳ vọng dựng độc lập (kỳ vọng không bao giờ là giá trị `NEM`):

   | chỗ gọi | cửa con (ca đích) | ô mới dùng nó | giá trị khi ném | trên nền |
   |---|---|---|---|---|
   | `doc(env)` quanh `_doc_che_do` | `--tu-kiem-che-do` (`t53`) | M1 (quét `bk`/`mh`/`ra`), M2 (12 ô `ra`) | `["NEM", <tên kiểu>]` (nhánh `ValueError` giữ nguyên) | chỉ bắt `ValueError` |
   | `_van_tay()` trong phép quét `head` | `--tu-kiem-che-do` (`t53`) | M1, M1b | `"NEM:<tên kiểu>"` | lưới `_luoi_git` của nền đã bắt `Exception`; phép quét mới thì chưa |
   | `main()` trong vòng kịch bản | `--tu-kiem-main` (`t54`) | M2b T2/T3a/T3b, M3 tích biên (và mọi kịch bản cũ, vì cùng vòng) | mã thoát `"NEM:<tên kiểu>"` | không bắt |
   | `_ket_thuc_manh(…)` hai lần | `--tu-kiem-gom` (`t52`) | M2b T4/T5 | `["NEM:<tên kiểu>"]` | ô `ghi_duong` của nền bắt `Exception`; ô mới thì tuỳ người viết |
   | `_van_tay()` dưới `subprocess.run` ném | `--tu-kiem-che-do` (`t53`) | M5b | `"NEM:<tên kiểu>"` | đã có trong chữ M5b từ r3 |

   Bọc vòng kịch bản của `--tu-kiem-main` đổi hành vi của cả các kịch bản cũ, nhưng chỉ khi `main()` ném — điều không
   xảy ra trên nền (`t54` xanh) — nên không có ô cũ nào đổi kết quả. Vì sao `BaseException` chứ không `Exception`:
   `SystemExit`, `KeyboardInterrupt`, `GeneratorExit` không là lớp con của `Exception`, và một `SystemExit` lọt ra làm
   cửa con thoát với mã của nó y như một `OSError` lọt ra (đo ở §1.10.3: biến thể chỉ bắt `Exception` để mọi dò răng
   `x4_*_thoat*` ra KHÁC). Dò răng của mỗi chỗ gọi là nhóm J-NEM của Phụ lục J. Dò răng của T1, `head` và T4 chỉ ném
   trên giá trị mà ô **cũ** của nền không có (ký tự ngoài ASCII ở `ra` của `_doc_che_do` và của bộ ghi, ký tự ngoài BMP ở
   stdout của `git`), nên SỐNG trên nền và chỉ đo chỗ gọi của ô mới. Dò răng của T2/T3 ném cả trên hai hàng **cũ** của
   `_luoi_noi_main` có ký tự ngoài ASCII (`dir/Sub Dir/Mảnh.TXT`, ` Đỏ Sub/Mixed.TXT `), nên trên nền chúng ra KHÁC (vòng
   kịch bản của nền không bắt) và chỉ GIẾT khi vòng ấy bắt — đó là đúng chỗ gọi mà M6 thêm. Không đổi thân sáu hàm của
   A4-d: các khối bọc nằm ở cửa con và ô, không trong mã bị đo.

**Bảng canh `DOT_BIEN`.** Thêm đúng **54** mục canh: 16 mục của r1 (M1–M3 cũ), 27 mục r2 và 11 mục r3. Mỗi
hàng trong lớp của bảng họ ở §2 có ít nhất một canh, trừ hàng "B phép khác": mọi dò ở đó là đối
chứng, trừ `s_mh_nfkd`, vốn bị đúng các ô fullwidth giết như canh `e49_nfkc_mh` (IMP-MIN, chỉ có ô
fullwidth cho `mh`, đã giết nó — §1.8.2). Mỗi mục có **cùng mỏ neo và cùng phép thay** với dò ghi ở
cột "dò" (Phụ lục A, C hoặc H), cùng ca đích, và được đăng ký **vô điều kiện** trong một bảng
có sẵn nằm **trước** `_TRUOC_NANG_LUC`. Tên mục do executor đặt; handoff phải kèm bảng nối
`tên dò ↔ tên mục DOT_BIEN` đủ 54 dòng, đúng định dạng Phụ lục F đọc (A5). r3 thêm đúng một canh cho mỗi
đường vào mới đo được ở §1.9 — mỗi tầng `ra`, mỗi loại ký tự tách của `head`, mỗi loại lớp ngoại lệ — để một
bản vá gỡ riêng một đường thì đúng canh của đường ấy ĐỎ.

**Mỏ neo của MỌI mục `DOT_BIEN` phải xuất hiện đúng MỘT lần trong tệp đích của nó trên cây ứng viên, SAU khi bảng
canh đã được ghi** (review lượt 3 nêu cho 54 canh; r4 mở rộng ra mọi mục theo phép đo dưới). Bảng nằm trong chính
`ops/cong_cu_test.py`, **trước** mã bị đo, và `_dung_cay_dot_bien` chỉ thay lần xuất hiện ĐẦU — nên bất kỳ văn bản mới
nào chứa nguyên văn một mỏ neo mà đứng trước chỗ ghi thật (literal của bảng, chú thích M4, mã ô mới) đều kéo đột biến
ra khỏi chỗ ghi. Luật đo được, cho Phụ lục F bản r4 (A5): mọi mục có tệp đích `ops/cong_cu_test.py` — 232 mục cũ cộng
54 canh, 286 mục — xuất hiện đúng **1** lần; mục có tệp đích khác xuất hiện đúng **bằng số lần trên nền** (184 mục;
trên nền 181 mục là 1, còn ba mục `bn_*` của `ops/bash_nen.py` là 2, 2 và 3 — có sẵn, ngoài write set). Đo trên bốn
biến thể đo của r4 (§1.10.2), chỉ khác nhau ở **cách viết** bảng hay một dòng chú thích:
- `repr` từng mỏ neo (`v4_lit`): đúng 1 mục lệch — `x3_wr5_nfkc`, mỏ neo một dòng `    tep.write_bytes((` có mặt 2 lần;
  dò `x3_wr5_nfkc` ra KHÁC, 9 ca `tin_dung_gia` (lỗi cú pháp trong tệp tạm) — khớp review lượt 3;
- chuỗi ba nháy nguyên văn **chỉ** cho 11 hàng r3 (`v4_tq`): **55** mục lệch — 11 canh r3, 24 canh r2 và **20 mục cũ**
  trong 416 (vd `f34_head_no_oserror` = 4, `f44_nen_ra_lower` = 2), vì mỏ neo của chúng trùng hoặc nằm trong mỏ neo của
  hàng r3 viết nguyên văn; lần xuất hiện đầu của cả 55 đều nằm trong vùng bảng. Ở dạng này tệp tạm vẫn biên dịch được,
  nên cái chết là **câm**: dò `x3_wr5_nfkc` và hai mục cũ trên đều SỐNG ("đích vẫn XANH");
- một dòng chú thích trích nguyên văn `    tep.parent.mkdir(parents=True, exist_ok=True)` ở vùng bảng (`v4_cu`): đúng 1 mục
  lệch — mục **cũ** `f35_writer_parents`, mỏ neo mà không canh nào dùng; một phép kiểm chỉ đếm 54 canh **qua** (rc=0);
- nối chuỗi cho mỏ neo một dòng (`v4_all`): 0 mục lệch trên 470; ba dò/mục trên đều GIẾT đúng ca đích, bán kính 1/56.
Vì vậy phép đếm phải phủ **mọi** mục, không chỉ 54 canh. Cách viết bảng thuộc executor; ràng buộc là phép đếm.

| họ | dò (phụ lục) | ca đích | số |
|---|---|---|---|
| B toàn chuỗi (r1) | `e49_nfkc_bk` `e49_nfkc_mh` `e49_nfkc_head` `e49_cf_bk` `e49_cf_mh` `e49_cf_head` `x46_tab_bk` `x46_tab_mh` `x46_tab_head` (A) | `t53` | 9 |
| C (r1) | `e49_ra_normpath` `e49_ra_expanduser` (A) | `t53` | 2 |
| D trục (r1) | `e50_bang_2` `e50_tu_2` `x50_bang_n_tru_1` `x47_hong_bang_1` `x47_tk_bang_1` (A) | `t54` | 5 |
| `ra` × B | `s_ra_nfkc` `s_ra_cf` `s_ra_tab` (C) | `t53` | 3 |
| `ra` phép | `s_ra_rstrip_slash` `s_ra_lstrip_dot` `s_ra_expandvars` (C) | `t53` | 3 |
| `ra` × vị trí, `ra` × thành viên | `q_cf_mid_ra` `m_cf_tag_ra` (C) | `t53` | 2 |
| vị trí | `q_cf_lead_bk` `q_cf_mid_head` `q_tab_lead_mh` (C) | `t53` | 3 |
| mọi vị trí | `p_cf_head_17` (C) | `t53` | 1 |
| thành viên | `m_cf_tag_bk` `m_cf_061c_bk` `m_nfkc_ngoai_bmp_mh` (C) | `t53` | 3 |
| dấu kết hợp | `m_bodau_bk` (C) | `t53` | 1 |
| Cc | `m_cc_head` (C) | `t53` | 1 |
| nhóm ngoài `D698` | `m_co_bk` (C) | `t53` | 1 |
| Zs và strip hẹp | `s_bk_drop_zs` `s_mh_drop_zs` `s_head_strip_ascii` (C) | `t53` | 3 |
| E ngoại lệ | `z_exc_all` `z_exc_them_valueerror` (C) | `t53` | 2 |
| D tích | `s2_hong_va_khong_bq` `s2_hong_gt_bq` `s2_tk_va_khong_bq` `s3_xor` (C) | `t54` | 4 |
| E ngoại lệ, r3: lớp con `Exception` trong `builtins` · lớp ngoài `Exception` · lớp ngoài `builtins` | `x_exc_typeerror` `x3_exc_kbint` `x3_exc_re_error` (H) | `t53` | 3 |
| `head` nhiều thẻ, r3: ký tự tách dòng · khoảng trắng không tách dòng | `x_head_nl_last` `x3_head_emsp_last` (H) | `t53` | 2 |
| nhóm Unicode, r3 (nhóm mà danh sách nhóm để lọt) | `x_cat_mc_bk` (H) | `t53` | 1 |
| `ra` tầng `main`, r3: giải gói (T2) · lời gọi nhánh nền đỏ (T3a) · lời gọi nhánh thường (T3b) | `x_main_ra_normpath` `x3_m3a_ra_nfkc` `x3_m3b_ra_cf` (H) | `t54` | 3 |
| `ra` tầng bộ ghi, r3: `tep = Path(ra)` (T4) · chỗ ghi (T5) | `x_wr_ra_nfkc` `x3_wr5_nfkc` (H) | `t52` | 2 |

Vì sao không đăng ký trọn tập dò đóng (350 dò thuộc A1–A3, A8 của r3) vào `DOT_BIEN`: mỗi mục canh cộng một lượt
chạy 56 ca vào mọi vòng bán kính; 350 mục (766 đột biến) đưa mảnh CI dài nhất lên khoảng 43,2 phút theo mô hình r4
(r3 ước 41,4 phút bằng mô hình cũ), vượt trần 30 phút của job (ƯỚC, §7), và vượt xa trần 300 dòng (S5). Tập đóng được đo **trọn** một lần ở nghiệm thu (A1–A3, A8); 54 canh
là phần canh hồi quy thường trực.

## 6. `nghiem_thu`

**Quy ước chung.** "Đột biến" nghĩa là chạy trên **bản sao tạm**, với `PYTHONDONTWRITEBYTECODE=1`,
và mọi thư mục đầu ra (tệp mảnh A5, jsonl của bản ghép Phụ lục C + H + J) nằm **ngoài** cây checkout. Phân hạng
một dò hay một mục canh theo Phụ lục D, trên đầu ra của chính `_do_ban_kinh` +
`_ket_luan_ban_kinh`:

- **GIẾT** (`ok … 1/N`): `_ket_luan_ban_kinh` trả 0 lỗi; ca đích ra `giet_that`, tức
  `TinHieuChotCa` mang **đúng tên ca đích** (nhánh `return "giet_that", …` của `_chay_1_ca` ở
  :2318; hàm bắt đầu ở :2292); và không ca nào khác chết, trừ ca bị môi trường bỏ qua (`bo_qua`).
- **SỐNG**: không ca nào chết.
- **KHÁC**: mọi trường hợp còn lại — `tin_dung_gia` (`LoiDungCa`, `AttributeError`, tiến trình con
  chết…), sai ca đích, bán kính > 1. KHÁC **không** được nhận, dù mã thoát khác 0 (bài học *"đột
  biến bị giết không phải đột biến bị giết đúng lý do"*).

**Phiên bản Python.** CI chạy Python **3.12** (`ci.yml` ghim `python-version: "3.12"` ở mọi job
có G5). Mọi phép đo nghiệm thu ghi phiên bản Python; A1–A3, A5 và A8 phải ĐẠT trên 3.12. `D698`
phụ thuộc bản Unicode của Python (§1.8.8), nên số ô S1/S2 phải được tính lại theo đúng bản đang
chạy, không chép số.

**Tập dò đóng** của r4 là Phụ lục C (sha256 c6a4db8b47fe246e8e173c13298a62310019809794ea322abcc94e1fdd922a36, 221
dò) cộng Phụ lục H (sha256 850734781257b3041e251e4e6554da60e76d4dfb3137add9bdf26b46ce3f90f7, 145 dò) cộng Phụ lục J
(khối dò của r4, 35 dò; băm ở tiêu đề Phụ lục J), ghép bằng lệnh ở Phụ lục H rồi lệnh ở Phụ lục J thành một script 401
dò mà 366 dò đầu trùng từng mục với bản ghép của r3. Chia theo tiêu chí bằng tên — hàm `tap` của Phụ lục D (bản r3,
**không đổi**: mọi tên của Phụ lục J kết thúc bằng `_ra` nên rơi vào T-C, trừ `x4_head_thoat` rơi vào T-B; đo bằng chính
hàm `tap` trên 401 tên):

| tập | luật tên | Phụ lục C | Phụ lục H | Phụ lục J | tổng | tiêu chí |
|---|---|---|---|---|---|---|
| T-B | mọi dò không thuộc các tập dưới | 155 | 68 | 1 | 224 | A1 |
| T-C | tên kết thúc bằng `_ra`, hoặc mở đầu bằng `s_ra_`, `p_cf_ra_`, `x_main_ra_`, `x_wr_ra_`, `x3_main_ra_`, `x3_wr_ra_`, `x3_m3a_ra_`, `x3_m3b_ra_`, `x3_wr5_` | 41 | 40 | 34 | 115 | A2 |
| T-D | mở đầu bằng `s2_`, `s3_`, `x_f50_` (trừ tập KHAI) | 12 | 4 | 0 | 16 | A3 |
| T-E | mở đầu bằng `z_exc_`, `x_exc_`, `x3_exc_` | 7 | 23 | 0 | 30 | A8 |
| ngoài lớp | mở đầu bằng `g_`, `t_`, `x3_gop_`, `x3_cua_` | 6 | 5 | 0 | 11 | không (đo để khai và ghi nợ, §2) |
| KHAI | năm tên nêu đích danh trong Phụ lục D | 0 | 5 | 0 | 5 | không (khai SỐNG; lý do dưới) |

Mỗi tập có **đối chứng** (dò bị giết ngay trên nền) và có thể có dò **TƯƠNG ĐƯƠNG** (không đầu vào nào phân biệt
được với nền) — cả hai được liệt kê đích danh ở §2 và §1.9 kèm phép đo. Dò đối chứng phải giữ **nguyên hạng như trên
nền** (GIẾT, hoặc KHÁC bán kính 2 như `s_ra_realpath`); dò tương đương không tính. Tập **KHAI** gồm năm dò SỐNG có chủ
đích, mỗi dò một lý do có neo: `x_head_cf2063_at17`, `x_head_cfk_mid_only`, `x_head_sm_mid_only` (tổ hợp "thành viên
ngoài `R698` × vị trí ngoài ba neo" của `head` không được đo — lời khai đã thu hẹp ở `objective`); `x_f50_tk_and_bq_ne3`,
`x_f50_h_and_bq_ne3` (vị từ gắn một hằng giữa của `bo_qua` với toạ độ khác — hậu quả của cách đọc Q4 "trục trọn cộng
tích biên", §11.1 (B)). Một dò KHAI mà GIẾT trên ứng viên thì không sao; SỐNG là trạng thái đã khai.

- **A1 (M1, M1b; bộ đọc `bk`, `mh`, `head`).**
  **ĐẠT KHI:** (i) các canh thuộc T-B của bảng canh §5 (9 r1 + 13 r2 + 3 r3 = 25) đều GIẾT `t53_…` trong A5; (ii)
  chạy bản ghép Phụ lục C + H trên ứng viên, mọi dò của T-B trừ dò tương đương đều GIẾT `t53_…` (kể cả đối chứng,
  vốn đã GIẾT trên nền); (iii) hợp đồng đếm của M1 và M1b khớp công thức (ca `t53` tự kiểm; A4-a xanh là bằng chứng);
  (iv) phép đo ký tự nguồn của M1 bằng nền, đo bằng máy — lệnh `python3 -c 'import sys,unicodedata as u; t=open(sys.argv[1],encoding="utf-8").read(); print(sum(u.category(c)=="Cf" for c in t), sum(0xFF01<=ord(c)<=0xFF5E for c in t), sorted({hex(ord(c)) for c in t if u.normalize("NFKC",c)!=c}))' ops/cong_cu_test.py` phải in đúng dòng của nền, `0 0 ['0x2026']` (đo lúc soạn r3 trên nền, `cand` và `v3_all`: cả ba như nhau); (v) mỗi nhóm `unicodedata.category` có mặt trong `D698` (27 nhóm, dẫn
  xuất) có một dò xoá-cả-nhóm trên `bk` trong Phụ lục H, và dò ấy GIẾT (đã nằm trong (ii); nêu riêng vì một phép quét
  dùng DANH SÁCH nhóm thay cho luật `D698` cho hạng giống hệt ứng viên trên cả 196 dò T-B và T-C của Phụ lục C — đo
  của reviewer lượt 2 — và chỉ lộ ở dò của nhóm mà danh sách thiếu).
  **PHẢI ĐỎ Ở** (bằng chứng tiêu chí có răng): nền `fc852ff` (phần Phụ lục C của T-B còn 149 dò SỐNG; phần Phụ lục H
  62/68 dò SỐNG, sáu dò còn lại là đối chứng); IMP-MIN và IMP-GEN của reviewer lượt 1 (133 và 101 dò SỐNG trong phần Phụ lục C; phần Phụ lục H không
  đo trên hai cây ấy); `cand` — ứng viên đúng chữ r2 của reviewer lượt 2 (23/68 dò T-B của Phụ lục H SỐNG, đều ở họ `head` nhiều thẻ; §1.9.4); `tv_head` — biến thể đúng hướng
  HINT lượt 2 cho `head` (2/38 dò `head` của Phụ lục H SỐNG: `x3_head_us_last`, `x3_head_emsp_last`); `tv_list` — biến thể dùng danh sách nhóm (4/27 dò xoá-nhóm SỐNG: Mc, Me, Pf, Pi; §1.9.7); và (r4) dò T-B duy nhất của Phụ lục J,
  `x4_head_thoat` (quét `head` ném `SystemExit` khi stdout có ký tự ngoài BMP), ra KHÁC trên `v4_go_head`, `v4_nocatch`
  và `v4_exc`, GIẾT trên `v4_all`, SỐNG trên nền (§1.10.3).
  **Bậc hai A1-b2** (số hiệu riêng, không phải mục (ii) ở trên), đo trên **một bản đo riêng** của ứng viên — mã gỡ
  nhóm không nằm trong bản giao (S5), handoff đính bảng đo và nói rõ dùng đúng định nghĩa dưới; thiếu bảng ⇒
  reviewer đỏ A1. **Định nghĩa nhóm (chốt)** — tập điểm mã của `D698 ∪ N698` thoả thuộc tính: `cf` = Cf; `tab` =
  U+0009; `cc` = Cc trừ U+0009; `zs` = Zs ∪ Zl ∪ Zp; `dau` = Mn, hoặc `NFD(c) ≠ c`; `nfkc` = `NFKC(c) ≠ c` trừ Zs ∪ Zl
  ∪ Zp; `ngoai` = `N698`; r3 thêm `tach` = các ô nhiều thẻ của M1b, và `mc` = Mc (chỉ cho canh `x_cat_mc_bk`). Các nhóm **được phép giao**; giao còn lại đo được:
  `zs ∩ dau` = {U+2000, U+2001}, `dau ∩ nfkc` = 1.132 điểm mã (§1.9.8). Đây là định nghĩa mà bảng §1.8.7 của r2 đã
  dùng mà không ghi ra (đo lại: `cc` ⇒ 1 canh, `nfkc` ⇒ 4 canh SỐNG lại, khớp bảng). Cách đo: (1) giữ từ r1 — gỡ
  nhóm của **một** phép (NFKC | Cf | TAB) thì đúng 3 canh r1 của phép ấy SỐNG lại, còn canh r1 của hai phép kia vẫn
  GIẾT; ba nhóm không tách được bằng đầu vào ⇒ bộ tương đương ⇒ ĐỎ; (2) mỗi canh r2 và r3 thuộc T-B khai **tập nhóm**
  K(c) mà gỡ đúng tập ấy thì c SỐNG lại (c chết vì chính phần miền được khai, không vì một ô tình cờ) — kỳ vọng theo
  định nghĩa trên là bảng §1.8.7 (đo trên IMP-R2-GO) cộng hai dòng r3: gỡ `tach` ⇒ `x_head_nl_last`,
  `x3_head_emsp_last` SỐNG lại (đo trên `v3_go_tach`, §1.9.8); canh `x_cat_mc_bk` có K = `mc` — đo gián tiếp: trên
  `tv_list`, miền thiếu trọn nhóm Mc và dò ấy SỐNG (§1.9.7).
- **A2 (M2, M2b và `ra` trong M1).** **ĐẠT KHI:** các canh thuộc T-C của bảng canh §5 (2 r1 + 8 r2 + 5 r3 = 15)
  GIẾT đúng ca đích (`t53_…` cho T1, `t54_…` cho T2/T3, `t52_…` cho T4/T5) trong A5; mọi dò của T-C trừ đối chứng và
  dò tương đương GIẾT trên ứng viên. **PHẢI ĐỎ Ở:** nền (phần Phụ lục C 40 dò SỐNG; phần Phụ lục H 37/40 dò SỐNG, ba dò còn lại là đối chứng),
  IMP-MIN (38) và IMP-GEN (24) ở phần Phụ lục C, `cand` — đúng chữ r2 (37/40 dò T-C của Phụ lục H SỐNG: mọi tầng T2–T5; §1.9.5). **Bậc hai:** gỡ riêng các ô cấu trúc `ra` của
  M2 thì đúng các canh `ra` mà miền M1 không giết được SỐNG lại (đo trên IMP-R2-GO: trong năm canh `ra` chạy dưới
  phép gỡ ấy, chỉ `s_ra_expandvars` SỐNG lại, §1.8.7); gỡ riêng các ô M2b (nhóm `ra2`) thì năm canh T-C của r3 SỐNG
  lại, còn canh T1 vẫn GIẾT (đo trên `v3_go_ra2`: `x_main_ra_normpath`, `x3_m3a_ra_nfkc`, `x3_m3b_ra_cf`, `x_wr_ra_nfkc`
  SỐNG lại, `s_ra_cf` vẫn GIẾT; canh T5 `x3_wr5_nfkc` SỐNG lại ở một lượt riêng trên cùng cây gỡ, và GIẾT `t52_…`
  trên `v3_ra`; §1.9.8).
  **Phần Phụ lục J (r4; §1.10.3–§1.10.4).** Mọi dò T-C của Phụ lục J GIẾT đúng ca đích trên ứng viên — nhóm J-NEM
  (ngoại lệ ở `doc`, `main`, bộ ghi; dò của quét `head` thuộc T-B, A1), J-T5 (gỡ tệp cũ, `exists`, `is_symlink`, `mkdir`,
  dòng in) và J-TV (thành viên U+2063, U+E0020, U+FF41 bị xoá ở T2, T3a, T3b, T4, T5). Không dò nào của Phụ lục J là
  đối chứng hay tương đương. **PHẢI ĐỎ Ở** (đo trên biến thể của r4, mỗi biến thể thiếu đúng một phần): `v4_nocatch`
  (9/9 dò J-NEM thuộc T-C KHÁC), `v4_exc` — chỉ bắt `Exception` — (5 dò `SystemExit` thuộc T-C KHÁC; dò thứ sáu,
  `x4_head_thoat`, thuộc A1), mỗi cây gỡ một chỗ gọi (`v4_go_t1`,
  `v4_go_head`, `v4_go_main`, `v4_go_wr`: đúng các dò của chỗ ấy KHÁC), `v4_t5_r3` — cách viết bộ ghi của `v3_all` —
  (6 dò gỡ tệp cũ và dòng in SỐNG), `v4_go_hai` (3 dò gỡ tệp cũ SỐNG), `v4_go_in` (3 dò dòng in SỐNG), `v4_nomem`
  (15/15 dò J-TV SỐNG); và nền (30/34 dò T-C của Phụ lục J SỐNG, 4 KHÁC — bốn dò J-NEM của `main`, §1.10.3). Đây là
  phần mà `HINT.patch` lượt 3 nêu bằng lời ("thêm vào T-C các dò thành viên ấy cho T2, T3a, T3b và T4") — r4 thêm T5
  và đính dò.
- **A3 (M3).** **ĐẠT KHI:** 5 canh D của r1 và 4 canh D tích của r2 GIẾT `t54_…` trong A5; mọi dò của T-D trừ đối
  chứng GIẾT trên ứng viên (r3 thêm bốn dò `x_f50_*` của reviewer lượt 2 vào T-D; hai dò hằng giữa vào KHAI).
  **PHẢI ĐỎ Ở:** nền (phần Phụ lục C 11 dò SỐNG; `x_f50_*` của Phụ lục H 2/4 SỐNG — `x_f50_or_bq_eq2`, `x_f50_or_bq_eq7`, đúng lỗ F50 gốc —, hai dò còn lại
  `x_f50_h_ge2`, `x_f50_tk_ge2` là đối chứng; trên `cand` cả bốn GIẾT, §1.9.2), IMP-MIN, IMP-GEN (hai bản ấy không có tích:
  8, 8 dò SỐNG). **Bậc hai:** gỡ riêng trục `bo_qua` ⇒ ba canh `bo_qua` của r1 SỐNG lại; gỡ riêng lưới tích ⇒ bốn canh
  D tích SỐNG lại; canh `hong`/`tien_kiem` của r1 bị cả trục lẫn tích giết, nên phải gỡ **cả hai** mới SỐNG lại (đo
  trên IMP-R2-GO: `bq` ⇒ 3, `tich` ⇒ 4, `hong` một mình ⇒ 0, `tk` một mình ⇒ 0; gỡ cả hai thì canh tương ứng SỐNG
  lại — bảng §1.8.7 ghi phần THÊM so với `tich` là 1, tức tổng SỐNG lại dưới `hong,tich` là 5 = 4 + 1, đúng số
  reviewer lượt 2 đo).
- **A4 (không hồi quy, không nới phạm vi).** Ứng viên và nền được đo trong **một** lệnh, cùng
  công cụ, cùng phiên bản Python. **ĐỎ KHI** một mục dưới đây đỏ trên ứng viên mà xanh trên nền:
  - (a) `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` ra `cong_cu_test: M/M đạt`,
    `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0. Nền đo lúc soạn r2 (Python 3.12.3, PyYAML 6.0.3,
    jsonschema 4.26.0 — đúng bản `ci.yml` ghim): `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0`, `SỐ LIỆU: … đột biến=416 (giao mảnh) · lỗi đột biến=0 · … · cổng cây thật=ĐẠT`, rc=0, 175 s — tức có `jsonschema` thì `t2` chạy và đạt. Thiếu `jsonschema` thì `t2` bị bỏ qua
    (`bỏ qua=1`), như lượt đo của r1.
  - (b) `ruff check --select F ops/cong_cu_test.py` bằng **ruff 0.15.15** (bản `ci.yml` ghim), so
    theo **đa tập (mã, thông điệp)**, không theo số dòng: chèn dòng làm vị trí trượt mà vẫn là cùng
    một lỗi. Nền đo lúc soạn r2: đúng 1 lỗi, `F841 Local variable ci is assigned to but never used` ở :2606.
    **Bẫy đo được lúc soạn r3** (ruff 0.15.8, bản 0.15.15 không có trong container r3): kho không có
    `pyproject.toml` hay `ruff.toml`, nên ruff dùng phiên bản Python đích mặc định và báo
    `F821 Undefined name BaseExceptionGroup` khi mã nêu tên trần lớp ấy (hoặc `ExceptionGroup`), tức A4-b ĐỎ. Lấy
    gốc nhóm qua `getattr(builtins, "BaseExceptionGroup", ())` thì đa tập lỗi của biến thể `v3_all` bằng nền
    (một `F841`, cùng thông điệp). Không thêm cấu hình ruff để lách (ngoài write set, S1).
  - (c) `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) cho delta 0.
  - (d) `git diff fc852fff7da37f1669569572b79571446e61c294 -- ops/cong_cu_test.py` **không chạm
    thân** `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`,
    `_chay_1_ca`. Đo bằng máy, không bằng mắt: **chạy Phụ lục G**; giao khác rỗng (mã thoát 1) ⇒ ĐỎ. Khoảng của
    hàm lấy bằng `ast` trên tệp NỀN; hunk lấy khoảng phía nền của `git diff -U0`; chèn ngay sau dòng cuối của hàm
    cũng tính là chạm. Phản chứng đã chạy: §1.9.10.
  - (e) Chạy Phụ lục E: số chỗ ghi `DOT_BIEN` **sau** dòng `_TEN_NANG_LUC = …` vẫn **= 0** (nền: 0).
    Bản vá không được mở rộng đường (e).
  - (f) `git diff --name-only fc852fff7da37f1669569572b79571446e61c294` (so với nền tiếp nối nếu
    lease khai khác) = `{ops/cong_cu_test.py}`, và `git status --short` của checkout không có tệp
    chưa theo dõi do phép đo sinh ra.
  - (g) **Chi phí — chạy Phụ lục I (bản r4, `chi_phi_r4.py`)** trên nền và ứng viên trong một lệnh, Python 3.12, POSIX.
    Hai phép làm đỏ, cả hai phải đạt: (1) **đếm tất định** — trong cửa con `--tu-kiem-che-do` chạy trong tiến trình, số
    lời gọi `_van_tay` băm một `TEP_TEST` lớn hơn 4096 byte không quá **2 × nền**. Đếm số lời gọi thôi thì **không**
    phân biệt được bản nhanh với bản chậm: đo ở §1.9.9, bản trỏ `TEP_TEST` sang tệp nhỏ và bản gọi `_van_tay()` thật
    cùng có 122.230 lời gọi, còn số lời gọi băm tệp lớn là 67 so với 122.215 (nền: 64); (2) **CPU** — mỗi ca `t52`,
    `t53`, `t54` chạy ba vòng xen kẽ nền và ứng viên; mỗi lượt đo CPU người dùng + hệ thống của chính tiến trình cộng
    mọi tiến trình con đã được `wait` (`resource.getrusage` SELF + CHILDREN, hiệu trước/sau lượt); lấy min mỗi ca;
    Δ_CPU = tổng qua ba ca của (min ứng viên − min nền); rồi đo **thước của chính máy** C56 = CPU của một lượt trọn mọi
    ca của `CA` trên nền, trong cùng lệnh (đại diện cho CPU của một lượt đột biến, vì mỗi lượt đột biến chạy trọn các ca
    ấy). **ĐẠT KHI** tỷ lệ r = (C56 + Δ_CPU)/C56 **≤ 1,35**, tức mảnh dài nhất ước ≈ 18,23 phút × (59/52) × r ≤ 27,9
    phút theo mô hình CPU của §7 (bản r4) — dưới trần 30 phút của job hơn 2 phút. Vì sao tỷ lệ chứ không một ngưỡng giây:
    mô hình chỉ cần tỷ lệ, còn số giây CPU đổi theo máy và theo tải — cùng mã nền, một mảnh A5 cho C₀ = 23,82 s CPU mỗi
    đột biến lúc soạn r4 (máy bận) so với 21,20 s ở review lượt 3 (§1.10.5) — nên một ngưỡng giây tuyệt đối đúng ở máy
    này thì lỏng gấp đôi ở máy nhanh gấp đôi. (3) **Đồng hồ — chỉ báo, không làm
    đỏ**: script in Δ giây tường của cùng các lượt, kèm số lõi mà tiến trình **khác** dùng trong cửa sổ đo
    (`/proc/stat` bận trừ CPU của chính lệnh) và loadavg trước/sau; handoff chép ba số ấy. Lý do đổi: review lượt 3 đo
    cùng một ứng viên đúng chữ cho Δ tường 5,9–11,7 s tuỳ tải (đỏ giả 2/12 lần khi quá tải) trong khi Δ CPU 6,2–6,5 s;
    r4 đo lại ở §1.10.5. **PHẢI ĐỎ Ở:** `tv_naive` (đỏ `dem` và `cpu`) và `tv_cpu` — ứng viên đo của r4 cộng một vòng
    đốt CPU trong cửa con (Δ_CPU 12,80 s so với 5,96–7,51 s của `v4_all`, tức thêm chừng 5–7 s; r 1,53; chỉ đỏ `cpu`,
    phép đếm không đổi). **Không bắt:** một bản chậm mà không tốn CPU — đo bằng `tv_cham` (ngủ 11 s trong cửa con):
    rc=0 — Δ_CPU 4,66 s, r 1,20, trong khi Δ tường 15,75 s (§1.10.5) — giới hạn khai ở §10. Vì CI chỉ chạy MỘT lần (Q7), một bản
    thi công đúng chữ mà chậm không có lượt thứ hai để sửa; phép CPU là chốt trước CI, `timeout-minutes: 30` là chốt
    fail-closed cuối cùng. Phép đồng hồ ≤ 10 s của r3 và hai ngưỡng riêng lẻ của `HINT.patch` lượt 2 (`t53` + 8 s,
    `t54` + 4 s) đều thôi áp dụng.
- **A5 (bán kính trọn).** Trước hết chạy **Phụ lục F (bản r4, `kiem_canh_r4.py`)** với bảng nối 54 dòng và hai script
  dò (Phụ lục A, bản ghép C + H + J) — vài giây, và nó bắt mỏ neo tự va chạm trước khi tốn tám mảnh. Rồi chạy 8 lượt
  `CONG_CU_TEST_MANH=k/8` với `CONG_CU_TEST_MANH_RA=<thư mục ngoài cây>/manh-k.txt` (k = 0…7), rồi
  `python ops/cong_cu_test.py --gop <thư mục ấy>`.
  **ĐẠT KHI:** ra `GOM MẢNH 8/8`, mọi dòng bảng là `ok`, `lỗi đột biến=0`, số đột biến **= 470** (416 + 54), **và**
  Phụ lục F bản r4 ra mã thoát 0 — tức: bộ sáu trường của cả 416 tên cũ y nguyên; tập tên thêm đúng bằng cột phải của
  bảng nối; **bộ** (mỏ neo, phép thay, ca đích) của từng mục bằng từng byte bộ của dò cùng tên trong Phụ lục A hoặc bản
  ghép (không chỉ so tên); và (r4, `dem-neo`) mỏ neo của **mọi** mục `DOT_BIEN` (470) xuất hiện trong tệp đích của nó
  trên cây ứng viên đúng 1 lần nếu tệp đích là `ops/cong_cu_test.py` hay mục là mục thêm, và đúng bằng số lần trên nền
  nếu không (§5, đoạn mỏ neo). Bản r3 của Phụ lục F chỉ so bộ theo giá trị nên không bắt tự va chạm — đo ở review lượt
  3 và lại ở §1.10.2 (`so_loi = 0` trên `v4_lit` và `v4_tq`).
  **ĐỎ KHI** có lượt rc ≠ 0, có dòng không `ok`, số lệch, hoặc Phụ lục F bản r4 ra mã 1. Phản chứng của Phụ lục F bản r4
  đã chạy lúc soạn r4 (§1.10.2): một canh cùng tên mà phép thay yếu hơn dò ⇒ `lech-bo`; một bộ cũ bị đổi ⇒ `bo-cu`;
  bảng nối thiếu một dòng ⇒ `tap-ten`; mỏ neo một dòng viết bằng `repr` (`v4_lit`) ⇒ `dem-neo` 1 mục; mỏ neo viết bằng
  chuỗi ba nháy (`v4_tq`) ⇒ `dem-neo` 55 mục, trong đó 20 mục cũ; một dòng chú thích trích nguyên văn mỏ neo của một mục
  cũ (`v4_cu`) ⇒ `dem-neo` 1 mục cũ; gỡ chốt `dem-neo` khỏi chính script ⇒ `v4_lit` rc=0 (chốt có răng).
- **A6 (review).** Reviewer Claude Sonnet 5.5 chạy bằng subagent, đưa verdict trên exact head, lặp
  tới **0 P1 · 0 P2 · 0 P3** (khối `nang_tran`); biên nhận ghi nhãn **`review_deferred`**. Chưa có
  `human_audited` của chủ kho thì không land. Tiêu chí này không có phép đo máy: nó là cổng thẩm
  quyền, không phải cổng hành vi.
- **A7 (M4).** Handoff liệt kê đầu ra của
  `grep -n -E "đã đóng|ĐÃ ĐÓNG|mọi |MỌI |trọn|TRỌN|không còn|KHÔNG còn" ops/cong_cu_test.py`
  giới hạn trong thân và chú thích của `t52`, `t53`, `t54`, `_luoi_che_do`, `_luoi_git`, `_mong_git`,
  `_luoi_noi_main`, `_in_tu_kiem_gom`, `_in_tu_kiem_che_do`, `_in_tu_kiem_main` và các hàm mới, kèm kết luận **giữ** hoặc **sửa** cho
  từng dòng. **ĐỎ KHI** còn một dòng mà §1, §1.8 hoặc §1.9 đo thấy sai nhưng không có kết luận "sửa",
  hoặc một chỗ thêm mới không có chú thích neo #698.
- **A8 (M5, M5b).** **ĐẠT KHI:** các canh E của bảng canh §5 (2 r2 + 3 r3 = 5) GIẾT `t53_…` trong A5; mọi dò của
  T-E (30) trừ hai đối chứng GIẾT trên ứng viên; hai đối chứng (`z_exc_oserror_only`, `z_exc_subproc_only`) vẫn GIẾT;
  và hợp đồng con–cha của M5b đạt (tổng lệch 0, danh sách không dựng được rỗng, khoá đã đo ⊇ `B698`). **PHẢI ĐỎ Ở:**
  nền (28/30 SỐNG), `cand` — đúng chữ M5 của r2 (22/30 SỐNG), `tv_exc` — đúng hướng HINT lượt 2 (7/30 SỐNG: năm lớp
  gốc ngoài `Exception`, `ExceptionGroup`, `re.error`, `json.JSONDecodeError`; §1.9.3). **Bậc hai** (r4 viết lại; đo trên
  ba cây gỡ của `v4_all`, §1.10.6): gỡ riêng miền `E698` của M5b ⇒ ba canh E của r3 SỐNG lại, hai canh E của r2 vẫn
  GIẾT; gỡ riêng ba ô ngoại lệ của r2 ⇒ cả năm canh E vẫn GIẾT; gỡ **cả hai** ⇒ cả năm canh E SỐNG lại (cùng ba dò mở
  rộng khác của `z_exc_*`), hai đối chứng vẫn GIẾT. Hai canh E của r2 vì vậy có hai nguồn giết trên ứng viên r4; mệnh
  đề "gỡ riêng ba ô ⇒ SỐNG lại" chỉ đúng trên IMP-R2-GO của r2 (chưa có `E698`, đo khi ấy: 2/2). Bậc hai này đo trên
  bản đo riêng của ứng viên, như A1-b2; handoff đính bảng ba cây.

## 7. `ci_budget`

Protocol §12 chia chi CI theo mục đích. Đơn vị là **lượt workflow run**; attempt tính riêng; mỗi
lượt ghi kèm exact SHA.

| loại | `used / reserved / limit` | ghi chú |
|---|---|---|
| Gate tự động | `0 / 1 / 1` | **Một** lượt `ci.yml`, bắn khi mở PR sau khi review đạt 0/0/0 (Q7). `thu-hoi` chạy theo sự kiện PR riêng và không tính vào đây. Hạn mức 1 là cách đọc nhãn "CI 1 lần khi sạch". Không chạy CI trong vòng lặp. Ước theo lượt `36696528580`: 14 job, toàn ubuntu. **Phạm vi sổ:** chỉ PR THI CÔNG của packet. Ruleset đòi bốn context cho MỌI PR vào master, nên PR bookkeeping (đặc tả và lease; hồ sơ land) và mỗi lần merge vào master (`on: push: branches: [master]`) cũng bắn `ci.yml`; các lượt ấy là chi ngoài packet, ghi ở hồ sơ land, không tính vào `limit` 1. Nếu phải đẩy thêm commit lên nhánh PR thi công sau khi đã mở thì mỗi lần đẩy bắn một lượt nữa, tức vượt `limit` ⇒ DỪNG, hỏi chủ kho (S10). |
| Phép đo được cấp | `0 / 0 / 0` | Không có `workflow_dispatch`, không Windows (Q8). |
| Thăm dò chưa cấp | không | — |

**Chi phí đo được trên ứng viên tham chiếu** (container 4 lõi, máy rảnh; `t52`/`t53`/`t54` của nền và
IMP-R2G đo trong **một** lệnh lúc 03:01:07Z–03:01:44Z 01-10; không lượt đo nào khác chạy song song, loadavg 1 phút lúc bắt đầu là 2,49 — đuôi của A5 vừa xong; mỗi số là một lần đo, không phải trung bình):

| ca hoặc đại lượng | Python | nền `fc852ff` | IMP-R2G | chênh |
|---|---|---|---|---|
| `t52` | 3.11.15 | 3,64 s | 3,99 s | +0,35 s (ca không đổi; nhiễu) |
| `t53` | 3.11.15 | 0,36 s | 4,59 s | +4,23 s |
| `t54` | 3.11.15 | 1,80 s | 2,70 s | +0,90 s |
| `t52` | 3.12.3 | 4,38 s | 4,59 s | +0,21 s (ca không đổi; nhiễu) |
| `t53` | 3.12.3 | 0,47 s | 4,53 s | +4,06 s |
| `t54` | 3.12.3 | 1,89 s | 2,44 s | +0,55 s |
| số mục `DOT_BIEN` | — | 416 | 459 | +43 |
| một lượt 56 ca của một dò (trung bình, 4 tiến trình) | 3.11.15 | 29,8 s | 34,3 s (IMP-R2) | ≈ ×1,15 |
| một mảnh A5 (57–58 đột biến, 4 tiến trình) | 3.12.3 | — | 497–521 s | — |

`t53` và `t54` chạy trong **mọi** lượt đột biến. **Ước của r2** (giữ để truy dòng dõi; r3 thay bằng đoạn *Cập nhật
r3* dưới) về tác động lên mảnh CI (không đo trên runner): lượt hậu-merge `36696528580` có 8 mảnh 12,7–18,2 phút cho 416 đột biến, tức khoảng 52 đột
biến mỗi mảnh và 59–84 s mỗi lượt đột biến trên runner (4 tiến trình). Giả định thời lượng mảnh tỷ lệ
với (số đột biến × thời lượng một lượt), và tỷ lệ thời lượng một lượt trên runner bằng tỷ lệ đo ở
container: trung bình một lượt 56 ca của một dò, 4 tiến trình song song, là 29,8 s trên nền (162 dò) và 34,3 s
trên IMP-R2 (209 dò), Python 3.11.15, tỷ lệ ≈ 1,15. Khi ấy 459 đột biến cho mảnh dài nhất khoảng 23,1 phút (cộng
3,4–4,9 phút mỗi mảnh), dưới trần 30 phút của job. Đăng ký trọn 215 dò thuộc A1–A3, A8 thay cho 43
canh (631 đột biến) cho mảnh dài nhất khoảng 31,8 phút, **vượt** trần 30 — lý do định lượng của việc
chỉ đăng ký 43 canh. Tích đầy đủ của M3 (6612 kịch bản) ước cộng khoảng 22–37 s (chênh `t54` đo được 0,55–0,90 s cho 162 kịch bản mới, tức 3,4–5,6 ms mỗi kịch bản, nhân 6612) mỗi lượt `t54`; đó
là lý do M3 chỉ lấy tích biên.

**Cập nhật r3** (giữ để truy dòng dõi; r4 thay bằng đoạn *Cập nhật r4* dưới). Ba hướng của r3 thêm ô vào `t52` (bộ ghi), `t53` (M1b, M5b) và `t54` (tầng `main`), mà ba ca ấy chạy
trong **mọi** lượt đột biến. Thay cho tỷ lệ trung bình mỗi dò (nhiễu theo tải máy dùng chung), r3 ước bằng **chênh
lệch ca**: một lượt đột biến chạy trọn 56 ca, nên thời lượng một lượt tăng khoảng Δ = tổng qua `t52`, `t53`, `t54` của
(thời lượng ứng viên − thời lượng nền). Đo bằng Phụ lục I (§1.9.9): Δ = 7,04 s trên `v3_all` (cả ba hướng r3) và 4,94 s trên `cand` (đúng chữ r2). Với T₀ ≈ 29,8 s (trung bình một
lượt 56 ca trên nền ở lô nhẹ tải nhất, `ra_nen`, Python 3.12.3, 4 tiến trình) và 470 đột biến, mảnh dài nhất ≈ 18,2 phút
× (470/416) × (T₀ + Δ)/T₀ ≈ 25,4 phút với Δ của `v3_all` — dưới trần 30 phút của job. Ngưỡng A4-g (Δ ≤ 10 s) cho ≈ 27,5 phút. Đăng ký trọn
350 dò thuộc A1–A3, A8 của tập đóng r3 thay cho 54 canh (766 đột biến) cho ≈ 18,2 × (766/416) × (T₀ + Δ)/T₀ ≈ 41,4 phút (cùng Δ),
**vượt** trần — lý do định lượng của việc chỉ đăng ký canh.

**Đo lại ở review lượt 3** (chữ của `HINT.patch` lượt 3, giữ nguyên; ứng viên độc lập; container 4 lõi dùng chung với một phiên khác). Δ tường của Phụ lục I trên MỘT
ứng viên đúng chữ: 5,9–6,5 s lúc rảnh, 6,8–7,0 s với hai tiến trình ăn CPU, 8,0–8,1 s với bốn tiến trình đo chạy song song,
9,0–11,7 s với bốn tiến trình ăn CPU (11,7 s ⇒ ĐỎ giả); Δ CPU (tự thân + con) của cùng ba ca: 6,2–6,5 s ở mọi tải. Một mảnh A5 thật:
nền 522,9 s cho 52 đột biến, ứng viên 669,6 s cho 59 đột biến (mỗi đột biến: tường ×1,129, CPU ×1,295), nên dự báo mảnh dài nhất
ở Δ = 10 s nằm trong dải 24,8–30,3 phút tuỳ runner bão hoà CPU hay không (KHÔNG ĐO ĐƯỢC trên runner): ≈ 27,5 phút là điểm giữa
của dải, biên 2,5 phút không chứng minh được. Revision sau: ghi điều kiện đo, đo thêm Δ CPU, thay lời khai biên bằng dải đo.

**Cập nhật r4** (thay đoạn *Cập nhật r3* cho mọi việc về sau; số đo ở §1.10.5). Mô hình r4 khác mô hình r3 ở ba chỗ, mỗi
chỗ một số đo:
(1) **Cơ sở thời gian là CPU, không phải giây tường.** Một lượt đột biến chạy trọn 56 ca, nên phần thêm của ứng viên vào
mỗi lượt là Δ_CPU của `t52` + `t53` + `t54`; chia cho CPU mỗi đột biến trên nền (C₀) ra tỷ lệ (ở A4-g, C₀ được thay bằng
C56 đo cùng lệnh — §6). C₀ đo bằng một mảnh A5 thật (`CONG_CU_TEST_MANH=0/8`, đúng lệnh A5, CPU của cả cây tiến trình
con): nền 1238,7 s CPU cho 52 đột biến, tức C₀ = 23,82 s (review lượt 3 đo 21,20 s trên máy nhẹ tải hơn — cùng mã,
khác tải); `v4_all` 1803,8 s cho 59 đột biến, tức 30,57 s; CPU mỗi đột biến tăng 6,75 s, tỷ lệ 1,283.
(2) **Lực lượng của mảnh lớn nhất, không phải trung bình.** `_phan_manh` chia theo `i % n == k`, nên 470 đột biến cho
sáu mảnh 59 và hai mảnh 58; 416 đột biến cho tám mảnh 52. Tỷ lệ của mảnh lớn nhất là 59/52 = 1,1346, không phải
470/416 = 1,1298.
(3) **Cơ sở của runner đọc lại, không chép.** Run `36696528580` (hậu-merge PR #696, head `423b4ba`, blob
`ops/cong_cu_test.py` trùng nền), đọc qua REST lúc soạn r4: tám job `gate-cong-cu (ubuntu-latest, k)` dài 17,58 · 18,23 ·
15,83 · 18,05 · 18,12 · 12,67 · 17,67 · 18,05 phút (k = 0…7); trong job dài nhất (k = 1), bước G5 chiếm 17,82 phút, các bước
khác 0,37 phút. Mô hình nhân **cả job** (18,23 phút) với tỷ lệ, tức coi cả phần cài đặt cũng chậm theo — thận trọng.
Mảnh dài nhất ≈ 18,23 × (59/52) × (C₀ + Δ_CPU)/C₀ phút. Ở tỷ lệ đo được của `v4_all` — 1,283 từ hai mảnh thật, 1,259–1,308 từ
sáu lượt Phụ lục I bản r4 (§1.10.5) — mảnh dài nhất ≈ 26,0–27,1 phút; ở ngưỡng r = 1,35 của A4-g ≈ 27,9 phút: biên ≥ 2 phút
dưới trần 30, **theo mô hình**.
**Ba giả định**, không đo được trên runner: (a) thời lượng job mảnh trên runner tăng theo tỷ lệ CPU mỗi đột biến — đúng
khi runner bão hoà CPU; kho là `private` (đo qua REST), và nếu runner là cấu hình 2 vCPU mà tài liệu GitHub công bố cho
kho riêng tư thì `_so_tien_trinh_ban_kinh` chạy 2 tiến trình trên 2 lõi, tức bão hoà — số vCPU thật **KHÔNG ĐO ĐƯỢC** (log
job nằm ở kho blob mà phiên này không đọc được); nếu runner không bão hoà thì thời lượng tăng chậm hơn tỷ lệ CPU, nên mô
hình là **cận trên** chứ không phải ước giữa; (b) phần thêm mỗi lượt đột biến bằng Δ_CPU đo trên ba ca **chưa** đột biến —
đo được: tỷ lệ r của Phụ lục I bản r4, tính với C56 của chính lượt đo, là 1,259–1,308 (trung bình 1,282) qua sáu lượt,
khớp tỷ lệ CPU mỗi đột biến của hai mảnh thật, 1,283; tính bằng giây thì phần thêm mỗi đột biến trong mảnh là 6,75 s so
với Δ_CPU 5,96–7,51 s — giây CPU tuyệt đối trôi theo tải, tỷ lệ thì không; (c) 54 canh tốn mỗi lượt như một đột biến
cũ (cùng 56 ca). **Không đổi cách chia mảnh:** số mảnh là ma trận của `ci.yml` (ngoài write set, S1); `_phan_manh` là
hợp đồng mà `t52` kiểm (`phan_hoach` đòi đúng `range(k, so_ten, n)`); và tám job của run trên cùng mang 52 đột biến mà
dài 12,67–18,23 phút, tức chênh giữa các mảnh không do số đột biến, nên cân lại số đột biến không chạm nguyên nhân.
Đăng ký trọn 350 dò thuộc A1–A3, A8 của r3 (766 đột biến) vẫn vượt trần theo mô hình này: mảnh lớn nhất mang
⌈766/8⌉ = 96 đột biến, ≈ 18,23 × (96/52) × 1,283 ≈ 43,2 phút với tỷ lệ CPU đo được của `v4_all`.

## 8. Điều kiện dừng

- **S1:** cần sửa thứ gì ngoài `ops/cong_cu_test.py`, hoặc cần đổi thân một hàm liệt kê ở A4-d
  ⇒ DỪNG, handoff, revision mới.
- **S2:** lúc cấp lease, so tập tên+OID ref bị lệch, hoặc `ai-dang-giu ops/cong_cu_test.py` ≠
  `NGƯỜI_GIỮ 0`, hoặc chưa có comment chủ kho xác nhận closure neo `spec_hash` **của r4** (Q10)
  ⇒ không cấp.
- **S3:** #671 land trước và đổi `ops/cong_cu_test.py` ⇒ revision mới dời nền **trước** khi cấp.
- **S4:** một mục canh hay một dò của tập đóng chỉ chết bằng `tin_dung_gia` hoặc với bán kính > 1,
  và muốn sửa thì phải đổi mã ngoài phạm vi ⇒ DỪNG.
- **S5:** vượt ≤ 3 tệp hoặc ≤ 300 dòng thêm (ADR-0044 cho `sensitive`; chủ kho giữ mặc định, Q12; "dòng thêm" là cột
  thêm của `git diff --numstat fc852ff -- ops/cong_cu_test.py`, §11.1 (B)) ⇒ DỪNG, hỏi chủ kho. **Ước r3** (đo trên biến
  thể, không phải bản giao; §1.9.9): `cand` — ứng viên đúng chữ r2 của reviewer lượt 2, dựng gọn — là +150/−4 (r2
  từng ước +191/−5 trên IMP-R2G, viết dài hơn); ba hướng r3 trên `v3_all` thêm +121 dòng (M5b ≈ 60, M1b ≈ 11, M2b
  ≈ 50) theo lối viết KHÔNG tối ưu số dòng của một biến thể đo, tức `v3_all` = +271/−4; cộng 11 hàng canh r3 (một
  dòng mỗi hàng như `cand`) và chú thích M4 (ước 10–25 dòng) ⇒ **khoảng 292–307 dòng thêm nếu viết như biến thể đo,
  có thể VƯỢT trần 300**; nếu phần r3 được viết gọn ngang tỷ lệ `cand`/IMP-R2G (≈ 0,8) thì ≈ 268–283. Đặc tả không
  nới trần và không chọn hộ phần cắt: vượt 300 thì DỪNG, hỏi chủ kho. Phần tốn dòng và tốn `t52` nhất là ô bộ ghi phủ
  `D698` theo khúc tên tệp (M2b). **Ước r4** (đo trên biến thể, không phải bản giao; §1.10.8): `v4_all` = `v3_all` + 11
  hàng canh r3 (một dòng mỗi hàng) + M6 ở bốn chỗ gọi + hai lần gọi bộ ghi và so dòng in = **+291/−4**, tức phần r4
  thêm vào `v3_all` là +20 dòng (11 hàng canh, 9 dòng cho M6 và T5) theo cùng lối viết không tối ưu số dòng. `v4_all`
  mang sẵn chú thích của `v3_all`, nhưng chưa có chú thích M4 (A7) đứng riêng dòng cho các chỗ thêm của r3–r4; cộng
  chúng (ước 0–15 dòng) ⇒ **khoảng 291–306 dòng thêm: có thể VƯỢT trần 300**. Luật DỪNG ở trên không đổi; một ứng viên
  độc lập của reviewer lượt 3 (`ind4`, chưa có M6 và T5 của r4) đã đo +311/−4.
- **S6:** không có trần số vòng review ngoài trần trục VÒNG của ADR-0048, đã được nâng bằng khối
  `nang_tran` (Q5); vòng lặp dừng khi đạt 0/0/0. Các quy tắc dừng theo lớp của protocol §12 vẫn áp. Chúng
  được **chép nguyên văn bằng máy** (không gõ lại) từ `docs/PROTOCOL_DA_PHIEN.md` dòng 1043–1056, blob
  `0dedc3d922dc86a78c71194b084b4bba7afda517` (cùng blob ở `fc852ff` và ở `20ec8d5`); sha256 của 14 dòng trích,
  nối bằng LF, là `dc93c2a34d4a6e64b9ab65285bfb431ad43bdf5b8f73f8a960f4205f311f7715`. Nguồn có thẩm quyền là protocol; đoạn dưới chỉ là bản chiếu:

  > **Tín hiệu không hội tụ theo lớp.** Với chuyển tiếp từ lượt r sang r+1, đặt U là tập
  > slug lớp còn mở ở cuối lượt r, F là tập con của U được reviewer lượt r+1 xác minh
  > ĐÃ VÁ THẬT theo §8.3. Tỷ lệ = |F|/|U|; nhiều finding cùng lớp chỉ tính một lần.
  > U rỗng thì tỷ lệ không xác định (`N/A`), không phải 0% hay 100%; không ghép hai tỷ lệ
  > thấp qua một chuyển tiếp N/A. Hai chuyển tiếp liên tiếp có tỷ lệ <50% thì dừng vòng
  > vá và đưa bằng chứng tới Review Rescue Checkpoint bên dưới. Ngưỡng này là heuristic
  > kế thừa từ #523, không là chứng minh thống kê; không thay trần độc lập.
  >
  > Báo riêng các lớp mới tại r+1 (không nằm trong U), lớp tái mở và phần chưa đo; chúng
  > không vào tử số F. Tỷ lệ cao chỉ nói về tập U, không chứng minh hội tụ khi lớp mới
  > vẫn xuất hiện, không thay điều kiện dừng theo class/Packet hay bằng chứng approval.
  > Một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint;
  > ba biểu hiện của lớp trong cùng một lượt chỉ là một lần xuất hiện. Revision/scope
  > cut không reset lịch sử đó, không tự cấp thêm review call hoặc attempt.

  Hệ quả cho packet này, đọc từ chữ trên:
  - **Chuyển tiếp lượt 1 → lượt 2** (đọc từ cột trạng thái của `VERDICT.md` lượt 2, không phải phán quyết
    của phiên soạn): U = 8 lớp của lượt 1; lượt 2 ghi "ĐÃ ĐÓNG" trọn cho `luc-luong-chi-quet-truc-khong-quet-tich`
    và `muc-tieu-m1-m4-cau-chu-thieu-chinh-xac`, "ĐÃ ĐÓNG phần P2, VÁ SINH LỖI MỚI" cho `tran-cu-adr-0043-da-bi-thay`,
    còn năm lớp kia là TÁI PHÁT hoặc VÁ HỜ. Tỷ lệ = 2/8 hoặc 3/8 tuỳ cách đọc dòng `tran-cu-…` — **dưới 50% theo cả
    hai cách đọc**. Nếu chuyển tiếp lượt 2 → lượt 3 cũng dưới 50% thì quy tắc thứ nhất kích hoạt: dừng vòng vá, đưa
    bằng chứng tới Review Rescue Checkpoint. Việc chốt F/U chính thức là của phiên điều phối.
  - **Checkpoint theo lớp.** Lịch sử không reset, nên hai lớp kế thừa trong phạm vi ở §9
    (`doc-che-do-van-tay`, `main-luc-luong-gia-tri`) đã quá ngưỡng ba lượt trước packet này. Mỗi lần một lớp kế
    thừa xuất hiện lại trong review của packet (kể cả review đặc tả), phiên điều phối báo chủ kho kèm bảng lớp
    **trước** khi soạn revision hay vá tiếp. Lượt 1 và lượt 2 đều là lần như thế (§9). Trước r3: phiên điều phối
    đã chiếu verdict lượt 2 (có BẢNG LỚP) lên #698 trước khi giao soạn r3 — theo chỉ thị giao việc; ID comment
    không có trong dữ kiện cấp cho phiên soạn, nên việc ấy là lời khai, **KHÔNG ĐO ĐƯỢC** từ tệp này. Comment Q10
    xác nhận closure chỉ ghi nhận rằng chủ kho đã thấy bảng; nó không thay việc báo trước. (r4 đọc lại #698 qua REST:
    bản chiếu verdict lượt 2 là comment `5928410072`, tạo 09:14:34Z 01-10, trước commit r3 `276a65f` lúc 12:35:58Z
    cùng ngày; nó trước hay sau **lúc giao** soạn r3 thì vẫn KHÔNG ĐO ĐƯỢC.)
  - **Chuyển tiếp lượt 2 → lượt 3** (đọc từ phần TỶ LỆ VÁ THẬT của `VERDICT.md` lượt 3, không phải phán quyết của
    phiên soạn): U = 16 lớp của lượt 2; F = 13 ⇒ **13/16 = 81,25%** (cách đọc nghiêm, xếp `a5-canh-khong-kiem-bang-do`
    vào TÁI PHÁT: 12/16 = 75,00%). Không có hai chuyển tiếp **liên tiếp** dưới 50% (1 → 2 dưới, 2 → 3 trên), nên quy
    tắc thứ nhất **không** kích hoạt. Lớp mới tại lượt 3, không vào tử số: 3 (hai P2, một P3) — như chữ protocol dặn,
    tỷ lệ cao không chứng minh hội tụ khi lớp mới vẫn xuất hiện.
  - **Quy tắc thứ hai — "một lớp xuất hiện ở ba lượt review khác nhau đòi xem lại cách làm tại checkpoint" — ĐÃ
    THOẢ cho ba họ** (đếm theo bảng nối của chính các verdict, `VERDICT.md` lượt 3 phần TỶ LỆ VÁ THẬT):
    họ `ra` — `ra-thieu-hang-chuan-hoa-lop-b` (lượt 1) → `ra-ha-nguon-main-bo-ghi-chua-co-o` (lượt 2) → T5 và thành viên
    hạ nguồn (lượt 3); họ thời gian/tiêu chí — `tieu-chi-nghiem-thu-thieu-chinh-xac` (lượt 1) →
    `t53-thoi-gian-khong-co-tieu-chi-do` (lượt 2) → đồng hồ và biên của A4-g (lượt 3); họ bậc hai —
    `tieu-chi-nghiem-thu-thieu-chinh-xac` (lượt 1) → `bac-hai-trung-so-hieu-va-khong-co-nhom-chuan` (lượt 2) → mệnh đề
    đầu của A8 (lượt 3). Cả ba biểu hiện ở lượt 3 đều là P3 hẹp. **r4 KHÔNG tự quyết** việc đưa packet tới Review Rescue
    Checkpoint hay đổi cách làm thay cho checkpoint ấy: đó là quyết định của phiên điều phối và chủ kho. r4 chỉ khai:
    (a) điều kiện đã thoả; (b) bản chiếu verdict lượt 3 trên #698 — comment `6038138825`, tạo 12:42:18Z 07-10, đọc lại
    qua REST lúc soạn r4 — có bảng sáu lớp và đoạn nguyên văn "ba họ lớp (`ra`, thời gian/tiêu chí, bậc hai) đã xuất
    hiện ở ba lượt. Đưa lên Review Rescue Checkpoint hay không là quyết định của chủ kho."; comment ấy có trước lệnh đo
    đầu tiên của phiên soạn r4 (12:45:57Z 07-10, theo `uptime` của lệnh ấy), còn việc chủ kho đã đọc nó hay chưa thì
    **KHÔNG ĐO ĐƯỢC**; (c) với mỗi họ, r4 đổi **cách làm** chứ không chỉ
    vá câu chữ — họ `ra` và họ ngoại lệ: liệt kê theo **chỗ gọi** (M6) và theo **mọi chỗ dùng** `tep` (T5), có dò răng
    cho từng chỗ (Phụ lục J); họ thời gian: đổi đại lượng đo từ giây tường sang CPU, và đổi mô hình biên sang lực lượng
    mảnh lớn nhất (§7); họ bậc hai: mỗi mệnh đề bậc hai của A8 đo trên chính ba cây gỡ của ứng viên r4 (§1.10.6) thay vì
    chép số của IMP-R2-GO. Ba lời khai (c) chỉ là lời khai của phiên soạn cho tới khi một lượt review xác minh.
- **S7:** hai nhánh tách riêng, mỗi nhánh một điểm dừng.
  - **S7a — `gate-registry (ubuntu-latest)` đỏ.** Đỏ đúng định nghĩa tác nghiệp "đỏ vì hết trần" ở
    `required_checks` (c) thì làm theo Q9: (c) được coi là đạt khi (a) và (b) xanh, ghi nợ có neo. Đỏ vì lý do
    khác ⇒ DỪNG.
  - **S7b — job `thu-hoi` đỏ, vì bất kỳ lý do nào ⇒ DỪNG, hỏi chủ kho.** Tiền lệ: lượt PR #696 (run
    `36688032631`, head `cc78b33`) có `CHAN [12]: KHÔNG_XÁC_ĐỊNH: S c16bec639efa không phải tổ tiên của H
    cc78b33bd04d` — mục log thô 765 và 767, nằm ở dòng 103–104 của
    `ops/land/pr696-wp668-provenance/trich-log.txt`. Vì sao (d) vẫn là điều kiện dù chưa là required check:
    `required_checks` (d). Không phiên nào tự xếp một lượt `thu-hoi` đỏ thành "bỏ qua được" hay "thất bại";
    người quyết là chủ kho.
- **S8:** lease hết hạn ⇒ ngừng sửa, handoff (§7).
- **S9:** phát hiện ngoài spec ⇒ handoff/successor (§3.2), không tự mở write set.
- **S10:** chưa đạt 0/0/0 mà đã muốn mở PR hay chạy CI, hoặc sau khi mở PR mà cần thêm một lượt
  CI ⇒ DỪNG, hỏi chủ kho (Q7).

## 9. `hinh_dang_ke_thua`

Đây là packet khắc phục của #668. Số đếm hình dạng lỗi chép từ hồ sơ tiền nhiệm (L4), mỗi số kèm
nguồn; dòng "review đặc tả wp698" là số của chính packet này.

| lớp (slug) | số lượt review có finding | nguồn |
|---|---|---|
| `registry-nang-luc` (lớp (6) của #668) | **≥ 5** tính tới lượt 20; lượt 21 có 0 finding và xếp (e) là giới hạn; lượt 22 có F48 ⇒ **6** nếu tính cùng lớp | #668 comment `5905962202` ("lớp registry năng lực ra finding lượt thứ 5"); `…-review-21-claude-verdict.md` H6; comment `5911284002` |
| `doc-che-do-van-tay` | **≥ 5** trước packet: Codex lượt 12, 13, 14, 15, và F49 ở lượt 22. Thêm F46, mà số lượt **KHÔNG ĐO ĐƯỢC** vì hồ sơ phiên `session_01VYtkBy…` không có trong kho. **Review đặc tả wp698 lượt 1: +1** (ba lớp con `ra-thieu-hang-chuan-hoa-lop-b`, `a1-khong-do-vi-tri-thanh-vien`, `khai-khong-do-duoc-nhung-do-duoc`; ba biểu hiện cùng lượt tính một lần) ⇒ **≥ 6**. **Review đặc tả wp698 lượt 2: +1** (năm lớp nối lớp này theo cột "nối" của VERDICT lượt 2: `m5-ngoai-le-chi-ba-kieu`, `ra-ha-nguon-main-bo-ghi-chua-co-o`, `head-nhieu-dong-chi-tach-lf-chua-co-o`, `a1-tap-dong-thieu-do-theo-nhom-unicode`, `head-moi-vi-tri-moi-thanh-vien-qua-loi`; cùng lượt tính một lần) ⇒ **≥ 7**. **Lượt 3: +1** (`ra-ha-nguon-main-bo-ghi-chua-co-o` TÁI PHÁT hẹp ở lượt 3 — đọc qua chuỗi nối của VERDICT lượt 2, vì VERDICT lượt 3 chỉ nối về slug lượt 2, không nối thẳng về lớp kế thừa) ⇒ **≥ 8** | chú thích mã trên nền: F29 :8106, F31 :8110, F33 :8041, F30/F32/F34 :8144, F36 :2257; comment `5911284002`; VERDICT.md lượt 1 (sha256 `c825a405…2133`); VERDICT.md lượt 2 (sha256 `e281338f…3968`); VERDICT.md lượt 3 (sha256 `d3d848ed…b955`) |
| `main-luc-luong-gia-tri` | **≥ 3** trước packet: F42 (Codex lượt 19), F44 (lượt 20), F50 (lượt 22). F47 **KHÔNG ĐO ĐƯỢC**. **Review đặc tả wp698 lượt 1: +1** (`luc-luong-chi-quet-truc-khong-quet-tich`) ⇒ **≥ 4**. **Lượt 2: +1** (`ra-ha-nguon-main-bo-ghi-chua-co-o` — VERDICT lượt 2 nối nó với lớp này qua F42/F44, vì đường `ra` trong `main` là dây nối giá trị của `main`) ⇒ **≥ 5**. **Lượt 3: +1** (cùng slug ấy TÁI PHÁT hẹp; đọc qua cùng chuỗi nối) ⇒ **≥ 6** | chú thích mã :2233, :2240; comment `5911284002`; VERDICT.md lượt 1, lượt 2 và lượt 3 |

Cả ba lớp đã qua ngưỡng của protocol §12. r1 tuyên bố "đổi cách làm" (ô dẫn xuất theo lớp; quét
trọn miền) nhưng review lượt 1 đo được rằng đổi ấy mới có trên chữ: A1 của r1 chỉ giết dò theo
**tên phép**, nên một bản thi công thoả chữ (IMP-MIN) vẫn xanh A1–A3 mà còn 28/47 dò anh em sống;
còn "quét trọn miền" của M3 thực chất là ba trục riêng. r2 đổi cách làm **ở tiêu chí**, không chỉ
ở chữ mục tiêu:

- Lớp B dùng **miền dẫn xuất từ thuộc tính** (`D698` × mọi vị trí) cho cả bốn bộ đọc, và tiêu chí
  A1/A2 là một **tập dò đóng có tên** (Phụ lục C) phủ vị trí × thành viên × họ ký tự — không còn là
  chín tên phép. Đây là *"danh sách CẤM không bao giờ đủ — đảo thành danh sách CHO PHÉP"* áp đúng
  chỗ: miền thử được định nghĩa bằng một luật, không bằng một danh sách chuỗi xấu.
- Lớp D thêm **tích biên** và đổi lời khai thành "trục trọn cộng tích biên".
- Mỗi tập ở §6 có phép **PHẢI ĐỎ Ở** trên hai ứng viên "thoả chữ r1" của reviewer: tiêu chí r2
  phân biệt được bản thi công tối thiểu với bản đủ, điều mà tiêu chí r1 không làm được.

Riêng lớp A, cách làm cũ đã bị chính verdict lượt 22 bác. Chốt AST ở đó là danh sách **CẤM**
(`dk` thiếu `ast.TryStar`) và áp lên **tên** thay vì **thẩm quyền**, đúng lỗi *"phân biệt cách
viết, không phân biệt thẩm quyền"*. Chủ kho quyết ghi nợ, không vá trong packet này (Q1).

Kế thừa thêm hình dạng *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*: lượt 22 nêu 3 finding,
phép đo của r1 ra 24 đường sống trong 4 lớp; review lượt 1 của r1 nêu 8 lớp / 52 biểu hiện, phép đo
của r2 dựng tập đóng 221 dò (§2) thay vì chỉ vá 52 biểu hiện được chỉ. Review lượt 2 nêu 16 lớp / 56 biểu hiện, và bốn lớp P2
của nó lại đúng hình dạng ấy (vá đúng tầng/đúng ba kiểu/đúng LF được chỉ). r3 vì vậy **tự liệt kê hết đường vào trước khi vá**
cho từng lớp P2 (§1.9) và đo cả hướng sửa của HINT trên chính các đường nó bỏ sót: miền ngoại lệ của HINT, tập ký tự tách của
HINT, và tầng `ra` của HINT đều để lọt đường thứ ba đo được (§0-r3). Review lượt 3 nêu 6 lớp / 11 biểu hiện, và cả hai
lớp P2 mới lại đúng hình dạng ấy, chỉ dời xuống một tầng: ô bộ ghi là **một** trong bốn chỗ gọi mà một ngoại lệ của mã
bị đo thoát ra được thành tín dụng giả, và `x3_wr5_nfkc` là **một** trong 470 mục mà mỏ neo có thể bị văn bản mới đứng
trước nó kéo đi. r4 vì vậy không vá theo hai chỗ được chỉ: nó liệt kê **theo chỗ gọi** (M6, bốn chỗ cộng M5b) và **theo
mọi mục** (phép đếm của Phụ lục F bản r4 phủ cả 470), rồi dựng cho mỗi chỗ một dò răng và một biến thể gỡ riêng chỗ ấy để
đo dò ấy ĐỎ đúng ở đó (§1.10).

## 10. `chua_do_duoc`

- Nội dung của `8d7faef` và `5a071b8` (chốt AST, bản vá F46/F47): không có trong kho. Đo lúc
  15:11:55Z, sau khi fetch đủ 458 ref, `git cat-file` báo không có. Vì thế không đối chiếu được
  **nguyên văn** F46 phần "kiểu ngoại lệ", nguyên văn F47, và mọi hint. Phần **đo được** của F46 —
  tập ngoại lệ mà `_van_tay` bắt — đã đo và vào M5 (§1.8.5); nếu F46 nói điều khác thì phần ấy vẫn
  KHÔNG ĐO ĐƯỢC.
- `VERDICT.md` lượt 22 (sha256 `1ffe9d6e…42`) và năm tệp patch: chỉ có băm trong comment
  `5911284002`.
- Windows: **không đo** (chủ kho quyết, Q8); nợ `windows-chua-do-o-moi-wp698`. Nhánh
  `_CO_SYMLINK=False` cũng chưa đo, vì container có symlink.
- Kích thước diff của bản vá thật: chưa thi công thì chưa đo được; có **ước** bằng IMP-R2G (S5).
- Ba nhóm điểm mã ngoài `D698` (`Lo` không có ánh xạ NFKC, `Co`, `Cn`): miền M1 có **một** đại
  diện mỗi nhóm (`N698`), nên dò "xoá cả nhóm" bị bắt (12 dò, §1.8.4), còn một phép chỉ xoá một
  **tập con khác** trong nhóm (ví dụ chỉ chữ Hangul) thì không. Tập đóng không có dò cho tập con
  như thế; đó là giới hạn khai của danh sách, không phải thứ đã đo mà chưa ghi.
- Bản Unicode khác 14.0.0 và 15.0.0: `D698` đổi theo; đã đo đúng hai bản ấy (§1.8.8).
- Thời lượng trên runner CI của các ca `t53`/`t54` mới: chỉ **ước** từ container (§7).
- Khối `nang_tran`: không cổng máy nào đọc (§ đầu tệp). Việc lease có chép đúng khối hay không chỉ
  được kiểm bằng mắt.
- ID comment verdict lượt 1 trên #698 và mọi số chỉ có trên GitHub mà r2 không đọc lại (§ đầu tệp).
- Danh tính người ký lease (#566); effort thực tế của executor.
- **r3:** ID comment verdict lượt 2 trên #698; `origin/master` lúc soạn r3 (phiên r3 không có mạng; mirror của
  sandbox lượt 2 ghi `20ec8d5`, header).
- **r3:** miền `E698` (M5b) chỉ chứa lớp đã nạp lúc quét. Một đột biến vừa nhập mô-đun mới vừa nêu lớp của mô-đun ấy
  trong mệnh đề `except` nằm ngoài miền; đó là đột biến hai bước, khác hình dạng "mở rộng tập bắt bằng một tên".
- **r3:** ô bộ ghi (M2b) và ô nhiều thẻ (M1b) trên Windows: chưa đo (Q8). Trên POSIX, khúc tên tệp phủ `D698` bỏ
  U+0000 và `/` (không là ký tự tên tệp hợp lệ), và đường "mọi thành viên" ở tầng `main` bỏ U+0000 (không nằm được
  trong biến môi trường): hai điểm mã ấy không có ô ở tầng hạ nguồn.
- **r3:** thời lượng trên runner của `t52`/`t53`/`t54` có ô r3: chỉ ước từ container (§7).
- **r4:** runner CI có bão hoà CPU hay không, và tỷ lệ thời lượng mảnh trên runner có theo tỷ lệ CPU hay không: **KHÔNG ĐO
  ĐƯỢC** (không chạy CI trong vòng lặp, Q7). Biên 30 phút của §7 bản r4 đứng trên ba giả định khai ở đó; nó là cận trên
  theo mô hình, không phải phép đo trên runner.
- **r4:** A4-g bản r4 **không** bắt một bản thi công chậm mà không tốn CPU (ngủ, chờ tiến trình ngoài, chờ hết giờ): phép
  CPU không thấy thời gian chờ, còn đồng hồ chỉ là chỉ báo. Đo ở §1.10.5 bằng `tv_cham` (ngủ 11 s trong cửa con). Một bản
  như thế, nếu có, chỉ lộ ở CI: job mảnh vượt `timeout-minutes: 30` thì đỏ (fail-closed), nhưng đã tiêu lượt CI duy nhất
  (Q7, S10).
- **r4:** A5 trọn tám mảnh không chạy ở bước soạn r4; chỉ chạy mảnh `0/8` trên nền và trên biến thể `v4_all` (§1.10.5).
- **r4:** trên `v4_all`, phần hồi quy chỉ chạy T-C của C + H, dò cùng tên 11 canh r3, Phụ lục J, ba mục cũ của §1.10.2 và
  28 dò `y_*` (§1.10.8); T-B, T-D, NGOÀI, KHAI và phần còn lại của T-E thuộc C + H **không** chạy trên `v4_all` (r3
  cũng chỉ chạy trên `v3_all` 158 dò thuộc các nhóm `exc`, `head`, `ra` — §1.9.1 — không phải trọn tập đóng). Nghiệm
  thu chạy trọn tập đóng trên ứng viên thật (A1–A3, A8), nên khe này không chuyển sang bản giao.
- **r4:** 35 dò của Phụ lục J chỉ đo ở nghiệm thu; r4 **không** thêm canh cho chúng (§5, §11.1 (D)), nên sau land chỉ chỗ
  gọi bộ ghi còn canh thường trực (`x_wr_ra_nfkc` ném `OSError` khi thiếu khối bắt — §1.10.3); khối bắt ở `doc`, ở quét
  `head`, ở vòng `main`, hai lần gọi bộ ghi và phép so dòng in không có canh. Nợ `j-chua-co-canh-wp698`.
- **r4:** ruff 0.15.15 (bản ghim) không có trong container; A4-b chỉ đo bằng 0.15.8 (§1.10.8). `jsonschema` không có, nên
  `t2` luôn `bo_qua` ở mọi phép đo của r4.

## 11. QUYẾT ĐỊNH CHỦ KHO

**Nguồn:** #698 comment **`5914438647`**, tạo 2026-09-30T15:30:26Z, đọc qua REST lúc 15:30:43Z.
Thân comment có sha256 `4a2dba07da0b23f5542a60cb528950736b25df07dfa1534d2d1c994f283684d0` và
chứa 0 dấu chéo ngược (đo lại lúc soạn r2 trên bản đọc lại có trong tay: khớp cả hai). Comment do
**phiên agent đăng hộ chủ kho**, là bản chiếu các câu trả lời trắc nghiệm của chủ kho trong phiên;
tư cách của nó là lời khai có neo (#566). Chủ kho trả lời làm hai lượt, lúc **15:28:25Z** và
**15:30:09Z**. Mọi nhãn trong bảng dưới chép nguyên văn từ comment ấy. Các quyết định này được
đưa ra cho r1; r2 giữ nguyên chúng, trừ các điểm ở §11.1.

| lượt | câu hỏi | nhãn chủ kho **chọn** | nhãn **không chọn** | trả lời Q |
|---|---|---|---|---|
| 1 (15:28:25Z) | Phạm vi | "Không, chỉ F49+F50 (Recommended)" | "Có, gộp cả F48" | Q1 |
| 1 (15:28:25Z) | Review | "0/0/0, subagent (Recommended)" | "0/0/0, phiên độc lập" · "0 P1/P2, P3 thành nợ" | Q5 (ngưỡng), Q6 |
| 1 (15:28:25Z) | Nền và CI | "fc852ff, CI 1 lần khi sạch (Recommended)" | "423b4ba, CI 1 lần khi sạch" · "fc852ff, thêm 1 lượt Windows" | Q7, Q8, Q11 |
| 2 (15:30:09Z) | Gói Q còn lại | "Chấp nhận, trừ Q5: lặp tới 0/0/0" | "Chấp nhận cả gói (Recommended)" · "Chấp nhận, trừ Q14: cho HINT" | Q2, Q3, Q4, Q5 (trần), Q9, Q10, Q12, Q13, Q14 |

Hệ quả, theo từng câu hỏi:

- **Q1 — Lớp A (F48 / đường (e)):** không gộp. Ghi nợ `registry-nang-luc-ngoai-cua-so`; muốn
  đóng thì mở packet riêng. Áp tại: header `objective`, §1.2, §2, §4, `land_obligations`.
- **Q2 — `_so_tien_trinh_ban_kinh`:** ghi nợ `so-tien-trinh-nhan-fullwidth`. Áp tại: §1.7, §2,
  §4, A4-d, `land_obligations`.
- **Q3 — Phần mở rộng (TAB, `>=2`, `len(CA)-1`, `hong`, `tien_kiem`):** giữ. Áp tại: M1, M3, §2.
  Nhãn "F49+F50" ở Q1 vì vậy bao gồm các phần mở rộng này.
- **Q4 — Miền M3:** quét trọn trục `0…len(CA)`. Áp tại: M3, A3. r2 giữ và **thêm** tích biên
  (§11.1).
- **Q5 — Ngưỡng và trần review:** lặp tới 0 P1 · 0 P2 · 0 P3, không giới hạn số vòng. Chữ
  "không giới hạn 2 vòng" trong comment `5914438647` dẫn con số trục VÒNG của ADR-0043, con số
  mà ADR-0048 đã thay từ 2026-09-12; ý quyết định (lặp tới 0/0/0, không trần) không đổi. Vượt trần
  trục VÒNG của ADR-0048 là có chủ đích và được ghi bằng khối `nang_tran`. Áp tại: header, khối
  `nang_tran`, A6, S6.
- **Q6 — Đường chạy reviewer:** Sonnet 5.5 chạy subagent ⇒ mức đạt được là `review_deferred`;
  land bằng `human_audited`. Áp tại: header (reviewer, assurance), A6, `land_obligations`.
- **Q7 — CI:** không chạy CI trong vòng lặp; mở PR (CI chạy một lần) khi review sạch. Áp tại:
  `required_checks`, §4, §7, S10.
- **Q8 — Windows:** không chạy. Ghi nợ `windows-chua-do-o-moi-wp698`. Áp tại: `environment`,
  `required_checks` (e), §4, §7, §10.
- **Q9 — `gate-registry` hết trần trên PR #698:** nguyên văn *"nếu `gate-registry` hết trần trên
  PR #698 thì coi các context bắt buộc xanh là đủ, kèm nợ có neo"*. r2 đọc: (c) được coi là đạt
  khi (a) và (b) xanh; nợ có neo `gate-registry-het-tran-wp698`; chỉ áp cho các run của PR #698;
  **không** miễn (d). Áp tại: `required_checks` (c), S7.
- **Q10 — Thẩm quyền closure:** chủ kho xác nhận bằng một comment trên #698 neo `spec_hash`;
  lease chỉ cấp sau comment ấy. Với r2: comment phải neo `spec_hash` **của r2**. Áp tại: đoạn
  closure, công thức băm, `depends_on` (4), S2, §11.1.
- **Q11 — Nền nghiệm thu:** `fc852fff7da37f1669569572b79571446e61c294`. Áp tại: header, §1, A1,
  A4. Đo lại lúc 15:31:57Z: blob `ops/cong_cu_test.py` trùng với `423b4ba`; đo lại lúc soạn r2:
  `origin/master` là `fc852ff` lúc 22:24Z 30-09 và `20ec8d5` lúc 03:09Z 01-10. Giữa hai mốc có hai
  merge commit trên chuỗi cha thứ nhất (PR #692, PR #689); tính cả các commit được merge thì
  `git rev-list --count fc852ff..20ec8d5` = 22. `git log fc852ff..20ec8d5 -- ops/cong_cu_test.py` rỗng
  và blob ở `20ec8d5` trùng nền, nên nền không dời (header). Thêm `--full-history` thì lệnh ấy liệt kê
  hai commit `merge origin/master vào nhánh` (`7c106a5`, `8e630c0`): mỗi commit đổi tệp so với cha
  phía nhánh (blob cũ `a2010821…`) về đúng blob nền `9edea6b1…`, và không đổi gì so với cha phía master.
- **Q12 — Trần kích thước:** ≤ 3 tệp và ≤ 300 dòng thêm. Áp tại: S5.
- **Q13 — Hồ sơ lượt 22:** đưa vào một nhánh `ops/**` kèm băm; việc này không chặn packet. Áp
  tại: §4, `land_obligations` 8.
- **Q14 — Patch-as-hint:** không dùng; reviewer chỉ mô tả hướng. Áp tại: header (reviewer), §4.
  Review lượt 1 gửi kèm `HINT.patch` **chỉ sửa văn bản đặc tả** (reviewer tự khai lý do và đề
  nghị bỏ nếu chủ kho đọc Q14 là cấm cả văn bản); r2 áp nó rồi sửa tiếp (§0-r2). Review lượt 2 cũng gửi một
  `HINT.patch` chỉ sửa văn bản; r3 áp nó rồi sửa tiếp (§0-r3). Review lượt 3 cũng vậy; r4 áp nó rồi sửa tiếp (§0).
  Không có mã `ops/cong_cu_test.py` nào đi từ reviewer vào đặc tả; reviewer lượt 3 không giao mã dựng ứng viên (Q14).
  28 dò `y_*` của nó (trong `evidence/`) được chạy đối chiếu (§1.10.8); Phụ lục J là dò do phiên soạn r4 tự viết.

Ba quyết định khác khuyến nghị trong bản nháp của r1:

- Q5: bản nháp đề 2 vòng (con số trục VÒNG của ADR-0043, đã bị ADR-0048 thay); chủ kho chọn lặp
  tới 0/0/0.
- Q6: bản nháp đề phiên độc lập; chủ kho chọn subagent.
- Q8: bản nháp đề một lượt Windows; chủ kho chọn không.

Nhãn "(Recommended)" trong bảng trên là của câu hỏi phiên điều phối trình cho chủ kho, không phải
khuyến nghị trong bản nháp.

### 11.1 Điều r2, r3 và r4 tự quyết — chỉ có hiệu lực khi comment Q10 xác nhận closure của r4

Chủ kho chưa trả lời câu hỏi nào về r2, r3 hay r4. Phần (A) là tám điểm r2 tự quyết theo verdict lượt 1 (điểm 4 và 8
được r3 cập nhật số); phần (B) liệt kê cách đặc tả đọc **từng** câu Q1–Q14 của comment `5914438647`; phần (C) là
điểm r3 tự quyết theo verdict lượt 2 (điểm 12 và 16 được r4 thay hoặc giữ, ghi ngay tại điểm); phần (D) là điểm r4 tự
quyết theo verdict lượt 3. Comment xác nhận closure của r4 (Q10) là chỗ chủ kho chấp nhận hay bác từng điểm. Bác một
điểm ⇒ revision mới, không sửa r4.

**(A) Điểm r2 tự quyết.**

1. **Mở rộng mục tiêu trong phạm vi Q1/Q3.** r2 đọc "F49" (Q1) là *khe đo của các phép chuẩn hoá
   đầu vào trong bộ đọc chế độ và nguồn HEAD*, nên nó gồm `ra` (bộ đọc thứ tư của `_doc_che_do`),
   mọi vị trí, mọi thành viên, và các họ ký tự r1 khai "KHÔNG ĐO" (Zs ngoài ASCII, Cc ngoài TAB, dấu
   kết hợp) mà §1.8 đo thấy sống. Phần "kiểu ngoại lệ" của F46 vào M5 theo cùng lý lẽ Q3 đã dùng
   để gộp TAB của F46 vào lớp B. Bác ⇒ r3 đưa phần bị bác về nợ có tên.
2. **Đổi cách làm lớp B sang miền dẫn xuất** (M1) và tiêu chí sang tập dò đóng (A1/A2/A8). Đây
   là "xem lại cách làm tại checkpoint" mà protocol §12 đòi cho lớp `doc-che-do-van-tay` (§9).
3. **M3 thêm tích biên** (48 kịch bản), trên nền Q4.
4. **43 canh `DOT_BIEN`** (16 của r1 + 27 mới), tổng 459 đột biến. r3 nâng thành 54 canh, 470 đột biến (điểm 16).
5. **Hai bộ đọc ngoài lớp B** — đầu tệp mảnh của `_gom_manh` và `CONG_CU_TEST_TIEN_TRINH` — được
   đo (§1.8.6) và để ngoài mục tiêu: nợ mới `gom-dau-manh-chuan-hoa-wp698`; phần mức đo của
   `CONG_CU_TEST_TIEN_TRINH` gộp vào nợ `so-tien-trinh-nhan-fullwidth` (Q2) đã có.
6. **Q9 không miễn (d)** — cách đọc nguyên văn ở trên. Chủ kho muốn miễn (d) thì phải nói riêng.
7. **Chủ thể của `land_obligations` 8** là người chủ kho chỉ định.
8. **Ước kích thước** của mục tiêu mở rộng: xem S5 (r3 cập nhật bằng phép đo trên biến thể của r3). Không nới
   trần Q12.

**(B) Cách đọc từng câu của chủ kho** (nguyên văn trích từ comment `5914438647`; cột "so với chữ" nói cách đọc
rộng hơn, hẹp hơn hay chặt hơn chữ). Bảng phủ đủ 14 câu; câu nào đặc tả đọc đúng như chữ cũng có dòng.

| Q | chữ chủ kho | đặc tả đọc thành | so với chữ | áp tại |
|---|---|---|---|---|
| Q1 | "Không, chỉ F49+F50" | F49 = khe đo của phép chuẩn hoá trong bộ đọc chế độ (`bk`, `mh`, `ra`) và nguồn HEAD: gồm `ra` (F49-P3), mọi vị trí × mọi thành viên, Zs/Cc/Mn, phần "kiểu ngoại lệ" của F46 (M5), — r3 — mọi tầng hạ nguồn của `ra` (M2b) cùng `head` nhiều thẻ (M1b), và — r4 — luật ngoại lệ thành dữ liệu ở mọi chỗ gọi của ô mới (M6) | rộng hơn chữ, trong cùng bản chất F49 | `objective`, M1, M1b, M2b, M5 |
| Q2 | "fullwidth trong `_so_tien_trinh_ban_kinh` ghi thành nợ" | nợ `so-tien-trinh-nhan-fullwidth` gồm cả khe mức đo Cf/TAB (`t_cf`, `t_tab`) | rộng hơn (thêm vào nợ, không vào mục tiêu) | §4, `land_obligations` 7 |
| Q3 | "giữ các phần mở rộng (TAB, `>=2`, `len(CA)-1`, `hong`, `tien_kiem`)" | danh sách trong ngoặc là các phần đã chấp nhận, **không** coi là danh sách đóng; M5/M5b và các họ ký tự Zs/Cc/Mn được thêm theo cùng lý lẽ | vượt chữ nếu đọc ngoặc là danh sách đóng (verdict lượt 2, hướng 4) | M1, M5 |
| Q4 | "quét trọn miền `0…len(CA)`" | trục `0…len(CA)` quét trọn, cộng 48 kịch bản tích biên; **không** quét tích đầy đủ 6.612 kịch bản | hẹp hơn nếu "miền" là tích; hậu quả đo được: `x_f50_tk_and_bq_ne3`, `x_f50_h_and_bq_ne3` SỐNG, khai ở tập KHAI (§6) | M3, A3 |
| Q5 | "lặp tới 0/0/0, không giới hạn 2 vòng. Vượt trần ADR-0043 là có chủ đích và ghi khối `nang_tran`" | ý giữ nguyên; con số "2" và "ADR-0043" là của trục VÒNG cũ, đã bị ADR-0048 thay; `tran_cu` ghi theo ADR-0048 | đọc lại con số, không đổi ý | header, khối `nang_tran` |
| Q6 | "0/0/0, subagent (Recommended)" | reviewer Sonnet 5.5 chạy subagent ⇒ `review_deferred`; land bằng `human_audited` | bằng chữ | A6, assurance |
| Q7 | "fc852ff, CI 1 lần khi sạch" | hạn mức 1 lượt `ci.yml` cho PR THI CÔNG; lượt của PR bookkeeping và của lần merge vào master là chi ngoài packet | đọc phạm vi sổ chi | §7 |
| Q8 | "Không chạy Windows" | không lượt Windows; ô mới (kể cả ô bộ ghi của r3) chưa đo trên Windows ⇒ nợ | bằng chữ | `environment`, §4, §10 |
| Q9 | "nếu `gate-registry` hết trần trên PR #698 thì coi các context bắt buộc xanh là đủ, kèm nợ có neo" | chỉ miễn (c); (b) tám mảnh và (d) `thu-hoi` vẫn là điều kiện, dù `thu-hoi` chưa là required check (`SO_THU_HOI_KICH_HOAT = False`); `thu-hoi` đỏ ⇒ DỪNG, hỏi chủ kho | chặt hơn chữ | `required_checks`, S7 |
| Q10 | "chủ kho xác nhận closure bằng một comment neo `spec_hash`" (nói cho r1) | áp cho mọi revision: comment phải neo `spec_hash` của chính revision được cấp lease (nay là r4); các điểm (A), (C) và (D) của mục này chỉ có hiệu lực qua comment ấy | rộng hơn về thời gian (r1 ⇒ mọi revision) | closure, công thức băm, S2 |
| Q11 | "Nền nghiệm thu là `fc852ff`" | nền nghiệm thu bất biến; nền tiếp nối = `origin/master` lúc cấp lease, khai riêng; nếu nền tiếp nối đổi `ops/cong_cu_test.py` thì dời nền bằng revision mới | thêm khái niệm nền tiếp nối | header, S3 |
| Q12 | "trần ≤ 3 tệp và ≤ 300 dòng thêm" | "dòng thêm" = cột thêm của `git diff --numstat fc852ff -- ops/cong_cu_test.py`, không trừ dòng xoá | đọc đơn vị đo | S5 |
| Q13 | "đưa hồ sơ lượt 22 vào một nhánh `ops/**`; việc này không chặn r1" | không chặn packet hay land, ở mọi revision | rộng hơn ("r1" ⇒ packet) | `land_obligations` 8 |
| Q14 | "không dùng patch-as-hint, reviewer chỉ mô tả hướng sửa" | cấm patch chứa MÃ `ops/cong_cu_test.py`; `HINT.patch` chỉ sửa văn bản đặc tả thì được áp (r2 áp HINT lượt 1, r3 áp HINT lượt 2, r4 áp HINT lượt 3) | hẹp hơn nếu Q14 cấm cả văn bản | §0, §0-r2, §0-r3, §4 |

**(C) Điểm r3 tự quyết theo verdict lượt 2.**

9. **M5b — miền kiểu ngoại lệ là bao đóng bắc cầu của `BaseException.__subclasses__()`** (§5 M5), rộng hơn miền
   "lớp con của `Exception` trong `builtins`" mà HINT lượt 2 đề nghị; lý do đo ở §1.9.3.
10. **M1b — tập ký tự tách là `str.isspace` cộng CR LF** (30 chuỗi), rộng hơn tập `str.splitlines` của HINT; lý do
    đo ở §1.9.4.
11. **M2b — ô cho mọi tầng hạ nguồn của `ra`**: tầng `main` (cả hai chế độ, cả hai lời gọi bộ ghi) và tầng bộ ghi
    với ô ghi tệp THẬT phủ `D698`; lý do đo ở §1.9.5. Ô bộ ghi làm `t52` chậm thêm (§7).
12. **A4-g — tiêu chí chi phí**: đếm tất định (lời gọi `_van_tay` băm tệp > 4 KiB không quá 2 × nền) cộng đồng hồ
    (min ba vòng, xen kẽ nền và ứng viên; Δ = tổng qua `t52`, `t53`, `t54` của chênh min không quá 10 s). Ngưỡng do r3
    chọn, suy từ trần 30 phút theo mô hình tỷ lệ §7, thay cho hai ngưỡng riêng lẻ mà HINT lượt 2 đề nghị (§0-r3 điểm 5);
    đo: `v3_all` Δ = 7,04 s, `cand` 4,94 s (§1.9.9). **r4 thay điểm này bằng điểm 21** (phép đồng hồ không còn làm đỏ).
13. **A1-b2 — định nghĩa nhóm bậc hai** chốt trong đặc tả (§6 A1), là định nghĩa mà bảng §1.8.7 của r2 đã dùng
    mà không ghi ra (đo lại ở §1.9.8).
14. **Tập dò đóng mở rộng** thêm Phụ lục H (145 dò; tổng 366) và tập **KHAI** năm dò khai SỐNG nêu đích danh (§6);
    Phụ lục D đổi hàm `tap` cho tên mới; Phụ lục F, G, I mới.
15. **Nợ mới `doc-argv-chua-co-o-wp698`** cho hai bộ đọc `argv` (thư mục `--gop`, cửa ở `argv[1]`) mà r2 chưa liệt
    kê: đo, để ngoài mục tiêu (§1.9.6).
16. **Thêm 11 canh `DOT_BIEN`** (tổng 54 canh, 470 đột biến; §5). r4 giữ nguyên số ấy (điểm 22).

**(D) Điểm r4 tự quyết theo verdict lượt 3.**

17. **M6 — luật "ngoại lệ do mã bị đo ném là dữ liệu" ở cả bốn chỗ gọi của ô mới** (`doc` của T1, phép quét `head`, vòng
    kịch bản quanh `main`, hai lần gọi bộ ghi), bắt **mọi `BaseException`** (§5 M6). Rộng hơn `HINT.patch` lượt 3, vốn chỉ
    nói ô bộ ghi và "mọi ngoại lệ"; và đổi một câu của r2 ở M1 ("ngoại lệ không phải `ValueError` … là `tin_dung_gia`").
    Lý do đo ở §1.10.3.
18. **T5 — gọi bộ ghi hai lần và so dòng in** (§5 M2b), thay cho phương án để ngỏ "ô tệp cũ tại `tep` … hoặc ghi vào §10"
    của `HINT.patch` lượt 3. Lý do đo ở §1.10.4.
19. **Phụ lục J — 35 dò `x4_*`** (J-NEM 10, J-T5 10, J-TV 15), tập đóng thành 401 dò; Phụ lục D không đổi. J-TV là phần
    "thêm vào T-C các dò thành viên" mà `HINT.patch` lượt 3 nêu bằng lời, không đính dò.
20. **A5 — phép đếm mỏ neo trên MỌI mục `DOT_BIEN`** (Phụ lục F bản r4), rộng hơn "(vii) cho 54 mục" của `HINT.patch`
    lượt 3; mục cũ có tệp đích khác `ops/cong_cu_test.py` so với số lần trên nền. Lý do đo ở §1.10.2.
21. **A4-g — tiêu chí CPU thay đồng hồ**, đo theo **tỷ lệ** với thước của chính máy: r = (C56 + Δ_CPU)/C56 ≤ 1,35, với
    Δ_CPU của ba ca và C56 = CPU một lượt trọn mọi ca trên nền, cùng lệnh, `getrusage` SELF + CHILDREN; đồng hồ chỉ còn là
    chỉ báo. Mô hình §7 dùng job dài nhất đọc lại từ run CI (18,23 phút), tỷ lệ lực lượng của **mảnh lớn nhất** (59/52) và
    cơ sở CPU đo bằng một mảnh A5 thật. Thay điểm 12. Lý do đo ở §1.10.5.
22. **Không thêm canh** cho các đường của r4: tổng giữ 54 canh, 470 đột biến; nợ `j-chua-co-canh-wp698` (§10).
23. **Ước kích thước** cập nhật bằng biến thể đo `v4_all` (S5); cách đọc Q12 và trần 300 dòng không đổi.

Bảng (B) phủ đủ 14 câu Q; mọi điểm tự quyết khác của r2, r3 và r4 nằm ở (A), (C) và (D). Reviewer tìm ra một cách đọc hay
một điểm tự quyết ngoài danh sách thì đó là finding.

---

## Phụ lục A — `do_dot_bien.py` (nguyên văn, sha256 `3d53b90d16e5fcfb138cff9a1c89a674027d84bca339abcb3e992921532d3d53`)

Cách dùng: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python3 do_dot_bien.py <gốc bản sao>
<ra.jsonl> nen`; thay `nen` bằng `liet_ke` để in tên các dò, hoặc bằng một danh sách `<tên dò>…`
để chạy chúng. Lượt ở §1.6 chia đầu ra của `liet_ke` thành 4 nhóm theo chỉ số mod 4, rồi chạy
song song.

```python
"""Đo đột biến dò (probe) cho F48/F49/F50 trên bản sao của nền nghiệm thu, bằng CHÍNH `_do_ban_kinh` +
`_ket_luan_ban_kinh` của `ops/cong_cu_test.py` (không có đường phân hạng thứ hai).

Dùng: PYTHONDONTWRITEBYTECODE=1 python do_dot_bien.py <gốc bản sao> <tệp ra jsonl> nen|<tên>...
Không ghi gì vào bản sao: mỗi đột biến dựng cây tạm riêng (`_dung_cay_dot_bien`).
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

goc, ra_tep, cac = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
spec = importlib.util.spec_from_file_location("cct_probe", goc / "ops" / "cong_cu_test.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

T52, T53, T54 = m._CA_668["t52_"], m._CA_668["t53_"], m._CA_668["t54_"]
NL = chr(10)
L = ("_TEN_NANG_LUC = frozenset(t for t in DOT_BIEN.keys() | _TRUOC_NANG_LUC.keys() "
     "if DOT_BIEN.get(t) != _TRUOC_NANG_LUC.get(t))" + NL)
DK = "if _CO_SYMLINK:" + NL
F24 = 'DOT_BIEN["f24_nhan_symlink"]'
DOC = ("    import re" + NL + "    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)" + NL)
HEAD = '        head = p.stdout.strip() if p.returncode == 0 else ""' + NL
RA = '    return "manh", (k, n, ra)' + NL
NEN = "        if hong or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh("


def cf(x):
    return f'None if {x} is None else "".join(c for c in {x} if unicodedata.category(c) != "Cf")'


P = {
    # ---- F48: registry năng lực — trong cửa sổ (đối chứng) vs sau cửa sổ (các hình dạng F48)
    "c48_trong_cua_so": (L, DK + f'    DOT_BIEN["f48_trong"] = {F24}' + NL + L, T52),
    "e48_sau_cua_so": (L, L + DK + f'    DOT_BIEN["f48_sau"] = {F24}' + NL, T52),
    "e48_get_self": (L, L + DK + f'    DOT_BIEN.get.__self__["f48_self"] = {F24}' + NL, T52),
    "e48_keys_self_pop": (L, L + DK + '    DOT_BIEN.keys.__self__.pop("f24_nhan_symlink")' + NL, T52),
    "e48_globals": (L, L + DK + f'    globals()["DOT_BIEN"]["f48_glob"] = {F24}' + NL, T52),
    "e48_ham_trong_goi_sau": (L, "def _f48_dk():" + NL + f'    DOT_BIEN["f48_ham"] = {F24}' + NL + L
                              + DK + "    _f48_dk()" + NL, T52),
    "e48_trystar": (L, L + "try:" + NL + "    " + DK + f'        DOT_BIEN["f48_ts"] = {F24}' + NL
                    + "except* KeyError:" + NL + "    pass" + NL, T52),
    "e48_gan_lai_moc": (L, DK + f'    DOT_BIEN["f48_an"] = {F24}' + NL + L
                        + '_TEN_NANG_LUC = _TEN_NANG_LUC - {"f48_an"}' + NL, T52),
    # ---- F49: chuẩn hoá đầu vào chế độ / nguồn HEAD / đường ra
    "e49_nfkc_mh": (DOC, DOC + "    import unicodedata" + NL
                    + '    mh = None if mh is None else unicodedata.normalize("NFKC", mh)' + NL, T53),
    "e49_nfkc_bk": (DOC, DOC + "    import unicodedata" + NL
                    + '    bk = None if bk is None else unicodedata.normalize("NFKC", bk)' + NL, T53),
    "e49_cf_mh": (DOC, DOC + "    import unicodedata" + NL + "    mh = " + cf("mh") + NL, T53),
    "e49_cf_bk": (DOC, DOC + "    import unicodedata" + NL + "    bk = " + cf("bk") + NL, T53),
    "e49_nfkc_head": (HEAD, "        import unicodedata" + NL
                      + '        head = unicodedata.normalize("NFKC", p.stdout).strip() if p.returncode == 0 else ""' + NL, T53),
    "e49_cf_head": (HEAD, "        import unicodedata" + NL
                    + '        head = "".join(c for c in p.stdout if unicodedata.category(c) != "Cf").strip() '
                    + 'if p.returncode == 0 else ""' + NL, T53),
    "e49_ra_normpath": (RA, '    return "manh", (k, n, os.path.normpath(ra))' + NL, T53),
    "e49_ra_expanduser": (RA, '    return "manh", (k, n, os.path.expanduser(ra))' + NL, T53),
    "c49_strip_mh": (DOC, DOC + "    mh = None if mh is None else mh.strip()" + NL, T53),
    "c49_lower_head": (HEAD, '        head = p.stdout.strip().lower() if p.returncode == 0 else ""' + NL, T53),
    # ---- F50: lực lượng `bo_qua` ở nhánh mảnh
    "e50_bang_2": (NEN, "        if hong or tien_kiem_bo_qua or len(bo_qua) == 2:" + NL + "            _ket_thuc_manh(", T54),
    "e50_tu_2": (NEN, "        if hong or tien_kiem_bo_qua or len(bo_qua) >= 2:" + NL + "            _ket_thuc_manh(", T54),
    "c50_bang_1": (NEN, "        if hong or tien_kiem_bo_qua or len(bo_qua) == 1:" + NL + "            _ket_thuc_manh(", T54),
    # ---- ngoài F48–F50: lớp TAB mà verdict lượt 22 ghi ĐÃ ĐÓNG trên 8d7faef (F46) — nền có ô chưa?
    "x46_tab_mh": (DOC, DOC + '    mh = None if mh is None else mh.replace(chr(9), "")' + NL, T53),
    "x46_tab_bk": (DOC, DOC + '    bk = None if bk is None else bk.replace(chr(9), "")' + NL, T53),
    "x46_tab_head": (HEAD, '        head = p.stdout.replace(chr(9), "").strip() if p.returncode == 0 else ""' + NL, T53),
    # ---- cùng lớp, verdict không nêu: lực lượng `hong` / `tien_kiem_bo_qua` ở nhánh mảnh; đăng ký TRƯỚC ảnh
    "x47_hong_bang_1": (NEN, "        if len(hong) == 1 or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh(", T54),
    "x47_tk_bang_1": (NEN, "        if hong or len(tien_kiem_bo_qua) == 1:" + NL + "            _ket_thuc_manh(", T54),
    "x50_bang_n_tru_1": (NEN, "        if hong or tien_kiem_bo_qua or len(bo_qua) == len(CA) - 1:" + NL
                         + "            _ket_thuc_manh(", T54),
    "c49_ra_strip": (RA, '    return "manh", (k, n, ra.strip())' + NL, T53),
    "c49_ra_abspath": (RA, '    return "manh", (k, n, os.path.abspath(ra))' + NL, T53),
    "e48_truoc_anh": ("_TRUOC_NANG_LUC = dict(DOT_BIEN)", "if _do_co_symlink():" + NL
                      + '    DOT_BIEN["f48_truoc"] = DOT_BIEN["t1_rc_gop"]' + NL + "_TRUOC_NANG_LUC = dict(DOT_BIEN)", T52),
}


def ghi(x):
    with ra_tep.open("a", encoding="utf-8") as f:
        f.write(json.dumps(x, ensure_ascii=True) + NL)
        f.flush()


if cac == ["liet_ke"]:
    print(" ".join(P))
    sys.exit(0)
if cac == ["nen"]:
    t0 = time.time()
    ket = {fn.__name__: m._chay_1_ca(fn) for fn in m.CA}
    ghi({"ten": "nen", "co_symlink": m._CO_SYMLINK, "so_ca": len(m.CA), "so_dot_bien": len(m.DOT_BIEN),
         "khong_qua": {t: v for t, v in ket.items() if v[0] != "qua"}, "giay": round(time.time() - t0, 1)})
    sys.exit(0)
do_o_nen = json.loads(Path(ra_tep.parent / "do_o_nen.json").read_text()) if (ra_tep.parent / "do_o_nen.json").exists() else []
for ten in cac:
    tim, thay, dich = P[ten]
    nguon = (goc / "ops" / "cong_cu_test.py").read_text(encoding="utf-8")
    so_neo = nguon.count(tim)
    m.DOT_BIEN[ten] = ("ops/cong_cu_test.py", tim, thay, "TEP_TEST", m._KEM_TEP_TEST, dich)
    t0 = time.time()
    try:
        ket, ca_dich = m._do_ban_kinh(ten, bo_qua_ca=do_o_nen)
        dong, loi = m._ket_luan_ban_kinh(ten, ca_dich, ket, len(m.CA), do_o_nen)
        ghi({"ten": ten, "so_neo": so_neo, "dich": ca_dich[:4], "dich_tt": ket.get(ca_dich, ["?"])[0],
             "khong_qua": {t[:4]: v[0] for t, v in ket.items() if v[0] != "qua"},
             "loi": loi, "dong_dau": dong[0][:200], "giay": round(time.time() - t0, 1)})
    except AssertionError as ex:
        ghi({"ten": ten, "so_neo": so_neo, "LOI_DUNG": str(ex)[:300]})
    finally:
        m.DOT_BIEN.pop(ten, None)
```

## Phụ lục B — `do_f49_ma.py` (nguyên văn, sha256 `6707002f3c37cfdfa5cbdf308be288dd9fb40472d8dc855d7cf52c12b2ff0473`)

Cách dùng: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python3 do_f49_ma.py <gốc bản sao>`.

```python
"""Đo mức MÃ (không đột biến) cho F49 trên bản sao của nền nghiệm thu.

Dùng: PYTHONDONTWRITEBYTECODE=1 python do_f49_ma.py <gốc bản sao>
Mọi ký tự ngoài ASCII dựng bằng chr() để không có chuỗi thoát nguyên văn đi qua lớp vận chuyển.
"""
import importlib.util
import json
import os
import sys
import types
import unicodedata
from pathlib import Path

goc = Path(sys.argv[1])
spec = importlib.util.spec_from_file_location("cct_probe", goc / "ops" / "cong_cu_test.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

FW = lambda s: "".join(chr(ord(c) - 0x21 + 0xFF01) if "!" <= c <= "~" else c for s_ in [s] for c in s_)
ZWSP, ZWJ, BOM, WJ, SHY, LRM = chr(0x200B), chr(0x200D), chr(0xFEFF), chr(0x2060), chr(0x00AD), chr(0x200E)
B, M, R = m._BIEN_BAN_KINH, m._BIEN_MANH, m._BIEN_MANH_RA


def doc(env):
    try:
        return list(m._doc_che_do(env))
    except ValueError as ex:
        return ["loi", str(ex).split("]")[0] + "]"]
    except Exception as ex:  # noqa: BLE001
        return ["NEM", type(ex).__name__]


ket = {}
# (1) _doc_che_do — fullwidth / NFKC-tương-thích / Cf
o = {
    "bk_fullwidth": {B: FW("manh")},
    "bk_zwsp_cuoi": {B: "manh" + ZWSP},
    "bk_bom_dau": {B: BOM + "manh"},
    "bk_wj_giua": {B: "ma" + WJ + "nh"},
    "bk_shy_giua": {B: "ma" + SHY + "nh"},
    "mh_fullwidth_so": {M: FW("3") + "/" + FW("8"), R: "x"},
    "mh_fullwidth_gach": {M: "3" + FW("/") + "8", R: "x"},
    "mh_fullwidth_tron": {M: FW("3/8"), R: "x"},
    "mh_so_mu": {M: "3/" + chr(0x2078), R: "x"},          # superscript 8, NFKC -> '8'
    "mh_zwsp_cuoi": {M: "3/8" + ZWSP, R: "x"},
    "mh_zwj_giua": {M: "3" + ZWJ + "/8", R: "x"},
    "mh_lrm_dau": {M: LRM + "3/8", R: "x"},
    "ra_normpath": {M: "3/8", R: "a/./b//c"},
    "ra_expanduser": {M: "3/8", R: "~/x"},
    "ra_dotdot": {M: "3/8", R: "a/../b"},
}
ket["doc_che_do"] = {k: doc(v) for k, v in o.items()}
# NFKC của các giá trị trên (để biết đột biến NFKC sẽ đổi gì)
ket["nfkc"] = {k: {x: unicodedata.normalize("NFKC", y) == y for x, y in v.items()} for k, v in o.items()}

# (2) _van_tay — nguồn HEAD qua subprocess giả (như cửa --tu-kiem-che-do)
hop = ("0123456789abcdef" * 4)[:40]
cu_sp = m.subprocess
bien_head = {
    "hop_le": hop,
    "fullwidth_1": FW(hop[0]) + hop[1:],
    "fullwidth_tron": FW(hop),
    "zwsp_cuoi": hop + ZWSP,
    "bom_dau": BOM + hop,
    "wj_giua": hop[:20] + WJ + hop[20:39],
}
ket["van_tay_head"] = {}
for ten, ra in bien_head.items():
    m.subprocess = types.SimpleNamespace(run=lambda *a, _ra=ra, **kw: types.SimpleNamespace(returncode=0, stdout=_ra),
                                         SubprocessError=cu_sp.SubprocessError)
    try:
        ket["van_tay_head"][ten] = m._van_tay()["head"]
    except Exception as ex:  # noqa: BLE001
        ket["van_tay_head"][ten] = "NEM:" + type(ex).__name__
    finally:
        m.subprocess = cu_sp

# (3) _so_tien_trinh_ban_kinh — CONG_CU_TEST_TIEN_TRINH (ngoài F49 nguyên văn; đo vì cùng họ đọc biến)
ket["so_tien_trinh"] = {}
cu = os.environ.get("CONG_CU_TEST_TIEN_TRINH")
for ten, v in {"ascii_3": "3", "fullwidth_12": FW("12"), "mu_2": chr(0x00B2), "arab_3": chr(0x0663),
               "zwsp": "3" + ZWSP, "rong": "", "khoang": " 3 "}.items():
    os.environ["CONG_CU_TEST_TIEN_TRINH"] = v
    try:
        ket["so_tien_trinh"][ten] = m._so_tien_trinh_ban_kinh()
    except Exception as ex:  # noqa: BLE001
        ket["so_tien_trinh"][ten] = "NEM:" + type(ex).__name__ + ":" + str(ex)[:60]
if cu is None:
    os.environ.pop("CONG_CU_TEST_TIEN_TRINH", None)
else:
    os.environ["CONG_CU_TEST_TIEN_TRINH"] = cu

# (4) oracle độc lập của t53 có đồng ý với mã trên CÙNG các giá trị không (để biết ô mới có cần đổi oracle)
# so SAU vòng JSON như t53 (con in `KQ` JSON, cha so): tuple của `_doc_che_do` thành list — so trần là tạo tác
J = lambda x: json.loads(json.dumps(x))
ket["oracle_che_do_khop"] = {k: J(m._mong_che_do(v)) == J(doc(v)) for k, v in o.items()}
TAB = chr(9)
bien_head["tab_giua"] = hop[:20] + TAB + hop[20:]
ket["oracle_git_khop"] = {}
for ten, ra in bien_head.items():
    m.subprocess = types.SimpleNamespace(run=lambda *a, _ra=ra, **kw: types.SimpleNamespace(returncode=0, stdout=_ra),
                                         SubprocessError=cu_sp.SubprocessError)
    try:
        ket["oracle_git_khop"][ten] = [m._van_tay()["head"] == m._mong_git(0, ra, None), m._mong_git(0, ra, None)]
    finally:
        m.subprocess = cu_sp
o_tab = {"bk_tab_cuoi": {B: "manh" + TAB}, "mh_tab_giua": {M: "3" + TAB + "/8", R: "x"}}
ket["tab_doc_che_do"] = {k: [doc(v), m._mong_che_do(v) == doc(v)] for k, v in o_tab.items()}
print(json.dumps(ket, ensure_ascii=True, indent=1))
```

## Phụ lục C — `do_dot_bien_r2.py` (nguyên văn, sha256 `c6a4db8b47fe246e8e173c13298a62310019809794ea322abcc94e1fdd922a36`)

Tập dò đóng của r2 (221 dò: 209 dò đo từ 22:39:52Z 30-09 cộng 12 dò nhóm ngoài `D698` đo từ 00:53:07Z 01-10, §1.8.4). Cách dùng: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python3 do_dot_bien_r2.py <gốc bản sao>
<ra.jsonl> <tên dò>…`; `liet_ke` in tên, `ho` in tên kèm họ. Lượt ở §1.8 chia tên theo chỉ số mod 4 cho 4 tiến trình
(`run4.sh` của reviewer lượt 1, mỗi nhóm một `TMPDIR`, rồi `wait`). 53 dò đầu chép **từng byte** từ
`do_dot_bien3.py`, `do_dot_bien4.py`, `do_dot_bien5.py` của reviewer (đã kiểm bằng so sánh bảng `P`).

```python
"""Tập dò ĐÓNG của wp698 r2 (Phụ lục C): đo bằng CHÍNH `_do_ban_kinh` + `_ket_luan_ban_kinh` của `ops/cong_cu_test.py`.

Dùng: PYTHONDONTWRITEBYTECODE=1 python do_dot_bien_r2.py <gốc bản sao> <tệp ra jsonl> liet_ke|ho|nen|<tên>...
  liet_ke : in tên mọi dò, theo thứ tự bảng.      ho : in "tên họ" từng dò (một dòng một dò).
Không ghi gì vào bản sao: mỗi đột biến dựng cây tạm riêng (`_dung_cay_dot_bien`). Không có dấu chéo ngược nào
trong tệp này: xuống dòng là chr(10), TAB là chr(9), chéo ngược là chr(92).
"""
import importlib.util
import json
import sys
import time
from pathlib import Path

goc, ra_tep, cac = Path(sys.argv[1]), Path(sys.argv[2]), sys.argv[3:]
spec = importlib.util.spec_from_file_location("cct_probe", goc / "ops" / "cong_cu_test.py")
m = importlib.util.module_from_spec(spec)
spec.loader.exec_module(m)

T52, T53, T54 = m._CA_668["t52_"], m._CA_668["t53_"], m._CA_668["t54_"]
NL, BS = chr(10), chr(92)
# ---- mỏ neo (mỗi chuỗi xuất hiện ĐÚNG một lần trên nền fc852ff; cột `so_neo` của đầu ra đo lại điều đó)
DOC = ("    import re" + NL + "    bk, mh, ra = env.get(_BIEN_BAN_KINH), env.get(_BIEN_MANH), env.get(_BIEN_MANH_RA)" + NL)
HEAD = '        head = p.stdout.strip() if p.returncode == 0 else ""' + NL
RA = '    return "manh", (k, n, ra)' + NL
NEN = "        if hong or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh("
EXC = "    except (OSError, subprocess.SubprocessError):" + NL + '        head = ""' + NL
GOM = '        if dau["sha256_test"] != van_tay["sha256_test"] or dau["head"] != van_tay["head"]:' + NL
TT = "        so = int(tho) if tho.strip().isdigit() and int(tho) >= 1 else 1" + NL
RE = '    m = re.fullmatch(r"(0|[1-9][0-9]?)/([1-9][0-9]?)", mh)' + NL
UN = "    import unicodedata" + NL

# ---- vị từ trên MỘT ký tự `c` (mã nguồn chèn vào đột biến)
CF = 'unicodedata.category(c) == "Cf"'
TAB = "c == chr(9)"
ZW = "ord(c) in (0x200B, 0x200C, 0x200D, 0xFEFF)"
BIDI = "(ord(c) in (0x200E, 0x200F) or 0x202A <= ord(c) <= 0x202E or 0x2066 <= ord(c) <= 0x2069)"
SHY = "ord(c) == 0xAD"
ALM = "ord(c) == 0x61C"
TAG = "0xE0000 <= ord(c) <= 0xE007F"
CFK = f"({CF} and not ({ZW} or {BIDI} or {SHY} or {ALM} or {TAG}))"
FW = "0xFF01 <= ord(c) <= 0xFF5E"
NO = 'unicodedata.category(c) == "No"'
SUPP = "ord(c) >= 0x10000"
NFK = f'(ord(c) < 0x10000 and not {FW} and not {NO})'
ZS = '(unicodedata.category(c) == "Zs" and c != " ")'
CC = '(unicodedata.category(c) == "Cc" and c != chr(9))'
MN = 'unicodedata.category(c) == "Mn"'


# ---- phép biến đổi trên biến `v` (trả BIỂU THỨC)
def bo(p):          # xoá ở MỌI vị trí
    return lambda v: f'"".join(c for c in {v} if not ({p}))'


def nfkc(p):        # NFKC CHỈ trên các ký tự thoả p
    return lambda v: f'"".join(unicodedata.normalize("NFKC", c) if ({p}) else c for c in {v})'


def dau(p):         # chỉ bỏ ở ĐẦU
    return lambda v: f"{v}[next((i for i, c in enumerate({v}) if not ({p})), len({v})):]"


def cuoi(p):        # chỉ bỏ ở CUỐI
    return lambda v: f"{v}[:len({v}) - next((i for i, c in enumerate(reversed({v})) if not ({p})), len({v}))]"


def giua(p):        # chỉ bỏ ở GIỮA (giữ ký tự đầu và cuối)
    return lambda v: f'{v} if len({v}) < 3 else {v}[:1] + "".join(c for c in {v}[1:-1] if not ({p})) + {v}[-1:]'


def tai(i, p):      # chỉ bỏ ở ĐÚNG chỉ số i
    return lambda v: f"({v}[:{i}] + {v}[{i} + 1:]) if len({v}) > {i} and (lambda c: {p})({v}[{i}]) else {v}"


def bodau(v):       # NFD rồi bỏ dấu kết hợp
    return f'"".join(c for c in unicodedata.normalize("NFD", {v}) if unicodedata.category(c) != "Mn")'


# ---- bốn bộ đọc: chỗ chèn phép biến đổi
def bk_(f, dich=T53):
    return (DOC, DOC + UN + f"    bk = None if bk is None else {f('bk')}" + NL, dich)


def mh_(f, dich=T53):
    return (DOC, DOC + UN + f"    mh = None if mh is None else {f('mh')}" + NL, dich)


def ra_(f, dich=T53):
    return (RA, UN + f"    ra = {f('ra')}" + NL + RA, dich)


def head_(f, dich=T53):
    return (HEAD, "        import unicodedata" + NL + "        _s = p.stdout" + NL + f"        _s = {f('_s')}" + NL
            + '        head = _s.strip() if p.returncode == 0 else ""' + NL, dich)


DOC_DOC = {"bk": bk_, "mh": mh_, "ra": ra_, "head": head_}
P, HO = {}, {}


def them(ho, ten, dinh_nghia):
    assert ten not in P, ten
    P[ten], HO[ten] = dinh_nghia, ho


# ======== (1) 47 dò anh em của reviewer lượt 1 (`evidence/do_dot_bien3.py`), NGUYÊN mỏ neo và phép thay
def _cf(x):
    return f'None if {x} is None else "".join(c for c in {x} if unicodedata.category(c) != "Cf")'


NBSP = "chr(0xA0) + chr(0x3000)"
R47 = {
    "s_ra_nfkc": (RA, UN + '    return "manh", (k, n, unicodedata.normalize("NFKC", ra))' + NL, T53),
    "s_ra_cf": (RA, UN + '    return "manh", (k, n, "".join(c for c in ra if unicodedata.category(c) != "Cf"))' + NL, T53),
    "s_ra_tab": (RA, '    return "manh", (k, n, ra.replace(chr(9), ""))' + NL, T53),
    "s_bk_strip": (DOC, DOC + "    bk = None if bk is None else bk.strip()" + NL, T53),
    "s_bk_lower": (DOC, DOC + "    bk = None if bk is None else bk.lower()" + NL, T53),
    "s_mh_nfkd": (DOC, DOC + UN + '    mh = None if mh is None else unicodedata.normalize("NFKD", mh)' + NL, T53),
    "s_mh_digit_d": (RE, '    m = re.fullmatch(r"(0|[1-9]' + BS + 'd?)/([1-9]' + BS + 'd?)", mh)' + NL, T53),
    "s_mh_strip_zs": (DOC, DOC + "    mh = None if mh is None else mh.strip(" + NBSP + ")" + NL, T53),
    "s_bk_strip_zs": (DOC, DOC + "    bk = None if bk is None else bk.strip(" + NBSP + ")" + NL, T53),
    "s_head_strip_set": (HEAD, '        head = p.stdout.strip(" " + chr(10)) if p.returncode == 0 else ""' + NL, T53),
    "s_ra_rstrip_slash": (RA, '    return "manh", (k, n, ra.rstrip("/"))' + NL, T53),
    "s_ra_lstrip_dot": (RA, '    return "manh", (k, n, ra[2:] if ra.startswith("./") else ra)' + NL, T53),
    "s_ra_dslash": (RA, '    return "manh", (k, n, ra.replace("//", "/"))' + NL, T53),
    "s_ra_pathlib": (RA, '    return "manh", (k, n, str(Path(ra)))' + NL, T53),
    "s2_hong_va_khong_bq": (NEN, "        if (hong and not bo_qua) or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh(", T54),
    "s2_hong_gt_bq": (NEN, "        if len(hong) > len(bo_qua) or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh(", T54),
    "s2_tk_va_khong_bq": (NEN, "        if hong or (tien_kiem_bo_qua and not bo_qua):" + NL + "            _ket_thuc_manh(", T54),
    "s2_hong_chan": (NEN, "        if len(hong) % 2 or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh(", T54),
    "s2_hong_lt_n": (NEN, "        if len(hong) < len(CA) or tien_kiem_bo_qua:" + NL + "            _ket_thuc_manh(", T54),
    "s2_bq_bang_n": (NEN, "        if hong or tien_kiem_bo_qua or len(bo_qua) == len(CA):" + NL + "            _ket_thuc_manh(", T54),
    "s2_bq_gt_hong": (NEN, "        if hong or tien_kiem_bo_qua or len(bo_qua) > 2 * len(hong) + 1:" + NL + "            _ket_thuc_manh(", T54),
    "q_cf_lead_bk": (DOC, DOC + UN + '    while bk and unicodedata.category(bk[0]) == "Cf":' + NL + "        bk = bk[1:]" + NL, T53),
    "q_cf_trail_bk": (DOC, DOC + UN + '    while bk and unicodedata.category(bk[-1]) == "Cf":' + NL + "        bk = bk[:-1]" + NL, T53),
    "q_cf_mid_bk": (DOC, DOC + UN + '    bk = bk if bk is None or len(bk) < 3 else bk[:1] + "".join(c for c in bk[1:-1] if unicodedata.category(c) != "Cf") + bk[-1:]' + NL, T53),
    "q_cf_lead_mh": (DOC, DOC + UN + '    while mh and unicodedata.category(mh[0]) == "Cf":' + NL + "        mh = mh[1:]" + NL, T53),
    "q_cf_trail_mh": (DOC, DOC + UN + '    while mh and unicodedata.category(mh[-1]) == "Cf":' + NL + "        mh = mh[:-1]" + NL, T53),
    "q_cf_mid_mh": (DOC, DOC + UN + '    mh = mh if mh is None or len(mh) < 3 else mh[:1] + "".join(c for c in mh[1:-1] if unicodedata.category(c) != "Cf") + mh[-1:]' + NL, T53),
    "q_cf_lead_head": (HEAD, "        import unicodedata" + NL + "        _s = p.stdout" + NL + '        while _s and unicodedata.category(_s[0]) == "Cf":' + NL + "            _s = _s[1:]" + NL + '        head = _s.strip() if p.returncode == 0 else ""' + NL, T53),
    "q_cf_trail_head": (HEAD, "        import unicodedata" + NL + "        _s = p.stdout.rstrip()" + NL + '        while _s and unicodedata.category(_s[-1]) == "Cf":' + NL + "            _s = _s[:-1]" + NL + '        head = _s.strip() if p.returncode == 0 else ""' + NL, T53),
    "q_cf_mid_head": (HEAD, "        import unicodedata" + NL + "        _s = p.stdout.strip()" + NL + '        _s = _s[:1] + "".join(c for c in _s[1:-1] if unicodedata.category(c) != "Cf") + _s[-1:]' + NL + '        head = _s if p.returncode == 0 else ""' + NL, T53),
    "q_tab_lead_bk": (DOC, DOC + "    bk = bk if bk is None else bk.lstrip(chr(9))" + NL, T53),
    "q_tab_trail_bk": (DOC, DOC + "    bk = bk if bk is None else bk.rstrip(chr(9))" + NL, T53),
    "q_tab_mid_bk": (DOC, DOC + '    bk = bk if bk is None or len(bk) < 3 else bk[:1] + bk[1:-1].replace(chr(9), "") + bk[-1:]' + NL, T53),
    "q_tab_lead_mh": (DOC, DOC + "    mh = mh if mh is None else mh.lstrip(chr(9))" + NL, T53),
    "q_tab_trail_mh": (DOC, DOC + "    mh = mh if mh is None else mh.rstrip(chr(9))" + NL, T53),
    "q_tab_mid_mh": (DOC, DOC + '    mh = mh if mh is None or len(mh) < 3 else mh[:1] + mh[1:-1].replace(chr(9), "") + mh[-1:]' + NL, T53),
    "m_cf_zw_bk": (DOC, DOC + "    bk = bk if bk is None else bk.translate({c: None for c in (0x200B, 0x200C, 0x200D, 0xFEFF)})" + NL, T53),
    "m_cf_bidi_bk": (DOC, DOC + "    bk = bk if bk is None else bk.translate({c: None for c in (0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A))})" + NL, T53),
    "m_cf_bidi_mh": (DOC, DOC + "    mh = mh if mh is None else mh.translate({c: None for c in (0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A))})" + NL, T53),
    "m_cf_bidi_head": (HEAD, "        head = p.stdout.translate({c: None for c in (0x200E, 0x200F, *range(0x202A, 0x202F), *range(0x2066, 0x206A))}).strip() if p.returncode == 0 else " + '""' + NL, T53),
    "m_cf_shy_bk": (DOC, DOC + '    bk = bk if bk is None else bk.replace(chr(0xAD), "")' + NL, T53),
    "m_cf_061c_bk": (DOC, DOC + '    bk = bk if bk is None else bk.replace(chr(0x61C), "")' + NL, T53),
    "m_cf_tag_bk": (DOC, DOC + '    bk = bk if bk is None else "".join(c for c in bk if not 0xE0000 <= ord(c) <= 0xE007F)' + NL, T53),
    "m_nfkc_fwonly_mh": (DOC, DOC + "    mh = mh if mh is None else mh.translate({0xFF10 + i: 48 + i for i in range(10)} | {0xFF0F: 47})" + NL, T53),
    "m_nfkc_fwonly_bk": (DOC, DOC + "    bk = bk if bk is None else bk.translate({0xFF41 + i: 97 + i for i in range(26)})" + NL, T53),
    "m_nfkc_super_mh": (DOC, DOC + "    mh = mh if mh is None else mh.translate({0xB9: 49, 0xB2: 50, 0xB3: 51, **{0x2070 + i: 48 + i for i in (0, 4, 5, 6, 7, 8, 9)}})" + NL, T53),
    "m_nfkc_fwonly_head": (HEAD, "        head = p.stdout.translate({0xFF10 + i: 48 + i for i in range(10)} | {0xFF41 + i: 97 + i for i in range(6)}).strip() if p.returncode == 0 else " + '""' + NL, T53),
}
for _t, _d in R47.items():
    them("R47", _t, _d)
# (2) dò kiểu ngoại lệ và Zs của reviewer lượt 1 (`do_dot_bien4.py`, `do_dot_bien5.py`)
for _t, _thay in (("z_exc_all", "Exception"), ("z_exc_oserror_only", "OSError"),
                  ("z_exc_them_valueerror", "(OSError, subprocess.SubprocessError, ValueError)"),
                  ("z_exc_subproc_only", "subprocess.SubprocessError")):
    them("R-exc", _t, (EXC, f"    except {_thay}:" + NL + '        head = ""' + NL, T53))
ZS3 = "{0xA0: None, 0x2003: None, 0x3000: None}"
them("R-zs", "s_bk_drop_zs", (DOC, DOC + "    bk = bk if bk is None else bk.translate(" + ZS3 + ")" + NL, T53))
them("R-zs", "s_mh_drop_zs", (DOC, DOC + "    mh = mh if mh is None else mh.translate(" + ZS3 + ")" + NL, T53))

# ======== (3) r2: VỊ TRÍ — `ra` (Cf, TAB × đầu/cuối/giữa) và `head` (TAB giữa; TAB ở hai đầu head TƯƠNG ĐƯƠNG vì strip())
for _x, _p in (("cf", CF), ("tab", TAB)):
    for _vt, _f in (("lead", dau), ("trail", cuoi), ("mid", giua)):
        them("vi-tri", f"q_{_x}_{_vt}_ra", ra_(_f(_p)))
them("vi-tri", "q_tab_mid_head", head_(giua(TAB)))
# (4) r2: MỌI VỊ TRÍ — bỏ Cf ở ĐÚNG chỉ số i, mọi i của giá trị hợp lệ chuẩn dài nhất cộng một ký tự chèn
for _r, _n in (("bk", 5), ("mh", 6), ("head", 65), ("ra", 4)):
    for _i in range(_n):
        them("moi-vi-tri", f"p_cf_{_r}_{_i}", DOC_DOC[_r](tai(_i, CF)))
# (5) r2: THÀNH VIÊN — tập con của Cf và của NFKC, cho cả bốn bộ đọc (bỏ tên đã có ở (1))
for _x, _p in (("zw", ZW), ("bidi", BIDI), ("shy", SHY), ("061c", ALM), ("tag", TAG), ("khac", CFK)):
    for _r in ("bk", "mh", "head", "ra"):
        if f"m_cf_{_x}_{_r}" not in P:
            them("thanh-vien-cf", f"m_cf_{_x}_{_r}", DOC_DOC[_r](bo(_p)))
them("thanh-vien-nfkc", "m_nfkc_fwonly_ra", ra_(nfkc(FW)))
for _x, _p in (("no", NO), ("ngoai_bmp", SUPP), ("khac_bmp", NFK)):
    for _r in ("bk", "mh", "head", "ra"):
        them("thanh-vien-nfkc", f"m_nfkc_{_x}_{_r}", DOC_DOC[_r](nfkc(_p)))
# (6) r2: họ ký tự khác — Zs ngoài ASCII, Cc ngoài TAB, dấu kết hợp (Mn), bỏ dấu (NFD rồi bỏ Mn)
for _r in ("bk", "mh", "head", "ra"):
    them("zs", f"m_zs_{_r}", DOC_DOC[_r](bo(ZS)))
    them("cc", f"m_cc_{_r}", DOC_DOC[_r](bo(CC)))
    them("mn", f"m_mn_{_r}", DOC_DOC[_r](bo(MN)))
    them("mn", f"m_bodau_{_r}", DOC_DOC[_r](bodau))
# (6b) r2: ba nhóm NGOÀI D698 (Lo, Co, Cn) — xoá cả nhóm; miền M1 có một đại diện mỗi nhóm ở mọi vị trí
for _x in ("Lo", "Co", "Cn"):
    for _r in ("bk", "mh", "head", "ra"):
        them("ngoai-d698", f"m_{_x.lower()}_{_r}", DOC_DOC[_r](bo(f'unicodedata.category(c) == "{_x}"')))
# (7) r2: phép đường dẫn/chuỗi khác trên `ra`
for _t, _bt in (("nfc", 'unicodedata.normalize("NFC", ra)'), ("nfd", 'unicodedata.normalize("NFD", ra)'),
                ("lower", "ra.lower()"), ("casefold", "ra.casefold()"), ("expandvars", "os.path.expandvars(ra)"),
                ("realpath", "os.path.realpath(ra)"), ("bslash", 'ra.replace(chr(92), "/")')):
    them("ra-phep", f"s_ra_{_t}", ra_(lambda v, _bt=_bt: _bt))
# (7b) đối chứng: casefold trên `bk` (ô `MANH` của nền giết nó; dạng fullwidth hoa casefold ra fullwidth thường, vẫn bị từ chối)
them("doi-chung", "s_bk_casefold", bk_(lambda v: f"{v}.casefold()"))
# (8) r2: `head` — strip HẸP (chỉ khoảng trắng ASCII): nền strip() bỏ cả Zs/Cc-khoảng-trắng ngoài ASCII ở hai đầu
them("head-strip", "s_head_strip_ascii", (HEAD, '        head = p.stdout.strip(" " + chr(9) + chr(10) + chr(11) + chr(12) + chr(13)) '
                                         'if p.returncode == 0 else ""' + NL, T53))
# (9) r2: kiểu ngoại lệ `_van_tay` — mở rộng tập bắt
for _t, _thay in (("z_exc_base", "BaseException"),
                  ("z_exc_them_unicode", "(OSError, subprocess.SubprocessError, UnicodeError)"),
                  ("z_exc_them_runtime", "(OSError, subprocess.SubprocessError, RuntimeError)")):
    them("exc", _t, (EXC, f"    except {_thay}:" + NL + '        head = ""' + NL, T53))
# (10) r2: lực lượng — vị từ nhiều biến chỉ lệch nền ở điểm có >= 2 toạ độ khác 0
for _t, _dk in (("s3_hong_khac_bq", "(hong and len(hong) != len(bo_qua)) or tien_kiem_bo_qua"),
                ("s3_xor", "(hong and not tien_kiem_bo_qua) or (tien_kiem_bo_qua and not hong)"),
                ("s3_tk_bq_nho", "hong or (tien_kiem_bo_qua and len(bo_qua) < len(CA))"),
                ("s3_tk_bq_le_hong", "hong or (tien_kiem_bo_qua and len(bo_qua) <= len(hong))"),
                ("s3_hai_tk", "(hong and len(tien_kiem_bo_qua) != 2) or (tien_kiem_bo_qua and not hong)")):
    them("luc-luong", _t, (NEN, f"        if {_dk}:" + NL + "            _ket_thuc_manh(", T54))
# (11) r2: bộ đọc NGOÀI lớp B — đo để khai trạng thái, không vào mục tiêu (đầu tệp mảnh của `_gom_manh`; số tiến trình)
_GH = "_gh(dau['head'])"
for _t, _bt in (("g_nfkc_head", 'unicodedata.normalize("NFKC", x)'), ("g_cf_head", bo(CF)("x")),
                ("g_tab_head", bo(TAB)("x")), ("g_strip_head", "x.strip()")):
    them("ngoai-lop-gom", _t, (GOM, "        import unicodedata" + NL + f"        _gh = lambda x: {_bt} if isinstance(x, str) else x" + NL
                               + '        if dau["sha256_test"] != van_tay["sha256_test"] or ' + _GH + ' != van_tay["head"]:' + NL, T52))
for _t, _bt in (("t_cf", bo(CF)("tho")), ("t_tab", bo(TAB)("tho"))):
    them("ngoai-lop-tien-trinh", _t, (TT, "        import unicodedata" + NL + f"        tho = {_bt}" + NL + TT, T54))


def ghi(x):
    with ra_tep.open("a", encoding="utf-8") as f:
        f.write(json.dumps(x, ensure_ascii=True) + NL)
        f.flush()


if cac == ["liet_ke"]:
    print(" ".join(P))
    sys.exit(0)
if cac == ["ho"]:
    print(NL.join(f"{t} {HO[t]}" for t in P))
    sys.exit(0)
if cac == ["nen"]:
    t0 = time.time()
    ket = {fn.__name__: m._chay_1_ca(fn) for fn in m.CA}
    ghi({"ten": "nen", "co_symlink": m._CO_SYMLINK, "so_ca": len(m.CA), "so_dot_bien": len(m.DOT_BIEN),
         "khong_qua": {t: v for t, v in ket.items() if v[0] != "qua"}, "giay": round(time.time() - t0, 1)})
    sys.exit(0)
do_o_nen = json.loads(Path(ra_tep.parent / "do_o_nen.json").read_text()) if (ra_tep.parent / "do_o_nen.json").exists() else []
for ten in cac:
    tim, thay, dich = P[ten]
    nguon = (goc / "ops" / "cong_cu_test.py").read_text(encoding="utf-8")
    so_neo = nguon.count(tim)
    m.DOT_BIEN[ten] = ("ops/cong_cu_test.py", tim, thay, "TEP_TEST", m._KEM_TEP_TEST, dich)
    t0 = time.time()
    try:
        ket, ca_dich = m._do_ban_kinh(ten, bo_qua_ca=do_o_nen)
        dong, loi = m._ket_luan_ban_kinh(ten, ca_dich, ket, len(m.CA), do_o_nen)
        ghi({"ten": ten, "ho": HO[ten], "so_neo": so_neo, "dich": ca_dich[:4], "dich_tt": ket.get(ca_dich, ["?"])[0],
             "khong_qua": {t[:4]: v[0] for t, v in ket.items() if v[0] != "qua"},
             "loi": loi, "dong_dau": dong[0][:200], "giay": round(time.time() - t0, 1)})
    except AssertionError as ex:
        ghi({"ten": ten, "ho": HO[ten], "so_neo": so_neo, "LOI_DUNG": str(ex)[:300]})
    finally:
        m.DOT_BIEN.pop(ten, None)
```

## Phụ lục D — `phan_hang_r3.py` (nguyên văn, sha256 `497d12c9fc9653b9656a7891ae9f871acfcd1a66c9533bd447d7e98c5fe1275c`)

Phân hạng và chia tập theo tên (§6). Cách dùng: `python3 phan_hang_r3.py '<mẫu glob jsonl>' [chi_tiet]`. r3 thay bản r2 (`phan_hang_r2.py`, sha256 `c1bdf8d23b85e932a23cdcb9bb31403ca754c952c43911aeaffbb27aacf26065`): chỉ hàm `tap` (thêm luật cho tên của Phụ lục H và tập KHAI) và dòng in theo tập đổi; hàm `hang` giữ nguyên từng chữ. Trên 221 tên của Phụ lục C, hai bản chia tập giống hệt (đo lúc soạn r3, §1.9.10).

```python
"""Phân hạng đầu ra jsonl của Phụ lục A/C/H (wp698 r3, Phụ lục D). Không chạy đột biến nào.

Dùng: python phan_hang_r3.py <mẫu glob jsonl> [chi_tiet]
Hạng: GIET = `_ket_luan_ban_kinh` 0 lỗi, đích `giet_that`, không ca nào khác chết ngoài ca `bo_qua`;
      SONG = không ca nào chết; KHAC = mọi trường hợp còn lại (tín dụng giả, sai đích, bán kính > 1);
      LOI_DUNG = phép đo tự hỏng (AssertionError của rig).
Tập (theo TÊN, §6): KHAI = năm dò khai SỐNG nêu đích danh · NGOAI `g_…`, `t_…`, `x3_gop_…`, `x3_cua_…` ·
T-D `s2_…`, `s3_…`, `x_f50_…` · T-E `z_exc_…`, `x_exc_…`, `x3_exc_…` · T-C `…_ra`, `s_ra_…`, `p_cf_ra_…` và tầng hạ nguồn
`x_main_ra_…`, `x_wr_ra_…`, `x3_main_ra_…`, `x3_wr_ra_…`, `x3_m3a_ra_…`, `x3_m3b_ra_…`, `x3_wr5_…` · T-B còn lại.
r3 chỉ đổi hàm `tap` và dòng in theo tập so với r2; luật hạng giữ nguyên từng chữ.
"""
import collections
import glob
import json
import sys

KHAI = {"x_head_cf2063_at17", "x_head_cfk_mid_only", "x_head_sm_mid_only", "x_f50_tk_and_bq_ne3", "x_f50_h_and_bq_ne3"}


def tap(ten):
    if ten in KHAI:
        return "KHAI"
    if ten.startswith(("g_", "t_", "x3_gop_", "x3_cua_")):
        return "NGOAI"
    if ten.startswith(("s2_", "s3_", "x_f50_")):
        return "T-D"
    if ten.startswith(("z_exc_", "x_exc_", "x3_exc_")):
        return "T-E"
    if ten.endswith("_ra") or ten.startswith(("s_ra_", "p_cf_ra_", "x_main_ra_", "x_wr_ra_", "x3_main_ra_", "x3_wr_ra_",
                                              "x3_m3a_ra_", "x3_m3b_ra_", "x3_wr5_")):
        return "T-C"
    return "T-B"


def hang(r):
    if "LOI_DUNG" in r:
        return "LOI_DUNG"
    chet = {k: v for k, v in r["khong_qua"].items() if v != "bo_qua"}
    if not chet and r["dich_tt"] == "qua":
        return "SONG"
    if r["loi"] == 0 and r["dich_tt"] == "giet_that" and list(chet) == [r["dich"]]:
        return "GIET"
    return "KHAC"


dong = {}
for tep in sorted(glob.glob(sys.argv[1])):
    with open(tep, encoding="utf-8") as f:
        for x in f:
            r = json.loads(x)
            if r.get("ten") != "nen":
                dong[r["ten"]] = r
h = {t: hang(r) for t, r in dong.items()}
print("so dong", len(dong), "| so_neo", dict(collections.Counter(r.get("so_neo") for r in dong.values())))
print("tong", dict(collections.Counter(h.values())))
for tp in ("T-B", "T-C", "T-D", "T-E", "NGOAI", "KHAI"):
    c = collections.Counter(v for t, v in h.items() if tap(t) == tp)
    print(tp, sum(c.values()), dict(c))
if sys.argv[2:] == ["chi_tiet"]:
    for t in sorted(dong):
        if h[t] != "GIET":
            print(" ", h[t], tap(t), t, dong[t].get("khong_qua"), dong[t].get("dong_dau", dong[t].get("LOI_DUNG", ""))[:100])
```

## Phụ lục E — `ast_dot_bien_r2.py` (nguyên văn, sha256 `b0772b01530fa80a8e2550bdc847444e9ed3c5c81bc886f8bcb9124241a39b7d`)

Đếm chỗ ghi `DOT_BIEN` cho A4-e. Cách dùng: `python3 ast_dot_bien_r2.py ops/cong_cu_test.py`.

```python
"""Đếm bằng AST mọi chỗ GHI vào `DOT_BIEN` (wp698 r2, Phụ lục E; tiêu chí A4-e).

Dùng: python ast_dot_bien_r2.py <đường dẫn ops/cong_cu_test.py>
Chỗ ghi = gán/gán tăng/gán có chú thích vào `DOT_BIEN[...]`, `del DOT_BIEN[...]`, và lời gọi
`DOT_BIEN.pop/update/setdefault/clear/popitem(...)`, ở MỌI phạm vi. In JSON: dòng của `_TRUOC_NANG_LUC = `
và `_TEN_NANG_LUC = ` (mức mô-đun), tổng số chỗ ghi, chỗ ghi trước ảnh, số chỗ trong cửa sổ, chỗ ghi SAU mốc.
"""
import ast
import json
import sys

nguon = open(sys.argv[1], encoding="utf-8").read()
cay = ast.parse(nguon)
DOI = {"pop", "update", "setdefault", "clear", "popitem"}


def la_db(n):
    return isinstance(n, ast.Name) and n.id == "DOT_BIEN"


ghi = []
for n in ast.walk(cay):
    if isinstance(n, (ast.Assign, ast.AugAssign, ast.AnnAssign)):
        for t in (n.targets if isinstance(n, ast.Assign) else [n.target]):
            if isinstance(t, ast.Subscript) and la_db(t.value):
                ghi.append(["gan", n.lineno])
    if isinstance(n, ast.Delete):
        for t in n.targets:
            if isinstance(t, ast.Subscript) and la_db(t.value):
                ghi.append(["xoa", n.lineno])
    if isinstance(n, ast.Call) and isinstance(n.func, ast.Attribute) and n.func.attr in DOI and la_db(n.func.value):
        ghi.append(["goi:" + n.func.attr, n.lineno])
moc = {}
for n in cay.body:
    if isinstance(n, ast.Assign) and len(n.targets) == 1 and isinstance(n.targets[0], ast.Name):
        if n.targets[0].id in ("_TRUOC_NANG_LUC", "_TEN_NANG_LUC"):
            moc[n.targets[0].id] = n.lineno
a, b = moc["_TRUOC_NANG_LUC"], moc["_TEN_NANG_LUC"]
print(json.dumps({"_TRUOC_NANG_LUC": a, "_TEN_NANG_LUC": b, "tong": len(ghi),
                  "truoc_anh": sorted(x[1] for x in ghi if x[1] < a),
                  "trong_cua_so": sum(1 for x in ghi if a <= x[1] < b),
                  "sau_moc": sorted(x[1] for x in ghi if x[1] > b)}, ensure_ascii=True))
```

## Phụ lục F — `kiem_canh_r4.py` (nguyên văn, sha256 `6ce86883a7510751654dd90c8f1f98e4c6c6c64757c2a929c8b297c5bde2b6aa`)

Phép kiểm A5 (vi) và (r4) phép đếm mỏ neo: so BỘ (mỏ neo, phép thay, ca đích) của từng canh với dò cùng tên, không chỉ so tên; rồi đếm số lần mỏ neo của **mọi** mục `DOT_BIEN` xuất hiện trong tệp đích của nó trên cây ứng viên. r4 thay bản r3 (`kiem_canh_r3.py`, sha256 `1125d6bedde472465031ef5739cc552cfc33be13caa43d30f2ded4176786e988`, dùng ở §1.9): phần so bộ giữ nguyên từng dòng; thêm khối `dem-neo` và trường `dem_neo` của đầu ra. Cách dùng: `PYTHONDONTWRITEBYTECODE=1 python3 kiem_canh_r4.py <gốc nền> <gốc ứng viên> <bảng nối> do_dot_bien.py do_dot_bien_r4.py` (Phụ lục A và bản ghép Phụ lục C + H + J). Phản chứng đã chạy lúc soạn r4 (§1.10.2): `v4_all` ⇒ rc=0, 0/470 lệch; `v4_lit` ⇒ rc=1 `dem-neo` 1 mục; `v4_tq` ⇒ rc=1 `dem-neo` 55 mục; `v4_cu` ⇒ rc=1 `dem-neo` 1 mục cũ; canh yếu hơn cùng tên ⇒ `lech-bo`; bộ cũ bị đổi ⇒ `bo-cu`; bảng nối thiếu một dòng ⇒ `tap-ten`; chính script với `if so != mong:` đổi thành `if False:` ⇒ `v4_lit` rc=0.

```python
"""A5 của wp698 r4 (Phụ lục F): bảng canh `DOT_BIEN` của ứng viên so với dò CÙNG TÊN trong các phụ lục — so BỘ, không so tên —
VÀ đếm số lần xuất hiện mỏ neo của MỌI mục trong tệp đích của nó trên cây ứng viên.

Dùng: PYTHONDONTWRITEBYTECODE=1 python kiem_canh_r4.py <gốc nền> <gốc ứng viên> <bảng nối> <script dò>...
  bảng nối : mỗi dòng "<tên dò> <tên mục DOT_BIEN>" (cách nhau bằng khoảng trắng), đúng một dòng mỗi canh.
  script dò: Phụ lục A và bản ghép Phụ lục C + H (+ J); bảng `P` của mỗi script lấy bằng cách chạy nó ở chế độ `liet_ke`.
Đỏ (mã 1) khi: một bộ sáu trường cũ của nền đổi hay mất; tập tên thêm khác cột phải của bảng nối; bảng nối trùng tên;
một tên dò không có trong phụ lục; bộ của mục khác ("ops/cong_cu_test.py", tìm, thay, "TEP_TEST", _KEM_TEP_TEST, ca đích)
dựng từ dò cùng tên; hoặc (r4, `dem-neo`) mỏ neo của một mục xuất hiện trong tệp đích của nó trên cây ứng viên một số lần
khác số mong: 1 với mọi mục có tệp đích `ops/cong_cu_test.py` và mọi mục thêm; với mục cũ có tệp đích khác thì bằng số
lần trên cây nền (đo lúc soạn r4: ba mục `bn_*` của `ops/bash_nen.py` là 2, 2, 3 trên nền). `_dung_cay_dot_bien` chỉ thay
lần xuất hiện ĐẦU, nên mỏ neo có mặt hai lần thì đột biến có thể rơi vào literal của bảng thay vì chỗ ghi. In JSON.
"""
import contextlib
import importlib.util
import io
import json
import sys
from pathlib import Path

nen, ung, bang, *nguon = sys.argv[1:]


def nap(goc, ten):
    spec = importlib.util.spec_from_file_location(ten, Path(goc) / "ops" / "cong_cu_test.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


P, argv = {}, sys.argv
for f in nguon:
    ns = {"__name__": "pl"}
    sys.argv = [f, nen, "/dev/null", "liet_ke"]
    with contextlib.redirect_stdout(io.StringIO()):
        try:
            exec(compile(Path(f).read_text(encoding="utf-8"), f, "exec"), ns)
        except SystemExit:
            pass
    sys.argv = argv
    trung = set(P) & set(ns["P"])
    assert not trung, sorted(trung)[:5]
    P.update(ns["P"])
mn, mu = nap(nen, "cct_nen"), nap(ung, "cct_ung")
noi = [x.split() for x in Path(bang).read_text(encoding="utf-8").splitlines() if x.strip()]
loi = [["bo-cu", t] for t, v in mn.DOT_BIEN.items() if mu.DOT_BIEN.get(t) != v]
them = {t for t in mu.DOT_BIEN if t not in mn.DOT_BIEN}
cot = [x[-1] for x in noi]
if any(len(x) != 2 for x in noi) or len(set(cot)) != len(cot) or len({x[0] for x in noi}) != len(noi):
    loi.append(["bang-noi", "dòng không đúng hai cột hoặc tên trùng"])
if them != set(cot):
    loi.append(["tap-ten", sorted(them ^ set(cot))[:10]])
for x in noi:
    if len(x) != 2:
        continue
    do, muc = x
    if do not in P:
        loi.append(["khong-co-do", do])
        continue
    tim, thay, dich = P[do]
    if mu.DOT_BIEN.get(muc) != ("ops/cong_cu_test.py", tim, thay, "TEP_TEST", mu._KEM_TEP_TEST, dich):
        loi.append(["lech-bo", do, muc])
doc = {}
dem = {"muc": 0, "lech": 0}
for t, v in mu.DOT_BIEN.items():
    tep, tim = v[0], v[1]
    for g in (ung, nen):
        if (g, tep) not in doc:
            p = Path(g) / tep
            doc[(g, tep)] = p.read_text(encoding="utf-8") if p.is_file() else ""
    so = doc[(ung, tep)].count(tim)
    mong = 1 if tep == "ops/cong_cu_test.py" or t in them else doc[(nen, tep)].count(tim)
    dem["muc"] += 1
    if so != mong:
        dem["lech"] += 1
        loi.append(["dem-neo", t, so, mong])
print(json.dumps({"nen": len(mn.DOT_BIEN), "ung_vien": len(mu.DOT_BIEN), "them": len(them), "bang_noi": len(noi),
                  "dem_neo": dem, "so_loi": len(loi), "loi": loi[:20]}, ensure_ascii=True))
sys.exit(1 if loi else 0)
```

## Phụ lục G — `giao_a4d_r3.py` (nguyên văn, sha256 `cd0817d5974c045781903a5a33486a3e195f0636bd938eac056291a602b39200`)

Phép kiểm A4-d bằng máy. Cách dùng: `python3 giao_a4d_r3.py <gốc checkout> fc852fff7da37f1669569572b79571446e61c294`. Phản chứng đã chạy lúc soạn r3 (§1.9.10): ứng viên của reviewer lượt 2 và biến thể `v3_all` ⇒ giao rỗng, rc=0; sửa một dòng trong thân `_van_tay` ⇒ rc=1; chèn một dòng ngay sau dòng cuối của `_van_tay` ⇒ rc=1; sửa một dòng trong thân `main` ⇒ rc=1; chèn một hằng ở mức mô-đun cách `_van_tay` bởi dòng trống ⇒ rc=0.

```python
"""A4-d của wp698 r3 (Phụ lục G): diff có chạm thân sáu hàm cấm sửa không — đo bằng máy, không bằng mắt.

Dùng: python giao_a4d_r3.py <gốc checkout> <sha nền>
Khoảng của mỗi hàm = [dòng decorator đầu (hoặc dòng def), end_lineno] do `ast` trả trên tệp NỀN. Mỗi hunk của
`git diff -U0 <nền> -- ops/cong_cu_test.py` lấy khoảng PHÍA NỀN: `-a,b` với b > 0 là dòng a…a+b−1; `-a,0` là chèn sau
dòng a, tính là chạm khi d ≤ a ≤ c (chèn ngay sau dòng cuối cũng tính, vì dòng thụt lề ở đó nối vào thân hàm).
In JSON; giao khác rỗng ⇒ mã thoát 1.
"""
import ast
import json
import re
import subprocess
import sys

goc, nen = sys.argv[1], sys.argv[2]
SAU = ("_doc_che_do", "_van_tay", "main", "_so_tien_trinh_ban_kinh", "_ket_luan_ban_kinh", "_chay_1_ca")
git = lambda *a: subprocess.run(["git", "-C", goc, *a], capture_output=True, text=True, check=True).stdout
khoang = {n.name: (min([n.lineno] + [x.lineno for x in n.decorator_list]), n.end_lineno)
          for n in ast.parse(git("show", nen + ":ops/cong_cu_test.py")).body
          if isinstance(n, (ast.FunctionDef, ast.AsyncFunctionDef)) and n.name in SAU}
assert set(khoang) == set(SAU), sorted(khoang)
hunk, cham = 0, []
for x in git("diff", "-U0", nen, "--", "ops/cong_cu_test.py").splitlines():
    m = re.match("@@ -([0-9]+)(,([0-9]+))? ", x)
    if not m:
        continue
    hunk += 1
    a, b = int(m.group(1)), int(m.group(3) or 1)
    for ten, (d, c) in khoang.items():
        if (d <= a <= c) if b == 0 else (a <= c and a + b - 1 >= d):
            cham.append([ten, x[:60]])
print(json.dumps({"khoang": khoang, "hunk": hunk, "cham": cham}, ensure_ascii=True))
sys.exit(1 if cham else 0)
```

## Phụ lục H — `khoi_do_r3.py` (nguyên văn, sha256 `850734781257b3041e251e4e6554da60e76d4dfb3137add9bdf26b46ce3f90f7`)

Khối dò của r3, ghép vào Phụ lục C ngay TRƯỚC dòng `def ghi(x):`. Lệnh ghép (không có dấu chéo ngược): `{ awk '/^def ghi/{exit} {print}' do_dot_bien_r2.py; cat khoi_do_r3.py; echo; echo; sed -n '/^def ghi/,$p' do_dot_bien_r2.py; } > do_dot_bien_r3.py` — bản ghép có sha256 `37b6e8bd53e8c14bc634a198aa4fabff7400b662d67b38ab80caf90aeef6e55b`. Bản ghép dùng y hệt Phụ lục C (`liet_ke`, `ho`, `nen`, `<tên dò>…`); bảng `P` của nó có 366 dò, 221 dò đầu trùng từng mục với Phụ lục C (đo lúc soạn r3). E1–E8 chép NGUYÊN từ `evidence/extra_probes.py` của reviewer lượt 2; R3-* là dò của phiên soạn r3.

```python
"""Khối dò của wp698 r3 (Phụ lục H): ghép vào Phụ lục C ngay TRƯỚC dòng `def ghi(x):` (xem cách ghép ở Phụ lục H).

E1–E8: dò ngoài tập đóng của reviewer lượt 2 (`evidence/extra_probes.py`, sha256 b678a50f…3c0e), chép NGUYÊN mỏ neo và
phép thay. R3-*: dò của phiên soạn r3. Không có dấu chéo ngược nào: chéo ngược là chr(92), xuống dòng là NL = chr(10).
"""
# ======================= EXTRA (reviewer lượt 2) — dò NGOÀI tập đóng Phụ lục C =======================
# E1: mở rộng tập bắt ngoại lệ của `_van_tay` sang kiểu NGOÀI ba kiểu M5 (ValueError/UnicodeDecodeError/RuntimeError)
for _t, _thay in (("x_exc_typeerror", "TypeError"), ("x_exc_attributeerror", "AttributeError"), ("x_exc_keyerror", "KeyError"),
                  ("x_exc_lookuperror", "LookupError"), ("x_exc_assertionerror", "AssertionError"), ("x_exc_importerror", "ImportError"),
                  ("x_exc_eoferror", "EOFError"), ("x_exc_unicodeencodeerror", "UnicodeEncodeError"),
                  ("x_exc_notimplemented", "NotImplementedError"), ("x_exc_indexerror", "IndexError"),
                  ("x_exc_zerodiv", "ZeroDivisionError"), ("x_exc_memoryerror", "MemoryError")):
    them("x-exc", _t, (EXC, f"    except (OSError, subprocess.SubprocessError, {_thay}):" + NL + '        head = ""' + NL, T53))
# E2: `head` — cấu trúc nhiều dòng của stdout (nhiễu trước/sau mã băm)
for _t, _expr in (
        ("x_head_lastline", '(p.stdout.strip().splitlines() or [""])[-1].strip()'),
        ("x_head_lastline_raw", '(p.stdout.splitlines() or [""])[-1].strip()'),
        ("x_head_firstline", '(p.stdout.strip().splitlines() or [""])[0].strip()'),
        ("x_head_lastnonblank", '([l for l in p.stdout.splitlines() if l.strip()] or [""])[-1].strip()'),
        ("x_head_split_last", '(p.stdout.split() or [""])[-1]'),
        ("x_head_split_first", '(p.stdout.split() or [""])[0]')):
    them("x-head", _t, (HEAD, f'        head = {_expr} if p.returncode == 0 else ""' + NL, T53))
# E3: `head` — thành viên NGOÀI R698 × vị trí NGOÀI ba neo
them("x-head-pos", "x_head_cf2063_at17", head_(tai(17, "ord(c) == 0x2063")))
them("x-head-pos", "x_head_cfk_mid_only", head_(giua(CFK)))
them("x-head-pos", "x_head_sm_mid_only", head_(giua('unicodedata.category(c) == "Sm"')))
them("x-head-pos", "x_head_cfk_lead_only", head_(dau(CFK)))
them("x-head-pos", "x_head_cfk_trail_only", head_(cuoi(CFK)))
# E4: `head` — NFKC chỉ chữ cái hex fullwidth (đối chứng: phải bị giết vì mọi vị trí hex đều nhận chữ hex)
them("x-head-pos", "x_head_nfkc_fwletters", head_(nfkc("0xFF41 <= ord(c) <= 0xFF46")))

# E5: `ra` ở HẠ NGUỒN của `_doc_che_do` — (a) trong `main` ngay sau `k, n, ra = tham_so` (ca đích t54), (b) ở bộ ghi `_ket_thuc_manh` (`tep = Path(ra)`; ca đích t52)
MAIN_RA = "        k, n, ra = tham_so" + NL
WR = "    tep = Path(ra)" + NL
_PH = (("normpath", "os.path.normpath(ra)"), ("expanduser", "os.path.expanduser(ra)"),
       ("nfkc", 'unicodedata.normalize("NFKC", ra)'),
       ("cf", '"".join(c for c in ra if unicodedata.category(c) != "Cf")'),
       ("tab", 'ra.replace(chr(9), "")'),
       ("zs", '"".join(c for c in ra if not (unicodedata.category(c) == "Zs" and c != " "))'))
for _t, _e in _PH:
    them("x-main-ra", f"x_main_ra_{_t}", (MAIN_RA, "        import unicodedata" + NL + MAIN_RA + f"        ra = {_e}" + NL, T54))
    them("x-wr-ra", f"x_wr_ra_{_t}", (WR, "    import unicodedata" + NL + f"    tep = Path({_e.replace('ra', 'ra', 1)})" + NL, T52))

# E6: `head` — nhiễu nhiều dòng, tách CHỈ theo LF (thành ngữ hay gặp: dòng cuối/đầu của stdout); VT/NEL... không phải LF
for _t, _expr in (
        ("x_head_nl_last", 'p.stdout.strip().split(chr(10))[-1].strip()'),
        ("x_head_nl_first", 'p.stdout.strip().split(chr(10))[0].strip()'),
        ("x_head_rsplit_nl", 'p.stdout.strip().rsplit(chr(10), 1)[-1].strip()'),
        ("x_head_crlf_last", 'p.stdout.strip().split(chr(13) + chr(10))[-1].strip()')):
    them("x-head", _t, (HEAD, f'        head = {_expr} if p.returncode == 0 else ""' + NL, T53))

# E7: nhóm Unicode KHÔNG có dò riêng trong tập đóng — xoá cả nhóm khỏi `bk` (đo răng của A1 trước bản dùng danh sách nhóm thay vì luật)
for _g in ("Sm", "Sc", "Sk", "So", "Pc", "Pd", "Ps", "Pe", "Pi", "Pf", "Po", "Mc", "Me", "Nl", "Lm", "Lt", "Zl", "Zp"):
    them("x-nhom", f"x_cat_{_g.lower()}_bk", bk_(bo(f'unicodedata.category(c) == "{_g}"')))

# E8: F50 — vị từ lực lượng của nhánh mảnh: biến thể NGOÀI T-D (đo răng của "trục trọn + tích biên" trước vị từ có hằng)
for _t, _e in (("x_f50_or_bq_eq2", "hong or tien_kiem_bo_qua or len(bo_qua) == 2"),
               ("x_f50_or_bq_eq7", "hong or tien_kiem_bo_qua or len(bo_qua) == 7"),
               ("x_f50_tk_ge2", "hong or len(tien_kiem_bo_qua) >= 2"),
               ("x_f50_h_ge2", "len(hong) >= 2 or tien_kiem_bo_qua"),
               ("x_f50_tk_and_bq_ne3", "hong or (tien_kiem_bo_qua and len(bo_qua) != 3)"),
               ("x_f50_h_and_bq_ne3", "(hong and len(bo_qua) != 3) or tien_kiem_bo_qua")):
    them("x-f50", _t, (NEN, "        if " + _e + ":" + NL + "            _ket_thuc_manh(", T54))

# ======================= R3 (phiên soạn r3) — dò NGOÀI tập đóng, đo các hướng vá của r3 =======================
# R3-EXC: mở rộng tập bắt sang kiểu NGOÀI miền "lớp con của Exception trong builtins" (hướng M5b của HINT),
# cộng hai dạng cú pháp tương đương mở rộng (mệnh đề except thứ hai; except trần).
for _t, _thay in (("x3_exc_kbint", "KeyboardInterrupt"), ("x3_exc_sysexit", "SystemExit"),
                  ("x3_exc_genexit", "GeneratorExit"), ("x3_exc_bexgroup", "BaseExceptionGroup"),
                  ("x3_exc_exgroup", "ExceptionGroup"), ("x3_exc_stopiter", "StopIteration"),
                  ("x3_exc_warning", "Warning"), ("x3_exc_re_error", "re.error"),
                  ("x3_exc_json", "json.JSONDecodeError")):
    them("x3-exc", _t, (EXC, f"    except (OSError, subprocess.SubprocessError, {_thay}):" + NL + '        head = ""' + NL, T53))
them("x3-exc", "x3_exc_menh_de_hai", (EXC, EXC + "    except TypeError:" + NL + '        head = ""' + NL, T53))
them("x3-exc", "x3_exc_tran", (EXC, "    except:" + NL + '        head = ""' + NL, T53))

# R3-HEAD: tách stdout theo TỪNG ký tự tách dòng của str.splitlines (ngoài LF đã có ở E6) và theo khoảng trắng
# không-phải-tách-dòng mà strip() vẫn bỏ (TAB, U+001F, Zs) — mỗi phép lấy phần cuối/đầu.
_SEP3 = {"cr": "chr(13)", "vt": "chr(11)", "ff": "chr(12)", "fs": "chr(0x1C)", "gs": "chr(0x1D)", "rs": "chr(0x1E)",
         "nel": "chr(0x85)", "ls": "chr(0x2028)", "ps": "chr(0x2029)"}
for _x, _s in _SEP3.items():
    for _vt, _ix in (("last", "-1"), ("first", "0")):
        them("x3-head", f"x3_head_{_x}_{_vt}",
             (HEAD, f'        head = p.stdout.strip().split({_s})[{_ix}].strip() if p.returncode == 0 else ""' + NL, T53))
them("x3-head", "x3_head_crlf_first",
     (HEAD, '        head = p.stdout.strip().split(chr(13) + chr(10))[0].strip() if p.returncode == 0 else ""' + NL, T53))
for _x, _s in (("tab", "chr(9)"), ("us", "chr(0x1F)"), ("nbsp", "chr(0xA0)"), ("emsp", "chr(0x2003)"), ("ideo", "chr(0x3000)")):
    them("x3-head", f"x3_head_{_x}_last",
         (HEAD, f'        head = p.stdout.strip().split({_s})[-1].strip() if p.returncode == 0 else ""' + NL, T53))
them("x3-head", "x3_head_pick_hex",
     (HEAD, '        head = next((x.strip() for x in p.stdout.splitlines() if re.fullmatch("[0-9a-f]{40}|[0-9a-f]{64}", x.strip())), "")'
      ' if p.returncode == 0 else ""' + NL, T53))
them("x3-head", "x3_head_longest", (HEAD, '        head = max(p.stdout.split() or [""], key=len) if p.returncode == 0 else ""' + NL, T53))

# R3-RA: `ra` ở MỌI tầng sau `_doc_che_do` — T2 unpack trong `main` (phép ngoài sáu phép của E5), T3a lời gọi bộ ghi ở
# nhánh nền đỏ, T3b lời gọi bộ ghi ở nhánh thường, T4 bộ ghi (phép ngoài E5), T5 chỗ dùng `tep` khi ghi.
_PH3 = (("expandvars", "os.path.expandvars(ra)"), ("rstrip_slash", 'ra.rstrip("/")'),
        ("lstrip_dot", 'ra[2:] if ra.startswith("./") else ra'), ("lower", "ra.lower()"),
        ("bslash", 'ra.replace(chr(92), "/")'), ("nfd", 'unicodedata.normalize("NFD", ra)'),
        ("dslash", 'ra.replace("//", "/")'),
        ("cc", '"".join(c for c in ra if not (unicodedata.category(c) == "Cc" and c != chr(9)))'),
        ("mn", '"".join(c for c in ra if unicodedata.category(c) != "Mn")'))
for _t, _e in _PH3:
    them("x3-main-ra", f"x3_main_ra_{_t}", (MAIN_RA, "        import unicodedata" + NL + MAIN_RA + f"        ra = {_e}" + NL, T54))
for _t, _e in (("expandvars", "os.path.expandvars(ra)"), ("lower", "ra.lower()"), ("bslash", 'ra.replace(chr(92), "/")'),
               ("cc", '"".join(c for c in ra if not (unicodedata.category(c) == "Cc" and c != chr(9)))'),
               ("mn", '"".join(c for c in ra if unicodedata.category(c) != "Mn")')):
    them("x3-wr-ra", f"x3_wr_ra_{_t}", (WR, "    import unicodedata" + NL + f"    tep = Path({_e})" + NL, T52))
_GOI_NEN = ('            _ket_thuc_manh(k, n, ra, ten, None, "n' + chr(0x1EC1) + 'n ' + chr(0x111) + chr(0x1ECF)
            + ' ho' + chr(0x1EB7) + 'c ti' + chr(0x1EC1) + 'n ki' + chr(0x1EC3) + 'm b' + chr(0x1ECB) + ' b' + chr(0x1ECF)
            + ' qua ' + chr(0x2014) + ' kh' + chr(0xF4) + 'ng ' + chr(0x111) + 'o", _van_tay())' + NL)
_GOI_THUONG = "        dong, loi = _ket_thuc_manh(k, n, ra, ten, None if ly_con else ket, ly_con, _van_tay())" + NL
for _t, _e in _PH:
    them("x3-m3a", f"x3_m3a_ra_{_t}", (_GOI_NEN, "            import unicodedata" + NL
                                        + _GOI_NEN.replace("(k, n, ra, ten,", "(k, n, " + _e + ", ten,", 1), T54))
    them("x3-m3b", f"x3_m3b_ra_{_t}", (_GOI_THUONG, "        import unicodedata" + NL
                                        + _GOI_THUONG.replace("(k, n, ra, ten,", "(k, n, " + _e + ", ten,", 1), T54))
_W5 = "    tep.write_bytes(("
them("x3-wr5", "x3_wr5_normpath", (_W5, "    Path(os.path.normpath(str(tep))).write_bytes((", T52))
them("x3-wr5", "x3_wr5_nfkc", (_W5, "    import unicodedata" + NL + '    Path(unicodedata.normalize("NFKC", str(tep))).write_bytes((', T52))
# R3-ARGV: bộ đọc argv mà §2 của r2 chưa liệt kê — thư mục `--gop` (job gom) và cửa ở argv[1] (dispatcher)
_GOP = "    dong, loi = _gom_manh(sys.argv[i + 1], _van_tay())" + NL
for _t, _e in (("normpath", "os.path.normpath(sys.argv[i + 1])"), ("nfkc", 'unicodedata.normalize("NFKC", sys.argv[i + 1])'),
               ("strip", "sys.argv[i + 1].strip()")):
    them("x3-gop", f"x3_gop_dir_{_t}", (_GOP, "    import unicodedata" + NL + _GOP.replace("sys.argv[i + 1]", _e, 1), T52))
_CUA3 = "    cua = sys.argv[1] if len(sys.argv) > 1 else None" + NL
them("x3-cua", "x3_cua_strip", (_CUA3, "    cua = sys.argv[1].strip() if len(sys.argv) > 1 else None" + NL, T52))
them("x3-cua", "x3_cua_nfkc", (_CUA3, "    import unicodedata" + NL
                                + '    cua = unicodedata.normalize("NFKC", sys.argv[1]) if len(sys.argv) > 1 else None' + NL, T52))

# R3-NHOM: một dò xoá-cả-nhóm cho MỖI nhóm Unicode chung có mặt trong D698 (dẫn xuất, không chọn tay), trên `bk`
import unicodedata as _ud3
_CAT3 = sorted({_ud3.category(chr(c)) for c in range(0x110000) if not 0xD800 <= c <= 0xDFFF and (
    _ud3.category(chr(c)) not in ("Lo", "Co", "Cn") or _ud3.normalize("NFKC", chr(c)) != chr(c))})
for _g in _CAT3:
    if f"x_cat_{_g.lower()}_bk" not in P:
        them("x3-nhom", f"x3_cat_{_g.lower()}_bk", bk_(bo(f'unicodedata.category(c) == "{_g}"')))

# R3-HEAD (bổ sung): tách theo ký tự KHÔNG phải khoảng trắng — kỳ vọng: ô chèn đầu/cuối của M1 (D698 × ba neo) đã giết.
for _x, _s in (("zwsp", "chr(0x200B)"), ("chu_g", '"g"')):
    them("x3-head", f"x3_head_{_x}_last",
         (HEAD, f'        head = p.stdout.strip().split({_s})[-1].strip() if p.returncode == 0 else ""' + NL, T53))
```

## Phụ lục I — `chi_phi_r4.py` (nguyên văn, sha256 `1b0814d690f4bb436b01190a4e66092b8ad45f4173903e90c20849b455e32d04`)

Phép kiểm A4-g (chi phí), bản r4. r4 thay bản r3 (`chi_phi_r3.py`, sha256 `db512319ac4c8b7768482699091b1e062cb50467cc6b03a31ac636b2cc6dc436`, dùng ở §1.9.9): phép đếm giữ nguyên từng dòng; phép đồng hồ làm đỏ được thay bằng phép CPU (`getrusage` SELF + CHILDREN) đo theo tỷ lệ với thước của chính máy — CPU của một lượt trọn mọi ca trên nền, đo trong cùng lệnh — ngưỡng r ≤ 1,35; giây tường chỉ còn là chỉ báo, in kèm số lõi mà tiến trình khác dùng trong cửa sổ đo và loadavg. Chỉ chạy trên POSIX (`resource`, `/proc/stat`). Cách dùng: `PYTHONDONTWRITEBYTECODE=1 python3.12 chi_phi_r4.py <gốc nền> <gốc ứng viên>`. Phản chứng đã chạy lúc soạn r4: §1.10.5.

```python
"""A4-g của wp698 r4 (Phụ lục I): chi phí của ứng viên so với nền, trong MỘT lệnh, cùng phiên bản Python. Chỉ POSIX.

Dùng: PYTHONDONTWRITEBYTECODE=1 python chi_phi_r4.py <gốc nền> <gốc ứng viên>
(1) ĐẾM (tất định): chạy cửa con `--tu-kiem-che-do` TRONG tiến trình với `_van_tay` được bọc (thay tên toàn cục của
    mô-đun; cửa con tra tên ấy lúc gọi) — số lời gọi, số lời gọi mà `TEP_TEST` lúc gọi lớn hơn 4096 byte, tổng byte băm.
(2) CPU: `t52`, `t53`, `t54` qua `_chay_1_ca`, ba vòng, XEN KẼ nền và ứng viên; mỗi lượt đo CPU người dùng + hệ thống của
    CHÍNH tiến trình cộng mọi tiến trình con đã được `wait` (`getrusage` SELF + CHILDREN, hiệu trước/sau); lấy MIN mỗi ca;
    Δ_CPU = tổng qua ba ca của (min ứng viên − min nền).
(3) THƯỚC CỦA CHÍNH MÁY: C56 = CPU của MỘT lượt trọn mọi ca của `CA` trên nền (đo như (2)) — đại diện cho CPU của một lượt
    đột biến, vì mỗi lượt đột biến chạy trọn các ca ấy. Tỷ lệ r = (C56 + Δ_CPU)/C56 không phụ thuộc máy nhanh hay chậm;
    mảnh dài nhất ước ≈ 18,23 phút × (59/52) × r (mô hình §7: job dài nhất của run 36696528580; lực lượng mảnh lớn nhất).
(4) ĐỒNG HỒ — CHỈ BÁO, không làm đỏ: giây tường cùng các lượt ấy, kèm số lõi mà tiến trình KHÁC trên máy dùng trong cửa sổ
    đo (`/proc/stat` bận trừ CPU của chính lệnh này) và loadavg trước/sau, để người đọc biết đồng hồ đo trong điều kiện nào.
ĐỎ (mã 1) khi: lời gọi lớn của ứng viên > 2 × nền; hoặc r > 1,35 (tức mảnh ước > 27,9 phút, dưới trần 30 phút của job hơn
2 phút); hoặc một lượt ca không ra `qua`. In JSON.
"""
import contextlib
import importlib.util
import io
import json
import os
import resource
import sys
import time
from pathlib import Path

goc = {"nen": sys.argv[1], "ung_vien": sys.argv[2]}
CA_DO, TRAN_TY_LE, JOB, LUC_LUONG = ("t52_", "t53_", "t54_"), 1.35, 18.23, 59 / 52


def nap(g, ten):
    spec = importlib.util.spec_from_file_location(ten, Path(g) / "ops" / "cong_cu_test.py")
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def cpu():
    a, b = resource.getrusage(resource.RUSAGE_SELF), resource.getrusage(resource.RUSAGE_CHILDREN)
    return a.ru_utime + a.ru_stime + b.ru_utime + b.ru_stime


def ban():
    try:
        x = [int(v) for v in Path("/proc/stat").read_text().splitlines()[0].split()[1:]]
    except (OSError, ValueError, IndexError):
        return None
    return sum(x) - x[3] - (x[4] if len(x) > 4 else 0)


mod = {k: nap(g, "cct_" + k) for k, g in goc.items()}
kq = {k: {"goi": 0, "lon": 0, "byte": 0, "cpu": {}, "giay": {}} for k in goc}
for k, m in mod.items():
    ham, dem = m._van_tay, kq[k]

    def boc(*a, _m=m, _h=ham, _d=dem, **kw):
        n = Path(_m.TEP_TEST).stat().st_size
        _d["goi"] += 1
        _d["lon"] += n > 4096
        _d["byte"] += n
        return _h(*a, **kw)
    m._van_tay = boc
    with contextlib.redirect_stdout(io.StringIO()):
        m._in_tu_kiem_che_do()
    m._van_tay = ham
loi, tai0, ban0, c0, t0 = [], os.getloadavg(), ban(), cpu(), time.perf_counter()
for vong in range(3):
    for k, m in mod.items():
        for pre in CA_DO:
            fn = next(f for f in m.CA if f.__name__.startswith(pre))
            a, b = time.perf_counter(), cpu()
            tt, ly = m._chay_1_ca(fn)
            kq[k]["cpu"].setdefault(pre, []).append(round(cpu() - b, 2))
            kq[k]["giay"].setdefault(pre, []).append(round(time.perf_counter() - a, 2))
            if tt != "qua":
                loi.append([k, pre, tt, str(ly)[:120]])
a, b, hong56 = time.perf_counter(), cpu(), []
for fn in mod["nen"].CA:
    tt, ly = mod["nen"]._chay_1_ca(fn)
    if tt not in ("qua", "bo_qua"):
        hong56.append([fn.__name__[:4], tt])
c56, g56 = round(cpu() - b, 2), round(time.perf_counter() - a, 2)
cua_so, minh, ban1 = time.perf_counter() - t0, cpu() - c0, ban()
khac = None if ban0 is None or ban1 is None else round(((ban1 - ban0) / os.sysconf("SC_CLK_TCK") - minh) / cua_so, 2)
if hong56:
    loi.append(["nen_56", hong56[:5]])
if kq["ung_vien"]["lon"] > 2 * kq["nen"]["lon"]:
    loi.append(["dem", kq["ung_vien"]["lon"], kq["nen"]["lon"]])
delta = {d: round(sum(min(kq["ung_vien"][d][p]) - min(kq["nen"][d][p]) for p in CA_DO), 2) for d in ("cpu", "giay")}
r = round((c56 + delta["cpu"]) / c56, 4)
if r > TRAN_TY_LE:
    loi.append(["cpu", r, TRAN_TY_LE])
print(json.dumps({"kq": kq, "delta_cpu": delta["cpu"], "c56_nen": c56, "ty_le": r,
                  "manh_uoc_phut": round(JOB * LUC_LUONG * r, 2),
                  "dong_ho": {"delta_giay": delta["giay"], "giay56_nen": g56, "loi_khac_dung": khac,
                              "loadavg": [round(tai0[0], 2), round(os.getloadavg()[0], 2)], "cua_so_giay": round(cua_so, 1)},
                  "loi": loi}, ensure_ascii=True))
sys.exit(1 if loi else 0)
```

## Phụ lục J — `khoi_do_r4.py` (nguyên văn, sha256 `687a358833c9d470a03f328f3f163fd7e21ab28f3891b81ab8b180a5f5fe8c7c`)

Khối dò của r4, ghép vào bản ghép Phụ lục C + H (`do_dot_bien_r3.py`, sha256 `37b6e8bd53e8c14bc634a198aa4fabff7400b662d67b38ab80caf90aeef6e55b`) ngay TRƯỚC dòng `def ghi(x):`. Lệnh ghép (không có dấu chéo ngược): `{ awk '/^def ghi/{exit} {print}' do_dot_bien_r3.py; cat khoi_do_r4.py; echo; echo; sed -n '/^def ghi/,$p' do_dot_bien_r3.py; } > do_dot_bien_r4.py` — bản ghép có sha256 `bec92f6ea6b4c20e24b698712cc3dd09c4ba8590a7b5291d64826f38f3920236`. Bản ghép dùng y hệt Phụ lục C (`liet_ke`, `ho`, `nen`, `<tên dò>…`); bảng `P` của nó có 401 dò, 366 dò đầu trùng từng mục với bản ghép của r3 (đo lúc soạn r4). Khối dùng lại tên của Phụ lục C và H (`RA`, `HEAD`, `MAIN_RA`, `WR`, `_GOI_NEN`, `_GOI_THUONG`, `_W5`, `them`, `T52`/`T53`/`T54`, `NL`); mọi dò của nó do phiên soạn r4 liệt kê từ mã.

```python
"""Khối dò của wp698 r4 (Phụ lục J): ghép vào bản ghép Phụ lục C + H ngay TRƯỚC dòng `def ghi(x):` (lệnh ở Phụ lục J).

Ba nhóm, do phiên soạn r4 liệt kê từ mã theo CHỖ GỌI và TẦNG (không chép từ verdict lượt 3):
 J-NEM: luật "mọi BaseException do mã bị đo ném là DỮ LIỆU" ở bốn chỗ gọi — T1 (`doc` của cửa `--tu-kiem-che-do`), quét
        `head`, `main` của T2/T3 (cửa `--tu-kiem-main`), bộ ghi T4/T5 (cửa `--tu-kiem-gom`). Mỗi chỗ một dò răng NHÂN TẠO
        (`sys.exit` chỉ khi gặp giá trị mà ô của nền không có) cộng các dò TỰ NHIÊN ném OSError hay TypeError.
 J-T5 : mọi chỗ dùng `tep` ở T5 ngoài `write_bytes` — gỡ tệp cũ, `exists`, `is_symlink`, `mkdir`, dòng in.
 J-TV : thành viên ngoài `R698` (U+2063, U+E0020, U+FF41) ở T2, T3a, T3b, T4, T5.
Mọi tên kết thúc bằng `_ra` (tập T-C theo hàm `tap` của Phụ lục D) trừ `x4_head_thoat` (T-B).
Không có dấu chéo ngược nào: chéo ngược là chr(92), xuống dòng là NL = chr(10).
"""
# ======================= J-NEM — ngoại lệ do mã bị đo ném, ở bốn chỗ gọi =======================
_THOAT = " if ra.isascii() else sys.exit(698)"
them("x4-nem", "x4_t1_thoat_ra", (RA, "    ra = ra" + _THOAT + NL + RA, T53))
them("x4-nem", "x4_head_thoat", (HEAD, "        head = (p.stdout.strip() if all(ord(c) < 0x10000 for c in p.stdout) else sys.exit(698))"
                                       ' if p.returncode == 0 else ""' + NL, T53))
them("x4-nem", "x4_t2_thoat_ra", (MAIN_RA, MAIN_RA + "        ra = ra" + _THOAT + NL, T54))
them("x4-nem", "x4_t2_resolve_ra", (MAIN_RA, MAIN_RA + "        ra = str(Path(ra).resolve(strict=True))" + NL, T54))
them("x4-nem", "x4_t3a_thoat_ra", (_GOI_NEN, _GOI_NEN.replace("(k, n, ra, ten,", "(k, n, ra" + _THOAT + ", ten,", 1), T54))
them("x4-nem", "x4_t3b_thoat_ra", (_GOI_THUONG, _GOI_THUONG.replace("(k, n, ra, ten,", "(k, n, ra" + _THOAT + ", ten,", 1), T54))
them("x4-nem", "x4_t4_thoat_ra", (WR, "    tep = Path(ra" + _THOAT + ")" + NL, T52))
them("x4-nem", "x4_t4_bytes_ra", (WR, "    tep = Path(ra if ra.isascii() else os.fsencode(ra))" + NL, T52))
for _t, _f in (("nfd", "NFD"), ("nfkd", "NFKD")):
    them("x4-nem", f"x4_t4_{_t}_ra", (WR, "    import unicodedata" + NL + f'    tep = Path(unicodedata.normalize("{_f}", ra))' + NL, T52))

# ======================= J-T5 — mọi chỗ dùng `tep` ở T5 ngoài `write_bytes` =======================
X5_GO = "    if tep.exists() or tep.is_symlink():" + NL + "        tep.unlink()" + NL
X5_MK = "    tep.parent.mkdir(parents=True, exist_ok=True)" + NL
X5_IN = ('    return dong + [f"M' + chr(0x1EA2) + 'NH {k}/{n}: {len(cac_ten)}/{len(cac_ten)} ' + chr(0x111) + chr(0x1ED9) + "t bi"
         + chr(0x1EBF) + "n b" + chr(0xE1) + "n k" + chr(0xED) + "nh 1 " + chr(0xB7) + ' ghi {tep}"], 0' + NL)
for _t, _e in (("nfkc", "unicodedata.normalize('NFKC', str(tep))"), ("strip", "str(tep).strip()"),
               ("cf", "''.join(c for c in str(tep) if unicodedata.category(c) != 'Cf')")):
    them("x4-t5", f"x4_t5_unlink_{_t}_ra", (X5_GO, "    import unicodedata" + NL + "    if tep.exists() or tep.is_symlink():" + NL
                                            + f"        Path({_e}).unlink()" + NL, T52))
    them("x4-t5", f"x4_t5_in_{_t}_ra", (X5_IN, "    import unicodedata" + NL + X5_IN.replace("ghi {tep}", "ghi {" + _e + "}", 1), T52))
them("x4-t5", "x4_t5_mkdir_nfkc_ra", (X5_MK, "    import unicodedata" + NL
                                      + "    Path(unicodedata.normalize('NFKC', str(tep))).parent.mkdir(parents=True, exist_ok=True)" + NL, T52))
them("x4-t5", "x4_t5_mkdir_normpath_ra", (X5_MK, "    Path(os.path.normpath(str(tep))).parent.mkdir(parents=True, exist_ok=True)" + NL, T52))
them("x4-t5", "x4_t5_exists_nfkc_ra", (X5_GO, "    import unicodedata" + NL
                                       + "    if Path(unicodedata.normalize('NFKC', str(tep))).exists() or tep.is_symlink():" + NL
                                       + "        tep.unlink()" + NL, T52))
them("x4-t5", "x4_t5_symlink_nfkc_ra", (X5_GO, "    import unicodedata" + NL
                                        + "    if tep.exists() or Path(unicodedata.normalize('NFKC', str(tep))).is_symlink():" + NL
                                        + "        tep.unlink()" + NL, T52))

# ======================= J-TV — thành viên ngoài R698, ở từng tầng hạ nguồn =======================
for _t, _c in (("u2063", "0x2063"), ("tag20", "0xE0020"), ("fwa", "0xFF41")):
    _e = f'ra.replace(chr({_c}), "")'
    them("x4-tv", f"x4_t2_{_t}_ra", (MAIN_RA, MAIN_RA + f"        ra = {_e}" + NL, T54))
    them("x4-tv", f"x4_t3a_{_t}_ra", (_GOI_NEN, _GOI_NEN.replace("(k, n, ra, ten,", f"(k, n, {_e}, ten,", 1), T54))
    them("x4-tv", f"x4_t3b_{_t}_ra", (_GOI_THUONG, _GOI_THUONG.replace("(k, n, ra, ten,", f"(k, n, {_e}, ten,", 1), T54))
    them("x4-tv", f"x4_t4_{_t}_ra", (WR, f"    tep = Path({_e})" + NL, T52))
    them("x4-tv", f"x4_t5_{_t}_ra", (_W5, f'    Path(str(tep).replace(chr({_c}), "")).write_bytes((', T52))
```
