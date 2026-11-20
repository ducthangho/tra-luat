import hashlib
import json
from pathlib import Path

W=Path(__file__).resolve().parent
R=W.parent/'repo'
old=json.loads((W.parent/'lich_su/VERDICT_vong4_codex.json').read_text())
v=json.loads((W/'VERDICT.json').read_text())
H='4b5e3c6b15eb311540447d67d0e0ad62a85e71d1'
S='9816599335afce624a058b445f0d9d85b1683fcc32aa232b874fa43b506c63ff'
v.update(review_state='verification_in_progress', verdict='changes_requested')
v['findings']=[
 {
  'id':'V01','class_slug':'nghiem-thu-khong-co-lap-chot-dich','severity':'P2',
  'vi_tri':'SPEC.md:316–337 (Ma trận, luật 3–5), đối chiếu :113–141, :182–183 và :291–309',
  'van_de':'Phép kiểm đóng lớp mới chưa xác định được một tập quét có thể tái lập và một ma trận consumer khả thi. Danh sách (a)–(l) được gọi là HỢP mọi toán tử lượt 6 nhưng thiếu các phép biến đổi đã dùng; quy tắc sinh cho một số toán tử còn để executor tự chọn. Luật 5 giữ được các mẫu hồi quy cũ, nhưng không định nghĩa phép quét tổng quát thay thế hoặc cách chạy cùng phép đo trên head mới.',
  'bang_chung':[
   'SPEC:318–324 chỉ quy định bỏ thành phần lớp ký tự/alternation, nới lượng từ, bỏ strip/casefold và return→None. make_independent.py/make_extra.py của lượt 6 còn có: mở rộng lớp ký tự (ref_any_run), bỏ escape literal thành wildcard (ref_txt_wild), thay isalnum bằng isalpha (key_alpha_only), ngừng duyệt con metadata (phi_skip_descendants), đổi so tập chính xác thành so chuỗi con (phi_substring), và 23 delete_return_* dùng pass để tiếp tục control flow. Return None không tương đương bỏ return. Hai phép đầu không phải bỏ thành phần lớp ký tự; các phép thay predicate/duyệt con cũng không được nêu trong (a)–(l). Một số có thể được người triển khai tự diễn giải vào (k), nhưng đặc tả không chốt diễn giải ấy.',
   'Phép đo độc lập: python3 -B ../work/audit_method_r5.py rc0, METHOD_R5_COMPLETE. Trên bản sao/fragment hồ sơ pr1453 và fixture T-v2-pass, 5/5 mutant được giao (ref_any_run, ref_txt_wild, key_alpha_only, phi_substring, phi_skip_descendants) làm kiem_ho_so từ danh sách vi phạm thành []; healthy control []. Băm mutant khớp hiện vật gốc. Đây là đối chứng trên c2d606b cho ý nghĩa của các toán tử, KHÔNG phải phát hiện r10 có mã lọt. audit_method_r5.json lưu từng cặp kết quả.',
   'Luật 3(g) không chốt thay literal bằng giá trị nào; (h) không chốt phần tử thêm vào từng tập/dict; (i) không chốt các phép nới lượng từ (hữu hạn nào, áp vào range/escape ra sao). Vì vậy hai bộ sinh cùng khai đủ a–l có thể sinh hai mẫu số khác nhau. :327–328 cho bộ quét ngoài kho chỉ nộp băm và biên nhận, không bắt buộc giao bytes script/dependencies hoặc manifest từng mutant/target. Hash tự nó không cho reviewer chạy lại. Quyền reviewer tự thêm toán tử không lấp được việc mẫu số bắt buộc chưa xác định.',
   'Luật 4 :331–333 đòi miền head có/không kèm đường đi qua kiem_ho_so. Nhưng hợp đồng :113–141 chỉ cho kiem_ho_so(du_lieu,thu_muc) và head=None ở hồ sơ; head khác None đi qua D2b :182–183. Đo AST c2d606b: đúng một call kiem_mien(v, thu_muc, None), không có đầu vào head. Không thể dùng consumer này để kiểm nhánh head khác None mà vẫn giữ API A. Cần ma trận theo đúng consumer/đợt, gồm None, chuỗi rỗng và SHA cho helper, cùng D2b cho nhánh neo merge_commit.',
   'Đã rà cả corpus hồi quy thay vì kết luận từ đường dẫn thiếu: năm JSONL gốc có trong sandbox, băm khớp MANIFEST_SANDBOX.sha256 trên ref 908a9f2 (OID đầy đủ ở audit_r5.json); 138 dòng, 127 ID duy nhất, 11 bản lặp cùng bytes, không xung đột nguồn/regex hỏng. Các JSONL không ở Git, nhưng phương án sandbox được luật 5 cho phép nên KHÔNG báo mất hồi quy. Luật 5 bảo toàn 127 mẫu cũ; vấn đề còn mở là hợp đồng quét mới và routing ma trận, không phải xoá các mẫu cũ.'
  ],
  'de_xuat':'Sửa CHUNG luật 3–5 trước khi tiếp tục thi công: lập một manifest hữu hạn của toán tử (node/site áp dụng, phép thay và giá trị thay xác định, cách xử lý không áp dụng), ghim nguồn bộ sinh/bộ chạy và bắt buộc giao bytes cùng hash. Nối mỗi toán tử/miền nghĩa với consumer thực: helper và kiem_ho_so ở A, L8 ở B, D2b/head!=None ở C. Giữ 127 regression ID/hash, khai bản gốc/phiên bản thay thế và cách tái dẫn xuất trên exact head mới; không chạy nguyên module cũ rồi coi là kiểm head mới. Chạy một pilot trên c2d606b để chứng minh tập kê đủ, 25 survivor không tương đương được nhận diện, loader sản phẩm giữ nguyên, baseline dương và phân hạng target/non-target hoạt động; giao lệnh, rc, stdout/hash và danh sách ngoại lệ từng mutant. Lỗi setup/import không có tín dụng đóng chốt; không dùng ngoại lệ của luật 3 để miễn yêu cầu chết đúng ca của luật 1/5. Rủi ro cần tránh: biến khâu này thành chốt tự bảo vệ nguồn kiểu A14-S0, thay grammar sản phẩm để làm test xanh, hoặc thêm vô hạn ví dụ mà không chốt lại thước đo.'
 },
 {
  'id':'V02','class_slug':'so-do-khong-cung-pham-vi-nguon','severity':'P3',
  'vi_tri':'SPEC.md:298, :341–372, :416–417, :542–549 (số ca/luật/lớp)',
  'van_de':'Các lời khai tổng số chưa được cập nhật theo phạm vi r10: bảng A đã thêm hai ca nhưng căn cứ kích thước vẫn ghi 28; phần giới thiệu nói BA luật dù có năm; phần đưa review mã lượt 6 vào r10 nói ba lớp dù L01/L02 cùng một slug. Đây là tái mở lớp số đo trôi đã từng xuất hiện vòng 1–3.',
  'bang_chung':[
   'audit_r5.py rc0, AUDIT_R5_COMPLETE: đếm các ID hàng bảng A1/A2 duy nhất cho 17 A1 + 13 A2 = 30, thêm A1-16/A1-17 tại :357–358; :417 vẫn ghi 28 ca + 50 đột biến. 50 là tập m1…m50 tối thiểu kế thừa, không phải tổng mới của luật 1–5; số tổng mới chưa đo được.',
   ':298 ghi BA luật, nhưng mục :301–337 có luật 1,2,3,4,5. :543 ghi ba lớp, trong bảng :547–549 L01/L02 đều test-thieu-chot, L03 là mo-ta-duong-dan-lech-hop-dong: ba finding, hai lớp.',
   'Phần số đo còn lại đã đối chiếu, không báo gộp thành sai: numstat 0f9aa2a2cc697129e1f5be72feddf60986286865..c2d606bb6fc230c288200b8f1dd79715462c172b là +1/+335/+988 = 1324, ba tệp, dưới trần 1400 được user xác nhận. Đây là số mã r9, không phải dự báo mã r10. Corpus vẫn 66=47/10/9; hồ sơ 170=25/56/39/50; 93 vi phạm; generator 50=20/28/2; đường dẫn 60/62.'
  ],
  'de_xuat':'Đồng bộ toàn bộ các tổng trong r10 từ một inventory có đơn vị: 30 ca bảng A là sàn hiện tại; năm luật; hai lớp/ba finding ở review mã lượt 6. Giữ riêng 50 mutant đánh số kế thừa, 127 mutant reviewer, và tổng quét r10 chưa đo. Giữ 1324 neo c2d606b, không nâng nó thành số mã r10 hay bằng chứng còn đủ 76 dòng cho mọi sửa đổi. Kiểm đóng bằng đếm lại tất cả chỗ nêu tổng và đối chiếu inventory, không sửa các số thuộc đoạn lịch sử có nhãn. Rủi ro: đổi số để làm đẹp hội tụ hoặc biến một ước lượng thành authority nâng trần.'
 }
]
# Fill the immutable source OID from the actual read, never from an abbreviation guessed in prose.
source_oid=json.loads((W/'audit_r5.json').read_text())['source_ref_oid']
v['findings'][0]['bang_chung'][-1]=v['findings'][0]['bang_chung'][-1].replace('ref 908a9f2 (OID đầy đủ ở audit_r5.json)', 'ref đã cấp tại '+source_oid)

