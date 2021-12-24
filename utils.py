import os
import re

from itertools import groupby
from pathlib import Path
from typing import Tuple, List
from urllib.request import urlretrieve

import matplotlib.pyplot as plt

from gwosc import datasets
from gwosc.timeline import get_segments
from gwosc.locate import get_urls
from gwpy.timeseries import TimeSeries

from conf import dT, TIMESTAMP_PATTERN


def get_all_events():
    data = datasets.find_datasets(type="event")
    all_events = [s for s in data if s.startswith("GW")]

    events = list(sorted([list(sorted(e))[0] for _, e in groupby(all_events, key=lambda s: s.split("-")[0])]))
    
    return events


def fetch_strains(timestamp: int, folder: Path) -> Tuple[Path, Path]:
    """Downloads H1 and L1 strains for [-dt,+dt] from a given timestamp
        and stores it on disk, and returns their paths."""
  
    urls = get_urls('H1', int(timestamp)-dT, int(timestamp)+dT) + \
            get_urls('L1', int(timestamp)-dT, int(timestamp)+dT)

    filtered_urls = [s for s in urls if s.endswith("-4096.hdf5")]
    
    print(list(map(os.path.basename, filtered_urls)))
    
    h1_path, l1_path = None, None

    for url in filtered_urls:
        filename = os.path.basename(url)
        filepath = folder / filename
        
        if filename.startswith("H-H1"):
            h1_path = filepath
        elif filename.startswith("L-L1"):
            l1_path = filepath
        else:
            raise Exception("Invalid file received.")

        if filepath.exists():
            continue
        
        print("Downloading", filename)
        urlretrieve(url, filepath)
    
    return h1_path, l1_path


    
def get_file_timestamp(file: Path) -> int:
    match = TIMESTAMP_PATTERN.search(file.name)
    return int(match.group(1))


def get_file_pairs(folder: Path) -> List[Tuple[Path, Path]]:
    all_files = sorted(folder.glob("*.hdf5"), key=lambda f: f.stem[6:])
    
    groups = groupby(all_files, key=lambda f: f.stem[6:])
    
    groups = groupby(all_files, key=lambda f: f.stem[6:])
    
    pairs = []
    for key, files in groups:
        files = list(files)

        if len(files) != 2:
            raise Exception("Files corrupt: ", files)
        
        h1_file, l1_file = None, None

        for file in files:
            if file.stem.startswith("H-H1"):
                h1_file = file
            elif file.stem.startswith("L-L1"):
                l1_file = file
        
        assert h1_file and l1_file
                
        pairs.append([h1_file, l1_file])
    
    return pairs


def plot_qtrans(row: Tuple[TimeSeries, TimeSeries], t=None, plot_dt=2, label=""):
    """
    Plot Q Trans of H1 and L1 strains.
    
    If t0 is None, it is set to the center of the TimeSeries pairs - plot_dt/2.
    """
    
    h1_ts, l1_ts = row
    
    if t is None:
        t = h1_ts.times[0].value + (h1_ts.duration.value - plot_dt) / 2.

    plt.figure()
    hq = h1_ts.q_transform(outseg=(t - plot_dt / 2, t + plot_dt / 2))
    fig4 = hq.plot()
    ax = fig4.gca()
    fig4.colorbar(label="Normalised energy")
    ax.grid(False)
    ax.set_yscale('log')
    plt.title(f"H1 strain {label}")
    plt.show()

    plt.figure()
    hq = l1_ts.q_transform(outseg=(t - plot_dt / 2, t + plot_dt / 2))
    fig5 = hq.plot()
    ax = fig5.gca()
    fig5.colorbar(label="Normalised energy")
    ax.grid(False)
    ax.set_yscale('log')
    plt.title(f"L1 strain {label}")
    plt.show()