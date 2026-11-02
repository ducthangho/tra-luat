verdict: changes_requested
reviewed_sha: df3e103b6b0c8ac9259c040a518c7baf99f46790
spec_sha256: dee36a1148bc1fe8a934a9dceb74dbe0eab7d3a2830908d7f15afb3293f0812e
Ket qua: 0 P0, 0 P1, 1 P2, 0 P3.

Còn một biểu hiện của F1 ở tiêu đề ADR. Phần sửa trong thân ADR và dòng §20 khớp phép đo; F2 đã đóng. Không phản đối quyết định chủ kho chấp nhận giới hạn vĩnh viễn. Chưa xác minh được toàn bộ A4 và A5 trong môi trường được cấp.

## Phạm vi và định danh

- Packet #825 r1/g1, lease `wp825-r1-g1-claude`, review_class `sensitive`; ngưỡng riêng: hết P0/P1/P2/P3.
- Base: `c7174bfe03b3acd22cfa055b5fce176129d29542`. HEAD: dòng 2, tree `c8f59120f695268d69fa9cdbff7b023be9138e0e`.
- `git show refs/remotes/origin/ops/wp825-r1-g1-lease:ops/specs/wp825.md` khớp byte `../SPEC.md`, hash dòng 3; ref lease tại `18a5f89442545943ac7a4965063dc7db01ed8a5a`. Lease khớp revision/generation/base/write set. Không gọi mạng để làm mới ref; authority lựa chọn ADR nhận theo chỉ thị giao review.
- Diff base→HEAD khớp `../diff.patch`, đúng hai tệp: thêm 85 dòng ADR và một dòng §20; mã và test không đổi. Bốn tệp runtime/test đo có byte giống nhau tại base/HEAD (`evidence/code-identity.json`).
- Reviewer theo `run/94d79755/run.json`: `provider: openai_codex`, `execution_surface: codex_cli`, `transport: machine`, run `94d79755ffa7477a99386b0a45277601`. Executor theo lease khai Claude/claude_code. Không đo được model/effort phục vụ từng response hoặc byte câu duyệt của chủ kho; không biến cấu hình/lease thành bằng chứng runtime ấy.
- Linux, Python 3.13.18; không mạng, không credential thật. Quyền sandbox cho ghi workspace và `/tmp`; checkout được giữ read-only theo chỉ thị, không phải mount read-only riêng. Cache, fixture và patch thử nằm ngoài `cay-kho/`.
- Snapshot đầu/cuối gồm HEAD/tree, diff/index và nội dung tracked/untracked/ignored trùng nhau, không có path đổi (`evidence/final-integrity.json`). Hai mốc quan sát không chứng minh toàn bộ lịch sử chưa từng ghi rồi hoàn nguyên. Không push/đăng verdict/merge/land hoặc thay state điều phối.

## Lệnh tái lập và hiện vật

Chạy từ `cay-kho/`:

```bash
python3 -B ../evidence/review_checks.py
python3 -B ../evidence/check_facts.py
python3 -B ../evidence/repro_probe.py
python3 -B ../evidence/supplement.py
```

Ba script đầu lấy từ `evidence-l1/`: chỉ thay HEAD SHA trong `review_checks.py` và run ID trong `check_facts.py`; `repro_probe.py` giữ nguyên byte (sha256 `442b8e512ab4e8f8445d342d87961a50b4475562e14c0fb324a62c2778ffe6ef`). Cả bốn lệnh đã chạy, rc=0. Lệnh con/cwd/rc/stdout/stderr được lưu ở `evidence/*.json`; rc=0 của runner không thay rc của từng ca.

Runner nghiệm thu dùng env sạch không kế thừa credential, `PYTHONDONTWRITEBYTECODE=1`, TMPDIR tuyệt đối `../evidence/tmp`, Git config global/system rỗng, `core.abbrev=7`. Base xuất bằng `git archive` vào `evidence/base/`. `/tmp/.git` tồn tại và `_KhoCodex` từ chối mọi descendant. Quyền hiện hành chỉ cho ghi dưới workspace hoặc `/tmp`, nên không dùng được cách executor đã chạy với `TMPDIR=/var/tmp`. Không sửa/bỏ chốt constructor để khai A4 xanh.

