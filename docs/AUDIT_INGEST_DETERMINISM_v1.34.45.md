# Báo cáo audit tra-luat v1.34.45

Ngày audit: 2026-07-14  
Phạm vi: `ingest`, `ingest-local`, `profile-ingest`, ingest URL/Drive/cache/ZIP, registry/readback, deterministic JSON và release bundle.  
Nguồn audit: `tra-luat-skill-v1.34.44.zip`; SHA-256 gốc `8BB63134973317E39623F274E2B7465FFC49749FB603C33C2CD837011041E2B3`.

## Kết luận

Toàn bộ bug blocker/major phát hiện trong phạm vi đã được sửa. Pipeline mới dùng fail-closed, identity theo byte nguồn, plan-hash bắt buộc cho apply, readback sau ghi, ZIP portable-safe và release tái lập byte-for-byte.

Các cổng offline đã đạt:

- selftest: 900/900;
- golden fixtures: 18/18;
- `workflow-audit --strict`: đạt, không warning;
- `determinism-audit --strict`: đạt;
- parser surface: khớp snapshot;
- benchmark dry-run ZIP end-to-end: +1,09%, dưới ngưỡng 15%.

Không thực hiện live write vào Drive/Registry/NotebookLM của người dùng trong audit này. Live smoke cần chạy tại môi trường đích với credential và tài liệu test có thể rollback.

## Phát hiện và xử lý

| Mức | Vấn đề trước sửa | Hệ quả | Xử lý v1.34.45 |
|---|---|---|---|
| Blocker | Registry/Drive response `{}` hoặc thiếu `ok` có thể bị coi là thành công | False success, pipeline tiếp tục sang NLM | Mọi write/readback yêu cầu bằng chứng dương; thiếu field là fail |
| Blocker | Lệnh `ingest` legacy có write path riêng, tin response `organize`, không verify đủ Registry/NLM | Hai engine sai khác nhau; báo xong khi corpus chưa xong | Biến thành adapter mỏng sang `ingest-local`; QT-2 `REVIEW` luôn chặn |
| Blocker | `--apply` không gắn với dry-run đã duyệt | Nguồn/tùy chọn có thể đổi giữa plan và apply | Bắt buộc `--confirm yes --expected-plan-hash`; mismatch fail trước write |
| Major | Resume/cache có thể chọn theo tên, số hiệu hoặc bản mới nhất | Nối nhầm journal/biến thể; vá nhầm cache | Chỉ exact `identity_hash + plan_hash` và exact `doc_key`; không fallback |
| Major | File giả đuôi DOCX/PDF/XLSX có thể đi sâu vào pipeline | Parse sai, convert lỗi muộn, tăng bề mặt tấn công | Kiểm magic, ZIP container members, size và extension/MIME |
| Major | URL download không có hợp đồng policy/streaming đầy đủ | Tải quá cỡ, redirect bất ngờ, khó dùng trên nhiều host | Stream giới hạn byte/timeout/redirect; scheme và allowlist host do môi trường cấp |
| Major | Cache patch quét toàn bộ và match chỉ theo số hiệu | Xung đột hai variant; O(n) mỗi ingest | Dùng thẳng `docs/<doc_key>.json`, verify `doc_key`, ghi atomic |
| Major | Cache writer không khóa theo identity; lock O_EXCL cũ có thể bị bỏ lại sau crash | Lost update hoặc tắc vĩnh viễn | Lock riêng từng identity, phá lock chủ process đã chết/stale, không dùng global lock |
| Major | ZIP chỉ chặn traversal cơ bản | Reserved Windows, trailing dot/space, Unicode/case collision, symlink/special entry có thể thoát contract | Chuẩn hóa NFC/portable path; chặn toàn bộ các trường hợp trên |
| Major | ZIP thiếu giới hạn tổng uncompressed/ratio và plan không khóa bytes archive | Zip bomb; thay ZIP sau dry-run | Cap tổng size/ratio/member; archive SHA-256 + member SHA-256; extract đúng plan |
| Major | Child ingest fail có thể không làm parent fail rõ | Lô báo hoàn thành dù một số item hỏng | Thu thập return code/JSON từng child; ingest-zip XỬ LÝ MỌI member (child độc lập+idempotent) rồi báo `counts{applied,failed}`+`partial`, `ok=all(member)` — KHÔNG fail-fast; `continue-on-error` giữ để tương thích, không đổi hành vi (sửa v1.34.45 merge) |
| Major | JSON deterministic scrub theo heuristic giá trị | Có thể làm sai regex, timestamp nghiệp vụ hoặc chuỗi chứa `\` | Serializer chỉ canonical hóa key/Unicode; audit projection khai báo field volatile/path |
| Major | Normalizer tự chèn timestamp hiện tại và JSON/index không khóa thứ tự | Cùng input sinh output khác byte | Không timestamp ngầm; chỉ ghi `--recorded-at`; JSON sort key, LF, atomic |
| Major | Release verifier không fail chặt mọi hash/metadata | Gói thay đổi vẫn có thể được chấp nhận | Verify package/content/archive hash, safe path, file set và ZIP metadata |
| Major | ZIP release nén phụ thuộc zlib/nền tảng | Không byte-for-byte reproducible | `ZIP_STORED`, thứ tự sort, timestamp/quyền cố định |
| Moderate | `reg-delete` chưa đòi confirm nhất quán | Dễ xóa nhầm | Bắt buộc `--confirm yes`; registry metadata audit kiểm cờ |
| Moderate | `ingest-analyze` sinh lệnh apply sai positional và thiếu plan-hash | Hướng dẫn tự tạo ra lệnh không an toàn | Sinh dry-run command và apply template có confirm/plan-hash |

## Thiết kế đã chốt

Các quyết định sống trong `docs/adr/0004` đến `0007`:

1. Một ingest contract/engine chung; CLI chỉ là adapter.
2. Source policy thuộc môi trường, không hard-code danh sách domain trong skill.
3. Identity theo nội dung; thay thế phải tường minh.
4. Release bundle tái lập byte-for-byte.

## Lợi ích và nhược điểm

| Thay đổi | Lợi ích | Chi phí/nhược điểm |
|---|---|---|
| Plan-hash + confirm | Người duyệt đúng thứ sẽ được ghi; chặn TOCTOU | Thêm một bước copy `plan_hash`; script tự động cũ phải cập nhật |
| Fail-closed readback | Không còn `ok:true` giả | Hệ thống đích chậm/chập chờn có thể làm nhiều lệnh dừng hơn; phải resume sau khi backend ổn định |
| Env-owned source policy | Chạy trên Claude Chat/Cowork/Code và nhiều host mới mà không phải sửa skill | Môi trường phải quản lý policy; allowlist rỗng nghĩa là không áp host restriction ngoài scheme |
| Hash archive/member | Phát hiện thay nguồn và collision, ràng buộc apply | Tăng chi phí CPU/I/O của hàm plan; trên fixture 10,49 MB là khoảng 62 ms, nhưng end-to-end chỉ +1,09% |
| Exact cache `doc_key` | Không nhầm variant; O(1) | Cache legacy không có `doc_key` chính xác sẽ fail rõ thay vì đoán |
| `ZIP_STORED` release | Cùng input cho cùng byte trên Windows/Linux/Python khác nhau | File ZIP lớn hơn ZIP nén; đổi lại xác minh reproducible đơn giản và chắc chắn |
| ZIP workers (mặc định 4, trần cứng 8) | Giảm wall-time lô mà không tạo bão request | Backend quota thấp có thể cần hạ `--workers`; thứ tự kết quả vẫn được sort tất định |

## Cấu hình source policy

Skill không chứa allowlist domain cứng. Môi trường có thể cấp:

```text
TL_SOURCE_POLICY=environment
TL_SOURCE_SCHEMES=https,http
TL_SOURCE_ALLOW_HOSTS=vbpl.vn,*.chinhphu.vn,*.gov.vn
TL_SOURCE_MAX_BYTES=36700160
TL_SOURCE_TIMEOUT_S=180
TL_SOURCE_MAX_REDIRECTS=5
TL_SOURCE_PROVIDER=claude-cowork
```

`TL_SOURCE_ALLOW_HOSTS` là tùy chọn. Mẫu `*.example.vn` chỉ khớp subdomain; nếu muốn cho phép cả apex thì thêm `example.vn`. Local file luôn đi qua `--input`; `file://` bị chặn.

