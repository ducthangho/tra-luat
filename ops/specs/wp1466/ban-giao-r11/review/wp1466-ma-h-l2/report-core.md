## Phạm vi và nguồn chứng cứ

Review độc lập trên H `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2`, base `6a4f52dde37582df5c6a562e988d9551f45ae150`; tree H `d2f22ad619c51a0bab1cd6241615d6ba6bf7ad33`. HEAD được kiểm đầu tiên sau PROMPT; băm đặc tả được kiểm trước khi review. Đã đọc nguyên văn chỉ thị cross-review, CLAUDE.md, AGENTS.md, các mục protocol được giao, ADR-0060 M1–M12, ADR-0062/0063 và đặc tả r11. Đối chiếu bốn handoff, review mã lượt 1 và review đặc tả r10.

Mọi đường dẫn bằng chứng dưới đây tính từ `out/`. Mỗi log có argv, cwd, giờ bắt đầu, output thật và rc/elapsed cuối nếu đã kết thúc. `run.py` chỉ bọc ghi log, đặt bytecode/cache/TMPDIR dưới `out/`, không sửa sản phẩm. `h/`, `base/`, `full-h/` là các cây thử riêng; core.abbrev=7. `independent.py`, `probes.py`, `reviewer_mutants.py`, `lint_delta.py`, `authority.py` do reviewer viết. `run_cases.py` lấy từ script executor sau khi đọc và gọi API thật `packet_loop_test_manh.chay`; phép đo tập bắt buộc/N3 âm dùng script executor đã đọc, chạy lại độc lập. Không nhận số của executor làm kết quả reviewer.

Identity theo phiên Codex; session ID lấy từ môi trường, không phải attestation máy chủ. Model cụ thể và effort thực phục vụ **KHÔNG ĐO ĐƯỢC** từ bên trong; `effort: high` là phân công. Họ `openai` theo identity provider và quy tắc ADR-0065. Một trợ lý `tl_auditor` chỉ đọc log selftest/registry và tổng hợp delta theo hướng dẫn bước 5 trong CLAUDE.md; không tạo verdict riêng, không gọi reviewer khác. Đây vẫn là lời gọi review Codex cuối 13/13.

## BẢNG LỚP — lớp MỞ

| slug lớp | finding IDs/biểu hiện | hạng cao nhất còn mở | nguồn lượt/SHA | phương án vá chung | phép kiểm đóng lớp |
|---|---|---|---|---|---|
| `thieu-khoi-nang-tran-kich-thuoc` | F03: bản chép khối nâng trần trong lease chưa đúng nguyên khối | P3 | Review đặc tả r10 `feb0b77`; lease g3 `ca001f8` dùng cho H | Chép khối r11§10 sang hồ sơ lease, giữ các trường khác | So nguyên văn/mapping; patch trong fixture đạt, lease nguồn chưa sửa |

## ĐỐI CHIẾU LƯỢT TRƯỚC

### (i) Bản vá thật và lớp đã kiểm

| slug lớp | finding IDs/biểu hiện | hạng cao nhất còn mở | nguồn lượt/SHA | phương án vá chung | phép kiểm đóng lớp |
|---|---|---|---|---|---|
| `ca-id-chi-do-mot-gia-tri` | F02: chỉ thử ID99 nên mutant chỉ nhận 99 sống | Không còn; lịch sử P3 | Review mã lượt 1, `da4e876` | **ĐÃ VÁ THẬT**: mở miền ca ID và biên hậu tố/tiền tố, thêm mutant thu hẹp miền | `reviewer_mutants.py`: nền 101/101, `rv_id_only_99` giết 6 ca và 3 đối chứng sống; cả 8 mutant reviewer `TỔNG: ĐẠT`. `probes.py`:100/100 ID00–99 bị bắt. Vòng mutant đăng ký được ghi ở bảng đo |
| `con-tro-trong-backtick-bi-cong-khac-doc` | Con trỏ ca trong bảng bị doc-claims hiểu sai | Không tái mở | Lịch sử r9/Q0 | Giữ sáu khối protocol đã sửa | N2 bằng byte; doc-claims H/base `ok:true`, flags rỗng; 392 advisory không thêm/mất khi bỏ số dòng |
| `khoa-khong-neo-vi-tri-va-duy-nhat` | Địa chỉ, tính duy nhất và phần đầu tệp | Không tái mở trong định nghĩa đơn vị | Lịch sử đặc tả/Q2 | Giữ địa chỉ, băm, hiển thị và đếm cùng loại | N5:7/7; bản sao đứng riêng 7/7 đỏ; phần đầu 10/10 đỏ; mutant rút mất khối ngắn ở phần đầu bị giết. Không gộp slug này với P2 dưới đây |

