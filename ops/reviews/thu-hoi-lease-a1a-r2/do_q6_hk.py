"""Q6 + (b) cho THU-HOI-LEASE-A1a r2: dẫn xuất cặp bia mộ từ ĐÚNG cây mốc, lọc (b) ở clock ghim.

Hiện vật review (không thuộc write set A1a). Đọc bằng yaml.safe_load, không regex nội dung.
Chỉ đọc cây của MOC — không đọc ref nào khác, không đọc HEAD.

Miền lease = mọi blob dưới ops/leases có đuôi .yaml/.yml (đúng miền của _quet_lease_toan_kho);
mọi thứ khác (vd .yaml.nhap) đếm vào `ngoai_mien`, không đọc. Liệt kê bằng `ls-tree -z` (bản ghi thô,
không trích dẫn): không có -z thì git bọc tên có tab/xuống dòng trong ngoặc kép, đuôi thành `.yaml"`
và tệp lọt ra `ngoai_mien` im lặng (hậu kiểm connector #652). Tên có ký tự điều khiển ⇒ vi phạm, bất kể đuôi.
Mỗi tệp trong miền PHẢI: nằm trực tiếp dưới ops/leases · YAML parse được · là mapping ·
lease_id là chuỗi khớp LEASE_ID (ASCII chữ/số/`.`/`_`/`-`) · lease_id == tên tệp bỏ đuôi · thay_the_cho đúng kiểu
(_danh_sach_thay_the_cho khác None), mỗi phần tử khớp LEASE_ID, không lặp · da_bi_thay_the vắng
khoá hoặc là chuỗi khớp LEASE_ID (có khoá mang null là sai) · lease_expires_at_utc đọc được bằng
_doc_han của cổng (ISO8601 có múi giờ) · lease_id không trùng. Vi phạm bất kỳ ⇒ rc=3 (KHÔNG ĐO ĐƯỢC), không ép kiểu, không bỏ qua.

Dùng:  python3 -B do_q6_hk.py <kho> <MOC> <CLOCK_UTC>      in JSON, rc 0 | 3
       python3 -B do_q6_hk.py --tu-kiem [<kho>]            dựng kho giả, kiểm các phản chứng, rc 0 | 1
                                                        (<kho> chứa ops/lease_publish.py; mặc định: gốc kho của script)
"""
import hashlib
import importlib.util
import json
import re
import subprocess
import sys
import tempfile
from datetime import datetime
from pathlib import Path

GOC_SCRIPT = Path(__file__).resolve()


def _nap_lp(goc: Path):
    spec = importlib.util.spec_from_file_location("lp_q6_hk", goc / "ops/lease_publish.py")
    lp = importlib.util.module_from_spec(spec)
    sys.modules["lp_q6_hk"] = lp
    spec.loader.exec_module(lp)
    return lp


