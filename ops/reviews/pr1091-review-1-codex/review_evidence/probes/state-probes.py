from pathlib import Path
import difflib
import json
import os
import shutil
import subprocess

ROOT = Path(__file__).resolve().parents[1]
PRODUCT = 'ops/vm/cap-nhat-cong-cu.ps1'
TEST = 'ops/vm/cap-nhat-cong-cu_test.ps1'
source = (ROOT/'cay-kho'/TEST).read_text()

def one(text, before, after):
    assert text.count(before) == 1, (before, text.count(before))
    return text.replace(before, after)

# Bản sao fixture thêm hai điều kiện chưa có trong suite. Đây là mô hình logic,
# không phải phép đo native NTFS. Cây vật lý, Copy-Item và hash vẫn chạy thật.
fixture = one(source, "if ($CheDo -eq 'ban-cu') {", "if ($CheDo -in 'ban-cu', 'dacl-rong', 'cay-long') {")
anchor = "    $Script:GiaCheDo = $CheDo; $Script:SuKien = [Collections.Generic.List[object]]::new()"
seed = r'''
    if ($CheDo -eq 'dacl-rong') {
        foreach ($p in @($Script:AclGia.Keys)) {
            if ($p -ne (Join-Path $env:ProgramFiles 'tra-luat-ops')) { $Script:AclGia[$p].Access = @() }
        }
    }
    if ($CheDo -eq 'cay-long') {
        $root = Join-Path $env:ProgramFiles 'tra-luat-ops'
        foreach ($relative in 'long', 'long/sau') {
            New-Item -ItemType Directory -Path (Join-Path $root $relative) | Out-Null
        }
        foreach ($relative in '.tep-an', 'long/sau/.tep-an', 'long/sau/khong-duoi') {
            [IO.File]::WriteAllText((Join-Path $root $relative), 'cu')
        }
        foreach ($relative in 'long', 'long/sau', '.tep-an', 'long/sau/.tep-an', 'long/sau/khong-duoi') {
            $Script:AclGia[(Join-Path $root $relative)] = [pscustomobject]@{
                Owner = 'BUILTIN\Administrators'; Access = @(New-QuyenGia 'BUILTIN\Users' 'Modify')
            }
        }
    }
'''
fixture = one(fixture, anchor, seed+anchor)
fixture = one(fixture, 'loi = $loi; su_kien = @($Script:SuKien);', 'acl = $Script:AclGia; loi = $loi; su_kien = @($Script:SuKien);')

# Mô hình thu hẹp: wildcard không /T chỉ chọn con trực tiếp; /reset đọc cha
# trực tiếp, duyệt từ trên xuống. ACL của con được xem là protected trước reset.
corrected = one(fixture, 'foreach ($key in @($Script:AclGia.Keys)) {', 'foreach ($key in @($Script:AclGia.Keys | Sort-Object Length)) {')
corrected = one(corrected, '$khop = if ($chiCon) { $laCon } else {', "$khop = if ($chiCon) { $laCon -and (($DoiSo -contains '/T') -or (Split-Path -Parent $key) -eq $goc) } else {")
corrected = one(corrected, "if ($DoiSo -contains '/reset') { $node.Access = @($Script:AclGia[$goc].Access); continue }", "if ($DoiSo -contains '/reset') { $node.Access = @($Script:AclGia[(Split-Path -Parent $key)].Access); continue }")
corrected = one(corrected, "if (-not ($laCon -and $DoiSo[$i] -match '\\((OI|CI)\\)'))", "if (-not ((Test-Path -LiteralPath $key -PathType Leaf) -and $DoiSo[$i] -match '\\((OI|CI)\\)'))")

