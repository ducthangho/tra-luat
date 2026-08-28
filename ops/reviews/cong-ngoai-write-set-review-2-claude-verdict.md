verdict: changes_requested
reviewed_sha: 7116d6c74349a91f12c3ef060de9c689aac2e822
P1: 1
P2: 2
finding_moi: 1

## ĐỐI CHIẾU LƯỢT TRƯỚC

Lượt 1 (`claude`, cross-provider, `reviewed_sha 4082ab5`) trả `changes_requested`, P1=2, P2=1.
Cả ba đo lại **độc lập** trên `7116d6c` (không dùng thông điệp commit, không dùng lời khai lease
r5 làm bằng chứng) — xem BẰNG CHỨNG trong từng finding tương ứng bên dưới.

- **finding-01 (P1, chuỗi trong chú thích giả mạo lời gọi thật)**: **ĐÃ VÁ THẬT, có giới hạn.**
  `kiem()` nay parse YAML bằng `yaml.safe_load`, lấy đúng trường `run:` của từng step đã cấu trúc
  hoá, và lọc dòng bắt đầu bằng `#` NGAY TRONG thân `run`. Tự dựng lại đúng kịch bản của lượt 1
  (xoá bước `run:` thật, giữ nguyên chuỗi lệnh trong một dòng chú thích YAML) trên bản sao ngoài
  cây (script riêng, không dùng `phan_chung()` có sẵn của chính tệp làm bằng chứng cho chính nó)
  → cổng báo đúng `CI không gọi mục đăng ký`, không còn bị lừa bởi chú thích. **Nhưng** phép sửa
  chỉ đổi "so chuỗi trên toàn văn bản" thành "so chuỗi trên văn bản `run:` đã lọc chú thích" — vẫn
  KHÔNG đọc `if:`. Tôi tự dựng ba biến thể mới (step `if: false`, job `if: false`, step với biểu
  thức luôn sai) và cả ba đều LỌT — xem finding-02. Tức: đóng đúng lỗ ĐÃ NÊU (chú thích), chưa đóng
  cùng HỌ lỗi (tĩnh trạng "có mặt trong `run:`" ≠ "GitHub thật sự thi hành").

- **finding-02 P2 lượt 1 (lease khai sai cơ chế loại `ops/reviews/**`)**: **ĐÃ VÁ ĐÚNG, trong tài
  liệu (không cần vá mã).** Tự vô hiệu nhánh `OPS_REVIEWS` trong `tim()` trên bản sao module thật
  (không sửa tệp), giữ nguyên "luật 1" (`GOC`) → hai tệp `ops/reviews/goi-va-lease-hoi-toan-kho-{1,2}`
  rơi vào `la` (vị trí lạ), xác nhận đúng như đính chính ở `luat_pham_vi.2` của lease r5: nhánh
  `OPS_REVIEWS` chạy TRƯỚC và là cơ chế loại trừ THẬT — "luật 1" một mình không tự lo được. Mã
  không đổi ở r5 (đúng như lease khai), chỉ tài liệu đổi, và tài liệu đổi ĐÚNG.

- **finding-03 P1 lượt 1 (giá trị `moi_truong` không bị khoá)**: **ĐÃ VÁ THẬT.** Nay `MOI_TRUONG_CI`
  là hằng số DUY NHẤT; `moi_truong_hien_tai()` trả đúng hằng số ấy hoặc `None`, và `kiem()` từ chối
  mọi mục cách ly có `moi_truong` khác hằng số đó (kể cả gõ nhầm một chữ, kể cả giá trị bất kỳ khác
  loại). Grep toàn tệp xác nhận không có bản chép thứ hai của chuỗi `"github-actions/linux"` nào
  nằm NGOÀI cơ chế kiểm — hai chỗ còn hardcode chuỗi đó là DỮ LIỆU của `CACH_LY` (đúng bản chất,
  phải là literal) và bị chính `kiem()` xác thực so với `MOI_TRUONG_CI`; ba chỗ khác chỉ là input
  test thuần cho hàm `cach_ly_chap_nhan()`, không phải nguồn thứ hai có thể trôi. Tự dựng đột biến
  neo `"github-actions/lin-typo"` trên module thật → đỏ đúng ở tầng cấu trúc (`cách ly có môi
  trường không hợp lệ`), không rơi xuống `None`/KHÔNG ĐO ĐƯỢC như trước khi vá.

