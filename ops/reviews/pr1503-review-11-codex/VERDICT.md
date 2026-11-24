# Verdict PR #1503 lượt 11 — Codex

reviewed_sha: 74fbf22a113e40cfa75d75e8ceaf6a3fd988d388
reviewed_tree: 76cd65b083303f13fa730f23147b3694c0f39c23
base_sha: a03a28ef076503c7fe93c208a4998c32590a977f
base_tree: 1c3dfd0b5363745cb27ca976cb37ae865aeb2ebe
nang_tran: chủ kho nâng trần lên 11 (lời gọi thứ 11, cuối cùng), lượt kiểm chứng

## Neo review

- Checkout riêng, detached, origin nhận diện `ducthangho/tra-luat`. `git merge-base HEAD a03a28e` trả đúng base đã giao. Ref `origin/master` cục bộ dừng ở `5259239d763c9ffc1677f033bd9a9cf23ede9299`, cha thứ nhất của base, khớp tình trạng đã được ghi ở lượt 9. So diff và chạy đối chứng theo hai OID đã đóng băng. `7bcb4bb` và HEAD chỉ khác ba tệp hồ sơ lượt 10.
- Chỉ thị là prompt snapshot lượt 11, dẫn quyết định chủ kho ở comment PR `7136813807`. SHA-256 `671ae88898882844a3e113c98dfec99407d4d4eaa69638200aecd7195e5b0fe2` khớp run và checkpoint. Checkpoint neo exact HEAD, SHA-256 `0ee31b157aa3938e7757fd847df754678802dcf7d3075831ef9fa83058c853f4` khớp run. Xử lý theo lớp `sensitive` vì diff đi qua launcher và xác thực. Phạm vi ghi gồm verdict trong checkout và khu vực tạm bên ngoài.
- Run `2eb962bb1707433a91cdd9d932b9a655` ghi `openai_codex / codex_cli / machine`. Linux x86_64, Bash, Python 3.13.18, Git 2.43.0, Codex CLI 0.172.0, sandbox `workspace-write`. Model và effort phục vụ `KHONG_DO_DUOC`. SHA-256 diff toàn PR `509d958646488115608fa138af65975922b77db31606838b9baa059ef53a819e`. SHA-256 diff vá V1 `782f1edff855fcb3497aba350c9afc35c83b9eaadfb48d13bb1399356fa00b00`.

## Đối chiếu (V1 và các lớp lượt 9 kết luận)

Nguồn đối chiếu là lượt 8 trên `a93b8f3069cd845468545fa79c501a2a6a1782f0` và lượt 9 trên `50d151899ae528e2a7e4dbc67288b092c0961cd5`. [Lượt 8](../ops/reviews/pr1503-review-8-codex/VERDICT.md) · [Lượt 9](../ops/reviews/pr1503-review-9-codex/VERDICT.md)

