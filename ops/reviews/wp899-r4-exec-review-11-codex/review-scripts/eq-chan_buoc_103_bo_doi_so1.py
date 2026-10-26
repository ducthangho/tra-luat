"""Thu provenance CI §10.2.2 từ REST và log job — packet #899 (wp899 P-A), đặc tả `ops/specs/wp899-r4.md` (thay r3).

`thu --repo o/r --run ID --attempt N --out DIR` ghi bốn mốc TÁCH BẠCH (Run · Checkout · Gate output · Workflow definition)
vào `DIR/provenance.yaml`. Chỉ REST; mọi lời gọi mạng đi qua MỘT hàm tiêm vào `goi(url) -> (mã HTTP, byte)` để test chạy
offline. Năm trạng thái §10.2.3: thiếu dữ liệu là `not_measured`, không bao giờ là `passed`. Mốc Workflow definition luôn
`not_measured` (GraphQL bị chặn trong phiên Claude; việc của P-B). SHA checkout đọc từ LOG, không lấy `head_sha` của REST.
r3 (F02): kịch bản của bước lấy từ `run:` của workflow tại SHA checkout ĐÃ ĐO (`git cat-file blob <sha>:<path REST>`). r4 (F02):
bước của mỗi nhóm log được ĐỊNH DANH qua REST `steps[]` + vị trí (`ghep_buoc`), không tìm ứng viên trùng chữ trên toàn workflow. Gốc tin là nội dung tại SHA ấy — workflow tại SHA vốn quyết định được mọi output, công cụ không chống nó.
Thoát: 0 không mốc nào `failed` · 12 có `failed` · 2 sai đối số · 3 REST khác 2xx (in nguyên mã). LUÔN in `NOT_MEASURED: <n>`;
rc 2/3 không sinh provenance nên cả bốn mốc là chưa đo (`NOT_MEASURED: 4` kèm `PROVENANCE: khong_sinh`).
"""
import argparse, datetime, hashlib, importlib.util, json, os, re, shutil, subprocess, sys, tempfile, urllib.error, urllib.request
from pathlib import Path
import yaml
for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, 'reconfigure'):
        _s.reconfigure(encoding='utf-8', errors='backslashreplace')
ROOT = Path(__file__).resolve().parent.parent
CI_DANG_KY = ROOT / '.claude/dev/ci_dang_ky_test.py'
API = 'https://api.github.com'
TRANG = 100
TRANG_TOI_DA = 1000
TS = '[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}(?:\\.[0-9]+)?Z'
RE_DONG = re.compile(f'^({TS}) ?(.*)$')
RE_SHA = re.compile(f'^{TS} ([0-9a-f]{{40}})$')
RE_GIO = re.compile('[0-9]{4}-[0-9]{2}-[0-9]{2}T[0-9]{2}:[0-9]{2}:[0-9]{2}Z')
RE_ANSI = re.compile('\\x1b\\[[0-9;]*m')
RE_HEX40 = re.compile('^[0-9a-f]{40}$')
RE_REPO = re.compile('^[\\w.-]+/[\\w.-]+$')
LY_DO_WD = 'graphql_bi_chan_trong_phien_claude; cho P-B'
KET_BUOC = ('success', 'failure', 'cancelled', 'skipped', 'neutral')
LOI_JOB = ('failure', 'cancelled', 'timed_out', 'action_required', 'startup_failure', 'stale')
RE_CHECK_RUN = re.compile('^https://api\\.github\\.com/repos/[\\w.-]+/[\\w.-]+/check-runs/[1-9]\\d*$')
RE_LOI_GOI = re.compile('^((?:[A-Za-z_]\\w*=[\\w./:-]*\\s+)*)(?:[\\w./-]*/)?python(?:\\d+(?:\\.\\d+)*)?(?:\\s+-[BuIsSEOqb]+)*\\s+(?:\\./)?([\\w.-]+(?:/[\\w.-]+)*\\.py)$')
KHOA_BUOC = {'name', 'id', 'if', 'run', 'shell', 'timeout-minutes', 'continue-on-error'}

