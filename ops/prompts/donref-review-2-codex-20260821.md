# Prompt BẤT BIẾN — Reviewer chéo PR "#213", lượt **2/2**, provider `codex`

**Executor `claude`, reviewer `codex`** ⇒ cross-provider, §8 thoả.

Đây là **review DELTA**: `cbc57214..9588bb1e`. Lượt 1 (chính bạn) đã soi `cbc57214` và trả
`changes_requested` với một P1. Delta này là **bản vá cho đúng P1 ấy**. Đừng soi lại phần lượt 1
đã kết luận sạch — nhưng **được phép** nói nếu bản vá làm hỏng một thứ lượt 1 đã duyệt.

Read-only với KHO: **không commit, không push, không đổi HEAD.** Đột biến chạy trên **BẢN SAO
TẠM** (`git -C kho archive <sha> | tar -x`).

```
./nhiem_vu.txt        prompt này
./VERDICT_LUOT_1.md   verdict lượt 1 của chính bạn — nguồn sinh ra delta này
./diff_delta.patch    cbc57214..9588bb1e — ĐÚNG phần phải soi
./diff.patch          master..9588bb1e — toàn bộ PR, để soi hồi quy
./bin/actionlint      actionlint 1.7.7 (NGOÀI cây kho)
./kho/                bản sao kho tại exact head, GHI ĐƯỢC
```

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| exact head | `9588bb1ef57209da02562928893f544d7d447db1` — ĐO LẠI bằng `git -C kho rev-parse HEAD` |
| head lượt 1 | `cbc57214be1f33b93c5d04e4363c2bcce87439b6` |
| write set | `.github/workflows/ops-don-ref.yml` · `ops/don_ref_chot_test.sh` · `CLAUDE.md` |
| số ca | 102 → **105** |

## 2. P1 của bạn đã được vá thế nào

Bạn đo được: bước làm đọc SHA → so → **rồi mới** `DELETE`, và một push chen vào giữa thì commit
mới bị xoá mà chưa từng được đo. REST `DELETE /git/refs` chỉ nhận TÊN ref, không có CAS.

Bản vá:

1. Xoá bằng `git push --force-with-lease="refs/$LOAI/$r:$neo" origin ":refs/$LOAI/$r"` —
   old-oid đi **trong cùng giao dịch**. Bỏ hẳn cặp đọc-lại/so.
2. `$neo` là SHA **đã GHIM ở bước chốt**, không phải SHA đọc lại.
3. GHIM nay áp cho **MỌI** ref sắp xoá, không riêng vùng làm việc; không ghim được ⇒ DỪNG.
4. Thêm `actions/checkout@v4` (`fetch-depth: 1`) để có remote xác thực cho `git push`.
5. `CLAUDE.md`: câu "đọc lại **đóng** khe" đã được sửa thành "chỉ THU HẸP", và nói rõ nó từng sai.

Người vá tự đo trên kho bare dựng tại chỗ: lease neo SHA cũ ⇒ `! [rejected] … (stale info)`,
`rc=1`, ref CÒN; lease neo SHA đúng ⇒ `- [deleted]`, `rc=0`, ref MẤT; và chạy được từ kho **0
object**. **Xác nhận các số ấy, đừng tin.**

## 3. Trục phải soi

### 3.1 Lease có thật sự đóng được khe không, và có đóng ĐÚNG CHỖ không

- `$neo` có chắc là SHA **đã được chứng minh `behind_by = 0`** không, hay có đường nào làm nó
  thành một SHA khác? Nếu ghim và phép đo tổ-tiên lệch nhau thì lease đang bảo vệ **sai giá trị**.
- **TAG có chú giải**: `git/ref/tags/X --jq .object.sha` trả SHA của **đối tượng tag**, còn
  `--paginate repos/…/tags` trả **commit**. Lease so với giá trị NÀO? Nếu lệch, `xoa-tag` sẽ
  luôn `stale info` (hỏng êm) hoặc tệ hơn. Dựng một tag có chú giải mà đo.
- Nhiều ref một lượt: ref thứ nhất xoá xong, ref thứ hai lease trượt ⇒ trạng thái **dở dang**.
  Có khai không? `set -e` dừng ở đâu?
- `chi_thu = true` có thật sự không đụng ref nào **sau** khi thêm checkout không?

### 3.2 `actions/checkout` — bề mặt MỚI trong một workflow đặc quyền

