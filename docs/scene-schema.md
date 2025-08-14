# Scene JSON Schema

This document defines the structure for narrative scene files used in the
`pilot_humility_hubris` prototype. Scenes are stored as individual JSON files
in `pilot_humility_hubris/scenes/` and are loaded at runtime.

## Top-level fields

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Unique identifier for the scene. |
| `act` | string | Optional act or chapter label. |
| `title` | string | Display title of the scene. |
| `subtitle` | string | Optional subtitle shown beneath the title. |
| `text` | string | Main body text presented to the player. |
| `thread` | string | Optional thread or story line identifier used for callbacks. |
| `set_flags` | array<string> | Flags set when this scene is entered. |
| `require_flags` | array<string> | Flags required to enter the scene. |
| `options` | array<object> | Available choices for the player. |

## Option fields

Each entry in `options` represents a player choice.

| Field | Type | Description |
| ----- | ---- | ----------- |
| `id` | string | Unique identifier for this option within the scene. |
| `label` | string | Text shown on the choice button. |
| `whisper` | string | Short feedback line shown after selection. |
| `delta` | object | Trait adjustments keyed by trait name. Values are numeric weights (e.g. `0.2`, `0.5`, `0.8`). |
| `next` | string or null | Identifier of the next scene. `null` ends the run. |
| `set_flags` | array<string> | Flags set when this option is taken. |
| `require_flags` | array<string> | Flags required for the option to appear. |

All fields other than `id`, `title`, `text`, and `options` are optional.

## Replay metadata

Preview scripts may record a `seed` and the sequence of option `id`s chosen.
Replaying with the same seed and path will produce deterministic runs.

## Example

```json
{
  "id": "mirror_pool",
  "act": "Act I · Mirrors",
  "title": "Mirror Pool",
  "subtitle": "A still pool mirrors the sky; your reflection waits for a ripple.",
  "text": "The surface holds your outline with too much patience.",
  "thread": "mirrors",
  "options": [
    {
      "id": "disturb",
      "label": "Disturb the surface and watch your face fracture.",
      "whisper": "You broke the stillness first.",
      "delta": {"Hubris": 0.6, "Impulsivity": 0.2},
      "next": "twin_scholar"
    }
  ]
}
```
