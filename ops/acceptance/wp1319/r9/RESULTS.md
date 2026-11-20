# WP1319 r9 — Miễn U11 theo quyết định của chủ kho; phép thử đường hầm IAP do chủ kho tự chạy

**Căn cứ:** đặc tả `ops/specs/wp1319-r9.md`, lease `ops/leases/wp1319-r9-g1-operator.yaml`.

## 1. Bối cảnh
- r8 (`../r8/RESULTS.md`) đã đo:
  - VM ở `10.70.0.2/24`;
  - ASUS không cùng mạng, và TCP từ ASUS tới cổng `5985`/`5986` hết hạn.
- Chủ kho cho biết (20/11): *"Tôi vào VM thông qua gcloud cli, chạy trên máy ASUS"*. Tức VM là máy Google Compute Engine; `10.70.0.2` là IP nội bộ trong VPC.
- Phiên điều phối hướng dẫn chủ kho mở đường hầm IAP tới cổng WinRM. Chủ kho tự chạy các lệnh trên ASUS và dán đầu ra vào phiên.

## 2. Đầu ra chủ kho dán vào phiên (lời khai, chép nguyên văn)
**Nhãn:**
- Đây là **lời khai của chủ kho**, chạy trên ASUS dưới tài khoản `admin`, pwsh 7.
- Phiên điều phối **không** tự chạy lại các lệnh này, và **không** có băm hay biên nhận từ host.
- Nguồn có thẩm quyền là đoạn chép dưới đây.

### 2.1 Đường hầm IAP tới 5986 và 5985
```text
PS7 C:\Users\admin> gcloud compute start-iap-tunnel tra-luat-win 5986 --local-host-port=localhost:15986 --zone asia-southeast1-a
WARNING:

To increase the performance of the tunnel, consider installing NumPy. For instructions,
please see https://cloud.google.com/iap/docs/using-tcp-forwarding#increasing_the_tcp_upload_bandwidth

Testing if tunnel connection works.
ERROR: (gcloud.compute.start-iap-tunnel) While checking if a connection can be made: Error while connecting [4003: 'failed to connect to backend']. (Failed to connect to port 5986)
PS7 C:\Users\admin> gcloud compute start-iap-tunnel tra-luat-win 5985 --local-host-port=localhost:15985 --zone asia-southeast1-a
WARNING:

To increase the performance of the tunnel, consider installing NumPy. For instructions,
please see https://cloud.google.com/iap/docs/using-tcp-forwarding#increasing_the_tcp_upload_bandwidth

Testing if tunnel connection works.
ERROR: (gcloud.compute.start-iap-tunnel) While checking if a connection can be made: Error while connecting [4003: 'failed to connect to backend']. (Failed to connect to port 5985)
```

### 2.2 Danh sách luật firewall của project
Lần đầu dùng bộ lọc `--filter="sourceRanges:35.235.240.0/20"` thì gcloud báo `Invalid list filter expression`. Đây là lỗi cú pháp trong lệnh do phiên điều phối đưa. Lần chạy lại không lọc:
```text
PS7 C:\Users\admin> gcloud compute firewall-rules list --format="table(name,network.basename(),direction,sourceRanges.list(),allowed[].map().firewall_rule().list(),targetTags.list(),disabled)"
NAME: default-allow-icmp
NETWORK: default
DIRECTION: INGRESS
SOURCE_RANGES: 0.0.0.0/0
ALLOW: icmp
TARGET_TAGS:
DISABLED: False

NAME: default-allow-internal
NETWORK: default
DIRECTION: INGRESS
SOURCE_RANGES: 10.128.0.0/9
ALLOW: tcp:0-65535,udp:0-65535,icmp
TARGET_TAGS:
DISABLED: False

NAME: default-allow-rdp
NETWORK: default
DIRECTION: INGRESS
SOURCE_RANGES: 0.0.0.0/0
ALLOW: tcp:3389
TARGET_TAGS:
DISABLED: False

NAME: default-allow-ssh
NETWORK: default
DIRECTION: INGRESS
SOURCE_RANGES: 0.0.0.0/0
ALLOW: tcp:22
TARGET_TAGS:
DISABLED: False

NAME: tra-luat-allow-iap-rdp
NETWORK: tra-luat-vpc
DIRECTION: INGRESS
SOURCE_RANGES: 35.235.240.0/20
ALLOW: tcp:3389
TARGET_TAGS: tra-luat-windows
DISABLED: False
```

