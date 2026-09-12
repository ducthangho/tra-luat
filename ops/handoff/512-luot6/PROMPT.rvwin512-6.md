# Cross-review PR #512 (WINDOWS-LEASE-SUITE, lease #504) · **lượt 6** · reviewer KHÁC NỀN với tác giả · **finding PHÂN THEO LỚP**

Năm lượt trước là của CHÍNH BẠN. Head **`353eae10120da2a1788dcaf7a906fe46261bd71b`**, base **`015ffcc09d76fbc9cdfbc3d2ee0735c3ead8d364`** (= `origin/master`). Diff PR = `git -C cay-kho diff origin/master...HEAD` (BA chấm, 2 tệp). Bản vá lượt này = `git -C cay-kho diff c3bcfa1 353eae1`, gồm **hai** commit: `a15f302` (áp HINT lượt 5) và `353eae1` (merge master, KHÔNG chạm write set — kiểm đi).

HINT lượt 5 (`nguon/HINT.rvwin512-5.patch`, sha256 `9087726521c621617de5dc9fc40eab5e0f302f928662d23a8c62d47e81b47cdc`) đã áp nguyên văn.

**Bản vá lượt này là một phép XOÁ.** Tầng chạy lại toàn suite mà lượt 4 thêm vào đã bị **bỏ hẳn**, vì chính nó tái tạo ba chốt của suite (F1 nhóm tiến trình · F2 tee · F4 ngân sách tổng) và làm `t160` chỉ đo hàm thuần (F7). Câu hỏi trung tâm của lượt này: **bỏ tầng ấy có đóng thật bốn lớp, hay nó chỉ dời chỗ hở — và cái giá "không còn phân biệt được nguyên nhân" có bị khai nhẹ hơn thực tế không?**

## Việc của lượt này — SÁU việc

1. **ĐỐI CHIẾU** bảy lớp (F1…F7), mỗi lớp **một** trạng thái canonical tại HEAD này (ĐÃ VÁ THẬT / VÁ HỜ / VÁ SINH LỖI MỚI / CHƯA VÁ), cộng bảng thể hiện. Năm thể hiện còn mở của lượt 5 — **F1.4, F2.2, F4.4, F7.1, F7.2** — phải được điểm danh từng cái, kèm phép đo độc lập.
2. **ĐO là tầng chạy lại đã đi THẬT.** Đừng tin `git diff`: tìm bằng hành vi. Còn đường nào trong `t125` (hoặc ca nào khác) sinh một lượt toàn suite **không** đi qua `_mo_con_nhom_rieng` / `_theo_duoi_va_in` / `_chay_day_lenh_trong_ngan_sach` không? Còn `subprocess.run` hay `PIPE` nào ở đường A/B không? Nếu F1/F2/F4 đã đóng theo KIẾN TRÚC thì phải có phản chứng: đột biến nào **tái sinh** được tầng ấy mà suite vẫn xanh?
3. **ĐỘT BIẾN lớp mới — `_phan_loai_lech_ab` + consumer ở `t125` + `t160`.** Tác giả khai 3 đột biến mới (M15 classifier trả `KHỚP` khi lệch · M16 consumer bỏ classifier · M17 consumer nhận `LỆCH_CHƯA_RÕ` là đạt) và cả ba GIẾT THẬT. **Kiểm lại, rồi đi xa hơn:** có đột biến nào ở chỗ NỐI DÂY mà `t160` **không** bắt được? Ví dụ để hỏi, không phải để chép: đổi thứ tự hai đối số của classifier; làm consumer đọc `thong_diep` nhưng bỏ `ket_luan`; cho `t160` bịa dữ liệu KHỚP nên nhánh lệch không bao giờ chạy; làm parser ở `t125` trả cùng một giá trị cho hai vế bất kể đầu vào. Lượt 5 đã bắt được **năm** mutant wiring sống — đừng cho rằng lần này hết.
4. **Soi phép ĐÁNH ĐỔI đối kháng.** Tác giả khai thẳng: bản vá **không** phân biệt rò actor với ca chập chờn, và gọi đó là "thay một lời khai nhân quả không đo được bằng một lời khai không biết". Hỏi ba câu: (i) `LỆCH_CHƯA_RÕ_NGUYÊN_NHÂN` có thật sự làm **mất dấu** một lỗi thật không — hay nó giữ đủ bằng chứng trong thông điệp để người đọc log truy được? (ii) thân thông điệp có **liệt kê đủ** các nguyên nhân chưa loại trừ, hay nó bỏ sót một nguyên nhân mà chính bạn nghĩ ra được? (iii) một ca chập chờn thật sẽ làm `t125` đỏ ở CI — **đó là fail-close hay đó là một cổng đỏ oan?** Nếu bạn cho là đỏ oan thì nó là P1 và phải nói rõ tần suất kỳ vọng.
5. **Cổng + lời khai neo dòng.** `nguon/suite-luot6-linux.log` (155/155 ở CHA và cả hai vế A/B) và `nguon/dotbien-16-linux.txt` (16/16 giết thật, 0 tín dụng giả). Mọi số trong `EVIDENCE.md` neo **số dòng** của log ấy — số nào lệch dòng đã neo ⇒ finding. Gói offline thật: `cong-cu/actionlint_1.7.7_linux_amd64.tar.gz`, sha256 `023070a287cd8cccd71515fedc843f1985bf96c436b7effaecce67290e7e0757`, khớp băm ghim trong `ops/cai_actionlint.sh`; chạy full wrapper bằng `AL_VER=1.7.7 AL_GOI=<gói> AL_DICH=<đích> bash ops/chay_lease_publish_test.sh`. `cong-cu/dotbien512.py` là catalogue của tác giả — **đọc nó như một công cụ nháp cần kiểm**, không như một phép đo đã tin được: hỏi nó một ca bạn biết trước đáp án.
6. **`S2` — tác giả tự khai đã vượt một điều kiện dừng suốt bốn vòng.** `EVIDENCE.md` mục cuối: `S2` = dòng thêm > 300, đo được **+1082**, vượt từ `8ffd062`. Việc của bạn ở đây là **KIỂM PHÉP ĐO, không phán xử thẩm quyền**: con số đúng không, neo đúng `base_sha` chưa, bảng theo head có tái lập được không, và **lời khai "không tự nâng" có khớp hiện vật** trong nhánh không. Nếu bảng sai hoặc lời khai rộng hơn phép đo thì đó là finding. Quyết định nâng trần thuộc chủ kho, không thuộc bạn và không thuộc tác giả.

