# Review độc lập PR #452

**Kết luận: `changes_requested`. Có hai finding mới so với hồ sơ review được lưu trong kho.** Cả hai nằm ngay trong bằng chứng dùng để dựng kết luận bản 3: đếm đường dẫn bản thảo thành mỏ neo đóng băng, và đếm thiếu khai báo nâng trần thành tuân thủ trần. Tôi không tính các lỗi bộ đếm đã được reviewer trước nêu là phát hiện mới.

Đây là bằng chứng rằng lượt khác nền này bổ sung được phản chứng; **không chứng minh quan hệ nhân quả “khác nền làm review tốt hơn”**. Khác revision, chỉ một lượt thử, và transcript đầy đủ của bốn reviewer trước không có trong kho. “Bỏ sót” dưới đây có nghĩa là không thấy phản chứng ấy trong hai verdict được lưu và §9, không phải đã kiểm toàn bộ transcript.

## Mỏ neo và phạm vi

- Reviewed SHA: `76318fa106019611fbd5ea9ec6e2553bb7773faf`.
- Reviewed tree: `9be094fee7c1e1a63f8df4526cb95f86484f1f25`.
- Base của bảng §0 / diff: `c03a409afc17ee3b8287cd1a88b0ed3f9ba02fab`.
- Tệp review: `ops/PHAN_BIEN_QUY_TRINH_BUILD_REVIEW_20260905.md`; SHA-256 `b38a11ef9301475300b6505bdea4ba279f8ab22f50cfed5fd4a435b9e7b8a8db`.
- Authority: yêu cầu trực tiếp của người dùng và toàn bộ `prompt.snapshot`; SHA-256 prompt `d0e56f1a0ce68702c8d0bf8c5feff31ebad79e813e19b8d8a2af6779705e7a53`.
- Đây là review tài liệu theo chỉ thị trực tiếp, không tự tạo Packet/lease/revision/generation. Hai receipt trước cũng khai việc này không có lease. Write set: duy nhất báo cáo `VERDICT.md`; thử nghiệm trong `/tmp/pr452-review/`.
- Role: reviewer độc lập; provider `openai_codex`; model GPT-6 / Codex theo danh tính phiên; execution surface Codex service qua API và công cụ shell; transport `machine`. Không chạy qua launcher, không có launcher receipt xác minh danh tính; không tự cấp approval/land authority.
- Phạm vi docs-only thuộc `routine`; người dùng chỉ định review khác nền. Chỉ đọc mã cổng và đột biến bản sao để kiểm lập luận, không sửa mã sản phẩm.
- Clone detached, sạch trước review, `shallow=false`, `git rev-list --count HEAD = 1683`, remote đúng `ducthangho/tra-luat`. Chưa readback PR head trên GitHub: verdict chỉ neo exact clone đã được giao.

## H1 — Đo lại toàn bộ bảng §0

Tôi dựng riêng hai snapshot bằng `git archive`, đọc YAML và đối chiếu với phép grep của tài liệu. **Mốc chuẩn của bảng là base, không phải HEAD**; thêm hai receipt ở PR này không làm số lịch sử sai.

