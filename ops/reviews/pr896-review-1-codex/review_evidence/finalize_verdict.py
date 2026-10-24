import json
from pathlib import Path
import re

root=Path(__file__).resolve().parent.parent
p=root/'VERDICT.md'
s=p.read_text()
sha='816f43988eb3012726120ad00166a989cc2b9af6'
rows=[
('Exact head/tree/base và diff','816f439… trên base 1ccc314…; 6 tệp','H1/H15: git rev-parse HEAD, HEAD^{tree}; git diff base head == ../diff.patch; tree=3da0ce24590dfcf2e60805b2bef76687cdd64405; +31/-34 CLAUDE, land +27/-0, sums +3/-0, readback +6/+436/+29','Có'),
('Ba lần tài liệu trôi khỏi CI','BA: #548, #878, #879','H11: python3 ../review_evidence/history_probe.py; so YAML/CLAUDE ở d705623^, d705623, 5f288ea, 747f983, e63961f, 6ac385f','Có'),
('#548 bỏ điều kiện master','CI-MA-TRAN-WINDOWS-CHAY-MOI-LAN-LAND; chuan-bi','H11: git show d705623^:.github/workflows/ci.yml so d705623:…; biểu thức cũ có github.ref master, mới không có; thêm nguồn chung chuan-bi','Có (bỏ điều kiện khi đưa công thức về chuan-bi)'),
('Sửa ở #870; cũ tiếp #878/#879; đo lại #889','windows-only và một phần gate','H11: git show 5f288ea, 747f983, e63961f, 6ac385f; docs #870 giữ hai nền dispatch khi #878 đã có windows-only; #879 thêm exclude; #889 thêm cảnh báo','Có'),
('Run 39354156843','ci.yml; push 3a3a3ca lên master; 23 job Ubuntu','H11: đọc JSON readback-run/readback-jobs-39354156843; id=39354156843, event=push, head_branch=master, head_sha=3a3a3caca5de4934ff53851feb6994c2c7b84ad5, total_count=len=unique=23; 23 success, 23 labels=[ubuntu-latest], runner_id0=0','Có'),
('Biên bản cũ gây hiểu nhầm','3f6c694: jobs: 23/23 success (gom windows)','H11: git show 3f6c694:ops/land/pr848-wp744-land-evidence.yaml; đúng chuỗi tại post_merge_checks','Có'),
('Connector bắt P1 #859, r4323607674','Tác giả/mức P1/comment cụ thể','H11: git show 4ae43f0 và merge #859/865; correction ghi connector P1 #859 r4323607674; không có raw comment để xác minh độc lập author/P1','Một phần; raw comment KHÔNG ĐO ĐƯỢC offline'),
('Sửa ở #865','Đính chính 23/23 chỉ Ubuntu','H11: git show fa362fd (merge #865) và 4ae43f0; hunk thay gom windows bằng 23 job Ubuntu','Có'),
('Nguồn dự kiến của từng gate*','outputs.os + exclude + job-if','H8: python3 ../review_evidence/workflow_probe.py; cả 8 job gate* lấy matrix.os từ chuan-bi; in riêng từng exclude/job-if','Có'),
('t162 thực sự đánh giá biểu thức thật','push / PR thường / PR windows / từng runner_set','H2/H3/H4: --chi-ca=t162 1/1 đạt; AST 7985–8086; trace 13 lời gọi trên chính raw_expr; không chỉ so chuỗi tên ca','Có'),
('Kỳ vọng được assert bởi t162','push/PR thường Ubuntu; PR windows hai nền; dispatch theo runner_set','H4: so thân ca và trace: [U], [U], [U,W], dispatch absent/default [U,W], windows-only [W]; input windows-only không lọt sang 3 sự kiện không dispatch','Có'),
('Răng của t162 đối với output os','Đổi hành vi được assert thì ca đỏ','H4: 4 mutant giá trị (master, nhãn windows, bỏ windows-only, windows-only trả hai nền) đều t162 FAIL; t161 PASS','Có, trong các nhánh được assert'),
('t162 đại diện toàn bộ ma trận job','hành vi ấy được khoá; đọc ca ấy là đọc ma trận HIỆN HÀNH','H12: bỏ exclude Windows/mảnh1 hoặc bỏ job-if gom → t161 PASS/t162 PASS; checker riêng ci_dang_ky.loi_g5_workflow báo lỗi. t162 không đọc hai trường này','KHÔNG — P2 bên dưới'),
('t161 chỉ khoá cấu trúc','Nguồn os chung; output không fromJSON; không evaluator','H4: AST 7927–7981, 0 lời gọi evaluator; độc lập job.os và output fromJSON làm t161 FAIL; đổi hành vi os vẫn PASS','Có'),
('Trường nhãn và runner_id','Đọc labels của từng job, runner_id khác 0','H11: 23 job đều Ubuntu/nonzero; readback-jobs-39745387589 có 22 job runner_id=0, 0 bước, failure. Đây là metadata nhận runner; không thay log/assertions của job','Có trong các readback; không suy nonzero là mọi bước đã đạt'),
('Ảnh chụp 23-10 trên e63961f','push master/PR thường chỉ Ubuntu','H4: evaluator trên git show e63961f:.github/workflows/ci.yml và exact reviewed SHA đều [ubuntu-latest] cho hai context','Có; ngày người viết thực đo không xác minh độc lập'),
('Ảnh chụp dispatch','hai nền; windows-only chỉ Windows','H4/H8: cả hai commit [U,W] khi input vắng/windows-and-ubuntu; [W] khi windows-only; input choice/default ở YAML khớp','Có cho matrix os; job chuan-bi vẫn cố định Ubuntu'),
('Windows tự động trên push master','Chỉ launcher-windows.yml, có paths, lane launcher','H8: quét mọi workflow ở cả hai SHA; ci dispatch/nhãn mới có Windows, ci-dot-bien-du và ops-* chạy Ubuntu; launcher.push paths=[.claude/dev/**,.github/workflows/launcher-windows.yml], chỉ job launcher','Có'),
('launcher PR có điều kiện','nhãn windows, types có labeled','H8: launcher.pull_request.types=[opened,synchronize,reopened,labeled], paths=.claude/dev/**; job-if kiểm nhãn; trigger/matrix in đầy đủ','Có (đây là workflow launcher, không phải ci.yml)'),
('G5 Windows chỉ mảnh 0 từ #879','gate-cong-cu duyệt ca nền rồi dừng','H8: expand matrix loại W/mảnh1..7, còn W/0; AST main 8880–8974, nhánh manh/nt return trước _phan_manh và vòng đột biến','Có'),
('Ca thiếu năng lực bị loại mẫu số','so_ca = len(CA) - len(bo_qua)','H8: AST giả lập nt, 2 pass+1 skip → CA 2/2 tổng=3, rc=0; 1 failure → rc=1; all skipped → rc=1; precheck skip → rc=1','Có'),
('Gom không chạy Windows','gate-cong-cu-gop loại W; windows-only bị skipped theo if','H8: exclude=[{os:windows-latest}], job-if đòi Ubuntu trong outputs.os; matrix gom sau exclude chỉ [U]','Có về định nghĩa; skipped thực tế trên Actions KHÔNG ĐO ĐƯỢC'),
('Nhiều bước if theo runner.os','Có job Windows chưa bảo đảm mọi bước chạy','H8: liệt kê đúng 6 bước có runner.os tại cả hai SHA (3 job); conditions Windows/Linux khác nhau','Có'),
('Windows xanh không chứng minh bán kính','Chỉ ca không bỏ qua; lấy bán kính Ubuntu cùng head','H8: main nt không chạy vòng mutation; thông báo KHÔNG ĐO TRÊN WINDOWS; mô phỏng skip vẫn rc=0. Không có log Windows mới trong phiên này','Có, không khai đã chạy Windows thật'),
('Dispatch trên ref để yêu cầu Windows','workflow_dispatch, xem runner_set để bỏ phút Ubuntu','H4/H8: workflow có dispatch và input choice; windows-only bỏ U khỏi matrix, chuan-bi vẫn U; không kiểm billing hay kích hoạt Actions offline','Có về cấu hình, không bảo đảm hạ tầng/job thực tế luôn thành công'),
('Bẫy gắn nhãn của ci.yml (context giữ nguyên)','Không types; labeled không tự bắn','H8: ci.pull_request=None, launcher có types riêng; lịch sử #109 qua git log HEAD có 3736fc0/05170b4/9796f67 (H11)','Cấu hình có; mặc định Actions/raw finding P2 thứ hai không tái đo nền tảng offline'),
('Bước EOL ở master (context giữ nguyên)','PR head contains required EOL base skipped','H8: if=${{ github.event_name == pull_request }} ở bước EOL, push không thoả; không suy lượt PR không có skipped khác','Có về điều kiện; không chạy job thật'),
('Bổ sung sau landed, không sửa hồ sơ cũ','#891 head 0390130; comment 6366218495; chỉ thêm','H10: git show 8324567 ghi merge #891, cha2=0390130… và message dẫn comment; toàn bộ 146 dòng prefix bằng base và 0390130, thêm đúng 27 dòng','Có về Git/prefix; body comment owner không có raw readback'),
('Ngày đo bổ sung','2026-10-23 15:16Z / 15:16:09Z','H10: YAML khai đúng timestamp; readback/blob-file có ngày 23-10; không có transport receipt/đồng hồ độc lập của lần thu nhận','KHÔNG ĐO ĐƯỢC thời điểm thu nhận độc lập; không suy là sai'),
('Yêu cầu review lại','6366307732, ducthangho, 13:43:34Z, @codex review, sau #891','H10: parse JSON đúng id/login/created_at/body; git merge #891 13:39:35Z < request 13:43:34Z; body nhắc 094e8d1 running','Có'),
('Receipt không finding','6366338141, connector, 13:45:03Z, Reviewed commit: 6ac385fdd7','H10: parse JSON exact id/login/time/body; đúng Didn\'t find any major issues và short SHA','Có'),
('Summary connector nay hoàn tất','6360319005; 6ac385fdd7325f532ac4b4b6eb861292bfa7e970; completed; false; 13:45:05Z','H10: parse codex-review-state JSON: commit_sha/status/has_any_findings/has_unresolved_findings khớp; outer updated_at 13:45:05Z','Có'),
('Reaction +1, không eyes','connector 13:45:08Z','H10: reactions mới đúng 1 phần tử, content=+1, login connector, created_at=13:45:08Z; cũ eyes 08:00:12Z','Có trong snapshot, không gọi GitHub sống'),
('Connector sửa summary tại chỗ','Running 094e8d1 chỉ còn readback cũ','H10: cùng id/created_at, body/state đổi từ running 094e8d1 sang completed 6ac385f; new readback không còn trạng thái cũ','Có trong cặp snapshot; hiện trạng GitHub hôm nay KHÔNG ĐO ĐƯỢC'),
('Đối chiếu CLAUDE.md','094e8d1 và 6ac385f cùng blob 975cd94…','H10: git rev-parse 094e8d1:CLAUDE.md 6ac385f:CLAUDE.md; cả hai 975cd94ff851a3a0ee3aa0493e90184e5f81c874','Có; không đồng nhất hai commit'),
('Diff stat giữa head/merge cũ','Chỉ subagent_ghi_detect_test.py, land_evidence_nguon_test.py, thuộc #872/#877','H10: git diff --stat 094e8d1 6ac385f: 2 files, 77 insertions(+), 5 deletions(-); tất cả dòng stat khớp readback; git show 9d4cb6a/daf8961 xác nhận PR','Có'),
('Giới hạn và nợ mở','Chỉ bù về nội dung; không xoá chuyện merge trước review','H10: receipt/state gắn merge 6ac385f, không phải head 094e8d1; prefix/no_con_mo giữ nguyên; tệp bổ sung không tạo verdict cho head','Có; đây không phải re-review exact head 094e8d1'),
('Readback mới dùng tên mới; sum chỉ thêm','3 tệp mới, không ghi đè cũ','H9/H10: 14/14 checksum OK; git diff base head -- ops/land/ không có dòng nội dung bị xoá; +3 SHA256SUMS, các tệp cũ prefix nguyên','Có'),
('Validator hồ sơ và hai cổng bổ sung','land_evidence_nguon, doctrine-scan, doc-claims-check ok=true','H5/H6/H7: cả ba rc=0; doctrine sạch 10 tệp; doc-claims ok=true/flags=[]/381 advisory; land_evidence_nguon TỔNG: ĐẠT','Có'),
]
table='## BẢNG ĐO\n\nQuy ước: U = `ubuntu-latest`, W = `windows-latest`; Hn trỏ hướng đo có lệnh/output bên dưới. Các script nằm ngoài cây review và có thể chạy từ `cay-kho/` với `PYTHONDONTWRITEBYTECODE=1`. Tên nhánh không được dùng làm chuẩn.\n\n| khẳng định | PR khai | đo được (lệnh) | khớp? |\n|---|---|---|---|\n'
for row in rows:
    table+='| '+' | '.join(x.replace('|','\\|').replace('\n',' ') for x in row)+' |\n'
