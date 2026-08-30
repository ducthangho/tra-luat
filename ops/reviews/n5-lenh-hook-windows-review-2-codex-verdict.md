verdict: approve
reviewed_sha: 472f11bd96e7e10779a0681fa1b52a93df85ee9d
luot: 2

## ĐỐI CHIẾU LƯỢT TRƯỚC

### P1 — lease còn neo vào base: ĐÃ VÁ THẬT

Tôi đọc blob đang ở `master/`, không dùng bản khai trong hồ sơ. `reviewed_sha_required` hiện là
`472f11bd96e7e10779a0681fa1b52a93df85ee9d`; thay đổi này nằm trong commit `61b7678`, đã vào
master qua merge `8b4e25d`. Bốn ô được sửa cùng commit:

```text
codex_review_calls_used: 1
review_rounds_used: 1
ngan_sach_kich_thuoc.da_dung: 158
ngan_sach_do_windows.ci_dispatch_da_dung: 2
```

Đối chứng độc lập: verdict lượt 1 hợp lệ là một lần gọi/một vòng; `git diff --numstat
1dedb8b5 472f11bd` cho đúng `158 5` trên một tệp; bundle có hai log Windows khác nhau
(`job 99198878779` và `job 99207635597`) ứng với lượt vân tay và lượt xanh. Bundle offline
không chứa danh sách toàn bộ workflow runs, nên tôi xác nhận dương được hai lượt dispatch,
nhưng không thể chứng minh mệnh đề phủ định “không có lượt thứ ba” chỉ từ hai log này. Hạn chế
đó không làm neo exact-head quay lại base và không làm sai hai hiện vật dispatch đã giao.

### P2 — số ref mơ hồ, thiếu manifest: ĐÃ VÁ THẬT

Tôi tự chạy cả hai chiều:

```text
comm -23 ref_sandbox.txt ref_github.txt  # rc=0, 0 dòng
comm -13 ref_sandbox.txt ref_github.txt  # rc=0, 0 dòng
```

`kho.git` hiện có 268 `refs/heads` và 39 `refs/tags`, tổng `show-ref` là 307; hai manifest
mỗi tệp có 268 tên và byte-identical. `git show-ref --verify refs/heads/HEAD` trả rc=128,
nên ref giả đã bị xoá. Cách trình bày mới tách rõ “268 nhánh” khỏi “307 ref mọi loại” và có
manifest đối chứng; việc số nhánh trôi 267 → 268 không tái sinh lỗi cũ.

## BẢNG ĐO

| Mục | Phép đo độc lập đã chạy | Kết quả |
|---|---|---|
| Exact head/master | `rev-parse`, `merge-base --is-ancestor`, `diff --quiet ... -- subagent_ghi_detect_test.py` | head review đúng `472f11bd…`; là tổ tiên master, rc=0; nội dung tệp ở master giống head, rc=0 |
| A1/A6 log vân tay | đếm byte bằng Python và đếm `VANTAY` | 1904 dòng nội dung, 1903 LF, dòng cuối không LF; đúng 266 dòng `VANTAY` |
| A1 nguyên nhân | bỏ NUL UTF-16 rồi đọc các dòng vân tay | `bash-which` là Git Bash; tên trần `bash --version` phóng WSL, stdout báo không có distro, rc=1; cả bốn tổ hợp đều lưu stdout |
| A2 | đọc log xanh | `t21 ... dung 4/4` ở dòng nội dung 1080; không có runner Windows để chạy lại |
| A3 | chạy gate mới ở `cay/` và `master/` | `ms1_bo_nhanh_du_phong_project_dir` bị giết; ca đích đỏ `dung 2/4` |
| A4/S7 | `python -B .claude/hooks/subagent_ghi_detect_test.py` ở `cay/`, `nen/`, `master/` | cả ba rc=0, `CA 30/30`, `DOT BIEN 18/18`, `TONG: DAT` |
| A5 | đọc log xanh | đúng 2 dòng `CI_DANG_KY … ĐỎ`, chỉ mcp_gh/pretooluse_guard; `21/21`, `chan=19 cach_ly=2` |
| A6 log xanh | đếm byte bằng Python | 1187 dòng nội dung, 1186 LF, dòng cuối không LF; dòng đầu 04:38:33Z, registry ở dòng 856 |
| S1/S2/S3 | `git diff --name-only`, `--numstat`, `--check` base→head | một tệp, `+158/−5`, không workflow, `diff --check` rc=0 |
| Spec | `sha256sum DAC_TA.md` | `930b12ef41aa58e2efa42473518466de547dac0cd3df3090f2467e3b6579a557` |

## THỬ LẬT BỐN KẾT LUẬN MÃ

1. Tôi dùng log vân tay mới để thử bác việc chọn đường tuyệt đối. Dữ liệu cho thấy hai cơ chế
   phân giải thật sự bất đồng: `which` chọn Git Bash, còn tên trần do CreateProcess chọn vỏ WSL
   và chết trước lệnh hook. Đường tuyệt đối loại nhiễu của wrapper, không bỏ một chiều sự kiện
   hay môi trường nào khỏi khẳng định.
2. Tôi chạy lại mã hiện tại và đọc log Windows mới: khẳng định vẫn tính `2 sự kiện × 2 nền = 4/4`.
3. Tôi chạy mutant `ms1`: nó làm đúng ca `t21` đỏ `2/4`, không lấy tín dụng từ lỗi vô can.
4. Tôi import đúng mã ở head, thay `shutil.which` trả `None`, rồi gọi `t21`: kết quả là `False`
   với `KHONG DO DUOC ... Trang thai thu ba CO TEN ... la DO, KHONG lam tron len`.

Giới hạn “in đúng một lần”: lần hỏng thật đầu tiên tích luỹ `_van_tay_lenh` cho cả bốn tổ hợp
rồi in cùng vân tay nền; cờ chỉ chặn các lần gọi lại trong cùng tiến trình và nhánh
`doi_lenh is not None` chỉ là mutant có lỗi mong đợi. Vì vậy nếu `t21` hỏng trên nền mới, log
vẫn chỉ ra tổ hợp, rc, stdout và stderr của lần hỏng thật đầu tiên; không thấy mất bằng chứng
chẩn đoán do chống flood.

## FINDING

Không có finding P1/P2/P3 mới về mã hoặc hai bản vá lượt trước.

## CAVEAT VỀ CỔNG ĐÃ BỊ ĐI VÒNG

PR #407 đã được merge khi verdict lượt 1 còn `changes_requested`, trước khi lượt cuối này tồn
tại. Verdict `approve` này chỉ nói rằng exact SHA nêu trên đạt đặc tả theo các phép đo hiện có;
nó không hồi tố biến lần land đó thành một lần land có cổng. Ngoài ra, approval khác danh tính
có thân rỗng không phải hiện vật “ghi evidence audit” theo §8. Vì thế assurance audit của thao
tác land đã xảy ra vẫn thiếu, dù mã tại exact SHA được approve ở lượt review cuối.

Không đo được trong sandbox: harness Claude Code trên Windows thật; chạy lại trên
`windows-latest`; danh sách workflow runs đầy đủ để chứng minh không có dispatch thứ ba; nội
dung audit ngoài các artifact đã giao. Các mục không đo được không được đọc thành ĐẠT.
