from pathlib import Path
import json
p=Path(__file__).resolve().parent;s=json.loads((p/'state.json').read_text());f=json.loads((p/'followup-checks.json').read_text());c=json.loads((p/'costs.json').read_text())
s['reconciliations']=[x for x in s['reconciliations'] if not x.startswith(('`a2-neo','`bien-do'))]
s['reconciliations'].append('`a2-neo-nen-cu-trai-write-set-hien-tai` [P1 lượt8 → P2 lượt9]: **VÁ HỜ về đồng bộ hợp đồng; phép so nghiệm thu đã vá đúng**. Mô hình r3 cùng base/event/lane: dispatch giữ88/88 bộ ba và PR ubuntu44/44 đều QUA; bỏ receipt-v2 lần lượt mất2/1 bộ ba, đều ĐỎ. So nhầm master/LAND với dispatch/WORKER lệch4 thêm/4 mất dù YAML bằng byte. A2 :463–471 không cho phép khác event/lane nữa. Tuy nhiên bảng thứ tự GATE :387 vẫn gộp A1/A2/A5 rồi khẳng định nền run34045664423/34048685345 “còn đúng”, trái phần revision và A2 mới; hai run này đều39 bước. Lỗ P1 ở phép so đã đóng; phần còn lại là mâu thuẫn văn bản P2. Hiện vật: `contract-checks.json`, `followup-checks.json`.')
s['reconciliations'].append('`bien-do-khac-head-khong-phai-nhieu-runner` [P2]: **VÁ HỜ**. Hai câu “mười một/mọi lượt master” và câu revision chưa làm đã mất3/3; Issue #463 đã sửa đúng. Tính lại mẫu đúng5 master/push +6 nhánh, 1×39+10×40 bước; A1≤25,00/A5≤135,00 giữ nguyên. Nhưng GATE :98–99 còn tuyên bố nhiễu runner1–2,3 phút “là có thật” và buộc mọi ngưỡng chừa biên; :447–448/:531–533 tiếp tục gọi chênh là nhiễu; :107 gọi hai run cũ là hai lượt master. Hai run cùng tree nhưng khác event và release-verify lane (4 bộ ba thêm/4 mất), nên không tách được nhiễu runner riêng, đúng nợ ở :619–625. Hiện vật: `costs.json`, `followup-checks.json`.')
order=['a2-neo-nen-cu-trai-write-set-hien-tai','bia-mo-mot-ref-khong-thu-hoi-moi-ban','bien-do-khac-head-khong-phai-nhieu-runner','quyet-dinh-tiep-h-con-bi-phu-dinh'];s['reconciliations'].sort(key=lambda x:next(i for i,k in enumerate(order) if x.startswith('`'+k+'`')))
s['rows'] += [
 ['A2: câu nền trong bảng thứ tự','run34045664423/34048685345 “còn đúng” cho A1/A2/A5','cả2 run39 bước; lease40; còn1 hàng mâu thuẫn tại GATE:387','không; phép so A2 mới đã đúng'],
 ['Câu mẫu và revision từng bị nêu lượt8','gỡ hai nhãn11-master + câu revision chưa làm','0/3 câu đích còn lại; Issue463 mô tả đúng5/6','có'],
 ['Nhiễu runner riêng','GATE98,447,531,533 vẫn khai nhiễu đã đo','hai head426bfc0/1b3caa1 cùng tree,0 path đổi; event dispatch/push,laneWORKER/LAND;86/86 bộ ba nhưng +4/−4','không chứng minh được nhiễu'],
 ['Thử đồng bộ văn bản ngoài checkout','không nới ngưỡng / không đổi thiết kế H','6 neo GATE +3 neo LO duy nhất; gỡ câu stale; A1/A5/43,20/21,03 và hai khốiPython H giữ nguyên','có trong thử nghiệm'],
 ['Gói hiện vật lượt8: sửa trong bản sao reviewer','manifest phải khớp toàn bộ','gốc rc1:50/69; thiếu19,tìm đủ19 byte-exact ở lượt6; phục dựng rc0:69/69','không ở PR; mô hình vá đạt'],
 ['Merge ec03c85 → 982cd1d','không đè bản vá executor','4 Issue: bỏ đúng1 block đính chính mỗi tệp thì bằng byte896c1c0; câu dẫn đúng4/4;0 path spec/lease đổi','có'],
 ['Merge master b416830 → reviewed_sha','wp461, ngoài phạm vi giao','3 path wp461;4/4 Issue giữ byte982cd1d; không đụng bốn packet đang review','có; không review nội dung wp461'],
 ['Nguồn A1/A5','13 run /26 job /1140 bước','13/26/1140;TSV14/9 cột;1140/1140 giây khớp timestamp; tái sinh rc0,4/4 đầu ra khớp byte','có'],
 ['Mẫu11 run','5master+6nhánh;1×39+10×40','5master/push+6nhánh;1×39+10×40','có'],
]
stat=c['sample']['windows_stats'];s['rows'].append(['Windows mẫu11: phút job','min40,20;max50,48;median46,02;mean45,84;biên10,28','; '.join(k+'='+format(v,'.10f') for k,v in stat.items()),'có'])
for name,r in c['ratios'].items():
 vals='; '.join(k+'='+format(r[k],'.10f') for k in ['n','minimum','maximum','median','mean','range'])+f"; dải median={r['rounding_lower']:.10f}–{r['rounding_upper']:.10f}"
 s['rows'].append(['Hệ số '+name,' / '.join(r['expected'])+('; dải '+'–'.join(r['range_expected']) if r['range_expected'] else ''),vals,'có; job không khai dải'])
