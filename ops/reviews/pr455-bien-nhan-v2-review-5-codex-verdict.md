# Cross-review vòng 5 — PR #455

**`approve_with_findings`: hai P2; không có P0/P1 mới được chứng minh.** Tám phản chứng cụ thể của R4-01 đã bị khóa thật. Bản vá phân loại nguồn provider đã sửa trường hợp cũ, nhưng chưa đóng hết lớp nguồn không dùng được; test mới còn bỏ lọt chiều nới danh sách. Không nâng hai lỗi này thành P1 để kéo dài review.

- `reviewed_sha`: `670071b700bd97a893d64393ffded0257957d0b3`
- `reviewed_tree`: `d5358e2ed149a1ad69810aa1f1104e8960cacfd8`
- Diff: `4ef73e69d5f3c419634118983723355e25e38305..670071b700bd97a893d64393ffded0257957d0b3`, 7 tệp.
- Reviewer độc lập với context Executor Claude; axes `spec`, `standards_security`; Review Class `sensitive` vì thay đổi cổng receipt/identity/evidence.
- Provider `openai_codex`; execution surface **Codex service/API với shell trong Linux container**; transport `machine`. Chỉ thị phiên định danh agent GPT-6; không có chứng thực độc lập backend/model version. Không tự nhận là ChatGPT Web hay Codex CLI run được launcher chứng thực.
- Authority: yêu cầu trực tiếp của user giao **vòng 5**, exact head/base, chỉ được ghi `VERDICT.md`. Không được cung cấp Packet revision/spec hash/generation/lease riêng; không tự tạo hoặc xác nhận chúng. Chỉ thị này cho phép review đang giao, không cấp state transition, vòng tiếp theo, approval GitHub hay land authorization.

Preflight tự đo: origin `https://github.com/ducthangho/tra-luat`; detached (`git symbolic-ref -q HEAD`: rc=1, stdout rỗng); full clone (`is-shallow-repository=false`), 1.734 commit; worktree ban đầu sạch. HEAD/tree giữ nguyên sau các phép đo. Đã đọc cả bốn verdict trước, CONTEXT, protocol, CLAUDE và kế hoạch đa provider; kiểm cả bảy tệp trong diff. Không gọi mạng/GitHub. Chỉ tái dùng fixture/phản chứng có sẵn và đột biến mã/nguồn trên bản sao ngoài clone; không soạn payload tấn công mới, không commit/push.

## ĐỐI CHIẾU LƯỢT TRƯỚC

| Finding/chốt | Kết luận và bằng chứng độc lập |
|---|---|
| **R4-01** — tám mutant sống | **ĐÃ VÁ THẬT tám phản chứng cụ thể.** Trích bảng mutant từ script A trong verdict R4; điều chỉnh hai neo MRI/provider theo refactor hiện tại. Cả tám subprocess rc=1 do **assertion ca nền**: c29 bắt CLI trả 0; c17/c34 bắt ép run ID; c28/c31 bắt danh sách chép tay; c32 bắt riêng cả năm phép gỡ `chua`. Không lấy lỗi neo stale của mutant nội bộ làm bằng chứng kill. Độ phủ mới vẫn còn R5-02 bên dưới. |
| **R4-02** — thiếu nguồn bị kết tội receipt | **ĐÃ VÁ THẬT phản chứng thiếu tệp và các hàng c28 hiện có; CHƯA VÁ hết lớp nguồn không dùng được.** Cây đủ nguồn rc=0; thiếu launcher/AGENTS rc=2, 0 vi phạm, 1 chưa đo, không có lời kết tội provider. Suite còn chạy hai ca không có assignment và lỗi cú pháp. Bảng transport rỗng vẫn rc=1/kết tội; UTF-8 hỏng văng khỏi đường phân ba trạng thái: R5-01. |
| **R4-03** — tổng tín dụng sai mẫu số | **ĐÃ VÁ THẬT cách tính/báo cáo hiện tại.** AST: 34 lời gọi `do`, 33 mutant thường, 1 tự kiểm, 16 đối chứng của mutant thường. Hai lượt đọc rows độc lập đều 33/33 + 1/1 + 16/33; khớp stdout. Không còn cộng tự kiểm vào số mutant có răng. Chưa tuyên bố đã khóa bằng mutant mọi phép sửa dòng tổng kết. |
| Connector P1 — ép kiểu attestation | **ĐÃ VÁ THẬT phản chứng đã cung cấp.** c34 chạy 7×4 và c34b nguyên văn đều qua; m28 khôi phục `str` bị c34 giết, m22 bỏ cửa ở run ID bị c17 giết. m30 gỡ yêu cầu `anchor.loai` bị c16 bắt. Đây là kết quả cấu trúc, không chứng minh identity thật. |
| Connector P2 — thiếu provider ngoài CLI | **ĐÃ VÁ THẬT trên từ vựng hiện tại.** Tập có đủ `google_antigravity`, `openai_chatgpt`, `anthropic_claude`; c31 nhận từng provider đọc được. Đột biến quay về một nguồn bị bắt. Chưa chứng minh parser chỉ nhận đúng tên provider trong mọi sửa đổi nguồn: R5-02. |

