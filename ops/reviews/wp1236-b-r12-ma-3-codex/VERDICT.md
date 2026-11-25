Review mã wp1236 đợt B, lượt **3/4**: **changes_requested**. B01 P2 còn mở; B02 P3 `ngoai_bang_dong` là biểu hiện bổ sung cùng lớp.

Ứng viên `8782e25719b2664ccc8968961ee4242febc5050d`, tree `290b353d0f9195b649e0185032fc2180e6edc514`; base `f602325574c62184caf16309631f5f680ca5cee2`. Đặc tả r12 SHA-256 `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`, generation 1. Provider/surface/transport: `openai_codex / codex_cli / machine`, run `97522a3b6fd249efa786a03241fa34dc`. Model và effort phục vụ: `KHONG_DO_DUOC` từ receipt hiện có; yêu cầu là high. Linux, Python 3.13.18, Ruff 0.15.15. Không gọi mạng, không sửa repository.

| Lớp | Biểu hiện | Mức mở cao nhất | Cách vá chung và phép đóng |
|---|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` | B01: miền văn bản tự do chưa đủ qua L8; B02: ca nhập từ A có thể biến mất âm thầm | P2 | Hợp đồng miền→ca tường minh; đủ đối chứng từng mệnh đề; xác minh tập ca trước khi chạy. Đóng bằng ledger qua L8, phản chứng mất từng ca, suite và luật 9. |

**Đối chiếu lượt trước: B01 — `VA_MOT_PHAN`.** Tôi đã chạy lại 23/23 đối chứng `lich_su/probe_scope.py`; chạy lại ledger và so bằng hoàn toàn **160 ô B + 8.396 phần tử c36** với hiện vật executor. Quan sát độc lập xác nhận **8.396 lần `main` và 8.396 lần L8**, roundtrip YAML giữ đúng đầu vào, gồm surrogate qua escape và ký tự ngoài BMP. Byte không UTF-8 mới ở c35 phát đúng `khong_phai_utf8`.

Phần đã đóng gồm token/casefold, dấu phân cách, miền chữ số của landed, URL/SHA/OS/ngày, `ly_do` qua JSON và lớp ký tự tên tệp. Miền số 8 vẫn thiếu một số vị trí văn bản tự do. B02 còn cho thấy bản vá sinh cách mất miền mà chốt tổng đếm không bắt. Bảng đủ chín miền và số đo nằm trong [scope-domain-review.json](scope-domain-review.json), [ledger.md](ledger.md), [scope-summary.json](scope-summary.json). Không dùng các probe riêng của reviewer như ca đã có của candidate.

Hội tụ **lượt 2→3 = 0/1**; lượt 1→2 cũng 0/1. Cùng lớp đã xuất hiện ở cả ba lượt B, chưa có lớp nào đóng thật. Theo §12 và chỉ thị trong handoff, cần **checkpoint điều phối, dừng vòng vá thông thường và xét lại cách làm**; lượt review này không cấp thêm vòng/lời gọi hay authority.

**B01 — P2: miền văn bản tự do qua consumer L8 vẫn chưa đủ.** Vị trí: `ops/land_evidence_nguon_test.py:790–816`; các ca được nhập ở `ops/gate_output_doi_chieu_test.py:952–1012,1133–1168`. Căn cứ: luật 4/8 và câu giữ nghĩa vụ ca bắt buộc ở luật 9, SPEC dòng 427–445, 473–474.

c36 giữ nguyên bộ sinh và oracle của những ca A được chọn. Nhưng a125 chủ yếu thay **ID** của dòng skipped; các đối chứng tên skipped bổ sung ở cuối a125 chỉ gọi hàm lá, không gọi `kiem_ho_so`, nên adapter không chuyển chúng qua L8. a129 thay tên/đuôi dòng job thường; nó không vét miền tên skipped, vùng `.*` của header, hay các đại diện Unicode hợp lệ của nhãn.

Phép đo `summarize_scope.py` đọc fixture thật tại biên L8 của toàn bộ 8.396 phần tử c36, rồi chạy và quan sát 20 fixture c35:

| Vị trí | Quan sát trên candidate |
|---|---|
| Tên skipped cũ | 0 tên rỗng; 0 tên ngoài ASCII |
| Tên skipped v3 | 0 tên rỗng; 0 tên ngoài ASCII |
| Vùng tự do header | Chỉ chuỗi rỗng hoặc `luat dau hieu duong THEO BUOC `; 0 ngoài ASCII |
| Nhãn | 0 giá trị ngoài ASCII; ca nhãn `]]` có nhưng không thay dương theo category |

Đây là **thiếu ca bắt buộc**, không phải nâng một đột biến ngoài manifest lên P2. Reviewer chạy thêm **12/12 đối chứng dữ liệu** qua `main`/L8: tên skipped rỗng → `dong_la`; tên ngoài BMP hoặc chứa delimiter bên trong nhưng hợp lệ → `bo_sinh_la`; vùng header/nhãn ngoài BMP hợp lệ → `bo_sinh_la`; LF trong vùng header → `dau_tep_sai`; nhãn chứa `]` → `dong_la`. Fixture dùng băm bộ sinh giả có chủ ý: `bo_sinh_la` là đối chứng **đúng ngữ pháp**, phân biệt với lỗi parse. Mã hiện tại xử lý đúng; ca nghiệm thu của candidate vẫn thiếu.

Tái lập từ `repo`, mọi tệp tạm nằm trong `work/`:

```sh
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/summarize_scope.py
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/probe_missing.py
```

Bằng chứng: [scope-summary.json](scope-summary.json), [missing-probes.json](missing-probes.json), [log probe](logs/probe-missing.log). Một lần dựng fixture reviewer ban đầu đặt ký tự sai vị trí header đã được sửa; kết quả lỗi setup được giữ riêng trong JSON, không tính là lỗi candidate.

Đề nghị trong write set B: giữ reuse A cho miền nó phủ và thêm bảng hữu hạn qua adapter L8 cho những vị trí còn thiếu, oracle theo mệnh đề SPEC. Kiểm mỗi vị trí có âm/dương và các category đi được qua tuyến; không dùng tổng phần tử hoặc kết quả sản phẩm làm oracle. Không sửa A ngoài write set. Tổng diff đã 448/450 dòng; phải giữ trần hoặc chuyển checkpoint đúng authority.

**B02 — P3 `ngoai_bang_dong`: đổi tên hoặc bỏ ca A không bảo đảm c36 đỏ.** Vị trí `ops/land_evidence_nguon_test.py:811–816`. Vòng lặp lọc từ các tên **đang tồn tại** trong `a.CA`; ca biến mất không vào vòng lặp, nên chốt “mỗi ca phải gọi consumer” không được xét. Tổng ≥8.000 còn cho phép mất miền nhỏ.

| Phản chứng trên bản sao | Kết quả c36 |
|---|---|
| Baseline nguyên byte | rc 0; 8.396 main/L8 |
| Bỏ a126+a129+a131 khỏi registry bản sao | rc 0; còn 8.307 main/L8 |
| Bỏ riêng a134 | rc 0; còn 8.078 main/L8 |
| Đổi tên thật ba hàm a126+a129+a131 thành `renamed_*`, giữ thân hàm | rc 0 |
| Đổi tên thật a134 thành `renamed_*` | rc 0 |
| Ca A được chọn không gọi consumer | rc 3, `DO:c36…` — chốt này hoạt động |
| Ca A chết vì lỗi vô can | rc 4, `RuntimeError` — không nhận nhầm là giết đúng chốt |

Các lần đổi tên thật dùng **bản sao vật lý** của cả bốn tệp A/B dưới `work/baseline`, `work/rename-small`, `work/rename-a134`; B giữ nguyên byte. Fixture chỉ đọc từ cây `ops/land`. Bằng chứng: [cặp đổi tên](outside-mutants.json), [baseline](real-baseline.result.json), [đổi ba tên](real-rename-small.result.json), [đổi a134](real-rename-a134.result.json), [đếm bỏ ba ca](adapter-drop-a126,a129,a131.json), [đếm bỏ a134](adapter-drop-a134.json). Những đột biến này tác động test A, không thuộc manifest module B và kho B rỗng; giữ đúng P3 theo assignment.

Tái lập trên các bản sao đã lưu:

```sh
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/baseline/ops/land_evidence_nguon_test.py --mot-ca c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/rename-small/ops/land_evidence_nguon_test.py --mot-ca c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a
TMPDIR="$PWD/../work/tmp" PYTHONDONTWRITEBYTECODE=1 python3 -B ../work/rename-a134/ops/land_evidence_nguon_test.py --mot-ca c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a
```

Đề nghị xác minh tập tám ca/prefix bắt buộc, mỗi mục giải được đúng một ca, rồi lookup và chạy từng mục. Đối chứng đổi tên/bỏ từng ca phải đỏ. Tránh chỉ tăng ngưỡng tổng: nó vẫn không chứng minh đủ miền. B02 đang mở, chưa có miễn; nếu chọn miễn thì **chờ miễn chủ kho neo exact SHA**. Có B01 P2 nên miễn B02 cũng chưa đủ approve.

Các mặt tái dùng c36 đã kiểm: oracle không lấy đầu ra L8 làm kỳ vọng; thân ca A giữ nguyên; YAML ASCII không làm rơi phần tử; năm hàm lá có `co_filename` trỏ module A nguyên bản; baseline của scanner với biến môi trường trỏ B vẫn chạy c36 đạt. Cache `compile` theo toàn bộ đối số không thay oracle. Adapter chiếu riêng các dòng L8 để cô lập consumer; không suy rc0 của toàn cổng từ danh sách L8 rỗng.

| Phép kiểm reviewer | rc | Bằng chứng dương |
|---|---:|---|
| Suite B | 0 | 36/36 ca, 144/144 đột biến, tự kiểm DAT (2); 318,23 giây |
| Cổng cây thật | 0 | 174 hồ sơ, 149 ĐẠT, 25/28 cutover miễn, 0 vi phạm/không đo được |
| MIEN_TRU_L8 | 0 | 174=25 cutover+56 đỏ+43 lời khai hợp lệ+50 không lời khai; 93 lý do, 56 tên/băm khớp |
| Ruff F head/base | 0/0 | Cùng hai tệp, 0 lỗi, delta=0; `--no-cache` |
| Ruff pin/probe riêng | 0 | `RUFF_CONTRACT 3 []` |
| ci_dang_ky_test | 0 | 1226/1226 phản chứng; TỔNG ĐẠT |
| numstat / diff-check | 0/0 | Hai tệp, 448 dòng thêm ≤450; không lỗi whitespace |
| Module từ lượt 1 | 0 | `git diff f4e93b3 HEAD -- ops/land_evidence_nguon.py` rỗng |
| Probe lịch sử | 0 | 23/23 |

**Luật 9: kiểm toàn bộ hiện vật, tái chạy mẫu; không khai đã chạy lại full `do`.** Tôi tái sinh manifest từ bộ quét ghim trên base và head, đối chiếu từng ID/sha256/src, neo module/test/shim/Python/kho, danh sách baseline và dấu `HOAN_TAT`. `hoi-quy` tái sinh bằng hoàn toàn hiện vật nộp. Kết quả hiện vật: head 624 = 76 delta + 548 kế thừa; **76/76 delta GIET**, 0 hồi quy kế thừa. Hai return base không áp được có thay thế cùng nghĩa dòng 408, đã đo lại GIET c14. Không có delta tương đương cần chứng minh.

Độc lập chạy `chay` trên **28 mutant head**: 22 delta GIET, 5 kế thừa GIET, 1 kế thừa SONG; baseline **36/36**. Chạy lại đúng **6 ID kế thừa trên base**: 5 GIET, 1 SONG; baseline **23/23**, không hồi quy trong mẫu. Shim base chỉ nối biến môi trường và đặt root fixture vào cây `ops/land` đã chứng minh có cùng Git tree với base; không thay mã test/base. Mọi mutant được đo trên bản sao ngoài repository. Các kết quả mẫu khớp hạng và ca giết của hiện vật.

54 delta và 542 mục kế thừa ngoài mẫu trên head chưa được reviewer tái chạy; full `do` 624/550 là **not_run trong lượt này**. Đây là nhánh kiểm tối thiểu assignment cho phép, không biến bằng chứng executor thành lời khai tự chạy. 173 SONG và 13 VO_CAN của head là mã kế thừa, không báo thành finding B. Bằng chứng: [kiểm hiện vật](law9/verification.json), [delta](law9/delta.json), [548 ánh xạ](law9/inherited-ledger.json), [mẫu head](law9/sample-kq.jsonl), [mẫu base](law9/base-sample-kq.jsonl).

**M3 Windows: required**, theo bước 2 ADR-0060; Windows local exact base/head chưa đo, điều phối phải hoàn tất. Windows CI được miễn theo assignment, không suy miễn local. c36 tạo **8.396 thư mục tạm mỗi lần** và sao provenance; cần đo thời gian và **MAX_PATH** trên Windows, chưa kết luận có lỗi Windows.

Snapshot đầu/cuối khớp HEAD/tree và băm **17.938 tệp tracked**; diff/index/untracked/ignored-file đều rỗng, chỉ mount `.codex/` rỗng xuất hiện trong status. Hai snapshot không chứng minh toàn bộ lịch sử ghi. Không chạy GitHub/connector/CI mạng, selftest toàn kho hay thử ghép master; không tính các lời khai ấy là reviewer đã đo. Chi tiết command, rc thật, hash stdout, `passed`/`failed`/`skipped`/`not_run`, giới hạn và nhận dạng nằm trong [VERDICT.json](VERDICT.json).

Kiểm schema: `python3 ../kiem_verdict_lop.py ../work/VERDICT.json --vong 3` → `HOP_LE (§8.3): 2 finding, 1 lop`, rc 0; stdout lưu tại [kiem_verdict.txt](kiem_verdict.txt). Đây là verdict review mã offline, không cấp quyền push/merge/land.

KET_LUAN: changes_requested
