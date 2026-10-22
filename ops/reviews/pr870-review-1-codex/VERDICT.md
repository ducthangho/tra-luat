verdict: changes_requested
reviewed_sha: b38fce83d0e97981012072ca2a2023ac726e5b2e
base_sha: 9e9a74b2a396ef458d25c51a5563efafbb45ba0c
reviewed_tree: 68e6c67e280e58f202658f551da150f783c2116a
reviewer: codex
provider: openai
execution_surface: Codex agent + local shell tools
transport: tool-mediated (local); không gọi mạng/GitHub

Kết quả: 0 P0, 0 P1, 1 P2, 0 P3. Hai cổng tài liệu passed; hạn chế đo được ghi riêng, không biến thiếu readback thành pass hoặc finding. `cay-kho/` giữ nguyên.

## BẢNG ĐO

| khẳng định | PR khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact SHA và phạm vi | head b38fce83…; base 9e9a74b…; CLAUDE.md +21/-9 | HƯỚNG 1: git rev-parse / merge-base / diff --numstat | Có |
| Output os, điều kiện Windows, push master | dispatch HOẶC PR nhãn windows; còn lại ubuntu | HƯỚNG 2: git show b38fce83:.github/workflows/ci.yml L50–53; diff với base rỗng | Có |
| Mốc đo 22-10-2026 trên 9e9a74b | ngày và snapshot | HƯỚNG 2: base/head timestamp 22-10; os cùng blob. Không có transcript gốc để chứng thực ngày đo của tác giả | Snapshot khớp; ngày đo gốc KHÔNG ĐO ĐƯỢC |
| Packet #548 / tên packet / bỏ vế master | CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND | HƯỚNG 3: git log -S + git show d1258fe xác định đúng hunk outputs.os; commit là tổ tiên head | Có |
| doctrine-scan | rc=0 | HƯỚNG 4: python3 .claude/dev/packet_loop.py doctrine-scan --root . | Có: rc=0, sạch 10 tệp |
| doc-claims-check | rc=0 và ok=true | HƯỚNG 4: python3 scripts/tl.py doc-claims-check --json | Có: rc=0, ok=true; flags=[]; 381 advisories |
| Run 39354156843 / đường dẫn JSON | ci.yml, push master, merge 3a3a3ca, 20-10-2026 | HƯỚNG 5: JSON jobs + companion readback-run; git show -s 3a3a3ca xác nhận full SHA/2 parents | Có (readback cục bộ) |
| Số và nhãn job | 23 job; 23 ubuntu-latest; 0 Windows | HƯỚNG 5: total_count=len(jobs)=unique IDs=23; Counter(labels); run_id/head_sha trên MỌI job | Có |
| Biên bản 3f6c694 | jobs: '23/23 success (gom windows)' | HƯỚNG 6: git show 3f6c694:ops/land/pr848-wp744-land-evidence.yaml | Có, đúng chuỗi |
| Codex connector P1 trên #859; r4323607674; sửa #865 | chuỗi truy vết GitHub | HƯỚNG 6: merge 637f780 và correction 4ae43f0 (ghi connector P1 #859); không có raw comment / PR #865 | Một phần; comment/PR #865 KHÔNG ĐO ĐƯỢC |
| Các workflow còn lại | ci-dot-bien-du / ops-* đều ubuntu-latest | HƯỚNG 7: phân tích MỌI tệp; in runs-on, matrix, job-level uses, trigger, step uses | Có: 1 ci-dot-bien-du + 4 ops-*; không reusable job |
| Launcher push master | paths .claude/dev/** hoặc .github/workflows/launcher-windows.yml; Windows + Ubuntu | HƯỚNG 8: on.push.branches/paths; matrix.os; job.if cho event push | Có |
| Launcher PR | chỉ chạy khi nhãn windows; có types labeled | HƯỚNG 8: còn paths=[.claude/dev/**]; if chỉ lọc job sau trigger | Đúng điều kiện cần; PR còn có paths=.claude/dev/** (không thêm finding) |
| Launcher chỉ đo lane launcher | KHÔNG phải gate | HƯỚNG 8: doctor, launcher_test.py, --dot-bien và probes Windows; không có bước chạy gate ci.yml | Có |
| Windows trên master chỉ đến từ launcher-windows | câu nhấn mạnh không giới hạn loại event | HƯỚNG 2, 7, 9: ci.yml dispatch trên ref master cũng chọn Windows; output không loại ref master | Không: thiếu phạm vi push tự động (P2) |
| Gate PR thường không tự đo Windows sau merge | không nhãn windows và không ai dispatch | HƯỚNG 7, 9: không cò ẩn gọi gate Windows; mọi consumer chung outputs.os | Có tại reviewed_sha, trong điều kiện đã nêu; không chứng minh mọi run tương lai |
| Muốn Windows gate: dispatch trên ref đó | đường chắc chắn chọn ma trận Windows | HƯỚNG 2, 9: on.workflow_dispatch có; output không phụ thuộc ref | Có ở mức chọn runner; chưa đo run thật trong sandbox |
| ci.yml không có labeled trigger | pull_request không types; mặc định opened/synchronize/reopened | HƯỚNG 10: parse YAML pull_request=""; git show 3736fc0; không đo trực tiếp event server | Có ở YAML; ngữ nghĩa mặc định chỉ đối chiếu dữ liệu cục bộ |
| Gắn nhãn cần event sau đó | synchronize/reopened hoặc bổ sung types labeled | HƯỚNG 2, 10: matrix đọc labels event; labeled không có trong on | Có, suy từ YAML; không tạo PR/run thật |
| Cross-review #109 P2 thứ hai | bẫy nhãn của workflow | HƯỚNG 10: 05170b4 rồi 3736fc0 và merge 9796f67; không có raw finding review | Dấu vết sửa khớp; mức P2/identity KHÔNG ĐO ĐƯỢC độc lập |
| PR head contains required EOL base | if github.event_name == pull_request; master skipped | HƯỚNG 10: parse step.if; push/dispatch master không thỏa | Có ở điều kiện; job không khởi động thì không có step readback để gọi skipped |
| 14-08-2026 ma trận còn master | khi ấy có vế master | HƯỚNG 11: log --until + git show a323974:.github/workflows/ci.yml L44–50 | Có |
| Đợt 14-08 sáu merge / không nhãn, không dispatch / lần Windows đầu | sáu lần đo đầu; nay cùng điều kiện không lần nào | HƯỚNG 11: 8 merge trước 19:00; chưa định danh “đợt” sáu lượt; thiếu run/labels/dispatch readback; hiện tại output os chỉ Ubuntu | Phạm vi sáu lượt, “đầu tiên” và không dispatch lịch sử KHÔNG ĐO ĐƯỢC |
| Tiêu đề matrix không phân biệt PR/master vs deploy §5 | chỉ sửa mô tả OS | HƯỚNG 12: LAND if ref master / WORKER if ref != master; OS dùng cùng output | Không mâu thuẫn: cùng chính sách chọn OS không đồng nghĩa cùng bộ bước |
| API CHỈ CÓ TRÊN MỘT NỀN (L800–811) | job Windows chỉ chạy khi PR nhãn windows | HƯỚNG 8, 12: launcher tự động PR cần nhãn + paths; dispatch và push là các event khác, bài học lịch sử | Không tạo phản ví dụ mới; không đọc câu cũ thành mô tả mọi event |
| Protocol T3 / ADR-0049 / “KHÔNG BAO GIỜ” | gate mã PR thường không Windows sau merge | HƯỚNG 12: protocol L884 có Windows+Linux, ADR L19 có gate deploy tại chỗ; không phải trigger của ci.yml | Chỉ đúng trong phạm vi CI tự động hiện tại; cần giữ phạm vi đó khi diễn đạt |
| Phản ví dụ Windows trên master | chỉ launcher-windows.yml | HƯỚNG 13: evaluator nguyên hàm của kho: event=workflow_dispatch, ref=refs/heads/master => [ubuntu-latest,windows-latest] | Không (P2 scope); chưa gọi GitHub |
| Quote cũ về master Ubuntu+Windows | bản cũ từng ghi ở đây | HƯỚNG 14: git show 9e9a74b:CLAUDE.md L158–163 | Có (trích ý của câu cũ) |
| Đọc nhãn từng job / EOL skipped thật | đọc labels thay vì event, master EOL skipped | HƯỚNG 5, 13, 14: 23 runner_id dương; labels thật; EOL step.conclusion=skipped; push và dispatch cùng ref khác OS | Có |
| Doctrine cũ gây lời khai gom windows | quan hệ nguyên nhân tác giả diễn giải | HƯỚNG 6/14 chứng minh lời cũ và biên bản sai cùng tồn tại; không có transcript lý do của executor ở 3f6c694 | Chỉ là suy luận của tác giả; KHÔNG ĐO ĐƯỢC quan hệ nhân quả |
| HINT.patch / read-only | patch -p0 từ gốc cay-kho; không sửa cây nguồn | HƯỚNG 15: patch trên bản sao ngoài kho; git diff HEAD/cached + status + ls-files | Có, hint dry-run rc=0; tracked/index/untracked/ignored sạch |

## BẢNG SĂN

15 hướng đã hoàn tất; mỗi hướng dưới đây giữ lệnh chạy từ `cay-kho/`, output thật và rc. Môi trường subprocess đặt `PYTHONDONTWRITEBYTECODE=1`, `GIT_OPTIONAL_LOCKS=0`; không cài dependency, không gọi mạng. PyYAML 6.0.3 có sẵn. Nội dung báo cáo được ghi tăng dần trong khi đo.

### HƯỚNG 1: Neo đúng cây và phạm vi diff
  giả thuyết : Cây đang review có thể sai SHA/base hoặc có thay đổi ngoài CLAUDE.md.

  lệnh (cwd=cay-kho/) :
```bash
git rev-parse HEAD HEAD^{tree}; git rev-parse --is-shallow-repository; git config core.abbrev; git status --porcelain=v1; git merge-base 9e9a74b2a396ef458d25c51a5563efafbb45ba0c HEAD; git diff --numstat 9e9a74b2a396ef458d25c51a5563efafbb45ba0c HEAD
```
  output thật (rc=0) :
```text
b38fce83d0e97981012072ca2a2023ac726e5b2e
68e6c67e280e58f202658f551da150f783c2116a
false
7
9e9a74b2a396ef458d25c51a5563efafbb45ba0c
21	9	CLAUDE.md

```

  kết luận : KHÔNG PHẢI LỖI — đúng exact head/base, cây sạch, đủ lịch sử; chỉ CLAUDE.md +21/-9.

### HƯỚNG 2: Ma trận os tại exact SHA và base
  giả thuyết : Điều kiện Windows hoặc mô tả push master sai so với output của chuan-bi.

  lệnh (cwd=cay-kho/) :
```bash
git show b38fce83d0e97981012072ca2a2023ac726e5b2e:.github/workflows/ci.yml | sed -n '10,19p;34,54p;87,94p'; git diff 9e9a74b2a396ef458d25c51a5563efafbb45ba0c b38fce83d0e97981012072ca2a2023ac726e5b2e -- .github/workflows/ci.yml; git show -s --format='%H %cI %s' 9e9a74b b38fce83
```
  output thật (rc=0) :
```text
on:
  push:
    branches: [master]
  pull_request:
  # r226 — CHỖ HỞ ĐÃ TRẢ GIÁ 9 RUN: hai cò trên chỉ bắn ở master và ở PR, nên nhánh làm việc KHÔNG bao
  # giờ được gate soi. Đợt r225 nối 3 guard vào CI mà nhánh không chạy được ⇒ tưởng đã đóng nhưng chưa
  # từng chạy lần nào. `workflow_dispatch` cho phép soi gate theo yêu cầu trên BẤT KỲ ref nào, không
  # phải mở PR mới biết. (GitHub đòi workflow có mặt ở nhánh mặc định thì nút này mới dùng được ⇒ chỉ
  # hiệu lực SAU khi bản này lên master.)
  workflow_dispatch:
jobs:
  chuan-bi:
    # packet #548 (CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND): nguon duy nhat cho ma tran os.
    # Chi ubuntu-latest, khong checkout ma nguon; bo github.ref == 'refs/heads/master'.
    #
    # packet #674 (CI-DUONG-NHANH-HO-SO r2): nguon duy nhat cho `che_do`. PR chi doi ho so
    # (ops/{land,leases,reviews,specs}/**) => `duong_nhanh`: ba job bat buoc VAN KHOI DONG va bao ket qua,
    # chi cac buoc nang bi `if:` muc buoc bo qua. KHONG dung `paths:` / `paths-ignore:` — workflow khong chay
    # thi required check VANG MAT va PR ket `blocked`. Logic phan loai o `ops/ci_duong_nhanh.py` (co phan
    # chung), khong o bieu thuc YAML. Chi `pull_request` duoc phan loai; push va workflow_dispatch LUON day du.
    # Fail-close: chi dung chuoi `duong_nhanh` moi bo buoc; rong/la/vang => day du (phia job: `!= 'duong_nhanh'`).
    runs-on: ubuntu-latest
    # Tran ngoai: het gio CAP JOB thi `chuan-bi` DO (ba context bat buoc khong duoc tao => PR bi chan, khong mo) — chi
    # ngan thoi gian chan tu 360 phut mac dinh xuong day. Tran trong o hai buoc phan loai ben duoi (het gio => roi day_du).
    timeout-minutes: 20
    outputs:
      os: ${{ (github.event_name == 'workflow_dispatch'
               || contains(github.event.pull_request.labels.*.name, 'windows'))
              && '["ubuntu-latest","windows-latest"]'
              || '["ubuntu-latest"]' }}
      che_do: ${{ github.event_name == 'pull_request' && steps.phan-loai.outputs.che_do || 'day_du' }}
  gate:
    needs: chuan-bi
    strategy:
      fail-fast: false
      matrix:
        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
    runs-on: ${{ matrix.os }}
    # r391 — NÂNG 25 -> 45 THEO CHỈ ĐẠO CHỦ KHO, và lý do phải ghi lại vì con số cũ
9e9a74b2a396ef458d25c51a5563efafbb45ba0c 2026-10-22T13:38:57+07:00 Merge pull request #864 from ducthangho/agent/wp858-g1-claude
b38fce83d0e97981012072ca2a2023ac726e5b2e 2026-10-22T07:14:02+00:00 docs(CLAUDE.md): sua bai hoc (c) — ma tran os cua ci.yml khong con ve master

```

  kết luận : KHÔNG PHẢI LỖI — output os đúng: dispatch hoặc labels chứa windows mới có hai nền; push master chỉ Ubuntu. Workflow không đổi từ 9e9a74b đến reviewed_sha. Ngày 22-10 là ngày tác giả khai phép đo; timestamp commit cùng ngày, không chứng minh đã chạy lệnh ngày ấy.

### HƯỚNG 3: Pickaxe: commit thật bỏ vế master của ma trận
  giả thuyết : Packet #548 chỉ bỏ vế master ở một if khác, hoặc commit được gán sai.

  lệnh (cwd=cay-kho/) :
```bash
git log --all --format='%h %cI %s' -S"github.ref == 'refs/heads/master'" -- .github/workflows/ci.yml; git show --format=fuller d1258fe -- .github/workflows/ci.yml; git log --all --format='%h %s' --grep='#548' --grep='CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND'; git merge-base --is-ancestor d1258fe b38fce83; git rev-parse d1258fe
```
  output thật (rc=0) :
```text
d1258fe 2026-09-17T03:12:08+07:00 feat(#548): ma tran CI Windows xuat tu chuan-bi va doi tieu chuan gate (ADR-0049)
cb29eb5 2026-09-07T20:51:51+00:00 ci(#463 GATE): tách `test registry` và `packet-loop selftest` khỏi `gate` sang `gate-registry` / `gate-packet-loop`; `loi_ruff_ci` tìm bước theo MỌI job
2b82a9b 2026-08-31T10:53:54+07:00 ci: tach lane land/worker cho release-verify --strict (packet #427, N9)
a323974 2026-08-13T08:56:12+00:00 CI: cắt ~73% phút Actions — gate đang chết vì cạn hạn mức, không phải vì lỗi
commit d1258fef203d6b1f87fa729775cd2d8a1b0cc552
Author:     ducthangho <ducthangho@gmail.com>
AuthorDate: Thu Sep 17 03:12:08 2026 +0700
Commit:     ducthangho <ducthangho@gmail.com>
CommitDate: Thu Sep 17 03:12:08 2026 +0700

    feat(#548): ma tran CI Windows xuat tu chuan-bi va doi tieu chuan gate (ADR-0049)
    
    - ci.yml: them job chuan-bi (ubuntu, khong checkout ma nguon) xuat outputs.os; bo github.ref == 'refs/heads/master'. Ba job gate, gate-registry, gate-packet-loop chuyen sang doc needs.chuan-bi.outputs.os.
    - ops/lease_publish_test.py: them t161 (chot nguon duy nhat ma tran) va t162 (evaluator toi gian fail-close kem bang 4 ca va dot bien).
    - docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md: ADR-0049 doi tieu chuan gate ve cong tai cho cua deploy-package.*, ghi nhan mat mat va rui ro da nhan, khai trung thuc launcher-windows.yml van chay khi diff cham .claude/dev/**.
    - docs/PROTOCOL_DA_PHIEN.md: them dung 1 dong vao bang dinh tuyen §20 cho ADR-0049.
    
    Refs #548.

diff --git a/.github/workflows/ci.yml b/.github/workflows/ci.yml
index cb025a5..cbdad03 100644
--- a/.github/workflows/ci.yml
+++ b/.github/workflows/ci.yml
@@ -32,20 +32,25 @@ concurrency:
   cancel-in-progress: ${{ github.ref != 'refs/heads/master' }}
 
 jobs:
+  chuan-bi:
+    # packet #548 (CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND): nguon duy nhat cho ma tran os.
+    # Chi ubuntu-latest, khong checkout ma nguon; bo github.ref == 'refs/heads/master'.
+    runs-on: ubuntu-latest
+    outputs:
+      os: ${{ fromJSON(
+            (github.event_name == 'workflow_dispatch'
+             || contains(github.event.pull_request.labels.*.name, 'windows'))
+            && '["ubuntu-latest","windows-latest"]'
+            || '["ubuntu-latest"]') }}
+    steps:
+      - run: 'true'
+
   gate:
+    needs: chuan-bi
     strategy:
       fail-fast: false
       matrix:
-        # Windows tốn GẤP ĐÔI phút. Chạy nó ở nơi thật sự cần: trước khi vào master,
-        # khi gọi tay, hoặc khi PR được gắn nhãn `windows` (dùng cho PR đụng đường
-        # phụ thuộc nền). PR thường vẫn được Linux soi mỗi lần đẩy.
-        # KHÔNG phải nới gate: master vẫn luôn qua CẢ HAI nền trước khi phát hành.
-        os: ${{ fromJSON(
-              (github.event_name == 'workflow_dispatch'
-               || github.ref == 'refs/heads/master'
-               || contains(github.event.pull_request.labels.*.name, 'windows'))
-              && '["ubuntu-latest","windows-latest"]'
-              || '["ubuntu-latest"]') }}
+        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
     runs-on: ${{ matrix.os }}
     # r391 — NÂNG 25 -> 45 THEO CHỈ ĐẠO CHỦ KHO, và lý do phải ghi lại vì con số cũ
     # KHÔNG sai lúc nó được đặt: gate đã chậm dần tới sát trần. Đo 29-08-2026:
@@ -595,16 +600,11 @@ jobs:
     # ma trận/`timeout-minutes`/tiền tố 9 bước với `gate`, KHÔNG thêm mặt điều kiện nào; phút TÍNH
     # TIỀN tăng vì trả tiền thiết lập ba lần. Consumer `loi_ruff_ci` đọc MỌI job, không chỉ `gate`.
     # Bước `test registry` (41,0 % tổng bước Windows) sống ở đây.
+    needs: chuan-bi
     strategy:
       fail-fast: false
       matrix:
-        # Vì sao Windows có điều kiện: xem chú thích cùng chỗ ở job `gate` (bản gốc).
-        os: ${{ fromJSON(
-              (github.event_name == 'workflow_dispatch'
-               || github.ref == 'refs/heads/master'
-               || contains(github.event.pull_request.labels.*.name, 'windows'))
-              && '["ubuntu-latest","windows-latest"]'
-              || '["ubuntu-latest"]') }}
+        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
     runs-on: ${{ matrix.os }}
     timeout-minutes: 60
     env:
@@ -659,16 +659,11 @@ jobs:
     # ma trận/`timeout-minutes`/tiền tố 9 bước với `gate`, KHÔNG thêm mặt điều kiện nào; phút TÍNH
     # TIỀN tăng vì trả tiền thiết lập ba lần. Consumer `loi_ruff_ci` đọc MỌI job, không chỉ `gate`.
     # Bước `packet-loop selftest` (22,5 % tổng bước Windows) sống ở đây.
+    needs: chuan-bi
     strategy:
       fail-fast: false
       matrix:
-        # Vì sao Windows có điều kiện: xem chú thích cùng chỗ ở job `gate` (bản gốc).
-        os: ${{ fromJSON(
-              (github.event_name == 'workflow_dispatch'
-               || github.ref == 'refs/heads/master'
-               || contains(github.event.pull_request.labels.*.name, 'windows'))
-              && '["ubuntu-latest","windows-latest"]'
-              || '["ubuntu-latest"]') }}
+        os: ${{ fromJson(needs.chuan-bi.outputs.os) }}
     runs-on: ${{ matrix.os }}
     timeout-minutes: 60
     env:
b38fce8 docs(CLAUDE.md): sua bai hoc (c) — ma tran os cua ci.yml khong con ve master
f4539f3 ops(#578): CAP lease r1/g1 — khai CHONG LAN va CHAN viec bat dau
bc183c0 review 541: SUA bo do — kich thuoc phai do so MERGE-BASE, khong so base ghim trong spec
4826388 ops(#562): CAP lease t125-do-r1-g1-antigravity theo chi thi chu kho
d204300 spec(#541): r3 — revision 2 / generation 2, gop 4 phat hien luot 4 + t136
f4749c4 review 541: bien nhan phep do tren Windows THAT — N1-N4 dat, N7 giet dung ly do
eb15657 Merge pull request #553 — bookkeeping(#548): verdict lượt 5 + biên nhận giao hàng/LAND
fddf5a5 lease(#551): cap gen 2 cho revision 2 — write set 4 -> 6, ngoai le §5 mo rong
0cd1b94 specs(#551): dong bang ASSURANCE-NEO-VAO-HO-MODEL revision 2 — write set 4 -> 6
2f86f77 lease(#541): khai NGOAI LE §5 — go DIEU_KIEN_BAT_DAU, ghi nhan nhanh that
34ebd10 review(#541): verdict luot 1 — changes_requested, neo 2170a4a4ce93
ed1102d ops(#541): chi thi thi cong cho executor antigravity, luot 1
f07982d bookkeeping(#548): nang verdict luot 5 len Muc luc cua ops/reviews/README.md
a7dcf94 merge master vao nhanh bookkeeping #548 — de S la to tien cua H (cong thu-hoi doi)
0abfbbe lease(#551): cap gen 1 cho ASSURANCE-NEO-VAO-HO-MODEL r1 (ghi ho, ngoai le §5)
e32c564 bookkeeping(#548): bien nhan giao hang luot 5 + ho so LAND (§7, §13.1)
b11dbdf ops(#541): cap lease cho agy theo chi thi chu kho — CHONG LAN DA KHAI
d705623 Merge pull request #550 — packet #548 CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND r2/g2
c2f6898 review(#548): verdict luot 5 (r2/g2) — approve, neo dff2ec14ed5b
4eae721 spec(#552): r1 — packet DO t150 tren Windows, khong phai packet VA
dff2ec1 fix(#548): thi cong M8-M9 (r2/g2) — ke khai slot r291 va tai sinh manifest
d90cd87 lease: SOAN gen 2 cho #548 (r2, write set 6 duong) — CHUA DAY, cho chu kho duyet
2ee0e21 fix(#548): dong P3-MOI — bat chieu mang va truyen doi tuong vao outputs
315fa5f specs: dong bang CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND revision 2 (thay r1)
a45c8dc review(#548): verdict luot 4 — blocked, khiem khuyet nam o DAC TA khong o ban va
6d46e6f fix(#548): xu ly P1 — go fromJSON o chuan-bi.outputs va them chot chan output sequence
4bc35d3 review(#548): verdict luot 3 — RUT approve cua luot 2, mot P1
7e2ef2e review(#548): verdict luot 2 — approve, ca ba finding dong co phep do
93abdf2 fix(#548): bo sung so do WP541 va phan tich do phu windows vao ADR-0049
053bc43 fix(#548): xu ly review luot 1 — ghi nhan no WP541 trong ADR-0049 va loai bo tautology trong test
2d8b4fb review(#548): verdict luot 1 — changes_requested, 2 P2 + 1 P3
b017e47 spec(ASSURANCE-NEO-VAO-HO-MODEL): dong bang revision 1
d1258fe feat(#548): ma tran CI Windows xuat tu chuan-bi va doi tieu chuan gate (ADR-0049)
6388d08 lease(#548): cap generation 1 cho CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND (ghi ho)
d784335 thu-hoi(#538): ban sao THU BA cua r3-g3 cung phai mang dau bia mo
abbac31 thu-hoi(#538): bia mo cho r4-g4 — packet da land, quyen ghi phai tat
7acf740 thu-hoi(#538): chep dau bia mo thieu vao ban sao r3-g3 tren nhanh nay
bee48bf thu-hoi(#538): lease bia mo wp538-thu-hoi-sau-land (write_set RONG)
642c802 spec(#548): dong bang dac ta r1 CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND
d1258fef203d6b1f87fa729775cd2d8a1b0cc552

```

  kết luận : KHÔNG PHẢI LỖI — d1258fe sửa đúng outputs.os của chuan-bi và loại nhánh master; không phải chỉ sửa lane LAND hay concurrency.

### HƯỚNG 4: Hai cổng tài liệu bắt buộc
  giả thuyết : Thay đổi làm doctrine-scan hoặc doc-claims-check thất bại.

  lệnh (cwd=cay-kho/) :
```bash
python3 .claude/dev/packet_loop.py doctrine-scan --root .
```
  output thật (rc=0) :
```text
doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine

```

  lệnh (cwd=cay-kho/) :
```bash
python3 scripts/tl.py doc-claims-check --json
```
  output thật (rc=0) :
```text
{
  "ok": true,
  "schema": "doc_claims_check.v1",
  "roots": [
    "CHANGELOG.md",
    "SKILL.md",
    "CLAUDE.md",
    "CONTEXT.md",
    "references",
    "docs"
  ],
  "files_scanned": 113,
  "claims_flagged": 381,
  "flags": [],
  "advisories": [
    {
      "layer": "L1",
      "file": "CHANGELOG.md",
[... 381 advisories; xem stdout nguyên văn ở doc-claims-check.json ...]
      "line": 4747,
      "claim": "references/Code.2.21.1.gs",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    },
    {
      "layer": "L1",
      "file": "references/changelog_archive/CHANGELOG-den-1.33.53.md",
      "line": 4747,
      "claim": "references/PATCH_REPORT.sample.md",
      "reason": "PATH_MISSING_IN_HISTORICAL_DOC"
    }
  ],
  "by_layer": {
    "L1": 0,
    "L2": 0,
    "L3": 0,
    "L4": 0,
    "L5": 0,
    "L6": 0,
    "L7": 0,
    "L8": 0,
    "L9": 0,
    "L12": 0
  },
  "advisory_count": 381,
  "layers": [
    "L1",
    "L2",
    "L3",
    "L4",
    "L5",
    "L6",
    "L7",
    "L8",
    "L9",
    "L12"
  ],
  "layers_skipped": {},
  "basis": {
    "version": "1.36.68",
    "sha_lens": [
      7,
      40
    ],
    "changelog_files": 3,
    "changelog_versions": 490,
    "changelog_rs": 351,
    "changelog_headings": 1066,
    "floor_version": "1.9.9",
    "floor_r": 10,
    "max_r": 375,
    "commands_source": "references/golden/parser_surface.json",
    "commands_known": 198,
    "test_ids_known": 1379,
    "test_id_kinds": {
      "legacy": 1309,
      "packet": 70
    },
    "layers_bac": {
      "L10": "24/30 version GAS được dẫn không có tệp .gs — kho giữ 6 bản gần nhất là có chủ đích",
      "L11": "2/2 hit ở tài liệu sống đều viết ĐÚNG (số hiệu chính thức là dạng bare); bất biến NN-YYYY-VBHN-XXX áp cho khoá registry, đã có cổng vbhn-year-fix"
    },
    "note": "tập tra cứu = CHANGELOG.md + references/changelog_archive/*.md, quét toàn văn; dưới sàn ⇒ advisory (khuyết của sổ, không phải trích dẫn sai)"
  },
  "strict": false
}
```

  kết luận : KHÔNG PHẢI LỖI — cả hai rc=0; doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine; doc-claims-check: ok=true, flags=[], 113 files, 381 advisories, layers_skipped={}. Stdout JSON nguyên văn: `doc-claims-check.json`, SHA256=a0e9af9a837c88c6e1a444b1f9d51e3bc9a60475fd3121a1385bde1bd4777f65. Các advisory không làm gate thất bại; các cổng tĩnh này không chứng thực lịch sử run/comment hoặc mọi mệnh đề ngôn ngữ tự nhiên.

### HƯỚNG 5: Readback run 39354156843 và 23 nhãn runner
  giả thuyết : Đếm theo tên job có thể sai, run/SHA/ngày/trigger hoặc JSON readback bị lệch.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
import json, hashlib, subprocess
from collections import Counter
from pathlib import Path
p = Path('ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json')
d=json.loads(p.read_text()); jobs=d['jobs']
print('path=', p, 'sha256=', hashlib.sha256(p.read_bytes()).hexdigest())
print('total_count=', d['total_count'], 'len(jobs)=', len(jobs), 'unique job ids=',len({j['id'] for j in jobs}))
for key in ['labels','run_id','head_sha','head_branch','workflow_name','conclusion','run_attempt']:
 print(key, dict(Counter(str(j.get(key)) for j in jobs)))
for key in ['created_at','started_at','completed_at']:
 print(key, 'min=',min(j[key] for j in jobs), 'max=',max(j[key] for j in jobs))
print('windows labels=',sum(any('windows' in label.lower() for label in j['labels']) for j in jobs))
print('job names=',[j['name'] for j in jobs])
r=json.loads(p.with_name('readback-run-39354156843.json').read_text())
for key in ['id','name','path','event','head_branch','head_sha','created_at','run_started_at','updated_at','conclusion']:
 print('run.'+key, '=',r.get(key))
print('git 3a3a3ca=', subprocess.check_output(['git','show','-s','--format=%H %P %cI %s','3a3a3ca'],text=True).strip())
PROBE
```
  output thật (rc=0) :
```text
path= ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json sha256= 6124ae7e587a4a1aaba31aeeab94624dbdc725cd75b7ceb93648bf95ead4fbea
total_count= 23 len(jobs)= 23 unique job ids= 23
labels {"['ubuntu-latest']": 23}
run_id {'39354156843': 23}
head_sha {'3a3a3caca5de4934ff53851feb6994c2c7b84ad5': 23}
head_branch {'master': 23}
workflow_name {'gate': 23}
conclusion {'success': 23}
run_attempt {'1': 23}
created_at min= 2026-10-20T01:34:10Z max= 2026-10-20T02:05:10Z
started_at min= 2026-10-20T01:34:12Z max= 2026-10-20T02:05:12Z
completed_at min= 2026-10-20T01:34:16Z max= 2026-10-20T02:05:31Z
windows labels= 0
job names= ['chuan-bi', 'gate-packet-loop (ubuntu-latest)', 'gate (ubuntu-latest)', 'gate-ops (ubuntu-latest)', 'gate-cong-cu (ubuntu-latest, 5)', 'gate-cong-cu (ubuntu-latest, 3)', 'gate-nhanh-manh (ubuntu-latest, 1)', 'gate-cong-cu (ubuntu-latest, 7)', 'gate-nhanh-manh (ubuntu-latest, 4)', 'gate-nhanh-manh (ubuntu-latest, 5)', 'gate-nhanh-manh (ubuntu-latest, 3)', 'gate-nhanh-manh (ubuntu-latest, 7)', 'gate-nhanh-manh (ubuntu-latest, 2)', 'gate-cong-cu (ubuntu-latest, 0)', 'gate-cong-cu (ubuntu-latest, 1)', 'gate-cong-cu (ubuntu-latest, 4)', 'gate-nhanh-manh (ubuntu-latest, 0)', 'gate-cong-cu (ubuntu-latest, 2)', 'gate-cong-cu (ubuntu-latest, 6)', 'gate-nhanh-manh (ubuntu-latest, 6)', 'gate-nhanh-gop (ubuntu-latest)', 'gate-registry (ubuntu-latest)', 'gate-cong-cu-gop (ubuntu-latest)']
run.id = 39354156843
run.name = gate
run.path = .github/workflows/ci.yml
run.event = push
run.head_branch = master
run.head_sha = 3a3a3caca5de4934ff53851feb6994c2c7b84ad5
run.created_at = 2026-10-20T01:34:09Z
run.run_started_at = 2026-10-20T01:34:09Z
run.updated_at = 2026-10-20T02:05:32Z
run.conclusion = success
git 3a3a3ca= 3a3a3caca5de4934ff53851feb6994c2c7b84ad5 94220547cd155c73392e95726e8daf353888b3aa 23bc189f28ea60f04ca1634b6fe66d02babf12ed 2026-10-20T08:34:06+07:00 Merge pull request #848 from ducthangho/agent/wp744-g3-claude

```

  kết luận : KHÔNG PHẢI LỖI — toàn bộ 23 job có labels=[ubuntu-latest], cùng run_id/head_sha/master, success; companion readback xác nhận ci.yml, push, ngày 20-10 UTC. Đây là đo nội dung readback đã lưu; không xác minh lại API trực tiếp trong sandbox không mạng.

### HƯỚNG 6: Chuỗi khai gom windows, PR #859/comment/PR #865
  giả thuyết : Không có khai sai ở 3f6c694, hoặc PR/comment sửa đã được đồng nhất với một commit không liên quan.

  lệnh (cwd=cay-kho/) :
```bash
git show 3f6c694:ops/land/pr848-wp744-land-evidence.yaml | nl -ba | sed -n '25,44p'
git show --format=fuller 4ae43f0 -- ops/land/pr848-wp744-land-evidence.yaml
git log --all --format='%h %s' --extended-regexp --grep='^Merge pull request #859([[:space:]]|$)' --grep='^Merge pull request #865([[:space:]]|$)' --grep='4323607674' --grep='#865([^0-9]|$)'
rg -l 'r4323607674|4323607674|#865([^0-9]|$)|#859([^0-9]|$)' ops docs .claude CLAUDE.md
git log --all --format='%h %s' -G '4323607674' -- ops
git merge-base --is-ancestor 4ae43f0 b38fce83; printf 'correction_is_ancestor_rc=%s\n' "$?"
git rev-parse 3f6c694 4ae43f0 637f780
```
  output thật (rc=0) :
```text
    25	approver: ducthangho
    26	authorization_url: https://github.com/ducthangho/tra-luat/pull/848
    27	land_operator: 'loi_khai_co_neo — chu kho tu bam merge, executor khong merge; REST chi neo tai khoan merged_by=ducthangho, KHONG_DO_DUOC nguoi bam hay phien dung credential'
    28	merge_method: merge
    29	merge_commit: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5
    30	merge_commit_tree: d49c674d3c3fb81d7c389b44e5ae4085d3d229be
    31	merge_commit_parents: [94220547cd155c73392e95726e8daf353888b3aa, 23bc189f28ea60f04ca1634b6fe66d02babf12ed]
    32	pre_merge_checks:
    33	  - {name: 'ci.yml pull_request (14 job ubuntu) tren head cuoi', run_id: 39291888405, sha: 23bc189f28ea60f04ca1634b6fe66d02babf12ed, conclusion: success, kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-23bc189.txt: packet_loop.py kiem-gate suite 106474075749, 14 ten, rc=0', nguon: [readback-run-39291888405.json, readback-jobs-39291888405.json, readback-check-runs-23bc189-all.json]}
    34	  - {name: 'thu-hoi (pull_request_target) tren head cuoi, 2 luot (mo PR + roi draft)', run_id: [39291888633, 39320797755], sha: 23bc189f28ea60f04ca1634b6fe66d02babf12ed, conclusion: success, kiem_gate: 'measured — cung tep do-lai-nguon-20261020/kiem-gate-23bc189.txt: suite 106474076361 rc=0, suite 106555136375 rc=0', nguon: [readback-run-39291888633.json, readback-jobs-39291888633.json, readback-run-39320797755.json, readback-jobs-39320797755.json]}
    35	  - {name: 'executor cross-review Codex luot 1/3 (launcher.py run f65e544e, 600s, ma_thoat 0)', sha: 23bc189f28ea60f04ca1634b6fe66d02babf12ed, conclusion: 'approve, P0=0 P1=0 P2=0 P3=0', nguon: [verdicts/wp744-g3-luot1-codex-verdict.md, verdicts/run-f65e544e.json], ghi_chu: 'measured — do-lai-nguon-20261020/spec-va-verdict.txt: dong 1-2 verdict = approve + reviewed_sha 23bc189 (= authorized_head_sha); sha256 af2b5fa4… = ban da chieu o #848 issuecomment-6272837552.'}
    36	  - {name: 'Codex connector', sha: 23bc189f28ea60f04ca1634b6fe66d02babf12ed, conclusion: 'completed, has_any_findings=false', nguon: readback-comments-848.json, ghi_chu: 'measured — readback-comments-848.json comment 6276780956 (neo 23bc189, chay luc roi draft).'}
    37	  - {name: 'thread review', conclusion: '0 review, 0 review comment', nguon: [readback-reviews-848.json, readback-review-comments-848.json]}
    38	post_merge_checks:
    39	  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
    40	bookkeeping:
    41	  - {item: 'dong PR #747 la da thay the (khong merge)', ket_qua: 'measured — readback-pr-747.json: state closed, merged false; comment 6281281678 neu ly do wp728/#755 (readback-comment-6281281678.json)'}
    42	  - {item: 'rut han lease wp744-r3-g3-claude', ket_qua: 'xem lease.thu_hoi_cuoi'}
    43	  - {item: 'dong Issue #744 (completed) kem comment ban chieu', ket_qua: 'measured — readback-issue-744.json: state closed, state_reason completed, closed_at 2026-10-20T02:08:11Z, closed_by ducthangho (thao tac do phien executor goi bang tai khoan chu kho theo chi thi trong phien); comment 6281670864 (readback-comment-6281670864.json)'}
    44	  - {item: 'PR ghi so', nhanh: claude/bookkeeping-744-land}
commit 4ae43f0c1e0cf121246da64336763daa41beea57
Author:     Claude <noreply@anthropic.com>
AuthorDate: Wed Oct 21 09:07:34 2026 +0000
Commit:     Claude <noreply@anthropic.com>
CommitDate: Wed Oct 21 09:07:34 2026 +0000

    land(#744): dinh chinh gate post-merge 3a3a3ca — chi ubuntu, khong gom windows (connector P1 #859)
    
    Ca 23 job cua ci.yml 39354156843 deu nhan ubuntu-latest; ci.yml chi chon windows-latest cho workflow_dispatch
    hoac PR gan nhan windows. Ket luan gate (xanh, kiem-gate rc=0) khong doi.
    
    Co-Authored-By: Claude Opus 5.5 <noreply@anthropic.com>
    Claude-Session: https://claude.ai/code/session_01FBUBzbedsJaUtQvX4vEYDE

diff --git a/ops/land/pr848-wp744-land-evidence.yaml b/ops/land/pr848-wp744-land-evidence.yaml
index ce05a96..e9ef051 100644
--- a/ops/land/pr848-wp744-land-evidence.yaml
+++ b/ops/land/pr848-wp744-land-evidence.yaml
@@ -36,7 +36,7 @@ pre_merge_checks:
   - {name: 'Codex connector', sha: 23bc189f28ea60f04ca1634b6fe66d02babf12ed, conclusion: 'completed, has_any_findings=false', nguon: readback-comments-848.json, ghi_chu: 'measured — readback-comments-848.json comment 6276780956 (neo 23bc189, chay luc roi draft).'}
   - {name: 'thread review', conclusion: '0 review, 0 review comment', nguon: [readback-reviews-848.json, readback-review-comments-848.json]}
 post_merge_checks:
-  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success (gom windows)', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
+  - {name: 'ci.yml push master — DUNG merge SHA', run_id: 39354156843, sha: 3a3a3caca5de4934ff53851feb6994c2c7b84ad5, run_attempt: 1, conclusion: success, jobs: '23/23 success, ca 23 job chi nhan ubuntu-latest (measured — readback-jobs-39354156843.json); Windows KHONG chay tren lan push nay', luc: '2026-10-20T01:34:09Z -> 02:05:32Z', kiem_gate: 'measured — do-lai-nguon-20261020/kiem-gate-3a3a3ca.txt: packet_loop.py kiem-gate suite 106643757504, 23 ten, rc=0', nguon: [readback-run-39354156843.json, readback-jobs-39354156843.json, readback-check-runs-3a3a3ca-all.json]}
 bookkeeping:
   - {item: 'dong PR #747 la da thay the (khong merge)', ket_qua: 'measured — readback-pr-747.json: state closed, merged false; comment 6281281678 neu ly do wp728/#755 (readback-comment-6281281678.json)'}
   - {item: 'rut han lease wp744-r3-g3-claude', ket_qua: 'xem lease.thu_hoi_cuoi'}
@@ -108,5 +108,6 @@ no_ngoai_pham_vi:
 
 khong_do_duoc:
   - 'Log day du cac job CI KHONG luu; chi readback run/job/check-run.'
+  - 'launcher-windows/Windows KHONG chay cho push 3a3a3ca: ci.yml chi chon windows-latest cho workflow_dispatch hoac PR gan nhan windows; Windows khong phai dieu kien cua lease (M-3 chi doi ci.yml). Ban dau ho so ghi sai "gom windows" — connector P1 #859 r4323607674, dinh chinh o PR sau.'
   - 'Comment-id GitHub trich trong ba spec: reviewer Codex chay offline nen KHONG_DO_DUOC; phien executor da kiem ton tai 6091609833 6091612697 6091615222 6133771506 truoc khi push (khong luu tho).'
   - 'stderr/transcript luot review Codex KHONG luu ngoai run.json; model thuc chay KHONG_DO_DUOC tu run.json.'
b38fce8 docs(CLAUDE.md): sua bai hoc (c) — ma tran os cua ci.yml khong con ve master
637f780 Merge pull request #859 from ducthangho/claude/bookkeeping-744-land
CLAUDE.md
4ae43f0 land(#744): dinh chinh gate post-merge 3a3a3ca — chi ubuntu, khong gom windows (connector P1 #859)
correction_is_ancestor_rc=1
3f6c6943ebcebc7799db6adae76f8540c07f1d7f
4ae43f0c1e0cf121246da64336763daa41beea57
637f78029f5a5fe56d35199dd0f75c50274f2c0f

```

  kết luận : KHÔNG ĐO ĐƯỢC toàn bộ chuỗi GitHub: đo được nguyên văn jobs ở 3f6c694, merge PR #859 ở 637f780, commit đính chính 4ae43f0 ghi connector P1 #859. Không có raw comment r4323607674 hay đối tượng PR #865/merge #865 trong kho để xác nhận tác giả/mức P1/comment và liên kết #865. Không lấy lời mới ở CLAUDE.md tự chứng thực cho chính nó; thiếu dữ liệu không tự là finding.

### HƯỚNG 7: Quét toàn bộ workflow, runners, matrix và reusable uses
  giả thuyết : Một workflow còn lại chạy Windows ẩn qua biểu thức/matrix/reusable workflow.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
from pathlib import Path
import yaml
for p in sorted(Path('.github/workflows').rglob('*')):
 if not p.is_file(): continue
 print('\nFILE',p)
 d=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
 print('name=',d.get('name'),'on=',d.get('on'))
 for name,j in d.get('jobs',{}).items():
  print(' job=',name,'runs-on=',j.get('runs-on'),'uses=',j.get('uses'),'matrix=',j.get('strategy',{}).get('matrix'),'if=',j.get('if'))
 print(' step uses=',[s.get('uses') for j in d.get('jobs',{}).values() for s in j.get('steps',[]) if 'uses' in s])
PROBE
```
  output thật (rc=0) :
```text

FILE .github/workflows/ci-dot-bien-du.yml
name= đột biến đủ (hằng tuần) on= {'schedule': [{'cron': '17 19 * * 6'}], 'workflow_dispatch': ''}
 job= dot-bien-du runs-on= ubuntu-latest uses= None matrix= None if= None
 job= dot-bien-manh runs-on= ubuntu-latest uses= None matrix= {'manh': ['0', '1', '2', '3', '4', '5', '6', '7']} if= None
 job= dot-bien-gop runs-on= ubuntu-latest uses= None matrix= None if= None
 step uses= ['actions/checkout@v4', 'actions/setup-python@v5', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/upload-artifact@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/download-artifact@v4']

FILE .github/workflows/ci.yml
name= gate on= {'push': {'branches': ['master']}, 'pull_request': '', 'workflow_dispatch': ''}
 job= chuan-bi runs-on= ubuntu-latest uses= None matrix= None if= None
 job= gate runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'} if= None
 job= gate-cong-cu runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': ['0', '1', '2', '3', '4', '5', '6', '7']} if= None
 job= gate-cong-cu-gop runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'} if= ${{ !cancelled() }}
 job= gate-ops runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'} if= None
 job= gate-nhanh-manh runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}', 'manh': ['0', '1', '2', '3', '4', '5', '6', '7']} if= None
 job= gate-nhanh-gop runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'} if= ${{ !cancelled() }}
 job= gate-registry runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'} if= ${{ !cancelled() }}
 job= gate-packet-loop runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'} if= None
 step uses= ['actions/checkout@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/upload-artifact@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/upload-artifact@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/download-artifact@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/upload-artifact@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/download-artifact@v4', 'actions/checkout@v4', 'actions/setup-python@v5', 'actions/checkout@v4', 'actions/setup-python@v5']

FILE .github/workflows/launcher-windows.yml
name= launcher (Windows that) on= {'workflow_dispatch': {'inputs': {'runner_set': {'description': 'Nền cần đo trong lượt gọi tay', 'required': 'true', 'default': 'windows-only', 'type': 'choice', 'options': ['windows-only', 'windows-and-ubuntu']}}}, 'push': {'branches': ['master'], 'paths': ['.claude/dev/**', '.github/workflows/launcher-windows.yml']}, 'pull_request': {'types': ['opened', 'synchronize', 'reopened', 'labeled'], 'paths': ['.claude/dev/**']}}
 job= launcher runs-on= ${{ matrix.os }} uses= None matrix= {'os': '${{ fromJSON(github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\' && \'["windows-latest"]\' || \'["windows-latest","ubuntu-latest"]\') }}'} if= github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'windows')
 step uses= ['actions/checkout@v4', 'actions/setup-python@v5']

FILE .github/workflows/ops-don-ref.yml
name= ops — dọn ref (xoá nhánh · xoá tag · tạo tag) on= {'workflow_dispatch': {'inputs': {'hanh_dong': {'description': 'Làm gì', 'required': 'true', 'type': 'choice', 'options': ['xoa-nhanh', 'xoa-tag', 'tao-tag']}, 'ref': {'description': 'Tên ref, cách nhau bằng dấu phẩy. KHÔNG có tiền tố refs/heads hay refs/tags.', 'required': 'true', 'type': 'string'}, 'sha': {'description': 'Chỉ cho tao-tag: SHA40 đích. Một SHA cho một tag, cùng thứ tự với ô ref.', 'required': 'false', 'type': 'string'}, 'xac_nhan': {'description': 'Gõ XOA để xoá, TAO để tạo tag. Sai một ký tự là dừng.', 'required': 'true', 'type': 'string'}, 'chi_thu': {'description': 'Thử khô — in ra sẽ làm gì rồi dừng, không đụng ref nào', 'required': 'false', 'default': 'true', 'type': 'boolean'}, 'ly_do': {'description': 'Vì sao dọn. Đi vào log, để nửa năm sau còn đọc được.', 'required': 'false', 'type': 'string'}}}}
 job= don runs-on= ubuntu-latest uses= None matrix= None if= None
 step uses= ['actions/checkout@v4']

FILE .github/workflows/ops-open-pr.yml
name= ops — mở PR bằng git on= {'push': {'branches': ['claude/**', 'ops/**']}}
 job= mo runs-on= ubuntu-latest uses= None matrix= None if= contains(github.event.head_commit.message, '[open-pr]')
 step uses= ['actions/checkout@v4']

FILE .github/workflows/ops-publish-lease.yml
name= ops — đăng lease bằng git on= {'push': {'branches': ['ops/**'], 'paths': ['ops/leases/**.yaml', 'ops/leases/**.yml']}}
 job= dang runs-on= ubuntu-latest uses= None matrix= None if= github.event.head_commit.author.name != 'github-actions[bot]'
 step uses= ['actions/checkout@v4']

FILE .github/workflows/ops-thu-hoi-admission.yml
name= thu-hoi on= {'pull_request_target': {'types': ['opened', 'reopened', 'synchronize', 'ready_for_review', 'edited'], 'branches': ['master']}}
 job= thu-hoi runs-on= ubuntu-latest uses= None matrix= None if= None
 step uses= ['actions/checkout@v4', 'actions/upload-artifact@v4']

```

  kết luận : KHÔNG PHẢI LỖI cho danh sách workflow còn lại — đủ 7 tệp: ci-dot-bien-du và 4 ops-* đều runs-on literal ubuntu-latest; không job-level reusable uses. Chỉ ci.yml và launcher-windows.yml có matrix.os. Riêng câu chỉ launcher trên master cần thử dispatch ở hướng kế tiếp.

### HƯỚNG 8: launcher-windows: paths, labeled, if và phạm vi đo
  giả thuyết : Label là điều kiện đủ cho PR, hoặc launcher đo toàn bộ gate.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
from pathlib import Path
import yaml
p=Path('.github/workflows/launcher-windows.yml')
d=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
print('on=', d['on'])
j=d['jobs']['launcher']
print('job.if=',j['if']); print('job.matrix=',j['strategy']['matrix']); print('job.runs-on=',j['runs-on'])
for s in j['steps']:
 if 'run' in s: print('step=',s.get('name'), 'if=',s.get('if'), 'run-first-line=',s['run'].splitlines()[0])
print('PR paths excludes workflow-only diff:',d['on']['pull_request']['paths'])
PROBE
```
  output thật (rc=0) :
```text
on= {'workflow_dispatch': {'inputs': {'runner_set': {'description': 'Nền cần đo trong lượt gọi tay', 'required': 'true', 'default': 'windows-only', 'type': 'choice', 'options': ['windows-only', 'windows-and-ubuntu']}}}, 'push': {'branches': ['master'], 'paths': ['.claude/dev/**', '.github/workflows/launcher-windows.yml']}, 'pull_request': {'types': ['opened', 'synchronize', 'reopened', 'labeled'], 'paths': ['.claude/dev/**']}}
job.if= github.event_name != 'pull_request' || contains(github.event.pull_request.labels.*.name, 'windows')
job.matrix= {'os': '${{ fromJSON(github.event_name == \'workflow_dispatch\' && inputs.runner_set == \'windows-only\' && \'["windows-latest"]\' || \'["windows-latest","ubuntu-latest"]\') }}'}
job.runs-on= ${{ matrix.os }}
step= Checkout LF if= None run-first-line= git config --global core.autocrlf false
step= Su that ve nen chay if= None run-first-line= python -c "import platform,sys;print('he:',platform.system(),'| python:',sys.version.split()[0])"
step= Install tool manifest dependencies if= None run-first-line= python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0
step= Install and verify test tools if= None run-first-line= set -euo pipefail
step= Verify tool manifest and shellcheck canary if= None run-first-line= python ops/cong_cu.py kiem-tra --json
step= doctor if= None run-first-line= python .claude/dev/launcher.py doctor
step= Bo phan chung (day du, giu nguyen danh sach bo qua) if= None run-first-line= python .claude/dev/launcher_test.py
step= Tu dot bien if= None run-first-line= python .claude/dev/launcher_test.py --dot-bien
step= Cay lam viec phai SACH sau khi chay test if= None run-first-line= $ban = git status --porcelain
step= Probe: dut ong KHONG duoc nuot ma that if= runner.os == 'Windows' run-first-line= # Tren Linux da do: 0 khi du cong cu, 12 khi thieu, o CA BA kieu cat ong.
step= Probe: console cp1258 + duong dan co dau tieng Viet if= runner.os == 'Windows' run-first-line= chcp 1258
step= Probe: t62 chay rieng (ca CHUA TUNG chay o bat ky vong nao) if= runner.os == 'Windows' run-first-line= python -c @"
step= Probe: taskkill /T tren tien trinh do CHINH minh sinh if= runner.os == 'Windows' run-first-line= # Vong 2 ket luan "Access denied" la han che sandbox codex chu khong phai
PR paths excludes workflow-only diff: ['.claude/dev/**']

```

  kết luận : KHÔNG PHẢI LỖI — PR còn cần paths=.claude/dev/** và activity type phù hợp; nhãn là điều kiện cần của job.if. “Chỉ chạy khi có nhãn” không hứa nhãn là điều kiện đủ, nên không nâng việc không liệt kê PR paths thành finding. Đã đo và ghi đầy đủ paths để tránh áp dụng nhãn cho PR chỉ sửa scripts/ hoặc workflow. Push master, matrix hai nền, types labeled và phạm vi launcher đều đúng.

### HƯỚNG 9: Cò ẩn: schedule/workflow_run/reusable/dispatch tự động
  giả thuyết : Một workflow tự gọi ci.yml hoặc schedule tạo gate Windows dù PR không nhãn và không gọi tay.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
from pathlib import Path
import yaml
for p in sorted(Path('.github/workflows').rglob('*')):
 if not p.is_file(): continue
 d=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
 print(p.name,'events=',list(d.get('on',{})))
 if p.name == 'ci.yml':
  print('chuan-bi.outputs.os=',d['jobs']['chuan-bi']['outputs']['os'])
 else:
  for name,j in d.get('jobs',{}).items():
   for s in j.get('steps',[]):
    if 'run' in s:
     lines=[l for l in s['run'].splitlines() if l.strip() and not l.lstrip().startswith('#')]
     print('run',name,s.get('name',s.get('id','unnamed')),repr('\n'.join(lines)[:210]))
PROBE
rg -n --max-columns 250 'gh[[:space:]]+workflow|actions/workflows|createWorkflowDispatch|/dispatches|workflow_run:|repository_dispatch:|workflow_call:|schedule:' .github ops .claude/dev scripts -g '*.py' -g '*.yml' -g '*.yaml' -g '*.sh' -g '!ops/reviews/**' -g '!ops/land/**'

```
  output thật (rc=0) :
```text
ci-dot-bien-du.yml events= ['schedule', 'workflow_dispatch']
run dot-bien-du Force LF checkout (hash parity với manifest) 'git config --global core.autocrlf false\ngit config --global core.eol lf\ngit config --global core.abbrev 7'
run dot-bien-du cài PyYAML + jsonschema (cổng đăng lease + validator verdict cần) 'python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0'
run dot-bien-du cài actionlint cho G5 'bash ops/cai_actionlint.sh'
run dot-bien-du cài shellcheck cho G5 (cài xong đo lại) 'bash ops/cai_cong_cu.sh shellcheck'
run dot-bien-du cài rg cho G5 (cài xong đo lại) 'bash ops/cai_cong_cu.sh rg'
run dot-bien-du G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6 'python ops/cong_cu.py kiem-tra --json'
run dot-bien-du cài Ruff 0.15.15 và in probe dương 'python -m pip install --quiet ruff==0.15.15\nruff --version'
run dot-bien-du test registry (phạm vi + các bộ chưa được nối) 'python .claude/dev/ci_dang_ky_test.py --chay'
run dot-bien-manh đột biến một mảnh 'python ops/nhanh_don_duoc_test.py'
run dot-bien-gop gom mảnh 'python ops/nhanh_don_duoc_test.py --gop-du manh'
ci.yml events= ['push', 'pull_request', 'workflow_dispatch']
chuan-bi.outputs.os= ${{ (github.event_name == 'workflow_dispatch' || contains(github.event.pull_request.labels.*.name, 'windows')) && '["ubuntu-latest","windows-latest"]' || '["ubuntu-latest"]' }}
launcher-windows.yml events= ['workflow_dispatch', 'push', 'pull_request']
run launcher Checkout LF 'git config --global core.autocrlf false\ngit config --global core.eol lf'
run launcher Su that ve nen chay 'python -c "import platform,sys;print(\'he:\',platform.system(),\'| python:\',sys.version.split()[0])"\npython -c "import sys;print(\'stdout encoding:\',sys.stdout.encoding)"\nWrite-Host "PYTHONUTF8      = \'$env:PYTHONU'
run launcher Install tool manifest dependencies 'python -m pip install --quiet PyYAML==6.0.3 jsonschema==4.26.0'
run launcher Install and verify test tools 'set -euo pipefail\nif [ "${RUNNER_OS:-}" = "Linux" ]; then sudo apt-get update -qq; fi\nfor tool in shellcheck rg actionlint; do\n  bash ops/cai_cong_cu.sh "$tool"\ndone'
run launcher Verify tool manifest and shellcheck canary 'python ops/cong_cu.py kiem-tra --json'
run launcher doctor 'python .claude/dev/launcher.py doctor'
run launcher Bo phan chung (day du, giu nguyen danh sach bo qua) 'python .claude/dev/launcher_test.py'
run launcher Tu dot bien 'python .claude/dev/launcher_test.py --dot-bien'
run launcher Cay lam viec phai SACH sau khi chay test '$ban = git status --porcelain\nif ($ban) { Write-Host "BAN:`n$ban"; exit 1 }\nWrite-Host \'sach\''
run launcher Probe: dut ong KHONG duoc nuot ma that '$loi = 0\npython .claude/dev/launcher.py doctor | Out-Null\n$ma = $LASTEXITCODE\nWrite-Host "CHOT | du cong cu   | Out-Null -> rc=$ma (mong doi 0)"\nif ($ma -ne 0) { $loi++ }\n$duong = Split-Path (Get-Command python'
run launcher Probe: console cp1258 + duong dan co dau tieng Viet 'chcp 1258\nmkdir "Quoc hoi ban do"\ngit init -q "Quoc hoi ban do\\kho"\ngit -C "Quoc hoi ban do\\kho" -c user.email=a@b -c user.name=c commit -q --allow-empty -m x\npython .claude\\dev\\launcher.py check --workspace "Q'
run launcher Probe: t62 chay rieng (ca CHUA TUNG chay o bat ky vong nao) 'python -c @"\nimport importlib.util, sys\nsp = importlib.util.spec_from_file_location(\'LT\', \'.claude/dev/launcher_test.py\')\nM = importlib.util.module_from_spec(sp); sys.modules[\'LT\'] = M; sp.loader.exec_module(M)'
run launcher Probe: taskkill /T tren tien trinh do CHINH minh sinh '$p = Start-Process python -ArgumentList \'-c "import time; time.sleep(60)"\' -PassThru\nStart-Sleep -Seconds 1\nif (-not (Get-Process -Id $p.Id -ErrorAction SilentlyContinue)) {\n  Write-Host "FIXTURE HONG: tien tri'
ops-don-ref.yml events= ['workflow_dispatch']
run don khai đầu vào vào log 'set -euo pipefail\nprintf \'hành động : %s\\n\' "$HANH_DONG"\nprintf \'ref       : %s\\n\' "$REF"\nprintf \'sha       : %s\\n\' "${SHA:-(không)}"\nprintf \'chỉ thử   : %s\\n\' "$CHI_THU"\nprintf \'người bấm : %s\\n\' "${GITHUB_ACT'
run don chốt — xác nhận, danh sách bảo vệ, dạng tên 'set -euo pipefail\nMONG=XOA; [ "$HANH_DONG" = tao-tag ] && MONG=TAO\nif [ "$XAC_NHAN" != "$MONG" ]; then\n  echo "DỪNG: xac_nhan phải đúng bằng \'$MONG\' (nhận \'$XAC_NHAN\')"; exit 2\nfi\nMAC_DINH=$(gh api "repos/$GITH'
run don làm, rồi ĐO LẠI trạng thái thật 'set -euo pipefail\nLOAI=heads; [ "$HANH_DONG" != xoa-nhanh ] && LOAI=tags\nNEO_TEP="${NEO_TEP:-${RUNNER_TEMP:-/tmp}/don_ref_neo.txt}"\nDS=(); DSS=()\nIFS=\',\' read -ra _R <<< "$REF"\nfor x in "${_R[@]}"; do\n  x="${x#'
ops-open-pr.yml events= ['push']
run mo mở PR nếu chưa có 'set -euo pipefail\nDA_CO=$(gh pr list --head "$NHANH" --state open --json number --jq \'length\')\nif [ "$DA_CO" != "0" ]; then\n  echo "nhánh $NHANH đã có PR mở — không mở thêm"\n  exit 0\nfi\nTIEU_DE=$(git log -1 --p'
ops-publish-lease.yml events= ['push']
run dang cài PyYAML 'python3 -m pip install --quiet PyYAML==6.0.3'
run dang neo bộ kiểm vào nhánh mặc định 'set -euo pipefail\ntest -n "$MAC_DINH"\ngit fetch --no-tags origin "$MAC_DINH"\nNEO="$RUNNER_TEMP/neo"          # NGOÀI workspace: không làm bẩn cây được đẩy\ngit worktree add --detach "$NEO" "origin/$MAC_DINH"\ntes'
run dang tự kiểm cổng trước khi tin nó (cài công cụ + chạy cổng) 'bash "$NEO/ops/chay_lease_publish_test.sh"'
run dang tìm lease vừa đổi 'set -euo pipefail\ntest -n "${NAY:-}"\ntest -n "${MAC_DINH:-}"\nTU=""\nif [ -n "${TRUOC:-}" ] \\\n   && [ "$TRUOC" != "0000000000000000000000000000000000000000" ] \\\n   && git cat-file -e "${TRUOC}^{commit}" 2>/dev/nu'
run dang đăng 'set -euo pipefail\nBI_CHAN=0\nbao_chan() {\n  echo "::error file=$tep::$1"\n  BI_CHAN=1\n  echo "::endgroup::"\n}\nwhile IFS= read -r tep; do\n  [ -n "$tep" ] || continue\n  [ -f "$tep" ] || continue\n  echo "::group::$t'
ops-thu-hoi-admission.yml events= ['pull_request_target']
run thu-hoi cài PyYAML 'python3 -m pip install --quiet PyYAML==6.0.3'
run thu-hoi đo S, fetch H từ endpoint canonical, chạy bộ kiểm canonical, ghi receipt 'set -euo pipefail\ncase "$TL_S" in *[!0-9a-f]*|"") echo "S không phải sha40: $TL_S" >&2; exit 12;; esac\ncase "$TL_H" in *[!0-9a-f]*|"") echo "H không phải sha40: $TL_H" >&2; exit 12;; esac\nif [ "${#TL_S}" -ne 40'
.github/workflows/ci-dot-bien-du.yml:14:  schedule:
.claude/dev/gh_readback.py:32:   `gh workflow run ... | tail -3; echo rc=$?` in `rc=0` trong khi `gh` ăn HTTP 503

```

  kết luận : KHÔNG PHẢI LỖI cho hệ quả có điều kiện tại reviewed_sha: ci chỉ có push/master, pull_request và dispatch; schedule chỉ ở ci-dot-bien-du chạy Ubuntu; không thấy workflow_run/repository_dispatch/workflow_call hoặc lời gọi dispatch trong mã sống đã quét. KHÔNG ĐO ĐƯỢC automation ngoài kho và mọi run tương lai. Tuy nhiên ci.yml workflow_dispatch trên ref master là phản ví dụ cho câu không điều kiện “Windows trên master hiện chỉ đến từ launcher-windows.yml” (P2). Ghi chú kỹ thuật: lần dựng lệnh hướng 9 đầu bị SyntaxError ở harness ngoài kho (rc=1); lệnh trên là bản đã sửa và đã chạy.

### HƯỚNG 10: Các câu giữ nguyên: labeled, EOL và dấu vết #109
  giả thuyết : ci.yml đã thêm types labeled hoặc đổi if của bước EOL khiến lời cũ sai.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
from pathlib import Path
import yaml
p=Path('.github/workflows/ci.yml'); d=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
print('pull_request=',repr(d['on']['pull_request']))
print('workflow_dispatch=',repr(d['on']['workflow_dispatch']))
for name,j in d['jobs'].items():
 for s in j.get('steps',[]):
  if s.get('name') == 'PR head contains required EOL base' or 'release-verify strict (lane' in s.get('name',''):
   print('job=',name, 'step=',s['name'],'if=',s.get('if'),'run=',s.get('run'))
PROBE
git log --all --format='%h %s' --extended-regexp --grep='^Merge pull request #109([[:space:]]|$)'
git show --format=fuller 05170b4 -- CLAUDE.md
git show --format=fuller 3736fc0 -- CLAUDE.md

```
  output thật (rc=0) :
```text
pull_request= ''
workflow_dispatch= ''
job= gate step= PR head contains required EOL base if= ${{ github.event_name == 'pull_request' }} run= set -eu
test -n "$PR_HEAD_SHA"
git cat-file -e "${PR_HEAD_SHA}^{commit}"
git cat-file -e "${EOL_BASE_SHA}^{commit}"
git merge-base --is-ancestor "$EOL_BASE_SHA" "$PR_HEAD_SHA"

job= gate step= release-verify strict (lane LAND — manifest committed) if= github.ref == 'refs/heads/master' run= python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
job= gate step= release-verify strict (lane WORKER — manifest TẠM ngoài repo) if= github.ref != 'refs/heads/master' run= set -euo pipefail
TAM="$RUNNER_TEMP/tl-manifest-tam.json"
NKY="$RUNNER_TEMP/tl-manifest-tam.log"
# Cả hai lệnh in ~900 dòng JSON, nên đẩy ra tệp — nhưng IM LẶNG lúc ĐỎ là mất chẩn
# đoán đúng lúc cần nhất, nên hỏng thì `cat` ra log. Đã đo: redirect chạy được cả khi
# `RUNNER_TEMP` mang dạng Windows (ổ đĩa + dấu chéo ngược) dưới Git Bash.
python scripts/tl.py release-manifest --root . --out "$TAM" --json > "$NKY" || { cat "$NKY"; exit 1; }
python scripts/tl.py release-verify "$TAM" --root . --strict --json > "$NKY" || { cat "$NKY"; exit 1; }
python - "$TAM" <<'PY'
import json, subprocess, sys
ra = subprocess.run(["git", "ls-files", "-z"], capture_output=True, check=True).stdout
theo_doi = set(ra.decode("utf-8").split(chr(0))) - {""}
duong = [f["path"] for f in json.load(open(sys.argv[1], encoding="utf-8"))["files"]]
thua = sorted(p for p in duong if p not in theo_doi)
for p in thua:
    print("TEP THUA trong cay, git khong theo doi:", p)
if thua:
    sys.exit(1)
print("manifest tam:", len(duong), "tep, tat ca deu duoc git theo doi")
PY

9796f67 Merge pull request #109 — ba lần đọc sai tín hiệu trong một phiên
commit 05170b4431b5d68632de2d9fc517b0eef9acb680
Author:     Claude <noreply@anthropic.com>
AuthorDate: Fri Aug 14 12:48:03 2026 +0000
Commit:     Claude <noreply@anthropic.com>
CommitDate: Fri Aug 14 12:48:03 2026 +0000

    docs: nói CÓ ĐIỀU KIỆN câu về đo Windows — ma trận có nhãn windows và workflow_dispatch
    
    Cross-review nêu P2 trên PR #109: câu 'mỗi lần merge là lần đo Windows đầu tiên'
    không đúng cho PR gắn nhãn windows hay head chạy qua workflow_dispatch — ma trận
    trong ci.yml kèm windows-latest cho cả hai. Bỏ điều kiện là đánh lừa người đang
    xem đúng một PR như vậy.
    
    Nay giới hạn vào PR THƯỜNG, và nêu luôn hai đường có sẵn để đo Windows trước khi
    merge. Trớ trêu: đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó.
    
    Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
    Claude-Session: https://claude.ai/code/session_019Dbx4qP9DYD4zv91vpm8Td

diff --git a/CLAUDE.md b/CLAUDE.md
index 73a2dc2..3594a64 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -138,8 +138,15 @@ Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package 
   trước. **Muốn biết đã review chưa thì tìm dòng `Reviewed commit:` cho ĐÚNG commit đang xét.**
   · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
   còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
-  hành). Nên **"PR xanh" không hàm ý "master xanh"**: mỗi lần merge là lần đo Windows ĐẦU TIÊN của mã
-  đó. Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
+  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
+  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
+  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
+  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
+  trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
+  **Muốn có Windows TRƯỚC khi merge thì có sẵn hai đường: gắn nhãn `windows`, hoặc gọi tay
+  `workflow_dispatch`.** Đợt 14-08 không dùng đường nào trong hai, nên cả sáu lần merge của đợt đúng
+  là sáu lần đo Windows đầu tiên. Kèm theo: trên lượt master, bước `PR head contains required EOL
+  base` LUÔN `skipped` vì nó có
   `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   lượt PR; bê nguyên sang lượt master là tự báo động giả.
   Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì
commit 3736fc0a69f38019cd54f39273e44655f38d40f6
Author:     Claude <noreply@anthropic.com>
AuthorDate: Fri Aug 14 12:54:19 2026 +0000
Commit:     Claude <noreply@anthropic.com>
CommitDate: Fri Aug 14 12:54:19 2026 +0000

    docs: gắn nhãn windows KHÔNG đủ cho PR đang mở — phải có cò mới
    
    Cross-review nêu P2 thứ hai trên PR #109, và nó là hệ quả trực tiếp của bản vá
    trước: ci.yml khai pull_request mà không khai types, nên mặc định chỉ bắn ở
    opened/synchronize/reopened — labeled không nằm trong đó. Gắn nhãn cho một PR đang
    mở không sinh lượt chạy nào; người làm theo sẽ thấy đúng một check Ubuntu rồi merge
    mà tưởng đã có Windows.
    
    Nay nêu workflow_dispatch là đường chắc chắn, và nói rõ nhãn cần kèm một cò mới.
    
    Co-Authored-By: Claude Opus 5 <noreply@anthropic.com>
    Claude-Session: https://claude.ai/code/session_019Dbx4qP9DYD4zv91vpm8Td

diff --git a/CLAUDE.md b/CLAUDE.md
index 3594a64..c885bf1 100644
--- a/CLAUDE.md
+++ b/CLAUDE.md
@@ -143,10 +143,15 @@ Phiên dev trên máy này ≠ phiên Cowork LIVE (bootstrap từ zip Package 
   trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
   ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
   trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
-  **Muốn có Windows TRƯỚC khi merge thì có sẵn hai đường: gắn nhãn `windows`, hoặc gọi tay
-  `workflow_dispatch`.** Đợt 14-08 không dùng đường nào trong hai, nên cả sáu lần merge của đợt đúng
-  là sáu lần đo Windows đầu tiên. Kèm theo: trên lượt master, bước `PR head contains required EOL
-  base` LUÔN `skipped` vì nó có
+  **Muốn có Windows TRƯỚC khi merge thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
+  Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
+  trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
+  `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
+  chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
+  check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
+  (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
+  Đợt 14-08 không dùng đường nào, nên cả sáu lần merge của đợt đúng là sáu lần đo Windows đầu tiên.
+  Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
   `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   lượt PR; bê nguyên sang lượt master là tự báo động giả.
   Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì

```

  kết luận : KHÔNG PHẢI LỖI về YAML: pull_request null, không types; labeled không được đăng ký; EOL if đúng pull_request nên push/dispatch master không chạy bước đó. Dấu vết hai lần sửa trên nhánh đã merge #109 đo được; raw review/comment và default event semantics trên máy chủ KHÔNG ĐO trực tiếp được khi không mạng. Bộ mặc định opened/synchronize/reopened được tài liệu và lịch sử repo mô tả nhất quán; không giả lập API thật.

### HƯỚNG 11: Snapshot 14-08 và lời khai sáu lần đo đầu
  giả thuyết : Chú thích mới hồi tố sai: ma trận ngày 14-08 đã bỏ vế master, hoặc có thể khẳng định đủ sáu lần đầu từ Git.

  lệnh (cwd=cay-kho/) :
```bash
git log -1 --format='%H %cI %s' --until='2026-08-14T23:59:59+07:00' b38fce83 -- .github/workflows/ci.yml
git show a323974:.github/workflows/ci.yml | nl -ba | sed -n '10,19p;33,52p'
git log --first-parent --format='%h %cI %s' --since='2026-08-14T00:00:00+07:00' --until='2026-08-14T19:00:00+07:00' b38fce83
git show 05170b4:CLAUDE.md | nl -ba | sed -n '138,156p'
python3 - <<'PROBE'
import json
from pathlib import Path
from collections import Counter
count=Counter(); samples=[]
for p in Path('ops').rglob('*.json'):
 try: d=json.loads(p.read_text())
 except (OSError,ValueError): continue
 objs=d if isinstance(d,list) else [d]
 for x in objs:
  if not isinstance(x,dict): continue
  if any(str(x.get(k,'')).startswith('2026-08-14') for k in ('created_at','started_at','run_started_at','updated_at')) and ('jobs' in x or 'event' in x or 'workflow_id' in x):
   samples.append(str(p))
print('ops JSON run-like snapshots for 2026-08-14:',sorted(set(samples)))
PROBE

```
  output thật (rc=0) :
```text
a323974f0303c3c462db2ef6fe77498063167f3d 2026-08-13T08:56:12+00:00 CI: cắt ~73% phút Actions — gate đang chết vì cạn hạn mức, không phải vì lỗi
    10	on:
    11	  push:
    12	    branches: [master]
    13	  pull_request:
    14	  # r226 — CHỖ HỞ ĐÃ TRẢ GIÁ 9 RUN: hai cò trên chỉ bắn ở master và ở PR, nên nhánh làm việc KHÔNG bao
    15	  # giờ được gate soi. Đợt r225 nối 3 guard vào CI mà nhánh không chạy được ⇒ tưởng đã đóng nhưng chưa
    16	  # từng chạy lần nào. `workflow_dispatch` cho phép soi gate theo yêu cầu trên BẤT KỲ ref nào, không
    17	  # phải mở PR mới biết. (GitHub đòi workflow có mặt ở nhánh mặc định thì nút này mới dùng được ⇒ chỉ
    18	  # hiệu lực SAU khi bản này lên master.)
    19	  workflow_dispatch:
    33	
    34	jobs:
    35	  gate:
    36	    strategy:
    37	      fail-fast: false
    38	      matrix:
    39	        # Windows tốn GẤP ĐÔI phút. Chạy nó ở nơi thật sự cần: trước khi vào master,
    40	        # khi gọi tay, hoặc khi PR được gắn nhãn `windows` (dùng cho PR đụng đường
    41	        # phụ thuộc nền). PR thường vẫn được Linux soi mỗi lần đẩy.
    42	        # KHÔNG phải nới gate: master vẫn luôn qua CẢ HAI nền trước khi phát hành.
    43	        os: ${{ fromJSON(
    44	              (github.event_name == 'workflow_dispatch'
    45	               || github.ref == 'refs/heads/master'
    46	               || contains(github.event.pull_request.labels.*.name, 'windows'))
    47	              && '["ubuntu-latest","windows-latest"]'
    48	              || '["ubuntu-latest"]') }}
    49	    runs-on: ${{ matrix.os }}
    50	    timeout-minutes: 25
    51	    env:
    52	      PYTHONIOENCODING: utf-8
92783f6 2026-08-14T18:54:15+07:00 Merge pull request #106 — bài học tầng vận chuyển cũng chuẩn hoá chuỗi
bbbaf8f 2026-08-14T18:43:31+07:00 Merge pull request #103 — năm bài học đo được của đợt 14-08
05692fe 2026-08-14T18:41:12+07:00 Merge pull request #105 — lưu verdict cross-review wp55 lượt 4 vào kho, neo băm
e344e7c 2026-08-14T18:35:28+07:00 Merge pull request #104 — đảo danh sách CẤM thành danh sách CHO PHÉP ở cổng đăng lease
438fc34 2026-08-14T16:26:11+07:00 Merge pull request #102 — khôi phục xác thực codex qua nhiều môi trường
8492380 2026-08-14T15:41:03+07:00 Merge pull request #101 — chốt chống lặp ra khỏi commit, vào lượt chạy
464124d 2026-08-14T15:11:54+07:00 Merge pull request #100 — lease #4 cho wp55 vào master, t23 quét mọi lease
4dd1d6f 2026-08-14T14:46:34+07:00 Merge pull request #98 — v1.36.68: đăng lease bằng git, lease neo prompt kiểm được, ops/ ra khỏi kiểm kê gói
   138	  trước. **Muốn biết đã review chưa thì tìm dòng `Reviewed commit:` cho ĐÚNG commit đang xét.**
   139	  · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
   140	  còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
   141	  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
   142	  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
   143	  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
   144	  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
   145	  trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
   146	  **Muốn có Windows TRƯỚC khi merge thì có sẵn hai đường: gắn nhãn `windows`, hoặc gọi tay
   147	  `workflow_dispatch`.** Đợt 14-08 không dùng đường nào trong hai, nên cả sáu lần merge của đợt đúng
   148	  là sáu lần đo Windows đầu tiên. Kèm theo: trên lượt master, bước `PR head contains required EOL
   149	  base` LUÔN `skipped` vì nó có
   150	  `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   151	  lượt PR; bê nguyên sang lượt master là tự báo động giả.
   152	  Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì
   153	  chưa chạy" nhìn giống hệt nhau** nếu hỏi sai chỗ. Chốt chung, rẻ và luôn dùng được: trước khi kết
   154	  luận từ một chỗ RỖNG, hỏi "nếu thứ tôi đang tìm CÓ THẬT thì nó sẽ được ghi ở đâu?" — rồi đi hỏi
   155	  đúng chỗ đó. Máy không canh được mục này; nó là kỷ luật đọc.
   156	- **Quét secrets: lọc theo PHẦN MỞ RỘNG là mù ĐÚNG CHỖ secrets nằm.** `Path('.env').suffix == ''` nên
ops JSON run-like snapshots for 2026-08-14: []

```

  kết luận : KHÔNG PHẢI LỖI về lịch sử ma trận — commit thay workflow gần nhất trước cuối 14-08 là a323974 (13-08), còn vế github.ref master. Output thực tế có TÁM merge trước 19:00 +07 ngày 14-08 (#98,#100,#101,#102,#104,#105,#103,#106), không phải sáu. Chưa định danh được phạm vi “đợt” gồm đúng sáu lượt mà tác giả muốn nói; lời sáu lần đầu đã có tại 05170b4. Không lấy số merge cả ngày để bác số của một đợt chưa định danh. KHÔNG ĐO ĐƯỢC lịch sử label/dispatch và job Windows thực sự của sáu lượt ấy: không có readback run ngày 14-08 tìm thấy dưới ops, Git không lưu event API. Không dùng lời cũ làm bằng chứng dương cho sự vắng mặt run Windows trước merge; cũng không tự coi là sai khi chưa có dữ liệu.

### HƯỚNG 12: Mâu thuẫn trong CLAUDE / protocol / ADR-0049
  giả thuyết : Câu mới về OS đánh đồng toàn bộ gate PR/master, trái lane LAND; hoặc tuyệt đối hóa không Windows trái gate tại chỗ.

  lệnh (cwd=cay-kho/) :
```bash
nl -ba CLAUDE.md | sed -n '158,186p;800,811p;945,950p'
nl -ba docs/PROTOCOL_DA_PHIEN.md | sed -n '880,892p;970,983p;1516,1522p'
nl -ba docs/adr/0049-cong-hai-nen-truoc-phat-hanh-khong-phai-moi-lan-land.md | sed -n '1,5p;15,35p'
python3 - <<'PROBE'
from pathlib import Path
import yaml
ci=yaml.load(Path('.github/workflows/ci.yml').read_text(),Loader=yaml.BaseLoader)
for s in ci['jobs']['gate']['steps']:
 if 'release-verify strict (lane' in s.get('name',''):
  print(s['name'],'if=',s.get('if'),'first run=',s['run'].splitlines()[0])
PROBE

```
  output thật (rc=0) :
```text
   158	  · **(c) Ma trận `os` của `ci.yml` KHÔNG phân biệt PR với master — và câu ngược lại từng nằm ở đây.**
   159	  Bản cũ của mục này viết: *"PR thường chỉ chạy `ubuntu`, còn master chạy CẢ `ubuntu` LẪN `windows`"*.
   160	  Câu ấy **ĐÃ CHẾT** từ packet #548 (`CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`, bỏ vế
   161	  `github.ref == 'refs/heads/master'` khỏi output `os` của job `chuan-bi`). **Đo 22-10-2026** trên
   162	  `9e9a74b`: `os` = `["ubuntu-latest","windows-latest"]` CHỈ KHI `github.event_name == 'workflow_dispatch'`
   163	  HOẶC PR mang nhãn `windows`; mọi trường hợp khác — **kể cả push lên master** — là `["ubuntu-latest"]`.
   164	  Bằng chứng chạy được: run `ci.yml` **39354156843** (push merge commit `3a3a3ca` lên master,
   165	  20-10-2026) có **23 job, cả 23 nhãn `ubuntu-latest`**, 0 job Windows — readback giữ ở
   166	  `ops/land/pr848-wp744-provenance/readback-jobs-39354156843.json`. Doctrine cũ đã kịp làm một biên
   167	  bản land (commit `3f6c694`) khai `jobs: '23/23 success (gom windows)'`; Codex connector bắt thành P1 trên PR #859 (comment
   168	  `r4323607674`), sửa ở PR #865. Đúng bệnh mục này đang dạy: tin một câu GẦN TAY thay vì đọc nhãn job.
   169	  **Windows trên master hiện chỉ đến từ `launcher-windows.yml`**, và CÓ ĐIỀU KIỆN: push master chỉ bắn
   170	  khi đổi `.claude/dev/**` hoặc chính tệp workflow ấy (`paths:`), ma trận `windows-latest` + `ubuntu-latest`;
   171	  PR chỉ chạy khi mang nhãn `windows` (workflow này CÓ khai `types: [..., labeled]`). Nó chỉ đo lane
   172	  launcher, KHÔNG phải gate. Các workflow còn lại (`ci-dot-bien-du` `ops-*`) đều `ubuntu-latest`.
   173	  Hệ quả: với một PR THƯỜNG — không nhãn `windows`, không ai gọi tay — **gate của mã đó KHÔNG BAO GIỜ
   174	  được đo trên Windows, kể cả sau merge**; merge không còn là "lần đo Windows đầu tiên" như bản cũ viết.
   175	  Muốn biết master có Windows hay không thì **đọc nhãn từng job của lượt chạy**, đừng suy từ tên sự kiện.
   176	  **Muốn có Windows cho gate thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
   177	  Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
   178	  trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
   179	  `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
   180	  chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
   181	  check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
   182	  (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
   183	  (Đợt 14-08 không dùng đường nào; khi ấy ma trận còn vế master nên sáu lần merge là sáu lần đo
   184	  Windows đầu tiên — nay cùng tình huống thì là **không lần nào**.)
   185	  Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
   186	  `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   800	- **API CHỈ CÓ TRÊN MỘT NỀN: hỏi trước, đừng đụng thẳng — và một job CI mặc định SKIP
   801	  là một cổng KHÔNG TỒN TẠI.** Hai lần trong cùng một ngày: `os.O_NOFOLLOW` (bot review
   802	  bắt) và `os.getpgid` trong chốt cô lập — cái sau làm suite **0/103** trên
   803	  `windows-latest`, tức bộ test **chưa từng chạy** trên Windows kể từ lúc có chốt ấy.
   804	  Không ai biết, vì job Windows chỉ chạy khi PR có nhãn `windows`. Năm lượt cross-review
   805	  trên Linux không thể thấy, và đã không thấy.
   806	  Ba luật: (1) `hasattr`/`getattr(..., mặc_định)` trước khi đụng API riêng nền; (2)
   807	  truyền **lambda** vào hàm bọc lỗi, đừng truyền thẳng `os.getpgid` — tra thuộc tính
   808	  xảy ra TRƯỚC lời gọi, tức NGOÀI `try`; (3) gán thêm một API mà nền vốn không có thì
   809	  phải **gỡ lại** khi ra khỏi chốt, kẻo nền tự nhận có thứ nó không có.
   810	  Gắn nhãn `windows` cho PR đụng `.claude/dev/**` — nó tốn ~40 phút và trả lại thứ mà
   811	  năm lượt review không mua được.
   945	5. **Thêm/xoá tệp — HOẶC ĐỔI NỘI DUNG một tệp CÓ TRONG manifest — ⇒ tái sinh `RELEASE_MANIFEST.json`, và ghi lại golden NẾU số đếm kiểm kê đổi.**
   946	   **Bản trước của dòng này chỉ viết "Thêm/xoá tệp" — HẸP HƠN chính sự cố nó sinh ra để chặn.**
   947	   `RELEASE_MANIFEST.json` băm NỘI DUNG từng tệp, nên sửa một tệp đã có sẵn cũng làm sha lệch dù `file_count` KHÔNG đổi. Đo 06-09-2026 (r356): sửa `CHANGELOG.md` ⇒ manifest giữ `9e1c4b27…` trong khi thực tế `20779e38…`, `file_count` vẫn 180 cả hai bên. **`CHANGELOG.md` và `requirements.txt` NẰM TRONG manifest; `CLAUDE.md`, `.claude/**`, `docs/**`, `ops/**` thì KHÔNG** — hỏi trước khi đoán.
   948	   Và **lane PR KHÔNG bắt được**: `ci.yml` cho `release-verify strict (lane LAND)` điều kiện `if: github.ref == 'refs/heads/master'`, còn lane WORKER sinh manifest TẠM từ chính cây nên nó **hấp thụ** mọi thay đổi nội dung ⇒ PR xanh, master ĐỎ. Muốn biết trước khi merge thì chạy ĐÚNG lệnh của lane LAND tại chỗ: `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` (đòi `ok=true` và `expected == checked`).
   949	   Bỏ bước này thì phiên deploy KẾ TIẾP ăn gate đỏ không phải do nó (bài học r238: `nlm_auth_convert.py`
   950	   làm `files_scanned` 67→68, golden không ghi lại ⇒ `golden` + `determinism` đỏ trên master cho phiên sau).
   880	|---|---|---|
   881	| T0 | inner loop của Executor | test/fragment trực tiếp cho thay đổi; không phải promotion evidence |
   882	| T1 | packet worker gate | affected fragments/groups cùng always-on write-set, EOL, security, manifest/package và selector guards |
   883	| T2 | trước `ready_for_rereview` | chạy lại T1 trên exact head; full nếu packet sensitive hoặc classifier yêu cầu |
   884	| T3 | integration freeze/`land prepare` | full selftest và release gates trên Windows + Linux cho frozen integration SHA |
   885	| T4 | canonical/`merge_group` | full trên candidate canonical, hoặc reuse duy nhất evidence T3 khi toàn bộ exact identity khớp |
   886	| T5 | exact release artifact | full smoke/verify trên bundle/artifact có hash sẽ phát hành |
   887	
   888	Unknown/unmapped path, selector/catalog/runner/shared fixture hoặc global state thay đổi, security/workflow,
   889	release/manifest/package, EOL hay gate policy thay đổi phải fallback full; classifier lỗi/không đọc được cũng
   890	fallback full. Top-level path filter hoặc job `skipped` không phải evidence: classifier + aggregator bắt buộc tạo
   891	kết quả dương và chặn merge khi required tier thiếu. Evidence chỉ được reuse khi tested SHA/tree, policy/catalog,
   892	runner, OS/runtime matrix và artifact hash (nếu có) khớp chính xác; head hoặc một identity đổi thì chạy lại.
   970	Ghi `passed`, `failed`, `skipped`, `not_run` và `not_measured` riêng. API thiếu quyền chỉ
   971	cho biết endpoint/field ấy chưa đo được; giữ HTTP status và lỗi thực. Có thể thu tiếp theo
   972	chuỗi GraphQL aggregate → jobs/logs → commit statuses, nhưng mỗi nguồn chỉ chứng minh phần
   973	nó chứa. Paginate đủ, chọn đúng SHA/run/attempt/context/producer; statuses không tự có
   974	workflow/runner/command/output. Chỉ nhận khi tổng evidence đủ identity và nội dung dương,
   975	không đổi 403 hay list rỗng thành pass.
   976	
   977	Job `skipped` không được cấp runner là chưa thực thi, không là Windows execution dù tên job
   978	có Windows. `owner_waived` là disposition riêng chỉ khi có waiver bền của owner: nguồn/actor,
   979	exact SHA, context/OS, lý do, phạm vi/hạn và điều kiện thay thế. Giữ nguyên kết quả skipped;
   980	waiver không viết lại nó thành passed, không tự gỡ branch protection. Không có waiver đúng
   981	scope thì required evidence còn thiếu và tiếp tục chặn gate.
   982	
   983	Tiêu chí đột biến riêng phải có receipt dương (baseline) và âm (mutant bị bắt vì đúng tính
  1516	| `ADR-0046` | Tác giả xuyên suốt, reviewer mới mỗi lượt, cắt phiên ở biên packet | Proposed | **0 cổng vận hành**; `adr-song` chỉ canh đăng ký/trạng thái |
  1517	| `ADR-0047` | Nguồn tin cậy cho cổng đọc lease: danh tính ghim, hồ sơ tiến trình, toàn vẹn object | Proposed | **0 cổng** (đo 08-09-2026, `origin/master` `585c7d5`: chưa có adapter/digest/băm object); `adr-song` chỉ canh đăng ký/trạng thái |
  1518	| `ADR-0048` | Trần trục VÒNG nâng theo chỉ thị chủ kho 12-09-2026, thay số của `ADR-0043`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** — `so-canon` vẫn chưa tồn tại (nợ cùng tên) |
  1519	| `ADR-0049` | Cổng hai nền trước phát hành, không phải mỗi lần land | Accepted | có nhắc: `ci.yml` · `deploy-package.*` |
  1520	| `ADR-0050` | `cross_approved` neo vào họ model, không vào hãng công cụ; ba mức bằng chứng model | Accepted | `ops/bien_nhan_v2.py` (`_NEO_LUAT_CHEP_TAY` + chốt tách họ model) |
  1521	| `ADR-0052` | Trần trục LỜI GỌI Codex mỗi PR nâng theo chỉ thị chủ kho 16-10-2026, thay số của `ADR-0036`/`0037`; lượt sau lượt đầu phải có lý do; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** — `codex_review_calls_used` không có bộ đếm trong mã |
  1522	| `ADR-0053` | Trần kích thước packet `sensitive` nâng theo chỉ thị chủ kho 16-10-2026, thay cặp số `sensitive` của `ADR-0044`; hiệu lực neo theo `spec_hash` đóng băng, không hồi tố | Accepted | **0 cổng** |
     1	# ADR-0049 — Cổng hai nền trước phát hành, không phải mỗi lần land
     2	
     3	- **Trạng thái:** Accepted (2026-09-16, chỉ thị chủ kho `ducthangho`; packet #548 `CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND`)
     4	
     5	ADR này ghi nhận việc **đổi tiêu chuẩn gate**: cổng kiểm thử hai nền (Linux và Windows) trước khi phát hành được bảo đảm bằng **cổng tại chỗ của `deploy-package.*`**, KHÔNG phải bằng lane `master` của `.github/workflows/ci.yml`.
    15	## 2. Quyết định: Đổi tiêu chuẩn gate
    16	
    17	1. **Đổi cò Windows trong `ci.yml`:** Bỏ điều kiện `github.ref == 'refs/heads/master'`. Windows chỉ còn kích hoạt khi gọi tay qua `workflow_dispatch` hoặc khi PR có nhãn `windows` (dành cho các thay đổi chạm mã phụ thuộc nền tảng).
    18	2. **Khử trùng lặp qua job `chuan-bi`:** Thêm job `chuan-bi` (chạy trên `ubuntu-latest`, không checkout mã nguồn), tính danh sách nền một lần và xuất qua `outputs.os`. Ba job `gate`, `gate-registry`, `gate-packet-loop` khai `needs: chuan-bi` và đọc `needs.chuan-bi.outputs.os`.
    19	3. **Cổng hai nền tại chỗ của `deploy-package.*`:** Trước khi phát hành gói (`tl drive-push` lên LIVE), người vận hành bắt buộc phải chạy bộ cổng kiểm tra tại chỗ của `deploy-package.ps1` / `deploy-package.sh` (8 cổng: `selftest`, `gen_inst`, `workflow`, `golden`, `docclaims`, `determinism`, `relcheck`, `relverify`). Cổng này chặn thật khi đỏ (dòng 234: `Bad 'GATE ĐỎ — DỪNG, không build/không đẩy'`).
    20	
    21	## 3. Phần mất mát & Rủi ro đã nhận
    22	
    23	- **Mất soi Windows tự động cho ~22 bước test:** Việc bỏ Windows khỏi mỗi lần land vào `master` đồng nghĩa ~22 bước kiểm thử trong `ci.yml` (như `lease_publish_test`, `ci_dang_ky_test`, `packet-loop selftest`) không còn được chạy tự động trên Windows sau mỗi commit vào master.
    24	- **Cổng Windows đang đỏ biến mất khỏi CI không phải vì được chữa:** Tại thời điểm land (commit `a612c70`, run `35232106589`, job `105238582317`), lane `gate (windows-latest)` trên `master` đang đỏ sẵn 15 ca ở bước 18 `lease-publish selftest` (`133/148 đạt`, do `shutil.which("git", path="/usr/bin:/bin")` hardcode tại `ops/lease_publish.py:1106`, nợ WP541). Việc bỏ Windows khỏi `master` làm tín hiệu đỏ này biến mất khỏi CI, nhưng ADR-0049 **KHÔNG** chữa nợ WP541. Nợ WP541 vẫn còn nguyên và được xử lý ở packet riêng.
    25	- **Độ phủ Windows tự động về 0 trên thực tế cho `ops/`, `scripts/`, `.github/`:**
    26	  - `ci.yml` dùng trigger `pull_request` mặc định (không khai `types: [labeled]`), nên gắn nhãn `windows` lên PR đang đứng yên không tự kích hoạt run mới mà chỉ ăn ở lần push kế tiếp (`synchronize`) hoặc khi tạo PR đã có nhãn.
    27	  - Dưới chính sách `manual_ci_budget: 0` (cấm `workflow_dispatch`), Windows tự động không còn chạy cho `ops/**`, `scripts/**`, `.github/**` (WP541 là bằng chứng sống).
    28	  - 8 cổng tại chỗ của `deploy-package.*` là script chạy tay và **không bao gồm** `lease_publish_test` hay các test của `ops/`, nên không thay thế được toàn bộ lane CI bị gỡ.
    29	  - Đây là **rủi ro đã nhận** (K4), được chấp nhận để bảo toàn hạn mức CI. Người điều phối và người phát hành chịu trách nhiệm khi thay đổi chạm mã phụ thuộc nền tảng. Nợ có tên `BATTERY-DEPLOY-HEP-HON-LANE-CI` ghi nhận việc mở rộng danh mục kiểm thử của script deploy khi cần thiết.
    30	
    31	## 4. Lời khai trung thực về Windows CI khi land
    32	
    33	Tuyên bố *"land không còn chạy Windows"* là **KHÔNG đúng tuyệt đối**:
    34	- Workflow `.github/workflows/launcher-windows.yml` (với `paths: .claude/dev/**`) vẫn được giữ nguyên. Mọi thay đổi chạm `.claude/dev/**` khi push vào `master` vẫn kích hoạt và tiêu tốn ~5 phút Windows (Đ6, run `35125176975`).
release-verify strict (lane LAND — manifest committed) if= github.ref == 'refs/heads/master' first run= python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json
release-verify strict (lane WORKER — manifest TẠM ngoài repo) if= github.ref != 'refs/heads/master' first run= set -euo pipefail

```

  kết luận : KHÔNG PHẢI LỖI khi phân biệt đúng phạm vi: tiêu đề ghi ma trận OS, không khẳng định mọi bước PR/master giống nhau; LAND/WORKER vẫn khác và khớp §deploy 5. API CHỈ CÓ TRÊN MỘT NỀN là bài học lịch sử lane launcher, tự động PR cần nhãn, không chứng minh dispatch không tồn tại. ADR-0049 khớp việc bỏ master và giữ launcher; protocol T3 + ADR yêu cầu gate Windows tại chỗ/trước phát hành, không phải một cò GitHub khác. Vì thế không được mở rộng “KHÔNG BAO GIỜ” thành mọi loại gate/mọi thời điểm: nên ghi rõ gate ci.yml tự động tại snapshot đang xét. Đây cùng hướng thu hẹp phạm vi với câu Windows trên master, không phải phát hiện thêm một workflow Windows ẩn.

### HƯỚNG 13: Phản ví dụ chạy được: dispatch gate trên chính master
  giả thuyết : Có thể câu chỉ launcher trên master vẫn đúng nếu dispatch bị loại khỏi ref master.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
import ast,json,re
from pathlib import Path
import yaml
source=Path('ops/lease_publish_test.py').read_text()
module=ast.parse(source)
node=next(n for n in module.body if isinstance(n,ast.FunctionDef) and n.name=='_danh_gia_bieu_thuc_chuan_bi')
namespace={'re':re}
exec(compile(ast.Module(body=[node],type_ignores=[]),'ops/lease_publish_test.py (function only)','exec'),namespace)
eval_os=namespace[node.name]
ci=yaml.load(Path('.github/workflows/ci.yml').read_text(),Loader=yaml.BaseLoader)
expr=ci['jobs']['chuan-bi']['outputs']['os']
print('SOURCE=ops/lease_publish_test.py:'+str(node.lineno)+'; evaluator is extracted unchanged, not GitHub runtime')
for event,ref,labels in [('push','refs/heads/master',[]),('pull_request','refs/pull/1/merge',[]),('pull_request','refs/pull/1/merge',['windows']),('workflow_dispatch','refs/heads/master',[]),('workflow_dispatch','refs/heads/example',[])]:
 result=eval_os(expr,{'event_name':event,'ref':ref,'labels':labels})
 print(json.dumps({'event':event,'ref':ref,'labels':labels,'os':result},ensure_ascii=False))
print('job gate runs-on=',ci['jobs']['gate']['runs-on'],'matrix=',ci['jobs']['gate']['strategy']['matrix'])
assert eval_os(expr,{'event_name':'workflow_dispatch','ref':'refs/heads/master','labels':[]}) == ['ubuntu-latest','windows-latest']
print('COUNTEREXAMPLE PASS: ci.yml dispatch on master selects windows-latest, without launcher-windows.yml')
PROBE
```
  output thật (rc=0) :
```text
<unknown>:2961: SyntaxWarning: invalid escape sequence '\s'
<unknown>:5104: SyntaxWarning: invalid escape sequence '\d'
SOURCE=ops/lease_publish_test.py:7848; evaluator is extracted unchanged, not GitHub runtime
{"event": "push", "ref": "refs/heads/master", "labels": [], "os": ["ubuntu-latest"]}
{"event": "pull_request", "ref": "refs/pull/1/merge", "labels": [], "os": ["ubuntu-latest"]}
{"event": "pull_request", "ref": "refs/pull/1/merge", "labels": ["windows"], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "workflow_dispatch", "ref": "refs/heads/master", "labels": [], "os": ["ubuntu-latest", "windows-latest"]}
{"event": "workflow_dispatch", "ref": "refs/heads/example", "labels": [], "os": ["ubuntu-latest", "windows-latest"]}
job gate runs-on= ${{ matrix.os }} matrix= {'os': '${{ fromJson(needs.chuan-bi.outputs.os) }}'}
COUNTEREXAMPLE PASS: ci.yml dispatch on master selects windows-latest, without launcher-windows.yml

```

  kết luận : LỖI P2 — evaluator có sẵn của kho, trích nguyên hàm bằng AST để không chạy suite/import side effect, xác nhận dispatch trên master và ref khác đều cho Windows. Đây là phép đo logic cục bộ, không phải tuyên bố đã tạo một Actions run. Câu L169 cần giới hạn ở tự động khi push master; không có chốt ref chặn dispatch trên master.

### HƯỚNG 14: Chống nhầm hiện vật: quote cũ, checksum/readback và EOL thực tế
  giả thuyết : Run đúng nhãn nhưng readback đã bị sửa sau này, hoặc EOL không thật sự skipped trên master.

  lệnh (cwd=cay-kho/) :
```bash
git show 9e9a74b:CLAUDE.md | nl -ba | sed -n '158,178p'
python3 - <<'PROBE'
import hashlib,json,subprocess
from pathlib import Path
root=Path('ops/land/pr848-wp744-provenance')
for basename in ['readback-jobs-39354156843.json','readback-run-39354156843.json']:
 p=root/basename; h=hashlib.sha256(p.read_bytes()).hexdigest()
 expected=next(line.split()[0] for line in (root/'SHA256SUMS').read_text().splitlines() if line.endswith('./'+basename))
 print(basename,'sha256=',h,'matches_SHA256SUMS=',h==expected)
 old=subprocess.check_output(['git','show','3f6c694:'+str(p)])
 print('same bytes at 3f6c694=',old==p.read_bytes())
jobs=json.loads((root/'readback-jobs-39354156843.json').read_text())['jobs']
print('positive_runner_ids=',sum(j.get('runner_id',0)>0 for j in jobs))
for j in jobs:
 for s in j.get('steps',[]):
  if s.get('name')=='PR head contains required EOL base':
   print('EOL actual job=',j['name'],'step.conclusion=',s['conclusion'],'head=',j['head_sha'])
print('ci workflow os unchanged since example run=',subprocess.check_output(['git','show','3a3a3ca:.github/workflows/ci.yml']).decode().split('      os:',1)[1].split('      che_do:',1)[0] == Path('.github/workflows/ci.yml').read_text().split('      os:',1)[1].split('      che_do:',1)[0])
PROBE
```
  output thật (rc=0) :
```text
   158	  · **(c) Gate PR và gate master KHÔNG phải một thứ.** `ci.yml` cố ý chỉ chạy `ubuntu` cho PR thường,
   159	  còn master chạy CẢ `ubuntu` LẪN `windows` (Windows tốn gấp đôi phút, để dành cho lượt gác cổng phát
   160	  hành). Nên **"PR xanh" không hàm ý "master xanh"**: với một PR THƯỜNG — không gắn nhãn `windows`,
   161	  không ai gọi tay — lần merge chính là lần đo Windows ĐẦU TIÊN của mã đó. Nói CÓ ĐIỀU KIỆN vì ma
   162	  trận cũng kèm `windows-latest` cho PR gắn nhãn `windows` và cho `workflow_dispatch`; bỏ điều kiện
   163	  ấy là đánh lừa người đang xem đúng một PR như vậy (cross-review bắt được, P2 trên PR #109 — và
   164	  trớ trêu là đoạn ngay trên đã trích đúng điều kiện đó rồi vẫn viết câu quên nó).
   165	  **Muốn có Windows TRƯỚC khi merge thì đường CHẮC CHẮN là gọi tay `workflow_dispatch` trên ref đó.**
   166	  Gắn nhãn `windows` KHÔNG đủ cho một PR ĐANG MỞ, và đây là bẫy thật (cross-review bắt, P2 thứ hai
   167	  trên PR #109): `ci.yml` khai `pull_request:` mà KHÔNG khai `types:`, nên mặc định chỉ bắn ở
   168	  `opened`/`synchronize`/`reopened` — **`labeled` không nằm trong đó**. Gắn nhãn không tự sinh lượt
   169	  chạy nào; ma trận chỉ đọc nhãn ở lượt bắn KẾ TIẾP. Người làm theo sẽ gắn nhãn, thấy vẫn đúng một
   170	  check Ubuntu, rồi merge mà tưởng đã có Windows. Muốn dùng nhãn thì phải kèm một cò mới sau khi gắn
   171	  (đẩy thêm commit, hoặc đóng rồi mở lại PR) — hoặc khai `types: [..., labeled]` cho workflow.
   172	  Đợt 14-08 không dùng đường nào, nên cả sáu lần merge của đợt đúng là sáu lần đo Windows đầu tiên.
   173	  Kèm theo: trên lượt master, bước `PR head contains required EOL base` LUÔN `skipped` vì nó có
   174	  `if: github.event_name == 'pull_request'` — nên tiêu chí "không bước nào `skipped`" chỉ đúng cho
   175	  lượt PR; bê nguyên sang lượt master là tự báo động giả.
   176	  Cả ba cùng họ với bài học "cổng không nói dối, nó VẮNG MẶT": **"vắng mặt vì sạch" và "vắng mặt vì
   177	  chưa chạy" nhìn giống hệt nhau** nếu hỏi sai chỗ. Chốt chung, rẻ và luôn dùng được: trước khi kết
   178	  luận từ một chỗ RỖNG, hỏi "nếu thứ tôi đang tìm CÓ THẬT thì nó sẽ được ghi ở đâu?" — rồi đi hỏi
readback-jobs-39354156843.json sha256= 6124ae7e587a4a1aaba31aeeab94624dbdc725cd75b7ceb93648bf95ead4fbea matches_SHA256SUMS= True
same bytes at 3f6c694= True
readback-run-39354156843.json sha256= 03049ac19b86b4fc10e42ff9ac3e8545e5a12bcc74e0d13fb467dbfa3b0c2598 matches_SHA256SUMS= True
same bytes at 3f6c694= True
positive_runner_ids= 23
EOL actual job= gate (ubuntu-latest) step.conclusion= skipped head= 3a3a3caca5de4934ff53851feb6994c2c7b84ad5
ci workflow os unchanged since example run= True

```

  kết luận : KHÔNG PHẢI LỖI — lời cũ có trong base; readback trùng SHA256SUMS và cùng byte từ 3f6c694, 23 runner_id dương; EOL trong gate (ubuntu-latest) thực tế skipped. Biểu thức os của lượt ví dụ và snapshot hiện tại trùng; không dùng một run cũ để chứng minh mọi run tương lai.

### HƯỚNG 15: Gợi ý patch -p0 và cây review nguyên vẹn
  giả thuyết : Hint sai định dạng hoặc phép đo vô tình sửa cây được review.

  lệnh (cwd=cay-kho/) :
```bash
python3 - <<'PROBE'
from pathlib import Path
import subprocess,tempfile,hashlib
repo=Path.cwd(); hint=repo.parent/'HINT.patch'
print('hint.sha256=',hashlib.sha256(hint.read_bytes()).hexdigest())
with tempfile.TemporaryDirectory(prefix='pr870-hint-',dir=repo.parent) as tmp:
 p=Path(tmp)/'CLAUDE.md'; p.write_bytes((repo/'CLAUDE.md').read_bytes())
 for mode in ['--dry-run','--forward']:
  argv=['patch',mode,'--batch','-p0','--input',str(hint)]
  r=subprocess.run(argv,cwd=tmp,text=True,capture_output=True)
  print('command=', 'patch '+mode+' --batch -p0 --input ../HINT.patch (cwd=ban sao ngoai kho)')
  print('rc=',r.returncode,'output=',r.stdout.strip(),r.stderr.strip())
  assert r.returncode==0
 changed=p.read_text()
 assert 'Windows tự động khi push master hiện chỉ đến từ' in changed
 assert 'của `ci.yml` theo ma trận hiện tại chỉ đo Ubuntu' in changed
 assert 'Windows trên master hiện chỉ đến từ' not in changed
 print('scratch assertions=PASS; reviewed tree not patched')
PROBE
git rev-parse HEAD HEAD^{tree}
git diff --no-ext-diff --exit-code HEAD --; printf 'tracked_diff_rc=%s\n' "$?"
git diff --cached --no-ext-diff --exit-code; printf 'index_diff_rc=%s\n' "$?"
git status --porcelain=v1 --untracked-files=all
python3 - <<'PROBE'
import subprocess
for args in [ ['git','ls-files','--others','--exclude-standard'], ['git','ls-files','--others','--ignored','--exclude-standard'] ]:
 r=subprocess.run(args,text=True,capture_output=True)
 print(' '.join(args),'rc=',r.returncode,'count=',len(r.stdout.splitlines()))
 if r.stdout: print(r.stdout[:2000])
PROBE
```
  output thật (rc=0) :
```text
hint.sha256= d5de1128840c6b3d81d52f7dcae8d5e939462c160c5075aee4f7214a32f8a5f4
command= patch --dry-run --batch -p0 --input ../HINT.patch (cwd=ban sao ngoai kho)
rc= 0 output= checking file CLAUDE.md 
command= patch --forward --batch -p0 --input ../HINT.patch (cwd=ban sao ngoai kho)
rc= 0 output= patching file CLAUDE.md 
scratch assertions=PASS; reviewed tree not patched
b38fce83d0e97981012072ca2a2023ac726e5b2e
68e6c67e280e58f202658f551da150f783c2116a
tracked_diff_rc=0
index_diff_rc=0
git ls-files --others --exclude-standard rc= 0 count= 0
git ls-files --others --ignored --exclude-standard rc= 0 count= 0

```

  kết luận : KHÔNG PHẢI LỖI — hint dry-run và áp trên bản sao ngoài kho rc=0; assertions đúng; cây nguồn, index sạch, không untracked/ignored mới trong checkout, HEAD/tree giữ nguyên. Đây chỉ là patch-as-hint, chưa áp trên cây thật; executor tự áp, tự đo, tự chịu trách nhiệm commit.

## FINDING

### master-windows-bo-sot-dispatch  [P2]  Giới hạn lời khai Windows trên master vào push tự động
TỆP/DÒNG: `CLAUDE.md:169` (liên quan cách hiểu “KHÔNG BAO GIỜ” tại 173–174).
VẤN ĐỀ: Câu nhấn mạnh “Windows trên master hiện chỉ đến từ launcher-windows.yml” khai rộng hơn cấu hình đã đo. `ci.yml` vẫn khai `workflow_dispatch`; output `chuan-bi.os` chọn Windows theo event này mà không loại `refs/heads/master`. Vì vậy cùng một ref master có thể có Windows từ gate `ci.yml`, đúng như chính dòng 176 hướng dẫn. Thiếu từ “tự động khi push” khiến người đọc lại suy phạm vi phủ Windows từ một câu doctrine thay vì đọc event/ref. Đây là P2 về thiếu điều kiện, không phải P1 cho số job/run/SHA (các số đã đo đều khớp).
ĐÃ THỬ NGHIỆM: HƯỚNG 13, evaluator nguyên hàm `ops/lease_publish_test.py:7848`, lấy biểu thức từ workflow thật: `push + refs/heads/master => [ubuntu-latest]`; `workflow_dispatch + refs/heads/master => [ubuntu-latest, windows-latest]`, `rc=0`, marker `COUNTEREXAMPLE PASS`. HƯỚNG 2/7/9 xác nhận trigger, consumers và không có chốt ref khác. Chưa tạo/chạy Actions run thật vì sandbox không mạng.
GỢI Ý VÁ: Sửa ngay L169 thành “Windows tự động khi push master …”; tại L173–174 giới hạn hệ quả vào các lượt PR/push của `ci.yml` theo ma trận đang đo. Không mở rộng thành mọi gate: protocol T3 và ADR-0049 vẫn nói tới gate Windows tại chỗ trước phát hành. `HINT.patch` là gợi ý cho hai chỗ cùng phạm vi này.
CA KHÓA: Giữ bảng năm context ở HƯỚNG 13, đặc biệt phân biệt push/master với dispatch/master; đối chiếu lại câu mới có nêu phạm vi push tự động. Không cần thêm test sản phẩm cho một sửa tài liệu.
RỦI RO BẢN VÁ: Chỉ thu hẹp mô tả; phải giữ nguyên ngoại lệ dispatch/label và điều kiện paths của launcher. Không đổi workflow, gate policy hoặc miễn nghĩa vụ gate Windows tại chỗ.
ĐỘ TIN: cao.

## CỔNG VÀ GIỚI HẠN CUỐI

- `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **rc=0** — `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- `python3 scripts/tl.py doc-claims-check --json`: **rc=0**, **`"ok": true`**, `flags=[]`, `layers_skipped={}`; 381 advisory, không phải failure. Stdout đầy đủ: `doc-claims-check.json`.
- `HINT.patch`: dạng `patch -p0` từ gốc `cay-kho/`, đã dry-run/apply trên bản sao ngoài repo (**rc=0**); **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.
- Không đo lại API GitHub; chưa xác minh raw comment `r4323607674`, liên kết PR #865, ngày tác giả thực sự chạy phép đo, hay nhãn/dispatch/job thực tế của đợt sáu merge 14-08. Có dấu vết commit cục bộ nhưng không dùng tên branch thay SHA hoặc dùng lời khai làm bằng chứng độc lập.
- Final head/tree nguyên vẹn; tracked/index diff rc=0, untracked=0, ignored=0. Không push; không sửa `cay-kho/`.
