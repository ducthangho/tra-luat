verdict: changes_requested
reviewed_sha: 472f11bd96e7e10779a0681fa1b52a93df85ee9d
luot: 1

## BẢNG ĐO

| Khẳng định | Ai khai | Tôi tự đo trong sandbox | Kết quả |
|---|---|---|---|
| A1: vân tay chỉ ra Git Bash qua `PATH` nhưng tên trần phóng vỏ WSL | executor/HO_SO | Log được giao là lượt cuối xanh nên không có khối `VANTAY`; sandbox không có Windows và không có log đầy đủ job `99198878779` của lượt vân tay | KHÔNG ĐO ĐƯỢC độc lập; không đọc thành ĐẠT |
| A2: Windows `t21` đạt `4/4` | executor | `rg -n 't21_lenh' windows_job_99207635597.log` cho dòng 1080: `dung 4/4`; không có runner Windows để chạy lại | Khớp log; KHÔNG chạy lại được trên Windows |
| A3: `ms1_bo_nhanh_du_phong_project_dir` làm `t21` đỏ | executor | Tự chạy `python -B .claude/hooks/subagent_ghi_detect_test.py` trong `cay/`: `GIET ... dung 2/4`; rc=0 toàn bộ. Đếm neo trong hai command settings: `[1, 1]`, mỗi command cũng có đúng một `git rev-parse --show-toplevel` | Khớp; đột biến có răng và neo trôi thì bị khai sống |
| A4: head và base đều `30/30`, `18/18`, rc=0 | executor | Tự chạy cùng lệnh trong `cay/` và `nen/`; cả hai in `TONG: CA 30/30 dat · DOT BIEN 18/18 bi giet`, `TONG: DAT`, rc=0 | Khớp, không hồi quy |
| A5: đúng 2 dòng đỏ, không có bộ subagent; đăng ký/trạng thái giữ nguyên | executor | Log có đúng 2 dòng `CI_DANG_KY ... ĐỎ` (mcp_gh và pretooluse_guard), không có subagent; `ĐĂNG KÝ: 21/21`, `TRẠNG THÁI: chan=19 cach_ly=2` | Khớp; `TỔNG: ĐỎ` là kết quả đã khai trước, không phải finding |
| A6: log đủ 1187 dòng, mốc đầu trước bước 13 | executor | Python: `len(splitlines())=1187`, 1186 LF và dòng cuối không có LF; dòng đầu `04:38:33.4915410Z`; bước registry ở dòng 843, `04:47:15.1957325Z` | Khớp phần nội dung/timestamps. `original_length=1187` là metadata ngoài file nên KHÔNG ĐO ĐƯỢC độc lập từ artifact này |
| S1/S2/S3: 1 tệp, `+158/-5`, trong write set, không workflow | executor | `git diff --name-only/--numstat base head`: chỉ `.claude/hooks/subagent_ghi_detect_test.py`, `158 5` | Khớp |
| S6: master trôi tới `f8eb9293`, chỉ lease/spec, không đụng write set | executor | `merge-base --is-ancestor base f8eb9293` rc=0; `git diff --name-only base f8eb9293` chỉ hai đường `ops/leases/**`, `ops/specs/**` | Khớp |
| S7: không hồi quy | executor | Phép A/B trực tiếp nêu tại A4 | Khớp |
| Băm đặc tả | executor | `sha256sum DAC_TA.md` và blob spec tại `f8eb9293` đều cho `930b12ef41aa58e2efa42473518466de547dac0cd3df3090f2467e3b6579a557` | Khớp |
| 267/267 ref, `comm` rỗng hai chiều | executor | `git --git-dir=kho.git show-ref \| wc -l` cho **307**, không phải 267; không có manifest ref thứ hai trong hồ sơ để tự chạy `comm` | Không khớp / phần `comm` KHÔNG ĐO ĐƯỢC |
| Không phân giải được `bash` phải đỏ có tên | executor | Import test, thay tạm `shutil.which=lambda _: None`, gọi trực tiếp `t21`: trả `(False, 'KHONG DO DUOC: ... Trang thai thu ba CO TEN ... la DO, KHONG lam tron len.')` | Khớp, không làm tròn xanh |
| Vân tay chỉ in một lần mỗi tiến trình | executor | Đọc nhánh `if xau and doi_lenh is None and not _VAN_TAY_DA_IN`: chỉ chặn bản chạy lại/đột biến; lần hỏng thật đầu tiên vẫn in đủ `_van_tay_nen_chay()+van_tay`; đột biến settings cố ý không in | Không thấy mất bằng chứng chẩn đoán so với mục tiêu đã khai |

## FINDING

### P1 — Xin review khi lease vẫn neo vào cây base, trái điều kiện bắt buộc của chính lease

Lease được giao và blob lease đang ở `master` đều chưa dời neo:

```text
reviewed_sha_required: 1dedb8b52e857e397c74084359d6e0e39b5734c4
```

Trong khi head xin review là `472f11bd96e7e10779a0681fa1b52a93df85ee9d`. Chính cặp neo nguyên văn trong lease quy định:

```text
BẮT BUỘC dời sang exact head TRƯỚC khi xin review hoặc land
Để nguyên giá trị này rồi xin duyệt là xin duyệt một cây KHÔNG chứa việc đã làm
```

Phép đo đã chạy:

```text
git --git-dir=kho.git show f8eb9293:ops/leases/n5-lenh-hook-windows-exec-1-claude-20260830.yaml \
  | rg 'reviewed_sha_required'
reviewed_sha_required: 1dedb8b52e857e397c74084359d6e0e39b5734c4
```

Do đó chuỗi assurance chưa cho phép phát hành approval cho head, dù các phép đo hành vi của patch đều đạt. Cần cập nhật biên nhận/lease qua đường thẩm quyền hợp lệ để neo exact head `472f11b…`, rồi xin lượt review còn lại theo bộ đếm cứng.

### P2 — Số ref được khai trong hồ sơ không khớp artifact

Phép đo đã chạy:

```text
git --git-dir=kho.git show-ref | wc -l
307
```

Hồ sơ khai `267 ref` và `267/267 ref, comm rỗng hai chiều`, nhưng không giao manifest đối chứng để chạy `comm`. Sai lệch 40 ref không tự chứng minh patch sai, song làm hỏng lời khai về độ đầy đủ/provenance của ảnh chụp. Cần sửa con số theo artifact thực hoặc giao hai manifest và lệnh đối chiếu tái lập được.

Không có finding về việc rút ruột `t21`: dùng đường dẫn Git Bash đã phân giải loại bỏ sai khác tìm executable của `CreateProcess` nhưng vẫn giữ đủ ma trận `2 × 2`; đột biến settings chứng minh nhánh dự phòng còn được canh.
