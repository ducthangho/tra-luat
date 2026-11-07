"""Kho đầu vào SINH TỔ HỢP cho K7-S (ops/specs/wp1236-r8.md, ca A14-S6).
Vòng 2 r8 (reviewer Claude I01) đòi kho sinh; vòng 3 (reviewer Codex J01, J02) chỉ ra hai lỗ của bản đầu: (1) ký tự chỉ chèn trên một mẫu
`python`, ống chỉ hai thành phần; (2) harness ĐỔI tên tệp trước khi chạy, tức đổi chính cú pháp đang đo, và gộp "chưa chạy" vào "nuốt lỗi".
Bản này:
  (i)  LENH_MAU: một mẫu cho MỖI nhánh DANG (python, bash, pwsh), có đối số W;
  (ii) ghép A op B và A | B | C (thành phần GIỮA có thể là lệnh hợp lệ hay ngoài tập) với mọi toán tử;
  (iii) mỗi ký tự KT chèn vào MỌI vị trí của MỖI mẫu, và thay MỌI dấu cách của nó; thêm vào thành phần ĐẦU/GIỮA/CUỐI của ống ba thành phần;
  (iv) harness chạy NGUYÊN BYTE thân (tự kiểm: tệp s.sh == thân), đặt chương trình ở ĐÚNG đường dẫn token, và phân loại từng lần chạy thành
       truyen_loi | nuot_loi (rc 0, chương trình hỏng đã chạy) | khong_chay (chương trình hỏng không chạy).
Đòi: (a) vị từ được đo == gram.py trên MỌI đầu vào; (b) mọi thân gram.py NHẬN: với mỗi thành phần k (đường dẫn riêng), k hỏng còn lại chép
stdin ⇒ truyen_loi; và khi mọi thành phần trùng đường dẫn thì cho tất cả hỏng ⇒ truyen_loi.
Chạy: python3 -I ops/reviews/wp1236-r8-soan/sinh_r8.py"""
import json, os, pathlib, re, subprocess, sys, tempfile
D = os.path.dirname(os.path.abspath(__file__)); sys.path.insert(0, D)
import gram

SHELL_LENH = {None: ["/usr/bin/bash", "-e"], "bash": ["/usr/bin/bash", "--noprofile", "--norc", "-eo", "pipefail"], "sh": ["/bin/sh", "-e"]}
HONG = "import pathlib, sys; pathlib.Path('DA_CHAY').touch(); sys.exit(1)\n"
QUA = "import sys; sys.stdout.write(sys.stdin.read())\n"
HONG_SH, QUA_SH = "touch DA_CHAY; exit 1\n", "cat\n"
LENH_MAU = ["python ops/a.py w", "bash ops/b.sh w", "pwsh -NoProfile -File ops/c.ps1 w"]
LENH = ["python ops/x.py", "python ops/y.py --json a=b", "bash ops/z.sh", "pwsh -NoProfile -File ops/v.ps1"]
NGOAI = ["true", "cat", ":", "exit 0"]
SHELL = [None, "bash", "sh"]
OP2 = ["||", "&&", ";", "&", "|", "|&", "\n", ";;", "&;", "||&", "| |"]
TIEN = ["!", "! ", "time ", "exec ", "command ", "builtin ", "eval ", "coproc ", "{ ", "( ", "A=1 ", "-", "--", "./", "/", "~"]
HAU = [" &", "&", " ;", ";", " ||", " |", " #", "#", " \\", "\\", ")", " }", " 2>&1", " >x", " <x", "\n", "\r", " ", "  "]
TOK = ["-n", "-s", "-h", "-c", "-x", "-i", "-m", "--", "-", "!", "||", "&&", ";", "&", "|", "|&", "time", "exec", "true", "{", "}", "(", ")",
       "2>&1", ">x", "<x", "#", "-NoProfile", "-File", "-Command"]
KT = ";&|!(){}$`'\"\\<>#*?[]~+,@%^= \t\n\r\x00 ο١"   # 35 ký tự


def chen(mau):
    out = []
    for c in KT:
        for i in range(len(mau) + 1):
            out.append(mau[:i] + c + mau[i:])
        out.append(mau.replace(" ", c))
    return out


