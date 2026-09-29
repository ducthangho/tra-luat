verdict: approve
reviewed_spec_sha256: ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1
reviewed_sha: 8eb076b6d5ff41feafa723829d126e2c34c8ba3b
P1: 0   P2: 0   P3: 0
reviewer_provider: openai_codex
model_tu_khai: GPT-6 (Codex); biến thể và effort backend KHONG_DO_DUOC
execution_surface_tu_khai: exec_command thực thi bash trong cwd, Git 2.43.0, Python 3.11.15; danh tính sản phẩm/launcher KHONG_DO_DUOC
transport_tu_khai: KHONG_DO_DUOC

Lượt 10/10. Tree được review: `3cffe001a02ebcc0d8e464b9810ee98566927b3e`.
Đã ghi VERDICT tạm trước khi chạy phép đo, rồi thay bằng kết luận này. Phạm vi: delta lượt 9→10,
đóng F19, đối chiếu C3/C4 và chạy lại các phép nghiệm thu bộ đo được yêu cầu. Không có finding mới
có bằng chứng chạy được. Không thay mức severity vì đây là lượt cuối.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Mục | Trạng thái | Bằng chứng tự chạy và giới hạn |
|---|---|---|
| F19 — P2, `so-do-khong-khop` | **ĐÓNG** | `python3 -B scratch/evidence10.py`: lời khai cũ vẫn ghi 7, liệt kê 8; mục đính chính `HAU-KIEM-CONNECTOR-652.md:128–143` nêu rõ con số sai, đơn vị mới là lời gọi `rep()`. `python3 -B scratch/review10.py generation`: AST đếm 8 lời gọi tại dòng 6, 10, 11, 13, 15, 17, 20, 29; trace thực thi cũng đếm 8. Chạy script nguyên byte trên bản sao r2 đúng đường dẫn yêu cầu: rc0, `cmp` rc0, băm đầu ra bằng SPEC. |
| C3 — khai execution surface / transport | **ĐÓNG-MỘT-PHẦN** | `integrity.json` ghi phiên bản Git/Python thực thi và kiểm hiện vật lịch sử bằng blob HEAD. Header verdict này chỉ khai bề mặt công cụ quan sát được; không suy `codex_cli`, `machine`, model/effort từ bảng S hoặc cấu hình yêu cầu. Không có run.json/header lịch sử của các lượt A1a trong packet để xác minh các lời khai đó. Hai run.json tìm thấy trong kho thuộc PR #468, không chứng minh lịch sử này. |
| C4 — origin và phạm vi ref | **ĐÓNG-MỘT-PHẦN** | `python3 -B scratch/review10.py integrity`: origin đúng `https://github.com/ducthangho/tra-luat.git`, `core.abbrev=7`, 441 cặp tên/OID cache = 441 cặp snapshot, sai khác đối xứng rỗng; băm snapshot khớp `.mirror-info`. Đây là đối chiếu hai hiện vật được cấp, không là readback máy chủ sống và không hồi tố xác minh các lượt cũ. |

**Chấp nhận cách đính chính F19:** giữ nguyên lời khai sai làm hồ sơ, chỉ rõ vị trí và thay con số
bằng một đơn vị đếm tái lập được là đủ sửa lỗi này. Không bắt buộc áp HINT lượt 9 hoặc sửa lại đầu
vào lịch sử. `luot9-EVIDENCE.md` hiện có băm
`59dd7d75ddbada73e7860c3179258ba13e30bc60319a1d682159c8694003d84d`, bằng bản checkout và blob HEAD;
câu “thay đúng 7 đoạn” còn nguyên. Không có bản chụp độc lập ngoài packet để chứng thực nó chính là
byte đã được vận chuyển tới phiên reviewer trước. Điều đó không cản kiểm sự đính chính số đếm hiện tại.

`tao_r3.py` có băm `ce56a45aa939e4cdfceef55a820ca8adc4e04f33c74e555c7bfd02e077a5d15b`.
Đã chứng minh khả năng tái tạo của script được giao; không chứng minh lời khai “trích nguyên văn từ
transcript phiên soạn”, vì transcript ấy không có trong phạm vi đọc.

