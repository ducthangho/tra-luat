import datetime as dt,json,pathlib,sys
B=pathlib.Path(__file__).resolve().parents[1];O=B/'do-review8'
read=lambda n:json.loads((O/n).read_text())
S=read('static.json');H=read('replay-h.json');C=read('costs.json');K=read('contract-checks.json');F=read('followup-checks.json')
final='--final' in sys.argv;status='changes_requested' if final else 'dang-do'
P=read('pretooluse.json') if (O/'pretooluse.json').exists() else None
V=[]
def add(t=''):V.append(t)
def row(a,b,c,d='có'):add(f'| {a} | {b} | {c} | {d} |')
add(f'''# VERDICT — cross-review PR #468, lượt 8

verdict: {status}
reviewed_sha: 4d0ead5591a58463423754cc93a84ce744c3a50b

Kết luận nội dung: **changes_requested — 2 P1, 2 P2**. Sáu finding lượt 7 được giữ nguyên slug và tự đo: **4 ĐÃ VÁ THẬT, 1 VÁ HỜ, 1 CHƯA VÁ**. Hai finding mới là hợp đồng A2 dùng nền cũ và trạng thái chọn H chưa đồng bộ.

Reviewer: **Codex / OpenAI**, phiên độc lập qua API, có shell cục bộ; transport: tệp trong sandbox. Đã đọc protocol trích §8/12/13 trước và dùng khung `tai-lieu/cross-review-SKILL.md`. Chỉ đọc/ghi trong phạm vi PROMPT; không mạng, không commit/push, không đăng GitHub, không lập receipt hay cấp merge authorization. Chỉ thị offline ưu tiên bước đăng PR trong skill.

Các mốc đo là **07-09-2026 UTC**, trước hạn #456 **14:30:07Z**. Lệnh/script và hiện vật của reviewer nằm trong `do-review8/`. Đường `ops/...` và `.claude/...` bên dưới tính từ `cay-kho/`. Tái tính dữ liệu API đã lưu không được khai thành readback GitHub trực tiếp; replay stdout có rc ghi trong hồ sơ không được khai thành suite vừa chạy.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `span-rong-nuot-ti-le-vo-can` [P1]: **ĐÃ VÁ THẬT về nghĩa vụ bằng chứng còn mở ở lượt 7**. Nguyên harness/attack/extra-checks lượt 6, chạy trong layout riêng ngoài checkout, tái lập **1213 ca / 0 đỏ giả / 0 bỏ sót / 0 ngoại lệ**, corpus và summary khớp byte. Bản `outputs-that/pretooluse_guard_test.stdout` đúng **9995 B**, SHA-256 `69878c4f9efb24a6666d1cf0e4dea99d1ac87fa0aa904e28c6d397fd08cb7991`, metadata ghi **rc=0**, BASE/H replay đều **0**. Đủ **8/8** định dạng có bản xanh ghi rc0; H bác **0/8**. P1 thiếu bản thứ tám nay **đóng**. Đây là review thiết kế và evidence; không tuyên bố H đã thi công hay mọi nghiệm thu tương lai đã đạt. Suite reviewer tự chạy với Ruff0.15.15 cũng **rc0, CA39/39, mutant34/34, stdout9995B trùng từng byte**; H/BASE replay bản vừa chạy đều0. Đ1–Đ5 ở bảng dưới.
- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **CHƯA VÁ tại thời điểm đo**. Quét thật lúc **09:21:30.927918Z**, xác nhận lại **09:30:02.764850Z**: **86** cặp blob/path, **2** blob #456; một có bia mộ đối xứng, một còn hạn chưa bia mộ. Registry có **2** người giữ, `ci.yml` có **1**. Blob cũ tồn tại trên **origin/master** thật trong snapshot, không chỉ ref GATE cục bộ. Mô phỏng **14:30:06Z → 14:30:07Z** cho registry **2 → 1**; không đổi thành trạng thái đã xảy ra. P1 còn mở; không tính lỗi rig. Chuỗi r2 không làm mất blob cũ.
- `thieu-hien-vat-quyet-dinh-h-va-chi-phi` [P1]: **ĐÃ VÁ THẬT đối với nguồn quyết định hiện hành**. Nguồn **13 run / 26 job / 1140 bước** tái sinh các đầu ra khớp byte. Chọn đúng **11 run**, cả hai job/bước success và tên `tl selftest` theo tiền tố: **28/28** ô n/min/max/median, **12/12** đầu dải làm tròn của GATE r2 khớp. Receipt-v2 trung vị **7.7929292929×**, dải **7.7051777052–7.8824863416×**. Băm spec r2 bằng lease exec-1r2 và blob Issue neo; `check` rc0. Không đòi nguồn 2062 hàng đã được rút khỏi vai trò nguồn hiện hành. Các câu phân loại mẫu/Issue còn cũ được giữ ở finding P2 riêng, không đánh đồng với việc bảng tỷ lệ đã tính đúng.
- `issue-lo-neo-commit-cu-kem-bam-moi` [P1]: **ĐÃ VÁ THẬT**. Tự đọc blob `<commit>:<spec_path>` cho cả bốn packet: **4/4** khớp spec hiện tại, hai trường hash lease và hash Issue. #463/#464 neo `d85365463259615537c4fb96acd2408d917d9bd2`; #465/#466 giữ `b743f1798aba12615f903a11bd451c87e404814e` và vẫn đúng. Bản chiếu `tai-lieu/` khớp byte.
- `a9-khai-sai-base-ngoai-le` [P2]: **ĐÃ VÁ THẬT**. Bốn fixture nguyên byte, hai formatter × hai vị trí số **5000** chữ số: ở CA, **BASE=H=ValueError**; ở cặp đột biến, **BASE=0/H=ValueError**. Đúng cả LO A9, LO `chua_do_duoc` D9 và Issue #464. Không đổi Python int limit; ngoại lệ H là fail-closed, không tính thành phản chứng Đ1 mới.
- `bien-do-khac-head-khong-phai-nhieu-runner` [P2]: **VÁ HỜ**. R2 đã sửa A1 giữ **≤25,00**, rút yêu cầu nới theo phương sai ở `chua_do_duoc` #3 và nêu nợ `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`. Tự đo đúng **5 master/push + 6 nhánh**, **1×39 + 10×40** bước. Nhưng GATE:97,195 còn gọi mười một/mọi lượt master; Issue #463:13,33–36 vẫn ghi run cancelled trên master và suy biên độ là nhiễu làm A1 không đáng tin. Issue:61–62 còn nói revision chưa làm trong PR này dù :119–125 đã neo r2. Cần đồng bộ phần còn lại, không nới A1.

## BẢNG ĐO

Bảng ghi cả phần khớp, lệch và không đo được. Giây/tỷ lệ chưa làm tròn, từng cặp run và mọi fixture nằm trong `static.json`, `costs.json`, `replay-h.json`, `contract-checks.json`, `followup-checks.json`; metadata từng lệnh có thời điểm, rc, thời lượng và SHA-256 stdout. `0` của `chay_moi` là số mục đỏ, không phải Boolean False.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|''')
row('HEAD / tree','exact reviewed_sha',S['head']+' / '+S['tree'])
row('Môi trường git','abbrev=7, không shallow, sạch','7; false; status đầu rỗng')
for key,label in [('since7','Diff từ lượt 7'),('full','Toàn PR so origin/master')]:
 d=S['diffs'][key];row(label,'patch + numstat được giao',f"{d['files']} tệp; +{d['additions']}/−{d['deletions']}; patch/numstat khớp byte; ngoài ops={len(d['outside_ops'])}")
