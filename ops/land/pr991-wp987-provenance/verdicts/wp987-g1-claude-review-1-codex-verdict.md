verdict: blocked
reviewed_sha: a2e2ebf812f57254affe9344fd02530efa1a0130

Kết luận: `blocked` do chưa chạy được mẫu PowerShell trên runtime thật theo yêu cầu
đo của lượt này: môi trường không có `pwsh`/`powershell`; tải runtime thất bại ở kết
nối proxy. Chưa phát hiện lỗi P0/P1/P2 trong phần đã đo. Launcher/Python, N1–N3 và
selftest offline exact SHA đều đạt. Thiếu runtime chưa phải finding lỗi cú pháp.

HEAD: `a2e2ebf812f57254affe9344fd02530efa1a0130`.
Tree: `427c0775c0f1b4f5fdadaf10c6e65bc23d4182aa`.
Base: `20a2e2b3dd52a83442c739d17db1f1bd66181a6c`.
SPEC sha256: `9403038447154f1e2e714c40fa8561460a2bac08e8a06708923a5541a5047b15`.
Packet `wp987 r1 g1`, review class `sensitive`; áp ngưỡng không còn P0/P1/P2.
Review offline theo chỉ thị trực tiếp; verdict không tự cập nhật assurance/state/CI.
Mọi hiện vật thử nằm ngoài `cay-kho/`; không gọi model thật trong các phép thử.
Reviewer: `provider=openai_codex`, `execution_surface=codex_cli`, `transport=machine`,
run `da438d8f0baa413586eff0a65f9e6fa2`, theo `runs/da438d8f/run.json` của chính lượt này.
Sổ hiện `dang_chay`, chưa có các trường đo model/effort cuối lượt; không suy chúng từ
cấu hình hoặc actor. Context review độc lập với Executor được giao trong prompt.
Sandbox phiên cho phép workspace-write; checkout ứng viên được đối xử read-only.

## BẢNG SĂN

HƯỚNG 1: Phạm vi, SPEC, adapter mỏng và lịch sử
  giả thuyết : Có sửa ngoài write set, quá trần, chép protocol hoặc mất câu r368.
  lệnh       : sha256sum SPEC.md; git -C cay-kho diff --numstat 20a2e2b HEAD;
               git -C cay-kho diff --check 20a2e2b HEAD;
               python .claude/dev/packet_loop.py doctrine-scan --root . (cwd=cay-kho);
               so bytes đoạn r368 ở base/head bằng git show và Python.
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
  giả thuyết : Pipeline gán biến sai cú pháp hoặc $Run.<property> không khớp JSON thật.
  lệnh       : pwsh -NoLogo -NoProfile -File review-evidence/powershell-check.ps1
               -RunJson /tmp/wp987-r1-review-*/run-measured.json
               (đường dẫn cụ thể trong review-evidence/powershell-availability.log).
  output     : pwsh=None; powershell=None; dotnet=None;
               not_run: FileNotFoundError: [Errno 2] No such file or directory: 'pwsh';
               tải PowerShell 7.4.6 từ release chính thức: curl rc=7,
               "Failed to connect to 127.0.0.1 port 45221 ... Couldn't connect to server".
               Đối chiếu tĩnh: "$Run = Get-Content -Raw -LiteralPath $RunJson | ConvertFrom-Json";
               ba property model_phuc_vu/effort_phuc_vu/sandbox_quan_sat khớp writer thật.
  kết luận   : KHÔNG ĐO ĐƯỢC phần thực thi PowerShell; không coi đối chiếu tĩnh là runtime pass.

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
| M2: các property PowerShell tương ứng M1 | Tên khớp JSON do writer ghi; runtime chưa có | Một phần; chưa đạt kiểm chạy PowerShell |
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

- N1: `passed`; doctrine-scan rc=0, diff --check rc=0.
- N2: `passed`; đủ chín trường, lệnh và output thật trong [schema-scope.log](review-evidence/schema-scope.log).
- N3: `passed`; ba dòng còn lại và lý do giữ ở HƯỚNG 6;
  output nguyên văn trong [gates.log](review-evidence/gates.log).
- Phép đo riêng: 29 mục hành vi `passed` và 1 mục đối chiếu PowerShell tĩnh, script [measure_launcher.py](review-evidence/measure_launcher.py),
  output [measure-launcher.log](review-evidence/measure-launcher.log).
  Mục PowerShell trong log chỉ là đối chiếu tĩnh và thông báo chưa đo, không tính là runtime pass.
- PowerShell: `not_measured`; script tái chạy [powershell-check.ps1](review-evidence/powershell-check.ps1),
  đối chiếu ba fixture bằng `python -B review-evidence/check_powershell.py`
  ([driver](review-evidence/check_powershell.py), [fixture](review-evidence/fixtures/run-measured.json));
  hiện rc=2, `NOT_MEASURED: no pwsh/powershell executable; native execution and parity not checked`.
  Lỗi môi trường trong [powershell-availability.log](review-evidence/powershell-availability.log).
- N4 selftest: `passed`, `python -B scripts/tl.py --selftest`, rc=0,
  `== tl selftest 1731/1731 ==`, transport 12/12, 226 giây.
  Chạy ở clone độc lập `/tmp/wp987-selftest-ppz4l9qc/checkout`, cùng exact SHA/tree trên.
  Setup riêng bản sao: `core.abbrev=7` như nguồn; env của tiến trình selftest đặt
  `commit.gpgsign=false` cho mini-repo fixture; bỏ `TL_SELFTEST_ALLOW_NET` để harness chặn mạng.
  Lần đầu 1727/1731, rc=1: bốn ca r218/r226/r264/r268 lỗi khi thiếu cấu hình SHA ngắn
  và Git fixture gọi signing service localhost bị chặn; đã đo setup đối chứng, không vá mã.
  [Log cuối](review-evidence/selftest.log), [metadata](review-evidence/selftest-meta.json),
  [log đầu](review-evidence/selftest-initial.log), [đối chứng setup](review-evidence/selftest-setup-probe.json).
  Agent `tl_auditor` chạy/tiêu hoá output dài theo `cay-kho/CLAUDE.md`, mục Quy trình sửa code bước 5;
  phiên chính thực hiện review diff và các phép đo launcher/Python.
  CI trên GitHub: `not_run`; review offline này không chứng nhận check run head cuối.
- Snapshot đầu/cuối: cùng 7.259 file ngoài `.git`, cùng hash nội dung/mode,
  HEAD/tree, diff/index và status tracked/untracked/ignored sạch; delta rỗng
  ([kết quả](review-evidence/snapshot-result.json)). Chỉ chứng minh không có delta ở hai mốc;
  không suy toàn bộ lịch sử ghi tệp từ snapshot.

## Findings và phần chặn

Không phát hiện lỗi P0/P1/P2 trong phần đã đo; không yêu cầu sửa candidate dựa trên việc
thiếu công cụ. Phần chặn hiện tại là thiếu bằng chứng thực thi PowerShell theo yêu cầu
đo của lượt review này. Cần chạy script PowerShell trên các fixture cùng đầu vào rồi
đối chiếu kết quả trước khi đổi verdict sang `approve`.
