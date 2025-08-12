from pathlib import Path
import json
import sys

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from modules.telemetry import Telemetry


def test_telemetry_logs_choice(tmp_path):
    log_file = tmp_path / "log.json"
    tel = Telemetry(str(log_file))
    tel.log({
        "event": "choice",
        "id": "door",
        "selection": "open",
        "primary_trait": "Hubris",
        "primary_weight": 0.5,
        "secondary_trait": "Fear",
        "secondary_weight": 0.2,
    })
    tel.save()
    data = json.loads(log_file.read_text())
    assert data[0]["primary_trait"] == "Hubris"
    assert data[0]["secondary_weight"] == 0.2
