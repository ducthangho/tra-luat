---
name: work-packet
description: Thực thi MỘT work packet của protocol đa phiên (tra-luat) trên nền Claude Code. Chỉ chứa cú pháp và công cụ của nền; mọi quy tắc, schema và tiêu chí hoàn tất nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-packet]"
---

# Adapter `work-packet` — Claude Code

**Đọc trước, không làm theo trí nhớ:** `docs/PROTOCOL_DA_PHIEN.md` §13 (trình tự bắt buộc, điều kiện
từ chối việc, định nghĩa hoàn tất) · §3.2 (schema packet) · §5 (write set) · §7 (handoff) ·
§12 (điều kiện dừng) · §3.2.1 (spec nguồn và ba mốc Git) · §10.2.1–§10.2.3
(preflight, provenance và evidence thiếu). Quy trình sửa code của kho: `CLAUDE.md`.

Tệp này **không tóm tắt** những mục trên. Tóm tắt là bản sao, và bản sao thì trôi lệch — ba lượt
review liên tiếp đã bắt được đúng lỗi đó ở chính adapter này. Nay có chốt cơ học:

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY" .claude/dev/packet_loop.py doctrine-scan --root . \
  --path .agents/skills/work-packet/SKILL.md \
  --path .agents/skills/cross-review/SKILL.md \
  --path .agents/skills/land-packets/SKILL.md
```

Dưới đây chỉ có cú pháp của nền.

## Lấy spec

```bash
gh api graphql -f query='{repository(owner:"ducthangho",name:"tra-luat"){issue(number:55){body}}}'
```

`gh issue view 55 --json body --jq .body` cũng lấy body; `-q` riêng không chọn JSON output.
Công thức `spec_hash` và nguồn blob: protocol §3.2.1. Ví dụ lưu bytes blob ra scratch bằng
Python (các biến Bash dưới đây do phiên điền từ assignment, không chạy nguyên placeholder):

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -c 'import hashlib,pathlib,subprocess,sys; b=subprocess.run(["git","show",sys.argv[1]+":"+sys.argv[2]],check=True,capture_output=True).stdout; pathlib.Path(sys.argv[3]).write_bytes(b); print(hashlib.sha256(b).hexdigest())' "$SPEC_OID" "$SPEC_PATH" "$SCRATCH/spec.md"
```

## Dựng worktree

```bash
git rev-parse --is-shallow-repository        # đòi false trước khi tin bất kỳ phép so lịch sử nào
git config core.autocrlf false && git config core.eol lf && git config core.abbrev 7
export PYTHONDONTWRITEBYTECODE=1
export PYTHONPYCACHEPREFIX="$SCRATCH/pycache"
```

## Công cụ — nhánh packet KHÔNG mang công cụ của kho

`base_sha` thường cũ hơn công cụ trên nhánh chính, nên cây làm việc của packet có thể
thiếu cả bộ dựng công cụ lẫn hook phiên, và `settings.json` bản cũ có thể chưa đăng ký
`SessionStart`. Kho gắn giữa phiên thì hook cũng không chạy. Ba chuyện độc lập, mỗi
chuyện một mình đã đủ để phiên mở ra mà không có `codex`/`rg`.

Lấy công cụ TỪ NHÁNH CHÍNH, đừng chạy cả hook phiên chỉ để lấy một thứ — hook có bước
cài phụ thuộc Python và đã đo được một lần làm hỏng môi trường đang tốt:

```bash
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" "$CANON/.claude/dev/launcher.py" doctor
```

**Vắng mặt là một QUAN SÁT; "môi trường không có" là một KẾT LUẬN.** Trước khi báo với
người điều phối rằng không gọi được một CLI, phải chạy `command -v <tool>` và
`<tool> login status` trong CHÍNH phiên này, rồi loại trừ xong hai khả năng còn lại: hook
chưa chạy, và nhánh đang checkout không mang hook. Tài liệu mô tả một lần đo trong quá
khứ trên một cây khác — nó không phải quan sát về phiên đang chạy. Đã trả giá:
một phiên báo cross-review không chạy được, trong khi CLI cài được và lượt review sau đó
tìm ra một P1 thật.

