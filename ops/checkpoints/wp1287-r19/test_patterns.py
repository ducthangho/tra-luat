"""Execute source-extracted guards, hashes and config emitters; no npm/browser.

Run with Python SOURCE_SKILL OUTPUT_DIRECTORY. Windows exercises native PS5.1/7;
Linux exercises Bash. Private raw outputs stay in OUTPUT_DIRECTORY.
"""
import hashlib,json,os,pathlib,re,shutil,subprocess,sys,tempfile
source=pathlib.Path(sys.argv[1]).read_text(encoding='utf-8-sig')
out=pathlib.Path(sys.argv[2]);out.mkdir(parents=True,exist_ok=False)
blocks={lang:re.findall(r'```'+lang+r'\n(.*?)\n```',source,re.S) for lang in ['bash','powershell']}
assert all(len(x)==5 for x in blocks.values())
env={k:v for k,v in os.environ.items() if not k.startswith(('GIT_','TL_PW_'))}
scratch=out/'fixtures';scratch.mkdir();root=scratch/'outside'/'new'/'root'
root.parent.parent.mkdir();install=root/'install'/'0.1.0';install.mkdir(parents=True)
lock=install/'package-lock.json';side=root/'install'/'0.1.0.lock.sha256'
env.update(TL_PW_ROOT=str(root),TL_PW_INSTALL=str(install),TL_PW_RUN=str(root/'run'))
repo=scratch/'repo';bare=scratch/'bare.git'
git=shutil.which('git');assert git
for p,args in [(repo,[]),(bare,['--bare'])]:subprocess.run([git,'init',*args,str(p)],check=True,capture_output=True,env=env)
records=[]
def run(label,script,language,expected=0,custom=None,marker=None):
    local=env.copy();local.update(custom or {})
    suffix='.ps1' if language!='bash' else '.bash'
    path=out/(label+suffix);path.write_text(script,encoding='utf-8-sig' if suffix=='.ps1' else 'utf-8')
    cmd=([language,'-NoProfile','-NonInteractive','-File',str(path)] if language!='bash' else ['bash','--noprofile','--norc',str(path)])
    cp=subprocess.run(cmd,env=local,capture_output=True,timeout=30)
    (out/(label+'.stdout')).write_bytes(cp.stdout);(out/(label+'.stderr')).write_bytes(cp.stderr)
    text=cp.stdout.decode('utf-8',errors='replace')
    passed=(cp.returncode==0 if expected==0 else cp.returncode!=0) and (marker in text if marker and expected==0 else marker not in text if marker else True)
    records.append(dict(id=label,rc=cp.returncode,expected='zero' if expected==0 else 'nonzero',passed=passed,command=cmd,stdout_sha256=hashlib.sha256(cp.stdout).hexdigest(),stderr_sha256=hashlib.sha256(cp.stderr).hexdigest()))
    return cp
def seed(case,windows):
    lock.write_bytes(b'{"lockfileVersion":3}\n');digest=hashlib.sha256(lock.read_bytes()).hexdigest()
    side.write_text(digest.upper() if windows else digest+'  -\n')
    if case in ['missing_lock','both_missing']:lock.unlink()
    if case in ['missing_side','both_missing']:side.unlink()
    if case=='empty_side':side.write_bytes(b'')
    if case=='invalid_side':side.write_text('not-a-hash')
    if case=='mismatch':side.write_text('F'*64 if windows else 'f'*64+'  -\n')
    if case=='unreadable_directory':side.unlink();side.mkdir()
def clean():
    if side.is_dir():side.rmdir()
    for p in [side,lock]:
        if p.exists():p.unlink()
