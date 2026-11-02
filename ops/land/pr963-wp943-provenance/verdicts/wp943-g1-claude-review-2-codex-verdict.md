verdict: approve
reviewed_sha: eb5e5bf119358babf831d2aec0ee27c7e5896c1f

Reviewer độc lập: Codex, họ OpenAI; executor theo assignment/lease: Claude. Thực thi lệnh cục bộ qua `exec_command`, transport machine. Không có header launcher/run.json trong bộ hiện vật này để tự xác minh tên model/effort hoặc wrapper CLI; không suy danh tính từ GitHub submitter. Ngưỡng áp dụng: không còn P0/P1/P2; không phát hiện cả P3. Verdict nội dung neo đúng SHA trên, không thay biên nhận assurance hay bằng chứng CI.

## BẢNG ĐO

Đã kiểm độc lập (lượt 2, không kế thừa kết luận lượt 1):

| Khẳng định | PR khai / SPEC đòi | Đo được | Khớp? |
|---|---|---|---|
| SPEC đóng băng | `22729e93eec0e1c4677a5d6529b81f9f0c46c47f3f605017b7abb337b5e1e270` | `sha256sum SPEC.md` khớp đủ 64 ký tự | Có |
| Exact head | `eb5e5bf119358babf831d2aec0ee27c7e5896c1f` | `git -C cay-kho rev-parse HEAD` khớp; tree `10d120f4083e8998645f88914214a002f4be9393`; status rỗng; `core.abbrev=7` | Có |
| N1 adr-song | rc 0 | rc 0; `55 ADR trên đĩa, 55 dòng trong §20, khớp 1–1` | Có |
| N1 doctrine-scan | rc 0 | rc 0; `đã quét 10 tệp, 0 chỗ chép doctrine` | Có |
| N1 whitespace | rc 0 | `git diff --check 3e973a0 HEAD`: rc 0, output rỗng | Có |
| N3 | Không còn lời ADR-0056 chưa kích hoạt | `rg -n "CHƯA KÍCH HOẠT VẬN HÀNH\|chưa kích hoạt vận hành" docs/adr/0056-* docs/PROTOCOL_DA_PHIEN.md`: rc 1, output rỗng | Có |
| N2 doc-claims-check | Delta HEAD/base = 0 | HEAD và base đều rc 0, `ok=true`, `flags=[]`, 381 advisory; hai JSON đo lại bằng nhau toàn bộ | Có |
| N2 selftest | N/N trên exact head | Executor: `1731/1731`; độc lập: rc 1, `== tl selftest 1729/1731 ==`; hai ca `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim`, `r268_l2_trichotomy_theo_trang_thai_object` fail do ký Git của môi trường; chạy riêng hai ca ở cả HEAD/base đều False, commit fixture đều rc 128 | Không khớp executor; độc lập thất bại hạ tầng, không ghi pass |
| N5 CI trên head cuối | Check run xanh | Không có hiện vật check run; review offline, không mạng theo assignment | KHÔNG ĐO ĐƯỢC |
| Trần diff | ≤ 2 tệp, ≤ 80 dòng thêm, đúng write set | 2 tệp, +12/−5; `diff.patch` và `numstat.txt` bằng byte với diff Git thật | Có |
| Dependency #834 | Base chứa merge #834, §4/accept giữ nguyên | Base `3e973a0`: `Merge pull request #950 ... wp834`; ancestor rc 0; toàn §4 bằng byte base/head | Có |
| Bất biến M1 | Giữ ba mục và phép đo lịch sử | Các mục `Những gì KHÔNG đổi`, `Không hồi tố`, `Vì sao sáu giờ` và đoạn đo 19-10/25-10 đều bằng byte | Có |
| Chứng cứ M1 | Câu trích #835 và lease wp943 khai 30 đúng | Câu trích sau nối soft-wrap có trong comment cấp; comment ngày 26-10-2026; LEASE.yaml khai `heartbeat_required_minutes: 30` | Có |
| M2 | Chỉ đổi dòng ADR-0056 trong §20 | Mọi dòng ADR khác bằng byte; ba hunk đúng phạm vi M1/M2 | Có |