## Bối cảnh bắt buộc đọc

`nguon/CI-e6feddb-gate-do-trich.md` — trích log job THẬT của lượt `gate (ubuntu-latest)` ĐỎ trên `e6feddb`. Lý do ĐỎ thật là mutant `S8-bo-deadline` sống sót (seam `KhoObject._con_thoi_gian`). **Gốc nằm trong `ops/lease_publish.py`, NGOÀI write set, và chạm vào nó là điều kiện dừng S3** — đừng ra HINT sửa mã sản phẩm; cho rằng gốc ở đó thì nói bằng lời và xếp riêng.

Cũng đừng đọc suite xanh trên Linux thành `A3` đạt: **không lượt Windows nào chạy trên head này**, theo chỉ thị chủ kho (không CI tay, full CI khi merge). Tác giả đã khai ở mục KHÔNG ĐO ĐƯỢC.

## Giới hạn

**CẤM đọc `cay-kho/CLAUDE.md`, `cay-kho/docs/PROTOCOL_DA_PHIEN.md`, `cay-kho/.claude/skills/**`, `cay-kho/AGENTS.md`.** Ngoại lệ: `cay-kho/docs/adr/0043-*.md`, `cay-kho/docs/adr/0044-*.md`, `cay-kho/ops/specs/WINDOWS-LEASE-SUITE.md`, `cay-kho/ops/specs/TRAN-VONG-REVIEW-LEN-BON*.md`, `cay-kho/ops/specs/QUY-TRINH-LAP-REVIEW-VA-DIEU-KIEN-DUNG*.md`. Được đọc tự do: `cay-kho/ops/**`, `cay-kho/.github/workflows/**`, `cay-kho/.claude/dev/**`, `cay-kho/scripts/tl.py`, `git log`/`git show`/`git diff`.

**CẤM tự soạn nội dung dạng đường dẫn thoát hoặc mã khai thác** — mọi phản chứng cần thiết đã nằm trong cây. Hướng thử nào cần soạn nội dung như thế thì **mô tả bằng lời** cho phiên điều phối viết.

**Read-only với `cay-kho/` ở mức git**; đột biến trong `scratch/luot1/`. Cuối lượt `git -C cay-kho status --porcelain` RỖNG và `git -C cay-kho log --oneline 353eae1..HEAD` RỖNG. **CẤM đọc ra ngoài thư mục hiện tại**; KHÔNG mạng, KHÔNG gọi GitHub, KHÔNG đăng comment. Sandbox từ chối `rm -rf` — dùng `mktemp -d` rồi cứ để đó. **Ghi `VERDICT.md` SỚM** rồi cập nhật, kẻo một lượt chết mất sạch; in `XONG VERDICT sha256=…` khi đủ.

## Thư mục (cwd)

