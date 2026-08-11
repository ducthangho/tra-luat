---
probe_date: '2026-08-11'
host: ASUS-LAPTOP
purpose: 'Xác minh Claude (qua bridge) gọi được Codex phi tương tác — nền cho A5-01/A7-02'
codex_version: 'codex-cli 0.146.0'
non_interactive_supported: true
---

# PROBE 11-08-2026 — năng lực Codex CLI phi tương tác (ASUS-LAPTOP)

Đo lại trên máy ASUS-LAPTOP, repo `D:\Quốc hội\tra-luat`, ngày 11-08-2026.
Mọi rc/output dưới đây chép nguyên văn từ lượt chạy thật của phiên này (không phải trích lại).
Không chạy packet thật, không mở PR, không deploy.

## 1. Bảng lệnh → rc → kết luận

| # | Lệnh | rc | Output rút gọn | Kết luận |
|---|------|----|----|----|
| 1 | `where codex` | 0 | `D:\Program Files\nodejs\codex`<br>`D:\Program Files\nodejs\codex.cmd` | Có trên PATH, cài qua npm global (nodejs dir) |
| 2 | `codex --version` | 0 | `codex-cli 0.146.0` | Bản đang cài |
| 3 | `codex exec --help` | 0 | (nguyên văn ở §3) | Subcommand `exec` = "Run Codex non-interactively" |
| 4 | `codex exec` (không prompt, `< /dev/null`) | **1** | `Reading prompt from stdin...`<br>`No prompt provided via stdin.` | Không TTY vẫn dispatch được; thiếu prompt thì lỗi SẠCH rc=1, không treo, không rơi vào TUI |
| 5 | `codex exec -a never "noop" < /dev/null` | **2** | `error: unexpected argument '-a' found` | **`-a` KHÔNG tồn tại ở `exec`** (chỉ ở top-level `codex`) |
| 6 | `codex exec --skip-git-repo-check -s read-only "reply with exactly: OK" < /dev/null` | **0** | stdout = `OK` (đúng 1 lần) | **Vòng lặp agent chạy trọn headless.** Đây là bằng chứng dương cho `non_interactive_supported: true` |
| 7 | `powershell -NoProfile -Command "$null \| codex exec --skip-git-repo-check -s read-only 'reply with exactly: PSOK'"` | 0 | `PSOK` | Đường PowerShell chạy được — nhưng phải dùng `$null \|`, xem gotcha #1 |
| 8 | `powershell -NoProfile -Command "codex exec --help < $null"` | — | `The '<' operator is reserved for future use.` (ParserError) | **PowerShell KHÔNG có toán tử `<`** — idiom `< /dev/null` của bash KHÔNG bê thẳng sang được |
| 9 | `codex login status` | 0 | `Logged in using ChatGPT` | Đã đăng nhập, không cần API key env |
| 10 | `codex exec --help \| grep -ic timeout` | — | `0` | **Không có cờ timeout nào** |

`grep -nE '^\s+-a,\|ask-for-approval'`: khớp ở `codex --help` **dòng 105**; KHÔNG khớp trong `codex exec --help` (rc=1).

## 2. Trạng thái auth — `%USERPROFILE%\.codex\`

Chỉ liệt kê tên + mtime, không đọc nội dung.

| Tên | mtime |
|---|---|
| `auth.json` | 2026-08-04 08:40 |
| `config.toml` | 2026-08-10 11:46 |
| `models_cache.json` | 2026-08-11 18:24 |
| `session_index.jsonl` | 2026-08-11 18:16 |
| `sessions/` (dir) | 2026-06-21 01:48 |
| `.codex-global-state.json` | 2026-08-11 18:23 |

Suy ra: `auth.json` tồn tại và `codex login status` trả `Logged in using ChatGPT`
⇒ **đã đăng nhập bằng tài khoản ChatGPT** (không dùng `OPENAI_API_KEY`).
`models_cache.json` được ghi trong ngày ⇒ CLI có gọi mạng thành công.