v['class_table']=[]
for f,manifestations,closing in [
 (v['findings'][0],[
   'Tập a–l không liệt kê đủ các họ biến đổi thực tế của lượt 6; hồi quy mẫu cũ được luật 5 giữ, phần tổng quát chưa chốt.',
   'Giá trị thay cho g/h/i và bytes bộ quét không là đầu vào bắt buộc của phép đo; tổng 0 sống không có mẫu số tái lập.',
   'Ma trận nghĩa gán head!=None cho consumer kiem_ho_so không có đường đi này.'
  ],'Một reviewer từ checkout và bundle sạch chạy lại cùng generator/manifest trên cùng head, sinh cùng tập ID/hash/site/target và cùng phân hạng; pilot phân biệt 25 survivor cũ và 9 tương đương bằng lý do cụ thể, không cấp tín dụng cho setup; từng miền được kiểm qua đúng consumer. Trên r10 code về sau mới được xác nhận đóng test-thieu-chot bằng target/non-target, không lấy review spec làm chứng chỉ code.'),
 (v['findings'][1],[
   '30 ca A nhưng căn cứ kích thước còn 28.',
   'Năm luật được giới thiệu là BA; ba finding mã được gọi là ba lớp thay vì hai.'
  ],'Đếm lại 30 ID A và 5 luật; bảng ma6 có 3 finding thuộc 2 slug. Mọi tổng hiện tại cùng đơn vị/nguồn; số r9 và lịch sử được gắn nhãn riêng; 1324 tiếp tục neo đúng c2d606b và không được dùng thay numstat r10.')]:
  v['class_table'].append({'slug':f['class_slug'],'finding_ids':[f['id']], 'manifestations':manifestations,
   'highest_open_severity':f['severity'],
   'nguon':{'reviewed_sha':H,'spec_sha256':S,'history':'vòng 4 và 12 lớp dựng lại; ma6 test-thieu-chot được nối tường minh bên dưới' if f['id']=='V01' else 'vòng 1/2/3 mở; vòng 4 đóng; vòng 5 tái mở'},
   'common_fix':f['de_xuat'],'closing_check':closing,
   'ly_do_va_rieng':'Không cần vá từng ví dụ. Một hợp đồng phép đo và ma trận consumer dùng chung xử lý cả lớp.' if f['id']=='V01' else 'Không cần cơ chế vá riêng; một inventory có đơn vị và quét các tổng xử lý cả lớp.'})

