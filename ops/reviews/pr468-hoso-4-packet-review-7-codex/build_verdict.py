import datetime as dt
import json
import pathlib
import sys

B=pathlib.Path(__file__).resolve().parents[1]
O=B/'do-review7'
def read(name): return json.loads((O/name).read_text())
initial=read('initial.json'); s=read('static.json'); n=read('nen-measurements.json')
extra=json.loads((O/'replay/extra-checks.json').read_text())
status='changes_requested' if '--final' in sys.argv else 'dang-do'
lines=[f'''# VERDICT — cross-review PR #468, lượt 7

verdict: {status}
reviewed_sha: b2ea0f24576275014e8124bfd3e0b6a16c3ca8b5

Kết luận nội dung: **changes_requested — 4 P1, 2 P2**. Đã đối chiếu đủ **7 P1 + 4 P2** của lượt 6, giữ nguyên slug: **6 ĐÃ VÁ THẬT, 2 VÁ HỜ, 1 VÁ SINH LỖI MỚI, 2 CHƯA VÁ**. Có thêm một finding P1 về mỏ neo đặc tả LO trong Issue #464.

Reviewer: **Codex / OpenAI**, phiên độc lập qua API, có shell cục bộ; transport: tệp trong sandbox. Đọc protocol trích §8/12/13 trước, dùng đúng khung `tai-lieu/cross-review-SKILL.md`. Chỉ đọc/ghi trong phạm vi PROMPT cấp. Không dùng mạng, không commit/push vào cây/ref được review. Không đăng GitHub, không lập receipt hay cấp merge authorization; chỉ thị offline của PROMPT ưu tiên bước đăng PR trong skill.

Đo ngày **07-09-2026 UTC**, các lệnh thực chạy có thời gian, rc, stdout và băm trong `do-review7/`. Đường dẫn `ops/...` và `.claude/...` bên dưới tính từ `cay-kho/`. Bản in lịch sử chỉ được **replay**, không khai thành suite vừa chạy. Dữ liệu MCP đã chép vào kho cho phép kiểm tính toán nội bộ, không chứng minh lại phản hồi GitHub trực tiếp.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `span-rong-nuot-ti-le-vo-can` [P1]: **VÁ HỜ về nghĩa vụ bằng chứng**. Nguyên `harness.py`/`attack_h.py` trong gói TRONG KHO tái lập **1213 ca / 0 đỏ giả / 0 bỏ sót / 0 ngoại lệ**, hai tệp JSON trùng từng byte. Bốn mutant tái đo đúng **5/51/42/0** ca đổi màu. Bản mcp executor lưu có băm khớp và H bác **0/1**; cộng sáu bản xanh lượt 6 thành **0/7**, chưa phải 0/8. Tự chạy pretooluse từ `cay-kho/`: **rc=1, 435.033 s, 36/39**, đúng ba ca lỗi môi trường; stdout băm trùng bản đỏ đã giao. Không tìm thấy phản chứng H mới ngoài ranh giới công khai; không coi lỗi rig là Đ1/Đ2 chạm ngưỡng. P1 còn mở vì thiếu bản xanh thứ tám.
- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **CHƯA VÁ**. Tự quét snapshot bằng bộ phân loại thật: **2 blob #456**, một bia mộ đối xứng, một còn hạn chưa bia mộ trên `refs/remotes/origin/claude/gate-tach-job-cat-chi-phi`. Registry vẫn có **2 người giữ**. Mô phỏng **14:30:06Z → 14:30:07Z** cho **2 → 1**; lời khai hết hạn đúng. Phản mô hình cập nhật riêng master sang cây có bia mộ, giữ ref GATE cũ, vẫn **2**: lời hứa tự đóng ngay khi merge thiếu điều kiện cập nhật/dọn mọi ref. Không sửa ref để làm phép đo.
- `issue-lo-giu-rang-buoc-cu` [P1]: **ĐÃ VÁ THẬT**. Issue #464:84–90 nay cho đổi giá trị thành `(SPAN,TONG)` và neo lại ba ca #456. Tự ghép H với consumer thật: **8/8 SPAN giữ nguyên, 8/8 giá trị đổi kiểu**, hai dạng Windows đúng thứ tự; không còn lệnh cấm thay kiểu MOI.
- `issue-kiem-lease-sai-write-set` [P1]: **ĐÃ VÁ THẬT**. Các Issue nay nêu đủ đường trong write set **2/1/2/2**, đều tồn tại; #465 dùng `.claude/hooks/subagent_ghi_detect_test.py`. Tự quét snapshot cho `ci.yml=1`, registry `=2`, subagent `=0`, nhanh `=0`; các Issue có giao registry đều ghi bị chặn. Số máy chủ 299/300 tại 05:52Z **KHÔNG ĐO ĐƯỢC**; kết luận đóng lỗi thiếu/sai đường và kết luận rảnh sai, không chứng nhận lại lịch sử máy chủ.
- `lease-gate-cap-that-con-ho-so-nhap` [P1]: **ĐÃ VÁ THẬT đối với hồ sơ lease được giao**. Ba trường §4 đủ; tự băm write set đúng `0f7b869d…`; heartbeat bằng mốc cấp, hai tên hạn bằng nhau, **1440 phút**. Ba neo đều `d28c4b1062e8505cbdaaf0237fcbe3f9b8ee4705`; `git log` cho commit **01:50:09Z**, trước cấp **03:37:33Z**. Dữ liệu run được giao ghi `push/master` **01:50:12Z**, không có master mới hơn trong snapshot; Issue #463 đã ghi lease cấp thật. Không còn ba neo giữ chỗ. Không suy việc thiếu literal `objective`/`acceptance_criteria` trong LEASE thành lỗi §4: đó là trường của Packet Spec §3.2, nội dung mục tiêu/nghiệm thu có trong spec dẫn băm. **Head máy chủ tại chính giây cấp vẫn KHÔNG ĐO ĐƯỢC trực tiếp**; không dùng git log để chứng nhận lịch sử di chuyển ref ngoài snapshot.
- `thieu-hien-vat-quyet-dinh-h-va-chi-phi` [P1]: **VÁ HỜ, đã sửa đáng kể**. LO đã rút 311/419 và các băm lịch sử khỏi vai trò cổng; corpus **1213** có oracle và hiện vật đầy đủ, không đòi dùng lại corpus lịch sử đã rút làm cổng. Nguồn A1/A5 mới **13 run / 26 job / 1140 bước** tái sinh khớp byte. Nhưng nguồn thay thế chưa tái lập bảng quyết định GATE đang hiệu lực: **4 trung vị lệch**, trong đó receipt-v2 **7.79293×** thay vì **7.56×**, nằm ngoài cả dải làm tròn đã khai. Bản gốc 2062 hàng/19 job Ubuntu vẫn thiếu. Chi tiết dưới; không gộp số học đúng trên ô phút đã làm tròn với tính từ giây gốc.
- `hint-provenance-bon-hunk-khong-co-de-kiem` [P1]: **ĐÃ VÁ THẬT bằng cách rút lời khai không có căn cứ**, không phải đã kiểm được bốn lý do. LO:261–271 rút rõ 40 hunk/4 hunk bị bác và lời khai tái dẫn xuất từng hunk; không còn dùng chúng làm chứng cứ hiện hành. Bề mặt nguồn còn dùng là hai khối H, tự trích và băm khớp nguyên bản gói reviewer (**c23bcd01…**, **bde441a0…**). Mã thi công tương lai vẫn phải khai provenance riêng theo §7. Bốn lý do lịch sử **KHÔNG ĐO ĐƯỢC**, không xác nhận chúng đúng.
- `a9-khai-sai-base-ngoai-le` [P2]: **VÁ SINH LỖI MỚI**. Đã sửa đúng việc BASE cũng ném khi số dài nằm trong nhóm CA, nhưng thêm lời khai BASE trả **1** khi số dài ở cặp đột biến. Tự chạy bốn fixture: CA pretooluse và nhanh **BASE=H=ValueError**; cặp đột biến pretooluse và mcp **BASE=0, H=ValueError**. Sai mới lặp ở ba chỗ trong spec/Issue.
- `bien-do-khac-head-khong-phai-nhieu-runner` [P2]: **CHƯA VÁ**. GATE:428–441 giữ A1≤25 và cấm nới, :598–606 vẫn đòi nới theo “phương sai”. Tự đọc YAML ở 11 head: **1×39 bước + 10×40 bước**; nguồn mới còn cho **5 master + 6 nhánh khác**, không phải 11 master. Đặc tả GATE không đổi băm, lease vẫn đóng băng nó. Lời khai cần revision chủ kho là hợp lý, nhưng không đóng được finding.
- `issue-chep-nham-du-lieu-va-chan-doan-cu` [P2]: **ĐÃ VÁ THẬT đối với các lỗi lượt 6 đã nêu**. Ba fixture Issue #464 có terminator, tự replay BASE **0/0/1**, tương đương **True/True/False**; H **0/1/1**. Issue #465 nêu đúng `CA33/33·DOTBIEN22/22`, Linux giữ hành vi và Windows có dòng riêng. Cả bốn Issue đã rút chẩn đoán proxy, ghi nguyên nhân chưa biết. Mỏ neo băm mới sai ở Issue #464 được ghi bằng finding riêng bên dưới.
- `gate-lease-cam-sua-phan-chung` [P2]: **ĐÃ VÁ THẬT**. Lease GATE:177–180 đã cho `loi_ruff_ci` và các ca A7 của nó trong `phan_chung()`, khớp write set #2/A7 của spec. AST consumer xác nhận hai hàm độc lập; chưa có runtime diff, không khai bốn ca thi công đã được thêm.

## BẢNG ĐO

Các số trên tệp đo gốc được giữ đầy đủ trong JSON/log; bảng sau ghi cả phần khớp, lệch và không đo được. `0` của `chay_moi` là số mục đỏ bằng không, khác `False` của vị từ. Các tỷ lệ/giá chi phí ở đây là tính toán trên dữ liệu được giao, không phải số đo Windows mới hay hóa đơn.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
''']
def row(a,b,c,d='có'):
    def clean(x): return str(x).replace('|','\\|').replace('\n','; ')
    lines.append('| '+' | '.join(map(clean,[a,b,c,d]))+' |\n')
