# BÀN GIAO — lớp cách ly gate (cgroup v2) và sổ nợ kèm theo

Đọc tệp này TRƯỚC khi làm gì. Nó là **bản chiếu**; nguồn có thẩm quyền vẫn là
lịch sử git, `ops/NO_KY_THUAT.md`, và comment trên PR.

Viết lúc PR sổ-nợ vòng 3 (`ops/so-no-vong-3`) **chưa merge**; mọi thứ khác đã ở
trên master.

## 0. Việc còn lại, đúng một câu

Merge PR sổ-nợ vòng 3, rồi xử sổ nợ `ops/NO_KY_THUAT.md` (còn 6 mục) — **không
mở vòng vá thứ n cho lớp cách ly tiến trình**, xem §4.

## 1. Đã land gì (đừng làm lại)

| PR | nội dung | commit trên master |
|---|---|---|
| #141 | **cgroup v2** thay vòng quét cây; fail-close khi dọn không trọn vẹn | `a70f481` |
| #154 | chặn tín hiệu **TRƯỚC** khi cắm handler; đóng khe `rc=1` + rò cgroup | `5f6eb92` |
| #152 | (đóng, gộp vào #154) | — |

Lớp cách ly hiện tại: **Linux → cgroup v2 `cgroup.kill`** · **Windows → Job
Object** · **macOS/FreeBSD → quét cây** (lỗ "đẻ trong lúc dọn" CÒN NGUYÊN, được
khai thẳng trong mã, đừng lặng lẽ bỏ dòng khai ấy).

## 2. Đường đi công cụ — đọc trước, tiết kiệm cả giờ

- **Mở phiên là chạy `doctor` trước mọi việc khác** (CLAUDE.md nay đòi thế).
  `codex` thường CHƯA cài: `npm install -g @openai/codex` rồi
  `python .claude/dev/launcher.py chuan-bi`, kiểm bằng `codex login status`.
- **`codex` BẮT BUỘC ở phiên remote và mặc định — thiếu là `doctor` THOÁT 12.**
  Bảng `CONG_CU` ghi `{"ten": "codex", "bat_buoc": {"mac_dinh": True,
  "remote": True, "ci": False}}` (`launcher.py:1604-1607`) và phép giải hạng
  đọc `GITHUB_ACTIONS`/`CI` → `bb["ci"]`, `CLAUDE_CODE_REMOTE` → `bb["remote"]`,
  còn lại → `bb["mac_dinh"]` (`launcher.py:1766-1780`). Nên: **chỉ CI** mới hạ
  `codex` xuống tuỳ chọn (in `khong codex`, thoát 0); phiên remote/mặc định in
  `THIEU codex` và **thoát 12**. Bản trước của tệp này viết ngược lại — mục 7 sổ
  nợ ngay trong PR ấy nói đúng, còn dòng bàn giao thì sai.
  **Đo lại, không suy luận** (phiên này `CLAUDE_CODE_REMOTE=true` ⇒ hạng
  `remote`): dựng một `PATH` chỉ thiếu mỗi `codex` rồi chạy `doctor --json`
  ⇒ **thoát 12**, `ok=False`, `thieu_bat_buoc=['codex']`. Muốn tự kiểm:

  ```
  S=$(mktemp -d); for d in ${PATH//:/ }; do for f in "$d"/*; do
    b=$(basename "$f"); [ "$b" = codex ] && continue
    [ -e "$S/$b" ] || ln -s "$f" "$S/$b" 2>/dev/null; done; done
  PATH="$S" python .claude/dev/launcher.py doctor --json; echo "thoat=$?"
  ```
- **Nhưng đừng đọc `doctor` thoát 0 thành "đủ đồ" theo chiều kia**: mã thoát chỉ
  đếm CÓ MẶT. `KHA DUNG` mới đếm DÙNG ĐƯỢC, và `doctor` in thẳng
  `CHUA CHUNG MINH KHA DUNG (co mat, chua ai goi that)` — muốn bằng chứng thật
  thì chạy lại với `--kiem-song`.
