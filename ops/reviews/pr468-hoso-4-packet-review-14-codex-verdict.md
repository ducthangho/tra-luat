verdict: approve
reviewed_sha: 922956a7048fd23eea1c9f88aeb986e076f10e24
base_da_review_truoc: f77f19895e00835d71644d82f1c54e9b519ccfe6
so_lan_luot_nay_bi_chet_va_phong_lai: 0

**Approve cho hồ sơ PR #468 tại exact SHA trên: 0 P1 · 0 P2 · 2 P3.** Không thấy hỏng manifest hoặc hồi quy workflow. P3 lượt 13 chỉ được vá một phần; bản ghi full-gate còn phân loại nguồn quá mạnh và mô tả sai trạng thái ca t33. Không coi DELTA=0 là full-gate xanh hay là quyền merge.

Reviewer: Codex / OpenAI, phiên API có shell cục bộ, độc lập với executor Claude. Đầu ra chỉ trong sandbox; checkout `cay-kho/` được giữ read-only. Không dùng mạng, không gọi CI, không chạy bộ test dài. Hai lần gọi riêng hàm t33 (âm/dương) không phải hai lượt chạy lại suite. Chưa có lần chết/phóng lại trong lượt này; `run-1/229ddb14/run.json` là launcher của **lượt 14**, không phải nguồn chứng minh lượt 13.

Các đường `ops/...` dưới đây tính từ `cay-kho/`. Bằng chứng mới ở `do-review14/`. Bản kết luận được ghi ngay khi có kết quả, rồi bổ sung gói gợi ý và kiểm cuối trong cùng phiên.

## ĐỐI CHIẾU LƯỢT TRƯỚC

`evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu` [P3]: **CHƯA VÁ ĐỦ, đã cải thiện thực chất**. README full-gate có bảng CÁCH TRÍCH SỐ và bốn giới hạn cụ thể: chuẩn hoá lease/mất bản thô, tail 5 dòng, không lưu nội dung hai cổng, không phủ CI. Tuy nhiên cả cột loại nguồn đều là “đo lại được”; `fullgate.sh` không có trong gói; số giây không có timestamp đầu/cuối; 5/6 kích thước stdout gốc không thể tự đếm từ tệp đã giao. Chưa có phương pháp trích **danh sách khẳng định**, hoặc câu theo §8 rằng mục bỏ sót do reviewer tìm ra vẫn tính finding. Đây vẫn là nợ P3, không tự nâng thành P1 vì cây Git và các phép đo ngắn đều dùng được.

## BẢNG ĐO