s['rows'].append(['Bảng hệ số r3','7 dòng +6 dải','28/28 ô n/min/max/median;12/12 đầu dải khớp sau làm tròn','có'])
for x in c['eleven']:s['rows'].append(['Run'+x['run']+' / '+x['head'],'bảng11run',f"{x['branch']};{x['event']};{x['steps']} bước;Windows {x['windows_seconds']}s={x['windows_minutes']:.10f}ph",'có'])
for plat,x in c['costs'].items():s['rows'].append(['Run nhánh34045664423 / '+plat,'43,20/21,03 Windows; ước từ bước cũ','; '.join(k+'='+format(v,'.10f') for k,v in x.items()),'có; dự toán dùng các số phút đã làm tròn'])
s['rows'].append(['Số học chi phí, phút theo định nghĩa spec','110,65→126,22;A1≤25;A5≤135','từ giây:110,65→126,2333333333; từ số hạng phút làm tròn trong bảng:126,22;longest21,0333333333;A1=25,A5=135','có theo hai cách tính đã khai; không xác minh hóa đơn'])
for x in c['cancelled']:s['rows'].append(['Run cancelled'+x['run_id'],'nhánh/workflow_dispatch',f"{x['head7']};{x['head_branch']};{x['event']};{x['seconds']}s={x['minutes']:.10f}ph;{x['conclusion']}",'có'])
expected={'bien-nhan-v2':'rc0;TỔNG ĐẠT','lease-check':'rc0;ĐĂNG ĐƯỢC','lease-publish-test':'rc0;121/121','doc-claims':'rc0;ok:true','doctrine-scan':'rc0','adr-song':'rc0;46/46','eol-json':'ok:true'}
for name,e in expected.items():
 meta=json.loads((p/(name+'.json')).read_text());out=(p/(name+'.stdout')).read_text();positive=out.strip().splitlines()[-1] if name not in ['doc-claims','eol-json'] else ''
 if name=='doc-claims':d=json.loads(out);positive='ok='+str(d['ok'])+';advisory='+str(d.get('summary',{}))
 if name=='eol-json':positive=out.strip()
 s['rows'].append(['Cổng '+name,e,f"rc={meta['rc']};{positive};{meta['seconds']:.3f}s;stdout={meta['stdout_bytes']}B",'có'])
s['rows'].append(['Cổng EOL không JSON','rc0','rc0;stdout0B; đã chạy lại --json để lấy bằng chứng dương','có, không suy pass chỉ từ output rỗng'])
s['notes']=[x for x in s['notes'] if not x.startswith('Kết luận nhỏ A2:')]
(p/'state.json').write_text(json.dumps(s,ensure_ascii=False,indent=2)+'\n')
