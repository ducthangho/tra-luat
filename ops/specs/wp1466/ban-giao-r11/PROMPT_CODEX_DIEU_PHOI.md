# Prompt bàn giao: Codex điều phối tiếp wp1466 (#1466) từ đặc tả r11, lease g4

Bạn là **phiên ĐIỀU PHỐI** của packet `wp1466`, kho `ducthangho/tra-luat`. Phiên điều phối trước là Claude Opus 5.5 (session `session_015GtxrcdabvDuhzgezMEE89`). Chủ kho quyết định chuyển việc điều phối sang Codex, ghi hộ ở #1466 issuecomment-7212794523.

Viết tiếng Việt. Chỉ hỏi chủ kho những câu thuộc mã E1–E5 của ADR-0067, và ghi mã E vào mỗi câu hỏi.

**Phân vai do chủ kho quyết, không đổi:**
- Codex chỉ ĐIỀU PHỐI; Claude viết mã. Ghi ở issuecomment-7130067171.
- Executor là Claude Fable 5.2 mức high. Reviewer là Codex mức high, review THEO LỚP. Ghi ở issuecomment-7130364325.
- Phiên điều phối KHÔNG viết mã của packet và KHÔNG tự review.

## Giải mã tệp nhị phân (làm TRƯỚC)
Cổng CI không nhận tệp nhị phân trong `ops/specs/**`, nên bundle và hai tệp zip bằng chứng được lưu ở dạng base64 (`*.b64`).
Giải mã từ thư mục này:

```
for f in $(find . -name '*.b64'); do base64 -d "$f" > "${f%.b64}"; done
sha256sum -c GIAI_MA.sha256
```

`sha256sum -c` phải in `OK` cho cả ba tệp; nếu không thì DỪNG. Bundle sau khi giải mã là `wp1466-r11-g3-c5d44c9.bundle`.

## 0. Đọc trước, theo thứ tự, NGUYÊN VĂN, đừng đọc theo trí nhớ
1. `CLAUDE.md`, toàn văn. Đặc biệt các mục §Bài học đắt giá, §Gọi agent đa nền và §Protocol đa phiên.
2. `docs/PROTOCOL_DA_PHIEN.md`: §4, §5, §7, §8, §8.3, §10.2.2, §12, §20.
3. `docs/adr/0060-dieu-kien-merge-va-moc-ready.md`, đủ M1–M12. Đọc thêm ADR-0053 (trần kích thước), ADR-0055 (trần lời gọi Codex), ADR-0062, ADR-0063, ADR-0067 (mã E, ghi hộ quyết định).
4. Đặc tả đóng băng `ops/specs/wp1466.md` r11 trên master `6a4f52d`. sha256 phải ra `9a41aa6c9d25f3bf884bc293284e3aa2f05613232c7cce8b6b2640c942dbd910`; lệch thì DỪNG.
5. Toàn bộ thư mục này (`ops/specs/wp1466/ban-giao-r11/`):
   - `handoff/HANDOFF-l1.md` … `HANDOFF-l4.md`;
   - `review/*/VERDICT.md`;
   - bundle mã.
6. Các comment trên #1466 từ issuecomment-7191469520 trở đi: mọi quyết định của chủ kho và mọi bản ghi review M8.

## 1. Trạng thái lúc bàn giao (27-11-2026, khoảng 08:15Z)

