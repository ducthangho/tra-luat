Bạn là REVIEWER ĐỘC LẬP (lượt 8) cho PR #690 của kho ducthangho/tra-luat — packet #671 `WINDOWS-BASH-NEN-ESCAPE`. Phiên MỚI, READ-ONLY với kho. Cùng họ Claude với executor ⇒ `advisory_review`, nhãn tối đa `same_provider_approved`; land vẫn cần `human_audited`. TỰ đọc spec/diff, TỰ chạy lại mọi phép đo (protocol §8), không tóm tắt lời khai executor.

## Hiện vật (trong thư mục làm việc `$R`)
- `kho.git` (bare, từ kho cục bộ) và `cay-kho/` detached tại **reviewed_sha = `02d169f`** (commit ký CỤC BỘ, chưa push; SHA đầy đủ: `git -C cay-kho rev-parse HEAD`). Chuỗi: `302a15d` (vá 7, review lượt 7) → `abc0339` (merge master `577d7b9`, ĐÃ push, CI xanh) → `02d169f` (vá 8).
- Mốc: `abc0339` (head lượt trước trên GitHub) và **master `577d7b9`** (merge-base; trần ~420 dòng thêm so master — head khai +420/−42). Dựng bản sao nền: `git clone -q kho.git tam/nen && git -C tam/nen checkout -q --detach <sha>` — hai vế trong CÙNG MỘT lệnh.
- `SPEC-WINDOWS-BASH-NEN-ESCAPE-r1.md` (sha256 phải `18504ced1549cbe62816f067b6ed16f36c12292820c8204cb6085a9c39e80b88`), `LEASE-g4.yaml` (hiện hành; write set `ops/bash_nen.py` + `ops/cong_cu_test.py`; chồng có duyệt với #748).
- Lượt trước: `luot7/VERDICT.md` + `luot7/HINT.patch` (CHÍNH — vá 8 áp HINT này), `luot6/`, `luot5/`. `HANDOFF_WINDOWS_6248128895.md` — số đo Windows thật (giả thuyết B, `protectNTFS`).
- `bao-cao-va-luot8/` — lời khai executor vòng 8. **Nguồn gốc:** bộ lọc an toàn chặn một phản hồi, CLI chuyển sang `claude-opus-4-8` (153/167 lượt). Soát lời khai kỹ hơn thường.
- Diff: `git -C cay-kho diff abc0339 02d169f -- ops/` (vá 8) và `git -C cay-kho diff 577d7b9 02d169f` (toàn PR; chỉ 2 tệp).
- Đọc trong `cay-kho/`: `CLAUDE.md` (bài học: đột biến trên BẢN SAO TẠM, `.pyc`, tín dụng giả, lời khai rộng hơn phép đo, vá đúng chỗ rồi bỏ sót đường thứ ba), `docs/PROTOCOL_DA_PHIEN.md` §8 §13.

## Quyết định chủ kho (đừng hỏi lại, nhưng ĐO)
- Trần ~420 dòng thêm; reviewer lượt này theo chỉ thị chủ kho là Sonnet 5.5, review THEO PHÂN LỚP.
- Nghiệm thu Windows KHÔNG ĐO ĐƯỢC ở đây (chủ kho: "Chỉ chạy tại máy") — phân hạng theo spec, không đòi vá bằng mã.
- Tên ca `t60`–`t64` lệch spec ⇒ khai ở PR, không đổi tên.

## Luật cứng
- KHÔNG sửa `cay-kho/`/`kho.git`. Mọi thử nghiệm trên bản sao trong `$R/tam/`; `TMPDIR=$R/tam`, `PYTHONDONTWRITEBYTECODE=1`, xoá `__pycache__` trước mỗi lượt.
- KHÔNG push, KHÔNG mạng GitHub, KHÔNG CI, KHÔNG ghi ngoài `$R`.
- `python3.12` đo chính. Pha ca như CI: `CONG_CU_TEST_BAN_KINH=manh python3.12 ops/cong_cu_test.py` (~6 phút) ở (a) `PYTHONUTF8=1 PYTHONIOENCODING=utf-8` và (b) `LC_ALL=C PYTHONUTF8=0 PYTHONIOENCODING=ascii` (qua `__main__` ⇒ đi nhánh phóng lại thật). Bán kính đột biến: chạy các đột biến liên quan bằng `_do_mot`/`_ket_luan_ban_ghi` CỦA tệp (nạp importlib, chạy `-X utf8`), không cần trọn 416.
- Phần giết tiến trình/Job Object/ABI: CHẠY ca/đột biến có sẵn, mô tả bằng lời thay vì tự soạn mã khai thác (lượt trước bộ lọc nội dung đã chặn executor).
- Ghi `$R/out/VERDICT.md` TĂNG DẦN (container có thể khởi động lại); điền dòng `verdict:` ngay khi có kết luận. Trần 4 giờ.

## Việc
1. **ĐỐI CHIẾU THEO LỚP**: mỗi lớp của `luot7` (P2 nghiệm thu Windows, P3 TU-PHONG-LAI (e), P4 CA-KHOA-T64-TREO, P4 DO-GIA-DOC-DIA-CHI-TUY-Y, P4 LOI-KHAI, P4 TRAN-DONG, P4 TEN-CA) + hai việc mới (cờ `protectNTFS` của `t49`, đối chứng (0) của `t63`): nhãn `ĐÃ VÁ THẬT` / `VÁ HỜ` / `VÁ SINH LỖI MỚI` / `CHƯA VÁ`, kèm lệnh + output.
2. **SĂN ĐỘT BIẾN SỐNG SÓT** ≥ 6 hướng độc lập trên các chốt mới/sửa của vá 8 — mỗi hướng lệnh + output + `LỖI | KHÔNG PHẢI LỖI | KHÔNG ĐO ĐƯỢC`. Ca đích phải ĐỎ bằng tín hiệu chốt (`TinHieuChotCa`/`bang`), không lỗi vô can (tín dụng giả).
3. **BẢNG ĐO**: đo lại lời khai executor/commit (+420/−42 so `577d7b9`; pha ca 60/60 (a)(b); 9/9 đột biến; ruff F = nền {F401 `ast` bash_nen, F841 `ci`}).
4. Mỗi finding đủ §8: vá ở đâu / vá thế nào / ca khoá + đột biến phải chết / bản vá có thể đẻ ra gì; kèm hunk trong `$R/out/HINT.patch` (`patch -p0` từ gốc cây, áp lên `02d169f`; tự kiểm dry-run rc=0 trên clone mới; nêu dòng thêm sau áp so `577d7b9` — vượt 420 thì nói rõ để chủ kho quyết).

## Đầu ra `$R/out/VERDICT.md`
```
verdict: approve | changes_requested | blocked
reviewed_sha: <SHA đầy đủ 02d169f>
provider: claude
role: reviewer
review_kind: advisory_review
model_reviewer_identity: <tự khai; điều phối đối chiếu modelUsage>
independent_from_executor_session: true
assurance: same_provider_approved (chỉ khi approve) | review_deferred
review_axes: [spec, standards_security]
## SNAPSHOT ĐẦU/CUỐI
## ĐỐI CHIẾU THEO LỚP
## BẢNG SĂN
## BẢNG ĐỘT BIẾN
## BẢNG ĐO
### <SLUG> [P0..P4] <tiêu đề>
## HINT.patch — tự kiểm
## KHÔNG ĐO ĐƯỢC
```
Hạng: P0/P1 chặn land; P2 phải vá trước land; P3 lời khai lệch phép đo; P4 vặt. `approve` chỉ khi không còn P0–P3 mở NGOÀI P2 nghiệm thu Windows (ghi rõ nó vẫn mở, không vá được ở Linux).
Khi xong in đúng một dòng: `XONG verdict=<...> P0=<n> P1=<n> P2=<n> P3=<n> P4=<n> hint_dry_run_rc=<rc>`.
