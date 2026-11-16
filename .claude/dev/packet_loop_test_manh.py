#!/usr/bin/env python3
"""packet_loop_test_manh — bộ chạy BỌC NGOÀI `packet_loop_test.py` (#1343 CI-PACKET-LOOP-NHANH r1).

Không sửa, không chép tệp gốc: nạp nó làm mô-đun rồi gọi ĐÚNG `main()` của nó, chỉ bọc ba cửa trong lúc `main()` chạy:
  · `chay_suite`    — lượt NỀN (lời gọi đầu, từ `_legacy_main`) chỉ chạy ca của mảnh; xong thì đặt `MUTANTS` = `_Pha` để chọn
                      pha đột biến. Lời gọi LỒNG của chính các ca (trong lượt nền) và lượt đột biến đi thẳng xuống bản gốc.
  · `_required1174` — lời gọi của `_legacy_main` chấm trên PHẦN ca bắt buộc nằm trong mảnh (M6); lời gọi khác giữ nguyên.
  · `_carrier1174`  — carrier Linux cần đủ kết quả `wp1174_*` trong MỘT tiến trình ⇒ `chia` dồn cả nhóm về mảnh 0; mảnh khác
                      IN RA rằng nó không chạy carrier, và `gom` đòi ĐÚNG MỘT mảnh đã chạy (không im lặng tắt).
Chốt `missing` của `main()` vẫn tính trên TOÀN BỘ `CASES`: bộ bọc không đụng `CASES`.

dùng:  (không cờ, không biến)      như chạy tệp gốc: đủ ca + đủ bảng đột biến
       --manh i/N [--ra TEP]       mảnh ca i của N, KHÔNG đột biến; ghi bản ghi JSON cho job gom
       --dot-bien j/M              mảnh đột biến j của M, nền RỖNG (job không bắt buộc)
       (CI đặt ba cờ trên qua biến PACKET_LOOP_MANH / PACKET_LOOP_RA / PACKET_LOOP_DOT_BIEN; cờ dòng lệnh thắng biến)
       --gom THU_MUC --n N         job gom: so TẬP ca từng mảnh với phân hoạch tự dựng lại (env PACKET_LOOP, KQ_MANH)
Giới hạn: `_Pha` dựa vào việc `_legacy_main` gọi `MUTANTS.items()` lần ĐẦU ở vòng đột biến; tệp gốc đổi thứ tự thì chốt
AC 18 nhận tập con và ĐỎ (ồn ào), không xanh lặng. Thời lượng dùng để chia mảnh: xem `chia`.
"""
from __future__ import annotations

import json
import os
import sys
import time
from pathlib import Path

HERE = Path(__file__).resolve().parent
N_TOI_DA, NHOM_CARRIER = 16, "wp1174_"


def nap(thu_muc=HERE):
    sys.path.insert(0, str(thu_muc))
    import packet_loop_test
    return packet_loop_test


class _Dung(Exception):
    pass


def ca_dang_ky(T):
    """Tên ca mà `main()` GỐC sẽ chạy trên nền này (đã qua bộ lọc nền của chính nó), theo thứ tự đăng ký."""
    goc = T.chay_suite

    def chi_ghi(script, tmp, chi_chay=None):
        raise _Dung([ten for ten, _ in T.CASES])
    T.chay_suite = chi_ghi
    try:
        T.main()
    except _Dung as ex:
        return list(dict.fromkeys(ex.args[0]))
    finally:
        T.chay_suite = goc
    raise SystemExit("KHÔNG ĐO ĐƯỢC: main() gốc không gọi chay_suite")


def chia(ten, n):
    """@@CHIA@@"""
    if type(n) is not int or not 1 <= n <= N_TOI_DA:
        raise ValueError(f"N={n!r} ngoài 1..{N_TOI_DA}")
    manh = [[] for _ in range(n)]
    con = [t for t in ten if n == 1 or not t.startswith(NHOM_CARRIER)]
    manh[0] = [t for t in ten if t not in set(con)]
    for k, t in enumerate(con):
        manh[k % (n - 1) + 1 if n > 1 else 0].append(t)
    return manh


class _Pha(dict):
    """`items()` lần ĐẦU (vòng đột biến của `_legacy_main`) chỉ trả phần ĐƯỢC CHỌN; các lần sau (chốt AC 18) trả đủ."""

    def __init__(self, goc, chon):
        super().__init__(goc)
        self.chon, self.lan = chon, 0

    def items(self):
        self.lan += 1
        return [(k, v) for k, v in super().items() if k in self.chon] if self.lan == 1 else super().items()


