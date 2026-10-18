exec(open('/tmp/wp812_r6_probe.py').read().split('for name,path,value in ')[0])
# Native Linux filename with a single byte that is not UTF-8; content stays unchanged.
q=d/('receipt-'+chr(0xdc80)+'.yaml');q.write_bytes(p.read_bytes());(sd/'wp55.json').write_bytes(before)
rc,_,e=t.run(t.CANONICAL,['record-review','--packet',55,'--provider','codex','--verdict','approve','--reviewed-sha',bn['reviewed_sha'],'--codex-call','g1','--bien-nhan',q,'--root',w],sd)
raw=(sd/'wp55.json').read_bytes();print(json.dumps(dict(probe='receipt-native-nonutf8-filename',rc=rc,bytes_before=len(before),bytes_after=len(raw),unchanged=raw==before,traceback=b'Traceback' in e,error=e.decode('utf-8','replace')),ensure_ascii=True),flush=True)
# Oversized single argv item (same logical field as the NUL probe).
dd=out/'oversize-ws';dd.mkdir();rc,ss,ee,bb=t._r812(t.Ctx(t.CANONICAL,dd),'lease',truoc_lease=lambda w:t._r812_doi_lease(w,{'write_set':['x/'+'a'*140000]}));report('write_set_argv_size',rc,ss,ee,bb)
# A malformed canonical API must also fail with a controlled rc.
def bad_api(w):
 pp=w/'ops/bien_nhan_v2.py';pp.write_text(pp.read_text()+'\nASSURANCE_CAN_DOC_LAP = None\n');t._g(w,'add','ops/bien_nhan_v2.py');t._g(w,'commit','-qm','ordinary incompatible API fixture');t._g(w,'push','-q','origin','master')
dd=out/'api-type';dd.mkdir();rc,ss,ee,bb=t._r812(t.Ctx(t.CANONICAL,dd),'lease',truoc_lease=bad_api);report('source-api-type',rc,ss,ee,bb)
print(json.dumps({'scratch':str(out)}),flush=True)
