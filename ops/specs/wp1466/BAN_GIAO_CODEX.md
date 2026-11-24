# Bàn giao packet wp1466 (#1466) cho Codex — 22-11-2026

Phiên điều phối trước là Claude Code, `session_015GtxrcdabvDuhzgezMEE89`. Chủ kho yêu cầu chuyển cho Codex triển khai tiếp.
**Tệp này là handoff, KHÔNG phải lease** (protocol §7). Không làm gì ghi vào kho khi chưa có Issue và lease còn hiệu lực.

Thứ định danh hiện vật là **BĂM và SHA**, không phải tên nhánh. Tìm tệp trên `master` trước; nếu PR #1495 chưa merge
thì fetch nhánh `ops/wp1466-spec`.

## 1. Packet làm gì
Biến §8.3 (review theo lớp: `class_slug`, bảng lớp, đối chiếu bốn nhãn, hội tụ |F|/|U|, lặp lần ba thì checkpoint ghi
sổ ADR-0067) thành bất biến cho MỌI lượt review. Kèm một bất biến meta: mọi nguyên tắc bắt buộc của protocol phải khai
cổng máy ở §20, hoặc mang nhãn "kỷ luật, 0 cổng" kèm một nợ có tên. Sản phẩm của wp1466 gồm:
- ADR-0068;
- bảng 28 dòng `INV-NN` trong `docs/PROTOCOL_DA_PHIEN.md`;
- cổng toàn vẹn trong `packet_loop.py doctrine-scan`, khoá 7 đơn vị văn bản protocol theo địa chỉ, tính duy nhất và
  băm byte;
- các ca `doctrine_inv_*` và đột biến.

Write set có đúng 4 tệp:
- `docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md`
- `docs/PROTOCOL_DA_PHIEN.md`
- `.claude/dev/packet_loop.py`
- `.claude/dev/packet_loop_test.py`

## 2. Trạng thái (đo lại 24-11-2026, 11:17Z)
| hạng mục | trạng thái |
|---|---|
| Đặc tả | `ops/specs/wp1466.md` r8, sha256 `98790505d927224bc5e1e42e8f9460376a911a913e2e1d1b12bdf36c5eb20834`, commit `e215940`. **ĐÃ ĐÓNG BĂNG**: chủ kho duyệt băm (C1, E5) tại #1466 issuecomment-7058374374 |
| Review đặc tả | 8 lượt Codex `gpt-6-astra`/`xhigh`; lượt 8 `approve`, bảng (i) 0 P0–P3. Hồ sơ ở `ops/specs/wp1466/review/r1-l1/` … `r8-l8/` (PROMPT, VERDICT, run.json, evidence, SHA256SUMS) |
| Quyết định chủ kho đã có | tách 3 packet (E2) · merge thẳng master cho #1466/#1469/#1470 (C5, E5) · đổi người soạn sang Opus 5.5 (E2) · tách khối tiền kiểm sang #1484 (E2) · C1 duyệt băm · C3 miễn Windows (`windows: <H> mien`) · C4 giữ INV-03 `chưa đo` và INV-18 nguồn CLAUDE.md. Mọi bản ghi hộ nằm trên #1466 |
| PR #1495 | đưa đặc tả và hồ sơ vào master. Head `85fbc80`, CI 25 xanh + 2 bỏ qua, bot Codex 0 finding, `mergeable_state: clean`. **Chờ chủ kho tự merge** |
| Lease wp1466 | CHƯA cấp |
| B4 #1462 | **ĐÃ MERGE vào master**: PR #1504, merge commit `2cbb552876c2f0dd6e957db7c2408112c7527127` (24-11 10:45Z), nằm trên first-parent master. Issue #1462 vẫn `open`. Lease `wp1462-r9-g6-codex-release` (trên `origin/ops/wp1462-r1`) VẪN GIỮ `packet_loop.py` và `packet_loop_test.py`, hết hạn `2026-11-24T14:46:31Z`, hoặc sớm hơn nếu bị thu hồi |
| Trần Codex | `tran_loi_goi_codex: ADR-0055@d2e3052…` ⇒ trần 10 lời gọi; **đã dùng 9**. Lời gọi 2 bị đứt mạng nhưng vẫn tính. Bot connector trên PR không tính |
| Packet kế nhiệm | KN-0 #1469, KN-1 #1470 (nối tiếp, sau wp1466), #1484 tiền kiểm lease toàn kho (nợ `INV-02-TIEN-KIEM-CAP-LEASE-KHONG-CLOSURE`, độc lập với KN-0/KN-1). Cả ba đều `proposed`, chưa có đặc tả |