| # | Trạng thái | Bằng chứng |
|---|---|---|
| V1 | ĐÃ VÁ THẬT cho dấu kép góc và đơn cong ở lượt 9. VÁ HỜ ở cấp lớp, P1. | `_dong_mo_ho` trả về mơ hồ với dấu ngoài tập thuộc `Ps/Pe/Pi/Pf` hoặc được ghi riêng trong `_DAU_KEP_PO`. `tach_khoan` chạy chốt trước phân đoạn. Ca sẵn có xác nhận bảy cặp ngoài danh sách, gồm hai mẫu V1. Ba đột biến V1 làm ca này đỏ. Nháy đơn thẳng ASCII vẫn lọt. Xem X1. |
| U1 | ĐÃ VÁ THẬT ca gốc. CÒN MỞ với nháy kép thẳng lồng. | `ca_nguon_mo_ho_luot8` gồm hai mẫu nháy kép cong lồng, kể cả một mẫu cân số dấu. Ca đỏ khi bỏ chốt dấu mở cong lồng. Với nháy kép thẳng, hai bộ quét vẫn đổi trạng thái qua mỗi dấu. Xem X2. |
| U2 | ĐÃ VÁ THẬT trong phạm vi mô phỏng. | `ca_sau_khoi_chay_khong_chuyen` dùng tiến trình Python thật và ép nhánh Windows. Ca kiểm `returncode` và ghi nhận việc đóng pipe trước khi tự dọn. Đột biến `dong_ong_tren_windows` làm ca đỏ. Windows bản địa chưa đo. |
| U3 | ĐÃ VÁ THẬT ca gốc. | Số đầu dòng kế tiếp trong mẫu trích dẫn kép cong bị chặn vì dòng trước chưa khép dấu. Ca đích đòi cả `tach_khoan(...) is None` và `lech == [0]`. Đột biến bỏ kiểm trích dẫn hoặc ngoặc mở qua dòng đều bị bắt. |
| `ranh-gioi-khoan` | CÒN MỞ, P1. | Kiểm đúng số mục, thứ tự và cả hai vế khi phân đoạn đúng. Ranh giới sai vẫn có thể trở thành chuẩn đối chiếu ở X1–X3. |
| `thu-hoi-tien-trinh-sub` | ĐÃ VÁ THẬT trong phạm vi đã đo. | Ca có sẵn chạy timeout và lỗi đọc trên Linux, đòi thu hồi tiến trình khi lỗi đọc. Đột biến bỏ `wait` bị bắt. Xem U2 về mô phỏng nhánh Windows. |
| `phan-loai-sub` | ĐÃ VÁ THẬT trong phạm vi đã đo. | Ca sẵn có chạy đối chứng spawn hỏng chuyển sang API giả. Sau spawn, timeout, lỗi I/O, mất envelope và envelope báo lỗi bị buộc dừng với API giả bị cấm. Mã định tuyến chỉ chuyển đường khi bắt `ChuyenDuong`. |

## Findings mới

### X1 [P1] Dấu nháy đơn thẳng nằm ngoài cả bộ quét và cổng từ chối — scripts/tl_core/llm_route.py:542–561,582–620

Khi một thuật ngữ chứa cụm trích dẫn bằng nháy đơn thẳng ASCII và cụm đó có từ “là” trước từ nối của khoản, cổng nhận dòng. Dấu nháy `U+0027` thuộc nhóm Unicode `Po` và vắng mặt trong `_DAU_KEP_PO`. `_quet` không mở trạng thái trích dẫn tại dấu ấy nên `_tu_noi` có thể lấy từ “là” bên trong cụm. `lech_nguyen_van` dùng chính ranh giới đó để xác minh cả hai vế. Nếu model chọn cùng ranh giới sai, handler có thể trả `ok=true`, rc 0 và ghi kết quả vào `--out`. Đây là phần còn mở của V1, xác định bằng đọc mã. Đề xuất cho cổng bảo thủ từ chối dấu nháy đơn thẳng trước phân đoạn và rà phạm vi các ký tự có thể dùng làm dấu trích dẫn nằm ngoài bốn nhóm Unicode đã xét.

### X2 [P1] Nháy kép thẳng lồng có thể được đọc thành hai trích dẫn độc lập — scripts/tl_core/llm_route.py:553–600

Khi OCR hoặc bản text làm phẳng cả hai tầng nháy thành nháy kép thẳng, hai bộ quét ghép bốn dấu lần lượt thành hai cặp. Phần giữa dấu thứ hai và thứ ba bị coi là ngoài trích dẫn dù trong văn bản nó vẫn thuộc trích dẫn ngoài. Nếu phần đó chứa từ “là”, `_tu_noi` có thể chọn sai từ nối và `lech_nguyen_van` xác nhận cách cắt sai. Chốt lồng hiện chỉ nhận dấu mở cong trong cặp cong. Đề xuất dùng cấu trúc của nguồn để xác định vai trò dấu hoặc từ chối dòng khi các dấu đối xứng cho nhiều cách hiểu có tác động đến ranh giới.

### X3 [P1] Phân đoạn theo dòng có thể bỏ hoặc tách sai khoản — scripts/tl_core/llm_route.py:67–69,485–531,633–650

