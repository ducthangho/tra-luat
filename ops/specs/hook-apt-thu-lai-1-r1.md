# HOOK-APT-THU-LAI-1 r1: hook phiên gọi `cai_cong_cu.sh` với 1 lần thử lại apt (đặc tả đóng băng)

- **Packet:** #1523. Revision 1, generation 1. Role `executor` (Claude), Review Class `sensitive`. Lý do `sensitive`: hook chạy ở mọi
  phiên remote.
- **Căn cứ:** Issue #1523. Chủ kho chọn việc này ngày 25-11-2026. Đề xuất gốc: `ops/handoff/phien-dieu-phoi-20261122-handoff.md` §3.2.

## 1. Hành vi
1. Trong khối `cong-cu-ban-ke` của `.claude/hooks/session-start.sh`, lời gọi `bash "$GOC/ops/cai_cong_cu.sh" "$t"` chạy dưới
   `env CAI_CONG_CU_THU_LAI="${CAI_CONG_CU_THU_LAI:-1}"`:
   - mặc định là **1** lần thử lại (chờ 15 s theo `cai_cong_cu.sh`);
   - biến đã được đặt sẵn (kể cả `0`) thì giữ nguyên giá trị ấy và chuyển xuống đúng như vậy;
   - việc kiểm hợp lệ để `cai_cong_cu.sh` lo, như #1479 đã làm.
2. Biến chỉ áp cho lời gọi ấy, không `export` ra phần còn lại của hook.
3. Trần 180 s cho mỗi lần cài, ngân sách khối 300 s, và mọi hành vi khác của khối giữ nguyên.
4. Thêm tên năng lực `cong-cu-apt-thu-lai-1` vào dòng `hook-nang-luc`.

## 2. Ngoài phạm vi
- CI và `ops/cai_cong_cu.sh`: không đổi. CI vẫn 3 lần thử lại.
- Khối cài `rg` riêng của hook (apt rồi cargo): không đổi.
- `.claude/dev/launcher_test.py` (lease `wp1511-r2-g2-claude` giữ tới 2026-11-26T16:30Z): không sửa. Các ca `r1474_*` của nó phải
  vẫn đạt, và mọi neo đột biến `wp1474_*` phải vẫn khớp đúng một chỗ; tự kiểm tại chỗ.

## 3. Test (`ops/cloud_agent_creds_test.py`, cạnh các ca `h1`–`h3`)
Ca mới tên `h4_*` trích riêng khối `cong-cu-ban-ke` và chạy trên cây tạm:
- `ops/cong_cu.py` giả: lần đo đầu báo một công cụ `chuan_bi` thiếu, sau khi cài thì DAT;
- `ops/cai_cong_cu.sh` giả: ghi giá trị `${CAI_CONG_CU_THU_LAI-VANG}` nó nhận được;
- `PY` giả: bắt `-m ruff` / `-m pip`, để không cài gì thật.
Hai vế:
- biến chưa đặt ⇒ trình cài nhận `1`;
- `CAI_CONG_CU_THU_LAI=3` ⇒ trình cài nhận `3`.
Kèm: phần còn lại của khối không thấy biến bị đổi; dòng `hook-nang-luc` có tên mới. Bỏ qua trên Windows (`_posix()`).

Đột biến (đích `hook` trong `DOT_BIEN`), mỗi cái làm đỏ đúng ca đích:
- bỏ `env CAI_CONG_CU_THU_LAI=…`;
- ép cứng `1` (không tôn trọng giá trị đã đặt);
- xoá tên năng lực mới.

Chạy tại chỗ: cả `ops/cloud_agent_creds_test.py` (đòi `TONG: DAT`); các ca `r1474_*` của `launcher_test.py` cùng kiểm neo `wp1474_*`;
`bash -n`; `shellcheck` delta; `doctrine-scan`.

## 4. Review và CI
- Codex offline qua `launcher.py run`, tối đa 2 lời gọi. P0–P2 chặn merge. Thêm connector Codex trên PR.
- CI của PR. Không gọi Windows CI.

## 5. Write set (không glob)
- `.claude/hooks/session-start.sh`
- `ops/cloud_agent_creds_test.py`
- `ops/specs/hook-apt-thu-lai-1-r1.md`
- `ops/leases/hook-apt-thu-lai-1-r1-g1-claude.yaml`
- `ops/acceptance/hook-apt-thu-lai-1/r1/VERDICT.md`
