"""Ma tran dot bien cho do_q6_hk.py (ban hau kiem connector #652; do_q6.py/mut_q6.py giu nguyen vi dac ta dong bang trich bam cua chung) --tu-kiem: tap ca dich KHAI TRUOC, doi khop dung tap; crash = LECH.

Phan hang (hau kiem connector #652, P2): truoc khi so tap, DOI ma thoat — tap dich rong => rc 0,
co dich => rc 1; moi kieu ket thuc khac (rc 2, SIGKILL/OOM am, loi trinh thong dich khong in
Traceback) la LECH. Thieu chot nay thi mutant chet som khong de lai dong HONG nao duoc tinh KHOP
voi tap dich rong. Mutant khai `mong="LECH"` la DOI CHUNG cho chinh chot ay: no phai ra LECH.
"""
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
 "doc-cay-HEAD":([('git("ls-tree", "-r", "-z", moc,','git("ls-tree", "-r", "-z", "HEAD",')],{"cay-sau-khong-doi-cay-moc"}),
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

def phan_hang(rc,hong,stderr,dich):
    if 'Traceback' in stderr: return False
    if rc!=(1 if dich else 0): return False
    return hong==dich
# Tu kiem bo phan hang: moi ca la mot cach chet ma ban cu (khong doc rc) cap tin dung gia.
for rc,hong,err,dich,mong in [(0,set(),"",set(),True),(1,{"a"},"",{"a"},True),
        (2,set(),"",set(),False),(-9,set(),"",set(),False),(0,{"a"},"",{"a"},False),
        (1,set(),"",set(),False),(1,{"a"},"Traceback (most recent call last)",{"a"},False)]:
    assert phan_hang(rc,hong,err,dich)==mong,(rc,hong,err,dich,mong)
KHONG_Z=('git("ls-tree", "-r", "-z", moc, "--", "ops/leases").split("\\0")','git("ls-tree", "-r", moc, "--", "ops/leases").splitlines()')
# Khong -z thi git trich dan MOI ten co byte dieu khien/khong-UTF-8 => ca bon ca ten deu lot ra ngoai_mien.
mut["doc-ls-tree-khong-z"]=([KHONG_Z],{"ten-co-tab","ten-xuong-dong-sau-duoi","ten-DEL-sau-duoi","ten-byte-sau-duoi"})
# Chot ky tu dieu khien: ten co tab van bi chot ten che (lease_id "bad" != "bad\tname"), nen go no chi lo hai ca ky tu dieu khien dat SAU duoi (xuong dong, DEL).
mut["bo-chot-ky-tu-dieu-khien"]=([('        if any(ord(c) < 0x20 or ord(c) == 0x7F for c in duong):\n','        if False:\n')],{"ten-xuong-dong-sau-duoi","ten-DEL-sau-duoi"})
mut["bo-rieng-DEL"]=([(' or ord(c) == 0x7F for c in duong','  for c in duong')],{"ten-DEL-sau-duoi"})
mut["bo-chot-utf8"]=([('        if any(0xDC80 <= ord(c) <= 0xDCFF for c in duong):\n','        if False:\n')],{"ten-byte-sau-duoi"})
# Doi chung cho chot rc: chet som bang rc 2, khong Traceback, khong dong HONG nao. Phai ra LECH.
mut["chet-im-lang-rc2"]=([('    lp = _nap_lp(goc)\n','    lp = _nap_lp(goc)\n    sys.exit(2)\n')],set(),"LECH")
ok_all=True
for ten,(sua,dich,*mong) in mut.items():
    s2=src
    for a,b in sua:
        assert s2.count(a)==1,(ten,a); s2=s2.replace(a,b)
    f=M/f"{ten}.py"; f.write_text(s2)
    r=subprocess.run([sys.executable,"-B",str(f),"--tu-kiem",str(goc)],capture_output=True,text=True)
    hong={l.split()[1].rstrip(':') for l in r.stdout.splitlines() if l.startswith("HONG")}
    crash='Traceback' in r.stderr; khop=phan_hang(r.returncode,hong,r.stderr,dich)
    kq='KHOP' if khop else 'LECH'; ok=(kq==(mong[0] if mong else 'KHOP')); ok_all&=ok
    print(f"{'DUNG' if ok else 'SAI '} {kq} {ten}: rc={r.returncode} do={sorted(hong)} khai={sorted(dich)}{' mong='+mong[0] if mong else ''}{' CRASH' if crash else ''}")
print("TAT_CA_KHOP" if ok_all else "CO_LECH"); sys.exit(0 if ok_all else 1)