## BẢNG ĐO

| khẳng định | hồ sơ khai (lease r5 / brief) | đo được (lượt này) | khớp? |
|---|---|---|---|
| numstat 226+4=230, dưới trần 240 | lease `ngan_sach_kich_thuoc` | `git diff --numstat 58b85cc2 7116d6c`: `ci_dang_ky_test.py` 226/0, `ci.yml` 4/0 = **230** | khớp |
| neo r5 riêng = 29 dòng | lease `neo_do_duoc` | `git diff --numstat 8fe6dcd 7116d6c`: **29 thêm / 3 xoá** (net +26) trên đúng `ci_dang_ky_test.py` | khớp — đúng 29, không phải số tròn |
| `python3 ci_dang_ky_test.py`, N/N | brief | `ĐĂNG KÝ: 21/21`, `PHẢN CHỨNG: 13/13 đỏ đúng`, `TỔNG: ĐẠT`, `RC_DIRECT=0` (đo `$?` ngay sau lời gọi trần, không qua ống) | khớp |
| 13 phản chứng đỏ đúng | brief | Đúng 13/13, liệt kê đủ tên: `i-thieu-so` … `rc-xanh-thieu-ban-in` | khớp |
| chỉ 2 tệp trong write set bị đổi | lease `write_set` | `git diff --stat 58b85cc2 7116d6c`: đúng 2 tệp | khớp |
| `git diff --check` sạch | — (tự kiểm) | rc=0, không có whitespace error | khớp |
| `doctrine-scan` sạch | CLAUDE.md | `doctrine-scan: sạch — đã quét 7 tệp, 0 chỗ chép doctrine`, rc=0 | khớp |
| `duyet_danh_tinh_test.py` → nhóm ĐÃ NỐI | lease `viec_4` | Grep `.github/workflows/duyet-phan-chung.yml:62` gọi thật `"$PY" .claude/dev/duyet_danh_tinh_test.py`; `kiem()` thật trên cây thật → `loi=[]`, `21/21` (không lỗi cho mục này) | khớp |
| `if: false` vẫn bị tính là "đã nối" (tự khai) | commit msg + lease `phan_chung_moi_cua_r5` | Tự dựng 3 biến thể độc lập (step `if: false`, job `if: false`, `if:` biểu thức luôn sai) trên `kiem()` thật qua `importlib` — cả 3 LỌT, không báo lỗi | khớp — khe có thật, đúng như khai |
| `--chay`: gate GitHub Actions | brief | KHÔNG ĐO ĐƯỢC — không có `gh`, REST `api.github.com/repos/...` trả 403 (chặn ở tầng proxy/tổ chức, không có header GitHub) | khớp cảnh báo của brief |

## finding-02-if-false-vinh-vien-vo-hieu-chieu-iii  [P1]  Cùng họ với P1-01: `if: false` (step hoặc job) làm một `run:` KHÔNG BAO GIỜ chạy vẫn được tính là "đã nối"

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:80-101` (khối `if workflows is None: ...` trong `kiem()`)

VẤN ĐỀ: Bản vá r5 đổi "so chuỗi trên toàn văn bản YAML" thành "so chuỗi trên trường `run:` của
từng step đã parse, đã lọc dòng chú thích BÊN TRONG run" — đúng như executor tự khai, đây đóng
đúng kịch bản CỤ THỂ của P1-01 (chú thích giả mạo). Nhưng phép trích `runs` KHÔNG đọc `step.get("if")`
lẫn `job.get("if")`. Một step (hoặc cả job) mang `if: false` vẫn có `step.get("run")` là chuỗi hợp lệ,
nên dòng lệnh của nó vẫn được nối vào `workflows` và vẫn khớp `x in workflows` — trong khi GitHub
**không bao giờ chạy step đó**. Đây CHÍNH XÁC là chiều (iii) mà lease mô tả là "chiều bắt được đúng
cái lỗ đã sinh ra packet" (`mục trong sổ mà ci.yml KHÔNG thật sự gọi ⇒ ĐỎ") — và `if: false` là cách
rẻ nhất, không cần giả mạo comment gì cả, để tái tạo nguyên vẹn lỗ #319/#334 mà packet #361 tồn tại
để đóng.