extra_tests = r'''
    Ca 'dk_chay_sua_tep_dacl_rong_truoc_khi_chep' {
        $k = Invoke-DangKyGia 'dacl-rong'
        (& $dungLaiDung $k)
    }
    Ca 'dk_chay_reset_ca_cay_long_va_tep_an' {
        $k = Invoke-DangKyGia 'cay-long'
        $bad = @($k.acl.Values | ForEach-Object { Test-AclChiAdminGhi $_.Owner $_.Access })
        (& $dungLaiDung $k) -and $k.acl.Count -eq 9 -and $bad.Count -eq 0
    }
'''
hint = one(corrected, "    Ca 'dk_chay_chep_du_ba_tep'", extra_tests+"    Ca 'dk_chay_chep_du_ba_tep'")
(ROOT/'copies/hint/ops/vm').mkdir(parents=True, exist_ok=True)
for path in [PRODUCT, TEST, 'ops/vm/README.md', 'ops/cong_cu.yaml', 'requirements.txt']:
    dest = ROOT/'copies/hint'/path
    dest.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(ROOT/'cay-kho'/path, dest)
(ROOT/'copies/hint'/TEST).write_text(hint)
delta = ''.join(difflib.unified_diff(source.splitlines(True), hint.splitlines(True), fromfile=TEST, tofile=TEST))
(ROOT/'HINT.patch').write_text('# chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit\n'+delta)

def harness(text):
    start = text.index("$DungLai = 'OFFLINE-DUNG-TRUOC-MAT-KHAU'")
    end = text.index("    $kSach = Invoke-DangKyGia 'sach'", start)
    definitions = text[start:end]
    return r'''
param([string]$Product, [string]$Mode, [string]$OutFile)
$ErrorActionPreference = 'Stop'
$Here = Split-Path -Parent $Product
. $Product -NapHam
$pfCu = $env:ProgramFiles
''' + definitions + r'''
    $k = Invoke-DangKyGia $Mode
    $events = @($k.su_kien | ForEach-Object {
        [ordered]@{ type=$_.loai; target=$_.dich; argv=$_.doi_so }
    })
    $states = @($k.acl.Keys | Sort-Object | ForEach-Object {
        $node = $k.acl[$_]
        [ordered]@{ path=$_; owner=$node.Owner; access=$node.Access; violations=@(Test-AclChiAdminGhi $node.Owner $node.Access) }
    })
    [ordered]@{ mode=$Mode; error=$k.loi; tasks=$k.tac_vu.Count; files=$k.tep; states=$states; events=$events } |
        ConvertTo-Json -Depth 12 | Set-Content -LiteralPath $OutFile -Encoding utf8NoBOM
} finally {
    $env:ProgramFiles = $pfCu
    $env:COMPUTERNAME = $cuMay
}
'''

(ROOT/'probes/state-original-model.ps1').write_text(harness(fixture))
(ROOT/'probes/state-recursive-model.ps1').write_text(harness(corrected))

cases = [
    ('head_empty', 'control', 'dacl-rong', 'original'),
    ('no_reset_empty', 'no_reset', 'dacl-rong', 'original'),
    ('after_copy_empty', 'reset_after_copy', 'dacl-rong', 'original'),
    ('head_nested', 'control', 'cay-long', 'recursive'),
    ('no_T_nested_original_model', 'reset_no_T', 'cay-long', 'original'),
    ('no_T_nested_recursive_model', 'reset_no_T', 'cay-long', 'recursive'),
]
results = []
for name, variant, mode, model in cases:
    out = ROOT/'evidence'/f'{name}.json'
    proc = subprocess.run([str(ROOT/'pwsh/pwsh'), '-NoProfile', '-File', str(ROOT/f'probes/state-{model}-model.ps1'), '-Product', str(ROOT/'copies'/variant/PRODUCT), '-Mode', mode, '-OutFile', str(out)], capture_output=True, text=True, timeout=60)
    (ROOT/'evidence'/f'{name}.log').write_text(proc.stdout+proc.stderr)
    assert proc.returncode == 0, (name, proc.stdout, proc.stderr)
    data = json.loads(out.read_text())
    row = dict(name=name, rc=proc.returncode, error=data['error'], tasks=data['tasks'], nodes=len(data['states']), bad_nodes=sum(bool(n['violations']) for n in data['states']))
    results.append(row)
    print(json.dumps(row, ensure_ascii=False), flush=True)
(ROOT/'evidence/state-probes.json').write_text(json.dumps(results, ensure_ascii=False, indent=2)+'\n')