| khẳng định | hồ sơ khai | tôi đo được | khớp? |
|---|---|---|---|
| HEAD / trạng thái | detached 922956a, sạch | `922956a7048fd23eea1c9f88aeb986e076f10e24`; tree `304c9a094c8cf54880a2e6efee6f0507bea69c6a`; symbolic-ref rc=1; porcelain rỗng | có |
| Snapshot refs/heads | 306, dựng có chủ ý | 306; giữ nguyên, không dọn ref | có về cây local |
| Diff f77f198 → 922956a | 72 tệp thuần ops | 72 tệp, +15834/−0; 0 path ngoài ops; patch và numstat bằng byte bản giao | có |
| “Không một dòng mã chạy được” | không có code | Có 6 tệp `.py`, tổng 571 dòng, cả 6 parse AST được; đều là script hiện vật review. Không đổi mã sản phẩm/CI/gate đang sống | không đúng theo nghĩa đen; phạm vi hồ sơ đúng |
| Hai dòng bổ sung mục lục/ghi nhận | hai chỗ | README thêm 1 dòng; GHI-NHAN thêm 12 dòng; cả hai thuật lại đúng approve lịch sử f77f198 | hai tệp/chỗ, không phải tổng hai dòng |
| Neo full-gate | nền b416830, sau f77f198 | `neo.txt` ghi đủ hai OID; các object tồn tại. Không có launcher/command/timestamp đầy đủ để xác thực cây thực tế của lần chạy lịch sử | khớp lời ghi; lịch sử chưa xác thực |
| cidk | rc 0/0, stdout 2934 B | `*.rc` ghi đúng; chỉ còn tail **206/206 B, 5/5 dòng**, bằng byte; có `51/51 đỏ đúng` và `TỔNG: ĐẠT` | marker/tail có; 2934 B chỉ là số ghi trong rc |
| ploop | rc 0/0, stdout 8752 B | `*.rc` ghi đúng; tail **96/96 B, 5/5 dòng**, bằng byte; có `TỔNG: ĐẠT` | marker/tail có; 8752 B chưa tự đếm được |
| lease | rc **1/1**, stdout 8971 B | `*.rc` ghi đúng; bản norm **8827/8827 B, 50/50 dòng**, bằng byte; raw không có | rc phù hợp log failed; 8971 B chưa tự đếm được |
| lease đột biến | 31; không có ĐỎ=[] | đếm **31** dòng chứa `đột biến`, **0** dòng chứa `ĐỎ=[]` trên từng bản norm | có; đây là đếm marker, không tái chạy mutation |
| lease kết quả | không tính xanh; t33 thiếu actionlint | một dòng thất bại t33; tổng **120/121 đạt; đã chạy=121, bỏ qua=0** | đúng fail-close; mâu thuẫn câu t33 “không đỏ/không chạy” |
| doctrine-scan | rc 0/0; 69 B | bản lịch sử chỉ giữ rc/size; lượt này tự chạy rc=0, **69 B**, quét 7 tệp, 0 chép doctrine | khớp phép đo mới, không hồi tố lịch sử |
| adr-song | rc 0/0; 113 B | bản lịch sử chỉ giữ rc/size; lượt này rc=0, **113 B**, 46 ADR/46 dòng, ngoại lệ trạng thái 0016 | khớp phép đo mới, không hồi tố lịch sử |
| doc-claims-check | rc 0/0; 70861 B | hai JSON **70861/70861 B**, 2708/2708 dòng, bằng byte; ok=true, 106 tệp, 367 advisory, 0 flags, 10 lớp, 0 lớp bỏ qua | có từ hiện vật; rc là bản ghi, phù hợp nội dung |
| Số stdout gốc tự đếm được | cả 6 “đo lại được” | **1/6 bộ** (doc-claims), tức **2/12 giá trị hai vế**; năm bộ còn lại thiếu stdout nguyên bản | chưa phân loại đúng |
| rc lịch sử | 12 số của 6 bộ | đọc lại được **12/12 số trong *.rc**; không có log launcher để độc lập đo lại mã thoát đã xảy ra | nhất quán nội bộ, không phải 12 phép thực thi mới |
| Giây | cidk 0/1; ploop 207/205; lease 58/63 | chỉ có các giá trị này trong rc; không có mốc `date +%s` gốc hoặc script | KHÔNG ĐO ĐƯỢC lịch sử; ±5 s không có phương pháp chứng minh |
| DELTA=0 | chỉ khác giây/temp | **4/4 cặp tệp lưu stdout/tail/norm bằng byte**; rc/out ghi trong hai rc giống nhau; giây khác. Không so được stdout gốc của cả 6 bộ | đúng cho bản chiếu giữ lại; rộng hơn thế chưa chứng minh |
| Không bộ nào out=0B | kiểm chống xanh giả | **12/12 trường out >0**; bốn bộ có hiện vật stdout/tail/norm đều >0; hai bộ không giữ output lịch sử | đúng với bảng rc; chưa chứng minh độc lập cả sáu stdout gốc |
| t33 trên cây hiện tại | lịch sử thiếu actionlint | gọi đúng hàm: PATH thiếu tool → AssertionError đúng thông báo; thêm actionlint 1.7.7 có sẵn → **passed**, khoảng 0,060 s | xác nhận cơ chế và lint hiện tại; không đổi lịch sử |
| Hồi quy t33 | không do PR | blob test và ops-publish-lease.yml bằng nhau tại b416830, f77f198, 922956a; phép gọi t33 hiện tại đạt | có căn cứ, chưa thấy lỗi bị che |
| “Full-gate một lần” | lần duy nhất, đồng thời kể một lần wrapper rc127 trước đó | không có run ledger/fullgate.sh/raw lần rc127 để kiểm số lần; hiểu được là một lần sáu bộ thực sự chạy, sau một lần launcher không khởi động được chúng | KHÔNG ĐO ĐƯỢC số attempt lịch sử |
| Manifest lượt 13 | 48/48 | **48/48, rc=0**, 48 đích duy nhất, không symlink | có |
| Manifest full-gate | 12/12 | **12/12, rc=0**; ngoài manifest chỉ bản thân ARTIFACTS | có |
| Tất cả ARTIFACTS trong ops/reviews | đều nguyên vẹn theo ánh xạ | **12 manifest, 967/967 mục kiểm, tất cả rc=0**; có bản sao lặp, không phải 967 tệp độc lập | có |
| Gói 13 ngoài manifest | reviewer 48 + bundle đầu vào | thư mục có **55 tệp = 47 hiện vật được băm + 6 bundle-* + ARTIFACTS + DOC-MANIFEST**; verdict là mục thứ 48 nằm ngoài thư mục | có phần ngoài manifest, không phải thiếu 8 hash đã cam kết |
| verdict_sha256 lượt 13 | 3a89739f… | `3a89739f471046ec447271ac993e580413bcceaf34e216030fa946cb363f70e6` | có |
| verdict_bytes lượt 13 | 19313 | **19313 B**; bằng byte VERDICT-luot13.md giao ở gốc sandbox | có |
| reviewed_sha lượt 13 | f77f19895… | receipt và verdict cùng `f77f19895e00835d71644d82f1c54e9b519ccfe6` | có; không phải approval head mới |
| Neo receipt13 | commit đầu chứa verdict babab322… | đúng `babab322fe4022cac54adb2f1f531e995e41c4da`; blob bằng byte; reviewed_sha là tổ tiên, rc=0 | có bằng Git local |
| prompt_sha256 lượt 13 | e60c376a… | `e60c376ab385ccc9b3cc8d2cdd87620b2110c8a68e607c879a6100c6b3f9958c`; bằng bundle-PROMPT.sha256 và receipt | có về byte prompt, không chứng minh launcher dùng nó |
| thoi_luong_giay / ma_thoat lượt 13 | 1035.206 / 0 | YAML có các giá trị đó; không có run.json d7edf347 để đối chiếu. Làm tròn 1035.2/1035 đúng | KHÔNG ĐO ĐƯỢC độc lập |
| so_lan_chet_truoc_khi_xong lượt 13 | yêu cầu đề cập trường này; prose “ngay lần đầu” | **trường không tồn tại** ở receipt; prose hàm ý 0, nhưng không có launcher ledger lượt 13 | KHÔNG ĐO ĐƯỢC; không lấy run lượt 14 thay thế |
| model_bang_chung lượt 13 | yêu cầu mô tả là “KHÔNG ĐO ĐƯỢC” | tệp thật ghi **model gpt-6-astra 6/6 mục session**, không có nhãn đó cho lượt 13; KHONG_do_duoc chỉ nói attestation lượt 11/12 | tiền đề yêu cầu sai; lời khai model mạnh hơn bằng chứng giao |
| Model/thread/stdout lượt 13 | gpt-6-astra, thread 01a07da0…, stdout486735 B | không có session JSONL hoặc stdout launcher; chỉ có lời khai trong receipt | KHÔNG ĐO ĐƯỢC độc lập, không khẳng định lời khai là bịa |
| Cổng ngắn lượt 14 | không thay full-suite | doctrine rc0, ADR rc0, doc-claims rc0; doc-claims mới **70854 B**, 106 tệp/367 advisory/0 flags | passed tại HEAD hiện tại; không coi là tái tạo byte lần gate cũ |
| Gate còn lại / CI / máy lịch sử | chủ kho cấm bộ dài và CI | không chạy cidk, ploop, lease suite hoặc CI | **KHÔNG ĐO ĐƯỢC ở lượt này (ràng buộc chủ kho)** |

