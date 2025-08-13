# Sprint 1 – Trait Glossary & Tagging API

## Trait Glossary

| Trait | Definition | Example In-Story Triggers |
| --- | --- | --- |
| Hubris | Overbearing pride and conviction that one cannot fail. | Boasting about achievements; ignoring wise counsel; taking reckless risks to prove superiority. |
| Avarice | Insatiable desire for wealth or possessions. | Hoarding resources; choosing profit over helping others; refusing to share spoils. |
| Deception | Habitual manipulation or dishonesty to gain advantage. | Lying to an ally; forging documents; hiding true motives during negotiations. |
| Control | Compulsion to direct outcomes and people to maintain order. | Micromanaging companions; rewriting rules mid‑task; insisting actions follow your exact plan. |
| Wrath | Impulse toward anger and retribution. | Threatening revenge; striking out at minor slights; refusing to forgive an insult. |
| Fear | Persistent anxiety that inhibits bold action. | Avoiding confrontation; fleeing from uncertain danger; hesitating despite opportunity. |
| Impulsivity | Acting without forethought or restraint. | Gambling critical supplies; blurting secrets; diving into a challenge without preparation. |
| Envy | Resentful desire for what others possess. | Sabotaging a rival’s success; obsessing over another’s reward; bitter remarks about peers. |
| Apathy | Lack of interest or motivation toward goals or people. | Ignoring pleas for help; skipping responsibilities; letting opportunities pass unnoticed. |
| Cynicism | Distrustful, negative view of others’ motives. | Mocking idealistic plans; assuming every gift hides a trap; dismissing acts of kindness as selfish. |
| Moodiness | Rapid, unpredictable swings in emotional state. | Snapping at allies without cause; withdrawing mid‑conversation; oscillating between enthusiasm and gloom. |
| Rigidity | Inflexible adherence to rules or routines. | Refusing to deviate from tradition; punishing minor infractions harshly; clinging to a plan despite new facts. |

## Tagging API Specification

### `tag(choice, primary_trait, primary_weight, secondary_trait=None, secondary_weight=0.0)`
Pseudocode:
```python
assert primary_trait in TRAITS
assert primary_weight in {0, 0.2, 0.5, 0.8}
choice.tags = [(primary_trait, primary_weight)]
if secondary_trait:
    choice.tags.append((secondary_trait, secondary_weight))
return choice
```

### `normalize(trait_totals, scene_cap=0.8, act_cap=2.0)`
Pseudocode:
```python
# Limit combined weight per scene and soft‑cap per trait per act
scene_total = sum(trait_totals.values())
if scene_total > scene_cap:
    factor = scene_cap / scene_total
    for trait in trait_totals:
        trait_totals[trait] *= factor
for trait, value in trait_totals.items():
    trait_totals[trait] = min(value, act_cap)
return trait_totals
```

### Choice Handling Format
Choices are stored in JSON and loaded by the engine. Each choice includes text and a tag list:
```json
{
  "id": "boast_to_council",
  "text": "Boast of your victory before the council.",
  "tags": [
    {"trait": "Hubris", "weight": 0.8},
    {"trait": "Deception", "weight": 0.2}
  ]
}
```

Additional examples:
```json
{
  "id": "pocket_donation",
  "text": "Secretly pocket the temple donation.",
  "tags": [
    {"trait": "Avarice", "weight": 0.5},
    {"trait": "Deception", "weight": 0.2}
  ]
},
{
  "id": "help_rival",
  "text": "Help your defeated rival to their feet instead of taking their weapon.",
  "tags": [
    {"trait": "Avarice", "weight": 0.0},
    {"trait": "Envy", "weight": -0.2}
  ]
}
```

### Weighting Rubric
- `0` = decoy (no trait influence)
- `+0.2` = micro choice (minor signal)
- `+0.5` = mid-stakes choice
- `+0.8` = major choice (high signal)
- Per scene cap: `+0.8` combined
- Per trait cap per act: `+2.0` soft cap

## Developer HUD Mockup
```
+----------------------------------+
| Trait Delta HUD                  |
+----------------------------------+
| Hubris      1.2 (+0.8) ▲        |
| Avarice     0.4 (+0.0)          |
| Deception   0.2 (+0.2) ▲        |
| Control     0.0 (+0.0)          |
| Wrath       0.0 (+0.0)          |
| Fear        0.0 (+0.0)          |
| Impulsivity 0.0 (+0.0)          |
| Envy       -0.2 (-0.2) ▼        |
| Apathy      0.0 (+0.0)          |
| Cynicism    0.0 (+0.0)          |
| Moodiness   0.0 (+0.0)          |
| Rigidity    0.0 (+0.0)          |
+----------------------------------+
```
The HUD lists current totals with the latest delta in parentheses and arrows indicating increases or decreases.

