#!/usr/bin/env python3
"""Trinity REG-REFERENCE-1, independent prototype v0.1.

Tests nine *specified canonical examples*. This is neither a general
transversality prover nor a certificate for the Trinity state space.
"""
from __future__ import annotations

import hashlib
import json
import platform
import sys
from pathlib import Path
from fractions import Fraction
from datetime import datetime, timezone

import sympy as sp

VERSION = "0.1"
X, Y, U, V, T = sp.symbols('x y u v t', real=True)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def canonical_bytes(d: dict) -> bytes:
    return json.dumps(d, ensure_ascii=False, sort_keys=True, separators=(",", ":")).encode("utf-8")


def equal(a, b) -> bool:
    return sp.simplify(a - b) == 0


def jac_rank(f: sp.Matrix, coords: tuple[sp.Symbol, ...], values: dict) -> int:
    return int(f.jacobian(coords).subs(values).rank())


def item(test_id, title, expected, observed, predicate, diagnostics, limits):
    return {
        "test_id": test_id,
        "title": title,
        "expected": expected,
        "observed": observed,
        "passed": bool(predicate and expected == observed),
        "diagnostics": diagnostics,
        "scope_limit": limits,
    }


def test_1():
    F = sp.Matrix([Y])
    J = F.jacobian((X, Y))
    samples = [(0, 0), (1, 0), (-3, 0), (sp.Rational(1, 2), 0)]
    regular = J.rank() == 1 and all(F.subs({X:a, Y:b}) == sp.zeros(1,1) and jac_rank(F, (X,Y), {X:a,Y:b}) == 1 for a,b in samples)
    exact = equal(F[0], Y) and equal(J[0,1], 1)
    ok = bool(regular and exact)
    return item("RR-01", "Smooth regular value F(x,y)=y", "REG1_REGULAR_VALUE_CERTIFIED", "REG1_REGULAR_VALUE_CERTIFIED" if ok else "FAIL", ok,
        {"jacobian":str(J), "rank":J.rank(),"zero_set":"y = 0", "codimension":1,"exact_identity":exact},
        "A concrete regular-value theorem premise, not a general proof engine.")


def test_2():
    F = Y
    A = sp.Matrix([[2,1],[1,1]])
    b = sp.Matrix([1,-2])
    new = A*sp.Matrix([U,V])+b
    pulled = sp.expand(F.subs({X:new[0], Y:new[1]}))
    J_old = sp.Matrix([F]).jacobian((X,Y))
    J_new = sp.Matrix([pulled]).jacobian((U,V))
    chain = J_old*A
    inv = A.inv()
    round_trip = inv*(new-b)
    tangent_old = sp.Matrix([1,0])
    tangent_new = inv*tangent_old
    ok = all([A.det()!=0, sp.simplify(J_new-chain)==sp.zeros(1,2), J_new.rank()==J_old.rank()==1,
              sp.simplify(round_trip-sp.Matrix([U,V])) == sp.zeros(2,1),
              sp.simplify(J_new*tangent_new)==sp.zeros(1,1),
              sp.simplify(pulled - new[1])==0])
    return item("RR-02", "Affine coordinate invariance", "ZERO_LOCUS_INVARIANT+TRANSVERSALITY_INVARIANT", "ZERO_LOCUS_INVARIANT+TRANSVERSALITY_INVARIANT" if ok else "FAIL",ok,
        {"affine_matrix":str(A),"determinant":str(A.det()),"pulled_back_F":str(pulled),"jacobian_chain":str(J_new),"rank":J_new.rank(),"tangent_kernel_preserved":True if ok else False},
        "Demonstrates one invertible affine coordinate change only.")


def test_3():
    # F(x,y) = y + |x|^(3/2); derivative in x = 3/2 sgn(x) sqrt(|x|), continuous at 0.
    # One-sided second derivative ~ 3/(4 sqrt(|x|)) diverges as x -> 0.
    plus_derivative_limit = sp.limit(sp.Rational(3,2)*sp.sqrt(X), X, 0, dir='+')
    minus_derivative_limit = sp.limit(-sp.Rational(3,2)*sp.sqrt(-X), X, 0, dir='-')
    right_second = sp.limit(sp.Rational(3,4)/sp.sqrt(X), X, 0, dir='+')
    J_at_0 = sp.Matrix([[0,1]])
    ok = bool(plus_derivative_limit==0 and minus_derivative_limit==0 and right_second==sp.oo and J_at_0.rank()==1)
    return item("RR-03", "C1 defect on C1 atlas (not C2)", "REG1_READY_C1", "REG1_READY_C1" if ok else "FAIL",ok,
        {"function":"F(x,y)=y+|x|^(3/2)","one_sided_first_derivative_limits":[str(plus_derivative_limit),str(minus_derivative_limit)],"second_derivative_right_limit":str(right_second),"dy_coefficient":1,"rank_at_x0":J_at_0.rank()},
        "Uses an analytic C1 argument on a specific non-C2 function; not an automatic C1 classifier.")