Đây **cùng họ** với P1-01, không phải họ khác: cả hai đều là "kiểm SỰ CÓ MẶT tĩnh của văn bản `run:`
mà không kiểm KHẢ NĂNG thi hành thật của nó" — đúng bệnh "đếm sự CÓ MẶT thay vì KHẢ NĂNG" mà
`CLAUDE.md` đã ghi nhận nhiều lần trong kho này. Vá P1-01 mà để hở `if: false` nghĩa là: đã thu hẹp
đường lách từ "sửa bất kỳ dòng nào trong `.github/workflows/*.yml` cũng được, miễn giữ chuỗi ở đâu đó
trong tệp" xuống còn "thêm đúng MỘT dòng `if: false` ngay trên step thật" — vẫn nằm gọn trong write
set của packet, vẫn không cần kỹ xảo nào, và vẫn xoá sạch bảo đảm mà chiều (iii) tuyên bố cung cấp.

**Vì sao xếp P1, không phải P2 (dù đây là khe tự khai, không giấu):** Khác với các biến thể khó hơn ở
finding-03 (biểu thức Actions bất kỳ, dead-code trong shell — đòi trình thông dịch/evaluator tổng quát,
về nguyên tắc không giải được tĩnh), `if: false` / `if: 'false'` / `if: ${{ false }}` là giá trị YAML
CÓ THỂ đọc tĩnh, rẻ, và quyết định được dứt khoát — không đòi đánh giá biểu thức GitHub Actions tổng
quát nào. Việc không xử lý ngay cả trường hợp tĩnh, rẻ, quyết định-được này trong khi CHÍNH BẢN VÁ đã
đổi từ so-chuỗi-thô sang parse-YAML-có-cấu-trúc (tức đã cầm sẵn `step`/`job` dict trong tay, chỉ còn
thiếu một dòng kiểm `step.get("if")`) là để lại phần RẺ NHẤT của đúng lỗ mà packet tồn tại để đóng.
Tự khai không làm giảm mức nghiêm trọng của một lỗ còn sống trong tay; nó chỉ làm review này KHÔNG
BẤT NGỜ khi tìm ra — và đúng chỗ để reviewer xếp hạng chứ không phải chỗ để executor tự miễn trừ.

BẰNG CHỨNG (đo trực tiếp trên module thật bằng `importlib`, KHÔNG sửa tệp thật, xác nhận trên bản
sao thư mục tạm dưới `/tmp`, tự viết mới — không tái dùng `phan_chung()` sẵn có):
```
=== step-if-false ===                       *** LỌT — cổng KHÔNG phát hiện ***
=== job-if-false ===                        *** LỌT — cổng KHÔNG phát hiện ***
=== step-if-always-false-expr ===           *** LỌT — cổng KHÔNG phát hiện ***
=== baseline-normal-step (đối chứng) ===    (không lỗi — ĐÚNG, vì step này thật sự chạy)
```
(mỗi ca: root tạm với `.claude/dev/a_test.py` + một `.github/workflows/x.yml` chứa đúng một step,
gọi `kiem(r, {".claude/dev/a_test.py"}, None, {})` sau khi tạm đặt `DA_NOI = {".claude/dev/a_test.py"}`
trên module đã import, khôi phục lại `DA_NOI` cũ ngay sau — không để lại trạng thái méo.)

