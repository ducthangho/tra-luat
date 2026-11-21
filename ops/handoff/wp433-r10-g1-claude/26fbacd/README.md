# Handoff wp433 r10-g1 — SECRETS-SET-BUNDLE-KIEU r5, ứng viên `26fbacd9d4ba73f8e83359e9af060a76b32cae08`

Định danh ứng viên là BĂM, không phải tên nhánh. Nhánh code `agent/wp433-r10-g1-claude` CHƯA push; ứng viên nằm trong
`wp433-r10-g1-claude-26fbacd.bundle` (sha256 `ab27262a…`). Tái lập:

```
git fetch <bundle> agent/wp433-r10-g1-claude:agent/wp433-r10-g1-claude   # cần 8656dc0 trong kho
bash rig/gate_n5.sh <clone_co_ung_vien> 8656dc0176ed108e12c209ba55c91a1f6f9d612f 26fbacd9d4ba73f8e83359e9af060a76b32cae08 <ra> <thu_muc_rig>
```

| tệp | nội dung |
|---|---|
| `handoff.yaml` | handoff §7 |
| `rig/sinh_ma_tran.py` → `rig/ma-tran-n4.json` | ma trận N4 (sha256 `2d6f4011…`): 23 đột biến (tập đích khai theo cơ chế), 5 tự kiểm, 2 đo nền |
| `rig/rig_n4.py` | mỗi mục một tiến trình mới, đọc bản đồ `WP433_SS_BAN_DO` của chính tiến trình; phân hạng GIET/SONG_SOT/LECH_TAP/TIN_DUNG_GIA/HONG |
| `rig/gate_n5.sh` | dựng hai clone trong một lệnh, chạy N1–N5 + N4 |
| `gate/gate.log` | dòng tóm tắt có giờ UTC; `gate/n4/ket-qua-n4.json` chi tiết N4 |
| `gate/{nen,sau}.*` | đầu ra từng cổng của hai vế |

Kết quả: selftest 1785→1786 (N/N), N1–N3 346/346, N4 30/30 (0 khoá chưa phủ, (c) SỐNG, (d) LECH_TAP), release-verify 186==186,
numstat 4 tệp +164/−8. Mọi công khai (container khởi động lại, commit dựng lại, thứ tự đo base) ở `handoff.yaml` › `cong_khai_trung_thuc`.
