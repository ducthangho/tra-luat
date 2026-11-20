# wp1461 r3 — B3 của kế hoạch nguồn r4: cổng phát hành đúng candidate + quy trình audit đỏ (CONG-PHAT-HANH-B3)
packet_id: wp1461
revision: 3
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab
mission_issue: 1172
risk: sensitive
review_class: sensitive
executor: claude
environment: cloud (Linux) + chạy Windows-local trên desktop của chủ kho
immutable_acceptance_baseline: **B** — KHÔNG ghim trong tệp này; là OID do Mission revision cài đặc tả và lease cùng ghi, theo luật ở mục "Baseline nghiệm thu"

Trạng thái: thay r2 (cùng đường dẫn, commit `b031bebce687fdb669c250b6c55280b9920f526d`, sha256 `13ee6edfa49120fa38bc5fb6cf6fd9bb20e07946daef320a12b9706dee76d4f6`), bản r2 thay r1 (commit `b8b408d86b3f92a5ea3ae3596ef612481b940b27`, sha256 `7dba9814b224763e7daaf69f61d101d03e499cf575e51113042b5c62b33081e6`). Review spec Codex lượt 1: 2 P1 + 7 P2 + 1 P3; lượt 2 (`wp1461-spec-review-2`): đóng 9/10, SPEC-09 còn một phần, thêm SPEC-11…14 (tổng 4 P2 + 1 P3); r3 sửa cả năm, xem "Thay đổi". CHƯA review lại, CHƯA được chủ kho duyệt băm, chưa có lease. Đặc tả Packet #1461, vai **B3** của Mission #1172 theo **kế hoạch nguồn r4 bản sửa 9** (`ops/specs/wp1172-source-plan-r4/KE_HOACH_NGUON_R4.md`, nhánh `ops/wp1172-plan-r4`, sha256 `0f287ce4369fbeb7b1939daa8de5db7c27c2a4efdc1a21f2fccdd37dc9d83fbe`; "§…" không ghi nguồn là tới tệp ấy). Quyết định Q7 của chủ kho: Mission r84 (`owner_decisions.Q7`); thẩm quyền và trần: Mission r85. Nơi đặc tả này và kế hoạch khác nhau thì đặc tả này thắng cho packet này; mỗi chỗ khác nêu ở "Chỗ lệch có chủ đích". Số dòng trích dẫn đo tại `0f9aa2a2cc697129e1f5be72feddf60986286865` (đầu `master` lúc soạn, `base_sha` của Mission r85); executor đo lại tại B trước khi sửa. Trong tệp này "baseline" luôn nghĩa là B.

**Hợp đồng biên nhận do B1 nắm thẩm quyền:** `ops/specs/wp1460-r1/SPEC.md` revision 2, nhánh `ops/wp1460-r1`, commit `9f7010e0d7c9bda10c2b42dd9889e8a3d3ead9fa`, sha256 `4c1e8ae9c0983edbe26b6fa1ff62012a28cc46c874be372b02cce18118aba480` (viết tắt "B1 §n"). B3 tiêu dùng ĐÚNG hợp đồng ấy, không thêm trường, không tạo biến thể v1. Băm B1 được duyệt khác băm trên ⇒ B3 cần revision mới.

Dòng `tran_kich_thuoc_sensitive` ở đầu tệp kích hoạt trần `ADR-0053`; đã đo lúc soạn: tệp ADR có ở OID ấy, vắng ở cha thứ nhất, OID nằm trên chuỗi first-parent của `origin/master`, kho không shallow.

"Release" = đẩy Package: `scripts/deploy-package.sh --push`, `scripts/deploy-package.ps1 -Push` (kể cả qua `scripts/deploy-package.cmd`). **H** = commit đang checkout tại bước A (mục 2), tức SAU khi `-Pull` của ps1 đã chạy xong. **M** = OID đầu `origin/master` do bước A fetch và ghim.

## Mục tiêu
Sau packet này, một lần đẩy Package chỉ xảy ra khi (1) gói được ràng buộc byte với đúng H, H là đầu `master`, và (2) có bằng chứng máy đọc được rằng full audit (biên nhận B1 `bien_nhan_audit.v1`) cùng lượt push `ci.yml` đã xanh trên đúng H — hoặc chủ kho tự tay dùng đường khẩn cấp có xác nhận TTY. Không có ngoại lệ do máy cấp. Packet land ở chế độ `warning_only`; bật chế độ chặn là một PR riêng về sau (mục 8).

## Hợp đồng

### 1. Bất biến
- **I1 — Chỉ siết.** Gate 8 bước, same-SHA ×2, verify nội dung gói, quét bí mật, chốt chống thụt lùi (rc 3), byte-match sau đẩy giữ nguyên quyết định trên cùng đầu vào. `scripts/deploy-guard.ps1` dự kiến diff = 0. Đổi DUY NHẤT ở mã có sẵn: mã thoát của nhánh "tụt sau master" của ps1 khi có `-Push` (mục 3).
- **I2 — Build-only không đổi.** Không `--push`/`-Push`: mã thoát, việc sinh zip và byte của zip BẰNG baseline trên cùng đầu vào, kể cả khi cây bẩn, khi không lấy được H, khi `git archive` lỗi, khi fetch lỗi. Ở build-only các bước của B3 chỉ IN chẩn đoán (H, tree, "cây bẩn/lệch H: gói này KHÔNG được phép đẩy") và mọi lỗi của chúng bị nuốt thành một dòng `khong_do_duoc`. Hai lệch có sẵn giữa hai nền KHÔNG thuộc packet này và nằm ngoài ma trận parity: ps1 build-only thoát 1 khi tụt sau master còn sh không kiểm; `deploy-guard.ps1` thoát 4 khi không đọc được Drive còn sh chỉ cảnh báo.
- **I3 — Không ngoại lệ do máy cấp.** Không cờ, biến môi trường, tệp ngoài kho, comment, nhãn hay bản ghi nào làm cổng nới, ngoài đúng hai thứ: tệp chế độ đọc từ M (mục 8) và cờ khẩn cấp có xác nhận TTY (mục 7). `--force-older`/`-ForceOlder` và `--no-test`/`-NoTest` không miễn phép kiểm nào của B3.
- **I4 — Ba trạng thái.** Mọi phép đọc cho ra `dat` · `khong_dat` · `khong_do_duoc`; `khong_do_duoc` không bao giờ thành `dat`. Ở chế độ chặn chỉ `dat` được đẩy.
- **I5 — Một nguồn cho logic dùng chung.** Đọc REST, kiểm biên nhận, ràng buộc byte, ghi nhật ký nằm ở MỘT tệp Python cho cả hai nền (`ops/cong_phat_hanh.py`, tiền lệ `scripts/pkg_secret_scan.py`). Hai script chỉ gọi nó, xử lý mã thoát, và tự làm phần TTY.
- **I6 — Không seam mới đổi quyết định.** Không biến môi trường hay tham số nào đổi địa chỉ API, kho, workflow, chế độ, hay bỏ bước. Test tiêm transport bằng tham số hàm Python; ở mức script dùng seam interpreter có sẵn (`TL_PYTHON`, `-Python`).
- **I7 — Bí mật.** Token không lên argv, không vào nhật ký, không in ra; `Authorization` chỉ gửi tới `api.github.com`.

### 2. Điểm chèn (số dòng đo tại `0f9aa2a`, đo lại tại B)
| Bước | `deploy-package.sh` | `deploy-package.ps1` | Việc của B3 |
|---|---|---|---|
| A. Ghi H, ghim M | sau khối `core.abbrev` (dòng 91–100), trước bước 1 (dòng 109) | NGAY SAU khối tụt-sau/`-Pull` (dòng 157–175), trước bước 1 (dòng 177) | H (40 hex), tree, cây sạch, fetch và ghim M; push: vi phạm ⇒ rc 7 trước khi build; build-only: chỉ in |
| B. Ràng buộc byte | sau bước 3 (dòng 258–259), trước nhánh build-only (dòng 262) | sau `finally` của bước 3 (dòng 324–326), trước dòng 329 | gói ↔ H; push: lệch ⇒ rc 7; build-only: chỉ in |
| C. Cổng audit | sau chốt chống thụt lùi (dòng 280–294), trước `drive-push` (dòng 302) | sau lời gọi `deploy-guard.ps1` (dòng 338–340), trước `drive-push` (dòng 342) | fetch, đòi master = M; đọc chế độ từ M; bằng chứng trên H; hỏi TTY nếu có cờ khẩn cấp |
| D. Kiểm lại | ngay trước `drive-push`, sau C, không lệnh nào chen giữa | như bên | HEAD = H, tree, cây sạch, sha256 zip = digest đã ghi, fetch lại và master = M |
| E. Ghi kết cục | mọi lối thoát kể từ sau khi sự kiện `phan_lop` đã ghi (D hỏng, đẩy hỏng, sau bước 5) | như bên | nối sự kiện `ket_cuc` cho ĐÚNG `id` của lần thử (mục 6: mỗi lần thử có hai sự kiện) |