Ba phép gỡ R3-02 cũng được replay: c24/c25/c26 lần lượt bắt mất trạng thái của protected/check object, mất từ chối non-ancestor, mất trạng thái lỗi merge-base; mỗi subprocess rc=1, 36/37 ca nền.

## R5-01 — P2: nguồn provider có mặt nhưng không dùng được vẫn thoát khỏi hợp đồng ba trạng thái

**Vá ở đâu:** `ops/bien_nhan_v2.py:143–169`, `_provider_chinh_tac`; bổ sung ca trong `ops/bien_nhan_v2_test.py:858`, c28. Đây là phụ thuộc được sửa trong diff, trước khi tạo `PROVIDER_NGUON_HONG` và trước `main`.

**Bằng chứng đã chạy:** script `sources.py` dùng nguyên `_cay_guong`/fixture Git hợp lệ hiện có. Chỉ thay nguồn trên bản sao; receipt không đổi.

| Biến thể nguồn | rc thật | Kết quả |
|---|---:|---|
| Nguyên bản | 0 | 1 đạt, 0 vi phạm, 0 chưa đo, `TỔNG: ĐẠT` |
| Thiếu launcher hoặc AGENTS, mỗi tệp riêng | 2 | 0 vi phạm, 1 chưa đo; đúng hợp đồng |
| Xóa các match nguồn 2 hoặc nguồn 3, mỗi nguồn riêng | 2 | 0 vi phạm, 1 chưa đo; đúng hợp đồng |
| Chỉ thay giá trị AST `_TRANSPORT_CONTRACTS` bằng `()` | **1** | **1 vi phạm, 0 chưa đo**; kết tội `openai_codex` ngoài danh sách, “chuỗi tự do không phải attestation” |
| Thêm byte không giải mã UTF-8 được vào launcher hoặc AGENTS, mỗi tệp riêng | **1** | stdout rỗng; `UnicodeDecodeError` lúc import, không có marker phân loại chưa đo |

Bảng rỗng vẫn có assignment nên `hd is None` không bắt. Trong khi nguồn 2/3 đòi tập không rỗng, nguồn 1 được coi là đã đo với tập rỗng. Hai ca decode lỗi do `read_text` chỉ bắt `OSError`; ngoại lệ xuất hiện trước `main`, nên không tới `KhongDoDuoc`. Không gọi traceback là bằng chứng receipt vi phạm.

**Vì sao P2:** cây nguyên bản đầy đủ vẫn hoạt động; những phép đo này không chứng minh đường cấp approval sai trên dữ liệu hiện hành. Đây là lỗi phân loại/khả dụng khi phụ thuộc hỏng, cùng hình dạng R4-02; không phải P1 chỉ vì nằm trong cổng evidence.

**Vá thế nào:** kiểm tính dùng được của từng nguồn trước khi hợp nhất: bảng transport phải đúng cấu trúc, có dữ liệu provider hợp lệ; lỗi đọc/giải mã/parse phải giữ lý do tới trạng thái thứ ba. Không dùng bảng rỗng hoặc bí danh lịch sử làm fallback giả vờ đã đo. Giữ miễn phép so membership khi nguồn hỏng, đồng thời CLI vẫn rc=2. Không cần viết verifier identity tổng quát để sửa lỗi này.