## TOÀN VẸN MANIFEST VÀ PHẦN NGOÀI MANIFEST

Dùng đúng `DOC-MANIFEST.md`: ở gói 11, `VERDICT.md` → verdict anh em, `do-review10/` → thư mục gói 11; ở gói 12/13 tương tự với `do-review12/`/`do-review13/`. Bản lồng `manifest11-layout/` đã giữ layout sandbox nên kiểm trực tiếp từ đó. Các manifest còn lại tính từ thư mục chứa chúng. Bộ đo giữ nguyên hash, chỉ giải đường dẫn sang tệp thật rồi gọi `sha256sum -c` trên danh sách ánh xạ đặt trong scratch; không sửa manifest/checkout.

Đường dưới tính từ `ops/reviews/`; mọi dòng là `ARTIFACTS.sha256` ở thư mục tương ứng:

| gói/thư mục | kết quả | rc |
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

Ở snapshot này chỉ **3** manifest đầu gói (11/12/13) cho `0/N` nếu cố chạy ngay tại thư mục manifest, do sai cwd/layout. Không đo lại được sự kiện executor từng thấy **4** gói như mô tả; bản lồng manifest11-layout hiện đã kiểm trực tiếp được 128/128. Không dùng lỗi bố trí của người kiểm để kết luận kho hỏng.