## 3. Nguyên văn `codex exec --help`

```
Run Codex non-interactively

Usage: codex exec [OPTIONS] [PROMPT]
       codex exec [OPTIONS] <COMMAND> [ARGS]

Commands:
  resume  Resume a previous session by id or pick the most recent with --last
  review  Run a code review against the current repository
  help    Print this message or the help of the given subcommand(s)

Arguments:
  [PROMPT]
          Initial instructions for the agent. If not provided as an argument (or if `-` is used),
          instructions are read from stdin. If stdin is piped and a prompt is also provided, stdin
          is appended as a `<stdin>` block

Options:
  -c, --config <key=value>
          Override a configuration value that would otherwise be loaded from `~/.codex/config.toml`.
          Use a dotted path (`foo.bar.baz`) to override nested values. The `value` portion is parsed
          as TOML. If it fails to parse as TOML, the raw string is used as a literal.

          Examples: - `-c model="o3"` - `-c 'sandbox_permissions=["disk-full-read-access"]'` - `-c
          shell_environment_policy.inherit=all`

      --enable <FEATURE>
          Enable a feature (repeatable). Equivalent to `-c features.<name>=true`

      --disable <FEATURE>
          Disable a feature (repeatable). Equivalent to `-c features.<name>=false`

      --strict-config
          Error out when config.toml contains fields that are not recognized by this version of
          Codex

  -i, --image <FILE>...
          Optional image(s) to attach to the initial prompt

  -m, --model <MODEL>
          Model the agent should use

      --oss
          Use open-source provider

      --local-provider <OSS_PROVIDER>
          Specify which local provider to use (lmstudio or ollama). If not specified with --oss,
          will use config default or show selection

  -p, --profile <CONFIG_PROFILE_V2>
          Layer $CODEX_HOME/<name>.config.toml on top of the base user config

  -s, --sandbox <SANDBOX_MODE>
          Select the sandbox policy to use when executing model-generated shell commands

          [possible values: read-only, workspace-write, danger-full-access]

      --dangerously-bypass-approvals-and-sandbox
          Skip all confirmation prompts and execute commands without sandboxing. EXTREMELY
          DANGEROUS. Intended solely for running in environments that are externally sandboxed

      --dangerously-bypass-hook-trust
          Run enabled hooks without requiring persisted hook trust for this invocation. DANGEROUS.
          Intended only for automation that already vets hook sources

  -C, --cd <DIR>
          Tell the agent to use the specified directory as its working root

      --add-dir <DIR>
          Additional directories that should be writable alongside the primary workspace

      --skip-git-repo-check
          Allow running Codex outside a Git repository

      --ephemeral
          Run without persisting session files to disk

      --ignore-user-config
          Do not load `$CODEX_HOME/config.toml`; auth still uses `CODEX_HOME`

      --ignore-rules
          Do not load user or project execpolicy `.rules` files

      --output-schema <FILE>
          Path to a JSON Schema file describing the model's final response shape

      --color <COLOR>
          Specifies color settings for use in the output

          [default: auto]
          [possible values: always, never, auto]

      --json
          Print events to stdout as JSONL

  -o, --output-last-message <FILE>
          Specifies file where the last message from the agent should be written

  -h, --help
          Print help (see a summary with '-h')

  -V, --version
          Print version
```

## 4. Bảng cờ CÓ / KHÔNG trên `codex exec`

