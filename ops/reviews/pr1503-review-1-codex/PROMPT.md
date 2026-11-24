# Cross-review PR #1503 (ducthangho/tra-luat) — lượt 1, reviewer Codex

Bạn là reviewer độc lập. Thư mục làm việc hiện tại là một bản sao RỜI của kho, đã checkout
detached đúng commit cần review. Thứ định danh lượt review là BĂM, không phải tên nhánh:

- reviewed_sha: `257beee354cf4861c2d2978d195dfebaf81904d0`
- base_sha (merge-base với master): `a99a74f75867172fe62f984d7528f5d5bd73dacb`
- Diff cần review: `git diff a99a74f75867172fe62f984d7528f5d5bd73dacb 257beee354cf4861c2d2978d195dfebaf81904d0`
  (21 tệp; commit trên nhánh: `git log --oneline a99a74f7..HEAD`)

Đọc `CLAUDE.md` ở gốc kho trước (quy tắc của kho, nhất là mục "Bài học đắt giá" và
"Quy trình sửa code"). Từ vựng ở `CONTEXT.md`.

## PR này làm gì

Cho script trong skill gọi Claude theo hai đường, tự chuyển khi một đường hỏng:
- `sub`: `claude -p` (Claude Code không tương tác) — tính vào SUBSCRIPTION;
- `api`: SDK `anthropic` + `TL_ANTHROPIC_API_KEY` (rồi `ANTHROPIC_API_KEY`) — tính vào credit API.

Thành phần:
1. `scripts/tl_core/llm_route.py` (lõi thuần, vào gói phát hành) + `scripts/tl_core/llm_route_test.py`
   (dev-side, loại khỏi gói).
2. Lệnh `tl llm-order [THU_TU] [--reset]` (thứ tự hiệu lực: cờ `--thu-tu` > tệp `~/.tra_luat_llm.json`
   / `TL_LLM_ORDER_FILE` > biến `TL_LLM_ORDER` > mặc định `sub,api`) và
   `tl llm-khai-niem <số hiệu> --dieu N | --tep <tệp>` — handler ở `scripts/tl_core/ops_misc.py`,
   spec/meta ở `scripts/tl_core/command_registry.py`, tên khai trong `_STUB_MAP` và
   `_CREDS_LAZY_CMDS` của `scripts/tl.py`.
3. `.claude/dev/launcher.py`: mục `anthropic-api` trong `KHA_NANG` (`_do_anthropic_api`), ca `t162`
   và 4 đột biến trong `.claude/dev/launcher_test.py`.
4. Kèm theo: VERSION 1.36.71 (3 chỗ), CHANGELOG, RELEASE_MANIFEST, golden, ratchet gói 186→187 trong
   `scripts/tl_selftest.py`, `ops/cong_cu.yaml`, `docs/GOI_AGENT_DA_NEN.md`, `references/*.md`.

## Việc của bạn

Tìm lỗi THẬT, xếp hạng P0 (chặn) · P1 (phải sửa trước merge) · P2 (nên sửa) · P3 (góp ý nhỏ).
Mỗi finding phải có: tệp:dòng, kịch bản hỏng cụ thể (đầu vào → kết quả sai), và BẰNG CHỨNG CHẠY
ĐƯỢC (lệnh + output) khi đo được. Lời khai không đo được thì ghi rõ "KHÔNG ĐO ĐƯỢC" kèm lý do.

Những hướng đáng soi (không phải danh sách đóng — tìm cả ngoài nó):
- Phân loại lỗi đường `api` (`phan_loai_loi_api`): có lỗi phía yêu cầu nào bị chuyển đường (tiêu
  tiền hai lần), hay lỗi phía đường nào bị dừng oan? Đối chiếu với SDK `anthropic` đang cài nếu có.
- Đường `sub`: có cách nào để nó lặng lẽ tính tiền vào API key thay vì subscription không? Cờ
  `claude -p` có đúng với CLI đang cài (`claude --help`) không? Đọc kết quả JSON có chỗ nào tin
  một tín hiệu yếu (rc, khoá vắng, model phụ) không?
- Thứ tự đường và tệp lưu: thứ tự ưu tiên, fail-closed khi tệp hỏng, ghi nguyên tử, ca biên.
- Kiểm nguyên văn (`chuan_hoa_khai_niem`, `lech_nguyen_van`): có kết quả sai nào vẫn lọt? có kết quả
  đúng nào bị chặn oan?
- Tích hợp `tl`: bẫy I11 (hàm re-home `__globals__` về `tl.py`), `_CREDS_LAZY_CMDS`, `--profile`,
  `lay_dieu_qua_extract` (cắt đầu ra `tl extract`), mã thoát.
- `_do_anthropic_api` trong launcher: nhãn trạng thái, mặc định không gọi mạng, không lộ key.
- Phát hành: ratchet số tệp gói, `_RELEASE_EXCLUDE_NAMES_ANYWHERE`, golden, parser_surface.
- Test có RĂNG không: đột biến bản vá (trên BẢN SAO TẠM, không sửa tệp trong cây) và xem ca đích
  có đỏ đúng lý do không; tìm chốt nào chưa có ca/đột biến canh.

## Cách đo (chạy được, không cần mạng)

```
python scripts/tl_core/llm_route_test.py
python .claude/dev/launcher_test.py --lap-ca t162 --lan 1
python scripts/tl.py --deterministic workflow-audit --strict --json
python scripts/tl.py --deterministic golden-test --json
python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
TL_LLM_ORDER_FILE=$(mktemp -d)/o.json python scripts/tl.py llm-order --json
python scripts/tl.py --selftest        # ~6 phút, tuỳ chọn
```

## Ràng buộc

- KHÔNG gọi Claude/Anthropic API thật, KHÔNG chạy `claude -p` thật, KHÔNG chạy `tl llm-khai-niem`
  mà không có đồ giả — mọi lời gọi đó tốn tiền thật của chủ kho. Không đọc/in giá trị biến bí mật.
- KHÔNG push, KHÔNG gọi GitHub, KHÔNG sửa tệp đã theo dõi trong cây (đột biến làm trên bản sao tạm).
- Hướng thử nào cần tự soạn nội dung tấn công (ví dụ dựng đường dẫn thoát khỏi cây thư mục) thì
  MÔ TẢ BẰNG LỜI trong verdict, đừng tự soạn — phiên điều phối sẽ dựng phản chứng.

## Đầu ra

Ghi `VERDICT.md` vào thư mục `.review/` dưới thư mục làm việc (tạo nếu chưa có), ghi TĂNG DẦN sau
mỗi finding để lượt bị ngắt vẫn còn phần đã ghi. Cấu trúc:

```
# Verdict PR #1503 lượt 1 — Codex
reviewed_sha: 257beee354cf4861c2d2978d195dfebaf81904d0
## Findings
### F1 [P?] <tiêu đề ngắn> — <tệp:dòng>
Kịch bản: ...
Bằng chứng: <lệnh> → <output rút gọn>
Đề xuất sửa: ...
## Đã kiểm mà không thấy lỗi
- ...
## Không đo được
- ...
VERDICT: APPROVE | REQUEST_CHANGES
```

Dòng `VERDICT:` cuối cùng là bắt buộc. REQUEST_CHANGES nếu có bất kỳ P0/P1 nào.
