# Cross-review DOC LAP — PR ducthangho/tra-luat#792 (packet #484, wp484 r8 / g7 (AUTH — reroute Codex credential path, refresh khong gian doan)) — cham HEAD DA MERGE

## Vi sao co luot nay
Ho so land cua PR #792 bi ha `landed: true -> false` o #748 r24 (lo A): bang chung reviewer cu khong do duoc ho model.
Dieu kien mo lai: MOT lan approve DOC LAP, hoan tat, tren DUNG `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`. Luot NAY la lan ay. Ban la Codex, khac ho
voi executor (Claude). Dung tim doc verdict cu cua PR nay (neu thay trong cay) — tu do tu dau.

## Doi tuong
- `reviewed_sha`: `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b` (head da merge). Diff can cham: `diff.patch` = `git diff d347d426334bbe1bbb1161184ab0acffee9be054 288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`; `numstat.txt`.
- Dac ta dong bang: `SPEC.md` (sha256 `4a512dd38721c3c4eec7978489ba06485feab32f94a0c5637a085d6c694ba38c` — tu do lai bang `sha256sum SPEC.md`).
- No da co quyet dinh chu kho, KHONG tinh la finding mo: codex-auth-json-khong-cas (#824), codex-rejected-state-khong-ghi-duoc (#825), launcher-resume-checkpoint-khong-rang-buoc-luot-goc (#826).
- Hai commit cuoi `bf10fab` (merge master) va `288ad3e` (runner dot bien harness nhan ca dich tu bo qua la KHONG DO DUOC, `.claude/dev/launcher_test.py` +18/-3) CHUA tung duoc Codex review: kiem rieng hai commit nay.

## Nhiem vu
1. Moi tieu chi nghiem thu trong SPEC.md: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` tai `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`.
2. Moi khang dinh co so / SHA / ten ca / dieu kien trong diff (code, comment, changelog, handoff): do lai. Danh sach ban
   tu lap se thieu — ghi ro cach ban tim.
3. Chay bo test cua write set: python3 .claude/dev/launcher_test.py ; python3 .claude/dev/codex_cred_test.py ; python3 .claude/dev/launcher_test.py --dot-bien (neu kip thoi gian). Ghi N/M cua tung bo; ca BO QUA ghi rieng.
4. Dot bien: chay tren BAN SAO TAM ngoai `cay-kho/` (khong sua cay that). Moi chot moi cua diff phai co it nhat mot dot bien
   lam ca dich do DUNG LY DO (assertion cua chinh ca, khong phai loi vo can).
5. Huong thu can soan noi dung nhay cam (vd duong dan thoat khoi cay thu muc, credential gia dang that) thi MO TA BANG
   LOI trong VERDICT, khong tu soan.

## Bay moi truong da biet (ghi KHONG DO DUOC kem ly do, dung doc thanh hoi quy)
- Sandbox Codex co the de lai `/tmp/.git` rong; khi ay cac ca dat Codex home duoi `/tmp` do vi "Codex home is inside a
  repository". Hoi `ls -d /tmp/.git` truoc khi ket luan.
- Khong co mang. Ca can mang/GitHub that ghi KHONG DO DUOC.

## Ghi VERDICT.md TANG DAN (o thu muc hien tai, ngoai `cay-kho/`)
Tao ngay khi bat dau (dong 1 `verdict: dang_lam`), noi them sau moi huong thu. Cuoi cung:
dong 1 `verdict: approve` hoac `verdict: changes_requested`; dong 2 `reviewed_sha: 288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`;
dong 3 `spec_sha256: <tu do>`; mot dong `Ket qua: <n> P0, <n> P1, <n> P2, <n> P3.`

Cau truc:
```
## BANG NGHIEM THU   | tieu chi | lenh | output | dat? |
## BANG DO           | khang dinh | diff khai | do duoc (lenh) | khop? |
## BANG TEST         | bo | N/M | bo qua |
## BANG SAN          (>= 6 huong DOC LAP, moi huong co LENH + OUTPUT THAT; ket luan LOI | KHONG PHAI LOI | KHONG DO DUOC)
### <slug>  [P0|P1|P2|P3]  <tieu de>
TEP/DONG: / VAN DE: / DA THU NGHIEM: / DO TIN:
```
P0/P1 = sai hanh vi hoac khang dinh sai su that do duoc; P2 = khai rong hon phep do / thieu dieu kien / chot thieu rang;
P3 = dien dat. "approve" khong co output that la khong hop le. Goi y va (neu co) vao `HINT.patch` (patch -p0 tu `cay-kho/`).

## Rang buoc
CHI DOC + DO. KHONG sua `cay-kho/`, KHONG push, KHONG goi mang, KHONG dung credential that.
Moi khang dinh do TAI `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b` — dung lay master hien tai lam chuan. Thu dinh danh tep la SHA, khong phai ten nhanh.
`cay-kho/` la cay day du, KHONG shallow, HEAD detached dung `288ad3ea79ef94e061b649effe7bee2c7e2a0a9b`, moi nhanh o `refs/remotes/origin/*`, `core.abbrev=7`.
