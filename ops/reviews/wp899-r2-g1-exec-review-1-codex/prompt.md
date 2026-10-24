# Cross-review OFFLINE — packet #899 `wp899` (CI-PROVENANCE-REST-LOG, P-A), lượt 1, lớp **sensitive**

Bạn là REVIEWER độc lập (Codex/OpenAI). Executor là Claude. Không kế thừa context của executor; không gọi subagent; không
đăng gì lên GitHub; không đẩy git; không sửa bất kỳ tệp nào trong cây kho (`git status` phải sạch khi bạn xong). Mọi tệp bạn
tạo nằm trong `.review/` ở gốc workspace (đã có trong `.git/info/exclude`).

## Đối tượng review — định danh bằng BĂM, không bằng tên nhánh

| | |
|---|---|
| repo | `ducthangho/tra-luat`, workspace là bản clone tại đúng commit dưới đây |
| reviewed_sha (HEAD) | `f43ea20fafaee9596d8a5847534cb8489217df02` |
| base | `76cf4c51a6b1a5a0f30621c73f9a6f03e7e68138` (commit merge PR #895) |
| đặc tả | `.review-input/wp899-r2.md`, sha256 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707` — kiểm băm trước, rồi đọc TRỌN |
| write set | `ops/ci_provenance.py` · `ops/ci_provenance_test.py` · `.claude/dev/ci_dang_ky_test.py` (thêm đúng một mục `MOI`) |
| trần | ≤ 3 tệp / ≤ 700 dòng thêm (`git diff --numstat <base> HEAD`) |

Diff cần review: `git diff 76cf4c5 HEAD`. Tiền lệ cùng loại để so: `ops/land_evidence_nguon.py`, `ops/land_evidence_nguon_test.py`.

## Hiện vật executor đã đo (đọc như LỜI KHAI, tự đo lại cái nào đo được)

- `.review-input/a10/stdout.txt` + `.review-input/a10/out/` — đo LIVE A10 bằng REST trên run 39342960764. Bạn KHÔNG có mạng;
  coi đây là dữ liệu, không phải bằng chứng bạn đã đo.
- Executor khai: `python ops/ci_provenance_test.py` ⇒ `CA: 21/21 dat` · `DOT BIEN: 19/19` · `TU KIEM PHAN HANG: DAT (3 dot bien)`
  · `TONG: DAT`; `ruff check --select F` 0 finding; `doctrine-scan`/`adr-song` rc 0; numstat 1+284+393 = 678.
- Executor khai một LỆCH so với kỳ vọng A10 của đặc tả: job `chuan-bi` (118368688427) KHÔNG có dòng SHA checkout vì bước
  `actions/checkout@v4` của nó `skipped` trên `push` (`if: github.event_name == 'pull_request'` trong `ci.yml`), nên công cụ ra
  `not_measured` cho job đó — 13/14 job ra `b27fe85…`. Hãy phán: đặc tả kỳ vọng sai, hay công cụ sai.

## Cách làm — BẮT BUỘC

1. Tạo `.review/VERDICT.md` ngay đầu với `verdict: pending`, cập nhật dần.
2. Kiểm băm đặc tả, HEAD, base, write set, numstat.
3. Chạy các ca CÓ SẴN (`python -B ops/ci_provenance_test.py`, `--mot-ca <tên>`), và **đột biến BẢN VÁ** trên BẢN SAO TẠM
   (`python -B`, `PYTHONDONTWRITEBYTECODE=1`) để đo răng của từng chốt: một đột biến chỉ tính là giết khi ca đích chết bởi
   `TinHieuChotCa` của ĐÚNG ca đó. Bạn được viết script đo và đột biến trong `.review/`.
4. **Không tự soạn nội dung tấn công nhạy cảm** (đường dẫn thoát cây thư mục, chuỗi giả mạo credential…). Hướng thử nào cần thứ
   đó thì MÔ TẢ BẰNG LỜI trong verdict để phiên điều phối tự viết.
5. Review **theo LỚP** (V3 của đặc tả): mỗi biểu hiện khái quát thành một lớp nguyên nhân, rồi quét MỌI biểu hiện cùng lớp trên
   ứng viên trước khi báo. Ưu tiên: luật năm trạng thái (thiếu dữ liệu không bao giờ thành `passed`), SHA checkout từ log
   (không từ REST), marker chỉ trên phần log của chính bước, `MOI` một nguồn, ghi nguyên tử, mã thoát, REST giả có giữ trạng
   thái thật không, mutant có giết đúng lý do không, fixture có đúng là log thật cắt gọn không (so `BAM_FIXTURE`).
6. Đối chiếu từng A1–A11 của đặc tả: đạt / đỏ / `KHÔNG ĐO ĐƯỢC` (nói vì sao).

## Hạng

- **P0**: công cụ có thể sinh bằng chứng sai theo hướng có lợi (một mốc thiếu/lệch mà ra `passed`, rc 0 khi phải 12/3), hoặc
  rò credential.
- **P1**: vi phạm một mục tiêu M1–M9/tiêu chí A1–A11 có thể đo được; mutant/ca không có răng ở một chốt đặc tả đòi.
- **P2**: lỗi thật nhưng hẹp (biên đầu vào, định dạng lạ đã biết, nền Windows), hoặc ca test có mặt mà không đo.
- **P3**: nợ/chất lượng; phải kèm đề xuất quyết định (chấp nhận/vá) có căn cứ.

## Đầu ra — `.review/VERDICT.md`

Dòng đầu tiên: `verdict: approve` hoặc `verdict: changes_requested`, rồi `reviewed_sha: <40 hex>`, `base_sha: …`, và một dòng
`Reviewed commit: <40 hex>` (OID đầy đủ). Approve CHỈ khi P0 = P1 = P2 = 0 (V2).

Bắt buộc có **BẢNG LỚP**: `| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện (lệnh + output) | HINT patch |`. Mỗi HINT là
một đoạn diff hoặc mô tả thay đổi đủ cụ thể để vá trong một lượt, kèm ca/mutant khoá lại. Sau bảng: đối chiếu A1–A11, rồi
danh sách mutant bạn đã chạy kèm hạng (GIET / SONG_SOT / TIN_DUNG_GIA). Không ghi khẳng định nào bạn chưa đo; cái không đo
được thì ghi `KHÔNG ĐO ĐƯỢC`.