def chay(T, manh, chon_dot_bien=None):
    """`T.main()` với lượt nền = `manh` (tên ca) và pha đột biến = `chon_dot_bien(tên các đột biến) -> tập chạy` (None =
    không đột biến). Trả (rc, tên ca ĐÃ chạy, carrier đã chạy?, số lượt chạy đột biến)."""
    goc = T.chay_suite, T._required1174, T._carrier1174
    manh, da_chay, co_carrier, pha, dem = set(manh), [], [], [], [0, 0]   # dem = [trạng thái 0 trước/1 trong/2 sau nền, lượt đb]
    can = T.WP1174_REQUIRED - {"wp1174_windows_claim_rejected"}

    def suite(script, tmp, chi_chay=None):
        if dem[0] or chi_chay is not None:               # ca gọi lồng, hoặc lượt đột biến: bản gốc nguyên vẹn
            dem[1] += dem[0] == 2
            return goc[0](script, tmp, chi_chay)
        dem[0] = 1
        ket = goc[0](script, tmp, manh or {""})          # tập rỗng là "chạy hết" ở bản gốc ⇒ lính canh không khớp ca nào
        da_chay.extend(ket)
        pha.append(_Pha(T.MUTANTS, chon_dot_bien(list(T.MUTANTS)) if chon_dot_bien else set()))
        T.MUTANTS, dem[0] = pha[0], 2
        return ket

    def required(outcomes, yeu_cau):
        cua_main = dem[0] == 2 and yeu_cau is T.__dict__.get("_WP1174_MAIN_REQUIRED")
        return goc[1](outcomes, yeu_cau & manh if cua_main else yeu_cau)

    def carrier(outcomes, gate_rc=0):
        if dem[0] != 2 or can <= manh:                   # trong lượt nền = ca tự gọi carrier: không phải carrier của main
            co_carrier.append(dem[0] == 2)
            return goc[2](outcomes, gate_rc)
        if can & manh:
            print(f"WP1174 carrier: nhóm ca bắt buộc bị XẺ giữa các mảnh ({len(can & manh)}/{len(can)}) - ĐỎ")
            return False
        print("WP1174 carrier: KHÔNG chạy ở mảnh này (cả nhóm wp1174_* nằm ở mảnh 0; job gom đòi đúng một mảnh đã chạy)")
        return True
    T.chay_suite, T._required1174, T._carrier1174 = suite, required, carrier
    try:
        rc = T.main()
    finally:
        T.chay_suite, T._required1174, T._carrier1174 = goc
    if not pha or pha[0].lan < 2 or (pha[0].chon and not dem[1]):
        print("ĐỎ: main() gốc không đi qua lượt nền, vòng đột biến đã chọn và chốt AC 18 như bộ bọc giả định")
        rc = 1
    return rc, da_chay, any(co_carrier), dem[1]


def gom(ten, n, ban_ghi, can_carrier=True):
    """Lỗi của job gom ([] = đạt). `ban_ghi`: {chỉ số mảnh: bản ghi}. Không tin `rc` của mảnh: so TẬP ca từng mảnh với phân
    hoạch dựng lại từ `ten`; thiếu mảnh, mảnh đỏ, ca thiếu/thừa/trùng, hay số mảnh chạy carrier khác 1 đều là lỗi."""
    loi, mong = [], chia(ten, n)
    for i in range(n):
        b = ban_ghi.get(i)
        if type(b) is not dict or (b.get("manh"), b.get("n")) != (i, n):
            loi.append(f"thiếu hoặc sai bản ghi mảnh {i}/{n}")
            continue
        if b.get("rc") != 0:
            loi.append(f"mảnh {i}/{n} đỏ: rc={b.get('rc')!r}")
        ca = b.get("ca") if type(b.get("ca")) is list else []
        if sorted(map(str, ca)) != sorted(mong[i]):
            loi.append(f"mảnh {i}/{n} lệch tập ca ({len(ca)}/{len(mong[i])}): thiếu {sorted(set(mong[i]) - set(map(str, ca)))[:5]}"
                       f" · thừa {sorted(set(map(str, ca)) - set(mong[i]))[:5]}")
    loi += [f"bản ghi mảnh lạ: {k!r}" for k in ban_ghi if k not in range(n)]
    so = sum(type(b) is dict and b.get("carrier") is True for b in ban_ghi.values())
    return loi + ([f"carrier WP1174 phải chạy ở ĐÚNG MỘT mảnh, đo được {so}"] if can_carrier and so != 1 else [])