Các phép đo Python chạy với `PYTHONDONTWRITEBYTECODE=1`, ngoại trừ một lệnh xem `release-manifest --help` đã vô ý sinh 31 tệp bytecode ignored (mtime cùng giây 03:23:28 UTC). Đã nhận diện và xóa đúng các tệp do lệnh đó tạo, cùng hai thư mục cache rỗng; `git status --porcelain=v1 --untracked-files=all --ignored=matching`, diff tracked và diff index đều rỗng sau khôi phục. Không sửa nội dung tracked. Vì đã có ghi cache tạm, không tuyên bố chưa từng ghi cây trong suốt lượt; kết luận sạch là không còn delta quan sát được. Base dựng bằng `mktemp -d` và `git clone --local --no-hardlinks`, không dùng git worktree. Bản clone tạm không kế thừa `core.abbrev=7`: lần thử đầu base rc 2 do độ dài SHA; sau `git -C <clone-tạm> config core.abbrev 7`, đo lại rc 0. Đây là sai khác setup, không phải lỗi bản vá.

Lệnh N1: `PYTHONDONTWRITEBYTECODE=1 python .claude/dev/packet_loop.py adr-song --root .`; tương tự `doctrine-scan`; `git diff --check 3e973a0 HEAD`. N3 đã chạy cả dạng glob nguyên văn trong assignment và dạng tên tệp mở rộng: đều rc 1, không output. N2 chạy `PYTHONDONTWRITEBYTECODE=1 python scripts/tl.py doc-claims-check --strict --json` riêng tại HEAD và clone base đã checkout detached đúng OID, cùng `core.abbrev=7`. Hai JSON đo lại bằng nhau toàn bộ. Bản executor cung cấp có 379 advisory, phép đo lại có 381: hai advisory thêm ở CHANGELOG.md:1267 và :10974 đều là `references/golden/fixtures/` không có trong clone được cấp. Chênh lệch này có ở cả base/head; delta của PR vẫn 0, không tăng hard flag.

Đối chiếu từng ý M1/M2 (các kiểm lại này KHÔNG tính vào sáu hướng mới):

- ADR-0056:3–8 bỏ trạng thái chưa kích hoạt, khai đã kích hoạt, neo merge PR thi công wp943 vào master, ghi đủ căn cứ xác nhận chủ kho + quét mã và packet thi hành. Không bịa SHA hoặc giờ cho merge. Ngày 26-10 tại :40 là mốc xác nhận, không phải thời điểm merge.
- ADR-0056:35–38 giữ nguyên phép đo lịch sử, hai base và hai ngày. :40–45 thay điều kiện controller chưa đo bằng xác nhận không controller ngoài, cách áp tay, luật chỉ lease cấp SAU merge khai 360; lease trước giữ byte/số, gồm chính wp943 khai 30. Số 360 có sẵn không bị thay; thêm một lần nhắc 360 đúng yêu cầu.
- Protocol :1535 đúng trạng thái Accepted — đã kích hoạt (merge wp943), giữ không controller trong kho và thêm phiên điều phối áp tay. §4, cửa accept của #834 và mọi dòng §20 khác giữ nguyên.
- Đã đọc lại các câu ngoài hunk: ADR :28–31, :47–51; protocol :271, :282–297, :1497 và :1533–1534. Không phát hiện câu trở thành sai: phạm vi lease mới ở §4 được giới hạn rõ bởi mốc kích hoạt; đồng hồ dự phòng dẫn lại cùng ngưỡng ở trên, nên không nâng lease cũ. Dòng ADR-0017 ghi ngày quyết định 19-10, không tự khai là ngày kích hoạt. Đoạn revision 4 tại ADR :47–51 nối lại hai base lịch sử và Issue #835, mô tả wp835; không phải khai revision của wp943. ADR-0054 còn chưa kích hoạt, độc lập với ADR-0056.
- Không đổi lease, code, ADR khác, `scripts/tl_selftest.py`, `RELEASE_MANIFEST.json` hoặc mục bất biến nào. Đọc Git thật, không chỉ dựa vào diff được giao.

Các phép đối chiếu byte dùng `git show 3e973a0:<path>` và `git show HEAD:<path>`, tách mục theo heading. Output thật: `Những gì KHÔNG đổi True`, `Không hồi tố True`, `Vì sao sáu giờ True`, `historical paragraph equal True`, `section4 incl accept byte identical True`, `other §20 rows equal True`, `quote in comment True`, `heartbeat_required_minutes: 30`; `base ancestor rc 0`; numstat `1 1 docs/PROTOCOL_DA_PHIEN.md` và `11 4 docs/adr/0056-lease-no-progress-six-hours.md`; `diff.patch equal True numstat equal True`.

