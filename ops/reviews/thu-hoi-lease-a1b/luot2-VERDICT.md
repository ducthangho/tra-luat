<!-- Verdict codex lượt 2 (gpt-6-astra high, codex_cli tại chỗ) trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 2 @ 673256e, base 67802bf. Chép nguyên văn từ tệp -o của codex exec; chỉ bỏ khoảng trắng cuối dòng (hard-break Markdown) theo tiền lệ ops/reviews/thu-hoi-lease-a1a-r2/. -->
Review `advisory_review`, không sửa tệp:

```text
base: 67802bf9a1b9adba6d8b13c63ee46744d74655b5
head: 673256e028bf44847bd9c6d79432faf6ea242675
tree: 5341fafe72e3cb58b03cbddea94d7003d229b8cd
spec_sha256: 0a1f7213c8f78456c4fdac24c0a0bcc4713e17da15a0204e286f9c2147dbb510
```

Phép đo chạy bằng shell/Python cục bộ, transport `machine`; không có bằng chứng runtime độc lập để chứng nhận model/effort hoặc connector như spec khai.

**1. P1 — F2 chưa đóng: A5 vẫn xanh khi luật mới không có tác dụng.**
`ops/specs/THU-HOI-LEASE-A1b.md:50`, `:93–105`. Lớp: `bat-co-chua-noi-verdict-production`.

“Delta chỉ gồm `0→8`” không bắt buộc **có** chuyển đổi `0→8` trên fixture cần chuyển đổi. Tập delta rỗng vẫn đạt. T6/M6 thêm điều kiện gọi discovery nhưng chưa đòi kết quả discovery được dùng để quyết verdict.

**Bằng chứng đã chạy:** `python3 -B -`, dùng `_kho_thu`, `lease_mau`, `_goi_main` của suite để dựng lại fixture `t135` trong `/tmp`: cặp thay thế ngoài danh sách lịch sử, sổ rỗng. Lệnh **rc=0**:

```text
flag False rc 0 forecast8 True
flag True rc 0 forecast8 True
A5_allowed_delta_only= True deltas= []
```

Chạy thêm mô hình phản chứng **trong bộ nhớ**: khi bật cờ, gọi discovery rồi bỏ kết quả và tiếp tục `lenh_check` cũ; discovery giả có chốt neo. **rc=0**:

```text
illustrative_T6_call_and_discard anchor True calls 1 rc 0
illustrative_T6_call_and_discard anchor False calls 1 rc 12
```

Đây là mô hình chứng minh điều kiện nghiệm thu còn thiếu, **không phải mã WIRING đã tồn tại**. Nó thỏa điều kiện gọi discovery/neo rỗng, nhưng không áp luật mới.

**Vá:** tại T6 và A5–A6, bắt buộc fixture dương có kết quả chính xác `False→True = 0→8`; mutant “gọi discovery rồi bỏ kết quả” phải làm ca ấy đỏ. Trước freeze, neo SHA/entry point WIRING và cách tiêm map, clock, nguồn nội bộ; phân biệt các đường production cần nghiệm thu. Không chỉ ghi “entry point production”.

**Khóa và rủi ro:** chạy qua verdict thật, không chép validator vào test. Nếu cần sửa seam hoặc hành vi WIRING, trả về packet WIRING; không âm thầm đưa phần đó vào M5/M6 của A1b.

**2. P2 — M5/A5 gọi là phân loại delta Q6 nhưng bỏ mất delta holder.**
`ops/specs/THU-HOI-LEASE-A1b.md:38`, `:93`, `:104`. Lớp: `loi-khai-delta-rong-hon-phep-do`.

Q6 của r9 yêu cầu đo **holder và eligibility, từng ID/path cùng nguyên nhân**. Bản nháp chỉ quy định chuyển mã thoát. Mất một holder vẫn có thể giữ nguyên `rc=11` vì holder khác còn tồn tại; phép đo A5 không phát hiện việc thu hẹp quyền giữ.

**Bằng chứng nguồn:**

```bash
sed -n '381,388p' ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md
sed -n '1934,1969p' ops/lease_publish.py
```

