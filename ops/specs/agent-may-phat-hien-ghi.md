# ĐẶC TẢ PHA 2 — `AGENT-MAY-PHAT-HIEN-GHI`

```yaml
packet_id: AGENT-MAY-PHAT-HIEN-GHI
packet_issue: 329
phase: 1
artifact: phase_2_specification
base_sha: 6cc64d399f6477c8ba256e761bde0e9c5187b180
executor: codex
reviewer: claude
write_set:
  - ops/specs/agent-may-phat-hien-ghi.md
```

## 1. Phạm vi và kết luận được phép

Pha 2 phải phát hiện thay đổi mà một lượt subagent có thể đã gây ra trong cây Git bằng cách
so hai ảnh chụp trạng thái. Đây là **máy phát hiện sau khi ghi**, không phải ranh giới ngăn ghi:
khi hook `SubagentStop` chạy thì tác dụng phụ đã có thể xảy ra.

Phạm vi đầu tiên là hai agent tự khai read-only: `tl-auditor` và `tl-rasoat`. Không suy rộng
sang agent khác nếu chưa có quyết định và ca đo tương ứng. Không gọi LIVE, không ghi Drive,
NLM hoặc registry corpus.

Mã hiện trạng cần được đo trước khi triển khai:

```sh
python .claude/hooks/pretooluse_guard_test.py
rg -n '_AGENT_CHI_DOC|_CHUONG_TRINH_CHO_PHEP|_KIEM_RIENG' \
  .claude/hooks/pretooluse_guard.py
```

Lệnh thứ hai cho thấy allowlist có 36 chương trình nhưng `_KIEM_RIENG` chỉ có 9:
`git`, `python`, `python3`, `py`, `find`, `sort`, `uniq`, `diff`, `ruff`. Với D2, điều này
có nghĩa 27 chương trình còn lại chỉ được lọc ở tầng tên chương trình cộng các chốt chung
(chuyển hướng, thay thế lệnh, tách dòng), **không** có bộ phân loại cờ/chế độ riêng nào.
Nó không chứng minh tập cơ chế ghi đã kín.

## 2. Payload đã đo và hệ quả thiết kế

Phép đo do phiên điều phối thực hiện ngày 2026-08-26 trên subagent thật cho kết quả dương:

| sự kiện | khóa payload đã quan sát |
|---|---|
| `SubagentStart` | `agent_id` · `agent_type` · `cwd` · `hook_event_name` · `prompt_id` · `session_id` · `transcript_path` |
| `SubagentStop` | các khóa trên + `agent_transcript_path` · `background_tasks` · `effort` · `last_assistant_message` · `permission_mode` · `session_crons` · `stop_hook_active` |

Cả hai payload mang `agent_type = "tl-auditor"`. Không sự kiện nào mang ảnh chụp hệ tệp.
Do đó hook phải tự chụp tại `SubagentStart`, lưu trạng thái qua ranh giới hai lần gọi, rồi tự
chụp và so tại `SubagentStop`. `agent_id`, có ở cả hai đầu, là khóa nối bắt buộc; không nối
bằng `session_id`, thời gian, `cwd` hoặc thứ tự sự kiện.

Ảnh chụp tối thiểu dùng chính `cwd` đã kiểm tra là worktree Git rồi chạy:

```sh
git -C <cwd> status --porcelain=v1 -uall
```

Phải giữ nguyên từng bản ghi của đầu ra (sau chuẩn hóa thứ tự nếu phép đo chứng minh cần),
không chỉ giữ số dòng. Snapshot phải gắn ít nhất `agent_id`, `agent_type`, `cwd` đã chuẩn hóa,
Git top-level, HEAD OID, kết quả lệnh và trạng thái thành công/thất bại. Dữ liệu lưu giữa hai
hook không được nằm trong worktree đang đo, nếu không máy tự tạo đúng thay đổi mà nó tố cáo.

Thiếu snapshot, trùng khóa, sai `agent_id`, lệch `cwd`/Git top-level, HEAD đổi, snapshot hỏng,
hoặc một lần `git status` lỗi đều là trạng thái **không xác định**, không được báo “không ghi”.
Cách xử lý trạng thái không xác định phụ thuộc quyết định D1 bên dưới.

