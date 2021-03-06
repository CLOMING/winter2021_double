import asyncio


async def main_async():
    d3 = Double3SDK()
    d3.events.subscribe(["DRCamera.enable", "DRBase.status", "DRAPI.status"])
    d3.api.request_status()
    d3.base.request_status()
    d3.camera.enable(template=Template.screen, width=1152, height=720)

    while True:
        packet = d3.recv()
        if packet == None:
            continue

        print(packet)

if __name__ == "__main__":
    import os.path
    import sys
    sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
    from double3sdk.camera import Template
    from double3sdk import Double3SDK

    asyncio.run(main_async())
