# Cross-review vòng 4 — packet #318 `DOCTRINE-RANH-GIOI-REVIEWER`

verdict: changes_requested
reviewed_sha: 6d0a183e4af6422d85af1d6d3373fcbab2c7e83e
reviewed_tree: 5557a399cc959a8cbc10f666f120da83cd3f60e0
base_sha: c35ae1c0a1104dbd6e65a321cda3b9f9441a408b
provider: openai_codex
execution_surface: codex_service
transport: machine
executor: claude
independent_from_executor_session: true
review_axes: [spec, standards_security]

## Kết luận

Yêu cầu thay đổi. N1, N3–N7 đạt theo các phép đo dưới đây, nhưng N2 không đạt:
vùng áp dụng vẫn còn một nhãn rút gọn, một câu đếm số ví dụ đã sai, và ô pha B
không giữ được quan hệ một mệnh đề/điều kiện đo/một nhãn. Hiện vật probe đã có thật,
nhưng cách nó quy mọi `Exception` về `1` và cách doctrine đọc `git ls-remote rc=128`
không phân biệt được lỗi mạng với lỗi khác. Phép chạy trực tiếp trên execution surface
của reviewer cũng cho `1/1/128`, khác cột `0/0/0` Executor khai.

## ĐỐI CHIẾU HAI FINDING VÒNG 3

| finding vòng 3 | phán quyết vòng 4 | phép đo độc lập |
|---|---|---|
| `nam-hang-khong-tao-phan-hoach` [P1] | **VÁ HỜ** | `git diff --unified=0 88bd4f2fe6e02803a97f2da9df86c8b43d53076f..6d0a183e4af6422d85af1d6d3373fcbab2c7e83e -- docs/GOI_AGENT_DA_NEN.md` (`rc=0`) xác nhận đã tách hai hàng `--allowedTools`, thêm nhãn đầy đủ ở các dòng 644, 674–675, 686–687, 700–701. Nhưng `rg -n -i '^#### Trong sandbox codex thì khác hẳn — CƠ CHẾ ĐÃ XÁC MINH,' docs/GOI_AGENT_DA_NEN.md` vẫn bắt tiêu đề nhãn rút gọn tại `:648`. Câu `:603–604` còn khai “đúng một ví dụ”, trong khi chính phần sau có ít nhất ba control đổi hạng theo cấu hình: `--allowedTools` (`:636–637`), mạng (`:659–675`), hệ tệp (`:686–687`). Ô `:701` đặt `FS ngoài cây = … chiều MỞ ⇒ chỉ còn máy phát hiện`, khiến cùng mệnh đề/cell mang hai nhãn hoặc để chủ thể của `máy phát hiện` không được nêu. Ô dư được dùng thật tại `:636`, nhưng chưa cứu được phân hoạch toàn vùng. |
| `probe-mang-moi-khong-tai-lap-duoc` [P2] | **VÁ SINH LỖI MỚI** | Hiện vật `.claude/dev/probe_mang.py` có thật, compile được và chạy trực tiếp `rc=0`; thiếu-hiện-vật đã được vá. Tuy nhiên lần chạy trực tiếp hiện tại in `bind 1 / urllib 1 / ls-remote 128`, không phải `0/0/0`. Trên clone độc lập, mutant đổi `urllib` sang URL dữ liệu hợp lệ và `git ls-remote` sang tên repo-relative không tồn tại vẫn cho probe `rc=0`, `urllib 0`, `ls-remote 128`; lệnh git riêng trả `rc=128` với lỗi “does not appear to be a git repository”, hoàn toàn không phải lỗi mạng. Mutant URL không có scheme làm `urllib` ném `ValueError` (`rc=1` khi chạy riêng), nhưng `ma_thoat` vẫn in `urllib 1` và toàn probe vẫn `rc=0`. Hai lỗi mới được ghi thành findings P2 dưới đây. |

## BẢNG CHẤM N1–N7