Thứ tự C → D → `drive-push` là bất biến. Bước C và D chỉ tồn tại trong nhánh push.

### 3. Ràng buộc byte gói ↔ H (cưỡng chế ở push, cả hai chế độ)
- **Cây sạch (A và D):** `git status --porcelain=v1 -z --untracked-files=all` rỗng (không `-uno`). Tệp bị ignore được phép tồn tại. Lệnh lỗi ⇒ `khong_do_duoc`.
- **H là đầu master, và master không được dịch chuyển.** A: `git fetch origin +refs/heads/master:refs/remotes/origin/master` phải thành công, kho không shallow; M = OID vừa fetch; đòi H = M. C và D: fetch lại, đòi OID vừa fetch = M. Master dịch chuyển (tiến, lùi hay rẽ) giữa A và lúc đẩy ⇒ rc 7, không đẩy, ở cả hai chế độ và cả khi có cờ khẩn cấp (đúng §B3 "ref di chuyển giữa lúc kiểm và lúc đẩy ⇒ chặn"). Fetch lỗi ⇒ `khong_do_duoc` ⇒ rc 7.
- **Thứ tự tiền kiểm push, để hai nền trả CÙNG mã:** H tụt sau, đi trước, hoặc rẽ khỏi M ⇒ rc 7 ở cả hai nền. ps1: khi có `-Push`, hai nhánh `exit 1` của khối dòng 157–175 (tụt sau mà không `-Pull`; `-Pull` không fast-forward được) trả 7 thay vì 1, thông điệp giữ nguyên; không `-Push` thì giữ 1. `-Pull` thành công ⇒ H là commit SAU khi fast-forward. sh không có `-Pull`.
- **Ảnh chụp H:** `git archive H` giải vào thư mục tạm ngoài kho. Chọn phương án "so tập tệp + byte phát hành với blob tại H" của §B3; KHÔNG build từ ảnh chụp.
- **Phép so, cả hai phải đạt:** (a) mọi tệp trong zip (bỏ thư mục đỉnh) có trong ảnh chụp H và trùng byte; tệp không có ở H ⇒ `khong_dat`; (b) tập đường dẫn trong zip BẰNG tập đường dẫn của `RELEASE_MANIFEST.json` tại H (cộng chính tệp manifest nếu đo thấy nó không tự liệt kê). In ba số: tệp trong zip, tệp đã so, tệp trong manifest; ba số vào bảng parity.
- **Digest gói:** sha256 của zip (`S1` có sẵn), ghi vào nhật ký. D tính lại từ tệp trên đĩa; lệch ⇒ rc 7. Bước 5 có sẵn giữ nguyên.

### 4. Bằng chứng trên H (bước C)
Kho cố định trong mã: `ducthangho/tra-luat`. Mọi OID so với H là so đủ 40 ký tự.

**4.1 Lượt push `ci.yml` trên H.** Liệt kê lượt của `.github/workflows/ci.yml` với `head_sha=H`, `event=push`, `branch=master`. Lấy lượt mới nhất: `status=completed`, `conclusion=success`; mọi job (`filter=latest`) kết luận `success` hoặc `skipped`, số job ≥ 1. Thêm tập tên `CHECK_BAT_BUOC` (hằng trong mã; ở packet này là tập RỖNG có chú thích "chưa đo bảo vệ master", giá trị thật do PR bật chặn điền từ hồ sơ đo của chủ kho — mục 8): mỗi tên phải có check run trên H do app `github-actions` tạo, thuộc đúng lượt ấy, kết luận `success`. Không có lượt, lượt `cancelled`/đỏ, check vắng ⇒ `khong_dat`. Lượt `pull_request` không thay được lượt push.

**4.2 Biên nhận B1 — ba loại nguồn, không trộn.**

| L | Từ BIÊN NHẬN (đường dẫn v1, B1 §2) | HẰNG hợp đồng | Đọc ĐỘC LẬP qua REST / git |
|---|---|---|---|
| L1 | `schema` | `bien_nhan_audit.v1` | — |
| L2 | `kho`, `kho_id` | tên kho cố định | `run.repository.full_name`, `run.repository.id` |
| L3 | `workflow.duong_dan` | `.github/workflows/ci-dot-bien-du.yml` | `run.path` |
| L4 | `su_kien.ten`, `su_kien.cron`, `su_kien.khung_danh_nghia_utc`, `su_kien.run_created_at` | `ten` ∈ {`schedule`, `workflow_dispatch`} | `run.event` |
| L5 | `su_kien.sha`, mọi `job[].checkout_sha`, mọi `job[].checkout_tree` | — | `run.head_sha`; H và tree của H từ git |
| L6 | `luot.run_id`, `luot.run_attempt`, `nhom_muc[].manh[].attempt_ben_san_xuat` | — | `run.id`, `run.run_attempt` (attempt CAO NHẤT) |
| L7 | `kiem_ke_job`, `nhom_muc[].kiem_ke_muc` | nhóm `nhanh_don_duoc` phải có | tập tên job REST (`filter=latest`) = `kiem_ke_job.ky_vong` |
| L8 | `job[].ket_luan_rest` của job TRƯỚC (`tu_than: false`) | — | kết luận MỌI job REST, **kể cả `bien-nhan-audit`** |
| L9 | `dinh_danh_definition` | — | mục 4.3 |
| L10 | `job[].dau_job`, `manh[].artifact` | — | `digest` REST + byte tải về |
| L11 | `ket_cuc.ket_luan_tong`, `ok` | `xanh`, `true` | — |
| L12 | `dau_hieu_duong` | mỗi cặp `a/b` có a = b ≥ 1 | — |
| L13 | — | artifact `bien-nhan-audit-<run_id>-<run_attempt>`, tệp `bien_nhan_audit.json` | danh sách artifact của run |

Một lượt audit trên H là `dat` ⇔ ĐỒNG THỜI (B1 §6 luật 1–6):
1. REST: run `path` = L3, `head_sha` = H, `event` ∈ L4, `completed`/`success`; mọi job của `filter=latest` `success`, gồm job thu `bien-nhan-audit`. Bản ghi của job thu trong biên nhận là bản tạm (`ket_luan_rest: null`) nên KHÔNG dùng để kết luận về job thu.
2. Biên nhận lấy từ artifact của attempt CAO NHẤT của run (tên theo L13, đúng một tệp). Attempt cao nhất không có biên nhận hợp lệ ⇒ không `dat`, kể cả khi attempt cũ có biên nhận hợp lệ.
3. Hình và tính nhất quán nội tại: chạy bộ kiểm của B1 `python .claude/dev/ci_dang_ky_test.py --kiem-bien-nhan-audit <tệp>` từ cây của H, đòi rc 0. B3 KHÔNG viết bộ kiểm hình thứ hai. Không chạy được bộ kiểm ⇒ `khong_do_duoc`. `schema` khác, khoá lạ, thiếu khoá, sai kiểu ⇒ không `dat`.
4. `ok == true`, L11 = `xanh`, L12 đạt; `luot`, `su_kien.sha`, `kho`, `kho_id`, `workflow.duong_dan` khớp REST; L5: mọi `checkout_sha` = H và mọi `checkout_tree` = tree của H, không giá trị nào `null`; L7: hai kiểm kê `do_duoc`, `thieu`/`thua`/`trung` rỗng, và tập tên job REST bằng `ky_vong`; L8: mọi job trước `success` ở cả biên nhận lẫn REST.
5. Khớp byte (B1 §6 luật 5): sha256(gói biên nhận tải qua REST) = `digest` REST của nó; với từng artifact mảnh được chọn và từng dấu job, sha256(gói tải về) = `digest` REST, và sha256(tệp bên trong) = `sha256_noi_dung` ghi trong biên nhận. Artifact hết hạn ⇒ coi là vắng ⇒ không `dat`.
6. Chạy lại RIÊNG job thu (biên nhận attempt 2, mảnh vẫn attempt 1) là hợp lệ; B3 không tự suy luật attempt nào ngoài phép 1–5 (luật A của B1 do bộ kiểm và job thu cưỡng chế).

B3 không áp luật tuổi bằng chứng (việc của B2); L4 chỉ ghi vào nhật ký. Lượt audit đỏ đứng cạnh một lượt `dat` trên H được in và ghi nhật ký, không tự chặn (mục 9 xử lý). Trong một lượt: đọc không trọn ⇒ `khong_do_duoc`; đọc trọn mà sai ⇒ `khong_dat`. Cách ghép các phép đọc thành kết quả bước C: mục 4.5.