- `cay-kho/` — clone từ mirror bare, detached `353eae1`, `core.abbrev 7`, 354 ref, KHÔNG nông.
- `cong-cu/` — `actionlint` 1.7.7 (binary + gói offline) · `dotbien512.py` (catalogue của tác giả).
- `nguon/VERDICT.rvwin512-{1..5}.md` · `HINT.rvwin512-{1..5}.patch` · `EVIDENCE.rvwin512-5.md` · `PROMPT.rvwin512-5.md`.
- `nguon/CI-e6feddb-gate-do-trich.md` · `nguon/suite-luot6-linux.log` · `nguon/dotbien-16-linux.txt`.
- `EVIDENCE.md` — lời khai tác giả, gồm mục KHÔNG ĐO ĐƯỢC và mục tự khai `S2`.
- `scratch/luot1/` — chỗ bạn đột biến.

## Xếp hạng — THEO LỚP

**P1**: cổng xanh dễ dãi hoặc đỏ oan; mất thu hồi thực tế; phản chứng không có răng (mutant sống / chết vì ngoại lệ vô can); lời khai thẩm quyền hay neo sai; **một cơ chế làm MẤT DẤU một lỗi thật**. **P2**: lời khai rộng hơn phép đo, nhãn sai, số bịa, vá được trong write set. **P3**: chữ nghĩa. `so_p1`/`so_p2`/`so_p3` = số **LỚP**; `so_the_hien` = tổng thể hiện.

Không còn P1 và P2 ⇒ **`approve`**. Còn P2 ⇒ `changes_requested` + `HINT.patch` cho ĐÚNG head này, **chỉ chạm hai tệp trong write set**. Đừng nâng hạng để kéo dài, đừng hạ hạng để kết thúc. Nếu bốn lớp thật đã đóng và không tìm được lớp mới thì **nói thế** — `approve` là kết luận hợp lệ khi phép đo cho ra nó.

## LƯỢT NÀY LÀ LẦN PHÓNG THỨ HAI — lần đầu CHẾT giữa chừng, và bạn KHÔNG được cho xem bản nháp của nó

Lần phóng đầu (run `cdeee323`, 09:45Z) chết lúc **10:00:30Z**, ~15 phút vào lượt, vì
container mất mạng: `codex_api::endpoint::responses_websocket: failed to connect to websocket:
IO error: Connection refused (os error 111)` rồi `Reconnecting... 3/5`. Ba phép đo cùng xác nhận
nó chết chứ không treo: PID không còn tồn tại · `VERDICT.md` đứng ở 09:54:09 · stderr có chữ ký
mất mạng. `run.json` vẫn khai `dang_chay` — đó là lời khai dối đã biết của công cụ, không phải
trạng thái thật.

Nó kịp ghi một `VERDICT.md` mang `verdict: in_progress` (mọi trường số còn `pending`) và một
`HINT.patch` dở. **Cả hai nằm ở `luot-chet-cdeee323/` và CỐ Ý KHÔNG đặt trong `nguon/`: đừng mở
chúng.** Lý do là kỷ luật đo, không phải bí mật — một bản nháp chưa có kết luận sẽ NEO bạn vào
đúng hướng nó đang đi, và lượt này cần một phép đo độc lập chứ không cần một bản xác nhận. Nếu
kết luận của bạn trùng nó thì trùng vì phép đo, không vì đã đọc.

**Thứ bạn ĐƯỢC dùng lại:** `scratch/luot1/` còn cây đột biến và script của lượt chết
(`mut512-*`, `make_hint.py`, `hint_catalog_check.py`, `al-n12`…). Đó là công cụ, không phải kết
luận — chạy lại, sửa, hay bỏ đi đều được. Kiểm lại bất cứ thứ gì bạn dùng lại: không có gì bảo
đảm chúng ở trạng thái hoàn chỉnh khi tiến trình bị cắt.

## Đầu ra

1. `VERDICT.md`: `verdict` · `reviewed_sha: 353eae10120da2a1788dcaf7a906fe46261bd71b` · `reviewed_base: 015ffcc09d76fbc9cdfbc3d2ee0735c3ead8d364` · `reviewed_files_sha256` · `model_tu_khai` · `review_round: 6` · `so_p1`/`so_p2`/`so_p3` · `so_the_hien` · `hint_sha256` · `previous_hint_sha256: 9087726521c621617de5dc9fc40eab5e0f302f928662d23a8c62d47e81b47cdc` · `## ĐỐI CHIẾU LƯỢT TRƯỚC` · `## BẢNG ĐO` (kể cả cái khớp) · `## Findings theo lớp` · `## Mutant đã chạy` · `## chua_do_duoc`.
2. `HINT.patch` — `patch -p0` từ gốc `cay-kho/`; tự `--dry-run` trước khi nộp và báo số hunk + số tệp trong verdict; không còn gì ⇒ 0 hunk kèm ghi chú.

Dòng cuối stdout: `XONG VERDICT sha256=<sha256 của VERDICT.md>`.
Bắt đầu lúc: 2026-09-12T10:11:45Z · hạn 60 phút. Lần phóng THỨ HAI (lần đầu chết vì mất mạng).