def _so(v, nho=0):
    return type(v) is int and v >= nho

def _chuoi(v):
    return type(v) is str and v.strip() != ''
RUN_BAT_BUOC = {'id': lambda v: _so(v, 1), 'run_attempt': lambda v: _so(v, 1), 'event': _chuoi, 'path': _chuoi, 'head_sha': lambda v: _chuoi(v) and bool(RE_HEX40.fullmatch(v)), 'check_suite_id': lambda v: _so(v, 1)}
JOB_BAT_BUOC = {'name': _chuoi, 'runner_id': lambda v: _so(v, 1), 'runner_name': _chuoi, 'conclusion': lambda v: v == 'success', 'labels': lambda v: type(v) is list and bool(v) and all((_chuoi(x) for x in v)), 'check_run_url': lambda v: _chuoi(v) and bool(RE_CHECK_RUN.fullmatch(v)), 'steps': lambda v: type(v) is list and bool(v) and all((type(b) is dict and _chuoi(b.get('name')) and (b.get('conclusion') in KET_BUOC) for b in v))}
ART_BAT_BUOC = {'name': _chuoi, 'size_in_bytes': _so, 'expired': lambda v: type(v) is bool, 'digest': lambda v: v is None or (_chuoi(v) and v.startswith('sha256:'))}
KHONG_SINH = 'NOT_MEASURED: 4\nPROVENANCE: khong_sinh (ca bon moc chua do)'

class LoiRest(Exception):

    def __init__(self, ma, url):
        super().__init__(f'REST {ma} {url}')
        self.ma, self.url = (ma, url)

class _KhongChuyenHuong(urllib.request.HTTPRedirectHandler):

    def redirect_request(self, *a, **k):
        return None

def goi_that(url):
    """GET REST. Log job trả 302 sang kho blob: theo TAY và KHÔNG mang token sang host khác."""
    tk = next((os.environ[k] for k in ('GITHUB_PAT', 'GH_TOKEN', 'GITHUB_TOKEN') if os.environ.get(k)), None)
    hd = {'Accept': 'application/vnd.github+json', 'X-GitHub-Api-Version': '2022-11-28'}
    if tk:
        hd['Authorization'] = f'Bearer {tk}'
    yeu_cau, mo = (urllib.request.Request(url, headers=hd), urllib.request.build_opener(_KhongChuyenHuong).open)
    for _ in range(2):
        try:
            with mo(yeu_cau, timeout=120) as r:
                return (r.status, r.read())
        except urllib.error.HTTPError as e:
            loc = e.headers.get('Location') if e.code in (301, 302, 303, 307, 308) else None
            if not loc or mo is urllib.request.urlopen:
                return (e.code, b'')
            yeu_cau, mo = (loc, urllib.request.urlopen)
        except (urllib.error.URLError, OSError) as e:
            raise LoiRest(f'khong_ket_noi ({e})', url)

def lay(goi, url):
    ma, byte = goi(url)
    if not (isinstance(ma, int) and 200 <= ma < 300):
        raise LoiRest(ma, url)
    return byte

def lay_json(goi, url):
    """(đối tượng, byte nguyên văn)."""
    byte = lay(goi, url)
    try:
        return (json.loads(byte), byte)
    except ValueError:
        raise LoiRest('than_khong_phai_json', url)

