# VERDICT — cross-review PR #468, lượt 8

verdict: changes_requested
reviewed_sha: 4d0ead5591a58463423754cc93a84ce744c3a50b

Kết luận nội dung: **changes_requested — 2 P1, 2 P2**. Sáu finding lượt 7 được giữ nguyên slug và tự đo: **4 ĐÃ VÁ THẬT, 1 VÁ HỜ, 1 CHƯA VÁ**. Hai finding mới là hợp đồng A2 dùng nền cũ và trạng thái chọn H chưa đồng bộ.

Reviewer: **Codex / OpenAI**, phiên độc lập qua API, có shell cục bộ; transport: tệp trong sandbox. Đã đọc protocol trích §8/12/13 trước và dùng khung `tai-lieu/cross-review-SKILL.md`. Chỉ đọc/ghi trong phạm vi PROMPT; không mạng, không commit/push, không đăng GitHub, không lập receipt hay cấp merge authorization. Chỉ thị offline ưu tiên bước đăng PR trong skill.

Các mốc đo là **07-09-2026 UTC**, trước hạn #456 **14:30:07Z**. Lệnh/script và hiện vật của reviewer nằm trong `do-review8/`. Đường `ops/...` và `.claude/...` bên dưới tính từ `cay-kho/`. Tái tính dữ liệu API đã lưu không được khai thành readback GitHub trực tiếp; replay stdout có rc ghi trong hồ sơ không được khai thành suite vừa chạy.

## ĐỐI CHIẾU LƯỢT TRƯỚC

- `span-rong-nuot-ti-le-vo-can` [P1]: **ĐÃ VÁ THẬT về nghĩa vụ bằng chứng còn mở ở lượt 7**. Nguyên harness/attack/extra-checks lượt 6, chạy trong layout riêng ngoài checkout, tái lập **1213 ca / 0 đỏ giả / 0 bỏ sót / 0 ngoại lệ**, corpus và summary khớp byte. Bản `outputs-that/pretooluse_guard_test.stdout` đúng **9995 B**, SHA-256 `69878c4f9efb24a6666d1cf0e4dea99d1ac87fa0aa904e28c6d397fd08cb7991`, metadata ghi **rc=0**, BASE/H replay đều **0**. Đủ **8/8** định dạng có bản xanh ghi rc0; H bác **0/8**. P1 thiếu bản thứ tám nay **đóng**. Đây là review thiết kế và evidence; không tuyên bố H đã thi công hay mọi nghiệm thu tương lai đã đạt. Suite reviewer tự chạy với Ruff0.15.15 cũng **rc0, CA39/39, mutant34/34, stdout9995B trùng từng byte**; H/BASE replay bản vừa chạy đều0. Đ1–Đ5 ở bảng dưới.
- `bia-mo-mot-ref-khong-thu-hoi-moi-ban` [P1]: **CHƯA VÁ tại thời điểm đo**. Quét thật lúc **09:21:30.927918Z**, xác nhận lại **09:30:02.764850Z**: **86** cặp blob/path, **2** blob #456; một có bia mộ đối xứng, một còn hạn chưa bia mộ. Registry có **2** người giữ, `ci.yml` có **1**. Blob cũ tồn tại trên **origin/master** thật trong snapshot, không chỉ ref GATE cục bộ. Mô phỏng **14:30:06Z → 14:30:07Z** cho registry **2 → 1**; không đổi thành trạng thái đã xảy ra. P1 còn mở; không tính lỗi rig. Chuỗi r2 không làm mất blob cũ.
- `thieu-hien-vat-quyet-dinh-h-va-chi-phi` [P1]: **ĐÃ VÁ THẬT đối với nguồn quyết định hiện hành**. Nguồn **13 run / 26 job / 1140 bước** tái sinh các đầu ra khớp byte. Chọn đúng **11 run**, cả hai job/bước success và tên `tl selftest` theo tiền tố: **28/28** ô n/min/max/median, **12/12** đầu dải làm tròn của GATE r2 khớp. Receipt-v2 trung vị **7.7929292929×**, dải **7.7051777052–7.8824863416×**. Băm spec r2 bằng lease exec-1r2 và blob Issue neo; `check` rc0. Không đòi nguồn 2062 hàng đã được rút khỏi vai trò nguồn hiện hành. Các câu phân loại mẫu/Issue còn cũ được giữ ở finding P2 riêng, không đánh đồng với việc bảng tỷ lệ đã tính đúng.
- `issue-lo-neo-commit-cu-kem-bam-moi` [P1]: **ĐÃ VÁ THẬT**. Tự đọc blob `<commit>:<spec_path>` cho cả bốn packet: **4/4** khớp spec hiện tại, hai trường hash lease và hash Issue. #463/#464 neo `d85365463259615537c4fb96acd2408d917d9bd2`; #465/#466 giữ `b743f1798aba12615f903a11bd451c87e404814e` và vẫn đúng. Bản chiếu `tai-lieu/` khớp byte.
- `a9-khai-sai-base-ngoai-le` [P2]: **ĐÃ VÁ THẬT**. Bốn fixture nguyên byte, hai formatter × hai vị trí số **5000** chữ số: ở CA, **BASE=H=ValueError**; ở cặp đột biến, **BASE=0/H=ValueError**. Đúng cả LO A9, LO `chua_do_duoc` D9 và Issue #464. Không đổi Python int limit; ngoại lệ H là fail-closed, không tính thành phản chứng Đ1 mới.
- `bien-do-khac-head-khong-phai-nhieu-runner` [P2]: **VÁ HỜ**. R2 đã sửa A1 giữ **≤25,00**, rút yêu cầu nới theo phương sai ở `chua_do_duoc` #3 và nêu nợ `NHIEU-RUNNER-CHUA-TACH-KHOI-TAI`. Tự đo đúng **5 master/push + 6 nhánh**, **1×39 + 10×40** bước. Nhưng GATE:97,195 còn gọi mười một/mọi lượt master; Issue #463:13,33–36 vẫn ghi run cancelled trên master và suy biên độ là nhiễu làm A1 không đáng tin. Issue:61–62 còn nói revision chưa làm trong PR này dù :119–125 đã neo r2. Cần đồng bộ phần còn lại, không nới A1.

