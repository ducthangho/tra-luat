# Review mã bo-sinh-bat-bien r1 g1 — lượt 1

**changes_requested — 2 finding P3, 1 lớp; không phát hiện P0/P1/P2.** Hai phản chứng B02 cũ đã đỏ đúng chốt. Lớp còn mở vì hai chốt thiếu phản chứng riêng và một đột biến thay ô cấu trúc vẫn sống. Không tự miễn P3; đây không phải quyền push/merge/land.

- HEAD: `ded412862fba5181fc59e8482ff40cb31162f577`
- Tree: `bcb8e5e85ae95e305274d0b5c82c32bd8c7ff0dd`
- Base: `a89c83acf998008caecba9084a7d295845bf1976`
- Spec SHA-256: `bdde0a9bdba79a19fbbc77cfee8311e209b0c91cc16612bb8029167cca186577` (đã tự băm); revision 1, generation 1, lease đến 2026-11-27T20:55:00Z.
- Reviewer độc lập: `openai_codex / codex_cli / machine/local`; run `efd533b8bf264ca5a8bee54ee6f44cb8`; Linux/Python 3.13.18/Unicode 15.1.0/Ruff 0.15.15; core.abbrev 7.
- CLI 0.172.0 công bố gpt-6-astra/high; model/effort thực phục vụ từng request `KHONG_DO_DUOC`. Sandbox workspace-write; giữ checkout được giao chỉ đọc, mọi bản sao và hiện vật ở work/. Không gọi mạng.

## Bảng lớp và lịch sử

| Lớp | Biểu hiện mở | Cao nhất | Cách vá chung / đóng lớp |
|---|---|---|---|
| `nghiem-thu-khong-co-lap-chot-dich` | R1-01: tổng 158/648 chưa cô lập; R1-02: thay ô bằng bản sao | P3 | Mỗi đường vào có expected độc lập, phản chứng riêng và healthy control cùng đường; kiểm lại 13 chốt và quét các ca A cùng lớp. |

Nguồn: B02 review wp1236 đợt B lượt 4 tại `bca55c1cd09c57180d60b05d5ca1813828ae1d10`. Hai cặp bỏ Mn / bỏ một kiem đã được xác nhận **ĐÃ VÁ THẬT** trong phạm vi cụ thể. Lớp **VA_MOT_PHAN**, không đổi slug hay reset lịch sử. Miễn ở SHA/packet cũ không được suy thành miễn cho hai biểu hiện tại HEAD này.

## R1-01 — P3: hai chốt chưa có phản chứng riêng

Vị trí: `ops/land_evidence_nguon_test.py:900–902`, `c39:925–950`. Kết quả gỡ riêng:

| Chốt | Ca phản chứng | rc | Kết quả |
|---|---|---:|---|
| c36-count | c40 | 3 | DO đúng ca; xem nguyên văn probes.json |
| c36-category | c40 | 3 | DO đúng ca; xem nguyên văn probes.json |
| c36-BMP | c40 | 3 | DO đúng ca; xem nguyên văn probes.json |
| c37-total-executor | c39 | 3 | DO đúng ca; xem nguyên văn probes.json |
| c37-total-literal | c39 | 0 | SỐNG |
| c37-distinct | c39 | 3 | DO đúng ca; xem nguyên văn probes.json |
| c37-category | c39 | 3 | DO đúng ca; xem nguyên văn probes.json |
| c37-648 | c39 | 0 | SỐNG |
| a135-so_phan_tu | a136 | 3 | DO đúng ca; xem nguyên văn probes.json |
| a135-category_vang | a136 | 3 | DO đúng ca; xem nguyên văn probes.json |
| a135-lap_category | a136 | 3 | DO đúng ca; xem nguyên văn probes.json |
| a135-thuoc_cam | a136 | 3 | DO đúng ca; xem nguyên văn probes.json |
| a135-tu_0080 | a136 | 3 | DO đúng ca; xem nguyên văn probes.json |
| a135-cuoi_ngoai_bmp | a136 | 3 | DO đúng ca; xem nguyên văn probes.json |

Bảng 12 của executor tái lập được 12/12 **theo đúng các phép sửa của họ**, nhưng bỏ 648 và phép `c37-total-executor` đổi thêm vế `len(set(vu_tru))==158` thành `==len(vu_tru)`. Với phép gỡ nguyên một mệnh đề, **11/13** chốt làm ca phản chứng đỏ; tổng 158 và 648 sống. Không dùng kết quả 12/12 để tuyên bố đã cô lập mọi chốt.

