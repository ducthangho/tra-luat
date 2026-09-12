verdict: approve
reviewed_sha: 745d8889d0d6468785f26003876ba823c8b2db99
base_da_review_truoc: 922956a7048fd23eea1c9f88aeb986e076f10e24
so_lan_luot_nay_bi_chet_va_phong_lai: 0

**Approve tại SHA trên: 0 P1 · 0 P2 · 1 P3 còn mở.** Đính chính t33 đúng; phân loại bằng chứng đã cải thiện thực chất nhưng chưa nhất quán toàn README. Không phát hiện lỗi hash, mất mục manifest hoặc hồi quy mã chạy do diff hai tệp này. Approval này không biến full-gate lịch sử thành xanh và không cấp quyền merge.

Reviewer: Codex / OpenAI, phiên API có shell cục bộ; executor Claude theo chỉ thị chủ kho. Launcher giao kèm `run-1/7c972490/run.json` ghi `openai_codex / codex_cli / machine`, đúng head, đang chạy; đây là lời ghi của launcher, không phải chứng thực độc lập model. `nhat-ky.txt` có một lần khởi động; không có lần chết/phóng lại trong phiên này.

Review Class của **delta lượt này**: routine, chỉ sửa prose và hash prose. Authority/phạm vi: chỉ thị trực tiếp của chủ kho trong lượt 15; không tự tạo lease, spec hash hoặc generation. Checkout chỉ đọc. Mọi đường `ops/...` dưới đây tính từ `cay-kho/`; phép đo và đầu ra mới ở `do-review15/`, bên ngoài checkout. Kết luận được ghi ngay sau khi có số đo; kiểm cuối bổ sung bên dưới.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `full-gate-t33-nham-that-bai-voi-khong-chay`: **ĐÃ VÁ THẬT** — cả `nen.lease.norm.out:48` và `sau.lease.norm.out:48` ghi `ĐỎ t33_workflow_dang_lease_phai_qua_actionlint` kèm lỗi thiếu actionlint; dòng 50 của cả hai ghi `120/121 đạt; đã chạy=121, bỏ qua=0`. README:76–86 nay diễn đạt đúng: hàm đã chạy, thất bại ở tiền điều kiện; lệnh lint chưa được gọi. Đọc điều khiển luồng ở `ops/lease_publish_test.py:1337` và `:4042`: assert thiếu tool nằm trước subprocess; main bắt AssertionError vào `hong` và trả 1. Không cần chạy lại hàm để đóng lỗi văn bản này.
- `evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu`: **VÁ HỜ — chưa đóng đủ, dù có cải thiện thực chất**. Bảng mới README:15–25 khớp phép đo **1/6 bộ**, tức **2/12 giá trị hai vế**; DELTA:59–63 đã giới hạn đúng bốn cặp tệp lưu. Nhưng bảng vẫn có hiệu lực ngay bên dưới, README:32–34, còn gọi cả rc, stdout gốc và giây là **“đo lại được”**, vẫn viện dẫn `fullgate.sh` không có trong gói và “nhiễu ±5 s” không có timestamp để kiểm. Chưa bổ sung cách trích **danh sách khẳng định**, tiêu chí chọn/bỏ sót và tuyên bố mục bỏ sót reviewer tìm ra vẫn tính finding theo PROTOCOL §8. Giữ nguyên slug/P3, không tách thành finding mới.

## BẢNG ĐO