Kiểm biến bí mật bằng **sự tồn tại**, không bao giờ in nội dung — biến khôi phục đăng
nhập chứa refresh token, in một lần là phải thu hồi và cấp lại:

```bash
if [ -n "${TEN_BIEN:-}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi
```

Đừng nối `${VAR:+…}` với `${VAR:-…}` trong cùng một chuỗi: `:-` chỉ thay thế khi biến
**rỗng hoặc chưa đặt**, nên ở nhánh "đã đặt" — nhánh người ta thật sự chạy — nó bung ra
**chính giá trị**. Bản trước của dòng này in `có, 27 ký tự` rồi in luôn cả token.

## Gate

Chọn lệnh theo protocol §10.1/§10.2 và Packet: `/gate-targeted` hoặc `/gate` khi scope cho phép.
`$CANON` là checkout mã canonical đã ghim, `$S` là OID của nó, `$H` là candidate có trong
object store của `$CANON`; `$SCRATCH` ở ngoài checkout. Ví dụ Bash, giữ rc cả khi bật `set -e`:

Admission này cần Linux/POSIX; Git Bash với Python native Windows không đáp ứng bộ giải
Git `/usr/bin:/bin` của checker. Nhánh không hỗ trợ và handoff theo §10.2.1. Khi dùng WSL
được cấp, probe trong distribution đã chọn; `$CANON` là clone Linux đọc được object store
(không giả định linked worktree Windows dùng được trong WSL). Bootstrap chuẩn bị clone tại
`$S`, có object `$H`; không fetch/checkout cây nguồn từ đoạn dưới.

Lưu khối sau thành `$ADMISSION_SCRIPT` ngoài checkout, chạy bằng
`bash "$ADMISSION_SCRIPT" "$CANON" "$S" "$H" "$SCRATCH"`. Bốn đối số là đường dẫn/OID
đã xác minh, không dùng đường dẫn Windows trong shell Linux:

```bash
set -eu
CANON="$1"; S="$2"; H="$3"; SCRATCH="$4"
PY="$(command -v python3 || command -v python || command -v py)"
"$PY" -B -c 'import os,shutil,sys; print(sys.executable,sys.version); g=shutil.which("git",path="/usr/bin:/bin"); print("admission git",g); sys.exit(0 if os.name=="posix" and g else "unsupported admission runtime")'
/usr/bin/git --version
"$PY" -B -c 'import yaml; print("PyYAML",yaml.__version__)'
bash --version
test "$(git -C "$CANON" rev-parse HEAD)" = "$S"
"$PY" -B -c 'import hashlib,pathlib,subprocess,sys; r,s=sys.argv[1:]; b=subprocess.run(["git","-C",r,"show",s+":ops/lease_publish.py"],check=True,capture_output=True).stdout; p=pathlib.Path(r)/"ops/lease_publish.py"; assert p.read_bytes()==b, "canonical checker bytes differ"; print("CANONICAL_CHECKER",s,hashlib.sha256(b).hexdigest())' "$CANON" "$S"
ANCESTRY_RC=0
git -C "$CANON" merge-base --is-ancestor "$S" "$H" || ANCESTRY_RC=$?
printf 'ancestor rc=%s\n' "$ANCESTRY_RC"
case "$ANCESTRY_RC" in 0) ;; 1) exit 1 ;; *) exit "$ANCESTRY_RC" ;; esac
ADMISSION_RC=0
"$PY" -B "$CANON/ops/lease_publish.py" kiem-thu-hoi-github "$H" \
  --root "$CANON" --canonical-base "$S" --nhanh-mac-dinh master \
  --receipt "$SCRATCH/local-admission.json" || ADMISSION_RC=$?
printf 'local admission rc=%s\n' "$ADMISSION_RC"
test "$ADMISSION_RC" -eq 0 || exit "$ADMISSION_RC"
git -C "$CANON" show -s --format=%B "$H" > "$SCRATCH/candidate-message.txt"
```

