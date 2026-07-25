#!/usr/bin/env node
/**
 * gas_reglock_test.js — Node harness cho v2.21.2p: ATOMIC registry read-modify-write.
 *
 * BỐI CẢNH (sự cố 2026-07-25, registry 1.313 → 2 dòng): regReadAll_ chạy NGOÀI lock, regWriteAll_ chỉ
 * khóa phần GHI. Giữa deleteSheet(old) và tmp.setName(REG_TAB_) KHÔNG tồn tại tab `files`; request song
 * song đọc đúng lúc đó thì ensureRegTabs_ LẶNG LẼ TẠO TAB RỖNG → 0 dòng → ghi đè cả registry.
 *
 * Harness nạp Code.gs qua vm với stub GAS TỐI THIỂU, nhưng LockService/SpreadsheetApp là stub CÓ TRẠNG
 * THÁI (faithful vừa đủ) để mô phỏng đúng ba thứ:
 *   (1) Lock của Apps Script KHÔNG đếm tầng — releaseLock() lồng nhau nhả SỚM (bẫy KI-25);
 *   (2) cửa sổ swap: tab `files` biến mất trong khi `files_tmp` còn (bẫy KI-26);
 *   (3) chốt chặn co thảm họa + sao lưu xoay vòng (KI-27).
 *
 * Chạy: node references/gas_reglock_test.js [đường dẫn .gs, mặc định ../../gas-project/Code.gs]
 */
'use strict';
const fs = require('fs');
const path = require('path');
const vm = require('vm');

const gsPath = process.argv[2]
  ? path.resolve(process.argv[2])
  : path.resolve(__dirname, '..', '..', 'gas-project', 'Code.gs');
const code = fs.readFileSync(gsPath, 'utf8');

function makeStubService(name) {
  return new Proxy({}, {
    get(_t, prop) {
      if (prop === Symbol.toPrimitive || typeof prop === 'symbol') return undefined;
      return (..._a) => makeStubService(name + '.' + String(prop));
    },
    apply() { return makeStubService(name); },
  });
}

// ── LockService CÓ TRẠNG THÁI: mô phỏng đúng ngữ nghĩa Apps Script (không đếm tầng) ──
let lockHeld = false;
let lockAcquires = 0;
const LockService = {
  getScriptLock() {
    return {
      tryLock(_ms) { if (lockHeld) return false; lockHeld = true; lockAcquires++; return true; },
      releaseLock() { lockHeld = false; },   // ← KHÔNG đếm tầng: nhả là nhả hẳn
      hasLock() { return lockHeld; },
    };
  },
};

const sandbox = {
  console,
  Utilities: { sleep(_ms) {}, computeDigest: () => [], base64Encode: () => '', DigestAlgorithm: {} },
  LockService,
  SpreadsheetApp: makeStubService('SpreadsheetApp'),
  DriveApp: makeStubService('DriveApp'),
  CacheService: makeStubService('CacheService'),
  PropertiesService: makeStubService('PropertiesService'),
  UrlFetchApp: makeStubService('UrlFetchApp'),
  Session: makeStubService('Session'),
  ScriptApp: makeStubService('ScriptApp'),
  Drive: makeStubService('Drive'),
  HtmlService: makeStubService('HtmlService'),
  ContentService: makeStubService('ContentService'),
};
sandbox.globalThis = sandbox;
vm.createContext(sandbox);
vm.runInContext(code, sandbox, { filename: gsPath });

/** Thân hàm top-level, cắt tới `\nfunction ` kế tiếp — KHÔNG dùng cửa sổ N ký tự cố định
 *  (cửa sổ cố định tràn sang hàm sau ⇒ dương tính GIẢ; đã trả giá khi viết harness này). */
function fnBody(name) {
  const i = code.indexOf('\nfunction ' + name);
  if (i < 0) return null;
  const j = code.indexOf('\nfunction ', i + 1);
  return code.slice(i, j < 0 ? code.length : j);
}

