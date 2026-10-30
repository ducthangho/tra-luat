verdict: approve
reviewed_sha: a2e2ebf812f57254affe9344fd02530efa1a0130

Kết luận lượt 2: `approve` trên exact SHA bên dưới. Không còn P0/P1/P2 và không còn
phần chặn của lượt 1. PowerShell thật 7.4.6 chạy script/fixtures nguyên gốc đạt 3/3;
dòng gán nguyên văn trong adapter và các property được chạy trên `run.json` THẬT,
khớp Python 9/9 trường. N1–N3 được xác nhận lại; selftest 1731/1731 được kế thừa
trên cùng SHA, không chạy lại theo chỉ thị lượt 2. Không phát hiện finding mới.

HEAD: `a2e2ebf812f57254affe9344fd02530efa1a0130`.
Tree: `427c0775c0f1b4f5fdadaf10c6e65bc23d4182aa`.
Base: `20a2e2b3dd52a83442c739d17db1f1bd66181a6c`.
SPEC sha256: `9403038447154f1e2e714c40fa8561460a2bac08e8a06708923a5541a5047b15`.
Packet `wp987 r1 g1`, review class `sensitive`; áp ngưỡng không còn P0/P1/P2.
Review offline theo chỉ thị trực tiếp; verdict không tự cập nhật assurance/state/CI.
Mọi hiện vật thử nằm ngoài `cay-kho/`; không gọi model thật trong các phép thử.
Reviewer lượt 2: `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`,
run `0e1042359a214887bcdedd2cce365dbb`, nguồn `../runs/0e104235/run.json`.
Tại thời điểm ghi verdict, sổ lượt 2 còn `dang_chay`, chưa có các trường đo
model/effort/sandbox cuối lượt; không suy từ cấu hình, actor hoặc sổ lượt 1.
Context review độc lập với Executor được giao trong prompt. Sandbox phiên cho phép
workspace-write; checkout ứng viên được đối xử read-only. Các phép PowerShell chạy
trên Linux với `/usr/local/bin/pwsh` → `/opt/pwsh/pwsh`; không chứng nhận runtime Windows.

## ĐỐI CHIẾU LƯỢT TRƯỚC

Nguồn: [VERDICT-luot1.md](VERDICT-luot1.md), cùng SHA/tree/base ở trên.
Lượt 1 không có finding, nên không có finding để phân loại ĐÃ VÁ THẬT / VÁ HỜ /
VÁ SINH LỖI MỚI / CHƯA VÁ. Số lớp lỗi còn mở: 0; số biểu hiện: 0.

| Mục lượt 1 | Tự kiểm lượt 2 | Kết quả |
| --- | --- | --- |
| HƯỚNG 8: thiếu PowerShell, phần chặn duy nhất | `/opt/pwsh/pwsh -NoLogo -NoProfile -c '$PSVersionTable.PSVersion.ToString()'` → `7.4.6`, rc=0; driver gốc → `POWERSHELL_PARITY 3/3`; đọc property trực tiếp trên sổ thật → 9/9 | ĐÃ GỠ PHẦN CHẶN môi trường; không có bản vá candidate |
| HƯỚNG 1, N1–N3, lịch sử r368 | 2 tệp +17/-11; diff khớp byte với packet; SPEC khớp băm; doctrine-scan sạch 10 tệp; 9 trường đều có; 3 dòng stderr.log vẫn đúng vai trò | Kết luận còn đúng |
| HƯỚNG 2–7 và 9 | 28 hiện vật lượt 1 khớp manifest trước khi chạy; toàn bộ 7.259 file/mode, HEAD/tree, diff/index và status giống snapshot lượt 1 | Kế thừa phép đo lượt 1 trên cùng nội dung; không khai chạy lại |
| N4 selftest | Kiểm log `1731/1731`, transport `12/12`, metadata exact SHA/tree và rc=0; hash log khớp manifest | Kế thừa pass; `not_run` trong lượt 2 theo yêu cầu |

