<!-- Verdict codex lượt 3 (gpt-6-astra high, codex_cli tại chỗ) trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 3 @ 1503ca8, base 67802bf. Chép nguyên văn từ tệp -o của codex exec; chỉ bỏ khoảng trắng cuối dòng (hard-break Markdown) theo tiền lệ ops/reviews/thu-hoi-lease-a1a-r2/. -->
Có **1 finding mới P2**. F6/F7 đã được vá ở mức đặc tả: hai phản chứng của lượt 2 nay bị tiêu chí mới từ chối.

```text
assurance: advisory_review
base: 67802bf9a1b9adba6d8b13c63ee46744d74655b5
reviewed_sha: 1503ca8c076c466dbc560c6b6e146d3958b7271e
tree: 7e56dbfdbf01e4a80f3817882ad66e5cb74b6d87
spec_sha256: b7baed1cc9076bb760963013b4accf7215c4e0a7955f3ce90ef483c85ad958b9
```

**F8 — P2: A6 áp oracle eligibility cho cả holder và admission, chưa có phép nghiệm thu đúng cho từng đường.**

Vị trí: [ops/specs/THU-HOI-LEASE-A1b.md:105](/tmp/claude-0/-home-user-tra-luat/6d0cd47b-1999-55e6-9ff7-5c7b553ad293/scratchpad/rv/ops/specs/THU-HOI-LEASE-A1b.md:105), liên quan T6 dòng 50 và M5(a) dòng 93. Lớp: `oracle-khong-khop-hop-dong-production`.

A6 đòi **từng đường production** đổi verdict “như fixture dương M5(a)”, tức cặp thay thế sau mốc, sổ rỗng, `0→8`. Nhưng ba đường không quyết định cùng một việc:

- `check` kiểm eligibility: fixture này cần `0→8`.
- `ai-dang-giu` trả tập holder; còn holder thì mã thoát là `11`. Tập có thể đổi mà rc vẫn `11` — chính lý do F7 cần oracle tập.
- `kiem-thu-hoi-github` kiểm admission của namespace sổ. Cặp thay thế trong lease không tự làm một sổ rỗng vi phạm admission. r9 Q3 còn ghi rõ: **“Validator ứng viên M4 độc lập với cờ.”**

**Bằng chứng chạy:** `python3 -B -`, dùng `runpy.run_path('ops/lease_publish_test.py')`, `_kho_thu`, `lease_mau`, `_goi_main`; dựng biến thể fixture `t135` trong `/tmp`, commit cặp thay thế với lease cũ hết hạn và lease mới giữ `ops/x.md`. Lệnh **rc=0**:

```text
flag False check rc 0 forecast8 True
flag False holder rc 11
NGƯỜI_GIỮ 1: moi-thay-the
flag False admission rc 0
THU_HOI_ADMISSION TAP_THU_HOI_RONG ... sổ S=0 T=0 entry

flag True check rc 0 forecast8 True
flag True holder rc 11
NGƯỜI_GIỮ 1: moi-thay-the
flag True admission rc 0
THU_HOI_ADMISSION TAP_THU_HOI_RONG ... sổ S=0 T=0 entry
```

Phép đọc AST từ `git show 67802bf:ops/lease_publish.py`, **rc=0**:

```text
lenh_ai_dang_giu returns: ['RC_DANG_GIU if nguoi_giu else RC_OK']
lenh_kiem_thu_hoi_github returns: ['RC_OK']
source identical at head: True
```

Đây là phép đo hợp đồng nền và fixture, **không phải** bằng chứng WIRING tương lai đã chạy. Nó chỉ ra rằng A6 chưa phân biệt một kết quả đúng với mutant bỏ discovery trên từng đường. Làm admission trả `8` chỉ để đạt fixture eligibility sẽ mở rộng hành vi ngoài hợp đồng M4.

