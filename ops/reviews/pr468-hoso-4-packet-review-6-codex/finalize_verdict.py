from pathlib import Path
import datetime, hashlib, json, re
BASE=Path(__file__).resolve().parents[1]; O=BASE/'do-review'; P=BASE/'VERDICT.md'
old=P.read_text()
findings=re.findall(r'^### ([a-z0-9-]+)  \[(P[123])\]  ([^\n]+)\n(.*?)(?=^#{2,3} |\Z)',old,re.M|re.S)
assert len(findings)==11,len(findings)
assessment=old.split('## Đánh giá chất lượng câu hỏi §12 — không chọn thay chủ kho\n',1)[1].split('\n### Ghi nhận:',1)[0].removesuffix('\nverdict: dang-do\n').strip()
st=json.loads((O/'static-audit.json').read_text());contracts=json.loads((O/'contracts.json').read_text());extra=json.loads((O/'extra-checks.json').read_text());attack=json.loads((O/'attack-h-summary.json').read_text());real=json.loads((O/'real-results.json').read_text());nr=json.loads((O/'nhanh-rerun.json').read_text());spawn=json.loads((O/'spawn-counts.json').read_text())
R=[]
def add(claim,pr,got,ok='có'):
    def esc(x):return str(x).replace('|','&#124;').replace('\n','<br>')
    R.append('| '+' | '.join(map(esc,(claim,pr,got,ok)))+' |')
add('Exact HEAD / tree','2adb6819caee0225d7b7e4f0c4e8c16f2faa7e73','HEAD đúng; tree c3c7bdaba867463ca33123025d7ac999b58fb6a3')
add('Môi trường git','core.abbrev=7; không shallow; cây sạch','7; false; status --porcelain rỗng trước/sau')
stat=[x.split('\t') for x in st['diff_numstat'].splitlines()]
add('Phạm vi diff d28c4b1→reviewed SHA','numstat.txt và diff.patch; thuần ops/',f"{len(stat)} tệp; +{sum(int(x[0]) for x in stat)}/−{sum(int(x[1]) for x in stat)}; cả 2 hiện vật khớp git diff từng byte; không có runtime diff")
add('doctrine-scan','rc=0, 7 tệp, 0 chỗ chép','rc=0, 7/0; 06:17:56Z')
add('adr-song','rc=0, 46/46','rc=0, 46/46; có ngoại lệ ADR0016 thiếu trạng thái')
add('doc-claims-check --strict --json','rc=0, ok=true, advisory=367','rc=0, ok=true, 106 tệp, claims_flagged=advisory_count=367')
add('ci_dang_ky_test.py không --chay','rc=0, 51/51','rc=0, PHẢN CHỨNG 51/51, TỔNG ĐẠT')
add('packet_loop_test / lease_publish_test trên exact HEAD','EVIDENCE chưa chạy lại; biên bản khai delta0 trên 7eb1145','KHÔNG ĐO ĐƯỢC delta lịch sử; không chạy lại hai suite trong lượt này','chưa xác minh')
labels={'GATE':'gate-tach','LO':'lo-319','2A':'mutant-windows-subagent','2B':'mutant-windows-nhanh'}
for label,prefix in labels.items():
    l=next(x for x in st['leases'] if x['file'].startswith(prefix))
    add(f'SHA-256 đặc tả {label}',l['declared_spec_sha256'],l['actual_spec_sha256'])
    add(f'Bản sao spec {label} / write set / dependency','khớp spec–lease',f"bản sao bằng byte; {len(l['write_set'])} tệp; depends_on={l['depends_on']}")
