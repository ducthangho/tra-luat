# DON-REF-TEST-VAO-CI r1 — đưa phản chứng của `ops-don-ref.yml` vào CI qua sổ đăng ký
packet_id: DON-REF-TEST-VAO-CI-r1
revision: 1
tran_loi_goi_codex: ADR-0055@d2e3052d479d140b7e7b91df41ec4914fab7d544
tran_kich_thuoc_sensitive: ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab

Trạng thái: `proposed`, chưa đóng băng, chưa có lease. Đặc tả không cấp việc (protocol §3.2, §4).
Soạn 26-11-2026 trên `origin/master` `1260fa0cba89353911e2f97188b2c04dab8139d7` (đo 03:47:26Z), bởi một
phiên Claude Code trên web, qua skill `soan-spec`. Mọi giờ ghi cạnh số là UTC của 26-11-2026, trừ khi ghi
ngày khác. Đo lại trước mỗi bước công bố (đăng băm, cấp lease, merge).

Quyết định của vòng hỏi: chủ kho trả lời "Theo khuyến nghị" cho cả bốn câu Q1–Q4 trong phiên soạn đặc tả
(26-11-2026). Nội dung bốn khuyến nghị được chép thành các mục `muc_tieu`, `ngoai_pham_vi` và `pham_vi_e`
dưới đây; đặc tả này là bản ghi của chúng.

## 1. `packet_id` · `packet_issue`

| trường | giá trị |
|---|---|
| packet | `DON-REF-TEST-VAO-CI-r1`, revision 1, generation 1 |
| `packet_issue` | #1540 (`open`, đọc qua MCP lúc ~02:40Z) |
| mission | không |
| base | `origin/master` lúc cấp lease; phải là tổ tiên của `origin/master` lúc đó |

## 2. `nguon_cap_viec`

Không thuộc dòng kế hoạch nào. Nguồn: phát hiện khi lập hồ sơ land cho packet #1532 (PR #1537, merge
`c4d707e`): mốc Gate output §10.2.2 ra `not_measured` vì không log CI nào có dấu hiệu dương của
`ops/don_ref_chot_test.sh` — https://github.com/ducthangho/tra-luat/issues/1532#issuecomment-7180017463.
Issue #1540 ghi phát hiện và đề xuất; chủ kho giao phiên này mở packet.

## 3. `review_class`

`sensitive`. Packet chạm `.claude/dev/ci_dang_ky_test.py`: đây là mã của bước
`test registry (phạm vi + các bộ chưa được nối)` trong job `gate-registry`, một cổng chặn merge.
Không rõ hơn thì lấy mức chặt nhất (protocol §8, fail-closed).

## 4. Số đo nền (dùng để quyết, không phải để nghiệm thu)

Đo trên `origin/master` `4a96ccd` lúc 02:35Z; đối chiếu lại lúc 03:47Z với `1260fa0`:
`git diff --stat 4a96ccd 1260fa0` trên năm tệp `.github/workflows/ci.yml`,
`.claude/dev/ci_dang_ky_test.py`, `ops/don_ref_chot_test.sh`, `.github/workflows/ops-don-ref.yml`,
`ops/ci_provenance.py` cho kết quả rỗng.

- N1. `bash ops/don_ref_chot_test.sh` trong container: rc=0, dòng cuối `don_ref: 149/149 đạt (chốt + bước
  làm)`, thời gian tường 2,6 giây. Đơn vị của 149: phép kiểm (`QUA+HONG`) mà bộ test tự đếm.
- N2. Bộ test gọi `actionlint -shellcheck= -pyflakes=` (dòng 577), tức đã tắt shellcheck. Nó cần
  `actionlint`, **không cần** `shellcheck`. Issue #1540 ghi cần cả hai; câu ấy sai.
- N3. Job `gate-ops` **không** có `actionlint` trên PATH cho bước khác: chỉ `ops/chay_lease_publish_test.sh`
  tự cài cho tiến trình của nó. Chú thích đầu job ghi cố ý không thêm bước cài (`t152` đếm dòng `AL_VER:`).
  Job `gate-registry` thì có: bước `cài actionlint cho G5` gọi `ops/cai_actionlint.sh`, tệp ấy ghi
  `$GITHUB_PATH` (dòng 226).
- N4. Sổ `MOI` không nhận tệp `.sh`. `tim()` chỉ quét `*_test.py`; mục `MOI` nào không có trong tập ấy thì
  `kiem()` báo `mục đăng ký không có tệp`. Tệp `*_test.py` mức đỉnh của `ops/` mà không đăng ký thì
  `kiem()` báo `test sống chưa đăng ký`.
