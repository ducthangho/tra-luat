from audit import R,P,y,j,out
import sys
land=y(R/'ops/land/pr1047-wp1045-land-evidence.yaml')
which=sys.argv[1:]
if not which or 'authorization' in which:
    pr=j(P/'readback-pr-1047.json'); comment=j(P/'readback-comment-6529094452.json')
    out('authorization_claim',land['authorization_ghi_chu'].split('; ')[-1])
    out('readback_merge',dict(merged=pr['merged'],merged_by=pr['merged_by']['login'],merged_at=pr['merged_at'],head_sha=pr['head']['sha']))
    out('authorization_comment_body',comment['body'])
    conditions=land['trang_thai_packet']['landed_dieu_kien']
    out('same_file_final_condition_5',conditions.split('(5) uy quyen')[1].split('(6)')[0])
    out('same_file_reopen',conditions.split('Mo lai')[1])
    out('land_operator_caveat',land['land_operator'])
    out('landed',land['trang_thai_packet']['landed'])
    print('Nguoi bam / duyet land exact-SHA: KHÔNG ĐO ĐƯỢC tu hai readback nay.')
if not which or 'labels' in which:
    jobs=j(P/'readback-jobs-41099486628.json')['jobs']
    out('claim',land['pre_merge_checks'][1]['ghi_chu'])
    out('counterexamples',[{k:x[k] for k in ('id','name','conclusion','labels','runner_id')} for x in jobs if x['name'].startswith('gate') and 'windows-latest' not in x['labels']])
    out('executed_gate_jobs',sum(x['name'].startswith('gate') and x['conclusion']=='success' and x['labels']==['windows-latest'] for x in jobs))
    out('job_counts',dict(success=sum(x['conclusion']=='success' for x in jobs),skipped=sum(x['conclusion']=='skipped' for x in jobs)))
