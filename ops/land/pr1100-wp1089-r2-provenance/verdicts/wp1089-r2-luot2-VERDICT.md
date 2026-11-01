verdict: approve
reviewed_sha: 6120ab88382ce605a2b7d1e853db208a15aaf835

Tree: `ef87a9803d039710399fe64e189a26a86d1fa692`. Base so sánh: `90c101b8d1f8895b66607de8582a18c5e72d834c`.
Spec r2 SHA-256: `c12e0449511f248de743ab603983c53d0a1c6f83f949bc4c1fa78b03f12bd020`; khớp lease g2. Effective write set gồm 7 tệp theo chỉ thị nới phạm vi.
Reviewer: OpenAI Codex, shell qua công cụ máy/API, transport machine. Chưa xác minh độc lập attestation model/effort/launcher hay bề mặt `codex_cli`; không suy các thuộc tính ấy từ lời khai executor. Sandbox thực tế là workspace-write; checkout nguồn được giữ read-only bằng quy trình.

Mọi phép thử chạy trên `thu-1/`, `thu-j1/` hoặc fixture tạm trong workspace. [Wrapper ngoại tuyến](review-support/run-offline.sh) dùng môi trường rỗng, HOME/CODEX_HOME riêng, TMPDIR trong workspace, tắt bytecode, chặn kết nối socket Python và curl/wget. Không gọi mạng/LIVE hoặc đọc credential thật. Probe dùng lại fixture giả sẵn có; không tự soạn credential/payload nhạy cảm.

## BẢNG SĂN

`PROBE <hướng>` dưới đây là `./review-support/run-offline.sh python review_probe.py <hướng>`, chạy từ workspace. [Mã probe](review_probe.py) và log được giữ để tái lập. Các ca đích của bộ cloud chạy qua runner nguyên trạng `--mot-ca`; mỗi mutant có đối chứng bản gốc xanh và chỉ được nhận GIET khi chốt đúng ca, không nhận crash vô can.

| Hướng / giả thuyết | Lệnh | Output thật cắt gọn | Kết luận |
|---|---|---|---|
| CAS server đọc md5 ngoài lock hoặc không nhả khi Drive lỗi | `PROBE cas` ([log](review-logs/cas.log)) | B1–B7 rc=0; get #1 lỗi: `tryLock,get,releaseLock`, ghi=0; get #2 lỗi: `tryLock,get,update,get,releaseLock`, ghi=1; update lỗi cũng nhả | KHÔNG PHẢI LỖI trong nguyên tử CAS/nhả lock; không hứa rollback khi update đã thành công rồi readback lỗi |
| CAS client retry giữ payload/md5 lần đầu | `PROBE cas`; `PROBE mutations` | `expected_md5_matches_each_download=[True, True]`, post=2, tải=3, rev=11, giữ khoá phiên khác; mutant cache bundle lần đầu → `GIET`, rev=4 | KHÔNG PHẢI LỖI |
| Readback thiếu một trong md5 server/rev/last_refresh hoặc cập nhật dấu khi lệch | `PROBE readback` ([log](review-logs/readback.log)) | Ba ca sai riêng md5/rev/last_refresh đều rc=0, `readback lệch`, `marker_unchanged=True` | KHÔNG PHẢI LỖI |
| Văn bản lỗi tầng vận chuyển hoặc lỗi giải mã lọt ra | `PROBE errors`; `PROBE transport` ([log](review-logs/transport.log)) | Lỗi tự do → `webapp LỖI_GỌI`; exception post/download → `lỗi RuntimeError/ValueError`; ping lỗi → `webapp không đo được`; cả gas thật với HTTP giả/non-JSON đều 1 dòng, rc=0 | KHÔNG PHẢI LỖI trên các nhánh đã đo |
| Version không hợp lệ còn phá hợp đồng một dòng | `PROBE errors`; `PROBE mutations` ([log](review-logs/errors.log)) | `lines=1`, output `webapp abc?phien-ban-khong-hop-le???2J`; P3A13 bỏ chuẩn hoá → `GIET` đúng ca | KHÔNG PHẢI LỖI; finding lượt 1 đã vá |
| `nap` còn đường bỏ xử lý dấu; Stop kế vẫn im lặng | `PROBE markers` ([log](review-logs/markers.log)) | 14 biến thể; missing entrypoint/PermissionError/communicate lỗi/quá hạn đều `marker_exists=False`; Stop sau missing: tải=2,ping=1,post=1,ghi=1 | KHÔNG PHẢI LỖI; finding lượt 1 đã vá |
| `--neu-doi` so sai `<`/`<=`, dấu hỏng không đi tiếp | `PROBE markers`; ca C2; mutant C2 | Đĩa < dấu: output rỗng, tất cả đếm=0; bằng cũng im lặng; mới hơn/vắng/`[1]` đi mạng; hai mutant C2 → `GIET` | KHÔNG PHẢI LỖI trên điều kiện đã đo |
| Daemon sau timeout tiếp tục bắt đầu post/ghi dấu | `PROBE timeout` ([đo lại](review-logs/timeout-recheck.log)) | Hạn .3s: trả sau .301s; tải trễ: post=0 sau worker; post đã vào trước hạn có thể hoàn tất, tải readback=2, nhưng dấu=False và chỉ 1 dòng timeout | KHÔNG PHẢI LỖI về hạn trả lệnh/không ghi dấu trong phạm vi đã đo; yêu cầu đã gửi không có bảo đảm huỷ từ xa |
| A12 r2 chỉ so identity và bỏ sót hằng 32 chép đúng giá trị | `PROBE ast_hook`; `PROBE mutations` | A12 rc=0; chép hằng 32/fileId/hàm đều `GIET ... (a) helper tự gắn tên`; helper không định nghĩa lại hai hàm | KHÔNG PHẢI LỖI |
| Hook Stop làm đổi khoá cũ hoặc sai argv/nuốt rc | `PROBE ast_hook`; mutant S2 | S1/S2 rc=0; bỏ `|| true` → `GIET`, rc=3, argv đúng `[ghi-nguoc,--neu-doi]` | KHÔNG PHẢI LỖI |
| `_goi_ngoai` nới quá rộng, bỏ cả gói bên thứ ba thật | `PROBE imports` ([đo lại](review-logs/imports-recheck.log)) | Cây thật `['yaml']`; cây kiểm soát chỉ còn `['external_dependency']`; t16 gốc PASS; bỏ stem scripts → GIET ở import `gas` chưa kê | KHÔNG PHẢI LỖI trên cây và phạm vi hiện tại; phương pháp stem không phân biệt được va chạm tên module trong tương lai |
| Cắt ca cũ / sai write set / đếm thiếu kích thước | `PROBE measure` ([log](review-logs/measure.log)) | `old_count=26; new_count=52; removed=[]; changed_old_bodies=[]`; files=7, .gs +33, ngoài .gs +471, tổng 504; snapshot hai diff khớp từng byte | KHÔNG PHẢI LỖI |

