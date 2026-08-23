# HANDOFF — `TAT-DINH-VOID-HA-TANG` (#262), **generation 2**, `blocked`

## 0. Khối bàn giao schema-v1 (protocol §7)

```yaml
schema_version: 1
packet_id: TAT-DINH-VOID-HA-TANG        # Issue #262
generation: 2
spec_hash: dc4bc6226dbdfe3b5a3dc86cb990cc2c85574456a30f3c65f6d7492bd015d827   # r4
provider: claude
role: executor
session_id: session_01CX1JhRkNDDuNirBzms5zUr
base_sha: 05de1ab81c235235b971a6fb8d8ae1fb226295d5
head_sha: 22f1d15d5e0563981b1a2b5bcdfc8e9cdcfaebfb
status: blocked
blocked_by: 'same_failure — CỔNG MÁY tự bắn, không phải người thi công tự khai'
summary: >-
  Stable Slice đứng vững về KIẾN TRÚC: bỏ M3/M4 đưa `void-attempt` về khớp master từng
  dòng (20/20), giữ M1/M2/M8 làm bảo vệ mới. Nhưng ca canh việc BỎ (N11) hỏng HAI lần
  liên tiếp theo hai kiểu khác nhau, và một "bản vá" của tôi là XOÁ nghĩa vụ chứ không
  thoả nó. Cổng `same_failure` bắn khi 4 finding-id lặp lần thứ hai.
changed_paths:
  - .claude/dev/packet_loop.py
  - .claude/dev/packet_loop_test.py
  - ops/KE_HOACH_THI_CONG_CLAUDE_CODEX.md
tests:
  - name: packet_loop_test.py
    status: passed        # 231/231; nền master 225/225 ⇒ 6 ca mới, 0 hồi quy
    evidence: 'ops/handoff/tat-dinh-void-ha-tang-exec-2-claude-20260823-handoff.md#3'
  - name: 'gate (ubuntu-latest) + gate (windows-latest) trên 7c54c9f'
    status: passed
    evidence: 'https://github.com/ducthangho/tra-luat/actions/runs/32623200062'
  - name: 'đột biến — bán kính nổ đo trên TOÀN BỘ 231 ca'
    status: passed        # 5 đột biến, mỗi cái giết đúng 1
    evidence: 'https://github.com/ducthangho/tra-luat/pull/274#issuecomment-5384756941'
  - name: 'lease_publish_test.py'
    status: passed        # 87/87, chạy trong worktree của chính kho
    evidence: 'ops/handoff/tat-dinh-void-ha-tang-exec-2-claude-20260823-handoff.md#3'
test_selection:
  gate_tier: null
  selector_policy_sha: null
  tested_sha: 22f1d15d5e0563981b1a2b5bcdfc8e9cdcfaebfb
  selected_groups: []
  full_fallback_reason: 'chạy toàn bộ gate, không chọn lọc'
reviews:
  - round: 1
    provider: codex
    reviewed_sha: 7c54c9fb1c75639ab4c647c278629cf7540bf03f
    verdict: changes_requested
    findings: 8
    evidence: 'https://github.com/ducthangho/tra-luat/pull/274#issuecomment-5384756941'
  - round: 2
    provider: codex
    reviewed_sha: 22f1d15d5e0563981b1a2b5bcdfc8e9cdcfaebfb
    verdict: changes_requested
    findings: 10
    evidence: 'https://github.com/ducthangho/tra-luat/pull/274#issuecomment-5384840611'
failure:
  fingerprint: 'n11-canh-viec-BO-hong-hai-lan-hai-kieu'
  loai: 'ca nghiệm thu không đo được thứ nó khai; và một bản vá XOÁ nghĩa vụ'
  co_phai_hinh_dang_cua_gen1: false
remaining_work:
  - 'P1a `n11-chi-kiem-help-khong-kiem-parser` — CÒN MỞ. Đã có bản vá ĐÚNG ở §4.1.'
  - 'P1b `mutant-siet-tuoi-giet-ba-muoi-bay-ca` — CÒN MỞ. Đã có bản vá ĐÚNG ở §4.2.'
  - 'P2 `anh-doctor-tu-khai-khong-co-nguon-goc` — CỐ Ý hoãn, cả hai vòng đồng thuận.'
  - '`packet_loop_test.py` KHÔNG có cổng CI nào — xem §5.'
  - 'Cổng `same_failure` đếm SLUG, không đếm Ý ĐỊNH — xem §6.'
```

