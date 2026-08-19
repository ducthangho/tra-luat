# -*- coding: utf-8 -*-
"""Unit tests for tl_core/command_registry.py (Packet AG-T0-03).

Kiểm thử toàn diện:
- Duyệt đệ quy cây lệnh Argparse (collect_parser_tree)
- Báo cáo độ phủ hai chiều cây lệnh ↔ metadata (compute_parser_coverage)
- Kiểm tra tính tất định, schema parser_tree_coverage.v1, cờ --strict và --unregistered-only
"""
import argparse
import sys
from pathlib import Path
import unittest

HERE = Path(__file__).resolve().parent
SCRIPTS_DIR = HERE.parent
if str(SCRIPTS_DIR) not in sys.path:
    sys.path.insert(0, str(SCRIPTS_DIR))

from tl import build_parser
from tl_core.command_registry import (
    COMMAND_META,
    GENERATED_SPECS,
    all_command_meta,
    collect_parser_tree,
    compute_parser_coverage,
)


class CommandRegistryCoverageTest(unittest.TestCase):
    def setUp(self):
        self.parser = build_parser()

    def test_collect_parser_tree_structure(self):
        tree = collect_parser_tree(self.parser)
        self.assertIsInstance(tree, list)
        self.assertGreater(len(tree), 150)

        # Kiểm tra tính tất định: mảng đã được sort theo path
        paths = [n["path"] for n in tree]
        self.assertEqual(paths, sorted(paths))

        # Kiểm tra các node container
        container_nodes = {n["path"]: n for n in tree if n["is_container"]}
        self.assertIn("hygiene", container_nodes)
        self.assertIn("rasoat", container_nodes)
        self.assertTrue(container_nodes["hygiene"]["is_container"])
        self.assertTrue(container_nodes["rasoat"]["is_container"])

        # Kiểm tra node lá thuộc container lồng
        leaf_nodes = {n["path"]: n for n in tree if not n["is_container"]}
        self.assertIn("rasoat keywords", leaf_nodes)
        self.assertIn("rasoat titles", leaf_nodes)
        self.assertIn("rasoat orchestrate", leaf_nodes)
        self.assertIn("rasoat worksheet", leaf_nodes)
        self.assertIn("rasoat phuluc", leaf_nodes)
        self.assertIn("hygiene scan", leaf_nodes)
        self.assertIn("hygiene plan", leaf_nodes)

        # Node con phải có parent và depth > 1
        node_kw = leaf_nodes["rasoat keywords"]
        self.assertEqual(node_kw["parent"], "rasoat")
        self.assertEqual(node_kw["depth"], 2)
        self.assertIn("--json", node_kw["options"])

        # Kiểm tra help text được trích xuất
        nodes_with_help = [n for n in tree if n["help"]]
        self.assertGreater(len(nodes_with_help), 150)

    def test_compute_parser_coverage_schema_and_metrics(self):
        report = compute_parser_coverage(self.parser, strict=False)
        self.assertEqual(report["schema"], "parser_tree_coverage.v1")
        self.assertTrue(report["ok"])

        summary = report["summary"]
        self.assertEqual(summary["total_nodes"], 198)
        self.assertEqual(summary["container_commands"], 2)
        self.assertEqual(summary["total_leaf_commands"], 196)
        self.assertEqual(summary["registered_leaf_commands"], 166)
        self.assertEqual(summary["unregistered_leaf_commands"], 30)
        self.assertEqual(summary["registry_orphaned_commands"], 0)
        expected_pct = round(166 / 196 * 100, 2)
        self.assertEqual(summary["coverage_percent"], expected_pct)
        self.assertEqual(summary["coverage_percent"], 84.69)

        # 0 lệnh trong registry bị mồ côi (mọi metadata đều trỏ đến lệnh thật trong parser)
        self.assertEqual(report["categories"]["registry_not_in_parser"], [])

    def test_compute_parser_coverage_strict_mode(self):
        # Khi strict=True, nếu còn lệnh chưa đăng ký thì ok=False
        report_strict = compute_parser_coverage(self.parser, strict=True)
        if report_strict["summary"]["unregistered_leaf_commands"] > 0:
            self.assertFalse(report_strict["ok"])
        else:
            self.assertTrue(report_strict["ok"])

    def test_compute_parser_coverage_unregistered_only_filter(self):
        report_all = compute_parser_coverage(self.parser, unregistered_only=False)
        report_unreg = compute_parser_coverage(self.parser, unregistered_only=True)

        self.assertEqual(len(report_all["commands"]), report_all["summary"]["total_leaf_commands"])
        self.assertEqual(len(report_unreg["commands"]), report_unreg["summary"]["unregistered_leaf_commands"])
        for cmd in report_unreg["commands"]:
            self.assertFalse(cmd["has_meta"])
            self.assertEqual(cmd["risk"], "unregistered")

    def test_registry_coverage_command_registered(self):
        # Lệnh mới registry-coverage phải có trong GENERATED_SPECS và COMMAND_META
        self.assertIn("registry-coverage", COMMAND_META)
        gen_names = [s["name"] for s in GENERATED_SPECS]
        self.assertIn("registry-coverage", gen_names)

        meta = all_command_meta()["registry-coverage"]
        self.assertTrue(meta["read_only"])
        self.assertEqual(meta["risk"], "low")
        self.assertEqual(meta["module"], "workflow")

    def test_synthetic_subparser_coverage(self):
        # Test với parser giả lập độc lập
        mock_p = argparse.ArgumentParser(prog="test_tl")
        subs = mock_p.add_subparsers(dest="cmd")
        p_a = subs.add_parser("cmd_a", help="cmd a help")
        p_a.add_argument("--json", action="store_true")
        p_b = subs.add_parser("container_b")
        b_subs = p_b.add_subparsers(dest="sub_cmd")
        p_b1 = b_subs.add_parser("sub1", help="b1 help")
        p_b1.add_argument("--apply", action="store_true")

        tree = collect_parser_tree(mock_p)
        self.assertEqual(len(tree), 3)  # cmd_a, container_b, container_b sub1
        self.assertEqual([n["path"] for n in tree], ["cmd_a", "container_b", "container_b sub1"])
        self.assertEqual(tree[0]["help"], "cmd a help")

        cov = compute_parser_coverage(mock_p)
        self.assertEqual(cov["summary"]["total_nodes"], 3)
        self.assertEqual(cov["summary"]["container_commands"], 1)
        self.assertEqual(cov["summary"]["total_leaf_commands"], 2)
        # Vì mock_p không nằm trong tl registry nên 2 leaf là unregistered
        self.assertEqual(cov["summary"]["unregistered_leaf_commands"], 2)
        self.assertIn("container_b sub1", cov["categories"]["high_risk_unregistered"])

    def test_orphan_detection_strict_fail_closed(self):
        # Phản chứng khoá nhánh orphan của strict mode (Finding F1)
        mock_p = argparse.ArgumentParser(prog="test_tl")
        subs = mock_p.add_subparsers(dest="cmd")
        subs.add_parser("cmd_a")

        # Mock module có cmd_a (khớp parser) VÀ cmd_orphan (không có trong parser)
        class MockTLModule:
            COMMAND_META = {
                "cmd_a": {"read_only": True, "risk": "low"},
                "cmd_orphan": {"read_only": True, "risk": "low"},
            }

        cov_non_strict = compute_parser_coverage(mock_p, tl_module=MockTLModule, strict=False)
        self.assertTrue(cov_non_strict["ok"])
        self.assertEqual(cov_non_strict["categories"]["unregistered"], [])
        self.assertEqual(cov_non_strict["categories"]["registry_not_in_parser"], ["cmd_orphan"])
        self.assertEqual(cov_non_strict["summary"]["registry_orphaned_commands"], 1)

        # Khi strict=True: unregistered rỗng nhưng orphan > 0 => PHẢI fail-closed (ok=False)
        cov_strict = compute_parser_coverage(mock_p, tl_module=MockTLModule, strict=True)
        self.assertFalse(cov_strict["ok"])


if __name__ == "__main__":
    unittest.main()
