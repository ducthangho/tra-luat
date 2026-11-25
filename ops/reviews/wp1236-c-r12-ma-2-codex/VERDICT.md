Review mã wp1236 đợt C — r12/g1, lượt 2/4. **changes_requested: còn C01 P1; C02 đã đóng.**

Reviewed SHA: `2439922c67a091c53e277c9e0b13d8fc04089453`  
Tree: `b2ba746fdbe08bff82d66467c0e9b0306fad38cd`  
Base: `f602325574c62184caf16309631f5f680ca5cee2`  
Spec SHA-256: `4589daf1fd666b03a68b7d7dcd5c60903c10e946963fd324c9ee6185ed8e2dc7`.

Reviewer: `openai_codex / codex_cli / machine-local`, run `fb13277a68b84805b3e641486bcf86db`, độc lập với executor. Linux, Python 3.13.18, Git 2.43.0; model và effort phục vụ `KHONG_DO_DUOC` (effort yêu cầu: high). Review offline, không GitHub/mạng, không sửa checkout. Cổng sandbox cho phép workspace-write; tính chỉ đọc của checkout được giữ bằng thao tác và snapshot, không khai thành mount read-only.

| Lớp lượt 1 | Đối chiếu lượt 2 | Mức còn mở |
|---|---|---|
| `archive-loc-mat-du-lieu-kiem` — C01 | `VA_MOT_PHAN`: symlink/attributes đã chặn; collision thư mục còn hở | P1 |
| `hop-dong-dau-ra-duong-dan-tu-do` — C02 | `DA_VA_THAT` theo miền E3 | — |

Hội tụ: **1/2 lớp**, chưa có lớp lặp lần ba. Không có P3 mở mới. C01 dưới đây là hành vi của mã gốc, không phải đột biến ngoài manifest.

**C01 — kiểm leaf bỏ sót collision ở thư mục**

Vị trí: `.claude/dev/packet_loop.py:3974–3978`, `_d2b_kiem`.

`git ls-tree -r -z` không liệt kê tree trung gian. Cây Git chứa `A/note.txt` và `a/readback-wp-issuecomment-7.json`; hai tên leaf vẫn khác nhau sau NFC/casefold. Khi nền gộp thư mục `A` và `a`, mọi blob vẫn đúng hash nên chốt hiện tại cho qua. `readback_thu_muc=…/A` nhận readback chỉ nằm trong `…/a` của OID.

Đã đo trên mã sản phẩm nguyên trạng qua toàn bộ `kiem-dong-wp`:

- Đối chứng Linux phân biệt hoa/thường: **rc 12**, `THIẾU D2b mien:readback`.
- Cùng dữ liệu, mô phỏng extraction/lookup không phân biệt hoa/thường: **rc 0**, `D2b ĐẠT mien …/A@OID` và `ĐÓNG ĐƯỢC WP`.
- Đây là **mô phỏng Linux, chưa phải Windows native**. Fixture chỉ có thư mục/tệp thường và readback từ helper sẵn có; không symlink hay đường dẫn thoát cây. Git, schema, D1–D4, module và mã D2b chạy thật. Chi tiết/hash: [case_directory.json](case_directory.json).

Tái lập từ thư mục `c2-2-codex` (script rc 0 nghĩa là đã tái hiện được lỗi và đối chứng):

```bash
PYTHONDONTWRITEBYTECODE=1 TMPDIR="$PWD/work/tmp" python3 -B work/probe_case_directory.py
```

Vá ở ranh giới Git → archive trong `_d2b_kiem`: kiểm namespace đầy đủ, gồm thư mục và tiền tố, cùng collision directory/directory và directory/file trước khi gọi validator. Giữ kiểm blob, symlink và phạm vi K2; namespace không tái lập duy nhất được thì rc8, không đổi miền cú pháp E3. Cách rẻ là bổ sung inventory thư mục và kiểm canonical key; đừng chỉ thêm `-t` vào vòng hiện tại rồi coi mọi tree là file. Cách chặt hơn là đối chiếu hai chiều danh mục cây và bản bung, tách luật namespace khỏi luật kiểm byte.

Ca khóa: `A` không readback phải không nhận readback từ `a` dù tên con khác nhau; có đối chứng một thư mục hợp lệ và các tiền tố dùng chung hợp lệ. Chạy cả mô phỏng Linux lẫn Windows native. Đột biến bỏ riêng kiểm collision thư mục phải làm ca này đỏ đúng tín hiệu. Rủi ro bản vá: chặn oan tiền tố dùng chung, nhầm directory với file, hoặc siết sai symlink/readback ngoài phạm vi K2.

**Các biểu hiện đã đo và phán quyết chỗ lệch**

Probe lượt 1 chạy lại: YAML thường cạnh YAML symlink nay rc12 `kiem_tep:not_measured:symlink`; LF ở hai nhánh nay rc12 `duong_dan_sai`. Bộ targeted qua `chay_suite`: **31/31 đạt**, gồm 17 D2b và 14 D cũ/CRLF.

Bốn vị trí regex được kiểm trên mọi codepoint Unicode (trừ `/`, vốn là dấu phân cách cấu trúc): mỗi vị trí nhận đúng 93 ký tự của miền E3. 160 gọi âm qua `_d2b_kiem` không gọi Git. Ca rc8 chứa LF trong ngoại lệ vẫn một dòng. Nhận `duong_dan_sai` khi đồng thời OID sai là hợp lý: dừng ở cú pháp D2b trước phép đo Git; không báo một vi phạm remote chưa đo.

