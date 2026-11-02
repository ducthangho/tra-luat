verdict: changes_requested
reviewed_sha: 916a60ac2d91025879aa420c42aacbf6c26d94c4
Kết quả: 0 P0, 6 P1, 1 P2, 0 P3.

Review độc lập tại exact head trên, tree `4c2296ee7a22cf389f1a6683aa058fed5c072fa6`; so `origin/master=e139e55883d90fd74a358230be5599c9e223d4b3`. Đặc tả revision1 SHA256 `69394c7658db28196b72e3a1b00f4f6931ad9aba8b9fdcf76563fab33edaa671` khớp. Review class theo chỉ thị là sensitive. Không sửa cay-kho, không push, không gọi mạng; mọi fixture/mutant/hint ở bản sao dưới `/tmp/wp960-r2-Dt2G8H/`. Base lease đã đo là `e3ea13923dceab7c15fc62a0823ef5f4f576e589`.

Các gate sẵn có đều xanh nhưng phản chứng độc lập chỉ ra mốc/đọc lịch sử, OID thiếu, phân loại trích dẫn và ba mục nợ surface còn sai; phép đo folded A3 chưa đạt. Một finding về lỗi đọc receipt là lỗi nền, được ghi tách rõ theo yêu cầu săn ba trạng thái, không quy là regression của bản vá.

## KẾT LUẬN VỀ FINDING CŨ

- `moc-muon-tay-trang-cau-cu`: **ĐÃ ĐÓNG** với đúng phản chứng cũ — plain/`>-`/`|`/list sau thêm mốc muộn, sửa khoảng trắng và commit đều còn rc=1 (`probe-anchors.log`); c81 qua, m86 làm đúng c81 đỏ trong full suite. Đường đổi tên mới là finding riêng.
- `surface-hong-nguon-thanh-sach-hoac-no-chet`: **ĐÃ ĐÓNG** — JSON lỗi/kiểu list/thiếu trường với và không nợ đều rc=2, không nợ chết; verdict byte hỏng thuộc c77 cũng qua; m83 giết c77 (`probe-surfaces.log`, `probe-old-cases.log`, `suite-head.log`).
- `oid-hop-le-toan-chu-bi-bo-qua`: **ĐÓNG MỘT PHẦN** — c78 dựng được commit thật prefix toàn chữ lẫn toàn số và bắt vi phạm; m84 giết c78. OID thiếu thuần chữ/số, kể cả OID40 có nhãn Commit, vẫn bị bỏ qua rc=0 (`probe-candidates.log`): xem finding mới.
- `yaml-alias-vong-lam-crash`: **ĐÓNG MỘT PHẦN** — đồ thị hiện tại ném `KhongDoDuoc` đúng, alias dùng lại không vòng được c82 duyệt cả hai đường; m88 giết c82. Cùng alias vòng trong lịch sử được lời gọi mới `_co_cau` duyệt mà không chuyển trạng thái, tiến trình con rc=1 (`probe-history.log`).
- `surface-thu-hai-cung-dong-bi-bo`: **ĐÃ ĐÓNG** — hai thứ tự khai báo đều rc=1 ở c83, probe đúng-trước/sai-sau cũng rc=1; m89 giết c83.
- `chot-moi-chua-duoc-ca-nao-khoa`: **ĐÃ ĐÓNG** cho năm chốt đã nêu — m90 (mốc40) giết c71; m91 (`luot` receipt khác) giết c70; m92 (merge-base lỗi) giết c84; m83 (nguồn surface hỏng) giết c77; m93 (lịch sử không đọc được không thành mốc sai) giết c85. Toàn full-suite xác nhận `giet_that`, không chỉ kiểm tên/anchor; các đường lịch sử hỏng mới vẫn có finding riêng.
- `a4-fixture-khong-co-lich-su-git`: **ĐÃ ĐÓNG** — độc lập quan sát bốn fixture c73: HEAD resolve rc=0, tree chứa receipt/verdict/run.json, c73 qua (`probe-acceptance.log`).
- `a3-mutant-chet-boi-literal-khong-phai-folded`: **CHƯA ĐÓNG** — dưới m78, `khoi_gap` vẫn vi phạm, c72 chỉ đỏ vì `khoi_lit`. Chú thích mới nói đúng giới hạn nhưng không đáp ứng phép đo folded A3 (`probe-a3.log`).
- Connector — run.json hỏng thành “không áp”: **ĐÃ ĐÓNG** — cùng phép đo nguồn hỏng có/không nợ đều rc=2; c77/m83.
- Connector — OID viết tắt toàn chữ số bị bỏ: **ĐÃ ĐÓNG** với OID thật — c78 tra commit thật prefix số, vi phạm đúng một tuple; m84 giết c78. OID thiếu được tách riêng ở finding còn mở.
- Connector — dòng TRÍCH DẪN hiện vật khác bị coi tự khai: **ĐÓNG MỘT PHẦN** — phản chứng trích nguyên dòng đã xanh đúng (c79/m85); hai nợ trích dẫn pr896-review-8/pr915-review-1 không còn trong tập đo. Regex mới lại miễn cả lời tự khai sau một tham chiếu văn xuôi; xem finding mới. Ba nợ còn lại cũng là lời trích nhưng bị coi tự khai; finding độc lập về M4.
- Connector — blame cả scalar kéo câu cũ vào mốc câu mới: **ĐÃ ĐÓNG** với phản chứng cũ — c80 qua; m87 giết đúng c80; mốc theo câu chuẩn hoá giữ được trường hợp thêm câu mới sau D. Không dùng kết quả này để chứng minh rename hay lịch sử hỏng đã đúng.

