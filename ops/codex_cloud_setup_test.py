#!/usr/bin/env python3
"""Bộ test tự đứng cho `ops/codex_cloud_setup.sh` (setup script môi trường Codex Cloud).

Gọi `cai_deb` qua `source` với apt-get/apt-cache/dpkg/dpkg-deb/id/sudo GIẢ đặt đầu PATH. Đồ giả GIỮ TRẠNG THÁI
(`dpkg -s` đọc danh sách gói đã cài, `apt-get download` tạo tệp .deb thật, `dpkg-deb -x` dựng cây thật) và
mọi lời gọi được ghi nhật ký — ca đo THAO TÁC xảy ra, không chỉ mã thoát. Ca `ca_dot_bien` tự đột biến bản sao
tạm của script và đòi ca đích ĐỎ bằng `ChotCa` (lớp riêng: lỗi vô can không được tính là giết).
In ĐÚNG MỘT dòng chỉ gồm `đạt/tổng` (đơn vị: ca test); ca đỏ in `DO <ca>: …`; ca không đo được trên nền này
(Windows: đồ giả là script POSIX) in `BO QUA <ca>: …`, bị trừ khỏi tổng. Chạy: python -B ops/codex_cloud_setup_test.py
"""
import os
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import bash_nen  # noqa: E402 — MỘT bộ giải `bash` dùng chung (#570); `bash` trần trên Windows có thể là WSL

for _s in (sys.stdout, sys.stderr):
    if hasattr(_s, "reconfigure"):
        _s.reconfigure(encoding="utf-8", errors="backslashreplace")

SCRIPT = Path(__file__).resolve().parent / "codex_cloud_setup.sh"
SCRIPT_DANG_DUNG = SCRIPT  # ca_dot_bien trỏ biến này sang bản sao đã đột biến

GIA = {
    "id": 'case "$1" in -u) echo "${FAKE_UID:-1000}";; -un) echo thu;; *) echo uid=1000;; esac\n',
    "sudo": 'echo "sudo $*" >> "$FAKE_LOG"\n[ "${FAKE_SUDO_OK:-0}" = 1 ] || exit 1\n'
            '[ "$1" = -n ] && [ "$2" = true ] && exit 0\nexec "$@"\n',
    "apt-get": 'echo "apt-get $*" >> "$FAKE_LOG"\ncase " $* " in *" download "*)\n'
               '  for p; do :; done; printf %s "$p" > "${p}_1_amd64.deb";; esac\n',
    "apt-cache": 'printf "%s\\n" "$FAKE_DEPS"\n',
    "dpkg": '[ "$1" = -s ] || exit 2\nfor g in $FAKE_INSTALLED; do [ "$g" = "$2" ] && exit 0; done\nexit 1\n',
    "dpkg-deb": '[ "$1" = -x ] || exit 2\ng="$(cat "$2")"\n'
                'if [ "$g" = "$FAKE_MAIN" ]; then mkdir -p "$3/usr/bin"\n'
                '  printf \'#!/bin/sh\\necho "LD=$LD_LIBRARY_PATH"\\n\' > "$3/usr/bin/$FAKE_CMD"; chmod +x "$3/usr/bin/$FAKE_CMD"\n'
                'else mkdir -p "$3/usr/lib/x86_64-linux-gnu"; : > "$3/usr/lib/x86_64-linux-gnu/lib$g.so"; fi\n',
    "python3": 'echo "python3 $*" >> "$FAKE_LOG"\n',
}
DEPS = "goi-a\n  Depends: libb\nlibb\n  Depends: libc6\nlibc6\n<ao-ao>"


class ChotCa(AssertionError):
    """Tín hiệu của CHÍNH assertion trong ca — mã triển khai không giả được (CLAUDE.md, bài học đột biến)."""


class BoQua(Exception):
    pass


def bang(dk, tb):
    if not dk:
        raise ChotCa(tb)


def _posix():
    if os.name == "nt":
        raise BoQua("đồ giả là script POSIX; script đích chỉ chạy trên Linux (Codex Cloud)")


