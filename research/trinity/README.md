# Trinity geometry — reference code and recovery status

This directory contains **three example-specific reference suites** recovered from the research trajectory. These are not a certified Trinity state space, a general-purpose manifold auditor or a proof of mathematical novelty.

| Suite | Cases | Meaning |
| --- | ---: | --- |
| Metric v0.1 | 7 | Reference diagnostic behavior for metric conditions |
| Topology v0.1 | 7 | Fixed canonical examples, **several predicates hardcoded** |
| Regularity v0.1 | 9 | Symbolic/example-specific rank, zero-locus, and O8 diagnostics |

The example suites have run locally (7/7 + 7/7 + 9/9). CI must independently verify the committed code.

## Scope and limitations
- Topology v0.1 includes **hardcoded mathematical assumptions**: a green test is not an independently checked topological theorem.
- Regularity v0.1 demonstrates nine canonical cases only, not a general certificate validator.
- Local/observational success must not be elevated to global claims.
- No concrete Trinity atlas, global Trinity metric, defect bundle, soundness theorem, or TF-REG-1 certificate is provided here.
- O8-I cannot be assigned automatically from a rank failure.
- The separate TP01–K_W Lean work belongs to a distinct mathematical research branch. It does not prove RH.

## Provenance
The metric and topology scripts were recovered from earlier user Library artifacts. The regularity script was separately developed from the supplied nine-case TF-REG-1 test specification. The original historical source documents and OneDrive archives are **not** copied here. No pre-existing source file is overwritten.

## Running
```bash
python -m pip install numpy==2.3.5 sympy==1.14.0
python research/trinity/reference_suites/trinity_reference_metric_suite_v01.py
python research/trinity/reference_suites/trinity_reference_topology_suite_v01.py
python research/trinity/reference_suites/trinity_reference_regularity_suite_v01.py
```
Output JSON and run logs are generated next to the scripts.

**Development gate:** candidate reference diagnostics only. **Production proof privilege:** none.
