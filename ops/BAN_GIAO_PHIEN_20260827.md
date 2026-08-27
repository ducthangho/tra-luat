# BÀN GIAO PHIÊN — 27-08-2026, điều phối #318 · #319 · #334

Phiên trước chạy hết ngân sách ngữ cảnh. Tệp này là **nguồn có thẩm quyền** cho phiên sau.
Đừng tin trí nhớ hội thoại; đọc ở đây, rồi **ĐO LẠI** trước khi dùng bất kỳ con số nào.

## 0. VIỆC ĐANG CHỜ NGAY

1. **PR #322 và #352 CHƯA MERGE.** Người giữ kho đã nói "merge xong rồi" **hai lần**; cả hai lần
   đo đều cho ngược lại. Đo lúc 09:34Z: `git ls-remote origin refs/heads/master` ⇒ `f715fc28`,
   không đổi; hai nhánh packet còn nguyên head; `refs/pull/322/merge` và `refs/pull/352/merge`
   vẫn tồn tại (⇒ PR còn MỞ). Blob `docs/GOI_AGENT_DA_NEN.md` trên master vẫn **y hệt base
   `c35ae1c`**, tức chưa có một dòng nào của 15 vòng vá.
   **Việc của phiên sau: đo lại, và nếu vẫn chưa merge thì nói thẳng lần nữa.** Đừng ghi "đã land"
   vào lease khi phép đo nói không — đó đúng bệnh phiên này bắt được bảy lần.
2. **Hai packet chờ số Issue của người giữ kho** (phiên KHÔNG mở Issue được, xem §4):
   - `MCP-GH-CONG-TU-CANH` — hồ sơ `ops/specs/mcp-gh-cong-tu-canh-packet-issue-nhap.md`.
     Write set `.claude/dev/mcp_gh_test.py` nay **NGƯỜI_GIỮ 0** ⇒ **cấp lease được NGAY** khi có số.
   - `CONG-NGOAI-WRITE-SET` — hồ sơ `ops/specs/cong-ngoai-write-set-packet-issue-nhap.md`.
     Phải chờ `.github/workflows/ci.yml` nhả: lease `ci-cong-idiom-ba-ten-exec-1r2` giữ tới
     **2026-08-28T03:40:00Z**.

## 1. Trạng thái ba packet

| packet | nhánh / head | verdict | ngân sách | còn gì |
|---|---|---|---|---|
| **#318** `DOCTRINE-RANH-GIOI-REVIEWER` | `claude/doctrine-ranh-gioi-reviewer-exec-1` @ `1c000495` | **approved** vòng 15 (`codex`), P1=0 P2=0 | 198/200, biên 2 | chỉ chờ merge (PR **#322**) |
| **#334** `MANG-SANDBOX-CODEX` | `claude/mang-sandbox-codex-exec-1` @ `667c7ed8` | **approved** vòng 4 (`claude`), P1=0 P2=0 | 318/320, biên 2 | chỉ chờ merge (PR **#352**) |
| **#319** `MCP-GH-CUU-HO` | `claude/mcp-gh-cuu-ho-exec-1` @ `f461413a` | `changes_requested`, 2 P1 | 900/900, biên 0 | **lease ĐÃ ĐÓNG SỚM**; hai P1 đã TÁCH sang `MCP-GH-CONG-TU-CANH`. KHÔNG land được. |

**#352 — bắt buộc kiểm trước khi merge.** Commit cuối là commit **RỖNG** mang dấu `[open-pr]`
(cách duy nhất kích hoạt `ops-open-pr.yml`). Nên head ≠ `reviewed_sha`. Hai phép kiểm:

```
git rev-parse 667c7ed8^{tree}   # 2bd7ec70da37adcebc418d68a7b871c71750b31e
git rev-parse 94474286^{tree}   # phải GIỐNG
git merge-base --is-ancestor 94474286 667c7ed8    # phải rc=0
```

## 2. Việc mở ra SAU khi #334 land — đừng làm sớm

Bằng chứng bốn tổ hợp (`network_access` **một mình** đảo cả ba kênh; `writable_roots` không đảo
kênh nào) sẽ nằm trên `master`, đọc được từ clone bất kỳ. Khi ấy mệnh đề thứ tám của
`docs/GOI_AGENT_DA_NEN.md` **đo lại được** và có thể lên `cơ chế đã xác minh — chiều MỞ`, phân bố
về `1/5/2/0/0`.

**Đó là packet MỚI, không phải sửa lén sau land.** Và tệp đã GHI SẴN đường quay lại — reviewer
vòng 14 xác nhận ở dòng 685-686. Hiện tại nhãn `chưa xếp được` là **ĐÚNG**, không phải tạm bợ:
reviewer vòng 14 chốt *"hạng đo trạng thái bằng chứng mà người đọc exact tree có thể kiểm, không
phải nhãn chân trị của thế giới bên ngoài."*

