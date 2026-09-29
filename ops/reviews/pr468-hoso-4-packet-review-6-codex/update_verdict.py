from pathlib import Path
P=Path(__file__).resolve().parents[1]/'VERDICT.md'
def add(text):
    s=P.read_text(); assert s.rstrip().endswith('verdict: dang-do')
    P.write_text(s.rstrip().removesuffix('verdict: dang-do').rstrip()+'\n\n'+text.strip()+'\n\nverdict: dang-do\n')
if __name__=='__main__':
    import sys
    add(sys.stdin.read())