const cases = [];
const t = (name, fn) => {
  let passed = false;
  try { passed = !!fn(); } catch (e) { passed = false; cases.push([name + ' (THREW: ' + e.message + ')', false]); return; }
  cases.push([name, passed]);
};

// ───────── KI-25: withRegLock_ re-entrant, lock thật chỉ lấy/nhả ở tầng NGOÀI CÙNG ─────────
t('ki25_withRegLock_om_tron_va_re_entrant', () => {
  lockHeld = false; lockAcquires = 0;
  let insideOuter = null, insideInner = null;
  const r = sandbox.withRegLock_(function () {
    insideOuter = lockHeld;
    sandbox.withRegLock_(function () { insideInner = lockHeld; return 1; });
    // ★ điểm chí tử: sau khi hàm LỒNG trả về, lock PHẢI còn giữ. Nếu tầng trong nhả sớm
    //   (bẫy Apps Script không đếm tầng) thì chu trình đọc-sửa-ghi hở đúng như sự cố 25-07.
    return lockHeld ? 'STILL_HELD' : 'RELEASED_EARLY';
  });
  return insideOuter === true && insideInner === true && r === 'STILL_HELD'
    && lockHeld === false          // nhả sạch khi ra tầng ngoài
    && lockAcquires === 1;         // chỉ lấy lock MỘT lần cho cả chuỗi lồng
});

t('ki25_nha_lock_ca_khi_fn_nem_loi', () => {
  lockHeld = false;
  try { sandbox.withRegLock_(function () { throw new Error('boom'); }); } catch (_e) { /* mong đợi */ }
  return lockHeld === false;
});

t('ki25_lock_ban_thi_nem_busy_khong_ghi', () => {
  lockHeld = true;               // giả lập request khác đang giữ
  let ran = false;
  let msg = '';
  try { sandbox.withRegLock_(function () { ran = true; }); } catch (e) { msg = e.message; }
  lockHeld = false;
  return ran === false && /busy/i.test(msg);
});

// ───────── KI-27: số học chốt chặn co thảm họa (thuần, không đụng Sheet) ─────────
// Tái tạo ĐÚNG biểu thức trong regWriteAll_ để khóa ngưỡng khỏi trôi âm thầm.
function refuse(oldN, newN, expectShrink) {
  const A = sandbox.REG_SHRINK_ABS_, F = sandbox.REG_SHRINK_FRAC_;
  if (!(oldN > 0 && newN < oldN)) return false;
  const lost = oldN - newN;
  const catastrophic = (lost > A) || (lost > oldN * F);
  return catastrophic && lost > (expectShrink || 0);
}

t('ki27_bat_dung_ca_su_co_1313_ve_2', () => refuse(1313, 2, 0) === true);
t('ki27_khong_chan_xoa_le_1_20_dong', () => refuse(1315, 1314, 0) === false && refuse(1315, 1295, 0) === false);
t('ki27_khong_chan_lo_118_dong_da_khai', () => refuse(1315, 1197, 118) === false);
t('ki27_van_chan_khi_khai_thieu', () => refuse(1315, 2, 118) === true);
t('ki27_khong_chan_khi_registry_dang_trong', () => refuse(0, 5, 0) === false);
t('ki27_khong_chan_khi_tang_dong', () => refuse(100, 101, 0) === false);
t('ki27_nguong_dung_bang_hang_so_cua_file', () => sandbox.REG_SHRINK_ABS_ === 100 && sandbox.REG_SHRINK_FRAC_ === 0.5);
t('ki27_co_qua_nua_bi_chan_du_duoi_100_dong', () => refuse(150, 70, 0) === true);   // mất 80 < 100 nhưng > 50%

// ───────── KI-27: tham số sao lưu xoay vòng ─────────
t('ki27_hang_so_sao_luu_xoay_vong', () =>
  sandbox.REG_BAK_PREFIX_ === 'files_bak_' && sandbox.REG_BAK_KEEP_ === 5);

