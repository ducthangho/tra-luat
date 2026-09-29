# Cross-review vòng 6 — PR #455

**approve_with_findings — hai P2 và một P3; chưa chứng minh P0/P1 mới.** Các phản chứng cụ thể của vòng 5 đã được khóa, nhưng bản vá vẫn thiếu khóa nhánh và còn một đường mất dữ liệu nguồn được báo sạch. Không nâng lỗi độ phủ thành P1 để kéo dài vòng review.

- `reviewed_sha`: `5a78c150106ae381461354c77ba2023834330bbd`
- `reviewed_tree`: `2e42173bfadd3869dfcc40ca2734723172fb58eb`
- Base diff: `670071b700bd97a893d64393ffded0257957d0b3`; đã xem diff 7 tệp.
- Reviewer độc lập với context Executor Claude; axes `spec`, `standards_security`; Review Class `sensitive` vì thay đổi cổng identity/evidence.
- Provider `openai_codex`; execution surface **Codex service/API với shell trong Linux container**; transport `machine`. Chỉ thị định danh agent GPT-6; không có chứng thực độc lập backend/model version. Không tự nhận ChatGPT Web hoặc một run CLI có launcher attestation.
- Authority: yêu cầu trực tiếp của user giao vòng 6, exact head/base, write set chỉ `VERDICT.md`. Không có Packet revision/spec hash/generation/lease riêng để xác minh; không tự cấp chúng. Yêu cầu này giao review hiện tại, không cấp state transition, vòng kế tiếp, approval GitHub hoặc land.

Preflight tự đo: origin `https://github.com/ducthangho/tra-luat`; detached (`git symbolic-ref -q HEAD`: rc=1, stdout rỗng); `is-shallow-repository=false`; `git rev-list --count HEAD` = **1740**; worktree ban đầu sạch. Đã đọc CONTEXT, protocol, CLAUDE, kế hoạch đa provider và verdict vòng 5 trước khi soi bản vá; đối chiếu các finding lịch sử vòng 1–4. Không dùng provider AG/ChatGPT Web nên không áp hợp đồng thực thi của hai bề mặt ấy. Phạm vi này không thay pháp luật/corpus hoặc runtime skill.

Chỉ dùng phản chứng có sẵn và đột biến mã/nguồn trên cây tạm ngoài repository. **Không tự soạn payload receipt hoặc văn bản tấn công mới.** Các hướng cần nội dung mới được giao lại bằng lời bên dưới. Bản sao có `.git` trỏ kho gốc chỉ để truy vấn đọc; không commit/push.

## Đóng bản vá vòng 5 đến đâu

| Chốt được giao | Kết quả độc lập |
|---|---|
| R5-01: bảng transport rỗng, lỗi decode | **Đóng các phản chứng cụ thể.** c28 qua; gỡ riêng `if not hd` hoặc bắt `UnicodeDecodeError` làm assertion c28 đỏ: đòi rc=2 nhưng nhận 1. Mỗi bản sao 39/40 ca nền. Không lấy lỗi neo mutant nội bộ làm bằng chứng kill. |
| R5-02: nới tập provider bằng surface | **Đóng phản chứng cũ.** Chèn lại phép hợp surface trước return, giữ nguyên neo m29: c31 chỉ đúng ba tên thừa `claude_code`, `codex_cli`, `llm_cli`; rc=1, 39/40 ca nền, 42/42 mutant nội bộ. |
| R5-02: mất nội dung nguồn 2/3 | Ca hiện tại qua. Tuy nhiên nguồn 2 nay tách hai literal mà c28 làm hỏng cả hai cùng lúc; hai guard riêng vẫn gỡ được: R6-01. |
| Connector P1: ChatGPT Web và assurance | c36 khóa phản chứng có sẵn cho `cross_approved`, surface lạ và đối chứng advisory. m32/m33 bị bắt. **Chưa khóa đủ mọi mức cấm/provider**: R6-01; không gọi mutant sống là lỗ đang tồn tại trong bản nguyên gốc. |
| Connector P2: verdict path | c37 và m34 qua; fixture c19 đã đổi cả path và URL để tới nhánh trỏ hụt. Chưa chứng minh mọi dạng chuẩn hóa đường dẫn. |
| Connector P2: Git thao tác thứ sáu | c32 và m35 qua. Trace độc lập: 7 lượt `kiem`, số lần bơm tương ứng **0,1,1,1,1,1,1**. Lượt đầu `loi=[]`, `chua_do=[]`; sáu lượt sau đều không lỗi receipt và đúng một chưa đo. Matcher mới thực sự chỉ chạm `rev-parse <commit>:<path>`. |
| c35: bốn hướng văn bản tự do | Bốn fixture có sẵn chạy qua, m31 bị c35 bắt. Chưa đo nội dung đánh lừa nằm trong literal/khối mã rào; không nhận bốn fixture là chứng minh parser tổng quát. |

