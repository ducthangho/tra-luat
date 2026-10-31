verdict: approve
reviewed_sha: 047eaa4d26a5bb1e702199c870f42480aebed673
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

## BẢNG ĐO

| khẳng định | bên giao khai | đo được (lệnh) | khớp? |
|---|---|---|---|
| Exact SHA/tree/phạm vi #1056 | 047eaa4; chỉ ops/reviews | Git preflight/final: `047eaa4d26a5bb1e702199c870f42480aebed673`, tree `ac826681109d74ad18efc3120c79b65ddb8280a2`; 180 tệp/+6716/−0; ngoài ops/reviews=[] | có |
| Finding lượt 1 | vá class standard | `measure_closure.py`: classifier 32/33 path → sensitive; cả hai receipt sensitive/effective sensitive | **ĐÓNG** |
| Lời khai áp nguyên HINT, không sửa khác | patch -p0 --fuzz=0 trên 1aae17b | dry-run/áp rc0; sau áp `git diff --exit-code 047eaa4 --` rc0 toàn cây; diff cung cấp 2202B bằng Git | có |
| SHA256SUMS | bao phủ toàn gói | `measure_artifacts.py`: 92/92 và 81/81; missing/extra/bad_hash=[]; duplicate=0; trừ chính manifest | có |
| Verdict phẳng/nguyên bản | từng byte không đổi | `measure_artifacts.py`: flat_equal True cả hai; 41128B/a26aab30… và 37384B/109dcb6a… | có |
| run.head/prompt_sha256/checkpoint | c24875d, f37b519; prompt đúng run | run.head=receipt=dòng 2; SHA256 prompt 9705d198…/23a3a3f8… bằng run/checkpoint; checkpoint hash khớp | có |
| run.rc/status/clean/time/stdout/stderr | 0/xong/true; 790.067s/606.043s | `measure_artifacts.py`/`measure_receipts.py`: đúng; stdout 379/401B, stderr 39/39B và hashes khớp; chênh thời lượng làm tròn <0.0003s | có; clean tại lúc phóng |
| OMITTED diff | 520915B/0aba68a3…; 525788B/1d9762a7… | `git diff b29da0b <head>` tái lập đúng bytes và SHA256 đầy đủ (Hướng 2) | có |
| OMITTED repo copies | không chép repo/mirror lớn | Git ls-tree gói không có cay-kho/review-copy/mirror.git; dòng omission chỉ khai băm cho diff | có |
| verdict-cu/diff riêng lượt 2 | bản verdict/HINT lượt 1 và phần vá #1050 | so byte True; diff-tu-luot1 bằng `git diff c24875d f37b519`, 11192B | có |
| schema_version/kind/role/review_axes | 2/review_delivery_receipt/reviewer/spec,standards_security | `measure_receipts.py` static fields True; validator v2 ĐẠT; nội dung verdict có phép đo spec/quy trình/an toàn | có |
| receipt_id/luot | a26aab30,109dcb6a; lượt 1,2 | hậu tố bằng băm verdict; static fields True cả hai | có |
| packet_id/packet_ghi_chu/target_pull_request | KHONG_AP_DUNG, không Issue/lease riêng; chủ kho giao trực tiếp; #1050 | nội dung Git/PROMPT đúng target; chỉ thị chat và không có lease ở mọi nơi chỉ `(b)` thuật lại | có về target; phần (b) không đo độc lập |
| land_merge_commit/ghi_chu | 79400f3 merge #1050, cha 2 f37b519 | `git show -s --format=%H,%P,%cI,%s 79400f3` khớp; người/phiên bấm merge không chứng minh bằng Git | Git có; phiên thuật lại |
| provider/executor_provider/cross_provider | codex/claude/true | MRI/run OpenAI; executor Claude theo nhiệm vụ và hồ sơ #1050; khác họ theo protocol | phù hợp nguồn; không có runtime executor |
| review_class/effective_review_class/ghi_chu | sensitive; fail-closed trên 32/33 path chưa phân loại; không override | hàm sẵn có `_tinh_lop_tu_write_set` trên diff đúng head trả sensitive; protocol §8 thiếu/không rõ → sensitive; kiểm path ngoài phạm vi=[] | có; không tự coi là đánh giá hết rủi ro |
| assurance/assurance_ghi_chu | cross_reviewed ở changes_requested; cross_approved ở approve | `measure_receipts.py`: cả hai MATCH True; model đo được, verdict/counts đúng; review độc lập theo nguồn được giữ | có trong giới hạn nguồn; không cấp quyền merge |
| verdict/verdict_nguon | changes_requested; approve | bằng dòng 1 hai verdict | có |
| verdict_path/verdict_sha256/verdict_bytes | đường dẫn phẳng; a26aab30…/41128;109dcb6a…/37384 | file tồn tại, băm/byte khớp Hướng 2 | có |
| nguon_tep/verdict_ban_goc | bản sao nguyên byte của VERDICT trong gói, copy từ sandbox | byte bằng nhau và bằng blob 7333f97; lịch sử công cụ copy thực là cp không chứng minh riêng | có về byte; provenance theo nguồn đã giữ |
| reviewed_sha/reviewed_tree/reviewed_sha_nguon | c24875d/9382f751…; f37b519/23544465…; launcher expected-head/require-clean | `git rev-parse X^{tree}` đúng; header/run.head đúng. Raw flags không được lưu | có về SHA/tree; flags không đo độc lập |
| base_sha/base_sha_ghi_chu | b29da0b lúc dựng sandbox | merge-base với master ngay trước merge #1050 đều b29da0b; chronology và origin/master snapshot phù hợp | phù hợp lịch sử; không readback ref đúng thời điểm |
| evidence_url/evidence_url_ghi_chu | blob 7333f97 trước commit receipt | `git show 7333f97:<path>` byte bằng verdict; 7333f97 tổ tiên 047eaa4; receipt ở commit sau | có; không GET mạng |
| so_p0..p3/so_dem_theo/so_dem_nguon | theo finding; 0/1/1/0 và 0/0/0/0 | dòng 3, heading finding/IDs đối chiếu độc lập đúng cả hai | có; sáu cổng không canh so_p1 |
| findings_ids/ket_luan | 2 slug lượt 1; [] lượt 2, hai finding đóng | `measure_receipts.py`: heading/IDs đúng; `measure_parent_closure.py` đo lease, nguồn Windows và diff | có |
| xu_ly_finding | f37b519 vá theo nghĩa HINT; lượt 2 xác nhận | ba tệp sửa đúng lease/nhãn Windows và thêm log sau hạn; không khai byte-identical HINT #1050 | có về thay đổi; tác giả phiên theo hồ sơ |
| MRI provider/surface/transport/session_run_id/run_json | openai_codex/codex_cli/machine; run 1b0ff763…/8c095c6b… | bốn trường MRI bằng run, đường dẫn đúng; hai run riêng | có theo metadata đã giữ |
| MRI run_json_ghi_chu | rc/status/clean/time/head/prompt | Hướng 2/3 khớp từng giá trị, thời lượng chỉ làm tròn | có; snapshot clean không chứng minh cả lịch sử |
| MRI cli/model_yeu_cau | codex-cli 0.164.0; các cờ; requested KHONG_DO_DUOC | run chỉ giữ chương trình codex/argc9/fingerprint, không raw argv/version. Served model không chứng minh requested/default account | KHÔNG ĐO ĐƯỢC độc lập version/cờ; không có chứng cứ ngược |
| MRI model/model_da_chay/model_evidence/muc_bang_chung_model | gpt-6.1-sol/do_may | run DO_DUOC: 30/30 và 25/25 event gpt-6.1-sol; effort DO_DUOC=[xhigh] | có trong telemetry được giữ |
| MRI model_evidence_ref/model_evidence_ghi_chu | #model_phuc_vu; 30/25 event, xhigh | ref có, count/model/effort đúng Hướng 2/3 | có |
| github_submitter_identity.actor/actor_nguon/ghi_chu | ducthangho, chưa đăng bản chiếu; credential phiên; chỉ vận chuyển | tự gắn (b); không có readback bản chiếu hay runtime xác minh người dùng credential | không đo độc lập người thật; không đánh tráo reviewer |
| independent_from_executor_session/independent_ghi_chu | true; Codex process/context riêng; điều phối khác executor | run IDs riêng, prompt tự chứa; session executor/điều phối theo hồ sơ; không giữ toàn bộ transcript executor | không thấy chứng cứ ngược; không chứng nhận toàn bộ context |
| anchor.loai/cuong_do/mo_ta | canonical_ancestry/thap; lên trung_binh khi land merge | 7333f97 tổ tiên 047eaa4 rc0, chưa tổ tiên base master6db9341 rc1 | có tại SHA đang review |
| CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY | workspace-write chứa cây review, sạch khi phóng | run.sandbox_quan_sat có ancestor workspace write; giới hạn /proc 0.2s; worktree_sach true | có; prompt không thay cơ chế sandbox |
| SCRIPT-DO-DOC-DUONG-DAN-SANDBOX | evidence có absolute sandbox paths; cần clone đúng head | script/log giữ /tmp paths và root assumptions; clone đúng SHA là điều kiện tái lập, một số script cần chỉnh root | có; không hứa clone là đủ mọi điều kiện |
| TEP-LON-KHONG-VAO-KHO | diff >500KB, repo copies không vào kho | OMITTED/tập Git khớp Hướng 2; băm chỉ dành diff | có |
| nguon_co_tham_quyen | tệp có băm trong kho | verdict path/hash khớp, nguồn nội dung; ADR-0040/ghi chú không cấp merge authority | có trong nghĩa nguồn nội dung |
| README | 2 TOC +6 cảnh báo mới đúng/tám hàng riêng | `measure_readme.py`: 8/8 unique, mỗi lượt 1 TOC+3 cảnh báo, mọi giá trị/link đúng | có |
| Baseline không phá cổng | sáu lệnh yêu cầu | rc0 tất cả; validator TỔNG ĐẠT; doctrine10/0; t26=1/1,t27=2/2,t138=1/1; skip0 | có |
| Phản chứng cổng | byte verdict/README phải có cổng đỏ | Hướng 8: chỉ t26 đỏ khi đổi byte, chỉ t27 đỏ khi xoá TOC; so_p1 sai sống qua mọi cổng | đã đo; giới hạn ghi rõ |
| Bí mật | hiện vật không rò token/key/credential | `measure_secrets.py`: 180 tệp,21 mẫu,secret0/credential_path0; scanner gói rc0 và phủ93/93,82/82 | không thấy trong phạm vi quét |
| Tính bất biến hiện vật/nguyên cây | chỉ đọc cây gốc, clone phục hồi | `final_integrity.py`: 180/180 blob head khớp cả hai cây; 177/177 tệp từ7333f97 nguyên byte; status gồm ignored/diff/index rỗng | có ở hai mốc; không suy chưa từng ghi rồi hoàn nguyên |

