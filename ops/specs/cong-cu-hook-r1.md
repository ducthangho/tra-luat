# CONG-CU-HOOK r1: hook phiên cài các công cụ còn thiếu theo bản kê, và ruff đúng bản ghim CI (đặc tả đóng băng)

- **Packet:** #1474. Revision 1, generation 1. Role `executor` (Claude), Review Class `sensitive`. Lý do `sensitive`: hook chạy ở
  MỌI phiên remote. Một lỗi ở đây có thể làm phiên khởi động chậm hoặc hỏng.
- **Căn cứ:** Issue #1474 (đo 21-11-2026). Chủ kho yêu cầu trong phiên dispatcher `session_015GtxrapMSm976JLC7Fp1HM`:
  *"Đồng ý, mở packet đó đi. Tìm nốt các công cụ khác như rg,..., nếu gặp vấn đề tương tự thì xử lý luôn"*.

## 1. Vấn đề
- Hook `.claude/hooks/session-start.sh` có bước cài riêng cho `rg` và `actionlint`. Mọi công cụ khác trong bản kê
  `ops/cong_cu.yaml` chỉ có mặt nếu ảnh container có sẵn:
  - `shellcheck`: `chuan_bi: true`; canary `actionlint_shellcheck` ở chế độ `blocking`. Vắng ở mọi phiên remote.
  - `jsonschema`: `bat_buoc: true`. Hiện có mặt chỉ nhờ ảnh container.
- `ruff`: `ci.yml` ghim `ruff==0.15.15`. Hook không cài ruff. Ảnh container có `ruff` 0.16.9 (uv tool) ở đầu PATH.
- Đã có sẵn công thức cài đúng cho mọi công cụ của bản kê: `ops/cai_cong_cu.sh <ten>`. Công thức này cài, ĐO LẠI, và đã có nhánh
  `apt-get update` rồi thử lại (wp1404). Đo 21-11-2026: chạy tay `bash ops/cai_cong_cu.sh shellcheck` ⇒ DAT 0.9.0.

## 2. Hành vi
### 2.1 Khối `cong-cu-ban-ke` trong hook
- Vị trí: nằm giữa hai dấu `# >>> cong-cu-ban-ke (wp1474)` và `# <<< cong-cu-ban-ke (wp1474)`. Đặt SAU khối `agent-creds` (tức sau
  bước pip của `requirements.txt`), TRƯỚC phần xác thực codex và TRƯỚC `launcher.py doctor`.
- Bước 1, đo: chạy `"$PY" "$GOC/ops/cong_cu.py" kiem-tra --json`. Đọc stdout dù mã thoát khác 0. Lệnh ấy trả mã khác 0 đúng khi có
  công cụ bắt buộc thiếu, mà đó chính là ca cần cài.
- Bước 2, chọn: tập cần cài là các công cụ trong `ops/cong_cu.yaml` có `bat_buoc: true` HOẶC `chuan_bi: true`, mà trạng thái trong
  kết quả đo khác `DAT`. Công cụ VẮNG MẶT trong kết quả đo cũng tính là chưa DAT (fail-close). Tên công cụ phải khớp
  `^[A-Za-z0-9_.-]+$`.
- Bước 1 hoặc bước 2 không đọc được (JSON hỏng, YAML hỏng, tên lạ) ⇒ in `cong-cu-ban-ke: KHONG DO DUOC …`, KHÔNG cài gì, khối trả
  mã khác 0.
- Bước 3, cài: với mỗi công cụ cần cài, gọi `bash "$GOC/ops/cai_cong_cu.sh" <ten>`, mỗi công cụ có trần 180 giây (dùng `timeout`
  nếu có lệnh ấy). Đầu ra của trình cài không in ra; in một dòng gồm tên công cụ và mã thoát.
- Bước 4, đo lại: chạy lại bước 1–2. In `cong-cu-ban-ke: DAT (n cong cu)` khi không còn công cụ nào thiếu. Còn thiếu thì in
  `cong-cu-ban-ke: CHUA DAT <tên…>` và khối trả mã khác 0. Kết luận chỉ dựa vào lần đo lại, KHÔNG dựa vào mã thoát của trình cài.
### 2.2 Ruff đúng bản ghim CI (cùng khối)
- Bản ghim: mọi chuỗi `ruff==X.Y.Z` trong `"$GOC/.github/workflows/ci.yml"`. Phải ra ĐÚNG MỘT giá trị khác nhau. Không có, hoặc có
  từ hai giá trị trở lên ⇒ in `ruff: KHONG DO DUOC ban ghim …`, không cài, khối trả mã khác 0.
- Đo `"$PY" -m ruff --version`. Bằng `ruff X.Y.Z` ⇒ in `ruff: DAT X.Y.Z`. Khác hoặc lỗi ⇒ chạy
  `"$PY" -m pip install --quiet "ruff==X.Y.Z"` (trần 180 giây), rồi đo lại. Đo lại vẫn lệch ⇒ in `ruff: CHUA DAT …`, khối trả mã
  khác 0.
- `ruff` trần trên PATH (nếu có) cho phiên bản khác bản ghim ⇒ in cảnh báo: dùng `"$PY" -m ruff`, kèm hai số phiên bản. Cảnh báo
  này KHÔNG đổi mã thoát của khối, vì `ruff` trần thuộc ảnh container, không thuộc kho.
### 2.3 Gọi khối
- Hook gọi khối theo dạng `MA_CC=0; <hàm> || MA_CC=$?` rồi in `cong-cu-ban-ke: rc=$MA_CC`. Khối KHÔNG BAO GIỜ làm hook dừng: hook vẫn
  chạy tiếp tới `doctor`, và `doctor` vẫn là cổng duy nhất quyết định thoát 12.