| tiêu chí | kết quả | lệnh, mã thoát và bằng chứng dương |
|---|---|---|
| N1 | **ĐẠT** | `sed -n '623,629p' docs/GOI_AGENT_DA_NEN.md` (`rc=0`): câu đầu tại `:625–629` giới hạn rõ **vỏ phiên điều phối**, đối tượng là **quyền ghi vào kho**, và tách kết quả trong sandbox sang mục kế. |
| N2 | **KHÔNG ĐẠT** | `rg -n -i -e 'ranh giới' -e 'hàng rào' -e 'cưỡng chế' -e 'cơ chế đã xác minh' -e 'máy phát hiện' -e 'chưa xếp được' docs/GOI_AGENT_DA_NEN.md` (`rc=0`) phơi nhãn rút gọn `:648`, ba ví dụ trái câu “đúng một” tại `:603–604`, và ô hai nhãn/thiếu chủ thể tại `:701`. `doctrine-scan` vẫn `rc=0`, nên gate hình thức không phủ lỗi ngữ nghĩa này. |
| N3 | **ĐẠT** | `sed -n '696,716p' docs/GOI_AGENT_DA_NEN.md` (`rc=0`): bảng hai pha không dựa vào claim `--allowedTools` đang `CHƯA XẾP ĐƯỢC`; nó ghi mạng chỉ đóng ở cấu hình mặc định và đoạn `:703–716` nói rõ mặc định có thể bị lật bằng cờ. Lỗi phân hạng riêng của ô `:701` được chấm ở N2, không đổi kết luận N3. |
| N4 | **ĐẠT** | `sed -n '659,675p' docs/GOI_AGENT_DA_NEN.md` (`rc=0`): ngày `26-08-2026`, `codex-cli 0.149.1`, hai mode mặc định/`network_access=true`, probe và cột đối chứng nằm ngay cạnh bảng quan sát. Finding về tính phụ thuộc execution surface ở dưới là yêu cầu chặt hơn bộ ba tối thiểu này. |
| N5 | **ĐẠT** | Sáu lệnh `rg -n -F` (`rc=0`) tìm đúng: `bash /tmp/refscan.sh` tại `:553`; `stdout.log` không được git theo dõi tại `:570–572`; `tương quan có neo` tại `:574–577`; và ba hàng nguyên văn `78/5/10,8 M`, `85/10/12,8 M`, `45/1/3,7 M` tại `:566–568`. `git diff --unified=0 88bd4f2..6d0a183 -- docs/GOI_AGENT_DA_NEN.md` không có hunk nào đổi các dòng ấy. |
| N6 | **ĐẠT** | `git diff --name-only c35ae1c0a1104dbd6e65a321cda3b9f9441a408b..6d0a183e4af6422d85af1d6d3373fcbab2c7e83e` (`rc=0`) in đúng hai path: `.claude/dev/probe_mang.py` và `docs/GOI_AGENT_DA_NEN.md`. Tệp verdict này là sản phẩm reviewer untracked, không thuộc diff của reviewed SHA. |
| N7a | **ĐẠT** | `python3 .claude/dev/packet_loop.py doctrine-scan --root . --path docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `doctrine-scan: sạch — đã quét 8 tệp, 0 chỗ chép doctrine`. |
| N7b | **ĐẠT** | `git diff --numstat c35ae1c0a1104dbd6e65a321cda3b9f9441a408b -- docs/GOI_AGENT_DA_NEN.md` → `rc=0`, `198  0`, dưới trần thêm 200. Phép đo riêng cho probe là `30  0`, đúng trần riêng 30; không cộng hai ngân sách vì lease revision 3 được giao tường minh theo từng path. |

## Phép đo probe và phản chứng sẵn có

| phép đo | kết quả |
|---|---|
| `codex --version` | `rc=0`; `codex-cli 0.149.1` (kèm một warning PATH alias do filesystem chỉ đọc). |
| `python3 .claude/dev/probe_mang.py` | `rc=0`; `bind 1 / urllib 1 / ls-remote 128`. **Lệch** cột đối chứng `0/0/0` Executor khai. Điều kiện thực tế: Codex service hiện tại, workspace-write sandbox ngoài cùng, mạng đóng, 26-08-2026. |
| `codex sandbox -c sandbox_mode=workspace-write -- python3 .claude/dev/probe_mang.py` | `rc=101`; probe chưa chạy. Bubblewrap chết tại `/tmp/codex-bwrap-synthetic-mount-targets-0/lock`: filesystem chỉ đọc. |
| `codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -- python3 .claude/dev/probe_mang.py` | `rc=101`; cùng lỗi bubblewrap trước khi probe chạy. Không dùng kết quả này để bác hay xác nhận bảng. |
| `python3 .claude/dev/packet_loop_test.py` trên clone detached `/tmp/tra-luat-review4.2hObCD/cay` | `rc=0`; nền `257/257`, `66` đột biến đều giết ca đích, `78/78` lớp lách có đột biến, `TỔNG: ĐẠT`. Clone ở exact reviewed SHA/tree, `core.abbrev=7`; sau mutant đã khôi phục byte-exact và `git status --porcelain` rỗng. |
| Compile probe không ghi bytecode | `python3 -c "compile(open('.claude/dev/probe_mang.py', encoding='utf-8').read(), '.claude/dev/probe_mang.py', 'exec')"` → `rc=0`. |

## FINDINGS CÒN MỞ / MỚI

### `nam-hang-khong-tao-phan-hoach` [P1] — còn mở từ vòng 3

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:603`, `:636–648`, `:686–701`.
- **Vấn đề:** phân hoạch chưa đạt quy tắc “một mệnh đề kèm điều kiện đo, đúng một nhãn đầy đủ”. Tiêu đề `:648` vẫn dùng nhãn rút gọn; số lượng “đúng một ví dụ” đã sai; pha B `:701` không tách claim mở của FS khỏi control phát hiện.
- **Phép đo tái lập:** các lệnh `rg`/`nl` trong N2; `doctrine-scan rc=0` đồng thời chứng minh cổng hiện tại không bắt lớp lỗi này.
- **Gợi ý vá — ở đâu:** sửa riêng vùng từ vựng/bảng tại `:603–704`, vì đây là nơi định nghĩa và áp dụng phân hoạch; không vá bằng cách đổi nghĩa chung ở phần khác của tệp.
- **Gợi ý vá — thế nào:** bỏ hoặc đổi tiêu đề `:648` thành mô tả trung tính; tách từng hàng thành `control + cấu hình + quan sát + đúng một nhãn đầy đủ`; nêu riêng tên/điều kiện của `--require-clean`/snapshot khi gọi chúng là `máy phát hiện`; bỏ con số “đúng một” hoặc thay bằng số đo tự sinh sau khi đếm lại.
- **Ca test khóa:** mutant rút `— chiều ĐÓNG/MỞ`, mutant gộp hai cấu hình vào một hàng, và mutant gắn `máy phát hiện` vào chính claim FS mở đều phải làm phép audit đỏ. Nếu cần thêm gate tracked ngoài hai path của lease, phải revision write set thay vì lén sửa scanner.
- **Rủi ro bản vá có thể đẻ:** ép máy đếm nhãn theo chuỗi có thể xanh giả khi một nhãn đứng cạnh hai claim, hoặc đỏ oan ở đoạn lịch sử trích lời cũ; fixture phải phân biệt câu vận hành với câu thuật lại.

