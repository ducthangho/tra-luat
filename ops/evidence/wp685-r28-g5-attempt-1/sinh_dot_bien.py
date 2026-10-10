"""Sinh 54 mục DOT_BIEN của wp685 (đặc tả r28 §7 B5) từ launcher.py ứng viên; in khối Python để chèn.
Mỗi mục: một thay đổi ở một vị trí; neo (chuỗi cũ) phải xuất hiện ĐÚNG MỘT lần trong ứng viên."""
import sys
from pathlib import Path

src = Path(sys.argv[1]).read_text(encoding="utf-8")
T156 = "t156_con_song_esrch_va_mien_loi_proc_stat_theo_nhan"
T157 = "t157_giet_cay_khi_stat_EACCES_van_tron_ven"
DOC = 'noi_dung = trang_thai.read_text(encoding="latin-1")'
TACH = 'return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"'
H_PLE = "    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None"
H_OS = "    except OSError:\n        co_tep = None"
D0_NEO = "comment 5905670017; cross-review lượt 7, lượt 8).\n"
D0 = (D0_NEO + f"        try:\n            {DOC}\n            {TACH}\n"
      "        except (OSError, ValueError, IndexError):\n            return False")
D_NEO = "Khối bọc chỉ gồm phép đọc và biểu thức tách theo ')' CUỐI.\n"
D = (D_NEO + f"        try:\n            {DOC}\n            {TACH}\n"
     "        except (OSError, ValueError, IndexError):\n            pass")
D_EX = D_NEO + f"        try:\n            {DOC}\n            {TACH}\n"
K = ("    try:\n        os.kill(pid, 0)\n    except ProcessLookupError:\n        return False\n"
     "    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n    except OSError:\n        return False\n")
for x in (H_PLE, D0, D, K):
    assert src.count(x) == 1, x

def d_except(moi):  # thay mệnh đề bắt của khối Đ
    return (D, D_EX + moi)

dong = []
def them(lop, ten, cap, dich=(T156,)):
    old, new = cap
    assert src.count(old) == 1, ten
    assert old != new
    dong.append((lop, ten, old, new, list(dich)))

# (a)-(j)
i0 = src.index("    try:\n        co_tep = trang_thai.exists()")
i1 = src.index(D) + len(D) + 1
vung = src[i0:i1]
nen_hoi = ('    if trang_thai.exists():\n        try:\n            ' + DOC + '\n            ' + TACH +
           '\n        except (OSError, ValueError, IndexError):\n            return False\n')
them("a", "wp685_a_go_ban_va", (vung, nen_hoi))
them("b", "wp685_b_ban_rong", (H_OS, "    except OSError:\n        return False"))
them("c", "wp685_c_bo_doc_duong_moi", (D, D_NEO + "        pass"), (T156, T157))
them("d1", "wp685_d1_hoi_chi_PermissionError", (H_OS, "    except PermissionError:\n        co_tep = None"))
them("d2", "wp685_d2_doc_chi_PermissionError", d_except("        except (PermissionError, ValueError, IndexError):\n            pass"))
them("e1", "wp685_e1_hoi_nuot_BaseException", (H_OS, "    except BaseException:\n        co_tep = None"))
them("e2", "wp685_e2_doc_nuot_KeyboardInterrupt",
     d_except("        except KeyboardInterrupt:\n            pass\n        except (OSError, ValueError, IndexError):\n            pass"))
them("f", "wp685_f_hoi_exists_lan_hai", ("        co_tep = trang_thai.exists()\n",
                                         "        co_tep = trang_thai.exists() and trang_thai.exists()\n"))
them("g1", "wp685_g1_doc_loi_False",
     d_except("        except OSError:\n            return False\n        except (ValueError, IndexError):\n            pass"))
them("g2", "wp685_g2_doc_ESRCH_False",
     d_except("        except ProcessLookupError:\n            return False\n"
              "        except (OSError, ValueError, IndexError):\n            pass"))
them("h1", "wp685_h1_hoi_bat_Exception", (H_OS, "    except Exception:\n        co_tep = None"))
them("h2", "wp685_h2_doc_bat_Exception", d_except("        except Exception:\n            pass"))
them("i", "wp685_i_noi_dung_hong_False",
     d_except("        except OSError:\n            pass\n        except (ValueError, IndexError):\n            return False"))