**Ca test khóa:** tái dùng các biến thể nguồn trong `sources.py`; bảng rỗng và hai ca UTF-8 phải rc=2, có thông báo nguồn cụ thể, 0 vi phạm và không traceback. Đối chứng nguyên bản vẫn rc=0. Sau vá, đột biến bỏ kiểm bảng rỗng và đột biến bỏ bắt lỗi decode phải bị assertion các ca tương ứng giết; không tính import crash là kill nghiệp vụ. Hai chốt sửa mới chưa tồn tại nên mutant gỡ chúng là đề xuất, chưa chạy.

**Bản vá có thể đẻ ra gì:** bắt mọi `Exception` rồi im lặng sẽ che lỗi lập trình; coi mọi thay đổi tập là hỏng sẽ cấm thay đổi provider có chủ ý. Cần phân biệt nguồn rỗng/hỏng với một schema được sửa có thẩm quyền, giữ thông tin lỗi và kiểm từng nguồn riêng. Không biến thiếu nguồn thành cho qua gate hoặc ép sửa receipt đúng.

## R5-02 — P2: test provider mới khóa chiều thiếu, chưa khóa chiều thừa và hai nhánh mất nội dung nguồn

**Vá ở đâu:** `ops/bien_nhan_v2_test.py:858–928`, c28/c31; tương ứng `_provider_chinh_tac` tại `ops/bien_nhan_v2.py:173–179`. `c31` chép cùng biểu thức AST/regex với sản phẩm và chỉ kiểm `ten ⊆ PROVIDER_CHO_PHEP`. Nó không kiểm phần dư; c28 có năm hàng nhưng chưa có hàng mất riêng nội dung regex nguồn 2/3. Câu CHANGELOG dòng 198 “c28 có hàng riêng cho từng đường” rộng hơn các ca thực sự có.

**Bằng chứng đã chạy:** giữ nguyên toàn suite, đột biến từng bản sao độc lập:

| Phép làm yếu sản phẩm | rc / bằng chứng |
|---|---|
| `if not ngoai:` → `if False:` | **0; 37/37 · 33/33 · 1/1 · 16/33** |
| `if not web:` → `if False:` | **0; 37/37 · 33/33 · 1/1 · 16/33** |
| Trước dòng hợp nhất, thêm `hd |= {t.elts[2].value for t in n.value.elts}` | **0; 37/37 · 33/33 · 1/1 · 16/33**; readback tập cho phép có thêm **`claude_code`, `codex_cli`, `llm_cli`**, vốn là execution surface trong tuple, không phải provider |

Đột biến thứ ba thay mã chọn từ vựng, dùng token có sẵn trong AST launcher; không soạn receipt tấn công. Nó giữ nguyên dòng `return hd | ngoai | web, None` để không phá neo m29. Lượt thăm dò đầu thay trực tiếp dòng return làm 37/37 ca nền vẫn qua nhưng m29 báo `gian_giao` do neo stale, rc=1; **không** dùng lần ấy làm bằng chứng suite giết được việc nới danh sách. Bản giữ neo trên mới là phép đo hoàn chỉnh.

Tại exact head nguyên bản, **chưa tìm được regex match nhầm**: launcher chỉ match `openai_api` ở dòng 3625 và `google_antigravity` ở dòng 3628; AGENTS chỉ match `openai_chatgpt` ở dòng 79. Finding này là thiếu khóa hồi quy, không phải tuyên bố ba execution surface đã được allowlist nguyên bản chấp nhận. Hai regex đọc toàn văn tệp, không giới hạn cấu trúc bảng/khối, nên oracle chép cùng regex chưa đủ chứng minh ranh giới đó. Hướng cần soạn nội dung đánh lừa parser được giao lại bằng lời cho điều phối, chưa thực hiện trong vòng này.

**Vá thế nào:** khóa cả tập thiếu lẫn tập thừa với oracle độc lập về vai trò từng cột/trường; tách bí danh lịch sử có khai báo. Với nguồn prose, hướng bền là dữ liệu provider có schema chính tắc; đường sửa nhỏ hơn là giới hạn vị trí đọc vào cấu trúc được chỉ định và test độc lập phần nào là provider. Thêm hai ca xóa riêng nội dung nguồn 2/3 trong khi giữ các nguồn khác nguyên vẹn. Không sửa bằng một danh sách cấm các surface vừa tìm thấy.