Đo bổ sung bằng `guard_witnesses.py`: c37 nguyên vẹn rc0 và thực chạy 648 ô. Bỏ riêng ô `(nhan,"",dung)` làm chốt 648 trả rc3 `DO:c37...:số ô lệch đặc tả: 647 (đúng 648)` trước mọi ô; bỏ cả chốt thì 647 ô thật chạy và rc0. Đây là chứng nhân cho tác dụng của chốt, không phải tuyên bố một mutant đơn đã làm HEAD thiếu ô. Thêm bản sao supplementary cuối làm bản gốc đỏ tại vũ trụ 159/158; bỏ vế tổng thì rơi sang chốt 652 ô. Các chứng nhân này có thể đưa vào ca phản chứng riêng.

Gợi ý: trong c39, thêm biến thể lặp **chính supplementary cuối**, và đường sửa danh sách ô mà giữ miền 158 đúng. Neo sửa trong bộ nhớ phải duy nhất; healthy control xanh; gỡ từng chốt phải làm ca phản chứng đỏ đúng DO, có kiểm không vào vòng ô. Tránh sửa hai vế trong một mutant hoặc dùng ky8 câm để nhận tín dụng kiểm consumer.

Xếp P3 `ngoai_bang_dong`: đây là độ nhạy của test mới; HEAD nguyên vẹn đủ miền/648 ô. Không nâng P2 từ lỗi chưa tồn tại trên sản phẩm.

## R1-02 — P3: thay ô a129 bằng bản sao vẫn xanh

Vị trí chốt mới `ops/land_evidence_nguon_test.py:868–872`; nguồn A `:1212`. Đột biến độc lập (neo đúng 1 lần):

```python
kiem(dau + " [khong khop]" + duoi, ten_goc + " [khong khop]")
# thay bằng
kiem(dong, ten_goc)
```

Giữ 36 phần tử và tập category, nhưng mất ô riêng kiểm delimiter sớm không khớp. Cả hai suite trên bản sao đạt: A rc0 CA 53/53, DOT BIEN 158/158; B rc0 CA 40/40, DOT BIEN 145/145; đều TONG DAT. Không khẳng định mọi ca backtracking khác đã mất. Cặp nguyên văn ở `outside-mutant.json`; output đầy đủ ở `probes.json`.

Đây đúng giới hạn spec 8 đã khai, ngoài manifest module và ngoài miền mới mà đặc tả bắt buộc chốt; giữ P3 theo yêu cầu quét lớp, không biến thành P2 hay tự mở rộng write set. Nếu vá: giữ đặc trưng/ID cấu trúc độc lập và phản chứng thay ô bằng ô trùng ở c36/c40. Không áp tính duy nhất lên toàn 8396 phần tử vì các vòng Unicode chủ ý gặp lại đại diện. Nếu giữ ngoài phạm vi, điều phối cần disposition đúng M1/exact SHA; lời khai giới hạn không tự đóng finding.

## Đối chiếu đặc tả và tín dụng thật

Mục 2.1: 128 ASCII+29 đại diện BMP trừ Cs+1 supplementary=158; `lech` kiểm multiplicity BMP, cardinality kiểm thiếu/thừa/trùng; CR/LF không thể nằm trong phần ngoài ASCII khi set cardinality đúng. 648 là literal và hai bang đều trước vòng ô. Trace độc lập: healthy control 648 lượt; cả 35 biến thể c39 có 0 lượt vào thân ô. Mất phản chứng bảo vệ guard là R1-01, không nhầm với lỗi thứ tự hiện tại.

Mục 2.2: sàn cũ đã bỏ. Các kỳ vọng xuất phát từ hằng, không gọi helper đang kiểm. Tự suy từng số hạng từ mã A, chi tiết [independent_counts.md](independent_counts.md):

| Ca | Biểu thức độc lập | Số |
|---|---|---:|
| a124 | 3*(128+19+1)+7*(128+9+2)+6+10*31 |1733|
|a125|24*128+21+3*9+24*30|3840|
|a126|7+12+2+2+29|52|
|a129|6+30|36|
|a131|1|1|
|a132|8*(128+1)+8*31|1280|
|a133|7*128+2*9+5+7*31|1136|
|a134|2*128+2*31|318|