- N5. `ops/ci_provenance.py` chỉ chấm `passed`/`failed` cho bước gọi thẳng dạng `python <đường>.py`
  (`RE_LOI_GOI`, dòng 50) không có `env` chặn. 17 trên 18 mục `MOI` (đếm khoá của dict `MOI`, 02:40Z) chỉ
  chạy qua `python .claude/dev/ci_dang_ky_test.py --chay`, nên với `ci_provenance` chúng luôn ra
  `not_measured`. Hồ sơ land hiện đo mốc Gate output theo dấu hiệu dương từng bước bằng công cụ khác (vd.
  `ops/land/pr1378-wp1319-land-evidence.yaml`).
- N6. `_chay_co_lap` của sổ đăng ký giữ nguyên `PATH` của cha, đặt `cwd=ROOT`, chỉ đổi `TMPDIR/TEMP/TMP`
  (dòng 1304–1313). Nên `actionlint` mà bước cài đã đưa lên PATH sẽ thấy được trong bộ con.
- N7. `ai-dang-giu` lúc 02:35Z, sau khi so tập tên ref máy chủ với bản cục bộ (thiếu cục bộ: 0 ref):
  `NGƯỜI_GIỮ 0` cho `.github/workflows/ci.yml`, `.claude/dev/ci_dang_ky_test.py`,
  `ops/don_ref_chot_test.py`, `ops/don_ref_chot_test.sh`.
- N8. Ba phép đo hiệu lực của `ADR-0055` và `ADR-0053` cho cả hai OID dòng khai, trên clone **không shallow**
  (03:47:26Z): `cat-file -e <L>:<adr>` rc=0; `cat-file -e <L>^1:<adr>` rc=128; có trên
  `rev-list --first-parent origin/master` rc=0. Lần đo đầu trên clone shallow cho rc=1 ở phép thứ ba, nên
  phải bỏ shallow trước khi đo lại.

## 5. `write_set`

1. `ops/don_ref_chot_test.py` — tệp MỚI.
2. `.claude/dev/ci_dang_ky_test.py`
3. `ops/specs/DON-REF-TEST-VAO-CI-r1.md` — chính đặc tả này (đã đóng băng thì không sửa).

Hồ sơ review và lease (`ops/reviews/**`, `ops/leases/**`) đi theo đường của protocol, không thuộc write set
mã. Kích thước dự kiến: 3 tệp, dưới 300 dòng thêm tính cả đặc tả; trần `ADR-0053` là 6 tệp, 450 dòng thêm.
Vượt trần thì dừng theo `luat_dung`.

## 6. `ngoai_pham_vi`

- **Không sửa `.github/workflows/ci.yml`.** Đăng ký vào `MOI` thì bước `--chay` sẵn có của `gate-registry`
  chạy bộ mới (Q1).
- **Không dạy `ops/ci_provenance.py` đọc kết quả của `--chay`.** Khoảng trống ấy chạm mọi mục `MOI`, không
  riêng `don_ref` (N5). Ghi thành nợ có tên `CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY` và mở Issue riêng
  (mục tiêu M5). Thêm bước gọi thẳng vào `gate-registry` cũng không làm, vì job ấy khoá bằng
  `LENH_REGISTRY` và `BAM_GATE_REGISTRY` (Q2).
- **Không mở rộng sổ hay `ci_provenance` để nhận tệp `.sh`** (Q1, phương án (b)).
- **Không sửa `ops/don_ref_chot_test.sh`** và không port nó sang Windows. Nếu nó đỏ trên Windows thì cách ly
  (M4), không vá (Q3).
- **Không thêm khối đột biến tự chạy vào bộ `don_ref`.** 21 đột biến của #1532 là phép đo tay; đưa chúng vào
  CI là việc khác.

## 7. `muc_tieu`

