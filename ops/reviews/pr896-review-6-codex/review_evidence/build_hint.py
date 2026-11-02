from pathlib import Path
import difflib,hashlib,json,subprocess,yaml
from audit import ROOT,OUT,BASE,SHA,MASTER,record
from states import at
copy=Path((OUT/'copy-path.txt').read_text());assert subprocess.check_output(['git','-C',str(copy),'status','--porcelain']).strip()==b''
rows=json.loads((OUT/'residual-status.json').read_text());landrows=json.loads((OUT/'land-surfaces.json').read_text());oldbytes={};newbytes={}
def read(path):
 if path not in oldbytes:oldbytes[path]=(ROOT/path).read_bytes() if (ROOT/path).exists() else b''
 return oldbytes[path].decode()
def replace_field(path,keys,value):
 text=newbytes.get(path,read(path).encode()).decode();node=yaml.compose(text)
 for key in keys:
  node=node.value[int(key)] if isinstance(node,yaml.SequenceNode) else next(v for k,v in node.value if k.value==key)
 # Replace full scalar including YAML >- body; retain following field indentation.
 start,end=node.start_mark.index,node.end_mark.index
 emitted=json.dumps(value,ensure_ascii=False)
 if node.style in ['>','|']:emitted+='\n'
 newbytes[path]=(text[:start]+emitted+text[end:]).encode()
for x in rows:
 if x['schema_version']!=2:continue
 path=x['receipt'];keys=x['field'].split('.')
 current=at(yaml.safe_load((ROOT/path).read_text()),keys)
 measured=(f"Do lai tai {SHA}: git merge-base --is-ancestor {x['evidence_oid']} {MASTER} va voi {SHA} deu rc=0; "
           f"git ls-tree {MASTER} -- {path} co blob cua receipt. Vi vay 'canonical inclusion pending'/chi-tren-PR/CHUA giao/chua o master "
           "o tren chi la loi khai lich su cua blob duoc neo, khong phai trang thai hien hanh. Chi dinh chinh quan he Git, khong nang assurance/cuong_do hay suy Packet da landed.")
 value=f"Loi khai lich su trong blob tai {x['last_unchanged_blob_commit']}: {current} {measured}"
 replace_field(path,keys,value)
supp_path='ops/reviews/pr896-review-6-legacy-caveats.yaml';supp={'kind':'supplementary_historical_caveats','measured_at_sha':SHA,'ghi_chu':'Dinh chinh tai lieu; khong phai review delivery receipt hay authority. Giu nguyen byte cac receipt v1 dong bang.','caveats':[]}
readme=read('ops/reviews/README.md');readme_rows=[]
for x in rows:
 if x['schema_version']!=1:continue
 d=yaml.safe_load((ROOT/x['receipt']).read_text())
 desc=(f"Dinh chinh {x['field']} cua receipt v1 dong bang (loi khai trong blob {x['last_unchanged_blob_commit']}). "
       f"Do lai tai {SHA}: git merge-base --is-ancestor {x['evidence_oid']} {MASTER} va voi {SHA} deu rc=0. "
       "Cau 'hien chi duoc nhanh giu'/chi-song-tren-nhanh/KHONG-trong-lich-su-master khong con la trang thai hien hanh. "
       "Chi xac nhan quan he Git cua OID nay; giu byte, verdict va assurance lich su, khong suy Packet da landed. "
       f"Dinh chinh o {supp_path}.")
 c={'receipt_path':x['receipt'],'verdict_path':d['verdict_path'],'verdict_sha256':d['verdict_sha256'],'id':'ANCESTRY-CHI-TREN-NHANH-LA-TRANG-THAI-LICH-SU','muc':'P1','mo_ta':desc}
 supp['caveats'].append(c);readme_rows.append(f"| `{Path(d['verdict_path']).name}` | `{c['id']}` | {desc} |")