**Ca test khóa:** ba mutant trong bảng phải chết ở assertion nghiệp vụ: hai ca mất nội dung nguồn đòi rc=2/0 vi phạm, và ca tập thừa chỉ rõ các tên surface không được phép. Đối chứng đủ các provider chính tắc và hai bí danh vẫn qua. Script `sources.py` đã đo nguyên bản khi mất từng nội dung nguồn là rc=2; `probe.py`/`rig.py` đã đo ba mutant còn sống. Khi điều phối cung cấp fixture prose ngoài bảng/khối, cần thêm đối chứng parser không lấy tên ở đó; tôi chưa viết/chạy fixture nhạy cảm ấy.

**Bản vá có thể đẻ ra gì:** đóng băng bảy tên trong mọi nơi sẽ tái tạo danh sách chép tay và cản thêm provider hợp lệ; một oracle dùng chung extractor với sản phẩm sẽ tiếp tục cùng sai. Parity chỉ chứng minh bản sao giống module đang kiểm, không chứng minh module đúng hợp đồng. Hai cây gương cần tiếp tục mang đúng nguồn của ca đo khi thêm registry/schema mới.

## Kiểm bốn vùng mỏng và lời khai định lượng

**`_chuoi`:** trên đường CLI, các `str` còn lại cho `evidence_url`, `reviewed_sha`, `verdict_sha256` được chặn kiểu trước: `_co_chuoi`/`_khop`; `_neo_git` chỉ chạy khi `_thieu` rỗng. Không chứng minh được bypass mới bằng các fixture được phép dùng. Phục hồi riêng ép `str` tại `che_do` vẫn cho suite xanh; chưa có bằng chứng nó là phép làm yếu gây nhận sai nên không biến mutant sống đó thành P1/finding sản phẩm. Bộ 7×4 không được đọc thành toàn bộ schema tùy chọn đã được chứng minh đầy đủ.

**Provider:** đo được bảy tên `anthropic`, `anthropic_claude`, `google_antigravity`, `human`, `openai_api`, `openai_chatgpt`, `openai_codex`. **Sửa lời khai “không tên nào chép tay”:** năm tên phân biệt đến từ ba nguồn đọc; `anthropic` và `human` được chép tường minh trong `PROVIDER_LICH_SU` dòng 185. Bí danh có giải thích trong mã, không phải phát hiện một allowlist ngầm mới. Nên báo “ba nguồn chính tắc + hai bí danh lịch sử”, không báo cả bảy đều được đọc từ nguồn.

**c32:** trace thực thi cho sáu lần `kiem` có số thao tác bị bơm lần lượt **0,1,1,1,1,1**. Đối chứng đầu có `loi=[]`, `chua_do=[]`. Năm lượt sau đều `loi=[]` và đúng một `chua_do`: reviewed SHA rc=127; commit evidence URL không tra được; `rev-parse --verify HEAD`; blob rc=3; blob ném OSError. Hai SHA khác nhau thật. Không có bằng chứng mock đang giết cả cụm trên fixture này. Ca hiện chưa tự assert số match; không suy trace một fixture thành tính đúng của matcher cho mọi tương lai.

**Hai cây gương:** mã cổng trong `_cay_guong` lấy từ `bnv2.__file__` đang hiệu lực; `_dot_bien_tep` dựng module từ nguồn nền, có cả launcher và AGENTS. Hai lượt runner liên tiếp đều 33/33 + 1/1; module/CONG phục hồi, danh sách tạm rỗng; sau đó chạy ngược CA được 37/37 `qua`. Chưa tìm được lệch cây gương mới gây sai kết luận trong các mutant hiện hành. **Phạm vi parity bốn hằng vẫn chỉ là parity**, như mutant mở rộng provider sống chứng minh: cả cây thật đang đột biến và cây gương cùng sai thì parity vẫn xanh. Không đo Windows/CRLF, crash/cleanup hoặc mọi phụ thuộc có thể thêm sau này trong vòng này.