s=s[:s.index('## BẢNG ĐO')]+table+'\n'+s[s.index('## BẢNG SĂN'):]
s=s.replace('Đang kiểm tra từng khẳng định tại SHA được giao; chưa kết luận.','Các hướng được ghi tăng dần trong lúc đo. Hướng 14 lưu cả phép thử byte thô thất bại; hướng 15 giải thích và kiểm lại theo `.gitattributes`. Không che rc thất bại đó.')

# Keep the full JSON outside the prose, without losing the real stdout.
raw=(root/'review_evidence/6.log').read_text()
d=json.JSONDecoder().raw_decode(raw[raw.index('{'):])[0]
summary=json.dumps({k:d[k] for k in ('ok','files_scanned','flags','advisory_count','layers_skipped')},ensure_ascii=False,indent=2)
section='''HƯỚNG 6: Cổng doc-claims-check

  giả thuyết : SHA/tuyên bố tài liệu làm cổng kiểm claim đỏ hoặc ok khác true.

  lệnh       : `cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 scripts/tl.py doc-claims-check --json`

  output     : trích các trường từ JSON thật; stdout đầy đủ giữ nguyên trong [review_evidence/6.log](review_evidence/6.log).

```json
'''+summary+'''
```

  rc         : 0

  kết luận   : KHÔNG PHẢI LỖI — ok=true, flags=[], không có lớp bị bỏ; 381 advisory không làm gate fail. Cổng này không tự chứng minh claim nằm ngoài tập quy tắc.

'''
s=re.sub(r'(?ms)^HƯỚNG 6:.*?(?=^HƯỚNG \d+:|\Z)',lambda _:section,s,count=1)
s=s.replace('kết luận   : Đối chiếu rc và dòng kết luận ở output; đây là cổng được chỉ thị yêu cầu, không thay thế phép đo từng khẳng định.','kết luận   : KHÔNG PHẢI LỖI — rc=0; doctrine-scan sạch, 10 tệp, 0 chỗ chép doctrine.')
s=s.replace('kết luận   : Đối chiếu rc và summary; validation schema/nguồn không thay phép kiểm nội dung readback riêng.','kết luận   : KHÔNG PHẢI LỖI — rc=0, 1 ĐẠT, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC, TỔNG: ĐẠT; vẫn đối chiếu nội dung riêng ở H10.')
s=s.replace('kết luận   : Đối chiếu từng dòng OK và rc; kiểm băm trên tệp snapshot tại reviewed SHA, không xác minh nguồn GitHub sống.','kết luận   : KHÔNG PHẢI LỖI — 14/14 tệp OK, rc=0; đây là toàn vẹn snapshot, không phải kiểm GitHub sống.')
s=s.replace('kết luận   : Đối chiếu assertions và output: các measured có readback khớp; chưa chứng minh độc lập được nội dung comment quyết định #891 hay đồng hồ thu nhận readback. Không suy tương đương SHA từ cùng blob.','kết luận   : KHÔNG PHẢI LỖI với mọi measured có readback được trích — assertions đều đạt; body comment quyết định #891/đồng hồ thu nhận không có chứng cứ độc lập. Giữ giới hạn đó, không suy cùng SHA từ cùng blob.')
s=s.replace('kết luận   : Đối chiếu tất cả rc, hash blob, status gồm ignored và diff đầu vào; chỉ kết luận nguyên vẹn ở các mốc quan sát.','kết luận   : KHÔNG PHẢI LỖI nguồn — phép kiểm byte thô rc=1 do ba checkout cmd có CRLF theo attributes. Lệnh ở đây là bản script trước khi thêm xử lý attributes; giữ output thật và giải quyết ở H15.')