## Quy trình CLI mới

```text
# 1. Dry-run
tl ingest-local <file> --auto-plan --json

# 2. Apply đúng plan đã duyệt
tl ingest-local <file> --auto-plan --apply --confirm yes \
  --expected-plan-hash <plan_hash> --json

# ZIP tương tự
tl ingest-zip <file.zip> --cat <NN> --json
tl ingest-zip <file.zip> --cat <NN> --apply --confirm yes \
  --expected-plan-hash <plan_hash> --json
```

## Benchmark

Máy chạy audit: Windows, Python 3.13; median sau warm-up.

| Ca | v1.34.44 | v1.34.45 | Chênh lệch |
|---|---:|---:|---:|
| CLI `ingest-zip` dry-run, ZIP_STORED 40 file/10.489.702 byte | 628,77 ms | 635,62 ms | +1,09% |
| Riêng `_zip_plan` cùng fixture | 1,33 ms | 63,50 ms | +62,17 ms do hash mật mã |
| Cache metadata, 1.000 record | 275,41 ms | 6,58 ms | -97,61% |

Ngân sách đã chốt là ≤15% cho median luồng local end-to-end; kết quả +1,09% đạt. Hash không bị bỏ vì đây là bằng chứng an toàn, không phải overhead trang trí.

## Kiểm tra còn phải chạy tại môi trường đích

1. `live-readiness --json` và `live-contract-check --json`.
2. Snapshot `before`.
3. Ingest một tài liệu smoke có thể xóa/rollback, kiểm tra Drive + Registry + NLM readback.
4. Snapshot `after`, `live-state-diff`, sau đó rollback và xác nhận net-zero.