def _bash():
    duong, chan_doan = bash_nen.tim_bash()
    if not duong:
        raise BoQua("không `bash` nào làm được việc: " + "; ".join(f"{c['duong']}: {c['ly_do']}" for c in chan_doan))
    return duong


def _san(them_lenh=False):
    """Thư mục tạm: bin giả + HOME. Trả (gốc, env)."""
    goc = Path(tempfile.mkdtemp(prefix="codex-cloud-setup-"))
    gia = goc / "gia"
    gia.mkdir()
    for ten, than in GIA.items():
        p = gia / ten
        p.write_text("#!/bin/sh\n" + than, encoding="utf-8", newline="\n")
        p.chmod(0o755)
    if them_lenh:
        p = gia / "mycmd"
        p.write_text("#!/bin/sh\necho co-san\n", encoding="utf-8", newline="\n")
        p.chmod(0o755)
    (goc / "home").mkdir()
    env = {"PATH": f"{gia}:/usr/bin:/bin", "HOME": str(goc / "home"), "FAKE_LOG": str(goc / "log"),
           "FAKE_DEPS": DEPS, "FAKE_INSTALLED": "libc6", "FAKE_MAIN": "goi-a", "FAKE_CMD": "mycmd", "LANG": "C"}
    (goc / "log").write_text("", encoding="utf-8")
    return goc, env


def _cai_deb(env, **them):
    env = {**env, **them}
    return subprocess.run([_bash(), "-c", 'source "$1"; cai_deb goi-a mycmd', "_", str(SCRIPT_DANG_DUNG)],
                          capture_output=True, text=True, env=env, timeout=60)


def _log(goc):
    return (goc / "log").read_text(encoding="utf-8").splitlines()


def ca_tep_lf_khong_crlf():
    """Checkout Windows (autocrlf) mà mang CRLF thì bash chết `$'\\r': command not found` trên Codex Cloud."""
    bang(b"\r" not in SCRIPT_DANG_DUNG.read_bytes(), "script có CR — bash trên Linux sẽ hỏng")


def ca_khong_nang_cap_pip():
    """Đo 27-10-2026: `pip install --upgrade pip` CHẾT trên Python của distro ("installed by debian")."""
    lenh = [d for d in SCRIPT_DANG_DUNG.read_text(encoding="utf-8").splitlines() if not d.lstrip().startswith("#")]
    bang(not any("--upgrade pip" in d for d in lenh), "script lại nâng cấp pip")


def ca_cu_phap_bash():
    _posix()
    p = subprocess.run([_bash(), "-n", str(SCRIPT_DANG_DUNG)], capture_output=True, text=True, timeout=60)
    bang(p.returncode == 0, f"bash -n rc={p.returncode}: {p.stderr}")


def ca_source_khong_chay_main():
    _posix()
    goc, env = _san()
    p = subprocess.run([_bash(), "-c", 'source "$1"; echo DA_SOURCE', "_", str(SCRIPT_DANG_DUNG)],
                       capture_output=True, text=True, env=env, timeout=60)
    bang(p.returncode == 0 and "DA_SOURCE" in p.stdout, f"source hỏng: rc={p.returncode} {p.stderr}")
    bang(_log(goc) == [], f"source mà main vẫn chạy: {_log(goc)}")
    bang(not (goc / "home/.local").exists(), "source mà vẫn tạo ~/.local")


def ca_co_san_khong_goi_apt():
    _posix()
    goc, env = _san(them_lenh=True)
    p = _cai_deb(env)
    bang(p.returncode == 0, f"rc={p.returncode} {p.stderr}")
    bang(_log(goc) == [], f"lệnh có sẵn mà vẫn gọi trình cài: {_log(goc)}")


