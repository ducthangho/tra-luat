from review_probe import hunt, row

cmd = r"""python3 - <<'PROBE'
from pathlib import Path
import yaml
for p in sorted(Path('.github/workflows').rglob('*')):
 if not p.is_file(): continue
 d=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
 print(p.name,'events=',list(d.get('on',{})))
 if p.name == 'ci.yml':
  print('chuan-bi.outputs.os=',d['jobs']['chuan-bi']['outputs']['os'])
 else:
  for name,j in d.get('jobs',{}).items():
   for s in j.get('steps',[]):
    if 'run' in s:
     lines=[l for l in s['run'].splitlines() if l.strip() and not l.lstrip().startswith('#')]
     print('run',name,s.get('name',s.get('id','unnamed')),repr('\n'.join(lines)[:210]))
PROBE
rg -n --max-columns 250 'gh[[:space:]]+workflow|actions/workflows|createWorkflowDispatch|/dispatches|workflow_run:|repository_dispatch:|workflow_call:|schedule:' .github ops .claude/dev scripts -g '*.py' -g '*.yml' -g '*.yaml' -g '*.sh' -g '!ops/reviews/**' -g '!ops/land/**'
"""
hunt(9, 'Cò ẩn: schedule/workflow_run/reusable/dispatch tự động',
     'Một workflow tự gọi ci.yml hoặc schedule tạo gate Windows dù PR không nhãn và không gọi tay.', [cmd],
     'KHÔNG PHẢI LỖI cho hệ quả có điều kiện tại reviewed_sha: ci chỉ có push/master, pull_request và dispatch; schedule chỉ ở ci-dot-bien-du chạy Ubuntu; không thấy workflow_run/repository_dispatch/workflow_call hoặc lời gọi dispatch trong mã sống đã quét. KHÔNG ĐO ĐƯỢC automation ngoài kho và mọi run tương lai. Tuy nhiên ci.yml workflow_dispatch trên ref master là phản ví dụ cho câu không điều kiện “Windows trên master hiện chỉ đến từ launcher-windows.yml” (P2). Ghi chú kỹ thuật: lần dựng lệnh hướng 9 đầu bị SyntaxError ở harness ngoài kho (rc=1); lệnh trên là bản đã sửa và đã chạy.')
row('Windows trên master chỉ đến từ launcher-windows', 'câu nhấn mạnh không giới hạn loại event', 'HƯỚNG 2, 7, 9: ci.yml dispatch trên ref master cũng chọn Windows; output không loại ref master', 'Không: thiếu phạm vi push tự động (P2)')
row('Gate PR thường không tự đo Windows sau merge', 'không nhãn windows và không ai dispatch', 'HƯỚNG 7, 9: không cò ẩn gọi gate Windows; mọi consumer chung outputs.os', 'Có tại reviewed_sha, trong điều kiện đã nêu; không chứng minh mọi run tương lai')
row('Muốn Windows gate: dispatch trên ref đó', 'đường chắc chắn chọn ma trận Windows', 'HƯỚNG 2, 9: on.workflow_dispatch có; output không phụ thuộc ref', 'Có ở mức chọn runner; chưa đo run thật trong sandbox')

cmd = r"""python3 - <<'PROBE'
from pathlib import Path
import yaml
p=Path('.github/workflows/ci.yml'); d=yaml.load(p.read_text(),Loader=yaml.BaseLoader)
print('pull_request=',repr(d['on']['pull_request']))
print('workflow_dispatch=',repr(d['on']['workflow_dispatch']))
for name,j in d['jobs'].items():
 for s in j.get('steps',[]):
  if s.get('name') == 'PR head contains required EOL base' or 'release-verify strict (lane' in s.get('name',''):
   print('job=',name, 'step=',s['name'],'if=',s.get('if'),'run=',s.get('run'))
PROBE
git log --all --format='%h %s' --extended-regexp --grep='^Merge pull request #109([[:space:]]|$)'
git show --format=fuller 05170b4 -- CLAUDE.md
git show --format=fuller 3736fc0 -- CLAUDE.md
"""
hunt(10, 'Các câu giữ nguyên: labeled, EOL và dấu vết #109',
     'ci.yml đã thêm types labeled hoặc đổi if của bước EOL khiến lời cũ sai.', [cmd],
     'KHÔNG PHẢI LỖI về YAML: pull_request null, không types; labeled không được đăng ký; EOL if đúng pull_request nên push/dispatch master không chạy bước đó. Dấu vết hai lần sửa trên nhánh đã merge #109 đo được; raw review/comment và default event semantics trên máy chủ KHÔNG ĐO trực tiếp được khi không mạng. Bộ mặc định opened/synchronize/reopened được tài liệu và lịch sử repo mô tả nhất quán; không giả lập API thật.')
row('ci.yml không có labeled trigger', 'pull_request không types; mặc định opened/synchronize/reopened', 'HƯỚNG 10: parse YAML pull_request=""; git show 3736fc0; không đo trực tiếp event server', 'Có ở YAML; ngữ nghĩa mặc định chỉ đối chiếu dữ liệu cục bộ')
row('Gắn nhãn cần event sau đó', 'synchronize/reopened hoặc bổ sung types labeled', 'HƯỚNG 2, 10: matrix đọc labels event; labeled không có trong on', 'Có, suy từ YAML; không tạo PR/run thật')
row('Cross-review #109 P2 thứ hai', 'bẫy nhãn của workflow', 'HƯỚNG 10: 05170b4 rồi 3736fc0 và merge 9796f67; không có raw finding review', 'Dấu vết sửa khớp; mức P2/identity KHÔNG ĐO ĐƯỢC độc lập')
row('PR head contains required EOL base', 'if github.event_name == pull_request; master skipped', 'HƯỚNG 10: parse step.if; push/dispatch master không thỏa', 'Có ở điều kiện; job không khởi động thì không có step readback để gọi skipped')
