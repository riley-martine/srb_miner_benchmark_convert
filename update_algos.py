#!/usr/bin/env python3
"""Convert benchmark results to algorithm file"""

import json
import sys
from pathlib import Path
from shutil import copyfile
from typing import Dict, List, Union

Algos = Dict[str, List[Dict[str, Union[str, int]]]]


def read_benchmarks(file_contents: str) -> Dict[str, int]:
    """Read in benchmark results."""
    out: Dict[str, int] = {}
    pairs = file_contents.split("\n\n")
    for pair in pairs:
        pair = pair.strip()
        if not pair:
            continue
        algo, bench = pair.split("\n")
        out[algo] = int(bench)
    return out


read_algos = json.loads


def update_algos(results: Dict[str, int], algos: Algos) -> Algos:
    """Return a copy of algos, updated with benchmark results."""
    bench_algos = results.keys()
    algo_names = [algo["algo"] for algo in algos["algos"]]
    for bench_algo in bench_algos:
        if bench_algo not in algo_names:
            print(f"Algo {bench_algo} in benchmark but not algos.txt.")
    for algo_name in algo_names:
        assert isinstance(algo_name, str)
        if algo_name not in bench_algos:
            print(f"Algo {algo_name} in algos.txt but not benchmark.")

    for algo in algos["algos"]:
        algo_name = algo["algo"]
        assert isinstance(algo_name, str)
        if algo_name in results:
            algo["hashrate"] = results[algo_name]
    return algos


def main() -> None:
    benchfile, algofile = Path("benchmark_results.txt"), Path("algos.txt")
    if not benchfile.exists():
        print(f"Cannot find {str(benchfile)}, aborting.")
        sys.exit(1)
    if not algofile.exists():
        print(f"Cannot find {str(algofile)}, aborting.")
        sys.exit(1)

    with benchfile.open("r") as benchmarks:
        results = read_benchmarks(benchmarks.read())
    with algofile.open("r") as algos:
        current_algos = read_algos(algos.read())

    new_algos = update_algos(results, current_algos)
    copyfile(algofile, f"{algofile}.bak")
    with algofile.open("w") as algos:
        algos.write(json.dumps(new_algos, indent=4))


if __name__ == "__main__":
    main()
