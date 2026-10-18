"""wp685 r28 (g5 attempt 2: chỉ đổi lời gọi AW.doi_chieu sang bộ ba thiếu/thừa/sai thứ tự) — phép (E) (B5 (E) mục 1–6): một biến thể của CHÍNH ứng viên cho mỗi tên ở danh sách ĐÓNG mục 6.
Dùng: python3.1x -B bang_chung_e.py <.claude/dev ứng viên> <thư mục tạm> <tệp đặc tả r28> [bang.json]
Đỏ (rc=1) khi: neo không xuất hiện ĐÚNG MỘT lần, biến thể giống hệt ứng viên, tập tên khác danh sách ĐÓNG trích từ
đặc tả, hay một biến thể không đúng kỳ vọng."""
import ast
import errno
import json
import sys
from pathlib import Path

sys.dont_write_bytecode = True
sys.argv += [""] * 0
DEV, TAM, SPEC = Path(sys.argv[1]).resolve(), Path(sys.argv[2]).resolve(), Path(sys.argv[3])
BANG_RA = Path(sys.argv[4]) if len(sys.argv) > 4 else None
TAM.mkdir(parents=True, exist_ok=True)
sys.path.insert(0, str(Path(__file__).resolve().parent))
import bang_chung_aw_d as AW  # noqa: E402  (chỉ dùng hàm; chế độ "none" không chạy gì)

SRC = (DEV / "launcher.py").read_text(encoding="utf-8")
T156, T157 = AW.T156, AW.T157
B8 = {"t158": "t158_comm_hong_SAU_luc_sinh_qua_han_khong_duoc_124_khi_con_song",
      "t159": "t159_chuong_trinh_ten_tieng_Viet_qua_han_phai_giet_duoc",
      "t160": "t160_giet_cay_chau_setsid_comm_hong_phot_lo_SIGTERM",
      "t161": "t161_giet_cay_me_da_thoat_chau_cung_nhom_comm_hong"}
B8_TEN = {"t158": "B8-sau-sinh", "t159": "B8-luc-sinh", "t160": "B8-setsid", "t161": "B8-me-thoat"}

# ---- danh sách ĐÓNG mục 6, trích bằng máy từ đặc tả (khối giữa "DS-E-HANG-MUC <n>" và rào đóng)
dong = SPEC.read_text(encoding="utf-8").splitlines()
i = dong.index("DS-E-HANG-MUC 83")
nhom, ds = None, {}
for d in dong[i:]:
    if d.startswith("```"):
        break
    p = d.split()
    if len(p) == 2 and p[0].startswith("DS-E-") and p[1].isdigit():
        nhom = p[0]
        ds[nhom] = (int(p[1]), [])
    else:
        ds[nhom][1].extend(p)
for k, (n, t) in ds.items():
    assert n == len(t) == len(set(t)), (k, n, len(t))

DOC = 'noi_dung = trang_thai.read_text(encoding="latin-1")'
TACH = 'return noi_dung[noi_dung.rindex(")") + 2:].split()[0] != "Z"'
D0_NEO = "comment 5905670017; cross-review lượt 7, lượt 8).\n"
D_NEO = "Khối bọc chỉ gồm phép đọc và biểu thức tách theo ')' CUỐI.\n"
D0 = D0_NEO + f"        try:\n            {DOC}\n            {TACH}\n        except (OSError, ValueError, IndexError):\n            return False"
D = D_NEO + f"        try:\n            {DOC}\n            {TACH}\n        except (OSError, ValueError, IndexError):\n            pass"
H_OS = "    except OSError:\n        co_tep = None   # KHÔNG kết luận"
K_PLE = "    except ProcessLookupError:\n        return False\n    except PermissionError:"
K_PE = "    except PermissionError:\n        return True  # tồn tại nhưng khác chủ\n"
K_OS = "    except OSError:\n        return False\n    if platform.system() == \"Darwin\":  # không có /proc: hỏi ps"
K_DARWIN = "    if platform.system() == \"Darwin\":  # không có /proc: hỏi ps"
VANG = "    if co_tep is None:\n        # wp685 (zombie"
KHOA_DOC = '            noi_dung = Path(f"/proc/{pid}/stat").read_text(encoding="latin-1")'
NHOM_DOC = '"biến mất"\n                nd = (p / "stat").read_text(encoding="latin-1")'
CHUP_DOC = 'ảnh chụp\n                nd = (p / "stat").read_text(encoding="latin-1")'


