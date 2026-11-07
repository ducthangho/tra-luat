"""Ap bien the duong_nhanh TOI THIEU cua r5 (muc 1) len run duong_nhanh THAT 41397205258 (REST jobs + ci.yml@8983e1b).
Chay tu repo: python -I -B ../work/nhanh_r5.py"""
import json, re, sys, subprocess, importlib.util, yaml
sys.argv = [sys.argv[0]]
spec = importlib.util.spec_from_file_location('k7', '../work/k7_r4.py'); K = importlib.util.module_from_spec(spec); spec.loader.exec_module(K)
cp = K.cp
jobs = json.load(open('ops/land/pr1055-wp1052-provenance/readback-jobs-41397205258.json'))['jobs']
wf = K.wf_tai('8983e1b')
J = [j for j in jobs if j['conclusion'] != 'skipped' and 'ubuntu-latest' in (j.get('labels') or []) and j['name'] != 'chuan-bi']
print('J =', len(J))
for j in J:
    k = cp.ghep_job(j['name'], wf)
    base = j['name'].split(' (')[0]
    want = f'DUONG_NHANH - liet ke buoc bo qua (job {base})'
    st = {s['name']: s['conclusion'] for s in j['steps']}
    lk = st.get(want)
    yml = [i for i, s in enumerate(wf['jobs'][k]['steps']) if cp.ten_du_kien(s) == want] if k else []
    chan = K.chan_k7(wf, k, yml[0], set()) if len(yml) == 1 else None
    print(f"  {j['name'][:36]:36} job_yaml={k!s:18} liet_ke_REST={lk!s:8} liet_ke_YAML={len(yml)} chan_k7={chan}")
# buoc khong co if theo che_do ma day_du co luat => r5 doi 'giu nguyen dau hieu'
cb = [j for j in jobs if j['name'] == 'chuan-bi'][0]
print('chuan-bi buoc:', [(s['name'], s['conclusion']) for s in cb['steps']][1:4])
i = [i for i, s in enumerate(wf['jobs']['chuan-bi']['steps']) if cp.ten_du_kien(s) == 'phan loai diff (duong nhanh ho so)'][0]
print('chuan-bi YAML buoc phan loai: continue-on-error =', wf['jobs']['chuan-bi']['steps'][i].get('continue-on-error'), '; chan_k7 =', K.chan_k7(wf, 'chuan-bi', i, set(wf['jobs']['chuan-bi']['steps'][i].get('env') or {})))
g = wf['jobs']['gate-cong-cu-gop']['steps']
print('gate-cong-cu-gop buoc gom:', [(cp.ten_du_kien(s), s.get('if'), sorted((s.get('env') or {}).keys())) for s in g if 'gom' in cp.ten_du_kien(s)])