| Đại lượng | Kết quả tại base | Kết luận |
|---|---|---|
| Receipt / có `packet_id` / giá trị ID khác nhau | 57 / 56 / 15 | KHỚP số đếm; 15 là số chuỗi ID, không chứng minh 15 packet |
| Thời lượng: n / min / median / mean / max | 9 / 835,6 / 922,422 / 1043,746889 / 1516,2 giây | KHỚP sau làm tròn; đây là 9 giá trị trích từ receipt, không phải mẫu ngẫu nhiên của mọi lượt |
| Ubuntu success 21m52s, 25m14s | Chú thích `ci.yml` ghi đúng hai giá trị | KHÔNG ĐO ĐƯỢC run thực; chỉ KHỚP văn bản nguồn |
| Dispatch cancelled 25m19s, 25m09s, 45m17s | Chú thích ghi đủ ba giá trị | KHÔNG ĐO ĐƯỢC run/job thực và nền nào chạm trần |
| ~20 phút × ~13,6/ngày ≈ 8.100/tháng | Tính với 30 ngày = 8.160, phù hợp làm tròn | KHỚP phép tính; tần suất/billing thực KHÔNG ĐO ĐƯỢC |
| Hạn Free 2.000 / cạn ~ngày 11 / cạn thật 12-08 | Nguồn là chú thích; 2.000/(20×13,6) = 7,35 ngày | “Ngày 11” LỆCH về số học; hạn tài khoản và ngày cạn thực KHÔNG ĐO ĐƯỢC. Đây là lỗi cũ §9 #14/#23, không finding mới |
| Verdict | 33 changes_requested, 18 approve, 1 blocked, 5 giá trị khác | KHỚP; tổng 8 cách viết; 52/57 = 91,228% |
| `luot` | 7, đa tập 1,1,2,2,3,4,4 | KHỚP |
| `review_rounds_used` 10/57 | 4 receipt có khóa đúng tên trong `so_sach_ngan_sach`; 2 receipt khác có cặp khóa trước/sau | LỆCH: 4/57 theo khóa chính xác; 6/57 nếu nhận hai alias trước/sau. Không phải 10/57 |
| `codex_review_calls_used` 2/57 | 0 khóa, kể cả duyệt cấu trúc lồng | LỆCH: 0/57; hai tệp chỉ nhắc tên trong văn xuôi |
| `codex_executor_calls_used` 0/57 | 0 | KHỚP |
| `spec_hash` / `spec_sha256_required` / `spec_sha256` / `spec_path` | 10 / 29 / 5 / 48 | KHỚP số tệp có trường |
| Union bốn trường / tổng lease / tỷ lệ | 50 / 82 / 60,9756% | KHỚP phép đếm, **không khớp nhãn “đặc tả đóng băng”**: finding N1 |

Ở HEAD: 59 receipt, 58 có packet_id, 16 chuỗi ID, 9 có luot, 35 changes_requested, 18 approve, 1 blocked, 5 biến thể; lease và mẫu thời lượng không đổi.

Các đại lượng §0 bỏ sót mà có ý nghĩa với kết luận:

- **6/50** lease trong tử số “có neo” không có trường băm: 3 chỉ trỏ bản thảo, 3 có `spec_path: null` — N1.
- **41/82** không có `review_rounds_limit`; 23 khai 2; **18 khai >2**, trong đó 17 không có khối `nang_tran` — N2.
- Độ phủ kiểm lớp: 13 lease schema v2, 69 v1. `_kiem_lop_review` chấp nhận 13/13 v2 trong phép gọi trực tiếp; v1 đi nhánh legacy. Đây là độ phủ của phép kiểm hiện tại, không phải tỷ lệ vi phạm. Không kết tội 69 lease cũ bằng luật mới.

Lệnh đã chạy: `python /tmp/pr452-review/measure.py` (rc=0). Script và snapshot còn trong thư mục tạm; lệnh đo độc lập các đại lượng mới nằm ngay dưới từng finding.

## N1 — P2: Đường dẫn bản thảo bị nâng thành mỏ neo đặc tả đóng băng

**Vị trí:** tệp review dòng 31, 49–50, 86, 105 và MVP-2 dòng 446–449.

Tài liệu nói bốn tên là một khái niệm và 50/82 lease “neo được một đặc tả đóng băng”. Nhưng ba lease `wp55-r4-review-di-tru-codex-20260815.yaml`, `wp55-r4-review-rebase-codex-20260816.yaml`, `wp55-r4-review-viet-lai-codex-20260815.yaml` khai `spec_status: ban_thao_chua_duyet`, chỉ có `spec_path`, và nói rõ **KHÔNG khai spec_hash làm mỏ neo** vì đặc tả còn thay đổi khi điền base SHA.