## BẢNG ĐO

| Executor khai / tiêu chí | Đo được độc lập | Khớp? |
|---|---|---|
| Cloud suite 52/52; mutant 80/80 | [Log](review-logs/cloud-suite.log): `CA: 52/52 dat`, `DOT BIEN: 80/80 bi giet dung ly do`, `TU KIEM PHAN HANG: DAT (4 dot bien)`, `TONG: DAT`; rc=0 | CÓ |
| `tl --selftest` 1774/1774 | Không chạy lại lượt 2 theo ngoại lệ prompt: diff lượt 1→2 chỉ đổi hai tệp ops, không đổi `scripts/`. Verdict lượt 1 ghi head/base cùng 1774/1774; đó là bằng chứng lịch sử trên SHA cũ, không phải lần đo mới trên SHA này | KHÔNG ĐO LẠI |
| Công cụ bán kính `manh`: 61/61 | [Log đo lại](review-logs/tools-recheck.log): `61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0`; tự kiểm song song ĐẠT, cổng cây thật ĐẠT, lỗi đột biến=0; rc=0 | CÓ |
| Release strict ok, 198/198 | [JSON](review-logs/release.json), rc=0: `ok=true`, expected=checked=198, `failed=[]`, `errors=[]`; base 197→198 | CÓ |
| K2 .gs +33, tổng 504 | 7 tệp đúng write set đã nới; +471 ngoài .gs +33 so Code.2.21.2p.gs =504≤600; .gs 33≤120 | CÓ |
| K1 bare Ruff F | [Log](review-logs/lint.log): Ruff 0.17.3, `All checks passed!`, rc=0; mutant tên chưa định nghĩa → F821, rc=1 | CÓ; không chứng nhận pin Ruff CI |
| G2 doctrine-scan | [Log](review-logs/doctrine.log): rc=0, 10 tệp, 0 chỗ chép doctrine | CÓ |
| L1 CI required jobs exact head | Không gọi mạng; chưa có biên nhận CI exact head được xác minh | KHÔNG ĐO ĐƯỢC |
| M1 LIVE sau land | Không thực hiện; chỉ thị cấm LIVE trong lượt này, chủ kho duyệt riêng | KHÔNG ĐO ĐƯỢC |