them("j1", "wp685_j1_doc_lan_hai_sau_thanh_cong",
     (D_EX, D_NEO + f"        try:\n            {DOC}\n            {DOC}\n            {TACH}\n"))
them("j2", "wp685_j2_doc_lan_hai_khi_doc_loi",
     d_except("        except (OSError, ValueError, IndexError):\n            try:\n"
              "                trang_thai.read_text(encoding=\"latin-1\")\n            except OSError:\n                pass"))
# (k)
them("k1", "wp685_k1_tra_True_khong_hoi_pid", d_except("        except (OSError, ValueError, IndexError):\n            return True"))
them("k2", "wp685_k2_hoi_pid_bo_ket_qua",
     d_except("        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n"
              "            except OSError:\n                pass\n            return True"))
them("k3", "wp685_k3_tu_kill_PermissionError_False",
     d_except("        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n"
              "            except OSError:\n                return False\n            return True"))
them("k4", "wp685_k4_tu_kill_OSError_khac_True",
     d_except("        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n"
              "            except ProcessLookupError:\n                return False\n            except OSError:\n"
              "                return True\n            return True"))
them("k5", "wp685_k5_hoi_pid_hai_lan",
     d_except("        except (OSError, ValueError, IndexError):\n            try:\n                os.kill(pid, 0)\n"
              "            except OSError:\n                pass"))
# (l) tầng H
them("l1", "wp685_l1_hoi_chi_ProcessLookupError", (H_PLE, "    except ProcessLookupError:\n        return False"))
them("l2", "wp685_l2_hoi_ESRCH_chung_nhanh", (H_PLE, H_OS))
them("l3", "wp685_l3_hoi_OSError_khac_False",
     (H_OS, "    except PermissionError:\n        co_tep = None\n    except OSError:\n        return False"))
them("l4", "wp685_l4_hoi_errno_trang_EACCES_EIO",
     (H_OS, "    except OSError as e:\n        if e.errno not in (13, 5):\n            raise\n        co_tep = None"))
them("l5", "wp685_l5_hoi_EPERM_False",
     (H_OS, "    except OSError as e:\n        if e.errno == 1:\n            return False\n        co_tep = None"))
them("l6", "wp685_l6_hoi_them_IndexError", (H_OS, "    except (OSError, IndexError):\n        co_tep = None"))
them("l7", "wp685_l7_hoi_them_ValueError", (H_OS, "    except (OSError, ValueError):\n        co_tep = None"))
them("l8", "wp685_l8_hoi_them_UnicodeDecodeError", (H_OS, "    except (OSError, UnicodeDecodeError):\n        co_tep = None"))
them("l9", "wp685_l9_hoi_boc_Exception",
     (H_OS, H_OS + "\n    except Exception as e:\n        raise RuntimeError(\"boc\") from e"))
# (l) tầng Đ
them("l10", "wp685_l10_doc_chi_bat_phan_tich", d_except("        except (ValueError, IndexError):\n            pass"))
them("l11", "wp685_l11_doc_errno_EACCES_EIO",
     d_except("        except (OSError, ValueError, IndexError) as e:\n"
              "            if isinstance(e, OSError) and e.errno not in (13, 5):\n                raise"))
them("l12", "wp685_l12_doc_errno_EACCES_EIO_ESRCH",
     d_except("        except (OSError, ValueError, IndexError) as e:\n"
              "            if isinstance(e, OSError) and e.errno not in (13, 5, 3):\n                raise"))
them("l13", "wp685_l13_doc_EPERM_False",
     d_except("        except (OSError, ValueError, IndexError) as e:\n"
              "            if isinstance(e, OSError) and e.errno == 1:\n                return False"))
them("l14", "wp685_l14_doc_OSError_khac_False",
     d_except("        except PermissionError:\n            pass\n        except OSError:\n            return False\n"
              "        except (ValueError, IndexError):\n            pass"))
