## Chủ kho duyệt ngoại lệ ready — exact H7, không merge

Chủ kho trả lời **“Đồng ý”** cho checkpoint https://github.com/ducthangho/tra-luat/issues/1239#issuecomment-6704355356 trong hội thoại dispatcher, sau câu hỏi xác nhận chỉ bỏ draft khi toàn bộ CI xanh. Dispatcher ghi hộ quyết định; không tự nhận reviewer/human auditor.

Áp dụng duy nhất PR1261, H **`4c319cc4f71b2f9a5c69a4b1be75e1add5f8aeaa`**, tree **`539a02f355c4ade3cee7c99efa327a4a729e79bb`**, canonical **`9607e3eba96b2ce091e34196cbb8ede31a521ff9`**:
- Ngoại lệ M6/K3: không yêu cầu thêm connectorcall trước bỏ draft.
- Dùng independent CLI review đã hoàn tất + quyết định owner_waivedF1/F2 làm đường chấp nhận có chỉ thị chủ kho cho K4 trên candidate này. Không thay rawverdictblocked, không khai cross_approved/human_audited hoặc machineK3/K4passed.
- Không gọi thêm model, tăng budget, restartExecutor hoặc sửa validator/state để giảapprove. Giữ globalattempts5/5, Codexcalls3/3.
- Không miễn CI/check khác, không gỡ protection, không admin/bypass. Chỉ bỏ draft; **không merge/land/deploy/auto-merge**, không mởP1–P6. H/tree/canonical thay đổi thì ngoại lệ hết hiệu lực.

Điều kiện trước ready đã đo: CIrun42352790095/attempt1 **SUCCESS**, **23/23jobsSUCCESS**, mọi runnerUbuntu; requiredchecks gate, gate-cong-cu-gop, gate-ops, gate-packet-loop, gate-registry và thu-hoi đềuSUCCESS trênH7 từ GitHubActionsApp15368. Đủ trangjobs/checkruns đã lưu. WorkflowdefinitionH7 quaGraphQLWorkflowRun.file; actualtestedPRmerge0eda0d2b3f28c723828b7e78692589176df57f35 cótree bằngH7, ghi đúnghaiidentityriêng. Preflightlivehead/canonicalđúngS7/H7, policycanonicalvẫnvắng, khôngfindingmớingoàihaifindingđãmiễn. KhôngWindowsCI/fullmutantWindows.

LegacybranchprotectionREST403/GraphQLFORBIDDEN vẫn được giữ là chưa đo đủ cho merge; đọc được effectivemasterrulesets không bị khai thành legacyprotectionđãđủ. Quyết định ready này không miễn phần kiểm tra merge đó.