- Credential nằm ở đâu sau checkout, và bước làm dùng remote nào? Có đường nào token lọt vào
  log không?
- Workflow được `dispatch` trên một ref bất kỳ. Nếu ref đang được checkout **chính là** nhánh sắp
  xoá thì sao?
- `permissions:` hiện là `contents: write`. Có đủ cho `git push` xoá ref không, và có **thừa** gì
  không?
- Checkout ở bước ĐẦU, còn `NEO_TEP` mặc định `${RUNNER_TEMP:-/tmp}/don_ref_neo.txt` — checkout
  có làm gì với `RUNNER_TEMP` không?

### 3.3 Bộ phản chứng: `git` giả có mô phỏng TRẠNG THÁI thật không

Đây là chỗ bạn đã bắt được lượt trước, ở một tệp khác. `git` giả mới cưỡng chế lease bằng một tệp
trạng thái. **Nó có nói dối chỗ nào không?** Cụ thể:

- Nó có mô phỏng đúng việc git thật **từ chối mà không đụng ref** không?
- Ca `GIA_PUSH_KHONG_AN_GI` (báo xanh mà không đổi trạng thái) có đúng là thứ khoá phép "đo lại
  sau khi xoá" không?
- Helper `lam()` nay **tự dựng** trạng thái và ghim mặc định nếu ca không cấp. Có ca nào vì thế
  được cấp sẵn một điều kiện mà nó lẽ ra phải tự chứng minh không? Đây là hướng tôi nghi.

### 3.4 Đột biến

Người vá khai tám con, mỗi con giết đúng ca của nó:
`N1` quay về REST DELETE (**ca của bạn đỏ đúng ở đây**, `rc=0 mong 1`) · `N2` bỏ lease giữ
`git push` · `N3` lease neo SHA **hiện tại** thay vì SHA ghim · `N4` bỏ đòi ghim ở bước làm ·
`N5` bỏ ghi ghim ở chốt · `M1` bỏ chặn `behind != 0` · `M4` bỏ cấm xoá TAG vùng · đối chứng
`105/105`. **Xác nhận, rồi tự nghĩ đột biến mới** — nhất là cho 3.1 và 3.3.

### 3.5 Những trục lượt 1 KHÔNG kịp soi

Lượt 1 dừng theo điều kiện phạm vi ngay khi thấy P1, và tự khai **không mục nào được coi là
sạch**: lịch sử rời (`compare` khi hai commit không có tổ tiên chung — `behind_by` có thể bằng 0
không?), ngưỡng 250 commit của `compare`, đột biến chèn bước YAML, lập luận `M2`, và các race
quanh đầu nhánh mặc định. **Lượt này phải phủ chúng** — chúng vẫn chưa ai đo.

## 4. NGOÀI phạm vi

- Proxy chặn xoá ref của phiên web; 65 nhánh còn commit chưa vào master; lỗ `git push --force`
  đã khai của chốt proxy.
- `ops-publish-lease.yml` thiếu `pull-requests: write` (lease của PR này phải đăng tay) — đã biết,
  có PR riêng, **không** thuộc đây.

## 5. Điều kiện DỪNG

- Cần sửa mã để chứng minh ⇒ **bản sao tạm**, không sửa cây kho.
- Thấy một tiêu chí ở mục 3 là **sai** ⇒ DỪNG và nói ra.
- Thứ đòi sửa ngoài write set ⇒ finding + đề xuất, không tự mở rộng.

## 6. Định dạng trả về

**IN RA STDOUT.** Kết thúc bằng **đúng hai dòng cuối**:

```
VERDICT: <approve|changes_requested|do_not_land>
Reviewed commit: <sha 40 ký tự đã ĐO>
```

Trước đó: finding (mức, **bằng chứng đo được**, invariant bị cắt, gợi ý vá) · **"đã đo và sạch"** ·
**"chưa đo được — GIẢ THUYẾT"**.

**`approve` ở lượt này nghĩa là:** P1 của bạn đã đóng **bằng đo**, các trục 3.5 mà lượt 1 bỏ dở
đã được phủ, và bạn **không tìm thấy** đường xoá được một ref chưa an toàn. Người viết bản vá cũng
là người viết prompt này — danh sách trên là **thứ họ đã nghĩ tới**, nên hướng nguy hiểm nhất
nhiều khả năng **không** nằm trong đó.