Đối chiếu riêng chuỗi review mã: U=2 lớp trước, F=1 lớp được vá thật; một lớp chuyển phạm vi theo chủ kho, không tính vào F. Ngoài hai lớp của review mã, lớp hồ sơ nâng trần từ review đặc tả r10 được kiểm lại là **VÁ HỜ**: đã có khối trong spec và đủ trường trong lease, nhưng lease chưa chép nguyên khối như r11 yêu cầu. Không tự giảm hạng, đổi slug hay miễn P3. Sửa câu giới hạn r11 cũng giải quyết biểu hiện “VÁ SINH LỖI MỚI” mà review r10 chỉ ra: K01 có bản sao dính chữ vẫn có thể đỏ do chốt ID.

### (ii) Lớp chuyển phạm vi/nợ kế nhiệm — không phải ĐÃ VÁ THẬT

| slug lớp | finding IDs/biểu hiện | hạng lịch sử | nguồn lượt/SHA | phương án chung và thẩm quyền | phép kiểm/giới hạn |
|---|---|---|---|---|---|
| `phep-dem-ban-sao-khong-phu-ca-tep` | F01.a–d: bản sao nguyên byte dính chữ/biên chỉ khoảng trắng/đoạn nối/HTML giữa dòng không thành đơn vị | P2, giữ lịch sử; không còn trong phạm vi wp1466 | Review mã lượt 1 `da4e876`, review đặc tả r10 `feb0b77` | Q3/E3 được chủ kho cấp trong PROMPT; issuecomment-7201538748; r11§0/§8.3; kế nhiệm **#1469**, nợ **INV-KHOA-BAN-SAO-DINH-CHU** | Phép đếm vẫn có giới hạn này. Dò đoạn nối trên cả 7 khóa: K02–K07 rc 0, K01 rc 9 bởi chốt ID. Không tuyên bố đã vá mã |

Ba điều kiện chuyển bảng (ii) đều được kiểm:

1. **Không còn lời hứa thuộc phần đã chuyển:** quét §0, M3, §8.3, N4, khối ADR và ADR thực; phép (3) chỉ hứa đếm đơn vị cùng loại. Câu r11 không còn suy ra toàn cổng xanh hoặc cấm mọi ca đỏ: các chốt ID, HTML, địa chỉ/băm/hiển thị và không đo được vẫn áp dụng. N1 xác nhận ADR thực bằng byte khối đã duyệt.
2. **Nợ có tên trong ADR:** `INV-KHOA-BAN-SAO-DINH-CHU` hiện diện ở phần Q3 và Nợ, giới hạn được nói thẳng.
3. **Có thẩm quyền và packet kế nhiệm:** Q3/E3 và #1469 do chủ kho xác nhận trong PROMPT, phù hợp r11; không cần xin lại. Không xác minh comment qua mạng trong lượt offline này.

## BẢNG SĂN

Lệnh có `out/...` chạy từ thư mục chứa PROMPT; số rc dưới đây là của cổng được thử, không phải rc của bộ probe. `probes.json` lưu toàn bộ 180 đầu vào theo tên, kỳ vọng và output. Các phép đo helper được phân biệt với CLI trong dữ liệu, không đánh đồng cả 180 lượt là CLI.

