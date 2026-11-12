"""Abstract contract checks only; no gate_output payloads or source mutants.

The new implementation does not exist. These results describe observations
mandated by the spec, not executed tests of gate_output_doi_chieu.py.
"""
import collections
import json
from pathlib import Path

from measure import ROOT, jobs_j, names, save

required5, required = names()
raw = json.loads((ROOT / 'ops/land/pr1055-wp1052-provenance/readback-jobs-41397205258.json').read_text())
actual = collections.Counter(j['name'] for j in jobs_j(raw['jobs']))

def reasons(counts, required_names, checks=('missing', 'duplicate', 'extra'), k6=False):
    out = []
    for name in required_names:
        if 'missing' in checks and not counts[name]:
            out.append('thieu_job_bat_buoc:' + name)
        if 'duplicate' in checks and counts[name] > 1:
            out.append('job_trung_ten:' + name)
    if 'extra' in checks:
        out += ['job_ngoai_luat:' + name for name in counts if name not in required_names]
    if k6:
        out.append('khong_co_luat_or_thieu_buoc')
    return ('not_measured' if out else 'passed'), sorted(out)

rows = []
# j uses the real 14-name census, independently of the missing step checks.
for label, reduced, k6 in [('m-A3d/j', False, False), ('m-A3e/j', True, False), ('m-A3k/k', False, True), ('m-A3e/k', True, True)]:
    baseline = reasons(actual, required, k6=k6)
    mutant = reasons(actual, required5 if reduced else required, checks=('missing','duplicate','extra') if reduced else ('duplicate','extra'), k6=k6)
    rows.append({'pair':label, 'baseline_status':baseline[0], 'mutant_status':mutant[0], 'baseline_missing':sum(x.startswith('thieu_job_bat_buoc:') for x in baseline[1]), 'mutant_missing':sum(x.startswith('thieu_job_bat_buoc:') for x in mutant[1]), 'reason_assertion_distinguishes':baseline[1] != mutant[1]})

# Only counts are varied, not a generated provenance/evidence payload.
dup = collections.Counter(required)
dup[required[0]] += 1
out = collections.Counter(required)
out['gate-moi (ubuntu-latest)'] = 1
for label, counts, checks, k6 in [('m-A3f/j-prime', dup, ('missing','extra'), False), ('m-A3g/j-double-prime', out, ('missing','duplicate'), True)]:
    before = reasons(counts, required, k6=k6)
    after = reasons(counts, required, checks=checks, k6=k6)
    rows.append({'pair':label, 'baseline_status':before[0], 'mutant_status':after[0], 'reason_assertion_distinguishes':before[1] != after[1]})

# A20 supplies hash/domain corruption, but no invalid input for any of the
# three new registry invariants. This truth-table is a coverage proof only.
properties = ('hash_ok','disjoint','one_open','unique_required','contains_check5','one_rule_per_name')
cases = {label:{k:True for k in properties} for label in ('A20a','A20b','A20c','A20d','A20e')}
cases['A20c']['hash_ok'] = False
cases['A20d']['disjoint'] = False
cases['A20e']['one_open'] = False
registry = []
for omit in properties[-3:]:
    unchanged = all(all(v.values()) == all(value for key,value in v.items() if key != omit) for v in cases.values())
    registry.append({'omitted_predicate':omit, 'A20a_to_e_observations_unchanged':unchanged})
save('contracts', {'scope':'abstract spec model; not implementation tests', 'K3':rows, 'registry_coverage':registry, 'A16': {'chuan_bi_STEP':'dinh_dang -> removed K9 predicate: no violation, with other inputs valid', 'Windows_STEP':'dinh_dang -> removed K9 predicate: no violation, with other inputs valid'}})