## R6-01 — P2: chốt mới vẫn khóa đúng phần giá trị mà fixture chọn

**Vá ở đâu:** `ops/bien_nhan_v2_test.py:887` (bảng c28), `:975` (c31 chọn surface từ sản phẩm), `:1225` (c36). Đây là lỗi độ phủ hồi quy của chính bản vá, không phải bốn lỗi P1 sản phẩm.

**Bằng chứng chạy được:** giữ nguyên toàn suite, mỗi lần chỉ đột biến sản phẩm trên bản sao. Cả bốn phép làm yếu đều **rc=0 · 40/40 ca · 42/42 mutant thường · 1/1 tự kiểm · 25/42 đối chứng · TỔNG: ĐẠT**, không lỗi giàn giáo:

| ID phép đo | Phép làm yếu và nhánh bị bỏ |
|---|---|
| `only_cross_banned` | Sau khi đọc `cam`, giao với tập chỉ chứa `cross_approved`. Mất cấm `same_provider_approved` và `human_audited`; c36 chỉ thử mức đầu. |
| `only_two_surfaces` | Đặt `hop_le=None` cho provider ngoài `openai_chatgpt`/`openai_codex`. Ba provider chính tắc khác mất kiểm surface; ca âm c36 chỉ chọn hai tên trên. |
| `empty_kha_nang` | Đổi `if not tim` thành chỉ báo lỗi khi bảng là `CONG_CU`; bỏ guard rỗng riêng `KHA_NANG`. |
| `empty_cong_cu` | Đổi guard theo chiều ngược lại; bỏ guard rỗng riêng `CONG_CU`. |

Hai mutant cuối không phải tương đương: phép đo nguồn riêng với nguyên bản, thay từng literal bằng `[]`, đều trả **rc=2**, có thông báo chỉ đúng bảng bị mất. c28 hiện thay cả hai cách khai provider trong toàn launcher, nên bảng nào còn guard cũng bắt lỗi chung. Nó không phân biệt hai đường độc lập. c31 lấy fixture surface từ `PROVIDER_BE_MAT` của chính sản phẩm và không có ma trận ca âm cho phần còn lại, nên không bù được lỗ này.

**Vá thế nào:** mở rộng c36 thành ma trận nhỏ theo từng mức assurance cấm và từng provider có hợp đồng surface; oracle phải độc lập với tập cấm/bản đồ đang bị kiểm. Tách c28 thành hàng làm mất riêng từng literal, giữ bảng còn lại nguyên vẹn. Không cần dựng thêm verifier danh tính hay tăng số lượng ca chỉ để đẹp tổng.

**Ca test khóa:** bốn mutant trên phải chết bằng assertion của ca nền tương ứng; đối chứng advisory và từng surface đúng vẫn qua. Điều phối cần chuẩn bị dữ liệu receipt cho các nhánh assurance/surface còn thiếu vì phiên này không được tự soạn chúng. Hai ca xóa literal đã chạy trong `sources.py`, có thể tái dùng nguyên phép biến đổi nguồn. Không chỉ thêm mutant gỡ toàn bộ guard: chúng đã bị bắt nhưng không khóa các nhánh vừa đo.

