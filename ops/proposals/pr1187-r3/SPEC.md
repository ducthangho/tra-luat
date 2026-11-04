# PR1184-MERGE-CONTRACT r3 — Remediation sau advisory 4

packet_id: PR1184-MERGE-CONTRACT
revision: 3

## Trạng thái và các mốc bất biến

ĐỀ XUẤT CHỜ CHỦ KHO DUYỆT; chưa cấp lease, chưa được ghi sản phẩm theo revision này.
Packet Issue #1187; liên quan PR #1184 / Packet #1178 / Mission #1177 bằng dependency,
không sửa Mission plan_hash hoặc tự nhận Mission complete.

- Immutable acceptance base: 1f0941e9bba1d1d517eda4174167b81963c06bd5.
- Continuation source: 29ee9ca74d61544fbddd56c39dabbe194d26408e.
- Continuation tree: 996c6af444aeb22d69587ed7852b78f35102eb9b.
- Frozen r2 spec: 74a0abdb2631ae38f9f76b7426b5e47a3c82ce8f:ops/specs/PR1184-MERGE-CONTRACT-r2.md,
  SHA256 975c5d31be6ec4f26145f14893b5c8f7063e5921d1c6dafdca020f50e795299d.
- Dự kiến generation 4, Executor codex / openai / codex_service / machine, cloud Linux.
- Review class/risk sensitive; primary reviewer human / manual_audit / human,
  độc lập với Executor, assurance human_audited trên exact final head/tree/spec.
- Product PR #1184 giữ head a7b5aedc122575a66280ace3ff7f2567251af8e2; không sửa năm tệp môi trường.

## Objective và lý do checkpoint

Hoàn tất cùng merge contract K1/K4/ADR0063 của r2 và sửa các finding P3 của advisory 4.
Không đổi chuẩn authority, không nới điều kiện merge, không che lỗi bằng mã thoát khác.
Review 4 trả changes_requested, sáu P3, không P0–P2. Executor đã đo actual wp1178 r3,
own r1/r2 qua external K1: ba blob đúng OID/hash đều được nhận trong synthetic rollout graph.
Đó là evidence A2, không chứng minh ADR0063 đã land trên canonical.
Các kiểm chứng còn lại tái hiện H1 benign bị từ chối, docs-crash được tính GIET,
thiếu một input model trả TypeError phụ, và datetime offset biên gây OverflowError.

## Nâng trần đề nghị — cần phê duyệt riêng

nang_tran:
  ai_nang: Chủ kho ducthangho — CHƯA DUYỆT proposal này
  can_cu: Current base diff +936/-9 còn 64 dòng so cap1000; cần thêm ca âm/dương và mutants có controls, không nén/bỏ test để vừa cap.
  tran_cu: 6 effective paths, 5 net product files, 1000 dòng thêm
  tran_moi: 6 effective paths, 5 net product files, 1250 dòng thêm

1250 là hard cap đề nghị, không phải số đo patch đã viết. Vượt phải dừng và trình actual numstat;
không tự tăng trần. Không reset các bộ đếm/historical receipts của r1/r2/g1–g3.

## Effective write set — đúng sáu đường dẫn

1. .claude/dev/packet_loop.py
2. .claude/dev/packet_loop_test.py
3. docs/PROTOCOL_DA_PHIEN.md
4. docs/adr/0063-merge-spec-ref-va-human-audit.md
5. ops/specs/PR1184-MERGE-CONTRACT-r2.md — chỉ DELETE product copy đã supersede.
6. ops/specs/PR1184-MERGE-CONTRACT-r3.md — exact approved bytes của proposal này khi frozen.

Frozen r1/r2 metadata và byte lịch sử ở abc6/db9/282/29ee9ca giữ nguyên. Net diff từ base vẫn
tối đa năm tệp, dùng own spec r3 thay r2. Không sửa launcher, publisher, workflows, rulesets,
release/version/manifest, corpus/registry, credential/LIVE hoặc tệp ngoài effective write set.

