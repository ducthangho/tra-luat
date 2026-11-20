# Bằng chứng đặc tả GWS-CRED-DICH-NGOAI-KHO-P2BW r1 (nợ `wp433-p2b-w6-windows`)

Base đo: `94cbb3688427a820de746df60a929e264981d248` (tree `2a38dae886836b7122bd8502d78251c46ff267a5`). Fragment P2b trong cây: sha256
`0175e598ffc3b653b41b37e2e8be0dce918ab5c93237610d015afc4eaaa5dde2`. Nguyên mẫu `nguyen-mau-wp433_gws_cred_dich_ngoai_kho_b.py`: sha256
`8b0904d961e14fb8ed5a9fef315c620430cacd18093d2a50c954b74536bd8b53` (= base + `p2bw.diff`; `git apply --check` sạch trên `94cbb36`).

| tệp | nội dung |
|---|---|
| `p2bw.diff` | M1 nguyên văn (5 chỗ, +5/−4) |
| `chay_p2b.py` | runner một fragment: `python chay_p2b.py <gốc kho> <tệp fragment>` (sha256 `29ef4779…`) |
| `chay_p2b_gia_nt.py` | runner Linux giả lập hình dạng đường nt (`expanduser` ra `<HOME>/./.tra_luat_config.json`) |
| `do433p.py` | driver Desktop (khoá `KHOA.txt`, clone `94cbb36`, hình dạng đường, base ×2, nguyên mẫu ×2) |
| `linux.txt` | Linux, không giả lập: base và nguyên mẫu cùng 36/36, `RUN True` |
| `linux-gia-nt.txt` | Linux, giả lập nt: base `giết_đúng=32`, `VẾ SAI: giet_dung`, `RUN False`; nguyên mẫu 36/36 `RUN True` |
| `desktop/` | lượt Desktop 08:08–08:15Z: zip `wp433p-out-20261120T080807Z.zip` (sha256 `4887d8ca…`, kiểm hai đầu) + bản giải nén (TOM-TAT, stdout/stderr base×2, nguyên mẫu×2, hình dạng đường) |

Hình dạng đường đo trên Desktop (Python 3.12.10, HOME/USERPROFILE = thư mục tạm):

```
expanduser= 'F:\\tl-win\\…\\tp-080807\\hd/.tra_luat_config.json'
join= 'F:\\tl-win\\…\\tp-080807\\hd\\.tra_luat_config.json'
bang_chuoi= False
bang_sau_chuan_hoa= True
```