| khẳng định | hồ sơ khai | tôi đo được | khớp? |
|---|---|---|---|
| HEAD / tree / trạng thái | detached 745d888, sạch | HEAD `745d8889d0d6468785f26003876ba823c8b2db99`; tree `4cb6cbb6ca930c6f485e82b333db78d5a2efab8b`; symbolic-ref rc=1; porcelain rỗng | có |
| refs/heads | 306, dựng có chủ ý | 306; không thay ref | có tại snapshot local |
| Delta từ lượt 14 | hai tệp, văn bản + manifest | đúng README + ARTIFACTS full-gate; README +34/−5, manifest +1/−1; patch và numstat giao kèm bằng byte Git diff; `git diff --check` rc=0 | có |
| t33 lịch sử | đã chạy, đỏ ở tiền điều kiện | hai norm cùng lỗi thiếu actionlint ở dòng 48; tổng 120/121, đã chạy=121, bỏ qua=0 ở dòng 50; hai rc ghi lease=1 | có |
| Phần chưa chạy | thao tác lint workflow bên trong t33 | assert thiếu tool chặn trước subprocess; main tính AssertionError là hỏng | có qua log + mã nguồn; không thực thi t33 lượt này |
| cidk | stdout gốc 2934 B; chỉ giữ tail 206 B | hai tail 206/206 B, 5/5 dòng, bằng byte | có về tail; không tự đếm được 2934 B lịch sử |
| ploop | stdout gốc 8752 B; tail 96 B | hai tail 96/96 B, 5/5 dòng, bằng byte | có về tail; không tự đếm được 8752 B lịch sử |
| lease | stdout gốc 8971 B; norm 8827 B | hai norm 8827/8827 B, 50/50 dòng, bằng byte; mỗi bản 31 dòng đột biến, 0 marker `ĐỎ=[]` | có về norm; không tự đếm được 8971 B lịch sử |
| doc-claims | nguyên stdout 70861 B | hai JSON hợp lệ, 70861/70861 B, 2708/2708 dòng, bằng byte | có từ hiện vật |
| doctrine-scan / adr-song | không giữ stdout; 69/113 B | không có stdout hai bộ trong gói full-gate; chỉ có số trong nen.rc/sau.rc | có về giới hạn; không lấy output các lượt review khác thay lịch sử này |
| Tỷ lệ tự đếm kích thước stdout gốc | 1/6 | chỉ doc-claims có nguyên liệu nguyên vẹn: **1/6 bộ, 2/12 giá trị** | có |
| 12 rc | chỉ log tổng hợp | đọc 12/12 trường: mỗi vế năm rc0, lease rc1; không có launcher/script của lần gate để xác thực độc lập mã thoát lịch sử | bảng mới đúng; bảng cũ :32 còn mâu thuẫn |
| Giây | cidk 0/1; ploop 207/205; lease 58/63 | đúng sáu trường đã ghi; không có timestamp đầu/cuối; không kiểm được sai số ±5 s | bảng mới đúng; bảng cũ :34 còn quá mạnh |
| DELTA=0 | byte chỉ trên bốn cặp lưu | **4/4 cặp bằng byte**; hai bộ thiếu stdout chỉ khớp rc và kích thước ghi sẵn | đúng với phạm vi mới |
| Không bộ nào out=0B | phép kiểm output | **12/12 trường out >0**; 8/8 tệp tail/norm/JSON đang lưu >0 | khớp log tổng hợp; không chứng minh độc lập sáu stdout lịch sử |
| Hash README full-gate | một dòng lập lại | SHA-256 `d276c2c28ec1b6dcce685043220ca2faa40da614bb95a0cfde303712d3ac377a`; 11 dòng còn lại và tập đường dẫn giữ nguyên | có |
| Manifest full-gate / bao phủ | còn nguyên và phủ đủ | **12/12, rc=0**, 12 đích duy nhất; thư mục có 13 tệp, chỉ ARTIFACTS nằm ngoài danh sách của chính nó | có; không rơi tệp |
| Tất cả manifest review | cần kiểm theo ánh xạ sandbox | **12 ARTIFACTS, 967/967 mục, cả 12 rc=0**; bảng từng gói bên dưới | có; không phải 967 tệp độc lập |
| Băm prompt phụ gói 13 | bundle-PROMPT.sha256 | digest đơn `e60c376ab385ccc9b3cc8d2cdd87620b2110c8a68e607c879a6100c6b3f9958c` bằng SHA-256 bundle-PROMPT.md | có, 1/1; đây không phải manifest cú pháp sha256sum -c |