ĐÃ THỬ VÁ: không — nằm ngoài quyền reviewer (không sửa, không commit). Hướng khả dĩ (chỉ để tham
khảo, không phải chỉ định): trong vòng lặp trích `run`, bỏ qua step khi
`str(step.get("if", "")).strip().lower() in ("false", "${{ false }}")`, và bỏ qua toàn bộ job khi
`str(job.get("if", "")).strip().lower()` cùng tập giá trị đó trước khi duyệt `steps`. Ước tính quy mô:
~4-6 dòng, nằm vừa trong biên ngân sách còn lại (240 trần − 230 đã dùng = 10 dòng).

ĐÃ THỬ NGHIỆM: script `probe2.py` (lưu tại
`/tmp/claude-0/-home-user-rv361/c00529d1-2392-55f7-af9b-618c465f4a50/scratchpad/r2_361/probe2.py`,
có thể dựng lại từ nội dung BẰNG CHỨNG ở trên), chạy trực tiếp bằng `python3`, output như trên.

ĐỘ TIN: cao — đo trực tiếp trên đúng module đang review (`7116d6c`), không suy diễn, có ca đối chứng
(step bình thường) để loại trừ khả năng bug nằm ở chính script probe.

## finding-03-danh-sach-han-che-khong-quyet-duoc-tinh-nen-khong-vao-cung-nhom  [P2]  Nợ có tên: biểu thức `if:` không phải literal, và dead-code cấp shell bên trong `run:`, vẫn LỌT — nhưng KHÔNG quyết định được tĩnh nên không cùng mức với finding-02

TỆP/DÒNG: cùng khối `kiem()` như trên.

VẤN ĐỀ: Ngoài `if: false` (finding-02, quyết định được tĩnh), tôi tự dựng thêm ba biến thể khác đều
LỌT: (a) `if:` mang một biểu thức GitHub Actions không phải literal `false` nhưng luôn sai về mặt
logic thực tế (`github.event_name == 'never-such-event'`); (b) một khối `run: |` có lệnh thật nằm
sau một điều kiện shell không bao giờ đúng (`if [ "$NEVER_SET_VAR" = "1" ]; then ...; fi`); (c) một
khối `run: |` có lệnh thật nằm SAU một `exit 0` (dead code cấp shell). Khác với `if: false`, cả ba ca
này đòi một trình đánh giá biểu thức GitHub Actions hoặc một trình thông dịch shell tĩnh — về nguyên
tắc KHÔNG giải quyết được đầy đủ bằng phân tích tĩnh (biểu thức có thể phụ thuộc ngữ cảnh runtime
thật; shell có thể rẽ nhánh theo bất kỳ điều gì). Đây là giới hạn CẤU TRÚC của cách tiếp cận "đọc
`run:` đã parse", không phải một lỗi có thể vá bằng vài dòng như finding-02.

BẰNG CHỨNG: script `probe3.py` (cùng thư mục scratchpad), ba ca `shell-if-unreachable`,
`shell-dead-code-after-exit` đều LỌT trên module thật; ca `step-if-always-false-expr` đã gộp bằng
chứng ở finding-02 (cùng lần chạy `probe2.py`).

ĐÃ THỬ VÁ: không.

ĐÃ THỬ NGHIỆM: `probe2.py`, `probe3.py` như trên, chạy trực tiếp, output đã trích.

ĐỘ TIN: cao cho SỰ TỒN TẠI của lỗ; vừa cho ĐỘ ƯU TIÊN (ranh giới "quyết định được tĩnh" vs "không"
là phán đoán của reviewer, không phải một vạch có sẵn trong doctrine kho).

## finding-04-write-text-goi-hai-lan-de-lai-dong-chet  [P2]  Nợ nhỏ, không ảnh hưởng hành vi: một khối trong `phan_chung()` ghi tệp hai lần, lần đầu là code chết

