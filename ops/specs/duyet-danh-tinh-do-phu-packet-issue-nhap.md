# `DUYET-DANH-TINH-DO-PHU` — ba nợ độ phủ mà packet #348 land KÈM KHAI

Packet #348 (`TACH-DANH-TINH-GITHUB`, PR #349) land ngày 2026-08-28 tại merge commit
`d4b3045a6e5ec7daf4a9ebfacb405153de04fc99`, verdict `approve` của cross-review lượt 4
(`claude-fable-5 / max`, neo `836b0a7`). Verdict ấy xếp **ba nợ P3**, và nói rõ không cái nào
tự chặn land. Hồ sơ này mở packet cho đúng ba nợ ấy.

**Mọi con số dưới đây là số phiên điều phối TỰ ĐO trên master `d4b3045`, không chép verdict.**
Executor phải đo lại — kho này có bài học *"một bất biến còn đúng không chứng minh các số hạng
còn đúng"*.

## Nền, đo trước

`.claude/dev/duyet_danh_tinh_test.py` trên master: `ca=35; dot bien=43`, `TONG: DAT`, `rc=0`.

---

## Nợ 1 — `tang-actionlint-khong-doi-shellcheck-va-tin-PATH-tran`

`_kiem_actionlint` (`duyet_danh_tinh_test.py:693-707`) đòi `actionlint` có mặt, **không đòi
`shellcheck`**.

Đo được, hai chiều:

| PATH | kết quả |
|---|---|
| đủ cả hai | `35/43`, `TONG: DAT`, `rc=0` |
| **bỏ `actionlint`** | `ĐỎ hai_workflow_QUA_ACTIONLINT: KHONG DO DUOC: thieu 'actionlint'`, `TONG: HONG`, **`rc=1`** |
| **bỏ `shellcheck`** | `35/43`, `TONG: DAT`, **`rc=0`** — không gì phát hiện |

Chiều thứ ba mới là chỗ đau: thiếu `shellcheck` thì `actionlint` **bỏ toàn bộ lớp luật `SC*`
trong im lặng rồi vẫn trả `rc=0`**. Chính commit `836b0a7` và chú thích trong
`duyet-phan-chung.yml` khai đúng câu ấy — rồi tầng đo lại không đòi công cụ mà lời khai gọi là
BẮT BUỘC. Bước cài trong CI là chốt **CÀI**, không phải chốt **ĐO**.

