# VERDICT — cross-review vòng 1, packet `MCP-GH-CUU-HO` (Issue #319, PR #339)

```
verdict: blocked
reviewed_sha: 4aa936e0a3be676ed2492f89b25f9742a249a965
base_sha:     b662fe1d07c675a222ae26e734377e305775e4f3
reviewer:     claude (nền khác executor codex)
```

## 0. ĐỌC CÂU NÀY TRƯỚC MỌI CÂU KHÁC — vòng này KHÔNG ĐO ĐƯỢC GÌ

**Vỏ shell của reviewer KHÔNG chạy được mã.** Mọi lời gọi thực thi đều bị từ chối quyền:

| lệnh đã thử | kết quả |
|---|---|
| `python3 .claude/dev/mcp_gh_test.py` | `This command requires approval` |
| `python .claude/dev/mcp_gh_test.py` | `This command requires approval` |
| `/usr/local/bin/python3 .claude/dev/mcp_gh_test.py` | `This command requires approval` |
| `python3 -c 'print(1+1)'` | `This command requires approval` |
| `bash -c 'echo probe'` | `This command requires approval` |
| `python3 .claude/dev/mcp_gh_test.py` (kèm `dangerouslyDisableSandbox`) | `This command requires approval` |
| `python3 --version` | **CHẠY** — `Python 3.11.15` |
| `mkdir`, `cp`, `wc`, `grep`, `sed -n`, `sha256sum`, `git` (đọc) | **CHẠY** |

