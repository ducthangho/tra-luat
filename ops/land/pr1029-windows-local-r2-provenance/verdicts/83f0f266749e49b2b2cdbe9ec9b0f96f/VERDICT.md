verdict: approved
reviewed_sha: 9aa725c72b6b38263de366ce34a80fb384a522a0
Kết quả: 0 P0, 0 P1, 0 P2, 0 P3.

Provider: `openai_codex`; họ model: `openai` (khai báo của phiên); execution surface: `codex_cli`; transport: `machine`.
Run: `83f0f266749e49b2b2cdbe9ec9b0f96f`; surface/transport khớp `run/83f0f266/run.json`.
Không suy model/effort thực phục vụ từ các phiên trước: run.json hiện chưa có phép đo hai trường này.
Vai trò: Reviewer độc lập, phiên mới, read-only trên cây `cay-kho/`.
Hai trục: Spec và Standards/Security. Review class: `sensitive`; ngưỡng áp dụng: 0 P0–P3 theo chỉ thị review và đặc tả §3.

## Neo đã kiểm

- HEAD: `9aa725c72b6b38263de366ce34a80fb384a522a0`.
- Tree: `a5820b68a689c8a07bc4c53ccb3ba927e56f6033`.
- Base: `5f3855eaf47e024b6c63f8923f64d8f80c5de707`.
- Spec SHA-256: `4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b` (khớp).
- Clone đầy đủ: `--is-shallow-repository` trả `false`; worktree sạch; `core.abbrev=7`.

Không tìm thấy finding có bằng chứng trên hai trục. Các đối chiếu sau áp cho exact HEAD ở trên.