F17/F18 và C5/C6 không bị delta tái mở. Bảng S vẫn giữ lời đính chính theo từng lượt: E7 lượt 1
430/429 lệch 1; E11 lượt 2 435/435 chỉ so tên; lượt 3 435/435; lượt 4 437/437; lượt 5–7 không đo
được độc lập. Các con số này đối chiếu được với hồ sơ đã cấp, không phải phép đo lại máy chủ lịch sử.
Không mở lại F1 prediction-only, F2 cây mốc + (b), ngoại lệ ADR-0044, trần 10 hoặc quyết định r3 tối thiểu.

## Findings

Không còn P1/P2/P3 trong phạm vi review. Không có đề xuất sửa đặc tả hoặc script.
`HINT.patch` rỗng, 0 byte; không có hunk nhắm `SPEC.md`.

## Bảng đo lại

| Đối tượng | Kết quả | Bằng chứng |
|---|---|---|
| HEAD / tree | đúng hai OID ở đầu verdict; worktree sạch | `scratch/integrity.json` |
| SPEC r3 | 436 dòng, 55.526 byte; sha256 đúng header; packet = checkout = blob HEAD = blob lượt 9 | `scratch/integrity.json` |
| SPEC r2 | 400 dòng, 50.574 byte; sha256 `9bc0fe282fbebc02791f47a30e4ff187b1182a2e5e357ee2e66c04d4f7dac7cd`; bằng origin/master | cùng tệp |
| Phạm vi r2→r3 | chỉ header, thêm §0 vòng 5 và thay chỉ dẫn thi công §8 mục 2; các byte còn lại nguyên r2 | `spec_changes_zero_based`, `permitted_blocks_only=true` |
| DIFF.r2-r3 | payload từ hunk đầu bằng diff tái tạo; khác tên đường header không tính là thay nội dung | `r2_r3_hunks_equal=true` |
| DIFF.luot9-luot10 | byte-equal diff Git từ `3f1bf2e…` tới HEAD; 6 tệp, +362/−0: nối 17 dòng hậu kiểm, thêm 4 hiện vật lượt 9 và script tạo r3 | `delta_names`, `delta_numstat` |
| DIFF.pr658 | byte-equal `git diff origin/master HEAD` | `diff_pr_equal=true` |
| Tái tạo r3 | chạy rc0, cmp rc0, 8 lời gọi tĩnh và 8 lời gọi thực thi; bản sao nguồn r2 không đổi | `scratch/generation.json` |
| Gốc do_q6.py | `36d8f1667aaa72a1bf00dfb7d1ded4331cb65efab5a0376bb3506528fd6d89d0` | bằng HEAD, lượt 9, origin/master |
| Gốc mut_q6.py | `272dc1e82a32331348f59c182803c7cada373f98fbbdd6d4f91ce40d6641e794` | bằng HEAD, lượt 9, origin/master |
| do_q6_hk.py | `0ec537e48b34631eee1e6161be2419bb7ba861a5a446b89afd4937672a974967` | khớp SPEC:388; không đổi từ lượt 9 |
| mut_q6_hk.py | `c4f04f03cf781089ae51faf1e8e63f1d7773bf301d2d61de0919f85a8428bb94` | khớp SPEC:389; không đổi từ lượt 9 |
| Lệnh tự kiểm | rc0, 35 DAT, 0 HONG, cuối `TU_KIEM: 35/35 dat`; byte-equal log cấp | `scratch/self.out`, `scratch/baseline.json` |
| Lệnh ma trận | rc0, 27 DUNG, 0 SAI, cuối `TAT_CA_KHOP`; duy nhất DUNG LECH là `chet-im-lang-rc2`; byte-equal log cấp | `scratch/matrix.out` |
| Lệnh Q6 thật | rc0, byte-equal JSON ghim; sha256 `1fc99cd9339fb5f085436e60ef39bac3058a79dbc009161597ecc7bc85efbd61` | `scratch/q6.out` |
| Giá trị Q6 | 89/89, ngoài miền 3, vi phạm 0, hai chiều 11, một chiều 3, KXD 0, giữ 0 | `scratch/evidence.json` |
| Digest cặp | `8f372ccd2ceab70901868a58d3380acbd89dce25c7127d4d514bc959270fef48` | cùng tệp |
| Mốc / clock | mốc là tổ tiên HEAD và origin/master, cả hai rc0; giờ commit `2026-09-10T11:55:37+07:00` đúng clock ghim | cùng tệp |
| Ref | 441/441 tên/OID, lệch 0; snapshot sha256 `1255ff13558e84dea153893106e95b0f8b4d684c118df44547a525a8677544ac` | `scratch/integrity.json`, `scratch/evidence.json` |
| Bảo toàn | toàn bộ đầu vào cấp ở gốc cwd và 2.222 tệp tracked đã băm trong checkout không đổi; HEAD không đổi, status sạch | `scratch/final-audit.json` |

