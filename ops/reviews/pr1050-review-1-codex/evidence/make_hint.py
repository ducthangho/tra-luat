from pathlib import Path
import difflib
relative='ops/land/pr1041-wp1037-land-evidence.yaml'
old=(Path('cay-kho')/relative).read_text();new=old
pairs=[
 ("name: 'ci.yml workflow_dispatch runner_set=windows-only tren head cuoi'", "name: 'ci.yml workflow_dispatch (nhan windows-latest do tu jobs) tren head cuoi'"),
 ('2 failure (gate-packet-loop, gate-cong-cu windows-latest 0, buoc G5 probe: runner thieu shellcheck — goc loi ops/cai_cong_cu.sh, tach packet #1045)', '2 failure (gate-packet-loop: G5 probe ban ke cong cu; gate-cong-cu windows-latest 0: G5 manh ban kinh dot bien)'),
 ('log khong luu trong kho).', 'log khong luu trong kho). Thuat_lai — executor khai input runner_set=windows-only va nguyen nhan runner thieu shellcheck, goc loi ops/cai_cong_cu.sh, tach packet #1045; KHONG_DO_DUOC tu readback run/jobs da luu, khong co log chan doan hoac readback inputs trong provenance.'),
 ('DA NHA bang RUT HAN (khong bia mo — lease con han, khong co lease ke', 'DA RUT HAN; CHUA NHA tai moc ghi so 17:37Z (khong bia mo — lease con han, khong co lease ke'),
 ('khong roi vao rc=8.\n', 'khong roi vao rc=8. Chi sau 17:53Z moi do lai ai-dang-giu tren du ref de xac nhan da nha; chua co phep do ay trong ho so nay.\n'),
 ('(2) lease da nha bang rut han (17:53Z);', '(2) lease CHUA nha tai moc ghi so 17:37Z, da rut han ve 17:53Z, can do lai ai-dang-giu sau han;'),
 ('VA (5) chu kho ghi duyet ben neo 9146632.', 'VA (2) do ai-dang-giu sau 17:53Z tren du ref, khong con wp1037-r1-g1-claude; VA (5) chu kho ghi duyet ben neo 9146632.')]
for a,b in pairs:
 assert new.count(a)==1,(a,new.count(a))
 new=new.replace(a,b,1)
Path('HINT.patch').write_text(''.join(difflib.unified_diff(old.splitlines(True),new.splitlines(True),fromfile=relative,tofile=relative)))
Path('evidence/hint-land-evidence.yaml').write_text(new)