| Hướng độc lập / giả thuyết | Lệnh đã chạy | Output thật (rút gọn) và kết luận |
|---|---|---|
| 1. Sai byte hoặc sai số Cưỡng chế trong ADR | `python3 -B out/independent.py` | `N1 BYTE_EXACT True`; 14918 byte; sáu số `0,11,0,0,0,0`. Không phải lỗi |
| 2. Chèn đúng khối nhưng sai vị trí/đổi ngoài sáu khối | Cùng lệnh, tự dựng protocol từ base | `N2 BYTE_EXACT True`; numstat 46/2. Không phải lỗi |
| 3. Hằng khóa có thể tự nhất quán nhưng băm sai | Cùng lệnh, parser độc lập không import parser/mask sản phẩm | `N5 7/7 tự băm = khoa = INV_KHOA_PROTOCOL`; mỗi bản 1. Không phải lỗi |
| 4. Chuẩn hóa text có làm mất thay đổi byte? | `python3 -B out/probes.py` | `raw-byte total35 matched35`: CR/TAB/NBSP/BOM/U+2028 trên 7 khóa đều rc 9. Không phải lỗi |
| 5. Địa chỉ trùng hoặc đổi tiêu đề cha | Cùng lệnh, nhóm `heading-path` | 3/3 khớp, đều rc 9. Không phải lỗi |
| 6. Nhân bản đứng riêng ở cuối tệp có bị bỏ sót? | Cùng lệnh, nhóm `copies` | 7/7 khớp, đều rc 9. Không phải lỗi trong định nghĩa cùng loại |
| 7. Khối trước tiêu đề đầu hoặc khối thứ hai ở phần đầu | Cùng lệnh, nhóm `preamble` | 10/10 khớp, rc 9; `rv_preamble_drop_short_blocks` giết 1 ca với 3 đối chứng sống. Không phải lỗi |
| 8. Biên dòng rỗng/EOF làm chặn oan? | Cùng lệnh, nhóm `blank-boundary`, `eof` | 5/5 thêm dòng rỗng vẫn rc 0; bỏ LF cuối rc 0. Đúng định nghĩa bỏ dòng rỗng cuối đơn vị |
| 9. Miền ID ngoài mẫu 99 có bị lọt? | Cùng lệnh, nhóm `id-domain`; `python3 -B out/reviewer_mutants.py` | 100/100 ID00–99 rc 9; `rv_id_only_99 → giết6ca đích ·3đối chứng khác họ còn sống`. P3 đã vá thật |
| 10. Biên tiền tố/hậu tố và chuẩn hóa ID có chặn oan? | Cùng hai lệnh, nhóm `id-boundary` và mutant riêng | 6/6 khớp; tên nợ, 3 chữ số, hậu tố ASCII xanh; mutant regex 1+chữ số, word-boundary, bỏ NFKC/Cf đều chết. Không phải lỗi |
| 11. Thu hẹp lời hứa có lặp lỗi r10? | `python3 -B out/probes.py`, nhóm `scope-debt`; đọc r11§8.3 và ADR | 7/7 đúng: K01 rc 9, sáu khóa khác rc 0 khi thêm đoạn nối. Không khẳng định mọi bản sao dính chữ đều xanh; bảng(ii) đủ 3 điều kiện |
| 12. Không đo được có âm thầm thành xanh? | Cùng lệnh, nhóm `input-error`, `unmeasurable` | rỗng/UTF8 hỏng đều rc 2 từ chốt nguồn cũ; helper báo `KHÔNG ĐO ĐƯỢC: phép che đổi số dòng`. Không xanh. Chưa dựng race giữa hai lần đọc |
| 13. Sổ/mã cũ bị đổi ngoài phạm vi dù test xanh | `python3 -B out/do-pham-vi.py ma out/base-packet_loop.py out/h-packet_loop.py`; tương tự `test`; `python3 -B out/so-dang-ky.py out/base out/h` | Cả hai `PHẠM VI [...]: ĐẠT`; `SỔ ĐĂNG KÝ: ĐẠT`; không mất/đổi mutant cũ, CASES giữ thứ tự |
| 14. ADR có mặt nhưng quên đăng ký §20 | `python3 -I -B exec-out/sc/do_n3_am.py out/h out/n3-cases` | Nguyên trạng 67/67, rc 0; bỏ dòng ADR-0068 rc 9. Không phải lỗi |

Các hướng cần payload đường dẫn, race/symlink và HTML độc hại chỉ được xem xét bằng lời theo chỉ thị chủ kho; không tự tạo payload. Đã đọc đường `resolve → relative_to → read_bytes`, UTF8 strict, mask/line-count và call site. Các fixture HTML/rào/comment/nguồn cũ và mới có sẵn được chạy qua suite thật; không suy từ đọc mã rằng mọi race hay mọi dạng Markdown đã được chứng minh an toàn. Reader chống race và cú pháp HTML ngoài định nghĩa là giới hạn/nợ kế nhiệm đã khai, không tự biến thành yêu cầu mới.

## Thẩm quyền, phạm vi và lịch sử ghi tệp

`authority-v2.log` ghi 20/20 điều kiện thẩm quyền/phạm vi cơ bản; phép so nguyên khối bổ sung phát hiện F03. Hai phép đo không đồng nghĩa: bộ 20 điều kiện chỉ kiểm có các khóa và trần 500, chưa kiểm nội dung sao chép. Các điều kiện cơ bản gồm: exact HEAD/base, lease revision 11/generation 3, commit lease `ca001f8…`, spec source/blob/hash, write_set và hash chuẩn hóa NFC+casefold, chủ kho/nhánh/căn cứ, thời hạn lease và khối nâng trần. Diff chỉ 4 tệp:+478−4, trong 4 commit, mode 100644; `git diff --check` sạch. Không có skip-ci trong commit message. Lease/ref là ảnh chụp được cấp; không chứng minh tình trạng máy chủ sau ngày chụp.

Handoff 1 thừa nhận đi vòng chốt ghi bằng git plumbing; handoff 2/3 dùng git apply. Trên exact H không thấy dấu vết nội dung vượt write set: không tệp thứ năm, ADR/protocol đúng byte, AST và sổ cũ giữ nguyên trong phạm vi cho phép. Điều đó không xác nhận rằng cách ghi lịch sử đã được phép và không xóa sự kiện đi vòng chốt. Giữ sự kiện cho audit của chủ kho. Handoff 4 do Opus 5.5 hoàn tất lời khai của Fable 5.2 theo E2; reviewer đã đo lại kết quả, không đồng nhất tác giả handoff với tác giả mã.