| Cờ | CÓ ở `exec`? | Ghi chú |
|---|---|---|
| `--output-schema <FILE>` | **CÓ** | JSON Schema tả hình dạng câu trả lời cuối |
| `-o, --output-last-message <FILE>` | **CÓ** | Ghi message cuối ra tệp — kênh lấy kết quả DUY NHẤT đáng tin |
| `-C, --cd <DIR>` | **CÓ** | Thư mục gốc làm việc của agent |
| `-s, --sandbox <MODE>` | **CÓ** | `read-only` \| `workspace-write` \| `danger-full-access` |
| `-a, --ask-for-approval` | **KHÔNG** | Chỉ có ở top-level `codex` (dòng 105 của `codex --help`). Truyền vào `exec` ⇒ **rc=2, chết parse**. Ở `exec`, approval điều khiển gián tiếp qua `-s` |
| `-m, --model <MODEL>` | **CÓ** | Mặc định quan sát được: `gpt-5.6-sol` |
| `--skip-git-repo-check` | **CÓ** | Cho chạy ngoài repo git |
| Cờ timeout | **KHÔNG** | Không có cờ nào. `grep -ic timeout` trên help = `0`. **Parent phải tự giữ timeout và tự giết process** |
| Cờ JSON output | **CÓ** — `--json` | In events dạng JSONL ra stdout (`thread.started` `turn.started` `item.completed` `turn.completed`) |
| `--add-dir <DIR>` | CÓ | Thêm thư mục ghi được ngoài workspace chính |
| `--ephemeral` | CÓ | Không lưu session xuống đĩa |
| `--ignore-user-config` / `--ignore-rules` | CÓ | Bỏ `config.toml` / bỏ `.rules` |
| `-p, --profile` | CÓ | Layer `$CODEX_HOME/<name>.config.toml` |
| `-c key=value` | CÓ | Override config, value parse như TOML |

## 5. BỐN GOTCHA — phần quan trọng nhất

### Gotcha #1 — Bẫy stdin: `exec` VẪN đọc stdin dù đã truyền prompt bằng đối số

Đây là bẫy nguy hiểm nhất vì hậu quả là **treo vô hạn**, không phải lỗi.