def test_4():
    F = X**3
    JF = sp.diff(F,X)
    alt = X
    roots = sp.solveset(sp.Eq(F,0),X,domain=sp.S.Reals)
    roots_alt = sp.solveset(sp.Eq(alt,0),X,domain=sp.S.Reals)
    ok = bool(roots==roots_alt==sp.FiniteSet(0) and JF.subs(X,0)==0 and sp.diff(alt,X)==1)
    return item("RR-04", "Nontransverse but embedded zero locus x^3", "REGULAR_VALUE_CERTIFICATE_FAILED+ALTERNATIVE_EMBEDDING_CERTIFIABLE", "REGULAR_VALUE_CERTIFICATE_FAILED+ALTERNATIVE_EMBEDDING_CERTIFIABLE" if ok else "FAIL",ok,
        {"zero_set":str(roots),"original_derivative_at_zero":str(JF.subs(X,0)),"alternative_defining_function":"G(x)=x", "alternative_derivative_at_zero":1, "o8_c":"NOT_INFERRED"},
        "An explicit alternative defining function certifies this particular singleton, not every failed rank test.")


def test_5():
    F = X*Y
    grad = sp.Matrix([sp.diff(F,X),sp.diff(F,Y)])
    factors = sp.factor(F)
    rank_origin = int(grad.subs({X:0,Y:0}).rank())
    rank_axis_x = int(grad.subs({X:1,Y:0}).rank())
    rank_axis_y = int(grad.subs({X:0,Y:1}).rank())
    zero_components = sp.solveset(sp.Eq(F.subs(Y,0),0), X, domain=sp.S.Reals) == sp.S.Reals and sp.solveset(sp.Eq(F.subs(X,0),0),Y,domain=sp.S.Reals)==sp.S.Reals
    ok = bool(equal(factors,X*Y) and rank_origin==0 and rank_axis_x==rank_axis_y==1 and zero_components)
    return item("RR-05", "Crossing zero locus xy", "REG1_STRATIFIED_CRITICAL_LOCUS+O8-S", "REG1_STRATIFIED_CRITICAL_LOCUS+O8-S" if ok else "FAIL",ok,
        {"factors":str(factors),"gradient":str(grad),"rank_origin":rank_origin,"rank_on_sampled_axis_points":[rank_axis_x,rank_axis_y],"strata":"four open rays + crossing origin", "o8_i":"NOT_ASSERTED"},
        "Crossing structure is deduced from the explicit factorization, not inferred from rank loss alone.")


def test_6():
    F = Y**2-X**3
    grad = sp.Matrix([sp.diff(F,X),sp.diff(F,Y)])
    gradient_at_cusp = grad.subs({X:0,Y:0})
    t_curve = sp.Matrix([T**2, T**3])
    param_on_zero = sp.expand(F.subs({X:t_curve[0], Y:t_curve[1]}))
    param_derivative_at_cusp = t_curve.diff(T).subs(T,0)
    ok = bool(gradient_at_cusp==sp.zeros(2,1) and param_on_zero==0 and param_derivative_at_cusp==sp.zeros(2,1))
    return item("RR-06", "Cusp y²-x³", "REG1_NONTRANSVERSE_UNRESOLVED", "REG1_NONTRANSVERSE_UNRESOLVED" if ok else "FAIL",ok,
        {"gradient_at_origin":str(gradient_at_cusp),"parametrization":str(t_curve),"parametrized_zero_identity":str(param_on_zero),"parametrization_derivative_at_zero":str(param_derivative_at_cusp),"o8_i":"NOT_ASSERTED"},
        "Detects the specified singular parametrization; no intrinsic O8-I certificate issued.")


def test_7():
    sa = sp.Matrix([U,V])
    G = sp.diag(2,3)
    sb_valid = G*sa
    sb_invalid = sp.Matrix([2*U,3*V+1])
    invalid_residual = sp.simplify(sb_invalid-G*sa)
    valid_residual = sp.simplify(sb_valid-G*sa)
    ok = bool(G.det()!=0 and valid_residual==sp.zeros(2,1) and invalid_residual!=sp.zeros(2,1))
    return item("RR-07", "Inconsistent bundle transition", "O8-C", "O8-C" if ok else "FAIL",ok,
        {"transition_matrix":str(G),"invertible":G.det()!=0,"valid_residual":str(valid_residual),"mutant_residual":str(invalid_residual)},
        "Tests a concrete rank-2 trivial bundle local gluing condition, not general bundle topology.")


def test_8():
    estimate=Fraction(1,20)
    error=Fraction(1,10)
    lower=estimate-error
    upper=estimate+error
    cannot_prove_full_rank=(lower<=0<=upper)
    ok=bool(cannot_prove_full_rank and upper>lower)
    return item("RR-08", "Uncertain derivative interval", "O8-E", "O8-E" if ok else "FAIL",ok,
        {"derivative_estimate":str(estimate),"error":str(error),"interval":[str(lower),str(upper)],"zero_in_interval":cannot_prove_full_rank,"conclusion":"RANK_UNDETERMINED"},
        "A modeled interval uncertainty, not an experimentally calibrated estimator.")


