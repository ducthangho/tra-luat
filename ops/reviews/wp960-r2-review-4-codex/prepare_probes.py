from pathlib import Path
src=Path('/tmp/claude-0/rv/wp960-r2-review-3-codex')
for name in ['probe_recheck.py','extra_recheck.py','rc_witness_recheck.py']:
 text=(src/name).read_text().replace('/tmp/wp960-r3-recheck-copy','/tmp/wp960-r4-copy').replace('/tmp/wp960-r3-recheck-clean','/tmp/wp960-r4-clean')
 (Path('replay_'+name)).write_text(text.replace('import probe_recheck as h','import replay_probe_recheck as h'))
print('Copied prior probes; only import/copy-path bridges changed.')