| # | mục tiêu | đường dẫn |
|---|---|---|
| M1 | Wrapper `ops/don_ref_chot_test.py`: tìm `bash`, chạy `ops/don_ref_chot_test.sh` (đường dẫn tính từ chính tệp), `stdin=DEVNULL`, chuyển nguyên stdout/stderr, thoát bằng đúng rc của bộ con. Thiếu `bash` thì in `KHÔNG ĐO ĐƯỢC` và thoát khác 0. Ép stdout/stderr sang UTF-8 trước khi in. Không pipeline, không cắt bớt output. | `ops/don_ref_chot_test.py` |
| M2 | Thêm mục `MOI` cho `ops/don_ref_chot_test.py`, mẫu khớp TRỌN dòng tổng có hai nhóm bằng nhau và khác 0: `^don_ref: ([1-9]\d*)/(\1) đạt \(chốt \+ bước làm\)$`. | `.claude/dev/ci_dang_ky_test.py` |
| M3 | Thêm các ca tự kiểm (tiền tố `p1540-`) vào bộ ca của chính sổ đăng ký, đo M1 và M2 (mục 8). | `.claude/dev/ci_dang_ky_test.py` |
| M4 | Windows: trên nhánh packet, gọi một lượt `workflow_dispatch` của `ci.yml` với `runner_set=windows-only`. Mục `ops/don_ref_chot_test.py` của job `gate-registry` ĐẠT thì không làm gì thêm. Đỏ thì thêm vào `CACH_LY` một mục `moi_truong: github-actions/windows` có `slug` `don-ref-test-chua-chay-duoc-tren-windows`, `ly_do`, và `log` trỏ lượt chạy ấy. | `.claude/dev/ci_dang_ky_test.py` |
| M5 | Ghi nợ `CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY` trong chú thích ngay trên mục `MOI` của M2, và mở một Issue mô tả nợ ấy (dẫn N5). | `.claude/dev/ci_dang_ky_test.py` |

## 8. `nghiem_thu`

Mỗi tiêu chí kèm phép đo làm nó ĐỎ. Đo trên head của nhánh packet, trừ khi ghi khác.

| # | tiêu chí | phép đo dương | đột biến / điều kiện làm nó ĐỎ |
|---|---|---|---|
| A1 (M1) | Wrapper chạy bộ thật và giữ rc | `python ops/don_ref_chot_test.py` ⇒ rc=0, có đúng một dòng khớp mẫu M2 | Chạy với `PATH` không có `actionlint` (không sửa tệp nào): bộ con in `KHÔNG ĐO ĐƯỢC: thiếu actionlint` và `don_ref: 148/149`, rc=1 ⇒ wrapper phải trả rc≠0. Đột biến wrapper luôn `sys.exit(0)` thì ca `p1540-rc-giu-nguyen` ĐỎ |
| A2 (M1) | Thiếu `bash` là fail-close | ca `p1540-thieu-bash`: chạy wrapper với `PATH` rỗng (Python gọi bằng `sys.executable`) ⇒ rc≠0 và stdout có `KHÔNG ĐO ĐƯỢC` | Đột biến nhánh thiếu `bash` thành `sys.exit(0)` ⇒ ca ĐỎ |
| A3 (M2) | Mẫu chỉ nhận dòng tổng đủ | ca `p1540-mau`: `bang_chung_xanh` với `MOI[...]` nhận `don_ref: 149/149 đạt (chốt + bước làm)`; từ chối `don_ref: 148/149 …`, `don_ref: 0/0 …`, `don_ref: 149/149 đạt` (thiếu phần sau), và văn bản không có dòng ấy | Nới mẫu thành `don_ref: (\d+)/(\d+)` ⇒ ca ĐỎ ở vế `0/0`; bỏ neo `$` ⇒ ca ĐỎ ở vế hậu tố khác |
| A4 (M2) | Sổ đăng ký thấy wrapper | `kiem()` trả danh sách lỗi rỗng trên head | Xoá mục `MOI` ⇒ `test sống chưa đăng ký: ops/don_ref_chot_test.py`; xoá wrapper ⇒ `mục đăng ký không có tệp: ops/don_ref_chot_test.py`. Hai đột biến này chạy trên bản sao tạm của cây, không trên tệp thật |
| A5 (M2, M3) | Bộ ca của sổ đăng ký đạt toàn bộ | `python .claude/dev/ci_dang_ky_test.py` (không cờ; chạy `kiem()` rồi `phan_chung()`) ⇒ dòng `PHẢN CHỨNG: N/N đỏ đúng` với hai số bằng nhau, dòng `TỔNG: ĐẠT`, rc=0; N trên head trừ N trên master đúng bằng số ca `p1540-*` đã thêm | Bất kỳ ca `p1540-*` nào đỏ, hoặc số ca nền giảm |
| A6 (M2) | CI Linux có dấu hiệu dương | log job `gate-registry (ubuntu-latest)` của lượt PR trên head có cả `don_ref: N/N đạt (chốt + bước làm)` (N>0, hai số bằng nhau) và `CI_DANG_KY ops/don_ref_chot_test.py: ĐẠT`. Đọc bằng `get_job_logs` | Dòng vắng, hai số khác nhau, hoặc `ĐỎ`. **Chưa đo được** cho tới khi có lượt PR (mục 11) |
| A7 (M4) | Windows có kết luận | lượt `workflow_dispatch runner_set=windows-only` trên head: mục `ops/don_ref_chot_test.py` ra `ĐẠT`, hoặc ra `CÁCH LY` với `slug` của M4 | Mục ra `ĐỎ` mà không có `CACH_LY`; hoặc có `CACH_LY` mà lượt chạy ĐẠT (sổ đăng ký tự báo `đã xanh, hãy gỡ khỏi cách ly`). **Chưa đo được** cho tới khi gọi lượt ấy |
| A8 (M5) | Nợ có tên và có Issue | `rg -n 'CI-PROVENANCE-KHONG-DOC-KET-QUA-CHAY' .claude/dev/ci_dang_ky_test.py` ⇒ ≥1 dòng, trong khối chú thích ngay trên mục M2; Issue mới tồn tại và nêu tên nợ | Tên nợ vắng ở vị trí ấy, hoặc Issue không có. Vế âm "master chưa có tên này" phải ĐỎ trên nền (đo lúc soạn: 0 dòng) |
| A9 | Delta cổng chung = 0 | `python3 -m ruff check --select F` trên hai tệp `.py` bị chạm: số F trên head trừ số trên master = 0; `python .claude/dev/packet_loop.py doctrine-scan --root .` rc=0; `python scripts/tl.py --selftest` N/N bằng nhau; `actionlint` (có `shellcheck`) trên `.github/workflows/*.yml`: delta so master = 0 | Bất kỳ delta nào khác 0 |