Đọc output/receipt theo §10.2.1; ví dụ không tạo receipt workflow. Đo dependency trong runtime
đích bằng `git --version`, `"$PY" --version`, import các module command dùng, `jq --version`,
`actionlint -version` và phiên bản shell. Tập cần probe lấy từ command thật (§10.2.1).

## Cú pháp máy trạng thái

Chọn đường điều phối theo protocol §3/§4 và authority của Packet; bảng lệnh này mô tả runtime
hiện có, không thay một ngoại lệ được cấp riêng bằng việc ghi tay state.

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py init          --packet 55 --mission 54 \
                                                --executor claude --reviewer codex
# `init` CHỈ tới `awaiting_lease`. Uỷ quyền là bước RIÊNG, và người cấp KHÔNG được
# là tên một provider — agent không tự cấp lease cho chính mình.
"$PY"  .claude/dev/packet_loop.py record-lease  --packet 55 \
                                --lease-id wp55-r2-review-2-codex-20260813 \
                                --granted-by ducthangho \
                                --evidence https://github.com/o/r/issues/55#issuecomment-5281636040 \
                                --expires-utc 2026-08-13T18:30:00Z
"$PY"  .claude/dev/packet_loop.py begin-attempt --packet 55 --provider claude
"$PY"  .claude/dev/packet_loop.py next-comment  --packet 55        # in văn bản → ĐĂNG lên Issue
"$PY"  .claude/dev/packet_loop.py record-post   --packet 55 --for reviewing --comment-id 5258163128
"$PY"  .claude/dev/packet_loop.py transition    --packet 55 --to reviewing --comment-id 5258163128 \
                                                --head-sha $(git rev-parse HEAD)
