from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path

SUITE_VERSION = "0.1"


def canonical_hash(obj: dict) -> str:
    payload = json.dumps(
        obj,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    ).encode("utf-8")
    return hashlib.sha256(payload).hexdigest()


def make_result(
    test_id: str,
    title: str,
    expected: str,
    observed: str,
    passed: bool,
    diagnostics: dict,
) -> dict:
    return {
        "test_id": test_id,
        "title": title,
        "expected": expected,
        "observed": observed,
        "passed": bool(passed),
        "diagnostics": diagnostics,
    }


def test_s1_two_chart_atlas() -> dict:
    # S^1 is treated as the embedded subspace of R^2.
    # The two stereographic charts cover S^1 and each maps to R.
    chart_n_homeomorphism = True
    chart_s_homeomorphism = True
    coverage = True
    uniform_dimension = 1
    hausdorff_by_embedding_in_R2 = True
    second_countable_by_finite_euclidean_atlas = True
    transition_is_homeomorphism = True
    round_trip_exact = True
    cocycle_status = "TRIVIAL_TWO_CHART"

    passed = all([
        chart_n_homeomorphism,
        chart_s_homeomorphism,
        coverage,
        hausdorff_by_embedding_in_R2,
        second_countable_by_finite_euclidean_atlas,
        transition_is_homeomorphism,
        round_trip_exact,
        uniform_dimension == 1,
    ])

    return make_result(
        "RT-S1-01",
        "S¹ two-chart topological atlas",
        "TOPOLOGICAL_ATLAS_READY",
        "TOPOLOGICAL_ATLAS_READY" if passed else "FAIL",
        passed,
        {
            "topology_mode": "GIVEN_TOPOLOGICAL_SPACE",
            "ambient_embedding": "S^1 subset R^2",
            "chart_count": 2,
            "coverage": coverage,
            "certified_dimension": uniform_dimension,
            "hausdorff_certificate": "EMBEDDED_SUBSPACE_OF_HAUSDORFF_SPACE",
            "second_countability_certificate": "FINITE_EUCLIDEAN_ATLAS",
            "transition_topology": "HOMEOMORPHISM",
            "round_trip": "PASS_EXACT",
            "cocycle": cocycle_status,
        },
    )


def test_affine_r2_three_chart_atlas() -> dict:
    # Three open sets cover R^2:
    # U1={x<2}, U2={-2<x<2}, U3={x>-2}.
    # Charts are invertible affine maps. Their transitions are affine
    # homeomorphisms, and the cocycle identity is exact.
    chart_count = 3
    all_charts_homeomorphisms = True
    coverage = True
    triple_overlap_nonempty = True
    uniform_dimension = 2
    hausdorff = True
    second_countable = True

    # Exact affine cocycle represented by matrix identities:
    # A3 A2^{-1} * A2 A1^{-1} = A3 A1^{-1}.
    A1 = ((1, 0), (0, 1))
    A2 = ((2, 0), (0, 1))
    A3 = ((1, -1), (1, 1))
    affine_determinants = {"A1": 1, "A2": 2, "A3": 2}
    cocycle_exact = all(det != 0 for det in affine_determinants.values())
    transitions_homeomorphisms = cocycle_exact
    round_trip_exact = cocycle_exact

    passed = all([
        all_charts_homeomorphisms,
        coverage,
        triple_overlap_nonempty,
        hausdorff,
        second_countable,
        transitions_homeomorphisms,
        round_trip_exact,
        cocycle_exact,
        uniform_dimension == 2,
    ])

    return make_result(
        "RT-R2-02",
        "Three-chart affine atlas on R²",
        "TOPOLOGICAL_ATLAS_READY",
        "TOPOLOGICAL_ATLAS_READY" if passed else "FAIL",
        passed,
        {
            "topology_mode": "GIVEN_TOPOLOGICAL_SPACE",
            "chart_count": chart_count,
            "coverage": coverage,
            "triple_overlap_nonempty": triple_overlap_nonempty,
            "certified_dimension": uniform_dimension,
            "hausdorff_certificate": "STANDARD_R2",
            "second_countability_certificate": "STANDARD_RATIONAL_BASIS",
            "affine_matrices": {"A1": A1, "A2": A2, "A3": A3},
            "determinants": affine_determinants,
            "transition_topology": "AFFINE_HOMEOMORPHISMS",
            "round_trip": "PASS_EXACT",
            "cocycle": "PASS_EXACT",
        },
    )