def dan_xuat(goc: Path, moc: str, clock: str, lp) -> dict:
    import yaml

    def git(*a):
        return subprocess.run(["git", "-C", str(goc), *a], capture_output=True, text=True, check=True,
                              encoding="utf-8", errors="surrogateescape").stdout

    now = datetime.fromisoformat(clock.replace("Z", "+00:00"))
    L, vi_pham, ngoai_mien = {}, [], []
    for dong in git("ls-tree", "-r", "-z", moc, "--", "ops/leases").split("\0"):
        if not dong:
            continue
        meta, duong = dong.split("\t", 1)
        _, loai, oid = meta.split()
        if any(ord(c) < 0x20 or ord(c) == 0x7F for c in duong):
            vi_pham.append((duong, "ten-tep-co-ky-tu-dieu-khien"))
            continue
        # Byte không phải UTF-8 về đây dưới dạng surrogate (surrogateescape); không chốt thì
        # một byte lạ SAU đuôi `.yaml` làm tệp lọt ra ngoai_mien im lặng (lượt 8, mutant sống).
        if any(0xDC80 <= ord(c) <= 0xDCFF for c in duong):
            vi_pham.append((duong.encode("utf-8", "surrogateescape").decode("utf-8", "backslashreplace"),
                            "ten-tep-khong-phai-utf8"))
            continue
        if loai != "blob" or not duong.endswith((".yaml", ".yml")):
            ngoai_mien.append(duong)
            continue
        ten = duong[len("ops/leases/"):]
        if "/" in ten:
            vi_pham.append((duong, "thu-muc-con"))
            continue
        try:
            d = yaml.safe_load(git("cat-file", "-p", oid))
        except Exception as e:  # noqa: BLE001 — mọi lỗi parse đều là vi phạm
            vi_pham.append((duong, f"yaml-hong: {type(e).__name__}"))
            continue
        if not isinstance(d, dict):
            vi_pham.append((duong, f"khong-phai-mapping: {type(d).__name__}"))
            continue
        lid = d.get("lease_id")
        if not isinstance(lid, str) or not lp.LEASE_ID.fullmatch(lid):
            vi_pham.append((duong, "lease_id-sai-kieu-hoac-mien"))
            continue
        if lid != re.sub(r"\.ya?ml$", "", ten):
            vi_pham.append((duong, f"lease_id-khac-ten-tep: {lid!r}"))
            continue
        tt = lp._danh_sach_thay_the_cho(d.get("thay_the_cho"))
        if tt is None:
            vi_pham.append((duong, "thay_the_cho-sai-kieu"))
            continue
        # Mỗi chốt dưới đây phải là chốt DUY NHẤT cho ca của nó: gỡ chốt kiểu ở trên thì các chốt
        # sau vẫn không được chết TypeError (tín dụng giả), nên đọc `tt or []`, `isinstance(t, str)`.
        if any(not lp.LEASE_ID.fullmatch(x) for x in tt or []):
            vi_pham.append((duong, "thay_the_cho-ngoai-mien-LEASE_ID"))
            continue
        if len(tt or []) != len(set(tt or [])):
            vi_pham.append((duong, "thay_the_cho-lap-phan-tu"))
            continue
        t = d.get("da_bi_thay_the")
        if "da_bi_thay_the" in d and (not isinstance(t, str) or not t.strip()):
            vi_pham.append((duong, "da_bi_thay_the-sai-kieu"))
            continue
        if isinstance(t, str) and not lp.LEASE_ID.fullmatch(t):
            vi_pham.append((duong, "da_bi_thay_the-ngoai-mien-LEASE_ID"))
            continue
        try:
            han = lp._doc_han(d.get("lease_expires_at_utc"))
        except OverflowError:
            vi_pham.append((duong, "lease_expires_at_utc-hong: vuot-mien-UTC"))
            continue
        except lp.Chan as e:
            vi_pham.append((duong, f"lease_expires_at_utc-hong: {e.thong_diep[:80]}"))
            continue
        d = {**d, "_han_utc": han}
        if lid in L:
            vi_pham.append((duong, f"trung-lease_id-voi {L[lid][2]}"))
            continue
        L[lid] = (d, oid, duong)

    cap, mot_chieu = [], set()
    for lid, (d, oid, p) in L.items():
        # `or []` để chốt kiểu ở trên là chốt DUY NHẤT: gỡ nó thì ca thay-sai-kieu phải ra rc0 (HONG), không chết TypeError.
        for x in lp._danh_sach_thay_the_cho(d.get("thay_the_cho")) or []:
            c = L.get(x)
            if c and c[0].get("da_bi_thay_the") == lid:
                cap.append((x, lid, c[1], oid, c[2], p))
            else:
                mot_chieu.add((x, lid))
    for lid, (d, oid, p) in L.items():
        t = d.get("da_bi_thay_the")
        if t and not any(c[0] == lid and c[1] == t for c in cap):
            mot_chieu.add((lid, t))
    cap.sort()

    def trang_thai(moi):
        d = L[moi][0]
        if d["_han_utc"] <= now:
            return "HET_HAN"
        t = d.get("da_bi_thay_the")
        if not t:
            return "CON_HIEU_LUC"
        return "DA_BI_THAY" if any(c[0] == moi and c[1] == t for c in cap) else "KHONG_XAC_DINH"

    hang = [dict(cu=a, moi=b, blob_cu=ba, blob_moi=bb, path_cu=pa, path_moi=pb,
                 han_moi=str(L[b][0].get("lease_expires_at_utc")), trang_thai=trang_thai(b))
            for a, b, ba, bb, pa, pb in cap]
    rep = json.dumps(sorted([h["cu"], h["moi"], h["blob_cu"], h["blob_moi"]] for h in hang),
                     separators=(",", ":")).encode()
    kxd = [h for h in hang if h["trang_thai"] == "KHONG_XAC_DINH"]
    return {
        "moc": moc, "clock": clock,
        "mien_lease": len(L) + len(vi_pham), "lease_hop_le": len(L),
        "ngoai_mien": ngoai_mien, "vi_pham": vi_pham,
        "cap_hai_chieu": len(cap), "mot_chieu": sorted(mot_chieu),
        "digest_cap_hai_chieu_sha256": hashlib.sha256(rep).hexdigest(),
        "hang": hang, "KHONG_XAC_DINH": len(kxd),
        "BIA_MO_LICH_SU_theo_b": [[h["cu"], h["moi"], h["blob_cu"], h["blob_moi"]]
                                  for h in hang if h["trang_thai"] == "CON_HIEU_LUC"],
        "ma_thoat": 3 if (vi_pham or kxd) else 0,
    }


