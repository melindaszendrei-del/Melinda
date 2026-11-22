from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

import numpy as np
import sympy as sp

POS_EPS = 1e-12
COND_MAX = 1e8
RESIDUAL_TOL = 1e-10


def mk(test_id, title, expected, observed, passed, diagnostics):
    return {
        "test_id": test_id,
        "title": title,
        "expected": expected,
        "observed": observed,
        "passed": bool(passed),
        "diagnostics": diagnostics,
    }


def run_suite():
    tests = []

    # RM-S1-01: standard metric on S^1 in two stereographic charts.
    u, v = sp.symbols("u v", real=True, nonzero=True)
    g_n = 4 / (1 + u**2)**2
    g_s = 4 / (1 + v**2)**2
    v_of_u = 1 / u
    residual = sp.simplify(g_n - sp.diff(v_of_u, u)**2 * g_s.subs(v, v_of_u))
    grid = np.r_[np.linspace(-4, -0.25, 200), np.linspace(0.25, 4, 200)]
    round_trip = float(np.max(np.abs(1 / (1 / grid) - grid)))
    ok = residual == 0 and round_trip <= RESIDUAL_TOL
    tests.append(mk(
        "RM-S1-01",
        "S¹ standard metric in two stereographic charts",
        "PASS_EXACT",
        "PASS_EXACT" if ok else "FAIL",
        ok,
        {
            "symbolic_metric_residual": str(residual),
            "round_trip_max_error": round_trip,
            "certified_overlap_sample": "0.25 <= |u| <= 4",
        },
    ))

    # RM-R2-02: Euclidean metric under an affine coordinate change.
    A = np.array([[2.0, 0.0], [0.0, 1.0]])
    g1 = np.eye(2)
    A_inv = np.linalg.inv(A)
    g2 = A_inv.T @ g1 @ A_inv
    compat = float(np.linalg.norm(g1 - A.T @ g2 @ A, ord=2))
    rt = float(np.linalg.norm(A.T @ (A_inv.T @ g1 @ A_inv) @ A - g1, ord=2))
    ok = compat <= RESIDUAL_TOL and rt <= RESIDUAL_TOL
    tests.append(mk(
        "RM-R2-02",
        "Euclidean metric under affine coordinates",
        "PASS_EXACT",
        "PASS_EXACT" if ok else "FAIL",
        ok,
        {
            "A": A.tolist(),
            "g_chart_1": g1.tolist(),
            "g_chart_2": g2.tolist(),
            "compatibility_residual_norm": compat,
            "round_trip_error": rt,
        },
    ))

    # RM-MUT-03: indefinite mutant.
    g = np.diag([1.0, -1.0])
    lam_min = float(np.linalg.eigvalsh(g).min())
    ok = lam_min < 0
    tests.append(mk(
        "RM-MUT-03",
        "Indefinite metric mutant",
        "REJECT_METRIC_INDEFINITE",
        "REJECT_METRIC_INDEFINITE" if ok else "MISCLASSIFIED",
        ok,
        {"lambda_min": lam_min, "intrinsic_singularity": "NOT_INFERRED"},
    ))

    # RM-MUT-04: degenerate mutant.
    g = np.diag([1.0, 0.0])
    lam_min = float(np.linalg.eigvalsh(g).min())
    ok = abs(lam_min) <= POS_EPS
    tests.append(mk(
        "RM-MUT-04",
        "Degenerate metric mutant",
        "METRIC_DEGENERACY_CANDIDATE",
        "METRIC_DEGENERACY_CANDIDATE" if ok else "MISCLASSIFIED",
        ok,
        {
            "lambda_min": lam_min,
            "tf1_status": "REJECTED_ON_REGULAR_INTERIOR",
            "intrinsic_singularity": "NOT_INFERRED",
        },
    ))

    # RM-MUT-05: deliberately wrong tensor transformation.
    g2_wrong = np.eye(2)
    wrong_residual = float(np.linalg.norm(g1 - A.T @ g2_wrong @ A, ord=2))
    ok = wrong_residual > RESIDUAL_TOL
    tests.append(mk(
        "RM-MUT-05",
        "Incorrect tensor-transformation mutant",
        "DETECTED_AS_O8_C",
        "DETECTED_AS_O8_C" if ok else "MISSED",
        ok,
        {
            "compatibility_residual_norm": wrong_residual,
            "threshold": RESIDUAL_TOL,
        },
    ))

    # RM-MUT-06: ill-conditioned but non-singular metric.
    g = np.diag([1.0, 1e-10])
    vals = np.linalg.eigvalsh(g)
    lam_min = float(vals.min())
    cond = float(vals.max() / vals.min())
    ok = lam_min > POS_EPS and cond > COND_MAX
    tests.append(mk(
        "RM-MUT-06",
        "Ill-conditioned but non-singular metric",
        "CHANGE_CHART_OR_RESTRICT_DOMAIN",
        "CHANGE_CHART_OR_RESTRICT_DOMAIN" if ok else "MISCLASSIFIED",
        ok,
        {
            "lambda_min": lam_min,
            "condition_number": cond,
            "condition_threshold": COND_MAX,
            "singular": False,
        },
    ))

    # RM-O8S-07: boundary-only rank loss.
    interior_grid = np.linspace(0.1, 1.0, 100)
    interior_lower = float(np.min(interior_grid**2))
    boundary_lower = 0.0
    ok = interior_lower > POS_EPS and abs(boundary_lower) <= POS_EPS
    tests.append(mk(
        "RM-O8S-07",
        "Boundary-only rank loss as O8-S handoff",
        "DETECTED_AS_O8_S",
        "DETECTED_AS_O8_S" if ok else "MISCLASSIFIED",
        ok,
        {
            "metric_family": "diag(1, t^2)",
            "certified_regular_domain": "0.1 <= t <= 1",
            "interior_lambda_min_lower_bound": interior_lower,
            "boundary_t": 0.0,
            "boundary_lambda_min": boundary_lower,
            "o8_i": "NOT_ASSERTED",
        },
    ))

    suite_pass = all(t["passed"] for t in tests)
    report = {
        "suite": "Trinity Reference Metric Suite",
        "suite_version": "0.1",
        "status": "PASS" if suite_pass else "FAIL",
        "gate_effect": (
            "TF1_REFERENCE_METRIC_PREREQ_PASS"
            if suite_pass
            else "TF1_REFERENCE_METRIC_PREREQ_BLOCKED"
        ),
        "tests_total": len(tests),
        "tests_passed": sum(t["passed"] for t in tests),
        "tests_failed": sum(not t["passed"] for t in tests),
        "thresholds": {
            "positive_definiteness_epsilon": POS_EPS,
            "conditioning_max": COND_MAX,
            "residual_tolerance": RESIDUAL_TOL,
        },
        "tests": tests,
        "execution_environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
            "numpy": np.__version__,
            "sympy": sp.__version__,
        },
        "scope_statement": (
            "Reference audit logic only; no concrete Trinity atlas "
            "or production g_T is certified."
        ),
    }
    canonical = json.dumps(
        report, ensure_ascii=False, sort_keys=True, separators=(",", ":")
    ).encode("utf-8")
    report["result_hash"] = hashlib.sha256(canonical).hexdigest()
    return report


if __name__ == "__main__":
    report = run_suite()
    out = Path(__file__).with_name(
        "trinity_reference_metric_suite_v01_result.json"
    )
    out.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )
    print(json.dumps({
        "status": report["status"],
        "gate_effect": report["gate_effect"],
        "tests_passed": report["tests_passed"],
        "tests_total": report["tests_total"],
        "result_hash": report["result_hash"],
    }, ensure_ascii=False, indent=2))