Suite cloud thực chạy từ workspace: `./review-support/run-offline.sh python -u thu-1/ops/cloud_agent_creds_test.py`. Các lệnh tổng còn lại thực chạy từ `thu-1/`:

```bash
../review-support/run-offline.sh env CONG_CU_TEST_BAN_KINH=manh python -u ops/cong_cu_test.py
../review-support/run-offline.sh python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
../review-support/run-offline.sh python .claude/dev/packet_loop.py doctrine-scan --root .
../review-support/run-offline.sh ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py
```

Lượt công cụ đầu dùng PATH thiếu `/root/.local/bin` nên t2 bỏ qua: `60/60 đạt; tổng=61, bỏ qua=1`. Không coi lượt đó là 61/61. Đã sửa PATH của wrapper để dùng binary actionlint có sẵn và đo lại, không cài hoặc tải gì. Chế độ `CONG_CU_TEST_BAN_KINH=manh` giao 490 mutant cho CI mảnh/gom; không nhận là đã chạy toàn bộ 490 ở lượt review này.

J1 phản chứng: cùng lệnh strict trên `thu-j1/` thêm 1 byte LF vào `.gs` → rc=2, `ok=false`, failed đúng `references/Code.2.21.2q.gs`, size 226231→226232 ([JSON](review-logs/release-mutant.json)). K1 phản chứng dùng stdin của Ruff ở cwd `thu-1/`, thêm một tên chưa định nghĩa → rc=1/F821 ([log](review-logs/lint-mutant.log)). Không sửa source để tạo hai phản chứng này.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: [VERDICT-luot1.md](VERDICT-luot1.md), `request_changes` trên `cf8d1efa24f597e4c6f9d336fdabc51fe094b39a`; [diff vá](diff-luot1-luot2.patch) khớp `git diff` hai exact SHA. Hai lớp, hai biểu hiện lịch sử; không có lớp/biểu hiện mới được xác nhận trong lượt này.

| Slug lớp / mức cũ | Trạng thái | Bằng chứng reviewer tự đo |
|---|---|---|
| `nap-loi-khong-xoa-dau` [P2] | ĐÃ VÁ THẬT | `ops/cloud_agent_creds.py:89` gọi `_dau_sau_nap` khi lỗi khởi chạy. Probe markers nay `marker_exists=False`; Stop kế đi mạng (tải=2,ping=1,post=1,ghi=1). PermissionError và lỗi communicate cũng xoá. `P3C4_nap_loi_khoi_chay_giu_dau` bị GIET đúng `p3c4_nap_khong_chay_duoc_xoa_dau` vì dấu còn=True |
| `phien-ban-ngoai-hop-dong-in-thang` [P3] | ĐÃ VÁ THẬT | `ops/cloud_agent_creds.py:245` thay ký tự ngoài tập cho phép bằng `?`; probe version newline/CR/ESC nay đúng 1 dòng. `P3A13_in_version_tho` bị GIET đúng ca mới. Kiểm thêm gas thật với lỗi HTTP/non-JSON và các exception: không in thông điệp gốc |

Đã rà toàn bộ đường thoát nghiệp vụ của `nap`, không chỉ hunk vá:

1. Thiếu khoá: dòng 78 xử lý dấu rồi return 0.
2. Entrypoint thiếu hoặc Popen ném OSError (gồm PermissionError): dòng 89 xử lý dấu rồi return 0.
3. Bootstrap đã chạy: communicate thành công, hết hạn hoặc lỗi chờ đều hội tụ qua dòng 102 rồi return 0 ở 103. Nhánh hết hạn/lỗi chờ dùng kết luận KHÔNG ĐO ĐƯỢC, nên không nhận nhầm dòng ĐÃ NẠP đã in trước khi treo. Kết quả dọn nhóm đã dừng hay chưa xác minh không đổi điểm hội tụ này.
4. Trong nhánh 3, đã đo đủ các nhóm kết luận: không có dòng agent (rc=0 và rc=7), nhiều dòng, sai trạng thái/thiếu dấu phân cách, KHÔNG CẤU HÌNH, KHÔNG ĐO ĐƯỢC, ĐÃ NẠP nhưng giữ đĩa, và ĐÃ NẠP có ghi đè Codex. Chỉ trường hợp cuối ghi dấu; mọi trường hợp khác xoá. Đọc/ghi/xoá dấu lỗi OSError được xử lý best effort; không khẳng định xóa được khi hệ điều hành từ chối quyền.

