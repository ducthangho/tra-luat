# Kết quả review lượt 3 — W0-R1

**Trục động đã được đo trọn lần đầu: suite `198/198 đạt` rc=0, cả 4 acceptance PASS bằng CLI thật, cả 8 mục vá hai lượt trước xác minh động là vá thật, lời khai "trần tự nguyện" của Executor đo lại là CHÍNH XÁC. Nhưng 7/7 đột biến mới tôi tự nghĩ đều SỐNG SÓT toàn suite (chỉ đối chứng cố ý bị bắt) — trong đó có ba cửa enforcement mới của chính packet này chưa có lấy một phản chứng. Verdict: `changes_requested`.**

## Phần A — đo động

**Suite (lần đo đầu tiên của trục này):** `python3 .claude/dev/packet_loop_test.py` → **rc=0**, `nền: 198/198 đạt`, 43/43 đột biến giết đúng ca đích + đối chứng khác họ sống, `SỐ LIỆU: ca 198 · đột biến 43 · lớp lách 78 · ca bắt-oan 35 · ngoại lệ AC 18: 0 · TỔNG: ĐẠT`. Không FAIL/BỎ QUA/Traceback ẩn trong output.

**Acceptance — 4/4 bằng CLI thật trong `/tmp` (state dựng bằng `init` + lease hợp lệ):**
- Đã sinh rồi hỏng VẪN tiêu: `sai-schema` 400B rc=0 used=1, `timeout-sau-sinh` 90B rc=0 used=2.
- Hỏng trước khi sinh KHÔNG tiêu: `preflight`/`permission`/`rate-limit` 0B đều rc=0, used=0; call thật sau đó used=1.
- Call thứ ba: rc=3, state=`checkpoint`, history có `checkpoint_review_calls_exhausted`.
- Đổi prompt/phiên không reset: 2×`sai-schema` rồi một lời gọi khác hẳn (tiến trình mới) → rc=3, used vẫn 2.
- Độc lập ngân sách hai chiều: 2 call review xong `attempts_used` vẫn 0, `begin-attempt` vẫn mở được; `void-attempt` không hoàn call (used giữ 2). Nhãn-phải-khớp-số-đo chặn cả hai chiều (rc=2).

## Phần B — 8/8 xác minh động

1. Vòng chạm trần same-failure ĐƯỢC đếm: `len(reviews)=2 == review_rounds_used=2` khi lượt 2 rc=3 → blocked.
2. State thiếu `codex_review_calls_used/limit` → rc=8, không traceback.
3. State thiếu `review_calls` → rc=8, không KeyError.
4. `void-attempt` bị chặn rc=8 ở CẢ BA state cuối (checkpoint/blocked/accepted — đo từng cái).
5. `record-review-call` bị chặn rc=8 ở cả ba state cuối, CẢ HAI nhánh tiêu/không-tiêu; sổ không phình thêm.
6. `codex_executor_calls_used` đếm LỜI GỌI thật: begin→void→begin với executor codex ra 2 trong khi `attempts_used`=1.
7. Chốt "mỏ neo khớp ĐÚNG MỘT chỗ" **có răng thật**: needle ngắn `if st["state"] in (…)` hôm nay đúng là trùng 2 chỗ; bơm nó vào runner THẬT → `ĐỎ … mỏ neo MƠ HỒ`, main() rc=1.
8. Lỗ Executor KHAI CHƯA VÁ — đo lại đúng, không nhỏ hơn cũng không lớn hơn về bản chất: 3 vòng khép trọn với used=0/2 (S10a); sắc hơn: ledger thật thà tới 2/2 vẫn không tự chặn vòng 3 nếu bỏ ghi call 3 (S10b); chỉ người TỰ GHI mới bị trần cắn (S10c: call 3 rc=3 → checkpoint → record-review rc=8). Điểm cưỡng chế duy nhất nằm trong `record-review-call`. Các đường lách "cùng họ" tôi tìm thêm được nằm ở phần đột biến dưới — chúng là cửa canh cái trần ấy chứ không phải đường tiêu-mà-không-đếm mới.

