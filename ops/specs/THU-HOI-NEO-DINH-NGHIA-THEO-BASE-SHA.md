# Đặc tả đóng băng — THU-HOI-NEO-DINH-NGHIA-THEO-BASE-SHA

- **Packet Issue:** #618
- **Revision:** 1
- **Trạng thái:** frozen 2026-09-24

## 1. Vấn đề, phát biểu bằng phép đo

`ops-thu-hoi-admission.yml` thoát `12` trên mọi PR có `base.sha` tụt sau nhánh mặc định. Đo trên
PR #601, hai head liên tiếp cùng ngày:

| head | `workflow_sha` | `base.sha` | kết quả |
|---|---|---|---|
| `fa263ef2` | `ce25a427` | `d553efa5` | exit 12, `thu-hoi` FAILURE (run `35981638892`) |
| `7e284661` | `ce25a427` | `ce25a427` | `thu-hoi` SUCCESS |

Bộ kiểm canonical chạy lại tại chỗ trên cùng `S`/`H` cho `rc=0` (`TAP_THU_HOI_RONG`, sổ `S=0 T=0`),
nên cổng chết ở bước **neo định nghĩa**, trước khi tới bộ kiểm.

## 2. Bất biến phải GIỮ

**B1.** Định nghĩa workflow đang chạy phải là **mã canonical của nhánh mặc định**, không bao giờ là
mã của nhánh ứng viên. (Nguồn: khối chú thích đầu tệp; finding `F07` cross-review A0.)

**B2.** Bộ kiểm chạy phải là mã canonical, không phải mã ứng viên; cây của `H` chỉ được **đọc** qua
object-store, không checkout.

**B3.** Thiếu hoặc mơ hồ thì ĐỎ (fail-close), ba trạng thái chứ không phải hai.

## 3. Bất biến KHÔNG được coi là bất biến

**K1.** *"Nhánh mặc định phải đứng yên kể từ base của PR."* Chốt hiện tại cưỡng chế điều này qua
`[ "$TL_WF_SHA" = "$TL_S" ]`, nhưng nó **không** phục vụ B1. Đây là vế bị gỡ.

## 4. Thay đổi được phép

1. `actions/checkout` lấy `ref: ${{ github.workflow_sha }}` thay cho `base.sha`.
2. Chốt neo đổi thành: `git rev-parse HEAD` **bằng** `$TL_WF_SHA`.
3. Thêm chốt chống lùi: `git merge-base --is-ancestor "$TL_S" HEAD` phải `rc=0`.
4. Giữ **nguyên** chốt `workflow_ref` dạng `<kho>/.github/workflows/ops-thu-hoi-admission.yml`
   nối `@` + `refs/heads/<nhánh mặc định>`. Đây là bằng chứng do GitHub cấp cho B1.
5. Giữ **nguyên** `--canonical-base "$TL_S"`: `S` vẫn là mốc so sổ revocation, chỉ thôi làm mốc checkout.
6. Receipt ghi thêm `checkout_commit` để ba mốc `S` / `workflow_sha` / `T` phân biệt được.

## 5. Đánh đổi phải khai trong PR

Bộ kiểm sẽ chạy bản `ops/lease_publish.py` tại `workflow_sha` (mới hơn hoặc bằng `S`) thay vì tại `S`.
Đó là bản canonical **mới nhất** của nhánh mặc định — chặt hơn, không lỏng hơn — nhưng **là một thay
đổi hành vi** và phải được review như vậy, không được mô tả là "chỉ sửa một phép so".

## 6. Acceptance — mỗi mục phải có ca chạy được

**A1.** Ca mới đo **HÀNH VI**, không đo hình thức: dựng `workflow_sha != S` với `workflow_sha` là hậu
duệ hợp lệ của `S` trên nhánh mặc định ⇒ cổng **QUA**. Đây là ca tái hiện chính sự cố PR #601.

**A2.** Phản chứng cho B1: `workflow_sha` **không** thuộc nhánh mặc định ⇒ cổng **ĐỎ**.

**A3.** Phản chứng cho chốt chống lùi: `workflow_sha` là **tổ tiên thực sự** của `S` ⇒ cổng **ĐỎ**.

**A4.** Đột biến bắt buộc: gỡ chốt ở mục 4.3 phải làm **A3 ĐỎ**; gỡ chốt `workflow_ref` phải làm
**A2 ĐỎ**. Không có đột biến nào thì không biết ca đang đo chốt hay đo thứ khác.

**A5.** `t148` hiện chốt theo hình thức (`"workflow_sha" in scripts and "$TL_S" in scripts`). Nó
**không** bắt được thay đổi phép so — phải khai điều đó ngay tại ca, không sửa ca thành lỏng hơn.

**A6.** `actionlint` chạy được trên tệp sau khi sửa; thiếu công cụ thì in `KHÔNG ĐO ĐƯỢC` và ĐỎ,
không tự tắt.

## 7. Write set

```
.github/workflows/ops-thu-hoi-admission.yml
ops/lease_publish_test.py
ops/specs/THU-HOI-NEO-DINH-NGHIA-THEO-BASE-SHA.md
ops/leases/wp618-exec-1-claude-20260924.yaml
```

KHÔNG chạm `ops/lease_publish.py`. KHÔNG chạm `ci.yml`. Tệp thứ năm trong diff là finding.

## 8. Ngoài phạm vi

- Không bật `SO_THU_HOI_KICH_HOAT`; cổng vẫn ở trạng thái A0 như khối chú thích đầu tệp khai.
- Không biến `thu-hoi` thành required check.
- Không đụng bốn packet đang mở khác.