## BẢNG ĐO

Bảng ghi cả phần khớp, lệch và không đo được. Giây/tỷ lệ chưa làm tròn, từng cặp run và mọi fixture nằm trong `static.json`, `costs.json`, `replay-h.json`, `contract-checks.json`, `followup-checks.json`; metadata từng lệnh có thời điểm, rc, thời lượng và SHA-256 stdout. `0` của `chay_moi` là số mục đỏ, không phải Boolean False.

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| HEAD / tree | exact reviewed_sha | 4d0ead5591a58463423754cc93a84ce744c3a50b / 168f575ffafd05f6a81f3119c33f21fcf4391860 | có |
| Môi trường git | abbrev=7, không shallow, sạch | 7; false; status đầu rỗng | có |
| Diff từ lượt 7 | patch + numstat được giao | 80 tệp; +22338/−65; patch/numstat khớp byte; ngoài ops=0 | có |
| Toàn PR so origin/master | patch + numstat được giao | 162 tệp; +47149/−0; patch/numstat khớp byte; ngoài ops=0 | có |
| Manifest hiện vật lượt 6 / 7 | băm bất biến | 62/62 và 66/66 khớp; không bao quát các tệp ngoài danh sách manifest | có |
| Receipt lượt 7 | v2 / SHA lượt 7 / băm nguyên văn | v2; reviewed_sha=b2ea0f24576275014e8124bfd3e0b6a16c3ca8b5; 45842 B; c3c454a867e859a4214f3574be147d8237ad0f798f21d38cb2763a20252c44c6; cả bytes/hash khớp | có |
| Spec–Issue–lease #463 | bda86f128c220b868e9c103c919d213d8aba5ed1753962b0898ea1ce1852812c | băm blob/spec/tai-lieu=bda86f128c220b868e9c103c919d213d8aba5ed1753962b0898ea1ce1852812c; revision=2; số đường write set=2; null=0 | có |
| Spec–Issue–lease #464 | 4db18266746e220b5745a341faa1307a105b1ace457e31c6af5dcf461d3c86ae | băm blob/spec/tai-lieu=4db18266746e220b5745a341faa1307a105b1ace457e31c6af5dcf461d3c86ae; revision=1; số đường write set=1; null=5 | có |
| Spec–Issue–lease #465 | 2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759 | băm blob/spec/tai-lieu=2abace8588ec2b4e0626c1c77e9c3e0f7e713ecb2ce528b149e6c7f1f0000759; revision=1; số đường write set=2; null=5 | có |
| Spec–Issue–lease #466 | 417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521 | băm blob/spec/tai-lieu=417dce16227687cbb1e642284f39d2f847a617b2d730f7f52aaa58f33c936521; revision=1; số đường write set=2; null=5 | có |
| Lease r2: 3 neo | head master lúc cấp | 3/3=d28c4b1062e8505cbdaaf0237fcbe3f9b8ee4705 | khớp snapshot; GitHub đúng giây cấp KHÔNG ĐO ĐƯỢC |
| Lease r2: write_set_hash | sort + LF + LF cuối | 0f7b869da648e9b21023e461925efd0d45bca58fb308a8fcc82bc55ad9f66ef0 | có |
| Lease r2: hạn / heartbeat | 24 giờ; heartbeat=mốc cấp | cấp/heartbeat=2026-09-07T07:50:35Z; until=expires=2026-09-08T07:50:35Z; 1440 phút | có |
| Lease r2: authority / replacement | revision2 + comment URL + thay exec-1 | granted_on_instruction=URL comment #463/5567157629; thay_the_cho=[exec-1]; exec-1.da_bi_thay_the=exec-1r2 | có trong hồ sơ; comment trực tiếp KHÔNG ĐO ĐƯỢC |
| Chuỗi ba lease trên cây PR | hai chiều #456→exec-1→exec-1r2 | cả 2 cạnh có bia mộ đối xứng; exec-1 bị thay; chỉ r2 giữ ci.yml; chú thích lịch sử không thay key YAML | có |
| Snapshot mọi ref cục bộ | registry2; ci.yml1 | 86 cặp blob/path; #456 có 2 blob, chỉ 1 bia mộ; ci.yml=1, registry=2, subagent=0, nhanh=0 | có |
| Blob #456 trên master | chưa bia mộ | 8b2103c06687546379a17f6deafc97f1fe0173fd; bằng blob cũ được scanner ghi trước ở ref GATE | có |
| Hết hạn #456 | 14:30:07Z | 14:30:06Z registry=2; 14:30:07Z registry=1 | khớp mô phỏng, chưa phải readback tương lai |
| Thu hồi mọi bản #456 | cần mọi ref hết giữ bản còn hạn | mô hình bia mộ mọi bản: registry2→1; chỉ sửa bản PR đã có bia mộ thì vẫn2 | có; không sửa ref |
| Nguồn A1/A5 | 13 run / 26 job / 1140 bước | đúng; job.tsv14 cột, buoc.tsv9 cột; 1140/1140 số giây khớp timestamp; 4 đầu ra tái sinh khớp byte | có |
| 11 run / workload | 5 master+6 nhánh; 1×39+10×40 bước | đúng theo metadata và YAML của 11 head | có; câu cũ còn mâu thuẫn |
| Thống kê 11 job Windows | n11; 40,20–50,48; median46,02; mean45,84; biên10,28 | n=11; min=40.2000000000; max=50.4833333333; median=46.0166666667; mean=45.8378787879; biên=10.2833333333; biên trần60=19,80→9,5166666667 phút | có |
| Hệ số test registry (n/min/max/median/dải) | 11 / 1,07 / 1,71 / 1,21 / 1,21–1,21 | n=11; min=1.06795017; max=1.70708661; median=1.21254355; mean=1.24990421; biên=0.63913644; dải median=1.21125943–1.21382917 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Hệ số tl selftest (n/min/max/median/dải) | 11 / 1,41 / 2,26 / 1,83 / 1,82–1,84 | n=11; min=1.40540541; max=2.25773196; median=1.83050847; mean=1.83149640; biên=0.85232655; dải median=1.81856540–1.84255319 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Hệ số packet-loop selftest (n/min/max/median/dải) | 11 / 1,88 / 2,89 / 2,37 / 2,36–2,38 | n=11; min=1.87755102; max=2.89385475; median=2.36929461; mean=2.36548470; biên=1.01630373; dải median=2.36231884–2.37629938 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Hệ số G5 kiem ban ke (n/min/max/median/dải) | 11 / 1,91 / 3,09 / 2,40 / 2,37–2,43 | n=11; min=1.91379310; max=3.09302326; median=2.39655172; mean=2.44731157; biên=1.17923015; dải median=2.36752137–2.42608696 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Hệ số lease-publish selftest (n/min/max/median/dải) | 11 / 2,42 / 3,84 / 2,94 / 2,91–2,97 | n=11; min=2.41666667; max=3.84313725; median=2.94202899; mean=2.93815245; biên=1.42647059; dải median=2.91366906–2.97080292 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Hệ số bien-nhan v2 selftest (n/min/max/median/dải) | 10 / 7,07 / 9,74 / 7,79 / 7,71–7,88 | n=10; min=7.06666667; max=9.74468085; median=7.79292929; mean=8.10748349; biên=2.67801418; dải median=7.70517771–7.88248634 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Hệ số job trọn (n/min/max/median/dải) | 11 / 1,52 / 2,36 / 1,73 / — | n=11; min=1.52378049; max=2.35828025; median=1.72670419; mean=1.77980484; biên=0.83449977; dải median=1.72585183–1.72755708 | có; job không khai dải nên dải job chỉ là tính bổ sung |
| Toàn bảng hệ số r2 | 7 dòng + dải | 28/28 ô n/min/max/median + 12/12 đầu dải khớp định dạng làm tròn | có |
| Run 34068433781 / 8ce02fd | bảng 11 run | master / push; YAML 40 bước; Windows 2412s = 40.20000000 phút | có |
| Run 34058508426 / 82e01a4 | bảng 11 run | claude/priceless-volhard-329577 / pull_request; YAML 40 bước; Windows 2499s = 41.65000000 phút | có |
| Run 34048685345 / 1b3caa1 | bảng 11 run | master / push; YAML 39 bước; Windows 2537s = 42.28333333 phút | có |
| Run 34052910676 / c0f18ac | bảng 11 run | claude/tra-luat-process-review-o4d7kb / pull_request; YAML 40 bước; Windows 2630s = 43.83333333 phút | có |
| Run 34060879398 / 28cb898 | bảng 11 run | master / push; YAML 40 bước; Windows 2735s = 45.58333333 phút | có |
| Run 34049592719 / b912e5f | bảng 11 run | claude/tra-luat-process-review-o4d7kb / pull_request; YAML 40 bước; Windows 2761s = 46.01666667 phút | có |
| Run 34055467808 / cacaba3 | bảng 11 run | master / push; YAML 40 bước; Windows 2831s = 47.18333333 phút | có |
| Run 34074288203 / d28c4b1 | bảng 11 run | master / push; YAML 40 bước; Windows 2880s = 48.00000000 phút | có |
| Run 34062997697 / 62a6385 | bảng 11 run | claude/tra-luat-process-review-o4d7kb / workflow_dispatch; YAML 40 bước; Windows 2962s = 49.36666667 phút | có |
| Run 34065779670 / 771c6ed | bảng 11 run | claude/tra-luat-process-review-o4d7kb / workflow_dispatch; YAML 40 bước; Windows 2977s = 49.61666667 phút | có |
| Run 34070122978 / 0c3405f | bảng 11 run | claude/tra-luat-process-review-o4d7kb / workflow_dispatch; YAML 40 bước; Windows 3029s = 50.48333333 phút | có |
| Run cancelled34048229370 | r2: nhánh, không master | 4cd80c5; claude/tra-luat-process-review-o4d7kb; workflow_dispatch; windows cancelled; 3610s=60,1666666667ph | có ở spec r2; Issue còn sai nhãn master |
| Chi phí run nhánh34045664423 / ubuntu | phân rã lịch sử làm nền ước | job=24.25000000; step_sum=24.20000000; setup=1.18333333; registry=13.13333333; packet=3.65000000; remaining=7.41666667; split_registry=14.31666667; split_packet=4.83333333; total_after=26.56666667 phút | khớp giây nguồn; các ô dự toán dùng số phút đã làm tròn |
| Chi phí run nhánh34045664423 / windows | phân rã lịch sử làm nền ước | job=43.20000000; step_sum=43.16666667; setup=3.33333333; registry=17.70000000; packet=9.70000000; remaining=15.76666667; split_registry=21.03333333; split_packet=13.03333333; total_after=49.83333333 phút | khớp giây nguồn; các ô dự toán dùng số phút đã làm tròn |
| 43,20→21,03 và giữ chữ trong r2 | job nhánh → ước sau tách | 43,2; 17,7+3,3333333333=21,0333333333; không dùng tập 11 run để sinh hai số này | có; không mâu thuẫn 5 master+6 nhánh |
| Billing A5 | 110,65→126,22; +15,57/+14,1% | 110,65 từ giây gốc; 126,22 từ các ô phút đã làm tròn theo chú thích; từ giây gốc126,2333333333 | có theo cách tính công khai; không coi 0,0133333333 là finding |
| Ngưỡng A1/A5 | ≤25,00 / ≤135,00 | giữ đúng cả hai; sửa câu phân loại mẫu trong bộ nhớ không đổi ngưỡng hoặc số43,20/21,03 | có |
| A2 cùng độ phủ | tập phải bằng trước tách | A2 cũ=86 bộ ba; lease base/tách đủ=88; delta2 receipt-v2, không mất bộ ba nào | KHÔNG; finding P1 mới |
| A2 phản mô hình | không mất bước | tách đủ: M2=True/A2=False; bỏ receipt-v2: A2 cũ=True; nền cùng lease: tách đủ=True, bỏ bước=False | chứng minh mâu thuẫn riêng A2; không khai toàn bộ gate bị vượt |
| Consumer / H layout | 8 SPAN giữ nguyên; 2 dạng Windows | consumer tai-lieu bằng byte cây; 8/8 SPAN giữ nguyên; cả 8 MOI đổi kiểu; 2 dạng Windows đúng thứ tự | có |
| Hai khối H | băm spec bằng harness | TONG=c23bcd019182023496cb3d9817c6553a0074c77bca26c0a0d1f71a4f5104e45c; predicate=bde441a08d129a962d862fe237003997610238edc8e87b7948d35de875e5f165 | có |
| Corpus H | 1213/0/0/0 | 1213/0 đỏ giả/0 bỏ sót/0 ngoại lệ; cases/summary khớp byte; 3/3 script nguyên byte rc0 | có |
| Phân rã corpus | bộ độc lập lượt 6 | bare-span=10; canonical=8; duplicate=100; exhaustive=625; grammar-equivalent=40; grammar-hole=33; old-law7=8; pair=91; prose=288; windows=10 | có |
| Mutant no_positions | 5/51/42/0 đổi màu theo thứ tự | đổi màu=5; ngoại lệ=11; ngoại lệ không tính là răng | có |
| Mutant no_unique | 5/51/42/0 đổi màu theo thứ tự | đổi màu=51; ngoại lệ=0; ngoại lệ không tính là răng | có |
| Mutant no_positive | 5/51/42/0 đổi màu theo thứ tự | đổi màu=42; ngoại lệ=0; ngoại lệ không tính là răng | có |
| Mutant remove_dead_bool | 5/51/42/0 đổi màu theo thứ tự | đổi màu=0; ngoại lệ=0; ngoại lệ không tính là răng | có |
| Đ2 .claude/dev/chon_reviewer_test.py | stdout có rc0 trong hồ sơ | 2765 B; sha256=a58070829bf0732f81f9e4fa601196637467cea0528ed7e362ed8da48a82ede7; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 .claude/dev/gh_readback_test.py | stdout có rc0 trong hồ sơ | 40 B; sha256=0a476a97ea3c334220ff9bee8485d720a8ab62acc17eb1e4a59e3d33c67f2cc2; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 .claude/dev/mcp_gh_test.py | stdout có rc0 trong hồ sơ | 2260 B; sha256=87349f553be22fa00992f3651963f850a12633b522efe19b2e0350d4cfc19340; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 .claude/dev/mcp_github_doc_test.py | stdout có rc0 trong hồ sơ | 55 B; sha256=82f89e9d5170cc190c941b9b5e247c69623d98f135217d8c8495c806074f033b; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 .claude/dev/probe_mang_test.py | stdout có rc0 trong hồ sơ | 497 B; sha256=c9997dac6d36e60d76b48d5b71e1b87fd60f0c387682061d09382d0585fd54a1; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 .claude/hooks/pretooluse_guard_test.py | stdout có rc0 trong hồ sơ | 9995 B; sha256=69878c4f9efb24a6666d1cf0e4dea99d1ac87fa0aa904e28c6d397fd08cb7991; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 .claude/hooks/subagent_ghi_detect_test.py | stdout có rc0 trong hồ sơ | 8340 B; sha256=56f4f998bed4b71e294e8d159fc624e6313d5102778838778d097a6d45026573; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 ops/nhanh_don_duoc_test.py | stdout có rc0 trong hồ sơ | 491 B; sha256=366795e45727a70aa7e6ed4ee64c6a1f0bd952dc1191b901c5d40479c722ad96; rc ghi=0; BASE/H=0/0 | có; replay |
| Đ2 tổng | 8/8 bản xanh | rc0 theo hồ sơ8/8; H bác0/8; hai bản bổ sung khớp bytes/hash riêng; không tự tạo rc0 | có |
| D9 pre-ca | 5000 chữ số ở CA hoặc mutant | BASE=ValueError; H=ValueError; fixture nguyên byte tại replay-h.json | có |
| D9 pre-mutant | 5000 chữ số ở CA hoặc mutant | BASE=0; H=ValueError; fixture nguyên byte tại replay-h.json | có |
| D9 mcp-ca | 5000 chữ số ở CA hoặc mutant | BASE=ValueError; H=ValueError; fixture nguyên byte tại replay-h.json | có |
| D9 mcp-mutant | 5000 chữ số ở CA hoặc mutant | BASE=0; H=ValueError; fixture nguyên byte tại replay-h.json | có |
| Quyết định §12 / nháp LO | chủ kho chọn1, khi cấp neo comment | cùng URL #464/5567158069 ở3/3; lựa chọn1 ở3/3; granted_on_instruction vẫn null; 2 câu phủ định cũ còn lại | chưa nhất quán; không coi nháp chưa cấp là lỗi |
| Cổng doctrine-scan | EVIDENCE rc0 | rc=0; 0.245s; 69 B stdout; 7 tệp; 0 chỗ chép | có |
| Cổng adr-song | EVIDENCE rc0 | rc=0; 0.110s; 113 B stdout; 46/46; ngoại lệ ADR0016 | có |
| Cổng doc-claims | EVIDENCE rc0 | rc=0; 3.488s; 70861 B stdout; ok=true;106 tệp;advisory=367 | có |
| Cổng ci-dang-ky | EVIDENCE rc0 | rc=0; 0.239s; 2934 B stdout; PHẢN CHỨNG51/51;TỔNG ĐẠT | có |
| Cổng bien-nhan-v2 | EVIDENCE rc0 | rc=0; 1.050s; 163 B stdout; 22 v2;11/11 miễn legacy;42 nợ;0 vi phạm;0 KHÔNG ĐO ĐƯỢC;tổng75 | có |
| Cổng lease-check | EVIDENCE rc0 | rc=0; 0.853s; 235 B stdout; ĐĂNG ĐƯỢC;không chạy kiểm GitHub | có |
| Cổng lease-publish-test | EVIDENCE rc0 | rc=0; 65.584s; 8649 B stdout; 121/121;đã chạy121,bỏ qua0 | có |
| Ruff suite pretooluse / Python D9 | Ruff0.15.15; không đổi int limit | PATH=/usr/local/bin:$PATH; ruff --version=0.15.15; Python3.11.15; int limit4300 | có |
| Suite pretooluse tự chạy | xanh và băm khớp bản9995B | start=2026-09-07T09:27:45.642641+00:00; end=2026-09-07T09:39:03.415140+00:00; rc=0; 677.772s; 9995B; sha256=69878c4f9efb24a6666d1cf0e4dea99d1ac87fa0aa904e28c6d397fd08cb7991 | có |
| Replay stdout suite vừa chạy | khớp bản xanh đã giao | rc0; CA39/39; mutant34/34; 9995B trùng từng byte; BASE/H=0/0 | có |

