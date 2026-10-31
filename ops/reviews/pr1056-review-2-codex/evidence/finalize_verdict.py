from pathlib import Path
b=Path(__file__).resolve().parent.parent;p=b/'VERDICT.md'
s=p.read_text()
table='''## BẢNG ĐO

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

'''
s=s[:s.index('## BẢNG ĐO')]+table+s[s.index('## BẢNG SĂN'):]
# Put the original raw command outputs into a fenced block; retain every logged byte.
a=s.index('LỆNH: các lệnh Git trong `evidence/preflight.log`');start=s.index('OUTPUT THẬT:\n\n',a)+len('OUTPUT THẬT:\n\n');end=s.index('\nKết luận Hướng 1:',start);s=s[:start]+'```text\n'+s[start:end]+'```\n'+s[end:]
s+='''
### Hướng 9 — kiểm cuối tính bất biến và phạm vi phép đo

LỆNH: `PYTHONDONTWRITEBYTECODE=1 python3 evidence/final_integrity.py`. OUTPUT THẬT:

```text
'''+(b/'evidence/final-integrity.log').read_text()+'''```

Kết luận: KHÔNG PHẢI LỖI. Cây gốc và clone đều ở exact reviewed SHA/tree; tracked/untracked/ignored, index và diff sạch; 180/180 tệp PR bằng blob đúng SHA, 177/177 tệp hiện vật ở 7333f97 nguyên byte. Mọi đột biến dữ liệu đã phục hồi. Không sửa cay-kho, không push, không gọi mạng trong lượt này. Các lệnh Python dùng PYTHONDONTWRITEBYTECODE=1; không tạo cache trong cây review. Snapshot sạch đầu/cuối chỉ chứng minh không có delta ở hai mốc.

Không có finding P0/P1/P2/P3 mới, không cần HINT.patch. Finding lượt 1 **ĐÓNG**; phần vá không khai rộng hơn kết quả classifier/so cây. **approve** tại `047eaa4d26a5bb1e702199c870f42480aebed673`: sáu cổng đạt, số đếm/hiện vật/README đúng; giới hạn về runtime executor, CLI argv/version, ref lịch sử và chốt so_p1 được giữ rõ. Đây là verdict cho PR ghi sổ #1056; không cấp quyền merge/land hoặc nâng hồ sơ #1037 thành landed.
'''
lines=s.splitlines();lines[0]='verdict: approve';lines[1]='reviewed_sha: 047eaa4d26a5bb1e702199c870f42480aebed673';lines[2]='Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.';p.write_text('\n'.join(lines)+'\n')
