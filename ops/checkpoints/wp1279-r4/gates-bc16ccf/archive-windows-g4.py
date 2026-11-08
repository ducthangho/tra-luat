import pathlib,os,zipfile,hashlib,json,base64
I=pathlib.Path(r'C:\tl-win\wp1279-r4-g4-inputs');W=pathlib.Path(r'C:\tl-win\wp1279-r4-g4\final-bc16ccff3601');files=[];excluded=[]
assert (W/'measurement.json').exists() and json.loads((W/'lock-release.json').read_text())['released'] is True
for root,dirs,names in os.walk(W,followlinks=False):
 root=pathlib.Path(root);keep=[]
 for n in dirs:
  p=root/n
  if (root==W and n in ['baseline','candidate','old-h3']) or n=='.git':excluded.append({'path':p.relative_to(W).as_posix(),'reason':'actual measured Git checkout excluded'});continue
  if getattr(p.lstat(),'st_file_attributes',0)&0x400:excluded.append({'path':p.relative_to(W).as_posix(),'reason':'reparse entry never followed'});continue
  keep.append(n)
 dirs[:]=keep
 for n in names:
  p=root/n
  if getattr(p.lstat(),'st_file_attributes',0)&0x400:excluded.append({'path':p.relative_to(W).as_posix(),'reason':'reparse file not read'});continue
  if p.suffix.lower() in ['.json','.jsonl','.log','.txt','.ps1','.psm1','.py','.csv','.xml','.clixml']:files.append(p)
entries={p.relative_to(W).as_posix():{'sha256':hashlib.sha256(p.read_bytes()).hexdigest(),'bytes':p.stat().st_size} for p in files};z=I/'windows-bc16ccff3601-g4-evidence.zip'
with zipfile.ZipFile(z,'w',zipfile.ZIP_DEFLATED) as f:
 for p in files:f.write(p,p.relative_to(W).as_posix())
 f.writestr('source-byte-manifest.json',json.dumps(entries,indent=2));f.writestr('archive-excluded.json',json.dumps(excluded,indent=2))
 for n in ['windows-compare-g4.py','g4_native_evidence.py','g4-candidate-manifest.json','device-online.json','g4-candidate.bundle.b64']:f.write(I/n,'operator-inputs/'+n)
b64=base64.b64encode(z.read_bytes()).decode();(I/(z.name+'.b64')).write_text('\n'.join(b64[i:i+60000] for i in range(0,len(b64),60000)),encoding='ascii');print(json.dumps({'zip_sha256':hashlib.sha256(z.read_bytes()).hexdigest(),'bytes':z.stat().st_size,'source_files':len(files),'xml_files':sum(p.suffix.lower() in ['.xml','.clixml'] for p in files),'excluded':len(excluded),'b64_lines':(len(b64)+59999)//60000,'b64_path':str(I/(z.name+'.b64'))}))