row('Exact HEAD / tree','SHA trong PROMPT',initial['head']+' / '+initial['tree'])
row('Môi trường git','abbrev=7, không shallow, sạch',f"{initial['abbrev']}; shallow={initial['shallow']}; status ban đầu rỗng")
for base,label in [('2adb681','Diff từ lượt 6'),('d28c4b1','Toàn PR so nền master')]:
    x=initial[base];row(label,'patch + numstat được giao',f"{x['files']} tệp; +{x['add']}/−{x['del']}; diff và numstat khớp từng byte; ngoài ops={len(x['outside_ops'])}")
row('Manifest hiện vật lượt 6','băm khớp',f"rc={initial['manifest_rc']}; {initial['manifest_ok']}/{initial['manifest_entries']} khớp; {len(initial['unlisted'])} tệp executor bổ sung ngoài manifest",'có trong phạm vi 62 tệp')
row('Corpus H','1213/0/0/0','1213/0/0/0; attack-h-cases.json và summary bằng byte')
case_counts=json.loads((O/'replay/attack-h-summary.json').read_text())['by_kind']
row('Phân rã corpus','bộ độc lập lượt 6',', '.join(f'{k}={v}' for k,v in case_counts.items()))
for name,data in s['H_blocks'].items(): row('Khối '+name,'băm spec = gói',data['extracted'])
row('Consumer tham chiếu','consumer thật',( 'bằng byte; 8 MOI; 8 SPAN giữ nguyên; 8 đổi kiểu; 2 dạng Windows' if s['consumer_copy_matches'] else 'lệch'))
for x in extra['mutants_on_1213']: row('Mutant '+x['name'],'đính chính 5/51/42/0',f"{x['changed_count']} đổi màu, {x['exception_count']} ngoại lệ; ngoại lệ không tính là răng")
for x in s['leases']:
    label=x['file'].split('-exec-')[0]
    row('Spec '+label,x['declared'],x['spec_hash'],'có; bản sao bằng byte' if x['hash_matches'] and x['copies_match'] else 'không')
    row('Issue neo spec '+label,'hash + commit '+x['issue_commit'][:7],x['issue_commit_hash'],'có' if x['issue_commit_hash_matches'] else 'KHÔNG: commit chứa bản cũ')
    row('Write set / dependency '+label,'spec–lease',f"{len(x['write_set'])} đường đều tồn tại; depends_on={x['dependency']}; null={len(x['null_keys'])}")
