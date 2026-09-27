# Hiện vật cross-review ĐẶC TẢ `THU-HOI-LEASE-A1a` revision 2 → 3 (PR #652, PR #658) — 10 lượt, 10 lời gọi

Thư mục con **cố ý** (không phải `*-verdict.md` mức gốc), cùng tiền lệ `../thu-hoi-lease-va-cap-lai-spec/`: đây là
review **đặc tả**, chưa có Packet lease hay biên nhận v2, nên không vào bảng `t26/t27`. Mọi `luotN-VERDICT.md` là
**nguyên văn** của reviewer (`codex exec -m gpt-6-astra -c model_reasoning_effort="high"`, phóng qua
`.claude/dev/launcher.py run`), không sửa. `luotN-PROMPT.md` / `luotN-EVIDENCE.md` là nguyên văn phiên điều phối gửi
reviewer. Đính chính ghi ở `HAU-KIEM-CONNECTOR-652.md` hoặc ở §0 của đặc tả, **không** ghi đè hiện vật.

**Đặc tả có hiệu lực: revision 3**, `ops/specs/THU-HOI-LEASE-A1a-r3.md`, sha256
`ac7e0129b281b517c69e9a2512a05b47d55ad99f0ac964462c061ea511f70bc1`, blob `401804bacea92ae5305bb5c3a36cc3821f973227`.
r2 (`9bc0fe28…`) giữ nguyên byte làm hồ sơ.

**Tệp này KHÔNG cấp việc và KHÔNG nói lease nào đang tồn tại.** Lúc viết (27-09-2026) **chưa có** lease A1a nào trong
`ops/leases`. Lease A1a **tương lai** phải neo `spec_hash` bằng đúng băm r3 ở trên, và chỉ được cấp khi #579 đã land
**và** `ai-dang-giu` đo lại ra `NGƯỜI_GIỮ 0` trên cả ba đường write set (r3 §8 mục 3). Thứ giao việc là Packet Issue
#564 **cộng** lease còn hiệu lực (protocol §3.2, §4). Muốn biết lease nào đang giữ gì thì hỏi `ai-dang-giu`, đừng hỏi
mục lục này: nó là hồ sơ lịch sử và cố ý không chép trạng thái lease.

## Các lượt

Cột "spec" là `reviewed_spec_sha256` trong header verdict; cột "head" là `reviewed_sha`. Băm là 8 ký tự đầu sha256
của tệp **trong kho**. Thời lượng, `run_id` và `ma_thoat` đọc từ `run.json` của launcher (nằm ở scratchpad phiên
điều phối, không vào kho).

| lượt | spec | head | VERDICT | HINT | PROMPT | `run_id` · thời lượng | kết luận |
|---|---|---|---|---|---|---|---|
| 1 | r2 nháp 1 `a5aacafa` | `f8a37c04` | `bec95f09` | `230087e1` ¹ | `386a9527` | `36c0d446` · 991 s | changes_requested — 2 P1 + 5 P2 |
| 2 | r2 nháp 2 `1bfdc7bb` | `981b9ea1` | `4de2f5a1` | `0ecd3674` ¹ | `45d9f797` | `b3a1f870` · 1074 s | changes_requested — 1 P1 + 3 P2 |
| 3 | r2 nháp 3 `fb67bebd` | `79b8ec7b` | `08b90523` | `ba75a091` ¹ | `789e9e04` | `4d58c283` · 890 s | changes_requested — 1 P1 |
| 4 | r2 nháp 4 `b8856466` | `33e19c41` | `3e8334a8` | `f571c1b3` ¹ | `695e83dc` | `e75b86d0` · 643 s | changes_requested — 1 P1 + 1 P3 |
| 5 | r2 nháp 5 `8a0a9a5a` | `43a17e1e` | `cec868b5` | `7a5c4ec1` ¹ | `b23d5887` | `8a6561f5` · 557 s | changes_requested — 1 P3 |
| 6 | r2 nháp 6 `c314ce69` | `635e9a23` | `6acafa4c` | `c6086b71` ¹ | `d653e208` | `66f348ca` · 381 s | changes_requested — 1 P3 |
| 7 | **r2 nháp 7 `9bc0fe28`** | `7fc28680` | `46afface` | rỗng | `d3c9183f` | `afa0ef1f` · 495 s | **approve** — 0/0/0 |
| 8 | r2 `9bc0fe28` + hậu kiểm #652 | `4abfdeb5` | `8b430050` | `b0717124` | `5bf68b53` | `905a19e8` · 672 s | changes_requested — 2 P1 (F17, F18) |
| 9 | **r3** `ac7e0129` | `3f1bf2e2` | `fb5e6901` | `bf56d801` | `cec6c01f` | `ef7602b8` · 623 s | changes_requested — 1 P2 (F19) |
| 10 | **r3** `ac7e0129` | `8eb076b6` | `19a49bb5` | rỗng | `5eabbaf8` | `9fbc066d` · 477 s | **approve** — 0/0/0 |