def lay_trang(goi, url, khoa):
    """Đọc tới trang NGẮN hơn `TRANG`. Đủ ⇔ số ID DUY NHẤT = `total_count` và total không đổi giữa trang; thiếu, trùng,
    total đổi hay chạm `TRANG_TOI_DA` ⇒ `du: False` (không suy gì về phần thiếu; mốc tập hợp `not_measured`)."""
    ds, ids, tong, trang, du = ([], set(), None, 1, True)
    try:
        while True:
            d = lay_json(goi, f'{url}?per_page={TRANG}&page={trang}')[0]
            if not (_so(d['total_count']) and type(d[khoa]) is list and all((type(x) is dict and _so(x['id'], 1) for x in d[khoa]))):
                raise TypeError(f'total_count/{khoa}/id sai kiểu')
            du, tong = (du and tong in (None, d['total_count']), d['total_count'])
            for x in d[khoa]:
                du = du and x['id'] not in ids
                if x['id'] not in ids:
                    ids.add(x['id'])
                    ds.append(x)
            if len(d[khoa]) < TRANG or trang >= TRANG_TOI_DA:
                return {'total_count': tong, khoa: ds, 'du': du and len(ids) == tong and (len(d[khoa]) < TRANG)}
            trang += 1
    except (KeyError, TypeError) as e:
        raise LoiRest(f'than_sai_dang ({e!r})', url)

def tap(d, khoa, bat_buoc=None):
    sai = sorted({k for x in d[khoa] for k, hop_le in (bat_buoc or {}).items() if not hop_le(x.get(k))})
    return {'trang_thai': 'passed' if d['du'] and (not sai) else 'not_measured', 'total_count': d['total_count'], 'so_id': len(d[khoa]), 'truong_sai': sai}

def doc_moi(duong=CI_DANG_KY):
    """`MOI` và `bang_chung_xanh` đọc bằng IMPORT sổ đăng ký — một nguồn, không chép bảng."""
    spec = importlib.util.spec_from_file_location('ci_dang_ky_cho_provenance', duong)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return (dict(m.MOI), m.bang_chung_xanh)

def git_cuc_bo(sha, goc=ROOT):
    """parents/tree của commit trong kho cục bộ; không có object (hoặc không phải commit) ⇒ None."""
    try:
        r = subprocess.run(['git', '-C', str(goc), 'cat-file', '-p', sha], capture_output=True, text=True, timeout=60)
    except (OSError, subprocess.SubprocessError):
        return None
    dau = r.stdout.split('\n\n', 1)[0].splitlines() if r.returncode == 0 else []
    tree = [x[5:] for x in dau if x.startswith('tree ')]
    return {'tree': tree[0], 'parents': [x[7:] for x in dau if x.startswith('parent ')]} if len(tree) == 1 else None

def git_blob(sha, path, goc=ROOT):
    """Văn bản blob `<sha>:<path>` trong kho cục bộ; thiếu object/tệp, không phải blob hay không UTF-8 ⇒ None."""
    try:
        r = subprocess.run(['git', '-C', str(goc), 'cat-file', 'blob', f'{sha}:{path}'], capture_output=True, timeout=60)
        return r.stdout.decode('utf-8') if r.returncode == 0 else None
    except (OSError, subprocess.SubprocessError, UnicodeDecodeError):
        return None

def _env_chan(d):
    return 'env' in d and (type(d['env']) is not dict or any((str(k).startswith('CI_DANG_KY_') for k in d['env'])))

def doc_wf(van):
    """Workflow tại SHA (`yaml.safe_load`); hỏng, không phải dict hay `jobs` không phải dict ⇒ None."""
    try:
        wf = yaml.safe_load(van)
    except Exception:
        return None
    return wf if type(wf) is dict and type(wf.get('jobs')) is dict else None

def ghep_job(ten, wf):
    """r4 (d): khoá DUY NHẤT `k` mà tên job REST bằng `k`, bằng `name:` nguyên văn (không `${{`), hoặc là `<k|name> (<…>)`."""
    khop = [k for k, j in wf['jobs'].items() if type(ten) is str and type(j) is dict and any((type(x) is str and x and ('${{' not in x) and re.fullmatch(re.escape(x) + '(?: \\(.*\\))?', ten) for x in (k, j.get('name'))))]
    return khop[0] if len(khop) == 1 else None

def ten_du_kien(s):
    if 'name' in s:
        return s['name'] if _chuoi(s['name']) and '${{' not in s['name'] else None
    v = s.get('run', s.get('uses'))
    return 'Run ' + v.split('\n')[0] if _chuoi(v) else None

