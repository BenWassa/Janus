# Sprint 8 – Playtest & Balancing

## Playtest Feedback Synthesis
- Test run logs showed Wrath accruing faster than other traits and highlighted repeated use of decoy Apathy choices.
- Players reported in surveys that Moodiness and Rigidity seldom triggered payoffs and that Wrath felt overly rewarded.

## Recommended Weight Adjustments
- Reduced Wrath weighting in the `feeding_pit` scene and added balancing secondary weights.
- Introduced secondary Moodiness and Control weights in early Act 1 scenes to diversify signals.
- Converted several Apathy decoys to actual trait tags (Rigidity, Control, Cynicism) to close avoidance exploits.

## Revised Scenes and Tags
- `mirror_pool.wait_silently` now tags **Rigidity** with a micro weight.
- `caged_lion.open_gate` now registers **Impulsivity** instead of a zero-weight Apathy decoy.
- `sealed_letter.deliver_unopened` reflects **Rigidity** rather than a no-weight choice.

## Payoff Frequency Updates
- Added midgame micro payoffs for **Cynicism**, **Moodiness**, and **Rigidity** so every trait now has two triggers.

Source data for these adjustments can be found in `data/playtests/logs.json` and `data/playtests/survey_results.json`.
