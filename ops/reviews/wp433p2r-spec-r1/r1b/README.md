# Bản sửa r1b của đặc tả R (`GWS-CRED-DICH-NGOAI-KHO-R`)

- Bản cũ: `ops/specs/GWS-CRED-DICH-NGOAI-KHO-R-r1.md`, sha256 `4d4b3181…` (giữ nguyên, lease g1 trỏ tới).
- Bản mới: `ops/specs/GWS-CRED-DICH-NGOAI-KHO-R-r1b.md`, sha256 `43d60d7c8fa66f559c4754bf45d152bb0a2362bb6179fe49c557c9a71491fb78`.
  Dựng lại: `python ap_r.py ops/specs/GWS-CRED-DICH-NGOAI-KHO-R-r1.md <tệp mới>` (sha256 `ap_r.py` `93c4b1c1…`) ⇒ in đúng băm trên.
- Lý do: executor (phiên `session_015GtxrYN8oeEszoAzSfeQFV`) phát hiện khi thi công trên `20eac11` — phép thay cũ của đột biến 2 (`!= 0`)
  chết sai lượt trên nt vì `os.lstat` của Windows đặt `st_file_attributes` khác 0 cho mọi entry thật.
- Đo xác nhận (phiên điều phối #1206, 2026-11-19T21:3xZ, Desktop `DESKTOP-T9R33P2`, Windows 11, Python 3.12.10): `probe_db2.py`
  (sha256 `93d92dbb70d4296969e1912fbdbf8a7ec8e2d7e5996ba4289db7f4cf0c7ed28c`, tự chứa) — đầu ra thô ở `probe-desktop.txt`.
- Chủ kho duyệt băm `43d60d7c` 19-11 (ADR-0067, AskUserQuestion phiên #1206), không qua review Codex thêm.
