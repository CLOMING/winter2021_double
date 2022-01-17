import asyncio


async def main_async():
    d3 = Double3SDK()
    d3.api.request_status()

    packet = d3.recv()
    print(packet)

if __name__ == "__main__":
    import os.path
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from double3sdk import Double3SDK

    asyncio.run(main_async())
