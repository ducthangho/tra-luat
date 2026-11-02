# Review offline ĐẶC TẢ packet — lượt 3

Bạn là reviewer độc lập. Thư mục làm việc là một clone của kho `ducthangho/tra-luat` ở commit
`4a508277b3c8c04e2c62ee6e229aa6d33039be9d`. Thứ định danh tệp là BĂM, không phải tên nhánh.
Đối tượng review: `ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md`
(sha256 `a6a78fdeb6a625e4469e1b9f8d69662dedcc5fb53a04040a722a962552a73e2c`).
Bối cảnh: `ops/specs/CI-LAN-LUU-TRU-r1.md` (packet tiền nhiệm #1113, tiêu chí A12),
`ops/ci_duong_nhanh.py`, `ops/ci_duong_nhanh_test.py`, `.github/workflows/ci.yml`,
`.claude/dev/ci_dang_ky_test.py`, `docs/PROTOCOL_DA_PHIEN.md`, `.claude/skills/soan-spec/SKILL.md`
(luật L1–L6). Nguồn số canary: `git show origin/claude/ghi-so-land-1113:ops/land/pr1128-wp1113-provenance/readback-jobs-41371625809-canary-a12.json`
và `...:ops/land/pr1128-wp1113-land-evidence.yaml`. Các ref `origin/*` đã có cục bộ; KHÔNG có mạng.

Sandbox chỉ đọc: được chạy lệnh đọc (`git show`, `grep`, `python -c` không ghi tệp), không sửa gì.
Đừng chạy cả bộ `ops/ci_duong_nhanh_test.py` (dài, cần ghi tệp tạm). Hướng thử nào cần dựng nội dung
nhạy cảm thì mô tả bằng lời.

Soi theo LỚP lỗi, mỗi lớp ghi rõ đã kiểm gì (kể cả khi không thấy lỗi):

1. **Số liệu (L1/L5).** Đo lại mọi con số kiểm được từ kho: 113 ca, 419 đột biến, 5 mẫu rc + 3 đột biến tự kiểm,
   1159 s / 966 / 636 / 303 / 193 / 27 s từ JSON canary. Kiểm SỐ HẠNG, không chỉ quan hệ.
2. **Write set (L2).** Mọi mục §2 có thực hiện được chỉ trong ba tệp §3 không? Đặc biệt: bảng ghim
   `KHUNG_BUOC`, `RUN_BUOC_PACKET`, `TAP_CHO_PHEP`, `BUOC_HARNESS`, các ca `y*`, `BAM_GATE_*` trong
   `.claude/dev/ci_dang_ky_test.py`, `ops/cong_cu_test.py`, `ops/lease_publish_test.py` — thêm khối `env:`
   vào bước harness có làm lệch ghim/băm nào nằm NGOÀI write set không? Bộ đột biến hiện có có đột biến
   được `ci.yml` không (M6/M7)?
3. **Tiêu chí có thể đỏ (L3/L6).** Với từng A1–A11: phép đo nào làm nó đỏ, có cách nào xanh mà không đo gì?
   Tiêu chí khớp chuỗi có vế dương + vế âm chưa? A1 có thật sự chặn bản vá tắt đột biến ở đường đầy đủ không?
4. **An toàn của đường nhanh.** Có đường nào `che_do=duong_nhanh` mà diff đổi được mã harness/bộ phân loại/
   `ci.yml`? Giá trị env có fail-close đủ chưa? Tiến trình con thừa kế biến (C3) — còn chỗ gọi con nào bị sót?
   Push master và `workflow_dispatch`: output `che_do` có luôn được đặt không?
5. **Khả thi của A6 (tiền-canary).** PR có base là một nhánh KHÔNG phải master: `chuan-bi`/`ops/ci_duong_nhanh.py`
   có phân loại nó thành `duong_nhanh` không, hay luôn `day_du`? Nếu không khả thi, đề xuất cách đo thay thế.
6. **Mâu thuẫn nội tại / thứ tự với #1132** (lease `ci-concurrency-master`, nhánh `origin/agent/wp1132-g1-claude`
   sửa cùng hai tệp): đặc tả có chỗ nào sẽ gãy sau khi #1132 land không?