def _lease(lid, han, thay=None, bi=None):
    s = f"lease_id: {lid}\nlease_expires_at_utc: '{han}'\n"
    if thay:
        s += f"thay_the_cho: {thay}\n"
    if bi:
        s += f"da_bi_thay_the: {bi}\n"
    return s


def _kho_gia(tmp: Path, tep: dict) -> tuple[Path, str]:
    k = Path(tempfile.mkdtemp(dir=tmp))
    subprocess.run(["git", "init", "-q", str(k)], check=True)
    for ten, nd in tep.items():
        (k / "ops/leases" / ten).parent.mkdir(parents=True, exist_ok=True)
        (k / "ops/leases" / ten).write_text(nd, encoding="utf-8")
    subprocess.run(["git", "-C", str(k), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(k), "-c", "user.email=q6@local", "-c", "user.name=q6",
                    "commit", "-qm", "moc"], check=True)
    return k, subprocess.run(["git", "-C", str(k), "rev-parse", "HEAD"], capture_output=True,
                             text=True, check=True).stdout.strip()


def tu_kiem(goc: Path) -> int:
    lp = _nap_lp(goc)
    SONG, CHET, CLOCK = "2099-01-01T00:00:00Z", "2000-01-01T00:00:00Z", "2026-09-10T04:55:37Z"
    sach = {"x.yaml": _lease("x", CHET, bi="y"), "y.yaml": _lease("y", SONG, thay="x")}
    ca = {
        "sach": (sach, 0, [["x", "y"]]),
        "sai-ten": ({"khac.yaml": _lease("x", CHET, bi="y"), "y.yaml": _lease("y", SONG, thay="x")}, 3, []),
        "khong-phai-mapping": ({**sach, "bad.yaml": "- 1\n- 2\n"}, 3, [["x", "y"]]),
        "thieu-id": ({**sach, "bad.yaml": "lease_expires_at_utc: '2099-01-01T00:00:00Z'\n"}, 3, [["x", "y"]]),
        "id-sai-kieu": ({**sach, "bad.yaml": "lease_id: 7\n"}, 3, [["x", "y"]]),
        "yaml-hong": ({**sach, "bad.yaml": "lease_id: [\n"}, 3, [["x", "y"]]),
        "trung-id": ({**sach, "y.yml": _lease("y", SONG, thay="x")}, 3, [["x", "y"]]),
        "thay-sai-kieu": ({**sach, "z.yaml": _lease("z", SONG) + "thay_the_cho: 5\n"}, 3, [["x", "y"]]),
        "mot-chieu-moi": ({**sach, "y.yaml": _lease("y", SONG, thay="x", bi="w")}, 3, []),
        "da-bi-thay-tiep": ({"x.yaml": _lease("x", CHET, bi="y"), "y.yaml": _lease("y", SONG, thay="x", bi="z"),
                             "z.yaml": _lease("z", SONG, thay="y")}, 0, [["y", "z"]]),
        "het-han": ({"x.yaml": _lease("x", CHET, bi="y"), "y.yaml": _lease("y", CHET, thay="x")}, 0, []),
        "nhap-ngoai-mien": ({**sach, "q.yaml.nhap": "- khong doc\n"}, 0, [["x", "y"]]),
        "id-ngoai-mien-don": ({**sach, "a+b.yaml": _lease("a+b", SONG)}, 3, [["x", "y"]]),
        "id-ngoai-mien-cu": ({"x+y.yaml": _lease("x+y", CHET, bi="y"), "y.yaml": _lease("y", SONG, thay="x+y")}, 3, []),
        "id-ngoai-mien-moi": ({"x.yaml": _lease("x", CHET, bi="x+y"), "x+y.yaml": _lease("x+y", SONG, thay="x")}, 3, []),
        "bia-null-moi": ({**sach, "y.yaml": sach["y.yaml"] + "da_bi_thay_the: null\n"}, 3, []),
        "bia-null-ngoai-cap": ({**sach, "z.yaml": _lease("z", SONG) + "da_bi_thay_the: null\n"}, 3, [["x", "y"]]),
        "bia-khoa-khong-gia-tri": ({**sach, "y.yaml": sach["y.yaml"] + "da_bi_thay_the:\n"}, 3, []),
        "thay-phan-tu-ngoai-mien": ({**sach, "z.yaml": _lease("z", SONG) + "thay_the_cho: [\"a+b\"]\n"}, 3, [["x", "y"]]),
        "thay-phan-tu-lap": ({"x.yaml": _lease("x", CHET, bi="y"),
                              "y.yaml": _lease("y", SONG) + "thay_the_cho: [x, x]\n"}, 3, []),
        "bia-gia-tri-ngoai-mien": ({**sach, "z.yaml": _lease("z", SONG) + "da_bi_thay_the: \"a+b\"\n"}, 3, [["x", "y"]]),
        "han-sai-dinh-dang": ({**sach, "y.yaml": "lease_id: y\nlease_expires_at_utc: 'mai'\nthay_the_cho: x\n"}, 3, []),
        "han-thieu-mui-gio": ({**sach, "y.yaml": "lease_id: y\nlease_expires_at_utc: '2099-01-01T00:00:00'\nthay_the_cho: x\n"}, 3, []),
        "han-tran-UTC-tren": ({**sach, "y.yaml": _lease("y", "9999-12-31T23:59:59-01:00", thay="x")}, 3, []),
        "han-tran-UTC-duoi": ({**sach, "y.yaml": _lease("y", "0001-01-01T00:00:00+01:00", thay="x")}, 3, []),
        # Ba khoảng trống phủ reviewer lượt 4 chỉ ra (đột biến tự soạn SỐNG trên 24 ca cũ):
        "han-bang-dung-C": ({"x.yaml": _lease("x", CHET, bi="y"), "y.yaml": _lease("y", CLOCK, thay="x")}, 0, []),
        "thu-muc-con": ({**sach, "sub/z.yaml": _lease("z", SONG)}, 3, [["x", "y"]]),
        "han-vang": ({**sach, "z.yaml": "lease_id: z\n"}, 3, [["x", "y"]]),
        # Đối chứng DƯƠNG sát miền ngày (reviewer lượt 5): hạn hợp lệ năm 1 / năm 9999 KHÔNG được từ chối.
        # Hạn biên đặt ở ĐẦU MỚI của cặp (reviewer lượt 6: đặt ngoài cặp thì mutant "bỏ qua im lặng tệp biên"
        # sống), và đòi thêm số lease hợp lệ (phần tử thứ 4) để bắt cả việc bỏ qua ở biên dưới.
        "han-bien-tren-hop-le": ({"x.yaml": _lease("x", CHET, bi="y"),
                                  "y.yaml": _lease("y", "9999-12-31T23:59:59Z", thay="x")}, 0, [["x", "y"]], 2),
        "han-bien-duoi-hop-le": ({"x.yaml": _lease("x", CHET, bi="y"),
                                  "y.yaml": _lease("y", "0001-01-01T00:00:00Z", thay="x")}, 0, [], 2),
        # Hậu kiểm connector #652 (P2): tên có tab/xuống dòng không được lọt ra ngoai_mien im lặng.
        "ten-co-tab": ({**sach, "bad\tname.yaml": _lease("bad", SONG)}, 3, [["x", "y"]]),
        "ten-xuong-dong-sau-duoi": ({**sach, "z.yaml\n": _lease("z", SONG)}, 3, [["x", "y"]]),
        # Lượt 8: nhánh DEL và nhánh byte không-UTF-8 mỗi nhánh một ca riêng (ký tự đặt SAU đuôi
        # để chốt so tên không che được).
        "ten-DEL-sau-duoi": ({**sach, "z.yaml\x7f": _lease("z", SONG)}, 3, [["x", "y"]]),
        "ten-byte-sau-duoi": ({**sach, "z.yaml\udcff": _lease("z", SONG)}, 3, [["x", "y"]]),
    }
    hong = 0
    with tempfile.TemporaryDirectory() as t:
        for ten, (tep, rc_mong, giu_mong, *hop_le_mong) in ca.items():
            k, moc = _kho_gia(Path(t), tep)
            kq = dan_xuat(k, moc, CLOCK, lp)
            giu = [x[:2] for x in kq["BIA_MO_LICH_SU_theo_b"]]
            ok = (kq["ma_thoat"] == rc_mong and (rc_mong == 3 or giu == giu_mong)
                  and (not hop_le_mong or kq["lease_hop_le"] == hop_le_mong[0]))
            hong += not ok
            print(f"{'DAT ' if ok else 'HONG'} {ten}: rc={kq['ma_thoat']} (mong {rc_mong}) giu={giu} vi_pham={kq['vi_pham']}")
        # Cây sau thêm cặp mới: cây mốc không đổi kết quả (r9 Q6 "không lấy HEAD").
        k, moc = _kho_gia(Path(t), sach)
        (k / "ops/leases/p.yaml").write_text(_lease("p", CHET, bi="q"), encoding="utf-8")
        (k / "ops/leases/q.yaml").write_text(_lease("q", SONG, thay="p"), encoding="utf-8")
        subprocess.run(["git", "-C", str(k), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(k), "-c", "user.email=q6@local", "-c", "user.name=q6",
                        "commit", "-qm", "sau"], check=True)
        giu = [x[:2] for x in dan_xuat(k, moc, CLOCK, lp)["BIA_MO_LICH_SU_theo_b"]]
        ok = giu == [["x", "y"]]
        hong += not ok
        print(f"{'DAT ' if ok else 'HONG'} cay-sau-khong-doi-cay-moc: giu={giu}")
    print(f"TU_KIEM: {len(ca) + 1 - hong}/{len(ca) + 1} dat")
    return 1 if hong else 0


if __name__ == "__main__":
    if sys.argv[1:2] == ["--tu-kiem"]:
        sys.exit(tu_kiem(Path(sys.argv[2]).resolve() if len(sys.argv) > 2 else GOC_SCRIPT.parents[3]))
    goc = Path(sys.argv[1]).resolve()
    kq = dan_xuat(goc, sys.argv[2], sys.argv[3], _nap_lp(goc))
    print(json.dumps(kq, ensure_ascii=False, indent=1))
    sys.exit(kq["ma_thoat"])