## BẢNG SĂN

Đã đọc LUOT1_PARTIAL_VERDICT.md như dữ liệu của lượt khác; không dùng các kết luận đó làm chứng cứ cho lượt này. Sáu hướng dưới đây đánh số tiếp 8–13 để không lẫn với bảy giả thuyết cũ. Các hướng mới đo lần lượt: nhận giá trị tại cửa lease, thực thi đồng hồ trong mã, cô lập sổ thu hồi, tác động gói phát hành, render Markdown và allowlist authority. Tất cả có lệnh chạy và output thật; không tính các lệnh bắt buộc N1/N2/N3 là hướng săn.

### HƯỚNG 8: Cửa tiếp nhận lease có từ chối hoặc ép 360 về 30 không

- Giả thuyết: sau kích hoạt, lease mới khai 360 nhưng validator/đọc YAML vẫn chỉ nhận 30, làm đường cấp lease hỏng.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp943-review2.05gESZ/hunt8.py` từ cwd. Script dựng lease schema v2 tối thiểu, đúng provider/cross-family/sensitive và hạn năm 2099 trong thư mục tạm; đổi duy nhất `heartbeat_required_minutes` giữa 30 và 360, gọi CLI `ops/lease_publish.py check`, rồi đọc ngược YAML. Không đăng lease, không gọi GitHub.

```python
from pathlib import Path
import subprocess,sys,yaml,os
root=Path('cay-kho').resolve()
out=Path('/tmp/wp943-review2.05gESZ')
lease=dict(schema_version=2,packet_issue=943,lease_id='review2-synthetic',
 role='executor',provider='claude',executor='claude',model_family='claude',
 execution_surface='claude_code',transport='machine/local',reviewer='codex',
 reviewer_model_family='openai',reviewer_execution_surface='codex_cli',
 reviewer_transport='machine',assurance_target='cross_approved',
 granted_by='ducthangho',lease_expires_at_utc='2099-01-01T00:00:00Z',
 reviewed_sha_required='eb5e5bf119358babf831d2aec0ee27c7e5896c1f',
 review_class='sensitive',effective_review_class='sensitive',
 write_set=['docs/PROTOCOL_DA_PHIEN.md'],thay_the_cho=[])
(out/'fixture.yaml').write_text(yaml.safe_dump(lease,allow_unicode=True))
for value in [30,360]:
 d=dict(lease,heartbeat_required_minutes=value)
 f=out/f'lease-{value}.yaml'; f.write_text(yaml.safe_dump(d,allow_unicode=True))
 p=subprocess.run([sys.executable,'-B',str(root/'ops/lease_publish.py'),'check',str(f)],capture_output=True,text=True)
 loaded=yaml.safe_load(f.read_text())
 print(f'value={value}; CLI rc={p.returncode}; readback={loaded["heartbeat_required_minutes"]}; type={type(loaded["heartbeat_required_minutes"]).__name__}')
 print(p.stdout.strip())
 if p.stderr:print(p.stderr.strip())
 assert p.returncode==0 and loaded['heartbeat_required_minutes']==value
```

Output thật (rc script 0):

```text
value=30; CLI rc=0; readback=30; type=int
LỆNH check KHÔNG CHẠY hai lớp GitHub: đo ISSUE/PR và dò comment; dùng `kiem-github`
lease review2-synthetic ĐĂNG ĐƯỢC — issue #943, neo eb5e5bf11935, hết hạn 2099-01-01T00:00:00Z
value=360; CLI rc=0; readback=360; type=int
LỆNH check KHÔNG CHẠY hai lớp GitHub: đo ISSUE/PR và dò comment; dùng `kiem-github`
lease review2-synthetic ĐĂNG ĐƯỢC — issue #943, neo eb5e5bf11935, hết hạn 2099-01-01T00:00:00Z
```

- Kết luận: **KHÔNG PHẢI LỖI**. Cả 30 và 360 qua cửa thuần, bảo toàn số nguyên. Đây là phép đo tính tương thích dữ liệu; việc kiểm thời điểm cấp và áp ngưỡng thuộc phiên điều phối làm tay, không được suy rằng CLI đã cưỡng chế luật mới.

### HƯỚNG 9: Có bộ thu hồi tự động 30 phút còn sống trong mã không

- Giả thuyết: lời giải thích “không controller trong kho” chỉ dựa phép đo cũ; mã hiện hành vẫn thu hồi theo 30 phút hoặc dùng cùng đồng hồ cho hết hạn tuyệt đối.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp943-review2.05gESZ/hunt9.py` từ cwd. Gọi hàm sản xuất `_phan_loai_lease` với hai ngưỡng và hai trạng thái hết hạn; đồng thời quét mọi Python production tracked, loại test, fragment và hiện vật review.

