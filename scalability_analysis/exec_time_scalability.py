"""Monitoring of execution time with respect to kernel amount."""
import os
import sys

from caller_scalability_analysis import SCALABILITY_ANALYSIS

if len(sys.argv) > 1:
    num_threads = sys.argv[1]

if SCALABILITY_ANALYSIS == "threads":
    update_ = dict.fromkeys(
        [
            "NUMBA_NUM_THREADS",
            "MKL_NUM_THREADS",
            "OMP_NUM_THREADS",
            "OPENBLAS_NUM_THREADS",
            "NUMEXPR_NUM_THREADS",
        ],
        num_threads,
    )

    print(update_)
    print("Number of threads:", num_threads, ".")
    os.environ.update(update_)

import datetime
import pickle
import pandas as pd
from config import ITERATIONS
from config import MAX_THREADS_PROCESSES
from config import PERIOD
from caller_scalability_analysis import PATH_AUXINPUT_PARAMS
from caller_scalability_analysis import SCALABILITY_ANALYSIS
from respy.solve import _full_solution


if __name__ == "__main__":

    if SCALABILITY_ANALYSIS == "processes" and len(sys.argv) > 1:
        num_processes = int(sys.argv[1])

    input_params = pickle.load(open(PATH_AUXINPUT_PARAMS, "rb"))

    times = []
    for _j in range(ITERATIONS[SCALABILITY_ANALYSIS]):

        start = datetime.datetime.now()
        calc = _full_solution(
            input_params["wages"],
            input_params["nonpecs"],
            input_params["continuation_values"],
            input_params["period_draws_emax_risk"],
            input_params["optim_paras"],
        )
        end = datetime.datetime.now()
        print("Iteration", _j)

        times.append((end - start).microseconds)

    df_times = pd.DataFrame(times, columns=[f"{num_threads}"])

    number = MAX_THREADS_PROCESSES[SCALABILITY_ANALYSIS]
    if int(num_threads) > 1:
        (
            pd.read_pickle(
                f"./resources/times_df_{number}{SCALABILITY_ANALYSIS}_{PERIOD}.pickle"
            ).join(df_times, lsuffix="_")
        ).to_pickle(
            f"./resources/times_df_{number}{SCALABILITY_ANALYSIS}_{PERIOD}.pickle"
        )
    else:
        df_times.to_pickle(
            f"./resources/times_df_{number}{SCALABILITY_ANALYSIS}_{PERIOD}.pickle"
        )