**Cách vá:** sửa A6/T6 thành ma trận oracle riêng: `check` dùng `0→8`; holder dùng tập ID/path cùng rc tương ứng; admission dùng đối chứng sổ hợp lệ và dữ liệu discovery không khớp phải bị từ chối. Mỗi đường vẫn phải giết riêng mutant “gọi discovery rồi bỏ kết quả”. Giữ ca dương admission sổ rỗng để tránh biến yêu cầu kiểm wiring thành thay đổi semantics; seam thiếu thì trả về packet WIRING.

**Đối chiếu F6/F7 — không mở lại finding cũ.**

Đã chạy phép áp điều kiện mới lên hai phản chứng cũ, **rc=0**:

```text
F6 old call-discard (0,0): new M5(a) accepts= False
F7 rc 11->11: removed= [('x', 'ops/x.md')]
new M5(c) accepts_without_Q6_source= False
```

M5(a)/A5 nay bắt buộc kết quả dương, M5(c) bắt mất holder dù rc không đổi; T6 đã yêu cầu SHA, entry point và seam trước freeze. **Đã vá trong đặc tả**; chưa chứng nhận implementation. F8 là vấn đề mới do mở rộng oracle sang mọi đường tại A6.

Các phép đo khác:

- **L5 passed:** băm đầy đủ của r9, A1a r2 và hai bản nháp trước đều khớp. Các dòng `934/942/944/948/1258`, workflow `47/160`, test `5154`, A1a `145/146/222` đều đúng tại base.
- `git diff --numstat 0721811^1 0721811`, **rc=0**: từng số hạng là **141, 919, 1327**; tổng **2387**, **3 tệp**.
- `python3 -B ops/reviews/thu-hoi-lease-a1a-r2/do_q6.py . 0721811 2026-09-27T02:40:00Z`, **rc=0**: **89** lease hợp lệ, **11** cặp, **0** cặp giữ lại; digest `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48`.
- Workflow có **2** bước `run`, **0** lời gọi `hoso_adapter_do`; checkout tại `workflow_sha`. Quyền job khai `contents/pull-requests/actions: read`. Bước đo profile thuộc tiền đề DO-PROFILE; A1b không còn sửa workflow.
- M1–M6 đều chiếu một đường trong write set. M2 khả thi bằng import consumer thật sau T2. Producer canonical → executor đề xuất → chủ kho duyệt digest không phải tự duyệt bị ADR-0047 cấm.
- T1–T4 chưa đủ để freeze; bản nháp đã bổ sung T5/T6 và giữ trạng thái chưa đóng băng đúng. F1/F4/F5 vẫn là nghĩa vụ successor, chưa được tính đã đóng bằng mã.

Đã đọc trực tiếp `GET /repos/ducthangho/tra-luat/rulesets/20856202`: thành công, `strict_required_status_checks_policy=false`, vẫn cho `[merge,squash,rebase]`, thiếu `thu-hoi`, `bypass_actors=[]`. Vì vậy strict nay **đo được là false**. API comments #656 trả `[]`; comment #579 `5850956654` xác nhận projection g20 có hạn `2026-09-29T00:00:00Z` và hai đường đang xét.

**Giới hạn:** 100/89 run và annotation Ubuntu chưa đo độc lập; truy vấn lịch sử workflow bị connector từ chối. Full suite/CI/canary: **not_run**. `git diff --check` **failed, rc=2** tại hai dòng Markdown hard-break trong verdict lượt 2 được chép nguyên văn. Không sửa repository; HEAD/tree giữ nguyên, trạng thái quan sát có `.codex/` ignored. Phép đo dùng shell/Python cục bộ, transport `machine`; model/effort không được chứng thực độc lập.

VERDICT: REQUEST_CHANGES

<!-- Đính chính 27-09 (bản nháp 14): header log runtime của lượt này ghi `reasoning effort: none`; nhãn effort `high` ở dòng đầu là SAI. -->
