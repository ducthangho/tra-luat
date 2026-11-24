import hashlib
import json
from pathlib import Path
import subprocess
import sys

W = Path(__file__).resolve().parent
R = W.parent / 'repo'
read = lambda p: json.loads(Path(p).read_text())
v = read(W / 'VERDICT.json')
previous = read(W.parent / 'lich_su/VERDICT_vong7_codex.json')
audit = read(W / 'audit_r8.json')
run = read(W.parent / 'run/e10bfd1d/run.json')
runtime6 = read(R / 'ops/reviews/wp1236-spec-r10-6-codex/run.json')
retained = read(W / 'unchanged_contracts.json')

v.update(status='complete', verdict='approve', findings=[], class_table=[])
v['class_table_scope'] = 'Chỉ lớp finding còn mở đối với ĐẶC TẢ r10 bản sửa 3. Không phát hiện finding mới. Lịch sử và nghĩa vụ mã chưa đóng giữ riêng đầy đủ trong prior_class_status; không xoá nợ để tạo approval mã.'
v['review_identity'] = {
    'provider': run['provider'], 'execution_surface': run['execution_surface'], 'transport': run['transport'],
    'run_id': run['run_id'], 'source': str(W.parent / 'run/e10bfd1d/run.json'),
    'role': 'independent_spec_reviewer', 'independence': 'Context được giao riêng theo assignment; không fork/tái dùng context Executor, không tạo subagent.',
    'model_phuc_vu': 'KHONG_DO_DUOC', 'effort_phuc_vu': 'KHONG_DO_DUOC',
    'reason': 'Launcher run.json đang dang_chay lúc đọc, chưa có kết luận đo serving model/effort; không suy từ tên tài khoản hoặc model được yêu cầu.',
    'sandbox_mode': 'workspace-write',
    'sandbox_limit': 'Cơ chế sandbox cho phép ghi repo/work; chỉ thị reviewer giới hạn mọi ghi của phiên này vào work. Không khai sandbox OS read-only.',
    'assurance': 'Verdict nội dung review đặc tả offline. Không tự cấp cross_approved, human_audited, lease hoặc quyền merge; receipt terminal của launcher do dispatcher đối chiếu sau run.'
}
v['preflight'] = {
    'repository': str(R), 'origin': 'https://github.com/ducthangho/tra-luat.git',
    'branch': 'detached HEAD', 'base_sha': '33b6803676b12fd069976dedb79f043a268c29c3',
    'reviewed_sha': v['reviewed_sha'], 'reviewed_tree': v['reviewed_tree'],
    'revision': 10, 'ban_sua': 3, 'vong': 8, 'generation': 'N/A — review đặc tả, không nhận lease thi công A/B/C',
    'authority': 'Chỉ thị trực tiếp của người dùng cho lượt review này; SPEC.md khớp byte git show HEAD:ops/specs/wp1236-r10.md.',
    'write_set': [str(W)], 'repository_write_set': [], 'network': 'not_run — theo chỉ thị cấm GitHub/mạng',
    'core_abbrev': 'Không có giá trị cấu hình (git config --get rc1); không sửa config. Chỉ dùng full OID, không chạy gate phụ thuộc short SHA.',
    'snapshot': 'preflight.json: tracked/index sạch, không untracked; ignored .codex/ đã có tại snapshot đầu, không tự coi ignored là thay đổi của packet.',
    'scope_limit': 'Không xác minh live lease/ref/comment/budget, không duyệt quyền thi công. E1 được nhận như dữ kiện và authority do người dùng cung cấp; không claim API readback.'
}