`CLAUDE.md` đã ghi sổ đúng gap này cho `t33` (*"đòi actionlint có mặt nhưng KHÔNG đòi
shellcheck"*). Tầng mới **tái sinh nó ngay trong lượt biết rõ về nó nhất**.

Vế phụ, phạm vi hẹp hơn: `_kiem_actionlint` gọi `actionlint` **trần** từ PATH và tin luôn, trong
khi kho có `ops/cai_actionlint.sh` mang doctrine *"có mặt != đúng bản"* (đối chiếu băm, `rc` 7/9).
Trong CI đường cài đã ghim băm nên vế này chỉ có nghĩa **ngoài** CI — dev local, sandbox reviewer.
Đừng thổi nó to hơn thế.

## Nợ 2 — `fixture-khoa-trung-chi-ghim-ba-ten-khoa-hai-muc`

Loader `_SafeLoaderKhongKhoaTrung` **chặn đúng, và chặn rộng**. Đo độc lập, không dùng fixture của
bộ test — dựng khoá trùng ở **8 mức**, so hai loader:

| mức | `yaml.safe_load` | loader mới |
|---|---|---|
| top-level (`name`) | NUỐT, xanh | `raise khoa trung: 'name'` |
| trong khối `on` | NUỐT, xanh | `raise khoa trung: 'pull_request'` |
| mức job (`runs-on`) | NUỐT, xanh | `raise khoa trung: 'runs-on'` |
| hai job trùng tên | NUỐT, xanh | `raise khoa trung: 'j'` |
| step (`if`) | NUỐT, xanh | `raise khoa trung: 'if'` |
| `with` | NUỐT, xanh | `raise khoa trung: 'k'` |
| `env` | NUỐT, xanh | `raise khoa trung: 'A'` |
| `permissions` workflow | NUỐT, xanh | `raise khoa trung: 'permissions'` |

**8/8.** Nhưng fixture chỉ dựng **ba tên khoá** (`permissions`, `runs-on`, `if`) ở **hai mức**.

Hệ quả đo được: đưa loader về **danh sách cấm** —
`if da_co and khoa in ("permissions", "runs-on", "if"):` — **sống sót trọn bộ**: `35 ca`,
`43 đột biến`, `TONG: DAT`, `rc=0`.

Nói thẳng vì packet này đã gặp **bảy lần** họ *"danh sách cấm đội lốt allow-list"*: cổng đang chạy
**KHÔNG** có chỗ thứ tám. Đây là **bóng** của họ ấy ở tầng độ phủ — tính chất "chặn MỌI khoá ở MỌI
mức" đang CÓ trong mã và KHÔNG CÓ trong phép đo. Một hồi quy hình-danh-sách-cấm ngay bên trong
chính cái loader sinh ra để đóng họ ấy sẽ **vô hình**.

## Nợ 3 — `moc-regex-khai-fail-close-nhung-khong-ai-do`

Docstring `_moc` (`duyet_danh_tinh.py:111-113`) khai *"dạng khác fail-close"*. Không ca nào ép điều
đó.

Đo: đột biến `if not m:` → `if False:` (bỏ hẳn tầng regex) — suite vẫn `35/43`, `TONG: DAT`,
`rc=0`. Mutant **sống**.

Ca thiếu đã có sẵn hình dạng: `'2026-05-05'` — `datetime.fromisoformat` đọc được
(`2026-05-05 00:00:00`), regex **từ chối** (`KhongDoDuoc: mốc thời gian không đọc được`). Đó chính
là fail-close mà lời khai hứa, và **không ai khoá nó lại**.

Phạm vi: **không khai thác được** trên dữ liệu GitHub thật (REST trả `submitted_at` độ chính xác
giây, hậu tố `Z`, cố định độ rộng). Đây là nợ ĐỘ PHỦ, không phải lỗ. Đừng viết nó thành lỗ.

---

## Việc

1. Nợ 1 vế chính: đòi `shellcheck` trong `_kiem_actionlint`, cùng thông điệp chỉ cách cài như vế
   `actionlint`. Kèm **đột biến canh**: bỏ phép đòi ấy phải làm một ca ĐỎ.
2. Nợ 2: một fixture khoá trùng ở mức `with`/`env`/step với **tên khoá ngoài bộ ba**, hoặc một ca
   sinh tên khoá **ngẫu nhiên** rồi đòi loader đỏ. Đủ để giết mọi biến thể danh-sách-cấm — nhưng
   hãy tự đo là nó giết thật, đừng tin câu này.
3. Nợ 3: một ca khoá `'2026-05-05'` ⇒ `KhongDoDuoc`, và một đột biến bỏ tầng regex phải giết đúng
   ca ấy.
4. Nợ 1 vế phụ: **quyết rồi ghi lý do**, không im lặng bỏ qua. Nếu chọn không đóng, viết vào
   docstring rằng tầng này tin PATH và vì sao thế là đủ trong CI.

## CÂU HỎI THẬT — hồ sơ CỐ Ý không đưa đáp án

Đường rẻ nhất cho nợ 1 là thêm một dòng đòi `shellcheck` vào `_kiem_actionlint`. Nhưng thế là buộc
**bộ test này** mang trách nhiệm kiểm công cụ, trong khi kho **đã có** `ops/cong_cu.py` +
`ops/cong_cu.yaml` cho đúng việc ấy, và `t33` mang cùng gap — nghĩa là gap **không thuộc về một bộ
test**, nó thuộc về chỗ chưa ai đứng.

`(A)` đóng tại `_kiem_actionlint`, chấp nhận mỗi bộ test tự kiểm công cụ của mình · `(B)` đóng ở
`ops/cong_cu.py` như một preflight dùng chung, rồi cả `t33` lẫn bộ này gọi vào · `(C)` cách khác mà
**bạn đo ra** là tốt hơn.

**Không được chọn `(A)` chỉ vì hồ sơ liệt kê nó trước.** Nếu chọn `(A)`, phải nói được vì sao
chấp nhận việc gap ấy còn sống ở `t33`.

## write set

- `.claude/dev/duyet_danh_tinh_test.py`
- `.claude/dev/duyet_danh_tinh.py` — chỉ docstring nợ 3; **không đổi hành vi cổng**

Nếu chọn `(B)` thì write set phải mở thêm `ops/cong_cu.py` / `ops/cong_cu.yaml` — và đó là một
**revision của lease**, không phải tiện tay ghi thêm.

## ĐO NGƯỜI GIỮ — và nó đang BỊ CHẶN

`ops/lease_publish.py ai-dang-giu` ngày 2026-08-28 trên bản sao cách ly (244 ref, hai nguồn lệch 0):

```
.claude/dev/duyet_danh_tinh.py       rc=11   NGƯỜI_GIỮ 1: tach-danh-tinh-github-exec-1r6-codex-20260828
.claude/dev/duyet_danh_tinh_test.py  rc=11   NGƯỜI_GIỮ 1: tach-danh-tinh-github-exec-1r6-codex-20260828
```

Người giữ là **lease của chính packet #348 đã land**, còn hạn tới `2026-08-29T04:05Z`, và kho
**không có đường thu hồi lease** — nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`. Đây là lần **thứ
ba** nó đo được là chặn việc thật (lease #348 r6 ghi hai lần trước).

**KHÔNG được đọc `rc=11` này thành "cứ làm đi".** Lease cho packet này chỉ cấp được sau khi
`NGƯỜI_GIỮ` về 0 — hoặc bằng đường thu hồi mà `LEASE-TOAN-VEN` mở ra, hoặc bằng việc chủ kho
quyết. Hồ sơ này KHÔNG tự quyết thay.