Tổng 8396. a125 có 24 vị trí từ 11 trường (2,2,3,3,2,3,3,2,2,1,1); 21 vị trí ngoài conclusion gặp lại Nd; 3 conclusion gặp lại 9 đại diện L/N/supplementary. a124 có 19 whitespace ngoài ASCII, 7 vị trí skipped và 6 ô rời. a133 có 2 trường LN, 5 trường Nd. a134 duyệt code point một vòng nên không đếm lặp đại diện.

Chốt category c36 là **CHỨA**, đúng 2.2.2. Đọc ký tự từ hồ sơ và mọi byte tệp provenance, thêm parse JSON để thấy Unicode escaped; ngoài BMP kiểm riêng. Dữ liệu fixture có thể góp category sẵn, nên c36 không chứng minh vị trí nào mang category; đây là giới hạn đã khai, không đổi yêu cầu CHỨA thành BẰNG. c37/a135 kiểm helper trực tiếp. c38 giữ 24/24 phản chứng inventory, ca c38 rc0.

Mục 2.3: a135 không trùng 8 tiền tố; kiem_bo_sinh nhận helper làm tham số; đúng 5 bộ đối số và 6 mệnh đề theo hằng đặc tả. Multiplicity tính phần BMP để không tính supplementary Lu thành trùng Lu; đúng baseline. a136 patch globals của chính a135, không vá oracle; phục hồi sau mỗi biến thể.

P1–P7: trace `controls.json` thu 35 âm c37 +4 âm c36 +6 âm a135 =45 phản chứng, tất cả rc3 DO đúng đích, không rc4. c39 ky8 câm chỉ bỏ I/O **sau** chốt; không được nhận là test consumer đầy đủ. c37 thật chạy riêng648 ô trong guard-witnesses. c40 chỉ thu A_CA về 1 ca, theo quyền spec P4/P5; main→L8 vẫn thật. Mock YAML gọi SafeLoader thật theo nội dung và trả deepcopy, không thay parser sản phẩm.

c40 thiếu healthy a129 cùng cache ngay trong ca: reviewer bổ sung cả cached/uncached, đều rc0 qua c36/main/L8. Không thấy tín dụng giả trên HEAD; nên giữ control ấy trong ca để bảo vệ đường cache về sau. c40 healthy a126 và healthy a129 qua c36 đầy đủ cũng xanh. Việc c40 kiểm chuỗi lỗi cụ thể giúp không nhận lỗi vô can thành kill.

## Hai phản chứng B02 nguyên gốc

Dùng đúng raw_cu/raw_moi từ lịch sử (không lấy neo c40 thay vào); script `b02_targeted.py` và `probes.py`. Kết quả trực tiếp:

- `omit-category-Mn` / rc3: `DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a124_token_ascii_qua_ho_so qua main → L8: 1723 phần tử (đặc tả: đúng 1733), rc=0`
- `omit-category-Mn` / rc3: `DO:c37_l8_van_ban_tu_do_tep_danh_gia_qua_cong:vũ trụ ký tự lệch đặc tả: 157 ký tự (157 khác nhau), category lệch ['Mn'], 1 ngoài BMP`
- `omit-lazy-backtracking` / rc3: `DO:c36_l8_ngu_phap_luat_8_qua_bang_cua_dot_a:a129_ten_job_lazy_qua_ho_so qua main → L8: 35 phần tử (đặc tả: đúng 36), rc=0`

Các lượt suite mutant có rc1 là rc tổng của suite; rc3 là tín hiệu từng ca. Không lấy lỗi baseline DOT_BIEN của suite-mutant làm bằng chứng chính; tín hiệu c36/c37 trực tiếp ở trên mới là bằng chứng. Kết quả full:

- B02-omit-category-Mn-B: rc1, CA: 36/40 dat; DOT BIEN: 143/145 bi giet dung ly do; TONG: DO.
- B02-omit-category-Mn-A: rc1, CA: 51/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TONG: DO.
- B02-omit-lazy-backtracking-B: rc1, CA: 38/40 dat; DOT BIEN: 144/145 bi giet dung ly do; TONG: DO.

## Cổng tự chạy

