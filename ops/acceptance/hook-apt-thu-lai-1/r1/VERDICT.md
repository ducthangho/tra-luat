# HOOK-APT-THU-LAI-1 r1 — review độc lập Codex offline (1/2 lời gọi): approve

**Căn cứ:** đặc tả `ops/specs/hook-apt-thu-lai-1-r1.md` §3–§4, lease `ops/leases/hook-apt-thu-lai-1-r1-g1-claude.yaml`
(`review_calls_limit: 2`), Issue #1523, PR #1524.

## Lượt review
| lượt | run (`launcher.py run`) | head review | kết luận | sandbox | model phục vụ |
|---|---|---|---|---|---|
| 1 | `eb653c21`, 08:10:06Z → 08:16:35Z (25-11), `ma_thoat` 0 | `402be90cf8803d8622184cfa8a670fdea1271cc9` | **approve**: 0 P0–P2, 1 P3 (2 đột biến tự dựng sống) | `DO_DUOC` | `gpt-6-astra` |

Lệnh: `python3 .claude/dev/launcher.py run --workspace <clone tại head> --expected-repo ducthangho/tra-luat --expected-root-commit
e13f74bb… --expected-head <head> --prompt-file <p> --expected-prompt-sha256 <sha> -- /opt/node22/bin/codex exec -m gpt-6-astra
--sandbox workspace-write --skip-git-repo-check -C <thư mục review> "…{PROMPT_FILE}…"`. Lời gọi thứ hai không dùng.

## Reviewer đo độc lập
- Hành vi thật end-to-end, với `ops/cai_cong_cu.sh` thật và `apt-get` giả luôn lỗi, `CAI_CONG_CU_CHO_GIAY=0`. Số lần `install`:
  | `CAI_CONG_CU_THU_LAI` | lần `install` |
  |---|---|
  | chưa đặt | 2 |
  | `3` | 4 |
  | `0` | 1 |
  | rỗng | 2 |
  | `abc` | 4 (trình cài tự về mặc định 3) |

  Trong cả 5 kịch bản, giá trị ở hook cha không đổi.
- `timeout -k 5 1 env … bash …` với con và cháu lờ TERM: cả cây bị giết sau 6,00 s, không tiến trình nào sống sót.
- 4/4 đột biến `H4_*` bị giết qua chính bộ chạy `chay_dot_bien`.
- 19/19 ca `r1474_*` của `launcher_test.py` đạt; 22/22 neo đột biến nhắm vào hook khớp đúng một chỗ.
- Delta so với base = 0: shellcheck 1 → 1, `bash -n` sạch, ruff F 0 → 0, `doctrine-scan` sạch.

## Xử lý finding
| finding | xử lý | bằng chứng |
|---|---|---|
| L1 F1523-01 P3: ca `h4` không khoá hai giá trị biên. Đột biến `invalid_to_1` và `empty_passthrough` sống | `h4` thêm vế rỗng (⇒ trình cài nhận `1`, cha vẫn rỗng) và vế `abc` (⇒ chuyển nguyên văn); thêm 2 đột biến `H4_rong_khong_ve_1`, `H4_ep_khong_phai_so_ve_1` | `fb18841`: 6/6 đột biến `H4_*` bị giết. Phần sửa chỉ ở test, không dùng lời gọi thứ hai; connector Codex review head cuối |

## Đo của executor trên head cuối `fb18841`
- `ops/cloud_agent_creds_test.py` đầy đủ: CA 61/61, DOT BIEN 97/97 bị giết đúng lý do, TU KIEM PHAN HANG DAT, `TONG: DAT`.
- `.claude/dev/launcher_test.py` đầy đủ, đo trên `402be90` (head code; `fb18841` chỉ đổi `cloud_agent_creds_test.py`): `rc=0`, 455/455
  ca chạy qua, 0 hỏng. Hai ca bỏ qua chỉ dành cho Windows, như trước.
- Ghi nhận môi trường: trong sandbox của reviewer, bộ `cloud_agent_creds_test` đầy đủ đỏ 11 ca. Nguyên nhân: `/tmp/.git` chỉ đọc, và
  clone thiếu commit lịch sử `8f123b2`. Reviewer tái hiện các ca ấy trên base, nên đây không phải hồi quy.

## Giới hạn đã nêu, không chặn
- Giá trị không phải số được chuyển nguyên văn, nên trình cài tự về mặc định 3 lần thử lại. Trần 180 s/lần cài và ngân sách khối 300 s
  của hook vẫn giới hạn thời gian.
- Chưa đo trên macOS/MSYS. Hook vốn đã dùng `env -u PATH` từ trước, nên thay đổi này không thêm phụ thuộc mới.