**4.3 Definition (B1 §6 luật 7–8).**
- `trang_thai == "measured"`: `blob_oid` = `git rev-parse H:<L3>` và `sha256` = sha256 của `git show H:<L3>` tính tại chỗ. Lệch ⇒ `khong_dat`.
- `not_measured`: dùng artifact A4, chỉ đọc, không dispatch. **Định vị:** `GET /actions/artifacts?name=workflow-definition-<run_id lượt audit>`; trong các artifact trả về, lấy cái thuộc lượt đo MỚI NHẤT (theo `created_at` của lượt). Lượt mới nhất không hợp lệ ⇒ không `dat` (không lùi về lượt cũ hơn). **Kiểm:** gọi nguyên hàm `nhap_wd` của `ops/ci_provenance.py` (không chép, không sửa tệp ấy) với transport của B3 — nó kiểm lượt đo (`path` = `.github/workflows/ops-do-workflow-definition.yml`, `workflow_dispatch`, `success`, đúng kho, `head_sha` không đi trước nhánh mặc định), đúng một artifact chưa hết hạn, `digest` khớp, gói chỉ có `wd.json`, `wd/1` khoá đóng, `repo`/`run_id`/`path` khớp, `trang_thai == "passed"`, rồi tự tải nội dung tại `oid_dinh_nghia` và tính lại `blob`/`sha256`. **B3 kiểm thêm:** `run_attempt_luc_do` = attempt cao nhất của lượt audit; `sha256` thu được = sha256 của `git show H:<L3>`; nếu biên nhận có `workflow_sha` khác `null` thì nó phải bằng `oid_dinh_nghia`. `head_sha` của lượt đo ĐƯỢC PHÉP khác H. Transport của B3 không dùng được với `nhap_wd` mà không sửa `ops/ci_provenance.py` ⇒ DỪNG, báo điều phối.

**4.4 Nhịp tim B2.** Đọc comment của Issue theo dõi B2 (số Issue và dạng dấu do đặc tả B2 chốt; hằng `ISSUE_NHIP_TIM` ở packet này là `None`). `None`, cũ hơn 24 giờ, hoặc không đọc được ⇒ CHỈ in cảnh báo và ghi `nhip_tim` vào nhật ký; không bao giờ vào quyết định, ở cả hai chế độ.

**4.5 Luật ghép ba trạng thái (đầy đủ, không phụ thuộc thứ tự).** Bước C đánh giá ĐỦ mọi điều kiện và mọi lượt ứng viên, không dừng sớm; kết quả và mã lý do phải giống nhau với mọi thứ tự duyệt.
- **Phép VÀ** (dùng cho: các phép con của 4.1; các phép con 1–5 + 4.3 của MỘT lượt audit; và tầng trên cùng `C = P VÀ Q`, với P = 4.1, Q = audit): có ít nhất một `khong_dat` ⇒ `khong_dat`; không thì có ít nhất một `khong_do_duoc` ⇒ `khong_do_duoc`; không thì `dat`.
- **Phép HOẶC** (dùng cho Q, trên tập lượt audit ứng viên của H): có ít nhất một lượt `dat` ⇒ `dat`; không thì nếu phép liệt kê lượt KHÔNG trọn (E1 lỗi, phân trang cụt) hoặc có ít nhất một lượt `khong_do_duoc` ⇒ `khong_do_duoc`; không thì (liệt kê trọn và mọi lượt `khong_dat`, hoặc liệt kê trọn và 0 lượt) ⇒ `khong_dat`. Liệt kê không trọn mà đã thấy một lượt `dat` ⇒ vẫn `dat`.
- P chỉ xét lượt push MỚI NHẤT (không HOẶC): liệt kê không trọn ⇒ `khong_do_duoc`; liệt kê trọn, 0 lượt ⇒ `khong_dat`.
- 4.4 (nhịp tim) không tham gia phép ghép nào.

| P (CI push) | Q (audit) | C | rc ở `chan` |
|---|---|---|---|
| `dat` | `dat` | `dat` | đẩy |
| `khong_dat` | bất kỳ | `khong_dat` | 5 |
| bất kỳ | `khong_dat` | `khong_dat` | 5 |
| `khong_do_duoc` | `dat` hoặc `khong_do_duoc` | `khong_do_duoc` | 6 |
| `dat` | `khong_do_duoc` | `khong_do_duoc` | 6 |

- **Mã lý do tất định.** Mỗi phép con có một mã cố định. Nhật ký ghi TOÀN BỘ danh sách (điều kiện, lượt, phép con, trạng thái, mã), xếp theo khoá (P trước Q; `run_id` tăng dần; số thứ tự phép con). Mã lý do CHÍNH = phần tử đầu tiên của danh sách ấy có trạng thái bằng trạng thái của C (với C = `dat`: mã `dat` kèm `run_id` nhỏ nhất trong các lượt audit `dat`).

### 5. Bảng năng lực endpoint
B3 chỉ gọi GET; không GraphQL, không ghi, không đọc bảo vệ nhánh, biến hay secret. Đường dẫn dưới `/repos/{kho}`.

| # | Endpoint | Quyền | Dùng cho | Lỗi ở chế độ chặn |
|---|---|---|---|---|
| E1 | `/actions/workflows/{tệp}/runs?head_sha=…` | Actions: read | 4.1, 4.2 | chặn |
| E2 | `/actions/runs/{id}`, `/actions/runs/{id}/jobs?filter=latest` | Actions: read | 4.1, 4.2, 4.3 | chặn |
| E3 | `/actions/runs/{id}/artifacts` | Actions: read | 4.2, 4.3 | chặn |
| E4 | `/actions/artifacts/{id}/zip` | Actions: read | 4.2, 4.3 | chặn |
| E5 | `/commits/{H}/check-runs` | Checks: read | 4.1 | chặn |
| E6 | `/commits/{H}` | Contents: read | xác nhận H và tree phía máy chủ | chặn |
| E7 | `/issues/{n}/comments` | Issues: read | 4.4 | chỉ cảnh báo |
| E8 | `/actions/artifacts?name=…` | Actions: read | 4.3 định vị A4 | chặn khi cần A4 |
| E9 | `/` (chính kho), `/git/ref/heads/{nhánh mặc định}`, `/compare/{a}...{b}`, `/contents/{path}?ref={oid}` | Metadata, Contents: read | 4.3, do `nhap_wd` gọi | chặn khi cần A4 |

Ba lớp phản hồi, luật riêng từng lớp:
- **J — JSON từ `api.github.com`** (mọi endpoint trừ thân tải của E4): nhận 2xx chỉ khi có `X-GitHub-Request-Id` và JSON đúng kiểu. 2xx không dấu, 3xx, 401/403/404/5xx, JSON hỏng, hết giờ ⇒ `khong_do_duoc` kèm mã lý do phân biệt "GitHub trả" với "không có dấu GitHub". Phân trang có giới hạn (hằng số trang × 100); còn `rel="next"` sau giới hạn, hoặc số mục gom được khác `total_count` ⇒ `khong_do_duoc`.
- **R — chuyển hướng của E4:** phản hồi 302 từ `api.github.com`, có `X-GitHub-Request-Id`, `Location` là URL `https`. Tối đa 3 lần chuyển hướng. Mã khác ⇒ `khong_do_duoc`.
- **S — tải từ host lưu trữ:** KHÔNG gửi `Authorization`; không đòi dấu GitHub, không đòi JSON. Nhận khi: 200, kích thước ≤ trần (hằng, ghi trong mã), thân là ZIP mở được, và sha256(thân) = `digest` REST của artifact. Sai một điều ⇒ không `dat` (`khong_do_duoc` khi không tải trọn; `khong_dat` khi tải trọn mà digest lệch).
- Mỗi lời gọi có hạn giờ; thử lại có trần cho lỗi mạng/5xx/429; tổng thời gian có trần.
- **Nguồn token:** thứ tự là hằng trong mã, do executor ĐO trên từng máy rồi chốt (ứng viên: `gh auth token`, `GITHUB_PAT`, `GH_TOKEN`, `GITHUB_TOKEN`, không token). Chỉ ghi TÊN nguồn. Nguồn cho 401 thì thử nguồn kế; hết nguồn ⇒ `khong_do_duoc`.
- **Lệnh `do-nang-luc`:** gọi từng endpoint E1–E9 một lần trên một run tham chiếu, kể cả một lượt tải E4 trọn vẹn; xuất JSON (mỗi endpoint: mã, có dấu GitHub, số trang, `total_count`, host chuyển hướng, nguồn token theo tên, giờ, OS/Python, có PyYAML không). Hồ sơ là điều kiện bật chặn (mục 8), không phải bằng chứng audit.

### 6. Quyết định, mã thoát, nhật ký G8
| Kết quả bước C | Chế độ `warning_only` | Chế độ `chan` |
|---|---|---|
| `dat` | đẩy; lớp `audit_passed` | đẩy; lớp `audit_passed` |
| `khong_dat` | đẩy; lớp `warning_only`; cảnh báo nổi bật | rc 5, không đẩy |
| `khong_do_duoc` | đẩy; lớp `warning_only`; cảnh báo nổi bật | rc 6, không đẩy |
| không `dat` + cờ khẩn cấp được xác nhận (mục 7) | đẩy; lớp `owner_emergency` | đẩy; lớp `owner_emergency` |