| Lệnh / phạm vi | rc | Bằng chứng dương |
|---|---:|---|
| `head-B`: ops/land_evidence_nguon_test.py |0|CA: 40/40 dat; DOT BIEN: 145/145 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT|
| `head-A`: ops/gate_output_doi_chieu_test.py |0|CA: 53/53 dat; DOT BIEN: 158/158 bi giet dung ly do; TU KIEM PHAN HANG: DAT (2 dot bien); TONG: DAT|
| `head-land`: ops/land_evidence_nguon.py --root . |0|land_evidence_nguon: 153 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 178; TỔNG: ĐẠT|
| `head-ci`: .claude/dev/ci_dang_ky_test.py |0|PHẢN CHỨNG: 1677/1677 đỏ đúng; TỔNG: ĐẠT|
| `head-selftest`: scripts/tl.py --selftest |1|== tl selftest 1773/1789 ==|
| `base-ruff`: ruff check --no-cache --select F ops/land_evidence_nguon_test.py ops/gate_output_doi_chieu_test.py |0|All checks passed!|
| `head-ruff`: ruff check --no-cache --select F ops/land_evidence_nguon_test.py ops/gate_output_doi_chieu_test.py |0|All checks passed!|
| base selftest: python3 -B scripts/tl.py --selftest |1|1773/1789;16 ID đỏ trùng head,failed|
| git diff --numstat a89c83a HEAD |0|2 tệp, +163/−6; trong 320|
| git diff --check a89c83a HEAD |0|không lỗi|
| Ruff pin/probe contract riêng |0|3 mục, errors=[]|

Selftest **FAILED**, không phải passed: base và head cùng rc1, 1773/1789, 16 ID đỏ giống nhau; delta lỗi mới 0. Xem `base-selftest.json` và hai log. Phép đo có giới hạn môi trường: clone scratch thiếu ref origin/master (khác môi trường executor; chưa chứng minh là nguyên nhân ca đỏ), sandbox có `/tmp/.git` trong tổ tiên TMPDIR (các fixture credential yêu cầu ngoài kho). Chưa cô lập nguyên nhân từng ca; không sửa tổ tiên ngoài work/ hay tuyên bố N/N. Executor khai 1789/1789 ở môi trường của họ; lượt này không tái lập được bằng chứng ấy.

Chi tiết command/cwd/rc/thời gian/hash ở `gates.json`, `static-checks.json` và các `head-*.log`. Ruff bare lint head/base 0/0, delta 0; không dùng pin/probe thay bare lint. Không có skipped được coi pass.

## Luật 9 và lựa chọn kho

Đã tự băm công cụ ghim `1b3e4a9e0a4608b9fd6c62e1de99bf509cfd8cb96bedb4d956bac681fc1b9c0c`, tái sinh manifest/hoi_quy/tat_ca, so đủ SHA256SUMS-D của cả 4 thư mục, neo test/module/kho/Python và inventory từng ID+hash. Hai bảng so của executor khớp phép so độc lập:

| Cặp | Tổng | GIET base/head | SONG | VO_CAN | GIET→khác |
|---|---:|---:|---:|---:|---:|
|B|624|438/438|173/173|13/13|0|
|A|946|923/923|23/23|0/0|0|

Tái chạy mẫu bằng chính lệnh ghim `chay`: 2 cặp mỗi module (4 cặp, 8 lượt mutant), mỗi vế chạy baseline đầy đủ trước; các log ghi TAP_CON, không khai HOAN_TAT. IDs/kết quả ở `luat9-audit.json`, `luat9-A/*sample*`, `luat9-B/*sample*`. Chưa tái chạy 622 cặp B và 944 cặp A còn lại, chưa chạy 4 lượt full do.

B dùng kho rỗng, A dùng 201 ID (148 áp dụng, 53 KHONG_AP_DUNG); cả hai vế dùng cùng kho và module byte-identical. Spec không chọn kho, nên đây là phép so không hồi quy hợp lệ **trên inventory được khai**; chọn kho khác mở rộng miền bằng chứng và cần đo mới, không thể suy 0 hồi quy của mọi kho. 53 không áp dụng và nợ SONG/VO_CAN không bị giấu hoặc tự tính GIET.

Lần đầu script audit reviewer chọn một killer c36 nhưng inventory không có nên StopIteration trước sample; sửa chọn mẫu có thật, tái chạy có baseline xanh. Đây là lỗi chọn mẫu của reviewer, không phải finding sản phẩm.

