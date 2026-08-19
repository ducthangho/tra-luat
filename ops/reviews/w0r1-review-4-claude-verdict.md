Cây sạch cả đầu lẫn cuối phiên (mọi bản sao đột biến đều nằm trong scratchpad ngoài cây kho; HEAD giữ nguyên `c9042bfe`). Tổng hợp kết quả review lượt 4:

---

## Kết luận: `changes_requested`

**7/7 bản vá lượt 3 là THẬT** và suite xanh trọn — nhưng áp đúng cái thước mà lượt 3 đã dùng ("cửa cưỡng chế không có phản chứng = finding") lên phần còn lại của tệp thì **12/13 đột biến mới tôi tự nghĩ SỐNG SÓT trọn 205 ca**, trong đó có **hai cửa thoát khỏi `checkpoint` chưa ai canh** — đúng cái state mà packet này dựng lên để làm ngõ cụt.

### A. Xác minh 7 bản vá — 7/7 THẬT
Tôi tự áp từng đột biến lên bản sao (kiểm mỏ neo khớp đúng 1 chỗ), chạy ca đích qua chính `chay_suite` của module test canonical trong worktree. Cả 7 ca đích đều CHẾT khi cửa bị gỡ. Riêng ca được đề bài yêu cầu soi — `record_review_bi_chan_o_state_cuoi` — bản sửa đo **đúng cửa nó khai**, chứng minh hai chiều:
- Canonical: rc=8 với thông điệp đúng cửa state (`chỉ ghi review khi state là 'reviewing' (đang là 'checkpoint')`), trong khi `attempt_open=True`, `attempts_used=1`, sha khớp — không chốt nào khác có thể phát rc=8 đó.
- Mutant (gỡ cửa state): `approve` đi lọt hẳn với **rc=0** → tức không còn chốt nào phía sau đỡ hộ; lỗi "chết nhờ chốt `attempt_open` kế tiếp" của bản đầu đã hết.

### B. 13 đột biến mới (khác 50 cái đã có) — 12 sống sót, 1 bị bắt
Mỗi cái chạy TRỌN suite 205 ca; survivor nào cũng được đo thêm **hành vi 2 chiều** (canonical chặn thật / mutant mở thật). Đáng chú ý nhất:
- **Hai cửa thoát checkpoint**: `record-lease` lần hai tại checkpoint (canon rc=8; mutant rc=0 → chuỗi `leased → begin → reviewing → approve` kết ở `accepted` với `used_review=2/2`) và `begin-attempt` tại checkpoint (canon rc=8; mutant rc=0, state=`running`). Lượt 3 chỉ đóng cửa `transition`.
- **`--verdict blocked` chưa ca nào đo**: mutant đổi map thành `running` → packet chạy tiếp sau một verdict blocked mà suite vẫn xanh.
- **`--attempts-limit` và `--same-failure-limit` bị init nuốt mà suite xanh** — đúng NGUYÊN hình dạng finding `--review-calls-limit` vừa vá ở lượt 3, chưa được tổng quát hoá sang hai cờ anh em.
- **`doctrine-scan` bỏ quét `CLAUDE.md` mà suite vẫn xanh** — mọi fixture chỉ bơm nội dung vào `skills/SKILL.md`; canon bắt cụm cấm trong CLAUDE.md (rc=6), mutant mù (rc=0).
- Hai kết quả tự sửa nhận định nhờ đo: `void` với số lượt 0 (dùng âm được tới −3 nhưng **không nở trần** vì chốt `attempts_used <= 0` của `record-review` — vá g5 — chặn tầng sau ⇒ chỉ là sổ âm + tự kẹt, hạ P3); tuple state-cuối của `void` bỏ `accepted`/`blocked` thì **vẫn rc=8 nhờ review-guard** trên mọi đường CLI với tới được ⇒ rỗng hành vi, P3.
- Bị bắt: 1/13 (`B10` gỡ chốt "vào reviewing phải có lượt mở" — ca `vao_reviewing_phai_co_luot_dang_mo` giết đúng).

### C. Ngoài đột biến
- Giới hạn ĐÃ KHAI kiểm lại **đúng như khai**: 3 vòng review khép trọn, `rounds=3`, `used=0/2` — không báo lại. Hai cửa thoát checkpoint ở trên là họ KHÁC (trần đã bắn rồi mới thoát hậu quả), không phải họ "né sổ lời gọi".
- Fail-open/fail-closed đặt đúng chỗ (`.get` chỉ trên bộ đếm thông tin, có chú thích); các ca thiếu-tệp đều raise chứ không thoát êm (không tái phát bệnh t24).
- `history`/`schema_version` là trường xanh rỗng — 0 ca đọc; đo bằng B13 (bỏ ghi event `blocked_attempts_exhausted`, suite vẫn xanh trọn) — cùng họ finding `codex-executor-calls` lượt 2.