def _gio(v):
    try:
        return datetime.datetime.strptime(v[:19], '%Y-%m-%dT%H:%M:%S') if type(v) is str and RE_GIO.fullmatch(v) else None
    except ValueError:
        return None

def ghep_buoc(job, buoc, wf, ly_do_wf):
    """r4 F02: ĐỊNH DANH bước của nhóm log — job REST → MỘT job YAML (d); nhóm i → bước REST đã chạy thứ i → bước YAML cùng vị trí,
    kèm (a) số đếm ba mức · (b) tên · (c) giờ cắt về giây ∈ [started_at, completed_at]. Vế hỏng ⇒ CẢ job không marker (`None`)."""

    def hong(ly_do):
        return ({'trang_thai': 'not_measured', 'ly_do': ly_do, 'so_buoc': len(buoc)}, None)
    if wf is None:
        return hong(ly_do_wf)
    k, st = (ghep_job(job.get('name'), wf), job.get('steps'))
    sy = wf['jobs'][k].get('steps') if k else None
    if k is None or 'uses' in wf['jobs'][k] or type(sy) is not list or (not all((type(s) is dict for s in sy))):
        return hong('d_job_yaml_khong_duy_nhat')
    if not (type(st) is list and all((type(s) is dict and _so(s.get('number'), 1) for s in st)) and (len({s['number'] for s in st}) == len(st))):
        return hong('steps_rest_sai_dang')
    ung = [s for s in sorted(st, key=lambda s: s['number']) if s.get('name') not in ('Set up job', 'Complete job') and (not str(s.get('name')).startswith('Post '))]
    chay = [i for i, s in enumerate(ung) if s.get('conclusion') != 'skipped']
    if len(buoc) != len(chay):
        return hong('a_so_nhom_khac_so_buoc_rest_chay')
    if len(ung) != len(sy):
        return hong('a_so_buoc_rest_khac_so_buoc_yaml')
    if any((not _chuoi(s.get('name')) or s.get('name') != ten_du_kien(y) for s, y in zip(ung, sy))):
        return hong('b_ten_buoc_lech')
    if not all(((a := _gio(ung[i].get('started_at'))) and (z := _gio(ung[i].get('completed_at'))) and (h := _gio(b['gio'])) and (a <= h <= z) for b, i in zip(buoc, chay))):
        return hong('c_gio_header_ngoai_cua_so')
    return ({'trang_thai': 'passed', 'so_buoc': len(buoc)}, [(k, i) for i in chay])

def chan_buoc(wf, k, i):
    """r4 Q7: chặn chế độ của CHÍNH bước `i` job `k`: khoá ngoài `KHOA_BUOC`, `shell:` lạ, `defaults:`/`env:` lạ mức job/workflow, `run:`
    ĐỨNG TRƯỚC trong CÙNG job nhắc `GITHUB_ENV`/`GITHUB_PATH`. Bước `uses:` đứng trước là giới hạn khai, không chặn."""
    j, s = (wf['jobs'][k], wf['jobs'][k]['steps'][i])
    return bool('defaults' in wf or _env_chan(wf) or 'defaults' in j or _env_chan(j) or set(s) - KHOA_BUOC or (s.get('shell', 'bash') not in ('bash', 'pwsh', 'sh')) or any((re.search('GITHUB_(ENV|PATH)', str(t.get('run'))) for t in j['steps'][:i])))

def than(dong):
    m = RE_DONG.match(dong)
    return RE_ANSI.sub('', m.group(2) if m else dong)

def doc_sha_checkout(dong):
    """Dòng ngay sau lệnh git có đuôi ` log -1 --format=%H`, khớp NGUYÊN dòng `<timestamp> <40 hex>`."""
    sha = []
    for i, d in enumerate(dong[:-1]):
        t = than(d)
        if t.startswith('[command]') and t.endswith(' log -1 --format=%H'):
            k = RE_SHA.fullmatch(dong[i + 1])
            if k:
                sha.append(k.group(1))
    return sha

