### Sprints for Project Janus Prototype "Humility-Hubris" Upgrade 

These sprints prioritize progressive enhancement, starting with refining existing features before integrating more complex ones, and finally expanding content and ensuring robustness.

---

#### **Sprint 1: Core UX/UI Polish & Refinement**

**Goal:** Enhance the visual fidelity, responsiveness, and subtle feedback of the existing prototype features.

*   **Task 1.1: Refine Decision Interfaces (`Orbit Selector`, `Cognitive Lens`)**
    *   **`Orbit Selector`:** Implement more nuanced visual feedback on hover and selection (e.g., subtle pulsing glow, minor scale change, or a brief "arc" animation on selection). Ensure smooth positioning.
    *   **`Cognitive Lens`:** Improve the blur/focus transition, making it smoother and more distinct. Experiment with `saturate()` or `brightness()` alongside `blur()` for clearer visual differentiation of focused options.
    *   **General:** Add subtle entry animations for choice elements when they appear in the `decision` area.
*   **Task 1.2: Enhance Atmospheric Shift & Constellation Bloom**
    *   **Atmosphere:** Refine the `background` transition to be more fluid and less abrupt. Explore adding a subtle, very faint particle effect overlay (e.g., "star dust" or "ethereal motes") that also shifts hue with the `trait` value.
    *   **Constellation Bloom:** Improve the ambient animation of stars; make them subtly "drift" or "flicker" more dynamically. Consider introducing faint, ephemeral "lines" between stars that subtly form and dissolve based on *current* trait influence (even if just for the single trait for now), hinting at connections.
*   **Task 1.3: Polish `Echo Ripple` Feedback**
    *   Experiment with different `ripple` animations (e.g., outward expansion with a light trail, or multiple, fainter ripples emanating from the click point). Adjust color and opacity to be more integrated with the background atmosphere.
*   **Task 1.4: Cross-Device Responsiveness & CSS Optimization**
    *   Thoroughly test on various screen sizes (mobile, tablet, desktop) and ensure all UI elements scale gracefully and remain functional. Optimize CSS for performance and readability.

---

#### **Sprint 2: Multi-Trait System & Initial Ambiguous Feedback**

**Goal:** Integrate the full set of "Hamartia Engine" traits and introduce mid-game feedback mechanisms as conceptual placeholders.

*   **Task 2.1: Implement Full Trait Tracking**
    *   Modify the `trait` variable into an object (`let traits = { Hubris: 0, Avarice: 0, ... }`) to track all 12 core traits from the "Hamartia Engine" commissioning document.
    *   Update `handleChoice` to apply `delta` values to specific traits as defined in new `scenes` data (e.g., `options: [{ delta: { Hubris: +0.6, Avarice: +0.1 }, ... }]`).
    *   Ensure all trait values are clamped within a defined range (e.g., -1 to 1 or 0 to 1).
*   **Task 2.2: Implement `Sigil Accumulation` (Mid-Clarity Feedback)**
    *   Design simple, abstract SVG "sigils" for each trait (e.g., a small flame for "Wrath", a lock for "Control", a broken chain for "Impulsivity").
    *   On the `statusCard`, create a small "Altar" or "Glyph Repository" area. When a choice significantly impacts a trait, the corresponding sigil should faintly appear or subtly glow/animate within this area, reflecting "accumulation" without revealing numerical values.
*   **Task 2.3: Refine `Atmospheric Shift` for Multi-Trait**
    *   Adjust `updateAtmosphere` to blend `bg-hue`, `bg-sat`, and `bg-light` based on the *dominant* 2-3 traits. This will require a mapping logic (e.g., `Cynicism` shifts to cooler, desaturated tones; `Impulsivity` to warmer, more vibrant tones). This provides a more complex, subconscious reflection.
*   **Task 2.4: Initial `Whisper Panel` Decision Interface**
    *   Implement `Whisper Panel` as a selectable option in the `modeSelect`. Initially, it can display one choice at a time as a "whisper" text with "Accept" / "Reject" buttons, cycling through options on rejection. Focus on the poetic presentation.

---

#### **Sprint 3: Scene Navigation & Advanced Reflection**