def ca_khong_root_tai_deb_bo_goi_da_cai():
    """Codex Cloud: không root, không sudo ⇒ tải .deb của gói CHƯA cài, giải nén, wrapper đặt LD_LIBRARY_PATH."""
    _posix()
    goc, env = _san()
    p = _cai_deb(env)
    bang(p.returncode == 0, f"rc={p.returncode} {p.stderr}")
    log = _log(goc)
    tai = sorted(d.split()[-1] for d in log if d.startswith("apt-get ") and " download " in d)
    bang(tai == ["goi-a", "libb"], f"tải sai tập gói (libc6 đã cài, <ao-ao> là gói ảo): {tai}")
    bang(not any(" install " in d for d in log), f"không root mà vẫn apt-get install: {log}")
    bang(not any(d.startswith("sudo apt-get") for d in log), f"sudo hỏng mà vẫn dùng sudo apt-get: {log}")
    w = goc / "home/.local/bin/mycmd"
    bang(w.is_file(), "không tạo wrapper ở ~/.local/bin")
    r = subprocess.run([str(w)], capture_output=True, text=True, env=env, timeout=60)
    lib = str(goc / "home/.local/tra-luat-goc/usr/lib/x86_64-linux-gnu")
    bang(r.returncode == 0 and lib in r.stdout, f"wrapper không đưa thư mục lib vào LD_LIBRARY_PATH: {r.stdout!r}")


def ca_root_dung_apt_get_install():
    _posix()
    goc, env = _san()
    p = _cai_deb(env, FAKE_UID="0")
    log = _log(goc)
    bang(p.returncode == 0, f"rc={p.returncode} {p.stderr}")
    bang("apt-get install -y -qq goi-a" in log, f"root mà không apt-get install: {log}")
    bang(not any(" download " in d for d in log), f"root mà vẫn đi đường tải .deb: {log}")


def ca_sudo_khong_mat_khau_dung_sudo():
    _posix()
    goc, env = _san()
    p = _cai_deb(env, FAKE_SUDO_OK="1")
    log = _log(goc)
    bang(p.returncode == 0, f"rc={p.returncode} {p.stderr}")
    bang("sudo apt-get install -y -qq goi-a" in log, f"có sudo mà không dùng: {log}")
    bang(not any(" download " in d for d in log), f"có sudo mà vẫn đi đường tải .deb: {log}")


def ca_bashrc_localappdata_ngoai_home():
    """Codex Cloud gắn $HOME CHỈ ĐỌC lúc agent chạy (đo 27-10-2026) ⇒ thư mục sao lưu config mặc định phải đi
    qua LOCALAPPDATA ra thư mục tạm GHI ĐƯỢC, ngoài $HOME. Chạy `ghi_bashrc` HAI lần: mỗi dòng đúng một lần,
    và một shell mới nạp ~/.bashrc thấy PATH có ~/.local/bin cùng LOCALAPPDATA dưới TMPDIR."""
    _posix()
    goc, env = _san()
    env = {**env, "TMPDIR": str(goc / "tmp")}
    p = subprocess.run([_bash(), "-c", 'source "$1"; ghi_bashrc; ghi_bashrc', "_", str(SCRIPT_DANG_DUNG)],
                       capture_output=True, text=True, env=env, timeout=60)
    bang(p.returncode == 0, f"ghi_bashrc rc={p.returncode} {p.stderr}")
    dong = (goc / "home/.bashrc").read_text(encoding="utf-8").splitlines()
    bang(len(dong) == len(set(dong)) == 2, f"~/.bashrc phải có đúng 2 dòng không trùng: {dong}")
    r = subprocess.run([_bash(), "-c", 'source "$HOME/.bashrc"; printf "%s\\n%s\\n" "$LOCALAPPDATA" "$PATH"'],
                       capture_output=True, text=True, env=env, timeout=60)
    lad, path = (r.stdout.splitlines() + ["", ""])[:2]
    bang(lad == str(goc / "tmp/tra-luat-localappdata"), f"LOCALAPPDATA phải dưới TMPDIR, được {lad!r}")
    bang(not lad.startswith(env["HOME"]), f"LOCALAPPDATA nằm dưới $HOME chỉ đọc: {lad!r}")
    bang(f"{env['HOME']}/.local/bin" in path.split(":"), f"PATH thiếu ~/.local/bin: {path!r}")