**Bản vá có thể đẻ ra gì:** sinh oracle từ `ASSURANCE_CAM_THEO_PROVIDER`/`PROVIDER_BE_MAT` lại khiến test cùng co với sản phẩm; hard-code mọi tên ở nhiều nơi gây drift. Lỗi nguồn của một bảng có thể bị bảng khác che nếu fixture làm hỏng cả hai; phải assert cả lý do cụ thể và dữ liệu còn lại vẫn nguyên. `42/42` là số mutant được chọn, không phải toàn bộ không gian lỗi.

## R6-02 — P2: nguồn Web mất surface vẫn được coi là dùng được

**Vá ở đâu:** `ops/bien_nhan_v2.py:238–250`, `_provider_chinh_tac`, và `:297–298`, `_mri`. Parser thêm provider vào `web` trước khi biết có surface; `if s_` chỉ thêm cặp khi tìm thấy. `_mri` chỉ kiểm surface khi `hop_le` truthy, nên bản đồ thiếu cặp trở thành miễn kiểm.

**Bằng chứng chạy được:** dùng nguyên `_cay_guong` và receipt Git hợp lệ có sẵn, không đổi receipt. Chỉ **xóa dòng hiện có** `execution_surface: chatgpt_web` khỏi bản sao `AGENTS.md`:

| Nguồn | rc thật | Kết quả |
|---|---:|---|
| Nguyên bản | 0 | 1 đạt v2, 0 vi phạm, 0 chưa đo; 5 cặp surface |
| Mất riêng dòng surface Web | **0** | **1 đạt v2, 0 vi phạm, 0 chưa đo, `TỔNG: ĐẠT`**; `PROVIDER_NGUON_HONG=None`; bản đồ chỉ còn 4 cặp nhưng `openai_chatgpt` vẫn được nhận vào tập provider |
| Mất riêng nội dung mỗi literal launcher | 2 | 0 vi phạm, 1 chưa đo; tên bảng bị mất được nêu chính xác |

Đây là dữ liệu nguồn **có tên nhưng không đủ hợp đồng mới vừa thêm**. Phép đo dùng receipt Codex nền, không chứng minh một receipt ChatGPT giả đã được nhận hoặc một approval thực tế đã được cấp. Vì thế xếp **P2**, không P1. Điều đã đo chắc chắn là nguồn thiếu cặp mà không có trạng thái thứ ba; đọc mã xác định đường miễn kiểm đối với provider ấy.

**Vá thế nào:** yêu cầu mỗi provider chính tắc được đọc từ khối Web phải có surface hợp lệ trước khi hợp nhất nguồn. Thiếu cặp phải giữ lý do tới rc=2, không dùng `None` như miễn kiểm ngầm. Miễn trừ lịch sử cần là nhánh có điều kiện riêng, không đồng nhất với mọi khóa thiếu trong bản đồ.

**Ca test khóa:** dùng nguyên phép xóa dòng trong `sources.py`: sau vá phải rc=2, 0 vi phạm và có thông báo thiếu surface của nguồn Web; cây nguyên bản vẫn rc=0. Đột biến bỏ yêu cầu surface bắt buộc/khôi phục việc chỉ thêm cặp khi có phải chết. Với ma trận receipt từng provider, điều phối viết thêm ca surface không đúng để khóa đường `_mri`; phiên này chưa viết/chạy dữ liệu mới đó.

**Bản vá có thể đẻ ra gì:** cấm cả alias lịch sử hoặc ép schema mới lên hiện vật cũ sẽ bắt oan. Báo thiếu nguồn thành receipt vi phạm tái tạo R4-02; tự điền surface mặc định tạo bằng chứng giả. Không bắt mọi ngoại lệ rồi trả bản đồ dự phòng.

## R6-03 — P3: mô tả “bộ ba” rộng hơn phép kiểm đang chạy

**Vá ở đâu:** `ops/bien_nhan_v2.py:292–295`, tên/chú thích m33 trong test, và CHANGELOG phần vòng bảy. Chú thích dẫn yêu cầu `provider/surface/transport tuple`, nhưng cấu trúc mới là **provider → tập surface**, và cổng không đọc trường transport nào của receipt. Năm cặp không phải năm bộ ba.

