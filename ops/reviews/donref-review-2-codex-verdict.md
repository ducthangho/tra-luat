### Finding P1 — Lease bảo vệ sai một nửa giao dịch

[`.github/workflows/ops-don-ref.yml`](/tmp/claude-0/-home-user-tra-luat/c7eab052-cf71-5777-b253-6b2e409ca64f/scratchpad/rvdonref2/kho/.github/workflows/ops-don-ref.yml:258) đo tổ-tiên so với đầu nhánh mặc định, nhưng chỉ ghim/lease ref nguồn ở dòng 420. Đầu nhánh mặc định có thể đổi sau phép đo.

Bằng chứng trên archive tạm, dùng bare repo thật:

- Dựng lịch sử `A → S → D`; `ops/work=S`, `master=D`.
- Bước chốt nguyên văn trả `rc=0`, chứng minh `S` là tổ tiên và ghi `ops/work S`.
- Giữa hai bước, ép `master: D → A`; `ops/work` vẫn ở `S`.
- Bước làm nguyên văn vẫn trả `rc=0`; lease nguồn khớp nên xoá `ops/work`.
- Sau đó `for-each-ref --contains=S` rỗng, trong khi `cat-file S^{commit}` còn tồn tại: commit `S` đã thành không tra được qua ref.
- SHA phép đo: `A=b7feea9f…`, `S=05378a51…`, `D=c2a96f9a…`.

Invariant “chỉ xoá khi mọi commit vẫn được nhánh mặc định giữ” bị cắt. Lease mới đóng race trên ref bị xoá, nhưng không đóng race trên ref làm căn cứ an toàn.

Gợi ý vá:

- Vị trí: hai bước `chốt`/`làm` trong workflow và `ops/don_ref_chot_test.sh`.
- Hướng rẻ, an toàn: khôi phục cấm xoá vùng làm việc. Nếu giữ chức năng, phải ràng buộc source và một ref giữ commit trong cùng giao dịch nguyên tử; đọc lại đầu mặc định rồi mới xoá vẫn là TOCTOU.
- Test khóa: fixture `A→S→D`, đổi default `D→A` sau chốt; đòi bước làm đỏ và source hoặc ref neo vẫn chứa `S`. Mutant chỉ lease source phải chết.
- Rủi ro bản vá: khôi phục cấm sẽ chặn cleanup; giải pháp multi-ref/anchor có thể tạo ref dư và phụ thuộc hỗ trợ atomic/object availability, nên phải đo trên runner GitHub thật.

### Đã đo và sạch

- HEAD/tree: `9588bb1ef57209da02562928893f544d7d447db1` / `5f52561de29c84c6d3d7041cf49af4cf8eac092c`.
- Prompt hash `5908bbed…`; delta hash khớp byte `cbc57214..9588bb1e`; đúng ba path write set.
- Bộ gốc: `105/105`, `rc=0`; actionlint cả 5 workflow: `rc=0`.
- Lease nguồn thật: SHA cũ ⇒ `rc=1`, ref còn; SHA đúng ⇒ `rc=0`, ref mất; chạy từ kho 0 object.
- Tag chú giải: lease bằng commit SHA bị stale và tag còn; lease bằng tag-object SHA xoá thành công.
- KHO giữ nguyên HEAD, index và worktree sạch.
- Provider/surface/transport: `openai_codex` / Codex service / machine.

### Chưa đo được — GIẢ THUYẾT

Theo điều kiện dừng, chưa chạy tám mutant đã khai và chưa kết luận về multi-ref dở dang, checkout credential/dispatch-ref, lịch sử rời, ngưỡng 250, YAML insertion, M2 hay các race mặc định khác. Lượt 2/2 đã hết; cần Review Rescue/human checkpoint, không gọi Codex lượt ba.

VERDICT: changes_requested
Reviewed commit: 9588bb1ef57209da02562928893f544d7d447db1