Đối chiếu riêng các điều kiện chuyển hướng H trong LO-319:

| khẳng định | PR khai | đo được | khớp? |
|---|---|---|---|
| Đ1 | ≥1 phản chứng ngoài ranh giới ⇒ dừng H | Không tìm thấy trên corpus1213 đã tái lập; D9 thuộc ranh giới công khai | chưa chạm ngưỡng; không tuyên bố chứng minh mọi đầu vào |
| Đ2 | ≥1 bản formatter xanh bị H bác ⇒ dừng H | H bác0/8 stdout có rc0 trong hồ sơ; bytes/hash pretooluse mới khớp | chưa chạm ngưỡng; A6 của phiên thi công vẫn phải chạy |
| Đ3 | formatter/packet hiện có cần metadata n/m trên tổng ⇒ revision | 8 bản xanh và bốn packet được giao không cung cấp nhu cầu này; grammar vẫn công khai bác schema1/2 | chưa thấy kích hoạt trong phạm vi; không suy toàn bộ packet máy chủ |
| Đ4 | additions runtime>300 ⇒ dừng | diff ci_dang_ky_test.py của PR này rỗng, additions0; H chưa thi công | implementation tương lai KHÔNG ĐO ĐƯỢC, không đóng Đ4 |
| Đ5 | sau thi công phải N/N, N≥51+số ca mới | consumer hiện tại chạy51/51; đây là BASE, không phải bộ phản chứng H sau thi công | KHÔNG ĐO ĐƯỢC nghiệm thu tương lai, không lấy51/51 thay nó |