def kho():
    out = []
    for a in LENH:
        for b in LENH:
            for op in OP2:
                for sep in (f" {op} ", op, f"{op} ", f" {op}"):
                    out.append(a + sep + b)
        for t in TIEN:
            out.append(t + a)
        for h in HAU:
            out.append(a + h)
    for a in LENH:   # ống ba thành phần: giữa hợp lệ / ngoài tập; và toán tử khác ở vế sau
        for b in LENH + NGOAI:
            for c in LENH:
                out.append(f"{a} | {b} | {c}")
                for op in OP2:
                    out.append(f"{a} | {b} {op} {c}")
    for a in LENH:   # toán tử ở ranh giới thứ nhất của ống ba thành phần (Claude J01 vòng 3: `X || Y | Z`, `X | Y || Y`)
        for c in LENH:
            for op in OP2:
                out.append(f"{a} {op} {c} | {LENH[0]}")
    hat = LENH + [f"{a} | {b}" for a in LENH for b in LENH] + [f"{LENH[0]} | {b} | {LENH[2]}" for b in LENH]
    for h in hat:   # (v) chèn TOKEN ở MỌI ranh giới dấu cách của mọi hạt (tuỳ chọn giữa tên chương trình và P, toán tử, từ khoá)
        vt = [i for i, ch in enumerate(h) if ch == " "] + [len(h)]
        for i in vt:
            for t in TOK:
                out.append(h[:i] + " " + t + h[i:])
    for mau in LENH_MAU:   # (iii) ký tự ở mọi vị trí của mỗi nhánh DANG
        out += chen(mau)
    x, y, z = "python ops/x.py", "bash ops/z.sh", "pwsh -NoProfile -File ops/v.ps1"
    for i, m in enumerate(chen("python ops/m.py w")):   # và ở thành phần đầu / giữa / cuối của ống ba thành phần
        out += [f"{m} | {y} | {z}", f"{x} | {m} | {z}", f"{x} | {y} | {m}"] if i % 3 == 0 else []
    return sorted(set(out))


def chay_nguyen_byte(run, sh, hong):
    """Chạy ĐÚNG byte `run`; chương trình ở đúng đường dẫn token; `hong` = tập đường dẫn cho thoát 1. Trả phân loại."""
    with tempfile.TemporaryDirectory() as d:
        p = pathlib.Path(d); (p / "bin").mkdir()
        os.symlink(sys.executable, p / "bin/python")
        # `bash P.sh` chạy /usr/bin/bash THẬT (Claude J02 vòng 3); `pwsh` GIẢ CHẶT: chỉ nhận đúng `-NoProfile -File <tệp> [đối số]`,
        # lệch dạng ⇒ thoát 99 KHÔNG chạy tệp (container không có pwsh)
        (p / "bin" / "pwsh").write_text(f"#!/bin/sh\n[ \"$1\" = -NoProfile ] && [ \"$2\" = -File ] && [ -n \"$3\" ] || exit 99\n"
                                       f"shift 2; exec {sys.executable} \"$@\"\n")
        (p / "bin" / "pwsh").chmod(0o755)
        for t in set(re.findall(r"[^\s|&;()<>]+\.(?:py|sh|ps1)", run)):
            f = p / t
            try:
                f.parent.mkdir(parents=True, exist_ok=True)
                f.write_text((HONG_SH if t in hong else QUA_SH) if t.endswith(".sh") else (HONG if t in hong else QUA))
            except (OSError, ValueError):
                pass
        (p / "s.sh").write_bytes(run.encode("utf-8", "surrogatepass"))
        assert (p / "s.sh").read_bytes() == run.encode("utf-8", "surrogatepass")   # tự kiểm: thân thực thi == thân gốc
        rc = subprocess.run(SHELL_LENH[sh] + [str(p / "s.sh")], cwd=d, env={"PATH": f"{p}/bin:/usr/bin:/bin", "HOME": d},
                            capture_output=True, stdin=subprocess.DEVNULL, timeout=20).returncode
        da = (p / "DA_CHAY").exists()
        return "truyen_loi" if rc != 0 and da else ("nuot_loi" if da else "khong_chay"), rc


def do_than(run, sh):
    tok = re.findall(r"[^\s|&;()<>]+\.(?:py|sh|ps1)", run)
    phep = [{t} for t in dict.fromkeys(tok)] + ([set(tok)] if len(set(tok)) < len(tok) else [])
    return [(sorted(h),) + chay_nguyen_byte(run, sh, h) for h in phep or [set()]]


def main(vi_tu=None):
    """vi_tu = None: đo THAM CHIẾU (chạy Bash trên mọi thân được nhận). vi_tu khác: đo ĐỘT BIẾN — (a) đếm lệch trên mọi đầu vào; (b) chỉ
    chạy Bash trên thân đột biến NHẬN mà tham chiếu từ chối (thân tham chiếu nhận đã đo ở lượt tham chiếu)."""
    dot_bien = vi_tu is not None
    vi_tu = vi_tu or gram.cu_phap_run
    lech, nhan, xau, n = [], 0, [], 0
    for than in kho():
        for sh in SHELL:
            for run in (than, than + "\n"):
                n += 1
                a, b = vi_tu(run, sh), gram.cu_phap_run(run, sh)
                if a != b:
                    lech.append((run, sh, a, b))
                if a is None and (not dot_bien or b is not None):
                    nhan += 1
                    for h, loai, rc in do_than(run, sh):
                        if loai != "truyen_loi":
                            xau.append((run, sh, h, loai, rc))
    kq = {"dau_vao": n, "nhan": nhan, "lech_tham_chieu": len(lech),
          "nuot_loi": sum(x[3] == "nuot_loi" for x in xau), "khong_chay": sum(x[3] == "khong_chay" for x in xau)}
    print(json.dumps(kq, ensure_ascii=False))
    return kq, lech, xau


if __name__ == "__main__":
    kq, lech, xau = main()
    json.dump({"kq": kq, "ky_tu": len(KT), "xau": xau[:50]}, open(os.path.join(D, "sinh_r8.json"), "w"), ensure_ascii=False, indent=1)
    sys.exit(1 if lech or xau else 0)