evidence={
 'xuong-dong-khong-khop-byte-that':('DA_VA_THAT','SPEC:68–79, :345 giữ LF/CRLF đồng nhất, loại CR trộn/lẻ. audit_r5.json/parser: LF/CRLF passed, mixed→xuong_dong_tron, lone→cr_le; census giữ 47/10/9.'),
 'nghiem-thu-khong-co-lap-chot-dich':('VA_MOT_PHAN','U02 cụ thể được sửa: SPEC:312–315, :345, :357 ghim đủ 5 ô trùng ID. audit_r5: 4 tổ hợp dòng→job_lap và provenance trùng→job_id_trung_provenance, healthy passed. Các sửa m13/m20/m22/C3–C5/B8/m45/m46/m50 giữ nguyên. Còn cơ chế bao lớp V01 ở luật 3–5; không lấy tổng mutant để đóng.'),
 'nang-tran-thieu-hop-dong-authority':('DA_VA_THAT','SPEC:410–425 có ai_nang/can_cu/tran_cu/tran_moi, chuỗi các lần nâng; user trực tiếp xác nhận #1236 issuecomment-7047718543 cho 1400. Đo numstat r9 +1324/3 tệp. ADR0053/0055 có ở OID ghim, không có ở cha, thuộc first-parent local origin/master (supplement_r5.json). Không xác thực freshness GitHub; không suy authority thi công/lease r10.'),
 'd2b-thieu-neo-attempt':('DA_VA_THAT','SPEC:168–181, :398 giữ passed-only, type int không bool, >=1 và neo header; C3/mC9/mC10 đủ lệch/thiếu/bool. audit_r5/attempt_types phân biệt None/True/1.0/0 với 1/2 và neo attempt1. Đây là đóng hợp đồng, chưa đo D2b thực thi.'),
 'so-do-khong-cung-pham-vi-nguon':('VA_MOT_PHAN','Các số corpus/số đo cũ vẫn khớp bằng hai script tham chiếu rc0, stdout trùng byte; landed170/94/0, claim60/62, generator50=20/28/2, numstat1324. Nhưng r10 phát sinh tổng ca/luật/lớp lệch ở V02; tái mở lớp, không tính vào F của tập U vòng4.'),
 'trang-thai-job-khong-khop-conclusion':('DA_VA_THAT','SPEC:95–97 và :355 giữ K5/A1-13. supplement_r5/conclusion: T-fail→(failed,[]); bản sao đổi dòng job136203672900 sang passed và tổng39/39→not_measured,ket_luan_lech:136203672900. Không phát hiện thay đổi r10 làm yếu luật này.'),
 'landed-khong-buoc-loi-khai-hop-le':('DA_VA_THAT','SPEC:126–132, :216–217, :370–371 giữ ba dạng landed và lời khai hợp lệ không vi phạm. audit_r5: 170 hồ sơ, 94 landed, 0 lệch với _xet_mot_tep; văn xuôi không thay lời khai có cấu trúc. Việc neo L8 vào H vẫn ngoài phạm vi đã khai.'),
 'l8-chua-chot-thu-tu-cutover':('DA_VA_THAT','SPEC:156, :198–205, :383–389 giữ cutover trước L8 và B8 nguyên byte. supplement_r5: pr680 SHA256=964742fef636a70587b2247c094ac4f38aea540a01abdce8b6319c8f74b447bf khớp MIEN_TRU_CUTOVER; nếu áp kiểm hồ sơ thì có dinh_dang_loi_khai và landed_khong_loi_khai_gate_output. Fixture tiếp tục phân biệt đổi thứ tự; chưa chạy L8 mới của B.'),
 'khong-kiem-co-toan-ven-provenance':('DA_VA_THAT','SPEC:88–91, :356 giữ cả bốn vế K3. supplement_r5/K3: run flag, tap_jobs flag, checkout flag và checkout rỗng đều not_measured/provenance_chua_du, healthy passed. Ca m50 và nghĩa vụ gỡ riêng chốt còn nguyên.'),
 'hop-dong-dau-vao-dau-ra-chua-chot':('DA_VA_THAT','U01 đã sửa ở SPEC:142–150, :184–196, :401: passed dùng tep@oid, owner_waived dùng mien readback_thu_muc@oid; vi phạm vào thieu/stderr, cấm in ĐẠT khi trượt, nhánh không chạy im lặng, lỗi đo rc8. C1/C6 so marker theo nhánh, C6 âm tac_gia/rc12/mC14; failed:- và attempt passed-only giữ nguyên. Quét toàn D2b/CLI không còn biến tep chưa được gán ở nhánh waiver. Routing ma trận head là nghĩa vụ test còn ở V01, không phải đổi API.'),
 'nguon-doc-khong-neo-cung-snapshot':('DA_VA_THAT','SPEC:113–117 và :156 dùng du_lieu đã nạp, giữ một lần đọc L4. D2b :170–196 lấy dữ liệu từ commit trên refs/remotes/origin/*, kiểm raw path/mode trong chính cây ấy, git archive; mã từ origin/master. C5/C9 giữ kiểm mode/path/remote. Phần thay đổi r10 là bảng output, không đưa việc đọc về worktree hoặc buộc hồ sơ phải ở master.'),
 'he-qua-gioi-han-khai-thieu':('DA_VA_THAT','SPEC:207–229, :244–262, :469–479 khai đủ hậu quả run phụ/skipped/hậu duệ/waiver cũ, L8 chưa neo H, log/provenance/readback có thể sửa tay, lệch Issue mục3 và symlink skip Windows. Đóng nghĩa vụ công bố của finding cũ, không đóng giới hạn authenticity hoặc tuyên bố log thật đã đo.')
}
v['prior_class_status']=[]
for p in old['prior_class_status']:
    status,ev=evidence[p['slug']]
    ids=list(p['finding_cu']); rounds=list(p['vong_xuat_hien'])
    if p['slug']=='hop-dong-dau-vao-dau-ra-chua-chot': ids+=['U01'];rounds+=[4]
    if p['slug']=='nghiem-thu-khong-co-lap-chot-dich':ids+=['U02'];rounds+=[4]
    if p['slug']=='so-do-khong-cung-pham-vi-nguon': rounds+=[5]
    v['prior_class_status'].append({'slug':p['slug'],'finding_cu':ids,'vong_xuat_hien':rounds,
      'status':status,'evidence':ev,
      'chua_do_duoc':'Kết luận về ĐẶC TẢ. Chưa có implementation r10 để chứng nhận test/code/L8/D2b, Windows hoặc CI. '+('Phần cần chốt còn ở V01/V02 tương ứng.' if status=='VA_MOT_PHAN' else 'Không còn phép đo cần thiết để đóng biểu hiện đặc tả nêu ở lớp này.')})
