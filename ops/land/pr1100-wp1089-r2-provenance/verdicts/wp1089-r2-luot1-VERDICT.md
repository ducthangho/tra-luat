verdict: request_changes
reviewed_sha: cf8d1efa24f597e4c6f9d336fdabc51fe094b39a

Spec r2 SHA-256: `c12e0449511f248de743ab603983c53d0a1c6f83f949bc4c1fa78b03f12bd020`.
Tree: `f08bcfa30a12772bbc8f4e001f5b8a24f90b0c94`; base so sánh: `90c101b8d1f8895b66607de8582a18c5e72d834c`.
Reviewer: OpenAI Codex; công cụ shell máy thực qua API. Không tự suy model/effort/CLI identity từ prompt; chưa đo được attestation của launcher. Ngưỡng theo prompt: chỉ P0/P1 hoặc P2 ảnh hưởng tính đúng đắn/an toàn chặn approve.

Kho `cay-kho/` được giữ read-only theo quy trình; mọi lệnh test chạy trên `thu-1/` hoặc fixture tạm trong workspace. Wrapper `review-support/run-offline.sh` dùng môi trường rỗng, HOME/CODEX_HOME riêng, TMPDIR trong workspace, cấm socket Python qua `sitecustomize`, tắt bytecode. Không gọi LIVE/mạng; không đọc credential thật. `ruff --no-cache`.

## BẢNG SĂN

Các lệnh dưới chạy từ workspace, tiền tố `./review-support/run-offline.sh python review_probe.py` (viết tắt `PROBE`); mã nguồn probe và log được giữ để tái lập. Các đột biến dùng runner gốc, tạo bản tạm rồi gọi `ops/cloud_agent_creds_test.py --mot-ca <ca>`.

| Hướng độc lập / giả thuyết | Lệnh | Output thật cắt gọn | Kết luận |
|---|---|---|---|
| CAS server: đọc md5 ngoài lock hoặc thiếu finally khi Drive lỗi | `PROBE cas` | B1–B7 rc=0. Lỗi update: `tryLock,get,update,releaseLock`; lỗi get thứ 1/2 đều `released=True` | KHÔNG PHẢI LỖI; lỗi readback sau update đã ghi 1 lần, không thể hứa rollback lỗi Drive |
| CAS client: retry trên bundle cũ hoặc sai số lần | `PROBE cas`; `PROBE mutations` | A6/A7 rc=0; `P3A6_payload_tren_ban_lan_1 GIET ... rev=4` thay vì rev=11; B2/B5/B6 đều GIET đúng ca | KHÔNG PHẢI LỖI |
| Readback thiếu một trong md5/rev/last_refresh; ghi dấu dù lệch | `PROBE readback`; `PROBE mutations` | A5/A8 rc=0; đúng md5+rev nhưng sai last_refresh ⇒ `readback lệch`, `marker_unchanged=True`; bỏ readback ⇒ GIET | KHÔNG PHẢI LỖI |
| Lỗi vận chuyển lọt ra stdout/stderr | `PROBE error` | error tự do ⇒ `webapp LỖI_GỌI`; exception post ⇒ `lỗi RuntimeError`; exception ping ⇒ `webapp không đo được`; mỗi ca 1 dòng, rc=0; A9/A10 rc=0 | KHÔNG PHẢI LỖI trên các nhánh vận chuyển đã đo |
| Ping.version không hợp lệ bị in nguyên văn | `PROBE error` | phiên bản gồm văn bản thường + xuống dòng ⇒ `lines=2; post=0; rc=0` | LỖI hợp đồng một dòng; P3; chưa chứng minh rò credential thật |
| Timeout: worker tiếp tục post/ghi dấu sau khi main hết hạn | `PROBE timeout` | hạn .5s: lệnh xong .500–.503s; tải trễ ⇒ post=0; post đã vào trước hạn có thể hoàn tất và tải readback sau hạn trong in-process; cả hai `marker_exists=False` | KHÔNG PHẢI LỖI về hạn trả lệnh/ghi dấu đã đo; không có bảo đảm huỷ yêu cầu đã gửi |
| Dấu: nap lỗi trước khởi chạy có xoá dấu cũ?; dấu mới hơn đĩa có im lặng? | `PROBE markers` | C1/C2/C3 rc=0; disk<marker ⇒ 0 mạng; bootstrap thiếu ⇒ `marker_exists=True`; Stop kế ⇒ 0 mạng | LỖI nhánh xoá dấu khi bootstrap không khởi chạy; P2: bỏ lượt đối chiếu bắt buộc sau nap lỗi |
| A12 r2 có bắt cả hằng 32 giữ nguyên? | `PROBE ast_hook`; `PROBE mutations` | A12 rc=0; chép hằng 32 / fileId / hàm đều `GIET ... (a) helper tự gắn tên` | KHÔNG PHẢI LỖI |
| Hook Stop phá hook cũ hoặc nuốt sai argv/rc | `PROBE ast_hook`; `PROBE mutations` | S1/S2 rc=0; bỏ `|| true` ⇒ `GIET ... rc=3 argv=[ghi-nguoc,--neu-doi]` | KHÔNG PHẢI LỖI |
| _goi_ngoai loại nhầm gói ngoài / quét lan scripts | `PROBE imports` | cây thật: `['yaml']`; cây kiểm soát có helper scripts và dependency ngoài: `['external_dependency']` | KHÔNG PHẢI LỖI trên phạm vi và cây hiện tại; stem-collision vốn là giới hạn phương pháp |
| Bộ ca cũ bị đổi/xoá; write set/kích thước/manifest khai sai | `PROBE measure` | `old_count=26; new_count=50; removed=[]; changed_old_bodies=[]`; 7 tệp đã nới, .gs +33, tổng +491; manifest 197→198 | KHÔNG PHẢI LỖI |