Sổ thật được dùng làm đầu vào đo: `../runs/da438d8f/run.json`, run
`da438d8f0baa413586eff0a65f9e6fa2`, `trang_thai=xong`, `ma_thoat=0`.
Có 74 bản ghi response/model, tất cả `gpt-6.1-sol`; effort `["xhigh"]`;
7 bản ghi quan sát sandbox (`bwrap`, `codex-linux-sandbox`); ba trạng thái đều `DO_DUOC`.
Đây là dữ liệu lượt 1, không phải phép đo model đang phục vụ lượt 2.
SHA-256 sổ trước/sau đều
`55d0826eec9319686bdc9b48a7b821f699f4f46a08487664ba4c3299262df8c1`.
Không sửa sổ, script gốc hoặc fixtures.

## BẢNG SĂN

HƯỚNG 1 và 8 dưới đây đã đo lại trong lượt 2; HƯỚNG 6 được xác nhận lại bằng N3.
Các phép phản chứng HƯỚNG 2–5, 7, 9 là kết quả lượt 1 được giữ rõ nguồn, không chạy lại.
Lệnh/rc/output/hash lượt 2: [commands.json](review-evidence/luot2/commands.json),
[script đo](review-evidence/luot2/run_checks.py).

HƯỚNG 1: Phạm vi, SPEC, adapter mỏng và lịch sử
  giả thuyết : Có sửa ngoài write set, quá trần, chép protocol hoặc mất câu r368.
  lệnh       : python3 -B review-evidence/luot2/run_checks.py;
               script dùng hashlib cho SPEC, git diff --numstat/--check trên base/head đầy đủ,
               python3 -B .claude/dev/packet_loop.py doctrine-scan --root . (cwd=cay-kho),
               git show + Python so bytes đoạn r368; từng argv/rc ở commands.json.
  output     : SPEC khớp băm; .agents +5/-4, .claude +12/-7; tổng 2 tệp, +17/-11;
               diff --check rc=0; doctrine-scan rc=0:
               "doctrine-scan: sạch — đã quét 10 tệp, 0 chỗ chép doctrine";
               đoạn hai dòng bắt đầu "Hồ sơ `r368`" giống nguyên văn ở base/head.
               diff.patch của packet khớp byte với git diff 20a2e2b a2e2ebf.
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 2: Tên trường có thật và kiểu dữ liệu do writer thật ghi
  giả thuyết : Tên khóa/lớp bị đoán hoặc giá trị có nghĩa khác adapter mô tả.
  lệnh       : rg -n -F '<từng tên>' cay-kho/.claude/dev/launcher.py;
               python -B review-evidence/measure_launcher.py
  output     : 9 tên trường đều rg rc=0; model writer tại 1831–1841, sandbox tại 2150–2153;
               _BoLocStderr tại 1794, _LayMauSandbox tại 2015;
               valid_without_header: model_phuc_vu=[{"response_id":"r1","model":"gpt-fixture","su_kien":"response.created"}],
               model_phuc_vu_trang_thai=DO_DUOC, effort_phuc_vu=["xhigh"], effort_phuc_vu_trang_thai=DO_DUOC.
               *_ly_do không có khi thành công; mẫu đọc Python hiển thị null, không ném KeyError.
  kết luận   : KHÔNG PHẢI LỖI

HƯỚNG 3: Có dữ liệu nhưng chưa đủ điều kiện DO_DUOC
  giả thuyết : Adapter coi mảng khác rỗng hoặc cấu hình yêu cầu là đã đo được.
  lệnh       : python -B review-evidence/measure_launcher.py
               (gọi _BoLocStderr.ghi_so, _ket_luan_model, _ket_luan_effort của candidate).
  output     : missing_effort: model=DO_DUOC, effort=["xhigh"] nhưng effort_state=KHONG_DO_DUOC,
               lý do="1 khung khong mang response.reasoning.effort hop le";
               damaged_response_frame: model có bản ghi nhưng model_state=KHONG_DO_DUOC;
               filter_error/pipe_open/frame_lost/frame_unknown/no_frames đều KHONG_DO_DUOC;
               header_without_frames: model/effort đều KHONG_DO_DUOC;
               multiple_models_efforts: hai model, effort=["xhigh","high"].
  kết luận   : KHÔNG PHẢI LỖI — phải xét riêng trạng thái tương ứng từng phép đo.

