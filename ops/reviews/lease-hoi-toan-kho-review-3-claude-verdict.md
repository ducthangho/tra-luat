verdict: approve
reviewed_sha: f12736dfbbb9760da4ce164988f3ee97784d0475

## ĐỐI CHIẾU LƯỢT TRƯỚC

- **kiem-dau-toan-kho-bo-qua-git-loi-that (P1, lượt 2): ĐÃ VÁ THẬT.**
  Bằng chứng CHẠY ĐƯỢC (tất cả tự dựng lại trong sandbox này, không nhận lời khai):
  1. Đọc diff `babceec → f12736d` (`git diff babceec f12736d -- ops/lease_publish.py`): hai
     `return` lặng lẽ bị thay bằng đúng một dòng `_git(root, "rev-parse", "--git-dir")`, dùng
     lại `_git()` mà P1 của lượt 1 đã khoá — không mở một đường fail-close thứ hai.
  2. Copy toàn bộ `cay-kho` ra `work/verify_unpatched`, thay `ops/lease_publish.py` bằng đúng
     bản `babceec` (chưa vá) → chạy `ops/lease_publish_test.py` → **95/97**, đỏ đúng
     `t33` (thiếu actionlint, đỏ sẵn) + `t97`, thông điệp
     *"`_kiem_dau_toan_kho` coi git lỗi thật (rev-parse --git-dir rc!=0) là 'không phải kho'
     và bỏ qua lặng lẽ…"* — nói đúng lỗ nó hứa bịt.
  3. Chạy nguyên bản patched (`f12736d`) tại chỗ → **96/97** (chỉ `t33`); cài `actionlint`
     thật trong sandbox này (`go install …@latest`, xác nhận `actionlint --version`) rồi chạy
     lại → **97/97, rc=0** — khớp đúng con số "cây đã vá + actionlint như CI" mà `EVIDENCE.md`
     khai, tự đo được chứ không phải tin lời.
  4. Tự dựng lại đúng bước gọi mà `t97` làm (mock `GOI_GIT` đếm số lần gọi) và gọi thẳng
     `_kiem_dau_toan_kho` trên bản vá: `GOI_GIT` bị gọi **đúng một lần** với
     `("rev-parse", "--git-dir")`, và `Chan(ma=12=RC_KHONG_XAC_DINH)` được ném đúng — xác nhận
     `t97` chạm thật đường vừa sửa, không xanh vì đường khác vô tình cũng đỏ.
  5. Đọc `main()` (dòng 719-723) và `.github/workflows/ops-publish-lease.yml` (dòng 209-229):
     `Chan` được `main()` bắt và in `CHAN [ma]: …` ra stderr rồi trả `sys.exit(e.ma)` — không
     traceback trần. Workflow đọc `rc` của `check`/`kiem-github` theo đúng ba nhánh
     (`0`=đăng được, `9`=đã đăng bỏ qua, "còn lại LÀ CHẶN" — dòng 219-220), nên `rc=12` mới
     (KHÔNG_XÁC_ĐỊNH) tự động rơi vào nhánh chặn (`bao_chan`, `BI_CHAN=1`, `exit 1`) mà
     KHÔNG cần sửa gì thêm ở workflow — không có đường gọi nào từng dựa vào việc hàm này
     không ném.
  6. Dựng thật một ca "kho là worktree, `.git` là TỆP" (`git worktree add`) — đúng ca thứ ba
     mà nhánh (1)/(2) *không* bắt (vì `.git` tồn tại dưới dạng tệp, và tệp lease nằm TRONG
     worktree nên `relative_to` cũng qua) — rồi gọi `_kiem_dau_toan_kho` bằng git THẬT
     (không mock) trên cả bản `babceec` lẫn `f12736d`: cả hai đều `return None`, không ném gì
     — **hành vi giống hệt nhau trước/sau vá**, không có ca hợp lệ nào bị chặn oan.

- **bien-het-han-khong-co-ca (P3, lượt 1): vẫn CHƯA VÁ — không đổi.**
  Diff `babceec → f12736d` (`ops/lease_publish.py`) không chạm `_phan_loai_lease`. Áp lại đột
  biến biên `han <= bay_gio` → `han < bay_gio` trên bản sao `work/verify_p3_boundary_r3` (đã
  có `t95`/`t96`/`t97`) → **96/97**, ca đỏ duy nhất là `t94` với lý do
  *"neo mutant A2b-co không duy nhất"* — tác dụng phụ tự-neo của chính bộ đột biến `t94`
  (đúng như lượt 2 đã ghi, chỉ khác thông điệp cụ thể vì `t94` chạy trên bản đã có thêm
  `t95`-`t97`), KHÔNG có ca nào trong `t95`/`t96`/`t97` bắt được đột biến biên. Đúng như
  `LEASE.yaml.viec_cua_luot_nay` đã khoanh: lượt này CHỈ được phép vá đúng một finding
  (`kiem-dau-toan-kho-bo-qua-git-loi-that`), không phải packet để đóng P3 — không nâng
  thành blocker của lượt này.

