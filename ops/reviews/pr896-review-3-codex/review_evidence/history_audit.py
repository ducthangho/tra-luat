from pathlib import Path
import subprocess,yaml,json
ROOT=Path(__file__).resolve().parent.parent;R=ROOT/'cay-kho'
def git(*args):return subprocess.check_output(['git',*args],cwd=R)
S='82359c4deec90edebbaebf9ab9d094902120b567';P='ops/land/pr896-claude-md-bai-hoc-c-tro-nguon-land-evidence.yaml'
for a,b,name in [('578fb4b',S,'diff.patch'),('356eb26',S,'diff-pr947.patch')]:
 actual=git('diff',a,b);print(name,'equals_supplied=',actual==(ROOT/name).read_bytes())
 actual=git('diff','--numstat',a,b);name=name.replace('diff','numstat').replace('.patch','.txt');print(name,'equals_supplied=',actual==(ROOT/name).read_bytes())
old=git('show','765ae89^:'+P);new=git('show','765ae89:'+P);current=(R/P).read_bytes();master=git('show','356eb26:'+P)
print('land_prefix_preserved_at_record=',new.startswith(old),'old_bytes=',len(old),'new_bytes=',len(new));print('land_unchanged_after_765ae89=',new==current,'master_prefix_preserved=',current.startswith(master));block=yaml.safe_load(current)['cap_nhat_20261026_luot2'];print('luot2_landed=',block['landed'],'reviewer_assurance_81=',block['reviewer_assurance_81']);print('land_proposal=',block['don_vi_land_de_xuat']);
for c in ['3bc4244','a9bc934']:
 p=subprocess.run(['git','merge-base','--is-ancestor',c,'8d56009'],cwd=R);print(c,'ancestor_of_reviewed=',p.returncode)
print('CLAUDE_diff_3bc4244_to_target_bytes=',len(git('diff','3bc4244',S,'--','CLAUDE.md')))
for file in ['ops/reviews/pr896-review-2-codex-verdict.receipt.yaml','ops/reviews/README.md',P]:
 print('FILE',file)
 for i,l in enumerate((R/file).read_text().splitlines(),1):
  if ('CHUA ap' in l or 'chua ap' in l or 'HINT-P1-CHUA-AP' in l or ('caveat' in l and any(x in l for x in ['chua co','thieu','con']))):print(i,l)
for rev in ['578fb4b',S]:
 receipt=yaml.safe_load(git('show',rev+':ops/reviews/pr889-review-1-codex-verdict.receipt.yaml'));print(rev,'caveat_count=',sum(c['id']=='VERDICT-KHAI-SAI-EXECUTION-SURFACE' for c in receipt['verdict_usage_caveats']))
