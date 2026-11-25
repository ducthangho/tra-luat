from pathlib import Path
import subprocess,sys,ast
O=Path(__file__).resolve().parent;h=(O/'prototype/.claude/dev/packet_loop.py').read_text();out=O/'n8-extra';out.mkdir(exist_ok=True)
old='9 bảng ADR §20 lệch với docs/adr/';new='9 bảng ADR §20 hoặc bất biến protocol lệch'
comment='        # `proto_words` luôn khác rỗng: `_doc_nguon_protocol` fail-close.\n'
assert h.count(new)==1 and h.count(comment)==1
variants={'clean':h,'omit_epilog':h.replace(new,old),'omit_epilog_delete_old_comment':h.replace(new,old).replace(comment,''),'omit_epilog_reflow_old_assignment':h.replace(new,old).replace('    root = Path(a.root)\n    muc_tieu: list[Path] = []','    root  = Path(a.root)\n    muc_tieu: list[Path] = []')}
for name,s in variants.items():
 compile(s,name,'exec');p=out/(name+'.py');p.write_text(s)
 r=subprocess.run([sys.executable,'-B',str(O/'sc/do_pham_vi.py'),'ma',str(O/'base/.claude/dev/packet_loop.py'),str(p)],capture_output=True,text=True)
 print(name,'rc',r.returncode,'EPILOG_REQUIRED',new in s,'OLD_COMMENT_PRESERVED',comment in s, r.stdout.strip().replace('\n',' | '))