| Nội dung | Đối chiếu và kết quả |
|---|---|
| Phạm vi | ADR-0058:22–25 khớp spec:26: mọi máy Windows của chủ kho có trong `list_devices` và `Online`; VM chỉ được dùng trong phạm vi ấy; không đi vòng qua `gcloud`/RDP. |
| Khoá/sổ đo theo máy | ADR-0058:26–28 khớp spec:27: gốc `D:\tl-win\` hoặc `C:\tl-win\` khi không có D:, diễn giải lại mọi đường dẫn cũ, bổ sung `may=<tên trong list_devices>` vào `ghi_chu`. |
| Hạn và gia hạn | ADR-0058:29–32 khớp spec:28–30: bốn trường của dòng khoá, hạn ≤2 giờ từ lúc bắt đầu, ghi lại dòng với hạn mới khi vẫn cần máy. |
| Ba trường hợp hết hiệu lực | ADR-0058:33–37 khớp spec:31: (a) quá hạn, (b) dạng cũ quá 2 giờ, (c) phiên giữ tuyên bố bỏ; (c) phải có tin nhắn của chính phiên đó hoặc comment trên PR của nó. |
| Tiếp nhận và tiến trình | ADR-0058:38–40 khớp spec:32: kiểm tải theo ADR-0057 mục 4 → ghi sổ khoá cũ/session/UTC/lý do → thay nội dung khoá. Cấm dừng tiến trình phiên khác được giữ ở cả dòng 40 và 50. |
| D7–D9 | Các ô số đo ADR-0058:16–18 khớp spec:20–22, kể cả session, SHA, giờ, số tiến trình và tỷ lệ 0/1, 2/2, 3/3. D7 chỉ bỏ một dấu phẩy; D8/D9 giữ nguyên ô số đo. |
| §20 | Protocol:1537 chỉ thêm phần mô tả “phạm vi và khoá sửa bởi ADR-0058”; các ô khác của dòng 0057 không đổi. Protocol:1538 là đúng một dòng ADR-0058, cột cổng chính xác `không cổng — kỷ luật executor`. |
| Con trỏ §10.2 | Protocol:1015 chỉ thêm `và ADR-0058` vào câu mô tả nơi đặt quy ước. Không có mệnh lệnh hoặc điều kiện chạy/merge mới; lớp lỗi `con-tro-tao-them-nghia-vu` của r1 không tái xuất hiện. |
| Những điểm giữ nguyên | ADR-0058:7–8, 44–50 giữ ADR-0057 mục 2, 4–10 và mục “Những gì KHÔNG đổi”. Việc đọc lại đường dẫn là ngoại lệ đã nêu rõ tại ADR-0058:26–28 và được spec:27 yêu cầu; cột CSV, kiểm tải, cô lập, môi trường, tiến độ, bằng chứng, mốc xét lại và CI không bị thay luật. |
| Không có cổng cưỡng chế | ADR-0058:52–57 khai 0 cổng, tệp khoá không nguyên tử được nêu ở dòng 48–49. Quét 380 tệp mã vận hành bằng `review_audit.py` không thấy tham chiếu máy/khoá/sổ đo; chỉ gặp các chuỗi ấy trong hồ sơ lịch sử khi quét rộng hơn. `cmd_adr_song` tại `.claude/dev/packet_loop.py:1916–2007` chỉ kiểm định tuyến, tên/trạng thái/định dạng metadata; không thi hành luật khoá. |

Đã quét toàn bộ các hunk theo các lớp: nghĩa vụ vượt spec hoặc con trỏ có tính mệnh lệnh; giới hạn/thứ tự xử lý khoá sai; tham chiếu sai hoặc lời khai “giữ nguyên” mâu thuẫn; số đo chép lệch; lời khai cổng rộng hơn bằng chứng; ghi ngoài write set. Không có biểu hiện vi phạm được chứng minh. Đảo lại đúng ba chỉnh sửa được phép trong protocol khôi phục nguyên byte bản base, nên không có doctrine bổ sung ở nơi khác trong tệp.

Tham chiếu đã kiểm riêng, ngoài kết quả cổng:

- ADR-0057 là `docs/adr/0057-windows-local-may-chu-kho.md`: các mục Quyết định 1–10 tồn tại, tương ứng đúng các tên được viện dẫn. Review class thuộc protocol §8; ranh giới local/CI trong ADR-0057:53–57 và protocol §10.2.2–§10.2.3 vẫn được giữ.
- Tiền lệ ADR-0056:11–24 đúng là thay câu “30 phút không có tiến triển” ở ADR-0017:32–34, giữ phần còn lại; cả hai tệp tham chiếu tồn tại duy nhất.
- [Chủ kho duyệt spec r2/g1 tại PR #1025](https://github.com/ducthangho/tra-luat/pull/1025#issuecomment-6514073214), actor `ducthangho`, `OWNER`, 2026-10-30T03:15:32Z: mục 1 khớp toàn bộ hash và revision/generation trong lease và ADR-0058:3–5. Issue #748 tồn tại. Mục 2 của comment giữ hồ sơ r1 ở `landed: false`; ADR-0058 không tự tuyên bố r1 đã landed.
- `9666771` → `96667715996d41bc45e70a64fbaa8996de20f6a0`; `10446ff` → `10446ffa400725b23189ad9c4902932d5eb969bc`; `f4d15ed` → `f4d15edcb5d0a9742182273e5950f76165060667`: đều là commit tồn tại trong lịch sử HEAD. `10446ff` là head lịch sử của PR #1007, được danh sách commit PR xác nhận; không nhầm với head cuối `76b6593`.
- [Số đo local #1007](https://github.com/ducthangho/tra-luat/pull/1007#issuecomment-6495697530) xác nhận hai SHA nền/head, 0/1 → 2/2 và thời điểm khoảng 11:40Z. [Số đo local #1022](https://github.com/ducthangho/tra-luat/pull/1022#issuecomment-6495668313) xác nhận `f4d15ed`, 3/3, hai session D7, khoá từ 09:24:55Z và hai tiến trình browser-use. Các session còn khớp URL phiên trong thân PR #1007/#1022. Phút/giây đầy đủ của D9 được đối chiếu với spec đóng băng; không tự nhận đã đo lại CSV trên laptop.
- Quét mọi tham chiếu session/SHA trong ADR, không chỉ một mẫu; dữ liệu GET và URL nguồn lưu ở [reference-evidence.json](reference-evidence.json). Sự kiện offline/VM của D7/D8 được đối chiếu với §1 spec; không đo lại trạng thái thiết bị lịch sử.

Diff đúng write set của lease và đúng `write_set_hash`: 2 tệp, **68 dòng thêm / 2 dòng xoá**, không chạm ADR-0057. `diff.patch` khớp từng byte với `git diff base HEAD`. Bằng chứng kiểm tự động: [review_audit.py](review_audit.py), [review-audit.log](review-audit.log).

Reviewer chạy trên Linux; Windows local trên candidate này: `not_run`. Các lượt Windows dẫn ở trên là bằng chứng lịch sử, không phải phép đo của lượt review này. Verdict nội dung không thay CI, receipt/assurance hoặc quyền merge/land.

## Đã chạy

Các lệnh Python chạy trong `cay-kho/`, với `PYTHONDONTWRITEBYTECODE=1` để không tạo bytecode trong cây review.

- `python3 .claude/dev/packet_loop.py adr-song --root .` — rc=0.
  Kết quả thật: `adr-song: sạch — 57 ADR trên đĩa, 57 dòng trong §20, khớp 1–1 (tha thiếu trạng thái: ['0016'])`.
- `python3 .claude/dev/packet_loop.py doctrine-scan --root .` — rc=0.
  Kết quả thật: `doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine`.
- `python3 scripts/tl.py doc-claims-check --json` — rc=0.
  Kết quả JSON thật: `"ok": true`, `"files_scanned": 117`, `"flags": []`, `"advisory_count": 381`, `"layers_skipped": {}`.
  Toàn bộ output: [doc-claims-check.json](doc-claims-check.json). Các advisory chưa được coi là lỗi hoặc bằng chứng đúng; tham chiếu trong diff được đối chiếu riêng.
- `git -C cay-kho rev-parse HEAD` — rc=0; `9aa725c72b6b38263de366ce34a80fb384a522a0`.
- `sha256sum cay-kho/ops/specs/WINDOWS-LOCAL-MAY-CHU-KHO-r2.md` — rc=0; `4c92ecbf38fb7f5f97ddea64ed4a43f1cbc9e7a826e87fd8c234dc7e25677c2b`.
- `git -C cay-kho rev-parse --is-shallow-repository` — rc=0; `false`.
- `git -C cay-kho rev-parse HEAD^{tree}` — rc=0; `a5820b68a689c8a07bc4c53ccb3ba927e56f6033`.
- `git -C cay-kho config --get core.abbrev` — rc=0; `7`.
- `git -C cay-kho diff --numstat 5f3855eaf47e024b6c63f8923f64d8f80c5de707 HEAD` — rc=0; output:

  ```text
  3	2	docs/PROTOCOL_DA_PHIEN.md
  65	0	docs/adr/0058-windows-local-han-khoa-va-pham-vi-may.md
  ```

- `git -C cay-kho diff --check 5f3855eaf47e024b6c63f8923f64d8f80c5de707 HEAD` — rc=0; không có output.
- `PYTHONDONTWRITEBYTECODE=1 python3 review_audit.py` (tại sandbox) — rc=0; dòng thật `PASS size: files=2, added=68, deleted=2`, `OPERATIONAL_SOURCE_SCAN {"files": 380, "hits": []}`, `AUDIT PASSED`. Script cũng kiểm byte diff/spec/protocol, write set/hash, D7–D9, các SHA/ADR/mục tham chiếu và worktree sạch.
- Các GET bằng plugin GitHub: `/issues/comments/6514073214`, `/pulls/1007`, `/pulls/1022`, `/issues/748`, `/issues/1007/comments?per_page=100`, `/issues/1022/comments?per_page=100`, `/pulls/1007/commits?per_page=100` của `ducthangho/tra-luat` — thành công (`isError=false`); công cụ không có shell rc. Các collection lần lượt 4 comment, 3 comment, 6 commit, đều dưới page size 100. Không gửi comment hoặc sửa GitHub.
- Mã thoát/output các cổng được giữ tại [gate-results.json](gate-results.json). Cây `cay-kho/` sạch sau mọi lệnh đo.