## 3. Ba quyết định trình người giữ kho

Đặc tả này **không chọn** phương án nào. Pha 2 chỉ được bắt đầu sau khi người giữ kho ghi ba
quyết định bền và Packet revision mới phản ánh chúng.

### D1 — Sau khi phát hiện: chặn, hoàn tác hay chỉ tố cáo?

| phương án | điều đo được hoặc suy trực tiếp từ cơ chế |
|---|---|
| **CHẶN**: `SubagentStop` thoát `2` | Có thể cho phản hồi ở cuối lượt mà không tạo thêm đường ghi; nhưng hiệu lực exit `2` mới chỉ có trong tài liệu, **chưa đo được** trên Claude Code thật, và thay đổi đã xảy ra trước hook. |
| **HOÀN TÁC**: ví dụ `git checkout --` | Có thể đưa một phần tracked worktree về nội dung đã biết, nhưng chính chốt trở thành một đường ghi mới; có thể phá thay đổi có trước/chạy chồng, không bao phủ an toàn mọi untracked/index/rename, và cần thẩm quyền ghi rộng hơn detector. |
| **CHỈ TỐ CÁO** | Không tạo đường ghi phục hồi và giữ hiện vật để điều tra; nhưng cây vẫn bẩn và lượt điều phối kế tiếp phải có cổng dừng riêng nếu không muốn tiếp tục trên nền đã đổi. |

Người giữ kho phải chốt riêng hành vi cho “có delta” và “không xác định”; không được ngầm coi
hai trạng thái là một.

### D2 — Giữ hay bỏ bộ phân tích chuỗi lệnh của packet #324?

| phương án | điều đo được hoặc suy trực tiếp từ mã |
|---|---|
| **GIỮ** | Có phản hồi tức thì ở `PreToolUse` và tạo hai lớp phát hiện; suite hiện hành đo các ca đã biết. Đổi lại, `_CHUONG_TRINH_CHO_PHEP`, `_KIEM_RIENG` và các cờ/chế độ riêng vẫn là tập liệt kê phải bảo trì, còn detector hậu quả không làm tập ấy tự kín. |
| **BỎ** | Giảm một bộ phân tích shell và nợ liệt kê; đổi lại mất phản hồi trước lệnh cho agent, và mọi phát hiện chỉ đến ở `SubagentStop`, sau tác dụng phụ. |

Lệnh neo quy mô/hình dạng hiện trạng là hai lệnh ở §1; không dùng việc suite xanh để tuyên bố
allowlist đầy đủ.

### D3 — Chấp nhận mù hay mở rộng phép đo ngoài `git status`?

| phương án | điều đo được hoặc suy trực tiếp từ phép đo |
|---|---|
| **CHẤP NHẬN MÙ** | Giữ detector nhỏ và cục bộ, nhưng chấp nhận mù cả đường ghi thật sau: (1) `.gitignore:22 -> .tl_state/` — BỊ IGNORE; (2) `git status --porcelain=v1 -uall -> 0 dòng (tệp bị ignore)`, còn cùng lệnh + `--ignored -> 1 dòng` (đối chứng dương: cùng một lệnh, chỉ khác một cờ); (3) cổng #324, `agent_type=tl-auditor`: `python scripts/tl.py nlm-reconcile x --json -> ALLOW`, `install -m 644 /tmp/a /tmp/b -> deny`; (4) `scripts/tl_core/nlm_admin_ops.py`, nhánh `if not getattr(a, "apply", False)`: `_pa, _pae = _reconcile_write_artifact(_plan_out, _artd)`, chú thích ngay trên: “TRƯỚC ĐÂY chỉ ghi khi có --plan-out ... nay LUÔN ghi”. Ghép lại, `tl nlm-reconcile SO --json` không `--apply` vẫn tạo `.tl_state/reconcile_plan_SO.json`: lớp 1 cho qua vì `python` thuộc allowlist, lớp 2 báo `clean` vì `.tl_state/` bị ignore; hai lớp trùng vùng mù. `A3` dùng `install`, là cơ chế lớp 1 chặn nên không đo đường có thể xảy ra từ subagent thật. Khuyết tật gốc thuộc master và có từ trước; PR #330 đã gỡ lệnh ấy khỏi vốn từ tại `6af77a2`, nhưng việc gỡ khỏi vốn từ không làm mất đường ghi hay vùng mù. Ghi ngoài Git top-level và tác dụng phụ mạng cũng không quan sát được; báo cáo phải gọi đúng các giới hạn này. |
| **MỞ RỘNG** | Có thể tăng vùng quan sát, nhưng phải chỉ rõ từng nguồn sự thật, baseline, chi phí và quyền truy cập; đo toàn filesystem hoặc mạng không thể được suy ra chỉ từ payload hook hiện có. Mỗi cảm biến mới cần ca dương, ca đối chứng và trạng thái lỗi fail-closed riêng. |

