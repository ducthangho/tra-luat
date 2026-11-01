from pathlib import Path
import subprocess,json,difflib
R=Path(__file__).resolve().parents[1]
s=(R/'probes/state-head-model.ps1').read_text()
def one(t,a,b):
 assert t.count(a)==1,(a,t.count(a))
 return t.replace(a,b)
# Trạng thái hidden-only không có ba tệp thường để giúp điều kiện có con.
seed=r'''
    if ($CheDo -eq 'chi-an') {
        $f = Join-Path (Join-Path $env:ProgramFiles 'tra-luat-ops') '.only-hidden'
        [IO.File]::WriteAllText($f, 'cu')
        $Script:AclGia[$f] = [pscustomobject]@{ Owner = 'BUILTIN\Administrators'; Access = @(New-QuyenGia 'BUILTIN\Users' 'Modify') }
    }
'''
s=one(s,'    $Script:GiaCheDo = $CheDo;',seed+'    $Script:GiaCheDo = $CheDo;')
s=one(s,"$CheDo -in 'ban-cu', 'dacl-rong', 'cay-long'","$CheDo -in 'ban-cu', 'dacl-rong', 'cay-long', 'reset-hong', 'enum-hong'")
s=one(s,"        $Script:SuKien.Add([pscustomobject]@{ loai = 'icacls'; doi_so = $DoiSo })", "        $Script:SuKien.Add([pscustomobject]@{ loai = 'icacls'; doi_so = $DoiSo })\n        if ($Script:GiaCheDo -eq 'reset-hong' -and $DoiSo -contains '/reset') { throw 'RESET-FAIL-INJECTED' }")
s=one(s,'        $Script:SuKien.Add([pscustomobject]@{ loai = \'chep\'; dich = "$Destination" })','        $Script:SuKien.Add([pscustomobject]@{ loai = \'chep\'; dich = "$Destination" })\n        if ($Script:GiaCheDo -eq \'copy-khoa\') { throw [IO.IOException]::new(\'SHARING-LOCK-INJECTED\') }')
wrapper=r'''
    function Get-ChildItem {
        [CmdletBinding()]
        param([string]$LiteralPath, [switch]$Force, [switch]$Recurse, $Attributes, [switch]$File)
        if ($Script:GiaCheDo -eq 'enum-hong' -and $LiteralPath -eq $Script:ThuMucCaiDat -and $Force -and -not $Recurse) {
            throw [IO.IOException]::new('ENUM-FAIL-INJECTED')
        }
        Microsoft.PowerShell.Management\Get-ChildItem @PSBoundParameters
    }
'''
s=one(s,'    $k = Invoke-DangKyGia $Mode',wrapper+'    $k = Invoke-DangKyGia $Mode')
(R/'probes/state-edges.ps1').write_text(s)
product=R/'copies/head/ops/vm/cap-nhat-cong-cu.ps1'
# Mutant chẩn đoán riêng cho branch có con; không viết vào HEAD.
p=product.read_text(); anchor='Get-ChildItem -LiteralPath $Script:ThuMucCaiDat -Force'; p=one(p,anchor,'Get-ChildItem -LiteralPath $Script:ThuMucCaiDat')
mutant=R/'copies/edge-no-Force/ops/vm/cap-nhat-cong-cu.ps1'; mutant.parent.mkdir(parents=True,exist_ok=True); mutant.write_text(p)
# GocKho và bản kê lấy từ cây head bằng Resolve-Path của harness; mutant chỉ đổi product.
(R/'evidence/edge-no-Force.patch').write_text(''.join(difflib.unified_diff(product.read_text().splitlines(True),p.splitlines(True),fromfile='ops/vm/cap-nhat-cong-cu.ps1',tofile='ops/vm/cap-nhat-cong-cu.ps1')))
# Cần đủ tệp nguồn để mutant không đỏ vì thiếu fixture.
import shutil
for rel in ['ops/cong_cu.yaml','requirements.txt']:
 d=R/'copies/edge-no-Force'/rel; d.parent.mkdir(parents=True,exist_ok=True); shutil.copyfile(R/'copies/head'/rel,d)
results=[]
for name,mode,path in [('head_hidden_only','chi-an',product),('no_Force_hidden_only','chi-an',mutant),('reset_failure','reset-hong',product),('enumeration_failure','enum-hong',product),('copy_sharing_failure','copy-khoa',product)]:
 out=R/f'evidence/{name}.json'
 args=[str(R/'pwsh/pwsh'),'-NoProfile','-File',str(R/'probes/state-edges.ps1'),'-Product',str(path),'-Mode',mode,'-OutFile',str(out)]
 proc=subprocess.run(args,capture_output=True,text=True,timeout=60)
 (R/f'evidence/{name}.log').write_text(proc.stdout+proc.stderr)
 assert proc.returncode==0,(name,proc.stdout,proc.stderr)
 d=json.loads(out.read_text())
 row=dict(name=name,rc=proc.returncode,error=d['error'],tasks=d['tasks'],nodes=len(d['states']),bad_nodes=sum(bool(n['violations']) for n in d['states']),copies=sum(e['type']=='chep' for e in d['events']),resets=sum(e['type']=='icacls' and '/reset' in e['argv'] for e in d['events']))
 results.append(row);print(json.dumps(row,ensure_ascii=False),flush=True)
(R/'evidence/edge-probes.json').write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
