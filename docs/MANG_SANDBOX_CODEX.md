# Sandbox mạng của Codex — quan sát có điều kiện

Packet `MANG-SANDBOX-CODEX` giữ nguyên doctrine: **mạng đóng là MẶC ĐỊNH CẤU HÌNH,
không phải bất biến an ninh**. Bảng dưới là số đã chốt ngày 27-08-2026, không phải lời
hứa cho phiên bản hay cấu hình khác.

Probe nay in `TEN=MA_CU class=LOP stage=GIAI_DOAN rc=RC raw=DU_LIEU_DA_KHU_NHAY_CAM`.
`MA_CU=0` ánh xạ `LOT`; `MA_CU=1` chỉ có nghĩa *không lọt*. Chỉ `class` mới phân biệt
`POLICY_DENIED`, `ENDPOINT_ERROR`, `DNS_ERROR`, `TIMEOUT`, `TOOL_ERROR`,
`REPOSITORY_ERROR`, `AUTH_ERROR`, `UNKNOWN`; `UNKNOWN` là `KHÔNG_ĐO_ĐƯỢC` và làm probe rc=1.
Hai bảng cũ giữ nguyên số 0/1; vì lượt đo cũ không lưu lớp/raw, không hồi tố số 1 thành policy-denied.

## Bảng ba cột đã chốt

Điều kiện: `Linux 6.18.44-fc-v21 x86_64` · Python 3.11.15 · `codex-cli 0.150.0` ·
`sandbox_mode=workspace-write` khi qua Codex.

| lệnh (tại gốc kho) | socket (cũ: bind) | url | git | LỚP đo được (socket · url · git) |
|---|---:|---:|---:|---|
| `python3 .claude/dev/probe_mang.py` | 0 | 0 | 0 | `LOT` · `LOT` · `LOT` |
| `codex sandbox -c sandbox_mode=workspace-write -- python3 .claude/dev/probe_mang.py` | 1 | 1 | 1 | `POLICY_DENIED`(create) · `POLICY_DENIED`(urlopen) · **`UNKNOWN`**(rc=128) |
| `codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -- python3 .claude/dev/probe_mang.py` | 0 | 0 | 0 | `LOT` · `LOT` · `LOT` |

**`1` KHÔNG đồng nghĩa "bị chặn bởi chính sách sandbox".** Ô `git` ở hàng giữa là `UNKNOWN`, tức
`KHÔNG_ĐO_ĐƯỢC` theo đúng luật ở đầu tệp — đừng đọc ba số `1` ấy thành một cơ chế chung.

## Bốn lệnh tách hai cờ

Khối Bash/Linux dưới đây là bốn lệnh nguyên văn đã được phiên điều phối rút từ chính tài liệu
và chạy lại; không dùng nó để tuyên bố đã tái lập trong sandbox Codex của executor lượt này.

```bash
DUONG_DAN_GOC=$(git rev-parse --show-toplevel)
codex sandbox -c sandbox_mode=workspace-write -- python3 .claude/dev/probe_mang.py
codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -- python3 .claude/dev/probe_mang.py
codex sandbox -c sandbox_mode=workspace-write -c 'sandbox_workspace_write.writable_roots=["'"$DUONG_DAN_GOC"'/.git","/tmp"]' -- python3 .claude/dev/probe_mang.py
codex sandbox -c sandbox_mode=workspace-write -c sandbox_workspace_write.network_access=true -c 'sandbox_workspace_write.writable_roots=["'"$DUONG_DAN_GOC"'/.git","/tmp"]' -- python3 .claude/dev/probe_mang.py
```

| tổ hợp | `network_access=true` | `writable_roots` | socket | url | git | LỚP (socket · url · git) |
|---|---|---|---:|---:|---:|---|
| (a) | không | không | 1 | 1 | 1 | `POLICY_DENIED` · `POLICY_DENIED` · **`UNKNOWN`** |
| (b) | CÓ | không | 0 | 0 | 0 | `LOT` · `LOT` · `LOT` |
| (c) | không | CÓ | 1 | 1 | 1 | `POLICY_DENIED` · `POLICY_DENIED` · **`UNKNOWN`** |
| (d) | CÓ | CÓ | 0 | 0 | 0 | `LOT` · `LOT` · `LOT` |

`network_access=true` một mình đã đảo cả ba quan sát; `writable_roots` không đảo ô nào.
Loopback không phải egress: cờ này gate capability socket rộng hơn hai phép HTTPS ra ngoài,
nên kết quả chỉ xác minh phạm vi cờ cấu hình đã đo, không xác minh một ranh giới mạng.

## KHÔNG_ĐO_ĐƯỢC

- Executor lượt này không chạy lại ba cột/bốn tổ hợp: `codex sandbox` lồng dừng `rc=101` trước probe.
- **`git` ở (a)/(c) bị chặn bởi CHÍNH SÁCH SANDBOX hay bởi HẠ TẦNG PROXY của phiên chạy — CHƯA
  TÁCH ĐƯỢC.** Môi trường phiên bơm `https_proxy` trỏ một cổng **loopback**; trong sandbox không mở
  `network_access`, `git` hỏng vì không nối được tới CHÍNH proxy ấy ("couldn't connect"), khác hẳn
  "operation not permitted" của hai kênh kia. `phan_loai_git()` fail-close đúng và trả `UNKNOWN`
  thay vì đoán. Hệ quả: `class` của `git` phụ thuộc cấu hình proxy TỪNG PHIÊN, không phải hằng số
  theo Codex — đừng suy nó ra môi trường khác.
- Chưa đo cơ chế kernel, OS/Codex/sandbox mode khác, và egress ngoài hai endpoint HTTPS đã chọn.