DOC-MANIFEST lượt 13 **đủ ánh xạ cho toàn bộ 48 mục manifest**; không có đích mơ hồ hoặc thiếu. Sáu `bundle-*` đều được đoạn cuối mô tả như đầu vào, nhưng chưa nói tường minh chúng **không được ARTIFACTS của reviewer băm**. Chúng là: `bundle-EVIDENCE.md`, `bundle-PROMPT.md`, `bundle-PROMPT.sha256`, `bundle-ai-dang-giu-readback.txt`, `bundle-ls-remote-heads.txt`, `bundle-ref-coverage.txt`. DOC-MANIFEST và bản thân ARTIFACTS cũng ở ngoài 48 mục. Biên nhận nằm ngoài thư mục gói và ngoài manifest reviewer; verdict nằm ngoài thư mục nhưng **có** trong manifest. Không suy 48/48 thành toàn bộ 55 tệp đã được manifest bao phủ.

Phạm vi cũ cũng có tệp ngoài manifest: gói 6 có 12 hiện vật bổ sung ngoài manifest (hai `d2-*.json`, bảy tệp `nen-a1-a5/`, ba `outputs-that/`); gói 8 có `verdict-format-check.json`; bản gợi ý artifact-repair trong gói 10 có `README.md`; gói 11/12 có `DOC-MANIFEST.md`. Các gói còn lại chỉ trừ bản thân ARTIFACTS. Danh sách đầy đủ đã đếm ở `do-review14/manifests.json`. Đây là khác biệt **bao phủ**, không phải hash mismatch hoặc finding mới về byte lịch sử.

## ĐÁNH GIÁ BẰNG CHỨNG FULL-GATE

Chuẩn hoá không làm phép so vô giá trị: nó chứng minh **hai bản chuẩn hoá đang được giao** bằng nhau, kể cả dòng t33 thất bại, tổng 120/121 và 31 dòng đột biến. Tuy nhiên phép `s/lp_[a-z0-9_]+/LP/g` không khả nghịch và áp toàn văn, không riêng trường thư mục. Phản chứng ngắn của reviewer: `error=lp_bad_permission` và `error=lp_no_permission` cùng thành `error=LP`. Đây là giới hạn của phép chiếu, không phải bằng chứng log này thực sự có hai lỗi đó. Thiếu raw thì không chứng minh được câu mạnh “khác duy nhất tên temp”, cũng không tái tạo byte gốc bằng chạy lại (temp/thời gian mới). Nên giữ kết luận DELTA cho phần lưu được.

Tail 5 dòng là thiếu độ phủ chẩn đoán, nhưng chưa thấy nó che lỗi thật trong diff này. `ci_dang_ky_test.py:537` thu lỗi vào `loi`, dòng 542–545 kết hợp vào `ok` rồi in tổng và trả rc; `packet_loop_test.py:4728` in tổng từ `that_bai_tong`, trả 1 khi có thất bại. Hai tail giữ marker tổng nên có bằng chứng dương hữu ích nếu rc/command lịch sử đúng. Dòng lỗi/warning giữa stdout hoặc lỗi không được harness tính vẫn chưa kiểm được; không có wrapper để loại khả năng rc lấy nhầm từ pipeline. Đó là lý do không coi tail+rc là xác minh đầy đủ full run, cũng không tự suy có hồi quy/P1 từ việc thiếu tail giữa.

`out>0` chỉ bắt một lớp xanh giả do không có stdout. Lệnh lỗi vẫn có thể in stdout; rc=127 ở cả hai vế vẫn là thất bại dù DELTA=0. Vì vậy phải đọc **rc mong đợi + marker dương + phạm vi output** cùng nhau. README đã công khai lease rc1 và loại trừ CI/merge; không thấy nó công nhận sáu bộ đều xanh.

Lần gọi t33 mới xác nhận có công cụ thì đúng workflow này lint được. Nó không biến lần full-gate cũ thành 121/121, không chứng minh các workflow khác, Windows hoặc GitHub Actions. Test và workflow có cùng blob trên ba SHA nên thiếu actionlint là giải thích hợp lý, được phản chứng ngắn xác nhận, cho lỗi lịch sử duy nhất hiện trong log.

