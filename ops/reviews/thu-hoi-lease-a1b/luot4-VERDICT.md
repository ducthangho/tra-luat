<!-- Verdict codex lượt 4 (gpt-6-astra high, codex_cli tại chỗ) trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 4 @ 52831cc, base 67802bf. Chép nguyên văn từ tệp -o của codex exec; chỉ bỏ khoảng trắng cuối dòng theo tiền lệ ops/reviews/thu-hoi-lease-a1a-r2/. -->
Không có finding P1/P2/P3 mới. **F8 đã vá thật ở mức đặc tả**; chưa chứng nhận implementation của WIRING.

```text
assurance: advisory_review
provider: openai_codex
execution_surface: codex_cli
transport: machine
base: 67802bf9a1b9adba6d8b13c63ee46744d74655b5
reviewed_sha: 52831cca2335a9237bcd846f72f72fabcc913caf
reviewed_tree: f90974b30aab860e2556dc70fdb4387b184384d2
spec_sha256: d135c6215680355de932ca5ec8db15bc856f6994a0ec4bea57d14838bf3519ec
```

**Đối chiếu lượt trước — F8:** tại `ops/specs/THU-HOI-LEASE-A1b.md:50` và `:105`, T6/A6 nay phân biệt đúng hợp đồng từng đường, giữ validator admission độc lập với cờ.

Đã chạy `python3 -B -`, dùng `_kho_thu`, `lease_mau`, `_goi_main` dựng lại fixture lượt 3 trong `/tmp`; **rc=0**:

```text
flag False check rc 0   forecast 8
flag False holder rc 11 NGƯỜI_GIỮ 1: moi-thay-the
flag False admission rc 0 TAP_THU_HOI_RONG
flag True  check rc 0   forecast 8
flag True  holder rc 11 NGƯỜI_GIỮ 1: moi-thay-the
flag True  admission rc 0 TAP_THU_HOI_RONG
```

Đây là hành vi **mã nền**, chưa có WIRING. Phép áp các điều kiện A6 mới lên phản chứng, **rc=0**:

```text
oracle cũ ép 0→8: check=True holder=False admission=False
đối chứng riêng từng đường: True True True
admission gọi discovery rồi bỏ kết quả: False
```

Như vậy, admission trả `8` để chiều oracle eligibility nay bị từ chối; admission giữ `0` cả khi discovery lệch cũng bị từ chối. Không mở lại F1–F7. F1/F4/F5 vẫn là nghĩa vụ successor, đúng lời khai hiện tại.

Các phép đo khác:

- **L5 passed trong phạm vi Git:** SHA-256 r9, A1a r2 và ba bản nháp trước khớp đầy đủ. Các dòng `934/942/944/948/1258`, workflow `47/160`, test `5154`, A1a `145/146/222` đều khớp base.
- `git diff --numstat 0721811^1 0721811`, **rc=0**: **141 + 919 + 1327 = 2387**, đúng **3 tệp**.
- `python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6.py . 0721811 2026-09-27T02:40:00Z`, **rc=0**:

  ```text
  lease_hop_le=89
  cap_hai_chieu=11
  BIA_MO_LICH_SU_theo_b=[]
  vi_pham=[]
  digest=8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48
  ```

- **L2:** M1–M6 mỗi mục chiếu một đường trong write set. M2 khả thi bằng import consumer sau T2. Bước đo profile đã chuyển sang DO-PROFILE; M6 hiện tại là test production.
- Đọc YAML/AST bằng Python, **rc=0**: workflow có **2** bước `run`, **0** lời gọi `hoso_adapter_do`; checkout `${{ github.workflow_sha }}`; quyền job `contents/pull-requests/actions: read`. Không chạy mã ứng viên trong workflow nền.
- **L3/phạm vi:** chưa tìm thấy tiêu chí không thể đỏ hoặc mâu thuẫn mới với r9/A1a r2. Producer canonical → executor đề xuất → chủ kho duyệt digest không phải executor tự duyệt bị ADR-0047 cấm. T1–T4 riêng lẻ chưa đủ; bản nháp đã buộc thêm T5/T6 trước freeze.
- Đọc API ruleset thành công: strict=false, thiếu `thu-hoi`, cho `[merge,squash,rebase]`, bypass rỗng. Comments #656 trả `[]`. Bản chiếu #579 g20 xác nhận hạn đã khai.
- `git diff --check 67802bf 52831cc`: **passed, rc=0**, không output.

**Giới hạn:** 100/89 run và annotation Ubuntu chưa đo độc lập; endpoint lịch sử workflow bị connector từ chối. Full suite/CI/canary: **not_run**. Lần gọi fixture đầu **failed, rc=2** vì thiếu `--nhanh-mac-dinh`; lần sửa lệnh đạt như trên. Model/effort không được chứng thực độc lập. Không sửa repository; HEAD/tree giữ nguyên, chỉ thấy `.codex/` ignored. Approval này dành cho **bản nháp đặc tả**, không xác nhận đủ tiền đề kích hoạt.

VERDICT: APPROVE

<!-- Đính chính 27-09 (bản nháp 14): header log runtime của lượt này ghi `reasoning effort: none`; nhãn effort `high` ở dòng đầu là SAI. -->
