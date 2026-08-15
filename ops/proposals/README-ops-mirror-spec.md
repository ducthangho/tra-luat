# ĐỀ XUẤT (chưa áp) — `ops-mirror-spec`: chiếu spec lên THÂN Issue bằng git

Soạn bởi phiên executor wp55 `wp55-r3-exec-4-claude-20260814`, 2026-08-15, theo yêu cầu
"soạn diff cho tôi duyệt".

**Đây là ĐỀ XUẤT BẤT HOẠT.** Diff nằm ở `ops/proposals/ops-mirror-spec.diff`, KHÔNG nằm ở
`.github/workflows/`. Cố ý: với sự kiện `push`, GitHub chạy workflow **lấy từ chính nhánh
được đẩy**, nên đặt tệp đúng chỗ trên bất kỳ nhánh `ops/**` nào là nó SỐNG ngay. Một phiên
agent chỉ có quyền git mà tự đặt một workflow `issues: write` vào kho chính là kịch bản leo
thang mà chú thích trong `ops-publish-lease.yml` đã cảnh báo. Nên nó nằm ở đây, chờ duyệt.

Áp khi đã duyệt:

```bash
git apply ops/proposals/ops-mirror-spec.diff     # đã kiểm `--check` sạch trên master 2531366
```

## Diff gồm gì

| tệp | dòng | vai |
|---|---|---|
| `.github/workflows/ops-mirror-spec.yml` | 140 | cầu git→API, shell mỏng |
| `ops/mirror_spec.py` | 211 | toàn bộ logic kiểm + dựng thân, KHÔNG gọi mạng |
| `ops/mirror_spec_test.py` | 500 | 21 phản chứng + 9 đột biến tự chứng minh không rỗng |

Logic nằm trong script chứ không nhúng python vào YAML, vì **YAML không test được**. Cùng
cách phân chia mà `ops/lease_publish.py` + `ops-publish-lease.yml` đang dùng.

## Điểm khác biệt QUYẾT ĐỊNH so với cửa lease — đọc trước khi duyệt

`ops-publish-lease.yml` chỉ **THÊM** comment: sai thì bản cũ còn nguyên để đối chiếu.
Cửa này **GHI ĐÈ** thân issue: một lượt chạy sai xoá sạch văn bản gõ tay, và trong kho
không có bản sao để dựng lại. Rủi ro cao hơn hẳn, nên có ba chốt cửa lease không cần:

- **A · quyền sở hữu** — chỉ ghi khi thân RỖNG hoặc đã mang dấu `<!-- ops-mirror-spec v1`.
  Thân do người viết mà không có dấu thì TỪ CHỐI. Không "hợp nhất thông minh".