## MANIFEST THEO ÁNH XẠ VÀ PHẦN NGOÀI PHẠM VI BĂM

**Tất cả 12 ARTIFACTS đạt rc=0 khi giải đúng đường dẫn.** Gói 11/12/13 ghi layout sandbox, không ghi layout kho. Đọc từng `DOC-MANIFEST.md`: `VERDICT.md` ánh xạ sang verdict anh em của đúng lượt; tiền tố `do-review10/`, `do-review12/`, `do-review13/` ánh xạ vào thư mục gói tương ứng. Bản lồng `manifest11-layout/` đã giữ layout sandbox nên không áp thêm ánh xạ gói 11 vào đó. Những manifest còn lại tính từ thư mục chứa chúng.

Phép đo giữ nguyên digest và thứ tự từng dòng, chỉ viết danh sách đường dẫn đã giải vào scratch rồi chạy `sha256sum -c do-review15/manifest-NN.mapped.sha256` từ gốc sandbox. Không sửa manifest hoặc dựng symlink trong checkout. Lệnh, stdout, stderr và danh sách ngoài phạm vi băm ở `do-review15/manifests.json` cùng các tệp `manifest-*.stdout/.stderr/.mapped.sha256`.

Đường dưới tính từ `ops/reviews/`, mỗi hàng là `ARTIFACTS.sha256` trong thư mục đó:

| gói / thư mục | đạt / mục | rc |
|---|---:|---:|
| `full-gate-pr468-20260907` | 12/12 | 0 |
| `pr468-hoso-4-packet-review-10-codex/goi-y/cay/ops/reviews/pr468-hoso-4-packet-review-9-codex/artifact-repair` | 69/69 | 0 |
| `pr468-hoso-4-packet-review-11-codex` | 128/128 | 0 |
| `pr468-hoso-4-packet-review-11-codex/artifact9-repair` | 69/69 | 0 |
| `pr468-hoso-4-packet-review-12-codex` | 178/178 | 0 |
| `pr468-hoso-4-packet-review-12-codex/manifest11-layout` | 128/128 | 0 |
| `pr468-hoso-4-packet-review-12-codex/manifest11-layout/do-review10/artifact9-repair` | 69/69 | 0 |
| `pr468-hoso-4-packet-review-13-codex` | 48/48 | 0 |
| `pr468-hoso-4-packet-review-6-codex` | 62/62 | 0 |
| `pr468-hoso-4-packet-review-7-codex` | 66/66 | 0 |
| `pr468-hoso-4-packet-review-8-codex` | 69/69 | 0 |
| `pr468-hoso-4-packet-review-9-codex/artifact-repair` | 69/69 | 0 |

Hash pass không đồng nghĩa băm mọi tệp trong mọi thư mục. Ngoài bản thân từng ARTIFACTS, các phần không được **manifest tại chính gói đó** băm là:

- Gói 6: 12 tệp — `d2-ci-results.json`, `d2-that-results.json`, 7 tệp `nen-a1-a5/`, 3 tệp `outputs-that/` (tên đầy đủ trong JSON).
- Gói 8: `verdict-format-check.json`.
- Gói gợi ý artifact-repair nằm trong gói 10: `README.md`.
- Gói 11 và 12: `DOC-MANIFEST.md`.
- Gói 13: `DOC-MANIFEST.md` và sáu `bundle-*`: `bundle-EVIDENCE.md`, `bundle-PROMPT.md`, `bundle-PROMPT.sha256`, `bundle-ai-dang-giu-readback.txt`, `bundle-ls-remote-heads.txt`, `bundle-ref-coverage.txt`. Thư mục có **55 tệp = 47 đích nội bộ được băm + 8 ngoài manifest**; verdict anh em là mục thứ 48 được băm. Băm prompt phụ 1/1 không biến sáu bundle thành phạm vi của ARTIFACTS.

