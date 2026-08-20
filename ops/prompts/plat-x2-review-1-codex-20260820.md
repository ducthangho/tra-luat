# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X2`, lượt 1, provider `codex`

Bạn là **reviewer khác nhà cung cấp**. Executor là `claude`; §8 protocol bắt reviewer phải
khác provider để đạt `cross_approved`. **Read-only: KHÔNG sửa tệp, KHÔNG commit, KHÔNG push.**

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#195` — `[WP PLAT-X2]` |
| exact head phải review | `c869796f5f052e2b564cf8c1d4bdd2dcd940cb47` |
| base | `50d8d12e146792368e7100f732ff15a8d32fe48d` |
| nhánh | `claude/plat-x2-exec-1` |
| write set khai báo | `.github/workflows/ops-publish-lease.yml` · `ops/lease_publish_test.py` · `.gitignore` |
| review class | `sensitive` |

Kiểm HEAD trước khi nói bất cứ điều gì: `git rev-parse HEAD` phải bằng đúng chuỗi trên. Lệch
⇒ dừng, khai `stale head`, không review.

## 2. Bối cảnh — vì sao có bản vá này

Lượt chạy `32342373756` của `ops-publish-lease.yml` ĐỎ `rc=8`. Bước `tìm lease vừa đổi` có
đường dự phòng `find ops/leases -type f` chạy khi `github.event.before` toàn số 0 — tức mọi
push **mở nhánh mới**, mà đó chính là cách kho vẫn đăng lease. Một lease cũ **chưa từng đăng
mà đã hết hạn** làm cả lượt chạy chết, nên **mọi lease mới không đăng được** từ 18-08-2026.

Bản vá: mốc so dùng `git merge-base origin/$MAC_DINH $NAY` cho nhánh mới; bỏ `|| true`;
đưa `${{ }}` ra khỏi thân `run`; thêm `t32`/`t33`; `.gitignore` một dòng.

## 3. Trục phải soi — đây là cổng CẤP QUYỀN GHI

Workflow này chạy bằng `GITHUB_TOKEN` với `contents: write` + `issues: write`. **Push được
thành đăng được.** Vì vậy:

1. **Bản vá có NỚI chốt nào không?** Lease hết hạn vẫn phải chặn; `granted_by` mang tên
   provider vẫn phải chặn; neo prompt vẫn phải kiểm; `GITHUB_ACTOR` vẫn phải kiểm. Bất cứ
   đường nào làm một lease **chưa ai review** đăng được dưới danh nghĩa kho là **P1**.
2. **Mốc so có bỏ SÓT lease không?** Nếu một lease hợp lệ mà push thật sự thêm lại **không**
   vào danh sách, cổng im lặng bỏ qua nó — im lặng còn tệ hơn đỏ.
3. **Mốc so có LẤY THỪA không?** Kéo theo lease của commit khác là dựng lại đúng lỗi cũ.
4. **`|| true` / fail-open còn sót ở đâu?** Ba trạng thái phải là có · không · **không đo
   được**, và trạng thái thứ ba phải ĐỎ.
5. **`t32` có thật sự ĐO không?** Nó trích thân bước từ YAML rồi chạy. Hỏi: có nhánh nào làm
   nó `return` sớm mà vẫn tính là ĐẠT? Fixture có mô phỏng TRẠNG THÁI hay chỉ diễn kịch bản?
6. **`t33` fail-close có răng không?** Thiếu `actionlint` phải ĐỎ, không được bỏ qua.
7. **YAML còn hợp lệ với GitHub không?** PyYAML không biết luật của GitHub; chỉ `actionlint`
   biết. Nhắc: `${{ }}` trong **chú thích** của `run` cũng làm hỏng cả tệp.

## 4. Cách trả lời

Với **mỗi** finding, bắt buộc bốn phần: (a) **bằng chứng đo được** (lệnh + kết quả, không
phải cảm nhận); (b) **mức** P1/P2/P3; (c) **vì sao nó là lỗi** — invariant nào bị cắt; (d)
**gợi ý vá** cụ thể. Không có bằng chứng chạy được thì ghi rõ là **giả thuyết**, đừng trình
bày như phép đo.

Kết luận đúng một trong: `approve` · `changes_requested` · `blocked`, kèm câu
`Reviewed commit: c869796f5f052e2b564cf8c1d4bdd2dcd940cb47`.

Nếu bạn không tìm được lỗi nào, hãy nói thẳng **bạn đã đo những gì** — một lời khen không
kèm phép đo thì không phải review.
