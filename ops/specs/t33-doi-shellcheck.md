# ĐẶC TẢ PACKET — `T33-DOI-SHELLCHECK`

```yaml
packet_id: T33-DOI-SHELLCHECK
packet_issue: 249
revision: 1
review_class: sensitive          # chạm workflow/CI authority (protocol §8), fail-closed
executor: claude
reviewer: codex
assurance_target: cross_approved
base_sha: 08bb4ecd6dbdb87267cb8179f52ac28c151eb4b9
```

## `nguon_cap_viec`

- Verdict cross-review lượt 2/3 của `#238` (`LEASE-DANG-WINDOWS`) — nợ có tên, do executor `#238` nêu
- Đo lại độc lập bởi phiên `tra-luat-3a` 22-08-2026, xem `muc_tieu`

**KHÔNG có dòng kế hoạch nào cấp việc này** — cùng lý do với `LEASE-HOI-TOAN-KHO`: nó sinh từ phép đo,
không từ kế hoạch. Ghi thẳng thay vì bịa.

## `write_set`

```
ops/lease_publish_test.py
ops/cai_actionlint.sh
```

Hai đường dẫn, liệt kê đủ, không ký tự đại diện.

**Kích thước dự kiến — có MỐC NEO đo được, chưa có số của chính packet này.** Phạm vi tương đương gần
nhất là `PLAT-X8` (PR #248): **cùng hai tệp**, `git diff --numstat` cho **2 tệp / +265 dòng thêm** lúc
16:5xZ, và phiên thi hành báo đã lên **313** sau hai bản vá P1 — tức **một** mối quan tâm trên vùng này đã
chạm trần `sensitive` của ADR-0044 (**≤ 3 tệp / ≤ 300 dòng thêm**).

Đó là mốc neo, **không** phải số của packet này: chưa có diff triển khai nên chưa suy ra được. **Phải đo lại
bằng `git diff --numstat` trước vòng review**, và vượt trần thì dừng để revision thiết kế hoặc khai lý do
theo ADR-0044 — chưa có số đo thì chưa được cấp lease thi hành.

Mốc neo ấy cũng là lý do packet này **không gộp** nợ của packet kia: xem `ngoai_pham_vi`.

**`ops/cai_actionlint.sh` BẮT BUỘC nằm trong write set, không phải tuỳ chọn.** Nếu `t33` đòi
`shellcheck` mà bộ cài không cấp nó thì lượt CI kế tiếp **ĐỎ trên master** — biến một bản vá cổng thành
một sự cố. Hai mục tiêu phải đi cùng một packet vì chúng khoá lẫn nhau. Đây chính là luật L2 áp dụng
đúng lúc: mục tiêu không chiếu được vào write set thì phải mở rộng write set **tại đây**, chứ không để
phiên thi hành gặp rồi tự xoay.

Đo **17:38Z** 22-08-2026: **11** lease `CÒN_HẠN` chạm `ops/lease_publish_test.py` — 3 lease
`plat-x8-exec-2`/`-2r2`/`-2r3` cộng 8 lease `LEASE-DANG-*`; **0** lease chạm `ops/cai_actionlint.sh`.
`PLAT-X8` **chưa tiêu**, nên write set **CHƯA RẢNH**: packet này chỉ được cấp lease sau khi `PLAT-X8`
land hoặc rút. Tám lease `LEASE-DANG-*` thuộc packet đã land qua PR `#246`, nhưng bản thân tệp lease
không tự khai trạng thái đã tiêu.

**Đo lại 18:2xZ: 13 lease, trong đó `PLAT-X8` chiếm 5 — nhưng chỉ MỘT là người giữ thật.** Bốn bản ghi
kia mang `da_bi_thay_the` và đã chết; hạn của chuỗi **không đổi** (`2026-08-23T14:10:00Z`). Vì vậy câu
trên cố ý **không** ghi số lease `PLAT-X8`: con số ấy phân rã theo giờ **và** phồng theo mỗi lượt review
của packet kia, trong khi thứ quyết định — *`PLAT-X8` còn giữ hay đã nhả* — thì không. Chi tiết cơ chế và
phép thử ở `A2c` của `ops/specs/lease-hoi-toan-kho.md`; nó là lý do hai packet này phải đi **tuần tự**
chứ không chỉ là chuyện lịch.

**Bản đầu khai "0 lease, write set RẢNH, cấp lease được ngay" — SAI, và cross-review lượt 2 bắt
(`write-set-khong-ranh`, P1).** Tác giả đo write set của `PLAT-X8` rồi **suy** rằng write set của packet
này rảnh, không hề quét `ops/lease_publish_test.py`. Đó là hình dạng **A** — *lời khai rộng hơn phép đo* —
và nếu chủ kho ký lease theo lời khai ấy thì có **hai writer** trên cùng một tệp, đúng tai nạn mà
write-set exclusion sinh ra để chặn.

**Hệ quả: hai packet KHÔNG chạy song song được.** Cả `LEASE-HOI-TOAN-KHO` lẫn packet này đều cần
`ops/lease_publish_test.py`. Thứ tự bắt buộc: `PLAT-X8` nhả ⇒ rồi **một** trong hai, xong ⇒ mới tới cái
kia. Con số lease phân rã theo giờ (9 lúc 16:5xZ · 8 lúc 17:38Z); **đo lại ngay trước khi cấp**, đừng
tin số trong đặc tả.

## `ngoai_pham_vi`

| thứ | vì sao KHÔNG làm ở đây |
|---|---|
| Vá finding `SC2320` | **Đã được `#238` vá rồi.** Đo trên master: `actionlint` cho `rc=0` / 0 finding **cả khi có lẫn khi vắng** `shellcheck`. Nhắm vào finding là nhắm vào thứ không còn tồn tại |
| Bệnh đăng trùng + `ai-dang-giu` | Packet `LEASE-HOI-TOAN-KHO`, Issue `#244` |
| Mở rộng `t33` sang workflow khác | `t33` hiện chỉ kiểm `ops-publish-lease.yml`. Mở rộng phạm vi là thay đổi khác, đo riêng |
| Ghim phiên bản `shellcheck` theo cách khác với `actionlint` | Bộ cài đã có nếp ghim `AL_VER`; theo nếp ấy, đừng chế nếp thứ hai |

## `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| **M1** | `t33` đòi `shellcheck` **có mặt** và **fail-close** khi thiếu — đúng cách nó đã đòi `actionlint` | `ops/lease_publish_test.py` |
| **M2** | Bộ cài cấp `shellcheck` cho CI, phiên bản **ghim**, theo đúng nếp `AL_VER` đang có | `ops/cai_actionlint.sh` |

### Phép đo làm nên packet này

Đo bằng `shellcheck` 0.9.0 + `actionlint` 1.7.7 cài thật trong container, trên workflow **trước `#238`**
(`ba82b06f:.github/workflows/ops-publish-lease.yml`):

```
CO  shellcheck tren PATH  ->  rc=1,  1 finding  (SC2320)
VANG shellcheck           ->  rc=0,  0 finding
```

**Cả tầng luật shell biến mất mà cổng vẫn xanh.** `actionlint` không báo rằng nó đã bỏ qua shellcheck —
nó chỉ trả 0. Cùng họ *"cổng vắng mặt trông giống cổng xanh"*, và cùng họ chính `t33`: ca ấy sinh ra vì
sáu lượt cross-review kết luận *"YAML ok"* bằng PyYAML, mà PyYAML không biết luật của GitHub.

**Hai đính chính so với lời khai của `#238`, cả hai đo được:** mã finding là **`SC2320`** (không phải
`SC1003`), và trên **master hiện tại** finding **đã được vá** — chỉ **lỗ cấu trúc** còn nguyên. Nhắm sai
một mã finding là gửi người thi hành đi tìm thứ không có.

## `nghiem_thu`

**M1** — `B1` Chạy bộ test với `shellcheck` **vắng khỏi PATH** ⇒ `t33` **ĐỎ** kèm thông điệp
`KHÔNG ĐO ĐƯỢC`, không phải bỏ qua. ĐỎ khi: đột biến đổi `assert duong_shellcheck` thành `if not ...:
return` — tức biến fail-close thành bỏ qua êm. `B2` Chạy với **cả hai** công cụ có mặt trên một workflow
**cố ý vi phạm shellcheck** (fixture, không phải tệp thật của kho) ⇒ `t33` **ĐỎ** và thông điệp nêu **đúng
mã SC cụ thể mà fixture tạo ra** (ghi mã ấy trong ca test, không chỉ khớp tiền tố `SC`). ĐỎ khi: đột biến
bỏ phần in `stdout` của `actionlint`, hoặc thay mã thật bằng một chuỗi giả như `SC0000` — cổng vẫn đỏ nhưng không nói vì sao, và
một cổng không nói lý do là cổng phải chẩn đoán lại từ đầu. `B3` Chạy với cả hai công cụ trên workflow
**thật** của master ⇒ `t33` **XANH**; sau đó chép workflow ấy sang fixture, chèn lỗi shell đã biết của
`B2` ⇒ chính `t33` **ĐỎ** với mã SC mong đợi. ĐỎ khi: bản vá làm cổng đỏ thường trực, hoặc miễn kiểm theo
tên/đường dẫn của workflow thật để nó xanh mà không chạy `actionlint`.

**M2** — `B4` Chạy bộ cài trong môi trường **không có sẵn** `shellcheck` ⇒ sau đó `shutil.which
("shellcheck")` khác `None`, `shellcheck --version` in đúng phiên bản đã ghim, **và chính executable vừa
cài** làm fixture shell sai của `B2` phát đúng mã SC mong đợi. ĐỎ khi: đột biến bỏ dòng cài `shellcheck`;
bỏ phần ghim phiên bản; hoặc cài một executable giả chỉ in đúng phiên bản rồi luôn thoát 0.
`B5` Một lượt Actions **THẬT** trên **exact head của packet** (gọi bằng `workflow_dispatch` trên đúng ref
ấy — gắn nhãn `windows` KHÔNG đủ, `ci.yml` không khai `types: [labeled]`): job `gate` xanh trên **cả
`ubuntu-latest` LẪN `windows-latest`**, `lease_publish` in `N/N` (**số ca kiểm thử đạt / số ca kiểm thử
đã chạy**) với **hai số bằng nhau**, và bằng chứng
nêu `run_id` + `head_sha` + kết luận TỪNG job. ĐỎ khi: `shellcheck` chỉ được cài trên một nền; hoặc bằng
chứng neo vào một SHA khác exact head.

**Bản đầu đòi lượt CI trên `master` — vòng tròn, và cross-review lượt 1 (PR #250, P1) bắt đúng chỗ đó.**
Packet phải qua nghiệm thu **trước** khi được land, nên lấy "CI trên master sau bản vá" làm tiêu chí nghiệm
thu là đòi kết quả của một việc chỉ xảy ra **sau** khi tiêu chí đã đạt. Tệ hơn: nó cho phép **một commit
master về sau** — không phải SHA đã review — trở thành bằng chứng. Lượt trên `master` là **cổng LAND sau
merge**, không phải bằng chứng nghiệm thu.

**Ràng buộc chéo, phải kiểm như một tiêu chí:** `B1` và `B4` **cùng phải xanh trong một lượt**. Vá `t33`
mà quên bộ cài ⇒ `B1` xanh, `B4` đỏ, master đỏ. Đó là lý do hai mục tiêu không tách được.

## `hinh_dang_ke_thua`

**Nguồn là BIÊN NHẬN, không phải thân Issue** — bản đầu chép từ thân Issue `#238`, cross-review lượt 1
(PR #250, P2) bác đúng chỗ đó. Đo trên `ops/reviews/lease-dang-review-5-claude-verdict.receipt.yaml`
(`bo-dem-sau-luot-5`): **A = 6 · B = 2 · C = 1 · D = 3 · E = 2**.

**Không có `F` trong biên nhận nào** — quét 37 biên nhận trên `master` ra **0**. Bản đầu ghi `F = 2` (lấy
từ thân Issue) rồi dùng nó tuyên bố *"F lần 3 ⇒ DỪNG"*, tức lấy một số **không có hiện vật** làm **cổng
dừng thi công**. Đã bỏ câu ấy.

Yêu cầu bằng chứng **cả hai nền** vẫn giữ nguyên, nhưng nó đứng bằng **`B5`** — một tiêu chí nghiệm thu
đo được — chứ không mượn một bộ đếm chưa ai ghi. `M2` là thay đổi phụ thuộc nền, nên bằng chứng phải đến
từ cả `ubuntu-latest` lẫn `windows-latest` **trên exact head**; lý do đủ nằm trong bản chất của `M2`, không
cần một con số để biện minh.

## `chua_do_duoc`

1. **Bản `shellcheck` mà CI sẽ nhận.** Container này cài `0.9.0` qua `apt`; runner GitHub có thể khác.
   Phiên bản ghim phải chọn lúc thi hành và **đo trên runner thật**, không chép từ đây.
2. **Có workflow nào KHÁC của kho sẽ đỏ khi shellcheck bật lên hay không.** Chưa đo — `t33` chỉ kiểm
   `ops-publish-lease.yml`, nhưng nếu ai mở rộng phạm vi thì bốn workflow còn lại chưa từng qua shellcheck.
   Đo trước khi mở rộng, đừng mở rồi mới đo.
3. **`SC2320` là finding DUY NHẤT hay chỉ là finding ĐẦU TIÊN** trên bản trước `#238`. `actionlint` có thể
   dừng sớm; chưa kiểm.
