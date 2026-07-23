# ADR-0007 — Bundle tái tạo giống byte tuyệt đối, ưu tiên tính tất định hơn kích thước

- **Trạng thái:** Accepted (2026-07-14, phiên audit ingest và tính tất định)
- **Bối cảnh:** Manifest canonical có thể ổn định nhưng ZIP dùng DEFLATE vẫn có thể khác byte giữa phiên bản
  zlib/runtime. Verifier hiện còn có nhánh trả `ok=true` khi `package_hash` sai. Chỉ so nội dung logic không đủ
  để chứng minh artifact được giao chính là artifact đã kiểm thử.
- **Quyết định:**
  1. Bundle mang hai lớp định danh: `content_hash` của manifest canonical và `archive_sha256` của byte ZIP.
  2. Exporter dùng `ZIP_STORED`, cố định root name, thứ tự entry, timestamp, permission, platform flag và UTF-8
     metadata; loại cache, tệp tạm và thời gian build khỏi nội dung được hash.
  3. Release gate build hai lần và yêu cầu SHA-256 giống nhau. Mismatch manifest/package/archive luôn thất bại;
     chế độ strict chỉ quyết định việc chấp nhận tệp thừa, không được nới kiểm tra hash.
  4. Verifier archive ràng buộc cả topology và manifest nhúng: đúng một root portable, không entry trùng/collision,
     không directory/special entry, metadata ZIP đúng canonical, mọi size/SHA khớp và `RELEASE_MANIFEST.json`
     trong ZIP phải bằng manifest dùng để verify. Duyệt một lượt O(n); không giải nén ra filesystem.
- **Phương án đã loại:**
  - *Giữ DEFLATE và chỉ cố định timestamp/thứ tự* — compressed bytes vẫn phụ thuộc implementation/runtime.
  - *Chỉ công bố content hash* — không chứng minh file ZIP được giao không bị đổi metadata hoặc thay byte.
  - *Cho non-strict bỏ qua package hash* — biến kiểm tra toàn vẹn thành advisory và đã tạo thành công giả.
- **Hệ quả:** Bundle lớn hơn nhưng đóng/mở nhanh hơn, dễ so sánh và tái tạo xuyên môi trường. Kênh phân phối phải
  lưu/công bố cả hai hash; mọi thay đổi metadata archive có chủ ý cũng tạo archive hash mới. ZIP được đóng lại
  bằng công cụ khác dù giữ nguyên nội dung sẽ không còn được coi là artifact canonical.

## Amend r194 (v1.35.25, 2026-07-24) — ZIP_DEFLATED mức 9 cố định

- **Bối cảnh:** bundle chạm 6,4MB (ZIP_STORED toàn phần); user yêu cầu hạ kích thước. Đo lại rủi ro
  "compressed bytes phụ thuộc implementation": mọi phép so archive-hash của quy trình đều là **build ×2
  trong CÙNG MÔI TRƯỜNG** (gate local ×2; CI build 2 bản CỦA CHÍNH NÓ rồi so nhau; deploy so bản build
  với bản tải ngược CÙNG artifact) — không có phép so hash cố định xuyên máy. Per-file SHA-256 trong
  `RELEASE_MANIFEST.json` tính trên NỘI DUNG GIẢI NÉN nên bất biến với mức nén; `release-verify` trong
  gói không đổi ngữ nghĩa.
- **Quyết định:** writer chuyển `ZIP_DEFLATED` `compresslevel=9` cố định (metadata vẫn đóng băng như cũ);
  verifier archive chấp nhận {STORED (bundle cũ), DEFLATED}; check `compress_size==file_size` chỉ áp cho
  STORED. Phần còn lại của ADR (root/thứ tự/timestamp/permission cố định, repro-gate ×2, hai hash) giữ
  nguyên hiệu lực. Kết quả đo: 6,4MB → ~1,5MB.
- **Ràng buộc mới:** archive-hash chỉ có nghĩa trong cùng môi trường build (zlib cùng bản). Nếu tương lai
  cần so hash xuyên máy (vd CI so với hash công bố sẵn) thì phải quay lại STORED hoặc pin zlib — mở lại
  amend này bằng ADR mới.