Cả hai **rc=0**: Q6 đòi `holder + eligibility`; `lenh_ai_dang_giu` trả `RC_DANG_GIU` khi tập holder còn bất kỳ phần tử nào. Phản chứng phép chiếu chạy bằng `python3 -B -`, **rc=0**:

```text
holder_rc_projection [(['x', 'y'], 11), (['y'], 11)]
```

Tức `{x,y}→{y}` mở lại quyền đối với `x`, nhưng delta mã thoát là rỗng.

**Vá:** bổ sung oracle tập holder theo ID/path trên cùng map/clock, cùng phân loại nguyên nhân; giữ chính sách `0→8` cho phần eligibility nếu đó là quyết định Q15. Nếu Q15 cố ý thay Q6 rộng hơn, phải ghi rõ quyết định thay thế, không gọi phép đo hiện tại là đủ Q6.

**Khóa và rủi ro:** mutant bỏ một holder trong tập có ít nhất hai holder phải đỏ dù cả hai lượt đều trả `11`. Ca này chỉ cần sửa test nếu WIRING đã cung cấp quan sát cần thiết; việc thực hiện xóa holder thuộc A1c vẫn ngoài phạm vi.

Đối chiếu lượt 1:

| Finding | Kết quả lượt 2 |
|---|---|
| F1 — producer profile chưa canonical | Đã sửa vòng phụ thuộc **trong thiết kế** bằng Q13/T5; việc thực thi chuyển sang DO-PROFILE, chưa đo được. |
| F2 — chưa nối production; delta sai | **Vá một phần**. Tách WIRING hợp lý, nhưng còn hai finding trên. |
| F3 — schema A0 thay vì v2 | **Đã vá thật ở đặc tả**: §2 khớp A1a r2 M1/M2/A2. |
| F4 — consumer/C≠S | Đã bổ sung hợp đồng tiền đề và import consumer thật. Chưa chứng minh bằng mã/canary; cần điền neo và giao diện trước freeze. |
| F5 — runner/bước workflow/test | Đã chuyển trách nhiệm sang DO-PROFILE, gồm cả test “hai bước run”; chưa có bằng chứng successor đóng finding. |

Vì vậy câu “bản nháp 2 đóng F1–F5” tại dòng 11 rộng hơn bằng chứng. Theo protocol §8.3, chuyển biểu hiện sang successor không tự được tính là **ĐÃ VÁ THẬT**.

Các phép đo L5 **passed**:

- SHA-256 r9, A1a r2 và bản nháp 1 đều khớp nguyên giá trị khai.
- Các dòng `934/942/944/948/1258`, workflow `47/160`, test `5154`, A1a `145/146/222` đều khớp.
- Workflow có **2** bước `run`, không gọi `hoso_adapter_do`; checkout tại `workflow_sha`; token khai `contents/pull-requests/actions: read`.
- `git diff --numstat 0721811^1 0721811`, **rc=0**: `141 + 919 + 1327 = 2387` dòng thêm, **3 tệp**.
- Chạy:

  ```bash
  python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6.py \
    . 0721811 2026-09-27T02:40:00Z
  ```

  **rc=0**: **89** lease hợp lệ, **11** cặp, **0** cặp giữ lại; digest `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48`.

Không tìm thấy số Git tĩnh sai trong §1/§2. **100/89 run, annotation Ubuntu, hạn #579 g20, ruleset và authority GitHub: not_measured độc lập**, không coi là passed. Full suite/CI/canary: **not_run** cho review chỉ đặc tả này.

M1–M6 đều chiếu đúng một đường về mặt bảng. M2 có thể nằm hoàn toàn trong tệp test nhờ import consumer; M5/M6 cũng khả thi theo cách đó **sau khi hợp đồng WIRING được khóa**, chưa thể chứng nhận từ T6 hiện tại. Executor đo rồi đề xuất digest, producer canonical và chủ kho duyệt độc lập không phải “tự khai” bị ADR-0047 cấm.

VERDICT: REQUEST_CHANGES

<!-- Đính chính 27-09 (bản nháp 14): header log runtime của lượt này ghi `reasoning effort: none`; nhãn effort `high` ở dòng đầu là SAI. -->
