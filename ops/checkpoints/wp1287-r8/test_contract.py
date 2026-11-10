"""Counterexamples from the independent advisory; controlled evidence, not native proof."""
import json,unittest
# Embedded Python uses an isolated sys.path; add only this frozen operator directory.
import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parent))
from contract import same_identity,module_state,presence,bridge,readiness,cleanup,terminal
class Counterexamples(unittest.TestCase):
    def test_first_false_18(self):
        s=module_state(True,False,18,None,[],True,False)
        self.assertEqual((s,presence(s,[],'chrome.dll')),('empty_snapshot','UNKNOWN'))
    def test_next_access_denied(self):
        s=module_state(True,True,None,5,[{'base':1}],True,True)
        self.assertEqual((s,presence(s,['chrome.exe'],'chrome.dll')),('partial','UNKNOWN'))
    def test_complete_missing_is_only_not_listed(self):
        s=module_state(True,True,None,18,[{'base':1}],True,True)
        self.assertEqual(presence(s,['chrome.exe'],'chrome.dll'),'NOT_LISTED_IN_COMPLETE_WALK')
    def test_pid_reuse(self):
        self.assertFalse(same_identity({'pid':8,'birth':1,'image':'chrome.exe'},{'pid':8,'birth':2,'image':'chrome.exe'}))
    def test_basename_is_not_file_bridge(self):
        a={'path':'C:/one/uvh64.dll','file_id':1};b={'path':'C:/two/uvh64.dll','file_id':2}
        self.assertEqual(bridge(a,b,a['path']),'UNKNOWN')
    def test_open_zero_empty_snapshot(self):
        self.assertEqual(readiness('acknowledged',None,'http://127.0.0.1/source',[302,200],None,b'nonce'),'unknown')
    def test_wrong_nonce(self):
        self.assertEqual(readiness('acknowledged','u','u',[302,200],b'old',b'new'),'failed')
    def test_capture_cannot_hide_cleanup_timeout(self):
        x=terminal('passed',cleanup('n',[{'rc':None}], [4]),2,1)
        self.assertFalse(x['success']);self.assertFalse(x['release_lock'])
    def test_wrong_closed_nonce(self):
        rows=[{'rc':0,'stdout':json.dumps({'session':'n','status':'closed'}).encode(),'stderr':b''},{'rc':0,'stdout':b'{"session":"n","deleted":false}','stderr':b''},{'rc':1,'stdout':b'{"isError":true,"error":"wrong nonce"}','stderr':b''}]
        self.assertEqual(cleanup('n',rows,[]),'failed')
        rows[0]['stdout']=b'';self.assertEqual(cleanup('n',rows,[]),'failed')
    def test_operator_shell_separate(self):
        x=terminal('failed','verified',2,1)
        self.assertEqual((x['operator_child_rc'],x['transport_shell_rc']),(2,1))
    def test_positive_cleanup_deleted_false(self):
        values=[(0,{'session':'n','status':'closed'}),(0,{'session':'n','deleted':False}),(1,{'isError':True,'error':"The browser 'n' is not open, please run open first"})]
        rows=[{'rc':rc,'stdout':json.dumps(v).encode(),'stderr':b''} for rc,v in values]
        self.assertEqual(cleanup('n',rows,[]),'verified')
if __name__=='__main__':unittest.main(verbosity=2)