Sai sót của phép đo reviewer được giữ trong hồ sơ: `authority.log` ban đầu tính hash write set thiếu casefold nên 19/20; sửa đúng quy tắc rồi `authority-v2.log`20/20. Lifecycle có lượt dùng chung TMPDIR nên tranh khóa; chỉ đối chiếu các lượt có cùng đầu vào và ghi riêng lượt cách ly. Không quy các lỗi phép đo đó thành lỗi sản phẩm.

## BẢNG LỚP ĐÃ ĐÓNG/ĐÃ KIỂM

Xem bảng (i) và (ii) phía trên. `ca-id-chi-do-mot-gia-tri` ĐÃ VÁ THẬT; `phep-dem-ban-sao-khong-phu-ca-tep` chuyển phạm vi hợp lệ, không tính là vá; `thieu-khoi-nang-tran-kich-thuoc` VÁ HỜ ở bản chép lease và vẫn P3. Không phát hiện P0/P1/P2 còn mở trong phạm vi r11.

### thieu-khoi-nang-tran-kich-thuoc [P3] Lease nâng trần diễn đạt lại khối mà đặc tả yêu cầu chép nguyên

TỆP/DÒNG: `ops/specs/wp1466.md:724`, khối dòng 727–735; `ops/leases/wp1466-r11-g3-claude.yaml:79`–84 tại ref `origin/ops/wp1466-r11-g3-lease`/commit `ca001f8`; ADR0053 dòng 34–37. Đây là hồ sơ lease được giao để review, không phải tệp thứ năm của diff sản phẩm.

VẤN ĐỀ: r11 yêu cầu “lease cấp cho mã giao nộp chép lại nguyên khối”. H có +478 dòng nên đang sử dụng phần nâng trên 450. Lease có đủ bốn trường và quyền nâng 500 đã có, nhưng ba giá trị `can_cu`, `tran_cu`, `tran_moi` bị viết lại; thêm `ai_nang_ghi_chu`. Sau parse YAML vẫn khác, nên không chỉ là xuống dòng, kiểu quote hay comment. Handoff 4 nói lease chép khối ấy nhưng phép so nguyên khối chưa đạt. Đây là phần hồ sơ còn thiếu của cùng lớp P3 r10, không phải một lỗi thuật toán hay thiếu thẩm quyền mới.

CÁC BIỂU HIỆN CÙNG LỚP ĐÃ QUÉT: toàn khối của spec và lease, cả bốn trường bắt buộc, tập khóa, số trần, người nâng, căn cứ E2, điều kiện kích hoạt và lời khai trong handoff 4. `ai_nang` bằng nhau; ba giá trị khác; một khóa dư. Số cũ 6/450 và mới 6/500 không khác; không cáo buộc được cấp sai trần. Spec đã có khối đúng, còn bản chép lease chưa nguyên vẹn: nhãn **VÁ HỜ** cho toàn bộ lớp, không ghi thiếu toàn bộ khối như r10.

GỢI Ý VÁ: bản dữ liệu `HINT-lease.patch` chép khối spec sang bản lease thử, giữ nguyên mọi trường khác. Đây là gợi ý cho hồ sơ coordination/lease; không đưa lease vào write set bốn tệp của PR sản phẩm và không cần đổi mã H. Chưa áp vào ref nguồn. Quyền nâng trần đã có; không đề nghị xin lại hay gọi thêm Codex vượt 13/13.

ĐÃ THỬ NGHIỆM: `python3 -B out/nang_tran_compare.py` in `MAPPING_EQUAL False`, `VALUE_DIFF_KEYS ['can_cu', 'tran_cu', 'tran_moi']`, `EXTRA_KEYS ['ai_nang_ghi_chu']`; candidate `MAPPING_EQUAL True`, mọi trường ngoài khối giữ nguyên. `python3 -B out/test_lease_hint.py`: `git apply --check` và `git apply` trên fixture dưới out đều rc 0, `PATCH_FIXTURE_BYTE_EXACT True`. Log: `logs/nang-tran.log`, `logs/lease-hint.log`; dữ liệu đầy đủ: `nang-tran-comparison.json`.

ĐỘ TIN: cao về khác biệt nội dung và yêu cầu sao nguyên khối; ảnh hưởng chỉ ở tính đúng hồ sơ. Không làm mất quyết định E2 đã được chủ kho cấp. Reviewer không tự miễn P3 này hoặc gọi bản thử dưới out là bản vá đã giao nộp.