them("l15", "wp685_l15_doc_khong_bat_ValueError", d_except("        except (OSError, IndexError):\n            pass"))
them("l16", "wp685_l16_doc_kiem_chuoi_rong",
     (D, D_NEO + f"        try:\n            {DOC}\n            if noi_dung:\n                {TACH}\n"
      "        except (OSError, IndexError):\n            pass"))
them("l17", "wp685_l17_doc_khong_bat_IndexError", d_except("        except (OSError, ValueError):\n            pass"))
them("l18", "wp685_l18_doc_IndexError_False",
     d_except("        except IndexError:\n            return False\n        except (OSError, ValueError):\n            pass"))
them("l19", "wp685_l19_doc_chi_OSError_tach_rieng",
     (D, D_NEO + f"        try:\n            {DOC}\n        except OSError:\n            noi_dung = \"\"\n"
      f"        try:\n            {TACH}\n        except (ValueError, IndexError):\n            pass"))
them("l20", "wp685_l20_doc_UnicodeDecodeError_False",
     d_except("        except UnicodeDecodeError:\n            return False\n"
              "        except (OSError, ValueError, IndexError):\n            pass"))
them("l21", "wp685_l21_doc_boc_ValueError",
     d_except("        except ValueError as e:\n            raise RuntimeError(\"boc\") from e\n"
              "        except (OSError, IndexError):\n            pass"))
# (l) tầng K
K_PLE = "    except ProcessLookupError:\n        return False\n    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n    except OSError:\n        return False\n    if platform.system() == \"Darwin\":  # không có /proc: hỏi ps"
assert src.count(K_PLE) == 1
K_DUOI = "    except OSError:\n        return False\n    if platform.system() == \"Darwin\":  # không có /proc: hỏi ps"
K_DARWIN = "    if platform.system() == \"Darwin\":  # không có /proc: hỏi ps"
them("l22", "wp685_l22_kill_chi_PermissionError",
     (K_PLE, "    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n" + K_DARWIN))
them("l23", "wp685_l23_kill_chi_ProcessLookupError", (K_PLE, "    except ProcessLookupError:\n        return False\n" + K_DARWIN))
them("l24", "wp685_l24_kill_bo_OSError", (K_DUOI, K_DARWIN))
for ma, ten, lop in (("l25", "BaseException", "l25"), ("l26", "Exception", "l26"), ("l27", "IndexError", "l27"),
                     ("l28", "ValueError", "l28"), ("l29", "UnicodeDecodeError", "l29")):
    them(lop, f"wp685_{ma}_kill_them_{ten}", (K_DUOI, "    except OSError:\n        return False\n"
                                               f"    except {ten}:\n        return True\n" + K_DARWIN))
# (m)
them("m1", "wp685_m1_nhanh_cu_hop_nhat_ve_kill", (D0, D0[:-len("return False")] + "pass"))
them("m2", "wp685_m2_nhanh_cu_bat_BaseException", (D0, D0 + "\n        except BaseException:\n            return False"))
them("m3", "wp685_m3_tep_vang_False", ("    if co_tep is None:\n", "    if co_tep is False:\n        return False\n    if co_tep is None:\n"))
them("m4", "wp685_m4_ESRCH_hoi_lai", ("    except ProcessLookupError:\n        return False\n    except OSError:\n        co_tep = None",
                                      "    except ProcessLookupError:\n        try:\n            trang_thai.exists()\n"
                                      "        except OSError:\n            pass\n        return False\n    except OSError:\n        co_tep = None"))
them("m5", "wp685_m5_duong_moi_tach_ngoac_dau",
     (D_EX, D_NEO + f"        try:\n            {DOC}\n            " + TACH.replace("rindex", "index") + "\n"))
assert len(dong) == 54, len(dong)
assert len({d[1] for d in dong}) == 54
for lop, ten, old, new, dich in dong:
    m = src.replace(old, new, 1)
    compile(m, ten, "exec")
out = ["    # ---- wp685 (đặc tả r28 §7 B5): 54 dòng (a)–(m), mỗi dòng MỘT vị trí; (c) hai ca đích ⇒ 55 cặp."]
for lop, ten, old, new, dich in dong:

    out.append(f"    ({ten!r},")
    out.append(f"     ({old!r},")
    out.append(f"      {new!r}),")
    out.append(f"     {dich!r}),")
print("\n".join(out))