Tên log trong mục này thuộc `evidence/`. Kết quả full suite đo trên `916a60ac2d91025879aa420c42aacbf6c26d94c4`.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Identity/phạm vi | head 916a60a, hai tệp, spec hash cố định | `git rev-parse`, `git diff --numstat origin/master HEAD`, `sha256sum`: HEAD/tree/spec khớp, đúng hai tệp | Có |
| Cấu hình ref giao | origin/HEAD vắng | `git symbolic-ref refs/remotes/origin/HEAD`: cây gốc có và trỏ nhánh PR; clone đo CI đã xoá ref này | Không; đã giữ nguyên cây gốc |
| CLI head | rc=0, nợ 1/60/3, surface unknown0 | `python3 ops/bien_nhan_v2.py --root .`: cả cây gốc và clone CI in `TỔNG: ĐẠT`, 295 receipt, 0 lỗi/unknown, nợ 1/60/3 | Có |
| Suite head/M5 | 85/85, 95/95, 2/2 | `python3 -u ops/bien_nhan_v2_test.py`: rc=0, đúng số; thêm 77/95 khai đối chứng | Có; răng A3 bị giới hạn |
| M1/A1 | SHA40 chính xác, `luot` lớn hơn, có mốc miễn | c69/c70 qua; m73/m74/m75/m91 giết đúng ca; SHA lệch một ký tự vẫn xanh | Có trên các ca này |
| M2/A2 | tổ tiên1, không tổ tiên0, OID thiếu2, mốc hợp lệ0, mốc sai1 | c71/c84/c85 qua; `probe_review.py candidates/anchors/historical` chỉ ra OID thiếu thuần chữ/số bị sạch, rename/mốc và lịch sử hỏng sai trạng thái | Một phần, P1 |
| M2/A3 | có dấu/không dấu/folded đều nhận, không OID không vi phạm; có đột biến đúng folded | c72 qua; `probe_review.py a3`: m78 giữ `khoi_gap`, chỉ mất `khoi_lit` | Hành vi dương khớp; phép đo đột biến folded không khớp, P2 |
| M3/A4 | so run.json, caveat, thiếu tệp không áp | c73 qua, fixture có Git history thật; c77/c79/c83 qua; `probe_review.py surfaces` bắt sai/multiple nhưng miễn nhầm tự khai sau tham chiếu | Một phần, P1 |
| M4/A5 | nợ cho qua, bỏ nợ đỏ, nợ chết đỏ | c74/c75 qua; m81/m82 giết đúng ca | Có trên ca đã đo |
| M4/A6 tập nợ | đóng băng base, chỉ co, đúng vi phạm | `p.debt()`: base/head cùng tập64, frozen rc0, empty rc1 đúng64 lỗi, unknown rỗng, không mục thừa/thiếu theo bộ chọn | Khớp bộ chọn; ba surface là nợ thừa khi đối chiếu ngữ cảnh, P1 |
| A6 nền | CLI/base và suite nền đạt | dữ liệu base + luật head frozen rc0; suite gốc base `68/68 · 74/74 · 2/2`, rc0 | Có |
| A7 | trước thi công chưa có luật/ca mới | `p.debt()`: base e3ea139 không `_kiem_cau_lich_su`, không `NO_CAU_LICH_SU`, không c69; suite gốc68 ca | Có |
| Commit đầu thêm câu | đầu tiên chứa câu chuẩn hoá, không theo rename | `probe_review.py anchors`: định dạng không tẩy trắng; rename tẩy trắng được. `historical`: lỗi YAML/blob bị bỏ qua | Một phần; không theo rename làm lỏng hơn, P1 |
| OID | tra mọi token, thiếu thuần chữ/số bỏ | `probe_review.py candidates` + c78: đúng như mã khai | Khớp lời khai, trái yêu cầu M2 đối với OID thiếu rõ ngữ cảnh |
| Surface | nguồn có/hỏng2, mọi khai báo, sau trích dẫn bỏ | `probe_review.py surfaces`: hai điều đầu đúng; tham chiếu văn xuôi cũng bị miễn | Một phần, P1 |
| Alias/ngày fixture | vòng thành trạng thái thứ ba, ngày ghim | hiện tại c82 đúng; lịch sử alias rc1. `p.acceptance()` lặp2 B0/X/M byte-identical OID | Một phần |
| A3 lời giải thích | parser gấp folded trước cổng, m78 chỉ literal | `probe_review.py a3`: đúng | Có với lời khai thu hẹp; chưa đạt đặc tả đóng băng |
| Kích thước | +1037/-12, đã khai trên PR | `git diff --numstat origin/master HEAD`: 453/10 + 584/2 | Số dòng khớp; khai PR KHÔNG ĐO ĐƯỢC vì không gọi mạng |
| Ruff delta | 0 so master nếu có ruff | hai tệp head/base đều1 F541 cùng thông điệp, delta0 (`ruff-*.json`) | Có |
| Doctrine/diff | sạch | `packet_loop.py doctrine-scan --root .`: rc0, 10 tệp/0 chép; `git diff --check origin/master HEAD`: rc0, stdout rỗng | Có |
| Git/object/nhánh lỗi | ba trạng thái giữ nguyên | `p.measurement()`: git/merge-base/nhánh/mốc thiếu2, alias hiện tại `KhongDoDuoc`; đọc receipt lỗi vẫn CLI1 | Một phần, P1; lỗi đọc receipt là lỗi nền |
| Đột biến reviewer | >=5 chốt khác m73–m82 | tám mutant riêng, toàn bộ85 CA/mutant; kết quả và cặp neo/thay ở hướng12 | Đã đo đủ8; mỗi mutant có ca đích đỏ thật |


## BẢNG SĂN

### Preflight

- `git -C cay-kho rev-parse HEAD HEAD^{tree} origin/master`: `916a60ac2d91025879aa420c42aacbf6c26d94c4`, tree `4c2296ee7a22cf389f1a6683aa058fed5c072fa6`, master `e139e55883d90fd74a358230be5599c9e223d4b3`.
- `git status --porcelain` rỗng; `--is-shallow-repository` = `false`.
- `sha256sum .../NO-CAU-LICH-SU-BIEN-NHAN.md` khớp `69394c7658db28196b72e3a1b00f4f6931ad9aba8b9fdcf76563fab33edaa671`.
- Khác lời giao: `git symbolic-ref refs/remotes/origin/HEAD` hiện trả `refs/remotes/origin/agent/wp960-g1-claude` (không vắng). Không sửa cây được review; sẽ đo nguyên trạng và mô phỏng cấu hình CI vắng origin/HEAD trên clone.

