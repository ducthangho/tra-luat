# ĐẶC TẢ — `CI-G5-CONG-CU-VA-TIEP` (`wp698`) — revision 1, ĐÓNG BĂNG

| trường | giá trị |
|---|---|
| `schema_version` | 1 (protocol §3.2) |
| `packet_id` | `wp698` (ID bền `wp<issue>`, protocol §3.2); tên đọc được: `CI-G5-CONG-CU-VA-TIEP`. Hai tên cùng chỉ một packet; lease dùng tên nào cũng phải kèm `packet_issue: 698`. |
| `revision` | **1** |
| `thay_the_cho` | RỖNG: đây là revision đầu. |
| `packet_issue` | **#698** (object ID `5646961843`, tạo 2026-09-30T13:09:12Z). Issue và hai comment quyết định (`5912199805`, `5914438647`) đều do **phiên agent đăng hộ chủ kho** bằng credential chủ kho. Vì vậy `author_association: OWNER` không chứng minh chủ kho tự gõ; tư cách của chúng là lời khai có neo (#566). |
| `mission_issue` | RỖNG. #698 không khai Mission. Packet mẹ #668 cũng không khai (đặc tả `ops/specs/CI-G5-CONG-CU-CHIA-MANH-r1.md`). Thẩm quyền của closure do đó đi qua quyết định Q10 (§11). |
| `nguon_cap_viec` | Chỉ thị chủ kho, nguyên văn: *"#668: mở packet tiếp nối cho F48–F50"*, neo ở #668 comment `5911957306` và thân #698. Nguồn phát hiện: verdict cross-review **lượt 22** của phiên `session_01VYtkBy…`, #668 comment `5911284002` (12:27:04Z 30-09). Verdict này mang nhãn `advisory_review`, kết luận `changes_requested` với 0 P1 · 2 P2 · 1 P3, `reviewed_sha` là `8d7faef`, và commit ấy **chưa được đẩy** lên GitHub. Executor và reviewer: #698 comment `5912199805`, nguyên văn *"Chọn opus 5.5 executor. Reviewer để sonnet 5.5 xem"*. **Quyết định chủ kho cho r1:** #698 comment `5914438647`, tạo 2026-09-30T15:30:26Z, gồm hai lượt trả lời trong phiên lúc 15:28:25Z và 15:30:09Z (chi tiết ở §11). |
| `objective` | Đóng ba lớp khe đo trong `ops/cong_cu_test.py`. Phép đo lại trên nền `fc852ff` (và trước đó trên `423b4ba`, cùng kết quả) tái hiện được cả ba lớp (§1). (B) Bộ đọc chế độ và nguồn HEAD không có ô bắt các phép chuẩn hoá NFKC, bỏ ký tự Cf, bỏ TAB. (C) `ra` ở tầng `_doc_che_do` không có ô bắt normpath hay expanduser. (D) Nhánh mảnh của `main` không có điểm lực lượng đủ để bắt vị từ đếm. Mỗi đường vào đo được ở §1 phải trở thành một đột biến canh, và chỉ đúng ca đích được giết nó bằng `TinHieuChotCa`, bán kính 1. Lớp (A), tức registry năng lực ngoài cửa sổ (F48), **không** thuộc r1: chủ kho quyết ghi nợ `registry-nang-luc-ngoai-cua-so` (§11, Q1). |
| `review_class` | **`sensitive`**: bộ test gate G5 có vòng đột biến tự kiểm, cùng lớp với #668. Fail-closed theo protocol §8. |
| `risk` | **`sensitive`**: cùng lý do trên. |
| `executor` | `claude`, model Claude Opus 5.5 (`claude-opus-5-5`), theo comment `5912199805`. Effort do phiên tự khai; từ ngoài là **KHÔNG ĐO ĐƯỢC**. |
| reviewer | Claude Sonnet 5.5, **chạy bằng subagent** trong phiên điều phối (quyết định chủ kho, §11 Q6). Chỉ mô tả hướng sửa, không đính patch-as-hint (Q14). |
| assurance đạt được | **`review_deferred`.** Hai lý do độc lập. (1) Reviewer tự khai chạy bằng subagent, tức `model_reviewer_identity.che_do` chứa `subagent`. Khi đó `_thieu()` của `ops/bien_nhan_v2.py` từ chối mọi mức trong `ASSURANCE_CAN_DOC_LAP` (`cross_approved`, `same_provider_approved`, `human_audited`), nên biên nhận chỉ được ghi `review_deferred`. (2) Dù chạy phiên độc lập, `cross_approved` cũng không đạt được, vì executor và reviewer cùng họ Claude (protocol §8 mục 1; `ops/bien_nhan_v2.py` từ chối `cross_approved` khi hai bên cùng họ model). **Cổng land là `human_audited`** do chủ kho audit (§8: `sensitive` phải có `cross_approved` hoặc `human_audited`). |
| ngưỡng review | **0 P1 · 0 P2 · 0 P3**. Không giới hạn số vòng: vượt trần canon 2 vòng của ADR-0043 là có chủ đích, và phải ghi bằng khối `nang_tran` ngay dưới bảng này (Q5). |
| `environment` | **`cloud`**. Mục tiêu r1 gồm ô thuần và giàn giả trong một tệp test. r1 không đo đồng hồ ngủ máy và không cần quyền tạo symlink, vì lớp (A) là lớp phụ thuộc năng lực symlink và đã ra ngoài r1. **Không chạy Windows** (quyết định chủ kho, Q8), nên đường Windows của các ô mới không được đo; đây là nợ `windows-chua-do-o-moi-wp698`. |
| `depends_on` | **Chặn cấp lease: lease `wp671-windows-bash-nen-escape-r1-g2-claude` (#671).** Lease này giữ `ops/bash_nen.py` và `ops/cong_cu_test.py` tới `2026-10-01T03:35:00Z`. Tệp lease nằm ở `refs/remotes/origin/ops/cap-lease-671-g1` (commit `1235a32`). Chỉ cấp lease `wp698` khi cả năm điều kiện dưới đây thoả **và được đo lại lúc cấp**; số trong ô này không thay được phép đo lúc cấp. (1) So `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (bỏ `HEAD`) theo **tập tên VÀ OID**: thiếu cục bộ 0, lệch OID 0. Không chạy được ⇒ `KHÔNG_XÁC_ĐỊNH` ⇒ không cấp. (2) `python ops/lease_publish.py ai-dang-giu ops/cong_cu_test.py` ra `NGƯỜI_GIỮ 0`, rc=0. Phải chạy trên clone mà mọi nhánh cục bộ đều không tụt sau `origin` và không nhánh nào khai upstream đã mất; nếu không, bộ quét fail-close `rc=12` trước khi kịp đếm người giữ (xem "Lịch sử đo" ở cuối ô này). (3) Nếu #671 land trước và đổi `ops/cong_cu_test.py` thì phải **dời nền bằng revision mới trước khi cấp**, không cấp trên nền cũ. Nhánh ứng viên `claude/wp671-windows-bash-nen-escape-g1` @ `bd6ad5d` đổi tệp này +163/−22 so với nền `89fc4fa` của nó (đo lại 15:41:32Z 30-09). (4) Chủ kho đã xác nhận closure bằng một comment trên #698 neo `spec_hash` của tệp này (Q10), và lease neo đúng `spec_hash` ấy. (5) Không có lượt review nào đang chạy trên write set. **Hiện trạng đo 15:40:23Z–15:40:36Z 30-09** (clone sạch, `origin` = GitHub, HEAD = `origin/master` = `fc852ff`): máy chủ 459 ref, cục bộ 459, thiếu cục bộ 0, thừa cục bộ 0, lệch tên+OID 0. `ai-dang-giu ops/cong_cu_test.py` ra `NGƯỜI_GIỮ 1: wp671-windows-bash-nen-escape-r1-g2-claude` (nhãn `CÒN_HẠN`), rc=11, kèm 54 dòng `HẾT_HẠN`. Điều kiện (2) **chưa thoả**. Lịch sử đo: lúc 15:04:45Z–15:05:09Z có 458/458 ref và cùng người giữ; lúc 14:43:27Z `ai-dang-giu .github/workflows/ci.yml` ra `NGƯỜI_GIỮ 0`, rc=0. Cũng tại 14:4xZ, kho dùng chung của phiên điều phối cho `rc=12` (`KHÔNG_XÁC_ĐỊNH`: một nhánh cục bộ khai upstream `refs/remotes/origin/ops/spec-lease-id-ep-kieu-yaml`, mà ref này không còn); đó là lỗi của kho cục bộ, không phải kết quả về người giữ. |
| nền nghiệm thu | **`fc852fff7da37f1669569572b79571446e61c294`** (merge PR #697, bookkeeping #668), theo quyết định chủ kho Q11. Đây là **nền bất biến** để đo diff và nghiệm thu. Bản nháp trước dùng `423b4ba14078701859b9e6ac101a68a3fc4ddef4` (merge PR #696). Đo 15:31:57Z 30-09: `git rev-parse 423b4ba:ops/cong_cu_test.py fc852fff7da37f1669569572b79571446e61c294:ops/cong_cu_test.py` cho hai lần cùng blob `9edea6b1629b46f27758b2073e74210dc73495b7`, và `git diff --quiet 423b4ba fc852fff7da37f1669569572b79571446e61c294 -- ops/cong_cu_test.py` cho rc=0. Hai nền khác nhau ở 66 tệp, tất cả là hồ sơ: `ops/land/` 23, `ops/leases/` 3, `ops/reviews/` 39, `ops/specs/` 1 (`git diff --name-only 423b4ba fc852ff`). Mọi phép đo ở §1 đều **chạy lại trên `fc852ff`** và cho cùng kết quả. Nền tiếp nối (continuation base) là `origin/master` lúc cấp lease; nếu nó khác `fc852ff` thì lease phải khai riêng. Diff nghiệm thu đo trên `ops/cong_cu_test.py` so với `fc852ff`, cộng với điều kiện A4-f. |
| `spec_hash` | Xem **Công thức băm** dưới đây. Giá trị **không** nằm trong tệp này. |

**Khối `nang_tran`** (ADR-0043: vượt trần phải khai `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`).
Lease phải chép nguyên khối này:

```yaml
nang_tran:
  truc: vong_review
  tran_cu: 2
  tran_moi: khong_gioi_han_lap_toi_0_P1_0_P2_0_P3
  ai_nang: ducthangho
  can_cu: https://github.com/ducthangho/tra-luat/issues/698#issuecomment-5914438647
  khi_nao: '2026-09-30T15:30:09Z'
  ghi_ho: phien agent dang ho chu kho (comment 5914438647, loi khai co neo #566)
```

Khối này chỉ nâng trần **số vòng** của ADR-0043. Nó **không** gỡ checkpoint theo lớp của
protocol §12 (xem S6). Đo lúc 15:4xZ: `grep nang_tran` trong `ops/lease_publish.py` và
`.claude/dev/packet_loop.py` ra 0 dòng. Tức hiện không có cổng máy nào đọc khối này, dù ADR-0043
viết rằng thiếu khối thì cổng đăng lease từ chối. Khối này là hồ sơ thẩm quyền, không phải
chốt máy. Hình dạng của khối theo tiền lệ lease `wp461-be-mat-thu-hai-cua-codex-exec-1g9-claude-20260925`.

**Công thức băm.** `spec_hash` = SHA-256 trên **toàn bộ bytes** của tệp này tại commit
đóng băng: `sha256sum ops/specs/ci-g5-cong-cu-va-tiep-r1.md`, không loại dòng nào. Giá trị
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
| `required_checks` | Trên PR, tại exact head. PR chỉ được mở **một lần**, khi review đã đạt 0/0/0; không chạy CI trong vòng lặp (Q7). (a) Bốn context bắt buộc của ruleset `bao-ve-cong-dang-lease` (id `20856202`, đọc lại qua REST lúc 15:40Z 30-09, `updated_at` không đổi so với lần đọc 14:44:35Z): `gate (ubuntu-latest)`, `gate-ops (ubuntu-latest)`, `gate-packet-loop (ubuntu-latest)`, `gate-cong-cu-gop (ubuntu-latest)`. (b) Tám job mảnh, từ `gate-cong-cu (ubuntu-latest, 0)` tới `gate-cong-cu (ubuntu-latest, 7)`; tên job lấy nguyên văn từ lượt hậu-merge `36696528580`. (c) `gate-registry (ubuntu-latest)` với rc=0. Theo quyết định Q9, nếu job này đỏ **vì hết trần** (`LỖI HẠ TẦNG: hết giờ`) trên một run của PR #698 thì (a) cộng (b) xanh là đủ; phải ghi nợ có neo `gate-registry-het-tran-wp698` kèm run ID/job ID. Quyết định này chỉ áp cho các run của PR #698. Đỏ vì bất kỳ lý do nào khác thì **không đạt**. (d) Job `thu-hoi` của `.github/workflows/ops-thu-hoi-admission.yml` (`pull_request_target` vào `master`, các kiểu `opened` `reopened` `synchronize` `ready_for_review` `edited`). (e) **Không** có lượt Windows (Q8). |
| `land_obligations` | 1. Chủ kho audit (`human_audited`) trên exact head, cộng uỷ quyền merge bền. Không phiên nào tự approve hay tự merge. 2. Verdict mọi lượt review và biên nhận v2 của chúng vào `ops/reviews/`, theo mẫu #668, với nhãn `review_deferred`. 3. Hồ sơ land vào `ops/land/`, theo tiền lệ PR #691 và #697. 4. Đặc tả và lease vào master bằng một PR bookkeeping. 5. Thu hồi lease sau land bằng rút hạn. **Không** viết bia mộ `da_bi_thay_the` vào lease đã hết hạn (bài học run `35519177197`/`35519243379` trong `CLAUDE.md`). 6. Đóng #698 và đăng comment nối trên #668. 7. Ghi nợ có tên: `registry-nang-luc-ngoai-cua-so` (Q1); `so-tien-trinh-nhan-fullwidth` (Q2); `windows-chua-do-o-moi-wp698` (Q8); và `gate-registry-het-tran-wp698` nếu xảy ra (Q9). 8. Hồ sơ lượt 22 vào một nhánh `ops/**` kèm băm (Q13); việc này **không** chặn land. |

Lease phải **chép** đúng các giá trị trên và khối `nang_tran`, không thêm, không đổi. Lệch ⇒ **DỪNG**.

**GIỚI HẠN LỜI KHAI:** mọi khẳng định chỉ chứng minh tới đúng phép đo ghi kèm. Danh sách
đường vào ở §2 do chính phiên soạn tự liệt kê, và bảng §1 được trích bằng đúng 30 đột biến dò
trong Phụ lục A. **Danh sách ấy có thể thiếu.** Reviewer tìm ra được một đường sống ngoài danh
sách thì đường ấy tính là finding (protocol §8, "bảng bằng chứng phải tự khai giới hạn").
**Ba trạng thái:** có · không · **KHÔNG ĐO ĐƯỢC**.

---

## 1. Đo lại F48–F50: trên nền `fc852ff`, và trước đó trên `423b4ba`

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

## 2. Đường vào: liệt kê HẾT trước khi vá

Áp bài học *"VÁ ĐÚNG CHỖ ĐƯỢC CHỈ RỒI BỎ SÓT ĐƯỜNG THỨ BA"*: danh sách dưới đây do phiên soạn tự
dựng từ mã, không chép từ verdict. Lượt 22 nêu 3 finding. Phép đo ra **24 đường sống trong 4
lớp**, trong đó verdict nêu 15 đường (A ×6, B ×6, C ×2, D ×1). **9** đường còn lại verdict không
nêu: gán thẳng sau cửa sổ ×1, trước ảnh ×1, TAB ×3, `>= 2`, `== len(CA) - 1`, `hong`,
`tien_kiem`.

| lớp | trục | đường đã liệt kê | trạng thái trên nền | vào r1? |
|---|---|---|---|---|
| B | bộ đọc × phép | {`bk`, `mh`, `head`} × {NFKC, bỏ Cf, bỏ TAB} = 9 | 9/9 sống | có (M1) |
| B | bộ đọc × phép | {`bk`, `mh`} × {`strip`}, `head` × {`lower`} | bị giết (đối chứng) | không cần |
| B | bộ đọc × phép | chỉ bỏ Zs ngoài ASCII; casefold; phép khác | **KHÔNG ĐO** | không (§10) |
| C | `ra` × phép đường dẫn | normpath, expanduser | 2/2 sống | có (M2) |
| C | `ra` × phép đường dẫn | strip, abspath | bị giết (đối chứng) | không cần |
| D | biến lực lượng × vị từ | `bo_qua` {`==2`, `>=2`, `==len(CA)-1`}, `hong` {`==1`}, `tien_kiem_bo_qua` {`==1`} | 5/5 sống | có (M3) |
| D | biến lực lượng × vị từ | `bo_qua` `==c` với 3 ≤ c ≤ len(CA)−2 | **KHÔNG ĐO** từng c; về cấu trúc sống vì không có điểm nào | có, qua quét trọn miền (M3, Q4) |
| A | vị trí × cú pháp | sau cửa sổ ×7 hình dạng, trước ảnh ×1 | 8/8 sống | **không**: nợ (Q1) |

## 3. `write_set`

- `ops/cong_cu_test.py`

Không có đường dẫn nào khác. Căn cứ: mọi ca đích (`t52`/`t53`/`t54`), mọi miền ô
(`_luoi_che_do`, `_luoi_git`, `bang_env`, kịch bản của `_in_tu_kiem_main`), bảng `DOT_BIEN` và
mọi hàm bị đột biến đều nằm trong tệp này. `ci.yml` không đổi, vì r1 không thêm job hay biến môi
trường. `.claude/dev/ci_dang_ky_test.py` cũng không đổi, vì hình dạng G5 giữ nguyên. Bản thân đặc
tả này là hồ sơ của lượt soạn spec, **không** thuộc write set của lượt thi hành.

## 4. `ngoai_pham_vi`

| thứ | lý do |
|---|---|
| Lớp A (F48 và đường (e)) | Chủ kho quyết không gộp (Q1). Ghi nợ `registry-nang-luc-ngoai-cua-so`; muốn đóng thì mở packet riêng. |
| `_so_tien_trinh_ban_kinh` nhận fullwidth và ném ở chữ số mũ | Chủ kho quyết ghi nợ `so-tien-trinh-nhan-fullwidth` (Q2). |
| F46 phần "kiểu ngoại lệ" | Nội dung chỉ có trong `5a071b8`, commit không có trong kho. Không dựng được phép đo (§10). |
| Patch-as-hint và các hint của lượt 22 | Chủ kho quyết không dùng patch-as-hint; reviewer chỉ mô tả hướng (Q14). Hồ sơ lượt 22 đưa lên nhánh `ops/**` chỉ để làm hồ sơ, không làm đầu vào (Q13). |
| Đẩy hoặc merge `8d7faef` / `5a071b8` | Không có trong kho, và không có lease. |
| Chạy Windows (`workflow_dispatch` hay nhãn `windows`) | Chủ kho quyết không (Q8); nợ `windows-chua-do-o-moi-wp698`. |
| CI trong vòng lặp vá–review | Chủ kho quyết không; CI chỉ chạy một lần khi mở PR sau lúc review sạch (Q7). |
| Đổi thân `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`, `_chay_1_ca` | §1.3–§1.5 đo được rằng chúng đúng; khe nằm ở ô đo, không ở mã. Đổi ⇒ S1. |
| `ci.yml`, `ci_dang_ky_test.py`, ruleset | Không cần cho mục tiêu r1. |
| Nợ `ops/nhanh_don_duoc_test.py` sát trần trong `gate-registry` | Nợ của #668 (quyết định `5910229584`). Packet này chỉ **gặp** nó và xử lý theo Q9, không sửa. |

## 5. `muc_tieu`

Mỗi mục chiếu vào đúng một đường dẫn trong write set (L2): `ops/cong_cu_test.py`.

1. **M1 (lớp B).** Thêm ô vào miền đầu vào của `t53`: `_luoi_che_do` và/hoặc `bang_env` cho
   `bk`/`mh`, `_luoi_git` cho `head`.
   - Các ô phải được **dẫn xuất** từ giá trị hợp lệ chuẩn (`manh`, một `k/N` hợp lệ, một đầu HEAD
     40 hex và một 64 hex) bằng cách chèn hoặc thay đúng một ký tự thuộc **một** trong ba lớp đã
     khai: dạng có NFKC khác chính nó, ký tự Cf, TAB.
   - Chỗ chèn phải gồm đầu, giữa và cuối, sao cho phép chuẩn hoá tương ứng biến một giá trị đang
     bị từ chối thành giá trị được nhận.
   - Kỳ vọng lấy từ oracle hiện có; §1.3 đã đo rằng không cần đổi oracle.
   - Thêm **9** mục `DOT_BIEN` canh. Mỗi mục có **cùng mỏ neo và cùng phép thay** với một trong
     chín dò lớp B ở Phụ lục A, ca đích `t53`, và được đăng ký **vô điều kiện** trong một bảng có
     sẵn nằm **trước** `_TRUOC_NANG_LUC`.
2. **M2 (lớp C).** Thêm ô `ra` mà cả normpath lẫn expanduser đều làm đổi giá trị (ví dụ
   `a/./b//c`, `a/../b`, `~/x`), với kỳ vọng nguyên văn. Thêm **2** mục canh có cùng mỏ neo và
   phép thay với `e49_ra_normpath` và `e49_ra_expanduser`, ca đích `t53`.
3. **M3 (lớp D).** Kịch bản mảnh của `t54` **quét trọn** miền lực lượng hữu hạn (Q4):
   - `len(bo_qua)` ∈ {0, …, len(CA)} và `len(hong)` ∈ {0, …, len(CA)} ở nhánh mảnh;
   - `tien_kiem_bo_qua` lấy mọi tập con của hai tiền kiểm.

   Kỳ vọng dựng bằng chính các hàm dựng kỳ vọng hiện có của `t54`. Thêm **5** mục canh có cùng mỏ
   neo và phép thay với `e50_bang_2`, `e50_tu_2`, `x50_bang_n_tru_1`, `x47_hong_bang_1` và
   `x47_tk_bang_1`, ca đích `t54`.
4. **M4 (hồ sơ trong tệp).** Mỗi chỗ thêm mới có chú thích neo về #698 và về dò tương ứng. Mọi
   docstring hay chú thích đang khai một lớp là "đã đóng" mà §1 đo thấy còn hở phải được sửa thành
   sự thật mới. Executor phải grep để tìm, không chỉ sửa chỗ mình đã biết.

Tổng cộng **16** mục canh mới. Tên mục do executor đặt, ví dụ theo mẫu có sẵn với tiền tố
`f49_`/`f50_`. Handoff phải kèm bảng nối `tên dò ↔ tên mục DOT_BIEN`.

## 6. `nghiem_thu`

"Đột biến" nghĩa là chạy trên **bản sao tạm**, với `PYTHONDONTWRITEBYTECODE=1`. "`ok … 1/N`"
nghĩa là `_ket_luan_ban_kinh` in `ok <tên> → giết đúng '<ca đích>' · bán kính 1/N`: ca đích ra
`giet_that` (`TinHieuChotCa` mang **đúng tên ca đích**, tức nhánh `giet_that` của `_chay_1_ca`
:2292), và không ca nào khác chết. Theo bài học *"đột biến bị giết không phải đột biến bị giết
đúng lý do"*, một mục canh chết bằng `tin_dung_gia` (`LoiDungCa`, `AttributeError`, tiến trình con
crash…) hoặc có bán kính > 1 thì **không được nhận**, dù mã thoát khác 0.

- **A1 (M1).** Trong vòng bán kính trọn (A5), cả 9 mục canh lớp B đều `ok … 't53_…' · 1/N`.
  **ĐỎ KHI:**
  - (i) Chạy 9 mục ấy trên nền `fc852ff` (chưa có ô mới) thì mỗi mục in *"vẫn XANH"*. §1.6 đã đo
    đúng như vậy trên cả `fc852ff` lẫn `423b4ba`; đây là phép đo làm tiêu chí đỏ trước bản vá.
  - (ii) Bậc hai: gỡ riêng nhóm ô của **một** phép (NFKC | Cf | TAB) thì **đúng** các mục canh
    của phép ấy sống lại, còn mục của hai phép kia vẫn `ok`. Nếu ba nhóm không tách được bằng đầu
    vào, chúng là bộ tương đương và tiêu chí ĐỎ.
  - (iii) Có mục nào `tin_dung_gia` hoặc bán kính > 1.
- **A2 (M2).** Cả 2 mục canh lớp C đều `ok … 't53_…' · 1/N`. **ĐỎ KHI:**
  - (i) chúng sống trên nền (đã đo ở §1.6);
  - (ii) gỡ các ô `ra` mới thì chúng sống lại;
  - (iii) có mục `tin_dung_gia` hoặc bán kính > 1.
- **A3 (M3).** Cả 5 mục canh lớp D đều `ok … 't54_…' · 1/N`. **ĐỎ KHI:**
  - (i) chúng sống trên nền (đã đo ở §1.6);
  - (ii) bậc hai: gỡ riêng phần quét `bo_qua` thì đúng ba mục canh `bo_qua` sống lại; gỡ riêng
    phần quét `hong` thì đúng mục `hong` sống lại; gỡ riêng phần tập con tiền kiểm thì đúng mục
    `tien_kiem` sống lại (mỗi trục là một nhóm riêng);
  - (iii) có mục `tin_dung_gia` hoặc bán kính > 1.
- **A4 (không hồi quy, không nới phạm vi).** Ứng viên và nền được đo trong **một** lệnh, cùng
  công cụ. **ĐỎ KHI** một mục dưới đây đỏ trên ứng viên mà xanh trên nền:
  - (a) `CONG_CU_TEST_BAN_KINH=manh python ops/cong_cu_test.py` phải ra `cong_cu_test: M/M đạt`,
    `lỗi đột biến=0`, `cổng cây thật=ĐẠT`, rc=0. Nền đo lúc 15:32Z trên `fc852ff`:
    `55/55; tổng=56, bỏ qua=1`. Môi trường có `jsonschema` thì kỳ vọng `bỏ qua=0`.
  - (b) `ruff check --select F ops/cong_cu_test.py` cho **delta F = 0**. Nền đo lúc 15:40:23Z
    trên `fc852ff` bằng ruff 0.15.8 tại chỗ: 1 lỗi, `F841` ở :2606. CI ghim 0.15.15, nên phải đo
    lại hai vế bằng đúng bản ghim.
  - (c) `python .claude/dev/ci_dang_ky_test.py` (không `--chay`) cho delta 0.
  - (d) `git diff fc852fff7da37f1669569572b79571446e61c294 -- ops/cong_cu_test.py` **không chạm
    thân** `_doc_che_do`, `_van_tay`, `main`, `_so_tien_trinh_ban_kinh`, `_ket_luan_ban_kinh`,
    `_chay_1_ca`.
  - (e) Đếm bằng AST như §1.2: số chỗ ghi `DOT_BIEN` **sau** dòng `_TEN_NANG_LUC = …` vẫn
    **= 0** (nền: 0). Bản vá không được mở rộng đường (e).
  - (f) Tập tệp đổi so với nền tiếp nối phải = `{ops/cong_cu_test.py}`.
- **A5 (bán kính trọn).** Chạy 8 lượt `CONG_CU_TEST_MANH=k/8` với `CONG_CU_TEST_MANH_RA=…`
  (k = 0…7), rồi `python ops/cong_cu_test.py --gop <thư mục>`. Phải ra `GOM MẢNH 8/8`, mọi dòng
  bảng là `ok`, `lỗi đột biến=0`, và số đột biến = **416 + số mục canh mới (≥ 16)**. Nghĩa là mọi
  đột biến cũ vẫn `ok`, và cả 16 mục mới cũng `ok`. **ĐỎ KHI:** có lượt rc≠0, có dòng không `ok`,
  hoặc số lệch.
- **A6 (review).** Reviewer Claude Sonnet 5.5 chạy bằng subagent, đưa verdict trên exact head, lặp
  tới **0 P1 · 0 P2 · 0 P3** (khối `nang_tran`); biên nhận ghi nhãn **`review_deferred`**. Chưa có
  `human_audited` của chủ kho thì không land. Tiêu chí này không có phép đo máy: nó là cổng thẩm
  quyền, không phải cổng hành vi.

## 7. `ci_budget`

Protocol §12 chia chi CI theo mục đích. Đơn vị là **lượt workflow run**; attempt tính riêng; mỗi
lượt ghi kèm exact SHA.

| loại | `used / reserved / limit` | ghi chú |
|---|---|---|
| Gate tự động | `0 / 1 / 1` | **Một** lượt `ci.yml`, bắn khi mở PR sau khi review đạt 0/0/0 (Q7). `thu-hoi` chạy theo sự kiện PR riêng và không tính vào đây. Hạn mức 1 là cách đọc nhãn "CI 1 lần khi sạch". Không chạy CI trong vòng lặp. Ước theo lượt `36696528580`: 14 job, toàn ubuntu. Nếu phải đẩy thêm commit lên nhánh PR sau khi đã mở thì mỗi lần đẩy bắn một lượt nữa, tức vượt `limit` ⇒ DỪNG, hỏi chủ kho (S10). |
| Phép đo được cấp | `0 / 0 / 0` | Không có `workflow_dispatch`, không Windows (Q8). |
| Thăm dò chưa cấp | không | — |

Chi phí tại chỗ, trên container 4 lõi với 4 tiến trình song song: mỗi đột biến mất 28–36 s cho
một lượt 56 ca (hai lượt đo ở §1.1), nên 16 mục canh cộng thêm 16 lượt như thế vào vòng bán kính.
Quét trọn miền ở M3 thêm khoảng 110 kịch bản vào `t54`. Nếu thời gian tăng tuyến tính theo 2,17 s
cho 219 kịch bản thì mỗi lượt `t54` chậm thêm khoảng 1,1 s; đây là **ƯỚC**, chưa đo trên bản vá.
`t54` chạy trong mọi lượt đột biến.

## 8. Điều kiện dừng

- **S1:** cần sửa thứ gì ngoài `ops/cong_cu_test.py`, hoặc cần đổi thân một hàm liệt kê ở A4-d
  ⇒ DỪNG, handoff, revision mới.
- **S2:** lúc cấp lease, so tập tên+OID ref bị lệch, hoặc `ai-dang-giu ops/cong_cu_test.py` ≠
  `NGƯỜI_GIỮ 0`, hoặc chưa có comment chủ kho xác nhận closure neo `spec_hash` (Q10) ⇒ không cấp.
- **S3:** #671 land trước và đổi `ops/cong_cu_test.py` ⇒ revision mới dời nền **trước** khi cấp.
- **S4:** một mục canh chỉ chết bằng `tin_dung_gia` hoặc với bán kính > 1, và muốn sửa thì phải
  đổi mã ngoài phạm vi ⇒ DỪNG.
- **S5:** vượt ≤ 3 tệp hoặc ≤ 300 dòng thêm (ADR-0044 cho `sensitive`; chủ kho giữ mặc định, Q12)
  ⇒ DỪNG, hỏi chủ kho.
- **S6:** không có trần số vòng review (khối `nang_tran`, Q5); vòng lặp dừng khi đạt 0/0/0. Checkpoint
  theo lớp của protocol §12 vẫn áp: nếu một lớp xuất hiện ở lượt review thứ ba của packet này thì
  báo chủ kho kèm bảng lớp, và chủ kho quyết tiếp tục hay đổi cách làm.
- **S7:** `gate-registry (ubuntu-latest)` đỏ. Nếu vì hết trần thì làm theo Q9: các context bắt buộc
  cộng tám mảnh xanh là đủ, ghi nợ có neo. Đỏ vì lý do khác ⇒ DỪNG.
- **S8:** lease hết hạn ⇒ ngừng sửa, handoff (§7).
- **S9:** phát hiện ngoài spec ⇒ handoff/successor (§3.2), không tự mở write set.
- **S10:** chưa đạt 0/0/0 mà đã muốn mở PR hay chạy CI, hoặc sau khi mở PR mà cần thêm một lượt
  CI ⇒ DỪNG, hỏi chủ kho (Q7).

## 9. `hinh_dang_ke_thua`

Đây là packet khắc phục của #668. Số đếm hình dạng lỗi chép từ hồ sơ tiền nhiệm (L4), mỗi số kèm
nguồn.

| lớp (slug) | số lượt review có finding | nguồn |
|---|---|---|
| `registry-nang-luc` (lớp (6) của #668) | **≥ 5** tính tới lượt 20; lượt 21 có 0 finding và xếp (e) là giới hạn; lượt 22 có F48 ⇒ **6** nếu tính cùng lớp | #668 comment `5905962202` ("lớp registry năng lực ra finding lượt thứ 5"); `…-review-21-claude-verdict.md` H6; comment `5911284002` |
| `doc-che-do-van-tay` | **≥ 5**: Codex lượt 12, 13, 14, 15, và F49 ở lượt 22. Thêm F46, mà số lượt **KHÔNG ĐO ĐƯỢC** vì hồ sơ phiên `session_01VYtkBy…` không có trong kho | chú thích mã trên nền: F29 :8106, F31 :8110, F33 :8041, F30/F32/F34 :8144, F36 :2257; comment `5911284002` |
| `main-luc-luong-gia-tri` | **≥ 3**: F42 (Codex lượt 19), F44 (lượt 20), F50 (lượt 22). F47 **KHÔNG ĐO ĐƯỢC** | chú thích mã :2233, :2240; comment `5911284002` |

Cả ba lớp đã qua ngưỡng của protocol §12: *"một lớp xuất hiện ở ba lượt review khác nhau đòi xem
lại cách làm tại checkpoint"*. Vì vậy đặc tả **đổi cách làm** ở lớp B và lớp D, thay vì thêm
từng điểm theo lời reviewer:

- Lớp B dùng ô **dẫn xuất từ lớp phép biến đổi**, và đòi mỗi lớp phép có nhóm ô riêng, được chứng
  minh bằng phép bậc hai (A1-ii).
- Lớp D **quét trọn một miền hữu hạn** thay cho chọn điểm.

Đây cùng tinh thần với bài học *"danh sách CẤM không bao giờ đủ — đảo thành danh sách CHO
PHÉP"*: thay vì liệt kê chuỗi xấu, ta khai tập hợp **lớp** được phép thử, và đo rằng mỗi lớp có
răng. Chủ kho đã chấp nhận hai cách làm này tại checkpoint (Q3, Q4).

Riêng lớp A, cách làm cũ đã bị chính verdict lượt 22 bác. Chốt AST ở đó là danh sách **CẤM**
(`dk` thiếu `ast.TryStar`) và áp lên **tên** thay vì **thẩm quyền**, đúng lỗi *"phân biệt cách
viết, không phân biệt thẩm quyền"*. Chủ kho quyết ghi nợ, không vá trong packet này (Q1).

Kế thừa thêm hình dạng *"vá đúng chỗ được chỉ rồi bỏ sót đường thứ ba"*: lượt 22 nêu 3 finding,
còn phép đo ra 24 đường sống trong 4 lớp (§2).

## 10. `chua_do_duoc`

- Nội dung của `8d7faef` và `5a071b8` (chốt AST, bản vá F46/F47): không có trong kho. Đo lúc
  15:11:55Z, sau khi fetch đủ 458 ref, `git cat-file` báo không có. Vì thế không đối chiếu được
  F46 phần "kiểu ngoại lệ", nguyên văn F47, và mọi hint.
- `VERDICT.md` lượt 22 (sha256 `1ffe9d6e…42`) và năm tệp patch: chỉ có băm trong comment
  `5911284002`.
- Windows: **không đo** (chủ kho quyết, Q8); nợ `windows-chua-do-o-moi-wp698`. Nhánh
  `_CO_SYMLINK=False` cũng chưa đo, vì container có symlink.
- Kích thước diff của bản vá: chưa thi công thì chưa đo được. Mốc duy nhất có số là hint lượt 22
  (+32/−12), nhưng hint ấy dựng trên `8d7faef` nên không mang sang nền được.
- Ruff 0.15.15 (bản CI ghim): lượt này chỉ đo bằng 0.15.8.
- `t2` không đo được tại chỗ vì thiếu `jsonschema`. Việc này không ảnh hưởng §1.6: `t2` là
  `bo_qua` ở cả 30 dòng, và không dò nào làm đổi ca ngoài bảng.
- Lớp B ngoài ba phép đã khai (chỉ bỏ Zs ngoài ASCII, casefold trên dạng fullwidth…): chưa đo (§2).
- Khối `nang_tran`: không cổng máy nào đọc (§ đầu tệp). Việc lease có chép đúng khối hay không chỉ
  được kiểm bằng mắt.
- Danh tính người ký lease (#566); effort thực tế của executor.

## 11. QUYẾT ĐỊNH CHỦ KHO

**Nguồn:** #698 comment **`5914438647`**, tạo 2026-09-30T15:30:26Z, đọc qua REST lúc 15:30:43Z.
Thân comment có sha256 `4a2dba07da0b23f5542a60cb528950736b25df07dfa1534d2d1c994f283684d0` và
chứa 0 dấu chéo ngược. Comment do **phiên agent đăng hộ chủ kho**, là bản chiếu các câu trả lời
trắc nghiệm của chủ kho trong phiên; tư cách của nó là lời khai có neo (#566). Chủ kho trả lời
làm hai lượt, lúc **15:28:25Z** và **15:30:09Z**. Mọi nhãn trong bảng dưới chép nguyên văn từ
comment ấy.

| lượt | câu hỏi | nhãn chủ kho **chọn** | nhãn **không chọn** | trả lời Q |
|---|---|---|---|---|
| 1 (15:28:25Z) | Phạm vi | "Không, chỉ F49+F50 (Recommended)" | "Có, gộp cả F48" | Q1 |
| 1 (15:28:25Z) | Review | "0/0/0, subagent (Recommended)" | "0/0/0, phiên độc lập" · "0 P1/P2, P3 thành nợ" | Q5 (ngưỡng), Q6 |
| 1 (15:28:25Z) | Nền và CI | "fc852ff, CI 1 lần khi sạch (Recommended)" | "423b4ba, CI 1 lần khi sạch" · "fc852ff, thêm 1 lượt Windows" | Q7, Q8, Q11 |
| 2 (15:30:09Z) | Gói Q còn lại | "Chấp nhận, trừ Q5: lặp tới 0/0/0" | "Chấp nhận cả gói (Recommended)" · "Chấp nhận, trừ Q14: cho HINT" | Q2, Q3, Q4, Q5 (trần), Q9, Q10, Q12, Q13, Q14 |

Hệ quả, theo từng câu hỏi của bản nháp:

- **Q1 — Lớp A (F48 / đường (e)):** không gộp. Ghi nợ `registry-nang-luc-ngoai-cua-so`; muốn
  đóng thì mở packet riêng. Áp tại: header `objective`, §1.2, §2, §4, `land_obligations`.
- **Q2 — `_so_tien_trinh_ban_kinh`:** ghi nợ `so-tien-trinh-nhan-fullwidth`. Áp tại: §1.7, §4,
  A4-d, `land_obligations`.
- **Q3 — Phần mở rộng (TAB, `>=2`, `len(CA)-1`, `hong`, `tien_kiem`):** giữ. Áp tại: M1, M3, §2.
  Nhãn "F49+F50" ở Q1 vì vậy bao gồm các phần mở rộng này.
- **Q4 — Miền M3:** quét trọn `0…len(CA)`. Áp tại: M3, A3.
- **Q5 — Ngưỡng và trần review:** lặp tới 0 P1 · 0 P2 · 0 P3, không giới hạn 2 vòng. Vượt trần
  ADR-0043 là có chủ đích và được ghi bằng khối `nang_tran`. Áp tại: header, khối `nang_tran`,
  A6, S6.
- **Q6 — Đường chạy reviewer:** Sonnet 5.5 chạy subagent ⇒ mức đạt được là `review_deferred`;
  land bằng `human_audited`. Áp tại: header (reviewer, assurance), A6, `land_obligations`.
- **Q7 — CI:** không chạy CI trong vòng lặp; mở PR (CI chạy một lần) khi review sạch. Áp tại:
  `required_checks`, §4, §7, S10.
- **Q8 — Windows:** không chạy. Ghi nợ `windows-chua-do-o-moi-wp698`. Áp tại: `environment`,
  `required_checks` (e), §4, §7, §10.
- **Q9 — `gate-registry` hết trần trên PR #698:** các context bắt buộc xanh là đủ, kèm nợ có neo
  `gate-registry-het-tran-wp698`; chỉ áp cho các run của PR #698. Áp tại: `required_checks` (c),
  S7.
- **Q10 — Thẩm quyền closure:** chủ kho xác nhận bằng một comment trên #698 neo `spec_hash`;
  lease chỉ cấp sau comment ấy. Áp tại: đoạn closure, công thức băm, `depends_on` (4), S2.
- **Q11 — Nền nghiệm thu:** `fc852fff7da37f1669569572b79571446e61c294`. Áp tại: header, §1, A1,
  A4. Đo lại lúc 15:31:57Z: blob `ops/cong_cu_test.py` trùng với `423b4ba`.
- **Q12 — Trần kích thước:** ≤ 3 tệp và ≤ 300 dòng thêm. Áp tại: S5.
- **Q13 — Hồ sơ lượt 22:** đưa vào một nhánh `ops/**` kèm băm; việc này không chặn r1. Áp tại:
  §4, `land_obligations` 8.
- **Q14 — Patch-as-hint:** không dùng; reviewer chỉ mô tả hướng. Áp tại: header (reviewer), §4.

Ba quyết định khác khuyến nghị trong bản nháp của đặc tả này:

- Q5: bản nháp đề 2 vòng; chủ kho chọn lặp tới 0/0/0.
- Q6: bản nháp đề phiên độc lập; chủ kho chọn subagent.
- Q8: bản nháp đề một lượt Windows; chủ kho chọn không.

Nhãn "(Recommended)" trong bảng trên là của câu hỏi phiên điều phối trình cho chủ kho, không phải
khuyến nghị trong bản nháp này.

**Không còn câu hỏi mở nào.**

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