HƯỚNG 4: Trạng thái sandbox thứ ba, fallback stdout và giới hạn nền
  giả thuyết : Bỏ sót KHONG_THAY_LENH hoặc suy không thấy tiến trình thành đo được.
  lệnh       : python -B review-evidence/measure_launcher.py
               (gọi _LayMauSandbox.ghi_so; gọi _quet thật trên /proc với tiến trình con giả).
  output     : sandbox_no_json=KHONG_DO_DUOC;
               sandbox_no_command=KHONG_THAY_LENH, lý do="stdout khong co command_execution nao";
               sandbox_command_unseen=KHONG_DO_DUOC;
               sandbox_observed=DO_DUOC;
               argv không rõ/lỗi lấy mẫu/luồng còn sống đều KHONG_DO_DUOC;
               nhánh Windows giả lập=KHONG_DO_DUOC, lý do="nen Windows khong do sandbox (chi Linux /proc)";
               actual_linux_proc_sampler: child_stat_read=true, child_cmdline_read=true,
               observed=[{"chuong_trinh":"bwrap","gan":[],"co":[],"so_lan":1}].
  kết luận   : KHÔNG PHẢI LỖI — mẫu bwrap là tiến trình giả để kiểm bộ lấy mẫu;
               phép này không chứng minh cơ chế cô lập hay runtime Windows thật.

HƯỚNG 5: Lệnh Python mẫu chạy được, có đủ chín khóa
  giả thuyết : One-liner hỏng quoting/JSON, thiếu *_ly_do gây crash hoặc rc=0 không in dữ liệu.
  lệnh       : python -B review-evidence/measure_launcher.py
               (trích nguyên khối Bash mới từ adapter, chỉ thay placeholder bằng đường dẫn JSON giả).
  output     : python_example_measured: rc=0, lines=9;
               python_example_not_measured: rc=0, lines=9;
               python_example_missing_fields: rc=0, lines=9;
               cả ba được parse lại và so chính xác với r.get(k) cho từng khóa.
               Fixture ở thư mục /tmp/wp987-r1-review-* ngoài cay-kho/.
  kết luận   : KHÔNG PHẢI LỖI — JSON thiếu trường in null; rc=0 của lệnh đọc không thay trạng thái đo.

HƯỚNG 6: Header cũ còn làm nguồn đo ở phần khác của adapter
  giả thuyết : Mục mới đúng nhưng câu cũ còn dạy đo model/effort từ stderr.log.
  lệnh       : rg -n 'stderr.log' .claude/skills/cross-review/SKILL.md .agents/skills/cross-review/SKILL.md
               (cwd=cay-kho); rg -n 'header|model_phuc_vu|effort_phuc_vu|reasoning effort'
               cay-kho/.claude/skills/cross-review/SKILL.md cay-kho/.agents/skills/cross-review/SKILL.md
  output     : N3 rc=0, chỉ 3 dòng:
               .claude:139 — nêu run.json là nguồn, KHÔNG từ stderr.log;
               .claude:151 — dẫn quan sát wp923 g2 về thiếu header;
               .claude:179 — tail log khi chẩn đoán reconnect/lượt còn chạy, không đo model/effort.
               .agents:68–69 dùng biến $StderrLog và nói rõ header chỉ là lời khai phụ;
               .claude:156–157 là đoạn lịch sử r368 được SPEC yêu cầu giữ.
  kết luận   : KHÔNG PHẢI LỖI — không còn câu hướng dẫn header là nguồn đo trong hai adapter.