status = []
for old in previous['prior_class_status']:
    row = {k: old[k] for k in ['slug', 'finding_cu', 'vong_xuat_hien', 'status']}
    slug = row['slug']
    row['nguon'] = {'verdict': 'lich_su/VERDICT_vong7_codex.json', 'reviewed_sha': previous['reviewed_sha'], 'spec_sha256': previous['spec_sha256']}
    if slug in retained:
        lines = ', '.join(f"{x['current_lines'][0]}–{x['current_lines'][1]}" for x in retained[slug])
        row['evidence'] = f'Giữ DA_VA_THAT của vòng 7, không mở lại lớp. Kiểm độc lập các đoạn hợp đồng hiện tại SPEC.md:{lines}: nguyên văn xuất hiện trong spec tại 33b6803676b12fd069976dedb79f043a268c29c3; hash/đoạn ở unchanged_contracts.json. Bản sửa 3 không đổi chốt của lớp này.'
        row['chua_do_duoc'] = 'Không còn nghĩa vụ đặc tả cần đo thêm để GIỮ nhãn đã đóng. Không chứng nhận mã r10, Windows/CI, authority live hoặc land.'
        if slug == 'nang-tran-thieu-hop-dong-authority':
            row['evidence'] += ' Đã đo numstat r9 1+335+988=1324; trần mới 1700 vẫn ghi ĐỀ NGHỊ/CHỜ E2. Phương án thay thế dòng 439 nay tham chiếu luật 4 bắt buộc, phù hợp việc rút luật 3.'
    elif slug == 'so-do-khong-cung-pham-vi-nguon':
        row['evidence'] = 'audit_r8.json: 17 A1+13 A2=30 ca sàn; đủ m1…m50; 5 luật với 4 luật bắt buộc; kho 127 ID duy nhất; manifest 800, pilot đủ 927 ID/hash và phân hạng 764 GIET/153 SONG/10 VO_CAN, không LOI_CHAY. Numstat r9 1324 trên 3 tệp. SPEC:424–439 phân biệt số r9, ước r10, không coi 153/927 là ngưỡng bắt buộc. Không phát hiện delta làm hỏng lớp đã đóng.'
        row['chua_do_duoc'] = 'Không chạy lại pilot 927 đột biến; chỉ kiểm artifact/ID/hash và sinh manifest hai lần. Chưa có numstat mã r10; không tuyên bố 1700 chắc chắn đủ.'
    elif slug == 'nghiem-thu-khong-co-lap-chot-dich':
        row['finding_cu'] = row['finding_cu'] + ['X01']
        row['vong_xuat_hien'] = row['vong_xuat_hien'] + [7]
        row['status'] = 'VA_MOT_PHAN'
        row['evidence'] = [
            'X01: audit_r8.json chạy đúng bộ quét hiện tại trên 800 dòng manifest đã bỏ toàn bộ src, rồi chỉ giữ 1 src: cả hai rc2 KHONG_DO_DUOC, không HOAN_TAT; không còn mất 800/799 ID im lặng như phản chứng vòng 7.',
            'Luật 5: năm biến thể nguồn đều giữ đúng tập/thứ tự 127 ID. Nguồn gốc và đổi định dạng áp127/127 cùng hash; đổi tên local áp125+2 KHONG_AP_DUNG; mất/nhân đôi mọi neo cho0+127 KHONG_AP_DUNG kèm lý do. runtime_r8.json: Python3.12 giữ127 dòng với125 áp dụng+2 KAD; chay trên3.12 bị từ chối rc2.',
            'SPEC:303–317,329–342 giữ target/control, đúng TinHieuChotCa, ma trận trùng ID, ma trận miền và ledger đầy đủ mỗi ID trên exact head mới. SPEC:327–328 thêm quét độc lập của reviewer mã; survivor khác nghĩa là finding theo §8.',
            'SPEC:318–328,585 rút nghĩa vụ nghiệm thu luật3 theo E1 chủ kho. Theo protocol§8.3: cắt acceptance/đưa biểu hiện khỏi scope KHÔNG được tính là vá. Vì vậy không ghi DA_VA_THAT cho X01/toàn lớp dù không còn blocker của đặc tả đã thu hẹp.'
        ]
        row['chua_do_duoc'] = 'Chưa có mã r10 và ledger target/control của A/B/C; chưa chạy baseline/child terminal toàn bộ của bộ quét mới hoặc pilot927. Phần assurance bộ quét toàn diện đã rút khỏi acceptance, không chứng minh đã sửa hết; nghĩa vụ mã và hồi quy còn phải nghiệm thu.'
        row['scope_disposition'] = {'authority': '#1236 issuecomment-7053621494 theo chỉ thị trực tiếp người dùng và SPEC:318–328', 'kind': 'authorized_scope_reduction', 'count_as_fix': False, 'successor': 'review mã r10 A/B/C, luật1/2/4/5 + review độc lập; công cụ luật3 chỉ tham khảo'}
    elif slug == 'test-thieu-chot':
        row['status'] = 'VA_MOT_PHAN'
        row['evidence'] = 'Giữ alias sang nghiem-thu-khong-co-lap-chot-dich. SPEC:293–342,374,561–562 còn nghĩa vụ target đúng, sáu fixture CLI, ma trận miền, thứ tự hai lỗi và kho reviewer. Đo127 ID/hash trên nguồn gốc/định dạng và ID-preservation qua mất neo. Hợp đồng mới kiểm được, nhưng chưa có mã r10 để chứng minh L01/L02 đã sửa; E1 không miễn hồi quy.'
        row['chua_do_duoc'] = 'L01 P2/L02 P3 của MÃ r9 chưa có kết quả thực thi r10. Không chuyển thành finding đặc tả mới chỉ vì code tương lai chưa được viết; không approve code hay miễn P3.'
    elif slug == 'mo-ta-duong-dan-lech-hop-dong':
        row['status'] = 'VA_MOT_PHAN'
        row['evidence'] = 'SPEC:122–124,563 vẫn cho ./tệp ở A, chỉ cấm tuyệt đối/../symlink. dotpath_r8.json: chạy kiem_ho_so trên module đúng blob c2d606b với plain và ./ đều trả[]; docstring _tep_trong vẫn ghi cấm `.`/`..`. Bản sửa3 không sửa mã r9. Yêu cầu đặc tả đã rõ; chưa đóng L03 ở mã.'
        row['chua_do_duoc'] = 'Chờ mã r10 sửa docstring và reviewer mã xác nhận; không tính P3 L03 là đã đóng/được miễn, không mở P3 đặc tả lặp lại.'
    else:
        raise AssertionError(slug)
    status.append(row)