"$PY"  .claude/dev/packet_loop.py void-attempt  --packet 55 --reason quota
"$PY"  .claude/dev/packet_loop.py status        --packet 55
"$PY"  .claude/dev/packet_loop.py where
```

**Lease không tự có.** `init` chỉ khai *hình dạng* của packet và dừng ở `awaiting_lease`; `leased`
chỉ đạt được qua `record-lease`, và lệnh đó chỉ **ghi hộ** một quyết định đã có ở nơi khác — nó đòi
người cấp (không được là `claude`/`codex`), dấu vết bền để đối chiếu, và hạn. Hạn được cưỡng chế
**cả lúc ghi lẫn mỗi lần mở lượt**: lease hết hạn thì `begin-attempt` thoát 8. Bản trước ghi thẳng
`leased` ngay trong `init`, nên ai gõ được `init` là tự có lease — review cross-provider tái hiện
bằng `init --packet 999999 --mission 888888` rồi `begin-attempt`, cả hai `rc=0`.

`--comment-id` là **ID GitHub trả về lúc đăng**, không phải URL. Ghi sổ bằng `record-post` trước, rồi
`transition` mới tiêu thụ được; mỗi ID dùng đúng một lần cho đúng một chuyển động. Tiến trình này
không gọi mạng nên **không xác minh** ID có thật — đọc `--help` để thấy nó bảo đảm đúng những gì.

Vào `reviewing` phải khai `--head-sha` là **exact head** đưa ra review. Bản duyệt sau đó phải neo
đúng SHA ấy, và mở lượt mới sẽ xoá mỏ neo — nên có commit mới thì bản duyệt cũ hết hiệu lực.

`--help` cho danh sách đầy đủ và ý nghĩa từng mã thoát. Mã thoát khác 0 ⇒ dừng và báo người; script
tự nói lý do trên stderr.

## Vòng lặp vá → review → dừng

`§8`/`§13` quy định mức review và định nghĩa hoàn tất; `§12` quy định điều kiện dừng. Mục này chỉ nói
**phiên phải làm gì với BẢNG LỚP mà reviewer trả về** — bảng ánh xạ `review_class → điều kiện dừng` nằm
ở `cross-review/SKILL.md`, đọc ở đó, đừng nhớ theo lần trước.

**ĐỌC BẢNG LỚP TRƯỚC KHI SỬA DÒNG NÀO.** Không mở tệp sản phẩm trước khi đã đọc xong cột *bản vá theo
lớp | lý do vá lẻ* của từng lớp. Mở tệp trước rồi phân loại sau là cách vá lẻ len vào mà không ai thấy.

| reviewer trả về | phiên làm gì |
|---|---|
| lớp P1/P2 còn mở, lớp khai **bản vá theo lớp** | **đóng CẢ LỚP** — xem *quyền chọn phương án* dưới |
| lớp khai **lý do vá lẻ** | vá lẻ ĐƯỢC, nhưng lý do phải đứng vững ở vòng sau |
| cùng một lớp sang vòng thứ **BA** | **CẤM vá lẻ lần nữa** — xem `M4` dưới |
| `approve` + bảng săn đủ | dừng vòng lặp |
| `blocked` | dừng, xuất handoff, **hỏi chủ kho** |

**Cột *bản vá theo lớp* là DỮ LIỆU BÀN GIAO, không phải chỉ thị triển khai.** Nghĩa vụ của phiên là
**đóng cả lớp**, không phải gõ đúng phương án reviewer viết. Phiên **được** chọn cách khác, với ba điều
kiện: **tái dẫn xuất** lớp từ đầu (đừng nhận phân loại làm tiền đề), **tự đo** rằng cách mình chọn đóng
hết các thể hiện, và **giải thích** vì sao khác. Chép nguyên phương án mà **chưa tự đo** thì KHÔNG đạt.

Quyền ấy **không** phải quyền quay về vá lẻ không lý do: đóng cả lớp vẫn là đầu ra bắt buộc, và `M4`
vẫn áp. Nói ra vì hàng trên từng viết *"thực hiện ĐÚNG bản vá theo lớp ấy"* — câu đó trao cho reviewer
quyền quyết định cách triển khai, trong khi protocol nói gợi ý **không** phải chỉ thị và buộc executor
tái dẫn xuất.

### `M4` — lớp sang vòng thứ BA thì CẤM vá lẻ

Lớp xuất hiện ở **vòng thứ ba** ⇒ **CẤM** vá lẻ lần nữa. Phải **đổi cách làm**, hoặc vào Review Rescue
Checkpoint (`ADR-0037`). Đây là **nghĩa vụ**, không phải một lời khuyên để cân nhắc: `§12` dùng chữ
bắt buộc, và adapter không được phát biểu yếu hơn doctrine.

**ĐƠN VỊ LÀ LỚP, KHÔNG PHẢI FINDING.** Ba finding **cùng một lớp** trong **MỘT** vòng là **lần 1** của
lớp ấy, không phải lần 3. Đếm nhầm đơn vị làm ngưỡng bắn sai lúc — sớm thì chặn oan một chuỗi đang hội
tụ, muộn thì để vá lẻ chạy thêm hai vòng.

### `M5` — tín hiệu KHÔNG HỘI TỤ tính từ PHÂN HẠNG, không từ TỔNG

```
tỉ lệ VÁ THẬT = (số finding vòng trước được phán ĐÃ VÁ THẬT) ÷ (số finding vòng trước)
```

**Hai vòng LIÊN TIẾP có tỉ lệ `< 50 %` ⇒ DỪNG và hỏi chủ kho.** Đây là điều kiện dừng bắt buộc, không
phải một chỉ báo để tham khảo.

**ĐƠN VỊ của cả tử và mẫu là LỚP** — cụ thể là **tập slug lớp duy nhất** của vòng trước. Phân hạng
lấy từ mục đối chiếu của verdict (`ĐÃ VÁ THẬT` / `VÁ HỜ` / `VÁ SINH LỖI MỚI` / `CHƯA VÁ`), mỗi slug
đúng một nhãn. **Thể hiện chỉ để TRUY VẾT, KHÔNG vào phép chia** — nhân số thể hiện trong một lớp
không được làm tỉ lệ đổi.

Vì sao phải chốt đơn vị: cùng một lượt **3 lớp / 10 thể hiện** với **1 lớp** vá thật có **8 thể hiện**
cho hai kết quả trái nhau — theo LỚP là `1/3 = 33 %` (**DỪNG** nếu lặp), theo THỂ HIỆN là
`8/10 = 80 %` (**tiếp tục**). Không chốt đơn vị thì hai người cùng tính ra hai quyết định.

**MIỀN XÁC ĐỊNH — mẫu số bằng 0.** Vòng trước có **0 lớp** thì tỉ lệ là **KHÔNG XÁC ĐỊNH**; **không**
tự gán `0 %`, **không** tự gán `100 %`. Vòng như thế **không tính** là một vòng `< 50 %`, và cũng
**không** làm đứt một chuỗi đang đếm: chuỗi *"hai vòng liên tiếp"* đếm trên các vòng **CÓ tỉ lệ xác
định**, theo thứ tự, bỏ qua vòng không xác định. Nói thẳng hệ quả của cách đọc ấy: hai vòng `< 50 %`
cách nhau bởi một vòng không xác định **VẪN** bắn — đó là chủ đích, vì một vòng không có gì để vá
không nói được điều gì về hội tụ.

**Vì sao PHÂN HẠNG chứ không TỔNG — đo trên dữ liệu thật của `#508`** (`13 → 12 → 11` finding; `VÁ
THẬT` `4` rồi `3`):

| luật | vòng 3 |
|---|---|
| theo **TỔNG** (*"số lượng không cải thiện"*) | **KHÔNG bắn** — 13 → 12 → 11 vẫn là đang giảm |
| theo **PHÂN HẠNG** (`4/13 = 31 %`, rồi `3/12 = 25 %`) | **BẮN** — cả hai vòng `< 50 %` |

**Bộ dữ liệu `#508` ở trên là dữ liệu LỊCH SỬ đếm theo FINDING**, từ trước khi packet chuyển sang đếm
theo LỚP. Giữ nguyên các con số ấy làm hồ sơ; **đừng** hồi tố đổi chúng sang đơn vị lớp rồi khai là
cùng một phép đo. Nó minh hoạ *TỔNG so PHÂN HẠNG*, không minh hoạ *lớp so thể hiện*.