## BẢNG ĐO

| Executor khai / yêu cầu | Đo được | Khớp? |
|---|---|---|
| cloud_agent_creds_test: 50/50; 78/78 đúng lý do | `CA: 50/50 dat`; `DOT BIEN: 78/78 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (4 dot bien)`; `TONG: DAT`; rc=0, `review-logs/cloud-suite.log` | CÓ |
| tl --selftest: 1774/1774 | Base và head cùng `1774/1774`, rc=0; 0 ca đỏ mới; `review-logs/selftest.log`, `selftest-base.log`, `g1-delta.json` | CÓ |
| cong_cu_test bán kính manh: 61/61 | `cong_cu_test: 61/61 đạt; tổng=61, bỏ qua=0, tiền kiểm bỏ qua=0`; rc=0; tự kiểm song song ĐẠT; cổng cây thật ĐẠT | CÓ; 490 đột biến được giao job CI, chưa đo trọn bán kính |
| release verify strict ok, 198/198 | rc=0; `ok=true`, expected=198, checked=198, errors=[] | CÓ |
| K2 .gs +33, tổng +491 | 458 dòng ngoài .gs +33 =491; 7 tệp đúng phạm vi được nới trong prompt | CÓ |
| K1 bare Ruff nhóm F | Ruff 0.16.9, `All checks passed!`, rc=0 | CÓ; chỉ bare lint, không chứng nhận pin CI |
| G2 doctrine-scan | rc=0, quét 10 tệp, 0 chỗ chép doctrine | CÓ |
| L1 CI required jobs exact head | Không gọi mạng; bundle chưa có biên nhận CI được xác minh | KHÔNG ĐO ĐƯỢC |
| M1 LIVE sau land | Ngoài phạm vi và bị cấm trong lượt này | KHÔNG ĐO ĐƯỢC |

`request_changes` vì finding P2 `nap-loi-khong-xoa-dau` làm mất lượt đối chiếu bắt buộc sau nap lỗi. P3 không tự chặn theo ngưỡng prompt. Các bộ đo head và selftest base đều kết thúc rc=0; suite xanh chưa bao phủ nhánh lỗi mới tái hiện.


Các lệnh tổng thực chạy (cwd `thu-1/`, output trong `review-logs/`):

```bash
../review-support/run-offline.sh python -u ops/cloud_agent_creds_test.py
../review-support/run-offline.sh python -u scripts/tl.py --selftest
../review-support/run-offline.sh env CONG_CU_TEST_BAN_KINH=manh python -u ops/cong_cu_test.py
../review-support/run-offline.sh python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
../review-support/run-offline.sh python .claude/dev/packet_loop.py doctrine-scan --root .
../review-support/run-offline.sh ruff check --no-cache --select F ops/cloud_agent_creds.py ops/cloud_agent_creds_test.py
```

