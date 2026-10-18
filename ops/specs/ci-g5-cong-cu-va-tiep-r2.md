# ĐẶC TẢ — `CI-G5-CONG-CU-VA-TIEP` (`wp698`) — revision 2, ĐÓNG BĂNG

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp698` (ID bền `wp<issue>`, protocol §3.2); tên đọc được: `CI-G5-CONG-CU-VA-TIEP`. Hai tên cùng chỉ một packet; lease dùng tên nào cũng phải kèm `packet_issue: 698`. |
| `revision` | **2** |
| `thay_the_cho` | **r1**: `ops/specs/ci-g5-cong-cu-va-tiep-r1.md`, sha256 `3a55526305e17cf06c644e2e3448cb8720aa67e8d6c0cab571d8e49dac974996`, commit `dcc2cbcd404856dfc9f878478b054198d1f46ca1`. Thứ định danh r1 là **cặp băm này**, không phải tên nhánh chứa nó. r1 bị review lượt 1 trả `changes_requested` (hàng dưới), nên không đi tới xác nhận closure Q10; mọi closure, lease và `spec_hash` từ nay neo **r2**. r2 không sửa byte nào của r1. |
| review của r1 | **Lượt 1**, reviewer Claude Sonnet 5.5 chạy bằng subagent: `verdict: changes_requested`, `reviewed_sha: dcc2cbcd404856dfc9f878478b054198d1f46ca1`, **0 P1 · 5 P2 · 3 P3 = 8 lớp**. Tệp `VERDICT.md` sha256 `c825a405a9897a21a356c5c721af1ce703f348d3972dd6c07b5a6b922f2f2133`; `HINT.patch` (chỉ văn bản đặc tả, không có mã `ops/cong_cu_test.py`) sha256 `b330820068a6d710351bbfd912e364b224759a533c8de59192b7a5ba0e95a641`. Verdict đã đăng trên #698; ID comment **KHÔNG ĐO ĐƯỢC** từ phiên soạn r2 (phiên này không đọc lại GitHub). Nguồn có thẩm quyền là tệp có băm, không phải bản chiếu. Cách r2 đóng từng lớp: **§0**. |
| `packet_issue` | **#698** (object ID `5646961843`, tạo 2026-09-30T13:09:12Z). Issue và hai comment quyết định (`5912199805`, `5914438647`) đều do **phiên agent đăng hộ chủ kho** bằng credential chủ kho. Vì vậy `author_association: OWNER` không chứng minh chủ kho tự gõ; tư cách của chúng là lời khai có neo (#566). |
| `mission_issue` | RỖNG. #698 không khai Mission. Packet mẹ #668 cũng không khai (đặc tả `ops/specs/CI-G5-CONG-CU-CHIA-MANH-r1.md`). Thẩm quyền của closure do đó đi qua quyết định Q10 (§11). |
| `nguon_cap_viec` | Chỉ thị chủ kho, nguyên văn: *"#668: mở packet tiếp nối cho F48–F50"*, neo ở #668 comment `5911957306` và thân #698. Nguồn phát hiện: verdict cross-review **lượt 22** của phiên `session_01VYtkBy…`, #668 comment `5911284002` (12:27:04Z 30-09). Verdict này mang nhãn `advisory_review`, kết luận `changes_requested` với 0 P1 · 2 P2 · 1 P3, `reviewed_sha` là `8d7faef`, và commit ấy **chưa được đẩy** lên GitHub. Executor và reviewer: #698 comment `5912199805`, nguyên văn *"Chọn opus 5.5 executor. Reviewer để sonnet 5.5 xem"*. **Quyết định chủ kho cho r1:** #698 comment `5914438647`, tạo 2026-09-30T15:30:26Z, gồm hai lượt trả lời trong phiên lúc 15:28:25Z và 15:30:09Z (§11). **r2:** phiên điều phối giao soạn revision 2 theo verdict lượt 1; những chỗ r2 tự quyết thay cho chủ kho được liệt ở §11.1 và chỉ có hiệu lực khi comment Q10 xác nhận closure của r2. |
| `objective` | Đóng các khe đo trong `ops/cong_cu_test.py` mà phép đo trên nền `fc852ff` tái hiện được (§1). **(B)** Bốn bộ đọc giá trị ngoài của lớp B — `bk`, `mh`, `ra` của `_doc_che_do` và `head` của `_van_tay` — không có ô bắt các phép chuẩn hoá trước khi nhận: NFKC, bỏ Cf, bỏ TAB, bỏ Zs ngoài ASCII, bỏ Cc, bỏ dấu kết hợp, theo **mọi vị trí** và **mọi thành viên** của từng họ ký tự. r2 đổi cách làm từ "chọn ô tay" sang **miền dẫn xuất** (§5 M1): mỗi giá trị hợp lệ chuẩn, chèn hoặc thay đúng một ký tự của tập điểm mã `D698` (định nghĩa bằng thuộc tính Unicode, không liệt kê), so với oracle độc lập. **(C)** `ra` không có ô cho các phép đường dẫn (`normpath`, `expanduser`, `expandvars`, bỏ `./` đầu, bỏ `/` cuối…) (M2). **(D)** Nhánh mảnh của `main` không có điểm lực lượng cho vị từ đếm một biến lẫn nhiều biến: r2 quét trọn ba trục và thêm lưới **tích biên** (M3). **(E)** Tập ngoại lệ mà `_van_tay` bắt không có ô nào ngoài tập bắt, nên mở rộng tập bắt không bị đo (M5). Mỗi họ đường vào có ít nhất một đột biến canh trong `DOT_BIEN`, chỉ đúng ca đích giết nó bằng `TinHieuChotCa`, bán kính 1; và **mọi** dò của tập dò đóng ở Phụ lục C thuộc A1–A3, A8 phải bị giết khi nghiệm thu, trừ đối chứng và dò tương đương khai đích danh ở §2. Lớp (A), tức registry năng lực ngoài cửa sổ (F48), **không** thuộc packet: nợ `registry-nang-luc-ngoai-cua-so` (Q1). Hai bộ đọc ngoài lớp B (đầu tệp mảnh của `_gom_manh`, `CONG_CU_TEST_TIEN_TRINH`) được đo và ghi nợ, không vào mục tiêu (§2, §11.1). |
| `review_class` | **`sensitive`**: bộ test gate G5 có vòng đột biến tự kiểm, cùng lớp với #668. Fail-closed theo protocol §8. |
| `risk` | **`sensitive`**: cùng lý do trên. |
| `executor` | `claude`, model Claude Opus 5.5 (`claude-opus-5-5`), theo comment `5912199805`. Effort do phiên tự khai; từ ngoài là **KHÔNG ĐO ĐƯỢC**. |
| reviewer | Claude Sonnet 5.5, **chạy bằng subagent** trong phiên điều phối (quyết định chủ kho, §11 Q6). Chỉ mô tả hướng sửa, không đính patch-as-hint chứa mã (Q14). `HINT.patch` của lượt 1 chỉ sửa văn bản đặc tả; r2 áp nó ở bước đầu rồi sửa tiếp (§0 ghi chỗ nào của HINT bị r2 thay). |
| assurance đạt được | **`review_deferred`.** Hai lý do độc lập. (1) Reviewer tự khai chạy bằng subagent, tức `model_reviewer_identity.che_do` chứa `subagent`. Khi đó `_thieu()` của `ops/bien_nhan_v2.py` từ chối mọi mức trong `ASSURANCE_CAN_DOC_LAP` (`cross_approved`, `same_provider_approved`, `human_audited`), nên biên nhận chỉ được ghi `review_deferred`. (2) Dù chạy phiên độc lập, `cross_approved` cũng không đạt được, vì executor và reviewer cùng họ Claude (protocol §8 mục 1; `ops/bien_nhan_v2.py` từ chối `cross_approved` khi hai bên cùng họ model). **Cổng land là `human_audited`** do chủ kho audit (§8: `sensitive` phải có `cross_approved` hoặc `human_audited`). |
| ngưỡng review | **0 P1 · 0 P2 · 0 P3**. Không giới hạn số vòng (Q5). Trần canon trục VÒNG áp cho packet này là trần của **ADR-0048** (Accepted 2026-09-12), vì đặc tả đóng băng **sau** mốc ấy; ADR-0048 thay đúng con số trục VÒNG của ADR-0043, còn ba trục, trần độc lập và luật `nang_tran` vẫn là của ADR-0043. Con số chỉ có một chỗ ở là ADR-0048; tệp này chỉ **chép** nó vào `tran_cu` của khối `nang_tran` dưới đây vì ADR-0043 đòi trường ấy. Vượt trần là có chủ đích; khối có hiệu lực từ vòng review hợp lệ đầu tiên vượt `tran_cu`. |
| `environment` | **`cloud`**. Mục tiêu r2 gồm ô thuần, miền dẫn xuất và giàn giả trong một tệp test. r2 không đo đồng hồ ngủ máy và không cần quyền tạo symlink, vì lớp (A) là lớp phụ thuộc năng lực symlink và đã ra ngoài packet. **Không chạy Windows** (quyết định chủ kho, Q8), nên đường Windows của các ô mới không được đo; đây là nợ `windows-chua-do-o-moi-wp698`. |
| `depends_on` | **Chặn cấp lease: lease `wp671-windows-bash-nen-escape-r1-g2-claude` (#671).** Lease này giữ `ops/bash_nen.py` và `ops/cong_cu_test.py` tới `2026-10-01T03:35:00Z`. Tệp lease nằm ở `refs/remotes/origin/ops/cap-lease-671-g1` (commit `1235a32`). Chỉ cấp lease `wp698` khi cả năm điều kiện dưới đây thoả **và được đo lại lúc cấp**; số trong ô này không thay được phép đo lúc cấp. (1) So `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`) theo **tập tên VÀ OID**: thiếu cục bộ 0, lệch OID 0. Không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. (2) `python ops/lease_publish.py ai-dang-giu ops/cong_cu_test.py` ra `NGƯỜI_GIỮ 0`, rc=0. Phải chạy trên clone mà mọi nhánh cục bộ đều không tụt sau `origin` và không nhánh nào khai upstream đã mất; nếu không, bộ quét fail-close `rc=12` trước khi kịp đếm người giữ (xem "Lịch sử đo" ở cuối ô này). (3) Nếu #671 land trước và đổi `ops/cong_cu_test.py` thì phải **dời nền bằng revision mới trước khi cấp**, không cấp trên nền cũ. Nhánh ứng viên `claude/wp671-windows-bash-nen-escape-g1` @ `bd6ad5d` đổi tệp này +163/−22 so với nền `89fc4fa` của nó (đo lại 15:41:32Z 30-09). (4) Chủ kho đã xác nhận closure bằng một comment trên #698 neo `spec_hash` của **tệp này (r2)** (Q10), và lease neo đúng `spec_hash` ấy. (5) Không có lượt review nào đang chạy trên write set. **Hiện trạng đo 15:40:23Z–15:40:36Z 30-09** (clone sạch, `origin` = GitHub, HEAD = `origin/master` = `fc852ff`): máy chủ 459 ref, cục bộ 459, thiếu cục bộ 0, thừa cục bộ 0, lệch tên+OID 0. `ai-dang-giu ops/cong_cu_test.py` ra `NGƯỜI_GIỮ 1: wp671-windows-bash-nen-escape-r1-g2-claude` (nhãn `CÒN_HẠN`), rc=11, kèm 54 dòng `HẾT_HẠN`. Điều kiện (2) **chưa thoả**. Lịch sử đo: lúc 15:04:45Z–15:05:09Z có 458/458 ref và cùng người giữ; lúc 14:43:27Z `ai-dang-giu .github/workflows/ci.yml` ra `NGƯỜI_GIỮ 0`, rc=0. Cũng tại 14:4xZ, kho dùng chung của phiên điều phối cho `rc=12` (`KHÔNG_XÁC_ĐỊNH`: một nhánh cục bộ khai upstream `refs/remotes/origin/ops/spec-lease-id-ep-kieu-yaml`, mà ref này không còn); đó là lỗi của kho cục bộ, không phải kết quả về người giữ. Phiên soạn r2 **không** đo lại ô này (không cấp lease ở bước soạn đặc tả); mọi số trong ô là của lượt soạn r1. |
| nền nghiệm thu | **`fc852fff7da37f1669569572b79571446e61c294`** (merge PR #697, bookkeeping #668), theo quyết định chủ kho Q11. Đây là **nền bất biến** để đo diff và nghiệm thu. Bản nháp trước r1 dùng `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (merge PR #696). Đo 15:31:57Z 30-09: `git rev-parse 423b4ba:ops/cong_cu_test.py fc852fff7da37f1669569572b79571446e61c294:ops/cong_cu_test.py` cho hai lần cùng blob `9edea6b1629b46f27758b2073e74210dc73495b7`, và `git diff --quiet 423b4ba fc852fff7da37f1669569572b79571446e61c294 -- ops/cong_cu_test.py` cho rc=0. Hai nền khác nhau ở 66 tệp, tất cả là hồ sơ: `ops/land/` 23, `ops/leases/` 3, `ops/reviews/` 39, `ops/specs/` 1 (`git diff --name-only 423b4ba fc852ff`). **Đo lại lúc soạn r2**: 22:24:51Z 30-09, `git ls-remote origin refs/heads/master` = `fc852fff…`; **03:09:18Z 01-10** = `20ec8d5d0e86cb7dc01f202c7596407a957e5961` (merge PR #689, commit lúc 2026-10-01T00:55:21Z, sau merge PR #692). Fetch vào một kho tạm: `git diff --name-only fc852ff 20ec8d5` = đúng 2 tệp, `ops/land/pr684-wp677-land-evidence.yaml` và `ops/lease_publish_test.py`; `git rev-parse 20ec8d5:ops/cong_cu_test.py` = `9edea6b1…` (trùng nền) và `git diff --quiet fc852ff 20ec8d5 -- ops/cong_cu_test.py` rc=0. `origin/master` đã đổi nhưng **không chạm write set**, nên nền nghiệm thu giữ `fc852ff` theo Q11, không dời; nền tiếp nối lúc cấp lease phải khai riêng (dòng dưới). Mọi phép đo ở §1.8 chạy trên bản sao `fc852ff` (blob `ops/cong_cu_test.py` = `9edea6b1…`, đo lại bằng `git hash-object`). Nền tiếp nối (continuation base) là `origin/master` lúc cấp lease; nếu nó khác `fc852ff` thì lease phải khai riêng, và nếu nó đổi `ops/cong_cu_test.py` thì phải dời nền bằng revision mới trước khi cấp (cùng lý lẽ với S3). Diff nghiệm thu đo trên `ops/cong_cu_test.py` so với `fc852ff`, cộng với điều kiện A4-f. |
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

Khối này chỉ nâng trần **trục VÒNG**. Hai trục kia của ADR-0043 (LỜI GỌI `codex_review_calls_used`, ATTEMPT) không bị nâng. Số 2 trong khối `nang_tran` của tiền lệ `wp461-be-mat-thu-hai-cua-codex-exec-1g9-claude-20260925` là trần **LỜI GỌI** (khối ấy khai `truc: loi_goi`), không phải trần vòng; tiền lệ cùng họ `…-1g7-…` ghi rõ `truc_vong_ghi_chu: 'Truc VONG theo ADR-0048 = 10 cho spec dong bang tu 2026-09-12; khong doi, khong nang o day.'` (đo lại lúc soạn r2 bằng `grep -n`). Khối **không** gỡ checkpoint theo lớp của protocol §12 (xem S6). Đo lúc soạn r2: `grep -c nang_tran` trong `ops/lease_publish.py` và `.claude/dev/packet_loop.py` ra 0 và 0. Tức không có cổng máy nào đọc khối này; ADR-0048 tự khai đúng điều đó và sửa lời khai ngược của ADR-0043 ("thiếu khối thì cổng đăng lease từ chối"). Khối này là hồ sơ thẩm quyền, không phải chốt máy; người cấp lease và reviewer kiểm nó **bằng tay**.

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit
đóng băng: `sha256sum ops/specs/ci-g5-cong-cu-va-tiep-r2.md`, không loại dòng nào. Giá trị
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
| `required_checks` | Trên PR, tại exact head. PR chỉ được mở **một lần**, khi review đã đạt 0/0/0; không chạy CI trong vòng lặp (Q7). (a) Bốn context bắt buộc của ruleset `bao-ve-cong-dang-lease` (id `20856202`, đọc lại qua REST lúc 15:40Z 30-09, `updated_at` không đổi so với lần đọc 14:44:35Z): `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, `gate-cong-cu-gop (ubuntu-latest)`. (b) Tám job mảnh, từ `gate-cong-cu (ubuntu-latest, 0)` tới `gate-cong-cu (ubuntu-latest, 7)`; tên job lấy nguyên văn từ lượt hậu-merge `36696528580`. (c) `gate-registry (ubuntu-latest)` với rc=0. Theo quyết định Q9, nếu job này đỏ **vì hết trần** trên một run của PR #698 thì (c) được coi là đạt khi (a) và (b) xanh; phải ghi nợ có neo `gate-registry-het-tran-wp698` kèm run ID/job ID. Quyết định này chỉ áp cho các run của PR #698, và **chỉ miễn (c)**: nguyên văn Q9 nói về `gate-registry`, không nói về (d) hay (e), nên (d) và (e) vẫn bắt buộc. Muốn miễn (d) thì phải có quyết định chủ kho riêng (§11.1). **Định nghĩa tác nghiệp của "đỏ vì hết trần"** — ĐẠT khi cả ba điều sau đúng trên log job `gate-registry` của run ấy: (1) có **đúng một** dòng `CI_DANG_KY … ĐỎ`, và nó là `CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐỎ — LỖI HẠ TẦNG: hết giờ <n> giây, rc=-9`; (2) không dòng `CI_DANG_KY` nào khác mang `ĐỎ` (dòng hợp lệ in `ĐẠT` hoặc `CÁCH LY`); (3) dòng tổng là `TỔNG: ĐỎ` và chỉ do mục ở (1). Tiền lệ có trong kho: `ops/land/pr696-wp668-provenance/trich-log.txt` — job `109832781748` của run `36696528580` có dòng 1962 `CI_DANG_KY_KE_HOACH ops/nhanh_don_duoc_test.py: day_du — diff chạm .github/workflows/ci.yml, ops/cong_cu_test.py`, dòng 2438 `…CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐỎ — LỖI HẠ TẦNG: hết giờ 4500 giây, rc=-9`, dòng 2440 `TỔNG: ĐỎ`; run PR `36689211190` có dòng 2590 `CI_DANG_KY ops/nhanh_don_duoc_test.py: ĐẠT rc=0`. PR #698 cũng sẽ chạy chế độ đủ: `.claude/dev/ci_dang_ky_test.py:730` khai `TIEN_TO_CHUNG = ("ops/cai_", "ops/cong_cu")`, và `ops/cong_cu_test.py` khớp tiền tố ấy (đo lúc soạn r2). Thời lượng hai run ấy (reviewer lượt 1 ghi 66,5 phút và 83,3 phút) **KHÔNG ĐO ĐƯỢC** ở r2: trích log trong kho đã bỏ dấu thời gian. (d) Job `thu-hoi` của `.github/workflows/ops-thu-hoi-admission.yml` (`pull_request_target` vào `master`, các kiểu `opened` `reopened` `synchronize` `ready_for_review` `edited`). (e) **Không** có lượt Windows (Q8). |
| `land_obligations` | 1. Chủ kho audit (`human_audited`) trên exact head, cộng uỷ quyền merge bền. Không phiên nào tự approve hay tự merge. 2. Verdict mọi lượt review và biên nhận v2 của chúng vào `ops/reviews/`, theo mẫu #668, với nhãn `review_deferred`; gồm cả lượt review đặc tả r1 và r2. 3. Hồ sơ land vào `ops/land/`, theo tiền lệ PR #691 và #697. 4. Đặc tả (r1 và r2) và lease vào master bằng một PR bookkeeping. 5. Thu hồi lease sau land bằng rút hạn. **Không** viết bia mộ `da_bi_thay_the` vào lease đã hết hạn (bài học run `35519177197`/`35519243379` trong `CLAUDE.md`). 6. Đóng #698 và đăng comment nối trên #668. 7. Ghi nợ có tên vào trường `no_con_mo` của hồ sơ land ở mục 3 (tiền lệ: `ops/land/pr696-wp668-land-evidence.yaml`, trường `no_con_mo`): `registry-nang-luc-ngoai-cua-so` (Q1); `so-tien-trinh-nhan-fullwidth` (Q2; gồm cả khe mức đo `t_cf`, `t_tab` của §1.8.6); `windows-chua-do-o-moi-wp698` (Q8); `gom-dau-manh-chuan-hoa-wp698` (§2, §11.1); và `gate-registry-het-tran-wp698` nếu xảy ra (Q9). Chủ thể ghi: phiên soạn hồ sơ land. 8. Hồ sơ lượt 22 vào một nhánh `ops/**` kèm băm (Q13). Chủ thể: **người chủ kho chỉ định**, vì executor không có các tệp ấy (phiên soạn r1 và r2 chỉ có băm của chúng trong comment `5911284002`). Việc này **không** chặn land. |

Lease phải **chép** đúng các giá trị trên và khối `nang_tran`, không thêm, không đổi. Lệch ⇒ **DỪNG**.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm. Tập dò đóng
ở Phụ lục C có 221 dò: 53 dò của reviewer lượt 1 chép nguyên văn, cộng 168 dò do chính phiên soạn
liệt kê từ mã; **danh sách ấy vẫn có thể thiếu**. Reviewer tìm ra được một đường sống ngoài
danh sách thì đường ấy tính là finding (protocol §8, "bảng bằng chứng phải tự khai giới hạn").
Ba đời ứng viên tham chiếu IMP-R2, IMP-R2F, IMP-R2G (§1.8) là công cụ đo của phiên soạn, **không** phải bản giao, và mã của
chúng **không** nằm trong tệp này (Q14 áp theo tinh thần: không có đáp án dựng sẵn cho executor).
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 0. Thay đổi so với r1 (theo tám lớp của review lượt 1)

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

§1.1–§1.7 là phép đo của lượt soạn r1, giữ nguyên chữ; chỗ nào r2 đo lại hoặc đo thêm thì ở §1.8.

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
làm `m_cf_tag_bk` sống ở đó (r2 không đo lại IMP-SWEEP); trong 8.606 điểm mã ấy có 120 Cf (TAG), 886 Mn, 782 Ll và 704 Lu (chữ toán
học có NFKC về ASCII), 3.874 So. **Vét cạn cho các dò tập con NFKC** (cả hai bản Python, cùng kết quả): với mỗi điểm mã `c` của tập
con có NFKC(c) ≠ c, đếm những `c` mà NFKC(c) là đoạn con khác rỗng của `manh` (với `bk`), chỉ gồm chữ
số ASCII và `/` (với `mh`), hoặc chỉ gồm hex thường (với `head`) — `No`
đối với `bk`: **0**; "khác trong BMP" đối với `mh`: **0**; mọi cặp (tập con, bộ đọc) còn lại: từ 4 tới
137. Hai dò `m_nfkc_no_bk` và `m_nfkc_khac_bmp_mh` vì vậy **tương đương** với nền theo cấu tạo:
không đầu vào nào làm chúng lệch nền.

## 2. Đường vào: liệt kê HẾT trước khi vá

Áp bài học *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*: danh sách dưới đây do phiên soạn tự
dựng từ mã, không chép từ verdict. r1 dựng 24 đường sống trong 4 lớp; review lượt 1 chỉ ra 8 lớp /
52 biểu hiện mà danh sách ấy thiếu. r2 **không** vá theo 52 biểu hiện được chỉ: nó dựng lại danh
sách theo **ba trục** — bộ đọc × họ phép × (vị trí, thành viên) — rồi đo từng ô của tích ấy.

**Bộ đọc cùng họ** (đọc một giá trị do môi trường, tiến trình ngoài hoặc tệp đưa vào, rồi nhận hay
từ chối bằng so khớp). Trên nền, `grep -c -E` với các mẫu `os.environ`, `env.get`, `getenv` cho 61
dòng; bỏ các ca test tự đặt môi trường cho mình, các chuỗi đột biến và oracle `_mong_che_do`, còn
đúng hai chỗ đọc thật: `_doc_che_do` (:7468, ba biến) và `_so_tien_trinh_ban_kinh` (:7092). Cộng
hai bộ đọc không đi qua môi trường — stdout của `git` trong `_van_tay` và đầu tệp mảnh trong
`_gom_manh` — thành sáu:

| bộ đọc | hàm | lớp | r2 |
|---|---|---|---|
| `CONG_CU_TEST_BAN_KINH` (`bk`) | `_doc_che_do` | B | mục tiêu (M1) |
| `CONG_CU_TEST_MANH` (`mh`) | `_doc_che_do` | B | mục tiêu (M1) |
| `CONG_CU_TEST_MANH_RA` (`ra`) | `_doc_che_do` | B và C | mục tiêu (M1, M2) — lớp `ra-thieu-hang-chuan-hoa-lop-b` |
| stdout của `git rev-parse HEAD` (`head`) và tập ngoại lệ bắt | `_van_tay` | B và E | mục tiêu (M1, M5) |
| `CONG_CU_TEST_TIEN_TRINH` | `_so_tien_trinh_ban_kinh` | ngoài B | nợ `so-tien-trinh-nhan-fullwidth` (Q2) |
| đầu tệp mảnh (`head`, `sha256_test`) so với vân tay của chính tiến trình gom | `_gom_manh` | ngoài B | nợ `gom-dau-manh-chuan-hoa-wp698` |

Ranh giới lớp B: bộ đọc **cấu hình và vân tay của chính tiến trình**, đúng phạm vi F49 (§11.1 điểm 1).
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

- **Nền** (`fc852ff`): 205 dò sống, tức mọi họ đều có đường sống trước bản vá — tiêu chí
  không thể xanh trên nền.
- **IMP-MIN, IMP-GEN** (hai ứng viên "thoả chữ r1" của reviewer lượt 1): 184 và 138
  dò sống. Tiêu chí r1 xanh trên cả hai (reviewer lượt 1 đo: 16/16 dò mục tiêu của r1 bị giết đúng
  ca đích trên cả hai); tiêu chí r2 đỏ trên cả hai.
- **IMP-R2F** (Python 3.12.3): 2 dò sống ngoài hai hàng Z. Hai dò ấy là `m_nfkc_no_bk` và `m_nfkc_khac_bmp_mh`, đúng hai dò mà phép vét cạn ở §1.8.8 chứng minh tương đương (không điểm mã nào của tập con có NFKC là đoạn con hợp lệ của bộ đọc) — chúng sống vì không thể chết, không vì thiếu ô. Mọi dò còn lại của T-B, T-C, T-D, T-E: GIẾT đúng ca đích, bán kính 1/56, trừ đối chứng `s_ra_realpath` giữ nguyên hạng KHÁC (giết `t53` và `t54`, bán kính 2) như trên nền — cùng hình dạng với `c49_ra_abspath` của Phụ lục A.
- **Đối chứng** (bị giết ngay trên nền, không đo răng của bản vá): 10 dò — `s_bk_strip` (ô nền ` manh`), `s_bk_lower` và `s_bk_casefold` (ô `MANH`), `s_mh_digit_d` (ô chữ số Ả Rập `so_la`), `m_cc_bk` và `m_cc_mh` (ô `manh` và `0/8` kèm xuống dòng — LF là Cc), `s_ra_realpath` (bán kính 2), `s2_hong_lt_n`, `z_exc_oserror_only`, `z_exc_subproc_only`. `s_bk_casefold` trả lời mục "casefold trên dạng fullwidth: chưa đo" mà HINT để lại: casefold bị ô `MANH` của nền giết; dạng fullwidth hoa casefold ra fullwidth thường, vẫn bị từ chối, nên không mở đường nào ngoài NFKC (đã có dò riêng).
- **Tương đương** (không đầu vào nào phân biệt được với nền): `m_nfkc_no_bk`, `m_nfkc_khac_bmp_mh` (vét cạn §1.8.8, cả Python 3.11.15 lẫn 3.12.3).

Lớp A (F48) giữ nguyên như r1: 8 dò sau/trước cửa sổ sống, đối chứng `c48_trong_cua_so` bị giết
(Phụ lục A); **không** vào r2, nợ `registry-nang-luc-ngoai-cua-so` (Q1).

## 3. `write_set`

- `ops/cong_cu_test.py`

Không có đường dẫn nào khác. Căn cứ: mọi ca đích (`t53`/`t54`), mọi miền ô (`_luoi_che_do`,
`_luoi_git`, `bang_env`, miền dẫn xuất M1, kịch bản của `_in_tu_kiem_main`), bảng `DOT_BIEN` và
mọi hàm bị đột biến đều nằm trong tệp này. `ci.yml` không đổi, vì r2 không thêm job hay biến môi
trường. `.claude/dev/ci_dang_ky_test.py` cũng không đổi, vì hình dạng G5 giữ nguyên. Bản thân đặc
tả này và các phụ lục của nó là hồ sơ của lượt soạn spec, **không** thuộc write set của lượt thi hành.

## 4. `ngoai_pham_vi`

| thứ | lý do |
|---|---|
| Lớp A (F48 và đường (e)) | Chủ kho quyết không gộp (Q1). Ghi nợ `registry-nang-luc-ngoai-cua-so`; muốn đóng thì mở packet riêng. |
| `_so_tien_trinh_ban_kinh`: mức mã nhận fullwidth và ném ở chữ số mũ; mức đo không có ô cho Cf/TAB | Chủ kho quyết ghi nợ `so-tien-trinh-nhan-fullwidth` (Q2). r2 đo thêm hai dò mức đo (`t_cf`, `t_tab`, §1.8.6): SỐNG 2/2 trên nền. Cả hai thuộc cùng nợ ấy; A4-d vẫn cấm đổi thân hàm. |
| Đầu tệp mảnh của `_gom_manh` (so `head`/`sha256_test` với vân tay của chính tiến trình gom) | Bộ đọc ngoài lớp B theo định nghĩa ở §2 (nó so bằng, không đọc cấu hình). r2 đo bốn dò (`g_*`, §1.8.6): SỐNG 4/4 trên nền. Ghi nợ `gom-dau-manh-chuan-hoa-wp698` (§11.1). |
| Patch-as-hint chứa mã và các hint của lượt 22 | Chủ kho quyết không dùng patch-as-hint; reviewer chỉ mô tả hướng (Q14). `HINT.patch` văn bản của review lượt 1 đã được áp và sửa tiếp (§0). Hồ sơ lượt 22 đưa lên nhánh `ops/**` chỉ để làm hồ sơ, không làm đầu vào (Q13). |
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
     S2 = 120.888 (Python 3.11.15); S1 = 673.234, S2 = 122.148 (Python 3.12.3). Ví dụ trên 3.11.15: S1 = (19.588 + 3) × (9 + 7 + 11 + 7) = 666.094 (vị trí chèn cộng thay của `manh`, `3/8`, `15/16`, `a/b`); S2 = 2 × 19.588 × 3 + (13 + 3) × (81 + 129) = 120.888. Ngoại lệ không
     phải `ValueError` trong `_doc_che_do` làm tiến trình con chết như `doc` hiện có, tức
     `tin_dung_gia`, không phải `giet_that`.
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
2. **M2 (lớp C — phép đường dẫn và chuỗi trên `ra`).** Miền M1 đã phủ các phép một ký tự trên
   `ra`. Thêm vào `_luoi_che_do` các ô `ra` có **cấu trúc**, mỗi phép một ô riêng làm đổi giá trị
   (không ô nào phải bị hai phép cùng đổi): `a/./b//c` và `a/../b` (`normpath`), `~/x`
   (`expanduser`), `$HOME/x` (`expandvars`), `./x` (bỏ `./` đầu), `x/` (bỏ `/` cuối), `a//b` (gộp
   `//`, `str(Path(…))`), `a` + chr(92) + `b` (đổi chéo ngược thành `/`), `X/Y.TXT` (`lower`,
   `casefold`), `M` + U+1EA3 + `nh` (NFD), `Ma` + U+0309 + `nh` (NFC), `x` + U+00A0 (Zs cuối). Kỳ
   vọng nguyên văn từ `_mong_che_do`. `HOME` ghim như M1.
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
5. **M5 (lớp E — tập bắt ngoại lệ của `_van_tay`).** Thêm vào `_luoi_git` ba ô `(0, "", kiểu)` với
   kiểu **ngoài** tập bắt `(OSError, subprocess.SubprocessError)`: `ValueError`,
   `UnicodeDecodeError` (lớp con của `ValueError`; là ngoại lệ thật mà `subprocess.run(…,
   text=True)` ném khi stdout không giải mã được — đo: byte 0xFF qua `printf` ⇒ `UnicodeDecodeError`,
   `isinstance(…, ValueError)` đúng, `isinstance(…, (OSError, SubprocessError))` sai) và `RuntimeError`, cộng hàm dựng tương ứng trong
   bảng `nem` của cửa con. Kỳ vọng: ngoại lệ **lọt** khỏi `_van_tay`, cửa con ghi `NEM:<tên kiểu>`.
   Kỳ vọng dựng độc lập, không gọi `_van_tay` (IMP-R2F thêm vào `_mong_git` một nhánh cho ba kiểu
   lọt). Như vậy hợp đồng "tập bắt CHÍNH XÁC là `(OSError, SubprocessError)`" được đo từ hai phía:
   ba ô sẵn có (`OSError`, `SubprocessError`, `TimeoutExpired`) bắt thu hẹp, ba ô mới bắt mở rộng.
   Không đổi thân `_van_tay` (A4-d). Muốn `_van_tay` bắt thêm kiểu nào là đổi mã, ngoài phạm vi (S1).

**Bảng canh `DOT_BIEN`.** Thêm đúng **43** mục canh: 16 mục của r1 (M1–M3 cũ) và 27 mục r2. Mỗi
hàng trong lớp của bảng họ ở §2 có ít nhất một canh, trừ hàng "B phép khác": mọi dò ở đó là đối
chứng, trừ `s_mh_nfkd`, vốn bị đúng các ô fullwidth giết như canh `e49_nfkc_mh` (IMP-MIN, chỉ có ô
fullwidth cho `mh`, đã giết nó — §1.8.2). Mỗi mục có **cùng mỏ neo và cùng phép thay** với dò ghi ở
cột "dò" (Phụ lục A hoặc Phụ lục C), cùng ca đích, và được đăng ký **vô điều kiện** trong một bảng
có sẵn nằm **trước** `_TRUOC_NANG_LUC`. Tên mục do executor đặt; handoff phải kèm bảng nối
`tên dò ↔ tên mục DOT_BIEN` đủ 43 dòng.

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

Vì sao không đăng ký trọn tập dò đóng (215 dò thuộc A1–A3, A8) vào `DOT_BIEN`: mỗi mục canh cộng một lượt chạy
56 ca vào mọi vòng bán kính; 215 mục đưa mảnh CI dài nhất lên khoảng 31,8 phút, vượt trần 30 phút của job (ƯỚC, §7), và vượt trần
300 dòng (S5): 43 hàng canh của IMP-R2G chiếm khoảng 106 dòng khi ngắt ở 120 ký tự, nên 215 hàng là khoảng 530. Tập đóng được đo **trọn** một lần ở nghiệm thu (A1–A3, A8); 43 canh là phần canh
hồi quy thường trực.

## 6. `nghiem_thu`

**Quy ước chung.** "Đột biến" nghĩa là chạy trên **bản sao tạm**, với `PYTHONDONTWRITEBYTECODE=1`,
và mọi thư mục đầu ra (tệp mảnh A5, jsonl của Phụ lục C) nằm **ngoài** cây checkout. Phân hạng
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

**Tập dò đóng** là Phụ lục C (sha256 c6a4db8b47fe246e8e173c13298a62310019809794ea322abcc94e1fdd922a36), chia theo tiêu chí bằng tên:

| tập | dò của Phụ lục C thuộc tập | số dò | tiêu chí |
|---|---|---|---|
| T-B | mọi dò không thuộc bốn tập dưới | 155 | A1 |
| T-C | tên kết thúc bằng `_ra` hoặc mở đầu bằng `s_ra_` hoặc `p_cf_ra_` | 41 | A2 |
| T-D | tên mở đầu bằng `s2_` hoặc `s3_` | 12 | A3 |
| T-E | tên mở đầu bằng `z_exc_` | 7 | A8 |
| ngoài lớp | tên mở đầu bằng `g_` hoặc `t_` | 6 | không (đo để khai, §2) |

Mỗi tập có **đối chứng** (dò bị giết ngay trên nền) và có thể có dò khai **TƯƠNG ĐƯƠNG** (không
đầu vào nào phân biệt được với nền) — cả hai được liệt kê đích danh ở §2 kèm phép đo. Dò đối
chứng phải giữ **nguyên hạng như trên nền** (GIẾT, hoặc KHÁC bán kính 2 như `s_ra_realpath`); dò tương đương không tính.

- **A1 (M1; bộ đọc `bk`, `mh`, `head`).**
  **ĐẠT KHI:** (i) 9 canh B toàn chuỗi của r1 và 13 canh r2 thuộc T-B (bảng canh §5) đều GIẾT
  `t53_…` trong A5; (ii) chạy Phụ lục C trên ứng viên, mọi dò của T-B trừ hai dò tương đương đều GIẾT
  `t53_…` (kể cả sáu đối chứng, vốn đã GIẾT trên nền); (iii) hợp đồng đếm của M1 khớp công thức (ca `t53` tự kiểm điều này; A4-a xanh là
  bằng chứng); (iv) phép đo ký tự nguồn của M1 bằng nền.
  **PHẢI ĐỎ Ở** (bằng chứng tiêu chí có răng, đo ở §1.8): nền `fc852ff` (T-B còn 149 dò
  SỐNG); IMP-MIN của reviewer lượt 1, tức bản "SAI-nhưng-thoả-chữ-r1" (133 dò SỐNG); IMP-GEN,
  tức bản "đúng chữ M1 của r1" (101 dò SỐNG). Hai ứng viên ấy qua A1 của r1 mà trượt A1 của
  r2 — đó là răng của lớp `a1-khong-do-vi-tri-thanh-vien`.
  **Bậc hai** (A1-ii), đo trên ứng viên bằng cách gỡ riêng một phần miền: (1) giữ nguyên từ r1 —
  gỡ nhóm điểm mã của **một** phép (NFKC | Cf | TAB) thì đúng 3 canh r1 của phép ấy SỐNG lại, còn
  canh r1 của hai phép kia vẫn GIẾT; ba nhóm không tách được bằng đầu vào ⇒ bộ tương đương ⇒ ĐỎ.
  (2) mới — mỗi canh r2 thuộc T-B khai **tập nhóm** K(c) mà gỡ đúng tập ấy thì c SỐNG lại (c chết vì
  chính phần miền được khai, không vì một ô tình cờ). Nhóm đặt theo thuộc tính (`cf`, `tab`, `cc`,
  `zs`, `dau`, `nfkc`) và **có thể giao nhau** — ví dụ U+00A0 vừa là Zs vừa có NFKC khác chính nó —
  nên handoff ghi rõ định nghĩa nhóm đã dùng. Handoff kèm bảng đo; r2 đo được cả hai phần trên
  IMP-R2-GO (§1.8.7), tức tiêu chí khả thi.
- **A2 (M2 và `ra` trong M1).** **ĐẠT KHI:** 2 canh C của r1 và 8 canh `ra` của r2 GIẾT `t53_…`
  trong A5; mọi dò của T-C trừ đối chứng (`s_ra_realpath`, giữ hạng nền) GIẾT trên ứng viên. **PHẢI ĐỎ Ở:** nền (40
  dò SỐNG), IMP-MIN (38), IMP-GEN (24). **Bậc hai:** gỡ riêng các ô cấu trúc `ra` của
  M2 thì đúng các canh `ra` mà miền M1 không giết được SỐNG lại (đo trên IMP-R2-GO: trong năm canh `ra` chạy dưới phép gỡ ấy, chỉ `s_ra_expandvars` SỐNG lại; bốn canh còn lại vẫn GIẾT vì miền M1 cũng giết chúng, §1.8.7).
- **A3 (M3).** **ĐẠT KHI:** 5 canh D của r1 và 4 canh D tích của r2 GIẾT `t54_…` trong A5; mọi dò
  của T-D trừ đối chứng GIẾT trên ứng viên. **PHẢI ĐỎ Ở:** nền (11 dò SỐNG), IMP-MIN,
  IMP-GEN (hai bản ấy không có tích: 8, 8 dò SỐNG). **Bậc hai:** gỡ riêng trục
  `bo_qua` ⇒ ba canh `bo_qua` của r1 SỐNG lại; gỡ riêng lưới tích ⇒ bốn canh D tích SỐNG lại; canh
  `hong`/`tien_kiem` của r1 bị cả trục lẫn tích giết, nên phải gỡ **cả hai** mới SỐNG lại (đo trên
  IMP-R2-GO: đúng như trên: `bq` ⇒ 3, `tich` ⇒ 4, `hong` một mình ⇒ 0, `hong,tich` ⇒ 1, `tk` một mình ⇒ 0, `tk,tich` ⇒ 1).
- **A4 (không hồi quy, không nới phạm vi).** Ứng viên và nền được đo trong **một** lệnh, cùng
  công cụ, cùng phiên bản Python. **ĐỎ KHI** một mục dưới đây đỏ trên ứng viên mà xanh trên nền:
  - (a) `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` ra `cong_cu_test: M/M đạt`,
    `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0. Nền đo lúc soạn r2 (Python 3.12.3, PyYAML 6.0.3,
    jsonschema 4.26.0 — đúng bản `ci.yml` ghim): `cong_cu_test: 56/56 đạt; tổng=56, bỏ qua=0, tiền kiểm bỏ qua=0`, `SỐ LIỆU: … đột biến=416 (giao mảnh) · lỗi đột biến=0 · … · cổng cây thật=ĐẠT`, rc=0, 175 s — tức có `jsonschema` thì `t2` chạy và đạt. Thiếu `jsonschema` thì `t2` bị bỏ qua
    (`bỏ qua=1`), như lượt đo của r1.
  - (b) `ruff check --select F ops/cong_cu_test.py` bằng **ruff 0.15.15** (bản `ci.yml` ghim), so
    theo **đa tập (mã, thông điệp)**, không theo số dòng: chèn dòng làm vị trí trượt mà vẫn là cùng
    một lỗi. Nền đo lúc soạn r2: đúng 1 lỗi, `F841 Local variable ci is assigned to but never used` ở :2606.
  - (c) `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) cho delta 0.
  - (d) `git diff fc852fff7da37f1669569572b79571446e61c294 -- ops/cong_cu_test.py` **không chạm
    thân** `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`,
    `_chay_1_ca`.
  - (e) Chạy Phụ lục E: số chỗ ghi `DOT_BIEN` **sau** dòng `_TEN_NANG_LUC = …` vẫn **= 0** (nền: 0).
    Bản vá không được mở rộng đường (e).
  - (f) `git diff --name-only fc852fff7da37f1669569572b79571446e61c294` (so với nền tiếp nối nếu
    lease khai khác) = `{ops/cong_cu_test.py}`, và `git status --short` của checkout không có tệp
    chưa theo dõi do phép đo sinh ra.
- **A5 (bán kính trọn).** Chạy 8 lượt `CONG_CU_TEST_MANH=k/8` với `CONG_CU_TEST_MANH_RA=<thư mục
  ngoài cây>/manh-k.txt` (k = 0…7), rồi `python ops/cong_cu_test.py --gop <thư mục ấy>`.
  **ĐẠT KHI:** ra `GOM MẢNH 8/8`, mọi dòng bảng là `ok`, `lỗi đột biến=0`, số đột biến
  **= 459** (416 + 43), **và** phép kiểm tên: nạp mô-đun nền và ứng viên, bộ sáu trường
  `DOT_BIEN` của cả 416 tên cũ y nguyên, tập tên thêm đúng bằng cột tên mục của bảng nối (43 tên).
  **ĐỎ KHI** có lượt rc ≠ 0, có dòng không `ok`, số lệch, một bộ cũ đổi hay mất, hoặc tập tên thêm
  khác bảng nối (đếm thôi không đủ: thay một đột biến cũ bằng một dò thừa vẫn ra cùng số).
- **A6 (review).** Reviewer Claude Sonnet 5.5 chạy bằng subagent, đưa verdict trên exact head, lặp
  tới **0 P1 · 0 P2 · 0 P3** (khối `nang_tran`); biên nhận ghi nhãn **`review_deferred`**. Chưa có
  `human_audited` của chủ kho thì không land. Tiêu chí này không có phép đo máy: nó là cổng thẩm
  quyền, không phải cổng hành vi.
- **A7 (M4).** Handoff liệt kê đầu ra của
  `grep -n -E "đã đóng|ĐÃ ĐÓNG|mọi |MỌI |trọn|TRỌN|không còn|KHÔNG còn" ops/cong_cu_test.py`
  giới hạn trong thân và chú thích của `t53`, `t54`, `_luoi_che_do`, `_luoi_git`, `_mong_git`,
  `_in_tu_kiem_che_do`, `_in_tu_kiem_main` và các hàm mới, kèm kết luận **giữ** hoặc **sửa** cho
  từng dòng. **ĐỎ KHI** còn một dòng mà §1 hoặc §1.8 đo thấy sai nhưng không có kết luận "sửa",
  hoặc một chỗ thêm mới không có chú thích neo #698.
- **A8 (M5).** **ĐẠT KHI:** 2 canh E GIẾT `t53_…` trong A5; mọi dò của T-E trừ đối chứng GIẾT trên
  ứng viên; hai đối chứng (`z_exc_oserror_only`, `z_exc_subproc_only`) vẫn GIẾT. **PHẢI ĐỎ Ở:** nền
  (5 dò SỐNG). **Bậc hai:** gỡ riêng ba ô ngoại lệ mới ⇒ hai canh E SỐNG lại (đo: 2/2 SỐNG lại).

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

`t53` và `t54` chạy trong **mọi** lượt đột biến. **Ước** tác động lên mảnh CI (không đo trên
runner): lượt hậu-merge `36696528580` có 8 mảnh 12,7–18,2 phút cho 416 đột biến, tức khoảng 52 đột
biến mỗi mảnh và 59–84 s mỗi lượt đột biến trên runner (4 tiến trình). Giả định thời lượng mảnh tỷ lệ
với (số đột biến × thời lượng một lượt), và tỷ lệ thời lượng một lượt trên runner bằng tỷ lệ đo ở
container: trung bình một lượt 56 ca của một dò, 4 tiến trình song song, là 29,8 s trên nền (162 dò) và 34,3 s
trên IMP-R2 (209 dò), Python 3.11.15, tỷ lệ ≈ 1,15. Khi ấy 459 đột biến cho mảnh dài nhất khoảng 23,1 phút (cộng
3,4–4,9 phút mỗi mảnh), dưới trần 30 phút của job. Đăng ký trọn 215 dò thuộc A1–A3, A8 thay cho 43
canh (631 đột biến) cho mảnh dài nhất khoảng 31,8 phút, **vượt** trần 30 — lý do định lượng của việc
chỉ đăng ký 43 canh. Tích đầy đủ của M3 (6612 kịch bản) ước cộng khoảng 22–37 s (chênh `t54` đo được 0,55–0,90 s cho 162 kịch bản mới, tức 3,4–5,6 ms mỗi kịch bản, nhân 6612) mỗi lượt `t54`; đó
là lý do M3 chỉ lấy tích biên.

## 8. Điều kiện dừng

- **S1:** cần sửa thứ gì ngoài `ops/cong_cu_test.py`, hoặc cần đổi thân một hàm liệt kê ở A4-d
  ⇒ DỪNG, handoff, revision mới.
- **S2:** lúc cấp lease, so tập tên+OID ref bị lệch, hoặc `ai-dang-giu ops/cong_cu_test.py` ≠
  `NGƯỜI_GIỮ 0`, hoặc chưa có comment chủ kho xác nhận closure neo `spec_hash` **của r2** (Q10)
  ⇒ không cấp.
- **S3:** #671 land trước và đổi `ops/cong_cu_test.py` ⇒ revision mới dời nền **trước** khi cấp.
- **S4:** một mục canh hay một dò của tập đóng chỉ chết bằng `tin_dung_gia` hoặc với bán kính > 1,
  và muốn sửa thì phải đổi mã ngoài phạm vi ⇒ DỪNG.
- **S5:** vượt ≤ 3 tệp hoặc ≤ 300 dòng thêm (ADR-0044 cho `sensitive`; chủ kho giữ mặc định, Q12)
  ⇒ DỪNG, hỏi chủ kho. Ước bằng ứng viên tham chiếu (§1.8.7): 1 tệp; IMP-R2G `git diff --numstat` = +191/−5 (dòng dài: 43 hàng canh viết một dòng mỗi hàng); ngắt ở 120 ký tự/dòng ra 266, bớt khoảng 10 dòng chỉ phục vụ đo bậc hai (hằng `_GO698`, bảng lọc nhóm, hàm `_n698`) ⇒ khoảng 256; cộng chú thích M4 mà IMP-R2G chưa có, ước 10–25 dòng ⇒ khoảng 265–280 dòng thêm, dưới trần 300 khoảng 20–35 dòng — biên mỏng. ƯỚC trên ứng viên tham chiếu, không phải bản giao. Không nới trần ở đây.
- **S6:** không có trần số vòng review ngoài trần trục VÒNG của ADR-0048, đã được nâng bằng khối
  `nang_tran` (Q5); vòng lặp dừng khi đạt 0/0/0. Hai quy tắc dừng của protocol §12 vẫn áp, chép
  đúng: (1) **tín hiệu không hội tụ** — với chuyển tiếp từ lượt r sang r+1, tỷ lệ = |F|/|U| (U là
  tập slug lớp còn mở cuối lượt r, F là phần của U được lượt r+1 xác minh ĐÃ VÁ THẬT); hai chuyển
  tiếp **liên tiếp** có tỷ lệ < 50% thì dừng vòng vá và đưa bằng chứng tới Review Rescue
  Checkpoint; (2) **checkpoint theo lớp** — một lớp xuất hiện ở **ba lượt review khác nhau** đòi xem
  lại cách làm tại checkpoint; ba biểu hiện của lớp trong cùng một lượt chỉ là một lần xuất hiện;
  revision hay cắt phạm vi **không** reset lịch sử ấy. Vì lịch sử không reset, cả ba lớp kế thừa ở §9
  đã quá ngưỡng trước packet này (hai lớp trong phạm vi: `doc-che-do-van-tay`, `main-luc-luong-gia-tri`); mỗi lần một lớp kế thừa xuất hiện lại trong review của packet
  (kể cả review đặc tả), phiên điều phối báo chủ kho kèm bảng lớp trước khi soạn revision hay vá
  tiếp. Review lượt 1 của r1 là một lần như thế (§9); comment Q10 xác nhận closure của r2 là chỗ
  chủ kho ghi rằng đã thấy bảng ấy.
- **S7:** `gate-registry (ubuntu-latest)` đỏ. Nếu đỏ đúng định nghĩa tác nghiệp "đỏ vì hết trần" ở
  `required_checks` (c) thì làm theo Q9: (c) được coi là đạt khi (a) và (b) xanh, ghi nợ có neo;
  (d) vẫn bắt buộc. Đỏ vì lý do khác ⇒ DỪNG.
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
| `doc-che-do-van-tay` | **≥ 5** trước packet: Codex lượt 12, 13, 14, 15, và F49 ở lượt 22. Thêm F46, mà số lượt **KHÔNG ĐO ĐƯỢC** vì hồ sơ phiên `session_01VYtkBy…` không có trong kho. **Review đặc tả wp698 lượt 1: +1** (ba lớp con `ra-thieu-hang-chuan-hoa-lop-b`, `a1-khong-do-vi-tri-thanh-vien`, `khai-khong-do-duoc-nhung-do-duoc`; ba biểu hiện cùng lượt tính một lần) ⇒ **≥ 6** | chú thích mã trên nền: F29 :8106, F31 :8110, F33 :8041, F30/F32/F34 :8144, F36 :2257; comment `5911284002`; VERDICT.md lượt 1 (sha256 `c825a405…2133`) |
| `main-luc-luong-gia-tri` | **≥ 3** trước packet: F42 (Codex lượt 19), F44 (lượt 20), F50 (lượt 22). F47 **KHÔNG ĐO ĐƯỢC**. **Review đặc tả wp698 lượt 1: +1** (`luc-luong-chi-quet-truc-khong-quet-tich`) ⇒ **≥ 4** | chú thích mã :2233, :2240; comment `5911284002`; VERDICT.md lượt 1 |

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
của r2 dựng tập đóng 221 dò (§2) thay vì chỉ vá 52 biểu hiện được chỉ.

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
  nghị bỏ nếu chủ kho đọc Q14 là cấm cả văn bản); r2 áp nó rồi sửa tiếp (§0). Không có mã
  `ops/cong_cu_test.py` nào đi từ reviewer vào đặc tả.

Ba quyết định khác khuyến nghị trong bản nháp của r1:

- Q5: bản nháp đề 2 vòng (con số trục VÒNG của ADR-0043, đã bị ADR-0048 thay); chủ kho chọn lặp
  tới 0/0/0.
- Q6: bản nháp đề phiên độc lập; chủ kho chọn subagent.
- Q8: bản nháp đề một lượt Windows; chủ kho chọn không.

Nhãn "(Recommended)" trong bảng trên là của câu hỏi phiên điều phối trình cho chủ kho, không phải
khuyến nghị trong bản nháp.

### 11.1 Điều r2 tự quyết theo verdict lượt 1 — chỉ có hiệu lực khi comment Q10 của r2 xác nhận

Chủ kho chưa trả lời câu hỏi nào về r2. Các điểm dưới là cách r2 đóng tám lớp của review lượt 1;
comment xác nhận closure của r2 (Q10) là chỗ chủ kho chấp nhận hay bác từng điểm. Bác một điểm
⇒ revision mới, không sửa r2.

1. **Mở rộng mục tiêu trong phạm vi Q1/Q3.** r2 đọc "F49" (Q1) là *khe đo của các phép chuẩn hoá
   đầu vào trong bộ đọc chế độ và nguồn HEAD*, nên nó gồm `ra` (bộ đọc thứ tư của `_doc_che_do`),
   mọi vị trí, mọi thành viên, và các họ ký tự r1 khai "KHÔNG ĐO" (Zs ngoài ASCII, Cc ngoài TAB, dấu
   kết hợp) mà §1.8 đo thấy sống. Phần "kiểu ngoại lệ" của F46 vào M5 theo cùng lý lẽ Q3 đã dùng
   để gộp TAB của F46 vào lớp B. Bác ⇒ r3 đưa phần bị bác về nợ có tên.
2. **Đổi cách làm lớp B sang miền dẫn xuất** (M1) và tiêu chí sang tập dò đóng (A1/A2/A8). Đây
   là "xem lại cách làm tại checkpoint" mà protocol §12 đòi cho lớp `doc-che-do-van-tay` (§9).
3. **M3 thêm tích biên** (48 kịch bản), trên nền Q4.
4. **43 canh `DOT_BIEN`** (16 của r1 + 27 mới), tổng 459 đột biến.
5. **Hai bộ đọc ngoài lớp B** — đầu tệp mảnh của `_gom_manh` và `CONG_CU_TEST_TIEN_TRINH` — được
   đo (§1.8.6) và để ngoài mục tiêu: nợ mới `gom-dau-manh-chuan-hoa-wp698`; phần mức đo của
   `CONG_CU_TEST_TIEN_TRINH` gộp vào nợ `so-tien-trinh-nhan-fullwidth` (Q2) đã có.
6. **Q9 không miễn (d)** — cách đọc nguyên văn ở trên. Chủ kho muốn miễn (d) thì phải nói riêng.
7. **Chủ thể của `land_obligations` 8** là người chủ kho chỉ định.
8. **Ước kích thước** của mục tiêu mở rộng: 1 tệp; IMP-R2G `git diff --numstat` = +191/−5 (dòng dài: 43 hàng canh viết một dòng mỗi hàng); ngắt ở 120 ký tự/dòng ra 266, bớt khoảng 10 dòng chỉ phục vụ đo bậc hai (hằng `_GO698`, bảng lọc nhóm, hàm `_n698`) ⇒ khoảng 256; cộng chú thích M4 mà IMP-R2G chưa có, ước 10–25 dòng ⇒ khoảng 265–280 dòng thêm, dưới trần 300 khoảng 20–35 dòng — biên mỏng. ƯỚC trên ứng viên tham chiếu, không phải bản giao (S5). r2 không nới trần Q12.

Ngoài tám điểm trên, **không còn câu hỏi mở nào**.

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

Tập dò đóng của r2 (209 dò). Cách dùng: `PYTHONDONTWRITEBYTECODE=1 TMPDIR=<scratch> python3 do_dot_bien_r2.py <gốc bản sao>
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

## Phụ lục D — `phan_hang_r2.py` (nguyên văn, sha256 `c1bdf8d23b85e932a23cdcb9bb31403ca754c952c43911aeaffbb27aacf26065`)

Phân hạng và chia tập theo tên (§6). Cách dùng: `python3 phan_hang_r2.py '<mẫu glob jsonl>' [chi_tiet]`.

```python
"""Phân hạng đầu ra jsonl của Phụ lục A/C (wp698 r2, Phụ lục D). Không chạy đột biến nào.

Dùng: python phan_hang_r2.py <mẫu glob jsonl> [chi_tiet]
Hạng: GIET = `_ket_luan_ban_kinh` 0 lỗi, đích `giet_that`, không ca nào khác chết ngoài ca `bo_qua`;
      SONG = không ca nào chết; KHAC = mọi trường hợp còn lại (tín dụng giả, sai đích, bán kính > 1);
      LOI_DUNG = phép đo tự hỏng (AssertionError của rig).
Tập (theo TÊN, §6): T-C `…_ra`, `s_ra_…`, `p_cf_ra_…` · T-D `s2_…`, `s3_…` · T-E `z_exc_…` · NGOAI `g_…`, `t_…` · T-B còn lại.
"""
import collections
import glob
import json
import sys


def tap(ten):
    if ten.startswith(("g_", "t_")):
        return "NGOAI"
    if ten.startswith(("s2_", "s3_")):
        return "T-D"
    if ten.startswith("z_exc_"):
        return "T-E"
    if ten.endswith("_ra") or ten.startswith(("s_ra_", "p_cf_ra_")):
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
for tp in ("T-B", "T-C", "T-D", "T-E", "NGOAI"):
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