**Chạy thử điều kiện bắt đầu, chỉ đọc (24-11 11:17Z, clone sạch, master `2cbb552`):**
- 3a: 330/330 nhánh, thiếu 0, thừa 0, không shallow.
- 3b: policy 0.
- 3d: chưa ref nào có ADR 0068 trở lên.
- 3c: ADR-0068 và `PROTOCOL_DA_PHIEN.md` cho `NGƯỜI_GIỮ 0`. Hai tệp `.py` cho `NGƯỜI_GIỮ 1: wp1462-r9-g6-codex-release` (rc 11).

Vậy chỉ cấp được lease wp1466 sau 14:46Z hôm nay, hoặc sớm hơn nếu lease B4 bị thu hồi.

**Nguyên mẫu trên master mới:** `git apply -3` của `nguyen-mau-r5/nguyen-mau.patch` lên `2cbb552`:
- `packet_loop.py`, `PROTOCOL_DA_PHIEN.md` và ADR-0068 áp sạch;
- `packet_loop_test.py` XUNG ĐỘT một chỗ, quanh dòng 19303 của bản cũ, ở phần đăng ký ca/đột biến.

B4 thêm khoảng 884 dòng vào tệp test và khoảng 251 dòng vào `packet_loop.py`. Executor phải giải xung đột, rồi đo lại
N1–N16, trần 450 dòng / 6 tệp, và khối `so-dang-ky` trên base mới.

## 3. Vai trò và trùng số ADR — ĐÃ QUYẾT (24-11)
- **Vai trò (E2), ghi hộ ở #1466 issuecomment-7130067171:** "Codex chỉ điều phối, Claude vẫn viết mã."
  - Đặc tả r8 giữ nguyên; không cần r9.
  - Executor mã là Claude. Reviewer exact-H là Codex.
  - Trần ADR-0055 còn 1/10 lời gọi Codex. Nếu lượt review exact-H cần nhiều hơn một lời gọi, xin `nang_tran` (E2) TRƯỚC khi gọi.
