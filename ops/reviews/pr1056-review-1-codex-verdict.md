verdict: changes_requested
reviewed_sha: 1aae17b5534f78767856f93f7d6089adda224f21
Kết quả: 0 P0, 1 P1, 0 P2, 0 P3.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact SHA/tree và phạm vi #1056 | `1aae17b…`; chỉ ops/reviews, 180 tệp/+6714 | `git rev-parse HEAD HEAD^{tree}` → `1aae17b5534f78767856f93f7d6089adda224f21` / `2d0cdcab508a07dd124356fd69635c36efa1d766`; `git diff --numstat 6db9341 HEAD` → 180/+6714/−0, ngoài ops/reviews=0 | có |
| Schema/kind/role/review_axes | 2 / review_delivery_receipt / reviewer / spec, standards_security | `measure_receipts.py`: hai receipt 48 trường; `_thieu` → []; nội dung verdict có phép đo spec và an toàn/quy trình | có về cấu trúc |
| receipt_id và luot | hậu tố a26aab30, 109dcb6a; lượt 1,2 | `measure_receipts.py` → suffix khớp SHA256 verdict và lượt đúng | có |
| packet_id/packet_ghi_chu/target_pull_request | KHONG_AP_DUNG, không lease riêng, chủ kho giao trực tiếp; PR 1050 | Target, trình tự và nội dung #1050 khớp Git/PROMPT; không có nguồn độc lập chứng minh chỉ thị chat hoặc không tồn tại lease ở mọi nơi; ghi chú đã gắn (b) | một phần; phần (b) thuật lại |
| land_merge_commit và ghi chú | `79400f3…` merge #1050; cha 2 f37b519 | `git show -s --format='%H%n%P%n%s' 79400f3` khớp; thời gian 18:55:24Z sau hai lượt review. Người/phiên bấm merge chỉ là lời kể | có về Git; phiên không đo độc lập |
| provider/executor_provider/cross_provider | codex/claude/true | MRI provider openai_codex trùng run; gate giải họ GPT/Claude. Executor là Claude theo nhiệm vụ và hồ sơ #1050/recorded_by, không có runtime executor kèm | có trong phạm vi nguồn; không gọi runtime executor là do_may |
| review_class/review_class_ghi_chu | standard; không lease, chỉ dữ liệu | Protocol §8/ADR-0038/đa-provider §4 chỉ có routine/systemic/sensitive. `measure_class.py` → enum_valid False cả hai; classifier hiện có trên 32/33 path → sensitive; không effective class | **không — P1** |
| assurance/assurance_ghi_chu | lượt 1 cross_reviewed; lượt 2 cross_approved | `measure_receipts.py` + header: lượt 1 changes_requested, lượt 2 approve/0 finding; reviewer GPT do_may, executor Claude theo nguồn khai; run độc lập; không biến thành quyền merge | có trong giới hạn chứng cứ; class vẫn sai |
| verdict/verdict_nguon | changes_requested và approve | Ba dòng đầu hai verdict → đúng verdict, exact reviewed SHA, 0/1/1/0 và 0/0/0/0 | có |
| verdict_path/verdict_sha256/verdict_bytes | a26aab30…/41128; 109dcb6a…/37384 | `measure_artifacts.py`/`measure_receipts.py`: file tồn tại; SHA256 đầy đủ và byte khớp | có |
| nguon_tep/verdict_ban_goc | bản phẳng nguyên byte của VERDICT trong gói | So byte trực tiếp cả hai → True; manifest và blob 7333f97 khớp. Không chứng minh công cụ copy thật là cp hoặc nguồn sandbox chưa vào kho ngoài bằng chứng đã giữ | có về byte; nguồn ban đầu theo provenance |
| reviewed_sha | c24875d…; f37b519… | Header dòng 2 = receipt = run.head; `measure_receipts.py` → HEAD_MATCH True | có |
| reviewed_tree và ghi chú reviewed_sha_nguon | 9382f751…; 23544465…; launcher --expected-head/--require-clean | `git rev-parse X^{tree}` khớp. Run có head/clean; raw argv không được giữ nên không kiểm độc lập flags cụ thể | tree/head có; flags không đo độc lập |
| base_sha/base_sha_ghi_chu | b29da0b… lúc dựng sandbox | First-parent chronology/prompt và final-integrity lượt 1 ghi origin/master=b29da0b. `git merge-base {c24875d,f37b519} 4f11b13` đều b29da0b; không nhầm merge-base sau merge #1050 | phù hợp; lịch sử ref lúc dựng chỉ có nguồn đã lưu |
| evidence_url/evidence_url_ghi_chu | blob ghim 7333f97, trước receipt | `git show 7333f97:<verdict_path>` byte bằng file hiện tại; 7333f97 là cha 1aae17b | có; không GET HTTP |
| so_p0..p3/so_dem_theo/so_dem_nguon | 0/1/1/0 và 0/0/0/0; theo finding/dòng 3 | Đếm heading finding độc lập, so header → counts và IDs đều khớp; mutant so_p1=9 qua cả sáu cổng | có về dữ liệu; cổng không canh số đếm |
| findings_ids/ket_luan | lượt 1 hai slug, lượt 2 [] và cả hai đóng | `measure_receipts.py` → IDS_MATCH True; `measure_closure.py` kiểm diff/lease/nguồn Windows | có |
| xu_ly_finding | f37b519 vá theo nghĩa HINT, lượt 2 xác nhận | Git diff c24875d..f37b519 → ba tệp (land, manifest, log), sửa đúng hai vấn đề và bổ sung đo lease. Tác giả phiên cụ thể chỉ là recorded_by/lời kể | có về thay đổi, không chứng minh session tác giả |
| MRI provider/surface/transport/session_run_id/run_json | openai_codex/codex_cli/machine; 1b0ff763… và 8c095c6b… | Bốn trường bằng run.json tương ứng; đường dẫn tồn tại; hai run ID khác nhau | có theo metadata được giữ |
| MRI run_json_ghi_chu: head/rc/status/clean/time | c24875d / f37b519; 0/xong/true; 790.067s/606.043s | `measure_receipts.py` → khớp; sai khác thời gian do làm tròn <0.0003s | có; clean chỉ lúc phóng |
| Prompt SHA256 | 9705d1982dd8… / 23a3a3f8be4b… | `sha256(PROMPT.md)` = run.prompt_sha256 = checkpoint; log artifact có băm đầy đủ | có |
| MRI cli/model_yeu_cau | codex-cli 0.164.0, command không -m; requested KHONG_DO_DUOC | Run lenh chỉ có program, argc=9 và fingerprint; không raw argv, không CLI version trong stdout/stderr. Không đo độc lập được version/default account/flags | không đo được độc lập; không có chứng cứ trái ngược |
| MRI model/model_da_chay/model_evidence/muc_bang_chung_model | gpt-6.1-sol; do_may | Run DO_DUOC: 30 và 25 event, tất cả gpt-6.1-sol; effort [xhigh]/DO_DUOC cả hai | có theo telemetry đã giữ |
| MRI model_evidence_ref/model_evidence_ghi_chu | run/run.json#model_phuc_vu; 30/25 event, xhigh | Tham chiếu tồn tại, khóa có và count/model/effort khớp (`measure_receipts.py`) | có |
| github_submitter_identity.actor/actor_nguon/ghi_chu | ducthangho, chưa đăng bản chiếu; credential phiên; chỉ actor vận chuyển | actor_nguon gắn (b). Không readback push/comment hoặc credential để xác định người thật. ADR-0040 tách submitter và reviewer đúng | phần (b) không đo độc lập |
| independent_from_executor_session/independent_ghi_chu | true; tiến trình/context khác | Run riêng, prompt tự chứa, không ghi fork; executor session_015… và người ghi sổ session_01W… là lời khai có neo, không có toàn bộ transcript executor | chưa có căn cứ bác; không chứng nhận toàn bộ context/người vận hành |
| anchor.loai/cuong_do/mo_ta | canonical_ancestry/thap; sẽ trung_binh khi land bằng merge | Blob hiện vật có tổ tiên trong branch #1056, chưa là tổ tiên base master 6db9341; không nâng required check/authorization | phù hợp tại commit đang review |
| CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY | workspace-write bao gồm cây; clean lúc phóng | Run sandbox quan sát restricted + to_tien_workspace write và caveat giới hạn lấy mẫu; worktree_sach=true | có, không bảo đảm mọi lệnh đều được sandbox |
| SCRIPT-DO-DOC-DUONG-DAN-SANDBOX | script/log có absolute sandbox paths | Các evidence chứa `/tmp/...`; clone đúng head cần thiết để tái lập, một số script còn phải chỉnh root sang clone hiện có | có; caveat không hứa chỉ clone là chạy ngay |
| TEP-LON-KHONG-VAO-KHO/OMITTED | bỏ diff >500KB và repo copies | Tái lập diff b29da0b..head: 520915B/0aba68a3…; 525788B/1d9762a7…; cả hai đúng OMITTED. Repo copies không có trong tập tracked mới | có; không có băm cho cả clone, chỉ diff |
| SHA256SUMS và không thiếu/thừa | manifest cho toàn bộ tệp gói trừ manifest | 92/92 và 81/81, missing/extra/duplicate/bad_hash đều rỗng/0 (`measure_artifacts.py`) | có |
| stdout/stderr/checkpoint | băm/byte tương ứng run metadata | stdout 379B/401B, stderr 39B cả hai; SHA256 bằng run. Checkpoint fields/hash khớp | có |
| verdict-cu và diff riêng lượt 2 | bản sao lượt 1 và phần vá | Hai file verdict-cu byte bằng VERDICT/HINT lượt 1; diff-tu-luot1.patch bằng git diff c24875d f37b519 (11192B) | có |
| README 2 mục lục + 6 cảnh báo | metadata, links và mô tả không trùng | `measure_readme.py`: 8 hàng mới/8 duy nhất; mỗi lượt 1 TOC +3 caveat, tất cả so khớp True | có |
| nguon_co_tham_quyen | tệp có băm trong kho | Tệp/băm có và khớp; đây là nguồn nội dung, không là merge authority; receipt chú giải ADR-0040 như vậy | phù hợp |
| Baseline cổng | không phá cổng sẵn có | Sáu lệnh → rc=0, 2 validator TỔNG ĐẠT, doctrine 10/0, t26=1/1, t27=2/2, t138=1/1; không skip | có |
| Cưỡng chế khi đột biến | không được suy pass là đo mọi trường | Đổi byte verdict: chỉ t26 đỏ; xoá TOC/caveat: chỉ t27 đỏ; so_p1 1→9: không cổng nào đỏ | đã đo giới hạn, không kết tội dữ liệu gốc |
| Bí mật trong phần thêm mới | phải rà token/key/credential path | `measure_secrets.py`: 180 file, 20 mẫu, secret hits=0, credential path hits=0; pkg scanner rc=0 mỗi gói, mọi tệp gói đều được xét | không thấy trong phạm vi dò mẫu |