## Phần A.3 + C — 7 đột biến mới, **7 SỐNG SÓT toàn suite** (đối chứng G bị bắt bởi 3 ca — chứng minh harness của tôi biết đỏ; chạy đủ 198 ca/lượt, bản sao trong `/tmp` nhưng import test module tại chỗ nên không dính ca đỏ giả nào)

Mỗi survivor đều kèm kịch bản khai thác CHẠY ĐƯỢC trên chính bản mutant:
- **A** gỡ cửa provider của `record-review-call` → executor `claude` ghi call rc=0, used nhích. Không ca nào đổi provider lệnh này.
- **B** init nuốt cờ `--review-calls-limit` (kẹp cứng 2; canonical trả 5 đúng) → suite xanh. Cờ chưa từng được ca nào truyền.
- **C** `CHUYEN_HOP_LE["checkpoint"] = ("running",)` → chuỗi khép trọn: checkpoint → running → reviewing → `record-review` rc=0, **rounds=3 khi used=2/2** — mở lại đúng vòng review vừa bị trần chặn, suite vẫn xanh.
- **D** nới cửa `reviewing` của `record-review` nhận thêm checkpoint → `approve` NGAY TẠI checkpoint rc=0, state=**accepted**. Đo thêm mutant **H** (gỡ hẳn cửa ấy) sống cả trên suite của **base** (185 ca, 0 đỏ) ⇒ món nợ có sẵn, delta=0 cho cửa nói chung — nhưng góc checkpoint là MỚI của packet này, và ma trận state-cuối của chính packet phủ `void` + `record-review-call` mà bỏ sót cửa thứ ba.
- **E** gỡ chặn `--output-bytes` âm → `sai-schema(-400)` rc=0, số âm vào sổ.
- **F** nhánh không-tiêu khai gian `"tieu": True` vào ledger (used vẫn 0) → không ai đọc trường ấy, suite xanh.

Quan sát thêm (không thành finding): `record-review-call` không đòi lease — packet chưa từng có lease vẫn tiêu được budget tới checkpoint (chiều tự hại, không mở khoá gì); `ok` với 0 byte thì thành finding P3 bên dưới vì chú thích hằng số hứa chiều đó mà code cố ý miễn.

Write set: đúng 2 tệp được phép, 0 tệp ngoài. Cây sạch đầu và cuối phiên.

