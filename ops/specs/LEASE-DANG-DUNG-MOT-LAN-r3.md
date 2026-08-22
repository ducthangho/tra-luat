# ĐẶC TẢ ĐÓNG BĂNG — `LEASE-DANG-DUNG-MOT-LAN`, **bản sửa đổi 3** (delta)

> Bản này **CHỈ ghi phần thay đổi** so với bản sửa đổi 2
> (`ops/specs/LEASE-DANG-DUNG-MOT-LAN-r2.md`, sha256
> `3f310582de59dce7c109717dbab13ef9467b80c67ffeafc0ac8e1484309e0093`).
> Mọi thứ **không** nêu ở đây thì bản 2 vẫn nguyên hiệu lực: `write_set`, `ngoai_pham_vi`,
> `muc_tieu` 1–7, `nghiem_thu` `T43`–`T58`, Q1–Q16.
>
> Bản 1 và bản 2 **KHÔNG bị sửa và KHÔNG bị xoá** — lease và biên nhận các lượt trước neo vào
> chúng.

`packet_id`: `LEASE-DANG-DUNG-MOT-LAN` · `packet_issue`: `#227`
`ke_thua`: r2 (`3f310582…`) → r1 (`e1026adb…`)

## Vì sao có bản này

Review lượt 2 (`claude`, verdict sha256 `f21069548bf0e0ff507822a246283fe47417bc334fa1e231b2e71dc88d52b4c0`)
kết luận **`can_sua`**: **7/7 finding của lượt 1 ĐÃ ĐÓNG THẬT**, còn lại **1×P1 + 3×P3**.

P1 là một **phản chứng THIẾU**, không phải hành vi sai. Q9 dời hai lớp GitHub ra khỏi `kiem()`,
nên `kiem-github` là **thứ duy nhất** chạy chúng — và nó có **đúng một điểm gọi trong toàn kho**:
một dòng trong `.github/workflows/ops-publish-lease.yml`. Không ca nào đo điểm gọi ấy.

Đo hai chiều, trên bản sao tạm dựng từ `git archive` head `90015a53`:

```
xoá khối gọi `kiem-github` khỏi YAML  ->  58/58, actionlint rc=0   (đếm còn 0 lần nhắc)
xoá khối gọi `check`       khỏi YAML  ->  57/58, `t51` ĐỎ
```

Bất đối xứng ấy là lỗ **do chính packet mở**: nó thêm một lời gọi bắt buộc thứ hai, dồn toàn bộ
giá trị an ninh của Q9 vào đó, rồi không nối nó vào phép đo đã có sẵn. Đúng họ **"cổng không nói
dối, nó VẮNG MẶT"** — chính lớp bệnh packet này sinh ra để chữa.

Người giữ kho chọn **vá nốt P1 rồi land** (2026-08-21).

## Quyết định MỚI — Q17…Q19

| # | quyết định | căn cứ ĐO ĐƯỢC |
|---|---|---|
| **Q17** | **Trần ngân sách nới 500 → 550 dòng thêm.** `write_set` vẫn đúng 3 tệp. | Head hiện tại `+498`. Bản vá P1 mà reviewer mô tả là ~10–15 dòng trong `_chay_buoc_dang`, cộng tách `t55` và ca `T53`. Nêu số vì trần cũ **không còn chỗ cho một dòng nào** — và một trần đã cạn thì nó không còn là trần, nó là một lệnh cấm. |
| **Q18** | `T53` phải **làm đúng chữ của nó** hoặc **hạ lời khai xuống đúng thứ nó đo**. Không được giữ nguyên. | P3 lượt 2: `T53` khai *"toàn suite"* nhưng `t53` chạy **một** lệnh `check`, với `GITHUB_ACTOR="ducthangho"` — đúng giá trị duy nhất **không** kích hoạt được lớp actor. Đo: `GITHUB_ACTOR=nguoi-la` ⇒ **36/58** trên head. Reviewer **đo nền trước**: `26/42` trên `cfaccff9` ⇒ **delta = 0**, đây là cơ chế có sẵn (`chay()` truyền `env=None`), **KHÔNG** phải hồi quy. Cái mới là **lời khai**. |
| **Q19** | `t55` **tách đôi**, và đột biến giết nhiều ca phải được **KHAI**. | P3 lượt 2: hai đột biến **độc lập** (dấu không ở đầu thân · thiếu `user.login`) cùng chỉ giết `t55` ⇒ ca ấy không nói được cái nào hỏng. Và đột biến *"bỏ lớp đo loại số hiệu"* giết `t43`+`t44` mà chưa ai khai — `nghiem_thu` r2 đã đòi khai, đòi ấy chưa được thực hiện. |

## `nghiem_thu` — BA ca THÊM

Giữ nguyên `T43`–`T58` của r2. Mỗi tiêu chí nêu **phép đo nào làm nó ĐỎ** (L3); đột biến chạy
trên **BẢN SAO TẠM**.

