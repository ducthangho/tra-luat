# VBHN cấp Bộ — year/name guard (v1.17.18)

Nguồn: log xử lý "lô 33 đổi tên" ngày 2026-06-21.

## Vấn đề

Nhóm E không phải rác thuần. Các văn bản như `05/VBHN-BGDĐT`, `09/VBHN-BYT`, `8/VBHN-BNV`,
`1233/VBHN-BNG`, `2279/VBHN-BLĐTBXH` là VBHN cấp Bộ/cơ quan khác VPQH. Chúng vẫn là văn bản
quy phạm pháp luật và vẫn cần năm ban hành trong metadata/tên chuẩn.

Rủi ro cũ:

- parser chỉ nhận tốt VBHN-VPQH, làm sót hoặc parse sai số hiệu cấp Bộ;
- hygiene dễ gom cụm theo số hiệu trần rồi đề xuất quarantine nhầm;
- tên kiểu `09-VBHN-BYT` thiếu năm/chủ đề không đủ để chốt canonical;
- sidecar `.docx/.pdf` cấp Bộ có thể là file gốc hợp lệ, cần verify nội dung trước khi move.

## Quy tắc mới

1. Nhận diện VBHN cấp Bộ bằng số hiệu dạng:

```text
NN/VBHN-<COQUAN>
NN-NN/VBHN-<COQUAN>
NNNN/VBHN-<COQUAN>
```

Ví dụ: `09/VBHN-BYT`, `05/VBHN-BGDĐT`, `161/1233/VBHN-BNG`.

2. Metadata phải có năm:

```text
issue_year != null
```

Nếu thiếu, `hygiene scan`/`vbhn-normalize` gắn `VBHN_MINISTRY_MISSING_YEAR` và chỉ đề xuất
`BACKFILL_ISSUE_YEAR_REQUIRED`. Không rename trước khi verify dòng ngày ban hành.

3. Tên chuẩn phải có năm:

```text
VBHN_<so>-VBHN-<co_quan>_<year>_<ten_rut_gon>
```

Ví dụ:

```text
VBHN_09-VBHN-BYT_2024_<ten_rut_gon>
VBHN_05-VBHN-BGDDT_2023_<ten_rut_gon>
VBHN_2279-VBHN-BLDTBXH_2022_<ten_rut_gon>
```

4. Không quarantine theo số hiệu trần. Trước khi move/quarantine, phải verify:

- năm ban hành;
- chủ đề/tên văn bản;
- nội dung phần đầu văn bản;
- quan hệ file gốc sidecar với GDoc canonical;
- mapping NLM/registry nếu có.

## Tooling

```bash
python scripts/tl.py --config config.json vbhn-normalize --json
python scripts/tl.py --config config.json hygiene scan --json
python scripts/tl.py --config config.json hygiene plan "<so hieu hoac ten>" --json
```

Các lệnh trên chỉ report/dry-run. Thao tác ghi Drive/NLM/registry vẫn phải có xác nhận riêng.