assert len(status) == 15
v['prior_class_status'] = status
v['prior_status_summary'] = {'DA_VA_THAT':12,'VA_MOT_PHAN':3,'CHUA_VA':0,'KHONG_DO_DUOC':0,
                            'canonical_unresolved_classes':2,'note':'test-thieu-chot là alias giữ nguyên, không đếm đôi.'}
v['bang_noi_slug'] = previous['bang_noi_slug']
v['bang_noi_slug'][0]['phep_doi_chieu'] = 'Giữ nguyên phép nối lịch sử. Đối chiếu cùng127 ID, luật1/2/4/5 và L01/L02; X01 không được đổi slug khi luật3 rút scope. Không có tách/gộp mới ở vòng8.'
history = dict(previous['hoi_tu']['lich_su_giu_nguyen'])
history['ma4_sang_5'] = 'KHONG_DO_DUOC'
history['vong6_sang_7'] = '0/2'
v['hoi_tu'] = {
    'vong7_sang_8':'0/2','U':['nghiem-thu-khong-co-lap-chot-dich','mo-ta-duong-dan-lech-hop-dong'],'F':[],
    'lop_lap_lan_ba':previous['hoi_tu']['lop_lap_lan_ba'],'lop_moi':[],'lop_tai_mo':[],
    'lich_su_giu_nguyen':history,
    'dinh_chinh':'ma4_sang_5 = KHONG_DO_DUOC; 0/1 trong verdict vòng6/7 là chép sai vì verdict mã4–5 không có slug. Không dùng số sai để suy hội tụ.',
    'giai_thich':'Giữ U cuối vòng7 sau alias; thu hẹp luật3 không là DA_VA_THAT và L03 chưa sửa mã. Tỷ lệ0/2 phản ánh lịch sử chưa đóng, không phủ định khả năng approve ĐẶC TẢ sau quyết định E1 có phạm vi mới. Không dùng approval này để reset call/round budget hoặc cấp phép review tiếp.',
    'checkpoint':'Hai chuyển tiếp6→7 và7→8 cùng0/2; giữ stop/checkpoint§12 và lịch sử lặp. Hướng mới đã được chủ kho chọn E1; lượt này chỉ đánh giá thiết kế mới, không tự mở vòng vá hoặc gọi reviewer khác.'
}
v['round6_identity_correction'] = {'model_phuc_vu':'KHONG_DO_DUOC','effort_phuc_vu':'KHONG_DO_DUOC',
    'source':'ops/reviews/wp1236-spec-r10-6-codex/run.json',
    'model_phuc_vu_trang_thai':runtime6['model_phuc_vu_trang_thai'],
    'effort_phuc_vu_trang_thai':runtime6['effort_phuc_vu_trang_thai'],
    'note':'Không nâng thành DO_DUOC từ các sự kiện gpt-6-astra đọc được; biên nhận vòng6 đã đính chính.'}

