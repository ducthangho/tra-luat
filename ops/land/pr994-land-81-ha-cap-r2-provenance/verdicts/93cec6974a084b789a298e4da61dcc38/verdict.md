verdict: approve
reviewed_sha: dd877daebbc70c9b74fb883bd69cc52d98b5f33c
so_lop: P0 0 / P1 0 / P2 0 / P3 0
so_finding: P0 0 / P1 0 / P2 0 / P3 0
reviewed_tree: c45281b2c8d560c7b207575909aa47dd20a8c408
base_sha: 44884446f71c89e25f9a72ac58e4f597db63c1ba
packet: land-81-ha-cap / revision 2 / generation 1 / mission 748
review_class: sensitive
provider: openai_codex
execution_surface: codex_cli
transport: machine
run_id: 93cec6974a084b789a298e4da61dcc38
independent_from_executor_session: true
review_axes: [spec, standards_security]

Áp ngưỡng 0 finding P0–P3. Không phát hiện finding còn mở sau khi đo lại toàn bộ (a)–(e) trên head này. Hai finding lượt trước đã đóng. `approve` là verdict về nội dung packet trên exact SHA ở trên, không cấp quyền merge/land và không tự khẳng định runtime assurance §8.1 của lượt reviewer hiện tại.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Đã đọc `verdict-cu/review-1-VERDICT.md` nhưng tự kiểm lại từ Git và YAML, không dùng kết luận hay log của lượt trước làm kết quả đo hiện tại.

| Finding trước | Phân loại | Bằng chứng trên head mới |
|---|---|---|
| F1, P2, #870: bỏ sót `$.cap_nhat_20261026.landed_ly_do` | **ĐÃ VÁ THẬT** | `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml:331` bổ sung đúng đường dẫn; ghi rõ chỉ thay thế lời khai assurance trong câu, giữ phần §10.2.2 và landed. Đường dẫn tồn tại ở dòng 212. |
| F2, P2, #889: cùng thiếu sót | **ĐÃ VÁ THẬT** | `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml:357` bổ sung đúng đường dẫn; cùng giới hạn phạm vi thay thế. Đường dẫn tồn tại ở dòng 238. |

`git -C cay-kho diff 3519c3d dd877da -- ops/land/` → **rc=0**: đúng hai dòng thêm, mỗi danh sách một mục; không sửa dòng khác. `python3 -B review-evidence-r2/check_coverage.py` → **rc=0**: đọc độc lập bản cũ bằng `git show 3519c3d:<tệp>` và bản hiện tại, xác nhận hai đường dẫn trước đây vắng, nay có; mọi mục cũ còn nguyên. Quét lại toàn tệp không phát hiện biểu hiện thứ ba của lớp bỏ sót assurance trong văn xuôi, hoặc lỗi mới do hai mục này gây ra.

## Finding

Không có finding P0–P3.

## Đã đo

Tất cả script, log, bản sao và JSON kiểm kê của lượt này nằm trong `review-evidence-r2/`, ngoài `cay-kho/`. Script do reviewer tự viết; các phép kiểm cổng dùng `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`. Wrapper `measure.py gate` lưu rc thật của tiến trình cổng vào JSON; rc của wrapper không thay cho rc cổng trong bảng dưới.

### Tiền kiểm và đặc tả đóng băng

- Lệnh kiểm đầu tiên sau khi đọc giao việc: `git -C cay-kho rev-parse HEAD` → **rc=0**, đúng `dd877daebbc70c9b74fb883bd69cc52d98b5f33c`.
- `git -C cay-kho show -s --format='%H%n%P%n%T%n%s' HEAD` → **rc=0**: cha trực tiếp `3519c3d07ae8334d4f09560fc0bce52a56b88507`, tree `c45281b2c8d560c7b207575909aa47dd20a8c408`. `git rev-parse --abbrev-ref HEAD` → **rc=0**, `HEAD` (detached checkout). `git status --short` → **rc=0**, rỗng; `git config --get core.abbrev` → **rc=0**, `7`.
- `sha256sum cay-kho/ops/specs/land-81-ha-cap-r2-pr870-889-896.md` → **rc=0**, `ba96df801af3caebd015b43611fdaaf64b48bf8dc8491c46310742fabd7d7bed`. Đã đọc §1–§5 và hai khối tiền lệ r1 trong `ops/land/pr924-wp923-land-evidence.yaml`.
- `python3 -B review-evidence-r2/measure.py audit` → **rc=0**, `AUDIT_PASS`. Script còn đọc `git show 02bdffa:ops/specs/land-81-ha-cap-r2-pr870-889-896.md` và xác nhận byte bằng bản đặc tả hiện tại.

