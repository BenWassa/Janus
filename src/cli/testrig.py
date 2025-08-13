"""Command line interface for the testing engine."""

from __future__ import annotations

import argparse
from pathlib import Path
from typing import List

from ..testing.policies import POLICIES
from .run_writer import write_run
from .build_index import build_index


def cmd_run(args: argparse.Namespace) -> None:
    for i in range(args.runs):
        seed = args.seed + i if args.seed is not None else i
        write_run(
            policy_name=args.policy,
            seed=seed,
            max_steps=args.max_steps,
            dominance_threshold=args.dominance_threshold,
            output_dir=Path(args.output),
        )

    build_index(Path(args.output))
    print(f"Completed {args.runs} runs for policy '{args.policy}'.")


def cmd_suite(args: argparse.Namespace) -> None:
    policies = POLICIES if args.all else {args.policy: POLICIES[args.policy]}
    for name, _ in policies.items():
        run_args = argparse.Namespace(
            policy=name,
            seed=args.seed,
            runs=args.runs,
            max_steps=args.max_steps,
            dominance_threshold=args.dominance_threshold,
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
    run_p.add_argument("--dominance-threshold", type=int, default=80)
    run_p.add_argument("--output", default="data/test_results")
    run_p.set_defaults(func=cmd_run)

    suite_p = sub.add_parser("suite", help="run a suite of policies")
    suite_p.add_argument("--policy", choices=POLICIES.keys())
    suite_p.add_argument("--all", action="store_true", help="run all policies")
    suite_p.add_argument("--seed", type=int, default=0)
    suite_p.add_argument("--runs", type=int, default=1)
    suite_p.add_argument("--max-steps", type=int, default=100)
    suite_p.add_argument("--dominance-threshold", type=int, default=80)
    suite_p.add_argument("--output", default="data/test_results")
    suite_p.set_defaults(func=cmd_suite)

    return parser


def main(argv: List[str] | None = None) -> None:
    parser = build_parser()
    args = parser.parse_args(argv)
    args.func(args)


if __name__ == "__main__":
    main()

