# Cross-review Codex — packet #814 (`MAY-ADR-0054-c`) revision 3 — lượt 5 (xác minh merge)

Bạn là **reviewer độc lập, offline** cho Packet #814, revision 3, generation 2. Executor là Claude (họ `claude`);
bạn là Codex (họ `openai`) ⇒ `assurance_target: cross_approved`, `review_class: sensitive`. Không kế thừa context
executor. Không truy cập mạng, không GitHub, không push. Bạn KHÔNG sửa mã nguồn của packet; mọi phép thử (đột biến,
fixture, script) chạy trên **bản sao riêng** của bạn dưới `OUT/`.

## Định danh (tự kiểm, đừng tin bảng này)

- `SRC` = thư mục `src/` cạnh tệp prompt này: clone thường (`.git` là thư mục, không nông), detached tại head ứng viên
  **`acce679c350adab2afa2c4c151039bf16edb4cc0`**. Base = **`c2d84ea7c20e835968b630a4fb1b8daa29ac12c7`** (`origin/master` lúc review;
  ref `refs/remotes/origin/master` trong clone trỏ base). Head = merge `acce679` của head đã approve `5a5c5c1` (lượt 4) với base; chuỗi packet `1a8388b` → merge `335e746` (master `20a2e2b`) → vá `4adbf92` → vá `b35a7e4` → merge `24f6a73` (master `7f19424`) → vá `f029321`; base lease là
  `09db70350414d767b793a71cb630e643f216a1b1`. Thứ định danh tệp là **băm/SHA**, không phải tên nhánh.
- `OUT` = thư mục `out/` cạnh tệp prompt này, là nơi DUY NHẤT bạn ghi.
- Đặc tả con `tham-chieu/wp814-r3.md`, sha256 `39b4288959f3889c6c3aad2d24b355c1c02b1462a8854c6a5b00677e81a7ce73`.
  Tệp này chỉ có trên nhánh đặc tả, không có trong `SRC`, nên được chép sang đây; hãy băm lại.
- Phần chung (ràng buộc) `SRC/ops/specs/may-adr-0054-chung.md`, sha256 `4e3d1e1b3f6a0b60b96ad7b70f0ece97eca4bb3d6d10defeab1cd24ac6d1cbf0`.
- Lease (bản chép) `tham-chieu/lease-wp814-r3-g2-claude.yaml`. Write set của PR: `.claude/dev/packet_loop.py`,
  `.claude/dev/packet_loop_test.py`. Diff ≤ 450 dòng thêm (ADR-0053).
