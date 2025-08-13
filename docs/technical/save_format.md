# Save File Format

Game state is stored as JSON. Example structure:

```json
{
  "player": {
    "name": "Ada",
    "traits": {
      "Hubris": 0.5,
      "Fear": 0.2
    }
  },
  "scene": "end"
}
```

Telemetry output is an array of events:

```json
[
  {
    "event": "choice",
    "id": "door",
    "selection": "open",
    "tags": [
      {"trait": "Hubris", "weight": 0.5},
      {"trait": "Fear", "weight": 0.2}
    ]
  }
]
```