`repro_probe.py` dùng auth INERT, probe giả và read/write sản phẩm trên dirfd riêng; factory fixture bỏ riêng constructor kiểm ancestor/ACL. `supplement.py` đo thêm ba ca/đột biến đích; materializer/t16 cũng dùng seam constructor đó. Đây là phép đo bổ sung của nhánh báo lỗi và chốt assertion, không thay các lệnh A4 nguyên trạng.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn lượt 1: `VERDICT-L1.md`, SHA `46421d7e4365b3490124bef541e243289f4d2006`.

| Finding / lớp | Đối chiếu độc lập trên HEAD hiện tại | Phân loại |
|---|---|---|
| F1 — `loi-ghi-khong-suy-ra-probe-lap` (P1 cũ) | Cả 24 tổ hợp base/HEAD × ba lối × bốn trạng huống tái lập đúng matrix lượt 1. ADR:15–32 đã giới hạn probe lặp, nhận cả state đã promote và lỗi đọc; §20 đã sửa đồng bộ. Câu “một lần” mới chỉ đếm helper của nhánh trực tiếp, phân biệt rõ HTTP request chưa đo. Tuy nhiên ADR:1 vẫn giữ phép suy không điều kiện “không ghi được … thì lần gọi sau probe lại”. | **VÁ HỜ** theo nghĩa chưa đóng toàn bộ lớp: thân bài đã vá thật, tiêu đề còn sót. Mức còn mở P2, không giữ P1 cho phần đã sửa. |
| F2 — `grep-ten-khong-do-khai-niem` (P2 cũ) | Chạy lại hai regex trên từng tệp, đủ sáu vị trí, cả base/HEAD: định danh đều 0; khái niệm chỉ launcher có 4 dòng. ADR và §20 dùng đúng “có nhắc”, không nâng proxy thành cưỡng chế; đọc `adr-song` xác nhận consumer metadata riêng. | **ĐÃ VÁ THẬT**. |

## BANG NGHIEM THU

Các lệnh dưới đây đã được runner gọi với cwd của từng cây. Base đặt ở `../evidence/base/`; HEAD là `cay-kho/`.

| Tiêu chí | Lệnh chạy được | Kết quả và kết luận |
|---|---|---|
| A1 | `python3 -B .claude/dev/packet_loop.py adr-song --root .` | HEAD rc=0, `60 ADR trên đĩa, 60 dòng trong §20`; base rc=0, 59/59. Bỏ đúng dòng ADR-0061 trên bản sao rồi gọi cùng consumer: rc=9, báo có tệp mà thiếu dòng §20. **ĐẠT**, dương/âm. |
| A2 | `python3 -B .claude/dev/packet_loop.py doctrine-scan --root .` | Base và HEAD rc=0, quét 10 tệp, 0 chỗ chép doctrine. **ĐẠT**. |
| A3 dương | `python3 -B ../evidence/review_checks.py` nối whitespace ADR, kiểm đủ năm chuỗi | `evidence/a3.json`: cả năm yêu cầu `true`. **ĐẠT**. |
| A3 âm | Hai regex ở bảng sáu cổng; đọc ADR:65–85 và consumer `packet_loop.py:1917–2009` | Không khai có cổng thực thi quyết định chấp nhận; phân biệt reader metadata và test hành vi. **ĐẠT**. |
| A4 launcher | `python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra --lan 1` | Base và HEAD rc=0, `1/1 qua, 0 bo qua, 0 hong`. **ĐẠT riêng ca này**. |
| A4 materializer | `python3 -B .claude/dev/launcher_test.py --lap-ca r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do --lan 1` | Cả hai rc=1, 0/1, setup `OSError: Codex home is inside a repository`. **FAILED khi chạy; KHÔNG ĐO ĐƯỢC hành vi A4 nguyên trạng** ở sandbox này. |
| A4 credential | `python3 -B .claude/dev/codex_cred_test.py` | Cả hai rc=1, nền 13/18; t6/t9/t16/t18 lỗi OSError, t15 bị chốt repo làm sai kết quả setup; runner không chạy mutation khi nền đỏ. **FAILED khi chạy; KHÔNG ĐO ĐƯỢC `TỔNG: ĐẠT`**. |
| A5 | Đọc check run `ci.yml` trên exact head dòng 2 | **KHÔNG ĐO ĐƯỢC / not_run**, theo chỉ thị offline. Local gate không thay CI. |

