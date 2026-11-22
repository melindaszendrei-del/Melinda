import Mathlib

/-!
TP01–K_W: FormCoreGate — initial compilation candidate.

This proves only an abstract positivity-transfer lemma. It does NOT
construct the Weil form, prove RH, or certify a native Riemann operator.

Crucial: Form carries its OWN norm topology. Density is checked in Form,
not in Ambient. The form-norm certificate is mandatory.
-/

namespace TP01KW

universe u v w

structure FormDomain
    (Ambient : Type u) (Form : Type v)
    [NormedAddCommGroup Ambient] [NormedSpace ℝ Ambient]
    [NormedAddCommGroup Form] [NormedSpace ℝ Form] where
  embed : Form →L[ℝ] Ambient
  q : Form → ℝ
  lowerBound : ℝ
  lowerBound_nonneg : 0 ≤ lowerBound
  form_norm_sq : ∀ h : Form,
    ‖h‖ ^ 2 = q h + (lowerBound + 1) * ‖embed h‖ ^ 2

/-- Continuity is derived from the certified form-norm identity. -/
theorem FormDomain.continuous_q
    {Ambient : Type u} {Form : Type v}
    [NormedAddCommGroup Ambient] [NormedSpace ℝ Ambient]
    [NormedAddCommGroup Form] [NormedSpace ℝ Form]
    (D : FormDomain Ambient Form) : Continuous D.q := by
  have h1 : Continuous (fun h : Form => ‖h‖ ^ 2) :=
    continuous_norm.pow 2
  have h2 : Continuous (fun h : Form => ‖D.embed h‖ ^ 2) :=
    (continuous_norm.comp D.embed.continuous).pow 2
  have h3 : Continuous (fun h : Form =>
      ‖h‖ ^ 2 - (D.lowerBound + 1) * ‖D.embed h‖ ^ 2) :=
    h1.sub (continuous_const.mul h2)
  have heq : D.q = (fun h : Form =>
      ‖h‖ ^ 2 - (D.lowerBound + 1) * ‖D.embed h‖ ^ 2) := by
    funext h
    have hh := D.form_norm_sq h
    dsimp
    linarith
  rw [heq]
  exact h3

/-- Density in the Form norm topology; ambient density is insufficient. -/
def FormDomain.IsFormCore
    {Ambient : Type u} {Form : Type v} {Test : Type w}
    [NormedAddCommGroup Ambient] [NormedSpace ℝ Ambient]
    [NormedAddCommGroup Form] [NormedSpace ℝ Form]
    (D : FormDomain Ambient Form) (W : Test → Form) : Prop :=
  closure (Set.range W) = Set.univ

/-- Transfer nonnegativity from a form-core and exact representation. -/
theorem nonneg_of_form_core
    {Ambient : Type u} {Form : Type v} {Test : Type w}
    [NormedAddCommGroup Ambient] [NormedSpace ℝ Ambient]
    [NormedAddCommGroup Form] [NormedSpace ℝ Form]
    (D : FormDomain Ambient Form)
    (QTest : Test → ℝ) (W : Test → Form)
    (hcore : D.IsFormCore W)
    (hrep : ∀ f : Test, QTest f = D.q (W f))
    (hpos : ∀ f : Test, 0 ≤ QTest f) :
    ∀ h : Form, 0 ≤ D.q h := by
  have hclosed : IsClosed {h : Form | 0 ≤ D.q h} := by
    change IsClosed (D.q ⁻¹' Set.Ici (0 : ℝ))
    exact isClosed_Ici.preimage D.continuous_q
  have hsubset : Set.range W ⊆ {h : Form | 0 ≤ D.q h} := by
    intro h hh
    rcases hh with ⟨f, rfl⟩
    change 0 ≤ D.q (W f)
    rw [← hrep f]
    exact hpos f
  have hclosure : closure (Set.range W) ⊆ {h : Form | 0 ≤ D.q h} :=
    closure_minimal hsubset hclosed
  intro h
  apply hclosure
  rw [hcore]
  exact Set.mem_univ h

/-- Converse uses only the exact representation, without density. -/
theorem test_nonneg_of_form_nonneg
    {Ambient : Type u} {Form : Type v} {Test : Type w}
    [NormedAddCommGroup Ambient] [NormedSpace ℝ Ambient]
    [NormedAddCommGroup Form] [NormedSpace ℝ Form]
    (D : FormDomain Ambient Form)
    (QTest : Test → ℝ) (W : Test → Form)
    (hrep : ∀ f : Test, QTest f = D.q (W f))
    (hpos : ∀ h : Form, 0 ≤ D.q h) :
    ∀ f : Test, 0 ≤ QTest f := by
  intro f
  rw [hrep f]
  exact hpos (W f)

end TP01KW

#print axioms TP01KW.nonneg_of_form_core
#print axioms TP01KW.test_nonneg_of_form_nonneg