- **Hook phiên có thể KHÔNG chạy lần nào**: phiên remote gắn kho GIỮA phiên thì
  `CLAUDE_PROJECT_DIR` không được đặt, lệnh hook giải ra `/.claude/hooks/...` và
  **vắng mặt lặng lẽ**. `doctor` mục `hook-phien` so BĂM tệp, tức đo "tệp có mới
  không" chứ KHÔNG đo "hook đã chạy chưa".
- `gh` KHÔNG có và kho cố ý không dùng. GitHub đi qua **MCP JSON-RPC** tới
  `https://api.githubcopilot.com/mcp/` với `GITHUB_PAT`, dùng **`urllib`** —
  KHÔNG `curl` (curl bị proxy chặn 403, urllib cùng host trả 200).
  Endpoint này **chập chờn**: gặp 503/404 thì thử lại vài lần rồi mới kết luận.
  `REST /repos/**` luôn 403 — chính sách theo ĐƯỜNG DẪN, không theo danh tính.

## 3. Chạy tại chỗ

Chép **cả phần bỏ qua**, đừng rút về mẫu số chung — bộ chạy cố ý tách
`qua`/`bo qua`/`hong` ra, và mục 4 sổ nợ vừa đóng CHÍNH VÌ lỗi nuốt phần ấy:

```
python .claude/dev/gate_lifecycle_test.py
#   26/26 ca (qua 26, bo qua 0, hong 0)          [máy cấp được cgroup]
TL_GATE_TAT_CGROUP=1 python .claude/dev/gate_lifecycle_test.py
#   26/26 ca (qua 24, bo qua 2, hong 0)          (giả lập macOS — hai ca cgroup TỰ BỎ QUA)
python scripts/tl.py --selftest                  # 1697/1697
python .claude/dev/launcher_test.py
#   118/119 ca QUA (bo qua 1, hong 0) - KHONG DU
python .claude/dev/launcher_test.py --dot-bien
#   DOT BIEN: 94/94 dat  (1 khong do duoc tren nen nay)
python .claude/dev/packet_loop.py doctrine-scan --root .       # sạch
```

Hai dòng `26/26` KHÔNG cùng nghĩa: lượt sau **chưa đo gì về lớp cgroup**, hai ca
`case_gate_dat_ma_bo_lai_daemon_van_bi_don_va_khai` và
`case_tien_trinh_trong_cgroup_con_khong_duoc_bo_sot` tự bỏ qua. Bộ chạy in
`[cach-ly] CO CHE THAT SU : ...` trước dòng tổng — **đọc dòng ấy trước con số**.

`118/119` chỉ đúng khi **đã cài `codex`**; thiếu nó thì `t53_doctor_bao_du_khi_du`
đỏ tất định (`doctor` thoát 12, xem mục 2) ⇒ `117/119 ... hong 1`. Chữ ký ấy
TRÙNG với flake `t53` ở mục 7 sổ nợ — `command -v codex` trước khi kết luận.
Còn `- KHONG DU` ở đuôi là bộ chạy tự khai 1 ca bỏ qua (`t62` là fixture Windows),
không phải lời than — cũng như `(1 khong do duoc tren nen nay)` ở dòng đột biến.
**Chép cả cái đuôi ấy.** Rút `94/94` trần ra là lại giấu đúng thứ nó cố khai.

`tl selftest` cần `git config --global core.abbrev 7` như `ci.yml`; không ghim
thì `r218`/`r264` đỏ — **đó là môi trường, không phải hồi quy**.

## 4. Chỗ tôi CHƯA yên tâm — nói thẳng

- **Lớp cách ly đã qua NĂM vòng vá** (killpg → chụp một lần → subreaper → điều
  kiện lặng → cgroup → chặn tín hiệu sớm). Doctrine của kho: cùng hình dạng lặp
  ba lần thì hỏi *có nên làm việc này không*. Nếu vòng sáu ló ra, **dừng và hỏi
  người dùng** thay vì vá.
- **Khe "cố tình trèo ra" KHÔNG chặn được** bằng uỷ quyền cgroup không đặc quyền:
  quyền cần để chuyển VÀO chính là quyền cho phép trèo RA một tầng. Sổ nợ mục 1.
  Đã thử một bản PHÁT HIỆN và **đo thấy nó sai cả hai chiều** — đừng làm lại
  bản ấy mà không đọc mục 1 trước.
