"""Ma tran dot bien cho do_q6.py --tu-kiem: tap ca dich KHAI TRUOC, doi khop dung tap; crash = LECH."""
import sys,subprocess
from pathlib import Path
M=Path(sys.argv[1]); goc=Path(sys.argv[2]).resolve(); src=Path(sys.argv[3]).read_text()
B='            vi_pham.append((duong, f"lease_expires_at_utc-hong: {e.thong_diep[:80]}"))\n            continue\n'
mut={
 "goc":([],set()),
 "bo-kiem-ten":([('        if lid != re.sub(r"\\.ya?ml$", "", ten):\n','        if False:\n')],{"sai-ten"}),
 "bo-kiem-mapping":([('        if not isinstance(d, dict):\n            vi_pham.append((duong, f"khong-phai-mapping: {type(d).__name__}"))\n            continue\n','        if not isinstance(d, dict):\n            continue\n')],{"khong-phai-mapping"}),
 "bo-kiem-trung":([('        if lid in L:\n','        if False:\n')],{"trung-id"}),
 "bo-kiem-kieu-thay":([('        if tt is None:\n            vi_pham','        if False:\n            vi_pham')],{"thay-sai-kieu"}),
 "bo-kxd":([('"ma_thoat": 3 if (vi_pham or kxd) else 0','"ma_thoat": 3 if vi_pham else 0')],{"mot-chieu-moi"}),
 "doc-cay-HEAD":([('git("ls-tree", "-r", moc,','git("ls-tree", "-r", "HEAD",')],{"cay-sau-khong-doi-cay-moc"}),
 "bo-loc-han":([('        if d["_han_utc"] <= now:\n            return "HET_HAN"\n','')],{"het-han","han-bang-dung-C","han-bien-duoi-hop-le"}),
 "bo-mien-id":([('not lp.LEASE_ID.fullmatch(lid)','False')],{"id-ngoai-mien-don"}),
 "null-nhu-vang":([('if "da_bi_thay_the" in d and (not isinstance(t, str)','if t is not None and (not isinstance(t, str)')],{"bia-null-moi","bia-null-ngoai-cap","bia-khoa-khong-gia-tri"}),
 "bo-mien-thay":([('any(not lp.LEASE_ID.fullmatch(x) for x in tt or [])','False')],{"thay-phan-tu-ngoai-mien"}),
 "bo-lap-thay":([('len(tt or []) != len(set(tt or []))','False')],{"thay-phan-tu-lap"}),
 "bo-mien-bia":([('if isinstance(t, str) and not lp.LEASE_ID.fullmatch(t):','if False:')],{"bia-gia-tri-ngoai-mien"}),
 "han-hong-coi-nhu-het-han":([(B,'            han = datetime.fromisoformat("2000-01-01T00:00:00+00:00")\n')],{"han-sai-dinh-dang","han-thieu-mui-gio","han-vang"}),  # han vang cung di qua Chan cua _doc_han
 "han-tran-coi-nhu-het-han":([('            vi_pham.append((duong, "lease_expires_at_utc-hong: vuot-mien-UTC"))\n            continue\n', '            han = datetime.fromisoformat("2000-01-01T00:00:00+00:00")\n')],{"han-tran-UTC-tren","han-tran-UTC-duoi"}),
 "han-bang-coi-nhu-con-han":([('        if d["_han_utc"] <= now:\n','        if d["_han_utc"] < now:\n')],{"han-bang-dung-C"}),
 "nhan-thu-muc-con":([('        if "/" in ten:\n','        if False:\n'),('        if lid != re.sub(r"\\.ya?ml$", "", ten):\n','        if lid != re.sub(r"\\.ya?ml$", "", ten.rsplit("/", 1)[-1]):\n')],{"thu-muc-con"}),
 "han-vang-mac-dinh-nam-2000":([('lp._doc_han(d.get("lease_expires_at_utc"))','lp._doc_han(d.get("lease_expires_at_utc") or "2000-01-01T00:00:00Z")')],{"han-vang"}),
 "tu-choi-nam-bien":([('            han = lp._doc_han(d.get("lease_expires_at_utc"))\n','            han = lp._doc_han(d.get("lease_expires_at_utc"))\n            if han.year in (1, 9999):\n                raise OverflowError\n')],{"han-bien-tren-hop-le","han-bien-duoi-hop-le"}),
 # Chot thu muc con bi chot ten CHE (ten "sub/z" != lease_id "z"; LEASE_ID cam "/") => go rieng no khong doi ca nao.
 # Khai tap dich RONG co chu dich: day la bang chung hai chot che nhau, khong phai ca thua.
 "bo-qua-im-lang-tep-han-bien":([('            han = lp._doc_han(d.get("lease_expires_at_utc"))\n','            han = lp._doc_han(d.get("lease_expires_at_utc"))\n            if han.year in (1, 9999):\n                continue\n')],{"han-bien-tren-hop-le","han-bien-duoi-hop-le"}),
 "bo-rieng-chot-thu-muc-con":([('        if "/" in ten:\n','        if False:\n')],set()),
 "bo-mien-ca-ba-cho":([('not lp.LEASE_ID.fullmatch(lid)','False'),('any(not lp.LEASE_ID.fullmatch(x) for x in tt or [])','False'),('if isinstance(t, str) and not lp.LEASE_ID.fullmatch(t):','if False:')],
    {"id-ngoai-mien-don","id-ngoai-mien-cu","id-ngoai-mien-moi","thay-phan-tu-ngoai-mien","bia-gia-tri-ngoai-mien"}),
}
ok_all=True
for ten,(sua,dich) in mut.items():
    s2=src
    for a,b in sua:
        assert s2.count(a)==1,(ten,a); s2=s2.replace(a,b)
    f=M/f"{ten}.py"; f.write_text(s2)
    r=subprocess.run([sys.executable,"-B",str(f),"--tu-kiem",str(goc)],capture_output=True,text=True)
    hong={l.split()[1].rstrip(':') for l in r.stdout.splitlines() if l.startswith("HONG")}
    crash='Traceback' in r.stderr; ok=(hong==dich) and not crash; ok_all&=ok
    print(f"{'KHOP' if ok else 'LECH'} {ten}: rc={r.returncode} do={sorted(hong)} khai={sorted(dich)}{' CRASH' if crash else ''}")
print("TAT_CA_KHOP" if ok_all else "CO_LECH"); sys.exit(0 if ok_all else 1)