Đầu ra (stdout): danh sách finding, mỗi finding `[Pn] tiêu đề — tệp:dòng — bằng chứng đo được — đề xuất`.
Dòng cuối cùng đúng dạng: `VERDICT: approve|request_changes P0=a P1=b P2=c P3=d`.

## Lượt 3 — thêm
Lượt 1 (`caa22e5`) 0/1/4/0, lượt 2 (`53c6579`) 0/0/2/0; nguyên văn verdict lượt 2 dán dưới (verdict lượt 1 đã được
lượt 2 xác nhận đóng đủ năm). Diff: `git diff 53c6579 4a50827 -- ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md`.
Việc: (1) từng finding lượt 2: ĐÃ ĐÓNG / CHƯA ĐÓNG kèm bằng chứng; (2) lỗi MỚI do bản sửa lượt 3 sinh ra (C3(d), M9b,
ΔM ≥ 10, bỏ M5). Đặc tả đã lặp hai lần hình dạng "phản chứng đo một đường khác đường được tuyên bố" — soi riêng
lớp này trên MỌI ca C1–C4 và MỌI đột biến M1–M10/M9b: với từng cái, ca đích có thật sự đi qua dòng mã bị đột biến không.

### Verdict lượt 2 (nguyên văn)
Review neo tại `53c65791e544e931fe6b8dce8760ffd6bcf97677`, tree `2d789baa4ce5781522c97b95fb9ef24a8610473d`. SHA-256 đặc tả khớp `a9c8b6073ff4134498b3624e8e13a8b5a004a1a0adf4e11dda2f5412e660eaaa`. Vai trò: reviewer offline, `openai_codex / codex_cli / machine`; sandbox chỉ đọc, không truy cập mạng.

1. **[P2] C3 chưa đo đường ngoại lệ cần `finally`** — `ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md:52` — Mục 2 yêu cầu khôi phục env cả khi `main` ném, nhưng C3(c) chỉ cho **ca giả** ném. Probe trên runner thật cho cả `TinHieuChotCa` và `RuntimeError`: ca được gọi đúng một lần, `main` trả **rc 1**, in `TONG: DO`, **không ngoại lệ nào thoát khỏi `main`**. Ngược lại, cho `tu_kiem_phan_hang` ném thì ngoại lệ thoát thật. Vì vậy, triển khai khôi phục env chỉ trên đường trả về bình thường vẫn qua phản chứng hiện được yêu cầu; M9 xóa hoàn toàn khôi phục cũng không phân biệt được hai cách triển khai này. **Đề xuất:** bổ sung vào C3 một helper giả ném ngoại lệ xuyên qua `main`; bắt đúng ngoại lệ ở ngoài, kiểm sentinel được gọi và env được khôi phục. Đột biến tương ứng chuyển khôi phục khỏi `finally` sang đường thành công phải làm ca đỏ. Giữ riêng kiểm tra ca `DO/HONG`, tránh đổi cơ chế phân hạng hiện có.

2. **[P2] Nhánh cho phép giữ M5 mâu thuẫn nghiệm thu mọi đột biến phải bị giết** — `ops/specs/CI-DUONG-NHANH-BO-DOT-BIEN-r1.md:59` — Nhận định M5 tương đương là đúng trong đường C3(b): sau khi biến đã bị gỡ khỏi `os.environ`, probe gọi **`chay_con` thật**, spy ghi **1 lời gọi**; thêm hay bỏ thao tác gỡ riêng khỏi env con tạo hai mapping **bằng nhau**. Tuy nhiên, dòng 59 vẫn cho giữ M5 nếu có thao tác gỡ riêng; A1 dòng 77 tính M5 vào ΔM khi giữ, còn A5 dòng 81 bắt mọi đột biến mới đạt `GIET`. Khi ấy M5 sống đúng nghĩa lại làm A1/A5 đỏ. **Đề xuất:** quy định M5 tương đương không nằm trong `DOT_BIEN` và không tính ΔM; nếu muốn lưu làm tự kiểm, dùng tập riêng với kỳ vọng `SONG_SOT`. Chỉ cho đưa lại vào tập bắt buộc giết khi có một cửa thực thi riêng và phản chứng chứng minh nó không tương đương. Không nới A5 để chấp nhận đột biến sống nói chung.