```python
from pathlib import Path
import subprocess,runpy
from datetime import datetime,timedelta,timezone
root=Path('cay-kho').resolve()
m=runpy.run_path(str(root/'ops/lease_publish.py'))
now=datetime(2026,10,27,tzinfo=timezone.utc)
for threshold in [30,360]:
 for expired in [False,True]:
  lease={'heartbeat_required_minutes':threshold,
         'heartbeat_at':(now-timedelta(minutes=threshold+1)).isoformat(),
         'lease_expires_at_utc':(now+timedelta(minutes=-1 if expired else 10)).isoformat()}
  got=m['_phan_loai_lease'](lease,now)
  print('threshold=',threshold,'heartbeat_age=',threshold+1,'absolute_expired=',expired,'class=',got)
  assert got==('HẾT_HẠN' if expired else 'CÒN_HẠN')
paths=subprocess.check_output(['git','-C',str(root),'ls-files','-z']).decode().split(chr(0))
code=[p for p in paths if p.endswith('.py') and
      not any(x in p for x in ['/test_fragments/','/tests/','/test_','_test.py','tl_selftest.py','tl_test_fragments_bundled.py','/evidence/','/reviews/'])]
hits=[]
for p in code:
 for n,line in enumerate((root/p).read_text().splitlines(),1):
  if any(k in line for k in ['heartbeat_required_minutes','heartbeat_at','review_sla']):
   hits.append((p,n,line.strip()))
print('production Python files scanned=',len(code))
print('heartbeat/review-SLA field references=',hits)
```

Output thật (rc 0):

```text
threshold= 30 heartbeat_age= 31 absolute_expired= False class= CÒN_HẠN
threshold= 30 heartbeat_age= 31 absolute_expired= True class= HẾT_HẠN
threshold= 360 heartbeat_age= 361 absolute_expired= False class= CÒN_HẠN
threshold= 360 heartbeat_age= 361 absolute_expired= True class= HẾT_HẠN
production Python files scanned= 140
heartbeat/review-SLA field references= []
```

- Kết luận: **KHÔNG PHẢI LỖI**. Hàm đang dùng để phân loại lease chỉ xét hạn tuyệt đối; không tự thu hồi theo heartbeat ở 30 hay 360. Trong 140 tệp Python production đã quét không có tham chiếu ba trường đồng hồ đó. Đã đọc đường `record-lease`, `check`, `ai-dang-giu` và workflow liên quan: không có controller thu hồi theo tiến triển để cần đồng bộ số 30 trong packet này. Việc áp ngưỡng là thủ công như văn bản mới khai; phép quét tĩnh không chứng minh hành vi của một hệ thống ngoài kho.



### HƯỚNG 10: Có nhầm kích hoạt ngưỡng với kích hoạt sổ thu hồi ADR-0047 không

- Giả thuyết: Văn bản cho thu hồi tay nhưng cửa sổ thu hồi đang tắt sẽ cản vận hành, hoặc wp943 vô tình mở sổ trước authority.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python -B /tmp/wp943-review2.05gESZ/hunt10.py` từ cwd.

```python
from pathlib import Path
import runpy,subprocess
root=Path('cay-kho').resolve()
m=runpy.run_path(str(root/'ops/lease_publish.py'))
print('SO_THU_HOI_KICH_HOAT=',m['SO_THU_HOI_KICH_HOAT'])
for ref in ['3e973a0','HEAD']:
 entries=m['_quet_so_thu_hoi_moi_ref'](root,[ref])
 m['_kiem_so_rong_khi_chua_kich_hoat'](root,[ref])
 print(ref,'ledger_entries=',len(entries),'empty-ledger guard=PASS')
