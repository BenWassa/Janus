# Commissioning Document – "Hamartia Engine" Game v2
## Purpose
To deliver a fully functional v2 of the interactive personality-profiling text RPG (“Hamartia Engine”), with expanded content, robust trait tagging, psychological weightings, decoys, and trait-gated narrative payoffs.
Execution will be broken into discrete, AI-friendly sprints (one sprint per week) so each can be completed in a single LLM pass.

## Stock Context Document (given with every sprint)
This is the core reference for all sprints.
It ensures every AI agent has the same foundational understanding.

## Project Overview
We are building a narrative-driven text RPG that infers the player’s psychological “fatal flaw” profile through their choices.
Version 2 will triple content, introduce decoy/no-weight choices, balance trait weighting, and include micro/mid/endgame narrative payoffs tied to the player’s top traits.

## Core Traits (v2 candidate set):

Hubris (pride/arrogance)

Avarice (greed/materialism)

Deception (manipulation/dishonesty)

Control (perfectionism/domineering)

Wrath (anger/revenge)

Fear (anxiety/timidity)

Impulsivity (recklessness/overindulgence)

Envy (resentment/comparison)

Apathy (indifference/laziness)

Cynicism (negativity/mistrust)

Moodiness (emotional volatility/indirectness)

Rigidity (inflexibility/dogmatism)

Weighting Rubric:

0 = decoy (no trait influence)

+0.2 = micro choice (minor signal)

+0.5 = mid-stakes choice

+0.8 = major choice (high signal)

Per scene cap: +0.8 combined

Per trait cap per act: +2.0 soft cap

## Story Structure:
Three acts (Mirrors, Beasts, Whispers), each with micro, mid, and optional pocket scenes. Endgame reveal based on top 3 traits (constellation).

## Narrative Continuum:
Traits expressed as spectrums — e.g., Hubris (confidence ↔ arrogance), Fear (prudence ↔ paralysis). The reveal frames them as reflections, not moral verdicts.