row('Lease GATE §4','write_set_hash, heartbeat_at, lease_until','0 trường thiếu; hash='+s['gate']['write_set_hash_actual'])
row('Chuỗi băm write set','sort + LF giữa đường + LF cuối',repr(s['gate']['payload']))
row('Ba neo GATE','head master lúc cấp','3/3 = '+s['gate']['anchors']['base_sha']+'; commit 01:50:09Z; run master 01:50:12Z; cấp 03:37:33Z','phù hợp snapshot; GitHub tại giây cấp KHÔNG ĐO ĐƯỢC')
row('Hạn/heartbeat GATE','cùng mốc cấp; 24 giờ','heartbeat=2026-09-07T03:37:33Z; lease_until=lease_expires_at_utc=2026-09-08T03:37:33Z; 1440 phút')
row('Drift hai tệp write set','+8/+1',s['gate']['drift'])
row('Schema §3.2 / §4','trường đúng đối tượng','objective/acceptance_criteria không là key lease; nội dung trong Packet Spec; lease GATE đủ toàn bộ 8 key §4','không dùng key Packet Spec để bác riêng lease')
row('Snapshot lease', 'quét mọi ref được giao',f"{s['snapshot_blob_path_pairs']} cặp blob/path; 2 blob #456, 1 bia mộ đối xứng; 1 chưa bia mộ")
row('Người giữ trong snapshot','GATE 1/2; sub/nhanh 0','ci.yml=1; registry=2; subagent=0; nhanh=0')
row('Đồng hồ #456','hết hạn 14:30:07Z','mô phỏng 14:30:06Z registry=2; 14:30:07Z registry=1','đúng trong snapshot, không phải readback tương lai')
row('Cập nhật riêng master','merge PR468 ⇒ hết chặn','mô hình giữ ref GATE cũ: ci.yml=1; registry=2','không đủ')
row('Ref máy chủ','299 ⊆ 300 tại 05:52Z','snapshot có 1 local head, 2 origin refs không HEAD; không có master ref','KHÔNG ĐO ĐƯỢC GitHub; không bác số lịch sử bằng số snapshot')
rec=s['receipt']
row('Receipt lượt 6','v2 / SHA exact / bytes/hash',f"v{rec['schema']}; {rec['actual_bytes']} byte; {rec['actual_sha256']}; reviewed_sha={rec['reviewed_sha']}; blob 8c3e371 và bản sao khớp")
row('Tên hiện vật lịch sử','LO đã rút khỏi cổng','9 tên kiểm bằng git ls-files đều không có: '+', '.join(s['artifact_missing']),'đúng giới hạn đã khai; không suy phép đo lịch sử')
gcounts={'doctrine-scan':'7 tệp, 0 chỗ chép','adr-song':'46/46; có ngoại lệ ADR0016 lịch sử','doc-claims':'ok=true; 106 tệp; advisory=claims_flagged=367','ci-dang-ky':'PHẢN CHỨNG51/51; TỔNG ĐẠT','lease-publish-test':'lần đầu120/121; lỗi t82 do symlink reviewer gây copytree vòng','bien-nhan-v2':'21 ĐẠT v2; 11/11 miễn legacy; 42 nợ đóng băng; 0 vi phạm; 0 KHÔNG ĐO ĐƯỢC; tổng74','lease-check':'ĐĂNG ĐƯỢC; neo d28c4b1','lease-publish-test-rerun':'121/121; đã chạy121, bỏ qua0'}
for x in read('gates-results.json')+read('lease-rerun-results.json'):
    row('Cổng '+x['name'],'EVIDENCE: rc0 (ci-dang-ky chạy thêm)',f"rc={x['rc']}; {x['seconds']:.3f}s; {x['bytes']} byte; {gcounts[x['name']]}",'lỗi rig reviewer, đã chạy sạch lại' if x['name']=='lease-publish-test' else 'có')