def d0x(moi):
    return (D0, D0[:D0.index("        except (OSError")] + moi)


def dx(moi):
    return (D, D[:D.index("        except (OSError")] + moi)


def ex(cls, than, sau=True, khoi="d0"):
    """thêm mệnh đề `except cls…` vào khối đọc (sau mệnh đề sẵn có nếu `sau`)."""
    goc, tra = (D0, "return False") if khoi == "d0" else (D, "pass")
    them = f"\n        except {cls}{than}"
    return (goc, goc + them) if sau else (goc, goc.replace("        except (OSError", f"        except {cls}{than}\n        except (OSError"))


def kx(cls, than):
    return (K_OS, f"    except OSError:\n        return False\n    except {cls}{than}\n" + K_DARWIN)


V = {}  # tên mục 6 -> (danh sách cặp (neo, thay), kỳ vọng)
G = lambda nhan, tieu=None, loai=None, ca=T156: ("giet", ca, nhan, tieu, loai)  # noqa: E731
VC = lambda nhan, tieu=None, ca=T156: ("vo_can", ca, nhan, tieu, None)  # noqa: E731
B = lambda *ds: ("b8", ds)  # noqa: E731  — ds: (ca, loai)
SONG = ("song",)
RB = ": raise RuntimeError(\"thay\")"
BOC = " as e: raise RuntimeError(\"boc\") from e"
# --- DS-E-HANG-MUC
V["h_co_bo_doc"] = ([("    if co_tep:\n", "    if False:\n")], G("B2-nhanh-cu", "song", "read count"))
V["d0_ok_khongZ_sai"] = ([(D0, D0.replace('!= "Z"', '== "Z"'))], G("B2-nhanh-cu", "song", "result False"))
V["d0_ok_Z_sai"] = ([(D0, D0.replace('!= "Z"', '!= "Z" or True'))], G("B3-zombie", None, "result True"))
V["k0_ok_sai"] = ([("    return True\n\n\nclass KetGiet", "    return False\n\n\nclass KetGiet")], G("B2-nhanh-cu", "vang", "result False"))
V["d_ok_khongZ_sai"] = ([(D, D.replace('!= "Z"', '== "Z"'))], G("B2-eacces", None, "result False"))
V["d_ok_Z_sai"] = ([(D, D.replace('!= "Z"', '!= "Z" or True'))], G("B3-zombie", None, "result True"))
V["k_ok_sai"] = ([("    return True\n\n\nclass KetGiet", "    return False\n\n\nclass KetGiet")], G("B2-doc-hong", "EACCES", "result False"))
V["d0_ESRCH_thoat"] = ([ex("ProcessLookupError", ":\n            raise", sau=False)], G("B2-nhanh-cu", "ESRCH", "seam escaped"))
V["d0_ESRCH_sai"] = ([ex("ProcessLookupError", ":\n            return True", sau=False)], G("B2-nhanh-cu", "ESRCH", "result True"))
for ten, so, tieu in (("EACCES", 13, "EACCES"), ("EIO", 5, "EIO"), ("EPERM", 1, "EPERM")):
    V[f"d0_{ten}_thoat"] = ([d0x(f"        except (OSError, ValueError, IndexError) as e:\n            if getattr(e, 'errno', None) == {so}:\n                raise\n            return False")], G("B2-nhanh-cu", tieu, "seam escaped"))
    if ten != "EACCES":
        V[f"d0_{ten}_sai"] = ([d0x(f"        except (OSError, ValueError, IndexError) as e:\n            if getattr(e, 'errno', None) == {so}:\n                return True\n            return False")], G("B2-nhanh-cu", tieu, "result True"))
