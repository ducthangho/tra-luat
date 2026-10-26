# Evidence wp899 r4 — lượt 5

Exact reviewed SHA: `22da28c738e651361274c1264e681a52461dad1e`.

Kết luận ở [VERDICT.md](VERDICT.md), inventory từng mutant ở [MUTANTS.md](MUTANTS.md).

Receipt hiện hành: `preflight5.json`, `runtime5.json`, `suite.json`, `audit.json`, `new5.json`, `proof5.json`, `norm-full.json`, `norm-head.json`, `norm-mutant.json`, `legacy-final.json`, `replay.json`, `ruff.json`, `doctrine.json`, `adr.json`, `operators-target.json` và snapshot/manifest cuối. JSON wrapper chứa command, rc con thật và size/hash output; rc0 driver không thay rc từng ca trong JSON dữ liệu.

`prior1/` và `prior2/` được seed từ input đóng băng để chạy lại script lịch sử. Chỉ những output nối tới producer đã chạy ở receipt/inventory của lượt này được dùng như bằng chứng hiện hành. Tệp lịch sử còn lại là tham chiếu; tên tệp không tự chứng nhận SHA hoặc runtime. Manifest ghi khi bytes khớp input lịch sử để người đọc nhận ra phạm vi ấy.

Mọi patch/mutant/case ở đây là dữ liệu reviewer trong scratch, chưa áp vào cây Executor. Cache/temp nằm tại đây; bản sao mutant toán tử ở `tmp/` được giữ để tái hiện. Không có approve/merge/land/LIVE authority từ các hiện vật này.