cases=['valid','missing_lock','missing_side','both_missing','empty_side','invalid_side','mismatch','unreadable_directory']
need="function Need($Ok,$Msg){if(-not $Ok){throw $Msg}}\n"
languages=([r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',r'C:\Program Files\PowerShell\7\pwsh.exe'] if os.name=='nt' else ['bash'])
for lang in languages:
    windows=lang!='bash';tag=('ps51' if 'WindowsPowerShell' in lang else 'ps7') if windows else 'bash'
    b=blocks['powershell' if windows else 'bash']
    if windows:
        hashcode=b[1][b[1].index('  $h = '):b[1].index('  $l = ')]
        wrapper=lambda h:need+b[1].splitlines()[0]+'\n'+h+"'PIN OK' }\n"
        guard=b[0][b[0].index('  $null = Get-Command git'):b[0].index("  foreach ($d in 'install")]
        guardwrap=lambda g:need+"& { $ErrorActionPreference='Stop'\n"+g+"'GUARD OK' }\n"
    else:
        hashcode='\n'.join(x for x in b[1].splitlines() if 'actual=' in x or '[[ "$actual"' in x)+'\n'
        wrapper=lambda h:b[1].splitlines()[0]+'\n'+h+'echo "PIN OK" )\n'
        guard=b[0][b[0].index('  command -v git'):b[0].index('  mkdir -p ')]
        guardwrap=lambda g:'( set -Eeu\n'+g+'echo "GUARD OK" )\n'
    for case in cases:
        clean();seed(case,windows)
        run(tag+'-hash-'+case,wrapper(hashcode),lang,0 if case=='valid' else 1,marker='PIN OK')
    if windows:
        clean();seed('valid',True)
        # A held exclusive handle proves actual unreadable-file behavior without ACL changes.
        held="$held=[IO.File]::Open($env:TL_PW_INSTALL+'\\package-lock.json',[IO.FileMode]::Open,[IO.FileAccess]::ReadWrite,[IO.FileShare]::None)\n"
        run(tag+'-hash-unreadable-file',held+wrapper(hashcode),lang,1,marker='PIN OK')
    clean()
    if windows:
        queries=[line for block in b[:2] for line in block.splitlines() if "'node'" in line or "'npm'" in line or "'cli'" in line]
        assert len(queries)==5
        for i,line in enumerate(queries):
            version='0.1.23' if "'cli'" in line else '11.20.0' if "'npm'" in line else 'v26.13.0'
            for rc in [0,17]:
                pre="function versionprobe { $global:LASTEXITCODE="+str(rc)+"; '"+version+"' }; $env:TL_PW_NODE='versionprobe'\n"
                run(tag+'-version-'+str(i)+'-rc'+str(rc),need+pre+line+"\n'VERSION OK'",lang,0 if rc==0 else 1,marker='VERSION OK')
        target='\n'.join(b[1].splitlines()[1:3])
        (root/'TARGET_ID').write_bytes(b'')
        run(tag+'-empty-target',need+"& { $ErrorActionPreference='Stop'\n"+target+"\n'PIN OK' }",lang,1,{'TL_PW_TARGET_ID':''},'PIN OK')
    else:
        queries=[]
        for block in b[:2]:
            for line in block.splitlines():
                if '--version' not in line or '/chrome" --version' in line:continue
                queries.extend(line.split(';') if line.count('--version')>1 else [line])
        assert len(queries)==5
        versionprobe=scratch/'versionprobe'
        for rc in [0,17]:
            versionprobe.write_text('#!/bin/sh\nif [ "$1" = --version ]; then echo v24.19.0; elif [ "$1" = npm-cli ]; then echo 11.9.0; else echo 0.1.23; fi\nexit '+str(rc)+'\n');versionprobe.chmod(0o755)
            for i,line in enumerate(queries):
                run(tag+'-version-'+str(i)+'-rc'+str(rc),'( set -Eeuo pipefail\n'+line+'\necho "VERSION OK" )',lang,0 if rc==0 else 1,{'TL_PW_NODE':str(versionprobe),'TL_PW_NPM_CLI':'npm-cli','TL_PW_CLI':'cli'},'VERSION OK')
        browser=scratch/'browser'/'chromium-1252'/'chrome-linux64'/'chrome';browser.parent.mkdir(parents=True)
        probe=next(line for line in b[1].splitlines() if '/chrome" --version' in line).split(';')[0]
        for rc in [0,17]:
            browser.write_text('#!/bin/sh\necho "Google Chrome 157.0.8103.15"\nexit '+str(rc)+'\n');browser.chmod(0o755)
            run(tag+'-browser-version-rc'+str(rc),b[1].splitlines()[0]+'\nB="'+str(scratch/'browser')+'"\n'+probe+'\necho "VERSION OK" )',lang,0 if rc==0 else 1,marker='VERSION OK')
    outside=scratch/'outside'/'never-created'/'leaf'
    for case,path,expect in [('outside',outside,0),('inside-existing',repo,1),('inside-nonexistent',repo/'new'/'leaf',1),('bare',bare,1)]:
        run(tag+'-git-'+case,guardwrap(guard),lang,expect,{'TL_PW_ROOT':str(path)},'GUARD OK')
        if case.endswith('nonexistent') or case=='outside':assert not path.exists()
    for rc,msg in [(1,'probe failed'),(128,'fatal: detected dubious ownership in repository'),(0,'true')]:
        if windows:
            stub="function git { $global:LASTEXITCODE="+str(rc)+"; Write-Output '"+msg+"' }\n"
            script=stub+guardwrap(guard)
            custom={}
        else:
            binpath=scratch/('gitstub'+str(rc));binpath.mkdir(exist_ok=True)
            exe=binpath/'git';exe.write_text('#!/bin/sh\nprintf "%s\\n" "'+msg+'"\nexit '+str(rc)+'\n');exe.chmod(0o755)
            script=guardwrap(guard);custom={'PATH':str(binpath)+os.pathsep+env['PATH']}
        custom['TL_PW_ROOT']=str(outside)
        run(tag+'-git-unrelated-'+str(rc),script,lang,1,custom,'GUARD OK')
    missingpath=scratch/'empty-bin';missingpath.mkdir(exist_ok=True)
    if windows:missing_script=guardwrap(guard);extra={'PATH':str(missingpath)}
    else:
        # Absolute Bash is needed to start while git is genuinely absent from PATH.
        missing_script=guardwrap(guard);extra={'PATH':str(missingpath)}
    if not windows:
        # run() starts bash by name; use its absolute path only for this missing-tool control.
        missing_script='PATH='+str(missingpath)+'\n'+missing_script;extra={}
    run(tag+'-git-missing',missing_script,lang,1,dict(extra,TL_PW_ROOT=str(outside)),'GUARD OK')
    run(tag+'-git-env-override',guardwrap(guard),lang,1,{'TL_PW_ROOT':str(outside),'GIT_DIR':str(repo/'.git')},'GUARD OK')
    # Execute the literal config emitter, then inspect emitted JSON; no browser commands.
    cfgdir=root/'run';cfgdir.mkdir(exist_ok=True)
    if windows:
        config=b[2][b[2].index('  $cfg = '):b[2].index('  Invoke-PwGhi 01-open')]
        emitter="$ErrorActionPreference='Stop'\n"+config
    else:
        emitter=b[2][b[2].index('  printf \'{"browser"'):b[2].index('  chay_ghi 01-open')]
    run(tag+'-config-emit',emitter,lang)
    cfg=json.loads((cfgdir/'browser.json').read_text(encoding='utf-8-sig'))
    check=lambda c:c['browser']['launchOptions']['timeout']==30000 and c.get('timeouts',{}).get('action')==10000
    records.append(dict(id=tag+'-config-values',passed=check(cfg)))
    for label,mut in [('old_launch',json.loads(json.dumps(cfg))),('missing_action',json.loads(json.dumps(cfg)))]:
        if label=='old_launch':mut['browser']['launchOptions']['timeout']=20000
        else:mut.pop('timeouts')
        records.append(dict(id=tag+'-config-mutant-'+label,passed=not check(mut)))
    # Restoring the unsafe combined missing-read comparison must be caught by the same assertion.
    seed('both_missing',windows)
    mutant=("  $h=(Get-FileHash -LiteralPath \"$env:TL_PW_INSTALL\\package-lock.json\" -Algorithm SHA256).Hash\n  Need ($h -eq (Get-Content -Raw -LiteralPath \"$env:TL_PW_ROOT\\install\\0.1.0.lock.sha256\")) 'lock'\n" if windows else '  [ "$(sha256sum < "$TL_PW_INSTALL/package-lock.json")" = "$(cat "$TL_PW_ROOT/install/0.1.0.lock.sha256")" ]\n')
    mutant_script=wrapper(mutant)
    if windows:mutant_script=mutant_script.replace("$ErrorActionPreference = 'Stop'","$ErrorActionPreference = 'Continue'")
    cp=run(tag+'-mutant-null-comparison',mutant_script,lang,0,marker='PIN OK')
    records[-1]['purpose']='mutant_survives_unsafe_implementation_and_is_rejected_by_negative_expectation'
    records[-1]['passed']=cp.returncode==0 and b'PIN OK' in cp.stdout
    # Same unrelated rc128 must expose the old any-nonzero guard.
    if windows:
        unsafe="function git { $global:LASTEXITCODE=128; Write-Output 'unrelated fatal' }; & git -C $env:TL_PW_ROOT rev-parse --is-inside-work-tree *> $null; Need ($LASTEXITCODE -ne 0) 'Git'\n"
    else:unsafe='if git -C "$TL_PW_ROOT" rev-parse --is-inside-work-tree >/dev/null 2>&1; then false; fi\n'
    cp=run(tag+'-mutant-any-nonzero',guardwrap(unsafe),lang,0,{'TL_PW_ROOT':str(repo/'missing'/'leaf')},'GUARD OK')
summary=dict(source_sha256=hashlib.sha256(source.encode()).hexdigest(),platform=sys.platform,tests=len(records),passed=sum(x['passed'] for x in records),failed=[x['id'] for x in records if not x['passed']],records=records,scope='extracted source components; no full Setup, npm, browser, cleanup matrix or full product acceptance')
(out/'summary.json').write_text(json.dumps(summary,indent=2)+'\n')
print(json.dumps({k:v for k,v in summary.items() if k!='records'}));sys.exit(0 if not summary['failed'] else 1)