Lần sửa trước loại ba tệp này khỏi phép đếm `spec_hash`; lần sửa theo “khả năng” lại nhận chúng qua `spec_path`. Đây là phản chứng mới đối với phép union, không phải lặp lỗi grep comment đã ghi ở §9. Một địa chỉ cho biết tìm bản thảo ở đâu; nó không định danh byte đã được duyệt. Còn ba lease `plat-x5-exec-1-codex-20260820.yaml`, `plat-x5-exec-1r2-codex-20260820.yaml`, `plat-x5-exec-1r3-codex-20260820.yaml` được đếm chỉ vì có khóa `spec_path`, nhưng giá trị YAML là `null`; ngay cả địa chỉ cũng không có.

**Hậu quả:** chủ kho có thể giữ nguyên việc thiếu đặc tả đóng băng vì tin đó chỉ là khác tên trường; MVP-2 khai “bắt oan 40/82 lease đang làm đúng” cũng chưa được chứng minh. Số đo đứng được là **44/82 có ít nhất một trường băm không rỗng trong ba tên**, chưa phải 44 lease tuân thủ: còn phải kiểm băm/phiên bản/authority.

**Sửa ở đâu và thế nào:** sửa định nghĩa tử số ở §0, rồi truyền sang §1 và MVP-2. Tách `có locator`, `có định danh bất biến`, `đã kiểm định danh và thẩm quyền`; chỉ ánh xạ các trường thật sự cùng ngữ nghĩa. Không sửa hồi tố ba lease, vì chúng đang khai trung thực mục đích riêng.

**Ca khóa và nguy cơ bản vá:** dùng ba lease bản thảo và ba lease locator null trên làm đối chứng âm cho “đã đóng băng”, và một lease đã kiểm hash thật làm đối chứng dương. Đột biến thay băm bằng đường dẫn còn tồn tại phải làm phép phân loại mất trạng thái “đã kiểm”, không được giữ xanh. Nguy cơ: siết duy nhất tên `spec_hash` lại bắt oan alias băm hợp lệ, hoặc suy băm sai chỉ vì kiểm nhầm revision hiện tại.

**Lệnh tái hiện (đã chạy cùng logic trên cả base và HEAD; rc=0):**

```bash
python -B - <<'PY'
from pathlib import Path
import yaml
keys = ('spec_hash', 'spec_sha256_required', 'spec_sha256')
rows = [(p, yaml.safe_load(p.read_text())) for p in Path('ops/leases').glob('*.yaml')]
print('co_truong_bam', sum(any(d.get(k) for k in keys) for p,d in rows))
for p,d in sorted(rows):
    if d.get('spec_path') and not any(d.get(k) for k in keys):
        print(p.name, d.get('spec_status'), d.get('spec_note'))
    elif any(k in d for k in (*keys, 'spec_path')) and not any(d.get(k) for k in keys):
        print(p.name, 'locator_null', d.get('spec_path'))
PY
```

## N2 — P1: Không có `nang_tran` bị tính thành không vượt trần

**Vị trí:** tệp review dòng 87–89, 105–109; nhật ký dòng 567. Nguồn phép suy hiện rõ ở verdict lượt 2, B3: “nang_tran: 1/82 ⇒ 81/82 giữ trần”.

`nang_tran` là khai báo ngoại lệ có thẩm quyền. Không khai nó có ít nhất hai khả năng: không cần nâng, hoặc đã vượt/nới mà thiếu khai báo. Phép lấy 82−1 không phân biệt hai khả năng, và còn tính **ngoại lệ có khai báo** như phần bù của “tuân thủ”, trong khi ngoại lệ được duyệt có thể hoàn toàn hợp lệ.

Đo trường liên quan trực tiếp: **41** lease không khai limit; **23** khai 2; **18** khai từ 3 đến 7; **17/18** không có `nang_tran`. Có **6** lease tự ghi `review_rounds_used_truoc_luot_nay > 2`. Các số này bác cách suy 81/82; **không được đảo thành kết luận 17 hay 18 vi phạm**, vì còn ngày hiệu lực ADR, miễn trừ/authority, đơn vị vòng và nhiều lease của cùng công việc.