Selftest base chạy cùng wrapper trong `thu-base/` đã checkout đúng merge-base: tổng kết 1774/1774, rc=0; head cũng 1774/1774, rc=0 và 0 ca đỏ mới (`review-logs/g1-delta.json`). Các nhãn trạng thái quan sát trên stdout hai lượt giống nhau; stdout có cả output ca lồng, không lấy số nhãn làm mẫu số ca. J1 mutant ở `thu-j1/` thêm đúng 1 byte LF vào `.gs`: size 226231→226232, strict verify rc=2, failed đúng tệp này. K1 mutant thêm một tên chưa định nghĩa vào helper trên bản sao: rc=1, F821 đúng tên (`review-logs/ruff-mutant.log`).

## BẢNG LỚP

Lượt 1, không có finding lượt trước của packet này được giao. A12 là errata kế thừa trong spec, đã kiểm lại ba mutant theo r2. Có 2 lớp / 2 biểu hiện mới:

| Slug lớp / finding | Mức cao nhất | Trạng thái | Hướng đóng lớp |
|---|---|---|---|
| nap-loi-khong-xoa-dau | P2 | MỞ; lý do request_changes | Mọi đường nap không ghi đè Codex đều xoá dấu; thêm chốt lỗi khởi chạy + Stop đi mạng |
| phien-ban-ngoai-hop-dong-in-thang | P3 | MỞ; owner executor #1089 | Chuẩn hoá version lỗi; chốt tổng số dòng bằng 1 |

## ĐỐI CHIẾU TỪNG TIÊU CHÍ NGHIỆM THU

Suite chạy đủ 50 hàm ca được nhận diện, đạt 50/50, không bỏ qua. Tên ca dưới đây thuộc `ops/cloud_agent_creds_test.py`; `PROBE` là lệnh đã định nghĩa trong BẢNG SĂN, có log riêng. Tập SC của A9 là tập đại diện trong mã test, không chứng minh mọi phản hồi server tuỳ ý.