- **Mã thoát, một bảng thẩm quyền, giống nhau ở hai nền:** 0 xong · 1 gate đỏ · 2 build/verify hỏng hoặc sai đối số · 3 đẩy hỏng/chặn thụt lùi · 4 không đọc được Drive (chỉ đường ps1, có sẵn) · 5 cổng audit chặn · 6 không đo được ở chế độ chặn · 7 ràng buộc byte/H/cây/master vi phạm · 8 đường khẩn cấp bị từ chối. Bảng này chép vào chú thích đầu `deploy-package.sh`, `deploy-package.ps1`, `deploy-package.cmd` và vào runbook.
- **`deploy-package.cmd`: chỉ sửa dòng `rem`.** Mọi dòng không bắt đầu bằng `rem` phải trùng byte với baseline (so trên blob), EOL giữ CRLF theo `.gitattributes`.
- **Nhật ký:** `scripts/.tl_state/deploy/nhat-ky-day.jsonl` (đã bị ignore), chỉ nối thêm, mỗi dòng một sự kiện JSON, `flush` + `fsync`. Phạm vi: mọi lần thử push ĐÃ TỚI bước C (thoát rc 7 ở A/B và rc 2/8 lúc phân tích đối số không vào nhật ký). Mỗi lần thử có `id` riêng và ĐÚNG HAI sự kiện, theo thứ tự: (1) `phan_lop`, ghi khi C có quyết định và TRƯỚC `drive-push`: giờ UTC, máy, nền, H, tree, M, digest gói, VERSION, chế độ, kết quả C, mã lý do chính + danh sách đầy đủ (4.5), run_id/attempt của lượt `ci.yml` và lượt audit đã dùng, L4, `nhip_tim`, lớp (`audit_passed` · `owner_emergency` · `warning_only` · `bi_chan`), lý do khẩn cấp; (2) `ket_cuc`, cùng `id`: `da_day_khop_byte` · `day_hong` · `khong_day` kèm mã thoát. Lần thử bị chặn ở C (rc 5, 6, 8): `phan_lop` lớp `bi_chan` rồi `ket_cuc` `khong_day`. Lần thử qua C nhưng hỏng ở D: `phan_lop` giữ lớp đã định rồi `ket_cuc` `khong_day` (rc 7). Lệnh `dem-g8` nối hai sự kiện theo `id`: một lần đẩy được đếm ĐÚNG MỘT LẦN, vào lớp của `phan_lop`, khi và chỉ khi `ket_cuc` = `da_day_khop_byte`; `id` có `phan_lop` mà thiếu `ket_cuc` (tiến trình chết giữa chừng) báo riêng là `dang_do`, không đếm vào dòng nào; `id` trùng hoặc `ket_cuc` không có `phan_lop` ⇒ lệnh thoát khác 0. Nhật ký là tệp cục bộ từng máy; gom hai máy là việc của runbook.

### 7. Đường khẩn cấp của chủ kho
- **Tên cờ (đóng băng):** sh `--khan-cap-chu-kho` · ps1 `-KhanCapChuKho` (switch). Không kèm `--push`/`-Push` ⇒ rc 2 với một thông điệp riêng của B3; đây là phép kiểm ĐẦU TIÊN sau khi gắn tham số, trước phép kiểm TTY và trước mọi việc khác (nó cũng là probe gắn tham số `PB` của nghiệm thu 13).
- **Lớp 1 — trong script, máy cưỡng chế, không chứng minh danh tính.** Có cờ ⇒ ngay khi phân tích đối số kiểm stdin VÀ stdout là TTY tương tác (sh: `[ -t 0 ] && [ -t 1 ]`; ps1: `[Console]::IsInputRedirected` và `IsOutputRedirected` đều false, phiên không `-NonInteractive`); không đạt ⇒ rc 8 trước mọi việc khác. Tại C, nếu kết quả không `dat`: kiểm TTY lần nữa, in H + digest + kết quả, hỏi một dòng lý do (khác rỗng, ≤ 200 ký tự), rồi đòi gõ lại ĐÚNG 40 ký tự hex thường của H (chỉ bỏ ký tự xuống dòng cuối). Sai hoặc EOF ⇒ rc 8, không đẩy, ghi `bi_chan`. Đúng ⇒ ghi `owner_emergency`, đi tiếp tới D. Kết quả đã `dat` ⇒ không hỏi, lớp `audit_passed`. Cờ khẩn cấp CHỈ thay bằng chứng của mục 4; nó không miễn mục 3, bước D, chốt chống thụt lùi, quét bí mật, byte-match sau đẩy.
- **Lớp 2 — hook PreToolUse, chỉ HỎI LẠI.** Thêm vào `RISKY` của `.claude/hooks/pretooluse_guard.py` (dòng 13–54) hai luật trả `permissionDecision=ask`: (a) chuỗi `--khan-cap-chu-kho` ở bất kỳ đâu trong lệnh; (b) lệnh có nhắc `deploy-package.ps1` hoặc `deploy-package.cmd` (không phân biệt hoa thường) VÀ có một token `-` + TIỀN TỐ KHÁC RỖNG của `KhanCapChuKho`, không phân biệt hoa thường, có hoặc không `:<giá trị>` (`-K`, `-kh`, `-KHANCAP`, `-KhanCapChuKho:$true`). Lý do hook in ra nêu "phiên AI không dùng cờ này" và trỏ runbook. Việc mọi tiền tố ấy gắn vào tham số được ĐO bằng nhóm probe `PB` của nghiệm thu 13, trên cả hai runtime Windows. B3 không khai gì về cách từng chế độ quyền hay phiên không tương tác xử lý `ask` (CHƯA ĐO; không nghiệm thu nào dựa vào nó). Lớp này KHÔNG phủ: Codex và nền agent khác; lệnh trong tệp script, ghép qua biến hoặc splatting; phiên không nạp hook; terminal của người. Nhánh `deny` của agent chỉ-đọc không đổi.
- **Lớp 3 — cấm theo quy trình, không do máy cưỡng chế.** "Phiên AI không dùng cờ khẩn cấp, kể cả khi được hỏi lại và được đồng ý" ghi ở runbook (mục 9). `CLAUDE.md` không thuộc packet này.
- Cờ và luật hook land trong CÙNG PR.

### 8. Chế độ và điều kiện bật chặn
- **Nguồn chế độ:** tệp một dòng `ops/cong_phat_hanh.che_do`, đọc bằng `git show M:ops/cong_phat_hanh.che_do` tại bước C — không từ cây làm việc, không từ biến môi trường. Chỉ đúng chuỗi `warning_only` (cho phép một ký tự xuống dòng cuối) mới cho chế độ cảnh báo; `chan`, rỗng, vắng, lạ, không đọc được ⇒ `chan`. Vì H = M và bước D đòi master vẫn = M, chế độ dùng ở C không thể cũ lúc đẩy.
- **Packet này land với `warning_only`.** Bật `chan` là MỘT PR riêng về sau, ngoài packet này, chỉ khi đủ: (a) hồ sơ `do-nang-luc` của CẢ HAI máy deploy — container Linux (sh) và desktop Windows của chủ kho (ps1) — mọi endpoint E1–E6, E8, E9 đọc trọn; VM chỉ dùng cho parity, không phải máy deploy; (b) hồ sơ đo bảo vệ `master` bằng quyền quản trị của chủ kho (cấm force-push/xoá, ai vượt được, danh sách check bắt buộc → `CHECK_BAT_BUOC`), đo lại hằng tháng theo runbook; (c) B1 đã land và có ít nhất một biên nhận thật `dat` qua bước C trên cả hai máy. B3 không đọc bảo vệ nhánh lúc deploy; trôi cấu hình giữa hai lần đo là rủi ro tồn dư đã nhận ở Q7(b).
- **Rủi ro tồn dư:** script chạy từ cây của H nên một H có trước B3 không có cổng (chỉ còn chốt chống thụt lùi và quy trình); người ngồi máy sửa được script; TTY không chứng minh ai gõ; `TL_PYTHON`/`-Python` là seam có sẵn; artifact hết hạn làm H cũ không còn `dat`. Mục tiêu là chặn tay trượt và phiên tự động.

### 9. Tài liệu quy trình (dev-side, không vào gói)
`docs/QUY_TRINH_PHAT_HANH_B3.md` (MỚI): bảng mã thoát; quy trình audit đỏ đúng §B3 (owner = chủ kho; xác nhận ≤ 2 giờ làm việc; ≤ 1 ngày làm việc có Issue nêu H, ID đỏ, phân loại code/test/hạ tầng, tái hiện tối thiểu hoặc lý do chưa tái hiện; tối đa 1 lần chạy lại hạ tầng, giữ attempt đỏ; bisect chỉ trên commit dựng được, không dựng được ghi `not_testable`; khi công tắc A+1 đã tồn tại thì đóng nó theo runbook công tắc và không merge thay đổi cùng vùng; release bị chặn tới khi có audit xanh đúng candidate hoặc chủ kho dùng đường khẩn cấp); ba lớp quanh cờ khẩn cấp, mỗi lớp nói đúng mức của nó; danh sách kiểm bật chặn; runbook đo bảo vệ `master` hằng tháng; cách gom nhật ký hai máy để báo G8 ba dòng TÁCH; kịch bản tay cho TTY trên console Windows.

