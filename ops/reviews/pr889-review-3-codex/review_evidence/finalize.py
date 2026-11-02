from pathlib import Path
import hashlib
import json
import os
import re
import subprocess

root = Path(__file__).resolve().parents[1]
repo = root / 'cay-kho'
sha = '094e8d17ae4dfcf21dca63702c9262267bdc072c'
commands = [
    ['git', 'rev-parse', 'HEAD'],
    ['git', 'rev-parse', 'HEAD^{tree}'],
    ['git', 'status', '--porcelain=v1', '--untracked-files=all'],
    ['git', 'diff', '--exit-code'],
    ['git', 'diff', '--cached', '--exit-code'],
    ['git', 'diff', '--check', 'e63961f', sha, '--', 'CLAUDE.md'],
]
records=[]
for cmd in commands:
    p=subprocess.run(cmd,cwd=repo,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'),capture_output=True,text=True)
    records.append({'command':' '.join(cmd),'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
    assert p.returncode == 0, records[-1]
assert records[0]['stdout'].strip() == sha
assert records[1]['stdout'].strip() == '55f5edf2f8601c976f390e8994193129a71203a1'
assert not records[2]['stdout']
claims=json.loads((root/'review-evidence/doc-claims.log').read_text())
assert claims['ok'] is True
assert all(v == 0 for v in claims['by_layer'].values())
assert not claims['flags'], claims['flags']
assert all(p.read_text().strip() == '0' for p in (root/'review-evidence').glob('*.rc'))
(root/'review-evidence/final-state.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
path=root/'VERDICT.md'
s=path.read_text()
assert s.startswith('verdict: dang_lam\nreviewed_sha: '+sha+'\n')
# Keep the useful SHA comparison and remediation diff from direction 7. The
# original discovery log also listed unrelated later commit subjects; direction
# 10 replaces that discovery with history constrained to reviewed_sha ancestry.
start=s.index('history #878:\n')
end=s.index('\n```\n',start)
s=s[:start]+'(Phần tìm lịch sử rộng ban đầu không dùng làm căn cứ; xem HƯỚNG 10 với git log giới hạn reviewed_sha và đối chiếu thay đổi trước/sau #878/#879.)\n'+s[end:]

rows = [
('Phạm vi/SHA (toàn diff)', 'Đo trên e63961f, ngày 23-10-2026; review head đã vá', '`git rev-parse HEAD; git show -s --format=fuller e63961f; python3 -B ../review-evidence/measure.py history` → HEAD đúng 094e8d17…; base là tổ tiên, ngày commit base 23-10; ci.yml/cong_cu_test.py/lease_publish_test.py ở base giống byte tại head. H1/H7/H10.', 'Có về phiên bản; thời điểm từng phép đo lịch sử không thể tái chứng thực'),
('Nhánh thứ ba, #878 (CLAUDE.md:164)', '#878 bổ sung nhánh windows-only', '`python3 -B ../review-evidence/measure_extra.py history-anchored` → trước #878 có 2 mảng literal, tại head có 3; commit 5585abe8499e920e2a6ae8236e70c4096f95e71d và merge 747f983 đều là tổ tiên. H10.', 'Có'),
('Dispatch windows-only (164–165)', 'Chỉ ["windows-latest"], không Ubuntu', '`python3 -B ../review-evidence/measure.py chuanbi` → dispatch windows-only: ["windows-latest"]. Evaluator được trích bằng AST từ chính SHA. H2.', 'Có'),
('Mặc định input (165)', 'windows-and-ubuntu', '`python3 -B ../review-evidence/measure.py chuanbi` → default=windows-and-ubuntu, required=false, type=choice, options có hai giá trị. H2.', 'Có'),
('Dispatch mặc định/vắng/lạ (165)', 'Mặc định vẫn hai nền', '`python3 -B ../review-evidence/measure.py chuanbi` → default/missing/other đều ["ubuntu-latest","windows-latest"]. Giá trị lạ chỉ kiểm biểu thức, không khẳng định API nhận choice ngoài danh sách. H2.', 'Có'),
('Push và PR đối chứng', 'runner_set chỉ đổi nhánh gọi tay', '`python3 -B ../review-evidence/measure.py chuanbi` → push master/PR thường: Ubuntu; PR nhãn windows: Ubuntu+Windows; ép input windows-only không đổi ba ca đối chứng. H2.', 'Có'),
('#879 làm gate Windows chỉ còn một phần (180)', 'Không phải bản song song đầy đủ', '`python3 -B ../review-evidence/measure.py topology; python3 -B ../review-evidence/measure_extra.py history-anchored` → Windows mất mảnh 1..7 và gom; lịch sử be00ef7 thêm đúng thay đổi ấy, là tổ tiên của head. H4/H10.', 'Có'),
('gate-cong-cu, mảnh 0 (181)', 'Windows chỉ mảnh 0', '`python3 -B ../review-evidence/measure.py topology` → os=[Windows] chỉ [{"os":"windows-latest","manh":0}]; os=hai nền giữ Ubuntu 0..7 và Windows 0. H4.', 'Có'),
('Duyệt ca nền rồi dừng (182)', 'Windows G5 mảnh chạy qua CA rồi dừng', '`python3 -B ../review-evidence/measure.py windows-main` → cả 5 kịch bản đều thăm đủ hai CA giả; cài chốt ném nếu chạm phân mảnh/phóng con/ghi mảnh/cổng cây thật nhưng không chạm. Predicate nt=true, posix/java=false. H6.', 'Có về đường điều khiển; không giả khai chạy CA thật trên Windows'),
('Bỏ qua vì thiếu năng lực (182)', 'Ca vẫn có thể BỎ QUA', '`python3 -B ../review-evidence/measure.py windows-main` → one-skip in BỎ QUA second và rc=0; all-skip rc=1; precheck-skip rc=1. H6.', 'Có'),
('Công thức mẫu số (183)', 'so_ca = len(CA) - len(bo_qua)', '`python3 -B ../review-evidence/measure.py windows-main` → source present=True; một ca bỏ qua trong hai ca cho cong_cu_test: 1/1 đạt, tổng=2, bỏ qua=1. Dòng nguồn 8916. H6.', 'Có'),
('Bán kính chỉ đo Ubuntu trong CI G5 (183)', 'Windows không có bằng chứng bán kính đầy đủ', '`python3 -B ../review-evidence/measure.py windows-main; python3 -B ../review-evidence/measure_extra.py workflow-modes` → gate dùng mode gate (giao vòng đầy đủ cho mảnh); Windows mảnh dùng mode manh nhưng dừng sau CA; gom chỉ Ubuntu. H4/H6/H9.', 'Có trong phạm vi CI được đoạn văn mô tả'),
('gate-cong-cu-gop loại Windows (184)', 'exclude: windows-latest', '`python3 -B ../review-evidence/measure.py topology` → exclude=[{"os":"windows-latest"}], ma trận hai nền sau lọc chỉ Ubuntu. H4.', 'Có'),
('gom với windows-only và if Ubuntu (184–185)', 'Job skipped vì if đòi ubuntu-latest trong os', '`python3 -B ../review-evidence/measure.py topology` → predicate chính xác !cancelled() && contains(fromJson(...),ubuntu-latest) trả false với windows-only cả khi cancelled=false/true; lọc ma trận cho []. H4.', 'Khớp cấu hình; skipped trên máy chủ là suy luận, KHÔNG ĐO ĐƯỢC lượt chạy thực khi không mạng'),
('Các gate* khác ở mức JOB (185)', 'Vẫn có Windows', '`python3 -B ../review-evidence/measure.py topology` → gate=1, gate-ops=1, gate-nhanh-manh=8, gate-nhanh-gop=1, gate-registry=1, gate-packet-loop=1 Windows rows; job-if không đòi Ubuntu. H4.', 'Có về khả năng được tạo trong ma trận, không bảo đảm job luôn chạy khi hủy/lỗi phụ thuộc'),
('Số bước điều kiện OS (185–187)', '6 bước theo runner.os', '`python3 -B ../review-evidence/measure.py os-steps` → total=6; runner.os=6; matrix.os=0; đối chiếu quét dòng cũng 6 (430,575,697,786,819,860). H5.', 'Có'),
('Có job chưa phải mọi bước (186–187)', 'Bước bị tắt hoặc thay riêng Windows', '`python3 -B ../review-evidence/measure.py os-steps` → ci-phamvi, upload mảnh, ci-duong-nhanh, don-nhanh, cgroup Linux và lifecycle nền không cgroup có điều kiện OS; Windows bỏ năm bước đầu, dùng bước lifecycle thay cgroup. H5.', 'Có'),
('Câu sửa thêm ngoài hint (187–188)', 'Lượt xanh chỉ chứng minh ca nền KHÔNG bị bỏ qua đạt', '`git diff 8d5cccb HEAD -- CLAUDE.md; python3 -B ../review-evidence/measure.py windows-main` → câu kết đã thu hẹp; one-skip=rc0, 1/1 trên tổng2; one-fail=rc1; all-skip=rc1; dat_windows đòi số ca>0, lỗi=0, số đột biến>0. H6/H7.', 'Có; không còn suy từ xanh thành tất cả CA đạt'),
('Đọc riêng log BỎ QUA (188)', 'Phải xem riêng ca thiếu năng lực', '`python3 -B ../review-evidence/measure.py windows-main` → in BỎ QUA cho CA, BỎ QUA (TIỀN KIỂM) riêng, tổng kết khai bỏ qua và tiền kiểm bỏ qua. H6.', 'Có; log tổng xanh không liệt kê trong tỷ lệ phần bị trừ'),
('Bán kính từ Ubuntu CÙNG head (188–189)', 'Không lấy bằng chứng từ SHA khác', '`python3 -B ../review-evidence/measure_extra.py workflow-modes` → _van_tay trả đúng 094e8d17… và hash test 23dbdeada416…; _gom_manh với header head=000… trả [G-van-tay], errors=1. Bằng chứng giả dựng ngoài repo. H9.', 'Có; không khẳng định đã có một lượt Ubuntu xanh thật tại SHA này'),
]
header='| khẳng định | PR khai | đo được (lệnh) | khớp? |\n|---|---|---|---|\n'
table=header+'\n'.join('| '+' | '.join(row)+' |' for row in rows)+'\n'
assert header in s
s=s.replace(header,table,1)
s=s.replace('Đang đọc chỉ thị và đo độc lập tại SHA được yêu cầu; không đọc verdict lượt 2.', 'Đo độc lập tại đúng SHA được yêu cầu; không đọc verdict lượt 2. Các script và tệp bằng chứng nằm ngoài cay-kho/. Lệnh trong bảng được chạy từ cay-kho/; -B tương đương PYTHONDONTWRITEBYTECODE=1 đã dùng khi đo. Output rút gọn có ghi rõ trong từng hướng; log đầy đủ của các phép đo được lưu ở review-evidence/.',1)
s+='\nHƯỚNG 11: Kiểm bất biến cuối phiên và whitespace của diff\n  giả thuyết : Phép đo làm đổi repository hoặc SHA, hoặc bản vá có lỗi whitespace.\n  lệnh       : Các lệnh git dưới đây, cwd=cay-kho/, GIT_OPTIONAL_LOCKS=0.\n  output     :\n\n```text\n'
for r in records:
    s+=r['command']+'\nrc='+str(r['rc'])+'; stdout='+repr(r['stdout'].strip())+'; stderr='+repr(r['stderr'].strip())+'\n'
s+='```\n  kết luận   : KHÔNG PHẢI LỖI. Repository vẫn sạch; không sửa cay-kho/, không commit/push, không gọi mạng.\n'
s+='''
## KẾT LUẬN

Không có finding P0/P1/P2/P3 trong diff tại reviewed_sha. Phần sửa ở 094e8d1, bao gồm câu kết ngoài hint, khớp phản chứng: xanh 1/1 có thể đến từ tổng 2 ca với một ca BỎ QUA, nên chỉ chứng minh những ca không bị bỏ qua đạt. Tỷ lệ 0/0 hoặc một ca đỏ không cho nhánh Windows trả thành công.

Hai cổng bắt buộc:

- `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **rc=0**; `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- `python3 scripts/tl.py doc-claims-check --json`: **rc=0**, **"ok": true**; 113 tệp; mọi `by_layer` bằng 0; `flags=[]`, `layers_skipped={}`. `claims_flagged=381` đều là advisory (`advisory_count=381`), không phải finding chặn.

Giới hạn phép đo: ma trận, predicate, số bước, mã nguồn và đường điều khiển AST đã đo cục bộ. Không có Windows runner và không có mạng nên không chạy CA thật trên Windows, không đo toàn bộ bán kính Ubuntu, không đọc kết luận scheduler `skipped` hay trạng thái một run GitHub thật tại SHA này. `skipped` trong tài liệu phù hợp điều kiện job đo được; không khai nó thành bằng chứng máy chủ đã readback. Không phát hiện sự thật cục bộ nào trái với mô tả và không coi phần không đo được là đã pass.

Không cần HINT.patch vì không có finding. Không áp patch vào cây thật.

Định danh: reviewer Codex; provider `openai_codex`; execution_surface `codex_service` (có công cụ shell trực tiếp, không phải ChatGPT Web human-mediated); transport `machine`. Không suy model thực tế từ tác giả commit hoặc tên launcher; định danh model máy chủ trả không được kiểm độc lập trong phép đo repo này. Không tự cấp assurance/approval cho state machine hay thao tác land.

`reviewed_tree: 55f5edf2f8601c976f390e8994193129a71203a1`
'''
s=s.replace('verdict: dang_lam\n','verdict: approve\n',1)
s=s.replace('reviewed_sha: '+sha+'\n','reviewed_sha: '+sha+'\nKết quả: 0 P0, 0 P1, 0 P2, 0 P3.\n',1)
path.write_text(s)
assert len(re.findall(r'^HƯỚNG \d+:',s,re.M)) == 11
assert len(rows)==20
assert not (root/'HINT.patch').exists()
print('VERDICT.md finalized: approve; 20 claim rows; 11 directions; 0 findings; both mandatory gates rc=0; repository clean.')
print('bytes:',path.stat().st_size)
print('sha256:',hashlib.sha256(path.read_bytes()).hexdigest())