Đây là lỗi thứ ba cùng họ ở H2: đổi tên biến thành “vi phạm” nhưng vẫn đo sự có mặt của một khóa, rồi coi phần không biết là tuân thủ. Tuyên bố “luật không cổng vẫn ràng buộc được 61–99%” không có cơ sở từ hai tử số này. Quy tắc “chỉ ô thứ ba là việc” còn bỏ qua trường hợp **chưa đo được**, cũng như cổng đã có nhưng độ phủ/răng chưa được kiểm.

**Hậu quả:** ưu tiên cải tiến dựa trên mức tuân thủ gần 99% giả; thiếu ghi nhận vi phạm càng nhiều thì hệ thống càng trông tốt. Đây là lỗi ở kết luận trung tâm, không chỉ sai một tỷ lệ.

**Sửa ở đâu và thế nào:** rút 81/82 và 61–99% khỏi §1. Định nghĩa quần thể áp dụng theo PR/Packet và ngày hiệu lực, phân biệt tuân / vi phạm / chưa đủ bằng chứng; ngoại lệ đã được duyệt nằm đúng ô tuân có điều kiện. Đánh giá nhu cầu đo và sửa cổng ở cả ba ô, không lấy “có cổng” làm lý do loại khỏi công việc.

**Ca khóa và nguy cơ bản vá:** dùng lease thiếu limit và lease limit>2 thiếu `nang_tran` làm ca không được tự kết luận tuân; dùng ngoại lệ có đủ authority làm ca không được tự kết luận vi phạm. Đột biến phép phân loại “thiếu trường ⇒ tuân” phải chết. Nguy cơ: sửa bằng `limit>2 ⇒ vi phạm` sẽ kết tội hồi tố, đếm trùng revision và phạt ngoại lệ hợp lệ.

**Lệnh tái hiện (rc=0):**

```bash
python -B - <<'PY'
from pathlib import Path
from collections import Counter
import yaml
rows = [(p,yaml.safe_load(p.read_text())) for p in Path('ops/leases').glob('*.yaml')]
print(Counter(d.get('review_rounds_limit','THIEU') for p,d in rows))
high = [(p,d) for p,d in rows if isinstance(d.get('review_rounds_limit'),int)
        and d['review_rounds_limit'] > 2]
print('tren_2',len(high),'khong_nang_tran',sum('nang_tran' not in d for p,d in high))
for p,d in sorted(rows):
    n=d.get('review_rounds_used_truoc_luot_nay')
    if isinstance(n,int) and n>2: print(p.name,n)
PY
```

## H3 — Cổng có răng trong các đột biến đã đo

**Hướng này sạch trong sáu phép thử đã chọn:** không thấy cổng nào mất khả năng đỏ ở ca đích. Không suy thành mọi cổng/đường đi đều được bảo vệ.

| Cổng | Đột biến chỉ trên bản sao | Bằng chứng |
|---|---|---|
| `RC_DOCTRINE` | Tắt nhánh xử lý `dinh`; chạy fixture doctrine có sẵn | Đối chứng sạch đạt; ca vi phạm đỏ bằng AssertionError: kỳ vọng rc=6, thực rc=0 |
| `bien-nhan` | Tắt kiểm số biên nhận tối thiểu | Ca thiếu receipt đỏ đúng assertion kỳ vọng rc=11, thực rc=0; ca đủ receipt vẫn đạt |
| `RC_LOP` | Tắt điều kiện so lớp hiệu lực với lớp tính được | `t76` đỏ: reviewer routine lọt chốt; control đạt |
| `t26` | Thêm một dòng vô hại vào verdict, giữ receipt | rc=1, 0/1, thông báo LỆCH BĂM |
| `t27` | Bỏ các hàng bảng cho verdict lượt 2 | rc=1, 0/1, báo thiếu verdict trong cột Mục lục |
| `t33` | Thêm một khóa top-level YAML không hợp lệ vào workflow | rc=1, 0/1; actionlint báo unexpected key tại đúng dòng thêm |