## BẢNG SĂN

Nhật ký được nối sau từng hướng thử. Chỉ đọc `cay-kho/`; mọi đột biến sẽ thực hiện trên clone tạm từ `mirror.git`. Không gọi mạng.

### Hướng 1 — exact SHA, phạm vi và merge

LỆNH: `git -C cay-kho rev-parse HEAD 'HEAD^{tree}'`; `git status --porcelain`; `git rev-parse --is-shallow-repository`; `git diff --numstat 6db9341 HEAD` (cộng số dòng độc lập); `git show -s --format='%H%n%P%n%s' 79400f3`.

OUTPUT THẬT:
```text
HEAD=1aae17b5534f78767856f93f7d6089adda224f21
TREE=2d0cdcab508a07dd124356fd69635c36efa1d766
status --porcelain: (rỗng); is-shallow-repository=false
files 180 additions 6714 deletions 0 outside []
79400f3cdc6b780319b66f57c27e5772ad010101
4f11b13c3d286a79dbe9a83547a800005cda0eda f37b5195978f1fe35b9cb55b6f79a2e09d165af0
Merge pull request #1050 from ducthangho/claude/magical-clarke-gzvwbp
```
Kết luận: KHÔNG PHẢI LỖI về HEAD/phạm vi/merge #1050. Log đầy đủ: `evidence/preflight.log`.

### Hướng 2 — hiện vật, checksum, prompt, run và bản sao

LỆNH: `python3 evidence/measure_artifacts.py` (mã đo đi kèm; chỉ đọc, băm SHA256, so byte, `git diff` và `git show`).

