import pathlib,sys,importlib.util,json
R=pathlib.Path(__file__).resolve().parent;s=importlib.util.spec_from_file_location('t',R.parent/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(s);s.loader.exec_module(t)
x=t.X

def expect_no(p,label):
 g=t.gate(p);t.bang(g['ghep_buoc']['trang_thai']=='not_measured' and g['dau_duong']==[] and g['trang_thai']!='passed',label+': '+str(g))
def rest_order():
 p=t.g1(t.wf_tu(x),t.buoc(x,'THU: 4/4 dat'),sua=lambda st:st.reverse())
 t.bang(t.gate(p)['trang_thai']=='passed','sort REST by number, independent of response list order')
def rest_duplicate():
 expect_no(t.g1(t.wf_tu(x),t.buoc(x,'THU: 4/4 dat'),sua=lambda st:st[2].update(number=st[1]['number'])),'duplicate number invalid')
def time_format():
 expect_no(t.g1(t.wf_tu(x),t.buoc(x,'THU: 4/4 dat'),sua=lambda st:st[2].update(started_at='2026-10-19T23:45:04+00:00')),'offset unsupported')
def time_missing_header():
 expect_no(t.g1(t.wf_tu(x),[r.replace(t.T+' ','',1) if '##[group]Run' in r else r for r in t.buoc(x,'THU: 4/4 dat')],sua=lambda st:st[2].update(started_at=t.T[:19]+'Z',completed_at=t.T[:19]+'Z')),'header timestamp missing')
def invalid_calendar():
 for change in ({'started_at':'2026-02-30T00:00:00Z'},{'completed_at':'2026-13-19T00:00:00Z'},{'completed_at':'2026-10-19T24:00:00Z'}):
  expect_no(t.g1(t.wf_tu(x),t.buoc(x,'THU: 4/4 dat'),sua=lambda st,d=change:st[2].update(d)),'not a valid timestamp '+str(change))
def github_path():
 e='echo A=1 >> $GITHUB_PATH'
 p=t.g1(t.wf_tu(e,x),t.buoc(e),t.buoc(x,'THU: 4/4 dat'))
 t.bang([(z['trang_thai'],z.get('ly_do')) for z in t.gate(p)['dau_duong']]==t.CHAN,'preceding run mentions GITHUB_PATH => block mode')
def expression_name():
 expect_no(t.g1(t.wf_tu(x,buoc_them={'name':'${{ matrix.step }}'}),t.buoc(x,'THU: 4/4 dat')),'expression step name cannot authenticate')
def first_line():
 p=t.g1(t.wf_tu('\n'+x),t.khoi(['',x],'THU: 4/4 dat'))
 t.bang(t.gate(p)['trang_thai']=='passed','name derives from first raw run line, including blank')
CA={f.__name__:f for f in (rest_order,rest_duplicate,time_format,time_missing_header,invalid_calendar,github_path,expression_name,first_line)}
if __name__=='__main__':
 name=sys.argv[1]
 try:CA[name]()
 except t.TinHieuChotCa as e:print('DO:'+name+':'+str(e));sys.exit(3)
 except Exception as e:print('HONG:'+name+':'+type(e).__name__+':'+str(e));sys.exit(4)
 print('DAT:'+name)