V["d0_value_thoat"] = ([d0x("        except (OSError, IndexError):\n            return False")], G("B2-nhanh-cu", "p1", "parse error escaped"))
V["d0_value_sai"] = ([ex("ValueError", ":\n            return True", sau=False)], G("B2-nhanh-cu", "p1", "result True"))
V["d0_index_thoat"] = ([d0x("        except (OSError, ValueError):\n            return False")], G("B2-nhanh-cu", "p3", "parse error escaped"))
V["d0_index_sai"] = ([ex("IndexError", ":\n            return True", sau=False)], G("B2-nhanh-cu", "p3", "result True"))
V["d0_decode_thoat"] = ([ex("UnicodeDecodeError", ":\n            raise", sau=False)], G("B2-nhanh-cu", "p4", "seam escaped"))
V["d0_decode_sai"] = ([ex("UnicodeDecodeError", ":\n            return True", sau=False)], G("B2-nhanh-cu", "p4", "result True"))
V["d0_exception_bat"] = ([ex("Exception", ":\n            return False")], G("B2-nhanh-cu", "exception", "sentinel identity"))
V["d0_exception_boc"] = ([ex("Exception", " as e:\n            raise RuntimeError(\"boc\") from e")], G("B2-nhanh-cu", "exception", "seam wrapped"))
V["d0_exception_thaythe"] = ([ex("Exception", ":\n            raise RuntimeError(\"thay\")")], VC("B2-nhanh-cu", "exception"))
V["d0_tin-hieu_boc"] = ([ex("KeyboardInterrupt", " as e:\n            raise RuntimeError(\"boc\") from e")], G("B2-nhanh-cu", "tin-hieu", "seam wrapped"))
V["d0_tin-hieu_thaythe"] = ([ex("KeyboardInterrupt", ":\n            raise RuntimeError(\"thay\")")], VC("B2-nhanh-cu", "tin-hieu"))
V["k0_ESRCH_thoat"] = ([(K_PLE, "    except ProcessLookupError:\n        raise\n    except PermissionError:")], G("B2-nhanh-cu", "vang-da-wait", "seam escaped"))
V["k0_ESRCH_sai"] = ([(K_PLE, "    except ProcessLookupError:\n        return True\n    except PermissionError:")], G("B2-nhanh-cu", "vang-da-wait", "result True"))
V["k0_EPERM_thoat"] = ([(K_PE, "    except PermissionError:\n        raise\n")], G("B2-nhanh-cu", "vang-eperm", "seam escaped"))
V["k0_EPERM_sai"] = ([(K_PE, "    except PermissionError:\n        return False\n")], G("B2-nhanh-cu", "vang-eperm", "result False"))
V["k0_EIO_thoat"] = ([(K_OS, "    except OSError:\n        raise\n" + K_DARWIN)], G("B2-nhanh-cu", "vang-eio", "seam escaped"))
V["k0_EIO_sai"] = ([(K_OS, "    except OSError:\n        return True\n" + K_DARWIN)], G("B2-nhanh-cu", "vang-eio", "result True"))
TV = {"index": ("IndexError", "kill-index", "vang-index"), "value": ("ValueError", "kill-value", "vang-value"),
      "decode": ("UnicodeDecodeError", "kill-decode", "vang-decode"), "exception": ("Exception", None, "vang-exception"),
      "tin-hieu": ("KeyboardInterrupt", None, "vang-tin-hieu")}
for tv, (cls, _k, vang) in TV.items():
    bat_cls = "BaseException" if tv == "tin-hieu" else cls
    V[f"k0_{tv}_bat"] = ([kx(bat_cls, ":\n        return True")], G("B2-nhanh-cu", vang, "sentinel identity"))
    V[f"k0_{tv}_boc"] = ([kx(cls, " as e:\n        raise RuntimeError(\"boc\") from e")], G("B2-nhanh-cu", vang, "seam wrapped"))
    V[f"k0_{tv}_thaythe"] = ([kx(cls, ":\n        raise RuntimeError(\"thay\")")], VC("B2-nhanh-cu", vang))
