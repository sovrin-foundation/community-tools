import asyncio
import logging
from aiohttp import web
from routes import setup_routes
from routes import setup_static_routes

from indy import wallet, pool

app = web.Application()
app['handles'] = {
    'pools': {
        'stagingnet': None,
        'buildernet': None
    },
    'wallet': None
}
WALLET = "stewardauto" #"test"
WALLETKEY = "stewardauto" #"test"
LOG_LEVEL = logging.INFO
LOGGER = logging.getLogger('Startup')

## - Functions - ##
async def open_handles():
    await pool.set_protocol_version(2)
    LOGGER.info("Opening steward_wallet")
    app['handles']['wallet'] = await wallet.open_wallet(f'{{"id": "{WALLET}"}}', f'{{"key": "{WALLETKEY}"}}')
    for pool_name in app['handles']['pools']:
        LOGGER.info(f"Connecting to pool: {pool_name}")
        app['handles']['pools'][pool_name] = await pool.open_pool_ledger(pool_name, None)

async def close_handles():
    LOGGER.info("Closing steward_wallet")
    await wallet.close_wallet(app['handles']['wallet'])
    for pool_name in app['handles']['pools']:
        LOGGER.info(f"Closing pool: {pool_name}")
        await pool.close_pool_ledger(app['handles']['pools'][pool_name])

## - Main - ##
logging.basicConfig(level=LOG_LEVEL)

LOOP = asyncio.get_event_loop()
LOOP.run_until_complete(open_handles())

setup_routes(app)
setup_static_routes(app)
web.run_app(app, host='127.0.0.1', port=8080)

LOOP = asyncio.new_event_loop()
LOOP.run_until_complete(close_handles())
LOOP.close()
