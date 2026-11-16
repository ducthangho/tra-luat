#!/usr/bin/env python3
"""Runner B17 (đặc tả THU-HOI-ADMISSION-MERGE-BASE-B r13 §5 "Đầu vào của B17") — NGOÀI kho, không thuộc write set.

Dùng: python b17_runner.py <kho đo> <tệp lease_publish.py ứng viên> <thư mục output> N [N ...]
Kho đo: clone thường, không shallow, không grafts, không refs/replace; mọi lệnh Git chạy với GIT_NO_REPLACE_OBJECTS=1.
"""
import hashlib, importlib.util, json, os, platform, subprocess, sys, time
from pathlib import Path

S = "132d376cbbfea0692ff6db284753b33f437c637a"
GHIM = {10: ("8dc07047ffc00637c3ee9353b84c3c5abac189e9", "3253b5406a0bedacabdc294d9b2b5f7c44270e25", "7cfa8e36a888bdd3b385da7000e1fa875f4f8821"),
        50: ("ec1b18a2a007fc2e697249c727a2ca8391ab209e", "a6d6cbb26c80f8dbcbeab04e443d31926f24a28f", "13b707af2be2a961920a570b21a95f78153fca8d"),
        100: ("4397ee616273a97c1503e8359452aef4e78cd75a", "0157f8bcc37e71972cecc2efdd1746635f061792", "f47c13d701112fa42ed9be38cfb070aa1c4a56c1"),
        500: ("32a440cf3477f8953bef3dcd5ffe2c1803bf8a20", "8d3a6a6bbfe034bf486bf348838ac3854dea74d2", "1bf2d4a82dd25337281296cce21a9e4a98e1817a")}
BAT_BUOC = {"Linux": (10, 50, 100), "Windows": (10, 50)}
ENV = dict({k: v for k, v in os.environ.items() if not k.startswith("GIT_")}, GIT_NO_REPLACE_OBJECTS="1")


def g(kho, *a, inp=None, env=None):
    p = subprocess.run(["git", "-C", str(kho), *a], input=inp, capture_output=True, env=env or ENV)
    if p.returncode != 0:
        raise SystemExit(f"git {a} rc={p.returncode}: {p.stderr.decode(errors='replace')[:300]}")
    return p.stdout


def dung_H(kho, N):
    B = g(kho, "rev-parse", f"{S}~{N}").decode().strip()   # `~` = first-parent
    blob = g(kho, "hash-object", "-w", "--stdin", inp=f"amb-b17 N={N}\n".encode("ascii")).decode().strip()
    ls = g(kho, "ls-tree", "-z", B)
    tree = g(kho, "mktree", "-z", inp=ls + f"100644 blob {blob}\tamb-b17-{N}.txt\0".encode()).decode().strip()
    env = dict(ENV, GIT_AUTHOR_NAME="amb-b17", GIT_AUTHOR_EMAIL="amb-b17@example.invalid", GIT_AUTHOR_DATE="@1794042814 +0000",
               GIT_COMMITTER_NAME="amb-b17", GIT_COMMITTER_EMAIL="amb-b17@example.invalid", GIT_COMMITTER_DATE="@1794042814 +0000")
    H = subprocess.run(["git", "-c", "i18n.commitEncoding=UTF-8", "-C", str(kho), "commit-tree", tree, "-p", B, "-F", "-"],
                       input=f"amb-b17 N={N}\n".encode(), capture_output=True, env=env, check=True).stdout.decode().strip()
    return B, H, g(kho, "rev-parse", f"{H}^{{tree}}").decode().strip()


def doc_receipt(raw: bytes):
    """Như `kiem_json` của C1a1a: không BOM, UTF-8 strict, `json.loads` trên chuỗi; thêm: khoá trùng ⇒ lỗi; gốc là object."""
    if raw[:3] == b"\xef\xbb\xbf":
        return None, "BOM"
    def cap(ps):
        d = {}
        for k, v in ps:
            if k in d:
                raise ValueError(f"khoá trùng {k}")
            d[k] = v
        return d
    try:
        r = json.loads(raw.decode("utf-8", "strict"), object_pairs_hook=cap)
    except (UnicodeDecodeError, ValueError, RecursionError) as e:
        return None, f"{type(e).__name__}: {e}"
    return (r, None) if type(r) is dict else (None, "gốc không phải object")


