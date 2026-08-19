# Kết luận lượt 2 — verdict `blocked`, nhưng khác hẳn lượt 1 về nội dung

**Chặn quyền chạy VẪN CÒN HIỆU LỰC — lời khai "ĐÃ GỠ chặn" của prompt không khớp thực tế đo được.** Tuy nhiên lượt này sandbox tha các lệnh git read-only, nên tôi đã review TĨNH trọn vẹn diff + toàn bộ hai tệp, xác minh tĩnh cả 5 bản vá lượt 1, và tìm ra **6 finding mới** (3 P2, 3 P3) bằng suy vết tĩnh có địa chỉ dòng chính xác. Mọi phép đo ĐỘNG (suite, đột biến, lách CLI) vẫn `KHÔNG ĐO ĐƯỢC` — theo đúng chỉ dẫn của packet, tôi trả `blocked` chứ không suy "pass" từ đọc tĩnh.

## Chẩn đoán vì sao gỡ chặn thất bại (để lượt 3 không lặp lại)

- `python3 .claude/dev/packet_loop_test.py` (đúng nguyên văn phép thử bắt buộc, lệnh đơn) → bị từ chối bởi "don't ask mode". Thử 2 lần, 2 dạng.
- Kể cả `python -m py_compile` và `python -m ruff check` — hai mục CÓ trong allowlist `.claude/settings.json` của repo — cũng bị từ chối ⇒ policy hiệu lực là của **harness phiên**, không phải settings repo; settings repo không được nạp hoặc bị đè.
- Thứ chạy được: `git status/log/diff/show/grep` (sandbox tha lệnh read-only) và Read/Grep trong project. Không tồn tại đường hợp lệ nào thực thi Python; tôi không lách (Agent/Workflow kế thừa cùng permission; luồn thực thi qua cờ git là bypass đúng nghĩa).
- Sửa cho lượt 3: cấp phiên reviewer với allow rule tường minh `Bash(python3:*)` (mutant phải chạy bản sao trong /tmp nên allow đúng một đường dẫn là không đủ), hoặc mode có người duyệt prompt.

## Những gì ĐÃ đo được (dương tính, tự tay chạy)

- HEAD = `7dc8a2f7121d505cb35ffb517842468f547bb455` = reviewed_sha; lịch sử đúng base `5f6eb929` + 2 commit.
- Write set: diff gộp **và** stat từng commit (`14495ece`, `7dc8a2f7`) đều chỉ chạm đúng 2 tệp được phép — loại cả kịch bản "commit 1 sửa file cấm, commit 2 hoàn tác" mà diff gộp che.
- Cây sạch đầu phiên và cuối phiên (`git status --short` rỗng cả hai lần).
- `scripts/tl.py` không tham chiếu packet_loop ⇒ selftest tl (lệnh duy nhất dạng test được phép) không đo được gate này.

## Phần A — 5 finding lượt 1: xác minh TĨNH 5/5, ĐỘNG 0/5

Cả 5 đều có đủ bộ ba {code sửa + case mới + mutant mới} trong diff, và tôi suy vết tay từng mutant giết đúng ca đích: (1) bộ đếm vòng dời lên TRƯỚC nhánh `_die` same-failure (`packet_loop.py:997`); (2) vòng fail-closed gồm cả `review_calls`, chết bằng `_die` rc=8 không traceback (`:1057`); (3) `void-attempt` chặn 3 state cuối (`:880`); (4)+(5) mutant `bo_vong_fail_closed_state_cu`, `bo_chot_nhan_CHIEU_HAI` có mặt và theo suy vết đều giết ca đích. Nhưng "vá THẬT" theo chuẩn packet đòi chạy — chưa chạy được, nên chỉ ghi nhận tĩnh.

## Phần B — 6 finding mới (chi tiết trong khối verdict)

Đáng chú ý nhất: **`record-review` không hề đọc ngân sách review-call** — mọi bộ đếm cũ đều được DỆT vào đường bắt buộc của máy trạng thái (không `begin-attempt` thì không có đường tới `accepted`), riêng `record-review-call` là lệnh TỰ NGUYỆN: bỏ qua nó là 3 vòng review khép trọn với `codex_review_calls_used = 0`. Kế đến: needle của mutant `bo_chan_void_o_state_cuoi` xuất hiện ở **hai** dòng (880, 1065) mà runner `replace(…, 1)` chỉ đổi lần đầu — cửa state-cuối của chính `record-review-call` không có ca lẫn mutant nào; `codex_executor_calls_used` (trường outcome của spec) **không được test nào đọc** và trong suite không bao giờ nhích khỏi 0 (fixture executor luôn là claude); ledger `review_calls` chỉ được đo SỰ TỒN TẠI khoá, không đo việc ghi.

