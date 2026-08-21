# Prompt BẤT BIẾN — Executor `PLAT-X4`, lượt 1, provider `claude`

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#203` — `[WP PLAT-X4]` |
| base | `origin/master` **tại lúc bạn bắt đầu** — đọc lại, đừng tin số trong tệp này |
| nhánh | `claude/plat-x4-exec-1` (dựng từ `origin/master` mới nhất) |
| role | `executor` · reviewer `codex` · assurance đích `cross_approved` |
| write set | `ops/lease_publish_test.py` · `.github/workflows/ops-publish-lease.yml` · `.github/workflows/ci.yml` · `planned:ops/cai_actionlint.sh` |
| mô hình · effort | Claude Opus 5 · `xhigh` |

## 2. ĐỌC TRẠNG THÁI THẬT TRƯỚC KHI VÁ — không tin tệp này

Kho đang có **nhiều phiên chạy song song**. Trước khi sửa dòng nào:

```
git fetch origin master && git log --oneline -5 origin/master
```

và liệt kê PR đang mở. Tại lúc soạn prompt này có **hai PR của phiên codex** đang mở —
`#202` (`PLAT-M3-R`, chạm `.claude/dev/launcher*.py`) và `#199` (`PROTO-01-FIX`). **Kiểm
giao write set** với chúng trước khi bắt đầu; nếu giao khác rỗng thì **DỪNG và báo người
giữ**, đừng tự xử.

## 3. Việc — đóng hai P2 của cross-review, chữa ở TẦNG

Đọc thân Issue `#203` để có bằng chứng đầy đủ. Tóm tắt:

- **P2-1**: `t34` bỏ sót caller thật — `echo preparing; python ops/lease_publish_test.py`
  vẫn cho suite `35/35`, vì danh sách `SOI` khớp **chuỗi con trên cả dòng**.
- **P2-2**: `t35` chỉ kiểm sự **đồng hiện** của chuỗi — thay `grep -qx "$AL_VER"` bằng
  `printf '%s\n' "$AL_VER" >/dev/null` thì suite vẫn `35/35`.

**KHÔNG vá bằng cách siết mẫu khớp chuỗi lần thứ tư.** Đây là lần thứ ba cùng một hình
dạng lỗi, và `CLAUDE.md` quy định lúc đó phải hỏi *"có nên làm việc này không"*. Hướng đề
nghị: tách phần **cài + đối chiếu phiên bản** thành `ops/cai_actionlint.sh`; cả hai
workflow chỉ gọi script ấy; `t35` **chạy thật** script đó với `actionlint` giả (version
sai · rc=0 mà không phải actionlint · không tồn tại) và đòi nó **từ chối**; `t34` chỉ còn
kiểm một token canonical.

Được quyền chọn cách khác **nếu đo được** rằng nó đóng cả hai finding tốt hơn — nhưng phải
nêu lý do, và không quay lại parse shell tự chế.

## 4. Nghiệm thu

Cả hai phản chứng của reviewer phải **ĐỎ** trên bản vá, cộng các dạng `&&`, `|`, gọi qua
biến, heredoc. `actionlint` giả trả version sai ⇒ bước cài ĐỎ. Bộ test **không tụt dưới
35 ca**, `N/N` hai số bằng nhau. **CI ubuntu VÀ Windows đều xanh trên đúng head trước khi
land** — `t32` chạy `bash`, và Windows đã cắn một lần ở `e03c6d28`.

## 5. Điều kiện DỪNG

- Chốt phải nằm ngoài write set ⇒ dừng, xuất handoff, mở revision — **không tự mở**.
- Cùng hình dạng lỗi lần thứ hai trong lượt này ⇒ dừng, quyết định về **cách làm**.
- Trần review **2 vòng**; hết trần mà chưa approve ⇒ Review Rescue Checkpoint, người giữ chọn.

## 6. Cấm

Không hạ chuẩn `t33`. Không nới chốt nào của cổng đăng lease. Không đụng
`ops/lease_publish.py` (write set `#188`). Không merge việc của chính mình.