def lenh_gom(T, thu_muc, n, env=os.environ):
    """`PACKET_LOOP` = output của `chuan-bi` (chỉ ĐÚNG chuỗi `bo_qua` mới tha), `KQ_MANH` = `needs.<job mảnh>.result`."""
    quyet, kq = env.get("PACKET_LOOP") or "", env.get("KQ_MANH") or ""
    if quyet == "bo_qua":
        print(f"GOM: {'KHÔNG ĐO' if kq == 'skipped' else 'ĐỎ'} - packet_loop=bo_qua (diff không chạm tập phụ thuộc của bộ ca, hoặc "
              f"push nhánh mặc định; lý do ở bước phân loại của job chuan-bi) · job mảnh: {kq!r} (phải là 'skipped')")
        return int(kq != "skipped")
    ban_ghi = {}
    for tep in sorted(Path(thu_muc).glob("manh-*.json")):
        try:
            b = json.loads(tep.read_text(encoding="utf-8"))
            ban_ghi[b["manh"] if type(b["manh"]) is int and b["manh"] not in ban_ghi else tep.name] = b
        except (OSError, ValueError, TypeError, KeyError) as ex:
            ban_ghi[tep.name] = type(ex).__name__
    ten = ca_dang_ky(T)
    loi = gom(ten, n, ban_ghi, can_carrier=sys.platform.startswith("linux"))
    loi += [f"job mảnh có kết quả {kq!r} trong lúc packet_loop={quyet!r} (phải là 'success')"] if kq != "success" else []
    print("\n".join(f"GOM: ĐỎ - {x}" for x in loi) or "GOM: mọi mảnh khớp phân hoạch")
    print(f"GOM: {'ĐẠT' if not loi else str(len(loi)) + ' lỗi'} · {n} mảnh · {len(ten)} ca đăng ký")
    return int(bool(loi))


def _phan_so(chuoi, tran):
    i, _, n = chuoi.partition("/")
    if not (i.isdecimal() and n.isdecimal() and 1 <= int(n) <= tran and int(i) < int(n)):
        raise SystemExit(f"KHÔNG ĐO ĐƯỢC: {chuoi!r} không phải i/N với 0 <= i < N <= {tran}")
    return int(i), int(n)


def main(argv=None):
    argv = sys.argv[1:] if argv is None else list(argv)
    bien = (("--manh", "PACKET_LOOP_MANH"), ("--ra", "PACKET_LOOP_RA"), ("--dot-bien", "PACKET_LOOP_DOT_BIEN"))
    co = {**{c: os.environ[b] for c, b in bien if os.environ.get(b)}, **dict(zip(argv[::2], argv[1::2]))}
    if len(argv) % 2 or set(co) - {"--manh", "--ra", "--dot-bien", "--gom", "--n"}:
        raise SystemExit(__doc__)
    T = nap()
    if "--gom" in co:
        return lenh_gom(T, co["--gom"], _phan_so("0/" + co.get("--n", ""), N_TOI_DA)[1])
    if "--manh" not in co and "--dot-bien" not in co:
        return T.main()
    i, n = _phan_so(co["--manh"], N_TOI_DA) if "--manh" in co else (None, None)
    j, m = _phan_so(co.get("--dot-bien", "0/1"), 64)
    bat_dau = time.monotonic()
    rc, da_chay, carrier, luot = chay(T, [] if n is None else chia(ca_dang_ky(T), n)[i],
                                      (lambda ten: {t for k, t in enumerate(ten) if k % m == j}) if "--dot-bien" in co else None)
    print(f"MẢNH: ca {co.get('--manh', '-')} · đột biến {co.get('--dot-bien', '-')} · {len(da_chay)} ca · {luot} lượt đột biến · "
          f"carrier={'có' if carrier else 'không'} · {time.monotonic() - bat_dau:.0f}s · rc={rc}")
    if "--ra" in co:
        Path(co["--ra"]).parent.mkdir(parents=True, exist_ok=True)
        Path(co["--ra"]).write_text(json.dumps({"manh": i, "n": n, "ca": da_chay, "rc": rc, "carrier": carrier}), encoding="utf-8")
    return rc


if __name__ == "__main__":
    sys.exit(main())