row('Ruff cho pretooluse','bắt buộc0.15.15','ruff --version =0.15.8; không có wheel/binary bổ sung trong sandbox','không đủ môi trường; không dùng mạng để cài')
for x in read('real-results.json'):
    row('Suite thật '+x['name'],'thử lấy bản xanh',f"start={x['start_utc']}; rc={x['rc']}; {x['seconds']:.3f}s; {x['bytes']} byte; sha256={x['sha256']}",'KHÔNG ĐO ĐƯỢC bản xanh trong rig')
row('Pretooluse nền','3 ca đỏ môi trường','36/39; t11 lo336, t15 --kiem-bang, t33 runtime; hai cổng rc4; stdout9490byte trùng gói')
row('Mcp nền cục bộ','socket loopback từng không dùng được','38/42; A5/A6-302/A6-303/A7 PermissionError; rc1; không có điểm mutant','lỗi rig, không phải Đ2 phản chứng H')
for x in s['stored_outputs']:
    row('Replay '+x['file'],'stdout đã lưu; không chạy lại suite',f"{x['bytes']} byte; sha256={x['sha256']}; BASE/H với rc0 giả định={x['BASE_with_rc0']}/{x['H_with_rc0']}",'chỉ bản có rc0 đã được ghi mới tính Đ2')
row('Đ2 cộng dồn','reviewer0/6 + executor mcp0/1','0/7 bản xanh bị H bác; pretooluse còn thiếu1/8','KHÔNG ĐO ĐƯỢC đủ8')
for x in extra['formatter_measurements']:
    row('SPAN '+pathlib.Path(x['path']).name,'bản stdout lịch sử trong gói',f"nhóm={x['groups']}; span ký tự/byte={x['span_chars']}/{x['span_utf8_bytes']}; cặp SPAN={x['pairs_in_span']}; cặp TONG={x['captured_pairs_in_TONG']}",'đo trên đúng bản in đã lưu; rc1 không tính Đ2')
for name,x in s['d9'].items(): row('D9 '+name,'5000 chữ số, Python int trần4300',f"BASE={x['BASE']}; H={x['H']}",'BASE=0 ở cặp mutant bác lời khai1')
row('Fixture Issue464','True / True / False','BASE số đỏ0/0/1; H0/1/1')
row('Nền A1/A5','13 run,26 job,1140 bước',f"{n['runs']}/{n['jobs']}/{n['steps']}; job14cột, bước9cột; 25success+1cancelled; tinh.py rc0; 4 đầu ra tái sinh bằng byte")
for name,x in n['summary'].items(): row('Thống kê '+name,'tom_tat.md',f"n={x['n']}; min={x['min']:.2f}; max={x['max']:.2f}; biên độ={x['range']:.2f}; trung vị={x['median']:.2f}; trung bình={x['mean']:.2f} phút")
x=n['eleven_stats'];row('11 job được GATE dẫn','n11;40.20–50.48;range10.28;median46.02;mean45.84',f"n={x['n']}; min={x['min']:.2f}; max={x['max']:.2f}; range={x['range']:.2f}; median={x['median']:.2f}; mean={x['mean']:.2f}")
row('11 run thuộc master?','11 master','5master+6nhánhkhác; 1head39bước,10head40bước','không; khác branch/event và workload')
for x in n['eleven']:row('Run '+x['run'],x['head'],f"{x['branch']}/{x['event']}; Windows{x['minutes']}phút; YAML{x['steps']}bước; receipt_v2={x['receipt_v2']}",'trị thời lượng khớp; nhãn master chỉ đúng5/11')
expected={'test registry':1.20,'tl selftest':1.83,'packet-loop selftest':2.35,'G5 kiem ban ke':2.39,'lease-publish selftest':2.94,'bien-nhan v2 selftest':7.56,'job':1.73}
for name,x in n['ratios'].items():
    measured=f"n={x['n']}; min={x['min']:.2f}×; max={x['max']:.2f}×; median={x['median']:.8f}×"
    if 'rounding_lower' in x: measured+=f"; dải±0.5s=[{x['rounding_lower']:.8f},{x['rounding_upper']:.8f}]"
    row('Tỷ lệ '+name,f"trung vị{expected[name]:.2f}×",measured,'không' if round(x['median'],2)!=expected[name] else 'có')