OUTPUT THẬT:
```text
ROUND 1: manifest=92, actual=92, missing=[], extra=[], duplicate=0, bad_hash=[]
flat_equal= True sha256= a26aab3018f613c785a1abc3c5e3291d25427be1d872cad0c29bc19c7fc81a35 bytes= 41128
verdict_header= ['verdict: changes_requested', 'reviewed_sha: c24875d00e93e6a98e0a0abd0837e0cbcad65d4d', 'Kết quả: 0 P0, 1 P1, 1 P2, 0 P3.']
run_fields= {"run_id": "1b0ff763deb040368dbd0b50bcefbeaa", "head": "c24875d00e93e6a98e0a0abd0837e0cbcad65d4d", "worktree_sach": true, "ma_thoat": 0, "trang_thai": "xong", "thoi_luong_giay": 790.067, "provider": "openai_codex", "execution_surface": "codex_cli", "transport": "machine", "model_phuc_vu_trang_thai": "DO_DUOC", "effort_phuc_vu": ["xhigh"], "effort_phuc_vu_trang_thai": "DO_DUOC"}
prompt_sha256= 9705d1982dd8680373b8c40348ac61d86fb0802f5fedc08eb341e951cb68878c matches_run= True
model_events= 30 models= ['gpt-6.1-sol']
stdout bytes= 379 hash= 735fbb50ba84af28a913b67390d895afddff42db6a21c4f5563ce2cd2085a91d matches_run= True
stderr bytes= 39 hash= 1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721 matches_run= True
regenerated_diff bytes= 520915 sha256= 0aba68a37e02f9532406b5ae9397271a9614494bcfd84a296a343b35ced43d63 matches_OMITTED= True
tree= 9382f7512f3adf569f1f82c4d597c66fa1b463d7 matches_receipt= True blob_equal= True
receipt_counts= [0, 1, 1, 0] receipt_assurance= cross_reviewed review_class= standard
ROUND 2: manifest=81, actual=81, missing=[], extra=[], duplicate=0, bad_hash=[]
flat_equal= True sha256= 109dcb6aa2325ab048933ab477171ed30a4004b1b335cae515e201efebeb8f11 bytes= 37384
verdict_header= ['verdict: approve', 'reviewed_sha: f37b5195978f1fe35b9cb55b6f79a2e09d165af0', 'Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.']
run_fields= {"run_id": "8c095c6b5f22407a9a443d42a08d7fbc", "head": "f37b5195978f1fe35b9cb55b6f79a2e09d165af0", "worktree_sach": true, "ma_thoat": 0, "trang_thai": "xong", "thoi_luong_giay": 606.043, "provider": "openai_codex", "execution_surface": "codex_cli", "transport": "machine", "model_phuc_vu_trang_thai": "DO_DUOC", "effort_phuc_vu": ["xhigh"], "effort_phuc_vu_trang_thai": "DO_DUOC"}
prompt_sha256= 23a3a3f8be4b87f91bf897b1656add36826168e7dd9253f8ef516bdeba7fd7a5 matches_run= True
model_events= 25 models= ['gpt-6.1-sol']
stdout bytes= 401 hash= 52d8b11fee269dcd1f126a5b064869f542fd4c004ec8e1445091d3be3d39da95 matches_run= True
stderr bytes= 39 hash= 1aa26269eb1cc57f86b235a03cda53c004edb5b1e9fc99d4da4f00843293d721 matches_run= True
regenerated_diff bytes= 525788 sha256= 1d9762a7d9e6ec6f4c724a0c21ba71ac4a816aa76fcb1f23538cab4aa27883db matches_OMITTED= True
tree= 235444656cad85bd969f99907b1dbeb4007d961a matches_receipt= True blob_equal= True
receipt_counts= [0, 0, 0, 0] receipt_assurance= cross_approved review_class= standard
verdict-cu/luot1-VERDICT.md matches_round1= True
verdict-cu/luot1-HINT.patch matches_round1= True
diff-tu-luot1.patch_equal= True git_diff_bytes= 11192
```
Kết luận: KHÔNG PHẢI LỖI về toàn vẹn hiện vật; 92/92 và 81/81 tệp khớp manifest (chuẩn hoá tiền tố `./`), không thiếu/thừa/trùng; hai diff bỏ ngoài kho tái tạo đúng hash/bytes. Phần review_class sẽ kiểm riêng với protocol. SHA256SUMS tự nó không liệt kê chính nó, đúng quy ước manifest.

### Đo cổng — baseline