Đây là phạm vi bao phủ đã tồn tại từ nền; diff lần này không đổi các gói ấy. Riêng gói full-gate đang sửa **không thiếu tệp nào ngoài bản thân manifest**. Không báo lỗi hash chỉ vì chạy sai cwd; cũng không suy 967/967 thành bao phủ toàn bộ `ops/reviews/**`.

## KIỂM LỜI KHAI SAU VÁ

Mục ĐÍNH CHÍNH không mâu thuẫn phần còn lại về t33: tiêu đề vẫn ghi lease rc1, không tính xanh; câu cũ nằm trong trích dẫn được đánh dấu **sai**, không còn là lời khẳng định hiện hành. Bản vá không sửa log, rc hay kết quả 120/121 thành 121/121.

README hiện chỉ có hai chỗ nhắc DELTA, đều nằm trong đoạn :59–63. Không còn câu khẳng định toàn sáu stdout “khác duy nhất số giây và tên temp”; hai bộ thiếu output được giới hạn rõ vào trường rc/kích thước. Trong phạm vi README hiện hành, không thấy lời DELTA khác rộng hơn. Các verdict/hiện vật review lịch sử không bị sửa và không được coi là lời khai mới tại head này.

Các số mới thêm đều khớp hiện vật; không thấy bản vá làm sai lời khai trước đó đang đúng. Phần chưa nhất quán là **hai bảng loại nguồn**: phần mở đầu bác nhãn “đo lại được”, nhưng :32–34 vẫn giữ nguyên nhãn đó như nội dung hiện hành. :28 nói “áp cho phần đọc lại được” không đủ giải quyết, vì chính :32 vẫn chỉ cách chạy một script không được giao và :34 vẫn khai sai số thời gian chưa có nguyên liệu kiểm. Câu :42 “muốn đối chiếu byte gốc phải chạy lại” cũng cần làm rõ: lần chạy mới cho log mới, không khôi phục byte lịch sử đã mất. Gộp toàn bộ vào P3 cũ dưới đây.

### evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu  [P3]  Bảng cũ vẫn nâng log tổng hợp thành số đo tái lập được

TỆP/DÒNG: `ops/reviews/full-gate-pr468-20260907/README.md:28`, trọng tâm :32–34; giới hạn :39–46; đối chứng bảng mới :15–25 và `docs/PROTOCOL_DA_PHIEN.md:569`.

VẤN ĐỀ: bảng mới đúng nhưng bảng cũ chưa được đồng bộ, nên người đọc vẫn có thể lấy rc/out/giây làm bằng chứng đo lại. `fullgate.sh` không có trong inventory gói full-gate và `git ls-files '*fullgate.sh'` rỗng. Không thể xác thực 5/6 kích thước stdout gốc, 12 mã thoát lịch sử hoặc ±5 s bằng các hiện vật đang giao. Phần còn thiếu theo §8 vẫn là cách trích **danh sách khẳng định** và giới hạn của cách chọn đó, không chỉ cách đọc từng số. Mức P3: giới hạn 1/6, lease rc1, phạm vi DELTA và không cấp quyền merge đều đã công khai; chưa thấy gate hoặc authority bị nới.

ĐÃ THỬ VÁ: chưa áp thay đổi vào checkout. Đã xác định hướng sửa tối thiểu từ hiện vật: thay đúng ba dòng loại nguồn rc/out/giây; giữ các dòng marker/tail/norm tự đếm được; bỏ sai số ±5 s chưa có căn cứ; sửa giới hạn raw lịch sử; bổ sung cách lập danh sách khẳng định và câu mục bỏ sót vẫn tính finding. Không cần sửa log hoặc tái chạy full-suite.