add('Chuỗi chung','GATE→LO→2A→2B','dependency 0/1/2/3; cùng giao .claude/dev/ci_dang_ky_test.py; không có chu trình')
add('Số ô null lease','6 ô mỗi nháp; GATE Issue vẫn nói .yaml.nhap','GATE .yaml=0; LO/2A/2B .yaml.nhap=5 mỗi tệp','không')
add('Trường lease §4','đủ trường hợp đồng','GATE thiếu literal write_set_hash, heartbeat_at, lease_until (3); chỉ hạn có bí danh lease_expires_at_utc','không đủ')
add('Schema §3.2 trong lease','spec dẫn protocol','objective/acceptance_criteria không là key (2), có mục tiêu/nghiệm thu dạng văn xuôi trong spec; chưa có projection được giao','chưa chứng minh ánh xạ')
add('Ba mỏ neo GATE lúc cấp','đo lại lúc 03:37:33Z 07-09','3/3 vẫn 1b3caa1 giữ chỗ; d28c4b1 có timestamp 01:50:09Z trước lúc cấp; drift +8 dòng ci.yml/+1 consumer','thiếu readback')
add('Thời hạn GATE','1440 phút; không phải trần run90','03:37:33Z 07-09→03:37:33Z 08-09 = 1440 phút')
add('Bia mộ ở HEAD','GATE thay #456; #456 trỏ ngược','hai chiều khớp, lease check rc=0')
add('A9 mọi bản #456 đã hết giữ','0 bản cũ còn hiệu lực khi bắt tay','snapshot 2 blob #456: 1 có bia mộ, 1 chưa có; ci.yml 1 người giữ, registry 2','chưa đạt trong snapshot')
add('ai-dang-giu thật','đối chiếu cả ref máy chủ','2 lệnh rc=12; git HTTPS bị chặn với GIT_ALLOW_PROTOCOL=file; KHÔNG ĐO ĐƯỢC máy chủ','chưa xác minh')
add('Ref/lease trong snapshot','historical 295/298/299 và 9/10 ref có mốc cũ','hiện 1 local head, 2 origin refs không HEAD; bare mirror 2 heads; 85 cặp blob/path lease; không có master ref','khác snapshot; không bác số cũ')
add('Trôi 1b3caa1→28cb898','46 commit','46 commit')
add('Cây 426bfc0 và merge1b3caa1','diff rỗng','0 tệp khác')
add('Additions #456 ở 0c5e889','consumer+76/−5; pretooluse+68/−0; tổng+144/−5','76/5; 68/0; 144/5')
for rev,claim in [('1b3caa1','39 bước/10 if/588 dòng/0 run trùng/trần60'),('28cb898','40 bước/10 if/596 dòng/trần60'),('HEAD','đã merge master, giữ runtime')]:
    w=st['workflow'][rev]
    add(f'ci.yml tại {rev}',claim,f"{w['steps']} bước/{w['ifs']} if/{w['lines']} dòng/{w['duplicate_run_bodies']} thân run trùng/trần{w['timeout']}")
add('Consumer Ruff khi tách','([],3)→([1 lỗi],3)','([],3)→([CI không provision Ruff trước test registry],3); 3 job, mỗi job mới 9 bước đầu')
add('Số dòng khối T\' / H','T\'=21+26; H=21+29','git diff --no-index: 21+26 và 21+29 additions, rc=1 vì có diff')
add('Diff runtime 1b3caa1→e5ab4b7','rỗng','0 dòng')
add('Hai băm khối H','c23bcd01… / bde441a0…','c23bcd019182023496cb3d9817c6553a0074c77bca26c0a0d1f71a4f5104e45c / bde441a08d129a962d862fe237003997610238edc8e87b7948d35de875e5f165 (gồm newline cuối)')
add('Consumer tham chiếu / số dạng','8 MOI, 1 mục Windows/2 dạng; SPAN giữ nguyên','tệp consumer bằng byte với cây; 8 MOI; 1/2 Windows; 8/8 SPAN giữ nguyên, 8/8 MOI đổi kiểu')
add('Số cặp H trong grammar Linux','13/13','13 cặp nhóm bắt trên 11 bản ghi của 8 mục (kiểm nguồn); khác phép đo stdout đủ8')
add('Bộ tấn công độc lập','ngoài danh sách ranh giới phải kiểm cả hai chiều',f"{attack['cases']} hàng / {attack['false_red']} đỏ giả / {attack['missed']} bỏ sót / {attack['exceptions']} ngoại lệ; gồm 625 tổ hợp số",'Đ1=0 trong bộ này')
add('Phân rã 1213 hàng','bộ reviewer mới',', '.join(f'{k}={v}' for k,v in attack['by_kind'].items()),'số mới')
add('Đ2','8 formatter thật rc=0','đã chạy cả8; sau sửa rig nhanh có6 bản xanh, H bác0/6; 2 chưa có bản xanh','KHÔNG ĐO ĐƯỢC đủ8')
old_hashes=['a5807082','0a476a97','b3034838','82f89e9d','c9997dac',None,'449578d8','366795e4']
for i,row in enumerate(real):
    p=row['path'];name=Path(p).name;z=nr if p==nr['path'] else row
    expected_time={'pretooluse_guard_test.py':'270s/rc1/3 ca đỏ (06-09)','subagent_ghi_detect_test.py':'88s rồi75s/rc0 (06-09)','nhanh_don_duoc_test.py':'33s rồi34s/rc0 (06-09)'}.get(name,'bản in thật rc0, mốc06-09')
    got=f"{z['start_utc']}; {z['seconds']:.2f}s; rc={z['rc']}; BASE/H đếm đỏ={z['BASE_red']}/{z['H_red']}; stdout {z['chars']} ký tự/{z['utf8_bytes']} byte"
    add('Chạy thật '+name,expected_time,got,'mốc mới; 0/6 đỏ giả H')
    hh=old_hashes[i]
    add('Băm stdout '+name,(hh+'…') if hh else 'pretooluse canonical chưa có stdout xanh',z['sha256'],'có' if hh and z['sha256'].startswith(hh) else 'không thay được stdout lịch sử')
    f=extra['formatter_measurements'][i]
    add('SPAN '+name,'số nhóm/cặp trong spec; chiều dài theo đúng bản in',f"groups={f['groups']}; span={f['span_chars']} ký tự/{f['span_utf8_bytes']} byte; cặp trong span={f['pairs_in_span']}; cặp nhóm H={f['captured_pairs_in_TONG']}",'thiếu match nếu rc1')
