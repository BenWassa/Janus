import json
import sys
from pathlib import Path

sys.path.append(str(Path(__file__).resolve().parents[1] / "src"))

from cli.run_writer import write_run
from cli.build_index import build_index


def test_run_writer_and_index(tmp_path):
    results_dir = tmp_path / "data" / "test_results"
    results_dir.mkdir(parents=True)

    run_data = write_run(
        policy_name="hubris",
        seed=42,
        max_steps=5,
        dominance_threshold=80,
        output_dir=results_dir,
    )

    assert (results_dir / f"run_{run_data['runId']}.json").exists()

    index = build_index(results_dir)
    index_file = results_dir / "index.json"
    assert index_file.exists()

    with index_file.open() as fh:
        index_data = json.load(fh)

    assert index_data[0]["runId"] == run_data["runId"]
    assert index_data[0]["policy"] == "hubris"
    assert "normalized" in index_data[0]
