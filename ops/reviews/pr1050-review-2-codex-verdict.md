verdict: approve
reviewed_sha: f37b5195978f1fe35b9cb55b6f79a2e09d165af0
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Review độc lập lượt 2 của PR #1050. Chỉ đọc cây `cay-kho/`; mọi đột biến dữ liệu được thực hiện trên bản sao tạm từ `mirror.git`. Không push. Một lần chạy lệnh sẵn `ai-dang-giu` đã vô ý thử `ls-remote` bên trong và bị môi trường chặn, không nhận được dữ liệu mạng; ghi đầy đủ tại hướng 11. Các kết luận dưới đây dùng blobs/readbacks offline và các phép thử cục bộ.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact head/tree | f37b519, base b29da0b | Hướng 1: `git rev-parse`; HEAD `f37b5195978f1fe35b9cb55b6f79a2e09d165af0`, tree `235444656cad85bd969f99907b1dbeb4007d961a` | Có |
| Phạm vi chỉ ghi sổ | Ba commit, ops/reviews + ops/land, không mã | Hướng 1: `git log`, `git diff --stat`: 33 tệp, +11665/−0; chỉ hai thư mục đã khai | Có |
| Nguồn handoff và lease | Nhánh ops/wp1037-r1-g1-lease | Đóng băng `a34b9a38cda2669f9a90958c69bb6f2faa0f4353`; `measure_artifacts.py`, `measure_lease.py` đọc blob theo OID | Có |
| Verdict lượt 1 nguyên byte | Flat = directory = gốc | Hướng 2: 14251 byte; SHA256 `e33a3c3efdeb3d55c7dd2c45ae831d814861690c360071b706026f4c9ed2a95b`; cả ba bằng nhau | Có |
| Verdict lượt 2 nguyên byte | Flat = directory = gốc | Hướng 2: 10679 byte; SHA256 `2f482565c235380145253d76ae51ab9606e8d7cfc8044d6efd113ff80049feaf`; cả ba bằng nhau | Có |
| Hai PROMPT nguyên byte | Chép nguyên gốc | Hướng 2: 3977 / 3907 byte; SHA256 `ca20a3a0…88dc` / `d1d75feb…a75d`; SOURCE_EQUAL và HEAD_EQUAL True | Có |
| Hai run.json nguyên byte | Chép nguyên gốc | Hướng 2: 10930 / 10492 byte; SHA256 `58050918…3e8b` / `21dfe28a…c629`; SOURCE_EQUAL True | Có |
| Manifest và tập tệp | SHA256SUMS đủ, đúng | Hướng 2: 6/6 + 6/6 + 12/12 OK, missing/extra rỗng; manifest nguồn 6/6 đúng | Có |
| Checkpoint/stdout/stderr | Thuộc đúng run | Hướng 2: hash và stdout/stderr byte count khớp; checkpoint run/head/prompt khớp | Có về nội bộ; không có bản handoff phụ riêng |
| Schema và receipt identity | v2, review_delivery_receipt, hậu tố hash | Hướng 5: từng FIELD MATCH True, receipt_id_hash_suffix True cả hai | Có |
| Packet/revision/generation/lease/class | #1037, r1/g1, wp1037-r1-g1-claude, sensitive | Hướng 5: các LEASE_FIELD MATCH True, risk/class và scope ops khớp | Có |
| Verdict/counts lượt 1 | changes_requested, 0/0/1/2 | Hướng 5: chuẩn hóa request_changes; đếm dòng finding gốc khớp cả bốn số | Có |
| Verdict/counts lượt 2 | approve, 0/0/0/0 | Hướng 5: dòng đầu và bảng không finding khớp; count 0/0/0/0 | Có |
| Slug và xử lý findings packet | Ba P2/P3 lượt 1, lượt 2 đã xử lý | Đọc hai verdict nguyên byte: ba slug/hạng khớp; lượt 2 có bảng mutant cũ và giới hạn mutant sống | Có về ghi sổ |
| Reviewed SHA/tree lượt 1 | 016852a | Hướng 5: receipt = run = verdict; tree `6907a286e95a2c6e86c7c08c0ec700dc2a75ef58` | Có |
| Reviewed SHA/tree lượt 2 | 9146632 | Hướng 5: receipt = run = verdict; tree `c20eace3f4aacea3f33afc5861688cb94d64cf3d` | Có |
| Base | Base packet 757bde5; base PR ghi sổ b29da0b | Lease `base_sha:757bde561d09738858506aecf5de2f050a5f0d5e`; ancestry rc 0, PR readback khớp | Có; tree/base là khóa tùy chọn vắng trong receipt |
| Hash/bytes/path biên nhận | Trỏ bản phẳng đúng byte/hash | Hướng 5: VERDICT_HASH_MATCH/BYTES_MATCH True cả hai, tên/path đúng | Có |
| evidence_url và anchor | Blob e788a5d, cùng nhánh; strength thấp | Hướng 5: exact blob bytes khớp, e788a5d → f37b519 rc 0 | Có |
| Ancestry và trạng thái PR ghi sổ | Reviewed head đã vào b29da0b; ghi sổ chưa merge | Hướng 5: 016852a/9146632 → b29da0b rc 0; b29da0b^2=9146632; f37b519 → master snapshot rc 1 | Có về Git snapshot; không suy PR trực tuyến |
| Hai run terminal/rc/prompt/thời lượng | 4d0668e2 / e400a320, xong, rc0 | Hướng 6: đúng run/head/prompt, 934.249 / 567.318 s, sạch lúc phóng | Có |
| Run nằm trong cửa sổ lease | 09:08:51Z / 09:34:41Z | Hướng 6: START_IN_LEASE True cả hai, trong [08:57Z,17:53Z) | Có |
| Model thực phục vụ và mức bằng chứng | gpt-6-astra do_may; xhigh | Hướng 6: DO_DUOC, 27/27 và 19/19 event cùng model; effort [xhigh] | Có |
| Model yêu cầu/CLI version/cờ | gpt-6-astra, codex-cli 0.164.0, flags | run chỉ lưu chương trình/số args/fingerprint; không có raw argv/version | KHÔNG ĐO ĐƯỢC độc lập cấu hình yêu cầu |
| Provider/surface/transport/run ID | openai_codex/codex_cli/machine | Hướng 6: bốn identity field = metadata đúng run | Có theo nguồn lưu |
| Assurance | cross_reviewed lượt 1, cross_approved lượt 2 | Khác họ model theo run reviewer/lease executor; lượt 2 approve 0/0/0/0, đúng head; không nâng thành merge authority | Có trong phạm vi evidence |
| Executor và submitter | Claude theo lease, actor ducthangho theo lời khai | Lease model/family khớp; không có runtime executor/readback push của PR ghi sổ; actor_nguon gắn (b) | Phần lời khai KHÔNG ĐO ĐƯỢC độc lập |
| Sandbox và caveat | Workspace có quyền ghi; scripts ngoài kho | Hướng 6/9: nguồn permission observations, run1 KHONG_DO_DUOC/run2 DO_DUOC; README đủ bốn caveat | Có với giới hạn lấy mẫu |
| Spec và write set | spec hash253f12ae…, write_set_hash d7872905… | Hướng 3/5: blob spec e16fb55/a34b9a3 cùng hash; băm JSON danh sách đúng d7872905… | Có |
| Finding cũ P1 lease | Chưa nhả tại 17:37Z, hạn mới17:53Z | Hướng 3: classifier CÒN_HẠN tại17:37/17:41; HẾT_HẠN từ17:53; các câu lịch sử đã sửa | **ĐÓNG / ĐÃ VÁ THẬT** |
| Khối đo mới | Đo18:07:34Z: #1037 HẾT_HẠN, holder #1021 | Hướng 3: log cbc0c4a3… đúng hash/header/rc11; classifier hai lease khớp; mốc trước commit vá18:08:52Z | Có; không phải trạng thái hiện hành |
| Đủ ref ở mốc mới | Log khai708/708, thiếu/thừa0/0 | Offline có708 tên + HEAD symref; log lưu summary, không có danh sách OID máy chủ | Khớp nguồn; tập máy chủ lịch sử KHÔNG ĐO ĐƯỢC độc lập |
| Finding cũ P2 Windows | Count/step/labels measured; input và root cause thuật lại | Hướng 7: metadata chứng minh count/steps/runner; câu mới nêu rõ thiếu inputs/log chẩn đoán | **ĐÓNG / ĐÃ VÁ THẬT** |
| CI PR Ubuntu | Run41033737059 attempt1 success23/23 | Hướng 7: đúng repo/head/event/attempt, 23success và23ubuntu-latest | Có ở mức Run/jobs |
| Windows attempts | Run41069257658: a1 13success/2failure/1skipped; a2 15success/1skipped | Hướng 7: total_count=length=16, run conclusions failure→success;14Windows+1Ubuntu+1không runner | Có |
| Rerun job lỗi | Attempt2 sau rerun một lần | Hướng 7: attempt2;13job success giữ nguyên runtime,2failed có runtime mới, job gộp vẫnskipped | Khớp hành vi; request endpoint không lưu |
| Windows runner/N/N | gate-ops job124108765783 runner1000026073;95/95,137/137,2/2,lease255/255 | Hướng 7: job/runner/label/conclusion đúng; N/N không có job log, được gắn thuat_lai | Metadata khớp; N/N KHÔNG ĐO ĐƯỢC độc lập |
| Merged/head/base/parents/tree/diff | PR1041 merged17:28:50Z b29da0b | Hướng 8: API/Git khớp; diff40b6d80f… bằng nhau, +120/−4 một tệp test | Có |
| Authorization/operator | Chủ tài khoản merge; chỉ thị có điều kiện không SHA | Hướng 8: account OWNER/merged_by đúng; comment không full authorized SHA; người thật/phiên credential tách lời khai | Có với giới hạn được khai |
| Connector | not_measured, running thuật lại | Không lưu readback comment6529077259; nguồn không được nhận measured | Đúng trạng thái thiếu bằng chứng |
| Push master pending | Run41099184556 pending **lúc17:37Z ghi sổ** | Hướng 8: snapshot pending/null, headb29da0b; mọi câu pending có ngữ cảnh ảnh chụp | Có tại snapshot; không đo hiện tại |
| §10.2.2 | Run có nguồn; Checkout/definition/output chưa đo | Hướng 8: REST có run identity; thiếu ba loại nguồn còn lại, GraphQL403 chỉ thuật lại | Đúng trạng thái thiếu nguồn |
| §8.1 thực thi reviewer lượt2 | Model/effort/sandbox đo được có giới hạn | Hướng 6:19model events, xhigh, permission observations và sampling caveat khớp | Có; không thay CI provenance |
| landed:false | Chưa đủ post-merge evidence/approval exact SHA riêng | Hướng 8: thiếu ba mốc CI, hồ sơ không suy merged=landed; lease mới không xóa các điều kiện này | Có |
| README | Hai mục lục+bốn caveat, không trùng | Hướng 9: mỗi mục/caveat count1; sáu link đích có; status/counts/bytes khớp | Có |
| Sáu cổng baseline | Rc0 và marker dương/N=N | Hướng 4: bien_nhan/land TỔNG ĐẠT, doctrine sạch, t26 1/1,t27 2/2,t138 1/1 | Có |
| Răng cổng dữ liệu | Đổi byte/xóa README/đổi so_p1 | Hướng 10: byte→t26rc1; README→t27rc1; so_p1→cả sáu rc0 | Có răng hash/mục lục; **không có răng số đếm** |