| # | tiêu chí | đột biến làm nó ĐỎ |
|---|---|---|
| **T59** | Trong phép đo thân bước, `lease_publish.py` giả **ghi nhật ký `argv`**. Với **mỗi** lease đăng được, nhật ký phải có một dòng `kiem-github <tệp>` và nó phải đứng **TRƯỚC** `check <tệp>`. | **D10** — xoá hẳn khối gọi `kiem-github` khỏi YAML (lượt 2: **SỐNG SÓT 58/58**) |
| **T60** | `kiem-github` trả `rc≠0` ⇒ lease đó **KHÔNG** được POST, **và** bước thoát khác 0. | **D11** — vẫn gọi `kiem-github` nhưng **nuốt mã thoát** (bỏ cả hai nhánh `if`) (lượt 2: **SỐNG SÓT 58/58**) |
| **T61** | `t55` tách thành **`t55a`** (thiếu `user.login` ⇒ CHẶN) và **`t55b`** (dấu không ở đầu thân ⇒ không tính). Hai đột biến độc lập phải giết **hai ca khác nhau**. | **D6** (dấu chỉ cần `in body`) phải giết **chỉ** `t55b`; **D7** (thiếu `user.login` ⇒ cho qua) phải giết **chỉ** `t55a` |

**Q18 không sinh ca bắt buộc mới** — nó cho hai đường: thêm một ca chạy **toàn suite** trong
tiến trình con với `GITHUB_ACTOR` **ngoài** allowlist (khi ấy `chay()` phải dựng env sạch, kẻo
chính ca ấy đỏ), **hoặc** sửa mô tả `t53` cho khớp thứ nó đo. Chọn đường nào cũng được, nhưng
**phải khai rõ đã chọn đường nào và vì sao** trong báo cáo.

Ngoài ba ca trên: suite `rc=0`, `N/N` hai số bằng nhau, **≥ 61 ca**; mỗi đột biến giết **đúng ca
của nó**; **đột biến giết nhiều ca phải được KHAI**, kể cả `bo lop do loai so hieu` → `t43`+`t44`
và `cho kiem() goi mang tro lai` → 8 ca.

## `ngoai_pham_vi` — thêm

| thứ | vì sao KHÔNG làm |
|---|---|
| Sửa mục `chua_do_duoc` của r2 (P3 thứ ba của lượt 2) | `ops/specs/**` **không nằm trong `write_set`**, và một đặc tả đã có băm thì **không sửa đè**. Một lời khai hẹp hơn thực tế được đính chính ở **biên nhận** (`verdict_usage_caveats`) rồi nâng lên `ops/reviews/README.md` — đúng cơ chế kho đã có. Phiên điều phối làm, KHÔNG phải executor. |
| Đóng khe race hai nhánh `ops/**` | Vẫn ngoài phạm vi. `concurrency` gom theo `github.ref`. **Thu hẹp**, không **đóng**. |

## `hinh_dang_ke_thua` — cập nhật

**A. *lời khai rộng hơn phép đo*** — bộ đếm giữ **6**.

Reviewer lượt 2 **chủ động từ chối** tăng lên 7, và lập luận đứng vững: lần thứ 6 (Q5/`T52`) là
một lời khai **SAI** mà phép đo không thể phát hiện; P1 lượt 2 thì lời khai của `muc_tieu` 5 là
**ĐÚNG** — đo được rằng wiring hiện tại chạy đúng thứ tự và tôn trọng mã thoát — chỉ **thiếu ca
khoá**. Đó là *"phản chứng bắt buộc còn thiếu"*, một hình dạng khác.

**Người giữ kho chưa quyết** liệu P3 về `T53` có tính là lần thứ 7 hay không; reviewer nêu ra và
để ngỏ. Ghi lại trạng thái ấy thay vì làm tròn theo hướng nào (L1).

**B. *mượn tiền lệ mà không đo xem nó áp dụng được không*** — giữ **2**.

**C. *phản chứng bắt buộc còn thiếu*** — **MỚI**, bộ đếm **1**: P1 lượt 2 của chính packet này.

**Chốt cho lượt 3:** hình dạng **A** lần thứ 7 · **B** lần thứ 3 · **C** lần thứ **2** ⇒ **DỪNG,
không vá**, xuất handoff.

## `chua_do_duoc` — thay trọn mục của r2

Sáu mục của r2 giữ nguyên, **thêm ba** mà lượt 2 đo được hoặc khai thiếu:

1. **`chua_do_duoc` của r2 khai HẸP hơn thực tế** — nó thiếu chính P1: Q9 khai *"CHỈ bước `đăng`
   gọi `kiem-github`"*, nửa *"check/body KHÔNG gọi"* có `t58` đo, nửa *"workflow CÓ gọi"* không
   ai đo. Bản r3 đóng nửa ấy bằng `T59`/`T60`.
2. **Mỏ neo `user.login == "github-actions[bot]"` là TÀI LIỆU, không phải phép đo.** Lý do nó
   không giả mạo được nằm ở luật không gian tên của GitHub; phép đo của kho chỉ chứng minh mã
   **lọc theo** trường ấy. Từ trong container **không** tách được *"không đặt được"* khỏi
   *"không ai thử"*. Kiểm được một nửa: `grep` trên 4 workflow còn lại ⇒ **không** workflow nào
   khác đăng comment.
3. **Không đo được có ruleset / branch protection cho `.github/workflows/**` và
   `ops/lease_publish*.py` hay không.** Thiếu nó thì cả cổng này vẫn quy về *"ai push được vào
   `ops/**` thì đăng được"*, đúng như đầu tệp YAML tự khai. Ngoài kho, ngoài phạm vi packet —
   nhưng **phải nói**, kẻo `cross_approved` bị đọc rộng hơn thực tế.
