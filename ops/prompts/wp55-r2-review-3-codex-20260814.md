Ban la phien REVIEWER cho wp55 revision 2 generation 2 (F3-03), repo ducthangho/tra-luat.
Ban KHONG phai Executor, KHONG phai Land Operator, KHONG phai Dispatcher.
KHONG sua file, KHONG push, KHONG merge, KHONG land, KHONG deploy, KHONG goi LIVE.

lease     : wp55-r2-review-3-codex-20260814 · het han 2026-08-14T09:08:40Z (16:08 VN)
            nguon su that la TEP ops/leases/wp55-r2-review-3-codex-20260814.yaml tren
            nhanh claude/ops-publish-qua-git; comment 5288950354 tren #55 chi la ban chieu.
            heartbeat moi 30 phut len #55: lease_id, gio VN, dang do gi, da chay lenh nao.
packet    : #55 · wp55 · revision 2 · generation 2
spec_hash : a05c10f71e205d6268c46c62de9fd2d1cc5f7629b070af69a8e3b4254d782c5c
mission   : #54 revision 6
PR        : #92
reviewed_sha doi: cf39109c9e5167516c53f2071e5fa7ec5c6afff5
base      : fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
provider  : codex — BAT BUOC, executor la claude (§8)
assurance : cross_approved
attempt   : 3/3 — DAY LA LUOT CUOI. Sau luot nay khong con attempt noi dung.

BUOC 0 — fail-closed, lech thi DUNG va bao:
  git rev-parse --is-shallow-repository        # DOI false
      Clone nong lam `git diff` voi base khong chay — generation 2 da chet o dung
      cho nay mot lan. Nong thi `git fetch --unshallow` truoc khi lam bat cu gi.
  head hien tai cua PR #92 phai la cf39109c…   # doi ⇒ dung, xin review lai
  Readback #54 revision 6 · #55 spec_hash a05c10f7…
  Doc rc TRUC TIEP tung lenh — rc cua pipe la rc cua lenh CUOI.

BUOC 0a — KIEM CHINH PROMPT NAY TRUOC KHI TIN NO:
  lease co truong prompt_sha256_required. Bam DUNG TEP NAY, khong phai mot khoi
  trong comment, khong phai doan ban dan lai:
      sha256sum <duong dan tep prompt>
  Lech ⇒ DUNG, bao chu kho, khong tu doan y.
  Ly do co buoc nay: lease #3 ban dau neo mot sha KHONG ung voi bat ky van ban nao
  ton tai — da quet 294.578 cua so 5292-byte tren toan bo comment #54+#55 va 941
  blob cua 3 nhanh, khong cai nao khop. Cong doi mot vat khong co that thi khong ai
  qua duoc, va no dung im lang — do la thu chan wp55 hai ngay.

BUOC 0b — KIEM DUONG GHI VERDICT TRUOC KHI LAM VIEC:
  Do ngay 14-08-2026 tren container Claude Code web:
    - `gh` KHONG co san.
    - api.github.com tra 403 o tang PROXY — 403 ca khi khong gui token. Token tot hay
      xau khong cuu duoc duong nay; dung mat thi gio thay token.
    - api.githubcopilot.com/mcp/ (GitHub MCP Server chinh thuc) CHAY: initialize tra
      HTTP 200 voi `Authorization: Bearer $GITHUB_PAT`, va 401 khi khong token.
  Nen: doc PR/issue va dang verdict bang cong cu MCP github.
  Neu phien cua ban khong co duong nao: NOI NGAY o dau bao cao, xuat verdict ra tep,
  de chu kho dang ho. TUYET DOI khong im lang bo qua buoc ghi verdict — vong 3 da lam
  xong het roi khong ghi duoc, cong suc do coi nhu mat.
  `python .claude/dev/launcher.py doctor` liet ke cong cu dang co.

DOC TRUOC: docs/PROTOCOL_DA_PHIEN.md §8 va §13; body #55 revision 2 (17 acceptance
criteria); hai verdict truoc cua chinh ban:
  https://github.com/ducthangho/tra-luat/issues/55#issuecomment-5281666832
  https://github.com/ducthangho/tra-luat/pull/92#issuecomment-5261240216

