from pathlib import Path
import ast,json,collections,hashlib,subprocess
R=Path(__file__).resolve().parent;root=R.parent
def read(p):return json.loads((R/p).read_text())
def need(p,n=None):
 v=read(p)
 if n is not None:assert len(v)==n,(p,len(v),n)
 return v
rows=need('frontier6/results.json',sum(isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id=='add' for n in ast.walk(ast.parse((R/'frontier6.py').read_text()))))
extra=need('frontier6-extra/results.json',1)+need('frontier6-extra2/results.json',1)+need('frontier6-extra3/results.json',1)
new=rows+extra
cat=need('mutants/results.json',233);assert sum(x['rank']=='GIET' for x in cat)==231
assert {x['rank'] for x in cat if x['expected']=='GIET'}=={'GIET'}
assert all(x['rank']==x['expected'] for x in cat)
assert read('suite.json')['returncode']==0
assert 'CA: 49/49 dat' in (R/'suite.stdout.txt').read_text() and 'DOT BIEN: 231/231 bi giet dung ly do' in (R/'suite.stdout.txt').read_text()
assert read('operators6-fixed.json')['returncode']==0
assert read('after-suite6-run.json')['returncode']==0
frontier5=need('frontier5/results.json',46)
ops=need('operators6-combined.json',130)
assert all(x['killed'] for x in ops)
hist=need('historical-targets6/results.json');norm=need('normalization6-results.json')
proofs={z['name']:z for z in read('proof-all6-results.json')}
for p in R.glob('proof6-*.json'):
 try:z=json.loads(p.read_text())
 except ValueError:continue
 if type(z) is list:
  for v in z:
   if v.get('proven'):proofs[v['name']]=v
for z in read('proof-final6-results.json'):proofs[z['name']]=z
p3={'env_only_keys_str':'Tương đương trên miền yaml.safe_load: các khoá scalar không phải str không thể có tiền tố CI_DANG_KY_; không cần cố giết. Ngoài miền YAML an toàn chưa được đặc tả.'}
surv=[x for x in new if x['rank']=='SONG_SOT']
p1=[x for x in surv if x['name'] not in p3]
for x in p1:assert x['name'] in proofs and proofs[x['name']]['proven'],('unproven',x['name'])
assert all(x['rc']==0 for x in read('legacy-after-suite6-results.json'))
for n in (1,2):
 z=read(f'prior{n}/old-cases-results.json');assert len([x for x in z if 'case' in x])==12 and all(x['rc']==0 for x in z),z
 z=read(f'prior{n}/registry-details.json');assert not z['normal'][0] and z['removed'][0] and z['accepts_suite'] and all(z['rejects_bad'].values()),z
