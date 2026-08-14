"""Hardened single-source file and Git readers for the trusted oracle package.

`authority.py`, `corpus.py` và `oracle.py` từng mỗi bên giữ MỘT bản sao của cùng
một đoạn `lstat` + `O_NOFOLLOW` + đối chiếu dev/ino, và bản trong `corpus.py` đã
TRÔI LỆCH thật (nó để `lstat` ném `OSError` trần thay vì lỗi có kiểu).  Ba bản đó
gộp về đây.

`source_pin.py` CỐ Ý giữ bản sao riêng: nó là bootstrap chạy TRƯỚC khi bất kỳ
module ứng viên nào được import, nên không được phép import từ cây ứng viên.  Đó
là ngoại lệ có chủ đích, không phải trôi lệch — và nó được ĐO chứ không phải hứa:
`oracle/selftest.py::hardened_reader_parity_between_bootstrap_and_shared_module`
chạy cùng một ma trận fixture qua cả hai bản và bắt lỗi nếu chúng phân kỳ.
"""

from __future__ import annotations

import os
import pathlib
import stat
import subprocess
from typing import Callable


def read_regular_single_link(
    path: pathlib.Path | str,
    label: str,
    error: Callable[[str], BaseException],
    *,
    require_readonly: bool = False,
) -> bytes:
    """Đọc một tệp thường, một hard link, không symlink, không đổi danh tính giữa chừng.

    `error` là factory lỗi của module gọi, để mỗi tầng vẫn ném đúng kiểu lỗi có
    tên của mình thay vì một `RuntimeError` chung chung.
    """
    target = pathlib.Path(path)
    try:
        before = target.lstat()
    except OSError as exc:
        # `lstat` hỏng cũng là một kết luận — trả lỗi CÓ KIỂU, đừng để OSError trần
        # rò ra ngoài rồi bị tầng trên bắt nhầm thành "thiếu fixture".
        raise error("%s cannot be inspected: %s" % (label, exc)) from exc
    if not stat.S_ISREG(before.st_mode) or stat.S_ISLNK(before.st_mode):
        raise error("%s is not a regular non-symlink file" % label)
    if before.st_nlink != 1:
        raise error("%s must have exactly one hard link" % label)
    if require_readonly and before.st_mode & (stat.S_IWUSR | stat.S_IWGRP | stat.S_IWOTH):
        raise error("%s must be sealed read-only" % label)
    flags = os.O_RDONLY | getattr(os, "O_NOFOLLOW", 0)
    # Thông điệp lỗi ở nhánh này phải TRÙNG bản trong `source_pin._read_regular_single_link`;
    # phép đo parity so đúng chuỗi trả về, nên một câu chữ lệch cũng là trôi lệch.
    try:
        fd = os.open(target, flags)
        with os.fdopen(fd, "rb") as handle:
            opened = os.fstat(handle.fileno())
            # Chen symlink/rename GIỮA lstat và open là ca TOCTOU kinh điển; so
            # (dev, ino) trên CHÍNH descriptor đang giữ mới bắt được.
            if (before.st_dev, before.st_ino) != (opened.st_dev, opened.st_ino):
                raise error("%s changed identity while opening" % label)
            return handle.read()
    except OSError as exc:
        raise error("%s cannot be read safely: %s" % (label, exc)) from exc


def git(
    root: pathlib.Path | str,
    *args: str,
    error: Callable[[str], BaseException],
    binary: bool = False,
):
    """Chạy git ở `root` và ném lỗi có kiểu khi rc khác 0.

    Không dùng `check=True`: `CalledProcessError` nuốt mất stderr trong thông báo,
    mà stderr chính là chỗ git nói vì sao ref/blob không với tới được.
    """
    proc = subprocess.run(
        ["git", "-C", str(root), *args],
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=not binary,
    )
    if proc.returncode != 0:
        stderr = proc.stderr if isinstance(proc.stderr, str) else proc.stderr.decode("utf-8", "replace")
        raise error("git %s failed rc=%d: %s" % (" ".join(args), proc.returncode, stderr.strip()))
    return proc.stdout
