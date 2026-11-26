from pathlib import Path
import json, hashlib, subprocess, re, sys, platform, unicodedata
root=Path.cwd(); area=root.parent; w=area/'work'; history=area/'lich_su/luot4'
def read(p): return json.loads(p.read_text())
def dump(p,d): p.write_text(json.dumps(d,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
prior=read(history/'VERDICT.json'); static=read(w/'static-checks.json'); before=read(w/'snapshot-before.json')
suites=read(w/'suite-receipts.json'); other=read(w/'other-checks.json'); compat=read(w/'compat-receipts.json')
assert all(x['rc']==0 for x in suites+other+compat)
for x in suites:
 s=Path(x['log']).read_text()
 for pattern in [r'CA: (\d+)/(\d+) dat',r'DOT BIEN: (\d+)/(\d+) bi giet dung ly do']:
  m=re.search(pattern,s); assert m and int(m[1])==int(m[2])>0
 assert 'TU KIEM PHAN HANG: DAT' in s and 'TONG: DAT' in s
 x['status']='passed'; x['positive_evidence']=s.strip().splitlines()
for x in other: x['status']='passed'
assert all(x['equal'] for x in static['products'].values())
cmds=[]
for c in [['git','rev-parse','HEAD','HEAD^{tree}'],['git','status','--porcelain=v1','--untracked-files=all','--ignored=matching'],['git','diff','--binary'],['git','diff','--cached','--binary'],['git','diff','--check',prior['base_sha'],'HEAD']]:
 p=subprocess.run(c,capture_output=True,text=True); cmds.append({'command':c,'rc':p.returncode,'stdout':p.stdout,'stderr':p.stderr}); assert p.returncode==0
assert cmds[0]['stdout'].splitlines()==[prior['reviewed_sha'],prior['reviewed_tree']]
assert cmds[1]['stdout']=='!! .codex/\n' and cmds[2]['stdout']==cmds[3]['stdout']==''
files={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in root.rglob('*') if p.is_file() and '.git' not in p.relative_to(root).parts}
delta=[k for k in set(files)|set(before['files']) if files.get(k)!=before['files'].get(k)]
assert not delta,delta
dump(w/'snapshot-after.json',{'commands':cmds,'files':files,'delta':delta})
sha=prior['reviewed_sha']; slug='nghiem-thu-khong-co-lap-chot-dich'
waiver={'status':'owner_waived','reviewed_sha':sha,'class_slug':slug,'finding_ids':['R4-01','R4-02'],'literal':f'mien_p3: {sha} {slug}',
 'source':'https://github.com/ducthangho/tra-luat/issues/1539#issuecomment-7197313309',
 'provenance':'Trích dẫn trong prompt.snapshot do điều phối cung cấp, ghi hộ lựa chọn chủ kho “Miễn 2 P3, đi tiếp (Recommended)”. Reviewer không gọi GitHub, không tự kiểm tác giả hoặc nội dung comment online. K5 kiem-merge phải đọc lại dòng miễn trên GitHub.',
 'debt_ids':['BO-SINH-BAT-BIEN-R4-01-danh-tinh-mien-doi-so','BO-SINH-BAT-BIEN-R4-02-danh-tinh-128-ascii']}
classes=prior['class_table']
for row in classes:
 row['source_round']=4;row['source_sha']=sha;row['highest_open_severity']=None
 if row['slug']==slug:
  row['status']='VA_MOT_PHAN';row['disposition']='owner_waived';row['waived_finding_ids']=['R4-01','R4-02'];row['note']='Trạng thái kỹ thuật giữ VA_MOT_PHAN; cả hai biểu hiện còn lại được miễn cho SHA này, không khai là đã vá.'
 else: row['disposition']='closed_by_prior_evidence_same_sha'
prior_status=[{'slug':slug,'status':'VA_MOT_PHAN','disposition':'owner_waived','source_round':4,'source_sha':sha,
 'finding_status':[{'id':f,'status':'CHUA_VA','disposition':'owner_waived'} for f in ['R4-01','R4-02']],
 'evidence':waiver,'note':'Giữ nhãn kỹ thuật theo bốn giá trị validator §8.3; miễn là disposition riêng. Không còn P3 mở chặn review trên SHA này.'},
 {'slug':'nghiem-thu-thoi-gian-chua-dat','status':'DA_VA_THAT','source_round':4,'source_sha':sha,
 'evidence':{'path':str(history/'VERDICT.json'),'samples':prior['prior_class_status'][1]['evidence']['samples'],
 'comparison':'prior-comparison.json: HEAD/tree trùng lượt 4; kế thừa năm cặp đã đạt (A 3/3, B 2/2). Không chạy lại benchmark ở lượt 5; suite lượt 5 chạy song song, không dùng thời gian để xét SPEC §4.'}}]
not_run=[
 {'name':'Luật 9 SPEC §5.8 trên exact SHA','status':'not_run','reason':'Theo điều phối executor đang chạy, chưa có kết quả. Đòi đủ base/head cả A/B, scanner ghim, không GIET-base sang hạng khác ở head; giữ nợ SONG/VO_CAN riêng.'},
 {'name':'CI GitHub, gồm Windows CI','status':'not_run','reason':'Review offline không gọi mạng.'},
 {'name':'M9 ci-dot-bien-du.yml','status':'not_run','reason':'Diff ops/**/*.py; do điều phối cung cấp sau.'},
 {'name':'Connector review','status':'not_run','reason':'Không gọi GitHub/connector trong lượt này.'},
 {'name':'Audit uỷ quyền và readback authority/K5','status':'not_run','reason':'Không xác minh comment miễn, tác giả, receipt hoặc quyền merge trên GitHub.'},
 {'name':'M3 Windows local độc lập bởi reviewer','status':'not_run','reason':'Chỉ ghi nhận lời khai điều phối về Windows; không có phép đo Windows của reviewer.'},
 {'name':'ci_dang_ky_test, selftest, Ruff pin/probe contract và benchmark base/head lượt 5','status':'not_run','reason':'Lượt xác nhận chỉ chạy các lệnh được yêu cầu; bằng chứng lượt 4 giữ nguyên nhãn. Selftest lượt 4 failed cả base/head 1773/1789, delta ID đỏ 0; không suy N/N pass.'}]
scan=[
 {'risk':'Cache che chốt sản phẩm','result':'Không thấy P0–P2. _bo_sinh_nho giữ chính function+args; đổi hàm giả tách key. YAML cache chỉ bao safe_load/safe_dump của test, không bao nap_yaml/SafeLoader hay main→L8 của sản phẩm. Mỗi đầu vào c36 vẫn main→L8; compile cache key chứa byte nguồn. Scanner _mot tạo subprocess mới từng mutant.', 'evidence':['compat312.json','compat313.json',str(history/'cache-review4.json'),'ops/land_evidence_nguon_test.py:838-901','ops/land_evidence_nguon.py:278-319','ops/reviews/wp1236-r10-soan/quet_dot_bien.py:263']},
 {'risk':'Phản chứng tự xanh trên mọi đầu vào','result':'Không thấy P0–P2. c39/c40/a136 đòi rc3 và đúng DO của ca đích cho âm, rc0 cho controls; c39 còn đòi 0 hoặc 648 ô. c38 giữ 24 biến thể. Trace lượt 4 cùng SHA: 68 âm đúng rc3/DO, 10 control đích xanh, 13 lượt A xanh, 0 rc4; không chạy lại quét đột biến sâu.', 'evidence':['suite-A.log','suite-B.log',str(history/'trace-v2.json')]},
 {'risk':'AST đọc nguồn trên CI/Windows','result':'Các lời gọi hiện tại là literal được ast.literal_eval hỗ trợ; đọc UTF-8 tường minh, LF/CRLF trả cùng năm bộ trên cả hai Python. Nguồn không đọc/parse được dẫn rc4/HONG, không false pass. Phép CRLF chạy Linux, không thay M3 Windows.', 'evidence':['compat312.json','compat313.json',str(history/'ast-failure.json')]},
 {'risk':'Python 3.12/3.13 và Unicode','result':'Đã đo cùng code bộ sinh/check/AST/cache: Python 3.12.3 Unicode15.0 và Python3.13.18 Unicode15.1 cho cùng codepoint/category tại cả năm bộ; miền 5, controls đạt, bộ sinh giả bị bắt sau warm cache. Không chạy full suite 3.12.', 'evidence':['compat-receipts.json','compat312.json','compat313.json']}]
reviewer={'provider':'openai_codex','execution_surface':'codex_cli','transport':'machine/local','model_family':'openai','run_id':read(area/'run/26c64248/run.json')['run_id'],'session_id':'01a218a2-de9f-7042-a63d-5bca1ceb748c','cli':'0.172.0','declared_model':'gpt-6-astra','declared_effort':'high','served_model':'KHONG_DO_DUOC','served_effort':'KHONG_DO_DUOC','sandbox':'workspace-write','identity_sources':[str(area/'run/26c64248/run.json'),str(area/'run/26c64248/stderr.log')],'note':'Executable codex.js và header đo được; header không chứng minh model/effort thực phục vụ từng request. Run chưa terminal khi viết verdict; điều phối phải ghi rc/hash stdout sau kết thúc.'}
m3={'classification':'required','basis':'ADR-0060 M3.2: added read_text(encoding=...)','status':'not_run','reported_by_dispatcher':{'status':'reported_passed_not_independently_verified','sha':sha,'host':'DESKTOP-T9R33P2','source':'https://github.com/ducthangho/tra-luat/issues/1539#issuecomment-7196524386','B':'40/40 ca; 145/145 đột biến','A':'53/53 ca; 149/149 đột biến','land_evidence_nguon':'ĐẠT','ci_dang_ky_test':'1654/1654','selftest':'1788/1789 cả hai vế; cùng ca đỏ r380_llm_khai_niem_bien_dau_vao; delta 0'},'limits':'Giữ nguyên lời khai. Số A149 của trích dẫn khác số Linux trong log lượt này; reviewer không có raw Windows receipt để đối chiếu nên không chứng nhận M3/Windows green.'}
v={'reviewed_sha':sha,'reviewed_tree':prior['reviewed_tree'],'base_sha':prior['base_sha'],'spec_sha256':prior['spec_sha256'],'revision':1,'generation':1,'vong':5,'review_class':'sensitive','findings':[],'class_table':classes,'prior_class_status':prior_status,'verdict':'approve','reviewer':reviewer,
 'authority':{'mode':'offline assignment + supplied excerpts','review_extension':'https://github.com/ducthangho/tra-luat/issues/1539#issuecomment-7197354187','calls':'5/5, thêm đúng một lượt xác nhận cùng SHA; không mở vòng sửa/quét sâu','waiver':waiver,'lease_until':'2026-11-27T20:55:00Z','limits':'Không kiểm trạng thái lease/authority online; không tự nhận quyền merge/land.'},
 'preflight':{'head_tree_matches_round4':True,'spec_git_blob':'a47f5bfb9648181f489a20d59c326caf300ab1ef','spec_source_oid':'d22fe11f9bf35517c70333c567481be460173eee','spec_path':'ops/specs/bo-sinh-bat-bien-r1.md','write_set':['ops/gate_output_doi_chieu_test.py','ops/land_evidence_nguon_test.py'],'numstat':'+274 -9; 2 files; limit 320 additions','core_abbrev':7,'checkout':'detached HEAD','status':'tracked/untracked/index sạch; ignored .codex/ có sẵn và không đổi','evidence':['snapshot-before.json','snapshot-after.json','static-checks.json','prior-comparison.json']},
 'checks':suites+other,'compatibility_checks':compat,'quick_class_scan':scan,'m3_windows':m3,
 'pham_vi_e':{'E1':'khong','E2':'khong','E3':'khong','E4':'khong','E5':'khong','basis':'Diff chỉ hai tệp test; không đổi điều kiện hồ sơ land của sản phẩm, lease/merge authority, secrets, LIVE.','coordination':'Gia hạn review lên 5/5 do chủ kho theo trích dẫn, không phải thay phạm vi E của diff.'},
 'luat9':{'status':'not_run','product_byte_identical':static['products'],'executor_report':'đang chạy, chưa có kết quả theo điều phối','acceptance':not_run[0]['reason']},'not_run':not_run,
 'historical_checks':{'source':str(history/'VERDICT.json'),'same_sha':True,'performance':'DA_VA_THAT: 5/5 cặp đúng trần; không tái đo','selftest':'failed: base/head 1773/1789, cùng ID đỏ, delta 0; không đổi thành passed','ci_dang_ky_test':'passed trong lượt 4, không tự chạy lại lượt 5','R3-01_R3-02':'DA_VA_THAT theo evidence lượt 4 cùng SHA; phần thiếu R4-01/R4-02 được miễn, không khai là vá.'},
 'environment':{'python':sys.version,'platform':platform.platform(),'unicode':unicodedata.unidata_version,'ruff':'0.15.15','PYTHONDONTWRITEBYTECODE':'1','TMPDIR':str(w/'tmp')},
 'limits':['Lời miễn P3, gia hạn 5/5 và Windows receipt là đầu vào điều phối, không tự xác minh tác giả comment; K5 phải đo lại miễn trên GitHub.','Review approve chỉ cho mã exact SHA, không chứng nhận đủ điều kiện merge, land hoặc Mission complete.','Không phát hiện P0–P2 mới trong một lượt quét nhanh toàn diff; không bảo đảm tuyệt đối không có lỗi. Không mở finding P3 mới hoặc lặp quét sâu lượt 4.','Sandbox workspace-write; tuân thủ chỉ đọc checkout. Snapshot 18703 tệp đầu/cuối chỉ chứng minh không delta tại hai mốc, không chứng minh toàn lịch sử I/O. Repo nguồn ngoài checkout không quan sát.','Thời gian hai suite lượt 5 chạy song song và có probe nhẹ khác nên không dùng kết luận hiệu năng. R3-03 kế thừa evidence cùng SHA lượt 4.','CRLF/Unicode probe trích đúng định nghĩa cần kiểm, chạy Linux; không phải full suite Python3.12 hay Windows.','Model/effort thực phục vụ KHONG_DO_DUOC; không suy từ actor đăng verdict. Terminal rc và stdout hash của launcher cần điều phối hoàn tất sau lượt chạy.'],
 'merge_readiness':'CHƯA ĐỦ ĐIỀU KIỆN MERGE: Luật 9, CI, M9, connector, audit uỷ quyền/readback K5 và xác minh evidence Windows thuộc các bước còn lại.'}
dump(w/'VERDICT.json',v)
lines=['# Review mã bo-sinh-bat-bien r1 g1 — lượt 5 xác nhận','',
'**approve** cho mã trên exact SHA dưới đây. Không phát hiện P0/P1/P2 mới qua một lượt đọc toàn diff. Hai P3 còn lại của lượt 4 đã được chủ kho miễn theo trích dẫn điều phối cung cấp; không có finding mở mới.','',
f'HEAD `{sha}` · tree `{prior["reviewed_tree"]}` · base `{prior["base_sha"]}`.',
f'SPEC SHA-256 `{prior["spec_sha256"]}`; revision 1, generation 1, sensitive. Blob `{v["preflight"]["spec_git_blob"]}` tại OID `{v["preflight"]["spec_source_oid"]}` khớp byte bản SPEC được cấp.','',
'Diff đúng hai tệp write set, +274/−9, trong trần 320. HEAD/tree trùng lượt 4; cả hai module sản phẩm byte-identical base. `git diff --check` rc 0. Tracked/untracked/index sạch; ignored `.codex/` có sẵn. Snapshot đầu/cuối 18703 tệp, 0 delta.','',
'Reviewer `openai_codex / codex_cli / machine/local`; run `'+reviewer['run_id']+'`, session `'+reviewer['session_id']+'`. CLI 0.172.0 công bố gpt-6-astra/high; model/effort thực phục vụ `KHONG_DO_DUOC`. Sandbox `workspace-write`, không phải mount chỉ đọc. Linux, Python 3.13.18, Unicode 15.1, Ruff 0.15.15, core.abbrev=7.','',
'Đối chiếu lượt trước:','',
'| Lớp / finding | Trạng thái kỹ thuật | Disposition lượt 5 |',
'| --- | --- | --- |',
'| nghiem-thu-khong-co-lap-chot-dich — R4-01, R4-02 | VA_MOT_PHAN; hai P3 CHUA_VA | owner_waived trên exact SHA |',
'| nghiem-thu-thoi-gian-chua-dat — R3-03 | DA_VA_THAT | Kế thừa 5/5 cặp đo đạt lượt 4 cùng SHA |','',
'R3-01/R3-02 giữ kết luận đã vá trong phạm vi đã kiểm lượt 4. Giữ toàn bộ stable slug và finding IDs. `VA_MOT_PHAN` là nhãn kỹ thuật theo validator, không phải P3 mở còn chặn sau miễn. Không đổi miễn thành “đã vá”.','',
'Nguồn miễn: '+waiver['source']+'. Nguyên văn trong prompt:','',
'```text',waiver['literal'],'```','',
'Đây là trích dẫn do điều phối cung cấp, ghi hộ lựa chọn chủ kho. **Tôi không tự kiểm được tác giả hoặc nội dung comment trên GitHub.** K5 `kiem-merge` phải đọc lại dòng miễn. Hai nợ giữ tên `'+waiver['debt_ids'][0]+'` và `'+waiver['debt_ids'][1]+'`. Quyền thêm đúng lượt xác nhận 5/5 theo '+v['authority']['review_extension']+' cũng là đầu vào điều phối.','',
'Các phép chạy lại trong lượt này:','',
'| Lệnh | rc | Bằng chứng dương |',
'| --- | ---: | --- |']
for x in suites:
 lines.append('| `'+ ' '.join(x['command'])+'` | 0 | '+'; '.join(x['positive_evidence'])+' |')
lines += ['| `python3 -B ops/land_evidence_nguon.py --root .` | 0 | 153 ĐẠT; 25/28 miễn trừ; 0 vi phạm; 0 không đo được; tổng 178; TỔNG: ĐẠT |',
'| `python3 -m ruff check --no-cache --select F` hai tệp, riêng base/head | 0 / 0 | All checks passed; delta 0 |','',
'Lệnh, cwd, rc thật, thời gian và SHA-256 log nằm trong `suite-receipts.json`, `other-checks.json`, `static-checks.json`; output gốc ở các tệp `.log`. Bare Ruff lint không thay pin/probe contract. Không có required check skipped nào được đổi thành pass.','',
'Quét nhanh toàn diff theo lớp:','']
for row in scan: lines.append('- **'+row['risk']+'**: '+row['result'])
lines += ['',
'Probe tương thích: `compat_probe.py` với `python3.12 -B` và `python3 -B`, đều rc 0; raw kết quả và hash trong `compat-receipts.json`. Năm miền có cùng codepoint/category giữa Python 3.12.3/Unicode15.0 và 3.13.18/Unicode15.1; CRLF giống LF. Không lặp bảng đột biến sâu lượt 4.','',
'R3-03 không đo lại: A 3/3 delta −0.543/−4.855/−3.727 giây (trần +5), B 2/2 delta +7.572/+0.709 giây (trần +30), từ evidence lượt 4 đúng SHA. Thời gian suite song song lượt 5 không dùng xét hiệu năng.','',
'M3 vẫn **required** do dòng `encoding=` thêm mới. Chỉ ghi nhận điều phối báo Windows DESKTOP-T9R33P2 đạt trên SHA này (comment 7196524386): B40/40·145/145, A53/53·149/149, land ĐẠT, ci_dang_ky_test1654/1654, selftest1788/1789 hai vế cùng ca đỏ `r380_llm_khai_niem_bien_dau_vao`, delta0. Không tự xác minh biên nhận; số A149 trong lời khai khác số Linux trong log lượt này. Không chuyển lời khai thành bằng chứng Windows do reviewer đo.','',
'Phạm vi E1–E5 đều `khong` theo diff: chỉ hai tệp test, không đổi sản phẩm hoặc lease/merge authority.','',
'`not_run`: Luật 9 trên SHA này (executor đang chạy, chưa kết quả); CI/Windows CI; M9; connector; audit uỷ quyền/readback authority K5; Windows local bởi reviewer. Không chạy lại ci_dang_ky_test, selftest, pin/probe contract và benchmark trong lượt xác nhận. Selftest lịch sử lượt 4 vẫn **failed** 1773/1789 cả base/head, delta ID đỏ0; không khai thành pass. Các mục này không đổi verdict review mã thành changes_requested theo assignment.','',
'**CHƯA ĐỦ ĐIỀU KIỆN MERGE:** thiếu xác minh Luật 9, CI, M9, connector, audit uỷ quyền/readback K5 và evidence Windows. Approval này không cấp quyền push/merge/land, không tự tạo receipt hoàn tất.','',
'Snapshot chỉ chứng minh hai mốc, không chứng minh chưa từng ghi rồi hoàn nguyên. Không gọi mạng; không quan sát repo nguồn ngoài checkout. Điều phối cần chốt rc terminal và hash stdout của launcher sau khi lượt chạy kết thúc.','',
'Validator và hash hiện vật được lưu riêng trong `kiem_verdict.txt`, `artifact-receipts.json`.','',
'KET_LUAN: approve']
(w/'VERDICT.md').write_text('\n'.join(lines)+'\n',encoding='utf-8')
c=['python3',str(area/'kiem_verdict_lop.py'),str(w/'VERDICT.json'),'--vong','5']; p=subprocess.run(c,capture_output=True); (w/'kiem_verdict.txt').write_bytes(p.stdout); (w/'kiem_verdict.stderr').write_bytes(p.stderr)
assert p.returncode==0 and b'HOP_LE' in p.stdout,(p.returncode,p.stdout,p.stderr)
a={'validator':{'command':c,'rc':p.returncode,'stdout':p.stdout.decode()},'artifacts':{}}
for n in ['VERDICT.json','VERDICT.md','kiem_verdict.txt']:
 q=w/n;a['artifacts'][n]={'bytes':q.stat().st_size,'sha256':hashlib.sha256(q.read_bytes()).hexdigest()}
dump(w/'artifact-receipts.json',a)
print(p.stdout.decode(),end='');print(json.dumps(a,ensure_ascii=False,indent=2))