rt=read('runtime6.json')[0]
id=rt['session_meta']['id'];ctx=rt['turn_context']
head=subprocess.run(['git','rev-parse','HEAD'],capture_output=True,check=True).stdout.decode().strip();tree=subprocess.run(['git','rev-parse','HEAD^{tree}'],capture_output=True,check=True).stdout.decode().strip()
assert head=='35453ff30170998ffea663801299db5876cc8e0c'
summary=[]
for label,a in [('catalogue',cat),('historical-targets6',hist),('frontier5',frontier5),('operators6',ops),('normalization6',norm),('frontier6 mới',new)]:summary.append(f'| {label} | {dict(collections.Counter(x["rank"] for x in a))} |')
texts=[]
texts.append(f'''verdict: changes_requested
reviewed_sha: {head}
base_sha: ba222ffd1615f0d74b59985b9612f725211b62f5
Reviewed commit: {head}
reviewed_tree: {tree}
packet: wp899-r4
review_round: 6
role: reviewer
provider: openai_codex
model_family: openai
model: {ctx['model']} (CLI-published)
effort: {ctx['effort']} (CLI-published)
session_id: {id}
execution_surface: codex_cli
transport: machine
github_submitter_identity: null
independent_from_executor_session: true
review_axes: [spec, standards_security]
assurance: review_deferred

**Chưa đạt V2: P0=0, P1=1, P2=0 theo lớp. F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` LẶP, chưa đóng cả lớp.** D01 đã vá thật theo quyết định chủ kho. Các biểu hiện định nghĩa được của lượt 5 đã có răng trong bộ ca hiện tại, nhưng {len(p1)} mutant mới vẫn qua toàn bộ 49 ca và đổi kết quả được đặc tả định nghĩa. Mỗi mutant P1 có đối chứng HEAD rc0 → mutant rc3 bởi `TinHieuChotCa` đúng tên. Không suy lỗi của mutant thành lỗi mã sản phẩm hiện tại.

**Authority và preflight.** Đọc assignment `.review-input/prompt.md`, trọn spec r4 và các mục r2/r3 được kế thừa, skill `cross-review`, protocol và hướng dẫn repository. SHA-256 spec r4 `be1e1feabe7c23b832168e36b0cce333043863af505e65c48d5a22d2101cef45` (23.860 byte), r3 `dd1a997d1f3682e23bb4b5577264076b7d9a12aeff5d9823f491cdda05e4f36f`, r2 `d858c7c65a38a7f0fadda1cabf839c98ce70a881372d847c8979165925971707`, đều khớp. Nguồn authority offline là bản đóng băng được user chỉ định; không tự coi local copy/branch name là xác minh GitHub.

Origin `https://github.com/ducthangho/tra-luat.git`; detached HEAD/tree đúng đầu verdict. Parent `22da28c738e651361274c1264e681a52461dad1e`; baseline bất biến `ba222ffd1615f0d74b59985b9612f725211b62f5` là ancestor (rc0). `full.patch` và `delta.patch` giữ raw bytes. Numstat ba tệp: registry +1, sản phẩm +444, test +1204 = **1649 dòng thêm**; registry chỉ thêm đúng một mục MOI. Delta lượt này: sản phẩm +3/−3; test +154/−10. `git diff --check <base> HEAD` rc0; `core.abbrev=7` có sẵn; clone shallow. Chỉ `.review/` được ghi theo assignment.

Áp Q1–Q12, quyết định nâng trần/tiếp tục sau checkpoint issuecomment-6393643859, cùng quyết định phân hạng và D01 ở issuecomment-6394979394 như assignment yêu cầu. Không coi 1649>1250 hay V5 cũ là finding. Đây là lời gọi 6/8 theo assignment; còn 2, gồm một connector sau lần đẩy. Generation/lease/state/ref fence GitHub, chi thực tế và các quyết định ngoài bundle **KHÔNG ĐO ĐƯỢC offline**. Không push, đăng GitHub, gọi subagent, merge, land, deploy, LIVE hay mạng.

Gốc tin giữ nguyên: nội dung workflow/script/action tại SHA checkout, kể cả action pin tag. Phản chứng mới chỉ là dữ liệu hợp đồng vô hại; không yêu cầu quyền sửa cây checkout và không tự soạn nội dung tấn công nhạy cảm.

**Môi trường và nhận dạng.** Linux x86_64; Python3.13.17, PyYAML6.0.3, Git2.43.0, Ruff0.15.15, codex-cli0.164.0. `runtime6.json` đọc đúng cwd/thread từ `{rt['path']}`. Model/effort trên là CLI công bố; model phục vụ từng request **KHÔNG ĐO ĐƯỢC**. Executor Claude/cloud theo assignment, không suy identity từ tài khoản vận chuyển. Rollout và launcher receipt chỉ đóng băng được sau khi tiến trình review kết thúc; A13 chưa hoàn tất và verdict này không tự tạo `cross_approved`. Sandbox workspace-write, network=false, approval=never, `.git` read-only; không khai sandbox là read-only toàn bộ.

**BẢNG LỚP.** Một lớp P1 lặp; không có lớp P0–P2 mới. Điểm lỗi nằm ở độ phủ test, không phải một bản vá sản phẩm được yêu cầu.

| lớp | hạng | biểu hiện (tệp:dòng) | phép đo tái hiện | HINT patch | ước lượng dòng |
|---|---|---|---|---|---|
| F10 — miền tên job và tính duy nhất | P1 | `ops/ci_provenance_test.py:763`, `:794`, `:846`; alias của c49 dài tối đa7, tên REST đều ASCII. Chốt sản phẩm `ops/ci_provenance.py:165`. | `job_ascii_suffix`, `job_alias_truncate`, `job_nested_suffix_pure`; xem từng mutant còn sống và `proof-final6-results.json`. | **Ở đâu:** c39/c48/c49 + DOT_BIEN, vì phải kiểm việc ghép đúng job trước marker. **Cách:** thêm miền Unicode, alias dài và hậu tố lồng, kiểm nguyên văn và ghép duy nhất; thêm đối chứng prefix gần đúng phải bị từ chối. **Khoá:** từng mutant trên chết đúng ca. **Rủi ro:** tên REST vô tình trỏ job khác/ghép hỏng vế a sẽ che chốt; giữ REST/YAML/log độc lập và kiểm vế d. | ~10–20 |
| F10 — hình dạng/miền REST và tên bước | P1 | `ops/ci_provenance_test.py:608`, `:629`, `:802`, `:807`; skipped luôn có giờ hợp lệ trong c49, metadata luôn bắt đầu number1; một số giá trị render thành chuỗi chưa có cặp phân biệt. Chốt `ops/ci_provenance.py:171`, `:185`. | Các mutant REST/number/name trong bảng dưới. Phản chứng kiểm cả `ghep_buoc` và danh sách marker, không chỉ Gate chung. | **Ở đâu:** c44/c45/c49 + DOT_BIEN. **Cách:** quan hệ số dương duy nhất có thể dịch/gap/lớn; mảng rỗng hai phía; skipped thiếu giờ; tên REST literal so với name YAML không hợp lệ. **Khoá:** mutant áp ràng buộc số đầu=1 hoặc đòi giờ skipped phải chết; ca rỗng kiểm đầu ra M12 dù Gate tổng vẫn thiếu metadata. **Rủi ro:** helper tự bù metadata hoặc đổi kiểu JSON làm ca không tới chốt. | ~15–25 |
| F10 — cửa sổ thời gian | P1 | `ops/ci_provenance_test.py:549`, `:818`, `:828`; bộ sinh chỉ dùng cửa sổ rất hẹp quanh cùng giây, thiếu một số quan hệ biên lịch/cửa sổ. Chốt `ops/ci_provenance.py:178`, `:205`. | Các mutant time còn sống; HEAD giữ đúng kết quả, mutant đổi kết quả bằng ca riêng. | **Ở đâu:** c38/c49 + DOT_BIEN. **Cách:** cửa sổ qua ngày/năm và các ngày hợp lệ/không hợp lệ ở cả header lẫn REST; oracle so timestamp hợp lệ rồi so quan hệ thời gian. **Khoá:** mutant siết cùng ngày/miền năm hoặc nhận ngày không tồn tại phải chết đúng ca. **Rủi ro:** header và REST sai cùng lúc chỉ đo số nhóm, không đo lịch; kiểm ghép và marker sau khi giữ các vế khác đúng. | ~10–18 |
| F10 — nguồn chặn và cấu trúc/đầu ra log | P1 | `ops/ci_provenance_test.py:763`, `:818`; mỗi run sinh một dòng output, thiếu nhiều biến thể metadata không màu và nguồn `uses:`/name so với `run:`. Chốt `ops/ci_provenance.py:211`, `:253`, `:288`. | Các mutant prior/log/run còn sống trong bảng dưới. | **Ở đâu:** c42/c47–c49 + DOT_BIEN. **Cách:** biến đổi riêng dòng metadata/ANSI/output trước-sau marker, vị trí dòng trống và run/uses/name của bước trước. Giữ khối in lại xác thực và ghép passed, so trọn marker/path/reason cùng số bước xác thực. **Khoá:** mutant quét cả bước thay cho run hoặc chỉ đọc đầu/cuối/trim output phải chết đúng ca. **Rủi ro:** nhầm marker với khối in lại hoặc fail ghép trước sẽ tạo răng giả; đòi đối chứng dương đi tới đúng bước. | ~20–35 |

Cách vá chung rẻ nhất: thêm các phân hoạch bắt buộc vào bảng/oracle hiện có, giữ bộ sinh c49 để hoán vị vị trí, và assert mỗi phân hoạch thực sự được lấy mẫu. Không cần thêm dependency hoặc sửa sản phẩm đang đúng. Một bộ sinh tổng quát hơn mua thêm miền dữ liệu, nhưng phải có oracle độc lập và không được dùng tính ngẫu nhiên làm chứng minh bao phủ. Script/fixture trong `.review/` là dữ liệu phản chứng; executor tự tái dẫn xuất, tự đo và tự commit.

**ĐỐI CHIẾU F01–F11 và D01.** Nguồn gần nhất là lượt5 trên parent; lịch sử không bị reset bởi revision/nâng trần.

| lớp | kết quả trên HEAD | bằng chứng độc lập và giới hạn |
|---|---|---|
| F01 `thieu-dinh-danh-van-passed` | GIỮ ĐÓNG trong tập đo | c22, probes thiếu/kiểu và catalogue mutant đúng ca; phân biệt Gate thiếu metadata với ghép bước. |
| F02 `nhac-ten-script-thanh-thuc-thi` | GIỮ ĐÓNG các phản chứng được giao | Chạy lại probes, r2-compare, reviewer cases r3, boundary/composite với REST r4 hợp lệ; composite dùng stdout suite thật sau khi suite kết thúc; c23/c25–27/c35/c40–43. Không vượt giới hạn gốc tin để gọi một thay đổi workflow được tin là exploit. |
| F03 `phan-trang-dem-thay-vi-chung-minh-du` | GIỮ ĐÓNG | c20, thiếu/lặp/total đổi cho jobs/artifacts, các mutant đích. |
| F04 `rest-gia-khong-neo-run` | GIỮ ĐÓNG | URL run/attempt/log sai ra404; mutant jobs/artifacts run+1 chết c20. |
| F05 `duong-loi-bo-dong-dem-bat-buoc` | GIỮ ĐÓNG phạm vi đo | c01/c18/c19/c22, HTTP403/shape/I/O/lưới cuối; command/rc/output được lưu. Không khẳng định mọi lỗi đã thử. |
| F06 `redirect-loi-thoat-ngoai-bo-boc` | GIỮ ĐÓNG | c24, mock redirect/network/token và mutant; không đo endpoint thật. |
| F07 `a10-doi-sha-khi-checkout-skipped` | GIỮ ĐÓNG bằng authority | Replay13+1 và22+1, không gán SHA cho chuan-bi bằng REST head. |
| F08 `nguon-workflow-git-khong-duoc-kiem-thu` | GIỮ ĐÓNG | c34 dùng Git/tree thật, thiếu path/nonUTF8, mutant reader và git_workflow_source cũ; không suy objects ngoài shallow clone. |
| F09 `thoi-diem-khong-hop-le-van-ghep` | GIỮ ĐÓNG sản phẩm trong tập đo | c38, calendar/finish probes, leap/century/min–max year/offset/fullmatch/header thiếu, mutant bỏ guard/calendar. Các thiếu răng miền bổ sung thuộc F10. |
| F10 `fixture-dinh-danh-buoc-chi-giu-dang-khop` | ĐÃ VÁ THẬT các biểu hiện định nghĩa được lượt5; CHƯA ĐÓNG CẢ LỚP | c48 bổ sung nối dòng + khoảng trắng, màu thiếu reset, LF cuối và uses có khoảng trắng; c49 khóa nhiều trục env/vị trí/định danh. Tuy nhiên còn mutant sống được nêu dưới, có phản chứng riêng. |
| F11 `chan-path-chua-co-phan-chung` | GIỮ ĐÓNG | c42 ENV/PATH trước/khác job/sau; bỏ riêng PATH chết đúng ca. Miền nguồn/vị trí mới vẫn theo F10. |
| D01 `mien-env-null-chua-chot` | ĐÃ VÁ THẬT theo quyết định chủ kho | `_env_chan` phân biệt key vắng với null; c46 hai scope + mutant gộp null/vắng bị giết đúng ca. Replay workflow lịch sử không có null env, provenance không đổi. |

U lượt5={{F10}}, F={{}}: **0/1 lớp cũ đóng toàn bộ**, 0 lớp P0–P2 mới. D01 là quyết định miền đã giải quyết và được đo, không phải P3 mới.

**A1–A27.** Tổng suite xanh không thay tiêu chí độ phủ M11.

| tiêu chí | trạng thái/phạm vi |
|---|---|
| A1 | passed c01: help đủ cờ, sai đối số rc2 + dòng đếm; mutant đúng ca. |
| A2 | passed c02: lệch attempt Run failed/rc12; mutant đúng ca. |
| A3 | passed c03–09 + mutant SHA/Linux/Windows/PR. Fixture Windows không chứng minh native Windows execution. |
| A4 | passed các vế c10–15: runner0, skipped, regex đúng bước, MOI import, job failure; mutant đúng ca. |
| A5 | passed c16: Workflow definition luôn not_measured, path chỉ là lời khai. |
| A6 | passed c17: ghi nguyên tử và fault injection; mutant đúng ca. |
| A7 | passed c18/c19 và receipt target: rc0/NOT_MEASURED1; HTTP403/rc3; mutant bỏ đếm/gộp rc12 bị bắt đúng ca. |
| A8 | Suite49/49,231/231,2 tự kiểm, TONG DAT; nghĩa vụ độ phủ M11 CHƯA ĐẠT do F10. |
| A9 | Kiểm đăng ký, negative bỏ mục MOI, regex và pin/probe đã đo; full `--chay` **not_run** theo chỉ thị chưa chạy gate nặng. Fixture signer bị sandbox từ chối giữ not_measured, không coi là pass. |
| A10 | Replay offline khớp byte hai provenance; LIVE mới/freshness endpoint **KHÔNG ĐO ĐƯỢC**. |
| A11 | passed Ruff hai tệp, doctrine10/0, ADR53/53, diff/check/write set. Trần mới áp theo assignment; báo1649, không tự đặt trần khác. |
| A12 | not_run/not_measured: không đẩy code, không mạng đo remote fence/nhánh. Cần đo ở bước đẩy có authority. |
| A13 | chưa hoàn tất: metadata đúng thread đã đọc; stdout thread.started, rollout hash sau kết thúc và launcher receipt do bên vận chuyển đóng băng sau run. Không tự nhận approval. |
| A14 | passed c25 env metadata mang màu không xác thực; mutant đúng ca. |
| A15 | passed c26 tập con khối không xác thực; mutant subset đúng ca. |
| A16 | passed c27 nguyên khối/lời gọi tối giản và đối chứng; các miền bổ sung chưa khóa thuộc F10. |
| A17 | passed c28–31/c46/c48–49: env ba mức, đối số, prefix, defaults, shell; D01 đo riêng. Không suy phủ mọi miền từ250 seed. |
| A18 | passed c32/c34: workflow thiếu object/path/YAML/SHA không marker, không ném ở tập đã thử; reader Git thật và mutant fallback. |
| A19 | passed c33 + c49 vị trí nhiều job, mutant chặn theo job khác/trùng chữ. |
| A20 | passed c36 count log/REST/YAML và mutant từng vế. |
| A21 | passed c37/c48–49 tên và mutant; phần coercion/miền mới ở F10. |
| A22 | passed c38/calendar/mutant, c49 cửa sổ bất kỳ vị trí; miền lịch/cửa sổ còn thiếu răng thuộc F10. |
| A23 | passed c39/c47–49 duy nhất/name/prefix/expression; miền tên mới thuộc F10. |
| A24 | passed c40/c35 nested; biến thể tương đương không ép giết. |
| A25 | passed c41 uses/composite/count, mutant đúng ca. |
| A26 | passed c42/c47–49 ENV/PATH trước/khác job/sau, skipped; nguồn và dữ liệu còn thiếu răng thuộc F10. |
| A27 | passed c43 khối khác bước, mutant đúng ca. |
''')
texts.append('''
**Phép đo đã chạy.** Từ gốc checkout, `PYTHONDONTWRITEBYTECODE=1 python -B .review/run.py <nhãn> <command...>` đặt TMPDIR/TMP/TEMP/cache trong `.review/`, giữ command, rc con thật, stdout/stderr và SHA-256. Tất cả mutation source là bản sao, chạy `python -B` với `CI_PROVENANCE_MA=<bản sao>`. Chỉ `rc3 + DO:<đúng ca>:` từ `TinHieuChotCa` được tính giết; lỗi import/anchor/setup hay ngoại lệ không được đổi thành pass.

| phép đo | kết quả dương / trạng thái |
|---|---|
| `python -B ops/ci_provenance_test.py` | passed, rc0: `CA: 49/49 dat`; `DOT BIEN: 231/231 bi giet dung ly do`; `TU KIEM PHAN HANG: DAT (2 dot bien)`; `TONG: DAT`. `suite.json` giữ command/rc/hash. |
| `python -B .review/audit_mutants.py` | passed, 231 mutant đúng ca; hai tự kiểm cố ý TIN_DUNG_GIA và SONG_SOT. `mutants/results.json` giữ baseline/neo/thay/ca/command/rc/output/hash từng mục. |
| `python -m ruff check --no-cache --select F ops/ci_provenance.py ops/ci_provenance_test.py` | passed rc0, `All checks passed!`; Ruff0.15.15. |
| Ruff pin/probe contract qua `loi_ruff_ci()` | passed rc0, `RUFF_CONTRACT 3 []`; riêng với bare lint. Bare lint `scripts/tl.py` not_run. |
| `python -B .claude/dev/packet_loop.py doctrine-scan --root .` | passed rc0, 10 tệp/0 chỗ chép doctrine. |
| `python -B .claude/dev/packet_loop.py adr-song --root .` | passed rc0,53 ADR/53 dòng; exemption lịch sử0016 được giữ nguyên. |
| Các probe/driver lịch sử, toán tử, normalization, frontier và phản chứng riêng | Các JSON ledger phân biệt lệnh con, target và lỗi raw/stale. Bảng bên dưới và MUTANTS.md liệt kê từng mục. |
| A9 full registry, heavy/release gates, CI mới, connector, network/LIVE | not_run theo authority và môi trường offline; không chuyển thành passed. |

`generator6-results.json` tái sinh độc lập đúng seed của c49: 250 kịch bản; 189 ghép passed,61 hỏng;487 marker (74 passed,75 failed,338 chặn chế độ). Alias dài tối đa7;0 tên REST ngoài ASCII;0 bước skipped có giờ thiếu/null. Số250 không chứng minh các miền này được thử. Những ca mới ở `cases6.py` giữ dữ liệu phân biệt để đổi chốt nào thì đúng oracle của chốt ấy đỏ.

**Đối chiếu script lịch sử.** `legacy6-results.json`, `legacy-cli-repaired6.json`, `legacy-after-suite6-results.json`, `historical-target-inventory6.json`, `historical-targets6/results.json`, `normalization6-results.json`, `reanchored6-results.json` và `signature6-results.json` giữ provenance. Chạy lại các probe/counterexample được giao của lượt1–5; các phép đo trùng neo/thay được hợp nhất và nối producer, không cộng thành mẫu độc lập. Các target lịch sử đã có tín hiệu giết thì chạy lại đúng target và baseline; mục chưa có target chạy cho tới tín hiệu đúng hoặc hết49 ca. Vì vậy không tự nhận đã quét mọi lỗi ở mọi ca cho mỗi mutant lịch sử/toán tử. Frontier5 và frontier mới chạy đủ49 ca trên mỗi mutant.

Các lỗi raw đã giữ, không phải finding sản phẩm: driver `reviewer_cases_r4.py` cần tên ca (đã chạy lại8 ca ×2); composite cần stdout suite thật (đã chạy lại sau suite); finish_probes cần thư mục output; operator target map stale vì chữ ký env thay đổi (đã tạo lại target đúng); ba anchor cũ có đường tương đương/đường ngược đã tái neo. Tệp nguồn r2 đi qua bản được giao vì OID lịch sử thiếu trong shallow clone; không tự xác thực được OID ấy. `n_env_v_truthy` và `env_prefix_value_only` bị biến dạng bởi adapter chữ ký cũ được ghi riêng là lỗi dựng phép đo, rồi đo lại đúng ý nghĩa trong `signature6-results.json`. Không lấy ca bắt NameError/KeyError do adapter sai làm bằng chứng cho kiểm giá trị env.

Script dựng snapshot/chuẩn bị/render verdict lịch sử và các bản source mutant là hiện vật, không phải ca nghiệm thu; không chạy các writer lịch sử để ghi đè verdict hiện hành. Phạm vi trên được khai tường minh, không gọi rc0 ngoài cùng là mọi phép con đã đạt.

**Replay A10 offline.** `replay.json`, `prior2/q1-summary.json`, `prior2/q1-details.json`, `a10checks6-results.json`: 37/37 full log khớp SHA256SUMS và hash/size trong provenance đóng băng. Hai workflow tại checkout SHA không có env null ở workflow/job. Hai provenance mới giống từng byte với bộ A10 đo trên52e9573: **0 khác biệt cần giải thích**.

| run / attempt | Run | Checkout / ghép bước | Gate và marker | SHA-256 provenance |
|---|---|---|---|---|
|39342960764 /1|passed|13 passed tại b27fe85…;1 chuan-bi not_measured; ghép13/14|14 Gate not_measured,0 failed;0 marker đường dẫn MOI; các đường ngoài MOI giữ not_measured|`5ad9afeafb5312101ae326d738855e8adb1e46e7e4240944c2b21e12ed2bafe0`|
|40074551995 /1|passed|22 passed tại dc65714…;1 chuan-bi not_measured; ghép22/23|23 Gate not_measured,0 failed;8 gate-nhanh-manh có nhanh_don_duoc not_measured/che_do_khong_xac_dinh; gate-nhanh-gop không marker|`24ffa770ff268876c030f12f59fee1010956138ba2ca3fa4370710456ffd185b`|

Tất cả labels ubuntu-latest; Workflow definition vẫn not_measured. Replay không đo LIVE hiện tại, hạn giữ log, Windows/pwsh thật, PR synthetic merge thật, action đổi môi trường hay receipt vận chuyển sau run. Không nhận replay thay A10 LIVE cuối cùng mà owner yêu cầu ở SHA cuối.

**Danh sách mutant sống và phân hạng.** Với mỗi P1, toàn bộ49 ca của repository xanh trên mutant; phản chứng riêng HEAD0→mutant3 đúng tên trong `proof-final6-results.json`. Các biến đổi định nghĩa được trên đầu vào malformed vẫn được phân theo quyết định chủ kho; không lấy việc runner có nhận workflow đó hay không làm cách miễn M4/M12. Các P3 có quyết định đề xuất ngay trong bảng. Không cần sửa sản phẩm để giết các mutant khi HEAD đang đúng.

| mutant | hạng / lớp | bằng chứng và quyết định đề xuất |
|---|---|---|
''')
for z in surv:
 name=z['name']
 if name in p3:desc='P3 / tương đương, không mở lớp mới';note=p3[name]+' Owner đề xuất ducthangho: giữ nguyên sản phẩm, không thêm ca chỉ để giết mutant tương đương.'
 else:desc='P1 / F10';note='49/49 xanh; HEAD0 → mutant3 đúng `TinHieuChotCa`; neo/thay ở `'+('frontier6/results.json' if z in rows else ('frontier6-extra/results.json' if name=='rest_number_min_one_safe' else 'frontier6-extra2/results.json' if name=='job_nested_suffix_pure' else 'frontier6-extra3/results.json'))+'`, ca cùng tên ở `cases6.py`. Đóng bằng phân hoạch oracle tương ứng trong BẢNG LỚP.'
 texts.append('|'+name+'|'+desc+'|'+note+'|\n')
