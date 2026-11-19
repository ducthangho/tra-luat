# WP1319 r5: đo chỉ đọc U2, U9 và lịch kiểm release trên ASUS (19/11, 15:03–15:12Z)

Đặc tả `ops/specs/wp1319-r5.md`, lease `ops/leases/wp1319-r5-g1-operator.yaml`. Packet chỉ đọc, không lấy khoá host, không inference.

**Driver:** `R5.ps1`, cùng một bản trên ba máy.
- Lượt đầu, sha256 `e1498db6…`, có **lỗi dựng**: hàm băm đặt tên `H` bị alias `h` → `Get-History` che (trong PowerShell, alias được ưu tiên hơn function). Vế U2 vì thế ném lỗi trên cả ba máy.
- Lượt chạy lại 1/1 dùng bản đã đổi tên hàm thành `Get-R5Sha`, sha256 `0a24594c4ae9fc24de8c08510c402008f2e8b0ad331704522d546304c3144d1a`. Băm của script được kiểm trên ASUS trước khi chạy.

**Lệch so với đặc tả:**
1. **ASUS hết chỗ trên ổ D.** Ghi script vào `D:\tl-win\…` thì gặp `ENOSPC`, còn sót lại một tệp 0 byte `D:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r5\R5.ps1`. Script và kết quả trên ASUS vì thế đặt ở `C:\Users\admin\tl-work\r5-session_015GtxrapMSm976JLC7Fp1HM\`.
2. **Không đóng zip.** Mỗi kết quả là một tệp JSON nhỏ. Mỗi tệp được đọc về, dựng lại byte-exact (dòng kết thúc CRLF, kèm LF cuối) và đối chiếu sha256 với giá trị script in trên chính host đó. Cả ba khớp. Nguyên văn nằm ở cuối tệp này.

## Kết quả
| Hàng | Kết quả | Điều kiện đọc |
|---|---|---|
| **U2** danh tính VM | **passed (scoped `f7281f27`)** | MachineGuid và UUID phần cứng (chỉ lưu sha256) của `TRA-LUAT-WIN` (`f10fdf96…` / `cb2800ae…`) khác Desktop (`f6cf446d…` / `4f8e903d…`) và khác ASUS (`cdde655f…` / `d80fc985…`). Windows Server 2022 Datacenter build 20348, cài ngày 2026-10-28, boot lần cuối 2026-11-18T14:36Z. **`810f79bb` offline nên không đo được**: không suy được nó có cùng máy với `f728` hay không |
| **U9** ổ D trên ASUS | **đo được; dữ kiện xấu** | NTFS, 55 341 740 032 byte (51,54 GiB), **trống 8 192 byte**. Ổ C còn khoảng 19,9 GB. ACL của `D:\`: owner `SYSTEM`; `Authenticated Users` có Modify; `Users` có ReadAndExecute; `SYSTEM` và `Administrators` có FullControl; không ACE nào kế thừa. `PLAYWRIGHT_BROWSERS_PATH` **không đặt** ở cả phạm vi User lẫn Machine |
| Kiểm release hằng ngày, ASUS | **not_present** | 209 tác vụ lập lịch được quét, 0 tác vụ có tên hay hành động khớp `proxima\|playwright\|traluat` |

**Finding vận hành, cần chủ kho quyết, phiên điều phối không tự dọn:**
- Ổ D của ASUS đã **đầy**. `pwsh` (`D:\Program Files\PowerShell\7`) và các thư mục làm việc `D:\tl-win`, `D:\Quốc hội\tra-luat` đều nằm trên ổ này.
- Hệ quả: mọi lượt chạy native cần ghi lên D (bằng chứng, cache, build) sẽ hỏng ngay.
- Với U9, nếu sau này đặt `PLAYWRIGHT_BROWSERS_PATH` lên D thì phải dọn hoặc mở rộng ổ trước.

## Sau khi dọn ổ D (19/11, 16:46–16:48Z, lease g2 chỉ để ghi sổ)
Chủ kho duyệt trong phiên: *"Dọn ô D, đồng ý 1,2"* (16:28Z). Phạm vi duyệt:
1. `D:\tlx`: chỉ xoá thư mục con không có thay đổi chưa commit, commit chưa đẩy hay stash, và không có tiến trình nào đang dùng.
2. Đổ thùng rác của ổ D.

Đây là thao tác **ghi** trên host, làm theo chỉ thị trực tiếp của chủ kho. Nó **nằm ngoài** đặc tả r5 (vốn chỉ đọc); g2 chỉ ghi sổ kết quả.

**Trước khi dọn:**
- Chủ kho đã tự giải phóng một phần: D từ 8 KB lên 824 MB trống.
- Kiểm từng thư mục bằng `tlx-check.ps1` và `tlx-check2.ps1`. Head của mỗi kho git được đối chiếu trên GitHub qua REST `compare`:
  - `l1265`, `lease-p1`, `p1`: head nằm trên nhánh còn sống (`behind_by 0`);
  - `rv1\cay-kho` và các bản `dcc-scratch\*\nen` (`9c1661f7`): head nằm trong master.
- "Commit chưa đẩy" báo trên máy (226 / 226 / 2) là do ref remote ở máy đã cũ.

**Đã xoá** (script `clean-d.ps1` kiểm lại ngay trước mỗi lần xoá: đường dẫn, reparse point, HEAD đúng SHA, dirty 0, stash 0, không tiến trình nào dùng):
`D:\tlx\l1265`, `D:\tlx\lease-p1`, `D:\tlx\p1`, `D:\tlx\rv1\cay-kho`, `D:\tlx\dcc-scratch\do\nen`, `D:\tlx\dcc-scratch\wip\nen`, cùng thùng rác ổ D.

**Giữ lại** vì không đạt điều kiện:
- có thay đổi chưa commit: `dcc`, `dcc-scratch\do\sau`, 4 thư mục `dcc-scratch\do-db\*`, `rv2\cay-kho` (13 300 thay đổi);
- head không chứng minh được nằm trên nhánh nào còn sống: `rv-1321\cay-kho`, `rv-1322\cay-kho`;
- thư mục không phải git (có thể là bằng chứng duy nhất): `rv-*`, `km*`, `*-run`, `*-scratch`.

Không đụng `D:\WSL`, `Dữ liệu`, `Quốc hội` và phần mềm đã cài.

**Kết quả: ổ D trống 2 003,3 MB** (khoảng 3,8% của 51,54 GiB). Nhật ký nguyên văn (`C:\Users\admin\tl-work\r5-session_015GtxrapMSm976JLC7Fp1HM\clean-d.log`):
```text
2026-11-19T16:46:47.8686148Z BAT DAU free_D_MB=824
2026-11-19T16:47:04.9474965Z DA XOA D:\tlx\l1265 head=ab16b97885b9773e1086a919e5b92bdbfb8ba252 gone=True free_D_MB 824 -> 993.1
2026-11-19T16:47:19.1562552Z DA XOA D:\tlx\lease-p1 head=91188e98858ed4a3869821b801d12503110a5738 gone=True free_D_MB 993.1 -> 1165
2026-11-19T16:47:36.2573691Z DA XOA D:\tlx\p1 head=2b6ff1574dd3d26908eb4bb8c425df87b0ad6d9f gone=True free_D_MB 1173.5 -> 1378.1
2026-11-19T16:47:54.7407192Z DA XOA D:\tlx\rv1\cay-kho head=e97d5d87f4f17c14fe350fb2fe56eddbd9301c9e gone=True free_D_MB 1378.1 -> 1549.8
2026-11-19T16:48:13.4652325Z DA XOA D:\tlx\dcc-scratch\do\nen head=9c1661f76d5f4ef811aa349df102989cc2e2d53d gone=True free_D_MB 1549.8 -> 1722.5
2026-11-19T16:48:32.1435077Z DA XOA D:\tlx\dcc-scratch\wip\nen head=9c1661f76d5f4ef811aa349df102989cc2e2d53d gone=True free_D_MB 1722.5 -> 1895.1
2026-11-19T16:48:35.0086176Z DA DO THUNG RAC D free_D_MB 1895.1 -> 2003.3
2026-11-19T16:48:35.1352487Z KET THUC free_D_MB=2003.3
```
Còn sót một tệp 0 byte `D:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r5\R5.ps1`, sinh ra từ lần ghi hỏng do ENOSPC.

**Nếu cần thêm chỗ** (chủ kho quyết): `D:\WSL\Ubuntu-Clean` 13,9 GB nếu không còn dùng WSL; `D:\tlx\dcc-scratch\do-db` 1,17 GB, bỏ 4 thay đổi chưa commit của một packet đã xong.

## Nguyên văn

### TRA-LUAT-WIN (`f7281f27`), `C:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r5\r5-vm-2.json`
sha256 trên host: `169110fb339e3dbbe857cbad6d6dc9d59fc0598e4540c1c2f1ef20f2c76fc93f` (bản CRLF; đã dựng lại và khớp)

```json
{
  "schema": "wp1319_r5_probe.v1",
  "utc": "2026-11-19T15:12:12.0143081Z",
  "errors": [],
  "u2": {
    "hostname": "TRA-LUAT-WIN",
    "user": "TRA-LUAT-WIN\\tlcommander",
    "machine_guid_sha256": "f10fdf96445fed1345e8e349b2e461d8a2ce189a3735e75e4c12167848989b99",
    "product_uuid_sha256": "cb2800aee768b3e186bf1d14038431be44f4dfb018e9afdd2397b8b91483d452",
    "os_caption": "Microsoft Windows Server 2022 Datacenter",
    "os_build": "20348",
    "install_date_utc": "2026-10-28T16:53:58.0000000Z",
    "last_boot_utc": "2026-11-18T14:36:34.5000000Z"
  }
}
```

### DESKTOP-T9R33P2 (`a5f7076e`), `F:\tl-win\session_015GtxrapMSm976JLC7Fp1HM\r5\r5-desktop-2.json`
sha256 trên host: `c5c6861f5de6feafabef7d6dedd704876873ff99e6c23f0b79563e96f68dc873` (bản CRLF; đã dựng lại và khớp)

```json
{
  "schema": "wp1319_r5_probe.v1",
  "utc": "2026-11-19T15:12:09.7934900Z",
  "errors": [],
  "u2": {
    "hostname": "DESKTOP-T9R33P2",
    "user": "DESKTOP-T9R33P2\\ThangHD",
    "machine_guid_sha256": "f6cf446d181992c46eda695100cc3886cad49fb33110e159d12a9686fca74e25",
    "product_uuid_sha256": "4f8e903d48444eb737d06d7a8fd4c48130eedde98cd7ae82a5f2f3410b8435b9",
    "os_caption": "Microsoft Windows 11 Pro",
    "os_build": "26300",
    "install_date_utc": "2026-09-27T10:38:31.0000000Z",
    "last_boot_utc": "2026-11-11T02:34:43.5000000Z"
  }
}
```

### ASUS-LAPTOP (`7404cfba`), `C:\Users\admin\tl-work\r5-session_015GtxrapMSm976JLC7Fp1HM\r5-asus-2.json`
sha256 trên host: `313e45724ae8e578ad085866e3d8f2d3dd8b4e0cb66ca406500c27586d0cb39b` (bản CRLF; đã dựng lại và khớp)

```json
{
  "schema": "wp1319_r5_probe.v1",
  "utc": "2026-11-19T15:12:06.1776675Z",
  "errors": [],
  "u2": {
    "hostname": "ASUS-LAPTOP",
    "user": "ASUS-LAPTOP\\admin",
    "machine_guid_sha256": "cdde655fa01607ce841d161a0f28c16fa4320b57e3b0d897d06aec66efd774f4",
    "product_uuid_sha256": "d80fc98518550df557095aeee02f99578a204d89f05dc4c63fc9f69ea8eb0a6e",
    "os_caption": "Microsoft Windows 11 Home Single Language",
    "os_build": "26300",
    "install_date_utc": "2025-01-11T11:26:02.0000000Z",
    "last_boot_utc": "2026-11-18T14:00:32.5038470Z"
  },
  "u9": {
    "d_exists": true,
    "filesystem": "NTFS",
    "size_bytes": 55341740032,
    "free_bytes": 8192,
    "label": "New Volume",
    "d_root_owner": "NT AUTHORITY\\SYSTEM",
    "d_root_access": [
      {
        "id": "NT AUTHORITY\\Authenticated Users",
        "rights": "-536805376",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "NT AUTHORITY\\Authenticated Users",
        "rights": "Modify, Synchronize",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "NT AUTHORITY\\SYSTEM",
        "rights": "FullControl",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "NT AUTHORITY\\SYSTEM",
        "rights": "268435456",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "BUILTIN\\Administrators",
        "rights": "268435456",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "BUILTIN\\Administrators",
        "rights": "FullControl",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "BUILTIN\\Users",
        "rights": "ReadAndExecute, Synchronize",
        "type": "Allow",
        "inherited": false
      },
      {
        "id": "BUILTIN\\Users",
        "rights": "-1610612736",
        "type": "Allow",
        "inherited": false
      }
    ],
    "playwright_browsers_path": {
      "user": null,
      "machine": null
    },
    "pw_dirs": []
  },
  "tasks": [],
  "tasks_scanned": 209
}
```
