# -*- coding: utf-8 -*-
"""tl_core.cli — I11 (v1.34.18): build_parser (35 block tay + register_generated + generic-flag pass)
tách NGUYÊN VĂN từ tl.py. Doctrine-comment trong block GIỮ NGUYÊN tại đây. tl giữ stub qua _STUB_MAP."""
from __future__ import annotations

import argparse   # noqa: F401
import json       # noqa: F401
import os         # noqa: F401
import re         # noqa: F401
import sys        # noqa: F401
from pathlib import Path  # noqa: F401

_TL = None


def bind(tl_module) -> None:
    """REBASE __globals__ (khuôn I1-I10)."""
    global _TL
    _TL = tl_module
    import types
    g = globals()
    tg = tl_module.__dict__
    for _n, _fn in list(g.items()):
        if isinstance(_fn, types.FunctionType) and _fn.__module__ == __name__ and _n != "bind":
            _re = types.FunctionType(_fn.__code__, tg, _n, _fn.__defaults__, _fn.__closure__)
            _re.__kwdefaults__ = _fn.__kwdefaults__
            _re.__doc__ = _fn.__doc__
            _re.__module__ = __name__
            g[_n] = _re


def build_parser() -> argparse.ArgumentParser:
    ap = argparse.ArgumentParser(prog="tl", description="CLI hợp nhất tra-luat (webapp target 2.21.2i)")
    # F (v1.33.6 — log rà: `tl --version` in usage-error thay vì version): flag chuẩn, nguồn = hằng VERSION.
    ap.add_argument("--version", action="version",
                    version=f"tl {VERSION} (webapp target {globals().get('EXPECT_VERSION', '2.21.2i')})")
    ap.add_argument("--config", help="file JSON webappUrl/token")
    ap.add_argument("--profile", help="corpus profile trong config v2: vbqppl, vbthuong, hoặc profile dự án")
    ap.add_argument("--timings", action="store_true", help="in thời gian từng call webapp ra stderr (=env TL_TIMINGS=1)")
    ap.add_argument("--deterministic", action="store_true", help="chuẩn hoá JSON output: sort keys + scrub path/temp/time volatile (=env TL_DETERMINISTIC=1)")
    ap.add_argument("--selftest", action="store_true", help="logic thuần, không mạng")
    sub = ap.add_subparsers(dest="cmd")
    try:
        tlg = _imp("tl_gws"); tlg.bind(sys.modules[__name__])
    except Exception as _e:   # noqa: BLE001 — tl_gws.py bị mount CẮT CỤT/NUL → KHÔNG để chết cả CLI.
        # Lệnh LÕI (footnote-map/cluster/rasoat-chongcheo/locate…) dùng hàm trong tl.py nên VẪN chạy; chỉ lệnh
        # gws/bootstrap/nlm/secrets (dùng tlg.*) báo lỗi rõ + cách khắc phục, thay vì SyntaxError sập toàn bộ.
        _tlg_err = (f"tl_gws.py không nạp được ({type(_e).__name__}: {_e}) — file bị mount cắt cụt/NUL? "
                    "Re-sync skill, HOẶC mirror scripts/ sang thư mục ghi được + strip NUL rồi chạy lại.")
        def _tlg_stub(_a, _m=_tlg_err):
            print(f"[tl] {_m}", file=sys.stderr); return 3
        class _TlgStub:
            def __getattr__(self, _n):
                return _tlg_stub
        tlg = _TlgStub()
        print(f"[tl] ⚠ {_tlg_err} (lệnh rà soát lõi vẫn chạy)", file=sys.stderr)

    p = sub.add_parser("gws-ping", help="GĐ0: cổng boot transport gws (PATH+pin version+auth), env-aware; Chat SKIP")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env (mặc định tự dò)")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_gws_ping)
    p = sub.add_parser("download", help="Tải file Drive → đĩa (gws raw-fast cho binary, tự fallback GAS cho text/JSON raw)")
    # v1.34.53 (A5 — log phiên 2026-07-15: `tl download <id>` gãy vì --file-id required, LỆCH extract/nlm-get
    # vốn nhận positional — mất 1 vòng thử-lỗi): nhận CẢ positional lẫn --file-id (--file-id thắng nếu đưa cả 2).
    p.add_argument("file_id_pos", nargs="?", help="Drive fileId (positional — tương đương --file-id)")
    p.add_argument("--file-id", dest="file_id")
    p.add_argument("--out", help="đường dẫn lưu (mặc định <fileId>.bin)")
    p.add_argument("--export-mime", dest="export_mime", help="MIME export cho Google-native (vd application/pdf)")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_download)
    p = sub.add_parser("gws-bootstrap-cowork", help="Cài gws BINARY MUSL-STATIC (public-curl Drive→chmod→PATH) + nạp cred. Cowork PHẢI dùng lệnh này — KHÔNG `npm i -g @googleworkspace/cli` (bản GNU cần GLIBC 2.39, Cowork glibc 2.35 → không chạy)")
    p.add_argument("--file-id", dest="file_id", help="fileId binary gws trên Drive (mặc định bản musl đã stage)")
    p.add_argument("--local-tgz", dest="local_tgz", help="dùng gws.tgz CÓ SẴN local (tl_fetch.sh giải nén từ bundle) → KHỎI tải Drive (md5 vẫn verify)")
    p.add_argument("--md5", help="md5 kỳ vọng (mặc định theo bản stage)")
    p.add_argument("--bindir", help="thư mục đặt gws (mặc định ~/.local/bin)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId cred mã hoá (mặc định GWS_CRED_FILEID)")
    p.add_argument("--no-auth", dest="no_auth", action="store_true", help="chỉ cài binary, KHÔNG tự nạp credential")
    p.add_argument("--force", action="store_true", help="ép tải lại binary kể cả khi gws đã có trên PATH (mặc định: gws có sẵn → chỉ nạp cred)")
    p.set_defaults(fn=tlg.cmd_gws_bootstrap_cowork)
    p = sub.add_parser("drive-push", help="[máy có gws auth] cập nhật NỘI DUNG file Drive (GIỮ fileId) = zip/bundle local, qua gws — đẩy bản ship mới mà KHÔNG đổi fileId")
    p.add_argument("path", help="đường dẫn zip/bundle local cần đẩy lên Drive")
    p.add_argument("--file-id", dest="file_id", help="fileId đích (mặc định SKILL_FILEID = file zip skill/bundle)")
    p.add_argument("--name", help="đổi tên file Drive thành tên này (GIỮ fileId)")
    p.add_argument("--rename-to-file", dest="rename_to_file", action="store_true", help="đổi tên file Drive theo TÊN FILE upload (basename, GIỮ fileId)")
    p.add_argument("--force", action="store_true",
                   help="(v1.33.59 ADR-0001) bỏ qua guard BUNDLE_META.json — chỉ khi CHẮC cây này là canonical")
    p.add_argument("--via", choices=["auto", "gws", "gcloud"], default="auto",
                   help="(v1.33.49) đường upload: auto = gws trước, chết → FALLBACK gcloud (cần `gcloud auth login "
                        "--enable-gdrive-access` 1 lần; OAuth production — né hạn-7-ngày Testing của gws)")
    p.set_defaults(fn=tlg.cmd_drive_push)
    p = sub.add_parser("bootstrap", help="ENV-AWARE: giải mã bundle (TL_MASTER_KEY) → nạp GAS token + gws (Code/Cowork)")
    p.add_argument("--secrets-id", dest="secrets_id", help="fileId tl_secrets.enc (mặc định SECRETS_FILEID)")
    p.add_argument("--secrets-file", dest="secrets_file", help="đường dẫn .enc đã tải sẵn (Cowork: agent tải qua MCP)")
    p.add_argument("--bindir", help="thư mục đặt gws (mặc định ~/.local/bin)")
    p.add_argument("--no-gws", dest="no_gws", action="store_true", help="chỉ nạp GAS token, bỏ qua gws")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true", help="bỏ qua pip install nlm (notebooklm-mcp-cli)")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.add_argument("--require-agent-creds", dest="require_agent_creds", action="store_true",
                   help="(WP1009) rc 4 khi credential agent (tl_agent_creds.enc) KHÔNG CẤU HÌNH / KHÔNG ĐO ĐƯỢC")
    p.set_defaults(fn=tlg.cmd_bootstrap)
    p = sub.add_parser("nlm-install", help="Cài nlm: mặc định tải Python 3.11 từ Drive (Cowork CHẶN astral). `--uv`: egress mở → uv tự cài Python 3.11 (dùng python hệ thống nếu đã ≥3.11) → KHÔNG tải 31MB từ Drive. ★Cowork 45s/lệnh: LẶP `--resume` tới rc=0 (mỗi lần 1 bước fetch→extract→install; rc=3=PARTIAL còn bước)")
    p.add_argument("--py-file-id", dest="py_file_id", help="fileId tarball Python 3.11 (mặc định PY311_FILEID)")
    p.add_argument("--uv", action="store_true", help="ƯU TIÊN uv (cài uv → uv python install 3.11 nếu hệ thống <3.11; egress mở) thay vì tải Drive; tự fallback Drive khi uv lỗi")
    p.add_argument("--resume", action="store_true",
                   help="(v1.30.1 #1) chạy ĐÚNG 1 bước kế tiếp rồi thoát (trạng thái dò từ đĩa, idempotent) — "
                        "cho env giới hạn 45s/lệnh (Cowork): lặp lại CÙNG lệnh tới rc=0; rc=3=PARTIAL")
    p.add_argument("--version", help="pin phiên bản notebooklm-mcp-cli (mặc định mới nhất)")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_nlm_install)
    p = sub.add_parser("overlap", help="E1+ SO QUY PHẠM: trích nguyên văn Điều bị sửa (VBHN) + cờ PENDING/đa-luật-sửa; --with-source thêm điều luật sửa")
    p.add_argument("target", nargs="?", help="gdocId | số hiệu VBHN canonical")
    p.add_argument("--text-file", dest="text_file", help="đọc canonical từ file thay vì Drive")
    p.add_argument("--with-source", dest="with_source", action="store_true", help="trích thêm điều của luật sửa (online, từ corpus)")
    p.add_argument("--refresh", action="store_true", help="refresh manifest")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_overlap)
    p = sub.add_parser("nlm-auth-pull", help="[COWORK] kéo cookie nlm mới nhất từ bundle → ~/.notebooklm-mcp-cli (refresh giữa phiên)")
    p.add_argument("--secrets-id", dest="secrets_id", help="fileId bundle (mặc định SECRETS_FILEID)")
    p.add_argument("--secrets-file", dest="secrets_file", help="dùng .enc local (project file) thay vì tải")
    p.add_argument("--env", choices=["code", "cowork", "chat"], help="ép runtime env")
    p.set_defaults(fn=tlg.cmd_nlm_auth_pull)
    p = sub.add_parser("secrets-stage", help="[CODE] gói {webappUrl,token GAS,gws_cred,nlm_auth} → mã hoá (TL_MASTER_KEY) → upload Drive")
    p.add_argument("--folder", help="folderId đích (mặc định _HOP_NAP)")
    p.add_argument("--secrets-id", dest="secrets_id", help="ghi đè bundle có sẵn (giữ fileId) thay vì tạo mới")
    p.add_argument("--no-gws", dest="no_gws", action="store_true", help="không gói gws_cred")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true", help="không gói nlm_auth (cookies NotebookLM)")
    p.set_defaults(fn=tlg.cmd_secrets_stage)
    p = sub.add_parser("secrets-set", help="[CODE] xoay vòng secret trong bundle: --gas-token/--webapp/--gws (ghi đè tại chỗ)")
    p.add_argument("--gas-token", dest="gas_token", help="token webapp GAS mới")
    p.add_argument("--webapp", help="webappUrl mới")
    p.add_argument("--gws", action="store_true", help="re-export gws cred hiện tại vào bundle")
    p.add_argument("--nlm", action="store_true", help="refresh cookie NotebookLM (nlm_auth) vào bundle — định kỳ ~2–4 tuần")
    p.add_argument("--no-public", dest="no_public", action="store_true",
                   help="(v1.33.1) KHÔNG đồng bộ file public .enc — mặc định --gws/--nlm ghi đè luôn GWS_CRED_FILEID/NLM_CRED_FILEID tại chỗ để CẢ 2 đường cùng tươi")
    p.add_argument("--secrets-id", dest="secrets_id", help="fileId bundle (mặc định SECRETS_FILEID)")
    p.add_argument("--secrets-file", dest="secrets_file", help="dùng .enc local thay vì tải")
    p.add_argument("--folder", help="folderId (khi cần tạo lại)")
    p.set_defaults(fn=tlg.cmd_secrets_set)
    p = sub.add_parser("secrets-keygen", help="(WP1009) in MỘT khoá TL_MASTER_KEY mạnh (token_urlsafe 32 = 43 ký tự), không ghi đĩa")
    p.set_defaults(fn=tlg.cmd_secrets_keygen)
    p = sub.add_parser("agent-creds-set", help="(WP1009) ghi credential agent (Codex auth.json/token Claude/khoá Gemini) → tl_agent_creds.enc mã hoá (TL_MASTER_KEY)")
    p.add_argument("--codex", action="store_true", help="gói <CODEX_HOME>/auth.json (thiếu CODEX_HOME ⇒ ~/.codex/auth.json)")
    p.add_argument("--claude-token-env", dest="claude_token_env", nargs="?", const="CLAUDE_CODE_OAUTH_TOKEN",
                   metavar="VAR", help="đọc token Claude từ BIẾN VAR (mặc định CLAUDE_CODE_OAUTH_TOKEN), không từ argv")
    p.add_argument("--antigravity-key-env", dest="antigravity_key_env", nargs="?", const="GEMINI_API_KEY",
                   metavar="VAR", help="đọc khoá Gemini cho `agy` từ BIẾN VAR (mặc định GEMINI_API_KEY), không từ argv")
    p.add_argument("--new", action="store_true", help="tạo tệp MỚI (rev=1) và in fileId")
    p.add_argument("--file-id", dest="file_id", help="ghi đè tại chỗ fileId này (mặc định TL_AGENT_CREDS_FILEID > AGENT_CREDS_FILEID)")
    p.add_argument("--folder", help="folderId khi --new (mặc định _HOP_NAP)")
    p.set_defaults(fn=tlg.cmd_agent_creds_set)
    p = sub.add_parser("gws-auth-stage", help="[CODE] export gws cred → mã hoá (khoá=webapp token) → v1.33.1: GHI ĐÈ TẠI CHỖ GWS_CRED_FILEID (fileId giữ nguyên, không bake lại); --new tạo file mới")
    p.add_argument("--folder", help="folderId đích (mặc định _HOP_NAP; chỉ dùng khi --new)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId đích ghi đè tại chỗ (mặc định GWS_CRED_FILEID baked)")
    p.add_argument("--new", action="store_true", help="tạo file MỚI thay vì ghi đè tại chỗ (hành vi cũ — nhớ bake fileId in ra)")
    p.set_defaults(fn=tlg.cmd_gws_auth_stage)
    p = sub.add_parser("gws-auth-load", help="[COWORK] tải cred mã hoá từ Drive → giải mã → ~/.config/gws/credentials.json (zero-setup)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId cred mã hoá (mặc định GWS_CRED_FILEID)")
    p.set_defaults(fn=tlg.cmd_gws_auth_load)
    p = sub.add_parser("nlm-auth-stage", help="[CODE, máy giữ hồ sơ trình duyệt gốc] gói cookie nlm → mã hoá (khoá=webapp token) → GHI ĐÈ TẠI CHỖ NLM_CRED_FILEID (fileId giữ nguyên); --new tạo file mới. Chỉ upload sau canary LIVE dương (đúng notebook); quy trình đầy đủ: RUNBOOK mục WP710")
    p.add_argument("--folder", help="folderId đích (mặc định _HOP_NAP; chỉ dùng khi --new)")
    p.add_argument("--refresh", action="store_true", help="làm tươi cookie best-effort trước khi gói; KHÔNG thay cổng canary LIVE")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId đích ghi đè tại chỗ (mặc định NLM_CRED_FILEID / env TL_NLM_CRED_FILEID)")
    p.add_argument("--new", action="store_true", help="tạo file MỚI thay vì ghi đè tại chỗ (hành vi cũ — nhớ bake fileId in ra)")
    p.add_argument("--force", action="store_true", help="(v1.33.39; WP710) KHÔNG bỏ qua được cổng canary LIVE — cookie không qua canary thì vẫn TỪ CHỐI, 0 upload")
    p.set_defaults(fn=tlg.cmd_nlm_auth_stage)
    p = sub.add_parser("nlm-auth-load", help="[COWORK] tải nlm cookie mã hoá từ Drive → giải mã (webapp token) → ~/.notebooklm-mcp-cli (HEADLESS, KHÔNG cần master key/`nlm login`)")
    p.add_argument("--cred-file-id", dest="cred_file_id", help="fileId nlm cred mã hoá (mặc định NLM_CRED_FILEID / env TL_NLM_CRED_FILEID)")
    # r208c 3.1 (đo 25-07): lệnh này GHI ĐÈ jar cục bộ — bundle cũ hơn sẽ giết cookie đang sống.
    p.add_argument("--force", action="store_true",
                   help="(r208c) BỎ QUA chốt chống hạ cấp — mặc định TỪ CHỐI khi bundle Drive CŨ HƠN jar cục bộ (đo 25-07: bản stage trễ 127', token xoay trong đó hết hạn 7,2h ⇒ nạp đè = mất cookie tươi)")
    p.set_defaults(fn=tlg.cmd_nlm_auth_load)
    p = sub.add_parser("drive-parity", help="GĐ1 pilot: đối chứng get-meta 1 fileId qua gws vs GAS (+spec MCP), đo ms, test fallback")
    p.add_argument("--file-id", dest="file_id", required=True, help="Drive fileId để get-meta đối chứng")
    p.add_argument("--test-fallback", dest="test_fallback", action="store_true", help="tắt gws (TL_GWS_DISABLE=1) → kiểm [FALLBACK→GAS]")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_drive_parity)
    p = sub.add_parser("transport-info", help="GĐ4: in ma trận định tuyến transport (A–E × 3-env) + trạng thái gws")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=tlg.cmd_transport_info)


    p = sub.add_parser("profile-files", help="liệt kê file trong manifest profile (lọc row-kind/NLM/corpus/name)")
    p.add_argument("--profile-name", dest="target_profile", help="profile cần đọc; mặc định global --profile/defaultProfile")
    p.add_argument("--name")
    p.add_argument("--row-kind", dest="row_kind")
    p.add_argument("--nlm", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc đã-trên-NLM (cờ trần; nhận cả '--nlm true/false')")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true")
    p.add_argument("--corpus", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc corpus=true (cờ trần; nhận cả '--corpus true/false' — v1.29.6 P2.3)")
    p.add_argument("--no-corpus", dest="no_corpus", action="store_true")
    p.add_argument("--limit", type=int)
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_profile_files)


    p = sub.add_parser("locate"); p.add_argument("query"); p.add_argument("--max", type=int, default=10)
    p.add_argument("--trust-cache", dest="trust_cache", action="store_true",
                   help="(v1.29.4 #9) TẮT auto-refresh khi cache >900s (mặc định tự refresh — chống báo-động-giả cache lệch)")
    p.add_argument("--refresh", action="store_true", help="tải lại manifest trước khi locate")
    p.add_argument("--debug", action="store_true", help="in lỗi fallback manifest nếu có")
    p.add_argument("--json", action="store_true",
                   help="(r179 T7) envelope JSON THẬT locate.v1 ở cả 3 nhánh (index/manifest/webapp) — hết no-op; row nền mang scope+BASE_SCOPE_HIT")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_locate)

    p = sub.add_parser("exists", help="kiểm tra hiện diện bằng source-map chuẩn hóa; không overclaim nếu miss")
    p.add_argument("query")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--json", action="store_true")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_exists)

    p = sub.add_parser("source-map", help="lập bản đồ nguồn rà soát theo nguyên tắc VBHN-first")
    p.add_argument("queries", nargs="+")
    p.add_argument("--refresh", action="store_true")
    p.add_argument("--strict", "--fail-on-finding", action="store_true",
                   help="(v1.29.4 #8) rc=1 khi verdict REVIEW/PAUSE (mặc định rc=0: phát-hiện ≠ lỗi lệnh — doctrine rc thống nhất; --fail-on-finding = alias CI)")
    p.add_argument("--json", action="store_true")
    p.add_argument("--out", help="ghi JSON ra file atomically (hữu ích trên Cowork để tránh stdout/heredoc timeout); tự bật JSON")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_source_map)


    p = sub.add_parser("instruction-audit", help="kiểm Instruction có ràng buộc skill/QT-3/research discovery-only")
    p.add_argument("--file", help="file Instruction/Project prompt cần kiểm")
    p.add_argument("--generate", action="store_true", help="generate bằng scripts/gen_instructions.py rồi audit")
    p.add_argument("--target", choices=["project", "nlm", "both", "config"], default="both")
    p.add_argument("--tier", choices=["core", "full"], default="core",
                   help="(v1.34.68 ⑤) core: audit bộ khóa CORE (MẶC ĐỊNH); full: audit REQUIRED_FULL (thêm khóa dev/release/live/OCR)")
    p.add_argument("--skill-version", default=VERSION)
    p.add_argument("--profile", help="profile corpus khi generate để audit (mặc định TL_PROFILE/default)")
    p.add_argument("--notebook", "--notebook-id", dest="notebook", help="notebookId của profile dự án")
    p.add_argument("--folder-name", dest="folder_name", help="tên folder trong Van_ban_thuong")
    p.add_argument("--root-folder-id", dest="root_folder_id", help="rootFolderId nếu đã tạo folder")
    p.add_argument("--print-text", action="store_true")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_instruction_audit)


    # ── WS1/WS2/WS3/WS5 (v1.19.7) ──


    p = sub.add_parser("nlm-reconcile", help="WS1: đối soát registry↔NLM bằng ground-truth CLI; backfill nlm_notebook_id (DRY mặc định)")
    p.add_argument("notebook_id", nargs="?")
    p.add_argument("--apply", action="store_true", help="THỰC THI reg_bulk backfill (mặc định DRY)")
    p.add_argument("--clear-stale", dest="clear_stale", action="store_true", help="clear mapping NLM của dòng KHÔNG có trên NLM")
    p.add_argument("--force-unsafe", dest="force_unsafe", action="store_true", help="(Pha 1) bỏ qua precheck blocker (rủi ro)")
    p.add_argument("--refresh", action="store_true")
    # A5 (v1.33.2 — log rà 111: `nlm-reconcile --json` crash unrecognized arguments trong khi mọi lệnh audit khác
    # đều nhận): output vốn ĐÃ là JSON — nhận cờ cho đồng bộ CLI (no-op), driver batch không phải case riêng.
    p.add_argument("--json", action="store_true", help="chấp nhận cho đồng bộ CLI (output vốn đã JSON)")
    p.add_argument("--out", help="ghi JSON ra file atomically; tự bật JSON")
    # v1.34.34 (THỰC CHỨNG lô 2026-07-12): nguồn nạp vào OVERFLOW shard KHÔNG được reconcile mặc định (chỉ quét
    # notebook chính) → ca VBHN 06 mất reg_link mà reconcile báo sạch. --all-notebooks quét base + overflow 1 lệnh.
    p.add_argument("--all-notebooks", dest="all_notebooks", action="store_true",
                   help="(v1.34.34) DRY quét CẢ base + overflow shard (TL_OVERFLOW_NOTEBOOK_ID) 1 lệnh — lưới cuối lô no-wait; --apply vẫn chạy per-notebook qua notebook_id")
    p.add_argument("--from-plan", dest="from_plan", nargs="?", const="auto",
                   help="(v1.34.54 A3) --apply nạp plan-artifact sweep DRY vừa ghi (mặc định .tl_state/reconcile_plan_<nb>.json) — BỎ re-scan NLM; an toàn: TTL 15' + freshness reg_get_bulk trên dòng sắp ghi")
    p.add_argument("--no-fallback", dest="no_fallback", action="store_true",
                   help="(v1.34.61 E2) NLM chết + --apply → GIỮ rc=2 như cũ thay vì DEFERRED_NLM_OFFLINE rc=0")
    # r208b 2.4 (báo cáo 25-07): DRY nay LUÔN ghi plan-artifact (mặc định .tl_state/reconcile_plan_<nb>.json —
    # đúng đường --from-plan auto); --apply bị guard CHẶN cũng in plan đầy đủ + ghi bản .BLOCKED để soát.
    # Cờ này chỉ để đổi ĐÍCH ghi (trước đây chỉ nhánh --all-notebooks nội bộ mới đặt được plan_out).
    p.add_argument("--plan-out", dest="plan_out",
                   help="(r208b) đường ghi plan-artifact JSON (mặc định .tl_state\\reconcile_plan_<nb>.json; bản bị guard chặn ghi .BLOCKED.json và `--from-plan` TỪ CHỐI nạp)")
    p.set_defaults(fn=cmd_nlm_reconcile)


    p = sub.add_parser("nlm-add", help="(1) thêm nguồn NLM qua CLI `nlm source add` (thay MCP source_add) — CLI-first")
    p.add_argument("notebook_id", nargs="?")
    # S8 (v1.33.44 — log 7A: drift doc↔CLI, ghi chú cũ dùng --drive/--wait): --drive = ALIAS của --drive-id;
    # --wait = NO-OP tương thích (mặc định ĐÃ wait; tắt bằng --no-wait) — driver theo doc cũ không gãy usage-error.
    p.add_argument("--drive-id", "--drive", dest="drive_id"); p.add_argument("--url"); p.add_argument("--file")
    p.add_argument("--row-kind", dest="row_kind", choices=["own", "overflow", "ref"],
                   help="r180 S8: ghi row_kind ngay ở bước reg_link (vd `ref` cho nguồn tham khảo) — trước đây trả row_kind=null, phải `register --row-kind` riêng")
    p.add_argument("--type", default=None, help="doc|sheets|slides — bỏ trống = tự nhận từ MIME manifest (#4 v1.34.17)"); p.add_argument("--title"); p.add_argument("--no-wait", action="store_true")
    p.add_argument("--wait", action="store_true",
                   help="no-op: mặc định ĐÃ wait tới khi nguồn settle; nhận cờ cho tương thích ghi chú cũ (tắt: --no-wait)")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước add (mặc định DỪNG nếu nguồn đã LIVE / không liệt kê được)")
    p.add_argument("--json", action="store_true",
                   help="(no-op v1.34.27 #6 — output vốn đã JSON; nhận cờ để đồng bộ bề mặt CLI, hết rc=2 usage-error)")
    p.add_argument("--no-fallback", dest="no_fallback", action="store_true",
                   help="(v1.34.60 ADR-4/5) NLM chết → GIỮ dừng rc=2 như cũ (mặc định: defer — registry "
                        "nlm_status=deferred + in batch-link, KHÔNG add mù, rc=0)")
    p.set_defaults(fn=cmd_nlm_add)

    p = sub.add_parser("nlm-cross", help="cross-shard query qua CLI `nlm cross query` (thay MCP cross_notebook_query)")
    p.add_argument("--json", action="store_true", help="(no-op v1.33.56 — output vốn đã JSON/verbatim; nhận để tương thích workflow cards)")
    p.add_argument("query")
    p.add_argument("--notebooks", help="csv id/tên shard (mặc định: base+overflow VBQPPL trong config)")
    p.add_argument("--all", action="store_true", help="query MỌI notebook (rate-limit)")
    p.add_argument("--no-fallback", dest="no_fallback", action="store_true",
                   help="(v1.34.60 ADR-5) NLM chết → GIỮ dừng rc=2 như cũ, không verbatim-return từ corpus")
    p.add_argument("--out", help="(v1.34.60 ADR-6) ghi envelope fallback ra file — né tràn stdout")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_nlm_cross)

    p = sub.add_parser("nlm-get", help="số nguồn vật lý + chi tiết notebook qua CLI `nlm notebook get` (thay MCP notebook_get; slot/preflight)")
    p.add_argument("notebook_id", nargs="?")
    # A1 (v1.33.18 — log rà 67: `nlm-get <nb> --json` chết `unrecognized arguments` dù lệnh VỐN luôn xuất JSON
    # → driver quen thêm --json đồng nhất cho nhóm read-only bị gãy riêng lệnh này): nhận làm NO-OP.
    p.add_argument("--json", action="store_true", help="no-op: lệnh luôn xuất JSON; nhận cờ để driver thêm --json đồng nhất không gãy")
    p.add_argument("--out", help="ghi JSON ra file atomically; tự bật JSON")
    p.set_defaults(fn=cmd_nlm_get)


    p = sub.add_parser("ingest-local", help="(2)+(3) ingest 1 file local → upload→organize→preflight→nlm add (CLI)→push (DRY mặc định, --apply để chạy; timeout giữa chừng → chạy lại CÙNG LỆNH + --resume)")
    p.add_argument("--json", action="store_true", help="(no-op v1.33.56 — output vốn đã JSON/verbatim; nhận để tương thích workflow cards)")
    p.add_argument("file", nargs="?", help="file NHỊ PHÂN local (.docx/.doc/.pdf); BỎ QUA nếu dùng --drive-id")
    p.add_argument("--drive-id", dest="drive_id",
                   help="(v1.34.37) file ĐÃ Ở TRÊN DRIVE (vd đã kéo-thả _HOP_NAP qua UI) — bỏ bước upload, organize "
                        "(convert→GDoc + tên chuẩn + xếp cat) ngay trên file đó. LOẠI TRỪ <file>. File NHỊ PHÂN, "
                        "KHÔNG phải GDoc đã convert.")
    p.add_argument("--name"); p.add_argument("--sohieu"); p.add_argument("--cat"); p.add_argument("--goc")
    p.add_argument("--hieuluc"); p.add_argument("--loai"); p.add_argument("--apply", action="store_true")
    p.add_argument("--confirm", choices=["yes"], help="bắt buộc khi --apply")
    p.add_argument("--expected-plan-hash", dest="expected_plan_hash",
                   help="SHA-256 plan_hash từ dry-run; apply từ chối nếu nguồn/tùy chọn đã đổi")
    p.add_argument("--resume", action="store_true",
                   help="(N6 v1.33.42) NỐI TIẾP tất định sau timeout/đứt giữa chừng: đọc journal run trước cho CÙNG file "
                        "→ skip bước đã xong (tái dùng fileId/gdoc/source_id), nguồn NLM đã live → LINK thay vì abort. "
                        "Cowork 45s: lặp CÙNG LỆNH + --resume tới rc=0 (mirror nlm-install --resume)")
    p.add_argument("--auto-plan", "--auto", dest="auto_plan", action="store_true",
                   help="đọc file/text local để suy tên chuẩn, số hiệu, loại, cat trước khi upload")
    p.add_argument("--text-file", dest="text_file", help="text đã OCR/extract cho PDF/DOCX để auto-plan và verify cat")
    p.add_argument("--source-quality", choices=["auto", "digital", "ocr"], default="auto",
                   help="gắn cảnh báo OCR trong auto-plan")
    p.add_argument("--ocr-verified", dest="ocr_verified", action="store_true",
                   help="xác nhận OCR đã đối chiếu; chỉ ghi vào auto-plan/cảnh báo")
    p.add_argument("--force-cat", dest="force_cat", action="store_true",
                   help="cho phép apply cat auto từ tên file/low-confidence khi đã kiểm tra tay")
    p.add_argument("--allow-large", dest="allow_large", action="store_true", help="nạp NGUYÊN file lớn (bỏ cổng HỎI tách; chấp nhận giảm chất lượng RAG)")
    p.add_argument("--large-threshold", dest="large_threshold", type=int, help=f"ngưỡng byte coi là 'lớn' (mặc định {NLM_LARGE_SRC_BYTES})")
    p.add_argument("--skip-nlm-preflight", dest="skip_nlm_preflight", action="store_true",
                   help="(v1.29.7) BỎ kiểm NLM sẵn-sàng trước upload (mặc định DỪNG sớm nếu NLM chưa cài/auth — tránh chuỗi dở dang)")
    p.add_argument("--no-fallback", dest="no_fallback", action="store_true",
                   help="(v1.34.60 ADR-5) NLM chết → DỪNG rc=2 (fail-closed) thay vì tự chuyển --no-nlm-add (v1.34.54)")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước nlm add (mặc định DỪNG nếu title đã LIVE / không liệt kê được)")
    p.add_argument("--replace-sohieu", dest="replace_sohieu", action="store_true",
                   help="(F1 r191) THAY BẢN có chủ đích: cho qua cổng dedup số hiệu LIVE (lỏng-năm) khi số hiệu "
                        "đã có dòng corpus-effective — in dòng cũ + chuỗi hạ bản sau nạp (mặc định CHẶN rc=2)")
    # v1.34.33 (benchmark 2026-07-12: settle-wait = ~50% của 238s/file): KHÔNG chờ nguồn settle sau `nlm source add`
    # — source_id có NGAY từ response nên reg_link vẫn ghi đủ; settle diễn ra ngầm phía NLM. Post-add dup-check bị
    # BỎ QUA khi no-wait (nguồn có thể chưa liệt kê được — check sẽ âm tính giả). Nạp LÔ xong chạy `tl nlm-reconcile`
    # xác nhận settle + link đủ. Truy vấn NLM ngay sau nạp no-wait có thể CHƯA thấy nội dung (chờ vài phút).
    p.add_argument("--nlm-no-wait", dest="nlm_no_wait", action="store_true",
                   help="(v1.34.33) KHÔNG chờ nguồn NLM settle sau add (−~50%% thời gian; source_id vẫn ghi registry đủ; bỏ post-add dup-check; nạp lô xong chạy `tl nlm-reconcile`)")
    # v1.34.35 (quy trình ADD-TAY — user chốt sau benchmark 2026-07-12): dừng ở Drive+registry, KHÔNG đụng NLM
    # (né hẳn cookie ~1h — hôm nay chết 2 lần giữa lô). Output in URL GDoc + notebook đích gợi ý + next_steps
    # điền sẵn: user add tay trên UI (Drive-picker chọn nhiều file, session browser) → nlm-reconcile --apply
    # link (bắc cầu exact-title) → register --corpus true. corpus KHÔNG set ở bước này (doctrine S4: corpus=true
    # chỉ khi đã lên NLM).
    p.add_argument("--no-nlm-add", dest="no_nlm_add", action="store_true",
                   help="(v1.34.35) DỪNG ở Drive+registry (không add NLM — né cookie; cho quy trình add tay trên UI): in gdoc_url + notebook gợi ý + next_steps (reconcile link + set corpus)")
    p.set_defaults(fn=cmd_ingest_local)


    p = sub.add_parser("reg-query", help="truy vấn registry/manifest OFFLINE (đọc CACHE) + lọc (name/sohieu/cat/loai/nlm/row-kind/corpus/mime). E2: SAU khi ghi sheet (reg_upsert/ingest/backfill) phải `--refresh` để thấy thay đổi LIVE, nếu không sẽ đọc cache CŨ (vd nlm rỗng dù sheet đã ghi).")
    p.add_argument("query", nargs="?", help="r180 S7: lọc mờ theo tên (alias --name) — vd `tl reg-query Hien_phap`")
    p.add_argument("--name"); p.add_argument("--sohieu"); p.add_argument("--cat")
    p.add_argument("--loai", help="(v1.33.6) lọc theo LOẠI văn bản, so CHUẨN HOÁ enum ('Luật' khớp cả 'Luat'/'luật'; 'Bộ luật' riêng) — trước đây phải lọc tay theo tiền tố tên")
    p.add_argument("--nlm", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc đã-trên-NLM (cờ trần; nhận cả '--nlm true/false')")
    p.add_argument("--no-nlm", dest="no_nlm", action="store_true")
    p.add_argument("--corpus", nargs="?", const=True, default=False, type=_optional_bool_flag,
                   help="lọc corpus=true (cờ trần; nhận cả '--corpus true/false' — v1.29.6 P2.3)")
    p.add_argument("--no-corpus", dest="no_corpus", action="store_true")
    p.add_argument("--corpus-effective", dest="corpus_effective", action="store_true",
                   help="(v1.34.42) lọc corpus theo ĐÚNG LUẬT SERVER (corpus∈{true,vbqppl}∪overflow − ref − thuong; = số `tl boot` đếm) — KHÁC `--corpus true` literal vốn bỏ sót vbqppl/overflow/blank-trên-NLM")
    p.add_argument("--notebook", help="(v1.34.53 A6) lọc dòng theo nlm_notebook_id — hết phải lọc tay bằng Python khi dòng nhiều shard/profile lẫn nhau")
    p.add_argument("--row-kind", dest="row_kind"); p.add_argument("--mime"); p.add_argument("--limit", type=int)
    p.add_argument("--drive-id", dest="drive_id",
                   help="(v1.34.2) lọc ĐÚNG 1 file theo drive_id/gdoc_id — readback chuẩn của các idempotency contract (Pha H bắt drift: contract dặn `reg-query --drive-id` mà parser thiếu cờ)")
    p.add_argument("--refresh", action="store_true", help="tải LẠI manifest/registry LIVE trước khi lọc (dùng sau khi vừa ghi sheet)"); p.add_argument("--json", action="store_true")
    p.add_argument("--live", action="store_true",
                   help="(v1.34.58 C-#11) đọc AUTHORITATIVE qua reg_get thay manifest cache — CHỈ hợp lệ kèm bộ lọc hẹp (--drive-id|--sohieu|--name; thiếu → LIVE_NEEDS_FILTER rc=2); filter còn lại áp tiếp phía client; envelope thêm source='live'")
    p.add_argument("--out", help="(S-4 v1.33.34) ghi JSON envelope ra file atomically; tự bật JSON (né stdout/heredoc timeout Cowork)")
    _add_base_also_flags(p)
    p.set_defaults(fn=cmd_reg_query)


    # v1.33.58 (Pha E - E2): 8 lệnh determinism sinh parser từ tl_core.command_registry
    # (GENERATED_SPECS giữ NGUYÊN VĂN flags/help; handler = stub tl; --profile/--config/--deterministic
    # do vòng inject cuối build_parser phủ như mọi subparser khác).
    _tl_registry.register_generated(sub, sys.modules[__name__])


    p = sub.add_parser("instructions", help="sinh Instruction/Project prompt; mặc định VBQPPL, --profile <tên> cho dự án văn bản thường")
    p.add_argument("--target", choices=["nlm", "project", "both", "config", "style-template"], default="both")
    p.add_argument("--tier", choices=["core", "full"], default="core",
                   help="(v1.34.68 Q3 — breaking chủ đích) core: Project tra cứu thường ngày, 2 khối dev thay bằng con trỏ CHỈ KHI (MẶC ĐỊNH); full: thêm đủ gate dev/release/OCR (bản cũ). NLM không đổi theo tier")
    p.add_argument("--skill-version", default=VERSION)
    p.add_argument("--notebook", "--notebook-id", dest="notebook", help="notebookId của profile dự án (văn bản thường)")
    p.add_argument("--folder-name", dest="folder_name", help="tên folder trong Van_ban_thuong (mặc định = tên profile)")
    p.add_argument("--root-folder-id", dest="root_folder_id", help="rootFolderId nếu đã tạo folder")
    p.add_argument("--check", action="store_true", help="chỉ kiểm output có đủ block bắt buộc")
    p.add_argument("--out", help="III.3: ghi Instruction ra FILE (UTF-8) thay vì in stdout (khỏi gọi thẳng gen_instructions.py)")
    p.set_defaults(fn=cmd_instructions)


    p = sub.add_parser("profile-ingest", help="profile own-scope: upload→GDoc canonical flat→verify draft/OCR→registry→NLM chunks (DRY mặc định)")
    p.add_argument("file", nargs="?", help="file NHỊ PHÂN local; BỎ QUA nếu dùng --drive-id")
    p.add_argument("--drive-id", dest="drive_id",
                   help="(v1.34.37) file ĐÃ Ở TRONG THƯ MỤC PROFILE — bỏ upload, CHỈ convert→GDoc + đổi tên chuẩn "
                        "(giữ PHẲNG trong root profile, KHÔNG xếp cat như vbqppl). LOẠI TRỪ <file>.")
    p.add_argument("--text-file", dest="text_file", help="file text đã OCR/extract để verify và lập split plan trước khi upload")
    p.add_argument("--name", help="tên canonical GDoc (mặc định suy từ header)")
    p.add_argument("--source-quality", choices=["auto", "digital", "ocr"], default="auto")
    p.add_argument("--ocr-verified", dest="ocr_verified", action="store_true", help="xác nhận OCR đã đối chiếu đủ để cho corpus/NLM")
    p.add_argument("--hieuluc", help="trạng thái hiệu lực nếu không phải dự thảo")
    p.add_argument("--large-threshold", dest="large_threshold", type=int, help=f"ngưỡng byte lập split plan (mặc định {NLM_LARGE_SRC_BYTES})")
    p.add_argument("--chunk-max-chars", dest="chunk_max_chars", type=int, default=100000, help="kích thước chunk text tối đa cho NLM")
    p.add_argument("--allow-default", dest="allow_default", action="store_true", help="cho phép chạy trên profile vbqppl (mặc định chặn)")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--confirm", choices=["yes"], help="bắt buộc khi --apply")
    p.add_argument("--expected-plan-hash", dest="expected_plan_hash",
                   help="SHA-256 plan_hash từ dry-run; apply từ chối nếu nguồn/tùy chọn đã đổi")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước nlm add (mặc định DỪNG nếu title đã LIVE / không liệt kê được)")
    p.add_argument("--allow-dup-name", dest="allow_dup_name", action="store_true",
                   help="(v1.34.53 C2) BỎ dup-guard tên registry trước upload (mặc định DỪNG nếu tên y hệt đã có dòng)")
    p.add_argument("--no-nlm-add", dest="no_nlm_add", action="store_true",
                   help="(v1.34.54 B2) DỪNG sau Drive+registry, KHÔNG đụng NLM — nạp NLM cuối lô bằng nlm-links (dán batch) + nlm-reconcile --apply")
    p.add_argument("--staged", action="store_true",
                   help="(r200 grill 24-07) lane STAGED — chỉ docx digital (TỪ CHỐI pdf/ocr/sheet): dừng sau "
                        "convert-readback, registry corpus=false + note staged:pending, HOÃN đọc-toàn-văn/"
                        "verify_gate/chunk/NLM sang `tl verify-staged` (parity — đổi thời điểm, không đổi tiêu chuẩn)")
    p.add_argument("--no-fallback", dest="no_fallback", action="store_true",
                   help="(v1.34.60 ADR-5) NLM chết → GIỮ dừng ở dedup-gate như cũ thay vì tự chuyển --no-nlm-add")
    p.add_argument("--resume", action="store_true",
                   help="(r184 ADR-0011/D5) NỐI sau khi chết giữa chừng: --name <tên> KHÔNG --apply = DRY repair plan; "
                        "--apply --confirm yes PHẢI kèm --drive-id HOẶC --journal <run_id> (chứng minh đúng nguồn)")
    p.add_argument("--journal", help="(r184 ADR-0011/D5) run_id journal của lần apply đứt — dùng với --resume --apply; "
                                     "journal legacy thiếu fingerprint → LEGACY_JOURNAL_REPLAN_REQUIRED")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_profile_ingest)

    p = sub.add_parser("profile-file-add", help="alias rõ nghĩa của profile-ingest: thêm file local vào profile + NLM")
    p.add_argument("file", nargs="?", help="file NHỊ PHÂN local; BỎ QUA nếu dùng --drive-id")
    p.add_argument("--drive-id", dest="drive_id",
                   help="(v1.34.37) file ĐÃ Ở TRONG THƯ MỤC PROFILE — bỏ upload, CHỈ convert→GDoc + đổi tên (giữ phẳng, không xếp cat). LOẠI TRỪ <file>.")
    p.add_argument("--text-file", dest="text_file", help="file text đã OCR/extract để verify và lập split plan trước khi upload")
    p.add_argument("--name", help="tên canonical GDoc (mặc định suy từ header)")
    p.add_argument("--source-quality", choices=["auto", "digital", "ocr"], default="auto")
    p.add_argument("--ocr-verified", dest="ocr_verified", action="store_true", help="xác nhận OCR đã đối chiếu đủ để cho corpus/NLM")
    p.add_argument("--hieuluc", help="trạng thái hiệu lực nếu không phải dự thảo")
    p.add_argument("--large-threshold", dest="large_threshold", type=int, help=f"ngưỡng byte lập split plan (mặc định {NLM_LARGE_SRC_BYTES})")
    p.add_argument("--chunk-max-chars", dest="chunk_max_chars", type=int, default=100000, help="kích thước chunk text tối đa cho NLM")
    p.add_argument("--allow-default", dest="allow_default", action="store_true", help="cho phép chạy trên profile vbqppl (mặc định chặn)")
    p.add_argument("--apply", action="store_true")
    p.add_argument("--confirm", choices=["yes"], help="bắt buộc khi --apply")
    p.add_argument("--expected-plan-hash", dest="expected_plan_hash",
                   help="SHA-256 plan_hash từ dry-run; apply từ chối nếu nguồn/tùy chọn đã đổi")
    p.add_argument("--skip-live-check", dest="skip_live_check", action="store_true",
                   help="(v1.29.3) BỎ cổng dedup-live trước nlm add (mặc định DỪNG nếu title đã LIVE / không liệt kê được)")
    p.add_argument("--allow-dup-name", dest="allow_dup_name", action="store_true",
                   help="(v1.34.53 C2) BỎ dup-guard tên registry trước upload (mặc định DỪNG nếu tên y hệt đã có dòng)")
    p.add_argument("--no-nlm-add", dest="no_nlm_add", action="store_true",
                   help="(v1.34.54 B2) DỪNG sau Drive+registry, KHÔNG đụng NLM — nạp NLM cuối lô bằng nlm-links (dán batch) + nlm-reconcile --apply")
    p.add_argument("--resume", action="store_true",
                   help="(r184 ADR-0011/D5) NỐI sau khi chết giữa chừng: --name <tên> KHÔNG --apply = DRY repair plan; "
                        "--apply --confirm yes PHẢI kèm --drive-id HOẶC --journal <run_id> (chứng minh đúng nguồn)")
    p.add_argument("--journal", help="(r184 ADR-0011/D5) run_id journal của lần apply đứt — dùng với --resume --apply; "
                                     "journal legacy thiếu fingerprint → LEGACY_JOURNAL_REPLAN_REQUIRED")
    p.add_argument("--json", action="store_true")
    p.set_defaults(fn=cmd_profile_file_add)


    p = sub.add_parser("register")
    p.add_argument("--drive-id", dest="drive_id"); p.add_argument("--bulk"); p.add_argument("--cols")
    p.add_argument("--force-insert", dest="force_insert", action="store_true",
                   help="(P0-1 v1.33.12) bỏ qua kiểm drive_id tồn tại (manifest/Drive) — CỐ Ý tạo dòng mới không gắn Drive; mặc định id lạ bị CHẶN vì reg_upsert insert-if-absent sẽ chèn dòng rác")
    for k in ("sohieu", "loai", "name", "cat", "linhvuc", "goc", "hieuluc", "sua_doi",
              "nlm_source_id", "nlm_notebook_id", "nlm_status", "nlm_title", "tukhoa", "corpus", "title_vn"):
        p.add_argument("--" + k.replace("_", "-"), dest=k)   # Group C2: +--nlm-notebook-id (khỏi backfill-notebook riêng)
    # v1.29.7 (log NĐ131 #7): cho SỬA row_kind qua CLI có kiểm soát (trước không có đường nào — dòng bị gán nhầm
    # overflow bởi bug #6 không sửa được). choices chặn giá trị lạ.
    p.add_argument("--row-kind", dest="row_kind", choices=["own", "overflow", "ref"],
                   help="(v1.29.7) sửa row_kind (own/overflow/ref) — vd chữa dòng bị gán nhầm overflow")
    p.add_argument("--force-unsafe", dest="force_unsafe", action="store_true", help="(v1.29.2) BỎ QUA precheck blocker — RỦI RO, tự chịu")
    # r279 (va chạm 2 phiên 31-07-2026): CAS chống ghi song song. Lặp được: --expect corpus=true --expect nlm_status=pushed
    p.add_argument("--expect", action="append", default=None, metavar="COL=VAL",
                   help="(r279) CHỐT CAS: chỉ ghi nếu dòng ĐANG có COL=VAL (lặp được; VAL rỗng = kỳ vọng cột rỗng). "
                        "Lệch ⇒ rc=3 KHÔNG ghi gì — nghĩa là phiên khác vừa đụng dòng này. Dùng cho mọi lô ghi khi "
                        "có thể có phiên song song")
    # r208b 2.1 (báo cáo 25-07): mặc định TỰ SUY name (tên file Drive) + cat (folder cha) khi cột trống,
    # không suy được thì cảnh báo trong kết quả. Cờ này để tắt khi cố ý muốn dòng trống (hiếm).
    p.add_argument("--no-autofill", dest="no_autofill", action="store_true",
                   help="(r208b) TẮT tự suy name/cat từ metadata Drive — mặc định register điền cột trống rồi báo `autofilled`, không suy được thì `warn: REGISTER_ROW_INCOMPLETE` (trước đây trả ok:true im lặng với name=\"\"/cat=\"\" ⇒ cờ NLM_GHOST_SOURCE/ORPHAN_CAT giả)")
    # N3 (v1.33.41 — log rà: agent quen tay `register … --apply` bị usage-error rc=2 giữa loop): register GHI
    # TRỰC TIẾP by-design (journaled+verified, không DRY) — nhận cờ --apply làm NO-OP để không vỡ muscle-memory.
    p.add_argument("--apply", action="store_true", help="(no-op compat) register luôn ghi trực tiếp — cờ này chỉ để khỏi vỡ script/agent-loop quen các lệnh DRY-mặc-định")
    # #5 TRỌN (v1.34.20, server ≥2.21.2j): XOÁ TRẮNG giá trị cột có kiểm soát — trước đây giá trị rỗng bị webapp
    # bỏ im lặng, không có đường đính chính sohieu/loai/goc gán nhầm (ca thật hồ sơ BHXH).
    p.add_argument("--clear-cols", dest="clear_cols",
                   help="CSV cột cần XOÁ TRẮNG (reg_clear 2-tầng: nlm_*/note tự do; cột thường server đòi force — tl tự gắn; drive_id/name BẢO VỆ). Cần --confirm yes.")
    p.add_argument("--confirm", help="'yes' để xác nhận --clear-cols (thao tác xoá giá trị)")
    p.add_argument("--json", action="store_true",
                   help="(no-op v1.34.30 #4 — register vốn LUÔN in JSON; nhận cờ để đồng bộ bề mặt CLI, hết rc=2 usage-error + hết đổ danh sách lệnh top-level. Nhất quán nlm-add #6)")
    p.set_defaults(fn=cmd_register)


    p = sub.add_parser("hygiene", help="registry hygiene: duplicate/orphan/quarantine plan")
    hsub = p.add_subparsers(dest="hsub")
    hp = hsub.add_parser("scan"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true"); hp.set_defaults(fn=cmd_hygiene)
    hp = hsub.add_parser("plan"); hp.add_argument("query"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true")
    hp.add_argument("--apply", action="store_true"); hp.add_argument("--confirm"); hp.add_argument("--to-cat", dest="to_cat"); hp.set_defaults(fn=cmd_hygiene)
    hp = hsub.add_parser("query"); hp.add_argument("query"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true")
    hp.set_defaults(fn=cmd_hygiene)
    hp = hsub.add_parser("reconcile", help="global reconcile theo số hiệu parse từ tên hoặc md5")
    hp.add_argument("query", nargs="?"); hp.add_argument("--refresh", action="store_true"); hp.add_argument("--json", action="store_true")
    hp.add_argument("--apply", action="store_true"); hp.add_argument("--confirm"); hp.add_argument("--to-cat", dest="to_cat"); hp.set_defaults(fn=cmd_hygiene)

    p = sub.add_parser("reconcile", help="alias: hygiene reconcile")
    p.add_argument("query", nargs="?"); p.add_argument("--refresh", action="store_true"); p.add_argument("--json", action="store_true")
    p.add_argument("--apply", action="store_true"); p.add_argument("--confirm"); p.add_argument("--to-cat", dest="to_cat"); p.set_defaults(fn=cmd_hygiene, hsub="reconcile")


    # r310 (RAS-01 vế metadata/CLI · RAS-14): `rasoat` hết `argparse.REMAINDER`. Trước đây cả sub lẫn đuôi
    # dòng lệnh là hai positional thô ⇒ không cờ nào được KHAI: ba đường GHI (keywords/titles/orchestrate)
    # vô hình với tool-inventory/workflow-audit --strict, và `--profile` gõ SAU sub bị đẩy nguyên cho script
    # con (RAS-14 — `backfill_nlm_title.py` có `--profile` RIÊNG nghĩa khác hẳn). Spec + meta ở
    # tl_core/command_registry.py (RASOAT_SPECS / NESTED_COMMAND_META); cổng `--apply` ở cmd_rasoat.
    p = sub.add_parser("rasoat", help="rà soát/backfill: keywords|titles|worksheet|phuluc|orchestrate")
    _tl_registry.register_rasoat(p, sys.modules[__name__])
    p = sub.add_parser("cache-build", help="B2: dựng cache cấu trúc docs/<sh>--consolidated.json (wrapper ingest_to_cache.py) cho `rasoat worksheet`; chain --gdoc-id/--input, tự nạp config")
    p.add_argument("sohieu", nargs="?", help="số hiệu canonical (vd 19/VBHN-VPQH)")
    p.add_argument("rest", nargs=argparse.REMAINDER, help="cờ chuyển thẳng cho ingest_to_cache.py: --gdoc-id/--input/--goc/--method/--nlm-source-id/--vbhn-first…")
    p.set_defaults(fn=cmd_cache_build)
    # v1.33.48 (rà Instruction 'Luật BHXH' — dặn 'MỌI lệnh truyền --profile' nhưng flag chỉ ở ROOT parser →
    # `tl reg-query --profile "Luật BHXH"` gãy `unrecognized arguments` rc=2; agent phải nhớ đặt TRƯỚC subcommand):
    # nhận --profile/--config Ở CẢ SAU subcommand — thêm vào từng subparser CHƯA có (subparser đã tự khai thì giữ).
    # ⚠ PHẢI default=SUPPRESS: Python mới parse subcommand vào NAMESPACE CON rồi copy-đè lên namespace gốc —
    # default None của cờ injected sẽ ĐÈ MẤT giá trị `tl --profile X <cmd>` đặt trước subcommand (bắt được bằng
    # smoke ngay khi viết). SUPPRESS = không truyền thì không set attr → giá trị root sống; truyền sau → thắng.
    def _walk_subparsers(_root):
        # v1.33.56 (review P4-04): đệ quy nested subparsers (hygiene có cấp con) — vòng cũ chỉ quét top-level.
        out = list(_root.choices.values())
        for _p in _root.choices.values():
            for _act0 in _p._actions:
                if isinstance(_act0, argparse._SubParsersAction):
                    out.extend(_walk_subparsers(_act0))
        return out
    for _sp in _walk_subparsers(sub):
        _opts = {o for _act in _sp._actions for o in _act.option_strings}
        if "--profile" not in _opts:
            _sp.add_argument("--profile", default=argparse.SUPPRESS, help="corpus profile (nhận cả trước lẫn sau subcommand)")
        if "--config" not in _opts:
            _sp.add_argument("--config", default=argparse.SUPPRESS, help="file JSON webappUrl/token (nhận cả sau subcommand)")
        if "--deterministic" not in _opts:
            _sp.add_argument("--deterministic", action="store_true", default=argparse.SUPPRESS,
                             help="chuẩn hoá JSON output (nhận cả sau subcommand)")
        if "--json" not in _opts:
            # v1.34.53 (C3 — log phiên OCR 2026-07-15: `tl source-delete <id> --json` chết `unrecognized
            # arguments` dù output vốn là JSON): --json NO-OP ở MỌI subcommand chưa tự khai — cờ thừa không
            # được làm crash lệnh. SUPPRESS: không truyền = không set attr (hành vi cũ nguyên vẹn).
            _sp.add_argument("--json", action="store_true", default=argparse.SUPPRESS,
                             help="(no-op nếu lệnh vốn in JSON) nhận cờ để không gãy vì cờ thừa")
    return ap