### bia-mo-mot-ref-khong-thu-hoi-moi-ban  [P1]  Blob lease #456 còn hạn trên master vẫn giữ registry

TỆP/DÒNG: `ops/leases/mutant-khong-chay-tren-windows-exec-1-claude-20260906.yaml:39` trên `origin/master` (blob `8b2103c06687546379a17f6deafc97f1fe0173fd`); bản có bia mộ trong cây PR; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:108–115`; `ops/leases/gate-tach-job-cat-chi-phi-exec-1r2-claude-20260906.yaml:120–126`.

VẤN ĐỀ: Chuỗi #456→exec-1→exec-1r2 trên cây PR đúng hai chiều nhưng scanner đếm từng `(blob,path)` trên mọi ref. Bản #456 chưa bia mộ trên master còn hạn tới14:30:07Z, cùng exec-1r2 giữ `ci_dang_ky_test.py`. Lời khai đã sửa đúng rằng phải đo lại mọi ref sau merge, nhưng trạng thái cần đóng vẫn chưa đạt ở lượt này. Không gọi đây là lỗi rig hay suy từ nhánh GATE cục bộ rằng master đã hết giữ.

ĐÃ THỬ VÁ: thử mô hình đánh bia mộ **mọi** bản #456 trong bộ nhớ → registry2→1; không sửa ref/lease thật. Hai hướng executor có thể kiểm: chờ hết hạn rồi fetch đủ ref/readback, hoặc làm thủ tục thu hồi có thẩm quyền trên mọi ref đang giữ blob cũ. Ca khoá: một bản mới có bia mộ + một bản cũ còn hạn phải vẫn đếm2; mọi bản bị thu hồi hoặc hết hạn thì đếm1 (chỉ r2). Rủi ro: cập nhật riêng master nhưng còn ref khác sẽ tái tạo cửa sổ hai writer. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/static_checks.py` và `followup_checks.py`, rc0; dùng `_quet_lease_toan_kho(..., doi_chieu_ref=False)`, `_phan_loai_lease`, `_bia_mo_doi_xung` thật. Registry2 ở09:21/09:30Z; mô phỏng14:30:06Z→14:30:07Z cho2→1. `git rev-parse origin/master:ops/leases/<id>.yaml` xác nhận blob cũ trên master. Tắt đối chiếu ref máy chủ chỉ để đo snapshot được giao, không dùng số này để chứng nhận toàn bộ GitHub; `check` rc0 không thay kiểm chồng lấn.