**Biên nhận R4 tự qua:** không thuộc miễn trừ/nợ; `_thieu=[]`, `_neo_git=([],[])`. Commit neo đầy đủ **`c34832a58bc4e4a2b23d67eb2d6d3df96814ab9e`**: `git show <sha>:ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.md` rc=0; blob khớp byte tệp local và khớp digest **`3708d03a1fd871ac143f74eaacd13fdf943fe5c3e0704b77a23640b13addda1c`**. `git merge-base --is-ancestor <sha> HEAD` rc=0. Đây là ancestry tới HEAD local; không chứng minh authority/ref protection hay lời khai launcher ngoài clone.

## Bằng chứng tái lập

Ba script bên dưới đã chạy từ root clone bằng `PYTHONDONTWRITEBYTECODE=1 python3 /tmp/pr455-r5-evidence/<tên>.py`, đều rc=0 với marker hoàn tất. Tạo trước thư mục log `/tmp/pr455-r5-evidence`. Các subprocess mutant có rc riêng được ghi ở trên; rc=0 của script đo không có nghĩa mọi mutant đã chết. Script giữ phép đo tái lập khi log tạm mất. Chỉ script/fixture và cây sao trong `/tmp` được ghi; `.git` trỏ về kho gốc trong các cây sao chỉ phục vụ truy vấn đọc.

### probe.py

```python
import os,sys,subprocess,tempfile,shutil,ast,json,concurrent.futures
from pathlib import Path
R=Path.cwd(); E=Path('/tmp/pr455-r5-evidence'); S=(R/'ops/bien_nhan_v2.py').read_text()
env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'}
old=(R/'ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.md').read_text().split('### A — probe.py')[1].split('```python\n')[1].split('```')[0]
a=next(n for n in ast.parse(old).body if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='mut');mut=ast.literal_eval(a.value)
mut['mri_rid_str_coercion']=('    rid = _chuoi(v.get("session_run_id"))','    rid = str(v.get("session_run_id") or "").strip()')
mut['provider_back_to_handcopy']=('PROVIDER_CHINH_TAC, PROVIDER_NGUON_HONG = _provider_chinh_tac()', 'PROVIDER_CHINH_TAC, PROVIDER_NGUON_HONG = ({"anthropic", "openai_codex", "openai_api", "google_antigravity", "human"}, None)')
mut.update({
 'provider_widen_to_surfaces':('return hd | ngoai | web, None','return hd | ngoai | web | {t.elts[2].value for t in n.value.elts}, None'),
 'drop_source2_empty_guard':('if not ngoai:', 'if False:'),
 'drop_source3_empty_guard':('if not web:', 'if False:'),
 'che_do_back_to_str':('"subagent" in (_chuoi(mri.get("che_do")) or "").lower()', '"subagent" in str(mri.get("che_do") or "").lower()'),
})
def run(item):
 label,(a,b)=item; assert S.count(a)==1,(label,S.count(a))
 with tempfile.TemporaryDirectory(prefix='r5-mut-') as td:
  r=Path(td);shutil.copytree(R/'ops',r/'ops',ignore=shutil.ignore_patterns('__pycache__'));(r/'.claude/dev').mkdir(parents=True);shutil.copyfile(R/'.claude/dev/launcher.py',r/'.claude/dev/launcher.py');shutil.copyfile(R/'AGENTS.md',r/'AGENTS.md');(r/'.git').write_text('gitdir: '+str(R/'.git')+'\n');(r/'ops/bien_nhan_v2.py').write_text(S.replace(a,b))
  q=subprocess.run([sys.executable,str(r/'ops/bien_nhan_v2_test.py')],cwd=r,env=env,capture_output=True,text=True)
  (E/(label+'.log')).write_text(q.stdout+q.stderr)
  return {'label':label,'rc':q.returncode,'summary':q.stdout.splitlines()[-2:],'failures':[l for l in q.stdout.splitlines() if l.startswith(('  ĐỎ','  KHÔNG ĐO','  KHÔNG RĂNG'))]}
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:
 for out in ex.map(run,mut.items()):print(json.dumps(out,ensure_ascii=False),flush=True)
print('MATRIX_COMPLETE')
```

### sources.py