intro=f'''verdict: changes_requested
reviewed_sha: {sha}
Kết quả: 0 P0, 0 P1, 1 P2, 0 P3.

Review độc lập, chỉ đọc + đo, theo `runs/64761d8e/prompt.snapshot`; base `1ccc31498b7d37c12305e8f1b5bf2d1fc217b92e`, reviewed_tree `3da0ce24590dfcf2e60805b2bef76687cdd64405`.

Reviewer `codex`; provider `openai_codex`; execution_surface `codex_cli`; transport `machine`. Run `64761d8e6164462d870c3d534d325dd2`; header CLI khai `gpt-6.1-sol`, effort `xhigh`, session `01a16ec6-03c0-72c0-ac25-dccfeef0cd62` (đọc `runs/64761d8e/run.json` và đầu `stderr.log`; header không chứng minh model phục vụ ở máy chủ). Không có GitHub submitter vì không đăng/push. Sandbox khai `workspace-write`; read-only đối với `cay-kho/` được giữ bằng phạm vi lệnh, bytecode bị tắt. Không gọi mạng, không dùng subagent, không sửa nguồn review.

P2 ở `CLAUDE.md:171–173`: t162 được mô tả rộng hơn phạm vi phép đo; `exclude:`/`if:` cấp job nằm ngoài ca đó. `HINT.patch` chỉ sửa lời văn. Các số/SHA/readback còn lại khớp trong phạm vi đo; những dữ kiện GitHub không có raw snapshot được đánh dấu rõ, không nâng thành pass.

'''
s=intro+s[s.index('## BẢNG ĐO'):]
s+='''
### t162-khong-khoa-toan-bo-ma-tran-job [P2] Thu hẹp lời khẳng định về phạm vi của t162

TỆP/DÒNG: `CLAUDE.md:171–173` (tại reviewed_sha nêu đầu báo cáo).

VẤN ĐỀ: Gạch đầu dòng trước định nghĩa ma trận dự kiến là `outputs.os` cộng `exclude:` và `if:` cấp job. Gạch sau gọi **“hành vi ấy”** là thứ `t162` khoá, rồi kết luận **“đọc ca ấy là đọc ma trận HIỆN HÀNH”**. Nhưng `t162` chỉ lấy `jobs.chuan-bi.outputs.os` và assert các context của biểu thức đó; nó không đọc hai trường còn lại. Vì thế người chỉ đọc ca theo hướng dẫn vẫn bỏ sót phần quyết định Windows có chạy mảnh/gom hay không. Đây là khai rộng hơn phép đo (P2), không phải phát hiện gate tổng đang bỏ lọt cấu hình sai.

ĐÃ THỬ NGHIỆM: `cd cay-kho && PYTHONDONTWRITEBYTECODE=1 python3 ../review_evidence/test_scope_probe.py` (H12, rc=0). Baseline: t161 PASS, t162 PASS, `loi_g5_workflow=[]`. Trong bản sao YAML ngoài repository: bỏ duy nhất `{os: windows-latest, manh: 1}` khỏi exclude, hoặc bỏ `gate-cong-cu-gop.if`, đều t161 PASS/t162 PASS. Checker khác `ci_dang_ky_test.py:loi_g5_workflow` mới báo lỗi matrix/needs-if tương ứng. H4 cũng cho thấy các đột biến giá trị của output os thật đều làm t162 đỏ. Không nói toàn bộ gate còn xanh với các mutant exclude/if.

ĐỘ TIN: cao về phạm vi đọc/assert của ca và phản chứng; mức P2 do lời văn bao trùm quá phạm vi đó.

GỢI Ý VÁ: Sửa đúng `CLAUDE.md:171–173`, vì lỗi nằm ở hướng dẫn tìm nguồn. Nói rõ t162 khoá **riêng output os**, vẫn đọc exclude/job-if ở ci.yml; nếu muốn trỏ chốt G5 thì trỏ `loi_g5_workflow` trong `.claude/dev/ci_dang_ky_test.py` cho đúng hai job mảnh/gom. Không cần đổi mã test hay mở rộng ca t162 để vá lỗi tài liệu này. HINT kèm theo làm đúng phạm vi đó.

CA KHOÁ/PHẢN CHỨNG: Dùng H4/H12: mutant output os phải làm t162 đỏ; mutant exclude/if phải được checker đúng bắt, đồng thời chứng minh t162 không kiểm chúng. Sau chỉnh tài liệu, chạy hai cổng tài liệu bắt buộc và đọc đối chiếu lại source của từng con trỏ. Không thêm test chỉ so lại chính câu văn.

NGUY CƠ CỦA GỢI Ý: Con trỏ tới `loi_g5_workflow` có thể bị đọc quá rộng thành mọi gate*. Vì vậy HINT giới hạn rõ **phần mảnh/gom của gate-cong-cu***; ci.yml vẫn là nguồn phải đọc cho các job còn lại. Không sửa cấu hình gate hoặc hành vi chạy.

`HINT.patch`: định dạng `patch -p0` từ gốc `cay-kho/`, đã dry-run và áp thử trên scratch (H13, cả hai rc=0). **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**. Executor dùng hint cần khai `hint_provenance` theo protocol; đây chỉ là artifact đề xuất của reviewer.

## CỔNG VÀ GIỚI HẠN

- `python3 .claude/dev/packet_loop.py doctrine-scan --root .`: **passed, rc=0**, `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- `python3 scripts/tl.py doc-claims-check --json`: **passed, rc=0**, `"ok": true`, `flags=[]`, `layers_skipped={}`, 381 advisory; toàn bộ JSON ở `review_evidence/6.log`.
- `python3 ops/land_evidence_nguon.py --root . --tep ops/land/pr889-claude-md-bai-hoc-c-land-evidence.yaml`: **passed, rc=0**, `TỔNG: ĐẠT` (1 ĐẠT, 0 vi phạm, 0 KHÔNG ĐO ĐƯỢC).
- `sha256sum -c SHA256SUMS.txt` trong provenance: **passed, rc=0**, 14/14 OK. `t161` và `t162` chạy riêng: **passed, rc=0**, mỗi selector 1/1 đạt.
- Chưa chạy full gate/bán kính, Windows thật hoặc GitHub Actions mới (**not_run**). Không có mạng để xác nhận raw comment `r4323607674`, raw owner decision `6366218495`, finding thứ hai #109 hoặc trạng thái GitHub hiện tại (**not_measured**); commit message/correction chỉ là dấu vết đã lưu, không là raw API. Ngày giờ tác giả thu readback không có transport receipt độc lập. Không coi các giới hạn này là pass hoặc tự suy thành lỗi.
- Hướng 14 là **failed probe** do chưa xét eol=crlf, đã giải quyết ở H15; không phải gate sản phẩm fail. Ba cmd có CRLF đúng attributes; 5.200 blob byte thô và 3 blob qua chuẩn hoá đều khớp HEAD. Trước/sau: HEAD/tree không đổi, tracked/index diff rc=0, untracked/ignored rỗng. Các snapshot này chứng minh không có delta quan sát được, không khẳng định lịch sử không từng có ghi-hoàn-nguyên. Không sửa `cay-kho/`, không push, không gọi mạng.
'''
p.write_text(s)
print('VERDICT finalized:', len(s.splitlines()), 'lines;',len(rows),'measurement rows;',len(re.findall(r'^HƯỚNG \d+:',s,re.M)),'directions')
assert s.splitlines()[0]=='verdict: changes_requested'
assert s.splitlines()[1]=='reviewed_sha: '+sha
assert len(re.findall(r'^HƯỚNG \d+:',s,re.M))>=6