## BẢNG SĂN

Nhật ký được nối sau mỗi hướng thử; đã hoàn tất các hướng dưới đây.

### Hướng 1 — Khóa định danh và phạm vi (KHÔNG PHẢI LỖI)

Lệnh: `git -C cay-kho rev-parse HEAD HEAD^{tree} refs/remotes/origin/master refs/remotes/origin/ops/wp1037-r1-g1-lease`; `git -C cay-kho rev-parse --is-shallow-repository`; `git -C cay-kho status --short --untracked-files=all --ignored=matching`; `git -C cay-kho log --format='%H %T %cI %s' b29da0b..HEAD`; `git -C cay-kho diff --stat b29da0b HEAD`.

Output thật:
```text
HEAD f37b5195978f1fe35b9cb55b6f79a2e09d165af0
TREE 235444656cad85bd969f99907b1dbeb4007d961a
origin/master b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
origin/ops/wp1037-r1-g1-lease a34b9a38cda2669f9a90958c69bb6f2faa0f4353
is-shallow-repository false
status --short: (rỗng)
e788a5d 2026-10-30T17:34:39+00:00 hiện vật
c24875d 2026-10-30T17:41:02+00:00 biên nhận và hồ sơ land
f37b519 2026-10-30T18:08:52+00:00 vá lượt 1
33 files changed, 11665 insertions(+)
```

