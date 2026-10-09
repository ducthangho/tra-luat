#requires -Version 7.0
$ErrorActionPreference = 'Stop'
# -WindowStyle exists only on Windows; splat it so the same file runs unchanged on Linux pwsh.
$hidden = @{}
if ($IsWindows) { $hidden['WindowStyle'] = 'Hidden' }
# WP710 g4: where the wrapper can PROVE a step's tree gone - Linux enumerates it, Windows contains it in a Job Object.
$contained = $IsLinux -or $IsWindows
$root = Join-Path ([IO.Path]::GetTempPath()) ('wp710-' + [guid]::NewGuid().ToString('N'))
New-Item -ItemType Directory -Path $root | Out-Null
$script = Join-Path $PSScriptRoot 'nlm-credential-refresh.ps1'
$cases = 0
try {
    $source = @'
import json, os, subprocess, sys, time
op = sys.argv[1] if len(sys.argv) > 1 else "stage"
if op == "--version" and os.environ.get("WP710_MODE") == "version_linger":
    # WP714 round 3: the version probe leaves a pipe-holding grandchild that cleared the operation marker.
    env = {k: v for k, v in os.environ.items() if k != "TRA_LUAT_NLM_OP"}
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"], env=env)
    with open(os.environ["WP714_LINGER_PID"], "w") as f:
        f.write(str(child.pid))
if op == "--version":
    print("fake-nlm 1.0")
    sys.exit(0)
tag = os.environ.get("WP710_TAG", "")
def note(kind):
    with open(os.environ["WP710_LOG"], "a", encoding="utf-8") as log:
        log.write(f"{kind}:{op}:{os.getpid()}:{tag}\n")
    if os.environ.get("WP710_TIMELOG"):
        with open(os.environ["WP710_TIMELOG"], "a", encoding="utf-8") as tlog:
            tlog.write(f"{kind} {op} {time.time()}\n")
note("start")
if op == "stage" and os.environ.get("WP710_ENVLOG"):
    with open(os.environ["WP710_ENVLOG"], "w", encoding="utf-8") as elog:
        elog.write(os.environ.get("TL_NOTEBOOK_ID", "<absent>") + "|" + os.environ.get("TL_CANARY_NOTEBOOK_ID", "<absent>"))
mode = os.environ.get("WP710_MODE", "ok")
if mode == "stdin_eof":
    try:
        if sys.stdin.buffer.read(1):
            print("STDIN_NOT_EOF", file=sys.stderr)
            sys.exit(91)
    except OSError:
        print("STDIN_NOT_READABLE", file=sys.stderr)
        sys.exit(92)
if mode == "leak_all":
    print("SECRET_SENTINEL", file=sys.stderr)
    if op != "notebook":
        print("SECRET_SENTINEL")
if mode == "beat":
    for _ in range(int(os.environ.get("WP710_DELAY", "0")) // 100):
        note("beat")
        time.sleep(0.1)
else:
    time.sleep(int(os.environ.get("WP710_DELAY", "0")) / 1000)
if mode == "timeout" and op == "auth":
    time.sleep(5)
if mode == "timeout_canary" and op == "notebook":
    time.sleep(5)
if mode in ("descendant_exit", "descendant_scrubbed_exit") and op == "auth":
    child_code = "import os,time;[(open(os.environ['WP714_BEAT_FILE'],'a').write(str(time.time())+'\\n'),time.sleep(0.1)) for _ in range(300)]"
    env = {k: v for k, v in os.environ.items() if k != "TRA_LUAT_NLM_OP"} if mode == "descendant_scrubbed_exit" else dict(os.environ)
    child = subprocess.Popen([sys.executable, "-c", child_code], env=env)
    with open(os.environ["WP714_CHILD_PID_FILE"], "w") as f:
        f.write(str(child.pid))
    sys.exit(0)
if mode == "linger" and op == "auth":
    child = subprocess.Popen([sys.executable, "-c", "import time; time.sleep(20)"])
    if os.environ.get("WP714_LINGER_PID"):
        with open(os.environ["WP714_LINGER_PID"], "w") as f:
            f.write(str(child.pid))
    sys.exit(0)
if mode == "daemon" and op == "auth":
    # A descendant that drops the redirected pipes and keeps working after the CLI returned rc 0.
    beat = "import os,time;[(open(os.environ['WP714_BEAT_FILE'],'a').write(str(time.time())+'\\n'),time.sleep(0.1)) for _ in range(300)]"
    child = subprocess.Popen([sys.executable, "-c", beat], stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(os.environ["WP714_CHILD_PID_FILE"], "w") as f:
        f.write(str(child.pid))
    time.sleep(0.5)
    sys.exit(0)
if mode == "hang_orphan" and op == "auth":
    # WP714 round 3: an orphan without pipes (its parent already exited), then the CLI itself hangs past the budget.
    inner = ("import os, subprocess, sys; c = subprocess.Popen([sys.executable, '-c', 'import time; time.sleep(20)'], "
             "stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL); "
             "open(os.environ['WP714_LINGER_PID'], 'w').write(str(c.pid))")
    subprocess.run([sys.executable, "-c", inner], stdin=subprocess.DEVNULL, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(5)
if mode in ("scrub_daemon", "scrub_daemon_hold") and op == "auth":
    # WP714 round 3: like `daemon`, but the descendant also CLEARED the operation marker from its environment.
    # WP714 round 4, scrub_daemon_hold: the CLI stays a little longer, so a test can kill the owner meanwhile.
    beat = "import os,time;[(open(os.environ['WP714_BEAT_FILE'],'a').write(str(time.time())+'\\n'),time.sleep(0.1)) for _ in range(300)]"
    env = {k: v for k, v in os.environ.items() if k != "TRA_LUAT_NLM_OP"}
    child = subprocess.Popen([sys.executable, "-c", beat], env=env, stdin=subprocess.DEVNULL,
                             stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    with open(os.environ["WP714_CHILD_PID_FILE"], "w") as f:
        f.write(str(child.pid))
    time.sleep(1.5 if mode == "scrub_daemon_hold" else 0.5)
    sys.exit(0)
if mode == "err_conn_reset" and op == "auth":
    print("Error running `nlm auth refresh`: connection reset by peer", file=sys.stderr)
    sys.exit(1)
if mode == "err_login_hint" and op == "auth":
    print("network unreachable; if this persists run `nlm login`", file=sys.stderr)
    sys.exit(1)
if mode == "err_traceback" and op == "auth":
    print('Traceback (most recent call last):\n  File "/x/nlm/auth/refresh.py", line 9\nValueError: boom', file=sys.stderr)
    sys.exit(1)
if mode == "err_line401" and op == "auth":
    print('Traceback (most recent call last):\n  File "/x/nlm/auth/refresh.py", line 401\nKeyError: cookies', file=sys.stderr)
    sys.exit(1)
if mode == "err_mixed" and op == "auth":
    print("Authentication expired after connection reset by peer", file=sys.stderr)
    sys.exit(1)
if mode == "err_http401" and op == "auth":
    print("HTTP 401 Unauthorized", file=sys.stderr)
    sys.exit(1)
if mode == "err_503" and op == "auth":
    print("503 Service Unavailable", file=sys.stderr)
    sys.exit(1)
if mode == "auth_second" and op == "auth":
    counter = os.path.join(os.path.dirname(os.environ["WP710_LOG"]), "auth-count.txt")
    seen = int(open(counter).read()) if os.path.exists(counter) else 0
    open(counter, "w").write(str(seen + 1))
    if seen >= 1:
        print("Authentication expired", file=sys.stderr)
        sys.exit(7)
if mode == "auth" and op == "auth":
    print("auth expired SECRET_SENTINEL", file=sys.stderr)
    sys.exit(7)
if mode == "network" and op == "notebook":
    print("network failure SECRET_SENTINEL", file=sys.stderr)
    sys.exit(8)
if mode == "stage" and op == "stage":
    print("SECRET_SENTINEL", file=sys.stderr)
    sys.exit(9)
if mode == "stage_flag" and op == "stage":
    # g5: the stage command ran to the end; the flag lets a projection make ITS job count unreadable afterwards.
    with open(os.environ["WP710_FLAG"], "w") as f:
        f.write("1")
if op == "notebook":
    if mode == "empty":
        print("{}")
    elif mode == "wrongcase":
        print(json.dumps({"id": sys.argv[3].lower(), "title": "Test"}))
    elif mode in ("title_bool", "title_array", "title_object", "title_space", "id_array", "conflict_id"):
        body = {"id": sys.argv[3], "title": "Canary"}
        if mode == "title_bool": body["title"] = True
        elif mode == "title_array": body["title"] = ["Canary"]
        elif mode == "title_object": body["title"] = {"text": "Canary"}
        elif mode == "title_space": body["title"] = "   "
        elif mode == "id_array": body["id"] = [sys.argv[3]]
        else: body.update(id="NB-OTHER-9999", notebook_id=sys.argv[3])
        print(json.dumps(body))
    elif mode in ("multi", "multi_same", "dup_id", "case_key", "ok_false", "error_set", "data_wrapped", "singleton", "title_date"):
        good = {"id": sys.argv[3], "title": "Canary"}
        print({
            "multi": json.dumps([good, {"id": "NB-OTHER-9999", "title": "Other"}]),
            "multi_same": json.dumps([good, good]),
            "dup_id": '{"id": "NB-OTHER-9999", "id": "' + sys.argv[3] + '", "title": "Canary"}',
            "case_key": json.dumps({"id": sys.argv[3], "ID": "NB-OTHER-9999", "title": "Canary"}),
            "ok_false": json.dumps(dict(good, ok=False)),
            "error_set": json.dumps(dict(good, error="offline failure")),
            "data_wrapped": json.dumps({"data": good}),
            "singleton": json.dumps([good]),
            "title_date": json.dumps({"id": sys.argv[3], "title": "2026-01-01T00:00:00"}),
        }[mode])
    elif mode.startswith("control_title_") or mode.startswith("control_name_"):
        # lop: stage-canary-true-khi-than-rong-hoac-sai-id
        key = "title" if mode.startswith("control_title_") else "name"
        print(json.dumps({"id": sys.argv[3], key: chr(int(mode.rsplit("_", 1)[1], 16))}))
    elif mode == "bom_canary":
        # bytes, not print(): on a Windows console code page (cp1258 measured) print cannot encode U+FEFF and the
        # fake would die with rc 1, turning this case into a refresh-style failure instead of a BOM in the body.
        sys.stdout.buffer.write(("\ufeff" + json.dumps({"id": sys.argv[3], "title": "Canary"}) + "\n").encode("utf-8"))
    elif mode.startswith("transport_"):
        # WP714 round 4: what nlm_cli._run + _strip_keyring do to stdout before the Python stage command judges it.
        nb = sys.argv[3]
        sys.stdout.buffer.write({
            "transport_keyring_noise": "Using keyring backend: fake\n" + json.dumps({"id": nb, "title": "Canary"}) + "\n",
            "transport_crlf_pretty": '{\r\n  "id": "' + nb + '",\r\n  "title": "Canary"\r\n}\r\n',
            "transport_ff_between": '{"id":"' + nb + '",\f"title":"Canary"}\n',
            "transport_u2028_title": '{"id":"' + nb + '","title":"Ca\u2028nary"}\n',
            "transport_nel_title": '{"id":"' + nb + '","title":"Ca\u0085nary"}\n',
            "transport_keyring_title": '{\n "id": "' + nb + '",\n "name": "N",\n "title": "using keyring backend"\n}\n',
            "transport_bad_utf8_title": None,
        }[mode].encode("utf-8") if mode != "transport_bad_utf8_title" else
            b'{"id":"' + nb.encode() + b'","title":"\xc0\xa2"}\n')
    elif mode in ("nan_meta", "overflow_meta", "surrogate_title", "surrogate_key", "surrogate_meta", "dup_nested", "deep65", "meta_ok"):
        # WP714 round 3: documents the Python reader (json.loads) used to accept and System.Text.Json reads
        # differently. Raw text: json.dumps cannot write most of these.
        head = '{"id":"' + sys.argv[3] + '","title":"Canary"'
        print({
            "nan_meta": head + ',"source_count":NaN}',
            "overflow_meta": head + ',"source_count":1e400}',
            "surrogate_title": '{"id":"' + sys.argv[3] + '","title":"\\ud800"}',
            "surrogate_key": head + ',"\\udc00":1}',
            "surrogate_meta": head + ',"note":"\\ud800"}',
            "dup_nested": head + ',"meta":{"x":1,"x":2}}',
            "deep65": head + ',"meta":' + '[' * 64 + ']' * 64 + '}',
            "meta_ok": '{"id":"' + sys.argv[3] + '","title":"\\ud83d\\ude00","n":1' + '0' * 300 + ',"meta":' + '[' * 63 + ']' * 63 + '}',
        }[mode])
    elif mode == "noname":
        print(json.dumps({"id": sys.argv[3]}))
    else:
        body = {"id": "WRONG12345" if mode == "wrong" else sys.argv[3], "title": "Test"}
        if mode == "leak_all":
            body["note"] = "SECRET_SENTINEL"
        print(json.dumps(body))
note("end")
'@
    $fake = Join-Path $root 'fake.py'
    Set-Content -LiteralPath $fake -Value $source -Encoding utf8
    $python = (Get-Command python).Source
    $browserProfile = Join-Path $root 'profile'
    New-Item -ItemType Directory -Path $browserProfile | Out-Null
    $config = Join-Path $root 'config.json'
    @{notebook_id='NOTEBOOK12345';browser_profile_path=$browserProfile} | ConvertTo-Json | Set-Content -LiteralPath $config
    $env:WP710_LOG = Join-Path $root 'calls.log'
    # [HINT reviewer - CHUA chay tren cay that; executor tu ap, tu do, tu chiu trach nhiem] lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con
    function Invoke-Wrapper([string]$mode, [string[]]$extra = @(), [string]$cfg = $config, [string]$tag = '') {
        $env:WP710_MODE = $mode; $env:WP710_TAG = $tag
        Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
        $wargs = @('-NoProfile','-File',$script,'-ConfigPath',$cfg,'-NlmCommand',$python,'-NlmArgumentsPrefix',$fake,
                   '-StageCommand',$python,'-StageArguments',$fake) + $extra
        $sw = [Diagnostics.Stopwatch]::StartNew()
        $out = & pwsh @wargs 2>&1
        $rc = $LASTEXITCODE
        $sw.Stop()
        $strings = @($out | Where-Object { $_ -is [string] })
        [pscustomobject]@{
            Rc = $rc; Seconds = $sw.Elapsed.TotalSeconds
            Text = (($out | ForEach-Object { "$_" }) -join "`n")
            Json = $(if ($strings.Count) { $strings[-1] | ConvertFrom-Json } else { $null })
            Calls = @(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue)
        }
    }
    foreach ($mode in @('ok','auth','network','timeout','wrong','empty','stage')) {
        $env:WP710_MODE = $mode
        Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
        # $args is an automatic variable inside PowerShell functions; never reuse that name.
        $loopArgs = @('-NoProfile','-File',$script,'-ConfigPath',$config,'-NlmCommand',$python,
                  '-NlmArgumentsPrefix',$fake,'-StageCommand',$python,
                  '-StageArguments',$fake,'-TimeoutSeconds',$(if ($mode -eq 'timeout') { '1' } else { '5' }))
        $output = & pwsh @loopArgs
        $rc = $LASTEXITCODE
        $result = $output | Select-Object -Last 1 | ConvertFrom-Json
        $calls = @(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue)
        $stageCalls = @($calls | Where-Object { $_ -like 'start:stage:*' }).Count
        $expected = @{ok='staged';auth='auth_failure';network='network_failure';
                      timeout='timeout';wrong='inconclusive';empty='inconclusive';stage='stage_failure'}[$mode]
        if ($result.status -ne $expected -or $output -match 'SECRET_SENTINEL' -or
            $stageCalls -ne [int]($mode -in @('ok','stage')) -or
            (($mode -eq 'ok') -ne ($rc -eq 0))) {
            throw "case $mode failed: status=$($result.status) rc=$rc stageCalls=$stageCalls step=$($result.step) reason=$($result.containment_reason)$($result.takeover_reason)"
        }
        $cases++
    }
    # Verify the Windows child receives a readable NUL stdin; the stdout pipe test in z1 does not measure this.
    if ($IsWindows) {
        $r = Invoke-Wrapper 'stdin_eof' @('-TimeoutSeconds','5')
        if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or
            @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 1) {
            throw 'the child stdin must be readable EOF from NUL'
        }
        $cases++
    }
    # [HINT reviewer - CHUA chay tren cay that; executor tu ap, tu do, tu chiu trach nhiem] lop: phan-loai-loi-doan-bang-chuoi-tu-do
    # <<case:c
    # (c) nhan trang thai KHONG duoc suy tu tu khoa tran (`auth`/`login`/`cookie`) vi chinh ten lenh (`nlm auth refresh`) va goi y
    #     (`nlm login`) nam trong stderr. Nhan mong doi la cach doc cua reviewer; executor co the doi kem ly do, nhung moi
    #     dau vao duoi day PHAI cho cung mot nhan on dinh va KHONG duoc stage.
    # WP710 r4/g3: anchored phrases only; command names, hints and paths are stripped; mixed signals are inconclusive.
    foreach ($case in @(@('err_conn_reset','network_failure'), @('err_login_hint','network_failure'), @('err_traceback','inconclusive'),
                        @('err_line401','inconclusive'), @('err_mixed','inconclusive'), @('err_http401','auth_failure'),
                        @('err_503','network_failure'), @('auth','auth_failure'))) {
        $r = Invoke-Wrapper $case[0] @('-TimeoutSeconds','5')
        if ($r.Json.status -ne $case[1] -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) {
            throw ('free-text classification wrong for ' + $case[0] + ': got ' + $r.Json.status + ', expected ' + $case[1])
        }
    }
    $cases++
    # >>case:c
    # Explicit keepalive is bounded; default made just one cycle above.
    $env:WP710_MODE = 'ok'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $output = & pwsh -NoProfile -File $script -ConfigPath $config -NlmCommand $python `
        -NlmArgumentsPrefix $fake -StageCommand $python -StageArguments $fake `
        -EnableKeepalive -MaxCycles 2 -IntervalSeconds 1
    if ($LASTEXITCODE -ne 0 -or @($output).Count -ne 2) { throw 'keepalive cycle count' }
    $cases++
    # The OS mutex must serialize two native processes. Each holds the lock through stage.
    $env:WP710_DELAY = '200'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $powershell = (Get-Command pwsh).Source
    $argline = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '"'
    $one = Start-Process -FilePath $powershell -ArgumentList $argline -PassThru @hidden -RedirectStandardOutput (Join-Path $root 'one.out')
    $two = Start-Process -FilePath $powershell -ArgumentList $argline -PassThru @hidden -RedirectStandardOutput (Join-Path $root 'two.out')
    $one.WaitForExit(); $two.WaitForExit()
    if ($one.ExitCode -ne 0 -or $two.ExitCode -ne 0) { throw 'concurrent process failed' }
    $lines = @(Get-Content -LiteralPath $env:WP710_LOG)
    $depth = 0
    foreach ($line in $lines) {
        if ($line -like 'start:*') { $depth++ } else { $depth-- }
        if ($depth -gt 1 -or $depth -lt 0) { throw 'concurrent critical sections overlap' }
    }
    if (@($lines | Where-Object { $_ -like 'start:stage:*' }).Count -ne 2) { throw 'missing concurrent stage' }
    $cases++
    # [HINT reviewer - CHUA chay tren cay that; executor tu ap, tu do, tu chiu trach nhiem] lop: test-ps1-thieu-rang
    # <<case:d
    # (d) ho so goc thieu / notebook_id sai / than canary khong co title|name => inconclusive, 0 thao tac con (Spec r4 #1, #2)
    $cfgNoProfile = Join-Path $root 'config-noprofile.json'
    @{notebook_id='NOTEBOOK12345';browser_profile_path=(Join-Path $root 'no-such-profile')} | ConvertTo-Json | Set-Content -LiteralPath $cfgNoProfile
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5') $cfgNoProfile
    if ($r.Json.status -ne 'inconclusive' -or $r.Rc -eq 0 -or $r.Calls.Count -ne 0) { throw 'missing original profile must be inconclusive with zero operations' }
    $cfgBadId = Join-Path $root 'config-badid.json'
    @{notebook_id='bad id!';browser_profile_path=$browserProfile} | ConvertTo-Json | Set-Content -LiteralPath $cfgBadId
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5') $cfgBadId
    if ($r.Json.status -ne 'inconclusive' -or $r.Rc -eq 0 -or $r.Calls.Count -ne 0) { throw 'invalid notebook_id must be inconclusive with zero operations' }
    $r = Invoke-Wrapper 'noname' @('-TimeoutSeconds','5')
    if ($r.Json.status -ne 'inconclusive' -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) { throw 'canary body without title/name must not stage' }
    $r = Invoke-Wrapper 'wrongcase' @('-TimeoutSeconds','5')
    if ($r.Json.status -ne 'inconclusive' -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) { throw 'notebook id must match case-sensitively' }
    $cases++
    # >>case:d
    # lop: stage-canary-true-khi-than-rong-hoac-sai-id
    # <<case:n
    foreach ($mode in @('title_bool','title_array','title_object','title_space','id_array','conflict_id',
                        'multi','multi_same','dup_id','case_key','ok_false','error_set',
                        'nan_meta','overflow_meta','surrogate_title','surrogate_key','surrogate_meta','dup_nested','deep65','control_title_001c','control_title_001d','control_title_001e','control_title_001f','control_name_001c','control_name_001d','control_name_001e','control_name_001f','bom_canary',
                        # WP714 round 4: the one blank table (both readers) and the stage command's view of stdout.
                        'control_title_0085','control_title_00a0','control_title_180e','control_title_200b','control_title_feff',
                        'control_name_3000','transport_u2028_title','transport_nel_title','transport_keyring_title')) {
        $r = Invoke-Wrapper $mode @('-TimeoutSeconds','5')
        # step must be 'canary': a reader exception escaping to 'preflight' is the same rc 4 for a different reason.
        if ($r.Rc -ne 4 -or $r.Json.status -ne 'inconclusive' -or $r.Json.step -ne 'canary' -or
            @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) {
            throw ('ambiguous or non-string notebook body must not stage: ' + $mode)
        }
    }
    # WP714: positive controls, so the allow-list is not "reject everything": one notebook object in the
    # three accepted shapes, and a date-like title stays a string (ConvertFrom-Json would turn it into DateTime).
    foreach ($mode in @('data_wrapped','singleton','title_date','meta_ok',
                        'transport_keyring_noise','transport_crlf_pretty','transport_ff_between','transport_bad_utf8_title')) {
        $r = Invoke-Wrapper $mode @('-TimeoutSeconds','5')
        if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or
            @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 1) {
            throw ('a single valid notebook object must stage: ' + $mode)
        }
    }
    $cases++
    # >>case:n
    # <<case:e
    # (e) thu tu refresh -> canary -> stage, dung 1 lan moi buoc, va bang chung ghi lai (Spec r4 #1, #4)
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5')
    $order = (@($r.Calls | Where-Object { $_ -like 'start:*' } | ForEach-Object { ($_ -split ':')[1] }) -join ',')
    if ($order -ne 'auth,notebook,stage') { throw ('operation order must be auth,notebook,stage; got ' + $order) }
    if ($r.Json.status -ne 'staged' -or $r.Json.cli_version -ne '1.0' -or $r.Json.profile_fingerprint -notmatch '^[0-9A-Fa-f]{16}$' -or $r.Json.rc -ne 0 -or $r.Json.elapsed_seconds -le 0) {
        throw 'emitted evidence fields (cli_version/profile_fingerprint/rc/elapsed_seconds) missing or wrong'
    }
    $cases++
    # >>case:e
    # <<case:f
    # (f) -MaxCycles/-IntervalSeconds KHONG tu bat keepalive: thieu -EnableKeepalive thi dung MOT chu ky (Spec r4 #6)
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-MaxCycles','3','-IntervalSeconds','1')
    if ($r.Rc -ne 0 -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 1) { throw '-MaxCycles without -EnableKeepalive must run exactly one cycle' }
    $cases++
    # >>case:f
    # <<case:g
    # (g) sentinel khong lot ra stdout LAN stderr, ke ca duong THANH CONG (`leak_all` in sentinel o stdout+stderr cua MOI thao tac) (Spec r4 #4)
    foreach ($m in @('leak_all','auth','network','stage')) {
        $r = Invoke-Wrapper $m @('-TimeoutSeconds','5')
        if ($r.Text -match 'SECRET_SENTINEL') { throw ('sentinel leaked to stdout/stderr in mode ' + $m) }
    }
    $r = Invoke-Wrapper 'leak_all' @('-TimeoutSeconds','5')
    if ($r.Json.status -ne 'staged') { throw 'leak_all control must still stage' }
    $cases++
    # >>case:g
    # <<case:h
    # (h) het han cho khoa => fail-closed, KHONG chay thao tac nao; ten khoa lay TU SCRIPT (khong cung) (Spec r4 #6)
    $lockFromScript = [regex]::Match((Get-Content -LiteralPath $script -Raw), 'Mutex\]::new\(\$false,\s*''([^'']+)''\)').Groups[1].Value
    if (-not $lockFromScript -or -not (Select-String -LiteralPath $PSCommandPath -SimpleMatch $lockFromScript -Quiet)) { throw 'script lock name not found, or the abandoned-owner case no longer holds that exact name' }
    $holdScript = Join-Path $root 'hold.ps1'
    @'
param([string]$Name, [string]$Ready, [int]$Seconds)
$m = [Threading.Mutex]::new($false, $Name)
[void]$m.WaitOne()
Set-Content -LiteralPath $Ready -Value 'held'
Start-Sleep -Seconds $Seconds
$m.ReleaseMutex()
'@ | Set-Content -LiteralPath $holdScript
    $readyHold = Join-Path $root 'ready-hold'
    $holder = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $holdScript + '" -Name "' + $lockFromScript + '" -Ready "' + $readyHold + '" -Seconds 8') -PassThru @hidden
    for ($i=0; $i -lt 100 -and -not (Test-Path -LiteralPath $readyHold); $i++) { Start-Sleep -Milliseconds 100 }
    if (-not (Test-Path -LiteralPath $readyHold)) { throw 'lock holder did not start' }
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    if ($r.Rc -eq 0 -or $r.Json.status -ne 'inconclusive' -or $r.Calls.Count -ne 0) { throw 'lock-wait timeout must fail closed without running any operation' }
    $holder.WaitForExit()
    $cases++
    # >>case:h
    # <<case:i
    # (i) MOT khoa cho ca refresh -> canary -> stage cua MOI tien trinh (khong phai khoa tung thao tac) (Spec r4 #4)
    $env:WP710_MODE = 'ok'; $env:WP710_DELAY = '200'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $argT = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '"'
    $env:WP710_TAG = 'one'; $t1 = Start-Process -FilePath $powershell -ArgumentList $argT -PassThru @hidden -RedirectStandardOutput (Join-Path $root 't1.out')
    $env:WP710_TAG = 'two'; $t2 = Start-Process -FilePath $powershell -ArgumentList $argT -PassThru @hidden -RedirectStandardOutput (Join-Path $root 't2.out')
    $t1.WaitForExit(); $t2.WaitForExit()
    if ($t1.ExitCode -ne 0 -or $t2.ExitCode -ne 0) { throw 'tagged concurrent wrappers failed' }
    $groups = @()
    foreach ($ln in @(Get-Content -LiteralPath $env:WP710_LOG | Where-Object { $_ -like 'start:*' })) {
        $tg = ($ln -split ':')[3]
        if ($groups.Count -eq 0 -or $groups[-1] -ne $tg) { $groups += $tg }
    }
    if ($groups.Count -ne 2) { throw ('refresh -> canary -> stage must be one critical section per process; tag sequence: ' + ($groups -join ',')) }
    $env:WP710_DELAY = '0'
    $cases++
    # >>case:i
    # <<case:j
    # (j) qua han => con BI GIET (khong de chay tiep), va nhan `timeout` cung ap cho buoc canary (Spec r4 #1, #5)
    $r = Invoke-Wrapper 'timeout' @('-TimeoutSeconds','1')
    Start-Sleep -Seconds 5
    if (@(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue | Where-Object { $_ -like 'end:auth:*' }).Count -ne 0) { throw 'timed-out child must be killed, not left to finish' }
    $r = Invoke-Wrapper 'timeout_canary' @('-TimeoutSeconds','1')
    if ($r.Json.status -ne 'timeout' -or @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count -ne 0) { throw 'canary timeout must report status timeout and not stage' }
    $env:WP710_MODE = 'ok'; $env:WP710_TAG = ''; $env:WP710_DELAY = '200'
    $cases++
    # >>case:j
    # A killed owner leaves an abandoned OS mutex; takeover is then permitted.
    $lockName = 'Global\tra_luat_nlm_credential_refresh'
    $ownerScript = Join-Path $root 'owner.ps1'
    @'
param([string]$Name, [string]$Ready)
$m = [Threading.Mutex]::new($false, $Name)
[void]$m.WaitOne()
Set-Content -LiteralPath $Ready -Value 'held'
Start-Sleep -Seconds 30
'@ | Set-Content -LiteralPath $ownerScript
    $ready = Join-Path $root 'ready'
    $owner = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $ownerScript + '" -Name "' + $lockName + '" -Ready "' + $ready + '"') -PassThru @hidden
    for ($i=0; $i -lt 50 -and -not (Test-Path -LiteralPath $ready); $i++) { Start-Sleep -Milliseconds 100 }
    if (-not (Test-Path -LiteralPath $ready)) { throw 'owner did not acquire lock' }
    Stop-Process -Id $owner.Id -Force
    $owner.WaitForExit()
    $env:WP710_DELAY = '0'
    $output = & pwsh -NoProfile -File $script -ConfigPath $config -NlmCommand $python `
        -NlmArgumentsPrefix $fake -StageCommand $python -StageArguments $fake
    if ($LASTEXITCODE -ne 0 -or ($output | Select-Object -Last 1 | ConvertFrom-Json).status -ne 'staged') {
        throw 'abandoned mutex takeover failed'
    }
    $cases++
    $env:WP710_DELAY = '0'
    # <<case:a
    # (a) mot hau due (trinh duyet/daemon) giu pipe stdout/stderr sau khi CLI thoat rc 0 khong duoc keo dai qua -TimeoutSeconds
    $env:WP714_LINGER_PID = Join-Path $root 'linger.pid'
    try {
        $r = Invoke-Wrapper 'linger' @('-TimeoutSeconds','2')
        if ($r.Seconds -gt 12) { throw ('wrapper exceeded its own timeout budget: ' + [int]$r.Seconds + 's with -TimeoutSeconds 2 (a descendant held the redirected pipes)') }
        # WP714: the outcome, not only the wall clock: a pipe held past the budget is a timeout with zero
        # stage, and on return the descendant is gone (Linux marker sweep) or the record stays (elsewhere).
        if ($r.Rc -ne 3 -or $r.Json.status -ne 'timeout' -or $r.Json.step -ne 'refresh' -or
            @($r.Calls | Where-Object { $_ -like 'start:stage:*' -or $_ -like 'start:notebook:*' }).Count -ne 0) {
            throw ('a lingering pipe writer must end as timeout with zero later steps: rc=' + $r.Rc + ' status=' + $r.Json.status)
        }
        $lingerPid = [int](Get-Content -LiteralPath $env:WP714_LINGER_PID -Raw)
        $lingerAlive = $null -ne (Get-Process -Id $lingerPid -ErrorAction SilentlyContinue)
        if ($IsLinux -and $lingerAlive) {
            try { $lingerAlive = [IO.File]::ReadAllText("/proc/$lingerPid/stat") -notmatch '\)\s+Z\s' } catch { $lingerAlive = $false }
        }
        $recLinger = Join-Path ([IO.Path]::GetTempPath()) 'tra_luat_nlm_credential_refresh.operation.json'
        if ($lingerAlive -and -not (Test-Path -LiteralPath $recLinger)) {
            throw 'a live descendant was left behind and its operation record was deleted'
        }
        if ($contained -and ($lingerAlive -or $r.Json.steps.refresh.child_confirmed_exited -ne $true)) {
            throw 'the descendant must be stopped and confirmed before the wrapper returns'
        }
        if ($IsWindows -and ($r.Json.tree_measurement -ne 'windows_job_object' -or $r.Json.steps.refresh.tree_state -ne 'gone' -or
            $r.Json.steps.refresh.descendants_stopped -lt 1 -or (Test-Path -LiteralPath $recLinger))) {
            throw ('Windows: a timed-out step must empty its job, count the descendant and leave no record: ' + ($r.Json.steps.refresh | ConvertTo-Json -Compress))
        }
    } finally {
        if (Test-Path -LiteralPath $env:WP714_LINGER_PID) {
            Stop-Process -Id ([int](Get-Content -LiteralPath $env:WP714_LINGER_PID -Raw)) -Force -ErrorAction SilentlyContinue
        }
        Remove-Item Env:WP714_LINGER_PID -ErrorAction SilentlyContinue
    }
    $cases++
    # >>case:a
    # <<case:b
    # (b) chu khoa bi giet khi thao tac con dang chay: wrapper ke tiep KHONG duoc chay thao tac chong len thao tac con cua chu cu
    $env:WP710_MODE = 'beat'; $env:WP710_DELAY = '4000'; $env:WP710_TAG = 'A'
    Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
    $argA = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '"'
    $wa = Start-Process -FilePath $powershell -ArgumentList $argA -PassThru @hidden
    for ($i=0; $i -lt 100 -and -not (Test-Path -LiteralPath $env:WP710_LOG -PathType Leaf -ErrorAction SilentlyContinue); $i++) { Start-Sleep -Milliseconds 100 }
    for ($i=0; $i -lt 100 -and -not (@(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue) -like 'beat:auth:*:A'); $i++) { Start-Sleep -Milliseconds 100 }
    if (-not (@(Get-Content -LiteralPath $env:WP710_LOG) -like 'beat:auth:*:A')) { throw 'wrapper A never started its child' }
    Stop-Process -Id $wa.Id -Force
    $wa.WaitForExit()
    $env:WP710_MODE = 'ok'; $env:WP710_DELAY = '0'; $env:WP710_TAG = 'B'
    & pwsh -NoProfile -File $script -ConfigPath $config -NlmCommand $python -NlmArgumentsPrefix $fake -StageCommand $python -StageArguments $fake -LockWaitSeconds 20 2>&1 | Out-Null
    Start-Sleep -Seconds 5
    $lines = @(Get-Content -LiteralPath $env:WP710_LOG)
    $firstB = -1
    for ($i=0; $i -lt $lines.Count; $i++) { if ($lines[$i] -like 'start:*:B') { $firstB = $i; break } }
    if ($firstB -ge 0 -and @($lines[$firstB..($lines.Count-1)] | Where-Object { $_ -like 'beat:*:A' }).Count -gt 0) {
        throw 'operations overlapped: wrapper B started while the dead wrapper A child was still running'
    }
    $cases++
    # >>case:b
    $env:WP710_DELAY = '0'
    # <<case:k
    # (k) WP710 r4/g3 Spec #1 evidence: rc/elapsed of EVERY step (not just stage), honest profile binding,
    #     and the stage child receives the trusted notebook so both canaries probe the same notebook.
    $env:WP710_ENVLOG = Join-Path $root 'stage-env.txt'
    Remove-Item -LiteralPath $env:WP710_ENVLOG -ErrorAction SilentlyContinue
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5')
    $s = $r.Json.steps
    if ($r.Json.status -ne 'staged' -or $r.Json.cycle -ne 1 -or $r.Json.profile_bound_to_cli -ne $false -or
        $s.version.rc -ne 0 -or $s.refresh.rc -ne 0 -or $s.refresh.elapsed_seconds -le 0 -or $s.refresh.timeout -ne $false -or
        $s.canary.rc -ne 0 -or $s.canary.elapsed_seconds -le 0 -or $s.stage.rc -ne 0 -or $s.stage.elapsed_seconds -le 0) {
        throw ('per-step evidence missing or wrong: ' + ($r.Json | ConvertTo-Json -Compress -Depth 5))
    }
    # WP714: TL_CANARY_NOTEBOOK_ID is the pin a profile config cannot rewrite; TL_NOTEBOOK_ID stays for older stage commands.
    if ((Get-Content -LiteralPath $env:WP710_ENVLOG -Raw) -cne 'NOTEBOOK12345|NOTEBOOK12345') { throw 'stage child did not receive TL_NOTEBOOK_ID and TL_CANARY_NOTEBOOK_ID of the trusted config' }
    $r = Invoke-Wrapper 'auth' @('-TimeoutSeconds','5')
    if ($r.Json.steps.refresh.rc -ne 7 -or $null -ne $r.Json.steps.canary -or $null -ne $r.Json.steps.stage) {
        throw 'refresh failure evidence must carry the real refresh rc and no later step'
    }
    Remove-Item Env:WP710_ENVLOG
    # A later keepalive cycle must not carry the previous cycle's canary/stage evidence.
    Remove-Item -LiteralPath (Join-Path $root 'auth-count.txt') -ErrorAction SilentlyContinue
    $r = Invoke-Wrapper 'auth_second' @('-TimeoutSeconds','5','-EnableKeepalive','-MaxCycles','2','-IntervalSeconds','1')
    if ($r.Rc -ne 2 -or $r.Json.cycle -ne 2 -or $r.Json.status -ne 'auth_failure' -or $r.Json.steps.refresh.rc -ne 7 -or
        $null -ne $r.Json.steps.canary -or $null -ne $r.Json.steps.stage) {
        throw ('cycle 2 evidence carries stale steps from cycle 1: ' + ($r.Json | ConvertTo-Json -Compress -Depth 5))
    }
    $cases++
    # >>case:k
    # <<case:l
    # (l) keepalive keeps its interval: cycle 2 refresh starts no earlier than IntervalSeconds after cycle 1 stage ended.
    $env:WP710_TIMELOG = Join-Path $root 'times.log'
    Remove-Item -LiteralPath $env:WP710_TIMELOG -ErrorAction SilentlyContinue
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-EnableKeepalive','-MaxCycles','2','-IntervalSeconds','2')
    $times = @(Get-Content -LiteralPath $env:WP710_TIMELOG)
    $endStage = @($times | Where-Object { $_ -like 'end stage *' })
    $startAuth = @($times | Where-Object { $_ -like 'start auth *' })
    if ($r.Rc -ne 0 -or $endStage.Count -ne 2 -or $startAuth.Count -ne 2) { throw 'keepalive did not run two full cycles' }
    $gap = [double]($startAuth[1] -split ' ')[2] - [double]($endStage[0] -split ' ')[2]
    if ($gap -lt 1.8) { throw ('keepalive interval not honoured: gap ' + $gap + 's for -IntervalSeconds 2') }
    Remove-Item Env:WP710_TIMELOG
    $cases++
    # >>case:l
    # <<case:m
    # (m) operation record: a live recorded child blocks a new owner (fail closed, zero operations); an unreadable
    #     record fails closed. WP714 round 3: a record WITHOUT a marker (dead or reused pid) cannot prove its tree
    #     gone on any platform, so it goes to the BOUNDED quarantine: blocked first (tree_quarantine, zero
    #     operations), released once -UnconfirmedQuarantineSeconds passed, with takeover evidence. Path is read
    #     from the script.
    $recName = [regex]::Match((Get-Content -LiteralPath $script -Raw), "GetTempPath\(\)\)\s+'([^']+)'").Groups[1].Value
    if (-not $recName) { throw 'operation record name not found in script' }
    $recPath = Join-Path ([IO.Path]::GetTempPath()) $recName
    $sleeper = Start-Process -FilePath $python -ArgumentList '-c "import time; time.sleep(60)"' -PassThru @hidden
    try {
        # Read through a FRESH pwsh, as the wrapper does. On Linux .NET derives StartTime from a boot time it
        # caches per process; where the wall clock and the uptime clock run at different rates (measured in
        # WSL2: this long-lived test process read 2.9 s off after 130 s and 7.0 s after 256 s) the reading of a
        # long-lived process no longer matches a fresh one within the wrapper's 1 s tolerance.
        $ticks = [int64](& pwsh -NoProfile -Command "(Get-Process -Id $($sleeper.Id)).StartTime.ToUniversalTime().Ticks")
        @{pid=$sleeper.Id; start_ticks=$ticks} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recPath
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Calls.Count -ne 0) { throw 'live recorded child must block the new owner with zero operations' }
        if ($r.Json.takeover_reason -ne 'root_alive') { throw ('a live root must be reported as such: ' + $r.Json.takeover_reason) }
        @{pid=$sleeper.Id; start_ticks=($ticks - 36000000000)} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recPath
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'tree_not_measurable' -or $r.Calls.Count -ne 0) {
            throw ('a reused pid without a marker must enter the bounded quarantine with zero operations: rc=' + $r.Rc + ' step=' + $r.Json.step)
        }
        Start-Sleep -Milliseconds 1200
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-UnconfirmedQuarantineSeconds','1')
        if ($IsLinux) {
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'quarantine_elapsed' -or (Test-Path -LiteralPath $recPath)) {
                throw ('the quarantine must release after its bound and say so: rc=' + $r.Rc + ' takeover=' + $r.Json.takeover)
            }
        } else {
            # WP710 g4: off Linux nothing was measured, so the timer is not an exit. Only the operator is.
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover -ne 'none' -or $r.Calls.Count -ne 0 -or -not (Test-Path -LiteralPath $recPath)) {
                throw ('an unmeasured tree must not be released by the timer: rc=' + $r.Rc + ' takeover=' + $r.Json.takeover + ' calls=' + $r.Calls.Count)
            }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case m by hand')
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'operator_release' -or
                $r.Json.takeover_reason -ne 'tree_not_measurable' -or (Test-Path -LiteralPath $recPath)) {
                throw ('an operator release of an unmeasured tree must stage and say so: rc=' + $r.Rc + ' takeover=' + $r.Json.takeover)
            }
        }
    } finally { Stop-Process -Id $sleeper.Id -Force -ErrorAction SilentlyContinue }
    $sleeper.WaitForExit()
    @{pid=$sleeper.Id; start_ticks=$ticks} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recPath
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Calls.Count -ne 0) { throw 'a dead pid without a marker must not be read as a dead tree' }
    if ($IsLinux) {
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','3','-UnconfirmedQuarantineSeconds','1')
        if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'quarantine_elapsed' -or (Test-Path -LiteralPath $recPath)) { throw 'a released quarantine must stage, and a finished run leaves no record' }
    } else {
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','3','-UnconfirmedQuarantineSeconds','1')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Calls.Count -ne 0) { throw 'a dead pid without a marker must stay quarantined past the bound' }
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case m by hand')
        if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'operator_release' -or (Test-Path -LiteralPath $recPath)) { throw 'an operator release must stage, and a finished run leaves no record' }
    }
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    if ($r.Rc -ne 0 -or $r.Json.takeover -ne 'none') { throw 'a clean start must not claim a takeover' }
    Set-Content -LiteralPath $recPath -Value 'not json'
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','2','-UnconfirmedQuarantineSeconds','1')
    Remove-Item -LiteralPath $recPath -ErrorAction SilentlyContinue
    if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Calls.Count -ne 0) { throw 'an unreadable operation record must fail closed, never through the quarantine' }
    $cases++
    # >>case:m
    # lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con
    # <<case:o
    $env:WP714_BEAT_FILE = Join-Path $root 'grandchild-beats.txt'
    $env:WP714_CHILD_PID_FILE = Join-Path $root 'grandchild.pid'
    try {
        $r = Invoke-Wrapper 'descendant_exit' @('-TimeoutSeconds','2')
        if ($r.Rc -ne 3 -or $r.Json.status -ne 'timeout') { throw 'inherited pipes must time out' }
        $childPid = [int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        $before = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue).Count
        Start-Sleep -Milliseconds 400
        $after = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue).Count
        if ($r.Rc -eq 0 -and $after -gt $before) {
            throw 'new owner staged while the old owner grandchild still performed operations'
        }
        # WP714: no overlap is not enough; a vacuous pass (B never ran) must fail too. On Linux the marked
        # grandchild is stopped and confirmed, so B must take over and stage; elsewhere B must not overlap.
        if ($contained -and ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $after -ne $before)) {
            throw ('takeover after a confirmed-dead old tree must stage: rc=' + $r.Rc + ' status=' + $r.Json.status)
        }
        if (-not $contained -and $r.Rc -ne 0 -and $r.Rc -ne 5) { throw ('unexpected takeover outcome rc=' + $r.Rc) }
        if ($IsWindows -and $null -ne (Get-Process -Id $childPid -ErrorAction SilentlyContinue)) { throw 'Windows: the pipe-holding grandchild outlived its job' }
    } finally {
        if (Test-Path -LiteralPath $env:WP714_CHILD_PID_FILE) {
            Stop-Process -Id ([int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)) -Force -ErrorAction SilentlyContinue
        }
        Remove-Item Env:WP714_BEAT_FILE, Env:WP714_CHILD_PID_FILE -ErrorAction SilentlyContinue
    }
    $cases++
    # >>case:o
    # <<case:p
    # (p) WP714: a record carrying an operation marker blocks a new owner while ANY process with that marker
    #     lives (the direct child may be long gone). Elsewhere a marker record without a pid fails closed.
    $recP = Join-Path ([IO.Path]::GetTempPath()) 'tra_luat_nlm_credential_refresh.operation.json'
    $markerP = [guid]::NewGuid().ToString('N')
    $markVar = [regex]::Match((Get-Content -LiteralPath $script -Raw), "MarkerName\s*=\s*'([^']+)'").Groups[1].Value
    if (-not $markVar) { throw 'operation marker variable not found in script' }
    $psi = [Diagnostics.ProcessStartInfo]::new($python)
    $psi.ArgumentList.Add('-c'); $psi.ArgumentList.Add('import time; time.sleep(60)')
    $psi.UseShellExecute = $false
    $psi.Environment[$markVar] = $markerP
    $marked = [Diagnostics.Process]::Start($psi)
    # The recorded pid is a direct child that already EXITED: only the marker can still see the live descendant.
    $gone = Start-Process -FilePath $python -ArgumentList '-c "import time; time.sleep(1)"' -PassThru @hidden
    $goneTicks = $gone.StartTime.ToUniversalTime().Ticks   # read while alive: StartTime is gone after exit
    $gone.WaitForExit()
    try {
        @{marker=$markerP; pid=$null; start_ticks=$null; tree_unconfirmed=$false} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recP
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        # Off Linux the marker cannot be searched for, and this hand-made record names no job: not measured,
        # so it blocks as a quarantine (the Windows "proven alive" case is x, with a real job).
        $wantP = if ($IsLinux) { 'lock_busy' } else { 'tree_quarantine' }
        if ($r.Rc -ne 5 -or $r.Json.step -ne $wantP -or $r.Calls.Count -ne 0) { throw 'a live marked process must block the new owner with zero operations' }
        if ($IsLinux) {
            # WP714 round 4: the manual exit never releases a tree proven alive.
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked the old tree')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Json.takeover -ne 'none' -or $r.Calls.Count -ne 0) { throw 'an operator release must never release a live marked tree' }
        }
        @{marker=$markerP; pid=$gone.Id; start_ticks=$goneTicks; tree_unconfirmed=$false} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recP
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        if ($IsLinux -and ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Calls.Count -ne 0)) {
            throw 'Linux: a live marked descendant must block even when the recorded child pid is dead'
        }
        Remove-Item -LiteralPath $recP -ErrorAction SilentlyContinue
    } finally { Stop-Process -Id $marked.Id -Force -ErrorAction SilentlyContinue }
    @{marker=$markerP; pid=$null; start_ticks=$null; tree_unconfirmed=$false} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recP
    $marked.WaitForExit()
    $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
    if ($IsLinux) {
        if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged') { throw 'Linux: a marker with no live process must not block' }
    } elseif ($r.Rc -ne 5 -or $r.Calls.Count -ne 0) { throw 'non-Linux: a marker record without a pid must fail closed' }
    Remove-Item -LiteralPath $recP -ErrorAction SilentlyContinue
    $cases++
    # >>case:p
    # <<case:q
    # (q) WP714: a descendant that dropped the pipes after `auth refresh` returned rc 0 is part of the operation:
    #     it is stopped and confirmed before the canary runs, and the evidence says so. Linux finds it by parent
    #     link and marker; WP710 g4, Windows: it is a member of the step's Job Object, whose count must reach 0.
    $env:WP714_BEAT_FILE = Join-Path $root 'daemon-beats.txt'
    $env:WP714_CHILD_PID_FILE = Join-Path $root 'daemon.pid'
    $env:WP710_TIMELOG = Join-Path $root 'daemon-times.log'
    Remove-Item -LiteralPath $env:WP714_BEAT_FILE, $env:WP710_TIMELOG -ErrorAction SilentlyContinue
    try {
        $r = Invoke-Wrapper 'daemon' @('-TimeoutSeconds','5')
        if ($contained) {
            $startNbLine = @(Get-Content -LiteralPath $env:WP710_TIMELOG -ErrorAction SilentlyContinue) | Where-Object { $_ -like 'start notebook *' } | Select-Object -First 1
            if (-not $startNbLine) { throw ('the run never reached the canary: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.containment_reason) }
            $startNb = [double](($startNbLine -split ' ')[2])
            $beatsQ = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue)
            if ($beatsQ.Count -lt 1) { throw 'fixture: the pipe-less descendant never ran, the case would pass vacuously' }
            $late = @($beatsQ | Where-Object { [double]$_ -gt $startNb })
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.steps.refresh.descendants_stopped -lt 1 -or
                $r.Json.steps.refresh.tree_state -ne 'gone' -or $late.Count -ne 0) {
                throw ('a pipe-less descendant must be stopped before the canary: rc=' + $r.Rc + ' stopped=' + $r.Json.steps.refresh.descendants_stopped + ' tree=' + $r.Json.steps.refresh.tree_state + ' late=' + $late.Count)
            }
            $daemonQ = [int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)
            if ($IsWindows -and $null -ne (Get-Process -Id $daemonQ -ErrorAction SilentlyContinue)) { throw 'Windows: the pipe-less descendant is still alive after the run' }
        } else {
            if ($r.Json.steps.refresh.descendants_stopped -ne 0) {
                throw 'non-Linux: descendants cannot be enumerated, the evidence must not claim any were stopped'
            }
            # The existing daemon fixture must not be allowed to overlap any subsequent operation.
            # A status/evidence label alone is insufficient on the Windows branch.
            $before = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue).Count
            Start-Sleep -Milliseconds 400
            $after = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue).Count
            $laterCalls = @($r.Calls | Where-Object { $_ -like 'start:notebook:*' -or $_ -like 'start:stage:*' })
            if ($laterCalls.Count -gt 0 -and $after -gt $before) {
                throw 'non-Linux: a live pipe-less descendant overlapped canary or stage'
            }
            if ($r.Rc -eq 0 -and $r.Json.status -ne 'staged') { throw 'successful control lacks staged evidence' }
        }
    } finally {
        if (Test-Path -LiteralPath $env:WP714_CHILD_PID_FILE) {
            Stop-Process -Id ([int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)) -Force -ErrorAction SilentlyContinue
        }
        Remove-Item Env:WP714_BEAT_FILE, Env:WP714_CHILD_PID_FILE, Env:WP710_TIMELOG -ErrorAction SilentlyContinue
    }
    $cases++
    # >>case:q
    # lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con
    # <<case:r
    foreach ($takeoverMode in @('descendant_exit', 'descendant_scrubbed_exit')) {
        # Reuse descendant_exit: kill its wrapper after the direct CLI has exited, then test takeover.
        # The operation marker must come from the real writer rather than a record assembled by the test.
        $env:WP714_BEAT_FILE = Join-Path $root 'owner-exit-beats.txt'
        $env:WP714_CHILD_PID_FILE = Join-Path $root 'owner-exit-child.pid'
        Remove-Item -LiteralPath $env:WP714_BEAT_FILE, $env:WP714_CHILD_PID_FILE -ErrorAction SilentlyContinue
        $ownerR = $null
        $childR = $null
        try {
            $env:WP710_MODE = $takeoverMode; $env:WP710_DELAY = '0'
            $argR = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '" -TimeoutSeconds 20'
            $ownerR = Start-Process -FilePath (Get-Command pwsh).Source -ArgumentList $argR -PassThru @hidden
            for ($i=0; $i -lt 100 -and -not (Test-Path -LiteralPath $env:WP714_CHILD_PID_FILE); $i++) { Start-Sleep -Milliseconds 100 }
            if (-not (Test-Path -LiteralPath $env:WP714_CHILD_PID_FILE)) { throw 'orphan takeover fixture never started' }
            $childR = [int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)
            $recordR = Join-Path ([IO.Path]::GetTempPath()) 'tra_luat_nlm_credential_refresh.operation.json'
            $writtenR = Get-Content -LiteralPath $recordR -Raw | ConvertFrom-Json
            if ([string]$writtenR.marker -notmatch '^[0-9a-f]{32}$') { throw 'actual operation record did not retain its child marker' }
            $directGoneR = $false
            for ($i=0; $i -lt 50 -and -not $directGoneR; $i++) {
                $directGoneR = $null -eq (Get-Process -Id ([int]$writtenR.pid) -ErrorAction SilentlyContinue)
                if ($IsLinux -and -not $directGoneR) {
                    try { $directGoneR = [IO.File]::ReadAllText("/proc/$([int]$writtenR.pid)/stat") -match '\)\s+Z\s' } catch { $directGoneR = $true }
                }
                if (-not $directGoneR) { Start-Sleep -Milliseconds 100 }
            }
            if (-not $directGoneR) { throw 'fixture direct CLI did not exit before owner death' }
            Stop-Process -Id $ownerR.Id -Force
            $ownerR.WaitForExit()
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            $beforeR = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue).Count
            Start-Sleep -Milliseconds 400
            $afterR = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE -ErrorAction SilentlyContinue).Count
            if ($r.Calls.Count -gt 0 -and $afterR -gt $beforeR) { throw 'new owner overlapped a descendant of the exited old CLI' }
            if ($r.Rc -eq 0) {
                if ($r.Json.status -ne 'staged' -or $afterR -ne $beforeR) { throw 'successful takeover lacks dead-tree evidence' }
            } elseif ($r.Rc -ne 5 -or $r.Calls.Count -ne 0) { throw 'unconfirmed old tree must block with zero operations' }
            if ($IsLinux -and ($r.Rc -ne 5 -or $r.Json.takeover_reason -ne 'marked_alive')) { throw 'Linux: the live marked grandchild of a killed owner must block' }
            if ($IsLinux -and -not ([int64]$writtenR.owner_start_jiffies -gt 0)) { throw 'actual operation record did not retain the owner start (quarantine floor)' }
            # WP710 g4, Windows: the owner's death closed the step's job, which ended the grandchild (marker or
            # not). The next owner finds no such job and takes over at once; the grandchild must really be gone.
            if ($IsWindows) {
                if ([string]$writtenR.job -notmatch '^Global\\tra_luat_nlm_op_[0-9a-f]{32}$') { throw 'actual operation record did not name the step job' }
                if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'none') { throw ('Windows: takeover after the owner died must stage: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason) }
                if ($null -ne (Get-Process -Id $childR -ErrorAction SilentlyContinue)) { throw 'Windows: a descendant survived the death of the job owner' }
            }
            Stop-Process -Id $childR -Force -ErrorAction SilentlyContinue
            # Off Linux the old tree is not measurable: the takeover is the bounded quarantine, stamped by the run above.
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','3','-UnconfirmedQuarantineSeconds','1')
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged') { throw 'takeover after the fixture tree ended must stage' }
            if ($IsLinux -and $r.Json.takeover -ne 'none') { throw 'Linux: a proven-gone tree is a plain takeover, not a quarantine release' }
        } finally {
            if ($null -ne $ownerR -and -not $ownerR.HasExited) { Stop-Process -Id $ownerR.Id -Force -ErrorAction SilentlyContinue }
            if ($null -ne $childR) { Stop-Process -Id $childR -Force -ErrorAction SilentlyContinue }
            Remove-Item Env:WP714_BEAT_FILE, Env:WP714_CHILD_PID_FILE -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:r
    # lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con (WP714 round 3)
    # <<case:s
    # (s) An environment that cannot be read is UNKNOWN, never "no marker"; the bounded quarantine never releases
    #     a tree PROVEN alive. Part A, real processes: a non-dumpable process carrying the old marker (as a browser
    #     sandbox child would). Whether its environment is readable depends on privilege (root with
    #     CAP_SYS_PTRACE reads it - measured in the container this suite was written in), so the case asserts the
    #     branch it actually observed: readable => marked_alive, blocked even past the bound; unreadable =>
    #     tree_unknown, blocked until the tree is proven gone. Part B, Linux: the classifier itself, on a
    #     projection whose enumeration root (the script's one $ProcRoot line) is a fixture tree in which root
    #     cannot read an environment either (it is a directory): unknown, floor, readable and marked controls.
    if ($IsLinux) {
        $recS = Join-Path ([IO.Path]::GetTempPath()) $recName
        $markerS = [guid]::NewGuid().ToString('N')
        $psiS = [Diagnostics.ProcessStartInfo]::new($python)
        $psiS.ArgumentList.Add('-c'); $psiS.ArgumentList.Add('import ctypes, time; ctypes.CDLL(None).prctl(4, 0, 0, 0, 0); time.sleep(60)')
        $psiS.UseShellExecute = $false
        $psiS.Environment[$markVar] = $markerS
        $hiddenS = [Diagnostics.Process]::Start($psiS)
        try {
            Start-Sleep -Milliseconds 500
            $readableS = $true
            try { [void][IO.File]::ReadAllBytes("/proc/$($hiddenS.Id)/environ") } catch { $readableS = $false }
            @{marker=$markerS; pid=$null; start_ticks=$null; tree_unconfirmed=$false} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recS
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            $wantStep = if ($readableS) { 'lock_busy' } else { 'tree_quarantine' }
            $wantReason = if ($readableS) { 'marked_alive' } else { 'tree_unknown' }
            if ($r.Rc -ne 5 -or $r.Json.step -ne $wantStep -or $r.Json.takeover_reason -ne $wantReason -or $r.Calls.Count -ne 0) {
                throw ('a live non-dumpable marked process must block: readable=' + $readableS + ' rc=' + $r.Rc + ' reason=' + $r.Json.takeover_reason)
            }
            Start-Sleep -Milliseconds 1200
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-UnconfirmedQuarantineSeconds','1')
            if ($readableS -and ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Calls.Count -ne 0)) { throw 'the quarantine bound must never release a tree proven alive' }
            if (-not $readableS -and ($r.Rc -ne 5 -or $r.Calls.Count -ne 0)) { throw 'quarantine expiry must not release a live unreadable child' }
        } finally { Stop-Process -Id $hiddenS.Id -Force -ErrorAction SilentlyContinue }
        $hiddenS.WaitForExit()
        Remove-Item -LiteralPath $recS -ErrorAction SilentlyContinue
        # Part B: classifier on a fixture enumeration root.
        $srcS = Get-Content -LiteralPath $script -Raw
        $rootLine = "`$ProcRoot = '/proc'"
        if (([regex]::Matches($srcS, [regex]::Escape($rootLine))).Count -ne 1) { throw 'enumeration root line not found exactly once in the script' }
        $fakeProc = Join-Path $root 'fakeproc'
        $projS = Join-Path $root 'projection-s'
        New-Item -ItemType Directory -Path $fakeProc, $projS | Out-Null
        $projScriptS = Join-Path $projS 'nlm-credential-refresh.ps1'
        Set-Content -LiteralPath $projScriptS -Value $srcS.Replace($rootLine, "`$ProcRoot = '$fakeProc'") -Encoding utf8
        $ownUidS = [regex]::Match([IO.File]::ReadAllText('/proc/self/status'), '(?m)^Uid:\s+(\d+)').Groups[1].Value
        $floorS = 100000
        function Set-FakeProcess([uint64]$start, $environ) {   # untyped: [string] would turn `$null into ''
            $dirF = Join-Path $fakeProc '424242'
            if (Test-Path -LiteralPath $dirF) { Remove-Item -LiteralPath $dirF -Recurse -Force }
            New-Item -ItemType Directory -Path $dirF | Out-Null
            Set-Content -LiteralPath (Join-Path $dirF 'stat') -NoNewline -Value ('424242 (fake) S 1 0 0 0 -1 4194560' + (' 0' * 12) + " $start 0 0")
            Set-Content -LiteralPath (Join-Path $dirF 'status') -Value ("Name:`tfake`nUid:`t$ownUidS`t$ownUidS`t$ownUidS`t$ownUidS")
            if ($null -eq $environ) { New-Item -ItemType Directory -Path (Join-Path $dirF 'environ') | Out-Null }
            else { [IO.File]::WriteAllText((Join-Path $dirF 'environ'), $environ) }
        }
        $realScriptS = $script
        try {
            $script = $projScriptS
            $rows = @(
                @{ name='unreadable'; start=($floorS + 10); env=$null; rc=5; step='tree_quarantine'; reason='tree_unknown' },
                @{ name='older_than_owner'; start=($floorS - 10); env=$null; rc=0; step='stage'; reason='' },
                @{ name='readable_unmarked'; start=($floorS + 10); env="PATH=/bin`0OTHER=1`0"; rc=0; step='stage'; reason='' },
                @{ name='readable_marked'; start=($floorS + 10); env="PATH=/bin`0$markVar=$markerS`0"; rc=5; step='lock_busy'; reason='marked_alive' }
            )
            foreach ($row in $rows) {
                Set-FakeProcess $row.start $row.env
                @{marker=$markerS; pid=$null; start_ticks=$null; tree_unconfirmed=$false; owner_start_jiffies=$floorS} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recS
                $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
                if ($r.Rc -ne $row.rc -or $r.Json.step -ne $row.step -or [string]$r.Json.takeover_reason -ne $row.reason -or
                    ($row.rc -ne 0 -and $r.Calls.Count -ne 0)) {
                    throw ('tree classifier ' + $row.name + ': rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason)
                }
            }
            Set-FakeProcess ($floorS + 10) $null
            @{marker=$markerS; pid=$null; start_ticks=$null; tree_unconfirmed=$false; owner_start_jiffies=$floorS} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recS
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            Start-Sleep -Milliseconds 1200
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-UnconfirmedQuarantineSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Calls.Count -ne 0) {
                throw ('expiry is not dead-tree proof: rc=' + $r.Rc + ' takeover=' + $r.Json.takeover)
            }
        } finally {
            $script = $realScriptS
            Remove-Item -LiteralPath $recS -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:s
    # <<case:t
    # (t) Where the tree can be neither enumerated nor contained (projection: the platform switches of the script
    #     set to $false; no supported platform is like this, it is the fail-closed floor). WP710 g4: a step that
    #     SUCCEEDS there is not a step whose tree ended - the run stops with rc 5 (tree_containment), keeps its
    #     record and starts nothing after it; the next owner is quarantined and the timer does NOT release it; an
    #     operator release is recorded but cannot make the tree measurable; a version probe that times out keeps
    #     its record and stops the run.
    $srcT = Get-Content -LiteralPath $script -Raw
    $projectedT = $srcT
    foreach ($switchT in @('$TreeMeasurable = [bool]$IsLinux', '$JobContainment = [bool]$IsWindows')) {
        if (([regex]::Matches($srcT, [regex]::Escape($switchT))).Count -ne 1) { throw ('platform switch not found exactly once in the script: ' + $switchT) }
        $projectedT = $projectedT.Replace($switchT, ($switchT.Split('=')[0] + '= $false'))
    }
    $projT = Join-Path $root 'projection'
    New-Item -ItemType Directory -Path $projT | Out-Null
    $projScript = Join-Path $projT 'nlm-credential-refresh.ps1'
    Set-Content -LiteralPath $projScript -Value $projectedT -Encoding utf8
    $recT = Join-Path ([IO.Path]::GetTempPath()) $recName
    $realScript = $script
    $env:WP714_LINGER_PID = Join-Path $root 'proj-linger.pid'
    try {
        $script = $projScript
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5')
        if ($r.Rc -ne 5 -or $r.Json.status -ne 'inconclusive' -or $r.Json.step -ne 'tree_containment' -or
            $r.Json.containment_reason -ne 'tree_not_measurable' -or $r.Json.tree_measurement -ne 'not_measurable' -or
            $r.Json.steps.version.tree_state -ne 'not_measurable' -or $r.Json.steps.version.child_confirmed_exited -ne $false -or
            $r.Calls.Count -ne 0) {
            throw ('a successful step with an unmeasured tree must stop the run: rc=' + $r.Rc + ' step=' + $r.Json.step + ' calls=' + $r.Calls.Count)
        }
        if (-not (Test-Path -LiteralPath $recT) -or (Get-Content -LiteralPath $recT -Raw | ConvertFrom-Json).tree_unconfirmed -ne $true) {
            throw 'an unmeasured tree must keep its operation record'
        }
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'tree_not_measurable' -or $r.Calls.Count -ne 0) {
            throw ('an unconfirmed tree must block the next owner with zero operations: rc=' + $r.Rc + ' step=' + $r.Json.step)
        }
        Start-Sleep -Milliseconds 1200
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-UnconfirmedQuarantineSeconds','1')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover -ne 'none' -or $r.Calls.Count -ne 0 -or -not (Test-Path -LiteralPath $recT)) {
            throw ('the timer must not release an unmeasured tree: rc=' + $r.Rc + ' step=' + $r.Json.step + ' takeover=' + $r.Json.takeover)
        }
        $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case t by hand')
        if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_containment' -or $r.Json.takeover -ne 'operator_release' -or $r.Calls.Count -ne 0) {
            throw ('an operator release cannot make the platform measurable: rc=' + $r.Rc + ' step=' + $r.Json.step + ' takeover=' + $r.Json.takeover)
        }
        Remove-Item -LiteralPath $recT -ErrorAction SilentlyContinue
        $r = Invoke-Wrapper 'version_linger' @('-TimeoutSeconds','1')
        if ($r.Rc -ne 3 -or $r.Json.step -ne 'version' -or $r.Json.steps.version.child_confirmed_exited -ne $false -or
            $r.Calls.Count -ne 0 -or -not (Test-Path -LiteralPath $recT)) {
            throw ('an unconfirmed version probe must stop before refresh and keep its record: rc=' + $r.Rc + ' step=' + $r.Json.step + ' calls=' + $r.Calls.Count)
        }
    } finally {
        $script = $realScript
        if (Test-Path -LiteralPath $env:WP714_LINGER_PID) {
            Stop-Process -Id ([int](Get-Content -LiteralPath $env:WP714_LINGER_PID -Raw)) -Force -ErrorAction SilentlyContinue
        }
        Remove-Item -LiteralPath $recT -ErrorAction SilentlyContinue
        Remove-Item Env:WP714_LINGER_PID -ErrorAction SilentlyContinue
    }
    $cases++
    # >>case:t
    # <<case:u
    # (u) Linux, real script: descendants that CLEARED the marker are still part of the operation. The wrapper is
    #     a child subreaper, so an orphan is adopted and found by parent link: the version probe's pipe-holding
    #     grandchild is stopped and confirmed (run continues), and a pipe-less daemon is stopped before the canary.
    if ($IsLinux) {
        $env:WP714_LINGER_PID = Join-Path $root 'version-linger.pid'
        $env:WP714_BEAT_FILE = Join-Path $root 'scrub-beats.txt'
        $env:WP714_CHILD_PID_FILE = Join-Path $root 'scrub.pid'
        $env:WP710_TIMELOG = Join-Path $root 'scrub-times.log'
        Remove-Item -LiteralPath $env:WP714_BEAT_FILE, $env:WP710_TIMELOG -ErrorAction SilentlyContinue
        try {
            $r = Invoke-Wrapper 'version_linger' @('-TimeoutSeconds','2')
            $v = $r.Json.steps.version
            $lingerU = [int](Get-Content -LiteralPath $env:WP714_LINGER_PID -Raw)
            $aliveU = $null -ne (Get-Process -Id $lingerU -ErrorAction SilentlyContinue)
            if ($aliveU) { try { $aliveU = [IO.File]::ReadAllText("/proc/$lingerU/stat") -notmatch '\)\s+Z\s' } catch { $aliveU = $false } }
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.tree_measurement -ne 'linux_subreaper_and_marker' -or
                $v.timeout -ne $true -or $v.child_confirmed_exited -ne $true -or $v.descendants_stopped -lt 1 -or $aliveU) {
                throw ('Linux: a marker-less pipe holder of the version probe must be found and stopped: rc=' + $r.Rc + ' ' + ($v | ConvertTo-Json -Compress))
            }
            $r = Invoke-Wrapper 'hang_orphan' @('-TimeoutSeconds','1')
            $orphanU = [int](Get-Content -LiteralPath $env:WP714_LINGER_PID -Raw)
            $aliveO = $null -ne (Get-Process -Id $orphanU -ErrorAction SilentlyContinue)
            if ($aliveO) { try { $aliveO = [IO.File]::ReadAllText("/proc/$orphanU/stat") -notmatch '\)\s+Z\s' } catch { $aliveO = $false } }
            if ($r.Rc -ne 3 -or $r.Json.steps.refresh.child_confirmed_exited -ne $true -or $aliveO) {
                throw ('Linux: an orphan that Kill($true) cannot reach must be stopped and confirmed on timeout: rc=' + $r.Rc + ' alive=' + $aliveO)
            }
            Remove-Item -LiteralPath $env:WP714_BEAT_FILE, $env:WP710_TIMELOG -ErrorAction SilentlyContinue   # per run, not per case
            $r = Invoke-Wrapper 'scrub_daemon' @('-TimeoutSeconds','5')
            $startNb = [double]((@(Get-Content -LiteralPath $env:WP710_TIMELOG) | Where-Object { $_ -like 'start notebook *' } | Select-Object -First 1) -split ' ')[2]
            $late = @(Get-Content -LiteralPath $env:WP714_BEAT_FILE | Where-Object { [double]$_ -gt $startNb })
            if ($r.Rc -ne 0 -or $r.Json.steps.refresh.descendants_stopped -lt 1 -or $late.Count -ne 0) {
                throw ('Linux: a marker-less pipe-less descendant must be stopped before the canary: rc=' + $r.Rc + ' late=' + $late.Count)
            }
        } finally {
            foreach ($f in @($env:WP714_LINGER_PID, $env:WP714_CHILD_PID_FILE)) {
                if (Test-Path -LiteralPath $f) { Stop-Process -Id ([int](Get-Content -LiteralPath $f -Raw)) -Force -ErrorAction SilentlyContinue }
            }
            Remove-Item Env:WP714_LINGER_PID, Env:WP714_BEAT_FILE, Env:WP714_CHILD_PID_FILE, Env:WP710_TIMELOG -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:u
    # lop: linux-subreaper-khong-thu-hoi-zombie
    # <<case:v
    # Reuse daemon; measure cleanup while the keepalive owner still lives.
    if ($IsLinux) {
        $env:WP710_MODE = 'daemon'; $env:WP710_DELAY = '0'
        $env:WP714_BEAT_FILE = Join-Path $root 'reap-beats.txt'
        $env:WP714_CHILD_PID_FILE = Join-Path $root 'reap-child.pid'
        $ownerV = $null; $childV = $null
        $outV = Join-Path $root 'reap-owner.out'
        $errV = Join-Path $root 'reap-owner.err'
        try {
            $argsV = '-NoProfile -File "' + $script + '" -ConfigPath "' + $config + '" -NlmCommand "' + $python + '" -NlmArgumentsPrefix "' + $fake + '" -StageCommand "' + $python + '" -StageArguments "' + $fake + '" -TimeoutSeconds 5 -EnableKeepalive -IntervalSeconds 10 -MaxCycles 2'
            $ownerV = Start-Process -FilePath (Get-Command pwsh).Source -ArgumentList $argsV -PassThru -RedirectStandardOutput $outV -RedirectStandardError $errV
            $firstV = $null
            for ($i=0; $i -lt 120 -and $null -eq $firstV; $i++) {
                $lineV = Get-Content -LiteralPath $outV -ErrorAction SilentlyContinue | Select-Object -First 1
                if ($lineV) { $firstV = $lineV | ConvertFrom-Json }
                if ($null -eq $firstV) { Start-Sleep -Milliseconds 100 }
            }
            if ($null -eq $firstV -or $firstV.status -ne 'staged' -or $ownerV.HasExited) { throw 'zombie fixture did not reach a live keepalive interval' }
            $childV = [int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)
            Start-Sleep -Milliseconds 500
            if (Test-Path -LiteralPath "/proc/$childV/stat") {
                throw ('subreaper must reap its stopped adopted descendant before keepalive sleeps: ' + [IO.File]::ReadAllText("/proc/$childV/stat"))
            }
        } finally {
            if ($null -ne $ownerV -and -not $ownerV.HasExited) { Stop-Process -Id $ownerV.Id -Force -ErrorAction SilentlyContinue; $ownerV.WaitForExit() }
            if ($null -ne $childV) { Stop-Process -Id $childV -Force -ErrorAction SilentlyContinue }
            Remove-Item Env:WP714_BEAT_FILE, Env:WP714_CHILD_PID_FILE -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:v
    # lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con (WP714 round 4)
    # <<case:w
    # (w) Linux, real script: the owner is killed while a descendant that CLEARED the marker and DROPPED the pipes
    #     still runs; the owner's parent is a child subreaper (as a terminal multiplexer or systemd --user is), so
    #     the orphan is adopted by a living ancestor of the dead owner. Nothing proves that process unrelated: the
    #     next owner is quarantined as tree_unknown, the timer does NOT release it, a malformed operator reason is
    #     refused at preflight, and a well-formed one releases it with the reason in the evidence.
    if ($IsLinux) {
        $env:WP714_BEAT_FILE = Join-Path $root 'escape-beats.txt'
        $env:WP714_CHILD_PID_FILE = Join-Path $root 'escape.pid'
        $ownerFileW = Join-Path $root 'escape-owner.pid'
        Remove-Item -LiteralPath $env:WP714_BEAT_FILE, $env:WP714_CHILD_PID_FILE, $ownerFileW -ErrorAction SilentlyContinue
        $helperW = $null; $childW = $null
        try {
            $env:WP710_MODE = 'scrub_daemon_hold'; $env:WP710_DELAY = '0'
            $psiW = [Diagnostics.ProcessStartInfo]::new($python)
            $helperCode = 'import ctypes, subprocess, sys, time; ctypes.CDLL(None).prctl(36, 1, 0, 0, 0); p = subprocess.Popen(sys.argv[2:]); open(sys.argv[1], "w").write(str(p.pid)); time.sleep(120)'
            foreach ($a in @('-c', $helperCode, $ownerFileW, (Get-Command pwsh).Source, '-NoProfile', '-File', $script, '-ConfigPath', $config,
                             '-NlmCommand', $python, '-NlmArgumentsPrefix', $fake, '-StageCommand', $python, '-StageArguments', $fake, '-TimeoutSeconds', '20')) {
                $psiW.ArgumentList.Add($a)
            }
            $psiW.UseShellExecute = $false
            $helperW = [Diagnostics.Process]::Start($psiW)
            for ($i=0; $i -lt 150 -and -not (Test-Path -LiteralPath $env:WP714_CHILD_PID_FILE); $i++) { Start-Sleep -Milliseconds 100 }
            if (-not (Test-Path -LiteralPath $env:WP714_CHILD_PID_FILE)) { throw 'escape fixture never started' }
            $childW = [int](Get-Content -LiteralPath $env:WP714_CHILD_PID_FILE -Raw)
            $recordW = Get-Content -LiteralPath (Join-Path ([IO.Path]::GetTempPath()) $recName) -Raw | ConvertFrom-Json
            Stop-Process -Id ([int](Get-Content -LiteralPath $ownerFileW -Raw)) -Force
            $directGoneW = $false
            for ($i=0; $i -lt 50 -and -not $directGoneW; $i++) {
                try { $directGoneW = [IO.File]::ReadAllText("/proc/$([int]$recordW.pid)/stat") -match '\)\s+Z\s' } catch { $directGoneW = $true }
                if (-not $directGoneW) { Start-Sleep -Milliseconds 100 }
            }
            if (-not $directGoneW) { throw 'fixture direct CLI did not exit' }
            $statW = [IO.File]::ReadAllText("/proc/$childW/stat")
            if ($statW -notmatch ('\)\s+[RS]\s+' + $helperW.Id + '\s')) { throw ('fixture orphan was not adopted by the subreaper ancestor: ' + $statW) }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'tree_unknown' -or $r.Calls.Count -ne 0) {
                throw ('an orphan that cleared the marker and dropped the pipes must quarantine the next owner: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason)
            }
            Start-Sleep -Milliseconds 1200
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-UnconfirmedQuarantineSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Calls.Count -ne 0) { throw ('the quarantine timer must not release an unknown tree: rc=' + $r.Rc) }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','x')
            if ($r.Rc -ne 4 -or $r.Json.step -ne 'preflight' -or $r.Calls.Count -ne 0) { throw 'a malformed operator reason must be refused before any operation' }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case w by hand')
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'operator_release' -or
                $r.Json.takeover_reason -ne 'tree_unknown' -or $r.Json.operator_reason -ne 'operator checked case w by hand') {
                throw ('an operator release must stage and say so: rc=' + $r.Rc + ' takeover=' + $r.Json.takeover)
            }
        } finally {
            if ($null -ne $childW) { Stop-Process -Id $childW -Force -ErrorAction SilentlyContinue }
            if ($null -ne $helperW) { Stop-Process -Id $helperW.Id -Force -ErrorAction SilentlyContinue; $helperW.WaitForExit() }
            Remove-Item Env:WP714_BEAT_FILE, Env:WP714_CHILD_PID_FILE -ErrorAction SilentlyContinue
            Remove-Item -LiteralPath (Join-Path ([IO.Path]::GetTempPath()) $recName) -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:w
    # lop: khoa-va-timeout-khong-rang-buoc-cay-tien-trinh-con (WP710 g4, Windows native)
    # <<case:x
    # (x) Windows, real script and a REAL Job Object built with the script's own type: a record naming a job that
    #     still has a member blocks the next owner (job_alive), and an operator release never releases it; when
    #     the job's holder dies the job closes, its member dies with it, and the next owner takes over. A record
    #     whose owner had already FAILED to empty its job (tree_unconfirmed) is not cleared by the job being
    #     closed: quarantine, no timer exit, operator only. A job name of any other shape is not measured.
    if ($IsWindows) {
        $srcX = Get-Content -LiteralPath $script -Raw
        $typeX = [regex]::Match($srcX, "(?s)Add-Type -TypeDefinition @'\r?\n(.*?)\r?\n'@").Groups[1].Value
        $prefixX = [regex]::Match($srcX, "JobPrefix\s*=\s*'([^']+)'").Groups[1].Value
        if (-not $typeX -or -not $prefixX) { throw 'job type or job name prefix not found in the script' }
        $typeFileX = Join-Path $root 'job-type.cs'
        Set-Content -LiteralPath $typeFileX -Value $typeX -Encoding utf8
        $holderScriptX = Join-Path $root 'job-holder.ps1'
        @'
param([string]$Source, [string]$Name, [string]$Python, [string]$Ready)
Add-Type -TypeDefinition (Get-Content -LiteralPath $Source -Raw)
$code = 0
$job = [TraLuatWp710.Job]::Create($Name, [ref]$code)
$stage = ''
$childId = 0
$child = [TraLuatWp710.Job]::Start($job, [TraLuatWp710.Job]::Quote([string[]]@($Python, '-c', 'import time; time.sleep(120)')),
    [TraLuatWp710.Job]::EnvironmentBlock([Environment]::GetEnvironmentVariables()), [ref]$stage, [ref]$code, [ref]$childId)
[void][TraLuatWp710.Job]::Resume($child)
Set-Content -LiteralPath $Ready -Value $child.Id
Start-Sleep -Seconds 120
'@ | Set-Content -LiteralPath $holderScriptX
        $recX = Join-Path ([IO.Path]::GetTempPath()) $recName
        $jobX = $prefixX + [guid]::NewGuid().ToString('N')
        $readyX = Join-Path $root 'job-holder.ready'
        $holderX = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $holderScriptX + '" -Source "' + $typeFileX + '" -Name "' + $jobX + '" -Python "' + $python + '" -Ready "' + $readyX + '"') -PassThru @hidden
        $memberX = $null
        try {
            for ($i=0; $i -lt 200 -and -not (Test-Path -LiteralPath $readyX); $i++) { Start-Sleep -Milliseconds 100 }
            if (-not (Test-Path -LiteralPath $readyX)) { throw 'job holder fixture never started' }
            $memberX = [int](Get-Content -LiteralPath $readyX -Raw)
            $writeX = { param($job, $unconfirmed) @{format=2; marker=[guid]::NewGuid().ToString('N'); pid=$null; start_ticks=$null; tree_unconfirmed=$unconfirmed; job=$job} | ConvertTo-Json -Compress | Set-Content -LiteralPath $recX }
            & $writeX $jobX $false
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Json.takeover_reason -ne 'job_alive' -or $r.Calls.Count -ne 0) {
                throw ('a job that still has a member must block the next owner: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason)
            }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked the old job')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Json.takeover -ne 'none' -or $r.Calls.Count -ne 0) { throw 'an operator release must never release a job that still has a member' }
            if ($null -eq (Get-Process -Id $memberX -ErrorAction SilentlyContinue)) { throw 'fixture: asking the job for its count must not end its member' }
            Stop-Process -Id $holderX.Id -Force
            $holderX.WaitForExit()
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','5')
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'none') { throw ('a closed job must be a plain takeover: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason) }
            if ($null -ne (Get-Process -Id $memberX -ErrorAction SilentlyContinue)) { throw 'the member of a closed job is still alive: KILL_ON_JOB_CLOSE did not hold' }
            & $writeX ($prefixX + [guid]::NewGuid().ToString('N')) $true
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'job_closed_unconfirmed' -or $r.Calls.Count -ne 0) {
                throw ('a job its owner could not empty is not cleared by being closed: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason)
            }
            Start-Sleep -Milliseconds 1200
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-UnconfirmedQuarantineSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Calls.Count -ne 0) { throw 'the timer must not release an unconfirmed job' }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case x by hand')
            if ($r.Rc -ne 0 -or $r.Json.takeover -ne 'operator_release' -or $r.Json.takeover_reason -ne 'job_closed_unconfirmed') { throw 'an operator release of an unconfirmed job must stage and say so' }
            & $writeX 'Global\tra_luat_other_job' $false
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'tree_not_measurable' -or $r.Calls.Count -ne 0) { throw 'a job name of another shape must not be measured' }
        } finally {
            if (-not $holderX.HasExited) { Stop-Process -Id $holderX.Id -Force -ErrorAction SilentlyContinue }
            if ($null -ne $memberX) { Stop-Process -Id $memberX -Force -ErrorAction SilentlyContinue }
            Remove-Item -LiteralPath $recX -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:x
    # <<case:y
    # (y) Windows: no job, no step. Projection: the script's one job-name prefix replaced by a name the kernel
    #     refuses (measured: error 3). The run stops at its first step with rc 5 and the reason, starts no child
    #     (the fake CLI logs nothing, the version file is never written) and leaves no record.
    if ($IsWindows) {
        $srcY = Get-Content -LiteralPath $script -Raw
        $prefixLineY = "`$JobPrefix = 'Global\tra_luat_nlm_op_'"
        if (([regex]::Matches($srcY, [regex]::Escape($prefixLineY))).Count -ne 1) { throw 'job name prefix line not found exactly once in the script' }
        $projY = Join-Path $root 'projection-y'
        New-Item -ItemType Directory -Path $projY | Out-Null
        $projScriptY = Join-Path $projY 'nlm-credential-refresh.ps1'
        Set-Content -LiteralPath $projScriptY -Value $srcY.Replace($prefixLineY, "`$JobPrefix = 'Global\no\such\'") -Encoding utf8
        $recY = Join-Path ([IO.Path]::GetTempPath()) $recName
        $realScriptY = $script
        $env:WP714_LINGER_PID = Join-Path $root 'no-job.pid'
        try {
            $script = $projScriptY
            $r = Invoke-Wrapper 'version_linger' @('-TimeoutSeconds','5')
            if ($r.Rc -ne 5 -or $r.Json.status -ne 'inconclusive' -or $r.Json.step -ne 'tree_containment' -or
                $r.Json.containment_reason -notmatch '^job_create_failed:\d+$' -or $r.Json.steps.version.tree_state -ne 'not_contained' -or
                $r.Calls.Count -ne 0 -or (Test-Path -LiteralPath $env:WP714_LINGER_PID) -or (Test-Path -LiteralPath $recY)) {
                throw ('without a job no step may start: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.containment_reason)
            }
        } finally {
            $script = $realScriptY
            Remove-Item -LiteralPath $recY -ErrorAction SilentlyContinue
            Remove-Item Env:WP714_LINGER_PID -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:y
    # <<case:z
    # (z) Windows, g5: two failure paths the reviewer of g4 found by reading the control flow.
    #     z1 - the child was created but could not be placed in the job AND its termination was not confirmed
    #     (projection: the assignment always "fails" and the terminate call is removed, so the suspended child
    #     really stays). The run stops with rc 5, and the record must SURVIVE and name that child: the next
    #     owner waits on it (root_alive), an operator cannot release it while it lives, and after it is gone
    #     the record is a quarantine (its owner never emptied anything), released only by the operator.
    #     z2 - the stage command RAN and then its job count could not be read (projection: the count reads -1
    #     once the fake stage command has written a flag). `inconclusive` promises zero stage calls, so this
    #     must be stage_failure (rc 6) with the containment reason, and the record must stay.
    if ($IsWindows) {
        $srcZ = Get-Content -LiteralPath $script -Raw
        # If Get-Process cannot resolve a created, suspended child, its CreateProcess PID and
        # outside_job flag must still survive in the record; an empty job cannot clear it.
        $recordFnZ = [regex]::Match($srcZ, '(?s)(function Write-OperationRecord\(.*?\r?\n\})\r?\n\r?\nfunction Get-StepPipes')
        if (-not $recordFnZ.Success) { throw 'fixture: record writer not found' }
        $recordProbePathZ = Join-Path $root 'record-null-lookup.json'
        try {
            $recordProbeZ = & {
                param($functionText, $destination)
                $OperationRecord = $destination
                $OwnerStartJiffies = $null; $OwnerChain = $null; $TreeMeasurable = $false
                . ([scriptblock]::Create($functionText))
                Write-OperationRecord 'probe' $null $true @() 'probe-job' 4242
                Get-Content -LiteralPath $destination -Raw | ConvertFrom-Json
            } $recordFnZ.Groups[1].Value $recordProbePathZ
            if ($recordProbeZ.pid -ne 4242 -or $recordProbeZ.outside_job -ne $true -or $recordProbeZ.tree_unconfirmed -ne $true) {
                throw ('a failed process lookup must keep the stray PID and outside-job flag: ' + ($recordProbeZ | ConvertTo-Json -Compress))
            }
        } finally { Remove-Item -LiteralPath $recordProbePathZ -ErrorAction SilentlyContinue }
        $recZ = Join-Path ([IO.Path]::GetTempPath()) $recName
        $realScriptZ = $script
        $assignZ = 'if (!AssignProcessToJobObject(job, pi.hProcess)) { error'
        $killZ = 'TerminateProcess(pi.hProcess, 1);'
        foreach ($needle in @($assignZ, $killZ)) {
            if (([regex]::Matches($srcZ, [regex]::Escape($needle))).Count -ne 1) { throw ('projection anchor not found exactly once: ' + $needle) }
        }
        $projZ1 = Join-Path $root 'projection-z1'
        New-Item -ItemType Directory -Path $projZ1 | Out-Null
        Set-Content -LiteralPath (Join-Path $projZ1 'nlm-credential-refresh.ps1') -Encoding utf8 -Value $srcZ.Replace($assignZ, 'if (job != IntPtr.Zero) { error').Replace($killZ, '')
        $strayZ = $null
        try {
            # Run through a PIPE with a deadline instead of Invoke-Wrapper: the stray child must not have inherited
            # the wrapper's own stdout. If it had, this read would never end (g5 measured 13 minutes before the
            # handle list); here that is a red case, not a hung suite.
            $env:WP710_MODE = 'ok'; $env:WP710_TAG = ''
            Remove-Item -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue
            $psiZ = [Diagnostics.ProcessStartInfo]::new($powershell)
            foreach ($a in @('-NoProfile','-File',(Join-Path $projZ1 'nlm-credential-refresh.ps1'),'-ConfigPath',$config,'-NlmCommand',$python,
                             '-NlmArgumentsPrefix',$fake,'-StageCommand',$python,'-StageArguments',$fake,'-TimeoutSeconds','5')) { $psiZ.ArgumentList.Add($a) }
            $psiZ.UseShellExecute = $false; $psiZ.RedirectStandardOutput = $true
            $runZ = [Diagnostics.Process]::Start($psiZ)
            $readZ = $runZ.StandardOutput.ReadToEndAsync()
            $closedZ = $readZ.Wait(90000)
            if (-not $closedZ) {
                try { $strayZ = [int](Get-Content -LiteralPath $recZ -Raw | ConvertFrom-Json).pid } catch { }
                if ($null -ne $strayZ) { Stop-Process -Id $strayZ -Force -ErrorAction SilentlyContinue }
                if (-not $runZ.HasExited) { $runZ.Kill($true) }
                throw 'the stray child inherited the wrapper stdout: the caller never saw the end of the output'
            }
            $runZ.WaitForExit()
            $r = [pscustomobject]@{ Rc = $runZ.ExitCode; Json = (@($readZ.Result -split "`n" | Where-Object { $_.Trim() })[-1] | ConvertFrom-Json)
                Calls = @(Get-Content -LiteralPath $env:WP710_LOG -ErrorAction SilentlyContinue) }
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_containment' -or $r.Json.containment_reason -notmatch '^job_assign_alive_failed:\d+$' -or $r.Calls.Count -ne 0) {
                throw ('a child that could not be placed in the job must stop the run: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.containment_reason)
            }
            if (-not (Test-Path -LiteralPath $recZ)) { throw 'the record of a stray suspended child was deleted' }
            $writtenZ = Get-Content -LiteralPath $recZ -Raw | ConvertFrom-Json
            if ($null -eq $writtenZ.pid -or $writtenZ.tree_unconfirmed -ne $true -or $writtenZ.outside_job -ne $true) { throw ('the record must name the stray child, be unconfirmed and say it is outside the job: ' + ($writtenZ | ConvertTo-Json -Compress)) }
            $strayZ = [int]$writtenZ.pid
            if ($null -eq (Get-Process -Id $strayZ -ErrorAction SilentlyContinue)) { throw 'fixture: the stray suspended child is not there, the case would pass vacuously' }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case z by hand')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'lock_busy' -or $r.Json.takeover_reason -ne 'root_alive' -or $r.Json.takeover -ne 'none' -or $r.Calls.Count -ne 0) {
                throw ('a live stray child must block the next owner, operator or not: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason)
            }
            # Reviewer round 5: the same stray child, but its start time could not be read (start_ticks null), while
            # ANOTHER process still holds the - empty - job of that name. The job then answers "0 members", which
            # is true and says nothing about a child that was never in it: the next owner must not take over.
            $jobZ = $prefixX + [guid]::NewGuid().ToString('N')
            $emptyHolderZ = Join-Path $root 'empty-job-holder.ps1'
            @'
param([string]$Source, [string]$Name, [string]$Ready)
Add-Type -TypeDefinition (Get-Content -LiteralPath $Source -Raw)
$code = 0
$job = [TraLuatWp710.Job]::Create($Name, [ref]$code)
Set-Content -LiteralPath $Ready -Value ([TraLuatWp710.Job]::Active($job))
Start-Sleep -Seconds 120
'@ | Set-Content -LiteralPath $emptyHolderZ
            $readyZ = Join-Path $root 'empty-job.ready'
            $holderZ = Start-Process -FilePath $powershell -ArgumentList ('-NoProfile -File "' + $emptyHolderZ + '" -Source "' + $typeFileX + '" -Name "' + $jobZ + '" -Ready "' + $readyZ + '"') -PassThru @hidden
            try {
                for ($i=0; $i -lt 200 -and -not (Test-Path -LiteralPath $readyZ); $i++) { Start-Sleep -Milliseconds 100 }
                if (-not (Test-Path -LiteralPath $readyZ) -or [int](Get-Content -LiteralPath $readyZ -Raw) -ne 0) { throw 'fixture: the empty job holder did not start with 0 members' }
                $writtenZ.start_ticks = $null; $writtenZ.job = $jobZ
                $writtenZ | ConvertTo-Json -Compress | Set-Content -LiteralPath $recZ
                $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
                if ($null -eq (Get-Process -Id $strayZ -ErrorAction SilentlyContinue) -or $holderZ.HasExited) { throw 'fixture: the stray child or the empty job holder ended early' }
                if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'stray_child_unconfirmed' -or $r.Calls.Count -ne 0) {
                    throw ('an empty job proves nothing about a child that was never in it: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason + ' calls=' + $r.Calls.Count)
                }
            } finally { if (-not $holderZ.HasExited) { Stop-Process -Id $holderZ.Id -Force -ErrorAction SilentlyContinue } }
            Stop-Process -Id $strayZ -Force
            for ($i=0; $i -lt 50 -and $null -ne (Get-Process -Id $strayZ -ErrorAction SilentlyContinue); $i++) { Start-Sleep -Milliseconds 100 }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1')
            if ($r.Rc -ne 5 -or $r.Json.step -ne 'tree_quarantine' -or $r.Json.takeover_reason -ne 'stray_child_unconfirmed' -or $r.Calls.Count -ne 0) {
                throw ('an unconfirmed record stays a quarantine after its child is gone: rc=' + $r.Rc + ' step=' + $r.Json.step + ' reason=' + $r.Json.takeover_reason)
            }
            $r = Invoke-Wrapper 'ok' @('-TimeoutSeconds','5','-LockWaitSeconds','1','-OperatorReleaseReason','operator checked case z by hand')
            if ($r.Rc -ne 0 -or $r.Json.status -ne 'staged' -or $r.Json.takeover -ne 'operator_release') { throw 'an operator release after the stray child is gone must stage' }
        } finally {
            $script = $realScriptZ
            if ($null -ne $strayZ) { Stop-Process -Id $strayZ -Force -ErrorAction SilentlyContinue }
            Remove-Item -LiteralPath $recZ -ErrorAction SilentlyContinue
        }
        $countZ = "    `$active = [TraLuatWp710.Job]::Active(`$job)`n    if (`$active -lt 0) { return @{ State = 'unknown'; Stopped = 0 } }"
        if (([regex]::Matches($srcZ.Replace("`r`n", "`n"), [regex]::Escape($countZ))).Count -ne 1) { throw 'job count line not found exactly once in the script' }
        $env:WP710_FLAG = Join-Path $root 'stage-ran.flag'
        $projZ2 = Join-Path $root 'projection-z2'
        New-Item -ItemType Directory -Path $projZ2 | Out-Null
        $readZ = "    `$active = if (Test-Path -LiteralPath '$($env:WP710_FLAG)') { -1 } else { [TraLuatWp710.Job]::Active(`$job) }`n    if (`$active -lt 0) { return @{ State = 'unknown'; Stopped = 0 } }"
        Set-Content -LiteralPath (Join-Path $projZ2 'nlm-credential-refresh.ps1') -Encoding utf8 -Value $srcZ.Replace("`r`n", "`n").Replace($countZ, $readZ)
        try {
            $script = Join-Path $projZ2 'nlm-credential-refresh.ps1'
            $r = Invoke-Wrapper 'stage_flag' @('-TimeoutSeconds','5')
            $script = $realScriptZ
            $stageCallsZ = @($r.Calls | Where-Object { $_ -like 'start:stage:*' }).Count
            if (-not (Test-Path -LiteralPath $env:WP710_FLAG) -or $stageCallsZ -ne 1) { throw ('fixture: the stage command did not run: calls=' + $stageCallsZ) }
            if ($r.Rc -ne 6 -or $r.Json.status -ne 'stage_failure' -or $r.Json.step -ne 'stage' -or $r.Json.containment_reason -ne 'job_unknown' -or
                $r.Json.steps.stage.tree_state -ne 'unknown') {
                throw ('a stage command that ran must never end as inconclusive: rc=' + $r.Rc + ' status=' + $r.Json.status + ' step=' + $r.Json.step + ' reason=' + $r.Json.containment_reason)
            }
            if (-not (Test-Path -LiteralPath $recZ) -or (Get-Content -LiteralPath $recZ -Raw | ConvertFrom-Json).tree_unconfirmed -ne $true) { throw 'a stage whose tree is unproven must keep its record' }
        } finally {
            $script = $realScriptZ
            Remove-Item -LiteralPath $recZ, $env:WP710_FLAG -ErrorAction SilentlyContinue
            Remove-Item Env:WP710_FLAG -ErrorAction SilentlyContinue
        }
        $cases++
    }
    # >>case:z
    "passed=$cases failed=0"
} finally {
    Remove-Item -LiteralPath $root -Recurse -Force -ErrorAction SilentlyContinue
}
