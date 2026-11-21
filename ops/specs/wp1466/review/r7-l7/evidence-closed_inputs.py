"""Đo bằng dữ liệu bình thường; không tạo payload đường dẫn hay mã độc."""
from pathlib import Path
import os,sys,subprocess,ast,json,datetime,shutil
O=Path(__file__).resolve().parent
os.environ.update(PYTHONDONTWRITEBYTECODE='1',TMPDIR=str(O/'tmp'),GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='commit.gpgsign',GIT_CONFIG_VALUE_0='false')
sys.argv=['fx',str(O),str(O/'base/ops/lease_publish.py')]
s=(O/'sc/fx_tien_kiem.py').read_text();stop=next(n.lineno for n in ast.parse(s).body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='KB' for t in n.targets))
h={};exec(compile('\n'.join(s.splitlines()[:stop-1]),'helpers', 'exec'),h)
h['FX']=O/'tmp/closed-inputs';h['FX'].mkdir(exist_ok=True)
g=h['g'];env=h['ENV'];TK=O/'sc/tien_kiem.py'; rows=[]
def record(name,cmd,rc,out,extra=None):
 r=dict(name=name,command=cmd,rc=rc,output=out,extra=extra); rows.append(r);print(json.dumps(r,ensure_ascii=False),flush=True);(O/'closed-inputs.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2))
def check(k,name,extra=(),flags=('-I','-B'),ev=None,script=TK):
 cmd=[sys.executable,*flags,str(script),'origin/master',*extra];r=subprocess.run(cmd,cwd=k,env=ev or env,capture_output=True,text=True)
 record(name,cmd,r.returncode,(r.stdout+r.stderr).strip());return r
print('UTC',datetime.datetime.now(datetime.timezone.utc).isoformat(),flush=True)
# --sau-dang là đầu vào độc lập với B/ref, chưa có dòng V/P dành cho nó.
h['dung']('sau',nhanh=h['GIU_A']);k=h['FX']/'sau/kho'
check(k,'sau_before')
check(k,'sau_other_packet_id',('--sau-dang',h['A']))
check(k,'sau_missing_own',('--sau-dang','wp1466-r7-g1-claude'))
h['dang_rieng'](k,ten='wp1466-r7-g1-claude')
check(k,'sau_two_live_correct_id',('--sau-dang','wp1466-r7-g1-claude'))
# Biên đường dẫn policy: tên ghi chú bình thường, trong/ngoài coordination.
for name,path in [('policy_notes_inside','.github/coordination/change-impact-notes.md'),('policy_notes_outside','docs/change-impact-notes.md'),('policy_other_coord','.github/coordination/notes.md')]:
 rc,out=h['dung'](name,master_them=[(path,'Notes for maintainers.\n')]);record(name,['fixture',path],rc,'\n'.join(out))
# Cấu hình local init.templateDir: xem init có đọc config clone không, dùng tệp marker thuần dữ liệu.
h['dung']('template');k=h['FX']/'template/kho';td=k.parent/'template';td.mkdir();(td/'ordinary-marker').write_text('ordinary template data\n')
g(k,'config','init.templateDir',str(td))
dest=k.parent/'new-bare';rr=subprocess.run(['git','init','-q','--bare',str(dest)],cwd=k,env={'PATH':'/usr/bin','HOME':str(k.parent),'GIT_CONFIG_NOSYSTEM':'1','GIT_CONFIG_GLOBAL':os.devnull},capture_output=True,text=True)
record('local_init_template',['git','init','-q','--bare',str(dest)],rr.returncode,rr.stdout+rr.stderr,{'marker_copied':(dest/'ordinary-marker').exists()})
check(k,'clone_config_init_template')
# -I giữ -S/-X: chỉ copy nguyên stdlib os.py để kiểm lời khai os đã nạp sẵn, không đổi thuật toán.
h['dung']('os_startup');k=h['FX']/'os_startup/kho'
import sysconfig
shutil.copyfile(Path(sysconfig.get_path('stdlib'))/'os.py',k/'os.py');shutil.copyfile(TK,k/'tk.py')
r=subprocess.run([sys.executable,'-B','-S','-X','frozen_modules=off','-v',str(k/'tk.py'),'origin/master'],cwd=k,env=env,capture_output=True,text=True)
(O/'os-startup-trace.log').write_text(r.stdout+r.stderr)
record('os_before_reexec',[sys.executable,'-B','-S','-X','frozen_modules=off','-v','tk.py','origin/master'],r.returncode,r.stdout,{'local_os_loaded':str(k/'os.py') in r.stderr,'trace':[x for x in r.stderr.splitlines() if str(k/'os.py') in x]})
# Policy có từ side parent và bị bỏ ở merge; bản sao Git thật, dữ liệu bình thường.
for label,mode in [('merge_ours', 'ours'),('merge_revert','revert')]:
 h['dung'](label);k=h['FX']/label/'kho';base=g(k,'rev-parse','master').strip();p=k/'.github/coordination/change-impact.v1.json';g(k,'checkout','-q','-b','side');p.parent.mkdir(parents=True);p.write_text('{}\n');g(k,'add','-A');g(k,'commit','-q','-m','add policy');g(k,'checkout','-q','master')
 if mode=='ours':g(k,'merge','-q','--no-ff','-s','ours','-m','merge','side')
 else:
  g(k,'merge','-q','--no-ff','-m','merge','side');g(k,'rm','-q',str(p));g(k,'commit','-q','-m','remove')
 g(k,'branch','-q','-D','side');g(k,'push','-q','origin','master');g(k,'fetch','-q','origin')
 cmd=[sys.executable,'-I','-B',str(TK),base];r=subprocess.run(cmd,cwd=k,env=env,capture_output=True,text=True);record(label,cmd,r.returncode,r.stdout+r.stderr)