Diff chỉ thuộc `ops/reviews/**` và `ops/land/**`; đóng băng nguồn lease bằng OID `a34b9a38cda2669f9a90958c69bb6f2faa0f4353`, không dùng tên nhánh làm định danh.

### Hướng 2 — Nguyên byte và tập hiện vật (KHÔNG PHẢI LỖI)

Lệnh: `python3 evidence/measure_artifacts.py | tee evidence/artifacts.log`. Script đọc blob bằng Git OID cố định ở trên, so byte với exact HEAD, băm toàn bộ manifest và đối chiếu tập tệp.

Output thật (trích; đầy đủ ở `evidence/artifacts.log`):
```text
ROUND 1 PROMPT.md bytes=3977 sha256=ca20a3a06a82643b7d48fe3185600a35d00d4dc7d7e45c4dd7409c5b142d88dc SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 1 VERDICT.md bytes=14251 sha256=e33a3c3efdeb3d55c7dd2c45ae831d814861690c360071b706026f4c9ed2a95b SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 1 run/run.json bytes=10930 sha256=58050918256f449a93a69403f46623d45dadb4f0888492d65d09a31cb7323e8b SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 1 FLAT bytes=14251 sha256=e33a3c3efdeb3d55c7dd2c45ae831d814861690c360071b706026f4c9ed2a95b DIRECTORY_EQUAL=True SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 2 PROMPT.md bytes=3907 sha256=d1d75feb247d2e20d64c5cbceffb2dd50fdbed8efa65f5accff67c72c339a75d SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 2 VERDICT.md bytes=10679 sha256=2f482565c235380145253d76ae51ab9606e8d7cfc8044d6efd113ff80049feaf SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 2 run/run.json bytes=10492 sha256=21dfe28a8d9410c39cfe3c02e2ece250bad1ec75e134c38f7ae25ddaf74ac629 SOURCE_EQUAL=True HEAD_EQUAL=True
ROUND 2 FLAT bytes=10679 sha256=2f482565c235380145253d76ae51ab9606e8d7cfc8044d6efd113ff80049feaf DIRECTORY_EQUAL=True SOURCE_EQUAL=True HEAD_EQUAL=True
MANIFEST_SET ops/reviews/wp1037-g1-codex-luot1 entries 6 files 6 MISSING [] EXTRA []
MANIFEST_SET ops/reviews/wp1037-g1-codex-luot2 entries 6 files 6 MISSING [] EXTRA []
MANIFEST_SET ops/land/pr1041-wp1037-provenance entries 12 files 12 MISSING [] EXTRA []
SOURCE_MANIFEST luot1-PROMPT.md True
SOURCE_MANIFEST luot1-VERDICT-codex.md True
SOURCE_MANIFEST luot1-run.json True
SOURCE_MANIFEST luot2-PROMPT.md True
SOURCE_MANIFEST luot2-VERDICT-codex.md True
SOURCE_MANIFEST luot2-run.json True
```

Mọi `stdout.log`, `stderr.log`, `checkpoint.json` khớp hash trong đúng `run.json`; byte count stdout/stderr khớp. Checkpoint cả hai lượt có đúng run ID/head/prompt hash. Ba tệp phụ không có bản handoff gốc riêng để so độc lập, nên chỉ xác nhận tính nhất quán nội bộ của chúng. Không thiếu/thừa tệp so với ba `SHA256SUMS`; cả sáu tệp gốc trong handoff được giữ nguyên.

### Hướng 3 — Nhiệm vụ 0: lease và mốc đo mới (KHÔNG PHẢI LỖI)

