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


def load_progress(path):
    try: return json.load(open(path, encoding='utf-8'))
    except Exception: return {'done': {}, 'patched': 0, 'empty': 0, 'err': 0}


def save_progress(path, p):
    json.dump(p, open(path, 'w', encoding='utf-8'), ensure_ascii=False)


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
    a = ap.parse_args()

    prog = load_progress(a.progress)
    done = prog['done']
    wl = [w for w in worklist(a.manifest, not a.all) if w['drive_id'] not in done]
    print(f"[worklist] còn {len(wl)} doc cần bóc tukhoa (đã xong {len(done)})")
    if not wl:
        print("HẾT — không còn gì để backfill."); return

    t0 = time.time(); items = []; n = 0
    for w in wl:
        if time.time() - t0 > a.budget:
            print(f"[budget] hết {a.budget}s — dừng đợt (xử lý {n})"); break
        gid = w['drive_id']
        try:
            r = gas.get('exporttext', fileId=gid)
            if not r.get('ok'):
                prog['err'] += 1; done[gid] = 'err'; continue
            text = r.get('text') or ''
            rec = {'so_hieu': w['so_hieu'], 'articles': split_articles(text), 'text': text}
            kw = extract_keywords(rec)
            if kw:
                it = {'drive_id': gid, 'tukhoa': kw}
                if w['nlm_source_id']: it['nlm_source_id'] = w['nlm_source_id']
                items.append(it); done[gid] = 'ok'
            else:
                prog['empty'] += 1; done[gid] = 'empty'
        except Exception as e:
            prog['err'] += 1; done[gid] = 'err:' + str(e)[:60]
        n += 1
        # vá theo lô để tiến độ bền
        if len(items) >= a.batch:
            rb = gas.post('reg_bulk', items=json.dumps(items, ensure_ascii=False), cols='tukhoa')
            prog['patched'] += int(rb.get('patched') or 0)
            print(f"  reg_bulk lô: patched={rb.get('patched')} missed={rb.get('missed')} (tổng patched={prog['patched']})")
            items = []
            save_progress(a.progress, prog)
    # vá phần dư
    if items:
        rb = gas.post('reg_bulk', items=json.dumps(items, ensure_ascii=False), cols='tukhoa')
        prog['patched'] += int(rb.get('patched') or 0)
        print(f"  reg_bulk dư: patched={rb.get('patched')} missed={rb.get('missed')} (tổng patched={prog['patched']})")
    save_progress(a.progress, prog)

    remaining = len([w for w in worklist(a.manifest, not a.all) if w['drive_id'] not in done])
    print(json.dumps({'xu_ly_dot_nay': n, 'tong_patched': prog['patched'],
                      'empty': prog['empty'], 'err': prog['err'], 'con_lai': remaining},
                     ensure_ascii=False))
    if remaining: print(f"CÒN {remaining} — gọi lại lệnh này để tiếp.")
    else: print("XONG TẤT CẢ.")


if __name__ == '__main__':
    main()
