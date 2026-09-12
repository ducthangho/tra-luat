# EVIDENCE — goi hien vat cho reviewer

Sinh boi `ops/dung_goi_review.sh` luc `2026-09-07T22:43:15Z`. Moi so duoi day do SCRIPT tinh, khong chep tay.

## Cach trich tung so

| so | trich bang | loai nguon |
|---|---|---|
| ref may chu | `git ls-remote --heads origin` -> `nguon-refs.tsv` | do lai duoc |
| ref mirror | `for-each-ref refs/heads` tren `kho.git`, bo symref | do lai duoc |
| ref cay lam viec | `for-each-ref refs/heads` tren `cay-kho` | do lai duoc |
| do lech | `comm -3` giua hai TSV — so TAP HOP (ten+OID) | do lai duoc |
| phien ban cong cu | `<cong-cu> --version` -> `cong-cu.txt` | do lai duoc |

## Bao phu ref

| nguon | so ref |
|---|---:|
| may chu | **306** |
| mirror trong goi | **306** |
| cay lam viec | **306** |

Lech mirror: **0** dong. Lech cay lam viec: **0** dong.

## PHAN BO SOT — doc truoc khi tin bang tren

- Object den tu `kho.git` CUC BO, khong tai truc tiep tu may chu luc review. Remote
  `origin` cua `cay-kho` do script DAT LAI thanh URL that de qua phep kiem
  `--expected-repo`; nguon object giu o remote `mirror-cuc-bo`.
- `refs/heads/*` trong `cay-kho` do `update-ref` tao. Day la CHU Y, khong phai rac.
- Anh chup ref la moc `2026-09-07T22:43:15Z`. Kho co the da doi sau do; khong co mang trong sandbox
  nen KHONG doi chieu lai duoc voi may chu tai luc reviewer doc.
- Chi phu `refs/heads`. KHONG co anh chup tag hay namespace khac.
- Bang nay khong phu CI tren GitHub Actions.