## BẢNG SĂN

### Nhật ký mở đầu

- Đã đọc toàn bộ tệp nhiệm vụ bằng `cat run/6ad116a8/prompt.snapshot` (rc=0).
- Chưa kết luận finding hay xác nhận lời khai của executor.

### Hướng 1 — neo SHA/phạm vi và đóng finding lượt 1

LỆNH: các lệnh Git trong `evidence/preflight.log`; `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_closure.py` (mã đo chỉ gọi Git/patch trên clone và hàm phân lớp sẵn có). OUTPUT THẬT:

```text
$ git rev-parse HEAD HEAD^{tree}
rc=0
047eaa4d26a5bb1e702199c870f42480aebed673
ac826681109d74ad18efc3120c79b65ddb8280a2


$ git status --porcelain=v1 --untracked-files=all --ignored=matching
rc=0
(empty)


$ git rev-parse --is-shallow-repository
rc=0
false


$ git diff --numstat 6db934145acf6e47d01db5b2dc8c9da417c2d8eb HEAD
rc=0
files=180 additions=6716 deletions=0 outside_ops_reviews=[]


$ git show -s --format=%H%n%P%n%cI%n%s 79400f3
rc=0
79400f3cdc6b780319b66f57c27e5772ad010101
4f11b13c3d286a79dbe9a83547a800005cda0eda f37b5195978f1fe35b9cb55b6f79a2e09d165af0
2026-10-31T01:55:24+07:00
Merge pull request #1050 from ducthangho/claude/magical-clarke-gzvwbp


$ git diff --name-only 1aae17b HEAD
rc=0
ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml
ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml

$ git checkout --force --detach 1aae17b5534f78767856f93f7d6089adda224f21 rc 0
(empty)
HEAD is now at 1aae17b ops/reviews: bien nhan v2 + hang muc luc/canh bao README cho 2 luot cross-review PR #1050
$ patch --dry-run --fuzz=0 -p0 -i /tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056-r2/verdict-cu/luot1-HINT.patch rc 0
checking file ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml
checking file ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml

$ patch --fuzz=0 -p0 -i /tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056-r2/verdict-cu/luot1-HINT.patch rc 0
patching file ops/reviews/pr1050-review-1-codex-verdict.receipt.yaml
patching file ops/reviews/pr1050-review-2-codex-verdict.receipt.yaml

$ git diff --exit-code 047eaa4d26a5bb1e702199c870f42480aebed673 -- rc 0
(empty)
$ git checkout --force --detach 047eaa4d26a5bb1e702199c870f42480aebed673 rc 0
(empty)
Previous HEAD position was 1aae17b ops/reviews: bien nhan v2 + hang muc luc/canh bao README cho 2 luot cross-review PR #1050
HEAD is now at 047eaa4 ops/reviews: va cross-review #1056 luot 1 — review_class standard ngoai tu vung -> sensitive
ROUND 1 DIFF_PATH_COUNT 32 OUTSIDE [] CLASSIFIER sensitive DECLARED sensitive EFFECTIVE sensitive
CHANGED_KEYS ['review_class', 'effective_review_class', 'review_class_ghi_chu']
ROUND 2 DIFF_PATH_COUNT 33 OUTSIDE [] CLASSIFIER sensitive DECLARED sensitive EFFECTIVE sensitive
CHANGED_KEYS ['review_class', 'effective_review_class', 'review_class_ghi_chu']
$ git diff --exit-code rc 0
(empty)
```

