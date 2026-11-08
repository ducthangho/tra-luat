import pathlib,json,hashlib,xml.etree.ElementTree as ET,re
class MissingNestedArtifact(Exception):pass
def sha(p):return hashlib.sha256(pathlib.Path(p).read_bytes()).hexdigest()
def wp(p):return pathlib.PureWindowsPath(str(p))
def under(p,r):return wp(p).is_relative_to(wp(r))
def read(p):return json.loads(pathlib.Path(p).read_text(encoding='utf-8-sig'))
def decode_xml(p):
 refs={}
 def tag(e):return e.tag.rsplit('}',1)[-1]
 def dec(e):
  t=tag(e)
  if t=='Ref':return refs[e.attrib['RefId']]
  if t=='Nil':return None
  if t=='B':return e.text=='true'
  if t in ['I16','I32','I64','U16','U32','U64','By','SB']:return int(e.text)
  if t=='S':return re.sub(r'_x([0-9a-fA-F]{4})_',lambda m:chr(int(m[1],16)),e.text or '')
  if t=='Obj':
   dct=next((x for x in e if tag(x)=='DCT'),None);lst=next((x for x in e if tag(x) in ['LST','IE','QUE','STK']),None);members=next((x for x in e if tag(x) in ['MS','Props']),None)
   o={} if dct is not None or members is not None else []
   if 'RefId' in e.attrib:refs[e.attrib['RefId']]=o
   if dct is not None:
    for en in dct:
     kv=list(en);o[dec(kv[0])]=dec(kv[1])
   elif lst is not None:o.extend(dec(x) for x in lst)
   elif members is not None:
    for x in members:o[x.attrib['N']]=dec(x)
   return o
  raise AssertionError('Unsupported CLIXML data node '+t)
 root=ET.fromstring(pathlib.Path(p).read_text(encoding='utf-8-sig'));return dec(next(iter(root)))
def verify_nested(rep,map_path,expect_valid=True):
 ev=rep['evidence'];assert ev['schema']=='px.evidence.v1';ed=ev['dir'];assert ev['check']['status']=='ok';assert not under(ed,rep['scratch']);assert not under(ed,str(wp(rep['module_path']).parent))
 arts=ev['artifacts'];lookup={};rows=[];endpoint_rows=[];forbidden=[rep['scratch'],str(wp(rep['module_path']).parent)]
 for a in arts:
  assert a['present'] is True and a['rel'] and '..' not in wp(a['rel']).parts;assert wp(ed)/wp(a['rel'])==wp(a['path']);assert under(a['path'],ed) and not any(under(a['path'],f) for f in forbidden)
  p=map_path(a['path'])
  if not p.is_file():raise MissingNestedArtifact('MISSING_NESTED_ARTIFACT:'+a['role']+':'+a['rel'])
  assert sha(p)==a['sha256'] and p.stat().st_size==a['bytes'];key=(a['child'],a['rel']);assert key not in lookup;lookup[key]=a
 for c in rep['children']:
  linked=[lookup[(c['index'],n)] for n in c['artifacts']];byrole={x['role']:x for x in linked};assert len(byrole)==len(linked);cmd=c['command'];assert c['index']>=0
  required={'output'}
  if c['kind']=='endpoint':required|={'endpoint-script','endpoint-input','endpoint-report'}
  elif c['kind']=='fresh-process wrapper':required|={'wrapper-script','wrapper-input','wrapper-report'}
  elif c['kind'].startswith('counterexample '):required|={'cx-module','cx-wrapper','cx-config-module','cx-report'}
  else:raise AssertionError('Unknown child kind '+c['kind'])
  assert required<=set(byrole);assert byrole['output']['sha256']==c['output_sha256']
  def arg(flag):return cmd[cmd.index(flag)+1]
  if c['kind'].startswith('counterexample '):
   assert wp(arg('-ModulePath'))==wp(byrole['cx-module']['path']) and wp(arg('-ReportPath'))==wp(byrole['cx-report']['path']);continue
  role='endpoint' if c['kind']=='endpoint' else 'wrapper';assert wp(arg('-File'))==wp(byrole[role+'-script']['path']);assert wp(arg('-In' if role=='endpoint' else '-ArgsFile'))==wp(byrole[role+'-input']['path']);assert wp(arg('-Out'))==wp(byrole[role+'-report']['path']);assert arg('-Culture')==rep['test_culture']
  raw=read(map_path(byrole[role+'-report']['path']));assert raw['ps_version']==c['ps_version'] and raw['ps_edition']==c['ps_edition'] and raw['culture']==raw['ui_culture']==rep['test_culture'];assert str(raw['codepage'])==str(c['codepage'])
  if role=='endpoint':
   assert c['rc']==0;payload=decode_xml(map_path(byrole['endpoint-input']['path']));assert isinstance(payload['Body'],str) and 'param($Request)' in payload['Body'];items={x['Name']:x['Envelope'] for x in payload['Items']};rr={x['name']:x for x in raw['rows']};assert set(items)==set(rr)
   for name in ['whatif-handshake','whatif-status']:
    e=items[name];row=rr[name];assert type(e['WhatIf']) is bool and e['WhatIf'] is True and row['received_whatif']=='True' and row['received_whatif_type']=='System.Boolean' and row['ambient_whatif'] is False
    # A deliberate CX03 bypass is allowed to fail the assertion in its child report; it is not a positive WhatIf proof.
    if expect_valid:assert row['result']['dryRun'] is True and row['result']['dispatched'] is False and row['imported_before']==row['imported_after']==0
   for name in ['positive-handshake','valid-com-lpt-handshake']:
    row=rr[name];assert row['ambient_whatif'] is False and row['received_whatif']=='False' and row['received_whatif_type']=='System.Boolean'
    if expect_valid:assert isinstance(row['result'],dict) and row['result']['outcome']=='ok' and row['result']['dryRun'] is False and row['result']['data']['moduleSha256']==items[name]['ModuleSha256'] and row['result']['data']['configModuleSha256']==items[name]['ConfigModuleSha256']
   endpoint_rows.append({'runtime':raw['ps_edition'],'version':raw['ps_version'],'codepage':raw['codepage'],'valid_path_result':rr['valid-com-lpt-handshake']['result'],'valid_path_fqid':rr['valid-com-lpt-handshake']['fqid'],'whatif_rows':{n:rr[n] for n in ['whatif-handshake','whatif-status']},'payload_body_sha256':hashlib.sha256(payload['Body'].encode('utf-8')).hexdigest(),'raw_report_sha256':byrole['endpoint-report']['sha256']})
  rows.append({'kind':c['kind'],'index':c['index'],'roles':sorted(byrole),'rc':c['rc']})
 return {'artifacts_verified':len(arts),'direct_children_verified':rows,'endpoint_observations':endpoint_rows}