```python
import importlib.util,sys,tempfile,subprocess,ast,re,json,hashlib
from pathlib import Path
R=Path.cwd();sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('t',R/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
l=(R/'.claude/dev/launcher.py').read_text(); a=(R/'AGENTS.md').read_text();node=next(n for n in ast.walk(ast.parse(l)) if isinstance(n,ast.Assign) and getattr(n.targets[0],'id','')=='_TRANSPORT_CONTRACTS');value=ast.get_source_segment(l,node.value)
print('CONTRACT',ast.literal_eval(node.value))
for source,pat,content in [('launcher',r'provider\s+([a-z0-9_]+)\s+qua\s+execution_surface',l),('AGENTS',r'(?m)^provider:\s*([a-z0-9_]+)\s*$',a)]:
 print('MATCHES',source,[(content[:m.start()].count('\n')+1,m.group()) for m in re.finditer(pat,content)])
print('PROVIDERS',sorted(t.bnv2.PROVIDER_CHO_PHEP),'error',t.bnv2.PROVIDER_NGUON_HONG,'historical',sorted(t.bnv2.PROVIDER_LICH_SU))
variants=['baseline','missing_launcher','missing_agents','empty_contract','empty_source2','empty_source3','bad_utf8_launcher','bad_utf8_agents']
for label in variants:
 with tempfile.TemporaryDirectory(prefix='r5-source-') as td:
  r=Path(td);p=t._cay_guong(r);lp=r/'.claude/dev/launcher.py';ap=r/'AGENTS.md'
  if label=='missing_launcher':lp.unlink()
  if label=='missing_agents':ap.unlink()
  if label=='empty_contract':lp.write_text(l.replace(value,'()'))
  if label=='empty_source2':lp.write_text(re.sub(r'provider\s+([a-z0-9_]+)\s+qua\s+execution_surface','',l))
  if label=='empty_source3':ap.write_text(re.sub(r'(?m)^provider:\s*([a-z0-9_]+)\s*$','',a))
  if label=='bad_utf8_launcher':lp.write_bytes(lp.read_bytes()+b'\xff')
  if label=='bad_utf8_agents':ap.write_bytes(ap.read_bytes()+b'\xff')
  q=subprocess.run([sys.executable,str(p),'--root',str(r)],capture_output=True,text=True)
  print('SOURCE',label,json.dumps({'rc':q.returncode,'stdout':q.stdout,'stderr':q.stderr[-1500:]},ensure_ascii=False))
import yaml
p=R/'ops/reviews/pr455-bien-nhan-v2-review-4-codex-verdict.receipt.yaml';d=yaml.safe_load(p.read_text());sha,path=d['evidence_url'].split('/blob/')[1].split('/',1)
q=subprocess.run(['git','show',sha+':'+path],capture_output=True);anc=subprocess.run(['git','merge-base','--is-ancestor',sha,'HEAD'])
print('RECEIPT',{'sha':sha,'schema':t.bnv2._thieu(d),'git':t.bnv2._neo_git(R,p.name,d),'exempt':p.name in t.bnv2.ALLOWLIST_CUTOVER,'debt':p.name in t.bnv2.NO_DA_DO,'blob_rc':q.returncode,'ancestry_rc':anc.returncode,'hash':hashlib.sha256(q.stdout).hexdigest(),'hash_match':hashlib.sha256(q.stdout).hexdigest()==d['verdict_sha256'],'local_match':q.stdout==(R/path).read_bytes()})
print('SOURCES_COMPLETE')
```

### rig.py