texts.append('''
`env_only_keys_str` được đánh giá trên miền thực sự đi qua yaml.safe_load; không tuyên bố tương đương trên Python object tuỳ ý. `rest_also_skip_null` và mảng rỗng kiểm đầu ra M12 dù Gate tổng có thể not_measured vì metadata khác; không suy ghép passed thành Gate passed. `log_endgroup_need_shell_first` thay đổi số bước xác thực với khối không phải lời gọi tối giản; không có marker passed giả trong phản chứng đó. Các ví dụ này giải thích chính xác kết quả đang được đặc tả định nghĩa và đo.

**Toàn bộ inventory mutant.** [MUTANTS.md](MUTANTS.md) liệt kê từng ID, producer, phân hạng thật, ca đích/phạm vi và cấp finding. GIET là kết quả phép đo; không phải một finding P1/P0 còn mở. TU_KIEM cố ý sống/ngoại lệ được đánh dấu riêng. Các lần đo trùng byte không cộng thành số mutant độc lập.

| producer | kết quả đo |
|---|---|
''')
texts.append('\n'.join(summary)+'\n')
texts.append('''
**TIN_DUNG_GIA và ngoại lệ ngoài ca đích.** Catalogue có một tín dụng giả cố ý để tự kiểm classifier. Đo bổ sung đúng các ca lỗi được ghi trong kq8.txt: 71 cặp mutant–ca thuộc29 toán tử đều TIN_DUNG_GIA. `operator-errors6-results.json` lưu baseline/SHA/source/command/rc/output; tối đa3 ca lỗi mỗi toán tử, không tự nhận là quét hết49 ca. `operators6-combined.json` hợp kết quả với các ca giết đúng:101 GIET,29 GIET+NEM. Hai toán tử dòng154 còn được đo các KeyError ở c28/c29/c31/c46; c49 bắt đúng nghĩa vụ không ném. Mọi lỗi ngoài ca đích đều không nhận tín dụng giết. Mutant `rest_number_order_contiguous` chết do ValueError ở c22 nên không tính GIET; bản biến đổi tương ứng có guard mảng rỗng (`rest_number_min_one_safe`) đã chạy riêng, sống49/49 và bị phản chứng số dương bắt đầu từ2 giết đúng ca. Các ngoại lệ khác được liệt kê đầy đủ ở MUTANTS.md và JSON từng producer, kể cả một mutant vừa có ca giết đúng vừa có lỗi vô can. Lỗi dựng script/anchor được tách ở phần đối chiếu lịch sử, không quy thành lỗi sản phẩm.

**Read-only và bàn giao.** Snapshot đầu/cuối băm tracked, untracked và ignored ngoài `.review/`, cùng HEAD/tree/diff/index. `snapshot-comparison6.json` xác nhận không có delta quan sát được; `git status --short` sạch. Chỉ chứng minh hai mốc, không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên. Repo nguồn ngoài checkout không nằm trong phạm vi quan sát. Các writer test đã kết thúc trước khi tạo `evidence-manifest6.json`; manifest giữ path/size/hash artifact và không tự chứng nhận runtime/transport sau khi phiên kết thúc. Không có authority land, approval hay quyền ghi vào branch Executor từ verdict này.
''')
# Mutation inventory keeps complete measurement outcomes, rather than just the survivors.
inv=['# Inventory đột biến — wp899 r4 lượt6\n\nNeo exact SHA `'+head+'`. Kết quả GIET phải có TinHieuChotCa đúng ca; scope khác nhau được khai từng producer.\n']
for label,a in [('catalogue',cat),('historical-targets6',hist),('frontier5',frontier5),('operators6',ops),('normalization6',norm),('frontier6',rows),('frontier6-extra',extra),('reanchored6',read('reanchored6-results.json')),('signature6',read('signature6-results.json'))]:
 inv.append('\n## '+label+'\n\n| ID | kết quả | hạng finding / disposition | ca / phạm vi |\n|---|---|---|---|\n')
 for z in a:
  name=z['name'];rank=z['rank'];sev='không finding (đã giết)' if rank.startswith('GIET') else 'không cấp tín dụng'
  if label.startswith('frontier6') and rank=='SONG_SOT':sev='P3: '+p3[name] if name in p3 else 'P1 / F10; proof-final6-results.json'
  elif name=='log_nested_after_only' or name=='nested_only_after_shell':sev='P3: tương đương; giữ nguyên, owner ducthangho; equivalence.json'
  elif z.get('expected') in ('SONG_SOT','TIN_DUNG_GIA'):sev='tự kiểm có chủ ý; đúng expected='+z['expected']
  elif rank=='HONG_NEO':sev='neo stale; xem reanchored6-results.json, không là kết quả sản phẩm'
  elif label=='normalization6' and name=='n_env_v_truthy':sev='adapter chữ ký stale; signature6-results.json đo đúng ý nghĩa'
  elif label=='frontier5' and name=='env_prefix_value_only':sev+='; bản adapter đúng ở signature6-results.json'
  target=z.get('case') or z.get('target') or ', '.join(z.get('killed',[])) or 'toàn49 ca / xem JSON'
  if type(target) is not str:target=str(target)
  inv.append('|'+name.replace('|','\\|')+'|'+rank+'|'+sev.replace('|','\\|')+'|'+target.replace('|','\\|')+'|\n')
  bad=z.get('other_errors',[])+z.get('additional_error_probes',[])
  if bad:inv.append('\nNgoại lệ riêng của `'+name+'`: `'+json.dumps(bad,ensure_ascii=False).replace('`','\\`')+'`\n\n')
(R/'MUTANTS.md').write_text(''.join(inv))
(R/'VERDICT.md').write_text(''.join(texts))
print(json.dumps({'verdict':'changes_requested','p1_classes':['F10'],'new_surviving_p1_mutants':len(p1),'new_p3_mutants':len(surv)-len(p1),'new_mutants_measured':len(new)},ensure_ascii=False))
