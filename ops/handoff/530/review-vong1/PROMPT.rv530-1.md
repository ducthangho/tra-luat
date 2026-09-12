# CROSS-REVIEW — PR #532 / packet #530 `CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE` — vòng 1/10

Bạn là reviewer KHÁC NỀN cho một work packet của protocol đa phiên trong kho `ducthangho/tra-luat`.
Phiên thi công là `claude`; bạn là `codex`. Nhiệm vụ: **ĐO**, không phải đọc.

## Nơi bạn đang đứng

| thứ | đường dẫn |
|---|---|
| cây làm việc, detached đúng head của lượt | `cay/` — `git -C cay rev-parse HEAD` phải là `a1c7d7ffbac710346400650b94e2d2a8035f62b5` |
| **gương git ĐẦY ĐỦ** (412 ref: 8 heads + 365 remotes + 39 tags; master 2175 commit; **không nông**) | `kho-guong.git/` — đã là `origin` của `cay/` |
| nhị phân + gói offline | `cong-cu/` — `actionlint` (1.7.7), `shellcheck` (0.9.0), `actionlint-1.7.7-goi.gz` |
| bảng lời khai của phiên thi công | `BANG_KHAI.md` |
| bộ trích số (và giới hạn của nó) | `trich_so.py` |
| **nơi bạn GHI verdict** | `ket-qua/VERDICT.md` |

Gương có đủ ref nên bạn **tra cứu được lịch sử**: `git -C kho-guong.git show <sha>:<path>`,
`git -C kho-guong.git log`, các nhánh `refs/remotes/origin/ops/handoff-512-luot7` (bộ đo CŨ),
`refs/remotes/origin/ops/handoff-530` (hồ sơ + log của lượt thi công), `refs/remotes/origin/master`.

Bật công cụ trước khi chạy bất cứ cổng nào:

```bash
export PATH="$PWD/cong-cu:$PATH"
actionlint --version   # phải in 1.7.7
shellcheck --version   # phải in 0.9.0
```

**`shellcheck` PHẢI có mặt.** Thiếu nó thì `t137` và `t159` fail-close `KHÔNG ĐO ĐƯỢC` và bạn sẽ
thấy một "hồi quy" không tồn tại. Đây là điều kiện đo, không phải một mẹo.

## Việc packet này làm

Packet là một **PORT** của kiến trúc đã LAND ở packet `#513` (`ops/nhanh_don_duoc_test.py` trên
master), không phải một thiết kế mới.