t('ki27_co_duong_khoi_phuc_va_da_noi_dispatch', () => {
  // Bản sao mà không có đường khôi phục thì chỉ là rác chiếm ô — khóa cả hai action.
  const list = fnBody('doRegBakList_'), rest = fnBody('doRegBakRestore_');
  return list !== null && rest !== null
    && /case 'reg_bak_list'/.test(code) && /case 'reg_bak_restore'/.test(code)
    && /confirm/.test(rest)                    // thay TOÀN BỘ registry ⇒ phải confirm=yes
    && /withRegLock_/.test(rest)               // khôi phục cũng là ghi ⇒ phải trong lock
    && /REG_BAK_PREFIX_ \+ new Date/.test(rest); // giữ bản đang dùng ⇒ khôi phục đảo ngược được
});

// ───────── Chống hồi quy: KHÔNG còn đường ghi nào tự lấy lock thô ─────────
t('khong_con_lock_tho_trong_duong_ghi_REGISTRY', () => {
  // Ngữ cảnh: getScriptLock() là lock TOÀN SCRIPT, dùng chung với phân hệ claims (F-04). Đợt 2.21.2p
  // chỉ nhận phần REGISTRY. Bất biến cần khóa: mọi lock thô còn lại PHẢI nằm trong withRegLock_ hoặc
  // trong 3 hàm claims đã biết — KHÔNG được mọc thêm ở đường ghi registry (mọc thêm = hở lại KI-25).
  const allowed = ['withRegLock_', 'claimsWriteAll_', 'doIngestClaim_', 'doRegGetBulk_'];
  const owners = [];
  const re = /LockService\.getScriptLock\(\)/g;
  let m;
  while ((m = re.exec(code)) !== null) {
    const before = code.slice(0, m.index);
    const fns = before.match(/\nfunction\s+([A-Za-z0-9_]+)/g) || [];
    owners.push(fns.length ? fns[fns.length - 1].trim().replace(/^function\s+/, '') : '(top)');
  }
  const regWriters = ['regWriteAll_', 'regUpsertOne_', 'doRegClear_', 'doRegBulk_', 'doRegDelete_',
                      'regApplyDeltas_', 'doRegen2_'];
  return owners.length === 4
    && owners.every((o) => allowed.indexOf(o) >= 0)
    && owners.filter((o) => regWriters.indexOf(o) >= 0).length === 0;
});

t('claims_khong_long_vao_duong_ghi_registry', () => {
  // Nếu claims (giữ lock thô) gọi vào regWriteAll_/regUpsertOne_ thì withRegLock_ sẽ nhả lock mà
  // claims còn cần — đúng bẫy nhả sớm, chỉ khác phân hệ. Khóa lại để tương lai không vô tình tạo ra.
  return ['claimsWriteAll_', 'doIngestClaim_', 'doRegGetBulk_'].every((fn) => {
    const body = fnBody(fn);
    return body !== null && !/regWriteAll_\(|regUpsertOne_\(/.test(body);
  });
});

t('cac_ham_RMW_deu_di_qua_withRegLock_', () => {
  const need = ['doRegClear_', 'doRegBulk_', 'doRegDelete_', 'regApplyDeltas_', 'doRegen2_'];
  return need.every((fn) => {
    const body = fnBody(fn);
    return body !== null && body.indexOf('withRegLock_') >= 0;
  });
});

t('ensureRegTabs_ khong_tu_tao_tab_rong_khi_dang_swap', () => {
  const body = fnBody('ensureRegTabs_');
  // phải kiểm tab _tmp (bằng chứng đang swap) + độ sâu lock, và ném busy thay vì tạo tab
  return body !== null && /_tmp/.test(body) && /_REG_LOCK_DEPTH_/.test(body) && /busy/.test(body);
});

let ok = 0;
for (const [name, passed] of cases) {
  console.log('  [' + (passed ? 'OK' : 'FAIL') + '] ' + name);
  if (passed) ok++;
}
console.log('== gas_reglock_test ' + ok + '/' + cases.length + ' ==');
process.exit(ok === cases.length ? 0 : 1);