### Chỗ lệch có chủ đích so với kế hoạch r4
1. Lớp 1 giữ trong script; phần còn lại gom vào helper dùng chung (I5).
2. Lỗi ràng buộc byte/H/master chặn cả ở `warning_only`.
3. Chế độ đọc từ M, mặc định đóng — kế hoạch chỉ nói "chưa đo ⇒ `warning_only`, ghi rõ".
4. H phải BẰNG đầu master (kế hoạch cho phép "bằng đầu nhánh hoặc tổ tiên"): chặt hơn, giữ luật mục 2 §Quy ước deploy của `CLAUDE.md`.
5. Write set rộng hơn danh sách của Mission r85 và vượt trần `ADR-0053` (xem "Kích thước và `nang_tran`").
6. Lệnh tìm A4 dùng lọc theo tên artifact (E8) thay vì duyệt từng lượt như B1 §6 luật 8 mô tả; kết quả chọn ("lượt MỚI NHẤT có artifact tên đúng") và mọi phép kiểm giữ nguyên.

## Nghiệm thu
1. **Hai chiều + ba trạng thái cho từng phép kiểm** của mục 3, 4, 5: ít nhất một ca `dat`, một `khong_dat`, một `khong_do_duoc`; ca đạt đòi đúng mã lý do, không chỉ mã thoát. **Ghép trạng thái (4.5):** mỗi dòng của bảng 4.5 một ca; thêm các ca hỗn hợp, mỗi ca chạy ở HAI thứ tự duyệt và đòi cùng kết quả, cùng mã lý do chính, cùng danh sách: CI đỏ + endpoint audit không đọc được (⇒ `khong_dat`, rc 5); CI không đọc được + audit đỏ (⇒ `khong_dat`); CI không đọc được + audit `dat` (⇒ `khong_do_duoc`, rc 6); một lượt audit sai hẳn + một lượt không đọc được, không lượt nào `dat` (⇒ `khong_do_duoc`); hai lượt đều sai hẳn (⇒ `khong_dat`); một lượt không đọc được + một lượt `dat` (⇒ `dat`); liệt kê lượt cụt + đã thấy một lượt `dat` (⇒ `dat`); liệt kê cụt + chỉ thấy lượt sai (⇒ `khong_do_duoc`); trong một lượt: một phép con sai + một phép con không đọc được (⇒ lượt `khong_dat`). **Nhật ký:** lần đẩy thành công, bị chặn ở C, hỏng ở D, đẩy hỏng — mỗi ca đúng hai sự kiện cùng `id` đúng thứ tự; `dem-g8` đếm lần thành công đúng một lần; `phan_lop` mồ côi ⇒ `dang_do`; `id` trùng ⇒ lệnh đỏ.
2. **Build-only (I2), A/B base và candidate dựng trong MỘT lệnh:** cây sạch và cây bẩn (sửa một tệp phát hành), mỗi cái có và không `--no-test`/`-NoTest`; thêm candidate với `git archive` lỗi và fetch lỗi. Hai vế: cùng mã thoát, cùng sha256 zip, 0 lời gọi `drive-push`.
3. **Cây, H, master (push):** tệp theo dõi bị sửa; bị xoá; tệp chưa theo dõi ngoài tập phát hành; tệp chưa theo dõi trong thư mục phát hành; tệp ignore bị gom vào zip (⇒ chặn ở phép so (a)); tệp ignore trong `scripts/.tl_state/` (⇒ không chặn); HEAD đổi giữa A và D; tệp bị sửa giữa build và D; zip bị thay giữa B và D; zip thừa/thiếu một tệp so với manifest tại H; H tụt sau M không `-Pull` (⇒ 7 ở cả hai nền); H đi trước M; H rẽ khỏi M; ps1 `-Pull` thành công (H = commit sau fast-forward, đi tiếp); ps1 `-Pull` không fast-forward được (⇒ 7); master TIẾN giữa A và C (⇒ 7); master tiến giữa C và D (⇒ 7); master bị ép lùi (⇒ 7); **master tiến giữa C và D sang commit đổi tệp chế độ thành `chan`, bằng chứng audit vắng, C đã cho qua ở `warning_only` ⇒ rc 7, đúng 0 lời gọi `drive-push`**; kho shallow; fetch lỗi.
4. **Biên nhận, dùng fixture CHUNG của B1** (`ops/specs/wp1460-r1/hop_dong/fixture.json`, đọc tại chỗ, không chép): ca dương `goc`; ca dương "chạy lại riêng job thu, mảnh giữ attempt cũ"; mọi ca của fixture cho đúng kết quả `dat`/không `dat` suy từ `hinh_hop_le` và `ok`. Thêm ca do B3 dựng trên `goc`: không có lượt audit trên H; có lượt nhưng không có artifact biên nhận; biên nhận chỉ có ở attempt cũ; `su_kien.sha` ≠ H; một `checkout_sha` ≠ H; `checkout_tree` sai; `checkout_sha` `null`; `kho` sai; `kho_id` lệch REST; `workflow.duong_dan` sai; `schema` lạ; khoá lạ; thiếu khoá; `ok: false`; `ket_luan_tong` khác `xanh`; `kiem_ke_job` `khong_do_duoc`; `thieu` khác rỗng; tập job REST khác `ky_vong`; **biên nhận xanh nhưng REST nói job thu `failure`**; biên nhận xanh nhưng REST nói một job trước đỏ; run REST chưa `completed`; digest gói biên nhận lệch; `sha256_noi_dung` của một mảnh lệch; của một dấu job lệch; artifact mảnh hết hạn; bộ kiểm B1 không chạy được (⇒ `khong_do_duoc`); hai lượt trên H một đỏ một `dat` (⇒ `dat`, có in lượt đỏ).
5. **Definition:** `measured` khớp; `blob_oid` lệch; `sha256` lệch; `not_measured` + A4 hợp lệ có `head_sha` lượt đo KHÁC H (⇒ `dat`); A4: không có artifact, hết hạn, sai workflow lượt đo, lượt đo không phải `workflow_dispatch`, lượt đo đỏ, `head_sha` lượt đo đi trước nhánh mặc định, `run_id` đích sai, digest lệch, gói có tệp thừa, `wd/1` thiếu khoá, `trang_thai` khác `passed`, `run_attempt_luc_do` cũ hơn attempt cao nhất, `sha256` khác H, `workflow_sha` của biên nhận khác `oid_dinh_nghia`, lượt đo mới nhất hỏng trong khi lượt cũ hơn hợp lệ (⇒ không `dat`), hết giờ.
6. **CI bắt buộc:** không có lượt push trên H; lượt `cancelled`; một job `failure`; tên trong `CHECK_BAT_BUOC` vắng / `skipped` / do app khác tạo (thử với tập khác rỗng tiêm qua tham số hàm); chỉ có lượt `pull_request` xanh; audit `dat` nhưng CI đỏ.
7. **Vận chuyển:** lớp J: 403 có dấu, 403 không dấu, 404, 401 rồi nguồn kế đạt, 5xx hết lượt thử, hết giờ, JSON hỏng, 200 không dấu, phân trang 2 trang đủ, vượt giới hạn trang, `total_count` lệch. Lớp R/S: **ca dương 302 → ZIP nhị phân thật** (không dấu GitHub, không JSON) được nhận; 302 thiếu `Location`; `Location` không `https`; quá 3 chuyển hướng; thân không phải ZIP; vượt trần kích thước; digest lệch; host lưu trữ không tới được; `Authorization` KHÔNG có mặt trong yêu cầu tới host lưu trữ (đọc nhật ký transport giả). E7 lỗi ⇒ chỉ cảnh báo.
8. **Chế độ:** đủ mọi ô bảng mục 6; tệp chế độ `warning_only` / `chan` / rỗng / vắng / `Warning_Only` / thừa khoảng trắng / `git show` lỗi; bản trong cây làm việc khác bản tại M (⇒ dùng M); biến môi trường (`GITHUB_API_URL`, `GH_HOST`, `GH_REPO`, các tên `TL_B3_*` thử được) KHÔNG đổi quyết định; `--force-older`/`-ForceOlder`, `--no-test`/`-NoTest` KHÔNG đổi quyết định của B3. Ca cho sai OID: M là commit đổi tệp chế độ từ `warning_only` sang `chan`, bằng chứng audit vắng ⇒ rc 5, đúng 0 lời gọi `drive-push` (bản đọc từ cha của M sẽ đẩy).
9. **Khẩn cấp:** cờ + không TTY ⇒ rc 8, không build; cờ không kèm push ⇒ rc 2; TTY + H sai (thiếu một ký tự, chữ hoa, 7 ký tự đầu, có khoảng trắng) ⇒ rc 8; lý do rỗng ⇒ rc 8; TTY + H đúng ⇒ đẩy (đồ giả), nhật ký `owner_emergency` có lý do và digest; kết quả đã `dat` ⇒ không hỏi; cờ + cây bẩn ⇒ vẫn 7; cờ + master dịch chuyển ⇒ vẫn 7; cờ + thụt lùi ⇒ vẫn 3. Linux dựng pty bằng module `pty`; Windows chạy trên console thật theo kịch bản tay của runbook.
10. **Hook:** hai cách viết cờ và các tiền tố PowerShell (`-K`, `-kh`, `-KHANCAP`, tên đủ, `:$true`, qua `.cmd`, qua `pwsh -File`) ⇒ `ask`; lệnh deploy thường (`--push`, `-Push`, `--force-older`, `-ForceOlder`, `-Pull -Push`, `--no-test`, `--out`, `-Out`, `-Python`, `-Repo`) ⇒ quyết định BẰNG quyết định của blob hook tại baseline (cơ chế blob-base như ca `t4`); `sort -k2`, `curl -k`, `ssh -K` không nhắc deploy-package ⇒ không đổi; agent chỉ-đọc vẫn `deny`. Ca mới có mặt trong `CA` (ca `t36` canh).
11. **Đột biến riêng cho từng chốt,** chạy trên BẢN SAO tạm (tên tệp riêng, `-B`), phân hạng bằng LỚP NGOẠI LỆ RIÊNG của ca đích neo TÊN CA, kèm ca tự kiểm bộ phân hạng (chết vì `AttributeError` hoặc assertion của ca khác ⇒ TÍN DỤNG GIẢ, kể cả qua một `except` đổi kiểu). Báo `giết thật / tín dụng giả / sống`, đòi n/n giết thật. Mỗi mục một đột biến có ca đích riêng: build-only thoát khác 0 khi lệch byte · build-only thoát khác 0 khi `git archive` lỗi · bỏ kiểm cây sạch · dùng `-uno` · bỏ phép so (a) · bỏ phép so (b) · so với cây làm việc thay ảnh chụp H · bỏ bước D · D trước C · bỏ so digest ở D · bỏ ghim M ở C · bỏ ghim M ở D · cho master tiến (chỉ kiểm tổ tiên) · đọc chế độ từ SAI OID (cha thứ nhất của M) · bỏ H = M · ps1 trả 1 thay 7 khi tụt sau ở push · bỏ so `head_sha` = H · bỏ so `checkout_sha` từng job · nhận `checkout_sha` `null` · tin `ket_luan_rest` của biên nhận cho job thu (bỏ REST) · bỏ REST cho job trước · dùng biên nhận attempt cũ · bỏ gọi bộ kiểm B1 · bộ kiểm lỗi thành `dat` · bỏ so `kho_id` · bỏ so tập job REST với `ky_vong` · bỏ digest gói biên nhận · bỏ `sha256_noi_dung` mảnh · bỏ `sha256_noi_dung` dấu · `not_measured` không cần A4 · A4: bỏ kiểm workflow lượt đo · bỏ kiểm nhánh mặc định · bỏ kiểm `run_id` đích · bỏ digest · bỏ so `sha256` với H · bỏ `run_attempt_luc_do` · lùi về lượt đo cũ hơn · nhận lượt `pull_request` thay push · bỏ `CHECK_BAT_BUOC` · bỏ kiểm app nguồn · `khong_do_duoc` thành `dat` · `khong_do_duoc` thành `khong_dat` · phân trang cụt coi là đủ · bỏ `total_count` · lớp J nhận 2xx không dấu · lớp S đòi dấu GitHub (làm hỏng ca dương) · bỏ digest ở lớp S · gửi `Authorization` sang host lưu trữ · bỏ trần chuyển hướng · nhịp tim lỗi làm chặn · chế độ lạ thành `warning_only` · đọc chế độ từ cây làm việc · đọc chế độ từ biến môi trường · bỏ TTY stdin · bỏ TTY stdout · nhận tiền tố của H · nhận H chữ hoa · khẩn cấp miễn ràng buộc byte · khẩn cấp miễn ghim M · `--force-older` miễn cổng audit · ghi `audit_passed` cho lần `warning_only` · không ghi nhật ký trước khi đẩy · gỡ luật hook (a) · gỡ luật hook (b) · luật (b) chỉ khớp tên đủ · luật (b) không đòi nhắc deploy-package · bộ so parity nhận kịch bản bắt buộc bị bỏ qua ở cả hai bên · bộ so nhận cặp (ID, runtime) vắng không có dòng `mien` · bộ so đếm dòng `mien` là đạt · phép VÀ để `khong_do_duoc` thắng `khong_dat` · phép VÀ dừng ở lỗi đầu tiên (kết quả đổi theo thứ tự) · phép HOẶC coi lượt không đọc được là `khong_dat` · phép HOẶC bỏ qua liệt kê cụt · P lấy HOẶC trên mọi lượt push thay vì lượt mới nhất · mã lý do chính lấy theo thứ tự duyệt · `dem-g8` đếm theo `phan_lop` (không nối `ket_cuc`) · `dem-g8` đếm `dang_do` là lần đẩy · không ghi `ket_cuc` khi D hỏng. **Không có đột biến "đọc chế độ sớm ở A rồi dùng lại":** dưới hợp đồng M bất biến (A, C, D cùng đòi master = M và chế độ đọc từ OID M) thay đổi thời điểm đọc ấy TƯƠNG ĐƯƠNG, không ca nào phân biệt được, nên không đòi giết nó. Chốt chống chế độ cũ là ba đột biến có đích thật: bỏ ghim M ở C, bỏ ghim M ở D, và đọc chế độ từ sai OID. Đột biến ở sh/ps1 là đột biến văn bản trên bản sao script trong kho tạm.
12. **Đồ giả giữ TRẠNG THÁI:** `gws` giả, interpreter bọc và transport giả ghi nhật ký từng lời gọi; mỗi ca chặn đòi ĐÚNG 0 lời gọi `drive-push`, mỗi ca đẩy đòi đúng 1, đúng zip, sau D. Ít nhất hai ca đầu-cuối dùng `release-bundle` THẬT (một đạt, một lệch byte).
13. **Parity hai nền trên CÙNG đầu vào.** `ops/specs/wp1461-r1/do/KICH_BAN.json` đóng băng HAI danh sách: **bắt buộc chung** (mọi ca mức script của mục 3, 6, 7 áp được cho cả hai nền) và **bắt buộc riêng nền** (ps1: hai ca `-Pull`, nhóm `PB-*`; sh: không có). Chạy sh trên container Linux và ps1 trên **desktop Windows của chủ kho**; VM là lượt parity thứ hai nếu chủ kho chạy được (máy Asus offline, không tính). Mỗi lượt xuất một hồ sơ: từng kịch bản — mã thoát, lớp G8, mã lý do, số và thứ tự lời gọi phá; cộng SỐ ĐẾM: kịch bản chạy / bỏ qua, tệp trong zip, tệp đã so với H, tệp trong manifest. Bộ so (`ops/cong_phat_hanh.py so-parity`) đạt ⇔ hai hồ sơ BẰNG nhau từng ô và từng số đếm ở danh sách chung, VÀ **0 kịch bản bắt buộc (chung hay riêng) ở trạng thái bỏ qua / `not_run`** ở mỗi bên. **Runtime Windows bắt buộc: CẢ HAI — Windows PowerShell 5.1 và PowerShell 7 trên desktop của chủ kho.** `KICH_BAN.json` gán cho mỗi ID một tập runtime bắt buộc: nhóm `PB-*` (probe gắn tham số: với từng tiền tố khác rỗng của `KhanCapChuKho`, cả chữ thường, chữ hoa và dạng `:$true`, gọi script THẬT không kèm `-Push` và đòi rc 2 với thông điệp của B3; lỗi gắn tham số của PowerShell là trượt) và nhóm `DP-*` (toàn bộ kịch bản triển khai của ps1) đều bắt buộc trên {5.1, 7}; kịch bản sh bắt buộc trên {bash/Linux}. Bộ so đòi MỖI cặp (ID, runtime bắt buộc) ở đúng một trong hai trạng thái: đã đo và đạt, hoặc có một dòng `mien` do CHỦ KHO khai (tên runtime, lý do, rủi ro tồn dư, ngày) — ví dụ desktop không có một runtime, hoặc A/B cho thấy `deploy-package.ps1` của base đã không chạy được dưới 5.1. Cặp vắng mà không có dòng `mien` ⇒ trượt. Dòng `mien` không bao giờ được đếm là `dat`: nghiệm thu 13 khi ấy ghi "đạt, có N cặp miễn" kèm danh sách. Hai hồ sơ Windows (5.1 và 7) cũng phải bằng nhau từng ô ở nhóm `DP-*`. Probe TUỲ CHỌN duy nhất là ps1 dưới `pwsh` trên Linux: ghi riêng, không tính vào parity. Bộ so có ca tự kiểm: cùng một kịch bản bắt buộc bị bỏ qua ở CẢ HAI hồ sơ ⇒ trượt; một cặp (`PB-*`, 5.1) vắng không có dòng `mien` ⇒ trượt; có dòng `mien` ⇒ không trượt nhưng không được đếm là đạt. Base lẫn candidate chạy các kịch bản không dùng tính năng mới (I1), hai vế dựng trong một lệnh. Có ca cho tệp nhật ký/chế độ rỗng và chỉ-BOM; tránh ba bẫy PowerShell của `CLAUDE.md`.
14. **Đo năng lực:** hồ sơ `do-nang-luc` cho container Linux và desktop Windows. Thiếu một máy không chặn merge (packet land ở `warning_only`) nhưng PR ghi rõ máy nào `chua_do`.
15. **Wrapper `.cmd`:** tập dòng không-`rem` trùng byte với baseline; EOL CRLF; bảng mã 0–8 có mặt.
16. **Cổng kho:** `python ops/cong_phat_hanh_test.py` và `python .claude/hooks/pretooluse_guard_test.py` (chế độ đủ) N/N hai số bằng nhau, có dòng dấu hiệu dương; `python .claude/dev/ci_dang_ky_test.py` đạt; `python .claude/dev/packet_loop.py doctrine-scan --root .` và `adr-song --root .` rc 0; `python scripts/tl.py --selftest` N/N (các ca đang đọc văn bản ba script deploy phải còn xanh); Ruff `--select F` DELTA = 0 so baseline trên mọi `.py` đổi hoặc thêm; `git diff --numstat` so baseline trong `tran_moi`.
17. **Gói phát hành không đổi:** `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` cho `ok=true`, `expected == checked`; `file_count` của `release-bundle` bằng baseline (A/B một lệnh). Đo thấy một tệp trong manifest phải đổi ⇒ DỪNG (tái sinh `RELEASE_MANIFEST.json`, golden, VERSION nằm ngoài write set, cần revision mới).
18. **CI:** CI PR Ubuntu xanh trên H; PR báo delta thời gian theo job/bước của bộ test mới và ghi nhận `pretooluse_guard_test` chạy chế độ đủ (§13: trung vị 1009 s thay 26 s). K7 (một lượt `ci-dot-bien-du.yml` `success` trên đúng H) nếu effective write set chạm vùng M9 theo dispatcher.