- Verdict lượt 4 (neo `5a5c5c1`, **approve**): `tham-chieu/wp814-g2-codex-luot4-VERDICT.md`, sha256 `d75eda0f09de0f997cf5acabdfc2f0ea172705a4dc3477ccf7fa34331e5718b2`.
- Verdict lượt 3 (neo `24f6a73`): `tham-chieu/wp814-g2-codex-luot3-VERDICT.md`, sha256 `9dc9d5a696f9fee205e964b582cf6f4b0c0a23a304250fde4c1e26fee1fd1c7f`.
- Verdict lượt 2 (neo `4adbf92`): `tham-chieu/wp814-g2-codex-luot2-VERDICT.md`, sha256 `d2459a3672a0b3de757323fc1a86bb0346637655e64f775ab3156df45a29bc0a`.
- Verdict lượt 1 (neo `335e746`): `tham-chieu/wp814-g2-codex-luot1-VERDICT.md`, sha256 `8ca0f12346366fd9efde9a445923d2c7e7bfc98358fb2a1a05989de6bc62aea2`. Các tệp probe/script lượt 1 nhắc tới KHÔNG có ở đây; hãy tự dựng lại phép đo từ mô tả.
- Đầu vào cho M4 (nợ P3 của #813): `tham-chieu/wp813-g1-claude-handoff.md` và `tham-chieu/wp813-g1-codex-luot6-VERDICT.md`.

## Vì sao có lượt 5 (ADR-0052: lượt thứ hai trở đi phải nêu lý do)

Lượt 4 **approve** `5a5c5c1` (0 P0–P2; P3 `legacy-p3-failure-counts-retained` owner #816, P3 `r814-mutation-evidence-incomplete`
biểu hiện `duplicate-destination`). Executor đẩy `5a5c5c1` một lần (PR #998). `master` tiến tới `2618eb4`/`c2d84ea` sau approve nên
check `thu-hoi` đỏ (`S 2618eb4 không phải tổ tiên của H 5a5c5c1`). Theo `push_policy` của lease (tiền lệ #813 lượt 5): merge master
(KHÔNG rebase) ⇒ `acce679`, rồi **một lượt xác minh** trước khi đẩy merge commit. Đây là lượt đó.

Lượt này phải: (a) xác nhận hai tệp write set ở `acce679` giống từng byte `5a5c5c1` (blob OID) và base mới là tổ tiên head;
(b) đọc `git diff 4488444 c2d84ea` (phần master mới) và đo xem nó có đổi hợp đồng của cửa nào mà packet chạm không — đặc biệt
`.claude/skills/cross-review/SKILL.md` (đọc bởi `doctrine-scan`) và mọi tệp canon `_du_dieu_kien_approve` nạp (`ops/bien_nhan_v2.py`,
`ops/lease_publish.py`, `.claude/dev/launcher.py`, `AGENTS.md`, `docs/PROTOCOL_DA_PHIEN.md`); chạy lại `doctrine-scan`, `adr-song` và
ca `^r81[234]_|^r834_|^stdout_cp|^moc_` trên head; (c) giữ nguyên hạng và slug của mọi lớp nếu không có thay đổi — không mở lớp mới
từ phần không đổi, trừ khi merge làm đổi hành vi thật.

## Luật phân hạng (chủ kho, #813 issuecomment-6434997179 — BẮT BUỘC áp từ lượt này)

- Một đột biến độ phủ **MỚI** do reviewer tự dựng mà mã sản phẩm vẫn từ chối/xử lý đúng ở probe A/B ⇒ **P3** (nợ có tên,
  owner, hướng xử lý), KHÔNG xếp P2.
- Chỉ xếp **P2 trở lên** khi: có hành vi sai thật của mã sản phẩm; hoặc một đột biến/phản chứng đã nêu ở lượt TRƯỚC vẫn sống;
  hoặc thiếu ca bắt buộc của `nghiem_thu`.
- Nói rõ cho mỗi lớp lý do xếp hạng theo luật này.

## Cơ chế executor đã chọn (đặc tả con chỉ cho bất biến; hãy đo xem cơ chế có giữ chúng không)

1. **Bảng nối (M1, I11).** (xem thêm bảng cửa ở trên) Biên nhận H có trường tuỳ chọn `bang_noi: [{tu: [slug vòng trước], den: slug vòng này, ly_do}]`;
   `tu: []` là reviewer khai một lớp MỚI. `_du_dieu_kien_approve` kiểm lược đồ (sai kiểu, nguồn lặp, đích lặp, lý do rỗng ⇒ từ
   chối, mọi cửa) và trả thêm `noi` từ chính ảnh đã đọc. Ở `record-review`: nguồn phải là lớp P3 vòng trước và đã rời vòng này,
   đích phải là lớp P3 vòng này ⇒ ngược lại từ chối.
2. **Vòng vá P3 (M2).** Mỗi review của packet áp ADR-0054 lưu `lop` (slug, hạng), `bang_noi`, `vong_p3`. Verdict là **vòng vá P3**
   khi review liền trước toàn-P3 (khác rỗng, mọi lớp P3) và không có sự kiện `mo_lai` (ci-do/connector) giữa hai lượt review.
   Verdict toàn-P3 đầu tiên không có tiền thân như vậy là mốc. Review cũ không có `lop`: xem bảng trên (state trước #814). Trong một vòng: slug P3 mới không có ở vòng trước và không là đích
   của bảng nối ⇒ từ chối ("đổi tên không bảng nối"); số lớp P3 so **sau khi áp bảng nối lên cả hai vòng**. `_xet_dung` (sau khi
   ghi sổ) chặn `blocked` khi vòng thứ > 2 hoặc số lớp không giảm. Bộ đếm `finding_counts` (và `finding_ids` của review và của sự kiện `mo_lai`) bỏ slug P3.
3. **Cửa tự chọn vá P3 (M3).** Lệnh mới `vua-p3 --packet N --finding-id <slug P3>...`: từ `approved_pending`, tập chọn khác rỗng và
   là tập con `bien_nhan_approve.p3` ⇒ `running`, ghi `mo_lai_tu = {nguyen_nhan: p3, generation, sha: pending_sha}` (I6) và sự kiện
   `vua_p3`; gọi `_xet_dung(..., "vua-p3")`, đã thêm vào `CUA_DI_TIEP`. Không đổi parser/hợp đồng của `mo-lai`, `accept`, `chu-kho-duyet`;
   `_load` nhận thêm `p3` là nguyên nhân hợp lệ của `mo_lai_tu`.
4. **M4.** Hai ca nợ #813: `r814_check_refs_tron_null` (đột biến `r814_refs_bo_do_dai`), `r814_ci_void_connector` (đột biến mới
   `r814_void_khoi_phuc_quyen_ci`, và ca được thêm vào đích của `r813_quyen_ci_qua_luot_moi`). Chốt chặn ca (b) là điều kiện
   "chưa có `begin_attempt` sau `mo_lai` cuối" trong `cmd_mo_lai` (rc=8).

## Việc

1. Băm lại hai đặc tả và bốn verdict trước. Xác nhận base là tổ tiên head. Đọc `git diff c2d84ea acce679` (chỉ hai tệp write set) và `git diff 4488444 c2d84ea`.
2. Review **không lọc** (chuẩn connector) theo bất biến I1–I11 của phần chung mà packet chạm, và theo M1–M4 của đặc tả con.
3. Đối chiếu **từng** ca bắt buộc trong `nghiem_thu` với ca `r814_*`. Với mỗi ca, đo đột biến khai trong `MUTANTS` có giết đúng ca
   ấy và **đúng lý do** không: đọc tên ca, lớp ngoại lệ và thông điệp, không chỉ mã thoát. Mutant chết vì traceback/CLI sập là tín
   dụng giả. Sau đó tự đột biến thêm bản vá để tìm chốt **không** được ca nào bảo vệ.
4. Đặc biệt soi (gợi ý, không giới hạn):
   - Cơ chế bảng nối có thực sự bắt được đổi tên/gộp để "giảm" giả không; có đường nào làm số lớp giảm mà không có sửa thật
     (vd khai `tu: []` cho lớp mới rồi bỏ lớp cũ, hay đẩy một lớp P3 sang hạng khác).
   - Định nghĩa "vòng vá": verdict `changes_requested` toàn-P3; chuỗi xen `mo-lai`, `void-attempt`, `chu-kho-duyet`; review cũ
     không có `lop` (state trước #814, I9).
   - I4: lỗi đầu vào (bảng nối, `vua-p3`) giữ state nguyên byte; vi phạm vòng là kết quả hợp lệ ⇒ ghi sổ rồi `blocked`.
   - I5/I6: `vua-p3` gọi `_xet_dung`; quyền `mo_lai_tu` p3 neo đúng, thay quyền cũ; quyền p3 không mở được `mo-lai connector`
     từ `running`.
   - Bất biến `findings` của `_load` sau khi bỏ slug P3 khỏi bộ đếm.
   - Hợp đồng `accept`, `mo-lai`, `chu-kho-duyet` không đổi; mọi ca `r812_*`, `r834_*`, `r813_*` vẫn đạt.
   Nếu thấy đặc tả mâu thuẫn với code hiện hành, hoặc cơ chế executor chọn trái một bất biến, thì nêu rõ.
5. Hướng thử nào đòi soạn nội dung dạng đường dẫn thoát khỏi cây thư mục thì **mô tả bằng lời** trong verdict, đừng tự soạn.

## Cách chạy

- Suite đầy đủ `python .claude/dev/packet_loop_test.py` tốn khoảng 60 phút; executor chạy riêng trên clone ghim head. Ưu tiên
  chọn lọc: `python -B -W ignore tham-chieu/chon.py src '<regex tên ca>' ['<regex tên đột biến>']` chạy các ca khớp regex trên
  `src`, rồi (nếu có đối số thứ ba) mọi đột biến khớp regex theo đúng logic mục 3 của `main()` (ca đích, đối chứng khác họ, tín
  dụng giả). Ví dụ `'^r814_' '^r814_'`. Hãy đọc mã script trước khi tin kết quả của nó.
- Chạy thêm `^r813_` và `^r812_` (và `^r834_` nếu thời gian cho phép) để kiểm không hồi quy.
- Muốn thử đột biến riêng: chép `SRC` sang `OUT/`, sửa bản chép, rồi trỏ script vào bản chép.
- Nếu git toàn cục của sandbox có `commit.gpgsign=true`, cô lập bằng `GIT_CONFIG_GLOBAL=/dev/null GIT_CONFIG_SYSTEM=/dev/null`.
- `export PYTHONDONTWRITEBYTECODE=1`.

## Dạng verdict — ghi TĂNG DẦN vào `OUT/VERDICT.md`

- Dòng 1: `Verdict: approve` hoặc `Verdict: request_changes`.
- Dòng 2: `Reviewed commit: acce679c350adab2afa2c4c151039bf16edb4cc0`.
- Dòng 3: `Spec sha256: <đủ 64 ký tự>` và `Chung sha256: <đủ 64 ký tự>`.
- Sau đó là bảng lớp, đếm theo nguyên nhân chứ không theo số biểu hiện:
  `slug | hạng P0–P3 | biểu hiện file:dòng | phép đo/tái hiện đã chạy | hướng vá`.
- Bảng đối chiếu từng ca bắt buộc. Kết quả các lệnh đã chạy, kèm rc và bằng chứng dương.

Slug phải là kebab-case ổn định, đặt theo nguyên nhân, để các lượt sau so được. Ngưỡng approve: **không còn P0/P1/P2**. P3 còn lại
thì nêu tên và hướng xử lý. Verdict chỉ neo commit trên, không cấp quyền push, merge hay land.

## Ngoài phạm vi (không tính hạng)

- Protocol (#977), generation kế tiếp (#815), ghi đẩy và kích hoạt (#816), tiêu thụ `mo_lai_tu`/`checkpoint_day` ở cửa đẩy.
- Packet này KHÔNG kích hoạt ADR-0054.
