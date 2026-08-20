# Prompt BẤT BIẾN — Reviewer chéo `PLAT-X2`, lượt **2**, provider `codex`

Read-only với KHO: **không commit, không push, không đổi HEAD.** Cây làm việc bạn đang
đứng là **bản sao rời** (git worktree tách hẳn khỏi nhánh packet) và **ghi được** — cố ý,
để bạn tự chạy phản chứng. Bẩn cây hoặc HEAD drift sau lượt này ⇒ verdict bị coi là hỏng.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#195` — `[WP PLAT-X2]` |
| exact head phải review | `23588c9723515669147dd7bfea530c4863f50556` |
| head lượt 1 (đã cũ) | `c869796f5f052e2b564cf8c1d4bdd2dcd940cb47` |
| base | `50d8d12e146792368e7100f732ff15a8d32fe48d` |
| write set khai báo | `.github/workflows/ops-publish-lease.yml` · `ops/lease_publish_test.py` · `.gitignore` |
| review class | `sensitive` · vòng **2/2** (trần canon 2 vòng) |

`git rev-parse HEAD` phải bằng đúng chuỗi trên. Lệch ⇒ dừng, khai `stale head`.

## 2. Lượt 1 bạn đã ra P1 — đây là bản đóng nó

Nguyên văn finding: diff có 5 tệp trong khi write set khai 3; hai tệp thừa là lease và
prompt của chính packet, *"không thể hợp thức hoá chúng bằng chính commit executor đang
được review"*.

Executor **nhận đúng**, và đã: xoá hai tệp khỏi nhánh packet bằng một commit MỚI (không
force-push, không rebase — lịch sử không bị viết lại), nên `git diff base..head` không còn
thấy chúng. Bốn artefact lease/prompt nay nằm ở nhánh `ops/lease-plat-x2` rẽ từ `master`,
**không mang mã**.

**Việc của bạn ở lượt này, theo thứ tự:**

1. **Đóng chưa?** `git diff --name-status <base>..HEAD` phải ra **đúng ba** tệp write set.
   Đừng tin lời khai trên — đo.
2. **Bản vá có bị đổi lén không?** So nội dung ba tệp ấy giữa `c869796` và HEAD: lượt này
   *chỉ* được phép xoá hai artefact, **không** được sửa mã. `git diff c869796..HEAD` phải
   chỉ có hai mục xoá.
3. Rồi mới quay lại **toàn bộ trục của lượt 1** — chúng chưa được đo hết vì sandbox lượt
   trước chặn `tempfile` (bạn tự khai `8/33`, và khai đúng). Nay chạy được:
   ```
   python3 ops/lease_publish_test.py          # chờ rc=0 và 33/33
   actionlint .github/workflows/ops-publish-lease.yml
   ```

## 3. Trục phải soi — đây là cổng CẤP QUYỀN GHI

Workflow này chạy bằng `GITHUB_TOKEN` với `contents: write` + `issues: write`: **push được
thành đăng được**.

1. **Có NỚI chốt nào không?** Lease hết hạn vẫn phải chặn; `granted_by` mang tên provider
   vẫn phải chặn; neo prompt vẫn phải kiểm; `GITHUB_ACTOR` vẫn phải kiểm. Đường nào làm một
   lease **chưa ai review** đăng được dưới danh nghĩa kho ⇒ **P1**.
2. **Mốc so bỏ SÓT lease?** Lease hợp lệ mà push thật sự thêm lại không vào danh sách ⇒ cổng
   im lặng bỏ qua. Im lặng tệ hơn đỏ.
3. **Mốc so LẤY THỪA?** Kéo theo lease của commit khác là dựng lại đúng lỗi cũ.
4. **Còn fail-open ở đâu?** Ba trạng thái: có · không · **không đo được**; cái thứ ba phải ĐỎ.
5. **`t32` có thật sự ĐO không?** Nó trích thân bước từ YAML rồi chạy trên kho git tạm. Hỏi:
   nhánh nào làm nó `return` sớm mà vẫn tính ĐẠT? Đồ giả mô phỏng **trạng thái** hay diễn
   kịch bản? Thử đột biến chính `ops-publish-lease.yml` **trên bản sao của bạn** rồi xem
   `t32` có đỏ không — đừng tin bảng đột biến của executor.
6. **`t33` fail-close có răng?** Thiếu `actionlint` phải ĐỎ, không được bỏ qua.
7. **YAML còn hợp lệ với GITHUB không?** PyYAML không biết luật GitHub; `${{ }}` trong
   **chú thích** của `run` cũng làm hỏng cả tệp.

## 4. Cách trả lời

Mỗi finding bắt buộc bốn phần: (a) **bằng chứng đo được** (lệnh + kết quả); (b) mức
P1/P2/P3; (c) **invariant nào bị cắt**; (d) **gợi ý vá** cụ thể. Không chạy được thì ghi
thẳng là **giả thuyết**, đừng trình bày như phép đo.

Kết luận đúng một trong: `approve` · `changes_requested` · `blocked`, kèm
`Reviewed commit: 23588c9723515669147dd7bfea530c4863f50556`.

Đây là **vòng cuối** trong trần. `changes_requested` ở đây đưa packet sang Review Rescue
Checkpoint để người giữ quyết, nên hãy phân biệt rõ **P1 chặn land** với **P3 nên làm sau**.