Không nhận cả A4 đạt, không bác phép chạy `/var/tmp` của executor chỉ vì reviewer có bẫy môi trường, cũng không dùng lời khai executor thay phép đo độc lập. A5 vẫn cần readback trước khi tuyên bố đủ điều kiện merge.

Đã chạy thêm `python3 -B scripts/tl.py doc-claims-check --strict --json`: rc=0, `ok: true`, mọi lớp kiểm có 0 finding cứng; 381 advisory nền. Log `evidence/doc-claims.json`. Đây là gate hình thức, không bác được finding ngữ nghĩa bên dưới. Một lần gọi nhầm subcommand trên `packet_loop.py` trả rc=2 được giữ riêng ở `doc-claims-invocation-error.json`.

## BANG DO

Mỏ neo mã dưới đây giống nhau ở base/HEAD. Lệnh đọc số dòng bằng `nl -ba <tệp>` hoặc `sed -n '<đầu>,<cuối>p' <tệp>`; các phép hành vi và consumer ghi cụ thể trong bảng.

| Khẳng định | Đo được (lệnh/consumer) | Khớp? |
|---|---|---|
| Accepted, r1/g1, spec có hash nêu trong ADR; nợ #825 từ #484/PR #792 | `python3 -B ../evidence/check_facts.py`; blob spec/lease local. Đối chiếu `ops/land/pr792-wp484-land-evidence.yaml` và `ops/handoff/wp484-g7-claude.md`. | Khớp hồ sơ local; lựa chọn chủ kho là authority đầu vào. Không đo GitHub/byte hội thoại. |
| `_danh_dau_auth_hong` ghi qua `_KhoCodex` và trả False khi OSError/ValueError/UnicodeError | `launcher.py:3589–3604`: ghi danh tính từ bytes đã probe; `_ghi_rejected` ở :3578–3586 ghi `credential-recovery.json`. | Khớp với helper. Materializer gọi `_ghi_rejected` trực tiếp ở :3704, không đi qua helper boolean này. |
| State đã nhớ danh tính thì không probe lại cùng danh tính | `launcher.py:3607–3616,3674–3678,3875`; `codex_cred.py:518`. `repro_probe.py` đối chứng thành công: cả ba lối `[1,0]`, đúng id. | Khớp trong phạm vi đo. |
| Không dựng chỗ lưu dự phòng | `rg -n 'credential-recovery\.json|codex-rejected-state-khong-ghi-duoc' .claude/dev/launcher.py .claude/dev/codex_cred.py` và đọc ba nhánh ghi. Một backend/file state, không có nhánh fallback. | Khớp phạm vi mã đang xét; không suy thành kiểm mọi dịch vụ ngoài kho. |
| Khi state còn đọc được nhưng chưa lưu id, cùng credential còn bị từ chối và lỗi trước promote lặp lại thì probe lặp | `python3 -B ../evidence/repro_probe.py`: `fail_before_replace`, cả ba lối `[1,1]`, state chưa chứa id. | Khớp ADR:22–25 có điều kiện. |
| Mỗi lượt đi đến nhánh ấy gọi helper một lần; chưa đo HTTP bên trong CLI | `launcher.py:3619–3636,3695–3713,3859–3901`; `codex_cred.py:183–222,518–529`. Ba hàm trực tiếp không lặp lời gọi helper; `_do_codex` :3989–4001 có các nhánh return loại trừ nhau. Fixture đếm helper cho cả ba lối. | Khớp cách diễn đạt mới. Chưa thấy >1 helper trong một lượt trực tiếp đi đến nhánh lỗi ấy. Không khẳng định một lệnh tổng hợp luôn có tối đa một probe hoặc một subprocess chỉ phát một HTTP request. |
| Ghi hỏng có thể đã đổi state, lần sau 0 probe; lỗi đọc cũng chặn, lý do có thể khác | `launcher.py:3388–3391`: replace rồi fsync thư mục POSIX; :3615–3616 fail-closed. `repro_probe.py`, hai chế độ lỗi tương ứng đều `[1,0]`. | Khớp ADR:27–32. Auth cũ giữ nguyên và không ghi nhầm id trong fixture; không nâng thành bảo đảm mọi I/O/xen kẽ. |
| Tiêu đề “không ghi được … thì lần gọi sau probe lại” | Cùng matrix, lỗi fsync sau replace và state không đọc được: lượt sau 0 probe ở cả ba lối. | **Chưa khớp phạm vi lời khai**, F1 còn ở ADR:1. |
| Launcher báo lỗi ghi riêng | `launcher.py:3895–3897`; ca `r484_g7_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra`, mutation `g7_nuot_loi_ghi_trang_thai` ở `launcher_test.py:13393`. | Khớp prefix `KHÔNG ghi được trạng thái chờ snapshot sau khi … — CHẶN: sửa CODEX_HOME (quyền/dung lượng) trước khi thử lại`. Ca nguyên trạng xanh; mutant bị ca đích bắt trên base/HEAD. |
| Materializer báo đúng lỗi ghi, giữ credential cũ | `launcher.py:3704–3709`: `CHỜ snapshot mới: auth bị từ chối nhưng KHÔNG ghi được trạng thái chờ (<loại lỗi>) — CHẶN; giữ credential cũ`. Ca `r484_g7_materializer_khong_ghi_duoc_trang_thai_noi_dung_ly_do`, mutation `g7_f01_materializer_gop_loi` ở test :13401. | Khớp mã và fixture. Ca/đột biến đích có răng với seam constructor; A4 nguyên trạng còn thiếu do môi trường. |
| `codex_cred.cmd_kiem` báo lỗi ghi riêng | `codex_cred.py:524–529`: prefix trên, đuôi `CHẶN: sửa CODEX_HOME trước khi thử lại`, rc=2. Ca `t16_khong_ghi_duoc_trang_thai_tu_choi_phai_noi_ra` ở test :449, mutation `t16_nuot_loi_ghi` ở :570. | Khớp mã và fixture. Mutation tồn tại, mỏ neo duy nhất và giết ca t16 với seam constructor; chưa phải full suite A4 xanh. ADR không ghi tên mutation t16 nhưng đã dẫn ca và tệp; không thiếu chốt trong mã. |
| Các test dẫn là bằng chứng hành vi, không đọc ADR | Đọc thân ba ca và `DOT_BIEN`; `check_facts.py` xác nhận cả ba mỏ neo chỉ khớp 1 lần. `supplement.py` cho baseline PASS, mutant lỗi assertion đúng của ca đích ở cả base/HEAD. | Khớp trong phạm vi đã khai. Historical full-suite pass và thời điểm 00:5xZ không được tái chứng nhận độc lập ở đây. |
| Sửa quyền/dung lượng rồi gọi lại; login/chuan-bi để khôi phục | Đọc các nhánh state và `chuan_bi_xac_thuc`, parser `chuan-bi`; đối chứng ghi thành công lưu id. | Hướng gỡ phù hợp, với snapshot từ biến phải đủ điều kiện. Không chạy login hoặc khôi phục credential thật. |
| Dự phòng thường hỏng cùng nguyên nhân, không mua thêm nhiều | ADR:59–63 có nhãn “suy luận, CHƯA ĐO trên từng loại hỏng”. | Khai đúng giới hạn. Không có phép đo đầy đĩa/quyền/read-only thực hoặc chỗ dự phòng sống/chết trong review này. |
| Sáu cổng: tên ADR 0, khái niệm launcher 4, §20 dùng mức “có nhắc” | Hai regex riêng trên từng tệp, cả hai cây; bảng bên dưới. Đọc định nghĩa §20:1487–1498. | Khớp. 4 dòng không có nghĩa 4 cổng cưỡng chế. |
| §20 thêm đúng một dòng, đủ bốn cột, mô tả và trạng thái khớp ADR | `git diff --numstat BASE HEAD`; `adr-song` A1 dương/âm thực sự chạy parser bảng. | Khớp dòng :1548 hiện tại; không lặp câu sai cũ trong mô tả. |
| `adr-song` đọc đăng ký/trạng thái, không thực thi quyết định chấp nhận | `packet_loop.py:1917–2009` đọc toàn bộ ADR để kiểm metadata; không xử lý hậu quả probe/fallback của ADR-0061. Đọc các nhánh của ba đường runtime không thấy consumer quyết định chấp nhận. | Khớp kết luận có phạm vi; không suy riêng từ grep tên và không phủ định việc đọc file metadata. |

