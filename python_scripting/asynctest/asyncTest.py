#!/usr/bin/env python3
#sauce: https://pawelmhm.github.io/asyncio/python/aiohttp/2016/04/22/asyncio-aiohttp.html

import json
import requests
import time
import asyncio
from aiohttp import ClientSession

with open('betauia.net-11-10-2020.json') as read_file:
    parsed = json.load(read_file)
    domains = parsed.keys()

async def fetch(url, session):
    async with session.get(url) as response:
        return response.status

async def run(domains):
    tasks = []

    # Fetch all responses within one Client session,
    # keep connection alive for all requests.
    async with ClientSession() as session:
        for domain in domains:
            task = asyncio.ensure_future(fetch(f'http://{domain}', session))
            tasks.append(task)

        responses = await asyncio.gather(*tasks)
        # you now have all response bodies in this variable
        print(responses)

def print_responses(result):
    print(result)

start = time.time()
loop = asyncio.get_event_loop()
future = asyncio.ensure_future(run(parsed.keys()))
loop.run_until_complete(future)
end = time.time()

print(f'Async: {end-start}')

start = time.time()
sync_tasks = []
for domain in domains:
    sync_tasks.append(requests.get(f'http://{domain}', timeout=2).status_code)
print(sync_tasks)
end = time.time()

print(f'Sync: {end-start}')