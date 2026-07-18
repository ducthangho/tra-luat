# Regen2 profile scope — best-combined v1.19.5

> **[TÀI LIỆU LỊCH SỬ — đúng theo thời điểm viết.]** Các nhắc server/version-gate trong file
> (ví dụ `2.21.2i`) là lịch sử. Version-gate/contract HIỆN HÀNH: `references/API_CONTRACT.md`
> (webapp **2.21.2m**) + `references/RUNBOOK.md`. Nội dung dưới đây giữ nguyên văn, KHÔNG cập nhật.

## Quyết định hợp nhất

Giữ `Code.2.21.2i.gs` làm server mục tiêu:

- quét mọi cấp dưới `rootFolderId`, không chỉ hai cấp;
- profile mặc định `manifestScope=own`;
- giữ riêng `row_kind=ref` khi merge;
- guard theo số dòng own: `new > max(2×old, old+50)`;
- dừng trước `regWriteAll_`.

Không lấy `Code.2.21.2h.gs` từ bản so sánh làm nền vì bản đó quét tối đa hai cấp, merge ref như own và
so tổng dòng registry thay vì own-count.

## Kết phiên

Profile `categories=inherit` dùng cây VBQPPL chỉ để ORGANIZE/tra cứu fallback. Kết phiên mặc định:

```bash
tl --profile <P> manifest
```

Chỉ khi cần đối soát cây riêng:

```bash
tl --profile <P> manifest --touched-drive --confirm yes
```

CLI kiểm `ping.version=2.21.2i` trước regen profile. Server cũ bị chặn trước khi có thể ghi registry.

## Phục hồi registry đã phình

DRY trước:

```bash
tl --profile <P> profile-rebuild-registry --keep-notebook <notebookId>
```

Tiêu chí giữ là hợp của:

1. file hiện nằm trong cây `rootFolderId` của profile;
2. dòng có `nlm_notebook_id` bằng notebook cần giữ;
3. dòng `row_kind=ref`.

Sau khi kiểm `drop_sample`, mới áp:

```bash
tl --profile <P> profile-rebuild-registry --keep-notebook <notebookId> --apply --confirm yes
```

Recovery từ chối xóa nếu danh sách cây own bị capped, chia `reg_delete` theo lô 200 và export lại manifest.
