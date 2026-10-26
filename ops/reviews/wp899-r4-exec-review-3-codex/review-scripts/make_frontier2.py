from pathlib import Path
R=Path('.review');s=(R/'frontier.py').read_text();start=s.index('M=[');end=s.index('\n# Compare against',start)
addition='''M=[
('mode_defaults_wf_truthy', '"defaults" in wf or', 'bool(wf.get("defaults")) or'),
('mode_defaults_job_truthy', 'or "defaults" in j or', 'or bool(j.get("defaults")) or'),
('mode_env_truthy', 'return v is not None and (type(v) is not dict', 'return bool(v) and (type(v) is not dict'),
('mode_env_string_only', 'type(v) is not dict or any(str(k)', 'type(v) is str or any(str(k)'),
('number_type_bool_guard_drop','type(s) is dict and _so(s.get("number"), 1)', 'type(s) is dict and isinstance(s.get("number"), int) and s["number"] >= 1'),
('number_min_strict','_so(s.get("number"), 1)', '_so(s.get("number"), 2)'),
('header_time_other_group','(h := _gio(b["gio"][:19] + "Z"))','(h := _gio(buoc[0]["gio"][:19] + "Z"))'),
('header_window_other_step','_gio(ung[i].get("started_at"))','_gio(ung[0].get("started_at"))'),
('time_current_end_other_step','_gio(ung[i].get("completed_at"))','_gio(ung[0].get("completed_at"))'),
('name_only_first_rest','for s, y in zip(ung, sy)):', 'for s, y in list(zip(ung, sy))[:1]):'),
('name_only_last_rest','for s, y in zip(ung, sy)):', 'for s, y in list(zip(ung, sy))[-1:]):'),
]
'''
s=s[:start]+addition+s[end:];s=s.replace("out=R/'frontier'","out=R/'frontier2'");(R/'frontier2.py').write_text(s)