def moc_checkout(sha_ds, event, head, git):
    r = {'dong_sha': sha_ds}
    if not sha_ds:
        return r | {'trang_thai': 'not_measured', 'ly_do': 'khong_co_dong_sha_checkout'}
    if len(set(sha_ds)) > 1:
        return r | {'trang_thai': 'failed', 'ly_do': 'nhieu_sha_checkout_khac_nhau'}
    sha = sha_ds[0]
    obj = git(sha)
    r |= {'sha': sha, 'parents': obj['parents'] if obj else 'not_measured', 'tree': obj['tree'] if obj else 'not_measured'}
    if not (RUN_BAT_BUOC['event'](event) and RUN_BAT_BUOC['head_sha'](head)):
        return r | {'trang_thai': 'not_measured', 'ly_do': 'REST_thieu_event_hoac_head_sha'}
    if sha == head:
        return r | {'trang_thai': 'passed', 'doi_chieu': 'sha_bang_head_sha'}
    if event == 'pull_request':
        if not obj:
            return r | {'trang_thai': 'not_measured', 'ly_do': 'khong_co_object_de_doi_chieu_parents'}
        if head in obj['parents']:
            return r | {'trang_thai': 'passed', 'doi_chieu': 'head_sha_trong_parents_merge_tong_hop'}
    return r | {'trang_thai': 'failed', 'ly_do': f'sha_checkout_lech_head_sha ({event})'}

def tach_buoc(dong):
    """[{lenh, gio, in_lai, hop_le, phan}]: nhóm = từ `##[group]Run <lệnh>` tới trước `##[group]Run` kế; `gio` = timestamp header.
    `gio` cắt về giây. `in_lai` = dòng `36;1m` LIỀN sau header, bỏ ANSI — CHỈ để đối chiếu, KHÔNG làm kịch bản (M10). `hop_le` = cấu trúc đo trên 226/226
    nhóm thật (màu đầu = header, kế khối màu là `shell: `, không màu sau đó, có `##[endgroup]`, r4: không `##[group]` lồng trong vùng
    nhóm đang mở). `phan` = sau `##[endgroup]`, nơi duy nhất đo marker."""
    buoc = []
    for d in dong:
        t = than(d)
        if t.startswith('##[group]Run '):
            buoc.append({'lenh': t[len('##[group]Run '):], 'in_lai': [], 'phan': [], 'mo': True, 'ok': True, 'tien_to': True, 'gio': d[:19] + 'Z'})
        elif buoc and (b := buoc[-1])['mo']:
            mau = '\x1b[36;1m' in d
            if t == '##[endgroup]':
                b['mo'] = False
            elif mau and b['tien_to']:
                b['in_lai'].append(t)
            else:
                b['ok'], b['tien_to'] = (b['ok'] and (not mau) and (not t.startswith('##[group]')) and (not b['tien_to'] or t.startswith('shell: ')), False)
        elif buoc:
            buoc[-1]['phan'].append(t)
    return [b | {'hop_le': not b['mo'] and b['ok'] and (not b['tien_to']) and (b['in_lai'][:1] == [b['lenh']])} for b in buoc]

def dong_logic(lenh):
    """Nối dòng kết thúc bằng `\\` thành MỘT dòng logic — một đối số nằm ở dòng nối không thành lệnh riêng."""
    ra, noi = ([], '')
    for d in lenh:
        noi += d[:-1] + ' ' if d.endswith('\\') else d
        if not d.endswith('\\'):
            ra.append(noi.strip())
            noi = ''
    return ra + ([noi.strip()] if noi else [])