Hai luật cho **hai kết luận KHÁC NHAU trên cùng một dữ liệu**; đó chính là thứ luật này mua được. Một
luật mới cho cùng kết quả với luật cũ thì không mua được gì.

Hệ quả dễ đọc ngược, nói thẳng: một chuỗi có **tỉ lệ vá thật cao** mà **hạng chưa giảm** thì `M5`
**KHÔNG** bắn — nó vẫn đang hội tụ, chỉ chưa xong. Đừng dùng hạng thay cho tỉ lệ.

### `M6` — thu hẹp phạm vi là `chua_do_duoc`, KHÔNG phải một bản vá

Một vòng làm finding biến mất bằng cách **thu hẹp phạm vi** (bỏ một đường dẫn khỏi diff, cắt một tiêu
chí, hạ một mục tiêu) thì phải **khai thẳng**: nó là một mục **`chua_do_duoc`**, và **KHÔNG** được tính
là đã vá. Lớp vẫn sống, chỉ là ra ngoài tầm nhìn của lượt sau.

Giữ **dấu vết**: khai lớp nào biến mất vì thu hẹp, phạm vi nào bị cắt, và lớp ấy chuyển thành nợ tên
gì. Không có dấu vết thì *"0 P1 + 0 P2"* mua được bằng cách cắt bớt tiêu chí. Reviewer được yêu cầu
**gọi tên** đúng chuyện này. Đổi write set là **revision mới** theo `§3.2`/`§5`, không phải một quyết
định trong vòng lặp.