### Matrix cùng phương pháp lượt 1

Kết quả giống nhau trên base và HEAD, ở cả launcher/materializer/cmd_kiem:

| Lỗi chèn / đối chứng | Số helper probe hai lượt | State đã nhớ đúng id sau hai lượt |
|---|---|---|
| Lỗi trước replace state | `[1,1]` | Không |
| Lỗi fsync thư mục sau replace | `[1,0]` | Có |
| State không đọc được sau probe đầu | `[1,0]` | Không |
| Ghi thành công | `[1,0]` | Có |

Mỗi tổ hợp giữ auth cũ và không ghi id của credential chưa probe. Lượt sau ở hai phản chứng trả `CHỜ snapshot Codex mới`, `CHỜ snapshot mới; không lặp credential đã thất bại`, hoặc materializer báo chờ id cũ/lỗi đọc ghi state chung. `evidence/{base,head}-probe-repro.json` lưu cả lý do từng lượt. Đây là I/O chèn có kiểm soát, không phải phép đo mạng hoặc mọi loại hỏng trên OS thật.

### Đủ sáu vị trí cổng

Đã chạy riêng từng regex trên từng tệp, cả base và HEAD:

```bash
rg -c 'ADR-0061|0061-codex' <tep>
rg -c 'codex-rejected-state-khong-ghi-duoc|_danh_dau_auth_hong|KHÔNG ghi được trạng thái' <tep>
```