### `probe-nuot-loi-thanh-chan-mang` [P2] — mới

- **Tệp/dòng:** `.claude/dev/probe_mang.py:18–24`, `:27–30`; `docs/GOI_AGENT_DA_NEN.md:670–672`.
- **Vấn đề:** `ma_thoat` bắt `Exception` trần rồi định nghĩa mọi lỗi là “bị chặn”; hàng git chỉ giữ một số `128` và bỏ stderr. Vì vậy DNS, TLS, timeout, URL sai, repo không tồn tại, thiếu quyền hoặc lỗi chương trình có thể bị đọc thành “mạng đóng”. Đây là chỗ giấu lỗi, dù comment nói là có chủ ý.
- **Phép đo tái lập:** trên clone, mutant không gọi mạng dùng URL dữ liệu hợp lệ và repo-relative `khong-ton-tai`: probe `rc=0`, in `urllib 0 / ls-remote 128`; lệnh `git ls-remote khong-ton-tai` riêng `rc=128` với lỗi “does not appear to be a git repository”. Mutant `urllib` không có scheme ném `ValueError` (`rc=1` riêng) nhưng probe vẫn `rc=0`, in `urllib 1`.
- **Gợi ý vá — ở đâu:** sửa helper và ba phép đo ngay trong `probe_mang.py`; sửa bảng doctrine chỉ sau khi output mới đã được đo lại.
- **Gợi ý vá — thế nào:** xuất ít nhất ba trạng thái `lọt / bị chặn đúng cơ chế / lỗi-khác` kèm loại exception hoặc stderr/returncode thô. Chỉ phân loại “bị chặn” khi chữ ký lỗi phù hợp với cơ chế sandbox đã biết; trường hợp khác phải là `KHÔNG_ĐO_ĐƯỢC`, không phải `1`. Đóng socket/response rõ ràng. Nếu 30 dòng không đủ để làm trung thực, xin revision ngân sách thay vì nén mất bằng chứng.
- **Ca test khóa:** giữ hai mutant phi-mạng ở trên và thêm timeout; chúng phải ra `lỗi-khác`, còn cấu hình mạng mặc định đã đo phải ra `bị chặn`. Mỗi kênh phải bảo toàn raw evidence để reviewer phân biệt.
- **Rủi ro bản vá có thể đẻ:** khớp chuỗi stderr quá chặt sẽ phụ thuộc locale/phiên bản; ưu tiên exception type, structured errno và raw evidence, không chỉ câu chữ.

