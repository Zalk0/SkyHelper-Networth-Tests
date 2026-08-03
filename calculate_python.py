import asyncio
import json
from dataclasses import asdict
from pathlib import Path

from aiohttp import ClientSession
from skyhelper_networth import ProfileNetworthCalculator
from skyhelper_networth.types import Networth

DATA_DIRECTORY = Path(__file__).parent.joinpath("data")
RESULT_DIRECTORY = Path(__file__).parent.joinpath("result_python")


async def calculate(prices: dict, user_data: dict) -> Networth:
    async with ClientSession() as session:
        return await ProfileNetworthCalculator(
            user_data["profile"],
            user_data["museum"],
            user_data["balance"],
            session=session
        ).get_networth(prices=prices, sort_items=True)


def main() -> None:
    RESULT_DIRECTORY.mkdir(exist_ok=True)
    prices = json.loads(DATA_DIRECTORY.joinpath("prices.json").read_bytes())

    for user_data in DATA_DIRECTORY.glob("*.json"):
        if user_data.name == "prices.json":
            continue
        data = json.loads(user_data.read_bytes())
        networth = asyncio.run(calculate(prices, data))
        RESULT_DIRECTORY.joinpath(user_data.name).write_text(json.dumps(asdict(networth)))


if __name__ == "__main__":
    main()
