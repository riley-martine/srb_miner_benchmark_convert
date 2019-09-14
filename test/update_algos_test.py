import os
from pathlib import Path
from shutil import copyfile

from update_algos import main, read_algos, read_benchmarks, update_algos

BENCH = "test/fixtures/benchmark_results.txt"
ALGOS = "test/fixtures/algos.txt"


def test_read_bench():
    with open(BENCH, "r") as f:
        results = read_benchmarks(f.read())
    assert len(results) == 27
    assert results["upx2"] == 51598
    assert results["normal"] == 886


def test_read_algos():
    with open(ALGOS, "r") as f:
        algos = read_algos(f.read())
    algs_list = algos["algos"]
    assert len(algs_list) == 27
    assert {
        "algo": "alloy",
        "config": "Config\\config-alloy.txt",
        "hashrate": 665,
        "startup_script": "",
    } in algs_list


def test_update_algos():
    with open(BENCH, "r") as f:
        results = read_benchmarks(f.read())
    with open(ALGOS, "r") as f:
        algos = read_algos(f.read())
    new = update_algos(results, algos)

    assert {
        "algo": "alloy",
        "config": "Config\\config-alloy.txt",
        "hashrate": 666,
        "startup_script": "",
    } in new["algos"]


def test_integration(tmpdir):
    tmp_bench = tmpdir / Path(BENCH).name
    tmp_algos = tmpdir / Path(ALGOS).name

    copyfile(BENCH, tmp_bench)
    copyfile(ALGOS, tmp_algos)
    cwd = Path.cwd()
    os.chdir(tmpdir)

    main()

    # Backup successful
    with open(tmp_algos + ".bak", "r") as f:
        old_algos = read_algos(f.read())
    assert {
        "algo": "alloy",
        "config": "Config\\config-alloy.txt",
        "hashrate": 665,
        "startup_script": "",
    } in old_algos["algos"]

    with open(tmp_algos, "r") as f:
        new_algos = read_algos(f.read())
    assert {
        "algo": "alloy",
        "config": "Config\\config-alloy.txt",
        "hashrate": 666,
        "startup_script": "",
    } in new_algos["algos"]

    os.chdir(cwd)
