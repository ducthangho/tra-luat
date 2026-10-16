import os,runpy,sys
sys.set_int_max_str_digits(4300)
os.environ['PYTHONINTMAXSTRDIGITS']='4300'
runpy.run_path('.claude/dev/doc_receipt_thu_hoi_test.py',run_name='__main__')