v['prior_class_status'] += [
 {'slug':'pham-vi-kiem-chung-trai-adr-windows','finding_cu':['U03'],'vong_xuat_hien':[4], 'status':'DA_VA_THAT',
  'evidence':'SPEC:428–442 tách OS bằng chứng khỏi OS kiểm mã: A/C required, B chốt theo diff thật; user xác nhận miễn Windows CI chỉ A (#1236 issuecomment-7048063512), A vẫn local exact H+nền theo M3; C không miễn trước; :476–477 không tính symlink skipped là đạt. Đối chiếu write_set :235–239 với ADR0060 M3/M9 và ADR0062 N1: nghĩa vụ chung còn nguyên. Câu nói không chạy Windows CI cho toàn packet đã bị bỏ.',
  'chua_do_duoc':'Không gọi máy Windows hoặc CI/mạng ở review spec. Waiver exact head A là nghĩa vụ audit về sau; lời xác nhận của user về quyết định không thay readback/audit khi land.'},
 {'slug':'test-thieu-chot','finding_cu':['ma1:F04','ma2:G02','ma3:H01','ma4:J01','ma4:J02','ma5:K01','ma5:K02','ma6:L01','ma6:L02'],
  'vong_xuat_hien':['ma1','ma2','ma3','ma4','ma5','ma6'], 'status':'VA_MOT_PHAN',
  'evidence':'Nối vào nghiem-thu-khong-co-lap-chot-dich bằng bang_noi_slug. Luật 4/5 có ma trận nghĩa, ưu tiên lỗi đôi và giữ regression; A2-10 đủ 6 fixture. Đo lại kho có127 ID/hash và5/5 consumer contrasts. V01 còn mở vì tập toán tử/handoff/routing chưa chốt; chưa có code r10 chứng minh 25 survivor cũ chết đúng ca. Không reset hai chuyển tiếp ma4→ma5 và ma5→ma6=0/1.',
  'chua_do_duoc':'Không chạy suite r10 hoặc nhận 127 mutant đã bị giết; chỉ kiểm nguồn, hash và5 đối chứng trên r9. Hồi quy runtime toàn bộ phải đo trên exact implementation r10 sau khi hợp đồng phép đo được chốt.'},
 {'slug':'mo-ta-duong-dan-lech-hop-dong','finding_cu':['ma6:L03'],'vong_xuat_hien':['ma6'], 'status':'VA_MOT_PHAN',
  'evidence':'SPEC:120–122,:549 đã chỉ rõ A cấm tuyệt đối/../symlink, ./tệp hợp lệ; không mang luật D2b cấm . sang A. audit_r5/dot_path: tên thường và ./tệp→[], ../tệp bị chặn. Docstring r9 c2d606b:224 vẫn ghi cấm .; đó là mã tham chiếu chưa sửa, không phải lỗi mới của spec r10.',
  'chua_do_duoc':'Phần đặc tả đã chốt, phần sửa docstring/code chưa thi công nên không đánh DA_VA_THAT cho finding mã L03. Không tạo finding đặc tả mới từ nghĩa vụ implementation chưa tới.'}
]
v['bang_noi_slug']=[{
 'slug_nguon':'test-thieu-chot','slug_dich':'nghiem-thu-khong-co-lap-chot-dich',
 'finding_cu':['ma1:F04','ma2:G02','ma3:H01','ma4:J01/J02','ma5:K01/K02','ma6:L01/L02','spec4:U02'],
 'ly_do':'Cùng cơ chế: ca/đột biến không phân biệt đúng chốt và miền nghĩa; đổi từ spec sang code không tạo lớp khác. Cách vá chung là thước kiểm độc lập có target/non-target, ma trận nghĩa và phân hạng. Giữ cả alias và lịch sử; không dùng phép gộp để xoá lần tái diễn.',
 'phep_doi_chieu':'U02 tập trùng ID được kiểm bằng5 ô; ma6 có25 mutant khác hành vi và fixture CLI thứ6. r10 luật1–5 định giải quyết cùng tính chất. V01 áp chung sau nối; không cộng alias làm một lớp mở thứ hai, không đổi U vòng4=3.'}]
