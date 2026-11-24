import importlib.util,pathlib,json,copy
R=pathlib.Path.cwd(); W=R.parent/'work'
s=importlib.util.spec_from_file_location('t',R/'ops/land_evidence_nguon_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
rows=[]
def check(label,doc,prov,rc,lines):
 got,out=t.chay(json.dumps(doc,ensure_ascii=False),prov,doi_chieu=t.DOI_CHIEU)
 actual=t.dong_l8(out); ok=(got,actual)==(rc,lines)
 rows.append({'label':label,'expected_rc':rc,'actual_rc':got,'expected_l8':lines,'actual_l8':actual,'passed':ok})
 print(label,got,actual,'PASS' if ok else 'FAIL',flush=True)
 if not ok: print(out,flush=True)
p=t.prov_that()
for sep in (' ','\t','—','-',':','(',',','.',';'):
 check('separator '+repr(sep),{'gate_output':'passed'+sep+' '+t.DG},p,0,[])
for k in ('gate_output_nguon','gate_output_nguon_va_gioi_han','moc_gate_output_rc_disposition','gate2output'):
 check('key '+k,{k:'unknown'},None,0,[])
for key in ('root','packet','dated'):
 for value in (True,1):
  doc=({'landed':value} if key=='root' else {'trang_thai_packet':{'landed':value},'post_merge_checks':[{'name':'g'}],'bookkeeping':[{'item':'x'}]} if key=='packet' else {'landed_20261124':{'landed':value}})
  check('landed '+key+' '+repr(value),doc,None,1 if value is True or key=='packet' else 0,['$: landed_khong_loi_khai_gate_output'] if value is True else [])
url='https://github.com/ducthangho/tra-luat/issues/1236#issuecomment-123';sha='d8cf2ab57f9f25a93cefedcebfb315826b6b78fe'
dong=f'mien_gate_output: {sha} os=ubuntu-latest ly_do=fixture review han=2026-12-31'
rb={'html_url':url,'user':{'login':'ducthangho'},'author_association':'OWNER','body':dong}
claim=f'owner_waived — {url} {sha}'
def waiver(label,r=rb,c=claim,why=None,landed=False):
 doc={'gate_output':c}
 if landed: doc['landed']=True
 check('waiver '+label,doc,{'readback-review-issuecomment-123.json':json.dumps(r)},1 if why else 0,['$.gate_output: waiver_khong_co_can_cu:'+why] if why else [])
waiver('valid',landed=True)
waiver('two URLs',c=claim+' '+url,why='url')
waiver('strip',r=dict(rb,body=' \t'+dong+'\t '))
waiver('trailing text',r=dict(rb,body=dong+' extra'),why='dong_mien')
waiver('wrong author',r=dict(rb,author_association='MEMBER'),why='tac_gia')
waiver('html before author',r=dict(rb,html_url=url+'0',author_association='MEMBER'),why='html_url')
waiver('os before sha',r=dict(rb,body=dong.replace('ubuntu-latest','windows-latest')),c=f'owner_waived — {url}',why='os')
waiver('date before os',r=dict(rb,body=dong.replace('ubuntu-latest','windows-latest').replace('2026-12-31','2026-02-30')),why='han')
(W/'matrix-probes.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('TOTAL',sum(r['passed'] for r in rows),'/',len(rows)); assert all(r['passed'] for r in rows)