HƯỚNG 1: mốc muộn, chuẩn hoá và đổi tên tệp
  giả thuyết : lịch sử câu đã chuẩn hoá chặn sửa hình thức, nhưng mất lịch sử khi đổi tên có thể nhận mốc muộn.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py anchors`.
  output     : plain/folded/literal/list: `anchor-only`, `reformat`, `committed` đều rc=1, chỉ đúng L-ANCESTRY, `chua_do=[]`. `rename-late-anchor {"rc":0,"loi":[],"chua_do":[],"surface_chua_do":[]}`; first=`96b09b49f33141ba96078ae7ffa0d275b9011b1a`, later=`f63ccda53d85dd1c0bce16afa9b5392d6437f4c8`; log đường dẫn mới chỉ có commit rename `62fe2d35e1ad166b4e3fa08305be4cbfb048f642`.
  kết luận   : LỖI ở rename; lỗi khoảng trắng lượt 1 đã đóng trên bốn kiểu scalar. Chi tiết: `evidence/probe-anchors.log`.

HƯỚNG 2: lint, doctrine và phạm vi diff
  giả thuyết : diff gây lỗi F mới hoặc chép doctrine.
  lệnh       : `ruff check --select F --output-format json ...` trên hai tệp head và byte từ `git show origin/master:<tệp>`; `python3 .claude/dev/packet_loop.py doctrine-scan --root .`; `git diff --check origin/master HEAD`; `git diff --numstat origin/master HEAD` (trên clone exact head).
  output     : ruff base=1 F541, head=1 F541 cùng thông điệp `f-string without any placeholders`, delta=0; doctrine `sạch — đã quét 10 tệp, 0 chỗ chép doctrine`; diff-check stdout rỗng, rc=0; numstat `453 10 ops/bien_nhan_v2.py`, `584 2 ops/bien_nhan_v2_test.py` (+1037/-12).
  kết luận   : KHÔNG PHẢI LỖI ở các phép đo này. Không đo được khai báo kích thước trên PR vì không gọi mạng.

HƯỚNG 3: OID không tồn tại thuần số/thuần chữ
  giả thuyết : ngoại lệ cho từ/số thường vẫn bỏ qua OID thiếu được đánh dấu rõ là commit.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py candidates`.
  output     : mọi `_commit_cua` đều null; `Commit 1234abc chua vao master` rc=2; cùng mẫu có backtick với `deadbeef`, `1111111`, 40 ký tự `a`, 40 ký tự `1` đều rc=0, `loi=[]`, `chua_do=[]`.
  kết luận   : LỖI — M2 nói OID không tra được ⇒ rc=2; ca 40 hex với nhãn Commit không có lý do coi là từ ngôn ngữ tự nhiên. `evidence/probe-candidates.log`.