old={'lease_id':'old','da_bi_thay_the':'new'}
for inverse in [[],['old']]:
 records=[{'lease':{'lease_id':'new','thay_the_cho':inverse}}]
 print('legacy tombstone inverse=',inverse,'result=',m['_bia_mo_doi_xung'](old,records))
probe=Path('/tmp/wp943-review2.05gESZ')/'ledger-mutant'
subprocess.run(['git','clone','--local','--no-hardlinks','--quiet',str(root),str(probe)],check=True)
file=probe/'ops/thu-hoi/review2-probe.yaml'
file.parent.mkdir(parents=True,exist_ok=True)
file.write_text('lease_id: review2-probe\n')
subprocess.run(['git','-C',str(probe),'add',str(file.relative_to(probe))],check=True)
subprocess.run(['git','-C',str(probe),'-c','user.name=ReviewProbe','-c','user.email=review-probe@example.invalid',
                '-c','commit.gpgsign=false','-c','core.hooksPath=/dev/null',
                'commit','--quiet','-m','Local isolated review probe'],check=True)
try:m['_kiem_so_rong_khi_chua_kich_hoat'](probe,['HEAD'])
except m['Chan'] as e:
 print('isolated ledger mutation rc=',e.ma,'message=',e.thong_diep)
 assert e.ma==12
else:raise AssertionError('mutation not rejected')
```

Output thật (rc script 0):

```text
SO_THU_HOI_KICH_HOAT= False
3e973a0 ledger_entries= 0 empty-ledger guard=PASS
HEAD ledger_entries= 0 empty-ledger guard=PASS
legacy tombstone inverse= [] result= False
legacy tombstone inverse= ['old'] result= True
isolated ledger mutation rc= 12 message= KHÔNG_XÁC_ĐỊNH: SO_THU_HOI_KICH_HOAT=False mà sổ có bản ghi ops/thu-hoi/review2-probe.yaml tại HEAD — bản ghi lọt trước kích hoạt: dừng, phục hồi có audit, không grandfather
```

- Kết luận: **KHÔNG PHẢI LỖI**. Ngưỡng thời gian và cơ chế sổ thu hồi là hai thứ độc lập. Ở cả base/head sổ rỗng, cờ vẫn False; bia mộ hai chiều hiện hành vẫn xác nhận đúng. Đột biến thêm một tệp sổ trên clone riêng bị chặn rc 12. Đã đọc phần A0 của lease_publish.py: đường sản phẩm hiện hành vẫn dùng bia mộ, không cần mở cơ chế ADR-0047 để áp ngưỡng thủ công.


### HƯỚNG 11: Tài liệu kích hoạt có làm manifest/gói phát hành bị stale không

- Giả thuyết: Không cập nhật RELEASE_MANIFEST.json theo SPEC nhưng docs thực tế vẫn vào gói, khiến gói thiếu hash hoặc phát hành nội dung sai.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python -B /tmp/wp943-review2.05gESZ/hunt11.py` từ cwd.

```python
from pathlib import Path
import subprocess,json,sys
root=Path('cay-kho').resolve(); base=Path('/tmp/wp943-review2.05gESZ')/'base'
data=[]
for label,path in [('base',base),('head',root)]:
 p=subprocess.run([sys.executable,'-B',str(path/'scripts/tl.py'),'release-manifest','--root',str(path),'--json'],capture_output=True,text=True)
 print(label,'CLI rc=',p.returncode)
 assert p.returncode==0,(p.stdout,p.stderr)
 d=json.loads(p.stdout);data.append(d)
 print(label,'ok=',d['ok'],'files=',d['file_count'],'content_hash=',d['content_hash'])
 paths={f['path'] for f in d['files']}
 print('target docs in package=',sorted(paths & {'docs/PROTOCOL_DA_PHIEN.md','docs/adr/0056-lease-no-progress-six-hours.md'}))
print('entire release manifest equal=',data[0]==data[1])
assert data[0]==data[1]
```

Output thật (rc script 0):

```text
base CLI rc= 0
base ok= True files= 192 content_hash= e280f452ad090a874c90f35c6310476e02cb32b400e3a7a6e569d7b4959b2929
target docs in package= []
head CLI rc= 0
head ok= True files= 192 content_hash= e280f452ad090a874c90f35c6310476e02cb32b400e3a7a6e569d7b4959b2929
target docs in package= []
entire release manifest equal= True
```

