# Cross-review §8 — wp55 revision 2 generation 2 — PR #92

Bạn là REVIEWER độc lập, khác nhà cung cấp với executor (executor là `claude`, bạn là `codex`).
Nhiệm vụ: review mã của PR #92 trong kho `ducthangho/tra-luat`.

## NEO — không được trôi khỏi các mốc này

- Kho: `ducthangho/tra-luat`
- HEAD đang review: `22d2cc92164ca2018c0560aaf9404659ea81f51e`
- Base (merge-base với master): `fbe5ab9e1ece3b45c065879bfd59dee2554db3e2`
- write_set — ĐÚNG 6 tệp, không review gì ngoài đây:
  - `.claude/dev/packet_loop.py`
  - `.claude/dev/packet_loop_test.py`
  - `.claude/skills/cross-review/SKILL.md`
  - `.claude/skills/land-packets/SKILL.md`
  - `.claude/skills/work-packet/SKILL.md`
  - `CLAUDE.md`

Xem diff bằng: `git diff fbe5ab9e1ece3b45c065879bfd59dee2554db3e2 HEAD -- <tệp>`

## Doctrine của kho — vi phạm là FINDING, không phải góp ý phong cách

1. **Đòi BẰNG CHỨNG DƯƠNG, đừng tin `rc=0`.** Cổng xanh nhờ mã thoát là cổng bị lừa được.
   Bằng chứng phải là hai số BẰNG NHAU (`N/N`) hoặc `"ok": true`. Đã trả giá: một lệnh thoát 0
   với stdout RỖNG từng được ghi thành "thành công".
2. **Chốt chỉ TỒN TẠI nếu có ca làm nó ĐỎ.** Một điều kiện không có phản chứng là trang trí.
3. **Script/quy trình đa nền phải chạy THẬT trên nền đó**, không suy từ đọc code.
4. **rc=0 mà đầu ra rỗng** là ca thật, phải bị coi là hỏng.
5. Không tự cấp lease, không tự review, không merge/land khi chưa được duyệt.

## Điều PR này TỰ NHẬN đã làm — hãy kiểm từng cái, đừng tin lời commit

Đọc `git log fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..HEAD` rồi kiểm:

- `acceptance` **chỉ còn MỘT cửa** — không còn đường thứ hai lọt qua.
- `reviewing` **đòi lượt mở** — không có lượt mở thì không vào được trạng thái đó.
- `void-attempt` phải **đóng lượt đang mở**; nếu không nó khoá cứng packet.
- `doctrine-scan` từng **lọt 5/9 dòng doctrine THẬT chỉ vì dấu nháy ngược** — kiểm bản vá có
  thật sự bắt được cả 9 không, và có ca đỏ cho nó không.
- Ba adapter khai cú pháp mới `--head-sha` / `--reviewed-sha` — kiểm khớp giữa adapter và nơi gọi.
- Máy trạng thái cưỡng chế stop conditions — tìm đường đi nào thoát được cưỡng chế.

## Việc bắt buộc phải LÀM (không chỉ đọc)

- Chạy bộ test của PR: `python3 .claude/dev/packet_loop_test.py` — ghi lại **hai con số**, không
  ghi "đạt".
- Nếu bộ test có chế độ tự đột biến, chạy nó và ghi số giết được.
- Thử **tự tay** phá một chốt bạn nghi ngờ (sửa tạm trong worktree này rồi chạy lại test) để xem
  có ca nào ĐỎ không. Worktree này dùng một lần, cứ sửa thoải mái. Không commit, không push.
- Nếu một lệnh không chạy được (sandbox, thiếu công cụ), **nói rõ là KHÔNG ĐO ĐƯỢC** — tuyệt đối
  không đoán kết quả rồi trình bày như đã đo.

## Định dạng trả lời — bám đúng

```
VERDICT: APPROVE | CHANGES_REQUESTED
BANG CHUNG DA CHAY:
  - <lệnh>: <kết quả, kèm hai con số nếu có>
FINDINGS (nặng trước):
  [1] <mức: CHAN | NEN SUA | GHI CHU> <tệp>:<dòng>
      Vấn đề: <một câu>
      Kịch bản hỏng: <đầu vào/trạng thái cụ thể → kết quả sai>
      Vì sao vi phạm: <doctrine nào, hoặc lỗi đúng/sai>
KHONG DO DUOC: <những gì bạn không kiểm được và vì sao>
```

Quy tắc cuối: **thà ít finding mà chắc còn hơn nhiều finding mà đoán.** Mỗi finding phải có kịch
bản hỏng cụ thể. Không có kịch bản thì hạ xuống `GHI CHU`. Nếu mã đúng thì nói thẳng là đúng —
`APPROVE` là kết luận hợp lệ, không phải thất bại của reviewer.
