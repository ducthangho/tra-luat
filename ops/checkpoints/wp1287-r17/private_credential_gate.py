import pathlib,runpy,json,ctypes,subprocess
R=pathlib.Path(r'C:\tl-win\wp1287-public-vm-review-20261110');M=runpy.run_path(str(R/'repo/.claude/dev/launcher.py'));H=M['_codex_home_hieu_luc']();K=M['_KhoCodex'];changed=False
try:
 with K(H):pass
except OSError as e:
 if str(e)!='credential ACL grants access to another principal':raise
 o=K.__new__(K);o.home=H;o._win_init();c,w=o.c,o.w;handle=o._win_open(H,directory=True,security=True);sd=c.c_void_p();text=w.LPWSTR()
 try:
  assert o.a.GetSecurityInfo(handle,1,5,None,None,None,None,c.byref(sd))==0
  assert o.a.ConvertSecurityDescriptorToStringSecurityDescriptorW(sd,1,5,c.byref(text),None)
  backup=R/'credential-home-acl-before.sddl';assert not backup.exists();backup.write_text(text.value,encoding='utf-8')
 finally:
  if text:o.k.LocalFree(c.cast(text,c.c_void_p))
  if sd:o.k.LocalFree(sd)
  o.k.CloseHandle(handle)
 fn=o.a.SetFileSecurityW;fn.argtypes=[w.LPCWSTR,w.DWORD,c.c_void_p];fn.restype=w.BOOL
 with o._win_security(directory=False) as sa:assert fn(str(H),0x80000004,sa.descriptor),'private_directory_dacl_restore_failed'
 changed=True
 with K(H):pass
p=subprocess.run([str(pathlib.Path(__import__('sys').executable)),str(R/'repo/.claude/dev/launcher.py'),'credential-status'],capture_output=True);assert p.returncode==0,'CANONICAL_CREDENTIAL_GATE_BLOCKED'
print(json.dumps({'credential_gate_rc':0,'private_home_directory_dacl_restored':changed,'recursive_acl_change':False,'credential_bytes_exported':False,'credential_bytes_copied':False,'other_profiles_or_accounts_changed':False}),flush=True)