**Bằng chứng:** đọc AST/nguồn và readback `PROVIDER_BE_MAT` cho đúng năm cặp được liệt kê dưới; tìm `transport` trong module chỉ thấy chú thích, không có đường lấy trường để validate. Phép đo không chứng minh transport sai bị từ chối. Đây là lỗi mô tả phạm vi, chưa phải bằng chứng khai thác mới.

**Vá thế nào:** đường nhỏ nhất là ghi đúng “kiểm cặp provider–surface; chưa kiểm transport” và ghi nợ transport nếu ngoài phạm vi. Nếu quyết định thực thi bộ ba, cần chốt schema/vị trí trường và ngoại lệ lịch sử trước; không lặng lẽ bắt buộc một trường mới.

**Ca test khóa:** với đường sửa tài liệu, đối chiếu mô tả với các trường thực sự được đọc; không cần test tìm chuỗi để duy trì prose. Với đường mở rộng sản phẩm, cần đối chứng cùng provider/surface nhưng khác transport; mutant bỏ so transport phải chết. **Chưa chạy** ma trận ấy: điều phối phải cung cấp fixture và phạm vi schema, không được tính các mutant surface hiện tại thay thế nó.

**Bản vá có thể đẻ ra gì:** transport của người đăng và của reviewer là hai lớp khác nhau; gộp chúng sẽ bắt oan receipt hợp lệ hoặc chứng thực nhầm lớp. Không suy transport từ actor GitHub.

## Bốn vùng mỏng và hiệu chỉnh lời khai

1. **Bí danh lịch sử:** `PROVIDER_LICH_SU={'anthropic','human'}` miễn kiểm surface theo tên, không theo filename/hash hay tuổi receipt. Đọc `_mri` thấy không có phân biệt receipt mới/cũ ở chốt này. Hướng yêu cầu điều phối soạn: receipt MỚI dùng alias với surface trái hợp đồng và assurance có thẩm quyền; đối chứng hiện vật lịch sử nguyên byte. Tôi **chưa chạy payload mới này**, không khẳng định đã chứng minh P1. Hướng vá cần cân nhắc alias có hợp đồng surface hoặc ngoại lệ có phạm vi, tránh viết lại lịch sử.
2. **Luật chép tay:** câu neo còn nguyên và c28/m36 đo việc mất câu. Phép tìm substring chỉ chứng minh câu có mặt, không chứng minh vị trí/ngữ nghĩa còn là điều cấm. Hướng cần dữ liệu mới về câu trích dẫn/khối ví dụ được giao điều phối, chưa chạy. Không tìm thấy bằng chứng đã đo đủ mọi hạn chế assurance của mọi provider.
3. **Hướng thứ năm của c35:** AST walker lấy mọi hằng chuỗi trong assignment, không chỉ một trường metadata; parser Web đọc mọi khối rào khớp regex, không định vị riêng khai báo §4. Cần điều phối cung cấp nội dung không phải khai báo provider nhưng nằm trong vùng ấy. Bốn hướng hiện tại đã qua; **chưa chứng minh** hướng này bị chặn hoặc đã khai thác được.
4. **Hình dạng lỗi:** c32 có sáu lần bơm riêng đã trace, ngoài ra c26 đo lỗi merge-base. Chưa bao trọn mọi mã lỗi Git/I/O. Mutant `che_do_str` tái chạy vẫn rc=0 với toàn tổng xanh; như R5, chưa có bằng chứng nó gây nhận sai nên không nâng thành finding sản phẩm.

Số đo độc lập: **7 provider = 5 tên chính tắc đọc từ nguồn + 2 bí danh chép tay**. Năm cặp là `anthropic_claude/claude_code`, `openai_codex/codex_cli`, `openai_api/llm_cli`, `google_antigravity/antigravity`, `openai_chatgpt/chatgpt_web`. Lời giao “không tên nào chép tay” không đúng với cả bảy tên. AST c28 có **11 hàng: 1 đối chứng + 10 hàng fail-close**, không phải chín; sửa con số không tự sửa lỗ từng bảng ở R6-01.

