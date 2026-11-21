from pathlib import Path
import subprocess,sys,os,re,hashlib,unicodedata,json
O=Path(__file__).resolve().parent;R=O.parent/'cay-kho';P=O/'prototype';env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
spec=(R/'ops/specs/wp1466.md').read_text();old=subprocess.run(['git','-C',str(R),'show','937d135:ops/specs/wp1466.md'],capture_output=True,text=True,check=True).stdout
for key in ['khoa','p1-moi','p2-moi','p3-moi','p4-cu','p4-moi','p5-cu','p5-moi','p6-moi']:
 get=lambda s:re.search(r'~~~ '+key+r'\n(.*?)\n~~~',s,re.S)[1];print('BLOCK_UNCHANGED',key,get(spec)==get(old))
print('SPEC_LINES',len(spec.splitlines()),'UNUSUAL',sum((unicodedata.category(c) in ['Cc','Cf','Zl','Zp'] and c!='\n') or (unicodedata.category(c)=='Zs' and c!=' ') for c in spec))
audit=subprocess.run(['git','-C',str(R),'show','a8affd58c0a7db2668f8de8c542edd225ccc2586:ops/specs/wp1172-kiem83/AUDIT_TUAN_THU_PHIEN_DIEU_PHOI_20261120.md'],capture_output=True,text=True);print('AUDIT',audit.returncode,len(audit.stdout.splitlines()));print('MATRIX_POINTS',len(re.findall(r'^\| [ABC][0-9]+ ',spec.split('**15.2')[1].split('## 16.')[0],re.M)))
print('HISTORY_SLUGS',len(re.findall(r'^\| `[^`]+` · P[0-3] \|',spec,re.M)))
base=O/'base/.claude/dev';print('THREE_ANCHORS',[(f,s,(base/f).read_text().count(s)) for f,s in [('packet_loop.py','    proto_words = _doc_nguon_protocol(root)'),('packet_loop.py','9 bảng ADR §20 lệch với docs/adr/'),('packet_loop_test.py','protocol if protocol is not None else _PROTO_TRUNG_TINH, encoding=')]])
folder=R/'ops/specs/wp1466/nguyen-mau-r5';sumrows=[]
for line in (folder/'SHA256SUMS').read_text().splitlines():
 h,p=line.split(maxsplit=1);sumrows.append(hashlib.sha256((folder/p).read_bytes()).hexdigest()==h)
print('BUNDLE_CHECKSUMS',sum(sumrows),len(sumrows));patch=(folder/'nguyen-mau.patch').read_bytes();print('PATCH_LINES_HASH',len(patch.splitlines()),hashlib.sha256(patch).hexdigest())
for name in ['do_pham_vi.py','so_dang_ky.py','tien_kiem.py']:print('BLOCK_SCRIPT_BYTES',name,(O/'sc'/name).read_bytes()==(folder/'sc'/name).read_bytes())
for name in ['moi','cu']:
 lines=(O/(name+'.log')).read_text().splitlines();oks=[l for l in lines if re.match(r'^  ok  \S+ → giết [0-9]+ ca đích',l)];print('MUTANT_OK_LINES',name,len(oks),'THREE_CONTROLS',sum('3 đối chứng khác họ còn sống' in l for l in oks));print('BASE_LINE',[l for l in lines if 'nền:' in l or 'BỎ QUA:' in l])
for case in ['tien_to_thu_muc','tien_to_khong_gach','khac_kieu_chu','chi_effective','planned_gach_nguoc','lien_ket_thu_muc','policy_co_mat']:
 k=O/'tmp/fx2'/case/'kho';r=subprocess.run([sys.executable,'-B',str(k/'ops/lease_publish.py'),'ai-dang-giu','.claude/dev/packet_loop.py','--root','.'],cwd=k,capture_output=True,text=True,env=env);print('RAW_MATCHER',case,r.returncode,(r.stdout+r.stderr).strip().splitlines()[-1])
sys.path.insert(0,str(P/'ops'));import ci_duong_nhanh as ci
for path in ['docs/adr/0068-bat-bien-protocol-va-review-theo-lop.md','docs/PROTOCOL_DA_PHIEN.md','.claude/dev/packet_loop.py','.claude/dev/packet_loop_test.py']:
 print('CI_ADMISSION',path,ci.phan_loai_packet_loop('pull_request',[path]))
print('CI_MASTER_ADMISSION',ci.phan_loai_packet_loop('push',[]))
