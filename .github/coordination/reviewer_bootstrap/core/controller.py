"""CLI của lõi reviewer bootstrap (wp77 / RA-01).

Lệnh:
  schema              in schema operation máy đọc được (JSON)
  call --op --params  kiểm rồi chạy một operation trên fake store; rc khác 0 nếu bị TỪ CHỐI
  produce --out       sinh một lượt artifact đầy đủ rồi THOÁT (dùng cho phép thử retention)
  verify --root       kiểm một lượt đã niêm phong; rc khác 0 và gọi ĐÍCH DANH file thiếu
  selftest            chạy suite phản chứng

KHÔNG có cờ nào nhận token, và không lệnh nào mở kết nối mạng.
"""

import argparse
import json
import os
import platform
import shutil
import sys
import tempfile

_HERE = os.path.dirname(os.path.abspath(__file__))
_PARENT = os.path.dirname(_HERE)
if _PARENT not in sys.path:
    sys.path.insert(0, _PARENT)

from core import artifacts, operations  # noqa: E402
from core.fake_github import FakeGitHub, FakeGitHubError  # noqa: E402

# rc quy ước - đọc được bằng máy, không phải "rc khác 0" chung chung.
RC_OK = 0
RC_REJECTED = 2
RC_VERIFY_FAILED = 3
RC_USAGE = 64


def _seed_store(ledger_path):
    store = FakeGitHub(ledger_path)
    store.add_issue(77, "wp77 packet spec", labels=["state:leased"])
    store.add_comment(5236083781, 77, "lease granted")
    store.add_pull(1001, "b044f8b14e9ea3ad5d91a7fb4f0d29a3fe8415eb", "mission/76/integration")
    store.add_ci_run(9001, "success")
    store.add_diff(1001, "--- a\n+++ b\n")
    return store


def cmd_schema(args):
    json.dump(operations.schema(), sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return RC_OK


def cmd_call(args):
    try:
        params = json.loads(args.params)
    except ValueError as exc:
        sys.stderr.write("invalid --params JSON: %s\n" % exc)
        return RC_USAGE
    ledger_path = args.ledger
    tmpdir = None
    if not ledger_path:
        tmpdir = tempfile.mkdtemp(prefix="ra01-call-")
        ledger_path = os.path.join(tmpdir, "ledger.json")
    try:
        return _do_call(args.op, params, ledger_path)
    finally:
        if tmpdir:
            shutil.rmtree(tmpdir, ignore_errors=True)


def _do_call(op, params, ledger_path):
    store = _seed_store(ledger_path)
    try:
        result = store.call(op, params)
    except operations.OperationError as exc:
        # Đường từ chối TRƯỚC khi chạy: op lạ, thiếu/thừa/sai kiểu tham số.
        sys.stderr.write("REJECTED: %s\n" % exc)
        return RC_REJECTED
    except FakeGitHubError as exc:
        sys.stderr.write("FAKE_GITHUB_ERROR: %s\n" % exc)
        return RC_REJECTED
    json.dump(result, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    return RC_OK


def cmd_produce(args):
    """Sinh đủ năm hạng mục artifact rồi thoát.

    Được gọi như một TIẾN TRÌNH RIÊNG trong phép thử retention: cái phải sống sót là locator trên
    đĩa, không phải trạng thái trong RAM của tiến trình sinh ra nó.
    """
    aset = artifacts.ArtifactSet(args.out, args.run_id)
    aset.add("source", "source/controller_snapshot.txt", "reviewer bootstrap core (RA-01)\n")
    aset.add("corpus", "corpus/cases.json", json.dumps({"cases": ["valid", "invalid"]}) + "\n")
    aset.add(
        "per_case_matrix",
        "matrix/per_case.tsv",
        "case\tstatus\nvalid\tpassed\ninvalid\trejected\n",
    )
    aset.add(
        "runner_env_digest",
        "runner/env_digest.json",
        json.dumps(
            {
                "python": platform.python_version(),
                "platform": platform.system(),
                "credentials_present_in_digest": False,
            },
            sort_keys=True,
        )
        + "\n",
    )
    aset.add("cleanup_record", "cleanup/record.json", json.dumps({"removed": [], "kept": "all"}) + "\n")
    manifest = aset.finalize()
    sys.stdout.write("run_id=%s entries=%d\n" % (manifest["run_id"], len(manifest["entries"])))
    return RC_OK


def cmd_verify(args):
    report = artifacts.verify(args.root)
    json.dump(report, sys.stdout, ensure_ascii=False, indent=2, sort_keys=True)
    sys.stdout.write("\n")
    if report["ok"]:
        return RC_OK
    for name in report["missing_files"]:
        sys.stderr.write("MISSING ARTIFACT: %s\n" % name)
    for name in report["hash_mismatches"]:
        sys.stderr.write("HASH MISMATCH: %s\n" % name)
    for name in report["missing_categories"]:
        sys.stderr.write("MISSING CATEGORY: %s\n" % name)
    if not report["manifest_hash_ok"] and report["manifest_present"]:
        sys.stderr.write("MANIFEST TAMPERED: %s\n" % artifacts.MANIFEST_NAME)
    return RC_VERIFY_FAILED


def cmd_selftest(args):
    from core import selftest

    return selftest.main()


def build_parser():
    parser = argparse.ArgumentParser(prog="reviewer-bootstrap-core", description=__doc__)
    sub = parser.add_subparsers(dest="command", required=True)

    sub.add_parser("schema").set_defaults(func=cmd_schema)

    call = sub.add_parser("call")
    call.add_argument("--op", required=True)
    call.add_argument("--params", required=True)
    call.add_argument("--ledger", default=None)
    call.set_defaults(func=cmd_call)

    produce = sub.add_parser("produce")
    produce.add_argument("--out", required=True)
    produce.add_argument("--run-id", dest="run_id", required=True)
    produce.set_defaults(func=cmd_produce)

    verify = sub.add_parser("verify")
    verify.add_argument("--root", required=True)
    verify.set_defaults(func=cmd_verify)

    sub.add_parser("selftest").set_defaults(func=cmd_selftest)
    return parser


def main(argv=None):
    args = build_parser().parse_args(argv)
    return args.func(args)


if __name__ == "__main__":
    sys.exit(main())
