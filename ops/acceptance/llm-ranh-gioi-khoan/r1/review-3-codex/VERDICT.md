# Verdict packet #1514 r2 lượt 3 — Codex

reviewed_sha: 64153dbfb402bcf1d0ac7ecd614b7aa23bb57d8f
tree_sha: a379aaca2aee983d0f62e0cb535175bbc27e9104
base_sha: 64b7f2c14776d5d0e1d34a6be4725490956f5bec

VERDICT: REQUEST_CHANGES

Finding C1 giữ mở lỗi bỏ khoản đầu trong nguồn mất số. Selftest và doc-claims đỏ đồng nhất trên head và base.

## Đối chiếu lượt 2 và đặc tả r2

Checkout detached đúng SHA được giao. Blob spec ở SHA này và bản local cùng có SHA-256 `b2d0d15c437c0f4c130539730edbc03b00b7cb3e935d9c3ef31a75c553cbe70c`, trùng lease r2/g1.

- Review Class `sensitive`, revision 2/generation 1, lời gọi thứ 3/5 tính chung với r1. Lease r2 có hạn tới `2026-11-25T11:40:00Z`. Base là tổ tiên của head (`git merge-base --is-ancestor`, rc 0), tree base `0cc14e79cecd2ce44bc4dc6cff92cadb31fd7ee4`. Lượt 2 neo `53c49ab125290b0a937c60aefe5481201b42cd4e`, tree `60c69ec622d97f9458bec739623235b06a3aa6ba`. Hai ref cục bộ của nhánh được giao cùng trỏ vào head đã review.
- Run `8b08daa9b0254f8e8ee03fa9f2889288` khai `openai_codex / codex_cli / machine`, khớp mục reviewer trong lease. Executor theo lease là Claude Code (`anthropic_claude / claude_code / machine/local`). SHA-256 của prompt `7e082a533abe97676fd4ccdebc01c674c4bce187ebc38aee8bfdf5a7bd074020` khớp run và checkpoint. Sandbox `workspace-write`, Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0 và `core.abbrev=7`. Origin trong checkout nhận diện `ducthangho/tra-luat`.
- Spec được đọc từ blob `9893bbf2bda456eec15f001a4a6982901380a022` ở reviewed SHA và đối chiếu byte với bản local. Toàn bộ 15/15 tệp trong diff từ base và 11/11 tệp từ lượt 2 nằm trong write set r2. SHA-256 của danh sách 25 đường dẫn đã sắp và kết thúc bằng LF là `23eafa7bcd14940de42c2ea0a98c0a2c8d0fe0263c6534871740501a6ee95534`, khớp lease. `git diff --check 64b7f2c 64153db` rc 0. Hai lease trỏ ngược đúng ID qua `da_bi_thay_the` (r1) và `thay_the_cho` (r2). Cổng check r2 rc 0, có kiểm bia mộ bằng `_kiem_bia_mo`. [Lease r1](../ops/leases/llm-ranh-gioi-khoan-r1-g1-claude.yaml#L63) · [Lease r2](../ops/leases/llm-ranh-gioi-khoan-r2-g1-claude.yaml#L58) · [Cổng lease](../ops/lease_publish.py#L833)

| Mục | Trạng thái | Bằng chứng |
| --- | --- | --- |
| A1 và §2.3 | ĐÃ VÁ THẬT cho ca lượt 2 | Điều kiện `_tu_noi(ln) is None` trở lại. Ca đích từ chối kết quả bỏ dòng đầu có từ nối. Bỏ điều kiện làm ca đỏ. Hai câu dẫn chuẩn vẫn đạt, còn mẫu kết thúc hai chấm sai hậu tố bị chặn. [Mã](../scripts/tl_core/llm_route.py#L540) · [Ca A1](../scripts/tl_core/llm_route_test.py#L1016) |
| A2 | VÁ MỘT PHẦN | Ba ca tái hiện của lượt 2 đều bị chặn. Lớp bỏ khoản đầu còn mở tại C1. |
| A2a và §2.2 | ĐÃ VÁ THẬT cho mẫu ngắt ở chấm phẩy | §2.5 thu hẹp tập dấu của §2.2 thành `.`, `!`, `?`. Kiểm sau khi gom điểm, nên chấm phẩy ở điểm chưa cuối vẫn qua. Bật lại chấm phẩy làm ca A2a đỏ. Các mẫu X3b/X3c và đối chứng khoản mở bằng hai chấm, có điểm theo sau, đều qua. [Mã](../scripts/tl_core/llm_route.py#L548) · [Ca A2a](../scripts/tl_core/llm_route_test.py#L1019) |
| A2b | ĐÃ VÁ THẬT cho luật và ca lượt 2 | Regex trùng §2.5 và chạy trên thân đã bỏ số khoản. Bỏ cả chốt làm mẫu tiểu mục đỏ. Làm rộng regex để nhận số thập phân cũng làm ca đối chứng đỏ. Dạng số trong ngoặc có căn cứ đọc regex, phần đo riêng xem mục cuối. [Mã](../scripts/tl_core/llm_route.py#L495) · [Ca A2b](../scripts/tl_core/llm_route_test.py#L1022) |
| A2c | VÁ MỘT PHẦN | Quét cả dòng tiêu đề bắt được mẫu có từ “là” sau dấu hai chấm. Đổi về `_tu_noi` làm đỏ đúng ca A2c. Regex vẫn buộc khoảng trắng hoặc biên dòng hai bên, hẹp hơn “ở bất kỳ đâu” khi từ đứng sát dấu câu. Xem C1. [Mã](../scripts/tl_core/llm_route.py#L519) · [Ca A2c](../scripts/tl_core/llm_route_test.py#L1028) |
| A3 | ĐÃ VÁ THẬT | Một lần xóa cả dải cuối gồm khoảng trắng và dấu đóng. Khôi phục cách tỉa lần lượt làm mẫu có khoảng trắng xen dấu đóng đỏ. [Mã](../scripts/tl_core/llm_route.py#L555) · [Ca A3](../scripts/tl_core/llm_route_test.py#L1031) |
| A4 và §4.6 | ĐÃ VÁ THẬT trong fixture offline | Nguồn đóng gói trong test có tám khoản mất số. Suite xác nhận 8/8 cho từng bản lưu `kn_tl`, `kn_sub`, `kn_api` sau cùng bước chuẩn hóa runtime. [Fixture](../scripts/tl_core/llm_route_test.py#L84) · [Ca A4](../scripts/tl_core/llm_route_test.py#L1035) |
| §2.1 và §4.1 | ĐẠT | Chốt từ ba nháy kép thẳng chạy trên dòng đã gỡ dấu đầu. Bỏ chốt làm mẫu bốn nháy đỏ, đối chứng một cặp nháy đạt. [Mã](../scripts/tl_core/llm_route.py#L583) · [Ca X2](../scripts/tl_core/llm_route_test.py#L981) |
| §2.4 và §4.5 | ĐẠT | So từng vế với bản chuẩn hóa giữ xuống dòng. Ca giữ xuống dòng đạt, ca dồn hai điểm báo lệch khoản 1. Đột biến gộp khoảng trắng qua dòng làm ca X4 đỏ. [Mã](../scripts/tl_core/llm_route.py#L563) · [Ca X4](../scripts/tl_core/llm_route_test.py#L1003) |
| §1 | GIỮ NGUYÊN trong diff | Đường gọi model giữ nguyên. Handler vẫn gắn `can_nguoi_duyet: true` và `pham_vi_kiem`, đồng thời yêu cầu số, thứ tự và hai vế khớp theo phân đoạn trước khi ghi `--out`. [So khớp](../scripts/tl_core/llm_route.py#L656) · [Handler](../scripts/tl_core/ops_misc.py#L3100) |

## Findings

### C1 [P1] Nhánh tiêu đề vẫn có thể bỏ khoản đầu dính cùng dòng — `scripts/tl_core/llm_route.py:519`

**Kịch bản.** Khi chuyển sang text, nguồn mất số tự động và dòng tiêu đề nhập với khoản đầu. Nếu khoản đầu là một đoạn dùng từ nối thiếu chữ “là”, chẳng hạn kiểu định nghĩa bằng “bao gồm”, dòng ghép có thể bị xóa nguyên. Các khoản còn lại vẫn có thể là những đoạn hoàn chỉnh với số và nội dung khớp cách quét. Cấu trúc định nghĩa dùng “bao gồm” đã xuất hiện trong các nguồn thật được đối chiếu ở PR #1503 lượt 3. Việc mất số và dính tiêu đề là hai biến đổi định dạng đã được ghi nhận như rủi ro của nguồn thô. Không cần sửa nội dung định nghĩa để phát sinh trường hợp này. [Hồ sơ nguồn](../ops/reviews/pr1503-review-3-codex/VERDICT.md#L33) · [Giới hạn công bố](../docs/GOI_AGENT_DA_NEN.md#L373)

**Căn cứ.** `_RE_TIEU_DE_DIEU` chỉ neo tiền tố. Sau khi khớp, `_RE_LA.search` quyết định giữa từ chối và `dong = dong[1:]`. Ngay cả từ “là” ở dạng thường cũng bị bỏ sót khi đứng sát dấu mở trích dẫn thay cho khoảng trắng. Điểm quyết định là dấu hiệu trên chính dòng đã bị xóa trước khi chốt dấu câu và đánh số nội dòng chạy. `lech_nguyen_van` đếm các khoản còn lại từ 1. Nếu model cũng bỏ mục đó, phép so có thể trả `[]`, lệnh có thể trả rc 0 và ghi `--out` cùng cờ cần người duyệt. Tài liệu hiện khẳng định cả tiêu đề dính khoản đầu lẫn khoản dùng từ nối khác “là” sẽ bị từ chối. Hạng P1 dựa trên đường bỏ cả khoản có từ nối khác trong văn bản thông thường. Biến thể sát dấu câu là phần hở riêng so với chữ “bất kỳ đâu” của A2c. [Nhận diện tiêu đề](../scripts/tl_core/llm_route.py#L67) · [Bỏ dòng](../scripts/tl_core/llm_route.py#L519) · [Đếm lại](../scripts/tl_core/llm_route.py#L662) · [Ghi kết quả](../scripts/tl_core/ops_misc.py#L3103)

**Đề xuất.** Chỉ bỏ dòng khi xác định được toàn dòng là tiêu đề của điều giải thích từ ngữ. Khi có phần dư chưa phân loại được, từ chối nguồn. Phép kiểm từ trong tiêu đề cần nhận biên từ bên dấu câu. Ca đóng lớp cần kiểm giữ tiêu đề độc lập, từ chối tiêu đề dính định nghĩa dùng từ nối khác và từ chối dạng “là” sát dấu mở. Tập tiêu đề được nhận quá hẹp có thể chặn tiêu đề hợp lệ có tên khác, nên đo cả tiêu đề hợp lệ có và không có phần tên.

### C2 [P2] Dấu chấm sau số ở cuối một dòng điểm có thể bị đọc thành số thứ tự nội dòng — `scripts/tl_core/llm_route.py:550`

**Kịch bản và căn cứ.** Một định nghĩa có các điểm chữ cái, trong đó một điểm kết thúc bằng câu dẫn chiếu có số điều ở cuối câu và điểm sau bắt đầu ở dòng kế. Parser nối điểm vào thân khoản bằng `\n`. Mẫu `(?=\s)` chấp nhận chính ký tự xuống dòng sau dấu chấm, nên số điều ở cuối câu khớp `_RE_SO_NOI_DONG` và cả nguồn bị từ chối. Đây là hình thức dẫn chiếu ở cuối câu giữa hai điểm đã nhận rõ cấp. Giới hạn r2 mô tả số thứ tự nội dòng và nêu ví dụ dẫn chiếu có phần chữ tiếp sau trên cùng dòng. Hệ quả qua ranh giới hai điểm chưa được nêu. Mã khớp regex đóng băng, nên việc thu hẹp cần đi cùng sửa đặc tả. [Gom điểm](../scripts/tl_core/llm_route.py#L531) · [Kiểm thân khoản](../scripts/tl_core/llm_route.py#L550) · [§2.5](../ops/specs/llm-ranh-gioi-khoan-r2.md#L43)

**Đề xuất.** Áp chốt trên từng dòng vật lý hoặc giới hạn khoảng trắng bên phải trong phạm vi dòng. Ca đóng cần cho qua dẫn chiếu ở cuối một điểm theo sau bằng điểm khác, đồng thời tiếp tục chặn số thứ tự thật và giữ đối chứng số thập phân. Nếu nới, kiểm rủi ro của số thứ tự đứng riêng ở cuối dòng khi nội dung của tiểu mục bị dồn sang dòng sau.

| Lớp | Biểu hiện | Hạng còn mở | Nguồn và điều kiện đóng |
| --- | --- | --- | --- |
| `ranh-gioi-khoan` | A1 đóng theo ca gốc, A2a/A2b đóng theo ca gốc, A2c/C1 còn mở | P1 | Nối X3 của PR #1503 lượt 11 và A1/A2 ở `53c49ab`. C1 yêu cầu kiểm đường loại bỏ nguyên dòng trước khi phân khoản. |
| Dẫn chiếu ở cuối dòng điểm | C2 | P2 | Phát sinh khi áp A2b trên thân khoản đã nối dòng. Kiểm cả đối chứng dẫn chiếu và các mẫu tiểu mục thực. |

Ngoài C1, với nguồn mất số, mỗi dòng có hai vế và kết thúc hợp lệ vẫn được nhận là một khoản. Nếu hai câu thuộc cùng một khoản nhưng nằm trên hai dòng và mỗi câu có “là”, mã có thể nhận kết quả tách thành hai mục. Đây là hệ quả của quy tắc mỗi dòng một khoản đã công bố. Câu dẫn cũng được xét lặp khi danh sách khoản còn rỗng. Đọc mã thấy nguy cơ bỏ thêm dòng nếu bản text mất số có dòng mở đầu khoản trùng hậu tố câu dẫn, đứng trước một phần tiếp dòng có hình dạng định nghĩa độc lập và không có dấu điểm. Chưa có bằng chứng địa phương rằng dạng sau là thông dụng. [Phân khoản](../scripts/tl_core/llm_route.py#L527) · [Giới hạn](../docs/GOI_AGENT_DA_NEN.md#L373)

## Kết quả test và đột biến

Log ở `/tmp/wp1514-review.v9VXifxV/`. Các test chạy với môi trường tối giản, HOME và cache riêng, bytecode tắt. Git ở các cổng dùng transport file. Các cổng sinh fixture hoặc quét nội dung gói chạy trên bản sao detached ngoài checkout được giao, ở cùng SHA/tree. Bản đối chứng dùng exact base đã nêu.

| Lệnh | Trạng thái | rc và bằng chứng |
| --- | --- | --- |
| `python scripts/tl_core/llm_route_test.py` | `passed` | 0. 50/50 ca đạt, 93/93 đột biến bị giết. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed` | 0. `ok=true`, 26 card, 60 task, 194 lệnh khả dụng, 0 lỗi và 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed` | 0. 20/20 ca đạt, 20/20 ổn định byte thô trong lần đo. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed` | 0. `ok=true`, 187/187 tệp, 0 thiếu/thừa/sai. Package hash khớp `cc4932f41e04341b12c209d8dcac0afc270e4508933e53863aa14a5ef2011c37`. |
| `python ops/lease_publish.py check --root . ops/leases/llm-ranh-gioi-khoan-r2-g1-claude.yaml` | `passed` offline | 0. `ĐĂNG ĐƯỢC` cho #1514, neo `64b7f2c14776`, hạn `2026-11-25T11:40:00Z`. |
| `python scripts/tl.py --selftest` | `failed` trên cả head và base | 1 trên mỗi mốc. Cả hai đạt 1775/1789. Danh sách ID và trạng thái ca trùng nhau. Cùng 14 ca đỏ trong sandbox có `/tmp/.git` rỗng, gồm 8 `r973_bootstrap_*`, 5 `wp433_*` và 1 `wp727_tl_gws_refresh`. Delta ca đỏ 0. |
| `python scripts/tl.py --deterministic determinism-audit --strict --json` | `passed` | 0. 15/15 phép kiểm đạt, `ok=true`. |
| `python scripts/tl.py --deterministic doc-claims-check --strict --json` | `failed` trên cả head và base | 2 trên mỗi mốc. Cùng một cờ cứng `SHA_NOT_A_COMMIT` cho `9941d8af52aeede1c78ea4e232fbe9a8d5272033` ở `docs/PROTOCOL_DA_PHIEN.md:1680`. Delta cờ cứng 0 trong checkout nông. |
| `python -m ruff check --no-cache --select F scripts/tl.py` | `failed` trên cả head và base, đạt tiêu chí delta | 1 trên mỗi mốc. Ruff 0.15.15, 12 lỗi trên mỗi mốc, stdout trùng byte. Delta 0. |

### Đột biến có sẵn

`python -m pdb <đường dẫn tuyệt đối tới scripts/tl_core/llm_route_test.py>` quan sát ở nhánh bắt `TinHieuChotCa` dòng 1263. Suite và debugger đều trả rc 0 sau phép kiểm. Các đột biến thay mã trên tệp tạm do bộ test tạo. Bảng ghi khẳng định đầu tiên thực sự đỏ trong từng đột biến của packet.

| Đột biến | Lý do ca đích đỏ |
| --- | --- |
| `wp1514_l2_cau_dan_bo_tu_noi` | A1. Dòng có từ nối bị bỏ như câu dẫn. |
| `wp1514_l2_cham_phay_ket_cau` | A2a. Hai mảnh trước và sau chấm phẩy bị nhận thành hai khoản. |
| `wp1514_l2_hai_cham_ket_cau` | X3c. Dòng có số kế tiếp được nhận khi khoản trước còn mở bằng hai chấm. |
| `wp1514_l2_bo_so_noi_dong` | A2b. Thân có số nội dòng vẫn qua cùng dãy số khoản liên tục. |
| `wp1514_l2_so_noi_dong_nhan_thap_phan` | A2b. Đối chứng số thập phân bị từ chối. |
| `wp1514_l2_tieu_de_chi_tu_noi` | A2c. Dòng tiêu đề và khoản đầu cùng bị bỏ, chỉ còn khoản sau. |
| `wp1514_l2_duoi_mot_luot` | A3. Dấu đóng xen khoảng trắng làm khoản hợp lệ bị từ chối. |
| `wp1514_bo_x2` | X2. Dòng có bốn nháy kép thẳng qua chốt mơ hồ. |
| `wp1514_bo_ket_cau` | X3b. Dòng gãy trước dấu câu kết được nhận làm một khoản. |
| `wp1514_cau_dan_moi_hai_cham` | X3. Dòng mở không khớp hậu tố lại bị bỏ như câu dẫn. |
| `wp1514_gon_gop_dong` | X4. Dồn các dòng điểm thành một dòng vẫn qua phép so. |

## Không đo được

- C1 và C2 là kết luận đọc mã. Chưa đo trực tiếp các biến thể hoặc tần suất của chúng trong corpus. Chưa đo riêng biến thể số trong ngoặc của A2b bằng ca đích. Phép thử 8/8 dùng ba kết quả đã lưu trong fixture của candidate, chưa đối soát byte với bản thu gốc ngoài checkout.
- Windows bản địa §3 là `not_run` và `not_measured` trên Linux offline. Suite đã chạy nhánh mô phỏng Windows. Claude/Anthropic thật, `tl llm-khai-niem` thật và GitHub/CI từ xa đều `not_run`. Không có bộ nào trong danh sách cách đo được báo `skipped`.
- Model và effort phục vụ là `KHONG_DO_DUOC` từ hiện vật của lượt. `run.json` còn ở `dang_chay` khi ghi, nên mã thoát launcher và hash stdout của cả phiên sẽ cần readback sau khi kết thúc.

Đối chiếu cuối bằng `git rev-parse HEAD 'HEAD^{tree}'`, `git diff --exit-code` và `git diff --cached --exit-code` cho đúng SHA/tree và rc 0. Trạng thái đầu đã có `.codex/` ignored. Trạng thái cuối chỉ thêm `.review/VERDICT.md`. Phép so quan sát trạng thái ở đầu và cuối phiên, ngoài phạm vi đọc nội dung `.codex/` và repo nguồn của Executor.

VERDICT: REQUEST_CHANGES
