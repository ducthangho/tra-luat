import pathlib,json,hashlib,subprocess,platform,sys,collections
R=pathlib.Path(__file__).resolve().parent.parent/'repo';W=R.parent/'work';B=R.parent/'bang_chung'
v=json.loads((W/'VERDICT.json').read_text());a=json.loads((W/'remaining_audit.json').read_text());la=json.loads((W/'luat9/audit.json').read_text())
v.update(status='complete',reviewed_tree='5474259bbb71e3be6e3f7d3eaf4661142906ca0d',base_sha='f602325574c62184caf16309631f5f680ca5cee2',previous_sha='d5a7d8510af03e0d08545f677ad5de687e0264f4',revision=12,generation=1)
v['identity']={'provider':'openai_codex','execution_surface':'codex_cli','transport':'machine/local','model':'KHONG_DO_DUOC','effort':'KHONG_DO_DUOC','effort_requested':'high','run_id':'845189ec5e834d1ba278b0b6c0b854c7','evidence':'../run/845189ec/run.json: thuc_thi_duong_dan=/opt/node22/lib/node_modules/@openai/codex/bin/codex.js; wrapper local_process/subprocess/machine. Không suy model/effort từ tên lượt.','independence':'Context reviewer mới được cấp riêng; không thực thi packet, không fork context executor, không subagent.'}
v['environment']={'python':sys.version,'os':platform.platform(),'additional_python':'/usr/bin/python3.12 = 3.12.3','sandbox':'workspace-write; approval never; network restricted','repository_read_only':'Ràng buộc vận hành; mọi ghi thử nghiệm ở work/. Sandbox workspace-write không phải bằng chứng chặn ghi vật lý vào repo.'}
v['preflight']={'head_tree_spec':'Khớp snapshot_before.json; SPEC.md và blob f602325:ops/specs/wp1236-r12.md cùng SHA256 đã giao.','lease':'wp1236-c-r12-g1-claude-20261124; r12/g1; lease_expires_at_utc=2026-11-27T11:22:26Z; review lượt 5/6 theo prompt. Không đọc GitHub theo yêu cầu offline.','review_class':'sensitive','effective_write_set':['.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py'],'numstat':'+429/-13; 2 tệp; trần +450 đạt','branch':'detached HEAD được giao','base_ancestry':subprocess.run(['git','merge-base','--is-ancestor',v['base_sha'],v['reviewed_sha']],cwd=R).returncode,'origin_master':'Không có ref origin/master trong checkout được cấp; không sửa checkout. Phép đo corpus dùng bản bare scratch với ref tổng hợp tại candidate, chỉ kiểm semantics dữ liệu, không chứng nhận remote authority.','core_abbrev':'Chưa pin (git config --get core.abbrev rc1). Không đo golden/full gate cần short SHA.'}
source='Lượt4 d5a7d8510af03e0d08545f677ad5de687e0264f4; lịch sử lượt1/2/3 giữ nguyên.'
v['prior_class_status']=[
 {'slug':'archive-loc-mat-du-lieu-kiem','status':'VA_MOT_PHAN','nhan_protocol':'VÁ HỜ','source':source,'evidence':'models.json: case/nfc/backslash dưới mô hình tep từ rc0 ở d5a7d85 thành rc12; probe_behavior: YAML link rc12; prior_directory.log: collision rc8 cả hai mô hình. C05 còn lọt tên chứa dấu chéo ngược native ở 3.13.18 và 3.12.3.','chua_do_duoc':'Không đo lại Windows native; chưa dựng được link chuẩn hoá tới tệp nhưng thực tế tới thư mục.'},
 {'slug':'symlink-tren-dia-lech-cay','status':'VA_MOT_PHAN','nhan_protocol':'VÁ HỜ','alias_of':'archive-loc-mat-du-lieu-kiem','source':source,'evidence':'Giữ ánh xạ lớp đã gộp từ lượt4. Ma trận C4 baseline36 không lệch; alias trong probe cũ bị chặn. Không đếm thành lớp mở thứ hai; C05 giữ lớp nguyên nhân chung.'},
 {'slug':'hop-dong-dau-ra-duong-dan-tu-do','status':'DA_VA_THAT','nhan_protocol':'ĐÃ VÁ THẬT','source':source,'evidence':'behavior.json: newline_passed và newline_waived đều rc12 duong_dan_sai; targeted.log 17/17 gồm miền ký tự; more.json giữ chẩn đoán một dòng; không đổi bộ regex trong lượt5.'}]
