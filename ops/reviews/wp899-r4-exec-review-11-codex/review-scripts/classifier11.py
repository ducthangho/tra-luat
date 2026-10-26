import contextlib, importlib.util, io, json, pathlib
from unittest import mock
R=pathlib.Path(__file__).resolve().parent; root=R.parent
s=importlib.util.spec_from_file_location('t11',root/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
source=(root/'ops/ci_provenance.py').read_text();old=json.loads((R/'criteria8-results.json').read_text())
rows=[]
for fixture in old['classifier']:
    # Reuse the four classifier fixtures already present in the review input;
    # test the complete closed runner, including aggregation, with one mutant.
    results=[[('c',0,'')],[(fixture['target'],fixture['rc'],fixture['output'])]]
    buf=io.StringIO()
    with mock.patch.object(t,'sinh_dot_bien_dong',return_value=[('review_fixture',source)]), \
         mock.patch.object(t,'_tat_ca_ca',side_effect=results), mock.patch.object(t,'TUONG_DUONG',{}), \
         contextlib.redirect_stdout(buf):
        rc=t.chay_dot_bien_dong(1)
    output=buf.getvalue()
    expected_rank='SONG' if fixture['rank']=='SONG_SOT' else fixture['rank']
    assert '[KQ] review_fixture ' in output and ' '+expected_rank+'\n' in output
    assert rc==(0 if fixture['rank']=='GIET' else 1)
    rows.append({'fixture':fixture,'runner_rc':rc,'output':output})
checks=[]
for name,old,new,prefix in t.DOT_BIEN:
    if name not in ('L9_D03_job_chi_tien_to','L9_D03_buoc_chi_tien_to','L9_D04_dem_mot_buoc','L10_bat_lai_tuple_luot9'):continue
    rank,detail=t.chay_dot_bien(name,old,new,prefix)
    checks.append({'name':name,'rank':rank,'detail':detail})
    assert rank=='GIET'
(R/'classifier11-results.json').write_text(json.dumps({'pipeline':rows,'previous_round_mutants':checks},ensure_ascii=False,indent=2))
print('CLASSIFIER11: 4/4 complete aggregation fixtures correct; previous-round targeted mutants',len(checks),'all GIET')