## Write set
Nhánh điều phối `ops/wp1461-r1` (không thuộc PR giao nộp):
- `ops/specs/wp1461-r1/SPEC.md`
- `ops/leases/wp1461-r2-g1-claude-<YYYYMMDD>.yaml` — do ĐIỀU PHỐI cấp và đăng; trước khi thi công, executor chạy `ai-dang-giu` và xác nhận lease này được trả về cho TỪNG đường dẫn của PR giao nộp.
- `ops/specs/wp1461-r1/do/ho-so/**` — hồ sơ parity, năng lực, đo PowerShell (bằng chứng chạy; không phải mã).

PR giao nộp (nhánh thi công riêng), 11 tệp đổi + 1 tệp dự kiến không đổi:
1. `scripts/deploy-package.sh`
2. `scripts/deploy-package.ps1`
3. `scripts/deploy-package.cmd` — CHỈ dòng `rem` (bảng mã thoát); thêm so với r85 vì wrapper chuyển tiếp mã 5–8.
4. `.claude/hooks/pretooluse_guard.py`
5. `.claude/hooks/pretooluse_guard_test.py`
6. `ops/cong_phat_hanh.py` (MỚI) — I5, gồm cả lệnh `so-parity`, `do-nang-luc`, `dem-g8`; `ops/` không vào gói nên không đụng manifest và trần 200 tệp.
7. `ops/cong_phat_hanh_test.py` (MỚI) — bộ test dev-side; không đặt vào `scripts/tl_selftest.py` vì tệp ấy trong manifest (kéo theo manifest + VERSION + CHANGELOG) và selftest chạy cả trong gói cài không có script deploy.
8. `ops/cong_phat_hanh.che_do` (MỚI) — mục 8.
9. `.claude/dev/ci_dang_ky_test.py` — CHỈ thêm mục đăng ký bộ test mới (bộ quét `rglob("*_test.py")` đòi mọi test mức đỉnh của `ops/` có trong sổ).
10. `docs/QUY_TRINH_PHAT_HANH_B3.md` (MỚI) — mục 9.
11. `ops/specs/wp1461-r1/do/KICH_BAN.json` (MỚI) — ma trận kịch bản đóng băng mà bộ test và hai lượt parity cùng đọc.
12. `scripts/deploy-guard.ps1` — trong write set theo r85, dự kiến diff = 0; đổi thì tính vào trần và phải kèm A/B quyết định không đổi.

