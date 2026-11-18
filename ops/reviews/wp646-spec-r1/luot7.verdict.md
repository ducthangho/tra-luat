## Review độc lập lượt 7 · Issue #646

Đặc tả được review có SHA-256 `24091c02f33dad991809e214abde6e2d663c065ac523b789ec7859a8cc6c8c0a`. Checkout ở detached HEAD, trùng ref `master` cục bộ tại `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Đặc tả là tệp chưa được Git theo dõi, nên SHA-256 neo nội dung review. Tôi dùng `openai_codex / codex_cli / machine`, chạy Git 2.43.0 trên Linux với rig trong RAM tại `/dev/shm` vì `/tmp` chỉ đọc. Không gọi mạng hoặc ghi worktree. Lease, CI và biên nhận bên ngoài chưa được xác minh.

### Finding lượt 6

| Finding | Trạng thái | Bằng chứng lượt 7 |
|---|---|---|
| P2 N1 + N5 bỏ lọt đổi mode Git | **Đóng** | Cùng blob và numstat `14 0`, đổi `100644 → 100755` cho N1 `rc=1` ở (c). Bỏ (c) vẫn đỏ ở (d). Bỏ cả hai mới cho N1 `rc=0`. |
| P3 §6 đếm lượt cũ | **Chưa đóng** | §6:270–272 ghi đúng sáu lượt trước, nhưng cộng “lượt approve sắp tới”. Sau verdict này đã dùng **7 lượt**, cả 7 `request_changes`. Khi đến điểm chờ E2, đọc lại số thực tế từ biên nhận. |
| P3 §8 ghi 13 dòng | **Đóng** | §8:291 ghi 14 dòng thêm, 0 dòng xoá. Rig xác nhận `14 0` trên H đúng. |

### Finding mới

- **P2 — N1 + N5 xanh giả khi Git ẩn gitlink ngoài write set.** Trên rig, tôi stage đúng khối §3 rồi thêm một entry bằng `git update-index --add --cacheinfo "160000,$B,extra-submodule"` và commit H. Với cấu hình mặc định, `bash n1.sh "$B" "$H" "$N5"` trả `1`. Sau `git config diff.ignoreSubmodules all`, cùng B và H cho **N1 `rc=0`, N5 `rc=0`**. `git diff-tree -r --ignore-submodules=none "$B" "$H"` vẫn hiện dòng `A extra-submodule`, mode `160000`. Ba lệnh `git diff` ở (a)–(c) đều kế thừa cấu hình này, còn (d)–(e) chỉ kiểm đường dẫn protocol. Cố định `--ignore-submodules=none` khi đo và giữ ca gitlink với cấu hình `all` làm phản chứng. [Đặc tả, §4 dòng 242](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:242)
- **P3 — N1 đỏ oan với H đúng khi thuộc tính Git cục bộ tắt text diff.** Trên cùng H hợp lệ đã qua cả hai script, ghi `docs/PROTOCOL_DA_PHIEN.md -diff` vào `.git/info/attributes` của rig. N1 chuyển từ `rc=0` sang `rc=1` tại (b), N5 vẫn `rc=0`. Bỏ riêng (b) cho N1 `rc=0`. Phép đo `14 0` cần môi trường thuộc tính được kiểm soát, hoặc cần đo trên byte blob đã trích. [Đặc tả, §4 dòng 243](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:243)

### Kết quả rig và rà L1–L7

| Ca | N1 rc | N5 rc |
|---|---:|---:|
| H đúng khối §3 | 0 | 0 |
| `chmod +x` | 1 | 0 |
| Chèn sai vị trí, cùng `14 0` | 1 | 1 |
| Thêm tệp thường ngoài write set | 1 | 0 |
| CRLF toàn tệp | 1 | 1 |
| Thay bằng symlink hoặc đổi tên | 1 | 1 |
| Thêm gitlink, cấu hình mặc định | 1 | 0 |
| Cùng gitlink, `diff.ignoreSubmodules=all` | 0 | 0 |

Bỏ (a) riêng ở ca thêm tệp vẫn đỏ bởi (b). Bỏ (d) riêng ở ca `chmod +x` vẫn đỏ bởi (c). Bỏ (e) riêng ở ca chèn sai vị trí làm N1 đổi `1 → 0`, còn N5 giữ `1`. Đột biến N5 từ “bằng” thành “chứa” làm cả năm ca thử đổi `1 → 0`.

Rà L1–L7, write set khớp mục tiêu, đơn vị đếm được nêu và L4 không áp dụng cho packet này. Các ngoại lệ có bằng chứng nằm ở L3/L6 đối với phép đo N1 và ở L5/L7 đối với số lượt tại điểm chờ E2. Trên base cục bộ, `doctrine-scan` và `adr-song` đều trả `0`, lần lượt báo 12 tệp quét và 66 ADR khớp 66 dòng. N3 và gate triển khai trên H thật chưa chạy.

KET_LUAN: request_changes
tokens used
59,781
## Review độc lập lượt 7 · Issue #646

Đặc tả được review có SHA-256 `24091c02f33dad991809e214abde6e2d663c065ac523b789ec7859a8cc6c8c0a`. Checkout ở detached HEAD, trùng ref `master` cục bộ tại `641108cb997872b0ef2a277ea9c8faf8b82532bb`, tree `e6c7c50863421e32cac4f5f1894f176d758375b1`. Đặc tả là tệp chưa được Git theo dõi, nên SHA-256 neo nội dung review. Tôi dùng `openai_codex / codex_cli / machine`, chạy Git 2.43.0 trên Linux với rig trong RAM tại `/dev/shm` vì `/tmp` chỉ đọc. Không gọi mạng hoặc ghi worktree. Lease, CI và biên nhận bên ngoài chưa được xác minh.

### Finding lượt 6

| Finding | Trạng thái | Bằng chứng lượt 7 |
|---|---|---|
| P2 N1 + N5 bỏ lọt đổi mode Git | **Đóng** | Cùng blob và numstat `14 0`, đổi `100644 → 100755` cho N1 `rc=1` ở (c). Bỏ (c) vẫn đỏ ở (d). Bỏ cả hai mới cho N1 `rc=0`. |
| P3 §6 đếm lượt cũ | **Chưa đóng** | §6:270–272 ghi đúng sáu lượt trước, nhưng cộng “lượt approve sắp tới”. Sau verdict này đã dùng **7 lượt**, cả 7 `request_changes`. Khi đến điểm chờ E2, đọc lại số thực tế từ biên nhận. |
| P3 §8 ghi 13 dòng | **Đóng** | §8:291 ghi 14 dòng thêm, 0 dòng xoá. Rig xác nhận `14 0` trên H đúng. |

### Finding mới

- **P2 — N1 + N5 xanh giả khi Git ẩn gitlink ngoài write set.** Trên rig, tôi stage đúng khối §3 rồi thêm một entry bằng `git update-index --add --cacheinfo "160000,$B,extra-submodule"` và commit H. Với cấu hình mặc định, `bash n1.sh "$B" "$H" "$N5"` trả `1`. Sau `git config diff.ignoreSubmodules all`, cùng B và H cho **N1 `rc=0`, N5 `rc=0`**. `git diff-tree -r --ignore-submodules=none "$B" "$H"` vẫn hiện dòng `A extra-submodule`, mode `160000`. Ba lệnh `git diff` ở (a)–(c) đều kế thừa cấu hình này, còn (d)–(e) chỉ kiểm đường dẫn protocol. Cố định `--ignore-submodules=none` khi đo và giữ ca gitlink với cấu hình `all` làm phản chứng. [Đặc tả, §4 dòng 242](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:242)
- **P3 — N1 đỏ oan với H đúng khi thuộc tính Git cục bộ tắt text diff.** Trên cùng H hợp lệ đã qua cả hai script, ghi `docs/PROTOCOL_DA_PHIEN.md -diff` vào `.git/info/attributes` của rig. N1 chuyển từ `rc=0` sang `rc=1` tại (b), N5 vẫn `rc=0`. Bỏ riêng (b) cho N1 `rc=0`. Phép đo `14 0` cần môi trường thuộc tính được kiểm soát, hoặc cần đo trên byte blob đã trích. [Đặc tả, §4 dòng 243](/tmp/claude-0/-home-user-tra-luat/1adbda56-058d-5ab2-9b04-c994e35e8ec6/scratchpad/wtP3/ops/specs/LEASE-TRUONG-KHAI-NGHIA-r1.md:243)

### Kết quả rig và rà L1–L7

| Ca | N1 rc | N5 rc |
|---|---:|---:|
| H đúng khối §3 | 0 | 0 |
| `chmod +x` | 1 | 0 |
| Chèn sai vị trí, cùng `14 0` | 1 | 1 |
| Thêm tệp thường ngoài write set | 1 | 0 |
| CRLF toàn tệp | 1 | 1 |
| Thay bằng symlink hoặc đổi tên | 1 | 1 |
| Thêm gitlink, cấu hình mặc định | 1 | 0 |
| Cùng gitlink, `diff.ignoreSubmodules=all` | 0 | 0 |

Bỏ (a) riêng ở ca thêm tệp vẫn đỏ bởi (b). Bỏ (d) riêng ở ca `chmod +x` vẫn đỏ bởi (c). Bỏ (e) riêng ở ca chèn sai vị trí làm N1 đổi `1 → 0`, còn N5 giữ `1`. Đột biến N5 từ “bằng” thành “chứa” làm cả năm ca thử đổi `1 → 0`.

Rà L1–L7, write set khớp mục tiêu, đơn vị đếm được nêu và L4 không áp dụng cho packet này. Các ngoại lệ có bằng chứng nằm ở L3/L6 đối với phép đo N1 và ở L5/L7 đối với số lượt tại điểm chờ E2. Trên base cục bộ, `doctrine-scan` và `adr-song` đều trả `0`, lần lượt báo 12 tệp quét và 66 ADR khớp 66 dòng. N3 và gate triển khai trên H thật chưa chạy.

KET_LUAN: request_changes
rc=0 xong 2026-11-18T08:19:51Z
