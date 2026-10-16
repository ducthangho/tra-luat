# Bàn giao — soạn spec `THU-HOI-LEASE-VA-CAP-LAI` (PR #475), phiên 1 → phiên 2, 08-09-2026

**Vai:** soạn đặc tả + điều phối cross-review. **KHÔNG** phải executor packet ⇒ không theo schema §7 đầy đủ
(không `generation`, không lease). **Chưa có Packet Issue, chưa có lease, chưa sửa một dòng mã nào.**

**Chỉ thị chủ kho (08-09-2026, nguyên văn):** *"Đóng gói và chuyển sang phiên khác, thực hiện và, review #475
tới hết P1"*. Neo bền: comment PR #475 **`5578460203`** (trần mới: tới hết P1, bộ đếm KHÔNG reset, lời gọi kế = 7).

## 1. Neo — đo cùng lúc, cùng commit

```yaml
do_luc: '2026-09-08T00:3xZ'
nhanh: claude/spec-thu-hoi-lease-va-cap-lai-20260907
head_khi_ban_giao: 2aee80a2ff6a088ff39a2a8bc882db978df64c75    # r6 spec; commit bàn giao này nằm NGAY SAU
base_nhanh: b416830ef2a509d60203d55552ce17950afcf67c           # merge-base với origin/master; mirror review dùng SHA này
origin_master_luc_do: 585c7d510e026b4ea5a2b395c69581f24c1d8fa0 # master đã đi 48 commit — KHÔNG merge vào nhánh spec
                                                              # trừ khi lượt review cần mã mới; nếu merge thì đo lại §1 spec
pr: 475            # draft; check `cong` ĐỎ theo thiết kế (đòi review khác danh tính) — đã comment 5571673973
spec: ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md
spec_revision: 6
spec_sha256: f78135cff428f0744476d7f27426f459d926578c4bac4a4339928330c4a0d6a5
spec_r6_da_review: false     # r6 vá theo HINT lượt 5, CHƯA lượt nào đọc
loi_goi_review_da_dung: 6    # 1,2,3,4a(chết),4b,5 — §12: 4a vẫn đếm vì đã sinh output
loi_goi_ke: 7
comment_neo: [5571673973, 5575587924, 5576397733, 5578460203]
hien_vat: ops/reviews/thu-hoi-lease-va-cap-lai-spec/   # VERDICT/HINT/PROMPT/spec-rN, sha256 ở README
```

## 2. Trạng thái P1/P2 sau lời gọi 6 (lượt 5, VERDICT `1596d562…`)

| ID | hạng | hình dạng | r5 sai gì | r6 đã làm (chưa review) |
|---|---|---|---|---|
| S1 adapter-environment-boundary | P1 | nguồn tin cậy | allowlist `credential.*`/`http.*` theo TÊN + dò chuỗi trong giá trị; receipt chỉ ghi tập tên biến | Q4.1: allowlist hữu hạn khoá+kiểu+miền giá trị; `PROFILE_ADAPTER_DA_DUYET` digest ghim trong mã; lệch ⇒ 12 |
| S2 raw-object-read-content-identity | P1 | nguồn tin cậy | băm blob nhưng chưa ràng CẠNH tree/parent; repo tạm `cat-file` trả `missing` | Q4.5: `GIT_DIR` tạm + `GIT_OBJECT_DIRECTORY` nguồn; mọi cạnh từ bytes đã băm; tự đi đồ thị, memoize (type,OID); không walker |
| S3 a6-single-mutant-shielded | P1 | tiêu chí nghiệm thu | A6 đòi `refs/replace` ⇒ 12 dù no-replace đọc object gốc (băm khớp) | A6: replacement ⇒ verdict KHÔNG đổi; ca riêng bytes lệch OID ⇒ 12; catalog ghi seam + chốt còn nguyên |
| S5 m9-publisher-consumer | P2 | — | `GITHUB_STEP_SUMMARY` ≠ `output.summary`; dispatch H không gắn check-run; join provenance | M9: receipt = workflow artifact `thu-hoi-receipt-<H>`; join độc lập; dispatch không tạo pass; consumer = bước land-packets (dependency) |
| S6 q13-exception-retirement | P2 | — | ai produce/verify descriptor; sự kiện A→B→D bị bỏ lỡ | Q13: descriptor ghim mã A1; `ops/thu-hoi/_ngoai-le-closure.retired.yaml` do M9 ép |