Kết luận Hướng 1: **KHÔNG PHẢI LỖI; finding `review-class-standard-ngoai-tu-vung` ĐÓNG thật.** Cây đúng `047eaa4…`, tree `ac826681109d74ad18efc3120c79b65ddb8280a2`; sạch gồm ignored; 180 tệp chỉ thuộc ops/reviews. HINT lượt 1 dry-run/áp rc=0 với fuzz=0 trên clone `1aae17b`; cây sau áp bằng toàn bộ `047eaa4` (`git diff --exit-code` rc=0). Hai receipt chỉ thay ba khóa class; classifier sẵn có trong `ops/lease_publish.py` trên đúng 32/33 đường dẫn trả `sensitive`, bằng cả khai báo lẫn effective class. Câu mới giới hạn rõ fail-closed do đường dẫn chưa phân loại, không tự nhận đã đánh giá mọi rủi ro hay có human override; không khai rộng hơn phép đo ở phần vá.

### Đo cổng — baseline

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_gates.py cay-kho baseline`; mỗi subprocess chạy các lệnh sẵn có dưới đây tại `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056-r2/cay-kho`. OUTPUT THẬT:

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ],
    "sandbox_artifact": false
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 0,
    "summary": [
      "lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  }
}
```

Log đầy đủ: `evidence/baseline-*.log`; rc lưu riêng.

