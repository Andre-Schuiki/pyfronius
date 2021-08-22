#!/usr/bin/env python
"""Basic usage example and testing of pyfronius."""
import asyncio
import logging
import sys
import aiohttp

import pyfronius


async def main(loop, host):
    timeout = aiohttp.ClientTimeout(total=10)
    async with aiohttp.ClientSession(loop=loop, timeout=timeout) as session:
        fronius = pyfronius.Fronius(session, host)

        # use the optional fetch parameters to configure
        # which endpoints are acessed
        # NOTE: configuring the wrong devices may cause Exceptions to be thrown
        res = await fronius.fetch(
            active_device_info=True,
            logger_info=True,
            power_flow=True,
            system_meter=True,
            system_inverter=True,
            system_storage=True,
            device_meter=frozenset([0]),
            # storage is not necessarily supported by every fronius device
            device_storage=frozenset([0]),
            device_inverter=frozenset([1]),
            loop=loop,
        )
        for r in res:
            print(r)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG)
    loop = asyncio.get_event_loop()
    loop.run_until_complete(main(loop, sys.argv[1]))
