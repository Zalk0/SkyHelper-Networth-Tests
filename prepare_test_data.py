import asyncio
import json
from pathlib import Path

from aiohttp import ClientSession

HYPIXEL_API_KEY = ""
HEADERS = {"API-Key": HYPIXEL_API_KEY}
DATA_DIRECTORY = Path(__file__).parent.joinpath("data")
PROFILES = {
    ("debb9e1f6dcb4f5b83c291fd5388bb56", "1ed76b10-45f0-44b9-8f88-d5f748bbe15a"),
    ("87337a49538844ca93500e82b55fad21", "8a2eae9b-52f1-47e7-8629-d7ae82604e2b"),
    ("652cb092926b4c8592acb7e53550afa9", "8a2eae9b-52f1-47e7-8629-d7ae82604e2b"),
    ("dbbb83c48d934182900d53aa45c8307c", "ac259587-81d3-4d33-8eba-2982b0b183fc"),
    ("9b6bc607015b44d3b5fba76ef919ebb6", "7f739c12-2742-46a5-909b-f5050706e0c3"),
    ("1ea194333f1d41e3a447d361e1fee503", "0b5620e5-7dc8-4fbd-a86b-178b7362ca17"),
    ("2d6361a1df194d6c9f0378c700efc7f2", "6f4b7151-8fdd-41cf-8c41-ae5725e8f5cd"),
    ("33bf9bdf904743fe9b19d38195056ccf", "7ca80bc5-2a22-465f-a2b4-04e4b1d821f6"),
    ("0b1974a47bf94ab9bbc0c9c857e012d0", "0b1974a4-7bf9-4ab9-bbc0-c9c857e012d0"),
    ("56db5ce123984741b054af404e7a7fd0", "3d75ed46-6784-450f-a8ad-f36f20d26035"),
    ("33e1a3315ffd4ff2843084d620d69f4f", "3d75ed46-6784-450f-a8ad-f36f20d26035"),
    ("286056ef165c4a3b87b30f0d872c946d", "22674cd0-c151-492a-9577-7cfa48ff3783"),
    ("669ea7965e534a97bc07663136cd23f9", "7ca80bc5-2a22-465f-a2b4-04e4b1d821f6"),
    ("4855c53ee4fb4100997600a92fc50984", "00912956-3fd6-42ee-a166-3f649ceaf559"),
    ("dec987bbfa734d63bb9d566139232f81", "0f777340-a566-4a11-a55b-ee38b5478550"),
    ("88d65ced157b4e8d880175b705aff329", "fbecd1bd-d064-44a1-b816-54bc63863bd3"),
    ("b876ec32e396476ba1158438d83c67d4", "b876ec32-e396-476b-a115-8438d83c67d4"),
    ("1915444928b64d8b8973df8044f8cdb7", "d05a0e80-fa02-4f5a-9367-ca66135b7347"),
    ("91f57dfc7f5845c9a4920f6c16640038", "9bef8fd9-82a8-4a0c-ba47-c3f6dfe8f836"),
    ("b44d2d5272dc49c28185b2d6a158d80a", "6edb2eba-4dd5-4f11-965d-1062322ccd9c"),
    ("d705483c5157460dad39712e4d74dfe1", "a2c33a65-1b43-49ca-a6a5-8352bff58c22"),
}


async def get_prices() -> dict:
    async with (
        ClientSession() as session,
        session.get(
            "https://raw.githubusercontent.com/SkyHelperBot/Prices/main/pricesV2.json"
        ) as response,
    ):
        prices = await response.json(content_type=None)
    return prices


async def get_skyblock_profile(
    uuid: str, profile_id: str, session: ClientSession
) -> tuple[float, dict]:
    async with session.get(
        "https://api.hypixel.net/v2/skyblock/profiles",
        headers=HEADERS,
        params={"uuid": uuid},
    ) as response:
        profiles = await response.json()

    profile = next(
        profile
        for profile in profiles.get("profiles")
        if profile.get("profile_id") == profile_id
    )

    return (
        profile.get("banking", {}).get("balance", 0),
        profile.get("members").get(uuid),
    )


async def get_skyblock_museum(
    uuid: str, profile_id: str, session: ClientSession
) -> dict:
    async with session.get(
        "https://api.hypixel.net/v2/skyblock/museum",
        headers=HEADERS,
        params={"profile": profile_id},
    ) as response:
        museum = await response.json()

    return museum.get("members").get(uuid)


async def get_skyblock_data(uuid: str, profile_id: str) -> dict[str, dict | float]:
    async with ClientSession() as session:
        profile = await get_skyblock_profile(uuid, profile_id, session)
        return {
            "balance": profile[0],
            "profile": profile[1],
            "museum": await get_skyblock_museum(uuid, profile_id, session),
        }


def main():
    DATA_DIRECTORY.mkdir(exist_ok=True)

    prices = asyncio.run(get_prices())
    DATA_DIRECTORY.joinpath("prices.json").write_text(json.dumps(prices))

    for uuid, profile_id in PROFILES:
        data = asyncio.run(get_skyblock_data(uuid, profile_id))
        DATA_DIRECTORY.joinpath(f"{uuid}_{profile_id}.json").write_text(
            json.dumps(data)
        )


if __name__ == "__main__":
    main()
