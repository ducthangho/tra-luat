"""Phản chứng vòng 3: đo RĂNG của bốn bản vá, mỗi bản vá một phép gỡ RIÊNG.

Chạy trên BẢN SAO TẠM — không bao giờ ghi vào cây thật (bài học "đột biến ghi vào tệp THẬT rồi
khôi phục trong finally là bom hẹn giờ").
"""
import os
import pathlib
import shutil
import subprocess
import sys

GOC = pathlib.Path("/home/user/tra-luat")
SAN = pathlib.Path(__file__).resolve().parent / "pc"
NGUON = (GOC / "ops/lease_publish_test.py").read_text(encoding="utf-8")


def dung_cay(ten, nguon):
    d = SAN / ten
    shutil.rmtree(d, ignore_errors=True)
    (d / "ops").mkdir(parents=True)
    for t in ("lease_publish.py", "cai_actionlint.sh", "chay_lease_publish_test.sh"):
        if (GOC / "ops" / t).exists():
            shutil.copy2(GOC / "ops" / t, d / "ops" / t)
    shutil.copytree(GOC / ".github", d / ".github")
    (d / ".claude" / "dev").mkdir(parents=True)
    for t in ("launcher.py", "launcher_test.py"):
        shutil.copy2(GOC / ".claude/dev" / t, d / ".claude/dev" / t)
    (d / "ops/lease_publish_test.py").write_text(nguon, encoding="utf-8")
    return d / "ops/lease_publish_test.py"


def chay(tep, tien_to, han=1800):
    mt = {k: v for k, v in os.environ.items() if k != "GITHUB_ACTOR"}
    mt["PYTHONDONTWRITEBYTECODE"] = "1"
    r = subprocess.run([sys.executable, "-B", str(tep), "--chi-ca=" + tien_to],
                       capture_output=True, env=mt, timeout=han)
    return r.returncode, r.stdout.decode("utf-8", "replace")


def ap(nguon, cu, moi, nhan):
    n = nguon.count(cu)
    if n != 1:
        raise SystemExit("KHONG DO DUOC: neo cua %s khop %d lan, phai dung 1" % (nhan, n))
    return nguon.replace(cu, moi)


def bao(nhan, rc, out, ky_vong_do=True):
    tom = [x for x in out.splitlines()
           if "tu kiem" in x or "ự kiểm" in x or "fail-close" in x
           or x.startswith("lease_publish:")]
    dat = (rc != 0) if ky_vong_do else (rc == 0)
    print("%-52s rc=%-3s %s" % (nhan, rc, "CO RANG" if dat else "!!! KHONG RANG"))
    for x in tom:
        print("        " + x)
    return dat


ket = []

# === 1. Lop m5-van-cham-chet-bang-chuoi: tiem Exception thay TinHieuChotCa tai chot cuoi t162 ===
# Day la DUNG phep tiem ma cross-review vong 2 dung de bac ban va vong 1 (luc do: 7/7, rc=0).
CU = '    chot(not lech, f"control LỆCH phân hạng: {lech}")'
MOI = ('    if lech:\n'
       '        raise Exception(f"control LỆCH phân hạng: {lech}")')
rc, out = chay(dung_cay("tiem-exception", ap(NGUON, CU, MOI, "tiem-Exception")), "t163")
ket.append(bao("P2-3 tiem Exception tai chot cuoi t162", rc, out))

# === 2. DOI BIEN: cung phep tiem, nhung GO cot NHAN THO ===
# Muc dich: chung minh so muc bi bat la NHO cot moi, khong phai nho mot chot co san.
# PHEP DO LA MOT CON SO, KHONG PHAI rc: hai muc (`bo-chot-DO_KHAC...`, `bo-CA-HAI-chot-vat-hoa...`)
# ky vong kenh=GIET nen chot `phan_hang != [kenh_mong]` CO SAN da bat chung; ba muc `dong-luot-*`
# ky vong KDD nen CHI cot NHAN THO phan biet duoc. Vi vay doi "go cot => rc=0" la doi sai — bao
# nhieu muc bi bat moi la dai luong dung.
CU2 = '            elif nhan_tho != [nhan_mong]:'
MOI2 = '            elif False:'
nguon2 = ap(ap(NGUON, CU, MOI, "tiem-Exception"), CU2, MOI2, "go-chot-nhan-tho")
rc, out = chay(dung_cay("go-nhan-tho", nguon2), "t163")


def dem_dat(txt):
    for x in txt.splitlines():
        if "ự kiểm bộ chấm 512: đạt" in x:
            return int(x.split("đạt")[1].split("/")[0].strip())
    return None


DAT_CO_COT = 6      # do o phep do 1 ngay tren
dat_khong_cot = dem_dat(out)
print("%-52s dat=%s (co cot: %s)" % ("   doi bien: go cot NHAN THO", dat_khong_cot, DAT_CO_COT))
ok2 = dat_khong_cot is not None and dat_khong_cot > DAT_CO_COT
print("        KET LUAN: cot NHAN THO bat THEM %s muc ma khong chot nao khac bat duoc"
      % (None if dat_khong_cot is None else dat_khong_cot - DAT_CO_COT))
ket.append(ok2)

# === 3. Lop control-bo-sot: go RIENG sau chot ma sau fixture moi cua t164 canh ===
SAU_CHOT = [
    ("vua-mang-ca-vua-dong-luot",
     '        if co_ca and co_dong:\n            return KHONG_DO_DUOC, "bản ghi vừa mang tên ca vừa khai đóng lượt"',
     '        if False:\n            return KHONG_DO_DUOC, "bản ghi vừa mang tên ca vừa khai đóng lượt"'),
    ("vo-doc_kenh-bat-ngoai-le",
     '    except Exception as exc:                  # noqa: BLE001 — fail-close CÓ CHỦ ĐÍCH\n        return KHONG_DO_DUOC, f"bộ đọc kênh ném {type(exc).__name__}: {exc}"',
     '    except _KhongAiNem512 as exc:\n        return KHONG_DO_DUOC, f"bộ đọc kênh ném {type(exc).__name__}: {exc}"'),
    ("dau-dong-khong-phai-true",
     '        if "dong_luot" in r and not co_dong:',
     '        if False:'),
    ("chi-tiet-khong-phai-chuoi",
     '        if not isinstance(ct, str):',
     '        if False:'),
    ("ca-khong-khop-tien-to",
     '    if la:\n        return KHONG_DO_DUOC, f"kênh có ca KHÔNG khớp tiền tố {tien_to!r}: {la}"',
     '    if False:\n        return KHONG_DO_DUOC, f"kênh có ca KHÔNG khớp tiền tố {tien_to!r}: {la}"'),
    ("dich-khong-co-mat",
     '    if vang:\n        return KHONG_DO_DUOC, f"đích KHÔNG có mặt trong kênh: {vang}"',
     '    if False:\n        return KHONG_DO_DUOC, f"đích KHÔNG có mặt trong kênh: {vang}"'),
]
for nhan, cu, moi in SAU_CHOT:
    rc, out = chay(dung_cay("t164-" + nhan, ap(NGUON, cu, moi, nhan)), "t164")
    ket.append(bao("P2-1 t164 go chot: " + nhan, rc, out))

print()
print("TONG: %d/%d phep do DAT" % (sum(ket), len(ket)))
raise SystemExit(0 if all(ket) else 1)