row('Manifest hiện vật lượt 6 / 7','băm bất biến','62/62 và 66/66 khớp; không bao quát các tệp ngoài danh sách manifest')
d=S['receipt'];row('Receipt lượt 7','v2 / SHA lượt 7 / băm nguyên văn',f"v2; reviewed_sha={d['reviewed_sha']}; {d['bytes']} B; {d['hash']}; cả bytes/hash khớp")
for d in S['leases']:
 row(f"Spec–Issue–lease #{d['issue']}",d['hash_declared'],f"băm blob/spec/tai-lieu={d['hash_actual']}; revision={d['revision']}; số đường write set={len(d['write_set'])}; null={len(d['null_keys'])}")
row('Lease r2: 3 neo','head master lúc cấp','3/3=d28c4b1062e8505cbdaaf0237fcbe3f9b8ee4705','khớp snapshot; GitHub đúng giây cấp KHÔNG ĐO ĐƯỢC')
row('Lease r2: write_set_hash','sort + LF + LF cuối',S['gate']['write_set_hash_actual'])
row('Lease r2: hạn / heartbeat','24 giờ; heartbeat=mốc cấp','cấp/heartbeat=2026-09-07T07:50:35Z; until=expires=2026-09-08T07:50:35Z; 1440 phút')
row('Lease r2: authority / replacement','revision2 + comment URL + thay exec-1','granted_on_instruction=URL comment #463/5567157629; thay_the_cho=[exec-1]; exec-1.da_bi_thay_the=exec-1r2','có trong hồ sơ; comment trực tiếp KHÔNG ĐO ĐƯỢC')
row('Chuỗi ba lease trên cây PR','hai chiều #456→exec-1→exec-1r2','cả 2 cạnh có bia mộ đối xứng; exec-1 bị thay; chỉ r2 giữ ci.yml; chú thích lịch sử không thay key YAML')
row('Snapshot mọi ref cục bộ','registry2; ci.yml1','86 cặp blob/path; #456 có 2 blob, chỉ 1 bia mộ; ci.yml=1, registry=2, subagent=0, nhanh=0')
row('Blob #456 trên master','chưa bia mộ',F['master_old_blob']+'; bằng blob cũ được scanner ghi trước ở ref GATE')
row('Hết hạn #456','14:30:07Z','14:30:06Z registry=2; 14:30:07Z registry=1','khớp mô phỏng, chưa phải readback tương lai')
row('Thu hồi mọi bản #456','cần mọi ref hết giữ bản còn hạn','mô hình bia mộ mọi bản: registry2→1; chỉ sửa bản PR đã có bia mộ thì vẫn2','có; không sửa ref')
row('Nguồn A1/A5','13 run / 26 job / 1140 bước','đúng; job.tsv14 cột, buoc.tsv9 cột; 1140/1140 số giây khớp timestamp; 4 đầu ra tái sinh khớp byte')
row('11 run / workload','5 master+6 nhánh; 1×39+10×40 bước','đúng theo metadata và YAML của 11 head','có; câu cũ còn mâu thuẫn')
s=C['sample']['windows_stats'];row('Thống kê 11 job Windows','n11; 40,20–50,48; median46,02; mean45,84; biên10,28',f"n={s['n']}; min={s['minimum']:.10f}; max={s['maximum']:.10f}; median={s['median']:.10f}; mean={s['mean']:.10f}; biên={s['range']:.10f}; biên trần60=19,80→9,5166666667 phút")
for name,d in C['ratios'].items():
 expected=' / '.join(d['expected'])+(' / '+ '–'.join(d['range_expected']) if d['range_expected'] else ' / —')
 measured=f"n={d['n']}; min={d['minimum']:.8f}; max={d['maximum']:.8f}; median={d['median']:.8f}; mean={d['mean']:.8f}; biên={d['range']:.8f}; dải median={d['rounding_lower']:.8f}–{d['rounding_upper']:.8f}"
 row('Hệ số '+name+' (n/min/max/median/dải)',expected,measured,'có; job không khai dải nên dải job chỉ là tính bổ sung')