Đường đầu ra mới của `ghi-nguoc` cũng được đối chiếu toàn bộ: các trạng thái bỏ qua/auth/bundle/readback/timeout là văn bản cố định; rev là int đã kiểm; lỗi import/worker chỉ đưa tên lớp; `_ma_loi` chỉ nhận dạng mã hằng và loại văn bản tự do; chỉ nhánh phiên bản dùng chuỗi server, nay giới hạn 40 ký tự và chuẩn hoá tập ký tự. Luồng worker không có print trong bản gốc; gas.get/post và public-download không tự in lỗi. A9 kiểm sentinel fixture và base64 blob; probe bổ sung kiểm tổng số dòng stdout+stderr.

Chuẩn hoá phiên bản bảo đảm một dòng, không tự chứng minh che mọi chuỗi nhạy cảm nếu một server bất thường phản xạ chúng vào trường version. Bản GAS đang review trả version từ hằng APP_VERSION; không tìm thấy đường thực tế phản xạ credential vào trường đó. `_ma_loi` lọc hình dạng, không phải danh sách mã ngữ nghĩa. Không tạo payload nhạy cảm để suy diễn finding rò credential; không có cơ sở nâng vấn đề phiên bản cũ thành P2 trong lượt này.

## ĐỐI CHIẾU TỪNG TIÊU CHÍ NGHIỆM THU

Cloud suite nguyên trạng đạt đủ 52 ca, không bỏ qua; các hàng dưới chỉ ra phép đo tương ứng. A9 dùng tập SC đại diện, không phải chứng minh mọi phản hồi server tuỳ ý. Các ca B trích nguyên hàm action và nhánh case từ `.gs`; đồ giả Python/Node lưu byte và tính lại md5 sau mỗi lần ghi, không diễn sẵn kết quả thành công. A6 thay blob giữa tải và post nên lần đầu phải xung đột thật.