Bộ control `t26/t27/t33/t76`: **4/4, rc=0, bỏ qua=0**. Control packet: **4/4**. Mỗi mutant packet chỉ làm đỏ ca đúng họ; ba đối chứng còn lại đạt. Lỗi được kiểm qua nội dung assertion, không chỉ qua rc khác 0. Script điều phối packet trả rc=0 vì ghi lại kết quả phản chứng; điều đó không có nghĩa mutant đạt.

Lệnh tái hiện và artifact ngoài repo:

```bash
python -B /tmp/pr452-review/probes.py
python -B /tmp/pr452-review/packet-probes.py
```

Script tạo tên thư mục riêng cho từng mutant; tắt ghi bytecode; không tự soạn chuỗi khai thác. Log: `/tmp/pr452-review/probes.log`, `/tmp/pr452-review/packet-probes.log`.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đối chiếu từng finding trong **verdict lượt 2 được lưu**, không giả vờ có transcript đầy đủ. “Đã vá” dưới đây chỉ nói phần được chỉ, không duyệt toàn tài liệu.

| Finding cũ | Trạng thái tại HEAD và bằng chứng |
|---|---|
| A1 — quét theo lớp | **CHƯA VÁ** đầy đủ: §0 vẫn 10/57 và 2/57; đọc YAML lồng cho 4 khóa exact / 0, hai alias thêm 2 receipt |
| A2 — quên §2/§5 | **VÁ HỜ**: có cập nhật bảng/khuyến nghị, nhưng F1 còn câu “dồi dào” trước đoạn rút, M1 còn khẳng định nhân quả trước §6 rút lại; không tính lỗi mới |
| A3 — 44% | **ĐÃ VÁ THẬT về số học** thành 40/82=48,8%; ngữ nghĩa “đang làm đúng” vẫn bị N1 bác |
| A4 — đếm 57 vòng | **VÁ HỜ**: §6 rút cách gọi vòng; §9 #10 vẫn viết “52 vòng phân biệt” rồi tự nhắc lệnh cấm gọi thế |
| A5 — ngày 11 | **CHƯA VÁ** ở §0; 2.000/(20×13,6)=7,35; §9 nói đã sửa nhưng dòng chính vẫn còn |
| A6 — không có hiện vật | **ĐÃ VÁ THẬT phần hiện vật**: hai verdict + hai receipt + mục lục; t26/t27 control và mutant đều có bằng chứng |
| A7 — trường đo tự khai | **CHƯA VÁ** thành cơ chế: F3/MVP-4 vẫn là đề xuất; chưa có thực thi để đo hiệu lực |
| B1 — hai tập không giao | **ĐÃ VÁ THẬT phần rút luận cứ** ở §1; không còn dùng bảng 8 ADR để kết luận 9 mục |
| B2 — ADR-0038 có cổng | **ĐÃ VÁ THẬT phần thừa nhận**; kiểm hàm lớp với 13 v2 và mutation t76 xác nhận có logic cưỡng chế |
| B3 — 61% và 81/82 chứng minh tuân | **VÁ SINH LỖI MỚI**: thành nền của kết luận bản 3; N1/N2 phản chứng hai tử số |
| B4 — “phần lớn” | **ĐÃ VÁ THẬT phần lượng từ** thành thiểu số 9/30, không chứng minh độ phủ cổng |
| B5 — thứ tự MVP | **VÁ HỜ**: MVP-4 thêm, vẫn tự gọi số một trong danh sách xếp rẻ-trước; chưa đo ưu tiên rủi ro |
| B6 — thiếu đề xuất gốc | **CHƯA VÁ** trong diff sáu tệp: chưa bổ sung hiện vật 13 mục + 10 câu hỏi; không kiểm được trích dẫn với nguyên bản |
| B7 — quyền ngoài kho | **ĐÃ VÁ THẬT phần cảnh báo** ở §1; activation/branch protection thật KHÔNG ĐO ĐƯỢC từ clone |

