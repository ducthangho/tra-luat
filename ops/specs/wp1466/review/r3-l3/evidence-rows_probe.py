from pathlib import Path
import subprocess,sys,json
O=Path(__file__).resolve().parent;P=O/'prototype';r=O/'row-probe';(r/'docs').mkdir(parents=True,exist_ok=True)
goc=(P/'docs/PROTOCOL_DA_PHIEN.md').read_text();header='\n\n## Bảng dữ liệu thử\n\n| INV | bất biến | nguồn | cổng |\n|---|---|---|---|\n'
# Chỉ dữ liệu Markdown lành tính, không đường dẫn hay nội dung thực thi.
for name,row in [('canonical','| `INV-99` | ví dụ | ví dụ | chưa đo |'),('no_space','|`INV-99`| ví dụ | ví dụ | chưa đo |'),('plain_id','| INV-99 | ví dụ | ví dụ | chưa đo |')]:
 (r/'docs/PROTOCOL_DA_PHIEN.md').write_text(goc+header+row+'\n')
 x=subprocess.run([sys.executable,'-B',str(P/'.claude/dev/packet_loop.py'),'doctrine-scan','--root',str(r)],capture_output=True,text=True)
 print(name,x.returncode,json.dumps((x.stdout+x.stderr).strip(),ensure_ascii=False),flush=True)