## BẢNG ĐO

| khẳng định | EVIDENCE khai | đo được | khớp? |
|---|---|---|---|
| `reviewed_sha` | `f12736d…` | `git -C cay-kho rev-parse HEAD` → `f12736dfbbb9760da4ce164988f3ee97784d0475` | ✅ |
| head lượt 2 | `babceec` | `git log --oneline` → cha trực tiếp của `f12736d` | ✅ |
| `ops/lease_publish_test.py` (nền/sandbox) | `96/97` / `96/97` | chạy trong `cay-kho` (không có `actionlint`) → `96/97`, đỏ duy nhất `t33` | ✅ |
| gỡ bản vá → `95/97`, `t97` ĐỎ | khai đúng | copy toàn cây, thay `lease_publish.py` = bản `babceec` → `95/97`, đỏ `t33`+`t97`, thông điệp đúng lỗ | ✅ |
| cây đã vá + `actionlint` như CI → `97/97 rc=0` | khai đúng | tự `go install actionlint`, thêm vào PATH, chạy lại → `97/97 đạt`, `rc=0` | ✅ (tự cài công cụ và đo, không tin lời) |
| `t94` (đột biến A1-A8) | `đã chạy=10, bị giết=10` | in trong cả hai lượt chạy (vá và gỡ vá) → `đã chạy=10, bị giết=10` | ✅ |
| `t93`/A7 | "vẫn XANH" | trong `96/97`/`97/97`, không có `t93` trong danh sách ĐỎ | ✅ |
| Ngân sách: 2 tệp / 368 dòng thêm | khai đúng | `git diff --numstat 8222c101 f12736d` → `ops/lease_publish.py +149/-0`, `ops/lease_publish_test.py +219/-0` = **368**, 2 tệp — khớp TỪNG SỐ | ✅ |
| trần ngoại lệ ADR-0044 (≤3 tệp/≤380 dòng) | không vượt | 2 ≤ 3, 368 ≤ 380 | ✅ trong trần |
| `write_set` = diff thật | `ops/lease_publish.py`, `ops/lease_publish_test.py` | `git diff --stat 8222c101 f12736d` chỉ đúng hai đường này | ✅ |
| diff `babceec→f12736d` chỉ sửa `_kiem_dau_toan_kho` + thêm `t97` | (đại diện) | `git diff babceec f12736d` → đúng 6 dòng xoá/4 dòng thêm ở `lease_publish.py` (2 `return` → 1 `_git()`), 33 dòng thêm ở test (`t97`), không chạm gì khác | ✅ |
| sha256 `SPEC.md` | `ffca019e…5da87` | `sha256sum SPEC.md` → khớp từng ký tự | ✅ |
| `git rev-parse --is-shallow-repository` | `false` | đo trong `cay-kho` → `false` | ✅ |
| `core.abbrev` | (bắt buộc = 7 theo protocol §8) | `git config core.abbrev` → `7` | ✅ |
| Ref 184/184, `comm` hai chiều rỗng | đo trên sandbox mirror | `ls-remote --heads` = 184, `for-each-ref` (loại HEAD) = 184, `comm -23`/`comm -13` cả hai rỗng | ⚠️ tự nhất quán (184/184) nhưng đo trên `kho.git` — mirror cục bộ do sandbox tự tạo, KHÔNG phải phép đo trên kho nguồn GitHub "trước khi clone" mà câu chữ EVIDENCE gợi ý — cùng giới hạn mà lượt 2 đã tự khai cho con số 182/182 của nó, không phải chỗ hổng mới |
| commit `f12736d` trích đúng sha256 verdict lượt 2 | `b6b6a3a2…` | `git show f12736d -s --format=%B` chứa `b6b6a3a2…`; `sha256sum VERDICT-LUOT-2.md` → `b6b6a3a2787d3018…` | ✅ |
| `Chan` không rò traceback trần | (ngụ ý, không khai tường minh) | đọc `main()` dòng 719-723: `except Chan as e: print(...); return e.ma` — bắt trọn, không lộ traceback | ✅ |
| workflow xử lý `rc=12` (mã mới) đúng chưa | (không khai, tự kiểm theo nhiệm vụ 2) | đọc `ops-publish-lease.yml` dòng 213-229: chỉ đặc cách `rc=9`, mọi `rc!=0` khác (gồm `12`) rơi vào `bao_chan`/`BI_CHAN=1`/`exit 1` — không cần sửa workflow | ✅ |

## BẢNG ĐỘT BIẾN