- **B · idempotent theo nội dung** — thân mới trùng thân cũ thì không gọi `PATCH`.
- **C · đọc lại đối chiếu BYTE sau khi ghi** — đường đăng của kho này ĐÃ TỪNG làm biến
  dạng ký tự (thân #55 còn `&#34;` nguyên văn). Lệch thì job ĐỎ, không khai "đã đăng".

Cộng hai lớp kế thừa từ cửa lease: chỉ nhánh `ops/**` + path hẹp; và **bộ kiểm neo vào
NHÁNH MẶC ĐỊNH** (finding P1 của PR #104 — *bộ kiểm nằm cùng nhánh với thứ nó kiểm thì nó
không kiểm gì hết*). Và một lớp riêng: **opt-in `[mirror-spec]`** trong commit cuối.

## Đã chạy thử — sáu đường, không chỉ đường thành công

Chạy `ops/mirror_spec.py` trên bản chiếu #119 thật:

```text
1  check, bản chiếu chưa khai khối ```mirror```   → CHẶN(8)  ✓
2  check, đủ mỏ neo                               → rc=0 "băm khớp 1740b1c5…, thân 6617 ký tự"
3  issue                                          → 119
4  body                                           → dòng đầu là dấu sở hữu ✓
5  guard · thân RỖNG                              → cho ghi đè ✓
6  guard · thân NGƯỜI viết                        → CHẶN(8) ✓
7  guard · thân có dấu sở hữu                     → cho ghi đè ✓
8  spec TRÔI băm (sửa 1 byte)                     → CHẶN(6) ✓
```

Chốt số 8 là cái đáng giá nhất: nó bắt **bản chiếu trôi khỏi spec**. Sửa spec mà quên cập
nhật bản chiếu thì thân issue nói một đằng, kho một nẻo, và không ai biết.

## Bộ phản chứng — ĐÃ CÓ, đã chạy

`ops/mirror_spec_test.py`: **21/21 ca nền đạt**, **9/9 đột biến giết đúng ca đích**,
`rc=0`. Gate EOL của kho: `ok=true`, 330 tệp, 0 vi phạm.

```text
nền: 21/21 đạt
  ok  bo_kiem_bam_spec                  → giết 1/1: t06_bam_LECH
  ok  bo_kiem_dang_bam                  → giết 1/1: t05_bam_SAI_DANG (neo THÔNG ĐIỆP)
  ok  bo_kiem_packet_issue_khop_spec    → giết 1/1: t07_packet_issue_LECH
  ok  bo_chan_ky_tu_va_dau_cham         → giết 1/1: t10_leo_RA_NGOAI_kho
  ok  bo_relative_to                    → giết 1/1: t11_SYMLINK_ra_ngoai
  ok  bo_resolve_nen_symlink_lot        → giết 1/1: t11_SYMLINK_ra_ngoai
  ok  bo_kiem_than_rong                 → giết 1/1: t15_than_RONG
  ok  bo_chot_quyen_so_huu              → giết 2/2: t18_than_NGUOI_VIET, t20_dau_gia_mao
  ok  chot_so_huu_nhan_dau_o_BAT_KY_dau → giết 1/1: t20_dau_gia_mao
mirror_spec: ĐẠT
```

**Ba chỗ bộ đột biến bắt được LỖI TRONG CHÍNH BỘ TEST — ghi lại vì đó là giá trị của nó:**

1. `t05` (băm sai dạng) ban đầu chỉ đo `rc`, nên gỡ chốt DẠNG băm nó VẪN xanh — chốt SO
   BĂM bên dưới vớt. Chốt dạng không bắt thêm ca nào; nó chỉ làm thông điệp đúng chỗ. Đã
   sửa: ca neo vào CÂU CHỮ. Cùng kết luận `lease_publish_test.py::t20` đã tự ghi.
2. `t10` ban đầu chỉ đòi "khác 0", nên nó xanh cả khi đường dẫn bị chặn vì lý do KHÁC. Đã
   sửa: đòi đúng `RC_THAM_SO`. Ca cô lập chốt chuỗi là ký tự `\` — trên Linux đó là ký tự
   tên tệp hợp lệ nên `PurePosixPath` bỏ qua, chỉ chốt chuỗi bắt được.
3. `t11` (symlink) ban đầu khai băm của TỆP SPEC trong khi symlink trỏ tệp NGOÀI có nội
   dung khác ⇒ chốt SO BĂM bắt trước, nên ca đang đo chốt băm chứ không đo `resolve()`.
   Đã sửa: tệp ngoài mang nội dung hợp lệ và bản chiếu khai đúng băm của NÓ.

Và một ca **cố ý không thuộc đột biến nào**: `t09` (`spec_path` tuyệt đối) bị phủ HAI lớp
— chốt chuỗi và `resolve()`+`relative_to()` — nên không đột biến đơn lẻ nào giết được.
Nói thẳng chỗ phủ chồng còn hơn gán bừa rồi tưởng đã đo được lớp ấy.

## ⛔ HAI VIỆC BẮT BUỘC TRƯỚC KHI MERGE

1. **Ruleset.** Chưa chặn push vào `.github/workflows/**` và `ops/mirror_spec*.py` thì
   đường này vẫn quy về *"ai push được vào `ops/**` thì GHI ĐÈ được thân issue"*. Với cửa
   ghi đè, câu đó nặng hơn hẳn cửa chỉ thêm comment. Đừng merge rồi mới đặt ruleset.
2. **Bản chiếu phải thêm khối `mirror`.** `ops/specs/wp119-r1-than-issue.md` hiện chưa có
   khối khai `spec_path`/`spec_hash`/`packet_issue` (đó là lý do phép thử số 1 CHẶN đúng).
   Khối này cố ý KHÔNG được thêm sẵn: thêm nó vào rồi push lên `ops/**` với nhãn
   `[mirror-spec]` là kích hoạt cửa — việc ấy phải xảy ra SAU khi bạn duyệt, không phải
   trước.

## Phần còn thủng, nói thẳng

Với sự kiện `push`, GitHub lấy **chính tệp YAML này** từ head được đẩy. Ai sửa được
`ops/mirror_spec.py` thì cũng sửa được YAML và gỡ luôn mỏ neo lớp 4. Lớp 4 đóng đường
"một push đổi bộ kiểm"; nó **KHÔNG** biến `push` thành thao tác có thẩm quyền. Thứ đóng nốt
phần còn lại nằm ngoài kho — ruleset. Đây là cùng một giới hạn mà `ops-publish-lease.yml`
đã tự khai; đề xuất này không giả vờ đã giải quyết nó.
