import asyncio
from aiohttp import web
from routes import setup_routes
from routes import setup_static_routes

app = web.Application()
app['pool_lock'] = asyncio.Lock()
app['handles'] = {
    'pools': {
        'stagingnet': None,
        'buildernet': None
    },
    'wallet': None
}
setup_routes(app)
setup_static_routes(app)
web.run_app(app, host='127.0.0.1', port=8080)
