# SRBMiner: Benchmark -> Config Update
Update algos.txt with SRB miner benchmark results.


[SRB miner](https://www.srbminer.com/) has a benchmarking program that doesn't auto populate its algorithms config file with the benchmark results.
This script copies the values over.

PRs and issues welcome!

## Requirements
* python 3.7+


## Instructions
* Download the script `update_algos.py` and put it in the same directory as `algos.txt` and `benchmark_results.txt`.
* Run the script using python from the command prompt

## Development
Use `pytest` to run the test suite, and [Black](https://github.com/psf/black) to format `.py` files.