v['prior_findings']=[
 {'id':'C03','disposition':'ĐÃ VÁ THẬT các phản chứng cụ thể lượt4; lớp chung chưa đóng','evidence':'probe_models.py nguyên văn SHA256 38b06b30aa86d31f2264c69462da7bb2e3ab8e8c38e2f65697a19975e7930065; case/nfc/backslash previous tep0 -> head tep12. Plain đều12. C05 là biểu hiện khác cùng lớp.'},
 {'id':'C04','disposition':'Hành vi cũ CHƯA ĐỔI; không còn chặn theo cùng tiêu chí cũ vì chủ kho đã siết K2. Không ghi thành bản vá mã.','evidence':'models.json: missing/file_parent previous và head đều rc12 plain/tep. Dạng chuẩn hoá tới thư mục bị cấm bởi luật mới. Quyết định 7180063460 thay acceptance cũ; giữ lịch sử, không tính việc đổi luật thành đóng cả lớp.','authority':'#1236 issuecomment-7180063460 (prompt được giao; không xác minh mạng)'}]
v['class_table'] += [{'slug':'hop-dong-dau-ra-duong-dan-tu-do','manifestations':['C02 lượt1: LF trong đường dẫn passed/waived'],'highest_open_severity':None,'source':source,'common_fix':'Giữ miền ASCII được owner chốt trước mọi đọc/in.','closing_check':'behavior.json newline_passed/newline_waived rc12 duong_dan_sai, targeted.log c5_mien_ky_tu đạt.'}]
v['class_table'][0]['source']=source
v['class_table'][0]['alias_slugs']=['symlink-tren-dia-lech-cay']
v['hoi_tu']={'luot4_sang_5':'0/1','F':0,'U':1,'count_unit':'Lớp mở chuẩn, alias symlink-tren-dia-lech-cay không đếm hai lần. Hai finding cũ cùng một lớp; lớp vẫn mở do C05.','lop_lap_lan_ba':['archive-loc-mat-du-lieu-kiem'],'history':[1,2,4,5],'decision':'Lượt5 thực hiện đổi kiến trúc theo quyết định chủ kho 7180063460, trần6 theo 7170968907. Không tự cấp lượt6, không reset lớp/budget.'}
v['m3_windows']={'classification':'required','independently_run':False,'status':'not_run','reported_evidence':'Prompt và handoff: issuecomment-7180853548, exact 8aab9da, Python3.12.10, base118/118 head135/135, không skip; C4 gồm lk4/lk6/lk7/lk8..lke và lk5. Reviewer không đo lại hay kiểm receipt GitHub.','new_finding_scope':'C05 đã đo Linux native; không khẳng định Windows native cùng đường tên literal-backslash. Windows không chứng minh loại trừ input POSIX.','ci_windows':'Chủ kho miễn theo lease/prompt; không biến not_run thành passed.','model_limit':'Mô hình tep/NFC chỉ mô phỏng semantics; không khẳng định NTFS chuẩn hoá NFC.'}
sample_file=W/'luat9/sample-results.jsonl'
assert sample_file.exists(),'sample still running'
sample=[json.loads(s) for s in sample_file.read_text().splitlines()]
receipt=json.loads((W/'luat9/receipt.json').read_text());assert receipt['rc']==0
v['luat9']={'delta':la,'sample':{'receipt':receipt,'baseline_passed':len(sample[0].get('baseline_ca_dat',[])),'count':len(sample)-1,'classifications':dict(collections.Counter(r['phan_hang'] for r in sample[1:])),'ids':[r['id'] for r in sample[1:]],'evidence':'luat9/sample.log, sample-results.jsonl; không khai chạy lại toàn bộ228.'},'executor_artifacts':'Đã đối chiếu khối trích, tái sinh manifest228 khớp, ledger byte-identical 225 GIET +3 TUONG_DUONG; log do có HOAN_TAT và đúng neo. 234/234 đột biến khai báo là log executor; reviewer chạy độc lập17 d2b_k2,7 ma trận riêng và mẫu AST.','equivalence':['g:_d2b_kiem:44:49: thêm ~ cuối ref không thay startswith refs/remotes/origin/.','i7:_d2b_kiem:30:90: SHA_RE có ^ và \\Z nên match/fullmatch tương đương.','j1:_d2b_kiem:31:23: YAML cung cấp kiểu builtin; type(ra)==int tương đương is int trong miền đó.'],'inheritance':{'independent':'14 ca legacy trên base/head đều14/14; corpus71 dòng byte-identical; 17 ca mới đạt.','executor_AB':'Log/bảng executor:1784->1801 ca,38skip mỗi vế;2009->2075 mutants,1skip và r1187_spec_packet_type đỏ cả hai. Chỉ audit artifact, không tự chạy full A/B.','pool':'kho_rong.jsonl rỗng là miền D2b mới, không thay nghĩa vụ không hồi quy.'},'ngoai_bang_dong':'Không phát hiện mutant sống ngoài manifest. probe_more.py cũ tạo ngoài-import tarfile và đo GIET; không có P3 sống. C05 là vi phạm hành vi trên mã nguyên bản, không phân hạng thành P3 test ngoài bảng.'}
v['design_review']=[
 {'point':'cây con','result':'Cách đọc chặt hơn cả cây oid nhưng được điều phối đồng ý trong prompt. Có0 mục120000 trong ops/land HEAD (10084 mode100644,2 mode100755). Corpus71 kết quả trước/sau đồng nhất; không thấy chặn oan hồ sơ hiện có. Không suy từ71 lên76 của master mới chưa được cấp.'},
 {'point':'chuẩn hoá văn bản','result':'paths hai runtime: ./, //, sub/.. native rc8 do data-filter đổi bytes; mô hình giữ nguyên link sau kiểm an toàn cho rc0. missing/file/chain trước .. cũng rc0 trong mô hình, nhưng lstat/exists chứng minh link hỏng, không phải thư mục. Không dựng được đường xuyên symlink thư mục thật mà mọi link vẫn thoả danh sách; không tuyên bố đã đo trên mọi nền.','reasoning':'Trong miền POSIX và tên được bảo toàn, đi qua một symlink ở thành phần giữa đòi nó phân giải thành thư mục. Tất cả symlink trong inventory đều phải chuẩn hoá tới tệp; chuỗi/vòng hỏng không tự tạo thư mục. Đây là lập luận kèm mô hình, không chứng minh Windows/macOS.','wording_limit':'Câu mọi đích hỏng bị chặn phải hiểu theo phép chuẩn hoá đã chọn: link hỏng nhưng chuẩn hoá trúng tệp có thể qua trên nền giữ văn bản. Không gọi phép đo native rc8 là ca dương. C04 cũ chuẩn hoá ra thư mục vẫn rc12.','evidence':'paths-3.13.18.json, paths-3.12.3.json; retained_safe_link_text ghi rõ exists/is_file/is_dir.'},
 {'point':'mode','result':'Mã gán mọi mode ngoài040000/120000 thành f, không tự whitelist100644/100755. mode100755 được đo rc0. Gitlink thật160000 bị inventory chặn rc8 trước membership (modes.json); không có đường gitlink qua đã đo. Ca gitlink ban đầu paths*.json không giữ mục160000 và chỉ là missing-target rc12; không dùng làm bằng chứng gitlink.'},
 {'point':'K2','result':'Siết đã được chủ kho giao. lk5/non-YAML regular vẫn rc0; YAML link tới regular vẫn do module trả symlink12. C05 cho thấy điều cấm backslash chưa được thực thi toàn bộ.'}]