H_DICH = {"index": ("B2-thoat-parse", "hoi-index"), "value": ("B2-thoat-parse", "hoi-value"),
          "decode": ("B2-thoat-parse", "hoi-decode"), "exception": ("B2-exception", "hoi"), "tin-hieu": ("B2-tin-hieu", "hoi")}
K_DICH = {"index": ("B2-thoat-parse", "kill-index"), "value": ("B2-thoat-parse", "kill-value"),
          "decode": ("B2-thoat-parse", "kill-decode"), "exception": ("B2-exception", "kill"), "tin-hieu": ("B2-tin-hieu", "kill")}
for tv, (cls, _k, _v) in TV.items():
    if tv != "exception":
        V[f"h_{tv}_boc"] = ([(H_OS, H_OS.split("   #")[0] + f"\n    except {cls} as e:\n        raise RuntimeError(\"boc\") from e  #")], G(*H_DICH[tv], "seam wrapped"))
    V[f"h_{tv}_thaythe"] = ([(H_OS, H_OS.split("   #")[0] + f"\n    except {cls}:\n        raise RuntimeError(\"thay\")  #")], VC(*H_DICH[tv]))
    V[f"k_{tv}_boc"] = ([kx(cls, " as e:\n        raise RuntimeError(\"boc\") from e")], G(*K_DICH[tv], "seam wrapped"))
    V[f"k_{tv}_thaythe"] = ([kx(cls, ":\n        raise RuntimeError(\"thay\")")], VC(*K_DICH[tv]))
V["d_exception_boc"] = ([ex("Exception", " as e:\n            raise RuntimeError(\"boc\") from e", khoi="d")], G("B2-exception", "doc", "seam wrapped"))
V["d_tin-hieu_boc"] = ([ex("KeyboardInterrupt", " as e:\n            raise RuntimeError(\"boc\") from e", khoi="d")], G("B2-tin-hieu", "doc", "seam wrapped"))
V["d_exception_thaythe"] = ([ex("Exception", ":\n            raise RuntimeError(\"thay\")", khoi="d")], VC("B2-exception", "doc"))
V["d_tin-hieu_thaythe"] = ([ex("KeyboardInterrupt", ":\n            raise RuntimeError(\"thay\")", khoi="d")], VC("B2-tin-hieu", "doc"))
V["h_thoat_hoi_lai"] = ([(H_OS, H_OS.split("   #")[0] + "\n    except BaseException:\n        try:\n            trang_thai.exists()\n        except BaseException:\n            pass\n        raise  #")], G("B2-tin-hieu", "hoi", "stat count"))
V["d0_doc_hai_lan"] = ([(D0, D0.replace(DOC, DOC + "\n            " + DOC))], G("B2-nhanh-cu", "song", "read count"))
V["d0_them_kill"] = ([(D0, D0.replace(D0_NEO, D0_NEO + "        try:\n            os.kill(pid, 0)\n        except OSError:\n            pass\n"))], G("B2-nhanh-cu", "song", "kill count"))
V["k0_hoi_hai_lan"] = ([(VANG, "    if co_tep is False:\n        trang_thai.exists()\n" + VANG)], G("B2-nhanh-cu", "vang", "stat count"))
V["k0_them_doc"] = ([(VANG, "    if co_tep is False:\n        try:\n            trang_thai.read_text(encoding=\"latin-1\")\n        except OSError:\n            pass\n" + VANG)], G("B2-nhanh-cu", "vang", "read count"))
V["k0_kill_hai_lan"] = ([(VANG, "    if co_tep is False:\n        try:\n            os.kill(pid, 0)\n        except OSError:\n            pass\n" + VANG)], G("B2-nhanh-cu", "vang", "kill count"))
V["d_hoi_lai_khac_EACCES"] = ([(H_OS, "    except OSError as e:\n        if e.errno != 13:\n            try:\n                trang_thai.exists()\n            except OSError:\n                pass\n        co_tep = None   # KHÔNG kết luận")], G("B2-eio", None, "stat count"))
V["k_hoi_hai_lan"] = ([dx("        except (OSError, ValueError, IndexError):\n            try:\n                trang_thai.exists()\n            except OSError:\n                pass")], G("B2-doc-hong", "EACCES", "stat count"))
V["d0_tach_ngoac_dau"] = ([(D0, D0.replace("rindex", "index"))], G("B3-zombie", None, "result True"))
V["g_khoa"] = ([(KHOA_DOC, KHOA_DOC.replace('encoding="latin-1"', ""))], B(("t159", "qua han khong giet duoc"), ("t160", "124 noi doi"), ("t161", "124 noi doi")))
V["g_nhom"] = ([(NHOM_DOC, NHOM_DOC.replace('encoding="latin-1"', ""))], B(("t160", "read args"), ("t161", "124 noi doi")))
V["g_chup"] = ([(CHUP_DOC, CHUP_DOC.replace('encoding="latin-1"', ""))], B(("t160", "124 noi doi"), ("t161", "khong giet duoc")))
V["g_d0"] = ([(D0, D0.replace('encoding="latin-1"', ""))], ("gop", [G("B2-nhanh-cu", "song", "read args")], [("t160", "124 noi doi"), ("t161", "124 noi doi")]))
V["g_d"] = ([(D, D.replace('encoding="latin-1"', ""))], G("B2-eacces", None, "read args"))
# --- DS-E-KHAC
V["d0_giai_ma_long"] = ([(D0, D0.replace('encoding="latin-1"', 'encoding="latin-1", errors="replace"'))], G("B2-nhanh-cu", "song", "read args"))
V["d_giai_ma_long"] = ([(D, D.replace('encoding="latin-1"', 'encoding="latin-1", errors="replace"'))], G("B2-eacces", None, "read args"))
for ten, neo in (("khoa", KHOA_DOC), ("nhom", NHOM_DOC), ("chup", CHUP_DOC)):
    V[f"g_{ten}_errors"] = ([(neo, neo.replace('encoding="latin-1"', 'encoding="latin-1", errors="surrogateescape"'))], B(("t160", "read args"), ("t161", "read args")))
