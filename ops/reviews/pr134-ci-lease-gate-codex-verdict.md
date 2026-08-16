# Review PR #134 — nối bộ cổng đăng lease vào `ci.yml`

reviewed_sha: `ae755d10856991db7577974a2e8464005f84c940`

verdict: `approve_with_findings`

## Kết luận

Hai bước mới **thật sự chặn** và được đặt đúng đường cưỡng chế. Tôi đo độc lập trên cây, không dùng số trong PR body hay commit message. Finding duy nhất là dependency CI không có biên phiên bản: nó không làm sai phép đo hôm nay, nhưng làm kết quả của cùng một SHA phụ thuộc vào thời điểm PyPI.

## 1. Bước mới có thật sự chặn không? — ĐÃ ĐO

Neo cây:

```bash
git rev-parse HEAD
# ae755d10856991db7577974a2e8464005f84c940
```

Ca lành, chạy bằng `subprocess.run` và đọc trực tiếp `returncode`:

```bash
python - <<'PY'
import subprocess, sys, time
t = time.perf_counter()
p = subprocess.run([sys.executable, "ops/lease_publish_test.py"],
                   text=True, capture_output=True)
print(p.returncode, time.perf_counter() - t)
print(p.stdout)
PY
# rc=0; 3.504 s; lease_publish: 30/30 đạt
```

Ca biết phải đỏ: tôi tạo detached worktree đúng SHA trên, xóa riêng hàng
`wp55-r4-review-2-codex-verdict.md` khỏi bảng `## Mục lục`, rồi chạy cùng lệnh:

```bash
git worktree add --detach /tmp/pr134-mut.pInKl9 ae755d10856991db7577974a2e8464005f84c940
# xóa hàng wp55-r4-review-2-codex-verdict.md khỏi ops/reviews/README.md
cd /tmp/pr134-mut.pInKl9
python ops/lease_publish_test.py
echo "$?"
# lease_publish: 29/30 đạt
# ĐỎ t27 ... verdict 'wp55-r4-review-2-codex-verdict.md' KHÔNG có ... bảng 'Mục lục'
# rc=1; phép đo bọc subprocess: 3.591 s
```

Trong YAML, cả bước cài và bước selftest nằm trực tiếp trong `jobs.gate.steps`; bước selftest không có `if:` và không có `continue-on-error`. `run` thất bại vì vậy làm matrix leg và job `gate` thất bại. Đây là cổng chặn, không chỉ là bước có mặt.

Việc thêm chính tệp verdict này tạo thêm một `*-verdict.md` chưa có trong Mục lục. Theo yêu cầu review, tôi **không sửa README để né**; phép chạy sau khi ghi tệp được ghi ở cuối verdict và phải đỏ ở `t27`.

## 2. Đặt ở `ci.yml` có đúng chỗ không? — ĐÃ KIỂM CẤU HÌNH VÀ SO ĐƯỜNG KÍCH HOẠT

Đúng chỗ. `ci.yml` chạy trên mọi `pull_request`, push vào `master`, và gọi tay; vì vậy nó kiểm bất biến của cây trước khi thay đổi đi vào master. PR thường chạy Ubuntu; push master và `workflow_dispatch` chạy cả Ubuntu lẫn Windows theo matrix hiện tại.

Nới riêng `paths:` của `ops-publish-lease.yml` tới `ops/reviews/**` chưa đủ: workflow ấy còn giới hạn `push.branches: ['ops/**']`, nên một PR từ nhánh khác vẫn không được đo trước merge. Có thể mở cả branch filter và tái thiết kế workflow cho `pull_request`, nhưng đó là đường đắt và nguy hiểm hơn: job hiện có `contents: write`, `issues: write`, logic tìm lease theo push event và bước đăng/ghi ngược. Tách một workflow read-only mới cuối cùng chỉ tái tạo vai trò mà `ci.yml` đã có.

Có trùng lặp có chủ đích với bước `tự kiểm cổng trước khi tin nó` trong `ops-publish-lease.yml`, nhưng hai lần chạy bảo vệ hai biên khác nhau:

- CI bảo vệ tính hợp lệ của cây sắp vào master.
- Workflow đăng lease chạy bộ test **neo từ default branch** ngay trước thao tác có quyền ghi/comment, bảo vệ đường công bố.

Không nên bỏ lần thứ hai chỉ vì CI có lần thứ nhất: lease workflow phải tự chứng minh bản neo tại thời điểm đăng, và một commit master xanh trước đó không chứng minh trạng thái/runtime của lượt đăng sau.