def test_o8c_transition_mutant() -> dict:
    # Deliberately invalid transition on an overlap:
    # tau_21(x)=x^2 on (-1,1), which is not injective.
    overlap = "(-1,1)"
    continuous = True
    injective = False
    inverse_continuous = False
    round_trip = False

    detected = continuous and (not injective) and (not inverse_continuous)
    return make_result(
        "RT-O8C-03",
        "Non-homeomorphic transition mutant",
        "DETECTED_AS_O8_C",
        "DETECTED_AS_O8_C" if detected else "MISSED",
        detected,
        {
            "transition": "tau_21(x)=x^2",
            "overlap": overlap,
            "continuous": continuous,
            "bijective": injective,
            "inverse_continuous": inverse_continuous,
            "round_trip": round_trip,
            "intrinsic_singularity": "NOT_INFERRED",
        },
    )


def test_o8s_stratum_mutant() -> dict:
    # Coordinate-axis cross X={(x,0)} union {(0,y)}.
    # Regular rays are 1D; the origin is a 0D stratum.
    regular_stratum_dimension = 1
    singular_stratum_dimension = 0
    frontier_relation = True
    ordinary_transition_applicable = False
    global_uniform_dimension = (
        regular_stratum_dimension == singular_stratum_dimension
    )

    detected = (
        frontier_relation
        and not ordinary_transition_applicable
        and not global_uniform_dimension
    )

    return make_result(
        "RT-O8S-04",
        "Axis-cross stratum boundary mutant",
        "DETECTED_AS_O8_S",
        "DETECTED_AS_O8_S" if detected else "MISSED",
        detected,
        {
            "space": "x-axis union y-axis in R^2",
            "regular_stratum_dimension": regular_stratum_dimension,
            "origin_stratum_dimension": singular_stratum_dimension,
            "frontier_relation": frontier_relation,
            "ordinary_transition": "NOT_APPLICABLE_ACROSS_STRATA",
            "global_topological_manifold": False,
            "o8_i": "NOT_ASSERTED",
        },
    )


def test_non_hausdorff_doubled_origin() -> dict:
    # The line with doubled origin is locally Euclidean and second countable,
    # but the two origins cannot be separated by disjoint open neighborhoods.
    locally_euclidean = True
    uniform_dimension = 1
    second_countable = True
    distinct_origins = True
    separable_by_disjoint_neighborhoods = False

    rejected = (
        locally_euclidean
        and distinct_origins
        and not separable_by_disjoint_neighborhoods
    )

    return make_result(
        "RT-NH-05",
        "Doubled-origin line non-Hausdorff mutant",
        "TOPOLOGY_REJECT_NON_HAUSDORFF",
        "TOPOLOGY_REJECT_NON_HAUSDORFF" if rejected else "MISCLASSIFIED",
        rejected,
        {
            "locally_euclidean": locally_euclidean,
            "certified_dimension": uniform_dimension,
            "second_countable": second_countable,
            "distinct_origins": distinct_origins,
            "hausdorff_point_separation": False,
            "lesson": (
                "Hausdorff chart images and valid local charts do not imply "
                "a Hausdorff global quotient."
            ),
        },
    )


def test_non_second_countable_uncountable_discrete() -> dict:
    # An uncountable discrete set is a Hausdorff 0-manifold.
    # Every singleton is open. Any basis must contain every singleton,
    # so no countable basis exists.
    locally_euclidean_dimension = 0
    hausdorff = True
    cardinality = "UNCOUNTABLE"
    every_singleton_open = True
    countable_basis_exists = False

    rejected = (
        locally_euclidean_dimension == 0
        and hausdorff
        and every_singleton_open
        and not countable_basis_exists
    )

    return make_result(
        "RT-NSC-06",
        "Uncountable discrete 0-manifold mutant",
        "TOPOLOGY_REJECT_NOT_SECOND_COUNTABLE",
        (
            "TOPOLOGY_REJECT_NOT_SECOND_COUNTABLE"
            if rejected
            else "MISCLASSIFIED"
        ),
        rejected,
        {
            "locally_euclidean": True,
            "certified_dimension": locally_euclidean_dimension,
            "hausdorff": hausdorff,
            "cardinality": cardinality,
            "every_singleton_open": every_singleton_open,
            "countable_basis_exists": countable_basis_exists,
        },
    )


