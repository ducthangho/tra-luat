# ADR-0068 — Dọn rác ngay sau land, và lịch dọn dự phòng

- **Trạng thái:** Accepted — hiệu lực từ commit land của chính ADR này (mục D12). Chủ kho `ducthangho` duyệt
  `spec_hash` `d8320e6195658d109cc26fcaa7d28425590d458f5b91cf09f68416d60e4c7b71` của đặc tả `DON-RAC-A` r1 trên Issue
  packet #1507: https://github.com/ducthangho/tra-luat/issues/1507#issuecomment-7129808091
- **Nguồn:** packet `DON-RAC-A` #1507 (Mission #1506), đặc tả `ops/specs/wp1507-r1.md`. Packet anh em trong Mission:
  `DON-RAC-B` (công cụ dọn), `DON-RAC-C` (lịch dọn và bước dọn trong skill land).

## Bối cảnh

Đo ngày 24-11-2026 trên máy chủ kho: một lượt dọn tay xoá 93 nhánh remote và 106 nhánh cục bộ đã gộp trọn vào master,
gỡ 16 worktree và 21 thư mục `work/`, trả khoảng 14 GB cho ổ C: và 4,8 GB cho ổ D:. Lúc kiểm kê, 103 trong 108 nhánh
remote rác là head của PR đã merge. Không bước nào của quy trình dọn chúng:

- `ADR-0060` M7 và khoá `hau_merge` của `ADR-0067` liệt kê đúng bốn việc hậu merge: thu bằng chứng hậu merge, ghi sổ,
  nhả lease, đóng WP.
- `ADR-0028` giữ remote branch/PR tới khi mission land hay huỷ cộng 30 ngày; protocol §4 chép luật ấy.
- `ADR-0058` và `ADR-0059` ghi "Dọn máy là việc của chủ kho."