HƯỚNG 7: RUST_LOG chỉ là lời mô tả, launcher không đặt thật
  giả thuyết : Trace tùy env bên ngoài hoặc chỉ đặt biến trong tiến trình cha.
  lệnh       : python -B review-evidence/measure_launcher.py
               (gọi lenh_run thật với executable Codex giả ở /tmp, chỉ stub preflight/auth/probe).
  output     : lenh_run_integration_fake_codex: rc=0,
               child_RUST_LOG="tungstenite::protocol=trace", override_recorded=true,
               model_state=DO_DUOC, effort_state=DO_DUOC, stderr_byte=39.
               Env đầu vào thử RUST_LOG="fixture_old=debug"; executable giả không gọi mạng/model.
  kết luận   : KHÔNG PHẢI LỖI — khớp _RUST_LOG_DO_MODEL tại 1596 và lenh_run tại 2284–2292.

HƯỚNG 8: PowerShell và tên thuộc tính của adapter .agents
  giả thuyết : Pipeline gán biến sai cú pháp, property mất kiểu/mảng hoặc không đọc được sổ thật.
  lệnh       : /opt/pwsh/pwsh -NoLogo -NoProfile -c '$PSVersionTable.PSVersion.ToString()';
               python3 -B review-evidence/check_powershell.py;
               pwsh -NoLogo -NoProfile -NonInteractive -File review-evidence/luot2/adapter-exact-real.ps1
                 -RunJson ../runs/da438d8f/run.json;
               pwsh -NoLogo -NoProfile -NonInteractive -File review-evidence/powershell-check.ps1
                 -RunJson ../runs/da438d8f/run.json.
               Script đầu trích nguyên văn dòng gán từ adapter (không viết lại), rồi đọc trực tiếp
               $Run.model_phuc_vu, $Run.effort_phuc_vu, $Run.sandbox_quan_sat,
               ba *_trang_thai và ba *_ly_do; đối chiếu JSON với Python json.loads.
  output     : Tất cả rc=0. Version=7.4.6; which=/usr/local/bin/pwsh → /opt/pwsh/pwsh.
               PASSED measured rc=0 properties=9 parity=exact;
               PASSED not_measured rc=0 properties=9 parity=exact;
               PASSED missing_fields rc=0 properties=9 parity=exact;
               POWERSHELL_PARITY 3/3.
               Sổ thật: xong, ma_thoat=0; 74 model records, models=["gpt-6.1-sol"],
               efforts=["xhigh"], sandbox_records=7; cả ba trạng thái=DO_DUOC.
               Direct-property parity=9/9 exact; original-script real parity=9/9 exact.
               Ba *_ly_do vắng khi đo được được đọc thành null; không lỗi.
               Hash sổ trước/sau bằng nhau; script/fixtures gốc không đổi.
  kết luận   : KHÔNG PHẢI LỖI — đã chạy PowerShell thật trên fixture và sổ launcher thật;
               phần chặn duy nhất của lượt 1 đã được gỡ. Giới hạn: PowerShell/Linux, không đo Windows.

HƯỚNG 9: Cụm "theo từng khung response" bị hiểu thành bộ đếm mọi khung
  giả thuyết : model_phuc_vu là list tên thuần hoặc một phần tử cho mỗi created/completed.
  lệnh       : python -B review-evidence/measure_launcher.py (valid_without_header).
  output     : Hai khung response.created/response.completed cùng response_id+model chỉ cho
               một bản ghi {response_id,model,su_kien}; effort là danh sách giá trị khác nhau.
  kết luận   : KHÔNG PHẢI LỖI về nguồn đo mà diff hướng dẫn; phải hiểu đây là các bản ghi
               lấy từ khung response, được khử trùng theo response_id+model, không là bộ đếm khung/request.

## BẢNG ĐO