row('Toàn bảng hệ số r2','7 dòng + dải','28/28 ô n/min/max/median + 12/12 đầu dải khớp định dạng làm tròn')
for d in C['eleven']:
 row('Run '+d['run']+' / '+d['head'],'bảng 11 run',f"{d['branch']} / {d['event']}; YAML {d['steps']} bước; Windows {d['windows_seconds']:.0f}s = {d['windows_minutes']:.8f} phút")
row('Run cancelled34048229370','r2: nhánh, không master','4cd80c5; claude/tra-luat-process-review-o4d7kb; workflow_dispatch; windows cancelled; 3610s=60,1666666667ph','có ở spec r2; Issue còn sai nhãn master')
for plat,d in C['costs'].items():
 row('Chi phí run nhánh34045664423 / '+plat,'phân rã lịch sử làm nền ước', '; '.join(f'{k}={v:.8f}' for k,v in d.items())+' phút','khớp giây nguồn; các ô dự toán dùng số phút đã làm tròn')
row('43,20→21,03 và giữ chữ trong r2','job nhánh → ước sau tách','43,2; 17,7+3,3333333333=21,0333333333; không dùng tập 11 run để sinh hai số này','có; không mâu thuẫn 5 master+6 nhánh')
row('Billing A5','110,65→126,22; +15,57/+14,1%','110,65 từ giây gốc; 126,22 từ các ô phút đã làm tròn theo chú thích; từ giây gốc126,2333333333','có theo cách tính công khai; không coi 0,0133333333 là finding')
row('Ngưỡng A1/A5','≤25,00 / ≤135,00','giữ đúng cả hai; sửa câu phân loại mẫu trong bộ nhớ không đổi ngưỡng hoặc số43,20/21,03')
row('A2 cùng độ phủ','tập phải bằng trước tách','A2 cũ=86 bộ ba; lease base/tách đủ=88; delta2 receipt-v2, không mất bộ ba nào','KHÔNG; finding P1 mới')
row('A2 phản mô hình','không mất bước','tách đủ: M2=True/A2=False; bỏ receipt-v2: A2 cũ=True; nền cùng lease: tách đủ=True, bỏ bước=False','chứng minh mâu thuẫn riêng A2; không khai toàn bộ gate bị vượt')
row('Consumer / H layout','8 SPAN giữ nguyên; 2 dạng Windows','consumer tai-lieu bằng byte cây; 8/8 SPAN giữ nguyên; cả 8 MOI đổi kiểu; 2 dạng Windows đúng thứ tự')
row('Hai khối H','băm spec bằng harness','TONG='+H['blocks']['h_tong.py']+'; predicate='+H['blocks']['h_predicate.py'])
row('Corpus H','1213/0/0/0','1213/0 đỏ giả/0 bỏ sót/0 ngoại lệ; cases/summary khớp byte; 3/3 script nguyên byte rc0')
row('Phân rã corpus','bộ độc lập lượt 6','; '.join(f'{k}={v}' for k,v in H['corpus']['by_kind'].items()))
for d in H['mutants']:row('Mutant '+d['name'],'5/51/42/0 đổi màu theo thứ tự',f"đổi màu={d['changed_count']}; ngoại lệ={d['exception_count']}; ngoại lệ không tính là răng")
for d in H['d2']:row('Đ2 '+d['path'],'stdout có rc0 trong hồ sơ',f"{d['bytes']} B; sha256={d['sha256']}; rc ghi={d['rc_recorded']}; BASE/H={d['BASE_red']}/{d['H_red']}",'có; replay')
row('Đ2 tổng','8/8 bản xanh','rc0 theo hồ sơ8/8; H bác0/8; hai bản bổ sung khớp bytes/hash riêng; không tự tạo rc0')
for name,d in H['d9'].items():row('D9 '+name,'5000 chữ số ở CA hoặc mutant',f"BASE={d['BASE']}; H={d['H']}; fixture nguyên byte tại replay-h.json")
row('Quyết định §12 / nháp LO','chủ kho chọn1, khi cấp neo comment','cùng URL #464/5567158069 ở3/3; lựa chọn1 ở3/3; granted_on_instruction vẫn null; 2 câu phủ định cũ còn lại','chưa nhất quán; không coi nháp chưa cấp là lỗi')
for n in ['doctrine-scan','adr-song','doc-claims','ci-dang-ky','bien-nhan-v2','lease-check','lease-publish-test']:
 d=read(n+'.json');details={'doctrine-scan':'7 tệp; 0 chỗ chép','adr-song':'46/46; ngoại lệ ADR0016','doc-claims':'ok=true;106 tệp;advisory=367','ci-dang-ky':'PHẢN CHỨNG51/51;TỔNG ĐẠT','bien-nhan-v2':'22 v2;11/11 miễn legacy;42 nợ;0 vi phạm;0 KHÔNG ĐO ĐƯỢC;tổng75','lease-check':'ĐĂNG ĐƯỢC;không chạy kiểm GitHub','lease-publish-test':'121/121;đã chạy121,bỏ qua0'}[n]
 row('Cổng '+n,'EVIDENCE rc0',f"rc={d['rc']}; {d['seconds']:.3f}s; {d['stdout_bytes']} B stdout; {details}")
