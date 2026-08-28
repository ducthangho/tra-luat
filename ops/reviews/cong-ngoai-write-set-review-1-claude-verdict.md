verdict: changes_requested
reviewed_sha: 4082ab57c74ec7396503990c2f1fa7e8291ffc30
P1: 2
P2: 1
finding_moi: 3

## BẢNG ĐO

| khẳng định | PR/hồ sơ khai | đo được | khớp? |
|---|---|---|---|
| numstat = 200+4=204 dòng thêm | brief packet | `git diff --numstat 27fb9de2 4082ab5` → `.claude/dev/ci_dang_ky_test.py` 200/0, `.github/workflows/ci.yml` 4/0 = **204** | khớp, dưới trần 220 |
| `python3 ci_dang_ky_test.py` tự canh, N/N | packet | `ĐĂNG KÝ: 20/20`, `PHẢN CHỨNG: 11/11 đỏ đúng`, `TỔNG: ĐẠT`, `RC=0` | khớp |
| `--chay` gọi 7 bộ MOI, 2 cách ly, `TỔNG` đúng | brief | Chạy trọn (không qua ống, `RC=0` đo bằng `$?`): 5 bộ `ĐẠT rc=0` với bằng chứng dương đúng mẫu (CA 41/41·ĐỘT BIẾN 51/51 cho `mcp_gh`… nhưng bị cách ly nên không tính; `probe_mang` 9/9+11/11; `mcp_github_doc` 17/17; `gh_readback` 8/8; `chon_reviewer` 25/25+34/34; `subagent_ghi_detect` 34/34+34/34; `nhanh_don_duoc` 8/8). 2 bộ cách ly (`mcp_gh_test.py`, `pretooluse_guard_test.py`) in đúng `KHÔNG ĐO ĐƯỢC — môi trường=không xác định` (sandbox này không phải GitHub Actions Linux) và **không** cộng vào `do`. `TỔNG: ĐẠT` | khớp, và đúng vì đúng lý do (môi trường không khớp anchor, không phải vì bộ test tự nó xanh) |
| chiều (iv) "vị trí lạ ⇒ ĐỎ" có răng thật | lease luật 3 | Đặt `vi_tri_moi_la/du_ma_test.py` ở bản sao ngoài cây (không tồn tại trước) → `kiem()` báo `test ở vị trí chưa biết: vi_tri_moi_la/du_ma_test.py`, sẽ làm `TỔNG: ĐỎ` | khớp — răng thật, đúng lý do |
| "luật 1 (chỉ ops mức đỉnh) đã đủ loại 2 bản sao lưu trữ về CƠ CHẾ" | lease `luat_pham_vi.2_ops_reviews_la_kho_hien_vat` | Vô hiệu nhánh `OPS_REVIEWS` trong `tim()` (giữ nguyên luật 1) trên bản sao ngoài cây → hai tệp `ops/reviews/**` **RƠI VÀO `la`**, cổng báo `TỔNG: ĐỎ` | **KHÔNG khớp** — xem finding-02 |
| P1 cũ của bot (mcp_gh D8(a) đỏ trên Linux/py3.12 sẽ làm gate đỏ) | comment PR #370 @84fcbd19 | `mcp_gh_test.py` nay nằm trong `CACH_LY` (r3+), `chay_moi()` không cộng `do` khi cách ly được chấp nhận hoặc không đo được | **ĐÃ VÁ** — stale ở sha hiện tại |
| P2 cũ của bot (0/N được chấp nhận vì không bắt cặp số đột biến) | comment PR #370 @84fcbd19 | `bang_chung_xanh("CA : 0/0 đạt · 0 đỏ · ĐẠT\nĐỘT BIẾN…TỔNG: ĐẠT")` → `False` (đo trực tiếp bằng import module) | **ĐÃ VÁ** — stale ở sha hiện tại |
| P2 cũ của bot (khớp "đã nối vào workflow" bằng chuỗi thô, comment cũng tính) | comment PR #370 @84fcbd19 | Đo lại: **VẪN ĐÚNG** ở `4082ab5`, và mức độ nghiêm trọng hơn khai — xem finding-01 (tôi nâng P2→P1 kèm lý do) |
| Bốn dòng thêm vào `ci.yml`: vị trí, không bị `exit` sớm che, comment đúng sự thật | brief Q7 | Vị trí: ngay sau bước `packet-loop selftest` (dòng 111-112), trước `idiom-ba-ten selftest`. Không bước nào trước nó có `exit`/`continue-on-error` (grep toàn tệp: 0 chỗ `continue-on-error` thật, chỉ 1 chỗ trong *comment* giải thích). Comment 2 dòng tại chỗ thêm nói đúng ý định (không tuyên bố sai về cơ chế — khác với lease) | khớp |
| Bộ tự canh (`phan_chung`) đỏ đúng lý do, không phải trùng hợp | brief Q5 | Gọi `kiem()` trực tiếp cho cả 4 chiều + 2 ca cách ly-thiếu-trường, in `loi` — mỗi ca có đúng dòng lỗi tương ứng dimension nó tuyên (xem log trong ĐÃ THỬ NGHIỆM của các finding) | khớp |