## 1. Cái ĐÃ đứng vững, đừng làm lại

| | bằng chứng |
|---|---|
| bỏ M3/M4 **không** lùi khỏi master | thân `cmd_void_attempt` lọc chú thích khớp master **20/20 dòng mã**, 0 khác, 0 thiếu |
| master **chưa từng** có cổng bằng chứng ở đó | `grep -c "bang_chung\|evidence"` trên `cmd_void_attempt` của master ⇒ **0** |
| M1/M2 là bảo vệ MỚI | `begin-attempt` nay đòi ảnh `doctor` sạch/tươi/đúng nền; ĐÃ DÙNG THẬT để mở cả hai attempt |
| 5 đột biến, bán kính nổ đo trên **toàn bộ** 231 ca | mỗi cái giết đúng **1** |
| ngân sách | **220/220** dòng · 3/3 tệp — vượt 7 sau vòng 1 ⇒ **NÉN**, không nới |

Reviewer vòng 2 xác nhận 4/8 finding vòng 1 **ĐÃ VÁ THẬT** và **rút lại** một vế sai của chính họ.

## 2. Vì sao packet dừng — cổng MÁY bắn, không ai tự khai

```
record-review vòng 2 ⇒ blocked_same_failure
  finding_ids lặp lần thứ 2 (trần 2):
    n11-chi-kiem-help-khong-kiem-parser
    mutant-siet-tuoi-giet-ba-muoi-bay-ca
    anh-doctor-tu-khai-khong-co-nguon-goc
    dem-commit-origin-master-troi
```

`attempts_used` là **2/3** — còn một lượt, nhưng không với tới được từ `blocked`. Đúng thiết kế: chốt bắn theo **hình dạng lỗi lặp**, không theo số lượt.

## 3. Số của head `22f1d15` (chép từ máy, không gõ tay)

```
packet_loop_test    231/231 ĐẠT · 58 đột biến · 78 lớp lách · 35 ca bắt-oan
                    (33 ca riêng biệt) · 3 đột biến PHỐI HỢP · 0 ngoại lệ AC 18
lease_publish_test  87/87 đạt, bỏ qua 0
ruff --select F     nhánh 3 == master 3  ⇒ DELTA 0
doctrine-scan       rc=0 (7 tệp)      adr-song  rc=0 (46/46)
write set           +220 / -2 · churn 222 · net 218 · 3 tệp
tree OID            405bd03e229028c7b25781a56a393400683c4f60
cổng CI gọi packet_loop_test   0
```

## 4. HAI BẢN VÁ ĐÃ THIẾT KẾ XONG — phiên sau áp thẳng, đừng thiết kế lại

### 4.1 P1a — đảo danh sách CẤM thành danh sách CHO PHÉP

**Phản chứng đã CHẠY** (cả hai lượt, trên bản sao tạm):

| đòn | kết quả |
|---|---|
| `--bang-chung` + `help=argparse.SUPPRESS` | `--help` không in cờ · `void-attempt … --bang-chung X` ⇒ **rc=0** · suite **231/231 xanh** |
| alias `--evidence-file` + `SUPPRESS` (vòng 2) | parser nhận · suite **0 ca chết** |

Bản vá vòng 1 của tôi liệt kê **bốn chính tả**. Nguyên văn bài học đã có trong `CLAUDE.md`:
*"Danh sách CẤM không bao giờ đủ — phải đảo thành danh sách CHO PHÉP"*, và
*"distinguishes spelling, not authority"*.

**Thay chiều BỀ MẶT của `case_void_giu_dung_hanh_vi_master` bằng:**

