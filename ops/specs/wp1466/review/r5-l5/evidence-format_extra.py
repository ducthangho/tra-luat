from pathlib import Path
import json,subprocess,sys,os,unicodedata
O=Path(__file__).resolve().parent;P=O/'prototype';raw=(P/'docs/PROTOCOL_DA_PHIEN.md').read_bytes();D=O/'tmp/format-extra';D.mkdir(exist_ok=True)
variants={'no_final_lf':raw[:-1] if raw.endswith(b'\n') else raw,'extra_final_lf':raw+b'\n','unlocked_note_crlf':raw+b'\nGhi chu ngoai khoa.\r\n','blank_lines_at_eof':raw+b'\n\n\n'}
for name,b in variants.items():
 d=D/name;(d/'docs').mkdir(parents=True,exist_ok=True);(d/'docs/PROTOCOL_DA_PHIEN.md').write_bytes(b)
 r=subprocess.run([sys.executable,'-B',str(P/'.claude/dev/packet_loop.py'),'doctrine-scan','--root',str(d)],capture_output=True,text=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'));print(name,r.returncode,r.stdout.strip(),r.stderr.strip())
print('NFKC_CANONICAL_I_VS_CYRILLIC',unicodedata.normalize('NFKC','I')==unicodedata.normalize('NFKC',chr(0x0406)))
print('NFKC_ASCII_VS_FULLWIDTH_DIGIT',unicodedata.normalize('NFKC','9')==unicodedata.normalize('NFKC',chr(0xff19)))
