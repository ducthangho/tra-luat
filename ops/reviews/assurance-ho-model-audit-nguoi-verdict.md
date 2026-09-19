# AUDIT CỦA NGƯỜI — `ASSURANCE-NEO-VAO-HO-MODEL` (#551 / PR #557), neo `13407c7`

**Tệp này là BẢN CHIẾU, không phải nguồn có thẩm quyền — và chiều ấy NGƯỢC với mọi verdict
khác trong thư mục này.**

Với verdict của một mô hình, nguồn có thẩm quyền là tệp có băm trong kho, còn comment trên
GitHub chỉ là bản chiếu. Với một lượt `human_audited` thì ngược lại: thứ §8 đòi là **danh
tính bền trên GitHub** của người audit, mà danh tính ấy chỉ tồn tại ở phía GitHub. Một tệp
trong kho không mang được nó — bất kỳ phiên nào có quyền ghi cũng tạo được tệp này. Nên
**nguồn có thẩm quyền là comment `5739262446`**; tệp này chỉ để tra ngoại tuyến.

- Người audit: `ducthangho` (chủ kho)
- **Đăng bởi: PHIÊN AGENT, đăng HỘ theo chỉ thị chủ kho** — **không** phải chủ kho tự gõ
- Đăng lúc: `2026-09-19T04:11:39Z`
- Nguồn: https://github.com/ducthangho/tra-luat/pull/557#issuecomment-5739262446

## Lượt này YẾU HƠN khuôn `PLAT-M4`, và khác biệt ấy phải đọc trước

Khuôn `human_audited` duy nhất trước đây (`plat-m4-human-audit-ducthangho-verdict.receipt.yaml`)
khai `tac_gia: ducthangho, author_association OWNER — không phải bot, không phải phiên agent`.
Lượt này **không** khai được câu ấy, và cũng đã **đo được rằng câu ấy không kiểm chứng được**:

Phiên agent đăng comment `5739262446`, rồi đọc ngược về qua API ⇒ phản hồi trả
`"user": {"login": "ducthangho"}` và `"author_association": "OWNER"` — **y hệt** một comment
chủ kho tự gõ. Nguyên nhân: phiên agent của kho chạy bằng credential chủ kho (kho đã ghi từ
`2026-08-26`: `get_me → ducthangho`).

⇒ `author_association` **không** phân biệt được người với phiên agent. Thẩm quyền của lượt
audit này neo vào **CHỈ THỊ của chủ kho trong phiên**, không neo vào tác giả comment. Nợ riêng
cho khuyết tật cơ chế này: **#566**.

---

## Nguyên văn (bản chiếu comment `5739262446`)

Chỉ thị chủ kho dẫn tới comment ấy, nguyên văn, phiên điều phối 19-09-2026:
*"Soạn verdict .md cho tôi ký đi"*, rồi *"Đăng hộ tôi luôn đi"*.

Phạm vi audit: `git diff 2aaf49f4..13407c7` — **6 tệp, +293/−18** — và đặc tả đóng băng
`ops/specs/assurance-neo-vao-ho-model-r4.md` (`sha256 050538d380d842cd…`).

Phép đo **do phiên agent chạy**; chủ kho chấp nhận chúng mà **không tự chạy lại**. Bộ đo chạy
trên máy chủ kho (Windows 11 / Python 3.13.1) cho **9/10 chốt khớp từng chữ** với số đo trên
Linux: `bien_nhan_v2` `131 ĐẠT v2 · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 184` (y hệt nền ⇒ `A3`) ·
`bien_nhan_v2_test` `63/63 ca · 74/74 đột biến CÓ RĂNG` · `adr-song` `49 → 50` ·
`release-verify` `ok=true, 180==180` · `doctrine-scan` · `doc-claims-check --strict` ·
`git diff --check` · `numstat` `6 tệp / +293`.

### Năm điều chủ kho chấp nhận TƯỜNG MINH khi ký

1. **`r330_deploy_msg_khong_chay_lenh` lệch chưa rõ nguyên nhân trên Windows.** Bốn lượt đo
   trên cùng một máy: nền `2aaf49f4` đỏ **2/2**, ứng viên `13407c7` đỏ 1 lượt và xanh 1 lượt.
   Hai tệp mà ca ấy đọc — `deploy-package.sh` (`693ef9a46dca7d9c`) và `.ps1`
   (`03bcccba890844e6`) — **giống nhau từng byte** ở hai vế; diff `tl_selftest.py` giữa hai vế
   đúng 13 dòng, toàn bộ là kê khai slot `r291`. Nên lệch **không** đến từ bản vá. Căn cứ ký là
   *ứng viên không tệ hơn nền*, **không** phải "đã xanh"; lượt xanh cuối cùng **không** được
   nhận làm bằng chứng đạt. Nợ riêng: **#565**.
2. **`S1` và `S2` đóng bằng SỬA ĐẶC TẢ, không bằng mã.** `M20` rút `M16`/`A16` vì chúng mất đối
   tượng khi packet bỏ `cross_approved`; `M21` sửa lời `A14` vì câu *"RỖNG ⇒ CHẶN"* rộng hơn mã.
   Chấp nhận rằng hai tiêu chí được **gỡ và viết lại**, chứ không phải được **thoả**.
3. **Xung đột lợi ích ở mức cao nhất của cả chuỗi packet.** Một phiên claude soạn **cả bốn**
   đặc tả, ghi hộ **cả bốn** lease, viết **cả ba** verdict, **và** là executor, **và** đăng hộ
   comment audit. Không còn vòng độc lập nào bằng máy.
4. **Kích thước vượt con số 250 mà gen 3 tự đặt.** Thực tế `+293`. Trần áp dụng là **300** theo
   `ADR-0044:5`; chủ kho chốt tại `issues/551#issuecomment-5734920075`.
5. **`cross_approved` KHÔNG đạt được, và chữ ký này THAY cho nó chứ không cộng vào nó.**
   `codex` hết quota review, `agy` hết quota, `claude` là executor ⇒ không còn bên thứ hai khác
   họ model.

### Chữ ký này KHÔNG được đọc thành

- **Không phải cross-review**, và không phải tiền lệ *"packet `sensitive` land được bằng chữ ký
  người"*. Packet khác phải tự chứng minh lại rằng đường `cross_approved` bị chặn.
- **Không phải một lượt `human_audited` đầy đủ theo khuôn `PLAT-M4`** — khuôn ấy đòi chủ kho
  **tự đăng**; lượt này đăng hộ.
- **Không đóng nợ `r330`** (#565), **không đóng** `AGY-CHUA-ATTEST-MODEL-TUNG-LUOT`, và **không
  đóng** khuyết tật cơ chế `human_audited` (#566).

VERDICT: approve
Reviewed commit: 13407c7bbf44ec2d1af49a013478a38e2824e6fc
