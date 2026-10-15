# Đặc tả packet `no-p3-ho-so` r1 — nợ P3 (a): đính chính spec đóng băng + neo phụ landed wp685

| mục | nội dung |
|---|---|
| `packet_id` | `no-p3-ho-so` |
| `packet_issue` | #750 |
| `revision` | 1 |
| `nguon_cap_viec` | Sổ nợ P3 của phiên điều phối `session_01CSM7GNazhN6uGJb4v1TqBT`, mục 1, 2, 3, 11; ngưỡng chủ kho "chỉ P1/P2 chặn merge, P3 xử ở packet riêng" (#698 comment `6094652521`, #686 comment `6094654297`); `no_con_mo` của `ops/land/pr721-wp698-land-evidence.yaml` (mục `S2-SPEC-HASH-CUA-R11`, `M8-GIU-RANG-CACH-NOI-R13`). Cách tách ba packet do chủ kho chốt trong phiên soạn spec ngày 15-10-2026 (Q1–Q10, "đồng ý hết" hai vòng). |
| `review_class` | standard — chỉ chạm `ops/specs/` (tệp MỚI) và một hồ sơ `ops/land/`; không chạm mã, workflow, authority. |
| `executor` · `reviewer` | Claude (executor); reviewer subagent Claude Sonnet, mức `review_deferred` (cùng họ). Ngưỡng: chỉ P1/P2 chặn merge. |
| `base` | `origin/master` `6f121a3810045af27bf65eb723edf36b29e387f2` (đo 15-10 ~06:10Z). |
| `write_set` | `ops/specs/dinh-chinh-p3-wp685-wp698.md` (MỚI) · `ops/land/pr732-wp685-land-evidence.yaml` · `ops/land/pr732-wp685-provenance/readback-comment-6103888794.json` (MỚI) · `ops/land/pr732-wp685-provenance/SHA256SUMS.txt` |
| `kich_thuoc` | 4 tệp. Ước ≤ 250 dòng thêm (đơn vị: dòng `git diff --numstat` cộng thêm + xoá); dưới trần thường ADR-0044 (6 tệp, 1.000 dòng). |

## Ngoài phạm vi (cố ý)

- **KHÔNG sửa** `ops/specs/ci-g5-cong-cu-va-tiep-r14.md` (sha256 `ed027f410aac7eeedd60335459ba8cfef521a34730fea68c1255533bb56f1a21`) hay `ops/specs/launcher-con-song-esrch-r28.md` (sha256 `8007edf4e00aaefc298bf299bf19be9a71c54e73ff6a1610eb676a806773e156`): cả hai đã đóng băng, có lease neo băm; sửa đè làm băm trong lease trỏ vào thứ không còn tồn tại.
- **KHÔNG sửa** quyết định `landed` của wp685 hay neo chuẩn của nó; chỉ THÊM neo phụ.
- Mục nợ 4 (#751), 5–6 (#752), nhóm `ops/cong_cu_test.py` (chờ #748) và hai mục đo Windows: thuộc packet khác.

## Mục tiêu

Mỗi dòng chiếu vào đúng một đường dẫn của `write_set` (L2).

1. **[`ops/specs/dinh-chinh-p3-wp685-wp698.md`] Đính chính S2 của wp698 r14 (mục nợ 1).** Dòng 3261–3262 của r14 ghi
   "chưa có comment chủ kho xác nhận closure neo `spec_hash` **của r11** (Q10)". Chữ đúng: "… neo `spec_hash` **của r14**"
   — đúng như chủ kho đã đọc ở comment cấp quyền #698 `6091633467` ("Tôi đọc S2 theo depends_on (4): neo spec_hash của r14").
2. **[cùng tệp] Đính chính M8 "Giữ răng" của wp698 r14 (mục nợ 2).** Dòng 2729–2731: vế "tập khoá `KQ` của ba cửa con chứa tập
   của g1 với độ dài mọi danh sách và từ điển lồng không nhỏ hơn (A10 (v))" thiếu "cùng đường, cùng loại". Chữ đúng theo
   gợi ý VERDICT review đặc tả lượt 14 (sha256 `892eeb8a…`, dòng 135): "… cùng đường, cùng loại, độ dài không nhỏ hơn
   (A10 (v), cách tính r14)". Ghi rõ: điều kiện CẦN, không đổi kết luận đo nào (theo chính VERDICT ấy).
3. **[cùng tệp] Ghi nhận O1–O6 của wp685 r28 (mục nợ 3).** Nguồn: VERDICT review lượt 5 r28 (sha256
   `d3f1d9db4896efe8c1b62112a3d0aa479b64c5dc110da1d323b3297d7e7c45fb`, mục "QUAN SÁT KHÔNG XẾP LỚP"). Với mỗi O1…O6 ghi: dòng
   r28 bị nói tới, thực chất, và quyết định (đính chính chữ / chỉ ghi nhận). Không mục nào trong O1–O6 đổi acceptance,
   closure hay write set của wp685 (theo VERDICT); tệp đính chính phải nói thẳng điều đó.
4. **[`ops/land/pr732-wp685-land-evidence.yaml`] Neo phụ landed wp685 (mục nợ 11).** Thêm khối `neo_phu` dưới
   `trang_thai_packet.quyet_dinh_chu_kho`: URL `https://github.com/ducthangho/tra-luat/issues/685#issuecomment-6103888794`,
   thời điểm, người đăng, số byte, sha256 thân — đo từ readback; ghi rõ **neo chuẩn vẫn là**
   `pull/739#issuecomment-6103749546` và `landed_hieu_luc_tu` không đổi.
5. **[`ops/land/pr732-wp685-provenance/readback-comment-6103888794.json`] Readback thô** của comment ấy (`gh api` GET, không sửa).
6. **[`ops/land/pr732-wp685-provenance/SHA256SUMS.txt`] Cập nhật** dòng băm cho tệp ở mục 5; mọi dòng cũ giữ nguyên.

## Nghiệm thu

Mỗi tiêu chí nêu phép đo làm nó ĐỎ (L3).

- **N1 (mục 1–3):** tệp đính chính có đúng ba phần `S2-r14`, `M8-r14`, `O1..O6-r28`; mỗi phần trích **nguyên văn** chữ cũ
  kèm số dòng và băm spec gốc. Phép đo ĐỎ: script trích dòng nêu từ blob spec gốc tại `6f121a3` và so chuỗi trích —
  một ký tự lệch ⇒ ĐỎ. Đột biến: đổi số dòng trong tệp đính chính sai 1 ⇒ phép so ĐỎ.
- **N2 (spec gốc bất biến):** `git diff --stat 6f121a3..HEAD -- ops/specs/ci-g5-cong-cu-va-tiep-r14.md ops/specs/launcher-con-song-esrch-r28.md`
  rỗng. Đột biến: chạm một byte spec gốc ⇒ lệnh trả không rỗng ⇒ ĐỎ.
- **N3 (mục 4–6):** `yaml.safe_load` hồ sơ pr732 thành công; `trang_thai_packet.landed` vẫn `true`; `neo_ben` vẫn là
  6103749546; `neo_phu.sha256` = sha256 của trường `body` trong readback (UTF-8). Đột biến: sửa 1 ký tự sha256 ⇒ ĐỎ;
  đổi `neo_ben` ⇒ ĐỎ.
- **N4:** `sha256sum -c` trong `ops/land/pr732-wp685-provenance/` (theo `SHA256SUMS.txt`) đạt hết. Đột biến: sửa 1 byte
  readback ⇒ ĐỎ.
- **N5 (cổng kho):** CI PR xanh; `python ops/ci_duong_nhanh.py kiem-re` ĐẠT (cả 4 tệp nằm trong `ops/{land,specs}/**`);
  `python .claude/dev/packet_loop.py doctrine-scan --root .` rc 0. Đột biến: thêm một tệp nhị phân vào provenance ⇒
  `kiem-re` ĐỎ (đã đo 15-10 ở PR #749).

## Hình dạng kế thừa

`khong_ap_dung` cho đếm hình dạng lỗi của mã (packet không sửa mã). Ghi lại hai hình dạng đã gặp ở packet tiền nhiệm
có thể tái phát ở đây: (a) **tệp nhị phân trong hồ sơ** bị `kiem-re` từ chối (PR #749 lượt `0876395`) — readback phải là
JSON văn bản; (b) **lời khai vị trí/số dòng trôi** (L5) — mọi số dòng trong tệp đính chính phải đo trên blob tại `6f121a3`.

## Chưa đo được

- Liệu reviewer cùng họ (Sonnet) có bắt được lệch chữ tinh vi trong O1–O6 — không đo được trước; mức `review_deferred`.
- Thân comment 6103888794 có thể bị tầng đọc MCP chuẩn hoá thực thể HTML (CLAUDE.md, bài học 22-08-2026): băm phải tính
  trên readback REST (`gh api`), không trên bản đọc qua MCP.
