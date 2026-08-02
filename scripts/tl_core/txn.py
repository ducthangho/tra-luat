# -*- coding: utf-8 -*-
"""Helper 1 — KẾT LUẬN GIAO DỊCH (Pha 1-0, §5 Mẫu A + §6.1 kế hoạch AUDIT_XAC_MINH 31-07).

Mẫu lỗi A chiếm 13/34 mục sổ audit (GATE-01, ING-03/05, PRO-01/06/07, RAS-04/05/10/11/12…). Dấu hiệu
chung LUÔN là một trong hai:

  * `ok` được **GÁN** thay vì được **TÍNH** (`out = {..., "ok": True, ...}` bất kể bước con ra sao);
  * `ok` được tính từ **HÌNH DẠNG** ("response có trường `fileId`") thay vì từ **KẾT QUẢ** ("bước
    register báo `upsert_done`"). ING-03 là bản mẫu: `ok:false` + `upsert_done:false` mà có `fileId`
    thì caller vẫn ĐI TIẾP.

Vá từng `if` rời thì mục thứ 14 tái sinh ở chỗ khác — nên hợp đồng nằm MỘT CHỖ, ở đây. Các slice sau
**DÙNG** module này, **không SỬA** nó.

Hợp đồng (§6.1):
  1. nhận danh sách `(tên_bước, kết_quả, bắt_buộc?)` theo ĐÚNG thứ tự đã chạy;
  2. `ok` được TÍNH, không bao giờ được GÁN;
  3. bước bắt buộc hỏng ⇒ CHẶN mọi mutation PHÍA SAU (ném `TxnBlocked`), không chỉ đánh dấu;
  4. `rc` dẫn xuất từ `ok`, không đặt tay;
  5. luôn phát ra *bước nào hỏng* + *ĐÃ GHI ĐƯỢC GÌ RỒI* — người vận hành cần biết phải đi dọn gì.

Điều 5 không phải trang trí: PRO-01 tháo con trỏ registry sau khi bước xoá đã hỏng, và vì `rc=0` nên
không ai biết có tài sản mồ côi. Bản kê `wrote` là thứ duy nhất chỉ được đường về.
"""
from __future__ import annotations

from typing import Any, Iterable

# Không import gì từ tl_core khác: module này là LÕI, mọi tầng trên đều được phép dùng.

RC_OK = 0
RC_FAIL = 2          # rc thất bại chuẩn của tl (giữ nguyên quy ước sẵn có, không phát minh mã mới)


class TxnBlocked(Exception):
    """Ném khi caller định chạy một mutation SAU một bước bắt buộc đã hỏng.

    Là EXCEPTION chứ không phải cờ trả về, có chủ đích: cờ thì caller quên kiểm là lại fail-open đúng
    kiểu cũ; exception thì bỏ quên là lệnh chết to, không phải chết im.
    """

    def __init__(self, op: str, blocking_step: str, attempted: str):
        self.op, self.blocking_step, self.attempted = op, blocking_step, attempted
        super().__init__(f"{op}: bước '{attempted}' bị CHẶN vì bước bắt buộc '{blocking_step}' đã hỏng")


def step_result_ok(result: Any, *, require_keys: Iterable[str] = ()) -> tuple[bool, str]:
    """Vị ngữ "kết quả DƯƠNG" — FAIL-CLOSED. Trả `(ok, lý_do_hỏng)`.

    Luật, theo đúng thứ tự:
      * `True` ⇒ dương. `False`/`None` ⇒ âm.
      * `dict`: PHẢI có khoá `ok` và `ok` phải truthy. **Thiếu khoá `ok` = ÂM**, không phải "chắc là ổn"
        — đây chính là chỗ ING-03 chết: suy ra thành công từ sự CÓ MẶT của một trường khác.
      * mọi hình dạng khác (str/int/list/object) ⇒ ÂM: không chứng minh được thì không tính là được.
      * `require_keys`: sau khi `ok` dương, MỌI khoá liệt kê phải có mặt VÀ truthy trong dict. Đây là
        chỗ khai "đủ marker" (`organize_done`, `rename_done`, `upsert_done`, `file`…).
    """
    if result is True:
        return True, ""
    if result is False or result is None:
        return False, "KET_QUA_AM" if result is False else "KHONG_CO_KET_QUA"
    if not isinstance(result, dict):
        return False, f"HINH_DANG_LA_{type(result).__name__.upper()}_KHONG_CHUNG_MINH_DUOC"
    if "ok" not in result:
        return False, "THIEU_TRUONG_OK"
    if not result.get("ok"):
        return False, str(result.get("error") or result.get("step") or "OK_FALSE")
    _thieu = [str(k) for k in require_keys if not result.get(k)]
    if _thieu:
        return False, "THIEU_MARKER:" + ",".join(_thieu)
    return True, ""