V["d0_giai_ma_lai_utf8"] = ([(D0, D0.replace(DOC, DOC + "\n            noi_dung = noi_dung.encode(\"latin-1\").decode(\"utf-8\")"))], G("B2-nhanh-cu", "utf8-hong-that", "result False"))
V["d_giai_ma_lai_utf8"] = ([(D, D.replace(DOC, DOC + "\n            noi_dung = noi_dung.encode(\"latin-1\").decode(\"utf-8\")"))], G("B2-dem-doc", "4", "kill count"))
V["g_khoa_open"] = ([(KHOA_DOC, '            noi_dung = open(f"/proc/{pid}/stat", encoding="latin-1").read()')], B(("t160", "read args"), ("t161", "read args")))
V["g_nhom_open"] = ([(NHOM_DOC, NHOM_DOC.replace('(p / "stat").read_text(encoding="latin-1")', 'open(p / "stat", encoding="latin-1").read()'))], B(("t160", "read args"), ("t161", "read args")))
V["g_chup_open"] = ([(CHUP_DOC, CHUP_DOC.replace('(p / "stat").read_text(encoding="latin-1")', 'open(p / "stat", encoding="latin-1").read()'))], B(("t160", "read args"), ("t161", "read args")))
V["g_d0_open"] = ([(D0, D0.replace(DOC, 'noi_dung = open(trang_thai, encoding="latin-1").read()'))], ("gop", [G("B2-nhanh-cu", "song", "read count")], [("t160", "read args"), ("t161", "read args")]))
V["g_d_open"] = ([(D, D.replace(DOC, 'noi_dung = open(trang_thai, encoding="latin-1").read()'))], G("B2-eacces", None, "read count"))
V["s_khoa_tach_ngoac_dau"] = ([("            sau = noi_dung[noi_dung.rindex(\")\") + 2:].split()\n            return f\"linux:", "            sau = noi_dung[noi_dung.index(\")\") + 2:].split()\n            return f\"linux:")], B(("t160", "124 noi doi"), ("t161", "124 noi doi")))
V["s_nhom_tach_ngoac_dau"] = ([(NHOM_DOC + "\n                sau = nd[nd.rindex", NHOM_DOC + "\n                sau = nd[nd.index")], B(("t161", "124 noi doi"),))
V["s_chup_tach_ngoac_dau"] = ([(CHUP_DOC + "\n                sau = nd[nd.rindex", CHUP_DOC + "\n                sau = nd[nd.index")], B(("t160", "124 noi doi"), ("t161", "khong giet duoc")))
V["g_to_hop_khoa_nhom"] = ([(KHOA_DOC, KHOA_DOC.replace('encoding="latin-1"', "")), (NHOM_DOC, NHOM_DOC.replace('encoding="latin-1"', ""))],
                           B(("t158", "124 noi doi"), ("t159", "qua han khong giet duoc"), ("t160", "124 noi doi"), ("t161", "124 noi doi")))
