# TP01–K_W / FormCoreGate — compilation checkpoint

**Scope:** a general topological positivity-transfer lemma with a
form-norm certificate; NOT an RH proof and NOT a constructed Weil operator.

- The type `Form` has its own norm topology.
- `form_norm_sq` ties this norm to `q` and the ambient embedding.
- The forward theorem needs density in `Form`, exact representation,
  and nonnegative tests.
- The converse needs ONLY the exact representation and form positivity.
- A norm identity alone does **not** prove `q ≥ 0`.
- The first version of the project is **UNVERIFIED until CI builds green**.

Remaining mathematical obligations (not discharged here):
a concrete form domain, the quadratic-form property, closedness and
injective ambient embedding where needed, form-core density, and the exact
arithmetic Weil representation. No private research notes are stored here.

For Copilot/DeepSeek review: inspect `TP01KW.lean` and report
exact theorem names, counterexamples, compile errors, and assumptions.
Do not call the result VALID unless Lean builds successfully.