Master đỏ vì bất biến `ops/` thật sự hỏng là đúng chủ đích, kể cả commit không đổi lease. `workflow_dispatch` trên ref cũ/hỏng cũng đỏ đúng theo cây được chọn. Tình huống đỏ không thuộc nội dung cây là cài dependency từ mạng thất bại hoặc PyYAML tương lai không tương thích; phần trôi phiên bản là finding dưới đây.

## 3. `pip install pyyaml` không ghim — ĐÃ ĐO BẢN HIỆN TẠI, RỦI RO TƯƠNG LAI CHƯA THỂ ĐO

finding_id: `unpinned-pyyaml-ci-dependency`

Mức: thấp, không chặn land.

Tái lập trạng thái dependency:

```bash
rg -n 'pip install --quiet pyyaml' .github/workflows
# ci.yml:123 và ops-publish-lease.yml:80 đều là spec trần
python -m pip index versions PyYAML
# latest 6.0.3; installed 6.0.1 tại môi trường review
```

Tôi tạo venv sạch, cài `PyYAML==6.0.3`, rồi chạy suite: `rc=0`, `30/30`, 3.443 giây. Vì vậy không có lỗi tương thích với bản phát hành hiện tại. `lease_publish.py` và test chỉ dùng API công khai, bảo thủ (`safe_load`; không có `safe_dump` trong hai tệp hiện tại), nên xác suất gãy trong một minor 6.x thấp. Một major tương lai vẫn có quyền đổi API, hành vi resolver hoặc yêu cầu Python; spec trần sẽ tự nhận major đó. Đây cùng lớp với tiền lệ `pypdf>=4.0` không có trần: cùng SHA có thể xanh hôm nay và đỏ sau này mà cây không đổi.

Sửa tối thiểu phù hợp phạm vi hiện tại là dùng cùng một spec có trần ở **cả hai** workflow, ví dụ:

```yaml
run: python -m pip install --quiet 'PyYAML>=6.0,<7'
```

(`python3` giữ nguyên ở workflow ops nếu muốn giữ idiom hiện tại.) Nếu mục tiêu là tái lập byte-for-byte hơn là chỉ chặn major, dùng `PyYAML==6.0.3` và cập nhật có chủ đích. Tôi nghiêng về pin exact cho CI.

Một `requirements-ops.txt` chưa đáng thêm chỉ cho một dependency: nó thêm tệp policy, tên/scope cần duy trì và buộc cả hai workflow đổi sang cài từ tệp. Khi nhánh ops có dependency thứ hai, tách file chung sẽ đáng để loại trùng; lúc ấy vẫn phải ghi upper bound hoặc exact pin trong file — chuyển spec trần sang requirements không tự chữa rủi ro.

## Đa nền và thời gian

Linux đã đo như trên. Windows **chưa đo thật** trong môi trường review này, nên tôi không gọi nó là đạt. Đọc code cho thấy `t19_symlink_tro_RA_NGOAI_kho_thi_CHAN` bắt `OSError`/`NotImplementedError` rồi `return`; harness vẫn tính ca đó vào `30/30`. Nếu Windows runner không được phép tạo symlink, con số sẽ chứa một ca có mặt nhưng không đo. Đây là nợ có sẵn của bộ test, không do hai bước PR này tạo ra, và trên nền không thể tạo symlink thì đường tấn công ấy cũng không khả dụng; tôi ghi nhận nhưng không nâng thành finding của PR #134 khi chưa chạy Windows thật. Nên đổi harness để báo `SKIP` riêng (và không tính vào số đạt) nhằm tránh lời khai 30/30 quá rộng.

Thời gian Linux đo ba lượt là 3.504 giây (PyYAML 6.0.1), 3.591 giây (cây đột biến) và 3.443 giây (PyYAML 6.0.3). Khai 3,4 giây của tác giả gần đúng, nhưng các số trên mới là phép đo của review này.

## Bằng chứng dương do chính verdict tạo ra

Sau khi ghi tệp này nhưng không thêm hàng Mục lục, chạy:

```bash
python ops/lease_publish_test.py
echo "$?"
```

Kỳ vọng bắt buộc: `t27` nêu `pr134-ci-lease-gate-codex-verdict.md` thiếu trong cột `tệp verdict`, suite `29/30`, `rc=1`. Kết quả thật được bổ sung ngay dưới sau phép chạy.

Kết quả thật: `rc=1`, 3.305 giây, `lease_publish: 29/30 đạt`; ca đỏ là `t27` và thông điệp định danh đúng `pr134-ci-lease-gate-codex-verdict.md` thiếu trong cột `tệp verdict` của bảng `Mục lục`.
