---
name: land-packets
description: Client do NGƯỜI gọi để chuẩn bị land các packet của một mission (tra-luat) trên nền Claude Code. Không tự trigger, không chứa quyền merge, không deploy. Quy tắc land nằm ở docs/PROTOCOL_DA_PHIEN.md.
argument-hint: "[so-issue-mission]"
disable-model-invocation: true
---

# Adapter `land-packets` — Claude Code

**Skill này KHÔNG tự trigger.** Nhãn `disable-model-invocation: true` ở trên là cách nền này cưỡng chế
điều §13 đã quy định — đừng gỡ.

**ĐỌC `docs/PROTOCOL_DA_PHIEN.md` TRƯỚC.** Nội dung `land prepare`, điều kiện review được chấp nhận,
ranh giới của `--apply`, và điều kiện mission được `complete` nằm ở **§8**, **§12**, **§13**. Tệp này
**cố ý KHÔNG chép lại** chúng — chép là để lệch.

Quy ước deploy của kho (chốt chống thụt lùi Package, hai đường ps1/sh, verify sau push):
`CLAUDE.md` §"Quy ước deploy".

## Trước mọi thao tác trong nhóm này

```bash
python .claude/dev/packet_loop.py guard --action merge      # hoặc deploy | live
```

Luôn dừng, **không có cờ nới**. Đó chính là điểm: land và deploy là quyết định của người, không phải
của vòng lặp.

## Cạm bẫy của kho này — kinh nghiệm vận hành, không phải doctrine

- `gh pr merge --auto` **land NGAY**: kho private + free plan nên branch protection/ruleset trả 403,
  không có required checks. "Auto" thoái hoá thành "merge now". Muốn chờ xanh thì tự đợi
  `gh pr checks`.
- **Không squash** khi packet nhiều commit.
- `release-check --full` **rc=0 dù manifest lệch** — chỉ `release-verify --strict` bắt được.
- Thêm/xoá tệp trong cây ⇒ tái sinh `RELEASE_MANIFEST.json`, và ghi lại golden **nếu** số đếm kiểm kê
  đổi. Bỏ bước này thì phiên land KẾ TIẾP ăn gate đỏ không phải do nó.
- Đọc log CI bằng `gh api repos/.../actions/jobs/<id>/logs`; `gh run view --job … --log` rụng step.
- Báo cáo ra **số**: `N/N` hai số bằng nhau, `"ok": true`, `release-verify --strict` 0 failed / 0 extra,
  `release-bundle` hai lần cùng SHA-256.