Lệnh: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_lease.py | tee evidence/lease.log` (gọi hàm có sẵn `_phan_loai_lease` với `bay_gio` tường minh); `nl -ba cay-kho/ops/land/pr1041-wp1037-land-evidence.yaml`; `git -C cay-kho show -s --format='%H %cI %s' a34b9a3`.

Output thật:
```text
LEASE_SOURCE_EQUAL True sha256 b1738f6ffa3edd8f03aada2b84c863ec74676f7c02acf05e9b409e7e2168b039
CLASSIFY 2026-10-30T17:37:00Z CÒN_HẠN
CLASSIFY 2026-10-30T17:41:02Z CÒN_HẠN
CLASSIFY 2026-10-30T17:53:00Z HẾT_HẠN
CLASSIFY 2026-10-30T18:07:34Z HẾT_HẠN
CLASSIFY 2026-10-30T18:08:52Z HẾT_HẠN
SHORTENING 2026-10-30T17:33:00Z 2026-10-30T17:53:00Z 2026-10-30T17:53:00Z
AFTER_EXPIRY_LOG_SHA256 cbc0c4a31a8df98e835ea232a96b4339cf763b3c7d302a087f7de4c23c1ba765
LOG_SUBJECT wp1037-r1-g1-claude ref_oid a34b9a38cda2669f9a90958c69bb6f2faa0f4353 expires 2026-10-30T17:53:00Z AT_180734 HẾT_HẠN
LOG_SUBJECT wp1021-r2-g1-claude ref_oid 71f96cf257425147440c0391b5e62928b1570435 expires 2026-10-31T08:57:00Z AT_180734 CÒN_HẠN
OFFLINE_REF_NAMES 708 PLUS_HEAD_ALIAS 1
```

Đọc trực tiếp nguồn `ai-dang-giu-sau-rut-han/luc-do.txt` (đã khớp manifest): header ghi `2026-10-30T18:07:34Z`; summary `708/708`, thiếu/thừa `0/0`; có dòng `HẾT_HẠN wp1037-r1-g1-claude`, dòng `CÒN_HẠN wp1021-r2-g1-claude`, `NGƯỜI_GIỮ 1: wp1021-r2-g1-claude`, `rc=11`. Mốc đo sau hạn 17:53Z và trước commit vá 18:08:52Z. Không diễn giải rc=11 thành đường ghi trống.

**`nha-lease-truoc-khi-het-han`: ĐÓNG / ĐÃ VÁ THẬT.** Dòng 70–73 giữ quá khứ “CHƯA NHA tại 17:37Z”; dòng 74–77 là khối đo mới có mốc và nguồn riêng; dòng 88, 93–94 cũng dẫn đúng phép đo mới. `NGƯỜI_GIỮ` được khai trong chính khối `do_lai_sau_han_20261030T1807Z`, không được khai là hiện hành. Không còn kết luận đã nhả lúc 17:37/17:41.

Giới hạn tái lập: không gọi mạng nên không đo lại được tập ref máy chủ tại 18:07:34Z; log chỉ lưu summary, không lưu danh sách tên/OID máy chủ. Số 708 khớp tập ref offline (bỏ symref HEAD); đây là kiểm chéo snapshot, không chứng nhận trạng thái máy chủ hiện tại hay lịch sử ngoài snapshot.

### Hướng 4 — Sáu cổng baseline tại exact SHA (KHÔNG PHẢI LỖI)

Lệnh chuẩn bị: `git clone --no-hardlinks --no-checkout mirror.git /tmp/rv1050-r2-copy`; `git -C /tmp/rv1050-r2-copy checkout --detach f37b5195978f1fe35b9cb55b6f79a2e09d165af0`; `git -C /tmp/rv1050-r2-copy config core.abbrev 7`. Clone nằm ngoài `cay-kho/`. Các cổng chạy trong clone sạch, với `PYTHONDONTWRITEBYTECODE=1`, output bên ngoài clone.

Lệnh điều khiển: `python3 evidence/run_gates.py baseline`; từng lệnh và output đầy đủ ở `evidence/baseline-*.log`, mã thoát ở `.rc`/`baseline-gates.json`.

```text
python3 ops/bien_nhan_v2.py --root .
rc=0; bien_nhan_v2: 255 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 308
TỔNG: ĐẠT
python3 ops/land_evidence_nguon.py --root .
rc=0; land_evidence_nguon: 65 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 90
TỔNG: ĐẠT
python3 .claude/dev/packet_loop.py doctrine-scan --root .
rc=0; doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine
python3 ops/lease_publish_test.py --chi-ca=t26_
rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t27_
rc=0; lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0
python3 ops/lease_publish_test.py --chi-ca=t138_
rc=0; lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0
```

N/N bằng nhau, có marker dương. Không gặp lỗi `Codex home is inside a repository` trong sáu cổng này. `SyntaxWarning` ở `lease_publish_test.py:5205` không làm đổi rc hay N/N.

### Hướng 5 — Biên nhận v2, nội dung verdict và mỏ neo (KHÔNG PHẢI LỖI)

Lệnh: `python3 evidence/measure_receipts.py | tee evidence/receipts.log`. Từng khóa máy đọc được được đối chiếu lease/run/verdict/Git; đọc cả hai receipt để kiểm các khóa diễn giải.

Output thật (trích):
```text
ROUND 1 VERDICT Verdict: request_changes NORMALIZED_MATCH True COUNTS {'P0': 0, 'P1': 0, 'P2': 1, 'P3': 2} COUNTS_MATCH True
ROUND 2 VERDICT Verdict: approve NORMALIZED_MATCH True COUNTS {'P0': 0, 'P1': 0, 'P2': 0, 'P3': 0} COUNTS_MATCH True
ROUND 1 REVIEWED_SHA_MATCH True TREE 6907a286e95a2c6e86c7c08c0ec700dc2a75ef58 LEASE_BASE 757bde561d09738858506aecf5de2f050a5f0d5e
ROUND 2 REVIEWED_SHA_MATCH True TREE c20eace3f4aacea3f33afc5861688cb94d64cf3d LEASE_BASE 757bde561d09738858506aecf5de2f050a5f0d5e
ROUND 1 VERDICT_HASH_MATCH True BYTES_MATCH True RECEIPT_ID_HASH_SUFFIX True
ROUND 2 VERDICT_HASH_MATCH True BYTES_MATCH True RECEIPT_ID_HASH_SUFFIX True
ROUND 1 ANCESTRY e788a5d0d518f8a08ac13473a85197287fad4fcb f37b5195978f1fe35b9cb55b6f79a2e09d165af0 rc 0
ROUND 2 ANCESTRY e788a5d0d518f8a08ac13473a85197287fad4fcb f37b5195978f1fe35b9cb55b6f79a2e09d165af0 rc 0
MERGE_HEAD_PARENT 91466322f705658ed51b80c7c152f6b77f4f90c6
WRITE_SET_HASH d7872905e38bb8e57304520785c71c0562f88d84f60946af2cfb41e4f2cd792a EXPECTED d7872905e38bb8e57304520785c71c0562f88d84f60946af2cfb41e4f2cd792a
BOOKKEEPING_HEAD_IN_MASTER_RC 1
```

Cả hai receipt: schema 2, kind, packet ID/#1037, target PR #1041, revision 1/generation 1/lease ID, provider, vai, class sensitive, đường dẫn verdict và hậu tố receipt ID đều khớp. Các `FIELD` và `LEASE_FIELD` trong log đều `MATCH True`. Hai URL blob ghim **đủ 40 ký tự** `e788a5d0d518f8a08ac13473a85197287fad4fcb`; blob bằng byte verdict, commit là tổ tiên exact head ghi sổ. Cường độ `thap` đúng với trạng thái PR ghi sổ chưa nằm trong master snapshot. Hai reviewed SHA đều là tổ tiên merge `b29da0b` (rc 0); base lease là tổ tiên cả hai (rc 0).

`reviewed_tree`, `base_sha`, `muc_bang_chung_model` không có như khóa trực tiếp trong receipt. Đây không phải trường bắt buộc của delivery receipt v2 (§7); tree/base đã đối chiếu từ Git và lease, mức model nằm ở khóa `model_reviewer_identity.model_evidence: do_may`. Không nhầm base packet `757bde5` với base PR ghi sổ `b29da0b`.

Ba slug/hạng lượt 1 khớp ba dòng finding gốc. Lượt 2 có bảng đối chiếu cả ba và không có finding mới; các mutant sống được ghi rõ là giới hạn c98, không bị biến thành finding mở hay xóa khỏi bản sao. Việc ghi sổ không phải một lần tái thực thi mutant mã của packet #1037.

### Hướng 6 — Model, runtime, assurance và caveat (KHÔNG PHẢI LỖI; có giới hạn KHÔNG ĐO ĐƯỢC)

Lệnh: `python3 evidence/measure_receipts.py | tee evidence/receipts.log`; đọc hai `run/run.json` và hai receipt. Output thật:
```text
ROUND 1 IDENTITY provider openai_codex RUN_MATCH True
ROUND 1 IDENTITY surface codex_cli RUN_MATCH True
ROUND 1 IDENTITY transport machine RUN_MATCH True
ROUND 1 IDENTITY session_run_id 4d0668e2f3d045ef86354bea2a6afd29 RUN_MATCH True
ROUND 2 IDENTITY provider openai_codex RUN_MATCH True
ROUND 2 IDENTITY surface codex_cli RUN_MATCH True
ROUND 2 IDENTITY transport machine RUN_MATCH True
ROUND 2 IDENTITY session_run_id e400a3206474480f827b771e59395389 RUN_MATCH True
ROUND 1 MEASURED_MODELS DO_DUOC 27 {'gpt-6-astra': 27} EFFORT DO_DUOC ['xhigh']
ROUND 2 MEASURED_MODELS DO_DUOC 19 {'gpt-6-astra': 19} EFFORT DO_DUOC ['xhigh']
ROUND 1 PROMPT_HASH_MATCH True
ROUND 2 PROMPT_HASH_MATCH True
ROUND 1 START_IN_LEASE True
ROUND 2 START_IN_LEASE True
ROUND 1 ASSURANCE cross_reviewed EXECUTOR_MODEL claude-opus-5-5 claude
ROUND 2 ASSURANCE cross_approved EXECUTOR_MODEL claude-opus-5-5 claude
```

Hai run terminal `xong`, rc 0; thời lượng 934.249 / 567.318 giây; sạch lúc phóng; head/prompt khớp; run ID và prompt riêng. `model`, `model_da_chay`, mức `do_may` và đường dẫn `#model_phuc_vu` khớp model thực phục vụ được lưu. Lượt 1 chỉ `cross_reviewed` vì request_changes; lượt 2 approve 0/0/0/0 trên đúng head merge, model reviewer họ OpenAI khác họ Claude theo lease, đủ ghi `cross_approved` trong phạm vi evidence §8, không thành quyền merge.