def do_dau_duong(buoc, moi, xanh, wf, ghep):
    """(kết quả, số bước XÁC THỰC). Nhóm i chỉ xét qua bước YAML `ghep` ĐỊNH DANH cho nó (r4): `run:` là chuỗi, KHÔNG `uses:` (Q8),
    khối in lại hợp lệ BẰNG NGUYÊN VĂN `run:` của CHÍNH bước ấy, TOÀN KHỐI là lời gọi tối giản. `chan_buoc` hoặc `VAR=` ⇒ lời gọi
    `MOI` ra `not_measured` (`che_do_khong_xac_dinh`); còn lại áp ĐÚNG regex `MOI` lên phần log của CHÍNH nhóm ấy."""
    kq, so = ([], 0)
    for b, (k, i) in zip(buoc, ghep or []):
        s = wf['jobs'][k]['steps'][i]
        run = s.get('run') if 'uses' not in s else None
        if not (type(run) is str and b['hop_le'] and (run.rstrip('\n') == '\n'.join(b['in_lai']))):
            continue
        so += 1
        goi = [RE_LOI_GOI.fullmatch(d) for d in dong_logic(run.rstrip('\n').split('\n')) if d]
        chan = chan_buoc(wf, k, i) or any((g and g[1] for g in goi))
        for duong in dict.fromkeys([g[2] for g in goi] if goi and all(goi) else []):
            muc = {'lenh': b['lenh'], 'duong_dan': duong}
            if duong not in moi or chan:
                kq.append(muc | {'trang_thai': 'not_measured', 'ly_do': 'khong_co_trong_MOI' if duong not in moi else 'che_do_khong_xac_dinh'})
            else:
                van = '\n'.join(b['phan']) + '\n'
                k = re.search(moi[duong], van, re.M) if (ok := xanh(van, moi[duong])) else None
                kq.append(muc | {'trang_thai': 'passed' if ok else 'failed', 'dong_khop': k.group(0).splitlines() if k else []})
    return (kq, so)

def moc_gate(job, dong, moi, xanh, wf=None, ly_do_wf=''):
    hop = {k: hop_le(job.get(k)) for k, hop_le in JOB_BAT_BUOC.items()}
    r = {'job_id': job['id'], 'name': job.get('name'), 'check_run_id': job['check_run_url'].rsplit('/', 1)[-1] if hop['check_run_url'] else None, 'labels': job.get('labels'), 'runner_id': job.get('runner_id'), 'runner_name': job.get('runner_name'), 'conclusion': job.get('conclusion'), 'buoc': [{'name': s['name'], 'conclusion': s['conclusion']} for s in job['steps']] if hop['steps'] else 'not_measured'}
    if job.get('conclusion') == 'skipped':
        return r | {'trang_thai': 'skipped'}
    if job.get('runner_id') == 0:
        return r | {'trang_thai': 'not_run'}
    anh = [than(d)[len('Image: '):] for d in dong if than(d).startswith('Image: ')]
    gh, ghep = ghep_buoc(job, (buoc := tach_buoc(dong)), wf, ly_do_wf)
    dau, so = do_dau_duong(buoc, moi, xanh, wf, ghep)
    thieu = [k for k, ok in hop.items() if not ok]
    r |= {'image': anh[0] if anh else 'not_measured', 'dau_duong': dau, 'thieu': thieu, 'ghep_buoc': gh, 'kich_ban': {'buoc_xac_thuc': so} | ({'trang_thai': 'not_measured', 'ly_do': ly_do_wf} if wf is None else {'trang_thai': 'passed', 'nguon': 'run_tai_sha_checkout'})}
    tt = {x['trang_thai'] for x in dau}
    if job.get('conclusion') in LOI_JOB or 'failed' in tt:
        return r | {'trang_thai': 'failed'}
    return r | {'trang_thai': 'not_measured' if thieu or 'passed' not in tt else 'passed'}

