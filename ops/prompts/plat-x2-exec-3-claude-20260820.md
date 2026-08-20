# Prompt BẤT BIẾN — Executor `PLAT-X2`, **revision 3**, lượt 3, provider `claude`

Revision 3 **thay** revision 2. Chỉ ghi phần DELTA; lõi vẫn là thân Issue `#195`.

## 1. Vì sao có revision 3 — hệ quả cơ học, không phải phạm vi mới

`.gitignore` (đã nằm trong write set từ revision 1) là **tệp ĐƯỢC ĐÓNG GÓI**: nó có mặt
trong `RELEASE_MANIFEST.json` với `size` + `sha256`. Thêm một dòng vào nó là đổi băm của
gói, và cổng `release-verify --strict` bắt đúng chỗ ấy:

```
failed: [{path: ".gitignore", expected_size: 1259, actual_size: 1282,
          expected_sha256: 7640fa50…, actual_sha256: 28e4f7ee…}]
checked_file_count: 180 / expected 180      ← KHÔNG thêm/bớt tệp, chỉ lệch băm
```

`CLAUDE.md` §Quy ước deploy mục 5 quy định: đổi cây ⇒ **tái sinh `RELEASE_MANIFEST.json`**.
Nên revision 3 thêm đúng **một** đường dẫn: `RELEASE_MANIFEST.json`.

**ĐÍNH CHÍNH một lời khai của lượt trước.** Tôi đã báo "CI đỏ vì runner thiếu `actionlint`".
Sai ở chỗ nói *vì*: có **hai** nguyên nhân độc lập chồng lên nhau, và tôi kết luận khi mới
thấy một. Nền master xanh (`58900b2`), nên cả hai đều là lỗi của lượt này.

## 2. Write set revision 3 (6 tệp)

```
.github/workflows/ops-publish-lease.yml
ops/lease_publish_test.py
.gitignore
.github/workflows/ci.yml
ops/NO_KY_THUAT.md
RELEASE_MANIFEST.json                        MỚI ở revision 3
```

## 3. Nghiệm thu bổ sung

- `release-verify RELEASE_MANIFEST.json --strict` → `"ok": true`.
- `golden-test` · `determinism-audit --strict` · `workflow-audit --strict` → `"ok": true`.
  Số tệp giữ nguyên **180** nên golden **không** phải ghi lại — nhưng phải ĐO, không suy.
- Diff của manifest đúng **5 dòng**: `total_bytes`, `package_hash`, `content_hash`, và
  `size`+`sha256` của `.gitignore`. Nhiều hơn thế là dấu hiệu tái sinh đã kéo theo thứ khác.
- `doc-claims-check --strict` toàn kho: cờ duy nhất còn lại nằm ở tệp **không thuộc diff**
  và do **clone cục bộ thiếu object**, không phải do lượt này — đo lại nền trước khi nghi.

## 4. Cấm

- Không đụng tệp thứ bảy. Cần ⇒ DỪNG, mở revision 4.
- Không `golden-test --write` để "cho khớp": số đếm không đổi thì không có gì để ghi lại.
- Không gọi thêm lượt review codex — cả hai trần đã cạn, người giữ đã chọn land kèm nợ.
