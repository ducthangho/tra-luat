import collections,hashlib,json,os,subprocess,sys,time
from pathlib import Path
W=Path(__file__).resolve().parent;R=W.parent/'repo'
def read(n):return json.loads((W/n).read_text())
def save(n,x):(W/n).write_text(json.dumps(x,ensure_ascii=False,indent=2)+'\n')
if not (W/'pilot_subset.receipt.json').exists():raise SystemExit('PILOT_PENDING')
pr=read('pilot_subset.receipt.json');assert pr['rc']==0
rows=[json.loads(x) for x in (W/'pilot_subset_kq.jsonl').read_text().splitlines()];hdr=rows.pop(0)
frozen={x['id']:x for x in map(json.loads,(R/'ops/reviews/wp1236-r10-soan/pilot_c2d606b_kq.jsonl').read_text().splitlines()) if 'id' in x}
manifest=[json.loads(x) for x in (W/'pilot_subset.jsonl').read_text().splitlines()]
assert len(rows)==99 and {x['id'] for x in rows}=={x['id'] for x in manifest}
fields=['sha256','phan_hang','giet','hong','rc']
mismatch=[{'id':x['id'],'fields':[k for k in fields if x[k]!=frozen[x['id']][k]]} for x in rows if any(x[k]!=frozen[x['id']][k] for k in fields)]
sum_old=json.loads((R/'ops/reviews/wp1236-spec-r10-6-codex/measurement_summary.json').read_text());non_eq=set('kho:'+x for x in sum_old['p2_survivors']+sum_old['p3_survivors']);eq=set('kho:'+x for x in sum_old['equivalent'])
assert not mismatch and len(non_eq)==25 and len(eq)==9
assert all(x['phan_hang']=='SONG' for x in rows if x['id'] in non_eq|eq)
pilot={'receipt':pr,'counts':dict(collections.Counter(x['phan_hang'] for x in rows)),'result_count':len(rows),'mismatches':mismatch,'non_equivalent25_reproduced':sum(x['id'] in non_eq and x['phan_hang']=='SONG' for x in rows),'equivalent9_reproduced':sum(x['id'] in eq and x['phan_hang']=='SONG' for x in rows),'completion_stdout':(W/'pilot_subset.stdout').read_text().splitlines()[-2:],'scope':'99 selected mutants, not full927; all prior25 non-equivalent survivors+9equivalent,all10incidental,55kills covering34target cases and every operator with a kill.'}
save('pilot_comparison.json',pilot)
v=read('VERDICT.json');v['review_status']='complete';v['pilot_replay']=pilot
v['validation_scope']['passed'].append('Pilot 99/99 khớp hash/rc/grade/giet/hong: 55 GIET, 34 SONG, 10 VO_CAN; tái hiện đủ 25/25 + 9/9, rc=0 và HOAN_TAT.')
v['validation_scope']['not_run'][0]='Full 927 pilot replay; đã chạy mẫu 99 có chủ đích, không là mẫu thống kê.'
v['da_do_khop'].append('Pilot chạy lại rc=0: 99/99 khớp pilot đóng băng, 55 GIET / 34 SONG / 10 VO_CAN / 0 LOI_CHAY; 25/25 survivor khác nghĩa và 9/9 tương đương đều tái hiện. Có HOAN_TAT và neo trong pilot_subset.stdout.')
v['execution_receipts'].append(pr)
v['evidence_files']+=['pilot_comparison.json','pilot_subset_kq.jsonl','pilot_subset.stdout','environment.json']
v['preflight']['capability']='Linux; Python 3.13.18/PyYAML 6.0.3; probe chuẩn hoá bằng Python 3.12.3/PyYAML 6.0.1. Repo review core.abbrev=7; ma_r9_git chưa đặt core.abbrev, các phép đo dùng full OID và không phụ thuộc short SHA. Không sửa config. Có objects 8048551 và ref review mã; freshness remote không đo vì cấm mạng.'
v['hoi_tu'].update(vong6_sang_7='0/2',U=['nghiem-thu-khong-co-lap-chot-dich','mo-ta-duong-dan-lech-hop-dong'],F=[],current_spec_finding_only='0/1')
v['hoi_tu']['giai_thich']='Đếm mọi lớp kế thừa còn VA_MOT_PHAN cuối vòng 6, sau phép nối alias đã có: W01 và L03, nên F/U=0/2. test-thieu-chot là alias của lớp W01, không đếm đôi. Nếu chỉ xét finding đặc tả mở W01 thì 0/1; không dùng cách đếm hẹp ấy để xoá nợ L03. Giữ nguyên tỷ lệ lịch sử 5→6=1/2. Checkpoint lặp lớp ít nhất ba vòng vẫn có hiệu lực.'
# Snapshot after all child processes are terminal. No new commands write to either source checkout.
os.environ['GIT_OPTIONAL_LOCKS']='0'
from bootstrap_review import snap
before=read('snapshot_before.json');after=snap();save('snapshot_after.json',after)
rr={}
for name in before:
 b=before[name];a=after[name];paths=sorted(set(b['files'])|set(a['files']));delta=[x for x in paths if b['files'].get(x)!=a['files'].get(x)]
 rr[name]={'files_before':len(b['files']),'files_after':len(a['files']),'changed_paths':delta,'git_equal':b['git']==a['git'],'head_tree':a['git']['rev-parse HEAD HEAD^{tree}']['stdout'].splitlines()};assert not delta and b['git']==a['git'],rr
v['read_only_snapshot']={'scope':'Mọi file thường ngoài .git có hash/mode; symlink có đích. Git HEAD/tree, status cả ignored/untracked, diff/index diff đo riêng. Không đo lịch sử từng ghi rồi hoàn nguyên.','before':'snapshot_before.json','after':'snapshot_after.json','results':rr}
v['validation_scope']['passed'].append('Snapshot repo và ma_r9_git không có delta quan sát được; HEAD/tree/diff/index/status khớp đầu/cuối.')
v['evidence_files'].append('snapshot_after.json')
save('VERDICT.json',v)
print('FINAL_REVIEW_DATA_READY',len(rows),rr)