Không tái đóng gói A1/A5 hoặc các chỗ rút lời chưa truyền hết thành “Codex bắt thứ bốn người bỏ sót”: chính các hồ sơ trước đã chỉ chúng.

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

**Đo được:** số đếm tại hai Git snapshot; hai phản chứng mới; sáu phép đo răng; exact SHA/tree và hash tài liệu. Môi trường Linux, Python 3.11.15, Git 2.43.0, PyYAML 6.0.1, actionlint 1.7.7; không có shellcheck trên PATH. Clone kiểm doc gate được ghim `core.abbrev=7`.

| Lệnh / phép kiểm | Trạng thái | Evidence |
|---|---|---|
| `git diff --check c03a409 HEAD` | passed, rc=0 | Không lỗi whitespace trong diff sáu tệp |
| `python /tmp/pr452-review/measure.py` | passed, rc=0 | Hai snapshot, 57/59 receipt và 82/82 lease; số chi tiết H1 |
| `python -B ops/lease_publish_test.py` trong archive HEAD | passed, rc=0 | 121/121, đã chạy=121, bỏ qua=0; `/tmp/pr452-review/lease-suite.log` |
| Control và mutation t26/t27/t33/RC_LOP | passed với tư cách phép thử phản chứng | Control rc=0; cả bốn mutant rc=1 đúng lý do; không skip |
| Control và mutation doctrine/bien-nhan | passed với tư cách phép thử phản chứng | 4 control đạt; mỗi mutant làm đỏ đúng ca đích |
| `python -B .claude/dev/packet_loop_test.py` trong archive HEAD | **failed**, rc=1 | Nền 267/278, bỏ qua=0, tổng 11 lỗi; rig archive thiếu Git/lịch sử/run evidence. Không gọi đây là hồi quy PR |
| `python -B scripts/tl.py doc-claims-check --strict` trong clone Git cùng HEAD | passed, rc=0 | `ok=true`, 106 files, flags rỗng; **roots mặc định không chứa ops**, nên không chứng minh bảng đang review đúng |

Tôi đã chạy lại baseline packet trên clone Git để phân biệt lỗi rig; kết quả được ghi bổ sung bên dưới. Một lệnh import đo nhanh có sinh bytecode `ops/__pycache__/lease_publish.cpython-311.pyc` trong clone review; đã xóa artifact đó ngay, không đổi nguồn/index. Các phép thử khác chạy ở bản sao hoặc tắt bytecode.

**KHÔNG ĐO ĐƯỢC:** tỷ lệ tuân thủ thật của toàn kho; thẩm quyền ngoại lệ qua GitHub; số review đã chạy nhưng không để receipt; transcript đầy đủ bốn reviewer; đề xuất gốc; billing/Actions run thực; PR head hiện tại ngoài clone; Windows và parity Windows–Linux. Không dùng kết quả Linux thay các phần ấy.

**not_run:** full runtime selftest, release gates, don_ref_chot_test.sh, test Windows, gọi LIVE, merge/deploy. **skipped:** không tính phép nào bị bỏ qua là pass; các bộ test đã kết thúc ở trên báo bỏ qua=0. Đây là review tài liệu và probes theo chỉ thị, không phải chứng nhận release/CI của PR.

**Đo lại rig đã hoàn tất:** `PYTHONDONTWRITEBYTECODE=1 python /tmp/pr452-review/clone-baseline.py` → **passed, rc=0, 278/278, non_pass={}** (`/tmp/pr452-review/clone-baseline.log`). Cùng mã HEAD, baseline chạy trên clone có Git thay cho archive: cả 11 lỗi trước không tái hiện. Tôi không khai đã chạy lại toàn bộ vòng mutation của suite trên clone; sáu probes H3 có kết quả riêng ở trên.

Kiểm cuối: HEAD/tree vẫn khớp các OID đầu báo cáo; `git status --short` chỉ có `?? VERDICT.md`. Không commit, push hoặc sửa tệp nguồn.

verdict: changes_requested