| Tiêu chí | Ca / phép đo đã chạy | Kết quả và giới hạn |
|---|---|---|
| B1 | p3b1_cas_khop_thi_ghi | Đạt 1 ghi, byte/md5/size đúng |
| B2 | p3b2_cas_lech_khong_ghi; mutant B2 | Đạt CAS_CONFLICT, 0 ghi, sha256 không đổi; mutant GIET |
| B3 | p3b3_tham_so_sai_khong_ghi | Đạt đủ 4 biến thể, đúng mã, 0 ghi |
| B4 | p3b4_co_blob | Đạt: từ chối 0/65537, nhận 65536 byte |
| B5 | p3b5_lock_ban; mutant B5 | Đạt LOCK_BUSY, 0 đọc/ghi; mutant GIET vì đọc=1 |
| B6 | p3b6_thu_tu_va_finally; PROBE cas | Đạt thứ tự lock/get/update/get/release; ném ở update/get #1/get #2 đều nhả lock |
| B7 | p3b7_ban_va_nhanh_case | Đạt version/case đúng 1 lần, 2p không có case, Node syntax rc=0 |
| A1 | p3a1_khong_phai_cloud | Đạt remote vắng/false, 0 mạng |
| A2 | p3a2_khoa_yeu | Đạt 3 biến thể yếu/vắng và biên 32 ký tự/12 ký tự khác nhau |
| A3 | p3a3_cong_phien_ban | Đạt p/không hậu tố/abc/ping lỗi và q/2.22.0/2.21.10; version xuống dòng bổ sung phát hiện P3 |
| A4 | p3a4_da_cu | Đạt bundle bằng/mới hơn đĩa, không post, auth.json byte không đổi |
| A5 | p3a5_da_ghi_giu_khoa_cu | Đạt decrypt byte Drive giả để so schema/rev/auth, giữ từng khoá cũ, không sentinel môi trường |
| A6 | p3a6_cas_tai_lai_dung_ban_moi; mutant stale payload | Đạt rev=11 và khoá phiên khác; mutant GIET vì rev=4 |
| A7 | p3a7_cas_lap_dung_ba | Đạt đúng 3 post cho cả CAS_CONFLICT và LOCK_BUSY, rc=0 |
| A8 | p3a8_readback_lech; PROBE readback | Đạt sai md5/sai rev; ca thêm đúng md5+rev nhưng sai last_refresh cũng lệch, dấu không đổi |
| A9 | p3a9_mot_dong_khong_lo; PROBE error | Đạt sentinel trong SC; văn bản lỗi vận chuyển không lọt ra. Cam kết một dòng tổng quát còn hở ở version, P3 |
| A10 | p3a10_rc0_va_cu_phap | Đạt nghiệp vụ rc=0, --la rc=2 và 0 mạng |
| A11 | p3a11_han_chot; PROBE timeout | Đạt hạn .5s và <1.5s; không ghi dấu sau huỷ trong các ca đo. POST đã vào vận chuyển có thể hoàn tất |
| A12 | p3a12_khong_dinh_nghia_lai_ten_tl_gws; PROBE mutations | Đạt AST/identity r2; chép đúng hằng 32, fileId, hàm đều GIET ở AST |
| C1 | p3c1_nap_ghi_xoa_dau; PROBE markers | Các ca kê trong C1 đạt; nhánh không khởi chạy bootstrap không xoá dấu, P2 mục tiêu 3 |
| C2 | p3c2_neu_doi; thêm disk<marker | Đạt = và < im lặng, > đi mạng, dấu vắng/[1] đi mạng; mutant != GIET |
| C3 | p3c3_dau_sau_ghi_va_cu | Đạt 2 khoá, md5/last_refresh đúng, 0600, không token; readback lệch không đổi dấu |
| S1 | p3s1_settings_co_stop | Đạt dict cũ bằng base, Stop đúng 1 hook/timeout=30/đúng lệnh; base không Stop |
| S2 | p3s2_stop_chay_that | Đạt argv đúng, giả rc=3 nhưng bash rc=0; bỏ || true ⇒ GIET |
| F1 | Suite gốc | Đạt rc=0; CA 50/50; DOT BIEN 78/78; TU KIEM PHAN HANG DAT; TONG DAT |
| F2 | PROBE measure | Đủ 26 ca cũ, không ca nào đổi thân; toàn bộ 50 ca xanh |
| J1 | strict release verify; mutant thu-j1 | Head ok=true, 198/198=197+1; mutant rc=2, failed đúng .gs |
| G1 | selftest head, core.abbrev=7 | Base và head đều 1774/1774, rc=0; 0 ca đỏ mới; xem g1-delta.json |
| G2 | doctrine-scan | Đạt rc=0, 10 tệp, 0 chỗ chép doctrine |
| K1 | Ruff 0.16.9 --no-cache --select F trên 2 tệp | Đạt rc=0; thêm tên chưa định nghĩa trong bản sao ⇒ rc=1/F821; không chứng nhận pin Ruff CI |
| K2 | PROBE measure | Effective write set 7 tệp đã được prompt nới; .gs +33≤120, tổng +491≤600 |
| L1 | Offline, chưa có receipt CI exact head đã xác minh | KHÔNG ĐO ĐƯỢC; check vắng/skipped không được coi xanh |
| M1 | Cấm LIVE, phép đo sau land do chủ kho duyệt | KHÔNG ĐO ĐƯỢC; không thay bằng đồ giả |

### nap-loi-khong-xoa-dau [P2] Xoá dấu cũ cả khi không khởi chạy được bootstrap

- **TỆP/DÒNG:** `ops/cloud_agent_creds.py:87–89`, đối chiếu đường mới gọi `_dau_sau_nap` ở dòng 102 và nhánh thiếu khoá ở dòng 78.
- **VẤN ĐỀ:** mục tiêu 3 yêu cầu mọi kết luận `nap` ngoài `ĐÃ NẠP` có ghi đè Codex đều xoá dấu, để `Stop` đầu tiên đối chiếu bundle qua mạng một lần. Nhánh `except OSError` thoát trước bước xoá dấu. Với dấu có timestamp bằng đĩa, `nap` báo `KHÔNG ĐO ĐƯỢC` nhưng `Stop --neu-doi` sau đó im lặng và không tải/ping/post. Đây là sai chuyển trạng thái của đường phục hồi, không chỉ thiếu ca test; C1 hiện chỉ bao phủ lỗi do tiến trình bootstrap đã chạy rồi in ra. Không khẳng định phép thử này chứng minh mất token mới.
- **ĐÃ THỬ NGHIỆM:** `./review-support/run-offline.sh python review_probe.py markers` (rc=0; [log](review-logs/markers.log)). Dùng fixture đã có của executor, tạo dấu cũ hợp lệ và xoá `scripts/tl.py` CHỈ trên cây tạm mà `chay_nap` dựng. Output thật:
  ```text
  nap bootstrap missing: rc=0; marker_exists=True; output=['agent_creds: KHÔNG ĐO ĐƯỢC — không chạy được bootstrap (FileNotFoundError)']
  next Stop with leftover marker: output=''; calls={'tai': 0, 'ping': 0, 'post': 0, 'ghi': 0}
  ```
  Mô phỏng thiếu entrypoint chỉ là cách kích hoạt nhánh; cùng nhánh xử lý lỗi khởi tạo tiến trình như PermissionError/OSError. Ca bổ sung giữ nguyên scripts/tl.py nhưng tiêm PermissionError vào Popen cũng cho marker_exists=True. Các ca C1/C2/C3 gốc vẫn rc=0.
