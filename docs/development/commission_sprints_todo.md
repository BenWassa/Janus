## **Sprint 17 – Persistent State & Narrative Callbacks**

**Objective:** Introduce persistent state tracking so early decisions visibly alter later scenes.
**Rationale:** Current alpha lacks cause-and-effect continuity, making choices feel ornamental rather than consequential.
**Deliverables:**

* **State Manager Module** — central Python dict storing flags like `echo_heard=True`.
* **Scene Callback Hooks** — logic that modifies scene text, options, or events based on flags.
* **Act 1 → Act 2 Links** — at least 3 callbacks from Act 1 decisions that manifest in Act 2 scenes.
  **Success Metrics:**
* ≥3 noticeable cause/effect moments per run.
* Player feedback indicates recognition of consequences.

---

## **Sprint 19 – Psychological Payoff System Upgrade**

**Objective:** Replace vague ending text with a concrete, data-driven psychological profile delivered in narrative form.
**Rationale:** Alpha’s ending fails to deliver on the promise of a “Hero’s Chronicle” or meaningful psychological mirror.
**Deliverables:**

* **Trait Scoring Engine Enhancement** — use existing traits + tagged decisions to generate scores.
* **Archetype Generator** — top traits mapped to 3–5 archetypes (e.g., “The Scholar eclipsed the Seeker…”).
* **Ending Template Variants** — narrative framing that blends score output with story resolution.
  **Success Metrics:**
* Endings are recognizably tied to player decisions.
* At least 3 distinct archetypes possible per run.

---

## **Shared Implementation Schema (For Sprints 17 & 19)**

| **Flag Name**    | **Type** | **Trigger Scene**    | **Values**                         | **Effect / Callback Example**               |
| ---------------- | -------- | -------------------- | ---------------------------------- | ------------------------------------------- |
| `echo_heard`     | Boolean  | `echo_parlor`        | `True` / `False`                   | If `True`, voice responds in `frozen_echo`. |
| `twin_defeated`  | Boolean  | `twin_scholar`       | `True` / `False`                   | If `True`, twin sabotages you in Act 2.     |
| `artifact_found` | String   | `shadow_archive`     | e.g., `"mirror_shard"`             | Unlocks dialogue in `guardian_gate`.        |
| `ally_status`    | Enum     | `lantern_market`     | `Friendly` / `Neutral` / `Hostile` | Alters ally support later.                  |
| `courage_level`  | Integer  | Any                  | 0–5                                | Increments from brave/reckless acts.        |
| `mystery_clues`  | Integer  | Investigation scenes | 0–X                                | Impacts clarity of end revelation.          |
