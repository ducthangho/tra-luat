#!/usr/bin/env node
/**
 * gas_rowkind_test.js — Node harness cho D3 (GAS 2.21.2m): export row_kind RAW.
 *
 * Nạp Code.2.21.2m.gs qua vm (stub service tối thiểu như gas_claim_test.js), gọi THẲNG các hàm PURE:
 *   - nlmCompactRow_: export phải RAW ('' giữ '', 'overflow' giữ 'overflow') — hết che blank thành 'own';
 *   - regIsCorpusCounted_ / profileOwnCount_: ĐẾM vẫn default-own (doctrine v2.21.2e — blank quy về own);
 *   - APP_VERSION == 2.21.2m.
 * Kèm ASSERT MỨC NGUỒN: không còn mẫu "row_kind: o.row_kind || 'own'" (2 site export đã đổi RAW).
 *
 * Chạy: node references/gas_rowkind_test.js [đường dẫn .gs, mặc định Code.2.21.2m.gs]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const gsPath = path.resolve(__dirname, process.argv[2] || 'Code.2.21.2m.gs');
const code = fs.readFileSync(gsPath, 'utf8');

function noop() { return undefined; }
function makeStubService(name) {
  return new Proxy({}, {
    get(_t, prop) {
      if (prop === Symbol.toPrimitive || typeof prop === 'symbol') return undefined;
      return (..._args) => makeStubService(name + '.' + String(prop));
    },
  });
}

const sandbox = {
  Logger: { log: noop },
  SpreadsheetApp: makeStubService('SpreadsheetApp'),
  DriveApp: makeStubService('DriveApp'),
  Drive: makeStubService('Drive'),
  LockService: makeStubService('LockService'),
  CacheService: makeStubService('CacheService'),
  PropertiesService: makeStubService('PropertiesService'),
  ContentService: makeStubService('ContentService'),
  Utilities: makeStubService('Utilities'),
  UrlFetchApp: makeStubService('UrlFetchApp'),
  Session: makeStubService('Session'),
  console: console,
};
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: path.basename(gsPath) });

let pass = 0, fail = 0;
function t(name, cond) {
  if (cond) { pass++; console.log('  [OK] ' + name); }
  else { fail++; console.log('  [FAIL] ' + name); }
}

// Trước đây pin CỨNG '2.21.2m' ⇒ đỏ từ 2.21.2n, rữa theo mỗi lần bump (test rỗng nghĩa).
// Nay khóa CHIỀU: version phải đúng dạng và KHÔNG được tụt dưới 2.21.2m (mốc ra đời của file test này).
t('app_version_khong_tut_duoi_2212m', (function () {
  const m = /^(\d+)\.(\d+)\.(\d+)([a-z]*)$/.exec(String(sandbox.APP_VERSION || ''));
  if (!m) return false;
  const cur = [Number(m[1]), Number(m[2]), Number(m[3]), m[4]];
  const min = [2, 21, 2, 'm'];
  for (let i = 0; i < 4; i++) {
    if (cur[i] > min[i]) return true;
    if (cur[i] < min[i]) return false;
  }
  return true;
})());
const rBlank = sandbox.nlmCompactRow_({ drive_id: 'd1', row_kind: '' });
const rMiss = sandbox.nlmCompactRow_({ drive_id: 'd2' });
const rOv = sandbox.nlmCompactRow_({ drive_id: 'd3', row_kind: 'overflow' });
const rOwn = sandbox.nlmCompactRow_({ drive_id: 'd4', row_kind: 'own' });
t('compact_export_blank_stays_blank', rBlank.row_kind === '' && rMiss.row_kind === '');
t('compact_export_overflow_kept', rOv.row_kind === 'overflow' && rOwn.row_kind === 'own');
// ĐẾM giữ doctrine blank→own: dòng corpus true + row_kind blank vẫn được đếm; ref bị loại.
t('count_blank_row_still_corpus', sandbox.regIsCorpusCounted_({ corpus: 'true', row_kind: '' }) === true);
t('count_ref_excluded', sandbox.regIsCorpusCounted_({ corpus: 'true', row_kind: 'ref' }) === false);
t('count_overflow_counted_even_corpus_blank', sandbox.regIsCorpusCounted_({ corpus: '', row_kind: 'overflow' }) === true);
t('own_count_blank_treated_own', sandbox.profileOwnCount_([{ row_kind: '' }, { row_kind: 'ref' }, { row_kind: 'overflow' }]) === 2);
// Mức nguồn: 2 site EXPORT hết default 'own'; các site đếm vẫn còn String(o.row_kind || 'own') — đúng chủ đích.
t('source_no_export_default_own', !code.includes("row_kind: o.row_kind || 'own'"));
t('source_counting_default_kept', code.includes("String(o.row_kind || 'own')"));

console.log(`== gas_rowkind_test ${pass}/${pass + fail} ==`);
process.exit(fail === 0 ? 0 : 1);
