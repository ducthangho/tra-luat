import datetime, hashlib, json, os, pathlib, time
from harness import C, OUT, replay
os.environ['TMPDIR'] = str(OUT/'tmp')
os.environ['GIT_ALLOW_PROTOCOL'] = 'file'
rows=[]
for path in C.MOI:
    start=datetime.datetime.now(datetime.timezone.utc).isoformat()
    t=time.monotonic()
    print('START', path, start, flush=True)
    rc, output=C._chay_that(path)
    elapsed=time.monotonic()-t
    log=OUT/'outputs'/(pathlib.Path(path).stem+'.stdout')
    log.write_text(output)
    row=dict(path=path, start_utc=start, seconds=elapsed, rc=rc, chars=len(output), utf8_bytes=len(output.encode()), sha256=hashlib.sha256(output.encode()).hexdigest(),
        H_red=replay(path,output,rc=rc), BASE_red=replay(path,output,rc=rc,base=True), output=str(log.relative_to(OUT)))
    rows.append(row)
    (OUT/'real-results.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
    print(json.dumps(row,ensure_ascii=False),flush=True)
print('DONE', len(rows), flush=True)