Không thuộc write set: `CLAUDE.md`, `ops/ci_provenance.py`, `ops/specs/wp1460-r1/**`, `scripts/tl.py`, `scripts/tl_core/**`, `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json`, `VERSION`, `.github/**`, `.claude/settings.json`, `.claude/dev/packet_loop.py`, `.claude/dev/launcher.py`.

## Baseline nghiệm thu
- **B không nằm trong tệp này** vì nó chỉ tồn tại sau khi B1 land. Mission revision cài đặc tả và lease của B3 cùng ghi MỘT OID B (40 hex); hai nơi lệch nhau ⇒ không thi công. B là quyết định bền của điều phối theo protocol §3.2.1; `0f9aa2a…` chỉ là base lúc SOẠN, không dùng để đo diff.
- **Điều kiện của B, executor và reviewer tự đo trước khi dùng (sai một điều ⇒ DỪNG):** (1) B nằm trên chuỗi first-parent của `origin/master` vừa fetch, kho không shallow; (2) B là commit merge PR giao nộp của B1 hoặc một commit first-parent sau nó: tại B có `ops/specs/wp1460-r1/hop_dong/fixture.json`, `ops/specs/wp1460-r1/hop_dong/bien_nhan_audit.v1.schema.json`, và `python .claude/dev/ci_dang_ky_test.py --kiem-bien-nhan-audit` nhận ca `goc` của fixture (rc 0); (3) đặc tả B1 mà PR ấy thi công có đúng băm `4c1e8ae9…` ghim ở đầu tệp này; (4) tại B chưa có tệp nào trong ba tệp MỚI `ops/cong_phat_hanh.py`, `ops/cong_phat_hanh_test.py`, `ops/cong_phat_hanh.che_do`.
- **Mọi phép đo của packet tính từ B:** `git diff --numstat B...<head>` cho trần kích thước; tập tệp đổi so với B phải nằm trong write set (tệp của B1 đã có ở B nên KHÔNG xuất hiện trong diff và không thuộc quyền ghi của B3; ở `.claude/dev/ci_dang_ky_test.py` diff so B chỉ được là mục đăng ký); mọi vế "base" của A/B là B; Ruff delta so B; blob hook "trước B3" là blob tại B; `file_count` gói so B; số dòng điểm chèn đo lại tại B.
- Cập nhật nhánh thi công lên master mới hơn trong lúc làm (merge) KHÔNG dời B. Dời B cần Mission revision mới.

## Kích thước và `nang_tran`
Trần `ADR-0053` (qua dòng khai ở đầu tệp): ≤ 6 tệp, ≤ 450 dòng thêm. PR giao nộp VƯỢT cả hai; xin nâng:

```
nang_tran:
  ai_nang: chủ kho (ducthangho), có hiệu lực khi duyệt băm đặc tả này và Mission revision cài nó
  can_cu: ước lượng theo thành phần, CHƯA có numstat vì chưa có mã (deploy-package.sh ~120; deploy-package.ps1 ~150; deploy-package.cmd ~8; hook ~20; hook test ~130; cong_phat_hanh.py ~950; cong_phat_hanh_test.py ~2 000 gồm ca, đồ giả giữ trạng thái, bảng đột biến và bộ phân hạng; che_do 1; ci_dang_ky_test.py ~8; runbook ~230; KICH_BAN.json ~350; deploy-guard.ps1 0). Không tách được: §B3 đòi cờ khẩn cấp và luật hook land trong CÙNG packet; hai script phải đổi cùng lúc với helper để parity đo trên một candidate; bộ test phải land cùng mã nó canh; wrapper .cmd phải khai mã thoát mới cùng lúc mã ấy xuất hiện
  tran_cu: 6 tệp / 450 dòng thêm
  tran_moi: 12 tệp / 4 200 dòng thêm
```

Executor đo `git diff --numstat B...<head>` trước MỖI lần xin review và ghi vào PR; vượt `tran_moi` ⇒ DỪNG, không cắt ca hay đột biến. Khối này chép nguyên vào lease và vào Mission revision cài đặc tả.