| khẳng định trong diff | đo được | khớp? |
| --- | --- | --- |
| M1: nguồn là run.json, header phụ/vắng header không suy chưa đo | Writer thật và ca valid_without_header / header_without_frames | Có |
| M2: các property PowerShell tương ứng M1 | PowerShell 7.4.6: ba fixture 3/3; dòng gán nguyên văn + direct properties và script gốc trên run.json thật đều khớp 9/9 | Có |
| model_phuc_vu | launcher.py:1831, list bản ghi response_id/model/su_kien, khử trùng | Có |
| model_phuc_vu_trang_thai | launcher.py:1832; ca đo được và 5 nhánh không đo được | Có |
| model_phuc_vu_ly_do | launcher.py:1834; lý do ở ca lỗi, vắng khi DO_DUOC | Có |
| effort_phuc_vu | launcher.py:1838; ["xhigh"] và ["xhigh","high"] | Có |
| effort_phuc_vu_trang_thai | launcher.py:1839; model DO_DUOC chưa đủ khi khung thiếu effort | Có |
| effort_phuc_vu_ly_do | launcher.py:1841; lý do thiếu effort/không neo model | Có |
| sandbox_quan_sat | launcher.py:2150; list summary từ mẫu /proc thật và fixture | Có |
| sandbox_trang_thai | launcher.py:2151; DO_DUOC, KHONG_DO_DUOC, KHONG_THAY_LENH | Có |
| sandbox_ly_do | launcher.py:2153; lý do khi không đo được/không thấy lệnh | Có |
| _BoLocStderr.ghi_so, _LayMauSandbox.ghi_so tồn tại đúng chức năng | Gọi trực tiếp cả hai writer trong script đo | Có |
| Chỉ DO_DUOC được tính đo được | Chạy _ket_luan_model, _ket_luan_effort và nhánh ghi sandbox | Có |
| Launcher tự đặt RUST_LOG cho Codex | Tiến trình con giả nhận tungstenite::protocol=trace, đè giá trị cũ | Có |
| Nhận response.created/response.completed của máy chủ | Cả hai loại frame fixture qua parser thật; chưa gọi máy chủ thật | Có về cơ chế mã; không tuyên bố phép đo server live |
| Lấy mẫu /proc, chỉ Linux | Đọc stat/cmdline thật; nhánh không Linux giả lập từ code | Có về mã; không chạy trên Windows thật |
| Không thấy sandbox thì xét stdout --json | Ba ca no JSON / JSON không lệnh / command_execution | Có |
| CLI 0.164 / wp923 g2 stderr.log 39 byte | SPEC đóng băng nêu quan sát; filter/integration tái hiện 39 byte và bỏ header giả | Khớp cơ chế; chưa đo lại hiện vật lịch sử wp923 g2 |
| -m/-c model_reasoning_effort là yêu cầu, không đủ evidence | Chỉ header không có frame => hai trạng thái KHONG_DO_DUOC; parser dùng response.model/reasoning.effort | Có |
| Không phải thống kê modelUsage của Claude | Writer chỉ ghi bản ghi frame và list effort, không thống kê token/modelUsage | Có |
| Lệnh đọc Python | Ba fixture JSON riêng, chín khóa mỗi ca, rc=0 và so giá trị | Có |
| Câu lịch sử r368, write set, <=60 dòng thêm, không chép doctrine | Đối chiếu bytes; 2 tệp/+17; N1 sạch | Có |

## Gate và hiện vật

- N1 lượt 2: `passed`; doctrine-scan rc=0, sạch 10 tệp/0 chỗ chép doctrine;
  [output](review-evidence/luot2/n1-doctrine.stdout.log); diff --check rc=0.
- N2 lượt 2: `passed`; đủ chín trường, từng lệnh `rg -n -F` kèm đường dẫn launcher và rc=0
  trong [commands.json](review-evidence/luot2/commands.json), output `n2-*.stdout.log` cùng thư mục.
  Ngữ nghĩa writer vẫn như [schema-scope.log](review-evidence/schema-scope.log) lượt 1.
- N3 lượt 2: `passed`; `rg -n 'stderr.log' .claude/skills/cross-review/SKILL.md .agents/skills/cross-review/SKILL.md`
  (cwd=cay-kho), rc=0; đúng ba dòng 139/151/179 và lý do giữ ở HƯỚNG 6;
  [output nguyên văn](review-evidence/luot2/n3-stderr.stdout.log).
- Phép đo riêng lượt 1, không chạy lại: 29 mục hành vi `passed` và 1 mục đối chiếu PowerShell tĩnh, script [measure_launcher.py](review-evidence/measure_launcher.py),
  output [measure-launcher.log](review-evidence/measure-launcher.log).
  Mục PowerShell trong log chỉ là đối chiếu tĩnh và thông báo chưa đo, không tính là runtime pass.