Ba lệnh chạy với cwd `cay-kho`, đường script tương đối nguyên như SPEC; `<kho>` là đường tuyệt đối
của checkout, `<tmp>` là `scratch/matrix` đã tạo. Argv, rc, băm stdout và stderr nằm trong
`baseline.json`; cả ba stderr rỗng. Sáu opcode diff r2→r3 không phải số lời gọi `rep()`; tám lời gọi
được đo riêng, không lẫn hai đơn vị. 27 là số hàng ma trận, có cả gốc và đối chứng, không phải 27 mutant bị giết.

## Nghiệm thu

**approve** theo ngưỡng 0 P1/P2/P3 của lượt này. F19 đã được đính chính rõ và tái lập được;
không có thay đổi SPEC hoặc bộ đo từ lượt 9. Các phép kiểm được yêu cầu đều đạt; thử bỏ ca tự kiểm,
khai thêm mong LECH hoặc đổi byte script đều bị hợp đồng r3 chặn.

Verdict này là kết luận nội dung tại exact SHA ở đầu tệp. Nó không tự tạo human audit, đóng băng r3,
lease, quyền merge hoặc bằng chứng CI/implementation A1a. Các giới hạn đo C3/C4 vẫn được giữ nguyên,
không suy assurance của transport hoặc lịch sử từ kết quả test xanh.

## Phản chứng đã chạy

Các runner tự đặt `GIT_CONFIG_NOSYSTEM=1`, `GIT_CONFIG_GLOBAL` tới tệp rỗng
`scratch/gitconfig.empty`, `TMPDIR` tới `scratch/tmp`, `GIT_OPTIONAL_LOCKS=0`,
`PYTHONDONTWRITEBYTECODE=1`. Mọi kho giả, mutant và kết quả đều dưới scratch. Không gọi mạng,
không sửa `cay-kho/`; không tự soạn tên thoát cây, đồng tự Unicode, chuỗi thoát hoặc helper/object Git giả.
Tên nhạy cảm được chạy chỉ là fixture nguyên có sẵn trong bộ đo.

Các lệnh tái lập từ cwd:

```sh
python3 -B scratch/review10.py integrity
python3 -B scratch/review10.py generation
python3 -B scratch/review10.py baseline
python3 -B scratch/probes10.py criteria
python3 -B scratch/probes10.py extra_lech
python3 -B scratch/probes10.py mutants
python3 -B scratch/probes10.py classifier
python3 -B scratch/evidence10.py
python3 -B scratch/review10.py final_audit
```

**Tiêu chí dương đỏ được:** `criteria.json` ghi 14 phép đổi bản in/băm/rc và một bản sao script bỏ
ca thật, tổng 15 phép âm đều bị chặn. Bộ kiểm trong runner diễn giải bảng SPEC để thử phản chứng,
không được trình bày như validator có sẵn của sản phẩm.