V["g_to_hop_dinh_dang_khoa"] = ([('return f"linux:{sau[19]}"', 'return f"linux:{sau[19]!r}"'), ('f"linux:{sau[19]}")', 'f"linux:{sau[19]!r}")')], B(("t160", "khong giet duoc"),))
V["d_doc_lai_khi_EPERM"] = ([dx("        except (OSError, ValueError, IndexError) as e:\n            if getattr(e, 'errno', None) == 1:\n                try:\n                    trang_thai.read_text(encoding=\"latin-1\")\n                except OSError:\n                    pass")], G("B2-doc-hong", "EPERM", "read count"))
V["k_kill_lai_khi_doc_EPERM"] = ([dx("        except (OSError, ValueError, IndexError) as e:\n            if getattr(e, 'errno', None) == 1:\n                try:\n                    os.kill(pid, 0)\n                except OSError:\n                    pass")], G("B2-doc-hong", "EPERM", "kill count"))
# năm bản vá sai lượt 6 trùng (m1)–(m5): lấy nguyên cặp của DOT_BIEN
_m = AW.nap(DEV / "launcher.py")
for k, n in (("m1", "B2-nhanh-cu"), ("m2", "B2-nhanh-cu"), ("m3", "B2-nhanh-cu"), ("m4", "B1"), ("m5", "B3-zombie")):
    muc = [x for x in _m.DOT_BIEN if x[0].startswith(f"wp685_{k}_")][0]
    _c, nh, tieu, loai = AW.DICH[k][0]
    V[f"luot6_{k}"] = ([muc[1]], G(nh, tieu, loai))
for ten, bieu in (("dc_khac_doi_so", 'raise ValueError("khac doi so")'), ("dc_fp", 'raise ValueError("substring not found")'),
                  ("dc_fp2", 'int("khong-phai-so")'), ("dc_fp3", '"".rindex(")")'), ("dc_fp4", 'str(noi_dung).rindex(")")'),
                  ("dc_fp5", '"x".index(")")'), ("dc_fp6", 'for _s in ("",):\n                _s[_s.rindex(")") + 2:]'),
                  ("dc_fp6b", 'for _s in ("", ""):\n                _s[_s.rindex(")") + 2:].split()[0]')):
    V[ten] = ([dx(f"        except ValueError:\n            {bieu}\n        except (OSError, IndexError):\n            pass")], VC("B2-parse", "p1"))
V["dc_j1_sai_doi_so"] = ([(D, D.replace(DOC, DOC + "\n            trang_thai.read_text(encoding=\"khong-co-ma-nay\")"))], VC("B2-dem-doc", "1"))
V["song_K0_tach_rieng"] = ([(VANG, "    if co_tep is False and platform.system() == \"Linux\":\n        try:\n            os.kill(pid, 0)\n        except ProcessLookupError:\n            return False\n        except PermissionError:\n            return True\n        except OSError:\n            return False\n        return True\n" + VANG)], SONG)
V["song_ba_errno"] = ([(H_OS, "    except OSError as e:\n        if e.errno not in (13, 1, 5):\n            raise\n        co_tep = None   # KHÔNG kết luận")], SONG)