## Quy trình và quyền
- **Điều kiện cấp lease:** (1) chủ kho duyệt băm đặc tả này cùng khối `nang_tran`; (2) đặc tả B1 đã được duyệt với đúng băm `4c1e8ae9…`, và PR giao nộp của B1 ĐÃ LAND trên `master` (B3 cần `ops/specs/wp1460-r1/hop_dong/fixture.json`, lệnh `--kiem-bien-nhan-audit`, và dùng chung `.claude/dev/ci_dang_ky_test.py` nên xếp NỐI TIẾP sau B1); (3) lease `wp1236-a-r9-g1-claude-20261120` (giữ `.claude/dev/ci_dang_ky_test.py` tới 2026-11-22T15:35Z) đã hết hoặc đã thu hồi hai chiều, và không lease sống nào chồng write set — `ai-dang-giu` trên MỌI ref, sau khi so tập ref cục bộ với `ls-remote`; (4) Mission revision riêng cài đặc tả, ghi OID B thoả mục "Baseline nghiệm thu"; lease chép đúng OID ấy.
- **Vai:** Executor Claude Code (Fable 5.2). Reviewer Codex service gpt-6-astra, mức xhigh, phiên độc lập, chỉ đọc; reviewer CHẠY ca và đột biến có sẵn trong cây, hướng thử cần soạn nội dung nhạy cảm thì mô tả bằng lời cho điều phối.
- **Trần (r85 `per_new_packet`):** soạn spec 3 · review spec Codex 4 · executor attempts 3 · review mã Codex 3 · CI PR Ubuntu 3 · `ci-dot-bien-du.yml` (K7) 1 nếu chạm vùng M9 · connector 2 · CI rerun 1 · Windows CI 0. Đếm số lời gọi Codex đã dùng TRƯỚC mỗi lời gọi.
- **Windows:** không dispatch Windows CI. Chủ kho chạy trên desktop dưới CẢ Windows PowerShell 5.1 lẫn PowerShell 7 và gửi lại hồ sơ; VM chỉ thêm parity. Cặp (ID, runtime) bắt buộc nào chưa đo ⇒ nghiệm thu 13 CHƯA đạt, trừ khi chủ kho khai dòng `mien` cho đúng cặp ấy (nghiệm thu 13).
- **Trong lúc thi công và test:** KHÔNG đẩy Package thật, KHÔNG gọi `drive-push` thật, KHÔNG dùng cờ khẩn cấp ngoài đồ giả, KHÔNG dispatch workflow, KHÔNG đổi biến/secret/bảo vệ nhánh, KHÔNG LIVE.
- Chủ kho tự audit exact-H trước lần đẩy đầu của H; merge do chủ kho bấm. Trước khi đẩy H: cập nhật nhánh lên master mới nhất và đo lại làn.
- **Ngoài phạm vi:** bật chế độ `chan` và điền `CHECK_BAT_BUOC`; B1; B2 (kể cả số Issue nhịp tim); B4 và công tắc A+1; mọi workflow; `release-bundle`/manifest/VERSION; công bố nhật ký G8 lên kho; hai lệch có sẵn nêu ở I2; sửa `CLAUDE.md`; đo cách các chế độ quyền xử lý `ask`; làn A, làn C.

## Thay đổi
### r1 → r2 (review lượt 1)
| Finding | Sửa ở r2 |
|---|---|
| SPEC-01 (P1) ánh xạ B1 không thi công được | Ghim B1 r2 (`9f7010e`, `4c1e8ae9…`). Mục 4.2 viết lại: bảng L1–L13 tách ba cột biên nhận / hằng hợp đồng / REST; `kho_id` có trong v1 và đối chiếu REST; kiểm kê theo `kiem_ke_job` + `kiem_ke_muc` của B1; kết luận job thu CHỈ từ REST; tên artifact và tên tệp là hằng; hình biên nhận kiểm bằng CHÍNH bộ kiểm của B1; attempt cao nhất; dùng fixture chung, có ca dương `goc` và "chạy lại riêng job thu"; bỏ yêu cầu "thiếu từng trường L một ca" và bảng `ANH_XA_V1` |
| SPEC-02 hợp đồng A4 chưa đủ | Mục 4.3: định vị bằng E8, gọi nguyên `nhap_wd`, ba phép kiểm thêm của B3, `head_sha` lượt đo được khác H; E8/E9 vào bảng năng lực; Nghiệm thu 5 và các đột biến A4 |
| SPEC-03 hình phản hồi tải artifact | Mục 5: ba lớp J / R / S với luật riêng; ca dương 302 → ZIP nhị phân; đột biến "lớp S đòi dấu GitHub", "bỏ digest lớp S", lộ `Authorization` |
| SPEC-04 mâu thuẫn build-only | I2 và mục 2: ở build-only bước A, B chỉ in chẩn đoán, lỗi bị nuốt; cưỡng chế chỉ ở push; Nghiệm thu 2 (A/B sạch/bẩn, có/không bỏ gate) và hai đột biến build-only |
| SPEC-05 (P1) master dịch chuyển lúc đẩy | Ghim M ở A; C và D đòi master = M, mọi dịch chuyển ⇒ rc 7 (đúng r4); chế độ đọc từ M ở C; ca "master sang `chan` giữa C và D" đòi 0 `drive-push`; đột biến chế độ cũ, bỏ ghim M, chỉ kiểm tổ tiên. Chỗ lệch 4 khai H = M |
| SPEC-06 trần kích thước | Dòng khai `ADR-0053@8ab1007…` (ba phép đo OID đã chạy); mục "Kích thước và `nang_tran`" đủ bốn trường, ước lượng theo tệp, numstat bắt buộc trước review; không bỏ ca nào |
| SPEC-07 lease ngoài `ops/leases` | Write set: lease ở `ops/leases/wp1461-r2-g1-claude-<YYYYMMDD>.yaml` do điều phối cấp; thư mục đặc tả không còn chứa lease; executor xác nhận `ai-dang-giu` trả lease cho từng đường dẫn |
| SPEC-08 parity tiền kiểm Windows | H định nghĩa là candidate SAU `-Pull`, ghi ở A; mục 3 chốt thứ tự: tụt sau / đi trước / rẽ ⇒ rc 7 ở cả hai nền, ps1 đổi 1 → 7 chỉ khi `-Push`; ca riêng cho tụt-sau-không-Pull, Pull thành công, Pull thất bại, đi trước, rẽ |
| SPEC-09 ca parity bắt buộc có thể bị bỏ qua | Nghiệm thu 13: 0 kịch bản bắt buộc bị bỏ qua / `not_run`; probe tuỳ chọn tách riêng; miễn ghi `mien`; ca tự kiểm và đột biến cho bộ so |
| SPEC-10 (P3) mã thoát của wrapper | `deploy-package.cmd` vào write set, chỉ dòng `rem`; một bảng mã thẩm quyền 0–8 (mục 6); Nghiệm thu 15 so byte dòng không-`rem` |
| Quyết định điều phối | `CLAUDE.md` rời write set (lớp 3 chỉ ở runbook, lý do hook trỏ tới); VM chỉ parity, hai máy deploy là container Linux và desktop Windows; bật `chan` là PR riêng; bỏ mục câu hỏi mở |

### r2 → r3 (review lượt 2; SPEC-01…08 và SPEC-10 đã đóng)
| Finding | Sửa ở r3 |
|---|---|
| SPEC-09 (P2, còn một phần) runtime Windows mâu thuẫn | Một cách xử lý duy nhất: Windows PowerShell 5.1 và PowerShell 7 trên desktop đều BẮT BUỘC cho cả nhóm probe gắn tham số `PB-*` lẫn nhóm triển khai `DP-*`; mỗi cặp (ID, runtime) phải đã đo hoặc có dòng `mien` do chủ kho khai, không có bỏ qua im lặng; `mien` không đếm là đạt; probe tuỳ chọn chỉ còn `pwsh` trên Linux. Mục 7 trỏ sang nhóm `PB`; phép kiểm "cờ không kèm push ⇒ rc 2" đặt đầu tiên để làm probe. Thêm ca tự kiểm và hai đột biến cho bộ so |
| SPEC-11 (P2) baseline có trước phụ thuộc | Bỏ OID ghim trong tệp; mục "Baseline nghiệm thu": B do Mission revision và lease cùng ghi, phải là commit first-parent của master ĐÃ chứa B1 (bốn điều kiện tự đo); numstat, tập tệp đổi, A/B, Ruff, blob hook đều đo từ B; `0f9aa2a…` chỉ còn là base lúc soạn |
| SPEC-12 (P2) đột biến chế độ cũ tương đương | Gỡ đột biến "đọc chế độ ở A rồi dùng lại" và khai rõ nó tương đương dưới hợp đồng M bất biến; thay bằng "đọc chế độ từ sai OID (cha của M)" có ca đích riêng (M là commit bật `chan`); giữ hai đột biến bỏ ghim M ở C và ở D |
| SPEC-13 (P2) thiếu luật ghép ba trạng thái | Mục 4.5: phép VÀ (sai thắng không-đo-được), phép HOẶC trên lượt audit (đạt thắng; không-đo-được hoặc liệt kê cụt giữ `khong_do_duoc`), P chỉ xét lượt push mới nhất, bảng P × Q → C → rc, mã lý do chính tất định, đánh giá đủ không dừng sớm. Nghiệm thu 1 thêm chín ca hỗn hợp chạy hai thứ tự; sáu đột biến ghép |
| SPEC-14 (P3) số dòng nhật ký | Bước E và mục 6 thống nhất: mỗi lần thử tới C có đúng hai sự kiện cùng `id` (`phan_lop` trước khi đẩy, `ket_cuc` sau); định nghĩa chuỗi sự kiện cho lần bị chặn ở C và hỏng ở D; lệnh `dem-g8` nối theo `id`, đếm lần thành công đúng một lần, `dang_do` báo riêng; ca và ba đột biến |