v['acceptance_assessment'] = {
    'ket_luan':'Đủ rõ và kiểm được ở mức đặc tả với reviewer đọc nghĩa độc lập; không là bảo đảm tự động đầy đủ của một scanner.',
    'thuc_kiem_doc_lap':[
        {'luat':1,'vi_tri':'SPEC:293–295,303–313','kiem':'Mỗi lý do/nhánh đầu ra có ca đúng lý do, healthy control, mutant gỡ đúng chốt; kill chỉ từ TinHieuChotCa của ca đích. Đối chiếu ca/mutant, không lấy rc hay lỗi khác làm tín dụng.'},
        {'luat':2,'vi_tri':'SPEC:314–317','kiem':'Năm ô trùng ID: provenance, job/job, skipped/skipped, skipped/job, job/skipped. Mỗi ô có control và mutant riêng; skipped kiểm lý do job_lap.'},
        {'luat':4,'vi_tri':'SPEC:329–334','kiem':'Ma trận miền nghĩa và route consumer: A hàm lá+kiem_ho_so; head!=None kiểm kiem_mien trực tiếp và C/D2b; B/L8; hai lỗi đồng thời để phân biệt thứ tự.'},
        {'luat':5,'vi_tri':'SPEC:335–342','kiem':'Bắt đầu từ127 ID có băm đã ghim, không từ tập src áp dụng được. Mỗi ID phải có GIET đúng ca, TUONG_DUONG có chứng minh mới, hoặc KAD kèm replacement cùng nghĩa GIET/CHOT_DA_BO có chứng minh. Cộng dồn ID mới các lượt sau; rc0 hoi-quy không là nghiệm thu.'},
        {'luat':'reviewer độc lập','vi_tri':'SPEC:327–328; PROTOCOL§8/8.3','kiem':'Reviewer tự chọn phản chứng ngoài ví dụ/minimum và ngoài scanner. Survivor không tương đương thành finding theo severity, không được bỏ chỉ vì ngoài manifest hoặc không có HOAN_TAT.'}
    ],
    'counterexamples_decided':[
        '127/127 dòng nhưng tất cả KAD không đạt luật5 nếu không có disposition từng ID; phép đo no_anchors/duplicate_anchors xác nhận inventory còn nguyên.',
        '125 áp dụng trênPython3.12 không được báo127 GIET; hai ID KAD vẫn phải tái dẫn xuất/chứng minh. Python pin ở do/chay, hoi-quy không pin; đây là khác biệt biểu diễn có ledger, không còn mất nghĩa vụ.',
        'HOAN_TAT của do không chứng minh ledgerKAD, target assertion hoặc không còn survivor ngữ nghĩa; bộ chạy hiện vẫn lọc KAD ra kq tại dòng301. Do đã advisory, nghiệm thu phải kiểm ledger ngoài kq theo luật5. Không công nhận đây là sửa xong mọi phần X01.',
        'Thay TinHieuChotCa bằng lỗi import/TypeError, chỉ kiểm tổng suite hoặc để chốt khác bắt thay vi phạm luật1 trực tiếp; nhãn GIET từ công cụ không ghi đè luật này.'
    ]
}
v['law3_consistency_scan'] = {
    'result':'Không tìm được câu hiện hành buộc chạy/đạt scanner luật3 trái với việc thu hẹp.',
    'scope':'Toàn bộ585 dòng SPEC.md; các hit lưu audit_r8.json/law3_reference_scan, đọc trong ngữ cảnh thay vì chỉ grep.',
    'decisions':[
        'Dòng300: năm luật nhưng nêu rõ3 khuyến nghị,1/2/4/5 bắt buộc. Dòng318–328 là nghĩa hiện hành.',
        'Dòng379–382 (bất kỳ đột biến nào sống) nằm trong tiêu chí tệp test đợtA, giữ sàn ca/mutant và kill đúng lý do; không nói mọi mutant sinh bởi scanner luật3 phải chết. Đọc cùng318/324 không tạo yêu cầu HOAN_TAT.',
        'Dòng424–430:927/153 là sốpilot r9 và danh sách việc ước lượng; không còn ngưỡng0 sống sạch của scanner.34 cặp là34 survivor kho trongpilot, không rút ledger từ127 xuống34.',
        'Dòng439 nay ghi luật4, không còn giữ điều kiện luật3 ở phương án táchA2.',
        'Dòng478 nói quét hệ thống trong bảng hình dạng kế thừa; phù hợp lượt quét độc lập327. Dòng553/561/570/578 ghi cách xử lý các vòng trước; không tái kích hoạt luật3 khi318 và585 đã thay thế. Cụm(g)–(l) ở561 là tham chiếu lịch sử, không trần reviewer hoặc nghĩa vụ hiện hành.',
        'Docstring công cụ còn chữ ĐO CHÍNH THỨC(luật3+5); đây là nhãn command của artifact tham chiếu. Không có authority vượt câu không phải điều kiện nghiệm thu của đặc tả. Không review/phê duyệt toàn bộ công cụ như mã cổng.'
    ]
}
v['counts_and_budget'] = {
    'A_cases':30,'A1':17,'A2':13,'matrix_laws':5,'mandatory_laws':[1,2,4,5],'advisory_law':3,
    'numbered_mutants_floor':50,'bank_ids':127,'pilot_inventory':927,'pilot_counts':audit['pilot']['counts'],
    'pilot_bank_survivors':34,'pilot_bank_non_equivalent_survivors_historical':25,
    'r9_numstat':{'files':3,'added':1324,'parts':{'module':335,'test':988,'registration':1}},
    'r10_measured_size':'KHONG_DO_DUOC','r10_estimate':'~1550–1650; ước công sức, không phải số đo hoặc bảo đảm đủ',
    'nang_tran':{'current_declared':1400,'proposed':1700,'files':3,'status':'CHỜ E2','location':'SPEC:432–440'},
    'assessment':'Nhất quán với bản sửa3: scope hẹp không bắt buộc phải giảm trần đề nghị.1700 là headroom dự kiến cho nghĩa vụ ca/ledger và survivor khác nghĩa được reviewer tìm ra; không tự cho phép dùng1700 hoặc làm tròn numstat đo thật.',
    'authorization_limit':'Không đo lại toàn bộ chi phí/call budget qua GitHub theo chỉ thị cấm mạng; không tự cấp thêm lượt hay budget. E2/E5 và lease thi công vẫn riêng.'
}