Lượt 1 `sandbox_trang_thai=KHONG_DO_DUOC`; lượt 2 `DO_DUOC`. Nguồn lượt 2 có `codex-linux-sandbox`, permission profile restricted, `root read`, `to_tien_workspace write`, network restricted, và giới hạn lấy mẫu /proc 0.2 s. Hồ sơ chỉ nhận thực thi §8.1 ở lượt 2. Caveat workspace có quyền ghi và scripts `evidence/*` không được giữ trong kho được nâng đủ lên README; không suy snapshot sạch thành chưa từng ghi.

**KHÔNG ĐO ĐƯỢC độc lập** CLI version `0.164.0`, raw cờ CLI và `model_yeu_cau`: run chỉ giữ `chuong_trinh`, `so_doi_so=11`, `van_tay`; `CLI_VERSION_FIELDS []`. Served model không chứng minh requested model/phiên bản CLI. Không có bằng chứng trái ngược các lời khai cấu hình đó; không biến hạn chế tái lập thành cáo buộc sai sự thật. Executor model theo lease, danh tính người thật dùng credential, phiên executor thực tế, và submitter PR ghi sổ chỉ có lời khai; `actor_nguon` tự gắn `(b)`, chưa có readback bản chiếu. Tách chúng khỏi served-model evidence của reviewer.

### Hướng 7 — Nhiệm vụ 0: Windows, metadata và nguồn CI (KHÔNG PHẢI LỖI)

