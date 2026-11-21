Review offline MÃ wp1236 đợt A r10 — lượt 7 — **changes_requested**.

HEAD `f4f17bc4237a5362117f37b56e65209b92465f64`; tree `b78a198f57d217c6f27a081316c04040fa120a52`. Spec SHA-256 `3ee831738c70c5eabb27720e295b4953c9a9bdd1ac29a03cc7b964d28658fcdc`. Baseline nghiệm thu `010046f2141799ec6ffc9cfa1322d49df3f3f680`; ref `origin/master` của bản sao đã trôi sang `e02d748…`, nên dùng OID bất biến khớp lease theo §3.2.1, giữ nguyên ref.

Có **1 P2 và 2 P3**, thuộc **2 lớp còn mở**:

- **M01 — P2 — `test-thieu-chot`:** quét độc lập 15 mutant bằng Python/PyYAML nguyên bản: 14 sống qua đủ 40/40 ca, cả 14 có đối chứng phân biệt hành vi. Các biểu hiện gồm labels mất thứ tự/số lần lặp, URL miễn lặp bị gộp, chuẩn hoá danh tính sai, mất dấu phân cách tại consumer, chặn `./tệp`, tiền tố `GIỚI HẠN:` không được khóa và sai thư mục của hồ sơ tên thường. HEAD đúng ở các đối chứng; thiếu nằm ở nghiệm thu hồi quy. Ma trận a120 có 34 lần `kiem_tep` nhưng 0 `kiem_ho_so`; a121/a122 mỗi ca chỉ gọi consumer một phần tử. A2-10 vẫn **5/6 fixture**, chưa gọi `T-khong-prov`.
- **M02 — P3 — `hop-dong-dau-vao-dau-ra-chua-chot`:** thiếu lệnh con, thiếu `--provenance`, thiếu hồ sơ và lệnh lạ đều rc 2 nhưng stderr bắt đầu `usage:`, trái mẫu `LỖI THAM SỐ:`. Đây là lỗi đầu ra trên HEAD.
- **M03 — P3 — `test-thieu-chot`:** hai dòng ledger cần sửa phân loại: `identity_72_67` khai `KHONG_AP_DUNG → TUONG_DUONG`; `ref_no_boundary` khai `CHOT_DA_BO` dù lookbehind còn trong đặc tả. Có chứng minh tương đương trên HEAD; nên ghi đúng nhánh `TUONG_DUONG`, giữ ID và lịch sử.

Hướng sửa chung: dùng cùng bảng miền qua helper và consumer, giữ đối chứng đúng/sai, thêm đầy đủ mẫu CLI và sáu fixture; ghim mutant mới, đo chết đúng ca. Sửa nhãn ledger bằng chứng minh hiện hành, không cố giết mutant tương đương. Đầu ra `argparse` cần xử lý lỗi chung mà vẫn giữ `--help` rc 0. Gợi ý chỉ là hướng; reviewer không sửa branch.

| Lớp kế thừa lượt 6 | Nhãn lượt 7 | Bằng chứng |
|---|---|---|
| `yaml-ngoai-schema-bi-chan` | `DA_VA_THAT` | 5 loại YAML ngoài schema vẫn passed; a116/mutant cũ đạt |
| `k2-mat-loi-doc` | `DA_VA_THAT` | lỗi đọc/YAML/UTF8/symlink/PermissionError giữ chặn |
| `cli-vong-yaml-traceback` | `DA_VA_THAT` | vòng YAML, ENAMETOOLONG và alias dùng chung đúng |
| `test-thieu-chot` — L01/L02 và lịch sử | `VA_MOT_PHAN` | 25 mutant sống cũ đã bị giết; 14 mới sống; fixture thứ sáu vẫn thiếu |
| `mo-ta-duong-dan-lech-hop-dong` — L03 | `DA_VA_THAT` | docstring và hành vi `./tệp` khớp; `..`/tuyệt đối/symlink bị chặn |