| Tiêu chí | Ca / phép đo thực chạy | Kết quả |
|---|---|---|
| B1 | `p3b1_cas_khop_thi_ghi` | 1 ghi, byte giả đổi, md5/size khớp; mutant không ghi bị giết |
| B2 | `p3b2_cas_lech_khong_ghi`; mutant B2 | CAS_CONFLICT, md5 hiện tại đúng, 0 ghi, sha256 không đổi; mutant bị giết vì ghi=1 |
| B3 | `p3b3_tham_so_sai_khong_ghi` | Đủ 4 biến thể: vắng/sai expect_md5, vắng property, sai fileId; đúng mã và 0 ghi |
| B4 | `p3b4_co_blob` | Từ chối 0 và 65537 byte; nhận 65536; mutant ngưỡng >= bị giết |
| B5 | `p3b5_lock_ban`; mutant B5 | LOCK_BUSY, 0 đọc/ghi; mutant bị giết vì đọc=1 |
| B6 | `p3b6_thu_tu_va_finally`; PROBE cas | Đúng lock→get→update→get→release; lỗi update/get#1/get#2 đều nhả |
| B7 | `p3b7_ban_va_nhanh_case` | Version/case đúng 1 lần, case không có ở 2p, node --check rc=0; mutant xoá case bị giết |
| A1 | `p3a1_khong_phai_cloud` | Remote vắng/false đều bỏ qua và 0 mạng |
| A2 | `p3a2_khoa_yeu` | Vắng/31 ký tự/40 ký tự nhưng 11 khác nhau không đi mạng; biên 32/12 đi tiếp |
| A3 | `p3a3_cong_phien_ban` | Chặn p/không hậu tố/abc/ping lỗi; cho q/2.22.0/2.21.10; mutant so chuỗi bị giết |
| A4 | `p3a4_da_cu` | Bundle bằng/mới hơn đĩa đều ĐÃ CŨ, 0 post, auth byte không đổi |
| A5 | `p3a5_da_ghi_giu_khoa_cu` | Giải mã Drive giả: đúng schema/rev/auth, giữ từng khoá cũ; sentinel môi trường không vào payload |
| A6 | `p3a6_cas_tai_lai_dung_ban_moi`; PROBE cas/mutations | 2 post, rev=11, khoá phiên khác được giữ; cả mutant suite và cache độc lập đều bị giết |
| A7 | `p3a7_cas_lap_dung_ba` | CAS_CONFLICT và LOCK_BUSY mỗi loại đúng 3 post, rc=0; mutant 1 lần/vô hạn bị giết |
| A8 | `p3a8_readback_lech`; PROBE readback | Sai md5, rev hoặc last_refresh đều readback lệch, dấu không đổi; bỏ tải lại bị giết |
| A9 | `p3a9_mot_dong_khong_lo`; PROBE errors/transport | Không sentinel/master/token/base64 fixture trên hai kênh; các lỗi vận chuyển thường và non-JSON đều 1 dòng |
| A10 | `p3a10_rc0_va_cu_phap` | Nghiệp vụ rc=0; --la rc=2, 0 mạng; mutant đổi rc bị giết |
| A11 | `p3a11_han_chot`; PROBE timeout | Hạn .5s xong <1.5s; bổ sung hạn .3s xong .301s, không ghi dấu sau huỷ; xem giới hạn yêu cầu đã gửi |
| A12 | `p3a12_khong_dinh_nghia_lai_ten_tl_gws`; 3 mutant A12 | AST mọi cấp + identity hai hàm; chép đúng hằng 32/fileId/hàm đều đỏ ở AST theo errata r2 |
| C1 | `p3c1_nap_ghi_xoa_dau`; `p3c4_nap_khong_chay_duoc_xoa_dau`; PROBE markers | Ghi dấu đúng hai khoá/0600 khi ghi đè Codex; giữ đĩa/lỗi/không khởi chạy đều xoá dấu cũ |
| C2 | `p3c2_neu_doi`; PROBE markers | Đĩa≤dấu im lặng/0 mạng; mới hơn/vắng/hỏng dạng [1] đi tiếp; mutant bị giết |
| C3 | `p3c3_dau_sau_ghi_va_cu` | Sau ĐÃ GHI/ĐÃ CŨ, last_refresh/md5 đúng nguồn; 0600, không có token |
| S1 | `p3s1_settings_co_stop` | Đúng1 Stop hook, lệnh và timeout 30; so dict mọi khoá cũ bằng base, base không Stop; mutant sửa SubagentStop bị giết |
| S2 | `p3s2_stop_chay_that`; mutant S2 | Chạy lệnh thật qua bash, argv đúng, helper giả rc=3 nhưng hook rc=0; bỏ || true bị giết |
| F1 | Cloud suite đầy đủ | rc=0, 52/52, 80/80, tự kiểm phân hạng DAT, TONG DAT; khớp regex đăng ký CI trước dòng rc của wrapper |
| F2 | PROBE measure | 26 tên ca cũ còn đủ, không thân ca cũ nào đổi; tất cả 52 ca đạt |
| J1 | Strict release và mutant1 byte | Head ok=true/198=198=197+1; mutant rc=2 và failed đúng .gs |
| G1 | Đối chiếu diff lượt 1→2 | Không đo lại full selftest theo ngoại lệ prompt; không đổi scripts;1774/1774 là số lịch sử lượt 1 |
| G2 | Doctrine-scan | rc=0;10 tệp,0 chỗ chép doctrine |
| K1 | Ruff F và mutant F821 | Head rc=0; mutant rc=1/F821; chỉ bare lint |
| K2 | PROBE measure | 7 tệp đúng phạm vi;33≤120; tổng 504≤600 |
| L1 | Offline | Chưa xác minh required CI exact SHA; không coi thiếu/skipped là pass |
| M1 | Sau land, LIVE | Chưa đo; không dùng fake thay phép đo đích thật |

`approve` cho diff trên exact SHA đã nêu: không có finding P0/P1/P2/P3 mới được xác nhận; hai finding lịch sử đã đóng bằng phép đo dương/âm. Kết quả này không thay biên nhận CI, assurance identity hoặc quyền merge/land/deploy.


## KIỂM TRA KHO NGUỒN VÀ GIỚI HẠN

HEAD/tree đầu và cuối vẫn là các OID ở đầu báo cáo. Kiểm cuối bằng `git --no-optional-locks` cho tracked/index sạch; status gồm untracked và ignored rỗng; diff Git khớp từng byte `diff.patch` ([log](review-logs/source-final.txt)). Không sửa `cay-kho/`, không push, không gọi mạng. Snapshot chỉ chứng minh trạng thái quan sát ở các mốc; không phải chứng nhận OS cưỡng chế read-only.

L1 (required CI exact head), M1 (LIVE sau land), Windows, attestation launcher/model/effort và toàn bộ 490 mutant công cụ qua job mảnh chưa được xác minh. Full selftest không chạy lại theo ngoại lệ prompt; không trình số 1774/1774 lịch sử thành phép đo mới. Hai lớp nhạy cảm CAS và rò credential được kiểm ngoại tuyến như BẢNG SĂN; không suy các phép đo ấy thành bằng chứng CAS hay đường ghi tới đích LIVE.