TỆP/DÒNG: `.claude/dev/ci_dang_ky_test.py:184-185`

VẤN ĐỀ:
```python
yml.write_text("jobs:\n  x:\n    steps:\n      - run: python .claude/dev/a_test.py\n", encoding="utf-8")
yml.write_text("jobs:\n  x:\n    steps:\n      # - run: python .claude/dev/a_test.py\n", encoding="utf-8")
```
Dòng đầu ghi một YAML có step thật, dòng sau ghi ĐÈ ngay bằng bản chỉ có chú thích — dòng đầu không
để lại tác dụng nào (không đọc file giữa hai lần ghi). Không sai hành vi (kết quả cuối cùng đúng ý:
kiểm ca "step thật đã biến thành chú thích"), nhưng đọc gây hiểu lầm là đang so sánh trước/sau — có
lẽ là tàn dư từ lúc soạn thử. Không phải lỗi tôi có thể dựng phản chứng cho "hành vi sai" vì hành vi
hiện tại đúng ý đồ của ca test.

ĐÃ THỬ VÁ: không.

ĐÃ THỬ NGHIỆM: đọc mã trực tiếp, không cần chạy.

ĐỘ TIN: cao (đọc mã trực tiếp, không suy diễn) — mức độ nghiêm trọng CHỦ Ý xếp thấp (dọn dẹp, không
phải đúng/sai).

## Trả lời trực tiếp các câu hỏi của brief

**Q1 (P1-01):** Đóng đúng kịch bản đã nêu (chú thích giả mạo), và đúng nghĩa là đọc CẤU TRÚC YAML
(`step.get("run")`) thay vì so chuỗi thô — một bước tiến thật, không phải đổi tên phép xấp xỉ. Nhưng
CHƯA đọc `if:`, nên nó vẫn là một phép xấp xỉ, chỉ hẹp hơn trước. Xem finding-02.

**Q2:** `if: false` **CÙNG HỌ** với P1-01 (cùng bệnh "có mặt tĩnh ≠ thi hành thật"), và tôi xếp **P1**
— lý do đầy đủ ở finding-02. Vá P1-01 mà để hở `if: false` nghĩa là đã thu hẹp bề mặt tấn công (không
còn xoá được TOÀN BỘ 7+12 mục bằng một chú thích ở bất kỳ đâu trong tệp) nhưng CHƯA đóng: vẫn xoá
được TỪNG MỤC một, chỉ cần đúng một dòng `if: false` ngay trên step thật của mục đó, vẫn trong write
set của chính packet, vẫn không cần giả mạo gì. Khác `finding-03`, đây là ca quyết định được tĩnh,
rẻ, và write set đã có sẵn mọi phần cần để vá — đó là lý do tôi không hạ xuống P2 dù được tự khai.

**Q3:** Có — biểu thức `if:` không-literal luôn-sai và dead-code shell (`if` không bao giờ đúng,
lệnh sau `exit`). Xem finding-03; xếp P2 vì không quyết định được tĩnh một cách tổng quát.

**Q4:** `MOI_TRUONG_CI` là nguồn DUY NHẤT — grep xác nhận không có bản chép thứ hai nằm ngoài cơ chế
kiểm; hai literal trong `CACH_LY` là DỮ LIỆU (đúng bản chất, phải literal) và bị đối chiếu với hằng
số đó. Phép kiểm bắt được **mọi** giá trị lệch (so `!=`, không phải so tiền tố/pattern), không chỉ ca
gõ nhầm — đã tự dựng một ca lệch một chữ và xác nhận đỏ đúng ở tầng cấu trúc.

**Q5:** Đúng. Tự vô hiệu nhánh `OPS_REVIEWS`, giữ nguyên luật 1 (GOC) → hai tệp lưu trữ rơi vào `la`
→ xác nhận cơ chế thật là nhánh `OPS_REVIEWS` chạy trước, đúng như đính chính của r5.

