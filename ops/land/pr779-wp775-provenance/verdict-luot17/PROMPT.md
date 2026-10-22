# Kiểm định độc lập — Packet #775 (wp775, bộ đếm review trong `packet_loop.py`), lượt 17

Bạn là reviewer Codex, khác họ với executor (Claude). Vai CHỈ ĐỌC với mã: không sửa tệp nào trong KHO; chỉ ghi vào thư mục
làm việc hiện tại (thư mục ra). Kết quả bắt buộc: `VERDICT.md` trong thư mục ra.

Đây là kiểm định **tính đúng của một bộ đọc/ghi JSON trạng thái cục bộ** (sổ đếm vòng review) — không có mạng, không có
người dùng khác, mọi "state hỏng" là tệp JSON do chính bộ test tạo trong `/tmp`.

**Cách ghi:** tạo `VERDICT.md` NGAY (khung + dòng đầu), rồi sau MỖI phép đo cập nhật kết luận của phép đo đó.

## Định danh

- Kho `ducthangho/tra-luat`, bản sao tại `KHO`, HEAD tách tại `f9d84d70fb46540bbecfae963c9afb4a2b48984d` (PR #779).
- Diff toàn packet: `git -C KHO diff 653fef3f52f3130dd6f597c1036430ffb807fef1 f9d84d7 -- .claude/dev/` (2 tệp, 346 dòng thêm).
  Diff từ lượt 16: `git -C KHO diff 84bdbaccbd85210db3cb829bc487a28c2e1848a4 f9d84d7 -- .claude/dev/` — đúng `HINT-F18.patch`
  (sha256 `cad226ea…`): trong `pl_m6_state_v1`, `sd2` ghi `reviewer_identity={"model_family":"openai"}`, `sd` giữ thiếu họ.
- Đặc tả `SPEC` sha256 `4b7530c265dddefbebd06ea209d7c0594210f57b391e0d0d353931171fd2b6d8`. Verdict lượt 16:
  `VERDICT-luot16.md` (có bảng audit 40 ô trên `84bdbac`).
- Quyết định chủ kho (#775 issuecomment-6234968131): vòng review ↔ vá tới khi P1=P2=P3=0. Bảy mục nợ ngoài phạm vi spec r1
  KHÔNG tính lại: bằng chứng launcher; receipt trước khi đếm vòng; trần vòng theo ngày đóng băng spec; fallback/human_audited;
  kế thừa ngân sách giữa generation; đổi chéo cờ `da_dung` giữa hai lời gọi; lời gọi codex cuối thất bại không tự vào rescue.

## Việc cần làm (theo thứ tự; ghi kết luận sau mỗi bước)

1. **F18 đã đóng chưa?** Diff 84bdbac→f9d84d7 đúng là HINT-F18; `pl_m6_state_cu_mat_ho` chết ở assertion "v1 phải suy
   3/3", không ở guard provider; `pl_m6_suy_used_0` vẫn chết ở `record-codex-call` đòi rc=3.
2. **Audit ĐỦ mọi đột biến `pl_*` một lượt** — lượt 16 đã audit (39/40 đúng chốt); audit LẠI trên HEAD này vì ca M6 vừa đổi.
   Lượt này hãy xét **toàn bộ** đột biến `pl_*` trong `MUTANTS` (39 tên / 40 ô): với từng ô, ghi (a) ca đích, (b) bước chết
   (lệnh + đối số), (c) chốt runtime mà đột biến nhắm tới, (d) điểm chết có phải đúng chốt đó không. Bảng đủ 40 dòng trong
   `VERDICT.md`. Mỗi ô chết sai chốt là một finding (gom cùng lớp `mutant-wrong-latch`), kèm HINT. Đặc biệt xét các đột biến khác nhắm ca
   `pl_m5_rescue`/`pl_m6_state_v1` (thứ tự bước trong ca vừa đổi).
3. **Driver có sẵn** (ở thư mục ra, `--dev KHO/.claude/dev`): `review_probes.py --only reader|consistency|bypass`;
   `probes_r2.py --repo KHO`; `probes_r3.py`; `probes_r4.py --repo KHO`; `probes_r6.py`; `schema_probe.py KHO/.claude/dev`;
   `conn_probe.py KHO/.claude/dev`. State hỏng rc=8 không traceback; luồng hợp lệ rc=0.
4. **Suite:** `cd KHO && PYTHONDONTWRITEBYTECODE=1 python3.13 -B .claude/dev/packet_loop_test.py` (đúng cwd KHO). Executor khai
   `351/351 · BỎ QUA 1 · 145 đột biến · ĐẠT`; bảng ngoài `bang_dot_bien.py` 40/40 GIẾT_THẬT.
5. **Săn finding còn lại** (P1/P2/P3) trong diff toàn packet, đối chiếu spec M1–M7. KHÔNG cần viết script mới ngoài phần audit
   đột biến; ý tưởng dữ liệu thử mới thì MÔ TẢ BẰNG LỜI.

## Mức và HINT

P1 = sai luật của spec, hoặc chốt ngân sách/rescue không giữ được; P2 = chặn nhầm state hợp lệ, ca/đột biến không đo đúng thứ
khai, traceback thay mã thoát; P3 = nhỏ (thông điệp, độ rõ, phong cách). Mọi finding kèm `HINT` patch `-p0` từ gốc KHO, đã thử
`patch -p0 --fuzz=0 --dry-run` trên bản sao, ghi Δ dòng thêm. Nhiều ô cùng lớp thì có thể gộp một HINT.

## Định dạng VERDICT.md

- Dòng đầu: `Reviewed commit: f9d84d70fb46540bbecfae963c9afb4a2b48984d`
- `verdict: approve` hoặc `verdict: changes_requested`; dòng `P1=… P2=… P3=…`.
- Mục ĐỐI CHIẾU LƯỢT TRƯỚC (F01–F18 + finding connector lượt 11–12), BẢNG AUDIT 40 Ô, bảng LỚP, mỗi finding (mã F19…, slug,
  mức, tệp:dòng, phép đo, HINT). Bảng ≥ 6 HƯỚNG THỬ. Mục "Đã đo" và "KHÔNG ĐO ĐƯỢC". approve chỉ khi P1=0 và P2=0.

## Đường dẫn

- KHO: `/tmp/claude-0/-home-user-tra-luat/d2609060-62e1-5761-b248-ec0c3bc71a0b/scratchpad/rv17`
- Thư mục ra: `/tmp/claude-0/-home-user-tra-luat/d2609060-62e1-5761-b248-ec0c3bc71a0b/scratchpad/rv17-out`