```python
    # Danh sách CHO PHÉP, không phải danh sách cấm: alias/SUPPRESS/tên chưa ai nghĩ ra
    # đều ĐỎ. Vòng 1 khoá `--help`, vòng 2 khoá bốn chính tả — cả hai đều bị lách.
    import importlib.util as _iu
    _s = _iu.spec_from_file_location("_n11", c.script); _m = _iu.module_from_spec(_s)
    _s.loader.exec_module(_m)
    _sub = next(a for a in _m.build_parser()._actions
                if isinstance(a, argparse._SubParsersAction))
    co = {t for a in _sub.choices["void-attempt"]._actions for t in a.option_strings}
    assert co == {"-h", "--help", "--packet", "--reason"}, f"cờ LẠ trong parser: {co}"
```

Cần `import argparse` ở đầu `packet_loop_test.py` (kiểm trước, đừng giả định).
`build_parser()` ở `packet_loop.py:1460`; tệp có `if __name__ == "__main__":` nên nạp module an toàn.

**Đột biến khoá nó** — giữ `mt_them_lai_co_M3_bi_SUPPRESS` và **thêm** bản alias:

```python
    "mt_them_lai_alias_M3": (
        '    q.add_argument("--reason", required=True, help=f"một trong {LY_DO_VOID}")\n',
        '    q.add_argument("--reason", required=True, help=f"một trong {LY_DO_VOID}")\n'
        '    q.add_argument("--evidence-file", default=None, help=argparse.SUPPRESS)\n',
        ["void_giu_dung_hanh_vi_master"],
    ),
```

Đo bán kính trên **toàn bộ** 231 ca, không tin bộ tự-chứng-minh (xem §6).

### 4.2 P1b — trả lại nghĩa vụ M6/N2, kèm SỐ THẬT

Tôi giải quyết một bán kính nổ sai bằng cách **xoá acceptance**. Nguyên văn reviewer:
*"Xóa mutant giải quyết bán kính sai bằng cách bỏ acceptance."*

Nhưng **bán kính 1 là BẤT KHẢ** cho N2: nó khẳng định `rc=0`, nên mọi đột biến siết cổng
môi trường tất yếu giết **mọi** ca gọi `begin-attempt`. Đo: **37/231**, và N1 **KHÔNG** nằm
trong đó (`thieu_bat_buoc` kiểm TRƯỚC tuổi) — reviewer đã rút lại vế ngược lại.

Cái sai của vòng 1 **không phải con số mà là khai 1 trong khi chưa đo**. Trả đột biến lại,
kèm số đúng:

```python
    # N2 là ca chiều BẮT OAN: khẳng định `rc=0`, nên CHỈ đột biến SIẾT giết nổi — và mọi
    # đột biến siết cổng ấy tất yếu giết cả 36 ca khác gọi `begin-attempt`. ĐO: **37/231**,
    # N1 KHÔNG nằm trong đó. Bán kính 1 là BẤT KHẢ cho ca chiều tha, không phải khuyết tật.
    # Vòng 1 khai "đúng 1" mà chưa đo — ĐÓ mới là lỗi. `phai_chet` chỉ nói "phải chết",
    # không nói "chỉ mình nó chết".
    "mt_siet_nguong_tuoi_ve_am_mot": (
        "NGUONG_TUOI_BANG_CHUNG_GIAY = 3600\n",
        "NGUONG_TUOI_BANG_CHUNG_GIAY = -1   # đột biến SIẾT\n",
        ["mt_sach_thi_van_mo_duoc_luot"],
    ),
```

**Ngân sách đang 220/220 — phiên sau phải NÉN, không nới.** Chỗ nén được đã khảo: khối
chú thích đột biến · docstring N11 · chú thích `cmd_void_attempt` trong `packet_loop.py`.
Gen 1 nới hai lần; gen 2 chưa lần nào — đừng phá.

## 5. `packet_loop_test.py` KHÔNG CÓ CỔNG CI NÀO — tự tìm ra, ngoài mọi vòng review

```
grep -rn "packet_loop" .github/   ⇒  0 dòng
```

Mọi dấu tick xanh trên PR #266/#274 đo những cổng **khác** của kho. Con số `231/231` chỉ
đứng trên các lượt chạy TAY, tất cả trên **cùng một nền Linux**. Hệ quả: **`N10′`
(`case_luong_canonical_chay_that`) chưa từng được đo** — trên Linux nó bỏ qua có in lý do,
trên Windows không ai gọi nó.

Bản vá đề xuất (một step cạnh `lease-publish selftest`, cả hai nền):

