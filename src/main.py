import utils as u
from utils import check_args, comm_world
from graph import Graph
from mpi4py import MPI
import logging
import sys


def main() -> None:
    logging.basicConfig(level=logging.DEBUG)
    check_args()
    g = Graph(sys.argv[1])
    # logging.debug(g)

    ans: set[tuple[int, int, int]] = set()  # Edges found Set

    iter = 1
    while not g.dsu.allsame():  # checking whether all belong to same segement
        # logging.debug(iter)
        iter = iter + 1

        # Finding MOE Iindiviuallly
        for a, vp in g.graph.items():
            vp.moe_weight = float("inf")
            vp.moe_start = a
            for v in g.graph[a].neighbours:
                if not g.belong_to_same_fragment(v[0], a) and (
                    v[1] < vp.moe_weight or (v[1] == vp.moe_weight and v[0] < vp.moe)
                ):
                    vp.moe = v[0]
                    vp.moe_weight = v[1]

        # Barrier 1
        comm_world.Barrier()

        # All Nodes
        for i in range(g.n):

            """
            If vertex i belongs to process
                Send or merge
            Else
                Recieve and merge
            """
            if g.belongs_to_this_process(i):
                parent_process_id = g.process_of_vertex(g.dsu.find_set(i))
                """
                If fragment head doesnt belong to proces
                    Send a tuple(moe,moe_weight,moe_start) to fragment head
                Else If fragment Head belongs to process and moe!=-1
                    Compare moe_weight with parent
                """
                if u.rank != parent_process_id:
                    req = comm_world.isend(
                        [
                            g.graph.get(i).moe,
                            g.graph.get(i).moe_weight,
                            g.graph.get(i).moe_start,
                        ],
                        dest=parent_process_id,
                    )
                    req.wait()
                elif g.graph.get(i).moe != -1:
                    parent_id = g.dsu.find_set(i)

                    if g.graph.get(i).moe_weight < g.graph.get(
                        parent_id
                    ).moe_weight or (
                        g.graph.get(i).moe_weight == g.graph.get(parent_id).moe_weight
                        and i < parent_id
                    ):

                        g.graph.get(parent_id).moe = g.graph.get(i).moe
                        g.graph.get(parent_id).moe_weight = g.graph.get(i).moe_weight
                        g.graph.get(parent_id).moe_start = g.graph.get(i).moe_start

            elif g.process_of_vertex(g.dsu.find_set(i)) == u.rank:

                req = comm_world.irecv(source=g.process_of_vertex(i))
                moe = req.wait()
                parent_id = g.dsu.find_set(i)

                if moe[1] != -1:
                    if moe[1] < g.graph.get(parent_id).moe_weight or (
                        moe[1] == g.graph.get(parent_id).moe_weight
                        and moe[0] < g.graph.get(parent_id).moe
                    ):

                        g.graph.get(parent_id).moe = moe[0]
                        g.graph.get(parent_id).moe_weight = moe[1]
                        g.graph.get(parent_id).moe_start = moe[2]

        comm_world.Barrier()

        merge = set()
        iterate = set()
        for i in g.dsu.parent:
            iterate.add(g.dsu.find_set(i))

        for i in iterate:
            if g.belongs_to_this_process(i):
                if g.graph.get(i).moe != -1:
                    # merge fragment
                    x = min(g.dsu.parent[i], g.dsu.parent[g.graph.get(i).moe])
                    y = max(g.dsu.parent[i], g.dsu.parent[g.graph.get(i).moe])
                    merge.add((x, y))
                    # choose edges
                    x = min(g.graph.get(i).moe_start, g.graph.get(i).moe)
                    y = max(g.graph.get(i).moe_start, g.graph.get(i).moe)
                    ans.add((x, y, g.graph.get(i).moe_weight))

        merge_round = set()
        for x in merge:
            merge_round.add(x)
        comm_world.Barrier()

        for i in range(u.size):
            if u.rank == i:
                data = len(merge)
                merge_list = list(merge)
            else:
                data = None
            data = comm_world.bcast(data, root=i)
            for j in range(0, data):
                if u.rank == i:
                    data_temp = merge_list[j]
                else:
                    data_temp = None
                data_temp = comm_world.bcast(data_temp, root=i)
                merge_round.add(data_temp)

        comm_world.Barrier()

        for request in merge_round:
            g.dsu.union_sets(request[0], request[1])

        for a, vp in g.graph.items():
            delete_set = set()
            for v in g.graph[a].neighbours:
                if g.dsu.parent[a] == g.dsu.parent[v[0]]:
                    delete_set.add(v)

            for x in delete_set:
                g.graph[a].neighbours.remove(x)

        # comm_world.Barrier()
        # this_comm = comm_world.Split(color=)
        # print(f'{rank=}, {g.start_node=}, {g.num_nodes=}')
        # logging.debug(g)
        # logging.debug(ans)
        # break
    comm_world.Barrier()

    # logging.debug('Mergeing Answer Step')
    # print('Mergeing Answer Step')

    for i in range(1, u.size):
        if u.rank == i:
            data = len(ans)
            ans_list = list(ans)
        else:
            data = None
        data = comm_world.bcast(data, root=i)

        for j in range(data):
            # logging.debug({i,j})
            if u.rank == i:
                data_temp = ans_list[j]
                comm_world.send(data_temp, dest=0)
            elif u.rank == 0:
                data_temp = comm_world.recv(source=i)
                ans.add(data_temp)
        comm_world.Barrier()

    if u.rank == 0:
        logging.debug(ans)
        if len(ans) + 1 == g.n:
            print("MST Found")
        else:
            print("Error: MST not found")
            # print(len(ans))


if __name__ == "__main__":
    main()
