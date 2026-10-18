Reviewed commit: ab4cd428f5a01d69ead7825108593f1092fe78fd
Verdict: approve — P1=0 P2=0 P3=0

Reviewer: Codex (họ GPT/OpenAI), độc lập với executor Claude. KHO=/home/user/rv773 chỉ được đọc; mọi bản sao và đầu ra tái đo nằm trong /tmp hoặc thư mục ra. Không dùng worktree, không sửa KHO.

## Findings

Không phát hiện P1/P2/P3 trong phạm vi yêu cầu. P3 lượt 1 đã đóng: `sua_gate_master.do_sau_sua` nay trỏ tới transcript kết quả, có ba đầu ra đầy đủ, nhận diện HEAD/tree/môi trường và checksum. Bản vá nói rõ lần đo gốc không giữ transcript và đây là phép đo lại, không giả làm bản ghi lịch sử gốc.

## Đã đo

### Gate và phạm vi diff

- `git -C KHO rev-parse HEAD`: đúng SHA đầu báo cáo. `status --porcelain` rỗng trước và sau review. Đã đọc `show -s fafbe15 ab4cd42`, toàn diff `653fef3..ab4cd42` và diff vá `fafbe15..ab4cd42`; `diff --check` sạch. Toàn PR thay 7 tệp; riêng vá lượt 2 thay 6 tệp (YAML, SHA256SUMS và 4 hiện vật đo lại).
- `git -C KHO show 0f4830f:ops/land_evidence_nguon.py > /tmp/len.py`; `python3.13 -B /tmp/len.py --root /home/user/rv773`: `1 ĐẠT · 28/28 miễn trừ · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC`, `TỔNG: ĐẠT`, rc=0.
- `git -C KHO archive 653fef3 ops | tar -x -C /tmp/rv787-r2-base`, rồi cùng checker: 5 L1, vì bản chỉ có ops thiếu RELEASE_MANIFEST.json ở gốc. Bổ sung đúng tệp gốc bằng `git -C KHO archive 653fef3 RELEASE_MANIFEST.json | tar -x -C /tmp/rv787-r2-base`, chạy lại: đúng **4 L1**, tại spec.nguon, khong_xung_dot, review.codex_connector, review.human_audit; `TỔNG: ĐỎ`, rc=1. Không bỏ qua sai biệt do cách dựng đối chứng.

### Từng con trỏ và các lời khai còn lại

- Dùng `duyet`, `token_nguon`, `phan_giai` của checker trên YAML hiện tại: **14 lời khai measured**. Các token mới phân giải đúng trong provenance hoặc đúng `KHO/ops/specs/wp766.md`; không thấy trùng tên tình cờ ở ops/land hay gốc khiến trỏ nhầm nguồn. Đã mở các nguồn, không chỉ kiểm tồn tại.
- `sha256sum KHO/ops/specs/wp766.md`: `da3095b47567dc8cb94137d0cc675d722eb256a77c8e06ddb90a216e7f148666`. `rev-parse HEAD:ops/specs/wp766.md` và `rev-parse fa33fa6:ops/specs/wp766.md` cùng cho `2176dd0c04e126beb6a57be645d315f51ebb2d23`; `show fa33fa6:ops/specs/wp766.md | sha256sum` cũng khớp. `show 701f41c:ops/specs/wp766.md` thoát 128 vì spec chưa có ở commit mã đó. Hồ sơ đã nói spec vào master qua PR ghi sổ; không lấy hash stdin rỗng làm chứng cứ lịch sử và không thấy con trỏ hiện tại gây sai nghĩa.
- Tái chạy ba lệnh của `do-tree-merge-e03d4bf.txt`: `git rev-parse e03d4bf^{tree}` và `git rev-parse 701f41c^{tree}` cùng trả `861df62ee0c17abf423908c5f41ba59b2604fdb4`; `git log -1 --format=%P e03d4bf` trả `e0273d31aba78b014aa89297f32ff86f9daf0277 701f41c686cef8456d43528ab9556a6b867cd7d6`. Cả ba khớp transcript, rc=0. Readback PR #772 có base/head/merge tương ứng, merged=true, merged_at=2026-10-16T06:31:51Z. Nguồn chứng minh đúng mức “gián tiếp”.
- `readback-codex-connector-772.json`: bot chatgpt-codex-connector[bot], code_review.commit_sha=701f41c686cef8456d43528ab9556a6b867cd7d6, completed, has_any_findings=false, has_unresolved_findings=false. updated_at=06:31:29Z, trước merge 22 giây.
- `readback-comment-6209427062.json`: user ducthangho, author_association=OWNER, performed_via_github_app=null, created_at=updated_at=2026-10-16T06:20:30Z; body có human audit và ủy quyền đúng candidate.
- Các nguồn khác: check-runs bắt buộc đều success, mốc muộn nhất 05:22:34Z; toàn bộ completed_at có giá trị đều trước merge, muộn nhất 06:21:13Z. Transcript lease có hai đường dẫn rc=0, NGƯỜI_GIỮ 0, lease hết hạn; do-ref 553/553, thiếu 0. Comment verdict 6208523504 có app=claude; events ready_for_review/merged có app=null. Nguồn events hỗ trợ phần sự kiện, comment readback riêng hỗ trợ phần comment; không thấy mâu thuẫn.
- `release-verify-strict-e0273d3-tai-cho.json`: ok=true; bản e03d4bf: ok=false, extra_files chỉ changelog.d/wp-766.md, failed=[], package_hash_match=true. Run readbacks và trích log khớp gate failure, launcher success cùng head e03d4bf; các số positive khớp trích log.