## Contract K1 phải giữ

Legacy không có spec_ref đọc blob tại H và so spec_hash, không đổi hành vi optional field cũ.
External source bắt buộc refs/heads/...@OID40 lowercase, đúng path/OID/hash; không resolve ref trôi,
không fallback khi nguồn authoritative hỏng. Blob tại H nếu có phải byte-identical.
Packet_id lease là nonempty str; revision positive exact int, không bool/string.
Mọi khai packet_id/revision standalone, inline Markdown và identity H1 cùng có mặt phải thống nhất;
fenced examples/HTML comments bị mask; rào/comment không đóng phải chặn.
H1 được coi là identity lookalike khi có revision-like token r/R ngay trước chữ số;
ordinary title như '# Design report' không được từ chối chỉ vì có từ bắt đầu bằng r.
Giữ các ca âm quoted/indented/upper/malformed/contradictory identity và dòng CR.
Giữ quy tắc ADR0062 cho 0/1/≥2 dòng dieu_kien_merge.

External K1 và mọi human K4 chỉ hoạt động sau ADR0063 đủ anchors ở introduction và current
first-parent origin/master: history không shallow, parent đọc được và chưa có path, introduction
nằm trên chuỗi first-parent. Dùng rõ --diff-merges=first-parent và --no-renames; Git không hỗ trợ
phải fail closed. Không dùng path chỉ có ở candidate hoặc synthetic fixture làm rollout authority.

## Contract K4 và timing phải giữ

Human raw comment phải từ canonical repo ducthangho/tra-luat, owner ducthangho/User/OWNER,
positive exact id, URL/issue/pr/self-source đúng; created_at/updated_at canonical UTC hợp lệ.
Body duy nhất YAML đóng schema human_exact_head_audit.v1, không duplicate key/anchor/alias,
đúng packet/revision/generation/PR/full H/tree(H)/spec hash, verdict approve và human_audited,
review_axes đủ spec + standards_security. Unknown/missing/wrong type/identity phải chặn.
P0–P2 chặn; P3 chuyển CLI K5 và chỉ exact owner waiver hiện hành mới nhận.
Model path cũ giữ nguyên; truyền cả model và human thì cả hai phải hợp lệ; thiếu cả hai chặn.
Thiếu đúng một model input phải có rejection chủ ý, không dựa TypeError của Path(None).
Datetime overflow phải thành rejection rõ ở parser liên quan, không mở rộng generic catch của _dk.

Chọn earliest complete same-head workflow run của đúng repo; selected raw run phải thuộc tập min
và khớp toàn bộ id/head/repository/URL/event/time. Rerun muộn không đổi lịch sử push.
Candidate mới sau ADR0062 1f0941e9bba1d1d517eda4174167b81963c06bd5 / 2026-11-04T08:36:24Z
đòi audit.updated_at trước run sớm nhất. Candidate lịch sử chỉ dùng audit sau push khi owner raw
comment schema human_audit_transition.v1 có đủ exact bindings, ADR OID, earliest remote_run,
disposition accept_post_push_audit, reason và self-source. Không tự nâng free text thành receipt.
Giữ K0/K2/K3/K5/K6/K7, CI/connector/P3/Windows/full_mutant_audit M9 và transport readback duties.

## Remediation và nghiệm thu bổ sung

- R1: khóa benign H1 positive + mutant mở rộng trigger; giữ toàn bộ negative grammar hiện có.
- R2: owner YAML anchor/alias (fixture hợp lệ mọi field khác), noncanonical repo self-consistent
  + canonical positive twin, invalid human + valid model qua CLI. Mutants phải vào đúng consumer.
  Nhánh alias dư thừa với anchor phải khai redundancy, không tạo mutation credit giả.