Receipt vòng 5 không thuộc miễn trừ/nợ; `_thieu=[]`, `_neo_git=([],[])`. Commit neo **`296cceec36a43bdebedd6357e055d61bc60f8158`** là tổ tiên HEAD local (`merge-base --is-ancestor`: rc=0). `git show <sha>:ops/reviews/pr455-bien-nhan-v2-review-5-codex-verdict.md`: rc=0; blob khớp byte local và digest **`331fa1296a6d65e684352de9073f9c7a09b0b970ee1e81974f0f978248dbde8e`**. Không coi lời khai launcher/delivery trong receipt là chứng thực độc lập của phiên này.

## Phụ lục — phép đo tái lập đã chạy

Các script dưới đã chạy từ root clone với `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr455-r6-evidence/<tên>.py`. Tạo thư mục `/tmp/pr455-r6-evidence` trước. Mỗi script rc=0, có marker hoàn tất; rc riêng của subprocess mutant được ghi trong kết quả, không nhập với rc của script. Log tạm không phải hiện vật bền; mã dưới giữ khả năng tái lập.

### mutate.py

```python
import sys,os,subprocess,tempfile,shutil,json,concurrent.futures
from pathlib import Path
R=Path.cwd(); E=Path('/tmp/pr455-r6-evidence'); S=(R/'ops/bien_nhan_v2.py').read_text()
mut={
'empty_contract':('    if not hd:\n','    if False:\n'),
'decode':('    except (OSError, UnicodeDecodeError) as ex:', '    except OSError as ex:'),
'excess_provider':('    return hd | ngoai | web, {k: frozenset(v) for k, v in bm.items()}, None','    hd |= {t.elts[2].value for t in n.value.elts}\n    return hd | ngoai | web, {k: frozenset(v) for k, v in bm.items()}, None'),
'only_cross_banned':('        if khai in cam:', '        cam = cam & {"cross_approved"}\n        if khai in cam:'),
'only_two_surfaces':('    if PROVIDER_NGUON_HONG is None and hop_le and be_mat not in hop_le:', '    if prov not in {"openai_chatgpt", "openai_codex"}:\n        hop_le = None\n    if PROVIDER_NGUON_HONG is None and hop_le and be_mat not in hop_le:'),
'empty_kha_nang':('        if not tim:', '        if not tim and bang == "CONG_CU":'),
'empty_cong_cu':('        if not tim:', '        if not tim and bang == "KHA_NANG":'),
'che_do_str':('"subagent" in (_chuoi(mri.get("che_do")) or "").lower()', '"subagent" in str(mri.get("che_do") or "").lower()'),
}
def run(item):
 k,(a,b)=item; assert S.count(a)==1,(k,S.count(a))
 with tempfile.TemporaryDirectory(prefix='r6-mut-') as td:
  r=Path(td);shutil.copytree(R/'ops',r/'ops',ignore=shutil.ignore_patterns('__pycache__'));(r/'.claude/dev').mkdir(parents=True);shutil.copyfile(R/'.claude/dev/launcher.py',r/'.claude/dev/launcher.py');shutil.copyfile(R/'AGENTS.md',r/'AGENTS.md');(r/'.git').write_text('gitdir: '+str(R/'.git')+'\n');(r/'ops/bien_nhan_v2.py').write_text(S.replace(a,b))
  q=subprocess.run([sys.executable,str(r/'ops/bien_nhan_v2_test.py')],cwd=r,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
  (E/(k+'.log')).write_text(q.stdout+q.stderr)
  return {'mutation':k,'rc':q.returncode,'tail':q.stdout.splitlines()[-3:],'errors':[l for l in q.stdout.splitlines() if l.startswith(('  ĐỎ','  KHÔNG RĂNG','  KHÔNG ĐO'))]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for x in ex.map(run,mut.items()):print(json.dumps(x,ensure_ascii=False),flush=True)
print('MUTATION_COMPLETE')
```

### sources.py