- PowerShell lượt 2: `passed`; script gốc [powershell-check.ps1](review-evidence/powershell-check.ps1),
  [driver gốc](review-evidence/check_powershell.py), fixtures gốc đều giữ hash.
  `python3 -B review-evidence/check_powershell.py` rc=0, `POWERSHELL_PARITY 3/3`:
  [log](review-evidence/luot2/powershell-parity.stdout.log).
  [Script trích dòng gán và đọc property](review-evidence/luot2/adapter-exact-real.ps1),
  [output trên sổ thật](review-evidence/luot2/powershell-adapter-real.stdout.log),
  [output script gốc trên sổ thật](review-evidence/luot2/powershell-original-real.stdout.log),
  [tóm tắt/băm đối chiếu](review-evidence/luot2/powershell-real-summary.json).
  Các log `not_measured` của lượt 1 là lịch sử; bản sao log parity cũ được giữ tại
  [prior-powershell-parity.log](review-evidence/luot2/prior-powershell-parity.log).
- N4 selftest: kế thừa `passed` lượt 1; lượt 2 `not_run` theo chỉ thị không cần chạy lại.
  Lượt 1 `python -B scripts/tl.py --selftest`, rc=0,
  `== tl selftest 1731/1731 ==`, transport 12/12, 226 giây.
  Chạy ở clone độc lập `/tmp/wp987-selftest-ppz4l9qc/checkout`, cùng exact SHA/tree trên.
  Setup riêng bản sao: `core.abbrev=7` như nguồn; env của tiến trình selftest đặt
  `commit.gpgsign=false` cho mini-repo fixture; bỏ `TL_SELFTEST_ALLOW_NET` để harness chặn mạng.
  Lần đầu 1727/1731, rc=1: bốn ca r218/r226/r264/r268 lỗi khi thiếu cấu hình SHA ngắn
  và Git fixture gọi signing service localhost bị chặn; đã đo setup đối chứng, không vá mã.
  [Log cuối](review-evidence/selftest.log), [metadata](review-evidence/selftest-meta.json),
  [log đầu](review-evidence/selftest-initial.log), [đối chứng setup](review-evidence/selftest-setup-probe.json).
  Trong lượt 1, agent `tl_auditor` chạy/tiêu hoá output dài theo `cay-kho/CLAUDE.md`,
  mục Quy trình sửa code bước 5; phiên chính lượt 1 review diff và đo launcher/Python.
  CI trên GitHub: `not_run`; review offline này không chứng nhận check run head cuối.
- Snapshot lượt 2 đầu/cuối và snapshot cuối lượt 1 đều giống nhau: 7.259 file ngoài `.git`,
  cùng hash nội dung/mode, HEAD/tree, diff/index và status tracked/untracked/ignored sạch;
  cả hai tập delta rỗng ([kết quả](review-evidence/luot2/snapshot-result.json)).
  Chỉ chứng minh không có delta ở các mốc, không suy toàn bộ lịch sử ghi tệp từ snapshot.
- 28 hiện vật lượt 1 khớp manifest trước khi chạy lại:
  [xác minh](review-evidence/luot2/round1-artifact-validation.json).
  Manifest lượt 1 được giữ nguyên; log PowerShell tái chạy được lưu riêng trong `luot2/`.
  Manifest lượt 2: [artifact-manifest.json](review-evidence/luot2/artifact-manifest.json).

## Findings và phần chặn

Không có finding mới; không có P0/P1/P2 còn mở. Phần chặn PowerShell của lượt 1 đã
được gỡ bằng bằng chứng runtime, fixture parity và đọc sổ launcher thật. Verdict:
`approve` cho `a2e2ebf812f57254affe9344fd02530efa1a0130` trong phạm vi review offline
được giao. CI GitHub vẫn `not_run` trong phiên này như lượt 1; verdict không tự
chứng nhận CI, assurance/state, quyền merge/land/deploy.
