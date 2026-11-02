# Cross-review DOC LAP — PR ducthangho/tra-luat#832 (packet #831, wp831 r4 / g4 (RG-NO-SAU-802 — cong thuc rg chon ban chay duoc, docs doctor, tai sinh manifest)) — cham HEAD DA MERGE

## Vi sao co luot nay
Ho so land cua PR #832 bi ha `landed: true -> false` o #748 r24 (lo A): bang chung reviewer cu khong do duoc ho model.
Dieu kien mo lai: MOT lan approve DOC LAP, hoan tat, tren DUNG `51ae5c095972611d2c6045bd81786a4fc7e9ca62`. Luot NAY la lan ay. Ban la Codex, khac ho
voi executor (Claude). Dung tim doc verdict cu cua PR nay (neu thay trong cay) — tu do tu dau.

## Doi tuong
- `reviewed_sha`: `51ae5c095972611d2c6045bd81786a4fc7e9ca62` (head da merge). Diff can cham: `diff.patch` = `git diff 6b641ca2a2b889c9f43eec58bae47a00a80373cd 51ae5c095972611d2c6045bd81786a4fc7e9ca62`; `numstat.txt`.
- Dac ta dong bang: `SPEC.md` (sha256 `5caec680395ae3dbe673091153e917feb4262a69142f36e54c63a2260d48bdad` — tu do lai bang `sha256sum SPEC.md`).
- No da co quyet dinh chu kho, KHONG tinh la finding mo: (xem SPEC.md muc ngoai pham vi).
- Hai commit cuoi `9385ad2` (F05 — co lap fixture batch khoi installer that) va `51ae5c0` (handoff) la phan sau luot Codex 6; kiem rieng. Lop loi tai phat qua cac luot: dau danh dau Python ke thua (F03/F04: `--bat-buoc`, `exec`, `bash -a`/`SHELLOPTS=allexport`) — liet ke het duong vao truoc, dung chi kiem duong da biet.

## Nhiem vu
1. Moi tieu chi nghiem thu trong SPEC.md: dat hay khong, bang LENH CHAY DUOC trong `cay-kho/` tai `51ae5c095972611d2c6045bd81786a4fc7e9ca62`.
2. Moi khang dinh co so / SHA / ten ca / dieu kien trong diff (code, comment, changelog, handoff): do lai. Danh sach ban
   tu lap se thieu — ghi ro cach ban tim.
3. Chay bo test cua write set: python3 .claude/dev/launcher_test.py ; python3 ops/cong_cu_test.py ; python3 scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json (doi ok=true, expected==checked). Ghi N/M cua tung bo; ca BO QUA ghi rieng.
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
dong 1 `verdict: approve` hoac `verdict: changes_requested`; dong 2 `reviewed_sha: 51ae5c095972611d2c6045bd81786a4fc7e9ca62`;
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
Moi khang dinh do TAI `51ae5c095972611d2c6045bd81786a4fc7e9ca62` — dung lay master hien tai lam chuan. Thu dinh danh tep la SHA, khong phai ten nhanh.
`cay-kho/` la cay day du, KHONG shallow, HEAD detached dung `51ae5c095972611d2c6045bd81786a4fc7e9ca62`, moi nhanh o `refs/remotes/origin/*`, `core.abbrev=7`.