| Tệp | Định danh base/HEAD | Khái niệm base/HEAD |
|---|---|---|
| `ops/lease_publish.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.claude/dev/packet_loop.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.claude/dev/launcher.py` | 0/0, rc=1/1 | 4/4, rc=0/0 |
| `.claude/dev/gate_lifecycle.py` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.github/workflows/ci.yml` | 0/0, rc=1/1 | 0/0, rc=1/1 |
| `.github/workflows/ops-publish-lease.yml` | 0/0, rc=1/1 | 0/0, rc=1/1 |

Không khớp nghĩa là stdout rỗng/rc=1, không phải stdout in `0`. Các dòng khái niệm launcher là :3589,3702,3895,3896. Log `evidence/{base,head}-{gate,concept}-{0..5}.json`.

## Bảng lớp và finding còn mở

| Slug lớp | Biểu hiện và mức còn mở | Nguồn | Phép đóng |
|---|---|---|---|
| `loi-ghi-khong-suy-ra-probe-lap` | ADR:1, P2; thân ADR và mô tả §20 đã sửa | F1 lượt 1/SHA `46421d7…`, còn sót trên SHA dòng 2 | Thu hẹp tiêu đề thành khả năng có điều kiện, đọc toàn ADR/§20 đối chiếu matrix hai lượt. |
| `grep-ten-khong-do-khai-niem` | Không còn mở | F2 lượt 1/SHA `46421d7…`, đóng trên SHA dòng 2 | Đã chạy đủ hai regex/sáu vị trí/hai cây, kiểm định nghĩa §20 và consumer metadata. |

Hai lớp lịch sử; một lớp còn mở, một biểu hiện còn mở. Không phát hiện lớp lỗi mới về runtime, ba đường báo lỗi hoặc phép đếm cổng trong phạm vi review.

### loi-ghi-khong-suy-ra-probe-lap [P2] Tiêu đề còn suy lỗi ghi thành lần sau chắc chắn probe lại

**Tệp/dòng:** `docs/adr/0061-codex-trang-thai-tu-choi-khong-ghi-duoc.md:1`.

Tiêu đề vẫn khẳng định “Không ghi được trạng thái … **thì lần gọi sau probe lại**”, trong khi chính thân bài mới ở :27–30 thừa nhận lần sau có thể không probe. Phép đo giữ nguyên của lượt 1 cho hai phản chứng chạy được trên HEAD: lỗi fsync thư mục sau replace đã lưu id, hoặc state không đọc được, đều cho `[1,0]` ở cả ba lối. Vì vậy tiêu đề vẫn trình bày hậu quả rộng hơn điều kiện thực sự đã đo/suy từ mã. Đây là phần còn sót của F1, không phải phát hiện rằng câu “một lần” đã được giới hạn ở :24 lại sai.

**Phân mức:** P2 cho lời khai còn rộng ở tiêu đề sau khi phần nội dung chính đã sửa; không giữ P1 của các bảo đảm sai đã được loại khỏi thân ADR/§20. Chỉ cần đổi tiêu đề thành “Chấp nhận vĩnh viễn khả năng probe lặp khi không ghi được trạng thái từ chối Codex”, hoặc nêu đủ điều kiện; không đổi quyết định chấp nhận và không sửa runtime.

**Bằng chứng chạy được:** từ gốc `cay-kho/`, `python3 -B ../evidence/repro_probe.py` rc=0; `head-probe-repro.json` có đủ ba lối và hai phản chứng trên, cùng đối chứng `[1,1]` trước replace và ghi thành công `[1,0]`. Sau sửa đọc lại cả tiêu đề/thân ADR/dòng §20 để cùng nói về khả năng có điều kiện. Độ tin cao về matrix; rủi ro vá thấp vì chỉ đổi một dòng văn bản.

## Tiền đề spec cần đưa vào handoff

Mục **Sự thật đã đo** của SPEC vẫn nói “Mỗi lần gọi tốn thêm 1 lần probe, và lần nào cũng … cùng lý do”. Matrix ở trên bác tính tuyệt đối của tiền đề này; ADR hiện tại đã thu hẹp đúng ở thân bài. **A1–A5 không có tiêu chí bắt buộc mọi lần gọi phải đúng một probe**: A4 chỉ đòi các ca dẫn chạy xanh. Vì vậy không ép ADR giữ lời khai sai để khớp tiền đề spec, cũng không tự sửa spec đóng băng.

Executor cần ghi rõ lệch tiền đề này trong handoff, kèm điều kiện state còn đọc được/chưa nhớ id và hai nhánh 0 probe; nếu authority muốn thay nghĩa vụ nghiệm thu thì xử lý revision theo protocol. Đây là lưu ý authority/handoff của tiền đề thực chứng đã nêu ở lượt 1, không là finding phản đối chủ kho chọn ADR. Bản handoff cập nhật có `hint_provenance` không được giao trong bundle/refs hiện tại, nên KHÔNG ĐO ĐƯỢC nội dung hay tính đầy đủ của nó; không tự kết luận đã có hoặc chưa có ở nơi ngoài bundle.

Các câu mới “một lần” và “suy từ luồng mã” ở ADR đã khai đúng mức helper, không tự nhận là số request mạng đã đo. Mục **Vì sao không dựng chỗ lưu dự phòng** giữ nhãn suy luận chưa đo rõ ràng. Lời “đã đo” về test có lệnh tái lập; full-suite pass lịch sử chỉ là lời khai chưa tái chứng nhận trong sandbox này, không bị xem là sai chỉ vì bẫy `/tmp/.git`.

## Gợi ý vá và giới hạn nghiệm thu

`HINT.patch` là artifact theo yêu cầu, dùng `patch -p0` từ gốc cây, chỉ đổi tiêu đề ADR. Nhãn: **“chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”**. Đã dry-run rồi áp thật chỉ trên bản sao reviewer `evidence/hint/`, `--fuzz=0`, rc=0; A1 bản sao 60/60 rc=0, A2 quét 10 tệp/0 vi phạm rc=0. Log `evidence/hint-{dry-run,apply,adr-song,doctrine-scan}.json`; script `evidence/validate_hint.py` đã chạy rc=0. Không áp vào `cay-kho/` và không coi hint là review của SHA tương lai.

Chưa đo được: A4 đầy đủ với constructor nguyên trạng trong temp không có ancestor `.git`; full 18 ca/18 mutation credential ở nền neutral xanh; CI exact-head A5; request/retry mạng thực; Windows, mất điện và mọi lỗi đầy đĩa/quyền/read-only thực; khả năng chỗ dự phòng sống sót; byte lời duyệt và handoff cập nhật của executor. Các mục đó không được ghi là passed. Finding P2 hiện còn mở nên không đủ ngưỡng approve của assignment.