### `doi-chung-vo-phien-phu-thuoc-be-mat` [P2] — mới

- **Tệp/dòng:** `docs/GOI_AGENT_DA_NEN.md:654`, `:661–672`; `.claude/dev/probe_mang.py:4–14`.
- **Vấn đề:** cột `đối chứng: vỏ phiên` được in như một bộ số cố định, nhưng cùng probe/cùng `codex-cli 0.149.1` chạy trực tiếp trên Codex service này cho `1/1/128`, không phải `0/0/0`. “Vỏ phiên” chưa phải điều kiện đủ; execution surface và sandbox ngoài cùng quyết định kết quả.
- **Phép đo tái lập:** `codex --version; python3 .claude/dev/probe_mang.py` → `rc=0`, version `0.149.1`, ba số `1/1/128` ngày 26-08-2026. Đây là finding theo chỉ thị Packet khi số đo khác, nhưng không phải bằng chứng rằng phép đo cũ trên vỏ Claude bị bịa.
- **Gợi ý vá — ở đâu:** đổi tên/caption cột tại `:668–672` và phần hướng dẫn ba lượt trong docstring probe.
- **Gợi ý vá — thế nào:** ghi cột là quan sát trên surface cụ thể, ví dụ `Claude Code outer shell đã đo`, kèm `provider`, `execution_surface`, sandbox ngoài cùng và network policy; không dùng “ngoài codex” như một điều kiện phổ quát. Nếu muốn đối chứng đa nền, lưu từng hàng theo metadata thay vì ép một giá trị chung.
- **Ca test khóa:** chạy trực tiếp cùng probe trên ít nhất hai surface được hỗ trợ và assert rằng báo cáo luôn mang metadata; test không được đòi hai surface cho cùng số.
- **Rủi ro bản vá có thể đẻ:** đưa quá nhiều metadata động vào doctrine làm số nhanh trôi; chỉ giữ các chiều thực sự phân biệt kết quả và chuyển log chi tiết sang evidence theo exact run.

## CHỖ KHÔNG ĐO ĐƯỢC

1. **Hai cột sandbox lồng nhau:** `KHÔNG_ĐO_ĐƯỢC` vì cả hai lệnh chết `rc=101` trước khi probe chạy, tại khóa bubblewrap chỉ đọc. Không suy bảng đúng/sai từ lỗi này.
2. **Tính mới của remote head, Packet projection, lease generation/spec hash/review class và quyền bền cho vòng 4:** `KHÔNG_ĐO_ĐƯỢC` từ cây. Mạng/GitHub bị cấm, không `fetch`; kho cục bộ không có Packet/lease #318. Chỉ thị trực tiếp của người giữ cung cấp role, revision 3 của lease, base/head, write set và acceptance để thực hiện review nội dung.
3. **Ba `stdout.log` của các lượt cũ và các số 78/5/10,8 M · 85/10/12,8 M · 45/1/3,7 M:** `KHÔNG_ĐO_ĐƯỢC` đúng như doctrine tự khai, vì scratchpad không được git theo dõi. Lượt này chỉ xác minh chúng được giữ nguyên trong text.
4. **Cột `0/0/0` trên chính vỏ Claude Code của Executor:** `KHÔNG_ĐO_ĐƯỢC` trên execution surface Codex hiện tại. Phép trực tiếp ở đây đo một surface khác và được báo riêng thành finding, không giả làm phép tái hiện cùng điều kiện.
5. **GitHub CI/check và trạng thái PR:** `KHÔNG_ĐO_ĐƯỢC` vì lượt review bị cấm gọi GitHub. Không coi vắng evidence là pass.

## Đếm finding

- P1: **1**
- P2: **2**

Đường dẫn verdict: `ops/reviews/doctrine-ranh-gioi-reviewer-review-4-codex-verdict.md`
