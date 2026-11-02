# Cross-review DOC LAP — PR ducthangho/tra-luat#823 (packet #802, wp802 r1 / g1 (RG-DA-NEN — doctor im lang khi rg dau PATH hong; hook)) — cham HEAD DA MERGE

## Vi sao co luot nay
Ho so land cua PR #823 bi ha `landed: true -> false` o #748 r24 (lo A): bang chung reviewer cu khong do duoc ho model.
Dieu kien mo lai: MOT lan approve DOC LAP, hoan tat, tren DUNG `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`. Luot NAY la lan ay. Ban la Codex, khac ho
voi executor (Claude). Dung tim doc verdict cu cua PR nay (neu thay trong cay) — tu do tu dau.

## Doi tuong
- `reviewed_sha`: `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` (head da merge). Diff can cham: `diff.patch` = `git diff fb490a7c3fa2992c6f4635ed091dafa813df2fe7 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`; `numstat.txt`.
- Dac ta dong bang: `SPEC.md` (sha256 `e4fd84e1f079d0ac4841a145d078473576af3a3e4e2f593e4f3e40c5de7200e0` — tu do lai bang `sha256sum SPEC.md`).
- No da co quyet dinh chu kho, KHONG tinh la finding mo: cong thuc rg Linux/macOS + docs/GOI_AGENT_DA_NEN.md ma 12 + manifest (packet #831); Windows t23/t49/t217 (#748).
- Spec cho phep vuot tran 6 tep / 450 dong them (diff that 482 dong them) theo quyet dinh chu kho; kiem diff co dung write set 6 tep cua spec khong.

## Nhiem vu
1. Moi tieu chi nghiem thu trong SPEC.md: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` tai `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`.
2. Moi khang dinh co so / SHA / ten ca / dieu kien trong diff (code, comment, changelog, handoff): do lai. Danh sach ban
   tu lap se thieu — ghi ro cach ban tim.
3. Chay bo test cua write set: python3 .claude/dev/launcher_test.py ; python3 ops/cong_cu_test.py ; python3 .claude/dev/launcher_test.py --dot-bien (neu kip). Ghi N/M cua tung bo; ca BO QUA ghi rieng.
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
dong 1 `verdict: approve` hoac `verdict: changes_requested`; dong 2 `reviewed_sha: 5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`;
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
Moi khang dinh do TAI `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456` — dung lay master hien tai lam chuan. Thu dinh danh tep la SHA, khong phai ten nhanh.
`cay-kho/` la cay day du, KHONG shallow, HEAD detached dung `5c6c7a8ac0dc1b968cfda9d11065e5f3e8713456`, moi nhanh o `refs/remotes/origin/*`, `core.abbrev=7`.