```yaml
reviewed_sha: 7dc8a2f7121d505cb35ffb517842468f547bb455
verdict: blocked
spec_axis: fail
standards_security_axis: fail
gates:
  - packet_loop_test: rc=KHÔNG ĐO ĐƯỢC — mọi lời gọi python bị permission mode từ chối (thử 4 dạng, kể cả 2 mục thuộc allowlist repo); không có dòng số liệu nào được in
  - dot_bien_tu_nghi: 0/5 bị bắt THEO SUY VẾT TĨNH trên 5 đột biến mới tự thiết kế (dự đoán cả 5 SỐNG SÓT ⇒ F2/F3/F4); CHƯA CHẠY nên không tính là đo
  - va_luot_1: 5/5 xác minh TĨNH (code + case + mutant khớp diff, suy vết giết đúng ca) · 0/5 xác minh ĐỘNG
  - write_set: 2 tệp đổi / ngoài write set: 0 (đo diff gộp VÀ stat từng commit)
  - cay_sach_dau_cuoi: có (rỗng cả hai lần đo)
findings:
  - id: record-review-khong-doc-so-loi-goi
    severity: P2
    locator: .claude/dev/packet_loop.py:919
    evidence: >
      TĨNH (mọi đường chạy python bị chặn). cmd_record_review (919–1028) không tham chiếu
      codex_review_calls_used/review_calls ở dòng nào. Đường "không gõ record-review-call":
      begin-attempt (809) → transition reviewing (1145) → record-review (921) — không chốt nào
      đọc ngân sách review ⇒ 3 vòng review khép được (tới trần attempt) với used=0. Mọi bộ đếm
      khác được dệt vào đường bắt buộc (accepted không thể ghi nếu thiếu begin-attempt);
      riêng lệnh mới là tự nguyện — trần 2 lời gọi lách được bằng THIẾU SÓT im lặng,
      không cần khai gian. Phản chứng chạy được khi có quyền: init → 2×(begin-attempt;
      record-post; transition reviewing; record-review changes_requested) không một
      record-review-call nào → status phải cho used=0, rounds=2, rc=0 toàn chuỗi.
    required_repair: >
      Dệt sổ lời gọi vào đường bắt buộc: record-review đòi ≥1 mục tieu trong review_calls
      CHƯA gắn vòng (đánh dấu round vào mục khi tiêu thụ), fail-closed khi state thiếu khoá
      ngân sách (đồng bộ với 1057); kèm case + mutant riêng.
  - id: cua-state-cuoi-record-review-call-khong-phan-chung-mutant-neo-lech
    severity: P2
    locator: .claude/dev/packet_loop.py:1065
    evidence: >
      ĐO ĐƯỢC: git grep cho đúng 2 dòng 880 và 1065 trùng nguyên văn needle của mutant
      bo_chan_void_o_state_cuoi; runner thay bằng replace(t, th, 1) (packet_loop_test.py:2672)
      nên mutant chỉ vô hiệu được cửa VOID (880). TĨNH: không case nào gọi record-review-call
      trên packet đã ở state cuối (4 chỗ dùng lệnh: 838/840 ở leased, helper 1850 — không ca
      nào gọi sau checkpoint); đột biến vô hiệu riêng dòng 1065 dự đoán SỐNG SÓT: nhánh tieu
      còn 1099 đỡ (rc=3 thay 8, không ca nào phân biệt), nhánh KHÔNG-tieu ghi sổ + rc=0 trên
      state cuối — đúng lớp lượt 1 vừa vá cho void-attempt, và vi phạm doctrine
      "cửa không có mutant là cửa sẽ âm thầm hở lại".
    required_repair: >
      Case mới: sau checkpoint (và blocked/accepted) gọi record-review-call cả hai nhánh,
      đòi rc=8 + sổ không đổi; mutant mới neo needle dài hơn (kèm dòng ngữ cảnh chỉ có trong
      cmd_record_review_call) để không dính dòng 880.
  - id: codex-executor-calls-khong-ca-nao-do
    severity: P2
    locator: .claude/dev/packet_loop.py:856
    evidence: >
      ĐO ĐƯỢC: git grep codex_executor_calls_used trên test file = 0 kết quả (chỉ có trong
      packet_loop.py:635,857). TĨNH: tăng chỉ khi provider=="codex" mà toàn suite dùng
      EXECUTOR="claude" (test:32) ⇒ bộ đếm không bao giờ nhích khỏi 0 trong suite và không ca
      nào đọc nó — trường OUTCOME của spec đang XANH RỖNG; đột biến xoá 856–857 dự đoán
      sống sót toàn suite.
    required_repair: >
      Thêm ca executor=codex/reviewer=claude: begin-attempt 2 lần (qua void hoặc vòng review),
      đòi codex_executor_calls_used==2 và ngân sách review không đổi; kèm mutant vô hiệu
      phép tăng.
  - id: review-calls-ledger-va-chot-phu-khong-rang
    severity: P3
    locator: .claude/dev/packet_loop.py:1088
    evidence: >
      ĐO ĐƯỢC: trong test file, chuỗi review_calls chỉ xuất hiện ở phép đọc bộ đếm, hai ca
      pop-khoá (đo SỰ TỒN TẠI) và needle mutant — không ca nào đọc NỘI DUNG/độ dài ledger.
      TĨNH: 3 đột biến dự đoán sống sót: bỏ append nhánh tieu (1114), bỏ append nhánh
      không-tieu (1088), vô hiệu chốt provider (1044 — không ca nào gọi record-review-call
      sai provider; ca cũ review_sai_provider_thoat_4 chỉ đo record-review); thêm chốt
      output-bytes âm (1068) cũng không có ca. Trace thô là ĐÍCH của finding lượt 1 nhưng
      bản vá mới chỉ bảo đảm khoá tồn tại, chưa bảo đảm trace được ghi.
    required_repair: >
      Ca đọc review_calls sau chuỗi gọi (đúng số mục, đúng cờ tieu từng mục); ca sai provider
      rc=4; ca output-bytes âm rc=2; mỗi chốt một mutant.
  - id: record-post-van-ghi-so-o-state-cuoi
    severity: P3
    locator: .claude/dev/packet_loop.py:1173
    evidence: >
      TĨNH: cmd_record_post không có guard state — trên packet checkpoint/blocked/accepted
      vẫn ghi posts với rc=0 (hàm chỉ kiểm dạng ID + trùng). Không thoát được state cuối
      (transition từ checkpoint bị CHUYEN_HOP_LE chặn) nên là bất nhất SỔ SÁCH — đúng chuẩn
      lượt 1 áp cho void-attempt. Tồn tại trước packet với accepted/blocked, nhưng checkpoint
      do W0-R1 sinh ra nên W0-R1 nợ guard cho cửa của mình.
    required_repair: >
      Guard state cuối ở record-post (rc=8) + case + mutant; hoặc khai tường minh trong
      docstring vì sao cửa này được phép ghi.
  - id: nhan-ket-cuc-thieu-va-bat-bien-ok-0-khong-cuong-che
    severity: P3
    locator: .claude/dev/packet_loop.py:53
    evidence: >
      TĨNH: (a) không có nhãn cho "chết SAU khi tới model, TRƯỚC byte đầu" — khai
      timeout-sau-sinh với 0 byte bị 1079 chặn, người vận hành bị ép khai rate-limit/preflight
      cho lời gọi ĐÃ đốt input token ⇒ lớp lời gọi đó retry tự do không đếm (không rửa được
      verdict vì 0 byte = 0 giá trị review, nhưng chi phí thật không vào sổ); (b) bất biến
      trong chú thích dòng 60 ("đã sinh ra thì output PHẢI khác 0") KHÔNG cưỡng chế cho ok:
      `--outcome ok --output-bytes 0` đi qua và tiêu call — mâu thuẫn tự thân được nhận;
      (c) --output-bytes là số TỰ KHAI không neo bằng chứng, mà chú thích gọi nó là "SỐ ĐO"
      không kèm câu khai giới hạn kiểu dòng 89–94.
    required_repair: >
      Thêm nhãn timeout-truoc-sinh vào KET_CUC_KHONG_TIEU (bắt buộc 0 byte); mở rộng 1079
      bao cả ok; thêm câu NÓI THẲNG GIỚI HẠN cho output-bytes (tuỳ chọn: --raw-log đối chiếu
      kích thước).
khong_do_duoc:
  - "packet_loop_test.py: rc + dòng số liệu — mọi lời gọi python bị permission mode từ chối (python3 <suite> ×2, python -m py_compile, python -m ruff check; hai lệnh sau thuộc allowlist repo vẫn bị chặn ⇒ policy harness đè settings repo)"
  - "đột biến tự nghĩ: 5 cái đã thiết kế kèm suy vết, 0 cái chạy được — cần quyền chạy python trên bản sao trong /tmp"
  - "lách trực tiếp bằng CLI trong /tmp: không chạy được lệnh nào của packet_loop.py"
  - "xác minh ĐỘNG 5 bản vá lượt 1 và baseline suite (kể cả kiểm 'mutant có THẬT giết ca đích')"
```