def thu(repo, run, attempt, goi, git, moi_tu=CI_DANG_KY, wf=git_blob):
    goc = f'{API}/repos/{repo}/actions'
    r, byte_run = lay_json(goi, f'{goc}/runs/{run}')
    if type(r) is not dict:
        raise LoiRest(f'than_sai_dang (run là {type(r).__name__})', f'{goc}/runs/{run}')
    jobs = lay_trang(goi, f'{goc}/runs/{run}/attempts/{attempt}/jobs', 'jobs')
    arts = lay_trang(goi, f'{goc}/runs/{run}/artifacts', 'artifacts')
    moi, xanh = doc_moi(moi_tu)
    moc_run = {'repo': repo, 'run_id': r.get('id'), 'run_attempt': r.get('run_attempt'), 'event': r.get('event'), 'head_sha': r.get('head_sha'), 'loi_khai_rest_path': r.get('path'), 'check_suite_id': r.get('check_suite_id'), 'nguon': f'{goc}/runs/{run}'}
    thieu = [k for k, hop_le in RUN_BAT_BUOC.items() if not hop_le(r.get(k))]
    lech = [k for k, v in (('id', run), ('run_attempt', attempt)) if k not in thieu and r.get(k) != v]
    moc_run |= {'thieu': thieu, 'lech': lech, 'trang_thai': 'failed' if lech else 'not_measured' if thieu else 'passed'}
    tep = {'run.json': byte_run, 'jobs.json': json.dumps(jobs, ensure_ascii=False, indent=1).encode()}
    co, gate, log = ([], [], {})
    for j in jobs['jobs']:
        if j.get('conclusion') == 'skipped' or j.get('runner_id') == 0:
            co.append({'job_id': j['id'], 'name': j.get('name'), 'trang_thai': 'skipped' if j.get('conclusion') == 'skipped' else 'not_run'})
            gate.append(moc_gate(j, [], moi, xanh))
            continue
        byte = lay(goi, f"{goc}/jobs/{j['id']}/logs")
        dong = byte.decode('utf-8', 'replace').splitlines()
        co.append({'job_id': j['id'], 'name': j.get('name')} | moc_checkout(doc_sha_checkout(dong), r.get('event'), r.get('head_sha'), git))
        sha = co[-1].get('sha') if co[-1]['trang_thai'] == 'passed' else None
        van = wf(sha, r['path']) if sha and RUN_BAT_BUOC['path'](r.get('path')) else None
        g = moc_gate(j, dong, moi, xanh, doc_wf(van) if van is not None else None, 'sha_checkout_chua_do' if not sha else 'workflow_tai_sha_khong_doc_duoc')
        gate.append(g)
        khop = {k for x in g.get('dau_duong', []) for k in x.get('dong_khop', [])}
        trich = [d for i, d in enumerate(dong) if than(d).startswith(('##[group]Run ', 'Image: ')) or than(d) in khop or RE_SHA.match(d) or (i + 1 < len(dong) and RE_SHA.match(dong[i + 1]))]
        tep[f"jobs/{j['id']}.trich.txt"] = ('\n'.join(trich) + '\n').encode()
        log[j['id']] = {'sha256': hashlib.sha256(byte).hexdigest(), 'bytes': len(byte), 'trich': f"jobs/{j['id']}.trich.txt"}
    prov = {'schema': 'ci_provenance/1', 'cong_cu': 'ops/ci_provenance.py', 'nguon': 'REST', 'attempt_yeu_cau': attempt, 'moc': {'run': moc_run, 'checkout': co, 'gate_output': {'jobs': gate, 'tap_jobs': tap(jobs, 'jobs'), 'tap_artifacts': tap(arts, 'artifacts', ART_BAT_BUOC), 'artifacts': [{k: a.get(k) for k in ('id', 'name', 'digest', 'size_in_bytes', 'expired')} for a in arts['artifacts']]}, 'workflow_definition': {'trang_thai': 'not_measured', 'ly_do': LY_DO_WD, 'loi_khai_rest_path': r.get('path')}}, 'log_day_du': log}
    tep['provenance.yaml'] = yaml.safe_dump(prov, sort_keys=False, allow_unicode=True).encode()
    return (prov, tep)