add('nhanh trước sửa rig','không có lời khai cùng môi trường','rc1, 0/8; 3,33s; 8515 ký tự/8531 byte; bị dịch vụ ký commit fixture chặn','lỗi rig; giữ log riêng')
add('nhanh stdout chi tiết','10 MUTANT: 8×1/1 + 2×3/3; tổng8/8','đúng 10 dòng, 8×1/1, 2×3/3, tổng8/8')
add('Ca nền/bảng mutant','pre39/34; sub33/22/6/1; nhanh8/10','AST/module: 39/34; 33/22/6/1; 8/10')
for s in spawn:
    declared={'subagent-base':438,'subagent-empty':438,'nhanh-base':136,'nhanh-mutants':35}[s['phase']]
    add('Spawn '+s['phase'],declared,f"{s['Popen']} Popen; {s['seconds']:.2f}s; kết quả {s['result'] if s['phase']!='subagent-base' else '33/33 True'}")
add('Nhánh mutant nhanh','5+3×N với N10; đầy đủ136+35','5+3×10=35; 136+35=171')
add('Subagent đầy đủ/kênh2/kênh3 (lịch sử)','10045 spawn, chênh9607; kênh2 10 spawn/6exec; kênh3 6spawn','KHÔNG ĐO ĐƯỢC lại riêng các đại lượng này; không suy từ thời gian toàn suite','chưa xác minh')
for m in extra['mutants_on_1213']:
    add('Mutant H '+m['name'],'bảng PR trên311 có mẫu số khác',f"trên1213: {m['changed_count']} đổi màu, {m['exception_count']} ngoại lệ (không tính ngoại lệ là răng)",'bộ mới; dead-bool0 khớp')
add('D9 đầu cặp 5000 chữ số','A9: BASE1 không ngoại lệ; bảng D9: BASE EXC','2 fixture pretooluse/nhanh: BASE=H=ValueError; vị trí mutant mcp: BASE0/H ValueError','A9 tự mâu thuẫn; không tính Đ1')
add('Bảng Issue464 nguyên chuỗi','True/True/False','False/False/False: lệch2/3; thêm TONG:DAT đúng khoảng trắng thành True/True/False','không')
add('Đường Issue465','.claude/dev/subagent_ghi_detect_test.py','không tồn tại; .claude/hooks/subagent_ghi_detect_test.py tồn tại','không')
for k,claim in [('9','n9,min40.20,max49.62,range9.42,median45.58,mean45.08'),('11','n11,min40.20,max50.48,range10.28,median46.02,mean45.84')]:
    a=contracts['printed_job_arithmetic'][k]
    add('Số học từ bảng job '+k,claim,', '.join(f'{n}={v:.2f}' if isinstance(v,float) else f'{n}={v}' for n,v in a.items()),'khớp số học; nguồn KHÔNG ĐO ĐƯỢC')