- Kết luận: **KHÔNG PHẢI LỖI**. Đo bằng CLI release-manifest sản xuất: cả hai manifest bằng nhau toàn bộ, 192 tệp và cùng content_hash; hai tài liệu nằm ngoài gói. Đây là kiểm tác động tới hiện vật downstream, độc lập với kiểm write set. Không chạy deploy hoặc tạo quyền phát hành.


### HƯỚNG 12: Metadata và luật áp dụng có thực sự hiển thị đúng trong Markdown không

- Giả thuyết: nguồn nhìn đúng nhưng bảng GFM bị tách cột hoặc câu trích/xác nhận kích hoạt bị rào, danh sách hay nhấn mạnh nuốt mất khi render; agent đọc bảng sẽ không thấy luật mới.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp943-review2.05gESZ/hunt12.py` từ cwd. Dùng Pandoc GFM thực sự, đọc DOM bằng BeautifulSoup.

```python
from pathlib import Path
import subprocess
from bs4 import BeautifulSoup
root=Path('cay-kho').resolve()
print(subprocess.check_output(['pandoc','--version'],text=True).splitlines()[0])
docs=['docs/adr/0056-lease-no-progress-six-hours.md','docs/PROTOCOL_DA_PHIEN.md']
html=[]
for name in docs:
 p=subprocess.run(['pandoc','--from=gfm','--to=html','--wrap=none',str(root/name)],capture_output=True,text=True)
 print(name,'pandoc rc=',p.returncode)
 assert p.returncode==0
 html.append(BeautifulSoup(p.stdout,'html.parser'))