- R3: packet_id integer/empty/None cho spec và human; external abbreviated/uppercase/tag ref
  với real object/abbreviation và positive twins. Mutants tách hai consumer bằng context unique.
- R4: docs và transition harness phải phân loại import/setup/crash/timeout thành _TinDungGia.
  Có committed crash-injection probes cho từng consumer; explicit import importlib.machinery.
  Có mutant gắn các ca CLI transition; controls là actual positive của consumer hoặc khai rõ
  phạm vi controls, không giữ lời claim rộng hơn runner. Bỏ qua/crash/timeout không tính GIET.
- R5: missing model input CLI assert intentional message và absence TypeError; datetime boundary
  qua CLI assert rc12/K4 và no traceback. Parser fix hẹp, không che lỗi lập trình của điều kiện khác.
- R6: actual wp1178 r3 + frozen own r1/r2/r3 external K1 receipts có exact OID/path/hash/rc;
  own spec trong tree có committed regression case. Synthetic policy graph phải được gắn nhãn.

Giữ toàn bộ A1–A9 của r2 theo các contract đầy đủ trên: source/hash/type/conflict/rollout,
human schema và timing, model regression, CLI P3 forwarding/waiver, docs/ADR registration,
canonical base K1 bootstrap của own spec r3, và lịch sử spec metadata bất biến.
Mọi mutant cần unique anchor, intended semantic consumers, actual positive controls;
không tính import/setup/crash/timeout thành kill và không chỉnh guard để che catalog lỗi.

## Gate, thời gian, review budget và handoff

Trước heavy gate: fresh whole-namespace ownership/fence/lease/clock, tools/modules trong đúng
runtime, canonical local admission S/H/T, clean tracked/untracked/ignored snapshot, diff/write-set/numstat.
Trên final exact H phải có complete packet_loop_test.py (baseline + toàn bộ mutation phases),
tl.py --selftest N/N, targeted repairs/mutants, doctrine, ADR, doc-claims và git diff --check.
Windows native theo ADR0057/58/59, paired baseline/candidate + native mutant, own lock/readback/CSV.
New head làm mọi old-head gate/Windows/review binding stale; archives lịch sử không sửa.

Writer run mới tối đa90 phút bằng absolute wall clock, không hồi sinh hoặc kéo run3 g3.
Lịch sử đã biết gồm bốn execution runs (r1 một, r2 ba); proposal xin đúng một run kế tiếp,
không reset attempt count. Override có phạm vi này cần owner duyệt cùng proposal. Tổng chi phí
cloud/token lịch sử chưa được phục hồi đầy đủ: không khai under-quota hoặc trả lại budget cũ.
Đề nghị grant riêng cho verification read-only của frozen H: một lượt tối đa180 phút,
deadline ghi lúc launch, không thêm thời gian viết code hoặc model review. Đây là budget đề nghị,
không bảo đảm fullstandard kết thúc; hết hạn phải giữ evidence và checkpoint, không tự gia hạn.

Model advisory đã dùng4/4; KHÔNG cấp lượt5, không đổi provider/session/prompt để lách.
Sau remediation, dùng primary human độc lập trên final exact H/tree/spec; finding của human
xử lý đúng protocol. Phê duyệt proposal/lease không phải human code audit hoặc land authority.
Không product push/new PR trước offline human audit + required local gates. GitHub CI/M9,
exact land authority, merge và deploy vẫn là các bước/quyền riêng; không mặc nhiên được cấp.

Handoff phải ghi exact H/tree, spec OID/hash, full diff/paths/numstat, commands/real rc/positive
markers, passed/failed/skipped/not_run/interrupted tách riêng, source/test/archive hashes,
review history/cumulative budget, provider/surface/transport và limits chưa đo được.
Stop khi stale/mismatched authority, ngoài write set/cap, same-failure/quota/attempt/budget
limit hoặc thiếu gate evidence; giữ finding IDs, không nén/bỏ test hoặc tự waiver P3.