### Hướng 2 — toàn vẹn hiện vật độc lập với biên nhận

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_artifacts.py` (băm mọi tệp, so byte, tái lập Git diff/blob tại SHA). OUTPUT THẬT:

```text
ROUND 1 MANIFEST 92 ACTUAL 92 MISSING [] EXTRA [] DUPLICATE 0 BAD_HASH []
FLAT_EQUAL True BYTES 41128 SHA256 a26aab3018f613c785a1abc3c5e3291d25427be1d872cad0c29bc19c7fc81a35 HEADER ['verdict: changes_requested', 'reviewed_sha: c24875d00e93e6a98e0a0abd0837e0cbcad65d4d', 'Kết quả: 0 P0, 1 P1, 1 P2, 0 P3.']
RUN {"run_id": "1b0ff763deb040368dbd0b50bcefbeaa", "head": "c24875d00e93e6a98e0a0abd0837e0cbcad65d4d", "provider": "openai_codex", "execution_surface": "codex_cli", "transport": "machine", "worktree_sach": true, "ma_thoat": 0, "trang_thai": "xong", "bat_dau_utc": "2026-10-30T17:53:06.148692+00:00", "ket_thuc_utc": "2026-10-30T18:06:16.215503+00:00", "thoi_luong_giay": 790.067, "model_phuc_vu_trang_thai": "DO_DUOC", "effort_phuc_vu": ["xhigh"], "effort_phuc_vu_trang_thai": "DO_DUOC"}
PROMPT_HASH 9705d1982dd8680373b8c40348ac61d86fb0802f5fedc08eb341e951cb68878c RUN_MATCH True
MODEL_EVENTS 30 MODELS {'gpt-6.1-sol': 30}
TREE 9382f7512f3adf569f1f82c4d597c66fa1b463d7 TREE_MATCH True
stdout BYTES 379 BYTE_MATCH True HASH_MATCH True
stderr BYTES 39 BYTE_MATCH True HASH_MATCH True
CHECKPOINT {'checkpoint_id': '1b0ff763deb040368dbd0b50bcefbeaa', 'head': 'c24875d00e93e6a98e0a0abd0837e0cbcad65d4d', 'prompt_sha256': '9705d1982dd8680373b8c40348ac61d86fb0802f5fedc08eb341e951cb68878c', 'schema_version': 1} HASH_MATCH True
OMITTED_REGENERATED BYTES 520915 SHA256 0aba68a37e02f9532406b5ae9397271a9614494bcfd84a296a343b35ced43d63 MATCH True
PINNED_BLOB 7333f9712ce0ccbae3a39dfb59484c97e8e03019 ops/reviews/pr1050-review-1-codex-verdict.md EXISTS_EQUAL True
NOT_IN_REPO []
ROUND 2 MANIFEST 81 ACTUAL 81 MISSING [] EXTRA [] DUPLICATE 0 BAD_HASH []
FLAT_EQUAL True BYTES 37384 SHA256 109dcb6aa2325ab048933ab477171ed30a4004b1b335cae515e201efebeb8f11 HEADER ['verdict: approve', 'reviewed_sha: f37b5195978f1fe35b9cb55b6f79a2e09d165af0', 'Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.']
RUN {"run_id": "8c095c6b5f22407a9a443d42a08d7fbc", "head": "f37b5195978f1fe35b9cb55b6f79a2e09d165af0", "provider": "openai_codex", "execution_surface": "codex_cli", "transport": "machine", "worktree_sach": true, "ma_thoat": 0, "trang_thai": "xong", "bat_dau_utc": "2026-10-30T18:09:50.106361+00:00", "ket_thuc_utc": "2026-10-30T18:19:56.149099+00:00", "thoi_luong_giay": 606.043, "model_phuc_vu_trang_thai": "DO_DUOC", "effort_phuc_vu": ["xhigh"], "effort_phuc_vu_trang_thai": "DO_DUOC"}
PROMPT_HASH 23a3a3f8be4b87f91bf897b1656add36826168e7dd9253f8ef516bdeba7fd7a5 RUN_MATCH True
MODEL_EVENTS 25 MODELS {'gpt-6.1-sol': 25}
TREE 235444656cad85bd969f99907b1dbeb4007d961a TREE_MATCH True
stdout BYTES 401 BYTE_MATCH True HASH_MATCH True
stderr BYTES 39 BYTE_MATCH True HASH_MATCH True
CHECKPOINT {'checkpoint_id': '8c095c6b5f22407a9a443d42a08d7fbc', 'head': 'f37b5195978f1fe35b9cb55b6f79a2e09d165af0', 'prompt_sha256': '23a3a3f8be4b87f91bf897b1656add36826168e7dd9253f8ef516bdeba7fd7a5', 'schema_version': 1} HASH_MATCH True
OMITTED_REGENERATED BYTES 525788 SHA256 1d9762a7d9e6ec6f4c724a0c21ba71ac4a816aa76fcb1f23538cab4aa27883db MATCH True
PINNED_BLOB 7333f9712ce0ccbae3a39dfb59484c97e8e03019 ops/reviews/pr1050-review-2-codex-verdict.md EXISTS_EQUAL True
NOT_IN_REPO []
OLD_COPY luot1-VERDICT.md EQUAL True
OLD_COPY luot1-HINT.patch EQUAL True
ROUND2_PATCH_MATCH True BYTES 11192
```

Kết luận: KHÔNG PHẢI LỖI. SHA256SUMS bao phủ đúng 92/92 và 81/81 tệp, trừ chính manifest; không thiếu/thừa/trùng/băm sai. Các verdict phẳng nguyên byte, checkpoint/hash stdout/stderr khớp; OMITTED khớp băm và byte hai diff. `verdict-cu/` và diff riêng lượt 2 đều bằng nguồn lượt 1/Git. Model/effort được xác minh trong telemetry được lưu, không suy từ cấu hình yêu cầu.

### Hướng 3 — từng trường receipt, nội dung verdict và identity

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_receipts.py`. Log đầy đủ `evidence/receipts.log` giữ cả 49 trường/receipt và mọi giá trị. OUTPUT THẬT (rút gọn chỉ bỏ dump giá trị dài, không bỏ kết quả phép so):

```text
STATIC_FIELDS {"schema_version": true, "receipt_id": true, "kind": true, "packet_id": true, "target_pull_request": true, "luot": true, "role": true, "provider": true, "executor_provider": true, "cross_provider": true, "review_class": true, "effective_review_class": true, "independent_from_executor_session": true, "review_axes": true, "so_dem_theo": true, "nguon_tep": true}
VERDICT_MATCH True SHA_MATCH True COUNTS [0, 1, 1, 0] RECEIPT_COUNTS [0, 1, 1, 0] FINDING_HEADINGS ['### nha-lease-truoc-khi-het-han  [P1]  Khai đã nhả lease khi lease vẫn còn hạn tại SHA ghi sổ', '### nguyen-nhan-windows-khai-do-thieu-log  [P2]  Gắn nhãn measured cho nguyên nhân thất bại và cấu hình dispatch không có nguồn tương ứng'] IDS ['nha-lease-truoc-khi-het-han', 'nguyen-nhan-windows-khai-do-thieu-log']
ASSURANCE cross_reviewed MATCH True
MRI_MATCH {'provider': True, 'surface': True, 'transport': True, 'session_run_id': True}
MODEL_MATCH True EVIDENCE do_may do_may REF_MATCH True
CLI_ARGV_OR_VERSION_FIELDS [] LENH {'chuong_trinh': 'codex', 'so_doi_so': 9, 'van_tay': 'fa940ff9899ff12d'}
DURATION 790.066811 DECLARED 790.067 ERROR -0.000189
BASE_MERGE_BASE_PRE_MERGE b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 DECLARED b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
CURRENT_MASTER_MERGE_BASE c24875d00e93e6a98e0a0abd0837e0cbcad65d4d HISTORICAL_HEAD_NOT_SAME_BASE_EXPECTED
ANCESTOR 7333f97 047eaa4 rc 0
ANCESTOR 7333f97 6db9341 rc 1
ANCESTOR c24875d00e93e6a98e0a0abd0837e0cbcad65d4d 79400f3 rc 0
STATIC_FIELDS {"schema_version": true, "receipt_id": true, "kind": true, "packet_id": true, "target_pull_request": true, "luot": true, "role": true, "provider": true, "executor_provider": true, "cross_provider": true, "review_class": true, "effective_review_class": true, "independent_from_executor_session": true, "review_axes": true, "so_dem_theo": true, "nguon_tep": true}
VERDICT_MATCH True SHA_MATCH True COUNTS [0, 0, 0, 0] RECEIPT_COUNTS [0, 0, 0, 0] FINDING_HEADINGS [] IDS []
ASSURANCE cross_approved MATCH True
MRI_MATCH {'provider': True, 'surface': True, 'transport': True, 'session_run_id': True}
MODEL_MATCH True EVIDENCE do_may do_may REF_MATCH True
CLI_ARGV_OR_VERSION_FIELDS [] LENH {'chuong_trinh': 'codex', 'so_doi_so': 9, 'van_tay': '665be3d592a0bc7c'}
DURATION 606.042738 DECLARED 606.043 ERROR -0.000262
BASE_MERGE_BASE_PRE_MERGE b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 DECLARED b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
CURRENT_MASTER_MERGE_BASE f37b5195978f1fe35b9cb55b6f79a2e09d165af0 HISTORICAL_HEAD_NOT_SAME_BASE_EXPECTED
ANCESTOR 7333f97 047eaa4 rc 0
ANCESTOR 7333f97 6db9341 rc 1
ANCESTOR f37b5195978f1fe35b9cb55b6f79a2e09d165af0 79400f3 rc 0
```