for name,x in n['split_costs'].items():row('Ước tách '+name,'GATE dùng ô phút đã làm tròn',f"giây gốc→phút: job={x['job']:.8f}; Σbước={x['step_sum']:.8f}; setup1–10={x['setup1_10']:.8f}; setup2–10={x['setup2_10']:.8f}; registry={x['registry']:.8f}; packet={x['packet_loop']:.8f}; sau={x['remaining']:.8f}/{x['split_registry']:.8f}/{x['split_packet']:.8f}; tổng={x['total_steps']:.8f}",'phân biệt hai cách làm tròn')
row('Ước chi phí','110.65→126.22; +15.57;+14.1%','tính từ ô đã in:126.22 (khớp); từ giây nguồn:126.23333333; không coi lệch làm tròn0.01333 là finding')
row('Phép tính giảm max job','43.20→21.03;−51.3%;biênA1≈4','−51.3194%; biên25−21.03=3.97; phản mô hình28 phút trượt25 nhưng qua31.31=21.03+10.28','số học khớp; 31.31 chỉ phản mô hình, không là ngưỡng được phép')
row('GitHub/Windows/billing mới','ngoài sandbox','không mạng; không Windows; không hóa đơn; packet_loop_test và ci_dang_ky --chay toàn bộ không chạy','KHÔNG ĐO ĐƯỢC; không coi pass')