Bằng chứng lượt này (stderr của lượt #6, đã có prompt đối số hẳn hoi):

```
Reading additional input from stdin...
```

Nếu stdin là pipe **không bao giờ đóng** (đúng tình huống khi một process cha spawn Codex và giữ
pipe stdin mở — tức chính kiến trúc bridge của A5-01/A7-02), Codex **đứng chờ EOF mãi mãi**.
Có `< /dev/null` thì gặp EOF ngay rồi chạy tiếp.

Không có prompt và stdin rỗng thì nó báo sạch:

```
Reading prompt from stdin...
No prompt provided via stdin.
```
rc = **1**.

**Chốt: LUÔN đóng stdin.** Và lưu ý idiom khác nhau theo shell — xem gotcha #2.

Cùng họ với bài học `$Args`/rc=0 trong `CLAUDE.md`: một chi tiết dispatch im lặng làm hỏng toàn bộ vòng.

### Gotcha #2 — PowerShell KHÔNG có toán tử `<`; phải dùng `$null |`

`< /dev/null` là idiom bash. Trên PowerShell (đo: `5.1.26100.8972`; PS7 giống hệt) nó là **lỗi cú pháp**:

```
At line:1 char:19
+ codex exec --help < $null
+                   ~
The '<' operator is reserved for future use.
    + CategoryInfo          : ParserError: (:) [], ParentContainsErrorRecordException
```

Nghĩa là: viết `< $null` hay `< NUL` trong `.ps1` thì **script chết ngay lúc parse**, chưa từng gọi Codex.

Idiom đúng cho PowerShell — đã đo rc=0 (lượt #7):

```powershell
$null | codex exec --skip-git-repo-check -s read-only 'reply with exactly: PSOK'
```

`$null |` đẩy một pipeline RỖNG ⇒ Codex thấy EOF ngay ⇒ không treo.
(Cách khác nếu buộc phải dùng cú pháp cmd: `cmd /c "codex exec ... < NUL"`.)

Đây là gotcha riêng của đường Windows và đúng loại lỗi mà `CLAUDE.md` §"Script đa nền" đã cảnh báo:
bản `sh` và bản `ps1` sẽ TRÔI LỆCH đúng ở dòng này nếu chép qua chép lại.

### Gotcha #3 — Hai thứ đọc-nhầm-thành-lỗi trên stderr / stdout

**(a) Dòng `ERROR` LÀNH TÍNH luôn có mặt.** Lượt #6 rc = **0** nhưng stderr vẫn in:

```
2026-08-11T11:28:28.416815Z ERROR codex_models_manager::cache: failed to load models cache: missing field `base_instructions` at line 94 column 5
```

⇒ **Đừng grep chuỗi `ERROR` để phán fail.** Làm thế thì mọi lượt chạy THÀNH CÔNG đều bị xếp là hỏng.

**(b) Câu trả lời cuối bị in ĐÚP nếu gộp stream.** Khi stdout KHÔNG phải TTY, Codex tách sạch:
stdout chỉ có message cuối (`OK`, đúng 1 lần), toàn bộ transcript + header đi stderr.
Nhưng lượt #7 chạy qua PowerShell với `2>&1` thì `PSOK` xuất hiện **hai lần** — một lần trong
transcript, một lần là message cuối.

⇒ **Đừng `2>&1` rồi parse stdout thô.** Lấy kết quả qua `-o <FILE>`: đó là JSON/text sạch, không lẫn
transcript, không đếm đúp. Đây là lý do `-o` không phải tuỳ chọn tiện nghi mà là **bắt buộc** cho bridge.

### Gotcha #4 — Không có timeout; và `-s` trên Windows chỉ là LỜI KHAI, không phải cưỡng chế

**(a) Không cờ timeout.** `grep -ic timeout` trên help = `0`. Codex sẽ chạy đến khi xong hoặc chết.
Đã có tiền lệ trả giá: một lượt cross-review **40 phút không ra verdict** phải giết bằng TaskStop.
⇒ **Process cha BẮT BUỘC tự giữ timeout** (bash `timeout N ...`; PowerShell `Wait-Process -Timeout` +
`Stop-Process`). Lượt #6 phiên này chạy dưới `timeout 180`.

**(b) Phạm vi phải khoá bằng sandbox biệt lập, không chỉ bằng `-C`.** Trỏ `codex exec` vào một worktree
mà prompt để phạm vi mở thì nó **quét ra ngoài kho**: `rg` lên `C:\Users\admin`, đọc cả
`.claude/projects/**` (transcript phiên Claude Code), sinh 1.3 MB output. Cách chạy đúng: dựng sandbox
biệt lập chứa sẵn `SPEC.md` · `diff.patch` · `numstat.txt` · `EVIDENCE.md` · bản sao cây, rồi
`-s workspace-write -C <sandbox>` kèm câu CẤM đọc ra ngoài thư mục đó.

Và quan trọng: parser chấp nhận `-s read-only` **KHÔNG** nói gì về việc kernel có cưỡng chế hay không —
Windows không có user/network/pid namespace kiểu Linux. Trên nền này `-s` gần như là khai báo ý định.
Đây chính là lý do wp86 chuyển sang cloud/Linux runner.

**Phụ chú chi phí:** header lượt chạy cho thấy mặc định là `reasoning effort: xhigh` — mặc định ĐẮT.
Việc cơ học nên ghim thấp hơn qua `-c`.

## 6. Cú pháp CHÍNH XÁC để chạy một packet

### Bash / Linux / Cowork

```bash
timeout 3600 codex exec \
  -C "$CODEX_WT" \
  -s workspace-write \
  --output-schema "$HANDOFF_SCHEMA" \
  -o "$HANDOFF_JSON" \
  "$PACKET_PROMPT" \
  < /dev/null
echo "rc=$?"
```

### PowerShell / Windows

```powershell
$CodexWt       = 'D:\Quốc hội\tra-luat-wt\wp101-codex'
$HandoffSchema = 'D:\Quốc hội\tra-luat\.github\coordination\schemas\handoff.v1.schema.json'
$HandoffJson   = 'D:\Quốc hội\tra-luat-wt\wp101-codex\.coord\handoff.json'
$PacketPrompt  = 'Thực thi packet wp101 từ Issue <URL> theo Protocol v1. Chỉ đọc/ghi trong thư mục làm việc này.'

$null | codex exec -C $CodexWt -s workspace-write `
  --output-schema $HandoffSchema -o $HandoffJson $PacketPrompt
"rc=$LASTEXITCODE"
```

Kiểm kết quả: đọc `$HandoffJson`, **không** parse stdout. rc=0 mà `$HandoffJson` không tồn tại /
không parse được JSON ⇒ coi như **CHƯA xong** (doctrine "rc=0 là cổng có thể bị lừa" của `CLAUDE.md`).

## 7. Đối chiếu §8.3 của `docs/KE_HOACH_TRIEN_KHAI_PROTOCOL_DA_PHIEN.md`

Lệnh trong kế hoạch (dòng 470):

```powershell
codex exec -C $CodexWt -s workspace-write --output-schema $HandoffSchema -o $HandoffJson $PacketPrompt
```

**Phần ĐÚNG:** cả 5 cờ đều tồn tại trên bản `codex-cli 0.146.0` đang cài, đúng dạng, đúng vị trí
(`exec` đứng trước cờ), và `-s workspace-write` là giá trị hợp lệ. `$CodexWt` có được gán ở dòng 448.
Lệnh này sẽ **parse thành công**.

**Phần SAI / THIẾU — 3 điểm:**

1. **THIẾU đóng stdin ⇒ rủi ro TREO.** Đây là lỗi nặng nhất. Chạy tay trong PowerShell tương tác thì
   may mà thoát (terminal cấp EOF khi gõ Ctrl-Z), nhưng khi lệnh này chạy từ script hoặc từ bridge
   (đúng kịch bản "headless sau A7" mà chính §8.3 đang mô tả) và stdin là pipe của process cha, nó
   **đứng chờ mãi**. Phải thêm `$null |` ở đầu.
2. **THIẾU timeout.** `codex exec` không có cờ timeout nào; kế hoạch cũng không nói ai giữ. Phải nêu rõ
   process cha chịu trách nhiệm giết theo hạn.
3. **`$HandoffSchema` trỏ tới tệp CHƯA TỒN TẠI.** `.github/coordination/schemas/` hiện chỉ có
   `change-impact.v1.schema.json` (trên `master`); trên nhánh `claude/wp86-cloud-linux-migration-ix5keq`
   thư mục `schemas/` chưa có. Chưa tạo `handoff.v1.schema.json` thì lệnh sẽ chết ngay khi mở tệp.

**Điểm cần cảnh báo thêm (không phải lỗi cú pháp):** `-s workspace-write` trên Windows **không được
kernel cưỡng chế** như trên Linux — xem gotcha #4(b). Kế hoạch không nên coi nó là hàng rào an ninh.

Sửa tối thiểu cho dòng 470: thêm `$null |` ở đầu, và ghi chú timeout + điều kiện tồn tại schema.

## 8. Kết luận

**Codex gọi phi tương tác ĐƯỢC** trên ASUS-LAPTOP với `codex-cli 0.146.0`, đã đăng nhập ChatGPT,
đã đo end-to-end rc=0 cả trên bash lẫn PowerShell. `--output-schema` + `-o` + `--json` đủ để làm
kênh handoff có cấu trúc cho A5-01/A7-02.

Ba điều kiện BẮT BUỘC của bridge: **đóng stdin** (idiom khác nhau theo shell) · **cha tự giữ timeout** ·
**lấy kết quả qua `-o`, không parse stdout**. Và trên Windows, `-s` không thay được sandbox thật.