adr,protocol=html
matches=[tr for tr in protocol.find_all('tr') if tr.find('td') and tr.find('td').get_text(' ',strip=True)=='ADR-0056']
print('rendered ADR0056 table rows=',len(matches))
assert len(matches)==1
cells=matches[0].find_all('td',recursive=False)
print('rendered table cells=',len(cells))
print('status=',cells[2].get_text(' ',strip=True))
print('gate=',cells[3].get_text(' ',strip=True))
assert len(cells)==4 and 'đã kích hoạt vận hành' in cells[2].get_text()
plain=' '.join(adr.get_text(' ',strip=True).split())
quote='Không có, phiên điều phối làm tay'
print('hard-wrapped quote preserved=',quote in plain)
strong=[e.get_text(' ',strip=True) for e in adr.find_all('strong')]
print('active phrase rendered bold=','ĐÃ KÍCH HOẠT VẬN HÀNH' in strong)
print('new paragraph rendered text=',next(' '.join(p.get_text(' ',strip=True).split()) for p in adr.find_all('p') if p.get_text().startswith('Mốc 26-10-2026')))
assert quote in plain and 'ĐÃ KÍCH HOẠT VẬN HÀNH' in strong
```

Output thật (rc 0):

```text
pandoc 3.1.3
docs/adr/0056-lease-no-progress-six-hours.md pandoc rc= 0
docs/PROTOCOL_DA_PHIEN.md pandoc rc= 0
rendered ADR0056 table rows= 1
rendered table cells= 4
status= Accepted — đã kích hoạt vận hành (merge PR thi công wp943)
gate= 0 cổng — không controller trong kho mang hằng 30 phút; không có controller ngoài, phiên điều phối áp tay
hard-wrapped quote preserved= True
active phrase rendered bold= True
new paragraph rendered text= Mốc 26-10-2026: chủ kho xác nhận không có controller ngoài (dispatcher) — "Không có, phiên điều phối làm tay" (#835 issuecomment-6407154789). Thu hồi lease do phiên điều phối làm tay theo protocol, nên "đồng bộ controller" nghĩa là phiên điều phối áp ngưỡng 360 phút khi xét thu hồi. Luật áp dụng: chỉ lease cấp SAU mốc kích hoạt (merge của PR thi công wp943 ) khai heartbeat_required_minutes: 360 ; lease cấp trước mốc ấy giữ nguyên byte và số đã đóng dấu — kể cả lease wp943-r1-g1-claude của chính packet kích hoạt, vẫn khai 30.
```

- Kết luận: **KHÔNG PHẢI LỖI**. Đúng một hàng ADR-0056, đủ bốn ô, trạng thái kích hoạt hiển thị đậm, đoạn luật và câu trích còn đủ. Lần probe đầu so nguyên văn nội dung thẻ strong thất bại vì Pandoc tự wrap HTML thành dòng mới; đã kiểm repr của thẻ, dùng `--wrap=none` và chạy lại. Đây là lỗi thước đo whitespace của probe, không phải lỗi Markdown của candidate.


### HƯỚNG 13: “Phiên điều phối làm tay” có vô tình cấp quyền cho agent tự cấp/thu hồi lease không

- Giả thuyết: bỏ điều kiện controller ngoài sẽ được diễn giải thành cho phép bất cứ agent mang tên dispatcher tự cấp hay thu hồi lease 360, vượt allowlist authority.
- Lệnh: `PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp943-review2.05gESZ/hunt13.py` từ cwd. Tái dùng fixture schema v2 của hướng 8, đo đối chứng owner hợp lệ và hai tên provider/giả dispatcher; kiểm riêng cấp và thu hồi bằng validator sản xuất. Tất cả chỉ là dữ liệu thử ngoài kho.

```python
from pathlib import Path
import subprocess,sys,yaml,runpy
from datetime import datetime,timezone
root=Path('cay-kho').resolve(); out=Path('/tmp/wp943-review2.05gESZ')
m=runpy.run_path(str(root/'ops/lease_publish.py'))
fixture=yaml.safe_load((out/'fixture.yaml').read_text())
for actor in ['ducthangho','codex','codex-dispatcher']:
 lease=dict(fixture,heartbeat_required_minutes=360,granted_by=actor)
 file=out/f'authority-{actor}.yaml';file.write_text(yaml.safe_dump(lease))
 p=subprocess.run([sys.executable,'-B',str(root/'ops/lease_publish.py'),'check',str(file)],capture_output=True,text=True)
 print('grant actor=',actor,'CLI rc=',p.returncode)
 if p.stderr:print(p.stderr.strip())
 assert p.returncode==(0 if actor=='ducthangho' else 4)
 record=dict(schema_version=1,event='lease_revoked',lease_id='review2-synthetic',packet_issue=943,
             thu_hoi_boi=actor,thu_hoi_luc_utc='2026-10-26T00:00:00Z',ly_do='offline synthetic authority probe',
             can_cu='https://github.com/ducthangho/tra-luat/issues/943#issuecomment-6416417774')
 try:
  m['kiem_ban_ghi_thu_hoi']('ops/thu-hoi/review2-synthetic.yaml','100644','blob',
                          yaml.safe_dump(record).encode(),datetime(2026,10,27,tzinfo=timezone.utc))
  rc=0
 except m['Chan'] as e:rc=e.ma
 print('revoke actor=',actor,'pure validator rc=',rc)
 assert rc==(0 if actor=='ducthangho' else 4)
```

Output thật (rc 0):

```text
grant actor= ducthangho CLI rc= 0
revoke actor= ducthangho pure validator rc= 0
grant actor= codex CLI rc= 4
CHAN [4]: granted_by='codex' là tên một provider — agent KHÔNG tự cấp lease cho mình được (doctrine 'không tự cấp lease')
revoke actor= codex pure validator rc= 4
grant actor= codex-dispatcher CLI rc= 4
CHAN [4]: granted_by='codex-dispatcher' KHÔNG nằm trong danh sách người có thẩm quyền ['ducthangho'] — danh sách CẤM không bao giờ đủ (cross-review 14-08-2026, finding lease-authority-spoof), nên cổng này đòi tên phải ĐƯỢC PHÉP chứ không chỉ 'không bị cấm'. Thêm người cấp mới = sửa NGUOI_CO_THAM_QUYEN qua một commit có review.
revoke actor= codex-dispatcher pure validator rc= 4
```

- Kết luận: **KHÔNG PHẢI LỖI**. Ngưỡng 360 không mở rộng allowlist: owner qua đối chứng; cả `codex` lẫn `codex-dispatcher` bị chặn rc 4 ở hai cửa. Văn bản mới nói cách áp ngưỡng, không sửa authority. Parser bản ghi thu hồi chỉ được gọi để thử schema/authority; rc 0 của fixture không có nghĩa cơ chế sổ đã được kích hoạt hay bản ghi đã được chấp thuận trên GitHub.


## SELFTEST ĐỘC LẬP — CẬP NHẬT SAU KHI CHỐT VERDICT

Đã chạy đến hết trên exact head bằng `PYTHONDONTWRITEBYTECODE=1 GIT_OPTIONAL_LOCKS=0 python -B scripts/tl.py --selftest` từ cay-kho/, log `/tmp/wp943-review2.05gESZ/selftest-independent.log` (sha256 `1fecb426aeb64eddaa85c8965e4c1ca37d0e8f7f9e7ae0cbbd850a0a9d3044e3`). Kết quả thật: **rc 1, `== tl selftest 1729/1731 ==`**. Không coi đây là N/N đạt. Hai ca thất bại là `r226_nguong_l2_troi_theo_abbrev_va_ci_ghim` và `r268_l2_trichotomy_theo_trang_thai_object`.

Đã đọc nguyên thân hai ca tại scripts/tl_selftest.py:26947 và :28552: cả hai tự khởi tạo kho Git tạm và cần commit fixture. Probe tạo mini-repo theo đúng lệnh của ca cho kết quả:

```text
git init -q rc= 0
git add -A rc= 0
git commit -q -m c1 rc= 128
MCP server request failed ... dial tcp 127.0.0.1:45717: socket: operation not permitted
fatal: failed to write commit object
git rev-parse HEAD rc= 128
```

Đây là lệnh ký commit của cấu hình môi trường gọi dịch vụ loopback bị sandbox chặn; không phải kiểm nội dung wp943. Đã trích nguyên hàm bằng AST (không sửa hàm), nạp module tl tương ứng của từng checkout và chạy riêng cả hai ca ở HEAD và clone base. Lệnh:

```sh
PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp943-review2.05gESZ/probe-selftest-failures.py cay-kho
PYTHONDONTWRITEBYTECODE=1 python -B /tmp/wp943-review2.05gESZ/probe-selftest-failures.py /tmp/wp943-review2.05gESZ/base
```

Output thật, cắt gọn (hai script đều rc 0 vì chúng báo chẩn đoán, không tự nhận test đạt):

```text
cay-kho _c226_nguong_l2_troi_theo_abbrev_va_ci_ghim result= False
cay-kho _c268_l2_trichotomy_theo_trang_thai_object result= False
base _c226_nguong_l2_troi_theo_abbrev_va_ci_ghim result= False
base _c268_l2_trichotomy_theo_trang_thai_object result= False
```

Ở cả hai probe, commit fixture đều rc 128 với cùng lỗi ký/MCP loopback. Code dưới scripts/ và cấu hình CI mà hai ca đọc bằng byte giữa base/head; hai ca chỉ quét tài liệu trong mini-repo tự dựng. Không có delta do bản vá cho cơ chế thất bại này. Không chỉnh cấu hình ký hay hạ safeguard để biến selftest thành xanh. Đây là giới hạn kiểm chứng hạ tầng, không ghi thành finding sản phẩm. Phần selftest đầy đủ độc lập không được chứng nhận pass; bằng chứng N/N đầy đủ còn lại là log executor được assignment cấp.

Selftest sinh thêm 9 tệp dưới `references/golden/fixtures/` và 11 tệp dưới `scripts/.tl_state/`, đều là ignored và đều chưa tồn tại ở snapshot ngay trước selftest. Đã chuyển riêng hai thư mục do selftest sinh sang `/tmp/wp943-review2.05gESZ/selftest-generated-artifacts/` để bảo toàn hiện vật và trả checkout về sạch. Snapshot cuối: status gồm ignored rỗng, diff tracked/index rỗng, HEAD/tree giữ nguyên. Không tuyên bố cả lượt chưa từng ghi checkout.

Không có finding P0/P1/P2/P3 (0 lớp, 0 biểu hiện). Giữ **approve** cho nội dung trên exact head. Căn cứ selftest N/N là log executor `1731/1731` (sha256 `a4c5b5f9b86a5c7686109bf7c35959191c1e81aae7f41a385c5f8f19d7f597a1`); kết quả độc lập thất bại hạ tầng được giữ nguyên ở trên. N5 vẫn **KHÔNG ĐO ĐƯỢC**: approval nội dung này không xác nhận CI xanh hoặc đủ điều kiện merge; không cấp quyền merge/land/deploy.

# XONG
