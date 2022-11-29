from mpi4py import MPI
import sys
from time import sleep
import sys

comm_world = MPI.COMM_WORLD
rank = comm_world.Get_rank()
size = comm_world.size
name = MPI.Get_processor_name()


def check_args():
    if len(sys.argv) != 2:
        abort_all_processes(
            "Usage:  mpiexec -n num_processes python3 main.py <input_file>"
        )


def abort_all_processes(error_message: str) -> None:
    print(f"Rank {rank}: {error_message}")
    sys.stdout.flush()
    comm_world.Abort()