class Txn:
    """Sổ ghi giao dịch: nhận bước theo ĐÚNG thứ tự đã chạy, kết luận được TÍNH ra từ sổ.

    Khuôn dùng:

        t = Txn("profile-file-remove")
        t.record("nlm_source_delete", r1, mutating=True, wrote={"nlm_source_id": sid})
        t.guard("reg_delete")                 # ném TxnBlocked nếu bước bắt buộc trước đó đã hỏng
        t.record("reg_delete", r2, mutating=True, wrote={"registry_rows": ids})
        out = {**plan, **t.conclude()}        # KHÔNG có `"ok": True` ở đâu trong câu này
        return t.rc()
    """

    def __init__(self, op: str):
        self.op = str(op or "")
        self.steps: list[dict] = []

    # ── ghi sổ ────────────────────────────────────────────────────────────────
    def record(self, name: str, result: Any, *, required: bool = True,
               require_keys: Iterable[str] = (), mutating: bool = False,
               wrote: Any = None) -> bool:
        """Ghi một bước ĐÃ CHẠY. Trả `ok` của riêng bước đó (tiện cho nhánh rẽ tại chỗ).

        `mutating=True` + bước DƯƠNG ⇒ `wrote` vào bản kê "đã ghi được gì rồi". Bước mutating mà ÂM thì
        KHÔNG vào bản kê: ta không chứng minh được nó đã ghi (và cũng không chứng minh được nó chưa ghi —
        chỗ đó ghi `uncertain`, xem `conclude`).
        """
        _ok, _why = step_result_ok(result, require_keys=require_keys)
        _rec = {"step": str(name), "ok": _ok, "required": bool(required), "mutating": bool(mutating)}
        if not _ok:
            _rec["error"] = _why
        if wrote is not None:
            _rec["wrote"] = wrote
        self.steps.append(_rec)
        return _ok

    def skipped(self, name: str, why: str = "KHONG_YEU_CAU") -> None:
        """Bước KHÔNG được yêu cầu chạy (vd `--delete-nlm` tắt). Không phải hỏng, không phải thành công.

        Ghi ra để bản kê đọc được: "registry chỉ được tháo khi các thao tác ĐƯỢC YÊU CẦU TRƯỚC ĐÓ đã
        thành công" — muốn nói được câu đó thì phải phân biệt được *bỏ qua* với *hỏng*.
        """
        self.steps.append({"step": str(name), "ok": None, "skipped": True, "why": str(why)})

    # ── tra sổ ────────────────────────────────────────────────────────────────
    def first_failure(self) -> dict | None:
        """Bước BẮT BUỘC hỏng ĐẦU TIÊN (theo thứ tự chạy) — hoặc None."""
        for s in self.steps:
            if s.get("required") and s.get("ok") is False:
                return s
        return None

    def can_mutate(self) -> bool:
        return self.first_failure() is None

    def guard(self, attempted: str) -> None:
        """Gọi NGAY TRƯỚC mỗi mutation. Ném `TxnBlocked` nếu một bước bắt buộc trước đó đã hỏng.

        Đây là điều 3 của hợp đồng: CHẶN, không phải đánh dấu rồi vẫn chạy.
        """
        _f = self.first_failure()
        if _f is not None:
            raise TxnBlocked(self.op, str(_f.get("step")), str(attempted))

    def ok(self) -> bool:
        """`ok` được TÍNH: mọi bước bắt buộc phải DƯƠNG. Không có bước nào ⇒ không có gì được chứng minh."""
        _req = [s for s in self.steps if s.get("required")]
        return bool(_req) and all(s.get("ok") is True for s in _req)

    def rc(self) -> int:
        """`rc` DẪN XUẤT từ `ok`, không đặt tay."""
        return RC_OK if self.ok() else RC_FAIL

    def wrote(self) -> list[dict]:
        """Bản kê ĐÃ GHI ĐƯỢC GÌ RỒI — chỉ những mutation ĐÃ CHỨNG MINH là thành công."""
        return [{"step": s["step"], "wrote": s["wrote"]}
                for s in self.steps if s.get("mutating") and s.get("ok") is True and "wrote" in s]

    def uncertain(self) -> list[dict]:
        """Mutation ÂM: không chứng minh được đã ghi, cũng không chứng minh được CHƯA ghi.

        Tách riêng khỏi `wrote` vì hai việc dọn khác nhau: `wrote` là "đã ghi, cần cân nhắc hoàn tác";
        `uncertain` là "phải đi KIỂM tận nơi trước khi làm gì".
        """
        return [{"step": s["step"], "error": s.get("error", "")}
                for s in self.steps if s.get("mutating") and s.get("ok") is False]

    def conclude(self, **extra: Any) -> dict:
        """Envelope kết luận. `ok` ở đây LUÔN là `self.ok()` — caller không có đường gán đè.

        `extra` chỉ để đính dữ liệu nghiệp vụ; khoá `ok`/`rc` trong `extra` bị BỎ QUA có chủ đích, để
        không ai vô tình dựng lại đúng cái bệnh `"ok": True` gán cứng mà module này sinh ra để diệt.
        """
        _f = self.first_failure()
        out = {k: v for k, v in extra.items() if k not in ("ok", "rc")}
        out["ok"] = self.ok()
        out["txn"] = {
            "op": self.op,
            "steps": list(self.steps),
            "failed_step": (_f or {}).get("step"),
            "failed_error": (_f or {}).get("error"),
            "wrote": self.wrote(),
            "uncertain": self.uncertain(),
        }
        if _f is not None:
            out.setdefault("step", f"{self.op}:{_f.get('step')}")
            out.setdefault("error", _f.get("error") or "TXN_STEP_FAILED")
        return out