Cây đo: `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056/cay-kho`. `PYTHONDONTWRITEBYTECODE=1`; không ghi bytecode vào cây review. LỆNH và OUTPUT THẬT (rc lấy trực tiếp subprocess):

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ]
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ]
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ]
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0"
    ]
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  }
}
```
Log đầy đủ: `evidence/baseline-*.log`, mã thoát: `evidence/baseline-*.rc`.

### Hướng 3 — base lịch sử, evidence_url và trạng thái tại commit

LỆNH: `git log --first-parent --format="%H %cI %s" -4 6db9341`; `git show -s --format="%H%n%P%n%cI%n%s" e788a5d b29da0b 4f11b13 7333f97 1aae17b`; `git merge-base {c24875d,f37b519} 4f11b13` (từng lệnh).

OUTPUT THẬT:
```text
6db934145acf6e47d01db5b2dc8c9da417c2d8eb 2026-10-31T02:11:55+07:00 Merge pull request #1054 from ducthangho/claude/epic-ritchie-quvrz1
79400f3cdc6b780319b66f57c27e5772ad010101 2026-10-31T01:55:24+07:00 Merge pull request #1050 from ducthangho/claude/magical-clarke-gzvwbp
4f11b13c3d286a79dbe9a83547a800005cda0eda 2026-10-31T01:46:42+07:00 Merge pull request #1053: land(#1030) hồ sơ land wp1030 r6 — landed false
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 2026-10-31T00:28:50+07:00 Merge pull request #1041 from ducthangho/agent/wp1037-g1-claude
e788a5d0d518f8a08ac13473a85197287fad4fcb
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
2026-10-30T17:34:39+00:00
ops/reviews: hien vat 2 luot cross-review Codex cua packet #1037 (PR #1041)
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
8cdb15a786304bab084b43c8b30c127ae87e2594 91466322f705658ed51b80c7c152f6b77f4f90c6
2026-10-31T00:28:50+07:00
Merge pull request #1041 from ducthangho/agent/wp1037-g1-claude
4f11b13c3d286a79dbe9a83547a800005cda0eda
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 9ff331d2559326568f24359e5dada1b5f5408e79
2026-10-31T01:46:42+07:00
Merge pull request #1053: land(#1030) hồ sơ land wp1030 r6 — landed false
7333f9712ce0ccbae3a39dfb59484c97e8e03019
6db934145acf6e47d01db5b2dc8c9da417c2d8eb
2026-10-30T19:25:07+00:00
ops/reviews: hien vat 2 luot cross-review codex cua PR #1050 (ghi so #1037)
1aae17b5534f78767856f93f7d6089adda224f21
7333f9712ce0ccbae3a39dfb59484c97e8e03019
2026-10-30T19:28:09+00:00
ops/reviews: bien nhan v2 + hang muc luc/canh bao README cho 2 luot cross-review PR #1050
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
```
Kết luận: KHÔNG PHẢI LỖI về base/merge/blob. Hai run bắt đầu 17:53:06Z và 18:09:50Z, sau merge b29da0b lúc 17:28:50Z và trước merge kế tiếp trên first-parent master (4f11b13 lúc 18:46:42Z). Đồ thị Git phù hợp base b29da0b; merge-base với master ngay trước merge #1050 cũng là b29da0b. Merge-base với master HIỆN TẠI ra chính reviewed head vì #1050 đã merge, không dùng kết quả đó để kết tội base lịch sử. Không có snapshot ref master của đúng thời điểm dựng sandbox trong run.json nên thời điểm ref ấy chỉ đối chiếu gián tiếp qua timestamp commit/prompt. Cả hai evidence_url ghim 7333f97 tồn tại, byte khớp (Hướng 2), và 7333f97 là cha của commit đang review. Cường độ thap tại 1aae17b chưa lên master là phù hợp; không suy thành required check/quyền land.

Kết luận baseline: KHÔNG PHẢI LỖI. Cả sáu cổng rc=0 và có bằng chứng dương: `TỔNG: ĐẠT` ở hai validator, doctrine-scan 10 tệp/0 chỗ, `t26=1/1`, `t27=2/2`, `t138=1/1`, bỏ qua=0. Không xuất hiện `Codex home is inside a repository`.

ĐỘT BIẾN `byte` (chỉ trên clone từ mirror.git tại exact SHA): ops/reviews/pr1050-review-1-codex-verdict.md: final LF -> space, bytes 41128 -> 41128, changed_bytes=1. LỆNH: `python3 evidence/run_mutations.py`; thao tác dữ liệu được ghi nguyên trong script.

### Đo cổng — mutant-byte

Cây đo: `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056/review-copy`. `PYTHONDONTWRITEBYTECODE=1`; không ghi bytecode vào cây review. LỆNH và OUTPUT THẬT (rc lấy trực tiếp subprocess):

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ]
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ]
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ]
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 1,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "  ĐỎ  t26_moi_bien_nhan_review_phai_khop_BAM_tep_no_tro_toi: pr1050-review-1-codex-verdict.receipt.yaml: LỆCH BĂM — biên nhận khai a26aab3018f613c785a1abc3c5e3291d25427be1d872cad0c29bc19c7fc81a35, tệp 'ops/reviews/pr1050-review-1-codex-verdict.md' thực c84d14c0250b1d8c468893af8ffef12e816a64ec23a7eb8c45f044cca552cead. Tệp verdict là NGUYÊN VĂN của reviewer: hoặc bạn vừa sửa nhầm nó, hoặc biên nhận chưa cập nhật. Đừng ghi đè băm cho hết đỏ trước khi biết là ca nào.",
      "lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0"
    ]
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  }
}
```
Log đầy đủ: `evidence/mutant-byte-*.log`, mã thoát: `evidence/mutant-byte-*.rc`.
Kết luận phản chứng: cổng ĐỎ=['t26']; cổng KHÔNG CÓ RĂNG với đúng đột biến này=['bien_nhan_v2', 'land_evidence_nguon', 'doctrine_scan', 't27', 't138']. Đã phục hồi byte nguyên bản trước hướng tiếp theo.

ĐỘT BIẾN `toc` (chỉ trên clone từ mirror.git tại exact SHA): ops/reviews/README.md: removed toc row, removed_bytes=446. LỆNH: `python3 evidence/run_mutations.py`; thao tác dữ liệu được ghi nguyên trong script.

### Hướng 4 — README mục lục và sáu cảnh báo

LỆNH: `python3 evidence/measure_readme.py` (trích các hàng mới từ diff exact SHA, đếm độc lập và đối chiếu receipt/run/bytes).

OUTPUT THẬT:
```text
ADDED_ROWS 8 UNIQUE_ROWS 8
ROUND 1 TOC_ROWS 1 CAVEAT_ROWS 3 CHECKS {'verdict': True, 'assurance': True, 'counts': True, 'run_id': True, 'head': True, 'bytes': True, 'model': True, 'receipt_link': True}
CAVEAT CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY rows 1 text_equal True
CAVEAT SCRIPT-DO-DOC-DUONG-DAN-SANDBOX rows 1 text_equal True
CAVEAT TEP-LON-KHONG-VAO-KHO rows 1 text_equal True
ALL_LINKS_EXIST True
ROUND 2 TOC_ROWS 1 CAVEAT_ROWS 3 CHECKS {'verdict': True, 'assurance': True, 'counts': True, 'run_id': True, 'head': True, 'bytes': True, 'model': True, 'receipt_link': True}
CAVEAT CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY rows 1 text_equal True
CAVEAT SCRIPT-DO-DOC-DUONG-DAN-SANDBOX rows 1 text_equal True
CAVEAT TEP-LON-KHONG-VAO-KHO rows 1 text_equal True
ALL_LINKS_EXIST True
```
Kết luận: KHÔNG PHẢI LỖI. Đúng 8 hàng mới/8 hàng duy nhất; mỗi verdict có một hàng mục lục và ba hàng cảnh báo. Các đường dẫn tồn tại, metadata và mô tả caveat bằng receipt; head f37b519 bằng cha thứ hai của merge #1050.

### Đo cổng — mutant-toc