```python
import sys,subprocess,tempfile,importlib.util,json
from pathlib import Path
R=Path.cwd();sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('t',R/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
for label in ['baseline','remove_web_surface','remove_KHA_NANG','remove_CONG_CU']:
 with tempfile.TemporaryDirectory(prefix='r6-source-') as td:
  r=Path(td);p=t._cay_guong(r)
  if label=='remove_web_surface':
   ap=r/'AGENTS.md';v=ap.read_text();old='execution_surface: chatgpt_web';assert v.count(old)==1;ap.write_text(v.replace(old,''))
  if label.startswith('remove_') and label!='remove_web_surface':
   import ast
   lp=r/'.claude/dev/launcher.py';v=lp.read_text();name=label.removeprefix('remove_');n=next(n for n in ast.parse(v).body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')==name);lines=v.splitlines(keepends=True);lines[n.lineno-1:n.end_lineno]=[name+' = []\n'];lp.write_text(''.join(lines))
  q=subprocess.run([sys.executable,str(p),'--root',str(r)],capture_output=True,text=True)
  sp=importlib.util.spec_from_file_location('m',p);m=importlib.util.module_from_spec(sp);sp.loader.exec_module(m)
  print(json.dumps({'label':label,'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr,'source_error':m.PROVIDER_NGUON_HONG,'surfaces':{k:sorted(v) for k,v in m.PROVIDER_BE_MAT.items()}},ensure_ascii=False))
print('SOURCES_COMPLETE')
```

### inspect.py

```python
import ast,sys,importlib.util,subprocess,hashlib,json
from pathlib import Path
import yaml
sys.dont_write_bytecode=True
R=Path.cwd();s=importlib.util.spec_from_file_location('t',R/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
m=t.bnv2
print('PROVIDERS',sorted(m.PROVIDER_CHO_PHEP),'HISTORY',sorted(m.PROVIDER_LICH_SU),'SURFACES',{k:sorted(v) for k,v in m.PROVIDER_BE_MAT.items()},'ERROR',m.PROVIDER_NGUON_HONG)
p=R/'ops/reviews/pr455-bien-nhan-v2-review-5-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text());sha,path=d['evidence_url'].split('/blob/')[1].split('/',1)
q=subprocess.run(['git','show',sha+':'+path],capture_output=True);a=subprocess.run(['git','merge-base','--is-ancestor',sha,'HEAD'])
print('RECEIPT',{'sha':sha,'schema':m._thieu(d),'git':m._neo_git(R,p.name,d),'exempt':p.name in m.ALLOWLIST_CUTOVER,'debt':p.name in m.NO_DA_DO,'blob_rc':q.returncode,'ancestry_rc':a.returncode,'hash':hashlib.sha256(q.stdout).hexdigest(),'hash_match':hashlib.sha256(q.stdout).hexdigest()==d['verdict_sha256'],'local_match':q.stdout==(R/path).read_bytes()})
cay=ast.parse((R/'ops/bien_nhan_v2_test.py').read_text())
f=next(n for n in cay.body if isinstance(n,ast.FunctionDef) and n.name.startswith('c28_'))
loop=next(n for n in f.body if isinstance(n,ast.For)); print('C28_ROWS',len(loop.iter.elts),[ast.literal_eval(n.elts[0]) for n in loop.iter.elts])
phases=[];current=None;orig=m.kiem
def measured(*args,**kw):
 global current
 current={'injected':[]};phases.append(current);r=orig(*args,**kw);current['errors']=r[0];current['unknown']=r[1].get('chua_do');return r
def trace(frame,event,arg):
 if event=='call' and frame.f_code.co_filename==str(R/'ops/bien_nhan_v2_test.py'):
  loc=frame.f_locals
  if frame.f_code.co_name=='_bom' and 'khop' in loc and loc['khop'](loc['args']):current['injected'].append(list(loc['args']))
  if frame.f_code.co_name=='run' and '_Shim' in type(loc.get('self')).__name__:
   cmd=loc['cmd']
   if isinstance(cmd,list) and 'cat-file' in cmd and '-p' in cmd:current['injected'].append(cmd)
 return trace
m.kiem=measured;sys.settrace(trace)
try:r=t._chay_1(t.c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC)
finally:sys.settrace(None);m.kiem=orig
print('C32',r,json.dumps(phases,ensure_ascii=False));assert r[0]=='qua';assert [len(x['injected']) for x in phases]==[0,1,1,1,1,1,1]
print('INSPECTION_COMPLETE')
```

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container, Python 3.11.15, Git 2.43.0, PyYAML có sẵn, `core.abbrev=7` có sẵn; không sửa Git config. Chạy Python với `PYTHONDONTWRITEBYTECODE=1`. Mã thoát lấy từ công cụ tiến trình/subprocess, không suy từ stdout.