## ĐỐI CHIẾU LƯỢT TRƯỚC
Không áp dụng — đây là lượt cross-review thứ nhất theo đúng khai của brief (lượt phóng trước trả về rỗng vì lỗi thiết kế nhiệm vụ điều phối, không phải một verdict). Có tìm thấy tàn dư của lượt đó trong scratchpad phiên này (`findings_notes.md`, `mut_tree/`, các `out_*.txt`) — đó là bằng chứng THẬT nhưng đo trên **snapshot cũ hơn r4** (thiếu `CACH_LY`, `moi_truong_hien_tai`, `cach_ly_chap_nhan` — xác nhận bằng `diff` giữa `mut_tree` và cây hiện tại). Hai kết luận của nó (F1 so chuỗi thô chấp nhận comment; F2 lease khai sai cơ chế loại `ops/reviews/**`) đã được **ĐO LẠI ĐỘC LẬP trên đúng sha `4082ab5`** ở đây (không chỉ tin lại), và cả hai vẫn đúng — xem finding-01/finding-02.

---

### finding-01-comment-gia-mao-loi-goi-that  [P1]  Chiều (iii) — và cả kiểm DA_NOI — bị lừa bởi CHUỖI trong COMMENT, không phân biệt với `run:` thật

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:74-86` (hàm `kiem`, khối `for x in sorted(DA_NOI): ... co = x in workflows` và dòng `if "python .claude/dev/ci_dang_ky_test.py --chay" not in workflows`)

VẤN ĐỀ: Cả phép kiểm "CI có thật sự gọi mục MOI (`--chay`)" lẫn phép kiểm "CI có thật sự gọi mỗi mục DA_NOI" đều là **substring match trên toàn bộ văn bản YAML nối lại** của mọi `*.yml` dưới `.github/workflows/`, không phân biệt dòng đó nằm trong một bước `run:` THẬT hay chỉ là một dòng **comment** nhắc lại đúng chuỗi lệnh để giải thích. `ci.yml` hiện đã có thói quen viết comment giải thích ngay sát bước liên quan (kể cả 2 dòng packet này vừa thêm), nên đây không phải kịch bản giả định.

Đây **chính xác** là chiều được lease mô tả là "bắt được đúng cái lỗ đã sinh ra packet" (chiều (iii): "mục trong sổ mà `ci.yml` KHÔNG thật sự gọi ⇒ ĐỎ") — và chiều đó có một đường lách thật, không cần sửa write set nào khác ngoài `ci.yml`.

BẰNG CHỨNG: Trên bản sao ngoài cây (`/tmp/.../scratchpad/mut_r4`, clone `.claude` + `.github` + `.githooks` + `ops` + `scripts` từ đúng sha `4082ab5`):
1. Thay bước thật
   ```
   - name: test registry (phạm vi + các bộ chưa được nối)
     run: python .claude/dev/ci_dang_ky_test.py --chay
   ```
   bằng một dòng comment `# (tạm tắt để debug — dòng lệnh thật: python .claude/dev/ci_dang_ky_test.py --chay)` → chạy `python3 .claude/dev/ci_dang_ky_test.py` (không `--chay`) → `TỔNG: ĐẠT`, `RC=0`. Tức: xoá hẳn việc CHẠY 7 bộ test MOI khỏi CI thật, cổng vẫn báo ĐẠT.
2. Tương tự với một mục DA_NOI (`codex_cred_test.py`): xoá bước thật, giữ tên tệp trong comment → vẫn `TỔNG: ĐẠT`, `RC=0`.