## BIÊN NHẬN LƯỢT 13 — CƯỜNG ĐỘ LỜI KHAI

Ba trường băm/byte/reviewed_sha, blob neo và băm prompt đo độc lập được. Thời lượng, mã thoát launcher, số lần phóng, model 6/6, thread và stdout launcher không đo được từ hiện vật đã giao. Không lấy `lease-publish-test.json` (54.863 s, rc0 của **một suite**) hay final-check 21:04:16Z thay cho 1035.206 s của phiên reviewer. Không lấy run 229ddb14/head922956a của lượt 14 thay run d7edf347/headf77f198 của lượt 13.

`model_bang_chung` thực tế **không có lời khai yếu như prompt mô tả**: nó nói session đã ghi 6/6. Cách đọc hợp lệ ở lượt này là **attestation do người vận chuyển khai, CHƯA được reviewer14 xác thực độc lập**. Nên gắn nhãn TỰ KHAI và bổ sung giới hạn thiếu raw lượt 13, hoặc giao đúng run/session để đối chứng; không tự sửa `model_da_chay`, assurance hoặc verdict lịch sử thành giá trị đoán. Thiếu hiện vật không chứng minh model khác đã chạy và cũng không đủ để kết luận biên nhận bịa. `ops/bien_nhan_v2.py:36` công khai validator chỉ kiểm cấu trúc, không chứng minh identity thật; tôi không dùng schema/hash pass để nâng assurance. Chưa có lỗi P1/P2 về receipt được chứng minh.

### evidence-thieu-phuong-phap-trich-va-gioi-han-bao-phu  [P3]  Phân loại nguồn vẫn mạnh hơn hiện vật được giữ

TỆP/DÒNG: `ops/reviews/full-gate-pr468-20260907/README.md:11` (bảng dòng 15–20, DELTA dòng 42–48); `ops/reviews/pr468-hoso-4-packet-review-13-codex/DOC-MANIFEST.md:3` là ghi chú bao phủ liên quan.

VẤN ĐỀ: bảng cách trích/giới hạn đã có nội dung thật, nhưng “mọi số lấy từ tệp trong chính thư mục” và mọi loại nguồn đều “đo lại được” chưa phân biệt đọc giá trị tổng hợp với tự đếm lại từ nguyên liệu. Chỉ 1/6 kích thước stdout gốc kiểm được; 12 rc và các giây là log tổng hợp, không có script/timestamp để xác thực lần chạy. Giới hạn còn thiếu cách trích danh sách khẳng định và quyền phát hiện mục ngoài danh sách theo §8. Giữ nguyên slug/P3 của lượt trước; không coi thiếu log là bằng chứng số sai.

ĐÃ THỬ VÁ: đã tạo và áp thử bản prose trong scratch dựa trên các số tự đo: phân loại “tự đếm từ hiện vật” / “chỉ đọc log tổng hợp” / “chưa được giao”; giới hạn DELTA vào bốn cặp tệp lưu; bổ sung inventory có tiêu chí và giới hạn. Không yêu cầu chạy lại full suite để làm đẹp số lịch sử.

GÓI VÁ: `do-review14/goi-y/full-gate-prose.patch`, bản đầy đủ `full-gate-README.md` và hướng áp ở `do-review14/goi-y/README.md`, với nhãn **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Khi sửa README full-gate, cập nhật hash của README trong ARTIFACTS tương ứng; bảo toàn manifest và verdict reviewer lịch sử.

ĐÃ THỬ NGHIỆM: `python3 -B do-review14/audit_evidence.py` rc=0; tự đếm byte/dòng/marker, so bốn cặp byte, đối chiếu YAML/prompt/blob; mọi manifest đã có kết quả sha256sum. Patch --dry-run và áp thực tế trên bản sao đều rc=0; byte README sau áp bằng bản gợi ý; sha256sum của bản sao 12/12, rc=0 (`do-review14/prose-hint-check.json`). Nguy cơ bản vá: gọi “đo lại” vẫn dễ bị hiểu thành tái tạo lịch sử, hoặc bộ lọc chữ số bỏ số viết bằng chữ; gợi ý phải nói rõ cả hai.