v['da_do_khop'] += [
    {'phep_do':'Hồi quy/manifest/đếm vànumstat','command':'python3 -B work/audit_r8.py','rc':0,'ket_qua':'passed','artifact':'audit_r8.json','positive_evidence':'127 ID được giữ ở5 biến thể;800 manifest lặp cùnghash;927pilot đúngID/hash;30ca;50IDmutant;1324dòngr9'},
    {'phep_do':'Python3.12 hoi-quy','command':'/usr/bin/python3.12 -B quet_dot_bien.py hoi-quy <bank> - <module> --ra work/python312_regression.jsonl','rc':0,'ket_qua':'passed','artifact':'runtime_r8.json','positive_evidence':'127dòng=125AP_DUNG+2KAD, đúngtậpID'},
    {'phep_do':'Python3.12 chay bị từ chối','command':'/usr/bin/python3.12 -B quet_dot_bien.py chay <manifest> <test> --goc <module> --ra <kq>','rc':2,'ket_qua':'passed','artifact':'runtime_r8.json','positive_evidence':'KHONG_DO_DUOC: can Python(3,13); rc2 là kết quả âm mong đợi, không khai runnerpass'},
    {'phep_do':'Bảo toàn hợp đồng lớp đã đóng','command':'Python so23đoạn SPEC với git show33b6803:ops/specs/wp1236-r10.md','rc':0,'ket_qua':'passed','artifact':'unchanged_contracts.json','positive_evidence':'11lớp có hợp đồng giữ nguyên; lớp sốđếm kiểm riêng audit_r8.json'},
    {'phep_do':'L03 plain/dotpath trên module r9','command':'importlib load exact c2d606b module; kiem_ho_so plain và./','rc':0,'ket_qua':'passed','artifact':'dotpath_r8.json','positive_evidence':'plain=[];dot=[];docstring cũ vẫn ghi cấm dấu chấm — xác nhận nghĩa vụ mã còn mở'}
]
v['validation_scope'] = {
    'passed':['spec hash/blob/OID/tree','inventory hoi-quy nguyên vẹn','phản chứng thiếu src bị từ chối','tính lặp manifest','đối chiếu pilot artifact','đếm/numstat r9','so hợp đồng giữ nguyên','dotpath đọc r9'],
    'failed':[], 'skipped':[],
    'not_run':['mã r10 A/B/C (chưa có)','baseline/child terminal và full927pilot của scanner mới','full selftest/release','Ruff pin/probe','bare Ruff lint','Windows local/CI','GitHub/readbackauthority','LIVE/merge/deploy'],
    'note':'Không chạy gate của mã sản phẩm vì nhiệm vụ là review đặc tả. Không biến phép đo hỗ trợ trên mã r9 thành pass mã r10. Phân biệt rc2 âm mong đợi với lỗi test.'
}
v['severity_decision'] = {
    'current_spec_open':{'P0':0,'P1':0,'P2':0,'P3':0},
    'reason':'Approve nội dung đặc tả theo phạm vi E1 do chủ kho giao; không phát hiện P3 để tự ghi nợ hoặc xin miễn. Các trạng thái VA_MOT_PHAN giữ cho lớp lịch sử/mã tương lai, không đổi thành DA_VA_THAT và không phải approval mã có P2/P3 mở.',
    'not_authorized':['thi công không lease','nâng trần1700 trướcE2','miễnL01/L02/L03','merge/land/deploy','resetbudget']
}

(W / 'VERDICT.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('VERDICT_WRITTEN',len(v['prior_class_status']),'prior rows',len(v['findings']),'current findings')