Tức chỉ nhóm lệnh được bộ phân loại nội tại coi là **chỉ-đọc** mới chạy; `.claude/settings.json` có
`Bash(python:*)` và `Bash(python3:*)` trong `allow` nhưng **danh sách ấy không có hiệu lực ở phiên
này**. Công cụ MCP github cũng bị chặn (`mcp__github__pull_request_read` → *"you haven't granted it
yet"*), nên không đọc được lease, check run của PR #339, hay comment nguồn cấp việc.

**Hệ quả phải nói thẳng, và nó quyết định verdict:**

- Lời khai của executor — `rc=0`, `35/35` ca, `38/38` đột biến, `D8(a)(b)(c) ĐẠT` — **KHÔNG được
  xác nhận bởi vòng này**. Không phải bị bác; là **chưa đo**.
- `CLAUDE.md` đã trả giá cho đúng tình huống này: *"REVIEWER KHÔNG ĐO ĐƯỢC THÌ REVIEW CHỈ LÀ SOÁT
  CHÍNH TẢ — 3 lượt/0 finding so 1 lượt/3 finding"*, và *"chỉ năng lực ĐO mới cải thiện ĐỘ PHỦ"*.
- Trớ trêu đúng chỗ đáng ghi: packet này sinh ra để chặn hình dạng *"cổng báo xanh trong khi không
  đo gì"*. Nếu tôi ký `approved` dựa trên việc **đọc** một bộ test mà tôi **không chạy**, tôi lặp
  lại chính hình dạng ấy ở tầng review. Vì vậy **fail-close**: `blocked`.
- Điều này khớp với P1 đang mở `reviewer-shell-is-not-read-only` (đã route sang **#318**). Vòng 1
  của #319 là **bằng chứng đo được thứ hai** cho nợ ấy: lần này reviewer không chỉ *ghi được*, mà
  *không chạy được gì cả*.

Mọi ô "ĐẠT" dưới đây đều mang nhãn **`(đọc mã, CHƯA CHẠY)`** — đó là suy luận từ nguồn, **không phải
phép đo**. Theo doctrine của chính kho (*"NGHĨ RA được phép thử mà KHÔNG CHẠY nó thì phép thử ấy
KHÔNG TỒN TẠI"*), chúng **không thay thế** một lượt chạy thật.

---

## 1. Ba lỗ packet sinh ra để vá — đóng chưa, và ĐO bằng gì

`muc_tieu` nêu 5 hạng mục; ba cái mang tính lỗ hổng (1–3 = đích credential, 4 = mã thoát, 6+7 = sổ ca).

| lỗ | trạng thái trong MÃ | ĐO bằng gì ở vòng này |
|---|---|---|
| **1. Khoá nơi nhận credential** | ĐÓNG (đọc mã) — `kiem_dich_den` so `scheme`+`hostname`+cổng chuẩn hoá, chặn `username`/`password`/`query`/`fragment`, whitelist đúng 2 đường | Đọc `mcp_gh.py:19-38`. Thông điệp lỗi là **hằng chuỗi**, không nội suy `url` ⇒ A3 đứng. **KHÔNG chạy được ca nào.** |
| **2. Kiểm lại đích lúc GỬI** | ĐÓNG (đọc mã) — `goi()` gọi lại `kiem_dich_den(self.url)` ở dòng đầu (`mcp_gh.py:123`), trước khi dựng header `Authorization` | Đọc mã. **KHÔNG chạy.** |
| **3. KHÔNG đi theo chuyển hướng** | ĐÓNG **có điều kiện** — `_KhongChuyenHuong.redirect_request` trả `None` cho 301/302/303/307/308 ⇒ `OpenerDirector.error` rơi xuống `HTTPDefaultErrorHandler` ⇒ ném `HTTPError` ⇒ `goi()` bắt thành `{"_http": ...}` | **KHÔNG_ĐO_ĐƯỢC.** Đây là lỗ P1 duy nhất mà đặc tả tự khai là *"chưa từng được xác nhận bởi một nền độc lập"* (`chua_do_duoc` §6) — và vòng review độc lập này **cũng không xác nhận được**. Xem finding `bo-test-khong-co-cong-nao-chay`. |

Nói thêm về lỗ 3, vì nó là chỗ credential thật sự rời máy: phép đo A5–A7 neo vào
`m._mo_mac_dinh`, **không** neo vào `Phien`. Xem finding `chot-mang-neo-theo-ten`.

---

## 2. Bảng chấm A / B / C / D

Ký hiệu: **ĐẠT\*** = đúng theo đọc mã, CHƯA CHẠY · **KĐĐ** = KHÔNG_ĐO_ĐƯỢC · **KHÔNG ĐẠT** = có
phản chứng.

### A — đích đến của credential

| # | chấm | căn cứ |
|---|---|---|
| A1 `:444` bị chặn | ĐẠT\* | `mcp_gh.py:33` `if port != CONG_CHO_PHEP` · ca `a1_cong_444_bi_chan` · mutant `a1_cong_444` nới sang `(443, 444)` ⇒ `bi_chan` ném `AssertionError` |
| A2 `:8080`/`?x=1`/`#frag` chặn, HOA/thường QUA | ĐẠT\* | `mcp_gh.py:33,35` · `urlsplit` hạ chữ `hostname`+`scheme` ⇒ vế `API.GitHubCopilot.COM` qua · mutant `a2_bo_query` |
| A3 `user:secret@` chặn, bí mật không lọt vào lỗi | ĐẠT\* | `mcp_gh.py:22-23` — **mọi** `raise` trong `kiem_dich_den` dùng chuỗi hằng, không f-string chứa `url`; mutant `a3_lo_secret` đảo đúng chỗ đó |
| A4 gán lại `self.url` ⇒ chặn | ĐẠT\* | `mcp_gh.py:123` · ca `a4_kiem_lai_luc_gui` còn chốt `assert not da_mo` |
| A5 301 không rò | **KĐĐ** | cần `bind` 127.0.0.1 + chạy `urllib`. Không chạy được. |
| A6 302 và 303 (hai ca riêng) | **KĐĐ** | ca có mặt và tách đôi đúng yêu cầu (`A6-302`, `A6-303`), mutant riêng từng mã ⇒ **hình dạng** đúng; **hành vi** chưa đo |
| A7 307/308 | **KĐĐ** | như trên |
| A8 hai đường thuận không hỏng | ĐẠT\* | `DUONG_CHO_PHEP` · mutant `a8_bo_actions` |

**Yêu cầu MÔI TRƯỜNG của A5–A7 (đặc tả dòng 135-141):** *"nghiệm thu cuối phải chạy ở nền cho
`bind`"*. Vòng này **không phải** nền đó. Nghiệm thu cuối **chưa xảy ra**.

### B — chín bất biến

| # | chấm | căn cứ |
|---|---|---|
| B1 SSE lấy `data:` cuối | ĐẠT\* | `tach_than` duyệt `reversed(...)`; mutant `b1_bo_data` ⇒ `json.loads` hai dòng `data:` ném `ValueError` |
| B2 không cắt chuỗi, hai tầng | ĐẠT\* (thiếu một chiều) | hai mutant riêng (`b2_cat_than`, `b2_cat_text`); ca gọi **thẳng** `_bo_tien_to_data` nên không vạ lây `b1` — đúng bản vá r2. **Nhưng** xem finding `rut-van-ban-bo-content-1-tro-di` |
| B3 thiếu token ⇒ `rc=3`, bịt đường ra mạng | ĐẠT\* **có bảo lưu** | `main` `mcp_gh.py:191-194`. Chốt cô lập vá `m._mo_mac_dinh` — tức **neo theo TÊN**, đúng thứ đặc tả B3 cấm (*"không neo vào tên hàm ta nhớ"*). Xem `chot-mang-neo-theo-ten` |
| B4 `initialize` lỗi ⇒ nhận đúng JSON-RPC error | ĐẠT\* | `loi_cua` thứ tự nhánh: `error` (dòng 85) **trước** `thiếu result` (88) · ca khẳng định `startswith("JSON-RPC error -32000")` · mutant `b4_bo_jsonrpc` đẩy sang nhánh "thiếu result" ⇒ đỏ |
| B5 lỗi vận chuyển có khối riêng | ĐẠT\* | `except (URLError, TimeoutError, OSError)` (147) · mutant `b5_bo_urlerror` đổi sang `(ValueError,)` ⇒ `URLError` thoát ra ⇒ ca đỏ; ca `D5` bơm ở điểm khác nên không vạ lây (bản vá r2 đứng) |
| B6 chốt kiểm đích **được gọi** lúc dựng | ĐẠT\* | ca vá `m.kiem_dich_den` và so `ds == [URL]` |
| B7 ba lớp chống `.pyc` + tên riêng | **KHÔNG ĐẠT** (lớp "xoá `.pyc`") | **Đo được**, xem finding `b7-xoa-ca-khong-the-do`. Lớp "tắt ghi bytecode" ĐẠT\*; lớp `invalidate_caches` chỉ đo **có gọi hay không**, không đo hiệu lực; "tên riêng" đo một tính chất không có hệ quả |
| B8 `notifications/initialized` đúng thời điểm, không `id` | ĐẠT\* | `mcp_gh.py:125-127`, `mo_phien:167` · ca đo cả hai vế (hỏng ⇒ `len(ghi)==1`; tốt ⇒ `len(ghi)==2` và `"id" not in`) |
| B9 giữ `Mcp-Session-Id` | ĐẠT\* | `mcp_gh.py:141-143,136-137` · ca đọc header của lời gọi **thứ hai** |

### C — sổ ca bất biến

| # | chấm | căn cứ |
|---|---|---|
| C1 sổ ca rỗng ⇒ ĐỎ | ĐẠT\* **ở HÀM**, **KHÔNG ĐẠT ở CỔNG** | `_du_ca` có `len(registry) > 0`; nhưng ca `c1_so_ca_rong_do` gọi `cong()` với **tuple bịa**. Xem P1 `cong-that-khong-noi-vao-du-lieu-that` |
| C2 sổ đột biến rỗng ⇒ ĐỎ | như C1 | `_co_dot_bien` |
| C3 cả hai rỗng ⇒ ĐỎ | như C1 | mutant `c3_cho_ca_hai_rong` khéo: `or` ngắn mạch chỉ bật khi cả hai rỗng ⇒ không vạ lây C1/C2 |
| C4 có MẶT mà không có ĐO ⇒ ĐỎ | như C1, **cộng lệch đặc tả** | Đặc tả C4 đòi *"đột biến bỏ lời gọi thân ca nhưng GIỮ dòng ghi sổ ĐẠT"*. Mutant thật (`c4_khong_goi_ca`) **không làm thế** — nó sửa `_du_ca` thành `bool(registry)`. **Không đột biến nào chạm `chay_cac_ca`**, tức chạm đúng chỗ đặc tả chỉ định |

*Ghi công cho chỗ đúng:* C1–C4 **là bốn hình dạng rỗng độc lập** như đặc tả đòi, và ba mutant
`c1`/`c4`/`d7` cùng đột biến một dòng nhưng theo ba hướng khác nhau để tách đích — thiết kế ấy tốt.
Vấn đề nằm ở chỗ nối, không ở chỗ này.

### D — hợp đồng và cổng

| # | chấm | căn cứ |
|---|---|---|
| D1 top-level `error` ⇒ rc≠0 | ĐẠT\* | `loi_cong_cu`→`main:221-224` trả 3 |
| D2 `result.isError` ⇒ rc≠0 | ĐẠT\* | `mcp_gh.py:98-99`; phản hồi **BƠM**, đã ghi ngay tại ca (`mcp_gh_test.py:385`) đúng như `chua_do_duoc` §2 đòi |
| D3 `{"result":{}}` ⇒ không mở phiên | ĐẠT\* | `mo_phien:165-166` `or not kq["result"]` |
| D4 phản hồi **list** ⇒ lỗi có cấu trúc | ĐẠT\* | `loi_cua:77-78` `isinstance(d, dict)` đứng **đầu** hàm |
| D5 lỗi vận chuyển ở notification ⇒ không mở phiên | ĐẠT\* | `mo_phien:168-170` dùng giá trị trả · mutant `d5_nuot_loi_notification` khớp **duy nhất** khối thứ hai (nhờ dòng `return {}` 8-space trong mẫu) |
| D6 bốn lời gọi CLI cũ, mã thoát 0/2/3 | ĐẠT\* | ca không chỉ đọc `rc` mà còn đọc **sổ `ghi`** (`sum(... == "tools/list") == 2`) ⇒ mutant `d6_doi_co_cli` vẫn cho `rc=0` nhưng **chết vì sổ**. Đây là chỗ làm tốt nhất của bộ test |
| D7 hai số bằng nhau và > 0, mọi đột biến bị giết, `rc=0` | **KĐĐ** | không chạy được suite. Cộng thêm: xem P1 `cong-that-khong-noi-vao-du-lieu-that` |
| D7b nền đỏ ⇒ ô đột biến in `KHÔNG_ĐO_ĐƯỢC` | **KĐĐ** (hình dạng ĐẠT\*) | `mcp_gh_test.py:591-592` đặt `kill_sets={}` và `d8_errors=((),(),())` khi `failed`; `dong_dot_bien`/`dong_d8`/`bang_giao_pham_vi` đều rẽ nhánh `failed`. Fail-close đúng: `errors` khác rỗng ⇒ `cong` False ⇒ `rc=1`. **Nền đỏ hay không thì chưa ai đo.** |
| D8 (a)(b)(c) — kiểm RIÊNG từng cái | **KĐĐ**, xem chi tiết dưới | |
| D9 ngân sách ≤ trần lease | ĐẠT **bằng số**, **có finding** | `git diff --numstat b662fe1..4aa936e0` ⇒ `230 / 610 / 315`; mã = **840**; cả write set = **1155**. Trần lease **KHÔNG ĐỌC ĐƯỢC** (xem §5). Xem finding `d9-ghi-cung-900-trai-chinh-D9` |

#### D8 — ba điều kiện con, kiểm riêng

| điều kiện | chấm | căn cứ |
|---|---|---|
| (a) ca ĐÍCH của mỗi đột biến nằm trong tập giết | **KĐĐ** | `loi_d8` viết đúng ý (`target not in kill_sets.get(name, ())`); mutant `d8_bo_dieu_kien_a` có răng trên **hàm**. Tập giết THẬT thì chưa đo. Truy vết trên giấy 38 mutant không thấy cái nào hụt đích, nhưng **đó không phải phép đo** |
| (b) không đột biến nào có tập giết RỖNG | **KĐĐ** | như trên. `d8_bo_dieu_kien_b` có răng trên hàm |
| (c) mọi ca là đích của ít nhất một đột biến | **ĐẠT** (đếm tĩnh được) | 35 tên trong `CASES`; 38 mutant phủ đúng 35 đích phân biệt (`B2` có 2, `D8` có 3). Đếm bằng mắt trên `mcp_gh_test.py:479-541`. **Nhưng** (c) chỉ phủ ca ĐÃ ĐĂNG KÝ — nó không nói gì về mã của chính runner/cổng |
| nền không rỗng ⇒ xem D7b | **KĐĐ** | |

---

## 3. ĐỘT BIẾN TÔI TỰ LÀM

**KHÔNG CÓ.** Con số là **0 đột biến chạy được / 0 lượt suite chạy được**.

Đây là mục quan trọng nhất của một cross-review vòng 1 và nó **rỗng**. Nói thẳng thay vì viết một
mục nghe cho đủ: tôi đã dựng được danh sách đột biến trên giấy, nhưng theo `CLAUDE.md` — *"NGHĨ RA
được phép thử mà KHÔNG CHẠY nó thì phép thử ấy KHÔNG TỒN TẠI... đừng để nó nằm trong prompt/README/
mô tả PR — chỗ đó là nơi các ca đi chết"* — tôi **không** ghi chúng vào đây như bằng chứng. Chúng
là **việc phải làm của vòng sau**, và vòng sau phải chạy chúng, không đọc chúng:

| # | đột biến bắt buộc phải chạy ở vòng 2 | vì sao nó là ưu tiên 1 |
|---|---|---|
| M1 | Trong `__main__` (`mcp_gh_test.py:606-608`), thay đối số thật của `cong(...)` bằng hằng đã biết là xanh | Nếu suite vẫn in `TỔNG: ĐẠT` + `rc=0` ⇒ khẳng định P1 `cong-that-khong-noi-vao-du-lieu-that` |
| M2 | Trong `chay_cac_ca` (`:549`), bỏ lời gọi `fn()`, giữ `ran.append(name)` | Đây là đột biến mà **đặc tả C4 chỉ định** và bộ test **không có**. Dự đoán: cổng ĐỎ *gián tiếp* qua D8(b) (mọi tập giết rỗng) — nếu đúng thì răng có nhưng **không phải răng của C4** |
| M3 | Trong `Phien.__init__` (`:119`), đổi `mo or _mo_mac_dinh` thành `mo or urllib.request.urlopen` | Dự đoán **SỐNG SÓT**: A5–A7 vẫn xanh vì chúng đo `_mo_mac_dinh`, không đo `Phien`. Nếu sống ⇒ khẳng định `chot-mang-neo-theo-ten` |
| M4 | Trong `b7_xoa_pyc_cu`, đổi `'cu'` → `'cu '` (cùng 16 byte với `'moi'`) rồi chạy `b7_bo_xoa_pyc` | Kiểm bản vá của `b7-xoa-ca-khong-the-do`: chỉ khi độ dài BẰNG NHAU thì cơ chế `.pyc` cũ mới được đo |

---

## 4. FINDING

### P1 — `cong-that-khong-noi-vao-du-lieu-that`

**Toàn bộ cổng — khối `if __name__ == "__main__":` — không có ca nào và không có đột biến nào.**

`mcp_gh_test.py:589-610`:

```
    ran, failed = chay_cac_ca(sys.modules[__name__])
    kill_sets, mutation_errors = ({}, []) if failed else chay_dot_bien()
    ...
    ok = cong(tuple(name for name, _ in CASES), tuple(ran),
              mutant_names, mutant_names if d8_ok else (),
              tuple(failed) + tuple(mutation_errors))
    print("TỔNG: " + ("ĐẠT" if ok else "ĐỎ"))
    sys.exit(0 if ok else 1)
```

C1, C2, C3, C4, D7, D7b, D8 **đều** gọi hàm thuần với đối số **bịa**:

```
def c1_so_ca_rong_do():
    assert not cong((), (), ("m",), ("m",), ())
def d7_cong_xanh_chi_khi_hai_so_duong_bang_nhau():
    assert cong(("c",), ("c",), ("m",), ("m",), ())
```

Chúng chứng minh **vị ngữ `cong` đúng**. Chúng **không** chứng minh cổng **truyền dữ liệu thật vào
vị ngữ ấy**. Và `chay_dot_bien` nạp module đột biến bằng `exec_module` với tên khác `"__main__"`,
nên khối `__main__` **không bao giờ chạy dưới bất kỳ đột biến nào** — kể cả đột biến trên chính tệp
test.

Phép đo tái lập được (M1 ở §3): trong bản sao, thay hai dòng cuối bằng
`ok = cong(("x",), ("x",), ("y",), ("y",), ())`. Không ca nào chạm dòng đó, không mutant nào nhắm
vào nó, `d8_ok` không được đọc nữa ⇒ dự đoán `rc=0`, `TỔNG: ĐẠT`.

**Vì sao đây là P1 chứ không phải P2:** đây là **cùng một hình dạng** với site #6 và #7 trong bảng
`hinh_dang_ke_thua` của chính đặc tả (*"xoá `DAT`/`DO` trước khi in tổng kết"*, *"tách sổ nhưng vị
ngữ cuối vẫn `not DO`"*), chỉ dịch lên **một tầng**: vòng 1 và 2 hỏng ở *vị ngữ*, vòng 3 vá vị ngữ
và để hở *chỗ nối*. Packet tuyên bố đóng 1/8 site; theo phép đọc này nó đóng **vị ngữ** của site
ấy, không đóng **cổng** của nó.

*Ghi công cho chỗ có răng gián tiếp:* nếu `chay_cac_ca` mất `fn()`, mọi tập giết thành rỗng ⇒ D8(b)
đỏ ⇒ cổng đỏ. Nên bất biến "ca có ĐO" **có** một hàng rào — chỉ là hàng rào ấy nằm ở nơi khác chỗ
đặc tả chỉ, và không ai đo nó (M2). Khối `__main__` thì không có hàng rào nào.

**Đề xuất:** một ca chạy suite bằng `subprocess` trên **bản sao đã đột biến khối `__main__`** và
đòi `rc != 0` — đó là cách duy nhất đưa cổng vào tầm đo của chính nó.

---

### P1 — `bo-test-khong-co-cong-nao-chay`

Đo:

```
grep -rn 'mcp_gh' . --exclude-dir=.git -l
  -> ops/specs/mcp-gh-cuu-ho.md
  -> .claude/dev/mcp_gh_test.py
```

**Không tệp nào khác trong kho nhắc tới `mcp_gh`.** `.github/workflows/ci.yml` chạy
`ops/cong_cu_test.py`, `codex_cred_test.py`, `packet_loop_test.py`, `eol_policy_test.py`,
`pre_push_test.py`, `chay_lease_publish_test.sh`, `gate_lifecycle_test.py`,
`command_registry_test.py`, `ci_phamvi_test.py` — **không có `mcp_gh_test.py`**.

Ba hệ quả, cái thứ ba là cái nặng:

1. `CLAUDE.md`: *"Workflow chỉ chạy khi có người bấm là workflow KHÔNG có ai canh."* Bộ 610 dòng
   phản chứng này còn yếu hơn thế — **không ai bấm được** vì không cổng nào biết nó tồn tại.
2. Lời khai `rc=0` của executor là **lời khai duy nhất tồn tại**; không có lượt chạy nào của bên thứ
   ba để đối chiếu, ở CI hay ở đâu.
3. **Đặc tả tự đặt ra một điều kiện nghiệm thu mà write set của nó khiến không thể thoả.**
   Dòng 140-141: *"nghiệm thu cuối phải chạy ở nền cho `bind`"*. `chua_do_duoc` §6:
   *"Cần một lượt chạy ở CI hoặc nền thứ ba."* Nhưng `write_set` là **đúng ba đường dẫn** và
   `.github/workflows/ci.yml` không nằm trong đó — executor **không được phép** nối nó vào CI.
   `ngoai_pham_vi` liệt kê 5 mục cố ý bỏ ra và **không mục nào** là mục này. Tức nợ này **không
   được khai ở đâu cả**: không trong write set, không trong `ngoai_pham_vi`, không trong
   `chua_do_duoc` dưới dạng "packet này không có đường đóng".

**Đây là finding về ĐẶC TẢ, không về bản vá.** Executor làm đúng phạm vi được giao. Chỗ sai là
đặc tả đóng băng một phạm vi khiến điều kiện nghiệm thu của chính nó trở thành bất khả thi, rồi
không ghi điều đó vào `ngoai_pham_vi`.

**Đề xuất:** hoặc mở write set cho `.github/workflows/ci.yml` (một dòng `run:`), hoặc thêm một mục
`ngoai_pham_vi` khai thẳng *"packet này giao một cổng chưa có runner; nợ có tên, Issue nào nhận"*.
Không có đường thứ ba: một cổng không ai chạy **vắng mặt**, và vắng mặt trông y hệt xanh.

---

### P1 — `review-vong-1-khong-do-duoc`

Xem §0. Vòng 1 **không cung cấp assurance nào**. Nếu phiên điều phối tính vòng này vào số vòng
review đã đạt, con số ấy đếm **sự CÓ MẶT của một vòng**, không đếm **năng lực ĐO của nó** — đúng
lỗi *"đếm sự CÓ MẶT thay vì KHẢ NĂNG"* mà kho đã trả giá bốn lần.

Phép đo tái lập được: bảng lệnh ở §0.

**Đề xuất:** vòng 2 phải chạy ở nền cho phép `python` + `bind` (đặc tả đã nói ra yêu cầu ấy cho
executor; nó áp cho **reviewer** không kém). Và điều kiện *"reviewer chạy được suite"* nên là điều
kiện **mở vòng**, kiểm trước khi giao việc, không phát hiện giữa chừng.

---

### P2 — `b7-xoa-ca-khong-the-do`

Ca `b7_xoa_pyc_cu` (`mcp_gh_test.py:288-298`) khai đo lớp *"xoá `.pyc` cũ"*. Khẳng định trung tâm là:

```
        path.write_text("GIA_TRI = 'cu'\n", encoding="utf-8")
        moc = 1_700_000_000
        os.utime(path, (moc, moc))
        assert _nap_co_pyc(path, "mau_cu").GIA_TRI == "cu"
        path.write_text("GIA_TRI = 'moi'\n", encoding="utf-8")
        os.utime(path, (moc, moc))
        assert nap_dot_bien(path, "mau_moi").GIA_TRI == "moi"
```

**Đo được (lệnh đã chạy):** ghi đúng hai chuỗi ấy ra hai tệp rồi `wc -c` ⇒ **15** và **16** byte.

CPython xác thực `.pyc` kiểu timestamp bằng cặp **(mtime, KÍCH THƯỚC nguồn)**. `os.utime` ghim
mtime bằng nhau, nhưng **kích thước lệch 1 byte**, nên `.pyc` cũ bị vô hiệu **bất kể** `xoa_pyc` có
chạy hay không. Khẳng định giữa **không thể ĐỎ** — nó là ca "có MẶT mà không có ĐO", đúng hình dạng
#1 trong bảng `hinh_dang_ke_thua` của chính đặc tả, nằm bên trong ca sinh ra để chặn hình dạng đó.

Mutant `b7_bo_xoa_pyc` **vẫn bị giết**, nhưng bởi khẳng định **cuối** cùng ca:
`assert not ...cache_from_source(path).exists()` — mà khẳng định ấy đo **lớp khác** (lớp "tắt ghi
bytecode", vốn đã có ca riêng `b7_tat_ghi_bytecode`). Nên `D8(a)` vẫn ĐẠT trong khi tính chất được
khai **chưa từng được đo** — đúng lớp lỗi *"một quan hệ đúng trông giống các số hạng đúng"*.

**Và đây không chỉ là một ca yếu — nó là một trong hai bằng chứng dùng để nới `D8`.** Đặc tả r3
biện hộ cho việc bỏ ràng buộc "đúng một ca" bằng lập luận rằng các giao phạm vi còn lại là **chính
đáng** (*"hai ca `B7` cùng đo một họ chốt chống `.pyc`"*). Giao `b7_bo_cam_ghi` → {`B7-xoa`,
`B7-khong-ghi`} **không** chính đáng: nó tồn tại vì `B7-xoa` phải mượn khẳng định của `B7-khong-ghi`
để có răng, do khẳng định của chính nó không thể đỏ. Sửa ca (M4 ở §3) thì giao ấy biến mất.

*Nói cho công bằng:* giao còn lại — `b6_bo_chot_init` → {`B6`, `D6`} — **là** chính đáng: hợp đồng
CLI *"`--path` sai ⇒ `rc=3`"* bắt buộc đi qua chốt lúc dựng, không có đường vòng nào không làm méo
ca. Lập luận nới `D8` đứng được cho ca đó. Nó không đứng được cho `B7`.

**Bản vá:** đổi nội dung sao cho hai phiên bản **cùng số byte** (ví dụ `'cu '` vs `'moi'`), và bỏ
khẳng định `.pyc`-còn-sót khỏi `B7-xoa` (nó thuộc `B7-khong-ghi`).

---

### P2 — `chot-mang-neo-theo-ten`

Hai chốt an ninh khác nhau cùng neo vào **tên** `_mo_mac_dinh`, không neo vào **đường mà credential
thật sự đi**:

- A5–A7 gọi `m._mo_mac_dinh(req, 2)` trực tiếp (`mcp_gh_test.py:116`). Không ca nào khẳng định
  `Phien` **dùng** `_mo_mac_dinh`. `Phien.__init__:119` `self._mo = mo or _mo_mac_dinh` — đổi vế
  phải thành `urllib.request.urlopen` thì credential **đi theo chuyển hướng** trở lại, mà A5–A7 vẫn
  xanh và không mutant nào nhắm vào dòng đó (M3 ở §3).
- B3 bịt mạng bằng `m._mo_mac_dinh = lambda ...` (`:244`). Đặc tả B3 viết, sau khi ca ấy **mất răng
  hai lần**: *"chốt cô lập phải neo vào đường `main` THẬT đi, không neo vào tên hàm ta nhớ"*.
  Bản thi công neo đúng vào tên hàm ta nhớ.

Hôm nay cả hai đúng, vì `Phien` thật sự dùng `_mo_mac_dinh`. Finding là về **phép đo**, không về
hành vi: tính chất *"credential không rời `_OPENER`"* không có hàng rào nào.

**Bản vá rẻ:** thêm khẳng định `Phien("/mcp/", "tok")._mo is m._mo_mac_dinh` vào A8 (hoặc ca riêng),
kèm mutant đổi mặc định opener.

---

### P2 — `dac-ta-dong-bang-co-ba-con-so-ma-mau-thuan`

Đặc tả đóng băng bằng băm chứa **ba** giá trị khác nhau cho **cùng một đại lượng** (số dòng MÃ), và
**không** giá trị nào đúng ở `reviewed_sha`:

| nơi | khai | thật ở `4aa936e0` |
|---|---|---|
| dòng 285 | *"Phần MÃ thật là **790**"* (226 + 564) | **840** |
| dòng 256 | *"mã đứng ở **802** (`mcp_gh.py` 230 · `mcp_gh_test.py` 572) **suốt từ lượt 2**"* | **840** (230 · **610**) |
| dòng 203 | *"trần của lease r2 **≤ 750 dòng thêm**, 3 tệp"* | đơn vị đã đổi sang 2 tệp; trần đã đổi (không đọc được từ đây) |
| dòng 275 | *"write set đã dùng **1000** dòng thêm (226 · 564 · 210)"* | **1155** (230 · 610 · 315) |

Lệnh: `git diff --numstat b662fe1d07c675a222ae26e734377e305775e4f3 4aa936e0a3be676ed2492f89b25f9742a249a965`
⇒ `230 0 .claude/dev/mcp_gh.py` · `610 0 .claude/dev/mcp_gh_test.py` · `315 0 ops/specs/mcp-gh-cuu-ho.md`.

Đây đúng bài học `CLAUDE.md` *"MỘT BẤT BIẾN CÒN ĐÚNG KHÔNG CHỨNG MINH CÁC SỐ HẠNG CÒN ĐÚNG"*: mỗi
mục nội tại nhất quán (226+564=790, 230+572=802, 226+564+210=1000), nên đọc bằng mắt thì cả ba đều
"sạch". Chỉ phép đo mới thấy.

**Và nó phá đúng tiền đề của việc đổi đơn vị ngân sách.** Xem finding kế.

---

### P2 — `don-vi-ngan-sach-doi-sau-khi-truot-va-tien-de-sai`

Đặc tả r3 đổi đơn vị đo ngân sách từ *cả write set* sang *hai tệp mã*, và tự khai là chỗ đáng nghi
(*"đổi ĐƠN VỊ trông tệ hơn đổi con số... Đây là lần thứ BA động vào ngân sách của cùng một packet"*).
Khai như thế là đúng nếp. Nhưng **lý lẽ, chứ không phải sự thành thật, mới là thứ phải đứng được**,
và nó không đứng ở hai chỗ:

1. **Tiền đề thực nghiệm sai.** Lý lẽ là: *"Trần bị chạm ba lần... **cả ba lần đều do ĐẶC TẢ nở,
   không do mã**. Mã đứng ở 802 suốt từ lượt 2."* Commit **kế tiếp** (`4aa936e0`, chính
   `reviewed_sha`) đưa `mcp_gh_test.py` từ 572 lên **610** — mã nở **38 dòng**. Tiền đề *"mã không
   nở"* không sống nổi qua một commit sau khi được viết ra để biện hộ cho một quyết định.

2. **Lý lẽ "reviewer đọc đặc tả như hợp đồng chứ không soát nó như diff" không đúng ở vòng này.**
   ADR-0044 bó **gánh nặng review**. Prompt của vòng này chỉ thị ngược lại: *"đừng chỉ kiểm mã có
   khớp đặc tả không — hãy nghi ngờ CẢ ĐẶC TẢ"*. Ba trong bảy finding của tôi nằm **trong** 315 dòng
   đặc tả. Với reviewer độc lập, đặc tả **là** bề mặt review, và trừ nó khỏi ngân sách là trừ đi
   phần chi phí review đang thật sự phát sinh.

*Chỗ lý lẽ ĐÚNG, ghi cho cân:* việc hợp đồng bị tính vào ngân sách của thứ nó điều khiển **thật sự**
là động cơ ngược — sửa đặc tả cho đúng mà bị phạt là hỏng. Vấn đề không phải ý tưởng; là (a) tiền đề
đo sai, (b) quyết định do **chính phiên soạn đặc tả** đưa ra ngay sau khi trượt ngưỡng cũ, không có
chữ ký độc lập nào trong hồ sơ, và (c) 840/900 là **93% trần** — packet vẫn sát trần dưới đơn vị mới,
nên câu *"packet chưa từng thật sự lớn"* (dòng 263) cũng đã hết hạn.

**Đề xuất:** giữ đơn vị mới nếu người giữ kho muốn, nhưng (i) sửa ba con số đã chết, (ii) ghi lại
tiền đề cho đúng (*"mã nở 802→840 ở lượt 3"*), (iii) đưa quyết định đổi đơn vị vào một ADR chứ đừng
để nó sống trong một đặc tả packet — ADR-0044 là luật chung, và một packet không nên tự sửa luật
chung trong tệp riêng của mình.

---

### P2 — `d9-ghi-cung-900-trai-chinh-D9`

`mcp_gh_test.py:473-475`:

```
def d9_ngan_sach_900_dong_ma():
    tong = sum(sum(1 for _ in path.open(encoding="utf-8")) for path in (NGUON, pathlib.Path(__file__)))
    assert tong <= 900, f"hai tệp mã dùng {tong}/900 dòng"
```

Đặc tả D9 (dòng 194) nói **nguyên văn**: *"**r2 CỐ Ý không ghi cứng con số ở đây**: r1 ghi `≤ 750`
rồi lease nâng lên 1000, và hai mệnh đề không cùng đúng được — đó chính là hình dạng 'sửa TRƯỜNG,
quên VĂN BẢN' mà packet này sinh ra để chặn. Đặc tả trỏ sang trường có thẩm quyền thay vì chép lại nó."*

Bản thi công **chép lại nó** — vào một chỗ khó thấy hơn (một hằng số trong ca test). Không có gì nối
`900` với trường `ngan_sach` của lease; lease đổi trần lần thứ tư thì ca này im lặng bất đồng.

Hai điểm phụ:
- Ca đo **tổng số dòng của tệp**, không đo **cột dòng THÊM của `numstat`** như D9 viết. Ở packet này
  hai đại lượng bằng nhau vì cả hai tệp đều mới (`230 0`, `610 0`); ở packet sau sửa tệp đã có thì
  chúng khác nhau, và ca sẽ đo sai đại lượng mà không ai biết.
- `assert tong <= 900` **cho phép đúng giá trị** mà đặc tả nói phải kích hoạt luật tách:
  *"nếu MÃ **chạm** 900 thì câu trả lời là TÁCH"* (dòng 270). Nên là `< 900`, hoặc sửa câu ở đặc tả.

---

### P2 — `rut-van-ban-bo-content-1-tro-di`

`mcp_gh.py:103-109`:

```
        nd = kq.get("result", {}).get("content") if isinstance(kq.get("result"), dict) else None
        if isinstance(nd, list) and nd and isinstance(nd[0], dict) and "text" in nd[0]:
            return nd[0]["text"]
```

Chỉ `content[0]` được trả; `content[1:]` bị **bỏ im lặng**, và khối không phải `text` (`image`,
`resource`) cũng vậy. Đó là **cắt tải trọng**, cùng lớp với thứ `B2` sinh ra để chặn — chỉ cắt theo
chiều **số khối** thay vì chiều **số ký tự**. `B2` khẳng định `len > 20000` trên **một** khối, nên
mù hoàn toàn với chiều này, và không mutant nào nhắm vào `nd[0]`.

Hậu quả thật cho người dùng module: một `tools/call` trả nhiều khối sẽ mất dữ liệu **không báo lỗi**
— `rc=0`, đầu ra trông hợp lệ. Đúng hình dạng packet này đang chống.

---

### P2 — `loi-khai-38-38-bi-giet-rong-hon-phep-do`

Handoff khai *"38/38 đột biến **bị giết**"*. Suite **không in con số ấy bao giờ**:

```
def dong_dot_bien(kill_sets, mutants, failed):
    if failed:
        return "ĐỘT BIẾN   : KHÔNG_ĐO_ĐƯỢC (nền đỏ)"
    return f"ĐỘT BIẾN   : đã đo {len(kill_sets)}/{len(mutants)} tập giết"
```

`len(kill_sets)` đếm **số đột biến đã ĐO ĐƯỢC tập giết**, kể cả tập giết **rỗng**. Sau khi `D8` đổi
sang "quy được trách nhiệm", khái niệm "bị giết" **không còn được cổng tính nữa** — `killed` truyền
vào `cong()` là `mutant_names if d8_ok else ()`, tức một **hệ quả của `d8_ok`**, không phải một phép
đếm. Điều kiện `D8(b)` mới là thứ chặn tập giết rỗng.

Về mặt ngữ nghĩa cổng thì ổn. Finding là về **lời khai**: nói "38/38 bị giết" trong khi công cụ nói
"đã đo 38/38 tập giết" là lời khai **rộng hơn phép đo** — đúng bệnh mà `CLAUDE.md` chép lại nhiều
lần. Sửa lời khai, hoặc cho suite in thẳng số tập giết **khác rỗng**.

---

### P2 — hai mục nhỏ, gộp

- `b7-ten-do-tinh-chat-khong-he-qua`: `b7_ten_tung_dot_bien_rieng` khẳng định 4 tên `ten_ban_sao`
  phân biệt. Nhưng `chay_dot_bien` cấp cho **mỗi** đột biến một `TemporaryDirectory` riêng
  (`:565`), nên tên tệp **không thể** va nhau dù `ten_ban_sao` trả hằng; và tên module đã riêng
  (`f"mcp_gh_db_{i}"`). Ca đo một tính chất **không có hệ quả** — nó là ca "có ĐO mà không có
  RỦI RO", mặt kia của cùng đồng xu với `B7-xoa`.
- `phien-cong-cu-khong-ai-do`: `Phien.cong_cu` (`mcp_gh.py:173-175`) không được `main` gọi (main
  gọi thẳng `p.goi("tools/list")`), không ca nào chạm, không mutant nào nhắm. `muc_tieu` 5 giao việc
  *"tách module khỏi CLI"* — bề mặt module giao ra có một phương thức công khai chưa ai đo. Hoặc đo
  nó, hoặc bỏ nó.

---

## 5. CHỖ KHÔNG ĐO ĐƯỢC

1. **Toàn bộ hành vi chạy của `mcp_gh_test.py`** — `rc`, `35/35`, tập giết, `D7`, `D7b`, `D8(a)(b)`.
   Lý do: quyền (bảng §0). Đây là chỗ trống lớn nhất của vòng này.
2. **`A5`, `A6-302`, `A6-303`, `A7`** — cần `bind` 127.0.0.1 **và** chạy được `python`. Không có cả
   hai. Lỗ P1 "không đi theo chuyển hướng" vì thế **vẫn chưa có nền độc lập nào xác nhận**, đúng
   như `chua_do_duoc` §6 đã dự báo — vòng review này không gỡ được nó.
3. **Lease của packet.** `git for-each-ref` trong worktree cho **2** nhánh (`claude/mcp-gh-cuu-ho-exec-1`
   và bản `origin/` của nó); không nhánh `ops/**` nào, `ls ops/leases/ | grep -i 'mcp|cuu-ho|319'`
   ⇒ **0**. `.git` chỉ đọc ⇒ không `fetch` được; MCP github bị chặn quyền. Nên **KHÔNG kiểm được**:
   trần ngân sách đang hiệu lực (900? 1100?), `spec_sha256` có khớp
   `7294d24e8acb1c388aae0098e9463ccc3e886a03f6d124ac79ca98a947e50d92` không, năm lần sửa đổi, việc
   đổi executor `claude`→`codex`, và việc `reviewed_sha_required` đã được sửa khỏi `base_sha`.
   Ba điều phiên điều phối tự khai ở phần giao việc **đều nằm nguyên trong ô này** — tôi không xác
   nhận được điều nào. Theo `CLAUDE.md` (*"SỔ LEASE KHÔNG NẰM MỘT CHỖ"*, *"không fetch được ref nào
   thì ĐỎ"*), trạng thái đúng là **KHÔNG ĐO ĐƯỢC**, không phải "chắc là ổn".
4. **PR #339** — check run, review, comment: MCP github bị chặn quyền; REST tới `repos/...` bị proxy
   chặn 403 theo `CLAUDE.md`. Không biết cổng CI của PR xanh hay đỏ, cũng không biết đã có review
   nào khác.
5. **Nguồn cấp việc** — comment `5423010218` trên PR #315 không đọc được. Kiểm được **một nửa** lời
   khai của đặc tả: `ls ops/reviews/ | grep -i '314|315|mcp-gh'` ⇒ **0** trong **113** tệp, khớp
   khẳng định *"verdict ấy KHÔNG có biên nhận trong kho"* — nhưng chỉ trên cây này, không phải trên
   206 ref.
6. **`hinh_dang_ke_thua` site 1–7** — không tái lập. Site **8** kiểm được và **ĐÚNG**:
   `ops/lease_publish_test.py:3290` là `return 1 if hong else 0`, không có chốt `len(CA) > 0`
   (`grep -n 'return 1 if|len(CA)' ops/lease_publish_test.py`).
7. **Ảnh hưởng tới cổng phát hành** — hai tệp `.py` mới dưới `.claude/dev/` có làm đổi
   `files_scanned` trong `references/golden/workflow_audit.json` (đang là **73**) hay không: không
   chạy được `workflow-audit` để so. Đọc mã cho thấy phép quét nhắm `scripts/**` (78 tệp `.py`
   tracked ⇒ 73 sau loại trừ), và `.claude/` nằm trong `_RELEASE_EXCLUDE_DIRS`, nên **có lẽ** không
   ảnh hưởng — nhưng *"có lẽ"* không phải phép đo, và bài học r238 là đúng ca này.

---

## 6. Tóm tắt cho phiên điều phối

**Không được land ở trạng thái hiện tại**, vì hai lý do độc lập:

- **Chưa ai ngoài executor chạy bộ test này**, và packet không có đường để ai chạy nó
  (`bo-test-khong-co-cong-nao-chay`). Cổng vắng runner ≡ cổng vắng mặt.
- **Cổng của chính bộ test nằm ngoài tầm đo của chính nó** (`cong-that-khong-noi-vao-du-lieu-that`)
  — cùng hình dạng với hai vòng trước, dịch lên một tầng.

Cộng thêm **một ca không thể ĐỎ** (`b7-xoa-ca-khong-the-do`) mà lại là một trong hai chỗ dựa của
lập luận nới `D8`.

Phần làm **tốt**, ghi để không bị đọc thành "bản vá kém": `kiem_dich_den` chặt và không phản chiếu
URL; chốt kiểm lại lúc gửi đúng chỗ; `loi_cua` xếp thứ tự nhánh chuẩn (`isinstance` trước, `error`
trước `thiếu result`); `D6` đo bằng **sổ lời gọi** chứ không bằng `rc` — đó là chỗ bộ test này mạnh
hơn hẳn hai vòng trước; ba mutant `c1`/`c4`/`d7` đột biến cùng một dòng theo ba hướng để tách đích
là thiết kế khéo; và ba bản sửa đổi đặc tả đều tự khai chỗ đáng nghi thay vì giấu. Vấn đề còn lại
là **chỗ nối** và **năng lực đo**, không phải trình độ của bản vá.

---

**Đường dẫn verdict:** `ops/reviews/mcp-gh-cuu-ho-review-1-claude-verdict.md`

**Số finding: P1 = 3 · P2 = 8**

P1: `cong-that-khong-noi-vao-du-lieu-that` · `bo-test-khong-co-cong-nao-chay` ·
`review-vong-1-khong-do-duoc`

P2: `b7-xoa-ca-khong-the-do` · `chot-mang-neo-theo-ten` ·
`dac-ta-dong-bang-co-ba-con-so-ma-mau-thuan` ·
`don-vi-ngan-sach-doi-sau-khi-truot-va-tien-de-sai` · `d9-ghi-cung-900-trai-chinh-D9` ·
`rut-van-ban-bo-content-1-tro-di` · `loi-khai-38-38-bi-giet-rong-hon-phep-do` ·
`hai-muc-nho-gop` (= `b7-ten-do-tinh-chat-khong-he-qua` + `phien-cong-cu-khong-ai-do`)

**Đột biến tự chạy: 0** — xem §3. **Suite chạy: 0 lượt.**