dong_ky_vong = set(ds["DS-E-HANG-MUC"][1]) | set(ds["DS-E-KHAC"][1])
thieu, thua = sorted(dong_ky_vong - set(V)), sorted(set(V) - dong_ky_vong)
print(f"(E) tap ten: {len(V)} bien the; DS-E-HANG-MUC {ds['DS-E-HANG-MUC'][0]} + DS-E-KHAC {ds['DS-E-KHAC'][0]}; "
      f"DS-E-C3 khong ap dung (ung vien KHONG tach trang thai trong ham tro giup); thieu={thieu} thua={thua}")
hong = 1 if (thieu or thua) else 0


def dem_kill(src):
    t = ast.parse(src)
    fns = {n.name: n for n in t.body if isinstance(n, ast.FunctionDef)}
    cs = fns["_con_song"]
    goi = {c.func.id for c in ast.walk(cs) if isinstance(c, ast.Call) and isinstance(c.func, ast.Name) and c.func.id in fns}
    def k(f):
        return sum(1 for c in ast.walk(f) if isinstance(c, ast.Call) and ast.unparse(c.func) == "os.kill")
    return k(cs) + sum(k(fns[g]) for g in goi)


def kiem_th(r, nhan, tieu, loai, thu_tu, a1=True):
    if r[0] != "TH":
        return f"{r[0]}"
    n, t, lo = AW.tach(r[1])
    if a1 and n is not None and n != nhan and thu_tu.index(n) < thu_tu.index(nhan):
        return None
    if n != nhan or (tieu and t != tieu) or (loai and not lo.startswith(loai)):
        return f"lech {n}/{t}/{lo[:40]}"
    return None


