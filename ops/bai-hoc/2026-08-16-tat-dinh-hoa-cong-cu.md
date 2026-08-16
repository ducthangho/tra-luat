# Vì sao ghi bài học rồi vẫn miss — và cách tất định hoá công cụ đa môi trường

**Ngày:** 2026-08-16 · **Phiên:** wp55 executor `claude` · **Kèm nguyên mẫu chạy được**

Câu hỏi của chủ kho: *"ghi bài học nhưng khi thực thi vẫn miss"*. Đây là bản nghiên cứu
trả lời câu đó. Kết luận ngắn: **bài học dạng văn xuôi là tri thức BỊ ĐỘNG, và tri thức bị
động thì bị bỏ qua đúng lúc cần nhất.** Chữa không phải bằng cách viết thêm bài học, mà
bằng cách biến bài học thành **nhãn do lệnh sinh ra**.

---

## 1. Bằng chứng: ba lần miss trong MỘT phiên, bài học đã có sẵn cả ba lần

| # | tôi kết luận | sự thật | bài học đã tồn tại ở đâu | vì sao vẫn miss |
|---|---|---|---|---|
| 1 | "không gọi được codex" | cài được, chạy được | `docs/GOI_AGENT_DA_NEN.md` §xác thực | tài liệu mô tả **một lần đo trong quá khứ**; tôi nhận là hiện tại |
| 2 | "`launcher.py` bị thiếu" | nhánh ghim base cũ hơn commit thêm nó | không ai viết — nhưng `doctor` có thể tự nói | không lệnh nào in ra "nhánh này thiếu công cụ vì base cũ" |
| 3 | "GitHub API bị chặn" | sai host; MCP chính thức trả 200 | `ops/prompts/wp55-r2-review-4-codex-20260814.md:54` | tri thức nằm trong **tệp prompt của một lượt review cũ**, không nơi nào khác |

Đo được, và đây là con số đắt nhất của bản nghiên cứu này:

```
$ grep -rc "githubcopilot" .claude/dev/launcher.py
0
```

**Tri thức cứu được cả một ngày làm việc tồn tại trong kho dưới dạng văn xuôi, và bằng 0
dưới dạng mã.** `doctor` thậm chí ĐÃ in một dòng về github:

```
CHUA_XAC_THUC  github   gh-cli=khong · REST truc tiep co the bi proxy chan (403)
                        — dung cong cu MCP github
```

Dòng ấy **biết câu trả lời** ("dùng công cụ MCP github") nhưng **không đo** nó, và tự gắn
nhãn `CHUA_XAC_THUC`. Một lệnh biết đường đúng mà không đi thử thì người đọc vẫn phải tự
quyết — và tôi quyết sai.

## 2. Vì sao văn xuôi thua

Một bài học `.md` đòi ba bước, và **hỏng ở bất kỳ bước nào là mất trắng**:

1. agent **biết** tệp ấy tồn tại;
2. agent **tìm và đọc** nó;
3. agent **nhận ra đang ở đúng tình huống** nó mô tả, rồi áp.

Bước 3 là chỗ chết nhiều nhất: lúc gõ `curl api.github.com` và thấy 403, tôi **không thấy
mình đang ở trong tình huống mà bài học 14-08 mô tả** — vì tình huống ấy được mô tả bằng
chữ, còn thứ trước mắt tôi là một mã HTTP.

Một **nhãn do lệnh sinh** thì bỏ qua cả ba bước: nó hiện ra không cần ai nhớ tìm.

## 3. Thiết kế: bốn nhãn, ý nghĩa cố định

| nhãn | nghĩa | được sinh từ |
|---|---|---|
| `DUNG_DUOC` | đã **gọi thật** và thành công | bằng chứng DƯƠNG |
| `CO_MAT` | nhị phân/tệp tồn tại, **chưa** chứng minh gọi được | `--version`, `which`, `login status` |
| `HONG` | đã gọi thật và **thất bại**, kèm lý do đo được | lời gọi thật |
| `KHONG_CO` | không tìm thấy | `which` rỗng |

**Chốt cốt lõi, và là toàn bộ bài học của phiên này:**

> `CO_MAT` là **mức trần** cho mọi phép kiểm không gọi thật. `--version`, `which`,
> `login status`, và **tài liệu** đều không bao giờ nâng được lên `DUNG_DUOC`.

Ba lần miss của tôi đều là nâng nhãn vượt quá bằng chứng, theo cả hai chiều:

- codex: tài liệu nói "không có" ⇒ tôi kết luận `KHONG_CO` mà chưa `which`;
- codex (lần 2): `login status` nói "Logged in" ⇒ hook kết luận `DUNG_DUOC` với token đã chết;
- github: `api.github.com` 403 ⇒ tôi kết luận `KHONG_CO` cho **toàn bộ** GitHub.

## 4. Nguyên mẫu — chạy được, đo được

`ops/proposals/tien_kiem.py`. Chạy trong chính phiên này:

```
công cụ          nhãn         chi tiết
git              DUNG_DUOC    ls-remote origin OK — đọc/ghi remote được
rg               DUNG_DUOC    tìm được trên stdin
claude           CO_MAT       2.1.233 · credential trên đĩa
codex            CO_MAT       Logged in using ChatGPT · login status CHỈ đọc tệp
github-mcp       DUNG_DUOC    api.githubcopilot.com/mcp/ HTTP 200 — dùng công cụ MCP
```