| Phép đổi | Chốt đỏ đã đo |
|---|---|
| Thêm một byte newline vào từng script | băm riêng của script tương ứng |
| rc mỗi lệnh thành 2, giữ bản in xanh | rc0 của lệnh đó |
| Tổng tự kiểm 34/34 | dòng cuối phải là 35/35 |
| Thêm HONG, giữ tổng 35/35 | 0 HONG |
| Cuối ma trận thành CO_LECH | TAT_CA_KHOP |
| Bỏ một hàng DUNG | đúng 27 DUNG |
| Thêm SAI, vẫn 27 DUNG | 0 SAI |
| Gốc thành DUNG LECH; đổi tên đối chứng âm; hoặc đổi đối chứng âm thành KHOP | duy nhất DUNG LECH đúng định danh |
| Thêm byte khoảng trắng vào JSON Q6 | cmp từng byte |
| Bản sao script bỏ ca `sach`, chạy thật rc0, cuối 34/34 | băm và tổng cố định đều đỏ |

`extra-lech.json`: bản sao harness đổi hàng gốc sang tập đích sai và khai `mong="LECH"`.
Chạy thật vẫn rc0, 27 DUNG, 0 SAI, TAT_CA_KHOP, nhưng có hai DUNG LECH. Cả tiêu chí định danh
đối chứng âm lẫn băm harness đều đỏ. Chỉ rc/tổng số hàng không đủ; r3 đã có các chốt bổ sung đó.

Bản in tự gõ chỉ chứa tổng 35/35 qua được riêng các điều kiện đọc log tự kiểm (`summary_only_failed=[]`).
Nó không đáp ứng bằng chứng đã chạy đúng lệnh trên script ghim. Không coi log giả tùy ý là chứng minh
script ghim có hành vi sai, cũng không coi tiêu chí đọc log là xác thực xuất xứ.

**Bản vá lượt 8 có tác dụng:** chạy lại từng bản mutant do harness sinh; tất cả rc1, stderr rỗng,
không Traceback. Tập HONG bằng đúng tập khai, lưu ở `mutants.json` và các `.out` tương ứng:

| Mutant | Tập HONG thực đo |
|---|---|
| doc-ls-tree-khong-z | ten-co-tab, ten-xuong-dong-sau-duoi, ten-DEL-sau-duoi, ten-byte-sau-duoi |
| bo-chot-ky-tu-dieu-khien | ten-xuong-dong-sau-duoi, ten-DEL-sau-duoi |
| bo-rieng-DEL | ten-DEL-sau-duoi |
| bo-chot-utf8 | ten-byte-sau-duoi |

Hai ca mới phân biệt được việc bỏ riêng hai chốt; không nhận tín dụng từ crash.
Tab vẫn bị chốt tên che khi chỉ bỏ chốt ký tự điều khiển; tập khai mở rộng phản ánh đúng thực đo.
`classifier.json`: trích nguyên hàm phân hạng bằng AST, thử 14 tổ hợp của rc 0, 1, 2, 3, 127,
−9, −15 với tập đích rỗng/có phần tử. Chỉ nhận rc0 cho tập rỗng và rc1 cho tập có phần tử khớp.
Mã âm ở phép này là đối số mô phỏng, không khai đã gửi tín hiệu giết tiến trình trong lượt 10.

## KHÔNG ĐO ĐƯỢC

- Nguồn gốc/thời điểm snapshot máy chủ, advertisement sống, REST comments và CI; không đọc mạng theo packet.
- Transcript tạo r3: chỉ kiểm script hiện có và kết quả tái tạo, không xác nhận provenance transcript.
- Run.json/header, launcher, model/effort backend và transport của các lượt A1a; lời khai mới về lượt 9
  trong hậu kiểm cũng chưa được xác minh độc lập. Không đọc hồ sơ ngoài cwd sau khi nhận chỉ thị trong snapshot.
- Byte thực sự truyền vào phiên reviewer lịch sử ngoài những hiện vật được cấp. Blob equality chứng minh
  tính toàn vẹn trong packet/kho hiện tại, không xác thực toàn bộ chuỗi vận chuyển lịch sử.
- Các tên Git mới hoặc tổ hợp nhạy cảm ngoài fixture đã cấp. Hướng như phối hợp byte không UTF-8 với
  ký tự điều khiển, tên thoát cây, đồng tự hoặc helper/object giả chỉ được nêu bằng lời, chưa thử và không là finding.
- Bộ nghiệm thu implementation A1–A22, Windows/LIVE, human audit và quyền land; không thuộc kết luận nội dung này.
