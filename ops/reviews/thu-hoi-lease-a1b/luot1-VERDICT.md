<!-- Verdict codex lượt 1 (gpt-6-astra high, codex_cli tại chỗ) trên ops/specs/THU-HOI-LEASE-A1b.md bản nháp 1 @ 65a612a, base 67802bf. Chép nguyên văn từ tệp -o của codex exec; chỉ bỏ khoảng trắng cuối dòng (hard-break Markdown) theo tiền lệ ops/reviews/thu-hoi-lease-a1a-r2/. -->
Review ở mức `advisory_review`, trên:

```text
base: 67802bf9a1b9adba6d8b13c63ee46744d74655b5
head: 65a612a385be504ca14b303433588106bbebb6b2
tree: b38f877012d96b5649f0e23e620a2c2dd613b9c2
```

Không sửa repository. Các phép đo dưới đây chạy bằng shell cục bộ; không nhận assurance của connector hay human audit.

1. **P1 — M6 là điều kiện trước đóng băng nhưng chỉ xuất hiện sau thi công.** `ops/specs/THU-HOI-LEASE-A1b.md:25`, `:78`, `:87`.

   Q10 đòi hai run cách nhau ≥24 giờ **trước đóng băng**, A4 yêu cầu digest do **bước M6** sinh. Nhưng bước này chưa có trên canonical, cũng không thuộc thay đổi workflow của A1a. Workflow PR chạy định nghĩa và mã tại `C = github.workflow_sha`; thêm M6 vào ứng viên H không làm bước ấy chạy.

   Bằng chứng: đọc workflow tại base bằng `git show 67802bf:.github/workflows/ops-thu-hoi-admission.yml`, parse YAML và đếm bước, **rc=0**:

   ```text
   runs-on: ubuntu-latest
   run_steps: 2
   workflow_calls_hoso_adapter_do: False
   ref: ${{ github.workflow_sha }}
   ```

   `git show 67802bf:ops/specs/THU-HOI-LEASE-A1a-r2.md` cho M12 chỉ đổi SHA của `upload-artifact`; không thêm bước đo profile.

   Chạy mã H để lấy digest không giải quyết hợp lệ vòng phụ thuộc: nó phá biên canonical của workflow và yêu cầu producer độc lập với ứng viên trong ADR-0047. `pull_request_target` có ngữ cảnh tin cậy của kho đích; **workflow này** giới hạn token thành `contents/pull-requests/actions: read`, nhưng vẫn truyền `secrets.GITHUB_TOKEN` vào bước kiểm. Không được suy token có quyền ghi, cũng không được suy quyền đọc khiến chạy mã ứng viên an toàn. [Tài liệu GitHub](https://docs.github.com/en/actions/reference/security/secure-use).

   **Sửa:** tách bước đo tin cậy thành tiền đề được cấp quyền và land trước, hoặc chỉ rõ bootstrap độc lập đã tồn tại. Receipt phải neo commit định nghĩa, mã producer, runner và attempt. **Khóa:** ứng viên sửa producer không được đổi phép đo canonical. **Rủi ro:** cần cập nhật thứ tự packet và thời điểm đóng băng.

2. **P1 — “Bật cờ” chưa nối luật mới vào production; A5 có thể xanh chính vì chưa kích hoạt.** `ops/specs/THU-HOI-LEASE-A1b.md:73`, `:77`, `:87–88`.

   Tại base, `check` vẫn dùng luật cũ; `ai-dang-giu` vẫn phân loại bằng luật cũ. Cờ `True` chủ yếu bỏ chốt “sổ phải rỗng”, không tự gọi discovery hay đưa verdict dự báo thành verdict production. A1a M1–M14 cũng không giao phần nối này.

   Bằng chứng:

   ```bash
   rg -n 'SO_THU_HOI_KICH_HOAT|def lenh_check|def lenh_ai_dang_giu' ops/lease_publish.py
   ```

   **rc=0**, các nơi dùng cờ thực thi là `:1734` và `:1873`; `lenh_check` ở `:1902`, `lenh_ai_dang_giu` ở `:1934`. Phân tích AST cho ba entry point:

   ```text
   lenh_kiem_thu_hoi_github direct discovery calls= []
   lenh_check direct discovery calls= []
   lenh_ai_dang_giu direct discovery calls= []
   ```

   Tôi chạy phản chứng `python3 -B -` bằng `_nap_cong`, `_kho_thu`, `_goi_main` của suite, dựng cặp thay thế trong kho tạm ngoài checkout theo fixture `t135`. **rc=0**:

   ```text
   flag= False check rc= 0
   DU_BAO: cu-het-han không có trong sổ lẫn BIA_MO_LICH_SU ⇒ rc dự báo 8
   flag= True check rc= 0
   DU_BAO: cu-het-han không có trong sổ lẫn BIA_MO_LICH_SU ⇒ rc dự báo 8
   ```

   Probe riêng với neo profile rỗng cũng cho:

   ```text
   check flag=True empty_anchor=True rc=0 discovery_calls=0
   ```

   Vì vậy A4 chưa có đường production để giết mutant bỏ so profile; A5 có thể xanh khi chẳng có chuyển đổi hành vi. Hơn nữa, M5 đòi **mọi rc bằng nhau** trái r9 Q6: r9 cho phép delta bảo thủ `0→8` và yêu cầu phân loại delta trên cùng map/clock.

   **Sửa:** giao rõ phần wiring production trước khi bật; thay M5 bằng phép đo delta theo Q6. **Khóa:** một ca production đi qua discovery thành công, neo sai ⇒12, và cặp sau mốc/sổ rỗng cho delta kỳ vọng `0→8`. **Rủi ro:** phần mã bổ sung có thể vượt trần 300 dòng, cần tách packet; không đẩy sang slice C vốn chỉ ghi dữ liệu thu hồi.

3. **P2 — Hợp đồng digest dùng schema A0, trái A1a r2 đã đóng băng.** `ops/specs/THU-HOI-LEASE-A1b.md:43`, `:67`, `:110`.

   Câu `git_sha256` thuộc digest đúng với mã ở base, nhưng sai với **tiền đề A1a đã land** của A1b. A1a đã quyết định đưa trường này ra tầng audit; A1b lại nói bỏ nó là quyết định tương lai ngoài phạm vi.

   Bằng chứng:

   ```bash
   rg -n '^\| M[12] \||^\| A2 \|' ops/specs/THU-HOI-LEASE-A1a-r2.md
   ```

   **rc=0**, output tại `:145–146`, `:222`:

   ```text
   tầng AUDIT-ONLY ra ngoài digest (`git_sha256`, băm nhị phân khác)
   `bam_ho_so` băm chỉ tầng bắt buộc
   đưa `git_sha256` trở lại dict được băm ⇒ ĐỎ
   ```

   Nếu M6 băm toàn bộ JSON như §2 mô tả, receipt có thể không bao giờ khớp digest mà adapter v2 thực sự so.

   **Sửa:** M6 gọi đúng `bam_ho_so` của schema canonical v2, ghi riêng phần audit; phân tích drift theo các trường thực sự được băm, gồm `image_version`. **Khóa:** đổi riêng `git_sha256` không đổi digest; đổi trường bắt buộc phải đổi digest. **Rủi ro:** thay lại schema sẽ lấn A1a; sửa mô tả và cách đo, không tự đảo quyết định đã đóng băng.

   Executor **tự đo rồi đề xuất**, chủ kho duyệt độc lập, không tự động là “tự khai” bị cấm. Điểm cần chứng minh là provenance và tính độc lập của producer, không phải cấm executor thực hiện phép đo.

4. **P2 — T2 chưa cung cấp hợp đồng consumer cần thiết để nghiệm thu M2, đồng thời bỏ ngỏ nợ C≠S.** `ops/specs/THU-HOI-LEASE-A1b.md:34`, `:74`, `:85`.

   “Tệp consumer có và gọi được” chưa xác định entry point production, cách tiêm raw API fixture, mã từ chối và identity được kiểm. Một fixture tự dựng lại join trong test có thể xanh dù consumer thật bỏ một mắt xích.

   Bằng chứng:

   ```bash
   git grep -n -E 'check_suite|check_run_url|thu-hoi-receipt' 67802bf -- .claude
   ```

   **rc=1**, không có match. Đây là bằng chứng consumer chưa có trong cây được giao, không phải lỗi công cụ.

   Đọc `.github/workflows/ops-thu-hoi-admission.yml:155–163`, **rc=0**:

   ```text
   d["bo_kiem_da_chay_commit"] = wf_sha
   ... hợp đồng consumer M9 ... còn giả định C == S: nợ có tên ...
   ```

   Trong khi r9 Q10(a) vẫn đòi actual definition/code `== S`. A1b kế thừa nguyên Q10 nhưng không chốt cách xử lý khác biệt này. Canary chỉ yêu cầu `S≠H` chưa kiểm trường hợp `C≠S`.

   **Sửa:** trước freeze, T2 phải neo exact consumer SHA, đường dẫn/API gọi thật và hợp đồng C/S/H/T đã được quyết định. Test ở `ops/lease_publish_test.py` được phép **đọc/import** consumer ngoài write set; điều đó không vi phạm L2. Nếu phải sửa consumer thì trả về packet tiền đề. **Khóa:** consumer thật nhận fixture đầy đủ, rồi từ chối từng liên kết sai; thêm canary/fixture `C≠S`. **Rủi ro:** không “sửa” bằng cách nới provenance hoặc chép validator vào test.

5. **P2 — M6 thiếu tiêu chí phân biệt đúng runner và bước đo; thêm bước còn đụng hợp đồng test hiện có.** `ops/specs/THU-HOI-LEASE-A1b.md:78`, `:90`.

   A7 chỉ kiểm lint và kích thước. A4 kiểm digest nhưng không chứng minh literal `runs-on: ubuntu-24.04`; giữ `ubuntu-latest` vẫn có thể chạy trên cùng image và cho cùng digest. Không tiêu chí nào nêu mutant giữ runner cũ phải đỏ.

   Bằng chứng:

   ```bash
   rg -n 'đúng hai bước run' ops/lease_publish_test.py
   ```

   **rc=0**:

   ```text
   5154: chot(len(than) == 2, f"đúng hai bước run (cài + kiểm): {len(than)}")
   ```

   M6 thêm bước `run` thứ ba sẽ làm test này đỏ, nhưng các mục tiêu trong tệp test chỉ giao M2/M3/M5; chưa giao cập nhật hợp đồng workflow tương ứng.

   **Sửa:** thêm mục tiêu test riêng, vẫn chiếu một đường dẫn, kiểm runner, producer canonical và trường receipt. **Khóa:** giữ `ubuntu-latest`, bỏ bước đo hoặc thay producer bằng H đều phải làm đúng ca đỏ. **Rủi ro:** đừng chỉ nới `len(than)` để suite xanh; cần giữ chốt nhận diện từng bước.

Các phép đo L5 **đã khớp** tại base: hai SHA-256 r9/A1a r2; các dòng `934/942/944/948/1258/47`; `ops/thu-hoi/` vắng; write set ba đường. Lệnh `git diff --numstat 0721811^1 0721811`, **rc=0**, cho **141 + 919 + 1327 = 2387 dòng thêm / 3 tệp**. Script Q6 chạy lại, **rc=0**, cho **89 lease hợp lệ, 11 cặp hai chiều, digest `8f372ccd…`, 0 cặp giữ lại**.

Các số **100 run/89 success**, annotation migration, lease #579 g20, ruleset và comment authority: **not_measured độc lập qua GitHub**, không coi là passed. A3 có phản chứng khả thi; A1/A6 là phép đo vận hành; A7 đo được lint nhưng chưa bao phủ M6. Không chạy full suite hay CI cho diff chỉ đặc tả này.

VERDICT: REQUEST_CHANGES

<!-- Đính chính 27-09 (bản nháp 14): header log runtime của lượt này ghi `reasoning effort: none`; nhãn effort `high` ở dòng đầu là SAI. -->