ĐÃ THỬ VÁ: không — reviewer không vá theo lease. Hướng vá khả dĩ (không áp dụng, chỉ ghi để executor tham khảo): so khớp theo dòng bắt đầu bằng `run:` hoặc parse YAML thành step object thay vì nối toàn văn bản thô, hoặc chí ít bỏ dòng bắt đầu bằng khoảng trắng + `#` trước khi khớp chuỗi.

ĐÃ THỬ NGHIỆM: hai lệnh trên, log ở `/tmp/.../scratchpad/mut_r4` (đã xoá sau khi ghi verdict, có thể dựng lại bằng đúng hai bước ở BẰNG CHỨNG).

ĐỘ TIN: cao — đo trực tiếp trên đúng sha đang review, không suy diễn.

**Vì sao nâng từ P2 (khai của bot cùng nhà cung cấp với executor) lên P1**: bot chỉ nói "một đường nằm trong chú thích/import cũng tính là đã nối" mà không nói rõ hậu quả là gì. Đo lại cho thấy hậu quả là: **toàn bộ 7 bộ test MOI + toàn bộ 12 bộ DA_NOI có thể ngừng chạy trong CI thật mà `TỔNG: ĐẠT`**, tức tái tạo NGUYÊN VẸN cái lỗ #319 mà packet này sinh ra để đóng, chỉ cần một sửa đổi một dòng trong đúng write set của packet (`ci.yml`), không cần quyền nào khác. `CLAUDE.md` đã ghi nhận đúng họ lỗi này ba lần độc lập (`[skip ci]` trong commit, biểu thức Actions trong comment, workflow `paths:` không chạy lần đầu) — đây là biến thể thứ tư, và packet #361 tồn tại chính vì họ lỗi ấy.

---

### finding-02-lease-khai-sai-co-che-loai-tru-ops-reviews  [P2]  `luat_pham_vi.2` khai nhầm CƠ CHẾ loại `ops/reviews/**`, không phải lỗi mã

TỆP/DÒNG: hồ sơ lease `ops/leases/cong-ngoai-write-set-exec-1r4-codex-20260828.yaml`, mục `luat_pham_vi.2_ops_reviews_la_kho_hien_vat` (không phải mã trong write set — mã không sai, chỉ tài liệu sai).

VẤN ĐỀ: Lease khẳng định "luật `1` (chỉ mức đỉnh của `ops/`) đã đủ loại hai bản sao ấy về mặt CƠ CHẾ; luật `2` chỉ tồn tại để ghi LÝ DO". Sai: cơ chế THẬT loại hai tệp `ops/reviews/goi-va-lease-hoi-toan-kho-{1,2}/lease_publish_test.py` là nhánh kiểm **tên thư mục** `OPS_REVIEWS = "ops/reviews/"` chạy TRƯỚC trong `tim()` (`.claude/dev/ci_dang_ky_test.py:55-56`) — một loại trừ theo TÊN TỆP, đúng hình dạng "danh sách cấm đội lốt" mà `CLAUDE.md` đã cảnh báo (`"Danh sách CẤM không bao giờ đủ"`). Nếu bỏ nhánh đó mà chỉ giữ "luật 1", hai tệp này **không được loại êm** — chúng rơi vào `la` ("vị trí chưa biết") và làm chiều (iv) bắn ĐỎ.

Không phải lỗ an ninh (mã hiện tại vẫn fail-closed đúng cho vị trí lạ khác), nhưng rủi ro thực hành: người đọc lease tin "luật 1 tự lo" rồi coi nhánh `OPS_REVIEWS` là thừa và xoá nó đi ⇒ cổng ĐỎ giả vĩnh viễn cho hai hiện vật review — một hồi quy dễ xảy ra vì chính lý do lease đưa ra để không xoá nó lại sai.

BẰNG CHỨNG: Trên bản sao ngoài cây (đúng sha `4082ab5`), vô hiệu hoá nhánh `if q.startswith(OPS_REVIEWS): hien_vat.add(q)` (thay bằng `if False: ...`), giữ nguyên "luật 1":
```
ĐỎ: test ở vị trí chưa biết: ops/reviews/goi-va-lease-hoi-toan-kho-1/lease_publish_test.py
ĐỎ: test ở vị trí chưa biết: ops/reviews/goi-va-lease-hoi-toan-kho-2/lease_publish_test.py
ĐĂNG KÝ: 20/20
TRẠNG THÁI: chan=18 cach_ly=2
TỔNG: ĐỎ
RC=1
```

