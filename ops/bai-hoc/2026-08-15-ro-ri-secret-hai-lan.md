# Bài học: rò rỉ secret HAI LẦN trong một phiên, cùng một lớp lỗi

**Ngày đo:** 2026-08-15 · **Phiên:** wp55 r3 executor `claude`

Cùng một phiên, cùng một lớp lỗi, hai lần. Lần thứ hai nằm ngay trong đoạn văn bản tôi viết
ra để **dạy cách tránh lần thứ nhất**. Ghi lại vì đó mới là phần đáng học.

---

## Lần 1 — in nguyên biến môi trường ra transcript

Đi tìm hiểu vì sao hook không chạy, tôi gõ:

```bash
echo "CODEX_AUTH_JSON = ${CODEX_AUTH_JSON:+CÓ, ${#CODEX_AUTH_JSON} ký tự}${CODEX_AUTH_JSON:-'(chưa đặt)'}"
```

Ra 5648 ký tự base64, giải ra là `~/.codex/auth.json` với `refresh_token`, `access_token`,
`id_token` còn sống. Chốt số 1 trong chính hook ấy ghi *"KHÔNG in giá trị, và KHÔNG truyền
qua đối số dòng lệnh"* — tôi vi phạm đúng chốt đó khi đi tìm hiểu vì sao hook không chạy.

**Hậu quả không vá được bằng code:** phải thu hồi và cấp lại credential.

## Lần 2 — dòng DẠY tránh lỗi lại chính là lỗi

Sau lần 1, tôi ghi bài học vào `.claude/skills/work-packet/SKILL.md`, kèm "cách đúng":

```bash
echo "${TEN_BIEN:+có, ${#TEN_BIEN} ký tự}${TEN_BIEN:-chưa đặt}"
```

Đo với giá trị giả:

```
biến ĐÃ ĐẶT  : có, 27 ký tựghp_FAKE_TOKEN_abcdef123456      ← LỘ
biến CHƯA ĐẶT: chưa đặt
```

`${VAR:-…}` chỉ thay thế khi biến **rỗng hoặc chưa đặt**. Ở nhánh "đã đặt" — nhánh người ta
thật sự chạy — nó bung ra **chính giá trị**. Nối `:+` với `:-` trong một chuỗi là tự dựng
một cái bẫy trông như phép kiểm an toàn.

Bản đúng, phiên điều phối vá ở `4085bbf`:

```bash
if [ -n "${TEN_BIEN:-}" ]; then echo "có, ${#TEN_BIEN} ký tự"; else echo "chưa đặt"; fi
```

---

## Ba nguyên nhân, và chỉ nguyên nhân thứ ba là thứ đáng sửa

**1. Tôi kiểm ý ĐỊNH thay vì kiểm HÀNH VI.** Tôi đọc lại dòng mình viết, thấy nó "nói về
việc đếm ký tự", và dừng ở đó. Tôi **không chạy nó với một giá trị giả**. Một lệnh xử lý
secret mà chưa từng chạy thử ở nhánh "đã đặt" là một lệnh chưa được kiểm.

> **Chốt:** mọi lệnh chạm biến bí mật phải được chạy thử với **giá trị giả** ở **cả hai**
> nhánh (đã đặt / chưa đặt) trước khi viết vào tài liệu. Dán đầu ra thật vào chú thích.

**2. Chú thích khai Ý ĐỊNH, không khai HÀNH VI.** Chú thích cũ viết "kiểm bằng sự tồn tại,
không bao giờ in nội dung" — đó là lời hứa, không phải mô tả. Người đọc sau tin lời hứa và
không kiểm lại. Bản vá thay bằng mô tả cạm bẫy cụ thể của `:-`.

**3. GỐC RỄ: mục an ninh chỉ nằm trong LEASE, không nằm trong PROMPT.**

Đây mới là thứ khiến hai lượt executor liên tiếp bỏ sót. `prompt_sha256_required` khoá băm
prompt, nên prompt không cập nhật được giữa chừng; những gì phát sinh sau đó chỉ ghi được
vào lease. Executor thì đọc prompt — nó là "nhiệm vụ" — và coi lease là thủ tục hành chính.

> **Chốt:** BƯỚC 0 của executor phải đọc **cả hai**: prompt VÀ tệp lease. Lease là nguồn sự
> thật của phạm vi và điều kiện; prompt chỉ là bản diễn giải bị khoá băm tại thời điểm cấp.
> Đọc thiếu lease thì làm thiếu việc, và cái thiếu sẽ rơi đúng vào mục thêm sau cùng —
> thường là mục quan trọng nhất, vì nó được thêm do vừa có sự cố.

---

## Chỗ sửa đề xuất — NGOÀI write_set, chưa áp

`.claude/skills/work-packet/SKILL.md` đã được phiên điều phối vá phần lệnh. Phần **chốt số
3** thì chưa ai ghi, và nó là nguyên nhân gốc. Đề xuất thêm vào mục BƯỚC 0 của adapter:

```markdown
## BƯỚC 0 — đọc CẢ prompt LẪN lease

`prompt_sha256_required` khoá băm prompt tại thời điểm cấp, nên mọi điều kiện phát sinh
SAU đó chỉ ghi được vào tệp lease. Đọc prompt mà bỏ lease là bỏ đúng phần mới nhất — và
phần mới nhất thường được thêm vì vừa có sự cố.

    git show origin/<nhánh-lease>:<prompt_path>   # nhiệm vụ
    git show origin/<nhánh-lease>:<đường-dẫn-lease>.yaml   # phạm vi + điều kiện

Lệch băm prompt ⇒ DỪNG. Lease có mục prompt không nhắc tới ⇒ mục ấy VẪN có hiệu lực.
```

Chốt này cũng đã đưa vào bản thảo spec revision 4 (`ops/specs/wp55-r4-spec.md`) dưới dạng
AC 26 phần push-precondition, nhưng nó đáng nằm trong adapter chứ không chỉ trong spec của
một packet.

## Điều duy nhất cần nhớ nếu quên hết phần trên

> Một lệnh chạm secret mà bạn **chưa chạy thử với giá trị giả ở nhánh "đã đặt"** thì bạn
> chưa biết nó in ra gì — kể cả khi chính bạn vừa viết nó, kể cả khi bạn viết nó để dạy
> người khác cách không rò rỉ.