```python
import importlib.util,sys,json,ast,contextlib,io,subprocess,tempfile,shutil,os
from pathlib import Path
R=Path.cwd();sys.dont_write_bytecode=True
s=importlib.util.spec_from_file_location('t',R/'ops/bien_nhan_v2_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
phases=[];current=None;original=t.bnv2.kiem
def measured(*args,**kw):
 global current
 current={'injected':[]};phases.append(current)
 result=original(*args,**kw);current['errors']=result[0];current['unknown']=result[1].get('chua_do');return result
def trace(frame,event,arg):
 if event=='call' and frame.f_code.co_filename==str(R/'ops/bien_nhan_v2_test.py'):
  loc=frame.f_locals
  if frame.f_code.co_name=='_bom' and 'khop' in loc and loc['khop'](loc['args']):current['injected'].append(list(loc['args']))
  if frame.f_code.co_name=='run' and '_Shim' in type(loc.get('self')).__name__:
   cmd=loc['cmd']
   if isinstance(cmd,list) and 'cat-file' in cmd and '-p' in cmd:current['injected'].append(cmd)
 return trace
t.bnv2.kiem=measured;sys.settrace(trace)
try:result=t._chay_1(t.c32_MOI_thao_tac_git_HONG_deu_phai_vao_KHONG_DO_DUOC)
finally:sys.settrace(None);t.bnv2.kiem=original
print('C32',result,json.dumps(phases,ensure_ascii=False));assert result[0]=='qua';assert [len(x['injected']) for x in phases]==[0,1,1,1,1,1]
# Run the current runner twice; inspect flags and restored state.
orig=t.bnv2;cong=t.CONG
for i in range(2):
 with contextlib.redirect_stdout(io.StringIO()):rows=t._dot_bien()
 print('ROWS',i,{'normal':sum(not r[5] for r in rows),'normal_killed':sum(r[2] and not r[5] for r in rows),'self':sum(r[5] for r in rows),'self_ok':sum(r[2] and r[5] for r in rows),'controls':sum(r[6] and not r[5] for r in rows),'restored':t.bnv2 is orig and t.CONG==cong,'temps':t._TAM_DOT_BIEN})
print('REVERSE',[(f.__name__,t._chay_1(f)[0]) for f in reversed(t.CA)])
# Product mutation broadens provider extraction with surface tokens already in its AST.
S=(R/'ops/bien_nhan_v2.py').read_text();a='    return hd | ngoai | web, None';b='    hd |= {t.elts[2].value for t in n.value.elts}\n'+a
with tempfile.TemporaryDirectory(prefix='r5-widen-') as td:
 r=Path(td);shutil.copytree(R/'ops',r/'ops',ignore=shutil.ignore_patterns('__pycache__'));(r/'.claude/dev').mkdir(parents=True);shutil.copyfile(R/'.claude/dev/launcher.py',r/'.claude/dev/launcher.py');shutil.copyfile(R/'AGENTS.md',r/'AGENTS.md');(r/'.git').write_text('gitdir: '+str(R/'.git')+'\n');assert S.count(a)==1;(r/'ops/bien_nhan_v2.py').write_text(S.replace(a,b))
 q=subprocess.run([sys.executable,str(r/'ops/bien_nhan_v2_test.py')],cwd=r,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'},capture_output=True,text=True)
 Path('/tmp/pr455-r5-evidence/widen_preserve.log').write_text(q.stdout+q.stderr)
 print('WIDEN_PRESERVE_ANCHOR',q.returncode,q.stdout.splitlines()[-2:])
 s=importlib.util.spec_from_file_location('w',r/'ops/bien_nhan_v2.py');m=importlib.util.module_from_spec(s);s.loader.exec_module(m);print('ADDED_NAMES',sorted(m.PROVIDER_CHO_PHEP-orig.PROVIDER_CHO_PHEP))
print('RIG_COMPLETE')
```

## TÔI ĐÃ ĐO ĐƯỢC GÌ / KHÔNG ĐO ĐƯỢC GÌ

Môi trường: Linux container, Python 3.11.15, Git 2.43.0, PyYAML có sẵn, `core.abbrev=7` có sẵn. Không sửa Git config. Python dùng `PYTHONDONTWRITEBYTECODE=1`; mã thoát lấy từ công cụ tiến trình hoặc `subprocess.returncode`.

