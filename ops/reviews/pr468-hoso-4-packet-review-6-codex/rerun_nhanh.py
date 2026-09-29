import datetime, hashlib, json, os, time
from harness import C, OUT, replay
os.environ.update({'TMPDIR':str(OUT/'tmp'),'GIT_ALLOW_PROTOCOL':'file','GIT_CONFIG_COUNT':'1','GIT_CONFIG_KEY_0':'commit.gpgsign','GIT_CONFIG_VALUE_0':'false'})
path='ops/nhanh_don_duoc_test.py';start=datetime.datetime.now(datetime.timezone.utc).isoformat();t=time.monotonic()
rc,output=C._chay_that(path)
(OUT/'outputs/nhanh_don_duoc_test.rerun.stdout').write_text(output)
row={'path':path,'start_utc':start,'seconds':time.monotonic()-t,'rc':rc,'chars':len(output),'utf8_bytes':len(output.encode()),'sha256':hashlib.sha256(output.encode()).hexdigest(),'H_red':replay(path,output,rc=rc),'BASE_red':replay(path,output,rc=rc,base=True), 'rig_change':'process-only git commit.gpgsign=false; signing remote service is not part of isolated fixture behavior'}
(OUT/'nhanh-rerun.json').write_text(json.dumps(row,indent=2)+'\n');print(json.dumps(row))
