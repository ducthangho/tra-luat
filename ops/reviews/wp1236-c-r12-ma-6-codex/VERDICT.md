Review độc lập wp1236 đợt C, r12/g1, lượt 6/6: **approve**, không còn finding P0/P1/P2/P3 mở trong phạm vi review mã.

- Reviewed SHA: `45944c7c3f4c75beaa87f36138b2bba9fb9198a3`.
- Tree: `66a0f315c1cf27eaac67beae06ee20cd1789f23a`.
- Base: `f602325574c62184caf16309631f5f680ca5cee2`.
- Spec SHA-256: `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`; local copy khớp blob nguồn `e5583bc042448517b94eadda57231dfc60e0a284`.
- Provider/surface/transport: `openai_codex / codex_cli / machine/local`; run `e72e7cbbf0e04bc78cf16c4603ef3f9d`. Model và effort phục vụ: `KHONG_DO_DUOC`; effort được yêu cầu: high. Linux, Python 3.13.18, Ruff 0.15.15. Không gọi mạng.

C05 **ĐÃ VÁ THẬT**. Điều kiện tại `packet_loop.py:3990` kiểm dấu chéo ngược trên `join(dirname(link), readlink)` trước `normpath`, kiểm đích thô chuẩn tắc và kiểm tên đích trùng chính xác tập tệp. `cam_cheo_chi_dich_tho` chỉ bị lkj bắt; `bo_chuan_tac` chỉ bị `nen_giu_nguyen_dich[lkl]` bắt. Bốn phản chứng backslash của lượt 5 nay rc 12. Bảy trường hợp giữ nguyên đích không chuẩn tắc nay rc 12; regular/executable/nested/nonutf_exact vẫn rc 0. Hai probe được chép nguyên byte từ lịch sử.

| Lớp lịch sử | Nhãn lượt 6 | Bằng chứng chính |
|---|---|---|
| `archive-loc-mat-du-lieu-kiem` | `DA_VA_THAT` | Probe đường dẫn/mode, mô hình alias, collision thư mục, ma trận C4 |
| `symlink-tren-dia-lech-cay` | `DA_VA_THAT` | Giữ alias của lớp trên từ lượt 4; không đếm thêm lớp |
| `hop-dong-dau-ra-duong-dan-tu-do` | `DA_VA_THAT` | LF cả hai nhánh rc 12; ca miền ký tự và chẩn đoán một dòng đạt |

Hội tụ lượt 5→6: **1/1 lớp**. Lịch sử lớp archive lặp ở lượt 1,2,4,5 được giữ nguyên; lượt 6 được chủ kho cấp tại issuecomment-7182681531, không reset ngân sách. C04 lịch sử được phân biệt với thay đổi acceptance của chủ kho, không gọi đổi luật là bản vá riêng.

Các phép đo reviewer thực chạy (command, rc và hash chi tiết trong `VERDICT.json`):

- `chay_ca.py repo ca cong_d2b_`: rc 0, **17/17**, không skip.
- `chay_ca.py repo db d2b_k2_`: rc 0, **19/19 GIET**, đối chứng khác họ không đỏ.
- `ma_tran_c4.py repo`: rc 0, **43 biến thể × 31 đột biến**; gốc 0 lệch; mọi mutant có ChotB4 đúng ca. lk5 hợp lệ vẫn qua, symlink YAML vẫn bị module chặn.
- `probe_paths.py`, `probe_modes.py`, `probe_models.py`, `probe_behavior.py`, `do_probe_l2.py`: process rc 0; kết quả gate bên trong phân biệt rc 0/12/8, không nhầm process hoàn tất với gate đạt.
- `legacy_ab.py`: rc 0, **13/13 mỗi vế** base/head. Con số 14 trong một cập nhật giữa lượt là nhầm và đã đính chính.
- Luật 9: khối trích, manifest **235** và ledger tái sinh khớp. Mẫu 11 có baseline 16 ca đạt, **8 GIET + 3 SONG tương đương**, rc 0; ba chứng minh tương đương đã kiểm lại. Không tuyên bố tự chạy lại toàn bộ 235.
- Bare Ruff F trên hai tệp: **failed, rc 1 ở cả base/head**, 16 lỗi mỗi vế, diagnostic delta = 0. Pin/probe contract riêng: rc 0, `RUFF_CONTRACT 3 []`.
- Numstat **+438/−13**, hai tệp đúng write set, trong trần +450; `git diff --check f602325 HEAD`: rc 0.
- Snapshot đầu/cuối: HEAD/tree, Git state và hash hai tệp không đổi. `.codex/` ignored có sẵn; không chứng nhận byte toàn bộ ignored hay lịch sử không từng ghi rồi hoàn nguyên.

Đã tái dựng bảng A/B từ log executor: 1784→1801 ca, 2009→2077 mutants, delta hồi quy 0; `r1187_spec_packet_type` đỏ sẵn ở cả hai vế. **38 ca và 1 mutant skipped mỗi vế không tính là passed**. Full A/B và 236/236 mutant khai báo là bằng chứng executor, không phải toàn bộ phép đo reviewer đã chạy.

M3 Windows **required**. Điều phối khai exact SHA này đạt trên Python 3.12.10 (base118/118, head135/135, tập trung), nguồn issuecomment-7184957862; reviewer Linux **not_run** native Windows và không xác minh GitHub. Năm fixture lkf–lkj **vắng mặt** trên Windows, dù báo cáo không có skipped; điều cấm backslash tại đó chỉ đo qua lka. Cả năm đã được đo độc lập trên POSIX ở lượt này.

Nợ (3) Windows/Python mới là giới hạn tương thích và đo đã khai, được chủ kho quyết giữ tại issuecomment-7182681531. Bộ bung đổi `linkname` sẽ bị chốt nội dung chặn rc 8 trước danh sách; ca đòi rc 12 có thể đỏ, kể cả đích hợp lệ có `/` có thể bị chặn. Không phát hiện đường fail-open mới, không tuyên bố interpreter ấy được hỗ trợ hay đã kiểm native. Các đích tuyệt đối/thoát gốc chỉ phân tích bằng lời; không soạn payload và không khai đã chạy. Gitlink thật được probe chặn rc 8; việc không thêm whitelist mode riêng đúng điểm (c) chủ kho đã chốt.

Bảng từng mệnh đề–dòng mã–ca–đột biến, quét độc lập theo lớp, giới hạn và hash bằng chứng nằm trong `VERDICT.json`. Không có P3 chờ miễn. Đây là verdict review mã; owner audit, CI và quyền merge/land là nghĩa vụ riêng, chưa được chứng nhận bởi lượt offline này.

KET_LUAN: approve