v['law_matrix']=[
 {'rule':'Thư mục và gốc bản bung','evidence':'matrix_names.log baseline36; targeted C4; lk4/lk6/lk7 rc12 dưới mô hình tep.','result':'đạt trong phạm vi đo'},
 {'rule':'Bí danh khác hoa/thường/NFC và đồng dạng','evidence':'models.json case/nfc; paths*.json case/nfd/homoglyph rc12.','result':'đạt trong phạm vi đo'},
 {'rule':'Đích chứa dấu chéo ngược','evidence':'paths*.json literal_backslash native0; modes.json ba biến thể0.','result':'C05 P2'},
 {'rule':'Đích hỏng/không tồn tại','evidence':'lkb, nonutf_missing rc12; noncanonical retained model có rc0 khi normpath trúng tệp.','result':'Xem giới hạn chuẩn hoá ở design_review, không khẳng định mọi link hỏng đều12'},
 {'rule':'Ngoài cây con và symlink khác','evidence':'lkc/lkd rc12; từng cho_ten bị ChotB4 riêng.','result':'đạt'},
 {'rule':'Tên byte không UTF8','evidence':'paths hai runtime: surrogateescape exact raw-ff rc0, target raw-fe không khớp rc12.','result':'So str là song ánh byte trong runtime Linux đã đo; không thấy nới tên'},
 {'rule':'Tệp100644/100755 và link lồng','evidence':'paths regular/executable/nested rc0; modes gitlink8.','result':'đạt trong phạm vi đo; C05 áp cả executable/nested'},
 {'rule':'export-ignore','evidence':'paths export_ignore rc8; C4 an_tep_bang_export_ignore.','result':'fail-closed ở inventory'},
 {'rule':'Đích rỗng','evidence':'paths empty rc8 trên cả3.12/3.13 do không dựng được link/bản bung.','result':'Chặn tại lỗi đo, không phải rc12 của membership'},
 {'rule':'Đích tuyệt đối hoặc thoát gốc','evidence':'Không soạn payload; mô tả: join giữ absolute, không thể trùng inventory relative; data-filter có thể ném trước guard.','result':'not_run; không khai đã đo'},
 {'rule':'Thứ tự báo lỗi D2b và YAML','evidence':'modes symlink_before_k1 rc12 với lý do symlink; yaml_link rc12; C3 nhiều lỗi/neo theo targeted17/17.','result':'giữ thứ tự hiện có'}]