## 3. Lease đang mở của phiên này

Tất cả trên nhánh `ops/cap-lease-tach-314`.

- `doctrine-ranh-gioi-reviewer-exec-1r4-claude-20260826` — #318, hết hạn **2026-08-27T10:00:00Z**
  (SẮP HẾT). `reviewed_sha_required: 1c000495`, `da_dung: 198`.
- `mang-sandbox-codex-exec-1r2-codex-20260827` — #334, hết hạn 2026-08-28T06:20Z.
  `reviewed_sha_required: 94474286` (chưa cập nhật sang `667c7ed8` — commit rỗng, tree giống).
- `mcp-gh-cuu-ho-exec-1r6-codex-20260827` — #319, **ĐÃ ĐÓNG SỚM** lúc 04:20Z. Khối `DONG_LEASE`
  ghi đầy đủ. **Kho KHÔNG có đường thu hồi lease** (nợ `AG-T0-01B-thu-hoi-lease-chua-co-duong`);
  cách duy nhất là hạ `lease_expires_at_utc`. Comment đã đăng trên #319 **vẫn hiển thị hạn CŨ** —
  bản chiếu và bản có thẩm quyền LỆCH NHAU.

## 4. Ràng buộc HẠ TẦNG — đo được, đừng thử lại từ đầu

- **Proxy chặn MỌI lời gọi `api.github.com`, kể cả `GET`**: `403 "GitHub access is not enabled for
  this session"`. Hệ quả: KHÔNG mở được Issue, KHÔNG đăng được comment, KHÔNG merge được.
  **Cài `gh` KHÔNG cứu được** — `gh` gọi đúng endpoint ấy; chặn ở PROXY, không ở công cụ.
  Không có MCP GitHub trong phiên. Chỉ **git transport** còn đi được.
- **Đường vòng HỢP LỆ, dùng đi:** đẩy commit có `[open-pr]` trong thông điệp lên nhánh `claude/**`
  ⇒ `ops-open-pr.yml` mở PR hộ. Đẩy tệp vào `ops/leases/**` trên nhánh `ops/**` ⇒
  `ops-publish-lease.yml` đăng comment lease hộ (nó tự bỏ qua lease đã có `posted_comment_id`).
- **Executor `claude` KHÔNG ghi được `.claude/**`** — `Edit`/`Write` bị nền từ chối vô điều kiện
  (*"which is a sensitive file"*). `codex` ghi được. Ghi qua `Bash` cũng được, nhưng **ĐỪNG dạy
  executor đi vòng qua chốt của nền**. Cấp lease chạm `.claude/**` thì chọn executor `codex`.
- **Executor `codex` KHÔNG chạy được `codex sandbox` LỒNG** (`rc=101`) và sandbox của nó chặn cả
  ba kênh mạng. Reviewer `claude` thì chạy được. ⇒ Đừng giao phép đo về một cái hộp cho tiến trình
  sống trong hộp đó.
- **Executor `codex` TỪ CHỐI VIỆC** nếu thư mục làm việc không có hồ sơ packet có thẩm quyền
  (§13). **Phải đặt tệp lease vào thư mục brief trước khi phóng** — phiên này mất một lượt 214s
  vì quên.

## 5. Luật đã chốt trong phiên — đừng diễn giải lại

- `luat_dung_LAND`: **chỉ P1 chặn land**; `changes_requested` mà chỉ còn P2 thì land được nếu mọi
  P2 thành nợ CÓ TÊN. Không nâng P2 lên P1 để giữ packet mở; không hạ P1 xuống P2 để land.
- **Chạm trần ⇒ CẮT hoặc VIẾT NGẮN LẠI, KHÔNG nâng trần.** #319 đã nâng/đổi đơn vị **bốn lần** và
  con số mất hết ý nghĩa. r5 của #319 chốt trước: *"MÃ chạm 900 ⇒ TÁCH."*
- **Không làm yếu phản chứng để vừa ngân sách.** Thà báo "không vừa" còn hơn báo "vừa" bằng cách
  đo ít đi.
- **`S4` (master trôi) đã bắn NĂM lần trong hai ngày.** Xử: đo `merge-base --is-ancestor` + đo
  `numstat` trên ĐÚNG write set. Không chạm write set ⇒ **giữ `base_sha`** (§3.2 không liệt kê
  `base_sha` là thứ tạo revision).
- **Đo NGƯỜI_GIỮ trước khi cấp lease**, và **so hai nguồn ref bằng TẬP TÊN** (`comm -23`/`comm -13`)
  chứ không bằng `wc -l`. Nhưng xem §6 — con số ấy CAO HƠN sự thật.

