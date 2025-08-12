"""Command line interface for the testing engine."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
from typing import List

from ..testing.runner import run
from ..testing.policies import POLICIES


def _write_trace(out_file: Path, trace: List[dict]) -> None:
    out_file.parent.mkdir(parents=True, exist_ok=True)
    with out_file.open("w", encoding="utf-8") as fh:
        for step in trace:
            json.dump(step, fh)
            fh.write("\n")


def cmd_run(args: argparse.Namespace) -> None:
    policy_cls = POLICIES[args.policy]
    finals = []
    for i in range(args.runs):
        policy = policy_cls()
        seed = args.seed + i if args.seed is not None else i
        result = run(policy, seed, args.max_steps)
        run_id = f"{args.policy}_seed{seed}_{i:03d}"
        _write_trace(Path(args.output) / f"{run_id}.jsonl", result["trace"])
        finals.append(result["final"])

    print(f"Completed {len(finals)} runs for policy '{args.policy}'.")


def cmd_suite(args: argparse.Namespace) -> None:
    policies = POLICIES if args.all else {args.policy: POLICIES[args.policy]}
    for name, _ in policies.items():
        run_args = argparse.Namespace(
            policy=name,
            seed=args.seed,
            runs=args.runs,
            max_steps=args.max_steps,
            output=args.output,
        )
        cmd_run(run_args)


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(prog="testrig", description="Alpha testing engine")
    sub = parser.add_subparsers(dest="cmd", required=True)

    run_p = sub.add_parser("run", help="execute runs for a single policy")
    run_p.add_argument("--policy", choices=POLICIES.keys(), required=True)
    run_p.add_argument("--seed", type=int, default=0)
    run_p.add_argument("--runs", type=int, default=1)
    run_p.add_argument("--max-steps", type=int, default=100)
    run_p.add_argument("--output", default="tests/artifacts")
    run_p.set_defaults(func=cmd_run)

    suite_p = sub.add_parser("suite", help="run a suite of policies")
    suite_p.add_argument("--policy", choices=POLICIES.keys())
    suite_p.add_argument("--all", action="store_true", help="run all policies")
    suite_p.add_argument("--seed", type=int, default=0)
    suite_p.add_argument("--runs", type=int, default=1)
    suite_p.add_argument("--max-steps", type=int, default=100)
    suite_p.add_argument("--output", default="tests/artifacts")
    suite_p.set_defaults(func=cmd_suite)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