## Sau khi đã QUYẾT MERGE — ba mệnh đề TÁCH RỜI

Đọc đủ ba, đừng gộp; bỏ mệnh đề nào cũng đổi nghĩa cả mục:

1. Head đổi tiếp **KHÔNG** kéo theo một vòng cross-review mới.
2. Nghĩa vụ còn lại **VẪN CÓ**: phải có **CI hậu merge**. Đây KHÔNG phải *"merge rồi khỏi đo"*.
3. Ngoại lệ duy nhất là **PHÁT HIỆN LỖI** — lúc ấy mở vòng mới và **khai lý do**.

**Bẫy đã đo khi đọc CI hậu merge:** huỷ một job trong lượt hậu merge làm kết luận **mức RUN** thành
`cancelled` dù job kia `success` — nền không có đường huỷ MỘT job. Đọc CI hậu merge ở **mức JOB**: một
job xanh trong một run bị huỷ trông y hệt một lượt chưa bao giờ xanh.

## Ba loại chi CI — và `N = 0` cho giai đoạn TRƯỚC merge

| loại | là gì | ngân sách | ghi vết |
|---|---|---|---|
| **(a)** | CI gác cổng do nền **tự bắn** theo push/PR, cộng lượt **CI hậu merge** | không đụng, không tính vào `N` | — |
| **(b)** | CI dùng làm **nhạc cụ đo**, gọi tay trong lúc lặp vá → review | đúng **`N`** lượt, `N` **đóng băng trong đặc tả**; **`N = 0` TRƯỚC merge** | **mỗi lượt ghi `run_id` vào biên nhận** |
| **(c)** | CI **thăm dò**: `workflow_dispatch`, lane nền-khác, hay full CI gọi tay trước merge | **CẤM** | — |

`run_id` của hàng (b) là thứ làm *"đã chi mấy lượt"* **đếm được**; bỏ nó thì `N` là lời hứa. Và `N = 0`
cho giai đoạn trước merge là điểm khác bản trước: để `N` mở kèm câu *"đóng băng trong đặc tả"* thì một
phiên vẫn tự cấp cho mình vài lượt full CI mà vẫn đúng chữ — đúng hình dạng *"ngoại lệ thành thường lệ"*.

**Ca đối chiếu, đo được:** chuỗi `#512` ba vòng cuối **không** gọi `workflow_dispatch` lượt nào và chỉ
nhận lượt tự động ⇒ luật này cho ra **ĐẠT** trên chuỗi ấy. Một luật làm một chuỗi đã tuân thủ thành *vi
phạm* là luật viết sai, không phải chuỗi sai.

Nhắc một điều đã đo và dễ đọc ngược: gắn nhãn để xin một lane khác **không tự sinh lượt chạy nào** khi
workflow không khai loại sự kiện gắn nhãn. Nhãn chỉ được đọc ở lượt bắn KẾ TIẾP — *"đã gắn nhãn"* không
phải *"đã có lượt đo"*.

**KHÔNG CỔNG NÀO CƯỠNG CHẾ MỤC NÀY.** Cả vòng lặp, phần hậu-merge và ba loại chi CI ở trên đều là
**chữ**, tức **kỷ luật đọc**.

**Và `doctrine-scan` XANH KHÔNG chứng minh adapter không chép doctrine** — nó chứng minh adapter không
chép những **CỤM CÓ TRONG DANH SÁCH** của nó. Đo được 12-09-2026, bốn phép trên cùng một cây: bản gốc
`rc=0` · chép nguyên một mục có cụm trong danh sách ⇒ `rc=6` (**có răng ở đó**) · chép nguyên câu phát
biểu con số trần từ ADR ⇒ **`rc=0`** · chép nguyên trọn mục ngoại lệ master-drift của protocol ⇒
**`rc=0`**. Hai phép sau **lọt**, tức hai *"phép làm ĐỎ"* mà tiêu chí nghiệm thu viện dẫn **chưa có
răng**. Cùng lớp *"danh sách CẤM phân biệt CÁCH VIẾT, không phân biệt HÀNH VI"*.

