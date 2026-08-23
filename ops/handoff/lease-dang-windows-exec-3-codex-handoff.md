# HANDOFF — `LEASE-DANG-WINDOWS` (#238), Executor lượt 3 (`codex`)

Executor đã đóng Q9/Q10 và đẩy code head. Handoff này đứng ngoài commit được review để
không tự làm đổi mỏ neo exact SHA.

## 1. Mỏ neo và ngân sách

- Branch/remote: `codex/lease-dang-windows-1`.
- Head: `b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19`.
- Tree: `1a7cfe36799a5575f93c36e329749d4269beddbc`.
- Start head: `edc1906cf01fcceb15c646e1fdc4fcd8957644ed`.
- Provider: `openai_codex`; execution surface: Codex workspace service; transport: machine;
  role: Executor; revision 3, generation 1.

`git diff --numstat ba82b06f..HEAD` trong ba tệp mã của write-set:

```text
2   4   .github/workflows/ops-publish-lease.yml
114 16  ops/lease_publish_test.py
```

Tổng: 2 tệp, 116 dòng thêm, còn 4/120. `ops/lease_publish.py` khớp byte-for-byte
`ba82b06f`; workflow không đổi so với `edc1906c`. Riêng lượt 3 chỉ đổi
`ops/lease_publish_test.py` (+38/-12 so với start head).

## 2. Hai suite và công cụ

| Phép đo | rc | Bằng chứng dương |
|---|---:|---|
| `PATH=/tmp/actionlint:$PATH python3 ops/lease_publish_test.py` | 0 | `72/72 đạt; đã chạy=72, bỏ qua=0` |
| cùng suite với `GITHUB_ACTIONS=true`, `GITHUB_REPOSITORY=ducthangho/tra-luat`, `GITHUB_ACTOR=ducthangho`, PATH không có `gh` | 0 | `72/72 đạt; đã chạy=72, bỏ qua=0`; `command -v gh` rc=127 |
| `/tmp/actionlint/actionlint .github/workflows/ops-publish-lease.yml` | 0 | workflow thuộc packet xanh |
| `/tmp/actionlint/actionlint .github/workflows/*.yml` | 1 | finding nền `ops-don-ref.yml:106 SC1003:info`, ngoài write-set, đã khai từ lượt 2 |
| `SHELLCHECK_OPTS=--severity=warning /tmp/actionlint/actionlint .github/workflows/*.yml` | 0 | cả 5 workflow không có finding warning/error |

Đã kiểm ShellCheck **trước** actionlint: `/usr/bin/shellcheck` 0.9.0. Actionlint:
`/tmp/actionlint/actionlint` 1.7.7. Không nhận lượt plain-all-five là pass và không sửa
lấn finding nền.

## 3. W9 — gỡ ca gọi thẳng rồi chạy đúng đột biến

Phép liệt kê `co_names` cho thấy ca duy nhất gọi thẳng `_ly_do_bo_qua_workflow` là
`t70_W6_matrix_co_Windows_phai_chay_lai_tam_ca`; không ca nào gọi thẳng
`_dong_tong_ket`. `t71`/`t72` gọi `main()` qua harness meta, không gọi hai helper ấy.

| Tiêu chí | Đột biến · vị trí | Ca đã gỡ | Ca còn đỏ thật | N/N · rc |
|---|---|---|---|---|
| W6′ | thay đọc YAML bằng `job = job or {"runs-on": "ubuntu-latest"}` · `ops/lease_publish_test.py:191` | `t70_W6_matrix_co_Windows_phai_chay_lai_tam_ca` | `t71_W7_workflow_khong_ubuntu_only_cam_bo_qua`; `t72_W8_bo_qua_phai_in_runs_on_va_tong_ket` | `69/71`, rc=1 |
| W7′ | thay khối phân loại bằng `bo_qua.append((fn.__name__, str(ex)))` · `ops/lease_publish_test.py:2654` | `t70_W6_matrix_co_Windows_phai_chay_lai_tam_ca` (ca gọi thẳng helper dùng chung) | `t71_W7_workflow_khong_ubuntu_only_cam_bo_qua`; `t72_W8_bo_qua_phai_in_runs_on_va_tong_ket` | `69/71`, rc=1 |
| W8 | bỏ vòng in `for ten, ly in bo_qua: print(...)` · `ops/lease_publish_test.py:2665` | không có ca gọi thẳng `_dong_tong_ket` | `t72_W8_bo_qua_phai_in_runs_on_va_tong_ket` | `71/72`, rc=1 |

Mỗi mutant nằm trên bản sao tạm riêng dưới `/tmp/lease-w9.peaRre`; tệp thật không bị
sửa rồi khôi phục. W6′, W7′, W8 và W9 đều ĐẠT phép đo r3.

## 4. Ba phản chứng P1 bắt buộc

| Phản chứng | Đột biến · vị trí | Ca đỏ thật | N/N · rc |
|---|---|---|---|
| P1-1 | bơm `raise BoQuaNen()` không mỏ neo tại `_chay_buoc_dang` · `ops/lease_publish_test.py:2303` | `t51`, `t52`, `t59`, `t60`, `t62`, `t63`, `t66`, `t68` | `64/72`, rc=1 |
| P1-2 | hằng số trá hình thay đọc tệp · `ops/lease_publish_test.py:191` | `t71_W7_workflow_khong_ubuntu_only_cam_bo_qua`; `t72_W8_bo_qua_phai_in_runs_on_va_tong_ket` | `70/72`, rc=1 |
| P1-2(b) | cùng hằng số + YAML job `dang` đổi sang matrix `[ubuntu-latest, windows-latest]` · `ops/lease_publish_test.py:191`, `.github/workflows/ops-publish-lease.yml:73` | `t71_W7_workflow_khong_ubuntu_only_cam_bo_qua`; `t72_W8_bo_qua_phai_in_runs_on_va_tong_ket` | `70/72`, rc=1 |

Chuỗi Ubuntu trong `t72` được dựng lúc chạy bằng prefix + tên tạm ngẫu nhiên, ghi vào YAML
thật, rồi chỉ được chấp nhận khi chính chuỗi ấy xuất hiện trong stdout của `main()`.
Đối chứng `windows-latest` ở `t71` phải làm lượt main lồng đỏ.

## 5. Tiêu chí chưa đạt

- Gate plain `actionlint` trên cả 5 workflow: **KHÔNG ĐẠT**, rc=1 do
  `.github/workflows/ops-don-ref.yml:106 SC1003:info`. Đây là finding nền ngoài write-set
  đã có trong handoff lượt 2; P2/P3 bị cấm nên Executor không sửa.
- W3′ trên **head mới**: chưa đạt/chưa chạy. Bằng chứng run `32558427472` chỉ neo
  `edc1906c`, không chuyển sang `b0c8fb3`. Phiên điều phối phải chạy workflow_dispatch
  thật trên exact head trước land.
- Không có tiêu chí Q9/Q10/W6′/W7′/W8/W9 nào không đạt.

## 6. `chua_do_duoc`

- Windows thật trên `b0c8fb368d70f17bce5eb7e3d1fe02d810db8e19`.
- ShellCheck có mặt hay không trên runner `windows-latest` thật.
- Nguyên nhân gốc thật của tám ca Windows và nội dung argv thật của `t49`.
- `gh` thật; kế thừa packet trước.

W3′/W4/W5 cũ không được chạy lại theo chỉ thị lượt 3. W4/W5 giữ kết luận đã có; riêng
W3′ bắt buộc có run mới vì head đã đổi. Không chạy LIVE, merge, land hoặc deploy.