Không được viết “phát hiện mọi ghi” ở cả hai phương án.

## 4. Hành vi pha 2 sau khi có quyết định

1. `SubagentStart` chỉ xử lý đúng tập `agent_type` đã chốt; xác thực `agent_id`, `cwd`, Git
   top-level và chụp baseline. Ghi snapshot theo cách nguyên tử ở nơi D3 cho phép.
2. `SubagentStop` tra đúng một snapshot bằng `agent_id`, xác thực lại metadata, chụp trạng thái
   sau, rồi so nội dung. Không được xóa bằng chứng trước khi kết quả/báo lỗi đã được tạo chắc chắn.
3. Kết quả có đúng ba lớp: `clean`, `changed`, `unknown`. `changed` phải in delta đủ để người
   điều phối nhận ra các path quan sát được; `unknown` phải in nguyên nhân có cấu trúc.
4. Hành động sau kết quả tuân đúng D1. Nếu D1 chọn hoàn tác, đường hoàn tác là một thành phần
   ghi riêng, có write set, phép đo và review riêng; không giấu nó trong detector.
5. Snapshot cũ phải có quy tắc dọn hữu hạn và chống dùng lại, nhưng tuổi thọ cụ thể chỉ được
   chốt sau phép đo lượt chạy dài/chạy chồng.

## 5. Tiêu chí nghiệm thu pha 2

Mọi test dùng repository tạm, không sửa cây thật. Mỗi ca phải kiểm cả mã thoát, kết quả có cấu
trúc và trạng thái Git cuối theo D1; “hook đã chạy” không thay cho bằng chứng dương.

- **A1 — nối hai đầu:** hai payload cùng `agent_id` tạo một cặp; payload khác ID không được
  lấy snapshot của nhau. Thiếu/nhân đôi snapshot cho ra `unknown`, không phải `clean`.
- **A2 — đối chứng sạch:** không đổi gì giữa Start/Stop cho `clean` và không tố path.
- **A3 — cơ chế không nằm trong danh sách:** sau Start, chạy thật trong repo tạm:

  ```sh
  install -m 644 <source> <repo-tam>/tep-moi.txt
  ```

  Stop phải trả `changed` và nêu `tep-moi.txt`. Ca này không được thêm `install` vào danh
  sách cơ chế ghi của detector; bỏ phép so snapshot phải làm ca đỏ. Đây là tiêu chí bắt buộc,
  không được thay bằng một lệnh đã có trong bảng test của packet #324.
- **A4 — các dạng Git quan sát được:** mỗi loại tracked sửa/xóa, untracked mới, rename và
  staged change có ít nhất một ca dương; delta không được rút còn một số đếm.
- **A5 — nền đã bẩn:** tạo thay đổi trước Start rồi giữ nguyên đến Stop không được gán cho
  lượt agent; tạo thêm một thay đổi sau Start chỉ tố delta mới. Nếu thiết kế không thể phân
  biệt path đổi tiếp trên nền đã bẩn, phải trả `unknown` cho path ấy thay vì khẳng định sạch.
- **A6 — lỗi phép đo:** không phải repo, `git status` lỗi, snapshot hỏng, HEAD/cwd/top-level
  lệch đều cho `unknown` và hành động đúng quyết định D1.