- **Mức review**: Codex HẾT QUOTA. Claude review Claude chỉ là
  `same_provider_approved` (§8 mục 3) — **KHÔNG đủ** cho PR đụng workflow/security.
  Phiên Claude cũng đã báo `seven_day: allowed_warning`.
- **Branch protection cưỡng chế up-to-date**: `behind` thì merge trả 405
  "Required status check `gate (ubuntu-latest)` is expected". Không có đường tắt
  — hoà master, chạy lại, chờ CI, rồi mới merge.

## 5. Bẫy đã trả giá TRONG đợt này — đừng lặp

- **Vá tệp bằng script mà tìm chuỗi từ ĐẦU TỆP**: `s.index(moc_ket)` không truyền
  vị trí bắt đầu → khớp một chỗ sớm hơn → `s[:i] + moi + s[j:]` **nhân bản** cả
  một vùng ~5 ca. Nó **không báo lỗi**, nó làm hỏng nội dung. Rồi bản "dọn trùng"
  cắt theo `dòng bắt đầu bằng "def "` lại **ghép đầu ca này vào thân ca kia** —
  và tổng `N/N` KHÔNG lộ ra vì `CASES` chỉ liệt kê tên. **Dùng ranh giới AST.**
- **Dựng nội dung dài bằng chuỗi nội tuyến trong `python3 -c "..."`**: shell nuốt
  phần trong dấu backtick (command substitution) → đăng lên PR một comment hỏng
  mà không hay. **Ghi ra TỆP rồi đọc tệp.**
- **Đặt probe sai chỗ rồi kết luận "reviewer sai"**: tôi chèn độ trễ SAU
  `atexit.register` nên không thấy rò cgroup, suýt bác một P1 đúng. Đặt đúng
  khoảng mới thấy.
- **Đọc giới hạn của phép đo MÌNH DỰNG thành thuộc tính của thứ được đo**: tôi
  cắt log bằng `tail -1` rồi kết luận "runner không in tên ca hỏng" — nó in sẵn.
- **Ghép số của hai lượt chạy vào một câu** (`thoát 12` + `ok=True`): hai thứ ấy
  bất khả cùng lượt. Giữ nguyên stdout của ĐÚNG lượt bất thường.
- **Bảng số theo giây là hệ quả, không phải nguyên nhân**: mốc thời gian không
  đơn điệu vì preflight dài ngắn tuỳ máy/tải. Neo phép đo vào **PHA**.

## 6. Sổ nợ — `ops/NO_KY_THUAT.md`

Còn **6 mục** (mục 4 đã đóng: nhánh khác sửa headline `launcher_test`, đi xa hơn
điều kiện đặt ra). Mỗi mục ghi *đo được gì / vì sao chưa làm / điều kiện coi là
xong*. Đọc mục 1 và mục 7 trước — hai mục ấy có nhiều người dễ vấp lại nhất.

Manh mối nóng nhất: **mục 7** — `doctor` chớp (thoát 12 rồi 0). Cơ chế đã dựng
lại được bằng shim: một lượt `--version` hết hạn ⇒ bị đếm là thiếu. Lần chớp tới
chỉ cần chạy `doctor --json` và **giữ nguyên stdout** là đóng được nửa đường.

## 7. Việc của người dùng, đừng làm hộ

Xoá nhánh: container **không xoá được ref** (`git push --delete` → 403) và
`ops-don-ref.yml` cố ý bảo vệ `ops/**`. Người dùng chạy `.\scripts\don-nhanh.cmd -Xoa`.

Danh sách chép cứng vào đây **hết hạn ngay khi người dùng chạy lệnh ấy** — bản
trước còn liệt `ops/gate-lifecycle` sau khi nó đã bị xoá. **Đo, đừng chép**:

```
git ls-remote --heads origin 'refs/heads/ops/*'
```

Đo lúc viết tệp này (`ops/gate-lifecycle` đã KHÔNG còn): các nhánh của loạt việc
này còn chờ xoá là `ops/no-ky-thuat-muc6` và `ops/tin-hieu-chan-som`, cộng
`ops/so-no-vong-3` sau khi PR #162 merge.
