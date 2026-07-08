# -*- coding: utf-8 -*-
"""JSON/text output helpers for ``tl.py``.

All new JSON-capable command handlers should route through these helpers (or the
thin wrappers in ``tl.py``) rather than calling ``json.dumps`` directly.
"""
from __future__ import annotations

from typing import Any, Callable

from .deterministic import json_dumps

JsonDumps = Callable[[Any], str]


def emit_json(obj: Any, *, deterministic: bool | None = None, default_on: bool = False,
              project_root=None, file=None) -> None:
    print(json_dumps(obj, deterministic=deterministic, default_on=default_on, project_root=project_root), file=file)


def print_json_or_text(obj: dict, as_json: bool, *, json_dumps_func: JsonDumps | None = None) -> None:
    """Shared JSON/text renderer for the route-task/tool-inventory family."""
    if as_json:
        print((json_dumps_func or json_dumps)(obj))
        return
    _schema = str(obj.get("schema") or "")
    if not ("groups" in obj or _schema.startswith("route_task")):
        # v1.33.55 (giữ fix #4 canonical v1.33.54): renderer text chỉ biết tool-inventory/route-task — schema
        # KHÁC (release_manifest/verify/…) từng in nhầm 'route-task ok=True task=None' → fallback JSON đầy đủ.
        print((json_dumps_func or json_dumps)(obj))
        return
    if "groups" in obj:
        print(f"tool-inventory ok={obj.get('ok')} commands={len(obj.get('commands_available', []))}")
        for g in obj.get("groups", []):
            print(f"- {g['name']}: {g.get('title','')} — {g.get('purpose','')}")
            print("  commands:", ", ".join(g.get("commands", [])) or "(none)")
            if g.get("planned_commands"):
                print("  planned:", ", ".join(g.get("planned_commands", [])))
        if obj.get("missing_capabilities"):
            print("missing/planned:")
            for m in obj["missing_capabilities"]:
                print(f"- {m.get('capability')}: {m.get('status')} — {m.get('recommendation')}")
        return
    print(f"route-task ok={obj.get('ok')} task={obj.get('task')} workflow={obj.get('workflow_id')} risk={obj.get('risk')}")
    print("recommended commands:", ", ".join(obj.get("recommended_commands", [])) or "(none)")
    if obj.get("requires_dry_run"):
        print("requires: dry-run")
    if obj.get("requires_readback"):
        print("requires: verify/readback")
    if obj.get("stop_conditions"):
        print("stop conditions:")
        for s in obj["stop_conditions"]:
            print("-", s)
