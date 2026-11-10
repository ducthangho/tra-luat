import pathlib,runpy,json,ctypes,subprocess,sys
R=pathlib.Path(r'C:\tl-win\wp1287-public-vm-review-20261110');M=runpy.run_path(str(R/'repo/.claude/dev/launcher.py'));H=M['_codex_home_hieu_luc']();K=M['_KhoCodex'];changed=[]
o=K.__new__(K);o.home=H;o._win_init();c,w=o.c,o.w
fn=o.a.SetFileSecurityW;fn.argtypes=[w.LPCWSTR,w.DWORD,c.c_void_p];fn.restype=w.BOOL
for label,path,directory in [('home_directory',H,True),('auth_file',H/'auth.json',False),('rejected_history_file',H/'credential-recovery.json',False)]:
 try:handle=o._win_open(path,directory=directory,security=True)
 except FileNotFoundError:continue
 try:
  try:o._win_private(handle);continue
  except OSError as e:
   if str(e)!='credential ACL grants access to another principal':raise
  sd=c.c_void_p();text=w.LPWSTR()
  try:
   assert o.a.GetSecurityInfo(handle,1,5,None,None,None,None,c.byref(sd))==0
   assert o.a.ConvertSecurityDescriptorToStringSecurityDescriptorW(sd,1,5,c.byref(text),None)
   backup=R/('credential-acl-before-'+label+'.sddl');assert not backup.exists();backup.write_text(text.value,encoding='utf-8')
  finally:
   if text:o.k.LocalFree(c.cast(text,c.c_void_p))
   if sd:o.k.LocalFree(sd)
  with o._win_security(directory=False) as sa:assert fn(str(path),0x80000004,sa.descriptor),'private_dacl_restore_failed'
  o._win_private(handle);changed.append(label)
 finally:o.k.CloseHandle(handle)
with K(H):pass
p=subprocess.run([sys.executable,str(R/'repo/.claude/dev/launcher.py'),'credential-status'],capture_output=True);assert p.returncode==0,'CANONICAL_CREDENTIAL_GATE_BLOCKED'
print(json.dumps({'credential_gate_rc':0,'private_acl_objects_restored':changed,'recursive_acl_change':False,'credential_content_changed':False,'credential_bytes_exported':False,'credential_bytes_copied':False,'other_profiles_or_accounts_changed':False}),flush=True)