v['hoi_tu']={'vong4_sang_5':'2/3',
 'U':['hop-dong-dau-vao-dau-ra-chua-chot','nghiem-thu-khong-co-lap-chot-dich','pham-vi-kiem-chung-trai-adr-windows'],
 'F':['hop-dong-dau-vao-dau-ra-chua-chot','pham-vi-kiem-chung-trai-adr-windows'],
 'giai_thich':'66,67%; U02 chỉ vá một phần nên không vào F. so-do-khong-cung-pham-vi-nguon tái mở ở vòng5 nhưng không nằm trong U vòng4, không đưa vào mẫu số hoặc tử số. test-thieu-chot là alias được nối, không đếm hai lần.',
 'lop_lap_lan_ba':['nghiem-thu-khong-co-lap-chot-dich','so-do-khong-cung-pham-vi-nguon','hop-dong-dau-vao-dau-ra-chua-chot','test-thieu-chot'],
 'lich_su_giu_nguyen':{'spec1_sang_2':'KHONG_DO_DUOC','spec2_sang_3':'KHONG_DO_DUOC','spec3_sang_4':'2/4','ma4_sang_5':'0/1','ma5_sang_6':'0/1'},
 'checkpoint':'Tỷ lệ2/3 không xoá checkpoint đã chạm ở lớp nghiệm thu/test-thieu-chot hoặc reset budget. IO đã đóng nhưng lịch sử lặp vẫn giữ.'}