| Command/phép đo | rc thật | Trạng thái và bằng chứng dương |
|---|---:|---|
| `python3 ops/bien_nhan_v2_test.py` | 0 | **passed theo suite**: 37/37 ca, 33/33 mutant thường, 1/1 tự kiểm, 16/33 khai đối chứng; tầng Git cutover khớp 11 tệp. Giới hạn độ phủ ở R5-02. |
| `python3 ops/bien_nhan_v2.py --root .` | 0 | **passed**: 13 đạt v2 · 11/11 miễn trừ băm khớp · 42 nợ · 0 vi phạm · 0 chưa đo · tổng 66, `TỔNG: ĐẠT`. |
| `python3 ops/lease_publish_test.py` | 0 | **passed**: 121/121; đã chạy 121, bỏ qua 0. Warning empty repository thuộc fixture. |
| `python3 .claude/dev/packet_loop_test.py` | 0 | **passed**: 278/278, bỏ qua 0; 81 mutant, 78 lớp lách, 35 ca bắt-oan, 0 ngoại lệ AC18; `TỔNG: ĐẠT`. |
| `python3 ops/cong_cu_test.py` | 0 | **passed**: 23/23, bỏ qua 0; 18 mutant, lỗi mutant 0; 7 ca tự kiểm bộ phân hạng. |
| `python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` | 0 | **passed**: `ok=true`, checked=expected=180; failed/extra/missing/required_missing/errors rỗng; package hash khớp `6a55695909dd015810762f0f87f2703e7a70e2950077b22734414e6158a62e46`. Có doc-pointer/bare-tool advisory. |
| `git diff --check 4ef73e69d5f3c419634118983723355e25e38305 HEAD` | 0 | **passed**: không lỗi whitespace; manifest chỉ đổi mục CHANGELOG và tổng byte/hash, file_count vẫn 180. |
| `probe.py` | 0 | **phép đo hoàn tất**, `MATRIX_COMPLETE`: 11 phép gỡ cũ đều bị ca nền bắt; hai guard nguồn mới gỡ được mà toàn suite vẫn xanh. Một lượt mở rộng provider chỉ làm stale neo m29; không tính là kill nghiệp vụ. Mutant `che_do` sống nhưng chưa chứng minh tác hại. |
| `sources.py` | 0 | **phép đo hoàn tất**, `SOURCES_COMPLETE`: control sạch; thiếu tệp/mất nội dung nguồn 2/3 được phân loại đúng; bảng nguồn 1 rỗng và hai lỗi decode tái hiện R5-01. Receipt R4 khớp schema/Git/bytes/hash/ancestry. |
| `rig.py` | 0 | **phép đo hoàn tất**, `RIG_COMPLETE`: c32 đúng 5 lần bơm riêng; hai lượt rows/restore khớp; 37/37 ca đảo thứ tự qua; mutant nới provider giữ neo còn sống, **rc=0** và toàn bộ tổng kết xanh. |

**failed:** các bất biến/phạm vi đo trong R5-01/R5-02 bị phản chứng. Không có suite nguyên bản nào thất bại. Lỗi import trên bản sao hỏng UTF-8 là kết quả phép bơm lỗi, không phải lỗi tự phát trên checkout nguyên bản. **skipped:** không ca bị bỏ qua trong lease/packet_loop/cong_cu; tầng Git của v2 đo được. Không đổi `not_run` thành passed.

**not_run:** full runtime selftest, workflow-audit/golden/determinism, release-bundle, Windows/CRLF parity, các phép crash/cleanup của R4, remote CI readback, LIVE/merge/deploy. Không tái chạy nguyên mọi script R1–R3; đã đọc chúng và chạy lại các nhánh cũ được nêu cụ thể cùng suite hiện tại. Chưa đo mọi kiểu dữ liệu tùy chọn, mọi lỗi I/O hoặc mọi nội dung có thể đánh lừa regex. Các hướng cần soạn nội dung nhạy cảm chỉ mô tả để điều phối chuẩn bị, không tự viết trong phiên này.

**KHÔNG ĐO ĐƯỢC:** trạng thái GitHub trực tiếp từ sandbox không có đường ra mạng — head PR hiện thời, required checks/CI, protection, delivery, authority điều phối; provenance thực tế của model/session và launcher artifacts lịch sử ngoài clone. Không coi lời khai trong receipt là chứng thực độc lập những việc đó. Báo cáo không tự tạo `cross_approved`, approval GitHub hay quyền land.

Chỉ tạo `VERDICT.md` trong clone; HEAD/tree giữ nguyên OID ở đầu báo cáo. Hai P2 được giao lại để điều phối quyết định sửa hoặc ghi nợ đúng authority; không tự mở thêm vòng review.

verdict: approve_with_findings