### (a) Nội dung §2 và kiểm kê mọi đường dẫn

Lệnh: `python3 -B review-evidence-r2/measure.py audit` và `python3 -B review-evidence-r2/check_coverage.py` → **rc=0** cả hai.

| Hồ sơ | `reviewer_assurance_81` cấp gốc | `review_exact_sha` | `thuc_thi` | Lá scalar toàn tệp / phần lịch sử | Đường dẫn thay thế |
|---|---|---|---|---:|---:|
| #870 | CHUA_DAT | DAT | model measured; effort và sandbox_mode not_measured, có lý do | 166 / 149 | 7/7 |
| #889 | CHUA_DAT | DAT | Như trên | 173 / 156 | 7/7 |
| #896 | CHUA_DAT | CHUA_DAT | Như trên | 283 / 269 | 4/4 |

Đã đọc toàn bộ ba tệp, duyệt scalar ở mọi độ sâu và quét thêm văn bản thô/comment. Danh sách ứng viên dùng `cross_approved|assurance_81|§\s*8[.]1` không phân biệt hoa/thường; sau đó đọc nghĩa và ngữ cảnh từng câu. Đây là hỗ trợ kiểm kê, không phải chứng minh một regex đủ bao phủ ngữ nghĩa. Mọi lá YAML và các dòng ứng viên được lưu ở `audit.json`; phân loại ở `coverage.json`.

Với cả #870 và #889, đủ bảy đường dẫn đang khẳng định assurance đạt được liệt kê riêng:

1. `$.cap_nhat_20261026.cross_review_moi.assurance`.
2. `$.cap_nhat_20261026.reviewer_assurance_81`.
3. `$.cap_nhat_20261026.reviewer_assurance_81_ly_do`.
4. `$.cap_nhat_20261026.landed_ly_do` — kể cả chữ `dat` viết thường trong văn xuôi về thời điểm comment.
5. `$.pr_ghi_so_duyet_landed_20261026.dieu_kien_da_dat[0]`.
6. `$.pr_ghi_so_duyet_landed_lan2_20261026.dieu_kien_da_dat`.
7. `$.landed_20261026.landed_dieu_kien`, riêng mục (3) review.

Với #896, đủ bốn đường dẫn:

1. `$.cap_nhat_20261026_luot8.cross_review_moi.assurance`.
2. `$.cap_nhat_20261026_luot8.reviewer_assurance_81`.
3. `$.pr_ghi_so_duyet_landed_20261027.dieu_kien_da_dat[0]`.
4. `$.landed_20261027.landed_dieu_kien`, riêng mục (3) review.

Mỗi mục đã liệt kê đều phân giải tới đúng scalar; không có mục trùng hoặc sai đường dẫn. Các câu `CHUA DAT`, giải thích thiếu bằng chứng và điều kiện mở lại `(A) cross_approved` không được nhận nhầm là lời khẳng định đã đạt. Các trường `verdict: approve`, thống kê model hoặc tóm tắt một verdict trong mục nợ là sự kiện review, không tự khẳng định assurance §8.1. Đã kiểm cả các câu ấy khi đọc toàn tệp.

`lich_su` của #870/#889 dẫn đúng `$.cap_nhat_20261026.reviewer_assurance_81`; #896 dẫn đúng `$.pr_ghi_so_duyet_landed_20261027.dieu_kien_da_dat`. Cả ba ghi đúng lỗi connector P1 #934/comment 4372912640 và việc hạ thuộc packet này.