| đột biến | ca đáng lẽ đỏ | kết quả | sống sót? |
|---|---|---|---|
| Khôi phục nguyên hai `return` (bản `babceec`) | `t97` | `95/97`, đỏ đúng `t33`+`t97`, thông điệp đúng lỗ | bị giết |
| `.git` là TỆP (worktree thật, `git worktree add`), git THẬT không mock, so trước/sau vá | (không có — kiểm KHÔNG hồi quy trên ca hợp lệ) | cả `babceec` lẫn `f12736d`: `_kiem_dau_toan_kho` trả `None`, không ném gì — HÀNH VI GIỐNG HỆT | không có hồi quy (ca hợp lệ không bị chặn oan) |
| Xoá hẳn dòng `_git(root, "rev-parse", "--git-dir")` (không khôi phục `return`, chỉ bỏ dòng) | *(không rõ — xem phân tích)* | `97/97` — **`t97` VẪN XANH** | **SỐNG SÓT MỘT PHẦN** — xem finding `t97-khong-ghim-nguon-loi` bên dưới |
| `_phan_loai_lease`: biên `han <= bay_gio` → `han < bay_gio` (P3 lượt 1) | (không có — đã biết) | `96/97`, không `t95`/`t96`/`t97` nào đỏ (chỉ `t94` tự-neo) | **SỐNG SÓT**, đã biết, CHƯA VÁ, ngoài phạm vi lượt này |

### t97-khong-ghim-nguon-loi  [P3]  `t97` chỉ khoá MÃ LỖI, không khoá ĐƯỜNG GỌI cụ thể

TỆP/DÒNG: `ops/lease_publish_test.py:3090-3122` (`t97_kiem_dau_toan_kho_phai_fail_close_khi_git_that_bai`)

VẤN ĐỀ: `t97` mock `GOI_GIT` để LUÔN trả `rc=128` bất kể đối số, rồi chỉ khẳng định
`ex.ma == mod.RC_KHONG_XAC_DINH` — không kiểm nội dung `ex.thong_diep`, không đếm số lần
`GOI_GIT` bị gọi, không khẳng định lời gọi đầu tiên là `("rev-parse", "--git-dir")`. Vì
`_kiem_dau_toan_kho` sau khi qua khỏi dòng đang xét vẫn gọi `_quet_lease_toan_kho()` — mà hàm
đó lại gọi `_git(goc, "for-each-ref", …)` — nên NẾU dòng `_git(root, "rev-parse", "--git-dir")`
bị xoá hẳn (không khôi phục hai `return` cũ, chỉ đơn giản bỏ dòng kiểm), `for-each-ref` bên
dưới cũng ăn đúng `GOI_GIT` giả và ném đúng `Chan(RC_KHONG_XAC_DINH, …)` — CÙNG MÃ LỖI, khác
thông điệp (`"git for-each-ref … rc=128"` thay vì `"git rev-parse --git-dir rc=128"`). `t97`
không phân biệt được hai nguồn này nên vẫn XANH: chạy thật trong `work/verify_t97_delete_check`
→ `97/97`, không ca nào đỏ.

Đây KHÔNG phải hồi quy trên `reviewed_sha` — bản vá thật sự (`f12736d`) GIỮ dòng kiểm, và đã tự
đo trực tiếp (không qua `t97`) rằng `GOI_GIT` bị gọi ĐÚNG MỘT LẦN với đúng đối số
`("rev-parse", "--git-dir")` trước khi ném `Chan` — tức trên chính commit đang xét, dòng đó
THẬT SỰ là nguồn gây lỗi, `t97` không xanh giả ở ĐÂY. Nhưng bài kiểm tra không TỰ KHOÁ được thứ
nó có vẻ khoá: một người sau này "dọn dẹp" xoá hẳn dòng kiểm (nghĩ nó thừa vì đường quét bên
dưới cũng đã fail-close) sẽ không bị `t97` bắt — dù về mặt hành vi, việc xoá đó với ĐÚNG kịch
bản "git hỏng toàn bộ" vẫn cho ra cùng `rc=12`, tức gần như một đột biến tương đương (không
gây khác biệt quan sát được từ phía gọi `main()`/workflow, vì cả hai đường đều fail-closed đúng
mã). Rủi ro thực tế vì vậy THẤP — không chặn duyệt.

ĐÃ THỬ VÁ: không — nằm ngoài `write_set` mà lease này đóng băng lại (một sửa nữa vào
`ops/lease_publish_test.py` sẽ tốn thêm dòng vào trần đã nới, và không phải finding của lượt
này được cấp quyền vá). Gợi ý cho lượt sau (không bắt buộc): thêm đếm `len(calls)==1` và
`calls[0][:2] == ("rev-parse", "--git-dir")` vào `t97`, hoặc kiểm `"rev-parse --git-dir" in
ex.thong_diep`.

