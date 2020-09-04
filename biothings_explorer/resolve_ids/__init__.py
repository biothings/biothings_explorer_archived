from aiohttp import ClientSession, TCPConnector
import asyncio

from .dispatch import Dispatcher
from .utils import generateFailedResponse


async def asyncQuery(inputIDs, session=None):
    """Asynchronously make a list of API calls."""
    responses = {}
    if not session:
        async with ClientSession(connector=TCPConnector(ssl=False)) as session:
            dp = Dispatcher(inputIDs, session)
            dp.dispatch()
            for task in dp.tasks.values():
                res = await asyncio.gather(*task)
                for _res in res:
                    responses.update(_res)
            return responses
    else:
        dp = Dispatcher(inputIDs, session)
        dp.dispatch()
        if dp.invalid and isinstance(dp.invalid, dict):
            for semantic_type, curies in dp.invalid.items():
                if curies and len(curies) > 0:
                    for curie in curies:
                        responses[curie] = generateFailedResponse(curie, semantic_type)
        for task in dp.tasks.values():
            res = await asyncio.gather(*task)
            for _res in res:
                if _res:
                    responses.update(_res)
        return responses


def syncQuery(inputIDs, loop=None):
    if not loop:
        loop = asyncio.new_event_loop()
    return loop.run_until_complete(asyncQuery(inputIDs))