Kết luận: KHÔNG PHẢI LỖI trong nội dung đo được. Verdict/counts/IDs, model evidence, số sự kiện, prompt, thời lượng (chênh làm tròn <0.0003s) và metadata đều khớp. Chỉ lượt approve nhận cross_approved. Hai run ID riêng; prompt tự chứa; người ghi sổ nhận mình là điều phối gọi Codex, không tự nhận tác giả verdict. MRI là OpenAI theo run đã lưu; executor họ Claude theo hồ sơ/chỉ thị, không có runtime executor kèm để chứng minh mọi chi tiết phiên/người vận hành. Submitter `(b)` và chỉ thị chat không đo độc lập được. Không suy actor GitHub thành model reviewer.

KHÔNG ĐO ĐƯỢC độc lập: phiên bản CLI 0.164.0, raw argv/các cờ cụ thể, cấu hình model mặc định tài khoản; run chỉ lưu chương trình/argc/fingerprint. Lời khai requested model đã ghi KHONG_DO_DUOC. Không có chứng cứ ngược để kết tội các lời khai cấu hình. Cặp nguồn run/verdict chứng minh sự nhất quán của hiện vật đã giữ, không chứng nhận tuyệt đối ngữ cảnh executor hay danh tính người thật.

### Hướng 4 — base lịch sử, merge và trạng thái mỏ neo

LỆNH: `python3 evidence/measure_receipts.py` gọi `git merge-base <reviewed_sha> 79400f3^1`, `git show -s ... 79400f3`, `git log --first-parent ... -4 6db9341`, `git merge-base --is-ancestor ...`; phép so blob ở Hướng 2. OUTPUT THẬT:

```text
MERGE 79400f3cdc6b780319b66f57c27e5772ad010101
4f11b13c3d286a79dbe9a83547a800005cda0eda f37b5195978f1fe35b9cb55b6f79a2e09d165af0
2026-10-31T01:55:24+07:00
Merge pull request #1050 from ducthangho/claude/magical-clarke-gzvwbp
MASTER_FIRST_PARENT_TIMELINE 6db934145acf6e47d01db5b2dc8c9da417c2d8eb 2026-10-31T02:11:55+07:00 Merge pull request #1054 from ducthangho/claude/epic-ritchie-quvrz1
79400f3cdc6b780319b66f57c27e5772ad010101 2026-10-31T01:55:24+07:00 Merge pull request #1050 from ducthangho/claude/magical-clarke-gzvwbp
4f11b13c3d286a79dbe9a83547a800005cda0eda 2026-10-31T01:46:42+07:00 Merge pull request #1053: land(#1030) hồ sơ land wp1030 r6 — landed false
b29da0bfe3bfb7a7be69136a1c5c40f82c088a93 2026-10-31T00:28:50+07:00 Merge pull request #1041 from ducthangho/agent/wp1037-g1-claude
OLD_BASE_SNAPSHOT origin/master b29da0bfe3bfb7a7be69136a1c5c40f82c088a93
PATCH_1050 10	4	ops/land/pr1041-wp1037-land-evidence.yaml
```

Kết luận: KHÔNG PHẢI LỖI. Cả hai merge-base với master ngay trước merge #1050 bằng b29da0b; run bắt đầu 17:53:06Z/18:09:50Z, sau b29da0b (17:28:50Z) và trước commit master kế tiếp 4f11b13 (18:46:42Z). Snapshot origin/master được lưu cũng b29da0b. Không có readback ref chính thời điểm dựng sandbox của tôi; chronology và snapshot hỗ trợ lời khai lịch sử, không phải chứng minh trực tiếp chuyển động mọi ref. Merge-base với master đã chứa #1050 ra chính reviewed head, không dùng để bác base lịch sử. Merge 79400f3 đúng #1050, cha 2 đúng f37b519. Blob tại 7333f97 tồn tại/bằng verdict và là tổ tiên 047eaa4 (rc0), chưa thuộc base master 6db9341 (rc1), nên anchor thap và điều kiện sẽ lên trung_binh khi land không sai tại SHA đang review. Người/phiên thực hiện merge chỉ có lời thuật lại, không chứng minh từ metadata tác giả Git.