## Thời gian, Windows và phạm vi E

Executor đo cùng lệnh/máy mỗi vế 1 lần: B 349,0→342,4s (−6,6s≤30); A 342,8→343,4s (+0,6s≤5). Log hợp lệ cho lượt đó. Reviewer head B 299.16s, head A 329.11s dưới tải song song; không dùng để tính delta so số executor. Chưa đo lặp để lượng hoá nhiễu; không gọi số này là bảo đảm hiệu năng Windows.

**M3 required**: bước 1 không phải làn lưu trữ; bước 2 khớp dòng mới 974 `read_text(encoding="utf-8")`; dừng tại bước 2, không đi sang unknown hay not_required vì chỉ sửa test. Windows local base/head **not_run**, do điều phối chạy theo spec. Rủi ro cần đo: đường dẫn Unicode/longpaths/tempfile/copytree/rglob; UTF-8/CRLF và neo c40; c40 chạy thêm a129 qua main/L8 với timeout 300s/cached YAML.

**E1–E5 đều khong đối với diff**: chỉ 2 tệp test; không đổi module quyết định hồ sơ land, mã cổng lease/merge, danh sách authority, workflow, secret hay tác động ngoài kho. Finding không biến thành quyền đổi đặc tả hay tự miễn.

## Tái lập và giới hạn

Từ repo, mọi script dùng `PYTHONDONTWRITEBYTECODE=1` và `TMPDIR="$PWD/../work/tmp"`. Lệnh tái lập:

```bash
export PYTHONDONTWRITEBYTECODE=1
export TMPDIR="$PWD/../work/tmp"
python3 -B ../work/probes.py
python3 -B ../work/b02_targeted.py
python3 -B ../work/guard_witnesses.py
python3 -B ../work/trace_controls.py
python3 -B ../work/run_gates.py
python3 -B ../work/audit_luat9.py
```

Các script chỉ sửa bản sao dưới work/; probes.py phục hồi hai tệp bằng finally. Không chạy probes.py đồng thời với một phép đo khác dùng cùng work/mut. Mã phản chứng là dữ liệu review, không phải patch để áp mù lên nhánh executor.

- Bốn lượt full Luật 9 do không tái chạy theo assignment; đã kiểm hiện vật và chạy mẫu chay, không nhận mẫu là HOAN_TAT.
- Windows local base/head và Windows CI: not_run trong review offline; M3 required, điều phối tiếp tục.
- GitHub CI/connector/full_mutant_audit M9, audit uỷ quyền và merge/land: not_run; không gọi mạng.
- Không đo lại delta thời gian full suite base/head trong cùng lệnh; số reviewer là head dưới tải song song.
- Selftest reviewer failed 1773/1789 ở cả base/head,16 ID đỏ trùng; không chứng nhận cổng selftest xanh. Clone scratch thiếu origin/master và sandbox có /tmp/.git; cần môi trường gate chuẩn để lấy N/N. Không sửa ngoài work/ để làm xanh.
- Read-only là kỷ luật reviewer; sandbox workspace-write cho phép ghi checkout. Mọi script đo chỉ ghi work/. Snapshot hai mốc không chứng minh mọi sự kiện trung gian.
- Không kiểm authority/refs GitHub live vì assignment cấm mạng; lease/spec/bundle offline là đầu vào authority.
- Model/effort thực phục vụ từng request KHONG_DO_DUOC. Header CLI công bố gpt-6-astra/high chỉ là evidence phụ, không chứng minh toàn phiên.
- Các mutant test do reviewer dựng không thuộc manifest module; hai finding giữ P3 ngoai_bang_dong. Không dùng tổng suite xanh để đóng lớp.
- Số đo thời gian executor chỉ một lần mỗi vế, đủ chứng minh lượt đo đó trong ngưỡng; không ước lượng độ biến động hay bảo đảm Windows.

HEAD/tree, tracked/index, untracked/ignored status cuối khớp đầu (`snapshot-start.json`, `snapshot-end.json`); `.codex/` đã tồn tại từ đầu. Schema kiểm bằng `python3 ../kiem_verdict_lop.py ../work/VERDICT.json --vong 1`; stdout ở `kiem_verdict.txt`.

KET_LUAN: changes_requested
