# Commissioning Document – "Hamartia Engine" Game v2
## Purpose
Deliver a fully functional v2 of the interactive personality-profiling text RPG (“Hamartia Engine”), culminating in a personalized "Hero's Chronicle" that reflects the player's psychological constellation. v2 expands content, refines trait tagging, introduces decoys, and upgrades payoff systems for nuanced, archetype-based endings.

## Stock Context Document (given with every sprint)
This is the core reference for all sprints, ensuring every AI agent and contributor shares the same foundational understanding and vision.

## Project Overview
Project Janus blends classic text adventure with covert psychological profiling. Player choices shape the story and build a profile across a spectrum of traits, revealed through narrative payoffs and a constellation-based endgame. v2 features:
- Tripled content and scenario depth
- Decoy/no-weight choices for realism
- Balanced trait weighting and tagging API
- Micro/mid/endgame payoffs tied to top traits
- Archetype generator for personalized endings
- Save/load, telemetry, and HUD for testing and analysis

## Core Traits (v2 candidate set):

Traits are tracked on spectrums (virtue ↔ flaw), never as binary categories. The current set includes:
- Hubris (confidence ↔ arrogance)
- Avarice (ambition ↔ greed)
- Deception (tact ↔ dishonesty)
- Control (order ↔ domineering)
- Wrath (assertiveness ↔ revenge)
- Fear (prudence ↔ paralysis)
- Impulsivity (spontaneity ↔ recklessness)
- Envy (aspiration ↔ resentment)
- Apathy (calm ↔ indifference)
- Cynicism (skepticism ↔ mistrust)
- Moodiness (sensitivity ↔ volatility)
- Rigidity (consistency ↔ dogmatism)

## Weighting Rubric:

0 = decoy (no trait influence)
0.2 = micro choice (minor signal)
0.5 = mid-stakes choice
0.8 = major choice (high signal)
Per scene cap: +0.8 combined
Per trait cap per act: +2.0 soft cap

## Story Structure:
Three acts (Mirrors, Beasts, Whispers), each with micro, mid, and optional pocket scenes. Endgame reveal is constellation-based, reflecting the player's top 3 traits through narrative artifacts, archetype mapping, and symbolic scenes.

## Narrative Continuum & Payoff System:
Traits are expressed as spectrums. Narrative payoffs (micro, mid, endgame) are delivered through story callbacks, NPC reactions, and customized epilogues. The reveal frames traits as reflections, not verdicts, and offers both cautionary and celebratory interpretations.

## Ethical Principles:
- Profiling is opt-in, with clear privacy and data handling policies
- Traits are presented neutrally, avoiding pathologizing or moralizing
- Cultural sensitivity and accessibility are prioritized

## Technical & Testing Notes:
- Modular architecture separates game logic from psychology assessment
- Save/load, telemetry, and HUD features support playtesting and analysis
- Sprints deliver trait glossary, scenario depth, payoff templates, and archetype mapping

## Vision Statement:
Project Janus aims to deepen immersion, increase replay value, and provide subtle, psychologically grounded self-reflection for players. The system is designed for ethical research, robust data collection, and meaningful narrative integration.