v['new_classes']=[]
v['reopened_classes']=['so-do-khong-cung-pham-vi-nguon']
v['checkpoint_assessment']={
 'ma':'E1',
 'ket_luan':'Theo yêu cầu của assignment, cách đóng lớp mới ở r10 CHƯA được phép đo chống đỡ đủ để tuyên bố đóng test-thieu-chot: phép quét bắt buộc chưa xác định/tái lập và một đường consumer không có thật. Giữ Review Rescue Checkpoint; không quay lại vòng vá mã thêm ca đơn lẻ.',
 'bang_chung_duong':'Hướng ma trận và hồi quy có ích: đủ5 ô trùng ID,127 regression nguyên hash,5 consumer contrasts phân biệt. Không kết luận mọi phương án đều bất khả thi; kết luận hẹp là hợp đồng r10 nguyên văn chưa đủ để nghiệm thu.',
 'de_xuat':'Trình phương án manifest toán tử/miền/consumer hữu hạn, bundle nguồn bộ đo và pilot trên c2d606b như V01; chốt nó trước khi giao thi công tiếp. Không cần thay semantics K1–K8/L8/D2b để đóng phần này.',
 'E2':'Trần đã xác nhận1400; r91324≤1400. Numstat r10 chưa đo, không suy76 dòng đủ. Lời gọi/budget không được tự cấp thêm.',
 'E3':'Chưa có bằng chứng implementation tuân thủ đúng r10 cho lời khai dương lọt ngoài giới hạn đã công bố. Các mutant làm sai code là phản chứng nghiệm thu, không là chứng minh thiết kế gốc thất bại mục1–2.',
 'E5':'Duyệt spec_hash và audit exact head vẫn theo pham_vi_e; verdict không cấp authority thi công/merge/land.'}