ĐÃ THỬ NGHIỆM: chạy trên bản sao `work/verify_t97_delete_check` (xoá đúng một dòng
`_git(root, "rev-parse", "--git-dir")`, giữ nguyên mọi thứ khác) → `97/97`, xác nhận `t97`
không đổi màu.

ĐỘ TIN: cao — đột biến tự dựng, chạy thật, kết quả tái lập được; đây là gap về ĐỘ CHÍNH XÁC của
một ca test đã CÓ RĂNG cho đúng mutation nó được viết ra để chặn (khôi phục `return`), không
phải một lỗ hành vi trên `reviewed_sha`.

## Còn lỗ thứ tư trong `ops/lease_publish.py`?

Quét lại toàn bộ nhánh `except`/`return` sớm/`continue`/`pass` trong tệp (không chỉ vùng vừa
sửa): `_kiem_lop_review` (dòng 176-178, `except ValueError: pass`) chỉ nằm trong nhánh
`schema_version < 2` và chỉ điều khiển một dòng CẢNH BÁO in ra (`print(..., file=sys.stderr)`),
không phải một chốt fail-close/fail-open — bỏ qua lỗi parse timestamp ở đây không làm lọt qua
cổng nào, nó chỉ làm MẤT một dòng cảnh báo phụ. `_doc_gh`, `_kiem_loai_so_hieu`,
`_kiem_comment_da_co`, `_quet_lease_toan_kho`, `_git`, `_ten_nhanh_may_chu`,
`_kiem_neo_prompt` — toàn bộ đều `raise Chan(RC_KHONG_XAC_DINH/RC_NEO/RC_NOI_DUNG, …)` trên mọi
nhánh không đo được; `continue` ở dòng 264/296/299/677 đều là lọc hợp lệ (ref tượng trưng,
dedup, lease không chạm write_set đang hỏi), không phải nuốt lỗi. **Không tìm thấy hình dạng
lỗi thứ 4** (KHÔNG_XÁC_ĐỊNH bị gộp vào coi-như-sạch) trong phạm vi tệp này — không cần đề nghị
dừng vá lẻ để xử lý cả lớp.

## Phạm vi / ngân sách

Diff `babceec → f12736d` nằm trọn trong `write_set` (`ops/lease_publish.py`,
`ops/lease_publish_test.py`), không chạm tệp thứ ba. Tổng diff (`base_sha` → `reviewed_sha`):
**2 tệp / 368 dòng thêm**, trong trần ĐÃ NỚI của ADR-0044 (≤3 tệp/≤380 dòng) và ADR-0043
(lượt 3/3, đã dùng hết trần — không còn lượt 4).

## Điều kiện dừng chưa thoả (không đổi bởi verdict này)

`LEASE.yaml.ngoai_le_ADR_0045.ba_dieu_kien_ADR_0045.human_readback_truoc_land` vẫn ghi
**BẮT BUỘC — CHƯA làm**. Approve của reviewer KHÔNG thay được bước này: chủ kho phải tự đọc
lại diff (`git diff babceec f12736d` — sáu dòng cốt lõi) trước khi land, đúng ADR-0045.

## Kết luận

Finding P1 duy nhất của lượt 2 (`kiem-dau-toan-kho-bo-qua-git-loi-that`) đã được vá THẬT: bản
vá dùng lại đúng `_git()` mà lượt 1 đã khoá (không mở đường fail-close thứ hai), gỡ bản vá làm
`t97` đỏ đúng lỗ, giữ actionlint vào thì `97/97 rc=0`, và không có đường gọi/worktree/ca `.git`-
là-tệp nào bị vỡ hay bị chặn oan — đã tự dựng và chạy thật cả ba hướng công kích mà đề bài yêu
cầu (đường gọi cũ dựa vào không-ném, ca thứ ba hợp lệ, `Chan` rò traceback). Một khe hở nhỏ được
tìm thấy ở chính `t97` (không ghim được ĐÚNG dòng nào gây lỗi, chỉ ghim ĐÚNG mã lỗi) nhưng đã đo
và xác nhận đây không phải hồi quy trên `reviewed_sha` — chỉ là dư địa siết `t97` chặt hơn cho
lượt sau, không đáng để tốn lượt review thứ 4 (vốn không còn) hay yêu cầu vá thêm ở đúng lượt
cuối này. Không tìm thấy hình dạng lỗi thứ tư trong phần còn lại của tệp. Phạm vi và ngân sách
đúng cam kết, không vượt trần đã nới.

`bien-het-han-khong-co-ca` (P3, lượt 1) vẫn CHƯA VÁ — đúng như đã biết từ hai lượt trước, ngoài
phạm vi việc được giao cho lượt vá này, không phải lý do chặn.

Đề nghị **approve**. Việc land vẫn phải chờ human readback của chủ kho theo ADR-0045 — verdict
này không thay thế bước đó.