Ghi chú về giới hạn của A1–A4: wrapper tự in một dòng `don_ref: …` giả thì mẫu M2 vẫn khớp. Không cổng nào
phân biệt được dòng do bộ `.sh` in với dòng giả; lời bảo đảm chỉ là review mã của wrapper. Ghi thẳng ở đây
để không ai đọc A3 thành "đã chống giả mạo".

## 9. `tran_*`

Hai dòng khai ở đầu tệp: `ADR-0055` (trần lời gọi Codex) và `ADR-0053` (kích thước `sensitive`). Không có
dòng `ADR-0052`. Không khai ngân sách mềm. Trước mỗi lời gọi Codex, đếm số đã dùng và đọc trần theo bảng
của `ADR-0055`.

## 10. `luat_dung`

- Điểm dừng của `docs/PROTOCOL_DA_PHIEN.md` §12, theo đúng ngưỡng ở đó.
- Trần lời gọi Codex của `ADR-0055` chạm thì dừng: **E2**, mang theo mức đã dùng, còn thiếu bao nhiêu, để làm gì.
- Diff vượt trần `ADR-0053` thì dừng: **E2**, mang theo số tệp và số dòng thêm đo bằng
  `git diff --numstat`, và khối `nang_tran` theo dạng ADR quy định.
- Lượt Windows (M4) không gọi được, hoặc hết phút CI: **E2**, mang theo lỗi gọi và số phút đã dùng.
- Thấy rằng muốn đạt A6 thì buộc phải sửa `ci.yml`: **E3** (đảo quyết định Q1 của chủ kho), mang theo bằng
  chứng và hậu quả nếu giữ nguyên.
- Một hình dạng lỗi lặp lại sau khi đã đổi thiết kế: **E1**.

## 11. `pham_vi_e`

- **E5: chạm.** `.claude/dev/ci_dang_ky_test.py` là mã của một cổng chặn merge; `ADR-0067` coi việc không rõ
  là thuộc. Hệ quả: chủ kho duyệt băm đặc tả, chủ kho audit, chủ kho merge.
- **E4: không chạm.** Packet không xoá ref, không đẩy Package, không đọc hay ghi secrets, không đổi ruleset.
  Lượt `workflow_dispatch` của M4 chạy `ci.yml` trên nhánh packet, chỉ đọc; hoàn tác được bằng huỷ lượt.

## 12. `hinh_dang_ke_thua`

`khong_ap_dung`. Đây không phải packet khắc phục của một lượt review. Nguồn là phát hiện khi land #1532; hồ
sơ #1532 không ghi hình dạng lỗi nào cho chỗ trống này.

## 13. `chua_do_duoc`

- Wrapper chạy trong `--chay` với `actionlint` của bước cài: suy từ N3 và N6, **chưa chạy thật**. Phiên soạn
  định dựng thử nguyên mẫu trong một bản clone tạm, nhưng lệnh bị từ chối quyền và không chạy lại. Đo ở A1,
  A4, A5 khi thi công; đo trên runner ở A6.
- Bộ `don_ref` trên Windows: chưa từng chạy (Q3). Kết luận ở A7.
- Thời gian thêm vào job `gate-registry`: 2,6 giây đo trong container; trên runner chưa đo.
- `ci_provenance` cho mốc Gate output của chính packet này vẫn ra `not_measured` (N5, mục 6). Hồ sơ land của
  packet này phải đo mốc ấy bằng dấu hiệu dương từng bước (A6), không bằng `ci_provenance`.