Cây đo: `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056/review-copy`. `PYTHONDONTWRITEBYTECODE=1`; không ghi bytecode vào cây review. LỆNH và OUTPUT THẬT (rc lấy trực tiếp subprocess):

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ]
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ]
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ]
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 1,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: verdict 'pr1050-review-1-codex-verdict.md' KHÔNG có trong CỘT 'tệp verdict' của bảng 'Mục lục'. Nằm ở đoạn giải thích, trong comment HTML, hay ở một cột mô tả nào đó thì bảng render ra vẫn thiếu nó.",
      "lease_publish: 1/2 đạt; đã chạy=2, bỏ qua=0"
    ]
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  }
}
```
Log đầy đủ: `evidence/mutant-toc-*.log`, mã thoát: `evidence/mutant-toc-*.rc`.
Kết luận phản chứng: cổng ĐỎ=['t27']; cổng KHÔNG CÓ RĂNG với đúng đột biến này=['bien_nhan_v2', 'land_evidence_nguon', 'doctrine_scan', 't26', 't138']. Đã phục hồi byte nguyên bản trước hướng tiếp theo.

ĐỘT BIẾN `caveat` (chỉ trên clone từ mirror.git tại exact SHA): ops/reviews/README.md: removed caveat row, removed_bytes=164. LỆNH: `python3 evidence/run_mutations.py`; thao tác dữ liệu được ghi nguyên trong script.

### Đo cổng — mutant-caveat

Cây đo: `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056/review-copy`. `PYTHONDONTWRITEBYTECODE=1`; không ghi bytecode vào cây review. LỆNH và OUTPUT THẬT (rc lấy trực tiếp subprocess):

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ]
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ]
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ]
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 1,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "  ĐỎ  t27_canh_bao_trong_bien_nhan_phai_duoc_NANG_len_muc_luc: README.md: caveat 'TEP-LON-KHONG-VAO-KHO' của pr1050-review-1-codex-verdict.receipt.yaml KHÔNG nằm ở CỘT 'id' trên cùng hàng với 'pr1050-review-1-codex-verdict.md' ở CỘT 'tệp verdict', trong bảng 'Cảnh báo đang có hiệu lực'. Bị nhắc trong phần mô tả của hàng khác KHÔNG tính — verdict này vẫn phải có hàng cảnh báo của riêng nó.",
      "lease_publish: 1/2 đạt; đã chạy=2, bỏ qua=0"
    ]
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  }
}
```
Log đầy đủ: `evidence/mutant-caveat-*.log`, mã thoát: `evidence/mutant-caveat-*.rc`.
Kết luận phản chứng: cổng ĐỎ=['t27']; cổng KHÔNG CÓ RĂNG với đúng đột biến này=['bien_nhan_v2', 'land_evidence_nguon', 'doctrine_scan', 't26', 't138']. Đã phục hồi byte nguyên bản trước hướng tiếp theo.

ĐỘT BIẾN `count` (chỉ trên clone từ mirror.git tại exact SHA): ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml: so_p1 1 -> 9 (1 byte). LỆNH: `python3 evidence/run_mutations.py`; thao tác dữ liệu được ghi nguyên trong script.

### Hướng 5 — Review Class và lý do phân lớp

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_class.py`; đọc protocol §8, ADR-0038 và `ops/KE_HOACH_THI_CONG_DA_PROVIDER.md` §4 tại exact HEAD.

OUTPUT THẬT:
```text
CLASS_ORDER {'routine': 0, 'systemic': 1, 'sensitive': 2}
ROUND 1 paths 32 declared standard enum_valid False classifier_actual_diff sensitive effective_review_class ABSENT
ROUND 2 paths 33 declared standard enum_valid False classifier_actual_diff sensitive effective_review_class ABSENT
IMPORTANT: classifier is a lease classifier; called here as a measurement of existing fail-closed path rules, not as proof that receipt schema validates review_class.
```
Kết luận: LỖI. Hai trường `standard` ngoài từ vựng chính tắc; câu lý do “không có lease / chỉ dữ liệu” không cấp một class mới hoặc một override có audit. Classifier của lease được dùng ở đây để đối chiếu luật fail-closed sẵn có, không coi nó là validator schema receipt. Không gán toàn bộ dữ liệu ghi sổ thành thay đổi mã; lỗi nằm ở khai class không tồn tại và thiếu phân lớp hiệu lực theo protocol.

### review-class-standard-ngoai-tu-vung  [P1]  Hai biên nhận mới khai một Review Class không tồn tại

TỆP/DÒNG: `ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml:21–22`; `ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml:21–22`.

VẤN ĐỀ: Cả hai khai `review_class: standard`. Protocol §8 và kế hoạch đa-provider §4 chỉ định ba giá trị `routine`, `systemic`, `sensitive`; thiếu/không rõ phải xử lý như `sensitive`, không có `standard`. Lý do kèm theo chỉ nói không có lease và diff là dữ liệu; không xác định class hợp lệ, không có quyết định override có audit. Đây là phân loại sai đo được tại SHA đang review, không phải nghi vấn về model. Sáu cổng baseline vẫn xanh nên không thể viện chúng làm bằng chứng class đúng. Tại cổng phân lớp hiện có, cả 32 và 33 đường dẫn của hai head được trả `sensitive` theo nhánh fail-closed cho đường chưa biết. Kết quả đó là giới hạn bảo thủ của classifier, không tự chứng minh dữ liệu này đổi authority; muốn hạ xuống một class khác cần lý do/override đúng protocol, không tự sáng tác `standard`.

ĐÃ THỬ NGHIỆM: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_class.py` → hai lần `enum_valid False`, `classifier_actual_diff sensitive`, `effective_review_class ABSENT`. `python3 ops/bien_nhan_v2.py --root .` → `257 ĐẠT v2`, `0 vi phạm`, `TỔNG: ĐẠT`; các cổng còn lại baseline cũng đạt. Mã và output đo được lưu ở `evidence/measure_class.py`, `evidence/classification-summary.log`, `evidence/baseline-gates.json`.

ĐỘ TIN: cao.

Gợi ý: phân lớp theo từ vựng thật; khi chưa có override có audit, ghi `sensitive` theo fail-closed cùng lý do và giá trị hiệu lực. Giữ nguyên verdict/hash/số finding/assurance lịch sử; không sửa bytes của hiện vật reviewer.

### Hướng 6 — rò bí mật và đường dẫn credential

