# wp856 (`KG-RANG-TEST-2`) — hiện vật review của executor

- Packet #856, lease `wp856-r1-g1-claude`, đặc tả `ops/specs/wp856.md` sha256 `d50065e7…dd34` (nhánh `ops/wp856-spec`).
- Nhánh thi hành `agent/wp856-g1-claude`; head đã review `bf671b0524a8472eb0b0fcd1d75ea3a89d1f6973`; head đẩy là commit merge
  `origin/master` vào head ấy (diff so master vẫn đúng 1 tệp `.claude/dev/packet_loop_test.py`).

| lượt | head | verdict | ghi chú |
|---|---|---|---|
| 1 | `7302ea3` | `changes_requested — P2=4` | bị cắt khi container khởi động lại (`run.json` còn `dang_chay`); VERDICT ghi tăng dần |
| 2 | `19fdfa6` | `changes_requested — P2=3` | |
| 3 | `bf671b0` | `approve — P0=P1=P2=P3=0` | |

Thư mục `evidence/` của reviewer KHÔNG chép vào đây (dung lượng); `EVIDENCE_SHA256SUMS` là băm của nó tại lúc giao.
Nguồn có thẩm quyền là các tệp trong kho; comment trên #856 chỉ là bản chiếu.