| Command/phép đo | rc thật | Trạng thái và bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | **passed theo suite**: 40/40 ca, 42/42 mutant thường, 1/1 tự kiểm, 25/42 khai đối chứng, `TỔNG: ĐẠT`; tầng Git cutover đo được. Giới hạn R6-01. |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | **passed**: 14 đạt v2, 11/11 miễn trừ băm khớp, 42 nợ, 0 vi phạm, 0 chưa đo, tổng 67, `TỔNG: ĐẠT`. |
| `python3 ops/lease_publish_test.py` | 0 | **passed**: 121/121, đã chạy 121, bỏ qua 0. Warning empty repository thuộc fixture. |
| `python3 .claude/dev/packet_loop_test.py` | 0 | **passed**: 278/278, bỏ qua 0; 81 mutant, 78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18, `TỔNG: ĐẠT`. |
| `python3 ops/cong_cu_test.py` | 0 | **passed**: 23/23, bỏ qua 0; 18 mutant, 0 lỗi mutant; 7 ca tự kiểm bộ phân hạng đạt. |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed**: `ok=true`, checked=expected=180; failed/extra/missing/required_missing/errors rỗng; package hash match=true, hash `0f4d8fbc0a96bb4cbde6a33efc87e78741a52ec634eaadbb215e94d294f8d9e6`. Có doc-pointer/bare-tool advisory. |
| `git diff --check 670071b700bd97a893d64393ffded0257957d0b3 HEAD` | 0 | **passed**: không lỗi whitespace. Manifest chỉ đổi mục CHANGELOG và tổng byte/hash; vẫn 180 tệp. |
| `mutate.py` | 0 | `MUTATION_COMPLETE`: 3 mutant cũ bị assertion ca nền bắt; 4 mutant mới sống (R6-01); mutant `che_do_str` vẫn sống, chưa chứng minh tác hại. Không tính giàn giáo stale của m37/m38 là kill. |
| `sources.py` | 0 | `SOURCES_COMPLETE`: baseline sạch; mỗi literal launcher mất riêng → rc=2; mất surface Web → rc=0/0 chưa đo, phản chứng R6-02. |
| `inspect.py` | 0 | `INSPECTION_COMPLETE`: 7 tên/5 cặp; c28 11 hàng; c32 trace 0+6 lần bơm riêng; receipt R5 khớp schema/Git/hash/bytes/ancestry. |

**failed:** bất biến đầy đủ nguồn ở R6-02 và yêu cầu khóa hồi quy R6-01 bị phản chứng. Không suite nguyên bản nào thất bại. Không gọi “script đo rc=0” là bằng chứng các bất biến ấy passed.

**skipped:** không ca bị bỏ qua trong lease/packet/cong_cu; tầng Git v2 đo được. **not_run:** full runtime selftest, workflow-audit/golden/determinism, release-bundle, Windows/CRLF parity, mọi script lịch sử R1–R4 nguyên vẹn, crash/cleanup/reorder của rig, LIVE/merge/deploy. Không đo mọi mã lỗi Git, kiểu nguồn AST, dạng Markdown hoặc tổ hợp assurance. Hướng cần payload mới về alias/transport/parser giao điều phối, chưa chạy; không tính là pass hay finding P1 đã chứng minh.

**KHÔNG ĐO ĐƯỢC:** trạng thái GitHub trực tiếp từ sandbox không có đường ra mạng: head PR hiện thời, CI/required checks, protection, delivery, authority điều phối. Provenance thực tế của model/session và launcher artifacts lịch sử ngoài clone cũng không đo được. Báo cáo không tự tạo `cross_approved`, approval GitHub hay quyền land; không tự mở thêm vòng review.

Chỉ tạo `VERDICT.md` trong clone, không sửa tệp tracked; HEAD/tree giữ nguyên OID ở đầu báo cáo. Hai P2 và một P3 được giao lại để điều phối quyết định sửa hoặc ghi nợ theo authority.

verdict: approve_with_findings
