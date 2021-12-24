from pathlib import Path

import numpy as np
from gwosc import datasets

import conf
import utils


def download_baseline(dir: Path):
    runs = datasets.find_datasets(type="run")

    print("Downloading baseline 'noise' signals from runs", runs)

    run_times = {run: datasets.run_segment(run) for run in runs}

    N = 62

    for i in range(N):
        while True:
            run = np.random.choice(runs)

            print(f"Downloading noise {i}/{N} from run {run}...")
            run_start, run_end = run_times[run]

            time = np.random.randint(run_start, run_end)
            try:
                print("time =", time)
                utils.fetch_strains(time, dir)
                break
            except ValueError as e:
                print(e)
                print("Error. retrying...")
                continue

        print("Done.")


if __name__ == "__main__":
    download_baseline(conf.NOISE_DIR)
