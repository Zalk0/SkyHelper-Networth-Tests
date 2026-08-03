import json
from pathlib import Path

PYTHON_DIRECTORY = Path(__file__).parent.joinpath("result_python")
NODE_DIRECTORY = Path(__file__).parent.joinpath("result_node")


def main() -> None:
    for file in PYTHON_DIRECTORY.iterdir():
        python_calc = json.loads(file.read_bytes())
        node_calc = json.loads(NODE_DIRECTORY.joinpath(file.name).read_bytes())
        if round(python_calc["networth"], 2) != round(node_calc["networth"], 2):
            print(file.name)
            print("Networth: Python:", python_calc["networth"], "Node:", node_calc["networth"])
        if round(python_calc["unsoulbound"], 2) != round(
            node_calc["unsoulboundNetworth"], 2
        ):
            print(file.name)
            print("Unsoulbound: Python:", python_calc["unsoulbound"], "Node:", node_calc["unsoulboundNetworth"])


if __name__ == "__main__":
    main()
