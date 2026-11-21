from pathlib import Path
import subprocess,sys,re,ast
O=Path(__file__).resolve().parent;P=O/'prototype'; out=O/'n8';out.mkdir(exist_ok=True)
code=(P/'.claude/dev/packet_loop.py').read_text();test=(P/'.claude/dev/packet_loop_test.py').read_text()
def run(name,mode,src):
 path=out/(name+'.py');path.write_text(src)
 r=subprocess.run([sys.executable,'-B',str(O/'n8_spec.py'),mode,str(O/('base-packet_loop.py' if mode=='ma' else 'base-packet_loop_test.py')),str(path)],capture_output=True,text=True)
 print(name,'rc',r.returncode,r.stdout.strip(),r.stderr.strip(),flush=True)
run('clean_ma','ma',code);run('clean_test','test',test)
needle='    return tu\n\n\n# --- ADR-0068';assert code.count(needle)==1
run('old_boundary_pass','ma',code.replace(needle,'    return tu\n    pass\n\n\n# --- ADR-0068'))
for name,extra in [('new_named_constant','INV_REVIEW_NOTE = 9'),('same_value_chained_binding','INV_REVIEW_NOTE = RC_ADR = 9'),('same_value_annotation','INV_REVIEW_NOTE: int = 9')]:
 # Harmless values; no candidate is executed. Probe the binding contract only.
 run(name,'ma',code.replace('INV_KHOA_PROTOCOL = (',extra+'\nINV_KHOA_PROTOCOL = (',1))
run('old_case_pass','test',test.replace('def case_doctrine_inv_fixture_trung_tinh_thuan', 'def case_doctrine_inv_fixture_trung_tinh_thuan',1).replace('    return r\n\n\n', '    pass\n    return r\n\n\n',1))
print('SAME_VALUE_BINDING stores RC_ADR, validator must reject even though value is unchanged',flush=True)