Lệnh: `python3 evidence/measure_ci.py | tee evidence/ci.log`; `nl -ba cay-kho/ops/land/pr1041-wp1037-land-evidence.yaml`. Output thật:
```text
JOBS 41033737059 TOTAL 23 LENGTH 23 CONCLUSIONS {'success': 23} LABELS {('ubuntu-latest',): 23}
JOBS 41069257658-a1 TOTAL 16 LENGTH 16 CONCLUSIONS {'success': 13, 'failure': 2, 'skipped': 1} LABELS {('ubuntu-latest',): 1, ('windows-latest',): 14, (): 1}
JOBS 41069257658-a2 TOTAL 16 LENGTH 16 CONCLUSIONS {'success': 15, 'skipped': 1} LABELS {('windows-latest',): 14, ('ubuntu-latest',): 1, (): 1}
WINDOWS_OPS_JOB 124108765783 RUNNER 1000026073 ['windows-latest'] CONCLUSION success
FAILED_JOB 124108765805 gate-cong-cu (windows-latest, 0) RUNNER 1000026071 ['windows-latest'] FAILED_STEPS [(9, 'G5 manh ban kinh dot bien (#668)', 'failure')]
SHELLCHECK_STEPS 124108765805 [(7, 'cài shellcheck cho G5 (cài xong đo lại)', 'success')]
FAILED_JOB 124108766201 gate-packet-loop (windows-latest) RUNNER 1000026080 ['windows-latest'] FAILED_STEPS [(9, 'G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6', 'failure')]
SHELLCHECK_STEPS 124108766201 [(7, 'cài shellcheck cho G5 (cài xong đo lại)', 'success')]
SOURCE_TOKEN 'runner thieu shellcheck' FILES []
SOURCE_TOKEN 'cai_cong_cu.sh' FILES []
SOURCE_TOKEN '1045' FILES []
SOURCE_TOKEN 'runner_set' FILES []
SOURCE_TOKEN 'windows-only' FILES []
```

Ba run thuộc đúng repository, đúng head `91466322f705658ed51b80c7c152f6b77f4f90c6`; attempts 1/1/2; events pull_request/workflow_dispatch/workflow_dispatch; conclusion success/failure/success. Toàn bộ job run_id/head_sha/attempt khớp đúng run; counts bằng `total_count` nên không bỏ trang được khai. Mọi `nguon` của checks đều tồn tại.

**`nguyen-nhan-windows-khai-do-thieu-log`: ĐÓNG / ĐÃ VÁ THẬT.** Tại dòng 39, phần `measured` giữ đúng count, step failure và runner labels. Phần mới bắt đầu `Thuat_lai — executor khai input runner_set=windows-only va nguyen nhan ...; KHONG_DO_DUOC ... khong co log chan doan hoac readback inputs` tách hẳn điều chưa có nguồn. Tên check chỉ nhận nhãn Windows đọc từ jobs. N/N `95/95 · 137/137 · 2/2` và lease `255/255` vẫn ghi rõ thuật lại từ job, log không lưu trong kho, không được nhận là đo độc lập.

Tự săn thêm cách diễn giải attempt 2: lệnh Python đọc hai `readback-jobs-41069257658-a*.json`, ghép theo tên job, so `started_at`/`completed_at`; output lưu `evidence/rerun-comparison.log`:
```text
chuan-bi a1=success a2=success start_equal=True end_equal=True
gate-ops (windows-latest) a1=success a2=success start_equal=True end_equal=True
gate-cong-cu (windows-latest, 0) a1=failure a2=success start_equal=False end_equal=False a1_start=2026-10-30T14:08:52Z a2_start=2026-10-30T15:27:27Z
gate-packet-loop (windows-latest) a1=failure a2=success start_equal=False end_equal=False a1_start=2026-10-30T14:08:53Z a2_start=2026-10-30T15:27:28Z
gate-cong-cu-gop a1=skipped a2=skipped start_equal=False end_equal=False
```
Đủ 13 job vốn success giữ nguyên cả hai mốc runtime; hai job failure đổi sang success và có runtime mới; job gộp vẫn skipped, không có runner. Điều này hỗ trợ cách mô tả rerun các job lỗi. Endpoint/request kích hoạt không được giữ, nên không xác nhận độc lập API nào đã được gọi; không lấy ID job mới làm bằng chứng mọi job đã thực thi lại.

### Hướng 8 — Merge, snapshot pending và `landed:false` (KHÔNG PHẢI LỖI)

Lệnh: `python3 evidence/measure_ci.py | tee evidence/ci.log`; script đọc readbacks và chạy `git show`, `git diff` trên đúng OID. Output thật:
```text
PR {'number': 1041, 'state': 'closed', 'merged': True, 'merged_at': '2026-10-30T17:28:50Z', 'merge_commit_sha': 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93'} MERGED_BY ducthangho HEAD 91466322f705658ed51b80c7c152f6b77f4f90c6 BASE 757bde561d09738858506aecf5de2f050a5f0d5e
MERGE_GIT b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
24a37bebf90e5f8e2dd3d4a34e842f2e2f9c6a39
8cdb15a786304bab084b43c8b30c127ae87e2594 91466322f705658ed51b80c7c152f6b77f4f90c6
2026-10-31T00:28:50+07:00
MERGE_IDENTITY_MATCH True True
DIFF_EQUAL True SHA256 40b6d80f2c0140953cc8712362138de059503982cce0e736b9a196b892ad2198 NUMSTAT 120 4 ops/bien_nhan_v2_test.py
MASTER_RUN {'id': 41099184556, 'run_attempt': 1, 'name': 'gate', 'event': 'push', 'head_sha': 'b29da0bfe3bfb7a7be69136a1c5c40f82c088a93', 'status': 'pending', 'conclusion': None, 'created_at': '2026-10-30T17:28:53Z', 'updated_at': '2026-10-30T17:28:54Z'}
```

Mốc Git `2026-10-31 00:28:50+07:00` chính là `2026-10-30 17:28:50Z`. Merge method/two parents/tree và diff landing đều khớp readback. Chủ tài khoản merge được đo; người thật/phần mềm dùng credential đã được hồ sơ tách thành lời khai.

