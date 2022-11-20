from graph import Graph
from utils import *


def main():
    logging.basicConfig(level=logging.DEBUG)
    check_args()
    graph = Graph(sys.argv[1])
    logging.debug(graph)


if __name__ == "__main__":
    main()