lines.append('''
## Trục Spec / Standards của phần đổi sau lượt 6

- **Đính chính LO:** việc rút các số 311/419, 40 hunk/4 lý do khỏi bằng chứng hiện hành là rõ, có phạm vi ưu tiên “đọc trước mọi con số bên dưới”. Không coi riêng việc giữ bảng lịch sử phía dưới là một finding mới, không ép corpus 1213 mang mẫu số lịch sử. Bảy luật và hai khối H **không đổi**, băm bằng nhau. A1–A6 vẫn là yêu cầu thi công tương lai; kết quả 1213 không tự chứng nhận tất cả nghiệm thu. Lời khai mới ở A9 vẫn sai như phản chứng dưới.
- **Lease GATE:** `write_set_hash` được tính đúng từ `.claude/dev/ci_dang_ky_test.py\\n.github/workflows/ci.yml\\n`; ba trường và ba neo đã sửa. Lịch sử git cùng bản run master trong gói ủng hộ `d28c4b1` là nền hợp lý tại lúc cấp; thiếu readback mạng nên không nâng kết luận thành chứng nhận ref máy chủ đúng giây đó. Nội dung GATE đã đóng băng vẫn có mâu thuẫn A1/nới ngưỡng; reviewer không tự sửa băm hay cấp revision.
- **Bốn Issue:** các lỗi phạm vi, đường dẫn, ví dụ và chẩn đoán mạng của lượt 6 đã sửa. Chuỗi phụ thuộc GATE→LO→2A→2B giữ nguyên; Issue 2A/2B nêu tiền nhiệm trực tiếp, spec/lease liệt kê thêm các tiền nhiệm bắc cầu, nên thứ tự thực thi không đổi. Issue #464 còn mỏ neo commit của LO cũ đi kèm băm mới. Bảng GATE/Issue #463 chưa khớp nguồn A1/A5 mới ở trung vị và nhãn master.
- **Receipt:** validator thực cho v2 hợp lệ; path/hash/byte/ancestry của verdict lượt 6 khớp. Đây là kiểm **hình dạng và nội dung đã lưu**, không xác minh lại session model, actor GitHub hoặc required check. Receipt giữ `changes_requested`; không dùng nhãn `assurance: cross_approved` trong đó làm quyền merge.

| điều kiện LO | phép kiểm ở lượt 7 | kết luận |
|---|---|---|
| Đ1 | Corpus trong kho, oracle hai chiều, 1213 hàng; 4 mutant tái đo | 0 đỏ giả/0 bỏ sót trong bộ đo; không có phản chứng mới ngoài ranh giới. Không lấy số mục đỏ của ca âm đúng làm lỗi H. |
| Đ2 | Replay 6 stdout xanh đã lưu + mcp executor rc0 có băm; thử chạy thật pretooluse | H bác0/7. Pretooluse rc1 do Ruff/rig, không có stdout xanh thứ8; **KHÔNG ĐO ĐƯỢC đủ8**. |
| Đ3 | Đọc bốn spec/Issue được giao, không có yêu cầu thêm metadata n/m vào dòng tổng | Không có chứng cứ dương kích hoạt trong phạm vi này; danh sách toàn bộ packet máy chủ **KHÔNG ĐO ĐƯỢC**. Không suy “không tồn tại ở mọi packet”. |
| Đ4 | git diff từ master hoặc lượt6: chỉ ops/, runtime consumer không đổi | Runtime additions=0 của PR hồ sơ; chưa phải nghiệm thu bản thi công H sau GATE. |
| Đ5 | Registry thật hiện tại51/51, H chưa thi công vào runtime | Chưa có phép đo N/N của bản thi công với toàn bộ ca mới; không lấy51/51 nền làm pass Đ5. |

**P1 `span-rong-nuot-ti-le-vo-can` còn mở vì nghĩa vụ bằng chứng.** Không điều nào trong Đ1/Đ2 đã được đo là ≥1; không tuyên bố H thất bại thiết kế vì suite nền đỏ. Đ3 còn giới hạn snapshot, Đ4/Đ5 chờ thi công. Quyết định §12 thuộc chủ kho; review này không chọn hướng, cấp lease hoặc cho phép bắt tay.

### span-rong-nuot-ti-le-vo-can  [P1]  Chưa có bản in xanh thật của formatter thứ tám để đóng nghĩa vụ xác nhận H

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:77`, `:249`, `:250`, `:744`; `ops/reviews/pr468-hoso-4-packet-review-6-codex/d2-that-results.json:13`.

VẤN ĐỀ: Corpus và băm mới đã kiểm được; thiếu bản xanh pretooluse vẫn còn. Bản `rc=1` chỉ chứng minh rig đỏ, không xác nhận H nhận formatter hợp lệ. Dữ liệu đã lưu cho 7/8 formatter và H bác0/7. Cả JSON lẫn EVIDENCE khai giới hạn đúng; khai đúng giới hạn không thay được bằng chứng còn thiếu ở chỗ quyết định.

ĐÃ THỬ VÁ: không vá regex khi chưa tìm thấy phản chứng H. Đã dựng đúng layout cho harness, chạy suite từ đúng cwd, giữ nguyên test/formatter. Hướng xử lý tại A6/Đ2: thu stdout nguyên byte từ `_chay_that` trên môi trường có Ruff0.15.15 thật, lưu rc/time/hash, rồi replay H qua consumer thật. Ca khóa: rc0 thật + H số đỏ0; giữ các ca malformed/duplicate đang đỏ. Rủi ro: ép xanh bằng skip, stdout tổng hợp hay Ruff giả sẽ che đúng điều cần đo. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: nguyên script gói trong kho cho1213/0/0/0; `python3 do-review7/replay_package.py extra_checks.py` cho5/51/42/0 đổi màu. `python3 do-review7/run_measurements.py real`: pretooluse **rc1,435.033s**, `TONG: CA36/39`, lỗi t11/t15/t33; băm `00bb4b944b12cca20b33fd8ce77ba8280e1becd4249e41aced15803ecab44004`, khớp bản đỏ executor. Ruff đang0.15.8; không có bản0.15.15 trong phạm vi được cấp và cấm mạng. Bản mcp executor2260byte có băm `87349f553be22fa00992f3651963f850a12633b522efe19b2e0350d4cfc19340`, replay BASE/H=0/0. Không tính hai suite cục bộ rc1 vào mẫu bản xanh.

ĐỘ TIN: cao về phép đo cục bộ và phần bằng chứng thiếu; không có kết luận rằng H tạo đỏ giả mới.

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Bản #456 còn hạn trên ref GATE vẫn giữ registry

TỆP/DÒNG: `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:97`, `ops/leases/gate-tach-job-cat-chi-phi-exec-1-claude-20260906.yaml:112`, `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:549`; blob `8b2103c06687546379a17f6deafc97f1fe0173fd` của lease #456 tại ref GATE trong snapshot.

VẤN ĐỀ: HEAD có bia mộ hai chiều, nhưng ref `refs/remotes/origin/claude/gate-tach-job-cat-chi-phi` vẫn ở d28c4b1 và có blob chưa bia mộ. Tại thời điểm đo, registry có GATE+#456. Lời khai “không vá được từ nhánh này” phù hợp giới hạn không sửa ref người khác. Lời khai tự đóng lúc hết hạn đúng theo classifier; lời khai chỉ cần merge PR468 chưa đủ: ref GATE cũ vẫn có thể tồn tại và vẫn được quét.

ĐÃ THỬ VÁ: dùng mô hình dữ liệu, không chuyển ref. Thử cập nhật riêng master sang các lease của cây mới vẫn còn hai người giữ; thử đồng hồ đúng giây hết hạn loại #456. Hướng xử lý: cập nhật/dọn mọi ref còn blob cũ theo authority phù hợp, hoặc chờ hết hạn rồi readback đủ write set trước khi bắt tay; kiểm hạn/heartbeat của GATE khi tiếp tục. Ca khóa: `ai-dang-giu` chỉ còn đúng lease mới trên từng đường. Rủi ro: chỉ đo `check`, chỉ nhìn master, hoặc dùng tập ref chưa đồng bộ sẽ bỏ sót bản giữ khác. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 do-review7/static_checks.py` gọi `_quet_lease_toan_kho(..., doi_chieu_ref=False)` và classifier/bia mộ của production: 2 blob #456; registry2, ci.yml1. Mô hình riêng-master vẫn2; giả lập14:30:06Z→14:30:07Z cho2→1. `lease_publish.py check` rc0 không phủ định phép quét này. Trạng thái GitHub/mọi ref máy chủ và sự kiện merge thực **KHÔNG ĐO ĐƯỢC**, không bỏ chốt mạng để khai cổng xanh.

ĐỘ TIN: cao với snapshot và phản mô hình; không suy trạng thái máy chủ hiện tại.

### thieu-hien-vat-quyet-dinh-h-va-chi-phi  [P1]  Nguồn chi phí thay thế chưa tái lập bảng quyết định GATE

TỆP/DÒNG: `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:110`; `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:152`, `:158`, `:160`, `:161`, `:163`, `:186`; `ops/reviews/pr468-hoso-4-packet-review-6-codex/nen-a1-a5/buoc.tsv:1`; bảng chiếu Issue #463:45–50.

VẤN ĐỀ: Nguồn mới được giới thiệu để thay nguồn vắng. Tái sinh13run/26job/1140bước thành công, nhưng đối chiếu đúng11head và đúng bộ lọc cả hai bước/cả hai job success cho **4/7 trung vị không khớp**: registry1.21254355 (khai1.20), packet-loop2.36929461 (2.35), G52.39655172 (2.39), receipt-v27.79292929 (7.56). Với receipt-v2, xét sai số±0.5giây từng mốc số đo như đặc tả vẫn cho dải[7.70517771,7.88248634], không phải[7.48,7.65]. Các n/min/max vẫn khớp, nên chỉ kiểm số dòng hoặc hai đầu dải sẽ bỏ qua sai lệch này. Không thể dùng gói mới làm bằng chứng rằng nguyên bảng quyết định cũ đã được tái lập. Bộ2062hàng/19Ubuntu gốc vẫn thiếu. Phần corpus H đã được thay/rút đúng không còn là lý do riêng để giữ finding này.

ĐÃ THỬ VÁ: đã tái tính từ giây gốc và ghi từng cặp vào `nen-measurements.json`, không sửa đặc tả đóng băng. Hướng xử lý tại bảng GATE và Issue #463: giao đúng nguồn của bảng cũ hoặc revision đồng bộ bảng/cỡ mẫu/băm/lease theo dữ liệu được chọn; giữ riêng dữ liệu lịch sử không dùng làm quyết định. Ca khóa: với danh sách run cố định, chọn cùng bước/success, lấy median của các tỷ lệ và kiểm từng ô, kể cả dải sai số. Rủi ro: sửa mỗi số trung vị mà không sửa mẫu số/dải sai số/bản chiếu sẽ tạo mâu thuẫn mới. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 do-review7/measure_costs.py` chạy bản sao nguyên `tinh.py`, bốn đầu ra khớp byte, rồi tính độc lập từ TSV. Receipt-v2 có10cặp; hai cặp giữa theo thứ tự là343/45 (`c0f18ac`) và438/55 (`0c3405f`), median=(343/45+438/55)/2=7.79292929. 9tên hiện vật lịch sử kiểm qua `git ls-files` không có; không kết luận tệp thiếu có số đúng. Chi phí126.22 khớp phép tính trên các ô phút **đã làm tròn** theo lời chú thích; từ giây gốc là126.23333333, chênh này không được tính thành finding. Nguồn MCP thật và bảng2062gốc **KHÔNG ĐO ĐƯỢC** offline.

ĐỘ TIN: cao về sự không khớp nội bộ; không xác định bảng cũ hay dữ liệu chép tay mới phản ánh GitHub đúng hơn.

### a9-khai-sai-base-ngoai-le  [P2]  Đính chính mới vẫn ghi sai kết quả BASE ở cặp đột biến

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:775`, `:847`; `ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md:75`.

VẤN ĐỀ: Đã sửa đúng BASE ném `ValueError` khi nhóm CA có5000chữ số, nhưng lại nói BASE trả1 khi số dài nằm ngoài nhóm bắt, ở cặp đột biến. Với CA xanh, BASE không đọc cặp đó nên **nhận xanh, chay_moi trả0**. Lỗi mới lặp ba chỗ; việc không đọc một vùng không khiến BASE tự đếm nó đỏ. D9 vẫn là ranh giới đã công khai, không tính thành phản chứng Đ1 mới; H ném ngoại lệ là fail-closed, không khai thành lỗ xanh H.

ĐÃ THỬ VÁ: thử fixture giống hệt ở cả hai vế, chứng minh hướng sửa văn bản thành BASE0 cho đúng fixture này; không áp lên spec. Cần sửa đồng thời ba chỗ và đính fixture nguyên byte, không khái quát cho mọi chuỗi có số dài. Ca khóa: CA xanh + mutant dài ở pretooluse/mcp cho BASE0/HValueError; CA dài cho cả haiValueError. Rủi ro: dùng fixture thiếu terminator/CAđỏ sẽ cho BASE1 vì lý do khác rồi che lỗi lời khai. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 do-review7/static_checks.py`; `static.json.d9` giữ đủ bốn đầu vào nguyên byte. Ví dụ `TONG: CA39/39 dat · DOT BIEN<5000 số9>/<5000 số9> bi giet` với khoảng trắng và dòng kết đúng như fixture: BASE0, HValueError. Tương tự mcp có hai dòng tổng CA/đột biến và terminator: BASE0, HValueError. Đặt số dài ở CA hoặc dòng nhanh: BASE=H=ValueError. Không thay Python int limit.

ĐỘ TIN: cao.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  GATE vẫn vừa đóng băng A1 vừa yêu cầu nới theo một mẫu khác tải

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:114`, `:122`, `:430`, `:440`, `:598`; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:33`.

VẤN ĐỀ: Biên độ10.28phút được gọi là nhiễu runner/phương sai, dùng để yêu cầu nới A1, trong khi A1≤25 và cấm nới vẫn còn. Mẫu11head có1workflow39bước,10workflow40bước, nên chưa tách được tác động tải khỏi runner. Nguồn mới còn cho5run master,6run nhánh khác với cả pull_request/workflow_dispatch; run60.17phút cancelled cũng là nhánh `claude/tra-luat-process-review-o4d7kb`, không phải run master như tiêu đề. “Sau này các commit vào master” không biến head_branch của run cũ thành master. Biên độ cũng không là phương sai.

ĐÃ THỬ VÁ: không tự chọn ngưỡng hoặc sửa spec đã được lease đóng băng. Cần chủ kho revision nếu đổi acceptance; trong lúc chưa có revision, giữ ngưỡng A1 và báo kết quả thật. Ca khóa: so cùng head/cùng tập bước/event trước khi quy biến động cho runner; kiểm hai đoạn không còn cho hai phán quyết với cùng một thời lượng. Rủi ro: thay ngưỡng bằng toàn biên độ quan sát có thể hợp thức hóa chính mức chậm cần phát hiện. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `measure_costs.py` lấy YAML bằng `git show` ở đủ11head và đối chiếu metadata13run: 1×39+10×40bước;5master+6nhánhkhác trong11mẫu. Số học dải10.283333phút khớp khi làm tròn; nó không chứng minh nguyên nhân. Phản mô hình28phút: A1≤25 bác, ngưỡng minh họa21.03+10.28=31.31 nhận. Đây không phải ngưỡng author đã chọn. GitHub/độ nhiễu runner thật **KHÔNG ĐO ĐƯỢC**.

ĐỘ TIN: cao về mâu thuẫn văn bản và khác mẫu; không ước lượng nhân quả runner.

### issue-lo-neo-commit-cu-kem-bam-moi  [P1]  Issue #464 đóng băng hai bản đặc tả khác nhau cùng lúc

TỆP/DÒNG: `ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md:132`, `:133`; `ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap:48`.

VẤN ĐỀ: Băm LO trong lease nháp và Issue đã đổi sang `730033f0…` đúng với tệp hiện tại. Nhưng dòng “Đặc tả đóng băng” của Issue vẫn neo commit `b743f1798aba12615f903a11bd451c87e404814e`. Blob LO ở commit đó có băm `3aafd766…`, thiếu đính chính lượt6. Người lấy đúng commit được chỉ dẫn sẽ đọc hợp đồng cũ và fail khi so băm mới; người lấy HEAD sẽ đọc bản khác. Hai định danh không cùng chỉ một đặc tả đóng băng. Ba Issue khác không có lỗi này.

ĐÃ THỬ VÁ: kiểm hướng đổi mỏ neo sang commit đầu chứa LO mới `8c3e37184275b4e2230c593be56e4aa1cff0b9ea`; blob đó băm đúng730033f0… và bằng byte với HEAD. Không sửa Issue trong cây thật. Ca khóa: đọc blob `<commit>:<spec_path>`, băm và so đồng thời với Issue/spec_hash của lease; kiểm cả bốn packet. Rủi ro: trỏ tên nhánh/HEAD di động sẽ tái tạo drift; phải ghim commit chứa đúng nội dung và giữ đồng bộ băm. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 do-review7/static_checks.py`: băm spec hiện tại/lease/Issue4/4khớp, nhưng băm blob ở commit Issue chỉ3/4khớp; LO là mục lệch duy nhất. `git show b743f179:ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md` → SHA-256 `3aafd766abd1fdcfa55a23e2f2716efbcbd8dc2505ddf9fe6dc878074a675067`; cùng đường tại8c3e371/HEAD → `730033f0f534fb325598182e08068861e12033dcbf5e32484c4962b23b542caf`. Đây là finding từ phép kiểm ngoài các cổng EVIDENCE liệt kê.

ĐỘ TIN: cao.

## Giới hạn và bàn giao

**KHÔNG ĐO ĐƯỢC:** GitHub trực tiếp hoặc tính đầy đủ của mọi ref máy chủ; head master đúng giây cấp; quyền/branch protection; các session/model log nằm ngoài sandbox; nguồn MCP trước khi chép tay; nguyên bộ lịch sử311/419/2062 và bốn lý do hint đã rút; Windows thật; hóa đơn; stdout xanh pretooluse trong rig này; Đ4/Đ5 của mã H sau thi công. Không mục nào được đổi thành pass. Không chạy `packet_loop_test` hoặc nguyên `ci_dang_ky --chay` trên PR thuần hồ sơ này; các cổng và suite đã chạy ghi rõ bên trên.

Lỗi rig do reviewer đã xử lý: harness gói giữ layout sandbox cũ nên chạy trực tiếp FileNotFoundError; dựng ba symlink tạm giúp chạy nguyên mã trong kho. Chạy lease test đồng thời khi các symlink ấy còn tồn tại gây copytree vòng ở t82 (rc1); đã dọn hết, chạy lại sạch cho121/121 rc0. Không dùng lần lỗi đó làm finding PR. `do-review7/replay_package.py` mô tả cách dựng/dọn layout; chạy riêng, không chạy đồng thời với test sao chép toàn kho. Không sửa script/hàm H được giao để đạt1213/0/0.

Các hiện vật mới: `do-review7/static.json` (fixture D9 nguyên byte, snapshot lease, băm/mỏ neo), `nen-measurements.json` (từng cặp giây/tỷ lệ), `replay/` (kết quả nguyên script trong kho), các stdout/stderr và metadata lệnh. Không có patch vào branch. Hướng sửa kèm từng finding là gợi ý có giới hạn, không tự cấp authority cho executor.

''')
final_check=O/'final-check.json'
if final_check.exists():
    x=json.loads(final_check.read_text())
    lines.append(f"Kiểm cuối: HEAD={x['head']}; tree={x['tree']}; diff tracked rỗng={x['tracked_clean']}; status --porcelain rỗng={x['status_clean']}; manifest gốc rc={x['manifest_rc']} ({x['manifest_ok']}/62 khớp).\n\n")
lines.append('verdict: '+status+'\n')
(B/'VERDICT.md').write_text(''.join(lines))
print('Wrote',B/'VERDICT.md','status',status)
