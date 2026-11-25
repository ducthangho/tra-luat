### 1.1 Bảng bất biến protocol

Mỗi nguyên tắc dưới đây là một BẤT BIẾN có ID ổn định. Cột `cổng` mang đúng một trong ba giá trị: `cổng: <tệp> <chốt> · ca: <tệp test>::<tên ca>` (có cổng máy và ca phản chứng) · `kỷ luật, 0 cổng · nợ: <TÊN-NỢ>` (chỉ sống bằng kỷ luật đọc, nợ ghi ở `ADR-0068`) · `chưa đo`. `adr-song` ĐỎ khi một dòng thiếu, trùng ID, rỗng, sai dạng cột cổng, trỏ ca không tồn tại, hoặc khi tập ID lệch danh sách đã biết trong mã. Thêm, bỏ hay đổi ID là sửa danh sách ấy qua một packet có review (`ADR-0068`).

| INV | bất biến | nguồn | cổng |
|---|---|---|---|
| `INV-01` | Mỗi packet có đúng một executor ghi và một lease generation còn hiệu lực | §1 (1), §4 | cổng: `.claude/dev/packet_loop.py` `record-lease --lease-ref` I2(Đ) · ca: `.claude/dev/packet_loop_test.py::r812_nguoi_giu_khac` |
| `INV-02` | Không hai lease còn hiệu lực có effective write set giao nhau trên toàn kho | §1 (2), §5 | cổng: `.claude/dev/packet_loop.py` `record-lease --lease-ref` I2(Đ) · ca: `.claude/dev/packet_loop_test.py::r812_nguoi_giu_prefix_giao_nhau` |
| `INV-03` | Worker không ghi canonical, không bump version, không deploy, không giữ credential LIVE | §1 (3), §11 | chưa đo |
| `INV-04` | Canonical chỉ đổi qua land cho đúng exact head đã được uỷ quyền; deploy là cổng riêng | §1 (5), §13 | cổng: `.claude/dev/packet_loop.py` `kiem-merge` K0 · ca: `.claude/dev/packet_loop_test.py::cong_c_k0_pr_head` |
| `INV-05` | Tệp text tracked dùng LF, riêng `*.cmd` và `*.bat` dùng CRLF | §1 (6), §9 | cổng: `.github/workflows/ci.yml` bước `eol-policy selftest` · ca: `.githooks/eol_policy_test.py::case_new_file_crlf_bi_chan` |
| `INV-06` | Một phiên giữ một vai trên một đơn vị công việc; executor không tự review hay approve | §1 (8), §2 | cổng: `.claude/dev/packet_loop.py` `init` · ca: `.claude/dev/packet_loop_test.py::init_cung_provider_thoat_4` |
| `INV-07` | Review, CI, authorization và land evidence gắn exact SHA; head đổi thì bằng chứng cũ hết hiệu lực | §1 (9) | cổng: `.claude/dev/packet_loop.py` `record-review` · ca: `.claude/dev/packet_loop_test.py::review_phai_neo_head_da_dua_ra_review` · ca: `.claude/dev/packet_loop_test.py::cong_c_k4_head` |
| `INV-08` | Packet Spec đóng băng bằng `spec_hash`; đổi hợp đồng thì revision mới | §3.2 | cổng: `.claude/dev/packet_loop.py` `kiem-merge` K1 · ca: `.claude/dev/packet_loop_test.py::cong_c_k1_hash` |
| `INV-09` | Diff ngoài effective write set bị từ chối | §5 | kỷ luật, 0 cổng · nợ: `INV-09-DIFF-NGOAI-WRITE-SET` |
| `INV-10` | Handoff mang bằng chứng dương và `tested_sha` bằng head đưa ra review | §7 | kỷ luật, 0 cổng · nợ: `INV-10-HANDOFF-KHONG-CO-CONG` |
| `INV-11` | Assurance tính theo họ model phục vụ; class `sensitive` cần `cross_approved` hoặc `human_audited` | §8 | cổng: `ops/bien_nhan_v2.py` chốt tách họ model · ca: `ops/bien_nhan_v2_test.py::c49_cross_approved_cung_ho_model_phai_bi_tu_choi` |
| `INV-12` | Mọi lượt review (mã, đặc tả, kế hoạch) xuất verdict theo lớp: mỗi finding một `class_slug`, bảng lớp, đối chiếu lượt trước bằng bốn nhãn | §7, §8, §8.3 | kỷ luật, 0 cổng · nợ: `INV-12-CONG-VERDICT-THEO-LOP` |
| `INV-13` | Review Class tính fail-closed; executor không hạ lớp | §8 | cổng: `ops/lease_publish.py` `_kiem_lop_review` · ca: `ops/lease_publish_test.py::t74_A1_A2_executor_khong_duoc_ha_lop_va_ve_dung_phai_QUA` |
| `INV-14` | Reviewer chỉ đọc: không ghi vào nhánh packet hay checkout được giao | §8, §8.2 | cổng: `.claude/dev/launcher.py` `run --chup-workspace` · ca: `.claude/dev/launcher_test.py::r1252_ghi_trong_git` |
| `INV-15` | `landed` đòi đủ bốn mốc provenance | §10.2.2 | cổng: `.claude/dev/packet_loop.py` `kiem-dong-wp` D2 · ca: `.claude/dev/packet_loop_test.py::cong_c_d2_not_measured` |
| `INV-16` | Trần lời gọi Codex, vòng review và attempt là stop condition; đổi prompt hay phiên không reset bộ đếm | §12 | cổng: `.claude/dev/packet_loop.py` `record-codex-call` · ca: `.claude/dev/packet_loop_test.py::pl_m3_codex` |
| `INV-17` | Agent chỉ hỏi chủ kho theo danh sách đóng E1–E5 | §12 | kỷ luật, 0 cổng · nợ: `INV-17-DANH-SACH-DONG-0-CONG` |
| `INV-18` | Registry chỉ ghi qua GAS webapp; không thêm đường ghi thứ ba | `CLAUDE.md` | kỷ luật, 0 cổng · nợ: `INV-18-DUONG-GHI-REGISTRY-0-CONG` |
| `INV-19` | Agent không tự cấp lease; người cấp thuộc danh sách cho phép và lease hết hạn thì hết quyền | §1 (4), §4 | cổng: `ops/lease_publish.py` `kiem` · ca: `ops/lease_publish_test.py::t02_granted_by_la_ten_provider_bi_CHAN` |
| `INV-20` | Adapter và `CLAUDE.md` chỉ trỏ protocol, không chép doctrine | §13 | cổng: `.claude/dev/packet_loop.py` `doctrine-scan` · ca: `.claude/dev/packet_loop_test.py::doctrine_scan_chep_tron_5_1_bi_chan` |
| `INV-21` | Finding P0, P1, P2 còn mở chặn merge; P3 phải đóng có bằng chứng hoặc được miễn neo SHA | §8 | cổng: `.claude/dev/packet_loop.py` `kiem-merge` K3, K5 · ca: `.claude/dev/packet_loop_test.py::cong_c_k3_p1` · ca: `.claude/dev/packet_loop_test.py::cong_c_k5_p3_khong_mien` |
