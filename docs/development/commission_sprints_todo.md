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
