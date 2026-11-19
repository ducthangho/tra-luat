import ntpath, sys, stat
B=chr(92)
cases=["C:"+B+"x","c:/x","C:","D:fake",B+"fake","/fake",B*2+"server"+B+"share",B*2+"server"+B+"share"+B+"x",B*2+"server",B*2+"server"+B,
 B*2+"?"+B+"C:"+B+"x",B*2+"."+B+"pipe"+B+"x",B*2+"?"+B+"UNC"+B+"s"+B+"sh", "//server/share/x", "/"+B+"server"+B+"share", B+"/server/share",
 "C:"+B+"a"+B+".."+B+"b","fake","..","C:"+B+"a/b"+B+"c", "C:"+B+"x:ads", B*3+"server"+B+"share", B*2+"server"+B*2+"share", "CON", "C:"+B+"NUL", "C:"+B+"a."+B+"b ", "1:"+B+"x", B*2+"localhost"+B+"C$"+B+"x"]
print(sys.version.split()[0])
for p in cases:
    d,r=ntpath.splitdrive(p)
    try: ia=ntpath.isabs(p)
    except Exception as e: ia=repr(e)
    sr = getattr(ntpath,'splitroot',None)
    print(repr(p), '| splitdrive', (d,r), '| isabs', ia, '| splitroot', sr(p) if sr else '-')
print('REPARSE', getattr(stat,'FILE_ATTRIBUTE_REPARSE_POINT',None), 'join', ntpath.join("C:"+B+"cwd","D:fake"), ntpath.join("C:"+B+"cwd",B+"fake"))
print('isreserved', getattr(ntpath,'isreserved',None) and [ntpath.isreserved(x) for x in ("CON","a.","k\nho","x:y")])