def main():
    kho, ung_vien, ra, Ns = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3]).resolve(), [int(x) for x in sys.argv[4:]]
    ra.mkdir(parents=True, exist_ok=True)
    chan = {"shallow": g(kho, "rev-parse", "--is-shallow-repository").decode().strip(),
            "grafts": (kho / g(kho, "rev-parse", "--git-path", "info/grafts").decode().strip()).exists(),  # đường tương đối theo kho
            "replace": g(kho, "for-each-ref", "refs/replace").decode().strip()}
    if chan["shallow"] != "false" or chan["grafts"] or chan["replace"]:
        raise SystemExit(f"kho đo không hợp lệ: {chan}")
    nen = platform.system()
    sp = importlib.util.spec_from_file_location("lp_b17", ung_vien)
    mod = importlib.util.module_from_spec(sp); sp.loader.exec_module(mod)
    kq = {"runner_sha256": hashlib.sha256(Path(__file__).read_bytes()).hexdigest(), "nen": nen, "platform": platform.platform(),
          "python": sys.version.split()[0], "git": subprocess.run(["git", "--version"], capture_output=True, text=True).stdout.strip(),
          "nproc": os.cpu_count(), "ung_vien": str(ung_vien), "ung_vien_sha256": hashlib.sha256(ung_vien.read_bytes()).hexdigest(),
          "kho_do": chan, "S": S, "ket_qua": []}
    for N in Ns:
        B, H, T = dung_H(kho, N)
        mong = GHIM[N]
        muc = {"N": N, "B": B, "H": H, "T": T, "bat_buoc": N in BAT_BUOC.get(nen, ()), "oid_khop": (B, H, T) == mong}
        if not muc["oid_khop"]:
            muc.update(dat=False, ly_do=f"runner dựng sai: {(B, H, T)} != {mong}")
            kq["ket_qua"].append(muc); continue
        rcp = ra / f"receipt-N{N}.json"
        if rcp.exists():
            rcp.unlink()
        t0 = time.monotonic()
        p = subprocess.run([sys.executable, str(ung_vien), "kiem-thu-hoi-github", H, "--canonical-base", S, "--nhanh-mac-dinh", "master",
                            "--root", str(kho), "--receipt", str(rcp)], capture_output=True, text=True, env=ENV)
        giay = time.monotonic() - t0
        r, loi = doc_receipt(rcp.read_bytes()) if rcp.is_file() else (None, "không có receipt")
        dat = p.returncode == 0 and r is not None and r.get("quan_he_S_H") == "merge_base" and r.get("merge_bases") == [B]
        # số commit bước tô màu đọc: đo riêng, in-process, KhoObject mới (không dùng để quyết định đạt)
        kho_o = mod.KhoObject(kho); t1 = time.monotonic()
        try:
            tm = mod.to_mau_hai_phia(kho_o, S, H); so_commit, giay_tm = tm["so_commit_doc"], time.monotonic() - t1
        except Exception as e:  # noqa: BLE001
            so_commit, giay_tm = f"lỗi {type(e).__name__}: {e}", time.monotonic() - t1
        finally:
            kho_o.dong()
        muc.update(dat=dat, rc=p.returncode, giay=round(giay, 3), stderr=p.stderr,
                   dong_admission=[d for d in p.stdout.splitlines() if d.startswith("THU_HOI_ADMISSION")],
                   receipt=r, loi_doc_receipt=loi, so_object_da_doc=(r or {}).get("so_object_da_doc"), tong_bytes=(r or {}).get("tong_bytes"),
                   so_commit_to_mau=so_commit, giay_to_mau_rieng=round(giay_tm, 3))
        kq["ket_qua"].append(muc)
        print(f"N={N} bat_buoc={muc['bat_buoc']} dat={dat} rc={p.returncode} {giay:.1f}s object={muc['so_object_da_doc']} "
              f"to_mau={so_commit} {loi or ''}", flush=True)
    kq["dat_moi_N_bat_buoc"] = all(m["dat"] for m in kq["ket_qua"] if m["bat_buoc"]) and \
        {m["N"] for m in kq["ket_qua"] if m["bat_buoc"]} == set(BAT_BUOC.get(nen, ()))
    tep = ra / f"b17-{nen}.json"
    tep.write_text(json.dumps(kq, ensure_ascii=False, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"B17 {nen}: dat_moi_N_bat_buoc={kq['dat_moi_N_bat_buoc']} json={tep} sha256={hashlib.sha256(tep.read_bytes()).hexdigest()}")
    return 0 if kq["dat_moi_N_bat_buoc"] else 1


if __name__ == "__main__":
    sys.exit(main())