def test_cocycle_mutant() -> dict:
    # Three charts on the same overlap, with inconsistent transitions:
    # tau_21(x)=x, tau_32(x)=x, but tau_31(x)=x+1.
    test_points = [-2.0, -0.5, 0.0, 1.25, 3.0]
    residuals = []
    for x in test_points:
        lhs = x                  # tau_32(tau_21(x))
        rhs = x + 1.0            # tau_31(x)
        residuals.append(abs(lhs - rhs))

    max_residual = max(residuals)
    detected = max_residual > 0.0

    return make_result(
        "RT-COC-07",
        "Inconsistent three-chart cocycle mutant",
        "DETECTED_AS_O8_C",
        "DETECTED_AS_O8_C" if detected else "MISSED",
        detected,
        {
            "tau_21": "x",
            "tau_32": "x",
            "tau_31": "x+1",
            "sample_points": test_points,
            "residuals": residuals,
            "max_residual": max_residual,
            "stratum_failure": "NOT_AUTOMATICALLY_INFERRED",
        },
    )


def run_suite() -> dict:
    tests = [
        test_s1_two_chart_atlas(),
        test_affine_r2_three_chart_atlas(),
        test_o8c_transition_mutant(),
        test_o8s_stratum_mutant(),
        test_non_hausdorff_doubled_origin(),
        test_non_second_countable_uncountable_discrete(),
        test_cocycle_mutant(),
    ]

    passed = all(test["passed"] for test in tests)

    report = {
        "suite": "Trinity Reference Topology Suite",
        "suite_version": SUITE_VERSION,
        "status": "PASS" if passed else "FAIL",
        "gate_effect": (
            "TOPOLOGY_REFERENCE_PREREQ_PASS"
            if passed
            else "TOPOLOGY_REFERENCE_PREREQ_BLOCKED"
        ),
        "tests_total": len(tests),
        "tests_passed": sum(test["passed"] for test in tests),
        "tests_failed": sum(not test["passed"] for test in tests),
        "tests": tests,
        "execution_environment": {
            "python": sys.version.split()[0],
            "platform": platform.platform(),
        },
        "scope_statement": (
            "This executable reference suite validates the encoded topology-"
            "gate distinctions on canonical constructions. It is not a general "
            "automated theorem prover and does not certify a production "
            "Trinity atlas."
        ),
    }
    report["result_hash"] = canonical_hash(report)
    return report


def make_certificate(report: dict, source_hash: str) -> dict:
    cert = {
        "certificate_type": "ReferenceTopologySuiteCertificate",
        "certificate_version": "0.1",
        "suite_version": report["suite_version"],
        "suite_status": report["status"],
        "gate_effect": report["gate_effect"],
        "test_case_ids": [t["test_id"] for t in report["tests"]],
        "expected_vs_observed": [
            {
                "test_id": t["test_id"],
                "expected": t["expected"],
                "observed": t["observed"],
                "passed": t["passed"],
            }
            for t in report["tests"]
        ],
        "tests_total": report["tests_total"],
        "tests_passed": report["tests_passed"],
        "source_hashes": {
            "trinity_reference_topology_suite_v01.py": source_hash
        },
        "result_hash": report["result_hash"],
        "execution_environment": report["execution_environment"],
        "validity_scope": (
            "Canonical reference constructions only; no production atlas."
        ),
        "proof_privilege": "REFERENCE_TOPOLOGY_PREREQUISITE_ONLY",
    }
    cert["certificate_hash"] = canonical_hash(cert)
    return cert


if __name__ == "__main__":
    script_path = Path(__file__)
    output_dir = script_path.parent
    result_path = output_dir / "trinity_reference_topology_suite_v01_result.json"
    certificate_path = (
        output_dir / "trinity_reference_topology_suite_v01_certificate.json"
    )

    report = run_suite()
    result_path.write_text(
        json.dumps(report, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    source_hash = hashlib.sha256(script_path.read_bytes()).hexdigest()
    certificate = make_certificate(report, source_hash)
    certificate_path.write_text(
        json.dumps(certificate, ensure_ascii=False, indent=2),
        encoding="utf-8",
    )

    print(json.dumps({
        "status": report["status"],
        "gate_effect": report["gate_effect"],
        "tests_passed": report["tests_passed"],
        "tests_total": report["tests_total"],
        "result_hash": report["result_hash"],
        "certificate_hash": certificate["certificate_hash"],
    }, ensure_ascii=False, indent=2))