- Bản chép văn bản có thể nhập tiêu đề Điều và khoản đầu mất số vào cùng một dòng. Regex chỉ kiểm tiền tố tiêu đề và `tach_khoan` bỏ cả dòng. Nếu các khoản sau mỗi khoản một dòng, chúng được đánh số lại từ 1. Kết quả bỏ khoản đầu có thể qua kiểm. Nhánh câu dẫn cũng bỏ mọi dòng đầu kết thúc bằng hai chấm và thiếu từ nối hợp lệ, kể cả khi dòng ấy thực chất là phần đầu của khoản.
- Trong nguồn mất số, một khoản dài có thể bị ngắt ngay trước một mệnh đề phụ có chủ ngữ và chữ “là” riêng. Nếu cả hai dòng có từ nối và hai vế hợp lệ theo bộ quét, `tach_khoan` tạo hai mục và `lech_nguyen_van` xác nhận cả hai. Phép kiểm hiện có chặn dòng gãy khi ít nhất một mảnh không tạo được cặp thuật ngữ và định nghĩa.
- Trong nguồn có số, một tiểu mục đánh số bên trong khoản cuối có thể bắt đầu bằng đúng số khoản kế tiếp. Sau khi bỏ thụt dòng, `_RE_SO_KHOAN` nhận nó là khoản mới trước khi xét tiếp dòng. Nếu cả hai thân đều qua kiểm từ nối và dãy số vẫn liên tục, số thứ tự cũng không phát hiện việc tách sai.

Đề xuất chỉ bỏ tiêu đề và câu dẫn khi cả dòng được nhận diện chắc chắn. Lấy ranh giới và cấp đánh số khoản từ cấu trúc đoạn gốc. Khi nguồn chỉ còn text, từ chối chỗ không phân biệt được ngắt đoạn với ngắt dòng hoặc khoản với tiểu mục.

### X4 [P2] Phép so khoảng trắng có thể làm mất xuống dòng của điểm — scripts/tl_core/llm_route.py:465–468,536–537,635–649,754–757

Prompt yêu cầu giữ xuống dòng của điểm. `_gon` gộp mọi khoảng trắng trong cả vế nguồn lẫn vế model trước khi so. Model có thể trả đầy đủ chữ và dấu câu nhưng gộp các điểm cùng dòng. Handler xuất chính các trường của model, nên JSON có thể mất định dạng điểm dù kiểm đạt. Đề xuất lấy các span đầu ra từ nguồn đã phân đoạn hoặc kiểm riêng các xuống dòng mang dấu điểm.

### Mốc chuyển đường

