# Đặc tả packet — `CLOUD-SETUP-P2B-WIRE` (revision 1)

- `packet_id`: **CLOUD-SETUP-P2B-WIRE** · `packet_issue`: **#1039** (Issue cha #1008) · `revision`: **1** · trạng thái:
  **ĐÓNG BĂNG** 31-10-2026. Băm `sha256` ghi trên Issue #1039 và PR của nhánh `claude/wp1039-cloud-setup-p2b-spec`, không
  ghi trong tệp. Sửa nội dung từ đây ⇒ revision 2 · soạn 31-10-2026, phiên `session_015GtxrcFW4EJYWbxuDTXnrJ`.
- `nguon_cap_viec`: chỉ thị trực tiếp của chủ kho (Issue cha #1008, chuỗi `cloud-setup`, nửa sau của P2). Phạm vi gốc chốt ở
  các vòng hỏi của P2 (ghi trong thân #1039: vòng 1 Q4, Q5; vòng 2 Q11; vòng 3 Q14, Q18). Phần còn lại chốt trong phiên soạn
  này: vòng 1 Q1–Q11 và vòng 2 Q12–Q20, chủ kho trả lời cả hai vòng "Đồng ý tất cả các khuyến nghị". Không có dòng kế hoạch
  nào trong `ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md`.
- `review_class`: **sensitive** — chạm ranh giới credential (gọi `bootstrap` giải mã bằng `TL_MASTER_KEY`, ghi `auth.json` và
  cấu hình `agy`) và hook phiên `.claude/hooks/session-start.sh` (protocol §8).
- Base dự kiến: `origin/master` lúc cấp lease (đo 05:01Z 31-10: `01ff6503`, merge PR #1042). Mọi phép đo kích thước/delta đo
  so merge-base (`git diff origin/master...HEAD`).
- **Điều kiện cấp lease (vòng 1 Q1):** hồ sơ land của P2a (PR #1063, merge `69dcfee` 04:28Z 31-10) phải có trên master với
  `landed: true` đủ bốn mốc §10.2.2. Đo 05:01Z 31-10: `ops/land/pr1063-*` **chưa có**. Lease `wp1038-cloud-setup-p2a-r1-g1-claude`
  vẫn CÒN_HẠN trên `scripts/tl_gws.py`; write set dưới đây KHÔNG chạm tệp ấy nên không giao nhau.
- `nang_tran`: chủ kho đồng ý vòng 2 Q18 trong phiên nói trên. Trần của packet này: **≤ 8 tệp / ≤ 600 dòng thêm** (thay
  `ADR-0053` CHỈ cho packet này). Vượt 600 dòng ⇒ bỏ bớt ca phụ, KHÔNG xin nâng thêm. Neo nguyên văn lời duyệt vào Issue
  #1039 lúc đóng băng.

tran_loi_goi_codex: ADR-0052@8ab100793df9831505f495543a74044b91c2c9ab
tran_kich_thuoc_sensitive: nang_tran vòng 2 Q18 (≤ 8 tệp / ≤ 600 dòng thêm; thay ADR-0053@8ab100793df9831505f495543a74044b91c2c9ab)

(OID là commit LAND của `ADR-0052` và `ADR-0053` — merge PR #791; cùng giá trị đặc tả P1 r4 và P2a r1. Đo lại 05:01Z 31-10:
`8ab1007^1` KHÔNG có hai tệp ADR, `8ab1007` có cả hai.)

## Vấn đề (một đoạn)

P1 (#1009) và P2a (#1038) dựng xong phần lõi: `tl bootstrap` nạp credential từ `TL_MASTER_KEY` và in đúng một dòng
`[bootstrap] agent_creds: …` (`scripts/tl_gws.py:1756`); `tl agent-creds-exec --gemini -- <lệnh>` đặt `GEMINI_API_KEY` chỉ cho
tiến trình con (`scripts/tl_gws.py:1260`); hằng `AGENT_CREDS_FILEID` đã có fileId thật (`scripts/tl_gws.py:1089`). Nhưng
**chưa nền cloud nào gọi `bootstrap`**: hook Claude Code (`.claude/hooks/session-start.sh`, 642 dòng) và setup Codex Cloud
(`ops/codex_cloud_setup.sh`, 105 dòng) không nhắc tới nó. Phiên cloud phải chạy tay. `agy` chưa được cài ở phiên cloud nào,
nên `agent-creds-exec --gemini` chưa từng được đo với `agy` thật. Ngoài ra `cmd_bootstrap` thoát rc 2/3 **trước** dòng
`agent_creds:` khi thiếu khoá, tải hoặc giải mã `tl_secrets.enc` lỗi (`scripts/tl_gws.py:1652–1672`). Vì vậy yêu cầu "log setup
phải có dòng `agent_creds: …`" (vòng 2 Q11 của P2) không tự đúng khi chỉ gọi `bootstrap`. Packet này nối `bootstrap` vào hai
tệp setup qua một helper dùng chung, cài `agy` bản ghim vào phiên Claude Code web, và viết RUNBOOK cho quy trình một secret.

## `write_set`

Đúng 8 đường dẫn (vòng 2 Q18). Không ký tự đại diện.

1. `.claude/hooks/session-start.sh` — gọi `nap` và `cai-agy`; thêm hai tên năng lực
2. `ops/codex_cloud_setup.sh` — gọi `nap` trong `main`
3. `ops/cloud_agent_creds.py` — **mới**: helper, hai lệnh con `nap` và `cai-agy`
4. `ops/cloud_agent_creds_test.py` — **mới**: ca + bảng đột biến
5. `ops/codex_cloud_setup_test.py` — ca cho phần nối `nap` vào `main`
6. `.claude/dev/ci_dang_ky_test.py` — +1 dòng đăng ký `ops/cloud_agent_creds_test.py`
7. `references/RUNBOOK.md` — mục A0.4e
8. `RELEASE_MANIFEST.json` — tái sinh vì (7) nằm trong manifest (CLAUDE.md, Quy ước deploy mục 5)

Không tệp nào khác. Cần sửa một tệp ngoài danh sách ⇒ DỪNG, hỏi chủ kho (L2). Cụ thể **KHÔNG** sửa `scripts/tl_gws.py`,
`scripts/tl_core/cli.py`, `ops/cong_cu.yaml`, `.claude/dev/launcher.py`, `.claude/dev/launcher_test.py`, golden, CHANGELOG, VERSION.

## `ngoai_pham_vi`

- **`agent-creds-exec` trong giai đoạn agent của Codex Cloud** (vòng 1 Q5). Theo tài liệu Codex, *secret* chỉ có trong setup
  script và bị gỡ trước khi agent chạy. Phép đo 27-10 cho thấy `$HOME` chỉ đọc lúc agent chạy (`ops/codex_cloud_setup.sh`, chú
  thích `ghi_bashrc`), và internet giai đoạn agent thường tắt. `agent-creds-exec` tải `.enc` mỗi lần và cần `TL_MASTER_KEY`,
  nên rất có thể không chạy được ở đó. Điều về secret CHƯA đo trên Codex Cloud (xem `chua_do_duoc`); nếu muốn đo thì làm
  ở packet sau.
- **Cài `agy` trên Codex Cloud** (vòng 1 Q5): chỉ hook Claude Code gọi `cai-agy`.
- **Sửa `cmd_bootstrap` để nhánh agent luôn chạy** (vòng 1 Q4, phương án B bị loại): helper bù khoảng trống ấy từ bên ngoài.
- **Thêm cờ "chỉ agent" cho `bootstrap`** (vòng 1 Q3, phương án C bị loại).
- **Thêm `agy` vào `ops/cong_cu.yaml`** (vòng 2 Q15): sổ ấy là sổ công cụ của cổng CI; `agy` không phải công cụ CI.
- **Chạy `agy install`** hoặc installer chính thức `install.sh`/`install.ps1` (vòng 1 Q6): installer luôn cài bản "latest",
  không có cờ chọn bản, và `agy install` sửa cấu hình shell.
- **Cơ chế PATH mới** (vòng 1 Q9): phiên Claude web đã có `/root/.local/bin` trong PATH (đo trong phiên soạn), còn Codex Cloud
  có `ghi_bashrc` (`ops/codex_cloud_setup.sh`). Packet chỉ ĐO, không thêm.
- **Hook tự chạy probe `agy models` mỗi phiên** (vòng 1 Q8): tốn lời gọi, đọc secret thật; chỉ đo một lần trong M1.
- **Windows** (vòng 1 Q11, vòng 2 Q20): hook thoát ngay khi `CLAUDE_CODE_REMOTE` khác `true`, nên không có gì chạy trên máy cục bộ.
- Ghi ngược `auth.json` của Codex, NLM tải lại cookie: P3 (#1008).
- Cloud agent của Antigravity; đăng nhập OAuth/ADC của `agy` (#1008, "Đã chốt").

## Hằng ghim `agy` (đo 04:31–05:01Z 31-10)

Nguồn: manifest `https://antigravity-cli-auto-updater-974169037036.us-central1.run.app/manifests/<nền>.json`. Cả sáu manifest
cùng trả `version` **1.4.12**. Đã tải tarball `linux_amd64` về scratch và kiểm `sha512sum -c` ⇒ `OK`; tarball chứa đúng một tệp
`antigravity` (234144144 B). Năm nền còn lại chỉ đọc manifest, chưa tải tarball.

| khoá nền | URL tarball | sha512 |
|---|---|---|
| `linux_amd64` | `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/linux-x64/cli_linux_x64.tar.gz` | `ea01c73b772187bca928852cf96235f0d846d6da5ebdac188b9ae719597465737f325540d483ee5f3f62d151029001713344972a187ddfb98cc7b97f7204b7f4` |
| `linux_arm64` | `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/linux-arm/cli_linux_arm64.tar.gz` | `7cae317fb6a02eb387982f06bfb234b366879cf9a80ad8969b571e5a55d1e37a6a5a49cd6b703c0443bb417937cf5e3b14a8c80cb26917ad79eef723a9f374c7` |
| `linux_amd64_musl` | `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/linux-x64-musl/cli_linux_x64_musl.tar.gz` | `60a2705b9d0446a88fe2a685a044e0f9ec65f9742492d96e6fa3a87c9c477d3fddd9c4d7f22bca7bdb2a99d6dd5833de9d6e690eb8fd9e77ebe25794fdb4555a` |
| `linux_arm64_musl` | `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/linux-arm-musl/cli_linux_arm64_musl.tar.gz` | `767902b8569d08e7283139f3aba05eacdc0070b96d940ca4d2fad863ea6c2f3c35bb79ab079fcfeb87f6f79272bb4c0b666af8829873883dc1c9798321dd28f6` |
| `darwin_amd64` | `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/darwin-x64/cli_mac_x64.tar.gz` | `1d78368cd5a136dc4c7cc71cfe4649d1b1e643630d79327ff3c4efd4b19a90d5603e2cf65a54f80c7eaef973dd09f854dae8a8228b4edd4c6466c679ded9babf` |
| `darwin_arm64` | `https://storage.googleapis.com/antigravity-public/antigravity-cli/1.4.12-4768735748292608/darwin-arm/cli_mac_arm64.tar.gz` | `e858cfc02fb5bb500a760643da270accd2847aa986b7e2973da97ad1928b99d62f62bad28c039e25b65e1ca073d27b2f30b13ed0919d0329774eb1e0ee5b4748` |

Chọn nền theo đúng luật của `install.sh` chính thức (đọc tĩnh 04:31Z): `uname -s` → `linux`/`darwin`; `uname -m`
`x86_64|amd64` → `amd64`, `arm64|aarch64` → `arm64`; Linux có musl (tệp `/lib/libc.musl-x86_64.so.1` hoặc
`/lib/libc.musl-aarch64.so.1`, hoặc `ldd /bin/ls` nhắc `musl`) ⇒ hậu tố `_musl`. Nền nằm ngoài bảng ⇒ `CHƯA HỖ TRỢ`
(vòng 2 Q15). Executor KHÔNG được tự thêm hay đổi băm. Muốn đổi bản thì ra revision mới của đặc tả.

Tên cấu hình đọc từ chuỗi tĩnh của nhị phân 1.4.12 (không chạy nhị phân):
- tệp settings: `~/.gemini/antigravity-cli/settings.json`; khoá `"modelProvider"`;
- thông báo khi thiếu khoá: *"modelProvider is set to %q in settings.json, but the %s environment variable is not set"*;
- biến `AGY_CLI_DISABLE_AUTO_UPDATE`;
- cảnh báo *"Both GOOGLE_API_KEY and GEMINI_API_KEY are set. Using GOOGLE_API_KEY."*

## `muc_tieu`

Mỗi dòng chiếu vào đúng một đường dẫn ở `write_set` (L2).

1. → `ops/cloud_agent_creds.py`: lệnh con **`nap`** (vòng 1 Q2–Q4, vòng 2 Q13–Q14).
   - Thiếu hoặc rỗng `TL_MASTER_KEY` ⇒ không gọi `tl`; in `agent_creds: BỎ QUA — thiếu TL_MASTER_KEY`.
   - Có khoá ⇒ chạy `<python đang chạy helper> <gốc kho>/scripts/tl.py bootstrap --env code --no-nlm` (không thêm
     `--require-agent-creds`). Không qua shell. Timeout đọc từ `TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY` (mặc định **180**; rác, âm,
     0 hay `inf` đều về 180). Quá hạn ⇒ giết cả nhóm tiến trình, rồi KIỂM LẠI là đã chết.
   - Gom stdout+stderr của `bootstrap`. Chuyển tiếp mọi dòng **trừ** các dòng chứa `agent_creds:`. Mọi lần xuất hiện của giá
     trị `TL_MASTER_KEY` trong output được thay bằng `***` trước khi in.
   - Cuối cùng in **đúng một** dòng chuẩn `agent_creds: <TRẠNG THÁI> — <chi tiết>`:
     · `bootstrap` in đúng 1 dòng `agent_creds: <S> — <ct>` với `S ∈ {ĐÃ NẠP, KHÔNG CẤU HÌNH, KHÔNG ĐO ĐƯỢC}` ⇒ chép `S` và
       `ct`, kèm `(bootstrap rc=N)`;
     · 0 dòng ⇒ `KHÔNG ĐO ĐƯỢC — bootstrap thoát rc=N trước bước agent`;
     · quá hạn ⇒ `KHÔNG ĐO ĐƯỢC — bootstrap quá <T> s, đã dừng`;
     · ≥ 2 dòng, hoặc `S` ngoài tập trên ⇒ `KHÔNG ĐO ĐƯỢC — đầu ra bootstrap không đúng hợp đồng (<lý do>)`;
     · không chạy được `tl.py` (OSError) ⇒ `KHÔNG ĐO ĐƯỢC — không chạy được bootstrap (<lớp lỗi>)`.
   - Mọi lời in đi qua stdout ép UTF-8. `nap` **luôn rc 0**; chỉ sai cú pháp mới rc 2.
2. → `ops/cloud_agent_creds.py`: lệnh con **`cai-agy`** (vòng 1 Q6, vòng 2 Q15).
   - Hằng `AGY_VER = "1.4.12"` và bảng 6 nền ở mục *Hằng ghim* ở trên, chép nguyên văn.
   - Đã có `~/.local/bin/agy` và `agy --version` (timeout 15 s) in chuỗi chứa `1.4.12` ⇒ không tải gì.
   - Thiếu, hoặc lệch bản, hoặc `--version` hỏng ⇒ tải URL của nền bằng `urllib`, đối chiếu sha512 với hằng. Lệch ⇒ không
     ghi gì, in `agy: ✗ sha512 lệch`. Khớp ⇒ đọc tarball bằng `tarfile`, chỉ nhận đúng một thành viên tệp thường tên
     `antigravity` (thành viên khác, symlink, đường dẫn tuyệt đối hay chứa `..` ⇒ từ chối toàn bộ), ghi ra tệp tạm cùng thư
     mục rồi `chmod 0755` và `os.replace` sang `~/.local/bin/agy`. Không gọi `agy install`.
   - Nền ngoài bảng ⇒ `agy: CHƯA HỖ TRỢ <khoá nền>`, không tải.
   - Sau khi cài, kiểm `shutil.which("agy")` với PATH của tiến trình. Không ra `~/.local/bin/agy` thì in cảnh báo (vòng 1 Q9).
   - `cai-agy` **luôn rc 0**; chỉ sai cú pháp mới rc 2. Mọi lỗi mạng/ghi đều in một dòng `agy: …`.
3. → `ops/cloud_agent_creds.py`: trong `cai-agy`, **gộp `modelProvider`** (vòng 1 Q7). Đọc
   `~/.gemini/antigravity-cli/settings.json`. Không có ⇒ tạo `{"modelProvider": "gemini"}`. Là JSON object ⇒ đặt đúng khoá
   `modelProvider` = `"gemini"`, giữ mọi khoá khác, ghi nguyên tử (tệp tạm cùng thư mục + `os.replace`). Không phải JSON object
   ⇒ không đụng tệp, in cảnh báo. Không bao giờ ghi khoá API hay giá trị nào lấy từ môi trường.
4. → `ops/cloud_agent_creds.py`: trong `cai-agy`, nếu `CLAUDE_ENV_FILE` được đặt ⇒ bảo đảm tệp ấy có **đúng một** dòng
   `export AGY_CLI_DISABLE_AUTO_UPDATE=1` (chạy lại không nhân bản) (vòng 2 Q16a). Không đặt ⇒ bỏ qua, không lỗi.
5. → `.claude/hooks/session-start.sh` (vòng 1 Q2, vòng 2 Q17).
   - Một khối duy nhất, bọc giữa hai dòng đánh dấu `# >>> agent-creds (wp1039)` và `# <<< agent-creds (wp1039)`. Khối đặt
     **sau** khối "phụ thuộc Python của kho" (`bootstrap` cần các gói ấy) và **trước** lời gọi `codex_env_policy.py` (đo
     05:01Z: dòng 237 và dòng 585 trên `01ff6503`), để `doctor` đo trên `auth.json` đã nạp.
   - Trong khối: `"$PY" "$GOC/ops/cloud_agent_creds.py" nap` rồi `"$PY" "$GOC/ops/cloud_agent_creds.py" cai-agy`. Mỗi lệnh có
     `|| true` hoặc dạng `MA=0; … || MA=$?`, để `set -euo pipefail` không giết hook. Mọi dòng in ra mang tiền tố `[session-start] `.
   - Dòng `# hook-nang-luc:` thêm hai tên `agent-creds-bootstrap` và `agy-ghim`.
6. → `ops/codex_cloud_setup.sh`: trong `main`, sau bước 1 (pip, vì `bootstrap` cần `requirements.txt`) và trước bước 5 (bằng
   chứng dương), gọi đúng một lần `"$PY" ops/cloud_agent_creds.py nap || true`. Không gọi `cai-agy` (vòng 1 Q5).
7. → `ops/cloud_agent_creds_test.py`: các ca ở `nghiem_thu` A/B/C/D + bảng đột biến chạy trên **bản sao tạm**. Ca đích được
   xác định bằng một lớp ngoại lệ riêng (kiểu `TinHieuChotCa(AssertionError)`) kèm **tên ca**. Mutant chết vì lỗi khác thì là
   tín dụng giả, không tính là bị giết (CLAUDE.md, bài học "đột biến bị giết không phải đột biến bị giết đúng lý do"). In dòng
   tổng kết theo một mẫu mà `ci_dang_ky_test.py` đã dùng cho tệp khác. Mẫu phải đòi số ca đạt bằng tổng số ca, số mutant bị
   giết bằng tổng số mutant, và cả hai số lớn hơn 0.
8. → `ops/codex_cloud_setup_test.py`: ca E1, E2 ở `nghiem_thu`.
9. → `.claude/dev/ci_dang_ky_test.py`: +1 dòng, ánh xạ `ops/cloud_agent_creds_test.py` tới mẫu nói ở mục 7.
10. → `references/RUNBOOK.md`: mục mới **"A0.4e — 1 secret cho phiên cloud"** (tên `A0.4d` đã có sẵn: mục NLM CLI ở Cowork, `references/RUNBOOK.md:180`, đo 05:0xZ 31-10), đặt ngay sau mục A0.4d, ≤ 60 dòng (vòng 1 Q10). Nội
    dung: đặt `TL_MASTER_KEY` ở đâu trên Claude Code web và trên Codex Cloud · hook/setup làm gì (gọi `nap`, `cai-agy`) · bảng
    bốn trạng thái của dòng `agent_creds:` và việc phải làm với từng trạng thái · cách dùng `tl agent-creds-exec --gemini --
    agy …` và `--claude` · đổi khoá (`secrets-keygen` → `secrets-stage` mã hoá lại → `agent-creds-set`) · giới hạn trên Codex
    Cloud (mục `ngoai_pham_vi` đầu tiên). Không chứa giá trị credential.
11. → `RELEASE_MANIFEST.json`: tái sinh sau mục 10.

## `nghiem_thu`

Mọi ca của A–D nằm trong `ops/cloud_agent_creds_test.py`. Helper được chép vào một cây tạm `<tmp>/ops/cloud_agent_creds.py`
cùng `<tmp>/scripts/tl.py` **giả**. `tl.py` giả ghi `argv`, PID và biến môi trường đáng quan tâm vào một tệp nhật ký, rồi in,
ngủ hoặc thoát theo kịch bản của từng ca. Helper tìm `scripts/tl.py` theo vị trí của chính nó, nên test không cần móc vào mã
sản phẩm. Ca của `cai-agy` chạy in-process: import module, thay hàm tải bằng đồ giả ĐẾM lời gọi, thay bảng nền/băm bằng bảng
của tarball giả, đặt HOME tạm. Mỗi tiêu chí kèm đột biến làm nó đổi màu (L3). Đột biến chạy trên bản sao tạm, không bao giờ
ghi lên tệp thật.

| # | mục tiêu | tiêu chí | phép đo làm ĐỎ (đột biến) |
|---|---|---|---|
| A1 | 1 | `nap` thiếu `TL_MASTER_KEY` (vắng, và riêng một ca: chuỗi rỗng) ⇒ rc 0, đầu ra có **đúng 1** dòng chứa `agent_creds:` và dòng ấy là `agent_creds: BỎ QUA — thiếu TL_MASTER_KEY`; nhật ký `tl.py` giả: **0** lần chạy (đếm từng ca riêng) | gọi `bootstrap` bất kể khoá ⇒ ĐỎ (đếm 1) |
| A2 | 1 | `tl.py` giả in `[bootstrap] agent_creds: ĐÃ NẠP — rev=7` rồi rc 0 ⇒ đúng 1 dòng `agent_creds:`, bắt đầu bằng `agent_creds: ĐÃ NẠP — rev=7`; dòng `[bootstrap] agent_creds:` gốc KHÔNG còn trong đầu ra | chuyển tiếp nguyên văn (không lọc) ⇒ ĐỎ (2 dòng) |
| A3 | 1 | bảng sáu ca, đếm từng ca: rc 2 không in dòng agent · rc 3 không in · rc 0 in 2 dòng `agent_creds:` · rc 0 in `agent_creds: LẠ — x` · `tl.py` không thực thi được (xoá tệp) · rc 1 in `KHÔNG CẤU HÌNH` ⇒ mỗi ca rc 0 và đúng 1 dòng `agent_creds:`; năm ca đầu ra `KHÔNG ĐO ĐƯỢC` kèm lý do đúng loại (ghi `rc=2`/`rc=3`/`không đúng hợp đồng`/`không đúng hợp đồng`/`không chạy được`), ca cuối ra `KHÔNG CẤU HÌNH` | bỏ nhánh "0 dòng" (không in gì) ⇒ ĐỎ ở hai ca đầu; bỏ kiểm tập trạng thái ⇒ ĐỎ ở ca 4 |
| A4 | 1 | `TL_CLOUD_BOOTSTRAP_TIMEOUT_GIAY=2`, `tl.py` giả ngủ 60 s ⇒ `nap` xong trong < 20 s, rc 0, dòng `KHÔNG ĐO ĐƯỢC — bootstrap quá 2 s, đã dừng`; PID ghi trong nhật ký **không còn sống** sau khi `nap` thoát (zombie tính là chết — CLAUDE.md) | bỏ bước giết ⇒ ĐỎ (PID còn sống); bỏ timeout ⇒ ĐỎ (quá 20 s) |
| A5 | 1 | đọc timeout: `abc`, `-5`, `0`, `inf` ⇒ đều 180 (đo hàm đọc, từng giá trị riêng) | nhận `0` ⇒ ĐỎ |
| A6 | 1 | `argv` mà `tl.py` giả nhận đúng bằng `["bootstrap", "--env", "code", "--no-nlm"]` (so nguyên danh sách); trình thông dịch là `sys.executable` của helper | bỏ `--no-nlm` ⇒ ĐỎ; thêm `--require-agent-creds` ⇒ ĐỎ |
| A7 | 1 | `TL_MASTER_KEY` = sentinel riêng; `tl.py` giả in sentinel trong một dòng thường VÀ trong dòng `agent_creds:` ⇒ stdout+stderr của `nap` KHÔNG chứa sentinel (đo cả hai kênh) | bỏ bước thay `***` ⇒ ĐỎ |
| A8 | 1 | `nap` luôn rc 0 với `bootstrap` rc 0, 1, 2, 3, 4 và khi quá hạn; `nap --la` (đối số lạ) ⇒ rc 2 và `tl.py` 0 lần | trả rc của `bootstrap` ⇒ ĐỎ |
| B1 | 2 | chưa có `agy` ⇒ đồ giả tải đếm **1**, `~/.local/bin/agy` tồn tại, có bit thực thi (POSIX), nội dung bằng thành viên `antigravity` của tarball giả | không ghi tệp ⇒ ĐỎ |
| B2 | 2 | sha512 tarball giả ≠ hằng ⇒ `~/.local/bin/agy` KHÔNG được tạo (ca chưa có) và byte KHÔNG đổi (ca đã có bản cũ); có dòng `agy: ✗ sha512 lệch`; rc 0 | bỏ kiểm sha512 ⇒ ĐỎ |
| B3 | 2 | đã có `agy` giả in `antigravity 1.4.12` cho `--version` ⇒ đồ giả tải đếm **0** | luôn tải ⇒ ĐỎ |
| B4 | 2 | `agy` giả in `1.4.13` (lệch bản) ⇒ đếm **1** và tệp được thay; `agy` giả rc 1 khi gọi `--version` ⇒ đếm **1** | chỉ kiểm tệp có mặt ⇒ ĐỎ |
| B5 | 2 | nền giả `freebsd_amd64` ⇒ dòng `agy: CHƯA HỖ TRỢ freebsd_amd64`, đếm **0**, rc 0 | rơi về `linux_amd64` ⇒ ĐỎ |
| B6 | 2 | ba tarball độc: thành viên `../x` · thêm một thành viên thứ hai · `antigravity` là symlink ⇒ mỗi ca: không ghi gì ngoài thư mục tạm của ca và không tạo `~/.local/bin/agy` (đếm từng ca) | dùng `extractall` ⇒ ĐỎ ở ca `../x` |
| B7 | 2 | nhật ký lời gọi của `agy` giả chỉ chứa `--version`; KHÔNG có `install` | thêm lời gọi `agy install` ⇒ ĐỎ |
| B8 | 2 | bảng nền trong `ops/cloud_agent_creds.py` (bản THẬT, không phải bản test đã thay) có đúng 6 khoá của mục *Hằng ghim*, và từng URL/sha512 bằng nguyên văn bảng ấy (so 6 cặp riêng); `AGY_VER == "1.4.12"` | đổi một ký tự sha512 ⇒ ĐỎ |
| B9 | 2 | luật chọn nền: (`Linux`,`x86_64`, không musl) ⇒ `linux_amd64`; (`Linux`,`aarch64`, musl) ⇒ `linux_arm64_musl`; (`Darwin`,`arm64`) ⇒ `darwin_arm64`; (`Linux`,`i686`) ⇒ ngoài bảng (đo hàm chọn, bốn vế riêng) | bỏ nhận diện musl ⇒ ĐỎ |
| C1 | 3 | settings có sẵn `{"a": 1, "modelProvider": "x"}` ⇒ sau `cai-agy` là `{"a": 1, "modelProvider": "gemini"}` (so dict); chưa có ⇒ `{"modelProvider": "gemini"}` | ghi đè cả tệp ⇒ ĐỎ (mất `a`) |
| C2 | 3 | settings là `[1,2]` và là `{không phải json` ⇒ byte tệp KHÔNG đổi (so sha256 trước/sau), có dòng cảnh báo; rc 0 | ghi đè khi parse lỗi ⇒ ĐỎ |
| C3 | 3 | `GEMINI_API_KEY`, `GOOGLE_API_KEY` = sentinel trong môi trường ⇒ settings.json KHÔNG chứa sentinel | ghi `apiKey` từ môi trường ⇒ ĐỎ |
| D1 | 4 | `CLAUDE_ENV_FILE` trỏ tệp tạm có sẵn một dòng khác; chạy `cai-agy` **hai** lần ⇒ tệp có đúng **1** dòng `export AGY_CLI_DISABLE_AUTO_UPDATE=1` và dòng cũ còn nguyên | nối mỗi lượt ⇒ ĐỎ (2 dòng) |
| D2 | 4 | `CLAUDE_ENV_FILE` không đặt ⇒ rc 0, không tạo tệp nào ở cwd/HOME tạm | — (ca biên; đột biến D1 đã phủ nhánh ghi) |
| H1 | 5 | trong `.claude/hooks/session-start.sh`: hai dòng đánh dấu mỗi dòng xuất hiện **đúng 1** lần; khối nằm SAU dòng `# --- phụ thuộc Python của kho` và TRƯỚC dòng đầu tiên chứa `codex_env_policy.py` (so số dòng); trong khối, `cloud_agent_creds.py nap` và `cloud_agent_creds.py cai-agy` mỗi thứ đúng 1 lần, `nap` đứng trước. Ngoài khối: 0 lần (đếm từng chuỗi riêng — L6c). Vế âm trên base: 0 lần | dời khối ra sau `doctor` ⇒ ĐỎ |
| H2 | 5 | trích khối giữa hai dòng đánh dấu từ CHÍNH tệp hook (không chép lại), chạy bằng `bash -c 'set -euo pipefail; …'` với `PY` trỏ một script giả thoát rc 3 và `GOC` trỏ cây tạm ⇒ bash rc 0 và có in `[session-start] ` (POSIX; Windows: bỏ qua có lý do, chỉ khi `LA_WINDOWS`) | bỏ `|| true` ⇒ ĐỎ |
| H3 | 5 | dòng `# hook-nang-luc:` chứa nguyên từ `agent-creds-bootstrap` và `agy-ghim` (tách theo khoảng trắng, so phần tử); mọi tên cũ của base vẫn còn (so tập: tập cũ ⊆ tập mới) | xoá một tên cũ ⇒ ĐỎ |
| E1 | 6 | trong `ops/codex_cloud_setup.sh`: `cloud_agent_creds.py nap` đúng 1 lần, nằm trong thân `main` và sau dòng `pip install --quiet -r requirements.txt`; `cai-agy` 0 lần trong tệp. Vế âm trên base: 0 lần | gọi trước pip ⇒ ĐỎ |
| E2 | 6 | trích dòng gọi `nap` từ chính tệp, chạy dưới `set -euo pipefail` với `PY` giả rc 3 ⇒ rc 0 | bỏ `|| true` ⇒ ĐỎ |
| F1 | 7, 9 | `python ops/cloud_agent_creds_test.py` thoát 0 và dòng tổng kết khớp mẫu đã đăng ký; số ca đạt = tổng số ca > 0 và số mutant bị giết đúng lý do = tổng số mutant > 0 (bằng chứng dương, không tin rc — CLAUDE.md r244) | một mutant sống ⇒ ĐỎ; xoá dòng đăng ký ⇒ `ci_dang_ky_test.py` ĐỎ |
| F2 | 7 | tự kiểm bộ phân hạng: một mutant chết vì `AttributeError` đi qua một `except` đổi kiểu thành `AssertionError` ⇒ bị xếp TÍN DỤNG GIẢ; assertion của một ca KHÁC ca đích ⇒ TÍN DỤNG GIẢ | phân hạng theo chuỗi `AssertionError` ⇒ ĐỎ |
| F3 | 8 | `python ops/codex_cloud_setup_test.py` in `N/N` với hai số bằng nhau; N tăng đúng bằng số ca E mới | — (đột biến E1/E2 đã phủ) |
| R1 | 10 | trong `references/RUNBOOK.md`, tiêu đề mục chứa `A0.4e` xuất hiện đúng 1 lần (vế âm: base 0 lần — đo 05:0xZ 31-10). Trên **văn bản mục A0.4e đã gộp khoảng trắng theo từng đoạn** (L6b), có đủ các cụm: `TL_MASTER_KEY`, `agent-creds-exec --gemini`, `agent_creds:`, `ĐÃ NẠP`, `KHÔNG CẤU HÌNH`, `KHÔNG ĐO ĐƯỢC`, `BỎ QUA`, `secrets-keygen`, `agent-creds-set`, `Codex Cloud` (đếm từng cụm riêng). Mục ≤ 60 dòng | xoá một trạng thái khỏi bảng ⇒ ĐỎ |
| R2 | 10 | mục A0.4e không chứa chuỗi khớp `sk-ant-`, `AIza`, hay dãy ≥ 40 ký tự `[A-Za-z0-9_-]` liền nhau (40 chứ không 32: fileId Drive công khai dài 33 ký tự được phép nhắc; token Claude đo được 108 ký tự, khoá Gemini 53 ký tự — đặc tả P2a, bước LIVE 4) | dán một khoá giả ⇒ ĐỎ |
| J1 | 11 | `python scripts/tl.py release-verify RELEASE_MANIFEST.json --strict --json` ⇒ `ok=true`, `expected == checked` | sửa một byte RUNBOOK sau tái sinh ⇒ ĐỎ |
| G1 | — | `python scripts/tl.py --selftest` (Ubuntu, `core.abbrev=7`): delta so base = 0 ca đỏ mới (đơn vị: ca selftest; nền đo lại trên base lúc cấp lease) | một ca đạt trên base mà đỏ trên head ⇒ ĐỎ |
| G2 | — | `python .claude/dev/launcher.py doctor` trên head: mục `hook-phien` không báo THIẾU năng lực | xoá tên cũ khỏi dòng hợp đồng ⇒ ĐỎ |
| G3 | — | `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0 | — (canh bất biến; xanh sẵn trên nền) |
| K1 | — | `ruff check --select F` trên `ops/cloud_agent_creds.py` và `ops/cloud_agent_creds_test.py` ⇒ 0; các `.py` khác của write set: delta so base = 0 | thêm tên chưa định nghĩa ⇒ ĐỎ |
| K2 | — | `git diff --numstat origin/master...HEAD` ⇒ ≤ 8 tệp và ≤ 600 dòng thêm (tổng mọi tệp), và mọi tệp đều thuộc `write_set` | vượt hoặc có tệp lạ ⇒ ĐỎ; DỪNG hỏi chủ kho |
| L1 | — | lượt CI PR (Ubuntu) trên head ứng viên: mọi job bắt buộc theo `ci.yml` lúc nghiệm thu đều `success`; đọc nhãn job, không suy từ tên workflow (CLAUDE.md, bài học (c)). Không đòi lượt Windows (vòng 2 Q20) | một job bắt buộc đỏ do packet ⇒ ĐỎ |
| M1 | 2, 3, 5 (LIVE) | phiên Claude Code web **mới** trên head ứng viên (hoặc master sau land), có `TL_MASTER_KEY`; chủ kho duyệt riêng trước khi chạy. (i) log hook có đúng 1 dòng `[session-start] agent_creds: ĐÃ NẠP — …`; (ii) `command -v agy` ⇒ `~/.local/bin/agy`; (iii) `agy --version` chứa `1.4.12`; (iv) `python scripts/tl.py agent-creds-exec --gemini -- agy models` ⇒ rc 0, ≥ 1 dòng tên model, và đầu ra KHÔNG chứa `modelProvider is set to` hay `Both GOOGLE_API_KEY and GEMINI_API_KEY`. Biên nhận chỉ ghi rc, số dòng, phiên bản; không ghi giá trị | `chưa đo được` cho tới khi chạy thật. Vế (iv) là phép đo DUY NHẤT xác nhận enum `"gemini"` đúng: có câu `modelProvider is set to` ⇒ ĐỎ, và không được thay bằng phép đo khác. Ai đo: executor hoặc phiên điều phối, sau khi chủ kho duyệt |
| M2 | 6 (LIVE, sau land) | chủ kho dựng lại một môi trường Codex Cloud có `TL_MASTER_KEY` ⇒ log setup có đúng 1 dòng `agent_creds: …`; ghi lại trạng thái quan sát được | `chưa đo được` cho tới khi chủ kho chạy. Ai đo: chủ kho; phiên điều phối đọc lại log chủ kho dán |

Ghi chú L6. H1, E1, R1 có vế dương trên head và vế âm trên base (L6a). R1 đo trên văn bản đã gộp khoảng trắng theo từng đoạn
của đúng mục A0.4e (L6b). H2, E2 không khớp chuỗi mà chạy thật đoạn trích. A1, A3, B6, H1, R1 đếm từng ca hoặc từng chuỗi riêng
(L6c). Không có lời khai số lượng dạng chữ (L6d). Không có lời khai "không cổng nào cưỡng chế" (L6e).

Chạy thử trên nền (05:01Z 31-10, `01ff6503`), tức các tiêu chí đo được trước khi có mã: H1, E1, R1 (vế dương), H3 (hai tên mới)
đều ra màu "chưa làm" (0 lần). A–D, F chưa chạy được vì tệp test chưa tồn tại, và đó cũng là trạng thái "chưa làm". G3 xanh sẵn
trên nền vì nó canh bất biến.

## Kích thước dự kiến

**Ước tính, chưa đo** (05:01Z 31-10). Helper ~150, test ~280, `codex_cloud_setup_test.py` ~30, RUNBOOK ~60, hook ~20, setup
~8, manifest ~2, đăng ký 1 ⇒ **khoảng 550 dòng thêm trên 8 tệp**. Đối chiếu: các commit trước trên `codex_cloud_setup*` ra
+81/+221 (`cab2f74d`), +17/+26 (`b2a36bdc`), +16/+52 (`2a3dc1a9`). Trần 8 tệp / 600 dòng. Lời gọi Codex theo `ADR-0052`
(**8**, vòng 2 Q19). Lời gọi thứ 8 chưa approve ⇒ Review Rescue Checkpoint (`ADR-0037`). Trước MỖI lời gọi Codex, đếm số lời
gọi đã dùng (CLAUDE.md, bài học trần lời gọi Codex).

## `hinh_dang_ke_thua`

`khong_ap_dung` — packet này không khắc phục packet nào. Ghi chú từ P1/P2a cho người thi hành:
- P2a (#1063) dùng hết 8/8 lời gọi Codex. Bốn finding liên tiếp (F01/F03/F04/F06) cùng một hình dạng "guard đọc tên lệnh khác
  Bash", và chủ kho phải đảo cấu trúc (S5). Ở packet này, lớp tương tự dễ tái phát nhất là **đầu ra của `bootstrap` không đúng
  hợp đồng** và **tarball độc**. Hai lớp ấy đã có ca A3 và B6; một finding cùng hình dạng lần thứ ba ⇒ dừng, hỏi chủ kho có
  nên đổi cấu trúc không, đừng vá tiếp.
- P1 vượt trần ba lần vì write set thiếu tệp cơ học. Ở packet này, manifest và dòng đăng ký CI đã nằm sẵn trong write set.

## `chua_do_duoc`

- **Giá trị enum `"gemini"` của `modelProvider`**: chỉ suy từ #1039 và chuỗi tĩnh. Đo ở M1 vế (iv).
- **`agy` có đọc `AGY_CLI_DISABLE_AUTO_UPDATE` không**: tên biến có trong nhị phân, hành vi chưa đo. Chốt thật là `cai-agy`
  kiểm lại bản mỗi phiên (mục tiêu 2), không phải biến này (vòng 2 Q16).
- **`CLAUDE_ENV_FILE` có được đặt khi hook SessionStart của kho chạy qua `session_start.py` không**: chưa đo. Đo 05:0xZ trong
  phiên soạn: biến vắng trong phiên agent, nhưng phép đo ấy không nói gì về lúc hook chạy. Executor ghi kết quả quan sát ở M1.
- **Secret của Codex Cloud có bị gỡ trước giai đoạn agent không**: theo tài liệu thì có, nhưng chưa đo trên kho này.
- **Thời gian chạy `bootstrap --env code --no-nlm` trong container cloud**: chưa đo. Phiên soạn không chạy `bootstrap` vì lệnh
  ấy ghi credential ra đĩa. Nếu M1 cho thấy 180 s không đủ thì ra revision mới.
- **Tarball của năm nền ngoài `linux_amd64`**: mới đọc manifest, chưa tải để kiểm băm.
- **Windows**: không đo. Hook không chạy trên máy cục bộ (vòng 1 Q11).