v['da_do_khop']=[
 {'check':'Preflight và diff','status':'passed','rc':0,'command':'git rev-parse HEAD HEAD^{tree}; sha256 SPEC/blob; git diff --numstat/--check f602325 HEAD','evidence':'snapshot_before.json; +429/-13 trong450; exact write set'},
 {'check':'17 cong_d2b_*','status':'passed','rc':0,'command':json.loads((W/'targeted.receipt.json').read_text())['command'],'evidence':'targeted.log:17/17, không skip'},
 {'check':'17 d2b_k2_*','status':'passed','rc':0,'command':json.loads((W/'declared_k2.receipt.json').read_text())['command'],'evidence':'declared_k2.log:17 GIET đúng ChotB4, oan=[]'},
 {'check':'36 biến thể ×7 cho_ten','status':'passed','rc':0,'command':json.loads((W/'matrix_names.receipt.json').read_text())['command'],'evidence':'matrix_names.log:baseline0lệch, mỗi mutant đúng1biến thể ChotB4'},
 {'check':'Probe lượt4','status':'passed','rc':0,'command':'PYTHONDONTWRITEBYTECODE=1 TMPDIR=work/tmp python3 -B work/probe_models.py; probe_behavior.py; probe_more.py; do_probe_l2.py repo','evidence':'models.json,behavior.json,more.json,prior_directory.log'},
 {'check':'Probe collision gốc với assertion lịch sử','status':'failed','rc':1,'command':'python3 -B work/probe_case_directory.py','evidence':'prior_directory_original.log: assertion đòi trạng thái dễ lọt của lượt2 đã lỗi thời; phiên bản đo không assert cho rc8/8. Không tính đây là regression.'},
 {'check':'C05 conformance oracle','status':'failed','probe_rc':0,'command':'PYTHONDONTWRITEBYTECODE=1 python3 -B work/probe_paths.py; /usr/bin/python3.12 -B work/probe_paths.py; python3 -B work/probe_modes.py','evidence':'paths*.json,modes.json: đòi12, gate0. Process probe0 chỉ là đo hoàn tất.'},
 {'check':'Legacy14 base/head và corpus71','status':'passed','rc':0,'command':'PYTHONDONTWRITEBYTECODE=1 python3 -B work/audit_remaining.py','evidence':'remaining_audit.json; ref scratch tổng hợp, không chứng nhận remote'},
 {'check':'Corpus với origin/master thật của checkout','status':'not_measured','rc':1,'command':'do_kho_that.py <script> repo origin/master <tsv>','evidence':'real_previous.log,real_head.log: git rev-parse origin/master rc128. Không thêm ref vào checkout.'},
 {'check':'Luật9 mẫu','status':'passed','rc':0,'command':receipt['command'],'evidence':'luat9/receipt.json,sample-results.jsonl,audit.json'},
 {'check':'Bare Ruff F hai tệp','status':'failed','rc':1,'command':'python3 -m ruff check --no-cache --select F --output-format json <packet_loop.py> <packet_loop_test.py> (base và head)','evidence':'ruff_receipts.json;16 lỗi mỗi vế;remaining_audit.json delta0 sau bỏ số dòng trong message F811; Ruff0.15.15'},
 {'check':'Ruff delta và pin/probe contract','status':'passed','rc':0,'command':'remaining_audit.py; runpy ci_dang_ky_test.py loi_ruff_ci()','evidence':'ruff_contract.log:RUFF_CONTRACT3[]; delta new=[] removed=[]'},
 {'check':'Full suite reviewer/Windows/CI mạng/LIVE','status':'not_run','rc':None,'evidence':'Ngoài phép đo offline được giao; không lấy log executor làm tự chạy'},
 {'check':'Executor skipped','status':'skipped','rc':None,'evidence':'38ca và1mutant mỗi vế trong bảng A/B; không tính pass'}]