- **Trùng số ADR-0068 (E2/E5), ghi hộ ở #1466 issuecomment-7130100252:** "wp1466 giữ, chạy trước".
  - wp1507 (DON-RAC-A, Mission #1506) đổi sang ADR-0069 và rebase sau khi wp1466 land; việc đó cần r2 và chủ kho duyệt lại băm.
  - Đã báo phiên wp1507 ở #1507 issuecomment-7130103221.
  - Hai packet cùng sửa `docs/PROTOCOL_DA_PHIEN.md`, nên phải chạy NỐI TIẾP. Trước khi cấp lease wp1466, ở bước 3c, kiểm
    xem wp1507 đã có lease giữ protocol chưa. Nếu có thì DỪNG và hỏi chủ kho.
  - Đặc tả nháp `SPEC-A` (CI-TAI-DUNG-THEO-CAY, nhánh `claude/ci-toi-uu-do-dac-20261115`) cũng đặt tệp `0068-`. Nó chưa
    đóng băng và tự có luật DỪNG khi số đã bị chiếm.
  - Bước 3d chỉ kiểm tệp `docs/adr/0068-*` trên mọi ref. Lúc đo chưa ref nào có tệp ấy; số chỉ thực sự được chiếm khi land.

## 4. Việc tiếp theo, theo thứ tự
1. Chờ chủ kho merge PR #1495. Kiểm sau merge: `git rev-parse origin/master:ops/specs/wp1466.md` phải trỏ tới blob có
   sha256 bằng `98790505…`.
2. Chờ B4 #1462 land: merge commit nằm trên `git rev-list --first-parent origin/master`, và lease
   `wp1462-r9-g3-claude` (cùng mọi generation sau nó) hết hiệu lực hoặc bị thu hồi.
3. Chạy **điều kiện bắt đầu 3a–3e ở mục 1 của đặc tả**, đúng nguyên văn, trên clone không shallow:
   - 3a: so tập cặp `ls-remote --heads origin` với `for-each-ref refs/remotes/origin`, rồi fetch tới khi hai bên khớp;
   - 3b: `ls-tree -z origin/master` không có policy/schema change-impact;
   - 3c: `python ops/lease_publish.py ai-dang-giu <đường dẫn>` cho cả 4 đường dẫn, đòi `NGƯỜI_GIỮ 0`. Nếu ra rc 12 thì
     đưa nhánh cục bộ về khớp rồi chạy lại;
   - 3d: số ADR 0068 chưa bị ref nào chiếm;
   - 3e: sau khi đăng lease, đo lại; đòi `NGƯỜI_GIỮ 1: <id vừa đăng>`.

   Giới hạn G1–G10 của các công cụ này là nợ #1484; đừng hứa gì về chúng.
4. Cấp lease: `spec_hash` `98790505…`, base là `origin/master` sau bước 3a (phải chứa merge của B4), dòng
   `windows: <H> mien`, executor Claude, reviewer Codex (mục 3).
5. Thi công. Áp nguyên mẫu `ops/specs/wp1466/nguyen-mau-r5/nguyen-mau.patch` (+434 −4, áp được lên `48d372e` bằng
   `git apply -p1`; trên base sau B4 có thể phải rebase tay) làm điểm xuất phát. Đo lại mọi tiêu chí N1–N16 ở mục 9 trên
   mã giao nộp. Dùng các khối `do-pham-vi` (N8) và `so-dang-ky` trong đặc tả. Trần ADR-0053 là 450 dòng / 6 tệp: đo
   `git diff --numstat` trước mỗi lần đẩy.
6. Review exact-H theo `.claude/skills/cross-review/SKILL.md`. Reviewer khác họ với executor; dùng mirror đầy đủ,
   `core.abbrev 7`, bảng lớp (i)/(ii) như các lượt review đặc tả.
7. Trình chủ kho audit exact-H; chủ kho tự merge (E5).
8. Sau khi land: báo phiên Mission #1172 (`session_015Gtxrb3cuZ7Nm935R8yA5W`) — việc này chỉ thực hiện khi KN-1 #1470
   land, để gỡ chốt tạm `kiem_verdict_lop.py`. Rồi soạn đặc tả KN-0 #1469.

## 5. Bẫy đã gặp trong phiên này
- `ai-dang-giu` trả rc 12 khi bộ đệm ref thiếu nhánh hoặc nhánh cục bộ tụt sau. Fetch đủ rồi so TẬP tên, không so số đếm.
- Gate `ops/bash_nen.py quet` parse MỌI `*.py` trong INDEX và fail-closed. Mảnh mã không phải module thì đặt đuôi
  `.py.txt` (xem `DOI_TEN_MANH_MA.md`).
- Workflow `ops — đăng lease bằng git` đỏ khi push một commit merge master vào nhánh `ops/**`, vì nó kéo theo lease của
  packet khác (rc 8 hết hạn, rc 9 đã đăng). Đó không phải lỗi nội dung.
- Không viết chuỗi dấu bỏ qua CI (skip + ci trong ngoặc vuông) trong commit, kể cả khi trích dẫn.
- Mọi quyết định chủ kho phải ghi hộ lên Issue theo ADR-0067 (dòng `Quyết định chủ kho — ghi hộ` + nguyên văn + ngữ
  cảnh), rồi đọc lại.
- Khối tiền kiểm r5–r7 đã rút; hồ sơ của nó (`tien-kiem-r6/`, `tien-kiem-r7/`, `review/r5-l5` … `r7-l7`) là đầu vào cho
  #1484, không phải lời khai của wp1466.

## 6. Hiện vật ngoài kho (sẽ MẤT khi container bị thu hồi)
Cây nguyên mẫu `proto` (`c35ee03`) và các clone reviewer nằm trong scratchpad của phiên cũ. Mọi thứ cần để tái lập đã
nằm trong kho: các patch `nguyen-mau-r*/`, script `sc/`, log và `SHA256SUMS`. Đừng trỏ tới đường dẫn `/tmp/...` nào.