BOI CANH — LUOT NAY KHAC HAI LUOT TRUOC:
Luot review #2 cua ban tim ra mot finding CHAN: `cmd_init` ghi thang state `leased`,
nen bat ky ai go duoc `init` deu tu cap cho minh mot lease hop le roi `begin-attempt`
sang `running` — duong vong qua dung cai doctrine "khong tu cap lease", trong khi
acceptance #55 r2 doi chan TU init.
cf39109c LA BAN SUA CHO FINDING DO. No la ma MOI NHAT va IT MAT DOC NHAT trong ca PR.
Viec chinh cua luot nay khong phai ra soat lai nhung cho da duyet, ma la: ban sua ay
co bit THAT khong, hay chi doi cho lo.

Cai da doi o cf39109c (102 dong packet_loop.py · 150 dong test · 14 dong SKILL.md):
  - `init` nay toi `awaiting_lease`, va state do co dich RONG trong CHUYEN_HOP_LE.
  - Duong duy nhat vao `leased` la lenh MOI `record-lease`, doi ba thu: --granted-by
    (KHONG duoc la ten mot provider), dau vet ben de doi chieu, va --expires-utc.
  - Han duoc cuong che CA luc GHI lease LAN moi lan mo luot (`begin-attempt`).
  - `--expires-utc` thieu mui gio bi CHAN chu khong doan.

DO, dung doc bang mat. So nen duoi day da do lai 14-08 tren dung cf39109c va khop:
  python .claude/dev/packet_loop_test.py
      # DOI "nen: 48/48 dat" VA 7 dot bien, moi dot bien giet DUNG ca dich cua no
  python .claude/dev/packet_loop.py doctrine-scan --root .    # DOI rc=0, 4 tep
  python scripts/tl.py --selftest                             # DOI hai so BANG NHAU
  python scripts/tl.py doc-claims-check --strict --json       # DOI flags=0
  python scripts/tl.py release-verify RELEASE_MANIFEST.json --root . --strict --json
  python scripts/tl.py golden-test
  python .githooks/eol_policy.py --all --json                 # DOI violations=0
  release-bundle hai lan + dung bundle tu fbe5ab9e, doi ca ba CUNG sha256

