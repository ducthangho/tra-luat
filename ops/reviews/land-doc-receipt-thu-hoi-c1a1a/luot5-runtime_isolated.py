import audit as A
import sys
A.OUT=A.OUT/('runtime-'+sys.version.split()[0]);A.OUT.mkdir(exist_ok=True)
A.runtime()