| mục | giá trị |
|---|---|
| đặc tả | r11, sha256 `9a41aa6c…dbd910`, trên master qua PR #1566 (merge `6a4f52d`). Chủ kho duyệt băm ở issuecomment-7206141143 |
| lease | `wp1466-r11-g4-claude`, nhánh `ops/wp1466-r11-g4-lease`, commit `ffa56f3`. Base `6a4f52d`; hết hạn 2026-11-30T08:10Z; thay g3 (g3 mang bia mộ). Khối `nang_tran` chép NGUYÊN VĂN mục 10 của r11 (đã kiểm: mapping YAML bằng nhau) |
| exact H | `c5d44c93b4aa9326fa087af0bd07cbe918c2adc2` trên nhánh `claude/wp1466-r11-g3`. **CHƯA push.** Mã nằm trong `wp1466-r11-g3-c5d44c9.bundle`, cần base `6a4f52d` |
| diff so base | 4 tệp, +478 −4: `packet_loop.py` 78/1, `packet_loop_test.py` 201/1, `PROTOCOL_DA_PHIEN.md` 46/2, `adr/0068-…` 153/0. Trần là 500 theo `nang_tran` |
| người viết mã | Claude Fable 5.2, lượt 1–4. Handoff lượt 4 do Claude Opus 5.5 viết nốt (lượt 4b), vì Fable hết credit API và hết hạn mức subscription tới 2-12 08:00Z |
| trần Codex | 14 (ADR-0055: 10 → 13 → 14). Đã dùng 13. Lời gọi thứ 14 dành cho lượt XÁC NHẬN HẸP ở mục 2 |
| review mã lượt 2 (13/13) | Quá hạn (rc 124). Bản nháp cuối `changes_requested` với đúng 1 lớp P3 `thieu-khoi-nang-tran-kich-thuoc`, nằm ở hồ sơ lease chứ không ở mã. g4 đã vá lớp này. Mã: 0 finding. P3 cũ `ca-id-chi-do-mot-gia-tri` đã đóng thật (`rv_id_only_99` giết 6 ca; vòng 8 đột biến reviewer đều chết; 43/43 đột biến mới chết). P2 `phep-dem-ban-sao-khong-phu-ca-tep` nằm ở bảng (ii), chuyển sang #1469, nợ `INV-KHOA-BAN-SAO-DINH-CHU`, thẩm quyền E3 |
| còn chưa đo trọn | 16 mảnh (reviewer mới chạy 11/16; executor chạy đủ 16/16 với gom ĐẠT 1861/1861). `ci_dang_ky_test --chay`, tức job `gate-registry` |
| đỏ sẵn do môi trường, delta 0 | `pretooluse_guard_test` t11/t15/t33; selftest 16 ca (trong sandbox reviewer); lifecycle 23/28; `mcp_gh` 4 ca; `codex_cred` 5 ca; `cong_b4_*` 15 ca (socket bị chặn) |

## 2. Việc kế tiếp, đúng thứ tự

### 2.1 Kiểm lease g4 đã đăng
- **Comment trên #1466.** Đã đăng: issuecomment-7212923792 (`github-actions[bot]`, workflow "ops — đăng lease bằng git", nhánh `ops/wp1466-r11-g4-lease`). Đọc lại để xác nhận.
- **Ref trên máy chủ.**
  - So TẬP tên `git ls-remote --heads origin` với `git for-each-ref refs/remotes/origin` (CLAUDE.md, mục `for-each-ref`). Phải thiếu 0.
  - Ba nhánh lease cũ `ops/wp1466-r8-g1-lease`, `ops/wp1466-r9-g2-lease`, `ops/wp1466-r11-g3-lease` đã được tua tiến (fast-forward) tới `ffa56f3` lúc bàn giao; kiểm lại. Bài học đã gặp: `ai-dang-giu` tính lease cũ còn giữ khi một ref vẫn mang bản lease chưa có bia mộ.
- **Người giữ.** `python3 ops/lease_publish.py ai-dang-giu <đường dẫn>` cho cả 4 tệp phải ra `NGƯỜI_GIỮ 1: wp1466-r11-g4-claude`. Gặp rc 12 (nhánh cục bộ tụt sau) thì tua nhánh cục bộ trước khi đo.

### 2.2 Lượt Codex XÁC NHẬN HẸP (lời gọi 14/14)
- **Sandbox.**
  - `git clone --mirror` kho vào `kho.git`.
  - `git -C kho.git fetch <đường dẫn bundle> 'refs/heads/claude/wp1466-r11-g3:refs/heads/claude/wp1466-r11-g3'`.
  - Clone ra `cay-kho`, ghim `core.abbrev 7`, checkout `--detach c5d44c9`.
  - Chép `ban-giao-r11/` sang `exec-out/`.