Bẫy đỏ-giả đã né bằng cách import module test canonical từ worktree (ROOT đúng) thay vì copy suite ra /tmp; bản sao đột biến đặt ở scratchpad — 15 lượt chạy trọn suite không có ca đỏ giả nào (lượt duy nhất có ca đỏ là cú giết chủ đích của B10).

```yaml
reviewed_sha: c9042bfe1df8e27a76ec685b89122701eeabe538
verdict: changes_requested
spec_axis: pass
standards_security_axis: fail
gates:
  - packet_loop_test: rc=0 — nền 205/205 đạt · 50 đột biến ok · "ca 205 · đột biến 50 · lớp lách 78 · ca bắt-oan 35 · ngoại lệ AC 18: 0 · TỔNG: ĐẠT" (100.7s)
  - va_luot_3_xac_minh: 7/7 cặp ca+đột biến là THẬT (ca state-cuối của record-review đo đúng cửa: canon rc=8 đúng thông điệp cửa state, mutant rc=0)
  - dot_bien_moi: 1/13 bị bắt (12 sống sót trọn 205 ca — chi tiết ở findings)
  - write_set: 2 tệp đổi / ngoài write set: 0
  - cay_sach_dau_cuoi: có (git status --short rỗng cả hai lần, HEAD giữ nguyên)
findings:
  - id: checkpoint-khong-kin-cua-record-lease
    severity: P2
    locator: .claude/dev/packet_loop.py:780
    evidence: "đột biến B01 (gỡ `if st[\"state\"] != \"awaiting_lease\"` trong record-lease) sống sót 205/205 ca. Hành vi 2 chiều: canon record-lease lần 2 tại checkpoint rc=8; mutant rc=0 → state=leased → begin=0 → approve=0 → state_cuoi=accepted với used_review=2/2. Checkpoint thoát được bằng một lease mới dù trần review đã cạn."
    required_repair: thêm cặp ca+đột biến — record-lease trên state ≠ awaiting_lease (đủ ba state cuối) phải rc=8 và state không đổi; đột biến gỡ cửa phải làm ca ĐỎ
  - id: checkpoint-khong-kin-cua-begin-attempt
    severity: P2
    locator: .claude/dev/packet_loop.py:809
    evidence: "đột biến B12 (nới tuple thành (\"leased\", \"running\", \"checkpoint\")) sống sót 205/205 ca. Canon begin-attempt tại checkpoint rc=8; mutant rc=0 và state bị ghi đè thành running — lối ra checkpoint thứ hai, cùng họ với cửa transition đã vá ở lượt 3 nhưng chưa ai canh."
    required_repair: thêm cặp ca+đột biến — begin-attempt tại checkpoint/blocked/accepted phải rc=8, state không đổi; đột biến nới tuple phải làm ca ĐỎ
  - id: record-review-call-state-cuoi-chi-neo-checkpoint
    severity: P2
    locator: .claude/dev/packet_loop.py:1081
    evidence: "đột biến B04 (thu tuple về (\"checkpoint\",)) sống sót 205/205 ca — ca hiện có chỉ dựng checkpoint. Hành vi: trên packet ACCEPTED với used=2/2, canon rc=8 giữ accepted; mutant rc=3 và GHI ĐÈ state accepted → checkpoint (packet đã hoàn tất bị giáng cấp bởi một lời gọi review)."
    required_repair: mở rộng ca state-cuối của record-review-call sang accepted và blocked (cả nhánh tiêu lẫn không-tiêu), kèm đột biến thu-hẹp-tuple phải ĐỎ
  - id: verdict-blocked-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:1016
    evidence: "grep: 0 ca dùng --verdict blocked (chỉ approve/changes_requested). Đột biến B06 (map \"blocked\" → \"running\") sống sót 205/205 ca. Hành vi: canon blocked → state=blocked, begin-attempt sau đó rc=8; mutant → state=running, begin-attempt rc=0 — packet chạy tiếp sau verdict blocked."
    required_repair: thêm ca record-review --verdict blocked → state=blocked + mọi cửa chạy tiếp bị chặn; đột biến đổi map phải làm ca ĐỎ
  - id: co-attempts-limit-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:629
    evidence: "grep: 0 ca truyền --attempts-limit. Đột biến B07 (init nuốt cờ, hardcode 3) sống sót 205/205 ca. Hành vi: init --attempts-limit 1, sau 1 lượt+review, begin #2: canon rc=3 state=blocked (limit=1 trong state); mutant rc=0 (limit=3). Nguyên hình dạng finding --review-calls-limit của lượt 3, chưa tổng quát sang cờ anh em."
    required_repair: thêm cặp ca+đột biến ghim trần theo đúng số được khai (như case_co_review_calls_limit_duoc_ton_trong đã làm cho cờ kia)
  - id: co-same-failure-limit-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:640
    evidence: "grep: 0 ca truyền --same-failure-limit. Đột biến B08 (hardcode 2) sống sót 205/205 ca. Hành vi: init --same-failure-limit 3, review thứ 2 cùng id: canon rc=0 state=running (limit=3); mutant rc=3 state=blocked — cờ bị nuốt im lặng mà suite xanh."
    required_repair: thêm cặp ca+đột biến ghim trần same-failure theo số được khai
  - id: doctrine-scan-claude-md-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:1243
    evidence: "mọi fixture doctrine (_repo_gia, _ca_doctrine) chỉ ghi vào .claude/skills/<x>/SKILL.md — 0 fixture có CLAUDE.md. Đột biến B09 (đổi tên tệp đích thành CLAUDE_DOT_BIEN.md) sống sót 205/205 ca. Hành vi: repo giả có cụm cấm `45 phút/run` trong CLAUDE.md: canon rc=6, mutant rc=0. CLAUDE.md là đúng chỗ bản miễn trừ thật duy nhất từng nằm (bài học dòng 82 master)."
    required_repair: thêm ca bơm cụm cấm vào CLAUDE.md của repo giả → rc=6, kèm đột biến bỏ tệp khỏi diện quét phải ĐỎ
  - id: begin-attempt-provider-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:829
    evidence: "grep: 0 ca begin-attempt sai provider. Đột biến B02 (gỡ cửa) sống sót 205/205 ca. Hành vi: begin-attempt --provider codex trên packet executor=claude: canon rc=4, used=0; mutant rc=0, attempts_used=1 VÀ codex_executor_calls_used=1 — reviewer đốt được trần executor và làm bẩn bộ đếm quan sát."
    required_repair: thêm cặp ca+đột biến cho cửa provider của begin-attempt (đối xứng với ca lượt 3 đã thêm cho record-review-call)
  - id: init-provider-allowlist-khong-phan-chung
    severity: P2
    locator: .claude/dev/packet_loop.py:591
    evidence: "0 ca init với provider ngoài PROVIDERS (ca hiện có chỉ đo trùng nền, rc=4). Đột biến B05 (gỡ membership check) sống sót 205/205 ca. Hành vi: canon init --executor bot-tu-che rc=2; mutant rc=0 rồi begin-attempt --provider bot-tu-che rc=0 state=running — nhãn nền tự chế đi trọn luồng; hai chuỗi khác nhau của CÙNG một nền (vd codex-2/codex) sẽ qua được chốt cross-provider."
    required_repair: thêm cặp ca+đột biến — init với executor/reviewer ngoài PROVIDERS phải rc=2
  - id: void-attempt-so-am-khong-phan-chung
    severity: P3
    locator: .claude/dev/packet_loop.py:882
    evidence: "đột biến B03 (gỡ `attempts_used <= 0`) sống sót 205/205 ca. Hành vi: void ×3 trên packet mới: canon rc=[8,8,8] used=0; mutant rc=[0,0,0] used=−3. KHÔNG nở trần được (chốt attempts_used<=0 của record-review — vá g5 — chặn tầng sau, chỉ mở thêm được 1 lượt rồi kẹt), nên chỉ là sổ sách âm + tự kẹt — vẫn là cửa cưỡng chế không ai canh."
    required_repair: thêm cặp ca+đột biến — void khi attempts_used=0 phải rc=8 và used không âm
  - id: void-state-cuoi-accepted-blocked-rong-hanh-vi
    severity: P3
    locator: .claude/dev/packet_loop.py:880
    evidence: "đột biến B11 (thu tuple của void về (\"checkpoint\",)) sống sót 205/205 ca, NHƯNG đo bóng che: trên packet blocked, mutant vẫn rc=8 qua review-guard (`lượt 2 đã có review`) — mọi đường CLI tới accepted/blocked đều có review cuối khớp attempts_used, nên hai phần tử ấy chỉ đổi thông điệp, không đổi hành vi."
    required_repair: hoặc thêm ca rẻ ghim cả accepted/blocked (đóng luôn cửa cho refactor tương lai), hoặc ghi chú tường minh tại code rằng hai phần tử ấy là lớp dự phòng bị review-guard che
  - id: history-truong-xanh-rong
    severity: P3
    locator: .claude/dev/packet_loop.py:845
    evidence: "grep: 0 ca đọc `history` (và `schema_version`). Đột biến B13 (bỏ ghi event blocked_attempts_exhausted) sống sót 205/205 ca — cùng họ finding codex-executor-calls-khong-ca-nao-do của lượt 2 đã được chấp là phải vá."
    required_repair: ít nhất một ca đọc history sau các biến cố chính (blocked/void/checkpoint) khẳng định event có mặt; hoặc khai tường minh history là trường không cưỡng chế
khong_do_duoc: []
```
