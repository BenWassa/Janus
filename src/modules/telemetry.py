"""Lightweight telemetry logging."""
from __future__ import annotations

import json
from pathlib import Path
from typing import Any, Dict, List, Optional


class Telemetry:
    """Collects and writes gameplay events to JSON."""

    def __init__(self, path: Optional[str] = None):
        self.events: List[Dict[str, Any]] = []
        self.path = Path(path) if path else None

    def log(self, event: Dict[str, Any]) -> None:
        if self.path:
            self.events.append(event)

    def save(self) -> None:
        if self.path:
            with open(self.path, "w", encoding="utf-8") as f:
                json.dump(self.events, f, indent=2)