- Thêm hai tên vào dòng `hook-nang-luc`: `cong-cu-ban-ke` và `ruff-ban-ghim-ci`.
### 2.4 Skill
`.claude/skills/work-packet/SKILL.md` (đoạn probe dependency, quanh dòng 130): thêm `shellcheck --version` và `"$PY" -m ruff --version`
vào danh sách probe. Kèm một câu: thiếu `shellcheck` thì `actionlint` bỏ âm thầm luật SC*. Chỉ sửa cú pháp và công cụ, không chép
doctrine. `doctrine-scan` phải còn xanh.

## 3. Ngoài phạm vi
- Không sửa `ops/cong_cu.yaml`, `ops/cai_cong_cu.sh`, `ops/cong_cu.py`, `.claude/dev/launcher.py`, `ci.yml`.
- Không thêm tệp `*_test.py` mới: `.claude/dev/ci_dang_ky_test.py` đang bị lease `wp1236-a-r10-g1-claude-20261121` giữ tới
  2026-11-23T00:15Z, nên không đăng ký được tệp mới. Ca test đặt trong `.claude/dev/launcher_test.py`, tệp đã đăng ký và đã test hook.
- Không cài `jq`, `gh`, `pwsh`, `llm`: CI không dùng chúng làm cổng, hoặc CLAUDE.md đã ghi là không cần.
- `ruff` trần của ảnh container: chỉ cảnh báo, không gỡ.

## 4. Test (`.claude/dev/launcher_test.py`, ca `r1474_*`, theo khuôn `_wp802_chay_khoi_rg_hook`)
Trích riêng khối giữa hai dấu rồi chạy trên cây tạm có đồ giả GIỮ TRẠNG THÁI: `ops/cong_cu.py` giả đọc trạng thái từ một tệp;
`ops/cai_cong_cu.sh` giả ghi nhật ký và đổi trạng thái; `PY` giả bắt `-m ruff` và `-m pip` (ghi nhật ký), còn lại chuyển cho Python
thật. Bỏ qua trên Windows (shell POSIX). Ít nhất các ca:
1. Thiếu `shellcheck` (`chuan_bi`) ⇒ đúng 1 lần cài `shellcheck`, 0 lần cài công cụ khác, dòng `DAT`, rc 0.
2. Đủ hết, ruff đúng bản ⇒ 0 lần cài, 0 lần pip, rc 0.
3. Trình cài "thành công" mà đo lại vẫn thiếu ⇒ `CHUA DAT shellcheck`, rc khác 0.
4. Công cụ không `bat_buoc` cũng không `chuan_bi` mà thiếu ⇒ không cài.
5. Công cụ vắng khỏi kết quả đo ⇒ coi là thiếu, cài.
6. Kết quả đo hỏng ⇒ `KHONG DO DUOC`, 0 lần cài, rc khác 0.
7. `-m ruff` lệch bản ghim ⇒ đúng 1 lần `pip install ruff==<ghim>`, đo lại ⇒ `ruff: DAT`.
8. `ci.yml` có hai bản ghim ruff khác nhau ⇒ `KHONG DO DUOC`, 0 lần pip, rc khác 0.
9. `ruff` trần lệch ⇒ có dòng cảnh báo, rc không đổi.
10. Cấu trúc trên hook THẬT: đúng một cặp dấu khối; khối nằm sau `<<< agent-creds` và trước dòng gọi `launcher.py doctor`; có dòng gọi
    `|| MA_CC=$?`; dòng `hook-nang-luc` có hai tên mới. Trên `ops/cong_cu.yaml` THẬT: `shellcheck` thuộc tập cần cài. Trên `ci.yml`
    THẬT: đúng một bản ghim ruff.
11. Skill `work-packet` có `shellcheck --version` và `-m ruff --version`.

Đột biến (đích `hook`, bảng `DOT_BIEN` của `launcher_test.py`). Mỗi đột biến phải làm ĐỎ đúng ca đích:
bỏ vế `chuan_bi` (ca 1); coi công cụ vắng mặt là DAT (ca 5); kết luận theo mã thoát trình cài thay vì đo lại (ca 3); kết quả đo hỏng
vẫn đi tiếp (ca 6); bỏ chốt bản ghim duy nhất (ca 8); bỏ so phiên bản ruff (ca 7).

Chạy tại chỗ trước khi push: các ca `r1474_*` và `r802_*` bằng `--lap-ca`, rồi cả bộ `launcher_test.py`. Thêm
`ops/cloud_agent_creds_test.py` (bộ này đọc hook), `packet_loop.py doctrine-scan --root .`, `bash -n` trên hook, và chạy thật khối mới
trong container (so trước/sau).

## 5. Review và CI
- Codex offline qua `launcher.py run`, **tối đa 2 lời gọi**. P0–P2 chặn merge. Thêm connector Codex trên PR.
- CI của PR: mọi check bắt buộc của ruleset. Không gọi Windows CI.
- Không có dòng hiệu lực ADR-0060 ⇒ luật cũ: không bắt buộc `full_mutant_audit`. Đột biến ở §4 là bắt buộc.

## 6. Write set (không glob)
- `.claude/hooks/session-start.sh`
- `.claude/skills/work-packet/SKILL.md`
- `.claude/dev/launcher_test.py`
- `ops/specs/cong-cu-hook-r1.md`
- `ops/leases/cong-cu-hook-r1-g1-claude.yaml`
- `ops/acceptance/cong-cu-hook/r1/VERDICT.md`