def test_9():
    # M=[0,infty), F(x)=x: zero is on boundary, dF/dx=1; no automatic O8-S.
    F=X
    zero=sp.solveset(sp.Eq(F,0), X, domain=sp.Interval(0,sp.oo))
    dF0=sp.diff(F,X).subs(X,0)
    boundary_at_zero = 0 in zero
    boundary_restriction_dim=0
    ok=bool(zero==sp.FiniteSet(0) and dF0==1 and boundary_at_zero and boundary_restriction_dim==0)
    return item("RR-09", "Manifold-with-boundary [0,∞), F(x)=x", "BOUNDARY_REGULARITY_REVIEW+NO_AUTOMATIC_O8-S", "BOUNDARY_REGULARITY_REVIEW+NO_AUTOMATIC_O8-S" if ok else "FAIL",ok,
        {"manifold":"[0, infinity)","zero_set":str(zero),"ambient_derivative_at_zero":str(dF0),"zero_lies_on_boundary":boundary_at_zero,"boundary_stratum_dimension":boundary_restriction_dim,"o8_s":"NOT_AUTOMATIC"},
        "Boundary preimage theorem has extra hypotheses; this test deliberately requests separate review instead of issuing a manifold certificate.")


def run() -> dict:
    tests=[]
    for test_fn in [test_1,test_2,test_3,test_4,test_5,test_6,test_7,test_8,test_9]:
        try:
            tests.append(test_fn())
        except Exception as exc:
            tests.append(item(test_fn.__name__,"test execution failure","PASS","EXCEPTION",False,{"error":repr(exc)},"No certificate on exception."))
    passed=sum(t["passed"] for t in tests)
    source=Path(__file__).read_bytes()
    report={
        "suite":"Trinity Reference Regularity Suite",
        "suite_version":VERSION,
        "status":"PASS" if passed==len(tests)==9 else "FAIL",
        "gate_effect":"REG_REFERENCE_DIAGNOSTICS_PASS" if passed==9 else "REG_REFERENCE_DIAGNOSTICS_BLOCKED",
        "tests_total":len(tests),"tests_passed":passed,"tests_failed":len(tests)-passed,
        "tests":tests,
        "source_sha256":sha256(source),
        "environment":{"python":sys.version.split()[0],"sympy":sp.__version__,"platform":platform.platform()},
        "scope_statement":"Nine canonical example-specific diagnoses. Not a general regularity, embedding or stratification prover. No TFREG1Certificate, no Trinity atlas certificate, no WTT privilege.",
        "readiness":"REFERENCE_TEST_ONLY / REG_RUNTIME_NOT_IMPLEMENTED / GEOMETRIC_INSTANCE_PENDING",
    }
    report["result_sha256"] = sha256(canonical_bytes(report))
    return report


def main():
    outdir=Path(__file__).parent
    result=run()
    (outdir/"trinity_reference_regularity_suite_v01_result.json").write_text(json.dumps(result,indent=2,ensure_ascii=False)+"\n", encoding="utf-8")
    run_record={
        "record_type":"ReferenceRegularitySuiteExecutionRecord",
        "version":"0.1",
        "suite_status":result["status"],
        "source_sha256":result["source_sha256"],
        "result_sha256":result["result_sha256"],
        "test_case_ids":[t["test_id"] for t in result["tests"]],
        "scope":"EXAMPLE_SPECIFIC_REFERENCE_TESTS_ONLY",
        "proof_privilege":"NO_GENERAL_REGULARITY_OR_TRINITY_GEOMETRY_CERTIFICATION",
        "tfreg1_certificate_issued":False,
        "execution_prerequisite_gate":"REG_REFERENCE_DIAGNOSTICS_PASS" if result["status"]=="PASS" else "BLOCKED",
        "execution_environment":result["environment"],
    }
    run_record["record_sha256"]=sha256(canonical_bytes(run_record))
    (outdir/"trinity_reference_regularity_suite_v01_run_record.json").write_text(json.dumps(run_record,indent=2,ensure_ascii=False)+"\n",encoding="utf-8")
    log = [f"Trinity REG-REFERENCE-1 prototype v{VERSION}", f"STATUS: {result['status']} ({result['tests_passed']}/{result['tests_total']})",f"Source SHA256: {result['source_sha256']}",f"Result SHA256: {result['result_sha256']}"]
    log.extend(f"{t['test_id']}  {'PASS' if t['passed'] else 'FAIL'}  {t['observed']}" for t in result["tests"])
    log.append("Scope: EXAMPLE_SPECIFIC_REFERENCE_TESTS_ONLY; no TFREG1 certificate issued")
    (outdir/"trinity_reference_regularity_suite_v01_run.log").write_text("\n".join(log)+"\n",encoding="utf-8")
    print("\n".join(log))
    if result["status"] != "PASS":
        sys.exit(1)


if __name__ == "__main__":
    main()