LỆNH: `python3 cay-kho/scripts/pkg_secret_scan.py cay-kho/ops/reviews/pr1050-review-{1,2}-codex` (từng thư mục); `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_secrets.py` (dùng hai bảng mẫu sẵn có `secret_guard`/`pkg_secret_scan`, bổ sung dò credential path, literal secret và GitHub fine-grained token; chỉ in loại/tệp/dòng, không in giá trị).

OUTPUT THẬT:
```text
secret-round1 rc=0; stdout rỗng
secret-round2 rc=0; stdout rỗng
SCANNED_CHANGED_FILES 180 SKIPPED_NON_UTF8 [] patterns 20
SECRET_PATTERN_HITS 0

CREDENTIAL_PATH_HITS 0

ROUND 1 files 93 pkg_scannable 93 max_file_bytes 41128 pkg_hits []
ROUND 2 files 82 pkg_scannable 82 max_file_bytes 41128 pkg_hits []
```
Kết luận: KHÔNG PHẢI LỖI trong phạm vi quét: không có pattern bí mật hay credential path; 180 tệp thay đổi đều UTF-8, không bỏ tệp nhị phân. Các đường dẫn sandbox `/tmp/...`, run/response/session IDs và băm hiện vật không phải credential. Đây là phép dò mẫu và rà nội dung hiện vật, không chứng minh tuyệt đối mọi chuỗi tự do đều không bí mật. Không đọc credential thật hoặc dump môi trường.

Bổ sung Hướng 3: `rg -n origin/master .../pr1050-review-1-codex/evidence/final-integrity.log` có output `16:origin/master b29da0bfe3bfb7a7be69136a1c5c40f82c088a93`. Snapshot cũ này củng cố base đã khai, nhưng vẫn là bằng chứng đã lưu của reviewer cũ, không là ref readback trực tiếp lúc dựng sandbox của tôi.

### Đo cổng — mutant-count

Cây đo: `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056/review-copy`. `PYTHONDONTWRITEBYTECODE=1`; không ghi bytecode vào cây review. LỆNH và OUTPUT THẬT (rc lấy trực tiếp subprocess):

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ]
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ]
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ]
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0"
    ]
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "  KHÔNG neo đầu dòng là `lease_publish: (\\d+)/(\\d+) đạt`, và nó đọc BẢN RIÊNG trong tệp chứ",
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ]
  }
}
```
Log đầy đủ: `evidence/mutant-count-*.log`, mã thoát: `evidence/mutant-count-*.rc`.
Kết luận phản chứng: cổng ĐỎ=[]; cổng KHÔNG CÓ RĂNG với đúng đột biến này=['bien_nhan_v2', 'land_evidence_nguon', 'doctrine_scan', 't26', 't27', 't138']. Đã phục hồi byte nguyên bản trước hướng tiếp theo.

### Hướng 7 — từng trường biên nhận, model/identity, giới hạn chứng cứ

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_receipts.py`.

OUTPUT THẬT:
```text
ROUND 1 TOP_LEVEL_FIELDS 48 SCHEMA_GATE_ERRORS []
KIND 2 review_delivery_receipt PACKET KHONG_AP_DUNG TARGET_PR 1050 ROLE reviewer ROUND 1
RECEIPT_ID_SUFFIX_MATCH True
COUNTS_FROM_FINDING_HEADINGS [0, 1, 1, 0] COUNTS_MATCH True FINDING_IDS [('nha-lease-truoc-khi-het-han', '1'), ('nguyen-nhan-windows-khai-do-thieu-log', '2')] IDS_MATCH True
VERDICT_MATCH True HEAD_MATCH True
HASH_MATCH True BYTES_MATCH True
MODEL_IDENTITY_MATCH {'provider': True, 'surface': True, 'transport': True, 'session_run_id': True}
MODEL gpt-6.1-sol gpt-6.1-sol SERVED_MODELS ['gpt-6.1-sol'] EVENTS 30 EVIDENCE do_may do_may
MODEL_EVIDENCE_REF_VALID True
CANONICAL_FAMILIES_REVIEWER ('gpt', 'do_may', True) EXECUTOR ('claude', '', False) ASSURANCE cross_reviewed
CHECKPOINT_FIELDS_MATCH True CHECKPOINT_HASH_MATCH True
DURATION_DELTA_SECONDS 0.000189 ACTUAL_RC 0 STATUS xong CLEAN_AT_LAUNCH True
SANDBOX DO_DUOC OBSERVED_PROFILES ['null', '{"file_system": "restricted", "loai": "managed", "muc": [["root", "read"], ["to_tien_workspace", "write"], ["slash_tmp", "write"], ["tmpdir", "write"], ["khac", "read"], ["khac", "read"], ["khac", "read"], ["khac", "read"]], "network": "restricted"}']
CLI_VERSION_FIELDS [] RAW_ARGV_PRESENT False
VERSION_IN_STDOUT_STDERR False
AUTHORSHIP_SESSION_AND_HUMAN_ACTOR_NOT_IN_RUN_JSON True
USAGE_CAVEATS ['CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY', 'SCRIPT-DO-DOC-DUONG-DAN-SANDBOX', 'TEP-LON-KHONG-VAO-KHO']
ANCHOR {'loai': 'canonical_ancestry', 'cuong_do': 'thap', 'mo_ta': '(a) Blob verdict ghim o commit hien vat 7333f97 cua PR ghi so; len trung_binh khi PR ghi so land bang merge commit.'} INDEPENDENCE_DECLARED True AXES ['spec', 'standards_security']
ROUND 2 TOP_LEVEL_FIELDS 48 SCHEMA_GATE_ERRORS []
KIND 2 review_delivery_receipt PACKET KHONG_AP_DUNG TARGET_PR 1050 ROLE reviewer ROUND 2
RECEIPT_ID_SUFFIX_MATCH True
COUNTS_FROM_FINDING_HEADINGS [0, 0, 0, 0] COUNTS_MATCH True FINDING_IDS [] IDS_MATCH True
VERDICT_MATCH True HEAD_MATCH True
HASH_MATCH True BYTES_MATCH True
MODEL_IDENTITY_MATCH {'provider': True, 'surface': True, 'transport': True, 'session_run_id': True}
MODEL gpt-6.1-sol gpt-6.1-sol SERVED_MODELS ['gpt-6.1-sol'] EVENTS 25 EVIDENCE do_may do_may
MODEL_EVIDENCE_REF_VALID True
CANONICAL_FAMILIES_REVIEWER ('gpt', 'do_may', True) EXECUTOR ('claude', '', False) ASSURANCE cross_approved
CHECKPOINT_FIELDS_MATCH True CHECKPOINT_HASH_MATCH True
DURATION_DELTA_SECONDS 0.000262 ACTUAL_RC 0 STATUS xong CLEAN_AT_LAUNCH True
SANDBOX DO_DUOC OBSERVED_PROFILES ['null', '{"file_system": "restricted", "loai": "managed", "muc": [["root", "read"], ["to_tien_workspace", "write"], ["slash_tmp", "write"], ["tmpdir", "write"], ["khac", "read"], ["khac", "read"], ["khac", "read"], ["khac", "read"]], "network": "restricted"}']
CLI_VERSION_FIELDS [] RAW_ARGV_PRESENT False
VERSION_IN_STDOUT_STDERR False
AUTHORSHIP_SESSION_AND_HUMAN_ACTOR_NOT_IN_RUN_JSON True
USAGE_CAVEATS ['CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY', 'SCRIPT-DO-DOC-DUONG-DAN-SANDBOX', 'TEP-LON-KHONG-VAO-KHO']
ANCHOR {'loai': 'canonical_ancestry', 'cuong_do': 'thap', 'mo_ta': '(a) Blob verdict ghim o commit hien vat 7333f97 cua PR ghi so; len trung_binh khi PR ghi so land bang merge commit.'} INDEPENDENCE_DECLARED True AXES ['spec', 'standards_security']
```
Kết luận: KHÔNG PHẢI LỖI về verdict/count/finding IDs/hash/bytes, identity lưu trong run, model phục vụ/effort/checkpoint/timing. Schema gate chấp nhận cả hai nhưng không kiểm review_class như Hướng 5. Assurance lượt 1 chỉ cross_reviewed; lượt 2 approve, khác họ GPT/Claude theo nguồn đã khai. Không thấy bằng chứng bác sự độc lập; hai run/prompt riêng không tự chứng minh toàn bộ ngữ cảnh hay người dùng credential. CLI version 0.164.0, nguyên argv, người thật/phiên vận chuyển và chỉ thị chủ kho KHÔNG ĐO ĐƯỢC độc lập từ hiện vật: run chỉ lưu chương trình/số đối số/fingerprint, không phiên bản. Phần kể về packet/actor được gắn (b), không coi thiếu chứng cứ độc lập là bằng chứng câu ấy sai. Executor family dùng mặc định Claude trong gate; không gọi đó là phép đo runtime executor. Snapshot worktree_sach chỉ nói lúc phóng, đúng như caveat; không được suy luôn cưỡng chế read-only.

