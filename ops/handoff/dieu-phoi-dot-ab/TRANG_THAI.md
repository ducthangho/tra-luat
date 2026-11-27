# Bàn giao điều phối #1569 dot-a-rang và #1570 dot-b-rang (ảnh chụp 2026-11-27T07:50Z)

Phiên giao: Claude Code `session_015Gtxraj8uybNKhrrYZSKtB`, điều phối của hai packet. Phiên nhận: một phiên Codex do chủ kho mở
(lệnh chủ kho 2026-11-27: *"Đóng gói và cho Prompt để triển khai tiếp trên Codex"*).

Tệp này là ẢNH CHỤP, không phải nguồn sự thật. Nguồn: tệp đặc tả và lease (theo BĂM ghi dưới), comment trên #1569/#1570, và
`docs/PROTOCOL_DA_PHIEN.md` cùng các ADR. Trạng thái có thể đã trôi khi bạn đọc. Đo lại trước khi hành động.

## 1. Hai packet

| | #1569 `dot-a-rang` r1 g1 | #1570 `dot-b-rang` r1 g1 |
|---|---|---|
| Nợ | R4-01 (danh tính năm bộ đối số) và 23 đột biến SONG cặp A | R4-02 (danh tính 128 ASCII) và 186 đột biến không bị giết cặp B |
| Write set | `ops/gate_output_doi_chieu_test.py` | `ops/land_evidence_nguon_test.py` |
| Đặc tả | `ops/specs/dot-a-rang-r1.md` @ `cc9547c85e7bd5aeb1dd90dadc8855810c8e86f1`, sha256 `e7b014137810ab14a8b0c27482ccdcf387de06665cf57f716f31d48d58e224e6` | `ops/specs/dot-b-rang-r1.md` @ `590fcfb7237fa31ab3252fffa212d67f7b2571ca`, sha256 `ed6778213a8e325489d548d67d01e9d3c019e5d8c79cb8f4871e97ffb732f029` |
| Tệp kèm | `ops/specs/dot-a-rang-r1.ton-kho.tsv` (`25d52320…`), `ops/specs/dot-a-rang-r1.kho-A.jsonl` (`191225ca…`) | `ops/specs/dot-b-rang-r1.ton-kho.tsv` (`ff5dab82…`); luật 9 dùng kho rỗng |
| Nhánh lease | `ops/dot-a-rang-lease` @ `1b6e9cc` | `ops/dot-b-rang-lease` @ `45d4f1b` |
| Lease | `ops/leases/dot-a-rang-r1-g1-claude.yaml`, hết hạn 2026-11-29T02:25:00Z | `ops/leases/dot-b-rang-r1-g1-claude.yaml`, hết hạn 2026-11-29T02:30:00Z |
| Bản chiếu lease | issuecomment-7208157650 (run 45927943417 success) | issuecomment-7208279251 (run 45928526381 success) |
| Base | `26a6e2a0f7addcaa26cb6e01c3ad690dd9ec860f` | như bên trái |
| Trần | 1 tệp, ≤200 dòng thêm, 4 lời gọi Codex review | 1 tệp, ≤420 dòng thêm, 4 lời gọi Codex review |
| Executor | phiên Claude cloud `session_015GtxrYpTbQHdZG1bCpbpTj` | phiên Claude cloud `session_015Gtxrc4Agcx2GFnZxx4aF2` |
| Lời gọi Codex đã dùng | 0/4 | 0/4 |

Cả hai đặc tả có `dieu_kien_merge: ADR-0060@36d7c5dcdcbbb27176b75135125b9009f9fe0587` (ADR-0060 áp dụng đủ M1–M12), dòng trần
ADR-0055 và ADR-0053. Review Class `sensitive`, assurance `delegated_audited`, reviewer `openai_codex`.

## 2. Trạng thái từng packet

### #1570 dot-b-rang — ĐÃ CÓ HANDOFF, CHỜ REVIEW LƯỢT 1