Hai khối mới là hai khóa cuối cùng của mỗi YAML, `ha_cap_assurance_81_20261027` ở cuối tệp. Khối đính chính nói `assurance_81` cấp gốc đã thay thế các lời khai được liệt kê; dẫn đúng comment duyệt landed 6411410063 trên PR #951 cho #870/#889, 6431407190 trên PR #956 cho #896; ghi rõ rút landed là quyết định riêng của chủ kho.

#896 ghi rõ approve trên `fb87110`, khác authorized head `816f439`; việc chủ kho chấp nhận đơn vị land `816f439 + 3bc4244` qua comment 6431407190 là căn cứ landed, không phải căn cứ nâng `review_exact_sha` lên DAT.

### (b) Run, verdict và mọi số/ID mới

Lệnh `python3 -B review-evidence-r2/measure.py audit` → **rc=0** mở trực tiếp đúng ba `run.json` và ba verdict được trỏ tới:

| Hồ sơ / nguồn run | `run_id` đầy đủ / 8 hex đầu | `ma_thoat` | `head` thật | Sự kiện model |
|---|---|---:|---|---|
| #870: `ops/reviews/pr870-review-3-codex/run/run.json` | `941251157e4b4a35be82d6daefb390b2` / `94125115` | 0 | `06a50c5feea77c2654f31edd26efeed7eeee62f5` | DO_DUOC; 21/21 `gpt-6.1-sol` |
| #889: `ops/reviews/pr889-review-3-codex/run/run.json` | `4764bd6fee0645728143c3eb4f1a417b` / `4764bd6f` | 0 | `094e8d17ae4dfcf21dca63702c9262267bdc072c` | DO_DUOC; 19/19 `gpt-6.1-sol` |
| #896: `ops/reviews/pr896-review-8-codex/run/run.json` | `1d140267c72349cc962d449f8959d52e` / `1d140267` | 0 | `fb87110cfab832406984f893e6a4c79fbb932aef` | DO_DUOC; 38/38 `gpt-6.1-sol` |

`authorized_head_sha` của #870/#889 lần lượt bằng hai head ở bảng; #896 là `816f43988eb3012726120ad00166a989cc2b9af6`, khác head approve. Trong cả ba run, `lenh` có đúng `chuong_trinh: codex`, `so_doi_so: 9`, `van_tay`; không lưu danh sách đối số. Duyệt mọi khóa JSON ở mọi độ sâu: không có khóa chứa `effort` hoặc `sandbox`. Số response_id phân biệt cũng lần lượt là 21, 19, 38; mọi sự kiện đều ghi model nêu trên.

Các tệp `ops/reviews/pr870-review-3-codex-verdict.md`, `ops/reviews/pr889-review-3-codex-verdict.md`, `ops/reviews/pr896-review-8-codex-verdict.md` đều có header `verdict: approve`, `reviewed_sha` bằng đúng head runtime tương ứng và kết quả 0 P0, 0 P1, 0 P2, 0 P3. Đây là kiểm nội dung nguồn được dẫn; không chạy lại các review lịch sử.

Đã mở ba readback comment landed trong provenance của chính các hồ sơ: kiểm `id`, PR trong `html_url`, tác giả `ducthangho` và nội dung chấp nhận. #896 có cả `816f439` và `3bc4244` trong quyết định; #870/#889 cùng comment 6411410063 trên #951. Đường dẫn và nội dung nguyên bản lưu trong `audit.json`.

Để kiểm độc lập các ID mới ngoài ba run, dùng plugin GitHub, chỉ GET:

- `github_fetch` với `https://api.github.com/repos/ducthangho/tra-luat/issues/comments/6445221939` → **isError=false**: đúng [comment trên #748](https://github.com/ducthangho/tra-luat/issues/748#issuecomment-6445221939), chiếu lease `land-81-ha-cap-r2-g1-claude-remote-20261027`, revision 2/generation 1, đúng base, spec commit `02bdffa34d6475080a55308b3f45b9006be00712`, SHA-256 và ba đường dẫn write set. Comment tự khai là bản chiếu; không dùng nó thay nguồn authority của lease.
- `github_fetch` với `https://api.github.com/repos/ducthangho/tra-luat/pulls/comments/4372912640` → **isError=false**: đúng [connector P1 trên PR #934](https://github.com/ducthangho/tra-luat/pull/934#discussion_r4372912640), nội dung nêu thiếu effort và sandbox mode thực tế.
- `python3 -B review-evidence-r2/verify_github.py` → **rc=0**, `GITHUB_ID_PASS`, kiểm lại các trường từ phản hồi đã lưu ở `lease-github.json`, `connector-github.json`. Không gọi API ghi.

### (c) Bảo toàn byte, YAML và landed

Lệnh: `python3 -B review-evidence-r2/measure.py audit` → **rc=0**.

| Hồ sơ | Độ dài byte base được giữ nguyên làm tiền tố | Nạp YAML, cấm khóa trùng ở mọi độ sâu | So các khóa cũ với base |
|---|---:|---|---|
| #870 | 19.700 | Đạt | Bằng nhau |
| #889 | 21.931 | Đạt | Bằng nhau |
| #896 | 34.530 | Đạt | Bằng nhau |

Phép đo lấy byte base bằng `git show BASE:<tệp>`, kiểm `head_bytes.startswith(base_bytes)`. Loader riêng từ chối khóa trùng ở mọi mapping, kể cả cấp gốc, trên cả base và head. Sau khi nạp, tập khóa mới đúng `assurance_81`, `ha_cap_assurance_81_20261027`; bỏ hai khóa ấy thì toàn bộ đối tượng YAML bằng base. Không chỉ so các trường được liệt kê trong diff.

Mọi trạng thái và trường landed cũ bằng nhau. Cụ thể `$.landed_20261026.landed` của #870/#889 và `$.landed_20261027.landed` của #896 vẫn `true`; các mốc lịch sử `landed: false` cũng giữ nguyên. Không rút landed.

### (d) Cổng, delta với base và đột biến nguồn

`python3 -B review-evidence-r2/measure.py setup` → **rc=0**. Dựng hai clone cục bộ bằng `git clone --no-hardlinks --no-checkout cay-kho <đích>`, rồi checkout detached exact base vào `review-evidence-r2/base/` và exact head vào `review-evidence-r2/mutation/`. Cả hai ngoài `cay-kho/`, checkout sạch trước khi đo/đột biến, `core.abbrev=7`. Lệnh và rc từng bước nằm ở `setup.json`.

Các lệnh cổng thực chạy từ thư mục từng cây bằng `measure.py gate <head|base|mutation> <land|receipt|doctrine>`:

| Lệnh cổng | Cây | Rc thật | Dòng tổng / bằng chứng dương |
|---|---|---:|---|
| `python3 ops/land_evidence_nguon.py --root .` | Head thật `cay-kho/` | 0 | `land_evidence_nguon: 53 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 78`; `TỔNG: ĐẠT` |
| `python3 ops/bien_nhan_v2.py --root .` | Base `44884446` | 2 | `bien_nhan_v2: 244 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 513 KHÔNG ĐO ĐƯỢC · tổng 297`; `TỔNG: KHÔNG ĐO ĐƯỢC` |
| `python3 ops/bien_nhan_v2.py --root .` | Head thật | 2 | Cùng dòng tổng với base: 0 vi phạm, 513 KHÔNG ĐO ĐƯỢC; `TỔNG: KHÔNG ĐO ĐƯỢC` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Base `44884446` | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |
| `python3 .claude/dev/packet_loop.py doctrine-scan --root .` | Head thật | 0 | `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine` |

So riêng stdout và stderr head/base: cả hai luồng bằng byte ở cả hai cổng. **Delta vi phạm = 0; delta KHÔNG ĐO ĐƯỢC = 0**, không có lỗi mới bù trừ lỗi cũ. Thống kê câu lịch sử cùng là `nợ L-REVIEW 1 · L-ANCESTRY 6 · L-SURFACE 3 · L-SURFACE chua_do_duoc 0`. `bien_nhan_v2` không được coi là pass tuyệt đối: clone nông thiếu object lịch sử, cổng trả rc=2 đúng trạng thái. Tiêu chí packet ở đây là không tăng lỗi hoặc phần chưa đo so với base; tiêu chí delta đạt.

Log và rc thật: `review-evidence-r2/{head-land,head-receipt,base-receipt,head-doctrine,base-doctrine}.{json,stdout.txt,stderr.txt}`. Kết quả so byte: `gate-comparison.json`.

**Đo răng:** `python3 -B review-evidence-r2/measure.py mutate` → **rc=0**. Chỉ trên clone `mutation/`, thay đúng một token ở `$.assurance_81.thuc_thi.model` của #870 từ `ops/reviews/pr870-review-3-codex/run/run.json` thành `ops/reviews/reviewer-missing-source/run.json`; đã kiểm đường dẫn mới không tồn tại. Các token nguồn khác và tiền tố byte base còn nguyên. Setup đột biến ở `mutation.json`.

`python3 -B review-evidence-r2/measure.py gate mutation land` chạy lại `python3 ops/land_evidence_nguon.py --root .` → **rc cổng=1**:

```text
ĐỎ ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml: 1 vi phạm
  L1 $.assurance_81.thuc_thi.model: lời khai đo không có token nguồn phân giải được
land_evidence_nguon: 52 ĐẠT · 25/28 miễn trừ (băm khớp) · 1 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 78
TỔNG: ĐỎ
```

Dòng L1 trên rút gọn phần nhắc lại token/giá trị; nguyên văn đầy đủ và rc ở `mutation-land.stdout.txt`, `mutation-land.json`. Cổng bắt đúng lời khai mới bị làm hỏng; không phải lỗi dựng bản sao.

### (e) Trần và đường dẫn cấm

`git -C cay-kho diff --stat BASE HEAD`, `git -C cay-kho diff --numstat BASE HEAD`, `git -C cay-kho diff --check BASE HEAD` → **rc=0**. Trong các lệnh này BASE/HEAD lần lượt là full OID ghi đầu verdict.

| Tệp được đổi | Dòng thêm | Dòng xóa |
|---|---:|---:|
| `ops/land/pr870-claude-md-bai-hoc-c-land-evidence.yaml` | 39 | 0 |
| `ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml` | 39 | 0 |
| `ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml` | 38 | 0 |
| Tổng | **116** | **0** |

Đúng ba tệp write set, trong trần ≤3 tệp/≤180 dòng thêm. Không đổi `ops/land_evidence_nguon.py`, test, hay bất kỳ tệp `ops/reviews/`. Phép đo (c) xác nhận không rút landed hoặc đổi trường lịch sử. Không tạo provenance trong repository, không chạy lại review cho ba PR lịch sử.

### Bảo toàn checkout và giới hạn runtime hiện tại

Snapshot trước các phép chạy cổng và `python3 -B review-evidence-r2/measure.py snapshot-after` → **rc=0**. `snapshot-before.json`, `snapshot-after.json`, `snapshot-comparison.json` xác nhận **whole_snapshot_equal=true**, **changed_paths=[]**, 7.358 tệp được kiểm, HEAD/tree/index hash bằng nhau, status gồm cả untracked/ignored rỗng. Các tệp thuộc đường dẫn cấu hình nhạy cảm chỉ so metadata; các tệp còn lại băm byte. Snapshot hai thời điểm không chứng minh một lịch sử tuyệt đối chưa từng có ghi rồi hoàn nguyên.

Định danh provider/surface/transport/run ở đầu verdict đối chiếu trực tiếp `run/93cec697/run.json`. Khi đọc, run còn `dang_chay`; chưa có các trường model/effort/sandbox runtime đã chốt. Không suy model hoặc effort của reviewer hiện tại từ ba run lịch sử. Cấu hình quyền công cụ được cấp cho phiên là `workspace-write`; checkout được đối xử read-only và snapshot kiểm không đổi. Launcher trong base có mã ghi `effort_phuc_vu` và `sandbox_trang_thai`; biên nhận hoàn tất sau khi reviewer thoát thuộc bước chốt của launcher, ngoài phép đo nội dung ba hồ sơ. Phần chưa chốt này không được gọi là execution assurance đã đạt.

Không sửa `cay-kho/`, không push, không gọi API ghi GitHub. Các phản chứng chỉ dùng nguồn thiếu bình thường trong cây tạm; không tự soạn nội dung dò thoát đường dẫn.