**Q6:** Đúng theo phép kiểm MỚI: `duyet-phan-chung.yml:62` gọi thật `duyet_danh_tinh_test.py`;
`kiem()` trên cây thật không báo lỗi cho mục này, `21/21` (đã kiểm bằng phép SET-DIFF nội tại của
`kiem()`, không chỉ so số lượng).

**Q7:** Neo 29 khớp CHÍNH XÁC với `git diff --numstat 8fe6dcd 7116d6c` (29 thêm / 3 xoá). Bản vá THẬT
dùng đúng 230/240 dòng trên toàn write set (biên còn lại 10, không phải 7 như lease ước tính trước
khi viết — số liệu SAU khi viết thấp hơn ước tính TRƯỚC khi viết, hướng lệch vô hại).

**Q8:** Không thấy dấu hiệu đáng ngờ. `git diff --stat` chỉ đổi đúng 2 tệp trong write set, không có
đổi mode/executable-bit, `git diff --check` sạch (không lỗi khoảng trắng), toàn bộ nội dung khớp mô
tả trong thông điệp commit — không có gì "thừa" ngoài phạm vi đã khai. Thông điệp commit của cả r4
lẫn r5 đều tự khai rõ "AI COMMIT" và ai đo — nhất quán, không có gì cần khai thêm mà bị bỏ sót mà tôi
tìm thấy. (Lưu ý: `.claude/dev/duyet_danh_tinh_test.py` — cổng xác thực danh tính khác của kho — kiểm
một vấn đề KHÁC hẳn, giả mạo tên reviewer trên GitHub, không liên quan tới việc executor/dispatcher
nào đứng tên `git commit --author`; không nhầm hai cơ chế.)

**Q9:** Có — finding-02 (P1, mới vì lượt 1 chưa từng thấy mã r5), finding-03 (P2, nợ mới), finding-04
(P2, nợ nhỏ). Không finding nào trùng slug với ba finding của lượt 1.

## Phản chứng bắt buộc — kết quả

- `python3 .claude/dev/ci_dang_ky_test.py`: `RC_DIRECT=0` (đo `$?` trần), `PHẢN CHỨNG: 13/13 đỏ đúng`,
  `TỔNG: ĐẠT`.
- `python3 .claude/dev/ci_dang_ky_test.py --chay`: xem phần cập nhật cuối tệp này (đang chạy tiền
  cảnh lúc soạn verdict; ghi bổ sung ngay khi có kết quả, không đoán trước).
- `git diff --numstat 58b85cc2 7116d6c -- .github/workflows/ci.yml .claude/dev/ci_dang_ky_test.py`:
  `226 + 4 = 230` / trần 240.
- Mỗi chốt r5 (khoá `moi_truong`, parse YAML `run:`) đã tự phá trên bản sao ngoài cây (script
  `probe1.py`..`probe4.py` dưới scratchpad) và xác nhận đỏ đúng lý do đã tuyên, không lý do khác đi
  ngang qua — chi tiết trong BẰNG CHỨNG của từng finding và BẢNG ĐO.
- `doctrine-scan --root .`: sạch, rc=0.
- `git diff --check`: sạch, rc=0.

## Khi không đo được

- Gate GitHub Actions (trạng thái check thật trên PR #370): **KHÔNG ĐO ĐƯỢC** trong phiên này —
  không có `gh`; `curl` thẳng tới `api.github.com/repos/ducthangho/tra-luat/...` trả `403` không kèm
  header GitHub nào (chặn ở tầng proxy/tổ chức, không phải GitHub từ chối token). Không suy ra màu.
- `ops/nhanh_don_duoc_test.py`: chưa tự đo riêng trong lượt này ngoài kết quả nằm trong `--chay`
  (xem cập nhật cuối tệp) — môi trường của tôi khác cả hai môi trường brief nhắc tới; sẽ khai đúng
  môi trường quan sát được, không suy ra ĐẠT/ĐỎ từ môi trường khác.