Comment `6529010520`: `ducthangho OWNER`, `2026-10-30T17:25:09Z`, nội dung nêu điều kiện và thứ tự merge; `CONTAINS_FULL_AUTHORIZED_HEAD False`. Hồ sơ không dùng hành động merge để nhận đã có một approval độc lập exact SHA trước land.

Các câu pending tại dòng 4–5, 43, 87 đều ghi **lúc ghi sổ**, phần nguồn có mốc **17:37Z** và header REST ~17:37Z. Vì vậy đây là snapshot nguồn, không khẳng định run còn pending tại 18:08:52Z hay lúc review. Không gọi mạng để suy trạng thái mới.

§10.2.2: chỉ mốc **Run** có API identity; không có checkout log/artifact, exact workflow-definition repository/path/OID/blob/hash của đúng run, hay command/rc/marker/artifact của gate output. Các giới hạn ấy được khai rõ, không được đánh `measured` xanh. REST head và Git merge tree không bị dùng thay checkout CI. GraphQL403 và connector comment `6529077259` không có raw readback nên chỉ thuật lại/KHÔNG ĐO ĐƯỢC. `landed:false` vẫn đúng vì chưa có đủ post-merge provenance và approval exact-SHA riêng, kể cả lease #1037 đã hết hạn ở phép đo mới.

### Hướng 9 — README, mục lục/caveat và trùng hàng (KHÔNG PHẢI LỖI)

Lệnh: `git -C cay-kho diff b29da0b HEAD -- ops/reviews/README.md`; `python3 evidence/measure_readme.py | tee evidence/readme.log`. Output thật:
```text
ROUND 1 TOC_COUNT 1
VERDICT_IN_ROW True ASSURANCE_IN_ROW True SHA_IN_ROW True BYTES_IN_ROW True
LINK wp1037-g1-codex-luot1-verdict.md EXISTS True
LINK wp1037-g1-codex-luot1-verdict.receipt.yaml EXISTS True
LINK wp1037-g1-codex-luot1/ EXISTS True
CAVEAT 1 CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY COUNT 1
CAVEAT 1 SCRIPT-DO-DOC-DUONG-DAN-SANDBOX COUNT 1
ROUND 2 TOC_COUNT 1
VERDICT_IN_ROW True ASSURANCE_IN_ROW True SHA_IN_ROW True BYTES_IN_ROW True
LINK wp1037-g1-codex-luot2-verdict.md EXISTS True
LINK wp1037-g1-codex-luot2-verdict.receipt.yaml EXISTS True
LINK wp1037-g1-codex-luot2/ EXISTS True
CAVEAT 2 CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY COUNT 1
CAVEAT 2 SCRIPT-DO-DOC-DUONG-DAN-SANDBOX COUNT 1
```

Đúng hai hàng mục lục và bốn hàng caveat mới, không trùng. Nội dung lease/gen/revision/spec, verdict/counts/assurance, run ID, reviewed SHA, byte count đều khớp receipt và nguồn; sáu link đích tồn tại. Hàng lượt 2 nói rõ `head da duyet = head PR #1041 luc merge`, không nhầm head `9146632` với merge OID `b29da0b`.

### Hướng 10 — Ba đột biến dữ liệu, chạy lại từng cổng (KHÔNG PHẢI LỖI của dữ liệu hiện tại; đo được chốt không có răng)

Lệnh: `python3 evidence/run_mutations.py > evidence/mutations.log 2>&1`; script chỉ đổi dữ liệu trên clone `/tmp/rv1050-r2-copy` tại f37b519, gọi đủ sáu lệnh sẵn của hướng 4 cho **từng** mutant rồi phục hồi byte gốc trong `finally`. Mọi lệnh/rc/output đầy đủ ở `evidence/mutant-*.log`, `.rc`, `*-gates.json`; bảng tổng hợp `evidence/mutations-summary.json`.

| Dữ liệu bị đổi | bien_nhan_v2 | land_evidence_nguon | doctrine-scan | t26 | t27 | t138 |
|---|---:|---:|---:|---:|---:|---:|
| Một byte đầu verdict phẳng lượt2: V→W, không đổi hash receipt | 0 | 0 | 0 | **1** | 0 | 0 |
| Xóa đúng một hàng mục lục mới của lượt2 trong README | 0 | 0 | 0 | 0 | **1** | 0 |
| Receipt lượt2: `so_p1: 0`→`so_p1: 1`, giữ approve và verdict nguyên byte | 0 | 0 | 0 | 0 | 0 | 0 |

Output thật:
```text
mutant-byte t26 rc=1
LỆCH BĂM — biên nhận khai 2f482565c235380145253d76ae51ab9606e8d7cfc8044d6efd113ff80049feaf, tệp 'ops/reviews/wp1037-g1-codex-luot2-verdict.md' thực acdabd02d27ec7dd2c44ea916bf03dc03d3b01549a6e465535fe69137bbf98ec.
lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0
mutant-readme t27 rc=1
README.md: verdict 'wp1037-g1-codex-luot2-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'.
lease_publish: 1/2 đạt; đã chạy=2, bỏ qua=0
MUTATION_RESULT mutant-count {'bien_nhan_v2': 0, 'land_evidence_nguon': 0, 'doctrine_scan': 0, 't26': 0, 't27': 0, 't138': 0}
RESTORED mutant-byte True
RESTORED mutant-readme True
RESTORED mutant-count True
FINAL_CLONE_STATUS (rỗng)
```

Tất cả cổng còn rc0 có marker baseline tương ứng: TỔNG ĐẠT, doctrine sạch, t26 1/1, t27 2/2, t138 1/1 (trừ đúng cổng đỏ nêu trên). Hash và mục lục có răng ở t26/t27; `bien_nhan_v2` không cưỡng chế hai tính chất ấy, t138 chỉ kiểm hợp đồng receipt thu hồi bằng fixture riêng. **Số đếm finding không có răng trong bất kỳ cổng nào của sáu cổng được yêu cầu**, kể cả approve với P1=1. Đây là giới hạn được đo, không phải finding mới về PR ghi sổ: PR không đổi mã cổng, số đếm hiện tại đã được đối chiếu thủ công chính xác ở hướng 5; lượt 1 cũng đã ghi giới hạn này.

