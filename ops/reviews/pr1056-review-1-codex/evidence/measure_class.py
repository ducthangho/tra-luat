from pathlib import Path
import sys, subprocess, yaml
root=Path(__file__).resolve().parent.parent/'cay-kho'
sys.path.insert(0,str(root/'ops'))
import lease_publish as gate
print('CLASS_ORDER',gate._THU_TU_LOP)
for n,head in [(1,'c24875d'),(2,'f37b519')]:
    d=yaml.safe_load((root/f'ops/reviews/pr1050-review-{n}-codex-verdict.receipt.yaml').read_text())
    paths=subprocess.check_output(['git','-C',str(root),'diff','--name-only','b29da0b',head],text=True).splitlines()
    print('ROUND',n,'paths',len(paths),'declared',d['review_class'],'enum_valid',d['review_class'] in gate._THU_TU_LOP,'classifier_actual_diff',gate._tinh_lop_tu_write_set(paths),'effective_review_class',d.get('effective_review_class','ABSENT'))
print('IMPORTANT: classifier is a lease classifier; called here as a measurement of existing fail-closed path rules, not as proof that receipt schema validates review_class.')