```yaml
      - name: packet-loop selftest
        run: python .claude/dev/packet_loop_test.py
```

**ĐO THỜI GIAN TRÊN WINDOWS TRƯỚC.** 58 đột biến, mỗi cái sinh một lượt chạy con; nhân hệ
số Windows ×2 thì nó đâm thẳng vào bài toán phút Actions mà `r245` trong `ci.yml` đã phải cắt.

## 6. Cổng `same_failure` đếm SLUG, không đếm Ý ĐỊNH — finding cho packet kế nhiệm

Trong bốn slug làm cổng bắn, **hai** không phải "bản vá không trúng gốc":

| slug | thực chất |
|---|---|
| `anh-doctor-tu-khai-khong-co-nguon-goc` | **CỐ Ý hoãn**, cả hai vòng đồng thuận đưa sang packet kế nhiệm. Reviewer viết thẳng *"phải sang packet kế nhiệm"* |
| `dem-commit-origin-master-troi` | khuyết tật của tệp EVIDENCE, **ngoài write set** thi công |

Cổng không phân biệt được *hoãn có thoả thuận* với *vá trượt*, cũng không phân biệt lỗi
**trong write set** với lỗi **trong hồ sơ**. Cùng họ *"phân biệt CÁCH VIẾT, không phân biệt
THẨM QUYỀN"*, đổi đối tượng.

**KHÔNG được vá điều này trong packet đang bị chính nó chặn** — `packet_loop.py` nằm trong
write set, và sửa cổng vừa dừng mình là tự cấp lối thoát. Ghi vào đây để packet kế nhiệm nhận.

Bộ tự-chứng-minh cũng có cùng lớp khuyết tật, và nó là thứ đã che P1b: nó chỉ chạy
`phai_chet` + 3 đối chứng **KHÁC HỌ**, nên **mù với bán kính nổ TRONG CÙNG HỌ**. Reviewer
thấy vì chạy mutant trên cả 231 ca. Đến khi bộ ấy được sửa, **mọi đột biến mới phải đo thủ
công trên toàn suite**.

## 7. Hình dạng lỗi — đếm cho đúng trước khi ai đó nới trần

Gen 1 dừng vì **một** hình dạng lặp ba lần: *tin một trường mà bên bị đo đặt được*.
Gen 2 **không** lặp hình dạng ấy. Hai P1 của gen 2 là hai lỗi **khác nhau**:

| | lỗi | cách chữa ĐÃ có |
|---|---|---|
| P1a | danh sách CẤM thay vì danh sách CHO PHÉP | đảo chiều chốt (§4.1) — **đổi KIỂU**, không mở rộng |
| P1b | xoá nghĩa vụ thay vì thoả nó | trả nghĩa vụ + số đo thật (§4.2) |

Nhưng N11 đã hỏng **hai lần liên tiếp**, và cả hai đều là *"chốt của tôi không phủ hết
không gian"*. Nếu bản vá §4.1 lại hỏng thì đó là lần thứ **BA** của hình dạng ấy ⇒ §12 cấm
vá lần thứ tư, và câu hỏi đúng khi ấy là *"N11 có phải cách đúng để canh việc BỎ không"*,
không phải *"vá thế nào"*.

## 8. Việc của phiên sau — theo thứ tự

1. **Đọc `ops/specs/TAT-DINH-VOID-HA-TANG-r4.md`** (`dc4bc622…`) và kiểm băm TRƯỚC khi đọc nội dung.
2. Xin **Issue + lease MỚI** từ người giữ kho. Gen 2 đã `blocked`; §12 cấm hồi sinh.
   **KHÔNG tự chọn một dòng trong bảng packet rồi bắt tay làm.**
3. Áp §4.1 và §4.2. Nén cho vừa **220** dòng. Đo bán kính đột biến trên **toàn bộ** suite.
4. Đừng làm lại §1 — nó đã đứng vững qua hai vòng.
5. Nợ để riêng, **Issue riêng, đừng gộp**: §5 (cổng CI) · §6 (cổng `same_failure` + bộ
   tự-chứng-minh) · `anh-doctor-tu-khai-khong-co-nguon-goc` (xác thực nguồn gốc launcher).

---
_Generated by [Claude Code](https://claude.ai/code)_