Mọi lượt: `ma_thoat 0`; `run.json` `provider openai_codex` · `execution_surface codex_cli` · `transport machine`;
header `stderr.log` `model: gpt-6-astra` · `reasoning effort: high`. Bảng theo từng lượt kèm `origin` của checkout
reviewer ở `HAU-KIEM-CONNECTOR-652.md` (bảng S).

¹ Băm **sau** khi thêm nhãn patch-as-hint (protocol §13 ràng buộc 1) ở PR #658. Bỏ 3 dòng đầu thì ra đúng byte
reviewer sinh ra; băm gốc nằm ngay trong dòng nhãn và trong bảng H của `HAU-KIEM-CONNECTOR-652.md`.

## Đóng băng và land

| mốc | revision | human audit | merge commit | neo |
|---|---|---|---|---|
| PR #652 | r2 | [`5851587276`](https://github.com/ducthangho/tra-luat/pull/652#issuecomment-5851587276) | `67802bf9a1b9adba6d8b13c63ee46744d74655b5` | `d71f77ec` · `9bc0fe28…` · blob `9c65f4e2` |
| PR #658 | **r3** | [`5852432543`](https://github.com/ducthangho/tra-luat/pull/658#issuecomment-5852432543) | `f5bef3afc99f71ed69a0321f6d14fe63a2453705` | `ca4feac` · `ac7e0129…` · blob `401804ba` |

Quyết định chủ kho theo vòng nằm ở §0 của r3 (vòng 5: #564 [`5852159297`](https://github.com/ducthangho/tra-luat/issues/564#issuecomment-5852159297)).

## Tệp khác

| tệp | là gì |
|---|---|
| `HAU-KIEM-CONNECTOR-652.md` | 6 finding connector Codex đăng **sau** merge #652, cách xử lý, bảng H (nhãn HINT), bảng S (bề mặt thực thi + `origin` từng lượt), kết quả lượt 8–10 |
| `do_q6.py` · `mut_q6.py` | bộ đo **r2**, r2 trích băm (`36d8f166…`, `272dc1e8…`); giữ nguyên byte, **không** dùng lúc thi công |
| `do_q6_hk.py` · `mut_q6_hk.py` | bộ đo **thi công** của r3 (`0ec537e4…`, `c4f04f03…`) |
| `tu-kiem-q6-2026-09-26.log` · `mut-q6-2026-09-26.log` | bản in bộ đo r2 (31/31, 21/21) |
| `tu-kiem-q6-2026-09-27.log` · `mut-q6-2026-09-27.log` | bản in bộ đo r3 (35/35, 27/27 `TAT_CA_KHOP`) |
| `q6-do-2026-09-26.json` | kết quả Q6 thật trên cây mốc (`1fc99cd9…`); cả hai bộ đo cho ra đúng byte này |
| `tao_r3.py` | script tạo r3 từ r2 (8 lời gọi `rep()`), trích từ transcript phiên soạn; chạy trên bản sao r2 ra r3 giống từng byte |
| `do_bia_mo.py` | phép đo chẩn đoán cho M14 (bẫy khử trùng), không phải bộ đo nghiệm thu |

## Cảnh báo đang có hiệu lực

| id | phải làm gì |
|---|---|
| `MODEL-YEU-CAU-khac-MODEL-DA-PHUC-VU` | `gpt-6-astra`/`high` là thứ **ta yêu cầu** và header CLI công bố; `codex` không phát `modelUsage`, nên model đã phục vụ từng yêu cầu là **KHÔNG ĐO ĐƯỢC**. |
| `ORIGIN-CUC-BO-luot-1-7` | Lượt 1–7 chạy với `origin` của checkout là bare mirror cục bộ; tập tên ref đối chiếu với máy chủ: lượt 1 **lệch 1**, lượt 2–4 lệch 0 (chỉ so tên, OID lấy từ cache), lượt 5–7 KHÔNG ĐO ĐƯỢC độc lập. Từ lượt 8: `origin` thật, so cả tên lẫn OID. Đừng đọc bảy lượt đầu như đã review trên danh tính remote đã xác minh. |
| `CONNECTOR-TU-KICH-KHI-ROI-DRAFT` | Rời draft là tự kích review của connector Codex. #652 đã merge **trong lúc** lượt ấy đang chạy, và 6 finding tới sau merge. Chờ tóm tắt connector ghi `Completed` (và không finding, hoặc đã xử lý) rồi mới merge. #658 làm đúng như vậy. |
| `HINT-KHONG-NHAM-DAC-TA-tu-luot-9` | Từ lượt 9, reviewer chỉ **mô tả bằng lời** mọi sửa nhắm đặc tả (§0 vòng 5). HINT lượt 1–6 nhắm `SPEC.md` giữ nguyên, có nhãn và provenance. |
| `TRAN-10-DA-HET` | Trần `codex_review_calls` 10 (#564 `5851241285`) đã dùng hết. Revision sau của A1a cần chủ kho khai trần mới trước lượt đầu. |