- **A7 — chạy chồng:** hai `agent_id` có snapshot riêng, không ghi đè/tái sử dụng lẫn nhau.
  Fixture phải bao gồm thứ tự Start(A), Start(B), Stop(B), Stop(A) và chiều Stop ngược lại.
- **A8 — vùng mù D3:** giữa Start/Stop, chạy `tl nlm-reconcile SO --json` không `--apply`
  để tạo `.tl_state/reconcile_plan_SO.json`. Nếu chấp nhận mù, kết quả phải là `unknown` hoặc
  báo rõ giới hạn; **cấm** `clean`. Ca ghi ngoài repo và mô phỏng tác dụng phụ mạng cũng phải
  chứng minh kết quả không quan sát được và báo giới hạn đúng; nếu mở rộng, mỗi vùng được chọn
  phải có ca dương và ca cảm biến lỗi.
- **A9 — tương thích D2:** nếu giữ guard #324, toàn bộ suite hiện hành vẫn xanh cùng suite
  detector; nếu bỏ, Packet phải chỉ rõ và đo việc gỡ hook/test thay vì để mã chết.
- **A10 — hiệu lực D1:** đo trên subagent Claude Code thật, không chỉ gọi script hook trực
  tiếp. Riêng phương án CHẶN phải chứng minh `SubagentStop` exit `2` thực sự ngăn bước tiếp
  theo nào và không được mô tả nó như hoàn tác thay đổi đã có.
- **A11 — tác dụng phụ của lệnh được cổng cho phép:** tách khỏi A3, chạy một lệnh nằm trong
  allowlist của cổng #324 nhưng vẫn ghi tệp — ca cụ thể là `tl nlm-reconcile SO --json` không
  `--apply` tạo `.tl_state/reconcile_plan_SO.json`. Ca đỏ nếu detector báo `clean`; tiêu chí
  này không được thay bằng cơ chế ngoài allowlist như `install`.

Lệnh kiểm tối thiểu của pha 2 phải được Packet revision ghi chính xác sau khi biết tên tệp
triển khai/test. Không bịa trước một CLI chưa tồn tại. Handoff phải ghi command, mã thoát thật,
bằng chứng dương, `passed`/`failed`/`skipped`/`not_run`, exact HEAD và tree hash.

## 6. Chưa đo được

- Chi phí thời gian/I/O của hai lần `git status --porcelain=v1 -uall` cho mỗi lượt trên cây
  thật; chưa có phân bố kích thước worktree hay thời gian chạy để đặt ngân sách.
- `SubagentStop` exit `2` có thực sự chặn được trên execution surface đang dùng hay chỉ báo lỗi;
  tài liệu không thay phép đo subagent thật.
- Hành vi và quy trách nhiệm khi nhiều subagent chạy chồng: một thay đổi ngoại sinh giữa hai
  snapshot có thể xuất hiện trong delta của nhiều agent.
- Nơi lưu snapshot, atomicity/locking, quyền tệp, cleanup sau crash và giới hạn tuổi thọ phù hợp;
  các điểm này phụ thuộc D3 và phép đo concurrency.
- Khả năng phân biệt agent gây thay đổi với phiên chính, hook khác hoặc process nền: phép so
  trước/sau chỉ chứng minh tương quan thời gian, không chứng minh tác giả.
- Mức bao phủ tệp ignored, ngoài repo và mạng cho tới khi D3 được quyết định và cảm biến tương
  ứng được đo.
- Hành vi khi worktree/HEAD đổi hợp lệ bởi điều phối trong lúc subagent chạy; hiện chỉ có thể
  phân loại là `unknown`, chưa có phép đo để nới.

## 7. Điều kiện dừng pha 2

Dừng và xin revision nếu thiếu bất kỳ quyết định D1–D3, cần ghi ngoài effective write set,
không tạo được ca A3 bằng cơ chế không liệt kê, hoặc test subagent thật không sinh đủ hai sự
kiện. Required check bị bỏ qua, không chạy, chạy trên SHA khác hoặc thiếu bằng chứng dương
không được tính là đạt.