ĐỘ TIN: cao với snapshot và mô phỏng; trạng thái GitHub trực tiếp KHÔNG ĐO ĐƯỢC.

### a2-neo-nen-cu-trai-write-set-hien-tai  [P1]  A2 dùng nền 39 bước trái lease hiện tại 40 bước

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:433`, `:457–462`, đối chiếu thông tin r2 ở`:121–123`; `ops/leases/gate-tach-job-cat-chi-phi-exec-1r2-claude-20260906.yaml:81–83`.

VẤN ĐỀ: A2 vẫn bắt buộc so với run34048685345/head1b3caa1 trong khi lease neo d28c4b1. Nền lease đã thêm `bien-nhan v2 selftest`, có40 bước YAML thay vì39. Ngay cả trong trường hợp lý tưởng mọi conclusion giữ nguyên, tách đúng theo M2 cho88 bộ ba còn nền A2 chỉ86. Xoá receipt-v2 trên hai nền lại khớp A2 cũ dù mất độ phủ. R2 đã biết39/40 nhưng chưa cập nhật phép so nghiệm thu; executor không thể vừa giữ đủ bước hiện tại vừa đạt nền cũ. Đây là mâu thuẫn hợp đồng và lỗ của **riêng phép so A2**, không tuyên bố đã vượt toàn bộ các tiêu chí khác.

ĐÃ THỬ VÁ: thử đổi nền phép so sang đúng lease base trong mô hình ngoài checkout: tách đủ bước qua, bỏ receipt-v2 bị bác. Cần sửa A2 để lấy baseline thực sự trước tách tại exact base, cùng event/lane/ma trận như lượt sau; lưu hai bộ dữ liệu nguyên vẹn. Không miễn riêng receipt-v2, không đổi so tập thành số đếm. Ca khoá: một baseline đã có bước mới, dời job đủ bước phải qua; xoá bất kỳ bước/bộ ba phải đỏ. Rủi ro: chỉ đổi SHA nhưng giữ phép so dispatch-nhánh với push-master còn tạo delta `success/skipped` do lane; phải ghim cả ngữ cảnh chạy. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/contract_checks.py`, rc0, phần`a2`. Từ TSV, dời hai bước nặng và nhân9 bước thiết lập2–10; bỏ cột job đúng A2: M2=True, A2 cũ=False, thêm đúng2 bộ ba receipt-v2 và không mất mục nào. Bỏ receipt-v2 → A2 cũ=True, so cùng base=False. `git show` xác nhận39→40 bước. Mô hình không thay `ci.yml`, không thực thi CI mới, không giả lập rằng GitHub đã chạy. Finding không nằm trong bảng cổng EVIDENCE; nó được phát hiện khi kiểm sự nhất quán giữa revision2 và phần nghiệm thu giữ lại.