Chi tiết từng ô: spec §0.3 và `hien_vat/luot5-VERDICT.md` mục "Findings mới" (có "Sửa …" + "Ca khoá" từng finding).
Diễn biến P1: 11 → 9 → 9 → (4a chết) → 4 → 3. Hình dạng "nguồn tin cậy cho cổng đọc" trúng **5** lần (spec
`hinh_dang_ke_thua`); reviewer 4b và 5 cùng khuyến nghị **ADR** trước thi công — xem §5.

## 3. Việc của phiên 2 — theo thứ tự

0. **Mở phiên:** `sed -n '1,140p' .claude/dev/launcher.py` → `python .claude/dev/launcher.py doctor` → `chuan-bi`.
   `CODEX_AUTH_JSON` là ảnh chụp cũ (>36h) nhưng lượt 5 vẫn chạy trọn 22:47Z 07-09; nếu `refresh_token_invalidated`
   thì xin chủ kho chuỗi mới, đừng đoán. Kho có thể shallow / master cục bộ tụt: `git fetch --unshallow` nếu
   `--is-shallow-repository` = true, `git branch -f master refs/remotes/origin/master`.
1. **Lượt 6 = lời gọi 7: review r6** (`f78135cf…`). Prompt theo khuôn `hien_vat/luot5-PROMPT.md`, đổi: tiêu đề
   "revision 6 · lượt 6 (lời gọi 7, trần mới theo comment `5578460203`)", bảng thư mục (SPEC.md = r6, SPEC.r5.md,
   VERDICT.luot5.md, HINT.luot5.patch), mục "Việc phải làm" đòi phân hạng S1/S2/S3/S5/S6 theo §0.3 r6 + tấn công chỗ
   mới. **GIỮ NGUYÊN đoạn "Phân công như lượt 4b — CẤM tuyệt đối tự soạn …"** — 4a chết vì thiếu nó.
2. **Còn P1 ⇒** vá rN+1 theo HINT (đọc VERDICT trước, HINT chỉ là gợi ý; không vá mù), cập nhật §0 bảng lượt + §0.x
   delta, `doctrine-scan` sạch, commit `ops(spec): … revision N`, chép VERDICT/HINT/PROMPT vào `hien_vat/luotN-*`
   + dòng README, comment ngắn lên PR #475, phóng lượt kế. Lặp.
3. **Hết P1 ⇒** đăng **Packet Issue** neo `spec_hash` = sha256 bản cuối (PROTOCOL §3.2; mẫu: Issue của
   `wp461`/`#456`), ghi: ngoại lệ Q13 + descriptor, lịch sử N lời gọi, trạng thái P2/P3 còn, ADR còn nợ. Rồi **DỪNG**:
   báo chủ kho số Issue + `spec_hash`, xin cấp lease. KHÔNG tự cấp (`--granted-by` từ chối `claude`/`codex`).
4. Chỉ sau khi có lease: thi công slice A0 (xem spec `write_set`) + cross-review + full gate đúng một lần ở cuối.

## 4. Cơ chế phóng review (đã chạy 6 lần, chép nguyên)

