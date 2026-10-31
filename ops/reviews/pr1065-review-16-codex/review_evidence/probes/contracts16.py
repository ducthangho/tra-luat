from pathlib import Path
import json
r=Path(__file__).resolve().parents[1];x=json.loads((r/'evidence/inventory16.json').read_text());checks={
366:('A/B đạt','Get-PhienBanLenh đã đo current: rc0 + mẫu caller. Test-CungDinhDanh so toàn token/case, chỉ bỏ v/V. Với Tag có chốt361 trước giu: response bằng ghim. closure16: keep-mismatch loi/0download; control đúng ghim, ZIP target/identity kiểm giu.'),
368:('A đạt; B không áp','Chỉ ChiKiem, guard357 chặn current rỗng; portable-check4/4: missing/rc9/cannot-start đều loi, bản cũ đo được mới can_cap_nhat. Không phải chứng nhận cài.'),
383:('B đạt','Save/Assert-Bam trước copy; getter381 đòi rc0+mẫu rồi Test-CungDinhDanh382 bằng moi. Nếu ghim, moi đã bị ràng361 bằng Tag. closure16 đúng ghim nâng1.7.7; ZIP third14/14 và alias-after không được đạt.'),
401:('A đạt; B ngoại lệ Python','pyTruoc đo --version rc0+Python\\s+(\\S+), null thì loi/return400. Chỉ báo Python không nâng, ngoại lệ rõ trong chỉ thị. Native version failure3 thành loi.'),
416:('A đạt','ChiKiem chỉ vào else khi metadata current có rc0 và khớp mẫu đầy đủ của Get-PhienBanGoi. Không đọc được thì415 loi; absence/new-paths kiểm trống/rác/rc6. Đích moi nhat ở pip chỉ là nhãn kiểm, không chứng nhận giu.'),
424:('B đạt','pip install rc được chụp trước getter; sau metadata rc0+mẫu và đích không rỗng. PyYAML/jsonschema = ghim; pip = pip index rc0+mẫu. -cne chứng nhận đúng token. real-pip/install-contract/unknown-target chặn rc0 nhưng chưa lên đích.'),
433:('A đạt','ChiKiem đo venv python --version rc0+mẫu; null thì loi. third-paths6/6: missing/runtime rc9/cannot-start lỗi; không chỉ Test-Path.'),
446:('B đạt theo hợp đồng venv','Sau pip rc0 đo lại python (rc0+mẫu) và PyYAML/jsonschema (rc0+mẫu), hai metadata -cne ghim. real-pip control/dryrun + install-contract: dry-run, Python hậu rc9, lệch ghim đều loi. Không chứng nhận mọi dependency ngoài hai ghim.'),
458:('A đạt','ChiKiem cần current CLI do getter đo rc0+mẫu caller và npm tồn tại; null thì loi. user-version/check-missing-cli đo cả2CLI, giữ đủ dòng các công cụ sau.'),
467:('B đạt','npm install rc0; đo CLI SAU qua getter rc0+mẫu giữ suffix; npm view version rc0+mẫu. -cne so đầy đủ, case-sensitive. case-equal giu, case-different/suffix/đích null/rác/rc9 loi; target-equality5/5.'),
485:('A đạt','ChiKiem: nlmPy phải tồn tại, nlm getter rc0+nlm version\\s+(\\S+) khác rỗng mới kiem. NLM prerequisite4/4 và lỗi native rc9 đều loi.'),
507:('B đạt','pip rc0, nlm CLI SAU rc0+mẫu, metadata gói rc0+mẫu, pip index đích rc0+mẫu; cả CLI+metadata -cne đích. Thêm status rc0+JSON+mode=file. Real-NLM stale CLI0.4/metadata+đích0.5 bị loi; finally khôi phục env.'),
544:('A đạt; B ngoại lệ quyết định','ChiKiem chặn current rỗng533 và Test-CoTheCai534 chặn token không parse được. current đo được mới thông báo có LTS major mới; không phải giu/nang_cap. Node current4ca chứng minh suffix/build/rác không cài.'),
546:('A đạt; B ngoại lệ quyết định','Không LTS cùng major thì can_quyet_dinh, không chứng nhận cài. Nếu ChiKiem current đã đo ở532/533, nên A thoả. system-check no-lts:4native rc0, node chỉ báo quyết định.'),
560:('A/B đạt','Current getter532 đòi rc0+mẫu và Test-CoTheCai hợp lệ; đích lấy HTTP/index. Test-CungDinhDanh560 chứng nhận bằng token/case. numeric/git-alias-before không được giu sai; stable4/4 giu, cao hơn đích loi561.'),
562:('A đạt; B không áp','Chỉ ChiKiem sau guard533/534; current đo được mới can_cap_nhat. system-check6/6: missing/rác/rc9/cannot-start đều loi; không có installer.'),
576:('A không tới; B ngoại lệ MSI3010','Chỉ cài thật; Install-Msi516 trả can_khoi_dong_lai riêng khi ExitCode3010, tiếp tục trước chứng nhận phiên bản. system-matrix msi-reboot đo logic này bằng fixture; Windows msiexec thật KHÔNG ĐO ĐƯỢC.'),
578:('B đạt','Sau Save/Assert-Bam và installer thành công, getter575 đo SAU rc0+mẫu rồi Test-CungDinhDanh577 phải bằng đích. suffix-after/numeric/git-marker-after loi; control 4nang_cap. Post-rc9/empty/cannot-start driver bổ sung kiểm riêng.'),
590:('Ngoài chứng nhận phiên bản B; A không tới','khoi_dong_lai là task Running, không phải giu/nang_cap/cai_moi. Script DaCaiNode khởi tạo false59, chỉ bật568 khi cài thật; ChiKiem không bật, không tới restart. system-matrix kiểm recovery cả khi Node MSI hỏng; task Windows thật chưa đo.')}
assert x['add_count']==50 and x['nonloi_count']==19 and set(checks)=={v['line'] for v in x['nonloi']}
rows=[{**v,'result':checks[v['line']][0],'proof':checks[v['line']][1]} for v in x['nonloi']]
(r/'evidence/contracts16.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
with (r/'VERDICT.md').open('a') as f:
 f.write('\n## KIỂM TOÀN BỘ Add-KetQua KHÁC loi\n\nLệnh: `pwsh/pwsh -NoProfile -File probes/inventory.ps1 > evidence/inventory16.json`; `python3 probes/contracts16.py`. Output: parse_errors=0; Add-KetQua50; khác loi19; đối chiếu19/19. Bộ lọc AST lấy MỌI CommandAst gọi Add-KetQua mà đối số HanhDong không phải literal loi, bao gồm hành động tính bằng biểu thức; không lọc chỉ theo tên giu/nang_cap, không chỉ xét diff. Helper không phát dòng thành công khác ngoài các caller dưới đây; source đã được đọc toàn bộ. A áp ChiKiem; B áp giu/nang_cap/cai_moi cùng ngoại lệ được giao.\n\n| Dòng | Hàm / hành động | A/B | Phép đo hoặc lập luận |\n| --- | --- | --- | --- |\n')
 for v in rows:f.write(f"| {v['line']} | {v['function']} / `{v['action']}` | {v['result']} | {v['proof']} |\n")
 f.write('\nKhông có phản chứng A/B còn mở trong phạm vi đã đo/phân tích tĩnh; hai điểm ZIP ghim366/383 nay dùng đích bị ràng bằng Tag trước chứng nhận. Không biến kết luận logic thành bằng chứng Windows native.\n')
print('Full Add-KetQua audit: 50 total; 19/19 non-loi sites checked against A/B')