ĐỘ TIN: cao.

### bien-do-khac-head-khong-phai-nhieu-runner  [P2]  Revision 2 chưa gỡ hết lời khai master và suy luận nhiễu cũ

TỆP/DÒNG: `ops/specs/GATE-TACH-JOB-CAT-CHI-PHI.md:95–97`, `:195–196`, so với`:121–133`, `:612–618`; `ops/issues/463-GATE-TACH-JOB-CAT-CHI-PHI.md:13`, `:33–36`, `:61–65`, so với`:119–125`.

VẤN ĐỀ: Phần đã sửa nói đúng5 master+6 nhánh và rút quyền nới A1; phần còn lại vẫn khẳng định mười một/mọi lượt master. Issue vẫn lấy10,28 làm “nhiễu” và hệ quả cứng cho A1, còn gọi run cancelled là master dù metadata là workflow_dispatch trên nhánh. Issue đồng thời nói revision “chưa làm ở PR này” và đóng băng revision2 phía dưới. Bảng tỷ lệ r2 đã đúng, và các số43,20/21,03 là run nhánh riêng nên **không** phải lỗi; lỗi là hai cách mô tả mẫu và trạng thái revision cùng còn hiệu lực.

ĐÃ THỬ VÁ: tính lại đầy đủ từ giây và thử thay các câu master/pending-revision trong bộ nhớ; các câu cũ mất, A1≤25/A5≤135 và43,20/21,03 được giữ. Cần đồng bộ các đoạn dẫn/Issue thành mô tả đúng mẫu và r2 đã cấp; nếu giữ bảng cũ làm lịch sử thì ghi rõ revision1 ở ngay bảng và không dùng7,56 như kết luận hiện hành. Ca khoá: danh sách11 run phải ánh xạ5/6; run cancelled phải là nhánh; mọi đoạn nghiệm thu giữ cùng ngưỡng; không câu hiện hành nào gọi mẫu này là mọi lượt master hoặc suy jitter thuần. Rủi ro: sửa riêng tiêu đề hoặc trung vị lại bỏ sót bản chiếu, hoặc vô tình đổi ngưỡng để ép xanh. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/measure_costs.py` và `followup_checks.py`, rc0. YAML11head=1×39+10×40; metadata=5master/push+6nhánh; biên10.28333333phút là range, chưa đo được phương sai runner cùng head/tập bước/event. Ba câu stale cụ thể hiện diện3/3; hướng thay trong bộ nhớ gỡ3/3 và giữ các ngưỡng. Cổng doc-claims vẫn xanh367advisory, nên không thay thế đối chiếu này.

ĐỘ TIN: cao về mâu thuẫn nội bộ; không suy nguyên nhân biến động runner.

### quyet-dinh-tiep-h-con-bi-phu-dinh  [P2]  Quyết định chọn H mới vẫn bị câu cũ phủ định

TỆP/DÒNG: `ops/specs/LO-319-LINUX-BANG-CHUNG-XANH.md:255–260`; `ops/leases/lo-319-linux-bang-chung-xanh-exec-1-claude-20260906.yaml.nhap:28`, `:119–123`; bản chọn nhất quán ở`ops/issues/464-LO-319-LINUX-BANG-CHUNG-XANH.md:53`.

VẤN ĐỀ: LO/Issue ghi chủ kho chọn1—tiếp H, ghi chú lease neo cùng comment. Nhưng ngay dưới quyết định LO vẫn đặt tiêu đề H “CHƯA được chọn”, và thân`ly_do_cap` của lease nói “Spec KHÔNG khai §12 đã xong” rồi để ba lựa chọn cho chủ kho quyết. Trạng thái quyết định chưa được đồng bộ giữa phần mới và phần cũ. Không coi5ônull của lease nháp là lỗi: chọn thiết kế không tự cấp lease và không miễn Đ1–Đ5.

ĐÃ THỬ VÁ: thử gỡ hai câu phủ định trong bộ nhớ, giữ URL và`granted_on_instruction=null`. Executor cần đồng bộ trọn đoạn lý do/tiêu đề thành quyết định thiết kế đã có, thi công chưa bắt đầu, lease chưa cấp và Đ1–Đ5 tiếp tục ràng buộc; phần ba lựa chọn nếu giữ phải gắn lịch sử. Ca khoá: cùng URL/lựa chọn ở ba hồ sơ, không còn câu hiện hành nói chưa chọn; null của nháp vẫn null. Rủi ro: sửa thành “đã cấp” hoặc “mọi điều kiện đã đạt” sẽ tạo authority hoặc evidence không có. **chưa chạy trên cây thật — executor tự áp, tự đo, tự chịu trách nhiệm commit**.

ĐÃ THỬ NGHIỆM: `python3 -B do-review8/contract_checks.py`, rc0, phần`h_decision`: URL/lựa chọn3/3, còn2câu phủ định; hướng thay gỡ2/2 và giữ URL/null. Quyền và nội dung comment GitHub trực tiếp KHÔNG ĐO ĐƯỢC theo phạm vi offline.

ĐỘ TIN: cao về mâu thuẫn văn bản; không chứng nhận độc lập comment chủ kho.

## Giới hạn và bàn giao

**KHÔNG ĐO ĐƯỢC:** GitHub trực tiếp/tính đầy đủ mọi ref máy chủ; master đúng giây cấp r2; quyền và nội dung gốc hai comment chủ kho; branch protection; Windows thật; hóa đơn và runner jitter; dữ liệu lịch sử2062hàng/19jobUbuntu, corpus311/419 và provenance đã rút; Đ4/Đ5 của implementation H tương lai. Không mục nào được đổi thành pass. Không chạy`packet_loop_test` hoặc toàn bộ`ci_dang_ky --chay` trên PR thuần hồ sơ này.

Tái lập môi trường: `core.abbrev=7`; dùng nguyên script lượt6 nhưng **chép sang layout riêng ở `do-review8/rig/`**, symlink chỉ hướng vào cây đọc/tài liệu; không đặt vòng symlink trong checkout. Test lease121/121 chạy xanh ngay. Lượt pretooluse đầu không thu được metadata/stdout hoàn tất, không dùng làm bằng chứng; lượt chạy lại có session được chờ để lấy rc thật. Không gán trục trặc thu hiện vật của reviewer cho PR.

Hiện vật chính: `do-review8/replay-h.json` và`rig/do-review/` (corpus, H trích, mutant); `costs.json`/`nen-a1-a5/` (mọi cặp giây và bảng tái sinh); `static.json` (băm, receipt, snapshot, mô phỏng hết hạn); `contract-checks.json` (phản mô hình A2 và trạng thái §12); `followup-checks.json` (master blob, mô hình thu hồi mọi bản, thử sửa câu stale); stdout/stderr/metadata các cổng. Hướng sửa là gợi ý dữ liệu có giới hạn, không phải quyền ghi branch hay duyệt self-review.

Kiểm cuối: HEAD=4d0ead5591a58463423754cc93a84ce744c3a50b; tree=168f575ffafd05f6a81f3119c33f21fcf4391860; tracked diff rỗng=True; status rỗng=True; commits sau reviewed_sha=0.

verdict: changes_requested
