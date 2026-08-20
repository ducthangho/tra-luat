# Prompt BẤT BIẾN — Executor `PLAT-X2`, lượt 1, provider `claude`

Tệp này là hợp đồng của MỘT lượt executor. Nó **không** cấp quyền: quyền đến từ
`ops/leases/plat-x2-exec-1-claude-20260820.yaml`. Sửa tệp này sau khi lease đã cấp là làm
**băm lệch** ⇒ cổng đăng lease trả `rc=6`.

## 1. Mỏ neo

| trường | giá trị |
|---|---|
| packet | `#195` — `[WP PLAT-X2]` |
| revision · generation | 1 · 1 |
| spec | **thân Issue `#195`** là authority |
| base / start head | `50d8d12e146792368e7100f732ff15a8d32fe48d` (`origin/master` lúc cấp lease) |
| nhánh làm việc | `claude/plat-x2-exec-1`, `branch_ownership: exclusive` |
| role | `executor`. KHÔNG review, KHÔNG approve, KHÔNG land việc của chính mình |
| effective write set | `.github/workflows/ops-publish-lease.yml` · `ops/lease_publish_test.py` · `.gitignore` |
| review class | `sensitive` · assurance đích `cross_approved` · reviewer `codex` |
| mô hình · effort | Claude Opus 5 · `xhigh` |
| hạn (wall clock) | lease tới `2026-08-21T07:30:00Z`; `timeout_clock=wall`, fail-closed |

## 2. Việc phải làm

Bước `tìm lease vừa đổi` của `ops-publish-lease.yml` có đường dự phòng **quét cả thư mục**
khi `github.event.before` toàn số 0 — tức **mọi push mở nhánh mới**, đúng cách kho vẫn đăng
lease. Một lease cũ **chưa từng đăng mà đã hết hạn** nằm trong cây làm cả lượt chạy `rc=8`,
nên **mọi lease mới đều không đăng được** kể từ 18-08-2026.

1. Bỏ đường quét cả thư mục; nhánh mới thì so với `git merge-base origin/$MAC_DINH $NAY`.
2. Không phân giải được mốc so ⇒ **ĐỎ**, không quét bừa, không `|| true`.
3. Đưa `${{ }}` ra khỏi thân `run`, khai qua `env:`.
4. `.gitignore`: thêm `.claude/.packet_state/`.

## 3. Nghiệm thu và phản chứng

§4 và §5 của thân Issue `#195`. Phản chứng phải **trích thân bước TỪ CHÍNH tệp YAML** rồi
chạy trên kho git tạm — chép lại thân bước là hai bản sẽ trôi lệch. Nền phải giữ: **28 ca**
(`rg -c '^def t[0-9]+_' ops/lease_publish_test.py` trên base). `N/N` hai số bằng nhau; `rc`
đọc **trực tiếp từ tiến trình**, không qua pipe.

## 4. Điều kiện DỪNG

- Chốt phải nằm ngoài ba tệp write set ⇒ dừng, xuất handoff, mở packet riêng. **Không tự mở
  write set.** Đặc biệt: **không** sửa `ops/lease_publish.py` (write set của `#188`).
- Cùng một hình dạng lỗi lần thứ hai ⇒ quyết định về **cách làm**, không mở vòng vá thứ ba.
- Trần review **2 vòng**; hết trần mà chưa approve ⇒ Review Rescue Checkpoint.

## 5. Cấm

- Không nới bất kỳ chốt nào của cổng: hết hạn vẫn chặn, tự cấp vẫn chặn, neo prompt vẫn kiểm.
- Không dọn lease cũ trong `ops/leases/` — sổ chép thêm.
- Không secret trong đầu ra; không merge/land; không xoá nhánh; không ép lùi.
- Không đọc `rc=0` thành bằng chứng: đòi **bằng chứng dương**.

## 6. Handoff bắt buộc khi kết thúc lượt

Tối thiểu: packet/revision/generation · base và exact head · provider/model/session/role ·
write set khai báo **và** changed paths thực · lệnh test, `rc`, số đếm dương, skipped/not-run
tách riêng · từng phản chứng đã chạy và invariant nó đo · việc còn lại · vai kế tiếp và **một**
hành động thủ công cụ thể.