### 2.3 Lệch: `Get-NetFirewallRule` chạy trên ASUS, không phải VM
Lệnh xem Windows Firewall lẽ ra phải chạy **trên VM**. Dấu nhắc `PS7 C:\Users\admin>` cho thấy nó chạy trên **ASUS**, nên kết quả dưới là của ASUS và **không** dùng làm dữ kiện về VM. Windows Firewall của VM với WinRM: **không đo được**.
```text
DisplayName                                              Enabled Direction Action         Profile
-----------                                              ------- --------- ------         -------
Windows Remote Management (HTTP-In)                        False   Inbound  Allow          Public
Windows Remote Management - Compatibility Mode (HTTP-In)   False   Inbound  Allow Private, Public
Windows Remote Management (HTTP-In)                         True   Inbound  Allow Domain, Private
Windows Remote Management - Compatibility Mode (HTTP-In)   False   Inbound  Allow          Domain
```

## 3. Đọc kết quả
- Việc đường hầm IAP tới VM được coi là **thử đúng VM** dựa trên lời khai của chủ kho: tên `tra-luat-win`, zone `asia-southeast1-a`. Phiên điều phối không đối chiếu được instance ấy với `f7281f27` bằng băm (U2 r5).
- Mã `4003: failed to connect to backend` ở cả hai cổng nghĩa là IAP tới được instance nhưng không mở được kết nối tới cổng đích.
- Trong danh sách firewall, chỉ một luật nằm trên mạng `tra-luat-vpc` và cho nguồn IAP `35.235.240.0/20`: `tra-luat-allow-iap-rdp`, **chỉ** `tcp:3389`, tag `tra-luat-windows`. Các luật `default-*` thuộc mạng `default`.
  - Giả định VM thuộc `tra-luat-vpc` và mang tag `tra-luat-windows` là **suy ra** từ tên luật. Network và tag của instance **chưa được đo**.
  - Với giả định ấy, cổng `5985`/`5986` không có luật nào cho IAP; điều này **phù hợp** với lỗi `4003`. Nhưng không loại trừ được việc Windows Firewall trên VM cũng chặn, vì phép đo ở 2.3 chạy nhầm máy.
- Kết luận dữ kiện: **từ ASUS qua IAP, hiện chỉ vào VM được bằng RDP (3389). Đường WinRM từ xa chưa được mở.**

## 4. Quyết định của chủ kho
Phiên điều phối đưa ba lựa chọn:
1. miễn U11;
2. chủ kho tự đo xác thực từ trong VM (loopback) qua RDP;
3. mở luật firewall hẹp (đổi hạ tầng LIVE).

Chủ kho chọn **"Miễn U11"** (20/11, AskUserQuestion; lời khai của phiên điều phối). Lý do ghi kèm lựa chọn: kiến trúc thực tế chỉ vào VM bằng RDP qua IAP; WinRM từ xa không được dùng.

Ghi vào MATRIX:
- U11 → `owner_waived`; dữ kiện `not_evidenced` giữ nguyên.
- §11 #2 giữ `partial`, thêm ghi chú đường WinRM từ xa chưa mở.
- **Không** đổi firewall, WinRM, TrustedHosts hay cấu hình nào.

## 5. Giới hạn
- Toàn bộ mục 2 là lời khai, không phải phép đo của phiên điều phối.
- Chưa đo network và tag của instance `tra-luat-win`, nên việc gắn luật `tra-luat-allow-iap-rdp` với VM là suy luận.
- Windows Firewall của VM với WinRM: không đo được (mục 2.3).
- Không có phép đo nào về xác thực WinRM: U11 được miễn, không được chứng minh.