GÓI VÁ: gợi ý văn bản, nhãn **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Thay ba hàng bằng:

```text
| `rc` từng bộ | đọc trường thứ 2 của `nen.rc` / `sau.rc` | chỉ đọc log tổng hợp; không có launcher để xác thực độc lập mã thoát lịch sử |
| `out_byte` | đọc số ghi trong `*.rc`; đếm byte `*.doc-claims.json` đang lưu | chỉ doc-claims tự đếm lại được kích thước stdout gốc; tail/norm không thay stdout gốc |
| số giây | đọc các trường `giay=` trong `*.rc` | chỉ đọc log tổng hợp; không có timestamp để kiểm thời lượng hoặc sai số |
```

Với raw lease, ghi: “Bản thô không được kèm; không khôi phục được byte lịch sử từ bản chuẩn hoá. Chạy lại chỉ tạo phép đo mới.” Executor cần thực sự lập inventory khẳng định của toàn README, gồm cả chữ và số, giữ script/lệnh đã dùng cùng kết quả, khai tiêu chí và phần có thể bỏ sót; ghi tường minh “Mỗi mục danh sách bỏ sót mà reviewer tìm ra vẫn tính là finding”. Không tự nhận một script đã chạy khi chưa chạy. Sau sửa README, chỉ cập nhật hash README trong ARTIFACTS full-gate; giữ 11 mục khác.

ĐÃ THỬ NGHIỆM: `python3 -B do-review15/audit.py` **rc=0**, tự đếm byte/dòng/marker, so byte 4 cặp, đọc 12 rc và kiểm 12 manifest bằng sha256sum thật. Không chạy test suite; gợi ý prose trên chưa được áp thử. Phép kiểm chấp nhận sau khi executor sửa: đối chiếu hai bảng với cùng inventory, xác nhận không còn coi rc/out/giây lịch sử là tự đo được, số 1/6 và 4 cặp vẫn đúng, rồi `sha256sum -c ARTIFACTS.sha256` phải đạt 12/12. Rủi ro của gợi ý: sửa quá tay thành “mọi số đều không đo được”, làm mất các marker/byte hiện vật thực sự đếm được; hoặc gọi số của lần chạy mới là bằng chứng lịch sử. Giữ rõ từng loại nguồn để tránh hai lỗi này.

ĐỘ TIN: cao về byte, phạm vi và mâu thuẫn văn bản; không kết luận số lịch sử bị ghi sai.

## GIỚI HẠN LƯỢT NÀY

Không chạy bộ test dài, CI, cấp lease, đăng Issue/PR, merge, sửa kho thật hoặc nâng timeout. Không cần chạy các cổng ngắn không quét prose này để chứng minh một bản sửa văn bản. Gate/CI và môi trường thực thi full-gate lịch sử: **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)**. Phép đo 1/6 chứng minh tính sẵn có của nguyên liệu trong gói; không chứng minh launcher lịch sử thực sự xuất chúng từ đúng lệnh/cây được khai. Thời lượng, số attempt full-gate lịch sử và trạng thái máy chủ hiện tại không được xác thực bằng review offline này.

## KIỂM CUỐI

Kiểm cuối **2026-09-07T22:51:02.391708+00:00**: HEAD và tree giữ nguyên; detached; `git status --porcelain --untracked-files=all` rỗng, rc=0; diff worktree/index rỗng, rc=0; **306 refs/heads cùng tên và OID như đầu lượt**, 0 commit mới. Chi tiết ở `do-review15/final-check.json`. Không có lần chết/phóng lại.

`do-review15/ARTIFACTS.sha256` băm VERDICT.md và toàn bộ script/kết quả đo của lượt này, trừ chính manifest; đường dẫn tính từ gốc sandbox. Kiểm bằng `sha256sum -c do-review15/ARTIFACTS.sha256`. Manifest đầu vào và checkout được giữ nguyên.
