verdict: approve
reviewed_sha: 3239279b8763b8950bc2f3289f680e5fb25d993d
luot: 3

## ĐỐI CHIẾU LƯỢT TRƯỚC

- Lượt 1, 0 finding và các khẳng định chức năng: ĐÃ VÁ THẬT — head mới giữ nguyên logic đã được duyệt; bảy ô tự dựng lại đều khớp.
- Finding P2 lượt 2 (`ubuntu-leg-overclaim`): ĐÃ VÁ THẬT — câu mới là `rc=0 khi chạy cục bộ trên Linux (đo 23-08-2026)`; nó không gọi đây là mọi Linux hay một chân CI. Hồ sơ có băm ghi phép đo ở worktree rời trên Linux ngày 23-08-2026, và đối chứng X2 trên cây nền hiện tại vẫn cho `97/97`, `rc=0`.
- Nguy cơ bản vá tự tái tạo hình dạng A: ĐÃ VÁ THẬT — “chạy cục bộ” phân biệt đúng phép chạy worktree với GitHub leg; “trên Linux” chỉ mô tả nền thực tế, không lượng hoá thành mọi Linux. Câu trước đó trong cùng docstring nêu rõ đột biến X2, còn `97/97` định danh bộ nền không có `t98`; không thiếu điều kiện làm đổi nghĩa phép đo.
- Khẳng định executor chép nguyên văn bản vá reviewer: ĐÃ VÁ THẬT — `cmp`/`diff` giữa hai tệp trả rc=0; `diff-luot-va.patch` có đúng một path, một dòng thêm và một dòng xoá.

## BẢNG ĐO

Tất cả số suite dưới đây được đo sau khi áp bản vá môi trường #296 đối xứng vào `cay-kho/` và `nen-f33c12d/`; vì vậy chúng **không phải số pristine**. Bản vá #296 nằm ngoài write set PR #293 và đã được hoàn nguyên sau khi đo.

| khẳng định | ai khai | đo được | khớp? |
|---|---|---|---|
| `TMPDIR` đúng gốc sandbox | hồ sơ | `/rv293/tmpdir` | có |
| head được review | hồ sơ | `3239279b8763b8950bc2f3289f680e5fb25d993d` | có |
| smoke VÁ | hồ sơ/executor | `98/98 đạt; đã chạy=98, bỏ qua=0`, rc=0 | có (không pristine; đã hiệu chỉnh #296) |
| NỀN | hồ sơ/executor | `97/97 đạt; đã chạy=97, bỏ qua=0`, rc=0 | có (không pristine; đã hiệu chỉnh #296) |
| NỀN + X2 | hồ sơ/executor | `97/97 đạt; đã chạy=97, bỏ qua=0`, rc=0 | có (không pristine; đã hiệu chỉnh #296) |
| VÁ + X1 | hồ sơ/executor | `89/90 đạt; đã chạy=90, bỏ qua=8`, đỏ `t73`, rc=1 | có (không pristine; đã hiệu chỉnh #296) |
| VÁ + X2 | hồ sơ/executor | `97/98 đạt; đã chạy=98, bỏ qua=0`, đỏ `t98`, rc=1 | có (không pristine; đã hiệu chỉnh #296) |
| VÁ + X1 · gỡ `t70` | hồ sơ/executor | `88/89 đạt; đã chạy=89, bỏ qua=8`, đỏ `t73`, rc=1 | có (không pristine; đã hiệu chỉnh #296) |
| VÁ + X2 · gỡ `t70` | hồ sơ/executor | `96/97 đạt; đã chạy=97, bỏ qua=0`, đỏ `t98`, rc=1 | có (không pristine; đã hiệu chỉnh #296) |
| tệp head chép nguyên văn cây vá lượt 2 | executor | `cmp cay-kho/ops/lease_publish_test.py goi-va-293-luot2/ops/lease_publish_test.py`, rc=0 | có |
| delta riêng lượt vá | executor | một path; đúng 1 dòng docstring thay thế (`+1/-1`), không có thay đổi khác | có |
| block `t98` head | executor | 14 dòng, SHA-256 rút gọn `1ed3eb53770076d6` | có |
| block `t98` r3 | executor | 14 dòng, SHA-256 rút gọn `4c9b223d3e5edd4a` | có |
| byte-identity với r3 vỡ đúng phạm vi | executor | chỉ dòng 7/14 khác; decorator, tên, thân ca và 13 dòng còn lại đồng nhất | có |
| ngày phép đo X2 | docstring/executor | `SPEC-r3.md` ghi mọi số đo lúc `10:0xZ 23-08-2026` và ma trận chạy trên worktree rời | có |
| `97/97` của X2 trên cây nền hiện tại | docstring/executor | tự dựng X2 trên `f33c12db…`: `97/97`, bỏ qua 0, rc=0 | có |
| “chạy cục bộ trên Linux” bằng phép đo | bản vá lượt 2 | worktree cục bộ trong container Linux; câu không nói “mọi Linux” và không còn nói Ubuntu leg | có |
| `t73` một mình chỉ chứng minh posix không bỏ qua | docstring `t98` | gọi riêng `t73` xanh; X2 vẫn sống `97/97`, nên `t73` không chứng minh quyết định tra theo nền | có |
| `t98` không phụ thuộc thứ tự suite | yêu cầu lượt 3 | gọi riêng `t98_truc_phan_biet_la_NEN_chu_khong_phai_TEN_TEP()` xanh | có |
| `t33` lint đúng một workflow | docstring `t33` | AST: lời gọi duy nhất là `subprocess.run([duong, str(goc / 'ops-publish-lease.yml')], ...)` | có |
| kho có đúng 5 workflow, `t33` không lint 4 tệp còn lại | docstring `t33` | 5 tệp trong `.github/workflows`; `t33` truyền đúng 1 tệp, còn 4 | có |
| lease/diff chỉ đúng một đường dẫn | lease/executor | `git diff --name-only base..head`: chỉ `ops/lease_publish_test.py` | có |
| numstat so base và trần | hồ sơ/executor | `22 1 ops/lease_publish_test.py`; 22 dòng thêm ≤ 120 | có |
| SHA-256 đặc tả đóng băng | hồ sơ | `78c3ecb40eb8dd7dcf628ef7ea9a372aae5cfbf7a4fcfd25bb4ec7f32fe6ea0d` | có |
| Windows thật | hồ sơ | KHÔNG ĐO ĐƯỢC — sandbox không có runner Windows thật; mock không thay thế runner | KHÔNG ĐO ĐƯỢC |
| trạng thái GitHub trực tiếp | hồ sơ | KHÔNG ĐO ĐƯỢC — `origin` chỉ là mirror cục bộ | KHÔNG ĐO ĐƯỢC |
| cây bàn giao sạch | luật phạm vi | `git status --porcelain` bằng rỗng ở cả `cay-kho/` và `nen-f33c12d/` | có |

Không có finding P1/P2/P3. Không tạo `goi-va-293-luot3/` vì không có bản vá cần đề xuất.