`_chay_co_moc` chỉ tạo `KhongKhoiChay` khi lời gọi `Popen` ném `OSError`. Sau khi đã nhận đối tượng tiến trình, lỗi `communicate` đi vào nhánh thu hồi. `duong_sub` chuyển timeout và lỗi I/O sang `Dung`, rồi kiểm envelope, model, usage và dữ liệu theo hướng dừng. `goi` chỉ thử đường kế tiếp khi bắt `ChuyenDuong`. Kiểm schema, nguyên văn và ghi kết quả chạy ngoài vòng này. Đọc đường gọi mặc định không thấy nhánh nào gọi `api` sau khi `Popen` của `claude -p` đã trả tiến trình. [llm_route.py:96–118](../scripts/tl_core/llm_route.py#L96) · [llm_route.py:319–403](../scripts/tl_core/llm_route.py#L319) · [ops_misc.py:3089–3135](../scripts/tl_core/ops_misc.py#L3089)

## Kết quả test và đột biến

Chạy trên bản sao detached của exact SHA, `core.abbrev=7`, với HOME, cache và vùng tạm riêng. Dùng môi trường tối giản, proxy loopback, Git chỉ transport file. Các tên `claude`, `gh`, `codex` và `gws` trong PATH của test trỏ tới executable cục bộ trả lỗi. Lệnh, mã thoát, OID/tree và stdout/stderr được lưu trong `/tmp/pr1503-review11.R7DO6I/logs/`. Bảy phép kiểm ngắn cho cùng kết quả ở cả hai lần chạy.

| Lệnh | Trạng thái | Bằng chứng |
|---|---|---|
| `python scripts/tl_core/llm_route_test.py` | `passed`, rc 0 | 48/48 ca và 82/82 đột biến bị bắt. |
| `python .claude/dev/launcher_test.py --lap-ca t162 --lan 1` | `passed`, rc 0 | 1/1, 0 bỏ qua, 0 hỏng. |
| `python .claude/hooks/pretooluse_guard.py --kiem-bang` | `passed`, rc 0 | 108 writer, 93 lệnh đọc, help 26/26 chương trình, 425 cờ xác nhận, 35 cờ được công cụ ghi là chưa đo. |
| `python scripts/tl_core/command_registry_test.py` | `passed`, rc 0 | 10/10, `OK`. |
| `python scripts/tl.py --deterministic workflow-audit --strict --json` | `passed`, rc 0 | `ok=true`, 26 cards, 0 lỗi, 0 cảnh báo. |
| `python scripts/tl.py --deterministic golden-test --json` | `passed`, rc 0 | `ok=true`, 20/20. Một ca có byte thô khác ở `snapshot_age_s`, trường biến động đã khai. Bản chiếu của ca ổn định và khớp fixture. |
| `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | `passed`, rc 0 | `ok=true`, 187/187. Băm gói khớp `59660eafdc0177778b0310098b4eaf449e6124d3110d414261eba1010e6d79f6`. |
| `python scripts/tl.py --selftest`, lần đầu | `failed`, rc 1 ở cả hai mốc | HEAD 1774/1789. Base 1771/1786. Cùng 15 ID đỏ, 0 ID đỏ riêng ở mỗi mốc. Cả ba ca `r380_*` đạt trên HEAD. |
| `python scripts/tl.py --selftest`, lần đo lại | `failed`, rc 1 ở cả hai mốc | HEAD 1775/1789. Base 1772/1786. Cùng 14 ID đỏ, 0 ID đỏ riêng ở mỗi mốc. Cả ba ca `r380_*` đạt trên HEAD. |

Lần đầu, tôi ghim `core.abbrev=7` bằng biến cấu hình Git truyền cho tiến trình con. Ghim này có ưu tiên cao hơn cấu hình của kho con, làm ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` đỏ ở cả hai mốc. Sau khi chuyển ghim sang tệp cấu hình Git trong HOME tạm, ca tự đặt được 7 và 8 ở repo fixture và đạt trên cả hai mốc. Mười bốn ca đỏ còn lại trùng nhóm lỗi môi trường đã ghi trong prompt. `/tmp/.git` hiện diện và rỗng. Đối chiếu đa tập ID cho tám ca `r973_bootstrap_*`, năm ca `wp433_*` và `wp727_tl_gws_refresh` đỏ chung. SHA-256 stdout lần đo lại của HEAD là `fd0ebd9e88a8b22294b784812bc006940eb928362548f1eb29979e7bb86437e0`, của base là `1876f2eb29975b47932412443188fa6a6c4112a95c3c8aeec32d8866c78db8cf`.

`DOT_BIEN` chỉ tính một đột biến bị bắt khi neo áp được đúng một lần, module nạp thành công và đúng ca đích ném `TinHieuChotCa`. Cả ba đột biến V1 (`cho_dau_ngoai_danh_sach`, `chi_xet_pi_pf`, `bo_dau_kep_po`) được tính qua điều kiện đó. Trong thứ tự mẫu hiện có, mẫu kép góc kiểm chốt tổng, mẫu ngoặc vuông kiểm `Ps/Pe`, mẫu nháy kép toàn chiều kiểm tập `Po`. Phần `Po` chỉ có một kiểu dấu được đo trực tiếp trong bảng mẫu. [llm_route_test.py](../scripts/tl_core/llm_route_test.py#L785)

Đọc lại checkout cuối lượt cho đúng SHA và tree đầu lượt. Hai phép `git diff --quiet` và `git diff --cached --quiet` đều rc 0. Trạng thái đầu và cuối chỉ chênh tệp verdict ngoài index. Thư mục `.codex/` đã được ignore từ đầu.

## Không đo được

- `not_run` cho các tình huống X1–X4 và tình trạng xuất hiện của chúng trong corpus. Các finding mới dựa trên đọc mã và không có fixture mới trong phạm vi lượt này.
- `not_run` cho Windows bản địa, gọi Claude/Anthropic thật, đối soát billing và CI từ xa. Ca nhánh Windows trong suite là mô phỏng trên Linux.

VERDICT: REQUEST_CHANGES