a=contracts['printed_split_arithmetic']
add('Ước tách Windows','15.77/21.03/13.03; tổng49.83 phút','15.77/21.03/13.03; tổng49.83 phút','số học khớp; chưa đo sau tách')
add('Ước tách Ubuntu','7.42/14.31/4.83; tổng26.56 phút','7.42/14.31/4.83; tổng26.56 phút','số học khớp; chưa đo sau tách')
add('Ước billing/giảm max job','110.65→126.22;+15.57/+14.1%; max−51.3%','110.65→126.22;+15.57/+14.07%; max−51.3194%; giảm22.17 phút, biên A1=3.97','số học khớp; hệ số×2 chưa kiểm hóa đơn')
add('11 head cùng tải?','coi biên độ là nhiễu runner','1 head39 bước không receipt-v2;10 head40 bước có receipt-v2','không cùng tải')
add('Biên mới có thể dùng làm ngưỡng?','A1≤25; mục nợ yêu cầu nới theo phương sai','phản mô hình28 phút: A1 đỏ; ngưỡng minh hoạ21.03+10.28=31.31 thì xanh','mâu thuẫn; chưa chọn ngưỡng mới')
add('Hiện vật lịch sử','do_h/law7/prior131/do_t2 + các gói, TSV, manifest','12 tên artifact inventory đều0; 6 tên file git-log kiểm đều0 dòng','KHÔNG ĐO ĐƯỢC')
add('Bảng H/mutant cũ','311 có kỳ vọng +54 ranh giới;14 mutants; 419 ca lượt5','KHÔNG ĐO ĐƯỢC lại nguyên bộ; có bộ mới1213 nhưng không thay dữ liệu lịch sử','chưa xác minh')
add('Bảng bước và tỷ lệ','buoc_master.tsv2062 hàng/12 cột; tỷ lệ1.07–9.74, median từng bước','KHÔNG ĐO ĐƯỢC; không có TSV/log nguồn hoặc mã trích','chưa xác minh')
add('hint_provenance','40 hunk, 4 bị bác','0 hiện vật; KHÔNG ĐO ĐƯỢC4/4 lý do bác','chưa xác minh')
add('Tình trạng Issue/lease nháp','6 null, chưa có Issue/Mission','4 Issue thân463–466 có băm; GATE có Mission467; nháp còn5 null; GATE0','lời mô tả đã cũ')
add('Chẩn đoán mạng trong Issue','4 Issue vẫn nói proxy cấm WebSocket','4 bản chiếu trái đính chính03:55Z; nguyên nhân thật KHÔNG ĐO ĐƯỢC trong review này','không nhất quán')
add('Guard --kiem-bang đối chứng cwd','các ca pretooluse lỗi môi trường','gọi nhầm từ root sandbox rc4; gọi đúng cay-kho rc0, runtime97+7=104, 8 lệnh write-scope, 26/26 help; flags425 xác nhận/35 chưa đo; Ruff0.15.8','chỉ chẩn đoán rig; không thay suite xanh')