**Đối chiếu từng finding lượt 1:**

| Finding cũ | Kết luận tại đặc tả lượt 2 | Bằng chứng |
|---|---|---|
| P1 — C3 đo sai cửa thực thi | **ĐÃ ĐÓNG lỗi gốc; bản sửa sinh khoảng trống mới ở finding 1** | Dòng 47–52 chuyển cô lập sang `os.environ`, giữ chế độ lượt ngoài, đo ca cùng tiến trình và gọi `chay_con` thật với số lời gọi dương. |
| P2 — thiếu bảng ngoại lệ `y04` | **ĐÃ ĐÓNG** | Dòng 53 yêu cầu thêm đúng mục vào `Y04_ENV_BUOC_CHE_DO`, giữ so toàn mapping. |
| P2 — nền 113/419 bỏ sót #1132 | **ĐÃ ĐÓNG** | A1 đo exact base, bảo toàn tập tên. Đo lại HEAD: **113/419**; `024212c1f565858788edc0b3e48fdf8a356ac8b4`: **114/421**. |
| P2 — dispatch sau merge thay push | **ĐÃ ĐÓNG** | A11 buộc dispatch hoàn tất trước merge; push bị hủy giữ `not_measured`. Probe dispatch diff rỗng trả **`day_du`**. |
| P2 — tiền-canary thất bại vẫn đạt A6 | **ĐÃ ĐÓNG** | A6 thêm run/check `success`, `CA: N/N`, `TONG: DAT`, đúng M và loại thời lượng thấp do lượt thiếu/hủy/thất bại sớm. |

**Đã kiểm sáu lớp yêu cầu:**

- **Số liệu L1/L5:** đo lại ngày 02-11-2026, khoảng 02:12 UTC. HEAD có **113 ca, 419 đột biến, 5 mẫu rc, 3 đột biến tự kiểm**; trong đó **84 đột biến `ci.yml`**. JSON canary có **16 job, 1159 s**; `gate-ops` **966 s**, harness **636 s**, biên nhận **303 s**, phần còn lại **27 s**; 15 job khác **193 s**. Phép cộng S5 ra **610 s**. S4 là số đo lịch sử, **chưa tái đo**.
- **Write set L2:** không thấy yêu cầu bắt buộc sửa ngoài ba tệp. `KHUNG_BUOC` và ngoại lệ `y04` nằm trong write set; `RUN_BUOC_PACKET`, `TAP_CHO_PHEP`, `BUOC_HARNESS` giữ được vì tên/run không đổi. Hai `BAM_GATE_*` đo lại đều khớp, băm các job khác. Đã đối chiếu các cửa đọc workflow trong `cong_cu_test.py` và `lease_publish_test.py`; chưa thấy ghim ngoài write set bị env mới tác động. M6/M7 dùng được cơ chế đột biến YAML hiện có. Một số neo đột biến cũ chứa nguyên stanza harness cần rà lại khi thêm env, vẫn sửa được trong tệp test.
- **Nghiệm thu L3/L6:** bảng dưới ghi từng A. Hai khoảng trống mới nằm ở C3 và quy tắc giữ M5.
- **An toàn đường nhanh:** probe Git giả cho diff đổi harness, bộ phân loại hoặc `ci.yml` đều trả **`day_du`**. So env chính xác cùng C1 đã bao phủ vắng/rỗng/sai chữ hoa/khoảng trắng/giá trị lạ/không phải chuỗi. Workflow phân loại cả push và dispatch; output có fallback `day_du`. Cô lập toàn tiến trình bao phủ cả các lời gọi con trực tiếp, nếu giữ hiệu lực suốt lượt chạy.
- **Khả thi A6:** PR base khác master, chỉ thêm `ops/land/probe.md`, được phân loại **`duong_nhanh`**, không truy vấn `origin/master`. Vì vậy mô hình PR lồng khả thi về bộ phân loại; Actions thật **chưa đo**.
- **Thứ tự #1132:** diff concurrency không xung đột trực tiếp với env harness. Công thức theo exact base và bảo toàn tập tên đã xử lý tăng nền. **ΔM ≥ 9 khớp** M1–M4 cộng M6–M10; với nền nhánh #1132 hiện có, mức tối thiểu là **118 ca/430 đột biến**, khi bỏ M5.