row('Ruff suite pretooluse / Python D9','Ruff0.15.15; không đổi int limit','PATH=/usr/local/bin:$PATH; ruff --version=0.15.15; Python3.11.15; int limit4300')
if P:
 row('Suite pretooluse tự chạy','xanh và băm khớp bản9995B',f"start={P['start_utc']}; end={P['end_utc']}; rc={P['rc']}; {P['seconds']:.3f}s; {P['stdout_bytes']}B; sha256={P['stdout_sha256']}",'có' if P['rc']==0 and P['stdout_sha256']==H['d2'][5]['sha256'] else 'xem giới hạn/đối chiếu bên dưới')
else: row('Suite pretooluse tự chạy','thử tái lập bản xanh','đang chạy lại; lượt đầu không thu được hiện vật hoàn tất','chưa kết luận')
if (O/'pretooluse-replay.json').exists(): row('Replay stdout suite vừa chạy','khớp bản xanh đã giao','rc0; CA39/39; mutant34/34; 9995B trùng từng byte; BASE/H=0/0')
add('''
Đối chiếu riêng các điều kiện chuyển hướng H trong LO-319:

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Đ1 | ≥1 phản chứng ngoài ranh giới ⇒ dừng H | Không tìm thấy trên corpus1213 đã tái lập; D9 thuộc ranh giới công khai | chưa chạm ngưỡng; không tuyên bố chứng minh mọi đầu vào |
| Đ2 | ≥1 bản formatter xanh bị H bác ⇒ dừng H | H bác0/8 stdout có rc0 trong hồ sơ; bytes/hash pretooluse mới khớp | chưa chạm ngưỡng; A6 của phiên thi công vẫn phải chạy |
| Đ3 | formatter/packet hiện có cần metadata n/m trên tổng ⇒ revision | 8 bản xanh và bốn packet được giao không cung cấp nhu cầu này; grammar vẫn công khai bác schema1/2 | chưa thấy kích hoạt trong phạm vi; không suy toàn bộ packet máy chủ |
| Đ4 | additions runtime>300 ⇒ dừng | diff ci_dang_ky_test.py của PR này rỗng, additions0; H chưa thi công | implementation tương lai KHÔNG ĐO ĐƯỢC, không đóng Đ4 |
| Đ5 | sau thi công phải N/N, N≥51+số ca mới | consumer hiện tại chạy51/51; đây là BASE, không phải bộ phản chứng H sau thi công | KHÔNG ĐO ĐƯỢC nghiệm thu tương lai, không lấy51/51 thay nó |

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Blob lease #456 còn hạn trên master vẫn giữ registry

TỆP/DÒNG: `ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml:39` trên `origin/master` (blob `8b2103c06687546379a17f6deafc97f1fe0173fd`); bản có bia mộ trong cây PR; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:108–115`; `ops/leases/gate-tach-job-cat-chi-phi-exec-1r2-claude-20260906.yaml:120–126`.

VẤN ĐỀ: Chuỗi #456→exec-1→exec-1r2 trên cây PR đúng hai chiều nhưng scanner đếm từng `(blob,path)` trên mọi ref. Bản #456 chưa bia mộ trên master còn hạn tới14:30:07Z, cùng exec-1r2 giữ `ci_dang_ky_test.py`. Lời khai đã sửa đúng rằng phải đo lại mọi ref sau merge, nhưng trạng thái cần đóng vẫn chưa đạt ở lượt này. Không gọi đây là lỗi rig hay suy từ nhánh GATE cục bộ rằng master đã hết giữ.

ĐÃ THỬ VÁ: thử mô hình đánh bia mộ **mọi** bản #456 trong bộ nhớ → registry2→1; không sửa ref/lease thật. Hai hướng executor có thể kiểm: chờ hết hạn rồi fetch đủ ref/readback, hoặc làm thủ tục thu hồi có thẩm quyền trên mọi ref đang giữ blob cũ. Ca khoá: một bản mới có bia mộ + một bản cũ còn hạn phải vẫn đếm2; mọi bản bị thu hồi hoặc hết hạn thì đếm1 (chỉ r2). Rủi ro: cập nhật riêng master nhưng còn ref khác sẽ tái tạo cửa sổ hai writer. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/static_checks.py` và `followup_checks.py`, rc0; dùng `_quet_lease_toan_kho(..., doi_chieu_ref=False)`, `_phan_loai_lease`, `_bia_mo_doi_xung` thật. Registry2 ở09:21/09:30Z; mô phỏng14:30:06Z→14:30:07Z cho2→1. `git rev-parse origin/master:ops/leases/<id>.yaml` xác nhận blob cũ trên master. Tắt đối chiếu ref máy chủ chỉ để đo snapshot được giao, không dùng số này để chứng nhận toàn bộ GitHub; `check` rc0 không thay kiểm chồng lấn.

ĐỘ TIN: cao với snapshot và mô phỏng; trạng thái GitHub trực tiếp KHÔNG ĐO ĐƯỢC.

### a2-neo-nen-cu-trai-write-set-hien-tai  [P1]  A2 dùng nền 39 bước trái lease hiện tại 40 bước

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:433`, `:457–462`, đối chiếu thông tin r2 ở`:121–123`; `ops/leases/gate-tach-job-cat-chi-phi-exec-1r2-claude-20260906.yaml:81–83`.

VẤN ĐỀ: A2 vẫn bắt buộc so với run34048685345/head1b3caa1 trong khi lease neo d28c4b1. Nền lease đã thêm `bien-nhan v2 selftest`, có40 bước YAML thay vì39. Ngay cả trong trường hợp lý tưởng mọi conclusion giữ nguyên, tách đúng theo M2 cho88 bộ ba còn nền A2 chỉ86. Xoá receipt-v2 trên hai nền lại khớp A2 cũ dù mất độ phủ. R2 đã biết39/40 nhưng chưa cập nhật phép so nghiệm thu; executor không thể vừa giữ đủ bước hiện tại vừa đạt nền cũ. Đây là mâu thuẫn hợp đồng và lỗ của **riêng phép so A2**, không tuyên bố đã vượt toàn bộ các tiêu chí khác.

ĐÃ THỬ VÁ: thử đổi nền phép so sang đúng lease base trong mô hình ngoài checkout: tách đủ bước qua, bỏ receipt-v2 bị bác. Cần sửa A2 để lấy baseline thực sự trước tách tại exact base, cùng event/lane/ma trận như lượt sau; lưu hai bộ dữ liệu nguyên vẹn. Không miễn riêng receipt-v2, không đổi so tập thành số đếm. Ca khoá: một baseline đã có bước mới, dời job đủ bước phải qua; xoá bất kỳ bước/bộ ba phải đỏ. Rủi ro: chỉ đổi SHA nhưng giữ phép so dispatch-nhánh với push-master còn tạo delta `success/skipped` do lane; phải ghim cả ngữ cảnh chạy. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/contract_checks.py`, rc0, phần`a2`. Từ TSV, dời hai bước nặng và nhân9 bước thiết lập2–10; bỏ cột job đúng A2: M2=True, A2 cũ=False, thêm đúng2 bộ ba receipt-v2 và không mất mục nào. Bỏ receipt-v2 → A2 cũ=True, so cùng base=False. `git show` xác nhận39→40 bước. Mô hình không thay `ci.yml`, không thực thi CI mới, không giả lập rằng GitHub đã chạy. Finding không nằm trong bảng cổng EVIDENCE; nó được phát hiện khi kiểm sự nhất quán giữa revision2 và phần nghiệm thu giữ lại.

ĐỘ TIN: cao.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  Revision 2 chưa gỡ hết lời khai master và suy luận nhiễu cũ

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:95–97`, `:195–196`, so với`:121–133`, `:612–618`; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:13`, `:33–36`, `:61–65`, so với`:119–125`.

VẤN ĐỀ: Phần đã sửa nói đúng5 master+6 nhánh và rút quyền nới A1; phần còn lại vẫn khẳng định mười một/mọi lượt master. Issue vẫn lấy10,28 làm “nhiễu” và hệ quả cứng cho A1, còn gọi run cancelled là master dù metadata là workflow_dispatch trên nhánh. Issue đồng thời nói revision “chưa làm ở PR này” và đóng băng revision2 phía dưới. Bảng tỷ lệ r2 đã đúng, và các số43,20/21,03 là run nhánh riêng nên **không** phải lỗi; lỗi là hai cách mô tả mẫu và trạng thái revision cùng còn hiệu lực.

ĐÃ THỬ VÁ: tính lại đầy đủ từ giây và thử thay các câu master/pending-revision trong bộ nhớ; các câu cũ mất, A1≤25/A5≤135 và43,20/21,03 được giữ. Cần đồng bộ các đoạn dẫn/Issue thành mô tả đúng mẫu và r2 đã cấp; nếu giữ bảng cũ làm lịch sử thì ghi rõ revision1 ở ngay bảng và không dùng7,56 như kết luận hiện hành. Ca khoá: danh sách11 run phải ánh xạ5/6; run cancelled phải là nhánh; mọi đoạn nghiệm thu giữ cùng ngưỡng; không câu hiện hành nào gọi mẫu này là mọi lượt master hoặc suy jitter thuần. Rủi ro: sửa riêng tiêu đề hoặc trung vị lại bỏ sót bản chiếu, hoặc vô tình đổi ngưỡng để ép xanh. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/measure_costs.py` và `followup_checks.py`, rc0. YAML11head=1×39+10×40; metadata=5master/push+6nhánh; biên10.28333333phút là range, chưa đo được phương sai runner cùng head/tập bước/event. Ba câu stale cụ thể hiện diện3/3; hướng thay trong bộ nhớ gỡ3/3 và giữ các ngưỡng. Cổng doc-claims vẫn xanh367advisory, nên không thay thế đối chiếu này.

ĐỘ TIN: cao về mâu thuẫn nội bộ; không suy nguyên nhân biến động runner.

### quyet-dinh-tiep-h-con-bi-phu-dinh  [P2]  Quyết định chọn H mới vẫn bị câu cũ phủ định

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:255–260`; `ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap:28`, `:119–123`; bản chọn nhất quán ở`ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md:53`.

VẤN ĐỀ: LO/Issue ghi chủ kho chọn1—tiếp H, ghi chú lease neo cùng comment. Nhưng ngay dưới quyết định LO vẫn đặt tiêu đề H “CHƯA được chọn”, và thân`ly_do_cap` của lease nói “Spec KHÔNG khai §12 đã xong” rồi để ba lựa chọn cho chủ kho quyết. Trạng thái quyết định chưa được đồng bộ giữa phần mới và phần cũ. Không coi5ônull của lease nháp là lỗi: chọn thiết kế không tự cấp lease và không miễn Đ1–Đ5.

ĐÃ THỬ VÁ: thử gỡ hai câu phủ định trong bộ nhớ, giữ URL và`granted_on_instruction=null`. Executor cần đồng bộ trọn đoạn lý do/tiêu đề thành quyết định thiết kế đã có, thi công chưa bắt đầu, lease chưa cấp và Đ1–Đ5 tiếp tục ràng buộc; phần ba lựa chọn nếu giữ phải gắn lịch sử. Ca khoá: cùng URL/lựa chọn ở ba hồ sơ, không còn câu hiện hành nói chưa chọn; null của nháp vẫn null. Rủi ro: sửa thành “đã cấp” hoặc “mọi điều kiện đã đạt” sẽ tạo authority hoặc evidence không có. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/contract_checks.py`, rc0, phần`h_decision`: URL/lựa chọn3/3, còn2câu phủ định; hướng thay gỡ2/2 và giữ URL/null. Quyền và nội dung comment GitHub trực tiếp KHÔNG ĐO ĐƯỢC theo phạm vi offline.

ĐỘ TIN: cao về mâu thuẫn văn bản; không chứng nhận độc lập comment chủ kho.

## Giới hạn và bàn giao

**KHÔNG ĐO ĐƯỢC:** GitHub trực tiếp/tính đầy đủ mọi ref máy chủ; master đúng giây cấp r2; quyền và nội dung gốc hai comment chủ kho; branch protection; Windows thật; hóa đơn và runner jitter; dữ liệu lịch sử2062hàng/19jobUbuntu, corpus311/419 và provenance đã rút; Đ4/Đ5 của implementation H tương lai. Không mục nào được đổi thành pass. Không chạy`packet_loop_test` hoặc toàn bộ`ci_dang_ky --chay` trên PR thuần hồ sơ này.

Tái lập môi trường: `core.abbrev=7`; dùng nguyên script lượt6 nhưng **chép sang layout riêng ở `do-review8/rig/`**, symlink chỉ hướng vào cây đọc/tài liệu; không đặt vòng symlink trong checkout. Test lease121/121 chạy xanh ngay. Lượt pretooluse đầu không thu được metadata/stdout hoàn tất, không dùng làm bằng chứng; lượt chạy lại có session được chờ để lấy rc thật. Không gán trục trặc thu hiện vật của reviewer cho PR.

Hiện vật chính: `do-review8/replay-h.json` và`rig/do-review/` (corpus, H trích, mutant); `costs.json`/`nen-a1-a5/` (mọi cặp giây và bảng tái sinh); `static.json` (băm, receipt, snapshot, mô phỏng hết hạn); `contract-checks.json` (phản mô hình A2 và trạng thái §12); `followup-checks.json` (master blob, mô hình thu hồi mọi bản, thử sửa câu stale); stdout/stderr/metadata các cổng. Hướng sửa là gợi ý dữ liệu có giới hạn, không phải quyền ghi branch hay duyệt self-review.
''')
if (O/'final-check.json').exists():
 d=read('final-check.json');add('Kiểm cuối: HEAD='+d['head']+'; tree='+d['tree']+'; tracked diff rỗng='+str(d['tracked_clean'])+'; status rỗng='+str(d['status_clean'])+'; commits sau reviewed_sha='+str(d['new_commits'])+'.')
add('\nverdict: '+status)
(B/'VERDICT.md').write_text('\n'.join(V)+'\n')
print('VERDICT.md',len(('\n'.join(V)+'\n').encode()),'bytes;',status)