out=['# VERDICT — cross-review PR #468, lượt 6','verdict: dang-do','reviewed_sha: 2adb6819caee0225d7b7e4f0c4e8c16f2faa7e73','',
'Kết luận dự kiến: **changes_requested**. 7 finding P1 và 4 P2; P3 cũ đã đóng. P1 cũ chưa đủ bằng chứng để đóng, nhưng không tìm được phản chứng H mới ngoài ranh giới công khai.','',
'Reviewer: Codex / OpenAI, phiên độc lập qua API, shell cục bộ. Transport: tệp trong sandbox. Không dùng mạng để xác minh GitHub, không commit/push vào ref được giao. Test có kho git giả lập nằm trong do-review/tmp. Đã đọc protocol §8/12/13 trước, áp khung tai-lieu/cross-review-SKILL.md; chỉ thị PROMPT cấm mạng ưu tiên hơn bước đăng verdict lên PR của skill. **Chưa đăng GitHub hoặc lập receipt/merge authorization.**','',
'## ĐỐI CHIẾU LƯỢT TRƯỚC',
'- `span-rong-nuot-ti-le-vo-can`: **VÁ HỜ về nghĩa vụ xác nhận**. Hai cơ chế cũ bị chặn trong bộ mới: **1213 ca / 0 đỏ giả / 0 bỏ sót**; Đ1=0 trên bộ đã đo. Đ2: **6/8 formatter có stdout xanh thật, H bác 0/6**, 2 formatter chưa đo được bản in xanh. Không gán hai suite lỗi nền thành lỗi H, không suy 0/8. Thiếu bộ ca lịch sử nên giữ P1 ở mức bằng chứng; chi tiết finding bên dưới.',
'- `uoc-kich-thuoc-lo-con-tinh-nhan-ac`: **ĐÃ VÁ THẬT**. Trích blob e5ab4b7 và HEAD, đo bằng git diff --no-index --numstat từ tệp rỗng: T\' **21+26**, H **21+29** additions. Không còn tính NHAN của A-c vào ước mới; vẫn phân biệt số dòng mẫu và additions triển khai.',
'- Lượt 5 không có verdict hoàn tất; không coi các bản dở là approval. Finding bia mộ cùng slug từ lịch sử được giữ nguyên khi tái xuất hiện trong snapshot.','',
'## BẢNG ĐO',
'Đo trong lượt 6 ngày **07-09-2026 UTC**, từ 06:14Z; UTC/giây/băm chi tiết nằm trong JSON/log đi kèm. “Số học khớp” chỉ xác nhận phép tính trên các ô đã in, không xác nhận nguồn CI lịch sử. Mọi số mới dùng mẫu số của bộ reviewer; không chép sang mẫu số 311.','',
'| khẳng định | PR khai | đo được | khớp? |','|---|---|---|---|',*R,'',
'Các phép đo chính: `python do-review/harness.py`; `python do-review/attack_h.py`; `python do-review/run_real.py`; `python do-review/rerun_nhanh.py`; `python do-review/run_gates.py`; `python do-review/audit_static.py`; `python do-review/recheck_contracts.py`; `python do-review/extra_checks.py`; `python do-review/count_spawn.py`; `sha256sum` bốn spec (lưu do-review/sha256sum.log).','',
'Mã H trích nguyên văn nằm tại `do-review/h_tong.py` và `do-review/h_predicate.py`, ghép với consumer thật bằng `harness.py`. `chay_moi`, `mau_theo_nen` và chuỗi SPAN giữ nguyên. Bộ mới chứa oracle hai chiều, bảng trường hợp và các đầu vào nguyên chuỗi; `attack-h-cases.json` là dữ liệu tái lập. Đ2 chỉ nhận đầu ra từ `_chay_that` có rc=0; bản nhanh chạy lại chỉ tắt ký commit trong tiến trình tạo fixture, không sửa test/formatter.','']
ordered=sorted(findings,key=lambda x:(0 if x[0]=='span-rong-nuot-ti-le-vo-can' else 1,int(x[1][1:]),findings.index(x)))
for slug,severity,title,body in ordered:
    out+=['### '+slug+'  ['+severity+']  '+title,body.strip(),'']
out+=['## Đánh giá chất lượng câu hỏi §12 — không chọn thay chủ kho',assessment,'',
'## Giới hạn và bàn giao',
'Đã đối chiếu cả bốn spec, bốn thân Issue, bốn lease và hunk bia mộ; diff/numstat khớp exact SHA. Write set và dependency giữa bốn spec/lease nhất quán, nhưng các bản chiếu Issue/điều kiện lease còn mâu thuẫn như findings. Các số mới đã ghi cả phần khớp và phần lệch.','',
'**KHÔNG ĐO ĐƯỢC**: stdout xanh thật mcp_gh/pretooluse trong rig này; replay nguyên bộ lịch sử và các kill-list; provenance bốn hunk; nguồn TSV thời lượng/billing; trạng thái GitHub, quyền/branch protection, đủ ref máy chủ tại lúc cấp, Windows thật. Không đánh giá những mục đó là pass. Không cần thêm lượt chạy nguyên các suite đỏ trong cùng rig để xác nhận lại cùng hạn chế.','',
'Gói dữ liệu nằm trong `do-review/`, có `ARTIFACTS.sha256` để kiểm tính toàn vẹn. Không có bản vá branch kèm theo; mọi hướng sửa trong verdict mang nhãn “chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit”.','',
'verdict: dang-do','']
P.write_text('\n'.join(out))
print(json.dumps({'findings':len(findings),'P1':sum(x[1]=='P1' for x in findings),'P2':sum(x[1]=='P2' for x in findings),'table_rows':len(R),'verdict_lines':len(out)},ensure_ascii=False))