v['da_do_khop']=[
 'SHA256 SPEC ngoài kho = blob HEAD:ops/specs/wp1236-r10.md = '+S+'; reviewed_sha '+H+'; tree293d124054e74bb0459b69c2e5df6691b74af49d.',
 'Diff r9→r10 đã đọc đầy đủ. K1–K8/L8/D2b giữ semantics gốc, phần mới là output/acceptance/kích thước/Windows/history; rà phần cũ với luật mới.',
 'Hai script tham chiếu rc0, stdout trùng byte do_tep.txt/do_loi_khai.txt:66=47/10/9;170=25/56/39/50;93=39+36+12+2+2+2.',
 'la_landed parity170/94/0;62 cặp hồ sơ-token,60 phân giải đúng,2 ngoại lệ đúng pr1392/pr1406;50 script đúng3 băm=20/28/2.',
 'Numstat base0f9aa2a..c2d606b =3 tệp,+1324/-0 (1+335+988),≤1400. Không có mã r10 để đo tổng mới.',
 'Năm ô trùngID có healthy control và lý do riêng đúng; LF/CRLF passed, CRlẻ/trộn bị chặn; K3bốn vế và K5conclusion có đối chứng đúng; pr680 byte khớp cutover và có lỗi nếu ápL8.',
 'Kho reviewer ma6:5 JSONL đọc từ sandbox gốc, SHA256 khớp MANIFEST trong Git;138 dòng→127 ID,11 trùng cùng bytes,0 xung đột nguồn,0 regex compile error. Không coi thiếu JSONL trong Git là mất hiện vật vì phương án sandbox hợp lệ.',
 'audit_method_r5.py rc0:5/5 đối chứng qua kiem_ho_so phân biệt được trên c2d606b; không dùng kết quả này thay suite r10.',
 'U01 bảng D2b/CLI đã chốt nhánh success/error/không chạy; U03 WindowsA/C required, miễnCI chỉA theo user, Windowslocal vẫn bắt buộc, symlinkskip không là pass.',
 'Số ca/luật/lớp hiện tại lệch ở V02; không suy corpus tổng xanh hay validator schema xanh là approval.'
]
v['authority']={'source':'Chỉ thị trực tiếp của user: review ĐẶC TẢ wp1236 r10 vòng5, read-only/offline; không phải giao thi công.',
 'spec_revision':10,'generation':'Không có generation/lease thi công được giao; đây là review spec trước lease mới.',
 'effective_write_set':[str(W)],'repo_policy':'read-only cả kho review và kho mã tham chiếu; không mạng/GitHub/commit/push.',
 'owner_decisions':'TrầnA1400 và miễnWindowsCI A dựa vào xác nhận trong prompt của user; không gọi GitHub để xác minh lại, không giả readback.'}