- Ứng viên cục bộ (chưa push): head `6e5750ec21f4c131f5804f2a8d439bc0e161db57`, tree `99d22b888b78bdac4223638c9549d3e911e7cbb0`,
  cha `26a6e2a`. 1 tệp, +136/−1.
- Handoff trên #1570:
  - issuecomment-7212193772: phần 1, gồm tóm tắt, `bundle.b64` và `handoff.yaml`. Bundle 5564 byte, sha256
    `10e0e0304b71ec9a8b02ee609392e0b8c6b61e07e13cd099b0272d3c2cc0594c`; `handoff.yaml` sha256 `d289e0ea…`.
  - 7212194161: phần 2, bảng 186 ID.
  - 7212194581: phần 3, consumer, nghĩa vụ, phép thử tương đương.
  - Hai đính chính: 7212206537 và 7212212698.
  - Ba comment hiện vật luật 9 và cổng: 7212753530, 7212753870, 7212754239.
- Biên nhận vận chuyển do executor tự đo: ba phần mất LF cuối. Phần 3 mất thêm ký tự `!` trong `<![`, nên `do_tuong_duong.py` in ở
  phần 3 bị hỏng; dùng bản base64 trong đính chính 1 (2963 byte, sha256 `c976bd30…`). Bundle và `handoff.yaml` giải từ bản ĐỌC LẠI của
  phần 1 vẫn khớp băm. Muốn nhận bundle thì giải từ bản đọc lại qua REST, rồi kiểm lại băm.
- Executor khai (lời khai, reviewer phải đo lại):
  - Cổng: bộ test head `CA 44/44 · DOT BIEN 145/145 · TONG DAT` (base 40/40); `gate_output_doi_chieu_test` 53/53, 158/158 hai vế;
    `land_evidence_nguon --root .` ĐẠT hai vế; selftest 1789/1789 hai vế; ruff F delta 0; thời gian head − base: −2,88 s,
    −10,84 s, +7,59 s.
  - Luật 9 cặp B (manifest trùng `a606d347`): base GIET 440 · SONG 171 · VO_CAN 13; head GIET 557 · SONG 67 · VO_CAN 0;
    GIET → hạng khác: 0.
  - 186 ID: GIET 119 · TUONG_DUONG 26 · NGOAI_HOP_DONG 39 · chờ quyết định 2.
- **Cần chủ kho quyết:** hai ID `d:map_khong_trung:285:39` và `d:map_khong_trung:288:48`. Executor khai rằng hai đột biến này chỉ
  đổi lỗi NÀO được báo khi một hồ sơ có từ 2 lỗi nạp trở lên. Đặc tả §2.2 không có trạng thái thứ tư. Đây là quyết định của
  chủ kho (§6 đặc tả), cần trước merge.
- **M3 Windows: `required`** theo executor (dòng thêm có `subprocess`, ca `c43`). Reviewer xác nhận khi phân loại M3.
- Lệch lời giao việc ĐÃ CHẤP NHẬN: executor không push nhánh `claude/handoff-*`. ADR-0060 M12 (dòng 132) đặt handoff lên Packet
  Issue; dòng 189 bác việc đẩy ứng viên vào không gian tên riêng. Lời giao việc gốc sai. Đã báo executor khoảng 07:46Z.

### #1569 dot-a-rang — ĐANG THI CÔNG