# (tên, chuỗi gốc, chuỗi đột biến, ca phải ĐỎ)
DOT_BIEN = [
    ("tai_ca_goi_da_cai", '    dpkg -s "$p" >/dev/null 2>&1 && continue\n', "", "ca_khong_root_tai_deb_bo_goi_da_cai"),
    ("wrapper_bo_ld_library_path", 'LD_LIBRARY_PATH="%s${LD_LIBRARY_PATH:-}" exec', "exec",
     "ca_khong_root_tai_deb_bo_goi_da_cai"),
    ("bo_nhanh_root", '[ "$(id -u)" = 0 ]', "false", "ca_root_dung_apt_get_install"),
    ("source_cung_chay_main", 'if [ "${BASH_SOURCE[0]}" = "$0" ]; then main "$@"; fi', 'main "$@"',
     "ca_source_khong_chay_main"),
    ("bo_dong_localappdata",
     "              'export LOCALAPPDATA=\"${LOCALAPPDATA:-${TMPDIR:-/tmp}/tra-luat-localappdata}\"'; do",
     "; do", "ca_bashrc_localappdata_ngoai_home"),
    ("bashrc_ghi_trung", 'grep -qxF "$dong" "$HOME/.bashrc" 2>/dev/null || printf', "printf",
     "ca_bashrc_localappdata_ngoai_home"),
]


def ca_dot_bien():
    """Mỗi đột biến phải làm ĐÚNG ca đích đỏ bằng `ChotCa` — chết vì lý do khác là tín dụng giả."""
    _posix()
    global SCRIPT_DANG_DUNG
    goc = SCRIPT.read_text(encoding="utf-8")
    tam = Path(tempfile.mkdtemp(prefix="codex-cloud-setup-dot-bien-"))
    song = []
    try:
        for ten, cu, moi, dich in DOT_BIEN:
            bang(goc.count(cu) == 1, f"đột biến {ten}: chuỗi gốc phải xuất hiện đúng 1 lần")
            SCRIPT_DANG_DUNG = tam / f"{ten}.sh"
            SCRIPT_DANG_DUNG.write_text(goc.replace(cu, moi), encoding="utf-8", newline="\n")
            try:
                globals()[dich]()
                song.append(f"{ten} (sống)")
            except ChotCa:
                pass
            except Exception as e:
                song.append(f"{ten} (tín dụng giả: {type(e).__name__})")
    finally:
        SCRIPT_DANG_DUNG = SCRIPT
    bang(not song, f"đột biến không bị giết đúng lý do: {song}")
    print(f"DOT BIEN: {len(DOT_BIEN)}/{len(DOT_BIEN)} bi giet dung ly do")


CA = [ca_tep_lf_khong_crlf, ca_khong_nang_cap_pip, ca_cu_phap_bash, ca_source_khong_chay_main,
      ca_co_san_khong_goi_apt, ca_khong_root_tai_deb_bo_goi_da_cai, ca_root_dung_apt_get_install,
      ca_sudo_khong_mat_khau_dung_sudo, ca_bashrc_localappdata_ngoai_home, ca_dot_bien]


def main():
    dat, bo_qua = 0, 0
    for ca in CA:
        try:
            ca()
            dat += 1
        except BoQua as e:  # không đo được trên nền này: in riêng, trừ khỏi tổng, KHÔNG tính đạt
            bo_qua += 1
            print(f"BO QUA {ca.__name__}: {e}")
        except Exception as e:  # ca đỏ vì bất kỳ lý do nào đều là đỏ; in tên ca và lý do
            print(f"DO {ca.__name__}: {type(e).__name__}: {e}")
    tong = len(CA) - bo_qua
    print(f"{dat}/{tong}")
    return 0 if dat == tong else 1


if __name__ == "__main__":
    sys.exit(main())