ĐÃ THỬ VÁ: không (thuộc phạm vi tài liệu/lease, không phải write set của packet).

ĐÃ THỬ NGHIỆM: lệnh trên, chạy trực tiếp bằng `python3.exec_module` sau khi patch file bằng script, output như trên.

ĐỘ TIN: cao.

---

### finding-03-cach-ly-moi-truong-khong-duoc-kiem-hop-le-nen-co-the-vinh-vien-vo-hieu-luat-b  [P1]  Giá trị `moi_truong` trong một mục `cách_ly` không bị kiểm so với tập giá trị THẬT mà `moi_truong_hien_tai()` có thể trả — một chuỗi lệch (kể cả gõ nhầm) làm luật (b) **vĩnh viễn không bao giờ thi hành được**, kể cả khi chạy đúng trên GitHub Actions Linux và test đã xanh thật

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:97-108` (`moi_truong_hien_tai`, `cach_ly_chap_nhan`) và `:71-73` (đoạn kiểm cấu trúc của `kiem()` cho mục cách ly).

VẤN ĐỀ: `moi_truong_hien_tai()` chỉ có đúng **hai** giá trị khả dĩ: `"github-actions/linux"` hoặc `None`. `kiem()` chỉ kiểm bốn trường `slug/ly_do/moi_truong/log` **không rỗng** (`all(no.get(k) for k in (...))`) — không kiểm `moi_truong` có phải MỘT TRONG những giá trị mà `moi_truong_hien_tai()` thực sự có thể trả về hay không. Nếu một mục cách ly khai `moi_truong` bằng bất kỳ chuỗi nào khác `"github-actions/linux"` (gõ nhầm — ví dụ thiếu một chữ — hoặc cố ý), thì `hien_tai != da_neo` **luôn luôn đúng** ở MỌI nơi chạy, kể cả chính runner GitHub Actions Linux thật. Hệ quả: `cach_ly_chap_nhan(...)` luôn trả `None` ("KHÔNG ĐO ĐƯỢC"), **không bao giờ** trả `False` (ĐỎ) dù bộ test đã chuyển xanh thật trên đúng CI. Đây chính là câu hỏi brief đặt ra ở Q2/Q3: cơ chế cách ly CÓ THỂ bị dùng để giấu vĩnh viễn một bộ test đỏ (hoặc đã xanh mà không ai biết) — bằng một lỗi chính tả hoặc một chuỗi tự chọn, không cần sửa logic nào. `kiem()` và `phan_chung()` đều không phát hiện được việc này: cả hai chỉ đo trên GIÁ TRỊ CÓ MẶT, không đo trên GIÁ TRỊ HỢP LỆ (đúng bệnh "đếm sự CÓ MẶT thay vì KHẢ NĂNG" mà `CLAUDE.md` đã ghi nhận nhiều lần).

r4 tự nhận mục đích của nó là chữa đúng lỗ này ở r3 ("cách ly phải neo môi trường... `(b)` là thứ DUY NHẤT ngăn cách ly sống lâu hơn nguyên nhân của nó"). Đo được: r4 THÊM đúng cơ chế neo, nhưng **không khoá được chính giá trị neo** — nên "chữa" chỉ đúng cho ca vô tình (môi trường thật sự khác), không đúng cho ca dữ liệu neo sai/giả — tức mới **đổi chỗ**, chưa đóng hết lỗ mà chính nó tuyên bố đóng.

Lưu ý phụ (không phải finding riêng, cùng gốc): kể cả khi `moi_truong` đúng, không có TTL/hạn cho một mục cách ly đỏ MÃI MÃI trên đúng môi trường neo — nhưng đó là giới hạn ĐÃ ĐƯỢC lease khai rõ và chấp nhận có chủ đích (nợ có tên), khác với lỗ này là ÂM THẦM và KHÔNG được khai.

BẰNG CHỨNG (đo trực tiếp bằng cách import module thật, không mock):
```
kiem() báo lỗi cho moi_truong="github-actions/lin-typo": []   # KHÔNG báo lỗi nào
hien_tai trên môi trường GHA-Linux thật (mô phỏng env): 'github-actions/linux'
cach_ly_chap_nhan(ok=True [đã xanh thật], da_neo="github-actions/lin-typo", hien_tai="github-actions/linux") -> None
```
(`ok=True` mô phỏng đúng ca "bộ test đã tự lành" mà chiều (b) được sinh ra để bắt; kết quả đúng ra phải là `False`/ĐỎ theo đặc tả `cach_ly_fail_close_hai_chieu.(b)`, nhưng ra `None`.)

ĐÃ THỬ VÁ: không.

ĐÃ THỬ NGHIỆM: script Python trên, chạy trực tiếp trong workspace đang review (đọc module thật bằng `importlib`, không sửa tệp).

ĐỘ TIN: cao — không phụ thuộc giả định, đo trực tiếp hàm thật với input hợp lệ về hình thức (qua được `kiem()`).

---

## Trả lời trực tiếp các câu hỏi còn lại của brief

**Q1 (chiều iv có răng thật?):** Có. Đặt `vi_tri_moi_la/du_ma_test.py` (tên/vị trí chưa từng tồn tại) vào bản sao ngoài cây → `kiem()` báo đúng `"test ở vị trí chưa biết: vi_tri_moi_la/du_ma_test.py"`, sẽ làm `TỔNG: ĐỎ`. Đỏ đúng vì đúng lý do (không phải vì entangled với chiều khác).

**Q2/Q3:** Trả lời bằng finding-03 ở trên — có, và đó là bệnh (r4 chưa đóng hết), không phải thiết kế cố ý.

**Q4:** 1 P1 cũ đã vá (mcp_gh vào CACH_LY). 1 P2 cũ đã vá (0/N bị bác đúng). 1 P2 cũ **vẫn đúng**, và đo sâu hơn cho thấy mức độ nghiêm trọng hơn khai ban đầu — nâng thành finding-01 (P1).

**Q5:** Đã kiểm 4 chiều phạm vi + 2 ca cách ly-thiếu-trường bằng cách gọi thẳng `kiem()` với input tối giản, đọc chuỗi lỗi trả về — mỗi ca đúng đúng dòng lỗi của đúng chiều nó tuyên, không phải trùng hợp.

**Q6:** `--chay` cho `TỔNG: ĐẠT`, đúng và đúng lý do: 5 bộ chan+có-thể-đo đều thật sự `rc=0` kèm bằng chứng dương khớp mẫu; 2 bộ cách ly in `KHÔNG ĐO ĐƯỢC` vì môi trường sandbox này không phải GitHub Actions Linux — không bị tính vào `do`, và đúng theo đặc tả r4 (không phải bị bỏ qua âm thầm, có dòng in ra nói rõ).

**Q7:** Vị trí đúng (ngay sau `packet-loop selftest`, trước `idiom-ba-ten`). Không bước nào trước đó `exit`/`continue-on-error` che nó (grep toàn tệp: không có `continue-on-error` thật). Hai dòng comment kèm theo nói đúng ý định thật của mã (không lặp lại cái sai của lease ở finding-02).

**Q8:** Có — ba finding trên (01, 02, 03) đều mới so với 3 nhận xét cũ của bot connector; không cái nào trùng khoá với chúng dù finding-01 cùng CHỦ ĐỀ với một P2 cũ (đã nói rõ quan hệ và lý do nâng bậc).

## Ghi chú vận hành
- `mcp__github__pull_request_read` (MCP GitHub) bị từ chối quyền trong phiên này (permission not granted) — không đọc được 3 comment gốc của bot connector qua công cụ; đã dùng đúng bản tóm tắt trong brief làm input, rồi đo lại từng ý bằng mã thật thay vì tin nguyên văn.
- Kết quả gate GitHub Actions thật: KHÔNG ĐO ĐƯỢC trong phiên này (đúng như brief cảnh báo) — không suy ra màu.
- Không gặp `PermissionError` do cấm socket loopback trong lượt `--chay` này; toàn bộ 7 bộ chạy được (2 tự báo KHÔNG ĐO ĐƯỢC vì lý do môi trường, không phải lỗi quyền).
- Phát hiện phụ: có một tiến trình phóng từ lượt review TRƯỚC (PID nền, cùng brief) và một thư mục scratchpad có tàn dư dữ liệu của lượt đó — đã đối chiếu (không tin suông) và ghi rõ trong mục ĐỐI CHIẾU LƯỢT TRƯỚC.
- `git status --porcelain` sạch tại workspace `/home/user/rv361` trước khi ghi tệp verdict này (tệp verdict nằm ngoài chỉ mục git — không track).