HƯỚNG 4: nguồn surface và phạm vi trích dẫn
  giả thuyết : nguồn có mà hỏng đã được sửa; regex trích dẫn có thể miễn nhầm lời tự khai sau tham chiếu.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py surfaces`.
  output     : nguồn `{`, `[]`, `{}` với/không nợ đều rc=2, không `loi`/nợ chết; chỉ khai sai và hai khai báo cùng dòng đều rc=1; trích dẫn kiểu `ops/land/other/verdict.md:6:` rc=0; `Tham chieu docs/PROTOCOL_DA_PHIEN.md:8; execution_surface: codex_service` cũng rc=0, `loi=[]`, `chua_do=[]` dù run.json=`codex_cli` và không caveat.
  kết luận   : LỖI mới ở miễn trích dẫn quá rộng; lỗi nguồn có mà hỏng và hai khai báo cùng dòng lượt 1 đã đóng. `evidence/probe-surfaces.log`.

HƯỚNG 5: lịch sử tệp không đo được
  giả thuyết : `_commit_them_cau` coi lỗi đọc lịch sử là phiên bản không chứa câu hoặc không chuyển alias vòng thành trạng thái thứ ba.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py historical` (builder c71, chỉ đổi fixture; `main` cũng đo bằng tiêm đúng allowlist fixture).
  output     : `history-yaml-invalid rc=0`, `history-missing-blob rc=0`, cả hai không vi phạm/unknown; `main-fixture-injected` đều rc=0, `TỔNG: ĐẠT`. `history-alias-cycle` ném `_AliasVong: cycle[0]`; `main` cũng ném cùng exception ra ngoài thay vì trả 2. Trong các fixture câu có trước B; bản sửa hiện tại thêm `dung_tai: B`.
  kết luận   : LỖI — YAML lịch sử sai cú pháp và blob thiếu bị bỏ qua, hợp thức hoá mốc muộn; alias vòng ở lịch sử thoát bộ phân ba trạng thái. `evidence/probe-history.log`. Đối chứng UTF8 ở log có phiên bản tốt sớm hơn nên dừng trước bản hỏng; không dùng nó làm finding.

HƯỚNG 6: răng folded của A3
  giả thuyết : sửa thông điệp assert vẫn không làm m78 kiểm đúng folded mà đặc tả đòi.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py a3` (đúng phép thay `_cac_cau` của m78, gọi nguyên c72).
  output     : `m78-fields {"fields":["co_dau","khoi_gap","khong_dau"],"rc":1}`; c72 `giet_that`, lý do duy nhất: `biến thể khối | gãy dòng (khoi_lit) không bị nhận`.
  kết luận   : LỖI nghiệm thu A3 còn nguyên; folded `khoi_gap` vẫn bị bắt dưới mutant. Lượt này lời khai đã thu hẹp đúng, nhưng đặc tả đóng băng chưa đổi. `evidence/probe-a3.log`.

HƯỚNG 7: lỗi git, nhánh mặc định và tệp biên nhận không đọc được
  giả thuyết : lỗi đo phải rc=2; không được traceback/rc=1.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u -c 'import probe_review as p; p.measurement()'` (đổi fixture git/I/O bằng builder có sẵn).
  output     : git hỏng, merge-base rc=127, không có nhánh mặc định, object mốc thiếu đều rc=2, không vi phạm; alias vòng hiện tại ⇒ `KhongDoDuoc`. Thay đúng tệp receipt đã commit bằng symlink tới nguồn không có: CLI thật rc=1, stdout rỗng, stderr traceback `FileNotFoundError`; gọi `kiem` cũng ném `FileNotFoundError`, không `KhongDoDuoc`.
  kết luận   : LỖI ở đọc/băm receipt ngoài khối bắt lỗi. Đây là đường lỗi nền còn tồn tại, không phải regression do ba commit vá mới; prompt (b) yêu cầu đo cả tệp không đọc được. `evidence/probe-measurement.log`.

HƯỚNG 8: gate đầu vào và CI không origin/HEAD
  giả thuyết : thiếu origin/HEAD làm fallback sai trên checkout merge commit đầy đủ lịch sử.
  lệnh       : CLI `PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .` ở cây gốc và clone local từ mirror exact head; clone ghim `origin/master=e139e55…`, xoá symbolic `origin/HEAD`.
  output     : cả hai rc=0, `242 ĐẠT v2 · 11/11 miễn trừ legacy · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 295`; `câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 3 · L-SURFACE chua_do_duoc 0`; `TỔNG: ĐẠT`.
  kết luận   : KHÔNG PHẢI LỖI trên hai cấu hình ref đã đo. Đây là mô phỏng checkout CI ngoại tuyến, chưa gọi GitHub Actions. Log `evidence/gate-original.log`, `evidence/gate-ci.log`.

HƯỚNG 9: tiền đề lịch sử thật của A4 và ngày fixture
  giả thuyết : c73 vẫn chỉ mkdir .git hoặc ngày commit chưa tất định.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u -c 'import probe_review as p; p.acceptance()'`; quan sát nguyên c73 qua builder, độc lập gọi `git rev-parse --verify HEAD`, `git ls-tree -r --name-only HEAD -- ops/reviews`; gọi `_kho_cau` hai lần.
  output     : bốn fixture đều git_rc=0; cả ba tệp `ops/reviews/r.receipt.yaml`, `ops/reviews/v.md`, `ops/reviews/v/run.json` đều trong HEAD; c73 `qua`. Hai lượt B0=`a19f1fcf233fc6c1358ca2e765f2e98cd9cb858d`, X=`3ccd98856a70ffd3358ef59089963f08648370fc`, M=`e72d8570d56391888423561308429963ae4f1b56` giống hệt nhau.
  kết luận   : KHÔNG PHẢI LỖI; finding fixture A4 lượt 1 đã đóng. `evidence/probe-acceptance.log`.

HƯỚNG 10: xuất xứ và tập nợ đóng băng trên base/head
  giả thuyết : tập nợ 64 thiếu/thừa theo bộ chọn hoặc không phải sinh từ base e3ea139.
  lệnh       : clone local mirror, checkout base `e3ea139`; `PYTHONDONTWRITEBYTECODE=1 python3 -u -c 'import probe_review as p; p.debt()'`. Nạp đúng mã luật từ head, truyền root dữ liệu head/base; không sửa source base.
  output     : head-frozen và base-frozen đều rc=0, 0 lỗi/unknown, counts=1/60/3, tập vi phạm 64 bằng đúng hằng, `extra=[]`, `missing=[]`; head-empty và base-empty đều rc=1, 64 lỗi, không unknown; `base-head-parity equal=true`; A7 `new_law_exists=false,new_debt_exists=false,new_A1_exists=false` tại base trước thi công.
  kết luận   : KHÔNG PHẢI LỖI về tập nợ theo bộ chọn hiện hành và A7. Không dùng sự khớp tập này để phủ nhận các phản chứng bộ chọn/mốc ở hướng 1,3,4,5. `evidence/probe-debt.log`.

Bổ sung hướng 5: chạy `main` trong tiến trình Python con (tiêm allowlist đúng fixture như nghiệm thu cho phép, giữ nguyên logic CLI). `history-yaml-invalid-process-fixture-injected` rc=0, `TỔNG: ĐẠT`; `history-missing-blob-process-fixture-injected` rc=0; `history-alias-cycle-process-fixture-injected` rc=1 với traceback cuối `_AliasVong: cycle[0]`. Log đầy đủ `evidence/probe-history.log`.

Đã tạo gợi ý `HINT.patch` CHỈ cho đường lỗi đọc lịch sử và băm receipt. `patch --dry-run --fuzz=0 -p0 -d /tmp/wp960-r2-Dt2G8H/hint < HINT.patch` trên clone exact head trả rc=0, `checking file ops/bien_nhan_v2.py` (`evidence/hint-dry-run.log`). Không áp vào cay-kho. Đây là gợi ý một phần, chưa giải quyết rename/OID/trích dẫn/A3.

Lưu ý giàn đo hướng đột biến: lượt đầu dùng `_dot_bien_tep` nhưng để thư mục mutant ngoài cùng trong `_TAM_DOT_BIEN`; ca sẵn có dọn danh sách này, làm mất tệp mutant ở các ca sau. Lỗi giàn này KHÔNG được tính finding hoặc tín dụng giết chốt. Đã lưu output bị loại ở `evidence/invalid-rig/`, `evidence/probe-mutations-invalid-rig.log`; sửa runner giữ riêng thư mục ngoài cùng và kiểm đường dẫn/byte sau MỖI ca, rồi chạy lại cả 85 CA cho mỗi mutant.

Bổ sung HINT: áp CHỈ trên clone hint rồi chạy lại đúng probe. `history-yaml-invalid`, `history-missing-blob`, `history-alias-cycle` trong tiến trình con đều rc=2; `unreadable-receipt-CLI` rc=2 và `kiem` ném `KhongDoDuoc`. Đây là đối chứng A/B cho hai nhóm lỗi; không thay thế full-suite hay bản vá hoàn chỉnh. Log `evidence/hint-history.log`, `evidence/hint-measurement.log`.

HƯỚNG 11: toàn bộ suite trên head và nền
  giả thuyết : thay đổi phá ca/đột biến cũ hoặc A6 không đạt.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u ops/bien_nhan_v2_test.py` trên clone head exact 916a60a, đầy đủ lịch sử, origin/master=e139e55, không origin/HEAD; cùng lệnh trên clone base e3ea139 nguyên bản.
  output     : head rc=0, `85/85 ca đạt · 95/95 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 77/95 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`; base rc=0, `68/68 ca đạt · 74/74 đột biến thường CÓ RĂNG · 2/2 ca TỰ KIỂM đạt · 56/74 đột biến thường khai đối chứng`, `TỔNG: ĐẠT`.
  kết luận   : KHÔNG PHẢI LỖI về hồi quy suite/đột biến cũ. Các finding phản chứng nằm ngoài phủ của suite; việc cả suite xanh không phủ nhận chúng. `evidence/suite-head.log`, `evidence/suite-base.log`.

HƯỚNG 12: gỡ tám chốt mới khác m73–m82, chạy toàn bộ ca sẵn có
  giả thuyết : sửa lượt1 có thể chỉ thêm nhánh chưa được ca nào khoá.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_mutations.py > evidence/probe-mutations.log 2>&1`. Runner nạp ca từ clone mirror exact916a60a; mỗi mutant gọi `_dot_bien_tep` sẵn có để đổi đúng một mẫu production, kiểm parity nguồn phụ, giữ riêng thư mục mutant ngoài cùng và kiểm byte/đường dẫn sau MỖI ca. Gọi toàn bộ85 CA, không dùng việc phá anchor của mutation harness lồng nhau làm tín dụng.
  output     : các JSON tổng kết thật được rút vào bảng dưới; cặp neo/thay nguyên văn và mọi trạng thái ca nằm ở `probe_mutations.py`, `evidence/r*.log`. Lượt giàn lỗi đã bị loại, nằm riêng trong `evidence/invalid-rig/` và log tên `invalid-rig`.
  kết luận   : KHÔNG PHẢI LỖI ở tám chốt đã gỡ: mỗi cái có ít nhất một ca `giet_that`, không có chốt sống qua toàn bộ85 ca. Các finding dữ liệu/đường chưa phủ được nêu riêng.

| mutant | chốt gỡ (mỗi mẫu khớp đúng1 chỗ) | ca qua/tổng | ca đỏ thật | ca không đo/loại khác |
|---|---|---|---|---|
| r1-moc-oid40 | bỏ đòi mốc đủ40 hex | 84/85 | c71_A2_cau_ancestry_do_bang_merge_base | không |
| r2-luot-other | bỏ kiểm luot hỏng ở receipt khác | 84/85 | c70_A1_luot_KHONG_so_duoc_la_KHONG_DO_DUOC | không |
| r3-merge-error | bỏ phân loại merge-base rc ngoài0/1 | 84/85 | c84_merge_base_HONG_la_KHONG_DO_DUOC_khong_phai_vi_pham | không |
| r4-run-invalid | nguồn surface hỏng trở về không áp | 84/85 | c77_run_json_CO_ma_HONG_la_KHONG_DO_DUOC_khong_phai_no_chet | không |
| r5-history-none | lịch sử không đo được trở thành mốc sai | 84/85 | c85_lich_su_tep_KHONG_DOC_DUOC_thi_moc_la_KHONG_DO_DUOC | không |
| r6-first-file | lấy commit đầu của tệp thay câu | 84/85 | c80_moc_chi_blame_DUNG_cau_duoc_mien | không |
| r7-default-fallback | bỏ fallback origin/master/master | 74/85 | c40_R7_01_nguon_hong_tren_bien_nhan_THAT_khong_ket_toi_bien_nhan_nao, c14_cli_ba_trang_thai, c71_A2_cau_ancestry_do_bang_merge_base, c72_A3_bien_the_co_dau_khong_dau_xuong_dong_deu_bi_nhan, c74_A5_no_cau_lich_su_chi_co_va_no_chet_la_vi_pham, c76_A6_kho_that_voi_no_RONG_phai_DO_dung_bang_so_no, c78_OID_viet_tat_TOAN_CHU_SO_van_duoc_tra, c80_moc_chi_blame_DUNG_cau_duoc_mien, c81_moc_muon_KHONG_tay_trang_duoc_cau_cu_bang_khoang_trang, c82_alias_VONG_la_KHONG_DO_DUOC_alias_dung_lai_van_duyet, c85_lich_su_tep_KHONG_DOC_DUOC_thi_moc_la_KHONG_DO_DUOC | không |
| r8-history-utf8 | bỏ qua phiên bản lịch sử không giải mã UTF8 | 84/85 | c85_lich_su_tep_KHONG_DOC_DUOC_thi_moc_la_KHONG_DO_DUOC | không |

HƯỚNG 13: kiểm ngữ cảnh độc lập của từng mục nợ, đặc biệt ba L-SURFACE còn lại
  giả thuyết : tập64 bằng máy quét vẫn có thể chứa false positive do lời của verdict khác được trích lại.
  lệnh       : `PYTHONDONTWRITEBYTECODE=1 python3 -u audit_debt.py`; `PYTHONDONTWRITEBYTECODE=1 python3 -u -c 'import probe_review as p; p.debt_surface_context()'`; đọc nguyên ngữ cảnh `sed -n '385,425p' ...pr896-review-2...`, `205,222p ...review-3...`, `315,345p ...review-7...`.
  output     : audit độc lập thấy60 tuple ancestry có OID resolve và merge-base rc0, một tuple review có receipt sau đúng SHA và luot2>1, ba tuple surface có text khác run. Nhưng đối chiếu ngữ cảnh chỉ ra cả ba surface là lời của hiện vật KHÁC: pr896 lượt2 các dòng407/418 là output `caveat.mo_ta` cho pr870/pr889, dòng730 nói rõ `Verdict #889 lượt1`; lượt3 dòng213 nằm trong finding về `wp766` (tệp/dòng211 dẫn verdict wp766:12); lượt7 dòng339 là output `SELF:` của `ops/land/pr823...verdict.md:6` được in ở dòng338. Cổng chọn đúng các dòng đó là nguồn của ba tuple nợ.
  output     : fixture c73 chỉ đổi verdict thành `VAN DE: Verdict #khac tu khai ...execution surface codex_service...` ⇒ rc=1; fixture trích `ops/land/khac/verdict.md:6` ở dòng trước rồi `SELF: execution_surface: codex_service` ⇒ rc=1; run của receipt hiện tại vẫn codex_cli, không lời tự khai sai.
  kết luận   : LỖI — M4 hiện khớp64 ứng viên cú pháp, chưa khớp64 vi phạm thật. Ba nợ L-SURFACE còn lại cũng là trích dẫn, cùng loại hai mục bản vá đã gỡ; miễn trích dẫn dựa trên cùng một dòng chưa đủ. Không dùng cờ xác nhận cú pháp của audit-debt làm xác nhận semantic self-claim. `evidence/audit-debt.log`, `evidence/probe-debt-surface.log`.

## FINDING

### doi-ten-tep-tay-trang-cau-cu [P1] Đổi tên receipt cho phép mốc muộn miễn câu đã tồn tại
TỆP/DÒNG: `ops/bien_nhan_v2.py:1141–1143`, `1157–1159`.
VẤN ĐỀ: Q7 đòi mốc là tổ tiên của commit đầu tiên thêm câu. Sau khi câu đã ở receipt cũ tại A, tạo commit B về sau, đổi tên receipt và thêm `dung_tai: B`, `git log -- <đường mới>` chỉ thấy commit đổi tên. Cổng vì thế công nhận B và trả sạch. Giới hạn “không theo dõi đổi tên” không nằm trong ngoại lệ của đặc tả; diễn giải ở dòng 1142 rằng việc này “chặt hơn” bị phép đo bác bỏ. Lỗi khoảng trắng cũ đã đóng, nhưng cùng bất biến nguồn gốc câu vẫn hở qua đổi tên.
ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py anchors` ⇒ cả plain, folded `>-`, literal `|`, list đều còn rc=1 sau sửa khoảng trắng/commit; fixture đổi tên ⇒ `rename-late-anchor rc=0`, không lỗi/unknown. A=`96b09b49f33141ba96078ae7ffa0d275b9011b1a`, B=`f63ccda53d85dd1c0bce16afa9b5392d6437f4c8`; lịch sử đường mới chỉ có `62fe2d35e1ad166b4e3fa08305be4cbfb048f642`. Log `evidence/probe-anchors.log`.
GỢI Ý: tại `_commit_them_cau`, theo lịch sử đổi tên cùng đường dẫn ở mỗi commit, hoặc trả KHÔNG ĐO ĐƯỢC nếu không xác lập được nguồn gốc trước rename. Khoá bằng fixture A/B/rename đã đo, mốc B không được trả 0; giữ ca mốc B0 hợp lệ và câu mới thật sau rename. Rủi ro: copy, rename không rõ và merge không được suy thành cùng nguồn gốc một cách tuỳ tiện. `HINT.patch` hiện chưa có hunk cho finding này.
ĐỘ TIN: cao.

### lich-su-hong-bi-doc-thanh-khong-co-cau [P1] Lỗi lịch sử bị nuốt thành sạch hoặc thoát bộ ba trạng thái
TỆP/DÒNG: `ops/bien_nhan_v2.py:1124–1131`, `1151–1157`.
VẤN ĐỀ: `_co_cau` trả False khi YAML lịch sử không phân tích được; `_commit_them_cau` bỏ qua MỌI rc khác 0 của `git show` như thể commit xoá tệp. Cả hai đường bỏ qua phiên bản có thể đã chứa câu, lấy phiên bản sửa muộn hơn làm lần thêm đầu tiên và công nhận mốc muộn. Mặt khác alias vòng trong phiên bản lịch sử ném `_AliasVong` ra ngoài `main`; chốt chuyển alias hiện tại thành `KhongDoDuoc` không bảo vệ lời gọi mới trong `_co_cau`. Đây là regression từ cách truy lịch sử mới, cùng lớp R4-02.
ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py historical`. Câu đã có trước B; hiện tại có `dung_tai: B`. Phiên bản đầu YAML lỗi cú pháp ⇒ `kiem` rc=0; xoá đúng blob lịch sử khỏi object store của kho fixture ⇒ rc=0; cả hai không `chua_do`. Chạy nguyên `main` trong tiến trình con với allowlist fixture được tiêm: hai ca rc=0, `TỔNG: ĐẠT`. Alias vòng nằm trước scalar trong lịch sử ⇒ tiến trình con rc=1, traceback `_AliasVong: cycle[0]`. Log `evidence/probe-history.log`.
GỢI Ý: giữ trạng thái “không biết có câu” riêng với False; chuyển lỗi YAML/alias thành `KhongDoDuoc`. Khi show lỗi, chỉ bỏ qua nếu đọc tree xác nhận đường dẫn không có, còn blob thiếu/git lỗi phải ra 2. Khoá ba fixture đã đo, giữ ca xoá tệp hợp lệ không bị kết tội. Hunk tham khảo trong `HINT.patch` đã dry-run sạch và cho cả ba probe rc=2 trên clone hint. Rủi ro: không được coi commit xoá tệp thật là bằng chứng lịch sử hỏng, cũng không được làm mất răng của m87.
ĐỘ TIN: cao.

### oid-thieu-thuan-chu-so-bi-bo-qua [P1] OID không tra được vẫn ra sạch chỉ vì không trộn chữ và số
TỆP/DÒNG: `ops/bien_nhan_v2.py:1273–1278`; ca chuẩn hoá ngoại lệ tại `ops/bien_nhan_v2_test.py:2835–2858`.
VẤN ĐỀ: Bản vá đã tra được OID thật toàn chữ/số, nhưng vẫn `continue` khi token thiếu không trộn chữ và số. M2/Q9 không cho miễn OID thiếu theo hình dạng ấy. Ngay câu `Commit <40 ký tự hex> chua vao master`, token được bọc backtick và có nhãn Commit, vẫn ra sạch nếu cả 40 ký tự là `a` hoặc `1`. Lý do tránh nhận nhầm từ thông thường không đủ để bỏ cả OID40 có ngữ cảnh rõ. c78 còn buộc `deadbeef` thiếu phải xanh, chưa đo đúng toàn bộ yêu cầu M2.
ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py candidates`: mọi token đều được xác minh `_commit_cua=null`. `1234abc` ⇒ rc=2; `deadbeef`, `1111111`, `aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa`, `1111111111111111111111111111111111111111` trong cùng mẫu câu ⇒ rc=0, không lỗi/unknown. c78 xác nhận phần OID hợp lệ toàn chữ/số đã sửa, không phủ ca thiếu. Log `evidence/probe-candidates.log`, `evidence/probe-old-cases.log`.
GỢI Ý: tại bộ chọn/xử lý OID, dùng độ dài và ngữ cảnh Commit/OID/backtick để phân biệt từ thường; token OID đã được xác định nhưng không resolve phải đi vào `chua`. Khoá ít nhất hai OID40 thiếu trên cùng fixture c71, thêm OID viết tắt thiếu có nhãn rõ và đối chứng số Actions/từ thường không phải OID. Rủi ro: không áp rc=2 đại trà cho mọi từ hex trong văn xuôi. `HINT.patch` chưa có hunk cho finding này.
ĐỘ TIN: cao.

### tham-chieu-truoc-khai-bao-mien-nham-surface [P1] Một tham chiếu tệp:dòng miễn luôn lời tự khai surface theo sau
TỆP/DÒNG: `ops/bien_nhan_v2.py:989`, `1201–1204`.
VẤN ĐỀ: `_RE_TRICH_DAN.search(dong[:m.start()])` coi bất kỳ tham chiếu đường dẫn kèm số dòng ở phía trước là bằng chứng rằng MỌI khai báo sau nó thuộc hiện vật khác. Regex còn không đòi dấu `:` sau số dòng. Vì vậy văn xuôi tự khai có dẫn nguồn trước đó được miễn L-SURFACE. Điều này trái M3: verdict đang khai surface khác run.json và không có caveat phải vi phạm. Bản vá sửa được ca trích nguyên dòng ở lượt trước nhưng mở đường bỏ sót mới.
ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py surfaces`: run.json=`codex_cli`, verdict `execution_surface: codex_service` ⇒ rc=1. Chỉ thêm tiền tố `Tham chieu docs/PROTOCOL_DA_PHIEN.md:8; ` trước cùng lời khai ⇒ rc=0, `loi=[]`, `chua_do=[]`. Đối chứng trích nguyên dòng `ops/land/other/verdict.md:6: ...` vẫn rc=0 đúng mục đích bản vá. Log `evidence/probe-surfaces.log`.
GỢI Ý: tại `_surface_cua_verdict`, xác định đoạn trích bằng cấu trúc trích dẫn rõ (ví dụ đầu dòng output tệp:N:) và giới hạn phần được miễn; một tham chiếu trong văn xuôi không tự biến lời sau thành trích dẫn. Khoá cặp fixture thêm đúng tiền tố trên, giữ c79 và hai khai báo cùng dòng của c83. Rủi ro: trích dẫn có tiền tố tên receipt ở pr915 và bảng Markdown cần được phân biệt bằng bằng chứng ngữ cảnh, tránh tái tạo false positive cũ. `HINT.patch` chưa có hunk cho finding này.
ĐỘ TIN: cao.

### receipt-khong-doc-duoc-thoat-1 [P1] Băm receipt ngoài khối bắt lỗi làm lỗi I/O thành traceback rc=1
TỆP/DÒNG: `ops/bien_nhan_v2.py:1369–1376`, gọi `_bam` ở `641–642`.
VẤN ĐỀ: `_bam(p)` chạy trước `try` bảo vệ đọc/parse receipt. Tệp không đọc được vì I/O/nguồn biến mất ném OSError ra ngoài cả `kiem` và `main`, thoát rc=1 thay vì 2. Đây là lỗi nền có sẵn trước packet, được giữ là finding vì nhiệm vụ (b) yêu cầu săn đường tệp không đọc được; không quy là regression của ba commit vá.
ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -u -c 'import probe_review as p; p.measurement()'`: kho fixture Git thật, receipt đã commit; thay đúng receipt bằng symlink tới nguồn không có. CLI thật rc=1, stdout rỗng, stderr traceback `FileNotFoundError` tại `_bam`; `kiem` cũng ném `FileNotFoundError`, không `KhongDoDuoc`. Đối chứng git hỏng, merge-base hỏng, nhánh thiếu, object mốc thiếu đều rc=2. Log `evidence/probe-measurement.log`.
GỢI Ý: đưa cả bước băm vào vùng chuyển lỗi I/O thành `KhongDoDuoc`; không coi thiếu nội dung là receipt sai nghiệp vụ. Khoá fixture I/O ở chỗ đọc byte, yêu cầu CLI rc=2 và không traceback, giữ receipt đọc được vẫn qua. Hunk tham khảo trong `HINT.patch` đã dry-run sạch; cùng phản chứng trên clone hint trả rc=2. Rủi ro: thông điệp phải phân biệt lỗi đọc với YAML sai cú pháp; không đổi xử lý allowlist/băm không khớp.
ĐỘ TIN: cao.

### a3-mutant-van-chet-boi-literal [P2] Răng folded của A3 vẫn chưa được đo đúng
TỆP/DÒNG: `ops/bien_nhan_v2_test.py:2688–2699`, `3563–3567` (m78).
VẤN ĐỀ: A3 đóng băng đòi đột biến khớp từng dòng làm ca folded `>-` xanh. m78 đổi `_cac_cau` sau khi YAML parser đã gấp folded thành một dòng nên không làm yếu folded; c72 chỉ đỏ do khối literal `|`. Bản vá đã sửa chú thích và tách assertion để nói rõ điều đó, nhưng việc thừa nhận không thay đổi yêu cầu nghiệm thu và không khép finding cũ.
ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 -u probe_review.py a3`: dưới nguyên phép thay của m78, fields=`['co_dau','khoi_gap','khong_dau']`; `khoi_gap` vẫn có. c72 `giet_that` với thông điệp duy nhất thiếu `khoi_lit`. Không có phản chứng production folded bị bỏ sót trong phép đo này; finding là thiếu phép đo nghiệm thu. Log `evidence/probe-a3.log`.
GỢI Ý: giữ m78 như răng literal và bổ sung một mutant nhắm đường nối dòng vật lý trước/ở parsing để riêng folded mất vi phạm, cùng đối chứng một dòng còn chạy bình thường; hoặc xin thay đổi đặc tả bằng authority riêng, không tự hạ yêu cầu tại test. Khoá bằng khẳng định đúng field folded dưới mutant, không lĩnh tín dụng từ literal hay parser crash. Rủi ro: mutant phá YAML/giàn giáo toàn cục không chứng minh răng folded. `HINT.patch` chưa có hunk cho finding này.
ĐỘ TIN: cao.

### ba-no-surface-con-lai-la-trich-dan [P1] Danh sách nợ vẫn đóng băng ba lời trích thành lời tự khai sai surface
TỆP/DÒNG: `ops/bien_nhan_v2.py:1040`, `1042`, `1047` (ba tuple L-SURFACE; xem tên receipt), `1196–1208` (phân loại lời khai).
VẤN ĐỀ: M4 đòi nợ là vi phạm thật. Cả ba tuple L-SURFACE còn lại — pr896-review-2, review-3, review-7 — đều sinh từ verdict đang trích hoặc mô tả lời khai của verdict khác. Cùng loại false positive mà bản vá đã gỡ hai mục review-8/pr915-review-1 vẫn tồn tại khi dấu trích là ngữ cảnh đoạn văn, code block, hoặc đường dẫn ở dòng trước. Không thể dùng run của reviewer hiện tại để bác surface của người được trích. Việc hằng nợ và tập máy quét cùng bằng3 chỉ đóng băng sai sót của bộ chọn.
ĐÃ THỬ NGHIỆM: `python3 -u -c 'import probe_review as p; p.debt_surface_context()'` tách từng dòng nguồn và gọi nguyên `_surface_cua_verdict` trên fixture. Mọi mismatch của pr896-review-2 chỉ ở dòng407/418 (output caveat cho pr870/pr889) và730 (finding dẫn lời `Verdict #889 lượt1`); review-3 chỉ ở213 (finding wp766); review-7 chỉ ở339 (`SELF:` được in cho đường dẫn pr823 ở dòng338). Dữ kiện ngữ cảnh có nguyên ở các verdict được neo SHA. Hai phản chứng fixture c73 trích bằng văn xuôi/đường dẫn ở dòng trước đều rc=1 dù không tự khai sai. Log `evidence/probe-debt-surface.log`; `audit-debt.log` lưu60 phép ancestry và một phép review độc lập cùng ba candidate surface.
GỢI Ý: tại `_surface_cua_verdict`, phân biệt lời tự khai với lời trích theo block/đoạn và nguồn của đoạn, rồi sinh lại nợ; không chỉ gỡ hằng để nhận nợ chết/vi phạm mới từ thuật toán vẫn sai. Khoá ba dữ liệu thật đã đo bằng fixture có run hiện tại CLI, lời trích service của hiện vật khác; phải rc=0, trong khi tự khai service thật vẫn rc=1. Rủi ro: bỏ qua mọi code block hoặc mọi dòng có chữ “Verdict” sẽ che tự khai thật; cần giữ các phản chứng sai surface ở c73/c83 và finding miễn tham chiếu quá rộng. `HINT.patch` chưa có hunk cho finding này.
ĐỘ TIN: cao.

## HIỆN VẬT VÀ GIỚI HẠN

- `evidence/suite-head.log`, `suite-base.log`: nguyên stdout/stderr của hai full suite, cả hai rc=0. Head giữ85/85,95/95,2/2; base giữ68/68,74/74,2/2. Không ca nào báo `Codex home is inside a repository` trong các output được dùng.
- `probe_review.py`, `probe_mutations.py`, `audit_debt.py`: phép đo ngoại tuyến chỉ gọi ca/builder có sẵn và đổi code/fixture ở bản sao; `evidence/probe-*.log`, `audit-debt.log`, `r*.log` giữ output. Audit64 khẳng định điều kiện cú pháp và Git; ngữ cảnh ba surface được phân xử riêng ở hướng13.
- `HINT.patch`: gợi ý một phần cho lịch sử hỏng/alias và lỗi đọc receipt; đường dẫn áp bằng `patch -p0` từ gốc repo. `patch --dry-run --fuzz=0 -p0 -d /tmp/wp960-r2-Dt2G8H/repo < HINT.patch` sạch tại clone916a60a nguyên trạng, stdout `checking file ops/bien_nhan_v2.py`, rc=0 (`evidence/hint-dry-run-final.log`). Sau áp chỉ trên clone hint, ba lỗi lịch sử và lỗi đọc receipt đều chuyển về rc=2 (`hint-history.log`, `hint-measurement.log`). Chưa đo full-suite trên hint, chưa có hunk sửa các finding còn lại; executor phải tự tái dẫn xuất và kiểm đủ trước commit.
- Chưa gọi GitHub Actions/PR/network. CI ở đây là mô phỏng local: full history, head chứa merge master, origin/master được ghim đúng base và origin/HEAD vắng. Không tuyên bố regex bao phủ mọi biến thể văn xuôi; cũng không suy model thực phục vụ hay tự đặt tên execution surface.

Kiểm cuối: `git -C cay-kho status --porcelain=v1` rỗng; HEAD/tree giữ nguyên như đầu báo cáo; `git -C cay-kho diff --check origin/master HEAD` rc=0, stdout rỗng. SHA256 production ở cây gốc và clone đo đều `ff6b649aa00e77eb8f103641ffa319191245b49376c8da9a611cbde94f84e505`. Cặp gate/master/spec chưa bị đổi trong review.