Vấn đề gốc (lớp `F6`, mở qua năm vòng review của PR #512): bộ đo đột biến chạy NGOÀI tiến trình và
chỉ đọc **CHUỖI** trên stdout, nên nó phải **SUY** xem một mutant chết vì chốt của ca đích hay vì
một ngoại lệ VÔ CAN. Ba lượt vá, ba lượt cùng một hình dạng lỗi; lý do là CẤU TRÚC — hai miền chuỗi
*"thông điệp assertion"* và *"tên lớp + thông điệp"* **GIAO NHAU** (`t96: ` là tiền tố tên ca bình
thường, có sẵn trong cây), nên không có biên nào để siết.

Bản vá thay phép đo trên chuỗi bằng một **KÊNH JSONL** mang NHÃN do `main()` gán theo **LỚP NGOẠI LỆ
THẬT**. Đọc `git -C cay show HEAD --stat` và hai thông điệp commit (`540b6f1`, `a1c7d7f`) — chúng khai
khá chi tiết việc đã làm và các phép đo.

Đặc tả **đóng băng revision 3**, sha256 `47c3b1fe70da6976cf802436fa8883c2ba48ac8f706b3d9ec103deaeb5f37778`:

```bash
git -C kho-guong.git show refs/remotes/origin/ops/handoff-512-luot7:ops/specs/CHAM-DOT-BIEN-MIEN-NHIEM-LEASE-SUITE.md | sha256sum
```

Đặc tả là **nguồn của tiêu chí `M1`…`M6` và `A1`…`A8`**. Nó ĐÃ ĐÓNG BĂNG: bạn **không sửa** nó, và
nếu bạn thấy đặc tả tự mâu thuẫn thì đó là một finding, không phải một chỗ để tự nới tiêu chí.

## PHẠM VI — sự thật, không phải một danh sách việc

- Write set của packet là **MỘT** đường: `ops/lease_publish_test.py`. Không ký tự đại diện.
- **NGOÀI phạm vi, cứng:** `ops/lease_publish.py` (mã sản phẩm, `S3`) · `.github/workflows/**` ·
  `ops/chay_lease_publish_test.sh` · `ops/nhanh_don_duoc_test.py` (bản mẫu đã land) ·
  `.claude/dev/ci_dang_ky_test.py` và `.github/workflows/ci.yml` (packet `#463` đang giữ hai đường
  này `exclusive`).
- Phát hiện thuộc đường **ngoài** write set: **vẫn báo**, nhưng đánh dấu là **NỢ**, không phải một
  finding đòi PR này sửa.
- Hai trần đã được chủ kho nâng, ghi ở lease `…exec-1r2…`: `S2` 300→**1000** (hiện `+802`, **dư 198**)
  và `S6` 2→**10** vòng. Một bản vá đẩy `numstat` quá **1000** là `S2` ⇒ phiên thi công phải DỪNG.

**TÔI KHÔNG LIỆT KÊ TRƯỚC CÁC LỚP LỖI CHO BẠN, VÀ ĐÓ LÀ CÓ CHỦ ĐÍCH.** Kho này đã đo được rằng
*"danh sách bạn giao cho reviewer trở thành TRẦN của họ"*. Bạn **tự phân lớp**. Verdict phân theo
**LỚP lỗi**, không theo từng thể hiện riêng lẻ.

## BỐN CHỖ TÔI TỰ BÁC TRONG LƯỢT THI CÔNG — mỏ neo cho bạn đo tiếp, không phải lời bào chữa

1. **"Hai điểm vật hoá `dich` là hai chốt ĐỘC LẬP"** — SAI. Đo riêng từng nửa: gỡ nửa nào cũng `rc=0`
   và **0** control lệch (nửa còn lại HẤP THỤ); chỉ gỡ **cả hai** mới `rc=1` và control dương lệch
   `GIET → KHONG_GIET`. Chúng là một bộ **TƯƠNG ĐƯƠNG** ⇒ mục `M5` ấy đo **đúng một** thứ.
2. **`A2` ở commit `540b6f1` chỉ nằm trong docstring** ⇒ nó **KHÔNG TỒN TẠI**. `a1c7d7f` biến nó
   thành ca chạy thật VÀ đo chiều ngược.
3. **Script đo delta bản đầu KHÔNG ĐO GÌ mà vẫn trông như thành công** — nó gọi `/usr/bin/env time -f`
   mà container không có GNU `time`; mỗi vế chết ngay, log còn 1 dòng, script in ra bình thường.
4. **9 chốt fail-close của bộ chấm CHƯA có control phân biệt** — khai trong `CHOT_CHUA_CO_CONTROL_512`,
   **không** đếm là đã đo.

Bốn chỗ này đã được khai. Việc của bạn là xem **chúng đã được khai ĐÚNG MỨC chưa**, và tìm những chỗ
**chưa** được khai.

## MỘT DỮ KIỆN ĐÃ CÓ QUYẾT ĐỊNH — đừng đọc thành khuyết tật chờ vá

Ba ca mới làm suite chậm **×3,06** (`104,4s`/155 ca → `319,4s`/158 ca), trong đó `t125` một mình
**+107,4s** vì HAI lượt con LỒNG của nó cũng chạy `t161`/`t162`/`t163`. Đường giảm đã biết —
*đừng chạy ba ca mới trong hai lượt con của `t125`* — **ĐỔI phạm vi `t125`**, nên nó bị
`ngoai_pham_vi` #5 của đặc tả chặn (*không đổi ngữ nghĩa 155 ca hiện có*). Chủ kho đã được báo con số
và **chọn giữ nguyên**. Bạn vẫn được nêu nếu bạn đo ra điều **MỚI** (ví dụ: một cách giảm KHÔNG đổi
ngữ nghĩa, hoặc một trần thời gian sắp bị vượt).

## NHIỆM VỤ — ĐO, theo thứ tự này

### 1. Chạy các cổng, đòi BẰNG CHỨNG DƯƠNG

```bash
cd cay
python3 ops/lease_publish_test.py --chi-ca=t161    # A4: đòi giết 16 · không giết 0 · KDD 0
python3 ops/lease_publish_test.py --chi-ca=t162    # A1: đòi 10/10 đúng phân hạng
python3 ops/lease_publish_test.py --chi-ca=t163    # A2+A3+A8: đòi 7/7
AL_VER=1.7.7 AL_GOI=../cong-cu/actionlint-1.7.7-goi.gz bash ops/chay_lease_publish_test.sh; echo "rc=$?"
python3 .claude/dev/packet_loop.py doctrine-scan --root .   ; echo "rc=$?"
python3 .claude/dev/packet_loop.py adr-song      --root .   ; echo "rc=$?"
git diff --numstat dc02c9beed42bd2ea44a80a2e34e1bbe3acfc6c5 -- ops/lease_publish_test.py
```

`A5` đạt **CHỈ KHI** có ĐÚNG **ba** dòng `lease_publish: N/N đạt … bỏ qua=0` (lượt CHA + `[A]` + `[B]`,
**hai số BẰNG NHAU** ở mỗi dòng), **0** dòng khớp `^  ĐỎ  `, và `rc=0`. **`rc=0` một mình là cổng có
thể bị lừa** — kho này đã trả giá đúng chỗ đó.

Wrapper mất ~3,5 phút. **ĐỪNG sửa `ops/lease_publish_test.py` trong lúc một lượt suite đang chạy**:
các ca sinh tiến trình con đọc tệp **từ đĩa** (18 chỗ `sys.executable`), nên một lần sửa giữa lượt làm
phép đo vô nghĩa **mà không báo gì**. Phiên thi công đã sập vì đúng chuyện này hai lần.

### 2. ĐO RĂNG bằng cách ĐỘT BIẾN BẢN VÁ — đây là phần chính

Đừng đọc code rồi kết luận một chốt có răng. **Gỡ chốt ra và đòi ca đích ĐỎ.** Mọi vật liệu bạn cần
đã nằm sẵn trong cây; hàm `_dot_bien_nguon_512(nguon, cu, moi)` trong chính tệp test làm việc thay
`str.replace` (nó CẮT BA BẢNG dữ liệu ra trước khi đếm, vì catalogue nằm TRONG tệp bị đột biến).

Bảng `DOT_BIEN_TU_KIEM_512` trong tệp test khai **7** mục và mỗi mục khai **control phân biệt** của nó.
Việc của bạn:

- **Kiểm lời khai "mỗi mục có control phân biệt"**: mục nào mà việc gỡ chốt KHÔNG làm đúng control ấy
  lệch? Mục nào tương đương với mục khác (cùng đầu vào không phân biệt được)?
- **Tìm chốt CHƯA có mutant nào canh nó.** `CHOT_CHUA_CO_CONTROL_512` khai **9** chốt như vậy — con số
  ấy đúng chưa? Có chốt nào KHÔNG nằm trong danh sách mà cũng không có mutant?
- **Tìm đường cấp TÍN DỤNG GIẢ còn mở**: có đầu vào nào làm `doc_kenh` trả `GIET` trong khi ca đích
  KHÔNG chết đúng bằng `TinHieuChotCa`? Có đầu vào nào làm nó trả `KHONG_GIET` cho một mutant đã bị
  giết thật (một phép đo BỊ MẤT — hướng ngược, cũng là lỗi)?
- **Bộ chấm có còn đọc hình dạng chuỗi ở đâu không?** `M6` đòi KHÔNG. Nếu còn một chỗ, nêu nó.

### 3. ĐO LẠI TỪNG CON SỐ trong `BANG_KHAI.md`

Đây là nhiệm vụ chính thứ hai, ngang hàng với mục 2. Bảng ấy **chắc chắn thiếu** — nó do tôi tự liệt
kê cộng một bộ lọc theo **danh sách đơn vị đoán trước**. **Mỗi con số bạn tìm ra mà bảng bỏ sót được
TÍNH LÀ MỘT FINDING.** Và mỗi con số trong bảng mà bạn đo ra KHÁC cũng là một finding.

Nhắc một hình dạng lỗi mà kho này đã trả giá: **một bất biến còn đúng KHÔNG chứng minh các số hạng
còn đúng.** Khi một câu vừa nêu số hạng vừa nêu quan hệ giữa chúng (kiểu *"148 + 67 + 90 + 497 = 802"*),
hãy **kiểm số hạng**, đừng kiểm quan hệ — quan hệ là thứ sống sót qua trôi số.

### 4. Điểm danh HỒI QUY

155 ca cũ phải giữ NGUYÊN ngữ nghĩa (`ngoai_pham_vi` #5 của đặc tả: port đổi **TÍN HIỆU**, không đổi
điều được khẳng định). `git -C ../kho-guong.git diff dc02c9b a1c7d7f -- ops/lease_publish_test.py` —
có ca nào bị đổi điều nó khẳng định, chứ không chỉ đổi cách nó báo?

## VIỆC BẠN **KHÔNG** LÀM

- **KHÔNG tự soạn** nội dung dạng đường-dẫn-thoát, payload khai thác, hay mã tấn công. Kho này đã trả
  giá: bộ lọc nội dung của nền bắn đúng khi reviewer phải TỰ SOẠN thứ ấy, làm chết hai lượt review
  liên tiếp và mất trắng cả hai transcript. Mọi phản chứng bạn cần **đã nằm trong cây**; việc của bạn
  là **CHẠY** chúng và **ĐỘT BIẾN BẢN VÁ**. Hướng thử nào cần soạn nội dung dạng ấy thì **mô tả bằng
  lời** trong verdict cho phiên điều phối viết.
- **KHÔNG** sửa đặc tả đóng băng, **KHÔNG** sửa lease, **KHÔNG** sửa `ops/reviews/**`.
- **KHÔNG** chạy CI, **KHÔNG** gọi `workflow_dispatch`, **KHÔNG** cần mạng. Mọi thứ chạy offline.
- **KHÔNG** đẩy gì lên remote (`origin` của `cay/` trỏ vào gương cục bộ, không phải GitHub).
- **KHÔNG** kết luận gì về Windows: `full CI`/`CI Windows` chỉ chạy khi merge, nên chúng **chưa tồn
  tại** cho mã này ⇒ `KHÔNG ĐO ĐƯỢC`.

## VERDICT — ghi `ket-qua/VERDICT.md`, và ghi SAU MỖI PHÁT HIỆN

**Ghi tăng dần: mở tệp, thêm một lớp, LƯU, rồi mới tìm tiếp.** Đừng dồn tới cuối lượt — một lượt bị
ngắt giữa chừng thì phần đã ghi phải còn.

Đầu tệp:

```
verdict: changes_requested | approve | blocked
reviewed_sha: a1c7d7ffbac710346400650b94e2d2a8035f62b5
vong: 1/10
so_p1: <n>
so_p2: <n>
so_p3: <n>
so_no_ngoai_write_set: <n>
```

Mỗi **LỚP** một mục, có:

- **slug kebab-case ổn định** (nó là khoá đếm qua các vòng);
- mức `P1`/`P2`/`P3`, hoặc `NỢ` nếu thuộc đường ngoài write set;
- **phép đo tái lập được**: lệnh đã chạy, đầu ra thật, `rc` thật. Không có phép đo ⇒ nói thẳng
  `KHÔNG ĐO ĐƯỢC`, đừng đoán;
- **các thể hiện** của lớp ấy (đếm riêng, đừng gộp vào số lớp);
- hướng chữa **đề xuất** — bạn được đề xuất, phiên thi công là người vá.

Ba trạng thái, không phải hai: **có** · **không** · **KHÔNG ĐO ĐƯỢC**. Trạng thái thứ ba là một kết
luận hợp lệ và phải được ghi như vậy; nó KHÔNG phải "không có vấn đề".

Nếu bạn thấy một lời khai của tôi rộng hơn phép đo của tôi — kể cả trong chính prompt này — **hãy nêu
nó**. Đó là lớp lỗi đắt nhất của kho này.
