from pathlib import Path
import subprocess, json,re,sys,os,ast
W=Path(__file__).resolve().parent.parent;O=W/'out';P=O/'prototype'
source=(P/'docs/PROTOCOL_DA_PHIEN.md').read_text(); code=P/'.claude/dev/packet_loop.py'
root=O/'protocol-probe';(root/'docs').mkdir(parents=True,exist_ok=True)
env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1')
def probe(name,text):
 assert name=='clean' or text!=source,name
 (root/'docs/PROTOCOL_DA_PHIEN.md').write_text(text)
 r=subprocess.run([sys.executable,'-B',str(code),'doctrine-scan','--root',str(root)],capture_output=True,text=True,env=env)
 print(name,'rc',r.returncode,json.dumps((r.stdout+r.stderr).strip(),ensure_ascii=False),flush=True)
def paragraph(prefix):return re.search(r'(?ms)^'+re.escape(prefix)+r'.*?(?=\n[ \t]*\n)',source)[0]
probe('clean',source)
for name,text in [('scope_cut','Thiếu quan sát, cắt acceptance hoặc chuyển biểu hiện ra ngoài scope không được\ntính là vá.'),('slug_map','Tách/gộp lớp cần bảng nối slug nguồn, lý do và phép\nđối chiếu trên cùng tập finding;'),('two_transitions','Hai chuyển tiếp liên tiếp có tỷ lệ <50% thì dừng vòng\nvá và đưa bằng chứng tới Review Rescue Checkpoint bên dưới.')]:
 assert source.count(text)==1
 probe('old_'+name,source.replace(text,''))
row=next(x for x in source.splitlines() if x.startswith('| `INV-07`'))
probe('old_table_split',source.replace(row,'\n'+row))
probe('old_table_spacing',source.replace(row,row.replace('| `INV-07` |','|  `INV-07`   |')))
for label,prefix in [('K04','Từ lượt review thứ HAI trở đi'),('K05','**Tín hiệu không hội tụ theo lớp.**'),('K06','Báo riêng các lớp mới tại r+1'),('K07','Checkpoint vì tín hiệu không hội tụ')]:
 para=paragraph(prefix)
 probe('tab_indent_'+label,source.replace(para,'\n'.join('\t'+x for x in para.splitlines()),1))
 probe('relocate_'+label,source.replace(para,'',1)+'\n\n## Phụ lục lưu trữ phép đo\n\n'+para+'\n')
 # A tab is an alternative four-column Markdown indentation, not attack text.
probe('duplicate_K04',source+'\n\n## Phụ lục lưu trữ phép đo\n\n'+paragraph('Từ lượt review thứ HAI trở đi')+'\n')
section=re.search(r'(?ms)^### 1\.1 .*?(?=^#)',source)[0]
# Move a complete frozen unit under an unrelated parent section.
probe('relocate_K01',source.replace(section,'',1)+'\n\n## Phụ lục lưu trữ phép đo\n\n'+section+'\n')
# Outside scope, declared limitation: do not count as unexpected failure.
line='Reviewer phải dùng checkout/context độc lập'
print('PROBE_NOTE path/security payloads: not constructed; supplied symlink tests are run unchanged')