def ghi_tep(p, byte):
    p.parent.mkdir(parents=True, exist_ok=True)
    p.write_bytes(byte)

def ghi_nguyen_tu(out, tep):
    """Ghi vào thư mục tạm CÙNG CẤP rồi `os.replace`: lỗi giữa chừng ⇒ `out` vắng hoặc giữ nguyên bản trước."""
    out = Path(out).resolve()
    out.parent.mkdir(parents=True, exist_ok=True)
    tam = Path(tempfile.mkdtemp(prefix=f'.{out.name}.tam-', dir=out.parent))
    cu = out.parent / f'{tam.name}.cu'
    try:
        for ten, byte in tep.items():
            ghi_tep(tam / ten, byte)
        if out.exists():
            os.replace(out, cu)
        os.replace(tam, out)
    except BaseException:
        if cu.exists() and (not out.exists()):
            os.replace(cu, out)
        shutil.rmtree(tam, ignore_errors=True)
        raise
    shutil.rmtree(cu, ignore_errors=True)

def cac_trang_thai(prov):
    m = prov['moc']
    g = m['gate_output']
    return [m['run']['trang_thai'], m['workflow_definition']['trang_thai'], g['tap_jobs']['trang_thai'], g['tap_artifacts']['trang_thai']] + [x['trang_thai'] for x in m['checkout']] + [x['trang_thai'] for x in g['jobs']]

def main(argv=None, goi=goi_that, git=git_cuc_bo, moi_tu=CI_DANG_KY, wf=git_blob):
    p = argparse.ArgumentParser(prog='ci_provenance.py', description=__doc__.split('\n')[0])
    sub = p.add_subparsers(dest='lenh', required=True)
    t = sub.add_parser('thu', help='thu provenance của MỘT run/attempt bằng REST')
    t.add_argument('--repo', required=True, help='owner/repo')
    t.add_argument('--run', required=True, type=int, help='id workflow run')
    t.add_argument('--attempt', required=True, type=int, help='run_attempt phải đo')
    t.add_argument('--out', required=True, help='thư mục đầu ra (ghi nguyên tử)')
    try:
        a = p.parse_args(argv)
    except SystemExit as e:
        if e.code == 0:
            return 0
        print(KHONG_SINH)
        return 2
    if not RE_REPO.fullmatch(a.repo) or a.run <= 0 or a.attempt <= 0:
        print(f'SAI_DOI_SO: --repo owner/repo, --run/--attempt nguyên dương (được {a.repo!r} {a.run} {a.attempt})\n{KHONG_SINH}')
        return 2
    try:
        prov, tep = thu(a.repo, a.run, a.attempt, goi, git, moi_tu, wf)
    except LoiRest as e:
        print(f'REST_LOI: HTTP {e.ma} {e.url}\n{KHONG_SINH}')
        return 3
    except Exception:
        print(KHONG_SINH)
        raise
    try:
        ghi_nguyen_tu(a.out, tep)
    except OSError as e:
        print(f'LOI_GHI: {e}\n{KHONG_SINH}')
        raise
    m = prov['moc']
    print(f"RUN: {m['run']['trang_thai']} (run_attempt {m['run']['run_attempt']}, yeu cau {a.attempt})")
    for c, g in zip(m['checkout'], m['gate_output']['jobs']):
        print(f"JOB {c['job_id']} {c['name']}: checkout={c['trang_thai']} {c.get('sha', '-')} gate={g['trang_thai']}")
    print(f"WORKFLOW_DEFINITION: {m['workflow_definition']['trang_thai']} ({LY_DO_WD})")
    tt = cac_trang_thai(prov)
    print(f"provenance.yaml sha256 {hashlib.sha256(tep['provenance.yaml']).hexdigest()}")
    print(f"NOT_MEASURED: {tt.count('not_measured')}")
    return 12 if 'failed' in tt else 0
if __name__ == '__main__':
    raise SystemExit(main(sys.argv[1:]))