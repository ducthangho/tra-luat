import importlib.util,json,pathlib,sys
sp=importlib.util.spec_from_file_location('t',pathlib.Path.cwd()/'ops/ci_provenance_test.py');t=importlib.util.module_from_spec(sp);sp.loader.exec_module(t)
d,oid,tree=sys.argv[1:]
case='r955_git_commit_message_encoding'
def criterion():
    try: actual=t.nap().git_cuc_bo(oid,goc=d)
    except UnicodeDecodeError as e:t.bang(False,f'Git commit metadata must not depend on message encoding: {type(e).__name__}')
    t.bang(actual=={'tree':tree,'parents':[]},f'wrong Git metadata: {actual}')
try: criterion()
except t.TinHieuChotCa as e:print(f'DO:{case}:{e}');raise SystemExit(3)
except Exception as e:print(f'HONG:{case}:{type(e).__name__}:{e}');raise SystemExit(4)
print('CA: 1/1 dat')
