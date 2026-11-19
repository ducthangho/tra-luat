# WP1319 r6 — Vị trí cache trình duyệt của add-on Playwright trên ASUS (đo chỉ đọc)

**Căn cứ:** đặc tả `ops/specs/wp1319-r6.md` (sha256 `cfecbe61…`). Lease `ops/leases/wp1319-r6-g1-operator.yaml` (đã thu hồi) và `ops/leases/wp1319-r6-g2-operator.yaml`. Hàng U9 sau PR #1426 ghi nơi add-on thật sự đặt cache là **chưa kiểm**.

**Máy:** ASUS-LAPTOP (`7404cfba`), PS 7.6.9, tài khoản Desktop Commander. Thư mục làm việc `C:\Users\admin\tl-work\r6-session_015GtxrapMSm976JLC7Fp1HM\`. Không lấy khoá host vì không có thao tác ghi nào trên host.

## Các lượt chạy
| Lượt | Lease | Kết quả |
|---|---|---|
| 1 | g1 | **Hỏng do lỗi dựng.** Chạy bằng Windows PowerShell 5.1: phiên ấy không nạp được `Get-FileHash`, và script ném lỗi khi gán `errors`. Không có JSON. |
| 2 | g1 | **Hỏng do lỗi dựng.** Chạy bằng pwsh 7.6.9: biến vòng lặp `$r` ghi đè biến kết quả `$R`, vì tên biến PowerShell không phân biệt hoa thường; lỗi `The property 'caches' cannot be found`. Không có JSON. |
| — | — | Hết 2/2 lượt của g1. Đã sửa (đổi `$r` thành `$scanRoot`; soát lại tên biến không phân biệt hoa thường: không còn trùng). Chủ kho cấp thêm 1 lượt (g2). |
| 3 | g2 | **Đạt.** Script sha256 `30dd27702d74e86f559db5d2e9d5b13a048bf759f58dc9a65ef2faa1fd3707b1`, băm khớp giữa container và ASUS, parser PS 7 cho 0 lỗi. JSON 21:18:52Z, `errors` rỗng. |

Cả ba lượt chỉ ghi vào thư mục làm việc của phiên.

## Kết quả (lượt 3)
- `TL_PW_ROOT` và `PLAYWRIGHT_BROWSERS_PATH`: **chưa đặt** ở cả ba phạm vi Process (tiến trình Desktop Commander), User và Machine.
- **Hai cache add-on hiện có đều nằm trên ổ C**, là hai add-on của P3:
  - `C:\Users\admin\tl-work\mission1238-asus-20261112-P3\addon-ps51\browsers`: 315 tệp, 467 067 094 byte;
  - `C:\Users\admin\tl-work\mission1238-asus-20261112-P3\addon-ps7\browsers`: 315 tệp, 467 067 093 byte;
  - mỗi cache có một thư mục con `0.1.0`; `install\0.1.0\package-lock.json` của cả hai có sha256 `0da56e1e…`, khớp lock P3 đã ghi.
- **Không có** thư mục `browsers` hay `ms-playwright` nào dưới `D:\tl-win` (độ sâu ≤ 4).
- Thư mục mặc định `C:\Users\admin\AppData\Local\ms-playwright`: 18 tệp, 7 759 byte, thư mục con `b` và `daemon`. Đây là dư lượng `daemon` mà P3 đã ghi (F1), không phải cache trình duyệt.
- Không có tiến trình `node.exe` hay `chrome.exe` nào chạy từ các thư mục trên.
- Dung lượng trống: C 21 092 708 352 byte; D 2 100 563 968 byte.

## Ghi nhận
- U9: cache trình duyệt của các add-on hiện có **đã nằm trên ổ C**, đúng với lựa chọn của chủ kho. Không chuyển hay cài gì.
- **Sửa lời khai của hàng U9 bản PR #1426.** Câu *"P3 ghi mỗi add-on trên ASUS có cache riêng dưới `D:\tl-win\…`"* là sai. P3 (`RAW-P3-VERDICT-claude-xhigh.md` §11 #5 và F4) chỉ ghi **nguồn seed** của cache nằm trên D (nay không còn). Hai cache thật nằm trên C như đo ở trên.
- Mẫu `TL_PW_ROOT` trong `.agents/skills/playwright-browser/SKILL.md` vẫn ghi ổ D. Vì vậy lượt cài kế tiếp phải đặt `TL_PW_ROOT` trên C một cách tường minh.

## Giới hạn
- Trường `installation_complete` chỉ kiểm **một cấp** dưới `browsers` (tức `browsers\0.1.0`), trong khi `INSTALLATION_COMPLETE` nằm sâu hơn một cấp (`browsers\0.1.0\chromium-*`). Danh sách rỗng ở đây **không** chứng minh cache cài dở. P3 đã ghi tệp ấy có mặt.
- Biến môi trường của các lượt khởi chạy add-on về sau được đặt trong tiến trình, nên không đo trước được.
- Chỉ quét `D:\tl-win` và `C:\Users\admin\tl-work` tới độ sâu 4, cộng thư mục mặc định. Cache đặt ở nơi khác không nằm trong phép đo.
- Tiến trình chỉ lọc theo đường dẫn thực thi của `node.exe`/`chrome.exe`.

## Bằng chứng nguyên văn
`r6-asus-g2.json` trên host, sha256 `6dcdbafcd1eb80b22411443244f5ad87bed9bad3e2d3b752f5d6d056f8af74b2` (in ở host). Tệp trên host dùng CRLF giữa các dòng và một LF ở cuối. Đổi mỗi LF trong khối dưới thành CRLF rồi thêm một LF ở cuối sẽ ra đúng băm trên; đã kiểm trong container.

```json
{
  "schema": "wp1319_r6_probe.v1",
  "utc": "2026-11-19T21:18:52.5240113Z",
  "host": "ASUS-LAPTOP",
  "errors": [],
  "env": {
    "TL_PW_ROOT": {
      "process": null,
      "user": null,
      "machine": null
    },
    "PLAYWRIGHT_BROWSERS_PATH": {
      "process": null,
      "user": null,
      "machine": null
    }
  },
  "caches": [
    {
      "path": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps51\\browsers",
      "drive": "C",
      "files": 315,
      "bytes": 467067094,
      "children": [
        "0.1.0"
      ],
      "installation_complete": [],
      "addon_root": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps51",
      "lock_present": true,
      "lock_sha256": "0da56e1ee6b81ad9226f000a917f6153b95e861ed41811d5eca7deb01bbb8ede"
    },
    {
      "path": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps7\\browsers",
      "drive": "C",
      "files": 315,
      "bytes": 467067093,
      "children": [
        "0.1.0"
      ],
      "installation_complete": [],
      "addon_root": "C:\\Users\\admin\\tl-work\\mission1238-asus-20261112-P3\\addon-ps7",
      "lock_present": true,
      "lock_sha256": "0da56e1ee6b81ad9226f000a917f6153b95e861ed41811d5eca7deb01bbb8ede"
    },
    {
      "path": "C:\\Users\\admin\\AppData\\Local\\ms-playwright",
      "drive": "C",
      "files": 18,
      "bytes": 7759,
      "children": [
        "b",
        "daemon"
      ],
      "installation_complete": [],
      "addon_root": "C:\\Users\\admin\\AppData\\Local",
      "lock_present": false
    }
  ],
  "procs": [],
  "free": {
    "C": 21092708352,
    "D": 2100563968
  }
}
```