```yaml
reviewed_sha: 6192c0571031d3d724c2bb7cdd7449278d0334c0
verdict: changes_requested
spec_axis: pass
standards_security_axis: fail
gates:
  - packet_loop_test: rc=0 "nền: 198/198 đạt · ca 198 · đột biến 43 · lớp lách 78 · ca bắt-oan 35 · ngoại lệ AC 18: 0 · TỔNG: ĐẠT"
  - dot_bien_tu_nghi: 1/8 bị bắt (1 là ĐỐI CHỨNG cố ý; 7 đột biến thật A,B,C,D,E,F,H đều SỐNG SÓT 198/198 — H sống cả trên base, delta=0)
  - acceptance_do_bang_CLI: 4/4 xác minh động
  - va_luot_truoc: 8/8 xác minh ĐỘNG đã vá thật (mục 8 là lời khai chưa-vá, đo lại CHÍNH XÁC)
  - write_set: 2 / ngoài write set: 0
  - cay_sach_dau_cuoi: có
findings:
  - id: record-review-call-cua-provider-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:1063
    evidence: "mutant gỡ khối provider (harness /tmp/rev3-mut, needle 5 dòng kèm thông điệp): chay_suite 198 ca → 0 đỏ; trên mutant: record-review-call --provider claude rc=0, used=1 (canonical đo được rc=4)"
    required_repair: thêm ca đòi rc=4 khi provider != reviewer của record-review-call + đột biến gỡ cửa (needle kèm dòng thông điệp, tránh mơ hồ với cửa cùng dạng ở record-review) phải giết đúng ca đó
  - id: checkpoint-loi-ra-transition-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:153
    evidence: "mutant đổi checkpoint:() thành (running,): 198 ca → 0 đỏ; chuỗi khai thác chạy được: 2 call + 2 vòng + call 3 rc=3 → checkpoint; record-post --for running; transition --to running rc=0; vào lại reviewing; record-review rc=0 ⇒ rounds=3 khi used=2/2"
    required_repair: ca phản chứng thoát-checkpoint (record-post rồi transition --to running từ checkpoint, đòi rc=8 và state vẫn checkpoint) + đột biến nới CHUYEN_HOP_LE["checkpoint"] phải giết ca đó
  - id: record-review-khong-co-ca-state-cuoi
    severity: P2
    locator: .claude/dev/packet_loop.py:921
    evidence: "mutant nới cửa reviewing nhận thêm checkpoint: 198 ca → 0 đỏ; trên mutant: approve TẠI checkpoint (attempt_open=True, head còn neo) rc=0, state=accepted; mutant gỡ HẲN cửa cũng sống — kể cả trên suite base 5f6eb929 (185 ca, 0 đỏ)"
    required_repair: thêm ca record-review tại checkpoint (đường thật thà tới checkpoint) đòi rc=8, + đột biến cửa reviewing phải giết; vá ở đây khoá luôn món nợ base cho blocked/accepted
  - id: co-review-calls-limit-khong-ai-do
    severity: P3
    locator: .claude/dev/packet_loop.py:632
    evidence: "mutant thay a.review_calls_limit bằng 2: 198 ca → 0 đỏ; init --review-calls-limit 5 → mutant limit=2, canonical limit=5; grep test: cờ chưa từng được ca nào truyền"
    required_repair: một ca init với limit khác mặc định (vd 1) và đo trần cắn đúng số đó; đột biến nuốt cờ phải chết
  - id: chan-output-bytes-am-khong-phan-chung
    severity: P3
    locator: .claude/dev/packet_loop.py:1084
    evidence: "mutant gỡ 2 dòng chặn số âm: 198 ca → 0 đỏ; trên mutant: sai-schema --output-bytes -400 rc=0, used=1, ledger ghi -400 (canonical rc=2)"
    required_repair: ca đòi rc=2 cho output-bytes âm + đột biến gỡ chốt phải chết
  - id: truong-tieu-trong-ledger-khong-ai-doc
    severity: P3
    locator: .claude/dev/packet_loop.py:1105
    evidence: "mutant đổi tieu:False→True ở nhánh không-tiêu: 198 ca → 0 đỏ; trên mutant: rate-limit(0B) → review_calls[0].tieu=True trong khi used=0 — sổ cái tự mâu thuẫn với bộ đếm mà suite xanh"
    required_repair: ca đọc ledger sau mỗi nhánh (không-tiêu ⇒ tieu=False, tiêu ⇒ tieu=True) + đột biến khai gian phải chết
  - id: ok-khong-byte-trai-chu-thich-nhan-phai-khop-so-do
    severity: P3
    locator: .claude/dev/packet_loop.py:1095
    evidence: "đo canonical: record-review-call --outcome ok --output-bytes 0 → rc=0 và TIÊU (used=1), trong khi chú thích tại KET_CUC_TIEU (dòng 48-51) hứa 'đã sinh ra thì output PHẢI khác 0'; code cố ý miễn 'ok' khỏi chiều đó"
    required_repair: chọn một — chặn ok+0 byte (rc=2) đúng câu chú thích, hoặc sửa chú thích khai thẳng ngoại lệ 'ok' và lý do; kèm ca ghim chiều đã chọn
khong_do_duoc: []
```