v['review_class']='sensitive'
v['review_identity']={'provider':'openai_codex','execution_surface':'codex_service','transport':'machine','model_family':'openai',
 'model_served':'KHONG_DO_DUOC','effort_served':'KHONG_DO_DUOC','session_id':'KHONG_DO_DUOC',
 'evidence':'Phiên API với exec tools; không có receipt launcher/CLI chứng minh codex exec hoặc model/session phục vụ. Theo bảng provider, dùng codex_service cho đường không qua CLI/Desktop; không suy từ tên thư mục hoặc actorGitHub.',
 'independence':'Context được giao là reviewer độc lập; không thực thi packet, không fork context Executor và không tạo subagent.',
 'assurance':'Verdict nội dung trên exact spec/head. Không tự tạo cross_approved/human_audited; receipt danh tính/transport và authority do điều phối kiểm riêng.'}
v['validation_scope']={'passed':['hash/blob/exactGit preflight','reference census byte match','fixture controls/parser/ID/K3/K5','regressionhash inventory và5 consumer contrasts','localADR OID structure'],
 'failed':['Hợp đồng nghiệm thuV01','Nhất quán sốV02'], 'skipped':[],
 'not_run':['implementation r10 suite và127 mutant trên r10','L8/D2b mới củaB/C','Windowslocal/WindowsCI','CI từ xa/full_mutant_audit/full release/land gate','Ruff bare lint và Ruff pin/probe (review spec)','GitHub/mạng/remote freshness'],
 'limits':['Read-only snapshot chỉ chứng minh không có delta ở hai mốc, không chứng minh không từng ghi rồi hoàn nguyên.','Sandbox được cấp workspace-write; ràng buộc kho read-only được giữ bằng thao tác và snapshot, không khai OS tự chặn mọi ghi.','Bản r9c2d606b dùng làm đối chứng kế thừa; không nâng thành code r10.'],
 'setup_observation':['Lần đầu audit_r5.py dừng do script reviewer thiếu tham số yaml khi gọi _xet_mot_tep; đã sửa và chạy lại rc0.','Lần đầu kiểmMANIFEST bỏ sót tiền tố ./; đã sửa so đường dẫn và chạy lại. Không lấy các lỗi setup này làm finding.','Dò pr1440-land-evidence không có tệp; đã dùng fragment hồ sơ thậtpr1453 cho phép đo consumer.']}
v['history_coverage']={'spec_prior_unique_classes':13,'spec_prior_findings_round4':['U01','U02','U03'],
 'historical_findings_rounds1_3':34,'historical_classes_rounds1_3':12,'additional_code_alias':'test-thieu-chot','additional_code_class':'mo-ta-duong-dan-lech-hop-dong',
 'prior_status_rows':15,'open_spec_classes':2,'open_spec_findings':2}
v['execution_receipts']=[]
for script,positive in [('audit_r5.py','AUDIT_R5_COMPLETE'),('audit_method_r5.py','METHOD_R5_COMPLETE:5/5 consumer contrasts;127unique')]:
 p=W/(script[:-3]+'.stdout')
 v['execution_receipts'].append({'command':'python3 -B ../work/'+script,'cwd':str(R),'rc':0,'output_file':str(p),'stdout_sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'script_sha256':hashlib.sha256((W/script).read_bytes()).hexdigest(),'positive_evidence':positive,'scope':'offline spec/fixture evidence, not r10 implementation gate'})
v['execution_receipts'].append({'command':'python3 -B (script nội tuyến đo ADR OID, cutover, K3 và K5; đọc source/fixture, chỉ ghi work/tmp)','rc':0,'output_file':str(W/'supplement_r5.json'),'sha256':hashlib.sha256((W/'supplement_r5.json').read_bytes()).hexdigest(),'positive_evidence':'ADRexists/parent rc0/128 đúng kỳ vọng;K3 4/4 đúng lý do;K5 contrast đúng;cutoverhash khớp'})
(W/'VERDICT.json').write_text(json.dumps(v,ensure_ascii=False,indent=2)+'\n')
print('VERDICT_WRITTEN',len(v['findings']),len(v['class_table']),len(v['prior_class_status']))
