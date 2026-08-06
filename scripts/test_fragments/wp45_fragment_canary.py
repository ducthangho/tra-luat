# -*- coding: utf-8 -*-
"""F1-05 canary for packet-owned fragment execution."""

TEST_ID = "wp45_fragment_canary"


def run(tl_module):
    return callable(getattr(tl_module, "main", None))