- **ĐỘ TIN:** cao về vi phạm mục tiêu 3 và thiếu lượt đối chiếu; không suy thành bằng chứng hỏng dữ liệu LIVE.
- **GỢI Ý VÁ:** tập trung xử lý dấu ở mọi đường thoát của `nap`, hoặc gọi xử lý kết luận trước `return` trong nhánh lỗi khởi chạy. Thêm ca dấu cũ + không khởi chạy được bootstrap; chốt dấu phải bị xoá và `--neu-doi` kế phải đi mạng. Không sửa kho nguồn trong lượt review này.

### phien-ban-ngoai-hop-dong-in-thang [P3] Chuẩn hoá phiên bản không hợp lệ trước khi in

- **TỆP/DÒNG:** `ops/cloud_agent_creds.py:242–244`.
- **VẤN ĐỀ:** chuỗi `ping.version` bị từ chối bởi regex lại được đưa nguyên 40 ký tự đầu vào output. Một ký tự xuống dòng đã tạo dòng thứ hai, trái hợp đồng đúng một dòng ở mục tiêu 2. Giới hạn chiều dài không chuẩn hoá ký tự điều khiển. Các error vận chuyển đã được `_ma_loi`/exception handling loại bỏ đúng; lỗi này là đường in phiên bản riêng.
- **ĐÃ THỬ NGHIỆM:** `./review-support/run-offline.sh python review_probe.py error` (rc=0; [log](review-logs/error.log)); chỉ dùng văn bản thường, không tạo payload credential:
  ```text
  non-sensitive malformed version: rc=0; lines=2; post=0; output='agent_creds_ghi_nguoc: KHÔNG HỖ TRỢ — webapp abc\nphien-ban-khong-hop-le\n'
  ```
  Đối chứng: error trả về tự do, exception post và exception ping đều rc=0, một dòng, không in thông điệp gốc. A9/A10 gốc vẫn rc=0.
- **ĐỘ TIN:** cao về lỗi một dòng; chưa chứng minh rò credential. Webapp của candidate trả `APP_VERSION` hằng, nên không có cơ sở nâng thành P2 rò token chỉ từ fixture phản hồi bất thường. Nếu tầng server phản xạ dữ liệu nhạy cảm vào version thì nhánh này sẽ in nó; hướng đó chỉ mô tả, không tự soạn payload nhạy cảm theo chỉ thị.
- **GỢI Ý VÁ:** với version không khớp regex, in nhãn cố định hoặc biểu diễn một dòng đã loại ký tự điều khiển; chỉ in số phiên bản đã xác thực. Thêm ca version xuống dòng, chốt tổng số dòng stdout+stderr. **Owner:** executor packet #1089; nên sửa cùng lượt P2. P3 này không tự chặn verdict theo ngưỡng prompt.


## KIỂM TRA KHO NGUỒN VÀ GIỚI HẠN

HEAD/tree đầu và cuối vẫn là các OID ghi đầu báo cáo. Diff tracked/index rỗng; không có tệp untracked/ignored trong `cay-kho/`; diff Git đúng merge-base so HEAD khớp từng byte `diff.patch` (`diff_snapshot_match_rc=0`). Bằng chứng: `review-logs/source-final.txt`. Sandbox thực tế là workspace-write; tính read-only của checkout được thực hiện bằng quy trình thao tác và kiểm trạng thái, không phải chứng nhận OS đã chặn mọi đường ghi.

Chỉ đo offline. Chưa chứng nhận required jobs CI exact head (L1), toàn bộ 490 đột biến công cụ qua các job mảnh, model/effort/launcher attestation, Windows hay LIVE (M1). Không cấp quyền merge/land/deploy hoặc tự tạo assurance từ kết quả review này.
