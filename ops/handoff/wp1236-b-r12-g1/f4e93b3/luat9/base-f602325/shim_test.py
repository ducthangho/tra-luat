"""Shim CHI DE DO NEN (base): bo quet ghim dat GATE_OUTPUT_DOI_CHIEU_MA, test base doc LAND_EVIDENCE_NGUON_MA."""
import os
import runpy

os.environ["LAND_EVIDENCE_NGUON_MA"] = os.environ["GATE_OUTPUT_DOI_CHIEU_MA"]
_g = runpy.run_path(os.environ["SHIM_TEST_THAT"], run_name="len_test_shim")
CA, chay_ca = _g["CA"], _g["chay_ca"]
