#!/usr/bin/env node
/**
 * gas_claim_test.js — Node harness cho F-04 ingest_claim (GAS 2.21.2l).
 *
 * Nạp Code.2.21.2l.gs qua vm với stub GAS services TỐI THIỂU (chỉ đủ để file PARSE — mọi `var` top-level
 * là literal, không gọi service nào lúc load), rồi gọi THẲNG các hàm PURE (_claimGcFilter_/_claimAcquireDecide_/
 * _claimCommitDecide_) — KHÔNG đụng SpreadsheetApp/LockService thật. Test race 2-host thật (cùng key, run_id
 * khác nhau, gọi decide tuần tự trên state đã ghi của lần trước — mô phỏng "ai tới trước thắng").
 *
 * Chạy: node references/gas_claim_test.js [đường dẫn .gs, mặc định Code.2.21.2l.gs]
 * Không phụ thuộc ngoài (fs/vm/path — core Node). Không sửa .gs khi chạy.
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const gsPath = path.resolve(__dirname, process.argv[2] || 'Code.2.21.2l.gs');
const code = fs.readFileSync(gsPath, 'utf8');

function noop() { return undefined; }
function makeStubService(name) {
  // Proxy trả về hàm no-op cho MỌI method gọi trên service — đủ để file PARSE/EXECUTE top-level
  // (var literal) mà không throw nếu code lỡ gọi 1 service nào đó ở phạm vi module (không nên có,
  // nhưng phòng hờ). Test PURE function không bao giờ chạm các service này.
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
  UrlFetchApp: makeStubService('UrlFetchApp'),
  Utilities: makeStubService('Utilities'),
  ContentService: makeStubService('ContentService'),
  HtmlService: makeStubService('HtmlService'),
  ScriptApp: makeStubService('ScriptApp'),
  MimeType: {},
  console,
};
vm.createContext(sandbox);
try {
  vm.runInContext(code, sandbox, { filename: gsPath });
} catch (e) {
  console.error('[gas_claim_test] LOAD LỖI:', e && e.stack || e);
  process.exit(1);
}

const cases = [];
function t(name, fn) {
  try {
    cases.push([name, !!fn()]);
  } catch (e) {
    console.error('  [EXCEPTION] ' + name + ': ' + (e && e.stack || e));
    cases.push([name, false]);
  }
}

const HAVE_FNS = ['_claimGcFilter_', '_claimAcquireDecide_', '_claimCommitDecide_', '_claimReleaseDecide_']
  .every((n) => typeof sandbox[n] === 'function');
if (!HAVE_FNS) {
  console.log('  [FAIL] pure_functions_exist (chưa viết _claimGcFilter_/_claimAcquireDecide_/_claimCommitDecide_ — RED mong đợi)');
  console.log('== gas_claim_test 0/13 ==');
  process.exit(1);
}

const NOW = Date.parse('2026-07-15T10:00:00.000Z');
const TTL_MS = 5 * 60 * 1000;
const RETENTION_MS = 24 * 60 * 60 * 1000;
function iso(msOffset) { return new Date(NOW + msOffset).toISOString(); }
function row(over) {
  return Object.assign({
    identity_hash: 'h1', state: 'pending', run_id: 'runA',
    acquired_at: iso(0), expires_at: iso(TTL_MS), source_id: '', drive_id: 'd1',
  }, over || {});
}

// ── GC ──
t('gc_drops_old_committed', () => {
  const rows = [row({ state: 'committed', acquired_at: iso(-RETENTION_MS - 1000) })];
  const kept = sandbox._claimGcFilter_(rows, NOW, RETENTION_MS);
  return kept.length === 0;
});
t('gc_keeps_recent_committed', () => {
  const rows = [row({ state: 'committed', acquired_at: iso(-1000) })];
  const kept = sandbox._claimGcFilter_(rows, NOW, RETENTION_MS);
  return kept.length === 1;
});
t('gc_drops_old_released', () => {
  const rows = [row({ state: 'released', acquired_at: iso(-RETENTION_MS - 1) })];
  return sandbox._claimGcFilter_(rows, NOW, RETENTION_MS).length === 0;
});
t('gc_keeps_pending_regardless_of_age', () => {
  // pending KHÔNG bị GC xoá dù cũ — tự chữa qua acquire-reclaim (D10: lazy GC chỉ dọn terminal states).
  const rows = [row({ state: 'pending', acquired_at: iso(-RETENTION_MS - 999999) })];
  return sandbox._claimGcFilter_(rows, NOW, RETENTION_MS).length === 1;
});

// ── Acquire: ca cơ bản ──
t('acquire_no_existing_grants_new', () => {
  const d = sandbox._claimAcquireDecide_(null, NOW, TTL_MS, 'runA');
  return d.action === 'grant' && d.reason === 'NEW';
});
t('acquire_released_grants_reclaim', () => {
  const d = sandbox._claimAcquireDecide_(row({ state: 'released' }), NOW, TTL_MS, 'runB');
  return d.action === 'grant' && d.reason === 'RELEASED_RECLAIM';
});
t('acquire_committed_denies_with_source_id', () => {
  const d = sandbox._claimAcquireDecide_(row({ state: 'committed', source_id: 'sid-9' }), NOW, TTL_MS, 'runB');
  return d.action === 'deny' && d.reason === 'ALREADY_COMMITTED' && d.source_id === 'sid-9';
});
t('acquire_pending_same_run_id_idempotent_grant', () => {
  const d = sandbox._claimAcquireDecide_(row({ state: 'pending', run_id: 'runA' }), NOW, TTL_MS, 'runA');
  return d.action === 'grant' && d.reason === 'IDEMPOTENT_SAME_OWNER';
});
t('acquire_pending_expired_grants_reclaim', () => {
  const d = sandbox._claimAcquireDecide_(
    row({ state: 'pending', run_id: 'runA', expires_at: iso(-1000) }), NOW, TTL_MS, 'runB');
  return d.action === 'grant' && d.reason === 'EXPIRED_RECLAIM';
});

// ── RACE THẬT: 2 host cùng acquire 1 key, host A tới trước ──
t('race_two_hosts_first_wins_second_denied', () => {
  // t0: chưa ai giữ. Host A acquire trước.
  const dA = sandbox._claimAcquireDecide_(null, NOW, TTL_MS, 'runA');
  if (!(dA.action === 'grant' && dA.reason === 'NEW')) return false;
  // Server GHI row pending run_id=runA (mô phỏng bước ghi ngay sau decide).
  const rowAfterA = row({ state: 'pending', run_id: 'runA', acquired_at: iso(0), expires_at: iso(TTL_MS) });
  // t0+1s: Host B acquire CÙNG key — phải THẤY row A vừa ghi, KHÔNG được cấp.
  const dB = sandbox._claimAcquireDecide_(rowAfterA, NOW + 1000, TTL_MS, 'runB');
  return dB.action === 'deny' && dB.reason === 'HELD_BY_OTHER';
});
t('race_host_b_can_reclaim_after_ttl_if_a_never_committed', () => {
  const rowAfterA = row({ state: 'pending', run_id: 'runA', acquired_at: iso(0), expires_at: iso(TTL_MS) });
  // Host A crash, không bao giờ commit/release. Sau TTL, Host B thử lại.
  const dB = sandbox._claimAcquireDecide_(rowAfterA, NOW + TTL_MS + 1000, TTL_MS, 'runB');
  return dB.action === 'grant' && dB.reason === 'EXPIRED_RECLAIM';
});

// ── Commit ──
t('commit_pending_matching_run_id_ok', () => {
  const c = sandbox._claimCommitDecide_(row({ state: 'pending', run_id: 'runA' }), 'runA', NOW);
  return c.ok === true && c.reason === 'COMMITTED';
});
t('commit_wrong_run_id_denied_run_id_mismatch', () => {
  // Ca cốt lõi chống double-commit: claim đã bị host khác reclaim (run_id đổi) — client CŨ (crash-resume)
  // KHÔNG được commit đè lên chủ sở hữu mới.
  const c = sandbox._claimCommitDecide_(row({ state: 'pending', run_id: 'runB' }), 'runA', NOW);
  return c.ok === false && c.reason === 'RUN_ID_MISMATCH';
});
t('commit_already_committed_denied_not_pending', () => {
  const c = sandbox._claimCommitDecide_(row({ state: 'committed', run_id: 'runA' }), 'runA', NOW);
  return c.ok === false && c.reason === 'NOT_PENDING';
});
t('commit_no_existing_row_denied_not_found', () => {
  const c = sandbox._claimCommitDecide_(null, 'runA', NOW);
  return c.ok === false && c.reason === 'NOT_FOUND';
});

// ── Release (D3: giải phóng tường minh khi fail vĩnh viễn) ──
t('release_owner_pending_ok', () => {
  const r = sandbox._claimReleaseDecide_(row({ state: 'pending', run_id: 'runA' }), 'runA');
  return r.ok === true && r.reason === 'RELEASED';
});
t('release_wrong_owner_denied', () => {
  // Chặn caller lạ giải phóng claim NGƯỜI KHÁC đang giữ (vd claim đã bị host khác reclaim sau TTL).
  const r = sandbox._claimReleaseDecide_(row({ state: 'pending', run_id: 'runB' }), 'runA');
  return r.ok === false && r.reason === 'RUN_ID_MISMATCH';
});
t('release_nonexistent_is_idempotent_noop', () => {
  const r = sandbox._claimReleaseDecide_(null, 'runA');
  return r.ok === true && r.reason === 'NOOP_NOT_FOUND';
});
t('release_already_committed_is_idempotent_noop', () => {
  const r = sandbox._claimReleaseDecide_(row({ state: 'committed', run_id: 'runA' }), 'runA');
  return r.ok === true && r.reason === 'NOOP_NOT_PENDING';
});

let ok = 0;
for (const [name, passed] of cases) {
  console.log('  [' + (passed ? 'OK' : 'FAIL') + '] ' + name);
  if (passed) ok++;
}
console.log('== gas_claim_test ' + ok + '/' + cases.length + ' ==');
process.exit(ok === cases.length ? 0 : 1);