### Hướng 11 — Thử scanner trực tiếp: KHÔNG ĐO ĐƯỢC do phụ thuộc mạng

Lệnh đã chạy trong `cay-kho/`: `PYTHONDONTWRITEBYTECODE=1 python3 ops/lease_publish.py ai-dang-giu ops/bien_nhan_v2_test.py`; output lưu ngoài cây tại `evidence/lease-current-offline.log`.

Output thật:
```text
PHẠM_VI: quét refs/heads/*; nhánh cục bộ tụt sau origin/<cùng tên> sẽ bị CHẶN
CHAN [12]: KHÔNG_XÁC_ĐỊNH: git ls-remote --heads origin rc=128: fatal: unable to access 'https://github.com/ducthangho/tra-luat.git/': Failed to connect to 127.0.0.1 port 33749 after 0 ms: Couldn't connect to server
rc=12
```

Sai sót thao tác của reviewer: gọi scanner mà chưa kiểm nó tự gọi `ls-remote`; đây là **một lần thử mạng trái ràng buộc**, bị môi trường chặn và không thu được dữ liệu từ máy chủ. Không lặp lại, không thay remote/cờ để tiếp tục gọi mạng, không dùng rc12 làm finding của PR hay làm bằng chứng nhả lease. Kết quả lease trong verdict dựa trên nguồn băm tại exact SHA và hàm phân loại có sẵn với mốc thời gian tường minh (hướng 3); không tự nhận đã tái chạy toàn bộ scanner thành công ở 18:07:34Z.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding trên c24875d | Trạng thái tại f37b519 | Bằng chứng tự đo |
|---|---|---|
| `nha-lease-truoc-khi-het-han` [P1] | **ĐÓNG — ĐÃ VÁ THẬT** | Hướng 3; `measure_lease.py` + `lease.log`: trước hạn CÒN_HẠN, sau hạn HẾT_HẠN; snapshot 17:37Z được giữ đúng quá khứ, khối 18:07:34Z có nguồn/hash riêng và không khai holder hiện hành. |
| `nguyen-nhan-windows-khai-do-thieu-log` [P2] | **ĐÓNG — ĐÃ VÁ THẬT** | Hướng 7; `measure_ci.py` + `ci.log`: count/steps/labels khớp; root cause và input không có nguồn được tách thành thuật lại/KHÔNG ĐO ĐƯỢC ngay tại check. |

Không phát hiện finding P0/P1/P2/P3 mới trong phạm vi ghi sổ đã đo. Không cần `HINT.patch`. Không tái dùng phán quyết lượt 1 làm bằng chứng pass; các log trong `evidence/` là phép đo của lượt này. Các giới hạn không có nguồn runtime/job log và chốt số đếm không có răng đã ghi rõ, không được biến thành pass độc lập.

## KIỂM CUỐI

Lệnh: `python3 evidence/final_integrity.py | tee evidence/final-integrity.log`. Output thật:
```text
cay-kho git rev-parse HEAD HEAD^{tree} rc 0 stdout f37b5195978f1fe35b9cb55b6f79a2e09d165af0
235444656cad85bd969f99907b1dbeb4007d961a
cay-kho git status --short --untracked-files=all --ignored=matching rc 0 stdout (empty) stderr (empty)
cay-kho git diff --exit-code rc 0 stdout (empty) stderr (empty)
cay-kho git diff --cached --exit-code rc 0 stdout (empty) stderr (empty)
cay-kho git diff --check rc 0 stdout (empty) stderr (empty)
cay-kho git config core.abbrev rc 0 stdout 7 stderr (empty)
cay-kho ALL_PR_PATHS_EQUAL_EXACT_HEAD 33 / 33
cay-kho SCOPE_ONLY_OPS_REVIEWS_LAND True
cay-kho NUMSTAT 33 files changed, 11665 insertions(+)
rv1050-r2-copy git rev-parse HEAD HEAD^{tree} rc 0 stdout f37b5195978f1fe35b9cb55b6f79a2e09d165af0
235444656cad85bd969f99907b1dbeb4007d961a
rv1050-r2-copy git status --short --untracked-files=all --ignored=matching rc 0 stdout (empty) stderr (empty)
rv1050-r2-copy git diff --exit-code rc 0 stdout (empty) stderr (empty)
rv1050-r2-copy git diff --cached --exit-code rc 0 stdout (empty) stderr (empty)
rv1050-r2-copy git diff --check rc 0 stdout (empty) stderr (empty)
rv1050-r2-copy git config core.abbrev rc 0 stdout 7 stderr (empty)
rv1050-r2-copy ALL_PR_PATHS_EQUAL_EXACT_HEAD 33 / 33
PROMPT_SHA256 PROMPT.md 6762 23a3a3f8be4b87f91bf897b1656add36826168e7dd9253f8ef516bdeba7fd7a5
PROMPT_SHA256 run/8c095c6b/prompt.snapshot 6762 23a3a3f8be4b87f91bf897b1656add36826168e7dd9253f8ef516bdeba7fd7a5
```

Cây gốc và clone cuối cùng đều sạch ở tracked/untracked/ignored, HEAD/tree không đổi; 33/33 tệp của PR bằng blob exact SHA. Các đột biến đã phục hồi, không sửa `cay-kho/`, không push. Kết quả **approve** chỉ chấm PR ghi sổ #1050 tại exact reviewed SHA nêu ở đầu, không cấp quyền merge/land và không nâng hồ sơ #1037 thành landed. Sai sót thử mạng bị chặn của chính reviewer được giữ nguyên trong hướng 11 để không khai sai phạm vi phép đo.
