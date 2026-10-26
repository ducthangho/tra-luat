from pathlib import Path
import sys
sys.stdout.buffer.write((Path('.review')/'suite.stdout.txt').read_bytes())
