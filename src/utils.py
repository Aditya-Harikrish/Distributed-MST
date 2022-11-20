from mpi4py import MPI
import sys
from itertools import islice
import logging
from time import sleep
import sys

comm = MPI.COMM_WORLD
rank = comm.Get_rank()
size = comm.size


def check_args():
    if len(sys.argv) != 2:
        abort_all_processes(
            "Usage:  mpiexec -n num_processes python3 main.py <input_file>"
        )


def abort_all_processes(error_message: str) -> None:
    print(f"Rank {rank}: {error_message}")
    sys.stdout.flush()
    comm.Abort()
