# wp498 — báo rõ phạm vi kiểm tra công cụ — revision 1

## Authority
Chủ kho duyệt đề xuất bằng “Đồng ý, duyệt và triển khai”, sau đó duyệt riêng
“Duyệt E1/E2 riêng #498 r1/g1” trong task Codex 01a0912a-91fb-79c3-b1ac-0eb2c55a721c, ngày 2026-09-11.
Đây là agent ghi hộ chỉ thị trực tiếp; GitHub submitter không tự chứng minh danh tính người ra quyết định.
Issue: https://github.com/ducthangho/tra-luat/issues/498. Corrective độc lập; #290 chỉ là nguồn gốc.
Không kế thừa bản vá/lease lịch sử. Lease mới chỉ có hiệu lực sau publish/readback và ownership pass.

## Phạm vi đóng băng
- revision: 1; generation: 1; packet_id: wp498.
- base_sha: 05ba3f96520a7f9e7f8676585cf6041e5e75c796.
- Executor: google_antigravity / antigravity / machine/local; model gemini-3.1-pro-high.
- Reviewer: openai_codex, phiên độc lập không fork context Executor; khai model/surface/session thực tế.
- Review class: sensitive; tối đa hai vòng review; mỗi run tối đa 90 phút.
- Product write set: ops/cong_cu.py; ops/cong_cu_test.py. Không companion/derived file được phép ghi.
- Thêm pham_vi, canary_da_quet, ghi_chu_pham_vi để báo rõ phạm vi kiểm một công cụ/toàn bộ.
- Giữ nguyên trang_thai_tong, RC, bat_buoc, chinh_sach và điều kiện chạy canary.
- Không gộp #249; không sửa workflow, launcher, credential, manifest, VERSION, CHANGELOG.
- Controller sở hữu hồ sơ điều phối trên nhánh riêng codex/wp498-authority-r1; AG không sửa hồ sơ này.

## Acceptance và bằng chứng
1. Có --chi: pham_vi=mot-cong-cu, canary_da_quet=false, ghi_chu_pham_vi giải thích chưa quét canary toàn bộ.
2. Không có --chi: pham_vi=toan-bo và canary_da_quet=true khi đã đi qua đường quét. Đã quét không có nghĩa mọi canary đạt.
3. Optional KHONG_DO_DUOC vẫn giữ trạng thái tổng/RC cũ nhưng tự khai giới hạn. Kết quả công cụ và canary cũ không bị sửa.
4. Test qua CLI thật, phân biệt hai phạm vi và bảo toàn RC. Mutant bỏ/sai khai báo bị test đúng đích bắt, không ghi công lỗi vô can.
5. Đo baseline/candidate trong cùng môi trường. Chạy ops/cong_cu_test.py và targeted test/mutant của sửa đổi; lưu command/RC/output dương.
6. Ruff F trên hai tệp không tăng lỗi. git diff --check sạch. Diff sản phẩm đúng hai tệp, dưới 300 dòng thêm; vượt thì dừng.
7. Freeze commit/head/tree, reviewer Codex kiểm Spec và Standards/Security độc lập. Mỗi finding kèm vị trí/cách vá/test/rủi ro.
8. Sau candidate cuối được review, một lượt CI gate trên exact head với Ubuntu và Windows; skipped/missing/failed là chưa pass.
9. Đích của nhiệm vụ: draft PR + review/evidence; không approve quyền land, merge, deploy hay LIVE. Gate nền đỏ vẫn ghi failed, không sửa ngoài packet.

## E1 — miễn trừ nền, đã được chủ kho duyệt riêng
Protocol §3.2 cấm agent tự khai bốn trường phái sinh, trong khi Dispatcher/change policy chưa có (#473).
Chỉ wp498 r1/g1 được để change_policy_sha, effective_write_set, required_checks, land_obligations chưa có;
không bịa hash/policy. Dùng hai đường chính xác và acceptance trên làm ràng buộc thủ công.
Kiểm giao bằng công cụ lease hiện hành, bổ sung full-ref snapshot và phân loại các ref/PR có thay đổi chạm hai đường.
Nếu cần thêm companion/write closure hoặc policy thay đổi, dừng để revision mới. Không sửa nợ #473 trong packet.

## E2 — điều phối AG thủ công, đã được chủ kho duyệt riêng
packet_loop hiện chỉ nhận claude/codex. Dùng lease + nhật ký GitHub thủ công cho AG thật;
không giả tên provider, không sửa/bypass mã cổng. Giữ revision/generation/spec hash, expiry,
heartbeat <=30 phút, exact SHA/tree và review budget. Khi reviewing ghi review_sla UTC tối đa hai giờ.

## Stop
Thiếu ownership/authority/model evidence; ref hoặc head thay đổi ngoài chuyển động đã ghi nhận;
lease hết hạn; cần ghi ngoài scope; finding lặp hoặc hết hai vòng review; model/provider đổi.
Prompt/rc=0 không tự chứng minh công việc đã làm. Probe AG không chứng minh model giữ nguyên trong lượt dài;
report giới hạn model identity nếu runtime không trả model trong receipt.

## Hash
spec_sha256/spec_hash là SHA-256 của toàn bộ byte UTF-8 LF của chính tệp này, không BOM.
Lease tách riêng để expiry/heartbeat không sửa byte spec.