- Executor nhận việc lúc 02:37Z (issuecomment-7208297404), tự tính băm đặc tả khớp. Chưa có handoff lúc chụp.
- Heartbeat lease 360 phút: hạn đăng tiến độ kế tiếp là 08:37Z. Đã nhắc executor khoảng 07:46Z, kèm đính chính đường bàn giao (handoff
  lên #1569, không push nhánh).

## 3. Kênh liên lạc với executor

Executor là phiên Claude cloud. Phiên Codex KHÔNG gọi được `send_message` tới họ. Đã dặn cả hai executor khoảng 07:46Z:
- tự đặt `send_later` khoảng 60 phút một lần, đọc comment mới trên Issue của mình;
- coi comment có dòng đầu bắt đầu bằng `## Điều phối dot-a-rang` (trên #1569) hoặc `## Điều phối dot-b-rang` (trên #1570) là chỉ
  thị và verdict của điều phối;
- mọi báo cáo đăng lên Issue.

Vì vậy mọi verdict của bạn phải đăng lên Issue với dòng đầu đúng như trên. Đăng xong thì đọc ngược qua REST theo id và so băm.
Executor có thể chậm tới khoảng 60 phút mới thấy. Nếu executor im quá 360 phút, đó là vi phạm heartbeat: báo chủ kho. Không tự
cấp generation mới.

## 4. Việc còn lại (theo thứ tự)

### #1570
1. Review offline Codex lượt 1/4 trên `6e5750e` (mục 5 dưới). Đếm lời gọi TRƯỚC khi gọi.
2. Có finding: đăng verdict lên #1570 (`## Điều phối dot-b-rang — verdict lượt N`), chờ handoff mới. Vá theo LỚP; lớp tái diễn lần 3
   thì dừng (E1). Hai lượt liền không hội tụ (|F|/|U| giảm dưới 50%) thì vào checkpoint.
3. Hỏi chủ kho quyết hai ID chờ (mục 2). Ghi hộ quyết định đúng khuôn ADR-0067 (dòng `Quyết định chủ kho — ghi hộ`) nếu chủ kho trả
   lời qua phiên của bạn.
4. M3 Windows local TẬP TRUNG trên base `26a6e2a` và head: chỉ bước 1–3 của §5 đặc tả (hai bộ test và `land_evidence_nguon --root .`).
   Chủ kho chỉ thị Windows chỉ chạy test tập trung. Máy DESKTOP-T9R33P2 có khoá `C:\tl-win\KHOA.txt`. Khoá gồm 5 trường cách nhau bằng TAB:
   phiên, UTC bắt đầu, UTC hạn, việc, UTC nhịp. Giữ khoá tối đa 2 giờ. Đọc lại trước khi nhả; nhả bằng cách ghi rỗng. Sổ đo:
   `C:\tl-win\do-luong.csv`.
5. Review approve trên SHA X ⇒ đăng `APPROVE trên X` lên #1570; executor push đúng X lên `claude/dot-b-rang-r1-g1` và mở PR draft.
6. Trên PR draft: gọi connector `@codex review` khi còn draft (M6), chờ dòng `Reviewed commit:` đúng head. Chạy `ci-dot-bien-du.yml`
   trên đúng head (M9, `workflow_dispatch`). Chờ `ci.yml` của PR.
7. Audit uỷ quyền ADR-0067 quyết định 3 (`delegated_audited`), do một phiên MỚI, chỉ đọc. Ghi sổ `uy_quyen_quyet_dinh.v1`.
8. `kiem-merge` K0–K7 rc 0 trên đúng head (mục 6 dưới). Đăng lên #1570 template `CHƯA ĐỦ ĐIỀU KIỆN MERGE: thiếu …` cho tới khi đủ.
9. Xin chủ kho DUYỆT MERGE M7 neo đúng SHA. KHÔNG merge khi chưa có.
10. Merge xong:
    - CI master và bốn mốc §10.2.2;
    - hồ sơ land `ops/land/pr<N>-dot-b-rang-land-evidence.yaml` cùng provenance (khuôn
      `ops/land/pr1565-bo-sinh-bat-bien-land-evidence.yaml`);
    - `land_evidence_nguon --root .` ĐẠT;
    - rút hạn lease (khối `thu_hoi_bang_rut_han`, xem lease cũ trên `origin/ops/bo-sinh-bat-bien-lease`);
    - biên bản M8 trên #1570, `kiem-dong-wp` rc 0, đóng Issue.

### #1569
- Chờ handoff, rồi đi đúng chuỗi như #1570. M3 do reviewer phân loại.
- Khi #1569 land hoặc rút lease: báo một dòng cho phiên điều phối #1236 (`session_015GtxrYsNDbfLo32S39f5uY`). Packet gộp
  #1552+#1553 đã hẹn xếp SAU #1569 vì cũng cần `ops/gate_output_doi_chieu_test.py`. Không gọi được `send_message` thì đăng một
  comment lên #1552.

## 5. Gọi review offline Codex

Mẫu prompt và cách bày thư mục: lượt 1–5 của #1539 trên nhánh `ops/bo-sinh-bat-bien-lease`,
`ops/reviews/bo-sinh-bat-bien-r1-ma-{1..5}-codex/` (`PROMPT.md`, `VERDICT.json`, `VERDICT.md`, `kiem_verdict.txt`). Lượt 1 là mẫu
cho lượt đầu; lượt 5 là mẫu cho lượt xác nhận.

Thư mục một lượt `R`:
- `R/repo`: clone đầy đủ, checkout đúng head ứng viên (dựng từ bundle);
- `R/SPEC.md` và `R/LEASE.yaml`: chép từ nhánh lease, kiểm băm;
- `R/bang_chung/`: handoff của executor (lời khai);
- `R/lich_su/`: verdict các lượt trước;
- `R/kiem_verdict_lop.py`: chép từ `ops/handoff/dieu-phoi-dot-ab/cong-cu/` (sha256 `7ef15531…`);
- `R/work/`: chỗ reviewer ghi.

Prompt phải đòi những việc sau:
- verdict theo §8.3: mỗi finding một `class_slug`, có `class_table`; từ lượt 2 có `prior_class_status`;
- đo lại MỌI con số executor khai;
- kiểm mẫu các ID `TUONG_DUONG`/`NGOAI_HOP_DONG` (với #1570);
- phân loại M3 Windows và phạm vi E;
- `VERDICT.json` qua validator với `--vong N`;
- tin nhắn cuối kết thúc đúng một dòng `KET_LUAN: approve|changes_requested`.

Reviewer chỉ ĐỌC repo, không mạng. Đừng bắt reviewer tự soạn nội dung dạng tấn công đường dẫn (bài học bộ lọc nội dung trong
`CLAUDE.md`): hướng thử nào cần thế thì mô tả bằng lời.

Lệnh (Linux, đã dùng cho #1539; `codex` là đường dẫn ĐÃ RESOLVE, xem bài học shim trong `CLAUDE.md`). `<SHA40>` là head ứng viên,
`<ten>` là tên lượt:

```
H=$(sha256sum $R/PROMPT.md | cut -d' ' -f1)
python3 .claude/dev/launcher.py run \
  --workspace $R/repo \
  --expected-repo github.com/ducthangho/tra-luat \
  --expected-root-commit 394e93468fc8d84ec20938e6df8fb7ab72b2cc37 \
  --expected-head <SHA40> --require-clean \
  --prompt-file $R/PROMPT.md --expected-prompt-sha256 $H \
  --run-root $R/run --name <ten> --json \
  -- <codex> exec -c 'model_reasoning_effort="high"' --cd $R/repo --sandbox workspace-write --skip-git-repo-check \
  "Đọc TOÀN BỘ tệp {PROMPT_FILE} và làm đúng mọi việc trong đó. Tin nhắn cuối phải kết thúc bằng dòng KET_LUAN như tệp yêu cầu." \
  > launcher.out 2> launcher.err < /dev/null
```

Ghi chú về lệnh:
- Chạy nền. `launcher.py run` cho tiến trình con `stdin=DEVNULL`, nên prompt phải đi bằng đối số.
- `run.json` và `stdout.log` trong `R/run/<ten>/` là đầu vào K4 của `kiem-merge`; dòng cuối của stdout phải là `KET_LUAN: approve`.
- Lời gọi bị cắt giữa chừng vẫn tính vào trần.
- Lượt review là một tiến trình Codex MỚI, độc lập với phiên điều phối. Executor không tự review.

Công bố verdict: commit `ops/reviews/dot-b-rang-r1-ma-<N>-codex/` (PROMPT, VERDICT.json/.md, kiem_verdict.txt, run.json) lên nhánh
lease của packet, rồi đăng tóm tắt và băm lên Issue.

## 6. kiem-merge và hồ sơ land

- `python3 .claude/dev/packet_loop.py kiem-merge --repo ducthangho/tra-luat --head <H> --base 26a6e2a0f7addcaa26cb6e01c3ad690dd9ec860f
  --spec <spec> --lease <lease> --pr <N> --workflow-runs … --workflow-jobs … --check-runs … --connector … --offline-run-json …
  --offline-stdout … --windows-json … --dot-bien-du-runs … --dot-bien-du-jobs … [--p3-offline … --chu-kho-comment …]`
- Thu các JSON đầu vào bằng `ops/land/pr1565-bo-sinh-bat-bien-provenance/kiem-merge/thu_kiem_merge.py <ra> <head> <pr> <comment_chu_kho_id>
  [dot_bien_du_run_id]` (REST, đọc `GITHUB_PAT`; trên máy chủ kho có thể thay bằng `gh api`). Khuôn `windows.json`:
  `ops/land/pr1565-bo-sinh-bat-bien-provenance/kiem-merge/windows.json`.
- Hồ sơ land và M8: khuôn `ops/land/pr1565-bo-sinh-bat-bien-land-evidence.yaml` cùng thư mục provenance; biên bản M8 mẫu
  #1539 issuecomment-7207691409. `kiem-dong-wp` D2b đòi `gate_output_nguon: {oid, tep}` trỏ tệp `danh-gia-gate-output-<run>.txt`
  trên một commit đã đẩy, và `ci_master.run_attempt`.
- Mốc Workflow definition §10.2.2: dispatch `ops-do-workflow-definition.yml` (input `run_id`), hoặc trên máy chủ kho chạy
  `gh api graphql` theo mẫu một dòng cho `cmd` ở `CLAUDE.md` (mục "Lệnh `gh api graphql`…").

## 7. Ràng buộc đứng (không đổi khi đổi phiên)

- Không đọc/ghi secrets, không `--apply`, không viết nguyên văn chuỗi bỏ-qua-CI trong commit message.
- Không đưa tên model vào hiện vật đẩy lên kho.
- Subagent và reviewer chỉ đọc; không ai ngoài executor sửa write set.
- Đo bằng clone sạch, đầy đủ, `core.abbrev 7`; hai vế base/head dựng trong cùng một lệnh. Đòi bằng chứng dương `N/N`, đừng tin rc.
- Đăng xong thì đọc ngược và so băm; tầng vận chuyển đã làm mất ký tự ở chính packet này.
- Trước MỖI lời gọi Codex: đếm số đã dùng, đọc trần trong lease. Chạm trần chưa approve ⇒ dừng, hỏi chủ kho (E2).
- Merge cần lần duyệt M7 của chủ kho neo đúng SHA. Quyết định của chủ kho chỉ được GHI HỘ bởi phiên điều phối của packet ấy.
- Windows local chỉ chạy test tập trung.
- Không dọn ref ngoài workflow `ops-don-ref` khi chưa có duyệt.

## 8. Biết sẵn

- `ops/kiem_ho_so_land.py` đỏ sẵn trên master (`pr1510-r1509-acl-codex` thiếu `authorization_url`, #1511), delta 0. Đừng vá.
- `canh-tuoi-audit.yml` đỏ ở mọi lượt (#1561/#1520), ngoài phạm vi.
- Selftest Windows từng có một ca đỏ sẵn ở cả hai vế: `r380_llm_khai_niem_bien_dau_vao` (#1545).
- Bộ test cặp B chạy khoảng 220 giây; một lượt luật 9 khoảng 80 phút với `--song-song 4`.
