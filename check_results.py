import json
import os
import sys
from pathlib import Path

PYTHON_DIRECTORY = Path(__file__).parent.joinpath("result_python")
NODE_DIRECTORY = Path(__file__).parent.joinpath("result_node")


def main() -> int:
    status = 0
    output_table = "|MC UUID_Profile UUID|Python|Node|Unsoulbound Python|Unsoulbound Node|Same result|\n"
    for file in PYTHON_DIRECTORY.iterdir():
        same_result = True
        python_calc = json.loads(file.read_bytes())
        node_calc = json.loads(NODE_DIRECTORY.joinpath(file.name).read_bytes())
        if round(python_calc["networth"], 2) != round(
            node_calc["networth"], 2
        ) or round(python_calc["unsoulbound"], 2) != round(
            node_calc["unsoulboundNetworth"], 2
        ):
            status = 1
            same_result = False

        output_table += f"|{file.stem}|{python_calc['networth']}|{node_calc['networth']}|{python_calc['unsoulbound']}|{node_calc['unsoulboundNetworth']}|{'✅' if same_result else '❌'}|\n"
    print(output_table)
    if os.getenv("GITHUB_ACTIONS"):
        print(os.getenv("GITHUB_ACTIONS"))
        os.putenv("GITHUB_STEP_SUMMARY", output_table)
    return status


if __name__ == "__main__":
    sys.exit(main())