v['limits']=['Không GitHub/mạng; authority theo prompt,lease,bundle được giao. Không xác minh biến động master/heartbeat ngoài bundle.','M3 native và full A/B là lời khai của điều phối/executor, tách khỏi kiểm độc lập.','Snapshot đầu/cuối chứng minh trạng thái Git và hash hai tệp không đổi, không chứng minh chưa từng có write rồi hoàn nguyên; ignored .codex/ có sẵn, không có attestation byte snapshot đầu của toàn bộ ignored.','Phép đo corpus71 trên candidate khác corpus76 ở1260fa0 của executor; không tráo hai miền.','Không tự đóng/miễn P3, approve, merge,land,push; C05P2 chặn approval.']
# Recheck exact candidate and worktree without mutating repository.
before=json.loads((W/'snapshot_before.json').read_text());after={}
for k,val in before.items():
 if isinstance(val,dict) and 'cmd' in val:
  p=subprocess.run(val['cmd'],cwd=R,capture_output=True);after[k]=dict(cmd=val['cmd'],rc=p.returncode,stdout=p.stdout.decode(errors='surrogateescape'),stderr=p.stderr.decode(errors='surrogateescape'))
 else:after[k]=json.loads(json.dumps(val))
for p in after['tracked_hashes']:after['tracked_hashes'][p]=hashlib.sha256((R/p).read_bytes()).hexdigest()
(W/'snapshot_after.json').write_text(json.dumps(after,ensure_ascii=True,indent=2));v['snapshot_equal']=before==after
assert v['snapshot_equal'];assert subprocess.check_output(['git','rev-parse','HEAD'],cwd=R).decode().strip()==v['reviewed_sha']
v['artifact_sha256']={str(p.relative_to(W)):hashlib.sha256(p.read_bytes()).hexdigest() for p in [W/n for n in ['models.json','behavior.json','modes.json','paths-3.13.18.json','paths-3.12.3.json','targeted.log','declared_k2.log','matrix_names.log','remaining_audit.json','snapshot_before.json','snapshot_after.json','luat9/sample-results.jsonl','luat9/audit.json','probe_paths.py','probe_modes.py']]}
(W/'VERDICT.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
md=f'''Review độc lập lượt 5, đợt C wp1236 r12/g1 — **changes_requested**.

`reviewed_sha`: `{v['reviewed_sha']}`  
Tree: `{v['reviewed_tree']}`  
Base: `{v['base_sha']}`  
Spec SHA256: `{v['spec_sha256']}`.

**C05 — P2 — archive-loc-mat-du-lieu-kiem** tại `.claude/dev/packet_loop.py:3988–3990`.

Chốt mới chưa thực thi điều cấm “đích chứa dấu chéo ngược”. Trên POSIX, một tệp thường có thể mang chính byte đó trong tên. Khi symlink trỏ đúng tên ấy, `normpath` giữ nguyên, membership đạt, CLI trả rc 0, in `D2b ĐẠT` và `ĐÓNG ĐƯỢC WP`, trái kỳ vọng rc 12 `kiem_tep:not_measured:symlink` của luật được giao. Đã đo trên mã nguyên bản, Linux Python 3.13.18 và 3.12.3; không mô phỏng OS cho phản chứng này.

Quét cùng lớp: tên lá chứa dấu chéo ngược, thành phần thư mục chứa dấu đó, tệp mode100755 và symlink lồng đều lọt. Bằng chứng: `paths-3.13.18.json`, `paths-3.12.3.json`, `modes.json`; script tái hiện là fixture vô hại trong scratch, không phải patch sản phẩm. Không khẳng định Windows native cũng nhận tên literal này.

Hướng sửa: kiểm điều cấm trên đích thô trước chuẩn hoá, giữ phép so byte với tệp thường; không đổi dấu chéo ngược thành `/` hoặc gộp case/NFC. Khoá bằng ca cho từng biến thể trên và đột biến bỏ riêng điều cấm, cạnh đối chứng regular/executable/nested rc0 và YAML link rc12. Đề xuất là mô tả hướng, không có patch gate.

Đối chiếu lượt trước:

- `archive-loc-mat-du-lieu-kiem`: **VA_MOT_PHAN**. C03 case/NFC/backslash-alias của probe cũ: d5a7d85 rc0 → HEAD rc12 dưới mô hình tep. C05 còn mở cùng lớp.
- `symlink-tren-dia-lech-cay`: **VA_MOT_PHAN**, giữ alias của lớp trên, không đếm thành lớp mới.
- `hop-dong-dau-ra-duong-dan-tu-do`: **DA_VA_THAT**; LF ở cả passed/waived rc12 `duong_dan_sai`.
- C04: hành vi missing/file_parent trước `..` không đổi (rc12 ở cả hai head), nhưng quyết định chủ kho7180063460 đã siết K2 và thay tiêu chí cũ. Không gọi đổi acceptance là vá mã hay đóng cả lớp.

Hội tụ lớp lượt4→5: **0/1**; `lop_lap_lan_ba` vẫn chứa `archive-loc-mat-du-lieu-kiem`. Giữ lịch sử1/2/4/5 và trần6, không tự cấp vòng tiếp theo.

Các phép đo:

- 17/17 ca `cong_d2b_*` đạt, không skip; 17/17 `d2b_k2_*` bị đúng ca đích giết, đối chứng sạch.
- Ma trận36×7: baseline0 lệch; mỗi `cho_ten_lk8…lke` bị đúng một biến thể ChotB4 bắt. Các kết quả xanh này không phủ C05.
- Luật9 tái sinh228 mục khớp artifact, ledger225 GIET+3 TUONG_DUONG khớp byte; mẫu độc lập{len(sample)-1} mục: {dict(collections.Counter(r['phan_hang'] for r in sample[1:]))}, baseline16/16, rc0. Không khai chạy lại toàn bộ228/234.
- Legacy14/14 trên base và head. Corpus71 hồ sơ trong candidate cho cùng kết quả:51 đạt,10 failed,10 not_measured. `ops/land` có0 symlink. Ref origin/master thiếu trong checkout; phép so corpus dùng ref tổng hợp trong bản bare scratch, không chứng nhận remote authority hay76 hồ sơ của master mới.
- Ruff0.15.15: cả hai vế rc1,16 lỗi nền; delta0, pin/probe contract3 kiểm tra đạt. Diff +429/−13, đúng2tệp, trong trần450; `git diff --check f602325 HEAD` rc0. Snapshot Git và hash hai tệp trước/sau không đổi.

Bốn quyết định thiết kế: phạm vi cây con chặt hơn nhưng đã được điều phối đồng ý, không thấy chặn oan corpus hiện có. Mode100755 qua; gitlink160000 thật bị inventory chặn rc8. K2 non-YAML regular vẫn rc0, YAML link do module chặn12; symlink trước lỗi K1 vẫn là lý do đầu. Với đường không chuẩn tắc, native3.12/3.13 ra8 do filter đổi byte; mô hình giữ văn bản sau kiểm an toàn cho phép cả link hỏng chuẩn hoá trúng tệp, nhưng chưa dựng được đường phân giải thành thư mục. Vì vậy không tuyên bố mọi link hỏng đều bị chặn hoặc đã chứng minh mọi nền. Đích tuyệt đối chỉ phân tích bằng lời, không soạn payload; đích rỗng đo được rc8, không gọi là rc12 của membership.

M3 Windows **required**, reviewer **not_run**. Bằng chứng base118/118→head135/135, Python3.12.10, các biến thể lk4…lke là lời khai điều phối trong prompt/handoff, không phải phép đo của reviewer. Không dùng mô hình Linux để khẳng định NTFS chuẩn hoá NFC. Full A/B là log executor:38 ca và1mutant skipped mỗi vế; `r1187_spec_packet_type` đỏ sẵn ở cả hai. Không nâng skipped/not_run thành pass.

Identity: `openai_codex / codex_cli / machine/local`, run `845189ec5e834d1ba278b0b6c0b854c7`; model/effort phục vụ `KHONG_DO_DUOC`, effort yêu cầu high. Sandbox workspace-write, repository được giữ read-only theo thao tác; mọi artifact trong work/. Không gọi mạng/GitHub, không sửa/commit/push repository.

CHƯA ĐỦ ĐIỀU KIỆN MERGE: C05 P2 còn mở. Đây là verdict nội dung offline trên exact SHA, không cấp quyền merge/land.

KET_LUAN: changes_requested
'''
(W/'VERDICT.md').write_text(md,encoding='utf-8')
print('WROTE VERDICT.json and VERDICT.md')