read(supp_path);newbytes[supp_path]=yaml.safe_dump(supp,sort_keys=False,allow_unicode=True).encode()
needle='\n## Mục lục\n';assert readme.count(needle)==1;newbytes['ops/reviews/README.md']=readme.replace(needle,'\n'+'\n'.join(readme_rows)+'\n'+needle).encode()
for x in landrows:
 stem=x['verdict'].split('-provenance/')[0];path=stem+'-land-evidence.yaml';text=read(path)
 if x['source'].endswith('.json'):
  run=x['runtime'];desc=(f"Verdict dong {x['line']} tu khai execution_surface codex_service, nhung {x['source']} "
                       f"(run {run['run_id']}, head {run['head']}, lenh.chuong_trinh=codex) ghi execution_surface=codex_cli, transport=machine. "
                       "Dinh chinh be mat cua CHINH luot nay thanh codex_cli.")
 else:
  desc=(f"Verdict luot 1 dong {x['line']} tu khai codex_service, nhung {x['source']} bat dau bang OpenAI Codex v0.163.0, "
        "session 01a157da-2170-7be2-b6d0-053fa8f91aec; review.luot_1.reviewer cua ho so nay ghi codex exec truc tiep. "
        "Dinh chinh be mat luot 1 thanh codex_cli. Khong dung run-f0909b38.json cua LUOT 2 de chung minh luot 1.")
 desc+=' Giu nguyen byte verdict lich su; khong chung thuc model/effort hay nang assurance/quyen merge/land.'
 block={'verdict_usage_caveats':[{'id':'VERDICT-KHAI-SAI-EXECUTION-SURFACE','muc':'P1','verdict_path':x['verdict'],'verdict_sha256':x['sha256'],'mo_ta':desc}]}
 assert 'verdict_usage_caveats' not in yaml.safe_load(text)
 newbytes[path]=(text.rstrip()+'\n\n'+yaml.safe_dump(block,sort_keys=False,allow_unicode=True)).encode()
patch='# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'
for path,new in sorted(newbytes.items()):
 old=oldbytes[path];patch+=''.join(difflib.unified_diff(old.decode().splitlines(keepends=True),new.decode().splitlines(keepends=True),fromfile=path if old else '/dev/null',tofile=path))
(BASE/'HINT.patch').write_text(patch)
# Dry run from the original SHA, before applying to the scratch clone.
p=subprocess.run(['patch','--dry-run','--batch','--fuzz=0','-p0','-i',str(BASE/'HINT.patch')],cwd=copy,capture_output=True,text=True)
(OUT/'hint-dry-run.log').write_text(p.stdout+p.stderr);assert p.returncode==0,(p.stdout,p.stderr)
p2=subprocess.run(['patch','--batch','--fuzz=0','-p0','-i',str(BASE/'HINT.patch')],cwd=copy,capture_output=True,text=True)
(OUT/'hint-apply.log').write_text(p2.stdout+p2.stderr);assert p2.returncode==0,(p2.stdout,p2.stderr)
for path,new in newbytes.items():
 assert (copy/path).read_bytes()==new
 if path.endswith('.yaml'):yaml.safe_load(new)
(OUT/'hint-paths.json').write_text(json.dumps(list(sorted(newbytes)),indent=2))
output=f'patch_paths={len(newbytes)} dry_run_rc={p.returncode} apply_rc={p2.returncode}\n'+p.stdout+'clone='+str(copy)+'\n'+subprocess.check_output(['git','-C',str(copy),'diff','--stat']).decode()
record(12,'Gợi ý vá tài liệu trên bản sao','python3 review_evidence/build_hint.py; patch --dry-run --batch --fuzz=0 -p0 -i <HINT.patch>',output,'KHÔNG PHẢI LỖI của hint; mới áp trên clone tại reviewed_sha, chưa chạy trên cây thật; không đổi ba receipt v1 hoặc byte verdict')
