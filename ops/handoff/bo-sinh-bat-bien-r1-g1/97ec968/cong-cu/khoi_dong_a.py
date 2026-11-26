"""Chi phí KHỞI ĐỘNG một tiến trình con của bộ test đợt A (nạp + biên dịch tệp test với -B, không chạy ca nào nặng), base vs head xen kẽ.
Mỗi đột biến của bộ A sinh 1 tiến trình con (`chay_con`), nên chi phí khởi động nhân với ~160 lượt mỗi lần chạy bộ.
Dùng: python3 -B khoi_dong_a.py <clone nen> <clone sau> <so lan>
"""
import os
import resource
import subprocess
import sys
import time

nen, sau, n = sys.argv[1], sys.argv[2], int(sys.argv[3])


def mot(goc):
    r0 = resource.getrusage(resource.RUSAGE_CHILDREN)
    t = time.perf_counter()
    # ten ca khong ton tai => main in cach dung va thoat 2 ngay sau khi nap module: do dung chi phi nap + bien dich
    subprocess.run([sys.executable, "-B", os.path.join(goc, "ops/gate_output_doi_chieu_test.py"), "--mot-ca", "khong_co_ca_nay"],
                   capture_output=True, env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"))
    r1 = resource.getrusage(resource.RUSAGE_CHILDREN)
    return time.perf_counter() - t, (r1.ru_utime + r1.ru_stime) - (r0.ru_utime + r0.ru_stime)


kq = {"nen": [], "sau": []}
for _ in range(n):
    for ve, goc in (("nen", nen), ("sau", sau)):
        kq[ve].append(mot(goc))
for ve, xs in kq.items():
    w = sorted(x[0] for x in xs)
    c = sorted(x[1] for x in xs)
    print(f"{ve}: n={len(xs)} wall trung vi {w[len(w) // 2] * 1000:.1f} ms · cpu trung vi {c[len(c) // 2] * 1000:.1f} ms")