TAM HUONG TAN CONG. 1-4 la MOI cho luot nay (nham vao cf39109c); 5-8 la nhung huong
con de ngo tu luot truoc:

 1. `record-lease` — chot moi tinh, chua ai review dong nao. Chot cot loi la
    `nguoi_cap.lower() in PROVIDERS`. Lop ky tu nao lot? Thu: --granted-by rong /
    chi khoang trang / "Codex" / "codex " co khoang trang duoi / "cödex" hoac ten
    provider gan dau ket hop unicode / chuoi CHUA ten provider nhu "codex-dispatcher"
    hoac "ai-codex-bot". Chieu nguoc lai cung phai thu: co chan OAN mot nguoi that
    ten trung mot phan voi provider khong?
 2. Hai lop kiem han — commit KHAI la doc lap ("hai dot bien han tach roi nhau de
    chung minh hai lop khong phu len nhau"). Kiem that: chung di qua hai duong ma
    khac nhau, hay cung goi mot ham? Bo mot lop thi lop kia con bat khong? Doc ma,
    dung tin loi khai trong commit message.
 3. `awaiting_lease` co dich RONG trong CHUYEN_HOP_LE — do la ca bo chot. Tim lenh
    nao ghi truong `state` truc tiep ma khong di qua bang do: `record-review`,
    `void-attempt`, `record-post`, `transition`, va chinh `record-lease`. MOT cua sot
    lai la lo y het bug goc, chi doi ten. Day dung la bai hoc "canh tung cua la thua"
    ma tep nay tu vien ra — hay kiem xem no co ap dung cho chinh no khong.
 4. `init` ghi de state da co: cf39109c doi state khoi diem tu `leased` sang
    `awaiting_lease`. Ca `init_khong_ghi_de_state_da_blocked` co con do dung thu no
    dinh do khong, hay nay chi con do duong `awaiting_lease` va da thanh ca rong?
 5. finding-id: co duong nao lam hai loi KHAC nhau gop thanh mot ID, hoac mot loi tach
    thanh hai ID, ma may khong thay? Thu slug unicode, rong, cuc dai, trung sau NFC.
    Dac biet: dedup trong-mot-review co lam SOT mot finding that khong?
 6. So comment-id: ma KHAI thang la SO TAY, khong xac minh ton tai. Kiem con cau chu
    nao trong ma hoac trong ba adapter ngu y MANH HON the khong — neu co, do la finding.
 7. `doctrine-scan`: FORBIDDEN_DOCTRINE_PHRASES co DU bon nhom spec doi khong? Chuan
    hoa nay bo ` * _ ~ va so tren van ban logic ca tep. Tim lop ky tu CON LAI lach
    duoc (nhay cong, zero-width, NBSP, HTML entity). Chieu nguoc: co bat OAN adapter
    viet binh thuong khong?
 8. Mo neo SHA: `accepted` nay chi con MOT cua (`record-review --verdict approve`).
    Tim cua thu hai. Thu duyet bang head cu sau khi mo luot moi; `--head-sha` hoa /
    rut gon / khong phai hex.

TUONG TAC VOI MASTER — da do 14-08, van phai tu kiem lai, dung tin loi khai:
  master = b666dedd6, di truoc merge-base fbe5ab9e1 dung 38 commit.
  master DA SUA CLAUDE.md (+49 dong). CLAUDE.md vua nam trong 6 tep write_set vua la
  tep doctrine-scan quet — do la cho hai ben cham nhau.
  Merge thu bang git merge-tree --write-tree: SACH, auto-merging CLAUDE.md, 0 xung dot.
  Nhung merge sach KHONG co nghia doctrine sach: hay chay doctrine-scan tren CAY DA
  MERGE chu khong chi tren nhanh.

KIEM PHAM VI: `git diff --name-status fbe5ab9e cf39109c` phai cho DUNG 6 tep write_set:
  A .claude/dev/packet_loop.py          A .claude/dev/packet_loop_test.py
  A .claude/skills/cross-review/SKILL.md  A .claude/skills/land-packets/SKILL.md
  A .claude/skills/work-packet/SKILL.md   M CLAUDE.md
Manifest/golden/bundled module KHONG duoc doi — kiem bang so, dung bang cam giac.
LUU Y: suite CHUA noi CI (`grep -c packet_loop .github/workflows/ci.yml` = 0) — co y,
hoan sang #52. Nen CI xanh KHONG dong nghia suite xanh; phai tu chay.

GHI VERDICT LEN PR — §13 doi. Khong co `gh` thi di duong MCP github:
  pull_request_review_write  method=create  event=REQUEST_CHANGES | APPROVE  body=…
Moi finding PHAI co finding-id SLUG on dinh (kebab-case) + severity + bang chung chay
duoc. Ghi lai luot review vao state:
  python .claude/dev/packet_loop.py record-review --packet 55 --provider codex \
      --verdict approve|changes_requested|blocked \
      --reviewed-sha cf39109c9e5167516c53f2071e5fa7ec5c6afff5 \
      --finding-id SLUG --finding-desc "..."
Cung dang evidence §7 (schema reviewer) len #55, neo reviewed_sha dung cf39109c….

STOP CONDITIONS:
  head doi ⇒ dung, xin review lai.
  can sua file ⇒ KHONG sua, ghi finding va tra ve executor.
  phat hien cho thay chinh Packet Spec thieu ⇒ verdict blocked + revision, KHONG tu noi.
  cham quota ⇒ ghi ly do allowlist, khong tieu attempt noi dung.
  lease het han (2026-08-14T09:08:40Z) ⇒ DUNG, xin lease moi. Khong chay tiep "cho
  xong": mot luot review da tung chay 7 GIO sau khi lease het han vi khong ai doc lai
  cai han — chinh la lo ma cf39109c sinh ra de bit. Dung tai pham no ngay trong luot
  di kiem no.
