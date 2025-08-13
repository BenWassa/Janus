## **Sprint 20 – Story Spine & Continuity Pass**

**Goal:**
Create a connected journey where earlier choices influence later scenes through state tracking and narrative callbacks.

**Tasks for LLM:**

1. **Add State Manager**

   * Create a persistent Python dictionary to store flags and trait scores (`state_flags` and `trait_scores`).
   * Save state to the current run’s memory object so later scenes can read and branch.

2. **Insert Act Intros & Interludes**

   * For each act start, insert a short narrative paragraph referencing relevant `state_flags`.
   * For act transitions, generate an interlude that summarises key prior actions.

3. **Add State-Driven Scene Variations**

   * In each Act 2 and Act 3 scene, check for at least one prior `state_flag`.
   * If present, alter description, available choices, or both.

4. **Define Symbol Anchors**

   * Assign `mirror`, `beast`, and `storm` as keys in `state_flags`.
   * Track how the player interacted with each and call these in later references.

**Example:**

```python
if state_flags.get("chimera_spared"):
    print("The chimera you spared in the pit now follows at a distance, its mirrored hide glinting.")
else:
    print("The pit is empty; the chimera is gone, leaving only dust and claw marks.")
```

---

## **Sprint 21 – Internal Mythos & Meaning Mapping**

**Goal:**
Give recurring imagery functional meaning linked to traits and earlier actions.

**Tasks for LLM:**

1. **Create Symbol–Trait Map**

   * Mirror → `self_reflection` / `avoidance`
   * Beast → `aggression` / `restraint`
   * Storm → `unresolved_conflict` / `decisiveness`

2. **Tag Symbol Scenes**

   * Add a `symbol` property to each scene definition where imagery appears.
   * Connect this property to relevant traits in the scoring engine.

3. **Symbol Evolution Rules**

   * Modify description of symbol scenes based on dominant related trait score.
   * Example: high `aggression` makes the beast more hostile; high `restraint` makes it wary but respectful.

4. **Consistency Layer**

   * Store all symbol descriptions and variations in a central `symbols.py` module for reuse across acts.

**Example:**

```python
if trait_scores["aggression"] > 3:
    beast_desc = "The beast growls low, testing your resolve."
else:
    beast_desc = "The beast tilts its head, cautious but unafraid."
```

---

## **Sprint 22 – Hero’s Chronicle & Psychological Payoff**

**Goal:**
Generate a personalised endgame summary that recaps key choices, assigns an archetype, and delivers a final symbolic scene.

**Tasks for LLM:**

1. **Enhance Trait Scoring Engine**

   * Every scene choice must include a `traits_impact` dict to adjust scores.
   * Update `trait_scores` live during play.

2. **Decision Recap Generator**

   * At game end, select 3–4 decisions with highest narrative weight (based on state flags).
   * Render them in narrative form before profile output.

3. **Archetype Generator**

   * Create a mapping of top 1–2 traits to one of at least 5 archetypes.
   * Example mapping:

     * High `self_reflection` + high `restraint` → “The Harmonizer”
     * High `aggression` + low `restraint` → “The Challenger”

4. **Final Symbolic Scene**

   * Pull symbol variations based on state flags and dominant traits.
   * Combine into 3–5 sentence epilogue.

5. **Output Structure:**

   ```
   === Hero’s Chronicle ===
   [Decision Recap]
   [Archetype Name & Description]
   [Final Symbolic Epilogue]
   ```

**Example Archetype Output:**

```python
print("=== Hero’s Chronicle ===")
print("You spared the chimera, refused the contract, and took the dangling key.")
print("The Harmonizer: You resist chaos, seek balance, and avoid dominance.")
print("As you leave the labyrinth, the chimera walks beside you. The storm has passed, but the mirror pool still waits.")
```
