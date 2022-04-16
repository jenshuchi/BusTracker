import os
import json
import aiohttp
import asyncio

async def get_route(session, bus_number, direction):
    # async with session.get(f"https://ptx.transportdata.tw/MOTC/v2/Bus/StopOfRoute/City/Taipei?%24filter=RouteName%2FZh_tw%20eq%20'{bus_number}'%20and%20Direction%20eq%20{direction}&%24top=30&%24format=JSON",
    #         headers={
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    #         }
    #     ) as response:

    #         if response.status != 200:
    #             print(f"Error: status={response.status}")

    #         data = await response.json()
    #         json.dumps(data, separators=(":", ","), indent=4)
    #         return data[0]["Stops"]
    with open("StopOfRoute_672.json", "r") as f:
        data = json.load(f)
    return data[0]["Stops"]


def get_target_stop_sequence(target_stop_name, stops):
    target_stop_sequence_num = None
    for stop in stops:
        if stop["StopName"]["Zh_tw"] == target_stop_name:
            target_stop_sequence_num = stop["StopSequence"]
            break
    return target_stop_sequence_num


async def get_running_buses(session, bus_number, direction):
    # async with session.get(f"https://ptx.transportdata.tw/MOTC/v2/Bus/RealTimeNearStop/City/Taipei?%24filter=RouteName%2FZh_tw%20eq%20'{bus_number}'%20and%20Direction%20eq%20{direction}&%24top=30&%24format=JSON",
    #         headers={
    #         "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36"
    #         }
    #     ) as response:

    #         if response.status != 200:
    #             print(f"Error: status={response.status}")

    #         return await response.json()
    import random
    i = random.randint(1, 4)
    with open(f"RealTimeNearStop_672-{i}.json", "r") as f:
        data = json.load(f)
    return data


def has_bus_near_target(target, buses):
    bus_location_diffs = [target - int(bus["StopSequence"]) for bus in buses]
    return any([d >=3 and d <= 5 for d in bus_location_diffs])


async def line_notify(session, access_token, message):
    async with session.post("https://notify-api.line.me/api/notify",
        headers={
            "Content-Type": "application/x-www-form-urlencoded",
            "Authorization": f"Bearer {access_token}"
        },
        data={
            "message": message
        }
    ) as response:
        if response.status == 200:
            print("notified")
        else:
            print(f"Error: {await response.json()}")


async def main():
    bus_number = "672"
    direction = 1
    target_stop_name = "博仁醫院"

    tokens = os.getenv("LINE_TOKENS").split(",")

    async with aiohttp.ClientSession() as session:
        stops = await get_route(session, bus_number, direction)
        target = get_target_stop_sequence(target_stop_name, stops)

        while True:
            buses = await get_running_buses(session, bus_number, direction)

            if has_bus_near_target(target, buses):
                for token in tokens:
                    asyncio.create_task(line_notify(session, token, f"Bus {bus_number} is coming"))

            await asyncio.sleep(10)


if __name__ == "__main__":
    asyncio.run(main())