| Tiêu chí | Phép làm đỏ / kết luận |
|---|---|
| A1 | Thiếu marker đầy đủ, sai N/M, ca đỏ hoặc mất tên base làm đỏ. Kết hợp C2 đếm lời gọi, chặn việc tắt đột biến ở đường đầy đủ. |
| A2 | Phải đạt toàn bộ A1 với env `day_du`; không chỉ so tổng đếm. |
| A3 | Có vế dương `BO QUA`, N/M, `TONG: DAT`, rc 0; có vế âm `bi giet`. |
| A4 | Ca mới xanh trên base làm đỏ; `HONG` chỉ được chấp nhận vì thiếu hàm như đã nêu. |
| A5 | Đột biến sống hoặc tín dụng giả làm đỏ; nhánh giữ M5 mắc finding 2. |
| A6 | Run/check thất bại, thiếu log dương, sai N/M hoặc vượt thời lượng làm đỏ. |
| A7 | Finding actionlint mới hoặc thiếu công cụ làm đỏ; khi đo cần ghi OID thực tế của `origin/master`. |
| A8 | Tệp ngoài write set hoặc quá 150 dòng thêm làm đỏ. |
| A9 | Delta mới, registry đỏ hoặc băm lệch làm đỏ. |
| A10 | Audit/CI không thành công hoặc thiếu output đột biến đầy đủ làm đỏ. |
| A11 | Từng run phải đủ check/log/thời lượng; push bị hủy không còn được thay bằng dispatch không tương đương. |

Về các tương tác mới: `t91` và `t93` hiện tại đã chạy chọn lọc đạt. Đọc đường gọi `t97`, `--nguon-test`, `--mot-ca` không cho thấy việc gỡ **riêng biến chế độ harness** tất yếu phá chúng; phải giữ `CI_DUONG_NHANH_CAY` và cách nạp nguồn đột biến. Yêu cầu “`t93` dưới env nhanh” cần được đo qua cửa thực thi đã cô lập, không gọi trực tiếp thân `t93` trong env nhanh rồi mặc nhiên coi đó là `main` lồng.

Trần **150 dòng thêm** vẫn có khả năng đạt nhưng chặt. Kích thước đo được: `main` **52 dòng**, `t91` **30**, `t92` **15**, `t93` **40**, `t97` **23**. Ước theo các khuôn này: tách helper để tránh thụt lại toàn thân `main` có thể giữ tổng quanh **140–150 dòng**; bọc trực tiếp và viết các fixture riêng dễ lên **170–190 dòng**. Đây là ước lượng, chưa phải numstat của bản triển khai.

Các probe kiểm kê, phân loại, băm, ngoại lệ và tám ca chọn lọc hoàn tất **rc 0**. Script đọc canary lần đầu **rc 1** vì giả định sai hình dạng JSON; đã sửa bộ đọc và đo lại thành công. Toàn suite, mutation suite, lint và CI **not_run**. HEAD/tree không đổi; trạng thái cuối sạch, kể cả untracked/ignored.

VERDICT: request_changes P0=0 P1=0 P2=2 P3=0