Hội tụ **6→7 = 1/2**; **4→5 = `KHONG_DO_DUOC`**. `test-thieu-chot` nối `nghiem-thu-khong-co-lap-chot-dich` ở đặc tả, đã lặp ít nhất ba lượt: cần **Review Rescue Checkpoint** xét lại phương pháp; revision không reset lịch sử. M02 là lớp mới trong chuỗi review mã, không vào tử số/mẫu số này.

| Phép kiểm | Kết quả tự đo |
|---|---|
| Luật 1 | 40 lý do nghiệp vụ đều có target/control và mutant GIET; **chưa đạt toàn bộ** vì các mẫu CLI còn thiếu chốt |
| Luật 2 | **Đạt** 5 ô trùng ID, 5 mutant riêng chết đúng ca; ô skipped so đúng `job_lap` |
| Luật 4 | **Chưa đạt** đường consumer của ma trận |
| Luật 5 | 127 ID đã đối chiếu; 115 GIET đúng ca, 7 tương đương hợp lệ, 5 KAD đã xét riêng — **2 nhãn cần sửa** |
| Suite bắt buộc | rc 0: CA **40/40**, DOT BIEN **145/145**, TU KIEM PHAN HANG DAT (2), TONG DAT |
| Ruff bare lint | rc 0, Ruff 0.15.15, `--no-cache --select F` ba tệp |
| Đăng ký CI | rc 0: **31/31**, Ruff pin/probe **3/3**, phản chứng **1226/1226** |
| Corpus tại `8048551` | **66 = 47/10/9**; **170 = 25/56/39/50**; **94 landed, 0 lệch**; 50 script = 20/28/2 |
| Rút gọn mã | Không thấy lệch: 20.000 chuỗi regex, 968 tổ hợp dòng tổng, đối chứng encoding/skip/path; có lập luận phạm vi |
| Kích thước và diff | **3 tệp, +1454/-0 ≤1700**; cả hai phạm vi `git diff --check` rc 0 |
| Read-only | HEAD/tree giữ nguyên; **17.339** tệp tracked/untracked/ignored giữ byte hash; diff/index rỗng |

Bằng chứng chi tiết và hướng đóng từng finding ở [VERDICT.json](VERDICT.json). Kết quả độc lập: [quét](independent_results.jsonl), [đối chứng](independent_contrasts.json), [đường consumer](matrix_routes.json), [CLI](cli_probe.json), [ledger](ledger_tail_audit.json), [corpus](corpus_probe.json). [Kho mới 14 ID](kho_dot_bien_reviewer_luot7.jsonl) đã ghim cặp `ast.unparse`; [kho cộng dồn](kho_dot_bien_reviewer_luot6_va7.jsonl) giữ đủ **141 ID**.

Reviewer `openai_codex / codex_cli / machine`, session `01a1fbda-3e4c-7b40-8cde-1c315ab71ea3`, độc lập với Executor trong lease. Model/effort thực phục vụ `KHONG_DO_DUOC`; họ OpenAI lấy theo identity provider (ADR-0065). Môi trường Linux, Python 3.13.18, PyYAML 6.0.3; không cache hoặc đổi loader. Sandbox `workspace-write`; thao tác giữ repo read-only, scratch chỉ trong `work/`. Snapshot không chứng minh lịch sử ghi rồi hoàn nguyên. Không mạng/GitHub/commit/push.

**not_run:** Windows local, remote CI, LIVE/full release gate và toàn bộ scanner khuyến nghị executor. **skipped:** 0 trong kiểm Linux đã chạy. Windows local vẫn là nghĩa vụ M3 riêng; không nhận các mục chưa đo là pass. Review này không cấp quyền merge/land.

Validator `kiem_verdict_lop.py --vong 7`: **rc 0, HOP_LE (§8.3): 3 finding, 6 lop**; log ở [kiem_verdict.txt](kiem_verdict.txt).

KET_LUAN: changes_requested