- **Cách gọi:** `python .claude/dev/launcher.py run --workspace <cay-kho> --expected-repo github.com/ducthangho/tra-luat --expected-root-commit 394e93468fc8d84ec20938e6df8fb7ab72b2cc37 --expected-head c5d44c93b4aa9326fa087af0bd07cbe918c2adc2 --prompt-file <P> --expected-prompt-sha256 <băm> --deadline-utc <+60 phút> --run-root <...> --name wp1466-ma-h-l3-hep --agent codex --json -- <codex> exec -m <model Codex> -c model_reasoning_effort=high --cd <thư mục sandbox> --sandbox workspace-write --skip-git-repo-check "<chỉ thị trỏ tới tệp prompt>"`. Truyền prompt dưới dạng ĐỐI SỐ, vì `launcher.py run` cho stdin là DEVNULL.
- **Phạm vi của prompt: đúng HAI việc, không mở lại phần đã đo.**
  1. **Đóng lớp P3 `thieu-khoi-nang-tran-kich-thuoc`.**
     - Khối `nang_tran` của `ops/leases/wp1466-r11-g4-claude.yaml` trên `origin/ops/wp1466-r11-g4-lease` phải bằng NGUYÊN VĂN khối `yaml` ở mục 10 của đặc tả r11.
     - Đo cả hai cách: so byte và so mapping YAML.
     - Không còn trường nào ngoài bốn trường `ai_nang`, `can_cu`, `tran_cu`, `tran_moi`.
     - Lease khớp H: base, write set, nhánh.
  2. **Chạy TRỌN trên H, so DELTA với base `6a4f52d` trong cùng một lệnh dựng hai vế (CLAUDE.md, mục phép đo delta):**
     - 16 mảnh `--manh i/16` cộng job gom. Cần bằng chứng dương: `GOM: ĐẠT · 16 mảnh`, và mọi ca đỏ phải trùng base.
     - `python3 -u -B .claude/dev/ci_dang_ky_test.py --chay`.
     - Ca nào đỏ sẵn trên base thì ghi delta 0, không phải finding.
- **Đầu ra:** verdict theo khuôn của `review/wp1466-ma-h-l2/PROMPT.md`, gồm bảng lớp, ĐỐI CHIẾU LƯỢT TRƯỚC, BẢNG ĐO. `approve` chỉ khi không còn P0–P3 mở.
- **Kỷ luật reviewer:** review theo lớp; không tự ghi nợ, không tự miễn P3; hướng thử cần payload thì MÔ TẢ BẰNG LỜI.
- **Ghi bản ghi review M8 lên #1466** bằng khối máy đọc giống issuecomment-7211535026. Tệp review đưa vào PR lưu trữ hằng tuần `ops/reviews/**`; đừng mở PR riêng chỉ để lưu review.
- **Nếu lượt này ra finding Ở MÃ:** DỪNG, lập bảng lớp, hỏi chủ kho (E2 hoặc E3). Phải có lượt executor mới (Fable 5.2: hạn mức mở lại 2-12 08:00Z; credit API chủ kho nạp), lease mới hoặc gia hạn, và nâng trần Codex. Không tự vá.
- **Nếu lượt này lại quá hạn:** không tự gọi thêm. Hỏi chủ kho (E2).

### 2.3 Sau khi approve: push MỘT lần, mở PR draft
1. Đo lại numstat `git diff --numstat 6a4f52d c5d44c9`: 4 tệp, ≤ 500 dòng thêm. Ghi vào thân PR cùng hai SHA.
2. Push nhánh `claude/wp1466-r11-g3` từ bundle, MỘT lần. Retry tối đa 4 lần khi lỗi mạng. KHÔNG viết dấu bỏ qua CI trong commit message.
3. Mở PR **draft** vào `master`, điền theo mẫu PR của kho. Nêu:
   - đặc tả r11 và băm;
   - lease g4;
   - bản ghi các lượt review;
   - lớp P2 đã chuyển #1469;
   - lớp P3 đã đóng;
   - dòng `windows: <H> mien` (chủ kho miễn Windows, C3/E2, issuecomment-7058374374).