**Goal:** Introduce `Dream-Walk` and `Tarot Spread` concepts, and enhance the final reflection to be more deeply tied to archetypes.

*   **Task 3.1: Enhance `Dream-Walk` Scene Transitions (`Linear Illusion`)**
    *   Refine the `dissolve` animation for scene changes. Instead of just fading, add subtle visual distortions, color shifts, or a "rippling" effect that makes the transition feel less like a discrete page load and more like a fluid, dream-like shift.
*   **Task 3.2: Implement `Tarot Spread` (Visible Progression)**
    *   On the `statusCard`, create a small visual area (e.g., "The Thread of Fate"). As scenes are completed, a small, abstract "card" (e.g., a simple rectangle with a faint, unique glyph representing the *scene itself* or the *type of decision made*) visually "flips" or "slides" into position, creating a growing "spread" of past vignettes. No trait info, just progression.
*   **Task 3.3: Develop `Archetype Shadowing` Logic**
    *   Create a JavaScript mapping table that links combinations of dominant traits to a set of pre-defined narrative archetypes (e.g., "The Wanderer," "The Sentinel," "The Trickster"). This will be used for the final reflection.
*   **Task 3.4: Enhance `Mythic Persona Portrait` (Multi-Trait)**
    *   Expand the `renderPortraitAndReading` function to generate more complex and varied SVG adornments/distortions based on the player's *dominant archetype* and specific high-scoring traits. The silhouette itself could also subtly change (e.g., more angular for "Rigidity", more fluid for "Impulsivity").

---

#### **Sprint 4: Final Reflection Formats & Content Expansion**

**Goal:** Implement richer final reflection formats and begin expanding narrative content with multi-trait interactions.

*   **Task 4.1: Implement `Cosmic Constellation Narrative`**
    *   Leverage the archetype mapping and dominant traits to generate more detailed and nuanced final "readings" text. Instead of single lines, aim for a short, paragraph-long interpretation that synthesizes 2-3 top traits into a "constellation narrative."
*   **Task 4.2: Refine `Poetic Echo Journal`**
    *   Review and ensure all "whisper" lines are consistently evocative, metaphorical, and contribute to the "ritual text" feel. Implement a simple formatting to break the journal text into stanzas or visual blocks.
*   **Task 4.3: Expand Prototype Narrative Content**
    *   Add 2-3 new scenes to the `scenes` array, carefully designing options that influence multiple core traits (Hubris, Avarice, Deception, etc.) using the v2 weighting rubric (0.2, 0.5, 0.8). Include at least one "decoy" option (delta 0).
*   **Task 4.4: Basic Save/Load System**
    *   Implement `localStorage` based save/load functionality for the current `trait` object, `journal`, `path`, and `sceneIndex`. Add "Save" and "Load" buttons to the HUD. This is a simplified version for prototype purposes.

---

#### **Sprint 5: Testing, Polish, and Documentation**

**Goal:** Ensure robustness, improve usability, and prepare the prototype for broader internal review.

*   **Task 5.1: Comprehensive Internal Playtesting**
    *   Conduct structured playtesting with the expanded content and new UI features. Gather feedback on the clarity of choices, the effectiveness of the ambient feedback, and the perceived accuracy/resonance of the final reflection.
*   **Task 5.2: Bug Fixing & Performance Optimization**
    *   Address all bugs identified during playtesting. Profile JavaScript and CSS for performance bottlenecks and optimize animations or heavy computations.
*   **Task 5.3: Enhanced Introductory & Explanatory Text**
    *   Update the `start-blurb` and any in-game explanatory text (e.g., `subtitle` on `statusCard`) to clearly but subtly convey the multi-trait system and the nature of the psychological profiling. Reiterate ethical principles implicitly where possible (e.g., "reflections, not verdicts").
*   **Task 5.4: Basic Telemetry Logging**
    *   Implement a simple console logging system that records `scene ID`, `choice ID`, `deltas applied`, and the resulting `trait` state after each choice. This will serve as a basic form of the "telemetry" mentioned in the `README.md` for internal analysis.

---

This roadmap provides a clear path to significantly upgrading the Project Janus prototype, moving it closer to the vision of a "symbolic introspection platform" with deep psychological integration.