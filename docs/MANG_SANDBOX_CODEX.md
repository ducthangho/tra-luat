# Mạng ra ngoài của sandbox `codex sandbox` — quan sát → phép đo tái lập được

Packet `MANG-SANDBOX-CODEX`. Nguồn: quan sát 24-08-2026 "sandbox `codex` không có đường ra
mạng" — **chưa ai đo CƠ CHẾ** trước gói này. Doctrine giữ nguyên, không bị nâng cấp bởi tài
liệu này: **mạng đóng là một MẶC ĐỊNH CẤU HÌNH, không phải bất biến an ninh** — biết cơ chế
KHÔNG làm nó thành ranh giới, vì cờ lật được (xem bảng dưới).

Công cụ: `.claude/dev/probe_mang.py` — ba kênh độc lập, mỗi kênh in `TEN=MA` (`0`=lọt,
`1`=bị chặn): `bind_loopback` (đối chứng nội bộ, không ra mạng), `urlopen`, `git_ls_remote`.
Phản chứng: `.claude/dev/probe_mang_test.py` — chạy `python3 .claude/dev/probe_mang_test.py`.

## Việc 3 — bảng ba cột

Điều kiện đo (27-08-2026): OS `Linux 6.18.44-fc-v21 x86_64` · `python3 3.11.15` ·
`codex-cli 0.150.0` · `sandbox_mode=workspace-write` khi qua codex.

| lệnh (chạy tại gốc kho) | bind | url | git | mệnh đề |
|---|---|---|---|---|
| `python3 .claude/dev/probe_mang.py` | 0 | 0 | 0 | đối chứng NGOÀI codex — container này có mạng |
| `codex sandbox -c sandbox_mode=workspace-write -- python3 .claude/dev/probe_mang.py` | 1 | 1 | 1 | sandbox mặc định, KHÔNG cờ mạng — cả ba bị chặn |
| `codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -- python3 .claude/dev/probe_mang.py` | 0 | 0 | 0 | bật `network_access=true` — cả ba lọt: cấu hình lật được, KHÔNG phải ranh giới |

Ba lệnh trên là nguyên văn để tái lập; không đối số nào bị lược.

## Việc 4 — tách hai cờ (mạng đóng do cờ nào)

Bản ghi cũ trong kho mở **đúng hai** chốt cùng lúc (`network_access=true` VÀ
`writable_roots=[...]`) rồi khai `fetch_rc=0`/`lsremote_rc=0` — hai biến bật cùng lúc thì
KHÔNG cô lập được cờ nào là nguyên nhân (cross-review packet #318 đã bác một bản vá đúng vì lý
do này). Đo lại BỐN tổ hợp, mỗi cờ riêng, cùng một lệnh nền
`codex sandbox -c sandbox_mode=workspace-write [CỜ] -- python3 .claude/dev/probe_mang.py`,
`[CỜ]` thay bằng đúng cột dưới (`DUONG_DAN_GOC` = `$(git rev-parse --show-toplevel)`):

| tổ hợp | `network_access=true` | `writable_roots=["DUONG_DAN_GOC/.git","/tmp"]` | bind | url | git |
|---|---|---|---|---|---|
| (a) | không | không | 1 | 1 | 1 |
| (b) | CÓ | không | 0 | 0 | 0 |
| (c) | không | CÓ | 1 | 1 | 1 |
| (d) | CÓ | CÓ | 0 | 0 | 0 |

**Trả lời thẳng:** `network_access=true` MỘT MÌNH đủ đảo cả ba kênh — (b) khớp byte-với-byte
(d), và (a) khớp (c). `writable_roots` không đảo kênh nào. Cơ chế mạng **ĐÃ XÁC MINH**: cờ gây
mở mạng là `sandbox_workspace_write.network_access`, không phải `writable_roots`. Bản ghi cũ
đúng VỀ KẾT QUẢ nhưng sai VỀ HẠNG BẰNG CHỨNG (đo tổ hợp, không đo từng cờ); nay đã tách.

## KHÔNG_ĐO_ĐƯỢC

- Cơ chế HỆ ĐIỀU HÀNH đứng sau `network_access` (netns/seccomp/…) — bảng trên đo ở mức
  cờ cấu hình, không đo bằng cách nào kernel thực thi nó.
- Hành vi trên phiên bản `codex-cli` khác 0.150.0, hay trên Windows — chưa chạy được ở đây.
- `sandbox_mode` khác `workspace-write` (vd `read-only`, `danger-full-access`) — ngoài phạm
  vi packet này.
