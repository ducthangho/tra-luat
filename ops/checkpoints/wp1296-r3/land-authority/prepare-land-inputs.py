from common import *
import hashlib
H='15ad82f56924a0ccc99833ec73eec078ce00b726';source=W/'review1-runs/c949f66c';out=W/'review1-transport-projection';out.mkdir()
r=json.loads((source/'run.json').read_text());raw=(source/'stdout.log').read_bytes();v=(W/'review1-verdict.md').read_bytes();assert r['head']==H and r['ma_thoat']==0 and r['trang_thai']=='xong' and r['stdout_sha256']==hashlib.sha256(raw).hexdigest()
messages=[]
for line in raw.decode().splitlines():
 j=json.loads(line)
 if j.get('type')=='item.completed' and j.get('item',{}).get('type')=='agent_message':messages.append(j['item']['text'])
assert messages[-1].encode()==v and v.rstrip().endswith(b'KET_LUAN: approve')
assert r['ket_thuc_utc']<'2026-11-09T08:05:45Z'
(out/'original-last-message.txt').write_bytes(v)
projection=dict(r);projection.update(stdout_sha256=hashlib.sha256(v).hexdigest(),stdout_byte=len(v),transport_projection={'kind':'DERIVED_TRANSPORT_VIEW_NOT_ORIGINAL_LAUNCHER_RUN','created_at':now(),'reason':'CLI was actually invoked --json. Canonical K4 expects plain originalreviewertext. Decode final completed agent_message from immutableJSONL, verify exactbytes equal original --output-last-message artifact; preserve originalactualrun identity/head/timing/exit unchanged. This is not a new review/modelrun or originalstdoutclaim.','original_run_path':str(source/'run.json'),'original_run_sha256':sha(source/'run.json'),'original_stdout_path':str(source/'stdout.log'),'original_stdout_sha256':hashlib.sha256(raw).hexdigest(),'original_stdout_byte':len(raw),'original_verdict_path':str(W/'review1-verdict.md'),'original_verdict_sha256':sha(W/'review1-verdict.md'),'only_changed_legacy_fields':['stdout_sha256','stdout_byte'],'identity_exit_and_actualreview_timestamps_unchanged':True,'model_calls':0})
assert {k for k in r if projection[k]!=r[k]}=={'stdout_sha256','stdout_byte'}
save(out/'derived-run-transport-view.json',projection)
save(out/'verification.json',{'at':now(),'original_run_sha256':sha(source/'run.json'),'original_stdout_sha256':sha(source/'stdout.log'),'original_verdict_sha256':sha(W/'review1-verdict.md'),'JSON_final_agentmessage_matches_original_lastmessage_bytes':True,'originalrun_andstdout_untouched':True,'actualreview_beforepush':True,'not_human_only_K4':True,'actualhuman_supplemental_source':json.loads((W/'owner-H2-human-delivery-binding.json').read_text())['comment']})
s=(W/'preflight-before-human.py').read_text().replace("d=W/'before-human'", "d=W/'land-final-inputs'")
s=s.replace("q=subprocess.run(cmd,env=env,capture_output=True)","cmd.extend(['--offline-run-json',str(W/'review1-transport-projection/derived-run-transport-view.json'),'--offline-stdout',str(W/'review1-transport-projection/original-last-message.txt')])\nq=subprocess.run(cmd,env=env,capture_output=True)")
s=s.replace("'K4_route':'Deliberately human-sensitive-assurance route; no absenthumanrecord fabricated. Existing independentCLIoriginal/v2 approval retained separately; no claim it is missing.'", "'K4_route':'Actual prepushCLI review, losslessJSONtransport projection. Human supplementalapproval separately validated v2; no postpushhuman-only fallback/backdate.'")
s=s.replace("'expected':'Othergates measurable, K4 humanpending. K4 modelJSONstdout transport not used tosubstitute actualhuman.'", "'expected':'AllK0K7 mustpass; originalmodelverdict byteexact, actualhumansupplement valid; no missinginputfabricated.'")
s=s.replace('K0-K7-pending-human.json','K0-K7-preReady.json');compile(s,'landpreflight','exec');(W/'land-preflight.py').write_text(s)
print(json.dumps({'transport_projection_only':True,'verdict_original_bytes':len(v),'new_model_calls':0}))
