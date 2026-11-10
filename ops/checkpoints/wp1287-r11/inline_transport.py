"""Normal inline command transport for documented pasted examples. No policy flags/settings."""
import base64
from pathlib import Path

def invocation(shell,source_root,step,arguments_file,preflight=False):
    root=Path(source_root)
    helper=(root/'documented-helper.ps1').read_text(encoding='utf-8-sig')
    cleanup=(root/'documented-cleanup.ps1').read_text(encoding='utf-8-sig')
    quote=lambda x:"'"+str(x).replace("'","''")+"'"
    prefix="$ErrorActionPreference='Stop';$env:PSModulePath=$PSHOME+'\\Modules;C:\\Program Files\\WindowsPowerShell\\Modules';\n"
    prefix+='function Need($Ok, $Msg) { if (-not $Ok) { throw "STOP[PLAYWRIGHT_ADDON_UNAVAILABLE]: $Msg" } }\n'
    code=prefix+helper+'\n'
    if preflight:
        code+="[pscustomobject]@{version=$PSVersionTable.PSVersion.ToString();edition=$PSVersionTable.PSEdition;helperLoaded=[bool](Get-Command Invoke-PwGhi);effectivePolicy=(Get-ExecutionPolicy).ToString();languageMode=$ExecutionContext.SessionState.LanguageMode.ToString();noCLIInvoked=$true}|ConvertTo-Json -Compress;exit 0"
    else:
        code+="$step="+quote(step)+";$argumentsFile="+quote(arguments_file)+";\n"
        code+='[IO.File]::WriteAllText("$env:TL_PW_RUN\\shell-version-$step.json", (@{version=$PSVersionTable.PSVersion.ToString();edition=$PSVersionTable.PSEdition}|ConvertTo-Json -Compress))\n'
        if step=='cleanup':code+=cleanup+'\nexit 0'
        else:code+="$parts=[string[]]@(Get-Content -LiteralPath $argumentsFile -Raw -Encoding UTF8|ConvertFrom-Json);Invoke-PwGhi -Ten $step -Argv $parts;exit 0"
    return [shell,'-NoProfile','-NonInteractive','-EncodedCommand',base64.b64encode(code.encode('utf-16-le')).decode()]
if __name__=='__main__':
    import sys,subprocess,json
    root=Path(__file__).resolve().parent;rows=[]
    for shell in [r'C:\Windows\System32\WindowsPowerShell\v1.0\powershell.exe',r'C:\Program Files\PowerShell\7\pwsh.exe']:
        r=subprocess.run(invocation(shell,root,'preflight','unused',True),capture_output=True,timeout=20)
        rows.append({'rc':r.returncode,'result':json.loads(r.stdout.decode('utf-8-sig')) if r.returncode==0 else None,'stderr_empty':not r.stderr})
    print(json.dumps(rows));sys.exit(0 if all(r['rc']==0 and r['result']['helperLoaded'] and r['result']['noCLIInvoked'] for r in rows) else 2)