bang_out = []
for idx, (ten, (caps, kv)) in enumerate(sorted(V.items())):
    moi = SRC
    ly = []
    for neo, thay in caps:
        if SRC.count(neo) != 1:
            ly.append(f"neo xuat hien {SRC.count(neo)} lan")
        moi = moi.replace(neo, thay, 1)
    if moi == SRC:
        ly.append("giong het ung vien")
    lp = TAM / f"launcher_e_{idx:03d}.py"
    lp.write_text(moi, encoding="utf-8")
    try:
        compile(moi, str(lp), "exec")
    except SyntaxError as e:
        ly.append(f"khong bien dich: {e}")
    kq = {}
    if not ly:
        m = AW.nap(lp)
        loai_kv = kv[0]
        cac_g = [kv] if loai_kv in ("giet", "vo_can") else (kv[1] if loai_kv == "gop" else [])
        cac_b8 = list(kv[1]) if loai_kv == "b8" else (kv[2] if loai_kv == "gop" else [])
        for g in cac_g:
            _k, ca, nhan, tieu, loai = g
            helper = m._cs_chay_t156 if ca == T156 else m._cs_chay_t157
            thu_tu = AW.NHAN156 if ca == T156 else ["B3b-giet-cay"]
            a1 = AW.chay(getattr(m, ca))
            a2 = AW.chay(lambda: helper(m._tai_launcher_thu(), noi=[nhan]))
            w1 = AW.chay(lambda: helper(m._tai_launcher_thu(), chay=[nhan]))
            cham = [0]
            g_exit = m._CsSeam.__exit__

            def dem_exit(self, *a, _g=g_exit):
                cham[0] += self.n_stat + self.n_exists + self.n_doc + self.n_kill
                return _g(self, *a)
            m._CsSeam.__exit__ = dem_exit
            w0 = AW.chay(lambda: helper(m._tai_launcher_thu(), chay=[nhan], noi=[nhan]))
            m._CsSeam.__exit__ = g_exit
            kq[ca] = {"A1": a1, "A2": a2, "W1": w1, "W0": w0, "W0_cham": cham[0]}
            if _k == "giet":
                x = kiem_th(a1, nhan, tieu, loai, thu_tu)
                if x:
                    ly.append(f"A1 {x}")
                x = kiem_th(w1, nhan, tieu, loai, thu_tu, a1=False)
                if x:
                    ly.append(f"W1 {x}")
                if w0[0] != "song" or cham[0] < 1:
                    ly.append(f"W0 {w0[0]} cham={cham[0]} (CHUA CO CHOT NGUOC)")
            else:  # đỏ vô can theo thiết kế ở A1, W1, W0
                for nm, r in (("A1", a1), ("W1", w1), ("W0", w0)):
                    if r[0] != "VO_CAN":
                        ly.append(f"{nm} {r[0]} (ky vong VO_CAN)")
        for ca_ngan, loai in cac_b8:
            r = AW.chay(getattr(m, B8[ca_ngan]))
            kq[ca_ngan] = r
            if r[0] != "TH" or not r[1].startswith(f"{B8_TEN[ca_ngan]} {loai}"):
                ly.append(f"{ca_ngan} {r[0]} {r[1][:60]} (ky vong {loai})")
        if loai_kv == "song":
            for ca in (T156, T157):
                r = AW.chay(getattr(m, ca))
                kq[ca] = r
                if r[0] != "song":
                    ly.append(f"{ca[:4]} {r}")
            ghi, loi = AW.quan_sat(m)
            # attempt 2: doi_chieu cua AW tra them tap THUA (VERDICT luot 1, D65) — doi chung song phai khong thieu, khong thua
            thieu_d, thua_d, sai_d = AW.doi_chieu(ghi)
            kq["D"] = {"thieu": thieu_d, "thua": thua_d, "order_sai": sai_d}
            if thieu_d or thua_d or sai_d or loi:
                ly.append("D khong xanh")
            if ten == "song_ba_errno":   # nhân chứng dương (E) mục 5
                def thu(mm):
                    with mm._CsSeam([__import__("os").getpid()], stat=OSError(errno.ENOMEM, "ENOMEM")):
                        return AW.chay(lambda: print(mm._tai_launcher_thu()._con_song(__import__("os").getpid())) or None)
                r_bt, r_uv = thu(m), thu(AW.nap(DEV / "launcher.py"))
                kq["nhan_chung"] = {"bien_the": r_bt, "ung_vien": r_uv}
                if not (r_bt[0] == "VO_CAN" and "Errno 12" in r_bt[1] and r_uv[0] == "song"):
                    ly.append(f"nhan chung duong sai {r_bt} {r_uv}")
            else:
                n_uv, n_bt = dem_kill(SRC), dem_kill(moi)
                kq["nhan_chung"] = {"os.kill ung_vien": n_uv, "os.kill bien_the": n_bt}
                if n_uv == n_bt:
                    ly.append("nhan chung duong: so os.kill khong khac")
    hang = "DAT" if not ly else "DO"
    hong += hang != "DAT"
    nhom_ten = "DS-E-HANG-MUC" if ten in ds["DS-E-HANG-MUC"][1] else "DS-E-KHAC"
    rec = {"ten": ten, "ten_muc6": ten, "nhom": nhom_ten, "cap": caps, "ky_vong": kv, "hang": hang, "ly_do": ly, "kq": kq}
    bang_out.append({k: rec[k] for k in ("ten", "ten_muc6", "nhom", "cap", "ky_vong")})
    print(json.dumps({k: rec[k] for k in ("ten", "nhom", "ky_vong", "hang", "ly_do", "kq")}, ensure_ascii=False, default=str), flush=True)
if BANG_RA:
    BANG_RA.write_text(json.dumps(bang_out, ensure_ascii=False, indent=1), encoding="utf-8")
print(f"TONG (E): {len(V) - hong + (1 if (thieu or thua) else 0)}/{len(V)} dat; KET LUAN: {'DAT' if hong == 0 else 'DO'} hong={hong}")
sys.exit(1 if hong else 0)
