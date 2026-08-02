#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
backfill_keywords_live.py — BƠM `tukhoa` khi CHƯA có parsed-cache (L1 trống, không có kho L2 doc).

Nguồn heading = EXPORT TEXT từng Google Doc qua webapp (server-side, KHÔNG qua context):
  exporttext(drive_id) → split_articles → keywords.extract_keywords → reg_bulk vá cột 'tukhoa'.
Chỉ xử lý dòng có gdoc là Google Doc (NLM chỉ nạp GDoc; đây cũng là tập Claude sẽ notebook_query).
Có CHECKPOINT (/tmp/tukhoa_progress.json) + ngân sách thời gian/đợt + vá reg_bulk theo lô
⇒ chạy lại nhiều lần tới khi hết. KHÔNG AI/RAG.

ENV: TL_WEBAPP, TL_TOKEN.
VD:  python3 backfill_keywords_live.py --manifest /tmp/manifest.json --budget 200 --batch 40
"""
import sys, json, os, time, argparse
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import gas
from keywords import extract_keywords
from verify_deep import split_articles

GDOC_MIME = 'application/vnd.google-apps.document'
import tempfile as _tf  # cross-platform: /tmp không có trên Windows → dùng thư mục tạm hệ điều hành
PROG = os.path.join(_tf.gettempdir(), 'tukhoa_progress.json')


# ── r292 (RAS-05, P1 — Slice R0) ────────────────────────────────────────────────────────────────────
# Ba lỗ của bản trước, tất cả cùng MẪU A (kết luận bằng hình dạng, không bằng kết quả):
#  (1) `prog['done']` vừa là sổ-đã-xong VỪA là BỘ LỌC worklist. Doc `exporttext` lỗi bị ghi
#      `done[gid]='err'` ⇒ **loại VĨNH VIỄN** khỏi mọi đợt sau. Mất dữ liệu IM LẶNG.
#  (2) `reg_bulk` **không kiểm `rb['ok']`**, chỉ cộng `patched`; mà item đã bị đánh `done='ok'` từ
#      TRƯỚC lúc gọi ⇒ lô ghi hỏng vẫn coi như xong.
#  (3) `remaining` tính lại từ chính `done` (đã nhiễm) ⇒ `remaining==0` in **"XONG TẤT CẢ."**,
#      `main()` return None ⇒ **rc=0**. Báo thành công cho một việc chưa xong.
#
# Nay: state machine tường minh. `committed` = ĐÃ ghi được và đã đối chiếu; `blocked` = kết cục XÁC
# ĐỊNH, chạy lại cũng thế (không có từ khoá nào bóc ra được); `retryable` = HỎNG, PHẢI thử lại;
# `inflight` = đã bóc xong nhưng CHƯA có xác nhận ghi — chỉ `committed`/`blocked` mới rời worklist.
PROGRESS_SCHEMA = 'tukhoa_progress.v2'
_TERMINAL = ('committed', 'blocked')


def migrate_progress(p):
    """Nâng checkpoint v1 → v2. ĐỌC ĐƯỢC BẢN CŨ là bắt buộc: file v1 đang nằm trên máy người giữ và
    chính nó là bằng chứng thiệt hại (§6.2 Pha 3.5) — vứt đi là mất luôn manh mối.

    Ánh xạ: `ok`→`committed` · `empty`→`blocked`(EMPTY_KEYWORDS) · `err*`→**`retryable`**.
    Chính vế cuối là bản vá: doc từng bị `err` nay **quay lại** worklist thay vì mất vĩnh viễn.
    """
    if not isinstance(p, dict):
        p = {}
    if p.get('schema') == PROGRESS_SCHEMA and isinstance(p.get('state'), dict):
        p.setdefault('reason', {})
        return p
    state, reason = {}, {}
    for gid, v in (p.get('done') or {}).items():
        sv = str(v or '')
        if sv == 'ok':
            state[gid] = 'committed'
        elif sv == 'empty':
            state[gid] = 'blocked'; reason[gid] = 'EMPTY_KEYWORDS'
        else:
            state[gid] = 'retryable'; reason[gid] = 'MIGRATED_V1:' + (sv[:60] or 'err')
    return {'schema': PROGRESS_SCHEMA, 'state': state, 'reason': reason,
            'patched': int(p.get('patched') or 0), 'empty': int(p.get('empty') or 0),
            'err': int(p.get('err') or 0)}


def load_progress(path):
    try:
        raw = json.load(open(path, encoding='utf-8'))
    except Exception:
        raw = {}
    return migrate_progress(raw)


def save_progress(path, p):
    # ATOMIC: đợt trước từng ghi thẳng — chết giữa chừng là mất sổ, mà sổ chính là thứ giữ tiến độ.
    tmp = str(path) + '.tmp'
    with open(tmp, 'w', encoding='utf-8') as f:
        json.dump(p, f, ensure_ascii=False)
    os.replace(tmp, path)


def pending(wl, prog):
    """Việc còn phải làm = mọi mục CHƯA ở trạng thái kết thúc. `retryable`/`inflight` QUAY LẠI hàng đợi."""
    st = prog.get('state') or {}
    return [w for w in wl if st.get(w['drive_id']) not in _TERMINAL]


def reg_bulk_verdict(rb, n_items):
    """Kết luận một lô `reg_bulk` bằng KẾT QUẢ. Trả (ok, lý_do).

    `ok=true` CHƯA đủ: lô có thể `patched < gửi` (dòng không khớp `drive_id`) — phần hụt đó CHƯA được
    ghi, nên cả lô phải quay về `retryable` chứ không được đánh dấu xong.
    """
    if not isinstance(rb, dict):
        return False, 'REG_BULK_HINH_DANG_LA_' + type(rb).__name__.upper()
    if 'ok' not in rb:
        return False, 'REG_BULK_THIEU_TRUONG_OK'
    if not rb.get('ok'):
        return False, 'REG_BULK_AM:' + str(rb.get('error') or 'ok=false')[:80]
    try:
        patched = int(rb.get('patched') or 0)
    except (TypeError, ValueError):
        return False, 'REG_BULK_PATCHED_KHONG_DOC_DUOC'
    if patched < n_items:
        return False, f'REG_BULK_HUT:patched={patched}/{n_items}'
    return True, ''


def worklist(manifest_path, only_nlm):
    m = json.load(open(manifest_path, encoding='utf-8'))
    ents = m.get('entries', m) if isinstance(m, dict) else m
    out = []
    for e in ents:
        gid = e.get('gdoc_id') or e.get('id') or e.get('drive_id')
        if not gid: continue
        if (e.get('mime') or '') != GDOC_MIME: continue          # chỉ GDoc export text được
        if only_nlm and not e.get('nlm_source_id'): continue      # mặc định: tập trên NLM
        if e.get('tukhoa'): continue                              # đã có (manifest mới)
        out.append({'drive_id': gid, 'nlm_source_id': e.get('nlm_source_id') or '',
                    'name': e.get('name') or '', 'so_hieu': e.get('so_hieu') or ''})
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument('--manifest', required=True)
    ap.add_argument('--budget', type=int, default=200, help='ngân sách giây/đợt')
    ap.add_argument('--batch', type=int, default=40, help='vá reg_bulk mỗi N doc')
    ap.add_argument('--all', action='store_true', help='cả doc chưa lên NLM (mặc định chỉ NLM)')
    ap.add_argument('--progress', default=PROG)
    # r310 (RAS-01 vế metadata/CLI): script này TRƯỚC ĐÂY không có đường chạy chỉ-đọc nào — mọi lần gọi
    # đều đi thẳng vào `exporttext` + `reg_bulk` + ghi checkpoint. `tl rasoat keywords` thiếu `--apply`
    # nay bơm cờ này. DRY = KHÔNG `exporttext`, KHÔNG `reg_bulk`, và KHÔNG lưu checkpoint: một lượt "dry"
    # mà vẫn dịch sổ tiến độ thì đúng là bệnh RAS-01 đang chữa, chỉ đổi chỗ.
    ap.add_argument('--dry', action='store_true',
                    help='chỉ-đọc: kê worklist rồi dừng — không exporttext, không reg_bulk, không ghi checkpoint')
    a = ap.parse_args()

    prog = load_progress(a.progress)
    st, rs = prog['state'], prog['reason']
    wl_all = worklist(a.manifest, not a.all)
    wl = pending(wl_all, prog)

    if a.dry:
        out = {'ok': True, 'dry': True, 'con_lai': len(wl), 'tong_worklist': len(wl_all),
               'da_chot': sum(1 for v in st.values() if v == 'committed'),
               'thu_lai': sum(1 for v in st.values() if v == 'retryable'),
               'treo_inflight': sum(1 for v in st.values() if v == 'inflight'),
               'bo_qua_co_ly_do': sum(1 for v in st.values() if v == 'blocked'),
               'vi_du': [w['drive_id'] for w in wl[:5]],
               'ghi_chu': 'DRY — chưa gọi exporttext/reg_bulk, checkpoint KHÔNG đổi. Thêm --apply '
                          '(qua `tl rasoat keywords … --apply`) để ghi thật.'}
        print(json.dumps(out, ensure_ascii=False))
        return 0
    _lai = sum(1 for w in wl if st.get(w['drive_id']) in ('retryable', 'inflight'))
    print(f"[worklist] còn {len(wl)} doc cần bóc tukhoa "
          f"(đã chốt {sum(1 for v in st.values() if v == 'committed')}, "
          f"bỏ qua có lý do {sum(1 for v in st.values() if v == 'blocked')}, "
          f"THỬ LẠI {_lai})")

    t0 = time.time(); items = []; n = 0

    def _flush(nhan):
        """Vá một lô rồi ĐỐI CHIẾU. Chỉ lô ĐƯỢC XÁC NHẬN mới chuyển `committed`; hỏng ⇒ `retryable`."""
        nonlocal items
        if not items:
            return
        _gids = [x['drive_id'] for x in items]
        try:
            rb = gas.post('reg_bulk', items=json.dumps(items, ensure_ascii=False), cols='tukhoa')
        except Exception as e:
            rb = {'ok': False, 'error': f'{type(e).__name__}: {e}'}
        _ok, _why = reg_bulk_verdict(rb, len(items))
        if _ok:
            prog['patched'] += int(rb.get('patched') or 0)
            for g in _gids:
                st[g] = 'committed'; rs.pop(g, None)
            print(f"  reg_bulk {nhan}: patched={rb.get('patched')} missed={rb.get('missed')} "
                  f"(tổng patched={prog['patched']})")
        else:
            prog['err'] += len(_gids)
            for g in _gids:
                st[g] = 'retryable'; rs[g] = _why
            print(f"  ✗ reg_bulk {nhan} HỎNG ({_why}) → {len(_gids)} doc về hàng THỬ LẠI, "
                  f"KHÔNG đánh dấu xong", file=sys.stderr)
        items = []
        save_progress(a.progress, prog)

    try:
        for w in wl:
            if time.time() - t0 > a.budget:
                print(f"[budget] hết {a.budget}s — dừng đợt (xử lý {n})"); break
            gid = w['drive_id']
            try:
                r = gas.get('exporttext', fileId=gid)
                if not isinstance(r, dict) or not r.get('ok'):
                    # LỖI ⇒ `retryable`, KHÔNG phải "xong". Đây chính là lỗ (1).
                    prog['err'] += 1
                    st[gid] = 'retryable'
                    rs[gid] = 'EXPORTTEXT_AM:' + str((r or {}).get('error') if isinstance(r, dict) else r)[:80]
                    n += 1
                    continue
                text = r.get('text') or ''
                rec = {'so_hieu': w['so_hieu'], 'articles': split_articles(text), 'text': text}
                kw = extract_keywords(rec)
                if kw:
                    it = {'drive_id': gid, 'tukhoa': kw}
                    if w['nlm_source_id']: it['nlm_source_id'] = w['nlm_source_id']
                    items.append(it)
                    # CHƯA phải `committed`: mới bóc xong, chưa có xác nhận ghi. Lỗ (2) nằm đúng ở đây.
                    st[gid] = 'inflight'; rs.pop(gid, None)
                else:
                    # Kết cục XÁC ĐỊNH: chạy lại vẫn không có từ khoá nào ⇒ rời worklist, KHÔNG phải lỗi.
                    prog['empty'] += 1
                    st[gid] = 'blocked'; rs[gid] = 'EMPTY_KEYWORDS'
            except Exception as e:
                prog['err'] += 1
                st[gid] = 'retryable'; rs[gid] = f'{type(e).__name__}: {str(e)[:60]}'
            n += 1
            if len(items) >= a.batch:
                _flush('lô')
        _flush('dư')
    finally:
        # Ngắt giữa chừng (Ctrl-C/hết giờ/nổ) cũng phải giữ được sổ — `inflight` còn lại sẽ tự quay
        # về hàng đợi ở đợt sau vì nó KHÔNG nằm trong tập kết thúc.
        save_progress(a.progress, prog)

    remaining = len(pending(wl_all, prog))
    n_retry = sum(1 for v in st.values() if v == 'retryable')
    n_flight = sum(1 for v in st.values() if v == 'inflight')
    out = {'xu_ly_dot_nay': n, 'tong_patched': prog['patched'], 'empty': prog['empty'],
           'err': prog['err'], 'con_lai': remaining, 'thu_lai': n_retry, 'treo_inflight': n_flight,
           'bo_qua_co_ly_do': sum(1 for v in st.values() if v == 'blocked')}
    # Lỗ (3): kết luận nay TÍNH từ `remaining` THẬT (sổ không còn bị nhiễm bởi doc lỗi), và rc≠0 khi
    # còn việc. "XONG TẤT CẢ." chỉ được in khi thật sự không còn gì — kể cả mục phải thử lại.
    out['ok'] = (remaining == 0)
    print(json.dumps(out, ensure_ascii=False))
    if remaining:
        _vd = [g for g, v in st.items() if v == 'retryable'][:5]
        print(f"CÒN {remaining} (thử lại {n_retry}, treo {n_flight}) — gọi lại lệnh này để tiếp."
              + (f" Ví dụ cần thử lại: {', '.join(_vd)}" if _vd else ""), file=sys.stderr)
        return 1
    print("XONG TẤT CẢ.")
    return 0


if __name__ == '__main__':
    # r292: `rc` DẪN XUẤT từ kết luận. Trước đây `main()` return None ⇒ rc=0 kể cả khi còn việc/còn lỗi —
    # cổng vận hành (và người đọc log) không có cách nào biết đợt đó chưa xong.
    sys.exit(main() or 0)