## 6. Bệnh lặp — thứ đắt nhất phiên này học được

**"Vá một chỗ hở rồi để lộ chỗ hở MỚI cao hơn một tầng."** Đếm được **bảy** lần:

1. #319 bộ chạy đột biến thiếu chốt duy-nhất;
2. #319 hai dòng hậu tố `ĐẠT`/`ĐỎ` không có đột biến canh;
3. #334 chốt duy-nhất không có phản chứng;
4. #334 lớp canh chốt ấy (`t12`) không có phản chứng;
5. #318 vòng 12 — vá `N4` thì đẻ hồi quy `N1`;
6. #318 vòng 13 — vá xong thì dòng 678 khai một phép đo KHÔNG XẢY RA;
7. #318 vòng 14 — hạ nhãn mà quên nội dung mệnh đề vẫn khai "biết cơ chế".

**Cách chữa đã tìm ra, và nó KHÔNG phải thêm một tầng canh nữa** (reviewer #334 vòng 2 nói thẳng:
thêm tầng chỉ dịch vấn đề lên tầng kế): **xác minh từ một cổng NẰM NGOÀI write set của packet** —
vì kẻ sửa ba tệp trong write set không đồng thời sửa được cấu hình CI. Đó chính là packet
`CONG-NGOAI-WRITE-SET` chờ mở.

**Quy tắc soi bản vá rút ra:** sau khi vá, đọc lại **VÙNG KIA** — chỗ cách vài chục dòng — chứ
không chỉ vùng vừa gõ. Và **quét theo Ý, không theo DIFF**: phiên này bỏ sót một dòng hậu tố vì
chỉ soi diff.

## 7. Lỗi vận hành của phiên — đừng lặp

- `git commit -m "..."` với **dấu nháy kép** trong thông điệp tiếng Việt ⇒ vỏ shell đóng chuỗi sớm,
  **commit KHÔNG chạy** và push in "Everything up-to-date". Luôn dùng **heredoc trích dẫn**.
- **Heredoc KHÔNG trích dẫn** (`<<EOF`) làm shell thực thi cụm trong dấu huyền và thay bằng chuỗi
  RỖNG. `yaml.safe_load` vẫn in "YAML OK" — **cổng cú pháp xanh trong khi nội dung đã hỏng**.
  Đọc lại NỘI DUNG bằng `assert`, đừng chỉ kiểm cú pháp.
- **In kết luận vô điều kiện** (`echo "(rỗng = an toàn)"` sau một lệnh có thể không rỗng) — mắc
  **ba lần**. Đừng in nhãn kết luận không gắn với kết quả.
- Đột biến **theo SỐ DÒNG**, không theo chuỗi: chuỗi đích có thể xuất hiện hai lần (một lần là mã,
  một lần là dữ liệu trong bảng `MUTATIONS`). Theo chuỗi thì đánh nhầm chỗ — #334 mất một lượt.
- **Nhánh cục bộ tụt sau làm sai phép đếm NGƯỜI_GIỮ.** `git fetch --prune` + `update-ref` trước
  khi đo.
- **Không typing SHA đầy đủ bằng tay.** Phiên trước đã bịa một đuôi băm.

## 8. Báo cáo đã viết, chờ ai đó đăng lên GitHub

- `ops/BAO_313_ai_dang_giu_dem_sai_20260827.md` — HAI khuyết tật của `ai-dang-giu`, tái lập được:
  (A) dedup theo `(blob, đường dẫn)` chứ không theo `lease_id`, và `nguoi_giu` là `list` chứ không
  phải `set` ⇒ một lease_id in HAI LẦN khi hai ref lệch nội dung;
  (B) mỗi revision còn hạn tính thành một người giữ riêng ⇒ `packet_loop.py` ra `NGƯỜI_GIỮ 4`
  trong khi sự thật là **2**. Gốc: schema lưu cùng một sự thật **hai chiều** và chiều dư trôi lệch
  (3/7 bản trượt). Hướng sửa: **suy** `da_bi_thay_the` từ chuỗi `thay_the_cho`.
- `ops/land/SAN_SANG_LAND_318_334_20260827.md` — hồ sơ land hai packet.
- `ops/DONG_LEASE_MCP_GH_CUU_HO_r6_20260827.md` — bản ghi để `grep` ra việc đóng lease sớm.

## 9. Biên nhận review của phiên (đủ băm, trên `ops/cap-lease-tach-314`)

`ops/reviews/`: `doctrine-ranh-gioi-reviewer-review-{11..15}-codex-verdict.*` ·
`mcp-gh-cuu-ho-review-4-claude-verdict.*` · `mcp-gh-cuu-ho-kiem-doc-lap-*` ·
`mang-sandbox-codex-review-{1..4}-*-verdict.*`