Với `--goi-that`:

```
codex(gọi thật)  DUNG_DUOC    gọi thật thành công
```

**Dòng `github-mcp` là dòng đã cứu được cả ngày của tôi nếu nó tồn tại từ sáng.**

Chú ý `codex` giữ `CO_MAT` chứ không tự nâng: `login status` chỉ đọc tệp, và ngày 16-08 nó
trả "Logged in using ChatGPT" cho một token **đã bị thu hồi**. Chỉ `--goi-that` mới nâng
được nhãn — đúng và đắt, nên tách cờ riêng.

## 5. Tất định hoá theo từng công cụ

| công cụ | cài ở đâu | phép kiểm `DUNG_DUOC` | bẫy đã trả giá |
|---|---|---|---|
| `git` | có sẵn mọi nơi | `git ls-remote origin HEAD` | nhị phân chạy ≠ remote với tới được |
| `rg` | apt / hook | `rg -c` trên stdin | thiếu nó thì codex và Claude Code gãy giữa chừng, không tự lùi về grep |
| `claude` | `npm i -g @anthropic-ai/claude-code` | — | `--version` chỉ cho `CO_MAT` |
| `codex` | `npm i -g @openai/codex` | `codex exec` thật, bắt 6 chuỗi từ chối | `login status` nói CÓ TỆP, không nói CÒN HIỆU LỰC |
| `github` | **không cài gì** | `POST api.githubcopilot.com/mcp/` initialize → 200 | **`api.github.com` là host SAI** — 403 kể cả không token |

Hai chuyện riêng về môi trường, cả hai đã trả giá:

**Hook chỉ chạy khi nhánh mang nó.** Nhánh packet ghim `base_sha` cũ hơn commit thêm hook
thì hook không tồn tại để chạy, và `settings.json` bản cũ cũng không đăng ký `SessionStart`.
Kho gắn giữa phiên thì hook cũng không chạy. Lấy công cụ **từ nhánh chính**, đừng dựa vào
cây làm việc:

```bash
git show origin/master:.claude/dev/launcher.py > "$(mktemp -d)/launcher.py"
```

**Biến môi trường không đổi giữa phiên.** Credential bị xoay thì phiên đang chạy vẫn giữ
giá trị cũ cho tới khi khởi động lại — hoặc tới khi có ai ghi tay. Phép kiểm phải phân biệt
*cùng credential* với *credential mới*, và `login status` không phân biệt được.

## 6. Đề nghị — ba việc, xếp theo tỷ lệ lợi/công

**1 · Thêm phép đo `github-mcp` vào `doctor`.** Rẻ nhất, cứu nhiều nhất. Một lời gọi
`curl`, một nhãn. Nếu dòng đó có từ sáng 16-08 thì cả ngày ấy không xảy ra.

**2 · Đổi mọi nhãn hiện có sang bốn nhãn cố định, và ép trần `CO_MAT`.** Luồng môi trường
đã đi đúng hướng này (`CO_CREDENTIAL` vs `DUNG_DUOC`, kèm chú thích *"NÂNG NHÃN VƯỢT QUÁ
BẰNG CHỨNG"*). Việc còn lại là **rà mọi chỗ sinh nhãn** xem có chỗ nào còn suy từ
`--version` hay tài liệu không.

**3 · Chuyển mỗi bài học đã có thành MỘT DÒNG NHÃN.** Tiêu chí nghiệm thu, đo được:

> Một bài học **chưa xong** nếu chưa có lệnh nào in ra kết luận của nó. Tệp `.md` là phần
> *giải thích*; phần *cưỡng chế* phải nằm trong `doctor`.

Áp thử cho ba bài học của phiên này:

| bài học | dòng nhãn tương ứng | đã có chưa |
|---|---|---|
| codex gọi được, đừng tin tài liệu | `codex  DUNG_DUOC/HONG` (`--goi-that`) | nguyên mẫu có |
| nhánh ghim base cũ không mang công cụ | `hook-phien  KHONG_CO (nhánh base cũ hơn commit thêm hook)` | **chưa** |
| GitHub dùng MCP, không dùng `api.github.com` | `github-mcp  DUNG_DUOC` | nguyên mẫu có |

## 7. Điều KHÔNG đề nghị

**Đừng viết thêm bài học dạng văn xuôi cho cùng một lỗi.** Phiên này đã có
`ops/bai-hoc/2026-08-15-*` và `2026-08-16-*`; chúng vẫn đúng và vẫn nên giữ làm phần giải
thích. Nhưng nếu chỉ thêm bài học thứ tư thì lần miss thứ tư sẽ tới — bằng đúng cơ chế đã
làm hỏng ba lần trước.

**Đừng gộp `--goi-that` vào đường mặc định.** Nó tốn thời gian và mạng; `SessionStart` mà
treo thì hỏng nặng hơn cái nó chữa. Tách cờ, và mặc định nói thẳng *"chưa gọi thật"*.

## 8. Câu một dòng, nếu quên hết phần trên

> Một bài học chỉ thật sự tồn tại khi có **một lệnh in ra kết luận của nó**. Văn xuôi giải
> thích *vì sao*; chỉ nhãn mới cưỡng chế được *cái gì*.
