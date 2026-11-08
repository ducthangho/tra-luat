import os,sys
if len(sys.argv)<2:raise SystemExit('command required')
env=os.environ.copy();credential=env.get('GITHUB_PAT')
if not credential:raise SystemExit('configured GitHub credential unavailable')
env['GH_TOKEN']=credential
os.execvpe(sys.argv[1],sys.argv[1:],env)
