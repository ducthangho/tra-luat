# wp55 · revision 3 · generation 5 · EXECUTOR handoff (§7) — attempt 2/3

```yaml
schema_version: 1
packet_id: wp55
packet_issue: 55
revision: 3
generation: 5
lease_id: wp55-r3-exec-5-claude-20260815
spec_hash: e321f811724fae97b19d523a3e5159bc13b425cd15fc6c753c7439fe28cae22d
prompt_sha256: b91b5fe54a7a92814c3857a409ed15ac28eec8a97babdb053fb775bd6ca02cbd
provider: claude
role: executor
base_sha: fbe5ab9e1ece3b45c065879bfd59dee2554db3e2
start_head_sha: e6e4b73dc940fcd04e9030e353e0e5fe7f3f0af8
head_sha: 2cccf1ea61859f1b051adb646294ead285dac39c
branch: claude/wp55-r3g5-f3-03
master_sha_at_measurement: 2531366e1abc6cbca0a6c2765e40e54be38d1fb7
attempts_used: 2
attempts_limit: 3
status: needs_followup
next_role: reviewer
next_reviewer_provider: codex          # §8 — executor claude ⇒ reviewer khác nền
```

## TÁM CON SỐ — bốn ma trận, trước/sau

| ma trận | nền (`e6e4b73`) | sau (`2cccf1e`) |
|---|---|---|
| **lọt** (doctrine-scan) | **42/54** — 12 lọt | **54/54** |
| **bắt-oan** | 14/14 | 14/14 |
| **lease** (hình dạng) | 28/28 | 28/28 |
| **codepage** (từ parser) | **24/28** — 4 hỏng | **28/28** |

12 lớp lọt ở nền: `I1–I6` (tag/thuộc tính, tag+comment ngắt dòng, link ngoặc lồng) và
`J1–J5,J7` (cụm đứng một mình). Bốn ca codepage hỏng ở nền chính là P1-2 lộ ra:
`begin-attempt` sau `void-attempt` trả rc=8 vì state kẹt ở `reviewing`.

## Bảy finding — trạng thái

| finding | cách đóng | đột biến chứng minh |
|---|---|---|
| `review-transition-bypasses-record-review` P1 | `CHUYEN_HOP_LE["reviewing"] = ()` — đường ra do VERDICT điều khiển | `mo_lai_cua_reviewing_sang_running` |
| `void-reviewing-accepts-attempt-zero` P1 | hai lớp rời nhau: `void` rời `reviewing`; `record-review` đòi lượt mở và `attempts_used>0` | `bo_void_roi_reviewing` · `bo_record_review_doi_luot_mo` · `bo_record_review_doi_so_luot_duong` |
| `doctrine-html-quoted-angle-bypass` P1 | regex tag phân tích thuộc tính theo CẤU TRÚC (nháy kép/đơn/ký tự thường) thay vì cấm `>` theo vị trí | `tra_regex_tag_ve_cam_ky_tu` |
| `doctrine-common-term-fail-open` P1 | miễn trừ thu về đúng bề rộng AC 19: **chỉ tha khi cụm bị NGẮT QUA DÒNG** | `noi_mien_tru_nhu_generation_4` |
| `ac18-mutation-not-per-class` P2 | đối chứng KHÁC HỌ + `PHU_NHIEU_LOP` khai tường minh + chốt "mỗi lớp lách một đột biến" | chốt số 4 của runner |
| `ac19-false-positive-matrix-incomplete` P2 | `ANH_XA_LOP_BAT_OAN` 41 lớp → 19 ca; suite ĐỎ nếu lớp nào không ánh xạ | chốt số 2 của runner |
| `ac14-codepage-void-attempt-uncovered` P2 | kịch bản sinh từ `build_parser()`; `LENH_KHONG_CO_STDOUT` khai miễn trừ; ĐỎ khi thiếu phủ | chốt trong `_kich_ban_in` |

`ac20-archive-tree-suite-not-self-contained` — **KHÔNG đụng**, chủ kho đã hoãn sang
revision 4. Sửa nó là sửa spec, tức đổi `spec_hash`, tức vô hiệu lease này.

## Gate — rc đọc trực tiếp

```
packet_loop_test   133/133 nền · 30/30 đột biến · 41/41 lớp có ca bắt-oan · TỔNG ĐẠT
doctrine-scan      rc=0
tl --selftest      rc=0 · 1696/1696
doc-claims-check   rc=0 · flags=[]
release-verify     rc=0 · ok=true checked=179 failed=0 extra=0
golden-test        rc=0
eol_policy         rc=0 · scanned=304 violations=0
release-bundle ×3  cả ba = 20c89545566b7682b3ecd2ac2ac0283add5af8a4d6ca377d9acbcde4487f8590
phạm vi            ĐÚNG 6 tệp write_set
```

## AC 20 — cây ĐÃ MERGE, neo SHA bất biến

```bash
MASTER=2531366e1abc6cbca0a6c2765e40e54be38d1fb7
merged=$(mktemp -d)
git archive "$MASTER" | tar -x -C "$merged"
git diff --binary fbe5ab9e1ece3b45c065879bfd59dee2554db3e2..2cccf1ea61859f1b051adb646294ead285dac39c | git -C "$merged" apply
python3 -B "$merged/.claude/dev/packet_loop.py" doctrine-scan --root "$merged"   # rc=0
GIT_DIR="$PWD/.git" python3 -B "$merged/.claude/dev/packet_loop_test.py"          # 133/133, ĐẠT
```

**Dùng `GIT_DIR`** — nói thẳng, không khai là công thức spec chạy được. Công thức
nguyên văn của AC 20 vẫn thiếu điều kiện object store; đó là finding thứ tám, đã hoãn.

## Ba chỗ TÔI TỰ SỬA LẠI THIẾT KẾ CỦA MÌNH — reviewer nên soi

1. **Chốt "đột biến không được giết lan"** — tôi thêm rồi bỏ. Chạy toàn bộ suite dưới
   mỗi đột biến cho kết quả sai dạng: `init_tu_cap_lease_nhu_bug_goc` giết **42 ca** vì
   gần như mọi ca đều gọi `c.init()` dựng nền. Đó là phụ thuộc FIXTURE, không phải "đo
   chung một chốt". Thay bằng ĐỐI CHỨNG KHÁC HỌ.
2. **Chốt "mọi ca phải có đột biến"** — cũng thu hẹp. Áp cho mọi ca thì 65 ca bị báo, gần
   hết là ca CHIỀU THA (`rc=0`) mà một đột biến GỠ chốt không thể giết. AC 18 nói về
   **lớp lách**, nên chốt chỉ áp cho `LOP_LACH`.
3. **Ca `oan_term_giua_cau` chuyển từ bắt-oan sang LỌT.** Câu *"Chỉ người có thẩm quyền
   mới cấp được lease"* trong adapter là CHÉP bảng vai trò §2. AC 2 đòi đỏ; AC 19 chỉ tha
   câu kể lại KẾT QUẢ ĐO bị ngắt dòng. Đây là ĐỔI KỲ VỌNG TEST — reviewer nên phán định.

## Đường ghi GitHub

`api.github.com` vẫn **403** với phiên này. Handoff ghi vào kho theo khuôn đã chạy được.