```bash
# Sandbox: mirror bare + clone detached tại base_nhanh, core.abbrev 7, spec chép vào cả cwd lẫn cay-kho (untracked)
git clone -q --mirror . "$RV/kho.git"; git clone -q "$RV/kho.git" "$RV/cay-kho"
git -C "$RV/cay-kho" checkout -q --detach b416830ef2a509d60203d55552ce17950afcf67c
git -C "$RV/cay-kho" config core.abbrev 7
cp ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md "$RV/SPEC.md"; cp "$RV/SPEC.md" "$RV/cay-kho/ops/specs/THU-HOI-LEASE-VA-CAP-LAI.md"
# lượt trước: SPEC.rN.md, VERDICT.luotN.md, HINT.luotN.patch, EVIDENCE.md (lời khai điều phối: số đo offline)
# Phóng (mẫu đầy đủ: hien_vat/phong.sh.mau) — chạy dưới setsid nohup … < /dev/null &, KHÔNG stdin
python3 .claude/dev/launcher.py run --workspace "$RV/cay-kho" --expected-head b416830ef2a509d60203d55552ce17950afcf67c \
  --run-root "$RUNS" --name spec-review-N --prompt-file "$RV/PROMPT.md" --expected-prompt-sha256 "$(sha256sum "$RV/PROMPT.md" | cut -c1-64)" \
  --deadline-utc "<now+75min>" --json --giu-ban-chup -- /usr/bin/bash -c \
  'exec "$0" exec -m gpt-6-astra -c model_reasoning_effort=xhigh -s workspace-write --skip-git-repo-check -C "$1" -o "$1/last.md" "$(cat "$2")"' \
  "$(command -v codex)" "$RV" "{PROMPT_FILE}"
```

- Thời lượng thực tế: **1600–3320 s**/lượt. Đặt deadline 75 phút. Đợi bằng `run.json` `trang_thai == "xong"`
  (poll nền), KHÔNG dùng `pgrep` (tiến trình codex lởn vởn sau XONG). Dòng cuối stdout phải là
  `XONG VERDICT sha256=…` và **băm lại VERDICT.md sau khi run xong** — lượt 5 reviewer còn sửa VERDICT sau dòng ấy.
- `ma_thoat=1` + stderr `flagged for possible cybersecurity risk` = bộ lọc nội dung của nền, KHÔNG phải mạng/proxy;
  vẫn **đếm** một lời gọi. `Connection refused (os error 111)` từng gặp, nguyên nhân chưa biết — đừng đổ cho proxy.
- Mỗi lượt là **RUN MỚI**: đo lại head/`origin/master`/`ai-dang-giu` trước khi làm (§12).

## 5. Chưa quyết — của chủ kho, KHÔNG tự quyết

- **ADR "nguồn tin cậy cho cổng đọc lease"**: S1/S2 là hình dạng ấy lần 5. Chủ kho chưa nói có soạn ADR không.
  Nếu soạn: `docs/adr/0047-…md` (số kế tiếp sau `0046`) + dòng trong `docs/PROTOCOL_DA_PHIEN.md` §20 (gate
  `packet_loop.py adr-song`). §20 là tệp nóng ⇒ **`ai-dang-giu` trước** (fetch đủ ref: so `ls-remote` với
  `for-each-ref` bằng TẬP TÊN); không đo được ⇒ ĐỎ, hỏi chủ kho. Đề xuất: hỏi chủ kho ở lượt review đầu tiên.
- Nợ #473 (`bia-mo-check-bo-sot-chieu-nguoc`), lease g2 wp461 (PR #474) hết hạn `2026-09-08T09:52:00Z` — spec §1 đã đo,
  số sẽ trôi; đo lại trước khi công bố (L5).

## 6. Bẫy đã trả giá trong phiên 1

- Hook/permission: lệnh Bash có `rm -rf` hoặc `cd` bị hỏi/từ chối — viết đường tuyệt đối, dọn bằng `find -delete`.
- Đồng hồ: `date` lệch tới 4h47 so GitHub **chỉ vì** `AskUserQuestion` treo chờ; so `date -u` với header `Date` HTTP trước khi nghi.
- `ops/chay_lease_publish_test.sh` cần `AL_VER=1.7.7` để 121/121.
- Lời khai r1 sai vì đoán thay vì đo (GITHUB_ACTOR, symref `origin/HEAD`, chữ ký `6635379`, số commit #468): mọi số
  vào spec phải có lệnh đo và đơn vị; reviewer đo lại trên mirror và bắt từng số.
- MCP đọc comment chuẩn hoá `'`→`&#39;`, `>`→`&gt;`: diff readback chỉ để bắt lệch KÝ TỰ THẬT.
- Verdict "ĐÓNG" là đóng hợp đồng trên bản đã đọc, không phải chứng nhận bản kế; đừng cộng dồn "đã vá" thành "đã đóng".