Hệ quả thực hành: **đừng phán "adapter không chép doctrine" từ `rc=0`.** Đọc mắt phần thêm vào, và khi
khai một tiêu chí kiểu ấy là ĐẠT thì khai kèm **phạm vi của phép đo** — cổng thấy được cái gì, và cái
gì nó không thấy. `§20` ghi `ADR-0037` và ADR trần vòng là **`0 cổng`**; cưỡng chế chi CI
nằm ở packet `CONG-CHAN-CHI-CI-SOM`; cổng đọc một hằng số trần duy nhất là nợ `SO-CANON-CHUA-TON-TAI`.
Ai tin ở đây đã có cơ chế sẽ bỏ đúng bước kiểm bằng tay mà mục này đang đòi.

## Chặn cứng

```bash
PY="$(command -v python3 || command -v python || command -v py)"   # CLAUDE.md: nhận CẢ BA tên
"$PY"  .claude/dev/packet_loop.py guard --action merge
# merge | deploy | live | secrets | force-push | delete-branch | delete-worktree | edit-other-spec
```

Lệnh này không có cờ nới, và không được thêm.

## Đăng heartbeat

```bash
gh issue comment 55 --body-file heartbeat.md
```

Nhịp và nội dung tối thiểu do lease của đợt khai; đọc chính comment cấp lease, đừng nhớ theo lần trước.

### Body file và exact readback

Theo protocol §7, khi có quyền đăng Issue comment, lưu ví dụ Python dưới thành
`$SCRATCH/post_comment.py`; gọi bằng `"$PY" "$SCRATCH/post_comment.py" 55 "$SCRATCH/heartbeat.md" "$SCRATCH"`.
`-F body=@...` là cú pháp đọc file của [gh api](https://cli.github.com/manual/gh_api).
Ví dụ chỉ hỗ trợ Issue comment của kho này; review PR dùng endpoint của review.

```python
import hashlib
import json
from pathlib import Path
import subprocess
import sys

issue, body_file, out_dir = sys.argv[1:]
if not issue.isdecimal() or int(issue) < 1:
    raise SystemExit("invalid issue")
out = Path(out_dir)
body_path = Path(body_file).resolve()
body = body_path.read_bytes()
body.decode("utf-8")
repo = "repos/ducthangho/tra-luat"

def api(args, filename):
    result = subprocess.run(["gh", "api", *args], capture_output=True)
    (out / filename).write_bytes(result.stdout)
    print(filename, "rc=", result.returncode)
    result.check_returncode()
    return json.loads(result.stdout)

posted = api(["--method", "POST", f"{repo}/issues/{issue}/comments",
              "-F", "body=@" + str(body_path)], "posted.json")
comment_id = posted["id"]
if type(comment_id) is not int or comment_id < 1:
    raise SystemExit("invalid comment ID; inspect posted.json before retry")
readback = api([f"{repo}/issues/comments/{comment_id}"], "readback.json")
actual = readback["body"].encode("utf-8")
if readback["id"] != comment_id or actual != body:
    raise SystemExit("readback mismatch; preserve both responses")
print("COMMENT_READBACK", comment_id, hashlib.sha256(body).hexdigest())
```

## Đọc log CI

```bash
gh api repos/ducthangho/tra-luat/actions/jobs/<id>/logs
```

Identity/attempt/provenance và fallback endpoint: protocol §10.2.2–§10.2.3; cú pháp truy vấn
`WorkflowRun.file` nằm trong `.claude/skills/cross-review/SKILL.md`, mục “Provenance CI”.