ĐỘ TIN: cao về thiếu nguyên liệu/phân loại nguồn; không khẳng định số lịch sử sai.

### full-gate-t33-nham-that-bai-voi-khong-chay  [P3]  t33 đã chạy và thất bại ở kiểm công cụ

TỆP/DÒNG: `ops/reviews/full-gate-pr468-20260907/README.md:56`; đối chứng `nen.lease.norm.out:48`, `nen.lease.norm.out:50` và hai dòng tương ứng của sau.

VẤN ĐỀ: câu “Nó không đỏ, cũng không xanh — nó không chạy” mâu thuẫn log **ĐỎ t33**, **120/121 đạt; đã chạy=121, bỏ qua=0**. Hàm t33 đã chạy, assert thiếu công cụ rồi được main tính vào hong. Phần **lint workflow** mới là phần chưa chạy. Mức P3 vì mục ngay trước vẫn ghi lease rc1, KHÔNG tính xanh; không thấy đường chấp nhận gate bị nới.

ĐÃ THỬ VÁ: đã áp thử trong bản sao scratch, sửa câu thành “t33 đã được gọi và thất bại ở tiền điều kiện thiếu actionlint; thao tác lint workflow chưa chạy trong lần gate này; suite 120/121, rc1”. Giữ nguyên log và kết quả lịch sử. Không đổi timeout hoặc cách tính bỏ qua.

GÓI VÁ: `do-review14/goi-y/full-gate-prose.patch` (cùng README với finding trước), nhãn **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: nạp nguyên module, chỉ gọi `t33_workflow_dang_lease_phai_qua_actionlint`: PATH thiếu tool → đúng AssertionError; PATH thêm binary 1.7.7 có sẵn → passed, 0.060127 s. Ba SHA có cùng blob test/workflow. Không gọi main hoặc suite. Nguy cơ bản vá: vô tình gọi probe mới là sửa kết quả cũ; gợi ý tách hai mốc và chỉ ghi lint mới đạt trên sandbox này.

ĐỘ TIN: cao, đối chiếu log với điều khiển luồng và gọi hàm trực tiếp.


## KIỂM CUỐI VÀ BÀN GIAO

Ba cổng ngắn thực thi mới: doctrine-scan rc0/69 B/0.228 s; adr-song rc0/113 B/0.140 s;
doc-claims strict JSON rc0/70854 B/4.315 s. Lệnh, stdout và stderr đầy đủ nằm ở
`do-review14/short-gates.json` và các tệp cùng tên. Cổng doc-claims quét sáu root
CHANGELOG, SKILL, CLAUDE, CONTEXT, references, docs; **không quét ops/reviews** nên
pass ấy không tự chứng minh prose mới đúng. So JSON lịch sử với lần đo mới chỉ khác
`/advisories/74/reason`: `SHA_NOT_A_COMMIT_IN_HISTORICAL_DOC` →
`SHA_NOT_REACHABLE_FROM_HEAD`, làm kích thước giảm 7 B; không đổi số advisory/flags.
Tôi không coi byte của hai lần khác môi trường/HEAD là bắt buộc bằng nhau.

Gói gợi ý đã được áp trên bản sao `do-review14/prose-check/`, dry-run/apply đều rc0,
README ra đúng byte dự kiến và manifest của bản sao **12/12, rc0**. Không áp vào
`cay-kho/`; không thay output lịch sử, lease, assurance, timeout hoặc required checks.

Kiểm cuối **2026-09-07T22:32:41.348011+00:00**: HEAD/tree giữ nguyên; `git status --porcelain`, diff và index đều rỗng; 306 refs/heads; 0 commit mới. Không có lần chết/phóng lại. Kết quả ở `do-review14/final-check.json`.


`do-review14/ARTIFACTS.sha256` băm VERDICT.md và các script/kết quả bàn giao của lượt này;
đường dẫn tính từ gốc sandbox. Không gồm bản sao `prose-check/` (đã có patch, bản prose
và log kiểm), cũng không gồm bản thân manifest. Chạy kiểm tại gốc sandbox bằng
`sha256sum -c do-review14/ARTIFACTS.sha256`. Đây là gói reviewer14 mới, không sửa manifest
reviewer13 để hợp thức hóa phần đầu vào ngoài phạm vi băm.

**Kết luận tại 922956a: approve hồ sơ, 0 P1 · 0 P2 · 2 P3; không phải full-gate xanh hoặc merge authorization.**