Chủ kho chỉ đạo ngày 24-11-2026 (nguyên văn ở Mission #1506): dọn rác ngay sau khi merge, land và ghi sổ; chưa dọn được
thì đặt lịch dọn; chủ kho không dọn tay nữa. Bốn quyết định đi kèm được ghi ở đặc tả `ops/specs/wp1507-r1.md` §2.

Tag lưu giữ (`luu-tru`, `archive`, `rescue`, `evidence`, `bak`) đã được ruleset `bao-ve-tag-luu-tru` (id 27976126)
chặn xoá và dời từ ngày 24-11-2026; ADR này không đụng tag.

## Quyết định

**D1 — Việc hậu merge thứ năm `don_rac`.** Danh sách hậu merge của `ADR-0060` M7 và khoá `hau_merge` của `ADR-0067`
thành năm việc: `bang_chung_hau_merge`, `ghi_so`, `nha_lease`, `dong_wp`, `don_rac`. Land Operator làm `don_rac` ngay sau
khi bản ghi sổ đã đọc ngược khớp. Lần duyệt M7 của chủ kho bao gồm `don_rac`.

**D2 — `don_rac` không chặn `landed`.** Khi `don_rac` thất bại hay không làm được (máy offline, thiếu quyền, một chốt
không đo được), Land Operator ghi `don_rac: chuyen_lich` kèm lý do vào bookkeeping; phần còn lại thuộc lịch dọn ở D5.
`landed`, Packet complete và Mission complete không chờ `don_rac`. Giá trị hợp lệ của mục ấy: `hoan_tat`, `chuyen_lich`,
`khong_ap_dung`.

**D3 — Phạm vi dọn của một packet.** (a) Nhánh remote: nhánh ghi ở trường `branch:` của mọi lease của packet, nhánh lease
`ops/wp<issue>-*`, và nhánh head của mọi PR của packet. (b) Mọi PR khác còn mở của cùng packet. (c) Worktree, clone và
nhánh cục bộ của packet trên máy chạy land.

**D4 — Luật xoá nhánh.** Một nhánh chỉ được xoá khi đủ cả sáu điều; thiếu một điều thì giữ:

1. mọi commit của nhánh đã nằm trong nhánh mặc định;
2. nhánh không phải nhánh mặc định và không thuộc `luu-tru/**`;
3. nhánh không là head hay base của PR đang mở;
4. không lease nào còn hạn và chưa bị thay khai nhánh ấy ở `branch:`, quét trên mọi ref sau khi tập tên nhánh máy chủ
   đã được so khớp với bộ đệm cục bộ;
5. xoá bằng CAS neo SHA đã đo (`git push --force-with-lease=<ref>:<sha> origin :<ref>` hoặc tương đương);
6. mỗi điều có ba trạng thái — có, không, KHÔNG ĐO ĐƯỢC — và điều nào không đo được thì nhánh được giữ.

**D5 — Lịch dọn dự phòng.** (a) Phía GitHub: một workflow chạy theo lịch mỗi ngày trên runner của GitHub, quét toàn kho,
xoá nhánh theo D4 và đóng PR theo D6. Nó chạy được khi máy chủ kho tắt. (b) Phía máy: một task Windows trên máy chủ kho chạy
mỗi ngày và lúc đăng nhập, bật `StartWhenAvailable`, nên lượt lỡ do máy tắt chạy bù khi máy bật lại; nó dọn theo D7.

**D6 — Đóng PR.** Khi packet land, `don_rac` đóng mọi PR khác còn mở của cùng packet với comment "thay bởi #X (đã land)".
Lịch dọn đóng PR mở mà mọi commit của head đã nằm trong nhánh mặc định. Không PR nào khác bị đóng tự động. Đóng PR hoàn
tác được bằng cách mở lại.

**D7 — Dọn trên máy.** Một worktree hay clone git được gỡ khi đủ bốn điều: HEAD và mọi nhánh cục bộ của nó đã nằm trên một
ref remote hay một tag; không tệp nào trong nó đổi trong 24 giờ; nó không thuộc một phiên app Claude chưa lưu trữ
(`.claude/worktrees/<tên phiên>`; app tự gỡ worktree sạch khi phiên được lưu trữ); nó không có trong danh sách giữ của
máy. Trước khi gỡ, thay đổi chưa commit được lưu thành bản vá (diff, danh sách tệp chưa theo dõi, và gói các tệp ấy khi
tổng không quá 30 MB) vào thư mục sao lưu; bản vá quá 90 ngày tự xoá. Nhánh cục bộ đã nằm trong `origin/master` và không
gắn worktree nào thì xoá; bản ghi worktree mồ côi thì `git worktree prune`. Thư mục thường không phải git chỉ được gỡ khi
mang tệp đánh dấu packet và packet ấy đã đóng. Việc dọn không dừng tiến trình của ai.

**D8 — Không phải E4.** Xoá nhánh đúng theo D4, bằng công cụ dọn của kho hay bằng `.github/workflows/ops-don-ref.yml`,
không là E4 của `ADR-0067`. Xoá hay dời tag, và xoá ref ngoài D4, vẫn là E4.

**D9 — Biên nhận.** Mỗi lượt dọn, ở bước land hay ở lịch, ghi một biên nhận máy đọc được gồm: thời điểm UTC; phạm vi;
từng ref đã xoá kèm SHA; từng PR đã đóng; từng thư mục đã gỡ kèm đường dẫn bản vá; từng mục bị giữ kèm điều nào của D4 hay
D7 giữ nó; và từng mục không đo được.

**D10 — Vai.** Executor vẫn không xoá nhánh hay worktree; `HANH_VI_CHAN` của `.claude/dev/packet_loop.py` giữ nguyên.
`don_rac` thuộc Land Operator. Lịch dọn đóng vai reconciler của protocol §2.

**D11 — Thay thế.** Phần giữ remote branch/PR 30 ngày của `ADR-0028` và câu tương ứng ở protocol §4 bị thay bởi D1–D6.
Câu "Dọn máy là việc của chủ kho." của `ADR-0058` và `ADR-0059` bị thu hẹp: phần nằm trong D7 do lịch dọn làm; phần còn lại,
và câu "không có quyền dừng tiến trình của phiên khác", giữ nguyên. Danh sách bốn việc của `ADR-0060` M7, khoá
`hau_merge` và ví dụ E4 của `ADR-0067` đọc theo D1 và D8. Tệp các ADR ấy không sửa; ghi chú nằm ở bảng §20 của protocol,
theo tiền lệ `ADR-0053` thay cặp số của `ADR-0044`.

**D12 — Hiệu lực.** Luật D1–D11 có hiệu lực từ commit land của ADR này trên first-parent master và không hồi tố. Công cụ
dọn và lịch dọn có hiệu lực từ commit land của packet đưa chúng vào (`DON-RAC-B`, `DON-RAC-C` của Mission #1506). Trước
đó, Land Operator dọn tay theo D4, D6, D7 hoặc ghi `don_rac: chuyen_lich`.

## Vì sao

- **Vì sao không bật `delete_branch_on_merge`.** Chủ kho chọn chưa bật ngày 24-11-2026. Thiết lập ấy xoá nhánh ngay lúc
  merge mà không kiểm lease, không kiểm PR thế hệ cũ, và nó làm một thao tác hậu merge nằm ngoài land authority mà §13.1
  đòi liệt kê. Nó cũng làm lỗi `fetch` cho phiên cloud dùng lại một nhánh `ccr-*` cho nhiều PR.
- **Vì sao `don_rac` không chặn `landed`.** Rác không làm sai sản phẩm. Nếu `don_rac` chặn `landed`, một lần máy offline
  sẽ treo cả việc ghi sổ; lịch dọn đã gánh phần còn lại.
- **Vì sao đòi mọi commit nằm trong nhánh mặc định.** Đó là bất biến kho đã dùng cho `ops-don-ref.yml`: xoá không được
  làm commit thành không tra được. Nhánh có commit riêng, kể cả nhánh của PR merge bằng squash, được giữ.
- **Vì sao CAS.** Đọc lại đầu nhánh rồi xoá vẫn để một khe giữa lúc đo và lúc xoá; `--force-with-lease` gửi SHA kỳ vọng
  trong cùng giao dịch nên không còn khe (bài học ở `CLAUDE.md`, mục *Đẩy ref từ phiên Claude Code trên web*).
- **Vì sao giữ worktree của phiên app chưa lưu trữ.** Phiên còn có thể được mở lại và dùng worktree ấy; app đã có cơ
  chế tự gỡ khi lưu trữ (`auto_archive_on_pr_close`, bật ngày 24-11-2026).

## Cưỡng chế

Lúc land ADR này: **0 cổng**. D1–D11 là luật cho Land Operator và lịch dọn. Công cụ của `DON-RAC-B` cưỡng chế D4, D6, D7,
D9 bằng mã kèm bộ test; `DON-RAC-C` nối nó vào lịch và vào skill land. Bảng §20 ghi lại vị trí cổng khi chúng land.