Các ca symlink YAML, thư mục symlink, symlink ngoài K2 và nhánh miễn giữ đúng phân biệt. `export-ignore`/EOL, `ident`, `export-subst`, filter smudge đổi byte, collision leaf case/NFC–NFD và gitlink đều bị chặn. Tệp đánh giá `100755` bị rc12; YAML nội bộ `100755` vẫn hợp lệ. Probe gitlink đầu tiên bị fixture xóa entry trước commit nên **không có giá trị**; [remaining.json](remaining.json) có phép đo sửa setup, chứng minh mode `160000` và rc8 cả hai nhánh.

Chấp nhận hướng bung trung thực rồi kiểm cây, nhưng C01 chứng minh phần namespace chưa đủ. Symlink tuyệt đối/thoát cây chỉ được phân tích bằng lời và chạy các phản chứng sẵn có của module; không dựng payload mới. Chưa đo topology symlink phức tạp hoặc can thiệp đồng thời cùng UID. Không tuyên bố bản bung hiện tại là song ánh đầy đủ với cây Git.

Chấp nhận ba điều chỉnh có điều kiện: (1) luật 9 trên khối D2b cộng A/B; khối chỉ bỏ hai LF phân cách và ghép lại đúng byte, import/lời gọi/help ngoài khối đã kiểm; (2) fixture rút gọn và đổi head, vì T-v3/T-fail giữ nguyên trạng thái, C4 chỉ đỏ `kiem_tep:failed:-`, C5(c) đúng `duong_dan_sai`; (3) hợp đồng output riêng của harness tích hợp. Riêng lời khai handoff “mC11 không ra ĐẠT” đã cũ: trên đúng fixture `lk5` của head, mC11 nay rc0/ĐẠT, phù hợp đặc tả.

**Bằng chứng chạy và giới hạn**

- Luật 9: bộ quét đúng SHA `1b3e4a9e…`, `do` rc0 có `HOAN_TAT`; **203 = 200 GIET + 3 TUONG_DUONG**, kho B rỗng. Manifest, ID và ca đích khớp executor. Ba chứng minh: thêm hậu tố ref không đổi tiền tố; SHA regex đã neo hai đầu nên match/fullmatch tương đương; type equality/is tương đương trên miền safe YAML. [luat9_summary.json](luat9_summary.json), [ledger_A.tsv](ledger_A.tsv).
- Audit độc lập log executor: đủ 16 nền +16 đột biến mỗi vế, cùng 38 skip; 1784/1801 ca nền, cộng hai CA_DAI mỗi vế. 2009/2051 mutant, trong đó 2007/2049 bị giết. `r1187_spec_packet_type` đỏ và một mutant native bị skip ở cả hai vế; không hồi quy theo tên/target/control. Đây là audit log, không tự nhận đã chạy lại full suite.
- Tự chạy đủ **30 mảnh**: nền 2–15 trên base/head (bao mọi D2b) và đột biến 4/16 mỗi vế. Nền base: `{'passed': 1579, 'skipped': 38, 'failed': 15}`; head: `{'passed': 1596, 'skipped': 38, 'failed': 15}`. D2b **17/17 passed**. Lỗi nền đều là socket `PermissionError` B4; không ghi thành pass. So tên: `{'missing_base_cases': [], 'passed_regressions': [], 'failed_sets_equal': True, 'skipped_sets_equal': True}`. Đột biến 4/16: base `{'killed': 125, 'failed': 1}` (rc 1), head `{'killed': 128}` (rc 0). Mutant base `b4_vc_bo_han_tuong` bị từ chối tín dụng giết vì ba ca đích CLI sập; chính các ca B4 ấy bị chặn socket ở nền. Đây là `failed`, không phải `GIET`. Mảnh cùng số không bảo đảm cùng tập mutant sau khi chèn delta; đối chiếu đầy đủ theo ID dựa trên audit A/B. Command, rc thật, ID và positive completion từng mảnh: [shards/receipts.json](shards/receipts.json), [shards_summary.json](shards_summary.json).
- Ruff 0.15.15, `--no-cache --select F` hai tệp: **rc1 ở cả hai**, 16 chẩn đoán nền, delta0 sau chuẩn hóa riêng số dòng được nhúng trong thông báo. Pin/probe contract riêng: rc0, 3 mục, không lỗi.
- Numstat toàn đợt: 2 tệp, **+374/−13**, trong trần 450; `git diff --check f602325 HEAD` rc0. Exact HEAD/tree và status/diff/index giữ nguyên. Hash ignored được chụp sau các probe đầu, không tự nhận có snapshot byte ignored tại đầu run; không chứng minh lịch sử chưa từng ghi rồi hoàn nguyên.
- `not_run`: Windows native, Python 3.12, GitHub/CI và full tl selftest/registration của reviewer. Full legacy mutation và nền mảnh 0/1/CA_DAI chỉ audit evidence executor. `origin/master` trong clone được cấp ở f602325; không xác minh trạng thái remote thật.

**M3: required.** Cần Windows local trên exact head/base. Rủi ro cần đo: collision thư mục trên NTFS (C01); symlink thiếu quyền ⇒ rc8 và nhánh `not_measured:symlink` chưa đo; `core.autocrlf` đổi byte archive khi thiếu attributes; MAX_PATH; NFC/NFD, tên dành riêng/dấu chấm cuối/backslash; khác biệt tarfile Python 3.12/3.13. Windows CI được miễn theo authority trong prompt/lease, không đồng nghĩa miễn Windows local.

CHƯA ĐỦ ĐIỀU KIỆN MERGE: còn C01 P1 và chưa chứng nhận Windows local/các gate, authority sau review.

KET_LUAN: changes_requested