### Hướng 8 — kiểm lại lời khai đóng hai finding #1050

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_closure.py` (git show exact c24875d/f37b519/a34b9a3, gọi hàm phân loại lease sẵn có với giờ đóng băng, đối chiếu log và job JSON được giữ).

OUTPUT THẬT:
```text
EXACT_OLD_NEW_LAND_MATCH_CURRENT_SNAPSHOTS True
LEASE_SNAPSHOT_EQUAL_GIT_OBJECT True
CLASSIFY 2026-10-30T17:37:00Z CÒN_HẠN
CLASSIFY 2026-10-30T17:53:00Z HẾT_HẠN
CLASSIFY 2026-10-30T18:07:34Z HẾT_HẠN
POST_EXPIRY_LOG_HASH cbc0c4a31a8df98e835ea232a96b4339cf763b3c7d302a087f7de4c23c1ba765 IN_MANIFEST True NEW_SOURCE_BLOCK True
NEW_LOG_MARKERS ['# do 2026-10-30T18:07:34Z trong phien session_015GtxrYjGJtmjF3eT1nCSG9 (sau han moi 17:53Z cua wp1037-r1-g1-claude)', 'HẾT_HẠN\twp1037-r1-g1-claude\trefs/heads/ops/wp1037-r1-g1-lease:ops/leases/wp1037-r1-g1-claude.yaml', 'NGƯỜI_GIỮ 1: wp1021-r2-g1-claude', 'rc=11']
LEASE_OLD_CLAIM DA NHA bang RUT HAN (khong bia mo — lease con han, khong co lease
LEASE_NEW_HISTORICAL_CLAIM DA RUT HAN; CHUA NHA tai moc ghi so 17:37Z (khong bia mo — lease con han, khong co lease ke nhiem): 
WINDOWS_NEW_NAME ci.yml workflow_dispatch (nhan windows-latest do tu jobs) tren head cuoi
WINDOWS_ATTEMPT 1 total 16 array 16 conclusions {'success': 13, 'failure': 2, 'skipped': 1} windows_jobs 14
WINDOWS_ATTEMPT 2 total 16 array 16 conclusions {'success': 15, 'skipped': 1} windows_jobs 14
CAUSE_IS_IN_THUAT_LAI_SEGMENT True
THREE_FILES_CHANGED 10	4	ops/land/pr1041-wp1037-land-evidence.yaml
1	0	ops/land/pr1041-wp1037-provenance/SHA256SUMS
28	0	ops/land/pr1041-wp1037-provenance/ai-dang-giu-sau-rut-han/luc-do.txt
LANDED_STAYS_FALSE True
NO_REMOTE_REF_READBACK: server 708/708 summary not independently reproducible offline; no network used.
```
Kết luận: KHÔNG PHẢI LỖI về lời khai hai finding đã vá. Câu trạng thái lease sai được đổi thành CHƯA NHẢ tại snapshot 17:37Z, có nguồn riêng cho phép đo sau hạn. Nguyên nhân/input Windows tách thành thuật lại/KHÔNG ĐO ĐƯỢC. Bản vá f37b519 không byte-identical với HINT vì thêm khối đo mới và provenance; receipt chỉ nói “theo nghĩa HINT”, phù hợp. Tác giả là session_015… chỉ là lời khai có neo trong recorded_by của hồ sơ, không có runtime executor để chứng minh độc lập. Verdict/PROMPT cũ ghi CHƯA merge được đọc như snapshot ở head lịch sử, không như trạng thái #1050 tại 1aae17b. Không gọi ls-remote hay API; số ref server tại 18:07:34Z không đo lại được offline.

### Hướng 9 — tổng hợp phản chứng và giới hạn của cổng

LỆNH: `git clone --no-hardlinks --no-checkout mirror.git review-copy`; `git -C review-copy checkout --detach 1aae17b5534f78767856f93f7d6089adda224f21`; `git -C review-copy config core.abbrev 7`; `python3 evidence/run_mutations.py`. Mã đột biến chỉ sửa dữ liệu trên clone rồi phục hồi nguyên byte; các cổng chạy bằng cùng sáu lệnh baseline.

OUTPUT THẬT (tóm tắt từ `evidence/mutations-summary.json`; log/rc từng lệnh đã nối phía trên):

| đột biến riêng lẻ | bien_nhan_v2 | land_evidence_nguon | doctrine-scan | t26 | t27 | t138 |
|---|---:|---:|---:|---:|---:|---:|
| cuối verdict phẳng LF → space, đúng 1 byte, giữ 41128B | 0 | 0 | 0 | **1 (0/1)** | 0 (2/2) | 0 (1/1) |
| xoá đúng hàng TOC mới lượt 1 (446B) | 0 | 0 | 0 | 0 (1/1) | **1 (1/2)** | 0 (1/1) |
| xoá đúng hàng caveat mới TEP-LON lượt 1 (164B) | 0 | 0 | 0 | 0 (1/1) | **1 (1/2)** | 0 (1/1) |
| receipt so_p1 1 → 9, đúng 1 byte | 0 | 0 | 0 | 0 (1/1) | 0 (2/2) | 0 (1/1) |

Kết luận: KHÔNG PHẢI LỖI mới của dữ liệu gốc ở các hướng này. Chốt băm t26 và chốt nâng cảnh báo/mục lục t27 có răng với đúng lỗi được thử. Những cổng còn xanh KHÔNG CÓ RĂNG đối với đúng đột biến tương ứng; toàn bộ sáu cổng không canh so_p1 theo verdict. Đây là giới hạn đã đo, không suy mọi nội dung receipt đều được chứng minh bởi `TỔNG: ĐẠT`. `t138` kiểm receipt thu hồi trong fixture riêng, không phải bộ đọc hai review receipt này. Không có ca nào báo lỗi `Codex home is inside a repository`; không ca nào phải đánh dấu KHÔNG ĐO ĐƯỢC vì tạo tác đó.

### Hướng 10 — patch-as-hint và kiểm tra cuối

`HINT.patch` chỉ đề xuất thay class/ghi chú và thêm effective class ở hai receipt; không sửa hiện vật verdict. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

LỆNH: `python3 evidence/make_hint.py`; `patch --dry-run --fuzz=0 -p0 -d review-copy -i ../HINT.patch`. Bản sao đang ở exact SHA đang review.

OUTPUT THẬT:
```text
checking file ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml
checking file ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml
dry-run rc=0
```

Sau dry-run, áp thật CHỈ TRÊN CLONE để xác minh YAML và bộ kiểm biên nhận, rồi phục hồi hai tệp từ bytes gốc. Output `evidence/hint-validation.log`:
```text
$ patch --fuzz=0 -p0 -i ../HINT.patch
rc=0
patching file ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml

ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml changed_keys=['effective_review_class', 'review_class', 'review_class_ghi_chu']

ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml changed_keys=['effective_review_class', 'review_class', 'review_class_ghi_chu']

$ PYTHONDONTWRITEBYTECODE=1 python3 ops/bien_nhan_v2.py --root .
rc=0

bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310
câu lịch sử: nợ L-REVIEW 1 · L-ANCESTRY 60 · L-SURFACE 0 · L-SURFACE chua_do_duoc 0
TỔNG: ĐẠT
```

Kết luận: KHÔNG PHẢI LỖI trong bản gợi ý đã đo; dry-run sạch với fuzz=0, YAML parse được, chỉ ba khóa metadata thay đổi ở mỗi receipt, validator vẫn TỔNG ĐẠT. Validator không tự chứng minh class, nên phần class được đối chiếu với protocol và classifier riêng ở Hướng 5.

Kiểm cuối — lệnh và output thật trong `evidence/final-integrity.log`:
```text
cay-kho git rev-parse HEAD HEAD^{tree} rc 0 output 1aae17b5534f78767856f93f7d6089adda224f21
2d0cdcab508a07dd124356fd69635c36efa1d766 stderr (empty)
cay-kho git status --short --untracked-files=all --ignored=matching rc 0 output (empty) stderr (empty)
cay-kho git diff --exit-code rc 0 output (empty) stderr (empty)
cay-kho git diff --cached --exit-code rc 0 output (empty) stderr (empty)
cay-kho git diff --check rc 0 output (empty) stderr (empty)
cay-kho git config core.abbrev rc 0 output 7 stderr (empty)
cay-kho ALL_CHANGED_FILES_EQUAL_EXACT_HEAD 180 / 180
review-copy git rev-parse HEAD HEAD^{tree} rc 0 output 1aae17b5534f78767856f93f7d6089adda224f21
2d0cdcab508a07dd124356fd69635c36efa1d766 stderr (empty)
review-copy git status --short --untracked-files=all --ignored=matching rc 0 output (empty) stderr (empty)
review-copy git diff --exit-code rc 0 output (empty) stderr (empty)
review-copy git diff --cached --exit-code rc 0 output (empty) stderr (empty)
review-copy git diff --check rc 0 output (empty) stderr (empty)
review-copy git config core.abbrev rc 0 output 7 stderr (empty)
review-copy ALL_CHANGED_FILES_EQUAL_EXACT_HEAD 180 / 180
7333f97_is_ancestor_of_frozen_master rc 1
```

Một finding theo lớp, hai thể hiện tại hai receipt: **0 P0, 1 P1, 0 P2, 0 P3**. `changes_requested` vì class `standard` sai từ vựng/protocol tại exact reviewed SHA. Sáu cổng baseline xanh không xoá finding ấy. Cây gốc và clone cuối cùng đều sạch, 180/180 tệp thuộc PR bằng blob exact HEAD; không push, không gọi mạng. Hạn chế độc lập về CLI version/argv, tác giả phiên, người dùng credential và ref server lịch sử đã ghi đúng là KHÔNG ĐO ĐƯỢC, không được nâng thành phép đo hoặc tự biến thành cáo buộc sai sự thật.