### Hướng 5 — mục lục/caveat README, đích link và trùng hàng

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_readme.py`. OUTPUT THẬT:

```text
NEW_ROWS 8 UNIQUE 8
ROUND 1 TOC_COUNT 1 CAVEATS_COUNT 3
TOC_MATCH {'verdict': True, 'assurance': True, 'counts': True, 'run_id': True, 'model': True, 'head': True, 'bytes': True, 'round': True, 'target': True}
CAVEAT CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY EXACT_COUNT 1
CAVEAT SCRIPT-DO-DOC-DUONG-DAN-SANDBOX EXACT_COUNT 1
CAVEAT TEP-LON-KHONG-VAO-KHO EXACT_COUNT 1
LINKS [('pr1050-review-1-codex-verdict.md', True), ('pr1050-review-1-codex-verdict.receipt.yaml', True), ('pr1050-review-1-codex/', True)]
ROW | [`pr1050-review-1-codex-verdict.md`](pr1050-review-1-codex-verdict.md) | [`.receipt.yaml`](pr1050-review-1-codex-verdict.receipt.yaml) | khong co (PR ghi so cua #1037, chu kho giao truc tiep) | **`changes_requested`** · `cross_reviewed` · luot **1** cua PR **#1050** · 0/1/1/0 (P0/P1/P2/P3) · codex CLI `launcher.py run 1b0ff763`, `gpt-6.1-sol` do_may · thu muc goc [`pr1050-review-1-codex/`](pr1050-review-1-codex/) | `c24875d` | 41128 |
WARNING_ROW | `pr1050-review-1-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong. |
WARNING_ROW | `pr1050-review-1-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (evidence/*) tham chieu duong dan tuyet doi cua sandbox phien (/tmp/...); tai lap can clone tai c24875d. |
WARNING_ROW | `pr1050-review-1-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff.patch (>500 KB) va cac ban sao kho cua sandbox KHONG vao kho; sha256/so byte o OMITTED.txt. |
ROUND 2 TOC_COUNT 1 CAVEATS_COUNT 3
TOC_MATCH {'verdict': True, 'assurance': True, 'counts': True, 'run_id': True, 'model': True, 'head': True, 'bytes': True, 'round': True, 'target': True}
CAVEAT CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY EXACT_COUNT 1
CAVEAT SCRIPT-DO-DOC-DUONG-DAN-SANDBOX EXACT_COUNT 1
CAVEAT TEP-LON-KHONG-VAO-KHO EXACT_COUNT 1
LINKS [('pr1050-review-2-codex-verdict.md', True), ('pr1050-review-2-codex-verdict.receipt.yaml', True), ('pr1050-review-2-codex/', True)]
ROW | [`pr1050-review-2-codex-verdict.md`](pr1050-review-2-codex-verdict.md) | [`.receipt.yaml`](pr1050-review-2-codex-verdict.receipt.yaml) | khong co (PR ghi so cua #1037, chu kho giao truc tiep) | **`approve`** · `cross_approved` · luot **2** cua PR **#1050** · 0/0/0/0 (P0/P1/P2/P3) · codex CLI `launcher.py run 8c095c6b`, `gpt-6.1-sol` do_may · head da duyet = head PR #1050 luc merge (`79400f3`) · thu muc goc [`pr1050-review-2-codex/`](pr1050-review-2-codex/) | `f37b519` | 37384 |
WARNING_ROW | `pr1050-review-2-codex-verdict.md` | `CHECKOUT-REVIEW-KHONG-CUONG-CHE-READ-ONLY` | Ban sao cay-kho/ nam TRONG vung ghi sandbox codex (workspace-write); read-only chi la CHI THI. run.json worktree_sach true luc phong. |
WARNING_ROW | `pr1050-review-2-codex-verdict.md` | `SCRIPT-DO-DOC-DUONG-DAN-SANDBOX` | Script/bang chung cua reviewer (evidence/*) tham chieu duong dan tuyet doi cua sandbox phien (/tmp/...); tai lap can clone tai f37b519. |
WARNING_ROW | `pr1050-review-2-codex-verdict.md` | `TEP-LON-KHONG-VAO-KHO` | diff.patch (>500 KB) va cac ban sao kho cua sandbox KHONG vao kho; sha256/so byte o OMITTED.txt. |
HEAD_AT_MERGE_MATCH True
```

Kết luận: KHÔNG PHẢI LỖI. Đúng hai hàng TOC và sáu cảnh báo mới, tám hàng riêng biệt. Verdict/số đếm/run/head/model/bytes đúng; link tồn tại; mỗi cảnh báo bằng nguyên văn receipt đúng một lần. Head approve f37b519 bằng cha 2 merge 79400f3, không đánh tráo thành merge SHA. Baseline sáu cổng rc0 đã có marker dương ở mục Đo cổng — baseline; không skip hay tạo tác `Codex home is inside a repository`.

### Đo cổng — mutant-byte

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_gates.py review-copy mutant-byte`; mỗi subprocess chạy các lệnh sẵn có dưới đây tại `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056-r2/review-copy`. OUTPUT THẬT:

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ],
    "sandbox_artifact": false
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 1,
    "summary": [
      "lease_publish: 0/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 0,
    "summary": [
      "lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  }
}
```

Log đầy đủ: `evidence/mutant-byte-*.log`; rc lưu riêng.

### Đo cổng — mutant-readme

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_gates.py review-copy mutant-readme`; mỗi subprocess chạy các lệnh sẵn có dưới đây tại `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056-r2/review-copy`. OUTPUT THẬT:

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ],
    "sandbox_artifact": false
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 1,
    "summary": [
      "lease_publish: 1/2 đạt; đã chạy=2, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  }
}
```

Log đầy đủ: `evidence/mutant-readme-*.log`; rc lưu riêng.

### Hướng 6 — rò rỉ trong hiện vật/run/log/evidence

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_secrets.py`, bao gồm chạy scanner sẵn có `python3 scripts/pkg_secret_scan.py ops/reviews/pr1050-review-{1,2}-codex` (đối số tuyệt đối đến đúng gói); 21 mẫu gồm scanner/hook hiện có và bổ sung PAT/URL credential/assignment, cộng mẫu đường dẫn credential. Chỉ quét tệp PR, không đọc credential thật. OUTPUT THẬT:

```text
CHANGED_FILES 180 NON_UTF8 [] PATTERNS 21 SECRET_HITS 0 CREDENTIAL_PATH_HITS 0
REDACTED_SECRET_LOCATIONS []
REDACTED_CREDENTIAL_PATH_LOCATIONS []
PKG_SCAN 1 rc 0 stdout (empty) stderr (empty)
COVERAGE 1 FILES 93 SCANNABLE 93 MAX_BYTES 41128
PKG_SCAN 2 rc 0 stdout (empty) stderr (empty)
COVERAGE 2 FILES 82 SCANNABLE 82 MAX_BYTES 41128
```

Kết luận: KHÔNG PHẢI LỖI trong phạm vi dò mẫu và rà nội dung đã lưu: không thấy token/key/credential path hay nội dung bí mật. Đường dẫn sandbox, Git hashes, response/session/run IDs là metadata, không tự là credential. Mọi tệp gói đều được xét; không lược vì đuôi .log/.patch hay kích thước. Phép dò không chứng minh tuyệt đối mọi chuỗi tự do đều không bí mật.

### Đo cổng — mutant-count

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_gates.py review-copy mutant-count`; mỗi subprocess chạy các lệnh sẵn có dưới đây tại `/tmp/claude-0/-home-user-tra-luat/6311a229-c7eb-5096-a819-78ab343b359f/scratchpad/rv1056-r2/review-copy`. OUTPUT THẬT:

```json
{
  "bien_nhan_v2": {
    "command": "python3 ops/bien_nhan_v2.py --root .",
    "rc": 0,
    "summary": [
      "bien_nhan_v2: 257 ĐẠT v2 · 11/11 miễn trừ legacy (băm khớp) · 42 NỢ đóng băng · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 310",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "land_evidence_nguon": {
    "command": "python3 ops/land_evidence_nguon.py --root .",
    "rc": 0,
    "summary": [
      "land_evidence_nguon: 66 ĐẠT · 25/28 miễn trừ (băm khớp) · 0 vi phạm · 0 KHÔNG ĐO ĐƯỢC · tổng 91",
      "TỔNG: ĐẠT"
    ],
    "sandbox_artifact": false
  },
  "doctrine_scan": {
    "command": "python3 .claude/dev/packet_loop.py doctrine-scan --root .",
    "rc": 0,
    "summary": [
      "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine"
    ],
    "sandbox_artifact": false
  },
  "t26": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t26_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t27": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t27_",
    "rc": 0,
    "summary": [
      "lease_publish: 2/2 đạt; đã chạy=2, bỏ qua=0"
    ],
    "sandbox_artifact": false
  },
  "t138": {
    "command": "python3 ops/lease_publish_test.py --chi-ca=t138_",
    "rc": 0,
    "summary": [
      "lease_publish: 1/1 đạt; đã chạy=1, bỏ qua=0"
    ],
    "sandbox_artifact": false
  }
}
```

Log đầy đủ: `evidence/mutant-count-*.log`; rc lưu riêng.

### Hướng 7 — lời khai hai finding của #1050 đã đóng, tránh tự khai thuận lợi

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/measure_parent_closure.py` dùng hàm `_phan_loai_lease` sẵn có với mốc tường minh; Git diff `c24875d..f37b519` và nguồn run/jobs được lưu. Không chạy scanner `ai-dang-giu` vì nó gọi mạng. OUTPUT THẬT (log đủ ở `evidence/parent-closure.log`):

```text
LEASE_SNAPSHOT_EQUAL True
LEASE_CLASS 2026-10-30T17:37:00Z CÒN_HẠN
LEASE_CLASS 2026-10-30T17:53:00Z HẾT_HẠN
LEASE_CLASS 2026-10-30T18:07:34Z HẾT_HẠN
AFTER_EXPIRY_LOG_HASH cbc0c4a31a8df98e835ea232a96b4339cf763b3c7d302a087f7de4c23c1ba765 IN_MANIFEST True
LANDED False
LEASE_CLAIM measured — lease-wp1037-r1-g1.yaml.txt (ban doc tai a34b9a3): DA RUT HAN; CHUA NHA tai moc ghi so 17:37Z (khong bia mo — lease con han, khong co lease ke nhiem): lease_until/lease_expires_at_utc ve 2026-10-30T17:53:00Z, ly do trong khoi thu_hoi_bang_rut_han cua chinh tep lease. Han moi = luc sua + 20 phut de luot ops-publish-lease cua commit rut han doc lease CON HAN (rc=9), khong roi vao rc=8. Chi sau 17:53Z moi do lai ai-dang-giu tren du ref de xac nhan da nha; chua co phep do ay trong ban ghi so dau (c24875d).
NEW_MEASUREMENT measured — ai-dang-giu-sau-rut-han/luc-do.txt (do 2026-10-30T18:07:34Z, SAU han moi 17:53Z): ls-remote 708 ten = for-each-ref 708 ten (thieu 0, thua 0); ai-dang-giu ops/bien_nhan_v2_test.py: wp1037-r1-g1-claude HẾT_HẠN; NGƯỜI_GIỮ 1: wp1021-r2-g1-claude (lease cua #1021, dung du kien). Khoi nay THEM SAU, co moc rieng; cau 'CHUA NHA tai moc ghi so 17:37Z' o tren giu nguyen.
WINDOWS 1 EVENT workflow_dispatch RUN_ATTEMPT 1 TOTAL 16 ACTUAL 16 COUNTS {'success': 13, 'failure': 2, 'skipped': 1} WINDOWS_JOBS 14
FAILED_STEPS gate-cong-cu (windows-latest, 0) ['G5 manh ban kinh dot bien (#668)']
FAILED_STEPS gate-packet-loop (windows-latest) ['G5 probe ban ke cong cu (#290; selftest T1..T8 chi o job gate, chot M6']
WINDOWS 2 EVENT workflow_dispatch RUN_ATTEMPT 2 TOTAL 16 ACTUAL 16 COUNTS {'success': 15, 'skipped': 1} WINDOWS_JOBS 14
WINDOWS_NAME ci.yml workflow_dispatch (nhan windows-latest do tu jobs) tren head cuoi
WINDOWS_NOTE measured — readback-run-41069257658-a1.json / readback-jobs-41069257658-a1.json: attempt 1 13 success · 2 failure (gate-packet-loop: G5 probe ban ke cong cu; gate-cong-cu windows-latest 0: G5 manh ban kinh dot bien) · 1 skipped; readback-run-41069257658-a2.json / readback-jobs-41069257658-a2.json: attempt 2 (rerun_failed_jobs mot lan) 15 success · 1 skipped (gate-cong-cu-gop), run conclusion success. Job gate-ops (windows-latest) attempt 1: bien_nhan_v2_test 95/95 · 137/137 · 2/2 TONG DAT, lease_publish 255/255 (thuat_lai tu log job 124108765783, log khong luu trong kho). Thuat_lai — executor khai input runner_set=windows-only va nguyen nhan runner thieu shellcheck, goc loi ops/cai_cong_cu.sh, tach packet #1045; KHONG_DO_DUOC tu readback run/jobs da luu, khong co log chan doan hoac readback inputs trong provenance.
NO_REMOTE_QUERY: historical server ref set 708/708 cannot be independently replayed offline; only saved log and lease classification measured.
```

Kết luận: KHÔNG PHẢI LỖI trong lời khai đóng finding ở receipt. Git diff chỉ ba tệp: land YAML, một hàng manifest, log 28 dòng. Lỗi lease sửa đúng thành CHƯA NHẢ tại snapshot 17:37Z; phép đo sau hạn có mốc/băm riêng, không viết lại quá khứ; `landed` giữ false. Nguyên nhân thiếu shellcheck và input Windows đã tách khỏi measured thành thuật lại/KHONG_DO_DUOC; nguồn jobs chỉ chứng minh labels/steps/counts, đúng câu mới. Receipt nói “theo nghĩa HINT”, không khai bản vá #1050 nguyên byte HINT (vì có thêm phép đo sau hạn).

KHÔNG ĐO ĐƯỢC độc lập: ref server 708/708 tại thời điểm cũ, tác giả phiên executor và người thật bấm merge; chỉ có log/bằng chứng đã giữ. Không đọc trạng thái CHƯA merge trong PROMPT/verdict lịch sử của #1050 như một câu nói về trạng thái hiện tại ở 047eaa4. Lượt 2 cũ có khai một lần vô ý thử mạng bị chặn; hiện vật giữ nguyên sự việc, không bị người ghi sổ xoá hay đổi thành phép đo thành công. Lượt review này không gọi mạng.

### Hướng 8 — phản chứng dữ liệu trên clone, cổng có răng tới đâu

LỆNH: `git clone --no-hardlinks --no-checkout mirror.git review-copy`; checkout detached `047eaa4…` và core.abbrev=7; `PYTHONDONTWRITEBYTECODE=1 python3 evidence/run_mutations.py`. Script chỉ sửa dữ liệu một trường hợp/lần rồi phục hồi byte gốc; mỗi trường hợp gọi đúng sáu lệnh sẵn có như baseline. OUTPUT THẬT tổng hợp (log/rc/marker đầy đủ đã nối từng mục ở trên và trong `evidence/mutations.log`, `evidence/*-gates.json`):

| đột biến độc lập | bien_nhan_v2 | land_evidence_nguon | doctrine-scan | t26 | t27 | t138 |
|---|---:|---:|---:|---:|---:|---:|
| verdict phẳng lượt 1: LF cuối → space, đúng 1 byte, vẫn 41128B | 0 | 0 | 0 | **1; 0/1** | 0; 2/2 | 0; 1/1 |
| xoá đúng hàng TOC mới lượt 1: README giảm 446B | 0 | 0 | 0 | 0; 1/1 | **1; 1/2** | 0; 1/1 |
| receipt so_p1: 1 → 9, đúng 1 byte, vẫn 6019B | 0 | 0 | 0 | 0; 1/1 | 0; 2/2 | 0; 1/1 |

Kết luận: KHÔNG PHẢI LỖI mới của dữ liệu gốc; số đếm gốc đúng theo đối chiếu trực tiếp ở Hướng 3. `t26` bắt sai byte, `t27` bắt mất hàng mục lục. Các cổng còn xanh **KHÔNG CÓ RĂNG với đúng đột biến tương ứng**; đặc biệt cả sáu cổng không canh so_p1 với verdict. `t138` kiểm fixture receipt thu hồi, không chứng minh nội dung hai biên nhận review này. Không nâng `TỔNG: ĐẠT` thành xác minh mọi câu chữ receipt. Các ca có marker N/N thực, không skip và không gặp lỗi `Codex home is inside a repository`.

### Hướng 9 — kiểm cuối tính bất biến và phạm vi phép đo

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/final_integrity.py`. OUTPUT THẬT:

```text
cay-kho git rev-parse HEAD HEAD^{tree} rc 0 stdout 047eaa4d26a5bb1e702199c870f42480aebed673
ac826681109d74ad18efc3120c79b65ddb8280a2 stderr (empty)
cay-kho git status --short --untracked-files=all --ignored=matching rc 0 stdout (empty) stderr (empty)
cay-kho git diff --exit-code rc 0 stdout (empty) stderr (empty)
cay-kho git diff --cached --exit-code rc 0 stdout (empty) stderr (empty)
cay-kho git diff --check rc 0 stdout (empty) stderr (empty)
cay-kho git config core.abbrev rc 0 stdout 7 stderr (empty)
cay-kho ALL_CHANGED_FILES_EQUAL_HEAD 180 / 180
review-copy git rev-parse HEAD HEAD^{tree} rc 0 stdout 047eaa4d26a5bb1e702199c870f42480aebed673
ac826681109d74ad18efc3120c79b65ddb8280a2 stderr (empty)
review-copy git status --short --untracked-files=all --ignored=matching rc 0 stdout (empty) stderr (empty)
review-copy git diff --exit-code rc 0 stdout (empty) stderr (empty)
review-copy git diff --cached --exit-code rc 0 stdout (empty) stderr (empty)
review-copy git diff --check rc 0 stdout (empty) stderr (empty)
review-copy git config core.abbrev rc 0 stdout 7 stderr (empty)
review-copy ALL_CHANGED_FILES_EQUAL_HEAD 180 / 180
ORIGINAL_ARTIFACT_COMMIT_FILES_EQUAL 177 / 177
SUPPLIED_PATCH_EQUAL True BYTES 2202
CURRENT_PROMPT_SNAPSHOT_EQUAL True PROMPT_BYTES 6387 SHA256 3f3def22144b76e031c9b5236d8ff98b4c4079e6474cc303a0a11b25dc0ee0c2
```

Kết luận: KHÔNG PHẢI LỖI. Cây gốc và clone đều ở exact reviewed SHA/tree; tracked/untracked/ignored, index và diff sạch; 180/180 tệp PR bằng blob đúng SHA, 177/177 tệp hiện vật ở 7333f97 nguyên byte. Mọi đột biến dữ liệu đã phục hồi. Không sửa cay-kho, không push, không gọi mạng trong lượt này. Các lệnh Python dùng PYTHONDONTWRITEBYTECODE=1; không tạo cache trong cây review. Snapshot sạch đầu/cuối chỉ chứng minh không có delta ở hai mốc.

Không có finding P0/P1/P2/P3 mới, không cần HINT.patch. Finding lượt 1 **ĐÓNG**; phần vá không khai rộng hơn kết quả classifier/so cây. **approve** tại `047eaa4d26a5bb1e702199c870f42480aebed673`: sáu cổng đạt, số đếm/hiện vật/README đúng; giới hạn về runtime executor, CLI argv/version, ref lịch sử và chốt so_p1 được giữ rõ. Đây là verdict cho PR ghi sổ #1056; không cấp quyền merge/land hoặc nâng hồ sơ #1037 thành landed.