### Kiểm độc lập phép đo lại trên 1a433a6

- Dựng `/tmp/rv787-r2-tree` bằng `git -C KHO archive 1a433a6 | tar -x -C /tmp/rv787-r2-tree`. Python 3.13.16. Chạy `python3.13 -B scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json`: JSON **bằng toàn bộ** JSON đã lưu; ok=true, expected=checked=187, failed/extra/missing rỗng, package_hash_match=true.
- Chạy `python3.13 -B scripts/tl.py golden-test --json --deterministic` không --write: ok=true, 20/20, mode=verify. Sau chuẩn hóa tiền tố đường dẫn và bỏ riêng raw_sha256, toàn JSON bằng bản lưu. Khác raw hash phù hợp việc hash stdout thô có dữ liệu vị trí; mã workflow.py:1716 tính hash trước audit_projection. Không nhầm raw hash với hash phép so golden.
- Selftest trên archive: rc=1, **1724/1731**, 7 ca FAIL. Tiếp tục dựng clone tạm bằng `git clone --shared --no-checkout KHO /tmp/rv787-r2-git`, checkout detached 1a433a6, config core.abbrev=7; HEAD=`1a433a690d56d6cce16312a10a35f4984e8d3644`, tree=`a623dbee938465677da535cbc00dabe5dc69012c` đúng transcript. Chạy toàn selftest: rc=1, **1729/1731**, còn r226_nguong_l2_troi_theo_abbrev_va_ci_ghim và r268_l2_trichotomy_theo_trang_thai_object. Năm chênh lệch đã mất khi có metadata Git; mã các ca xác nhận nhánh kiểm khác giữa cây Git và gói bung.
- Đo nguyên nhân hai ca còn lại: tạo mini-repo rồi `git -c user.email=t@t -c user.name=t commit --allow-empty -qm c1` thất bại ở dịch vụ ký, báo `socket: operation not permitted`, `fatal: failed to write commit object`; `git config --get commit.gpgsign` trả true. Hai ca này đều tạo commit trong mini-repo. Trích nguyên hai FunctionDef bằng AST từ đúng tl_selftest.py (không sửa thân hàm), gọi với module tl thật và `GIT_CONFIG_COUNT=1 GIT_CONFIG_KEY_0=commit.gpgsign GIT_CONFIG_VALUE_0=false`: cả hai trả **True**, rc=0. Đây là kiểm lại có mục tiêu sau khi xác định khác biệt môi trường; không tuyên bố đã có một lượt toàn suite 1731/1731 độc lập mới.
- Bản selftest được lưu có 0 `[FAIL]`, kết thúc 1731/1731; r291_docs_ngoai_goi và r357_agents_ngoai_goi đều OK trong bản lưu và các lượt tái chạy. Kết quả tái đo và đối chiếu mã không cho thấy hiện vật thuộc sai cây hay số liệu sai.
- So byte từng tệp thường của archive 1a433a6 với bản tạm sau chạy: **3.599 tệp, 0 thay đổi**. Clone tạm có `status --porcelain` rỗng sau selftest. Transcript lưu đo porcelain 0 trước/sau, chỉ đo --ignored sau và ghi rõ giới hạn đó. “Cây không đổi” được đọc theo kết luận cụ thể trong transcript: không đổi tệp theo dõi; không phải lời khai rằng mọi tệp ignored bất biến.

### Toàn vẹn và giới hạn chứng cứ

- `(cd KHO/ops/land/pr772-wp766-provenance && sha256sum -c SHA256SUMS)`: **27/27 OK**, rc=0. So tập tệp đệ quy với tên trong SHA256SUMS: chỉ chính SHA256SUMS không tự liệt kê; không thiếu tệp dữ liệu. Bốn hiện vật đo lại tổng 124.712 byte, đều có checksum.
- Đường dẫn tuyệt đối trong golden JSON là dữ liệu vị trí lần chạy, không phải con trỏ nguồn YAML cần tồn tại ở máy reviewer. Transcript dùng tên tương đối tới các hiện vật cùng thư mục; có thể mở và đối chiếu độc lập.
- Header do-tree nói “master 653fef3”: commit 653fef3 có mốc 2026-10-16T14:47:00Z, trước mốc đo 17:35:51Z. Ba lệnh không ghi HEAD/branch nên không độc lập xác nhận checkout lịch sử ấy. Kết quả của chúng không phụ thuộc checkout và đã tái đo khớp; không nâng hạn chế này thành P3.
- Bốn lời khai ban đầu giữ nguyên nghĩa. Thay đổi do_sau_sua bổ sung xuất xứ phép đo lại và giới hạn phép đo gốc, không lặng lẽ thay kết quả được khai.

## Ngoài phạm vi

- Không xác thực GitHub live hoặc nguồn gốc server của readback; kiểm nội dung lưu trong Git, quan hệ Git và checksum. Không đăng bình luận, merge, land hay sửa kho.
- Không tính các hạn chế đã khai về log CI đầy đủ, stderr review cũ hoặc model phục vụ thành finding. Không sửa các selftest hay cấu hình ký toàn cục; sai khác môi trường tái đo đã được báo rõ ở trên.
