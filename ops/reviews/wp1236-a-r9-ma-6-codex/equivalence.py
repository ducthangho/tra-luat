import pathlib,importlib.util,json,itertools,random,re
w=pathlib.Path(__file__).resolve().parent;r=w.parent/'repo'
def load(p,n):
 s=importlib.util.spec_from_file_location(n,p);m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m
g=load(r/'ops/gate_output_doi_chieu.py','g'); variants={x['id']:x for x in map(json.loads,(w/'independent_mutants.jsonl').read_text().splitlines())};p=w/'contrast_modules/ref_no_boundary.py';p.write_text(variants['ref_no_boundary']['src']);m=load(p,'mutant')
parts=['','x','/','../',' ',':','é','_','-','.', 'danh-gia-gate-output-1.txt','danh-gia-gate-output-2.txt'];diff=[];count=0
for xs in itertools.product(parts,repeat=4):
 s=''.join(xs);a,b=g.tep_danh_gia(s),m.tep_danh_gia(s);count+=1
 if a!=b:diff.append([s,a,b])
proof='Mọi ký tự của phần tên tệp bắt buộc đều thuộc lớp C=[A-Za-z0-9_./-]. Prefix C* tham lam làm match bắt đầu ở đầu dải C và kết thúc ở tên hợp lệ cuối trong dải; findall không cần khởi đầu lại trong cùng dải. Lookbehind cùng C không loại thêm match trong miền str này.'
(w/'equivalence.json').write_text(json.dumps({'ref_no_boundary':{'vectors':count,'differences':diff,'argument':proof},'identity_equivalent':['identity_72_67','identity_85_11','identity_126_7','identity_131_7','identity_154_11','identity_262_25','identity_271_11','identity_285_19'],'identity_scope':'Giá trị được tạo bởi parser/Path/regex chuẩn và YAML safe_load; loại hai phép is True trong la_landed vì int 1 phân biệt được.'},ensure_ascii=False,indent=2));print('REF_BOUNDARY',count,'DIFF',len(diff))