4. Theo dõi CI cho tới khi xanh. Đo bằng check run và nhãn job, KHÔNG dùng `get_status` kiểu cũ (CLAUDE.md đã ghi bài học này).
5. Chạy `kiem-merge` bằng mã của master trên H. **Khai ĐỦ đầu vào cho mọi cổng**, kể cả `--p3-offline` cho MỌI P3 còn mở; đo lại, đừng tin rc (chỉ thị chủ kho, chuyển qua Mission #1172).
6. Chủ kho audit exact-H (`human_audited`, E5) rồi TỰ merge. Phiên điều phối KHÔNG merge.

### 2.4 Sau merge
- **Ghi sổ land lên #1466.** Mặc định `landed: false` và liệt kê các mốc `not_measured` của §10.2.2. Phiên web không gọi được GraphQL, nên mốc Workflow definition phải nhờ chủ kho chạy `gh api graphql` theo mẫu một dòng cho `cmd` ở CLAUDE.md.
- **Báo phiên Mission #1172.** Hiện tại là `session_015Gtxrb3cuZ7Nm935R8yA5W`; kiểm lại trước khi gửi.
- **Việc kế nhiệm:**
  - Issue #1469 phải nhận thêm nợ `INV-KHOA-BAN-SAO-DINH-CHU`; cập nhật thân Issue và nêu thẩm quyền E3 (issuecomment-7201538748).
  - #1470: khi land thì báo Mission để gỡ `kiem_verdict_lop.py`.
  - #1484 chạy độc lập.
  - wp1507 (#1507) chuyển sang ADR-0069 và rebase sau khi wp1466 land.
- **Dọn dẹp:** việc xoá nhánh lease cũ và nhánh `ops/wp1466-*` để chủ kho hoặc DON-RAC quyết; KHÔNG tự xoá.

## 3. Câu còn mở cho chủ kho
| # | mã | nội dung | khuyến nghị |
|---|---|---|---|
| Q5 | E2 | Đo bổ sung trước review. Đã được gộp vào lượt xác nhận hẹp ở 2.2 (việc thứ hai). | đóng khi lượt 14 chạy xong |
| Q6 | E5 | Handoff lượt 4 do Opus 5.5 viết trên log của Fable 5.2; toàn bộ mã của H do Fable 5.2 viết. | ghi nhận trong comment audit |
| — | E5 | Executor lượt 1 đã đi vòng qua chốt "sensitive file" của harness bằng git plumbing (`hash-object`, `update-index`, `checkout-index`). Từ lượt 2 trở đi không còn dùng cách này. Reviewer xác nhận H chỉ chạm 4 tệp của write set, không có dấu vết ngoài phạm vi. | chủ kho xét khi audit |

## 4. Bẫy đã trả giá ở packet này (đọc trước khi lặp lại)
- **Bia mộ lease phải có mặt trên MỌI ref.** Bản lease cũ chưa có bia mộ ở nhánh gốc vẫn được `ai-dang-giu` đếm là đang giữ write set.
- **Chuỗi trong backtick trong protocol bị `doc-claims-check` đọc thành con trỏ.** Lớp L12 đọc `rNNN_…` thành tên ca; lớp L8 đọc `tl <lệnh>` thành lệnh. Hễ thêm chữ vào protocol hay ADR là phải chạy `doc-claims-check --strict` trên H.
- **Lời hứa trong ADR hay đặc tả phải đúng bằng phép đo.** Đã mất hai vòng vì hai câu: "ở chỗ hiển thị bất kỳ", và "cổng xanh / cấm ca đỏ".
- **Nâng trần kích thước phải chép NGUYÊN khối `nang_tran` vào lease.** Diễn đạt lại khối ấy là một finding.
- **Giới hạn thời gian và chi phí của executor.**
  - Tác vụ nền bị cắt ở 2 giờ.
  - `claude -p --resume` một phiên có ngữ cảnh lớn tốn rất nhiều ($89 một lượt) và chạm giới hạn 500k token/phút. Ưu tiên phiên MỚI có prompt hẹp.
- **Lượt review Codex rộng dễ quá hạn.** Lượt 2 chạy quá 115 phút. Hãy giữ phạm vi hẹp và đặt hạn rõ ràng.
- **Đọc tệp của trình chạy test trước.** `pretooluse_guard_test` và một số bộ khác đỏ sẵn trong container. Luôn đo delta với base trước khi gọi một ca đỏ là hồi quy.
